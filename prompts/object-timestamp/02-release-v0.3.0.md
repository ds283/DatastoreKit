# Prompt 02 — release `v0.3.0`

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

*Written 2026-10-12 against `75c237e`, whose `datastorekit/` and `docs/` are `1b2f91a`'s (prompt
01's).*

**Gate:**
- 01 landed (`1b2f91a`) and was reviewed (`d88615e`). CI passed on `d88615e` at both ends,
  [run 38190920683](https://github.com/ds283/DatastoreKit/actions/runs/38190920683), recorded at
  `75c237e`.
- U6 is taken (README §6.2): `v0.3.0`, minor; SI adopts it (G4); CPBH may stay on `v0.2.3` or move
  (G3, "`v0.2.3` or later"); SGK may stay on `v0.2.2` or move (G2, "`v0.2.2` or later").
- `git status` is clean in this repository, and `origin/main` is an ancestor of `main`.
- This board's §3 holds no issue, and `docs/OPEN_ISSUES.md` counts 4, all on `inherited-issues`'
  board.

**Closes:** nothing. **Narrows:** nothing. **Changes:** nothing in the package but its version.
**Opens:** only what the work finds.

**Recommended model:** **Opus.**
- No line of code changes. The work is three short edits, four dated addenda and two gates.
- The addenda are not alike. For SI the release removes an obligation its checklist spells out at
  length (item 2's `DatastoreObject.timestamp` paragraph, and item 4's line); for CPBH and SGK it
  changes nothing they meet, and both may stay where they are. Each addendum must say exactly that,
  and supersede by `path:line` without rewriting a word.
- Each file's head gains a line, which moves every citation below it, including the `v0.2.3`
  addendum's own table. The addendum must say how to read those, as `factory-defaults` 02 did.
- The release check and both ends of the suite are run as `factory-defaults` 02 ran them, offline.

**Read first:**

1. [`README.md`](README.md): §0 (§0.1 and §0.2 especially), §1, §2, §4, §5 (rules 4, 5, 9 and 10),
   §6.2 (U1 and U6), §6.1 (the inherited U23, U28, U36 and U37, `actor-names` U3 and
   `factory-defaults` U5) and §7.
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`, above all "Releases".
3. This board's review of 01, and log 01 (`logs/01-the-object-carries-a-timestamp.md`), §1 and §8.
4. `factory-defaults` prompt 02 (`../factory-defaults/02-release-v0.2.3.md`) and its log
   (`../factory-defaults/logs/02-release-v0.2.3.md`). 02 is that prompt again, for one change.
   Their release check, their addenda's form and their breakages are this prompt's.
5. The files 02 changes, as they stand: `pyproject.toml`, `README.md`, `PROVENANCE.md`,
   `docs/adoption/README.md` and the three checklists. In each, read the head, and the `v0.2.3`
   addendum in full; in SI's checklist, also the one-paragraph summary (`:35-41`), item 2's
   `DatastoreObject.timestamp` paragraph (`:78-105`) and item 4's list (`:134-160`).
6. `docs/client-contract.md` §6 and §9.6, which 02 points at and does not change.
7. The extraction board's §2 (G1–G4), `../extraction/IMPLEMENTATION_STATE.md:1532-1541`. G2 holds
   (2026-10-12, recorded at `6465a6a`: SGK adopted `v0.2.2`).

Facts below are at `75c237e`, measured on 2026-10-12.

---

## 1. What is wanted

02 makes the package ready to be released as **`v0.3.0`** (U6). After it:

- `pyproject.toml` says `0.3.0`;
- `README.md` and `PROVENANCE.md` describe `v0.3.0`;
- `docs/adoption/` carries a dated addendum, in its README and in each checklist, giving the pin and
  what changed for that client since `v0.2.3`;
- the extraction board's gates say that SI adopts `v0.3.0` (G4), that CPBH adopts `v0.2.3` or later
  (G3), and that the tag waits for CI. G2, which holds, is not changed.

**No line of code changes.** Nothing under `datastorekit/` is touched, and the suite stays at
**509**.

**02 makes no tag and pushes nothing** (U23, U28; README §5 rule 9). After its review, its commit
is pushed as `main`. `v0.3.0` is made on it, annotated, only once CI passes there at both ends, as
`v0.2.3` was. If CI fails, a fix prompt lands first, and no tag is ever made on a commit whose CI
is red. The tag is not this prompt's work.

### 1.1 What changed since `v0.2.3`, measured

One prompt changed the package after `v0.2.3` (`0de2b16`): 01, `1b2f91a` (U1, the user's ruling).

- **In the wheel, only `object.py` changed**: `from datetime import datetime`; `__init__` gains a
  keyword-only `timestamp: Optional[datetime] = None` and the assignment `self._timestamp =
  timestamp`; a `timestamp` property, with a docstring and no setter or deleter (`git diff
  --numstat 0de2b16 1b2f91a -- datastorekit/object.py`: 18 added, 1 removed). `store_id` and
  `available` are `v0.2.3`'s (the review's `ast` comparison, board §1). Two wheels built offline,
  from `git archive v0.2.3` and from `75c237e` with only the version changed, have the same 20
  `RECORD` lines under `datastorekit/` but `object.py`'s.
- **Outside the wheel**: `datastorekit/tests/test_declared_facts.py` changed by one expected dict;
  `datastorekit/tests/client/stamped.py` and `datastorekit/tests/test_object_timestamp.py` are new
  (5 tests: 504 → 509); the contract gained §9.6 and its head line, and the verification document
  §4.9. The smoke script is unchanged.

**What a client sees** (contract §9.6). Nothing the layer writes or reads changes, and no message,
refusal or exception of the layer's. What changes is the package's stored object:
- **`DatastoreObject(store_id, *, timestamp=None)`** keeps `timestamp`, and **`obj.timestamp`**
  returns it. The argument is keyword-only, and the property read-only.
- **The layer never sets it and never reads it.** A factory that reads a row of a class whose
  `register()` declares `"timestamp": True` may pass the row's `timestamp`; it is `None` for an
  object not yet stored, one built from an insert, one whose factory does not pass it, and one
  whose table has no such column.
- **Two things a client can now meet:** every `DatastoreObject` has `_timestamp` in its `vars()`
  (`None` unless given); and a subclass that assigns or deletes `self.timestamp` now raises
  `AttributeError`. A second positional argument raised `TypeError` at `v0.2.3` and still does,
  with the same message.

This is added API, so the release is minor (U6, reading extraction U36 and `factory-defaults` U5).

**What the clients do with it**, read through `git` only. The planner's measure, a script of `ast`
reads of every `.py` file from `git show <commit>:<path>`, outside each client's `prompts/`,
`.prompts/`, `docs/` and `.documents/`: where `DatastoreObject` comes from; the classes descending
from it by name; every `DatastoreObject.__init__(…)`, and every `super().__init__(…)` in a class
whose bases name `DatastoreObject`, by its positional and keyword arguments; every `def timestamp`,
class-level `timestamp` or `_timestamp`, and `self.timestamp`/`self._timestamp` assignment or
deletion, with whether its class descends from `DatastoreObject`.

| Client, commit | `DatastoreObject` from | Descendants | `__init__` calls (store_id alone / with `timestamp=` / other) | `timestamp` defined or assigned in a descendant |
|---|---|---|---|---|
| SGK `d03a643` (its `HEAD` at writing; it has adopted `v0.2.2`) | the package (`from datastorekit import DatastoreObject`, 19) | 30 | 38 / 0 / 0 | none |
| CPBH `64ef9aa` (its `HEAD` at writing; not yet adopted) | its own `Datastore/object.py` | 31 | 19 / 0 / 0 | none |
| SI `7bb3efd` | its own `Datastore/object.py`, whose `__init__` takes `timestamp` positional-or-keyword and whose `timestamp` is a read-only property (`:25-30`, `:43-45`) | 34 | 9 / 14 / 0 | only its own `DatastoreObject` (`:30`, `:44`), which leaves with its layer |

And for SI, outside its `DatastoreObject`: `def timestamp` at five sites, none a descendant (four
plot adapters, `plotting/adapters/base.py:84`, `full.py:60`, `gradient.py:132`, `slow_roll.py:65`,
and a test stand-in, `tests/test_plot_adapters_golden.py:870`, which README §0.1 did not list);
`self.timestamp = …` at 12 sites, none a descendant (README §0.1's list); no `.timestamp` or
`._timestamp` assigned on any other object. 18 of SI's factory modules pass `timestamp=`.
No client has a `vars()` or `__dict__` read of a stored object (CPBH's one `vars(` is of a module,
`Datastore/tests/test_compare_stores.py:735`; SGK's two `__dict__`s are of classes), and none keeps
a pickled `DatastoreObject` on disk (SI's `joblib.dump` in `regression_InstantonOutputs.py:370` is
of regression models).

So:
- **SI**: its 14 direct calls and ten pass-throughs (its checklist, item 2) pass `timestamp=` by
  keyword, so each works under `v0.3.0` once its import is rewritten; its reads of `.timestamp`
  (three direct, two by `getattr`) get what its factories pass; its stand-ins are not
  `DatastoreObject`s. Item 2's `DatastoreObject.timestamp` paragraph no longer asks anything of SI,
  and item 4's line no longer leaves the layer.
- **CPBH and SGK** pass `store_id` alone, and define and assign no `timestamp` on a descendant.
  `v0.3.0` changes nothing they meet but one key in `vars()`, which none of them reads.

**The clients' pins at writing**, read through `git`: SGK `requirements.txt:17` pins `v0.2.2`; CPBH
has no `datastorekit` line at `64ef9aa` (it pins in its own prompt 07); SI has none. SGK's and
CPBH's `HEAD`s move often (other sessions work there); record what you read, and compare nothing
but the table's facts.

### 1.2 The release check, probed

The planner probed the release on this machine, offline, as `factory-defaults` 02 did.
- **The build.** From a `git archive` of `75c237e` with only `version = "0.3.0"` changed,
  `uv build --offline --wheel` gives `datastorekit-0.3.0-py3-none-any.whl` (99,488 bytes). It has
  25 entries, none under `datastorekit/tests/`. `METADATA` says `Version: 0.3.0`,
  `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43` and `Requires-Dist:
  sqlalchemy<2.1,>=2.0.39`.
- **The install.** `uv venv --offline -p /opt/local/bin/python3.13`, then `uv pip install
  --offline <wheel> "ray==2.55.1" "sqlalchemy==2.0.46"`.
- **The run**, from a directory outside the repository with `PYTHONPATH` unset:
  - `datastorekit` imports from the venv's `site-packages`;
  - `importlib.metadata.version("datastorekit")` is `0.3.0`;
  - `inspect.signature(DatastoreObject)` has `store_id` `POSITIONAL_OR_KEYWORD` and `timestamp`
    `KEYWORD_ONLY` with default `None`; `DatastoreObject.timestamp.fset` and `.fdel` are `None`;
  - `DatastoreObject(3, timestamp=t).timestamp is t`; `DatastoreObject(3).timestamp` is `None`,
    and its `vars()` is `{'_my_id': 3, '_timestamp': None}`; `DatastoreObject(3, t)` raises
    `TypeError` ("takes 2 positional arguments but 3 were given"); assigning `timestamp` raises
    `AttributeError` ("property 'timestamp' of 'DatastoreObject' object has no setter"); a stamped
    object round-trips `pickle` with its timestamp;
  - `import datastorekit.tests` raises `ModuleNotFoundError`;
  - `python -m datastorekit.tools.sharded_store --help` exits 0.
- **Against `v0.2.3`'s wheel**, built from `git archive v0.2.3`: of the 20 `RECORD` lines under
  `datastorekit/`, only `object.py`'s differs.
- **Breakage (b), probed:** with the `exclude` line removed, the wheel has 76 entries, 51 of them
  under `datastorekit/tests/`.
- **Breakage (c), probed:** a wheel built from `git archive v0.2.3` with only its version set to
  `0.3.0` has no `RECORD` line differing from `v0.2.3`'s.

The wheel's bytes are not reproducible across builds (file times). Record the SHA-256 of yours,
and do not compare it with the planner's. The `RECORD` lines are content hashes, and do compare.

---

## 2. What to change

### 2.1 `pyproject.toml`

`version = "0.3.0"` (`:7`). Nothing else. No other file carries the version.

### 2.2 `README.md`

- **Status.** A paragraph for **`v0.3.0`**, above `v0.2.3`'s (`README.md:10-19`):
  - it is a minor release with one change, `object-timestamp` prompt 01, on the user's ruling:
    `DatastoreObject` takes an optional, keyword-only `timestamp` and exposes it as a read-only
    property;
  - the layer never sets it and never reads it: a factory that reads a row of a class registered
    with `"timestamp": True` may pass the row's value, and it is `None` otherwise;
  - what a client can now meet: one more key, `_timestamp`, in an object's `vars()`, and
    `AttributeError` from a subclass that assigns `self.timestamp`;
  - nothing the layer writes or reads changes, and no message, refusal or exception of the layer's;
  - it adds API, so it is a minor release;
  - it points at contract §9.6 for the detail, by its anchor.
- **Installing.** The pin is `v0.3.0` (`:83`). Replace `:86-89` with what U6 says, as of the tag:
  - `v0.2.3`, `v0.2.2`, `v0.2.1`, `v0.2.0` and `v0.1.0` remain tagged, and no tag is moved or
    deleted;
  - StochasticInstantons adopts `v0.3.0`; ChamPBH may stay on `v0.2.3` and SecondaryGWKit on
    `v0.2.2`, or either may move, in a commit of its own, as it chooses: neither reads the value
    back, and nothing they call changes.

  Name no client's paths. The README is committed before the tag exists, and is true once it does.
- **Using it.** One item changes: **"What changed after `v0.2.0`"** (`:121-125`) adds `v0.3.0`'s
  change, that a stored object may carry its row's `timestamp`, still linking §9. If you add a
  link to §9.6 there, derive its anchor (hazard 2).
- **Nothing else changes.** Check every name and anchor the README mentions, as `factory-defaults`
  02 did.

### 2.3 `PROVENANCE.md`

Add, after "`factory-defaults` prompt 01: the base defaults three hooks (`v0.2.3`)" (`:205`, the
file's last section, which ends at `:240`), a section **"`object-timestamp` prompt 01: the object
carries a timestamp (`v0.3.0`)"**. It says:
- **The change has no source in SGK.** SGK's `Datastore/object.py` at `6f7f291` (the file map's
  source of `datastorekit/object.py`) takes `store_id` alone, and the package carried it over.
  StochasticInstantons' own `DatastoreObject` (SI `Datastore/object.py`, added at SI `51b04f8`,
  2026-06-21) takes a `timestamp` and exposes it read-only; SI asked the package for the same
  (README §0, the brief). `object-timestamp` U1, on the user's ruling (2026-10-12), adds it,
  **keyword-only**, where SI's is positional-or-keyword. It fixes no defect. Its test module is
  `datastorekit/tests/test_object_timestamp.py`, and `docs/client-contract.md` §9.6 gives the
  detail.
- **What changed in the package**: `datastorekit/object.py` only (18 lines added and 1 removed):
  the import, the keyword-only argument and its assignment, and the read-only property; `store_id`
  and `available` unchanged. In this repository only, outside the wheel: one expected dict of
  `datastorekit/tests/test_declared_facts.py`, the new `datastorekit/tests/client/stamped.py` and
  test module, the contract's §9.6, and the verification document's §4.9. The suite went from 504
  to 509.
- **The files 01 changed, and its log.**

Change nothing above it. `PROVENANCE.md` is outside the package, so it may name SGK and SI and
their paths.

### 2.4 The addenda (U6)

Each addendum is dated, says it was written by `object-timestamp` prompt 02, and is added.
**Nothing already in the file is rewritten** (`CLAUDE.md` rule 6): 07a's text and the `v0.2.1`,
`v0.2.2` and `v0.2.3` addenda all stay as written, true of their releases. Each file gains two
things.

1. **An italic line at its head**, after `factory-defaults` 02's (`docs/adoption/README.md:17-20`,
   `secondarygwkit.md:27-31`, `champbh.md:28-32`, `stochasticinstantons.md:26-30`). It says that
   the addendum below gives the pin and what changed since `v0.2.3`, and that it supersedes the
   statements it names.
2. **A section `## Addendum: v0.3.0 (object-timestamp prompt 02, <date>)`**, unnumbered, after the
   `v0.2.3` addendum. In each checklist it goes before `## Appendix: the script's output`
   (`secondarygwkit.md:629`, `champbh.md:616`, `stochasticinstantons.md:581`), in the form the
   `v0.2.3` addendum took there. In the README it goes at the end (the `v0.2.3` addendum ends the
   file, at `:470`). The date is the day you write it.

Each addendum states:
- **the pin, by client** (U6): for SI, `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.3.0`,
  in place of `v0.2.3`'s, when it is next active; for CPBH, `v0.2.3` or `v0.3.0`, CPBH's choice;
  for SGK, `v0.2.2`, `v0.2.3` or `v0.3.0`, SGK's choice; a move being a commit of the client's own.
  That amends `factory-defaults` U5 for G3 (CPBH) and keeps it for G2 (README §6.1);
- **what changed since `v0.2.3`, for that client** (below), with contract §9.6's row as the detail,
  linked by anchor;
- **which statements it supersedes**, each by `path:line` of the file it is in. At least: the head
  line that says `v0.2.3`; the `v0.2.3` addendum's pin, its sentence that the client adopts
  `v0.2.3` (CPBH, SI) and its gate statement; and SI's statements named below;
- **how to read the earlier addenda's citations.** This addendum's head line moves every line
  below it, so the `v0.2.3` addendum's `path:line`s, which are that file's as `factory-defaults` 02
  committed it, are read at `0de2b16`, or N lines later here (say N, and which citations are above
  the insert). The `v0.2.3` addendum did the same for the `v0.2.2` and `v0.2.1` addenda; say that
  its rule still holds, shifted by N;
- **line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, one in the `v0.2.1`
  addendum `v0.2.1`'s, one in the `v0.2.2` addendum `v0.2.2`'s, and one in the `v0.2.3` addendum
  `v0.2.3`'s. A line this addendum cites is `v0.3.0`'s tree, whose `datastorekit/` is `1b2f91a`'s
  and 02's.

What each addendum says:

| File | States | Supersedes, at least (each in part, by `path:line`) |
|---|---|---|
| `README.md` | the pins by client (U6); what changed, §1.1's "What a client sees", linked to contract §9.6's row; nothing any client supplies or stores changes, and no message; §1.1's measure, per client, in one table; the checklists are not re-measured (as U37), and each has its own addendum | the `v0.2.3` addendum's pins (`:382-391`), its sentence that `v0.2.3` carries the earlier releases' changes (`:393-394`), and its "What this addendum supersedes" rows that give the pins and gates (`:462-463`, `:470`, and any other you find); and §2's module-map row for `DatastoreObject` (`:81`) **only if** it says something `v0.3.0` makes untrue (it maps a module; read it and say) |
| `secondarygwkit.md` | SGK adopted `v0.2.2` (G2 holds, 2026-10-12, the extraction board) and may stay or move (U6); nothing changes for SGK: it passes `store_id` alone at 38 sites and defines or assigns no `timestamp` on a `DatastoreObject` (§1.1's measure at the `HEAD` you read); its objects gain one key in `vars()`, which it does not read; item 8 still holds | the `v0.2.3` addendum's pin and G2 statement (`:551-562` and its table rows that give them) |
| `champbh.md` | CPBH may stay on `v0.2.3` or move (U6), and G3 reads "CPBH has adopted `v0.2.3` or later"; nothing changes for CPBH: 19 sites pass `store_id` alone, and no descendant defines or assigns `timestamp` (its own `DatastoreObject` leaves with its layer, item 2); its factories, most of whose classes declare `"timestamp": True` (item 5's table), may pass the row's value if CPBH chooses, and need not | the `v0.2.3` addendum's pin, its sentence that CPBH adopts `v0.2.3`, and its G3 statement (`:540-545` and its table rows that give them) |
| `stochasticinstantons.md` | SI adopts `v0.3.0`, when it is next active, and G4 reads "SI has adopted `v0.3.0`"; under `v0.3.0` the package's `DatastoreObject` takes `timestamp` keyword-only and exposes it read-only, as SI's own does but for the keyword; SI's 14 direct calls and ten pass-throughs pass it by keyword and work as they stand once the import is rewritten (item 3); its reads of `.timestamp` get what its 18 factory modules pass; its plot adapters and test stand-ins are not `DatastoreObject`s, and are unaffected; so item 2's paragraph asks nothing of SI, and `DatastoreObject.timestamp` does not leave the layer (item 4); the rest of items 2 and 4 is unchanged | the one-paragraph summary's clause that SI's `DatastoreObject` "carries a `timestamp`, which the package's lacks" (`:39`); item 2's paragraph (`:78-105`): that the 14 direct calls "raise `TypeError`", that the direct reads "would raise `AttributeError`" and the `getattr` reads "would quietly get `None`", and "Whether SI drops the timestamp or keeps it on its own classes is SI's choice"; item 4's line (`:154`); and the `v0.2.3` addendum's pin and G4 statement (`:509-514` and its table rows that give them) |

**The line numbers here are the planner's at `75c237e`.** Check each against the file before citing
it, and cite what you find, in the file as committed with your addendum. A statement the table does
not name that is no longer true of `v0.3.0` is superseded too, and recorded in the log: grep each
file for `timestamp`, `DatastoreObject`, `v0.2.3` and `TypeError` (planner's grep: the hits above;
the factory tables' `timestamp` columns, CPBH's `:345-348` and SI's `:319` on the replicated
stamp, and every import-map row naming `DatastoreObject`, all of which stay true).

### 2.5 The extraction board's gates

On `../extraction/IMPLEMENTATION_STATE.md` §2:
- **G3**'s title says "CPBH adopted `v0.2.3` or later (U37; `actor-names` U3; `factory-defaults`
  U5; `object-timestamp` U6)";
- **G4**'s title says "SI adopted `v0.3.0` (U37; `actor-names` U3; `factory-defaults` U5;
  `object-timestamp` U6)";
- each of the two rows gains a dated line: `v0.3.0` is ready to be tagged on `object-timestamp`
  02's commit once CI passes there at both ends (as U23 and U28), and 02 makes no tag and pushes
  nothing; and that client's addendum, by anchor.

The lines already there stay as they are, and each row's diff is the row as it was with its title
changed and its line added. **G1 and G2 are unchanged** (G2 holds, and "`v0.2.2` or later" is
already U6's reading), and so is the rest of that board. That campaign stays closed.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **Additive documents.** Everything under `docs/` is additive (`CLAUDE.md` rule 6). An addendum
   that rewrites a line of 07a's or of an earlier addendum fails acceptance. `git diff` of each
   file under `docs/adoption/` shows `+` lines only.
2. **A name or link that does not exist.** Check every module, name, file, anchor and contract row
   that the README, `PROVENANCE.md` and the addenda mention: names by importing them in `venv/`,
   and anchors by finding the heading by GitHub's rule. The log lists each, with how it was
   checked. Contract §9.6's heading is "9.6 `object-timestamp` prompt 01"; derive its anchor, and
   say how. Each new addendum's own anchor, which the head line and the gates link to, is derived
   the same way.
3. **The tag does not exist yet.** The README, the addenda and the gates name `v0.3.0` as of the
   tag. Nothing may say it is tagged.
4. **No client is re-measured beyond §1.1.** Re-run §1.1's measure yourself, read-only through
   `git` (a script of your own in the scratchpad, run with `python -I`, that reads `git show` and
   imports nothing of the client), at SI `7bb3efd` and at the `HEAD`s of SGK and CPBH you read, and
   record it. If SI's counts differ, stop. If SGK or CPBH at the `HEAD` you read passes anything
   but `store_id` to a `DatastoreObject`, or defines or assigns `timestamp` on a descendant, stop.
5. **Offline only.** Every venv and the build are `--offline`. A pin, or the build backend, that
   does not resolve offline is a stop.
6. **`venv/`'s metadata.** After §2.1, `pip show datastorekit` in `venv/` still says `0.2.3`, since
   the editable install records the version when it is installed. Reinstall it offline:
   `uv pip install --offline --no-deps --no-build-isolation --python venv/bin/python -e .`. That
   writes a `datastorekit.egg-info/` at the root, which you delete afterwards. Then run the suite in
   `venv/` again. Nothing else is built in the checkout.
7. **No Ray.** This prompt starts no Ray. The smoke script is not run: no code changes. Its runs
   at 01's tree, verification §4.9, are the release's.
8. **U6's wording.** "CPBH may stay on `v0.2.3`" and "SGK may stay on `v0.2.2`" are permission,
   not advice to stay. No document says CPBH or SGK should or should not move.
9. **Run from the right place.** Every scratch-venv command runs with its export, or a directory
   outside the repository, as the working directory: run from this checkout, `python -c`/`-m` puts
   the checkout first on `sys.path` (`object-timestamp` 01's note). Print `datastorekit.__file__`
   once in each venv and record it.

---

## 4. Verification

1. **The suite.** In `venv/`, `Ran 509 tests … OK` before and after, with `pip show` saying `0.3.0`
   after. Also at the high end: a fresh offline scratch venv (Python 3.13.16, `ray==2.55.1`,
   `sqlalchemy==2.0.46`, `setuptools`) with a `git archive` of your tree installed editable
   (`--no-deps --no-build-isolation`) gives `Ran 509 tests … OK`. Record the `ResourceWarning`
   lines at each end: 0 in `venv/`; 0 or 4 at the high end, which is timing (`actor-names` log 01,
   correction 8; CI saw 0 on `d88615e`).
2. **The checks.**
   - `compare_ported_tests.py` exits 0 with "20 module(s) … 1 test(s) declared not ported".
   - `black --check datastorekit docs` leaves 76 files unchanged.
   - The two guards pass; they are in the suite.
3. **The release check**, as §1.2. Build from a clean `git archive` of your tree, never in this
   checkout, and install at the high pins, offline. Record:
   - the wheel's name, size, entry count and SHA-256, and its file list;
   - `METADATA`'s `Version`, `Requires-Python` and `Requires-Dist` lines;
   - each command of §1.2, with its output;
   - the `RECORD` comparison with a wheel built from `git archive v0.2.3`.

   `git status` shows no `build/`, `dist/` or `*.egg-info` afterwards.
4. **The documents.** List every remaining `v0.2.3` in `README.md`, `PROVENANCE.md` and
   `docs/adoption/*.md`, each with why it stays: history, a statement an addendum supersedes,
   CPBH's or SGK's permitted pin, or the README's "remain tagged". Also confirm:
   - `git diff` of the four files under `docs/adoption/` has no `-` line;
   - `docs/client-contract.md` and `docs/extraction-verification.md` are unchanged.
5. **The breakage record.** Each item is a change exactly as applied in a scratch export, with
   what failed. None is committed. Check each diff with `git apply --check` and `-R --check` as
   recorded.
   - **(a)** `pyproject.toml`'s version left at `0.2.3`: the release check's `METADATA` and
     `importlib.metadata.version` assertions fail, naming `0.2.3`.
   - **(b)** the `exclude` line removed from `pyproject.toml`: the wheel lists files under
     `datastorekit/tests/`, and `import datastorekit.tests` succeeds.
   - **(c)** the wheel built from `git archive v0.2.3` with only its version set to `0.3.0`: its
     `METADATA` says `0.3.0`, but the `RECORD` comparison with `v0.2.3`'s wheel shows no line
     differing, where the release shows `object.py`'s; `inspect.signature(DatastoreObject)` has no
     `timestamp`; and `DatastoreObject(3, timestamp=t)` raises `TypeError`. The check must catch a
     version number with no change behind it.
6. **The clients.** Record each client's `HEAD` and `git status --short`, at the start and the end.
   SI unchanged; SGK's and CPBH's `HEAD`s recorded, since other sessions commit there. None is
   written, run, imported or opened.

---

## 5. Acceptance

1. `pyproject.toml` says `0.3.0`, and nothing else in it changed.
2. `README.md` and `PROVENANCE.md` are as §2.2 and §2.3 say, and every name in them exists.
3. Each of the four files under `docs/adoption/` has its italic line and its addendum, per §2.4,
   and no line of it is rewritten.
4. The extraction board's G3 and G4 are as §2.5 says, and G1 and G2 are unchanged.
5. §4.1–§4.6 hold.
6. **The records**, in the same commit:
   - the log `logs/02-release-v0.3.0.md`, per README §5.1. Besides its sections it has the release
     check, the documents' check (§4.4), every name and link checked (hazard 2), §1.1's measure
     re-run (hazard 4), (a)–(c), and the clients at the start and the end;
   - this board: §1's row for 02 (landed, commit, log), and the header;
   - this campaign's README: its header and §2's row for 02;
   - `docs/OPEN_ISSUES.md`: unchanged at **4**, unless the work opens an issue;
   - `prompts/INDEX.md`: the campaign's line.

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 509, in any venv.
- The release check fails in a way (a)–(c) do not explain.
- §1.1's measure, re-run, differs for SI at `7bb3efd`; or SGK or CPBH, at the `HEAD` you read,
  passes anything but `store_id` to a `DatastoreObject`, or defines or assigns `timestamp` on a
  descendant.
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
  - the extraction board's §2 (G3 and G4), per §2.5;
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

The campaign closes when `v0.3.0` is tagged on 02's commit after green CI. The orchestrator records
that on this board and on the extraction board's G3 and G4, closes the campaign in its header,
README and `prompts/INDEX.md`, in a records commit of its own, and pushes it with the user's
approval. It then gives the user the tag object and commit, for SI's prompt 08, with README §0.2's
four points to report back to the StochasticInstantons session, and one more: SI has a sixth
`def timestamp`, a test stand-in at `tests/test_plot_adapters_golden.py:870`, which is not a
`DatastoreObject` and is unaffected (§1.1).
