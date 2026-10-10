# Log 08b — dispose engines on a refused open

**Subject:** Close what a refused open made before it raises · **Commit:** `efedc8d` ·
**Date:** 2026-10-10 · **Model:** Claude Opus 5.5 · **Result:** landed; unpushed and untagged.

`[05-a-refused-open-leaves-its-engines-undisposed]`, held open since 05 and assigned here by U33
and U35, is fixed. When `ShardedPool`'s constructor raises, by a refusal or because the open was
abandoned (`KeyboardInterrupt` included), it now closes every actor built so far by its own
`__exit__` and disposes the pool's engine, and then re-raises the open's exception unchanged.
Before, each engine's pooled SQLite connection was closed only when the garbage collector reached
it.

`ShardedPool.py` gains added lines only: the guard, a `def _open` line with its docstring, and
`_close_refused_open`. No line of the open moves or changes. A new module of **11** tests counts
the connections a refused open makes and requires every one closed when the exception reaches the
test: the suite goes from **469 to 480**, in `venv/` and at the high end. On the unfixed layer
tests 1–10 fail on their counts and test 11 passes. Over the whole suite, the connections never
closed go from **109** to **2**, both `TestInsertBeforeSetVersion`'s, at both ends; the high end's
`ResourceWarning` lines go to **4**. Each of the seven breakages is caught, and only (f) is also
caught by an existing test. `docs/client-contract.md` gains a header line and §9.2. The issue
moves to the board's §4; the index goes from **6 to 5 open**.

No client was written, imported or run; nothing was pushed, tagged or downloaded; Ray was never
started.

Prompt: [`../08b-dispose-engines-on-a-refused-open.md`](../08b-dispose-engines-on-a-refused-open.md),
with the orchestrator's dispatch note §0: four corrections, four additions, its measured facts and
its conventions. Each is followed as given; §2 classifies them.

## 1. What shipped

### 1.1 The layer (§2.1, §2.2)

`datastorekit/SQL/ShardedPool.py`, two hunks of added lines (`git diff` of the file shows no `-`
line):

```diff
@@ -200,6 +200,18 @@ class ShardedPool:
         # the version row of version_label, found or written once every actor exists
         self._version = None
 
+        try:
+            self._open(version_label, drop_tables, read_table_config, read_only)
+        except BaseException:
+            self._close_refused_open()
+            raise
+
+    def _open(self, version_label: str, drop_tables, read_table_config, read_only):
+        """
+        Open the store, read-only or read-write, once __init__ has set the pool's attributes. If
+        it raises, __init__ closes what it made (_close_refused_open), and the exception
+        propagates.
+        """
         # A READ-ONLY POOL (prompts/a3-v2-readiness, prompt 03). It opens an existing store with
         # every file mode=ro and writes nothing to any of them; _open_read_only is the whole of its
         # construction, and nothing below this block runs for it
@@ -359,6 +371,41 @@ class ShardedPool:
             ]
         )
 
+    def _close_refused_open(self) -> None:
+        """
+        Close what a refused or abandoned open made, before its exception propagates. Each actor
+        built so far is closed by its own __exit__, as the pool's __exit__ closes them (its engine
+        disposed, its serial manager and profile batcher cleaned up), every call submitted before
+        any is waited for; then the pool's engine is disposed. Until the actors exist
+        self._shards is the shard count, and self._engine exists only once _create_engine has
+        run, so either may be absent.
+
+        Nothing this meets is raised, and it prints nothing, so that the exception the caller
+        sees is the open's own: an actor that is dead raises from its __exit__, and that is
+        ignored. The profile agent is the caller's and outlives a refused pool, so it is not
+        cleaned up here, although __exit__ cleans it up; the broker holds no engine.
+        """
+        shards = self._shards if isinstance(self._shards, dict) else {}
+        refs = []
+        for shard in shards.values():
+            try:
+                refs.append(
+                    shard.__exit__.remote(exc_type=None, exc_val=None, exc_tb=None)
+                )
+            except Exception:
+                pass
+        for ref in refs:
+            try:
+                ray.get(ref)
+            except Exception:
+                pass
+        engine = getattr(self, "_engine", None)
+        if engine is not None:
+            try:
+                engine.dispose()
+            except Exception:
+                pass
+
     def _find_version_row(self, version_label: str):
         """
         The version row of ``version_label``, read from every shard file with a plain ``mode=ro``
```

**At 08b's tree** (correction 4, by `grep -n` of the committed file): the guard is `:203-207`;
`_open` is `:209-372`, its docstring `:210-214`, and the open's own lines, unchanged, `:215-372`
(at `2123445` they were `:203-360`, so every one moves down by 12). Within it: the read-only
branch `:215-221`; the read-write actors' dict `:316-332`; the read-table refusal `:345-351`; the
version row `:360-372`. `_close_refused_open` is `:374-407`. Further down, every line moves by 47:
`_open_read_only` `:526-637` (its actors' dict `:592-609`, its read-table refusal `:625-631`),
`__exit__` `:809-821`, `_create_engine` `:823`, `_refuse_a_primary_that_differs` `:898` (the
connection `:916`), `_write_shard_data` `:927` (the first use `:928`). No message, refusal or
existing comment changed. `black` leaves the file unchanged.

**The open's free names** are its four arguments: `_open` reads `self`, `version_label`,
`drop_tables`, `read_table_config` and `read_only`, besides module globals and builtins (as the
note's `ast` walk found). The read-only branch's `return` now returns from `_open`, and `__init__`
returns after the guard, as before.

### 1.2 The test (§2.3)

**`datastorekit/tests/test_refused_open_closes_engines.py`**, 11 tests in three classes. Not
ported, and not added to `PORTED`.

**How it counts.** `counting()`, a context manager of the module's own, wraps the open alone. It
replaces `sqlite3.connect` and `sqlite3.dbapi2.connect` with a wrapper that passes `factory=_Counted`
(a `sqlite3.Connection` subclass whose `close()` sets `closed_by_close`, and which keeps the file
it was opened on), keeps every connection made in a list, and restores both attributes in
`finally`. A count is over that list (by identity), never a difference of global counters
(addition 4). Nothing waits for the collector.

**The setting.** `setUp` makes a temporary directory, enters `cluster.active()` (exited in
cleanup), and writes and closes a store there with `build.open_pool` and `cluster.close_pool`,
before any counting. Each test opens by calling `ShardedPool(...)` itself with the registry's
arguments (`build.open_pool`'s) and its overrides, inside `counting()` and with stdout captured.
The helper `refused(expected, **overrides)` catches only `expected`, so any other exception reaches
the runner as raised; if the open succeeds it closes the pool and fails the test; it requires at
least one connection counted; and it registers a cleanup that closes every counted connection still
open, after the test's assertions have read the counts. `tearDown` and `tearDownModule` assert that
Ray was never initialised.

| # | Test | The open | Asserts | Unfixed layer | Fixed |
|---|---|---|---|---|---|
| 1 | `TestARefusedOpenClosesItsConnections.test_a_primary_that_differs_is_refused_and_closed` | read-write; `CREATE TABLE extra (x INTEGER)` on the primary through `sqlite3` | `StoreSchemaMismatch`, its message beginning `Cannot open sharded datastore "<primary>": the primary "<primary>" differs from the tables this code declares`, `extra` among `differences.extra_tables`; every connection closed | **FAIL** `1 of 1` open | 0 of 1 |
| 2 | `….test_a_sharded_tables_mismatch_is_refused_and_closed` | read-write; `sharded_tables` lacks `Sample` | `RuntimeError`, the mismatch message whole (08a's) | **FAIL** `1 of 1` | 0 |
| 3 | `….test_a_divergence_at_open_is_refused_and_closed` | read-write; every `version` row of shard 1's file deleted through `sqlite3` | `ReplicatedDivergence`, "its replicated tables differ across shards", a difference of class `version` | **FAIL** `1 of 10` | 0 |
| 4 | `….test_a_read_only_open_of_an_absent_label_is_refused_and_closed` | read-only; `version_label="absent-label"` | `ReadOnlyMiss` of class `version`, payload `{"label": "absent-label"}`, "was opened read-only, and a lookup of "version" matched no row" | **FAIL** `1 of 15` | 0 |
| 5 | `TestARefusalAfterTheActorsClosesThem.test_a_read_table_config_refusal_closes_the_actors` | read-write; `read_table_config={"Sample": {"tables_arg": False}}` | `RuntimeError` `It is only possible to configure a read-table method for a replicated table (class name="Sample")`, whole | **FAIL** `4 of 13` | 0 |
| 6 | `….test_a_read_only_read_table_config_refusal_closes_the_actors` | read-only; the same `read_table_config` | the same | **FAIL** `4 of 16` | 0 |
| 7 | `….test_a_new_store_whose_version_write_fails_closes_the_actors` | a new store beside the first; `cluster.pin_controller(0)` (entered, exited in cleanup) and `cluster.fault(0, "object_get", "version", "before")` | `StandinActorDied` `shard0000-store.object_get(version) killed before it ran`, whole | **FAIL** `4 of 7` | 0 |
| 8 | `….test_an_actor_whose_exit_fails_after_it_ran_does_not_replace_the_refusal` | as 5, with `cluster.fault(1, "__exit__", None, "after")` | test 5's `RuntimeError`, not `StandinActorDied` | **FAIL** `4 of 13` | 0 |
| 9 | `….test_an_actor_whose_exit_never_ran_does_not_replace_the_refusal` | as 5, with `cluster.fault(1, "__exit__", None, "before")` | test 5's `RuntimeError`; the connections left open are exactly one, on shard 1's file; closed in cleanup | **FAIL** `4 of 13` (lists differ) | 1 of 13, shard 1's |
| 10 | `….test_an_open_abandoned_by_keyboard_interrupt_closes_the_actors` | the registry's open; a hook raising `KeyboardInterrupt("the open interrupted at read_largest_store_ids")` once, on `"before"` of the first `read_largest_store_ids` call; removed in cleanup | `KeyboardInterrupt`, caught inside the test (`assertRaises`), its message whole; the hook fired once | **FAIL** `4 of 13` | 0 |
| 11 | `TestAnOpenThatSucceeds.test_a_pool_that_opens_keeps_its_connections_until_it_is_closed` | the registry's open, succeeding; then `cluster.close_pool` | 4 open while the pool is open (`1 + len(shard_files)`: the pool's engine and three actors'), 0 after the close; the pool is closed before either is asserted | passes (pin) | passes |

Test 9's docstring comment says why one connection is expected: under Ray a dead actor's process
is gone, and its connection with it; under the stand-in the cleanup closes it. Under §4.4 (g) test
11 counts `0 of 17` open while the pool is open.

The module names no client; its words were also checked against
`tests/data/client_vocabulary.json`, and the only matches are generic words of that file (`b`,
`factories`, `label`, `name`, `type`).

### 1.3 The contract (§2.5)

`docs/client-contract.md`:
- below 08a's header line, unchanged, a line: "§9.2 is measured from the package at prompt 08b's
  tree, and its line numbers are that tree's";
- **§9.2 Prompt 08b**, in §9.1's form: one row, "An open that raises". It supersedes no row
  ("§1–§8 never said what a refused open leaves open"); it gives the guard `:203-207`, `_open`
  `:209-372`, `_close_refused_open` `:374-407`, the pool's `__exit__` it mirrors (`:809-815` for
  the actors, `:820-821` for the engine), and the actors' dicts `:316-332` and `:592-609`; it
  names `tests/test_refused_open_closes_engines.py`.

No other line of the contract changed, and there is no marker.

### 1.4 The records

This log; the board (header, 08b's row, the issue moved from §3 to §4 with its closing line);
`docs/OPEN_ISSUES.md` (the row deleted, 6 → 5, the date); `prompts/INDEX.md` (the campaign's line,
its open-issue count 2 → 1).

## 2. Deviations from the prompt

1. **Correction 1: test 7 pins the controller with `pin_controller(0)`**, entered in the test and
   exited in cleanup, and does not set `cluster.controller`. A comment says why. Found as the note
   says: the open raises `StandinActorDied` for shard 0's `object_get(version)` on every run (and
   4 of 7 are left open unfixed). **STRUCTURALLY REQUIRED.**
2. **Correction 2: breakage (g) removes the bare `raise` as well** (§5 (g)). Under it test 11 counts
   0 of 17 open while the pool is open, and every refusal test passes. **STRUCTURALLY REQUIRED.**
3. **Correction 3: test 10 catches the `KeyboardInterrupt` inside the test**, through `refused`'s
   `except expected` (an `assertRaises` in effect), under every breakage; its hook fires once, on
   `"before"` of the first `read_largest_store_ids`, and is removed in cleanup. Under (e), where the
   guard does not catch it, the test fails on its count (`4 of 13`) and the run goes on.
   **STRUCTURALLY REQUIRED.**
4. **Correction 4: line numbers at 08b's tree.** The guard and the `def _open` with its five-line
   docstring add 12 lines before the open, so the open's lines move from `:203-360` to `:215-372`;
   `_close_refused_open` adds 35 more, so lines after the open move by 47 (§1.1). §9.2 and this log
   cite the committed tree. Recorded as found.
5. **Addition 1: the module was run on the unfixed layer first, in a scratch export**, in the
   note's order (§4): baseline; §1.1's measurement on an export of `HEAD`; the module copied into
   that export and run there; then the fix in the checkout; then the rest. The unfixed layer was
   never in the checkout as a run, and no `git stash` was used. **IMPLEMENTATION CHOICE**, at the
   orchestrator's direction.
6. **Addition 2: the probes are outside `datastorekit/`**, under `<scratch>/probe/`, and each
   printed `datastorekit.__file__` (the export's, every time). **IMPLEMENTATION CHOICE**, at the
   orchestrator's direction.
7. **Addition 3: each breakage is recorded as a diff, exactly as applied** (§5), and replays with
   `git apply --check` and `-R --check`. **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
8. **Addition 4: each refusal test counts by identity**, over the list of connections its own open
   made. **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
9. **The module was first written into `datastorekit/tests/` in the checkout, and moved to the
   scratchpad before anything ran.** Addition 1 asks that the checkout never hold a half-state; for
   a few minutes it held the new module beside the unfixed layer, unrun. It was moved out, run on
   the unfixed export, and copied back only with the fix. Nothing was committed or run in between.
   **UNINTENDED DRIFT** (corrected at once; no effect on any result).
10. **Every test's cleanup closes every counted connection still open**, not only test 9's. On the
    fixed layer only test 9 has one; under a breakage, or on the unfixed layer, the others' leftovers
    are closed too, so a failing run leaves nothing for the collector. The counts are read before
    the cleanup runs. **IMPLEMENTATION CHOICE.**
11. **Test 9 identifies its leftover by file**: exactly one connection open, on shard 1's file (the
    file `_Counted` records), rather than a count of 1. **IMPLEMENTATION CHOICE.**
12. **Test 11 closes the pool before asserting**, so that a failing count (as under (g)) still
    closes it. **IMPLEMENTATION CHOICE.**
13. **The measurement probe tracks a caller's own `factory=`** through a subclass of it, so that the
    new module's counted connections (which pass `factory=_Counted`) are measured too (§4.4). Log 05
    found no caller passing one; the new module is the first. **IMPLEMENTATION CHOICE.**
14. **§1.1's list of exceptions omits `ReadOnlyMiss`.** The unfixed measurement finds one of the 107
    under a raised `ReadOnlyMiss` (`test_read_only_pool.TestAtOpen.test_an_absent_version_label_is_refused_naming_the_labels_present`,
    `:869` read-only), beside the six the prompt names. The totals are the prompt's. An expectation
    corrected; recorded, no change. **STRUCTURALLY REQUIRED** (an expectation corrected).
15. **The note says seven modules read `cluster.calls`; `grep` finds six** naming `.calls`
    (`test_drop_refuses_dangling_references`, `test_layer_registry`, `test_neutral_client`,
    `test_read_only_pool`, `test_replicated_write`, `test_version_row_at_open`). Either way the 469
    pass with the fix (hazard 4). Recorded as found.
16. **The breakage suites ran four, then three, at a time**, which is why they took 164–238 s
    against about 110 s alone. **IMPLEMENTATION CHOICE.**
17. **`uv`'s cache.** `venv-high` was resolved `--offline` from `uv`'s default cache; nothing was
    downloaded. **IMPLEMENTATION CHOICE.**

No other UNINTENDED DRIFT was found.

## 3. The hazards (§3)

1. **The editable install.** `venv/`'s `datastorekit` is the checkout's. Every probe and every
   export run printed `datastorekit.__file__`: the export's for the unfixed module, the
   measurements, the high end and each breakage; the checkout's only for runs in the checkout.
2. **The unfixed layer is the reference.** §4.2: tests 1–10 fail on their counts, test 11 passes,
   in an export of `HEAD` with the module copied in. Only then was the fix applied.
3. **The stand-in builds an actor at once.** Read so: under the stand-in an actor constructor that
   raised would raise inside the comprehension at `:316-332`, while `self._shards` is still the
   count, and the actors built before it would not be closed. No test of the suite reaches this
   (§4.4: no actor's constructor raised, before or after). Not changed (it would move the open's
   lines); §6 item 2.
4. **The cleanup is visible in `cluster.calls`.** A refused open after the actors now records one
   `__exit__` per actor. The 469 pass with the fix, so no existing test breaks on it; six modules
   name `.calls` (§2 item 15). No stop.
5. **The counting wrapper is restored** in `counting()`'s `finally`, both attributes. Every test,
   including test 10 under `KeyboardInterrupt`, leaves `sqlite3` as it found it; the 469 pass after
   the module in every run.
6. **No other line of `ShardedPool.py` changes, and none of `Datastore.py`.** `git diff` shows only
   added lines in `ShardedPool.py`, and nothing else under `datastorekit/` but the new module.
7. **Prose.** No comment or docstring outside the added lines changed. The two new docstrings name
   no client and no SGK path; the guard passes with `KNOWN_HITS` at its one entry.
8. **Line numbers move.** §1.1 and correction 4; earlier citations are of their own trees, and are
   not rewritten.

## 4. Verification performed

### 4.1 The suite

Each run is `<python> -m unittest discover -s datastorekit/tests -t .` from the tree's root, in the
foreground, output written to `<scratch>/out/` and the verdict grepped.

| # | When | Venv | Tree | Verdict | `ResourceWarning` lines |
|---|---|---|---|---|---|
| 1 | at dispatch | `venv/` | the checkout at `f24ded1` | `Ran 469 tests in 107.759s` / `OK` | 0 |
| 2 | the new module alone, unfixed | `venv/` | export of `HEAD` + the module | `Ran 11 tests` / `FAILED (failures=10)` (§4.2) | — |
| 3 | the new module alone, fixed | `venv/` | the checkout | `Ran 11 tests` / `OK` | — |
| 4 | after the fix | `venv/` | the checkout | `Ran 480 tests in 110.640s` / `OK` | 0 |
| 5 | the high end | `venv-high` | the fixed export | `Ran 480 tests in 112.181s` / `OK` | **4** |
| 6 | the final tree, with the records | `venv/` | the checkout | `Ran 480 tests in 90.638s` / `OK` | 0 |

**469 before, 480 after, at both ends; N = 11** (`loadTestsFromName` of the module,
`countTestCases()` → `11`). The 469 pass unchanged in every run with the fix.

The high end's 4 lines are two warnings, two lines each (`ResourceWarning: unclosed database in
<sqlite3.Connection …>` and `ResourceWarning: Enable tracemalloc …`), in the stretch of
`test_version_row_at_open`: the two connections of §4.4 that 08b does not close. 08a's log had
188 over the 469, the board's review 214.

### 4.2 The module on the unfixed layer (hazard 2)

`<scratch>/exports/unfixed` = `git archive HEAD` (`f24ded1`), with the module copied in;
`datastorekit.__file__` = the export's. `Ran 11 tests` / `FAILED (failures=10)`:

- tests 1–8 and 10 **FAIL** on their counts: `1 of 1` (tests 1, 2), `1 of 10` (3), `1 of 15` (4),
  `4 of 13` (5, 8, 10), `4 of 16` (6), `4 of 7` (7), each message listing the files still open
  (the primary, and the three shards for 5–8 and 10);
- test 9 **FAILS** with four connections open (`4 of 13`) where it requires shard 1's alone;
- test 11 passes.

Each refusal arrived as its expected type with its expected message (every assertion before the
count passed). With the fix, all 11 pass. A first run of the unfixed module, before the one
recorded here, errored ten times with `UnboundLocalError` in the module's own `refused` helper
(`pool` unset on the refusal path); the helper was corrected before any recorded run.

### 4.3 The venvs

| Venv | Python | Ray | SQLAlchemy | SQLite | `datastorekit` |
|---|---|---|---|---|---|
| `venv/` | 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.43.0 | 2.0.39 | 3.53.4 | 0.2.0, editable, the checkout; `black` 25.1.0 |
| `<scratch>/venv-high` | 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.55.1 | 2.0.46 | 3.53.4 | 0.2.0, editable, `<scratch>/exports/fixed` |

`venv-high`: `uv` 0.12.20; `uv venv --offline -p /opt/local/bin/python3.13 <scratch>/venv-high`;
`uv pip install --offline --python <scratch>/venv-high/bin/python "ray==2.55.1" "sqlalchemy==2.0.46"`;
`uv pip install --offline --no-deps --python … -e <scratch>/exports/fixed`. Every pin resolved
offline. `uv pip freeze`: attrs 26.1.0, certifi 2026.7.22, charset-normalizer 3.5.2, click 8.5.0,
datastorekit (editable, the export), filelock 4.0.12, idna 3.20, jsonschema 4.26.0,
jsonschema-specifications 2025.9.1, msgpack 1.2.3, packaging 26.3, protobuf 7.36.2, pyyaml 6.0.3,
ray 2.55.1, referencing 0.37.0, requests 2.34.2, rpds-py 2026.9.1, sqlalchemy 2.0.46,
typing-extensions 4.16.0, urllib3 2.8.0.

`<scratch>/exports/fixed` = `git archive HEAD` with the fixed `ShardedPool.py` and the new module
copied in; `cmp` of every tracked file and the module against the checkout found no difference.

### 4.4 The measurement (§1.1, §2.4)

**Method.** `<scratch>/probe/measure_unclosed.py <tree> <report>`, run with each venv's
interpreter under `-I`, puts `<tree>` first on `sys.path`, `chdir`s there and prints
`datastorekit.__file__`. Then:
- `sqlite3.connect` and `sqlite3.dbapi2.connect` are replaced by a wrapper that passes
  `factory=Tracked`, a `sqlite3.Connection` subclass; a caller's own `factory=` (the new module's
  `_Counted`) is replaced by a subclass of it with the same tracking (§2 item 13);
- at creation `Tracked` records: the innermost frame under `datastorekit/` but not
  `datastorekit/tests/` (the layer's site); the innermost `ShardedPool` and `Datastore` (actor)
  objects whose methods are on the stack, through a record per object that `__init__` wrappers
  (`functools.wraps`) on both classes create and mark, when the constructor ends, with whether it
  raised and what; whether `_open_read_only` is on the stack; the running test (from the result's
  `startTest`) and the outermost `test_*.py` frame;
- `close()` marks it closed; `__del__` counts it if it never was;
- the suite runs through discovery and `TextTestRunner`; then `gc.collect()` twice, and any tracked
  connection still alive and unclosed is reported (none ever was).

Its core:

```python
class TrackedMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mark_closed = False
        self._mark_info = info()          # site, pool/actor records, read-only, test
        state["opened"] += 1
        live.add(self)
    def close(self):
        self._mark_closed = True
        super().close()
    def __del__(self):
        if not getattr(self, "_mark_closed", True):
            unclosed.append(self._mark_info)

Tracked = type("Tracked", (TrackedMixin, sqlite3.Connection), {})

def connect(*args, **kwargs):
    if "factory" in kwargs:
        kwargs["factory"] = tracked_factory(kwargs["factory"])   # (TrackedMixin, factory)
    else:
        kwargs["factory"] = Tracked
    return _real(*args, **kwargs)

sqlite3.connect = connect
sqlite3.dbapi2.connect = connect
```

**The reference: the unfixed tree** (`exports/unfixed` before the module was copied in; `venv/`):
`Ran 469 tests` / `OK`; **41,213** connections opened, none with a caller's own factory,
**109** never closed, 0 alive at the end:

| Opened at (`2123445`'s lines) | Never closed | Whose |
|---|---|---|
| `SQL/ShardedPool.py:869` | 62 | a raised pool constructor's engine: read-write 55 (`ReplicatedDivergence` 24, `SimulatedDeath` 9, `StoreSchemaMismatch` 8, `RuntimeError` 7, `StandinActorDied` 7), read-only 7 (`StoreSchemaMismatch` 3, `ReadOnlyWrite` 2, `ReadOnlyMiss` 1, `ReplicatedDivergence` 1) |
| `SQL/Datastore.py:378` | 39 | an actor whose constructor returned, in a pool whose constructor raised `StandinActorDied` |
| `SQL/Datastore.py:378` | 2 | an actor built directly, never exited: `TestInsertBeforeSetVersion`'s two tests |
| `SQL/ShardedPool.py:881` | 6 | a raised pool constructor's engine (`StandinActorDied`) |

So 107 are a raised constructor's and 2 a test's, as §1.1 says; no actor's own constructor raised.
By defining module: `test_version_row_at_open` 55, `test_reconcile_at_open` 23,
`test_prune_at_open` 13, `test_store_schema` 9, `test_read_only_pool` 4,
`test_unsupplied_sharded_table` 4, `test_declared_facts` 1.

**After the fix** (`exports/fixed`), identical at both ends:

| End | Tests | Opened | With a caller's own factory | Opened during the new module | Never closed | Alive at the end |
|---|---|---|---|---|---|---|
| low (3.12.15 / 2.43.0 / 2.0.39) | 480 OK | 41,411 | 119 | 198 | **2** | 0 |
| high (3.13.16 / 2.55.1 / 2.0.46) | 480 OK | 41,411 | 119 | 198 | **2** | 0 |

- **The 2** are `SQL/Datastore.py:378`, an actor built directly whose constructor returned, one in
  each of `test_version_row_at_open.TestInsertBeforeSetVersion.test_a_versioned_insert_raises_names_the_class_and_writes_nothing`
  and `…test_an_unversioned_insert_is_not_refused_and_set_version_admits_the_rest` (`bare_actor`,
  `:474`).
- **None from a constructor that raised.**
- **None from the new module**: 198 connections were opened while it ran (its `setUp`s' stores, its
  `sqlite3` edits, and the 119 its opens made, counted through `_Counted`), and every one was
  closed (test 9's by its cleanup).
- The 469's own connections are the reference's 41,213 (41,411 − 198).

### 4.5 The checks

- **The port check** (in place of `compare_with_source.py`, retired by U27): `./venv/bin/python
  docs/extraction/compare_ported_tests.py` exits 0 before and after, its 106 lines byte-identical;
  its last line: `OK: 20 module(s) keep their source's tests, classes and assertion skeletons; 1
  test(s) declared not ported`. The new module is not in `PORTED`.
- **`black`**: `black --check datastorekit docs` leaves **68** files unchanged before and **69**
  after; `black` reformatted the new module once while it was written, and leaves
  `ShardedPool.py` unchanged.
- **The layer guard**: `test_layer_is_generic` passes (`Ran 8 tests` / `OK`) before and after, its
  file unchanged, `KNOWN_HITS` at its one entry (`datastorekit/tools/shard_key_audit.py:188`).

### 4.6 The clients (§4.5)

Read only through `git -C <client> rev-parse|branch|status`; nothing else of them was read,
imported, run or written. The same at the start and at the end:

| Client | Commit | Branch | `git status --short` |
|---|---|---|---|
| SGK | `b510bc9` | `handover-remedial` | empty |
| CPBH | `52142d7` | `main` | 23 untracked entries (none read) |
| SI | `7bb3efd` | `main` | empty |

08b changes no call a client makes.

## 5. The deliberate-breakage record (§4.4)

**The method.** `<scratch>/probe/make_breaks.py` wrote each breakage into a scratch `git`
repository made from the fixed export (`<scratch>/breaks/repo`), took `git diff`, and restored the
file; the repository was clean after. The diffs' `index` lines name `b63c1a3`, the fixed
`ShardedPool.py` (`git hash-object` of the checkout's file). `<scratch>/probe/run_break.sh <name>`
then made a fresh copy of that tree (`<scratch>/exports/break-<name>`), ran `git apply --check`,
`git apply` and `git apply -R --check` (all passed for all seven), printed `datastorekit.__file__`
(the copy's, every time), and ran the new module and then the whole suite with `venv/`'s
interpreter and `PYTHONPATH` set to the copy. The checkout was never broken. The diffs below are
the files applied, byte for byte.

**(a) The guard removed.**

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index b63c1a3..226ff6e 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -200,11 +200,7 @@ class ShardedPool:
         # the version row of version_label, found or written once every actor exists
         self._version = None
 
-        try:
-            self._open(version_label, drop_tables, read_table_config, read_only)
-        except BaseException:
-            self._close_refused_open()
-            raise
+        self._open(version_label, drop_tables, read_table_config, read_only)
 
     def _open(self, version_label: str, drop_tables, read_table_config, read_only):
         """
```

Module: `FAILED (failures=10)`, tests 1–10 with their unfixed counts (§4.2). Suite: `Ran 480
tests` / `FAILED (failures=10)`, those ten; the 469 pass.

**(b) No actor closed.**

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index b63c1a3..a6ab70c 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -385,7 +385,7 @@ class ShardedPool:
         ignored. The profile agent is the caller's and outlives a refused pool, so it is not
         cleaned up here, although __exit__ cleans it up; the broker holds no engine.
         """
-        shards = self._shards if isinstance(self._shards, dict) else {}
+        shards = {}
         refs = []
         for shard in shards.values():
             try:
```

Module: `FAILED (failures=6)`: tests 5–10, each `3 of N` open (`3 of 7`, `3 of 16`, `3 of 13`; test
9 `3 of 13`, the three shards' where it requires shard 1's alone); tests 1–4 pass. Suite: `Ran 480
tests` / `FAILED (failures=6)`, those six; the 469 pass.

**(c) The engine not disposed.**

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index b63c1a3..2fef853 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -399,12 +399,6 @@ class ShardedPool:
                 ray.get(ref)
             except Exception:
                 pass
-        engine = getattr(self, "_engine", None)
-        if engine is not None:
-            try:
-                engine.dispose()
-            except Exception:
-                pass
 
     def _find_version_row(self, version_label: str):
         """
```

Module: `FAILED (failures=10)`: tests 1–8 and 10 each `1 of N` open (the primary's), test 9 `2 of
13` (the primary's and shard 1's). Suite: `Ran 480 tests` / `FAILED (failures=10)`, those ten; the
469 pass.

**(d) An actor's `__exit__` failure raised.**

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index b63c1a3..f61199a 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -395,10 +395,7 @@ class ShardedPool:
             except Exception:
                 pass
         for ref in refs:
-            try:
-                ray.get(ref)
-            except Exception:
-                pass
+            ray.get(ref)
         engine = getattr(self, "_engine", None)
         if engine is not None:
             try:
```

Module: `FAILED (errors=2)`: tests 8 and 9 **ERROR** with `StandinActorDied:
shard0001-store.__exit__(None) killed after it ran` and `… killed before it ran`, raised during
the handling of the open's `RuntimeError`, in place of it; they error before counting. Suite: `Ran
480 tests` / `FAILED (errors=2)`, those two; the 469 pass.

**(e) `except Exception` in place of `BaseException`.**

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index b63c1a3..095d240 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -202,7 +202,7 @@ class ShardedPool:
 
         try:
             self._open(version_label, drop_tables, read_table_config, read_only)
-        except BaseException:
+        except Exception:
             self._close_refused_open()
             raise
 
```

Module: `FAILED (failures=1)`: test 10, `4 of 13` open; the `KeyboardInterrupt` was caught inside
the test and the run went on. Suite: `Ran 480 tests` / `FAILED (failures=1)`, test 10; the 469
pass.

**(f) The `isinstance` guard removed.**

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index b63c1a3..a33d34b 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -385,7 +385,7 @@ class ShardedPool:
         ignored. The profile agent is the caller's and outlives a refused pool, so it is not
         cleaned up here, although __exit__ cleans it up; the broker holds no engine.
         """
-        shards = self._shards if isinstance(self._shards, dict) else {}
+        shards = self._shards
         refs = []
         for shard in shards.values():
             try:
```

Module: `FAILED (errors=4)`: tests 1–4 **ERROR** with `AttributeError: 'int' object has no
attribute 'values'` in place of their own exception. Suite: `Ran 480 tests` / `FAILED
(errors=76)`: the module's 4 and **72 of the 469**, in ten modules: `test_reconcile_at_open` 23,
`test_read_only_pool` 15, `test_store_schema` 9, `test_prune_at_open` 7, `test_layer_registry` 5,
`test_one_timestamp_per_write` 4, `test_unsupplied_sharded_table` 4,
`test_drop_refuses_dangling_references` 3, `test_declared_facts` 1, `test_version_row_at_open` 1.
75 of the 76 end in that `AttributeError`; one
(`test_layer_registry.TestAnUndeclaredDropTable.test_read_write_the_pool_refuses_it_before_anything_is_opened`)
ends in an `UnboundLocalError` of the test's own code, after the `AttributeError` replaced the
refusal it catches.

**(g) The cleanup in `finally:`, the `raise` removed** (correction 2).

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index b63c1a3..002463b 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -202,9 +202,8 @@ class ShardedPool:
 
         try:
             self._open(version_label, drop_tables, read_table_config, read_only)
-        except BaseException:
+        finally:
             self._close_refused_open()
-            raise
 
     def _open(self, version_label: str, drop_tables, read_table_config, read_only):
         """
```

Module: `FAILED (failures=1)`: test 11, `0 != 4 : 0 of 17 connections open while the pool is
open`; every refusal test passes. Suite: `Ran 480 tests` / `FAILED (failures=1)`, test 11; the
469 pass.

**Only the new module catches (a)–(e) and (g)**: the 469 pass under each. (f) is also caught by 72
of the 469. Every breakage fails exactly the tests §4.4 expects.

**Replayed from this log.** The seven diffs above, extracted from this file, are byte-identical to
the files applied, and each passes `git apply --check`, `git apply`, `git apply -R --check` and
`git apply -R` against a fresh export of the final tree (`git archive HEAD` with the fixed
`ShardedPool.py`), which is then identical to the checkout's file.

## 6. Observations not acted on

1. **`TestInsertBeforeSetVersion`'s two connections** (§4.4). Its `bare_actor`
   (`test_version_row_at_open.py:474`) builds an actor directly and never exits it, so its engine's
   connection is left for the collector: the 2 never closed at both ends, and the high end's 4
   `ResourceWarning` lines. Not 08b's: the test is ported (03b), changing `bare_actor` changes a
   ported test's fixture, and no change to the layer can close an actor its caller keeps. No issue
   is opened (§2.4).
2. **An actor constructor that raises under the stand-in** (hazard 3). The stand-in builds each
   actor when `.remote()` is called, so an actor constructor's exception would leave the
   comprehension at `:316-332` (or `:592-609`) before `self._shards` is the dict, and the actors
   built before it would not be closed. Under Ray the exception surfaces at the first `ray.get`,
   once the dict exists, and the cleanup closes them. No test reaches this (no actor's constructor
   raises in the suite); building the dict incrementally would move the open's lines. Not changed;
   no issue.
3. **`ReadOnlyMiss`** is among the raised constructors of §1.1's 107, which the prompt's list of
   exceptions omits (§2 item 14).
4. **Under Ray, a dead actor's `__exit__` raises `RayActorError`** at `ray.get`, which
   `_close_refused_open` ignores; the connection goes with the process. Pinned under the stand-in
   by tests 8 and 9; not run under Ray (no test may start it).

## 7. Issues

- **Closed:** `[05-a-refused-open-leaves-its-engines-undisposed]`, moved to the board's §4 with a
  "Closed (2026-10-10, prompt 08b)" line naming the fix, the test module and §4.4's count.
- **Opened, narrowed, changed:** none.

The index goes from **6 to 5 open**: 1 on this board (`[01-package-prose-names-sgks-layout]`,
09's), 4 inherited. `prompts/INDEX.md`'s count goes from 2 to 1.

## 8. State handed to the next prompt

- `HEAD` is `efedc8d`. The tree is clean but for the ignored entries of dispatch (`.idea/`, the
  `__pycache__/` directories, `venv/`). `venv/` is unchanged.
- **Not pushed, not tagged.** `origin/main` is `102f225`; the tags are `v0.1.0` and `v0.2.0`. The
  version stays `0.2.0`; 10 releases `v0.2.1`.
- **The suite is 480** in `venv/` and at the high end. `compare_ported_tests.py`: 20 modules, one
  test declared not ported, exit 0. `black --check datastorekit docs`: 69 files.
- **The high end** now prints 4 `ResourceWarning` lines over the suite, both of `bare_actor`'s
  actors.
- **For 09:** `ShardedPool.py`'s lines from `:203` move by 12 to `:372`, then by 47 (§1.1). The two
  new docstrings and the new module name no SGK path or campaign; `KNOWN_HITS` is unchanged. The
  open's comment `# A READ-ONLY POOL (prompts/a3-v2-readiness, prompt 03)` is now at `:215`, inside
  `_open`, unchanged.
- **For 10:** `docs/client-contract.md` §9 has §9.1 and §9.2; 10 adds its own subsection if it
  changes the layer, and the addenda (U37) can say that a refused open now closes its engines.
- **Scratch** (not in the repository): `<scratch>` =
  `/private/tmp/claude-35086/-Users-ds283-Documents-Code-DatastoreKit/7e3a7e99-93dc-48bd-ac70-ccc037cd8c42/scratchpad/agent-08b`,
  holding `venv-high`, `exports/` (`unfixed`, `fixed`, `break-a` … `break-g`), `module/` (the
  module as run on the unfixed export), `breaks/` (the seven diffs and the scratch repository),
  `out/` (every run's output) and `probe/` (`measure_unclosed.py`, `make_breaks.py`,
  `run_break.sh`).
