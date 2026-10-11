# Prompt 02 — release `v0.2.3`

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

*Written 2026-10-11 against `97c9a8e`, whose `datastorekit/` is `f5d8957`'s (prompt 01's).*

**Gate:**
- 01 landed (`f5d8957`) and was reviewed (`85f504d`). CI passed on `85f504d` at both ends,
  [run 38172753163](https://github.com/ds283/DatastoreKit/actions/runs/38172753163), recorded at
  `97c9a8e`.
- U5 is taken (README §6.2): `v0.2.3`, patch-level; CPBH and SI adopt it; SGK may stay on `v0.2.2`
  or move.
- `git status` is clean in this repository, and `origin/main` is an ancestor of `main`.
- This board's §3 holds no issue, and `docs/OPEN_ISSUES.md` counts 4, all inherited.

**Closes:** nothing. **Narrows:** nothing. **Changes:** nothing in the package. **Opens:** only
what the work finds.

**Recommended model:** **Opus.**
- No line of code changes. The work is three short edits, four dated addenda and the gates.
- The addenda are not alike. For CPBH and SI the release removes an obligation their checklists
  spell out at length (item 5's U32 paragraph, and SI's item 3); for SGK it changes nothing SGK
  meets. Each must say exactly that, and supersede by `path:line` without rewriting a word.
- Each file's head gains a line, which moves every citation below it, including the `v0.2.2`
  addendum's own table. The addendum must say how to read those, as `actor-names` 02 did.
- The release check and both ends of the suite are run as `actor-names` 02 ran them, offline.

**Read first:**

1. [`README.md`](README.md): §0, §1, §2, §4, §5 (rules 4, 5, 9 and 10), §6.2 (U1 and U5), §6.1 (the
   inherited U23, U28, U36 and U37, and `actor-names` U3) and §7.
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`, above all "Releases".
3. This board's review of 01, and log 01 (`logs/01-the-base-defaults-three-hooks.md`), §1 and §8.
4. `actor-names` prompt 02 (`../actor-names/02-release-v0.2.2.md`) and its log
   (`../actor-names/logs/02-release-v0.2.2.md`). 02 is that prompt again, for one change. Their
   release check, their addenda's form and their breakages are this prompt's.
5. The files 02 changes, as they stand: `pyproject.toml`, `README.md`, `PROVENANCE.md`,
   `docs/adoption/README.md` and the three checklists. In each checklist read item 5, the `v0.2.1`
   addendum and the `v0.2.2` addendum; in the adoption README, §4 and both addenda; in SI's
   checklist, item 3 too.
6. `docs/client-contract.md` §3 and §9.5, which 02 points at and does not change.
7. The extraction board's §2 (G1–G4), `../extraction/IMPLEMENTATION_STATE.md`.

Facts below are at `97c9a8e`, measured on 2026-10-11.

---

## 1. What is wanted

02 makes the package ready to be released as **`v0.2.3`** (U5). After it:

- `pyproject.toml` says `0.2.3`;
- `README.md` and `PROVENANCE.md` describe `v0.2.3`;
- `docs/adoption/` carries a dated addendum, in its README and in each checklist, giving the pin and
  what changed for that client since `v0.2.2`;
- the extraction board's gates say that CPBH and SI adopt `v0.2.3` (G3, G4), that SGK adopts
  `v0.2.2` or later (G2), and that the tag waits for CI.

**No line of code changes.** Nothing under `datastorekit/` is touched, and the suite stays at
**504**.

**02 makes no tag and pushes nothing** (U23, U28; README §5 rule 9). After its review, its commit
is pushed as `main`. `v0.2.3` is made on it, annotated, only once CI passes there at both ends, as
`v0.2.2` was. If CI fails, a fix prompt lands first, and no tag is ever made on a commit whose CI
is red. The tag is not this prompt's work.

### 1.1 What changed since `v0.2.2`, measured

One prompt changed the package after `v0.2.2` (`6d8ee9a`): 01, `f5d8957` (U1, the user's ruling).

- **In the wheel, only `SQL/factory_base.py` changed**: three `@abstractmethod` lines removed, the
  comment on defaulted hooks moved above the three and reworded, and a docstring added to each
  (`git diff --stat 6d8ee9a f5d8957 -- datastorekit/SQL`: 1 file, 24 insertions, 6 deletions).
  Every hook's arguments and body are `v0.2.2`'s (the review's `ast` comparison, board §1). Two
  wheels built offline, from `git archive v0.2.2` and from `97c9a8e` with only the version
  changed, have the same 20 `RECORD` lines under `datastorekit/` but `SQL/factory_base.py`'s.
- **Outside the wheel**: `datastorekit/tests/test_neutral_client.py` changed;
  `datastorekit/tests/client/instances.py` and `datastorekit/tests/test_factory_instances.py` are
  new (10 tests in all: 494 → 504); `docs/extraction/ray_smoke_run.py` gained step I; the
  contract's §9.5 and its five markers, verification §4.8 and §8.1, and a note on extraction U32
  were added.

**What a client sees** (contract §9.5). Nothing a client supplies changes, no API is added or
removed, nothing the layer writes changes, and no message, refusal or exception of the layer's
changes. One thing Python did is gone:
- **a factory class that defines `register` and `build` can be instantiated.** At `v0.2.2`
  `SQLAFactoryBase` made `store`, `validate` and `validate_on_startup` abstract too, so Python
  refused (`TypeError`) to instantiate a class lacking any of them, at the line that made the
  instance. Now the base defaults them, static, each raising a bare `NotImplementedError`, as it
  defaults `revalidate`, `owned_serials` and `inventory_spec`;
- **a registered instance meets, for a hook its class does not define, what a class meets**: the
  base's `NotImplementedError`, reached only when the layer calls the hook (contract §3's rows);
- **unchanged:** a class lacking `register` or `build` is still refused at instantiation; a class
  that is never instantiated meets nothing new; and the layer still never instantiates a factory.

And one fact the contract now states that it did not (§9.5, third row): the registry reaches each
actor as a constructor argument, serialised under Ray, so a registered instance must be of a class
defined at module level, with picklable attributes. Smoke step I showed a registry of instances
served by real actors at both ends (verification §4.8).

**What the clients do with it**, read through `git` only. The planner's measure, a script of
`ast` reads of every `.py` file from `git show <commit>:<path>`: each class whose bases name
`SQLAFactoryBase`, the methods it defines, and every call of such a class by name.

| Client, commit | Factory classes | Lacking `store`, `validate` or `validate_on_startup` | Lacking `register` or `build` | Calls that instantiate one | Of a class lacking one of the three |
|---|---|---|---|---|---|
| SGK `b510bc9` (its checklist's) | 38 | 31 | none | 0 | 0 |
| SGK `789b72d` (its `HEAD` at writing) | 38 | 31 | none | 0 | 0 |
| CPBH `52142d7` | 23 | 20 | none | 27, all in its registry (`Datastore/SQL/Datastore.py:95-121`) | 24 |
| SI `7bb3efd` | 28 | 16 | none | 33: 30 in its registry (`Datastore/SQL/Datastore.py:97-126`), and three at import (`CosmologyConcepts/Potentials/registry.py:33`, `:40`; `Datastore/SQL/ObjectFactories/MasslessDecoupledDiffusion.py:71`) | 21 (18 registry entries and the three at import) |

So:
- **CPBH**: its checklist's U32 count holds, 20 classes over 24 registry entries. Under `v0.2.2`
  each of those 24 calls raises `TypeError`; under `v0.2.3` each instantiates, since every class
  defines `register` and `build`. CPBH's registry of instances works as it stands, and item 5 asks
  nothing of its factories but the base's import path (item 3). Its quantity factories, one class
  each over several tables told apart by an `ObjectType` held on the instance, are the case 01's
  parameterised factory tests.
- **SI**: 16 classes over 18 registry entries, as its checklist says, and the three import-time
  instantiations of its item 3 (`docs/adoption/stochasticinstantons.md:121-126`) stop raising too
  (README §0.2, item 3). SI's other item 5 findings (`InflatonTrajectory`'s `prune_unvalidated`,
  its validated class) are unchanged by `v0.2.3`.
- **SGK** instantiates no factory, at its checklist's commit or its `HEAD`: it registers classes
  (its item 5). `v0.2.3` changes nothing SGK meets.

**SGK since its checklist** (read through `git`, at `789b72d`, branch `handover-remedial`): SGK's
own adoption campaign has begun. Its commit `0c9e2cf` (2026-10-11, "Adopt datastorekit and delete
SGK's copy of the datastore layer") deleted its copy of the layer, `Datastore/SQL/ObjectFactories/base.py`
among it, and its `requirements.txt:17` pins `v0.2.2`. Its factories import the package's base.
This is a fact for SGK's addendum to state, if it states it, as read; **G2 is not recorded by
02**: it is recorded on the extraction board when it holds, in a records commit of the
orchestrator's. SGK's `HEAD` moves often (another session works there); compare nothing but the
facts above, and record the `HEAD` you read.

### 1.2 The release check, probed

The planner probed the release on this machine, offline, as `actor-names` 02 did.
- **The build.** From a `git archive` of `97c9a8e` with only `version = "0.2.3"` changed,
  `uv build --offline --wheel` gives `datastorekit-0.2.3-py3-none-any.whl`. It has 25 entries, none
  under `datastorekit/tests/`, and `…dist-info/licenses/LICENSE` is among them. `METADATA` says
  `Version: 0.2.3`, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43` and
  `Requires-Dist: sqlalchemy<2.1,>=2.0.39`.
- **The install.** `uv venv --offline -p /opt/local/bin/python3.13`, then `uv pip install
  --offline <wheel> "ray==2.55.1" "sqlalchemy==2.0.46"`.
- **The run**, from a directory outside the repository with `PYTHONPATH` unset:
  - the layer modules import from the venv's `site-packages`;
  - `importlib.metadata.version("datastorekit")` is `0.2.3`;
  - `SQLAFactoryBase.__abstractmethods__` is `{'register', 'build'}`; `store`, `validate` and
    `validate_on_startup` keep `v0.2.2`'s signatures (`inspect.signature`), and none is abstract;
  - a subclass defining only `register` and `build` instantiates, and its instance's `store`
    raises `NotImplementedError` with no arguments;
  - `import datastorekit.tests` raises `ModuleNotFoundError`;
  - `python -m datastorekit.tools.sharded_store --help` exits 0.
- **Against `v0.2.2`'s wheel**, built from `git archive v0.2.2`: of the 20 `RECORD` lines under
  `datastorekit/`, only `SQL/factory_base.py`'s differs.
- **Breakage (c), probed:** a wheel built from `git archive v0.2.2` with only its version set to
  `0.2.3` has no `RECORD` line differing from `v0.2.2`'s, and its `factory_base.py` has five
  `@abstractmethod`s.

The wheel's bytes are not reproducible across builds (file times). Record the SHA-256 of yours,
and do not compare it with the planner's. The `RECORD` lines are content hashes, and do compare.

---

## 2. What to change

### 2.1 `pyproject.toml`

`version = "0.2.3"`. Nothing else. No other file carries the version.

### 2.2 `README.md`

- **Status.** A paragraph for **`v0.2.3`**, above `v0.2.2`'s (`README.md:10-21`):
  - it is a release with one change, `factory-defaults` prompt 01, on the user's ruling:
    `SQLAFactoryBase` keeps `register` and `build` abstract and defaults `store`, `validate` and
    `validate_on_startup`, so a factory class that defines the two can be instantiated and its
    instance registered;
  - a registered instance meets, for a hook its class does not define, what a class meets;
  - a class lacking `register` or `build` is still refused, and a client that registers classes
    meets nothing new;
  - no API is added or removed, nothing the layer writes changes, and no message, refusal or
    exception of the layer's changes;
  - it points at contract §9.5 for the detail, by its anchor.
- **Installing.** The pin is `v0.2.3` (`:72`). Replace `:75-76` with what U5 says, as of the tag:
  - `v0.2.2`, `v0.2.1`, `v0.2.0` and `v0.1.0` remain tagged, and no tag is moved or deleted;
  - CPBH and SI adopt `v0.2.3`, with which their registries of factory instances work as they
    stand; SGK, which registers classes, may stay on `v0.2.2` or move, in a commit of its own, as
    it chooses.

  Name no client's paths. The README is committed before the tag exists, and is true once it does.
- **Using it.** Two items change:
  - **"Each factory's hooks"** (`:94-96`): `register` and `build`, the base's two abstract hooks,
    and the six it defaults, `store`, `validate`, `validate_on_startup`, `revalidate`,
    `owned_serials` and `inventory_spec`; and that a registry may map a name to a factory class or
    to an instance of one (§3, §9.5, by anchor);
  - **"What changed after `v0.2.0`"** (`:106-109`): add `v0.2.3`'s change, still linking §9.
- **Nothing else changes.** Check every name and anchor the README mentions, as `actor-names` 02
  did.

### 2.3 `PROVENANCE.md`

Add, after "`actor-names` prompts 01 and 01b: a closed pool releases its actor names (`v0.2.2`)"
(`:160`, the file's last section, which ends at `:203`), a section
**"`factory-defaults` prompt 01: the base defaults three hooks (`v0.2.3`)"**. It says:
- **The change has no source, and is a departure from it.** SGK's base,
  `Datastore/SQL/ObjectFactories/base.py` at `6f7f291` (the file map's source of
  `datastorekit/SQL/factory_base.py`), makes all five hooks abstract, and the package carried that
  over. `factory-defaults` U1, on the user's ruling (2026-10-11), makes `store`, `validate` and
  `validate_on_startup` defaulted, revisiting extraction U32 in part. It fixes no defect of SGK's:
  SGK registers classes, which are never instantiated, so its base's abstractness was never
  enforced on it. Its test module is `datastorekit/tests/test_factory_instances.py`, and
  `docs/client-contract.md` §9.5 gives the detail.
- **What changed in the package**: `datastorekit/SQL/factory_base.py` only: three `@abstractmethod`
  lines removed, the comment on defaulted hooks moved and reworded, and three docstrings added;
  every hook's arguments and body unchanged. In this repository only, outside the wheel:
  `datastorekit/tests/test_neutral_client.py`, the new `datastorekit/tests/client/instances.py` and
  test module, the smoke script's step I, the contract's §9.5 and its markers, verification §4.8
  and §8.1, and the note on extraction U32. The suite went from 494 to 504.
- **The files 01 changed, and its log.**

Change nothing above it. Do not describe SGK's adoption here: G2 is the extraction board's.
`PROVENANCE.md` is outside the package, so it may name SGK and its paths.

### 2.4 The addenda (U5)

Each addendum is dated, says it was written by `factory-defaults` prompt 02, and is added.
**Nothing already in the file is rewritten** (`CLAUDE.md` rule 6): 07a's text, the `v0.2.1`
addendum and the `v0.2.2` addendum all stay as written, true of their releases. Each file gains
two things.

1. **An italic line at its head**, after `actor-names` 02's (`docs/adoption/README.md:12-15`,
   `secondarygwkit.md:21-25`, `champbh.md:22-26`, `stochasticinstantons.md:20-24`). It says that the
   addendum below gives the pin and what changed since `v0.2.2`, and that it supersedes the
   statements it names.
2. **A section `## Addendum: v0.2.3 (factory-defaults prompt 02, <date>)`**, unnumbered, after the
   `v0.2.2` addendum. In each checklist it goes before `## Appendix: the script's output`
   (`secondarygwkit.md:537`, `champbh.md:526`, `stochasticinstantons.md:495`), in the form the
   `v0.2.2` addendum took there. In the README it goes at the end (the `v0.2.2` addendum ends the
   file, at `:363`). The date is the day you write it.

Each addendum states:
- **the pin, by client** (U5): for CPBH and SI,
  `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.3`, in place of `v0.2.2`'s; for
  SGK, `v0.2.2` or `v0.2.3`, SGK's choice, a move being a commit of its own. That amends extraction
  U37 and `actor-names` U3 ("every client adopts the release named") for SGK only;
- **what changed since `v0.2.2`, for that client** (below), with contract §9.5's rows as the
  detail, linked by anchor;
- **which statements it supersedes**, each by `path:line` of the file it is in. At least: the head
  line that says `v0.2.2`; the `v0.2.2` addendum's pin, its sentence that the client adopts
  `v0.2.2`, and its gate statement; and the U32 statements named below;
- **how to read the earlier addenda's citations.** This addendum's head line moves every line
  below it, so the `v0.2.2` addendum's `path:line`s, which are that file's as `actor-names` 02
  committed it, are read at `6d8ee9a`, or N lines later here (say N, and which citations are above
  the insert). The `v0.2.2` addendum did the same for the `v0.2.1` addendum; say that its rule
  still holds, shifted by N;
- **line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, one in the `v0.2.1`
  addendum `v0.2.1`'s, and one in the `v0.2.2` addendum `v0.2.2`'s. A line this addendum cites is
  `v0.2.3`'s tree, whose `datastorekit/` is `f5d8957`'s and 02's.

What each addendum says:

| File | States | Supersedes, at least (each in part, by `path:line`) |
|---|---|---|
| `README.md` | the pins by client (U5); what changed, §1.1's "What a client sees", linked to contract §9.5's three rows; nothing any client supplies or stores changes, and no message; §1.1's measure, per client, in one table; the checklists are not re-measured (as U37), and each has its own addendum | §4's paragraph "The layer never instantiates a factory" (`:130-141`): its account of the base (all five abstract) and its second bullet (a client that registers instances "must give each instantiated class all five", and the two routes). Its first sentence, that the layer never instantiates a factory, and its first bullet still hold; say so |
| `secondarygwkit.md` | SGK may stay on `v0.2.2` or move (U5), and G2 reads "SGK has adopted `v0.2.2` or later"; nothing changes for SGK: it instantiates no factory (§1.1's measure at `b510bc9` and at the `HEAD` you read); item 8 still holds; optionally, §1.1's facts on SGK's adoption, as read, with no gate recorded | item 5's statement that `Datastore/SQL/ObjectFactories/base.py` equals the package's base byte for byte (`:192-194`) was superseded by the `v0.2.1` addendum (its table row for `:187-188` at `33778b0`: they differ in comments and docstrings); add that at `v0.2.3` they also differ by the three decorators, which SGK, registering classes, never meets. And the `v0.2.2` addendum's pin and G2 statement |
| `champbh.md` | CPBH adopts `v0.2.3`, and G3 reads "CPBH has adopted `v0.2.3`"; under `v0.2.3` its 24 registry entries instantiate as they stand, and item 5 asks nothing of its factories but the base's import path (item 3); the defaults are static, so a hook a CPBH class defines with `self` overrides a default as before, and a hook it does not define raises `NotImplementedError`, as CPBH's own base does today (`Datastore/SQL/ObjectFactories/base.py:16-30` at `52142d7`, read through `git`); item 5's other findings (keyed lookups, the layer's own tables, the `inventory()` hooks) are unchanged | item 5's U32 paragraph (`:200-221`): the package's ABC with five abstract hooks, the `TypeError` at instantiation, and "the two routes"; the one-paragraph summary's clause on U32 (`:34-35`); and the `v0.2.2` addendum's pin and G3 statement |
| `stochasticinstantons.md` | SI adopts `v0.2.3`, when it is next active, and G4 reads "SI has adopted `v0.2.3`"; under `v0.2.3` its 18 registry entries and the three import-time instantiations of item 3 instantiate as they stand; item 5's other findings (`InflatonTrajectory`'s `prune_unvalidated`, its validated class) are unchanged | item 3's paragraph on the import-time sites (`:121-126`), in its last clause ("under the package's ABC each raises `TypeError` at import"); item 5's U32 paragraph (`:187-200`); the one-paragraph summary's clause on U32 (`:30-31`); and the `v0.2.2` addendum's pin and G4 statement |

**The line numbers here are the planner's at `97c9a8e`.** Check each against the file before citing
it, and cite what you find, in the file as committed with your addendum. A statement the table does
not name that is no longer true of `v0.2.3` is superseded too, and recorded in the log: grep each
file for `abstract`, `TypeError`, `instanti` and `U32` (planner's grep: the hits above, and SI's
`:76` and `:239` and CPBH's `:244`, which are other `TypeError`s and stay true).

### 2.5 The extraction board's gates

On `../extraction/IMPLEMENTATION_STATE.md` §2:
- **G2**'s title says "SGK adopted `v0.2.2` or later (U37; `actor-names` U3; `factory-defaults`
  U5), fingerprint reproduced";
- **G3**'s and **G4**'s titles say `v0.2.3`, with "(U37; `actor-names` U3; `factory-defaults`
  U5)";
- each of the three rows gains a dated line: `v0.2.3` is ready to be tagged on `factory-defaults`
  02's commit once CI passes there at both ends (as U23 and U28), and 02 makes no tag and pushes
  nothing; and that client's addendum, by anchor.

The lines already there stay as they are, and each row's diff is the row as it was with its title
changed and its line added. G1 is unchanged, and so is the rest of that board. That campaign stays
closed.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **Additive documents.** Everything under `docs/` is additive (`CLAUDE.md` rule 6). An addendum
   that rewrites a line of 07a's or of an earlier addendum fails acceptance. `git diff` of each
   file under `docs/adoption/` shows `+` lines only.
2. **A name or link that does not exist.** Check every module, name, file, anchor and contract row
   that the README, `PROVENANCE.md` and the addenda mention: names by importing them in `venv/`,
   and anchors by finding the heading by GitHub's rule. The log lists each, with how it was
   checked. Contract §9.5's heading is "9.5 `factory-defaults` prompt 01"; derive its anchor, and
   say how. Each new addendum's own anchor, which the head line and the gates link to, is derived
   the same way.
3. **The tag does not exist yet.** The README, the addenda and the gates name `v0.2.3` as of the
   tag. Nothing may say it is tagged.
4. **No client is re-measured beyond §1.1.** Re-run §1.1's measure yourself, read-only through
   `git` (a script of your own in the scratchpad, run with `python -I`, that reads `git show` and
   imports nothing of the client), and record it. If any count differs at the checklists' commits,
   stop. SGK's `HEAD` may have moved: record what you read, and stop only if SGK instantiates a
   factory there.
5. **Offline only.** Every venv and the build are `--offline`. A pin, or the build backend, that
   does not resolve offline is a stop.
6. **`venv/`'s metadata.** After §2.1, `pip show datastorekit` in `venv/` still says `0.2.2`, since
   the editable install records the version when it is installed. Reinstall it offline:
   `uv pip install --offline --no-deps --no-build-isolation --python venv/bin/python -e .`. That
   writes a `datastorekit.egg-info/` at the root, which you delete afterwards. Then run the suite in
   `venv/` again. Nothing else is built in the checkout.
7. **No Ray.** This prompt starts no Ray. The smoke script is not run: no code changes. Its runs
   at 01's tree, verification §4.8, are the release's.
8. **U5's wording.** "SGK may stay on `v0.2.2`" is permission, not advice to stay. No document says
   SGK should or should not move.

---

## 4. Verification

1. **The suite.** In `venv/`, `Ran 504 tests … OK` before and after, with `pip show` saying `0.2.3`
   after. Also at the high end: a fresh offline scratch venv (Python 3.13.16, `ray==2.55.1`,
   `sqlalchemy==2.0.46`, `setuptools`) with a `git archive` of your tree installed editable
   (`--no-deps --no-build-isolation`) gives `Ran 504 tests … OK`. Record the `ResourceWarning`
   lines at each end: 0 in `venv/`; 0 or 4 at the high end, which is timing (`actor-names` log 01,
   correction 8; CI saw 4 on `85f504d`).
2. **The checks.**
   - `compare_ported_tests.py` exits 0 with "20 module(s) … 1 test(s) declared not ported".
   - `black --check datastorekit docs` leaves 74 files unchanged.
   - The two guards pass; they are in the suite.
3. **The release check**, as §1.2. Build from a clean `git archive` of your tree, never in this
   checkout, and install at the high pins, offline. Record:
   - the wheel's name, size, entry count and SHA-256, and its file list;
   - `METADATA`'s `Version`, `Requires-Python` and `Requires-Dist` lines;
   - each command of §1.2, with its output;
   - the `RECORD` comparison with a wheel built from `git archive v0.2.2`.

   `git status` shows no `build/`, `dist/` or `*.egg-info` afterwards.
4. **The documents.** List every remaining `v0.2.2` in `README.md`, `PROVENANCE.md` and
   `docs/adoption/*.md`, each with why it stays: history, a statement an addendum supersedes, SGK's
   permitted pin, or the README's "remain tagged". Also confirm:
   - `git diff` of the four files under `docs/adoption/` has no `-` line;
   - `docs/client-contract.md` and `docs/extraction-verification.md` are unchanged.
5. **The breakage record.** Each item is a change exactly as applied in a scratch export, with
   what failed. None is committed. Check each diff with `git apply --check` and `-R --check` as
   recorded.
   - **(a)** `pyproject.toml`'s version left at `0.2.2`: the release check's `METADATA` and
     `importlib.metadata.version` assertions fail, naming `0.2.2`.
   - **(b)** the `exclude` line removed from `pyproject.toml`: the wheel lists files under
     `datastorekit/tests/`, and `import datastorekit.tests` succeeds.
   - **(c)** the wheel built from `git archive v0.2.2` with only its version set to `0.2.3`: its
     `METADATA` says `0.2.3`, but the `RECORD` comparison with `v0.2.2`'s wheel shows no line
     differing, where the release shows `SQL/factory_base.py`'s, and `__abstractmethods__` has
     five names, and the subclass defining only `register` and `build` raises `TypeError`. The
     check must catch a version number with no change behind it.
6. **The clients.** Record each client's `HEAD` and `git status --short`, at the start and the end.
   CPBH and SI unchanged; SGK's `HEAD` recorded, since another session commits there. None is
   written, run, imported or opened.

---

## 5. Acceptance

1. `pyproject.toml` says `0.2.3`, and nothing else in it changed.
2. `README.md` and `PROVENANCE.md` are as §2.2 and §2.3 say, and every name in them exists.
3. Each of the four files under `docs/adoption/` has its italic line and its addendum, per §2.4,
   and no line of it is rewritten.
4. The extraction board's G2–G4 are as §2.5 says.
5. §4.1–§4.6 hold.
6. **The records**, in the same commit:
   - the log `logs/02-release-v0.2.3.md`, per README §5.1. Besides its sections it has the release
     check, the documents' check (§4.4), every name and link checked (hazard 2), §1.1's measure
     re-run (hazard 4), (a)–(c), and the clients at the start and the end;
   - this board: §1's row for 02 (landed, commit, log), and the header;
   - this campaign's README: its header and §2's row for 02;
   - `docs/OPEN_ISSUES.md`: unchanged at **4**, unless the work opens an issue;
   - `prompts/INDEX.md`: the campaign's line.

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 504, in any venv.
- The release check fails in a way (a)–(c) do not explain.
- §1.1's measure, re-run, differs at the checklists' commits; or SGK instantiates a factory at the
  `HEAD` you read; or a CPBH or SI class lacks `register` or `build`.
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

The campaign closes when `v0.2.3` is tagged on 02's commit after green CI. The orchestrator records
that on this board and on the extraction board's G2–G4, closes the campaign in its header, README
and `prompts/INDEX.md`, in a records commit of its own, and pushes it with the user's approval.
It then gives the user the tag object and commit, for CPBH's prompt 07, with README §0.2's four
points to report back to the ChamPBH session.
