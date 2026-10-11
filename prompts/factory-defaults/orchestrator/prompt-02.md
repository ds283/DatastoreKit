# Orchestrator — prompt 02, release `v0.2.3`

Read [`../README.md`](../README.md) first: §0, §1, §2, §4, §5 (every rule), §6.1 and §6.2 (U1 and
U5), and §7. Then read [`prompt-01.md`](prompt-01.md), whose "Conventions" and §4–§5 this note
keeps unless it says otherwise, and `actor-names`'
[`prompt-02.md`](../../actor-names/orchestrator/prompt-02.md), the note for the release this one
repeats: its §0, its additions, and its §5, which this note's §5 follows. Then read this board's
review of 01.

**You do not write code.** You may:
- run the suite, the port check, `black --check` and the guards;
- make venvs in the session scratchpad with `uv … --offline`, from the cache the extraction
  campaign filled, and nothing else: **no download**;
- export the tree with `git archive` into the scratchpad, and build wheels, run probes and replay
  breakages there, never in this checkout and never committing one;
- **start no Ray.** No code changes, so the smoke script is not run (the prompt's hazard 7);
- reach the network only for one `git ls-remote origin` at dispatch and one at the review, and for
  the pushes, the tag and the CI read of §5, each with the user's approval;
- read the three clients only through `git -C <client> rev-parse|status|show|grep|ls-tree|log|cat-file|merge-base`;
- fix small residue in a follow-up commit of your own (§4).

**The prompt:** [`02-release-v0.2.3.md`](../02-release-v0.2.3.md)
**Closes:** nothing · **Narrows:** nothing · **Changes:** nothing in the package · **Opens:** only
what the work finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- 01 landed (`f5d8957`), was reviewed (`85f504d`) and passed CI there at both ends,
  [run 38172753163](https://github.com/ds283/DatastoreKit/actions/runs/38172753163), recorded at
  `97c9a8e`. 02 was written against `97c9a8e` (`f01c4e2`).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- `git diff --stat f5d8957 HEAD -- datastorekit docs pyproject.toml README.md PROVENANCE.md
  .github` is empty: everything 02 reads or edits, but the extraction board, is 01's tree. And
  `git diff --stat 6d8ee9a HEAD -- docs/adoption README.md PROVENANCE.md pyproject.toml .github`
  is empty: the files 02 edits are `v0.2.2`'s.
- `origin/main` is `85f504d` (`git ls-remote origin`, 2026-10-11), an ancestor of `main`, which is
  ahead of it by `97c9a8e`, `f01c4e2` and this note. The tags are `v0.1.0` (`0ece4aa` →
  `68db557`), `v0.2.0` (`9eaf542` → `240028e`), `v0.2.1` (`0ba2e4d` → `33778b0`) and `v0.2.2`
  (`c32d027` → `6d8ee9a`), here and on `origin`, and no other.
- The clients' `HEAD`s: SGK `789b72d` (branch `handover-remedial`), CPBH `52142d7` (`main`, 1
  modified entry, `prompts/INDEX.md`, and 24 untracked), SI `7bb3efd` (`main`, clean). **SGK is
  being worked on by another session**: at writing its status shows 11 staged entries (its own
  adoption work: `RayTools/` deleted, `main.py` and the `extract_*.py` scripts modified, and
  others) and one untracked file. Its `HEAD` is what is compared; a changed status or `HEAD` there
  is not this campaign's doing, and is recorded, not stopped on, unless SGK instantiates a factory
  at the `HEAD` read (the prompt's §6).
- This board's §3 holds no issue, and the index is **4** (0 on this repository's boards, 4
  inherited). It stays 4 unless the work opens an issue.
- One prompt at a time in this checkout. 02 is the campaign's last.

## 0. What makes this prompt unusual

**No line of code changes, so the suite cannot catch a bad edit.** It passes whatever the
documents say. What stands in for it, as at `actor-names` 02:
- the release check, from a clean export, which alone sees `0.2.3` and the change behind it;
- hazard 1's `git diff`, which must show `+` lines only under `docs/adoption/`;
- reading: every statement an addendum makes is true of `v0.2.3`, every statement it supersedes is
  named by `path:line`, and every name and link resolves.

**The release removes an obligation, and must not overstate it.** For CPBH and SI it removes the
U32 paragraphs' whole burden: their registries of instances work as they stand. For SGK it changes
nothing SGK meets. What it does not do: it does not make a missing `register` or `build`
acceptable, change any message, or make a hook a client does not define do anything but raise
`NotImplementedError` when the layer calls it.

**The pins differ by client for the first time.** CPBH and SI adopt `v0.2.3`; SGK may stay on
`v0.2.2` or move (U5). Every earlier release said "every client adopts". The README, each addendum
and the gates must say U5 exactly, and none may advise SGK either way (hazard 8).

**SGK's adoption has begun.** At SGK `789b72d`, `0c9e2cf` ("Adopt datastorekit and delete SGK's
copy of the datastore layer") is an ancestor, `Datastore/SQL/ObjectFactories/base.py` no longer
exists, and `requirements.txt:17` pins `v0.2.2`. G2 is not recorded by 02 (the prompt's §1.1).

**The acceptance finishes elsewhere.** `v0.2.3` is made on 02's commit only once CI has passed
there at both ends (§5). It is the commit CPBH's prompt 07 will pin.

**The push carries more than 02.** `origin/main` is `85f504d`. Pushing 02's commit as `main`
fast-forwards over `97c9a8e`, `f01c4e2`, this note and 02 itself. None of them but 02 changes a
file CI reads, so the tree CI tests is 02's.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-11 at `f01c4e2` (whose
`datastorekit/`, `docs/`, `README.md`, `PROVENANCE.md` and `pyproject.toml` are `97c9a8e`'s), in
`venv/`, in offline scratch venvs and exports at the high end, and with wheels built offline from
exports. Pass them on. Corrections 1 and 2 change what the agent does, and are STRUCTURALLY
REQUIRED. Corrections 3 and 4 correct or complete what the prompt states; the log records each as
found.

1. **Hazard 6's reinstall cannot run, again.** `venv/` has no `setuptools` (`import setuptools`
   raises `ModuleNotFoundError`), so `uv pip install --offline --no-deps --no-build-isolation
   --python venv/bin/python -e .` is refused: probed on a scratch `python3.12 -m venv` against an
   export at `0.2.3`, uv refuses and suggests installing `setuptools` into the environment. That
   would change `venv/`, which this prompt does not do. **Use `actor-names` 02's form (its
   correction 1), `uv pip install --offline --no-deps --python venv/bin/python -e .`, from the
   repository root, without `--no-build-isolation`.** Probed the same way: it installs
   `datastorekit==0.2.3` editable, `pip show` says `Version: 0.2.3`, and it writes
   `datastorekit.egg-info/` at the root, which is deleted afterwards. The high-end scratch venv of
   §4.1 has `setuptools`, so `--no-build-isolation` is right there.
2. **§1.2's probe of the instance's `store` must pass its arguments.** "Its instance's `store`
   raises `NotImplementedError` with no arguments" cannot be read as a call with no arguments:
   `store` is static with six positional parameters, so `F().store()` raises `TypeError: … missing
   6 required positional arguments` at every release, `v0.2.2`'s included. Probed at `0.2.3`:
   **call each of the three on the instance with its arity** (`store` six arguments, `validate`
   four, `validate_on_startup` three; `None` for each will do), and check that each raises
   `NotImplementedError` whose `args` is `()`, the bare exception. Under breakage (c) the same
   probe fails earlier, at `F()`, with `TypeError: Can't instantiate abstract class F without an
   implementation for abstract methods 'store', 'validate', 'validate_on_startup'`, which is the
   failure (c) is to show.
3. **How the earlier addenda's citations are read, with numbers.** The `v0.2.2` italic line added
   **five** lines in `docs/adoption/README.md` (`:12-16`, after `:11`) and **six** in each
   checklist (after `:20` in SGK's, `:21` in CPBH's, `:19` in SI's), as each `v0.2.2` addendum
   says (`README.md:347`, `secondarygwkit.md:518`, `champbh.md:510`,
   `stochasticinstantons.md:479`). After 02's italic line of N lines:
   - the `v0.2.2` addendum's citations are read at `6d8ee9a`, or N lines later here, except those
     above the insert: the head lines it cites (the `v0.2.1` italic line, `README.md:7-10`, and
     each checklist's like it, and `:3`, `:6` or `:5`);
   - the `v0.2.1` addendum's are read at `33778b0`, or **k + N** lines later here (k = 5 in the
     README, 6 in each checklist), except, as before, `:3`, `:6` or `:5`. The prompt's "its rule
     still holds, shifted by N" means this; the addendum states k + N as a number.

   The agent states N and k + N for each file, and the review checks them against the file as
   committed.
4. **The grep of §2.4 finds more than the prompt names, and each stays true.** At `f01c4e2`,
   beyond the table's hits and SI's `:76`, `:239` and CPBH's `:244`:
   - `secondarygwkit.md:197-199`, that SGK registers classes "so the abstractness of
     `SQLAFactoryBase` is never enforced on them (U32 does not reach SGK)": true at `v0.2.3`, and
     more so;
   - the "all five" cells of item 5's tables (`champbh.md:187-193`, `stochasticinstantons.md:180-185`),
     which say which hooks a class defines: facts of the client, unchanged;
   - `champbh.md:610`, `:613` and `stochasticinstantons.md:81`, `:579`: the file names
     `AbstractCoupling.py` and `AbstractPotential.py`, not statements.

   None is superseded. The log lists each with why it stays.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **Work in this order:**
  1. the baseline: 504 in `venv/`, and at the high end from a fresh venv with an export of `HEAD`
     installed editable; the port check; `black --check datastorekit docs`, 74 files; the clients'
     `HEAD`s and statuses; §1.1's measure (hazard 4);
  2. `pyproject.toml`; `venv/`'s reinstall (correction 1), the `egg-info` removed; the suite;
  3. `README.md` and `PROVENANCE.md`;
  4. the four addenda and italic lines; then hazard 1's `git diff`;
  5. the extraction board's gates;
  6. the release check (correction 2); the high end;
  7. (a)–(c);
  8. the documents' check (§4.4) and the name-and-link check (hazard 2);
  9. `venv/`'s suite again, the port check, `black`, the clients again, the records.
- **Give each addendum's supersessions as a table** (`path:line`, the statement in brief, what
  replaces it), as the `v0.2.1` and `v0.2.2` addenda do. The log repeats the four tables, with
  any statement found that the prompt's table does not name.
- **Where the `v0.2.2` addenda state the pin and the gate.** In the README: "The pin" (`:284-285`),
  the pin (`:288`), and the gate in its table's "What replaces it" cells (`:360`, `:362`). In each
  checklist: the pin sentence, which also states the gate (`secondarygwkit.md:454-455`,
  `champbh.md:472-473`, `stochasticinstantons.md:442-444`), the pin (`:458`, `:476`, `:447`), and
  the table's gate row (`:533`, `:522`, `:491`). Each is cited as it stands after 02's italic line.
- **Placement.** In each checklist the `v0.2.2` addendum is preceded by a `---` rule
  (`secondarygwkit.md:445`, `champbh.md:463`, `stochasticinstantons.md:433`) and followed by one
  before the appendix (`:535`, `:524`, `:493`). The `v0.2.3` addendum goes after the `v0.2.2`
  addendum's table and before that second rule, with a `---` of its own above it. In the README it
  goes at the end, after a `---`. Its heading is `## Addendum: v0.2.3 (factory-defaults prompt 02,
  <date>)`; by GitHub's rule the anchor is `#addendum-v023-factory-defaults-prompt-02-<yyyy-mm-dd>`.
- **`PROVENANCE.md`'s new section is a `###`**, as `:89`, `:118` and `:160` are, under "After
  `v0.1.0`", after the `actor-names` section, which ends the file at `:203`.
- **The contract's anchor**, by GitHub's rule (lower-case; drop backticks and punctuation other
  than hyphens; spaces to hyphens): §9.5 "9.5 `factory-defaults` prompt 01"
  (`docs/client-contract.md:338`) is `#95-factory-defaults-prompt-01`. From `docs/adoption/` the
  path is `../client-contract.md#…`; from the root, `docs/client-contract.md#…`. §3 is
  `#3-the-factory-hooks`, as `README.md:96` already links it.
- **The gate titles**, exactly: G2 "SGK adopted `v0.2.2` or later (U37; `actor-names` U3;
  `factory-defaults` U5), fingerprint reproduced"; G3 "CPBH adopted `v0.2.3` (U37; `actor-names`
  U3; `factory-defaults` U5)"; G4 "SI adopted `v0.2.3` (U37; `actor-names` U3; `factory-defaults`
  U5)". Each row's status cell gains one dated italic sentence, in the form of the `v0.2.2` "ready
  to be tagged" sentences, linking its client's new addendum by anchor. G2's says too that SGK
  may stay on `v0.2.2` (U5). Nothing else on that board changes, its header included
  (`prompts/extraction/IMPLEMENTATION_STATE.md:1537-1539`).
- **Keep the name-and-link check as a scratch script**, never committed, as `actor-names` log 02
  did: every relative link and anchor in `README.md`, `PROVENANCE.md`, the four adoption files and
  the extraction board's §2, each file resolved and each anchor found among its target's headings
  by GitHub's rule; every dotted `datastorekit.` name imported in `venv/`.
- **Build (a)'s, (b)'s and (c)'s wheels from their own exports**, each with the prompt's change
  and only that. Record (a) and (b) as diffs to `pyproject.toml` that `git apply --check` and `-R
  --check` accept against an export of the commit; (c) is the version line applied to an export of
  `v0.2.2`, and is recorded so that it applies there. Run the release probe (with correction 2) in
  each wheel's venv, and record each output.
- **§1.1's measure.** The orchestrator's own, a script of `ast` reads from `git show` run with
  `python3 -I`, gave the prompt's table exactly (below). The agent writes its own, and records its
  essentials and its output.

**The facts, checked by the orchestrator.** Pass them on.

- **The suite** at `f01c4e2`: `Ran 504 tests … OK` in `venv/` (118 s), 0 `ResourceWarning` lines,
  and at the high end from a fresh offline venv with an export installed editable
  (`--no-deps --no-build-isolation`), `Ran 504 tests … OK` (112 s), with 4 `ResourceWarning`
  lines, which is timing. The port check exits 0 ("OK: 20 module(s) … 1 test(s) declared not
  ported"); `black --check datastorekit docs` leaves 74 files unchanged.
- **§1.1 reproduces**, read through `git` at SGK `b510bc9` and `789b72d`, CPBH `52142d7` and SI
  `7bb3efd`:
  - SGK: 38 classes whose bases name `SQLAFactoryBase`, 31 lacking one of the three, none lacking
    `register` or `build`, and no call of any by name, at both commits;
  - CPBH: 23, 20, none; 27 calls, all at `Datastore/SQL/Datastore.py:95-121`, 24 of a class
    lacking one of the three;
  - SI: 28, 16, none; 33 calls, 30 at `Datastore/SQL/Datastore.py:97-126` and three at
    `CosmologyConcepts/Potentials/registry.py:33`, `:40` and
    `Datastore/SQL/ObjectFactories/MasslessDecoupledDiffusion.py:71`; 21 of a class lacking one of
    the three;
  - CPBH's base at `52142d7` (`Datastore/SQL/ObjectFactories/base.py:16-30`) is a plain class
    whose five hooks are instance methods raising `NotImplementedError`, as the prompt says;
  - SGK at `789b72d`: `0c9e2cf` an ancestor, `Datastore/SQL/ObjectFactories/base.py` absent,
    `requirements.txt:17` the `v0.2.2` pin. SGK's base at `6f7f291` has five `@abstractmethod`s.
- **The package.** `git diff --stat 6d8ee9a f5d8957 -- datastorekit/SQL`: 1 file, 24 insertions,
  6 deletions. Over `datastorekit/`, four files: `SQL/factory_base.py`, `tests/client/instances.py`
  (new), `tests/test_factory_instances.py` (new) and `tests/test_neutral_client.py`. Only
  `pyproject.toml:7` carries the version.
- **§1.2 reproduces**, with correction 2. From a `git archive` of `f01c4e2` with only
  `version = "0.2.3"`, `uv build --offline --wheel` gives `datastorekit-0.2.3-py3-none-any.whl`,
  99,185 bytes (the bytes are not reproducible; compare `RECORD` lines, not hashes):
  - 25 entries, none under `datastorekit/tests/`; `datastorekit-0.2.3.dist-info/licenses/LICENSE`;
  - `METADATA`: `Version: 0.2.3`, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43`,
    `Requires-Dist: sqlalchemy<2.1,>=2.0.39`;
  - installed offline with `ray==2.55.1` and `sqlalchemy==2.0.46` into a Python 3.13.16 venv and
    run from a directory outside the repository with `PYTHONPATH` unset and `python -I`: the
    package imports from `site-packages`; the metadata version is `0.2.3`;
    `__abstractmethods__` is `['build', 'register']` sorted; `store (obj, conn, table, inserter,
    tables, inserters)`, `validate (obj, conn, table, tables)` and `validate_on_startup (conn,
    table, tables, prune=False)`, `v0.2.2`'s, none with `__isabstractmethod__`; a subclass
    defining only `register` and `build` instantiates, and its instance's three hooks each raise
    `NotImplementedError` with `args == ()`; `import datastorekit.tests` raises
    `ModuleNotFoundError`; `python -m datastorekit.tools.sharded_store --help` exits 0;
  - against `git archive v0.2.2`'s wheel (98,811 bytes): 20 `RECORD` lines under `datastorekit/`
    each side, the same paths, and only `SQL/factory_base.py`'s differs.
- **The breakages**, each from its own export, at the high pins:

  | | Change | Measured |
  |---|---|---|
  | (a) | version left at `0.2.2` | `datastorekit-0.2.2-py3-none-any.whl`; `Version: 0.2.2`; the installed metadata version is `0.2.2`. Its `RECORD` differs from `v0.2.2`'s wheel's in `SQL/factory_base.py` only: the version alone is wrong |
  | (b) | `exclude = ["datastorekit.tests", "datastorekit.tests.*"]` deleted (`pyproject.toml:17`) | 74 entries, 49 under `datastorekit/tests/`; `import datastorekit.tests` succeeds from `site-packages` |
  | (c) | `v0.2.2`'s tree at `0.2.3` | `Version: 0.2.3`; all 20 `RECORD` lines under `datastorekit/` equal `v0.2.2`'s; `__abstractmethods__` has five names, each of the three with `__isabstractmethod__` true; `F()` raises `TypeError: Can't instantiate abstract class F …` |

- **The line numbers the prompt cites hold at `f01c4e2`**: `README.md:10-21`, `:72`, `:75-76`,
  `:94-96`, `:106-109`; `PROVENANCE.md:160` (the file is 203 lines, and that section is its last);
  the italic lines `docs/adoption/README.md:12-15`, `secondarygwkit.md:21-25`, `champbh.md:22-26`,
  `stochasticinstantons.md:20-24`; the appendices `secondarygwkit.md:537`, `champbh.md:526`,
  `stochasticinstantons.md:495`; the README addendum ending the file at `:363`; the superseded
  statements `docs/adoption/README.md:130-141`, `secondarygwkit.md:192-194`, `champbh.md:34-35`
  and `:200-221`, `stochasticinstantons.md:30-31`, `:121-126` and `:187-200`; the `v0.2.1`
  addendum's row for `secondarygwkit.md:187-188` (`:439`); contract §9.5 at `:338`. The extraction
  board's G2–G4 are `prompts/extraction/IMPLEMENTATION_STATE.md:1537-1539`.
- **The toolchain.** `venv/`: Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39, SQLite 3.53.4,
  `black` 25.1.0, `datastorekit 0.2.2` editable from this checkout, no `setuptools`. `uv` 0.12.20.
  The high end, `uv venv --offline -p /opt/local/bin/python3.13`: 3.13.16, 2.55.1, 2.0.46, SQLite
  3.53.4.
- **Expected counts.**
  - The suite: **504**, before and after, at both ends; 0 `ResourceWarning` lines in `venv/`, 0
    or 4 at the high end (timing).
  - `compare_ported_tests.py`: exit 0, "20 module(s) … 1 test(s) declared not ported".
  - `black --check datastorekit docs`: **74** files, before and after.
  - The index: **4**, unchanged unless the work opens an issue.
- **Ray.** No Ray process (`pgrep -lf 'gcs_server|raylet|ray::'` empty); `RAY_ADDRESS` and
  `RAY_ENABLE_AUTO_CONNECT` unset; no `/tmp/ray/ray_current_cluster`. Nothing in this prompt
  calls one of Ray's auto-init APIs: the release probes import the base and call its hooks only.

**What the review exists to establish.**
- **(E1) Scope.** Only the prompt's §7 files change. Nothing under `datastorekit/`, and not the
  contract, the verification document, `docs/extraction/` or the workflow.
- **(E2) The release.** A wheel from a clean export of the commit is `0.2.3`, holds 01's base and
  no tests, and behaves as §1.2 (with correction 2) says from outside the repository.
- **(E3) The documents.** `pyproject.toml`, `README.md` and `PROVENANCE.md` as §2.1–§2.3 say; the
  change stated as the removal of a refusal, not as a fix of SGK's; U5's pins exactly, advising SGK
  neither way; nothing says `v0.2.3` is tagged; every name and link resolves.
- **(E4) The addenda.** Each additive, dated and placed as the additions say; each states its pin,
  what changed for its client, what it supersedes by `path:line`, and the line shifts (correction
  3), true at the file.
- **(E5) Both ends.** 504 in `venv/` (now `0.2.3`) and at the high end.
- **(E6) The breakages.** (a)–(c) fail as recorded.
- **(E7) The records**, and the extraction board's gates.

**Conventions.** `actor-names` 02's note's, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff **as recorded in the log** with `git apply --check` and `-R --check`
  against a scratch export;
- read a client only through `git`, and never import or run its code;
- use a subdirectory of the session scratchpad, never `/tmp`, for venvs, exports, wheels and
  probes; put no scratch `.py` under `datastorekit/` or `docs/`;
- a stop goes to the user, through the orchestrator;
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
   --ignored` (at writing: `.idea/`, `venv/` and five `__pycache__/` directories, one of them
   `docs/extraction/__pycache__/`).
2. **The baseline.** In `venv/`, `Ran 504 tests … OK` with no `ResourceWarning`; the port check
   exits 0; `black --check datastorekit docs` leaves 74 files unchanged; `pip show datastorekit`
   says `0.2.2`.
3. **The clients.** Each `HEAD` and `git status --short` as the gate says, SGK's as found.
4. **The remote.** `git ls-remote origin`: `main` at `85f504d…` and the four tags as the gate says.
5. **Ray.** No Ray process; `RAY_ADDRESS` and `RAY_ENABLE_AUTO_CONNECT` unset.
6. **The index.** 4 now, and 4 after unless the work opens an issue. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, this board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `PROVENANCE.md`, log 01 (§1 and §8), `actor-names` prompt 02 and its log;
- `HEAD`, the clients' `HEAD`s and statuses, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's four corrections and its additions. Correction 1 is the
one that would stop it: the prompt's own reinstall fails in `venv/`. Correction 2 is the one that
would make the release probe fail for the wrong reason, at every release.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/02-release-v0.2.3.md`, in README §5.1's form, with
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
   Each client's `HEAD` and status as at dispatch (SGK's recorded as found).
2. **Additive (E1, E4).** `git diff <parent> <commit> -- docs/adoption/` has no `-` line.
   `pyproject.toml`'s diff is the version line alone. The extraction board's diff is G2–G4's three
   rows alone, each keeping every sentence it had.
3. **The release (E2).** From `git archive <commit>`, build the wheel offline and install it into a
   fresh high-end venv, offline. Check §1.2's facts as the facts above give them: 25 entries, none
   under `tests/`; the licence; `METADATA`; from outside the repository, `0.2.3`,
   `__abstractmethods__`, the three signatures, the subclass's instance and its three bare
   `NotImplementedError`s (correction 2), `datastorekit.tests` refused, `sharded_store --help`. The
   `RECORD` comparison with the review's own `v0.2.2` wheel: only `SQL/factory_base.py`'s line
   differs. Compare the wheel's file list with the log's.
4. **`README.md` and `PROVENANCE.md`, by reading (E3).**
   - Status: a `v0.2.3` paragraph above `v0.2.2`'s, which is unchanged. It says the release has one
     change, U1 on the user's ruling; that a class defining `register` and `build` instantiates;
     that an instance meets what a class meets; that a class lacking either is still refused and a
     class-registering client meets nothing new; that no API, nothing written and no message
     changes; and links §9.5 by anchor.
   - The pin is `v0.2.3`; the sentence replacing `:75-76` says the four earlier tags remain, none
     moved or deleted, that CPBH and SI adopt `v0.2.3`, and that SGK may stay on `v0.2.2` or move,
     in a commit of its own, as it chooses. It names no client path, advises SGK neither way, and
     nothing says `v0.2.3` is tagged.
   - "Using it": the hooks item names `register` and `build` as abstract and the six defaulted,
     and that a registry may map a name to a class or an instance, linking §3 and §9.5; the "What
     changed after `v0.2.0`" item adds `v0.2.3`'s change, still linking §9.
   - `PROVENANCE.md`'s new `###` section follows the `actor-names` section; it says the change has
     no source and departs from SGK's base at `6f7f291` (five abstract hooks, read through `git`),
     fixes no defect of SGK's, and lists 01's files and log. Nothing above it changes, and it does
     not describe SGK's adoption.
5. **The addenda, by reading (E4).** For each of the four files:
   - the italic line is after `actor-names` 02's; the addendum is placed as the additions say,
     unnumbered, dated, and names `factory-defaults` prompt 02;
   - it gives its pin per U5, with U37 and `actor-names` U3 amended for SGK only;
   - what it says changed for its client is the prompt's row, true of `f5d8957`'s package and of
     the client at the commit it names, and links §9.5;
   - each superseded statement is cited by a `path:line` that holds in the file as committed; the
     italic line moved them, so check each against the committed file;
   - correction 3's sentence is there, with N and k + N, each the number of lines the italic lines
     added;
   - CPBH's and SI's say their registries work as they stand, and what is unchanged (their other
     item 5 findings); SGK's says nothing changes for SGK, with no instruction to SGK.
6. **Names and links, by running (E3, E4).** The review's own extraction of every relative link
   and anchor in the six documents and the extraction board's §2: each file exists, and each anchor
   is a heading by GitHub's rule. Every dotted `datastorekit.` name imports in the review's release
   venv. The list matches the log's.
7. **Both ends (E5).** In `venv/`: `pip show datastorekit` says `0.2.3`; `Ran 504 tests … OK`; no
   `datastorekit.egg-info/` at the root. In a fresh high-end venv with `git archive <commit>`
   installed editable: `Ran 504 tests … OK`, with the `ResourceWarning` lines counted (0 or 4). The
   port check exits 0. `black --check datastorekit docs` leaves 74 files unchanged.
8. **The breakages (E6).** Replay (a)–(c) as the log records them, each in its own export, against
   the facts' table. (c) must show all 20 `RECORD` lines equal to `v0.2.2`'s, five abstract hooks,
   and `TypeError` at instantiation.
9. **The records (E7).**
   - The log: every section of README §5.1, with the release check, the documents' check (§4.4),
     every name and link, §1.1's measure re-run, (a)–(c), the clients at both ends, the four
     corrections and the additions, and each addendum's supersession table.
   - The extraction board: G2–G4 as the additions say; the rest unchanged.
   - This board: 02's row (landed, commit, log) and the header. The README's header and §2 row;
     `prompts/INDEX.md`'s line. `docs/OPEN_ISSUES.md` unchanged at 4, or as opened.
10. **Nothing left behind.** No Ray process. `git tag -l` is the four tags, and `origin` is
    unchanged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 02* paragraph, in the form of
  01's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on this board, the extraction board, the log, the README and
    `prompts/INDEX.md`;
  - "reviewed; awaiting CI for `v0.2.3`" for 02 in this board's header and row, README §2 and
    `prompts/INDEX.md`;
  - the notes line, with this note marked "used for 02".
- Anything the review finds that is not residue is opened on this board's §3 and in the index.
  **An issue open against 02's commit is a stop for the tag**: tell the user, and nothing in §5
  runs until they decide.
- **Report to the user:**
  - what landed: `0.2.3`, the README, `PROVENANCE.md`, the four addenda and the gates;
  - the release check and its `RECORD` comparison, and the 504 at both ends, from the review's own
    venvs;
  - §1.1's measure, re-run;
  - (a)–(c);
  - that the push carries `97c9a8e`, `f01c4e2` and this note with 02 (§0);
  - **and ask for approval to push 02's commit** (§5).

## 5. Reaching `v0.2.3`

`actor-names` 02's note §5, with `v0.2.3` for `v0.2.2`, 02's commit for that 02's, and `85f504d`
for `2fd3ba2`. Each push and the tag is an outward-facing act: **ask the user, and wait for a clear
yes, before each.** Approval of one is not approval of the next.

1. **Push 02's commit as `main`:** `git push origin <02's SHA>:refs/heads/main`. It fast-forwards
   from `85f504d`. The workflow runs on 02's commit at both ends; the smoke script is not
   collected, so CI starts no Ray.
2. **Read the run** once it has finished: `gh run list --workflow tests.yml --commit <02's SHA>`
   and `gh run view <id> --log`. Do not poll: ask the user to say when it has finished, or check
   once when they return. From each job's log, record the versions it prints (SQLite's among
   them), the suite's verdict (`Ran 504 tests … OK`) and black's line on `low`.
3. **If either end fails**, stop. No tag. Record the failure on this board's §3 with the job's log
   lines, open it in the index, and tell the user that a fix prompt is needed. The tag goes on the
   fix's commit once its CI passes.
4. **If both pass**, with the user's approval:
   - `git tag -a v0.2.3 <02's SHA> -m "datastorekit 0.2.3: the factory base defaults store, validate and validate_on_startup, so a factory class defining register and build can be instantiated"`;
   - `git push origin v0.2.3`;
   - check that `git ls-remote origin refs/tags/v0.2.3^{}` is 02's SHA.
5. **Record it, and close the campaign** (the prompt's §8), in a records commit of its own:
   - the extraction board's G2, G3 and G4: one dated italic sentence each, in the form of the
     `v0.2.2` "is made" sentences: `v0.2.3` made, annotated, on 02's SHA, the tag object, the run's
     URL and both ends' versions and counts; for G3 and G4 that the client may now adopt it, for G2
     that SGK may adopt it or stay on `v0.2.2` (U5);
   - this board: the review paragraph's last line, 02's row, and the header: **CLOSED**;
   - the campaign README's header and §2 row, and `prompts/INDEX.md`'s line: closed, with the
     tag; the count in `docs/OPEN_ISSUES.md` unchanged;
   - then **push the rest of `main`** (`git push origin main`), with approval.
6. **Hand the user** the tag object and commit, for CPBH's prompt 07, with README §0.2's four
   points to report back to the ChamPBH session.

**Hand on.** `v0.2.3` is on 02's commit once §5 has run. CPBH and SI adopt it in place of `v0.2.2`;
SGK may stay on `v0.2.2` or move (U5), each in a campaign of its own, in its own repository; G2–G4
are recorded on the extraction board as they hold. No campaign of this repository is open after
this one.
