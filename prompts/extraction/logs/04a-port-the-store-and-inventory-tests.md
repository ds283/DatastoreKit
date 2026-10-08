# Log 04a — port the store and inventory tests

**Subject:** Port the store, reader, inventory and schema tests · **Commit:** `7ceed25` ·
**Date:** 2026-10-08 · **Model:** Claude Opus 5.5 · **Result:** landed.

SGK's five modules now run in `datastorekit/tests/` under their names, on the neutral client and a
neutral hand-built store: `test_store_inventory` (42), `test_store_schema` (13), `test_store_reader`
(15), `test_foreign_key_check` (8) and `test_schema_builder` (7). So do the two fixtures they
import, `real_store_fixtures` (on neutral rows) and `schema_description`. The neutral schema
witness is `datastorekit/tests/data/schema_at_extraction-04a.json`.

The neutral client has U15's sharded family: `Trace`, `Trace_tags`, `TraceStep`, `Weave`,
`Weave_tags` and `Weave_members`. `Gadget`'s validate now warns when a Gadget does not validate, and
`Sample`'s `inventory_spec` no longer declares `validated` (U18). U19 adds `traces` to one drop
list of 03a's, and U20 points the witness at the registry's classes with a table.

`compare_ported_tests.py` finds fifteen modules equal to SGK's in tests, classes, bases and
assertion skeletons, and `compare_with_source.py` accounts for the seven as `PORTED`.
`Ran 353 tests … OK` (268 before). `[01-package-prose-names-sgks-layout]` is re-measured at 146
lines in 35 files. No issue was opened or closed, and the index stays at 6.

Prompt: [`../04a-port-the-store-and-inventory-tests.md`](../04a-port-the-store-and-inventory-tests.md),
with the orchestrator's dispatch note:
- the dispatch: four corrections and five additions;
- the addendum after the agent's first stop: correction 5 (U19);
- the addendum after the second stop: corrections 6 and 7 (U20, U21).

The work stopped twice for the user (§2 items 5 and 6). It was resumed each time from the
uncommitted tree, and one commit was made, at the end.

## 1. What shipped

- **Five ported modules**, each SGK's at `6f7f291` with only the changes of 03a §2.1:
  - `datastorekit/tests/test_store_inventory.py`
  - `test_store_schema.py`
  - `test_store_reader.py`
  - `test_foreign_key_check.py`
  - `test_schema_builder.py`

  Every class and method keeps its name (no R-name).
- **Two ported fixtures**, `datastorekit/tests/real_store_fixtures.py` and
  `schema_description.py`, with SGK's public names and signatures (§1.4).
- **The witness**, `datastorekit/tests/data/schema_at_extraction-04a.json` (§1.7).
- **The client additions (U15, U18)** in `client/objects.py`, `factories.py`, `registry.py` and
  `build.py` (§1.3).
- **U19**: `"traces"` added to one drop list of `test_reconcile_at_open.py` (§1.3).
- **The literals of `test_neutral_client.py`, and the client cells of `docs/client-contract.md`**
  (§1.3).
- **`docs/extraction/compare_ported_tests.py`**: `PORTED` gains the seven pairs. `NAME_MAP` and
  everything else are unchanged.
- **`compare_with_source.py`**: `FILES` gains the same seven as `PORTED`, and `NO_SOURCE` is
  unchanged.
- **The records**:
  - this log;
  - the board (header, §1's row, §3);
  - `docs/OPEN_ISSUES.md`;
  - `prompts/INDEX.md`.

### 1.1 The map as used (§2.2)

Each row is the planner's unless it says otherwise. Columns and payload keys move with their table
(R-map); values move by R-value.

| SGK | Used for | Neutral, as used | Changed from the planner's row? |
|---|---|---|---|
| `wavenumber` (`k_inv_Mpc`; `source`, `response`) | the shard key; a float identity; the OR-flags | `keypoint` (`kp_position`; `kp_marked`, `kp_flagged`) | no |
| `redshift` | a second flagged leaf | `keypoint`. The one site with two flagged classes is `NON_IDENTITY`'s two OR-flag entries (`redshift 1 source`, `wavenumber 1 response`). They become `keypoint 1 kp_marked` and `keypoint 2 kp_flagged`: two rows, one class | no |
| `tolerance` (`log10_tol`) | a replicated leaf with a float identity, three rows, no dependents | `routing_rule` (`rule_threshold`; -5.0, -7.0, -9.0 kept) everywhere in `test_store_inventory` and `test_store_schema`. **`gauge_setting`** in `TestStandinStore`, whose two gets need only "a replicated leaf" (exponents 10, 9, as 03b's) | no |
| `LambdaCDM`, `QCD_Cosmology` | the polymorphic parent's two types | `dial_setting` (kind 1), `knob_setting` (kind 2), through `FRAME_TYPES`. Dial 1 and knob 1 share serial 1 | no |
| `cosmology_type`, `cosmology_serial` | the type column and the reference | `frame_kind`, `frame_serial` | no |
| `IntegrationSolver`, `GkSourcePolicy`, `QuadSourcePolicy` | replicated leaves | `GkSourcePolicy` → `routing_rule` (in `test_store_schema`, a versioned replicated class a drop leaves out, and in `TestStandinStore`). `IntegrationSolver` and `QuadSourcePolicy` have no site in the five modules (their rows were SGK's fixture's). `gauge_setting` holds rows 1 and 2 in the full store, as `IntegrationSolver` did | by role |
| `wavenumber_exit_time` | the shard key's proxy; a polymorphic replicated referrer | `keypoint_alias` as the proxy, including `test_the_last_bit_of_k_changes_the_records`. **`Gadget`** in `test_an_unknown_cosmology_type`, which needs a *replicated* polymorphic referrer; `Trace` is sharded | **yes**: `Gadget`, not `Trace`, for the unknown type |
| `BackgroundModel` (+`_tags`, `Value`) | replicated, tagged, validated, with values and a polymorphic parent | `Gadget` (+`Gadget_tags`, `GadgetPart`) | no |
| `TkNumericIntegration` (+`_tags`, `Value`) | sharded, tagged, validated, with values | `Trace` (+`Trace_tags`, `TraceStep`); `stop_Tprime` → `step_count` (hazard 6) | no |
| `GkSource` | a sharded tagged parent of a sharded child | `Trace` as the parent (`test_a_tagged_parents_digest_covers_its_tags`). In `test_store_schema` and `test_store_reader`, which need only "a table", `GkSource` → `Sample` (deviation 19) | by role |
| `GkSource_parents` | member rows with serials and nullable members | `Weave_members` (`IDENTITY["Weave"]["strands"]`). In `test_store_schema`'s reversed pair, `Sample_members` (deviation 19) | by role |
| `GkWKBIntegration.numeric` | a nullable key parent | `Weave.anchor` (None in the full store). `Sample.anchor` is set on every full-store Sample (deviation 11) | — |
| `OneLoopIntegral` (+`_tags`) | tagged, no validated column, one record, no dependents, sharing serial 1 | `Weave` (+`Weave_tags`), sharing serial 1 with `Trace` 1 | no |
| `QuadSourceIntegral` | the class most tests address | by role: **`Sample`** where it is the class with a cross-shard parent and no dependents (`test_resolve_names_every_parent`, `test_adding_a_tag…`, `test_different_serial_assignments`, `test_timestamps`, `TestReadOnlyAndNoRay`, `test_store_schema`'s missing tag table). **`Trace`** where it shares serial 1 with the `OneLoopIntegral` role (`test_oneloop_tags…`), and in all four `TestDuplicates` tests (the note's preference) | by role |
| `QuadSource` | validated, tagged, unvalidated rows | the unvalidated-rows tuple: `Gadget`, `Trace` (U18); in `test_foreign_key_check`, the class with the same-shard foreign key: the added `Sample` and its `Sample_members` row | by role |
| `GkSourcePolicyData` | the child keyed on a tagged parent; a sharded-to-replicated foreign key | `Weave` (keyed on `trace`); in `test_foreign_key_check`, `Tessera.alias_serial` → `keypoint_alias` | no |
| `Run_fixture`, `grid-A`, `grid-B`, `unused-tag`, `oneloop-tag` | the store's tags | `fixture-run`, `grid-A`, `grid-B`, `unused-tag`, `weave-tag`. `fixture-run` sorts before `grid-B` as `Run_fixture` did, so every tag tuple the tests compare keeps SGK's order | R-value |
| `config.datastore.factories`, `config.sharding.*` | the registry | `registry.factories`, `registry.replicated_tables`, `registry.sharded_tables` | no |
| `sp.make_units`, `StandinCosmology`, `get_tolerance`, `get_wavenumber`, `make_exit_time`, `make_policy_data` | `TestStandinStore` | `build.get_gauge`, `build.get_keypoint`, `build.make_alias` + `object_store`, `build.get_rule`, `build.make_sample_on` | no |

`version` and `store_tag` keep their names.

### 1.2 The port table (§4.4)

One row per test (85), in SGK's file order.

- **"Kinds in the test"** are the changes inside the test method itself, measured by comparing
  the method's `ast` with SGK's. "—" means the method is SGK's unchanged.
- **Every test also runs under its module's changes**, listed in the "Fixture" column:
  - R-imp: the imports;
  - R-help: the fixture's neutral rows, `FACTORIES`, `store_inventory_tables`;
  - R-count: the data tables.

| # | SGK origin (module · class · method) | Kinds in the test | Fixture | SGK → neutral |
|---|---|---|---|---|
| 1 | `test_store_inventory` · `TestTheFullStore` · `test_every_class_has_a_record` | — | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | — |
| 2 | `test_store_inventory` · `TestTheFullStore` · `test_the_full_store_has_no_problem` | — | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | — |
| 3 | `test_store_inventory` · `TestTheFullStore` · `test_records_are_json_safe` | — | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | — |
| 4 | `test_store_inventory` · `TestTheFullStore` · `test_classes_with_tags_validated_and_values` | R-map, R-value, R-count | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | the tagged classes `BackgroundModel`, `TkNumericIntegration`, `TkWKBIntegration`, `GkNumericIntegration`, `GkWKBIntegration`, `GkSource`, `QuadSource`, `QuadSourceIntegral`, `OneLoopIntegral` → `Gadget`, `Sample`, `Trace`, `Weave`; untagged-and-unvalidated `QuadSourceIntegral`, `OneLoopIntegral` → `Sample`, `Weave` (U18); the unvalidated-rows tuple `BackgroundModel`, `TkNumericIntegration`, `QuadSource` → `Gadget`, `Trace`; `Run_fixture` → `fixture-run` |
| 5 | `test_store_inventory` · `TestTheFullStore` · `test_replicated_and_sharded` | R-imp | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `config.sharding.replicated_tables` → `registry.replicated_tables` |
| 6 | `test_store_inventory` · `TestTheFullStore` · `test_resolve_names_every_parent` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `QuadSourceIntegral` → `Sample` (all three key parents set; deviation 11) |
| 7 | `test_store_inventory` · `TestKeysArePhysical` · `test_different_serial_assignments` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `BackgroundModel`, `wavenumber_exit_time`, `tolerance` → `Gadget`, `keypoint_alias`, `routing_rule`; `QuadSourceIntegral` → `Sample` |
| 8 | `test_store_inventory` · `TestKeysArePhysical` · `test_sharded_rows_on_different_shards` | — | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | — |
| 9 | `test_store_inventory` · `TestKeysArePhysical` · `test_replicated_serials_permuted_and_rows_moved` | — | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | — |
| 10 | `test_store_inventory` · `TestIdentityColumnsMatter` · `test_the_key_fields_are_the_lookup_columns` | — | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | — |
| 11 | `test_store_inventory` · `TestIdentityColumnsMatter` · `test_each_identity_column_changes_the_records` | — | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | — |
| 12 | `test_store_inventory` · `TestNonIdentityDoesNotMatter` · `test_non_identity_columns` | — | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | — |
| 13 | `test_store_inventory` · `TestNonIdentityDoesNotMatter` · `test_timestamps` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `QuadSourceIntegral` → `Sample` |
| 14 | `test_store_inventory` · `TestFloats` · `test_canonical` | — | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | — |
| 15 | `test_store_inventory` · `TestFloats` · `test_canonical_json` | — | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | — |
| 16 | `test_store_inventory` · `TestFloats` · `test_the_last_bit_of_k_changes_the_records` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `wavenumber` (`k_inv_Mpc`) → `keypoint` (`kp_position`); `wavenumber_exit_time` → `keypoint_alias` |
| 17 | `test_store_inventory` · `TestFloats` · `test_log10_tol_is_used_as_stored` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `tolerance` (`log10_tol`) → `routing_rule` (`rule_threshold`); values -5, -7, -9 kept |
| 18 | `test_store_inventory` · `TestFloats` · `test_every_float_leaf_goes_through_canonical` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `tolerance` → `routing_rule`; `wavenumber` → `keypoint` |
| 19 | `test_store_inventory` · `TestFloats` · `test_only_canonical_formats_a_float` | R-imp, R-count | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | the module path; `builders` 21 → 12 for 13 classes (hazard 9) |
| 20 | `test_store_inventory` · `TestTags` · `test_adding_a_tag_changes_that_record_and_nothing_else` | R-map, R-value | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `QuadSourceIntegral` (+`_tags`, `parent_serial`) → `Sample` (+`_tags`, `sample_serial`); `Run_fixture` → `fixture-run` |
| 21 | `test_store_inventory` · `TestTags` · `test_a_tagged_parents_digest_covers_its_tags` | R-map, R-count | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `GkSource` → `Trace` (4), `GkSourcePolicyData` → `Weave`, field `source` → `trace`; the changed set (3 classes → 2) |
| 22 | `test_store_inventory` · `TestTags` · `test_a_tag_on_the_background_model_reaches_its_children` | R-map, R-count | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `BackgroundModel` → `Gadget`; the changed set (4 classes → `Gadget`, `Sample`) |
| 23 | `test_store_inventory` · `TestTags` · `test_oneloop_tags_come_from_its_own_table` | R-map, R-value | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `OneLoopIntegral` → `Weave`; `QuadSourceIntegral` (sharing serial 1) → `Trace`; `oneloop-tag` → `weave-tag` |
| 24 | `test_store_inventory` · `TestTags` · `test_a_tag_no_row_carries_is_only_a_store_tag` | — | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | — |
| 25 | `test_store_inventory` · `TestValueCounts` · `test_the_counts_are_per_parent` | R-count | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | 7 value-table classes → `Gadget` [3, 2], `Trace` [3, 4, 2, 1] |
| 26 | `test_store_inventory` · `TestValueCounts` · `test_deleting_a_value_row_lowers_one_count_by_one` | — | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | — |
| 27 | `test_store_inventory` · `TestValueCounts` · `test_value_tables_are_only_counted` | — | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | — |
| 28 | `test_store_inventory` · `TestReplicatedDivergence` · `test_a_changed_row` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `tolerance` (`log10_tol`) → `routing_rule` (`rule_threshold`) |
| 29 | `test_store_inventory` · `TestReplicatedDivergence` · `test_a_changed_tag_set` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `BackgroundModel_tags` (`model_serial`) → `Gadget_tags` (`gadget_serial`) |
| 30 | `test_store_inventory` · `TestReplicatedDivergence` · `test_a_changed_value_count` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `BackgroundModelValue` → `GadgetPart`; `BackgroundModel` → `Gadget` |
| 31 | `test_store_inventory` · `TestReplicatedDivergence` · `test_the_right_shard_of_three` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `tolerance` → `routing_rule` |
| 32 | `test_store_inventory` · `TestOldStoresAndOrphans` · `test_an_orphan_value_row` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `TkNumericValue` → `TraceStep`; `TkNumericIntegration` → `Trace` |
| 33 | `test_store_inventory` · `TestOldStoresAndOrphans` · `test_a_tag_row_whose_parent_is_missing` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `TkNumeric_tags` → `Trace_tags` |
| 34 | `test_store_inventory` · `TestOldStoresAndOrphans` · `test_a_tag_row_whose_tag_is_missing` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `TkNumeric_tags` → `Trace_tags` (Trace 2 is on shard 1, as Tk 2 was) |
| 35 | `test_store_inventory` · `TestOldStoresAndOrphans` · `test_a_reference_that_cannot_be_resolved` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `TkNumericIntegration` (`model_serial`, field `model`) → `Trace` (`frame_serial`, field `frame`) |
| 36 | `test_store_inventory` · `TestOldStoresAndOrphans` · `test_an_unknown_cosmology_type` | R-map, R-value | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `wavenumber_exit_time` 3 (`cosmology_type`) → `Gadget` 1 (`frame_kind`), by role: the replicated polymorphic referrer; field `cosmology` → `frame` |
| 37 | `test_store_inventory` · `TestDuplicates` · `test_on_one_shard` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `QuadSourceIntegral` (+`_tags`, `parent_serial`) → `Trace` (+`_tags`, `trace_serial`) |
| 38 | `test_store_inventory` · `TestDuplicates` · `test_across_shards` | R-map, R-count | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `QuadSourceIntegral` → `Trace`; the chain of same-shard parents (8 tables) → none (deviation 14) |
| 39 | `test_store_inventory` · `TestDuplicates` · `test_a_replicated_class` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `tolerance` → `routing_rule` (3 rows, count 4) |
| 40 | `test_store_inventory` · `TestDuplicates` · `test_other_tags_are_not_a_duplicate` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `QuadSourceIntegral` → `Trace` (no parent set) |
| 41 | `test_store_inventory` · `TestReadOnlyAndNoRay` · `test_read_inventory_writes_nothing` | R-map | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | `QuadSourceIntegral` → `Sample` |
| 42 | `test_store_inventory` · `TestReadOnlyAndNoRay` · `test_no_ray` | R-imp, R-map, R-count | `_Stores` (`build_full_store`, `full_rows`, `vary_row`) on the neutral full rows; the four data tables (R-count) | the child's two imports; `QuadSourceIntegral` → `Sample`; the payload key `qsi` → `sample`; 3 |
| 43 | `test_store_schema` · `TestSchemaDifferences` · `test_every_file_of_a_current_store_has_no_difference` | — | `build_real_store` / `build_full_store` (default and full rows); `_PoolTestCase` on the stand-in pool | — |
| 44 | `test_store_schema` · `TestSchemaDifferences` · `test_each_kind_is_found_on_the_right_shard_by_name` | R-map | `build_real_store` / `build_full_store` (default and full rows); `_PoolTestCase` on the stand-in pool | `OneLoopIntegral_tags`, `GkSource_parents` → `Weave_tags`, `Sample_members` (still in reverse declaration order); `TkNumericIntegration.stop_Tprime` → `Trace.step_count`; `GkSource` → `Sample` |
| 45 | `test_store_schema` · `TestSchemaDifferences` · `test_it_issues_no_write` | — | `build_real_store` / `build_full_store` (default and full rows); `_PoolTestCase` on the stand-in pool | — |
| 46 | `test_store_schema` · `TestTheReader` · `test_a_refusal_yields_nothing_and_disposes_every_engine` | R-imp, R-map | `build_real_store` / `build_full_store` (default and full rows); `_PoolTestCase` on the stand-in pool | `OneLoopIntegral` → `Weave` |
| 47 | `test_store_schema` · `TestTheInventory` · `test_read_inventory_refuses_a_store_missing_a_table` | R-map | `build_real_store` / `build_full_store` (default and full rows); `_PoolTestCase` on the stand-in pool | `QuadSourceIntegral_tags` → `Sample_tags` |
| 48 | `test_store_schema` · `TestTheReadWriteOpenRefuses` · `test_an_absent_column_an_extra_column_and_an_extra_table` | R-map | `build_real_store` / `build_full_store` (default and full rows); `_PoolTestCase` on the stand-in pool | `TkNumericIntegration.stop_Tprime` → `Trace.step_count`; `tolerance` → `routing_rule` |
| 49 | `test_store_schema` · `TestTheReadWriteOpenRefuses` · `test_an_absent_table_beside_another_difference_is_still_refused` | R-map | `build_real_store` / `build_full_store` (default and full rows); `_PoolTestCase` on the stand-in pool | `GkSourcePolicy` → `routing_rule` |
| 50 | `test_store_schema` · `TestTheReadWriteOpenRefuses` · `test_a_prune_record_is_not_completed` | R-map | `build_real_store` / `build_full_store` (default and full rows); `_PoolTestCase` on the stand-in pool | `BackgroundModel` → `Gadget` |
| 51 | `test_store_schema` · `TestTheReadWriteOpenRecoversAnAbsentTable` · `test_a_fresh_store_has_no_difference` | — | `build_real_store` / `build_full_store` (default and full rows); `_PoolTestCase` on the stand-in pool | — |
| 52 | `test_store_schema` · `TestTheReadWriteOpenRecoversAnAbsentTable` · `test_an_interrupted_drop_of_a_sharded_class` | — | `build_real_store` / `build_full_store` (default and full rows); `_PoolTestCase` on the stand-in pool | — |
| 53 | `test_store_schema` · `TestTheReadWriteOpenRecoversAnAbsentTable` · `test_an_interrupted_drop_of_a_replicated_class` | R-map | `build_real_store` / `build_full_store` (default and full rows); `_PoolTestCase` on the stand-in pool | `GkSourcePolicy` → `routing_rule` |
| 54 | `test_store_schema` · `TestTheReadWriteOpenRecoversAnAbsentTable` · `test_an_interrupted_first_open` | — | `build_real_store` / `build_full_store` (default and full rows); `_PoolTestCase` on the stand-in pool | — |
| 55 | `test_store_schema` · `TestThePrimaryIsRefused` · `test_an_extra_table_and_a_missing_column` | — | `build_real_store` / `build_full_store` (default and full rows); `_PoolTestCase` on the stand-in pool | — |
| 56 | `test_store_reader` · `TestReaderReads` · `test_every_shard_with_its_serial_and_path` | — | `build_real_store` (default rows) | — |
| 57 | `test_store_reader` · `TestReaderReads` · `test_row_counts_equal_an_independent_count` | — | `build_real_store` (default rows) | — |
| 58 | `test_store_reader` · `TestReaderReads` · `test_replicated_rows_have_the_same_serials_on_every_shard` | — | `build_real_store` (default rows) | — |
| 59 | `test_store_reader` · `TestReaderReads` · `test_every_engine_is_disposed_on_exit` | — | `build_real_store` (default rows) | — |
| 60 | `test_store_reader` · `TestReaderReads` · `test_engines_open_mode_ro_and_never_immutable` | — | `build_real_store` (default rows) | — |
| 61 | `test_store_reader` · `TestReaderNeverWrites` · `test_reading_every_table_changes_nothing` | — | `build_real_store` (default rows) | — |
| 62 | `test_store_reader` · `TestReaderNeverWrites` · `test_a_write_through_a_reader_engine_raises` | — | `build_real_store` (default rows) | — |
| 63 | `test_store_reader` · `TestADifferingSchemaIsRefused` · `test_a_missing_table_or_column_is_refused_naming_the_shard` | R-map | `build_real_store` (default rows) | `OneLoopIntegral_tags` → `Weave_tags`; `TkNumericIntegration.stop_Tprime` → `Trace.step_count` |
| 64 | `test_store_reader` · `TestADifferingSchemaIsRefused` · `test_an_extra_column_or_table_is_refused_naming_the_shard` | R-map | `build_real_store` (default rows) | `GkSource` → `Sample` |
| 65 | `test_store_reader` · `TestRefusals` · `test_journal_beside_the_primary` | — | `build_real_store` (default rows) | — |
| 66 | `test_store_reader` · `TestRefusals` · `test_journal_beside_a_shard` | — | `build_real_store` (default rows) | — |
| 67 | `test_store_reader` · `TestRefusals` · `test_missing_shard_is_refused_by_read_closed_store` | — | `build_real_store` (default rows) | — |
| 68 | `test_store_reader` · `TestRefusals` · `test_primary_with_no_shards_table` | — | `build_real_store` (default rows) | — |
| 69 | `test_store_reader` · `TestRefusals` · `test_missing_primary` | — | `build_real_store` (default rows) | — |
| 70 | `test_store_reader` · `TestNoRay` · `test_reading_in_a_child_interpreter_leaves_ray_uninitialised` | — | `build_real_store` (default rows) | — |
| 71 | `test_foreign_key_check` · `TestFullStore` · `test_the_added_row_is_not_satisfied_by_coincidence` | R-map | `own_rows` (full rows plus the added Sample and member row) | `QuadSource.Tq_serial` (→ `TkNumericIntegration`, wrongly → `QuadSource`) → `Sample_members.tessera_serial` (→ `Tessera`, wrongly → `Sample`) |
| 72 | `test_foreign_key_check` · `TestFullStore` · `test_the_added_rows_are_in_the_written_shard` | R-map | `own_rows` (full rows plus the added Sample and member row) | the added `QuadSource` → the added `Sample` and its member row; the SQL joins the two (deviation 10) |
| 73 | `test_foreign_key_check` · `TestFullStore` · `test_every_shard_passes_foreign_key_check` | — | `own_rows` (full rows plus the added Sample and member row) | — |
| 74 | `test_foreign_key_check` · `TestFullStore` · `test_the_default_stores_pass_too` | — | `own_rows` (full rows plus the added Sample and member row) | — |
| 75 | `test_foreign_key_check` · `TestFullStore` · `test_a_relabelled_store_passes` | — | `own_rows` (full rows plus the added Sample and member row) | — |
| 76 | `test_foreign_key_check` · `TestTheCheckSeesAViolation` · `test_a_dangling_tq_is_reported` | R-map, R-value | `own_rows` (full rows plus the added Sample and member row) | `QuadSource.Tq_serial` 2 → `Sample_members.tessera_serial` 4 (on shard 1); `row["serial"]` → `row["sample_serial"]` |
| 77 | `test_foreign_key_check` · `TestTheCheckSeesAViolation` · `test_a_dangling_exit_time_in_the_policy_data_is_reported` | R-map | `own_rows` (full rows plus the added Sample and member row) | `GkSourcePolicyData.wavenumber_exit_serial` → `wavenumber_exit_time` becomes `Tessera.alias_serial` → `keypoint_alias` |
| 78 | `test_foreign_key_check` · `TestStandinStore` · `test_a_store_written_by_the_real_write_path_passes` | R-help, R-map | `own_rows` (full rows plus the added Sample and member row) | `sp.get_tolerance` ×2 → `build.get_gauge` (10, 9); `sp.get_wavenumber` → `build.get_keypoint`; `sp.make_exit_time` → `build.make_alias`; `GkSourcePolicy` → `build.get_rule`; `sp.make_policy_data` → `build.make_sample_on`; `GkSource` → `Gadget` (the unbacked reference); `wavenumber_exit_time` → `keypoint` (hazard 10); `ray.get` → `build.resolve`; units and cosmology removed |
| 79 | `test_schema_builder` · `TestSchemaIsUnchanged` · `test_build_schema_reproduces_the_witness` | — | the witness `schema_at_extraction-04a.json`; the registry less `ephemeral_probe` (U20) | — |
| 80 | `test_schema_builder` · `TestSchemaIsUnchanged` · `test_build_schema_records_hold_no_inserter` | — | the witness `schema_at_extraction-04a.json`; the registry less `ephemeral_probe` (U20) | — |
| 81 | `test_schema_builder` · `TestSchemaIsUnchanged` · `test_actor_build_schema_reproduces_the_witness` | — | the witness `schema_at_extraction-04a.json`; the registry less `ephemeral_probe` (U20) | — |
| 82 | `test_schema_builder` · `TestSchemaIsUnchanged` · `test_actor_adds_only_the_inserters` | — | the witness `schema_at_extraction-04a.json`; the registry less `ephemeral_probe` (U20) | — |
| 83 | `test_schema_builder` · `TestSchemaIsUnchanged` · `test_actor_tables_are_in_its_metadata` | — | the witness `schema_at_extraction-04a.json`; the registry less `ephemeral_probe` (U20) | — |
| 84 | `test_schema_builder` · `TestNoneRegistration` · `test_build_schema_gives_a_record_with_no_table` | — | the witness `schema_at_extraction-04a.json`; the registry less `ephemeral_probe` (U20) | — |
| 85 | `test_schema_builder` · `TestNoneRegistration` · `test_actor_gives_a_record_with_no_table_and_no_inserter` | R-imp | the witness `schema_at_extraction-04a.json`; the registry less `ephemeral_probe` (U20) | the module path in `importlib.import_module` |

### 1.3 The client additions, and every literal and contract line that changed

**The six tables (U15)**, in `factories` after `Sample_members`, in this order:

| Table | Kind | Columns | Inventory spec |
|---|---|---|---|
| `Trace` | sharded on `"k"`; `version`, `timestamp` | `keypoint_serial` (FK `keypoint`, indexed, not null); `frame_kind` (`Integer`, not null); `frame_serial` (`Integer`, indexed, not null, no FK); `trace_label` (`String(256)`, not null); `step_count` (`Integer`, not null); `trace_validated` (`Boolean`, default `False`, not null) | `leaves=("trace_label", "frame_kind")`; `k` → `keypoint`; `frame` polymorphic through **the same `FRAME_TYPES` object** as `Gadget`'s; `tags=("Trace_tags", "trace_serial")`; `values=("TraceStep", "trace_serial")`; `validated="trace_validated"` |
| `Trace_tags` | neither; `serial: False`; `timestamp` | `trace_serial` (FK `Trace`), `tag_serial` (FK `store_tag`), the primary key | — |
| `TraceStep` | neither; default `serial`, no `version`, no `timestamp` | `trace_serial` (FK `Trace`, indexed, not null); `step_index` (`Integer`); `step_value` (`Float(64)`) | — |
| `Weave` | sharded on `"k"`; `version`, `timestamp` | `keypoint_serial` (FK `keypoint`); `trace_serial` (FK `Trace`); `anchor_serial` (`Integer`, indexed, nullable, no FK); `weave_label` (`String(256)`) | `leaves=("weave_label",)`; `k`, `trace`, and `anchor` (nullable) → `Tessera`; `tags=("Weave_tags", "weave_serial")`; `parent_sets={"strands": ParentSet("Weave_members", "weave_serial", {"anchor": Parent(… "Tessera", nullable=True), "origin": Parent(… "Trace", nullable=True)})}` |
| `Weave_tags` | as `Trace_tags`, on `weave_serial` | | — |
| `Weave_members` | neither; default `serial`, no `version`, no `timestamp` | `weave_serial` (FK `Weave`, indexed); `anchor_serial` (FK `Tessera`, indexed, nullable); `origin_serial` (FK `Trace`, indexed, nullable) | — |

**The factories.**
- `Trace_factory` and `Weave_factory`:
  - a sharded `build` that finds the stored object or returns an unstored one, and inserts nothing;
  - a `store` that writes the row, its tags, and its steps or strands.
- `Trace_factory.validate` checks that `step_count` equals the number of `TraceStep` rows.
- The tag, step and member tables' `build` raises `NotImplementedError`.
- Neither class declares `validate_on_startup`.

**The registry.**
- `sharded_tables` gains `"Trace": "k"` and `"Weave": "k"`.
- A drop group, `traces`, holds the six in registry order.
- `replicated_tables`, `read_table_config`, `serial_batch_sizes` and `__all__` are unchanged.
- The docstring's role table gains three rows, and its drop-group paragraph one sentence.

**`Gadget_factory._validate_row`'s warning.** When the Gadget does not validate, it reads the row's
label in one more query and prints:

```
!! WARNING: Gadget "<label>" did not validate after serialization (expected parts=<n>, number stored=<m>)
```

Nothing else in the factory changes.

**`build.py`.**
- New constants: `TRACES` and `WEAVE_LABEL`.
- New helpers: `make_trace`, `store_trace`, `get_trace`, `make_weave`, `store_weave` and
  `get_weave`.
- `write_every_class` now also writes:
  - two Traces, on keypoints 0.25 and 0.5, one on each frame kind, with tags and steps: one
    validated, one not;
  - one Weave, on keypoint 0.25, keyed on that keypoint's Trace, with a Tessera anchor and two
    strands, one with no anchor and one with no origin.
- One docstring bullet.

**By deletion.** The client's four files remove two lines:
- **U18's one line**, `validated="sample_validated",` in `Sample_factory.inventory_spec`;
- the last bullet of `write_every_class`'s docstring, whose full stop became a semicolon before
  the new bullet.

**U19** (correction 5), in `test_reconcile_at_open.py`, exactly:

```diff
diff --git a/datastorekit/tests/test_reconcile_at_open.py b/datastorekit/tests/test_reconcile_at_open.py
index d59e8c5..a6e6fc3 100644
--- a/datastorekit/tests/test_reconcile_at_open.py
+++ b/datastorekit/tests/test_reconcile_at_open.py
@@ -1088,7 +1088,7 @@ class TestPruningAfterRepair(_ReconcileTestCase):
         """The copied model is unvalidated everywhere: pruned on every shard, or kept on every
         shard, and never on some. The drop actions include aliases, which drops
         the replicated keypoint_alias table: on every shard alike. They also name
-        aliases' dependents (tesserae and samples), because
+        aliases' dependents (tesserae, samples and traces), because
         a drop without them is refused (prompts/datastore-generic-followup, prompt 01).
         """
         for prune in (True, False):
@@ -1110,6 +1110,7 @@ class TestPruningAfterRepair(_ReconcileTestCase):
                                 "samples",
                                 "aliases",
                                 "tesserae",
+                                "traces",
                             ]
                         ),
                     )
```

The port check still gives `test_reconcile_at_open` 41 tests, 9 classes, 52 functions and 148
assertions (§4.3).

**`test_neutral_client.py`, every changed literal.** All are measured over the registry or
`build_store`:
- `MEASURED_DEPENDENTS`:
  - `aliases` and `tesserae` gain `"Weave", "Weave_tags", "Weave_members"`, because `Weave.anchor`
    and `Weave_members.anchor_serial` name a `Tessera`;
  - `"traces": []` is added.
- `test_each_form_of_a_registration_is_in_use`: the `no_serial` list gains `"Trace_tags",
  "Weave_tags"`.
- `test_every_declaration_field_is_in_use`: `len(polymorphic)` goes from 1 to 2, since `Trace.frame`
  is also polymorphic. `polymorphic[0]` is still `Gadget`'s.
- `test_the_shard_key_and_its_proxy`: the `registry.sharded_tables` literal gains `"Trace": "k",
  "Weave": "k"`.
- `test_the_reader_and_the_inventory_read_every_class`:
  - `counts` gains `"Trace": 2, "Weave": 1`;
  - the four Samples' expected `validated` change from `True, True, True, False` to `None` (U18).

`KEPT` is unchanged.

**The ripple, as measured.**
- With only the client changed, the suite gave `Ran 268 tests`, `FAILED (failures=5, errors=4)`:
  - the five `test_neutral_client` literals above;
  - `TestPruningAfterRepair.test_an_interrupted_store` in `test_reconcile_at_open`, and its
    inheritor in `test_one_timestamp_per_write`, both subtests each. The reopen was refused with
    "cannot drop ['Sample', 'Sample_members', 'Sample_tags', 'Tessera', 'keypoint_alias'] alone:
    the rows of ['Weave', 'Weave_tags', 'Weave_members'] would name rows that are gone".
- That was the first stop (§2 item 5). After the literals and U19: `Ran 268 tests … OK`.

**`docs/client-contract.md`, every changed line (client cells only).**
- §1 row 6: `{"Tessera": "k", "Sample": "k"}` → `{"Tessera": "k", "Sample": "k", "Trace": "k",
  "Weave": "k"}`.
- §1 row 15: `(16 classes)` → `(22 classes)`.
- §2 rows:
  - `serial`: gains `Trace_tags`, `Weave_tags`;
  - `version`: gains `Trace`, `Weave`;
  - `timestamp`: gains `Trace`, `Trace_tags`, `Weave`, `Weave_tags`.
- §3 rows:
  - `build`: "every factory but the three association tables" → "every factory but the seven
    association, step and member tables";
  - `store` (sharded): `Sample` → `Sample`, `Trace`, `Weave`;
  - `validate` (sharded): `Sample` → `Sample`, `Trace`;
  - `inventory_spec()`: 11 → 13 classes.
- §4 field rows:
  - `parents`: gains `Trace`, `Weave`;
  - `tags`: gains `Trace`, `Weave`;
  - `values`: gains `Trace` (`TraceStep`);
  - **`validated`: `Gadget`, `Sample` → `Gadget`, `Trace`** (U18);
  - `parent_sets`: gains `Weave` (`strands`).
- §4 *Neutral client* notes:
  - for `Parent`: `Trace.frame` is polymorphic through the same map, and `Weave.anchor` is
    nullable;
  - for `ParentSet`: `Weave.strands` over `Weave_members`.
- §5: the tag-column row gains `Trace_tags`, `Weave_tags`.
- §6: the shard-key attribute row gains `Trace.k`, `Weave.k`.

### 1.4 `real_store_fixtures`: what is transcribed, and what is new

**Transcribed** (R-imp only, with the registry's names):
- `RowSet`, `FIXED_TIMESTAMP`, `RealStore`, `with_rows`;
- `_write_primary` (`_ShardKeyType_name = "keypoint"`), `_insert_rows`, `_write_shard`;
- `build_real_store`, `expected_row_counts`, `independent_row_counts`, `file_state`;
- `_schema_tables`, `_placeholder`, `fill_required`, `full_rows`, `_empty_shard_bytes`,
  `_write_full_shard`, `build_full_store`;
- `relabel_serials`, `find_row`, `vary_row`.

`relabel_serials` keeps SGK's control flow. SGK's
`if target == "cosmology": target = _COSMOLOGY_TABLES[row["cosmology_type"]]` becomes
`if target == _FRAME: type_column, types = polymorphic[table][column]; target = types[row[type_column]]`,
with `polymorphic = _polymorphic()` derived from the specs.

**New**:
- the row data;
- the private row helpers `_trace`, `_values` (step rows), `_tags`, `_merge`, `_members` and
  `_weave_members` (SGK's `_tk_numeric` and `_gk_source_parents` have no counterpart);
- `_polymorphic` and `_FRAME`;
- **`references()`, derived**: the schema's foreign keys, then every `inventory_spec` parent (its
  `of`, or `"frame"` for a polymorphic one) and every parent-set member (on its member table).
  SGK's `_UNDECLARED_REFERENCES` and `_COSMOLOGY_TABLES` have no counterpart. The derived map,
  tables with no reference omitted:

- `keypoint_alias`: `version` → `version`, `keypoint_serial` → `keypoint`
- `routing_rule`: `version` → `version`
- `Gadget`: `version` → `version`, `frame_serial` → `frame`
- `Gadget_tags`: `gadget_serial` → `Gadget`, `tag_serial` → `store_tag`
- `GadgetPart`: `gadget_serial` → `Gadget`
- `Tessera`: `version` → `version`, `alias_serial` → `keypoint_alias`
- `Sample`: `version` → `version`, `keypoint_serial` → `keypoint`, `gadget_serial` → `Gadget`, `anchor_serial` → `Tessera`
- `Sample_tags`: `sample_serial` → `Sample`, `tag_serial` → `store_tag`
- `Sample_members`: `sample_serial` → `Sample`, `tessera_serial` → `Tessera`
- `Trace`: `version` → `version`, `keypoint_serial` → `keypoint`, `frame_serial` → `frame`
- `Trace_tags`: `trace_serial` → `Trace`, `tag_serial` → `store_tag`
- `TraceStep`: `trace_serial` → `Trace`
- `Weave`: `version` → `version`, `keypoint_serial` → `keypoint`, `trace_serial` → `Trace`, `anchor_serial` → `Tessera`
- `Weave_tags`: `weave_serial` → `Weave`, `tag_serial` → `store_tag`
- `Weave_members`: `weave_serial` → `Weave`, `anchor_serial` → `Tessera`, `origin_serial` → `Trace`

**Neither fixture asserts anything** (port check: 0 functions compared, 0 assertions; (b) and (m)
show that the check would see it).

### 1.5 The fixture's rows

Row counts per table and row set:

| Table | `REPLICATED_ROWS` | `SHARDED_ROWS[0]` | `SHARDED_ROWS[1]` | `FULL_REPLICATED_ROWS` | `FULL_SHARDED_ROWS[0]` | `FULL_SHARDED_ROWS[1]` |
|---|---|---|---|---|---|---|
| `version` | 1 | 0 | 0 | 2 | 0 | 0 |
| `store_tag` | 3 | 0 | 0 | 5 | 0 | 0 |
| `keypoint` | 2 | 0 | 0 | 3 | 0 | 0 |
| `keypoint_alias` | 2 | 0 | 0 | 4 | 0 | 0 |
| `dial_setting` | 1 | 0 | 0 | 2 | 0 | 0 |
| `knob_setting` | 0 | 0 | 0 | 1 | 0 | 0 |
| `gauge_setting` | 1 | 0 | 0 | 2 | 0 | 0 |
| `routing_rule` | 2 | 0 | 0 | 3 | 0 | 0 |
| `Gadget` | 1 | 0 | 0 | 2 | 0 | 0 |
| `Gadget_tags` | 1 | 0 | 0 | 3 | 0 | 0 |
| `GadgetPart` | 3 | 0 | 0 | 5 | 0 | 0 |
| `Tessera` | 0 | 0 | 0 | 0 | 3 | 2 |
| `Sample` | 0 | 0 | 0 | 0 | 2 | 1 |
| `Sample_tags` | 0 | 0 | 0 | 0 | 3 | 1 |
| `Sample_members` | 0 | 0 | 0 | 0 | 3 | 1 |
| `Trace` | 0 | 1 | 1 | 0 | 3 | 1 |
| `Trace_tags` | 0 | 2 | 2 | 0 | 5 | 2 |
| `TraceStep` | 0 | 3 | 4 | 0 | 6 | 4 |
| `Weave` | 0 | 0 | 0 | 0 | 1 | 0 |
| `Weave_tags` | 0 | 0 | 0 | 0 | 2 | 0 |
| `Weave_members` | 0 | 0 | 0 | 0 | 2 | 0 |
| **total** | 17 | 6 | 7 | 32 | 30 | 12 |

**The default rows** (the small store `test_store_reader` and `test_store_schema` read).
- Replicated:
  - version 1;
  - tags 1 `fixture-run`, 2 `grid-A`, 3 `unused-tag`;
  - keypoints 1 (0.1) and 2 (1.0), both flags on;
  - routing rules 1 (-5.0) and 2 (-7.0);
  - dial 1 (level 3, stepping 1);
  - gauge 1 (4);
  - aliases 1 and 2 (offset 0.125, on keypoints 1 and 2);
  - Gadget 1 on dial 1: validated, tag 1, three parts.
- Sharded: Trace 1 on shard 0 (keypoint 1) and Trace 2 on shard 1 (keypoint 2). Each is on dial
  1, validated, tags 1 and 2, with 3 and 4 steps.
- Shard keys `{1: 0, 2: 1}`.

**The full rows** add:
- version 2;
- tags 4 `grid-B` and 5 `weave-tag`;
- keypoint 3 (0.5);
- rule 3 (-9.0);
- dial 2 (5, 0);
- knob 1 (7, 2): it shares serial 1 with dial 1;
- gauge 2 (8);
- aliases 3 (keypoint 3) and 4 (keypoint 1, offset 0.25);
- Gadget 2 on knob 1: unvalidated, tag 1, two parts. Gadget 1 gains tag 2.

On shard 0:
- Tesserae 1, 2 (alias 1) and 3 (alias 4).
- Samples 1 and 2:
  - Sample 1: validated, on Gadget 1, anchored on Tessera 4 (shard 1), members Tesserae 1 and 2,
    tags 1 and 2;
  - Sample 2: validated, anchored on Tessera 5 (shard 1), member Tessera 2, tag 1.
- Trace 3: knob 1, unvalidated, 2 steps, tags 1 and 4.
- Trace 4: dial 2, validated, 1 step, tag 1.
- Weave 1:
  - keypoint 1, keyed on Trace 4, no anchor, tags 1 and 5;
  - strands 701 (Tessera 1, no origin) and 702 (no anchor, Trace 3).

On shard 1:
- Tesserae 4 (alias 2) and 5 (alias 3).
- Sample 4: unvalidated, on Gadget 2, anchored on Tessera 1 (shard 0), member Tessera 4, tag 1.

Full shard keys `{1: 0, 2: 1, 3: 1}`.

§2.4's properties, checked:
- **Fixed serials, at least two version rows.** Every timestamp is `FIXED_TIMESTAMP`.
- **Every inventory class has a row, and every table has rows.** Measured: the full store reads
  13 classes, `problems == ()`, and `foreign_key_check` is empty on both shards.
- **A run tag every tagged record carries, and a tag no row carries.**
- **Both frame kinds**, each referenced by a Gadget and by a Trace:
  - dial: Gadget 1, and Traces 1, 2 and 4;
  - knob: Gadget 2 and Trace 3.

  Dial 1 and knob 1 share serial 1.
- **Unvalidated rows** of Gadget (2), Trace (3) and Sample (4). Sample's flag is not read by the
  inventory after U18.
- **A different value count per parent**: Gadget 3, 2; Trace 3, 4, 2, 1.
- **Exactly one Weave**, sharing serial 1 with Trace 1, which no Weave names. It is tagged
  `weave-tag` beside the run tag, and nothing depends on it.
- **`Weave_members` rows** with a `None` anchor and with a `None` origin, and a Weave whose own
  anchor is `None`.
- **Sample anchors on the other shard: yes. "And one None": no, deviation 11.**
- **A second row for every identity field to vary to.** See §1.6; each variation was probed and
  gives no problem (§3, hazard 2).
- **Shard keys over two shards**, and no sharded row on a further shard.
- **Consistent counts (hazard 7).** Every `part_count`, `member_count` and `step_count` equals its
  rows.
- **For `test_foreign_key_check`**, every `Sample_members` row names a Tessera whose serial is
  also a Sample serial on its shard: shard 0 {1, 2}, shard 1 {4}.

### 1.6 `test_store_inventory`'s four data tables (R-count as a whole)

Each table is re-derived from the neutral rows.

| Table | Rule | SGK | Neutral |
|---|---|---|---|
| `INVENTORY_CLASSES` | the order `inventory_classes(registry.factories)` derives, as a literal | 21 | 13: `version`, `store_tag`, `keypoint`, `dial_setting`, `knob_setting`, `gauge_setting`, `routing_rule`, `keypoint_alias`, `Gadget`, `Tessera`, `Sample`, `Trace`, `Weave` |
| `VALUE_TABLES` | every spec's `values` table | 7 | 2: `GadgetPart`, `TraceStep` |
| `IDENTITY` | for every inventory class, every key field (leaf, key parent, parent set), each with one row and column whose change to a real, resolving value changes that field | 93 entries over 21 classes | 33 over 13: 1, 1, 1, 2, 2, 1, 3, 3, 3, 2, 5, 4, 5 in the order above |
| `NON_IDENTITY` | every column of the neutral classes and their value tables that the inventory does not read, timestamps apart (`test_timestamps`) | 40 (correction 2) | 17 |

**`NON_IDENTITY` by category:**

| Category | SGK | Neutral |
|---|---|---|
| compute-target labels | 9 | **absent**: every neutral label is a leaf (`gadget_label`, `trace_label`, `weave_label`, `sample_code`) |
| payload and provenance | 14 | 8: `Gadget.part_count`, `GadgetPart.part_index`, `GadgetPart.part_value`, `Sample.member_count`, **`Sample.sample_validated`** (non-identity since U18), `Trace.step_count`, `TraceStep.step_index`, `TraceStep.step_value` |
| solver serials | 6 | **absent**: the client has no solver reference |
| descriptive names and labels | 4 | **absent**: `routing_rule`'s label is a leaf |
| version foreign keys | 5 | 7: `keypoint_alias`, `routing_rule`, `Gadget`, `Tessera`, `Sample`, `Trace`, `Weave` |
| the OR-flags | 2 | 2: `keypoint 1 kp_marked`, `keypoint 2 kp_flagged` |

The 19 absent entries are listed here as absent, not invented.

**How each identity variation resolves.** Probed from the scratchpad, `identity_probe.py`:
- each of the 33 variations gives `problems == ()` and leaves the class's record count unchanged,
  so each changes an identity and does not make a parent unresolved;
- each of the 17 non-identity variations gives `problems == ()` and equal records.

The variation that is not a column of the class's own rows:
- `Sample.members` varies Tessera 2's weight, since `Sample_members` has no serial (deviation 12).

### 1.7 The witness (§2.5, U20)

**Captured from the registry less the classes whose `register()` is `None`** (correction 6), with
`schema_description.py`'s `__main__`:

```
./venv/bin/python datastorekit/tests/schema_description.py datastorekit/tests/data/schema_at_extraction-04a.json
```

- **The tree.** `HEAD` `74c6343` with this prompt's uncommitted work: §2.3, U18, U19 and U20
  applied, and `test_schema_builder` not yet passing.
- **Size and hash.** 73,842 bytes; SHA-256
  `c3536a2b0edf73cfbd3cf1fdc38d5135c5ba4f7edf9da257c9ff344ffb9bad6c`. 21 classes, without
  `ephemeral_probe`.
- **The second capture.** The tree's `datastorekit/` (without `__pycache__` and `data/`) was
  copied to the scratchpad (`treecopy2/`). From there, with `PYTHONPATH=.`, `datastorekit.__file__`
  resolved to the copy, and the capture was compared with `cmp`: **byte-identical**, with the same
  SHA-256.

**The superseded capture.** It was taken before U20 from the whole registry (22 classes,
`ephemeral_probe` with `"insert": None`), and captured twice, byte-identical: 74,055 bytes,
SHA-256 `49fd03298a6222f21fc58a8bc42160fea12da1a28568bb2a3d2a763959e800c0`.
- **Why it was superseded:** with it, `test_build_schema_reproduces_the_witness` failed and
  `test_actor_adds_only_the_inserters` raised `KeyError: 'ephemeral_probe'` (§2 item 6).
- It was never committed, and nothing depended on it.

SGK's witnesses are not copied, and `WITNESS` names the new file.

## 2. Deviations from the prompt

1. **Correction 1, U18**: `validated="sample_validated",` is deleted from
   `Sample_factory.inventory_spec`.
   - Its allowed ripple: the four Sample flags in `test_neutral_client.py` (now `None`), and the
     contract's `validated` row (now `Gadget`, `Trace`).
   - `Sample` plays `QuadSourceIntegral` in `test_classes_with_tags_validated_and_values`: tagged,
     no flag, no values.
   - The unvalidated-rows tuple holds `Gadget`, `Trace` (R-count).

   No other test of 02, 03a or 03b changed through it. **STRUCTURALLY REQUIRED.**
2. **Correction 2**: `NON_IDENTITY` has 40 entries, and the three absent categories are 19
   (§1.6). **STRUCTURALLY REQUIRED.**
3. **Correction 3**: hazard 1's figures, re-measured (§3, hazard 1). **STRUCTURALLY REQUIRED.**
4. **Correction 4**: the line numbers. `stop_Tprime` is at `test_store_schema.py:152`, `:164`,
   `:191`, `:341`, `:343`, `:345`, and at `test_store_reader.py:231`, `:234`, `:236`; all are
   mapped to `Trace.step_count`. **STRUCTURALLY REQUIRED.**
5. **Correction 5, U19, and the first stop.**
   - **The stop.** With §2.3 applied, `test_reconcile_at_open.TestPruningAfterRepair.test_an_interrupted_store`
     and its inheritor `test_one_timestamp_per_write.TestRepairThenPruneAtOpen` errored, 4
     subtests in all. The layer refused the drop of `samples`, `aliases` and `tesserae` without
     the `traces` tables (`ShardedPool._refuse_drop_that_leaves_references`, `SQL/ShardedPool.py:733`).
   - That was §5's third condition. The agent stopped, uncommitted.
   - **The resolution.** The user took U19: `"traces"` is added to that one list (R-count), and
     the docstring's list of aliases' dependents gains it (§1.3).
   - No other line of 03a's or 03b's modules changed.

   **STRUCTURALLY REQUIRED.**
6. **Correction 6, U20, and the second stop.**
   - **The stop.** With the witness captured from the whole registry, `test_schema_builder` gave 2
     failures and 1 error, all on `ephemeral_probe`, the client's class whose `register()` is
     `None`:
     - the actor's record carries `"insert": None`, and `build_schema`'s has no `insert`, so no
       one witness matches both;
     - `test_actor_adds_only_the_inserters` indexes `actor._inserters` for every record.
   - Passing needed either a layer change, or a narrower registry and a second capture. The agent
     stopped, uncommitted.
   - **The resolution.** The user took U20:
     - `test_schema_builder`'s `_factories`, and `schema_description.actor_with_built_schema`
       (so its `__main__`), are `{n: f for n, f in registry.factories.items() if f.register() is
       not None}` (R-help, as 03a's `REPLICATED`);
     - the witness is captured again, twice (§1.7).
   - No assertion changes. The `None` case stays pinned by `TestNoneRegistration`.

   **STRUCTURALLY REQUIRED.**
7. **Correction 7, U21**: `test_schema_builder`'s module docstring, the run from "The current one
   is" to "``stepping_mode``)." (SGK `:16-35`).
   - **Before:** "The current one is ``schema_at_datastore-generic-07.json``
     (``prompts/datastore-generic`` prompt 07: no table changes; every record of a class with a
     table carries three more keys, …), and before that ``schema_at_datastore-integrity-06.json``
     (prompt 06: …, and the exit time's and ``IntegrationSolver``'s ``stepping_mode``)." This is
     20 lines, which name SGK tables on 12.
   - **After:** "The current one is ``schema_at_extraction-04a.json``, the neutral test client's
     schema, captured by prompt 04a of the extraction campaign from the registry's classes with a
     table. The source repository's earlier witnesses, from ``schema_at_base.json`` to
     ``schema_at_datastore-generic-07.json``, are that repository's history of its own schema,
     and are not copied here."
   - The rest of the docstring is ported unchanged.

   **IMPLEMENTATION CHOICE**, at the user's direction.
8. **The orchestrator's five additions:**
   - (l), the full store with no Weave (§6.2);
   - (m), `schema_description` made to assert (§6.1);
   - (h) already biting (§6.2);
   - `Trace` preferred in `TestDuplicates` (all four tests);
   - the second vocabulary grep (§4.5).

   Each is an **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
9. **`test_foreign_key_check`'s added row follows the test's assertions, not §2.7's wording.**
   - §2.7 says the added member row's `tessera_serial` "is also a `Sample` serial on that shard".
   - The test asserts the opposite of the added row: `assertNotIn(ADDED_TQ_SERIAL,
     serials(rows, "Sample"))`. It asserts the coincidence of the fixture's own rows instead.
   - So the added row names Tessera 3, which is no Sample serial on shard 0. Every fixture
     `Sample_members` row names a Tessera whose serial is also a Sample serial on its shard.

   The coordinator confirmed this reading. **STRUCTURALLY REQUIRED** (the assertion).
10. **The added rows are a `Sample` (serial 10, `ADDED_QUADSOURCE_SERIAL`) and its one
    `Sample_members` row** (Tessera 3, `ADDED_TQ_SERIAL`). The Sample's cross-shard anchor is
    Tessera 4 (`ADDED_TR_SERIAL`), the counterpart of SGK's `Tr` on shard 1.
    - `Sample_members` has no serial. So `test_the_added_rows_are_in_the_written_shard` selects
      `"Sample".serial, tessera_serial, anchor_serial` from `Sample` joined to its member rows,
      and `test_a_dangling_tq_is_reported` finds the member row by `row["sample_serial"]` in place
      of `row["serial"]` (R-map).
    - The three constants keep their names (§2.1).

    **STRUCTURALLY REQUIRED.**
11. **Every full-store Sample has an anchor, against §2.4's "and one None".**
    `test_resolve_names_every_parent`, with `Sample` in `QuadSourceIntegral`'s role, asserts
    `"key"` in the resolution of every parent of every record. A `None` anchor resolves to `None`,
    and `assertIn` raises `TypeError` on it.
    - A nullable `None` key parent is still in the store: `Weave.anchor`, and the `Weave_members`
      rows.
    - `build_store`'s `sample-0` keeps Sample's `None` anchor (02's test).

    **STRUCTURALLY REQUIRED.**
12. **`IDENTITY["Sample"]["members"]` is `("Tessera", 2, "tessera_weight", 0.875)`.** The member
    table has no serial (02's design), so `find_row` cannot address a member row. The set is
    varied through the Tessera its members name.
    - Tessera 2 is a member of Samples 1 and 2 only.
    - The variation changes `members` and Tessera's records, and no other class's.

    **STRUCTURALLY REQUIRED.**
13. **`IDENTITY["Weave"]["strands"]` varies strand 701's `anchor_serial` (1 → 2).**
    - It first varied strand 702's `origin_serial` (3 → 1). With that, breakage (k), the parent
      set without its `anchor` member, **failed nothing** (`Ran 353 tests … OK`).
    - The anchor member is the field whose name the key parent shares, so it is the one varied.
    - Now (k) fails `test_each_identity_column_changes_the_records (cls='Weave',
      field='strands')`. The origin member is no longer varied (§7 item 1).

    **IMPLEMENTATION CHOICE.**
14. **`TestDuplicates.test_across_shards`' chain tuple is empty** (`for table, column in ():`).
    Trace 1's parents (its keypoint and its frame) are replicated, so there is no same-shard row
    to copy. The comment says so.
    - R-count of the tuple, which lists the chain as measured.
    - The loop stays, so the control flow is SGK's. The port check cannot see that the loop runs
      zero times (§7 item 3).

    **IMPLEMENTATION CHOICE** (following the note's preference for `Trace`).
15. **`FACTORIES` is the client's directory** (`REPO_ROOT / "datastorekit" / "tests" / "client"`),
    and the test's `glob("*.py")` is unchanged. Only `factories.py` there defines
    `inventory_spec`, and the test skips `base.py` as before. This keeps the test body SGK's.
    **IMPLEMENTATION CHOICE** (R-help).
16. **`builders` is compared with 12, not `len(INVENTORY_CLASSES)`** (13). The client's
    `_label_factory` defines one `inventory_spec` for `version` and `store_tag` (hazard 9). A
    comment says so. **STRUCTURALLY REQUIRED** (R-count).
17. **`TestReadOnlyAndNoRay.test_no_ray`'s child prints `'sample'`** where SGK printed `'qsi'`, an
    abbreviation of `QuadSourceIntegral`. Expected `{"ray": False, "sample": 3}` (R-map, R-count).
    **IMPLEMENTATION CHOICE.**
18. **`TestStandinStore` keeps SGK's gets**, though the Sample takes none of them, as 03a's
    deviation 8:
    - `atol` and `rtol` (`build.get_gauge` 10 and 9);
    - `policy` (`build.get_rule`).

    Its alias is stored by `object_store(build.make_alias(k, 1.5))`, as SGK stored its exit time
    by `object_store`. **IMPLEMENTATION CHOICE.**
19. **`test_store_schema` and `test_store_reader`, by role:**
    - `GK_SOURCE_TABLES` (`:62`) becomes the `samples` drop group's three tables, `("Sample_tags",
      "Sample_members", "Sample")`, where SGK's had four (`Sample` has no value table). The
      constant keeps its name.
    - The pair given in reverse declaration order (`:151`) is `["Weave_tags", "Sample_members"]`:
      `OneLoopIntegral_tags` → `Weave_tags`, `GkSource_parents` → `Sample_members`. `Weave_tags`
      is declared after `Sample_members`, so the point of `:166` holds.
    - `GkSource` (an extra column) → `Sample`; `OneLoopIntegral` → `Weave`;
      `QuadSourceIntegral_tags` → `Sample_tags`.
    - `GkSourcePolicy` → `routing_rule`, and `tolerance` → `routing_rule`.

    **IMPLEMENTATION CHOICE.**
20. **The run tag's label is `fixture-run`**, chosen so that every tag tuple keeps SGK's sorted
    order. **IMPLEMENTATION CHOICE** (R-value).
21. **Prose by R-map.**
    - `test_foreign_key_check`'s docstring describes the neutral added rows, the stand-in store
      and the references the check cannot see (`Sample.anchor_serial`, `Weave.anchor_serial`,
      `shard_keys`), in place of SGK's.
    - `test_store_schema`'s item 5 names `samples` and `routing_rule`.
    - The ported comments of `test_store_inventory` (`IDENTITY`, `TestTags`, `TestDuplicates`)
      describe the neutral rows.
    - SGK's campaign references stay as provenance.

    **IMPLEMENTATION CHOICE.**
22. **The client's docstrings change by addition**: the registry's role table and drop-group
    paragraph, the factories' module docstring, the new classes and helpers. **IMPLEMENTATION
    CHOICE.**
23. **`Gadget_factory._validate_row` reads the label in a second query inside `if not
    validated:`**, so that the existing query is unchanged. **IMPLEMENTATION CHOICE.**
24. **`Weave_factory.build` matches a `None` anchor with `IS NULL`.** Its `strands` come back as
    `SerialHandle` pairs, as `Sample`'s members do. **IMPLEMENTATION CHOICE.**
25. **`black`** re-wrapped lines whose length the map changed, and collapsed `WITNESS = (…)` to
    one line. **STRUCTURALLY REQUIRED** (`CLAUDE.md`).

No UNINTENDED DRIFT is in the committed diff. Two slips were caught before anything depended on
them:
- a heredoc whose backticks the shell expanded wrote nothing;
- a replacement of `WITNESS = (` that no longer matched left `_factories` undefined, and the test
  module said so on its first run.

## 3. The eleven hazards (§2.2)

1. **`build.build_store` cannot stand for the fixture. It holds.**
   - Re-measured twice per shard count: `build_store`'s two dial settings came out serials 1 and
     2, then 1 and 501, at 2 shards, and 1 and 501, then 1 and 2, at 3. The note's
     correction 3 had 1 and 501 at both.
   - The Samples sat at {0: [21, 22], 1: [1, 2]} at 2 shards, and at {0: [21, 22], 1: [41],
     2: [1]} at 3.
   - The timestamps are wall-clock (2026-10-08 17:27:49…).
   - So every test SGK built with `real_store_fixtures` uses the ported fixture. Only
     `TestStandinStore` keeps the pool.
2. **A copied record with a parent set.** All four `TestDuplicates` tests use `Trace`, which has
   no parent set, so no member rows are copied. Probed: each of the 33 identity variations and 17
   non-identity variations gives no problem (§1.6).
3. **Validated if and only if it has values.** It holds after U18. `Gadget` and `Trace` have both;
   `Sample` and `Weave` have neither.
4. **A common tag.** Every tagged record carries `fixture-run`, and `unused-tag` is carried by no
   row.
5. **Divergence through dependents.** The divergence tests use `routing_rule` (no dependents) and
   `Gadget` (tag set and value count, which a dependent's digest does not cover). Each `set(problems)`
   holds.
6. **`DROP COLUMN`.** `missing_columns` names `Trace.step_count`, a plain column. It drops, and
   the refusal names it.
7. **Consistent counts.** They hold in every row set (§1.5).
8. **`references()` and `relabel_serials`.**
   - `references()` is derived (§1.4). It covers `Sample.anchor_serial` → `Tessera`,
     `Weave.anchor_serial` → `Tessera`, the polymorphic `frame_serial` and `Weave_members`'
     members.
   - `relabel_serials` remaps shard keys through `mapping["keypoint"]`.
   - `Sample_members` (no serial) is relabelled through its references.
   - Measured: the relabelled full store's records equal the base's, with no problem, and
     `test_a_relabelled_store_passes` passes.
9. **`inventory_spec` definitions.** There are 12 in `factories.py` for 13 classes (deviation 16).
10. **`TestStandinStore`.** It holds, in the test itself:
    - exactly one violation, `('Sample', 1, 'Gadget')`, on the shard that holds the Sample;
    - none on the other shards;
    - one `keypoint` row on every shard.

    `exit_rows` reads `keypoint` (a partial role: the sharded row names the keypoint, not the
    alias).
11. **The ripple of §2.3.** It reached 02's literals, as §2.3 allows, and 03a's drop list (U19).
    - 03b's modules are unedited, and pass, including `test_read_only_pool` on
      `reader.build_full_store`, which now writes Traces and a Weave.
    - The Gadget warning is printed where 03a's tests validate an unvalidated Gadget. No test
      compares that output.

## 4. Verification performed

### 4.1 The suite (§3.1)

`./venv/bin/python -m unittest discover -s datastorekit/tests -t .`, in the foreground, with the
output written to the scratchpad.

**Before: `Ran 268 tests … OK`. After: `Ran 353 tests` / `OK`**, which is 268 + 85.

Along the way:

| Point in the work | Result |
|---|---|
| step 1 (client, literals, U19, contract) | 268 OK |
| step 2 (`schema_description`) | 268 OK |
| step 3 (fixture, `test_store_schema`, `test_store_reader`) | 296 OK |
| step 4 (`test_foreign_key_check`, `test_schema_builder` after U20) | 311 OK |
| step 5 | 353 OK |

- **Names.** All 268 test ids of before are present after (`comm` over the loader's ids: none
  missing). The 85 new ids are 42, 13, 15, 8 and 7 by module.
- **Toolchain.** Python 3.12.15, `ray==2.43.0`, `SQLAlchemy==2.0.39`, `black==25.1.0`,
  SQLite 3.53.4.
- **Isolation.** No Ray process was up at any point (`pgrep -lf 'gcs_server|raylet|ray::'`
  empty), and every store was in a `tempfile` directory.

**Control flow, measured.** The agent's own `ast` comparison covers all 176 functions of SGK's
seven files. It compares the sequence of `If`, `For`, `While`, `With` (with its item count),
`Try`, `Return`, `Raise`, `Break`, `Continue`, conditional expressions, comprehensions, lambdas
and nested `def`s.
- **Equal to SGK's** for every function of the five test modules.
- **The fixtures differ only where the prompt allows:**
  - `_tk_numeric` and `_gk_source_parents` are gone, and `_trace`, `_members`, `_weave_members`
    and `_polymorphic` are new;
  - `_full_shard0` and `_full_shard1` lost their list comprehensions (new rows);
  - `references` is derived;
  - `actor_with_built_schema` gained U20's dict comprehension.

### 4.2 The loader's run counts (§2.6, §3.4)

`unittest.TestLoader().loadTestsFromName('datastorekit.tests.<module>').countTestCases()`:

| Module | Run count |
|---|---|
| `test_store_inventory` | **42** |
| `test_store_schema` | **13** |
| `test_store_reader` | **15** |
| `test_foreign_key_check` | **8** |
| `test_schema_builder` | **7** |

### 4.3 The port check (§3.2)

`./venv/bin/python docs/extraction/compare_ported_tests.py`, exit **0**. Its whole output:

```
source:  /Users/ds283/Documents/Code/SecondaryGWKit at 6f7f291e857265e429f5d6f810124fd3bf57ce55 Record the orchestrator's review of datastore-generic-followup prompt 03
package: /Users/ds283/Documents/Code/DatastoreKit

datastorekit/tests/test_replicated_write.py (from Datastore/tests/test_replicated_write.py): ok
  tests: 25 (source 25)
  classes: 9 (source 9)
  functions compared: 32
  assertions: 125
datastorekit/tests/test_reconcile_at_open.py (from Datastore/tests/test_reconcile_at_open.py): ok
  tests: 41 (source 41)
  classes: 9 (source 9)
  functions compared: 52
  assertions: 148
datastorekit/tests/test_prune_at_open.py (from Datastore/tests/test_prune_at_open.py): ok
  tests: 10 (source 10)
  classes: 7 (source 7)
  functions compared: 16
  assertions: 74
datastorekit/tests/test_version_row_at_open.py (from Datastore/tests/test_version_row_at_open.py): ok
  tests: 12 (source 12)
  classes: 7 (source 7)
  functions compared: 16
  assertions: 79
datastorekit/tests/test_read_only_pool.py (from Datastore/tests/test_read_only_pool.py): ok
  tests: 23 (source 23)
  classes: 5 (source 5)
  functions compared: 27
  assertions: 138
datastorekit/tests/test_one_timestamp_per_write.py (from Datastore/tests/test_one_timestamp_per_write.py): ok
  tests: 1 (source 1)
  classes: 9 (source 9)
  functions compared: 5
  assertions: 7
datastorekit/tests/test_absolute_shard_record_refused.py (from Datastore/tests/test_absolute_shard_record_refused.py): ok
  tests: 12 (source 12)
  classes: 3 (source 3)
  functions compared: 14
  assertions: 28
datastorekit/tests/test_closed_store_refusals.py (from Datastore/tests/test_closed_store_refusals.py): ok
  tests: 5 (source 5)
  classes: 3 (source 3)
  functions compared: 7
  assertions: 21
datastorekit/tests/test_store_inventory.py (from Datastore/tests/test_store_inventory.py): ok
  tests: 42 (source 42)
  classes: 12 (source 12)
  functions compared: 44
  assertions: 127
datastorekit/tests/test_store_schema.py (from Datastore/tests/test_store_schema.py): ok
  tests: 13 (source 13)
  classes: 8 (source 8)
  functions compared: 17
  assertions: 64
datastorekit/tests/test_store_reader.py (from Datastore/tests/test_store_reader.py): ok
  tests: 15 (source 15)
  classes: 6 (source 6)
  functions compared: 17
  assertions: 65
datastorekit/tests/test_foreign_key_check.py (from Datastore/tests/test_foreign_key_check.py): ok
  tests: 8 (source 8)
  classes: 4 (source 4)
  functions compared: 8
  assertions: 25
datastorekit/tests/test_schema_builder.py (from Datastore/tests/test_schema_builder.py): ok
  tests: 7 (source 7)
  classes: 4 (source 4)
  functions compared: 8
  assertions: 29
datastorekit/tests/real_store_fixtures.py (from Datastore/tests/real_store_fixtures.py): ok
  tests: 0 (source 0)
  classes: 1 (source 1)
  functions compared: 0
  assertions: 0
datastorekit/tests/schema_description.py (from Datastore/tests/schema_description.py): ok
  tests: 0 (source 0)
  classes: 0 (source 0)
  functions compared: 0
  assertions: 0

OK: 15 module(s) keep their source's tests, classes and assertion skeletons
```

The seven new modules' counts equal the note's measurement of SGK's:

| Module | Counts |
|---|---|
| `test_store_inventory` | 42/12/44/127 |
| `test_store_schema` | 13/8/17/64 |
| `test_store_reader` | 15/6/17/65 |
| `test_foreign_key_check` | 8/4/8/25 |
| `test_schema_builder` | 7/4/8/29 |
| `real_store_fixtures` | 0/1/0/0 |
| `schema_description` | 0/0/0/0 |

The eight modules of before are unchanged.

### 4.4 The equivalence check (§3.3)

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
files ported, checked by compare_ported_tests.py: 15
files with no source, declared: 9
ported: checked by compare_ported_tests.py: datastorekit/tests/test_replicated_write.py (from Datastore/tests/test_replicated_write.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_reconcile_at_open.py (from Datastore/tests/test_reconcile_at_open.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_prune_at_open.py (from Datastore/tests/test_prune_at_open.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_version_row_at_open.py (from Datastore/tests/test_version_row_at_open.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_read_only_pool.py (from Datastore/tests/test_read_only_pool.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_one_timestamp_per_write.py (from Datastore/tests/test_one_timestamp_per_write.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_absolute_shard_record_refused.py (from Datastore/tests/test_absolute_shard_record_refused.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_closed_store_refusals.py (from Datastore/tests/test_closed_store_refusals.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_store_inventory.py (from Datastore/tests/test_store_inventory.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_store_schema.py (from Datastore/tests/test_store_schema.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_store_reader.py (from Datastore/tests/test_store_reader.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_foreign_key_check.py (from Datastore/tests/test_foreign_key_check.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_schema_builder.py (from Datastore/tests/test_schema_builder.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/real_store_fixtures.py (from Datastore/tests/real_store_fixtures.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/schema_description.py (from Datastore/tests/schema_description.py)
not compared (no source, declared): datastorekit/tests/client/__init__.py
not compared (no source, declared): datastorekit/tests/client/build.py
not compared (no source, declared): datastorekit/tests/client/factories.py
not compared (no source, declared): datastorekit/tests/client/objects.py
not compared (no source, declared): datastorekit/tests/client/reader.py
not compared (no source, declared): datastorekit/tests/client/registry.py
not compared (no source, declared): datastorekit/tests/test_neutral_client.py
not compared (no source, declared): datastorekit/tests/test_package_imports.py
not compared (no source, declared): datastorekit/tests/test_shard_key_assignment.py

Lines listed: D-fmt always, UNCLASSIFIED always, the rest with --show.
datastorekit/tests/test_sharded_store_script.py (from Datastore/tests/test_sharded_store_script.py):
  D-fmt         source line removed or changed  Datastore/tests/test_sharded_store_script.py:27: 
datastorekit/tests/standin_pool.py (from Datastore/tests/standin_pool.py):
  D-fmt         source line removed or changed  Datastore/tests/standin_pool.py:419: 
  D-fmt         source line removed or changed  Datastore/tests/standin_pool.py:420: 

OK: every differing line is classified, and every file is accounted for
```

Against its output before, only these change:
- the seven new `ported` lines;
- the count of ported files, from 8 to 15.

The table over the 31 compared files and its totals are unchanged, and 9 files have no source
(55 tracked `.py` files under `datastorekit/`).

### 4.5 The vocabulary (§3.5, and the second grep)

- **The 80 names.** These are log 02 §1.2's 82, less `version` and `store_tag`, matched as whole
  identifiers. They were searched for over:
  - the five modules and the two fixtures;
  - `client/objects.py`, `factories.py`, `registry.py` and `build.py`.

  **None** was found. The same search over SGK's files matches:

  | SGK file | Lines matched |
  |---|---|
  | `test_store_inventory` | 284 |
  | `test_store_schema` | 25 |
  | `test_store_reader` | 9 |
  | `test_foreign_key_check` | 34 |
  | `test_schema_builder` | 12 |
  | `real_store_fixtures` | 102 |
  | `schema_description` | 0 |

  These are the note's figures.
- **The second grep.** `CosmologyModels`, `CosmologyConcepts`, `ComputeTargets`, `extract_common`,
  `config\.`, `Planck2018`, `k_inv_Mpc`, `log10_tol`, `cosmology_type`, `cosmology_serial`,
  `model_serial` and `Run_fixture`, over the same files: **no hit.**
  - SGK's seven match 33, 1, 2, 1, 1, 50 and 1 lines, the note's figures.
  - The method: whole identifiers, with `config\.` matched without a trailing word boundary. A
    `grep -w` reading of `config\.` misses `config.datastore`.
  - The imports inside test bodies (`config.sharding`, `:419`; `store_inventory_tables`,
    `:530-534`) are R-imp.

### 4.6 `black` (§3.7)

`./venv/bin/black --check datastorekit docs/extraction` (25.1.0) gives `57 files would be left
unchanged.`

## 5. The breakage method

Each diff was made as follows:
1. The work was staged by explicit path.
2. One file was edited, and `git diff` taken of it against the index.
3. The file was restored from the index (`mkbreak.py` in the scratchpad).

Each diff was then run through `runbreak.sh` in `bash`:
1. checked with `git apply --check`;
2. applied with `git apply`;
3. checked with `git apply -R --check`;
4. run;
5. reverted with `git apply -R`.

After each, `git diff` was empty and nothing was untracked. The diffs below are byte-for-byte the
files that were applied, trailing context lines included. Each was checked again both ways
against the final staged tree (they differ from the first set only in their `index` lines). None
is committed.

- The checks' breakages ran their check.
- (d)–(l) ran the whole suite, on the final tree.

## 6. The deliberate-breakage record (§3.6)

### 6.1 The checks

**(a)** One `assertEqual` is deleted from `TestDuplicates.test_a_replicated_class`.
`compare_ported_tests.py` exits **1**, naming the test:

```diff
diff --git a/datastorekit/tests/test_store_inventory.py b/datastorekit/tests/test_store_inventory.py
index 1efebbb..072280f 100644
--- a/datastorekit/tests/test_store_inventory.py
+++ b/datastorekit/tests/test_store_inventory.py
@@ -853,7 +853,6 @@ class TestDuplicates(_Stores):
     def test_a_replicated_class(self):
         inventory = self._duplicate("routing_rule", 1, 4, None)
         self.assertEqual(kinds(inventory["routing_rule"].problems), ["duplicate"])
-        self.assertEqual(inventory["routing_rule"].count, 4)
 
     def test_other_tags_are_not_a_duplicate(self):
         replicated, sharded, keys = full_rows()
```
```
  DIFFERS  TestDuplicates.test_a_replicated_class: skeleton differs at position 2: the source has assertEqual, the package (nothing) (2 in the source, 1 in the package)
FAIL: 1 of 15 module(s) differ from their source
exit 1
```

**(b)** A `raise AssertionError` is added to `real_store_fixtures.with_rows`. It exits **1**:
"asserts in the package …, and not in the source".

```diff
diff --git a/datastorekit/tests/real_store_fixtures.py b/datastorekit/tests/real_store_fixtures.py
index d386be8..3d89b60 100644
--- a/datastorekit/tests/real_store_fixtures.py
+++ b/datastorekit/tests/real_store_fixtures.py
@@ -188,6 +188,8 @@ class RealStore:
 
 def with_rows(base: RowSet, extra: RowSet) -> RowSet:
     """A copy of ``base`` with ``extra``'s rows appended, table by table."""
+    if not isinstance(base, dict):
+        raise AssertionError("a row set is a dict")
     out = copy.deepcopy(base)
     for table, rows in extra.items():
         out.setdefault(table, []).extend(copy.deepcopy(rows))
```
```
  DIFFERS  with_rows: asserts in the package (raise AssertionError), and not in the source
FAIL: 1 of 15 module(s) differ from their source
exit 1
```

**(m)** The same, in `schema_description._name`. It exits **1**:

```diff
diff --git a/datastorekit/tests/schema_description.py b/datastorekit/tests/schema_description.py
index 5b6ac74..e0cecd6 100644
--- a/datastorekit/tests/schema_description.py
+++ b/datastorekit/tests/schema_description.py
@@ -40,6 +40,8 @@ _DIALECT = sqlite.dialect()
 
 def _name(value) -> Any:
     """A constraint's or index's name, or None for an unnamed one (SQLAlchemy's sentinel)."""
+    if value is Ellipsis:
+        raise AssertionError("no name")
     return str(value) if isinstance(value, str) else None
 
 
```
```
  DIFFERS  _name: asserts in the package (raise AssertionError), and not in the source
FAIL: 1 of 15 module(s) differ from their source
exit 1
```

**(c)** `real_store_fixtures` is removed from `FILES`. `compare_with_source.py` exits **1**:

```diff
diff --git a/docs/extraction/compare_with_source.py b/docs/extraction/compare_with_source.py
index 45f6aaf..639db8e 100644
--- a/docs/extraction/compare_with_source.py
+++ b/docs/extraction/compare_with_source.py
@@ -174,7 +174,6 @@ FILES: List[Tuple[str, str, str]] = (
             "test_store_reader",
             "test_foreign_key_check",
             "test_schema_builder",
-            "real_store_fixtures",
             "schema_description",
         )
     ]
```
```
files ported, checked by compare_ported_tests.py: 14
not compared (NOT ACCOUNTED FOR): datastorekit/tests/real_store_fixtures.py
FAIL: 1 file(s) under datastorekit/ not accounted for
exit 1
```

### 6.2 The layer and the client, through the ported tests

Each case gives the diff, then the failing tests.

**For each of (d)–(i), whether SGK's counterpart pins the same line** is by reading SGK's test,
which makes the same assertion on the same layer line. It was not run: SGK is never run.

**(d)** `canonical` formats a float with `repr` (`store_inventory.py:133`):

```diff
diff --git a/datastorekit/store_inventory.py b/datastorekit/store_inventory.py
index 10b46da..64cfc04 100644
--- a/datastorekit/store_inventory.py
+++ b/datastorekit/store_inventory.py
@@ -130,7 +130,7 @@ def canonical(value: Any) -> Any:
     if value is None or isinstance(value, (bool, int, str)):
         return value
     if isinstance(value, float):
-        return float.hex(value)
+        return repr(value)
     raise TypeError(
         f"canonical(): no canonical form for a leaf of type {type(value).__name__!r} ({value!r})"
     )
```
`Ran 353 tests in 73.277s` / `FAILED (failures=5)`. The tests that fail:

- `FAIL test_store_inventory.TestFloats.test_canonical`
- `FAIL test_store_inventory.TestFloats.test_canonical_json`
- `FAIL test_store_inventory.TestFloats.test_every_float_leaf_goes_through_canonical`
- `FAIL test_store_inventory.TestFloats.test_log10_tol_is_used_as_stored`
- `FAIL test_store_inventory.TestFloats.test_only_canonical_formats_a_float`

Each SGK counterpart pins the same line.

**(e)** No `orphan-value` is reported (`store_inventory.py:658`, made false):

```diff
diff --git a/datastorekit/store_inventory.py b/datastorekit/store_inventory.py
index 10b46da..6033d4e 100644
--- a/datastorekit/store_inventory.py
+++ b/datastorekit/store_inventory.py
@@ -655,7 +655,7 @@ def read_records(
                 counts[parent] = n
             else:
                 orphans[parent] = n
-        if len(orphans) > 0:
+        if len(orphans) < 0:
             problems.append(
                 _problem(
                     "orphan-value",
```
`Ran 353 tests in 74.556s` / `FAILED (failures=1)`. The tests that fail:

- `FAIL test_store_inventory.TestOldStoresAndOrphans.test_an_orphan_value_row`

SGK's `test_an_orphan_value_row` pins the same line.

**(f)** A key held twice is not a duplicate (`store_inventory.py:880`, `> 1` → `> 2`):

```diff
diff --git a/datastorekit/store_inventory.py b/datastorekit/store_inventory.py
index 10b46da..fa19d3f 100644
--- a/datastorekit/store_inventory.py
+++ b/datastorekit/store_inventory.py
@@ -877,7 +877,7 @@ def _combine(
     by_identity: Dict[str, List[Tuple[int, int]]] = {}
     for s, serial, record, _ in rows:
         by_identity.setdefault(record.identity(), []).append((s, serial))
-    duplicated = {i: where for i, where in by_identity.items() if len(where) > 1}
+    duplicated = {i: where for i, where in by_identity.items() if len(where) > 2}
     if len(duplicated) > 0:
         examples = [
             f"shard/serial {', '.join(f'#{s}/{serial}' for s, serial in sorted(where))}"
```
`Ran 353 tests in 70.343s` / `FAILED (failures=3)`. The tests that fail:

- `FAIL test_store_inventory.TestDuplicates.test_a_replicated_class`
- `FAIL test_store_inventory.TestDuplicates.test_across_shards`
- `FAIL test_store_inventory.TestDuplicates.test_on_one_shard`

The fourth test, `test_other_tags_are_not_a_duplicate`, passes, as it should: it expects no
duplicate. SGK's three pin the same line.

**(g)** `schema_differences` ignores an absent column (`SQL/schema.py:468`):

```diff
diff --git a/datastorekit/SQL/schema.py b/datastorekit/SQL/schema.py
index 25e44ba..069dd43 100644
--- a/datastorekit/SQL/schema.py
+++ b/datastorekit/SQL/schema.py
@@ -465,7 +465,7 @@ def schema_differences(conn, tables: Mapping[str, sqla.Table]) -> SchemaDifferen
         declared = [c.name for c in table.columns]
         absent = tuple(c for c in declared if c not in file_columns)
         extra = tuple(c for c in file_columns if c not in declared)
-        if len(absent) > 0:
+        if len(absent) < 0:
             absent_columns[name] = absent
         if len(extra) > 0:
             extra_columns[name] = extra
```
`Ran 353 tests in 69.542s` / `FAILED (failures=3, errors=2)`. The tests that fail:

- `ERROR test_store_schema.TestThePrimaryIsRefused.test_an_extra_table_and_a_missing_column (case='a missing column', read_only=False)`
- `ERROR test_store_schema.TestThePrimaryIsRefused.test_an_extra_table_and_a_missing_column (case='a missing column', read_only=True)`
- `FAIL test_store_reader.TestADifferingSchemaIsRefused.test_a_missing_table_or_column_is_refused_naming_the_shard (shape='a missing column')`
- `FAIL test_store_schema.TestSchemaDifferences.test_each_kind_is_found_on_the_right_shard_by_name`
- `FAIL test_store_schema.TestTheReadWriteOpenRefuses.test_an_absent_column_an_extra_column_and_an_extra_table (case='an absent column')`

The two errors are the primary's missing column: the open is no longer refused, and the pool
fails later. SGK's counterparts pin the same line.

**(h)** `read_only_url` drops `mode=ro` (`store_reader.py:114`):

```diff
diff --git a/datastorekit/store_reader.py b/datastorekit/store_reader.py
index 46de102..32b6ef0 100644
--- a/datastorekit/store_reader.py
+++ b/datastorekit/store_reader.py
@@ -111,7 +111,7 @@ def _refuse_journals(primary: Path, path: Path, what: str) -> None:
 
 def read_only_url(path: Path) -> str:
     """The SQLAlchemy URL of ``path`` opened read-only: ``mode=ro``, never ``immutable=1``."""
-    return f"sqlite:///file:{path}?mode=ro&uri=true"
+    return f"sqlite:///file:{path}?uri=true"
 
 
 def _read_only_engine(path: Path) -> sqla.Engine:
```
`Ran 353 tests in 70.875s` / `FAILED (failures=8)`. The tests that fail:

- `FAIL test_read_only_pool.TestAtOpen.test_every_connection_is_opened_read_only`
- `FAIL test_read_only_pool.TestOtherWritesRaiseReadOnlyWrite.test_the_backstop_a_flag_update_on_a_hit`
- `FAIL test_store_reader.TestReaderNeverWrites.test_a_write_through_a_reader_engine_raises`
- `FAIL test_store_reader.TestReaderNeverWrites.test_a_write_through_a_reader_engine_raises (shard=0, what='ddl')`
- `FAIL test_store_reader.TestReaderNeverWrites.test_a_write_through_a_reader_engine_raises (shard=0, what='insert')`
- `FAIL test_store_reader.TestReaderNeverWrites.test_a_write_through_a_reader_engine_raises (shard=1, what='ddl')`
- `FAIL test_store_reader.TestReaderNeverWrites.test_a_write_through_a_reader_engine_raises (shard=1, what='insert')`
- `FAIL test_store_reader.TestReaderReads.test_engines_open_mode_ro_and_never_immutable`

Of the five modules, `test_store_reader`'s three fail. 03b's two fail too, as the note probed.
SGK's `test_engines_open_mode_ro_and_never_immutable` and `test_a_write_through_a_reader_engine_raises`
pin the same line.

**(i)** The prepended `version` column is not indexed (`SQL/schema.py:131`):

```diff
diff --git a/datastorekit/SQL/schema.py b/datastorekit/SQL/schema.py
index 25e44ba..d7ea23a 100644
--- a/datastorekit/SQL/schema.py
+++ b/datastorekit/SQL/schema.py
@@ -129,7 +129,6 @@ def build_schema(metadata: sqla.MetaData, factories: Mapping[str, Any]) -> Built
                 "version",
                 sqla.Integer,
                 sqla.ForeignKey(f"{VERSION_TABLE}.serial"),
-                index=True,
             )
             tab.append_column(version_col)
             schema["version_col"] = version_col
```
`Ran 353 tests in 68.325s` / `FAILED (failures=16)`. The tests that fail:

- `FAIL test_schema_builder.TestSchemaIsUnchanged.test_actor_build_schema_reproduces_the_witness`
- `FAIL test_schema_builder.TestSchemaIsUnchanged.test_actor_build_schema_reproduces_the_witness (cls='Gadget')`
- `FAIL test_schema_builder.TestSchemaIsUnchanged.test_actor_build_schema_reproduces_the_witness (cls='keypoint_alias')`
- `FAIL test_schema_builder.TestSchemaIsUnchanged.test_actor_build_schema_reproduces_the_witness (cls='routing_rule')`
- `FAIL test_schema_builder.TestSchemaIsUnchanged.test_actor_build_schema_reproduces_the_witness (cls='Sample')`
- `FAIL test_schema_builder.TestSchemaIsUnchanged.test_actor_build_schema_reproduces_the_witness (cls='Tessera')`
- `FAIL test_schema_builder.TestSchemaIsUnchanged.test_actor_build_schema_reproduces_the_witness (cls='Trace')`
- `FAIL test_schema_builder.TestSchemaIsUnchanged.test_actor_build_schema_reproduces_the_witness (cls='Weave')`
- `FAIL test_schema_builder.TestSchemaIsUnchanged.test_build_schema_reproduces_the_witness`
- `FAIL test_schema_builder.TestSchemaIsUnchanged.test_build_schema_reproduces_the_witness (cls='Gadget')`
- `FAIL test_schema_builder.TestSchemaIsUnchanged.test_build_schema_reproduces_the_witness (cls='keypoint_alias')`
- `FAIL test_schema_builder.TestSchemaIsUnchanged.test_build_schema_reproduces_the_witness (cls='routing_rule')`
- `FAIL test_schema_builder.TestSchemaIsUnchanged.test_build_schema_reproduces_the_witness (cls='Sample')`
- `FAIL test_schema_builder.TestSchemaIsUnchanged.test_build_schema_reproduces_the_witness (cls='Tessera')`
- `FAIL test_schema_builder.TestSchemaIsUnchanged.test_build_schema_reproduces_the_witness (cls='Trace')`
- `FAIL test_schema_builder.TestSchemaIsUnchanged.test_build_schema_reproduces_the_witness (cls='Weave')`

These are the classes with a `version` column: `keypoint_alias`, `routing_rule`, `Gadget`,
`Tessera`, `Sample`, `Trace`, `Weave`. SGK's two witness tests pin the same line.

**(j)** `Trace`'s spec without `values`:

```diff
diff --git a/datastorekit/tests/client/factories.py b/datastorekit/tests/client/factories.py
index 683fe9a..a391552 100644
--- a/datastorekit/tests/client/factories.py
+++ b/datastorekit/tests/client/factories.py
@@ -1463,7 +1463,6 @@ class Trace_factory(SQLAFactoryBase):
                 ),
             },
             tags=("Trace_tags", "trace_serial"),
-            values=("TraceStep", "trace_serial"),
             validated="trace_validated",
         )
 
```
`Ran 353 tests in 70.712s` / `FAILED (failures=4)`. The tests that fail:

- `FAIL test_store_inventory.TestOldStoresAndOrphans.test_an_orphan_value_row`
- `FAIL test_store_inventory.TestTheFullStore.test_classes_with_tags_validated_and_values (cls='Trace')`
- `FAIL test_store_inventory.TestValueCounts.test_deleting_a_value_row_lowers_one_count_by_one (table='TraceStep')`
- `FAIL test_store_inventory.TestValueCounts.test_the_counts_are_per_parent (cls='Trace')`

**(k)** `Weave`'s parent set without its `anchor` member:

```diff
diff --git a/datastorekit/tests/client/factories.py b/datastorekit/tests/client/factories.py
index 683fe9a..cb78cc2 100644
--- a/datastorekit/tests/client/factories.py
+++ b/datastorekit/tests/client/factories.py
@@ -1680,7 +1680,6 @@ class Weave_factory(SQLAFactoryBase):
                     "Weave_members",
                     "weave_serial",
                     {
-                        "anchor": Parent("anchor_serial", "Tessera", nullable=True),
                         "origin": Parent("origin_serial", "Trace", nullable=True),
                     },
                 )
```
`Ran 353 tests in 83.219s` / `FAILED (failures=1)`. The tests that fail:

- `FAIL test_store_inventory.TestIdentityColumnsMatter.test_each_identity_column_changes_the_records (cls='Weave', field='strands')`

With the first `IDENTITY["Weave"]["strands"]` (strand 702's origin varied), this diff failed
nothing (`Ran 353 tests` / `OK`). That is why the strand's anchor is varied instead (deviation 13).

**(l)** The full rows with no `Weave` row, and so none of its tags or strands (the orchestrator's
addition):

```diff
diff --git a/datastorekit/tests/real_store_fixtures.py b/datastorekit/tests/real_store_fixtures.py
index d386be8..3eb46cf 100644
--- a/datastorekit/tests/real_store_fixtures.py
+++ b/datastorekit/tests/real_store_fixtures.py
@@ -595,22 +595,6 @@ def _full_shard0() -> RowSet:
         _tags("Trace_tags", "trace_serial", 4, (1,)),
         _values("TraceStep", "trace_serial", 3, ((31, 1), (32, 2))),
         _values("TraceStep", "trace_serial", 4, ((41, 1),)),
-        # Weave 1 shares its serial with Trace 1, and carries different tags, so reading its tags
-        # from the wrong association table is visible
-        {
-            "Weave": [
-                {
-                    "serial": 1,
-                    "version": 1,
-                    "keypoint_serial": 1,
-                    "trace_serial": 4,
-                    "anchor_serial": None,
-                    "weave_label": "fixture-weave-1",
-                }
-            ]
-        },
-        _weave_members(1),
-        _tags("Weave_tags", "weave_serial", 1, (1, 5)),
     )
 
 
```
`Ran 353 tests in 74.163s` / `FAILED (failures=3, errors=7)`. The tests that fail:

- `ERROR test_store_inventory.TestIdentityColumnsMatter.test_each_identity_column_changes_the_records (cls='Weave', field='anchor')`
- `ERROR test_store_inventory.TestIdentityColumnsMatter.test_each_identity_column_changes_the_records (cls='Weave', field='k')`
- `ERROR test_store_inventory.TestIdentityColumnsMatter.test_each_identity_column_changes_the_records (cls='Weave', field='strands')`
- `ERROR test_store_inventory.TestIdentityColumnsMatter.test_each_identity_column_changes_the_records (cls='Weave', field='trace')`
- `ERROR test_store_inventory.TestIdentityColumnsMatter.test_each_identity_column_changes_the_records (cls='Weave', field='weave_label')`
- `ERROR test_store_inventory.TestNonIdentityDoesNotMatter.test_non_identity_columns (table='Weave', column='version')`
- `ERROR test_store_inventory.TestTags.test_oneloop_tags_come_from_its_own_table`
- `FAIL test_store_inventory.TestIdentityColumnsMatter.test_the_key_fields_are_the_lookup_columns (cls='Weave')`
- `FAIL test_store_inventory.TestTags.test_a_tagged_parents_digest_covers_its_tags`
- `FAIL test_store_inventory.TestTheFullStore.test_every_class_has_a_record (cls='Weave')`

`test_every_class_has_a_record` fails, as the note requires. The test reads the fixture's rows,
not a literal copied from them. The errors are `find_row`'s `KeyError` on the Weave rows that
`IDENTITY` and `NON_IDENTITY` address.

## 7. Observations not acted on

1. **The `origin` member of `Weave`'s parent set is no longer varied by any test.** A breakage
   that removed it would now fail nothing (deviation 13: each key field has one `IDENTITY`
   entry). Recorded, not opened: it is not one of the prompt's mutations. 04b's
   `test_inventory_declarations` checks the declarations themselves.
2. **A class whose `register()` is `None` makes the two schema records differ.** `build_schema`'s
   record has no `insert` key, and the actor's has `"insert": None`. So SGK's
   `TestSchemaIsUnchanged` cannot hold over a registry with such a class. This is the layer's
   behaviour, and `TestNoneRegistration` pins both shapes. U20 settles the test; the behaviour is
   inherited and left as it is.
3. **The port check's blind spot.** It compares assertion skeletons, not whether a loop runs.
   `test_across_shards`' chain loop runs zero times on the neutral rows (deviation 14), and the
   check cannot see that. The control-flow comparison (§4.1) sees the loop, not its count.
4. **`[01-package-prose-names-sgks-layout]`, re-measured** by log 03a §8's method.
   - **124 lines in 28 files at `ae94aaa`** (03b's figure, reproduced), and 114 in 23 at
     `72cf34a`.
   - **146 lines in 35 files after this prompt.** All the new lines are SGK's prose ported
     unchanged (03a §2.1):

     | File | Lines | At |
     |---|---|---|
     | `tests/schema_description.py` | 9 | `:3`, `:6`, `:9`, `:12`, `:15`, `:16`, `:20`, `:183`, `:184` |
     | `tests/test_store_reader.py` | 3 | `:2`, `:12`, `:182` |
     | `tests/test_store_schema.py` | 3 | `:2`, `:3`, `:411` |
     | `tests/test_foreign_key_check.py` | 2 | `:2`, `:4` |
     | `tests/test_schema_builder.py` | 2 | `:2`, `:9` |
     | `tests/test_store_inventory.py` | 2 | `:2`, `:702` |
     | `tests/real_store_fixtures.py` | 1 | `:29` |

     That is +22 lines in 7 new files. The client's files add none.
   - The ported prose's other SGK references, outside the pattern:
     - `var/`;
     - "store-fingerprint prompt 01/02";
     - `[00-quadsource-tq-serial-has-the-wrong-foreign-key]`;
     - "S1", "S2", "S4";
     - SGK's witness file names in `schema_description`.

   The issue's hook is updated.
5. **§2.4's "and one None"** Sample anchor is not in the full store (deviation 11).
6. **Two of hazard 1's figures differ from the note's.** The serials vary between runs; the
   conclusion holds.

## 8. Issues

- **Opened:** none. Every mutation of §3.6 fails a test.
- **Closed:** none.
- **Changed:** `[01-package-prose-names-sgks-layout]`, from 124 to **146 lines**, and from 28 to
  **35 files** (§7 item 4).

The index is at **6 open**: 2 on this board, 4 inherited.

## 9. State handed to the next prompt (04b)

- `HEAD` is `7ceed25`. The tree is clean, and `venv/` is unchanged.
- **The suite is 353** (`Ran 353 tests … OK`). 04b records 353 as its "before".
- **The checks.**
  - `compare_ported_tests.py` exits 0 over `PORTED`'s fifteen pairs.
  - `compare_with_source.py` exits 0: 31 compared, 15 `PORTED`, 9 with no source.
  - 04b adds `NOT_PORTED` (U16), and its modules join `PORTED` and `FILES`.
- **Hazard 1, for 04b.** Log 02's role table maps `real_store_fixtures.build_full_store` to
  `build.build_store`. That holds for none of 04a's five modules, and should not be assumed for
  04b's:
  - `build_store`'s serials are leased and vary between runs (a dial setting came out serial 2 or
    501);
  - its timestamps are wall-clock;
  - it takes no `replicated=`, `sharded=`, `shard_keys=`, `missing_*` or `extra_sql`.

  04b's modules that SGK built with `real_store_fixtures` use the ported fixture, whose names are:
  - `build_full_store`, `build_real_store`, `full_rows`, `with_rows`, `fill_required`;
  - `relabel_serials`, `find_row`, `vary_row`, `references`;
  - `file_state`, `expected_row_counts`, `independent_row_counts`;
  - `REPLICATED_ROWS`, `SHARDED_ROWS`, `SHARD_KEYS`, `FULL_*`, `FIXED_TIMESTAMP`, `RealStore`,
    `RowSet`.
- **For 04b's `test_inventory_declarations`:**
  - `Trace`'s `frame` declares **the same `FRAME_TYPES` object** as `Gadget`'s (`assertIs` holds
    by construction);
  - `Weave`'s parent set has a member field, `anchor`, that shares its name with a key parent;
  - `Gadget_factory` prints "did not validate after serialization" (`TestRevalidate`).
- **The drop groups:**

  | Group | Tables |
  |---|---|
  | `aliases` | `keypoint_alias` |
  | `tesserae` | `Tessera` |
  | `samples` | `Sample`, `Sample_tags`, `Sample_members` |
  | `gadgets` | `Gadget`, `Gadget_tags`, `GadgetPart` |
  | `traces` | the six, closed on its own |

  `aliases` and `tesserae` must now be dropped with `Weave`, `Weave_tags` and `Weave_members`.
- **The witness** is `datastorekit/tests/data/schema_at_extraction-04a.json`. It is never
  regenerated: a later schema change adds a new file, and `WITNESS` names it.
- **`schema_description.actor_with_built_schema` builds the actor from the registry's classes
  with a table** (U20).
