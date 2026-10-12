# Adoption checklist: ChamPBH (CPBH)

- **Client:** ChamPBH, `/Users/ds283/Documents/Code/ChamPBH`, at **`52142d7`**
  (`52142d75aebe00855804e2daff4f63aee50ffc3e`, branch `main`, "Store each shard key under its own
  serial").
- **Package:** `datastorekit` at **`v0.2.0`** (`240028e`).
- **How it was measured:** read-only, by DatastoreKit's extraction prompt 07a on 2026-10-09,
  through `git show`, `git grep`, `git ls-tree` and `git log` only, and by
  `docs/extraction/measure_client_imports.py` (the appendix). Two untracked run scripts were read as
  text, by name (item 1). Nothing of CPBH was imported, run or opened, and **no store or database
  file was opened**. **CPBH's adoption campaign measures again before acting, and its numbers
  govern.**
- **This is data, not instructions.** It describes CPBH at `52142d7`. CPBH's campaign decides what
  to do, under CPBH's `CLAUDE.md`. A recommendation is marked **Advice:**; a choice that is CPBH's
  is named as CPBH's.

*Added by extraction prompt 10 on 2026-10-10: the section
[Addendum: v0.2.1](#addendum-v021-extraction-prompt-10-2026-10-10), after item 10, gives the pin
**`v0.2.1`** and what changed for CPBH since `v0.2.0`, and supersedes the statements it names.
07a's text is unchanged and true of `v0.2.0`.*

*Added by `actor-names` prompt 02 on 2026-10-11: the section
[Addendum: v0.2.2](#addendum-v022-actor-names-prompt-02-2026-10-11), after the `v0.2.1` addendum,
gives the pin **`v0.2.2`** and what changed for CPBH since `v0.2.1`, and supersedes the statements
it names. The text before it, the `v0.2.1` addendum included, is unchanged and true of the
release it names.*

*Added by `factory-defaults` prompt 02 on 2026-10-11: the section
[Addendum: v0.2.3](#addendum-v023-factory-defaults-prompt-02-2026-10-11), after the `v0.2.2`
addendum, gives the pin **`v0.2.3`** and what changed for CPBH since `v0.2.2`, and supersedes the
statements it names. The text before it, the `v0.2.1` and `v0.2.2` addenda included, is unchanged
and true of the release each names.*

*Added by `object-timestamp` prompt 02 on 2026-10-12: the section
[Addendum: v0.3.0](#addendum-v030-object-timestamp-prompt-02-2026-10-12), after the `v0.2.3`
addendum, gives CPBH's pin, `v0.2.3` or `v0.3.0` as CPBH chooses, and what changed for CPBH since
`v0.2.3`, and supersedes the statements it names. The text before it, the `v0.2.1`, `v0.2.2` and
`v0.2.3` addenda included, is unchanged and true of the release each names.*

Unless another commit is named, a `path:line` is CPBH's at `52142d7`, and one under
`datastorekit/` is the package's at `v0.2.0`.

**In one paragraph.** CPBH's layer is 9 files, 2,686 lines, close to SGK's of late 2025. It holds
CPBH's registry, drop groups, batch sizes and inventory configuration, which must leave it first.
The package's pool takes `factories=` and `drop_tables=` and refuses CPBH's `drop_actions` and
`inventory_config`; its factory base is an ABC, and CPBH registers instances of 20 classes that
define only two of its five abstract hooks (U32); its vectorized get takes a mapping, not CPBH's
bare `beta_value`; and every CPBH store is refused at open, so CPBH's stores are rebuilt, not
migrated (decision D4).

---

## 1. The client and its versions

- `52142d7` on `main`. `git status --short` lists **23 untracked entries**, the same at the start
  and at the end of 07a's measurement: the pilot store's 17 `.db` files (`pilot-2026.6.0.db` and
  `pilot-2026.6.0-shard0000.db` … `-shard0015.db`), two logs (`pilot-main.log`, `pilot-plot.log`),
  two run scripts (`full_run_2026.6.0.sh`, `full_run_2026.6.0-refresh.sh`), `pilot-out/` and
  `prompts/jordan-normalization/`. **The `.db` files were not opened**; they are named only. The
  two run scripts were read as text (item 8).
- **Python 3.13.16**: no tracked file states it. It is from `venv/pyvenv.cfg` (`version =
  3.13.16`), read as text; `venv/bin/python3.13` links to MacPorts' 3.13 framework.
  **`ray==2.53.0`** (`requirements.txt:78`); **`SQLAlchemy==2.0.46`** (`requirements.txt:89`).
- Its documents are under `.documents/` (there is no `docs/`, `CLAUDE.md:58`); its issue index is
  `.documents/OPEN_ISSUES.md`; its test commands are `CLAUDE.md:64-66`, the Datastore one at
  `CLAUDE.md:66`.

## 2. What it deletes

**The 9 layer files, 2,686 lines:**

| File | Lines |
|---|---|
| `Datastore/__init__.py` | 1 |
| `Datastore/object.py` | 36 |
| `Datastore/SQL/__init__.py` | 1 |
| `Datastore/SQL/ClientPool.py` | 256 |
| `Datastore/SQL/Datastore.py` | 844 |
| `Datastore/SQL/ProfileAgent.py` | 355 |
| `Datastore/SQL/SerialPoolBroker.py` | 164 |
| `Datastore/SQL/ShardedPool.py` | 999 |
| `Datastore/SQL/ObjectFactories/base.py` | 30 |

Item 4 lists what in them is CPBH's and must leave first.

**What the package has that CPBH's layer lacks** (`PROVENANCE.md`; `docs/client-contract.md`):
- `datastorekit.SQL.schema`: one schema builder (`build_schema`), the store-schema check
  (`StoreSchemaMismatch`), `drop_order` and `dependent_tables`;
- `datastorekit.contract`: the layer's table names, and `VERSION_SERIAL_KEY` with
  `require_version_serial`;
- `datastorekit.replication`: the recorded replicated write, `ReplicationMismatch`,
  `ReplicatedDivergence`, `ReadOnlyMiss`, `ReadOnlyWrite`;
- `datastorekit.shard_paths`: shard records as bare names beside the primary;
- `datastorekit.store_reader` (`open_read_only`) and `datastorekit.store_inventory`
  (`read_inventory`, `InventorySpec`): a read-only reader and a structured inventory;
- the tools, `python -m datastorekit.tools.sharded_store` (copy, move) and `python -m
  datastorekit.tools.shard_key_audit`;
- a read-only pool (`ShardedPool(read_only=True)`), the check at open (repair or refusal of an
  interrupted replicated write), the prune of replicated classes under a record, and
  `ShardedPool.copy_store`, `move_store` and `delete_store`.

## 3. Which imports it rewrites

The script counts **41** import statements of the 9 modules, in **38** files, outside the layer's
own files; none is nested (appendix). By what they import:

| Imported | Statements | Where |
|---|---|---|
| `SQLAFactoryBase` (`Datastore.SQL.ObjectFactories.base`) | 17 | one in each of the 17 factory modules |
| `DatastoreObject` (`Datastore`, the package root) | 13 | `ComputeTargets/` 3, `CosmologyConcepts/` 5, `CosmologyModels/base.py:18`, `MetadataConcepts/` 3, `Quadrature/integration_metadata.py:18` |
| `ShardedPool` | 6 | `RayTools/RayWorkPool.py:23` (a type hint), `config/model_list.py:19`, `main.py:48`, `plot_ScalarModel.py:42`, `plot_by_beta.py:36`, `Datastore/tests/test_shard_key_assignment.py:40` |
| `ProfileAgent` | 3 | `main.py:47`, `plot_ScalarModel.py:41`, `plot_by_beta.py:35` |
| `Datastore` (the actor, `Datastore.SQL.Datastore`) | 2 | `Datastore/tests/test_version_keyed_lookups.py:45`; `prompts/run-integrity/planning-probes/datastore_version_probe.py:18`, a historical probe |
| **total** | **41** | |

`Datastore/tests/` holds 2 of them (`Datastore/tests/test_version_keyed_lookups.py:45`,
`Datastore/tests/test_shard_key_assignment.py:40`).
`ComputeTargets/tests/test_foreign_bbn_provenance.py:49` imports no layer module, but imports helpers
from `Datastore.tests.test_version_keyed_lookups` (item 7). No string literal or `import_module`
call names a layer module.

**The two names that move into the package.** `config/version.py:55` (`VERSION_SERIAL_KEY =
"_version_serial"`) and `config/version.py:58-71` (`require_version_serial`) are, with the same key,
`datastorekit.contract.VERSION_SERIAL_KEY` and `datastorekit.contract.require_version_serial`
(`datastorekit/contract.py:39`, `datastorekit/contract.py:42-56`). They are imported by the three
keyed factories, `Datastore/SQL/ObjectFactories/AdiabaticHistory.py:31`,
`Datastore/SQL/ObjectFactories/BBNData.py:20` and `Datastore/SQL/ObjectFactories/ScalarModel.py:44`,
by `Datastore/tests/test_version_keyed_lookups.py:350`, and by the layer itself
(`Datastore/SQL/Datastore.py:85`, deleted).

**A hazard of that move: two different `VERSION_LABEL`s.** `datastorekit.contract.VERSION_LABEL`
is `"label"`, the *name of the version table's label column* (`datastorekit/contract.py:28`).
CPBH's `config.version.VERSION_LABEL` is `"2026.6.0"`, the *label* every driver opens the store
under (`config/version.py:50`), imported by `main.py:66`, `plot_ScalarModel.py:57` and
`plot_by_beta.py:50`. A rewrite that moves `config.version`'s imports wholesale to
`datastorekit.contract` would bind the wrong one; only `VERSION_SERIAL_KEY` and
`require_version_serial` move. `Datastore/tests/test_version_keyed_lookups.py:428` (test f)
checks that the three scripts import `VERSION_LABEL` from `config.version`.

## 4. What leaves the layer, and where it may go

Each of these is CPBH's, lives in a file item 2 deletes, and must be moved out first. Where it goes
is CPBH's choice; `datastorekit/tests/client/registry.py` (in this repository, not installed) is
the worked example of a client's registry module.

- **The registry**, `_factories` (`Datastore/SQL/Datastore.py:94-122`): 27 entries, each an
  **instance** (`sqla_..._factory()`, five of them `sqla_dimensionful_quantity_factory(<class>)`).
  It reaches the package as `ShardedPool(factories=...)`, and as the registry given to
  `open_read_only` and `read_inventory`. Its imports of the 17 factory modules and of
  `CosmologyConcepts`' six quantity classes (`Datastore/SQL/Datastore.py:27-83`) go with it.
- **The drop groups**, `_drop_actions` and `_drop_order` (`Datastore/SQL/Datastore.py:128-142`):
  `scalar-model`, `adiabatic-history`, `bbn-data`, each a list of three tables, and an order. The
  same three names are the command line's `--drop` choices (`config/argument_parser.py:33`). The
  package takes tables, and orders a drop itself from foreign keys (item 6).
- **The inventory configuration**: `InventoryConfigType` (`Datastore/SQL/Datastore.py:149`), the
  actor's `inventory()` (`Datastore/SQL/Datastore.py:817-844`), and the pool's `_merge_queue()` and
  `inventory()` (`Datastore/SQL/ShardedPool.py:881-999`), driven by `config/sharding.py:58-103`
  (`inventory_config`). The package has no `inventory()` and takes no `inventory_config`; its
  inventory is `datastorekit.store_inventory.read_inventory(primary, factories)`, over each
  factory's `inventory_spec()` (item 6).
- **The serial batch sizes**, `_default_serial_batch_size` (`Datastore/SQL/ClientPool.py:24-49`):
  24 tables, `LambdaCDM` among them. They become `ShardedPool(serial_batch_sizes=...)`. A table
  the mapping does not name leases 500 at a time in the package
  (`datastorekit/SQL/ClientPool.py:130`).
- **The bare-shard-key branch** of `object_get_vectorized` (`Datastore/SQL/ShardedPool.py:592-593`),
  which accepts a `beta_value` itself as the shard key. The package has no such branch (item 6).
- **The client imports inside the layer**: `CosmologyConcepts` (`Datastore/SQL/Datastore.py:27`),
  the 17 factory modules (`Datastore/SQL/Datastore.py:36-83`), `config.version`
  (`Datastore/SQL/Datastore.py:85`), `utilities` (`Datastore/SQL/Datastore.py:86`,
  `Datastore/SQL/ProfileAgent.py:26`), `config.defaults` (`Datastore/SQL/ProfileAgent.py:25`,
  `Datastore/SQL/ShardedPool.py:29`), `MetadataConcepts.version` (`Datastore/SQL/ShardedPool.py:28`)
  and `config.sharding.ShardKeyType` (`Datastore/SQL/ShardedPool.py:30`). The package needs none:
  the registry carries the factories, and the constructor the shard-key type.

**The factory modules' location is CPBH's choice.** They are under `Datastore/SQL/ObjectFactories/`
(17 modules besides `base.py` and `__init__.py`). With the layer's two `__init__.py` files deleted,
`Datastore/` and `Datastore/SQL/` become namespace packages unless CPBH gives them empty ones, or
moves the factories. One import of a factory module lies outside `Datastore/`: `main.py:46`
(`from Datastore.SQL.ObjectFactories import tolerance`, used as a type hint at `main.py:117-118`).

## 5. What its factories must change

**The per-factory table.** Kind is from `config/sharding.py` (`replicated_tables`,
`config/sharding.py:18-37`; `sharded_tables`, `config/sharding.py:39-47`, all on the field
`shard_key`). Every hook takes `self`; none is a `staticmethod`.

| Registry key(s) (`Datastore/SQL/Datastore.py:94-122`) | Class | Kind | `register()` keys (besides `columns`) | Hooks defined |
|---|---|---|---|---|
| `version` | `sqla_version_factory` (`Datastore/SQL/ObjectFactories/version.py:23`) | replicated | `version` False, `timestamp` False | `register`, `build` |
| `store_tag` | `sqla_store_tag_factory` (`Datastore/SQL/ObjectFactories/store_tag.py:23`) | replicated | `version` False, `timestamp` True | `register`, `build` |
| `redshift` | `sqla_redshift_factory` (`Datastore/SQL/ObjectFactories/redshift.py:31`) | replicated | `version` False, `timestamp` True | `register`, `build`; `read_table`, `inventory` |
| `tolerance` | `sqla_tolerance_factory` (`Datastore/SQL/ObjectFactories/tolerance.py:25`) | replicated | `version` False, `timestamp` True | `register`, `build` |
| `beta_value` | `sqla_dimensionless_quantity_factory(beta_value)` (`Datastore/SQL/ObjectFactories/DimensionlessQuantity.py:28`) | replicated | `version` False, `timestamp` True | `register`, `build`; `read_table`, `inventory` |
| `M_value`, `Lambda_value`, `temperature`, `phi_value`, `pi_value` | `sqla_dimensionful_quantity_factory(<class>)` (`Datastore/SQL/ObjectFactories/DimensionfulQuantity.py:28`) | replicated | `version` False, `timestamp` True | `register`, `build`; `read_table`, `inventory` |
| `InversePowerPotential`, `StarobinskyPotential`, `ExponentialPotential`, `ReclinerPotential`, `ReflectingPotential` | one class each (`Datastore/SQL/ObjectFactories/InversePowerPotential.py:25`, `Datastore/SQL/ObjectFactories/Starobinsky.py:25`, `Datastore/SQL/ObjectFactories/ExponentialPotential.py:25`, `Datastore/SQL/ObjectFactories/ReclinerPotential.py:25`, `Datastore/SQL/ObjectFactories/ReflectingPotential.py:25`) | replicated | `version` True, `timestamp` True | `register`, `build` |
| `ExponentialCoupling` | `sqla_ExponentialCoupling_factory` (`Datastore/SQL/ObjectFactories/ExponentialCoupling.py:25`) | sharded | `version` True, `timestamp` True | `register`, `build` |
| `QCD_Cosmology` | `sqla_QCDCosmology_factory` (`Datastore/SQL/ObjectFactories/QCD_Cosmology.py:23`) | replicated | `version` False, `timestamp` True | `register`, `build` |
| `IntegrationSolver` | `sqla_IntegrationSolver_factory` (`Datastore/SQL/ObjectFactories/integration_metadata.py:23`) | replicated | `version` False, `stepping` `"minimum"`, `timestamp` True | `register`, `build` |
| `ScalarModel` | `sqla_ScalarModelFactory` (`Datastore/SQL/ObjectFactories/ScalarModel.py:102`) | sharded | `version` True, **`key_on_version` True**, `stepping` False, `timestamp` True, `validate_on_startup` True | all five; `inventory` |
| `ScalarModel_tags` | `sqla_ScalarModelTagAssociation_factory` (`Datastore/SQL/ObjectFactories/ScalarModel.py:47`) | neither | `serial` False, `version` False, `stepping` False, `timestamp` True | `register`, `build` |
| `ScalarModelValue` | `sqla_ScalarModelValue_factory` (`Datastore/SQL/ObjectFactories/ScalarModel.py:877`) | sharded | `version` False, `timestamp` False, `stepping` False | `register`, `build` |
| `AdiabaticHistory` | `sqla_AdiabaticHistoryFactory` (`Datastore/SQL/ObjectFactories/AdiabaticHistory.py:89`) | sharded | as `ScalarModel` (**keyed**) | all five; `inventory` |
| `AdiabaticHistory_tags` | `Datastore/SQL/ObjectFactories/AdiabaticHistory.py:34` | neither | as `ScalarModel_tags` | `register`, `build` |
| `AdiabaticHistoryValue` | `Datastore/SQL/ObjectFactories/AdiabaticHistory.py:440` | sharded | as `ScalarModelValue` | `register`, `build` |
| `BBNData` | `sqla_BBNDataFactory` (`Datastore/SQL/ObjectFactories/BBNData.py:78`) | sharded | as `ScalarModel` (**keyed**) | all five; `inventory` |
| `BBNData_tags` | `Datastore/SQL/ObjectFactories/BBNData.py:23` | neither | as `ScalarModel_tags` | `register`, `build` |
| `BBNDataValue` | `Datastore/SQL/ObjectFactories/BBNData.py:514` | sharded | as `ScalarModelValue` | `register`, `build` |

`replicated_tables` also
names `LambdaCDM` (`config/sharding.py:34`), which no factory registers (item 8).

**U32: 20 classes, 24 registry entries.** Of the 23 classes registered, only `ScalarModel`,
`AdiabaticHistory` and `BBNData` define all five abstract hooks. The other **20 classes** define
`register` and `build` only (three of them also `read_table` and `inventory`); they fill **24
registry entries** (`sqla_dimensionful_quantity_factory` fills 5, every other class 1).
- CPBH's own `SQLAFactoryBase` is not an ABC: its five hooks are instance methods that raise
  `NotImplementedError` (`Datastore/SQL/ObjectFactories/base.py:16-30`). So today the 20 classes
  instantiate, and a call of an undefined hook raises `NotImplementedError`.
- The package's `SQLAFactoryBase` is an ABC with the five abstract
  (`datastorekit/SQL/factory_base.py:5-29`). Subclassing it, `sqla_version_factory()` and the
  other 19 raise `TypeError` at instantiation, that is, wherever the registry is built.
- **The two routes, and what each needs** (the choice is CPBH's):
  - **Define `store`, `validate` and `validate_on_startup` on each of the 20.** The layer calls
    `store` only on an `object_store`, `validate` only on an `object_validate`, and
    `validate_on_startup` only for a class whose `register()` says `validate_on_startup: True`
    (`docs/client-contract.md` §3), which none of the 20 does.
  - **Register the class itself.** The layer calls the hooks on what the registry holds, with no
    instance of its own (`factory.register()`, `datastorekit/SQL/schema.py:101`). Every CPBH hook
    takes `self`, and the two quantity factories hold their `ObjectType` on the instance
    (`Datastore/SQL/ObjectFactories/DimensionfulQuantity.py:30`,
    `Datastore/SQL/ObjectFactories/DimensionlessQuantity.py:30`), which six registry entries
    differ by. So this route works only once each class's hooks can be called without an
    instance.

**The layer's own tables (contract §5).** `version` and `store_tag` each register a `label` column
(`Datastore/SQL/ObjectFactories/version.py:31`, `Datastore/SQL/ObjectFactories/store_tag.py:31`),
and the three tag tables name the tag by `tag_serial` (`Datastore/SQL/ObjectFactories/ScalarModel.py:67`,
`Datastore/SQL/ObjectFactories/AdiabaticHistory.py:54`, `Datastore/SQL/ObjectFactories/BBNData.py:43`):
contract §5 holds. An oddity, not a defect: `version`'s `build` returns a `store_tag` object
(`Datastore/SQL/ObjectFactories/version.py:51`). The package reads only its `store_id` (contract §6).

**Keyed lookups.** `ScalarModel`, `AdiabaticHistory` and `BBNData` declare `key_on_version` with
`version` True, as contract §8 requires; their `build`s read the serial through
`require_version_serial` (item 3's import moves).

**The six `inventory()` hooks** (`redshift`, the two quantity factories, `ScalarModel`,
`AdiabaticHistory`, `BBNData`; for example `Datastore/SQL/ObjectFactories/redshift.py:118`) are
never called by the package. No CPBH factory declares `inventory_spec` (`git grep inventory_spec
52142d7` finds none), so `read_inventory` reads no CPBH class until one does (item 6).

## 6. Its call sites and pool construction

**The pool is constructed three times**: `main.py:1338-1353`, `plot_ScalarModel.py:1577-1590`,
`plot_by_beta.py:1007-1020`. Against the package's constructor
(`datastorekit/SQL/ShardedPool.py:95-114`):
- **Each call is a `TypeError`.** `main.py:1350` passes `drop_actions=` and `main.py:1352`
  `inventory_config=`; the plot scripts pass `inventory_config=` (`plot_ScalarModel.py:1589`,
  `plot_by_beta.py:1019`) and no `drop_actions`. The package takes neither.
- **None passes `factories=`**, which the package requires (keyword-only).
- `serial_batch_sizes=` replaces `ClientPool.py`'s table (item 4).
- **Drops become table lists.** Under the package, by the foreign keys CPBH declares:
  - `bbn-data` (`BBNData_tags`, `BBNDataValue`, `BBNData`) and `adiabatic-history` (its three) each
    drop alone: nothing outside each group names its tables;
  - **`scalar-model` alone is refused** (`_refuse_drop_that_leaves_references`,
    `datastorekit/SQL/ShardedPool.py:730-749`): `AdiabaticHistory` and `BBNData` name
    `ScalarModel.serial` (`Datastore/SQL/ObjectFactories/AdiabaticHistory.py:107`,
    `Datastore/SQL/ObjectFactories/BBNData.py:94`), so it is accepted only with both other groups.
  - CPBH's `_drop_order` is not needed: the actor orders a drop by foreign key (`schema.drop_order`).

**The 7 `object_get_vectorized` calls pass a bare `beta_value`**: `main.py:196`, `main.py:358`,
`main.py:408`, `main.py:476`, `main.py:614`, `main.py:666`, `main.py:739`. Each passes
`x["shard_key"]`, which `build_solver_batch` and its kin set to the coupling's `beta_value`
(for example `main.py:157`, `main.py:168`). CPBH's layer accepts that by its bare-key branch
(`Datastore/SQL/ShardedPool.py:592-593`). The package wants a mapping from the sharded table's
field to the key, here `{"shard_key": beta}` (`datastorekit/SQL/ShardedPool.py:3299-3307`); with a
bare `beta_value`, its membership test (`datastorekit/SQL/ShardedPool.py:3300`) is applied to the
key object itself, which is not a mapping. It also adds that mapping to every payload dict in place (`datastorekit/SQL/ShardedPool.py:3309-3310`;
DatastoreKit's `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]`). CPBH's layer
adds nothing to the payloads (`Datastore/SQL/ShardedPool.py:581-608`). No CPBH factory reads a
`shard_key` payload field or iterates a payload's keys (`git grep` over the factories finds none).

**`pool.inventory(...)`: 4 sites**, all in `main.py`'s `--inventory` path: `main.py:1188`,
`main.py:1215`, `main.py:1244`, `main.py:1278`. Both run scripts call `--inventory`
(`full_run_2026.6.0.sh:48`, `full_run_2026.6.0-refresh.sh:50`; untracked). The package has no
`pool.inventory`. Its inventory is `datastorekit.store_inventory.read_inventory(primary,
factories)` over each factory's `inventory_spec()`, read-only, on a closed store (contract §4, §7).
CPBH has two routes; the choice is CPBH's:
- **Port to `inventory_spec`**: declare an `InventorySpec` on each class the report covers (its
  leaves, parents, tags, values, validated column), and read the inventory with `read_inventory`
  after the pool closes. Every class a spec depends on must declare one too (contract §4).
- **Keep a reader of its own**: the six `inventory()` hooks stay CPBH's, called by CPBH code
  through its own connection to the store (for example under `open_read_only`), not through the
  pool.

**The unchanged calls**, by count of calls on a pool (an `ast` count in 07a's scratchpad):
`object_get` 59 (`main.py` 26, `plot_ScalarModel.py` 15, `plot_by_beta.py` 17,
`config/model_list.py` 1), `read_table` 6 (3 in each plot script), `object_validate` 3 (`main.py`),
`object_store` 1 (`RayTools/RayWorkPool.py`). Their signatures are the package's
(`datastorekit/SQL/ShardedPool.py:3027`, `:3339`, `:3431`, `:3593`). `read_table_config` names only
replicated classes (`config/sharding.py:49-56`), as the package requires.

## 7. Its tests and fixtures

CPBH's tests are `unittest` modules; `Datastore/tests/` holds six.
- **Delete `Datastore/tests/test_shard_key_assignment.py`** (4 tests; added at `52142d7`). The
  package pins the same fix, SGK `2610abe`, in its own `test_shard_key_assignment`
  (`datastorekit/tests/test_shard_key_assignment.py`, `TestShardKeysAssignedOutOfSerialOrder`), and
  this module builds `ShardedPool` by `object.__new__` with CPBH's tables, which leave CPBH.
- **`Datastore/tests/test_version_keyed_lookups.py`** (11 tests):
  - **d2 and d4 test the layer**, and the package's `datastorekit/tests/test_version_keyed_lookups.py`
    covers both. d4 expects `RuntimeError` (`Datastore/tests/test_version_keyed_lookups.py:395`);
    the package refuses `key_on_version` without `version` with `ValueError` at schema build.
  - **a, b, c1, c2, c3, d, d3, e and f test CPBH's factories, registry and scripts**, and stay.
- **Every actor-based test is rewritten.** The shared harness is `_TempStoreCase`
  (`Datastore/tests/test_version_keyed_lookups.py:187-201`). Its `open` builds the actor with two
  arguments, `DS(version_label=label, db_name=self.db)` (`Datastore/tests/test_version_keyed_lookups.py:199`),
  and relies on CPBH's constructor inserting the version row. The package's actor
  (`datastorekit/SQL/Datastore.py:39-55`):
  - takes `replicated_tables` (positional, required) and `factories=` (keyword-only, required);
  - **inserts no version row** (the pool writes it, `datastorekit/SQL/ShardedPool.py:341-360`);
  - refuses a versioned insert before `set_version`, and a keyed lookup before `set_version` or
    `set_lookup_version` has set the lookup serial (`datastorekit/SQL/Datastore.py:150-190`,
    `datastorekit/SQL/Datastore.py:598-625`).
  
  **The harness's five importers**: `Datastore/tests/test_bbn_failure_lookup.py:38` (6 tests),
  `Datastore/tests/test_first_bounce_round_trip.py:45` (5), `Datastore/tests/test_fixed_T_values_round_trip.py:47`
  (5), `Datastore/tests/test_scalarmodel_failure_reason.py:39` (4), and
  `ComputeTargets/tests/test_foreign_bbn_provenance.py:49` (6; `TestProvenanceOnStoredRows` at
  `ComputeTargets/tests/test_foreign_bbn_provenance.py:236`). The worked example of building the
  package's actor directly, with a stand-in broker, is the package's
  `test_version_keyed_lookups.TestTheActor` (`datastorekit/tests/test_version_keyed_lookups.py:309`);
  it is in this repository, not in the wheel.
- `CLAUDE.md:68-72`'s `__ray_actor_class__` is still available: the package's actor is a
  `@ray.remote` class, reached as `datastorekit.SQL.Datastore.Datastore`.

## 8. Which of its stores the package refuses, and why

**D4: CPBH's stores are rebuilt, not migrated.** Every CPBH store is refused. The order is read
from the package's code; **no store was opened** to observe it.

**Read-write** (`ShardedPool(...)` on an existing primary):
1. **`StoreSchemaMismatch`: the primary lacks `replication_in_flight`.** The pool's first read of an
   existing primary refuses one whose tables differ from the six it declares
   (`_refuse_a_primary_that_differs`, `datastorekit/SQL/ShardedPool.py:851-878`, called at
   `datastorekit/SQL/ShardedPool.py:258`). CPBH's layer never makes that table (`git grep
   replication_in_flight 52142d7` finds nothing). **Every CPBH store stops here first.**
2. **The absolute shard record.** CPBH records each shard by the absolute path of a resolved
   primary (`Datastore/SQL/ShardedPool.py:88`, `Datastore/SQL/ShardedPool.py:296`). The package
   accepts only a bare file name (`datastorekit/shard_paths.py:51-55`), and refuses any other
   record as unusable (`datastorekit/SQL/ShardedPool.py:2476-2481`).
3. **`ReplicatedDivergence` on `timestamp`.** CPBH's actor stamps `datetime.now()` on each insert
   (`Datastore/SQL/Datastore.py:679-680`), so each shard's copy of a replicated row carries its
   own time. The check at open compares replicated tables across shards, and the package's
   replicated write stamps one time on every shard (contract §2, `timestamp`).

**Read-only** (`ShardedPool(read_only=True)`, or `open_read_only`), a different order
(`datastorekit/SQL/ShardedPool.py:440-470`):
1. **the absolute shard record**, refused by the reader as it reads the primary's `shards`
   (`datastorekit/store_reader.py:206-209`);
2. **`replicated_tables` naming `LambdaCDM`**, a class the registry does not declare
   (`datastorekit/store_reader.py:166-172`);
3. a shard whose tables differ from the declared ones, `StoreSchemaMismatch` (not measured);
4. **the primary's `StoreSchemaMismatch`** (`replication_in_flight`);
5. **`ReplicatedDivergence`**, compared read-only;
6. a label the store lacks, `ReadOnlyMiss`.

**A store the package rebuilds is still refused read-only** while CPBH's `replicated_tables` names
`LambdaCDM` (`config/sharding.py:34`), which no factory registers. A read-write pool accepts the
name, keeps only the names with a table for its checks (`datastorekit/SQL/ShardedPool.py:1345`),
and writes the list it was given to the primary's record (`datastorekit/SQL/ShardedPool.py:920`);
the reader then refuses that record (`datastorekit/store_reader.py:166-172`).

**The stores, by name only:**
- the pilot store in the working tree, `pilot-2026.6.0.db` and its 16 shards (untracked);
- the science store `~/ChamPBH-stores/science-2026.6.0.db` and its shards, and the BBN-refresh copy
  `~/ChamPBH-stores-bt02/` (`.documents/review-remediation-verification.md:1257-1259`).

**What a rebuild needs:**
- **a fresh primary path**: the package makes a new store only where no primary exists;
- **the run scripts' hard-coded store**: `DB="$STORE_DIR/science-2026.6.0.db"` (`full_run_2026.6.0.sh:11`;
  `STORE_DIR` is overridable, `full_run_2026.6.0.sh:10`; the refresh script's default is
  `~/ChamPBH-stores-bt02`, `full_run_2026.6.0-refresh.sh:10`), and their `--inventory` step
  (item 6);
- **the copy route.** CPBH's BBN refresh copies a store with `cp -p`
  (`.documents/review-remediation-verification.md:1258`) and runs `main.py` on the copy with
  `--drop bbn-data`, as `BBN_REFRESH_ROUTE` says (`pipeline_selection.py:217-219`, a message). The
  package refuses a copy of a CPBH-era store (its absolute records). It opens a file-level copy of
  a store the package wrote, whose records are bare names (`datastorekit/shard_paths.py:72-103`),
  and its own route is `ShardedPool.copy_store` (`datastorekit/SQL/ShardedPool.py:2546`), run as
  `python -m datastorekit.tools.sharded_store copy SRC DST`.

**Advice:** until G3, a copy of a CPBH store in any directory still opens the original's shards
(README §7 of this campaign), so a copy is a backup only and is never run against.

## 9. Its acceptance (G3)

G3 holds when CPBH has adopted `v0.2.0` in a campaign of its own:
1. its 9 layer files are deleted, and it imports `datastorekit` at the pinned tag;
2. **its suites pass** (`CLAUDE.md:64-66`);
3. **a pilot store is rebuilt through the package.**

What CPBH compares the rebuild against is CPBH's choice. What exists: the pilot store and
`pilot-out/` in the working tree (untracked), and the science store and its outputs
(`~/ChamPBH-stores/`, item 8).

## 10. What goes stale in it

- **`CLAUDE.md:66`**, the `Datastore/tests` command: the directory keeps only CPBH's own tests
  (item 7).
- **`CLAUDE.md:68-72`**: the undecorated `Datastore.__ray_actor_class__` is still how a test builds
  an actor, but it is `datastorekit.SQL.Datastore.Datastore`, and it takes `replicated_tables` and
  `factories=` and writes no version row (item 7).
- **`CLAUDE.md:74-75`** says to record the per-package test counts before and after every prompt;
  `CLAUDE.md` itself holds no counts.
- **`.documents/architecture-summary.md`**, well beyond the directory tree at
  `.documents/architecture-summary.md:38-48`: §4, "The Database Layer"
  (`.documents/architecture-summary.md:213-393`), and §§12–14 (from
  `.documents/architecture-summary.md:975`) describe the layer CPBH deletes.
- **`[00-two-files-are-not-black-clean]`** (`.documents/OPEN_ISSUES.md:48`) names
  `Datastore/SQL/ObjectFactories/base.py`, which is deleted.

---

## Addendum: v0.2.1 (extraction prompt 10, 2026-10-10)

*Written by extraction prompt 10 on 2026-10-10, and added to 07a's text, which stays as written
and true of `v0.2.0` (`CLAUDE.md` rule 6). CPBH was not re-measured (decision U37); what this
section says of CPBH comes from 07a's measurements, log 08a §3 and the `KeyError` measure below.*

**The pin.** CPBH adopts **`v0.2.1`** in place of `v0.2.0` (decision U37), and G3 reads "CPBH has
adopted `v0.2.1`":

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.1
```

`v0.2.1` carries `key_on_version`, `v0.2.0`'s feature, unchanged.

**What changed for CPBH since `v0.2.0`.** The three changes are
[`docs/client-contract.md` §9](../client-contract.md#9-changes-after-v020)'s rows, and
[`README.md`'s addendum](README.md#addendum-v021-extraction-prompt-10-2026-10-10) gives them for
every client. Nothing CPBH supplies changes, so items 1–10 stand as written but for the
statements below.
- **The vectorized get.** The refusal of a bare `beta_value` (item 6) is unchanged, and CPBH still
  converts its 7 calls to the mapping form, `{"shard_key": beta}`. At `v0.2.1`
  `object_get_vectorized` is `datastorekit/SQL/ShardedPool.py:3327-3351`: its membership test is
  `:3339` and the payload line `:3348`, so a bare key is refused before the payload line, as at
  `v0.2.0`. Once CPBH has converted, the package sends each shard copies of the payloads,
  `{**value, **shard_key}`, and CPBH's dicts are left as they were passed. **The in-place hazard
  is gone.** CPBH reads no payload list back in any case (log 08a §3).
- **The `KeyError`.** A reopen whose primary records a sharded table that `sharded_tables` lacks is
  refused with the intended `RuntimeError`, not a bare `KeyError`
  (`datastorekit/SQL/ShardedPool.py:1071-1072`, `:1100-1103`), and CPBH's code does not depend on
  the `KeyError`: measured through `git grep` at `52142d7`, CPBH catches `KeyError` nowhere, and has
  no `try` within three lines before a `ShardedPool(` outside its layer.
- **The refused open.** An open that raises closes the actors it built and disposes the pool's
  engine (`datastorekit/SQL/ShardedPool.py:203-207`, `:375-408`): a client that retries refused
  opens no longer holds a file descriptor per refused engine until the collector runs.

**Line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, read at that tag
(`240028e`). A `datastorekit/` line in this addendum is `v0.2.1`'s, whose `datastorekit/` is the
tree of extraction prompt 09's commit `cad7bc1`.

**What this addendum supersedes**, in this file. Each `path:line` is this file's as committed with
this addendum. In 07a's file (`dd45243`) every line after `:15` is five lines earlier, since the
italic line under the title adds five.

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/champbh.md:6` | the package at **`v0.2.0`** | at `v0.2.1`, with this addendum |
| `docs/adoption/champbh.md:22-23` | a `datastorekit/` line is the package's at `v0.2.0` | still so for 07a's text; a `datastorekit/` line in this addendum is at `v0.2.1` |
| `docs/adoption/champbh.md:259-260` | "It also adds that mapping to every payload dict in place" | `v0.2.1` sends copies, and leaves CPBH's dicts as passed; "The vectorized get", above |
| `docs/adoption/champbh.md:379` | G3 holds when CPBH has adopted `v0.2.0` | G3 holds when CPBH has adopted `v0.2.1` (U37) |

---

## Addendum: v0.2.2 (actor-names prompt 02, 2026-10-11)

*Written by `actor-names` prompt 02 on 2026-10-11, and added after extraction prompt 10's `v0.2.1`
addendum. 07a's text and the `v0.2.1` addendum stay as written, each true of the release it names
(`CLAUDE.md` rule 6). CPBH was not re-measured (as decision U37); what this section says of CPBH
comes from 07a's measurements and from reads through `git` only, at `52142d7`.*

**The pin.** CPBH adopts **`v0.2.2`** in place of `v0.2.1` (decision U3 of the `actor-names`
campaign, which amends extraction decision U37), and G3 reads "CPBH has adopted `v0.2.2`":

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.2
```

`v0.2.2` carries `key_on_version`, `v0.2.0`'s feature, and `v0.2.1`'s three fixes, unchanged.

**What changed for CPBH since `v0.2.1`.** The changes are the rows of
[`docs/client-contract.md` §9.3](../client-contract.md#93-actor-names-prompt-01) and
[§9.4](../client-contract.md#94-actor-names-prompt-01b), and
[`README.md`'s addendum](README.md#addendum-v022-actor-names-prompt-02-2026-10-11) gives them for
every client: a closed pool, and an open that is refused, release their actors' names at once; a
closed pool's handles are dead; a second `__exit__` does nothing. Two pools open at once still
collide, and closing a pool never starts Ray. Nothing CPBH supplies changes, so items 1–10 stand
as the `v0.2.1` addendum leaves them.
- **Item 6's constructions.** CPBH constructs the pool 3 times (item 6): `main.py:1338`,
  `plot_ScalarModel.py:1577` and `plot_by_beta.py:1007`. Read by an `ast` read of `git show`, each
  is a `with ShardedPool(…) as pool:` block, the only construction in its file and the last
  statement of its block, and nothing after it names `pool`. CPBH calls no pool's `__exit__`
  directly: the two `super().__exit__` calls `git grep` finds, `Quadrature/simple_quadrature.py:60`
  and `Quadrature/supervisors/ScalarField.py:105`, are not pools. It calls neither `ray.kill` nor
  `ray.get_actor`, and reads no pool's `_shards` or `_broker`. So CPBH uses no closed pool and
  meets no dead handle, and since each script opens one pool per process it never met the defect
  either. **For CPBH the fix is latent.**
- **Nothing in item 6 or item 8 changes.** No API is added or removed, and no message, refusal or
  exception of the layer's changes: the constructor, which takes neither `drop_actions=` nor
  `inventory_config=` and requires `factories=`, and the vectorized get's refusal of a bare
  `beta_value` are as at `v0.2.1`. Nothing the layer writes changes, so every CPBH store is refused
  in the same order, by the same exceptions, and is rebuilt (D4).

**Line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, read at that tag
(`240028e`), and one in the `v0.2.1` addendum stays `v0.2.1`'s (`33778b0`). This addendum cites no
`datastorekit/` line; one cited here would be `v0.2.2`'s, whose `datastorekit/` is the tree of
`actor-names` prompt 01b's commit `f024fc6`.

**What this addendum supersedes**, in this file. Each `path:line` is this file's as committed with
this addendum. In the file as extraction prompt 10 left it (`33778b0`), every line after `:21` is
six lines earlier, since this addendum's italic line under the title adds six: so the `v0.2.1`
addendum's citations, which are that file's, are read at `33778b0`, or six lines later here (all
but `:6`, which is above the insert).

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/champbh.md:17-20` | the `v0.2.1` addendum gives the pin **`v0.2.1`** | it gives `v0.2.1`'s pin and changes, true of `v0.2.1`; this addendum gives `v0.2.2` |
| `docs/adoption/champbh.md:418-419` | "CPBH adopts **`v0.2.1`** in place of `v0.2.0`", and G3 reads "CPBH has adopted `v0.2.1`" | CPBH adopts `v0.2.2` in place of `v0.2.1` (`actor-names` U3), and G3 reads "CPBH has adopted `v0.2.2`" |
| `docs/adoption/champbh.md:422` | the pin `…@v0.2.1` | the pin `…@v0.2.2`, above |
| `docs/adoption/champbh.md:452-454` | the `v0.2.1` addendum's `path:line`s are "this file's as committed with this addendum" | they are read at `33778b0`, or six lines later here (all but `:6`) |
| `docs/adoption/champbh.md:458` | the package "at `v0.2.1`, with this addendum" | at `v0.2.2`, with both addenda |
| `docs/adoption/champbh.md:461` | "G3 holds when CPBH has adopted `v0.2.1` (U37)" | G3 holds when CPBH has adopted `v0.2.2` (U37; `actor-names` U3) |

---

## Addendum: v0.2.3 (factory-defaults prompt 02, 2026-10-11)

*Written by `factory-defaults` prompt 02 on 2026-10-11, and added after `actor-names` prompt 02's
`v0.2.2` addendum. 07a's text, the `v0.2.1` addendum and the `v0.2.2` addendum stay as written,
each true of the release it names (`CLAUDE.md` rule 6). CPBH was not re-measured (as decision
U37); what this section says of CPBH comes from 07a's measurements and from reads through `git`
only, at `52142d7`.*

**The pin.** CPBH adopts **`v0.2.3`** in place of `v0.2.2` (decision U5 of the `factory-defaults`
campaign, which keeps extraction decision U37 and `actor-names` decision U3 for CPBH), and G3
reads "CPBH has adopted `v0.2.3`":

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.3
```

`v0.2.3` carries `key_on_version`, `v0.2.0`'s feature, `v0.2.1`'s three fixes and `v0.2.2`'s fix,
unchanged.

**What changed for CPBH since `v0.2.2`.** The change is
[`docs/client-contract.md` §9.5](../client-contract.md#95-factory-defaults-prompt-01)'s, and
[`README.md`'s addendum](README.md#addendum-v023-factory-defaults-prompt-02-2026-10-11) gives it for
every client: `SQLAFactoryBase` keeps `register` and `build` abstract and defaults `store`,
`validate` and `validate_on_startup`, so a factory class that defines the two can be instantiated
and its instance registered. Nothing CPBH supplies changes, nothing the layer writes changes, and
no message, refusal or exception of the layer's. **For CPBH it removes item 5's U32 obligation.**
- **CPBH's registry of instances works as it stands.** Read by an `ast` read of every `.py` file
  through `git show` at `52142d7`: 23 classes whose bases name `SQLAFactoryBase`, 20 of them
  lacking one of `store`, `validate` and `validate_on_startup`, and none lacking `register` or
  `build`; 27 calls of them by name, all in the registry (`Datastore/SQL/Datastore.py:95-121`), 24
  of them of a class lacking one of the three. Under `v0.2.2` each of those 24 raises `TypeError`
  where the registry is built; under `v0.2.3` each instantiates, since every class defines
  `register` and `build`. Item 5 asks nothing of CPBH's factories but the base's import path
  (item 3), and neither of its two routes is needed.
- **The defaults are static.** A hook a CPBH class defines with `self` overrides the base's default
  as before, and is called on the instance. A hook it does not define raises a bare
  `NotImplementedError` when the layer calls it, as CPBH's own base does today
  (`Datastore/SQL/ObjectFactories/base.py:16-30` at `52142d7`: a plain class whose five hooks are
  instance methods raising `NotImplementedError`). The layer calls `store` only on an
  `object_store`, `validate` only on an `object_validate`, and `validate_on_startup` only for a
  class whose `register()` declares `validate_on_startup: True` (contract §3), which none of the 20
  does.
- **The quantity factories** (`sqla_dimensionful_quantity_factory`, five registry entries, and
  `sqla_dimensionless_quantity_factory`, one) are each one class whose instance holds the
  `ObjectType` that tells its table apart. One class over several tables, each an instance, is the
  case of the package's parameterised factory test (`datastorekit/tests/test_factory_instances.py`,
  test 2). Contract §9.5's third row says what a
  registered instance must be under Ray: of a class defined at module level, with picklable
  attributes.
- **Item 5's other findings are unchanged:** the keyed lookups of `ScalarModel`,
  `AdiabaticHistory` and `BBNData`, the layer's own tables, and the six `inventory()` hooks the
  package never calls. So are items 6 and 8: the constructor and the vectorized get are as at
  `v0.2.2`, and every CPBH store is refused in the same order, by the same exceptions, and is
  rebuilt (D4).

**Line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, read at that tag
(`240028e`), and one in the `v0.2.1` addendum stays `v0.2.1`'s (`33778b0`). The `v0.2.2` addendum
cites none. This addendum cites no `datastorekit/` line; one cited here would be `v0.2.3`'s, whose
`datastorekit/` is the tree of `factory-defaults` prompt 01's commit `f5d8957`.

**What this addendum supersedes**, in this file. Each `path:line` is this file's as committed with
this addendum. In the file as `actor-names` prompt 02 left it (`6d8ee9a`), every line after `:27`
is six lines earlier, since this addendum's italic line under the title adds six. So the `v0.2.2`
addendum's citations, which are that file's, are read at `6d8ee9a`, or six lines later here (all
but `:17-20`, which is above the insert). The `v0.2.1` addendum's citations, which the `v0.2.2`
addendum reads at `33778b0` or six lines later, are read at `33778b0`, or twelve lines later here
(all but `:6`).

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/champbh.md:22-26` | the `v0.2.2` addendum gives the pin **`v0.2.2`** | it gives `v0.2.2`'s pin and changes, true of `v0.2.2`; this addendum gives `v0.2.3` |
| `docs/adoption/champbh.md:40-41` | "its factory base is an ABC, and CPBH registers instances of 20 classes that define only two of its five abstract hooks (U32)" | at `v0.2.3` the base's only abstract hooks are `register` and `build`, which all 23 classes define, so CPBH's instances are accepted; "What changed for CPBH since `v0.2.2`", above |
| `docs/adoption/champbh.md:213-215` | "The package's `SQLAFactoryBase` is an ABC with the five abstract (`datastorekit/SQL/factory_base.py:5-29`). Subclassing it, `sqla_version_factory()` and the other 19 raise `TypeError` at instantiation" | true through `v0.2.2`. At `v0.2.3` the base defaults the three, and each of the 20 instantiates |
| `docs/adoption/champbh.md:216-227` | "The two routes, and what each needs": define the three hooks on each of the 20, or register the class itself | neither is needed at `v0.2.3`: CPBH registers its instances as they stand. The rest of item 5's U32 paragraph (`:206-212`), the counts and CPBH's own base, still holds |
| `docs/adoption/champbh.md:478-479` | "CPBH adopts **`v0.2.2`** in place of `v0.2.1`", and G3 reads "CPBH has adopted `v0.2.2`" | CPBH adopts `v0.2.3` in place of `v0.2.2` (`factory-defaults` U5), and G3 reads "CPBH has adopted `v0.2.3`" |
| `docs/adoption/champbh.md:482` | the pin `…@v0.2.2` | the pin `…@v0.2.3`, above |
| `docs/adoption/champbh.md:515-519` | the `v0.2.2` addendum's `path:line`s are "this file's as committed with this addendum" | they are read at `6d8ee9a`, or six lines later here (all but `:17-20`) |
| `docs/adoption/champbh.md:524` | in the `v0.2.2` addendum's table, CPBH adopts `v0.2.2` in place of `v0.2.1`, and G3 reads "CPBH has adopted `v0.2.2`" | as `:478-479` |
| `docs/adoption/champbh.md:525` | "the pin `…@v0.2.2`, above" | the pin `…@v0.2.3`, above |
| `docs/adoption/champbh.md:527` | the package "at `v0.2.2`, with both addenda" | at `v0.2.3`, with the three addenda |
| `docs/adoption/champbh.md:528` | "G3 holds when CPBH has adopted `v0.2.2` (U37; `actor-names` U3)" | G3 holds when CPBH has adopted `v0.2.3` (U37; `actor-names` U3; `factory-defaults` U5) |

---

## Addendum: v0.3.0 (object-timestamp prompt 02, 2026-10-12)

*Written by `object-timestamp` prompt 02 on 2026-10-12, and added after `factory-defaults` prompt
02's `v0.2.3` addendum. 07a's text and the `v0.2.1`, `v0.2.2` and `v0.2.3` addenda stay as written,
each true of the release it names (`CLAUDE.md` rule 6). CPBH was not re-measured (as decision
U37); what this section says of CPBH comes from 07a's measurements and from reads through `git`
only, at `52142d7` and at the commits named.*

**The pin.** CPBH may stay on **`v0.2.3`** or move to **`v0.3.0`**, as CPBH chooses, a move being
a commit of its own (decision U6 of the `object-timestamp` campaign, which amends
`factory-defaults` decision U5 for CPBH), and G3 reads "CPBH has adopted `v0.2.3` or later":

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.3
```

or

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.3.0
```

`v0.3.0` carries `key_on_version`, `v0.2.0`'s feature, `v0.2.1`'s three fixes, `v0.2.2`'s fix and
`v0.2.3`'s change, unchanged.

**What changed for CPBH since `v0.2.3`.** The change is
[`docs/client-contract.md` §9.6](../client-contract.md#96-object-timestamp-prompt-01)'s, and
[`README.md`'s addendum](README.md#addendum-v030-object-timestamp-prompt-02-2026-10-12) gives it for
every client: the package's `DatastoreObject` takes an optional, keyword-only `timestamp` and
exposes it as a read-only property, and the layer never sets it and never reads it. Nothing CPBH
supplies changes, nothing the layer writes or reads changes, and no message, refusal or exception
of the layer's. **Nothing changes for CPBH but one key in `vars()`.**
- **CPBH passes `store_id` alone.** Read by an `ast` read of every `.py` file through `git show`,
  outside `prompts/`, `.prompts/`, `docs/` and `.documents/`, at `64ef9aa` (the planner's),
  `cb0c675` and `0f1c25b` (CPBH's `HEAD` when read, 2026-10-12, branch `dk-and-rpk-migration`),
  the same at each: 31
  classes descend from CPBH's own `DatastoreObject` (`Datastore/object.py:19`, which takes
  `store_id` alone, and is deleted with its layer, item 2); the 19 calls
  `DatastoreObject.__init__(…)` each pass `store_id` alone; and no class defines or assigns
  `timestamp`. Each call is accepted under `v0.3.0` as under `v0.2.3`.
- **One key more in `vars()`.** Every `DatastoreObject` has `_timestamp`, `None` unless given, in
  its `vars()`. CPBH reads no stored object's `vars()` or `__dict__`: its one `vars(` is of a
  module (`Datastore/tests/test_compare_stores.py:735`).
- **Its factories may pass the row's value, and need not.** Most of CPBH's classes declare
  `"timestamp": True` (item 5's table, `:189-207`), so a factory that reads such a row may pass the
  row's `timestamp` to the object it builds, by keyword, if CPBH chooses. The layer fills nothing.
- **Item 8's `ReplicatedDivergence` on `timestamp`** (`:351-354`) is unchanged: it is about the
  stamp CPBH's actor writes to each shard, not about the object.
- **Item 5's other findings, and items 6 and 8, are unchanged**: every CPBH store is refused at
  open in the same order, by the same exceptions, and is rebuilt (D4).

**Line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, read at that tag
(`240028e`), and one in the `v0.2.1` addendum stays `v0.2.1`'s (`33778b0`). The `v0.2.2` and
`v0.2.3` addenda cite none, and neither does this addendum; one cited here would be `v0.3.0`'s,
whose `datastorekit/` is the tree of `object-timestamp` prompt 01's commit `1b2f91a`. A CPBH line is
CPBH's at the commit named.

**What this addendum supersedes**, in this file. Each `path:line` below is this file's as committed
with this addendum. In the file as `factory-defaults` prompt 02 left it (`0de2b16`), every line after
`:33` is six lines earlier, since this addendum's italic line under the title adds six (N = 6). So:
- the `v0.2.3` addendum's citations, which are that file's, are read at `0de2b16`, or **6** lines
  later here (all but `:22-26`, which is above the insert);
- the `v0.2.2` addendum's, which the `v0.2.3` addendum reads at `6d8ee9a` or six lines later, are
  read at `6d8ee9a`, or **12** lines later here (all but `:17-20`);
- the `v0.2.1` addendum's, which the `v0.2.3` addendum reads at `33778b0` or twelve lines later, are
  read at `33778b0`, or **18** lines later here (all but `:6`).

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/champbh.md:28-32` | the `v0.2.3` addendum gives the pin **`v0.2.3`** | it gives `v0.2.3`'s pin and changes, true of `v0.2.3`; this addendum gives CPBH's pins at `v0.3.0`: `v0.2.3` or `v0.3.0`, as CPBH chooses |
| `docs/adoption/champbh.md:546-548` | "CPBH adopts **`v0.2.3`** in place of `v0.2.2`", and G3 reads "CPBH has adopted `v0.2.3`" | CPBH may stay on `v0.2.3` or move to `v0.3.0` (`object-timestamp` U6), and G3 reads "CPBH has adopted `v0.2.3` or later"; "The pin", above |
| `docs/adoption/champbh.md:550-552` | the pin `…@v0.2.3` | `…@v0.2.3` or `…@v0.3.0`, as CPBH chooses, above |
| `docs/adoption/champbh.md:598-604` | the `v0.2.3` addendum's `path:line`s are "this file's as committed with this addendum", and the earlier addenda's are read six and twelve lines later | they are read at `0de2b16`, or six lines later here; the `v0.2.2` addendum's twelve, and the `v0.2.1` addendum's eighteen; above |
| `docs/adoption/champbh.md:612` | the row for `:478-479`: CPBH adopts `v0.2.3` in place of `v0.2.2`, and G3 reads "CPBH has adopted `v0.2.3`" | as `:546-548` |
| `docs/adoption/champbh.md:613` | the row for `:482`: "the pin `…@v0.2.3`, above" | as `:550-552` |
| `docs/adoption/champbh.md:614` | the row for `:515-519`: the `v0.2.2` addendum's citations "are read at `6d8ee9a`, or six lines later here" | at `6d8ee9a`, or twelve lines later here (all but `:17-20`) |
| `docs/adoption/champbh.md:615-616` | the rows for `:524` and `:525`, "as `:478-479`" and "the pin `…@v0.2.3`, above" | as `:546-548` and `:550-552` |
| `docs/adoption/champbh.md:617` | the row for `:527`: "at `v0.2.3`, with the three addenda" | at `v0.2.3` or `v0.3.0`, as CPBH chooses, with the four addenda |
| `docs/adoption/champbh.md:618` | the row for `:528`: "G3 holds when CPBH has adopted `v0.2.3` (U37; `actor-names` U3; `factory-defaults` U5)" | G3 holds when CPBH has adopted `v0.2.3` or later (U37; `actor-names` U3; `factory-defaults` U5; `object-timestamp` U6) |

---

## Appendix: the script's output

Made by, from DatastoreKit's repository root:

```bash
./venv/bin/python docs/extraction/measure_client_imports.py cpbh
```

# Imports of the layer: ChamPBH (CPBH) at `52142d7`

Written by `docs/extraction/measure_client_imports.py`, reading through `git ls-tree` and `git show` only.

- **Repository:** `/Users/ds283/Documents/Code/ChamPBH`
- **Commit:** `52142d75aebe00855804e2daff4f63aee50ffc3e` (given as `52142d7`), 2026-10-07 Store each shard key under its own serial
- **Layer files** (9): `Datastore/__init__.py`, `Datastore/object.py`, `Datastore/SQL/__init__.py`, `Datastore/SQL/ClientPool.py`, `Datastore/SQL/Datastore.py`, `Datastore/SQL/ProfileAgent.py`, `Datastore/SQL/SerialPoolBroker.py`, `Datastore/SQL/ShardedPool.py`, `Datastore/SQL/ObjectFactories/base.py`
- **Layer files absent at this commit:** none
- **Factory package:** `Datastore/SQL/ObjectFactories/` (its `base.py` is the layer's)
- **Files read:** 196 tracked `.py` files outside the layer; 0 do not parse

## Totals

| What | Count |
|---|---|
| Import statements naming a layer module | **41** in 38 files |
| of which nested (not at module level) | 0 |
| String literals naming a layer module | 0 (0 exactly its name) |
| `import_module` / `__import__` calls naming a layer module | 0 |
| Import statements naming a factory module (not layer imports) | 1 (1 outside `Datastore/SQL/ObjectFactories/`) |
| Imports of names that move into the package | 4 |

## Layer imports, by group

| Group | Statements | Nested | Files |
|---|---|---|---|
| `(top level)` | 6 | 0 | 3 |
| `ComputeTargets/` | 3 | 0 | 3 |
| `CosmologyConcepts/` | 5 | 0 | 5 |
| `CosmologyModels/` | 1 | 0 | 1 |
| `Datastore/SQL/ObjectFactories/` | 17 | 0 | 17 |
| `Datastore/tests/` | 2 | 0 | 2 |
| `MetadataConcepts/` | 3 | 0 | 3 |
| `Quadrature/` | 1 | 0 | 1 |
| `RayTools/` | 1 | 0 | 1 |
| `config/` | 1 | 0 | 1 |
| `prompts/` | 1 | 0 | 1 |
| **total** | **41** | **0** | **38** |

## Layer imports, by module

A statement naming two layer modules is counted under each.

| Module | Statements | Names imported by `from` (statements) |
|---|---|---|
| `Datastore` | 13 | `DatastoreObject` 13 |
| `Datastore.SQL.Datastore` | 2 | `Datastore` 2 |
| `Datastore.SQL.ObjectFactories.base` | 17 | `SQLAFactoryBase` 17 |
| `Datastore.SQL.ProfileAgent` | 3 | `ProfileAgent` 3 |
| `Datastore.SQL.ShardedPool` | 6 | `ShardedPool` 6 |

## Every layer import

### `(top level)` (6)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `main.py:47` | — | `Datastore.SQL.ProfileAgent` | `ProfileAgent` |
| `main.py:48` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `plot_ScalarModel.py:41` | — | `Datastore.SQL.ProfileAgent` | `ProfileAgent` |
| `plot_ScalarModel.py:42` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `plot_by_beta.py:35` | — | `Datastore.SQL.ProfileAgent` | `ProfileAgent` |
| `plot_by_beta.py:36` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |

### `ComputeTargets/` (3)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `ComputeTargets/AdiabaticHistory.py:11` | — | `Datastore` | `DatastoreObject` |
| `ComputeTargets/BBNData.py:13` | — | `Datastore` | `DatastoreObject` |
| `ComputeTargets/ScalarModel.py:44` | — | `Datastore` | `DatastoreObject` |

### `CosmologyConcepts/` (5)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `CosmologyConcepts/ConformalCouplings/AbstractCoupling.py:19` | — | `Datastore` | `DatastoreObject` |
| `CosmologyConcepts/DimensionfulQuantity.py:19` | — | `Datastore` | `DatastoreObject` |
| `CosmologyConcepts/DimensionlessQuantity.py:19` | — | `Datastore` | `DatastoreObject` |
| `CosmologyConcepts/Potentials/AbstractPotential.py:19` | — | `Datastore` | `DatastoreObject` |
| `CosmologyConcepts/redshift.py:19` | — | `Datastore` | `DatastoreObject` |

### `CosmologyModels/` (1)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `CosmologyModels/base.py:18` | — | `Datastore` | `DatastoreObject` |

### `Datastore/SQL/ObjectFactories/` (17)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `Datastore/SQL/ObjectFactories/AdiabaticHistory.py:28` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/BBNData.py:16` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/DimensionfulQuantity.py:20` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/DimensionlessQuantity.py:21` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/ExponentialCoupling.py:21` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/ExponentialPotential.py:21` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/InversePowerPotential.py:21` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/QCD_Cosmology.py:19` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/ReclinerPotential.py:21` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/ReflectingPotential.py:21` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/ScalarModel.py:39` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/Starobinsky.py:21` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/integration_metadata.py:18` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/redshift.py:24` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/store_tag.py:18` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/tolerance.py:20` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/version.py:18` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |

### `Datastore/tests/` (2)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `Datastore/tests/test_shard_key_assignment.py:40` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `Datastore/tests/test_version_keyed_lookups.py:45` | — | `Datastore.SQL.Datastore` | `Datastore` |

### `MetadataConcepts/` (3)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `MetadataConcepts/store_tag.py:16` | — | `Datastore` | `DatastoreObject` |
| `MetadataConcepts/tolerance.py:18` | — | `Datastore` | `DatastoreObject` |
| `MetadataConcepts/version.py:16` | — | `Datastore` | `DatastoreObject` |

### `Quadrature/` (1)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `Quadrature/integration_metadata.py:18` | — | `Datastore` | `DatastoreObject` |

### `RayTools/` (1)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `RayTools/RayWorkPool.py:23` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |

### `config/` (1)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `config/model_list.py:19` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |

### `prompts/` (1)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `prompts/run-integrity/planning-probes/datastore_version_probe.py:18` | — | `Datastore.SQL.Datastore` | `Datastore` |

## String literals naming a layer module

None.

## `import_module` calls naming a layer module

None.

## Imports of factory modules, by group (count only)

| Group | Statements |
|---|---|
| `(top level)` | 1 |
| **total** | **1** |

## Imports of names that move into the package

`config.version`: `VERSION_SERIAL_KEY`, `require_version_serial`.

| File:line | Module | Names |
|---|---|---|
| `Datastore/SQL/ObjectFactories/AdiabaticHistory.py:31` | `config.version` | `require_version_serial` |
| `Datastore/SQL/ObjectFactories/BBNData.py:20` | `config.version` | `require_version_serial` |
| `Datastore/SQL/ObjectFactories/ScalarModel.py:44` | `config.version` | `require_version_serial` |
| `Datastore/tests/test_version_keyed_lookups.py:350` | `config.version` | `VERSION_SERIAL_KEY` |

## Files that do not parse

None.
