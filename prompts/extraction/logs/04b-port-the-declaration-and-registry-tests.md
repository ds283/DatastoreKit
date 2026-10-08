# Log 04b — port the declaration and registry tests, and write the package's guard

**Subject:** Port the declaration and registry tests and write the guard · **Commit:** `0c66505`
· **Date:** 2026-10-08 · **Model:** Claude Opus 5.5 · **Result:** landed.

SGK's `test_inventory_declarations` (25 of 26; U16's one test declared not ported),
`test_declared_facts` (25), `test_layer_registry` (20) and `test_drop_refuses_dangling_references`
(11) run in `datastorekit/tests/` under their names, on the neutral client and 04a's fixture. SGK's
`test_layer_is_generic` (8) is the package's guard. It reads the three clients' vocabulary from
`datastorekit/tests/data/client_vocabulary.json`, which `docs/extraction/measure_client_vocabulary.py`
measured from the clients by `git show` alone. It pins exactly one hit, the comment
`datastorekit/tools/shard_key_audit.py:188` (U17). The new `test_parent_set_members` (2) closes
`[04a-no-test-pins-a-second-parent-set-member]`.

`compare_ported_tests.py` gains `NOT_PORTED` and finds twenty modules equal to SGK's in tests,
classes, bases and assertion skeletons, with one test declared not ported. `compare_with_source.py`
accounts for the five as `PORTED` and the new module as having no source. `Ran 444 tests … OK`
(353 before). `[01-package-prose-names-sgks-layout]` is re-measured at 155 lines in 40 files. One
issue is closed and none is opened; the index goes from 7 to 6.

Prompt: [`../04b-port-the-declaration-and-registry-tests.md`](../04b-port-the-declaration-and-registry-tests.md),
with the orchestrator's dispatch note:
- the dispatch: five corrections, the additions (n), (o) and (p), a second run of the measuring
  script, and a work order;
- the addendum after the agent's stop: correction 6 (U22) and correction 7 (the fifth
  `NOT_PORTED` rule, kept).

The work stopped once for the user (§2 item 6). It was resumed from the uncommitted tree, and one
commit was made, at the end.

## 1. What shipped

- **Five ported modules**, each SGK's at `6f7f291` with only the changes of 03a §2.1, §2.3 and
  §2.4, and U22:
  - `datastorekit/tests/test_inventory_declarations.py`
  - `test_declared_facts.py`
  - `test_layer_registry.py`
  - `test_drop_refuses_dangling_references.py`
  - `test_layer_is_generic.py` (the guard, §1.4)

  Every class and method keeps its name (no R-name), and every class its bases.
- **One new module**, `datastorekit/tests/test_parent_set_members.py` (§2.6; §4 below).
- **The vocabulary**: `datastorekit/tests/data/client_vocabulary.json`, written by the new
  `docs/extraction/measure_client_vocabulary.py` (§1.4).
- **`docs/extraction/compare_ported_tests.py`**: `PORTED` gains the five pairs; `NOT_PORTED` and its
  rules are added (§1.5). `NAME_MAP` is unchanged.
- **`compare_with_source.py`**: `FILES` gains the five as `PORTED`, and `NO_SOURCE` gains
  `test_parent_set_members.py`. 01's to 04a's entries are unchanged.
- **The records**:
  - this log;
  - the board (header, §1's row, §3, §4);
  - `docs/OPEN_ISSUES.md`;
  - `prompts/INDEX.md`.

Nothing under `datastorekit/` outside `tests/` changed, nor did `datastorekit/tests/client/`,
`standin_pool.py`, `shard_store_fixtures.py`, `real_store_fixtures.py`, `schema_description.py`,
the witness, or any module 01–04a ported.

### 1.1 The map as used (§2.2)

Each row is the planner's unless it says otherwise. Columns move with their table (R-map).

| SGK | Used for | Neutral, as used | Changed from the planner's row? |
|---|---|---|---|
| `config.datastore.factories`, `drop_groups`, `tables_to_drop`; `config.sharding.replicated_tables`, `sharded_tables` | the registry | `datastorekit.tests.client.registry`, the same names | no |
| `BackgroundModel` (+`_tags`, `Value`; `validated`, `label`, `model_serial`) | the replicated owner | `Gadget` (+`Gadget_tags`, `GadgetPart`; `gadget_validated`, `gadget_label`, `gadget_serial`) | no |
| `redshift`, `wavenumber` (`source`, `response`) | the classes with `monotone_flags` | `keypoint` (`kp_marked`, `kp_flagged`), one class where SGK has two | no |
| `tolerance` | a replicated leaf with no dependents | `routing_rule` in `test_the_inventory_compares_exactly_the_recorded_classes`; `dial_setting` in the prune trigger, as `_PruneTestCase` has it | no |
| `LambdaCDM`, `QCD_Cosmology`; `COSMOLOGY_TYPES`, `LAMBDACDM_IDENTIFIER`, `QCD_EOS_IDENTIFIER`; `cosmology`, `cosmology_type` | the polymorphic parent | `dial_setting`, `knob_setting`; `factories.FRAME_TYPES`, `FRAME_KINDS["dial_setting"]`, `FRAME_KINDS["knob_setting"]`; `frame`, `frame_kind` | no |
| `wavenumber_exit_time`, `BackgroundModel` | the two referencing factories | `Gadget`, `Trace` | no |
| `GkWKBIntegration.numeric`; `GkSource`'s member `numeric` | a nullable key parent; a member field of the same name | `Weave.anchor`; `Weave`'s member `anchor` (one class, where SGK's are two) | no |
| `OneLoopIntegral` (+`_tags`) | a class a registry can leave out | `Weave` (+`Weave_tags`, `Weave_members`) | no |
| `QuadSourceIntegral` (+`_tags`) | a class left in | `Trace` (+`Trace_tags`) | no |
| `GkSource` | a sharded table a drop names | `Sample` (`DROP`, `test_an_undeclared_name_is_refused`) | no |
| `GkSourcePolicy` | a name with dependents beside an undeclared one | `Gadget` (hazard 9) | no |
| `QuadSourceIntegral` → `TkWKBIntegration`, no foreign key | a declared parent without a foreign key | `Sample` → `Tessera` (`anchor_serial`) | no |
| `GkSource_parents` → `GkNumericIntegration` | a foreign key without a declared parent | `Sample_members` → `Tessera` | no |
| `QuadSourceIntegral_tags` | a dependent behind the first level | `Sample_tags` (→ `Sample` → `Tessera`) | no |
| `BackgroundModelValue`, `GkSource_tags`, `GkSource_parents` | tables that declare no spec | `GadgetPart`, `Sample_tags`, `Sample_members` | no |
| `TkNumericValue`, `redshift` (batch sizes) | a table given a size, and one not given | `GadgetPart`, `keypoint` | no |
| the drop groups | `drop_groups` | `aliases`, `tesserae`, `samples`, `gadgets`, `traces`; `tk-wkb` ×2 → `samples` ×2, `gk-source-policy`, `tk-numeric` → `gadgets`, `tesserae` | no |
| `REFUSED_GROUP` `gk-source-policy-records`; `WITH_ITS_DEPENDENTS` | a sharded refused group | `tesserae`; `[REFUSED_GROUP, "samples", "traces"]` | no |

`version` and `store_tag` keep their names. Two local variables named for SGK's vocabulary were
renamed with their table: `tolerance` → `routing_rule` (in
`test_the_inventory_compares_exactly_the_recorded_classes`) and `tk_numeric` → `tesserae` (in
`test_dependents_are_followed_transitively`). Neither asserts.

### 1.2 The port table (§4.5)

One row per test (89), in SGK's file order. **"Kinds in the test"** are the changes inside the
method, found by comparing its `ast` with SGK's ("—": unchanged). Every test also runs under its
module's changes, in the fourth column.

U16's test, **not ported**: `test_inventory_declarations` · `TestResolve` ·
`test_the_report_renders_both_cosmology_types`, which "asserts on SGK's `tools.inventory_report`,
which stays in SGK (README §1)". It is declared in `NOT_PORTED` (§1.5). Its skeleton is
`assertNotIn, assertEqual, subTest, assertIn, assertEqual`. The module's `import re`, used only by
it, is removed (R-imp), as is the import of `format_inventory_report`.

| # | SGK origin (module · class · method) | Kinds in the test | Module's changes | SGK → neutral |
|---|---|---|---|---|
| 1 | `test_inventory_declarations` · `TestTheDerivedOrder` · `test_it_is_the_order_the_inventory_was_built_in` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 2 | `test_inventory_declarations` · `TestTheDerivedOrder` · `test_the_classes_are_those_that_declare_a_spec` | R-map | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | `BackgroundModelValue`, `GkSource_tags`, `GkSource_parents` → `GadgetPart`, `Sample_tags`, `Sample_members` (by role: a value, a tag and a member table) |
| 3 | `test_inventory_declarations` · `TestTheDerivedOrder` · `test_a_spec_takes_no_connection` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 4 | `test_inventory_declarations` · `TestTheDerivedOrder` · `test_roots_come_first_unlike_a_plain_sort` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 5 | `test_inventory_declarations` · `TestTheDerivedOrder` · `test_roots_first_on_a_hand_built_registry` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 6 | `test_inventory_declarations` · `TestTheDerivedOrder` · `test_the_earliest_ready_class_in_registry_order` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 7 | `test_inventory_declarations` · `TestTheDerivedOrder` · `test_every_class_follows_every_class_it_references` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 8 | `test_inventory_declarations` · `TestTheDerivedOrder` · `test_a_tagged_class_follows_the_tag_table` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 9 | `test_inventory_declarations` · `TestRefusals` · `test_a_cycle_is_refused_by_name` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 10 | `test_inventory_declarations` · `TestRefusals` · `test_a_self_reference_is_refused` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 11 | `test_inventory_declarations` · `TestRefusals` · `test_a_parent_with_no_spec_is_refused_by_name` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 12 | `test_inventory_declarations` · `TestRefusals` · `test_a_tagged_class_whose_tag_table_declares_no_spec_is_refused` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 13 | `test_inventory_declarations` · `TestRefusals` · `test_a_polymorphic_parents_classes_come_before_it` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 14 | `test_inventory_declarations` · `TestRefusals` · `test_a_type_column_that_is_not_a_leaf_is_refused` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 15 | `test_inventory_declarations` · `TestRefusals` · `test_a_malformed_parent_is_refused` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 16 | `test_inventory_declarations` · `TestRefusals` · `test_a_polymorphic_member_of_a_parent_set_is_refused` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 17 | `test_inventory_declarations` · `TestRefusals` · `test_a_parent_stays_hashable` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 18 | `test_inventory_declarations` · `TestRefusals` · `test_the_reader_refuses_a_registry_before_the_order_is` | R-map | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | `BackgroundModel` (+`_tags`, `Value`) → `Gadget` (+`_tags`, `GadgetPart`) |
| 19 | `test_inventory_declarations` · `TestResolve` · `test_a_hand_built_inventory` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 20 | `test_inventory_declarations` · `TestResolve` · `test_an_absent_nullable_parent_resolves_to_none` | — | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | — |
| 21 | `test_inventory_declarations` · `TestResolve` · `test_the_full_store_resolves_no_absent_parent_as_unresolved` | R-map, R-count | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | `GkWKBIntegration` → `Weave`; field `numeric` → `anchor`; counts 11 → 1 (key), 9 → 1 (member); docstring |
| 22 | `test_inventory_declarations` · `TestResolve` · `test_the_full_store_resolves_both_cosmology_types` | R-imp, R-map | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | `CosmologyModels.model_ids` → `factories.FRAME_KINDS`; `LAMBDACDM_IDENTIFIER`/`QCD_EOS_IDENTIFIER` → `FRAME_KINDS["dial_setting"]`/`["knob_setting"]`; `LambdaCDM`, `QCD_Cosmology` → `dial_setting`, `knob_setting`; `wavenumber_exit_time`, `BackgroundModel` → `Gadget`, `Trace`; `cosmology`/`cosmology_type` → `frame`/`frame_kind` |
| 23 | `test_inventory_declarations` · `TestResolve` · `test_both_referencing_factories_declare_the_one_map` | R-imp, R-map | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | `cosmology_types.COSMOLOGY_TYPES` → `factories.FRAME_TYPES`; `wavenumber_exit_time`, `BackgroundModel` → `Gadget`, `Trace`; `cosmology`/`cosmology_type` → `frame`/`frame_kind` |
| 24 | `test_inventory_declarations` · `TestTheLayerKnowsNoProject` · `test_reading_records_loads_no_project_module` | R-imp, R-help (§2.4) | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | the child's import; the membership test `m == p or m.startswith(p + '.')` over `PROJECT_PACKAGES = ("datastorekit.tests",)` |
| 25 | `test_inventory_declarations` · `TestTheLayerKnowsNoProject` · `test_read_inventory_loads_only_what_the_registry_loads` | R-imp, R-help (§2.4) | R-imp; `ORDER` (R-count); `registry`, `plain_sort`, `_class` unchanged; 04a's `build_full_store` | the child's two imports (`config.datastore` → `datastorekit.tests.client.registry`); the comprehension's membership test as above |
| 26 | `test_declared_facts` · `TestTheRecords` · `test_every_record_of_a_class_with_a_table_carries_the_three_keys` | R-help (U22) | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | `build_schema` given `WITH_A_TABLE`, the registry less `ephemeral_probe` |
| 27 | `test_declared_facts` · `TestTheRecords` · `test_exactly_the_four_declarations_are_not_default` | R-help (U22) | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | as above; `DECLARED` (R-count) has three entries; the name keeps SGK's "four" |
| 28 | `test_declared_facts` · `TestTheRecords` · `test_a_record_with_no_table_is_unchanged` | — | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | — |
| 29 | `test_declared_facts` · `TestBuildSchemaRefusesAMisfit` · `test_the_fitting_declarations_are_accepted` | — | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | — |
| 30 | `test_declared_facts` · `TestBuildSchemaRefusesAMisfit` · `test_an_owner_column_that_is_not_a_column` | — | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | — |
| 31 | `test_declared_facts` · `TestBuildSchemaRefusesAMisfit` · `test_an_owner_column_with_no_foreign_key` | — | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | — |
| 32 | `test_declared_facts` · `TestBuildSchemaRefusesAMisfit` · `test_an_owner_column_with_two_foreign_keys` | — | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | — |
| 33 | `test_declared_facts` · `TestBuildSchemaRefusesAMisfit` · `test_monotone_flags_given_as_a_string` | — | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | — |
| 34 | `test_declared_facts` · `TestBuildSchemaRefusesAMisfit` · `test_monotone_flags_naming_a_column_that_is_absent` | — | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | — |
| 35 | `test_declared_facts` · `TestBuildSchemaRefusesAMisfit` · `test_monotone_flags_naming_a_column_that_is_not_boolean` | — | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | — |
| 36 | `test_declared_facts` · `TestBuildSchemaRefusesAMisfit` · `test_a_validated_column_that_is_not_a_column` | — | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | — |
| 37 | `test_declared_facts` · `TestBuildSchemaRefusesAMisfit` · `test_a_validated_column_that_is_not_boolean` | — | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | — |
| 38 | `test_declared_facts` · `TestTheUnit` · `test_every_compared_table_of_the_registry` | R-map | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | `BackgroundModel` (+`_tags`, `Value`) → `Gadget` (+`_tags`, `GadgetPart`) |
| 39 | `test_declared_facts` · `TestTheUnit` · `test_a_declared_owner_joins_and_an_undeclared_reference_does_not` | — | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | — |
| 40 | `test_declared_facts` · `TestTheFlags` · `test_the_declared_flags_reach_the_specs` | R-map, R-count | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | `redshift`, `wavenumber` (`source`, `response`) → `keypoint` (`kp_marked`, `kp_flagged`), one class; `BackgroundModel`/`validated` → `Gadget`/`gadget_validated`; `BackgroundModelValue`/`model_serial` → `GadgetPart`/`gadget_serial` |
| 41 | `test_declared_facts` · `TestTheFlags` · `test_a_declared_flag_is_set_after_a_get` | — | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | — |
| 42 | `test_declared_facts` · `TestTheFlags` · `test_an_undeclared_flag_is_refused_in_the_declarations_words` | — | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | — |
| 43 | `test_declared_facts` · `TestTheFlags` · `test_the_declared_validated_column_is_recomputed_after_a_validate` | — | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | — |
| 44 | `test_declared_facts` · `TestRevalidate` · `test_the_same_result_flag_and_warning_as_stored_and_with_a_value_row_deleted` | R-map | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | `BackgroundModel` (`label`) → `Gadget` (`gadget_label`) |
| 45 | `test_declared_facts` · `TestRevalidate` · `test_the_base_hook_raises` | — | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | — |
| 46 | `test_declared_facts` · `TestOwnedSerials` · `test_the_base_owns_nothing` | — | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | — |
| 47 | `test_declared_facts` · `TestOwnedSerials` · `test_a_background_model_names_its_value_rows` | R-map | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | `factories["BackgroundModel"]` → `factories["Gadget"]` |
| 48 | `test_declared_facts` · `TestOwnedSerials` · `test_the_pool_checks_each_answer_through_the_hook` | R-map | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | `BackgroundModel` → `Gadget` |
| 49 | `test_declared_facts` · `TestTheVersionObject` · `test_built_by_the_registry_version_factory_with_the_attributes_it_had` | R-value (correction 5) | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | `_label` → `label`, the neutral version object's attribute |
| 50 | `test_declared_facts` · `TestThePruneRefusalNamesItsUnit` · `test_a_prune_that_deletes_outside_its_unit` | R-map, R-count | R-imp; `DECLARED` (R-count); `WITH_A_TABLE` (U22); `bare_pool` keeps `NoShardKeyClass`; `_Owner` sets `parts` (R-help); 03a's `_PruneTestCase` | trigger on `BackgroundModel` → `Gadget`, deleting from `tolerance` → `dial_setting` (hazard 7); the expected unit `['Gadget', 'GadgetPart', 'Gadget_tags']` |
| 51 | `test_layer_registry` · `TestTheClientRegistries` · `test_tables_to_drop_gives_each_table_once_and_names_an_unknown_action` | R-map, R-count | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | `tk-wkb` ×2 → `samples` ×2; `gk-source-policy`, `tk-numeric` → `gadgets`, `tesserae`; their tables |
| 52 | `test_layer_registry` · `TestTheClientRegistries` · `test_every_table_of_every_group_is_declared_by_the_registry` | — | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | — |
| 53 | `test_layer_registry` · `TestTheClientRegistries` · `test_the_groups_are_in_the_command_line_order` | — | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | — |
| 54 | `test_layer_registry` · `TestDropOrder` · `test_a_referencing_table_comes_before_what_it_references` | — | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | — |
| 55 | `test_layer_registry` · `TestDropOrder` · `test_a_cycle_raises` | — | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | — |
| 56 | `test_layer_registry` · `TestTheDropOnAFullStore` · `test_every_group_drops_from_both_shards_and_leaves_no_violation` | — | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | — |
| 57 | `test_layer_registry` · `TestTheDropOnAFullStore` · `test_unsorted_the_same_drop_is_refused_by_enforcement` | — | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | — |
| 58 | `test_layer_registry` · `TestAnUndeclaredDropTable` · `test_read_write_the_pool_refuses_it_before_anything_is_opened` | R-map | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | `GkSource` → `Sample` (through `DROP`) |
| 59 | `test_layer_registry` · `TestAnUndeclaredDropTable` · `test_the_actor_refuses_it_before_dropping_anything` | R-map | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | `GkSource` → `Sample` |
| 60 | `test_layer_registry` · `TestAnUndeclaredDropTable` · `test_read_only_the_refusal_is_read_only_write` | — | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | — |
| 61 | `test_layer_registry` · `TestSerialBatchSizes` · `test_the_manager_uses_the_sizes_it_is_given_and_500_otherwise` | R-map | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | `TkNumericValue`, `redshift` → `GadgetPart`, `keypoint`; the patched path `datastorekit.SQL.ClientPool.ClientPool` (R-imp) |
| 62 | `test_layer_registry` · `TestSerialBatchSizes` · `test_the_pool_gives_every_actor_its_sizes_and_its_registry` | R-map | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | `TkNumericValue`, `redshift` → `GadgetPart`, `keypoint` |
| 63 | `test_layer_registry` · `TestTheRecordedReplicatedSet` · `test_the_reader_yields_the_record_in_serial_order` | — | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | — |
| 64 | `test_layer_registry` · `TestTheRecordedReplicatedSet` · `test_a_store_the_pool_wrote_records_the_configured_set` | — | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | — |
| 65 | `test_layer_registry` · `TestTheRecordedReplicatedSet` · `test_a_primary_without_the_record_is_refused` | — | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | — |
| 66 | `test_layer_registry` · `TestTheRecordedReplicatedSet` · `test_a_record_naming_an_undeclared_class_is_refused` | — | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | — |
| 67 | `test_layer_registry` · `TestTheRecordedReplicatedSet` · `test_the_inventory_compares_exactly_the_recorded_classes` | R-map | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | `tolerance` → `routing_rule` (and the local variable); `redshift` → `keypoint` |
| 68 | `test_layer_registry` · `TestThePoolUsesItsRegistry` · `test_a_registry_without_a_class_builds_shards_without_its_tables` | R-map, R-count | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | left out: `OneLoopIntegral`, `_tags` → `Weave`, `Weave_tags`, `Weave_members` (hazard 8); kept: `QuadSourceIntegral`, `_tags` → `Trace`, `Trace_tags` |
| 69 | `test_layer_registry` · `TestTheLayerImportsNoClient` · `test_a_fresh_interpreter_loads_no_client_registry` | R-imp, R-help (§2.4) | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | `Datastore.SQL.ObjectFactories` prefix → `datastorekit.tests`; the module constants (below) |
| 70 | `test_layer_registry` · `TestTheLayerImportsNoClient` · `test_no_layer_file_imports_a_registry` | R-help (§2.4) | R-imp; `COMMAND_LINE_ORDER` (R-count); `DROP`; `LAYER_MODULES`, `LAYER_FILES`, `FORBIDDEN_*`, `ALLOWED_FACTORY_MODULES` (§2.4); 04a's `build_full_store` | `node.module == "config"` → `"datastorekit.tests.client"`, and its f-strings |
| 71 | `test_drop_refuses_dangling_references` · `TestDependentTables` · `test_each_group_alone_needs_its_measured_dependents` | — | R-imp; `MEASURED`, `REFUSED_GROUP`, `WITH_ITS_DEPENDENTS` (R-count); 04a's `build_full_store` | — |
| 72 | `test_drop_refuses_dangling_references` · `TestDependentTables` · `test_each_group_with_its_dependents_needs_nothing_more` | — | R-imp; `MEASURED`, `REFUSED_GROUP`, `WITH_ITS_DEPENDENTS` (R-count); 04a's `build_full_store` | — |
| 73 | `test_drop_refuses_dangling_references` · `TestDependentTables` · `test_every_group_together_needs_nothing` | — | R-imp; `MEASURED`, `REFUSED_GROUP`, `WITH_ITS_DEPENDENTS` (R-count); 04a's `build_full_store` | — |
| 74 | `test_drop_refuses_dangling_references` · `TestDependentTables` · `test_a_declared_parent_without_a_foreign_key_counts` | R-map | R-imp; `MEASURED`, `REFUSED_GROUP`, `WITH_ITS_DEPENDENTS` (R-count); 04a's `build_full_store` | `QuadSourceIntegral` → `TkWKBIntegration` becomes `Sample` → `Tessera`; group `tk-wkb` → `tesserae` |
| 75 | `test_drop_refuses_dangling_references` · `TestDependentTables` · `test_a_foreign_key_without_a_declared_parent_counts` | R-map | R-imp; `MEASURED`, `REFUSED_GROUP`, `WITH_ITS_DEPENDENTS` (R-count); 04a's `build_full_store` | `GkSource_parents` → `Sample_members`; target `GkNumericIntegration` → `Tessera`; group `gk-numeric` → `tesserae` |
| 76 | `test_drop_refuses_dangling_references` · `TestDependentTables` · `test_dependents_are_followed_transitively` | R-map | R-imp; `MEASURED`, `REFUSED_GROUP`, `WITH_ITS_DEPENDENTS` (R-count); 04a's `build_full_store` | `QuadSourceIntegral_tags` → `Sample_tags`; group `tk-numeric` → `tesserae` (and the local variable) |
| 77 | `test_drop_refuses_dangling_references` · `TestDependentTables` · `test_an_undeclared_name_is_refused` | R-map | R-imp; `MEASURED`, `REFUSED_GROUP`, `WITH_ITS_DEPENDENTS` (R-count); 04a's `build_full_store` | `GkSource` → `Sample` |
| 78 | `test_drop_refuses_dangling_references` · `TestThePoolRefuses` · `test_a_drop_that_leaves_references_is_refused_before_anything_is_opened` | — | R-imp; `MEASURED`, `REFUSED_GROUP`, `WITH_ITS_DEPENDENTS` (R-count); 04a's `build_full_store` | — |
| 79 | `test_drop_refuses_dangling_references` · `TestThePoolRefuses` · `test_nothing_is_created_for_an_absent_store` | — | R-imp; `MEASURED`, `REFUSED_GROUP`, `WITH_ITS_DEPENDENTS` (R-count); 04a's `build_full_store` | — |
| 80 | `test_drop_refuses_dangling_references` · `TestThePoolRefuses` · `test_an_undeclared_name_is_refused_first` | R-map | R-imp; `MEASURED`, `REFUSED_GROUP`, `WITH_ITS_DEPENDENTS` (R-count); 04a's `build_full_store` | `GkSourcePolicy` → `Gadget` (replicated, with dependents; hazard 9) |
| 81 | `test_drop_refuses_dangling_references` · `TestThePoolRefuses` · `test_a_drop_with_its_dependents_is_accepted` | — | R-imp; `MEASURED`, `REFUSED_GROUP`, `WITH_ITS_DEPENDENTS` (R-count); 04a's `build_full_store` | — |
| 82 | `test_layer_is_generic` · `TestTheLayer` · `test_the_derived_files_hold_the_audits_list` | — | R-help (§2.3): `layer_files`, `AUDIT_LIST`, the data file, `KNOWN_HITS`, `import_allowed` | — |
| 83 | `test_layer_is_generic` · `TestTheLayer` · `test_no_test_and_no_client_factory_is_in_it` | R-help (§2.3) | R-help (§2.3): `layer_files`, `AUDIT_LIST`, the data file, `KNOWN_HITS`, `import_allowed` | `Datastore/…` paths → `datastorekit/…`; the factory branch reads `"factor" in Path(rel).name` against `_FACTORY_CONTRACT`, `datastorekit/SQL/factory_base.py` |
| 84 | `test_layer_is_generic` · `TestTheLayer` · `test_the_vocabulary_holds_the_registry_and_the_packages` | R-value (§2.3) | R-help (§2.3): `layer_files`, `AUDIT_LIST`, the data file, `KNOWN_HITS`, `import_allowed` | the package literal `tools` → `Caching` |
| 85 | `test_layer_is_generic` · `TestTheLayerNamesNoProjectWord` · `test_no_code_name` | — | R-help (§2.3): `layer_files`, `AUDIT_LIST`, the data file, `KNOWN_HITS`, `import_allowed` | — |
| 86 | `test_layer_is_generic` · `TestTheLayerNamesNoProjectWord` · `test_no_string_or_docstring` | — | R-help (§2.3): `layer_files`, `AUDIT_LIST`, the data file, `KNOWN_HITS`, `import_allowed` | — |
| 87 | `test_layer_is_generic` · `TestTheLayerNamesNoProjectWord` · `test_no_comment` | — | R-help (§2.3): `layer_files`, `AUDIT_LIST`, the data file, `KNOWN_HITS`, `import_allowed` | — |
| 88 | `test_layer_is_generic` · `TestTheLayerImportsNoProjectPackage` · `test_every_import_is_allowed` | — | R-help (§2.3): `layer_files`, `AUDIT_LIST`, the data file, `KNOWN_HITS`, `import_allowed` | — |
| 89 | `test_layer_is_generic` · `TestTheLayerImportsNoProjectPackage` · `test_the_allow_list` | R-imp (§2.3) | R-help (§2.3): `layer_files`, `AUDIT_LIST`, the data file, `KNOWN_HITS`, `import_allowed` | allowed: `datastorekit.defaults`, `._timing`, `.SQL.factory_base`, `.tools.shard_key_audit`, `sqlalchemy.exc`; refused: `datastorekit.tests.client.registry`, `.factories`, `config.datastore`, `CosmologyModels.model_ids`, `MetadataConcepts` |

### 1.3 The R-count literals, before and after

Each was measured on the tree, from the scratchpad, never translated entry by entry.

| Literal | SGK (before) | Neutral (after) | How measured |
|---|---|---|---|
| `test_inventory_declarations.ORDER` | 21 classes, `version` … `OneLoopIntegral` | 13: `version`, `store_tag`, `keypoint`, `dial_setting`, `knob_setting`, `gauge_setting`, `routing_rule`, `keypoint_alias`, `Gadget`, `Tessera`, `Sample`, `Trace`, `Weave` | `inventory_classes(registry.factories)`; the planner's order, re-measured. A plain sort places `keypoint_alias` fourth, so `assertNotEqual` holds |
| the tables with no spec (`:115-117`) | `BackgroundModelValue`, `GkSource_tags`, `GkSource_parents` | `GadgetPart`, `Sample_tags`, `Sample_members` | by role; each `inventory_spec()` is `None` |
| the walk's counts (`TestResolve`) | `key` 11, `member` 9 | `key` 1, `member` 1 (`records` 1, `no_digest` 0) | SGK's `walk` with `anchor` and `Weave`, on `build_full_store` |
| `test_declared_facts.DECLARED` | 4 entries | 3: `keypoint` `(None, ('kp_marked', 'kp_flagged'), None)`; `Gadget` `(None, (), 'gadget_validated')`; `GadgetPart` `('gadget_serial', (), None)` | `declared(record) != DEFAULT` over `build_schema(WITH_A_TABLE)` |
| `TestTheFlags`' three literals | `redshift`, `wavenumber`; `BackgroundModel`; `BackgroundModelValue` | `{"keypoint": ("kp_marked", "kp_flagged")}`; `{"Gadget": "gadget_validated"}`; `{"GadgetPart": "gadget_serial"}` | the registry's specs |
| `TestTheUnit`'s expected unit | `BackgroundModel`, `_tags`, `Value` | `["Gadget", "Gadget_tags", "GadgetPart"]` | `ShardedPool._unit_tables("Gadget", specs)` |
| the prune refusal's unit (hazard 7) | `['BackgroundModel', 'BackgroundModelValue', 'BackgroundModel_tags']`; `"tolerance" lost rows [(1,)]` | `['Gadget', 'GadgetPart', 'Gadget_tags']`; `"dial_setting" lost rows [(1,)]` | the test's own run (and the orchestrator's three) |
| `test_layer_registry.COMMAND_LINE_ORDER` | SGK's ten `--drop` choices | `["aliases", "tesserae", "samples", "gadgets", "traces"]` | `list(registry.drop_groups)`; the comment says the client has no command line |
| `tables_to_drop`'s two examples | `tk-wkb` ×2 (3 tables); `gk-source-policy`, `tk-numeric` (4) | `samples` ×2 → `Sample`, `Sample_tags`, `Sample_members`; `gadgets`, `tesserae` → `Gadget`, `Gadget_tags`, `GadgetPart`, `Tessera` | `registry.tables_to_drop` |
| `TestAnUndeclaredDropTable.DROP` | `["GkSource", "NotATable"]` | `["Sample", "NotATable"]` | a sharded table of the registry |
| the batch sizes | `TkNumericValue` 7, `redshift` 11 | `GadgetPart` 7, `keypoint` 11 | a value table, and a leaf |
| `TestThePoolUsesItsRegistry`'s left-out tuple | `OneLoopIntegral`, `_tags` (2) | `Weave`, `Weave_tags`, `Weave_members` (3; hazard 8) | the orchestrator's probe, and the test |
| `test_drop_refuses_dangling_references.MEASURED` | SGK's ten groups | `aliases`: 7 tables; `tesserae`: 6; `samples`: none; `gadgets`: `Sample`, `Sample_tags`, `Sample_members`; `traces`: none | `dependent_tables(group, factories)`, as `test_neutral_client.MEASURED_DEPENDENTS` |
| `REFUSED_GROUP`, `WITH_ITS_DEPENDENTS` | `gk-source-policy-records`; with `gk-source-policy`, `quad-source-integral` | `tesserae`; with `samples`, `traces` | `dependent_tables(tables_to_drop(...))` is `[]` |
| `test_layer_is_generic.AUDIT_LIST` | 13 SGK paths | 12 package paths (SGK's less `RayTools/RayWorkPool.py`, by README §4's map) | the README's map |

### 1.4 The guard (§2.3, U17)

**The data file.**
- Command: `./venv/bin/python docs/extraction/measure_client_vocabulary.py`, from the repository
  root. Output:

  ```
  wrote /Users/ds283/Documents/Code/DatastoreKit/datastorekit/tests/data/client_vocabulary.json (19733 bytes)
    SGK: SecondaryGWKit at 6f7f291e857265e429f5d6f810124fd3bf57ce55: 38 registry keys, 190 column names in 21 modules, 14 packages
    CPBH: ChamPBH at 52142d75aebe00855804e2daff4f63aee50ffc3e: 27 registry keys, 80 column names in 17 modules, 11 packages
    SI: StochasticInstantons at 00d254ee41abc6518d13584aa02f656158d8005b: 30 registry keys, 101 column names in 22 modules, 15 packages
    SGK extra names: 5
    all clients: 82 registry keys, 325 column names, 20 packages
  ```
- **Commits:** SGK `6f7f291` (`config/datastore.py`, `factories`), CPBH `52142d7`
  (`Datastore/SQL/Datastore.py`, `_factories`), SI `00d254e` (`Datastore/SQL/Datastore.py`,
  `_factories`). Each is stored in full in the file.
- **Size and SHA-256:** 19,733 bytes,
  `98af1124cf62e143b46141be49d61ceeea9d401a76af1af601d88176017f332e`.
- **The second run:** `--output <scratchpad>/measure-run2.json`, from the same tree: the same
  output, 19,733 bytes, the same SHA-256; `cmp` finds the two identical. A third run with no
  `--output` refuses to overwrite the committed file (exit 1).
- **What the script reads.** Only `git -C <client> rev-parse`, `show` and `ls-tree`, at the three
  commits. `grep` of the script for `import`, `sys.path`, `open(`, `subprocess.` and file access:
  it imports `argparse`, `ast`, `json`, `subprocess`, `sys`, `pathlib` and `typing`; its one
  `subprocess.run` (`:80`) runs `git -C <client> …`; its one write is the output file. It imports
  no client and opens no client file.
- **SGK's `EXTRA_NAMES`** are taken from SGK's own guard at `6f7f291`
  (`Datastore/tests/test_layer_is_generic.py`, the set literal `EXTRA_NAMES`), by `ast`, and held
  under SGK: `COSMOLOGY`, `cosmology`, `cosmology_serial`, `cosmology_type`, `model_ids`.
- **The file holds what was read, before any rule**, and its `summary` counts that: 82 registry
  keys, 325 column names, 20 packages (deviation 7).

**The vocabulary, by the guard's own functions** (`registry_words`, `project_packages`,
`forbidden_words`), measured from the scratchpad:

| | Before the guard's exclusions | After |
|---|---|---|
| tables | **82** (the union of the three registries' keys) | 80 (less `version`, `store_tag`: `LAYER_WORDS`) |
| identifier columns | **301** (an underscore, or a capital and more than one character) | 300 (less `tag_serial`) |
| packages | 20 | **16** (less `Datastore`, `RayTools`, `config`, `tools`: `_NOT_PROJECT_PACKAGES`) |
| forbidden words | — | **398** (tables, columns, packages and the five extra names) |

The bold figures are §2.3's, as correction 4 reads them. The one-letter columns are `C`, `G`, `N`,
`T` (excluded by length) and `b`, `h`, `z` (plain words).

**The layer** (`layer_files()`): 20 files, every `.py` under `datastorekit/` but `tests/`,
`datastorekit/SQL/factory_base.py` among them. `AUDIT_LIST`'s twelve are all in it.

**The scans**, run with the guard's functions over the 20 files:
- code names: none; strings: none; imports: none;
- comments: `datastorekit/tools/shard_key_audit.py:188 wavenumber`, the one U17 names.
- Without `tools` in `_NOT_PROJECT_PACKAGES`: four string hits, `datastorekit/tools/shard_key_audit.py:44`,
  `datastorekit/tools/sharded_store.py:5`, `:6` and `:39`, each `tools` (correction 3).

**`KNOWN_HITS`:**

```python
KNOWN_HITS = {
    "test_no_code_name": [],
    "test_no_string_or_docstring": [],
    "test_no_comment": [
        # 'e.g. "wavenumber"', a name of SecondaryGWKit's shard-key table, in a comment imported
        # unchanged; README §5 rule 8 freezes it until after prompt 05, and
        # [01-package-prose-names-sgks-layout] rewrites it (README §6.2, U17)
        "datastorekit/tools/shard_key_audit.py:188 wavenumber",
    ],
    "test_every_import_is_allowed": [],
}
```

`assertNoHits(found)` is one assertion,
`self.assertEqual(KNOWN_HITS.get(self._testMethodName, []), found, …)`: a new hit fails ((i)), and
so does a pinned hit no longer found ((j)). The port check finds the guard's skeletons equal to
SGK's (8 tests, 9 functions, 17 assertions).

**The changes to SGK's guard**, each R-help unless it says otherwise:
- `REPO_ROOT` is the repository root; `layer_files()` walks `datastorekit/` less `tests/`, with no
  `ObjectFactories/` exclusion and no `RayTools/` glob;
- `AUDIT_LIST`: twelve paths (R-count);
- `LAYER_WORDS`: SGK's, through `datastorekit.contract`;
- `_NOT_PROJECT_PACKAGES`: SGK's three and `tools`, with the comment;
- `FRAGMENTS`, `FLAG_PHRASES`, the scanners, `_absolute`, `scan_imports` and the three scanning
  tests: SGK's;
- `registry_words()`, `project_packages()` and the new `extra_names()` and `_clients()` read
  `VOCABULARY`; `registry_words` keeps its docstring's rule and adds the one-character one;
- `import_allowed`: the standard library, `ray`, `sqlalchemy`, and `datastorekit` less
  `datastorekit.tests`; `_ALLOWED_MODULES` is empty, and the comment says why; SGK's `RayTools`
  branch is gone (deviation 9);
- `test_no_test_and_no_client_factory_is_in_it`: two branches, the factory one on
  `factory_base.py`;
- `test_the_allow_list`: §2.3's five and five (R-imp);
- `test_the_vocabulary_holds_the_registry_and_the_packages`: `tools` → `Caching` (R-value);
- the imports of `config.datastore`, `build_schema` and `sqlalchemy` are gone (R-imp), and `json`
  is added;
- the module docstring describes the package's guard (deviation 10).

### 1.5 `NOT_PORTED` (§2.5, U16)

`compare_ported_tests.py` gains `NOT_PORTED`, a list of (package path, source `Class.method`
after `NAME_MAP`, reason), with one entry: `test_inventory_declarations.py`,
`TestResolve.test_the_report_renders_both_cosmology_types`, "asserts on SGK's
tools.inventory_report, which stays in SGK (README §1)". For a module with declared tests:

1. **the names**: the source's tests less the declared ones equal the package's;
2. **the skeletons**: a declared function, and any function nested in it, is not compared and not
   counted;
3. a declared test that the package does define is a difference ((c));
4. a declared test that the source does not define is a difference ((p));
5. **kept at the user's direction (correction 7):** a declaration naming a module that `PORTED`
   does not hold is a difference, since that module's source is never read ((q)).

The report prints each declared test with its reason (`NOT PORTED  …`), and the module's `tests`
line gives the source's count and the number not ported. The final line counts the declared tests.
The docstring states the rules.

## 2. Deviations from the prompt

1. **Correction 1**: breakage (k) is appended as `store_inventory.py`'s last line. Among the
   imports it is a circular import. **STRUCTURALLY REQUIRED.**
2. **Correction 2**: (m) also fails `test_no_comment`, measured (§6.2). **STRUCTURALLY REQUIRED.**
3. **Correction 3**: §2.3's "six string hits" are four, on four lines, measured (§1.4).
   **STRUCTURALLY REQUIRED.**
4. **Correction 4**: the vocabulary summary's counts are given with which is which (§1.4).
   **STRUCTURALLY REQUIRED.**
5. **Correction 5**: `TestTheVersionObject`'s literal is `{"_my_id": 1, "label": "standin",
   "_deserialized": True}`, R-value. **STRUCTURALLY REQUIRED.**
6. **The stop, and U22 (correction 6).**
   - **The stop.** With the five modules ported, the suite gave `Ran 444 tests` /
     `FAILED (failures=1, errors=1)`, both in `test_declared_facts.TestTheRecords`:
     - `test_every_record_of_a_class_with_a_table_carries_the_three_keys`: `22 != 21`;
     - `test_exactly_the_four_declarations_are_not_default`: `KeyError: 'owner_column'`.

     Both call `build_schema(sqla.MetaData(), factories)` on the whole registry. The client's
     `ephemeral_probe` registers `None`, so its record has no table and none of the three keys. No
     SGK class registers `None`. Narrowing the registry is none of the six kinds, so the agent
     stopped, uncommitted (prompt §5, first condition).
   - **Probe 1, a module-wide filter** (a scratch runner that replaced the module's `factories`
     with the registry less `register() is None`): 24 pass, and `TestTheVersionObject` errors.
     Its read-only open is refused, since the store's `replicated_tables` still names
     `ephemeral_probe`.
   - **Probe 2**, a scratch copy outside `datastorekit/` giving only those two `build_schema`
     calls the narrowed registry: `Ran 25 tests … OK`.
   - **The resolution.** The user took U22. The module constant `WITH_A_TABLE = {n: f for n, f in
     factories.items() if f.register() is not None}` is what those two calls are given (R-help, as
     U20's filter). No assertion, name or control flow changes, and the port check's counts for
     the module stay 25 tests, 26 functions and 64 assertions. Every other test keeps the whole
     registry.

   **STRUCTURALLY REQUIRED.**
7. **The data file holds what was read; the guard's counts are in this log.** The `summary` in
   the file counts registry keys, column names and packages before any rule (82, 325, 20). The
   identifier-column rule, `LAYER_WORDS` and `_NOT_PROJECT_PACKAGES` are the guard's alone, so
   the figures §3.6 names (82 tables, 301 identifier columns, 16 packages, 398 words) are measured
   by the guard's functions (§1.4), not written into the data. **IMPLEMENTATION CHOICE.**
8. **SGK's `EXTRA_NAMES` are read from SGK's guard** at the import commit, by the script, rather
   than copied by hand; the guard reads them through `extra_names()`, a new function with no
   assertion. **IMPLEMENTATION CHOICE.**
9. **`import_allowed` loses SGK's `RayTools` branch.** `RayWorkPool` is not in the package (D2), and
   §2.3 allows only the standard library, `ray`, `sqlalchemy` and `datastorekit` less its tests.
   The function's control flow is SGK's less that `if`. **STRUCTURALLY REQUIRED.**
10. **Prose that became false is rewritten** (as 04a's deviation 21):
    - the guard's module docstring and its comments on `_FACTORY_CONTRACT`, `AUDIT_LIST`,
      `_NOT_PROJECT_PACKAGES`, `FRAGMENTS`, `FLAG_PHRASES` and `_ALLOWED_MODULES`;
    - the comments of `ORDER`, `COMMAND_LINE_ORDER`, `MEASURED`, `REFUSED_GROUP`, and the block above
      `FORBIDDEN_MODULES`;
    - `datastore_module`'s comment (its module path, R-imp);
    - `test_declared_facts`' docstring items 1, 3 and 6 ("three declarations"; `Gadget`), and
      `test_layer_registry`'s item 7 (`Weave`), which named SGK's classes.

    Every other docstring and comment is SGK's. **IMPLEMENTATION CHOICE.**
11. **§2.4's membership test is an expression, not control flow.** In
    `test_read_inventory_loads_only_what_the_registry_loads`'s comprehension it adds a generator
    inside `any(...)`; in `test_reading_records_loads_no_project_module` it is inside the child's
    code string. The agent's control-flow comparison sees the one `GeneratorExp`. As §2.4 directs.
    **STRUCTURALLY REQUIRED.**
12. **`FORBIDDEN_PACKAGES` is `tuple(sorted(project_packages()))`**, imported from the guard, so
    that it is the data file's packages less `_NOT_PROJECT_PACKAGES`, with the rule held once.
    **IMPLEMENTATION CHOICE.**
13. **The factory branch of `test_no_test_and_no_client_factory_is_in_it`** reads
    `"factor" in Path(rel).name`: a module of the layer named for factories must be the contract.
    SGK's `rel.startswith("Datastore/SQL/ObjectFactories/")` has no counterpart path. An expression,
    not control flow. **IMPLEMENTATION CHOICE.**
14. **Two local variables are renamed** with their table (§1.1). **IMPLEMENTATION CHOICE.**
15. **(q) is added to the breakage record**, for the fifth `NOT_PORTED` rule. **IMPLEMENTATION
    CHOICE.**
16. **(n), (o) and (p)**, and the second run of the measuring script, at the orchestrator's
    direction. **IMPLEMENTATION CHOICE.**

No UNINTENDED DRIFT was found.

## 3. The ten hazards (§2.2)

1. **The two classes would test nothing as written. They now bite.** (k) fails
   `test_reading_records_loads_no_project_module`, `test_a_fresh_interpreter_loads_no_client_registry`
   and `test_no_layer_file_imports_a_registry`. Under (n) (SGK's `PROJECT_PACKAGES`), the first
   passes, so the retarget is what makes it bite. `test_read_inventory_loads_only_what_the_registry_loads`
   imports the registry before its snapshot, so (k) cannot fail it, in SGK or here (correction 1).
2. **`assertNoHits` is exact in both directions with one assertion** (§1.4; (i) and (j)).
3. **The guard needs no client.** It imports `datastorekit.contract` and the standard library,
   and reads only its data file ((o): pointed at a copy, it follows the copy).
4. **`DECLARED` has three entries**, and `test_exactly_the_four_declarations_are_not_default`
   keeps SGK's name (rule 6). `TestTheFlags`' first literal names `keypoint` alone.
5. **`TestRevalidate` reads `Gadget`.** `gadget_label`, `gadget_validated`, `GadgetPart` on
   `gadget_serial`. Every Gadget of shard 0 validates with nothing deleted, and not with one part
   deleted, with the warning U15 added. `_Model` is a `DatastoreObject`, which gives `available`
   and `store_id`. It passes.
6. **`TestOwnedSerials` reads `.parts`.** `_Owner` sets `parts` (R-help); `[3, None, 5]`, `[]` and
   `None` hold.
7. **`TestThePruneRefusalNamesItsUnit`.** The trigger deletes from `dial_setting`. The message is
   `"dial_setting" lost rows [(1,)], and a prune of "Gadget" deletes only from ['Gadget', 'GadgetPart', 'Gadget_tags']`,
   as the planner expected.
8. **Three tables left out.** `Weave`, `Weave_tags`, `Weave_members`; the shards hold `Trace` and
   `Trace_tags` and no `Weave` table.
9. **`REFUSED_GROUP` is sharded**: `tesserae`, six dependents; `Gadget` in the
   undeclared-name test.
10. **`build_store` does not stand for the fixture.** Every test SGK built with
    `real_store_fixtures` uses 04a's `build_full_store`.

## 4. The issue (§2.6)

`datastorekit/tests/test_parent_set_members.py` holds two tests on 04a's `build_full_store`:
- `test_the_set_declares_both_members_in_order`: `list(inventory["Weave"].parent_sets["strands"].items())`
  is `[("anchor", "Tessera"), ("origin", "Trace")]`;
- `test_varying_the_second_member_changes_only_the_weave`: `vary_row` sets `Weave_members` row
  702's `origin_serial` from 3 to 1. Exactly `{"Weave"}`'s records change, and the inventory has
  no problem.

Breakage (l), `"origin"` deleted from `Weave_factory.inventory_spec`, fails both (§6.2). So
`[04a-no-test-pins-a-second-parent-set-member]` is closed, and moves to the board's §4.

## 5. Verification performed

### 5.1 The suite (§3.1)

`./venv/bin/python -m unittest discover -s datastorekit/tests -t .`, in the foreground, with the
output written to the scratchpad.

**Before: `Ran 353 tests … OK`. After: `Ran 444 tests` / `OK`**, which is 353 + 89 + 2.

| Point in the work | Result |
|---|---|
| step 1 (the script, the data file, the guard) | 361 OK |
| step 2 (`NOT_PORTED`, `test_inventory_declarations`) | 386 OK |
| steps 3 and 4, before U22 | 444, 1 failure and 1 error (the stop) |
| after U22 | 444 OK |

- **Names.** All 353 test ids of before are present after (`comm` over the loader's ids: none
  missing). The 91 new ids are 25, 25, 20, 11, 8 and 2 by module.
- **Toolchain.** Python 3.12.15, `ray==2.43.0`, `SQLAlchemy==2.0.39`, `black==25.1.0`.
- **Isolation.** No Ray process was up (`pgrep -lf 'gcs_server|raylet|ray::'` empty), and every
  store was in a `tempfile` directory.

**Control flow, measured.** The agent's `ast` comparison (compound statements, `With` item
counts, returns, raises, break, continue, conditional expressions, comprehensions, lambdas and
nested `def`s) covers SGK's 154 functions in the five modules:
- equal for every function of `test_declared_facts`, `test_layer_registry` and
  `test_drop_refuses_dangling_references`;
- `test_inventory_declarations`: equal but for `test_read_inventory_loads_only_what_the_registry_loads`
  (one `GeneratorExp`, §2.4; deviation 11), and U16's test, absent;
- `test_layer_is_generic`: equal but for `layer_files` (no factory exclusion, no `RayTools` loop),
  `registry_words` (two set comprehensions over the data) and `import_allowed` (deviation 9); the
  package adds `_clients` and `extra_names`.

### 5.2 The loader's run counts (§3.4)

| Module | Run count |
|---|---|
| `test_inventory_declarations` | **25** |
| `test_declared_facts` | **25** |
| `test_layer_registry` | **20** |
| `test_drop_refuses_dangling_references` | **11** |
| `test_layer_is_generic` | **8** |
| `test_parent_set_members` | **2** |

### 5.3 The port check (§3.2)

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
datastorekit/tests/test_inventory_declarations.py (from Datastore/tests/test_inventory_declarations.py): ok
  tests: 25 (source 26, 1 not ported)
  classes: 4 (source 4)
  functions compared: 26
  assertions: 57
  NOT PORTED  TestResolve.test_the_report_renders_both_cosmology_types: asserts on SGK's tools.inventory_report, which stays in SGK (README §1)
datastorekit/tests/test_declared_facts.py (from Datastore/tests/test_declared_facts.py): ok
  tests: 25 (source 25)
  classes: 11 (source 11)
  functions compared: 26
  assertions: 64
datastorekit/tests/test_layer_registry.py (from Datastore/tests/test_layer_registry.py): ok
  tests: 20 (source 20)
  classes: 9 (source 9)
  functions compared: 22
  assertions: 93
datastorekit/tests/test_drop_refuses_dangling_references.py (from Datastore/tests/test_drop_refuses_dangling_references.py): ok
  tests: 11 (source 11)
  classes: 2 (source 2)
  functions compared: 13
  assertions: 48
datastorekit/tests/test_layer_is_generic.py (from Datastore/tests/test_layer_is_generic.py): ok
  tests: 8 (source 8)
  classes: 4 (source 4)
  functions compared: 9
  assertions: 17

OK: 20 module(s) keep their source's tests, classes and assertion skeletons; 1 test(s) declared not ported
```

The fifteen earlier modules' counts are unchanged.

### 5.4 The equivalence check (§3.3)

`./venv/bin/python docs/extraction/compare_with_source.py`, exit **0**: 31 compared, 20 `PORTED`, 10
with no source, 61 tracked `.py` files. Its whole output:

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
files ported, checked by compare_ported_tests.py: 20
files with no source, declared: 10
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
ported: checked by compare_ported_tests.py: datastorekit/tests/test_inventory_declarations.py (from Datastore/tests/test_inventory_declarations.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_declared_facts.py (from Datastore/tests/test_declared_facts.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_layer_registry.py (from Datastore/tests/test_layer_registry.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_drop_refuses_dangling_references.py (from Datastore/tests/test_drop_refuses_dangling_references.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_layer_is_generic.py (from Datastore/tests/test_layer_is_generic.py)
not compared (no source, declared): datastorekit/tests/client/__init__.py
not compared (no source, declared): datastorekit/tests/client/build.py
not compared (no source, declared): datastorekit/tests/client/factories.py
not compared (no source, declared): datastorekit/tests/client/objects.py
not compared (no source, declared): datastorekit/tests/client/reader.py
not compared (no source, declared): datastorekit/tests/client/registry.py
not compared (no source, declared): datastorekit/tests/test_neutral_client.py
not compared (no source, declared): datastorekit/tests/test_package_imports.py
not compared (no source, declared): datastorekit/tests/test_parent_set_members.py
not compared (no source, declared): datastorekit/tests/test_shard_key_assignment.py

Lines listed: D-fmt always, UNCLASSIFIED always, the rest with --show.
datastorekit/tests/test_sharded_store_script.py (from Datastore/tests/test_sharded_store_script.py):
  D-fmt         source line removed or changed  Datastore/tests/test_sharded_store_script.py:27: 
datastorekit/tests/standin_pool.py (from Datastore/tests/standin_pool.py):
  D-fmt         source line removed or changed  Datastore/tests/standin_pool.py:419: 
  D-fmt         source line removed or changed  Datastore/tests/standin_pool.py:420: 

OK: every differing line is classified, and every file is accounted for
```

### 5.5 The vocabulary (§3.5)

- **The 80 names** (log 02 §1.2's 82, less `version` and `store_tag`; equal to the data file's
  union of registry keys less those two), matched as whole words with `grep -cwE`:

  | File | Lines matched |
  |---|---|
  | `test_inventory_declarations` | 0 |
  | `test_declared_facts` | 0 |
  | `test_layer_registry` | 0 |
  | `test_drop_refuses_dangling_references` | 0 |
  | `test_parent_set_members` | 0 |
  | `test_layer_is_generic` (the guard) | 3 (`:197`, `:200`, the pinned hit's comment and string; `:344`, SGK's literal) |
  | `data/client_vocabulary.json` | 134 |

  SGK's five match 33, 22, 31, 54 and 2 lines, §3.5's figures.
- **The second grep of 04a §4.5** (`CosmologyModels`, `CosmologyConcepts`, `ComputeTargets`,
  `extract_common`, `config\.`, `Planck2018`, `k_inv_Mpc`, `log10_tol`, `cosmology_type`,
  `cosmology_serial`, `model_serial`, `Run_fixture`):
  - the four modules and `test_parent_set_members`: two lines, both in `test_layer_registry`, both
    SGK's prose ported unchanged (`:9`, docstring item 1, and `:138`, the banner
    `# 1. config.datastore`);
  - the guard: five lines, its docstring's examples (`:160`) and §2.3's literals (`:345`, `:347`,
    `:393`, `:394`);
  - SGK's five match 13, 5, 10, 1 and 14 lines.

### 5.6 `black` (§3.8)

`./venv/bin/black --check datastorekit docs/extraction` (25.1.0) gives `64 files would be left
unchanged.`

## 6. The deliberate-breakage record (§3.7)

### 6.1 The method

The work was staged by explicit path. Each diff was made by editing the file(s), taking `git diff`
against the index, and restoring the file(s) from the index (`mkbreak.py` in the scratchpad).
Each was then run through `runbreak.sh` in `bash`:
1. `git apply --check`;
2. `git apply`;
3. `git apply -R --check`;
4. the check, or the whole suite;
5. `git apply -R`.

After each, `git diff` against the index was empty and nothing was untracked. The diffs below are
the files that were applied, byte for byte, trailing context lines included, and were checked again
both ways from this log after it was written. None is committed. The checks' breakages ran their
check; (e)–(n) ran the whole suite on the final tree.

**Whether SGK's counterpart pins the same line** is by reading SGK's test, which makes the same
assertion on the same layer line. SGK is never run.

### 6.2 The checks

**(a)** One `assertFalse` deleted from `TestTheFlags.test_a_declared_flag_is_set_after_a_get` (`test_declared_facts`). `compare_ported_tests.py` exits **1**, naming the test:

```diff
diff --git a/datastorekit/tests/test_declared_facts.py b/datastorekit/tests/test_declared_facts.py
index fcae920..73c5c5e 100644
--- a/datastorekit/tests/test_declared_facts.py
+++ b/datastorekit/tests/test_declared_facts.py
@@ -410,7 +410,6 @@ class TestTheFlags(unittest.TestCase):
         )
         self.assertEqual([], refusals)
         self.assertEqual({("Flagged", 1): {(1,): ["on", "lit"]}}, plan["flags"])
-        self.assertFalse(plan["recompute"])
 
     def test_an_undeclared_flag_is_refused_in_the_declarations_words(self):
         plan, refusals = self.plan(
```
```
  NOT PORTED  TestResolve.test_the_report_renders_both_cosmology_types: asserts on SGK's tools.inventory_report, which stays in SGK (README §1)
  DIFFERS  TestTheFlags.test_a_declared_flag_is_set_after_a_get: skeleton differs at position 3: the source has assertFalse, the package (nothing) (3 in the source, 2 in the package)
FAIL: 1 of 20 module(s) differ from their source
exit 1
```

**(b)** The `NOT_PORTED` entry removed. It exits **1**, naming the test as missing from the package:

```diff
diff --git a/docs/extraction/compare_ported_tests.py b/docs/extraction/compare_ported_tests.py
index b45511d..f57ef58 100644
--- a/docs/extraction/compare_ported_tests.py
+++ b/docs/extraction/compare_ported_tests.py
@@ -165,13 +165,7 @@ NAME_MAP: Dict[str, Dict[str, str]] = {
 
 
 # U16: the tests of a ported module that are not ported: (package path, source Class.method, reason)
-NOT_PORTED: List[Tuple[str, str, str]] = [
-    (
-        "datastorekit/tests/test_inventory_declarations.py",
-        "TestResolve.test_the_report_renders_both_cosmology_types",
-        "asserts on SGK's tools.inventory_report, which stays in SGK (README §1)",
-    ),
-]
+NOT_PORTED: List[Tuple[str, str, str]] = []
 
 
 class CannotRun(Exception):
```
```
  DIFFERS  test missing from the package: TestResolve.test_the_report_renders_both_cosmology_types
  DIFFERS  TestResolve.test_the_report_renders_both_cosmology_types: asserts in the source (5), missing from the package
FAIL: 1 of 20 module(s) differ from their source
exit 1
```

**(c)** U16's test added back to `test_inventory_declarations` as a stub that asserts. It exits **1**:

```diff
diff --git a/datastorekit/tests/test_inventory_declarations.py b/datastorekit/tests/test_inventory_declarations.py
index 7b3ba4c..0005861 100644
--- a/datastorekit/tests/test_inventory_declarations.py
+++ b/datastorekit/tests/test_inventory_declarations.py
@@ -434,6 +434,9 @@ class TestResolve(unittest.TestCase):
                 ("frame_kind", expected),
             )
 
+    def test_the_report_renders_both_cosmology_types(self):
+        self.assertTrue(True)
+
     def test_both_referencing_factories_declare_the_one_map(self):
         from datastorekit.tests.client.factories import FRAME_TYPES
 
```
```
  NOT PORTED  TestResolve.test_the_report_renders_both_cosmology_types: asserts on SGK's tools.inventory_report, which stays in SGK (README §1)
  DIFFERS  declared not ported, and the package defines it: TestResolve.test_the_report_renders_both_cosmology_types
FAIL: 1 of 20 module(s) differ from their source
exit 1
```

**(p)** `NOT_PORTED`'s method renamed to one SGK's module does not define (§2.5's fourth rule). It exits **1**:

```diff
diff --git a/docs/extraction/compare_ported_tests.py b/docs/extraction/compare_ported_tests.py
index b45511d..3e27732 100644
--- a/docs/extraction/compare_ported_tests.py
+++ b/docs/extraction/compare_ported_tests.py
@@ -168,7 +168,7 @@ NAME_MAP: Dict[str, Dict[str, str]] = {
 NOT_PORTED: List[Tuple[str, str, str]] = [
     (
         "datastorekit/tests/test_inventory_declarations.py",
-        "TestResolve.test_the_report_renders_both_cosmology_types",
+        "TestResolve.test_the_report_renders_no_cosmology_type",
         "asserts on SGK's tools.inventory_report, which stays in SGK (README §1)",
     ),
 ]
```
```
  NOT PORTED  TestResolve.test_the_report_renders_no_cosmology_type: asserts on SGK's tools.inventory_report, which stays in SGK (README §1)
  DIFFERS  declared not ported, and the source does not define it: TestResolve.test_the_report_renders_no_cosmology_type
  DIFFERS  test missing from the package: TestResolve.test_the_report_renders_both_cosmology_types
  DIFFERS  TestResolve.test_the_report_renders_both_cosmology_types: asserts in the source (5), missing from the package
FAIL: 1 of 20 module(s) differ from their source
exit 1
```

**(q)** A second `NOT_PORTED` entry naming a module `PORTED` does not hold (the fifth rule, kept at the user's direction). It exits **1**:

```diff
diff --git a/docs/extraction/compare_ported_tests.py b/docs/extraction/compare_ported_tests.py
index b45511d..72f2a8d 100644
--- a/docs/extraction/compare_ported_tests.py
+++ b/docs/extraction/compare_ported_tests.py
@@ -171,6 +171,11 @@ NOT_PORTED: List[Tuple[str, str, str]] = [
         "TestResolve.test_the_report_renders_both_cosmology_types",
         "asserts on SGK's tools.inventory_report, which stays in SGK (README §1)",
     ),
+    (
+        "datastorekit/tests/test_neutral_client.py",
+        "TestNeutralClient.test_nothing",
+        "a module that PORTED does not hold",
+    ),
 ]
 
 
```
```
  NOT PORTED  TestResolve.test_the_report_renders_both_cosmology_types: asserts on SGK's tools.inventory_report, which stays in SGK (README §1)
  DIFFERS  NOT_PORTED names a module that PORTED does not hold: datastorekit/tests/test_neutral_client.py
FAIL: 0 of 20 module(s) differ from their source; 1 declaration(s) name no ported module
exit 1
```

**(d)** The guard module removed from `FILES`. `compare_with_source.py` exits **1**:

```diff
diff --git a/docs/extraction/compare_with_source.py b/docs/extraction/compare_with_source.py
index 6129985..c1c8962 100644
--- a/docs/extraction/compare_with_source.py
+++ b/docs/extraction/compare_with_source.py
@@ -186,7 +186,6 @@ FILES: List[Tuple[str, str, str]] = (
             "test_declared_facts",
             "test_layer_registry",
             "test_drop_refuses_dangling_references",
-            "test_layer_is_generic",
         )
     ]
 )
```
```
files ported, checked by compare_ported_tests.py: 19
not compared (NOT ACCOUNTED FOR): datastorekit/tests/test_layer_is_generic.py
FAIL: 1 file(s) under datastorekit/ not accounted for
exit 1
```


### 6.3 The layer, the guard and the issue, through the tests

**(e)** No roots-first step in `inventory_classes` (`store_inventory.py:964`; `order` starts empty):

```diff
diff --git a/datastorekit/store_inventory.py b/datastorekit/store_inventory.py
index 10b46da..8e6bd25 100644
--- a/datastorekit/store_inventory.py
+++ b/datastorekit/store_inventory.py
@@ -961,7 +961,7 @@ def inventory_classes(factories: Mapping[str, Any]) -> List[str]:
         if name in spec.dependencies():
             raise ValueError(f"inventory_classes(): {name} references itself")
 
-    order: List[str] = [name for name in specs if len(depends[name]) == 0]
+    order: List[str] = []
     placed = set(order)
     while len(order) < len(specs):
         ready = [
```
`Ran 444 tests in 83.963s` / `FAILED (failures=4)`. The tests that fail:

- `FAIL test_inventory_declarations.TestTheDerivedOrder.test_it_is_the_order_the_inventory_was_built_in`
- `FAIL test_inventory_declarations.TestTheDerivedOrder.test_roots_come_first_unlike_a_plain_sort`
- `FAIL test_inventory_declarations.TestTheDerivedOrder.test_roots_first_on_a_hand_built_registry`
- `FAIL test_store_inventory.TestTheFullStore.test_every_class_has_a_record`

**(f)** `dependent_tables` follows one level only (a `break` after `gone |= more`, `SQL/schema.py:380`):

```diff
diff --git a/datastorekit/SQL/schema.py b/datastorekit/SQL/schema.py
index 25e44ba..75b726c 100644
--- a/datastorekit/SQL/schema.py
+++ b/datastorekit/SQL/schema.py
@@ -378,6 +378,7 @@ def dependent_tables(dropped: Iterable[str], factories: Mapping[str, Any]) -> Li
             break
         found |= more
         gone |= more
+        break
 
     return [name for name in tables if name in found]
 
```
`Ran 444 tests in 97.696s` / `FAILED (failures=9)`. The tests that fail:

- `FAIL test_drop_refuses_dangling_references.TestDependentTables.test_dependents_are_followed_transitively`
- `FAIL test_drop_refuses_dangling_references.TestDependentTables.test_each_group_alone_needs_its_measured_dependents (group='aliases')`
- `FAIL test_drop_refuses_dangling_references.TestDependentTables.test_each_group_alone_needs_its_measured_dependents (group='gadgets')`
- `FAIL test_drop_refuses_dangling_references.TestDependentTables.test_each_group_alone_needs_its_measured_dependents (group='tesserae')`
- `FAIL test_drop_refuses_dangling_references.TestThePoolRefuses.test_a_drop_that_leaves_references_is_refused_before_anything_is_opened`
- `FAIL test_drop_refuses_dangling_references.TestThePoolRefuses.test_nothing_is_created_for_an_absent_store`
- `FAIL test_neutral_client.TestTheRegistry.test_dependent_tables_accepts_each_group_as_declared (group='aliases')`
- `FAIL test_neutral_client.TestTheRegistry.test_dependent_tables_accepts_each_group_as_declared (group='gadgets')`
- `FAIL test_neutral_client.TestTheRegistry.test_dependent_tables_accepts_each_group_as_declared (group='tesserae')`

**(g)** An `owner_column` with no foreign key accepted (`SQL/schema.py:211`, `n != 1` → `n > 1`):

```diff
diff --git a/datastorekit/SQL/schema.py b/datastorekit/SQL/schema.py
index 25e44ba..9961cf6 100644
--- a/datastorekit/SQL/schema.py
+++ b/datastorekit/SQL/schema.py
@@ -208,7 +208,7 @@ def _declared_owner_column(
             cls_name, "owner_column", owner, tab, "which is not a column of its table"
         )
     n = len(tab.c[owner].foreign_keys)
-    if n != 1:
+    if n > 1:
         raise _refuse_declaration(
             cls_name,
             "owner_column",
```
`Ran 444 tests in 92.391s` / `FAILED (failures=1)`. The tests that fail:

- `FAIL test_declared_facts.TestBuildSchemaRefusesAMisfit.test_an_owner_column_with_no_foreign_key`

**(h)** `_unit_tables` ignores a declared owner (`SQL/ShardedPool.py:2144`, `and False`):

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 8d1fd81..7aa447e 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -2141,7 +2141,7 @@ class ShardedPool:
             ):
                 unit.append(spec["name"])
         for spec in specs:
-            if spec["name"] != cls_name and ShardedPool._declares_owner(spec, cls_name):
+            if spec["name"] != cls_name and ShardedPool._declares_owner(spec, cls_name) and False:
                 unit.append(spec["name"])
         return unit
 
```
`Ran 444 tests in 86.651s` / `FAILED (failures=7, errors=26)`. The tests that fail:

- `ERROR test_one_timestamp_per_write.TestCompletionOfAnInterruptedPrune.test_faulted_after_each_shard (after=0)`
- `ERROR test_one_timestamp_per_write.TestCompletionOfAnInterruptedPrune.test_faulted_after_each_shard (after=1)`
- `ERROR test_one_timestamp_per_write.TestCompletionOfAnInterruptedPrune.test_faulted_after_each_shard (after=2)`
- `ERROR test_one_timestamp_per_write.TestCompletionOfAnInterruptedPrune.test_faulted_before_the_first_shard`
- `ERROR test_one_timestamp_per_write.TestPruneAtOpen.test_every_shard_identical_and_no_record_left`
- `ERROR test_one_timestamp_per_write.TestRepairAtOpen.test_store_of_a_background_model (point='C-P2')`
- `ERROR test_one_timestamp_per_write.TestRepairAtOpen.test_store_of_a_background_model (point='P2-R1')`
- `ERROR test_one_timestamp_per_write.TestRepairAtOpen.test_store_of_a_background_model (point='Ri-Ri+1, r0 lacks')`
- `ERROR test_one_timestamp_per_write.TestRepairAtOpen.test_store_of_a_background_model (point='Ri-Ri+1, r1 lacks')`
- `ERROR test_one_timestamp_per_write.TestRepairAtOpen.test_store_of_a_second_background_model_beside_the_first`
- `ERROR test_one_timestamp_per_write.TestRepairThenPruneAtOpen.test_an_interrupted_store (prune=False)`
- `ERROR test_one_timestamp_per_write.TestRepairThenPruneAtOpen.test_an_interrupted_store (prune=True)`
- `ERROR test_prune_at_open.TestInterruptedPrune.test_faulted_after_each_shard (after=0)`
- `ERROR test_prune_at_open.TestInterruptedPrune.test_faulted_after_each_shard (after=1)`
- `ERROR test_prune_at_open.TestInterruptedPrune.test_faulted_after_each_shard (after=2)`
- `ERROR test_prune_at_open.TestInterruptedPrune.test_faulted_before_the_first_shard`
- `ERROR test_prune_at_open.TestRecordsStayApart.test_a_get_record_of_a_background_model_is_repaired_not_pruned`
- `ERROR test_prune_at_open.TestRecordsStayApart.test_a_prune_record_over_a_difference_in_another_class_refuses`
- `ERROR test_prune_at_open.TestUninterruptedPrune.test_every_shard_identical_and_no_record_left`
- `ERROR test_reconcile_at_open.TestKillAndReopen.test_store_of_a_background_model (point='C-P2')`
- `ERROR test_reconcile_at_open.TestKillAndReopen.test_store_of_a_background_model (point='P2-R1')`
- `ERROR test_reconcile_at_open.TestKillAndReopen.test_store_of_a_background_model (point='Ri-Ri+1, r0 lacks')`
- `ERROR test_reconcile_at_open.TestKillAndReopen.test_store_of_a_background_model (point='Ri-Ri+1, r1 lacks')`
- `ERROR test_reconcile_at_open.TestKillAndReopen.test_store_of_a_second_background_model_beside_the_first`
- `ERROR test_reconcile_at_open.TestPruningAfterRepair.test_an_interrupted_store (prune=False)`
- `ERROR test_reconcile_at_open.TestPruningAfterRepair.test_an_interrupted_store (prune=True)`
- `FAIL test_declared_facts.TestThePruneRefusalNamesItsUnit.test_a_prune_that_deletes_outside_its_unit`
- `FAIL test_declared_facts.TestTheUnit.test_a_declared_owner_joins_and_an_undeclared_reference_does_not`
- `FAIL test_declared_facts.TestTheUnit.test_every_compared_table_of_the_registry (cls='Gadget')`
- `FAIL test_neutral_client.TestCoverageByDeclaration.test_the_replicated_only_declarations_are_where_the_pool_reads_them`
- `FAIL test_prune_at_open.TestPruneFailsInTheFactory.test_the_record_stays_and_the_next_open_completes_it`
- `FAIL test_reconcile_at_open.TestMismatchLeftByTheCheck.test_a_validate`
- `FAIL test_reconcile_at_open.TestRecordDoesNotExplain.test_part_of_the_recorded_background_model`

**(i)** A client word in a layer comment (`# GkSource` in `store_reader.py`):

```diff
diff --git a/datastorekit/store_reader.py b/datastorekit/store_reader.py
index 46de102..51a7f16 100644
--- a/datastorekit/store_reader.py
+++ b/datastorekit/store_reader.py
@@ -58,7 +58,7 @@ from datastorekit.shard_paths import shard_file_problem
 
 PathType = Union[str, os.PathLike]
 
-_VERB = "read"
+_VERB = "read"  # GkSource
 
 
 @dataclass(frozen=True)
```
`Ran 444 tests in 93.315s` / `FAILED (failures=1)`. The tests that fail:

- `FAIL test_layer_is_generic.TestTheLayerNamesNoProjectWord.test_no_comment`

**(j)** The pinned comment reworded (`shard_key_audit.py:188`, `(e.g. "wavenumber")` removed):

```diff
diff --git a/datastorekit/tools/shard_key_audit.py b/datastorekit/tools/shard_key_audit.py
index 96b9deb..5457447 100644
--- a/datastorekit/tools/shard_key_audit.py
+++ b/datastorekit/tools/shard_key_audit.py
@@ -185,7 +185,7 @@ def main(argv: List[str]) -> int:
     print(f">> shard_keys row count: {len(key_serials)}")
     print(f">> per-shard key distribution: {distribution}")
 
-    # Cross-file check against the actual shard-key table (e.g. "wavenumber"),
+    # Cross-file check against the actual shard-key table,
     # which lives in the replicated tables inside each shard database, not in
     # the primary file. Best-effort: attach one shard file read-only.
     cross_file_done = False
```
`Ran 444 tests in 92.207s` / `FAILED (failures=1)`. The tests that fail:

- `FAIL test_layer_is_generic.TestTheLayerNamesNoProjectWord.test_no_comment`

**(k)** `import datastorekit.tests.client.registry` appended as `store_inventory.py`'s last line (correction 1):

```diff
diff --git a/datastorekit/store_inventory.py b/datastorekit/store_inventory.py
index 10b46da..1cef0eb 100644
--- a/datastorekit/store_inventory.py
+++ b/datastorekit/store_inventory.py
@@ -1047,3 +1047,4 @@ def read_inventory(primary: PathType, factories: Mapping[str, Any]) -> StoreInve
             shards=tuple(shard.serial for shard in store.shards),
             classes=classes,
         )
+import datastorekit.tests.client.registry
```
`Ran 444 tests in 93.654s` / `FAILED (failures=4)`. The tests that fail:

- `FAIL test_inventory_declarations.TestTheLayerKnowsNoProject.test_reading_records_loads_no_project_module`
- `FAIL test_layer_is_generic.TestTheLayerImportsNoProjectPackage.test_every_import_is_allowed`
- `FAIL test_layer_registry.TestTheLayerImportsNoClient.test_a_fresh_interpreter_loads_no_client_registry`
- `FAIL test_layer_registry.TestTheLayerImportsNoClient.test_no_layer_file_imports_a_registry (path='datastorekit/store_inventory.py')`

**(m)** The data file's tables (`registry.keys`) emptied for all three clients:

```diff
diff --git a/datastorekit/tests/data/client_vocabulary.json b/datastorekit/tests/data/client_vocabulary.json
index f2ea09a..7d24d27 100644
--- a/datastorekit/tests/data/client_vocabulary.json
+++ b/datastorekit/tests/data/client_vocabulary.json
@@ -8,46 +8,7 @@
       "registry": {
         "module": "config/datastore.py",
         "name": "factories",
-        "keys": [
-          "version",
-          "store_tag",
-          "redshift",
-          "wavenumber",
-          "wavenumber_exit_time",
-          "tolerance",
-          "LambdaCDM",
-          "QCD_Cosmology",
-          "IntegrationSolver",
-          "BackgroundModel",
-          "BackgroundModel_tags",
-          "BackgroundModelValue",
-          "TkNumericIntegration",
-          "TkNumeric_tags",
-          "TkNumericValue",
-          "TkWKBIntegration",
-          "TkWKB_tags",
-          "TkWKBValue",
-          "GkNumericIntegration",
-          "GkNumeric_tags",
-          "GkNumericValue",
-          "GkWKBIntegration",
-          "GkWKB_tags",
-          "GkWKBValue",
-          "GkSourcePolicy",
-          "GkSourcePolicyData",
-          "GkSource",
-          "GkSource_tags",
-          "GkSourceValue",
-          "GkSource_parents",
-          "QuadSourcePolicy",
-          "QuadSource",
-          "QuadSource_tags",
-          "QuadSourceValue",
-          "QuadSourceIntegral",
-          "QuadSourceIntegral_tags",
-          "OneLoopIntegral",
-          "OneLoopIntegral_tags"
-        ]
+        "keys": []
       },
       "columns": {
         "modules": [
@@ -299,35 +260,7 @@
       "registry": {
         "module": "Datastore/SQL/Datastore.py",
         "name": "_factories",
-        "keys": [
-          "version",
-          "store_tag",
-          "redshift",
-          "tolerance",
-          "beta_value",
-          "M_value",
-          "Lambda_value",
-          "temperature",
-          "phi_value",
-          "pi_value",
-          "InversePowerPotential",
-          "StarobinskyPotential",
-          "ExponentialPotential",
-          "ReclinerPotential",
-          "ReflectingPotential",
-          "ExponentialCoupling",
-          "QCD_Cosmology",
-          "IntegrationSolver",
-          "ScalarModel",
-          "ScalarModel_tags",
-          "ScalarModelValue",
-          "AdiabaticHistory",
-          "AdiabaticHistory_tags",
-          "AdiabaticHistoryValue",
-          "BBNData",
-          "BBNData_tags",
-          "BBNDataValue"
-        ]
+        "keys": []
       },
       "columns": {
         "modules": [
@@ -452,38 +385,7 @@
       "registry": {
         "module": "Datastore/SQL/Datastore.py",
         "name": "_factories",
-        "keys": [
-          "version",
-          "store_tag",
-          "redshift",
-          "tolerance",
-          "efold_value",
-          "delta_Nstar",
-          "N_init",
-          "N_final",
-          "n_collocation_points",
-          "alpha_regularization",
-          "inflaton_mass",
-          "quartic_coupling",
-          "phi_value",
-          "pi_value",
-          "QuadraticPotential",
-          "QuarticPotential",
-          "MasslessDecoupledDiffusion",
-          "IntegrationSolver",
-          "InflatonTrajectory",
-          "InflatonTrajectoryValue",
-          "CosmologicalParams",
-          "FullInstanton",
-          "FullInstantonValue",
-          "GradientCoupledInstanton",
-          "GradientCoupledInstantonValue",
-          "GradientCoupledInstantonProfile",
-          "SlowRollInstanton",
-          "SlowRollInstantonValue",
-          "CompactionFunction",
-          "CompactionFunctionSamples"
-        ]
+        "keys": []
       },
       "columns": {
         "modules": [
```
`Ran 444 tests in 92.864s` / `FAILED (failures=2)`. The tests that fail:

- `FAIL test_layer_is_generic.TestTheLayer.test_the_vocabulary_holds_the_registry_and_the_packages`
- `FAIL test_layer_is_generic.TestTheLayerNamesNoProjectWord.test_no_comment`

**(l)** The `origin` member deleted from `Weave_factory.inventory_spec` (`client/factories.py:1684`):

```diff
diff --git a/datastorekit/tests/client/factories.py b/datastorekit/tests/client/factories.py
index 683fe9a..7ae8803 100644
--- a/datastorekit/tests/client/factories.py
+++ b/datastorekit/tests/client/factories.py
@@ -1681,7 +1681,6 @@ class Weave_factory(SQLAFactoryBase):
                     "weave_serial",
                     {
                         "anchor": Parent("anchor_serial", "Tessera", nullable=True),
-                        "origin": Parent("origin_serial", "Trace", nullable=True),
                     },
                 )
             },
```
`Ran 444 tests in 105.970s` / `FAILED (failures=2)`. The tests that fail:

- `FAIL test_parent_set_members.TestTheSecondMember.test_the_set_declares_both_members_in_order`
- `FAIL test_parent_set_members.TestTheSecondMember.test_varying_the_second_member_changes_only_the_weave`

**(n)** (n), the vacuous retarget: `PROJECT_PACKAGES` set back to SGK's tuple, with (k):

```diff
diff --git a/datastorekit/store_inventory.py b/datastorekit/store_inventory.py
index 10b46da..1cef0eb 100644
--- a/datastorekit/store_inventory.py
+++ b/datastorekit/store_inventory.py
@@ -1047,3 +1047,4 @@ def read_inventory(primary: PathType, factories: Mapping[str, Any]) -> StoreInve
             shards=tuple(shard.serial for shard in store.shards),
             classes=classes,
         )
+import datastorekit.tests.client.registry
diff --git a/datastorekit/tests/test_inventory_declarations.py b/datastorekit/tests/test_inventory_declarations.py
index 7b3ba4c..ef28aa9 100644
--- a/datastorekit/tests/test_inventory_declarations.py
+++ b/datastorekit/tests/test_inventory_declarations.py
@@ -449,7 +449,13 @@ class TestResolve(unittest.TestCase):
 # 4. the layer loads no project package when it runs
 # ------------------------------------------------------------------------------------------------
 
-PROJECT_PACKAGES = ("datastorekit.tests",)
+PROJECT_PACKAGES = (
+    "CosmologyModels",
+    "CosmologyConcepts",
+    "ComputeTargets",
+    "MetadataConcepts",
+    "config",
+)
 
 
 def _run(code):
```
`Ran 444 tests in 96.014s` / `FAILED (failures=3)`. The tests that fail:

- `FAIL test_layer_is_generic.TestTheLayerImportsNoProjectPackage.test_every_import_is_allowed`
- `FAIL test_layer_registry.TestTheLayerImportsNoClient.test_a_fresh_interpreter_loads_no_client_registry`
- `FAIL test_layer_registry.TestTheLayerImportsNoClient.test_no_layer_file_imports_a_registry (path='datastorekit/store_inventory.py')`

**(o)** The guard reads its data, not a client. No diff: a scratch runner
(`<scratchpad>/tools/breakage_o.py`) writes a copy of the committed data file with `CosmologyModels`
removed from every client's packages, sets the guard module's `VOCABULARY` to the copy, and runs
the guard's tests. The committed file is not edited. The runner:

```python
import json
import sys
import unittest
from pathlib import Path

from datastorekit.tests import test_layer_is_generic as guard

copy = Path(sys.argv[1])
data = json.loads(guard.VOCABULARY.read_text())
for client in data["clients"].values():
    client["packages"] = [p for p in client["packages"] if p != "CosmologyModels"]
copy.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
guard.VOCABULARY = copy
print(f"VOCABULARY -> {guard.VOCABULARY}", flush=True)
suite = unittest.defaultTestLoader.loadTestsFromModule(guard)
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
```

`Ran 8 tests` / `FAILED (failures=1)`, exit 1:

- `FAIL test_layer_is_generic.TestTheLayer.test_the_vocabulary_holds_the_registry_and_the_packages`
  (`{'MetadataConcepts', 'CosmologyModels', 'Caching'} not less than or equal to {…}`)

### 6.4 What each breakage fails, and SGK's counterparts

| | Fails | Does SGK's counterpart pin the same line? |
|---|---|---|
| (a)–(d), (p), (q) | the check exits 1, naming the test, the declaration or the file | — (the checks) |
| (e) | `TestTheDerivedOrder`: three tests; and 04a's `test_every_class_has_a_record` | yes: SGK's `TestTheDerivedOrder` asserts the same order of `inventory_classes` |
| (f) | `TestDependentTables`: two tests (three subtests of one); `TestThePoolRefuses`: two; and 02's `test_dependent_tables_accepts_each_group_as_declared` (three subtests) | yes: SGK's `TestDependentTables` |
| (g) | `test_an_owner_column_with_no_foreign_key` | yes |
| (h) | `TestTheUnit`: both tests; `TestThePruneRefusalNamesItsUnit`; and 4 failures and 26 errors of 02's, 03a's and 03b's prune and repair tests | yes: SGK's `TestTheUnit` and `TestThePruneRefusalNamesItsUnit` |
| (i) | `test_no_comment`, naming `datastorekit/store_reader.py:61 GkSource` | yes: SGK's comment scan |
| (j) | `test_no_comment`, the pinned hit missing | no: SGK's guard has no pinned hit (U17 is new) |
| (k) | `test_every_import_is_allowed`, `test_reading_records_loads_no_project_module`, `test_a_fresh_interpreter_loads_no_client_registry`, `test_no_layer_file_imports_a_registry` | yes, for SGK's client: an import of `config.datastore` fails SGK's same four |
| (m) | `test_the_vocabulary_holds_the_registry_and_the_packages` and `test_no_comment` (correction 2) | in kind: SGK's reads its registry, not a data file |
| (l) | both of `test_parent_set_members` | no counterpart: the module is new |
| (n) | (k)'s less `test_reading_records_loads_no_project_module`: SGK's tuple makes the class vacuous | — |
| (o) | `test_the_vocabulary_holds_the_registry_and_the_packages` | — |

No mutation failed nothing, so no issue is opened for one.

## 7. Observations not acted on

1. **`test_inventory_declarations`' module docstring still says "resolve() and the report"** (its
   item 3). The report test is not ported (U16), so the sentence overstates the module. It is SGK's
   prose ported unchanged, and left for the prose rewrite of
   `[01-package-prose-names-sgks-layout]`.
2. **`test_layer_registry`'s prose still names SGK's command line and config** (`config/datastore.py`,
   `config.datastore`, "main.py offers list(drop_groups) as --drop's choices" in
   `test_the_groups_are_in_the_command_line_order`). The constant's own comment now says the neutral
   client has no command line (deviation 10); the rest is SGK's prose ported unchanged.
3. **`FORBIDDEN_PACKAGES` cannot bite in this repository by itself.** No client package is on the
   path, so a fresh interpreter can never load one; the retargeted `FORBIDDEN_MODULES` and the
   factory-prefix test are what fail under (k). It is kept as §2.4 directs.
4. **`test_read_inventory_loads_only_what_the_registry_loads` cannot fail on (k)**, here or in SGK:
   the registry is imported before the snapshot (correction 1).
5. **The two scratch probes of U22** are in the scratchpad (`tools/probe_u20_declared_facts.py`,
   `probe_u22/probe_declared_facts.py`), not in the repository.

## 8. `[01-package-prose-names-sgks-layout]`, re-measured (§2.9)

By log 03a §8's method (a scratch reimplementation, `tools/prose.py`), which reproduces the
earlier figures first: **102** lines in 19 files at `8bc60a5` (01's 101, and the comment 02 moved
by hand), **114** in 23 at `72cf34a`, **124** in 28 at `ae94aaa`, and **146 in 35 at `7ceed25`**.

**After this prompt: 155 lines in 40 files**, +9 in 5 files:

| File | Lines | At |
|---|---|---|
| `tests/test_layer_registry.py` | 3 | `:2` (`prompts/datastore-generic`), `:75` (the new `COMMAND_LINE_ORDER` comment, "the source's … main.py"), `:176` (`main.py`, SGK's comment) |
| `tests/test_drop_refuses_dangling_references.py` | 2 | `:2` (`prompts/…`), `:10` (`Datastore.SQL.schema`) |
| `tests/test_layer_is_generic.py` | 2 | `:71` ("repository root", SGK's docstring of `layer_files`, true here); `:200` (`tools/` in `KNOWN_HITS`' entry, the package's own path) |
| `tests/test_inventory_declarations.py` | 1 | `:2` (`prompts/…`) |
| `tests/test_declared_facts.py` | 1 | `:2` (`prompts/…`) |

Two of the guard's lines are matches of the pattern that do not name SGK's layout (`:71`, `:200`);
they are counted, as the method counts. `test_parent_set_members.py` adds none. Their SGK
references outside the pattern: "audit C1 rows 12 and 13", "audit §C", SGK's README §0.2,
§6.1 and §6.2 (U4), SGK's prompts 06–09, `measure/out/f2_closure.txt` (gone with its comment).

## 9. Issues

- **Closed:** `[04a-no-test-pins-a-second-parent-set-member]` (§4; (l) fails both tests of
  `test_parent_set_members`).
- **Changed:** `[01-package-prose-names-sgks-layout]`: 146 → **155 lines**, 35 → **40 files** (§8).
- **Opened:** none.

The index is at **6 open**: 2 on this board, 4 inherited.

## 10. State handed to the next prompt

- `HEAD` is `0c66505`. The tree is clean, and `venv/` is unchanged.
- **The suite is 444** (`Ran 444 tests … OK`). 05 records 444 as its "before".
- **The checks.** `compare_ported_tests.py` exits 0 over twenty modules with one test declared not
  ported; `compare_with_source.py` exits 0 with 31 compared, 20 `PORTED` and 10 with no source.
- **The guard.** `datastorekit/tests/test_layer_is_generic.py` reads
  `datastorekit/tests/data/client_vocabulary.json`. A re-measure (for example after a client adds
  tables) runs `measure_client_vocabulary.py --output <new file>` and points `VOCABULARY` at it; the
  committed file is never edited. `KNOWN_HITS` holds one comment, to be emptied when the layer's
  prose is rewritten after 05 (U17).
- **For 05:** the suite runs at both ends of the version table. The guard uses
  `sys.stdlib_module_names` (Python ≥ 3.10) and the measuring script needs `git` and the three
  clients' repositories, which CI will not have; CI runs the guard on the committed data file,
  never the script.
