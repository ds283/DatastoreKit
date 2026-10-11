# Log 01b — closing a pool starts no Ray

**Subject:** Start no Ray when closing a pool while not connected · **Commit:** `f024fc6` ·
**Date:** 2026-10-11 · **Model:** Claude Opus 5.5 · **Result:** landed; unpushed and untagged.

`[02-closing-a-pool-can-start-ray]` is fixed and closed. `SQL/ShardedPool.py` gains a module-level
`_ray_is_running()`, which returns `ray.is_initialized()`. `_kill_actors` now returns at once,
before reading any handle, when it is false. So a pool closed, or an open refused, while the process
is not connected to Ray kills nothing and never reaches Ray's `ray.kill`, which is one of Ray's
auto-init calls and would have run `ray.init()` first. While the process is connected, nothing
changes. Nothing else in the layer changes.

The stand-in pool stands in `_ray_is_running` as true inside `StandinCluster.active()`, beside
`ray.kill`, in every test. It leaves `ray.is_initialized` alone. No existing test moved: the 492
passed at the high end with the patch in place, before the new tests were written. Two tests, 7 and
8, join 01's module, so the suite goes from **492 to 494** in `venv/` and at the high end. There
were 0 `ResourceWarning` lines in `venv/`, and 0 and then 4 in the high end's two runs of the 494,
which is timing.
- Breakage (a), the guard removed, fails test 7 alone, `[1, 1, 1, 1] != []`, and starts no Ray.
- (b), the stand-in's patch removed, fails **170** entries.
- (c), `_ray_is_running` always false, fails test 8 alone.

Under real Ray, `docs/extraction/ray_smoke_run.py`, unchanged, exits 0 at both ends, every step
`PASS`, as at 01. Under (c) at the high end it fails at step N, with 4 of 4 names held, and exits 1.
No Ray process was up before or left after any run. `docs/client-contract.md` gains §9.4 and a head
line, and `docs/extraction-verification.md` gains §4.7. The issue moves to this board's §4, and the
index goes from **5 to 4 open** (0 on this repository's boards).

No client was written, run, imported or opened. Nothing was pushed, tagged or downloaded. Ray was
started only by the smoke script, three times.

Prompt: [`../01b-closing-a-pool-starts-no-ray.md`](../01b-closing-a-pool-starts-no-ray.md), with
the orchestrator's dispatch note §0: four corrections, its additions, its checked facts and its
conventions. §2 classifies each.

`<scratch01b>` below is `<session scratchpad>/agent01b`, outside the repository.

---

## 1. What shipped

### 1.1 The layer (§2.1)

`datastorekit/SQL/ShardedPool.py`, 16 lines added and none removed (`git diff --stat`). Line
numbers are `f024fc6`'s:

- **`_ray_is_running() -> bool`** (`:47-55`), after `_INCOMPLETE_COPY_SUFFIX` (`:44`) and before
  the first class (`_RelocationPlan`, `:58`). It returns `ray.is_initialized()` (`:55`). Its
  docstring says why it exists: `ray.is_initialized()` is not one of Ray's auto-init calls;
  `_kill_actors` kills nothing when it is false, since no actor of the process can then be alive,
  and Ray's `ray.kill`, one of its auto-init calls, would run `ray.init()` first and so start a
  local Ray. It also says that it is a function of the module, not a method, so that a test's
  stand-in can stand it in, as it stands in the module's `random`.
- **`_kill_actors`** (`:430-457`) returns at once when `_ray_is_running()` is false (`:446-447`),
  before it reads `_shards` or `_broker`. Its docstring gains one sentence (`:443-444`). Nothing
  else in it changes.
- **Nothing else.** `__exit__` (`:857-884`), `_close_refused_open` (`:390-428`), the closed flag
  and the names are 01's, unchanged; they have moved (`_close_refused_open` by 11 lines, from
  `:379-417`, and `__exit__` by 16, from `:841-868`). A pool closed while the process is not
  connected to Ray is still marked closed (`:884`).

### 1.2 The stand-in pool (§2.2)

`datastorekit/tests/standin_pool.py`, 8 lines added and 1 changed (`git diff --numstat`: 9 and 1):
- in `StandinCluster.active()` (`:292-314`), after the `ray.kill` patch (`:296`), a one-line
  comment and `mock.patch.object(sp_mod, "_ray_is_running", lambda: True)` (`:297-300`). It
  patches the name on the module, as `random` is patched, and does not touch `ray.is_initialized`;
- in the module docstring, a new item after the one for `ray.kill`. It says that the pool's
  `_ray_is_running` is true inside `active()`, since a stand-in cluster is a Ray session, so the
  pool's kills reach the stand-in `ray.kill`. It also says that `ray.is_initialized()` is left as
  it is, and stays false, since the tests assert it. The changed line is the end of the item
  before it (`.` → `;`).

Always on (U2): no test opts in or out.

### 1.3 The tests (§2.3)

`datastorekit/tests/test_closed_pool_releases_its_names.py`, 59 lines added and 1 changed (60 and 1). At
module level, `RAY_KILL = ray.kill` and `RAY_IS_RUNNING = sp.sp_mod._ray_is_running` (`:71-72`)
are captured when the module is imported, outside any `active()`. They follow a two-line comment.
A new class, `TestClosingAPoolStartsNoRay(_OneSessionCase)` (`:222`), comes after `TestAfterExit`:

| # | Test | What it does |
|---|---|---|
| 7 | `test_a_pool_closed_while_not_connected_to_ray_starts_no_ray` (`:223`) | Opens a pool in the cluster, gets a keypoint, and records the cluster's held names. Then, still inside `active()`, it nests three `mock.patch.object`s: `ray.init` (outermost) to a function that records its call and raises `RuntimeError`; `ray.kill` to `RAY_KILL`; and `sp_mod._ray_is_running` to `RAY_IS_RUNNING`. It closes the pool through `self.cluster.close_pool`. It asserts that `ray.init` was never called (the record is `[]`), that `__exit__` returned, and that `ray.is_initialized()` is false. It also asserts that the pool is marked closed and that the cluster's names are as before the close, so nothing was killed. |
| 8 | `test_ray_is_running_follows_ray_is_initialized` (`:250`) | Asserts that `sp_mod._ray_is_running` is not `RAY_IS_RUNNING`: inside `active()` the module's attribute is the stand-in's. Then, with `ray.is_initialized` replaced (by `mock.patch.object` in a `with`) by a function returning `True`, `RAY_IS_RUNNING()` is `True`; then with one returning `False`, it is `False`. Each `with` ends before `tearDown`'s `assertFalse(ray.is_initialized())`. |

The module's docstring gains items 7 and 8, citing "``actor-names`` prompt 01b" and the issue's
tag, and a paragraph. The paragraph says why the stand-in makes `_ray_is_running` true, why the
tests use the captured functions, and that test 7's `ray.init` stand-in is what keeps it from
starting Ray.

### 1.4 The documents (§2.4, §2.5)

- **`docs/client-contract.md`**, 21 lines added and none removed. One italic line at the head,
  after §9.3's, in its form: "*§9.4 is measured from the package at `actor-names` prompt 01b's
  tree, and its line numbers are that tree's.*" At the end comes **§9.4 `actor-names` prompt 01b**:
  a paragraph and one row, `ShardedPool._kill_actors`, when the process is not connected to Ray.
  Its "Supersedes" names §9.3's rows `ShardedPool.__exit__` and "A refused open", in their clauses
  that `_kill_actors` kills each actor, and says that both still hold whenever the process is
  connected. Its "Pinned by" names test 7 for the guard, test 8 for the helper's body, and the
  smoke script's step N for "while connected, every kill of §9.3 is made".
- **`docs/extraction-verification.md`**, 193 lines added and none removed. **§4.7** is inserted
  after §4.6.3's last line and before §4's closing rule and `## 5. The pin (U42)` (correction 4).
  It is dated and attributed to this prompt under rule 6, and says that §4.6 stays true of 01's
  tree. It gives the script's SHA-256 (unchanged), a table of both ends' runs, what they show,
  each end's full output, and (c)'s, with scratch paths as `<scratch01b>`.

### 1.5 The records (§2.6, §5 item 8)

- **This board**: the header (2 landed; 01b not yet reviewed; no issue open on this board), the
  "Owns" line, 01b's row, §3 (no issue held), and §4. The issue's entry moves from §3 to the head
  of §4, indented under a "**Closed** (2026-10-11, by `actor-names` prompt 01b, `f024fc6`)"
  paragraph. That paragraph names the guard, the stand-in's patch, the two tests and the smoke runs.
- **`docs/OPEN_ISSUES.md`**: the header (**4 open**: 0 on this repository's boards, 4 inherited),
  and §1.3's table replaced by a dated "None open" line.
- **This campaign's README**: a sentence in its header, and §2's row for 01b.
- **`prompts/INDEX.md`**: `actor-names`'s status, and its "Open issues" column (0).
- **This log.**

---

## 2. Deviations from the prompt

1. **Correction 1: test 8 calls the helper as captured when the module is imported**
   (`RAY_IS_RUNNING`), not `sp_mod._ray_is_running` looked up at call time. The class is built on
   `_OneSessionCase`, whose `setUp` enters `active()`, so inside test 8 the module's attribute is
   the stand-in's, and §2.3's "Outside `active()`" cannot hold. Of the two forms the note allows,
   I chose the capture, which test 7 needs anyway. `ray.is_initialized` is replaced by
   `mock.patch.object` in a `with` inside the test body, so it is restored before `tearDown`.
   Under (c), test 8 fails (§5). **STRUCTURALLY REQUIRED.**
2. **Correction 2: breakage (b)'s count.** The note measured 169 entries against its prototype.
   Here (b) gives **170**, `FAILED (failures=5, errors=165)`. The 161 entries in 11 other modules
   are the note's, module by module, and so are the 8 entries of 01's tests 1–4 and 6. The 170th is
   test 8, through its first assertion (item 6 below). The prompt's "as 01's breakage (a) did" is
   near, not exact: 01's (a) failed 159 entries in the other modules, and (b) adds one each in
   `test_one_timestamp_per_write` and `test_version_row_at_open`, since without the patch a refused
   open's kills are skipped too. Recorded as found.
3. **Correction 3: the smoke script under (c) runs no step after N.** Step N fails, "4 of 4 held
   (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store)" after `__exit__`, and the
   second open is refused with `ray.exceptions.ActorAlreadyExistsError`. Steps C, 3, 4, 5 and 6 are
   `NOT RUN` ("needs step N"), 0 Ray processes are left, and the script exits 1. The prompt names
   only step N. Recorded as found.
4. **Correction 4: where the verification subsection goes.** `:375` is §4.6's heading. §4 ended
   with §4.6.3's closing fence at `:575`, followed by a blank line, the rule `---` (`:577`) and
   `## 5. The pin (U42)` (`:579`). §4.7 is inserted after `:575`, so §4's closing rule follows it.
   Every other line number the prompt cites held at `3aa57ce`: in the package, in Ray's source at
   both ends (`AUTO_INIT_APIS` at `ray/__init__.py:211` and `:208`, `kill` in it, `is_initialized`
   in `NON_AUTO_INIT_APIS` at `:237` and `:233`), and in SGK at `b510bc9` (`active()` from `:231`,
   `ray.get` at `:233`). Recorded as found.
5. **The orchestrator's additions**, each followed as given, and each an **IMPLEMENTATION
   CHOICE**, at the orchestrator's direction:
   - the order of work. First the baseline. Then §2.1 and §2.2, and the existing 492 at the high
     end before any test was written (`Ran 492 … OK`, 0 warnings). Then §2.3 and the suite at both
     ends. Then test 7, read against hazard 2, and the breakages (a)–(c), each in its own export
     at the high end. Then the smoke runs at both ends, and (c)'s. Then the documents, the issue,
     the index and the records. Last, the final checks;
   - every export installed editable into a fresh offline venv (`ray`, `sqlalchemy` and
     `setuptools` first, then `--no-deps --no-build-isolation -e`), and no `PYTHONPATH`;
   - test 7's form: three nested `mock.patch.object`s over the close (`ray.kill` to Ray's own,
     `_ray_is_running` to the module's own, both captured at import, and `ray.init` to a recording
     function that raises), and the close made through `self.cluster.close_pool`;
   - `RAY_ENABLE_AUTO_CONNECT` unset for every run, (a) included (§3 item 2), and set nowhere;
   - under (a), test 7's assertion message quoted (§5);
   - the prose under `datastorekit/` names no client and no path that does not exist. The prompt
     is cited as "``actor-names`` prompt 01b", and the issue by its tag;
   - §9.4's "Pinned by" names tests 7 and 8 and the smoke script's step N.
6. **Test 8 first asserts that `sp_mod._ray_is_running` is not the captured function.** That is,
   it asserts that the stand-in's patch is in place inside the class's `active()`, and so that the
   captured function is the module's own. §2.3 does not ask for it. It makes test 8 a direct
   witness of §2.2, as well as of the helper's body. So under (b) test 8 fails too ("unexpectedly
   identical"), which is the one entry beyond the note's 169 (item 2). Under (c) it passes, and
   test 8 fails on the helper's body. **IMPLEMENTATION CHOICE.**
7. **Test 7 also asserts that the pool is marked closed, and that nothing was killed.** The note
   leaves the first to the agent (§2.1 item 3). The second, the cluster's names unchanged by the
   close, makes acceptance 1's "kills nothing" visible in the test. Neither changes what (a)
   reports: under (a) the `ray.init` record fails first, and the names are still held there too,
   since Ray's auto-init raises before any kill is attempted. **IMPLEMENTATION CHOICE.**
8. **In test 7, `ray.init` is the outermost of the three patches.** It is stood in before Ray's
   own `ray.kill` is restored and restored after the stand-in's `ray.kill` is put back. So Ray's
   `ray.kill` is never in place without it, even between the three patches. The note lists the
   patches in another order without fixing their nesting. A comment in the test says why.
   **IMPLEMENTATION CHOICE.**
9. **The new class is named `TestClosingAPoolStartsNoRay`**, after the prompt's title and in the
   form of the module's other classes. The note's prototype called it `TestNoRay`. **IMPLEMENTATION
   CHOICE.**
10. **The test module's docstring gains a paragraph** after items 7 and 8, as well as the items.
    It says why the stand-in makes `_ray_is_running` true, why the tests use the captured functions,
    and what keeps test 7 from starting Ray. **IMPLEMENTATION CHOICE.**
11. **The issue's entry is indented when it moves to §4**, under its closing paragraph, so that the
    two bullets with the same tag do not read as two issues. Its text is unchanged. Boards are not
    verification documents. **IMPLEMENTATION CHOICE.**
12. **The exports are of the working tree**, made by `git ls-files -z -co --exclude-standard |
    tar`, as log 01 §2 item 18 does, because the work was uncommitted. The baseline high end ran on
    `git archive HEAD` (`3aa57ce`). **STRUCTURALLY REQUIRED.**
13. **SGK's status at the start was not dispatch's.** Dispatch recorded SGK clean. At my start it
    had one untracked entry, `prompts/dk-and-rpk-migration/`, with `HEAD` at `b510bc9` on
    `handover-remedial` as stated. I did not write it: the clients were read only through `git`.
    It was the same at the end (§4.6). Recorded as found.

No UNINTENDED DRIFT was found.

---

## 3. The hazards (§3)

1. **Ray.** Ray was started only by the smoke script, from scratch venvs, three times: the low end
   (02:35:31), the high end (02:35:53) and (c) (02:36:26), one after another, with no suite
   running. By the script's own rule and by my check of the same rule
   (`<scratch01b>/probe/raycheck.sh`), no Ray process was up before or left after any run (§4.3).
   That rule is a `pgrep -f` of `gcs_server|raylet|ray::|default_worker\.py`, with each PID classed
   by `ps -o comm=` and shells dropped. The same check found 0 Ray processes at the start (02:16:57),
   before and after breakage (a) (02:28:23, 02:31:02), after (b) and (c) (02:34:48), before the
   final suites (02:40:56) and at the end (02:44:03). No `ray.kill`, `ray.init` or other auto-init call was made outside the stand-in or
   test 7.
2. **The new test cannot start Ray.** Before running (a), I read test 7 against this hazard:
   - Ray's own `ray.kill` is in place only inside the innermost two patches, and `ray.init` is stood
     in for the whole of that window, entered before it and restored after it (§2 item 8);
   - in that window the only call to `ray.kill` is `_kill_actors`'s, inside `self.close(pool)`;
     `ray.get` is still the stand-in's, and the pool has no profile agent;
   - Ray's `ray.kill` is `auto_init_wrapper(kill)`. Its `auto_init_ray()` calls `ray.init()`
     through the `ray` module's attribute (`ray/_private/auto_init_hook.py:14` at 2.43.0, `:15` at
     2.55.1, read in each venv), so it reaches the stand-in, which raises. `_kill_actors` ignores
     that, and the close returns.

   `RAY_ENABLE_AUTO_CONNECT` was unset for every run (and checked unset before (a)), so (a) could
   not pass for the wrong reason. Under (a), the stand-in was reached four times and Ray was not
   initialised. The module's `tearDownModule`, which raises if it is, passed, and no Ray process was
   found afterwards.
3. **The stand-in's patch carries every kill.** Without it, breakage (b), 170 entries fail. With
   it, the existing 492 passed at the high end before the tests were written, and nothing the suite
   saw at 01 changed.
4. **No network.** Every venv and install was `uv … --offline`. No `git fetch`, `push` or
   `ls-remote` was run.
5. **The package changes in `SQL/ShardedPool.py` only by the helper and the guard.** `git diff
   --stat -- datastorekit` names three files: `SQL/ShardedPool.py`, `tests/standin_pool.py` and
   the test module.
6. **Additive documents.** Under `docs/`, `git diff` removes no line of the contract or the
   verification document. `docs/OPEN_ISSUES.md` changes by its rule. `docs/adoption/` and
   `docs/extraction/` are unchanged.
7. **No client is touched.** The clients were read only with `git -C <client> rev-parse`, `status
   --short` and `show <commit>:<path>`. Their `HEAD`s and statuses are unchanged (§4.6).
8. **The count.** 492 before, and 494 after, at both ends.

---

## 4. Verification performed

### 4.1 The suite

Each run was made in the foreground, from its tree's root, with its output written to a scratch
file. The verdict was taken with `grep -E '^Ran |^OK|^FAILED'`, and the warnings with `grep -c
ResourceWarning`.

| When | Where | Result | `ResourceWarning` lines |
|---|---|---|---|
| start (02:17) | `venv/` (3.12.15 / 2.43.0 / 2.0.39) | `Ran 492 tests in 90.381s` / `OK` | 0 |
| start (02:19) | `<scratch01b>/base-hi`: `git archive HEAD` (`3aa57ce`), editable, 3.13.16 / 2.55.1 / 2.0.46 | `Ran 492 tests in 97.596s` / `OK` | 0 |
| after §2.1 and §2.2, before the tests (02:21) | `<scratch01b>/stage2-hi`: an export of the working tree | `Ran 492 tests in 91.579s` / `OK` | 0 |
| after §2.3 (02:23) | `venv/` | `Ran 494 tests in 103.931s` / `OK` | 0 |
| after §2.3 (02:25) | `<scratch01b>/stage3-hi`: an export of the working tree | `Ran 494 tests in 139.957s` / `OK` | 0 |
| end (02:41) | `venv/` | `Ran 494 tests in 89.273s` / `OK` | 0 |
| end (02:42) | `<scratch01b>/final-hi`: an export of the final working tree, this log included (before this table's last two rows and §4.6's end column were filled in) | `Ran 494 tests in 90.787s` / `OK` | 4 (two warnings, each "unclosed database" with tracemalloc's hint, the kind log 01 saw; the count is timing, log 01 correction 8) |

SQLite is 3.53.4 everywhere. `venv/` holds `datastorekit 0.2.1`, editable from this checkout, and
was not reinstalled. Each scratch venv's `datastorekit` was checked, from outside the export, to
import from that export's tree.

### 4.2 The checks

- **The port check**, `venv/bin/python docs/extraction/compare_ported_tests.py`: exit 0, "OK: 20
  module(s) keep their source's tests, classes and assertion skeletons; 1 test(s) declared not
  ported", at the start and at the end.
- **`black --check datastorekit docs`** (`black` 25.1.0): 72 files unchanged at the start and at
  the end. Each changed `.py` file was formatted with `black`.
- **The two guards**, `test_layer_is_generic` and `test_prose_names_no_source`, run on their own
  at the end: `Ran 14 tests … OK`; and in every run of the suite.
- **Scope** (hazard 5): `git diff --stat -- datastorekit` lists `SQL/ShardedPool.py` (16 added, 0
  removed), `tests/standin_pool.py` (9 and 1, by `--numstat`) and the test module (60 and 1).
  Every changed file is in §7's list, and `git status` adds only this log.
- **Ray's source, at both ends** (§6's fifth condition): `kill` is in `AUTO_INIT_APIS`
  (`ray/__init__.py:211` at 2.43.0, `:208` at 2.55.1), and `is_initialized` is in
  `NON_AUTO_INIT_APIS` (`:237`, `:233`). `auto_init_ray` reads `RAY_ENABLE_AUTO_CONNECT` once, at
  import (`auto_init_hook.py:7`, `:8`), and calls `ray.init()` when `ray.is_initialized()` is false.
- **The breakages as recorded** (§5): the three diff blocks of §5, extracted from this log, are
  byte-equal to the diffs applied. Each passed `git apply --check`, `git apply` and `git apply -R
  --check` on its own export when it was run, and again **as recorded here** on a fresh export of
  the final working tree (`<scratch01b>/final-hi/tree`, each applied and reversed in turn, the tree's `datastorekit/` then equal to the checkout's): each passed.

### 4.3 The smoke runs

Each ran from its own fresh export of the working tree and fresh offline venv, from the export's
root, as `env -u PYTHONPATH <venv>/bin/python docs/extraction/ray_smoke_run.py` under
`/usr/bin/time -p`. The script is unchanged (SHA-256 `e9be6ffa…c331`, equal in each export to the
file at `HEAD`). Each run's full output is in `docs/extraction-verification.md` §4.7.

| Run | Started | Ray's session directory | `ray.init` | Steps (1, 2, N, C, 3, 4, 5, 6) | In all | Exit | Ray before; after (script; mine) |
|---|---|---|---|---|---|---|---|
| low (3.12.15 / 2.43.0 / 2.0.39) | 02:35:31 | `session_2026-10-11_02-35-32_544683_10646` | 3.6 s | every one PASS: 0.7, 0.0, 1.5, 1.9, 2.3, 3.4, 0.0, 2.5 s | 18.3 s (real 18.55) | **0** | 0; 0 and 0 |
| high (3.13.16 / 2.55.1 / 2.0.46) | 02:35:53 | `session_2026-10-11_02-35-55_125717_10866` | 6.5 s | every one PASS: 1.7, 0.3, 4.1, 3.0, 3.0, 3.2, 0.0, 2.9 s | 27.6 s (real 27.91) | **0** | 0; 0 and 0 |
| (c), high | 02:36:26 | `session_2026-10-11_02-36-27_901115_11394` | 5.0 s | 1 PASS, 2 PASS, **N FAIL**, C and 3–6 NOT RUN | 11.0 s (real 11.26) | **1** | 0; 0 and 0 |

At both ends, after each read-write pool's `__exit__`, the pool referenced, 0 of 4 names were held,
and 0 of 3 after the read-only pool's. Step N's second open worked at once, and step 5's refused
open left 0 of 4 held. **Step C's second open was refused with `builtins.ValueError` at 2.43.0 and
`ray.exceptions.ActorAlreadyExistsError` at 2.55.1**, each with Ray's "is already taken" message
naming `SerialPoolBroker`. The first pool then served step 2's get, serials `[1, 2]`. These are
§4.6's results. The times are longer than 01's runs, mostly in steps N, C, 3, 4 and 6. The cause
was not measured, and the results did not change.

Under (c), step 2's record was already 4 of 4 held after `__exit__`. Step N failed:

```text
FAIL  step N (0.2 s): __main__.StepFailed: after __exit__, the pool referenced, 4 of 4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store); the second open raised ray.exceptions.ActorAlreadyExistsError: The name SerialPoolBroker (namespace=None) is already taken. Please use a different name or get the existing actor using ray.get_actor('SerialPoolBroker', namespace='None')
```

Its `finally` dropped the pools, whose names were then free after 0.0 s. Before and after each run,
`RAY_ADDRESS` and `RAY_ENABLE_AUTO_CONNECT` were unset and there was no
`/tmp/ray/ray_current_cluster`. Ray's other session directories under `/tmp/ray/` were not
touched.

### 4.4 The breakages

§5.

### 4.5 The documents

- Every relative link added resolves from its file:
  - in the contract, `../prompts/actor-names/README.md`;
  - in the verification document, `../prompts/actor-names/01b-closing-a-pool-starts-no-ray.md` and
    `../prompts/actor-names/logs/01b-closing-a-pool-starts-no-ray.md`;
  - in this campaign's board and README, `logs/01b-closing-a-pool-starts-no-ray.md`.

  No anchor was added.
- Every `path:line` of §9.4 and of §1 above was read at this tree with `sed -n`:
  - `SQL/ShardedPool.py`: `:44`, `:47-55`, `:55`, `:58`, `:390-428`, `:428`, `:430-457`,
    `:443-444`, `:446-447`, `:857-884`, `:867-868`, `:883`, `:884`;
  - `tests/standin_pool.py`: `:292-314`, `:296`, `:297-300`;
  - the test module: `:71-72`, `:222`, `:223`, `:250`.
- `git diff` of `docs/client-contract.md` and `docs/extraction-verification.md` has no removed
  line.

### 4.6 The clients

Read only with `git -C <client> rev-parse HEAD`, `rev-parse --abbrev-ref HEAD`, `status --short`
and, for SGK, `show b510bc9:<path>`.

| Client | Start (02:17) | End |
|---|---|---|
| SecondaryGWKit | `b510bc9`, `handover-remedial`, 1 untracked entry (`prompts/dk-and-rpk-migration/`; §2 item 13) | `b510bc9`, `handover-remedial`, the same 1 untracked entry (02:44; `diff` of the two listings empty) |
| ChamPBH | `52142d7`, `main`, 23 untracked entries | `52142d7`, `main`, the same 23 untracked entries (`diff` empty) |
| StochasticInstantons | `7bb3efd`, `main`, clean | `7bb3efd`, `main`, clean |

---

## 5. The deliberate-breakage record (§4.4)

Each diff is relative to the repository root, exactly as applied. Each was applied to its own fresh
export of the working tree (`<scratch01b>/break-<x>/tree`), with its own fresh offline venv at the
high end (3.13.16 / 2.55.1 / 2.0.46), installed editable. Each passed `git apply --check`, was
applied with `git apply`, and then passed `git apply -R --check`. Each was checked again **as
recorded here**, extracted from this log, against a fresh export of the final tree (§4.2). None was
committed. The whole suite ran under each: 494 tests. "Entries" are `unittest`'s failures plus
errors, with a sub-test counting on its own. `RAY_ENABLE_AUTO_CONNECT` and `RAY_ADDRESS` were unset
for each.

### (a) the guard removed from `_kill_actors`

```diff
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -443,8 +443,6 @@
         When this process is not connected to Ray (_ray_is_running() is false), it kills
         nothing and returns at once, so that closing a pool never starts Ray.
         """
-        if not _ray_is_running():
-            return
         shards = self._shards if isinstance(self._shards, dict) else {}
         handles = list(shards.values())
         broker = getattr(self, "_broker", None)
```

`FAILED (failures=1)`: **test 7** only, on its first assertion:

```text
AssertionError: Lists differ: [1, 1, 1, 1] != []
```

That is `ray.init` reached four times, once for each of the three shards and once for the broker.
Each time it was the test's stand-in, which raised, and `_kill_actors` ignored it. **No Ray was
started.** `ray.is_initialized()` stayed false: the module's `tearDownModule`, which raises if it is
true, passed, and my check found 0 Ray processes before (02:28:23) and after (02:31:02). Every other
test passed, since the stand-in's `_ray_is_running` is true in every other test, and the guard is
not reached there. 4 `ResourceWarning` lines: the count is timing (log 01, correction 8).

### (b) the stand-in's `_ray_is_running` patch removed — the positive control

```diff
--- a/datastorekit/tests/standin_pool.py
+++ b/datastorekit/tests/standin_pool.py
@@ -294,10 +294,6 @@
         with contextlib.ExitStack() as stack:
             stack.enter_context(mock.patch.object(ray, "get", standin_get))
             stack.enter_context(mock.patch.object(ray, "kill", standin_kill))
-            # a stand-in cluster is a Ray session: the pool's kills are made
-            stack.enter_context(
-                mock.patch.object(sp_mod, "_ray_is_running", lambda: True)
-            )
             stack.enter_context(
                 mock.patch.object(
                     sp_mod, "Datastore", _StandinActorClass(DatastoreClass, self)
```

`FAILED (failures=5, errors=165)`: **170 entries**. Without the patch, `_ray_is_running()` is
false in every test, `_kill_actors` kills nothing, and the names stay reserved in each cluster.

- **9 in 01's module.** Tests 1, 2, 3 and 4 fail with one error each, on the stand-in's collision
  (`ValueError: The name SerialPoolBroker (namespace=None) is already taken. …`, and test 2's on
  `shard0002-store`). Test 6 fails in its three sub-tests (`StandinActorDied not raised`) and on
  its call log (`24 != 21`). Test 8 fails on its first assertion, `AssertionError: unexpectedly
  identical: <function _ray_is_running at …>` (§2 item 6). Tests 5 and 7 pass.
- **161 in 11 other modules**, every one on a name collision: `test_one_timestamp_per_write` 54,
  `test_reconcile_at_open` 45, `test_replicated_write` 14, `test_version_row_at_open` 10,
  `test_prune_at_open` 9, `test_store_schema` 8, `test_refused_open_closes_engines` 7,
  `test_read_only_pool` 5, `test_version_keyed_lookups` 5, `test_shard_key_assignment` 3,
  `test_declared_facts` 1.

In all, 158 entries are on `SerialPoolBroker` and 7 on `shard0002-store`, plus the 3 sub-tests,
test 6's log and test 8. The 161 are the note's, module by module. They are 01's breakage (a)'s 159
and one more each in `test_one_timestamp_per_write` and `test_version_row_at_open`, where a refused
open's kills are skipped too (correction 2). 0 `ResourceWarning` lines.

### (c) `_ray_is_running` made to return `False`

```diff
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -52,7 +52,7 @@
     ray.init() first and so start a local Ray. It is a function of the module, not a method, so
     that a test's stand-in can stand it in, as it stands in the module's random.
     """
-    return ray.is_initialized()
+    return False
 
 
 class _RelocationPlan(NamedTuple):
```

`FAILED (failures=1)`: **test 8** only, `AssertionError: False is not True`: with
`ray.is_initialized` returning `True`, the module's own `_ray_is_running` returned `False`. Every
other test passed, since the stand-in replaces the helper in every test. 0 `ResourceWarning` lines.

**Then under real Ray, at the high end:** the smoke script, unchanged, from the same export
(§4.3). Step N fails, 4 of 4 names held after `__exit__` and the second open refused. Steps C and
3–6 are not run, the script exits 1, and no Ray process is left (correction 3). Beyond test 8, only
the smoke run sees (c).

---

## 6. Observations not acted on

1. **The docstrings of `__exit__` and `_close_refused_open` still say, without qualification,
   that the actors are killed.** The guard is stated in `_kill_actors`'s docstring and in
   `_ray_is_running`'s, which both name. §2.1 item 3 keeps both methods unchanged, so their
   docstrings were not touched. A reader who stops at `__exit__`'s docstring would not learn that a
   close while not connected to Ray kills nothing. This is prose only, and no issue is opened.
2. **A client's stand-in that does not stand in `_ray_is_running` now gets no kill.** At this
   tree, SGK's stand-in (`Datastore/tests/standin_pool.py` at `b510bc9`, `active()` from `:231`)
   stands in `ray.get` and the actor classes, but neither `ray.kill` nor `_ray_is_running`. So
   inside it, a close kills nothing and starts no Ray. That matches that stand-in, which reserves
   no names. SGK's `ComputeTargets/tests/test_quadsource_policy_main.py` also asserts `not
   ray.is_initialized()` in its `tearDownModule` (`:430-431` at `b510bc9`). So under 01's tree that
   module would have started a local Ray and also failed; at this tree it does neither. I read
   this through `git show` only. Nothing of SGK was run, and this is for 02's adoption addenda, not
   for the package or the contract.
3. **The test module's docstring says "Each test opens its pools in one `StandinCluster`".** Test
   8 opens no pool, though it runs in one. This was left as it is.
4. **The scratch tools** are in `<scratch01b>/probe/`, not in the repository: `raycheck.sh` (the
   smoke script's process rule), `mkexport.sh` (an export and its venv), `suite.sh`, `breakrun.sh`
   (an export, a breakage and the suite) and `smoke.sh`. Each run's output is in
   `<scratch01b>/logs/`, and each breakage's diff in `<scratch01b>/diffs/`.

---

## 7. Issues

- **Closed**: `[02-closing-a-pool-can-start-ray]`, moved from this board's §3 to the head of its
  §4, with its closing paragraph.
- **Opened, narrowed**: none.
- **`docs/OPEN_ISSUES.md`**: 5 → **4** open, 0 on this repository's boards, 4 inherited.

---

## 8. State handed to the next prompt

- **`HEAD`** is `f024fc6`, unpushed and untagged. `origin/main` is `1925898`, and the tags are
  `v0.1.0`, `v0.2.0` and `v0.2.1`, unchanged. `pyproject.toml` is at `0.2.1`. Prompt 02 is
  unchanged, and is re-measured against this tree before its orchestration note (README §2).
- **The suite** is 494, in `venv/` and at the high end. The port check passes over 20 modules with
  1 test declared not ported. `black` leaves 72 files unchanged.
- **The interfaces** (README §4): `SQL/ShardedPool.py`'s `_ray_is_running()` and the guard in
  `_kill_actors`; the stand-in's patch of `_ray_is_running` in `active()`, always on; tests 7 and 8
  of `tests/test_closed_pool_releases_its_names.py`; contract §9.4;
  `docs/extraction-verification.md` §4.7.
- **For 02** (`v0.2.2`, U3): 02 §1.1's claim that the kill under a client's stand-in "never starts
  Ray" was false at 01's tree. At this tree it holds, by the guard, and not by Ray's
  `check_connected()`. Under such a stand-in a close kills nothing (§6 item 2).
- **Open**: none on this repository's boards; the four inherited issues of `docs/OPEN_ISSUES.md`
  §1.2.
