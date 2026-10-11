# Orchestrator — prompt 02, release `v0.2.2`

Read [`../README.md`](../README.md) first: §1, §2, §4, §5 (every rule), §6.1 (U23, U28, U37) and
§6.2 (U3 and U4), and §7. Then read [`prompt-01b.md`](prompt-01b.md), whose "Conventions" and
§4–§5 this note keeps unless it says otherwise, and the extraction campaign's
[`prompt-10.md`](../../extraction/orchestrator/prompt-10.md), the note for the release this one
repeats: its §0, and its §5, which this note's §5 follows. Then read this board's reviews of 01 and
01b.

**You do not write code.** You may:
- run the suite, the port check, `black --check` and the guards;
- make venvs in the session scratchpad with `uv … --offline`, from the cache the extraction
  campaign filled, and nothing else: **no download**;
- export the tree with `git archive` into the scratchpad, and build wheels, run probes and replay
  breakages there, never in this checkout and never committing one;
- **start no Ray.** No code changes, so the smoke script is not run (the prompt's hazard 7);
- reach the network only for one `git ls-remote origin` at dispatch and one at the review, and for
  the pushes, the tag and the CI read of §5, each with the user's approval;
- read the three clients only through `git -C <client> rev-parse|status|show|grep`;
- fix small residue in a follow-up commit of your own (§4).

**The prompt:** [`02-release-v0.2.2.md`](../02-release-v0.2.2.md)
**Closes:** nothing · **Narrows:** nothing · **Changes:** nothing · **Opens:** only what the work
finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- 01 landed (`ac50a8a`), was reviewed (`049fa1a`) and passed CI there (`168ecd0`). 01b landed
  (`f024fc6`), was reviewed (`2fd3ba2`) and passed CI there,
  [run 38103745544](https://github.com/ds283/DatastoreKit/actions/runs/38103745544), recorded at
  `a4290de`. 02 was re-measured against `a4290de` and amended (`ce2070b`).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- `git diff --stat f024fc6 HEAD -- datastorekit docs pyproject.toml README.md PROVENANCE.md
  .github` is empty: everything 02 reads or edits, but the extraction board, is 01b's tree.
- `origin/main` is `2fd3ba2` (`git ls-remote origin`, 2026-10-11), an ancestor of `main`, which is
  ahead of it by `a4290de`, `ce2070b` and this note. The tags are `v0.1.0` (`0ece4aa` → `68db557`),
  `v0.2.0` (`9eaf542` → `240028e`) and `v0.2.1` (`0ba2e4d` → `33778b0`), here and on `origin`, and
  no other.
- The clients' `HEAD`s: SGK `b510bc9` (branch `handover-remedial`, one untracked entry,
  `prompts/dk-and-rpk-migration/`, which 01b's review found and which is none of this campaign's),
  CPBH `52142d7` (`main`, 23 untracked entries), SI `7bb3efd` (`main`, clean).
- This board's §3 holds no issue, and the index is **4** (0 on this repository's boards, 4
  inherited). It stays 4 unless the work opens an issue.
- One prompt at a time in this checkout. 02 is the campaign's last.

## 0. What makes this prompt unusual

**No line of code changes, so the suite cannot catch a bad edit.** It passes whatever the
documents say. What stands in for it, as at extraction prompt 10:
- the release check, from a clean export, which alone sees `0.2.2` and the fix behind it;
- hazard 1's `git diff`, which must show `+` lines only under `docs/adoption/`;
- reading: every statement an addendum makes is true of `v0.2.2`, every statement it supersedes is
  named by `path:line`, and every name and link resolves.

**The release carries two prompts, and must not overstate the second.** Against `v0.2.1`, 01 is
the fix; 01b keeps 01's kill from starting Ray, and changes nothing a client sees against `v0.2.1`,
which never killed on a close (§1.1). The README and the addenda say 01b's guard as a property the
release keeps, not as a second fix. Breakage (c) is the check that sees a version number with no
fix behind it, and it must see 01b's helper as well as 01's.

**The acceptance finishes elsewhere.** `v0.2.2` is made on 02's commit only once CI has passed
there at both ends (§5). It is the release every client adopts (U3, amending U37), so it is the
commit their pins will name.

**The push carries more than 02.** `origin/main` is `2fd3ba2`. Pushing 02's commit as `main`
fast-forwards over `a4290de`, `ce2070b`, this note and 02 itself. None of them but 02 changes a
file CI reads, so the tree CI tests is 02's.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-11 at `ce2070b` (whose
`datastorekit/`, `docs/`, `README.md`, `PROVENANCE.md` and `pyproject.toml` are `f024fc6`'s), in
`venv/`, in offline scratch venvs and exports at the high end, and with wheels built offline from
exports. Pass them on. Corrections 1 and 2 change what the agent does or writes, and are
STRUCTURALLY REQUIRED. Correction 3 corrects what the prompt states; the log records it as found.

1. **Hazard 6's reinstall cannot run.** `uv pip install --offline --no-deps --no-build-isolation
   --python venv/bin/python -e .` builds in `venv/` itself, and `venv/` has no `setuptools`
   (`import setuptools` raises `ModuleNotFoundError`). Probed on a scratch `python3.12 -m venv`,
   which has none either, against an export at `0.2.2`: uv refuses, and suggests installing
   `setuptools` into the environment. That would change `venv/`, which this prompt does not do.
   **Use extraction prompt 10's form, `uv pip install --offline --no-deps --python
   venv/bin/python -e .`, from the repository root, without `--no-build-isolation`**: uv builds
   in an isolated environment from its cache, offline. Probed the same way: it installs
   `datastorekit==0.2.2` editable, `pip show` says `Version: 0.2.2`, and it writes
   `datastorekit.egg-info/` at the export's root, which is deleted afterwards (log 10, correction
   2). The high-end scratch venv of §4.1 has `setuptools`, so `--no-build-isolation` is right
   there.
2. **The italic line moves every later line of each adoption file, and the `v0.2.1` addendum's
   citations with it.** Extraction prompt 10's italic line is 4 lines and a blank, and each new
   one will be about the same. Each `v0.2.1` addendum gives its supersessions as "this file's as
   committed with this addendum", that is at `33778b0`; after 02's italic line every one of them
   past the head (all but README `:3`, SGK `:6`, CPBH `:6` and SI `:5`) points k lines early. They
   are not rewritten (rule 6). **Each `v0.2.2` addendum says so in one sentence beside its own
   table**, as each `v0.2.1` addendum did for 07a's file (`docs/adoption/README.md:257`,
   `secondarygwkit.md:425`, `champbh.md:447`, `stochasticinstantons.md:417`):
   in the file as extraction prompt 10 left it (`33778b0`), every line after the italic line is k
   lines earlier, so the `v0.2.1` addendum's citations are read at `33778b0`, or plus k here. Its
   own table cites lines as committed with it. The agent states k for each file, and the review
   checks it.
3. **The `RECORD` comparison under breakage (c).** The prompt's (c) reads well, and the facts
   hold: a wheel from `git archive v0.2.1` with only the version set to `0.2.2` says `Version:
   0.2.2`, and every one of its 20 `RECORD` lines under `datastorekit/` equals `v0.2.1`'s wheel's;
   installed at the high pins, `ShardedPool` has no `_kill_actors` and the module has no
   `_ray_is_running`. Nothing to change; the agent records the 20 lines compared, not only "none
   differ".

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **Work in this order:**
  1. the baseline: 494 in `venv/`, and at the high end from a fresh venv with an export of `HEAD`
     installed editable; the port check; `black --check datastorekit docs`, 72 files; the clients'
     `HEAD`s and statuses; §1.1's measure (hazard 4);
  2. `pyproject.toml`; `venv/`'s reinstall (correction 1), the `egg-info` removed; the suite;
  3. `README.md` and `PROVENANCE.md`;
  4. the four addenda and italic lines; then hazard 1's `git diff`;
  5. the extraction board's gates;
  6. the release check; the high end;
  7. (a)–(c);
  8. the documents' check (§4.4) and the name-and-link check (hazard 2);
  9. `venv/`'s suite again, the port check, `black`, the clients again, the records.
- **Give each addendum's supersessions as a table** (`path:line`, the statement in brief, what
  replaces it), as the `v0.2.1` addenda do. The log repeats the four tables, with any statement
  found that the prompt's table does not name.
- **Placement.** In each checklist the `v0.2.1` addendum is preceded by a `---` rule
  (`secondarygwkit.md:361`) and followed by one before the appendix (`:439`). The `v0.2.2`
  addendum goes after the `v0.2.1` addendum's table and before that second rule, with a `---` of
  its own above it. In the README it goes at the end, after a `---`. Its heading is `## Addendum:
  v0.2.2 (actor-names prompt 02, <date>)`; by GitHub's rule the anchor is
  `#addendum-v022-actor-names-prompt-02-<yyyy-mm-dd>`.
- **`PROVENANCE.md`'s new section is a `###`**, as `:89` and `:118` are, under "After `v0.1.0`".
- **The contract's anchors**, by GitHub's rule (lower-case; drop backticks and punctuation other
  than hyphens; spaces to hyphens): §9.3 `#93-actor-names-prompt-01`, §9.4
  `#94-actor-names-prompt-01b` (`docs/client-contract.md:301`, `:317`). No file links them yet.
  From `docs/adoption/` the path is `../client-contract.md#…`.
- **The gate titles**, exactly: G2 "SGK adopted `v0.2.2` (U37; `actor-names` U3), fingerprint
  reproduced"; G3 "CPBH adopted `v0.2.2` (U37; `actor-names` U3)"; G4 "SI adopted `v0.2.2` (U37;
  `actor-names` U3)". Each row's status cell gains one dated italic sentence, in the form of the
  `v0.2.1` "ready to be tagged" sentences, linking its client's new addendum by anchor. Nothing
  else on that board changes, its header included.
- **Keep the name-and-link check as a scratch script**, never committed, as log 10 did: every
  relative link and anchor in `README.md`, `PROVENANCE.md`, the four adoption files and the
  extraction board's §2, each file resolved and each anchor found among its target's headings by
  GitHub's rule; every dotted `datastorekit.` name imported in `venv/`.
- **Build (a)'s, (b)'s and (c)'s wheels from their own exports**, each with the prompt's change
  and only that. Record (a) and (b) as diffs to `pyproject.toml` that `git apply --check` and `-R
  --check` accept against an export of the commit; (c) is the version line applied to an export of
  `v0.2.1`, and is recorded so that it applies there.

**The facts, checked by the orchestrator.** Pass them on.

- **The suite** at `ce2070b`: `Ran 494 tests … OK` in `venv/` (104 s) and at the high end from a
  fresh offline venv with an export installed editable (101 s), 0 `ResourceWarning` lines at each.
  The port check exits 0 ("20 module(s) … 1 test(s) declared not ported"); `black --check
  datastorekit docs` leaves 72 files unchanged.
- **§1.1 reproduces**, read through `git` at SGK `b510bc9`, CPBH `52142d7` and SI `7bb3efd`:
  - step 1, the grep, gives exactly the prompt's lines: SGK's 7 constructions, the two
    `test_reader_read_only.py` lines (`:91`, `:104`) and two `super().__exit__`; CPBH's 3 and two
    `super().__exit__`; SI's 4 and one. No `ray.kill` or `ray.get_actor`;
  - step 2, an `ast` read of the 14 files: each construction is a `with ShardedPool(…) as pool:`
    and the file's only `ShardedPool(` call; 13 are the last statement of their block, and SI's
    `tests/conftest.py:57` is followed by one statement that does not name `pool`. 14 in all.
  - SGK's stand-in: `importlib.import_module` at `Datastore/tests/standin_pool.py:43`, `active()`
    at `:231-247` patching `ray.get` (`:233`), the actor classes and `random`, not `ray.kill`;
    `test_quadsource_policy_main.py`'s `tearDownModule` asserts `not ray.is_initialized()`
    (`:430-431`); the checklist's citation `secondarygwkit.md:258-260` holds.
  - SGK's actor names at `Datastore/SQL/ShardedPool.py:294`, `:305` and `:544`, at both
    `6f7f291` and `b510bc9`, as §2.3 says.
- **The package.** `git diff --numstat 33778b0 f024fc6 -- datastorekit`: `SQL/ShardedPool.py`
  64/0 (01's 48 and 01b's 16), `tests/standin_pool.py` 70/2, the new test module 262/0. The cited
  lines hold: `_ray_is_running` `:47-55`, the guard `:446-447`. Only `pyproject.toml:7` carries the
  version.
- **§1.2 reproduces.** From a `git archive` of `ce2070b` with only `version = "0.2.2"`, `uv build
  --offline --wheel` gives `datastorekit-0.2.2-py3-none-any.whl`, 98,811 bytes (the bytes are not
  reproducible; compare `RECORD` lines, not hashes):
  - 25 entries, none under `datastorekit/tests/`; `datastorekit-0.2.2.dist-info/licenses/LICENSE`;
  - `METADATA`: `Version: 0.2.2`, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43`,
    `Requires-Dist: sqlalchemy<2.1,>=2.0.39`;
  - installed offline with `ray==2.55.1` and `sqlalchemy==2.0.46` into a Python 3.13.16 venv and
    run from a directory outside the repository with `PYTHONPATH` unset and `python -I`: the
    package and its 19 submodules import from `site-packages`; the metadata version is `0.2.2`;
    `ShardedPool._kill_actors` exists, `__exit__` has 01's docstring, and `_ray_is_running`'s last
    line is `return ray.is_initialized()`; `import datastorekit.tests` raises
    `ModuleNotFoundError`; `python -m datastorekit.tools.sharded_store --help` exits 0;
  - against `git archive v0.2.1`'s wheel (97,849 bytes): 20 `RECORD` lines under `datastorekit/`
    each side, the same paths, and only `SQL/ShardedPool.py`'s differs.
- **The breakages**, each from its own export, at the high pins:

  | | Change | Measured |
  |---|---|---|
  | (a) | version left at `0.2.1` | `datastorekit-0.2.1-py3-none-any.whl`; the installed metadata version is `0.2.1` |
  | (b) | `exclude = ["datastorekit.tests", "datastorekit.tests.*"]` deleted (`pyproject.toml:17`) | 72 entries, 47 under `datastorekit/tests/`; `import datastorekit.tests` succeeds from `site-packages` |
  | (c) | `v0.2.1`'s tree at `0.2.2` | `Version: 0.2.2`; all 20 `RECORD` lines equal `v0.2.1`'s; no `_kill_actors`, no `_ray_is_running` |

- **The line numbers the prompt cites hold at `ce2070b`**: `README.md:10-17`, `:59`, `:62-63`,
  `:93-94`; `PROVENANCE.md:118` (the file is 158 lines, and that section is its last); the italic
  lines `docs/adoption/README.md:7-10`, `secondarygwkit.md:16-19`, `champbh.md:17-20`,
  `stochasticinstantons.md:15-18`; the appendices `secondarygwkit.md:441`, `champbh.md:459`,
  `stochasticinstantons.md:429`; the README addendum ending the file at `:268`; contract §9.3 and
  §9.4 at `:301` and `:317`. The extraction board's G2–G4 are `prompts/extraction/IMPLEMENTATION_STATE.md:1537-1539`.
- **The toolchain.** `venv/`: Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39, SQLite 3.53.4,
  `black` 25.1.0, `datastorekit 0.2.1` editable from this checkout, no `setuptools`. `uv` 0.12.20.
  The high end, `uv venv --offline -p /opt/local/bin/python3.13`: 3.13.16, 2.55.1, 2.0.46, SQLite
  3.53.4.
- **Expected counts.**
  - The suite: **494**, before and after, at both ends; 0 `ResourceWarning` lines in `venv/`, 0
    or 4 at the high end (timing).
  - `compare_ported_tests.py`: exit 0, "20 module(s) … 1 test(s) declared not ported".
  - `black --check datastorekit docs`: **72** files, before and after.
  - The index: **4**, unchanged unless the work opens an issue.
- **Ray.** No Ray process; `RAY_ADDRESS` and `RAY_ENABLE_AUTO_CONNECT` unset; no
  `/tmp/ray/ray_current_cluster`. Nothing in this prompt calls one of Ray's auto-init APIs: the
  release probes import the pool's module and read attributes only.

**What the review exists to establish.**
- **(E1) Scope.** Only the prompt's §7 files change. Nothing under `datastorekit/`, and not the
  contract, the verification document, `docs/extraction/` or the workflow.
- **(E2) The release.** A wheel from a clean export of the commit is `0.2.2`, holds 01's and 01b's
  code and no tests, and behaves as §1.2 says from outside the repository.
- **(E3) The documents.** `pyproject.toml`, `README.md` and `PROVENANCE.md` as §2.1–§2.3 say; 01b
  stated as a property kept, not a second fix; nothing says `v0.2.2` is tagged; every name and link
  resolves.
- **(E4) The addenda.** Each additive, dated and placed as the additions say; each states its pin,
  what changed for its client, what it supersedes by `path:line`, and the line shift (correction
  2), true at the file.
- **(E5) Both ends.** 494 in `venv/` (now `0.2.2`) and at the high end.
- **(E6) The breakages.** (a)–(c) fail as recorded.
- **(E7) The records**, and the extraction board's gates.

**Conventions.** 01b's note's, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff **as recorded in the log** with `git apply --check` and `-R --check`
  against a scratch export;
- read a client only through `git`, and never import or run its code;
- use a subdirectory of the session scratchpad, never `/tmp`, for venvs, exports, wheels and
  probes; put no scratch `.py` under `datastorekit/` or `docs/`;
- a stop goes to the user;
- check `git log` before committing.

And for this prompt:
- **Start no Ray.** Nothing calls `ray.init`, `ray.kill`, `ray.get` or any other of Ray's auto-init
  APIs outside the suite.
- **No download of any kind.** Every venv and build is `--offline`; `venv/`'s reinstall is
  correction 1's.
- **Nothing is built in the checkout** but `venv/`'s editable reinstall, whose `egg-info` is
  removed.
- **No push, no tag, and no change to the GitHub repository's settings.**

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. Record `git status --short
   --ignored` (at writing: `.idea/`, `venv/` and six `__pycache__/` directories, one of them
   `docs/extraction/__pycache__/`).
2. **The baseline.** In `venv/`, `Ran 494 tests … OK` with no `ResourceWarning`; the port check
   exits 0; `black --check datastorekit docs` leaves 72 files unchanged; `pip show datastorekit`
   says `0.2.1`.
3. **The clients.** Each `HEAD` and `git status --short` as the gate says.
4. **The remote.** `git ls-remote origin`: `main` at `2fd3ba2…` and the three tags as the gate
   says.
5. **Ray.** No Ray process (`pgrep -lf 'gcs_server|raylet|ray::'` empty); `RAY_ADDRESS` and
   `RAY_ENABLE_AUTO_CONNECT` unset.
6. **The index.** 4 now, and 4 after unless the work opens an issue. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, this board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `PROVENANCE.md`, logs 01 and 01b (§1 and §8 of each), extraction prompt 10 and its log;
- `HEAD`, the clients' `HEAD`s and statuses, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's three corrections and its additions. Correction 1 is the
one that would stop it: the prompt's own reinstall fails in `venv/`. Correction 2 is the one a
reader of the `v0.2.1` addenda would otherwise be misled by.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/02-release-v0.2.2.md`, in README §5.1's form, with
  the prompt's §5 item 6 additions.
- **The files it may change are the prompt's §7 list, and nothing else.** It must not touch:
  - anything under `datastorekit/`;
  - `docs/client-contract.md`, `docs/extraction-verification.md`, `docs/extraction/` or the
    workflow;
  - `CLAUDE.md`, `LICENSE` or `.gitignore`;
  - on the extraction board, anything but G2–G4's rows;
  - anything under `orchestrator/`.
- **Under `docs/adoption/` it adds lines only.**
- **It writes nothing in any client repository, and runs, imports or opens nothing of one.**
- **It downloads nothing, and starts no Ray.**
- **It pushes nothing, makes no tag, and changes no setting of the GitHub repository.**
- **Stop and ask** on any of the prompt's §6 conditions.

## 3. The review — ten checks

Make the review's venvs, exports and wheels fresh, offline, in a subdirectory of the scratchpad of
their own, not the agent's.

1. **Scope (E1).** `git show --stat <commit>` touches only `pyproject.toml`, `README.md`,
   `PROVENANCE.md`, the four files under `docs/adoption/`, the extraction board, the log, this
   board, the campaign README, `prompts/INDEX.md`, and `docs/OPEN_ISSUES.md` only if an issue is
   opened. `git diff <parent> <commit> -- datastorekit docs/client-contract.md
   docs/extraction-verification.md docs/extraction .github CLAUDE.md` is empty. No wheel,
   `dist/`, `build/`, `*.egg-info` or scratch file; `git status --short --ignored` as at dispatch.
   Each client's `HEAD` and status as at dispatch.
2. **Additive (E1, E4).** `git diff <parent> <commit> -- docs/adoption/` has no `-` line.
   `pyproject.toml`'s diff is the version line alone. The extraction board's diff is G2–G4's three
   rows alone, each keeping every sentence it had.
3. **The release (E2).** From `git archive <commit>`, build the wheel offline and install it into a
   fresh high-end venv, offline. Check §1.2's facts as the facts above give them: 25 entries, none
   under `tests/`; the licence; `METADATA`; from outside the repository, `0.2.2`, `_kill_actors`,
   `_ray_is_running`, `datastorekit.tests` refused, `sharded_store --help`. The `RECORD`
   comparison with the review's own `v0.2.1` wheel: only `SQL/ShardedPool.py`'s line differs.
   Compare the wheel's file list with the log's.
4. **`README.md` and `PROVENANCE.md`, by reading (E3).**
   - Status: a `v0.2.2` paragraph above `v0.2.1`'s, which is unchanged. It names 01's fix and its
     three consequences, says two open pools still collide, says closing a pool never starts Ray
     as a property kept (not a fix against `v0.2.1`), says no API, nothing written and no message
     changes, and links §9.3 and §9.4 by anchor.
   - The pin is `v0.2.2`; the sentence replacing `:62-63` says the three earlier tags remain, none
     moved or deleted, and every client adopts `v0.2.2`. Nothing says `v0.2.2` is tagged.
   - "Using it"'s §9 item names `v0.2.2`'s fix and that a close never starts Ray.
   - `PROVENANCE.md`'s new `###` section follows "Prompts 08a, 08b and 09", and says what the
     prompt's §2.3 lists; SGK's three citations read true at `6f7f291` and `b510bc9`. Nothing above
     it changes.
5. **The addenda, by reading (E4).** For each of the four files:
   - the italic line is after extraction prompt 10's; the addendum is placed as the additions say,
     unnumbered, dated, and names `actor-names` prompt 02;
   - it gives the pin, and says the client adopts `v0.2.2` (`actor-names` U3, amending U37);
   - what it says changed for its client is the prompt's row, true of `f024fc6`'s package, and
     links §9.3 or §9.4;
   - each superseded statement is cited by a `path:line` that holds in the file as committed; the
     italic line moved them, so check each against the committed file;
   - correction 2's sentence is there, and its k is the number of lines the italic line added;
   - SGK's addendum states the stand-in as a fact, with no instruction to SGK.
6. **Names and links, by running (E3, E4).** The review's own extraction of every relative link
   and anchor in the six documents and the extraction board's §2: each file exists, and each anchor
   is a heading by GitHub's rule. Every dotted `datastorekit.` name imports in the review's release
   venv. The list matches the log's.
7. **Both ends (E5).** In `venv/`: `pip show datastorekit` says `0.2.2`; `Ran 494 tests … OK`; no
   `datastorekit.egg-info/` at the root. In a fresh high-end venv with `git archive <commit>`
   installed editable: `Ran 494 tests … OK`, with the `ResourceWarning` lines counted (0 or 4). The
   port check exits 0. `black --check datastorekit docs` leaves 72 files unchanged.
8. **The breakages (E6).** Replay (a)–(c) as the log records them, each in its own export, against
   the facts' table. (c) must show all 20 `RECORD` lines equal to `v0.2.1`'s, and neither name.
9. **The records (E7).**
   - The log: every section of README §5.1, with the release check, the documents' check (§4.4),
     every name and link, §1.1's measure re-run, (a)–(c), the clients at both ends, the three
     corrections and the additions, and each addendum's supersession table.
   - The extraction board: G2–G4 as the additions say; the rest unchanged.
   - This board: 02's row (landed, commit, log) and the header. The README's header and §2 row;
     `prompts/INDEX.md`'s line. `docs/OPEN_ISSUES.md` unchanged at 4, or as opened.
10. **Nothing left behind.** No Ray process. `git tag -l` is the three tags, and `origin` is
    unchanged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 02* paragraph, in the form of
  01b's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on this board, the extraction board, the log, the README and
    `prompts/INDEX.md`;
  - "reviewed; awaiting CI for `v0.2.2`" for 02 in this board's header and row, README §2 and
    `prompts/INDEX.md`;
  - the notes line, with this note marked "used for 02".
- Anything the review finds that is not residue is opened on this board's §3 and in the index.
  **An issue open against 02's commit is a stop for the tag**: tell the user, and nothing in §5
  runs until they decide.
- **Report to the user:**
  - what landed: `0.2.2`, the README, `PROVENANCE.md`, the four addenda and the gates;
  - the release check and its `RECORD` comparison, and the 494 at both ends, from the review's own
    venvs;
  - §1.1's measure, re-run;
  - (a)–(c);
  - that the push carries `a4290de`, `ce2070b` and this note with 02 (§0);
  - **and ask for approval to push 02's commit** (§5).

## 5. Reaching `v0.2.2`

Extraction prompt 10's note §5, with `v0.2.2` for `v0.2.1`, 02's commit for 10's and `2fd3ba2` for
`102f225`. Each push and the tag is an outward-facing act: **ask the user, and wait for a clear
yes, before each.** Approval of one is not approval of the next.

1. **Push 02's commit as `main`:** `git push origin <02's SHA>:refs/heads/main`. It fast-forwards
   from `2fd3ba2`. The workflow runs on 02's commit at both ends; the smoke script is not
   collected, so CI starts no Ray.
2. **Read the run** once it has finished: `gh run list --workflow tests.yml --commit <02's SHA>`
   and `gh run view <id> --log`. Do not poll: ask the user to say when it has finished, or check
   once when they return. From each job's log, record the versions it prints (SQLite's among
   them), the suite's verdict (`Ran 494 tests … OK`) and black's line on `low`.
3. **If either end fails**, stop. No tag. Record the failure on this board's §3 with the job's log
   lines, open it in the index, and tell the user that a fix prompt is needed. The tag goes on the
   fix's commit once its CI passes.
4. **If both pass**, with the user's approval:
   - `git tag -a v0.2.2 <02's SHA> -m "datastorekit 0.2.2: a closed pool, and a refused open, release their Ray actors' names; closing a pool never starts Ray"`;
   - `git push origin v0.2.2`;
   - check that `git ls-remote origin refs/tags/v0.2.2^{}` is 02's SHA.
5. **Record it, and close the campaign** (the prompt's §8), in a records commit of its own:
   - the extraction board's G2, G3 and G4: one dated italic sentence each, in the form of the
     `v0.2.1` "is made" sentences: `v0.2.2` made, annotated, on 02's SHA, the tag object, the run's
     URL and both ends' versions and counts, and that the client may now adopt it;
   - this board: the review paragraph's last line, 02's row, and the header: **CLOSED**;
   - the campaign README's header and §2 row, and `prompts/INDEX.md`'s line: closed, with the
     tag; the index's §1.3 heading as campaign closed, the count unchanged;
   - then **push the rest of `main`** (`git push origin main`), with approval.

**Hand on.** `v0.2.2` is on 02's commit once §5 has run. Every client adopts it in place of
`v0.2.1` (U3), each in a campaign of its own, in its own repository; G2–G4 are recorded on the
extraction board as they hold. No campaign of this repository is open after this one.
