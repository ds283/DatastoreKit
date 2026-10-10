# Prompt 08b — dispose engines on a refused open

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 08a landed (`f938844`) and was reviewed (`2123445`).
- `git status` is clean in this repository, and `origin/main` is an ancestor of `main`.

**Closes:** `[05-a-refused-open-leaves-its-engines-undisposed]`, assigned here by U33 and U35.
**Narrows:** nothing. **Changes:** nothing. **Opens:** only what the work finds.

**Recommended model:** **Opus.**
- The code is one guard and one method.
- The weight is in the test: it must count connections deterministically, without the garbage
  collector, and fail on the unfixed layer for the reason the issue gives.
- The fix runs on every refused open in the suite, so the review reads every place it reaches.

**Read first:**

1. [`README.md`](README.md): §1, §2 (rows 08b–11), §4, §5 (rules 4, 6, 7, 9 and 10), §6.2
   (U33–U37).
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`.
3. The board's §3 entry for the issue, in full, and its review of 08a.
4. Log 05 §4, where the issue was measured, and log 08a §8.
5. The layer:
   - `datastorekit/SQL/ShardedPool.py`: `__init__` (`:95-360`), its read-only branch at
     `:203-209` and the read-write open to `:360`; `_open_read_only` (`:479-590`); `__exit__`
     (`:762-774`); `_create_engine` (`:776-849`); `_refuse_a_primary_that_differs` (`:851-878`,
     the connection at `:869`); `_write_shard_data` (`:880`, the first use of the engine at
     `:881`);
   - `datastorekit/SQL/Datastore.py`: `__init__` (`:39-147`), `__exit__` (`:351-360`) and
     `_create_engine` (`:363-378`, the inspector's connection at `:378`).
6. The fixtures: `datastorekit/tests/standin_pool.py` (`_Method.remote` `:102-145`, how a fault
   and a hook act; `_Options.remote` `:169-176`, which builds an actor at once;
   `StandinCluster.fault` `:277`); `datastorekit/tests/client/build.py` (`open_pool`); and
   `datastorekit/tests/test_unsupplied_sharded_table.py`, the model of a test that reopens through
   `ShardedPool(...)` itself.
7. [`docs/client-contract.md`](../../docs/client-contract.md): its header and §9.

Line numbers here are the package's at `2123445`, whose `datastorekit/` is `f938844`'s.

---

## 1. What is wanted

When a pool's open is refused, or abandoned by an exception, the SQLAlchemy engines it made are
never disposed. Each engine's pooled SQLite connection is closed only when the garbage collector
reaches it. Python 3.13 reports each as a `ResourceWarning`; 3.12 reports nothing, but the
behaviour is the same. A long-lived process that retries refused opens holds a file descriptor per
engine until the collector runs.

**08b makes the pool's constructor close what it made when it raises**: every actor built so far
is closed by its own `__exit__`, and the pool's engine is disposed. Then the exception propagates
unchanged. A test module counts the connections a refused open makes and requires every one
closed when the exception reaches the caller.

**Nothing the layer writes changes.** No refusal is added or removed, and no message changes. An
open that succeeds behaves exactly as before.

08b changes no prose beyond the lines it adds (09 rewrites the package's prose), and no file under
`docs/adoption/` (10 adds the addenda, U37). It makes no tag and pushes nothing.

### 1.1 The measurement, at `2123445`

The planner re-ran log 05 §4's measurement at `2123445` in `venv/`. `sqlite3.connect` and
`sqlite3.dbapi2.connect` were wrapped with a `factory=` subclass that marks `close()` and counts,
on `__del__`, any connection never closed. To that measurement the planner added which pool or
actor object opened each connection, and whether that object's constructor raised. Over the 469,
41,213 connections were opened, and **109** were never closed. That is log 05's 105 plus four
from 08a's constructor test. None was still alive after the run.

| Opened at | Never closed | Whose |
|---|---|---|
| `SQL/ShardedPool.py:869` (`_refuse_a_primary_that_differs`; read-write 55, through `_open_read_only` 7) | 62 | the pool's engine, in a pool whose constructor raised |
| `SQL/Datastore.py:378` (`_create_engine`'s `sqla.inspect`) | 39 | an actor's engine, in a pool whose constructor raised after building it |
| `SQL/Datastore.py:378` | 2 | an actor built directly by a test and never exited: `test_version_row_at_open.TestInsertBeforeSetVersion`'s two tests (`bare_actor`, `:474`) |
| `SQL/ShardedPool.py:881` (`_write_shard_data`, a new store) | 6 | the pool's engine, in a pool whose constructor raised |

So **107 of the 109 are a raised constructor's**, and 2 are a test's. No actor's own constructor
raised in the suite. The exceptions the raised constructors gave were `ReplicatedDivergence`,
`RuntimeError`, `StandinActorDied`, `StoreSchemaMismatch`, `SimulatedDeath` and `ReadOnlyWrite`.

---

## 2. What to change

### 2.1 The constructor's open, guarded (`ShardedPool.py:200-360`)

`__init__` sets its attributes (`:138-201`), then opens the store: read-only (`:203-209`) or
read-write (`:211-360`). The open moves into a method of its own, and `__init__` calls it under a
guard:

```python
        # the version row of version_label, found or written once every actor exists
        self._version = None

        try:
            self._open(version_label, drop_tables, read_table_config, read_only)
        except BaseException:
            self._close_refused_open()
            raise

    def _open(self, version_label: str, drop_tables, read_table_config, read_only):
        """<one or two sentences: the open, after the attributes are set; if it raises,
        __init__ closes what it made>"""
        # A READ-ONLY POOL (prompts/a3-v2-readiness, prompt 03). It opens an existing store with
        ...
```

- **The open's lines do not move or change.** `__init__`'s body and a method's body share an
  indentation, so the `def _open` line goes immediately before the read-only comment (`:203`), and
  every line from there to `:360` stays where it is, unchanged. `git diff` of the file shows only
  added lines: the guard, the `def` with its docstring, and §2.2's method.
- **The four arguments are the open's only free names** that are not module globals or
  attributes. The planner checked this with `ast`: the read-only branch reads `read_only` and
  `drop_tables`, and the rest reads `version_label` and `read_table_config`. Omitting `read_only`
  gives `NameError` on every open (probed: 171 errors).
- **`BaseException`, not `Exception`**, so that an open abandoned by `KeyboardInterrupt` or
  `SystemExit` is closed too. §2.3's test 10 pins this.
- `return` in the read-only branch now returns from `_open`, as it returned from `__init__`.

### 2.2 `_close_refused_open`

A new method of `ShardedPool`, placed after `_open`:

```python
    def _close_refused_open(self) -> None:
        """<docstring: what it closes, as below, and why nothing it meets is raised>"""
        shards = self._shards if isinstance(self._shards, dict) else {}
        refs = []
        for shard in shards.values():
            try:
                refs.append(
                    shard.__exit__.remote(exc_type=None, exc_val=None, exc_tb=None)
                )
            except Exception:
                pass
        for ref in refs:
            try:
                ray.get(ref)
            except Exception:
                pass
        engine = getattr(self, "_engine", None)
        if engine is not None:
            try:
                engine.dispose()
            except Exception:
                pass
```

- **The actors are closed as the pool's `__exit__` closes them** (`:763-768`), by their own
  `__exit__`: the engine disposed, the serial manager and the profile batcher cleaned up
  (`Datastore.py:351-360`). Every call is submitted before any is waited for, so under Ray they
  run in parallel.
- **`self._shards` is the shard count until the actors exist** (`:169`, then the dict at
  `:304-320` or `:545-562`). Before that there is no actor to close, so the guard is needed. With
  the guard removed, every refusal made before the actors exist raises `AttributeError` in place of
  its own exception (§4.4 (f)).
- **`self._engine` does not exist until `_create_engine` runs.** `__init__` never sets it to
  `None`, so `getattr` is needed. A refusal before it (`:213-235`) has nothing to dispose.
- **Nothing `_close_refused_open` meets is raised**, and it prints nothing. The exception the
  caller sees is the open's own. An actor that is dead under Ray raises `RayActorError` from its
  `__exit__`; under the stand-in, a faulted `__exit__` returns `StandinActorDied`. Neither
  replaces the open's exception.
- **The caller's profile agent is not cleaned up.** The pool's `__exit__` calls
  `profile_agent.clean_up` (`:770-771`), which disposes the agent's own engine; but the agent is
  the caller's, given to the constructor, and outlives a refused pool. The docstring says so.
- **The broker is not touched.** It holds no engine.

Probed by the planner, at `2123445` with §2.1 and §2.2 applied:
- in `venv/`, `Ran 469 tests … OK`; the measurement of §1.1 gives **2** never closed, both
  `TestInsertBeforeSetVersion`'s;
- at the high end (Python 3.13.16 / Ray 2.55.1 / SQLAlchemy 2.0.46), `Ran 469 tests … OK`, with
  **4** `ResourceWarning` lines (those two connections). Before, it was 184–214 lines.

### 2.3 The test: `datastorekit/tests/test_refused_open_closes_engines.py`

A new module. It is not ported, and is not added to `PORTED`.

**How it counts.** A context manager of the module's own, around the open only. It replaces
`sqlite3.connect` and `sqlite3.dbapi2.connect` with a wrapper that passes `factory=` a subclass of
`sqlite3.Connection` whose `close()` sets a flag, and keeps every connection made. On exit it
restores both attributes. SQLAlchemy's SQLite dialect looks up `connect` on `sqlite3.dbapi2` when
it connects, so the layer's engines are counted along with its raw `sqlite3.connect` calls. Log 05
§4 found that no caller in the suite passes a `factory=` of its own. The count does not wait for
the collector: a connection is closed when its flag is set, at the moment the exception reaches
the test.

Every test runs inside `cluster.active()` with stdout captured, on a store in a `tempfile`
directory that a stand-in pool wrote and closed *before* the counting begins. Each test also
requires that at least one connection was counted, so that none passes vacuously. A test that
reopens with arguments other than the registry's calls `ShardedPool(...)` itself, as
`test_unsupplied_sharded_table` does.

At least these tests (the planner probed each, before and after §2.1–§2.2):

| # | The open | Refused by | Unfixed: unclosed | Fixed |
|---|---|---|---|---|
| 1 | read-write; the primary gains a table (`CREATE TABLE extra (x INTEGER)` through `sqlite3`) | `StoreSchemaMismatch`, before any actor | 1 of 1 | 0 |
| 2 | read-write; `sharded_tables` lacks `Sample` | the mismatch `RuntimeError` (08a's) | 1 of 1 | 0 |
| 3 | read-write; shard 1's `version` rows deleted through `sqlite3` | `ReplicatedDivergence`, at the check at open | 1 of 10 | 0 |
| 4 | read-only; a `version_label` the store lacks | `ReadOnlyMiss`, before any actor | 1 of 15 | 0 |
| 5 | read-write; `read_table_config={"Sample": {"tables_arg": False}}` | `RuntimeError` "It is only possible to configure a read-table method for a replicated table", **after the actors** (`:333-339`) | 4 of 13 | 0 |
| 6 | read-only; the same `read_table_config` | the same, after the actors (`:578-584`) | 4 of 16 | 0 |
| 7 | a **new** store; `cluster.controller = 0` and `cluster.fault(0, "object_get", "version", "before")` | `StandinActorDied` at the version write, after the actors | 4 of 7 | 0 |
| 8 | as 5, with `cluster.fault(1, "__exit__", None, "after")` | test 5's `RuntimeError`, **not** the fault's `StandinActorDied` | 4 of 13 | 0 |
| 9 | as 5, with `cluster.fault(1, "__exit__", None, "before")` | test 5's `RuntimeError` | 4 of 13 | **1**: shard 1's, whose `__exit__` never ran |
| 10 | as the registry's open, with a hook raising `KeyboardInterrupt` at the first `read_largest_store_ids` call, `"before"` | `KeyboardInterrupt`, after the actors (an abandoned open) | 4 of 13 | 0 |
| 11 | the registry's open, succeeding; then `cluster.close_pool` | — | 4 open while the pool is open, 0 after | the same |

- **Each refusal test also asserts the exception's type and its message** (whole, or by a
  substring that names the refusal), so that a cleanup that replaced the exception would fail it.
- **Test 9's leftover connection is closed by the test**, from the counted list, in its cleanup,
  so that the module itself leaves nothing unclosed. The test says why one is expected: under Ray
  a dead actor's process is gone, and with it the connection.
- **Test 11 pins that the guard runs only on failure.** A pool that opens keeps its engines'
  connections open until it is closed (4 counted open: the pool's engine and the three actors').
  Under §4.4 (g) they are 0.
- Ray is never initialised: a `tearDownModule` and each test's `tearDown` say so, as 08a's
  modules do.

The exact names, the split into classes and any further test are the agent's. The log lists each
test with what it pins, and its result on the unfixed layer.

Every test meets README §5 rule 7: no Ray, no client, no store outside a `tempfile` directory. The
module's names, docstrings and strings name no client (`CLAUDE.md`).

### 2.4 The measurement, again

Re-run §1.1's measurement over the whole suite, at both ends, after the fix. The planner's probe
was not committed; the agent writes its own in the session scratchpad, as log 05 §4 describes,
and records it in the log. Expected:
- the 469 + N pass;
- exactly **2** connections never closed, both `TestInsertBeforeSetVersion`'s;
- none from a constructor that raised;
- none from the new module (test 9's is closed by the test).

**Those two are not 08b's to fix.** They are actors that a ported test (03b) builds directly and
never exits. Changing `bare_actor` is a change to a ported test's fixture, and nothing in the
layer can close an actor its caller keeps. Record them under "Observations not acted on"; they
open no issue.

### 2.5 The contract: §9.2 (`docs/client-contract.md`)

Below 08a's header line, add a line saying that §9.2 is measured from the package at 08b's tree.
Do not rewrite 08a's line (`CLAUDE.md` rule 6). Add **§9.2 (prompt 08b)**, in §9.1's form: one row,
"An open that raises", with:
- what it supersedes: no row, since §1–§8 never said what a refused open leaves open;
- what the layer now does, at 08b's tree, citing the guard, `_open`, `_close_refused_open` and the
  pool's `__exit__` it mirrors;
- the test module.

No other line of the contract changes. There is no marker, since nothing is superseded.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **`venv/`'s `datastorekit` is an editable install of this checkout.** A probe run from a
   scratch copy imports the checkout unless the copy comes first on `sys.path`. Print
   `datastorekit.__file__` in every probe.
2. **The unfixed layer is the reference for every test.** Write the module, run it on the unfixed
   layer, and record that tests 1–10 fail on their counts. Test 11 passes on both trees, as a
   pin. Only then apply the fix. Use a scratch export for the unfixed run, not `git stash`.
3. **The stand-in builds an actor at once.** Under Ray, an actor constructor's exception surfaces
   at the first `ray.get`, by which time `self._shards` is the dict. Under the stand-in it raises
   inside the comprehension at `:304-320`, so `self._shards` is still the count, and the actors
   built before it in that comprehension are not closed. No test of the suite reaches this
   (§1.1: no actor's constructor raised). It is not 08b's to change: building the dict
   incrementally would move the open's lines (§2.1). Record it under "Observations not acted on".
4. **The cleanup is visible in `cluster.calls`.** A refused open after the actors now records one
   `__exit__` call per actor. No existing test reads `cluster.calls` after a refused open; the 469
   pass. If one does, stop (§6).
5. **The counting wrapper must be restored.** Restore both `sqlite3` attributes in `finally`, or
   every later test of the run is counted.
6. **No other line of `ShardedPool.py` changes**, and no line of `Datastore.py` changes. `git
   diff` shows only added lines in `ShardedPool.py` (§2.1).
7. **Prose.** Do not rewrite comments or docstrings outside the lines you add. That is 09's
   (`[01-package-prose-names-sgks-layout]`), and the guard's `KNOWN_HITS` stays at its one entry.
   The new docstrings name no client and no SGK path.
8. **Line numbers move.** Every line from `:202` on moves down. Contract and board citations made
   before 08b are of their own trees. Cite 08b's tree in §9.2 and in the log.

---

## 4. Verification

1. **The suite, in `venv/`** (Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39): `Ran 469 tests
   … OK` before. After, `469 + N` OK, where N is the loader's count for the new module. The count
   falls nowhere.
2. **The high end**, in a fresh venv in the session scratchpad: Python 3.13.16 / Ray 2.55.1 /
   SQLAlchemy 2.0.46, made with `uv pip install --offline` from the cache 05's work filled, with a
   `git archive` of your tree installed editable. Expect `469 + N` OK. Record the
   `ResourceWarning` lines (the planner's: 4 over the 469). **No download**; a pin that does not
   resolve offline is a stop.
3. **The checks.**
   - `compare_ported_tests.py` exits 0 with "20 module(s) … 1 test(s) declared not ported",
     unchanged.
   - `black --check datastorekit docs` leaves 69 files unchanged (68 + the module).
   - The layer guard passes with `KNOWN_HITS` at its one entry.
   - §2.4's measurement at both ends.
4. **The deliberate-breakage record.** Each is a diff to `ShardedPool.py`, applied in a scratch
   copy, never committed. Record which tests fail under each, and the verdict over the whole suite.
   The planner's probes give:
   - **(a)** the guard removed (`self._open(...)` called bare): tests 1–10 fail; the 469 pass.
     The 469 also pass under (b)–(e) and (g): no existing test counts connections, so only the new
     module catches those.
   - **(b)** no actor closed (`shards = {}`): tests 5–10 fail (3 left open; test 9 also has 3);
     tests 1–4 pass.
   - **(c)** the engine not disposed: tests 1–10 fail (1 left open; test 9 has 2).
   - **(d)** an actor's `__exit__` failure raised (the `try` around `ray.get(ref)` removed): tests
     8 and 9 fail, with `StandinActorDied` in place of the open's `RuntimeError`.
   - **(e)** `except Exception` in place of `BaseException`: test 10 fails (4 left open).
   - **(f)** the `isinstance` guard removed (`shards = self._shards`): tests 1–4 fail with
     `AttributeError: 'int' object has no attribute 'values'` in place of their own exception.
     Over the 469: `FAILED (errors=72)`, in ten modules.
   - **(g)** the cleanup in `finally:` in place of `except BaseException:` (it runs on success
     too): test 11 fails (0 open while the pool is open). The 469 pass, so test 11 alone catches
     it.

   For each, record the verdict line over the whole suite, and which of the 469 fail.
5. **The clients.** None is read; 08b changes no call a client makes. Record each client's `HEAD`
   and `git status --short`, at the start and the end, as unchanged.

---

## 5. Acceptance

1. §2.1's guard and `_open`, and §2.2's method: added lines only in `ShardedPool.py`, and nothing
   else in `datastorekit/` outside the new module.
2. The module, with every test of §2.3. Tests 1–10 fail on the unfixed layer on their counts, and
   test 11 pins the open that succeeds.
3. §2.4: 2 connections never closed over the suite at both ends, both the ported test's.
4. `docs/client-contract.md`'s header line and §9.2.
5. §4.1–§4.5 hold.
6. **The records**, in the same commit:
   - the log, `logs/08b-dispose-engines-on-a-refused-open.md`, per README §5.1;
   - the board: 08b's row and the header; the issue moved from §3 to §4, with a dated "Closed
     (…, prompt 08b)" line naming the fix, the test module and §2.4's count;
   - `docs/OPEN_ISSUES.md`: its row deleted, the count **6 → 5**, and the date;
   - `prompts/INDEX.md`: the campaign's line, and its open-issue count (**2 → 1**).

---

## 6. Stop conditions — stop and ask the user

- An existing test fails with the fix in place, or the suite's count falls.
- The fix cannot be made without changing a line of the open, a message, or a refusal.
- §2.4's measurement finds a connection never closed whose opener's constructor raised, or more
  than the two of `TestInsertBeforeSetVersion`.
- An existing test reads `cluster.calls` after a refused open and breaks on the `__exit__` calls
  (hazard 4).
- The high end does not resolve offline.
- Anything would write in a client repository, push, tag, download, or start Ray.

---

## 7. What this prompt changes, and what it does not

- **Files it creates or changes:**
  - `datastorekit/SQL/ShardedPool.py` (§2.1, §2.2);
  - `datastorekit/tests/test_refused_open_closes_engines.py` (new);
  - `docs/client-contract.md` (§2.5);
  - the log, the board, `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.
- **It changes nothing else.** In particular, it does not change:
  - `SQL/Datastore.py`, any other file under `datastorekit/`, `standin_pool.py`, the fixtures,
    the client or any existing test (`test_version_row_at_open`'s `bare_actor` among them, §2.4);
  - `compare_ported_tests.py`, `PROVENANCE.md`, `README.md`, `pyproject.toml`, `docs/adoption/`;
  - the campaign README, `CLAUDE.md` or the workflow.
- **It touches no client repository.**
- It makes no tag and pushes nothing. The version stays `0.2.0`; 10 releases.

---

## 8. The log and the board

`logs/08b-dispose-engines-on-a-refused-open.md`, using README §5.1. There is no
`compare_with_source.py` output (U27); in its place go the port check's output, the test-by-test
record of §2.3 and §4.4, and §2.4's measurement at both ends, with its method. The log also lists
the clients' commits and statuses, at the start and the end.

`IMPLEMENTATION_STATE.md`: §1's row for 08b (landed, commit, log), the header, and §3/§4 for the
issue.
