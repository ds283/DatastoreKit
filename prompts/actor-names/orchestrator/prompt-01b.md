# Orchestrator — prompt 01b, closing a pool starts no Ray

Read [`../README.md`](../README.md) first: §0, §1, §4, §5 (every rule) and §6.2 (U1, U2 and U4).
Then read [`prompt-01.md`](prompt-01.md), whose "Conventions", additions on installing and on
breakages, and §3–§5 this note keeps unless it says otherwise. Then read this board's §3 entry
for `[02-closing-a-pool-can-start-ray]`, including how the issue was found.

**You do not write code.** You may:
- run the suite, the port check, `black --check` and the guards;
- make venvs in the session scratchpad with `uv … --offline`, from the cache the extraction
  campaign filled;
- export the tree with `git archive` into the scratchpad, and run prototypes, the smoke script and
  breakages there, never in this checkout and never committing one;
- start Ray **only** through the smoke script, under README §5 rule 7, with no Ray process up
  before or left after, and never while a suite runs. **Never probe `ray.kill`, or any other of
  Ray's auto-init calls, outside a test that stands in `ray.init`**: that is how the issue was
  found, and it broke rule 7 (the board's §3);
- reach the network only for one `git ls-remote origin` at dispatch and one at the review;
- read the three clients only through `git -C <client> rev-parse|status|show|grep`;
- fix small residue in a follow-up commit of your own (§4);
- after the review, and only with the user's approval, push `main` (§5).

**The prompt:** [`01b-closing-a-pool-starts-no-ray.md`](../01b-closing-a-pool-starts-no-ray.md)
**Closes:** `[02-closing-a-pool-can-start-ray]` · **Narrows:** nothing · **Opens:** only what the
work finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- 01 landed (`ac50a8a`) and was reviewed (`049fa1a`); CI passed on `049fa1a` at both ends
  (`168ecd0`). U4 is taken (`2c3d298`), and 01b is written (`2c3d298`). The user has not changed
  the form at dispatch: it is the prompt's.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- `git diff --stat ac50a8a HEAD -- datastorekit` is empty: the package is 01's.
- `origin/main` is `1925898` (`git ls-remote origin`, 2026-10-11), an ancestor of `main`, which is
  ahead of it by `2c3d298` and this note. The tags are `v0.1.0` (`0ece4aa` → `68db557`), `v0.2.0`
  (`9eaf542` → `240028e`) and `v0.2.1` (`0ba2e4d` → `33778b0`), here and on `origin`, and no other.
- The clients' `HEAD`s: SGK `b510bc9` (branch `handover-remedial`, clean), CPBH `52142d7` (`main`,
  23 untracked entries), SI `7bb3efd` (`main`, clean).
- The index is **5** (1 on this repository's boards, 4 inherited), and will be **4** after.
- One prompt at a time in this checkout. 02 stays held until 01b is reviewed.

## 0. What makes this prompt unusual

**The defect is invisible to the suite, by construction.** Every test runs inside the stand-in's
`active()`, which stands in `ray.kill`, so no test can reach Ray's `ray.kill` and its auto-init.
The fix's witness (test 7) must step outside the stand-in's `ray.kill` *on purpose*, and its
breakage (a) would then start a real Ray unless `ray.init` is stood in first. **The `ray.init`
stand-in is what keeps this prompt within rule 7**, and the review reads it before (a) is run.

**The fix's stand-in patch carries every kill the suite makes.** Without it, `_ray_is_running()`
is false in every test and nothing is killed: breakage (b) fails 169 entries. With it, the suite
sees exactly what it saw at 01.

**What only Ray sees.** Breakage (c) (`_ray_is_running` always false) fails test 8 and nothing
else in the suite, since the stand-in replaces the helper. Under real Ray it skips every kill, and
the smoke script's step N fails. So the smoke run, unchanged, is the second witness.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-11 at `2c3d298` (whose
`datastorekit/` is `ac50a8a`'s), in `venv/`, in offline scratch venvs at both ends, in scratch
exports with a prototype of §2.1–§2.3 (tests 7 and 8 both), and under a local Ray started and
stopped by the smoke script. Pass them on. Correction 1 changes what the agent writes, and is
STRUCTURALLY REQUIRED. Corrections 2–4 correct what the prompt states; the log records each as
found.

1. **Test 8 runs inside `active()`, so it must call the module's own helper.** §2.3 puts both
   tests in a class built on `_OneSessionCase`, whose `setUp` enters `active()`; so inside test 8
   `sp_mod._ray_is_running` *is the stand-in*, which returns `True` whatever `ray.is_initialized`
   says. "Outside `active()`" cannot hold in that class. Test 8 calls the helper as captured when
   the test module is imported (the same capture test 7 needs, §2.3), not `sp_mod._ray_is_running`
   looked up at call time. Under (c) the captured function is the broken one, and test 8 fails, as
   measured. (A separate `unittest.TestCase` for test 8 alone would also do; the prototype used
   the capture, and either is the agent's choice, recorded.) `ray.is_initialized` is replaced by
   `mock.patch.object` in a `with` inside the test body, so it is restored before `tearDown`'s
   `assertFalse(ray.is_initialized())`.
2. **Breakage (b)'s count.** At the high end, `FAILED (failures=4, errors=165)`, 169 entries:
   - **8 in 01's module**: tests 1, 2, 3 and 4 (one error each), and test 6 (its three subtests
     and the test, four failures). Tests 5, 7 and 8 pass;
   - **161 in 11 other modules**: `test_one_timestamp_per_write` 54, `test_reconcile_at_open` 45,
     `test_replicated_write` 14, `test_version_row_at_open` 10, `test_prune_at_open` 9,
     `test_store_schema` 8, `test_refused_open_closes_engines` 7, `test_read_only_pool` 5,
     `test_version_keyed_lookups` 5, `test_shard_key_assignment` 3, `test_declared_facts` 1.

   That is 01's breakage (a) (159, log 01 §5) and two more, one each in
   `test_one_timestamp_per_write` and `test_version_row_at_open`: (b) stops a refused open's kills
   too, as 01's (b) did. The prompt's "as 01's breakage (a) did" is near, not exact.
3. **The smoke script under (c) runs no step after N.** At the high end: step N `FAIL` with "4 of
   4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store)" after
   `__exit__`, the second open refused with `ray.exceptions.ActorAlreadyExistsError`; steps C, 3,
   4, 5 and 6 `NOT RUN` ("needs step N"); 0 Ray processes left; exit 1. The prompt names only step
   N. This is as 01's review found for its (e).
4. **Where the verification subsection goes.** `:375` (§2.5) is §4.6's heading. §4 ends at
   `:578`, and `## 5. The pin (U42)` is `:579`: the new subsection is inserted between them.
   Every other line number the prompt cites holds at `2c3d298`, in the package, in Ray's source at
   both ends, and in SGK at `b510bc9`.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **Work in this order:**
  1. the baseline: 492 in `venv/`, and at the high end from a fresh venv with an export of `HEAD`
     installed editable; the port check; `black --check datastorekit docs`, 72 files; the
     clients' `HEAD`s and statuses; Ray's processes, by the script's rule; `RAY_ADDRESS` and
     `RAY_ENABLE_AUTO_CONNECT` (both unset at writing);
  2. §2.1 and §2.2; then the existing 492 at the high end, **before** writing the tests, so that
     an existing test that fails once the stand-in stands in `_ray_is_running` is seen on its own
     (a stop, §6);
  3. §2.3; the suite at both ends;
  4. read test 7 against hazard 2; then the breakages (a)–(c), each in its own export at the
     high end;
  5. the smoke run at both ends; then (c) at the high end;
  6. the documents (§2.4, §2.5), the issue and the index (§2.6), the records;
  7. `venv/`'s suite again, the port check, `black`, the guards, the clients again, Ray's
     processes again.
- **Install, do not set `PYTHONPATH`**, as 01's note says: 19 subprocess tests fail in an export
  that is not installed. Into each scratch venv: `ray`, `sqlalchemy` and `setuptools` offline,
  then `uv pip install --offline --no-deps --no-build-isolation -e <export>`. High end
  `/opt/local/bin/python3.13`, `ray==2.55.1`, `sqlalchemy==2.0.46`; low end
  `/opt/local/bin/python3.12`, `ray==2.43.0`, `sqlalchemy==2.0.39`. `venv/` is not reinstalled.
- **Test 7's form.** Inside the test, nest three `mock.patch.object`s over the close: `ray.kill`
  to Ray's own (captured at import), `sp_mod._ray_is_running` to the module's own (captured at
  import), and `ray.init` to a function that records its call and raises. Close through
  `self.cluster.close_pool`, as the module's other tests do. Assert the record is empty and
  `ray.is_initialized()` is false. The test may also assert that the pool is marked closed
  (§2.1 item 3); the agent chooses and records it. Ray's auto-init calls `ray.init()` through the
  `ray` module's attribute (`ray/_private/auto_init_hook.py:14` at 2.43.0, `:15` at 2.55.1), so
  the patch intercepts it.
- **`RAY_ENABLE_AUTO_CONNECT`.** Ray reads it once, at import (`auto_init_hook.py:7` at 2.43.0,
  `:8` at 2.55.1). If it were `"0"` in the agent's environment, Ray's `ray.kill` would skip
  `ray.init()` and raise from `check_connected()`, and test 7 would pass under (a) for the wrong
  reason. The log records it unset for every run of (a). Do not set it anywhere.
- **Under (a), record the record.** Test 7's assertion message shows the calls: measured,
  `[1, 1, 1, 1] != []`, one for each of the three shards and one for the broker. The log quotes
  it, and says that `ray.is_initialized()` stayed false (the module's `tearDownModule` checks).
- **Prose.** Under `datastorekit/`, comments and docstrings name no client and no path that does
  not exist (the two guards). Cite the prompt as the module does now, "``actor-names`` prompt
  01b", and the issue by its tag.
- **Contract §9.4's "Pinned by"** names tests 7 and 8 for the guard and the helper, and the smoke
  script's step N for "while connected, every kill of 01 is made" (it alone sees (c)).

**The facts, checked by the orchestrator.** Pass them on.

- **The prototype.** In an export of `2c3d298`: `_ray_is_running()` after
  `_INCOMPLETE_COPY_SUFFIX` (`:44`), returning `ray.is_initialized()`; `_kill_actors` returning
  at once when it is false, before reading any handle; in `active()`,
  `mock.patch.object(sp_mod, "_ray_is_running", lambda: True)` after the `ray.kill` patch
  (`:292`); tests 7 and 8 in a class `TestNoRay(_OneSessionCase)` after `TestAfterExit`, with
  `RAY_KILL = ray.kill` and `RAY_IS_RUNNING = sp_mod._ray_is_running` at module level.
- **The suite.**
  - At `2c3d298`, high end: `Ran 492 tests … OK`, 0 `ResourceWarning` lines. This replaces the
    high-end run of `1925898` the board does not rely on.
  - At `2c3d298`, `venv/`: `Ran 492 tests … OK`, 0 `ResourceWarning` lines.
  - With the prototype: `Ran 494 tests … OK` at both ends (3.12.15 / 2.43.0 / 2.0.39 and
    3.13.16 / 2.55.1 / 2.0.46, SQLite 3.53.4), installed editable, 0 `ResourceWarning` lines at
    each. So no existing test is moved by the stand-in's patch.
- **The breakages**, in exports at the high end, each against the prototype, installed editable:

  | | Change | 01's module | Other modules |
  |---|---|---|---|
  | (a) | the two guard lines removed from `_kill_actors` | test 7 fails, `[1, 1, 1, 1] != []`; no Ray | none |
  | (b) | the stand-in's `_ray_is_running` patch removed | tests 1–4 and 6 (8 entries) | 161 (correction 2) |
  | (c) | `_ray_is_running` returns `False` | test 8 fails | none |

- **The smoke run, the script unchanged** (SHA-256 `e9be6ffa…c331`), each from an offline scratch
  venv with the export installed editable:
  - low end, prototype: Ray started in 3.9 s; every step `PASS`; 0 of 4 names held after each
    read-write `__exit__`, 0 of 3 after the read-only one; the second open in step N worked at once
    (1.5 s); step C raised `builtins.ValueError`, and the first pool then served `[1, 2]`; 15.5 s;
    exit 0;
  - high end, prototype: the same, Ray in 4.9 s, step C `ray.exceptions.ActorAlreadyExistsError`;
    23.8 s; exit 0;
  - high end, (c): correction 3; 9.7 s; exit 1.
  - "Ray processes before: 0" and "after: 0" in each. `RAY_ADDRESS` and `RAY_ENABLE_AUTO_CONNECT`
    unset; no `/tmp/ray/ray_current_cluster`; `pgrep -f` for the script's pattern empty after.
- **Ray's source.** `kill` is in `AUTO_INIT_APIS` and `is_initialized` in `NON_AUTO_INIT_APIS`
  at both ends (`ray/__init__.py:211-220` and `:237` at 2.43.0; `:208-217` and `:233` at 2.55.1),
  so §6's fifth condition does not fire. `auto_init_ray` is as the prompt says at both ends.
- **The clients**, read through `git`: SGK's `Datastore/tests/standin_pool.py` `active()` is
  `:231-247` at `b510bc9` and patches `ray.get` (`:233`), not `ray.kill`, as the prompt says.
  SGK's `ComputeTargets/tests/test_quadsource_policy_main.py` also has a `tearDownModule` that
  asserts `not ray.is_initialized()` (`:430-431`). So under 01's tree that module would not only
  start a Ray but fail. The log may record this (it is a client's file, so not in the contract or
  the package).
- **The toolchain.** `venv/`: Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39, SQLite 3.53.4,
  `black` 25.1.0, `datastorekit 0.2.1` editable from this checkout. `uv` 0.12.20.
- **Expected counts.**
  - The suite: **492** before, **494** after, at both ends.
  - `compare_ported_tests.py`: exit 0, "OK: 20 module(s) … 1 test(s) declared not ported".
  - `black --check datastorekit docs`: **72** files before and after (no `.py` is added).
  - The index: **5** now; **4** after.

**What the review exists to establish.**
- **(E1) Scope.** Only §7's files change; under `datastorekit/`, three files, and in
  `SQL/ShardedPool.py` only the helper and the guard.
- **(E2) The fix.** A close while not connected to Ray kills nothing and never reaches Ray's
  `ray.kill`; while connected, 01's kills are unchanged.
- **(E3) The stand-in.** `_ray_is_running` stood in on `sp_mod` inside `active()`, always on;
  `ray.is_initialized` left alone.
- **(E4) The tests.** Tests 7 and 8, each failing under its breakage, test 7 unable to start Ray
  under (a), and (b) failing widely.
- **(E5) Ray.** The smoke script, unchanged, exits 0 at both ends, fails under (c), and leaves no
  Ray process.
- **(E6) The documents and the close.** Contract §9.4 and its head line, and the verification
  subsection, additive and true at their tree; the issue closed on this board and gone from the
  index.
- **(E7) Both ends.** 494 in `venv/` and at the high end.

**Conventions.** Prompt 01's note's, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- record each breakage as a diff relative to the repository root, and check it **as recorded in
  the log** with `git apply --check` and `-R --check` against a scratch export;
- read a client only through `git`, and never import or run its code;
- use a subdirectory of the session scratchpad, never `/tmp`, for venvs and exports; put no
  scratch `.py` under `datastorekit/` or `docs/`;
- a stop goes to the user;
- check `git log` before committing.

And for this prompt:
- **Ray is started only by the smoke script**, from a scratch venv, never while a suite runs.
  Nothing else calls `ray.kill`, `ray.get`, `ray.put`, `ray.wait`, `ray.cancel`, `ray.get_actor`
  or `ray.get_runtime_context` outside the stand-in or a test that stands in `ray.init`.
- **No network.** Every venv and install is `--offline`.
- **No push, no tag, and no change to the GitHub repository's settings.** `pyproject.toml` stays
  at `0.2.1`. Prompt 02 is not touched.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. Record `git status --short
   --ignored` (at writing: `.idea/`, `venv/` and five `__pycache__/` directories).
2. **The baseline.** In `venv/`, `Ran 492 tests … OK` with no `ResourceWarning`; the port check
   exits 0; `black --check datastorekit docs` leaves 72 files unchanged; `pip show datastorekit`
   says `0.2.1`.
3. **The clients.** Each `HEAD` and `git status --short` as the gate says.
4. **The remote.** `git ls-remote origin`: `main` at `1925898…` and the three tags as the gate
   says.
5. **Ray.** No Ray process by the script's rule; `RAY_ADDRESS` and `RAY_ENABLE_AUTO_CONNECT`
   unset.
6. **The index.** 5 now, and 4 after. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, this board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `docs/client-contract.md`, `docs/extraction-verification.md`, log 01 and prompt 01;
- `HEAD`, the clients' `HEAD`s and statuses, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's four corrections and its additions. Correction 1 is the
one that would make test 8 pass under (c); the `ray.init` stand-in in test 7 is the one thing
that keeps (a) from starting Ray.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/01b-closing-a-pool-starts-no-ray.md`, in README
  §5.1's form.
- **The files it may change are the prompt's §7 list, and nothing else.** It must not touch
  `pyproject.toml`, `README.md`, `PROVENANCE.md`, `docs/adoption/`, `docs/extraction/`, prompt 02,
  the extraction board, the workflow, `CLAUDE.md`, `LICENSE`, `.gitignore`, or anything under
  `orchestrator/`.
- **Under `docs/`, no line is removed** except the index's (§2.6).
- **It writes nothing in any client repository, and runs, imports or opens nothing of one.**
- **It reaches no network**, and starts Ray only by the smoke script, leaving no Ray process.
  It never calls one of Ray's auto-init APIs outside a test that stands in `ray.init`.
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §6 conditions, in particular an existing test that fails
  once the stand-in stands in `_ray_is_running`, before the tests are written.

## 3. The review — ten checks

Make the review's venvs and exports fresh, offline, in a subdirectory of the scratchpad of their
own, not the agent's.

1. **Scope (E1).** `git show --stat <commit>` touches only §7's files. `git diff <parent> <commit>
   -- pyproject.toml README.md PROVENANCE.md docs/adoption docs/extraction .github
   prompts/extraction prompts/actor-names/02-release-v0.2.2.md` is empty. `git diff -- datastorekit`
   names three files. No venv, egg-info or scratch file; `git status --short --ignored` as at
   dispatch. Each client's `HEAD` and status as at dispatch.
2. **The fix, by reading (E2).** `_ray_is_running()` is module-level, returns
   `ray.is_initialized()`, and calls no auto-init API. `_kill_actors` returns before reading any
   handle when it is false, and is otherwise 01's. `__exit__`, `_close_refused_open` and the flag
   are unchanged. The docstrings say why, and name no client.
3. **The stand-in, by reading (E3).** The patch is on `sp_mod._ray_is_running` inside `active()`,
   beside `ray.kill`'s; `ray.is_initialized` is not patched anywhere in the stand-in; the
   docstring says so; nothing is opt-in.
4. **The tests, by reading (E4).** Test 7 patches `ray.init` to a recorder that raises around the
   close, restores Ray's own `ray.kill` and the module's own `_ray_is_running` (each captured at
   import, outside any `active()`), and asserts no call and `ray.is_initialized()` false. Test 8
   calls the captured helper (correction 1), and restores `ray.is_initialized` before `tearDown`.
   The module docstring has items 7 and 8, citing the prompt and the issue. **Read this before
   running (a).**
5. **The suite at both ends (E7).** In `venv/`, `Ran 494 tests … OK`. In a fresh high-end venv with
   `git archive <commit>` installed editable, the same, with the `ResourceWarning` lines counted
   (0 or 4 is timing). The port check and the guards pass; `black --check datastorekit docs`
   leaves 72 files.
6. **The breakages (E4).** Extract (a)–(c) from the log; check each with `git apply --check` and
   `-R --check` against its own export of the commit, install it, and run the suite, with
   `RAY_ENABLE_AUTO_CONNECT` unset. (a): test 7 alone, with four `ray.init` calls, and no Ray
   process during or after. (b): 169 entries as correction 2, up to the agent's form of test 6.
   (c): test 8 alone.
7. **Ray (E5).** In the review's own offline venvs at both ends, each with the commit's export
   installed editable: the smoke script exits 0, its output matches the log's step by step, the
   step C exception class at each end among it; no Ray process before or after. Then (c) at the
   high end: exit 1, as correction 3.
8. **The documents (E6).** Contract §9.4 in §9's form, each row's `path:line` read at the commit,
   its "Supersedes" column true of §9.3's rows; the head line in §9.3's form after `:31-32`;
   `git diff` of the contract and of the verification document removes no line. The verification
   subsection is between §4.6 and `## 5` (correction 4), dated, names this prompt, quotes both
   runs, and says §4.6 stays true of 01's tree. Every relative link and anchor added resolves.
9. **The close (E6).** This board: the entry at the head of §4 with its "Closed" line; §3 saying
   no issue is held; the header and 01b's row. The README's header and §2 row; `prompts/INDEX.md`.
   The index: the §1.3 row gone, a dated "None open" line, the count at 4 (0 on this repository's
   boards), the date.
10. **Nothing left behind.** No Ray process. `git tag -l` is the three tags, and `origin` is
    unchanged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 01b* paragraph, in the form of
  01's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log, in the verification subsection if it uses
    the phrase, in the README and in `prompts/INDEX.md`;
  - "reviewed" for 01b in the board's header and row, README §2 and `prompts/INDEX.md`;
  - the notes line, with this note marked "used for 01b".
- Anything the review finds that is not residue is opened on this board's §3 and in the index.
- **Report to the user:**
  - what landed: the helper and the guard, the stand-in's patch, tests 7 and 8, §9.4, the
    verification subsection, and the issue closed;
  - the suite at both ends, and the breakages, with (b)'s count and (a)'s four intercepted
    `ray.init` calls;
  - the smoke run at both ends from the review's own venvs, and (c);
  - the index at 4;
  - that 02 is re-measured against the tree 01b leaves, and amended in a planning commit of its
    own, before its note;
  - **and ask whether to push `main`** (§5).

## 5. Pushing

As 01's note §5: 01b makes no release and no tag. Its commit and the records after it are on local
`main` only, ahead of `origin/main` (`1925898`). **Ask the user, and wait for a clear yes.** With
approval, `git push origin main`, a fast-forward. Read the CI run once, when the user says it has
finished, and record its URL and both verdict lines on this board in a records commit of its own,
pushed with approval too. If either end fails, record it in §3 and the index, and tell the user.
Nothing is reverted without the user.

**Hand on.** 02 is re-measured against 01b's tree: its §1.1 claim about a client's stand-in is
rewritten (it is what the issue found wrong), its counts move to 494, and the wheel's facts are
re-taken. Then its orchestration note is written, and its tag is made only after CI is green on
its commit.
