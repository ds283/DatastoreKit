# Prompt 02 — release `v0.2.2`

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 01 landed (`ac50a8a`) and was reviewed (`049fa1a`). CI passed on `049fa1a` at both ends, recorded
  at `168ecd0`.
- U3 is taken (README §6.2): `v0.2.2`, adopted by every client in place of `v0.2.1`.
- `git status` is clean in this repository, and `origin/main` is an ancestor of `main`.
- This board's §3 holds no issue, and `docs/OPEN_ISSUES.md` counts 4, all inherited.

**Closes:** nothing. **Narrows:** nothing. **Changes:** nothing. **Opens:** only what the work
finds.

**Recommended model:** **Opus.**
- No line of code changes. The work is three short edits, four dated addenda and the gates.
- Each addendum must say exactly what changed for its client between `v0.2.1` and `v0.2.2`, no
  more. It must leave the text it extends as it was written (`CLAUDE.md` rule 6), and that includes
  extraction prompt 10's `v0.2.1` addendum.
- The release check and both ends of the suite are run as extraction prompt 10 ran them, offline.

**Read first:**

1. [`README.md`](README.md): §1, §2, §4, §5 (rules 4, 5, 9 and 10), §6 (U3, and the inherited
   U23, U28 and U37) and §7.
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`, above all "Releases".
3. This board's review of 01, and log 01 (`logs/01-a-closed-pool-releases-its-actor-names.md`), §1
   and §8.
4. Extraction prompt 10 (`../extraction/10-release-v0.2.1.md`) and its log
   (`../extraction/logs/10-release-v0.2.1.md`). 02 is that prompt again, for one fix. Their
   release check, their addenda's form and their breakages are this prompt's.
5. The files 02 changes, as they stand: `pyproject.toml`, `README.md`, `PROVENANCE.md`,
   `docs/adoption/README.md` and the three checklists. In each checklist, read extraction prompt 10's
   `v0.2.1` addendum, which 02's follows.
6. `docs/client-contract.md` §9.3, which 02 points at and does not change.

Facts below are at `168ecd0`, whose `datastorekit/` is `ac50a8a`'s, measured on 2026-10-10.

---

## 1. What is wanted

02 makes the package ready to be released as **`v0.2.2`** (U3). Every client adopts it in place of
`v0.2.1`. After it:

- `pyproject.toml` says `0.2.2`;
- `README.md` and `PROVENANCE.md` describe `v0.2.2`;
- `docs/adoption/` carries a dated addendum, in its README and in each checklist, giving the new
  pin and what changed for that client since `v0.2.1`;
- the extraction board's gates G2–G4 say that each client adopts `v0.2.2`, and that the tag waits
  for CI.

**No line of code changes.** Nothing under `datastorekit/` is touched, and the suite stays at
**492**.

**02 makes no tag and pushes nothing** (U23, U28; README §5 rule 9). After its review, its commit
is pushed as `main`. `v0.2.2` is made on it, annotated, only once CI passes there at both ends, as
`v0.2.1` was. If CI fails, a fix prompt lands first, and no tag is ever made on a commit whose CI
is red. The tag is not this prompt's work.

### 1.1 What changed since `v0.2.1`, measured

One prompt changed the package after `v0.2.1` (`33778b0`): `actor-names` 01, `ac50a8a`. It closed
`[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]`.

- **In the wheel, only `SQL/ShardedPool.py` changed.** It gained 48 lines and lost none
  (`git diff --stat 33778b0 ac50a8a -- datastorekit`). Two wheels built offline, one from
  `git archive v0.2.1` and one from `168ecd0` with only the version changed, have the same 20
  `RECORD` lines under `datastorekit/` but `SQL/ShardedPool.py`'s.
- **Outside the wheel**, `datastorekit/tests/standin_pool.py` changed and
  `datastorekit/tests/test_closed_pool_releases_its_names.py` is new (6 tests: 486 → 492).
  `docs/extraction/ray_smoke_run.py`, the contract's §9.3 and verification §4.6 changed too.

**What a client sees.** Nothing a client supplies changes. No API is added or removed. Nothing the
layer writes changes, and no message, refusal or exception of the layer's changes (contract §9.3).
Four behaviours differ:
- **a closed pool releases its actors' names at once.** `__exit__` kills each shard actor and the
  broker (`ray.kill(handle, no_restart=True)`). A store can then be reopened in the same Ray
  session while the closed pool object is still referenced. At `v0.2.1` that reopen was refused by
  Ray until the pool was collected;
- **a closed pool's handles are dead.** A call through `pool._shards` or `pool._broker` after
  `__exit__` fails, and so does a pool method that reaches an actor. At `v0.2.1` the actors lived
  on, with their engines disposed;
- **a second `__exit__` does nothing;**
- **a refused open releases the names it took**, even while its exception is held.

**Unchanged:** two pools open at once in one Ray session still collide, since the names are fixed
(U1). The second open is refused by Ray when it creates its broker, with `ValueError` at Ray
2.43.0 and `ray.exceptions.ActorAlreadyExistsError` at 2.55.1.

**What the clients do with them**, read through `git` only, at the checklists' commits (SGK
`b510bc9`, CPBH `52142d7`, SI `7bb3efd`; each is that client's `HEAD` at writing). The planner's
measure:
1. `git -C <client> grep -n -E 'ShardedPool\(|\.__exit__\(|ray\.kill|ray\.get_actor' <commit> --
   '*.py' ':!Datastore/**' ':!prompts/**' ':!docs/**'`;
2. for each construction, an `ast` read of the file (`git show <commit>:<path>`): is it a `with`
   block, which statements follow it in the same block, and does any later statement name its
   `as` variable?

The results:
- **Every construction is a `with ShardedPool(…) as pool:` block.** Each is the last statement of
  its own block, or is followed by nothing that names `pool`. There are 14:
  - SGK 7: `main.py:4164`, and `extract_GkSource_data.py:932`, `extract_GkWKB_data.py:505`,
    `extract_Gk_data.py:453`, `extract_QuadSourceIntegral_data.py:1294`, `extract_TkWKB_data.py:493`
    and `extract_tensor_source_data.py:421`;
  - CPBH 3: `main.py:1338`, `plot_ScalarModel.py:1577` and `plot_by_beta.py:1007`;
  - SI 4: `main.py:1345`, `plot_GradientCoupledSolutions.py:974`, `plot_InstantonSolutions.py:1207`
    and `tests/conftest.py:57`. The fixture yields the pool inside the block, then calls
    `ray.shutdown()` after it.
- **No client calls a pool's `__exit__` directly** (the five `super().__exit__` hits, two each in
  SGK and CPBH and one in SI, are `Quadrature/` classes, not pools), **or `ray.kill` or
  `ray.get_actor`**. As README §0.1
  measured, none reads `_shards` or `_broker`.
- **So no client uses a closed pool**, and none meets a dead handle. Each opens one pool per
  process (SI's conftest one per pytest session), so none met the defect either. For each client
  the fix is latent.
- **SGK's own test stand-in.** SGK keeps `Datastore/tests/standin_pool.py` (its checklist
  `docs/adoption/secondarygwkit.md:258-260`, for `ComputeTargets/tests/test_quadsource_policy_main.py`).
  It stands in `ray.get` and the actor classes, but not `ray.kill` (its `:233-245` at `b510bc9`).
  Under `v0.2.2` the pool's kill therefore reaches Ray's own `ray.kill`. With Ray not started, that
  raises `RaySystemError` from `worker.check_connected()`, and it never starts Ray (Ray 2.43.0 and
  2.55.1, `ray/_private/worker.py`, `def kill`). `_kill_actors` ignores what a kill raises, so
  those tests run as under `v0.2.1` and do not see the release. Whether SGK's stand-in takes up
  the package's `ray.kill` is SGK's choice.

### 1.2 The release check, probed

The planner probed the release on this machine, offline, as extraction prompt 10 did.
- **The build.** From a `git archive` of `168ecd0` with only `version = "0.2.2"` changed,
  `uv build --offline --wheel` gives `datastorekit-0.2.2-py3-none-any.whl`. It has 25 entries, none
  under `datastorekit/tests/`, and `…dist-info/licenses/LICENSE` is among them. `METADATA` says
  `Version: 0.2.2`, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43` and
  `Requires-Dist: sqlalchemy<2.1,>=2.0.39`.
- **The install.** `uv venv --offline -p /opt/local/bin/python3.13`, then `uv pip install
  --offline <wheel> "ray==2.55.1" "sqlalchemy==2.0.46"`.
- **The run**, from a directory outside the repository with `PYTHONPATH` unset:
  - the layer modules import from the venv's `site-packages`;
  - `importlib.metadata.version("datastorekit")` is `0.2.2`;
  - `ShardedPool` has `_kill_actors`, and `__exit__` has the docstring 01 gave it;
  - `import datastorekit.tests` raises `ModuleNotFoundError`;
  - `python -m datastorekit.tools.sharded_store --help` exits 0.
- **Against `v0.2.1`'s wheel**, built from `git archive v0.2.1`: of the 20 `RECORD` lines under
  `datastorekit/`, only `SQL/ShardedPool.py`'s differs.

The wheel's bytes are not reproducible across builds (file times). Record the SHA-256 of yours,
and do not compare it with the planner's. The `RECORD` lines are content hashes, and do compare.

---

## 2. What to change

### 2.1 `pyproject.toml`

`version = "0.2.2"`. Nothing else. No other file carries the version.

### 2.2 `README.md`

- **Status.** A paragraph for **`v0.2.2`**, above `v0.2.1`'s (`README.md:10-17`):
  - it is a fix release with one fix, `actor-names` 01: a closed pool, and a refused open,
    release their Ray actors' names at once, so a store can be reopened in one Ray session while a
    closed pool is still referenced;
  - a closed pool's actor handles are dead afterwards, and a second `__exit__` does nothing;
  - two pools open at once in one Ray session still collide;
  - no API changes, nothing the layer writes changes, and no message changes;
  - it points at contract §9.3 for the detail, by its anchor.
- **Installing.** The pin is `v0.2.2` (`:59`). Replace `:62-63` with one sentence saying:
  - `v0.2.1`, `v0.2.0` and `v0.1.0` remain tagged, and no tag is moved or deleted;
  - every client adopts `v0.2.2`, which fixes a defect that all three earlier releases carry.

  Write it as of the tag. The README is committed before the tag exists, and is true once it does.
- **Using it.** The item at `:93-94` names "the three fixes of `v0.2.1`". Extend it to name
  `v0.2.2`'s fix too, still linking §9.
- **Nothing else changes.** Check every name and anchor the README mentions, as extraction prompt
  10 did.

### 2.3 `PROVENANCE.md`

Add, after "Prompts 08a, 08b and 09: fixes and prose (`v0.2.1`)" (`:118`, the file's last section),
a section **"`actor-names` prompt 01: a closed pool releases its actor names (`v0.2.2`)"**. It says:
- **The fix has no source.** It was made here, and closed
  `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]` (opened by extraction prompt 11,
  closed on the extraction board's §4 by `actor-names` 01, `ac50a8a`). Its test module is
  `datastorekit/tests/test_closed_pool_releases_its_names.py`.
- **SGK's frozen copies carry the defect.** SGK names the same actors at
  `Datastore/SQL/ShardedPool.py:294`, `:305` and `:544`, at `6f7f291` and `b510bc9` (the
  extraction board's §4 entry), and its `__exit__` kills none. "The freeze" says a defect found
  during the freeze is fixed here after G2. Decision U3 of `actor-names` fixed this one before it,
  as extraction U33 fixed three. SGK receives it by adopting `v0.2.2`.
- **What changed in the package**: `SQL/ShardedPool.py` only, by addition. In this repository
  only, the stand-in pool (`datastorekit/tests/standin_pool.py`), the new test module, the smoke
  script and the contract's §9.3 changed too.
- **The files 01 changed, and its log.**

Change nothing above it. `PROVENANCE.md` is outside the package, so it may name SGK and its paths.

### 2.4 The addenda (U3)

Each addendum is dated, says it was written by `actor-names` prompt 02, and is added. **Nothing
already in the file is rewritten** (`CLAUDE.md` rule 6). That covers 07a's text and extraction
prompt 10's `v0.2.1` addendum: both stay as written, true of their releases. Each file gains two
things.

1. **An italic line at its head**, after extraction prompt 10's (`docs/adoption/README.md:7-10`,
   `secondarygwkit.md:16-19`, `champbh.md:17-20`, `stochasticinstantons.md:15-18`). It says that
   the addendum below gives the pin `v0.2.2` and what changed since `v0.2.1`, and that it
   supersedes the statements it names.
2. **A section `## Addendum: v0.2.2 (actor-names prompt 02, <date>)`**, unnumbered, after the
   `v0.2.1` addendum. In each checklist it goes before `## Appendix: the script's output`
   (`secondarygwkit.md:441`, `champbh.md:459`, `stochasticinstantons.md:429`). In the README it
   goes at the end (the `v0.2.1` addendum ends the file, at `:268`). The date is the day you write
   it.

Each addendum states:
- **the pin**, `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.2`, in place of
  `v0.2.1`'s, and that the client adopts `v0.2.2` (U3 of `actor-names`, amending U37);
- **what changed since `v0.2.1`, for that client** (below), with contract §9.3's rows as the
  detail, linked by anchor;
- **which statements it supersedes**, each by `path:line` of the file it is in. At least: the head
  line that says `v0.2.1`, the `v0.2.1` addendum's pin and its sentence that the client adopts
  `v0.2.1`, and its gate statement;
- **line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, and one in the
  `v0.2.1` addendum stays `v0.2.1`'s. A line this addendum cites is `v0.2.2`'s tree, whose
  `datastorekit/` is `ac50a8a`'s and 02's.

What each addendum says:

| File | States |
|---|---|
| `README.md` | the pin; the four behaviours of §1.1 and the one unchanged, each linked to its row of contract §9.3; nothing any client supplies or stores changes, and no message; §1.1's measure of the 14 constructions, so no client uses a closed pool; the checklists are not re-measured (as U37), and each has its own addendum |
| `secondarygwkit.md` | the files: at `v0.2.2` SGK's `Datastore/SQL/ShardedPool.py` and the package's differ also by 01's 48 lines, and the six files the `v0.2.1` addendum names as able to equal SGK's sources are unchanged by 01; item 8 still holds (nothing written changes, so every SGK store opens as under `v0.2.1`, and G2's rehearsal is the measurement); SGK's 7 constructions (§1.1); SGK's own stand-in and `test_quadsource_policy_main` (§1.1), as a fact and with no instruction; SGK's frozen copies carry the defect, and adoption fixes it |
| `champbh.md` | CPBH's 3 constructions (§1.1); nothing in its item 6 or 8 changes; the fix is latent for CPBH |
| `stochasticinstantons.md` | SI's 4 constructions (§1.1), the conftest fixture among them, which closes its pool before `ray.shutdown()`; the fix is latent for SI |

**The line numbers here are the planner's at `168ecd0`.** Check each against the file before citing
it, and cite what you find. A statement the table does not name that is no longer true of `v0.2.2`
is superseded too, and recorded in the log.

### 2.5 The extraction board's gates

On `../extraction/IMPLEMENTATION_STATE.md` §2, the titles of G2, G3 and G4 say `v0.2.2`, with
"(U37; `actor-names` U3)". Each row gains a dated line: `v0.2.2` is ready to be tagged on
`actor-names` 02's commit once CI passes there at both ends (as U23 and U28), and 02 makes no tag
and pushes nothing. The lines already there stay as they are. G1 is unchanged, and so is the rest
of that board. That campaign stays closed.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **Additive documents.** Everything under `docs/` is additive (`CLAUDE.md` rule 6). An addendum
   that rewrites a line of 07a's, or of the `v0.2.1` addendum, fails acceptance. `git diff` of each
   file under `docs/adoption/` shows `+` lines only.
2. **A name or link that does not exist.** Check every module, name, file, anchor and contract row
   that the README, `PROVENANCE.md` and the addenda mention: names by importing them in `venv/`,
   and anchors by finding the heading by GitHub's rule. The log lists each, with how it was
   checked. Contract §9.3's heading is "9.3 `actor-names` prompt 01"; derive its anchor, and say
   how.
3. **The tag does not exist yet.** The README, the addenda and the gates name `v0.2.2` as of the
   tag. Nothing may say it is tagged.
4. **No client is re-measured beyond §1.1.** Re-run §1.1's measure yourself, read-only through
   `git`, and record it. If any result differs, stop.
5. **Offline only.** Every venv and the build are `--offline`. A pin, or the build backend, that
   does not resolve offline is a stop.
6. **`venv/`'s metadata.** After §2.1, `pip show datastorekit` in `venv/` still says `0.2.1`, since
   the editable install records the version when it is installed. Reinstall it offline:
   `uv pip install --offline --no-deps --no-build-isolation --python venv/bin/python -e .`. That
   writes a `datastorekit.egg-info/` at the root, which you delete afterwards (extraction log 10
   records both). Then run the suite in `venv/` again. Nothing else is built in the checkout.
7. **No Ray.** This prompt starts no Ray. The smoke script is not run: no code changes.

---

## 4. Verification

1. **The suite.** In `venv/`, `Ran 492 tests … OK` before and after, with `pip show` saying `0.2.2`
   after. Also at the high end: a fresh offline scratch venv (Python 3.13.16, `ray==2.55.1`,
   `sqlalchemy==2.0.46`, `setuptools`) with a `git archive` of your tree installed editable
   (`--no-deps --no-build-isolation`) gives `Ran 492 tests … OK`. Record the `ResourceWarning`
   lines at each end: 0 in `venv/`; 0 or 4 at the high end, which is timing (log 01, correction 8).
2. **The checks.**
   - `compare_ported_tests.py` exits 0 with "20 module(s) … 1 test(s) declared not ported".
   - `black --check datastorekit docs` leaves 72 files unchanged.
   - The two guards pass; they are in the suite.
3. **The release check**, as §1.2. Build from a clean `git archive` of your tree, never in this
   checkout, and install at the high pins, offline. Record:
   - the wheel's name, size, entry count and SHA-256, and its file list;
   - `METADATA`'s `Version`, `Requires-Python` and `Requires-Dist` lines;
   - each command of §1.2, with its output;
   - the `RECORD` comparison with a wheel built from `git archive v0.2.1`.

   `git status` shows no `build/`, `dist/` or `*.egg-info` afterwards.
4. **The documents.** List every remaining `v0.2.1` in `README.md`, `PROVENANCE.md` and
   `docs/adoption/*.md`, each with why it stays: history, a statement an addendum supersedes, or
   the README's "remain tagged". Also confirm:
   - `git diff` of the four files under `docs/adoption/` has no `-` line;
   - `docs/client-contract.md` and `docs/extraction-verification.md` are unchanged.
5. **The breakage record.** Each item is a change exactly as applied in a scratch export, with
   what failed. None is committed. Check each diff with `git apply --check` and `-R --check` as
   recorded.
   - **(a)** `pyproject.toml`'s version left at `0.2.1`: the release check's `METADATA` and
     `importlib.metadata.version` assertions fail, naming `0.2.1`.
   - **(b)** the `exclude` line removed from `pyproject.toml`: the wheel lists files under
     `datastorekit/tests/`, and `import datastorekit.tests` succeeds.
   - **(c)** the wheel built from `git archive v0.2.1` with only its version set to `0.2.2`: its
     `METADATA` says `0.2.2`, but the `RECORD` comparison with `v0.2.1`'s wheel shows no line
     differing, where the release shows `SQL/ShardedPool.py`'s, and `ShardedPool` has no
     `_kill_actors`. The check must catch a version number with no fix behind it.
6. **The clients.** Record each client's `HEAD` and `git status --short`, at the start and the end,
   unchanged. None is written, run, imported or opened.

---

## 5. Acceptance

1. `pyproject.toml` says `0.2.2`, and nothing else in it changed.
2. `README.md` and `PROVENANCE.md` are as §2.2 and §2.3 say, and every name in them exists.
3. Each of the four files under `docs/adoption/` has its italic line and its addendum, per §2.4,
   and no line of it is rewritten.
4. The extraction board's G2–G4 are as §2.5 says.
5. §4.1–§4.6 hold.
6. **The records**, in the same commit:
   - the log `logs/02-release-v0.2.2.md`, per README §5.1. Besides its sections it has the release
     check, the documents' check (§4.4), every name and link checked (hazard 2), §1.1's measure
     re-run (hazard 4), (a)–(c), and the clients at the start and the end;
   - this board: §1's row for 02 (landed, commit, log), and the header;
   - this campaign's README: its header and §2's row for 02;
   - `docs/OPEN_ISSUES.md`: unchanged at **4**, unless the work opens an issue;
   - `prompts/INDEX.md`: the campaign's line.

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 492, in any venv.
- The release check fails in a way (a)–(c) do not explain.
- §1.1's measure, re-run, differs: a construction that is not a `with` block, a use of a pool after
  its block, or a client that calls `ray.kill`, `ray.get_actor` or a pool's `__exit__`.
- An addendum cannot say what it must without rewriting a line already in its file.
- Anything would change a file under `datastorekit/`, `docs/client-contract.md`,
  `docs/extraction-verification.md`, `docs/extraction/`, the workflow, or any file not in §7.
- Anything would push, make or move a tag, download, start Ray, or write, run, import or open
  anything of a client.

---

## 7. What this prompt changes, and what it does not

- **Files it changes:**
  - `pyproject.toml`, `README.md` and `PROVENANCE.md`;
  - `docs/adoption/README.md`, `secondarygwkit.md`, `champbh.md` and `stochasticinstantons.md`,
    by addition only;
  - the extraction board's §2 (G2–G4), per §2.5;
  - the log, this board, this campaign's README (its header and §2's row for 02),
    `docs/OPEN_ISSUES.md` if an issue is opened, and `prompts/INDEX.md`.
- **It changes nothing else:** no file under `datastorekit/`; not `docs/client-contract.md`,
  `docs/extraction-verification.md`, `docs/extraction/`, the workflow, `CLAUDE.md`, `LICENSE` or
  `.gitignore`.
- **It touches no client repository.**
- **It makes no tag and pushes nothing.** The orchestrator's note says how the push and the tag are
  made after the review.

---

## 8. After 02

The campaign closes when `v0.2.2` is tagged on 02's commit after green CI. The orchestrator
records that on this board, closes the campaign in its header, README and `prompts/INDEX.md`, in a
records commit of its own, and pushes it with the user's approval. G2–G4 stay on the extraction
board, recorded when they hold.
