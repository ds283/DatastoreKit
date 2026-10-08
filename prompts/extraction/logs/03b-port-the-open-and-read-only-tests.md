# Log 03b — port the open and read-only tests

**Subject:** Port the version-row, read-only and refusal tests · **Commit:** `0d5380c` ·
**Date:** 2026-10-08 · **Model:** Claude Opus 5.5 · **Result:** landed. SGK's
`test_version_row_at_open` (12), `test_read_only_pool` (23), `test_one_timestamp_per_write` (1
defined, 28 run), `test_absolute_shard_record_refused` (12) and `test_closed_store_refusals` (5)
run in `datastorekit/tests/` under their names, on the stand-in pool and the neutral client, with
U12's four renames; `compare_ported_tests.py` finds the eight ported modules' tests, classes, bases
and assertion skeletons equal to SGK's; `compare_with_source.py` accounts for the five as `PORTED`
and `client/reader.py` as no-source. The neutral client has `gauge_setting` and `routing_rule`
(U13), and `client/reader.py` holds the neutral store, reader sequence and instrument (U11).
`Ran 268 tests … OK` (188 before). No issue opened or closed; `[01-package-prose-names-sgks-layout]`
is re-measured at 124 lines in 28 files. The index stays at 6.

Prompt: [`../03b-port-the-open-and-read-only-tests.md`](../03b-port-the-open-and-read-only-tests.md),
with the orchestrator's dispatch note (one correction and four additions, applied as given). The
work was interrupted once by a usage limit with nothing committed, and resumed from the tree as it
stood (the suite at 268 OK); one commit was made, at the end.

## 1. What shipped

- **Five ported modules**, each SGK's at `6f7f291` with the changes of 03a §2.1 only:
  `datastorekit/tests/test_version_row_at_open.py`, `test_read_only_pool.py`,
  `test_one_timestamp_per_write.py`, `test_absolute_shard_record_refused.py`,
  `test_closed_store_refusals.py`. Every class and method keeps its name, but for U12's four.
- **`datastorekit/tests/client/reader.py`** (new, no source): §1.6.
- **The two classes (U13)**, by addition, in `client/objects.py`, `factories.py`, `registry.py`,
  and `build.py`, whose one changed function is `write_every_class`: §1.4.
- **`test_neutral_client.py`**: the `KEPT` and `counts` literals; **`docs/client-contract.md`**: five
  client cells (§1.5).
- **`docs/extraction/compare_ported_tests.py`**: `PORTED` gains the five pairs, `NAME_MAP` U12's four
  renames. **`compare_with_source.py`**: `FILES` gains the five as `PORTED`, `NO_SOURCE` gains
  `reader.py` (and the comment above `NO_SOURCE` names it).
- **The records**: this log; the board (header, §1's row, §3); `docs/OPEN_ISSUES.md`;
  `prompts/INDEX.md`.

### 1.1 The map as used (§2.2)

Each row is the planner's unless it says otherwise. Columns and payload keys move with their table
(R-map); values by R-value.

| SGK | Used for | Neutral, as used | Changed from the planner's row? |
|---|---|---|---|
| `tolerance` (`log10_tol`; payload `tol`) | an unversioned replicated leaf a get inserts; four per frame in the sequence; the unversioned insert of `TestInsertBeforeSetVersion` | `gauge_setting` (`gauge_exponent`; payload `exponent`), `build.get_gauge`. R-value: `tol=1.0e-N` → `exponent=N` (1e-10 → 10, 1e-9 → 9, 1e-5 → 5); SGK's `DEFAULT_QUADRATURE_RTOL` → `reader.DEFAULT_GAUGE` (12), its `DEFAULT_HEXIT_*` pair → `reader.ALIAS_GAUGES` (4, 8) | no |
| `GkSourcePolicy` (`label`, `Levin_threshold`, `numeric_policy`) | a versioned replicated class a get inserts | `routing_rule` (`rule_label`, `rule_threshold`, `rule_mode`; payload `label`, `threshold`, `mode`). R-value: `numeric_policy="maximize-numeric"` → `mode="prefer-direct"`; SGK's two QSI policies → `build.ROUTING_RULES` (`rule-low` 1.5, `rule-high` 5.0) | no |
| `LambdaCDM` | the sequence's first frame, which has a validated model | `dial_setting` (`reader.DIAL_FRAME`, `build_store`'s `(3, 1)`, the frame of `gadget-one`) | no |
| `QCD_Cosmology` | the frame with no validated model: where the sequence stops | `knob_setting` (`reader.KNOB_FRAME`, `(7, 2)`, the frame of the unvalidated `gadget-two`) | no |
| `wavenumber` (`k_inv_Mpc`; `is_source`, `is_response`) | the shard-key class, read by `read_table`, got as a new shard key | `keypoint` (`position`; `marked`, `flagged`) | no |
| `redshift` | the backstop's flag update on a hit | `keypoint` (0.5, held marked, asked for marked and flagged) | no |
| `wavenumber_exit_time` | the stored proxy | `keypoint_alias`; `build.make_alias` / an `object_get` of `objects.keypoint_alias` | no |
| `BackgroundModel` | the replicated owner: got, validated, pruned | `Gadget`; `build.make_framed_gadget` (version row), an `object_get` of `objects.Gadget` | no |
| `GkSourcePolicyData` | a sharded versioned class, stored | `Sample`, `build.make_sample_on` | no |
| `GkSource` (validates), `OneLoopIntegral` (does not) | a table a shard may lack | `Sample`, `Tessera` | no |
| `GkNumericValue` | a sharded class a vectorized get inserts into | `Tessera` (a new weight, 0.875) | no |
| `QuadSourcePolicy`, `QuadSource`, `QuadSourceIntegral`, the probe's `GkSource` | the sequence's further reads | `reader.reader_sequence` (§1.6) | — |
| `config.defaults.DEFAULT_*`, `Planck2018`, `extract_common.run_label_tag` | SGK's values and labels | constants of `client/reader.py` and its `run_label_tag` (§1.6) | no |
| `sp.make_units`, `sp.StandinCosmology`, `self.units` | SGK's units and cosmology | removed | no |
| `sp.StandinSerial` | a handle read for its `store_id` | `objects.SerialHandle` | no |

`version` and `store_tag` keep their names. The one helper renamed (R-help) is
`TestOtherWritesRaiseReadOnlyWrite.lcdm` → `dial_frame` (it asserts nothing).

### 1.2 The port table (§4.4)

One row per defined test. "Kinds in the test" are those inside the test method. Every test also
runs under its module's changes: R-imp (the imports), and R-help (`setUp` without `units`; the
pool's getter `shard_key_store_id`; in `test_read_only_pool`, `rw` imported in place of
`_load_probe` and `rw.reader_sequence` in place of `qsi_sequence`, and the helpers `dial_frame` and
`exit_time`). The classes column lists what the test uses, directly or through its fixture.

| # | SGK origin (module · class · method) | Package name if renamed | Kinds in the test | SGK classes → neutral |
|---|---|---|---|---|
| 1 | `test_version_row_at_open` · `TestNewStore` · `test_the_row_is_written_once_through_the_recorded_write` | — | — | — (the layer's `version` only) |
| 2 | `test_version_row_at_open` · `TestNewStore` · `test_no_actor_constructor_inserts_the_row` | — | — | — |
| 3 | `test_version_row_at_open` · `TestNewStore` · `test_versioned_rows_carry_the_serial_on_every_shard` | — | R-help, R-map, R-value | `tolerance`→`gauge_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias`, `GkSourcePolicy`→`routing_rule` (helper `policy`), `BackgroundModel`→`Gadget` (with `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint` through `make_framed_gadget`), `GkSourcePolicyData`→`Sample` |
| 4 | `test_version_row_at_open` · `TestNewLabelInterrupted` · `test_a_fault_after_the_controller_commits` | — | — | — |
| 5 | `test_version_row_at_open` · `TestNewLabelInterrupted` · `test_a_fault_before_the_controller_commits` | — | — | — |
| 6 | `test_version_row_at_open` · `TestNewLabelInterrupted` · `test_a_fault_on_one_replica_only` | — | — | — |
| 7 | `test_version_row_at_open` · `TestNewLabelInterrupted` · `test_a_label_no_shard_holds_is_written_through_the_recorded_write` | — | — | — |
| 8 | `test_version_row_at_open` · `TestNewStoreInterrupted` · `test_interrupted_at_the_version_write` | — | — | — |
| 9 | `test_version_row_at_open` · `TestInsertBeforeSetVersion` · `test_a_versioned_insert_raises_names_the_class_and_writes_nothing` | — | R-map, R-value (`POLICY`) | `GkSourcePolicy`→`routing_rule` |
| 10 | `test_version_row_at_open` · `TestInsertBeforeSetVersion` · `test_an_unversioned_insert_is_not_refused_and_set_version_admits_the_rest` | — | R-map, R-value | `tolerance`→`gauge_setting` (`tol=1.0e-5`→`exponent=5`), `GkSourcePolicy`→`routing_rule` |
| 11 | `test_version_row_at_open` · `TestVersionDifferenceWithNoRecord` · `test_refused_naming_the_class_and_nothing_written` | — | — | — |
| 12 | `test_version_row_at_open` · `TestTheLicenceAndTheVersionRow` · `test_a_prune_record_is_refused_where_a_get_record_is_admitted` | — | — | — |
| 13 | `test_read_only_pool` · `TestNothingWrittenOnAFullStore` · `test_the_instrument_counts_a_read_write_pool_then_read_only_writes_nothing` | — | R-help, R-count, R-map | the whole sequence (§1.6): `BackgroundModel`→`Gadget`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias`, `redshift` (read_table)→`dial_setting` (read_table), `GkSourcePolicy`→`routing_rule`, `GkSourcePolicyData`→`Sample`, `LambdaCDM`→`dial_setting`, `QCD_Cosmology`→`knob_setting`, `tolerance`→`gauge_setting`; `21`→`18`, the six outcome strings and their step names, the stop message |
| 14 | `test_read_only_pool` · `TestNothingWrittenOnAFullStore` · `test_a_replicated_get_is_one_call_to_the_drawn_shard` | — | R-help, R-map, R-value | `tolerance`→`gauge_setting` (`DEFAULT_QUADRATURE_RTOL`→`DEFAULT_GAUGE`) |
| 15 | `test_read_only_pool` · `TestEachMissRaisesReadOnlyMiss` · `test_store_tag` | — | R-imp (`run_label_tag` from `reader`) | — (the layer's `store_tag`) |
| 16 | `test_read_only_pool` · `TestEachMissRaisesReadOnlyMiss` · `test_LambdaCDM` | `test_dial_setting` | R-name, R-map, R-value (payload by column) | `LambdaCDM`→`dial_setting`; the sequence |
| 17 | `test_read_only_pool` · `TestEachMissRaisesReadOnlyMiss` · `test_QCD_Cosmology` | `test_knob_setting` | R-name, R-map, R-value (payload by column) | `QCD_Cosmology`→`knob_setting`; the sequence |
| 18 | `test_read_only_pool` · `TestEachMissRaisesReadOnlyMiss` · `test_tolerance` | `test_gauge_setting` | R-name, R-map, R-value (payload by column) | `tolerance`→`gauge_setting`; the sequence |
| 19 | `test_read_only_pool` · `TestEachMissRaisesReadOnlyMiss` · `test_GkSourcePolicy` | `test_routing_rule` | R-name, R-map, R-value (payload by column) | `GkSourcePolicy`→`routing_rule`; the sequence |
| 20 | `test_read_only_pool` · `TestOtherWritesRaiseReadOnlyWrite` · `test_object_store_sharded_and_replicated` | — | R-help, R-map, R-value | `GkSourcePolicyData`→`Sample`, `wavenumber_exit_time`→`keypoint_alias`, `tolerance`→`gauge_setting`, `LambdaCDM`→`dial_setting` (helpers `exit_time`, `dial_frame`) |
| 21 | `test_read_only_pool` · `TestOtherWritesRaiseReadOnlyWrite` · `test_object_validate` | — | R-imp, R-help, R-map, R-value (tags) | `BackgroundModel`→`Gadget`, `LambdaCDM`→`dial_setting` |
| 22 | `test_read_only_pool` · `TestOtherWritesRaiseReadOnlyWrite` · `test_the_actors_refuse_store_and_validate_themselves` | — | R-help | `GkSourcePolicyData`→`Sample`, `wavenumber_exit_time`→`keypoint_alias` (helper `exit_time`) |
| 23 | `test_read_only_pool` · `TestOtherWritesRaiseReadOnlyWrite` · `test_a_new_shard_key` | — | R-map, R-value | `wavenumber`→`keypoint` (`k_inv_Mpc=3.0e8`→`position=3.0e8`, `is_source`/`is_response`→`marked`/`flagged`) |
| 24 | `test_read_only_pool` · `TestOtherWritesRaiseReadOnlyWrite` · `test_a_vectorized_get_that_reaches_an_inserter` | — | R-help, R-map, R-value | `GkNumericValue`→`Tessera` (one new weight), `wavenumber_exit_time`→`keypoint_alias` |
| 25 | `test_read_only_pool` · `TestOtherWritesRaiseReadOnlyWrite` · `test_drop_actions_and_prune_refuse_before_anything_is_opened` | — | R-map | `GkSourcePolicyData`→`Sample` |
| 26 | `test_read_only_pool` · `TestOtherWritesRaiseReadOnlyWrite` · `test_the_backstop_a_flag_update_on_a_hit` | — | R-map, R-value | `redshift`→`keypoint` (`z=1.0e5`→`position=0.5`, flags) |
| 27 | `test_read_only_pool` · `TestAtOpen` · `test_a_missing_primary_creates_nothing` | — | — | — |
| 28 | `test_read_only_pool` · `TestAtOpen` · `test_an_empty_journal_beside_a_shard_is_refused` | — | — | — |
| 29 | `test_read_only_pool` · `TestAtOpen` · `test_an_empty_journal_beside_the_primary_is_refused` | — | — | — |
| 30 | `test_read_only_pool` · `TestAtOpen` · `test_a_hot_journal_beside_a_shard_is_refused_and_not_rolled_back` | — | — (`HOT_JOURNAL_CHILD`'s SQL is R-map) | `tolerance`→`gauge_setting` |
| 31 | `test_read_only_pool` · `TestAtOpen` · `test_a_record_of_any_operation_is_refused_by_name_and_not_cleared` | — | R-map | `tolerance`→`gauge_setting`, `BackgroundModel`→`Gadget` |
| 32 | `test_read_only_pool` · `TestAtOpen` · `test_an_absent_version_label_is_refused_naming_the_labels_present` | — | — | — |
| 33 | `test_read_only_pool` · `TestAtOpen` · `test_diverged_shards_are_refused_and_nothing_repaired` | — | R-map, R-value | `tolerance`→`gauge_setting` |
| 34 | `test_read_only_pool` · `TestAtOpen` · `test_a_shard_lacking_a_table_is_refused_naming_it` | — | R-map | `GkSource`→`Sample`, `OneLoopIntegral`→`Tessera` |
| 35 | `test_read_only_pool` · `TestAtOpen` · `test_every_connection_is_opened_read_only` | — | R-imp (the patched module path, a string) | the sequence |
| 36 | `test_one_timestamp_per_write` · `TestVersionRowOfANewStore` · `test_the_version_row_is_its_serial_and_label` | — | — | — |
| 37 | `test_absolute_shard_record_refused` · `TestTheResolver` · `test_resolve_shard_path_refuses_an_absolute_record` | — | — | — |
| 38 | `test_absolute_shard_record_refused` · `TestTheResolver` · `test_the_bare_name_of_the_same_file_is_not_refused` | — | — | — |
| 39 | `test_absolute_shard_record_refused` · `TestEveryReader` · `test_the_constructors_read_of_the_shards_table` | — | — | — |
| 40 | `test_absolute_shard_record_refused` · `TestEveryReader` · `test_a_primary_naming_its_own_siblings_is_refused_the_same_way` | — | — | — |
| 41 | `test_absolute_shard_record_refused` · `TestEveryReader` · `test_copy_store` | — | — | — |
| 42 | `test_absolute_shard_record_refused` · `TestEveryReader` · `test_move_store` | — | — | — |
| 43 | `test_absolute_shard_record_refused` · `TestEveryReader` · `test_closed_store_files` | — | — | — |
| 44 | `test_absolute_shard_record_refused` · `TestEveryReader` · `test_delete_store` | — | — | — |
| 45 | `test_absolute_shard_record_refused` · `TestEveryReader` · `test_delete_store_resuming` | — | — | — |
| 46 | `test_absolute_shard_record_refused` · `TestEveryReader` · `test_closed_store_files_resuming` | — | — | — |
| 47 | `test_absolute_shard_record_refused` · `TestEveryReader` · `test_the_read_only_reader` | — | — | — (the registry, R-imp) |
| 48 | `test_absolute_shard_record_refused` · `TestEveryReader` · `test_the_store_it_names_is_not_refused` | — | — | — |
| 49 | `test_closed_store_refusals` · `TestEachPrefixOnce` · `test_delete_and_closed_store_files_state_their_prefix_once` | — | — | — |
| 50 | `test_closed_store_refusals` · `TestEachPrefixOnce` · `test_copy_and_move_state_their_prefix_once` | — | — | — |
| 51 | `test_closed_store_refusals` · `TestEachPrefixOnce` · `test_the_reader_states_its_prefix_once` | — | — | — (the registry, R-imp) |
| 52 | `test_closed_store_refusals` · `TestEachPrefixOnce` · `test_an_unreadable_shards_table_is_named_once_by_each` | — | — | — (the registry, R-imp) |
| 53 | `test_closed_store_refusals` · `TestTheBareReason` · `test_read_closed_store_states_no_prefix` | — | — | — |

**The 27 inherited tests**, run by `test_one_timestamp_per_write` under the ticking clock (each kept
by its own module's port check, not this module's):

- `TestRepairAtOpen` (`reconcile_at_open.TestKillAndReopen`, 12): `test_scalar_get`,
  `test_scalar_get_of_the_shard_key`, `test_scalar_get_that_turns_a_flag_on`, `test_vectorized_get`,
  `test_vectorized_get_that_inserts_and_turns_a_flag_on`, `test_get_that_inserts_nothing`,
  `test_store_of_an_exit_time`, `test_store_of_a_background_model`,
  `test_store_of_a_second_background_model_beside_the_first`, `test_validate_of_a_background_model`,
  `test_validate_whose_controller_counts_short`, `test_between_the_record_cleared_and_the_shard_key`;
- `TestRepairThenPruneAtOpen` (`reconcile_at_open.TestPruningAfterRepair`, 2):
  `test_an_interrupted_validate`, `test_an_interrupted_store`;
- `TestCompletionOfAnInterruptedPrune` (`prune_at_open.TestInterruptedPrune`, 2):
  `test_faulted_after_each_shard`, `test_faulted_before_the_first_shard`;
- `TestPruneAtOpen` (`prune_at_open.TestUninterruptedPrune`, 3):
  `test_every_shard_identical_and_no_record_left`,
  `test_a_prune_with_nothing_to_prune_writes_nothing`,
  `test_the_set_of_classes_is_read_from_the_factories`;
- `TestVersionRowOfANewStore` (`version_row_at_open.TestNewStore`, 3):
  `test_the_row_is_written_once_through_the_recorded_write`,
  `test_no_actor_constructor_inserts_the_row`, `test_versioned_rows_carry_the_serial_on_every_shard`;
- `TestVersionRowOfANewLabel` (`version_row_at_open.TestNewLabelInterrupted`, 4):
  `test_a_fault_after_the_controller_commits`, `test_a_fault_before_the_controller_commits`,
  `test_a_fault_on_one_replica_only`,
  `test_a_label_no_shard_holds_is_written_through_the_recorded_write`;
- `TestVersionRowOfAnInterruptedNewStore` (`version_row_at_open.TestNewStoreInterrupted`, 1):
  `test_interrupted_at_the_version_write`.

**Control flow**, measured beside the port check: for each of the 116 functions of SGK's five
modules, the sequence of `If`, `For`, `While`, `With` (with its item count), `Try`, `Return`,
`Raise`, `Break`, `Continue`, conditional expressions, comprehensions, lambdas and nested `def`s
equals the package's (after U12's renames and `lcdm` → `dial_frame`), but for `_load_probe`, which
goes (addition 4). No function is added.

### 1.3 The rewritten docstring sentences (§2.1)

`test_read_only_pool`'s module docstring, `:5-10`. **Before:**

> The store is the audit's full store, and the lookup sequence is QSI's: both are **imported** from
> ``docs/a3-v2-readiness/reader_writes_probe.py`` (``build_full_store``, ``qsi_sequence``,
> ``other_sharded_lookups``), so that the sequence run here is the one audit R2 measured, not a
> second transcription of it. That probe guards its own run behind ``__main__``, so importing it
> runs nothing.

**After:**

> The store is the neutral client's full store, and the lookup sequence is a reader's on the neutral
> client: both are **imported** from ``datastorekit.tests.client.reader`` (``build_full_store``,
> ``reader_sequence``, ``other_sharded_lookups``), which stands in for the audit probe the source
> repository's test imported, and keeps that probe's instrument. Importing it runs nothing.

`_load_probe`'s comment has nothing to rewrite: `_load_probe` goes (addition 4), and with it
`REPO_ROOT`, `PROBE` and the imports only it used (`importlib.util`; `math` went with the two
lambdas that used it). The docstring's list of misses (`:21-22`) is R-map, not this rewrite.

### 1.4 The two classes (U13)

- **`objects.gauge_setting(store_id, exponent)`** and **`objects.routing_rule(store_id, label,
  threshold, mode)`**, after `knob_setting`.
- **`factories.gauge_setting_factory`**: `register()` = `{"version": False, "timestamp": True,
  "columns": [gauge_exponent Integer not null]}`; `build` gets by `exponent` and inserts on a miss,
  honouring a payload `serial`, setting `_new_insert` / `_deserialized` as `knob_setting_factory`
  does; `inventory_spec()` = `InventorySpec(leaves=("gauge_exponent",))`.
- **`factories.routing_rule_factory`**: `register()` = `{"version": True, "timestamp": True,
  "columns": [rule_label String(DEFAULT_STRING_LENGTH), rule_threshold Float(64), rule_mode
  String(DEFAULT_STRING_LENGTH)]}`, all not null; `build` gets by all three, inserts on a miss as
  above; `inventory_spec()` names the three as leaves.
- **`registry`**: both in `factories` and in `replicated_tables`, after `knob_setting`; in no drop
  group, not in `read_table_config` or `serial_batch_sizes`; `__all__` unchanged. Its docstring's
  role table gains two rows, and one sentence says the two are in no drop group.
- **`build`**: `GAUGE_EXPONENTS = (4, 8)`, `ROUTING_RULES = (("rule-low", 1.5, "prefer-direct"),
  ("rule-high", 5.0, "prefer-direct"))`; `get_gauge(pool, exponent)`, `get_rule(pool, label,
  threshold, mode)`; `write_every_class` writes both gauges and both rules right after the knob
  setting (two lines, and one docstring bullet). No other line of `build.py` changes.

`git diff` of `objects.py`, `factories.py`, `registry.py` and `build.py` against `72cf34a` has no
removed line.

### 1.5 The ripple: `test_neutral_client.py` and the contract

With only the classes added (before either literal changed), the suite gave `Ran 188 tests` /
`FAILED (failures=2)`, exactly the two §2.3 names:
- `TestTheRegistry.test_dependent_tables_accepts_each_group_as_declared`: `KEPT` gains
  `"gauge_setting"`, `"routing_rule"` (in registry order, after `knob_setting`; `black` re-wraps
  the list);
- `TestRoundTrip.test_the_reader_and_the_inventory_read_every_class`: `counts` gains
  `"gauge_setting": 2`, `"routing_rule": 2`.

Then `Ran 188 tests … OK`; 03a's four modules, run alone, `Ran 79 tests … OK`, unedited.

`docs/client-contract.md`, client columns only:
- §1 row 5 (`replicated_tables`): `(9 classes)` → `(11 classes)`;
- §1 row 15 (`factories`): `(14 classes)` → `(16 classes)`;
- §2 `version` row (`:67`): `routing_rule` added to the classes with `True`;
- §2 `timestamp` row (`:68`): `gauge_setting`, `routing_rule` added to the classes with `True`;
- §3 `inventory_spec()` row (`:98`): `9 classes` → `11 classes`.

The other client cells hold as they are ("every spec", "every factory but the three association
tables", "every get-or-insert `build`", …).

### 1.6 `client/reader.py`

**The instrument**, transcribed from the probe at `6f7f291` with its behaviour unchanged (R-imp
only: `sp` is `datastorekit.tests.standin_pool`):

| Item | Probe lines |
|---|---|
| `change_counter` | `:133-136` |
| `table_counts` (correction 1) | `:139-146` |
| `file_state` | `:149-159` |
| `state_delta` | `:162-191` |
| `ReplicatedWriteLog` (with `since`) | `:220-261` |
| `Step` | `:279-300` |
| `Recorder` (`__init__`, `step`) | `:303-310` |
| `quiet` | `:341-344` |

`Recorder.print` (`:312-333`), `describe_delta` (`:194-217`) and `summarise_writes` (`:264-276`) are
left out: the test never prints (deviation 2). Every file is read as bytes (`file_state`,
`change_counter`) or through `standin_pool._read` (`mode=ro`), so the instrument passes
`test_every_connection_is_opened_read_only`, which patches `sqlite3.connect` for the whole process.

**The constants:** `RUN = "north"` and `run_label_tag(run) -> f"tag-{run}"`, so the run's tag is
`build_store`'s `tag-north` (the tag of `gadget-one`); `DIAL_FRAME = (3, 1)`, `KNOB_FRAME = (7, 2)`,
`FRAMES = (("dial", "gadget-one"), ("knob", "gadget-two"))`; `ALIAS_GAUGES = (4, 8)` (build's),
`WORK_GAUGES = (10, 12)`, `SEQUENCE_GAUGES` the four, `DEFAULT_GAUGE = 12`; `RULE_LOW`, `RULE_HIGH`
(build's two, as payload dicts); `RUN_SAMPLE_CODE = "sample-run"`, `MISSED_SAMPLE_CODE =
"sample-elsewhere"`; `CONTEXT`, `FACTS` as in the probe.

**`build_full_store(primary, cluster)`** opens the pool with `build.open_pool`, calls
`build.write_every_class`, and then writes, through the pool, only what the sequence needs beyond
it: the two work gauges (10, 12) and one validated Sample (`sample-run`, on the marked keypoint 0.5,
keyed on `gadget-one`, tagged with the run's tag), the counterpart of the probe's one stored
`GkSourcePolicyData`. It returns the facts, keyed by neutral class (`store_tag`, `dial_setting`,
`knob_setting`, `Gadget`, `validated`, `unvalidated`, `keypoint_alias`, `routing_rule`, `Sample`,
`gauge_setting` → `{exponent: serial}`). The full store holds four gauges and two rules; the
aliases, Gadgets and tags are `build_store`'s.

**`reader_sequence(pool, rec)`**, the step table. Outcomes are measured on the full store; they are
equal on the read-write and the read-only run (serials vary between builds: the test reads them from
the facts).

| # | Step | Lookups | Stands for (SGK QSI step) | Outcome on the full store |
|---|---|---|---|---|
| 1 | `the run's tag (store_tag)` | `store_tag` get, `tag-north` | `resolve_run_selection (L1308)` | `ok [serial=…]` |
| 2 | `the frames (dial_setting, knob_setting)` | `dial_setting (3, 1)`, `knob_setting (7, 2)` | `build_model_list (L1313)` | `ok` |
| 3 | `[dial] gauge_setting x4` | gauges 4, 8, 10, 12 | `[LambdaCDM] tolerance x4` | `ok` |
| 4 | `[dial] Gadget` | `Gadget` get: `gadget-one`, the dial frame, `[tag-north]` | `[LambdaCDM] BackgroundModel` | `ok [available=True, serial=<facts Gadget>]` (asserted) |
| 5 | `[dial] read_table keypoint x2` | `read_table("keypoint", marked=True / False)` | `read_table wavenumber x2` | `ok [1 marked, 2 unmarked]` (asserted) |
| 6 | `[dial] keypoint_alias x3` | the three keypoints' aliases (offset 0.125, stepping 1) | `wavenumber_exit_time x6` | `ok [3 of 3 available]` (asserted) |
| 7 | `[dial] read_table dial_setting` | `read_table("dial_setting")` | `read_table redshift x2` | `ok [2 row(s)]` (asserted) |
| 8 | `[dial] routing_rule x2` | `rule-low`, `rule-high` | `GkSourcePolicy x2` | `ok [serials <facts routing_rule>]` (asserted) |
| 9 | `[dial] work item: object_read_batch Sample` | `object_read_batch("Sample", {"k": 0.5})` | `work item: object_read_batch QuadSourceIntegral` | `ok [2 row(s)]` |
| 10 | `[dial] work item: Sample, the stored row` | `Sample` get, `sample-run` | `work item: GkSourcePolicyData, the stored row's source` | `ok [available=True]` (asserted) |
| 11 | `[dial] work item: Sample, a miss` | `Sample` get, `sample-elsewhere` | `work item: GkSourcePolicyData, a miss` | `ok [available=False]` |
| 12 | `[knob] gauge_setting x4` | gauges 4, 8, 10, 12 | `[QCD_Cosmology] tolerance x4` | `ok` |
| 13 | `[knob] Gadget` | `Gadget` get: `gadget-two`, the knob frame, `[tag-north]` | `[QCD_Cosmology] BackgroundModel` | `raised RuntimeError: Could not locate suitable gadget instance in the datastore [available=False, serial=None]` (asserted by `assertIn`) |

SGK's steps `read_table QuadSourcePolicy`, `GkSource labels_only` and `QuadSource labels_only` have
no counterpart. **`other_sharded_lookups(pool, rec)`**: three `Sample` gets on the dial frame's work
item, each `ok [available=False]`: a code no Sample has; `sample-run` under no tag; the unvalidated
Sample (`build.UNVALIDATED_SAMPLE`, on keypoint 0.5, keyed on `gadget-two`'s serial from `FACTS`).
(`Tessera` is not used: its get inserts on a miss.)

**Measured from the scratchpad** (`run_reader.py`, outside `datastorekit/`) before the test module
used it, on a read-write and a read-only copy of the full store: the read-write run changed only
`store.sqlite`, entered `_replicated_write` 18 times with 0 rows inserted or updated, and stopped
with the sequence's own `RuntimeError`; the read-only run changed no file and entered it 0 times;
the 16 `(step, outcome)` pairs (13 + 3) were equal; `ray.is_initialized()` was `False`.

## 2. Deviations from the prompt

1. **Correction 1** (the orchestrator's): `table_counts` (`:139-146`) is transcribed with the
   instrument, reading through `standin_pool._read`, since `file_state` calls it. **STRUCTURALLY
   REQUIRED.**
2. **`Recorder.print`, `describe_delta` and `summarise_writes` are left out** (the note's choice):
   nothing calls them. **IMPLEMENTATION CHOICE.**
3. **Breakage (p)** (the orchestrator's addition): §6.1. The port keeps SGK's module aliases
   (`reconcile_at_open`, `prune_at_open`, `replicated_write`, `version_row_at_open`).
   **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
4. **The second vocabulary grep** (the orchestrator's addition): §5.5. **IMPLEMENTATION CHOICE**,
   at the orchestrator's direction.
5. **The two gauge gets of `TestNewStore.test_versioned_rows_carry_the_serial_on_every_shard` are
   kept** (the orchestrator's addition): `atol = build.get_gauge(self.pool, 10)`, `rtol =
   build.get_gauge(self.pool, 9)` (SGK's `1.0e-10`, `1.0e-9`), before the keypoint and the alias,
   where SGK's were; the alias (`build.make_alias(k, 1.0e6)`) takes neither, so the variables are
   unused. Under (e) this test fails in both its modules (§6.2). **IMPLEMENTATION CHOICE**, at the
   orchestrator's direction.
6. **`_load_probe` goes** (the orchestrator's addition): `rw = _load_probe()`, `REPO_ROOT`, `PROBE`
   and `_load_probe` become `from datastorekit.tests.client import reader as rw` (R-help), and
   `importlib.util` goes. **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
7. **The miss payloads are checked by column name.** `ReadOnlyMiss.payload` is the inserter's row:
   SGK's `payload["name"]`, `["log10_max_z"]`, `["log10_tol"]`, `["label"]` become
   `payload["dial_level"]`, `["knob_turns"]` and `["stepping"]` (the knob lambda's two assertions),
   `["gauge_exponent"]`, `["rule_label"]`. A literal port fails with `KeyError` inside the lambda.
   **STRUCTURALLY REQUIRED.**
8. **`test_object_validate` asks for the Gadget with the run's tag**, where SGK asked for its
   `BackgroundModel` with `tags=[]` (R-value): `Gadget_factory.build` serves only a stored Gadget
   whose tag set equals the one asked for, so `tags=[]` finds none and the test's
   `assertTrue(model.available)` fails. **STRUCTURALLY REQUIRED.**
9. **`reader.py` resolves references with `build.resolve`** (the stand-in's `ray.get`) and imports
   no `ray`, as `build.py` does (log 02 §2 item 5); the probe called `ray.get`. The transcribed
   instrument makes no such call. **IMPLEMENTATION CHOICE.**
10. **The split of the full store's writes.** §2.3 has `write_every_class` write at least two
    gauges and two rules, and §2.4 has `build_full_store` write what the sequence needs beyond it.
    `build_store` writes two gauges (4, 8) and the sequence's two rules; `build_full_store` adds the
    other two gauges (10, 12) and one run-tagged Sample, so that the full store, like SGK's, holds
    rows `build_store` does not. The aliases `build_store` writes are enough for the alias step.
    **IMPLEMENTATION CHOICE.**
11. **The sequence's design choices** within §2.4: one `read_table` of `dial_setting` (standing
    for SGK's `read_table redshift x2`); the run's tag `tag-north` so that the Gadget hit is
    `gadget-one`; the work item on the one marked keypoint; three other lookups, all of `Sample`
    (§1.6). **IMPLEMENTATION CHOICE.**
12. **The comment beside `assertEqual(len(rw_log), 18)`** says "enters _replicated_write 18 times"
    where SGK's said 21, R-count applied to the comment that states the literal; "(audit R2 Run 1)"
    stays as provenance. **IMPLEMENTATION CHOICE.**
13. **Comments describing the fixture, by R-map and R-value**: "the stop at `knob_setting`'s
    background" (was `QCD_Cosmology`'s); `test_a_new_shard_key`'s "a keypoint on every shard …
    keys against keypoints" (was wavenumbers); the backstop's "the store's position = 0.5 is a
    marked keypoint only; asking for it as a flagged keypoint too" (was "z = 1e5 is a source
    redshift only; … as a response redshift too"). `version_row_at_open`'s "on its keypoint's shard"
    (was wavenumber's), `TestInsertBeforeSetVersion`'s "routing_rule has a version column", and the
    timestamp module's "Gadget's tag table" (§2.6). **IMPLEMENTATION CHOICE.**
14. **The helpers of `TestOtherWritesRaiseReadOnlyWrite`**: `lcdm` → `dial_frame` (R-help: it
    returns the dial frame, and asserts nothing). `exit_time` reads the first marked keypoint
    and gets its alias by `objects.keypoint_alias` (as SGK passed its class); it keeps SGK's other
    gets — the frame and the two alias gauges — as hits, unpassed, with a comment saying so.
    `test_object_store_sharded_and_replicated` keeps `frame = self.dial_frame(pool)` and `tol =
    objects.SerialHandle(...)` (SGK's `lcdm`, `tol`) though `make_alias` takes neither; as 03a's
    deviation 8, the fixture's reads stay SGK's. **IMPLEMENTATION CHOICE.**
15. **Docstrings of the client, by addition**: the registry's role table gains two rows and its
    drop-group paragraph one sentence; the new classes, factories and helpers carry "added by prompt
    03b"; `compare_with_source.py`'s comment above `NO_SOURCE` names the neutral reader.
    **IMPLEMENTATION CHOICE.**
16. **`black` rewrote two `with a, b:` statements into the parenthesized form** (`quiet` in
    `test_version_row_at_open` and `test_read_only_pool`; the two `mock.patch.object` of
    `test_a_record_of_any_operation_is_refused_by_name_and_not_cleared`), as in 03a (its deviation 9).
    **STRUCTURALLY REQUIRED** (`CLAUDE.md`: format with `black`).
17. **SGK's layout in the ported modules' prose is unchanged** (`prompts/…`, `var/`,
    `Datastore.tests.standin_pool`, "audit R2", `resolve_run_selection`,
    `readonly_open_probe.py`), as 03a §2.1 says; counted in §7 item 1.

No UNINTENDED DRIFT was found.

## 3. The five hazards (§2.2)

1. **The ticking clock over 03a's classes.** `test_one_timestamp_per_write` runs 03a's 19 tests
   and the version-row eight under `_TickingDatetime`: `Ran 28 tests … OK`, alone and in the suite.
   Under (e) 19 of its 28 fail (§6.2), so the clock is read.
2. **The helpers that read `REPLICATED`.** `REPLICATED = reconcile_at_open.REPLICATED` is now 11
   tables (03a's 9 plus `gauge_setting` and `routing_rule`, both with a `timestamp` column).
   `_VersionTickingClock.tearDown` compares them whole on every shard, and `assertNoShardClock`
   reads their timestamps: `TestVersionRowOfANewStore.test_versioned_rows_carry_the_serial_on_every_shard`
   writes two gauges and two rules there and passes, and fails under (e).
3. **The order of the sequence.** Step 2 gets both frames before any frame's lookups; each frame's
   four gauges come before anything else that inserts on a miss; the rules come after only lookups
   that insert nothing (`Gadget`, aliases) and `read_table`s of classes not deleted. Each
   `TestEachMissRaisesReadOnlyMiss` test passes, its error naming the class, with payloads
   `{'dial_level': 3, 'stepping': 1}`, `{'knob_turns': 7, 'stepping': 2}`, `{'gauge_exponent':
   12}` and `{'rule_label': 'rule-high', 'rule_threshold': 5.0, 'rule_mode': 'prefer-direct'}`
   (read from (g)'s output).
4. **Nothing inserted on the read-write run.** Measured (§1.6): only `store.sqlite` changes, 18
   `_replicated_write` entries, none inserting or updating; no vectorized get of `Tessera` is in
   the sequence. The read-only run's outcomes equal it.
5. **`keypoint` is not deleted.** No miss test deletes a keypoint; `gauge_setting` plays
   `tolerance` (the reason for U13), and the shard-key class is reached only by the read-write
   `test_a_new_shard_key` and the backstop.

## 4. Verification performed

### 4.1 The suite (§3.1)

`./venv/bin/python -m unittest discover -s datastorekit/tests -t .`, in the foreground, output to
the scratchpad. **Before: `Ran 188 tests … OK`. After: `Ran 268 tests in 50.260s` / `OK`** = 188 +
80. Along the way: 188 OK after the two classes; 205 after the small modules; 245 after the version
row and the timestamp module; 268 after the read-only module. The 188 names of before are all
present after (the modules that held them are unedited, but for `test_neutral_client`'s two
literals). Python 3.12.15, `ray==2.43.0`, `SQLAlchemy==2.0.39`, `black==25.1.0`; no Ray process was
up at any point (`pgrep -lf 'gcs_server|raylet|ray::'` empty), and every store was in a `tempfile`
directory.

### 4.2 The loader's run counts (§2.5, §3.4)

`unittest.TestLoader().loadTestsFromName('datastorekit.tests.<module>').countTestCases()`:
`test_version_row_at_open` **12**, `test_read_only_pool` **23**, `test_one_timestamp_per_write`
**28**, `test_absolute_shard_record_refused` **12**, `test_closed_store_refusals` **5**.

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

OK: 8 module(s) keep their source's tests, classes and assertion skeletons
```

The five new modules' counts equal the orchestrator's measurement of SGK's (12/7/16/79, 23/5/27/138,
1/9/5/7, 12/3/14/28, 5/3/7/21); 03a's three are unchanged.

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
files ported, checked by compare_ported_tests.py: 8
files with no source, declared: 9
ported: checked by compare_ported_tests.py: datastorekit/tests/test_replicated_write.py (from Datastore/tests/test_replicated_write.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_reconcile_at_open.py (from Datastore/tests/test_reconcile_at_open.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_prune_at_open.py (from Datastore/tests/test_prune_at_open.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_version_row_at_open.py (from Datastore/tests/test_version_row_at_open.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_read_only_pool.py (from Datastore/tests/test_read_only_pool.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_one_timestamp_per_write.py (from Datastore/tests/test_one_timestamp_per_write.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_absolute_shard_record_refused.py (from Datastore/tests/test_absolute_shard_record_refused.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_closed_store_refusals.py (from Datastore/tests/test_closed_store_refusals.py)
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

Against its output before: the five `ported` lines, the counts (3 → 8 ported, 8 → 9 no-source) and
`reader.py`'s line. The table over the 31 compared files and its totals are unchanged.

### 4.5 The vocabulary (§3.5, and addition 2)

- **The 80 names** (log 02 §1.2's 82 less `version` and `store_tag`), `grep -nwE` over the five
  modules, `client/reader.py`, `build.py`, `objects.py`, `factories.py` and `registry.py`: **no
  match** (exit 1). The same grep over SGK's five matches 12, 55, 1, 0 and 0 lines, the note's
  figures.
- **The second grep**, `grep -nwE
  'CosmologyModels|CosmologyConcepts|ComputeTargets|extract_common|config\.[a-z_]+|Planck2018|DEFAULT_[A-Z_]*TOL[A-Z_]*|k_inv_Mpc|log10_tol|log10_max_z|Levin_threshold|numeric_policy|is_source|is_response'`
  over the five modules and `reader.py`: **no match** (exit 1); and `grep -nE '\bunits\s*='` over
  the same: **no match**. (`run_label_tag` is kept as the name of `reader.py`'s function, and
  `resolve_run_selection` stays in one ported comment, §2 item 17.)

### 4.6 `black` (§3.7)

`./venv/bin/black --check datastorekit docs/extraction` (25.1.0) → `50 files would be left
unchanged.`

## 5. The breakage method

Each diff below was made by editing the tree and taking `git diff` against the index (the work
staged), then restoring the file from the index. Each was checked with `git apply --check`, applied
with `git apply`, checked with `git apply -R --check`, run, and reverted with `git apply -R`, in
`bash` (`runbreak.sh` in the scratchpad). `git diff` and the untracked list were empty after each.
None is committed. The checks' breakages ran their check; the layer's ran the whole suite.

## 6. The deliberate-breakage record (§3.6)

### 6.1 The checks

**(a)** one `NAME_MAP` entry removed (`test_tolerance`) — `compare_ported_tests.py` exits **1**, naming the test:

```diff
diff --git a/docs/extraction/compare_ported_tests.py b/docs/extraction/compare_ported_tests.py
index 95f3ed6..744f244 100644
--- a/docs/extraction/compare_ported_tests.py
+++ b/docs/extraction/compare_ported_tests.py
@@ -97,7 +97,6 @@ NAME_MAP: Dict[str, Dict[str, str]] = {
     "datastorekit/tests/test_read_only_pool.py": {
         "test_LambdaCDM": "test_dial_setting",
         "test_QCD_Cosmology": "test_knob_setting",
-        "test_tolerance": "test_gauge_setting",
         "test_GkSourcePolicy": "test_routing_rule",
     },
 }
```
```
  DIFFERS  test missing from the package: TestEachMissRaisesReadOnlyMiss.test_tolerance
  DIFFERS  test not in the source: TestEachMissRaisesReadOnlyMiss.test_gauge_setting
  DIFFERS  TestEachMissRaisesReadOnlyMiss.test_tolerance: asserts in the source (2), missing from the package
  DIFFERS  TestEachMissRaisesReadOnlyMiss.test_gauge_setting: not in the source, and asserts (assert_miss, assertAlmostEqual)
FAIL: 1 of 8 module(s) differ from their source
```

**(b)** `_TickingClock` dropped from `TestRepairAtOpen`'s bases — exits **1**, naming the class:

```diff
diff --git a/datastorekit/tests/test_one_timestamp_per_write.py b/datastorekit/tests/test_one_timestamp_per_write.py
index 0c3ddf0..6f0aa66 100644
--- a/datastorekit/tests/test_one_timestamp_per_write.py
+++ b/datastorekit/tests/test_one_timestamp_per_write.py
@@ -87,7 +87,7 @@ class _TickingClock:
 # ------------------------------------------------------------------------------------------------
 
 
-class TestRepairAtOpen(_TickingClock, reconcile_at_open.TestKillAndReopen):
+class TestRepairAtOpen(reconcile_at_open.TestKillAndReopen):
     pass
 
 
```
```
  DIFFERS  class TestRepairAtOpen: bases ['reconcile_at_open.TestKillAndReopen'], the source's ['_TickingClock', 'reconcile_at_open.TestKillAndReopen']
FAIL: 1 of 8 module(s) differ from their source
```

**(c)** the `assertAlmostEqual` inside `test_knob_setting`'s payload lambda deleted — exits **1**, naming the test and the position:

```diff
diff --git a/datastorekit/tests/test_read_only_pool.py b/datastorekit/tests/test_read_only_pool.py
index 9ff807c..43a832b 100644
--- a/datastorekit/tests/test_read_only_pool.py
+++ b/datastorekit/tests/test_read_only_pool.py
@@ -390,7 +390,6 @@ class TestEachMissRaisesReadOnlyMiss(_ReadOnlyTestCase):
             "knob_setting",
             lambda payload: (
                 self.assertEqual(payload["knob_turns"], rw.KNOB_FRAME[0]),
-                self.assertAlmostEqual(payload["stepping"], rw.KNOB_FRAME[1]),
             ),
         )
         MESSAGES["knob_setting"] = str(e)
```
```
  DIFFERS  TestEachMissRaisesReadOnlyMiss.test_knob_setting: skeleton differs at position 3: the source has assertAlmostEqual, the package (nothing) (3 in the source, 2 in the package)
FAIL: 1 of 8 module(s) differ from their source
```

**(d)** `reader.py` removed from `NO_SOURCE` — `compare_with_source.py` exits **1**:

```diff
diff --git a/docs/extraction/compare_with_source.py b/docs/extraction/compare_with_source.py
index c7126ac..3245d23 100644
--- a/docs/extraction/compare_with_source.py
+++ b/docs/extraction/compare_with_source.py
@@ -180,7 +180,6 @@ NO_SOURCE = {
     "datastorekit/tests/client/build.py",
     "datastorekit/tests/test_neutral_client.py",
     "datastorekit/tests/test_shard_key_assignment.py",
-    "datastorekit/tests/client/reader.py",
 }
 
 # D-int: what each internalised module takes from its source.
```
```
not compared (NOT ACCOUNTED FOR): datastorekit/tests/client/reader.py
FAIL: 1 file(s) under datastorekit/ not accounted for
```

**(p)** `TestRepairAtOpen`'s base written by a direct import (addition 1) — exits **1**, naming the class:

```diff
diff --git a/datastorekit/tests/test_one_timestamp_per_write.py b/datastorekit/tests/test_one_timestamp_per_write.py
index 0c3ddf0..5e2a5ba 100644
--- a/datastorekit/tests/test_one_timestamp_per_write.py
+++ b/datastorekit/tests/test_one_timestamp_per_write.py
@@ -87,7 +87,10 @@ class _TickingClock:
 # ------------------------------------------------------------------------------------------------
 
 
-class TestRepairAtOpen(_TickingClock, reconcile_at_open.TestKillAndReopen):
+from datastorekit.tests.test_reconcile_at_open import TestKillAndReopen
+
+
+class TestRepairAtOpen(_TickingClock, TestKillAndReopen):
     pass
 
 
```
```
  DIFFERS  class TestRepairAtOpen: bases ['_TickingClock', 'TestKillAndReopen'], the source's ['_TickingClock', 'reconcile_at_open.TestKillAndReopen']
FAIL: 1 of 8 module(s) differ from their source
```

### 6.2 The layer, through the ported tests

"SGK" says whether the failing test's SGK counterpart pins the same line, by reading (SGK's code is
not run here; the package's layer is SGK's modulo D-imp).

**(e)** the replicated write's timestamp ignored by the actor (`SQL/Datastore.py:684`, after the read-only short-circuit at `:682-683`, which is left alone) — `Ran 268 tests` / `FAILED (failures=19, errors=120)`: 77 tests (139 failures and errors, counting subtests). In `test_one_timestamp_per_write`, **19 of its 28**: every `TestRepairAtOpen` test (12), both of `TestRepairThenPruneAtOpen`, both of `TestCompletionOfAnInterruptedPrune`, `TestPruneAtOpen.test_every_shard_identical_and_no_record_left` and `test_a_prune_with_nothing_to_prune_writes_nothing`, and `TestVersionRowOfANewStore.test_versioned_rows_carry_the_serial_on_every_shard`; the nine that pass write no timestamped replicated row (the version-row tests but one, and `test_the_set_of_classes_is_read_from_the_factories`). Each shard then stamps its own time, the shards' copies differ in `timestamp`, and the next open refuses (`ReplicatedDivergence`), or the test's own identity assertion fails. Every failing test, by module:

- `test_neutral_client`: `TestRoundTrip.test_a_reopen_passes_the_check_at_open_repairs_nothing_and_writes_nothing`, `TestRoundTrip.test_build_store_writes_every_class`, `TestRoundTrip.test_every_class_reads_back_through_a_reopened_pool`
- `test_one_timestamp_per_write`: `TestCompletionOfAnInterruptedPrune.test_faulted_after_each_shard`, `TestCompletionOfAnInterruptedPrune.test_faulted_before_the_first_shard`, `TestPruneAtOpen.test_a_prune_with_nothing_to_prune_writes_nothing`, `TestPruneAtOpen.test_every_shard_identical_and_no_record_left`, `TestRepairAtOpen.test_between_the_record_cleared_and_the_shard_key`, `TestRepairAtOpen.test_get_that_inserts_nothing`, `TestRepairAtOpen.test_scalar_get`, `TestRepairAtOpen.test_scalar_get_of_the_shard_key`, `TestRepairAtOpen.test_scalar_get_that_turns_a_flag_on`, `TestRepairAtOpen.test_store_of_a_background_model`, `TestRepairAtOpen.test_store_of_a_second_background_model_beside_the_first`, `TestRepairAtOpen.test_store_of_an_exit_time`, `TestRepairAtOpen.test_validate_of_a_background_model`, `TestRepairAtOpen.test_validate_whose_controller_counts_short`, `TestRepairAtOpen.test_vectorized_get`, `TestRepairAtOpen.test_vectorized_get_that_inserts_and_turns_a_flag_on`, `TestRepairThenPruneAtOpen.test_an_interrupted_store`, `TestRepairThenPruneAtOpen.test_an_interrupted_validate`, `TestVersionRowOfANewStore.test_versioned_rows_carry_the_serial_on_every_shard`
- `test_prune_at_open`: `TestInterruptedPrune.test_faulted_after_each_shard`, `TestInterruptedPrune.test_faulted_before_the_first_shard`, `TestNoActorDeletesAReplicatedRow.test_under_prune_unvalidated`, `TestPruneFailsInTheFactory.test_the_record_stays_and_the_next_open_completes_it`, `TestRecordsStayApart.test_a_get_record_of_a_background_model_is_repaired_not_pruned`, `TestRecordsStayApart.test_a_prune_record_over_a_difference_in_another_class_refuses`, `TestUninterruptedPrune.test_a_prune_with_nothing_to_prune_writes_nothing`, `TestUninterruptedPrune.test_every_shard_identical_and_no_record_left`
- `test_read_only_pool`: `TestAtOpen.test_an_absent_version_label_is_refused_naming_the_labels_present`, `TestAtOpen.test_every_connection_is_opened_read_only`, `TestEachMissRaisesReadOnlyMiss.test_dial_setting`, `TestEachMissRaisesReadOnlyMiss.test_gauge_setting`, `TestEachMissRaisesReadOnlyMiss.test_knob_setting`, `TestEachMissRaisesReadOnlyMiss.test_routing_rule`, `TestEachMissRaisesReadOnlyMiss.test_store_tag`, `TestNothingWrittenOnAFullStore.test_a_replicated_get_is_one_call_to_the_drawn_shard`, `TestNothingWrittenOnAFullStore.test_the_instrument_counts_a_read_write_pool_then_read_only_writes_nothing`, `TestOtherWritesRaiseReadOnlyWrite.test_a_new_shard_key`, `TestOtherWritesRaiseReadOnlyWrite.test_a_vectorized_get_that_reaches_an_inserter`, `TestOtherWritesRaiseReadOnlyWrite.test_object_store_sharded_and_replicated`, `TestOtherWritesRaiseReadOnlyWrite.test_object_validate`, `TestOtherWritesRaiseReadOnlyWrite.test_the_actors_refuse_store_and_validate_themselves`, `TestOtherWritesRaiseReadOnlyWrite.test_the_backstop_a_flag_update_on_a_hit`
- `test_reconcile_at_open`: `TestCleanStoreUntouched.test_opening_a_clean_store_writes_nothing`, `TestHotJournal.test_a_hot_journal_on_one_shard_is_rolled_back_then_compared`, `TestHotJournal.test_a_hot_journal_on_the_primary_is_rolled_back_before_the_record_is_read`, `TestKillAndReopen.test_between_the_record_cleared_and_the_shard_key`, `TestKillAndReopen.test_get_that_inserts_nothing`, `TestKillAndReopen.test_scalar_get`, `TestKillAndReopen.test_scalar_get_of_the_shard_key`, `TestKillAndReopen.test_scalar_get_that_turns_a_flag_on`, `TestKillAndReopen.test_store_of_a_background_model`, `TestKillAndReopen.test_store_of_a_second_background_model_beside_the_first`, `TestKillAndReopen.test_store_of_an_exit_time`, `TestKillAndReopen.test_validate_of_a_background_model`, `TestKillAndReopen.test_validate_whose_controller_counts_short`, `TestKillAndReopen.test_vectorized_get`, `TestKillAndReopen.test_vectorized_get_that_inserts_and_turns_a_flag_on`, `TestNoRecordRefuses.test_a_difference_in_a_sharded_table_is_not_looked_at`, `TestNoRecordRefuses.test_a_flag`, `TestNoRecordRefuses.test_a_missing_row`, `TestNoRecordRefuses.test_a_timestamp_difference`, `TestNoRecordRefuses.test_a_value_count_difference`, `TestNoRecordRefuses.test_a_value_row_held_under_another_serial`, `TestPruningAfterRepair.test_an_interrupted_store`, `TestPruningAfterRepair.test_an_interrupted_validate`, `TestRecordDoesNotExplain.test_a_shard_key_the_repair_does_not_supply`, `TestRecordDoesNotExplain.test_part_of_the_recorded_background_model`
- `test_replicated_write`: `TestCleanWrite.test_every_copy_is_row_identical`, `TestShardedWritesUnchanged.test_a_replicated_row_does_not_take_the_shards_time`, `TestWriteOverASetRecord.test_a_reopened_pool_repairs_from_the_controller_and_the_write_succeeds`
- `test_shard_key_assignment`: `TestShardKeysAssignedOutOfSerialOrder.test_every_sample_is_on_the_shard_the_reopened_map_names`, `TestShardKeysAssignedOutOfSerialOrder.test_the_keys_were_assigned_out_of_serial_order`, `TestShardKeysAssignedOutOfSerialOrder.test_the_saved_map_is_the_map_in_memory_and_the_reopened_map`
- `test_version_row_at_open`: `TestNewStore.test_versioned_rows_carry_the_serial_on_every_shard`

SGK: the same `test_one_timestamp_per_write` classes run the same tests over the same line (by reading).

```diff
diff --git a/datastorekit/SQL/Datastore.py b/datastorekit/SQL/Datastore.py
index 83f33ea..10a0849 100644
--- a/datastorekit/SQL/Datastore.py
+++ b/datastorekit/SQL/Datastore.py
@@ -681,7 +681,7 @@ class Datastore:
         # a read-only actor's inserters all refuse, whatever the timestamp (prompt 03)
         if getattr(self, "_read_only", False):
             return self._inserters
-        if insert_timestamp is None:
+        if True:
             return self._inserters
 
         return {
```

**(f)** the refusal of an insert before `set_version` removed (`SQL/Datastore.py:718`) — `Ran 268 tests` / `FAILED (failures=1)`: `test_version_row_at_open.TestInsertBeforeSetVersion.test_a_versioned_insert_raises_names_the_class_and_writes_nothing` (`AssertionError: RuntimeError not raised`). SGK: the same test pins it.

```diff
diff --git a/datastorekit/SQL/Datastore.py b/datastorekit/SQL/Datastore.py
index 83f33ea..ff2b2dc 100644
--- a/datastorekit/SQL/Datastore.py
+++ b/datastorekit/SQL/Datastore.py
@@ -715,7 +715,7 @@ class Datastore:
         # a row that carries a version serial cannot be written before the pool has set it
         # (set_version). Refused here, before the serial lease below, so that a refused insert
         # takes no serial from the broker and writes nothing
-        if uses_version and self._version_serial is None:
+        if False:
             raise RuntimeError(
                 f'Datastore "{self._my_name}": cannot insert into "{cls_name}" before the version '
                 f"serial is set: ShardedPool calls set_version once the version row of label "
```

**(g)** a read-only actor's miss of a replicated class raised as `ReadOnlyWrite` (`SQL/Datastore.py:278-279`) — `Ran 268 tests` / `FAILED (errors=5)`: every test of `test_read_only_pool.TestEachMissRaisesReadOnlyMiss` (`test_store_tag`, `test_dial_setting`, `test_knob_setting`, `test_gauge_setting`, `test_routing_rule`), each raising `ReadOnlyWrite: … an insert of "<class>" would write to it (payload {…})` where `ReadOnlyMiss` was expected. SGK: the same five tests (its four under their SGK names) pin it.

```diff
diff --git a/datastorekit/SQL/Datastore.py b/datastorekit/SQL/Datastore.py
index 83f33ea..2c609f6 100644
--- a/datastorekit/SQL/Datastore.py
+++ b/datastorekit/SQL/Datastore.py
@@ -275,7 +275,7 @@ class Datastore:
         ``ReadOnlyWrite``.
         """
         cls_name = schema["name"]
-        if cls_name in self._replicated_tables:
+        if False:
             raise ReadOnlyMiss(cls_name, dict(payload), store=self._my_name)
         raise ReadOnlyWrite(
             self._my_name,
```

**(h)** `resolve_shard_path` accepting an absolute record, `_require_bare_name` bypassed for one (`shard_paths.py:101`) — `Ran 268 tests` / `FAILED (failures=20, errors=1)`: in `test_absolute_shard_record_refused`, **10 of its 12** (`TestTheResolver.test_resolve_shard_path_refuses_an_absolute_record`, six subtests; every `TestEveryReader` test but the control `test_the_store_it_names_is_not_refused`, `test_the_read_only_reader` as an error); the two controls pass. Also 01's `test_shard_paths.TestResolveShardPath.test_refused_records` (four subtests) and `test_shard_key_audit_refusals.TestTheAuditRefuses.test_a_primary_naming_another_stores_shards_by_absolute_path` and `…_its_own_siblings_by_absolute_path`. SGK: the same tests pin it.

```diff
diff --git a/datastorekit/shard_paths.py b/datastorekit/shard_paths.py
index c5354a8..e019acc 100644
--- a/datastorekit/shard_paths.py
+++ b/datastorekit/shard_paths.py
@@ -98,7 +98,11 @@ def resolve_shard_path(primary: Union[str, Path], stored: str) -> Path:
             f"shard record {stored!r} is not a string (type {type(stored).__name__})"
         )
 
-    name = _require_bare_name(stored, stored)
+    name = (
+        Path(stored).name
+        if Path(stored).is_absolute()
+        else _require_bare_name(stored, stored)
+    )
 
     return primary.parent / name
 
```

**(i)** `delete_store`'s refusal stating its prefix twice (`SQL/ShardedPool.py:2932`) — `Ran 268 tests` / `FAILED (failures=2)`: `test_closed_store_refusals.TestEachPrefixOnce.test_delete_and_closed_store_files_state_their_prefix_once` and `test_an_unreadable_shards_table_is_named_once_by_each` (`operation='delete_store'`), each `2 != 1`. SGK: the same two tests pin it.

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 8d1fd81..83004e7 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -2929,7 +2929,7 @@ class ShardedPool:
 
         def refuse(reason: str) -> RuntimeError:
             return RuntimeError(
-                f'Cannot delete sharded datastore "{str(given)}": {reason}. Nothing was deleted'
+                f'Cannot delete sharded datastore "{str(given)}": Cannot delete sharded datastore "{str(given)}": {reason}. Nothing was deleted'
             )
 
         # the primary: an existing regular file, not a symbolic link (the same test as a shard, as
```

**(j)** `?mode=ro` dropped from `_find_version_row`'s connection (`SQL/ShardedPool.py:378`; the read-only open reaches it through `_find_version_row`, so this is the prompt's first choice) — `Ran 268 tests` / `FAILED (failures=1)`: `test_read_only_pool.TestAtOpen.test_every_connection_is_opened_read_only` (`False is not true : ('file:///…/copy-1/store-shard0000.sqlite',)`). SGK: the same test pins the same line.

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 8d1fd81..cbcf8dc 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -375,7 +375,7 @@ class ShardedPool:
         """
         found = {}
         for sid, path in sorted(self._shard_db_files.items()):
-            conn = sqlite3.connect(f"{Path(path).as_uri()}?mode=ro", uri=True)
+            conn = sqlite3.connect(f"{Path(path).as_uri()}", uri=True)
             try:
                 rows = conn.execute(
                     f'SELECT serial, "{VERSION_LABEL}" FROM "{VERSION_TABLE}" '
```

No breakage failed nothing; no issue is opened for one.

## 7. Observations not acted on

1. **`[01-package-prose-names-sgks-layout]`, re-measured** by log 03a §8's method (the script in
   the scratchpad, `prose_count.py`): **114 lines in 23 files at `72cf34a`** (reproduced; the same
   method gives 01's 101/102 and 02's 104 at `8bc60a5` and `e988e69`), and **124 lines in 28 files
   after this prompt**. The five modules add 10, all SGK's prose ported unchanged:
   `test_read_only_pool.py` 5 (`:2`, `:5`, `:29`, `:71`, `:816`), `test_version_row_at_open.py` 2
   (`:2`, `:10`), `test_absolute_shard_record_refused.py` 1 (`:4`), `test_closed_store_refusals.py` 1
   (`:3`), `test_one_timestamp_per_write.py` 1 (`:3`); `reader.py` and the client add none (the
   rewritten docstring of §1.3 drops one probe path SGK's had). Their SGK references outside the
   pattern: `var/` (`test_version_row_at_open.py:27`, `test_read_only_pool.py:6`,
   `test_one_timestamp_per_write.py:28`, `test_absolute_shard_record_refused.py:28`,
   `test_closed_store_refusals.py:18`); "audit V1"/"audit R1"/"audit R2"
   (`test_version_row_at_open.py:14`, `:290`; `test_read_only_pool.py:19`, `:240`, `:273-274`,
   `:358`, `:625`); `resolve_run_selection` (`test_read_only_pool.py:357`); "QSI"
   (`test_read_only_pool.py:18`, `:213`); SGK's commit `b04671f` and "the A3 baseline store"
   (`test_absolute_shard_record_refused.py:9`, `:26`). The issue's measurement and hook are updated.
2. **(e) breaks far beyond its module**: 77 tests in nine modules, including all of
   `test_read_only_pool` that open the full store (each shard then stamps its own time, the full
   store's shards differ, and the read-only open refuses). Expected, and recorded.
3. **Serials of the full store vary between builds** (e.g. `routing_rule` `(1, 501)`), since the
   stand-in pool draws the controlling shard at random and leases serials in batches. The test reads
   every serial from the facts, as SGK's did ("stand-in serials vary between builds").
4. **`factories.py`'s module docstring** lists the leaves (`version`, …, `Tessera`) without the two
   new ones, and `client/__init__.py` names no class; left, since the client changes by addition
   only. **`compare_ported_tests.py`'s docstring** still says `NAME_MAP` "is empty for prompt 03a's
   modules", which stays true; left, since §2.5 changes nothing else there.
5. **`test_read_only_pool` keeps unused variables** in `exit_time` (`frame`, `atol`, `rtol`) and in
   `test_object_store_sharded_and_replicated` (`frame`, `tol`), the counterparts of SGK's arguments
   the alias does not take (§2 item 14).

## 8. Issues

- **Changed:** `[01-package-prose-names-sgks-layout]`: 114 → 124 lines, 23 → 28 files (§7 item 1).
- **Opened, closed:** none. Every breakage failed a test.

The index is at **6 open**: 2 on this board, 4 inherited.

## 9. State handed to the next prompt

- `HEAD` is `0d5380c`. The tree is clean; `venv/` unchanged.
- The suite: **268** (`Ran 268 tests … OK`). 04 records 268 as its "before".
- `compare_ported_tests.py` exits 0 over eight modules, with U12's four renames in `NAME_MAP`;
  `compare_with_source.py` exits 0 over 31 compared, 8 `PORTED`, 9 with no source (48 `.py` files
  under `datastorekit/`). 04 extends `PORTED` and `FILES` the same way.
- The interfaces of README §4 "After 03b": `gauge_setting` and `routing_rule`, with
  `build.get_gauge`, `build.get_rule`, `GAUGE_EXPONENTS`, `ROUTING_RULES`; `client/reader.py`
  (`build_full_store`, `reader_sequence`, `other_sharded_lookups`, the instrument and constants).
- For 04: `build_store` now writes 16 classes' worth of rows in 15 tables (two more gauges and rules);
  `test_neutral_client`'s `KEPT` and `counts` show it. Any 04 test that counts a whole store's
  tables or rows counts them.
