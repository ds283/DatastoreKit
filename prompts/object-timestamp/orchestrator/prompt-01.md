# Orchestrator — prompt 01, the object carries a timestamp

Read [`../README.md`](../README.md) first: §0, §1, §4, §5 (every rule) and §6.2 (U1–U4). Then
read `factory-defaults`' [`prompt-01.md`](../../factory-defaults/orchestrator/prompt-01.md), whose
"Conventions", additions on installing and on breakages, and §3–§5 this note keeps unless it says
otherwise.

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

**The prompt:** [`01-the-object-carries-a-timestamp.md`](../01-the-object-carries-a-timestamp.md)
**Closes:** nothing on a board · **Carries out:** the user's ruling of 2026-10-12 (README §0) ·
**Opens:** only what the work finds · **Model:** Opus, as the prompt recommends (the same agent
writes the code, the contract's §9.6 and the verification subsection).

**Gate:**
- U1–U6 are taken, and 01 is written (`251986b`).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- `git diff --stat 0de2b16 HEAD -- datastorekit pyproject.toml docs` is empty: the package and its
  documents are `v0.2.3`'s.
- `origin/main` is `83068cb` (`git ls-remote origin`, 2026-10-12), an ancestor of `main`, which is
  ahead of it by `251986b` and this note. The tags are `v0.1.0` (`0ece4aa` → `68db557`), `v0.2.0`
  (`9eaf542` → `240028e`), `v0.2.1` (`0ba2e4d` → `33778b0`), `v0.2.2` (`c32d027` → `6d8ee9a`) and
  `v0.2.3` (`8dac562` → `0de2b16`), here and on `origin`, and no other.
- The clients, read while this note was written (each moved under it; see correction 4):
  - SGK `718e650` (branch `handover-remedial`), with a large staged change in its index: `M`, `D`
    and `R` entries moving `Datastore/SQL/ObjectFactories/` to `ObjectFactories/`. Its `HEAD` was
    `f78e8b6`, clean, earlier in the same session, and `ede4062` at planning;
  - CPBH `f5fe207` (branch `dk-and-rpk-migration`), 23 untracked entries (pilot `.db` files, logs,
    `prompts/jordan-normalization/`); `d7791c5` earlier in the session, `0e64ef0` at planning;
  - SI `7bb3efd` (`main`), 2 modified (`.documents/OPEN-ISSUES.md`, `.prompts/INDEX.md`) and 1
    untracked (`.prompts/dk-and-rpk-migration/`), as at planning.
- No Ray process is up by the script's rule, and `RAY_ADDRESS` is unset.
- The index is **4** (all four on `inherited-issues`' board), and stays 4 unless the work opens an
  issue.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**The code change is a dozen lines; the risk is in what must not change.** `object.py` gains a
keyword-only argument, one assignment and a read-only property. Nothing the layer writes or reads
changes, and no message, refusal or exception. The one thing a caller passing `store_id` alone can
see is `"_timestamp": None` in `vars()`, which one existing test pins (U2). The tests must fail on
`v0.2.3`'s object for the right reason, and must not pass for a wrong one (breakages (b) and (c)).

**Unlike `factory-defaults` 01, Ray is free.** No Ray process was up at writing, and the
orchestrator ran the smoke script on a prototype at both ends (below). If another session's Ray is
up when the agent reaches the smoke runs, `factory-defaults`' rule for a foreign instance holds
(its note, "The foreign Ray instance"): never touch it, finish what does not depend on the runs,
do not commit, and stop.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-12 at `251986b` (whose
`datastorekit/` is `0de2b16`'s), in `venv/`, in offline scratch venvs at both ends, and in a scratch
export with a prototype of §2.1–§2.4. Pass them on. Corrections 1 and 2 change what the agent
writes or how it judges a result, and are STRUCTURALLY REQUIRED. Corrections 3–5 correct what the
prompt states; the log records each as found.

1. **Test 4 passes under breakage (a), and that is right.** `v0.2.3`'s `DatastoreObject.__init__`
   takes one positional argument after `self`, so `DatastoreObject(3, t)` raises `TypeError` there
   too, with the same message as under U1's form: `DatastoreObject.__init__() takes 2 positional
   arguments but 3 were given` (both forms checked at Python 3.13). §2.4's last paragraph ("test 4
   should fail because the call succeeds") and §4.4 (a) ("every test of §2.4 fails or errors") are
   wrong for test 4, and **§6's third stop does not apply to it**. Test 4 is breakage (c)'s test,
   and (c) fails it. Do not bend test 4 to fail under (a): no match on a message that does not
   differ, and no keyword call folded into it (test 1 holds that). Measured with the prototype,
   (a) on the full suite at the high end gives `Ran 509 tests … FAILED (failures=2, errors=4)`:
   errors in tests 1, 2, 3 and 5, each `TypeError: DatastoreObject.__init__() got an unexpected
   keyword argument 'timestamp'` (test 2's raised inside the actor and re-raised by the stand-in's
   `ray.get`, from the stamped factory's insert branch, before any read); failures in the two
   subtests of `TestTheVersionObject` (`{'_my_id': 1, '_timestamp': None, …} != {'_my_id': 1, …}`);
   test 4 passes; nothing else fails.
2. **Do not name the stamped column `value`.** `value` is a column name in all three clients'
   vocabulary (`datastorekit/tests/data/client_vocabulary.json`, an exact entry under `columns` for
   SGK, CPBH and SI). §2.3's "the value's column" is a description, not a name: choose a column
   name the vocabulary does not hold (none of `count`, `reading`, `level`, `amount`, `tally` is in
   it, measured; the name is yours). An attribute and payload key called `value` follow
   `instances.scalar_entry`'s precedent (its columns are `left_value` and `right_value`); use it or
   not, and say in the log which and why. The guard does not scan `tests/`, but `CLAUDE.md`'s rule
   applies to the whole package.
3. **Breakage (d) fails test 3 too**, when test 3 checks, as §2.4 says, that `obj.timestamp` is
   unchanged after the refused assignment and deletion (compared with the `t` it was given).
   Measured: tests 1, 2, 3 and 5 fail; test 4 passes.
4. **The clients are moving under other sessions.** SGK's and CPBH's `HEAD`s each moved while this
   note was written (the gate), and SGK has a large staged change. Hazard 8 and §4.6 ask for each
   client's `HEAD` and `git status --short` at the start and the end, "unchanged". Read that as:
   each is recorded at both points, and **a change there that is not the agent's is recorded, not
   stopped on**. What must hold is that no command of the agent wrote, ran, imported or opened
   anything of a client. The log lists the read-only `git` commands it ran against each.
5. **Line numbers.** Every line the prompt cites holds at `251986b`, in the package, the tests and
   the documents, with these readings:
   - `SQL/Datastore.py:764-830`: `_insert` begins at `:760`; the timestamp block is `:809-815`;
   - `docs/extraction-verification.md`: §4.8.3's closing fence is `:1017`, then two blank lines,
     `---` at `:1020`, and `## 5. The pin (U42)` at `:1022`. §4.9 goes after the fence and before
     the blank lines and `---`, as §4.8 follows §4.7.3's fence;
   - `pool._shards` is an `int` when the pool is constructed (`SQL/ShardedPool.py:180`) and is
     replaced by the dict of shard actors when it opens (`:332-333`, `:640-641`), so test 2's
     `pool._shards[k]` is right on an open pool, and wrong on one not yet opened or closed.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **Work in this order:**
  1. the baseline: 504 in `venv/`, and at the high end from a fresh venv with an export of `HEAD`
     installed editable; the port check; `black --check datastorekit docs`, 74 files; the
     clients' `HEAD`s and statuses; Ray's processes, by the script's rule; `RAY_ADDRESS`;
  2. §2.1 and §2.2; then the existing suite at the high end, **before** writing the new modules:
     504, all `OK`;
  3. §2.3 and §2.4; the suite at both ends;
  4. the breakages (a)–(e), each in its own export at the high end; (a) with the full suite;
  5. the smoke runs (§2.5), if no Ray process is up;
  6. the documents (§2.6–§2.7), the records;
  7. `venv/`'s suite again, the port check, `black`, the guards, the clients again, Ray's
     processes again.
- **Install, do not set `PYTHONPATH`, and run from the export's root.** Into each scratch venv:
  `ray`, `sqlalchemy` and `setuptools` offline, then `uv pip install --offline --no-deps
  --no-build-isolation -e <export>`. High end `/opt/local/bin/python3.13`, `ray==2.55.1`,
  `sqlalchemy==2.0.46`; low end `/opt/local/bin/python3.12`, `ray==2.43.0`, `sqlalchemy==2.0.39`.
  `venv/` is not reinstalled. **Run every scratch-venv command with the export as the working
  directory**: run from this checkout, `python -c`/`-m` puts the checkout first on `sys.path`, and
  `datastorekit` is then imported from here, not from the export (seen at writing: an editable
  export reported `datastorekit.__file__` under this checkout until the command was run from the
  export). Print `datastorekit.__file__` once in each venv and record it.
- **Test 2's comparison.** The raw read (`sp.table_columns` / `sp.shard_rows`) returns the
  `timestamp` column as SQLite's text, `YYYY-MM-DD HH:MM:SS.ffffff`; `datetime.fromisoformat` of it
  equals the `datetime` a get answers, at both ends (measured). Either that or `str` of the answer
  will do; the log says which.
- **The stamped object's constructor.** Pass `timestamp` to `super().__init__` by keyword, as the
  prompt says; give the subclass's own `timestamp` parameter a default of `None`, so that the
  factory's insert branch passes nothing.
- **The `ast` comparison of acceptance 1.** For instance: from `git show 0de2b16:datastorekit/object.py`
  and from the tree, `ast.dump` of `store_id` and of `available` (each whole) compared equal;
  `__init__`'s `args` differing by one `kwonlyargs` entry with a `None` default, and its body by
  one `Assign` to `self._timestamp` (less any docstring); the module's other differences an
  `ImportFrom` of `datetime`, the `timestamp` `FunctionDef` decorated `property`, and docstrings.
  The log gives the script's essentials and its result.
- **Neutral names.** Check each new identifier, the table name and the column name against
  `client_vocabulary.json` by a script that loads it (walking each client's `registry`, `columns`
  and `packages`), and quote the result (correction 2).
- **The smoke runs** are taken as `factory-defaults` log 01 §4.3 took them: each from its own fresh
  export of the working tree and fresh offline venv, from the export's root, as `env -u PYTHONPATH
  <venv>/bin/python docs/extraction/ray_smoke_run.py` under `/usr/bin/time -p`, with the Ray
  processes listed by the script's rule before and after.

**The facts, checked by the orchestrator.** Pass them on.

- **The prototype**, in an export of `251986b`: `object.py` as U1 (a keyword-only `timestamp`,
  `self._timestamp`, a read-only property with a one-line docstring, `from datetime import
  datetime`); §2.2's dict; a module `tests/client/stamped.py` with a replicated class subclassing
  `DatastoreObject` (one integer, `timestamp=None` passed on by keyword), a factory class with
  static `register` (`"version": False`, `"timestamp": True`, one integer column) and `build`
  (selecting `serial` and `timestamp` by the integer; `timestamp=row.timestamp` and `_deserialized`
  when found; an insert carrying a payload's `serial`, no timestamp and `_new_insert` when not),
  and a function returning a copy of the registry's factories with the class added and a copy of
  the replicated tables with its name at the end; and `tests/test_object_timestamp.py`, five
  tests, one per item of §2.4, test 2 on one store through a read-write open, a close, a raw read
  of every shard, a read-write reopen with a direct get to each of the three shard actors, and a
  read-only reopen. (Its column was called `value`; correction 2 forbids that.)
- **The suite.**
  - At `251986b`, `venv/`: `Ran 504 tests … OK`, 0 `ResourceWarning` lines (248 s).
  - With the prototype: `Ran 509 tests … OK` at both ends (3.12.15 / 2.43.0 / 2.0.39 and
    3.13.16 / 2.55.1 / 2.0.46, SQLite 3.53.4), installed editable, 0 `ResourceWarning` lines at
    each. `test_object_timestamp`, `test_declared_facts`, `test_layer_is_generic` and
    `test_store_inventory` alone: `Ran 80 tests … OK` at the high end, so the guard passes on
    the prototype's `object.py` and the inventory's count of 12 holds with a module that defines
    no `inventory_spec`.
  - A stamped row's timestamp was one value on all three shards; after a reopen a get answered a
    `datetime` equal to it, as did a get sent to each shard's actor directly, and a read-only
    reopen.
- **The breakages**, in the prototype's export at the high end:

  | | Change | New module | Other |
  |---|---|---|---|
  | (a) | `object.py` as `0de2b16`'s | tests 1, 2, 3, 5 error (`TypeError`, unexpected keyword `timestamp`); **test 4 passes** (correction 1) | `TestTheVersionObject`, 2 subtests fail; nothing else in the 509 |
  | (b) | a setter (and, separately, a setter and a deleter) on the property | test 3 fails | none in `test_declared_facts` |
  | (c) | the `*` removed | test 4 fails | none in `test_declared_facts` |
  | (d) | the property returns `None` | tests 1, 2, 3, 5 fail (correction 3) | none in `test_declared_facts` |
  | (e) | the stamped factory passes `timestamp=datetime.now()` on a read | test 2 fails | none in `test_declared_facts` |

  (b)–(e) were run on the new module and `test_declared_facts` (30 tests).
- **The smoke runs**, on the prototype, script unchanged (SHA-256
  `032036798e101d610a4ac0185ea4eaa7f1db0fe58f52c48ad9f3707548a6a92a`, as verification §4.8 records):
  exit 0 at both ends, steps 1, 2, N, C, 3, 4, 5, 6 and I each `PASS`; step C named
  `builtins.ValueError` at the low end and `ray.exceptions.ActorAlreadyExistsError` at the high
  end; `real` 30.75 s and 65.16 s; no Ray process before or after either run.
- **The checks.** `compare_ported_tests.py`: exit 0, "OK: 20 module(s) … 1 test(s) declared not
  ported", at `251986b`. `black --check datastorekit docs`: 74 files at `251986b`.
- **The toolchain.** `venv/`: Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39, SQLite 3.53.4,
  `black` 25.1.0, `datastorekit 0.2.3` editable from this checkout. `uv` 0.12.20.
- **Expected counts.**
  - The suite: **504** before; **504 + n** after, at both ends (n = 5 in the prototype's form).
  - `compare_ported_tests.py`: unchanged.
  - `black --check datastorekit docs`: **74** before, **76** after (or 75 if §2.3's classes live
    in the test module; the prompt recommends a module of their own).
  - The index: **4**, unchanged unless an issue is opened.

**What the review exists to establish.**
- **(E1) Scope.** Only §7's files change; under `datastorekit/`, `object.py`,
  `tests/test_declared_facts.py` (one line or one dict), the new test module and §2.3's module.
- **(E2) The object.** A keyword-only `timestamp`, `None` by default; a read-only property with no
  setter or deleter; `store_id` and `available` `v0.2.3`'s; the docstring true and neutral.
- **(E3) The tests.** Each of §2.4's five, failing under its breakages as corrections 1 and 3 and
  the table say; (a) failing nothing outside the new module and `TestTheVersionObject`.
- **(E4) Ray.** The unchanged script passes every step at both ends, and no Ray process is left.
- **(E5) The documents.** Contract §9.6 and its head line; verification §4.9. Each additive, and
  true at its tree.
- **(E6) Both ends.** 504 + n in `venv/` and at the high end.

**Conventions.** `factory-defaults` prompt 01's note's, and all bind the agent:
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
  at `0.2.3`.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. Record `git status --short
   --ignored` (at writing: `.idea/`, `venv/` and five `__pycache__/` directories).
2. **The baseline.** In `venv/`, `Ran 504 tests … OK` with no `ResourceWarning`; the port check
   exits 0; `black --check datastorekit docs` leaves 74 files unchanged; `pip show datastorekit`
   says `0.2.3`. (Taken at writing; re-take only if `HEAD` has moved outside `prompts/`.)
3. **The clients.** Each `HEAD` and `git status --short`, recorded (correction 4).
4. **The remote.** `git ls-remote origin`: `main` at `83068cb…` and the five tags as the gate says.
5. **Ray.** Record the Ray processes by the script's rule, and `RAY_ADDRESS` (unset).
6. **The index.** 4, and 4 after unless an issue is opened. Tell the agent.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, this board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `docs/client-contract.md`, `docs/extraction-verification.md`, `factory-defaults` prompt 01 and
  its log;
- `HEAD`, the clients' `HEAD`s and statuses, the counts and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's five corrections and its additions. Correction 1 is the
one that would otherwise send it to a false stop, or tempt it to bend test 4; correction 2 the one
that would put a client's column name into the package.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/01-the-object-carries-a-timestamp.md`, in README
  §5.1's form.
- **The files it may change are the prompt's §7 list, and nothing else.** It must not touch
  `pyproject.toml`, `README.md`, `PROVENANCE.md`, `docs/adoption/`, `docs/extraction/` (the smoke
  script included), the workflow, `CLAUDE.md`, `LICENSE`, `.gitignore`, the neutral client's
  `registry.py`, `objects.py`, `factories.py` or `instances.py`, `standin_pool.py`, or anything
  under `orchestrator/`.
- **Under `docs/`, no line is removed.**
- **It writes nothing in any client repository, and runs, imports or opens nothing of one.**
- **It reaches no network**, starts Ray only by the smoke script, never touches another session's
  Ray instance, and stops uncommitted if one is up at the smoke runs.
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §6 conditions, read with correction 1.

## 3. The review — ten checks

Make the review's venvs and exports fresh, offline, in a subdirectory of the scratchpad of their
own, not the agent's, and run from each export's root.

1. **Scope (E1).** `git show --stat <commit>` touches only §7's files. `git diff <parent> <commit>
   -- pyproject.toml README.md PROVENANCE.md docs/adoption docs/extraction .github` is empty.
   `git diff -- datastorekit` names four files. No venv, egg-info or scratch file; `git status
   --short --ignored` as at dispatch. Each client's `HEAD` and status recorded (correction 4).
2. **The object, by reading (E2).** The signature, the one new assignment, the property with no
   setter or deleter, the import; the docstring says who fills the value and when it is `None`,
   and that the layer neither sets nor reads it, naming no client. Re-run the `ast` comparison
   against `0de2b16`. In `venv/`: `DatastoreObject.timestamp.fset is None` and `.fdel is None`;
   `inspect.signature(DatastoreObject)`'s `timestamp` is `KEYWORD_ONLY` with default `None`.
3. **§2.3's module, by reading.** Module-level classes; a static `register` and `build` only; the
   column not named `value`, every name checked against the vocabulary (correction 2); no
   `inventory_spec`; the registry function copies the neutral one and leaves `registry.py`
   untouched; the subclass passes `timestamp` by keyword.
4. **The tests, by reading (E3).** §2.4's five, each store in a `tempfile` directory, with a
   `tearDownModule` asserting Ray is not initialised; test 2's raw read on every shard, its direct
   gets on every shard actor of an open pool, its read-only reopen, and its comparison with the
   row (not with any `datetime`); test 3's check that the value is unchanged; §2.2's dict, and
   nothing else in `test_declared_facts.py`.
5. **The suite at both ends (E6).** In `venv/`, `Ran <504 + n> tests … OK`. In a fresh high-end
   venv with `git archive <commit>` installed editable, the same, with the `ResourceWarning` lines
   counted. The port check and the guards pass; `black --check datastorekit docs` leaves 76 files
   (or as the agent's form gives, with its reason).
6. **The breakages (E3).** Extract (a)–(e) from the log; check each with `git apply --check` and
   `-R --check` against its own export of the commit, install it, and run the suite ((a)) or the
   new module and `test_declared_facts` ((b)–(e)). Each fails as the log records, and as §0's
   table predicts up to the agent's form; (a) fails nothing outside the new module and
   `TestTheVersionObject`, and test 4 passes under it.
7. **Ray (E4).** Only when no Ray process is up. In the review's own offline venvs at both ends,
   each with the commit's export installed editable: the smoke script exits 0, every step `PASS`,
   its output matching the log's and §4.9's; no Ray process before or after. If a foreign Ray
   instance is up at the review, say so to the user and take this check when it has gone; the
   review is not recorded as complete without it.
8. **The documents (E5).** Contract: the head line after `:37-38`; §9.6 in §9's form, its
   `path:line` citations read at the commit, its "Supersedes" none with the reason; `git diff` of
   the file `+` lines only. Verification: §4.9 between §4.8.3's fence and `## 5`, quoting the runs
   at both ends with the script's SHA-256; `+` lines only. Every relative link and anchor added
   resolves.
9. **The records.** The log in §5.1's form with the smoke output, the breakage diffs, the names
   checked, the clients at the start and the end; this board's header and 01's row; the README's
   header and §2 row; `prompts/INDEX.md`; `docs/OPEN_ISSUES.md` at 4, or as an opened issue
   requires.
10. **Nothing left behind.** No Ray process of ours. `git tag -l` is the five tags, and `origin`
    is unchanged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 01* paragraph, in the form of
  `factory-defaults`' board. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log, in the verification subsection and the
    contract if they use the phrase, in the README and in `prompts/INDEX.md`;
  - "reviewed" for 01 in this board's header and row, README §2 and `prompts/INDEX.md`;
  - the notes line, with this note marked "used for 01".
- Anything the review finds that is not residue is opened on this board's §3 and in the index.
- **Report to the user:**
  - what landed: the object's keyword-only, read-only `timestamp`, the one dict, the stamped class
    and its tests, §9.6, verification §4.9;
  - the suite at both ends, and the breakages, with (a)'s count and test 4's pass under it;
  - the smoke run at both ends from the review's own venvs;
  - the index at 4;
  - that 02 (`v0.3.0`) is written next, against the tree 01 leaves;
  - **and ask whether to push `main`** (§5).

## 5. Pushing

As `factory-defaults`' notes: 01 makes no release and no tag. Its commit and the records after it
are on local `main` only, ahead of `origin/main` (`83068cb`). **Ask the user, and wait for a clear
yes.** With approval, `git push origin main`, a fast-forward. Read the CI run once, when the user
says it has finished, and record its URL and both verdict lines on this board in a records commit
of its own, pushed with approval too. If either end fails, record it in §3 and the index, and tell
the user. Nothing is reverted without the user.

**Hand on.** 02 is written after this review, against the tree 01 leaves: it releases `v0.3.0`
(U6), carries the adoption addenda, and its tag is made only after CI is green on its commit.
