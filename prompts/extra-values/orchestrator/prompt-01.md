# Orchestrator — prompt 01, a spec counts more than one value table

Read [`../README.md`](../README.md) first: §0 (with §0.1 and §0.2), §1, §4, §5 (every rule) and
§6.2 (U1–U5). Then read `fingerprint`'s [`prompt-01.md`](../../fingerprint/orchestrator/prompt-01.md),
whose "Conventions", additions on installing and on breakages, and §3–§5 this note keeps unless it
says otherwise. **Like that note's prompt, this one starts no Ray** (README §5 rule 7): there is no
smoke run, and nothing of the smoke script's rule applies but its check that no Ray process is up.
**Unlike it, no client code is run at all**: there is no extract and no equivalence check.

**You do not write code.** You may:
- run the suite, the port check, `black --check` and the guards;
- make venvs in the session scratchpad with `uv … --offline`, from the cache the extraction
  campaign filled (README §0.1 says how the high end resolves);
- export the tree with `git archive` into the scratchpad, and run prototypes, reproductions and
  breakages there, never in this checkout and never committing one;
- reach the network only for one `git ls-remote origin` at dispatch and one at the review;
- read the three clients only through `git -C <client> rev-parse|status|show|grep|log|diff`;
- fix small residue in a follow-up commit of your own (§4);
- after the review, and only with the user's approval, push `main` (§5).

**The prompt:** [`01-a-spec-counts-more-than-one-value-table.md`](../01-a-spec-counts-more-than-one-value-table.md)
**Closes:** nothing on a board · **Carries out:** the user's request of 2026-10-21 and the ruling U2
(README §0) · **Opens:** only what the work finds · **Model:** Opus, as the prompt recommends (the
risk is in what must not change, and the witness and golden must be reproduced to the byte).

**Gate:**
- U1–U5 are taken and U2 is the user's ruling; 01 is written (`d401e84`).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- `git diff --stat c8570e8 HEAD -- datastorekit pyproject.toml docs` is empty: the package and its
  documents are `v0.4.0`'s.
- `origin/main` is `38ebb9f` (`git ls-remote origin`, 2026-10-21), an ancestor of `main`, which is
  ahead of it by `d401e84` and this note. The tags are `v0.1.0` (`0ece4aa` → `68db557`), `v0.2.0`
  (`9eaf542` → `240028e`), `v0.2.1` (`0ba2e4d` → `33778b0`), `v0.2.2` (`c32d027` → `6d8ee9a`),
  `v0.2.3` (`8dac562` → `0de2b16`), `v0.3.0` (`bf0a3b2` → `2f5417e`) and `v0.4.0` (`8e7c1d7` →
  `c8570e8`), here and on `origin`, and no other.
- The clients, read while this note was written (2026-10-21), each clean and as at planning:
  SGK `031bcb4` (branch `handover-remedial`), CPBH `7055532` (branch `jordan-normalization`), SI
  `f5f395b` (branch `dk-and-rpk-migration`).
- No Ray process is up by the smoke script's rule (`pgrep -f
  'gcs_server|raylet|ray::|default_worker\.py'`), and `RAY_ADDRESS` is unset.
- The index is **4** (all four on `inherited-issues`' board), and stays 4 unless the work opens an
  issue.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**The code is about forty lines; the risk is in what must not change.** Every record of a class
that declares no extra table must be today's, byte for byte, so that no fingerprint a client holds
moves at `ENCODING_FORMAT` 1. Test 1, against the format-1 golden read through a spec that does not
declare the field, is the proof; the golden at format 2 is not.

**Two files are reproductions, not outputs.** The witness and the format-2 golden must be the
planner's to the byte (prompt §1.1). The orchestrator reproduced both independently (below), so a
difference means the agent's §2.3 departs from the prompt, and is a stop, not a new file.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-21 at `d401e84` (whose
`datastorekit/` is `c8570e8`'s), in `venv/`, in an offline scratch venv at the high end, and in a
scratch export with a prototype of §2.1–§2.6 written from the prompt alone. Pass them on.
Corrections 1 and 2 change what the agent writes or how it judges a result, and are STRUCTURALLY
REQUIRED. Corrections 3–5 correct what the prompt states; the log records each as found.

1. **`fill_required` knows only the neutral schema.** It reads `_schema_tables()`, built from the
   neutral registry (`real_store_fixtures.py:654-658`, `:676-694`), so a row set holding
   `TraceNote` or `GadgetNote` raises `KeyError` there. §2.6's "`fill_required` of `full_rows()`'s
   rows plus the rows a test adds" must be read as: `fill_required` of `full_rows()`'s rows, **then**
   the test's `TraceNote` / `GadgetNote` rows added, each stating every non-null column. And
   `build_real_store` must be given `full_rows()`'s **shard keys** too: its default is
   `SHARD_KEYS`, not the full store's (`:294`). `build_full_store` and `fill_required` stay
   unchanged, as §2.3 item 6 says. The prototype's store of `wider()` built this way gave every
   count tests 3–5 expect, and no problem but the one each test makes.
2. **Breakages fail more than §4.4 names; that is right.** Measured on the prototype at the high
   end, running the new module, `test_store_inventory`, `test_store_fingerprint` and
   `test_neutral_client` (91 tests):

   | | §4.4 predicts | Fails (prototype) |
   |---|---|---|
   | (a) emit always | 1, 2, JSON-safe, golden | 1; 2 (subtests of every class but Trace); JSON-safe (the same); the golden |
   | (b) no zeros | 2, 3 | 2, 3; JSON-safe (`Trace`, whose records with no mark lose the key); the golden |
   | (c) extra orphans unreported | 4 | 4 (an error: its one-problem unpacking) |
   | (d) counted from `values` | 2, 3 | 2, 3, 4, 5 (errors), 6; the two existing orphan-value tests (the `values` orphans reported twice); the golden |
   | (e) `keywords()` omits it | 2, 3, 6 | 2, 3, 4 and 5 (errors), 6; JSON-safe (`Trace`); the golden |
   | (f) never emit | 5, 6, golden | 5 (an error), 6; JSON-safe (`Trace`); the golden |
   | (g) refusal removed | 7 | 7 |
   | (h) refusal in `__post_init__` | 7 | 7 (an error: the spec is refused where the test builds it) |
   | (i) counted in Python | counted-never-listed | `test_value_tables_are_only_counted` |

   Every named test fails under its breakage, and nothing passes that §4.4 says fails. The extra
   failures follow from the change, and **are not §6's fourth stop**. The log records what failed
   for each, in the agent's form, beside §4.4's prediction. (c)'s, (d)'s, (e)'s, (f)'s and (h)'s
   errors are failures of the test, not of the harness; a test written to fail, not error, is
   equally right.
3. **The brief is read through `git`.** §"Read first" item 3 gives SI's working-tree path. Read it
   with `git -C /Users/ds283/Documents/Code/StochasticInstantons show
   f5f395b:.prompts/dk-and-rpk-migration/datastorekit-second-value-table-brief.md` (211 lines; SI
   is clean at `f5f395b`), under README §5 rule 5 and the conventions below.
4. **`ResourceWarning` at the high end.** The prototype gave 0 lines in `venv/` and **2** at the
   high end (one warning: an unclosed `sqlite3.Connection` reported from SQLAlchemy's
   `event/base.py`). The planner's 4 is two such warnings. Read §4.1's "0 or 4 is timing" as **0, 2
   or 4**: each line pair is one warning of that kind. Any other kind, or more, is explained test by
   test.
5. **Line numbers.** Every line the prompt cites holds at `d401e84`, with these readings:
   - `store_inventory.py`'s module docstring is `:1-84` (the imports and `_EXAMPLES` follow, to
     `:113`); `Record`'s decorator is `:177`, the class `:178`; `InventorySpec`'s decorator `:292`;
     the value counting's comment `:640`, its block `:641-663`;
   - `store_fingerprint.py`: the comment is `:38-64`, `ENCODING_FORMAT = 1` is `:65`; §2.2's
     paragraph goes after `:64`;
   - `test_neutral_client.py`'s `test_every_declaration_field_is_in_use` is `:310`;
     `test_store_inventory.py`'s counted-never-listed test is `test_value_tables_are_only_counted`,
     `:617`; `NEUTRAL_FORMAT` is `test_store_fingerprint.py:57`;
   - the contract's §9.7 head line is `:43-44`, and §9.7 runs `:372-386`, the file's end. Its
     `ENCODING_FORMAT` row cites `(:65)` for the constant: that is right.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **Work in this order:**
  1. the baseline: 530 in `venv/`, and at the high end from a fresh venv with an export of `HEAD`
     installed editable; the port check; `black --check datastorekit docs`, 78 files; the
     clients' `HEAD`s and statuses; Ray's processes; `RAY_ADDRESS`;
  2. §2.1 and §2.2; then §2.3; then the witness (§2.4) and the golden (§2.5) **before** any test is
     amended, each checked against the planner's hashes at once;
  3. §2.6; the suite at both ends;
  4. the breakages (a)–(i), each in its own export at the high end, on the four modules named in
     correction 2;
  5. §2.7 and the records;
  6. `venv/`'s suite again, the port check, `black`, the guards, the clients again, Ray's
     processes again.
- **The high-end venv.** As README §0.1: `uv … --offline` of `ray==2.55.1` alone fails (a
  dependency's version not in the cache: `filelock` at writing). Write a constraints file pinning
  each package to the highest version under `~/.cache/uv/archive-v0/*/*.dist-info`, and install
  `ray==2.55.1 sqlalchemy==2.0.46 setuptools` with `-c` it, into a venv of
  `/opt/local/bin/python3.13`; then `uv pip install --offline --no-deps --no-build-isolation -e
  <export>`. Run every scratch-venv command from the export's root under `env -u PYTHONPATH`, and
  print `datastorekit.__file__` once. `venv/` is not reinstalled; the witness is captured there
  (§2.4), from this checkout's root.
- **The golden at both ends.** Write it once, from `venv/`, with the script the log keeps; run the
  same script at the high end and compare the digest and the file's SHA-256.
- **Test 7 builds the bad registry so that the refusal is visible.** Under (h) the spec's
  construction raises; the test fails either where the spec is built or in `inventory_specs`.
  Either is right. Match the message on both names (`assertRaisesRegex`), as §2.6 says.
- **Neutral names.** Check each new identifier and table and column name against
  `datastorekit/tests/data/client_vocabulary.json` by a script that loads it, and quote the
  result. The orchestrator's check found none of `TraceMark`, `TraceNote`, `GadgetNote`,
  `mark_index`, `marks`, `TRACE_MARKS`, `EXTRA_VALUE_CLASSES`, `extra_values`,
  `extra_value_counts` in it.

**The facts, checked by the orchestrator.** Pass them on.

- **The prototype**, in an export of `d401e84`, written from the prompt alone: §2.1 (the inner
  function `count_values(table, column)` returning the counts and appending the problem; `values`
  counted through it, then each extra table in sorted order; `extra_value_counts` built per
  declared table with `.get(serial, 0)`; the refusal after the polymorphic-parent check, before
  `depends[name]`); §2.2's paragraph; §2.3 to the letter (`TraceMark_factory` between
  `TraceStep_factory` and `Trace_factory`, its rows written after the steps; `Trace.marks`;
  `TRACE_MARKS`; the registry and drop group; the fixture rows; `factories` on `build_real_store`
  and `_write_shard`); §2.6's literals; an eight-test module. Its diff under `datastorekit/` other
  than the new files: 10 files, +116 −15 after `black`.
- **The reproductions.**
  - The witness, captured in `venv/` from the export: SHA-256
    `971ec253ce78d5f0f7cfeccf13dd0a3b94fc3f5bc9a57b2eadee7b7f2c07d196`, the planner's; its diff
    from `schema_at_extraction-06.json` 117 lines, every one an addition.
  - The golden at `fingerprint_format=2`: digest
    `524cefd41ab593f73abe0610558d8444c64f9514c4d1edb5041591737161d14a` and file SHA-256
    `848fe4c90bd622bafda061d6e59cf780308b8a7cb6044203f18da2fa43ba9fb8` at both ends, the
    planner's.
  - Test 1: the format-1 golden reproduced, every field but `taken`, through `undeclared()`.
- **The suite.**
  - At `d401e84`, `venv/`: `Ran 530 tests … OK`, 0 `ResourceWarning` lines (101 s).
  - With the prototype: `Ran 538 tests … OK` at both ends (3.12.15 / 2.43.0 / 2.0.39 in `venv/`;
    3.13.16 / 2.55.1 / 2.0.46 in the scratch venv; SQLite 3.53.4), `ResourceWarning` lines 0 and 2
    (correction 4).
- **The breakages**: correction 2's table.
- **The checks.** `compare_ported_tests.py`: exit 0, "OK: 20 module(s) … 1 test(s) declared not
  ported", at `d401e84` and with the prototype. `black --check datastorekit docs`: 78 files at
  `d401e84`, 79 with the prototype.
- **The toolchain.** `venv/`: Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39, SQLite 3.53.4,
  `black` 25.1.0, `datastorekit 0.4.0` editable from this checkout. `uv` 0.12.20.
- **Expected counts.**
  - The suite: **530** before; **538** after, at both ends.
  - `compare_ported_tests.py`: unchanged.
  - `black --check datastorekit docs`: **78** before, **79** after.
  - The index: **4**, unchanged unless an issue is opened.

**What the review exists to establish.**
- **(E1) Scope.** Only §7's files change; under `datastorekit/`, three new files (the witness, the
  golden, the test module) and the ten §7 names, and no other file.
- **(E2) Compatibility.** A record of a class that declares no extra table is today's: `as_json`'s
  fifth key only when not empty; test 1 against the format-1 golden; `ENCODING_FORMAT` 1.
- **(E3) The reproductions.** The witness and the golden are the planner's, to the byte.
- **(E4) The tests.** U4's eight, each failing under its breakages as correction 2 says.
- **(E5) The documents.** The `ENCODING_FORMAT` paragraph in §2.2's words; contract §9.8 and its
  head line, additive, each citation true at the commit.
- **(E6) Both ends.** 538 in `venv/` and at the high end.

**Conventions.** `fingerprint` prompt 01's note's, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- record each breakage as a diff relative to the repository root, and check it **as recorded in
  the log** with `git apply --check` and `-R --check` against a scratch export;
- read a client only through `git`, and never import, run or open its code or stores;
- use a subdirectory of the session scratchpad, never `/tmp`, for venvs, exports and scripts;
  put no scratch `.py` under `datastorekit/` or `docs/`;
- a stop goes to the user, through the orchestrator;
- check `git log` before committing.

And for this prompt:
- **Ray is not started**, by anything.
- **No network.** Every venv and install is `--offline`.
- **No push, no tag, and no change to the GitHub repository's settings.** `pyproject.toml` stays
  at `0.4.0`.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. Record `git status --short
   --ignored` (at writing: `.idea/`, `venv/` and five `__pycache__/` directories).
2. **The baseline.** In `venv/`, `Ran 530 tests … OK` with no `ResourceWarning`; the port check
   exits 0; `black --check datastorekit docs` leaves 78 files unchanged; `pip show datastorekit`
   says `0.4.0`. (Taken at writing; re-take only if `HEAD` has moved outside `prompts/`.)
3. **The clients.** Each `HEAD` and `git status --short`, recorded. A change there that is not the
   agent's is recorded, not stopped on.
4. **The remote.** `git ls-remote origin`: `main` at `38ebb9f…` and the seven tags as the gate
   says.
5. **Ray.** Record the Ray processes by the script's rule, and `RAY_ADDRESS` (unset).
6. **The index.** 4, and 4 after unless an issue is opened. Tell the agent.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, this board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `docs/client-contract.md`, `fingerprint` prompt 01's log;
- `HEAD`, the clients' `HEAD`s and statuses, the counts and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's five corrections and its additions. Correction 1 is the
one that would otherwise stop it at a `KeyError` in the fixtures, or tempt it to change
`fill_required`; correction 2 the one that would send it to a false stop on the breakages.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/01-a-spec-counts-more-than-one-value-table.md`, in
  README §5.1's form.
- **The files it may change are the prompt's §7 list, and nothing else.** It must not touch the
  pool, `store_reader.py`, `SQL/schema.py`, `pyproject.toml`, `README.md`, `PROVENANCE.md`,
  `docs/adoption/`, `docs/extraction/`, `docs/extraction-verification.md`, the workflow,
  `CLAUDE.md`, `LICENSE`, `.gitignore`, `schema_at_extraction-06.json`,
  `store_fingerprint-neutral-1-encoding-1.json`, or anything under `orchestrator/`.
- **Under `docs/`, no line is removed.**
- **It writes nothing in any client repository, and runs, imports or opens nothing of one.**
- **It reaches no network and starts no Ray.**
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §6 conditions, read with corrections 1 and 2.

## 3. The review — ten checks

Make the review's venvs and exports fresh, offline, in a subdirectory of the scratchpad of their
own, not the agent's, and run from each export's root.

1. **Scope (E1).** `git show --stat <commit>` touches only §7's files. `git diff <parent> <commit>
   -- pyproject.toml README.md PROVENANCE.md docs/adoption docs/extraction
   docs/extraction-verification.md .github datastorekit/SQL datastorekit/store_reader.py
   datastorekit/tests/data/schema_at_extraction-06.json
   datastorekit/tests/data/store_fingerprint-neutral-1-encoding-1.json` is empty. `git diff
   --name-status <parent> <commit> -- datastorekit` is three `A` lines and ten `M`. No venv,
   egg-info or scratch file; `git status --short --ignored` as at dispatch. Each client's `HEAD`
   and status recorded.
2. **The change, by reading (E2).** `Record` and `InventorySpec`'s new fields last and defaulted
   by `default_factory`; `as_json`'s fifth key only when not empty; `canonical_json`, `identity`,
   `__hash__` and `dependencies()` unchanged; one inner function serving `values` and each extra
   table, sorted, the `orphan-value` text today's; the refusal in `inventory_classes` only, with
   §2.1 item 4's message and in its docstring; no refusal at construction. `git diff` of
   `store_fingerprint.py` is the paragraph alone, in §2.2's words. The module docstring as §2.1
   item 5, naming no client.
3. **The neutral client, by reading.** §2.3 to the letter; compare the agent's diff of the five
   client and fixture files with the orchestrator's prototype (scratch `orch/proto`, if it is still
   there; otherwise by reading against §2.3).
4. **The reproductions (E3).** Capture the witness in `venv/` from the commit's export and compare
   bytes with the committed file; run the log's golden script at both ends on the commit's export
   and compare bytes; both hashes the planner's. The witness diff in the log is additions only.
5. **The tests, by reading (E4).** U4's eight, each store in a `tempfile` directory; correction 1
   applied without changing `fill_required`; test 1 reading `FORMAT_1_GOLDEN` by a name built from
   `ENCODING_FORMAT`; test 7 matching both names; the amended literals as §2.6, with no assertion
   call added or removed in `test_store_inventory` (the port check); no `Test*` class imported from
   another module; the prose neutral.
6. **The suite at both ends (E6).** In `venv/`, `Ran 538 tests … OK`. In a fresh high-end venv
   with `git archive <commit>` installed editable, the same, with the `ResourceWarning` lines
   counted (correction 4). The port check and the guards pass; `black --check datastorekit docs`
   leaves 79 files.
7. **The breakages (E4).** Extract (a)–(i) from the log; check each with `git apply --check` and
   `-R --check` against its own export of the commit, and run the four modules. Each fails as the
   log records, and at least as correction 2's table says for the named tests; (a) fails test 1.
8. **The documents (E5).** Contract: the head line after §9.7's; §9.8 in §9's form, after §9.7,
   its rows as §2.7, its `path:line` citations read at the commit, its "Supersedes" entries as
   §2.7; the `ENCODING_FORMAT` row in §2.2's words; `git diff` of the file `+` lines only. Every
   relative link and anchor added resolves.
9. **The records.** The log in §5.1's form with the witness diff, the golden's script, the
   breakage diffs, the names checked, the clients at the start and the end; this board's header
   and 01's row; the README's header and §2 row; `prompts/INDEX.md`; `docs/OPEN_ISSUES.md` at 4,
   or as an opened issue requires.
10. **Nothing left behind.** No Ray process. `git tag -l` is the seven tags, and `origin` is
    unchanged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 01* paragraph, in the form of
  `fingerprint`'s board. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log, in the contract if it uses the phrase, in
    the README and in `prompts/INDEX.md`;
  - "reviewed" for 01 in this board's header and row, README §2 and `prompts/INDEX.md`;
  - the notes line, with this note marked "used for 01".
- Anything the review finds that is not residue is opened on this board's §3 and in the index.
- **Report to the user:**
  - what landed: `extra_values`, `extra_value_counts`, the refusal, the `ENCODING_FORMAT`
    paragraph, the neutral client's `TraceMark`, the witness and the format-2 golden, the tests,
    contract §9.8;
  - the reproductions and test 1 replayed, and the suite at both ends, and the breakages;
  - the index at 4;
  - that 02 (`v0.5.0`) is written next, against the tree 01 leaves;
  - **and ask whether to push `main`** (§5).

## 5. Pushing

As `fingerprint`'s notes: 01 makes no release and no tag. Its commit and the records after it are
on local `main` only, ahead of `origin/main` (`38ebb9f`). **Ask the user, and wait for a clear
yes.** With approval, `git push origin main`, a fast-forward. Read the CI run once, when the user
says it has finished, and record its URL and both verdict lines on this board in a records commit
of its own, pushed with approval too. If either end fails, record it in §3 and the index, and tell
the user. Nothing is reverted without the user.

**Hand on.** 02 is written after this review, against the tree 01 leaves: it releases `v0.5.0`
(U5), carries the adoption addenda (SI's saying what it does; ChamPBH's and SGK's that nothing
changes), and its tag is made only after CI is green on its commit. The tag object, the commit and
the SI addendum's anchor then go to the user for SI's pin prompt.
