# Prompt 03b — port the open and read-only tests

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 03a landed (`11247c7`), and its review was recorded (`e35ade2`).
- U9–U13 are taken (README §6.2). U13 (2026-10-07): this prompt adds two replicated classes to
  the neutral client (§2.3).
- `git status` is clean in this repository.

**Closes:** nothing. **Narrows:** nothing. **Changes:** `[01-package-prose-names-sgks-layout]`,
whose count grows by the ported modules' prose (§2.7). **Opens:** only what the work finds.

**Recommended model:** **Opus**. Four of the five modules port almost mechanically. The fifth,
`test_read_only_pool` (909 lines), imports SGK's audit probe for its store and its reader's lookup
sequence. U11 replaces both with a neutral store and a neutral sequence, which this prompt
designs, and the test's outcome strings are recomputed for it.

**Read first:**

1. [`README.md`](README.md): §0.2, §2 (rows 03b and 04), §4, §5 (rules 6–9 especially) and §6.2
   (U8–U13).
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`.
3. The board, with the reviews of 02 and 03a; [`logs/02-the-neutral-test-client.md`](logs/02-the-neutral-test-client.md)
   §1.1–§1.4; [`logs/03a-port-the-replicated-write-tests.md`](logs/03a-port-the-replicated-write-tests.md)
   §1.1–§1.5, §2, §3, §7, §8 and §10.
4. The package as 03a left it:
   - `datastorekit/tests/client/` (all of it) and `datastorekit/tests/standin_pool.py`;
   - `datastorekit/tests/test_neutral_client.py`;
   - the three ported modules, `test_replicated_write`, `test_reconcile_at_open` and
     `test_prune_at_open`;
   - `docs/client-contract.md`, `docs/extraction/compare_ported_tests.py` and
     `docs/extraction/compare_with_source.py`.
5. In SGK at `6f7f291`, **read with `git -C /Users/ds283/Documents/Code/SecondaryGWKit show
   6f7f291:<path>`**, never from SGK's working tree:
   - the five modules, under `Datastore/tests/`: `test_version_row_at_open.py`,
     `test_read_only_pool.py`, `test_one_timestamp_per_write.py`,
     `test_absolute_shard_record_refused.py` and `test_closed_store_refusals.py`;
   - `docs/a3-v2-readiness/reader_writes_probe.py`, the probe `test_read_only_pool` imports
     (`build_full_store` at `:347`, `qsi_sequence` at `:454`, `other_sharded_lookups` at `:651`,
     and the instrument `ReplicatedWriteLog`, `Step` and `Recorder` at `:220-340`);
   - `Datastore/SQL/ObjectFactories/GkSourcePolicy.py` and `config/sharding.py`, for the roles
     of `GkSourcePolicy` and `OneLoopIntegral`.

Line numbers below are at `e35ade2` for the package, and at `6f7f291` for SGK.

---

## 1. What is wanted

U10 gave 03b the second half of §0.2's 129 write-path tests:

| SGK module | Lines | Tests defined | Tests run |
|---|---|---|---|
| `test_version_row_at_open` | 634 | 12 | 12 |
| `test_read_only_pool` | 909 | 23 | 23 |
| `test_one_timestamp_per_write` | 169 | 1 | 28 |
| `test_absolute_shard_record_refused` | 189 | 12 | 12 |
| `test_closed_store_refusals` | 169 | 5 | 5 |
| **total** | 2,070 | **53** | **80** |

The counts were taken by `ast` at `6f7f291`, with inherited test methods resolved.
`test_one_timestamp_per_write` defines one test and inherits 27, all under a ticking clock:
- from 03a's modules: `TestKillAndReopen` (12), `TestPruningAfterRepair` (2),
  `TestInterruptedPrune` (2) and `TestUninterruptedPrune` (3);
- from `test_version_row_at_open`: `TestNewStore` (3), `TestNewLabelInterrupted` (4) and
  `TestNewStoreInterrupted` (1).

After this prompt:
- the five modules run in `datastorekit/tests/` under their SGK names, on the stand-in pool and
  the neutral client. Each test keeps its SGK class and method name, except U12's four renames,
  and keeps its assertions;
- `compare_ported_tests.py` checks the five, with U12's renames in `NAME_MAP`, and
  `compare_with_source.py` accounts for each as `PORTED`;
- the neutral client has two more replicated classes (U13, §2.3), and
  `datastorekit/tests/client/reader.py` holds the neutral store, reader sequence and instrument
  that `test_read_only_pool` runs (U11, §2.4);
- the suite is **268**: 188 + 80.

**No behaviour of the layer changes.** No file under `datastorekit/` outside `tests/` is touched
(README §5 rule 8). If a ported test fails on the neutral client and passing it would need a
change to the layer, that is a stop (§5).

---

## 2. What to change

### 2.1 What re-fixturing may change

03a §2.1 governs unchanged: the kinds R-imp, R-map, R-help, R-value, R-count and R-name, and
nothing else. Read it there. Three points are particular to 03b:

- **R-name applies to four tests** (U12), all in `test_read_only_pool`'s
  `TestEachMissRaisesReadOnlyMiss`, by §2.2's map:
  - `test_LambdaCDM` → `test_dial_setting`;
  - `test_QCD_Cosmology` → `test_knob_setting`;
  - `test_tolerance` → `test_gauge_setting`;
  - `test_GkSourcePolicy` → `test_routing_rule`.

  No other name changes. `MESSAGES`' keys (`MESSAGES["LambdaCDM"]`, …) are R-map.
- **A docstring or comment that describes a fixture R-help replaced** may be rewritten to describe
  the replacement, and only those sentences. This covers `test_read_only_pool`'s module docstring
  on the probe (`:5-10`) and `_load_probe`'s comment. The log quotes each sentence before and
  after. Every other piece of prose follows 03a §2.1: SGK campaign references, SGK line numbers in
  prose and "audit R2" stay.
- **Dotted module paths in strings** are R-imp. An example is `mock.patch("Datastore.SQL.ShardedPool.sqlite3.connect", …)`
  (`test_read_only_pool.py:882`), which becomes `"datastorekit.SQL.ShardedPool.sqlite3.connect"`.

### 2.2 The map

**In 03b's five modules**, by role:

| SGK | What the tests use it for | Neutral |
|---|---|---|
| `tolerance` (`log10_tol`) | an unversioned replicated leaf a get inserts; four per reader frame in the sequence; the unversioned insert of `TestInsertBeforeSetVersion` | **`gauge_setting`** (`gauge_exponent`), new (§2.3), `build.get_gauge` |
| `GkSourcePolicy` (`label`, `Levin_threshold`, `numeric_policy`) | a **versioned** replicated class a get inserts | **`routing_rule`** (`rule_label`, `rule_threshold`, `rule_mode`), new (§2.3), `build.get_rule` |
| `LambdaCDM` | a cosmology that has a validated background model: the sequence's first frame | `dial_setting`: `build_store`'s validated `gadget-one` is on a dial frame |
| `QCD_Cosmology` | a cosmology with no validated model: where the sequence stops | `knob_setting`: `gadget-two` is on a knob frame, unvalidated |
| `wavenumber` (`k_inv_Mpc`; flags `is_source`, `is_response`) | the shard-key class, read by `read_table`, and got as a new shard key | `keypoint` (`kp_position`; `kp_marked`, `kp_flagged`) |
| `redshift` | a flagged leaf read by `read_table`; the backstop's flag update on a hit | `keypoint` |
| `wavenumber_exit_time` | the stored proxy, got by a hit or stored | `keypoint_alias`, `build.make_alias` / `get_alias` |
| `BackgroundModel` | the replicated owner: got (a hit or not), validated, pruned | `Gadget`, `build.get_gadget` / `make_framed_gadget` |
| `GkSourcePolicyData` | a sharded versioned class, stored | `Sample`, `build.make_sample_on` |
| `GkSource` (validates), `OneLoopIntegral` (does not) | two sharded tables a shard may lack | `Sample` (validates), `Tessera` (does not) |
| `GkNumericValue` | a sharded class a vectorized get inserts into | `Tessera`, `object_get_vectorized` |
| `QuadSourcePolicy`, `QuadSource`, `QuadSourceIntegral`, `GkSource` (the probe's) | the sequence's further reads, each a hit or a miss that inserts nothing | §2.4 |
| `config.defaults.DEFAULT_*_TOLERANCE`, `Planck2018`, `run_label_tag` | SGK's values and labels | constants of `client/reader.py` (§2.4), or literals |

**This map differs from 03a's in one row.** 03a maps `tolerance` to `dial_setting`. Here
`dial_setting` is the first frame, and U12's four test names must map to four different names,
so `tolerance` → `gauge_setting` in **all five** modules. 03a's modules are not changed.
`test_one_timestamp_per_write` inherits 03a's classes with 03a's map, and that is correct.

`version` and `store_tag` are the layer's, and keep their names. `sp.StandinSerial` →
`objects.SerialHandle` (log 02 §1.3). `sp.make_units` and `self.units` go, as in 03a.

**Hazards the planner saw.** Check each, and say in the log what you found.
1. **The ticking clock over 03a's classes.** `test_one_timestamp_per_write` runs 19 of 03a's
   tests with `datastorekit.SQL.Datastore`'s `datetime` replaced by `_TickingDatetime`, and adds
   `assertNoShardClock` to each `assertIdentical`. The planner ran exactly that (the module's
   classes 1–4, imports rewritten, 03a's `REPLICATED`) from the scratchpad on `e35ade2`:
   `Ran 19 tests … OK`. The version-row eight inherit from your port of `test_version_row_at_open`.
2. **The version-row helpers that read `REPLICATED`.** `_VersionTickingClock.tearDown` and
   `assertNoShardClock` read `REPLICATED = reconcile_at_open.REPLICATED`. That is 03a's
   correction 1: the registry filtered on `register() is not None`, plus `Gadget_tags`. With §2.3's
   two classes it grows by two, which is right, since both have tables.
3. **The sequence must reach each deleted row, in order, through a lookup that inserts on a
   miss.** Each `TestEachMissRaisesReadOnlyMiss` test deletes the rows of one class from every
   shard, runs the sequence on a read-only pool, and requires a `ReadOnlyMiss` naming that class
   with its payload. So the sequence looks up `dial_setting` and `knob_setting` (the two frames)
   first, then `gauge_setting` and `routing_rule` per frame. It makes no other lookup that inserts
   on a miss before those. A deleted row of a class that a later step reads with no insert (a
   `read_table`) must not be reached first, or the error is not a `ReadOnlyMiss`.
4. **On the read-write run, nothing may be inserted.** `test_the_instrument_counts_…` requires
   that only the primary changes (`changed == ["store.sqlite"]`). It also requires every step's
   outcome on the read-only run to equal the read-write run's. So every replicated lookup of the
   sequence is a hit on the full store, and every sharded lookup is a hit or a miss that inserts
   nothing. A vectorized get of `Tessera` with a new weight inserts, and belongs only in
   `test_a_vectorized_get_that_reaches_an_inserter`.
5. **`keypoint` cannot be deleted for a miss test.** The read-only open refuses a primary whose
   `shard_keys` name a keypoint no shard holds, before any lookup. Probed on a `build_store`
   with keypoint 1.0 deleted from every shard: the open raises `ReplicatedDivergence` naming
   class `"shard_keys"`. That is why `tolerance` needs a class of its own.

### 2.3 The two classes (U13)

**What changes in the client.** Two replicated classes, by addition:
- **`gauge_setting`**: an object `gauge_setting(store_id, exponent)`; `register()` with
  `"version": False`, `"timestamp": True`, and one column `gauge_exponent` (`Integer`, not null).
  `build` gets by exponent and inserts on a miss, honouring a replica's `"serial"` in the payload
  as `knob_setting_factory.build` does. `inventory_spec()` is `InventorySpec(leaves=("gauge_exponent",))`.
- **`routing_rule`**: an object `routing_rule(store_id, label, threshold, mode)`; `register()`
  with `"version": True`, `"timestamp": True`, and the columns `rule_label`
  (`String(DEFAULT_STRING_LENGTH)`, not null), `rule_threshold` (`Float(64)`, not null) and
  `rule_mode` (`String(DEFAULT_STRING_LENGTH)`, not null). `build` gets by all three and inserts
  on a miss, as above. `inventory_spec()` names the three as leaves.
- **The registry:** both in `factories`, and in `replicated_tables` after `knob_setting`. Neither
  in a drop group, `read_table_config` or `serial_batch_sizes`. `__all__` is unchanged.
- **`build.py`:**
  - `get_gauge(pool, exponent)` and `get_rule(pool, label, threshold, mode)`;
  - constants `GAUGE_EXPONENTS` and `ROUTING_RULES`, which `write_every_class` writes after
    `knob_setting`, through the pool: at least two of each, so that `build_store` fills both
    tables. The sequence needs four gauges and two rules (§2.4);
  - this is the one change to an existing function of `build.py` (U13). Every other helper stays
    as it is.

The names were checked: none of `gauge_setting`, `gauge_exponent`, `routing_rule`, `rule_label`,
`rule_threshold` or `rule_mode` occurs as a word under `datastorekit/` or `docs/` at `e35ade2`, or
among log 02 §1.2's 82 registry names.

**What else follows, and nothing more:**
- `test_neutral_client.py` changes only in measured literals:
  - `KEPT` gains the two names;
  - `test_the_reader_and_the_inventory_read_every_class`'s `counts` gains their counts.

  Every other test of 02's passes unchanged. If one does not, stop.
- `docs/client-contract.md` changes only in its client columns ("Exercised by" and the like),
  where a row lists the client's classes by a property the two classes have. Examples are the
  `timestamp` row (`:68`, which says "`False` on the rest") and the `version` row (`:67`). Nothing
  about the layer changes in it.
- 03a's modules are not edited. Their `REPLICATED` picks up the two tables through the registry.
  They pass unchanged: run them, and say so.
- `objects.py`, `factories.py` and `registry.py` change by addition only.

### 2.4 The neutral store and reader sequence (U11): `datastorekit/tests/client/reader.py`

A new module, with no source, in place of SGK's probe. `test_read_only_pool` imports it as `rw`,
so that its calls keep their shape. It holds:

- **The instrument, transcribed from the probe:**
  - `file_state`, `state_delta` and `change_counter`;
  - `ReplicatedWriteLog`, which wraps `sp_mod.ShardedPool._replicated_write`, and `Step` and
    `Recorder`.

  These are generic: they read files and wrap a layer method. Keep their behaviour exactly, and
  say in the log which probe lines each came from.
- **`build_full_store(primary, cluster) -> dict`.** It writes the store the sequence reads, and
  returns its facts, keyed by the neutral class names. It opens the pool with `build.open_pool`,
  calls `build.write_every_class`, and then writes, through the pool, only what the sequence
  needs that `write_every_class` does not: four gauges, two rules, aliases enough for the alias
  step, and so on. `FACTS` and `CONTEXT` as in the probe.
- **`reader_sequence(pool, rec)`**, in place of `qsi_sequence`. The sequence keeps QSI's shape:
  1. a step that resolves the run's tag (`store_tag`, a hit);
  2. a step that gets the two frames, `dial_setting` then `knob_setting` (hits);
  3. then, for each frame in that order:
     - its four gauges;
     - its validated `Gadget`. If none is available, it raises the sequence's own `RuntimeError`,
       `"Could not locate suitable gadget instance in the datastore"`;
     - `read_table` of `keypoint`, twice with two filters;
     - the aliases of those keypoints;
     - `read_table` of `dial_setting`;
     - the two rules;
     - the sharded work items: `object_read_batch` of `Sample`, a `Sample` that is a hit, and one
       that is a miss.

   On `build_store`'s data the second frame has no validated Gadget, so the sequence stops there,
   as QSI's does at `QCD_Cosmology`.
- **`other_sharded_lookups(pool, rec)`:** two to four sharded lookups that miss and insert
  nothing. Each step records `available=…`.
- Any constant the test needs in place of SGK's (the gauge exponent standing for
  `DEFAULT_QUADRATURE_RTOL`, the rule standing for `GKSOURCE_POLICY_5PT0`, the run's tag label).

Step names are the module's own. `test_the_instrument_counts_…` then asserts what this sequence
gives, by R-count:
- `len(rw_log) == <the read-write run's count>`;
- the six `outcomes[...]` strings, each keyed by the neutral step that plays the SGK step's part
  (the Gadget hit, the two `read_table` steps, the alias step, the rules, the stored Sample);
- the `assertIn` of the stop message.

The assertion calls do not change. The log gives the step table: each neutral step, the SGK step
it stands for, and its outcome on the full store.

`reader.py` holds no assertion (03a §2.4 rule 3 is about the ported modules, but a fixture that
asserts would hide an assertion from the port check). It is pickled only by reference, as the
probe's `Proxy` was, so it defines what it passes to an actor at module level.

### 2.5 The checks

**`compare_ported_tests.py`:**
- `PORTED` gains the five pairs.
- `NAME_MAP` holds U12's four renames, under `datastorekit/tests/test_read_only_pool.py`.
- Nothing else changes. Its rule for bases compares them as written, so
  `test_one_timestamp_per_write`'s `reconcile_at_open.TestKillAndReopen` and the like compare by
  their dotted names. Its inherited tests are compared in their own modules.

**`compare_with_source.py`:**
- `FILES` gains the five as `PORTED`.
- `NO_SOURCE` gains `datastorekit/tests/client/reader.py`.
- 01's, 02's and 03a's counts do not change.

**The run count**, which neither script sees: per module, `unittest`'s loader runs 12, 23, 28,
12 and 5 tests. Verify it with `unittest.TestLoader().loadTestsFromName(...).countTestCases()`,
and put it in the log.

### 2.6 The three small modules

`test_absolute_shard_record_refused` and `test_closed_store_refusals` import only the layer, 01's
`shard_store_fixtures`, and `config.datastore.factories`. Each is R-imp, plus the fixtures'
neutral names if any expected string names a table (measured: none of the 82 names occurs in
either). `test_one_timestamp_per_write` is R-imp, plus one comment (`BackgroundModel` →
`Gadget`).

### 2.7 The records

- `[01-package-prose-names-sgks-layout]`: re-measure by log 03a §8's method, and record the new
  count and the lines the five ported modules and `reader.py` add. Update its index hook.
- `docs/OPEN_ISSUES.md`: 6 open now, and 6 after, unless the work opens an issue.

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s datastorekit/tests -t .` gives `Ran 268 tests …
   OK`. The 188 are still there by name, and 02's 19 and 03a's 79 pass with their literals as
   §2.3 allows.
2. `compare_ported_tests.py` exits 0 over eight modules. Its whole output goes in the log.
3. `compare_with_source.py` exits 0, with eight `PORTED` files and `reader.py` as no-source. Its
   whole output goes in the log.
4. The loader's run counts are 12, 23, 28, 12 and 5 (§2.5).
5. `grep -nwE` for log 02 §1.2's 80 client names (the 82 less `version` and `store_tag`) finds
   none in the five modules, `reader.py`, `build.py`, `objects.py`, `factories.py` or
   `registry.py`.
6. **The breakage record.** Each item is a diff exactly as applied, with what failed. None is
   committed.
   - **The checks:**
     - (a) one `NAME_MAP` entry removed: `compare_ported_tests.py` exits 1, naming the test;
     - (b) `_TickingClock` dropped from one class's bases in `test_one_timestamp_per_write`: it
       exits 1;
     - (c) the `assertAlmostEqual` inside `test_knob_setting`'s payload lambda deleted: it exits
       1;
     - (d) `reader.py` removed from `NO_SOURCE`: `compare_with_source.py` exits 1.
   - **The layer, through the ported tests:**
     - (e) the replicated write's timestamp ignored by the actor: `_inserters_for` returns the
       actor's own inserters whatever `insert_timestamp` is (`SQL/Datastore.py:684`). A
       `test_one_timestamp_per_write` test fails; name every test that fails;
     - (f) the refusal of an insert before `set_version` removed (`SQL/Datastore.py:718`):
       `TestInsertBeforeSetVersion` fails;
     - (g) a read-only actor's miss of a replicated class raised as `ReadOnlyWrite`, not
       `ReadOnlyMiss` (`SQL/Datastore.py:278-279`): `TestEachMissRaisesReadOnlyMiss` fails;
     - (h) `resolve_shard_path` accepting an absolute record, `_require_bare_name` bypassed for
       one (`shard_paths.py:101`): `test_absolute_shard_record_refused` fails;
     - (i) `delete_store`'s refusal stating its prefix twice (`SQL/ShardedPool.py:2932`):
       `test_closed_store_refusals` fails;
     - (j) `?mode=ro` dropped from `_find_version_row`'s connection (`SQL/ShardedPool.py:378`):
       `test_every_connection_is_opened_read_only` fails, if the read-only open reaches it. If it
       does not, pick another `mode=ro` connection on the read-only path, and say why.
   - For (e)–(j), name every test that fails, and say whether its SGK counterpart pins the same
     line. A mutation that fails nothing is a finding: open a §3 issue for it.
7. `black --check` (25.1.0) is clean on everything under `datastorekit/` and `docs/extraction/`.

---

## 4. Acceptance

1. The five modules are ported under their names, with U12's four renames, and both checks
   pass.
2. The two classes are in the client as §2.3 says, and the only other edits are those §2.3
   allows.
3. §3.1–§3.7 hold.
4. **The records**, in the same commit:
   - the log, `logs/03b-port-the-open-and-read-only-tests.md`, per README §5.1. It also has:
     - **the port table:** one row per defined test (53), giving its SGK origin, the kinds of
       change made to it, and the SGK classes it uses with their neutral counterparts; and the
       27 inherited tests, listed by the class they run under;
     - the map as used (§2.2), with each row the agent changed and why;
     - what the agent found for each of §2.2's five hazards;
     - the two classes, and every literal of `test_neutral_client.py` and line of
       `docs/client-contract.md` that changed;
     - `reader.py`'s step table (§2.4), and the probe lines the instrument came from;
     - the rewritten docstring sentences, before and after (§2.1);
     - both checks' whole output, and the loader's run counts;
     - the test count before (188) and after (268);
   - the board: §1's row for 03b and the header; §3 per §2.7;
   - `docs/OPEN_ISSUES.md`, per §2.7;
   - `prompts/INDEX.md`: the campaign's line.

---

## 5. Stop conditions — stop and ask the user

- A ported test would need an assertion removed, replaced or added, a name changed beyond
  U12's four, or its control flow changed. A test that cannot be expressed on the neutral
  client is recorded, not dropped, and the user decides.
- A test needs a class, column or registry entry beyond §2.3's two classes.
- One of 02's or 03a's tests fails with the two classes added, other than through a literal
  §2.3 names.
- A ported test fails on the neutral client, and passing it would need a change to the layer.
  That may be a real defect: record what fails, and ask.
- `compare_with_source.py`, `compare_ported_tests.py` or the stand-in pool would need a change
  outside §2.5.
- Anything would start Ray, open a store outside a `tempfile` directory, or edit, run or open a
  store of SGK, ChamPBH or StochasticInstantons. Reading their files through `git show` is the
  only access allowed. Do not import or run SGK's probe: transcribe from it.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `datastorekit/tests/test_version_row_at_open.py`, `test_read_only_pool.py`,
    `test_one_timestamp_per_write.py`, `test_absolute_shard_record_refused.py` and
    `test_closed_store_refusals.py` (ported);
  - `datastorekit/tests/client/reader.py` (new);
  - `datastorekit/tests/client/objects.py`, `factories.py`, `registry.py` and `build.py`, as
    §2.3 says;
  - `datastorekit/tests/test_neutral_client.py` and `docs/client-contract.md`, in the literals
    and lines §2.3 names;
  - `docs/extraction/compare_ported_tests.py` and `compare_with_source.py`, as §2.5 says;
  - the log, this board, `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.
- No file under `datastorekit/` outside `tests/` changes. Neither do `standin_pool.py`,
  `shard_store_fixtures.py`, 03a's three modules, `PROVENANCE.md`, `pyproject.toml` or the
  repository's `README.md`.
- It ports none of 04's modules.
- It fixes nothing in the layer, including the four inherited issues, the bare `KeyError` of
  `[02-an-unsupplied-sharded-table-raises-keyerror]`, and anything a ported test reveals.
- It writes no orchestration note and makes no tag.

---

## 7. The log and the board

`logs/03b-port-the-open-and-read-only-tests.md`, using README §5.1, with the additions of §4.4.

`IMPLEMENTATION_STATE.md`: §1's row for 03b (landed, commit, log), the header, and §3.
