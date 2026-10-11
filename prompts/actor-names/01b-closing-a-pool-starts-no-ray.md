# Prompt 01b — closing a pool starts no Ray

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 01 landed (`ac50a8a`) and was reviewed (`049fa1a`). CI passed on `049fa1a` at both ends
  (`168ecd0`).
- U4 is taken (README §6.2): the user chose, on 2026-10-11, to fix this before the release. The
  form below is the planner's recommendation, and the user may change it at dispatch.
- `git status` is clean in this repository, and `origin/main` is an ancestor of `main`.
- `datastorekit/` is `ac50a8a`'s: `git diff --stat ac50a8a HEAD -- datastorekit` is empty.

**Closes:** `[02-closing-a-pool-can-start-ray]`. **Narrows:** nothing. **Opens:** only what the
work finds.

**Recommended model:** **Opus.**
- The code change is four lines and a helper, but it sits in the pool's close, which every test and
  every client runs through.
- The stand-in's change is one line, and it carries every kill the suite makes. A slip there fails
  the suite widely or, worse, hides the guard from it.
- The new test must not be able to start Ray, even under its own breakage.

**Read first:**

1. [`README.md`](README.md): §0, §5 (every rule) and §6.2 (U1, U2 and U4).
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`.
3. This board's §3 entry for the issue, and its record of how the issue was found.
4. Log 01 (`logs/01-a-closed-pool-releases-its-actor-names.md`), §1 and §5 (the breakages), and
   prompt 01 §2.1 and §2.2.
5. The code: `datastorekit/SQL/ShardedPool.py` (`import ray`, `:10`; the module constants,
   `:38-44`; `_close_refused_open`, `:379-417`; `_kill_actors`, `:419-441`; `__exit__`,
   `:841-868`), `datastorekit/tests/standin_pool.py` (its docstring, `:1-44`; `standin_kill`,
   `:214-231`; `StandinCluster.active`, `:288-306`) and
   `datastorekit/tests/test_closed_pool_releases_its_names.py`.
6. Ray's own code, in `venv/` (Ray 2.43.0) and in a high-end scratch venv (2.55.1): `ray/__init__.py`
   (`AUTO_INIT_APIS`), `ray/_private/auto_init_hook.py` (`auto_init_ray`) and
   `ray/_private/worker.py` (`def kill`, `def is_initialized`).
7. `docs/client-contract.md` §9 (its form, and §9.3), and `docs/OPEN_ISSUES.md`.

Line numbers are at `1925898`, whose `datastorekit/` is `ac50a8a`'s, measured on 2026-10-11.

---

## 1. What is wanted

After this prompt, **closing a pool never starts Ray.** `_kill_actors` kills nothing when this
process is not connected to Ray. When it is connected, nothing changes: every kill of 01 is made as
before, and the suite and the smoke run see exactly what they saw at 01.

**Nothing the layer writes changes.** No API is added. `pyproject.toml` stays at `0.2.1`: 02
releases, once it is re-measured against the tree this prompt leaves (README §2).

### 1.1 The defect, measured

The orchestrator found it on 2026-10-10 while checking 02's facts at `1925898`. 02 §1.1 says
that, under a client's stand-in that patches `ray.get` and not `ray.kill`, the pool's kill reaches
Ray's `ray.kill`, which raises `RaySystemError` without starting Ray. **It does start Ray.**
- `ray.kill` is in Ray's `AUTO_INIT_APIS` at both ends (`ray/__init__.py:211-220` at 2.43.0,
  `:208-217` at 2.55.1). `ray/__init__.py` wraps each of them with `auto_init_ray`, which calls
  `ray.init()` when `ray.is_initialized()` is false and `RAY_ENABLE_AUTO_CONNECT` is not `"0"`.
  The `check_connected()` in `ray/_private/worker.py`'s `def kill` is reached only after that.
- **Probed at 2.55.1, once.** `ray.kill` of an object that is not a handle, in a process with no
  Ray, logged "Started a local Ray instance", then raised `ValueError` ("ray.kill() only supported
  for actors"). `ray.is_initialized()` was then `True`. The Ray it started was shut down when the
  process exited, and no Ray process was left. That probe broke README §5 rule 7, since it was not
  the smoke script. The board records it, and nothing else in this campaign repeats it: 2.43.0 is
  known from its source, which is the same in the lines above.
- `_kill_actors` ignores what a kill raises, so the close returns normally. **The side effect is a
  local Ray, started by a close and left up for the rest of the process.**

**Who meets it.** A process that closes a pool while not connected to Ray. Under real Ray, a pool's
actors exist only while the process is connected, so in practice this is a client's test stand-in
that stands in `ray.get` and the actor classes but not `ray.kill`. Read through `git` at the
checklists' commits (SGK `b510bc9`, CPBH `52142d7`, SI `7bb3efd`):
- **SGK** keeps `Datastore/tests/standin_pool.py`. Its `active()` (`:231-247`) patches `ray.get`
  (`:233`), the two actor classes and `random`, not `ray.kill`. Its staying importer
  `ComputeTargets/tests/test_quadsource_policy_main.py` opens a pool on stand-in shards in
  `TestTheExtractionScript.setUp` and closes it in a cleanup, inside `active()`. Its docstring says
  "No Ray". Under `v0.2.2` as 01 left it, that close would start a local Ray.
- **CPBH and SI** patch neither `ray.get` nor `ray.kill` anywhere outside their prompts and docs.
  SI's `tests/conftest.py` runs real Ray, and closes its pool before `ray.shutdown()`.

`v0.2.2` is a tag that is never moved, and every client adopts it (U3). So the fix lands before the
tag (U4).

### 1.2 What the planner measured

In scratch exports of `1925898`, with a prototype of §2.1–§2.3, offline:
- **The prototype.** A module-level `_ray_is_running()` in `SQL/ShardedPool.py`, returning
  `ray.is_initialized()`. `_kill_actors` returns at once when it is false. In the stand-in's
  `active()`, `mock.patch.object(sp_mod, "_ray_is_running", lambda: True)` beside the `ray.kill`
  patch. A scratch test, as §2.3's test 7.
- **The suite:** `Ran 493 tests … OK` at both ends: Python 3.12.15 / Ray 2.43.0 / SQLAlchemy
  2.0.39 and 3.13.16 / 2.55.1 / 2.0.46, SQLite 3.53.4, each export installed editable. There were
  0 `ResourceWarning` lines at each end. 493 is 492 and the one scratch test; §2.3's test 8 was not
  prototyped.
- **The breakage of the guard**, at the high end only: with the two guard lines removed, the scratch
  test failed, and its `ray.init` stand-in was reached four times, once for each of three shards
  and once for the broker. No Ray was started: the stand-in raised in place of `ray.init`.
- **The smoke run, unchanged, under real Ray**, with the prototype installed: exit 0 at both ends,
  every step `PASS`, 0 of 4 names held after each read-write `__exit__`. Step C raised
  `builtins.ValueError` at 2.43.0 and `ray.exceptions.ActorAlreadyExistsError` at 2.55.1. No Ray
  process was left.
- **Why not the obvious form.** Faking `ray.is_initialized` inside `active()` would fail every
  test whose `tearDown` asserts `self.assertFalse(ray.is_initialized())`, which runs while
  `active()` is still entered (`tearDown` runs before cleanups). The assertion is in 13 modules,
  in a `tearDown` in 12 of them (`grep -rn 'assertFalse(ray.is_initialized())' datastorekit/tests`),
  and 01's module is one.

---

## 2. What to change

### 2.1 `datastorekit/SQL/ShardedPool.py` (U4)

1. **A module-level helper, `_ray_is_running() -> bool`**, after the module constants (`:44`),
   before the first class. It returns `ray.is_initialized()`, which is not one of Ray's auto-init
   calls. Its docstring says why it exists: `_kill_actors` kills nothing when it is false, since no
   actor of this process can then be alive, and Ray's `ray.kill` would run `ray.init()` first. It is
   a function of the module, not a method, so that the stand-in can stand it in as it stands in
   `random` (§2.2).
2. **`_kill_actors`** (`:419-441`) returns at once, before reading any handle, when
   `_ray_is_running()` is false. Nothing else in it changes. Its docstring gains one sentence
   saying so.
3. **Nothing else.** `__exit__`, `_close_refused_open`, the closed flag and the names are 01's,
   unchanged. If `_ray_is_running()` is false, a closed pool is still marked closed by `__exit__`.
4. **The prose guards** (`test_prose_names_no_source`, `test_layer_is_generic`) still pass: name
   nothing of the source repository or of any client.

### 2.2 `datastorekit/tests/standin_pool.py` (U4)

1. **`_ray_is_running` is stood in** inside `StandinCluster.active()` (`:288-306`), beside the
   `ray.kill` patch (`:292`), as a function returning `True`: a stand-in cluster is a Ray session.
   Patch the name on `sp_mod`, as `random` is patched (`:303-305`), not `ray.is_initialized` (§1.2).
2. **The module docstring** says what is stood in, beside `ray.kill` (`:18-25`): the pool's
   `_ray_is_running` is true inside `active()`, and `ray.is_initialized()` is left as it is.
3. **Always on**, as U2. No test opts in or out.

### 2.3 Two tests in `datastorekit/tests/test_closed_pool_releases_its_names.py`

In a new class after `TestAfterExit`, built on `_OneSessionCase`:

7. **A pool closed while this process is not connected to Ray starts no Ray.** Open a pool in the
   cluster. Then, still inside `active()`, restore Ray's own `ray.kill` and the pool's own
   `_ray_is_running`, which is what a client's stand-in that does not stand in `ray.kill` leaves.
   Replace `ray.init` with a function that records its call and raises. Close the pool. Assert:
   - `ray.init` was never called;
   - `__exit__` returned;
   - `ray.is_initialized()` is false.

   Capture Ray's `ray.kill` and the module's `_ray_is_running` when the test module is imported,
   which is outside any `active()`. **The `ray.init` replacement is what keeps this test from ever
   starting Ray**, under breakage (a) too: Ray's auto-init calls `ray.init()` through the `ray`
   module's attribute, so the replacement intercepts it. Do not use `RAY_ENABLE_AUTO_CONNECT=0` in
   its place: it is read when Ray is imported, and it would hide (a).
8. **`_ray_is_running` follows `ray.is_initialized()`.** Outside `active()`, with
   `ray.is_initialized` replaced by a function returning `True` and then one returning `False`,
   `sp_mod._ray_is_running()` returns each. This is the suite's only witness of the helper's body
   (breakage (c)). Restore `ray.is_initialized` before the test's `tearDown`.

Extend the module's docstring with items 7 and 8, citing this prompt and the issue. Name and word
the tests as the module's others are.

### 2.4 `docs/client-contract.md`

A new subsection, **§9.4**, in §9's form, headed for this campaign's prompt 01b, measured at this
prompt's tree. One row:
- **`ShardedPool._kill_actors`, when the process is not connected to Ray.** It kills nothing and
  starts no Ray: `_ray_is_running()` (`path:line`) is false, and `_kill_actors` returns
  (`path:line`). Ray's `ray.kill` would have run `ray.init()` first. Its "Supersedes" column names
  §9.3's two rows that say `_kill_actors` kills each actor: they still hold whenever the process is
  connected to Ray, which a pool with live actors always is.

Add one italic line at the contract's head, in §9.3's form, after §9.3's (`:31-32`). Remove or
rewrite no line.

### 2.5 `docs/extraction-verification.md`

A new dated subsection at the end of §4, after §4.6 (`:375`), saying it was added by `actor-names`
prompt 01b (`CLAUDE.md` rule 6). It gives the smoke run at both ends at this prompt's tree, with
the script unchanged, and says that §4.6 stays true of 01's tree. Nothing above it changes.

### 2.6 The issue

- **This board:** the entry moves from §3 to the head of §4 with a "**Closed** (date, by
  `actor-names` prompt 01b, this commit)" line naming the guard, the stand-in's patch, the two
  tests and the smoke runs. §3 then says no issue is held on this board.
- **`docs/OPEN_ISSUES.md`:** the row in §1.3 is deleted, and §1.3 says "None open", dated. The
  count goes back to **4** (0 on this repository's boards), and the date is updated.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **Ray.** README §5 rule 7. Ray is started only by the smoke script, at each end, with no Ray
   process up before or left after, by the script's own check. Do not probe `ray.kill`, or any of
   Ray's auto-init calls, outside a test that stands in `ray.init`. The suite never runs while Ray
   is up.
2. **The new test cannot start Ray**, under any breakage (§2.3, test 7). Before running (a), read
   the test and confirm that `ray.init` is replaced in every path that reaches Ray's `ray.kill`.
3. **The stand-in's patch carries every kill.** Without it, `_ray_is_running()` is false in every
   test, `_kill_actors` kills nothing, and the names stay reserved: breakage (b). With it, nothing
   the suite saw at 01 changes.
4. **No network.** Every venv and install is `uv … --offline`.
5. **The package changes in `SQL/ShardedPool.py` only**, there only by the helper and the guard,
   and `git diff -- datastorekit` names three files: that one, `tests/standin_pool.py` and the test
   module.
6. **Additive documents.** Under `docs/`, the contract gains §9.4 and a head line, the verification
   document a subsection, and neither loses a line. `docs/OPEN_ISSUES.md` changes by its rule.
7. **No client is touched.** Nothing of a client is written, run, imported or opened.
8. **A count that falls is a stop.** The suite is 492 before, and 494 after, at both ends.

---

## 4. Verification

1. **The suite.** In `venv/`, `Ran 492 tests … OK` before, and `Ran 494 tests … OK` after. The
   same at the high end, in a fresh offline venv (Python 3.13.16 / Ray 2.55.1 / SQLAlchemy 2.0.46,
   with `setuptools`) with an export of your tree installed editable (`--no-deps
   --no-build-isolation`). Record the `ResourceWarning` lines at each end: 0 in `venv/`, and 0 or 4
   at the high end, which is timing (log 01, correction 8).
2. **The checks.** `compare_ported_tests.py` exits 0 with "20 module(s) … 1 test(s) declared not
   ported". `black --check datastorekit docs` leaves 72 files unchanged. The two guards pass.
3. **The smoke run** at both ends, with the script unchanged, from fresh offline venvs with an
   export of your tree installed editable: exit 0, every step `PASS`, its full output, its time,
   and Ray's processes before and after.
4. **The breakage record.** Each is a diff, exactly as applied, to its own scratch export, never
   committed, checked with `git apply --check` and `-R --check` as recorded. Run the suite under
   each, or the module where said, and record which tests fail:
   - **(a)** the guard removed from `_kill_actors`. Test 7 fails, with `ray.init` reached once for
     each shard and once for the broker. Nothing else fails. No Ray is started.
   - **(b)** the stand-in's `_ray_is_running` patch removed. 01's tests 1–4 and 6 fail, and most
     modules that reopen a store in one cluster, as 01's breakage (a) did (log 01 §5): record the
     count. The positive control that the patch carries the kills.
   - **(c)** `_ray_is_running` made to return `False`. Test 8 fails. Everything else passes, since
     the stand-in replaces the helper. Then at the high end only, the smoke script under (c): step
     N fails with 4 of 4 names held after `__exit__`, and it exits 1 (expected; the planner did
     not run it). Beyond test 8, only the smoke run sees (c).
5. **The documents.** Every relative link and anchor you add resolves. Every `path:line` you cite
   is read at your tree.
6. **The clients.** Record each client's `HEAD` and `git status --short`, at the start and the end,
   unchanged.

---

## 5. Acceptance

1. A pool closed, or an open refused, while the process is not connected to Ray kills nothing and
   starts no Ray. While it is connected, every kill of 01 is made.
2. The stand-in stands in `_ray_is_running` inside `active()`, in every test, and leaves
   `ray.is_initialized` alone.
3. Tests 7 and 8 pass, and §4.4's breakages fail as stated.
4. The smoke script, unchanged, exits 0 at both ends under real Ray, fails under (c), and leaves no
   Ray process.
5. The contract has §9.4 and its head line, and the verification document its subsection.
6. The issue is closed on this board and gone from the index, at 4.
7. §4.1–§4.6 hold.
8. **The records**, in the same commit: the log `logs/01b-closing-a-pool-starts-no-ray.md` per
   README §5.1, with the smoke runs, the breakage record and the clients at both ends; this
   board (its row for 01b, §3, §4 and the header); `docs/OPEN_ISSUES.md`; `prompts/INDEX.md`; and
   this campaign's README (its header and §2's row for 01b).

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count is not 494, in any venv, other than under a breakage.
- An existing test fails once the stand-in stands in `_ray_is_running`.
- The smoke script fails at either end, other than under (c).
- A Ray process is up before a run or left after one, or anything other than the smoke script
  starts Ray.
- `ray.kill` is not among `AUTO_INIT_APIS`, or `ray.is_initialized` is, at either end.
- Anything would change a file outside §7, push, make or move a tag, download anything, or write,
  run, import or open anything of a client.

---

## 7. What this prompt changes, and what it does not

- **Files it adds:** the log.
- **Files it changes:**
  - `datastorekit/SQL/ShardedPool.py`, by §2.1 only;
  - `datastorekit/tests/standin_pool.py`, by §2.2 only;
  - `datastorekit/tests/test_closed_pool_releases_its_names.py`, by §2.3 only;
  - `docs/client-contract.md`, by §2.4, and `docs/extraction-verification.md`, by §2.5;
  - `docs/OPEN_ISSUES.md`;
  - this campaign's board and README (its header and §2's row for 01b), and `prompts/INDEX.md`.
- **It changes nothing else:** not `pyproject.toml`, `README.md`, `PROVENANCE.md`, `docs/adoption/`,
  `docs/extraction/`, prompt 02, the extraction board, the workflow, `CLAUDE.md`, `LICENSE` or
  `.gitignore`.
- **It touches no client repository.**
- **It makes no tag and pushes nothing.**
