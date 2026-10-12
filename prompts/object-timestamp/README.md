# Campaign — object-timestamp

**Written:** 2026-10-12 by Claude Opus 5.5, at the user's request, from a brief written in a
StochasticInstantons session (§0). **Prompt 01 is written** (2026-10-12). The user took U1–U6 as
recommended the same day (§6.2). Prompt 02, the release, is written after 01 has landed and been reviewed, against the
tree 01 leaves.
**Prompt 01 landed** on 2026-10-12 (`1b2f91a`; [log](logs/01-the-object-carries-a-timestamp.md)),
and was reviewed the same day. **Prompt 02 is written** (2026-10-12, against `75c237e`).
**Prompt 02 landed** on 2026-10-12 (this commit; [log](logs/02-release-v0.3.0.md)): the package is
ready to be released as `v0.3.0`; it is not tagged and not pushed.

## 0. Why this campaign exists

**The user's ruling (2026-10-12):** the change is made here, not in StochasticInstantons (SI). SI
keeps its objects' `timestamp`, and pins a release in which `DatastoreObject` carries it.

The brief that carries the ruling is
`/Users/ds283/Documents/Code/StochasticInstantons/.prompts/dk-and-rpk-migration/datastorekit-v0.2.4-brief.md`,
written 2026-10-12 at DatastoreKit `83068cb` and SI `7bb3efd`. It is evidence, not a specification
(`CLAUDE.md` rule 7): §0.1 re-measures it here, and where it and this repository's records
disagree, the records are right (§0.2). The brief calls the release `v0.2.4` and leaves the number
to this repository (its §4); U6 recommends `v0.3.0`.

**What is missing.** The package owns the `timestamp` column from end to end. A factory whose
`register()` returns `"timestamp": True` gets a `timestamp` `DateTime` column, prepended by the
schema builder (`SQL/schema.py:141-146`; contract §2, `timestamp`). The actor stamps it at insert
(`SQL/Datastore.py:809-815`). A replicated write stamps every shard with the driver's one
timestamp (`SQL/ShardedPool.py:3203`, passed as `insert_timestamp=` at `:3288`, `:3316`, `:3343`,
`:3480`, `:3493`). The check at open compares it (`:1449-1450`) and repairs a missing row only if
its timestamp is the record's start (`:1941-1946`). The inventory reports the earliest and latest
per class (`store_inventory.py:391-392`). But the package's `DatastoreObject`
(`datastorekit/object.py:4-21`) takes `store_id` only. A factory that reads the column back has
nowhere on the package's object to put it, so each client that wants the value must add the
attribute on a subclass of its own.

`object.py` is SGK's file, carried over at extraction (`PROVENANCE.md:19`), and SGK's never had the
attribute. No decision here chose to leave it out: SI's checklist records the difference and leaves
SI the choice (`docs/adoption/stochasticinstantons.md:78-105`, item 2). SI has now chosen, as a
request to the package.

**The change.** `DatastoreObject` gains an optional `timestamp` argument and a read-only
`timestamp` property returning it (U1). **The layer does not set the value**: a factory that reads
a row of a class registered with `"timestamp": True` may pass the row's `timestamp` to the object it
builds, as SI's factories do today. An object not yet stored, built from an insert, or read from a
table without the column, has `timestamp` `None`. Nothing the layer writes or reads changes, and no
message, refusal or exception.

### 0.1 Measurements taken by the planner (2026-10-12)

All at `83068cb`, whose `datastorekit/` is `0de2b16`'s (`v0.2.3`): `git diff --stat 0de2b16 HEAD --
datastorekit pyproject.toml docs/client-contract.md docs/adoption` is empty. The suite gives `Ran
504 tests … OK` in `venv/` (Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39). Nothing was committed.

**The brief's §3, point 1: nothing in the layer inspects an object's attributes in a way a new one
would change. Holds for the layer; not for the suite.**
- `git grep` over `datastorekit/` less `tests/` for `__dict__`, `vars(`, `__eq__`, `__getstate__`,
  `__setstate__`, `__slots__`, `copy.copy` and `deepcopy` finds nothing that touches a stored
  object (the `__reduce__`s in `replication.py` and `SQL/schema.py:541` are of exceptions; the
  `dataclass`es in `store_inventory.py` and `store_reader.py` are the inventory's and the reader's
  own records).
- Every `getattr`/`hasattr` the layer makes of an object reads `_my_id`, `_new_insert`, `_updated`
  or the shard key's field (`SQL/ShardedPool.py:3270-3272`, `:3320`, `:3347`, `:3483`, `:3496`,
  `:3522-3527`, `:3570`, `:3607-3612`). A replicated write compares the controller's answer with
  each replica's by `_my_id` alone (`:3320-3331`, `:3347-3349`, `:3496-3501`, `:3589`), and
  `owned_serials` by the serials it returns. Nothing reaches a new attribute.
- **The suite has one such test, which the brief's search excluded.**
  `tests/test_declared_facts.py:643-646` (`TestTheVersionObject`, ported at extraction 04b,
  `0c66505`) asserts that `vars()` of the pool's version object is exactly `{"_my_id": 1, "label":
  "standin", "_deserialized": True}`. Under the change every `DatastoreObject` has `_timestamp`, so
  the dict gains `"_timestamp": None` and the test fails, twice (its two subtests). U2.

**Point 2: every existing call keeps working.** Every `DatastoreObject.__init__` call in the
package passes `store_id` alone, positionally: 16 in `tests/client/objects.py`, one in
`tests/client/instances.py:49` and one in `tests/test_declared_facts.py:445` (the brief cited four
of the 18). SGK and ChamPBH pass `store_id` alone (they have no other argument to pass). A
defaulted second argument, positional or keyword-only, changes none of them.

**Point 3: no client class would collide with a read-only base property. Holds.** Read through
`git` at each client's `HEAD`, outside its layer and its `prompts/`, `.prompts/`, `docs/` and
`.documents/`:
- SGK and ChamPBH: no `self.timestamp =`, `self._timestamp`, `def timestamp(` or `timestamp =
  property` anywhere, and no use of the word `timestamp` on an object (SGK's matches are a debug
  plotter's argument and test schema builders; ChamPBH has none);
- SI: `def timestamp(` on its own `DatastoreObject` (`Datastore/object.py:44`) and on four plot
  adapters (`plotting/adapters/base.py:84`, `full.py:60`, `gradient.py:132`, `slow_roll.py:65`),
  whose classes descend from `abc.ABC`, not from `DatastoreObject`; and `self.timestamp = …` at
  **12** sites in six test modules (the brief cited four in two), each in a class with no base:
  `tests/test_plot_adapters_golden.py:141`, `:186`; `tests/test_plot_diagnostics_figures.py:75`,
  `:91`, `:119`; `tests/test_plot_gradient_adapter.py:152`, `:584`, `:612`;
  `tests/test_plot_gradient_coupled_driver.py:210`, `:246`; `tests/test_plot_spatial_figures.py:118`;
  `tests/test_plot_spatial_movies.py:127` (by an `ast` read of each enclosing class through `git
  show`). None is a `DatastoreObject`.
- No client sets `self._my_id` outside its layer, so no client subclass skips
  `DatastoreObject.__init__`.

**Point 4: pickling.** An object with one more plain attribute pickles as before; a `datetime`
pickles. The stand-in pool pickles every actor call's result (contract §6, last row), so every
existing test that gets an object already sends one across a pickle, and in the prototype below the
stamped object came back through it.

**SI's calls, re-counted at `7bb3efd`.** 14 direct `DatastoreObject.__init__(self, store_id,
timestamp=timestamp)` and ten `super().__init__(…, timestamp=timestamp)`, each by keyword, as the
checklist lists them (item 2). So a keyword-only argument serves SI as well as a positional one
(U1).

**A prototype.** In a scratch export of `83068cb`, `object.py` was given a keyword-only
`timestamp` stored as `_timestamp` and a read-only property, and nothing else in the layer
changed. With two scratch tests added, over a neutral replicated class outside the registry whose
static factory passes `timestamp=row.timestamp` on a read and nothing on an insert:
1. a get that inserts answers `timestamp` `None`; the row's timestamp is one value on all three
   shards; after a reopen, a get answers a `datetime` equal to it, and so does a get sent to each
   shard's actor directly;
2. the property defaults to `None`, returns what it was given, refuses assignment with
   `AttributeError`, refuses a positional second argument with `TypeError`, and survives
   `ray.cloudpickle`.

Results:
- **low end** (`venv/`): `Ran 506 tests`, `FAILED (failures=2)`: the two subtests of
  `TestTheVersionObject`, and nothing else;
- **high end** (Python 3.13.16 / Ray 2.55.1 / SQLAlchemy 2.0.46, SQLite 3.53.4; an offline scratch
  venv with the export installed editable): the same, and only those;
- **with `"_timestamp": None` added to that test's expected dict**: `test_declared_facts`, the two
  scratch tests and `test_layer_is_generic` give `Ran 35 tests … OK` at both ends. `black --check`
  passes on the changed `object.py`.

`docs/extraction/compare_ported_tests.py` compares a ported test's assertion *skeleton*, not its
arguments (its docstring, rule 2), so the change to `test_declared_facts.py` leaves it at "20
module(s) … 1 test(s) declared not ported"; 01 runs it to show so. `object.py` is in the guard's
scan (`tests/test_layer_is_generic.py:91`); `timestamp` is not in the client vocabulary
(`tests/data/client_vocabulary.json`).

**The clients**, read through `git` only: SGK `ede4062` (clean; `requirements.txt:17` pins
`v0.2.2`); ChamPBH `0e64ef0` (29 entries in `git status --short`; no `datastorekit` line in its
`requirements.txt` yet: it pins `v0.2.3` in its own prompt 07); SI `7bb3efd` (3 entries).

### 0.2 Where the brief and this repository's records differ

None that changes the request. Its citations into the package hold at `83068cb`. To be reported
back to the SI session when the release is tagged:
1. **`vars(version)` in `tests/test_declared_facts.py:643-646`** (§0.1, point 1). The brief's test
   4, "the neutral client's existing objects … their tests pass as they stand", cannot hold for
   this one test under any form that gives the object an instance attribute. U2 updates its
   expected dict by one key.
2. **The counts of sites** are larger than the brief's examples (18 positional calls in the
   package, 12 SI test stand-ins), and every conclusion drawn from them holds.
3. **The version.** By this repository's own criteria, a release that adds API is a minor one
   (extraction U36 made `v0.2.1` patch-level because its fixes "add no API"; `factory-defaults` U5
   made `v0.2.3` patch-level because "no name is added or removed"; `v0.2.0`, which added
   `key_on_version`, was minor). U6 recommends `v0.3.0`, and SI's plan is corrected to match.
4. **The form.** U1 recommends a keyword-only `timestamp`, which the brief left open. SI's 24
   sites work unchanged under it.

## 1. Scope

**In scope:**
- `datastorekit/object.py`: the argument, the attribute and the property (U1);
- the one expected dict of `tests/test_declared_facts.py:643-646` (U2);
- a neutral stamped class and its factory outside the registry, and a test module that a revert
  fails (U3);
- the existing smoke script, run unchanged under real Ray at both ends (U4);
- `docs/client-contract.md` §9.6, and a dated subsection of `docs/extraction-verification.md`
  (`CLAUDE.md` rule 6);
- the release (prompt 02, U6), with adoption addenda.

**Out of scope:**
- **any client repository** (`CLAUDE.md`). SI adopts the release in its own campaign (its prompt
  08);
- **the layer filling `timestamp`**, on a store, on an insert, or on a get's answer. The inserter
  knows the stamp it wrote, so filling it after an insert is a possible later change; it is not
  asked for, and SI does not do it today (`Datastore/object.py:27-29` at `7bb3efd`);
- **any other change to the layer.** Nothing the layer writes or reads changes, and no message,
  refusal or exception;
- the four issues inherited from SGK (`docs/OPEN_ISSUES.md` §1.2), and anything else a prompt
  finds: it is recorded, not fixed (§5 rule 4), unless the user rules otherwise.

## 2. Prompts

| # | Prompt | Covers | Status |
|---|---|---|---|
| 01 | [`01-the-object-carries-a-timestamp.md`](01-the-object-carries-a-timestamp.md) | `DatastoreObject` takes a keyword-only `timestamp` and exposes it read-only (U1); `TestTheVersionObject`'s expected dict (U2); a neutral stamped class and factory outside the registry, and `tests/test_object_timestamp.py` (U3); the smoke script unchanged under real Ray at both ends (U4); contract §9.6; a dated subsection of the verification document. | **landed** 2026-10-12 (`1b2f91a`; [log](logs/01-the-object-carries-a-timestamp.md)), reviewed; U1–U4 taken |
| 02 | [`02-release-v0.3.0.md`](02-release-v0.3.0.md) | `pyproject.toml`, `README.md`, `PROVENANCE.md`; dated addenda to `docs/adoption/` (the README and the three checklists: SI's supersedes item 2's `DatastoreObject.timestamp` paragraph and item 4's line); the extraction board's G3 and G4 (G2 holds, and is unchanged); both ends locally and in CI; **the tag** on its commit after green CI, not by the prompt. | **landed** 2026-10-12 (this commit; [log](logs/02-release-v0.3.0.md)); not tagged, not pushed; U6 taken |

**Order.** 01 → 02. 02 releases what 01 leaves. Each is landed and reviewed on its own (U5).

## 3. Datastores

No prompt opens a store of any client. Tests and the smoke script build their stores in `tempfile`
directories.

## 4. The interfaces between prompts

- **After 01:** `DatastoreObject(store_id, *, timestamp=None)` and its `timestamp` property; the
  neutral stamped class and factory, and the test module (their names and home are 01's to choose,
  its §2.3); contract §9.6; the verification document's new subsection.
- **After 02:** `pyproject.toml` at the version U6 names; the adoption addenda. After its CI passes,
  the tag on 02's commit, and the tag object and commit given to the user for SI's prompt 08.

## 5. The rules this campaign runs under

The project-wide ones in `CLAUDE.md`, plus:

1. **One commit per prompt**, in this repository only.
2. **Every prompt writes a log** to `logs/NN-<name>.md`, using §5.1.
3. **Every prompt updates `IMPLEMENTATION_STATE.md`** in its own commit, plus
   `docs/OPEN_ISSUES.md`.
4. **Do not fix things the prompt did not ask for.** A defect found is recorded with a §3 issue.
   Nothing rides in the release but U1, unless the user rules otherwise.
5. **No prompt edits a client repository.** Reading one through `git` is allowed. Running a
   client's code or tests, or opening a client's store, is not.
6. **No test needs Ray, imports a client, or opens a store outside a `tempfile` directory.** The
   suite count is recorded before and after each prompt; a count that falls is a stop.
7. **Ray is started only by `docs/extraction/ray_smoke_run.py`**, under extraction prompt 11's
   rules as its script embodies them: `ray.init(address="local", …)`, from a scratch venv, with no
   Ray process up before or left after (shells excluded), and never with the suite running.
8. **Deliberate breakage.** Each prompt names mutations its tests must catch. The log records each
   as a diff, exactly as applied, so the orchestrator can replay it with `git apply`. Mutations are
   never committed.
9. **No tag except where a prompt says so** (02), and none is moved or deleted. No prompt pushes.
10. **Verification documents are additive** (`CLAUDE.md` rule 6): a re-run that supersedes a
    measurement is a new dated subsection. A contract row is superseded by a §9 row, not rewritten.

### 5.1 The log template

- the subject, commit and result;
- **What shipped**;
- **Deviations from the prompt**, each classified `STRUCTURALLY REQUIRED`, `IMPLEMENTATION CHOICE`
  or `UNINTENDED DRIFT`;
- **Verification performed**: the suite count before and after, at both ends, and the prompt's own
  checks;
- **The deliberate-breakage record**;
- **Observations not acted on**;
- **State handed to the next prompt**.

## 6. Decisions

### 6.1 Inherited, and not reopened here

The extraction campaign's decisions stand (its README §6), in particular U4 (clients pin a tagged
release), U23 and U28 (a tag is made on its prompt's commit only after CI passes there, each push
and tag with the user's approval), U36 (a fix release is patch-level; U6 reads it) and U41 (the
smoke run). So do `actor-names` U1–U4 and `factory-defaults` U1–U5, except that U6 amends
`factory-defaults` U5 for G3 and G4.

### 6.2 Decisions this campaign needs

- **U1: the form of the change.** *(The change is the user's ruling, 2026-10-12. Its form taken
  2026-10-12, as recommended.)* **Recommended:**
  - `def __init__(self, store_id: Optional[int], *, timestamp: Optional[datetime] = None)`:
    `timestamp` **keyword-only**, stored as `self._timestamp`;
  - `@property def timestamp(self) -> Optional[datetime]: return self._timestamp`, with no setter;
  - a docstring, on the class or the property, saying who sets the value (a factory, from the row
    it read, for a class registered with `"timestamp": True`) and when it is `None` (an object not
    yet stored, one built from an insert, one whose factory does not pass it, or one whose table
    has no column), and that the layer never sets or reads it;
  - `store_id`, `available` and the existing signature's first parameter unchanged.

  SI's 24 sites pass `timestamp=` by keyword (§0.1), so they work unchanged. A keyword-only
  argument also refuses, with `TypeError`, a second positional argument meant for an intermediate
  class's signature (SI has several, such as `DimensionlessQuantity(store_id, value, name,
  timestamp=…)`), where a positional one would take it silently as the timestamp.

  **Rejected:**
  - **positional-or-keyword**, SI's own form (the brief's advice): it serves SI equally, but lets a
    misplaced positional argument become the timestamp without error. It can be relaxed to this
    later without breaking a caller; the reverse cannot;
  - **a class-level default, `_timestamp = None`, set on the instance only when given**: it keeps
    `vars()` of an unstamped object as it was (U2) and would answer `None` for an object unpickled
    from before the release, but an attribute that sometimes lives on the class and sometimes on
    the instance is a trap for the next reader, for a pickle no client keeps;
  - **`getattr(self, "_timestamp", None)` in the property**: robust to a subclass that skips
    `DatastoreObject.__init__`, but `store_id` and `available` already assume `_my_id` is set by
    it, and no client skips it (§0.1);
  - **a setter**, or a public attribute: the value is the row's, and the layer's other properties
    of a stored object are read-only;
  - **the layer filling the value** after an insert or on a get's answer: not asked for (§1).
- **U2: the version object's `vars()` test.** *(Taken 2026-10-12, as recommended.)* **Recommended:** in
  `tests/test_declared_facts.py:643-646`, the expected dict gains `"_timestamp": None`, and nothing
  else in the test or module changes. The test pins that the pool's version object is built by the
  registry's version factory "with the attributes it had" (the module's docstring, item 7); after
  U1 every `DatastoreObject` has one more, and the pin should say so. The port check compares
  assertion skeletons, not arguments, so it is unaffected (§0.1). **Rejected:** U1's class-level
  default, to leave the test as it is (U1); loosening the assertion to a subset, which would stop
  it pinning anything new that appears on the object.
- **U3: the tests.** *(Taken 2026-10-12, as recommended.)* **Recommended:** a new module, `tests/test_object_timestamp.py`, always run,
  on the stand-in pool, with no Ray, every store in a `tempfile` directory; and a neutral module
  under `tests/client/` (01 §2.3) holding a replicated stored class and a **static** factory for it
  (registered as a class, as SGK registers its factories) whose `build` passes
  `timestamp=row.timestamp` when it finds the row and nothing when it inserts, with a function
  returning a copy of the registry and of the replicated tables with the class added, outside
  `registry.py`, as `tests/client/instances.py` is. Tests:
  1. `DatastoreObject(store_id)` has `timestamp` `None`; `DatastoreObject(store_id,
     timestamp=t)` returns `t`, the same object; `store_id` and `available` are as before;
  2. through the pool, on the stamped class: a get that inserts answers `timestamp` `None` (the
     layer does not fill it); the row's timestamp is one value on every shard; after a reopen a
     get answers a `datetime` equal to it, and a get sent to each shard's actor directly answers
     the same value;
  3. assigning `timestamp` raises `AttributeError`, and so does deleting it;
  4. a second positional argument raises `TypeError`;
  5. a stamped object round-trips `ray.cloudpickle` with its timestamp, and an unstamped one with
     `None`, as `test_factory_instances` test 5 does for a factory.

  The neutral client's registry and objects are unchanged, and their tests pass as they stand but
  for U2's one dict. **Rejected:** making an existing neutral factory pass `timestamp` (for
  example `gauge_setting`'s), which changes the objects every module gets for a fact one module
  shows; adding the stamped class to the registry, which moves every count the registry's tests
  pin (the schema witness, the drop groups, the inventory); a test of `object_store` with a stamped
  object, which would need the stamped factory to define `store` and would show what that factory
  writes, not what the layer does.
- **U4: Ray.** *(Taken 2026-10-12, as recommended.)* **Recommended:** no new smoke step. 01 runs `docs/extraction/ray_smoke_run.py`,
  unchanged, under real Ray at both ends, every step `PASS`: every object a real actor answers is
  then a `DatastoreObject` with `_timestamp`, crossing Ray's serialisation. **Rejected:** a new
  step that gets a stamped row under Ray: the stand-in pool already pickles every result, test 5
  round-trips `ray.cloudpickle`, and a `datetime` is a standard picklable value, so the step would
  show nothing the suite does not; no Ray run at all, since the run is cheap and is how every
  earlier change to what crosses an actor was checked.
- **U5: the shape.** *(Taken 2026-10-12, as recommended.)* **Recommended:** two prompts, as `actor-names` and `factory-defaults` were: 01
  the change and its evidence; 02 the release, written after 01 is reviewed. The commit boundary is
  the rollback boundary, and 02's four addenda are reviewed against a settled tree. **Rejected:**
  one prompt for change and release, which puts the code and four adoption documents in one review
  and one revert.
- **U6: the release, and who adopts it.** *(Taken 2026-10-12, as recommended. Needed by 02, not 01.)* **Recommended:**
  - **`v0.3.0`**, minor: the release adds a constructor argument and a property to a public class.
    That is added API, which extraction U36 and `factory-defaults` U5 each gave as the reason a
    release was *not* minor, and which made `v0.2.0` minor. It is also not additive for every
    conceivable client: a subclass that assigns `self.timestamp` would now raise. None of the three
    does (§0.1), but the version should say a client must look;
  - **SI adopts it**, and with it keeps its 24 sites as they stand once their import is rewritten;
    G4 reads "SI has adopted `v0.3.0`";
  - **ChamPBH and SGK may stay on their pins or move**, each in a commit of its own, as it chooses:
    neither reads the value back, and nothing they call changes. G3 reads "`v0.2.3` or later", G2
    "`v0.2.2` or later". This amends `factory-defaults` U5 for G3 and G4.

  **Rejected:** **`v0.2.4`**, the brief's name, treating an added argument and property as a
  patch: defensible, since nothing any client calls changes, but it breaks the line U36 drew;
  requiring ChamPBH or SGK to move, a pin change mid-adoption that changes nothing they meet.

## 7. Gates outside this repository

The extraction campaign's G2–G4 (each client's adoption) are recorded on the extraction board when
they hold. Under U6, G4 reads the new release once it is tagged, G3 "`v0.2.3` or later" and G2
"`v0.2.2` or later"; 02's addenda say so. This campaign does not wait for them. SI's prompts 01–07
do not wait for the release; its 08 does. If the release has not been tagged when SI's 08 is due,
SI's fallback is a class of its own (the brief, §5); that is SI's decision, not this campaign's.
