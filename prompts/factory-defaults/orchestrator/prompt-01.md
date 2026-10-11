# Orchestrator — prompt 01, the base defaults three hooks

Read [`../README.md`](../README.md) first: §0, §1, §4, §5 (every rule) and §6.2 (U1–U3). Then
read `actor-names`' [`prompt-01.md`](../../actor-names/orchestrator/prompt-01.md) and
[`prompt-01b.md`](../../actor-names/orchestrator/prompt-01b.md), whose "Conventions", additions on
installing and on breakages, and §3–§5 this note keeps unless it says otherwise.

**You do not write code.** You may:
- run the suite, the port check, `black --check` and the guards;
- make venvs in the session scratchpad with `uv … --offline`, from the cache the extraction
  campaign filled;
- export the tree with `git archive` into the scratchpad, and run prototypes, the smoke script and
  breakages there, never in this checkout and never committing one;
- start Ray **only** through the smoke script, under README §5 rule 7, with no Ray process up
  before or left after, and never while a suite runs;
- reach the network only for one `git ls-remote origin` at dispatch and one at the review;
- read the three clients only through `git -C <client> rev-parse|status|show|grep`;
- fix small residue in a follow-up commit of your own (§4);
- after the review, and only with the user's approval, push `main` (§5).

**The prompt:** [`01-the-base-defaults-three-hooks.md`](../01-the-base-defaults-three-hooks.md)
**Closes:** nothing on a board · **Addresses:** extraction 07a §7.3 · **Revisits:** extraction U32,
in part · **Opens:** only what the work finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- U1–U5 are taken, and 01 is written (`93446be`).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- `git diff --stat 6d8ee9a HEAD -- datastorekit pyproject.toml` is empty: the package is
  `v0.2.2`'s. Under `docs/`, only `docs/OPEN_ISSUES.md` differs from `6d8ee9a` (one line, at
  `460b012`).
- `origin/main` is `460b012` (`git ls-remote origin`, 2026-10-11), an ancestor of `main`, which is
  ahead of it by `93446be` and this note. The tags are `v0.1.0` (`0ece4aa` → `68db557`), `v0.2.0`
  (`9eaf542` → `240028e`), `v0.2.1` (`0ba2e4d` → `33778b0`) and `v0.2.2` (`c32d027` → `6d8ee9a`),
  here and on `origin`, and no other.
- The clients' `HEAD`s: SGK `6861a9f` (branch `handover-remedial`), CPBH `52142d7` (`main`, 1
  modified entry, `prompts/INDEX.md`, and 24 untracked), SI `7bb3efd` (`main`, clean). **SGK is
  being worked on by another session**: its untracked list grew from 0 to 17 entries
  (`docs/dk-and-rpk-migration/rehearsal/*_05.txt`) while this note was written. Its `HEAD` is what
  is compared; a changed untracked list there is not this campaign's doing, and is recorded, not
  stopped on.
- The index is **4** (0 on this repository's boards, 4 inherited), and stays 4 unless the work
  opens an issue.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**The code change is three deleted lines; everything else is evidence.** The base's diff is three
`@abstractmethod`s and a moved comment. The risk is what must *not* change: no hook's signature or
body, no message, nothing a class-registering client meets. The tests must fail on `v0.2.2`'s base
for the right reason (`TypeError` at instantiation) and must not pass for a wrong one (breakages
(c) and (d)).

**Ray is blocked at writing, by someone else's Ray.** A local Ray instance started from SGK's venv
(`extract_GkSource_data.py --ray-address local`, the cluster's session
`/tmp/ray/session_2026-10-11_20-01-57_*`, about 20 processes: `gcs_server`, `raylet`, `ray::`
workers) is up. It belongs to another session's work on a client. The smoke script refuses to
start while `pgrep` finds any Ray process (exit 2), as README §5 rule 7 requires, so **the
orchestrator did not take a smoke run of step I**, and the agent cannot until that instance has
gone. See the addition "The foreign Ray instance" below.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-11 at `93446be` (whose
`datastorekit/` is `6d8ee9a`'s), in `venv/`, in offline scratch venvs at both ends, and in scratch
exports with a prototype of §2.1–§2.4. Pass them on. Corrections 1 and 2 change what the agent
writes, and are STRUCTURALLY REQUIRED. Corrections 3–7 correct what the prompt states; the log
records each as found.

1. **Make no factory instance at import.** §2.3's module must create its instances inside the
   function that returns the registry, and the test module inside its tests, never at module
   level. Otherwise, under breakage (a), the `TypeError` is raised when the module is imported:
   the new test module then fails as one import error, not test by test as §2.4 requires, and the
   smoke script fails at its imports in `main`, before any step, not at step I alone as §2.5
   requires.
2. **The contract's markers: five lines, not four.** §2.6 supersedes §3's first sentence *and* its
   "three defaulted hooks", but the phrase is in §3's **second** sentence, which ends on `:117`
   ("Subclassing it is how a factory gets the three defaulted hooks."). The first sentence ends
   on `:116`. So a marker goes at the end of each of the two sentences (`:116`, `:117`) and at the
   end of the "Kind" cell of each of the three rows (`:123`, `:124`, `:125`). The form is §1 row
   6's (`:69`): `*(superseded in part by §9.5)*`, inside the sentence's full stop where there is
   one (`… is never enforced *(superseded in part by §9.5)*.`), and after the cell's text where
   there is none (`abstract (`:17-20`) *(superseded in part by §9.5)*`). Hazard 5 then reads
   "exactly **five** changed lines", each the old line plus a marker. §9.5's first row says it
   supersedes both sentences.
3. **Breakage (a) fails test 6 too.** Test 6 makes `gauge_setting_factory()`, so under (a) it
   errors with `TypeError` at instantiation, like tests 1, 2 and 5. Measured with the prototype
   (below), the suite at the high end gives `Ran 502 tests … FAILED (failures=2, errors=6)`:
   errors in tests 1, 2, 4 (direct), 4 (through the pool), 5 and 6, each `TypeError: Can't
   instantiate abstract class gauge_setting_factory without an implementation for abstract
   methods 'store', 'validate', 'validate_on_startup'` (6 such lines); failures in test 3 and
   §2.2's assertion; **nothing else in the suite**. Test 4's class half passes under (a) only if it
   runs apart from the instance half (a separate test, or a `subTest` entered before the instance
   is made): it is `v0.2.2`'s behaviour. The prototype built `(cls, cls())` first, so its whole
   test 4 errored. The agent chooses the form, and the log says which.
4. **Breakage (c) fails test 6 too, and test 4's pool half.** With `store` an instance method, an
   instance's `store` is a bound method, which `_defines` reads as "defined": test 6 fails
   (`True is not false : store`). Test 4's direct call on the class raises `TypeError: … missing
   1 required positional argument: 'obj'`, and its pool half errors too, the layer making the same
   call. Measured on the two modules: `FAILED (failures=1, errors=2)`.
5. **Breakage (e) fails test 5 too**, when test 5 builds its registry with §2.3's function, as it
   should: measured, tests 2 and 5 fail.
6. **Where the verification subsections go.** §4.7 ends at `:771`, and `## 5. The pin (U42)` is
   `:772`: §4.8 is inserted between them. §8's table ends at `:1086`, and `## 9. Known gaps` is
   `:1087`: §8.1 is inserted between them. Every other line number the prompt cites holds at
   `93446be`, in the package, the documents, and the extraction campaign's README (U32,
   `:585-597`) and board (U32's row, `:62`).
7. **What test 4's pool half prints.** A failed store or validate prints the actor's traceback
   (through the stand-in) and `_timing.py:21`'s `type=<class 'NotImplementedError'>, value=`,
   with the class registered as with an instance: `v0.2.2`'s output. The test may redirect
   stdout and stderr around the call. Nothing in the layer changes.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **Work in this order:**
  1. the baseline: 494 in `venv/`, and at the high end from a fresh venv with an export of `HEAD`
     installed editable; the port check; `black --check datastorekit docs`, 72 files; the
     clients' `HEAD`s and statuses; Ray's processes, by the script's rule; `RAY_ADDRESS` (unset at
     writing);
  2. §2.1 and §2.2; then the existing suite at the high end, **before** writing the new modules:
     495 (or 494, if §2.2's check is an assertion in an existing test), all `OK`;
  3. §2.3 and §2.4; the suite at both ends;
  4. the breakages (a)–(e), each in its own export at the high end; (a) with the full suite;
  5. §2.5; then the smoke runs, **if no Ray process is up** (below);
  6. the documents (§2.6–§2.8), the records;
  7. `venv/`'s suite again, the port check, `black`, the guards, the clients again, Ray's
     processes again.
- **The foreign Ray instance.** Never stop, kill, signal, connect to, or wait on it in a loop
  longer than a few minutes; never set `RAY_ADDRESS`; never change the smoke script's refusal. At
  step 5, look for Ray processes by the script's rule. If any is up, do steps 6 and 7 that do not
  depend on the smoke run (write §4.8 with its runs left to fill), **do not commit**, and stop:
  report to the orchestrator what is done, what is left (the three smoke runs and their records),
  and the processes found. The orchestrator resumes you once the instance has gone. The commit is
  still one, at the end.
- **Install, do not set `PYTHONPATH`.** 19 subprocess tests fail in an export that is not
  installed. Into each scratch venv: `ray`, `sqlalchemy` and `setuptools` offline, then
  `uv pip install --offline --no-deps --no-build-isolation -e <export>`. High end
  `/opt/local/bin/python3.13`, `ray==2.55.1`, `sqlalchemy==2.0.46`; low end
  `/opt/local/bin/python3.12`, `ray==2.43.0`, `sqlalchemy==2.0.39`. `venv/` is not reinstalled.
  The smoke runs need the export installed too: Ray's workers import `datastorekit.tests.client`
  from it.
- **Import only the function.** If test 6 imports `_defines` from `test_neutral_client`, it imports
  that name alone, never a `TestCase`, so that no test is collected twice.
- **Test 4's pool half** uses a fresh store for each call, as §2.4 says, and checks that the
  `NotImplementedError` reaches the caller's `ray.get` (the stand-in's `resolve`). The prototype
  stored and validated a `gauge_setting` got through the same pool.
- **A parameterised factory's objects are got, not stored.** The pool dispatches a store and a
  validate by the object's class name (`SQL/ShardedPool.py:3455`, `:3548`), and §2.3's one object
  class serves two registry names, neither of which is its class's name. §2.3's factory defines
  neither hook, so nothing reaches this. Do not test it. The log may record it as an observation;
  it is contract §1 row 5's existing fact, and no issue.
- **The `ast` comparison of acceptance 1.** For instance: for each of the five hooks, `ast.dump`
  of its `args` and of its body less a leading docstring, from `git show 6d8ee9a:…` and from the
  tree, compared; and the base's other three hooks unchanged in full. The log gives the script's
  essentials and its result.
- **Neutral names.** Check each new identifier and table name against
  `datastorekit/tests/data/client_vocabulary.json` by a script that loads it, and quote the
  result. The guard does not scan `tests/`, but the campaign's rule (`CLAUDE.md`) applies to the
  whole package.

**The facts, checked by the orchestrator.** Pass them on.

- **The prototype**, in an export of `93446be`: the three `@abstractmethod`s removed (nothing
  moved); `datastorekit/tests/client/instances.py` holding an object class with one integer, a
  factory class whose `__init__(self, column)`, `register(self)` and `build(self, …)` are its only
  methods, and a function returning a copy of the registry with `gauge_setting_factory()` and two
  instances over two new replicated names, and the replicated list with them; seven tests in
  `test_factory_instances.py` (test 4 split into its direct and pool halves), on a pool built with
  `sp_mod.ShardedPool(…)` inside `cluster.active()` (§2.3's first route); and §2.2's change in
  `test_neutral_client.py`, as one new test.
- **The suite.**
  - At `93446be`, `venv/`: `Ran 494 tests … OK`, 0 `ResourceWarning` lines.
  - With the prototype (without §2.2): `Ran 501 tests … OK` at both ends (3.12.15 / 2.43.0 /
    2.0.39 and 3.13.16 / 2.55.1 / 2.0.46, SQLite 3.53.4), installed editable, 0
    `ResourceWarning` lines at each. With §2.2's test, 502.
  - So no existing test depends on the three hooks being abstract, and `_defines` reads an
    instance as its class.
- **The breakages**, in exports at the high end, each against the prototype:

  | | Change | New module | Other |
  |---|---|---|---|
  | (a) | `@abstractmethod` restored on the three | tests 1, 2, 4 (both halves, in the prototype's form), 5, 6 error; test 3 fails | §2.2's test; nothing else in the 502 (correction 3) |
  | (b) | `@abstractmethod` removed from `register` | test 3 fails | §2.2's test |
  | (c) | `store` an instance method, without `@staticmethod` | test 4 (both halves) errors with `TypeError`; test 6 fails | none in `test_neutral_client` |
  | (d) | `validate` returns `None` | test 4 (both halves) fails | none in `test_neutral_client` |
  | (e) | §2.3's two instances on one column name | tests 2 and 5 fail | none in `test_neutral_client` |

  (b)–(e) were run on the two modules only.
- **Not measured: the smoke run.** Ray could not be started (§0). The suite's `cloudpickle` round
  trip passed at both ends; whether a Ray worker unpickles the registry is what step I alone
  shows. If it fails, it is §6's fifth stop.
- **The checks.** `compare_ported_tests.py`: exit 0, "OK: 20 module(s) … 1 test(s) declared not
  ported", at `93446be` and with the prototype. `black --check datastorekit docs`: 72 files at
  `93446be`, 74 with the prototype's two new files.
- **The toolchain.** `venv/`: Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39, SQLite 3.53.4,
  `black` 25.1.0, `datastorekit 0.2.2` editable from this checkout. `uv` 0.12.20.
- **Expected counts.**
  - The suite: **494** before; **494 + n** after, at both ends (n = 8 in the prototype's form:
    seven in the new module and one in `test_neutral_client`).
  - `compare_ported_tests.py`: unchanged.
  - `black --check datastorekit docs`: **72** before, **74** after (or 73 if §2.3's classes live
    in the test module; the prompt recommends a module of their own).
  - The index: **4**, unchanged unless an issue is opened.

**What the review exists to establish.**
- **(E1) Scope.** Only §7's files change; under `datastorekit/`, `SQL/factory_base.py`,
  `tests/test_neutral_client.py`, the new test module and §2.3's module (and `tests/standin_pool.py`
  only on §2.3's second route, with its reason).
- **(E2) The base.** Two abstract hooks, six defaulted, every signature and body `v0.2.2`'s; the
  docstrings true and neutral.
- **(E3) The tests.** Each of §2.4's six, failing under its breakages as correction 3–5 and the
  table say, (a) failing nothing outside the two modules.
- **(E4) Ray.** Step I passes at both ends, fails under (a) with `TypeError` while every other step
  passes, and no Ray process is left by the script.
- **(E5) The documents.** Contract §9.5, its head line and five markers; verification §4.8 and §8.1;
  the note on U32 in two places. Each additive, and true at its tree.
- **(E6) Both ends.** 494 + n in `venv/` and at the high end.

**Conventions.** `actor-names` prompt 01's note's, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- record each breakage as a diff relative to the repository root, and check it **as recorded in
  the log** with `git apply --check` and `-R --check` against a scratch export;
- read a client only through `git`, and never import or run its code;
- use a subdirectory of the session scratchpad, never `/tmp`, for venvs and exports; put no
  scratch `.py` under `datastorekit/` or `docs/`;
- a stop goes to the user, through the orchestrator;
- check `git log` before committing.

And for this prompt:
- **Ray is started only by the smoke script**, from a scratch venv, never while a suite runs, and
  never while another Ray instance is up.
- **No network.** Every venv and install is `--offline`.
- **No push, no tag, and no change to the GitHub repository's settings.** `pyproject.toml` stays
  at `0.2.2`.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. Record `git status --short
   --ignored` (at writing: `.idea/`, `venv/` and five `__pycache__/` directories).
2. **The baseline.** In `venv/`, `Ran 494 tests … OK` with no `ResourceWarning`; the port check
   exits 0; `black --check datastorekit docs` leaves 72 files unchanged; `pip show datastorekit`
   says `0.2.2`.
3. **The clients.** Each `HEAD` and `git status --short` as the gate says.
4. **The remote.** `git ls-remote origin`: `main` at `460b012…` and the four tags as the gate says.
5. **Ray.** Record the Ray processes by the script's rule, and `RAY_ADDRESS` (unset). At writing
   the foreign instance of §0 is up; dispatch does not wait for it.
6. **The index.** 4, and 4 after unless an issue is opened. Tell the agent.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, this board, the extraction README §6.2 (U32) and board,
  `docs/OPEN_ISSUES.md`, `CLAUDE.md`, `docs/client-contract.md`, `docs/extraction-verification.md`,
  `actor-names` prompt 01 and its log;
- `HEAD`, the clients' `HEAD`s and statuses, the counts and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's seven corrections and its additions. Correction 1 is
the one that would make breakage (a) fail for the wrong reason, and correction 2 the one that
would leave a superseded sentence unmarked.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/01-the-base-defaults-three-hooks.md`, in README
  §5.1's form.
- **The files it may change are the prompt's §7 list, and nothing else.** It must not touch
  `pyproject.toml`, `README.md`, `PROVENANCE.md`, `docs/adoption/`, the other scripts of
  `docs/extraction/`, the workflow, `CLAUDE.md`, `LICENSE`, `.gitignore`, or anything under
  `orchestrator/`.
- **Under `docs/` and `prompts/extraction/`, no line is removed**, except the five marked lines of
  the contract and U32's board row, each the old line plus its addition.
- **It writes nothing in any client repository, and runs, imports or opens nothing of one.**
- **It reaches no network**, starts Ray only by the smoke script, never touches the foreign Ray
  instance, and stops uncommitted if that instance is still up at the smoke runs.
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §6 conditions.

## 3. The review — ten checks

Make the review's venvs and exports fresh, offline, in a subdirectory of the scratchpad of their
own, not the agent's.

1. **Scope (E1).** `git show --stat <commit>` touches only §7's files. `git diff <parent> <commit>
   -- pyproject.toml README.md PROVENANCE.md docs/adoption .github` is empty, and so is the diff of
   `docs/extraction/` other than `ray_smoke_run.py`. `git diff -- datastorekit` names four files
   (five on §2.3's second route). No venv, egg-info or scratch file; `git status --short --ignored`
   as at dispatch. Each client's `HEAD` as at dispatch, and its status recorded.
2. **The base, by reading (E2).** Two `@staticmethod @abstractmethod` hooks; the three below the
   comment, each `@staticmethod` with a bare `raise NotImplementedError`; the comment true of six;
   the docstrings say when the layer calls each, as contract §3 does, naming no client. Re-run the
   `ast` comparison against `6d8ee9a`. `SQLAFactoryBase.__abstractmethods__` in `venv/`.
3. **§2.3's module, by reading.** Module-level classes; no instance made at import (correction 1);
   no `inventory_spec`; `register`, `build` and `__init__` only, taking `self`; the registry
   function copies the neutral one and leaves `registry.py` untouched; names neutral.
4. **The tests, by reading (E3).** §2.4's six, each in a `tempfile` directory, with a
   `tearDownModule` asserting Ray is not initialised; test 4's pool half on a fresh store per
   call; test 6 importing only `_defines`, or restating it; §2.2's lists and assertion.
5. **The suite at both ends (E6).** In `venv/`, `Ran <494 + n> tests … OK`. In a fresh high-end
   venv with `git archive <commit>` installed editable, the same, with the `ResourceWarning` lines
   counted. The port check and the guards pass; `black --check datastorekit docs` leaves 74 files.
6. **The breakages (E3).** Extract (a)–(e) from the log; check each with `git apply --check` and
   `-R --check` against its own export of the commit, install it, and run the suite ((a)) or the
   two modules ((b)–(e)). Each fails as the log records, and as §0 predicts up to the agent's
   form; (a) fails nothing outside the two modules.
7. **Ray (E4).** Only when no Ray process is up. In the review's own offline venvs at both ends,
   each with the commit's export installed editable: the smoke script exits 0, every step `PASS`
   with step I among them, its output matching the log's; no Ray process before or after. Then (a)
   at the high end: step I `FAIL` naming `TypeError`, every other step `PASS`, exit 1. If a foreign
   Ray instance is up at the review, say so to the user and take this check when it has gone; the
   review is not recorded as complete without it.
8. **The documents (E5).** Contract: the head line after `:34-35`; §9.5 in §9's form, each row's
   `path:line` read at the commit, its "Supersedes" column naming both sentences and the three
   Kind cells; `git diff --word-diff` shows exactly five changed lines, each the old line plus its
   marker, and nothing else removed. Verification: §4.8 between §4.7 and `## 5`, quoting the runs
   at both ends and the breakage run; §8.1 between §8's table and `## 9`; no line removed.
   Extraction: the italic line after U32's paragraph, and the board row's diff the old row plus
   its note. Every relative link and anchor added resolves.
9. **The records.** The log in §5.1's form with the smoke output, the breakage diffs, the names
   checked, the clients at the start and the end; this board's header and 01's row; the README's
   header and §2 row; `prompts/INDEX.md`; `docs/OPEN_ISSUES.md` at 4, or as an opened issue
   requires.
10. **Nothing left behind.** No Ray process of ours. `git tag -l` is the four tags, and `origin`
    is unchanged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 01* paragraph, in the form of
  `actor-names`' boards. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on both boards, in the log, in the verification subsections and the
    contract if they use the phrase, in the README and in `prompts/INDEX.md`;
  - "reviewed" for 01 in this board's header and row, README §2 and `prompts/INDEX.md`;
  - the notes line, with this note marked "used for 01".
- Anything the review finds that is not residue is opened on this board's §3 and in the index.
- **Report to the user:**
  - what landed: the base, the tests and the hook lists, smoke step I, §9.5 and its markers, the
    verification subsections, the note on U32;
  - the suite at both ends, and the breakages, with (a)'s count;
  - the smoke run at both ends from the review's own venvs, and (a);
  - the index at 4;
  - that 02 (`v0.2.3`) is written next, against the tree 01 leaves;
  - **and ask whether to push `main`** (§5).

## 5. Pushing

As `actor-names`' notes: 01 makes no release and no tag. Its commit and the records after it are on
local `main` only, ahead of `origin/main` (`460b012`). **Ask the user, and wait for a clear yes.**
With approval, `git push origin main`, a fast-forward. Read the CI run once, when the user says it
has finished, and record its URL and both verdict lines on this board in a records commit of its
own, pushed with approval too. If either end fails, record it in §3 and the index, and tell the
user. Nothing is reverted without the user.

**Hand on.** 02 is written after this review, against the tree 01 leaves: it releases `v0.2.3`
(U5), carries the four adoption addenda, and its tag is made only after CI is green on its commit.
