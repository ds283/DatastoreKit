# Orchestrator — prompt 10, release `v0.2.1`

Read [`../README.md`](../README.md) first: §1, §2 (rows 08a–11), §4, §5 (rules 4, 5, 9 and 10),
§6.2 (U3, U23, U28, U29, U33, U36 and U37) and §7. Then read [`prompt-09.md`](prompt-09.md) §0's
"Conventions", which this note keeps unless it says otherwise; [`prompt-06.md`](prompt-06.md) §5,
which this note's §5 follows; and the board's review of 09.

**You do not write code.** You may:
- run the suite, the port check, `black --check`, the layer guard and the prose guard;
- make venvs in the session scratchpad with `uv pip install --offline`, from the cache 05's work
  filled, and nothing else: **no download** (the prompt's hazard 5);
- export the tree with `git archive` into the scratchpad, and build wheels, run probes and replay
  breakages there, never in this checkout and never committing one;
- read the three clients only through `git -C <client> rev-parse|status|log|grep`, at the
  checklists' commits (the prompt's hazard 4);
- fix small residue in a follow-up commit of your own (§4);
- after the review, and only with the user's approval of each push, push and tag as §5 says.

**The prompt:** [`10-release-v0.2.1.md`](../10-release-v0.2.1.md)
**Closes:** nothing · **Narrows:** nothing · **Changes:** nothing · **Opens:** only what the work
finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- 09 landed (`cad7bc1`) and was reviewed (`ffe843c`); the user's decision on its finding is at
  `98fb497`. 10 is written (`29bf379`).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- From `cad7bc1` to `29bf379` only five files under `prompts/` changed. So `datastorekit/`,
  `docs/`, `README.md`, `PROVENANCE.md` and `pyproject.toml` are `cad7bc1`'s, and the prompt's
  facts "at `98fb497`" are the tree's.
- `origin/main` is `102f225`, an ancestor of local `main`, which is 18 commits ahead of it at
  `29bf379`. `origin` holds `v0.1.0` (peeling to `68db557`) and `v0.2.0` (`240028e`) only.
- The clients' `HEAD`s, which are the checklists' commits: SGK `b510bc9` (branch
  `handover-remedial`, clean), CPBH `52142d7` (`main`, 23 untracked entries), SI `7bb3efd`
  (`main`, clean).
- The board's §3 holds no issue of this repository, and the index is **4**, all inherited.
- One prompt at a time in this checkout. 11 is not written.

## 0. What makes this prompt unusual

**No line of code changes, so the suite cannot catch a bad edit.** It passes whatever the
documents say. What stands in for it:
- the release check, from a clean export, which is the only thing that sees `0.2.1`;
- hazard 1's `git diff`, which must show `+` lines only under `docs/adoption/`;
- reading: every statement an addendum makes is true of `v0.2.1`, every statement it supersedes is
  named by `path:line`, and every name and link resolves.

The review is therefore mostly reading and the release check.

**The acceptance finishes elsewhere**, as 05's and 06's did. `v0.2.1` is made on 10's commit only
once CI has passed there at both ends (§5). It is the release every client adopts (U37), so it is
the commit their pins will name.

**The push carries more than 10.** `origin/main` is `102f225`. Pushing 10's commit as `main`
fast-forwards over 07a, 08a, 08b and 09, their reviews and this note. CI runs on the pushed head
only, so 08a's, 08b's and 09's commits never run in CI on their own. The tree the tag names is the
one CI tests, which is what U23 and U28 ask for. The review's report says so.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-10 at `29bf379`, in `venv/`,
in offline scratch venvs and in scratch exports. Pass them on. Corrections 1–3 change what the
agent does or writes, and are STRUCTURALLY REQUIRED. Corrections 4 and 5 correct what the prompt
states; the log records each as found.

1. **Hazard 7's reinstall cannot run offline.** `./venv/bin/python -m pip install --no-deps -e .`
   builds the package in an isolated environment. That environment needs `setuptools>=64`
   (`pyproject.toml`'s `[build-system]`) from an index, and `venv/` has no `setuptools`.
   - Probed with `--no-index`: the build subprocess fails.
   - Without `--no-index`, pip would download. That is hazard 5's stop.

   **Use `uv pip install --offline --no-deps --python ./venv/bin/python -e .`** from the
   repository root. `uv`'s cache holds the build backend. Probed on a scratch `python3.12 -m venv`
   with an export at `0.2.1`: it installs, `pip show datastorekit` says `Version: 0.2.1`, and the
   editable location is the export.
2. **The editable reinstall writes `datastorekit.egg-info/` at the root.** It is ignored
   (`.gitignore` has `*.egg-info/`), so `git status --short` does not show it. `--ignored` does, and
   §4.3 says the checkout holds no `*.egg-info`.
   - Remove that one directory after the reinstall, and record it.
   - Probed: with it removed, the editable install still imports from the source tree, and
     `importlib.metadata.version("datastorekit")` is `0.2.1`. The metadata is in `site-packages`.

   `git status --short --ignored` at the end must equal dispatch's.
3. **"Log 08a §2.5" is log 08a §3.** Log 08a has no §2.5. Its §3 is headed "The clients (§2.5)":
   it answers prompt 08a's §2.5, and holds the payload measurement. The prompt cites it at its
   "Read first" item 4, §1.1, the SGK and SI rows of §2.4, and hazard 4. **Every citation the agent
   writes says "log 08a §3"**: in the addenda, in `PROVENANCE.md` if it cites it, and in the log.
   A citation of a section that does not exist fails hazard 2.
4. **The contract's rows have no anchors.** §2.4's README row says "each a link to its contract
   row". Link each behaviour to its subsection, and name the row by its "Change" cell:
   - the `KeyError` and the payloads: §9.1, `#91-prompt-08a`;
   - the refused open: §9.2, `#92-prompt-08b`.

   From `docs/adoption/` the path is `../client-contract.md#…`. §9's own anchor is
   `#9-changes-after-v020`, as the prompt says. All three follow GitHub's rule: lower-case, drop
   backticks and punctuation other than hyphens, spaces to hyphens. That is the rule behind the
   README's existing `#8-version-keyed-lookups-v020-prompt-06`. The headings are
   `docs/client-contract.md:249`, `:254` and `:263`.
5. **One line number in §2.4's table is off.** In `docs/adoption/README.md`, "The campaign closes
   at 07b" is at `:156` alone. `:155` is the G2 bullet's link, and the bullet is `:154-156`. Cite
   `:154` for G2's `v0.2.0` and `:156` for 07b. Every other number in the table holds (below).

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **Work in this order:**
  1. the baseline: 486 in `venv/`; the port check; `black --check datastorekit docs`, 70 files; the
     clients' `HEAD`s and statuses; the `KeyError` measure (hazard 4);
  2. `pyproject.toml`; `venv/`'s reinstall (corrections 1 and 2); the suite;
  3. `README.md` and `PROVENANCE.md`;
  4. the four addenda; then hazard 1's `git diff`;
  5. the board's gates;
  6. the release check; the high end;
  7. (a) and (b);
  8. the documents' check (§4.4) and the name-and-link check (hazard 2);
  9. `venv/`'s suite again, the port check, `black`, the clients again, the records.
- **Give each addendum's supersessions as a table**: `path:line`, the statement in brief, and what
  replaces it. The log repeats the four tables, with any statement found that the prompt's table
  does not name.
- **Keep the name-and-link check as a scratch script**, never committed. It extracts every
  relative link and anchor from `README.md`, `PROVENANCE.md` and the four adoption files, resolves
  each file, and finds each anchor among the target's headings by GitHub's rule. It also lists
  every dotted `datastorekit.` name, each of which is imported in `venv/`. The log gives its
  method and its output.
- **Build (a)'s and (b)'s wheels from their own exports**, each with the prompt's change and only
  that, and record each as a diff to `pyproject.toml` that `git apply --check` and `-R --check`
  accept against an export of the commit.

**The facts, checked by the orchestrator.** Pass them on.

- **§1.1 reproduces.** With every module, class and function docstring blanked, `ast.dump` of each
  layer file at `240028e` and `cad7bc1` gives:
  - **code:** `SQL/ShardedPool.py` alone;
  - **prose only:** 12 files, `_timing.py`, `contract.py`, `defaults.py`, `replication.py`,
    `shard_paths.py`, `store_inventory.py`, `store_reader.py`, `SQL/Datastore.py`,
    `SQL/factory_base.py`, `SQL/schema.py` and both tools;
  - **unchanged:** the seven the prompt names.

  08a and 08b changed only `SQL/ShardedPool.py` among layer files (`git diff --stat 240028e
  efedc8d`: +50 −2). 09 changed the prose of 13 layer files, `SQL/ShardedPool.py` among them. The
  four test modules the prompt names are the only ones added.
- **SGK's 17 and the six.** SGK's 17 are `PROVENANCE.md`'s file map less `tools/__init__.py`: the
  15 layer files and the two tools. 09 touched 11 of them, both tools and `SQL/ShardedPool.py`
  among them. The other six are the prompt's six. Each was byte-identical to SGK's source against
  `v0.2.0` (the checklist's 11), and none has changed since.
- **The `KeyError` measure reproduces**, at the checklists' commits, exactly as §1.1 states:
  - SGK: `RunRegistry/__init__.py:606` (`except (KeyError, TypeError, ValueError):`) and
    `RunRegistry/tests/test_run_registry.py:489`; the `try` within three lines before a
    `ShardedPool(` outside `Datastore/` is in `m7_messages.py:184` and `m4c_open_rw.py:38` only;
  - CPBH and SI: nothing, on either measure.
- **The bare-key refusal is unchanged at `v0.2.1`.** `object_get_vectorized` is
  `SQL/ShardedPool.py:3326-3350` at `cad7bc1`. Its membership test is `:3338` and the payload copy
  is `:3347`, so a bare key is refused before the payload line in both releases.
- **§1.2 reproduces.** From a `git archive` of `29bf379` with only the version changed, `uv build
  --offline --wheel` gives `datastorekit-0.2.1-py3-none-any.whl`:
  - 97,849 bytes; 25 entries, none under `datastorekit/tests/`;
  - `datastorekit-0.2.1.dist-info/licenses/LICENSE` among them;
  - `METADATA`: `Version: 0.2.1`, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43`,
    `Requires-Dist: sqlalchemy<2.1,>=2.0.39`.

  Installed offline with `ray==2.55.1` and `sqlalchemy==2.0.46` into a Python 3.13.16 venv, and run
  from a directory outside the repository with `PYTHONPATH` unset:
  - the 20 layer modules import from `site-packages`;
  - the `contract` import works;
  - `import datastorekit.tests` raises `ModuleNotFoundError`;
  - the metadata version is `0.2.1`;
  - `sharded_store --help` exits 0;
  - `shard_key_audit --help` exits 2 with `!! No such file: <cwd>/--help`.

  The orchestrator's SHA-256 is not given; the agent records its own.
- **(b) reproduces.** With the `exclude` line deleted as well, the wheel has 71 entries, 46 of them
  under `datastorekit/tests/`.
- **The line numbers of §2.4's table hold**, but for correction 5:
  - `docs/adoption/README.md` `:3`, `:8`, `:24-26`, `:35`, `:154`, `:174`;
  - `secondarygwkit.md` `:6`, `:17`, `:25-27` (the count, in the paragraph `:19-29`), `:203-206`,
    `:292-297`, `:301`;
  - `champbh.md` `:6`, `:18`, `:254-255`, `:374`;
  - `stochasticinstantons.md` `:5`, `:16`, `:255-257`, `:348`.

  The orchestrator found no further statement that `v0.2.1` makes false, outside what the table
  names. The inherited issues at `secondarygwkit.md:350-354` are still four and still inherited.
  The agent's own reading decides; the prompt's table is not the scope.
- **The README's lines** the prompt replaces are at `README.md:10-13` (Status, `v0.2.0`), `:50` (the
  pin) and `:53` ("`v0.1.0` remains, …"). "Using it"'s link to contract §8 is at `:82`.
  `PROVENANCE.md`'s "After `v0.1.0`" is `:78`, and "Prompt 06" is `:89`, the file's last section.
- **The toolchain.**
  - `venv/`: Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39, SQLite 3.53.4 and `black` 25.1.0, with
    `datastorekit 0.2.0` installed editable by pip from this checkout.
  - `uv` 0.12.20.
  - The high end, `uv venv --offline -p /opt/local/bin/python3.13`, gives Python 3.13.16, Ray
    2.55.1, SQLAlchemy 2.0.46 and SQLite 3.53.4.
- **Expected counts.**
  - The suite: **486**, before and after, at both ends. The high end has 4 `ResourceWarning` lines,
    and `venv/` none. Measured at writing: `Ran 486 tests … OK` in `venv/`, and in an offline
    high-end venv with an export of `29bf379` installed editable. Each took 8–9 minutes, run side
    by side.
  - `compare_ported_tests.py`: exit 0, "20 module(s) … 1 test(s) declared not ported".
  - `black --check datastorekit docs`: **70** files, before and after.
  - The index: **4**, unchanged unless the work opens an issue.
- **Ray.** No Ray process was up at writing.

**What the review exists to establish.**
- **(E1) Scope.** Only the prompt's §7 files change. Nothing under `datastorekit/`, and not
  `docs/client-contract.md`.
- **(E2) The release.** A wheel from a clean export of the commit is `0.2.1`, holds the layer and
  its tools and no tests, and behaves as §1.2 says from outside the repository.
- **(E3) The documents.** `pyproject.toml`, `README.md` and `PROVENANCE.md` are as §2.1–§2.3 say.
  Every statement is true of `v0.2.1` and says nothing is tagged yet. Every name and link
  resolves.
- **(E4) The addenda.** Each is additive, dated and placed as §2.4 says. Each states its pin, what
  changed for its client, and what it supersedes, by `path:line`, true at the file.
- **(E5) Both ends.** 486 in `venv/` (now `0.2.1`) and at the high end.
- **(E6) The breakages.** (a) and (b) fail as recorded.
- **(E7) The records.**

**Conventions.** 09's note's, unchanged, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff **as recorded in the log** with `git apply --check` and `-R --check`
  against a scratch export;
- read a client only through `git`, and never import or run its code;
- use a subdirectory of the session scratchpad, never `/tmp`, for venvs, exports, wheels and
  probes, and put **no scratch `.py` under `datastorekit/` or `docs/`**;
- start no Ray;
- a stop goes to the user;
- check `git log` before committing.

And for this prompt:
- **No download of any kind.** Every venv and build is `--offline`, and `venv/`'s reinstall is
  correction 1's. A pin that does not resolve offline is a stop.
- **No push, no tag, and no change to the GitHub repository's settings.**
- **Nothing is built in the checkout** but `venv/`'s editable reinstall, whose `egg-info` is
  removed (correction 2).

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. Record `git status --short
   --ignored` (at writing: `.idea/`, `venv/` and five `__pycache__/` directories).
2. **The baseline.** In `venv/`, the suite gives `Ran 486 tests … OK`; the port check exits 0;
   `black --check datastorekit docs` leaves 70 files unchanged; `pip show datastorekit` says
   `0.2.0`.
3. **The clients.** Each `HEAD` is the gate's, and `git status --short` is as the gate says.
4. **The remote.** `git ls-remote origin` shows `main` at `102f225…`, `v0.1.0` peeling to
   `68db557…` and `v0.2.0` to `240028e…`, and no other tag. (The sandbox has no network;
   `ls-remote` needs it lifted, for that one read.)
5. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`.
6. **The index.** 4 now, and 4 after unless the work opens an issue. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `PROVENANCE.md`, and logs 05 (§5.3), 06 (§5.5), 08a (§3 and §8), 08b (§8) and 09 (§8);
- `HEAD`, the clients' `HEAD`s and statuses, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's five corrections and four additions. Correction 1 is the
one that would stop it: the prompt's own reinstall reaches for the network.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/10-release-v0.2.1.md`, in README §5.1's form, with
  the prompt's §5.5 and §8 additions.
- **The files it may change are the prompt's §7 list, and nothing else.** It must not touch:
  - anything under `datastorekit/`;
  - `docs/client-contract.md`, `docs/extraction/` or the workflow;
  - `CLAUDE.md`, `LICENSE`, `.gitignore` or the campaign README;
  - anything under `orchestrator/`.
- **Under `docs/adoption/` it adds lines only.**
- **It writes nothing in any client repository, and runs, imports or opens nothing of one.**
- **It downloads nothing.**
- **It pushes nothing, makes no tag, and changes no setting of the GitHub repository.**
- **It starts no Ray.**
- **Stop and ask** on any of the prompt's §6 conditions.

## 3. The review — ten checks

Make the review's venvs fresh, offline, in a subdirectory of the scratchpad of their own, not the
agent's.

1. **Scope.** `git show --stat <commit>` touches only:
   - `pyproject.toml`, `README.md` and `PROVENANCE.md`;
   - the four files under `docs/adoption/`;
   - the log, the board, `prompts/INDEX.md`, and `docs/OPEN_ISSUES.md` only if an issue is opened.

   No wheel, `dist/`, `build/`, `*.egg-info` or scratch file. `git status --short --ignored` lists
   the same entries as at dispatch. Each client's `HEAD` and `git status --short` are as at
   dispatch.
2. **E1 and E4, additive.** `git diff <parent> <commit> -- docs/adoption/` has no `-` line.
   `git diff <parent> <commit> -- datastorekit docs/client-contract.md docs/extraction .github` is
   empty. `pyproject.toml`'s diff is the version line alone.
3. **E2, the release.** From `git archive <commit>`, build the wheel offline and install it into a
   fresh high-end venv, offline. Check §1.2's facts:
   - 25 entries, none under `tests/`; the licence;
   - `METADATA`'s three lines and `Version: 0.2.1`;
   - from outside the repository with `PYTHONPATH` unset: the 20 modules, the `contract` import,
     `datastorekit.tests` refused, `0.2.1`, and the two tools as §1.2 says.

   Compare the wheel's file list with the log's.
4. **E3, `README.md` and `PROVENANCE.md`, by reading.**
   - The Status paragraph names the three fixes and 09, says no API, nothing written and no
     message changes, names `KeyError` → `RuntimeError`, and points at §9.
   - The pin is `v0.2.1`. The sentence that replaces `:53` says both earlier tags remain, and
     that every client adopts `v0.2.1`. Nothing says `v0.2.1` is tagged.
   - "Using it" gains §9's item, with `#9-changes-after-v020`. Nothing else in the README changes.
   - `PROVENANCE.md`'s new section is after "Prompt 06". It names each issue, prompt, commit and
     test module, and U3 and U33. It states 09's seven untouched files, and the files and log of
     each prompt. Nothing above it changes.
5. **E4, the addenda, by reading.** For each of the four files:
   - the italic line is where §2.4 puts it; the addendum is unnumbered, dated, says it is
     extraction prompt 10's, and sits after item 10 (after §6 in the README), before the
     appendix;
   - it gives the pin, and says the client adopts `v0.2.1` (U37);
   - what it says changed for the client is the prompt's row, true of `cad7bc1`'s tree, and
     links §9.1 or §9.2 (correction 4);
   - each superseded statement is cited by a `path:line` that holds in the file as committed
     (an addition above a cited line would move it: check);
   - log 08a is cited as §3 (correction 3), and §1.1's `KeyError` finding is stated as measured;
   - the engine disposal and the `KeyError` change are one sentence each in every checklist.
6. **E3 and E4, names and links, by running.** The review's own extraction of every relative link
   and anchor in the six documents: each file exists, and each anchor is a heading by GitHub's
   rule. Every dotted `datastorekit.` name imports in the review's release venv. The list matches
   the log's.
7. **E5, both ends.** In `venv/`: `pip show datastorekit` says `0.2.1`; `Ran 486 tests … OK`. In a
   fresh high-end venv with `git archive <commit>` installed editable: `Ran 486 tests … OK`, with
   4 `ResourceWarning` lines. The port check exits 0 with 04b's counts. `black --check
   datastorekit docs` leaves 70 files unchanged.
8. **E6, the breakages.** Replay (a) and (b) as the log records them, each in its own export. (a):
   `METADATA` and the metadata version say `0.2.0`. (b): the wheel lists `datastorekit/tests/`, and
   `import datastorekit.tests` succeeds from the installed wheel.
9. **E7, the records.**
   - The log: every section of README §5.1, with the prompt's §5.5 list in place of
     `compare_with_source.py`'s output. That is the port check, the release check, the documents'
     check, the names and links, the `KeyError` measure, (a) and (b), and the clients at both
     ends. It also has the five corrections and four additions, and each addendum's supersession
     table.
   - The board: 10's row, the header, and §2's gate titles at `v0.2.1`. Each gate gains a dated
     line saying `v0.2.1` is ready to tag on 10's commit once CI passes and no tag is made. The
     `v0.1.0` and `v0.2.0` lines are unchanged.
   - `docs/OPEN_ISSUES.md`: unchanged at 4, or as opened.
   - `prompts/INDEX.md`: the campaign's line.
10. **Nothing left behind.** No Ray process. `git tag -l` is `v0.1.0` and `v0.2.0`, and `origin` is
    unchanged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 10* paragraph, in the form of
  09's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README's header, and its §2 status for 10 ("landed, reviewed; awaiting CI for `v0.2.1`");
  - the notes line, with this note marked "used for 10".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Report to the user:**
  - what landed: `0.2.1`, the README, `PROVENANCE.md`, the four addenda and the gates;
  - the release check, and the 486 at both ends, from the review's own venvs;
  - the `KeyError` measure;
  - (a) and (b);
  - that the push carries 07a–09 and their records (§0);
  - **and ask for approval to push** (§5).

## 5. Reaching `v0.2.1`

06's note §5, with `v0.2.1` for `v0.2.0` and 10's commit for 06's. Each push and the tag is an
outward-facing act: **ask the user, and wait for a clear yes, before each.** Approval of one is not
approval of the next.

1. **Push 10's commit as `main`:** `git push origin <10's SHA>:refs/heads/main`. It fast-forwards
   from `102f225`, carrying every commit from 07a's review to this note's with it. The workflow runs
   on 10's commit, at both ends.
2. **Read the run** once it has finished: `gh run list --workflow tests.yml --commit <10's SHA>`
   and `gh run view <id> --log`. Do not poll in a loop. Ask the user to say when it has finished,
   or check once when they return. From each job's log, record:
   - the versions step 4 prints, SQLite's among them;
   - the suite's verdict line (`Ran 486 tests … OK`);
   - black's line on `low`.
3. **If either end fails**, stop. No tag. Record the failure on the board's §3 with the job's log
   lines, and tell the user that a fix prompt is needed. The tag goes on the fix's commit once its
   CI passes.
4. **If both pass**, with the user's approval:
   - `git tag -a v0.2.1 <10's SHA> -m "datastorekit 0.2.1: three fixes (an unsupplied sharded table, the vectorized get's payloads, a refused open's engines) and the package's prose"`;
   - `git push origin v0.2.1`;
   - check that `git ls-remote origin refs/tags/v0.2.1^{}` is 10's SHA.
5. **Then push the rest of `main`** (`git push origin main`), with approval.
6. **Record it**, in a commit of its own, before step 5's push or as part of it:
   - the board's G2, G3 and G4 lines: `v0.2.1` made on 10's SHA, with the tag object, the run's
     URL and both ends' versions;
   - the review paragraph's last line;
   - README §2's status for 10;
   - `prompts/INDEX.md`.

**Hand on to 11's author:**
- `v0.2.1` is on 10's commit, once §5 has run. Every client adopts it (U37). G2–G4 are recorded as
  they hold, and the campaign does not wait for them.
- The adoption checklists are 07a's measurements of `v0.2.0` plus 10's addenda. 11's verification
  document cites both, and re-measures no client.
- The contract's §8 citation is 11's to correct (U34). The commit-point labels of
  `test_reconcile_at_open` are 11's to record (the user's decision at `98fb497`).
