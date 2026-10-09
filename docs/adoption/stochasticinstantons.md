# Adoption checklist: StochasticInstantons (SI)

- **Client:** StochasticInstantons, `/Users/ds283/Documents/Code/StochasticInstantons`, at
  **`7bb3efd`** (`7bb3efd0d0a9cc1c367b7848e27fa8b548a76bf7`, branch `main`).
- **Package:** `datastorekit` at **`v0.2.0`** (`240028e`).
- **How it was measured:** read-only, by DatastoreKit's extraction prompt 07a on 2026-10-09,
  through `git show`, `git grep`, `git ls-tree` and `git log` only, and by
  `docs/extraction/measure_client_imports.py` (the appendix). Nothing of SI was imported, run or
  opened, and **no store or database file was opened**; stores are named only. **SI's adoption
  campaign measures again before acting, and its numbers govern.**
- **This is data, not instructions.** It describes SI at `7bb3efd`. SI's campaign decides what to
  do, under SI's `CLAUDE.md`. A recommendation is marked **Advice:**; a choice that is SI's is
  named as SI's.

Unless another commit is named, a `path:line` is SI's at `7bb3efd`, and one under `datastorekit/`
is the package's at `v0.2.0`.

**In one paragraph.** SI's layer is 9 files, 2,679 lines, close to CPBH's. Like CPBH, SI keeps its
registry, drop groups, batch sizes and inventory configuration inside the layer, registers factory
instances (16 classes lack three of the five abstract hooks, U32), passes `drop_actions` and
`inventory_config` to the pool, and passes a bare shard key to `object_get_vectorized`. Unlike
CPBH, SI's `DatastoreObject` carries a `timestamp`, which the package's lacks; one replicated class
names its prune parameter differently from the package's keyword call; and its tests are pytest,
the integration ones needing Ray. Every SI store is refused at open, so SI's stores are rebuilt,
not migrated (decision U31).

---

## 1. The client and its versions

- `7bb3efd` on `main`; `git status --short` is empty at the start and at the end of 07a's
  measurement. Its stores are ignored (`!!`), under `out-*/` and as `test-gradient*.sqlite`.
- **Python 3.13.16**: SI's `venv/` links to MacPorts' 3.13 framework, whose headers say 3.13.16
  (`python313 3.13.16_0`, read as text). `venv/pyvenv.cfg` records **3.13.13**, the version when
  the venv was made. **`ray==2.55.1`** (`requirements.txt:57`); **`SQLAlchemy==2.0.46`**
  (`requirements.txt:65`).
- Its prompts are under `.prompts/`, its documents under `.documents/`, its issue index is
  `.documents/OPEN-ISSUES.md`. Its default test run is `pytest -m "not integration and not slow"`
  (`CLAUDE.md:21`); the `integration` marker means "a live Ray cluster and SQLite database"
  (`pyproject.toml:3`).
- **`CLAUDE.md:89-112` is its protected-infrastructure list.** It names more than the layer:
  `RayTools/`, `Datastore/object.py`, `Datastore/SQL/ClientPool.py`, `ShardedPool.py`,
  `SerialPoolBroker.py`, `ProfileAgent.py`, `Datastore/SQL/ObjectFactories/base.py`, **seven
  factories** (`version`, `store_tag`, `tolerance`, `DimensionlessQuantity`, `DimensionfulQuantity`,
  `integration_metadata`, `redshift`; `CLAUDE.md:99-105`), two `Quadrature/` files, `Units/`,
  `MetadataConcepts/`, `utilities.py` and `constants.py`. Only the layer's files leave SI;
  `Datastore/SQL/Datastore.py` is governed by `CLAUDE.md:111-112`.

## 2. What it deletes

**The 9 layer files, 2,679 lines:** `Datastore/__init__.py` (1), `Datastore/object.py` (45),
`Datastore/SQL/__init__.py` (1), `Datastore/SQL/ClientPool.py` (261), `Datastore/SQL/Datastore.py`
(816), `Datastore/SQL/ProfileAgent.py` (355), `Datastore/SQL/SerialPoolBroker.py` (164),
`Datastore/SQL/ShardedPool.py` (1,001), `Datastore/SQL/ObjectFactories/base.py` (35).

Item 4 lists what in them is SI's and must leave first. What the package has that SI's layer
lacks is CPBH's list (`docs/adoption/champbh.md` item 2): the schema module, the contract, the
recorded replicated write and its check at open, bare shard records, the read-only reader and
pool, the structured inventory, and the tools.

**`DatastoreObject.timestamp`.** SI's `DatastoreObject` takes `timestamp` (`Datastore/object.py:25-30`)
and exposes it as a property (`Datastore/object.py:43-45`), added at SI `51b04f8` (2026-06-21,
"Surface row-creation timestamps via DatastoreObject"). The package's `DatastoreObject`
(`datastorekit/object.py:9`) takes `store_id` only. So:
- **the 14 direct calls `DatastoreObject.__init__(…, timestamp=…)` raise `TypeError`**:
  `ComputeTargets/CompactionFunction.py:477`, `ComputeTargets/FullInstanton.py:434`,
  `ComputeTargets/GradientCoupledInstanton/GradientCoupledInstanton.py:622`,
  `ComputeTargets/InflatonTrajectory.py:207`, `ComputeTargets/SlowRollInstanton.py:433`,
  `CosmologyConcepts/DimensionfulQuantity.py:37`, `CosmologyConcepts/DimensionlessQuantity.py:31`,
  `CosmologyConcepts/Potentials/AbstractPotential.py:21`, `CosmologyModels/cosmo_params.py:35`,
  `InflationConcepts/DiffusionModel/__init__.py:29`, `InflationConcepts/alpha_regularization.py:53`,
  `InflationConcepts/efold_value.py:26`, `InflationConcepts/n_collocation_points.py:49`,
  `MetadataConcepts/tolerance.py:33`;
- **ten subclasses pass `timestamp=` through `super().__init__`** to those:
  `CosmologyConcepts/FieldValues.py:26`, `:33`; `InflationConcepts/DiffusionModel/__init__.py:76`;
  `InflationConcepts/N_final.py:17`; `InflationConcepts/N_init.py:17`;
  `InflationConcepts/QuadraticPotential.py:20`; `InflationConcepts/QuarticPotential.py:20`;
  `InflationConcepts/delta_Nstar.py:22`; `InflationConcepts/inflaton_mass.py:15`;
  `InflationConcepts/quartic_coupling.py:14`;
- **code outside the layer reads `.timestamp`**:
  - directly, and would raise `AttributeError` without it: `plotting/adapters/full.py:61`,
    `plotting/adapters/gradient.py:133`, `plotting/adapters/slow_roll.py:66`;
  - by `getattr(obj, "timestamp", None)`, and would quietly get `None`: `plotting/provenance.py:41`,
    `plotting/figures/spatial.py:259`;
  - test stand-ins set a `timestamp` attribute of their own (for example
    `tests/test_plot_adapters_golden.py:141`).

Whether SI drops the timestamp or keeps it on its own classes is SI's choice.

## 3. Which imports it rewrites

The script counts **48** import statements of the 9 modules, in **47** files, outside the layer's
own files; **1** is nested (appendix):
- **22 in the factories**, one `SQLAFactoryBase` import in each of the 22 factory modules;
- **26 statements in 25 files outside them**:
  - `DatastoreObject` 18: from the package root 12 (`CosmologyConcepts/` 4, `InflationConcepts/` 4,
    `MetadataConcepts/` 3, `Quadrature/integration_metadata.py:18`), and from `Datastore.object` 6
    (`ComputeTargets/` 5, `CosmologyModels/cosmo_params.py:19`);
  - `ShardedPool` 5: `main.py:37`, `plot_GradientCoupledSolutions.py:61`,
    `plot_InstantonSolutions.py:42`, `RayTools/RayWorkPool.py:23` (a type hint),
    `tests/conftest.py:25`, **the only test import**;
  - `ProfileAgent` 1: `main.py:36`;
  - `SQLAFactoryBase` 2 outside the factories: `CosmologyConcepts/Potentials/registry.py:5`, and
    `InflationConcepts/DiffusionModel/registry.py:5`, nested under `if TYPE_CHECKING:`.

No string literal or `import_module` call names a layer module. Two imports of factory modules lie
outside the factory package, `CosmologyConcepts/Potentials/registry.py:6-7`; they are not layer
imports.

**Two sites instantiate factories when they are imported**, besides the registry:
`CosmologyConcepts/Potentials/registry.py:33` and `CosmologyConcepts/Potentials/registry.py:40`
(`sqla_QuadraticPotential_factory()`, `sqla_QuarticPotential_factory()`), and
`Datastore/SQL/ObjectFactories/MasslessDecoupledDiffusion.py:71`
(`sqla_MasslessDecoupledDiffusion_factory()`). All three classes are among U32's (item 5), so under
the package's ABC each raises `TypeError` at import.

## 4. What leaves the layer, and where it may go

Each is SI's, lives in a file item 2 deletes, and must be moved out first. Where it goes is SI's
choice.
- **The registry**, `_factories` (`Datastore/SQL/Datastore.py:96-127`): 30 entries, each an
  **instance**. It reaches the package as `ShardedPool(factories=...)`. Its imports of the factory
  modules and of four concept classes (`Datastore/SQL/Datastore.py:28-86`) go with it.
- **The drop groups**, `_drop_actions` and `_drop_order` (`Datastore/SQL/Datastore.py:133-147`):
  five groups. The same five names are the command line's `--drop` choices
  (`config/argument_parser.py:55-61`).
- **The inventory configuration**: `InventoryConfigType` (`Datastore/SQL/Datastore.py:154`), the
  actor's `inventory()` (`Datastore/SQL/Datastore.py:789-816`), the pool's `_merge_queue()` and
  `inventory()` (`Datastore/SQL/ShardedPool.py:883-1001`), driven by `config/sharding.py:89`
  (`inventory_config`). The package has neither (item 6).
- **The serial batch sizes**, `_default_serial_batch_size` (`Datastore/SQL/ClientPool.py:24-54`),
  with a default of **5** for a table it does not name (`Datastore/SQL/ClientPool.py:172`). They
  become `ShardedPool(serial_batch_sizes=...)`; the package's default is **500**
  (`datastorekit/SQL/ClientPool.py:130`).
- **`base._timestamp_column`** (`Datastore/SQL/ObjectFactories/base.py:32-35`), a static helper
  nothing calls (`git grep _timestamp_column 7bb3efd` finds only its definition).
- **`DatastoreObject.timestamp`** (item 2).
- **The bare-shard-key branch** of `object_get_vectorized` (`Datastore/SQL/ShardedPool.py:595-596`).
- **The client imports inside the layer**: `CosmologyConcepts.FieldValues`,
  `CosmologyModels.cosmo_params`, `InflationConcepts.inflaton_mass`,
  `InflationConcepts.quartic_coupling` and the factory modules (`Datastore/SQL/Datastore.py:28-86`),
  `utilities` (`Datastore/SQL/Datastore.py:88`, `Datastore/SQL/ProfileAgent.py:26`),
  `config.defaults` (`Datastore/SQL/ProfileAgent.py:25`, `Datastore/SQL/ShardedPool.py:24`),
  `config.sharding.ShardKeyType` (`Datastore/SQL/ShardedPool.py:25`) and `MetadataConcepts.version`
  (`Datastore/SQL/ShardedPool.py:30`).

The factory modules' location is SI's choice, as for CPBH; seven of them are on SI's protected
list (item 1).

## 5. What its factories must change

**The per-factory table.** Kind is from `config/sharding.py` (`replicated_tables` from
`config/sharding.py:15`, `sharded_tables` from `config/sharding.py:43`, all on the field
`delta_Nstar`). Every hook takes `self`; none is a `staticmethod`. Paths are under
`Datastore/SQL/ObjectFactories/`.

| Registry key(s) (`Datastore/SQL/Datastore.py:96-127`) | Class | Kind | `register()` keys (besides `columns`) | Hooks defined |
|---|---|---|---|---|
| `version` | `version.py:23` | replicated | `version` False, `timestamp` False | `register`, `build` |
| `store_tag` | `store_tag.py:23` | replicated | `version` False, `timestamp` True | `register`, `build` |
| `redshift` | `redshift.py:27` | **in neither list** | `version` False, `timestamp` True | `register`, `build`; `read_table`, `inventory` |
| `tolerance` | `tolerance.py:25` | replicated | `version` False, `timestamp` True | `register`, `build` |
| `efold_value`, `delta_Nstar`, `N_init`, `N_final`, `n_collocation_points`, `alpha_regularization` | one class each (`efold.py:14`, `delta_Nstar.py:14`, `N_init.py:14`, `N_final.py:14`, `n_collocation_points.py:24`, `alpha_regularization.py:29`) | replicated | `version` False, `timestamp` True | `register`, `build`; `read_table`, `inventory` |
| `inflaton_mass`, `phi_value`, `pi_value` | `sqla_dimensionful_quantity_factory(<class>)` (`DimensionfulQuantity.py:28`) | replicated | `version` False, `timestamp` True | `register`, `build`; `read_table`, `inventory` |
| `quartic_coupling` | `sqla_dimensionless_quantity_factory(quartic_coupling)` (`DimensionlessQuantity.py:28`) | replicated | `version` False, `timestamp` True | `register`, `build`; `read_table`, `inventory` |
| `QuadraticPotential`, `QuarticPotential` | `QuadraticPotential.py:11`, `QuarticPotential.py:11` | replicated | `version` False, `timestamp` True | `register`, `build`; `load_by_serial`, `read_table`, `inventory` |
| `MasslessDecoupledDiffusion` | `MasslessDecoupledDiffusion.py:11` | replicated | `version` False, `timestamp` True | `register`, `build`; `load_by_serial` |
| `IntegrationSolver` | `integration_metadata.py:23` | replicated | `version` False, `stepping` `"minimum"`, `timestamp` True | `register`, `build` |
| `InflatonTrajectory` | `InflatonTrajectory.py:24` | replicated | `version` True, `timestamp` True, `validate_on_startup` True | all five; `read_table`, `inventory` |
| `InflatonTrajectoryValue` | `InflatonTrajectory.py:384` | replicated | `serial` False, `version` False, `timestamp` False | all five |
| `CosmologicalParams` | `CosmologicalParams.py:21` | replicated | `version` False, `timestamp` True | all five; `read_table`, `inventory` |
| `FullInstanton`, `SlowRollInstanton`, `CompactionFunction`, `GradientCoupledInstanton` | `FullInstanton.py:24`, `SlowRollInstanton.py:23`, `CompactionFunction.py:24`, `GradientCoupledInstanton.py:23` | sharded | `version` True, `timestamp` True, `validate_on_startup` True | all five; `inventory` (and `read_table` on the first two) |
| `FullInstantonValue`, `SlowRollInstantonValue`, `GradientCoupledInstantonValue` | `FullInstanton.py:542`, `SlowRollInstanton.py:537`, `GradientCoupledInstanton.py:697` | sharded | `serial` False, `version` False, `timestamp` False | all five |
| `CompactionFunctionSamples`, `GradientCoupledInstantonProfile` | `CompactionFunction.py:560`, `GradientCoupledInstanton.py:748` | sharded | `serial` True, `version` False, `timestamp` False | all five |

**U32: 16 classes, 18 registry entries.** The 16 classes that define only `register` and `build`
(with the extras shown) are those of the first ten rows: `version`, `store_tag`, `redshift`,
`tolerance`, the six parameter classes, the two quantity factories
(`sqla_dimensionful_quantity_factory` fills 3 entries), the two potentials,
`MasslessDecoupledDiffusion` and `IntegrationSolver`. SI's own `SQLAFactoryBase` is not an ABC
(`Datastore/SQL/ObjectFactories/base.py:16-30`); the package's is
(`datastorekit/SQL/factory_base.py:5-29`), so each raises `TypeError` at instantiation: in the
registry, and at the three import-time sites of item 3. The two routes, and what each needs, are
CPBH's (`docs/adoption/champbh.md` item 5): define `store`, `validate` and `validate_on_startup` on
each, or register the class once its hooks can be called without an instance. Every SI hook takes
`self`, and the quantity factories hold `ObjectType` on the instance
(`Datastore/SQL/ObjectFactories/DimensionfulQuantity.py:30`,
`Datastore/SQL/ObjectFactories/DimensionlessQuantity.py:30`). Seven of the 16 are on SI's
protected list (`CLAUDE.md:99-105`). The choice is SI's.

**`InflatonTrajectory.validate_on_startup(self, conn, table, tables, prune_unvalidated)`**
(`Datastore/SQL/ObjectFactories/InflatonTrajectory.py:256`). The package's pool calls a replicated
class's hook **by keyword**, `prune=False` and `prune=True`
(`datastorekit/SQL/ShardedPool.py:2185-2187`, `datastorekit/SQL/ShardedPool.py:2220-2221`), under
`prune_unvalidated`, and SI's `main.py` always prunes (`--prune-unvalidated` is `store_true` with
`default=True`, `config/argument_parser.py:46-48`; passed at `main.py:1356`). All 12 SI classes that
define the hook name its parameter `prune_unvalidated` (for example
`Datastore/SQL/ObjectFactories/FullInstanton.py:361`), but the keyword call reaches replicated
classes only, and of SI's replicated classes only `InflatonTrajectory` registers
`validate_on_startup: True`. So `Datastore/SQL/ObjectFactories/InflatonTrajectory.py:256` must take
`prune`; the value factory's hook at
`Datastore/SQL/ObjectFactories/InflatonTrajectory.py:431` is never called by the pool (its
`register()` does not ask for it), and the actors call every hook positionally
(`datastorekit/SQL/Datastore.py:493`).

**`InflatonTrajectory` is a replicated, validated class** (its `validated` column,
`Datastore/SQL/ObjectFactories/InflatonTrajectory.py:82`). What the contract offers: an
interrupted replicated validate is repaired at open only for a class that declares
`validated_column` and defines `revalidate`, and otherwise the shards differ and the open is
refused (`docs/client-contract.md` §2, `validated_column`; §3, `revalidate`). Its value table
names it by `trajectory_serial` (`Datastore/SQL/ObjectFactories/InflatonTrajectory.py:395-397`), so
declaring that column as `InflatonTrajectoryValue`'s `owner_column` would put the two in one unit,
copied and pruned together (§2, `owner_column`). The choice is SI's.

**The layer's own tables.** `version` and `store_tag` register `label`
(`Datastore/SQL/ObjectFactories/version.py:31`, `Datastore/SQL/ObjectFactories/store_tag.py:31`);
contract §5 holds. As in CPBH, `version`'s `build` returns a `store_tag` object
(`Datastore/SQL/ObjectFactories/version.py:51`). SI has no tag-association tables. No factory
declares `inventory_spec`, and 17 classes define an `inventory()` the package never calls.

## 6. Its call sites and pool construction

**The pool is constructed four times**: `main.py:1345-1360`, `plot_GradientCoupledSolutions.py:974-989`,
`plot_InstantonSolutions.py:1207-1224`, and `tests/conftest.py:57-71` (the `live_pool` fixture).
Each passes `drop_actions=` (`main.py:1357`, `plot_GradientCoupledSolutions.py:986`,
`plot_InstantonSolutions.py:1221`, `tests/conftest.py:68`) and `inventory_config=`
(`main.py:1359`, `plot_GradientCoupledSolutions.py:988`, `plot_InstantonSolutions.py:1223`,
`tests/conftest.py:70`), which the package does not take (a `TypeError`), and none passes
`factories=`, which it requires (`datastorekit/SQL/ShardedPool.py:95-114`).

**Each drop group's dependents under the package**, from the foreign keys SI declares (SI declares
no `inventory_spec`, so foreign keys are all `dependent_tables` reads):
- `compaction-function` and `gradient-coupled-instanton` each drop alone;
- **`full-instanton` and `slow-roll-instanton` must take `CompactionFunction` (and
  `CompactionFunctionSamples`) with them**: `CompactionFunction` names both
  (`Datastore/SQL/ObjectFactories/CompactionFunction.py:44`,
  `Datastore/SQL/ObjectFactories/CompactionFunction.py:51`);
- **`inflaton-trajectory` reaches every sharded family**: `FullInstanton`, `SlowRollInstanton`,
  `GradientCoupledInstanton` and `CompactionFunction` name `InflatonTrajectory`
  (`Datastore/SQL/ObjectFactories/FullInstanton.py:37`,
  `Datastore/SQL/ObjectFactories/SlowRollInstanton.py:36`,
  `Datastore/SQL/ObjectFactories/GradientCoupledInstanton.py:36`,
  `Datastore/SQL/ObjectFactories/CompactionFunction.py:37`). It also drops a **replicated**
  table, which is the inherited issue
  `[00-a-drop-action-drops-a-replicated-table-outside-the-in-flight-record]` (DatastoreKit's
  `docs/OPEN_ISSUES.md` §1.2).

`redshift` is registered (`Datastore/SQL/Datastore.py:99`) but is in neither list.

**15 `object_get_vectorized` calls pass a bare `delta_Nstar`**: `main.py` 10 (`main.py:224`,
`main.py:252`, `main.py:319`, `main.py:448`, `main.py:592`, `main.py:874`, `main.py:903`,
`main.py:967`, `main.py:1018`, `main.py:1044`), `plot_InstantonSolutions.py` 3
(`plot_InstantonSolutions.py:697`, `:700`, `:733`), `plotting/fetch.py` 2 (`plotting/fetch.py:127`,
`:166`). SI's layer accepts the bare key (item 4); the package wants a mapping from the field to the
key, here `{"delta_Nstar": key}` (`datastorekit/SQL/ShardedPool.py:3299-3307`), and adds it to each
payload dict in place (`datastorekit/SQL/ShardedPool.py:3309-3310`;
`[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]`).
`plot_InstantonSolutions.py:697-702` passes one `payload_data` list to two calls. Four test stubs
mirror the signature (`tests/test_plot_adapters_golden.py:1010`,
`tests/test_plot_extraction_golden.py:381`, `:450`, `:477`).

**`pool.inventory`**: `main.py:1256`, `main.py:1266`, `main.py:1278`, `main.py:1288`, and
`tests/test_grid_builder_integration.py:133-135`. The same two routes as CPBH's
(`docs/adoption/champbh.md` item 6): port to `inventory_spec` and `read_inventory`, or keep a
reader of SI's own. The choice is SI's.

**The version label.** `main.py` opens under `"2026.6.1"` (`main.py:49`); the two plot scripts
import `VERSION_LABEL = "2026.3.0"` from `plotting/provenance.py:18`
(`plot_GradientCoupledSolutions.py:98`, `plot_InstantonSolutions.py:70`). The plot scripts open
**read-write** (no `read_only=`). Under the package a read-write open under a label the store lacks
writes a version row for it (`datastorekit/SQL/ShardedPool.py:348-354`); a read-only open under such
a label is refused with `ReadOnlyMiss` (`datastorekit/SQL/ShardedPool.py:531-534`). This is SI's to
settle, not the package's.

**The unchanged calls**, by count of calls on a pool (an `ast` count in 07a's scratchpad, tests
included): `object_get` 115, `object_store` 42, `object_validate` 40. Their signatures are the
package's.

## 7. Its tests and fixtures

- **None tests the layer itself, so none is deleted.**
- `tests/conftest.py`'s `live_pool` (`tests/conftest.py:36-74`) is rewritten: its `ShardedPool(...)`
  is item 6's, and it imports `ShardedPool` from the layer (`tests/conftest.py:25`).
- **57 test functions in 11 files reach `live_pool`**, directly or through the fixtures that request
  it (`dense_record`, `scalars_only_record`, `single_value_record`, `stability_records`); two of
  them are parametrized three ways, so 61 are collected. The 11 files are
  `tests/test_alpha_regularization.py` (3), `tests/test_gci_parity_cheap_fetch.py` (1),
  `tests/test_gci_parity_persistence_roundtrip.py` (1), `tests/test_gci_profile_only_fetch_contract.py`
  (13), `tests/test_gradient_coupled_instanton_end_to_end.py` (6),
  `tests/test_grid_builder_integration.py` (3), `tests/test_n_collocation_points.py` (2),
  `tests/test_pipeline.py` (1), `tests/test_plot_stability_figures.py` (5),
  `tests/test_scalars_only_compaction_function.py` (8), `tests/test_scalars_only_storage.py` (14).
  They need Ray and are `integration`-marked.

## 8. Which of its stores the package refuses, and why

**U31: SI's stores are rebuilt, not migrated, as D4.** Every SI store is refused, in the same order
as CPBH's (`docs/adoption/champbh.md` item 8; read from the package's code, **no store opened**):
read-write, first `StoreSchemaMismatch` (the primary lacks `replication_in_flight`; `git grep
replication_in_flight 7bb3efd` finds nothing), then the absolute shard record (SI records
`str(db_name)` of a resolved primary, `Datastore/SQL/ShardedPool.py:88`,
`Datastore/SQL/ShardedPool.py:296`), then `ReplicatedDivergence` on `timestamp` (SI's actor stamps
each insert, `Datastore/SQL/Datastore.py:652`); read-only, the absolute record first. Two additions:
- **Serial splits.** SI recorded one: in `SMSR_scaling_values.sqlite`, `MasslessDecoupledDiffusion`
  had serials 1, 6, 11, … across ten shards (`.claude/rules/datastore-factories.md:263-272`). A
  replicated class whose shards hold one object under different serials differs at the check at
  open.
- **Column changes since a store was written**, which make a shard differ from the declared tables
  (`StoreSchemaMismatch`). The factory commits after 2026-06-21 that add or change `sqla.Column`
  lines: `5b62de5` (2026-06-23, noise statistics), `ade2fcf` (2026-06-23, `DiffusionModel`
  persisted), `2907de0` and `8c35add` (2026-06-23, compaction radii and renames), `1b8249b`
  (2026-06-24, compaction flags), `9490eb6` and `c3e1d07` (2026-07-06, `n_collocation_points`,
  `alpha_regularization`, `GradientCoupledInstanton`'s three tables), `f63a5cf` (2026-07-06, noise
  columns renamed), `9f4741f` (2026-07-09, GCI parity scalar columns).

**The stores, by path only:**
- in the working tree (ignored): `out-gci-convergence-campaign/phase_a.sqlite` with its two shards,
  `out-gci-convergence-campaign/phase_a_followup.sqlite` with one, and `test-gradient.sqlite` with
  `test-gradient-profile.sqlite` and ten shards;
- in SI's notes: `phase_a` (`.documents/gradient-coupled-instanton/24-campaign-closeout.md:69-72`),
  `SMSR_scaling.sqlite` and `SMSR_scaling_values.sqlite` (`.documents/grid-sampling/handoff-goal2.md:140-141`),
  `large-grid-1500.sqlite` (`.documents/grid-sampling/handoff-large-grid.md:269`),
  `doe-run-500.sqlite` (`.documents/grid-sampling/handoff-sparse-sampling.md:292`), and
  `quad-ast-small-full.sqlite`, `quad-ast-small-novalues.sqlite`
  (`.prompts/sparse-sampling/10-provenance-footer.md:147-148`).

**Advice (U31):**
- SI adopts at the start of its **P2 campaign**, which re-runs the June grids: every `S_MSR`-bearing
  June or July number is provisional (`[june-smsr-results-provisional]`,
  `.documents/OPEN-ISSUES.md:93`, "P2, re-run").
- **Before adopting, SI tags its last commit on the old layer**, so that the stores it keeps stay
  readable from that tag's checkout and venv. The closeout keeps the **July** `phase_a` stores
  "as the primary evidence for the results table" (`.documents/gradient-coupled-instanton/24-campaign-closeout.md:69-72`;
  written at SI `b5a3a9f`, 2026-07-08).
- `[hfp-closed-form-audit-not-run]`, the zero-compute check planned on the stored grids
  (`.documents/OPEN-ISSUES.md:92`, "P2, first prompt"), reads the old stores, so it runs on that tag
  or before adoption.

**Rebuild costs, as SI records them.** SI records per-point wall-clock times, not whole-grid
rebuild costs: for example 3603.5 s and 7224.9 s for one Phase A point under 3600 s and 7200 s
budgets (`.documents/gradient-coupled-instanton/24-phase-a-deep-dive.md:39-40`), and ~0.3–0.5 s for
a seeded `FullInstanton` solve
(`.documents/gradient-coupled-instanton/22c-fullinstanton-seed-fixed-target.md:92`). The ignored
`full_instanton_compute_times.csv` and `slow_roll_instanton_compute_times.csv` were named, not read.

## 9. Its acceptance (G4)

G4 holds when SI has adopted `v0.2.0`, when it is next active:
1. its 9 layer files are deleted, and it imports `datastorekit` at the pinned tag;
2. **its non-integration and integration suites pass** (`CLAUDE.md:21`; the integration tests need
   Ray, item 7);
3. **a small grid is rebuilt through the package.** What it is compared against is SI's choice.

## 10. What goes stale in it

- **`CLAUDE.md:89-112`**: the layer's files on the protected list leave SI. A change to them is made
  in DatastoreKit and reaches SI through its pin; the rest of the list stays SI's.
- **`.claude/rules/pool-read-apis.md:8-15`**: `pool.inventory()` does not exist in the package
  (item 6).
- **`.claude/rules/datastore-factories.md:245-301`**: its account of replication (a random
  controlling shard; the serial passed to the other shards; `_new_insert` and `_deserialized`). The
  package's replicated write is recorded and checked at open, and it reads `_new_insert` or
  `_updated`, not `_deserialized` (`datastorekit/SQL/ShardedPool.py:3169`).
- **`.claude/memory/bug-assign-shard-keys-key-id.md:24`**: "Fixed 2026-06-20:
  `Datastore/SQL/ShardedPool.py` line 819", a file that leaves SI.
- **`shard-key-assignment-bug.md`**: the package carries the fix in `_assign_shard_keys`, with both
  of SI's commits present: `3f1caad`'s `key_serial` (`datastorekit/SQL/ShardedPool.py:3572`) and
  `20d9a61`'s de-duplication (`datastorekit/SQL/ShardedPool.py:3524`).

---

## Appendix: the script's output

Made by, from DatastoreKit's repository root:

```bash
./venv/bin/python docs/extraction/measure_client_imports.py si
```

# Imports of the layer: StochasticInstantons (SI) at `7bb3efd`

Written by `docs/extraction/measure_client_imports.py`, reading through `git ls-tree` and `git show` only.

- **Repository:** `/Users/ds283/Documents/Code/StochasticInstantons`
- **Commit:** `7bb3efd0d0a9cc1c367b7848e27fa8b548a76bf7` (given as `7bb3efd`), 2026-10-09 Record the R1 calculation review and open its issues board
- **Layer files** (9): `Datastore/__init__.py`, `Datastore/object.py`, `Datastore/SQL/__init__.py`, `Datastore/SQL/ClientPool.py`, `Datastore/SQL/Datastore.py`, `Datastore/SQL/ProfileAgent.py`, `Datastore/SQL/SerialPoolBroker.py`, `Datastore/SQL/ShardedPool.py`, `Datastore/SQL/ObjectFactories/base.py`
- **Layer files absent at this commit:** none
- **Factory package:** `Datastore/SQL/ObjectFactories/` (its `base.py` is the layer's)
- **Files read:** 186 tracked `.py` files outside the layer; 0 do not parse

## Totals

| What | Count |
|---|---|
| Import statements naming a layer module | **48** in 47 files |
| of which nested (not at module level) | 1 |
| String literals naming a layer module | 0 (0 exactly its name) |
| `import_module` / `__import__` calls naming a layer module | 0 |
| Import statements naming a factory module (not layer imports) | 2 (2 outside `Datastore/SQL/ObjectFactories/`) |

## Layer imports, by group

| Group | Statements | Nested | Files |
|---|---|---|---|
| `(top level)` | 4 | 0 | 3 |
| `ComputeTargets/` | 5 | 0 | 5 |
| `CosmologyConcepts/` | 5 | 0 | 5 |
| `CosmologyModels/` | 1 | 0 | 1 |
| `Datastore/SQL/ObjectFactories/` | 22 | 0 | 22 |
| `InflationConcepts/` | 5 | 1 | 5 |
| `MetadataConcepts/` | 3 | 0 | 3 |
| `Quadrature/` | 1 | 0 | 1 |
| `RayTools/` | 1 | 0 | 1 |
| `tests/` | 1 | 0 | 1 |
| **total** | **48** | **1** | **47** |

## Layer imports, by module

A statement naming two layer modules is counted under each.

| Module | Statements | Names imported by `from` (statements) |
|---|---|---|
| `Datastore` | 12 | `DatastoreObject` 12 |
| `Datastore.SQL.ObjectFactories.base` | 24 | `SQLAFactoryBase` 24 |
| `Datastore.SQL.ProfileAgent` | 1 | `ProfileAgent` 1 |
| `Datastore.SQL.ShardedPool` | 5 | `ShardedPool` 5 |
| `Datastore.object` | 6 | `DatastoreObject` 6 |

## Every layer import

### `(top level)` (4)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `main.py:36` | — | `Datastore.SQL.ProfileAgent` | `ProfileAgent` |
| `main.py:37` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `plot_GradientCoupledSolutions.py:61` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `plot_InstantonSolutions.py:42` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |

### `ComputeTargets/` (5)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `ComputeTargets/CompactionFunction.py:25` | — | `Datastore.object` | `DatastoreObject` |
| `ComputeTargets/FullInstanton.py:23` | — | `Datastore.object` | `DatastoreObject` |
| `ComputeTargets/GradientCoupledInstanton/GradientCoupledInstanton.py:75` | — | `Datastore.object` | `DatastoreObject` |
| `ComputeTargets/InflatonTrajectory.py:24` | — | `Datastore.object` | `DatastoreObject` |
| `ComputeTargets/SlowRollInstanton.py:23` | — | `Datastore.object` | `DatastoreObject` |

### `CosmologyConcepts/` (5)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `CosmologyConcepts/DimensionfulQuantity.py:20` | — | `Datastore` | `DatastoreObject` |
| `CosmologyConcepts/DimensionlessQuantity.py:20` | — | `Datastore` | `DatastoreObject` |
| `CosmologyConcepts/Potentials/AbstractPotential.py:6` | — | `Datastore` | `DatastoreObject` |
| `CosmologyConcepts/Potentials/registry.py:5` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `CosmologyConcepts/redshift.py:19` | — | `Datastore` | `DatastoreObject` |

### `CosmologyModels/` (1)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `CosmologyModels/cosmo_params.py:19` | — | `Datastore.object` | `DatastoreObject` |

### `Datastore/SQL/ObjectFactories/` (22)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `Datastore/SQL/ObjectFactories/CompactionFunction.py:21` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/CosmologicalParams.py:18` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/DimensionfulQuantity.py:20` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/DimensionlessQuantity.py:21` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/FullInstanton.py:21` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/GradientCoupledInstanton.py:20` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/InflatonTrajectory.py:20` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/MasslessDecoupledDiffusion.py:3` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/N_final.py:7` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/N_init.py:7` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/QuadraticPotential.py:8` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/QuarticPotential.py:8` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/SlowRollInstanton.py:20` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/alpha_regularization.py:22` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/delta_Nstar.py:7` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/efold.py:7` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/integration_metadata.py:18` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/n_collocation_points.py:21` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/redshift.py:20` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/store_tag.py:18` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/tolerance.py:20` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/version.py:18` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |

### `InflationConcepts/` (5)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `InflationConcepts/DiffusionModel/__init__.py:6` | — | `Datastore` | `DatastoreObject` |
| `InflationConcepts/DiffusionModel/registry.py:5` | if TYPE_CHECKING | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `InflationConcepts/alpha_regularization.py:20` | — | `Datastore` | `DatastoreObject` |
| `InflationConcepts/efold_value.py:5` | — | `Datastore` | `DatastoreObject` |
| `InflationConcepts/n_collocation_points.py:22` | — | `Datastore` | `DatastoreObject` |

### `MetadataConcepts/` (3)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `MetadataConcepts/store_tag.py:16` | — | `Datastore` | `DatastoreObject` |
| `MetadataConcepts/tolerance.py:20` | — | `Datastore` | `DatastoreObject` |
| `MetadataConcepts/version.py:16` | — | `Datastore` | `DatastoreObject` |

### `Quadrature/` (1)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `Quadrature/integration_metadata.py:18` | — | `Datastore` | `DatastoreObject` |

### `RayTools/` (1)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `RayTools/RayWorkPool.py:23` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |

### `tests/` (1)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `tests/conftest.py:25` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |

## String literals naming a layer module

None.

## `import_module` calls naming a layer module

None.

## Imports of factory modules, by group (count only)

| Group | Statements |
|---|---|
| `CosmologyConcepts/` | 2 |
| **total** | **2** |

## Files that do not parse

None.
