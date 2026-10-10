# Orchestrator — prompt 08b, dispose engines on a refused open

Read [`../README.md`](../README.md) first: §1, §2 (rows 08b–11), §4, §5 (rules 4, 6, 7, 9 and 10)
and §6.2 (U33–U37). Then read [`prompt-08a.md`](prompt-08a.md) §0's "Conventions", which this note
keeps unless it says otherwise, and the board's review of 08a.

**You do not write code.** You may:
- run the suite, the port check, `black --check` and the layer guard;
- make venvs in the session scratchpad with `uv pip install --offline`, from the cache 05's work
  filled, and nothing else: **no download** (the prompt's §4.2);
- export the tree with `git archive` into the scratchpad, and run probes, measurements and
  breakages there, never in this checkout and never committing one;
- read the three clients only through `git -C <client> rev-parse|status|log`; 08b reads nothing
  else of them (the prompt's §4.5);
- fix small residue in a follow-up commit of your own (§4).

You push nothing and make no tag: 08b makes no release (10 does, U36).

**The prompt:** [`08b-dispose-engines-on-a-refused-open.md`](../08b-dispose-engines-on-a-refused-open.md)
**Closes:** `[05-a-refused-open-leaves-its-engines-undisposed]` · **Narrows:** nothing ·
**Changes:** nothing · **Opens:** only what the work finds · **Model:** Opus, as the prompt
recommends.

**Gate:**
- 08a landed (`f938844`) and was reviewed (`2123445`). 08b is written (`9f9c970`).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- Nothing under `datastorekit/` or `docs/` has changed from `f938844` to `9f9c970` (only
  `prompts/` has), so the layer is 08a's, and the prompt's line numbers "at `2123445`" are
  `f938844`'s.
- `origin/main` is `102f225`, an ancestor of local `main`; `origin` holds `v0.1.0` and `v0.2.0`
  only.
- The clients' `HEAD`s: SGK `b510bc9` (branch `handover-remedial`), CPBH `52142d7` (`main`), SI
  `7bb3efd` (`main`).
- One prompt at a time in this checkout. 09 is not written.

## 0. What makes this prompt unusual

**The fix runs on every refused open in the suite.** 08a changed two paths; 08b wraps the whole
open. 107 of the suite's connections that are never closed come from raised constructors, in ten
modules, and every one of those opens now runs `_close_refused_open`. The review therefore reads
the fix against every place it reaches, and replays all seven breakages over the whole suite.

**The test counts, it does not wait.** A connection is closed when its `close()` has run, at the
moment the exception reaches the test. Nothing depends on the collector, so the counts are exact
and the same at both ends.

**`git diff` of `ShardedPool.py` shows added lines only.** The open moves into `_open` by gaining a
`def` line above it; none of its lines changes, in content or indentation.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-10 at `9f9c970`, in scratch
exports with §2.1 and §2.2 applied as the prompt gives them, in `venv/` and in an offline
high-end venv. Pass them on. Corrections 1–3 change what the agent writes, and are
STRUCTURALLY REQUIRED. The rest correct or complete what the prompt states; the log records each
as found.

1. **Test 7's `cluster.controller = 0` does nothing.** Inside a constructor `cluster.pool` is
   `None`, so `_StandinRandom.randrange` draws at random (`standin_pool.py:203-204`); and a
   replica's call in the version row's write is also an `object_get` of `version`
   (`ShardedPool.py:3214`, under `_get_impl_replicated_table`). So the fault on shard 0 fires
   whichever shard controls, and the open raises `StandinActorDied` ("shard0000-store.object_get(
   version) killed before it ran") on every run, with 4 of 7 left open unfixed: probed four times
   with the line, and twice with `cluster.pin_controller(0)` in its place, alike. The test pins the
   controller with `pin_controller(0)` (a context manager; exit it in cleanup), or leaves the line
   out and says why the fault fires anyway. It does not set `cluster.controller`.
2. **(g)'s diff also removes the bare `raise`.** With `finally:` in place of
   `except BaseException:` and the `raise` kept, every open that succeeds raises `RuntimeError: No
   active exception to reraise`, so the suite's first store fails to build and nothing is
   measured (probed). The (g) that pins test 11 is:

   ```diff
            try:
                self._open(version_label, drop_tables, read_table_config, read_only)
   -        except BaseException:
   +        finally:
                self._close_refused_open()
   -            raise
   ```

   Under it the probe's test 11 counts 0 open while the pool is open, and every refusal test
   passes, as the prompt says.
3. **A `KeyboardInterrupt` that escapes a test ends the whole run.** `unittest` re-raises it rather
   than recording a failure. So test 10 catches it inside the test (`assertRaises
   (KeyboardInterrupt)`), under every breakage too; and its hook fires once, on `"before"` of the
   first `read_largest_store_ids`, since the cleanup's own `__exit__` calls run the hooks as well
   (`standin_pool.py:126-127`, `:135-136`). A hook raised before the call is outside the stand-in's
   `try` (`:126-131`), so it reaches the constructor as it would a driver interrupted there. The
   hook is removed in cleanup.
4. **Line numbers at 08b's tree.** With §2.1's guard and a `def _open` line and a two-line
   docstring, the guard is inserted after the blank `:202`, so every line from `:203` moves down
   (hazard 8 says `:202`). The exact shift depends on the docstrings the agent writes; §9.2 and the
   log cite the committed tree.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **Write the module before the fix, and run it on the unfixed tree first, in a scratch export.**
  08a's agent wrote its tests in the checkout before the fix (board, review of 08a); 08b's runs the
  unfixed module in an export of `HEAD` with the new module copied in, so that the checkout never
  holds a half-state. Order:
  1. the baseline (469; the port check; `black --check datastorekit docs`, 68 files; the guard;
     the clients' `HEAD`s and statuses);
  2. §1.1's measurement on the unfixed tree, as the reference for §2.4;
  3. the module, run on the unfixed layer: tests 1–10 fail on their counts, test 11 passes;
  4. the fix. The suite: `469 + N` OK;
  5. §2.4's measurement at both ends; the high end's `ResourceWarning` lines;
  6. the contract's §9.2;
  7. (a)–(g), each in its own scratch export, each over the new module and over the whole suite;
  8. `venv/`'s suite again, the port check, `black`, the guard, the clients again, the records.
- **Name the probes' files outside `datastorekit/`**, and run them with the copy's root first on
  `sys.path`, printing `datastorekit.__file__` (hazard 1). The measurement script is the agent's own,
  in the scratchpad, never committed; the log gives its method and enough of it to re-run.
- **Record each breakage as a diff, exactly as applied**, so that the review can replay it with
  `git apply` against an export of the commit.
- **Each refusal test asserts its connections were counted and closed by identity**: the count
  over the list of connections the wrapper made, not a difference of two global counters, so that
  a connection another test leaves open cannot move it.

**The facts, checked by the orchestrator.** Pass them on.

- **The prompt's line references hold** at `9f9c970`: `__init__` `:95-360`, the read-only branch
  `:203-209`, `self._version = None` at `:201`, the actors' dicts `:304-320` and `:545-562`, the
  `read_table_config` refusals `:333-339` and `:578-584`, the version row `:348-360`;
  `_open_read_only` `:479-590`; `__exit__` `:762-774`; `_create_engine` `:776-849`;
  `_refuse_a_primary_that_differs` `:851-878`, the connection `:869`; `_write_shard_data` `:880`,
  the first use `:881`. `Datastore.py`: `__init__` from `:39`, its open `:131-146`; `__exit__`
  `:351-361`; `_create_engine` `:363-378`. `standin_pool.py`: `_Method.remote` `:102-145`,
  `_Options.remote` `:169-175`, `fault` `:277`. `bare_actor` at `test_version_row_at_open.py:474`.
- **The open's free names are its four arguments.** By the orchestrator's `ast` walk of `_open` in
  a fixed export: every name it loads that is not a module global, a builtin or its own local is
  `self`, `version_label`, `drop_tables`, `read_table_config` or `read_only`.
- **§1.1 reproduces.** The orchestrator's wrapper (a `factory=` subclass of `sqlite3.Connection`
  marking `close()` and counting on `__del__`, installed on `sqlite3.connect` and
  `sqlite3.dbapi2.connect`), over the 469 in `venv/`: **41,213** opened, **109** never closed,
  none alive after the run: `ShardedPool.py:869` 62 (55 read-write, 7 under `_open_read_only`, by
  a second run that marks the read-only stack), `Datastore.py:378` 41 (39 in raised
  constructors' pools, and `TestInsertBeforeSetVersion`'s 2), `ShardedPool.py:881` 6.
- **§2.2 reproduces.** With the fix, in `venv/`: `Ran 469 tests … OK`; 41,213 opened, **2** never
  closed, both `Datastore.py:378` in `TestInsertBeforeSetVersion`'s two tests. At the high end:
  `Ran 469 tests … OK`, with **4** `ResourceWarning` lines (two
  connections, two lines each), as the prompt says.
- **§2.3's table reproduces, row by row**, by the orchestrator's probe of the eleven opens through
  the stand-in pool, each on a store `build.open_pool` wrote and `cluster.close_pool` closed (test
  7 on a new store), counting only across the open. Unfixed: 1 of 1, 1 of 1, 1 of 10, 1 of 15, 4 of
  13, 4 of 16, 4 of 7, 4 of 13, 4 of 13, 4 of 13, and test 11 4 of 17 open, 0 after the close.
  Fixed: 0 everywhere but test 9 (1 of 13) and test 11 (4 open, 0 after). Each refusal is the
  prompt's type with the prompt's message, before and after: `StoreSchemaMismatch`,
  the mismatch `RuntimeError`, `ReplicatedDivergence`, `ReadOnlyMiss`, the read-table
  `RuntimeError` (tests 5, 6, 8, 9), `StandinActorDied`, `KeyboardInterrupt`. Test 1's extra table
  was `CREATE TABLE extra (x INTEGER)` on the primary; test 3 deleted every `version` row of shard
  1's file. Ray was never initialised.
- **The breakages, over the probe's eleven opens.** Exactly the prompt's §4.4:
  - (a): tests 1–10 leave their unfixed counts;
  - (b): tests 1–4 leave 0, tests 5–10 leave 3 (test 9 also 3);
  - (c): tests 1–10 leave 1 (test 9 2);
  - (d): tests 8 and 9 raise `StandinActorDied` ("shard0001-store.__exit__(None) killed after it
    ran" / "… before it ran") in place of the `RuntimeError`, leaving 1 and 2;
  - (e): test 10 leaves 4;
  - (f): tests 1–4 raise `AttributeError: 'int' object has no attribute 'values'`, each leaving 1;
  - (g), as correction 2: test 11 counts 0 open while the pool is open.
- **The breakages, over the 469.** In `venv/`, each in its own export of `9f9c970` with the fix and the
  breakage applied: (a), (b), (c), (d), (e) and (g) each give `Ran 469 tests … OK`; (f) gives
  `FAILED (errors=72)`, in ten modules (`test_reconcile_at_open` 23, `test_read_only_pool` 15,
  `test_store_schema` 9, `test_prune_at_open` 7, `test_layer_registry` 5,
  `test_one_timestamp_per_write` 4, `test_unsupplied_sharded_table` 4,
  `test_drop_refuses_dangling_references` 3, `test_declared_facts` 1, `test_version_row_at_open`
  1). So only the new module catches (a)–(e) and (g), as the prompt says.
- **The high end resolves offline.** `uv` 0.12.20, `uv venv --offline -p
  /opt/local/bin/python3.13`, then `uv pip install --offline "ray==2.55.1" "sqlalchemy==2.0.46"`
  and `uv pip install --offline --no-deps -e <export>`: Python 3.13.16, Ray 2.55.1, SQLAlchemy
  2.0.46, SQLite 3.53.4.
- **The toolchain.** `venv/`: Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39, `black` 25.1.0,
  `datastorekit 0.2.0` installed editable from this checkout.
- **No existing test reads `cluster.calls` after a refused open in a way the fix breaks** (hazard
  4): the 469 pass with the fix. Seven modules read `calls`.
- **Expected counts.**
  - The suite: **469** before; **469 + N** after, at both ends, N the loader's count for the new
    module (at least 11).
  - `compare_ported_tests.py`: exit 0, "20 module(s) … 1 test(s) declared not ported", unchanged.
  - `black --check datastorekit docs`: **68** files before, **69** after.
  - The guard: `KNOWN_HITS` at its one entry, before and after.
  - The index is **6**, and **5** after, unless the work opens an issue; `prompts/INDEX.md`'s
    count **2 → 1**.
- **The clients' trees.** SGK and SI clean; CPBH's 23 untracked entries. None is read.
- **Ray.** No Ray process was up at writing.

**What the review exists to establish.**
- **(E1) The layer.** `ShardedPool.py`'s diff is added lines only: §2.1's guard, the `def _open`
  line with its docstring, and §2.2's method; nothing else in `datastorekit/` outside the new
  module.
- **(E2) The test.** Each test of §2.3 is there; on the unfixed layer tests 1–10 fail on their
  counts and test 11 passes; each refusal test asserts its exception's type and message, and that
  it counted at least one connection; test 9 closes its leftover. No Ray, no client, `tempfile`
  only, and the wrapper restored.
- **(E3) Both ends.** `469 + N` in `venv/` and at the high end, in the review's own venv.
- **(E4) The measurement.** §2.4's 2, both `TestInsertBeforeSetVersion`'s, at both ends.
- **(E5) The contract.** The header line and §9.2; nothing else.
- **(E6) The breakages.** (a)–(g) each fail as recorded.
- **(E7) The records.**

**Conventions.** 08a's note's, unchanged, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff **as recorded in the log** with `git apply --check` and `-R --check`
  against a scratch export;
- read a client only through `git`, and never import or run its code;
- use a subdirectory of the session scratchpad, never `/tmp`, for venvs, exports and probes, and
  put **no scratch `.py` under `datastorekit/` or `docs/`**;
- start no Ray;
- a stop goes to the user;
- check `git log` before committing.

And for this prompt:
- **No download of any kind.** Every venv is made `--offline`. A pin that does not resolve offline
  is a stop.
- **No `git stash` in this checkout**, and no unfixed run in it: the unfixed layer is a scratch
  export.
- **No push, no tag.**

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. Record `git status --short
   --ignored` (at writing: `.idea/`, `venv/` and five `__pycache__/` directories).
2. **The baseline.** In `venv/`, the suite gives `Ran 469 tests … OK`; the port check exits 0;
   `black --check datastorekit docs` leaves 68 files unchanged.
3. **The clients.** Each `HEAD` is the gate's, and `git status --short` is as §0's facts say.
4. **The remote.** `git ls-remote origin` shows `main` at `102f225…`, `v0.1.0` peeling to
   `68db557…` and `v0.2.0` to `240028e…`, and no other tag.
5. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`.
6. **The index.** 6 now, and 5 after unless the work opens an issue. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `docs/client-contract.md`, and logs 05 and 08a;
- `HEAD`, the clients' `HEAD`s and statuses, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's four corrections and four additions. Correction 3 is
the one most likely to bite: a `KeyboardInterrupt` that escapes test 10 under a breakage ends the
run, and every later test goes unrun.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/08b-dispose-engines-on-a-refused-open.md`, in
  README §5.1's form, with the prompt's §8 additions.
- **The files it may add or change are the prompt's §7 list, and nothing else.** It must not touch
  `SQL/Datastore.py` or any other file under `datastorekit/` (`standin_pool.py`, the fixtures, the
  client, the guard and `test_version_row_at_open.py` among them), `compare_ported_tests.py`,
  `PROVENANCE.md`, `README.md`, `pyproject.toml`, `docs/adoption/`, `CLAUDE.md`, the campaign
  README, the workflow, or anything under `orchestrator/`.
- **It writes nothing in any client repository, and runs, imports or opens nothing of one.**
- **It downloads nothing.**
- **It pushes nothing and makes no tag.**
- **It starts no Ray.**
- **Stop and ask** on any of the prompt's §6 conditions.

## 3. The review — eleven checks

Make the review's venv fresh, offline, in a subdirectory of the scratchpad of its own, not the
agent's.

1. **Scope.** `git show --stat <commit>` touches exactly: `ShardedPool.py`, the new module,
   `docs/client-contract.md`, the log, the board, `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.
   `git status --short --ignored` lists the same entries as at dispatch. Each client's `HEAD` and
   `git status --short` are as at dispatch.
2. **E1, by reading.** `git diff 9f9c970 <commit> -- datastorekit/SQL/ShardedPool.py` has no `-`
   line. Its `+` lines are the guard, after `self._version = None`; the `def _open` line and its
   docstring, before the read-only comment; and `_close_refused_open`, after `_open`, as §2.2
   gives it (the `isinstance` guard, every `__exit__` submitted before any is waited for, each
   `ray.get` and the dispose in their own `try`). The docstrings name no client and no SGK path,
   and say that the caller's profile agent is not cleaned up. `git diff 9f9c970 <commit> --
   datastorekit/SQL/Datastore.py` is empty.
3. **E2, the test, by reading.** Each test of §2.3 is there, under a name that says what it pins.
   The wrapper is a context manager around the open only, restoring both attributes in `finally`.
   Each refusal test asserts the exception's type and message and at least one connection counted.
   Test 7 does not set `cluster.controller` (correction 1). Test 9 closes its leftover in cleanup
   and says why one is expected. Test 10 catches its `KeyboardInterrupt` inside the test, and its
   hook fires once (correction 3). Test 11 counts open while the pool is open and 0 after. Every
   store in a `tempfile` directory, stdout captured, Ray checked uninitialised; nothing names a
   client.
4. **E2, the test, by running against the unfixed layer.** In a `git archive <commit>` export,
   restore `ShardedPool.py` from `9f9c970` and run the new module: tests 1–10 fail on their counts,
   and test 11 passes. The run ends with a verdict line (no escaped `KeyboardInterrupt`).
5. **E3, both ends.** In `venv/`: `Ran 469 + N tests … OK`, the loader giving N for the module. In
   a fresh offline high-end venv with the export installed editable: the same, and the
   `ResourceWarning` count against the log's.
6. **E4, the measurement.** The review's own wrapper over the whole suite of the commit, at both
   ends: 2 never closed, both `TestInsertBeforeSetVersion`'s; none from the new module.
7. **The checks.** The port check exits 0 with 04b's counts; `black --check datastorekit docs`
   leaves 69 files unchanged; the layer guard passes with `KNOWN_HITS` at its one entry.
8. **E5, the contract.** `git diff 9f9c970 <commit> -- docs/client-contract.md` adds the header
   line after 08a's and §9.2 after §9.1, and nothing else; 08a's line and §9.1 are unchanged. §9.2
   supersedes no row, carries no marker, and its line references hold at the commit.
9. **E6, the breakages.** Replay (a)–(g) as the log records them, each in its own export. Over the
   module each fails as the prompt's §4.4 says; (g) as correction 2. Over the whole suite each
   verdict is the log's, and the 469 fail only under (f).
10. **E7, the records.**
    - The log has every section of README §5.1, the port check's output in place of
      `compare_with_source.py`'s, the test-by-test record of §2.3 and §4.4, §2.4's measurement at
      both ends with its method, the clients' commits and statuses at the start and the end, and
      under "Observations not acted on" `TestInsertBeforeSetVersion`'s two connections and hazard
      3's stand-in comprehension.
    - The board: 08b's row, the header, and the issue moved from §3 to §4 with its "Closed (…,
      prompt 08b)" line naming the fix, the module and §2.4's count.
    - `docs/OPEN_ISSUES.md`: 1 row on this repository, the header saying 5 open and the date.
    - `prompts/INDEX.md`: the campaign's line, and its open-issue count of 1.
11. **Nothing left behind.** No Ray process; `git tag -l` is `v0.1.0` and `v0.2.0`; `origin`
    unchanged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 08b* paragraph, in the form of
  08a's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log, in `prompts/INDEX.md`, and in
    `docs/client-contract.md`'s header line and §9.2 if it names 08b's tree that way;
  - README's header, and its §2 status for 08b ("landed, reviewed");
  - the notes line, with this note marked "used for 08b".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Report to the user:** the guard and the method; the test, its counts unfixed and fixed; the 469
  + N at both ends; §2.4's 2; (a)–(g); the contract's §9.2; the index at 5; and that 09 can be
  written.

**Hand on to 09's author:**
- `ShardedPool.py`'s lines move from 08b: every line from `:203` on, by the guard, the `def` and
  its docstring, and again after `_open` by `_close_refused_open`. The prose 09 rewrites inside
  the open (the read-only comment at `:203-205` among them) is now `_open`'s.
- 08b's docstrings are new prose and name no SGK path; 09 need not touch them.
- `KNOWN_HITS` is unchanged at its one entry.
