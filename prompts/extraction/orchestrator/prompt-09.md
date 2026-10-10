# Orchestrator — prompt 09, rewrite the package prose

Read [`../README.md`](../README.md) first: §1, §2 (rows 09–11), §4, §5 (rules 4, 6, 7, 9 and 10)
and §6.2 (U17, U33–U40). Then read [`prompt-08b.md`](prompt-08b.md) §0's "Conventions", which this
note keeps unless it says otherwise, and the board's review of 08b.

**You do not write code.** You may:
- run the suite, the port check, `black --check`, the layer guard and the new module;
- make venvs in the session scratchpad with `uv pip install --offline`, from the cache 05's work
  filled, and nothing else: **no download** (the prompt's §4.2);
- export the tree with `git archive` into the scratchpad, and run probes, measurements and
  breakages there, never in this checkout and never committing one;
- read the three clients only through `git -C <client> rev-parse|status|log`; 09 reads nothing
  else of them (the prompt's §4.7);
- fix small residue in a follow-up commit of your own (§4).

You push nothing and make no tag: 09 makes no release (10 does, U36).

**The prompt:** [`09-rewrite-the-package-prose.md`](../09-rewrite-the-package-prose.md)
**Closes:** `[01-package-prose-names-sgks-layout]` · **Narrows:** nothing · **Changes:** nothing ·
**Opens:** only what the work finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- 08b landed (`efedc8d`) and was reviewed (`452b3c9`). 09 is written (`21334c2`).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- Nothing under `datastorekit/` has changed from `efedc8d` to `21334c2` (only `prompts/` and
  `docs/OPEN_ISSUES.md` have), so the prompt's line numbers "at `452b3c9`" are the tree's.
- `origin/main` is `102f225`, an ancestor of local `main`; `origin` holds `v0.1.0` (peeling to
  `68db557`) and `v0.2.0` (`240028e`) only.
- The clients' `HEAD`s: SGK `b510bc9` (branch `handover-remedial`), CPBH `52142d7` (`main`), SI
  `7bb3efd` (`main`).
- One prompt at a time in this checkout. 10 is not written.

## 0. What makes this prompt unusual

**No line of code changes, so the suite cannot catch a bad rewrite.** It passes whatever the prose
says. Three things stand in for it: §4.3's AST check (only prose changed), the new module (no
comment or docstring matches tier A's rules), and reading (every other citation, and whether each
rewritten sentence is still true). The review is therefore mostly reading. It reads every hunk of
the diff, not a sample.

**The appendix is a reading, and it is not complete.** The orchestrator's sweep found further lines
that cite the source (correction 3). Rule 8 already puts such lines in scope. The agent's own last
pass (§4.4) will find more; each is recorded, not argued away.

**The diff is wide.** 43 files under `datastorekit/`: the appendix's 42, every one of correction
3's lines among them, and the new module. Add any file the agent's own pass finds, and the
records. Every file is staged by explicit path.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-10 at `21334c2`, in `venv/`,
in an offline high-end venv, and in scratch exports. Pass them on. Correction 1 changes what the
agent writes, and is STRUCTURALLY REQUIRED. The rest correct or complete what the prompt states;
the log records each as found.

1. **The module rule needs a trailing boundary.** As §2.4's table words it, `Datastore.` followed by
   `object` also matches `Datastore.object_get`, a method of this package's own class. Without the
   boundary the four rules give **186 lines in 43 files**, not 181 in 42. The five extra lines are
   true here and must not be rewritten:
   - `SQL/Datastore.py:590`;
   - `contract.py:16`, `:37` and `:44`;
   - `tests/test_version_keyed_lookups.py:6`.

   There is no allow list, so test 1 could not pass. The rule takes the module name as a whole
   word: `(?<![\w.])Datastore\.(SQL|tests|…|store_inventory)(?!\w)`. This is log 03a §8's `\b`.
   With it, the four rules give exactly **181 in 42**, line for line the appendix's tier A.
2. **Tier B is 9 lines and tier C is 58.** The prompt's table says 10 and 57; the total of 248
   stands.
   - The appendix stars 58 lines.
   - Its unstarred lines are tier A's 181 and nine SHA lines:
     - `test_absolute_shard_record_refused.py:7`, `:26` and `:123`;
     - `test_reconcile_at_open.py:746` and `:912`;
     - `test_shard_key_audit_refusals.py:6`, `:11`, `:134` and `:178`.
   - By path, the 248 are 96 lines in 12 files of the layer and 152 in 30 files under `tests/`.
     The prompt's 97 in 13 counts the guard's `:71` with the layer.
   - Every one of the 248 is a comment or docstring line (checked by `tokenize` and `ast`).
3. **Lines the appendix misses.** The orchestrator's sweep is not exhaustive. Each line below is a
   further line under rule 8: the agent reads it, decides it, and records the decision. Numbers
   are at `452b3c9`.
   - **The source's issues.** None of these is on this repository's board or in its index. The
     index's inherited `[00-…]` issues are cited nowhere in the package.
     - `test_closed_store_refusals.py:4`: `[04-closed-store-refusals-repeat-their-prefix]`.
     - `test_foreign_key_check.py:9`: `[00-quadsource-tq-serial-has-the-wrong-foreign-key]`. It
       also names a client's table, lower-cased (`QuadSource` is in the guard's vocabulary). The
       guard does not scan tests, so nothing catches it. Log 04a §7 item 4 listed it.
     - `test_schema_builder.py:22`: `[00-build-schema-reads-registration-before-its-none-check]`.
   - **The source's logs and audits, by path.** `logs/` is not a rule's prefix, so test 1 will
     not find these. Record that in "Observations not acted on"; do not add a rule.
     - `test_delete_store.py:13`: `logs/01-delete-a-closed-store.md`.
     - `test_copy_move_store.py:10`: `logs/02-copy-and-move-a-store.md`.
   - **The source's labels, used as pointers into its records.**
     - `test_read_only_pool.py:19` (R2 Run 1), `:64` (O2; rule 1 names O1–O2), `:239` (A2) and
       `:274` (R2).
     - `store_inventory.py:49` and `:123`, and `test_store_inventory.py:394`: "decision D1". This
       is the source's D1. This campaign's D1 is "extract the layer".
     - `test_store_inventory.py:617`: F7.
     - `test_store_schema.py:18`: "U1:". This is the source's U1. This campaign's U1 is the
       repository's name.
     - `test_schema_builder.py:10` and `schema_description.py:13`: "§6.2 D5". Each continues an
       appendix line.
     - `test_copy_move_store.py:44` and `:211`: "prompt §2 P6", "every refusal of P6".
     - `test_shardedpool_shard_paths.py`:
       - `:13`: "prompt 01's P0";
       - `:26`: "prompt §6 item 2";
       - `:68`: "prompt §6 item 3";
       - `:90`: "Prompt §5";
       - `:140`: "the §4 demonstration";
       - `:183`: "The P0 case".
     - `test_delete_store.py:193` and `:536`: R1.
     - `test_drop_refuses_dangling_references.py:43`: "its README §0.2's table".
     - `shard_store_fixtures.py:93`: "the sweep script's check", a tool this package does not
       have.
   - **The source's history, with no record cited.** These say what happened in the source; they
     cite no file of it. Rule 3 decides them, and the log records each decision.
     - `shard_paths.py:22`;
     - `test_delete_store.py:8`;
     - `test_shardedpool_shard_paths.py:9-10` and `:104`.

     They mention "the A3 baseline store", 2026-09-23 and "the atol sweep".

   **How a label is decided:**
   - **A label the module's code uses is its own vocabulary, and stays.** This covers a runtime
     string, a dict key or a version label:
     - `P1-C`, `C-P3` and `Rn-P3` in `test_reconcile_at_open`;
     - `C5` and `M4` in `test_copy_move_store`;
     - `L1` and `L2` in `test_version_row_at_open`.

     Prose naming such a label stays. It loses only the pointer to where the label was defined.
   - **A label that only points into the source's records goes.** Its explanation stays.
   - **A label that collides with this campaign's own** (U1, D1, D5, "README §6.2") is decided by
     provenance and context:
     - In a module imported at 01, `git blame` naming `8bc60a5` on an unchanged line means the
       line is the source's.
     - In a ported module, a label beside a source campaign's name is the source's.
     - A line this campaign wrote says "extraction prompt NN" or cites a U-number this campaign
       took for that file.

     If a line still cannot be decided, that is the prompt's §6 stop.
4. **Two more sentences go false with §2.3.** Both are corrected under §2.2's last line, and
   recorded.
   - The guard's banner at `test_layer_is_generic.py:189` ("the hits the layer's frozen prose
     holds") is false once `KNOWN_HITS` is empty.
   - The docstring's "The layer's prose is frozen until after prompt 05" (`:31`) is false too. It
     is in §2.3's paragraph already.

   Neither is an AST change: the banner is a comment, and `:31` is docstring.
5. **The existence check needs the whole tree.** Test 1's path rule resolves against the
   repository's top.
   - It passes in this checkout and in a `git archive` of the whole tree.
   - It fails in an export of `datastorekit/` alone, on this repository's own `docs/` citations.
   - Every export the agent runs the module in is of the whole tree.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **Pin the anchor.** Test 4 also asserts that `Datastore.object_get`, in a planted comment and a
  planted docstring, is not found. The deliberate-breakage record gains:
  - **(i)** the module rule's trailing boundary dropped: test 1 fails on correction 1's five
    lines, and test 4 fails.
- **Write the module first, and run it on the unrewritten tree.** Do this in a scratch export of
  `HEAD` with the module copied in. Expected: test 1 fails with 181 lines in 42 files; tests 2–4
  pass. That is the module's baseline, and the review replays it. Order:
  1. the baseline: 480; the port check; `black --check datastorekit docs`, 69 files; the guard;
     the clients' `HEAD`s and statuses;
  2. the module, run on the unrewritten tree as above;
  3. the rewrite, file by file, with §2.3's guard changes;
  4. §4.3's check, file by file; the suite, `480 + N` OK;
  5. the high end; §4.4's measurement after; `--help`;
  6. (a)–(i), each in its own scratch export, each over the module (and the guard, for (d)) and
     over the whole suite;
  7. `venv/`'s suite again, the port check, `black`, the guard, the clients again, the records.
- **Keep the AST check and the measurement scripts in the scratchpad, never committed.** The log
  gives each one's method, and enough of it to re-run. The AST check compares against
  `452b3c9`'s blobs (`git show 452b3c9:<path>`). For the new module and `test_layer_is_generic.py`
  it records "different", and says why.
- **Record each breakage as a diff, exactly as applied**, so that the review can replay it with
  `git apply` against an export of the commit.
- **Record tier C and the further lines in one table.** Give each line at `452b3c9`'s number: its
  text in brief, "rewritten" or "kept", and the reason. Give tiers A and B per file, as §8 says.

**The facts, checked by the orchestrator.** Pass them on.

- **The prompt's line references hold at `21334c2`.**
  - `test_layer_is_generic.py`:
    - the "known hits" paragraph `:31-35`;
    - `:71` ("relative to the repository root");
    - `:178` ("SecondaryGWKit's prompt 08");
    - the comment `:192`, and `KNOWN_HITS` `:193-203` with its inner comment `:197-199`;
    - `assertNoHits` `:323-327`.
  - `test_sharded_store_script.py:115-128`. Its seven phrases are in `tools/sharded_store.py`'s
    docstring, `:16-23`.
  - `tools/sharded_store.py`:
    - the source citation `:22-23`;
    - the false sentence `:25-26`;
    - `description=__doc__` `:40`.

    `import sys` at `:30` is used for no `sys.path`.
  - `tools/shard_key_audit.py`:
    - `:9` ("the B1 fix");
    - `:19` (`Datastore/shard_paths.py`);
    - `:24-26`, the false sentence;
    - `:188`, `e.g. "wavenumber"`.

    Its docstring is not its `--help`; no test reads it.
  - `test_shard_key_audit_copy.py:11` and `:89-91`.
  - `test_shard_key_audit_refusals.py:28`, `:92`, and `:193` (`"a2bd966"`, code).
  - `test_sharded_store_script.py:5-6`.
- **§1.1 reproduces.** The orchestrator reimplemented log 03a §8's method, matching each pattern
  within the token's own span of the physical line. At `8bc60a5`, `72cf34a`, `ae94aaa`, `7ceed25`,
  `0c66505` and `452b3c9` it gives:
  - 102 / 19;
  - 114 / 23;
  - 124 / 28;
  - 146 / 35;
  - 155 / 40;
  - 155 / 40.

  Matching the whole physical line gives 159 instead. It counts four `REPO_ROOT` code lines that
  carry a string token:
  - `test_layer_is_generic.py:73`;
  - `test_store_inventory.py:74` and `:450`;
  - `test_store_reader.py:356`.

  The agent's measure after must match within the token.
- **Tier A reproduces** with correction 1's anchor: 181 lines in 42 files, the appendix's
  unstarred lines less the nine SHA lines, exactly.
- **(g) reproduces.** With the existence check dropped, the rules find six more lines:
  - `tests/client/__init__.py:3`, `tests/client/factories.py:3` and `tests/client/registry.py:15`;
  - `test_layer_is_generic.py:25` and `:66`;
  - `test_neutral_client.py:4`.

  Each is a `docs/` path of this repository.
- **§4.3's check behaves as the prompt says.** It compares `ast.dump` with every module, class and
  function docstring set to `""`; `ast.dump` omits line numbers, so a shrunk docstring moves
  nothing. Probed in a scratch export of `452b3c9`:
  - a citation removed from `test_sharded_store_script.py`'s docstring and rewrapped compares
    equal;
  - one removed from a comment of `SQL/Datastore.py` compares equal;
  - 08b's `ShardedPool.py` (`f24ded1` → `efedc8d`) compares different;
  - (h), a docstring edit with one changed assertion string, compares different;
  - `KNOWN_HITS` with its entry emptied compares different.
- **The guard with `KNOWN_HITS` emptied.** Probed in an export of `452b3c9`:
  - with `:188` rewritten to name no table, the guard's 8 tests pass;
  - with `:188` left as it is, `test_no_comment` fails, which is (d).
- **The high end resolves offline.** `uv` 0.12.20, then:
  1. `uv venv --offline -p /opt/local/bin/python3.13`;
  2. `uv pip install --offline "ray==2.55.1" "sqlalchemy==2.0.46"`;
  3. `uv pip install --offline --no-deps -e <export>`.

  This gives Python 3.13.16, Ray 2.55.1, SQLAlchemy 2.0.46 and SQLite 3.53.4. The export of
  `452b3c9` gives `Ran 480 tests … OK`, with **4** `ResourceWarning` lines.
- **The toolchain.** `venv/`: Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39, SQLite 3.53.4, `black`
  25.1.0, `datastorekit 0.2.0` installed editable from this checkout. Hazard 1 of 08b holds: run
  an export's tests from its root, and print `datastorekit.__file__`.
- **Expected counts.**
  - The suite: **480** before; **480 + N** after, at both ends, N the loader's count for the new
    module (at least 4).
  - `compare_ported_tests.py`: exit 0, "20 module(s) … 1 test(s) declared not ported", unchanged.
  - `black --check datastorekit docs`: **69** files before, **70** after.
  - The guard: `KNOWN_HITS` at one entry before, empty after; 8 tests pass at both.
  - `.py` files under `datastorekit/`: **65**, and **66** with the module (test 2's floor is 60).
  - The index is **5**, and **4** after, unless the work opens an issue. `prompts/INDEX.md`'s
    count goes **1 → 0**.
- **The clients' trees.** SGK and SI are clean; CPBH has 23 untracked entries. None is read.
- **Ray.** No Ray process was up at writing.

**What the review exists to establish.**
- **(E1) Only prose.** §4.3's check over every changed `.py` file: equal, except the two declared
  files. `KNOWN_HITS` is the guard's one code difference.
- **(E2) The rewrite.** Every appendix line, and every further line, is rewritten or recorded as
  kept with a reason. Each rewritten sentence:
  - keeps its explanation;
  - is true for this package;
  - opens a module docstring with what the module is about (hazard 1);
  - keeps hazard 3's seven phrases verbatim;
  - adds no client vocabulary.

  §2.2's five sentences are true, and so are correction 4's two.
- **(E3) The module.** §2.4's four tests and addition 1. On the unrewritten tree, test 1 fails with
  181 and tests 2–4 pass. Its prose passes its own scan.
- **(E4) Both ends.** `480 + N` in `venv/` and at the high end, in the review's own venv.
- **(E5) The measurement after.** Tier A's rules give 0. No SHA of the source is left in prose.
  Log 03a's method finds only lines the log explains.
- **(E6) The breakages.** (a)–(i) each fail as recorded.
- **(E7) The records.**

**Conventions.** 08b's note's, unchanged, and all bind the agent:
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
- **No `git stash` in this checkout.** The unrewritten tree is a scratch export.
- **No push, no tag.**
- **Format only the files changed**, with `black`. A docstring's text is not reflowed by `black`,
  so a rewrapped paragraph is the agent's own, within the file's existing width.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. Record `git status --short
   --ignored` (at writing: `.idea/`, `venv/` and five `__pycache__/` directories).
2. **The baseline.** In `venv/`, the suite gives `Ran 480 tests … OK`; the port check exits 0;
   `black --check datastorekit docs` leaves 69 files unchanged.
3. **The clients.** Each `HEAD` is the gate's, and `git status --short` is as §0's facts say.
4. **The remote.** `git ls-remote origin` shows `main` at `102f225…`, `v0.1.0` peeling to
   `68db557…` and `v0.2.0` to `240028e…`, and no other tag. (The sandbox has no network;
   `ls-remote` needs it lifted, for that one read.)
5. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`.
6. **The index.** 5 now, and 4 after unless the work opens an issue. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `PROVENANCE.md`, and logs 03a (§8), 04a (§7 item 4), 04b (§8) and 08b;
- `HEAD`, the clients' `HEAD`s and statuses, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's five corrections and five additions. Correction 1 is
the one that would stop it: without the boundary test 1 cannot pass on true prose. Correction 3's
list is a start, not the scope; its own last pass decides the rest.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/09-rewrite-the-package-prose.md`, in README §5.1's
  form, with the prompt's §8 additions.
- **The files it may add or change are the prompt's §7 list, and nothing else.** It changes only
  comments and docstrings under `datastorekit/`, except §2.3's `KNOWN_HITS` entry and the new
  module. It must not touch:
  - `docs/` (the contract and `docs/adoption/` among them);
  - `compare_ported_tests.py`, `PROVENANCE.md`, `README.md` or `pyproject.toml`;
  - `CLAUDE.md`, the campaign README or the workflow;
  - anything under `orchestrator/`.
- **It writes nothing in any client repository, and runs, imports or opens nothing of one.**
- **It downloads nothing.**
- **It pushes nothing and makes no tag.**
- **It starts no Ray.**
- **Stop and ask** on any of the prompt's §6 conditions.

## 3. The review — twelve checks

Make the review's venv fresh, offline, in a subdirectory of the scratchpad of its own, not the
agent's.

1. **Scope.** `git show --stat <commit>` touches only:
   - files under `datastorekit/`, each among the appendix's 42, correction 3's or the log's
     further lines;
   - the new module;
   - the log, the board, `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.

   Nothing under `docs/` is touched but the index. `git status --short --ignored` lists the same
   entries as at dispatch. Each client's `HEAD` and `git status --short` are as at dispatch.
2. **E1, by running.** The review's own AST check, over every `.py` file the commit changes under
   `datastorekit/`, against `21334c2`'s blobs. Every file compares equal except:
   - `test_layer_is_generic.py`, whose one difference is the emptied `test_no_comment` list;
   - the new module.

   The comparison is made with docstrings blanked.
3. **E2, by reading: the diff.** Read every hunk. For each:
   - the source's citation is gone and the explanation kept;
   - the sentence is true at the commit;
   - a module docstring opens with what the module is about;
   - "extraction prompt NN" is used where a bare "prompt NN" in an imported module could be read
     as the source's;
   - nothing is restyled beyond the rewrapped sentence;
   - no client vocabulary is added.

   §2.2's five sentences and correction 4's two are true. `defaults.py:2-3` and `_timing.py:2-4`
   keep the import commit and `PROVENANCE.md`, and drop the source's file names.
4. **E2, by reading: what was kept.** Check the log's tier C and further-line table. Check correction
   3's lines one by one against it. Read the reason for each "kept", and run a sweep of the
   review's own for `prompt \d`, `log \d`, `README`, `audit`, `§`, labels and 7-hex strings in
   prose. Every remaining hit is this repository's, the module's own vocabulary or the tool's own,
   or is in the log.
5. **E3, the module, by reading.** Each of §2.4's tests is there, under a name that says what it
   pins, and addition 1 is in test 4.
   - The file set comes from the filesystem.
   - Docstrings are read by `ast`, comments by `tokenize`, and nothing else.
   - The path rule checks existence against the repository's top.
   - The module rule has its trailing boundary.
   - Failures name `file:line rule matched-text`, all at once.
   - The planted forms are runtime strings, and its own prose quotes no forbidden form.
   - No Ray, no store, no client; `tearDownModule` checks Ray.
6. **E3, by running against the unrewritten tree.** In a `git archive 21334c2` export of the whole
   tree with the new module copied in: test 1 fails, naming 181 lines in 42 files, and tests 2–4
   pass.
7. **E4, both ends.** In `venv/`: `Ran 480 + N tests … OK`, the loader giving N for the module. In a
   fresh offline high-end venv with a whole-tree export installed editable: the same, and the
   `ResourceWarning` count against the log's (4 at `21334c2`).
8. **E5, the measurement after.**
   - The review's own tier A scan gives 0.
   - `b04671f`, `a2bd966` and `e53f323` appear in no comment or docstring. `:193`'s string stays.
   - Log 03a's method, matched within the token, finds only lines the log lists with a reason.
   - `python -m datastorekit.tools.sharded_store --help` carries hazard 3's seven phrases and no
     citation.
9. **The checks.**
   - The port check exits 0 with 04b's counts.
   - `black --check datastorekit docs` leaves 70 files unchanged.
   - The layer guard passes with every `KNOWN_HITS` list empty.
10. **E6, the breakages.** Replay (a)–(i) as the log records them, each in its own whole-tree
    export. Each fails as the prompt's §4.6 says, and (i) as addition 1. Over the whole suite each
    verdict is the log's.
11. **E7, the records.**
    - The log:
      - every section of README §5.1, with the port check's output in place of
        `compare_with_source.py`'s;
      - §4.3's check file by file;
      - §4.4's measurement after;
      - the tier C and further-line table;
      - §2.2's corrections;
      - the breakage record;
      - the clients' commits and statuses, at the start and the end.

      Under "Observations not acted on": that `logs/` is no rule's prefix (correction 3).
    - The board: 09's row and the header. The issue moves from §3 to §4, with its "Closed (…,
      prompt 09)" line naming:
      - the count rewritten;
      - the guard emptied;
      - the new module.
    - `docs/OPEN_ISSUES.md`: no row on this repository, the header saying 4 open and the date.
    - `prompts/INDEX.md`: the campaign's line, and its open-issue count of 0.
12. **Nothing left behind.** No Ray process; `git tag -l` is `v0.1.0` and `v0.2.0`; `origin`
    unchanged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 09* paragraph, in the form of
  08b's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README's header, and its §2 status for 09 ("landed, reviewed");
  - the notes line, with this note marked "used for 09".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Report to the user:**
  - the lines rewritten, by tier, and the further lines;
  - the AST check;
  - the module, and its 181 on the unrewritten tree;
  - the `480 + N` at both ends;
  - (a)–(i);
  - `KNOWN_HITS` empty;
  - the index at 4, and the board with no open issue;
  - that 10 can be written.

**Hand on to 10's author:**
- Line numbers move in every file 09 rewrites. Citations made before 09 are of their own trees
  (`CLAUDE.md` rule 6), and 10's addenda cite 09's tree or later.
- `KNOWN_HITS` is empty, and `test_prose_names_no_source` guards the package's prose. 10 writes no
  prose under `datastorekit/` that names the source's layout.
- 09 does not change `README.md`, `PROVENANCE.md`, `pyproject.toml` or `docs/`. All four are 10's
  to bring to `0.2.1`.
