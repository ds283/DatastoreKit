# Log 03a — port the replicated-write tests

**Subject:** Port the replicated-write, check-at-open and prune-at-open tests · **Commit:**
`11247c7` · **Date:** 2026-10-07 · **Model:** Claude Opus 5.5 · **Result:** landed. SGK's
`test_replicated_write` (25), `test_reconcile_at_open` (41) and `test_prune_at_open` (10) run in
`datastorekit/tests/` under their names, on the stand-in pool and the neutral client;
`docs/extraction/compare_ported_tests.py` finds their tests, classes and assertion skeletons equal
to SGK's; `compare_with_source.py` accounts for them as `PORTED`; the new
`test_shard_key_assignment` pins `_assign_shard_keys` against the `key_id` binding, and a ported
test reaches `revalidate`. `Ran 188 tests … OK` (109 before).
`[02-no-test-reaches-revalidate]` and `[01-no-ported-test-pins-the-shard-key-assignment]` are
closed; the index is at 6.

Prompt: [`../03a-port-the-replicated-write-tests.md`](../03a-port-the-replicated-write-tests.md),
with the orchestrator's dispatch note (two corrections and two additions, followed as given).

## 1. What shipped

- **Three ported modules** (§2.3), each SGK's at `6f7f291` with the changes of §2.1 only:
  `datastorekit/tests/test_replicated_write.py`, `test_reconcile_at_open.py`,
  `test_prune_at_open.py`. Every test class and method keeps its name (no R-name; prompt §2.1).
- **One new module**, `datastorekit/tests/test_shard_key_assignment.py` (§2.5): three tests, §4.
- **`datastorekit/tests/client/build.py`, by addition only**: one import name (`SerialHandle`)
  added to its existing import from `objects`, and two helpers and two constants appended (§1.4).
  Nothing else in `tests/client/`, and not `standin_pool.py`, changed.
- **`docs/extraction/compare_ported_tests.py`** (new, U9): §1.5.
- **`docs/extraction/compare_with_source.py`**: the `PORTED` kind, the three modules as `PORTED`,
  the new module in `NO_SOURCE`, and its docstring (§1.6).
- **The records**: this log; the board (header, §1's row, §3, §4); `docs/OPEN_ISSUES.md`;
  `prompts/INDEX.md`.

### 1.1 The map as used (§2.2)

Each row is the planner's unless it says otherwise. Columns and payload keys move with their
table (R-map); values by R-value.

| SGK | Used for | Neutral, as used | Changed from the planner's row? |
|---|---|---|---|
| `tolerance` (`log10_tol`; payload `tol`) | a replicated leaf a scalar get inserts | `dial_setting` (`dial_level`; payload `level`), `build.get_dial`. R-value: `tol=1.0e-N` → `level=N` (1e-10 → 10, 1e-9 → 9, 1e-6 → 6, 1e-4 → 4), so `log10_tol = -6.0` → `dial_level = 6`, and equal and different values stay so | no |
| `redshift` (`z`; flags `source`, `response`; payload `is_source`, `is_response`) | a replicated leaf a vectorized get inserts, with monotone flags | `keypoint` (`kp_position`, `kp_marked`, `kp_flagged`; payload `position`, `marked`, `flagged`), `build.get_keypoints(..., marked=True)` (SGK's `get_redshifts` passes `is_source=True`) | no |
| `wavenumber` (`k_inv_Mpc`) | the shard-key class | `keypoint`, `build.get_keypoint(..., marked=True)` (SGK's `get_wavenumber` passes `is_source=True`) | no |
| `wavenumber_exit_time` (`z_exit`; attribute `k`) | a stored replicated proxy of the shard key | `keypoint_alias` (`ka_offset`; attribute `keypoint`, so `exit_time.k.store_id` → `exit_time.keypoint.store_id`), `build.make_alias` and `object_store` | no |
| `IntegrationSolver` (got by `make_background_model`); `LambdaCDM`/`QCD_Cosmology` (SGK's `StandinCosmology`, never stored) | the replicated parents a model is written on | **`knob_setting` only**, got through the pool as the Gadget's `frame` (`build.make_framed_gadget`) | **yes**: `dial_setting` already plays `tolerance`, so the frame is a `knob_setting`, and a frame row never coincides with a tolerance row (e.g. `max(serial) FROM dial_setting` in `test_a_prune_record_over_a_difference_in_another_class_refuses` is still the second tolerance's). SGK's cosmology is not stored, so nothing stands for it |
| `BackgroundModel` (`validated`; `model.values`; `_label`) | the replicated owner | `Gadget` (`gadget_validated`; `model.parts`; `label`), **`build.make_framed_gadget`** and `object_store` (not `store_gadget`: SGK stores and validates in separate steps) | **yes**: a new helper, since `make_background_model` gets its parents (redshifts, solver) through the pool and `make_gadget` gets nothing (§1.4) |
| `BackgroundModel_tags` (`model_serial`, `tag_serial`) | its tag table | `Gadget_tags` (`gadget_serial`, `tag_serial`) | no |
| `BackgroundModelValue` (`model_serial`; `_Hubble`) | its owned value table | `GadgetPart` (`gadget_serial`; `part_value`); in one docstring the value row's parent `redshift` → `part_index` (its identity within the owner) | no |
| `GkSourcePolicy` | a replicated class a get inserts, dropped by a drop action | `keypoint_alias`, `build.get_alias(pool, build.get_keypoint(pool, 0.5, marked=True), 1.5)` | no (the alias needs a keypoint, got first) |
| `GkSourcePolicyData` (`quality`) | a sharded class, stored | `Sample` (`sample_code`), **`build.make_sample_on(alias)`** with `store_sample` (validated: correction 2, and §2 item 6) or a bare `object_store` (correction 2's two tests) | **yes**: a new helper, the counterpart of `sp.make_policy_data(exit_time)`; its Gadget is an `objects.SerialHandle(1)`, as SGK's policy data takes `StandinSerial` handles (correction 2) |
| `GkSource`, `TkNumericIntegration` | sharded classes that prune at startup, in the actor | `Sample` | no |
| drop actions `gk-source`, `gk-source-policy-records`, `gk-source-policy`, `quad-source-integral` | a drop of a replicated table with its dependents | `samples`, `aliases`, `tesserae` (in that order: `gk-source` → `samples`, `gk-source-policy-records` → `aliases`, the last two → `tesserae`) | no; the list has 3 entries where SGK's has 4 |
| `sp.make_units`, `sp.StandinCosmology` (`self.units`, `self.cosmology` in each `setUp`) | SGK's units and cosmology | removed from each `setUp` | no |

`version` and `store_tag` keep their names. The base classes' helpers keep their names
(`exit_time`, `background`, `stored_background`, `store_model`, `build`, `tags`, `serials`, …), with
their parameters renamed by the map (`k_inv_Mpc` → `position`, `z_exit` → `offset`, `zs` →
`positions`): none of those names is a client's table identifier, and keeping them keeps the
tests' text. The helper `TestRecordDoesNotExplain.interrupted_tolerance_get` asserts, so it keeps
its name (§2.1, R-help); `tolerance` is part of a longer identifier there, not a whole word.

### 1.2 The three modules' constants

- **`REPLICATED`** (correction 1): in each module,
  `[t for t in replicated_tables if factories[t].register() is not None] + ["Gadget_tags"]`, the
  registry filtered, not an explicit list. It names the 9 tables the check at open compares, in
  its order: `version`, `store_tag`, `keypoint`, `keypoint_alias`, `dial_setting`,
  `knob_setting`, `Gadget`, `GadgetPart`, `Gadget_tags`. R-count.
- `UNIT = ("Gadget", "Gadget_tags", "GadgetPart")` (prune) and
  `KEYS = {"Gadget_tags": ("gadget_serial", "tag_serial")}` (reconcile): R-map.
- `quiet`, `execute`, `SimulatedDeath`, `_TickingDatetime`, `FIXED_NOW`, `_FixedDatetime`,
  `standin_copy`, `tearDownModule`: unchanged (but for `black`, §2 item 9).

### 1.3 The port table (§4.4)

One row per ported test. The package's module, class and method are the SGK origin's, in every
row (no R-name). "Kinds in the test" are the kinds of change inside the test method itself,
measured by a token diff of the method against SGK's (every changed token is one of them, or
`black`'s re-wrapping; nothing else). Every test also runs under its module's changes: R-imp (the
imports), R-help (each `setUp` without `units`/`cosmology`; the base helpers in the "Fixture"
column, rewritten on the neutral client), R-map (`UNIT`, `KEYS`, and the helpers' SQL) and R-count
(`REPLICATED`, correction 1). The classes column lists the SGK classes the test uses, directly or
through its fixture, with their neutral counterparts.

| # | SGK origin (module · class · method) | Kinds in the test | Fixture it uses (R-help) | SGK classes → neutral | Note |
|---|---|---|---|---|---|
| 1 | `test_replicated_write` · `TestCleanWrite` · `test_every_copy_is_row_identical` | R-help, R-map, R-value | `setUp`, `exit_time`, `stored_background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` | hazard 2: `written` holds `keypoint` once for SGK's `redshift` and `wavenumber` (9 names → 8) |
| 2 | `test_replicated_write` · `TestCleanWrite` · `test_a_get_that_inserts_nothing_replicates_nothing` | R-help, R-value | `setUp` | `tolerance`→`dial_setting` |  |
| 3 | `test_replicated_write` · `TestRecordAcrossTheWindow` · `test_scalar_get` | R-help, R-map, R-value | `setUp` | `tolerance`→`dial_setting` |  |
| 4 | `test_replicated_write` · `TestRecordAcrossTheWindow` · `test_vectorized_get` | R-help, R-map | `setUp` | `redshift`→`keypoint` |  |
| 5 | `test_replicated_write` · `TestRecordAcrossTheWindow` · `test_store_of_an_exit_time` | R-map | `setUp`, `exit_time` | `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 6 | `test_replicated_write` · `TestRecordAcrossTheWindow` · `test_store_of_a_background_model` | R-map | `setUp`, `background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint` |  |
| 7 | `test_replicated_write` · `TestRecordAcrossTheWindow` · `test_validate_of_a_background_model` | R-map | `setUp`, `stored_background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint` |  |
| 8 | `test_replicated_write` · `TestRecordAcrossTheWindow` · `test_a_controller_that_dies_after_its_commit_leaves_the_record` | R-help, R-map, R-value | `setUp`, `exit_time`, `background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 9 | `test_replicated_write` · `TestRecordAcrossTheWindow` · `test_the_record_is_on_disk_during_every_shards_call` | R-help, R-map, R-value | `setUp`, `exit_time`, `background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 10 | `test_replicated_write` · `TestReplicaSerialMismatch` · `test_scalar_get` | R-help, R-map, R-value | `setUp` | `tolerance`→`dial_setting` |  |
| 11 | `test_replicated_write` · `TestReplicaSerialMismatch` · `test_vectorized_get` | R-help, R-map | `setUp` | `redshift`→`keypoint` |  |
| 12 | `test_replicated_write` · `TestReplicaSerialMismatch` · `test_store_over_a_replica_holding_the_key_under_another_serial` | R-map | `setUp`, `exit_time` | `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 13 | `test_replicated_write` · `TestReplicaSerialMismatch` · `test_the_exception_pickles_with_its_fields` | R-map | `setUp` | `tolerance`→`dial_setting` |  |
| 14 | `test_replicated_write` · `TestIdempotentReplicaStores` · `test_exit_time_replay_writes_nothing_and_returns_the_row` | — | `setUp`, `exit_time` | `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 15 | `test_replicated_write` · `TestIdempotentReplicaStores` · `test_exit_time_differing_row_raises` | R-map | `setUp`, `exit_time` | `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 16 | `test_replicated_write` · `TestIdempotentReplicaStores` · `test_exit_time_key_under_another_serial_raises` | — | `setUp`, `exit_time` | `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 17 | `test_replicated_write` · `TestIdempotentReplicaStores` · `test_background_replay_writes_nothing_and_returns_the_row` | R-map | `setUp`, `stored_background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint` |  |
| 18 | `test_replicated_write` · `TestIdempotentReplicaStores` · `test_background_differing_row_raises` | R-map | `setUp`, `stored_background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint` |  |
| 19 | `test_replicated_write` · `TestIdempotentReplicaStores` · `test_background_key_under_another_serial_raises` | R-map | `setUp`, `background`, `stored_background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint` |  |
| 20 | `test_replicated_write` · `TestIdempotentReplicaStores` · `test_background_unvalidated_row_of_the_same_key_does_not_block` | R-map | `setUp`, `background`, `stored_background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint` |  |
| 21 | `test_replicated_write` · `TestWriteOverASetRecord` · `test_every_path_refuses` | R-help, R-value | `setUp`, `TestWriteOverASetRecord.setUp` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 22 | `test_replicated_write` · `TestWriteOverASetRecord` · `test_a_reopened_pool_repairs_from_the_controller_and_the_write_succeeds` | R-help, R-map, R-value | `setUp`, `TestWriteOverASetRecord.setUp` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 23 | `test_replicated_write` · `TestWriteOverASetRecord` · `test_overlapping_writes_are_a_programming_error` | R-help, R-value | `setUp`, `TestWriteOverASetRecord.setUp` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 24 | `test_replicated_write` · `TestShardedWritesUnchanged` · `test_a_sharded_store_stamps_its_own_time_and_writes_no_record` | R-help, R-map | `setUp`, `exit_time` | `GkSourcePolicyData`→`Sample`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` | correction 2: bare `object_store` of the Sample kept |
| 25 | `test_replicated_write` · `TestShardedWritesUnchanged` · `test_a_replicated_row_does_not_take_the_shards_time` | R-help, R-map, R-value | `setUp` | `tolerance`→`dial_setting` |  |
| 26 | `test_reconcile_at_open` · `TestKillAndReopen` · `test_scalar_get` | R-help, R-map, R-value | `setUp` | `tolerance`→`dial_setting` |  |
| 27 | `test_reconcile_at_open` · `TestKillAndReopen` · `test_scalar_get_of_the_shard_key` | R-help, R-map | `setUp` | `wavenumber`→`keypoint` |  |
| 28 | `test_reconcile_at_open` · `TestKillAndReopen` · `test_scalar_get_that_turns_a_flag_on` | R-help, R-map | `setUp` | `wavenumber`→`keypoint` |  |
| 29 | `test_reconcile_at_open` · `TestKillAndReopen` · `test_vectorized_get` | R-help, R-map | `setUp` | `redshift`→`keypoint` |  |
| 30 | `test_reconcile_at_open` · `TestKillAndReopen` · `test_vectorized_get_that_inserts_and_turns_a_flag_on` | R-help, R-map | `setUp` | `redshift`→`keypoint` |  |
| 31 | `test_reconcile_at_open` · `TestKillAndReopen` · `test_get_that_inserts_nothing` | R-help, R-map, R-value | `setUp` | `tolerance`→`dial_setting` |  |
| 32 | `test_reconcile_at_open` · `TestKillAndReopen` · `test_store_of_an_exit_time` | R-map | `setUp`, `exit_time` | `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 33 | `test_reconcile_at_open` · `TestKillAndReopen` · `test_store_of_a_background_model` | R-map | `setUp`, `background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint` |  |
| 34 | `test_reconcile_at_open` · `TestKillAndReopen` · `test_store_of_a_second_background_model_beside_the_first` | R-map | `setUp`, `background`, `stored_background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint` |  |
| 35 | `test_reconcile_at_open` · `TestKillAndReopen` · `test_validate_of_a_background_model` | R-map | `setUp`, `stored_background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint` | reaches `Gadget_factory.revalidate`; fails under (i) |
| 36 | `test_reconcile_at_open` · `TestKillAndReopen` · `test_validate_whose_controller_counts_short` | R-map | `setUp`, `stored_background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint` |  |
| 37 | `test_reconcile_at_open` · `TestKillAndReopen` · `test_between_the_record_cleared_and_the_shard_key` | R-help, R-map | `setUp` | `wavenumber`→`keypoint` | hazard 1: the one checksum window spanning a get of the shard-key class (as in SGK) |
| 38 | `test_reconcile_at_open` · `TestSerialSplit` · `test_with_the_record_set` | — | `setUp`, `TestSerialSplit.setUp` | `tolerance`→`dial_setting` |  |
| 39 | `test_reconcile_at_open` · `TestSerialSplit` · `test_with_no_record` | — | `setUp`, `TestSerialSplit.setUp` | `tolerance`→`dial_setting` |  |
| 40 | `test_reconcile_at_open` · `TestSerialSplit` · `test_the_refusal_pickles_with_its_fields` | — | `setUp`, `TestSerialSplit.setUp` | `tolerance`→`dial_setting` |  |
| 41 | `test_reconcile_at_open` · `TestMismatchLeftByTheCheck` · `test_a_vectorized_get` | R-help, R-map | `setUp` | `redshift`→`keypoint` |  |
| 42 | `test_reconcile_at_open` · `TestMismatchLeftByTheCheck` · `test_a_store` | R-map | `setUp`, `exit_time` | `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 43 | `test_reconcile_at_open` · `TestMismatchLeftByTheCheck` · `test_a_validate` | R-map | `setUp`, `stored_background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint` |  |
| 44 | `test_reconcile_at_open` · `TestNoRecordRefuses` · `test_a_missing_row` | R-map | `setUp`, `TestNoRecordRefuses.setUp` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 45 | `test_reconcile_at_open` · `TestNoRecordRefuses` · `test_an_extra_row` | R-map | `setUp`, `TestNoRecordRefuses.setUp` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 46 | `test_reconcile_at_open` · `TestNoRecordRefuses` · `test_a_flag` | R-map | `setUp`, `TestNoRecordRefuses.setUp` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 47 | `test_reconcile_at_open` · `TestNoRecordRefuses` · `test_a_validated_difference` | R-map | `setUp`, `TestNoRecordRefuses.setUp` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 48 | `test_reconcile_at_open` · `TestNoRecordRefuses` · `test_a_value_count_difference` | R-map | `setUp`, `TestNoRecordRefuses.setUp` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 49 | `test_reconcile_at_open` · `TestNoRecordRefuses` · `test_a_timestamp_difference` | R-map | `setUp`, `TestNoRecordRefuses.setUp` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 50 | `test_reconcile_at_open` · `TestNoRecordRefuses` · `test_a_value_row_held_under_another_serial` | R-map | `setUp`, `TestNoRecordRefuses.setUp` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` | docstring's `redshift` (the value row's parent) → `part_index` |
| 51 | `test_reconcile_at_open` · `TestNoRecordRefuses` · `test_a_primary_without_the_record_table_is_refused` | — | `setUp`, `TestNoRecordRefuses.setUp` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 52 | `test_reconcile_at_open` · `TestNoRecordRefuses` · `test_a_difference_in_a_sharded_table_is_not_looked_at` | R-help, R-map | `setUp`, `TestNoRecordRefuses.setUp` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `GkSourcePolicyData`→`Sample`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` | correction 2: bare `object_store` of the Sample kept |
| 53 | `test_reconcile_at_open` · `TestRecordDoesNotExplain` · `test_a_row_the_controller_lacks` | R-map | `setUp`, `TestRecordDoesNotExplain.interrupted_tolerance_get` | `tolerance`→`dial_setting` |  |
| 54 | `test_reconcile_at_open` · `TestRecordDoesNotExplain` · `test_a_record_naming_another_class` | R-help, R-map | `setUp`, `TestRecordDoesNotExplain.interrupted_tolerance_get` | `redshift`→`keypoint`, `tolerance`→`dial_setting` |  |
| 55 | `test_reconcile_at_open` · `TestRecordDoesNotExplain` · `test_a_row_the_recorded_write_did_not_insert` | R-help, R-map, R-value | `setUp`, `TestRecordDoesNotExplain.interrupted_tolerance_get` | `tolerance`→`dial_setting` |  |
| 56 | `test_reconcile_at_open` · `TestRecordDoesNotExplain` · `test_a_flag_the_controller_lacks` | R-help, R-map | `setUp`, `TestRecordDoesNotExplain.interrupted_tolerance_get` | `redshift`→`keypoint`, `tolerance`→`dial_setting` |  |
| 57 | `test_reconcile_at_open` · `TestRecordDoesNotExplain` · `test_part_of_a_background_model` | R-map | `setUp`, `background`, `stored_background`, `TestRecordDoesNotExplain.interrupted_tolerance_get` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting` |  |
| 58 | `test_reconcile_at_open` · `TestRecordDoesNotExplain` · `test_part_of_the_recorded_background_model` | R-map | `setUp`, `background`, `TestRecordDoesNotExplain.interrupted_tolerance_get` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting` |  |
| 59 | `test_reconcile_at_open` · `TestRecordDoesNotExplain` · `test_a_recomputed_validated_that_disagrees` | R-map | `setUp`, `stored_background`, `TestRecordDoesNotExplain.interrupted_tolerance_get` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting` |  |
| 60 | `test_reconcile_at_open` · `TestRecordDoesNotExplain` · `test_a_shard_key_the_repair_does_not_supply` | R-map | `setUp`, `TestRecordDoesNotExplain.interrupted_tolerance_get` | `tolerance`→`dial_setting`, `wavenumber`→`keypoint` |  |
| 61 | `test_reconcile_at_open` · `TestHotJournal` · `test_a_hot_journal_on_one_shard_is_rolled_back_then_compared` | R-help, R-map, R-value | `setUp` | `tolerance`→`dial_setting` |  |
| 62 | `test_reconcile_at_open` · `TestHotJournal` · `test_a_hot_journal_on_the_primary_is_rolled_back_before_the_record_is_read` | R-help, R-value | `setUp` | `tolerance`→`dial_setting` |  |
| 63 | `test_reconcile_at_open` · `TestPruningAfterRepair` · `test_an_interrupted_validate` | R-map | `setUp`, `stored_background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint` |  |
| 64 | `test_reconcile_at_open` · `TestPruningAfterRepair` · `test_an_interrupted_store` | R-help, R-map, R-value | `setUp`, `background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `GkSourcePolicy`→`keypoint_alias`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint` | 4 drop actions → 3 (`samples`, `aliases`, `tesserae`) |
| 65 | `test_reconcile_at_open` · `TestCleanStoreUntouched` · `test_opening_a_clean_store_writes_nothing` | R-help, R-value, R-count | `setUp`, `exit_time`, `stored_background` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `GkSourcePolicyData`→`Sample`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` | correction 1: `REPLICATED` (9 tables); the Sample stored validated (§2 item 6) |
| 66 | `test_reconcile_at_open` · `TestCleanStoreUntouched` · `test_a_new_store_has_no_reconciliation` | — | `setUp` | — |  |
| 67 | `test_prune_at_open` · `TestUninterruptedPrune` · `test_every_shard_identical_and_no_record_left` | R-map | `setUp`, `build` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `GkSourcePolicyData`→`Sample`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` | correction 2 (fails if the Sample is stored unvalidated) |
| 68 | `test_prune_at_open` · `TestUninterruptedPrune` · `test_a_prune_with_nothing_to_prune_writes_nothing` | — | `setUp`, `build` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `GkSourcePolicyData`→`Sample`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` | correction 2 (fails if the Sample is stored unvalidated) |
| 69 | `test_prune_at_open` · `TestUninterruptedPrune` · `test_the_set_of_classes_is_read_from_the_factories` | R-imp, R-map | `setUp`, `build` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `GkSource`→`Sample`, `GkSourcePolicyData`→`Sample`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 70 | `test_prune_at_open` · `TestInterruptedPrune` · `test_faulted_after_each_shard` | R-map | `setUp`, `build` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `GkSourcePolicyData`→`Sample`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 71 | `test_prune_at_open` · `TestInterruptedPrune` · `test_faulted_before_the_first_shard` | R-map | `setUp`, `build` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `GkSourcePolicyData`→`Sample`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 72 | `test_prune_at_open` · `TestPruneFailsInTheFactory` · `test_the_record_stays_and_the_next_open_completes_it` | R-map | `setUp`, `build` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `GkSourcePolicyData`→`Sample`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 73 | `test_prune_at_open` · `TestRecordsStayApart` · `test_a_prune_record_over_a_difference_in_another_class_refuses` | R-map | `setUp`, `build` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `GkSourcePolicyData`→`Sample`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 74 | `test_prune_at_open` · `TestRecordsStayApart` · `test_a_prune_record_naming_a_class_that_does_not_prune_refuses` | R-map | `setUp`, `build` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `GkSourcePolicyData`→`Sample`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 75 | `test_prune_at_open` · `TestRecordsStayApart` · `test_a_get_record_of_a_background_model_is_repaired_not_pruned` | R-help, R-map | `setUp`, `build` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `GkSourcePolicyData`→`Sample`, `IntegrationSolver`→`knob_setting`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |
| 76 | `test_prune_at_open` · `TestNoActorDeletesAReplicatedRow` · `test_under_prune_unvalidated` | R-map | `setUp`, `build` | `BackgroundModel`→`Gadget`, `BackgroundModelValue`→`GadgetPart`, `BackgroundModel_tags`→`Gadget_tags`, `GkSourcePolicyData`→`Sample`, `IntegrationSolver`→`knob_setting`, `TkNumericIntegration`→`Sample`, `redshift`→`keypoint`, `tolerance`→`dial_setting`, `wavenumber`→`keypoint`, `wavenumber_exit_time`→`keypoint_alias` |  |

### 1.4 The helpers added to `build.py`

Appended under a banner "the fixtures of the ported write-path tests (added by prompt 03a)";
`SerialHandle` is added to the existing `from datastorekit.tests.client.objects import (...)`.
Nothing existing changes (the diff of `build.py` has no removed line), and 02's 19 tests pass
unchanged.

```python
FRAME_TURNS = 1
PART_POSITIONS = (1.0e4, 1.0e2, 1.0)

def make_framed_gadget(
    pool,
    tags: Sequence[tag_entry],
    positions: Sequence[float] = PART_POSITIONS,
    scale: float = 1.0,
    label: str = "standin-gadget",
) -> Gadget

def make_sample_on(
    alias: keypoint_alias, gadget_serial: int = 1, code: str = "standin-sample"
) -> Sample
```

- `make_framed_gadget` is `sp.make_background_model`'s counterpart: one vectorized get of
  keypoints at `positions` (marked, as SGK's redshifts are got with `is_source=True`), one get of
  the `knob_setting` frame, and an unstored Gadget with `tags` and one part per keypoint, of value
  `scale * (1 + position)`. As in SGK, a `scale` other than 1 changes only the parts, so a second
  Gadget's row equals the first's but for its serial (and flags), and its tags and parts differ.
- `make_sample_on` is `sp.make_policy_data`'s: an unstored Sample on the alias's keypoint (so on
  that keypoint's shard), with no tags or members, keyed on `objects.SerialHandle(gadget_serial)`.

### 1.5 The port check, `docs/extraction/compare_ported_tests.py`

As §2.4 says: `PORTED` (the three pairs) and `NAME_MAP` (empty) are its only configuration; it
reads SGK with `git show 6f7f291:<path>` and the package from the tree, with `ast`; it writes
nothing; exit 0, 1, or 2 when it cannot run. Per module it requires:

1. the set of `Class.method` of every test method (a method named `test*` of a top-level class)
   equal to SGK's after `NAME_MAP`, and every top-level class of SGK's present with the same bases
   (each base by `ast.unparse`, after `NAME_MAP`);
2. for every function or method of SGK's module with a non-empty skeleton, the same qualified name
   in the package with an equal skeleton. The qualified name is the dotted path of enclosing classes
   and functions (nested functions included; a repeated name in one scope gets `#2`, …). The
   skeleton is the source-order list of: calls whose callee is a name, or an attribute, beginning
   with `assert` or `fail` (§2 item 5: any receiver, not only `self`); `raise AssertionError`; and
   `subTest`. A nested function's body belongs to it, not to its parent; a lambda's body belongs to
   the function it is in;
3. no function of the package with a non-empty skeleton that SGK's module lacks, or has with an
   empty one.

Its output per module: tests, classes, functions compared, assertions; each difference, with the
qualified name and the first position at which the skeletons differ; then `OK` or `FAIL`.

### 1.6 `compare_with_source.py`

A fourth kind, `PORTED` (beside `MODULE`, `INTERNALISED` and `SPLIT`). A `PORTED` entry of `FILES`
is not compared line by line, and no class applies to it: the check requires only that the source
exists at the import commit and the package file exists, reports it as "ported: checked by
compare_ported_tests.py", counts it ("files ported, checked by compare_ported_tests.py: 3"), and
fails (exit 1, "FAIL: N ported file(s) missing") if either is missing. The three modules are
`PORTED`; `test_shard_key_assignment.py` joins `NO_SOURCE`. An unaccounted file still fails. 01's
and 02's rules are untouched, and their counts over the 31 compared files are unchanged (§5.3).

## 2. Deviations from the prompt

1. **Correction 1** (the orchestrator's): each module's `REPLICATED` names the replicated classes
   that have a table, then `Gadget_tags`, by filtering the registry on `register() is not None`
   (§1.2). The literal port (`list(replicated_tables) + ["Gadget_tags"]`) names
   `ephemeral_probe`, which has no table. **STRUCTURALLY REQUIRED.**
2. **Correction 2** (the orchestrator's): in `_PruneTestCase.build` the Sample is stored
   **validated** (`build.store_sample`'s default). Probed: with `validate=False` (the literal port)
   `test_every_shard_identical_and_no_record_left` and
   `test_a_prune_with_nothing_to_prune_writes_nothing` fail (`Ran 10 tests` / `FAILED
   (failures=2)`), since each actor then prunes the unvalidated Sample under `prune_unvalidated`.
   The Sample's Gadget is an `objects.SerialHandle(1)` (in `build.make_sample_on`), everywhere, so
   no stored Gadget adds a row to any `Gadget` count. The bare `object_store` stays in
   `TestShardedWritesUnchanged.test_a_sharded_store_stamps_its_own_time_and_writes_no_record` and
   `TestNoRecordRefuses.test_a_difference_in_a_sharded_table_is_not_looked_at`.
   **STRUCTURALLY REQUIRED.**
3. **Breakage (o)** (the orchestrator's addition): §6.1. The note's example, the first two assertion
   calls of `test_a_sharded_store_stamps_its_own_time_and_writes_no_record`, are both
   `assertEqual`, so swapping them changes no skeleton (arguments are not compared, by design); the
   swap made is of the fourth and fifth (`assertNotIn`, `assertEqual`). **IMPLEMENTATION CHOICE**,
   at the orchestrator's direction.
4. **The port check's blind spot is stated** (the orchestrator's addition): §7 item 1.
   **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
5. **The port check counts an assertion call on any receiver**, not only `self.<name>(…)` and
   `<name>(…)` (§1.5). Breakage (d) as first written moved an `assertEqual` into a new module
   function called as `check_no_records(self)`, whose body is `case.assertEqual(...)`; under the
   literal rule the check still exited 1 (the calling test's skeleton lost an `assertEqual`) but
   did not name the helper, so rule 3 ("nothing added that asserts") could be dodged by a helper
   given the test case. Counting `<anything>.assert*(…)`/`.fail*(…)`/`.subTest(…)` closes that.
   It changes no count over 03a's modules (SGK's three hold no such call on another receiver), and
   it makes 03b's modules' `super().assertIdentical()`, `mock.assert_not_called()` and
   `unittest.TestCase().assertRaises(...)` visible (measured at `6f7f291`). **IMPLEMENTATION
   CHOICE.**
6. **`TestCleanStoreUntouched.test_opening_a_clean_store_writes_nothing` stores its Sample
   validated** (`build.store_sample`), where SGK stored its policy data with a bare
   `object_store`. Correction 2 names only `_PruneTestCase.build`; this test is the other place a
   sharded row is written into a store that is then reopened, and an unvalidated Sample would be
   reported as an integrity warning by every actor at the reopen, which SGK's clean store (a class
   with no `validate_on_startup`) never prints. The test passes either way; the validate is made
   before the store is closed, outside its measured window. **IMPLEMENTATION CHOICE**, following
   correction 2's reasoning.
7. **`make_framed_gadget` gets keypoints, as `make_background_model` gets redshifts**, though no
   neutral part names a keypoint. This keeps the fixture's writes SGK's (a vectorized get of the
   flagged class before every model). Its consequence is hazard 1's one measurable effect (§3,
   hazard 1; §6.2 (j)). **IMPLEMENTATION CHOICE.**
8. **The `exit_time` helpers and `_PruneTestCase.build` keep SGK's two tolerance gets**
   (`atol = build.get_dial(self.pool, 10)`, `rtol = build.get_dial(self.pool, 9)`), though the
   alias takes neither; the variables are unused, as in a literal rewrite. The prune tests need the
   rows (one is deleted by hand), and keeping them everywhere keeps every fixture's writes SGK's.
   **IMPLEMENTATION CHOICE.**
9. **`black` rewrote each `with a, b(...):` that it wraps into the parenthesized form** (in `quiet`
   in all three modules, and in `TestInterruptedPrune.test_faulted_after_each_shard`), and re-wrapped
   lines whose length the map changed. `black` 25.1.0 takes its target versions from
   `pyproject.toml`'s `requires-python = ">=3.12"`, where SGK has none. No token other than
   brackets and commas changes. **STRUCTURALLY REQUIRED** (`CLAUDE.md`: format with `black`).
10. **Two docstring words that are SGK column names were mapped**: reconcile's module docstring
    (a ``` ``validated`` ``` difference → ``` ``gadget_validated`` ```) and
    `test_a_recomputed_validated_that_disagrees` (`validated=True` → `gadget_validated=True`).
    R-map, as §2.1 asks for columns "wherever [they appear] in code or text"; the English word
    "validated" and the layer's action name `validated recomputed` are unchanged.
    **IMPLEMENTATION CHOICE.**
11. **SGK's layout in the ported modules' prose is unchanged** (`Datastore.tests.standin_pool`,
    `prompts/…`, `var/`, `utilities.WallclockTimer`, SGK commits, "log 01"), as §2.1 says; it is
    counted under `[01-package-prose-names-sgks-layout]` (§7).

No UNINTENDED DRIFT was found. (A first edit of `build.py` duplicated `build_store`'s body; it was
put right before anything ran, and the committed diff of `build.py` is additions only.)

## 3. The three hazards (§2.2)

**Hazard 1: `keypoint` is both the shard key and the flagged class.**
- `_assign_shard_keys` (`SQL/ShardedPool.py:3505-3580`) writes only the primary's `shard_keys`,
  through `self._engine`, and makes no actor call. Read, and probed in the scratchpad: a
  vectorized get of two new keypoints makes three `object_get` calls and the broker's
  `lease_serials`, and `_assign_shard_keys`, wrapped, adds none to `cluster.calls`.
- **Checksums.** The ported modules take `store_checksums` at 12 lines each in
  `test_reconcile_at_open` (`:148/:160`, `:293/:299`, `:562/:570`, `:780/:786`, `:806/:811`,
  `:1151/:1155`) and `test_prune_at_open` (`:292/:296`, `:344/:348`, `:384/:395`, `:442/:446`,
  `:478/:487`, `:497/:502`). Only `:562-570`
  (`TestKillAndReopen.test_between_the_record_cleared_and_the_shard_key`) spans a successful get
  of the shard-key class; it does in SGK too (`wavenumber` is SGK's shard key), and it asserts that
  the files change.
- **Call counts.** `cluster.calls` is read in `test_a_get_that_inserts_nothing_replicates_nothing`
  (a `dial_setting` get), `TestWriteOverASetRecord.assertRefused` (refused before any call) and
  `test_a_sharded_store_stamps_its_own_time_and_writes_no_record` (cleared after the keypoint get);
  `refused_reopen`'s and `test_a_primary_without_the_record_table_is_refused`'s actor counts span
  no get. None sees the primary's shard keys.
- **What a write touched.** `shard_snapshot`/`shard_rows`/`all_keys` read shards, never the
  primary.
- **Three tests where the flagged class's row is edited by hand** (`test_a_flag`,
  `test_a_flag_the_controller_lacks`, `test_a_record_naming_another_class`): the first two set a
  flag, which no shard key concerns. The third deletes keypoint 5.0 from r1 while the primary
  assigns it a shard key; probed, the refusal still names exactly one difference
  (`class "keypoint", shard [1], serial 1: … the record names "dial_setting"`), as SGK's names one.
- **The one effect seen: (j).** The prune fixture gets a keypoint (SGK's `wavenumber`, serial
  from the first lease) and then, inside `make_framed_gadget`, three more (SGK's redshifts). With no
  pinned controller the second get may run on an actor whose lease starts at 501, so the keys are
  assigned to serials that do not start where `key_serial`'s autoincrement does. Under 01's
  `key_id` binding, the check at open then refuses those stores ("the primary assigns keypoint
  serial 2 to shard 0, but it is missing on shard(s) [0, 1, 2]"), and a varying set of
  `test_prune_at_open` tests fails (§6.2 (j): 7, 3 and 8 tests over three runs). SGK's prune tests
  cannot see that line, since SGK's redshifts are not its shard key. On the unmutated tree nothing
  changes: the four new modules ran six times, `Ran 79 tests … OK` each time. Recorded; no
  assertion changed, and no test was moved.

**Hazard 2: two SGK classes map to one neutral class.**
- `wavenumber` and `redshift` → `keypoint`: the one set holding both is `written` in
  `TestCleanWrite.test_every_copy_is_row_identical` (9 names → 8; `IntegrationSolver` →
  `knob_setting` keeps its own). The test asserts each listed table non-empty and every replicated
  table identical, which holds for the union. No other test lists both: where both are written
  (`TestNoRecordRefuses.setUp`, `TestCleanStoreUntouched`), the positions differ (0.5 against 5.0
  and 50.0), the hand edits name a position (`WHERE kp_position = 5.0`), and the expected
  differences are `["keypoint"]` where SGK's are `["redshift"]`, one entry each.
- `wavenumber_exit_time` and `GkSourcePolicy` → `keypoint_alias`: never in one test (only
  `TestPruningAfterRepair.test_an_interrupted_store` uses `GkSourcePolicy`, and it makes no exit
  time).
- No test's meaning depends on the two being different classes. Not a stop.

**Hazard 3: `TestPruneFailsInTheFactory`.** `Gadget_factory.validate_on_startup`
(`tests/client/factories.py:761-799`) deletes `GadgetPart`, then `Gadget_tags`, then the
`Gadget` rows, inside `except SQLAlchemyError`, and returns normally with "DATABASE ERROR" in its
messages. The trigger `BEFORE DELETE ON "Gadget"` aborts the owner's delete after the parts and
tags were deleted; the pool sees B still there, rolls the shard back whole and raises "did not
take". `test_the_record_stays_and_the_next_open_completes_it` passes unchanged in every assertion.

## 4. The two issues (§2.5)

**`[02-no-test-reaches-revalidate]`.** `TestKillAndReopen.test_validate_of_a_background_model`
(SGK `test_reconcile_at_open.py:486`) interrupts the replicated validate of a stored, unvalidated
`Gadget` at r0, r1 or both, and expects `("validated recomputed", "Gadget", role)` actions: on the
neutral client they come from `_recompute_validated` (`SQL/ShardedPool.py:1992`) calling
`Gadget_factory.revalidate`. 02's breakage (k), replayed byte for byte as (i), fails it (three
subtests) and `TestPruningAfterRepair.test_an_interrupted_validate` (both subtests): §6.2 (i).
**Closed.**

**`[01-no-ported-test-pins-the-shard-key-assignment]`.** None of the 76 compares the saved map
with the one in memory. The new module, `datastorekit/tests/test_shard_key_assignment.py`,
`TestShardKeysAssignedOutOfSerialOrder`:

- **How the order is made, and why it works.** Through the layer's own paths and the stand-in
  pool's faults alone, with no mock of the layer: (1) a get of keypoint A (serial 1) is killed on
  replica r0 (`fault(r0, "object_get", "keypoint", "before")`), so the replicated write raises
  before `_assign_shard_keys` is reached and leaves its record; (2) the store is reopened, and the
  check at open copies A to r0 and clears the record, assigning no key; (3) one vectorized get
  inserts B and C (serials 2, 3) and assigns their keys, and a get of A then assigns A's last. The
  keys are assigned in the order 2, 3, 1. Under the `key_id` binding SQLAlchemy drops the unknown
  parameter and `key_serial` autoincrements 1, 2, 3, so the saved map pairs each shard with the
  wrong serial; with three shards, load balancing gives the three keys three different shards, so
  the pairing is visible.
- `setUp` then stores one validated Sample on each keypoint, closes the pool, reads `shard_keys`
  (`key_serial`, `shard_id`) from the primary with `standin_pool._read`, and reopens.
- `test_the_keys_were_assigned_out_of_serial_order`: the premise (A copied to r0 by the check at
  open, no key after the reopen, serials `[1, 2, 3]`, assignment order `[2, 3, 1]`, and no
  `_assign_shard_keys MISMATCH` printed).
- `test_the_saved_map_is_the_map_in_memory_and_the_reopened_map`: the saved map equals the map
  the pool held before closing, and the reopened pool's `_shard_keys`.
- `test_every_sample_is_on_the_shard_the_reopened_map_names`: for each keypoint (a subtest each),
  the Sample's row is on the shard the reopened map names and on no other (read from the shard
  files), and the reopened pool's `read_batch` finds it there.

01's `key_id` diff, replayed byte for byte as (j), fails all three, every run (§6.2 (j)).
**Closed.**

## 5. Verification performed

### 5.1 The suite (§3.1)

`./venv/bin/python -m unittest discover -s datastorekit/tests -t .`, in the foreground, output to
the scratchpad. **Before: `Ran 109 tests … OK`. After: `Ran 188 tests in 30.125s` / `OK`** = 109
+ 76 + 3. The 109 names of before are all present after (by `Class.test_name`, from `-v`); the
79 new are the 76 of §1.3 and:

- `test_shard_key_assignment.TestShardKeysAssignedOutOfSerialOrder`:
  `test_the_keys_were_assigned_out_of_serial_order`,
  `test_the_saved_map_is_the_map_in_memory_and_the_reopened_map`,
  `test_every_sample_is_on_the_shard_the_reopened_map_names`.

02's 19 tests of `test_neutral_client` pass unchanged. The four new modules, run six more times
together, gave `Ran 79 tests … OK` each time. Python 3.12.15, `ray==2.43.0`,
`SQLAlchemy==2.0.39`, `black==25.1.0`; no Ray process was up at any point (`pgrep -lf
'gcs_server|raylet|ray::'` empty), and every store was in a `tempfile` directory.

### 5.2 The port check (§3.2)

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

OK: 3 module(s) keep their source's tests, classes and assertion skeletons
```

It was run after each module was ported, in the order `test_prune_at_open`, `test_replicated_write`,
`test_reconcile_at_open`, and exited 0 each time.

### 5.3 The equivalence check (§3.3)

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
files ported, checked by compare_ported_tests.py: 3
files with no source, declared: 8
ported: checked by compare_ported_tests.py: datastorekit/tests/test_replicated_write.py (from Datastore/tests/test_replicated_write.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_reconcile_at_open.py (from Datastore/tests/test_reconcile_at_open.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_prune_at_open.py (from Datastore/tests/test_prune_at_open.py)
not compared (no source, declared): datastorekit/tests/client/__init__.py
not compared (no source, declared): datastorekit/tests/client/build.py
not compared (no source, declared): datastorekit/tests/client/factories.py
not compared (no source, declared): datastorekit/tests/client/objects.py
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

Against its output before this prompt, the only differences are the three `ported` lines, the
"files ported" count and the eighth `NO_SOURCE` file: the table over the 31 compared files and
its totals are unchanged (D-imp −50/+50, D-str −7/+7, D-tool −26/+22, D-root −8/+6, D-fix
−15/+15, D-split −169/+8, D-int −222/+11, D-fmt −3/+0, UNCLASSIFIED 0). 31 compared, 3 `PORTED`,
8 with no source: the 42 `.py` files under `datastorekit/`.

### 5.4 The vocabulary (§3.4)

`grep -nwE` for the 80 client table names of log 02 §1.2 (the 82 less `version` and `store_tag`)
over `test_replicated_write.py`, `test_reconcile_at_open.py`, `test_prune_at_open.py` and
`test_shard_key_assignment.py`: **no match** (exit 1). The same grep over SGK's three modules
matches 67, 84 and 32 lines.

### 5.5 `black` (§3.6)

`./venv/bin/black --check datastorekit docs/extraction` (25.1.0) → `44 files would be left
unchanged.`

## 6. The deliberate-breakage record (§3.5)

Each diff below is exactly as applied. Each was made by editing the tree, taken with `git diff`
against the staged tree `11247c7` records, and the file restored from the index; then checked
with `git apply --check` and `git apply -R --check`, applied with `git apply`, run, and reverted
with `git apply -R`, in `bash`. `git diff` and the untracked list were empty after each. None is
committed.

### 6.1 The checks

**(a) the last `assertNoRecord()` deleted from
`TestCleanWrite.test_a_get_that_inserts_nothing_replicates_nothing`** — `compare_ported_tests.py`
exits **1**:

```diff
diff --git a/datastorekit/tests/test_replicated_write.py b/datastorekit/tests/test_replicated_write.py
index 8a890fd..0d7c032 100644
--- a/datastorekit/tests/test_replicated_write.py
+++ b/datastorekit/tests/test_replicated_write.py
@@ -233,7 +233,6 @@ class TestCleanWrite(_PoolTestCase):
         build.get_dial(self.pool, 6)
         gets = [c for c in self.cluster.calls if c["method"] == "object_get"]
         self.assertEqual([self.controller], [c["shard"] for c in gets])
-        self.assertNoRecord()
 
 
 # ------------------------------------------------------------------------------------------------
```
```
  DIFFERS  TestCleanWrite.test_a_get_that_inserts_nothing_replicates_nothing: skeleton differs at position 2: the source has assertNoRecord, the package (nothing) (2 in the source, 1 in the package)
FAIL: 1 of 3 module(s) differ from their source
```

**(b) that test renamed** — exits **1**:

```diff
diff --git a/datastorekit/tests/test_replicated_write.py b/datastorekit/tests/test_replicated_write.py
index 8a890fd..2022bb9 100644
--- a/datastorekit/tests/test_replicated_write.py
+++ b/datastorekit/tests/test_replicated_write.py
@@ -227,7 +227,7 @@ class TestCleanWrite(_PoolTestCase):
             self.serials("keypoint_alias"),
         )
 
-    def test_a_get_that_inserts_nothing_replicates_nothing(self):
+    def test_a_get_that_inserts_nothing_replicates_nothing_at_all(self):
         build.get_dial(self.pool, 6)
         self.cluster.calls.clear()
         build.get_dial(self.pool, 6)
```
```
  DIFFERS  test missing from the package: TestCleanWrite.test_a_get_that_inserts_nothing_replicates_nothing
  DIFFERS  test not in the source: TestCleanWrite.test_a_get_that_inserts_nothing_replicates_nothing_at_all
  DIFFERS  TestCleanWrite.test_a_get_that_inserts_nothing_replicates_nothing: asserts in the source (2), missing from the package
  DIFFERS  TestCleanWrite.test_a_get_that_inserts_nothing_replicates_nothing_at_all: not in the source, and asserts (assertEqual, assertNoRecord)
FAIL: 1 of 3 module(s) differ from their source
```

**(c) `assertEqual` → `assertTrue` inside `_PoolTestCase.assertNoRecord`** — exits **1**:

```diff
diff --git a/datastorekit/tests/test_replicated_write.py b/datastorekit/tests/test_replicated_write.py
index 8a890fd..8a8ece9 100644
--- a/datastorekit/tests/test_replicated_write.py
+++ b/datastorekit/tests/test_replicated_write.py
@@ -156,7 +156,7 @@ class _PoolTestCase(unittest.TestCase):
         return record
 
     def assertNoRecord(self):
-        self.assertEqual([], self.records())
+        self.assertTrue([] == self.records())
 
     def serials(self, table, where="", params=()):
         """table -> {shard: sorted serials}."""
```
```
  DIFFERS  _PoolTestCase.assertNoRecord: skeleton differs at position 1: the source has assertEqual, the package assertTrue (1 in the source, 1 in the package)
FAIL: 1 of 3 module(s) differ from their source
```

**(d) a new helper holding an `assertEqual`, called from a ported test in place of an inline
assertion** — exits **1**, naming both the test and the helper (§2 item 5):

```diff
diff --git a/datastorekit/tests/test_prune_at_open.py b/datastorekit/tests/test_prune_at_open.py
index 9391e5b..c48a0dd 100644
--- a/datastorekit/tests/test_prune_at_open.py
+++ b/datastorekit/tests/test_prune_at_open.py
@@ -78,6 +78,10 @@ def execute(path: Path, *statements):
         conn.close()
 
 
+def check_no_records(case):
+    case.assertEqual([], case.records())
+
+
 class SimulatedDeath(Exception):
     """The process killed inside the pool's prune."""
 
@@ -276,7 +280,7 @@ class TestUninterruptedPrune(_PruneTestCase):
             [(sid, [("prune", "Gadget", None, None)]) for sid in self.shard_ids],
             seen,
         )
-        self.assertEqual([], self.records())
+        check_no_records(self)
         self.assertPruned(a_rows)
         self.assertEqual(sharded, self.sharded_rows())
         self.assertEqual(others, self.replicated_rows())
```
```
  DIFFERS  TestUninterruptedPrune.test_every_shard_identical_and_no_record_left: skeleton differs at position 2: the source has assertEqual, the package assertPruned (7 in the source, 6 in the package)
  DIFFERS  check_no_records: not in the source, and asserts (assertEqual)
FAIL: 1 of 3 module(s) differ from their source
```

**(o) two assertion calls of different names swapped in
`TestShardedWritesUnchanged.test_a_sharded_store_stamps_its_own_time_and_writes_no_record`**
(§2 item 3) — exits **1**, naming the test and the position:

```diff
diff --git a/datastorekit/tests/test_replicated_write.py b/datastorekit/tests/test_replicated_write.py
index 8a890fd..24417e1 100644
--- a/datastorekit/tests/test_replicated_write.py
+++ b/datastorekit/tests/test_replicated_write.py
@@ -700,8 +700,8 @@ class TestShardedWritesUnchanged(_PoolTestCase):
         self.assertEqual(1, len(stores))
         self.assertEqual(shard, stores[0]["shard"])
         self.assertEqual("Sample", stores[0]["class"])
-        self.assertNotIn("insert_timestamp", stores[0]["kwargs"])
         self.assertEqual([0, 0], seen)
+        self.assertNotIn("insert_timestamp", stores[0]["kwargs"])
         self.assertNoRecord()
 
         rows = sp._read(
```
```
  DIFFERS  TestShardedWritesUnchanged.test_a_sharded_store_stamps_its_own_time_and_writes_no_record: skeleton differs at position 4: the source has assertNotIn, the package assertEqual (8 in the source, 8 in the package)
FAIL: 1 of 3 module(s) differ from their source
```

**(e) one ported module deleted** (`test_prune_at_open.py`) — `compare_with_source.py` exits
**1**. The diff is the deletion of the whole file as `11247c7` records it (`rm` of the file,
then `git diff`); it is given in full below.

```
ported (MISSING in the package): datastorekit/tests/test_prune_at_open.py (from Datastore/tests/test_prune_at_open.py)
FAIL: 1 ported file(s) missing: datastorekit/tests/test_prune_at_open.py
```

<details><summary>(e)'s diff, in full</summary>

```diff
diff --git a/datastorekit/tests/test_prune_at_open.py b/datastorekit/tests/test_prune_at_open.py
deleted file mode 100644
index 9391e5b..0000000
--- a/datastorekit/tests/test_prune_at_open.py
+++ /dev/null
@@ -1,612 +0,0 @@
-"""
-The prune at open of a replicated class, by the pool, under a record (prompts/a3-v2-readiness,
-prompt 02, W3; the user's decision U1).
-
-Under ``prune_unvalidated=True``, ``ShardedPool.__init__`` prunes every replicated class whose
-factory prunes at startup (``Gadget``, with its tags and values) after the check at open
-and before the broker or any actor exists: a ``prune`` record is committed on the primary, each
-shard is pruned by the factory's own ``validate_on_startup`` in its own transaction and checked,
-and the record is cleared last. The check at open completes an interrupted prune by running it
-again on every shard, whatever the open's ``prune_unvalidated`` is. Actors prune sharded classes
-only. These tests drive the real ``ShardedPool``, ``Datastore``, factories and broker on stand-in
-shards (``Datastore.tests.standin_pool``):
-
-1. an uninterrupted prune: every shard identical, no record left, the record set while each shard
-   was pruned; a validated model, and every sharded row, untouched; a prune with nothing to
-   prune writes nothing;
-2. faulted after shard k's prune, for each k, and before the first shard: the next open, with
-   ``prune_unvalidated`` false, completes it and clears the record;
-3. a prune that fails on one shard inside the factory (which catches its own ``SQLAlchemyError``):
-   the record stays, the open raises, a completion that fails the same way writes nothing, and
-   the next open completes it;
-4. the two kinds of record stay apart: a ``prune`` record over a difference in another class
-   refuses; a ``get`` record of ``Gadget`` over shards that differ is repaired, not
-   pruned;
-5. no actor deletes a replicated row, even when the pool's prune has not run;
-6. no Ray is initialised.
-
-Every store is built in a temporary directory; nothing under ``var/`` is opened.
-"""
-
-import contextlib
-import io
-import re
-import sqlite3
-import tempfile
-import unittest
-from pathlib import Path
-from unittest import mock
-
-import ray
-import sqlalchemy as sqla
-
-from datastorekit.tests.client.registry import factories as _factories
-from datastorekit.replication import ReplicatedDivergence
-from datastorekit.tests import standin_pool as sp
-from datastorekit.tests.client import build
-from datastorekit.tests.client.registry import replicated_tables, sharded_tables
-
-# every table the check compares: the replicated classes that have a table (a class whose
-# register() is None has none, and is not compared) and Gadget's tag table
-REPLICATED = [t for t in replicated_tables if _factories[t].register() is not None] + [
-    "Gadget_tags"
-]
-UNIT = ("Gadget", "Gadget_tags", "GadgetPart")
-
-
-def tearDownModule():
-    if ray.is_initialized():
-        raise AssertionError("Ray was initialised by test_prune_at_open")
-
-
-@contextlib.contextmanager
-def quiet():
-    with (
-        contextlib.redirect_stdout(io.StringIO()),
-        contextlib.redirect_stderr(io.StringIO()),
-    ):
-        yield
-
-
-def execute(path: Path, *statements):
-    conn = sqlite3.connect(path)
-    try:
-        for statement in statements:
-            conn.execute(statement)
-        conn.commit()
-    finally:
-        conn.close()
-
-
-class SimulatedDeath(Exception):
-    """The process killed inside the pool's prune."""
-
-
-class _PruneTestCase(unittest.TestCase):
-    """
-    A three-shard store holding a validated Gadget (A, tag run-A), an unvalidated one
-    (B, tag run-B, its values scaled), an exit time and a sharded Sample row.
-    """
-
-    def setUp(self):
-        tmp = tempfile.TemporaryDirectory()
-        self.addCleanup(tmp.cleanup)
-        self.root = Path(tmp.name)
-        self._stores = 0
-
-        self.cluster = sp.StandinCluster()
-        active = self.cluster.active()
-        active.__enter__()
-        self.addCleanup(active.__exit__, None, None, None)
-        self.addCleanup(self.close)
-
-    def tearDown(self):
-        self.assertFalse(ray.is_initialized())
-
-    def build(self, unvalidated=True):
-        """A new store, closed: model A validated, model B (if ``unvalidated``) not."""
-        self.close()
-        self._stores += 1
-        self.primary = self.root / f"store-{self._stores}" / "store.sqlite"
-        self.pool = self.cluster.open_pool(self.primary)
-        self.shard_ids = sorted(self.pool._shards.keys())
-        self.files = dict(self.pool._shard_db_files)
-
-        atol = build.get_dial(self.pool, 10)
-        rtol = build.get_dial(self.pool, 9)
-        k = build.get_keypoint(self.pool, 0.5, marked=True)
-        exit_time = ray.get(self.pool.object_store(build.make_alias(k, 1.0e6)))
-        build.store_sample(self.pool, build.make_sample_on(exit_time))
-
-        self.model_a = self.store_model("run-A", 1.0)
-        self.assertTrue(ray.get(self.pool.object_validate(self.model_a)))
-        self.model_b = self.store_model("run-B", 2.0) if unvalidated else None
-        self.close()
-
-    def store_model(self, tag, scale):
-        tags = [ray.get(self.pool.object_get("store_tag", label=tag))]
-        return ray.get(
-            self.pool.object_store(
-                build.make_framed_gadget(self.pool, tags, scale=scale)
-            )
-        )
-
-    def open(self, **kwargs):
-        self.close()
-        self.pool, printed = self.cluster.open_pool_output(self.primary, **kwargs)
-        return printed
-
-    def close(self):
-        self.cluster.clear_faults()
-        self.cluster.hooks.clear()
-        if self.cluster.pool is not None:
-            self.cluster.close_pool()
-        self.pool = None
-
-    # -- reading the closed store ------------------------------------------------------------
-
-    def records(self):
-        rows = sp._read(
-            self.primary,
-            'SELECT operation, class_name, controller_shard, store_id FROM "replication_in_flight"',
-        )
-        return [tuple(r) for r in rows]
-
-    def models(self, sid):
-        return sp._read(
-            self.files[sid],
-            'SELECT serial, gadget_validated FROM "Gadget" ORDER BY serial',
-        )
-
-    def unit_rows(self, sid, serial):
-        return {
-            "Gadget": sp._read(
-                self.files[sid],
-                'SELECT * FROM "Gadget" WHERE serial = ?',
-                (serial,),
-            ),
-            "Gadget_tags": sp._read(
-                self.files[sid],
-                'SELECT * FROM "Gadget_tags" WHERE gadget_serial = ?',
-                (serial,),
-            ),
-            "GadgetPart": sp._read(
-                self.files[sid],
-                'SELECT * FROM "GadgetPart" WHERE gadget_serial = ? ORDER BY serial',
-                (serial,),
-            ),
-        }
-
-    def sharded_rows(self):
-        return {
-            (table, sid): sp._read(path, f'SELECT * FROM "{table}" ORDER BY 1')
-            for table in sharded_tables
-            for sid, path in self.files.items()
-        }
-
-    def replicated_rows(self, exclude=UNIT):
-        out = {}
-        for table in REPLICATED:
-            if table in exclude:
-                continue
-            for sid, path in self.files.items():
-                out[(table, sid)] = sp._read(
-                    path, f'SELECT * FROM "{table}" ORDER BY 1'
-                )
-        return out
-
-    def assertIdentical(self):
-        for table in REPLICATED:
-            rows = {
-                sid: sp._read(path, f'SELECT * FROM "{table}" ORDER BY 1')
-                for sid, path in self.files.items()
-            }
-            first = rows[self.shard_ids[0]]
-            for sid in self.shard_ids:
-                self.assertEqual(first, rows[sid], f"{table}: shard {sid}")
-
-    def assertPruned(self, a_rows=None):
-        """B is gone from every shard, as a unit; A is there, validated, unchanged."""
-        for sid in self.shard_ids:
-            self.assertEqual([(self.model_a.store_id, 1)], self.models(sid), sid)
-            gone = self.unit_rows(sid, self.model_b.store_id)
-            self.assertEqual({t: [] for t in UNIT}, gone, sid)
-            if a_rows is not None:
-                self.assertEqual(
-                    a_rows[sid], self.unit_rows(sid, self.model_a.store_id), sid
-                )
-        self.assertIdentical()
-
-    # -- faults inside the pool's prune ------------------------------------------------------
-
-    @contextlib.contextmanager
-    def die_in_prune(self, after=None, before=None):
-        """Kill the open inside the pool's prune: after the ``after``-th shard's prune has
-        committed (0-based, in the order the pool prunes them), or before the ``before``-th.
-        """
-        original = sp.sp_mod.ShardedPool._prune_shard_and_commit
-        calls = {"n": 0}
-
-        def wrapped(pool, *args, **kwargs):
-            n = calls["n"]
-            calls["n"] += 1
-            if before is not None and n == before:
-                raise SimulatedDeath(f"killed before shard prune {n}")
-            result = original(pool, *args, **kwargs)
-            if after is not None and n == after:
-                raise SimulatedDeath(f"killed after shard prune {n}")
-            return result
-
-        with mock.patch.object(
-            sp.sp_mod.ShardedPool, "_prune_shard_and_commit", wrapped
-        ):
-            yield calls
-
-
-# ------------------------------------------------------------------------------------------------
-# 1. the uninterrupted prune
-# ------------------------------------------------------------------------------------------------
-
-
-class TestUninterruptedPrune(_PruneTestCase):
-    def test_every_shard_identical_and_no_record_left(self):
-        self.build()
-        a_rows = {
-            sid: self.unit_rows(sid, self.model_a.store_id) for sid in self.shard_ids
-        }
-        sharded = self.sharded_rows()
-        others = self.replicated_rows()
-
-        # the record is set, naming the prune and no controller, while each shard is pruned
-        seen = []
-        original = sp.sp_mod.ShardedPool._prune_shard_and_commit
-
-        def watching(pool, cls_name, sid, *args, **kwargs):
-            seen.append((sid, self.records()))
-            return original(pool, cls_name, sid, *args, **kwargs)
-
-        with mock.patch.object(
-            sp.sp_mod.ShardedPool, "_prune_shard_and_commit", watching
-        ):
-            printed = self.open(prune_unvalidated=True)
-        pruned = self.pool.pruned
-        self.close()
-
-        self.assertEqual(
-            [(sid, [("prune", "Gadget", None, None)]) for sid in self.shard_ids],
-            seen,
-        )
-        self.assertEqual([], self.records())
-        self.assertPruned(a_rows)
-        self.assertEqual(sharded, self.sharded_rows())
-        self.assertEqual(others, self.replicated_rows())
-
-        self.assertEqual(
-            {(t, sid) for t in UNIT for sid in self.shard_ids},
-            {(a["class_name"], a["shard"]) for a in pruned},
-        )
-        self.assertIn('pruned by the pool under a "prune" record', printed)
-
-    def test_a_prune_with_nothing_to_prune_writes_nothing(self):
-        self.build(unvalidated=False)
-        checksums = sp.store_checksums(self.primary)
-        self.open(prune_unvalidated=True)
-        self.assertEqual([], self.pool.pruned)
-        self.close()
-        self.assertEqual(checksums, sp.store_checksums(self.primary))
-
-    def test_the_set_of_classes_is_read_from_the_factories(self):
-        from datastorekit.SQL.schema import build_schema
-
-        built = build_schema(sqla.MetaData(), _factories)
-        self.assertEqual(
-            ["Gadget"],
-            sp.sp_mod.ShardedPool._replicated_prune_classes(replicated_tables, built),
-        )
-        # a replicated list naming a sharded class that prunes at startup would include it
-        self.assertEqual(
-            ["Gadget", "Sample"],
-            sp.sp_mod.ShardedPool._replicated_prune_classes(
-                ["version", "Gadget", "Sample"], built
-            ),
-        )
-
-
-# ------------------------------------------------------------------------------------------------
-# 2. an interrupted prune, completed by the next open
-# ------------------------------------------------------------------------------------------------
-
-
-class TestInterruptedPrune(_PruneTestCase):
-    def assertCompleted(self, done_before):
-        """Reopen with prune_unvalidated false: the prune is completed on the shards it had not
-        reached, the record cleared, and a second reopen writes nothing."""
-        printed = self.open(prune_unvalidated=False)
-        rec = self.pool.reconciliation
-        self.close()
-        self.assertEqual("prune", rec["record"]["operation"])
-        self.assertEqual("Gadget", rec["record"]["class_name"])
-        self.assertIsNone(rec["controller"])
-        self.assertTrue(rec["cleared"])
-        self.assertEqual(
-            {
-                (t, sid)
-                for t in UNIT
-                for sid in self.shard_ids
-                if sid not in done_before
-            },
-            {(a["class_name"], a["shard"]) for a in rec["repaired"]},
-        )
-        self.assertIn("was opened with a prune in flight", printed)
-        self.assertEqual([], self.records())
-        self.assertPruned(self.a_rows)
-
-        checksums = sp.store_checksums(self.primary)
-        self.open()
-        self.assertIsNone(self.pool.reconciliation["record"])
-        self.close()
-        self.assertEqual(checksums, sp.store_checksums(self.primary))
-
-    def test_faulted_after_each_shard(self):
-        for k in range(3):
-            with self.subTest(after=k):
-                self.build()
-                self.a_rows = {
-                    sid: self.unit_rows(sid, self.model_a.store_id)
-                    for sid in self.shard_ids
-                }
-                with (
-                    self.die_in_prune(after=k),
-                    quiet(),
-                    self.assertRaises(SimulatedDeath),
-                ):
-                    self.open(prune_unvalidated=True)
-                self.cluster.pool = None
-
-                self.assertEqual([("prune", "Gadget", None, None)], self.records())
-                done = self.shard_ids[: k + 1]
-                for sid in self.shard_ids:
-                    models = [s for s, _ in self.models(sid)]
-                    if sid in done:
-                        self.assertNotIn(self.model_b.store_id, models, (k, sid))
-                    else:
-                        self.assertIn(self.model_b.store_id, models, (k, sid))
-
-                self.assertCompleted(done)
-
-    def test_faulted_before_the_first_shard(self):
-        self.build()
-        self.a_rows = {
-            sid: self.unit_rows(sid, self.model_a.store_id) for sid in self.shard_ids
-        }
-        shards_before = {
-            name: c
-            for name, c in sp.store_checksums(self.primary).items()
-            if name != "store.sqlite"
-        }
-        with self.die_in_prune(before=0), quiet(), self.assertRaises(SimulatedDeath):
-            self.open(prune_unvalidated=True)
-        self.cluster.pool = None
-        self.assertEqual([("prune", "Gadget", None, None)], self.records())
-        self.assertEqual(
-            shards_before,
-            {
-                name: c
-                for name, c in sp.store_checksums(self.primary).items()
-                if name != "store.sqlite"
-            },
-        )
-        self.assertCompleted([])
-
-
-# ------------------------------------------------------------------------------------------------
-# 3. a prune that fails inside the factory
-# ------------------------------------------------------------------------------------------------
-
-
-class TestPruneFailsInTheFactory(_PruneTestCase):
-    TRIGGER = (
-        'CREATE TRIGGER standin_refuse BEFORE DELETE ON "Gadget" '
-        "BEGIN SELECT RAISE(ABORT, 'standin: delete refused'); END"
-    )
-
-    def test_the_record_stays_and_the_next_open_completes_it(self):
-        """The factory catches the SQLAlchemyError its delete raises and returns normally; the
-        pool sees the unvalidated row still there, rolls the shard back and raises."""
-        self.build()
-        self.a_rows = {
-            sid: self.unit_rows(sid, self.model_a.store_id) for sid in self.shard_ids
-        }
-        failing = self.shard_ids[1]
-        b_rows = self.unit_rows(failing, self.model_b.store_id)
-        execute(self.files[failing], self.TRIGGER)
-
-        with quiet(), self.assertRaises(RuntimeError) as raised:
-            self.open(prune_unvalidated=True)
-        self.cluster.pool = None
-        self.assertIn("did not take", str(raised.exception))
-        self.assertIn(f"shard {failing}", str(raised.exception))
-        self.assertEqual([("prune", "Gadget", None, None)], self.records())
-        # the shard before it was pruned and committed, the failing shard rolled back whole
-        # (its values and tags were deleted before the model's delete failed), the one after
-        # never reached
-        self.assertNotIn(
-            self.model_b.store_id, [s for s, _ in self.models(self.shard_ids[0])]
-        )
-        self.assertEqual(b_rows, self.unit_rows(failing, self.model_b.store_id))
-        self.assertIn(
-            self.model_b.store_id, [s for s, _ in self.models(self.shard_ids[2])]
-        )
-
-        # a completion that fails the same way rolls every shard back and writes nothing
-        checksums = sp.store_checksums(self.primary)
-        with quiet(), self.assertRaises(RuntimeError):
-            self.open()
-        self.cluster.pool = None
-        self.assertEqual(checksums, sp.store_checksums(self.primary))
-
-        # the fault cleared, the next open completes the prune
-        execute(self.files[failing], "DROP TRIGGER standin_refuse")
-        self.open()
-        rec = self.pool.reconciliation
-        self.close()
-        self.assertTrue(rec["cleared"])
-        self.assertEqual(
-            {(t, sid) for t in UNIT for sid in self.shard_ids[1:]},
-            {(a["class_name"], a["shard"]) for a in rec["repaired"]},
-        )
-        self.assertEqual([], self.records())
-        self.assertPruned(self.a_rows)
-
-
-# ------------------------------------------------------------------------------------------------
-# 4. the two kinds of record stay apart
-# ------------------------------------------------------------------------------------------------
-
-
-class TestRecordsStayApart(_PruneTestCase):
-    def test_a_prune_record_over_a_difference_in_another_class_refuses(self):
-        self.build()
-        with self.die_in_prune(after=0), quiet(), self.assertRaises(SimulatedDeath):
-            self.open(prune_unvalidated=True)
-        self.cluster.pool = None
-        # a difference the prune does not explain: a dial_setting row gone from one shard
-        execute(
-            self.files[self.shard_ids[2]],
-            "DELETE FROM dial_setting WHERE serial = (SELECT max(serial) FROM dial_setting)",
-        )
-        checksums = sp.store_checksums(self.primary)
-        with quiet(), self.assertRaises(ReplicatedDivergence) as raised:
-            self.open()
-        self.cluster.pool = None
-        e = raised.exception
-        self.assertEqual("prune", e.record["operation"])
-        self.assertTrue(e.after_repair)
-        self.assertEqual({"dial_setting"}, {d["class_name"] for d in e.differences})
-        # every shard rolled back, the record left
-        self.assertEqual(checksums, sp.store_checksums(self.primary))
-        self.assertEqual([("prune", "Gadget", None, None)], self.records())
-
-    def test_a_prune_record_naming_a_class_that_does_not_prune_refuses(self):
-        self.build(unvalidated=False)
-        execute(
-            self.primary,
-            "INSERT INTO replication_in_flight (operation, class_name, controller_shard, "
-            "store_id, started) VALUES ('prune', 'dial_setting', NULL, NULL, '2026-10-03 00:00:00')",
-        )
-        checksums = sp.store_checksums(self.primary)
-        with quiet(), self.assertRaises(ReplicatedDivergence) as raised:
-            self.open()
-        self.cluster.pool = None
-        self.assertIn("prune of a class", str(raised.exception))
-        self.assertEqual(checksums, sp.store_checksums(self.primary))
-
-    def test_a_get_record_of_a_background_model_is_repaired_not_pruned(self):
-        """An interrupted store of the unvalidated model B, whose replica never ran, with its
-        record then read as a get: the check at open copies B to that replica, from the
-        controller, and deletes nothing."""
-        self.build(unvalidated=False)
-        self.pool = self.cluster.open_pool(self.primary)
-        shard_ids = list(self.pool._shards.keys())
-        self.cluster.controller = shard_ids[1]
-        replica = self.cluster.replica_ids()[1]
-        model = build.make_framed_gadget(
-            self.pool,
-            [ray.get(self.pool.object_get("store_tag", label="run-B"))],
-            scale=2.0,
-        )
-        self.cluster.fault(replica, "object_store", "Gadget", "before")
-        with quiet(), self.assertRaises(sp.StandinActorDied):
-            ray.get(self.pool.object_store(model))
-        self.close()
-        self.cluster.controller = None
-        execute(self.primary, "UPDATE replication_in_flight SET operation = 'get'")
-        held = [s for s, _ in self.models(shard_ids[1])]
-        serial_b = max(held)
-        self.assertNotIn(serial_b, [s for s, _ in self.models(replica)])
-
-        self.open(prune_unvalidated=False)
-        rec = self.pool.reconciliation
-        self.close()
-        self.assertEqual("get", rec["record"]["operation"])
-        self.assertTrue(rec["cleared"])
-        self.assertEqual(
-            {("copied", t, replica) for t in UNIT},
-            {(a["action"], a["class_name"], a["shard"]) for a in rec["repaired"]},
-        )
-        for sid in self.shard_ids:
-            self.assertEqual(
-                [(self.model_a.store_id, 1), (serial_b, 0)], self.models(sid), sid
-            )
-        self.assertIdentical()
-
-
-# ------------------------------------------------------------------------------------------------
-# 5. no actor deletes a replicated row
-# ------------------------------------------------------------------------------------------------
-
-
-class TestNoActorDeletesAReplicatedRow(_PruneTestCase):
-    def test_under_prune_unvalidated(self):
-        """With the pool's own prune stood down, so that the unvalidated model B is still there
-        when the actors start: each actor's _validate_on_startup issues no DELETE on a replicated
-        table, asks the Gadget factory to report only, and asks a sharded class's
-        factory to prune. B is still on every shard afterwards."""
-        self.build()
-        deletes = []
-        prunes = []
-        original_validate = sp.DatastoreClass._validate_on_startup
-
-        def validate(actor):
-            def on_execute(conn, cursor, statement, parameters, context, executemany):
-                if statement.lstrip().upper().startswith("DELETE"):
-                    deletes.append((actor._my_name, statement))
-
-            sqla.event.listen(actor._engine, "before_cursor_execute", on_execute)
-            try:
-                return original_validate(actor)
-            finally:
-                sqla.event.remove(actor._engine, "before_cursor_execute", on_execute)
-
-        patches = []
-        for cls_name in ("Gadget", "Sample"):
-            factory = _factories[cls_name]
-            original = factory.validate_on_startup
-
-            def recording(conn, table, tables, prune=False, _o=original, _c=cls_name):
-                prunes.append((_c, prune))
-                return _o(conn, table, tables, prune)
-
-            patches.append(mock.patch.object(factory, "validate_on_startup", recording))
-
-        with contextlib.ExitStack() as stack:
-            stack.enter_context(
-                mock.patch.object(sp.DatastoreClass, "_validate_on_startup", validate)
-            )
-            stack.enter_context(
-                mock.patch.object(
-                    sp.sp_mod.ShardedPool,
-                    "_prune_replicated_tables",
-                    lambda pool: [],
-                )
-            )
-            for p in patches:
-                stack.enter_context(p)
-            with quiet():
-                self.open(prune_unvalidated=True)
-        self.close()
-
-        tables = [
-            re.match(r'\s*DELETE\s+FROM\s+"?(\w+)"?', s, re.IGNORECASE).group(1)
-            for _, s in deletes
-        ]
-        self.assertEqual([], [t for t in tables if t in set(REPLICATED)])
-        self.assertEqual({("Gadget", False), ("Sample", True)}, set(prunes))
-        self.assertEqual(6, len(prunes))
-        for sid in self.shard_ids:
-            self.assertIn(self.model_b.store_id, [s for s, _ in self.models(sid)])
-        self.assertIdentical()
-
-
-if __name__ == "__main__":
-    unittest.main()
```

</details>

### 6.2 The layer, through the ported tests

Each through the whole suite (`Ran 188 tests`). "SGK" says whether the failing test's SGK
counterpart pins the same line: by reading, since SGK's code is not run here; the package's
`SQL/ShardedPool.py` is SGK's modulo D-imp, so the line is SGK's too.

**(f) the refusal of a write over a set record made a `pass`** (`SQL/ShardedPool.py:3097`) —
`FAILED (errors=1)`: `test_replicated_write.TestWriteOverASetRecord.test_every_path_refuses`
(its first `assertRefused`: the get goes ahead over the set record, writes a second record, and
then raises `RuntimeError: ShardedPool: the replication_in_flight record of a replicated get of
"dial_setting" has 2 rows, expected 1` where `ReplicationInFlight` was expected).
SGK: the same test, the same `assertRefused` path, pins it.

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 8d1fd81..c5eff80 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -3094,7 +3094,7 @@ class ShardedPool:
             with self._engine.begin() as conn:
                 existing = conn.execute(sqla.select(record_table)).mappings().first()
                 if existing is not None:
-                    raise ReplicationInFlight(self._primary_file, dict(existing))
+                    pass
                 conn.execute(
                     sqla.insert(record_table),
                     {
```

**(g) the monotone-flag repair made to set nothing** (`SQL/ShardedPool.py:1938-1945`) —
`FAILED (errors=2)`: `test_reconcile_at_open.TestKillAndReopen.test_scalar_get_that_turns_a_flag_on`
and `…test_vectorized_get_that_inserts_and_turns_a_flag_on` (each: the reopen raises
`ReplicatedDivergence`, e.g. `class "keypoint", shard [1], serial 1: … kp_flagged: True on
shard(s) [0, 2]; False on shard(s) [1]`). SGK: the same two tests (on
`wavenumber` and `redshift`) expect `"flags set"`, and pin it.

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 8d1fd81..e21ec25 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -1938,11 +1938,7 @@ class ShardedPool:
         for (name, sid), per_key in sorted(plan["flags"].items()):
             table = by_name[name]["table"]
             for key, columns in sorted(per_key.items()):
-                conns[sid].execute(
-                    sqla.update(table)
-                    .where(table.c.serial == key[0])
-                    .values({c: True for c in columns})
-                )
+                pass
             actions.append(
                 {
                     "action": "flags set",
```

**(h) the prune's record left in place** (`SQL/ShardedPool.py:2341`) — `FAILED (failures=2)`:
`test_prune_at_open.TestUninterruptedPrune.test_every_shard_identical_and_no_record_left`
(`[] != [('prune', 'Gadget', None, None)]`) and
`test_reconcile_at_open.TestPruningAfterRepair.test_an_interrupted_store` (`prune=True`; the
prune's record left, `assertNoRecord` fails). SGK: the same two tests pin it.

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 8d1fd81..6c24ceb 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -2338,7 +2338,6 @@ class ShardedPool:
                 )
 
             # 4. the record, cleared last
-            self._clear_in_flight_record("prune", cls_name)
             print(
                 f'>> Pruned the unvalidated rows of "{cls_name}" from every shard of '
                 f'"{str(self._primary_file)}" under a "prune" record, which was cleared'
```

**(i) 02's (k): `Gadget`'s `revalidate` returns `True` without writing** (byte for byte 02's
hunk) — `FAILED (errors=5)`: `test_reconcile_at_open.TestKillAndReopen.test_validate_of_a_background_model`
(`point='C-R1'`, `'Ri-Ri+1, r0 lacks'`, `'Ri-Ri+1, r1 lacks'`) and
`TestPruningAfterRepair.test_an_interrupted_validate` (`prune=True`, `prune=False`); each reopen
raises `ReplicatedDivergence` (e.g. `class "Gadget", shard [1, 2], serial 1: … gadget_validated:
True on shard(s) [0]; False on shard(s) [1, 2]`). Before 03a this
failed nothing (log 02 §4.5 (k)). SGK: the same tests reach SGK's `BackgroundModel` factory's
`revalidate`.

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

**(j) 01's `key_id` binding** (byte for byte log 01 §4.4 (f), `SQL/ShardedPool.py:3561`) — run
three times; every run fails the new module's three tests (5 failures, with the three subtests of
`test_every_sample_is_on_the_shard_the_reopened_map_names`; `test_the_keys_were_assigned_out_of_serial_order`
fails on the `MISMATCH` lines the layer prints: `store_id=2, assigned key_serial=1`, …), and a
varying set of `test_prune_at_open` tests (§3, hazard 1):

- run 1: `FAILED (failures=6, errors=6)`; prune: `test_faulted_after_each_shard` (`after=1`),
  `test_faulted_before_the_first_shard`, `test_under_prune_unvalidated`,
  `test_a_get_record_of_a_background_model_is_repaired_not_pruned`,
  `test_a_prune_record_over_a_difference_in_another_class_refuses`,
  `test_every_shard_identical_and_no_record_left`,
  `test_the_record_stays_and_the_next_open_completes_it`;
- run 2: `FAILED (failures=6, errors=2)`; prune: `test_faulted_after_each_shard` (`after=0`),
  `test_every_shard_identical_and_no_record_left`,
  `test_the_record_stays_and_the_next_open_completes_it`;
- run 3: `FAILED (failures=6, errors=9)`; prune: `test_faulted_after_each_shard` (all three),
  `test_faulted_before_the_first_shard`, `test_under_prune_unvalidated`,
  `test_a_get_record_of_a_background_model_is_repaired_not_pruned`,
  `test_a_prune_record_over_a_difference_in_another_class_refuses`,
  `test_a_prune_with_nothing_to_prune_writes_nothing`,
  `test_every_shard_identical_and_no_record_left`,
  `test_the_record_stays_and_the_next_open_completes_it`.

SGK: no SGK counterpart of these prune tests pins it (SGK's redshifts are not its shard key); the
new module has none.

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 8d1fd81..0a6a83e 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -3558,7 +3558,7 @@ class ShardedPool:
                 # insert a new record for this key
                 result = conn.execute(
                     sqla.insert(self._shard_key_table),
-                    {"key_serial": item.store_id, "shard_id": new_shard},
+                    {"key_id": item.store_id, "shard_id": new_shard},
                 )
                 assigned_serial = result.inserted_primary_key[0]
 
```

No breakage failed nothing.

## 7. Observations not acted on

1. **The port check's blind spot.** It compares the sequence of assertion calls, not when or
   whether they run, nor what they compare. An assertion wrapped in `if False:`, put in a loop that
   runs zero times, or given other arguments, passes it; so do two calls of the same name swapped
   (the note's example pair for (o)). The review measures control flow separately; nothing here
   tries to close it.
2. **`[01-package-prose-names-sgks-layout]`, re-measured.** By the method of §8: **104 lines in
   20 files at `03fa97a`** (02's figure, reproduced), and **114 lines in 23 files after this
   prompt**. The ported modules add `test_reconcile_at_open.py` 5 (`:2`, `:9`, `:733`, `:1061`,
   `:1092`), `test_replicated_write.py` 3 (`:2`, `:6`, `:615`) and `test_prune_at_open.py` 2
   (`:2`, `:12`); the new module adds none. Their other SGK references, outside the pattern:
   `var/` (`test_prune_at_open.py:28`, `test_replicated_write.py:23`,
   `test_reconcile_at_open.py:31`); `utilities.WallclockTimer` (`test_replicated_write.py:51`);
   SGK's commit `e53f323` (`test_reconcile_at_open.py:746`, `:912`); "log 01" and "prompt 01"
   (`test_reconcile_at_open.py:11`, `:230`, `:335`; `test_replicated_write.py:618`); "the audit
   probe" (`test_replicated_write.py:410`, `test_reconcile_at_open.py:579`); `hot_journal_probe.py`
   (`test_reconcile_at_open.py:985`); "prompt 02, W3; the user's decision U1"
   (`test_prune_at_open.py:3`). The issue's measurement and hook are updated (board §3).
3. **(j) reaches `test_prune_at_open` only by chance** (§3, hazard 1): a test that must catch it is
   the new module's, which does every time.
4. **`test_reconcile_at_open.TestRecordDoesNotExplain.interrupted_tolerance_get`** keeps a name
   holding `tolerance` inside a longer identifier (it asserts, so it keeps its name). 04's guard
   matches whole identifiers, and this is not one; recorded for 04's author.
5. **`StandinCluster.open_pool` passes no `serial_batch_sizes`** (02's `build.open_pool` does), so
   the ported tests' pools lease the default batch, and a replicated get's serials depend on which
   actor controls it. The ported tests do not depend on that (they read serials back), as SGK's
   did not.

## 8. The prose measurement's method

`tokenize` over every tracked `.py` file under `datastorekit/` (`git show <rev>:<path>`, or the
tree), counting the physical lines of `COMMENT` and `STRING` tokens that match
`Datastore/|tools/|prompts/|docs/|Datastore\.(SQL|tests|replication|contract|object|shard_paths|store_reader|store_inventory)\b|repository root|REPO_ROOT|ObjectFactories|RunRegistry|main\.py|config\.defaults|utilities\.py`
(the board's pattern, with "`Datastore.<module>`" read as a module of the layer, so that
`Datastore.py` and `Datastore.set_version` do not count), with the two internalised modules'
provenance docstrings excluded. Under Python 3.12 an f-string is not a `STRING` token, so f-strings
are not read. Two rules reproduce 02's figure: a `docs/` path that exists in this repository at
that revision (the client's `docs/client-contract.md`, four lines) is this repository's and does
not count; and the comment 02 moved into the issue by hand, `tools/shard_key_audit.py:188`
(`e.g. "wavenumber"`), which the pattern does not match, does. At `8bc60a5` without the second
rule it gives 01's 101 lines in 19 files, with 01's count in every file.

## 9. Issues

- **Closed:** `[02-no-test-reaches-revalidate]` (§4; (i) fails
  `test_validate_of_a_background_model`), and `[01-no-ported-test-pins-the-shard-key-assignment]`
  (§4; (j) fails `test_shard_key_assignment`).
- **Changed:** `[01-package-prose-names-sgks-layout]`: 104 → 114 lines, 20 → 23 files (§7 item 2).
- **Opened:** none.

The index is at **6 open**: 2 on this board, 4 inherited.

## 10. State handed to the next prompt

- `HEAD` is `11247c7`. The tree is clean; `venv/` unchanged.
- The suite: **188** (`Ran 188 tests … OK`). 03b records 188 as its "before".
- `compare_ported_tests.py` exits 0 over `PORTED`'s three pairs; 03b and 04 extend `PORTED` (and
  `NAME_MAP`, for U12's four renames). `compare_with_source.py` exits 0 over 31 compared files, 3
  `PORTED`, 8 with no source; a module 03b ports joins `FILES` as `PORTED`.
- The interfaces of README §4 "After 03a": the three ported modules (03b's
  `test_one_timestamp_per_write` subclasses `test_replicated_write`'s and
  `test_reconcile_at_open`'s classes; `_PruneTestCase`, `execute` and `quiet` are importable from
  `test_prune_at_open`), and `build.make_framed_gadget` and `build.make_sample_on`.
- For 03b: the port check counts assertion calls on any receiver (§2 item 5), so its modules'
  `super().assertIdentical()`, `mock.assert_not_called()` and `unittest.TestCase().assertRaises`
  are in their skeletons.
