# Orchestrator — prompt 05, supported versions and CI

Read [`../README.md`](../README.md) first: §0.2, §2 (rows 05 and 06), §4, §5 (rules 7, 8 and 10),
§6.2 (U4, U6, U23 and U24) and §7 (G2). Then read [`prompt-04b.md`](prompt-04b.md) §0's
"Conventions", which this note keeps unless it says otherwise, and the board's review of 04b.

**You do not write code.** You may:
- run the suite and both checks;
- make venvs in the session scratchpad with `uv`, downloading PyPI packages into it (U24), and
  nothing else;
- build wheels from a clean export in the scratchpad, never in this checkout (correction 1);
- replay the log's breakage record, and revert it;
- run a probe from the session scratchpad, never committing one;
- read SGK through `git -C /Users/ds283/Documents/Code/SecondaryGWKit show <commit>:<path>`;
- fix small residue in a follow-up commit of your own (§4);
- after the review, and only with the user's approval of each push, push and tag as §5 says.

**The prompt:** [`05-supported-versions-and-ci.md`](../05-supported-versions-and-ci.md)
**Closes:** nothing · **Narrows:** nothing · **Changes:** nothing · **Opens:**
`[05-a-refused-open-leaves-its-engines-undisposed]`, and only what else the work finds ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- 04b landed (`0c66505`) and its review is recorded (`18c102c`). 05 is written (`2255206`).
  U6, U23 and U24 are taken.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- Nothing outside `prompts/` and `docs/OPEN_ISSUES.md` has changed from `0c66505` to `2255206`.
- SGK's `Datastore/`, `tools/`, `utilities.py` and `config/` (`defaults.py`, `sharding.py`,
  `datastore.py`) are unchanged from `6f7f291` to SGK `HEAD` (`b510bc9`), so
  `compare_with_source.py` and `compare_ported_tests.py` read what they read at 04b.
- `origin/main` is `47d3ab1` (by `git ls-remote`), an ancestor of local `main`.
- One prompt at a time in this checkout. 06 is not written.

## 0. What makes this prompt unusual

**No file under `datastorekit/` changes, and no test is added.** Its weight is in environments:
- two fresh venvs, one at each end of §0.2's table, and the checkout's own `venv/`;
- a wheel, installed into a third venv and run from outside the repository;
- a workflow that cannot run here, replayed step by step.

Each of these fails in its own way when it is set up wrongly, and the failure looks like the
layer's. The review re-does each from its own venvs, not the agent's.

**It is the first prompt whose acceptance finishes elsewhere.** CI runs only on GitHub, after the
review, and `v0.1.0` is made only when CI has passed at both ends on 05's commit (U23). §5 says how.

**What moves on purpose:**
- `pyproject.toml`;
- `.github/workflows/tests.yml` (new);
- `README.md`;
- the records.

Nothing under `datastorekit/` or `docs/` (but `OPEN_ISSUES.md`) changes. Neither do
`PROVENANCE.md`, `CLAUDE.md`, `LICENSE`, `.gitignore` or the campaign README.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-09 at `2255206` (package
files as at `0c66505`, unchanged since), with `uv` 0.12.20 and MacPorts' Python 3.12.15 and
3.13.16. Pass them on. Corrections 1–3 change what the agent does, and are STRUCTURALLY REQUIRED.
Corrections 4 and 5 correct what the prompt expects; the log records them as found.

1. **Build every wheel from a clean export, never in this checkout.** The checkout holds two
   ignored directories that setuptools reads back into a build:
   - `build/` (61 files, 41 of them under `build/lib/datastorekit/tests/`), left by the planner's
     `uv build` on 2026-10-09;
   - `datastorekit.egg-info/`, from 01's editable install, whose `SOURCES.txt` lists the 41 test
     files.

   **Probed**, each from a copy of `2255206`'s tree with §2.1's and §2.4's `pyproject.toml`:
   - with neither directory: 25 entries, none under `datastorekit/tests/`;
   - with the checkout's `build/` added: 66 entries, 41 under `datastorekit/tests/`;
   - with only the checkout's `datastorekit.egg-info/` added: 66 entries, 41 under it.

   So a wheel built in place fails the release check with the exclusion right, and (f) passes
   without testing anything. A stale `SOURCES.txt` also defeats (e): built from a copy holding one,
   the `datastorekit.t*` wheel still carried `datastorekit/tools/`.

   **The method.** For the release check, and for each of (e) and (f), export the working tree's
   tracked and unignored files into a fresh scratch directory:

   ```bash
   git ls-files -z -co --exclude-standard | tar --null -T - -cf - | tar -xf - -C <fresh dir>
   ```

   Then build with `uv build --wheel --out-dir <scratch> <fresh dir>`. A breakage is applied in its
   own export, never in the checkout. **Do not delete `build/` or `datastorekit.egg-info/`.**
   They are ignored and not this prompt's; the editable installs rewrite the second, and that is
   expected. `git status --short --ignored` lists the same ignored entries before and after the
   work: `.idea/`, `build/`, `datastorekit.egg-info/`, `venv/` and five `__pycache__/`
   directories at dispatch. No `dist/` appears. The log quotes both listings.
2. **`shard_key_audit` has no `--help`.** It has no `argparse`. `main(argv)` takes exactly one
   argument, so `--help` is read as a primary's path:
   - `python -m datastorekit.tools.shard_key_audit --help` prints `!! No such file: <cwd>/--help`
     and exits 2, from `venv/` and from the wheel (probed);
   - with no argument it prints `usage: <path of the module's file> <path-to-primary-database>`
     and exits 2.

   Rule 8 forbids adding a `--help`. So §2.4's release check reads, for that tool:
   - with no argument, it exits 2, and the path in its usage line is under the release venv's
     `site-packages`. This shows that the wheel's copy ran, not the checkout's;
   - `--help` exits 2 with the "No such file" line. The log quotes it.

   `sharded_store --help` exits 0, as the prompt says. For both tools, `python -c "import
   datastorekit.tools.<name> as m; print(m.__file__)"` names `site-packages`.
   - **(e)** is shown on `sharded_store --help` (exit 1, `No module named datastorekit.tools`),
     and on `shard_key_audit` by its message, since that tool exits 2 either way.
   - **§2.7's "one line each, from their `--help`"** reads, for `shard_key_audit`: from its module
     docstring's "Usage:" line and its usage message.
3. **(a) runs in a fourth, throwaway venv.** §3.7 says "in the high scratch venv", and also that
   the venvs you verify with are never changed. Make a fresh high-end venv with the two pins and
   no package, and run the suite from the repository root with `PYTHONPATH` unset.
   - **Probed:** `Ran 444 tests … FAILED (failures=19)`. These are 3 in `test_shard_key_audit_copy`,
     11 in `test_shard_key_audit_refusals` and 5 in `test_sharded_store_script`, all failures (not
     errors), and 21 lines say `No module named 'datastorekit'`. The log names the 19.
4. **The `ResourceWarning` line count is not a measurement.** The planner saw 188 lines at the high
   end; the orchestrator's run gave 172. They are printed when the collector runs, and that varies.
   §2.6's wrapper count is the measurement. The orchestrator's own wrapper (a `factory=` subclass of
   `sqlite3.Connection` installed on `sqlite3.connect` and `sqlite3.dbapi2.connect`, recording the
   innermost `datastorekit/` frame at creation and counting on `__del__` the connections never
   closed) gives the same result at **both** ends:

   | Opened at | Never closed | In tests of |
   |---|---|---|
   | `SQL/ShardedPool.py:858` (`with self._engine.connect() as conn:`) | 58 | `test_reconcile_at_open` 23, `test_prune_at_open` 13, `test_store_schema` 9, `test_version_row_at_open` 8, `test_read_only_pool` 4, `test_declared_facts` 1 |
   | `SQL/Datastore.py:349` (`sqla.inspect(self._engine)`) | 41 | `test_version_row_at_open` |
   | `SQL/ShardedPool.py:870` (`self._shard_file_table.create(self._engine)`) | 6 | `test_version_row_at_open` |

   That is **105** of 40,874 opened, the prompt's figures exactly. A test run by inheritance (03b's
   `test_one_timestamp_per_write`) is counted under the module that defines the method, since that
   is the file in the stack. The log says how its own wrapper attributes a test.
5. **`origin/main` is 27 commits behind `2255206`**, not 26: 05's own commit came after the
   prompt's measurement. It is 28 behind this note. This changes nothing the agent does.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **The matrix pins the patch releases:** `python-version: "3.12.15"` and `"3.13.16"`, the two
  interpreters this machine tests. `actions/python-versions`' manifest carries both for Ubuntu
  24.04 (checked on 2026-10-09). Step 4's print then shows that CI ran what was tested here, and
  only the operating system and SQLite differ.
- **Record the wheel by its `RECORD`, as well as by its SHA-256.** setuptools writes the build
  time into the zip, so two builds of the same tree differ: two exports of 05's tree gave two wheel
  SHA-256s, but byte-identical `RECORD` files. The log gives:
  - the wheel's name, size, entry count and SHA-256, as the prompt asks;
  - the SHA-256 of its `datastorekit-0.1.0.dist-info/RECORD`;
  - the `Generator:` line of its `WHEEL` file.

  **Probed:** 96,304 bytes, 25 entries; `RECORD` SHA-256
  `a689847ec47869c479304270fe5c4709595c35668136cb1e7f134fedd652330a`, with
  `Generator: setuptools (84.0.0)`. The review rebuilds and compares the `RECORD`.
- **Reinstall `venv/` with its own pip:** `./venv/bin/python -m pip install --no-deps -e .` (pip
  26.2.1 is there; 01 built `venv/` with it). Then `./venv/bin/pip show datastorekit` says
  `0.1.0`, and the log quotes it.
- **Check the README's links.** Each relative link in the new `README.md` names a file that exists
  at the commit.
- **Work in this order, and run the suite after each step that changes a file.**
  1. `pyproject.toml` (§2.1 and §2.4); reinstall `venv/`; the suite there.
  2. The low and high venvs (§2.3); the suite in each, with their versions; §2.6's measurement at
     both ends.
  3. The release check (§2.4), from an export (correction 1).
  4. The workflow (§2.5); its replay; the YAML parse and the matrix check.
  5. The README (§2.7); the names it mentions, each imported; its links.
  6. (a)–(f).
  7. `venv/`'s suite again, both checks, `black --check`, the records.

**The facts, checked by the orchestrator.** Pass them on.

- **The prompt's measurements hold** (§2.2), with the `pyproject.toml` of §2.1 and §2.4 applied to
  a scratch copy of the tree and installed editable:
  - low (`/opt/local/bin/python3.12`): Python 3.12.15, `ray` 2.43.0, `sqlalchemy` 2.0.39, SQLite
    3.53.4: `Ran 444 tests … OK`, no `ResourceWarning`;
  - high (`/opt/local/bin/python3.13`): Python 3.13.16, `ray` 2.55.1, `sqlalchemy` 2.0.46, SQLite
    3.53.4: `Ran 444 tests … OK`;
  - each run takes about 95 seconds.
- **The resolves.** `uv pip compile --only-binary ray` resolves both ends' pins on
  `x86_64-manylinux_2_28` and `aarch64-apple-darwin`. On 3.13, `ray==2.44.1` has no solution on
  either, and `ray==2.45.0` resolves on both.
- **(b), (c) and (d), probed** with `uv pip install --dry-run`:
  - `sqlalchemy==2.0.38` and `sqlalchemy==2.1.4` each give "No solution found", naming
    `datastorekit==0.1.0 depends on sqlalchemy>=2.0.39,<2.1`;
  - `requires-python = ">=3.13"` gives "the current Python version (3.12.15) does not satisfy
    Python>=3.13" on the low venv.

  Each exits 1.
- **The release check, probed** from an export:
  - the wheel holds the 20 `.py` files of the guard's `layer_files()`,
    `datastorekit-0.1.0.dist-info/licenses/LICENSE`, `METADATA`, `WHEEL`, `top_level.txt` and
    `RECORD`;
  - `METADATA` says `Requires-Dist: ray>=2.43` and `Requires-Dist: sqlalchemy<2.1,>=2.0.39`;
  - installed at the high pins and run from a directory outside the repository with `PYTHONPATH`
    unset, every one of the 20 modules imports, `import datastorekit.tests` raises
    `ModuleNotFoundError`, and the tools behave as correction 2 says.
- **(e) and (f), probed** from exports: `exclude = ["datastorekit.t*"]` gives 22 entries, with
  nothing under `tools/` or `tests/`; with no `exclude`, 66 entries, 41 under `tests/`.
- **The child interpreters.** Of the tests that run one:
  - `test_package_imports` sets `PYTHONPATH` to the repository root itself;
  - the three tool modules clear it and change directory.

  So only the second group needs the package installed, which is hazard 1.
- **The Actions.** `actions/checkout` `v7.0.1` and `actions/setup-python` `v7.0.0` are each one's
  latest release. `ds283/DatastoreKit` is public, with default branch `main`, and Actions are
  enabled for all actions.
- **The toolchain.** `venv/` from 01: Python 3.12.15, `ray==2.43.0`, `sqlalchemy==2.0.39`,
  `black==25.1.0`, `PyYAML` 6.0.3, SQLite 3.53.4, with `datastorekit 0.1.0.dev0` installed
  editable.
- **Expected counts.**
  - The suite is **444** before and after, in every venv.
  - `compare_with_source.py` exits 0 with 31 compared, 20 `PORTED` and 10 with no source.
    `compare_ported_tests.py` exits 0 over twenty modules, with one test declared not ported.
  - `black --check datastorekit docs`: "64 files would be left unchanged", before and after.
  - The index is **6**, and **7** after, unless the work opens another issue.
- **Ray.** No Ray process was up at writing (`pgrep -lf 'gcs_server|raylet|ray::'` empty).

**What the review exists to establish.**
- **(E1) The declaration.** `pyproject.toml` is §2.1's and §2.4's, and nothing else.
- **(E2) Both ends.** The 444 pass in fresh venvs at each end, built by the workflow's install,
  and in `venv/`.
- **(E3) The release.** A wheel built from a clean export of the commit holds the layer and its
  tools and nothing of the tests, and works when installed, from outside the repository.
- **(E4) The workflow.** It is §2.5's, with the patch versions, and it parses. Its steps were
  replayed here.
- **(E5) The issue.** §2.6's measurement holds at both ends, and the issue is open with it.
- **(E6) The README.** It is true at the tag: every name it mentions exists, every link resolves,
  and its versions equal `pyproject.toml`'s and the workflow's.
- **(E7) The breakages.** (a)–(f) each fail as recorded.
- **(E8) The records.**

**Conventions.** 04b's note's, unchanged, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff to a tracked file with `git apply --check` and `-R --check` **as
  recorded in the log**, with its trailing context lines;
- read SGK only through `git show` and `git ls-tree`, and never import or run its code;
- use a subdirectory of the session scratchpad, never `/tmp`, for venvs, exports, wheels and probes,
  and put **no scratch `.py` under `datastorekit/`**;
- start no Ray;
- a stop goes to the user;
- check `git log` before committing.

And for this prompt:
- **No push, no tag, and no change to the GitHub repository's settings** (U23). Reading it with
  `gh api` is allowed.
- **No download but PyPI packages into the scratchpad** (U24).

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. Record `git status --short
   --ignored`.
2. **The baseline.** In `venv/`, the suite gives `Ran 444 tests … OK`, and both checks exit 0.
3. **SGK.** `git -C SecondaryGWKit diff --stat 6f7f291 HEAD -- Datastore tools utilities.py
   config/defaults.py config/sharding.py config/datastore.py` is empty.
4. **The remote.** `git ls-remote origin main` is `47d3ab1…`.
5. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`.
6. **The index.** 6 now, and 7 after unless the work opens another issue. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`, and logs 01 and
  04b;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's five corrections and five additions. Correction 1 is
the one most likely to cost time: a wheel built in this checkout carries the test package whatever
`pyproject.toml` says, and the agent could take that for the exclusion failing.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/05-supported-versions-and-ci.md`, in README §5.1's
  form, with the prompt's §4.6 additions.
- **The files it may add or change are the prompt's §6 list, and nothing else**, plus any issue
  the work opens. It must not touch:
  - any file under `datastorekit/`;
  - anything under `docs/` but `OPEN_ISSUES.md`;
  - `PROVENANCE.md`, `CLAUDE.md`, `LICENSE`, `.gitignore` or the campaign README;
  - `build/` or `datastorekit.egg-info/` by hand (correction 1);
  - anything under `orchestrator/`.
- **It pushes nothing, makes no tag, and changes no setting of the GitHub repository.**
- **It edits no client repository, and runs, imports or opens nothing of one.**
- **It downloads nothing but PyPI packages, into the scratchpad.**
- **It starts no Ray.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — eleven checks

Make the review's venvs fresh, in a subdirectory of the scratchpad of their own, not the agent's.

1. **Scope.** `git show --stat <commit>` touches exactly `pyproject.toml`,
   `.github/workflows/tests.yml`, `README.md`, the log, the board, `docs/OPEN_ISSUES.md` and
   `prompts/INDEX.md`. No file under `datastorekit/` or `docs/extraction/`; no wheel, `dist/` or
   scratch file. `git status --short --ignored` lists the same entries as at dispatch.
2. **E1, by reading.** `git show <commit> -- pyproject.toml`: the version, the two dependencies and
   the `exclude` line, and nothing else.
3. **E2, `venv/`.** `./venv/bin/pip show datastorekit` says `0.1.0`. The suite gives `Ran 444 tests …
   OK`. Both checks exit 0 with 04b's counts. `black --check datastorekit docs` (25.1.0) is clean.
4. **E2, both ends, fresh.** Make a low and a high venv by the workflow's install line, with `uv`
   and the matrix's pins, from the commit's tree (`git archive <commit>` into a scratch directory,
   installed editable from there, the suite run from its root). Each gives `Ran 444 tests … OK`.
   Record each venv's versions, and check that they are the log's.
5. **E3, the release.** Export the commit's tree with `git archive <commit>`, build the wheel from
   it, and install it into a fresh high-end venv.
   - The entries are correction 1's 25. The `RECORD`'s SHA-256 is the log's, or, if the build
     backend's version differs, each file's hash in it is.
   - Re-run §2.4's checks from outside the repository with `PYTHONPATH` unset, as correction 2
     reads them.
6. **E4, the workflow, by reading.**
   - The triggers are `push` to `main`, `pull_request` and `workflow_dispatch`.
   - There is one job, `suite`, on `ubuntu-24.04`, with `fail-fast: false` and exactly two matrix
     entries, `low` and `high`, holding 3.12.15 / 2.43.0 / 2.0.39 and 3.13.16 / 2.55.1 / 2.0.46.
   - The steps are §2.5's 1–6, with black on `low` only. The two actions are at `@v7`.
   - `permissions` is `contents: read`. There are no secrets, cache, artefacts or other actions,
     nothing of hazard 6, and nothing that turns warnings into errors (`-W error`,
     `PYTHONWARNINGS`).
   - It parses with `yaml.safe_load`, and the matrix read back from the parse equals the table.
   - The log maps each step to the command that replayed it, and names any step with no local
     counterpart.
7. **E5, the issue.** Run the orchestrator's wrapper (correction 4) on the commit at both ends: 105,
   as 58 / 41 / 6. The log's counts and method agree. The board's §3 entry has the measurement,
   the impact statement and the next step of §2.6; the index has its row.
8. **E6, the README, by reading.** The six parts of §2.7 are all there, and it keeps the opening
   description, the `RayWorkPool` note and the licence.
   - Every name it mentions imports, from the release venv, or is a file that exists at the
     commit. Every relative link resolves.
   - The supported-versions table equals `pyproject.toml` and the matrix, and says that Ray's floor
     on 3.13 is in effect 2.45.0.
   - The install line is CLAUDE.md's form at `v0.1.0`.
   - No code block names a thing that does not exist; no client is written out from scratch.
9. **E7, the breakages.** Replay (a)–(f) as the log records them: (a) in a throwaway venv, (b)–(d)
   as dry runs, (e) and (f) each in its own export. Each fails as recorded. `git status` is clean
   after each.
10. **E8, the records.**
    - The log has every section of README §5.1 and each §4.6 addition, the five corrections and
      the additions, and both `git status --ignored` listings.
    - The board: 05's row, the header, the G2 line in §2 (ready to tag once CI passes; no tag
      made), and the issue in §3.
    - `docs/OPEN_ISSUES.md`: count its rows; the header says 7 and today's date.
    - `prompts/INDEX.md`: the campaign's line.
11. **Nothing left behind.** No Ray process is up. No tag exists (`git tag -l` is empty), and
    `git ls-remote origin` shows `main` at `47d3ab1` and no tag.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 05* paragraph, in the form of
  04b's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README's header, and its §2 status for 05 ("landed, reviewed; awaiting CI for `v0.1.0`");
  - the notes line, with this note marked "used for 05".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Report to the user:**
  - what landed: the range, the exclusion, the workflow and the README;
  - the 444 at both ends and in `venv/`, with the versions, from the review's own venvs;
  - the release check, and correction 1's finding about the checkout's `build/` and
    `datastorekit.egg-info/`, which the user may delete (they are ignored, and nothing needs
    them);
  - the issue opened, with its 105;
  - (a)–(f);
  - **and ask for approval to push** (§5).

## 5. Reaching `v0.1.0` (U23)

Each push and the tag is an outward-facing act. **Ask the user, and wait for a clear yes, before
each.** Approval of one is not approval of the next.

**Why 05's commit goes alone first.** A push to `main` runs CI on the pushed head only. If `main` is
pushed whole after the review, CI runs on the review's follow-up commit, not on 05's, and U23 asks
for CI on 05's commit. The review's commit changes only `prompts/`, but the tag must sit on a
commit whose own CI is green.

1. **Push 05's commit as `main`:** `git push origin <05's SHA>:refs/heads/main`. It fast-forwards
   from `47d3ab1`. The workflow runs on 05's commit, both ends.
2. **Read the run** once it has finished: `gh run list --workflow tests.yml --commit <05's SHA>`
   and `gh run view <id> --log`. Do not poll in a loop; ask the user to say when it has finished,
   or check once when they return. From each job's log, record:
   - step 4's `sys.version`, `ray`, `sqlalchemy` and SQLite versions (hazard 2);
   - the suite's verdict line;
   - black's line on `low`.
3. **If either end fails**, stop. No tag. Record the failure on the board's §3 with the job's log
   lines, and tell the user that a fix prompt is needed. The fix prompt lands, is reviewed, and its
   commit goes through steps 1–2 in turn, and the tag goes on it, not on 05's.
4. **If both pass**, with the user's approval:
   - `git tag -a v0.1.0 <05's SHA> -m "datastorekit 0.1.0: SecondaryGWKit's Datastore / ShardedPool layer at 6f7f291, extracted"`;
   - `git push origin v0.1.0`;
   - check that `git ls-remote origin refs/tags/v0.1.0^{}` is 05's SHA.
5. **Then push the rest of `main`** (`git push origin main`), with approval. It holds the review
   and the records, and runs CI again on its head, which changes nothing.
6. **Record it**, in a commit of its own, before step 5's push or as part of it:
   - the board's G2 line: `v0.1.0` made on 05's SHA, with the run's URL and both ends' SQLite
     versions;
   - the review paragraph's last line;
   - README §2's status for 05;
   - `prompts/INDEX.md`.

   Hazard 2's answer is recorded there. A SQLite older than 3.35 would mean `ALTER TABLE … DROP
   COLUMN` is unavailable, and the tests that use it would already have failed in step 2.

**Hand on to 06's author:**
- `v0.1.0` is on 05's commit, and rule 8 lifts after it. 06 adds behaviour only behind a
  `register()` key.
- CI runs the suite at both ends on every push, so 06's prompt names the workflow run of its
  commit in its acceptance.
- Wheels are built from a clean export (correction 1). 06's `v0.2.0` follows §5's order.
- `shard_key_audit` has no `--help` (correction 2), and the prose rewrite after 05 may add one,
  as behaviour, in a prompt that says so.
