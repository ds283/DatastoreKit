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

*Added by extraction prompt 10 on 2026-10-10: the section
[Addendum: v0.2.1](#addendum-v021-extraction-prompt-10-2026-10-10), after item 10, gives the pin
**`v0.2.1`** and what changed for SI since `v0.2.0`, and supersedes the statements it names.
07a's text is unchanged and true of `v0.2.0`.*

*Added by `actor-names` prompt 02 on 2026-10-11: the section
[Addendum: v0.2.2](#addendum-v022-actor-names-prompt-02-2026-10-11), after the `v0.2.1` addendum,
gives the pin **`v0.2.2`** and what changed for SI since `v0.2.1`, and supersedes the statements
it names. The text before it, the `v0.2.1` addendum included, is unchanged and true of the
release it names.*

*Added by `factory-defaults` prompt 02 on 2026-10-11: the section
[Addendum: v0.2.3](#addendum-v023-factory-defaults-prompt-02-2026-10-11), after the `v0.2.2`
addendum, gives the pin **`v0.2.3`** and what changed for SI since `v0.2.2`, and supersedes the
statements it names. The text before it, the `v0.2.1` and `v0.2.2` addenda included, is unchanged
and true of the release each names.*

*Added by `object-timestamp` prompt 02 on 2026-10-12: the section
[Addendum: v0.3.0](#addendum-v030-object-timestamp-prompt-02-2026-10-12), after the `v0.2.3`
addendum, gives the pin **`v0.3.0`** and what changed for SI since `v0.2.3`, and supersedes the
statements it names. The text before it, the `v0.2.1`, `v0.2.2` and `v0.2.3` addenda included, is
unchanged and true of the release each names.*

*Added by `fingerprint` prompt 02 on 2026-10-14: the section
[Addendum: v0.4.0](#addendum-v040-fingerprint-prompt-02-2026-10-14), after the `v0.3.0`
addendum, gives SI's pin, `v0.3.0` or `v0.4.0` as SI chooses, and what changed for SI since
`v0.3.0`, and supersedes the statements it names. The text before it, the four earlier addenda
included, is unchanged and true of the release each names.*

*Added by `extra-values` prompt 02 on 2026-10-21: the section
[Addendum: v0.5.0](#addendum-v050-extra-values-prompt-02-2026-10-21), after the `v0.4.0`
addendum, gives SI's pin, `v0.5.0`, and what SI declares to adopt it, what then holds and what of
SI's own code and tests moves. It supersedes the statements it names. The text before it, the
five earlier addenda included, is unchanged and true of the release each names.*

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

## Addendum: v0.2.1 (extraction prompt 10, 2026-10-10)

*Written by extraction prompt 10 on 2026-10-10, and added to 07a's text, which stays as written
and true of `v0.2.0` (`CLAUDE.md` rule 6). SI was not re-measured (decision U37); what this section
says of SI comes from 07a's measurements, log 08a §3 and the `KeyError` measure below.*

**The pin.** SI adopts **`v0.2.1`** in place of `v0.2.0`, when it is next active (decision U37),
and G4 reads "SI has adopted `v0.2.1`":

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.1
```

**What changed for SI since `v0.2.0`.** The three changes are
[`docs/client-contract.md` §9](../client-contract.md#9-changes-after-v020)'s rows, and
[`README.md`'s addendum](README.md#addendum-v021-extraction-prompt-10-2026-10-10) gives them for
every client. Nothing SI supplies changes, so items 1–10 stand as written but for the statements
below.
- **The vectorized get.** The refusal of a bare `delta_Nstar` (item 6) is unchanged, and SI still
  converts its 15 calls to the mapping form, `{"delta_Nstar": key}`. At `v0.2.1`
  `object_get_vectorized` is `datastorekit/SQL/ShardedPool.py:3327-3351`: its membership test is
  `:3339` and the payload line `:3348`, so a bare key is refused before the payload line, as at
  `v0.2.0`. Once SI has converted, the package sends each shard copies of the payloads,
  `{**value, **shard_key}`, and SI's dicts are left as they were passed. **The in-place hazard is
  gone.** `plot_InstantonSolutions.py:697-702`, which passes one `payload_data` list to two calls,
  is safe under `v0.2.1`: each call merges its own key into copies (log 08a §3).
- **The `KeyError`.** A reopen whose primary records a sharded table that `sharded_tables` lacks is
  refused with the intended `RuntimeError`, not a bare `KeyError`
  (`datastorekit/SQL/ShardedPool.py:1071-1072`, `:1100-1103`), and SI's code does not depend on
  the `KeyError`: measured through `git grep` at `7bb3efd`, SI catches `KeyError` nowhere, and has no
  `try` within three lines before a `ShardedPool(` outside its layer.
- **The refused open.** An open that raises closes the actors it built and disposes the pool's
  engine (`datastorekit/SQL/ShardedPool.py:203-207`, `:375-408`): a client that retries refused
  opens no longer holds a file descriptor per refused engine until the collector runs.

**Line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, read at that tag
(`240028e`). A `datastorekit/` line in this addendum is `v0.2.1`'s, whose `datastorekit/` is the
tree of extraction prompt 09's commit `cad7bc1`.

**What this addendum supersedes**, in this file. Each `path:line` is this file's as committed with
this addendum. In 07a's file (`dd45243`) every line after `:13` is five lines earlier, since the
italic line under the title adds five.

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/stochasticinstantons.md:5` | the package at **`v0.2.0`** | at `v0.2.1`, with this addendum |
| `docs/adoption/stochasticinstantons.md:20-21` | a `datastorekit/` line is the package's at `v0.2.0` | still so for 07a's text; a `datastorekit/` line in this addendum is at `v0.2.1` |
| `docs/adoption/stochasticinstantons.md:260-262` | the package "adds it to each payload dict in place" | `v0.2.1` sends copies, and leaves SI's dicts as passed; "The vectorized get", above |
| `docs/adoption/stochasticinstantons.md:353` | G4 holds when SI has adopted `v0.2.0` | G4 holds when SI has adopted `v0.2.1` (U37) |

---

## Addendum: v0.2.2 (actor-names prompt 02, 2026-10-11)

*Written by `actor-names` prompt 02 on 2026-10-11, and added after extraction prompt 10's `v0.2.1`
addendum. 07a's text and the `v0.2.1` addendum stay as written, each true of the release it names
(`CLAUDE.md` rule 6). SI was not re-measured (as decision U37); what this section says of SI comes
from 07a's measurements and from reads through `git` only, at `7bb3efd`.*

**The pin.** SI adopts **`v0.2.2`** in place of `v0.2.1`, when it is next active (decision U3 of
the `actor-names` campaign, which amends extraction decision U37), and G4 reads "SI has adopted
`v0.2.2`":

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.2
```

**What changed for SI since `v0.2.1`.** The changes are the rows of
[`docs/client-contract.md` §9.3](../client-contract.md#93-actor-names-prompt-01) and
[§9.4](../client-contract.md#94-actor-names-prompt-01b), and
[`README.md`'s addendum](README.md#addendum-v022-actor-names-prompt-02-2026-10-11) gives them for
every client: a closed pool, and an open that is refused, release their actors' names at once; a
closed pool's handles are dead; a second `__exit__` does nothing. Two pools open at once still
collide, and closing a pool never starts Ray. Nothing SI supplies changes, so items 1–10 stand as
the `v0.2.1` addendum leaves them.
- **Item 6's constructions.** SI constructs the pool 4 times (item 6): `main.py:1345`,
  `plot_GradientCoupledSolutions.py:974`, `plot_InstantonSolutions.py:1207` and
  `tests/conftest.py:57`. Read by an `ast` read of `git show`, each is a `with ShardedPool(…) as
  pool:` block and the only construction in its file, and nothing after it names `pool`. The first
  three are the last statement of their block.
- **The `live_pool` fixture** (`tests/conftest.py:36-74`, session-scoped, `:36`) yields the pool
  inside its block (`:72`), and calls `ray.shutdown()` after the block (`:74`). So the pool is
  closed, and under `v0.2.2` its actors are killed, before Ray is shut down, and nothing uses the
  pool after its block. It opens one pool per pytest session.
- **No other use.** SI calls no pool's `__exit__` directly: the one `super().__exit__` call `git
  grep` finds, `Quadrature/simple_quadrature.py:60`, is not a pool. It calls neither `ray.kill` nor
  `ray.get_actor`, and reads no pool's `_shards` or `_broker`. So SI uses no closed pool and meets
  no dead handle, and since each script opens one pool per process it never met the defect either.
  **For SI the fix is latent.**

**Line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, read at that tag
(`240028e`), and one in the `v0.2.1` addendum stays `v0.2.1`'s (`33778b0`). This addendum cites no
`datastorekit/` line; one cited here would be `v0.2.2`'s, whose `datastorekit/` is the tree of
`actor-names` prompt 01b's commit `f024fc6`.

**What this addendum supersedes**, in this file. Each `path:line` is this file's as committed with
this addendum. In the file as extraction prompt 10 left it (`33778b0`), every line after `:19` is
six lines earlier, since this addendum's italic line under the title adds six: so the `v0.2.1`
addendum's citations, which are that file's, are read at `33778b0`, or six lines later here (all
but `:5`, which is above the insert).

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/stochasticinstantons.md:15-18` | the `v0.2.1` addendum gives the pin **`v0.2.1`** | it gives `v0.2.1`'s pin and changes, true of `v0.2.1`; this addendum gives `v0.2.2` |
| `docs/adoption/stochasticinstantons.md:389-390` | "SI adopts **`v0.2.1`** in place of `v0.2.0`", and G4 reads "SI has adopted `v0.2.1`" | SI adopts `v0.2.2` in place of `v0.2.1` (`actor-names` U3), and G4 reads "SI has adopted `v0.2.2`" |
| `docs/adoption/stochasticinstantons.md:393` | the pin `…@v0.2.1` | the pin `…@v0.2.2`, above |
| `docs/adoption/stochasticinstantons.md:422-424` | the `v0.2.1` addendum's `path:line`s are "this file's as committed with this addendum" | they are read at `33778b0`, or six lines later here (all but `:5`) |
| `docs/adoption/stochasticinstantons.md:428` | the package "at `v0.2.1`, with this addendum" | at `v0.2.2`, with both addenda |
| `docs/adoption/stochasticinstantons.md:431` | "G4 holds when SI has adopted `v0.2.1` (U37)" | G4 holds when SI has adopted `v0.2.2` (U37; `actor-names` U3) |

---

## Addendum: v0.2.3 (factory-defaults prompt 02, 2026-10-11)

*Written by `factory-defaults` prompt 02 on 2026-10-11, and added after `actor-names` prompt 02's
`v0.2.2` addendum. 07a's text, the `v0.2.1` addendum and the `v0.2.2` addendum stay as written,
each true of the release it names (`CLAUDE.md` rule 6). SI was not re-measured (as decision U37);
what this section says of SI comes from 07a's measurements and from reads through `git` only, at
`7bb3efd`.*

**The pin.** SI adopts **`v0.2.3`** in place of `v0.2.2`, when it is next active (decision U5 of
the `factory-defaults` campaign, which keeps extraction decision U37 and `actor-names` decision U3
for SI), and G4 reads "SI has adopted `v0.2.3`":

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.3
```

`v0.2.3` carries `key_on_version`, `v0.2.0`'s feature, `v0.2.1`'s three fixes and `v0.2.2`'s fix,
unchanged.

**What changed for SI since `v0.2.2`.** The change is
[`docs/client-contract.md` §9.5](../client-contract.md#95-factory-defaults-prompt-01)'s, and
[`README.md`'s addendum](README.md#addendum-v023-factory-defaults-prompt-02-2026-10-11) gives it for
every client: `SQLAFactoryBase` keeps `register` and `build` abstract and defaults `store`,
`validate` and `validate_on_startup`, so a factory class that defines the two can be instantiated
and its instance registered. Nothing SI supplies changes, nothing the layer writes changes, and no
message, refusal or exception of the layer's. **For SI it removes item 5's U32 obligation, and
item 3's `TypeError` at import.**
- **SI's registry of instances works as it stands.** Read by an `ast` read of every `.py` file
  through `git show` at `7bb3efd`: 28 classes whose bases name `SQLAFactoryBase`, 16 of them
  lacking one of `store`, `validate` and `validate_on_startup`, and none lacking `register` or
  `build`; 33 calls of them by name, 21 of them of a class lacking one of the three. Of those 21,
  18 are registry entries (`Datastore/SQL/Datastore.py:97-126`), and under `v0.2.3` each
  instantiates, since every class defines `register` and `build`.
- **The three instantiations at import** of item 3, `CosmologyConcepts/Potentials/registry.py:33`
  and `:40` (`sqla_QuadraticPotential_factory()`, `sqla_QuarticPotential_factory()`) and
  `Datastore/SQL/ObjectFactories/MasslessDecoupledDiffusion.py:71`
  (`sqla_MasslessDecoupledDiffusion_factory()`), stop raising too: under `v0.2.3` each
  instantiates as it stands.
- **So item 5 asks nothing of the 16 classes** but the base's import path (item 3), and neither of
  the two routes is needed; the seven of them on SI's protected list need no change for U32. The
  defaults are static: a hook an SI class defines with `self` overrides the base's default as
  before, and one it does not define raises a bare `NotImplementedError` when the layer calls it,
  as SI's own base does today (`Datastore/SQL/ObjectFactories/base.py:16-30` at `7bb3efd`).
  Contract §9.5's third row says what a registered instance must be under Ray: of a class defined
  at module level, with picklable attributes.
- **Item 5's other findings are unchanged:** `InflatonTrajectory.validate_on_startup` names its
  parameter `prune_unvalidated`, where the pool calls a replicated class's hook by keyword,
  `prune`; and `InflatonTrajectory` is a replicated, validated class, repaired after an interrupted
  validate only if it declares `validated_column` and defines `revalidate`. Both choices stay SI's.
  So do items 6 and 8: every SI store is refused at open, and is rebuilt (U31).

**Line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, read at that tag
(`240028e`), and one in the `v0.2.1` addendum stays `v0.2.1`'s (`33778b0`). The `v0.2.2` addendum
cites none. This addendum cites no `datastorekit/` line; one cited here would be `v0.2.3`'s, whose
`datastorekit/` is the tree of `factory-defaults` prompt 01's commit `f5d8957`.

**What this addendum supersedes**, in this file. Each `path:line` is this file's as committed with
this addendum. In the file as `actor-names` prompt 02 left it (`6d8ee9a`), every line after `:25`
is six lines earlier, since this addendum's italic line under the title adds six. So the `v0.2.2`
addendum's citations, which are that file's, are read at `6d8ee9a`, or six lines later here (all
but `:15-18`, which is above the insert). The `v0.2.1` addendum's citations, which the `v0.2.2`
addendum reads at `33778b0` or six lines later, are read at `33778b0`, or twelve lines later here
(all but `:5`).

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/stochasticinstantons.md:20-24` | the `v0.2.2` addendum gives the pin **`v0.2.2`** | it gives `v0.2.2`'s pin and changes, true of `v0.2.2`; this addendum gives `v0.2.3` |
| `docs/adoption/stochasticinstantons.md:36-37` | SI "registers factory instances (16 classes lack three of the five abstract hooks, U32)" | the count holds; at `v0.2.3` the base's only abstract hooks are `register` and `build`, which all 28 classes define, so SI's instances are accepted; "What changed for SI since `v0.2.2`", above |
| `docs/adoption/stochasticinstantons.md:131-132` | the three import-time sites: "under the package's ABC each raises `TypeError` at import" | true through `v0.2.2`; under `v0.2.3` each instantiates. The rest of the paragraph (`:127-131`), the sites themselves, still holds |
| `docs/adoption/stochasticinstantons.md:198-206` | the package's base "is" an ABC (`datastorekit/SQL/factory_base.py:5-29`), "so each raises `TypeError` at instantiation: in the registry, and at the three import-time sites of item 3", and the two routes, "The choice is SI's" | true through `v0.2.2`. At `v0.2.3` each instantiates, and neither route is needed. The rest of item 5's U32 paragraph (`:193-198`), the counts and SI's own base, still holds |
| `docs/adoption/stochasticinstantons.md:448-450` | "SI adopts **`v0.2.2`** in place of `v0.2.1`, when it is next active", and G4 reads "SI has adopted `v0.2.2`" | SI adopts `v0.2.3` in place of `v0.2.2`, when it is next active (`factory-defaults` U5), and G4 reads "SI has adopted `v0.2.3`" |
| `docs/adoption/stochasticinstantons.md:453` | the pin `…@v0.2.2` | the pin `…@v0.2.3`, above |
| `docs/adoption/stochasticinstantons.md:484-488` | the `v0.2.2` addendum's `path:line`s are "this file's as committed with this addendum" | they are read at `6d8ee9a`, or six lines later here (all but `:15-18`) |
| `docs/adoption/stochasticinstantons.md:493` | in the `v0.2.2` addendum's table, SI adopts `v0.2.2` in place of `v0.2.1`, and G4 reads "SI has adopted `v0.2.2`" | as `:448-450` |
| `docs/adoption/stochasticinstantons.md:494` | "the pin `…@v0.2.2`, above" | the pin `…@v0.2.3`, above |
| `docs/adoption/stochasticinstantons.md:496` | the package "at `v0.2.2`, with both addenda" | at `v0.2.3`, with the three addenda |
| `docs/adoption/stochasticinstantons.md:497` | "G4 holds when SI has adopted `v0.2.2` (U37; `actor-names` U3)" | G4 holds when SI has adopted `v0.2.3` (U37; `actor-names` U3; `factory-defaults` U5) |

---

## Addendum: v0.3.0 (object-timestamp prompt 02, 2026-10-12)

*Written by `object-timestamp` prompt 02 on 2026-10-12, and added after `factory-defaults` prompt
02's `v0.2.3` addendum. 07a's text and the `v0.2.1`, `v0.2.2` and `v0.2.3` addenda stay as written,
each true of the release it names (`CLAUDE.md` rule 6). SI was not re-measured (as decision U37);
what this section says of SI comes from 07a's measurements and from reads through `git` only, at
`7bb3efd`.*

**The pin.** SI adopts **`v0.3.0`** in place of `v0.2.3`, when it is next active (decision U6 of
the `object-timestamp` campaign, which amends `factory-defaults` decision U5 for SI), and G4 reads
"SI has adopted `v0.3.0`":

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.3.0
```

`v0.3.0` carries `key_on_version`, `v0.2.0`'s feature, `v0.2.1`'s three fixes, `v0.2.2`'s fix and
`v0.2.3`'s change, unchanged.

**What changed for SI since `v0.2.3`.** The change is
[`docs/client-contract.md` §9.6](../client-contract.md#96-object-timestamp-prompt-01)'s, and
[`README.md`'s addendum](README.md#addendum-v030-object-timestamp-prompt-02-2026-10-12) gives it for
every client: the package's `DatastoreObject` takes an optional, keyword-only `timestamp`
(`datastorekit/object.py:10-14`) and exposes it as a read-only property (`:27-38`), as SI's own
does (`Datastore/object.py:25-30`, `:43-45`) but for the keyword. The layer never sets it and never
reads it. Nothing SI supplies changes, nothing the layer writes or reads changes, and no message,
refusal or exception of the layer's. **For SI it removes item 2's `DatastoreObject.timestamp`
obligation, and item 4's line.**
- **SI's 24 sites work as they stand once their import is rewritten** (item 3). Read by an `ast`
  read of every `.py` file through `git show` at `7bb3efd`, outside `prompts/`, `.prompts/`,
  `docs/` and `.documents/`: 34 classes descend from SI's `DatastoreObject`; of the 23 calls
  `DatastoreObject.__init__(…)`, 9 pass `store_id` alone and 14 pass `timestamp=` by keyword (item
  2's list), and none passes anything else; and the ten pass-throughs of item 2 each pass
  `timestamp=` by keyword. Under `v0.3.0` each is accepted as it stands. A `timestamp` passed
  positionally would be refused with `TypeError`; SI passes none so.
- **Its reads of `.timestamp` get what its factories pass**, as today: the three direct reads
  (`plotting/adapters/full.py:61`, `plotting/adapters/gradient.py:133`,
  `plotting/adapters/slow_roll.py:66`) and the two by `getattr` (`plotting/provenance.py:41`,
  `plotting/figures/spatial.py:259`). 18 of SI's factory modules pass `timestamp=`; the layer fills
  nothing, so they go on passing it.
- **Its plot adapters and test stand-ins are not `DatastoreObject`s**, and are unaffected: `def
  timestamp` on four adapters (`plotting/adapters/base.py:84`, `plotting/adapters/full.py:60`,
  `plotting/adapters/gradient.py:132`, `plotting/adapters/slow_roll.py:65`) and on one test
  stand-in (`tests/test_plot_adapters_golden.py:870`), and `self.timestamp = …` at twelve sites in
  test stand-ins (for example `tests/test_plot_adapters_golden.py:141`), none on a class descending
  from `DatastoreObject`. No descendant defines or assigns `timestamp`; one that did would now raise
  `AttributeError`.
- **So item 2's `DatastoreObject.timestamp` paragraph asks nothing of SI**, and
  `DatastoreObject.timestamp` does not leave the layer (item 4): the package's object carries it.
  SI's own `Datastore/object.py` is deleted with its layer (item 2). The rest of items 2 and 4 is
  unchanged, `base._timestamp_column` included, and so are items 5, 6 and 8: every SI store is
  refused at open, and is rebuilt (U31).
- **One key more in `vars()`**: `_timestamp`, as SI's own `DatastoreObject` has today
  (`Datastore/object.py:30`). No SI `.py` file calls `vars(` or reads a `__dict__`.

**Line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, read at that tag
(`240028e`), and one in the `v0.2.1` addendum stays `v0.2.1`'s (`33778b0`). The `v0.2.2` and
`v0.2.3` addenda cite none. A `datastorekit/` line in this addendum is `v0.3.0`'s, whose
`datastorekit/` is the tree of `object-timestamp` prompt 01's commit `1b2f91a`; prompt 02 does not
change it. An SI line is SI's at `7bb3efd`.

**What this addendum supersedes**, in this file. Each `path:line` below is this file's as committed
with this addendum. In the file as `factory-defaults` prompt 02 left it (`0de2b16`), every line after
`:31` is six lines earlier, since this addendum's italic line under the title adds six (N = 6). So:
- the `v0.2.3` addendum's citations, which are that file's, are read at `0de2b16`, or **6** lines
  later here (all but `:20-24`, which is above the insert);
- the `v0.2.2` addendum's, which the `v0.2.3` addendum reads at `6d8ee9a` or six lines later, are
  read at `6d8ee9a`, or **12** lines later here (all but `:15-18`);
- the `v0.2.1` addendum's, which the `v0.2.3` addendum reads at `33778b0` or twelve lines later, are
  read at `33778b0`, or **18** lines later here (all but `:5`).

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/stochasticinstantons.md:26-30` | the `v0.2.3` addendum gives the pin **`v0.2.3`** | it gives `v0.2.3`'s pin and changes, true of `v0.2.3`; this addendum gives `v0.3.0` |
| `docs/adoption/stochasticinstantons.md:44-45` | in the one paragraph, "SI's `DatastoreObject` carries a `timestamp`, which the package's lacks" | true through `v0.2.3`. At `v0.3.0` the package's carries one too, keyword-only; "What changed for SI since `v0.2.3`", above |
| `docs/adoption/stochasticinstantons.md:86-87` | "The package's `DatastoreObject` (`datastorekit/object.py:9`) takes `store_id` only" | true of `v0.2.0`, whose line it cites, through `v0.2.3`; the sentence before it (`:84-86`), that SI's own takes `timestamp` and exposes it, still holds. At `v0.3.0` the package's takes `store_id` and a keyword-only `timestamp` (`datastorekit/object.py:10-14`) |
| `docs/adoption/stochasticinstantons.md:88` | "the 14 direct calls `DatastoreObject.__init__(…, timestamp=…)` raise `TypeError`" | under `v0.3.0` each is accepted as it stands. The sites (`:89-96`) and the ten pass-throughs (`:97-102`) still hold |
| `docs/adoption/stochasticinstantons.md:104` | the direct reads of `.timestamp` "would raise `AttributeError` without it" | under `v0.3.0` they get what SI's factories pass. The sites still hold |
| `docs/adoption/stochasticinstantons.md:106` | the reads by `getattr`, which "would quietly get `None`" | the same |
| `docs/adoption/stochasticinstantons.md:111` | "Whether SI drops the timestamp or keeps it on its own classes is SI's choice" | under `v0.3.0` SI keeps it on the package's `DatastoreObject`, its sites as they stand (the user's ruling, `object-timestamp` README §0); whether its factories pass it stays SI's. The test stand-ins (`:108-109`) still hold |
| `docs/adoption/stochasticinstantons.md:160` | item 4: "**`DatastoreObject.timestamp`** (item 2)" leaves the layer | it does not leave the layer: the package's object carries it. The rest of item 4 still holds |
| `docs/adoption/stochasticinstantons.md:515-521` | "SI adopts **`v0.2.3`** in place of `v0.2.2`, when it is next active", G4 reads "SI has adopted `v0.2.3`", and the pin `…@v0.2.3` | SI adopts `v0.3.0` in place of `v0.2.3`, when it is next active (`object-timestamp` U6), and G4 reads "SI has adopted `v0.3.0`"; the pin `…@v0.3.0`, above |
| `docs/adoption/stochasticinstantons.md:563-569` | the `v0.2.3` addendum's `path:line`s are "this file's as committed with this addendum", and the earlier addenda's are read six and twelve lines later | they are read at `0de2b16`, or six lines later here; the `v0.2.2` addendum's twelve, and the `v0.2.1` addendum's eighteen; above |
| `docs/adoption/stochasticinstantons.md:577` | the row for `:448-450`: SI adopts `v0.2.3` in place of `v0.2.2`, and G4 reads "SI has adopted `v0.2.3`" | as `:515-521` |
| `docs/adoption/stochasticinstantons.md:578` | the row for `:453`: "the pin `…@v0.2.3`, above" | the pin `…@v0.3.0`, above |
| `docs/adoption/stochasticinstantons.md:579` | the row for `:484-488`: the `v0.2.2` addendum's citations "are read at `6d8ee9a`, or six lines later here" | at `6d8ee9a`, or twelve lines later here (all but `:15-18`) |
| `docs/adoption/stochasticinstantons.md:580-581` | the rows for `:493` and `:494`, "as `:448-450`" and "the pin `…@v0.2.3`, above" | as `:515-521` |
| `docs/adoption/stochasticinstantons.md:582` | the row for `:496`: "at `v0.2.3`, with the three addenda" | at `v0.3.0`, with the four addenda |
| `docs/adoption/stochasticinstantons.md:583` | the row for `:497`: "G4 holds when SI has adopted `v0.2.3` (U37; `actor-names` U3; `factory-defaults` U5)" | G4 holds when SI has adopted `v0.3.0` (U37; `actor-names` U3; `factory-defaults` U5; `object-timestamp` U6) |

---

## Addendum: v0.4.0 (fingerprint prompt 02, 2026-10-14)

*Written by `fingerprint` prompt 02 on 2026-10-14, and added after `object-timestamp` prompt 02's
`v0.3.0` addendum. 07a's text and the `v0.2.1`, `v0.2.2`, `v0.2.3` and `v0.3.0` addenda stay as
written, each true of the release it names (`CLAUDE.md` rule 6). SI was not re-measured (as
decision U37); what this section says of SI comes from reads through `git` only, at `5fb4a1d` (SI's
`HEAD` when read, 2026-10-14, branch `dk-and-rpk-migration`).*

**The pin.** SI adopts **`v0.3.0`** or **`v0.4.0`**, as SI chooses, when it is next active, a move
being a commit of its own (decision U6 of the `fingerprint` campaign, which amends
`object-timestamp` decision U6 for SI), and G4 reads "SI has adopted `v0.3.0` or later". SI's tree
at `5fb4a1d` has no `datastorekit` line in its `requirements.txt`.

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.3.0
```

or

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0
```

`v0.4.0` carries `key_on_version`, `v0.2.0`'s feature, `v0.2.1`'s three fixes, `v0.2.2`'s fix,
`v0.2.3`'s change and `v0.3.0`'s change, unchanged.

**What changed for SI since `v0.3.0`.** One module was added to the package, by `fingerprint`
prompt 01 (`d1b61d6`): `datastorekit/store_fingerprint.py`, which takes a store's fingerprint from
what `read_inventory` returns, compares two and lists one, recording the package's own
`ENCODING_FORMAT` beside the client's format. The detail is
[`docs/client-contract.md` §9.7](../client-contract.md#97-fingerprint-prompt-01), and
[`README.md`'s addendum](README.md#addendum-v040-fingerprint-prompt-02-2026-10-14) gives it for
every client. The layer never calls the module: nothing SI supplies changes, nothing the layer
writes or reads changes, and no message, refusal or exception of the layer's. **Nothing changes for
SI.**
- **SI defines and calls none of the three functions.** By an `ast` read of every `.py` file
  through `git show` at `5fb4a1d`, outside `prompts/`, `.prompts/`, `docs/` and `.documents/`: no
  `def` and no call of `fingerprint_of`, `compare_fingerprints` or `listing_lines`, and no file
  names `datastorekit.store_fingerprint`.
- **It meets the module only when it adopts RunRegistryKit**, whose `[stores]` extra will require
  this release (`fingerprint` README §7). When and how SI does that is SI's.
- **The `v0.3.0` addendum's account of `DatastoreObject.timestamp` holds at `v0.4.0`**, whose
  `datastorekit/object.py` is `v0.3.0`'s: SI's 24 sites work as they stand once their import is
  rewritten, and `DatastoreObject.timestamp` does not leave the layer. Items 5, 6 and 8 are
  unchanged: every SI store is refused at open, and is rebuilt (U31).

**Line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, read at that tag
(`240028e`), one in the `v0.2.1` addendum stays `v0.2.1`'s (`33778b0`), and one in the `v0.3.0`
addendum stays `v0.3.0`'s (`2f5417e`, whose `datastorekit/` is `1b2f91a`'s). The `v0.2.2` and
`v0.2.3` addenda cite none, and neither does this addendum; one cited here would be `v0.4.0`'s,
whose `datastorekit/` is the tree of `fingerprint` prompt 01's commit `d1b61d6`. An SI line is SI's
at the commit named.

**What this addendum supersedes**, in this file. Each `path:line` below is this file's as committed
with this addendum. In the file as `object-timestamp` prompt 02 left it (`2f5417e`), every line
after `:37` is six lines earlier, since this addendum's italic line under the title adds six
(N = 6). The `v0.3.0` addendum's italic line added six too (k = 6), and the rule it states for the
earlier addenda still holds, each shift now N more. So:
- the `v0.3.0` addendum's citations, which are that file's, are read at `2f5417e`, or **6** lines
  later here (all but `:26-30`, which is above the insert), its rows for `:44-45` and later among
  them;
- the `v0.2.3` addendum's, which the `v0.3.0` addendum reads at `0de2b16` or six lines later, are
  read at `0de2b16`, or **12** lines later here (all but `:20-24`);
- the `v0.2.2` addendum's, which the `v0.3.0` addendum reads at `6d8ee9a` or twelve lines later,
  are read at `6d8ee9a`, or **18** lines later here (all but `:15-18`);
- the `v0.2.1` addendum's, which the `v0.3.0` addendum reads at `33778b0` or eighteen lines later,
  are read at `33778b0`, or **24** lines later here (all but `:5`).

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/stochasticinstantons.md:32-36` | the `v0.3.0` addendum gives the pin **`v0.3.0`** | it gives `v0.3.0`'s pin and changes, true of `v0.3.0`; this addendum gives SI's pins at `v0.4.0`: `v0.3.0` or `v0.4.0`, as SI chooses |
| `docs/adoption/stochasticinstantons.md:601-607` | "SI adopts **`v0.3.0`** in place of `v0.2.3`, when it is next active", G4 reads "SI has adopted `v0.3.0`", and the pin `…@v0.3.0` | SI adopts `v0.3.0` or `v0.4.0`, as SI chooses, when it is next active (`fingerprint` U6), and G4 reads "SI has adopted `v0.3.0` or later"; the pins `…@v0.3.0` or `…@v0.4.0`; "The pin", above |
| `docs/adoption/stochasticinstantons.md:609-610` | "`v0.3.0` carries `key_on_version`, `v0.2.0`'s feature, `v0.2.1`'s three fixes, `v0.2.2`'s fix and `v0.2.3`'s change, unchanged" | true of `v0.3.0`; `v0.4.0` carries those and `v0.3.0`'s change, unchanged |
| `docs/adoption/stochasticinstantons.md:654-662` | the `v0.3.0` addendum's `path:line`s are "this file's as committed with this addendum", and the earlier addenda's are read 6, 12 and 18 lines later | they are read at `2f5417e`, or 6 lines later here; the `v0.2.3` addendum's 12, the `v0.2.2` addendum's 18, and the `v0.2.1` addendum's 24; above |
| `docs/adoption/stochasticinstantons.md:674` | the row for `:515-521`: "SI adopts `v0.3.0` in place of `v0.2.3`, when it is next active (`object-timestamp` U6), and G4 reads 'SI has adopted `v0.3.0`'; the pin `…@v0.3.0`" | as `:601-607` |
| `docs/adoption/stochasticinstantons.md:675` | the row for `:563-569`: read "at `0de2b16`, or six lines later here; the `v0.2.2` addendum's twelve, and the `v0.2.1` addendum's eighteen" | at `0de2b16`, or twelve lines later here; the `v0.2.2` addendum's eighteen, and the `v0.2.1` addendum's twenty-four; above |
| `docs/adoption/stochasticinstantons.md:676` | the row for `:577`: "as `:515-521`" | as `:601-607` |
| `docs/adoption/stochasticinstantons.md:677` | the row for `:578`: "the pin `…@v0.3.0`, above" | the pins `…@v0.3.0` or `…@v0.4.0`, above |
| `docs/adoption/stochasticinstantons.md:678` | the row for `:579`: the `v0.2.2` addendum's citations are read "at `6d8ee9a`, or twelve lines later here" | at `6d8ee9a`, or eighteen lines later here (all but `:15-18`) |
| `docs/adoption/stochasticinstantons.md:679` | the rows for `:580-581`: "as `:515-521`" | as `:601-607` |
| `docs/adoption/stochasticinstantons.md:680` | the row for `:582`: "at `v0.3.0`, with the four addenda" | at `v0.3.0` or `v0.4.0`, as SI chooses, with the five addenda |
| `docs/adoption/stochasticinstantons.md:681` | the row for `:583`: "G4 holds when SI has adopted `v0.3.0` (U37; `actor-names` U3; `factory-defaults` U5; `object-timestamp` U6)" | G4 holds when SI has adopted `v0.3.0` or later (U37; `actor-names` U3; `factory-defaults` U5; `object-timestamp` U6; `fingerprint` U6) |

**Standing, not superseded:** the `v0.3.0` addendum's account of `DatastoreObject.timestamp`, true
of `v0.4.0`, whose `datastorekit/object.py` is `v0.3.0`'s: its "What changed for SI since `v0.2.3`"
(`:612-646`), with its line that `DatastoreObject.timestamp` "does not leave the layer" (`:641`);
its row for the `v0.2.3` addendum's head line (`:666`); and its rows for `:44-45` to `:160`
(`:667-673`), each a statement about `DatastoreObject.timestamp` that `v0.3.0` superseded.

---

## Addendum: v0.5.0 (extra-values prompt 02, 2026-10-21)

*Written by `extra-values` prompt 02 on 2026-10-21, and added after `fingerprint` prompt 02's
`v0.4.0` addendum. 07a's text and the `v0.2.1`, `v0.2.2`, `v0.2.3`, `v0.3.0` and `v0.4.0` addenda
stay as written, each true of the release it names (`CLAUDE.md` rule 6). SI was not re-measured
(as decision U37); what this section says of SI comes from reads through `git` only, at `f5f395b`
(SI's `HEAD` when read, 2026-10-21, branch `dk-and-rpk-migration`). An SI `path:line` here is SI's
at `f5f395b`. Nothing of SI was imported, run or opened.*

**This is the note SI's pin prompt reads.** `v0.5.0` is the release SI asked for, in its brief
(`.prompts/dk-and-rpk-migration/datastorekit-second-value-table-brief.md`, committed as
`f5f395b`), and it carries the one change SI asked for. It says what SI declares, where, what then
holds, and what of SI's own code and tests moves.

**The pin.** SI adopts **`v0.5.0`** in place of `v0.4.0`, which its `requirements.txt:16` pins at
`f5f395b` (since SI's `1b1ca6d`), by a pin prompt of its own, a commit of its own (decision U5 of
the `extra-values` campaign, as amended by the user on 2026-10-21):

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.5.0
```

G4 reads, as before, "SI has adopted `v0.3.0` or later"; whether it holds is not recorded here.

`v0.5.0` carries `key_on_version`, `v0.2.0`'s feature, `v0.2.1`'s three fixes, `v0.2.2`'s fix,
`v0.2.3`'s change, `v0.3.0`'s change and `v0.4.0`'s change, unchanged.

**What changed since `v0.4.0`.** One prompt changed the package, `extra-values` prompt 01
(`5475cef`): an `InventorySpec` may name further value tables, `extra_values`, each table → its
column naming the class's serial, and the inventory counts each as it counts `values`, into each
record's `extra_value_counts`, which `Record.as_json` carries only where it is not empty;
`ENCODING_FORMAT` stays `1`; and `inventory_classes` gains one refusal, of a spec whose value table
is also one of its `extra_values`. The detail is
[`docs/client-contract.md` §9.8](../client-contract.md#98-extra-values-prompt-01), and
[`README.md`'s addendum](README.md#addendum-v050-extra-values-prompt-02-2026-10-21) gives it for
every client. Nothing the pool writes or reads changes, and no message, refusal or exception of
the pool's.

**Nothing SI calls changes.** By an `ast` read of every `.py` file through `git show` at
`f5f395b`, outside `prompts/`, `.prompts/`, `docs/` and `.documents/`: SI's 22 `InventorySpec(...)`
calls each pass keywords, and none passes `extra_values`; its one `Record(...)` call passes
keywords (`tests/test_inventory_report.py:67`); it calls no `read_records`, walks no spec's fields
with `dataclasses.fields`, and reads no `extra_values`, `extra_value_counts` or `as_json`. Its
reads of `record.value_count` (`tools/inventory_report.py:373-374`, `:405-406`;
`tests/test_inventory_store.py:306`) are unchanged. Until SI declares the field, every record and
fingerprint of a store read with SI's specs is `v0.4.0`'s.

### What SI declares, and where

In `GradientCoupledInstanton`'s spec (`Datastore/SQL/ObjectFactories/GradientCoupledInstanton.py`,
`inventory_spec`, `:147-182`; `InventorySpec(` at `:158`), beside its `values=` (`:180`,
`("GradientCoupledInstantonProfile", "parent_serial")`), one keyword:

```python
extra_values={"GradientCoupledInstantonValue": "instanton_serial"},
```

`instanton_serial` is `GradientCoupledInstantonValue`'s column naming its owner, a foreign key to
`GradientCoupledInstanton.serial` (`:686-692`). The mapping is keyed by the table's name; the count
is read back as `record.extra_value_counts["GradientCoupledInstantonValue"]`.

### What then holds

- **Each `GradientCoupledInstanton` record carries `extra_value_counts`**,
  `{"GradientCoupledInstantonValue": n}`, n the number of that table's rows naming the record's
  row, **0 where none** (a row stored without full values). `value_count` still counts
  `GradientCoupledInstantonProfile`, as now. The record's canonical line, and so its class's digest
  in a fingerprint, gains the fifth key; every other class's records are `v0.4.0`'s.
- **Rows of `GradientCoupledInstantonValue` naming a serial not on their shard** are an
  `orphan-value` problem of `GradientCoupledInstanton`, naming the table and the shard, in the
  words of the `values` table's.
- **The table and its column are read whenever the inventory is.** A store that lacks either
  raises `KeyError` when read, as for `values`.
- **Naming `GradientCoupledInstantonProfile` in both slots is refused**: `inventory_classes`
  raises `ValueError`, naming the class and the table. `inventory_specs` does not, and no spec's
  construction does.
- **SI's fingerprints of the class change**, which is SI's `fingerprint_format`, never
  `ENCODING_FORMAT`. SI has recorded no fingerprint, so none it holds moves.

### What of SI's own moves

Each is SI's to change, as SI chooses; this addendum names them and makes no choice.
- **Its coverage test**, `tests/test_inventory_specs.py`: `EXCLUDED` names
  `GradientCoupledInstantonValue` (`:208-214`); `READ_THROUGH` maps a class to `(owner, slot)`
  (`:199-205`), checked against `SLOTS`, which names `tags`, `values` and `parent_sets` (`:216`);
  `_slot_tables` (`:224-228`) reads a slot's table as `value[0]`, a pair's first item, where
  `extra_values` is a mapping, table → column; and the counts it asserts, `(24, 5, 1)` declaring,
  read through and excluded (`:412`).
- **Its spec tests**: `_as_table` (`:283-297`), which `test_each_spec_is_the_identity_its_build_matches`
  (`:325-…`) compares with `EXPECTED_SPECS`, holds `spec.values` and not `extra_values`; and
  `test_every_named_column_is_a_column_of_its_table` checks the `values` table's column and its
  foreign key (`:351-358`) and not an extra table's. Neither sees the declaration unless it is
  extended.
- **Its report**, `tools/inventory_report.py`, which reads `value_count` (`:373-374`, `:405-406`),
  if SI chooses to show the new counts.
- **The comment in the spec** (`:152-155`), which says the table "is outside the inventory".
- **The issue SI holds**, `[gci-value-table-outside-the-inventory]`, which is SI's to close.

SI has recorded no fingerprint and has no spec guard. **Advice:** if SI adds a spec guard, use
RunRegistryKit's recipe (its `docs/adoption/README.md` §6) with the one condition
[`README.md`'s addendum](README.md#addendum-v050-extra-values-prompt-02-2026-10-21) gives ("The
spec guard"): `plain` leaves out a field named `extra_values` whose value is empty.

### Where this release departs from SI's brief

As `prompts/extra-values/README.md` §0.2 records, each point:
1. **The field's shape.** The brief advises a name SI chooses for each table,
   `Mapping[str, Tuple[str, str]]`. `v0.5.0` keys the mapping by the table's name,
   `extra_values: Mapping[str, str]`, table → column, and `extra_value_counts` the same way. A
   table cannot be named twice and no name can be empty, so of the brief's three refusals one is
   left: an extra table that is also the `values` table.
2. **The tests are not on a separate registry alone.** This repository's neutral client declares
   the field (a `TraceMark` table under `Trace`), since a test requires the neutral registry to use
   every field; its format became 2 with a new golden beside the old, and the format-1 golden is
   kept as the test that a spec which does not declare the field gives the records it gave.
3. **Where the refusal is.** In `inventory_classes`, naming the class, not in the spec's
   construction, so that a spec stays as forgiving as it is for the pool's drop, which reads
   `inventory_specs` and never `inventory_classes`.
4. **`ENCODING_FORMAT`** stays `1`, by the user's ruling; the comment beside it and contract §9.8
   say how its rule's item 1 is read.
5. **Everything else the brief measured holds.**

**Line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, read at that tag
(`240028e`), one in the `v0.2.1` addendum stays `v0.2.1`'s (`33778b0`), and one in the `v0.3.0`
addendum stays `v0.3.0`'s (`2f5417e`, whose `datastorekit/` is `1b2f91a`'s). The `v0.2.2`,
`v0.2.3` and `v0.4.0` addenda cite none, and neither does this addendum; one cited here would be
`v0.5.0`'s, whose `datastorekit/` is the tree of `extra-values` prompt 01's commit `5475cef`. An SI
line is SI's at the commit named, and at `f5f395b` in this addendum.

**What this addendum supersedes**, in this file. Each `path:line` below is this file's as committed
with this addendum. In the file as `fingerprint` prompt 02 left it (`c8570e8`), every line after
`:43` is six lines earlier, since this addendum's italic line under the title adds six (N = 6),
and every line of the appendix, which follows this addendum, is 181 lines earlier (N and this
addendum's 175 lines). The `v0.4.0` addendum's italic line added six too (k = 6), and the rule it
states for the earlier addenda still holds, each shift now N more. So:
- the `v0.4.0` addendum's citations, which are that file's, are read at `c8570e8`, or **6** lines
  later here (all but `:32-36`, which is above the insert);
- the `v0.3.0` addendum's, which the `v0.4.0` addendum reads at `2f5417e` or six lines later, are
  read at `2f5417e`, or **12** lines later here (all but `:26-30`), its rows for `:44-45` and
  later among them;
- the `v0.2.3` addendum's, which the `v0.4.0` addendum reads at `0de2b16` or twelve lines later,
  are read at `0de2b16`, or **18** lines later here (all but `:20-24`);
- the `v0.2.2` addendum's, which the `v0.4.0` addendum reads at `6d8ee9a` or eighteen lines later,
  are read at `6d8ee9a`, or **24** lines later here (all but `:15-18`);
- the `v0.2.1` addendum's, which the `v0.4.0` addendum reads at `33778b0` or twenty-four lines
  later, are read at `33778b0`, or **30** lines later here (all but `:5`).

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/stochasticinstantons.md:38-42` | the `v0.4.0` addendum gives "SI's pin, `v0.3.0` or `v0.4.0` as SI chooses" | it gives `v0.4.0`'s pins and changes, true of `v0.4.0`; this addendum gives SI's pin at `v0.5.0`: `v0.5.0` |
| `docs/adoption/stochasticinstantons.md:699-712` | in part: "SI adopts **`v0.3.0`** or **`v0.4.0`**, as SI chooses, when it is next active", "SI's tree at `5fb4a1d` has no `datastorekit` line in its `requirements.txt`", and the pins `…@v0.3.0` or `…@v0.4.0` | SI is on `v0.4.0` (`requirements.txt:16` at `f5f395b`, since its `1b1ca6d`), and adopts `v0.5.0` (`extra-values` U5, as amended); the pin `…@v0.5.0`; "The pin", above. The rest stands: a move is a commit of SI's own, and G4's reading |
| `docs/adoption/stochasticinstantons.md:714-715` | "`v0.4.0` carries `key_on_version`, `v0.2.0`'s feature, `v0.2.1`'s three fixes, `v0.2.2`'s fix, `v0.2.3`'s change and `v0.3.0`'s change, unchanged" | true of `v0.4.0`; `v0.5.0` carries those and `v0.4.0`'s change, unchanged |
| `docs/adoption/stochasticinstantons.md:744-757` | the `v0.4.0` addendum's `path:line`s are "this file's as committed with this addendum", and the earlier addenda's are read 6, 12, 18 and 24 lines later | they are read at `c8570e8`, or 6 lines later here; the `v0.3.0` addendum's 12, the `v0.2.3` addendum's 18, the `v0.2.2` addendum's 24, and the `v0.2.1` addendum's 30; above |
| `docs/adoption/stochasticinstantons.md:761` | in part, the row for `:32-36`: "this addendum gives SI's pins at `v0.4.0`: `v0.3.0` or `v0.4.0`, as SI chooses" | the `v0.4.0` addendum gives those, true of `v0.4.0`; this addendum gives `v0.5.0`, above |
| `docs/adoption/stochasticinstantons.md:762` | in part, the row for `:601-607`: "SI adopts `v0.3.0` or `v0.4.0`, as SI chooses, when it is next active (`fingerprint` U6) …; the pins `…@v0.3.0` or `…@v0.4.0`" | as `:699-712`. The row's G4 reading stands |
| `docs/adoption/stochasticinstantons.md:763` | the row for `:609-610`: "`v0.4.0` carries those and `v0.3.0`'s change, unchanged" | as `:714-715` |
| `docs/adoption/stochasticinstantons.md:764` | the row for `:654-662`: read "at `2f5417e`, or 6 lines later here; the `v0.2.3` addendum's 12, the `v0.2.2` addendum's 18, and the `v0.2.1` addendum's 24" | at `2f5417e`, or 12 lines later here; the `v0.2.3` addendum's 18, the `v0.2.2` addendum's 24, and the `v0.2.1` addendum's 30; above |
| `docs/adoption/stochasticinstantons.md:765` | the row for `:674`: "as `:601-607`" | as `:762` |
| `docs/adoption/stochasticinstantons.md:766` | the row for `:675`: read "at `0de2b16`, or twelve lines later here; the `v0.2.2` addendum's eighteen, and the `v0.2.1` addendum's twenty-four" | at `0de2b16`, or eighteen lines later here; the `v0.2.2` addendum's twenty-four, and the `v0.2.1` addendum's thirty; above |
| `docs/adoption/stochasticinstantons.md:767` | the row for `:676`: "as `:601-607`" | as `:762` |
| `docs/adoption/stochasticinstantons.md:768` | the row for `:677`: "the pins `…@v0.3.0` or `…@v0.4.0`, above" | the pin `…@v0.5.0`, above |
| `docs/adoption/stochasticinstantons.md:769` | the row for `:678`: the `v0.2.2` addendum's citations are read "at `6d8ee9a`, or eighteen lines later here" | at `6d8ee9a`, or twenty-four lines later here (all but `:15-18`) |
| `docs/adoption/stochasticinstantons.md:770` | the row for `:679`: "as `:601-607`" | as `:762` |
| `docs/adoption/stochasticinstantons.md:771` | the row for `:680`: "at `v0.3.0` or `v0.4.0`, as SI chooses, with the five addenda" | at `v0.5.0`, with the six addenda |

**Standing, not superseded:** G4's reading, "SI has adopted `v0.3.0` or later", in the `v0.4.0`
addendum's pin (`:699-701`) and its rows (`:762`, `:772`); its "What changed for SI since
`v0.3.0`" (`:717-735`), true of `v0.4.0`: SI defines and calls none of the package's fingerprint
functions as read at `5fb4a1d`, "It meets the module only when it adopts RunRegistryKit" is a
condition, which this addendum does not re-measure, and the `v0.3.0` addendum's account of
`DatastoreObject.timestamp` holds at `v0.5.0` too, whose `datastorekit/object.py` is `v0.3.0`'s;
and its "Standing" paragraph (`:774-778`).

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
