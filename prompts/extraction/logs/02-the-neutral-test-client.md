# Log 02 — the neutral test client

**Subject:** Add the neutral test client, the stand-in pool and the client contract · **Commit:**
this commit · **Date:** 2026-10-07 · **Model:** Claude Opus 5.5 · **Result:** landed.
`docs/client-contract.md` states every fact a client supplies; the neutral client supplies each
one; the stand-in pool is SGK's generic half; the 88 ported tests use the client's names (U8);
`compare_with_source.py` exits 0 over 31 files and now fails on an unaccounted file;
`Ran 109 tests … OK` (90 before).

Prompt: [`../02-the-neutral-test-client.md`](../02-the-neutral-test-client.md), with the
orchestrator's notes for this prompt (four corrections and two additions, followed as given except
where §2 says otherwise).

## 1. What shipped

Eight new files, four changed, and the records.

- **`docs/client-contract.md`** (§2.1): the 16 constructor parameters, the 9 `register()` keys and
  the `None` registration, the 10 hooks, the three declarations and their 15 fields, the layer's
  tables, what the layer reads from an object, and the other entry points. Each with where it is
  given, its kind and default, whether it is read for replicated or sharded classes, what the layer
  does with it, what it does when it is wrong or absent (with the line), and the neutral client's
  class. Measured from the package (§4.1 below). It names no client.
- **The neutral client**, `datastorekit/tests/client/` (§2.2): `__init__.py`, `objects.py` (the
  stored classes, each named as its table), `factories.py` (one factory per class), `registry.py`
  (exactly the nine names, in `__all__` and as the module's only public names) and `build.py`
  (helpers per class, `write_every_class(pool)` and `build_store(directory, shards=3)`). It imports
  the standard library, `sqlalchemy` and `datastorekit` only; no `ray` (§2 item 5).
- **The stand-in pool**, `datastorekit/tests/standin_pool.py` (§2.3): SGK's `:1-418`, changed only
  by D-str (the three module paths), D-split (the cut at the banner; the two imports and the
  getter's name in `open_pool` and `open_pool_output`) and D-fmt (`black` removing the two blank
  lines the cut left). Nothing else; the docstring is SGK's.
- **`datastorekit/tests/test_neutral_client.py`** (§2.7): 19 tests in three classes (§4.2).
- **U8** (§2.4): 15 lines in three files, inside string literals only (§3 below).
- **`docs/extraction/compare_with_source.py`** (§2.6): D-fix, D-split, and the failure on an
  unaccounted file (§4.3).
- **The records**: this log; the board (header, §1's row, §3 and §4); `docs/OPEN_ISSUES.md`;
  `prompts/INDEX.md`.

### 1.1 The neutral client

Fourteen classes (13 tables), one class per role where one class carries several:

| Class | Kind | Roles |
|---|---|---|
| `version`, `store_tag` | replicated | the layer's two tables, label column `label`; `store_tag` with `timestamp: True` |
| `keypoint` | replicated | **the shard-key class**; `monotone_flags` (`kp_marked`, `kp_flagged`); `read_table`, `tables_arg` False; `_updated` on a flag turned on |
| `keypoint_alias` | replicated | **the proxy** (the getter maps it to its keypoint); `stepping: "exact"`; `version: True`; a replicated `store` that inserts or verifies by serial, with no owned rows |
| `dial_setting` | replicated | `stepping: "minimum"` (served by the smallest stepping at least the one asked); `read_table`, `tables_arg` True; `version` left to its default |
| `knob_setting` | replicated | `stepping: True`; `timestamp: False` |
| `ephemeral_probe` | replicated | `register()` returns `None` |
| `Gadget` | replicated | **the replicated owner**: `validate_on_startup` (the pool's prune), `validated_column` + `revalidate`, `owned_serials`; tagged; values; a **polymorphic** `Parent` (`frame`, over `dial_setting` and `knob_setting`); insert-or-verify `store` |
| `Gadget_tags` | neither list | the replicated class's tag table; `serial: False` |
| `GadgetPart` | replicated | `owner_column` (`gadget_serial`) |
| `Tessera` | sharded on `"k"` | keyed on the proxy (its `k` is a `keypoint_alias`) |
| `Sample` | sharded on `"k"` | `validate_on_startup` (each actor's prune); `read_batch`; tags; a `nullable`, `cross_shard` `Parent` with no foreign key (`anchor`, a `Tessera` maybe on another shard); a `ParentSet` (`members`) |
| `Sample_tags` | neither list | the tag association |
| `Sample_members` | neither list | the `ParentSet`'s member table: names its rows by foreign key, declares no `inventory_spec`; `serial: False` |

The replicated-only roles (`owner_column`, `monotone_flags`, `validated_column` with `revalidate`,
`owned_serials`) are on replicated classes (correction 1): `keypoint`, `Gadget` and `GadgetPart`.
`Sample` keeps `validate_on_startup`, and declares no `validated_column`, so that the coverage test
can require it on a replicated class.

`build_store` writes, through the stand-in pool: three tags (one unused); three keypoints by one
vectorized get, then one again with its flag on (an update, replicated); two dial settings, one
knob setting, one probe get; one alias per keypoint (a miss, then a replicated store); two Gadgets
with tags and parts (one validated, one left unvalidated); two Tesserae per alias (by
`object_get_vectorized`); one validated Sample per keypoint, keyed on the validated Gadget, its own
keypoint's Tesserae as members and the next keypoint's first Tessera as anchor (none for the first);
and one unvalidated Sample. Every table holds rows; `PRAGMA foreign_key_check` is empty on every
shard, and `read_inventory` reports no problem, at 3, 2 and 1 shards (measured in the scratchpad).

**The drop groups.** `aliases` (`keypoint_alias`), `tesserae` (`Tessera`), `samples` (`Sample`,
`Sample_tags`, `Sample_members`), `gadgets` (`Gadget`, `Gadget_tags`, `GadgetPart`). Their union
is every table but `version`, `store_tag`, `keypoint`, `dial_setting` and `knob_setting`, and is
closed (`dependent_tables` of it is `[]`). Alone, `samples` is closed; `tesserae` and `gadgets`
must be dropped with `Sample`, `Sample_tags`, `Sample_members`; `aliases` with those and `Tessera`.
Two groups hold a replicated table (`aliases`, `gadgets`). This mirrors what 04's
`test_drop_refuses_dangling_references` needs: a group refused alone (`tesserae` or `aliases`), a
declared parent with no foreign key (`Sample.anchor` → `Tessera`), a foreign key with no declared
parent (`Sample_members` → `Tessera`), a transitive dependent (`Sample_tags`), and a group with a
replicated table (§2 item 3).

### 1.2 The three clients' registries, measured (§2.2)

Read with `git show` at SGK `6f7f291` (`config/datastore.py`, `config/sharding.py`), CPBH
`52142d7` and SI `96d0562` (`Datastore/SQL/Datastore.py`, `config/sharding.py`), by `ast`, from the
scratchpad. Registry keys (the table names):

- **SGK (38):** version, store_tag, redshift, wavenumber, wavenumber_exit_time, tolerance,
  LambdaCDM, QCD_Cosmology, IntegrationSolver, BackgroundModel, BackgroundModel_tags,
  BackgroundModelValue, TkNumericIntegration, TkNumeric_tags, TkNumericValue, TkWKBIntegration,
  TkWKB_tags, TkWKBValue, GkNumericIntegration, GkNumeric_tags, GkNumericValue, GkWKBIntegration,
  GkWKB_tags, GkWKBValue, GkSourcePolicy, GkSourcePolicyData, GkSource, GkSource_tags,
  GkSourceValue, GkSource_parents, QuadSourcePolicy, QuadSource, QuadSource_tags, QuadSourceValue,
  QuadSourceIntegral, QuadSourceIntegral_tags, OneLoopIntegral, OneLoopIntegral_tags.
- **CPBH (27):** version, store_tag, redshift, tolerance, beta_value, M_value, Lambda_value,
  temperature, phi_value, pi_value, InversePowerPotential, StarobinskyPotential,
  ExponentialPotential, ReclinerPotential, ReflectingPotential, ExponentialCoupling, QCD_Cosmology,
  IntegrationSolver, ScalarModel, ScalarModel_tags, ScalarModelValue, AdiabaticHistory,
  AdiabaticHistory_tags, AdiabaticHistoryValue, BBNData, BBNData_tags, BBNDataValue. (Its
  `replicated_tables` also names `LambdaCDM`, which its registry does not declare.)
- **SI (30):** version, store_tag, redshift, tolerance, efold_value, delta_Nstar, N_init, N_final,
  n_collocation_points, alpha_regularization, inflaton_mass, quartic_coupling, phi_value, pi_value,
  QuadraticPotential, QuarticPotential, MasslessDecoupledDiffusion, IntegrationSolver,
  InflatonTrajectory, InflatonTrajectoryValue, CosmologicalParams, FullInstanton,
  FullInstantonValue, GradientCoupledInstanton, GradientCoupledInstantonValue,
  GradientCoupledInstantonProfile, SlowRollInstanton, SlowRollInstantonValue, CompactionFunction,
  CompactionFunctionSamples.

82 names in all. Shared by all three: `version`, `store_tag` (the layer's), `redshift`,
`tolerance`, `IntegrationSolver`. `QCD_Cosmology` is in SGK's and CPBH's, **not SI's** (§2 item
11). Shard-key types: `wavenumber`, `beta_value`, `delta_Nstar`.

None of the neutral client's 14 class names is among the 82, and none occurs as a whole word in the
package's code or prose before this commit (`grep -rw`; `Tessera` was chosen over `Fragment`,
whose lower-case form occurs in four test modules).

### 1.3 The role table for 03 and 04

One row per name the 18 modules of README §0.2 import from SGK outside the layer (the layer's own
imports map by README §4), measured by `ast` at SGK `6f7f291`; for the stand-in pool and the
fixture modules, per attribute used.

| Imported name | Used by | What it does for the test | Neutral counterpart |
|---|---|---|---|
| `config.datastore.factories` | 03, 04 (13 modules) | the registry a pool, the reader and the schema builder are given | `registry.factories` |
| `config.sharding.replicated_tables`, `sharded_tables` | 03, 04 | the pool's lists; what the check at open compares | `registry.replicated_tables`, `registry.sharded_tables` |
| `config.sharding.shard_key_type`, `shard_key_wavenumber_store_id` | `test_version_row_at_open`, `test_read_only_pool` | a pool built by hand | `registry.shard_key_type`, `registry.shard_key_store_id` |
| `config.sharding.read_table_config` | `test_read_only_pool` | `read_table` on a read-only pool | `registry.read_table_config` |
| `config.datastore.drop_groups`, `tables_to_drop` | `test_reconcile_at_open`, `test_layer_registry`, `test_drop_refuses_dangling_references` | drop actions, and their tables | `registry.drop_groups`, `registry.tables_to_drop` (§1.1) |
| `config.defaults.DEFAULT_QUADRATURE_RTOL`, `DEFAULT_HEXIT_ABS_TOLERANCE`, `DEFAULT_HEXIT_REL_TOLERANCE` | `test_read_only_pool` | SGK's tolerance values, got as rows | none: the test uses the client's own values (`build.get_dial`, `get_knob`) |
| `CosmologyModels.LambdaCDM.Planck2018`, `CosmologyConcepts.wavenumber_exit_time`, `ComputeTargets.BackgroundModel`, `extract_common.run_label_tag` | `test_read_only_pool` | a cosmology row, an exit time, a model, a tag label | `knob_setting`/`dial_setting` rows; `keypoint_alias` (`build.make_alias`); `Gadget` (`build.make_gadget`); a literal tag label — 03 adapts |
| `CosmologyModels.model_ids.*`, `ObjectFactories.cosmology_types.COSMOLOGY_TYPES` | `test_inventory_declarations` | the polymorphic parent's type map | `factories.FRAME_TYPES`, `FRAME_KINDS` |
| `tools.inventory_report.format_inventory_report` | `test_inventory_declarations` | SGK's report | none: SGK's tool, stays in SGK (README §1); 04 drops or rewrites the tests that use it |
| `sp.StandinCluster`, `StandinActorDied`, `StandinRef`, `sp_mod`, `ds_mod`, `DatastoreClass`, `_Options`, `_read`, `table_columns`, `shard_rows`, `shard_snapshot`, `store_checksums`, `in_flight_records` | 03, 04 | the stand-in pool and its file readers | `datastorekit.tests.standin_pool`, the same names (§2.3) |
| `sp.StandinSerial` | `test_read_only_pool` | something a factory reads only a `store_id` of | `objects.SerialHandle` |
| `sp.StandinCosmology`, `sp.make_units` | 03 | a cosmology and units for SGK's objects | none needed: the client has no units, and its frames are stored rows |
| `sp.get_wavenumber` | 03 | a replicated get of the shard-key class | `build.get_keypoint` |
| `sp.get_redshifts` | 03 | a vectorized replicated get of a flagged leaf | `build.get_keypoints` |
| `sp.get_tolerance` | 03 | a replicated get of a leaf | `build.get_dial`, `build.get_knob` |
| `sp.make_exit_time` | 03 | an unstored replicated proxy, for a replicated store | `build.make_alias` (+ `get_alias`) |
| `sp.make_background_model` | 03 | an unstored replicated owner with tags and values | `build.make_gadget` (+ `store_gadget`) |
| `sp.make_policy_data` | 03 | an unstored sharded object, for a sharded store | `build.make_sample` (+ `store_sample`); `Tessera` is the class keyed on the proxy |
| `real_store_fixtures.build_full_store` | 04, `test_foreign_key_check` | a store with every class populated | `build.build_store` (a counterpart, written through the pool) |
| `real_store_fixtures.build_real_store`, `file_state`, `find_row`, `full_rows`, `relabel_serials`, `vary_row`, `expected_row_counts`, `independent_row_counts` | 04 | hand-built stores (with schema variants), file states, row edits | **03/04 ports it** |
| `schema_description.actor_with_built_schema`, `describe_schema`, `dumps` | `test_schema_builder` | the schema witness | **04 ports it** |
| `shard_store_fixtures.bare_pool`, `read_pool`, `tree_state`, `write_hand_built_primary`, `write_new_store`, `write_placeholder` | 03, 04 | hand-built primaries | ported by 01; now keyed on `keypoint` / `Sample` |
| `test_prune_at_open._PruneTestCase`, `execute`, `quiet`; the modules `test_replicated_write`, `test_reconcile_at_open`, `test_version_row_at_open` | `test_declared_facts`, `test_one_timestamp_per_write` | test helpers across modules | **03/04 ports it**, with its module |

### 1.4 The entry points 03 and 04 use

`datastorekit.tests.client.registry`: `factories: Dict[str, type]`; `replicated_tables: List[str]`;
`sharded_tables: Dict[str, str]`; `shard_key_type = objects.keypoint`;
`shard_key_store_id(obj) -> int`; `read_table_config: Dict[str, dict]`;
`serial_batch_sizes: Dict[str, int]`; `drop_groups: Dict[str, List[str]]`;
`tables_to_drop(actions: Iterable[str]) -> List[str]`.

`datastorekit.tests.client.objects`: `SerialHandle(store_id)`; `version_entry(store_id, label)`;
`tag_entry(store_id, label)`; `keypoint(store_id, position, marked=False, flagged=False)`;
`keypoint_alias(store_id, keypoint, offset, stepping=0)`; `dial_setting(store_id, level,
stepping=0)`; `knob_setting(store_id, turns, stepping=0)`; `ephemeral_probe(note)`;
`GadgetPart(store_id, part_index, part_value)`; `Gadget(store_id, label, frame, tags=(),
parts=None, validated=False)`; `Tessera(store_id, k, weight)`; `Sample(store_id, k, gadget, code,
tags=(), members=(), anchor=None, validated=False)`.

`datastorekit.tests.client.factories`: one `<class>_factory` per class (`Sample_factory`,
`keypoint_factory`, …); `FRAME_KINDS`, `FRAME_TYPES`.

`datastorekit.tests.client.build`: `build_store(directory, shards=3) -> Path`;
`write_every_class(pool) -> Dict[str, list]`; `open_pool(cluster, primary, shards=3, **kwargs)`
(adds the registry's `read_table_config` and `serial_batch_sizes`); `resolve(refs)`;
`get_version(pool, label)`; `get_tags(pool, *labels)`; `get_keypoint(pool, position,
marked=False, flagged=False)`; `get_keypoints(pool, positions, marked=False, flagged=False)`;
`get_dial(pool, level, stepping=0)`; `get_knob(pool, turns, stepping=0)`; `get_probe(pool, note)`;
`make_alias(k, offset, stepping=0)`; `get_alias(pool, k, offset, stepping=0)`;
`make_gadget(label, frame, tags, values)`; `store_gadget(pool, gadget, validate=True)`;
`get_gadget(pool, label, frame, tags)`; `get_tesserae(pool, alias, weights)`; `make_sample(k,
gadget, code, tags=(), members=(), anchor=None)`; `store_sample(pool, sample, validate=True)`;
`get_sample(pool, k, gadget, code, tags=())`; `read_samples(pool, k, validated_only=True)`; and the
constants of what `build_store` writes (`TAG_LABELS`, `KEYPOINT_POSITIONS`, `MARKED_POSITION`,
`ALIAS_OFFSET`, `ALIAS_STEPPING`, `TESSERA_WEIGHTS`, `DIAL_LEVELS`, `KNOB_TURNS`, `GADGETS`,
`UNVALIDATED_SAMPLE`).

`datastorekit.tests.standin_pool`: `StandinCluster()` with `active()`, `pin_controller(shard_id)`,
`fault(shard_id, method, cls_name, when="before")`, `clear_faults()`, `open_pool(primary,
shards=3, **kwargs)`, `open_pool_output(primary, shards=3, **kwargs)`, `close_pool(pool=None)`,
`replica_ids(pool=None)`, and the attributes `controller`, `calls`, `hooks`, `faults`, `pool`;
`StandinActorDied`, `StandinRef`, `standin_get(refs)`; `sp_mod`, `ds_mod`, `broker_mod`,
`DatastoreClass`, `BrokerClass`; `_read(path, sql, params=())`, `table_columns(path, table)`,
`shard_rows(pool, table)`, `shard_snapshot(pool, tables)`, `store_checksums(primary)`,
`in_flight_records(pool)`.

## 2. Deviations from the prompt

1. **Correction 1** (orchestrator): `validated_column` with `revalidate`, and `owned_serials`, are on
   the replicated `Gadget`, `owner_column` on the replicated `GadgetPart`, `monotone_flags` on the
   replicated `keypoint`; `Sample` keeps `validate_on_startup` only. The contract says, for each of
   the five, that it is read for replicated classes only. **STRUCTURALLY REQUIRED.**
2. **Corrections 2-4** (orchestrator): `build_schema(sqla.MetaData(), factories)`; §2.4 re-fixtures
   three files; breakage (m) fails a test in this commit
   (`test_a_replicated_get_is_written_on_the_pinned_controller_then_copied`, written for it).
   **STRUCTURALLY REQUIRED.**
3. **The drop groups are not each closed.** The notes read "`dependent_tables` accepts each group
   as the client declares it" as "returns `[]` for each group". The client's groups are instead
   shaped as 04's `test_drop_refuses_dangling_references` needs (the notes ask the groups to be
   made from it): that test refuses one group alone, and asserts a dependent reached by a declared
   parent with no foreign key, one by a foreign key with no declared parent, and one transitively,
   each through a group, which a set of closed groups cannot give. The test therefore asserts that
   every group's names are declared tables (no `ValueError`), that each group's dependents are the
   measured ones and lie within the groups (each group with them, and the union, give `[]`), and
   that the union is every table but the five kept. **IMPLEMENTATION CHOICE**, flagged for the
   orchestrator.
4. **The contract's head line** says the package's layer is "the source repository's at `6f7f291`
   (`PROVENANCE.md`)", not SGK's, since the document names no client (as 01's internalised
   docstrings do). **IMPLEMENTATION CHOICE.**
5. **The client imports no `ray`.** `build.py`'s helpers resolve references with the stand-in's own
   `standin_get`, so a helper called outside `StandinCluster.active()` cannot start Ray (the prompt
   allows `ray` only where a factory needs it; none does). **IMPLEMENTATION CHOICE.**
6. **`build.open_pool`** passes the registry's `read_table_config` and `serial_batch_sizes`, which
   SGK's `StandinCluster.open_pool` does not, and which D-split may not add. **IMPLEMENTATION
   CHOICE.**
7. **The check**: `NEW_FILES` became `NO_SOURCE`; a declared no-source file that is missing also
   fails; D-fix skips f-strings, as D-str does; D-split runs before D-imp; the two blank lines the
   cut leaves are D-fmt (−2/+0), not D-split. **IMPLEMENTATION CHOICE.**
8. **(k) and (n)**, the orchestrator's additions. **IMPLEMENTATION CHOICE** (orchestrator's).
9. **Two issues opened, not one**: `[02-no-test-reaches-revalidate]` ((k), as the notes expect) and
   `[02-an-unsupplied-sharded-table-raises-keyerror]` (§5 item 1), under `CLAUDE.md` rule 4. The
   index is **8**, not 7. **IMPLEMENTATION CHOICE.**
10. **The prose issue's count is 104, not 102.** The moved comment is one line; the stand-in pool's
    docstring, ported unchanged, brings two more lines the issue's pattern matches (`:4`, `:5`) and
    seven SGK-campaign lines it does not (§5 item 5). **STRUCTURALLY REQUIRED.**
11. **Facts that differed from the notes or the prompt:** `QCD_Cosmology` is not in SI's registry
    (§1.2); `validate_on_startup` is read for replicated classes too, by the pool's prune
    (`SQL/ShardedPool.py:2094-2103`, `:2314-2347`), not only for sharded ones (the notes say the
    prune at open applies only to sharded classes; that is the *actor's* prune). Recorded; no
    effect on the work beyond the contract's wording.

No UNINTENDED DRIFT was found.

## 3. The re-fixtured lines (U8)

By `grep -nw` at `737ad6e`, 15 lines, each changed only inside a plain string literal, as whole
identifiers (`wavenumber` → `keypoint`, `wavenumber_serial` → `keypoint_serial`, `GkSource` →
`Sample`), by a `tokenize` script; no test name, class, other assertion or control flow changed:

- `tests/shard_store_fixtures.py:25`, `:26`, `:27` (`KEY_TYPE`, `REPLICATED`, `SHARDED`);
- `tests/test_shard_key_audit_copy.py:43`, `:45` (the key table's DDL and insert), `:104` (the
  expected `"'keypoint' table (shard #0) row count: 2"`, echoing the fixture's key type);
- `tests/test_shard_key_audit_refusals.py:7` (docstring), `:65`, `:66`, `:184`, `:186`, `:192`
  (`"keypoint_serial"`; its comment unchanged), `:205`, `:227`, `:229` (the expected
  `"does not contain the 'keypoint' table"`).

`tools/shard_key_audit.py:188` (`e.g. "wavenumber"`), a comment, is unchanged and moves to
`[01-package-prose-names-sgks-layout]`.

## 4. Verification performed

### 4.1 The contract against the planner's survey

Measured from the package (`grep`, `ast`, and probes in the scratchpad), at this tree, whose files
outside `tests/` equal `8bc60a5`'s.

| Item | Survey | Measured |
|---|---|---|
| `ShardedPool.__init__` | 16: 6 / 8 / 2 | **16**: 6 positional required, 8 defaulted, `factories` (keyword, required) and `serial_batch_sizes` (keyword, defaulted) |
| `register()` keys | 9, `SQL/schema.py:95-180` | **9**, read at `:108`, `:117`, `:125`, `:137`, `:144`, `:163`, `:203`, `:228`, `:265`; plus the `None` return (`:98`) |
| Hooks | 5 abstract + 3 defaulted + 2 undeclared | **10**, the same; called at the lines of contract §3 |
| `InventorySpec` / `Parent` / `ParentSet` fields | 6 / (count) / (incl. `cross_shard`) | **6 / 6 / 3**; `cross_shard` is `Parent`'s, as the notes say |
| Layer-owned tables | `version`, `store_tag`, `tag_serial` | the same; `version` is required (without it the open raises `OperationalError: no such table: version`, probed), `store_tag` optional (any tagged class needs it) |
| Other entry points | `open_read_only`, `read_inventory` | also `build_schema`, `dependent_tables`, `inventory_specs`, `inventory_classes`, `read_records`, `drop_order` (tables only) and `ShardedPool.factories` |

Behaviours measured by probe: an unknown `stepping` string prints the warning and adds no column; a
factory column named `serial` raises `DuplicateColumnError`; `version: True` with no version table
cannot be created (`NoReferencedTableError`); a store recording a sharded table the constructor
lacks raises `KeyError('…')` at `SQL/ShardedPool.py:1015` (§5 item 1). `job_name` is kept and read
by nothing (`:138`).

**Every contract item mapped to the client and a test** (tests of `test_neutral_client`; `Cov` =
`TestCoverageByDeclaration`, `RT` = `TestRoundTrip`, `Reg` = `TestTheRegistry`):

| Contract item | Neutral client | Exercised by |
|---|---|---|
| ctor `version_label`, `db_name`, `shards`, `factories` | `StandinCluster.open_pool` / `build.open_pool` | every `RT` test (via `build_store`) |
| ctor `ShardKeyType`, `ShardKeyStoreIdGetter` | `keypoint`, `shard_key_store_id` (keypoint and proxy) | `Cov.test_the_shard_key_and_its_proxy`; `RT` (sharded gets, stores, `read_batch`) |
| ctor `replicated_tables`, `sharded_tables` | the registry's | `Cov.test_the_layer_owned_tables`; `RT.test_a_reopen_…` (compared list) |
| ctor `read_table_config` | both `tables_arg` values | `Cov.test_read_table_config_takes_tables_arg_both_ways`; `RT.test_every_class_reads_back_…` |
| ctor `serial_batch_sizes` | `registry.serial_batch_sizes` | every `RT` test (given by `build.open_pool`) |
| ctor `drop_tables` | `tables_to_drop` | `Reg.test_dependent_tables_accepts_each_group_as_declared` (the pool's refusal reads the same derivation) |
| ctor `read_only`, `prune_unvalidated`, `timeout`, `profile_agent`, `job_name` | not given (defaulted) | — (03's `test_read_only_pool` and `test_prune_at_open` give them) |
| `register()`: all 9 keys, each form, and `None` | §1.1 | `Cov.test_every_register_key_is_declared_by_some_factory`, `Cov.test_each_form_of_a_registration_is_in_use` |
| `owner_column`, `monotone_flags`, `validated_column` (replicated only) | `GadgetPart`, `keypoint`, `Gadget` | `Cov.test_the_replicated_only_declarations_are_where_the_pool_reads_them` (through the pool's own `_replicated_table_specs` and `_unit_tables`) |
| `validate_on_startup` (both) | `Gadget`, `Sample` | `Cov.test_validate_on_startup_is_declared_by_a_replicated_and_a_sharded_class`; `RT` (actors report at reopen) |
| hooks `register`, `build`, `store`, `validate`, `validate_on_startup` | every factory; `store`/`validate` on both kinds | `Cov.test_every_hook_is_defined_…`; `RT` (all called by `build_store`) |
| hooks `revalidate`, `owned_serials` | `Gadget` | `Cov` (defined); `owned_serials` called by every replicated store of `build_store`; `revalidate` reached by **no** test (§4.4 (k)) |
| hook `inventory_spec` | 9 classes | `Cov.test_every_declaration_field_is_in_use`, `Cov.test_the_inventory_derives_an_order_…`; `RT.test_the_reader_and_the_inventory_…` |
| hooks `read_batch`, `read_table` | `Sample`; `keypoint`, `dial_setting` | `RT.test_every_class_reads_back_through_a_reopened_pool` |
| `InventorySpec` (6), `Parent` (6), `ParentSet` (3) fields | §1.1 | `Cov.test_every_declaration_field_is_in_use` (fields counted); `RT.test_the_reader_and_the_inventory_…` |
| `version`, `store_tag`, `tag_serial`, a replicated class's tag table | `version`, `store_tag`, `Gadget_tags`, `Sample_tags` | `Cov.test_the_layer_owned_tables`; `RT.test_build_store_writes_every_class` |
| object: class name, `DatastoreObject`, `_new_insert`/`_updated`, `serial` in payload, shard key attribute, `ShardKeyType` instance, inserter, picklable | `objects.py`, `factories.py` | `RT.test_build_store_writes_every_class` (replicated rows identical on every shard, the flag update replicated); `RT.test_a_replicated_get_is_written_on_the_pinned_controller_then_copied` |
| entry points `open_read_only`, `read_inventory`, `build_schema`, `dependent_tables`, `inventory_specs`, `inventory_classes` | the registry | `RT.test_the_reader_and_the_inventory_…`; `Cov`; `Reg` |

Every item is covered by the client; every one but `revalidate`'s call and the defaulted constructor
arguments is reached by a test here.

### 4.2 The suite (§3.1)

`./venv/bin/python -m unittest discover -s datastorekit/tests -t .`, in the foreground, output to
the scratchpad: **before `Ran 90 tests … OK`; after `Ran 109 tests in 6.540s` / `OK`.** The 90
names of `737ad6e` (listed from an exported tree of it) are all present after, unchanged; the 19
new:

- `TestCoverageByDeclaration` (10): `test_every_register_key_is_declared_by_some_factory`,
  `test_each_form_of_a_registration_is_in_use`,
  `test_the_replicated_only_declarations_are_where_the_pool_reads_them`,
  `test_validate_on_startup_is_declared_by_a_replicated_and_a_sharded_class`,
  `test_every_hook_is_defined_by_a_factory_of_the_kind_it_is_called_for`,
  `test_read_table_config_takes_tables_arg_both_ways`, `test_every_declaration_field_is_in_use`,
  `test_the_inventory_derives_an_order_from_the_declarations`, `test_the_shard_key_and_its_proxy`,
  `test_the_layer_owned_tables`;
- `TestRoundTrip` (5): `test_build_store_writes_every_class`,
  `test_a_reopen_passes_the_check_at_open_repairs_nothing_and_writes_nothing` (every file's
  checksum unchanged), `test_every_class_reads_back_through_a_reopened_pool`,
  `test_the_reader_and_the_inventory_read_every_class`,
  `test_a_replicated_get_is_written_on_the_pinned_controller_then_copied`;
- `TestTheRegistry` (4): `test_the_registry_exports_exactly_the_nine_names`,
  `test_tables_to_drop_gives_each_groups_tables`,
  `test_dependent_tables_accepts_each_group_as_declared`,
  `test_an_undeclared_name_is_refused_by_dependent_tables`.

### 4.3 The equivalence check (§3.2)

`./venv/bin/python docs/extraction/compare_with_source.py`, exit **0**. Its whole output:

```
source:  /Users/ds283/Documents/Code/SecondaryGWKit at 6f7f291e857265e429f5d6f810124fd3bf57ce55 Record the orchestrator's review of datastore-generic-followup prompt 03
package: /Users/ds283/Documents/Code/DatastoreKit/datastorekit
black:   25.1.0

Lines per file and class, as -source/+package: the source lines a class changed or
removed, and the package lines it accounts for.

file                                                        D-imp         D-str        D-tool        D-root         D-fix       D-split         D-int         D-fmt  UNCLASSIFIED
datastorekit/__init__.py                                        .             .             .             .             .             .             .             .             .
datastorekit/object.py                                          .             .             .             .             .             .             .             .             .
datastorekit/contract.py                                        .             .             .             .             .             .             .             .             .
datastorekit/replication.py                                     .             .             .             .             .             .             .             .             .
datastorekit/shard_paths.py                                     .             .             .             .             .             .             .             .             .
datastorekit/store_reader.py                                -3/+3             .             .             .             .             .             .             .             .
datastorekit/store_inventory.py                             -2/+2             .             .             .             .             .             .             .             .
datastorekit/SQL/__init__.py                                    .             .             .             .             .             .             .             .             .
datastorekit/SQL/schema.py                                  -2/+2             .             .             .             .             .             .             .             .
datastorekit/SQL/ShardedPool.py                           -13/+13             .             .             .             .             .             .             .             .
datastorekit/SQL/Datastore.py                               -9/+9             .             .             .             .             .             .             .             .
datastorekit/SQL/ClientPool.py                              -1/+1             .             .             .             .             .             .             .             .
datastorekit/SQL/SerialPoolBroker.py                            .             .             .             .             .             .             .             .             .
datastorekit/SQL/ProfileAgent.py                            -2/+2             .             .             .             .             .             .             .             .
datastorekit/SQL/factory_base.py                                .             .             .             .             .             .             .             .             .
datastorekit/tools/__init__.py                                  .             .             .             .             .             .             .             .             .
datastorekit/tools/sharded_store.py                         -1/+1             .         -7/+3             .             .             .             .             .             .
datastorekit/tools/shard_key_audit.py                       -1/+1             .         -5/+1             .             .             .             .             .             .
datastorekit/defaults.py                                        .             .             .             .             .             .       -202/+5             .             .
datastorekit/_timing.py                                         .             .             .             .             .             .        -20/+6             .             .
datastorekit/tests/__init__.py                                  .             .             .             .             .             .             .             .             .
datastorekit/tests/shard_store_fixtures.py                  -2/+2             .             .             .         -3/+3             .             .             .             .
datastorekit/tests/test_shard_paths.py                      -1/+1         -2/+2             .             .             .             .             .             .             .
datastorekit/tests/test_shard_file_name.py                  -2/+2             .             .         -8/+6             .             .             .             .             .
datastorekit/tests/test_shardedpool_shard_paths.py          -1/+1             .             .             .             .             .             .             .             .
datastorekit/tests/test_copy_move_store.py                  -3/+3             .             .             .             .             .             .             .             .
datastorekit/tests/test_delete_store.py                     -3/+3         -1/+1             .             .             .             .             .             .             .
datastorekit/tests/test_sharded_store_script.py             -2/+2             .         -5/+3             .             .             .             .         -1/+0             .
datastorekit/tests/test_shard_key_audit_copy.py             -1/+1         -1/+1        -6/+14             .         -3/+3             .             .             .             .
datastorekit/tests/test_shard_key_audit_refusals.py         -1/+1             .         -3/+1             .         -9/+9             .             .             .             .
datastorekit/tests/standin_pool.py                              .         -3/+3             .             .             .       -169/+8             .         -2/+0             .
total                                                     -50/+50         -7/+7       -26/+22         -8/+6       -15/+15       -169/+8      -222/+11         -3/+0         -0/+0

files compared: 31
files with no source, declared: 7
not compared (no source, declared): datastorekit/tests/client/__init__.py
not compared (no source, declared): datastorekit/tests/client/build.py
not compared (no source, declared): datastorekit/tests/client/factories.py
not compared (no source, declared): datastorekit/tests/client/objects.py
not compared (no source, declared): datastorekit/tests/client/registry.py
not compared (no source, declared): datastorekit/tests/test_neutral_client.py
not compared (no source, declared): datastorekit/tests/test_package_imports.py

Lines listed: D-fmt always, UNCLASSIFIED always, the rest with --show.
datastorekit/tests/test_sharded_store_script.py (from Datastore/tests/test_sharded_store_script.py):
  D-fmt         source line removed or changed  Datastore/tests/test_sharded_store_script.py:27: 
datastorekit/tests/standin_pool.py (from Datastore/tests/standin_pool.py):
  D-fmt         source line removed or changed  Datastore/tests/standin_pool.py:419: 
  D-fmt         source line removed or changed  Datastore/tests/standin_pool.py:420: 

OK: every differing line is classified, and every file is accounted for
```

Per class over the 31 files (`-source/+package`): D-imp −50/+50, D-str −7/+7, D-tool −26/+22,
D-root −8/+6, **D-fix −15/+15**, **D-split −169/+8**, D-int −222/+11, D-fmt −3/+0, UNCLASSIFIED 0.
01's 30 files have 01's counts, except D-fix in the three re-fixtured files (3, 3, 9). The stand-in
pool: D-str −3/+3 (the three module paths); D-split −169/+8 (161 lines cut from the banner, `:421`,
to `:581`; in the two methods, 2 × 4 lines: the two import lines that change and the getter's name
in the import and in the call); D-fmt −2/+0 (`:419-420`, the blank lines before the cut). 7 files
declared with no source.

### 4.4 Imports from a clean shell (§3.3)

From `…/scratchpad/agent02/elsewhere`, in `env -u PYTHONPATH bash --noprofile --norc`:

```
PYTHONPATH=unset cwd=/private/tmp/claude-35086/…/scratchpad/agent02/elsewhere
import ok /Users/ds283/Documents/Code/DatastoreKit/datastorekit/tests/client/registry.py /Users/ds283/Documents/Code/DatastoreKit/datastorekit/tests/standin_pool.py
ray.is_initialized() = False
exit 0
```

### 4.5 The deliberate-breakage record (§3.4)

Each was checked with `git apply --check` and `git apply -R --check`, applied, run, and reverted
with `git apply -R`, in `bash`, against the staged tree this commit records; `git diff` and the
untracked list were empty after each. None is committed. No Ray process was up at any point.

**(a)-(e), 01's, replayed** byte for byte from log 01 §4.4 (extracted from its ```` ```diff ````
blocks). Each check exits **1**, naming the same lines as in 01:
- (a) `UNCLASSIFIED … ShardedPool.py:953: num_config = 1`; (b) `… schema.py:52: from
  datastorekit.replication import ReadOnlyMiss`; (c) `… Datastore.py:155: f"datastorekit.set_version
  …"`; (d) `… Datastore/shard_paths.py:101: name = _require_bare_name(stored, stored)`; (e) `…
  shard_key_audit.py:19: … datastorekit/shard_paths.py …`.

**(f) `wavenumber` → `keypoint` in a comment of `tools/shard_key_audit.py`**, a file D-fix does not cover — check exits **1**:

```diff
diff --git a/datastorekit/tools/shard_key_audit.py b/datastorekit/tools/shard_key_audit.py
index 96b9deb..8656dc5 100644
--- a/datastorekit/tools/shard_key_audit.py
+++ b/datastorekit/tools/shard_key_audit.py
@@ -185,7 +185,7 @@ def main(argv: List[str]) -> int:
     print(f">> shard_keys row count: {len(key_serials)}")
     print(f">> per-shard key distribution: {distribution}")
 
-    # Cross-file check against the actual shard-key table (e.g. "wavenumber"),
+    # Cross-file check against the actual shard-key table (e.g. "keypoint"),
     # which lives in the replicated tables inside each shard database, not in
     # the primary file. Best-effort: attach one shard file read-only.
     cross_file_done = False
```
```
  UNCLASSIFIED  expected, not in the package  tools/shard_key_audit.py:192:     # Cross-file check against the actual shard-key table (e.g. "wavenumber"),
  UNCLASSIFIED  in the package, not expected  datastorekit/tools/shard_key_audit.py:188:     # Cross-file check against the actual shard-key table (e.g. "keypoint"),
FAIL: 2 line(s) unclassified, or a file missing
```

**(g) one extra line in the ported half of `standin_pool.py`** — check exits **1**:

```diff
diff --git a/datastorekit/tests/standin_pool.py b/datastorekit/tests/standin_pool.py
index 7aa4d27..b999fd1 100644
--- a/datastorekit/tests/standin_pool.py
+++ b/datastorekit/tests/standin_pool.py
@@ -53,6 +53,7 @@ class StandinActorDied(Exception):
 
 
 def _copy(x):
+    # one extra line in the ported half
     return pickle.loads(pickle.dumps(x))
 
 
```
```
  UNCLASSIFIED  in the package, not expected  datastorekit/tests/standin_pool.py:56:     # one extra line in the ported half
FAIL: 1 line(s) unclassified, or a file missing
```

**(h) an empty `datastorekit/stray.py`** — check exits **1**, as NOT ACCOUNTED FOR:

```diff
diff --git a/datastorekit/stray.py b/datastorekit/stray.py
new file mode 100644
index 0000000..e69de29
```
```
not compared (NOT ACCOUNTED FOR): datastorekit/stray.py
FAIL: 1 file(s) under datastorekit/ not accounted for
```

**(i) `keypoint` written outside a string literal of `test_shard_key_audit_refusals.py`** (a local variable renamed) — check exits **1**:

```diff
diff --git a/datastorekit/tests/test_shard_key_audit_refusals.py b/datastorekit/tests/test_shard_key_audit_refusals.py
index 68ceb5e..85baf4e 100644
--- a/datastorekit/tests/test_shard_key_audit_refusals.py
+++ b/datastorekit/tests/test_shard_key_audit_refusals.py
@@ -80,12 +80,12 @@ class TestTheAuditRefuses(unittest.TestCase):
     def a_current_store(self, directory: str) -> Path:
         """A hand-built primary with bare-name records, a key in shard 0 and a shard_key_config
         row: the shape the tool audits to "VERDICT: OK"."""
-        primary = self.root / directory / "store.sqlite"
-        write_hand_built_primary(primary, dict(enumerate(NAMES)), shard_keys=[(1, 0)])
+        keypoint = self.root / directory / "store.sqlite"
+        write_hand_built_primary(keypoint, dict(enumerate(NAMES)), shard_keys=[(1, 0)])
         for name in NAMES[1:]:
-            write_placeholder(primary.parent / name)
-        _write_key_shard(primary.parent / NAMES[0])
-        return primary
+            write_placeholder(keypoint.parent / name)
+        _write_key_shard(keypoint.parent / NAMES[0])
+        return keypoint
 
     def audit(self, primary: Path):
         return subprocess.run(
```
```
  UNCLASSIFIED  expected, not in the package  Datastore/tests/test_shard_key_audit_refusals.py:85:         primary = self.root / directory / "store.sqlite"
  UNCLASSIFIED  expected, not in the package  Datastore/tests/test_shard_key_audit_refusals.py:86:         write_hand_built_primary(primary, dict(enumerate(NAMES)), shard_keys=[(1, 0)])
  UNCLASSIFIED  in the package, not expected  datastorekit/tests/test_shard_key_audit_refusals.py:83:         keypoint = self.root / directory / "store.sqlite"
  UNCLASSIFIED  in the package, not expected  datastorekit/tests/test_shard_key_audit_refusals.py:84:         write_hand_built_primary(keypoint, dict(enumerate(NAMES)), shard_keys=[(1, 0)])
  UNCLASSIFIED  expected, not in the package  Datastore/tests/test_shard_key_audit_refusals.py:88:             write_placeholder(primary.parent / name)
  UNCLASSIFIED  expected, not in the package  Datastore/tests/test_shard_key_audit_refusals.py:89:         _write_key_shard(primary.parent / NAMES[0])
  UNCLASSIFIED  expected, not in the package  Datastore/tests/test_shard_key_audit_refusals.py:90:         return primary
  UNCLASSIFIED  in the package, not expected  datastorekit/tests/test_shard_key_audit_refusals.py:86:             write_placeholder(keypoint.parent / name)
  UNCLASSIFIED  in the package, not expected  datastorekit/tests/test_shard_key_audit_refusals.py:87:         _write_key_shard(keypoint.parent / NAMES[0])
  UNCLASSIFIED  in the package, not expected  datastorekit/tests/test_shard_key_audit_refusals.py:88:         return keypoint
FAIL: 10 line(s) unclassified, or a file missing
```

**(j) `monotone_flags` removed from `keypoint`'s factory** — `Ran 109 tests` / `FAILED (failures=2)`: `test_every_register_key_is_declared_by_some_factory` (`'monotone_flags'` declared by no factory) and `test_the_replicated_only_declarations_are_where_the_pool_reads_them` (`{} != {'keypoint': ('kp_marked', 'kp_flagged')}`):

```diff
diff --git a/datastorekit/tests/client/factories.py b/datastorekit/tests/client/factories.py
index 9c17a86..ab18b3c 100644
--- a/datastorekit/tests/client/factories.py
+++ b/datastorekit/tests/client/factories.py
@@ -173,7 +173,6 @@ class keypoint_factory(SQLAFactoryBase):
                 sqla.Column("kp_marked", sqla.Boolean, default=False, nullable=False),
                 sqla.Column("kp_flagged", sqla.Boolean, default=False, nullable=False),
             ],
-            "monotone_flags": ("kp_marked", "kp_flagged"),
         }
 
     @staticmethod
```

**(k) `Gadget`'s `revalidate` returns without writing** (the replicated owner's, per correction 1) — `Ran 109 tests` / `OK`. **No test fails**: `revalidate` is called only by the check at open after an interrupted replicated validate (`SQL/ShardedPool.py:1992`), and no test here makes one. A finding for 03: `[02-no-test-reaches-revalidate]`.

```diff
diff --git a/datastorekit/tests/client/factories.py b/datastorekit/tests/client/factories.py
index 9c17a86..92d48a1 100644
--- a/datastorekit/tests/client/factories.py
+++ b/datastorekit/tests/client/factories.py
@@ -748,7 +748,7 @@ class Gadget_factory(SQLAFactoryBase):
 
     @staticmethod
     def revalidate(serial, conn, table, tables) -> bool:
-        return Gadget_factory._validate_row(serial, conn, table, tables)
+        return True
 
     @staticmethod
     def owned_serials(obj) -> Optional[List[Optional[int]]]:
```

**(l) the audit's row-count message prints the literal `'wavenumber'`** (`tools/shard_key_audit.py:220`) — `Ran 109 tests` / `FAILED (failures=1)`: `test_shard_key_audit_copy.TestAuditOfACopiedStore.test_audit_of_the_copy_attaches_the_copys_shard`, `"'keypoint' table (shard #0) row count: 2" not found in "…>> 'wavenumber' table (shard #0) row count: 2…"`. Before §2.4 the test expected `'wavenumber'`, and this mutation would have passed:

```diff
diff --git a/datastorekit/tools/shard_key_audit.py b/datastorekit/tools/shard_key_audit.py
index 96b9deb..2dc1ca0 100644
--- a/datastorekit/tools/shard_key_audit.py
+++ b/datastorekit/tools/shard_key_audit.py
@@ -217,7 +217,7 @@ def main(argv: List[str]) -> int:
                     unassigned = sorted(key_table_serials - shard_key_serials)
 
                     print(
-                        f">> '{key_type}' table (shard #{shard_serial}) row count: "
+                        f">> 'wavenumber' table (shard #{shard_serial}) row count: "
                         f"{len(key_table_serials)}"
                     )
                     if orphaned:
```

**(m) `_StandinRandom.randrange` ignores the pinned controller** (returns index 0) — `Ran 109 tests` / `FAILED (failures=1)`: `test_neutral_client.TestRoundTrip.test_a_replicated_get_is_written_on_the_pinned_controller_then_copied`, `Tuples differ: (2, 'object_get', 'dial_setting', […]) != (0, 'object_get', 'dial_setting', […])`. It cannot start Ray, and the `ray.get` patch is untouched:

```diff
diff --git a/datastorekit/tests/standin_pool.py b/datastorekit/tests/standin_pool.py
index 7aa4d27..9d5d59e 100644
--- a/datastorekit/tests/standin_pool.py
+++ b/datastorekit/tests/standin_pool.py
@@ -203,7 +203,7 @@ class _StandinRandom:
         if cluster.controller is None or cluster.pool is None:
             return _random.randrange(n)
         # ShardedPool swaps entry i of list(self._shards.keys()) to the end and pops it
-        return list(cluster.pool._shards.keys()).index(cluster.controller)
+        return 0
 
 
 class StandinCluster:
```

**(n) 01's `key_id` diff, replayed** (log 01 §4.4, `SQL/ShardedPool.py:3561`): **`Ran 109 tests` /
`OK`. No test fails**, and no `!! _assign_shard_keys MISMATCH` is printed. `build_store` does reach
`_assign_shard_keys`, but SQLAlchemy ignores the unknown `key_id` key of the parameters, so
`key_serial` is autoincremented; the three keypoints are assigned in serial order from 1, so the
autoincremented `key_serial` equals each `store_id` and the saved map equals the one in memory.
Recorded here only, as the notes direct; 03 still owns
`[01-no-ported-test-pins-the-shard-key-assignment]`, and a test that pins it must assign keys out
of serial order (§5 item 4).

### 4.6 `black` (§3.5)

`./venv/bin/black --check datastorekit docs/extraction` (25.1.0) → `39 files would be left
unchanged.`

## 5. Observations not acted on

1. **A sharded table the store records and the constructor lacks raises `KeyError`.**
   `_read_shard_data` indexes `self._sharded_tables[row.table]` (`SQL/ShardedPool.py:1015`) before
   it reaches the `RuntimeError` and the printed list meant for that case (`:1022-1045`), so the
   open is refused with a bare `KeyError('<table>')` (probed with `shard_store_fixtures`). The
   refusal still happens; its message does not. Opened as
   `[02-an-unsupplied-sharded-table-raises-keyerror]`; not fixed (README §5 rule 8).
2. **`revalidate` is reached by no test** ((k)). Its one call site is `_recompute_validated`
   (`SQL/ShardedPool.py:1992`), after an interrupted replicated validate. Opened as
   `[02-no-test-reaches-revalidate]`, for 03.
3. **`job_name` is read by nothing** (`SQL/ShardedPool.py:138`). Recorded in the contract.
4. **The `key_id` binding fails no test here** ((n)): SQLAlchemy drops the unknown key silently,
   and keys assigned in serial order from 1 hide it. Left to 03's issue.
5. **The stand-in pool's prose names SGK's layout and campaigns**, unchanged under D-split's rule:
   `:4-5` (`docs/datastore-integrity-audit/…`, `prompts/datastore-integrity`), and `:2` (`var/`),
   `:195`, `:225`, `:252` (`a3-v2-readiness prompt 02`), `:286` ("the production table lists"),
   `:314`, `:397` ("prompt 02"). Added to `[01-package-prose-names-sgks-layout]`.
6. **CPBH's `replicated_tables` names `LambdaCDM`**, which its registry does not declare (§1.2). A
   client's matter, for its adoption checklist (07).
7. **The contract's measured behaviours** that look like defects but are as designed are recorded
   in it, not here: an unknown `stepping` string is ignored with a warning; replication silently
   skipped for a get answer without `_new_insert`/`_updated`, caught only at the next open.

## 6. Issues

- **Closed:** `[01-ported-tests-use-sgk-table-names]` (§3).
- **Opened:** `[02-no-test-reaches-revalidate]`, `[02-an-unsupplied-sharded-table-raises-keyerror]`.
- **Changed:** `[01-package-prose-names-sgks-layout]`: 101 → 104 lines, 19 → 20 files (the moved
  comment; the stand-in pool's two lines), and the stand-in pool's seven other lines noted.

The index is at **8 open**: 4 on this board, 4 inherited.

## 7. State handed to the next prompt

- `HEAD` is this commit. The tree is clean; `venv/` unchanged.
- The suite: **109** (`Ran 109 tests … OK`). 03 records 109 as its "before".
- `compare_with_source.py` exits 0 over 31 files, with 7 declared no-source files. A file 03 or 04
  ports from SGK goes into `FILES`; a new file with no source into `NO_SOURCE`; any other fails the
  check.
- The interfaces of README §4 "After 02": `docs/client-contract.md`, `datastorekit/tests/client/`,
  `datastorekit/tests/standin_pool.py`, with the entry points of §1.4.
- For 03: `[01-no-ported-test-pins-the-shard-key-assignment]` (with §4.5 (n)'s finding) and
  `[02-no-test-reaches-revalidate]`; the role table (§1.3). 03 and 04 both edit the stand-in pool
  and must not run concurrently.
- For 04: the drop groups (§1.1, §2 item 3); the vocabulary of §1.2; `schema_description` and
  `real_store_fixtures`' helpers to port.
