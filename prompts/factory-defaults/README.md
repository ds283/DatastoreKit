# Campaign — factory-defaults

**Written:** 2026-10-11 by Claude Opus 5.5, at the user's request, from a brief written in a
ChamPBH session (§0). **Prompt 01 is written** (2026-10-11). The user took U1–U5 as recommended the
same day (§6.2), U1 after its wording was clarified (below). Prompt 02,
the release, is written after 01 has landed and been reviewed, against the tree 01 leaves.

## 0. Why this campaign exists

**The user's ruling (2026-10-11):** the factory base is fixed here, not in the clients. ChamPBH
(CPBH) keeps registering factory **instances**, and pins a release in which that works. The release
is **`v0.2.3`**.

The brief that carries the ruling is
`/Users/ds283/Documents/Code/ChamPBH/prompts/dk-and-rpk-migration/datastorekit-v0.2.3-brief.md`,
written 2026-10-11 at DatastoreKit `460b012` and CPBH `52142d7`. It is evidence, not a
specification (`CLAUDE.md` rule 7): §0.1 re-measures it here, and where it and this repository's
records disagree, the records are right (§0.2).

**The defect.** `SQLAFactoryBase` (`datastorekit/SQL/factory_base.py:5-29`) is an `ABC` whose five
hooks `register`, `build`, `store`, `validate` and `validate_on_startup` are all
`@staticmethod @abstractmethod`. Python enforces an abstract method only when a class is
instantiated. The layer never instantiates a factory: it calls each hook on whatever the registry
maps a name to, class or instance alike. So:
- for a client that registers **classes** (SGK, and the neutral test client), the ABC checks
  nothing, since its classes are never instantiated;
- for a client that registers **instances** (CPBH, SI), the ABC refuses every class that does not
  define `store`, `validate` and `validate_on_startup`, though the layer calls them only on an
  `object_store`, an `object_validate`, or a class whose `register()` says
  `validate_on_startup: True` (contract §3). CPBH has 20 such classes over 24 registry entries, SI
  16 over 18 (extraction U32).

Contract §3 already treats the three as optional ("Not defined: the base's
`NotImplementedError`", `store`'s row), and the base already defaults `revalidate`,
`owned_serials` and `inventory_spec` "so a factory that has no use for one need not define it"
(`factory_base.py:31-32`). The ABC is SGK's base, carried over at extraction (`PROVENANCE.md`); no
decision here chose it as a requirement on clients. Extraction U32 (2026-10-09) met its consequence
at 07a and kept it, rejecting the package fix because it "changes the contract that SGK's factories
and the neutral client satisfy". The change only relaxes the base: every factory that satisfies the
`v0.2.2` base satisfies the new one. U1 below revisits U32 in part.

### 0.1 Measurements taken by the planner (2026-10-11)

All at `460b012`, whose `datastorekit/` is `6d8ee9a`'s (`v0.2.2`): `git diff --stat 6d8ee9a HEAD --
datastorekit pyproject.toml docs/client-contract.md docs/adoption` is empty. Nothing was committed.

**The brief's §3, point 1: no test depends on the three hooks being abstract.** `git grep` over
`datastorekit/` for `SQLAFactoryBase`, `abstractmethod`, `__isabstractmethod__`,
`__abstractmethods__` and `isabstract` finds, outside the base and the neutral client's 23
subclasses (`tests/client/factories.py`):
- `SQL/Datastore.py:14`, `:28`: the base imported for a type alias only;
- `store_inventory.py:31`: a docstring;
- `tests/test_declared_facts.py:542`, `:563`: `SQLAFactoryBase.revalidate` and `.owned_serials`
  called on the class;
- `tests/test_neutral_client.py:124-130`: `_defines(factory, hook)`, which compares a factory's
  hook with `getattr(SQLAFactoryBase, hook)` by identity. A `@staticmethod` reached from a class or
  from an instance is the same function object, abstract or not, so `_defines` is unaffected
  (measured in the prototype below).

No test instantiates a factory or reads `__abstractmethods__`. **One thing the brief did not
name:** `tests/test_neutral_client.py:64` defines `ABSTRACT_HOOKS = ("register", "build", "store",
"validate", "validate_on_startup")`, beside `DEFAULTED_HOOKS` (`:65`). It is used once, at `:259`,
summed with the other two lists, so its test passes either way, but its name describes the base
and becomes wrong. 01 corrects it (U2).

**Point 2: nothing in the layer relies on the hooks being static.** Every hook call is made on the
registry entry: `factory.register()` (`SQL/schema.py:99`); `factory.validate_on_startup`
(`SQL/Datastore.py:266`, `:492`; `SQL/ShardedPool.py:2289`, `:2324-2325`); `factory.build`
(`SQL/Datastore.py:565`; the version table's at `SQL/ShardedPool.py:521`); `factory.read_batch`
(`SQL/Datastore.py:643`); `factory.store` (`:711`); `factory.validate` (`:876`); `factory.read_table`
(`:931`, after `hasattr(factory, "read_table")` at `:921`); `factory.revalidate`
(`SQL/ShardedPool.py:2110`); `factory.owned_serials` (`:3490`, `:3499`); and `inventory_spec` by
`getattr(factory, …)` (`store_inventory.py:922`). The layer has no `type(factory)`, no `inspect`,
`vars`, `__dict__` or `__mro__` of a factory, and names no factory by `__name__`: every class name
in a message comes from the object or the registry key. Factories reach the actors as constructor
arguments, so under Ray they are serialised by `cloudpickle`. An instance of a module-level class
pickles by reference to its class, with its attributes by value: in the low-end venv,
`ray.cloudpickle` round-trips a registry entry that is an instance holding a column name, and the
copy builds its table (Ray not started). **The suite cannot see this**: the stand-in pool runs the
actors in-process and pickles nothing (U3).

**Point 3: the defaults' form.** A `@staticmethod` that raises `NotImplementedError` is called with
the same arguments from a class or an instance, so it serves both. Made an instance method instead,
a class's call `Cls.store(obj, conn=…, …)` would bind `obj` to `self` and raise `TypeError`, which
changes what SGK and the neutral client meet (U1).

**A prototype.** In a scratch export of `460b012`, `@abstractmethod` was removed from the three
hooks and nothing else in the layer changed. With three scratch tests added:
1. the neutral client's `gauge_setting_factory`, which defines only `register`, `build` and
   `inventory_spec`, registered as an **instance**: a get writes a row, and a reopen finds the same
   serial;
2. a parameterised factory, one class whose hooks take `self` and whose column name is a
   constructor argument, registered as two instances over two new replicated tables: each builds
   its own rows, and a reopen finds them;
3. `store`, `validate` and `validate_on_startup` raise `NotImplementedError` from the class and
   from an instance; `SQLAFactoryBase.__abstractmethods__` is `{"register", "build"}`; a subclass
   without `build` still raises `TypeError` on instantiation.

Results:
- **low end** (Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39, `venv/`): `Ran 497 tests … OK`,
  that is, the 494 and the three;
- **high end** (3.13.16 / 2.55.1 / 2.0.46, an offline scratch venv with the export installed
  editable): `Ran 497 tests … OK`, 0 `ResourceWarning` lines. *(Run first without the editable
  install, 19 tests failed: the tool tests that run `python -m datastorekit.tools…` in a subprocess
  from another directory, which need the package installed. A venv's setup, not the change.)*
- **the same three tests on the unchanged tree**: all three error with `TypeError: Can't
  instantiate abstract class … without an implementation for abstract methods 'store', 'validate',
  'validate_on_startup'`;
- **through the pool**, with `gauge_setting` registered once as the class and once as an instance:
  `object_store` of a `gauge_setting` raises a bare `NotImplementedError` in both, and
  `object_validate` on a fresh pool the same, in both. On the unchanged tree the class gives the
  same, and the instance cannot be made. So an instance meets exactly what a class meets.
  *(Observed, not new: after the failed replicated store, the next write on that pool is refused
  with `ReplicationInFlight`, the store's in-flight record being left set. That is `v0.2.2`'s
  behaviour for a class too, and the check at open is what clears it.)*

**The clients**, read through `git` only: SGK `6861a9f` (clean; `requirements.txt:17` pins
`v0.2.2`), CPBH `52142d7` (25 untracked entries), SI `7bb3efd` (clean). CPBH's own base at
`52142d7` (`Datastore/SQL/ObjectFactories/base.py:16-30`) is a plain class whose five hooks are
instance methods raising `NotImplementedError`, as its checklist's item 5 says.

### 0.2 Where the brief and this repository's records differ

None of substance. The brief's citations hold at `460b012`. It is silent on four things this plan
adds, each to be reported back to the ChamPBH session when `v0.2.3` is tagged:
1. `ABSTRACT_HOOKS` in `tests/test_neutral_client.py:64` (§0.1, point 1);
2. the suite cannot show that an instance survives Ray's serialisation (§0.1, point 2; U3);
3. SI instantiates three factories **at import** as well as in its registry (its checklist, item 3,
   `docs/adoption/stochasticinstantons.md:119-126`): those sites too stop raising under `v0.2.3`,
   and 02's SI addendum says so;
4. extraction verification §8 records 07a's observation §7.3 as "still an observation"
   (`docs/extraction-verification.md:1060`); 01 records it addressed, additively.

## 1. Scope

**In scope:**
- `datastorekit/SQL/factory_base.py`: `store`, `validate` and `validate_on_startup` defaulted
  (U1). The base stays an `ABC` with `register` and `build` as its only abstract hooks;
- a test module that a revert fails, and `test_neutral_client.py`'s hook lists brought into line
  with the base (U2);
- a step of `docs/extraction/ray_smoke_run.py` that registers instances, run under real Ray at both
  ends (U3);
- `docs/client-contract.md` §9.5, and a dated subsection of `docs/extraction-verification.md`
  (`CLAUDE.md` rule 6);
- a dated note on extraction U32, in that campaign's README §6.2 and its board's decision row;
- the release `v0.2.3` (prompt 02, U5), with adoption addenda.

**Out of scope:**
- **any client repository** (`CLAUDE.md`). CPBH adopts `v0.2.3` in its own campaign (its prompt
  07); SI when it is next active;
- **any other change to the base or the layer.** No hook's signature, no message, refusal or
  exception changes but the one removed: the `TypeError` on instantiating a factory class that
  lacks `store`, `validate` or `validate_on_startup`. Nothing the layer writes changes;
- the four issues inherited from SGK (`docs/OPEN_ISSUES.md` §1.2), and anything else a prompt
  finds: it is recorded, not fixed (§5 rule 4), unless the user rules otherwise.

## 2. Prompts

| # | Prompt | Covers | Status |
|---|---|---|---|
| 01 | [`01-the-base-defaults-three-hooks.md`](01-the-base-defaults-three-hooks.md) | `store`, `validate` and `validate_on_startup` lose `@abstractmethod` and move under the base's comment on defaulted hooks (U1); a test module of instances, parameterised instances, the two abstract hooks, the defaults, and a `cloudpickle` round trip, and the neutral client's hook lists (U2); a smoke step that registers instances, run under real Ray at both ends (U3); contract §9.5; a dated subsection of the verification document, closing 07a §7.3; a dated note on extraction U32. | **written** 2026-10-11; U1–U3 taken |
| 02 | Release `v0.2.3` (planned) | `pyproject.toml` at `0.2.3`, `README.md`, `PROVENANCE.md`; dated `v0.2.3` addenda to `docs/adoption/` (the README and the three checklists); the extraction board's G2–G4; both ends locally and in CI; **tag `v0.2.3`** on its commit after green CI, not by the prompt. Shaped by U5. | not written: written after 01 is reviewed, against its tree |

**Order.** 01 → 02. 02 releases what 01 leaves. Each is landed and reviewed on its own (U4).

## 3. Datastores

No prompt opens a store of any client. Tests and the smoke script build their stores in `tempfile`
directories.

## 4. The interfaces between prompts

- **After 01:** the base's two abstract and six defaulted hooks; the new test module and the
  neutral factory class and object class it adds (their names and home are 01's to choose, §2.3 of
  01); the smoke script's step I; contract §9.5; the verification document's new subsection; the
  note on extraction U32.
- **After 02:** `pyproject.toml` at `0.2.3`; the adoption addenda. After its CI passes, the tag
  `v0.2.3` on 02's commit, and the tag object and commit given to the user for CPBH's prompt 07.

## 5. The rules this campaign runs under

The project-wide ones in `CLAUDE.md`, plus:

1. **One commit per prompt**, in this repository only.
2. **Every prompt writes a log** to `logs/NN-<name>.md`, using §5.1.
3. **Every prompt updates `IMPLEMENTATION_STATE.md`** in its own commit, plus
   `docs/OPEN_ISSUES.md`.
4. **Do not fix things the prompt did not ask for.** A defect found is recorded with a §3 issue.
   Nothing rides in `v0.2.3` but U1, unless the user rules otherwise.
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
9. **No tag except where a prompt says so** (02: `v0.2.3`), and none is moved or deleted. No prompt
   pushes.
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

The extraction campaign's decisions stand (its README §6), except U32, which U1 revisits in part:
in particular U4 (clients pin a tagged release), U23 and U28 (a tag is made on its prompt's commit
only after CI passes there, each push and tag with the user's approval), U36 (a fix release is
patch-level) and U41 (the smoke run). So do `actor-names` U1–U4.

### 6.2 Decisions this campaign needs

- **U1: what the base becomes, and how U32 is recorded.** *(The change is the user's ruling,
  2026-10-11. Its form taken 2026-10-11, as recommended.)* **Recommended:**
  - in `factory_base.py`, `store`, `validate` and `validate_on_startup` lose `@abstractmethod`,
    keep `@staticmethod` and their present signatures and bodies (`raise NotImplementedError`,
    bare), and move below the comment on defaulted hooks (`:31-32`), whose wording is adjusted to
    cover six hooks. The base stays an `ABC` with `register` and `build` as its only abstract
    hooks (`@staticmethod @abstractmethod`). A factory class is refused at instantiation only if it
    lacks one of those two: every CPBH and SI class defines both (each checklist's item 5), so
    each instantiates as it stands, and a client that instantiates is still refused a factory
    that lacks either;
  - the base's docstrings may say when the layer calls each of the three, in neutral terms, as
    `revalidate`'s does (the guard, `test_layer_is_generic`, scans this file);
  - extraction U32 is not rewritten. 01 adds a dated italic line under it in
    `../extraction/README.md` §6.2, and a dated note in that board's U32 row, each saying that
    `factory-defaults` U1 revisited it in part on the user's ruling, from `v0.2.3`, and pointing
    here.

  **Rejected:**
  - **dropping the `ABC`**, or making `register` and `build` defaulted too: an instance lacking
    `build` would then be accepted and fail at its first get, where today it fails when built. The
    ABC's one useful check, for a client that instantiates, is kept;
  - **defaults as instance methods** (`def store(self, obj, …)`, CPBH's form): a class's call
    binds `obj` to `self`, so SGK and the neutral client would meet `TypeError` where they meet
    `NotImplementedError` today (§0.1, point 3);
  - **a message naming the hook**: it changes a message, which the ruling's scope excludes, and the
    actor's traceback already names the class and the call;
  - **the client-side change of U32** (CPBH's 20 classes and SI's 16 given the three hooks, or
    every hook made static): overruled by the user.
- **U2: the tests.** *(Taken 2026-10-11, as recommended.)* **Recommended:** a new module,
  `datastorekit/tests/test_factory_instances.py`, always run, on the stand-in pool and the neutral
  client, with no Ray:
  1. the neutral client's `gauge_setting_factory`, which defines `register` and `build` but not the
     three, registered as an instance in place of its class: it instantiates; a get writes a row;
     a reopen gets the same serial;
  2. a parameterised factory: one neutral class whose hooks take `self` and whose constructor
     argument names its column, registered as two instances over two replicated tables. Each
     builds and reads back its own rows, the two tables hold different rows, and a reopen finds
     them;
  3. `SQLAFactoryBase.__abstractmethods__` is exactly `{"register", "build"}`, and a subclass
     lacking either raises `TypeError` on instantiation;
  4. `store`, `validate` and `validate_on_startup` of a factory that defines none raise
     `NotImplementedError` from the class and from an instance; and through the pool, an
     `object_store` and an `object_validate` (each on a fresh pool) raise the same with the class
     registered as with an instance;
  5. a registry holding instances round-trips `ray.cloudpickle`, and the copies serve a pool;
  6. `_defines` of `tests/test_neutral_client.py` reads an instance as it reads its class.

  And in `tests/test_neutral_client.py`, `ABSTRACT_HOOKS` becomes `("register", "build")` and the
  three move to `DEFAULTED_HOOKS`, with an assertion that `ABSTRACT_HOOKS` equals the base's
  `__abstractmethods__`. The neutral client's registry is unchanged: it registers classes, as SGK
  does, and its tests pass as they stand. The parameterised class and its object class live
  outside the registry, so no schema, drop group or inventory count moves.
  **Rejected:** adding the parameterised factory to the neutral client's registry, which would move
  every count the registry's tests pin, for a fact one module shows; and leaving `ABSTRACT_HOOKS`
  as it is, a list whose name says what the base no longer is.
- **U3: Ray.** *(Taken 2026-10-11, as recommended.)* **Recommended:** the smoke script gains a step **I**: on a fresh store, a
  read-write pool whose registry holds the parameterised factory as two instances, and
  `gauge_setting` as an instance, gets a row of each, closes, reopens and finds the same serials.
  01 runs the script under real Ray at both ends, every step `PASS`, and once with U1 reverted,
  step I `FAIL` naming `TypeError`. The stand-in pool pickles nothing, so this step is the only
  place an instance is sent to a real actor. **Rejected:** the suite's `cloudpickle` round trip
  alone, which does not show a worker process unpickling the registry; an uncommitted scratch run,
  which no one can repeat; no Ray run, since the risk U1 adds, if any, is in what Ray does with an
  instance.
- **U4: the shape.** *(Taken 2026-10-11, as recommended.)* **Recommended:** two prompts, as `actor-names` was: 01 the change
  and its evidence; 02 the release, written after 01 is reviewed. The commit boundary is the
  rollback boundary, and 02's four addenda are reviewed against a settled tree. **Rejected:** one
  prompt for change and release, which puts the code and four adoption documents in one review and
  one revert.
- **U5: the release, and who adopts it.** *(The version, `v0.2.3`, is the user's ruling. The rest
  taken 2026-10-11, as recommended. Needed by 02, not 01.)* **Recommended:**
  - patch-level, as U36: no name is added or removed, nothing the layer writes changes, and the
    one behaviour that changes is a refusal removed. Every factory valid under `v0.2.2` is valid
    under `v0.2.3`;
  - **CPBH and SI adopt `v0.2.3`**, and with it register their instances as they stand; item 5 of
    each checklist then asks nothing of their factories but the base's import path. G3 and G4 read
    `v0.2.3`;
  - **SGK may stay on `v0.2.2` or move**, in a commit of its own, as it chooses: it registers
    classes, and `v0.2.3` changes nothing it meets. G2 reads "`v0.2.2` or later". This amends
    extraction U37 and `actor-names` U3 ("every client adopts the release named") for SGK only.

  **Rejected:** requiring SGK to move, a pin change in a client mid-adoption that fixes nothing it
  meets; `v0.3.0`, treating a relaxed base as a change of contract, when no factory valid today
  becomes invalid.

## 7. Gates outside this repository

The extraction campaign's G2–G4 (each client's adoption) are recorded on the extraction board when
they hold. Under U5, G3 and G4 read `v0.2.3` once it is tagged, and G2 `v0.2.2` or later; 02's
addenda say so. This campaign does not wait for them. CPBH's prompts 01–06 do not wait for
`v0.2.3`; its 07–10 do.
