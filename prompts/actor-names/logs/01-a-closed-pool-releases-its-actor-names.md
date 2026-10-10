# Log 01 — a closed pool releases its actor names

**Subject:** Release a closed pool's actor names, and a refused open's · **Commit:** `ac50a8a` ·
**Date:** 2026-10-10 · **Model:** Claude Opus 5.5 · **Result:** landed; unpushed and untagged.

`[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]` is fixed and closed. A
`ShardedPool`'s `__exit__` now runs its body unchanged and then kills each shard actor and the
broker with `ray.kill(handle, no_restart=True)`, and marks the pool closed, so that a second
`__exit__` does nothing. A refused or abandoned open kills what it made, in the same way. Only the
handles the pool holds are killed, never an actor looked up by name. The names are unchanged, so
two open pools still collide (U1).

The stand-in pool now reserves each actor's name in its cluster until the handle is killed, stands
in `ray.kill`, and refuses a call to a killed handle, in every test (U2). No existing test met a
collision or a killed handle. A new module of **6** tests pins the fix: the suite goes from **486
to 492**, in `venv/` and at the high end. Breakage (a), the kill removed from `__exit__`, fails 4
of the new tests and **159** failure entries in 11 other modules. Every other breakage fails its
test.

Under real Ray, `docs/extraction/ray_smoke_run.py` has step N reversed and a new step C ("two open
pools collide"). It exits 0 at both ends, and leaves no Ray process. Under (e) it fails at step N,
naming the collision. `docs/client-contract.md` gains §9.3, and
`docs/extraction-verification.md` gains §4.6. The issue moves to the extraction board's §4, and
the index goes from **5 to 4 open** (0 on this repository's boards).

No client was written, run, imported or opened; nothing was pushed, tagged or downloaded. Ray was
started only by the smoke script, three times.

Prompt: [`../01-a-closed-pool-releases-its-actor-names.md`](../01-a-closed-pool-releases-its-actor-names.md),
with the orchestrator's dispatch note §0: eight corrections, its additions, its checked facts and
its conventions. §2 classifies each.

`<scratch01>` below is `<session scratchpad>/agent-01`, outside the repository.

---

## 1. What shipped

### 1.1 The layer (§2.1)

`datastorekit/SQL/ShardedPool.py`, 48 lines added and none removed (`git diff --stat`). Line
numbers are this commit's:

- **The closed flag**, `self._closed: bool = False`, with a two-line comment (`:203-205`), before
  the guard of `__init__` (`:207-211`), so that it exists whenever a pool object does.
- **`_kill_actors`** (`:419-441`), new. It kills each shard actor and then the broker with
  `ray.kill(handle, no_restart=True)`, each kill in its own `try`, and raises nothing. It reads
  `self._shards` only when it is a dict (until the actors exist it is the shard count), and
  `self._broker` with `getattr`, since a refused open may not have set it (correction 4). It never
  looks an actor up by name. Its docstring says so, and why.
- **`_close_refused_open`** (`:379-417`) calls `_kill_actors()` last (`:417`), after its present
  body, which is unchanged. Its docstring gains one paragraph, that it releases the names.
- **`__exit__`** (`:841-868`) gains a docstring: what it closes, that it releases the actors'
  names, that the handles are dead afterwards, and that a second call does nothing. It returns at
  once if the pool is closed (`:851-852`). Its present body follows unchanged (`:854-865`), then
  `self._kill_actors()` (`:867`) and `self._closed = True` (`:868`), with no `try`/`finally`
  (addition).
- **The profile agent is not killed**, and no name, message, refusal or exception changes.
  `_open`'s comprehensions are as they were (addition).

### 1.2 The stand-in pool (§2.2)

`datastorekit/tests/standin_pool.py`, 62 lines added and 2 changed: the docstring line ending the
list item before the new one (`.` → `;`), and `_Options.remote`'s `return`:

- **`standin_kill(actor, no_restart=True)`**, new, patched over `ray.kill` in
  `StandinCluster.active()` beside `ray.get`. Anything that is not a stand-in `Handle` raises
  `ValueError` with Ray's message ("ray.kill() only supported for actors. For tasks, try
  ray.cancel(). Got: …", `ray/_private/worker.py` at 2.43.0). A killed handle is left as it is.
  Otherwise it sets `handle.__dict__["killed"] = True`, and frees the handle's name in its cluster
  if that handle is the name's live holder.
- **`StandinCluster.names`**, new: the actor name → the live handle that holds it.
  `_Options.remote` refuses a name a live handle holds with `ValueError` and Ray 2.43.0's message,
  before the constructor runs (§2 item 10). It reserves the name once the constructor has returned,
  so a constructor that raises reserves nothing.
- **A killed handle is dead.** `_Method.remote` first reads `handle.__dict__.get("killed",
  False)` (never `getattr`, which `Handle.__getattr__` answers with a truthy `_Method`). For a
  killed handle it returns a `StandinRef` of `StandinActorDied("<name>.<method>(<class>) called on
  a killed actor")`, before the call log, the faults and the hooks.
- **The module docstring** lists the new stand-in, and says the one way it is stricter than Ray:
  Ray also frees a name when the last handle is collected, and the stand-in only when the handle
  is killed. It adds the two consequences: a pool dropped unclosed holds its names for the rest of
  its cluster, and a pool whose actor's constructor raised inside `_open`'s comprehension cannot
  kill the actors built before it.

Always on (U2): no test opts in or out.

### 1.3 The test (§2.3)

**`datastorekit/tests/test_closed_pool_releases_its_names.py`**, 6 tests in three classes, on
the neutral client and the stand-in pool. Not ported, and not added to `PORTED`. Each test makes a
temporary directory and one `StandinCluster`, enters `cluster.active()` (exited in cleanup), and
opens every pool through `build.open_pool`. `tearDown` and `tearDownModule` assert that Ray was
never initialised. The serial written is compared with one read from another call, never with a
literal. `assertFoundNotWritten` also requires the shards' `keypoint` rows unchanged by the get, so
a get that found nothing and inserted would fail.

| # | Test | What it does |
|---|---|---|
| 1 | `TestAClosedPoolReleasesItsNames.test_a_read_write_pool_releases_its_names_at_exit` | opens a new store, gets a keypoint (stored on the miss), closes the pool and keeps it; a read-write reopen works, and its get finds the same serial and writes no row |
| 2 | `….test_a_read_only_pool_releases_its_names_at_exit` | as 1, with a read-only pool between: it finds the serial (a miss would raise), is closed and kept; then a read-write reopen, the same get |
| 3 | `….test_a_refused_open_releases_its_names` | an open of a new store with `read_table_config={"Sample": {"tables_arg": False}}`, refused with the whole `RuntimeError` message once every actor exists; the exception is held, with its traceback (whose frames hold the half-built pool); then an open works, and serves a get |
| 4 | `TestTwoOpenPoolsStillCollide.test_a_second_open_while_a_pool_is_open_is_refused_by_name` | with a pool open, a second open raises `ValueError` with "is already taken" and `SerialPoolBroker`; the first pool still finds its serial; once it is closed (and kept), a third open works and finds it |
| 5 | `TestAfterExit.test_a_second_exit_does_nothing` | a second `__exit__` raises nothing, prints nothing and adds nothing to the cluster's call log |
| 6 | `….test_a_closed_pools_handles_are_dead` | after `__exit__`, `read_largest_store_ids` through each of `_shards`' handles (a sub-test each) raises `StandinActorDied` on `ray.get`, naming the actor and the method; the call log does not grow |

The module's docstring says what it pins, and cites this campaign and the issue.

### 1.4 The smoke script (§2.4)

`docs/extraction/ray_smoke_run.py` (SHA-256
`e9be6ffaf35ce05fabfd4788a90a9101c761b4b57bdd0baf58464d16d51cc331`, the file of this commit, run
at both ends and for (e)):

- **Step N, reversed** (`step_names`): with step 2's closed pool still referenced (in a local, and
  in `self.pool` until the second open succeeds), no name is held, and a second read-write open
  works at once. That pool is closed, and none of its names is held. If the second open is
  refused, the step fails naming the collision and the record. A `finally` drops both pools
  whatever happens (addition), and the check after a close is in the step, not in `close_pool`.
- **Step C, new** (`step_collide`, label `"C"`, title "two open pools collide", needs `["1",
  "N"]`): with a pool open, a second read-write open raises `ValueError`. The step requires "is
  already taken" and `SerialPoolBroker` in its message, and then that the first pool serves step
  2's get (`same_serials(the_alias())`). Its `finally` closes and drops the first pool. If the
  second open succeeds, that pool is closed at once and the step fails.
- **The record after each `__exit__`** expects no name held. A new `require_none_held` is called
  after the close in steps N, C, 3, 4 and 6 (the last three through `reopen_and_get`). Step N
  checks step 2's record.
- **Unchanged:** steps 1, 2 and 5, and the bodies of 3, 4 and 6 apart from that check;
  `"N"`'s label; the `needs` lists of steps 3–6; the drop of each pool before the next open; the
  refusals, the start and stop of Ray, and the process check.
- **The docstring** gives step N reversed and step C, says what step N measured at `v0.2.1` and
  what it asserts now, and keeps the issue's reference.

### 1.5 The documents (§2.5, §2.6)

- **`docs/client-contract.md`**, 19 lines added and none removed. After extraction prompt 11's head
  paragraph, unchanged, comes one italic line in §9.2's form: "§9.3 is measured from the package at
  `actor-names` prompt 01's tree…" (correction 2). At the end comes **§9.3 `actor-names` prompt
  01**: a paragraph and three rows. The rows are `ShardedPool.__exit__`, a refused open and two
  open pools, each with its "Supersedes" (none, with why §9.2's row still holds) and its
  `path:line`s at this commit, each read at this tree (§4.5).
- **`docs/extraction-verification.md`**, 202 lines added and none removed: **§4.6**, after §4.5,
  dated and attributed to this prompt under rule 6. It says §4.1–§4.5 are of `v0.2.1` and stay
  true of it. It gives the script's changes, both ends' runs (a table, what they show, and the
  full output, with scratch paths as `<scratch01>`), and (e).

### 1.6 The records (§2.7)

- **The extraction board**: the issue's entry moves whole from §3 to the head of §4, with a
  "**Closed** (2026-10-10, by `actor-names` prompt 01, this commit)" line. §3 says no issue of this
  repository is open on that board. Its header is unchanged.
- **This campaign's board**: its header (in progress, 01 landed), the "Owns" line, 01's row, §3
  (no issue held; the issue closed on the extraction board) and §4 (a pointer to the entry).
- **This campaign's README**: a sentence in its header, and §2's row for 01.
- **`docs/OPEN_ISSUES.md`**: the header (`:6`, **4 open**: 0 on this repository's boards, 4
  inherited); §1.1's line (`:12`, closed by this prompt); §1.3's table (`:30-32`) replaced by one
  dated "None open" line (correction 3).
- **`prompts/INDEX.md`**: the header (1 in progress, 1 closed), the status and "Open issues"
  column of `actor-names` (0), and the "Open issues" column of `extraction` (closed by this
  prompt).
- **This log.**

---

## 2. Deviations from the prompt

1. **Correction 1: breakage (d) keeps each shard's name starting `shard{key:04d}`**, with the
   pool's `id` appended (`-{id(self)}`), on the broker's `.options(name=…)` and the two shards'.
   `my_name=` is unchanged. Under it test 4 fails, and one existing test fails as the correction
   says,
   `test_refused_open_closes_engines.TestARefusalAfterTheActorsClosesThem.test_a_new_store_whose_version_write_fails_closes_the_actors`:
   `'shard0000-store-4513352176.object_get(version) killed before it ran' !=
   'shard0000-store.object_get(version) killed before it ran'`. That is (d) renaming the actor
   that test names, not a defect. **STRUCTURALLY REQUIRED.**
2. **Correction 2: the contract's head gains one italic line**, after extraction prompt 11's
   paragraph, which is not rewritten. §2.5's "changes no other line" is read as "removes or rewrites
   no line": the diff is 19 lines added and none removed. §9.3 supersedes nothing, and says so row
   by row. **STRUCTURALLY REQUIRED.**
3. **Correction 3: `docs/OPEN_ISSUES.md` changes three places**: the header, §1.1's line, and
   §1.3's table, replaced by a dated "None open" line. `prompts/INDEX.md`'s "Open issues" column
   changes for both campaigns. **STRUCTURALLY REQUIRED.**
4. **Correction 4: the helper kills only what the pool holds**: `self._shards` when it is a dict,
   and `self._broker` read with `getattr`. It looks nothing up by name. Test 4 asserts that the
   open pool serves its get after a refused second open, and so does step C under Ray at both ends.
   **STRUCTURALLY REQUIRED.**
5. **Correction 5: breakage (a) fails more than tests 1, 2 and 6.** It fails tests 1, 2, 4 and 6
   of the new module, and 159 failure entries in 11 other modules (91 distinct tests), exactly the
   note's counts, module by module (§5). Test 3 passes under (a), because it refuses an open of a
   new store, with no pool closed before it in its cluster (item 11). Recorded as found.
6. **Correction 6: breakage (b) fails ten existing entries**, five each in
   `test_one_timestamp_per_write` and `test_version_row_at_open` (four distinct tests in each), as
   the note says, and test 3. Recorded as found.
7. **Correction 7: line numbers.** At `33778b0`'s `datastorekit/`, the `read_table_config` check
   of `_open` is `:346-352`, and `_Options.remote` `:168-174`. This commit moves them to
   `:350-356` and `:193-211`. Everything this log and §9.3 cite is this commit's. Recorded as
   found.
8. **Correction 8: `ResourceWarning` lines at the high end.** 4 before, as stated; **0** after, in
   both of the 492's runs (stage 3, and the final). Under the breakages: (a) 0, (b) 4, (c) 0,
   (d) 4, (f) 6. Every line is the same kind as before ("unclosed database", with tracemalloc's
   hint). Under (f), the three extra warnings fit the three killed handles' calls, which ran and
   opened a connection on an actor whose engine `__exit__` had disposed. No new kind. Recorded as
   found.
9. **The orchestrator's additions**, each followed as given, and each an **IMPLEMENTATION
   CHOICE**, at the orchestrator's direction:
   - the order of work: the baseline; §2.1 and §2.2, then the existing 486 at the high end before
     the new module (`Ran 486 … OK`, 0 warnings); §2.3 and the suite at both ends; breakages
     (a)–(d) and (f); §2.4, the smoke run at both ends, then (e); the documents and records; the
     final checks;
   - every export installed editable into a fresh offline venv (`ray`, `sqlalchemy` and
     `setuptools` first, then `--no-deps --no-build-isolation -e`), and no `PYTHONPATH`;
   - `__exit__` follows the prompt literally, with no `try`/`finally` (§6 item 1);
   - `_open`'s comprehensions are not restructured (§6 item 2);
   - the killed flag, and anything else the stand-in adds to a handle, is read from
     `handle.__dict__`; a kill frees a name only if that handle is its live holder;
   - step N drops both pools in a `finally`, and checks its record in the step; `close_pool` raises
     nothing new; the new step's label is `"C"`, and `"N"` and the `needs` of steps 3–6 are kept;
   - breakage (a) is the suite's positive control (§5).
10. **The stand-in refuses a live name before the constructor runs**, and reserves it after. §2.2
    item 2 fixes when the name is reserved, but not when a collision is detected. Ray checks the
    name before it creates the actor (`ray/actor.py:1036-1051` at 2.43.0), so a colliding
    constructor never runs there. Checking after would run a `Datastore` constructor, opening its
    engine, for a name Ray would refuse. Hazard 4. **IMPLEMENTATION CHOICE.**
11. **Test 3 refuses an open of a new store**, so that no pool has been closed in its cluster
    before it. Under (a), then, only (b) can fail it, and it passes under (a). The note's prototype
    built the store with a closed pool first, which (a) also fails. The prompt's "an open with a
    `read_table_config` naming a sharded class (refused after every actor exists)" holds for a new
    store too: `_open` reaches the check after the broker and the shards (`:350-356`). **IMPLEMENTATION
    CHOICE.**
12. **Test 3 holds the exception with its traceback**, in a list, rather than as `assertRaises`'
    `exception`, whose traceback `unittest` clears. The traceback's frames hold the half-built
    pool, as a caller's held exception would under Ray. It makes no difference to the stand-in,
    which frees names only by a kill. **IMPLEMENTATION CHOICE.**
13. **Tests 1–4 check that the reopened pool finds the row and does not write it**: the same
    serial, and the shards' `keypoint` rows unchanged by the get. Test 2's read-only pool cannot
    insert, so its get finds or raises. **IMPLEMENTATION CHOICE.**
14. **Test 6 calls through every shard handle**, in sub-tests, and checks the call log. So under
    (a) and (f) it reports four failure entries (three sub-tests and the log). **IMPLEMENTATION
    CHOICE.**
15. **The extraction board's §3 gains a sentence** that no issue of this repository is open on it,
    as it said before extraction prompt 11 (log 11 §2 item 20). **This campaign's board's §3
    sentence** "The issue this campaign owns stays on the extraction board's §3 … 01 closes it
    there" is rewritten, and so is its "Owns" line, since this commit makes both false. Boards are
    not verification documents, and `CLAUDE.md` rule 3 has each prompt update §3/§4.
    **STRUCTURALLY REQUIRED.**
16. **`prompts/INDEX.md`'s header and `actor-names` status** change with 01's landing ("1 in
    progress, 1 closed"; "01 landed (this commit), not yet reviewed"), beside the "Open issues"
    columns of correction 3. **IMPLEMENTATION CHOICE.**
17. **The smoke script's step C reports what it saw on one line**: the collision's type, the first
    pool's get, and the record after its `__exit__`. Steps 3, 4 and 6 return what they returned
    before. **IMPLEMENTATION CHOICE.**
18. **The exports are of the working tree**, made by `git ls-files -z -co --exclude-standard | tar`
    as log 11 §2 item 17 does, because the work was uncommitted. The baseline high end ran on `git
    archive HEAD` (`7c97125`). **STRUCTURALLY REQUIRED.**

No UNINTENDED DRIFT was found.

---

## 3. The hazards (§3)

1. **Ray.** Ray was started only by the smoke script, from scratch venvs, three times: the low end,
   the high end and (e), one after another, with no suite running. By the script's own rule (a
   `pgrep -f` of `gcs_server|raylet|ray::|default_worker\.py`, each PID classed by `ps -o comm=`,
   shells dropped), and by my check of the same rule (`<scratch01>/probe/raycheck.py`), no Ray
   process was up before or left after any run (§4.3). `RAY_ADDRESS` was unset, and there was no
   `/tmp/ray/ray_current_cluster`, throughout. The same check found 0 Ray processes at 20:54:16
   (the start), 21:21:44 (before the final suites) and 21:25:00 (the end).
2. **No network.** Every venv and install was `uv … --offline`. No `git fetch`, `push` or
   `ls-remote` was run.
3. **The package changes in `SQL/ShardedPool.py` only**, and there only in the flag, `__exit__`,
   `_close_refused_open` and the new `_kill_actors`. `git diff --stat -- datastorekit` lists
   `SQL/ShardedPool.py`, `tests/standin_pool.py` and the new module, and nothing else.
4. **The stand-in stays faithful.** It refuses a live name before the constructor (as Ray does),
   with Ray 2.43.0's message, and `ray.kill` of a non-handle with Ray's. Its one strictness is in
   its docstring. No test passes under the stand-in that Ray would fail. Steps N and C exercise the
   same behaviour under Ray at both ends.
5. **Additive documents.** Under `docs/`, `git diff` removes no line of the contract or the
   verification document. `docs/OPEN_ISSUES.md` changes by its rule (correction 3).
   `docs/adoption/` and the other scripts of `docs/extraction/` are unchanged.
6. **No client is touched.** The clients were read only with `git -C <client> rev-parse` and
   `status`. Their `HEAD`s and statuses are unchanged (§4.6).
7. **The count.** 486 before, and 492 after, at both ends.

---

## 4. Verification performed

### 4.1 The suite

Each run in the foreground, from its tree's root, its output to a scratch file, and the verdict
taken with `grep -E '^Ran |^OK|^FAILED'`, the warnings with `grep -c ResourceWarning`.

| When | Where | Result | `ResourceWarning` lines |
|---|---|---|---|
| start (20:54) | `venv/` (3.12.15 / 2.43.0 / 2.0.39) | `Ran 486 tests in 81.521s` / `OK` | 0 |
| start (20:56) | `<scratch01>/base-hi`: `git archive HEAD` (`7c97125`), editable, 3.13.16 / 2.55.1 / 2.0.46 | `Ran 486 tests in 86.653s` / `OK` | 4 |
| after §2.1 and §2.2, before the new module (20:59) | `<scratch01>/stage2-hi`: an export of the working tree | `Ran 486 tests in 90.282s` / `OK` | 0 |
| after §2.3 (21:02) | `venv/` | `Ran 492 tests in 82.129s` / `OK` | 0 |
| after §2.3 (21:04) | `<scratch01>/stage3-hi`: an export of the working tree | `Ran 492 tests in 86.303s` / `OK` | 0 |
| end (21:21) | `venv/` | `Ran 492 tests in 90.791s` / `OK` | 0 |
| end (21:23) | `<scratch01>/final-hi`: an export of the final working tree, this log included | `Ran 492 tests in 86.647s` / `OK` | 0 |

SQLite is 3.53.4 everywhere. `venv/` holds `datastorekit 0.2.1`, editable from this checkout, and
was not reinstalled.

### 4.2 The checks

- **The port check**, `venv/bin/python docs/extraction/compare_ported_tests.py`, at the end: exit 0,
  "OK: 20 module(s) keep their source's tests, classes and assertion skeletons; 1 test(s) declared
  not ported" (and the same at the start). The new module is not a port, and the check does not
  count it.
- **`black --check datastorekit docs`**: 71 files unchanged at the start; **72** at the end, the
  new module the one more. Every changed `.py` file was formatted with `black` 25.1.0.
- **The two guards**, `test_layer_is_generic` and `test_prose_names_no_source`, run on their own
  at the end: `Ran 14 tests … OK`; and in every run of the suite.
- **Scope** (hazard 3): `git diff --stat -- datastorekit` lists `SQL/ShardedPool.py` (48 added, 0
  removed) and `tests/standin_pool.py` (62 added, 2 changed), and `git status` adds the new module
  alone. Every changed file is in §7's list.
- **The breakages as recorded** (§5): the five diff blocks of §5, extracted
  from this log, are byte-equal to the diffs applied, and each passed `git apply --check`, `git apply`
  and `git apply -R --check` on its own fresh export of the final working tree.

### 4.3 The smoke runs

Each from its own fresh export of the working tree and fresh offline venv, from the export's root,
as `env -u PYTHONPATH <venv>/bin/python docs/extraction/ray_smoke_run.py` under `/usr/bin/time -p`.
The script is this commit's (SHA-256 `e9be6ffa…c331`, equal in each export). The full output of
each is in `docs/extraction-verification.md` §4.6.

| Run | Started | Ray's session directory | `ray.init` | Steps (1, 2, N, C, 3, 4, 5, 6) | In all | Exit | Ray before; after (script; mine) |
|---|---|---|---|---|---|---|---|
| low (3.12.15 / 2.43.0 / 2.0.39) | 21:15:21 | `session_2026-10-10_21-15-23_174455_99956` | 4.0 s | every one PASS: 0.7, 0.0, 1.2, 1.3, 1.2, 1.2, 0.0, 1.2 s | 13.2 s (real 13.44) | **0** | 0; 0 and 0 |
| high (3.13.16 / 2.55.1 / 2.0.46) | 21:15:40 | `session_2026-10-10_21-15-41_686311_458` | 5.1 s | every one PASS: 1.0, 0.2, 1.5, 1.4, 1.3, 1.3, 0.0, 1.3 s | 15.6 s (real 15.79) | **0** | 0; 0 and 0 |
| (e), high | 21:16:05 | `session_2026-10-10_21-16-06_706126_720` | 4.8 s | 1 PASS, 2 PASS, **N FAIL**, C and 3–6 NOT RUN | 8.8 s (real 9.00) | **1** | 0; 0 and 0 |

The step lines, at each end:

```text
LOW:  PASS  step 1 (0.7 s): wrote store_tag 3, keypoint 3, dial_setting 2, knob_setting 1, gauge_setting 2, routing_rule 2, ephemeral_probe 1, keypoint_alias 3, Gadget 2, Tessera 6, Sample 4, Trace 2, Weave 1
LOW:  PASS  step 2 (0.0 s): serials [1, 2] (step 1's), the caller's dicts unchanged
LOW:  PASS  step N (1.2 s): after __exit__, the pool referenced, 0 of 4 held; a second read-write open worked at once (1.2 s); after its __exit__, 0 of 4 held
LOW:  PASS  step C (1.3 s): the second open raised builtins.ValueError naming SerialPoolBroker; the first pool then: serials [1, 2], the caller's dicts unchanged; after its __exit__, 0 of 4 held
LOW:  PASS  step 3 (1.2 s): serials [1, 2], the caller's dicts unchanged
LOW:  PASS  step 4 (1.2 s): read-only: serials [1, 2], the caller's dicts unchanged
LOW:  PASS  step 5 (0.0 s): builtins.RuntimeError: Mismatch between sharded tables supplied to the constructor and read from the existing ShardedPool; 0 of 4 held
LOW:  PASS  step 6 (1.2 s): read-write open after the refusal: serials [1, 2], the caller's dicts unchanged
HIGH: PASS  step N (1.5 s): after __exit__, the pool referenced, 0 of 4 held; a second read-write open worked at once (1.4 s); after its __exit__, 0 of 4 held
HIGH: PASS  step C (1.4 s): the second open raised ray.exceptions.ActorAlreadyExistsError naming SerialPoolBroker; the first pool then: serials [1, 2], the caller's dicts unchanged; after its __exit__, 0 of 4 held
(e):  FAIL  step N (0.1 s): __main__.StepFailed: after __exit__, the pool referenced, 4 of 4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store); the second open raised ray.exceptions.ActorAlreadyExistsError: The name SerialPoolBroker (namespace=None) is already taken. Please use a different name or get the existing actor using ray.get_actor('SerialPoolBroker', namespace='None')
```

The high end's other steps are the low end's, with their times. At both ends the read-only pool
held 0 of 3 names after `__exit__`. **`ray.kill` freed every name at once at both ends**: the
record after each `__exit__` is taken straight after it, with no wait, and was 0 held every time.
Under (e), step N's `finally` dropped the first pool, whose names were then free after 0.0 s. Ray's
other session directories under `/tmp/ray/` were not touched, and none of mine was deleted.

### 4.4 The breakages

§5.

### 4.5 The documents

- Every relative link added resolves from its file: `../prompts/actor-names/README.md` (the
  contract); `../prompts/actor-names/01-a-closed-pool-releases-its-actor-names.md` and
  `../prompts/actor-names/logs/01-a-closed-pool-releases-its-actor-names.md` (the verification
  document); `../actor-names/logs/01-a-closed-pool-releases-its-actor-names.md` (the extraction
  board); `logs/01-a-closed-pool-releases-its-actor-names.md` and
  `../extraction/IMPLEMENTATION_STATE.md` (this campaign's board and README). No anchor was added.
- Every `path:line` of §9.3 and of §1.1 above was read at this tree with `sed -n`: `:203-205`,
  `:207-211`, `:311`, `:322`, `:350-356`, `:379-417`, `:417`, `:419-441`, `:621`, `:625`,
  `:656-663`, `:841-868`, `:851-852`, `:854-859`, `:861-862`, `:864-865`, `:867`, `:868`.
- `git diff` of `docs/client-contract.md` and `docs/extraction-verification.md` has no removed
  line.

### 4.6 The clients

Read only with `git -C <client> rev-parse HEAD`, `rev-parse --abbrev-ref HEAD` and
`status --short`.

| Client | Start (20:54) | End |
|---|---|---|
| SecondaryGWKit | `b510bc9`, `handover-remedial`, clean | `b510bc9`, `handover-remedial`, clean (21:24) |
| ChamPBH | `52142d7`, `main`, 23 untracked entries | `52142d7`, `main`, the same 23 untracked entries (`diff` of the two listings empty) |
| StochasticInstantons | `7bb3efd`, `main`, clean | `7bb3efd`, `main`, clean |

---

## 5. The deliberate-breakage record (§4.4)

Each diff is relative to the repository root, exactly as applied, to its own fresh export of the
working tree (`<scratch01>/break-<x>/tree`) with its own fresh offline venv at the high end
(3.13.16 / 2.55.1 / 2.0.46), installed editable. Each passed `git apply --check`, was applied with
`git apply`, and then passed `git apply -R --check`. Each was checked again **as recorded here**,
extracted from this log, against a fresh export of the final tree (§4.2). None was committed. The
whole suite ran under each: 492 tests. "Entries" are `unittest`'s failures plus errors, a sub-test
or a cleanup counting on its own; "tests" are distinct test ids.

### (a) the kill removed from `__exit__` — the positive control

```diff
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -864,7 +864,6 @@
         if self._engine is not None:
             self._engine.dispose()
 
-        self._kill_actors()
         self._closed = True
 
     def _create_engine(self):
```

`FAILED (failures=4, errors=162)`: **166 entries**, 95 distinct tests. In the new module, **tests
1, 2, 4 and 6** fail (7 entries): 1, 2 and 4 on the stand-in's collision, `ValueError: The name
SerialPoolBroker (namespace=None) is already taken. …` (test 2's on `shard0002-store`, its
read-only pool having no broker); 6 on `StandinActorDied not raised`, in each of its three
sub-tests, and on its call log (`24 != 21`). Tests 3 and 5 pass (§2 item 11).

**In 11 other modules, 159 entries** (91 distinct tests), every one on the name collision (155 on
`SerialPoolBroker`, 4 on a shard's): `test_one_timestamp_per_write` 53, `test_reconcile_at_open`
45, `test_replicated_write` 14, `test_prune_at_open` 9, `test_version_row_at_open` 9,
`test_store_schema` 8, `test_refused_open_closes_engines` 7, `test_read_only_pool` 5,
`test_version_keyed_lookups` 5, `test_shard_key_assignment` 3, `test_declared_facts` 1. Each
reopens a store in the cluster that closed it. 0 `ResourceWarning` lines.

### (b) the kill removed from `_close_refused_open`

```diff
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -414,7 +414,6 @@
                 engine.dispose()
             except Exception:
                 pass
-        self._kill_actors()
 
     def _kill_actors(self) -> None:
         """
```

`FAILED (errors=11)`, 9 distinct tests. **Test 3** fails: the open after the refusal collides on
`SerialPoolBroker`. And 10 existing entries, 5 each (4 distinct tests each) in
`test_one_timestamp_per_write` (`TestVersionRowOfAnInterruptedNewStore`,
`TestVersionRowOfANewLabel`) and `test_version_row_at_open` (`TestNewStoreInterrupted`,
`TestNewLabelInterrupted`). Each injects a fault on the version write, so the open is refused once
every actor exists, and then opens again in the same cluster (correction 6). 4 `ResourceWarning`
lines.

### (c) the closed flag's early return removed from `__exit__`

```diff
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -848,9 +848,6 @@
         self._broker are kept, and are dead afterwards: a call through one fails. A second call
         does nothing.
         """
-        if self._closed:
-            return
-
         ray.get(
             [
                 shard.__exit__.remote(exc_type=None, exc_val=None, exc_tb=None)
```

`FAILED (errors=1)`: **test 5** only. The second `__exit__` calls `__exit__` through the killed
handles, and `ray.get` raises `StandinActorDied: shard0002-store.__exit__(None) called on a killed
actor`. 0 `ResourceWarning` lines.

### (d) the actors named per pool (correction 1)

```diff
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -308,7 +308,7 @@
 
         # the broker is created only now, so that nothing on the Ray side exists until the shard
         # files have been checked
-        self._broker = SerialPoolBroker.options(name="SerialPoolBroker").remote(
+        self._broker = SerialPoolBroker.options(name=f"SerialPoolBroker-{id(self)}").remote(
             name="SerialPoolBroker"
         )
 
@@ -319,7 +319,7 @@
         shard_ids = list(self._shard_db_files.keys())
         shard_ids = shard_ids[-1:] + shard_ids[:-1]
         self._shards = {
-            key: Datastore.options(name=f"shard{key:04d}-store").remote(
+            key: Datastore.options(name=f"shard{key:04d}-store-{id(self)}").remote(
                 version_label=version_label,
                 db_name=self._shard_db_files[key],
                 replicated_tables=list(self._replicated_tables),
@@ -622,7 +622,7 @@
         shard_ids = list(self._shard_db_files.keys())
         shard_ids = shard_ids[-1:] + shard_ids[:-1]
         self._shards = {
-            key: Datastore.options(name=f"shard{key:04d}-store").remote(
+            key: Datastore.options(name=f"shard{key:04d}-store-{id(self)}").remote(
                 version_label=version_label,
                 db_name=self._shard_db_files[key],
                 replicated_tables=list(self._replicated_tables),
```

`FAILED (failures=2)`: **test 4** (`AssertionError: ValueError not raised`), and
`test_refused_open_closes_engines.TestARefusalAfterTheActorsClosesThem.test_a_new_store_whose_version_write_fails_closes_the_actors`,
whose expected message names the actor (§2 item 1). 4 `ResourceWarning` lines.

### (e) (a) under real Ray, at the high end

(a)'s diff, applied to `<scratch01>/break-e/tree` as above, and the smoke script run from it
(§4.3). Step N fails naming the collision, `ray.exceptions.ActorAlreadyExistsError` on
`SerialPoolBroker`, and its record, 4 of 4 names held after `__exit__`. Its `finally` drops both
pools. Steps C and 3–6 are not run. Exit 1. No Ray process was left.

### (f) the stand-in's killed check removed

```diff
--- a/datastorekit/tests/standin_pool.py
+++ b/datastorekit/tests/standin_pool.py
@@ -120,15 +120,6 @@
         cls_name = _class_name(args)
         call = (handle.shard_id, self._name, cls_name)
 
-        # a killed actor runs nothing. The flag is read from the instance's __dict__: any
-        # attribute a handle lacks is a _Method (Handle.__getattr__), which is always truthy
-        if handle.__dict__.get("killed", False):
-            return StandinRef(
-                error=StandinActorDied(
-                    f"{handle.name}.{self._name}({cls_name}) called on a killed actor"
-                )
-            )
-
         cluster.calls.append(
             {
                 "shard": handle.shard_id,
```

`FAILED (failures=4)`: **test 6** only, in each of its three sub-tests (`StandinActorDied not
raised`) and on its call log (`24 != 21`). 6 `ResourceWarning` lines (§2 item 8).

---

## 6. Observations not acted on

1. **`__exit__` that raises releases nothing.** As the prompt and the note say, the kill and the
   flag follow the body with no `try`/`finally`. If a shard's `__exit__` (or the profile agent's
   `clean_up`) raises, `__exit__` raises as it did at `v0.2.1`, kills nothing, and leaves the pool
   not closed, so a retried `__exit__` runs the body again. The names are then held until the pool
   is collected, as before this prompt. That is the old behaviour on an error path, not one this
   prompt introduced, and the caller is told by the exception. Not opened as an issue; a later
   campaign may want `__exit__` to kill whatever it can on that path too.
2. **A constructor that raises inside `_open`'s comprehension** (`:321-337`, `:624-641`) leaves the
   actors built before it in no attribute, so neither `_close_refused_open` nor anything else can
   kill them. Under Ray `.remote()` does not raise for a failing constructor, so this does not
   arise there in that form, and the handles would be collected. Under the stand-in their names
   stay reserved in that cluster, which its docstring says. No test meets it.
3. **The high end's 4 `ResourceWarning` lines went to 0** in both runs of the 492. The note found
   the count is timing (correction 8). Nothing here measured whether killing the actors changes
   when the collector reaches the two actors `TestInsertBeforeSetVersion` builds directly.
4. **The scratch tools** are in `<scratch01>/probe/`, not in the repository: `raycheck.py`,
   `mkexport.sh` (an export of the working tree and its venv) and `breakrun.sh` (an export, a
   breakage and the suite). Each run's output is in `<scratch01>/logs/`, and each breakage's diff
   in `<scratch01>/diffs/`.

---

## 7. Issues

- **Closed**: `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]`, moved from the
  extraction board's §3 to the head of its §4, with its closing line; this board's §4 points to it.
- **Opened, narrowed**: none.
- **`docs/OPEN_ISSUES.md`**: 5 → **4** open, 0 on this repository's boards, 4 inherited.

---

## 8. State handed to the next prompt

- **`HEAD`** is this commit (`ac50a8a`), unpushed and untagged. `origin/main` is `d06b46a`, and the tags are
  `v0.1.0`, `v0.2.0` and `v0.2.1`, unchanged. `pyproject.toml` is at `0.2.1`.
- **The suite** is 492, in `venv/` and at the high end. The port check passes over 20 modules with
  1 test declared not ported. `black` leaves 72 files unchanged.
- **The interfaces** (README §4): `ShardedPool._closed` and `ShardedPool._kill_actors`; the
  stand-in's `standin_kill` and `StandinCluster.names`, always on; the new module; the smoke
  script's step N reversed and step C; contract §9.3; `docs/extraction-verification.md` §4.6.
- **For 02** (`v0.2.2`, U3): what changes for a client is that a closed pool's handles are dead,
  and that a store can be reopened in one Ray session while a closed pool is referenced. The
  contract's §9.3 says both.
- **Open**: none on this repository's boards; the four inherited issues of `docs/OPEN_ISSUES.md`
  §1.2.
