# Prompt 03a — port the replicated-write tests

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 02 landed (`e988e69`), and its review was recorded (`03fa97a`).
- U9–U12 are taken (README §6.2): ported tests are checked by a port-check script (U9); README
  §2's 03 is split into 03a and 03b (U10); 03b ports `test_read_only_pool` onto a neutral reader
  sequence (U11); a test name holding a client's table name changes by the table map (U12).
- `git status` is clean in this repository.

**Closes:** `[02-no-test-reaches-revalidate]` and
`[01-no-ported-test-pins-the-shard-key-assignment]` (§2.5). **Narrows:** nothing. **Changes:**
`[01-package-prose-names-sgks-layout]`, whose count grows by the ported modules' prose (§2.6).
**Opens:** only what the work finds.

**Recommended model:** **Opus**. The three modules are 2,510 lines of SGK tests written against
SGK's classes. Porting them means matching each SGK class to the neutral client's class that plays
the same role, test by test. Most of the work is judgement, checked by a script this prompt also
writes.

**Read first:**

1. [`README.md`](README.md): §0.2 (the test placement table), §1, §2 (rows 03a, 03b, 04), §4,
   §5 (rules 6, 7, 8 and 9 especially) and §6.2 (U8–U12).
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`.
3. The board, with the reviews of 01 and 02, and [`logs/02-the-neutral-test-client.md`](logs/02-the-neutral-test-client.md):
   §1.1 (the client), §1.3 (the role table), §1.4 (the entry points), §4.5 (k) and (n), §5 and §7.
4. The package as 02 left it: `datastorekit/tests/client/`, `datastorekit/tests/standin_pool.py`,
   `datastorekit/tests/test_neutral_client.py`, `docs/client-contract.md` and
   `docs/extraction/compare_with_source.py`.
5. In SGK at `6f7f291`, **read with `git -C /Users/ds283/Documents/Code/SecondaryGWKit show
   6f7f291:<path>`**, never from SGK's working tree: `Datastore/tests/test_replicated_write.py`,
   `test_reconcile_at_open.py`, `test_prune_at_open.py` and `standin_pool.py`. Read the factories
   their classes use too (`Datastore/SQL/ObjectFactories/BackgroundModel.py`, `redshift.py`,
   `wavenumber.py`), so that you know which role each class plays.

Line numbers below are at `03fa97a` for the package, and at `6f7f291` for SGK.

---

## 1. What is wanted

README §0.2 places 129 SGK tests in 03. U10 splits them:

| Prompt | SGK modules | Tests defined | Tests run |
|---|---|---|---|
| **03a (this)** | `test_replicated_write` (720 lines, 25), `test_reconcile_at_open` (1,172, 41), `test_prune_at_open` (618, 10) | 76 | 76 |
| 03b | `test_version_row_at_open` (12), `test_read_only_pool` (23), `test_one_timestamp_per_write` (1), `test_absolute_shard_record_refused` (12), `test_closed_store_refusals` (5) | 53 | 80 |

`test_one_timestamp_per_write` subclasses test classes of four modules, two of them 03a's, so 03b
follows 03a. The counts were taken by `ast` at `6f7f291`, with inherited test methods resolved.

After this prompt:
- the three modules run in `datastorekit/tests/` under their SGK names, on the stand-in pool and
  the neutral client, each test with its SGK class and method name and its assertions;
- `docs/extraction/compare_ported_tests.py` checks that, mechanically (U9), and
  `compare_with_source.py` accounts for each ported file;
- a test pins `_assign_shard_keys` so that the `key_id` binding fails it, and a ported test
  reaches `revalidate`, so that the two issues assigned to 03 close.

**No behaviour of the layer changes.** No file under `datastorekit/` outside `tests/` is touched
(README §5 rule 8). If a ported test fails on the neutral client and passing it would need a
change to the layer, that is a stop (§5).

---

## 2. What to change

### 2.1 What re-fixturing may change (README §5 rule 6, U9)

A ported test keeps its **module name, class name, method name, and assertions**. Six kinds of
change are allowed, and the log names the kind of each change, test by test:

- **R-imp**: imports. SGK's layer modules map by README §4. `Datastore.tests.standin_pool` becomes
  `datastorekit.tests.standin_pool`. `config.*` becomes `datastorekit.tests.client.registry`.
- **R-map**: an SGK table, column, payload key or drop-group name becomes its neutral counterpart
  by §2.2's map, wherever it appears in code or text: strings, SQL, dict keys, expected values,
  docstrings and comments. Afterwards **no identifier of a client's table** remains in the
  module, so that 04's vocabulary guard needs no exemption (U8, U12).
- **R-help**: a call to an SGK fixture helper (`sp.get_tolerance`, `sp.make_background_model`,
  `self.exit_time()`, …) becomes a call to its neutral counterpart. A base class's helper
  methods (`exit_time`, `background`, `unit_rows`, …) are rewritten on the neutral client.
  Helpers may be renamed. A helper that **contains an assertion** keeps its name and its
  assertions (§2.4).
- **R-value**: a payload value (a tolerance, a redshift, a wavenumber, a scale) becomes a
  neutral value that plays the same part. Two values that differ in SGK still differ, and values
  that coincide still coincide.
- **R-count**: an expected literal that counts or names what the fixture wrote (a row count, a
  list of serials, a fragment of a message naming a class or a column) is recomputed for the
  neutral fixture. The assertion that holds it does not change.
- **R-name**: a test or class name holding a client's table identifier changes by the table map
  (U12). There is none in 03a's three modules (measured at `6f7f291`), so a name that changes is
  a stop.

Nothing else changes: not control flow, not which assertion is made, not what it compares. SGK
campaign references in prose (`prompts/datastore-integrity`, `utilities.WallclockTimer`, …) stay as
they are. They are provenance, and `[01-package-prose-names-sgks-layout]` counts them (§2.6).

### 2.2 The planner's map (2026-10-07)

Measured by reading the three modules and the neutral client at `03fa97a`. **It is a check on
your reading, not a substitute for it.** For each SGK name, find what the tests use it *for*. If
a row does not hold for some test, use the neutral class that does play that role, and say so in
the log (IMPLEMENTATION CHOICE).

| SGK | What the tests use it for | Neutral |
|---|---|---|
| `tolerance` (`log10_tol`) | a replicated class a scalar get inserts | `dial_setting` (`dial_level`), `build.get_dial` |
| `redshift` (`z`; flags `source`, `response`; payload `is_source`, `is_response`) | a replicated class a vectorized get inserts, with monotone flags | `keypoint` (`kp_position`; `kp_marked`, `kp_flagged`; `marked`, `flagged`), `build.get_keypoints` |
| `wavenumber` (`k_inv_Mpc`) | the shard-key class | `keypoint`, `build.get_keypoint` |
| `wavenumber_exit_time` (`z_exit`) | a replicated proxy of the shard key, stored, which a replica inserts or verifies by serial | `keypoint_alias` (`ka_offset`), `build.make_alias` and `object_store` |
| `IntegrationSolver`, `LambdaCDM`, `QCD_Cosmology` | the replicated parents a background model is written on | `dial_setting` and `knob_setting`, as a `Gadget`'s frame |
| `BackgroundModel` (`validated`, the value count) | the replicated owner: tagged, with values, `validated_column`, `revalidate`, `owned_serials`, pruned at startup | `Gadget` (`gadget_validated`, `part_count`), `build.make_gadget`, `store_gadget` |
| `BackgroundModel_tags` (`model_serial`, `tag_serial`) | its tag table | `Gadget_tags` (`gadget_serial`, `tag_serial`) |
| `BackgroundModelValue` (`model_serial`) | its owned value table | `GadgetPart` (`gadget_serial`) |
| `GkSourcePolicy` | a replicated class a get inserts, dropped by a drop action (`TestPruningAfterRepair` only) | `keypoint_alias`, `build.get_alias` |
| `GkSourcePolicyData` | a sharded class, stored | `Sample`, `build.make_sample` and `store_sample` |
| `GkSource`, `TkNumericIntegration` | sharded classes that prune at startup, in the actor | `Sample` |
| drop actions `gk-source`, `gk-source-policy-records`, `gk-source-policy`, `quad-source-integral` | a drop of a replicated table, with its dependents | `samples`, `aliases`, `tesserae` (`aliases`' dependents are `Tessera` and `Sample` and its tables: `dependent_tables`, log 02 §2 item 3) |
| `sp.make_units`, `sp.StandinCosmology` | SGK's units and cosmology | none needed |

`version` and `store_tag` are the layer's, and keep their names.

**Three hazards the planner saw.** Check each, and say in the log what you found:
1. **`keypoint` is both the shard key and the flagged class.** A get of keypoints reaches
   `_assign_shard_keys` (`SQL/ShardedPool.py:687`, `:3246`) and writes the primary's
   `shard_keys`. SGK's get of `redshift` writes nothing there. A test that checksums the primary,
   counts calls, or lists what a write touched across such a get may see the difference. Resolve
   it without changing an assertion: for example, get the keypoints before the measured window,
   as a test's setup. If that cannot be done, stop.
2. **Two SGK classes map to one neutral class**: `wavenumber` and `redshift` both to `keypoint`;
   `wavenumber_exit_time` and `GkSourcePolicy` both to `keypoint_alias`. A set or list of tables
   in a test (for example `written` in `TestCleanWrite.test_every_copy_is_row_identical`) then
   holds one name where SGK's held two. That is R-map. A test whose meaning depends on the two
   being different classes is a stop.
3. **`TestPruneFailsInTheFactory`** relies on the factory catching its own `SQLAlchemyError`,
   and on deleting values and tags before the owner. `Gadget_factory.validate_on_startup`
   (`tests/client/factories.py:761-799`) does both, in that order.

### 2.3 The three modules

Port each module to `datastorekit/tests/<same name>.py`. Every test class and test method of
the SGK module is in the package module under its name. Module-level helpers (`quiet`,
`execute`, `REPLICATED`, `KEYS`, `UNIT`, `SimulatedDeath`, the datetime stand-ins) keep their names
where they still exist.

**The neutral client is not changed, except by additions to `tests/client/build.py`:**
- **What may be added:** a new helper, or a new keyword argument with a default that keeps the
  current behaviour. An example is a `scale` for `make_gadget`'s part values.
- **What may not change:** existing behaviour, signatures and constants. Nothing in
  `objects.py`, `factories.py` or `registry.py` changes.
- **Afterwards:** 02's 19 tests pass unchanged.
- **If a test needs a class, column or registry entry the client lacks, stop.**

`standin_pool.py` does not change: it is D-split's, and any change to it fails the check.

### 2.4 The port check, `docs/extraction/compare_ported_tests.py` (U9)

A script, run from the repository root with the venv's interpreter, like `compare_with_source.py`.
It reads each SGK source with `git show 6f7f291:<path>`, and each package module from the tree.
It writes nothing. It exits 0 when every module passes, 1 otherwise, and 2 when it cannot run.

**Its table.** `PORTED = [(SGK path, package path), …]` names the three modules. 03b and 04
extend it. `NAME_MAP` holds the R-name changes (empty in 03a). Nothing else is configurable.

**Per module, it requires:**
1. **The names.** The set of `Class.method` of every test method (a method named `test*` of a
   class) equals SGK's, after `NAME_MAP`. Each test class has the same bases, by name.
2. **The assertion skeleton.** Every function or method of the SGK module that contains an
   assertion exists in the package module under the same qualified name. Its *skeleton* is the
   ordered list, by an `ast` walk in source order, of:
   - each call `self.<name>(…)` or `<name>(…)` whose name begins with `assert` or `fail`, whether
     or not it is used as a context manager;
   - each `raise AssertionError`;
   - each `self.subTest`.

   The skeleton is equal to SGK's. Arguments are not compared, and neither is anything else. So
   a test may change *what* it passes to `assertEqual`, but not whether it calls `assertEqual`
   there.
3. **Nothing added that asserts.** A function of the package module that is not in the SGK
   module may not contain an assertion, so that a new helper cannot hide a changed one.

**Its output**, per module:
- the counts of tests, of functions compared and of assertions;
- each difference, naming the qualified name and the first position where the skeletons differ;
- a final `OK` or `FAIL` line.

**`compare_with_source.py`** gains a third kind beside `MODULE` and `SPLIT`:
- `PORTED`: an entry `(SGK path, package path, PORTED)` in `FILES`. The check requires that the
  source exists at the import commit and the package file exists, and does not compare their
  lines. It reports each as "ported: checked by compare_ported_tests.py", and counts PORTED
  files in its summary.
- The three modules join `FILES` as `PORTED`. §2.5's new module joins `NO_SOURCE`.
- An unaccounted file still fails.
- The script's docstring describes the new kind.
- 01's and 02's rules and counts do not change.

### 2.5 The two issues

**`[02-no-test-reaches-revalidate]`.** `TestKillAndReopen.test_validate_of_a_background_model`
(SGK `test_reconcile_at_open.py:486`) interrupts a validate of the replicated owner, and expects
`"validated recomputed"` actions. On `Gadget`, it reaches `Gadget_factory.revalidate` through
`_recompute_validated` (`SQL/ShardedPool.py:1992`). Replay 02's breakage (k) (log 02 §4.5) and
name the tests it now fails. If none fails, stop. Close the issue: move it to the board's §4
with a dated "Closed" line naming the test and the breakage.

**`[01-no-ported-test-pins-the-shard-key-assignment]`.** None of the 76 compares the shard map
saved on disk with the one in memory after a reopen. Two tests touch `_assign_shard_keys`:
SGK `test_reconcile_at_open.py:332-343` (its self-heal) and `:553-566` (a death inside it).
Neither would see the `key_id` binding, for the reason log 02 §4.5 (n) gives: SQLAlchemy drops
the unknown `key_id` parameter, `key_serial` autoincrements, and keys assigned in serial order
from 1 hide the difference.

So add **one new module**, `datastorekit/tests/test_shard_key_assignment.py` (not a port; name its
tests by what they show). It:
- writes keypoints through the stand-in pool so that **the order in which shard keys are
  assigned differs from the order of the keypoints' serials**, or so that the serials do not
  start at 1. Choose how, and say why it works;
- closes the pool, and reads the primary's `shard_keys` table (`key_serial`, `shard_id`) with
  `standin_pool._read`;
- requires that it equals the reopened pool's `_shard_keys` map, and the map the pool held
  before closing;
- requires that every `Sample` written before closing is found on the shard the map names, after
  the reopen.

01's `key_id` diff (log 01 §4.4, `SQL/ShardedPool.py:3561`) must fail it. Close the issue the
same way, naming the test.

### 2.6 The records

- Board §3/§4 and `docs/OPEN_ISSUES.md` for the two closed issues.
- `[01-package-prose-names-sgks-layout]`: re-measure its pattern (board §3) over the package,
  and record the new count and the lines the three ported modules add. Update its index hook.
- `docs/OPEN_ISSUES.md`: the header count (8 now; 6 after the two closures, unless the work
  opens anything).

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s datastorekit/tests -t .` gives `Ran N tests … OK`,
   where N is 109 + 76 + the new module's tests. The 109 are still there, by name.
2. `compare_ported_tests.py` exits 0. Its whole output goes in the log.
3. `compare_with_source.py` exits 0, with the three files as PORTED and the new module as
   NO_SOURCE. Its whole output goes in the log. The counts for 01's and 02's files are
   unchanged.
4. `grep -nwE` for every table name in the three clients' registries (log 02 §1.2's list) finds
   none in the three ported modules or the new one. `version` and `store_tag` are the layer's.
5. **The breakage record.** Each item is a diff exactly as applied, with what failed. None is
   committed.
   - **The checks:**
     - (a) one assertion deleted from a ported test (for example the last `assertNoRecord()` in
       `TestCleanWrite.test_a_get_that_inserts_nothing_replicates_nothing`):
       `compare_ported_tests.py` exits 1, naming the test;
     - (b) a ported test renamed: it exits 1;
     - (c) `assertEqual` replaced by `assertTrue` inside a custom assertion helper (for example
       `_PoolTestCase.assertNoRecord`): it exits 1;
     - (d) a new helper holding an `assertEqual`, called from a ported test in place of an
       inline assertion: it exits 1;
     - (e) one ported module deleted: `compare_with_source.py` exits 1.
   - **The layer, through the ported tests:**
     - (f) the refusal of a write over a set record (`SQL/ShardedPool.py:3097`, the `raise
       ReplicationInFlight`) made a `pass`: a `TestWriteOverASetRecord` test fails;
     - (g) the monotone-flag repair (`SQL/ShardedPool.py:1938-1945`) made to set nothing: a
       `test_reconcile_at_open` test fails;
     - (h) the prune's record left in place (`SQL/ShardedPool.py:2341`, the
       `_clear_in_flight_record("prune", cls_name)` removed): a `test_prune_at_open` test fails;
     - (i) 02's (k), `Gadget`'s `revalidate` returning without writing: a ported test fails
       (§2.5);
     - (j) 01's `key_id` binding: the new module fails (§2.5).
   - For (f)–(j), name every test that fails, and say whether its SGK counterpart pins the
     same line. A mutation that fails nothing is a finding: open a §3 issue for it.
6. `black --check` (25.1.0) is clean on everything under `datastorekit/` and `docs/extraction/`.

---

## 4. Acceptance

1. The three modules are ported under their names, and `compare_ported_tests.py` passes on them.
2. `[02-no-test-reaches-revalidate]` and `[01-no-ported-test-pins-the-shard-key-assignment]` are
   closed, each by a test that a named breakage fails.
3. §3.1–§3.6 hold.
4. **The records**, in the same commit:
   - the log, `logs/03a-port-the-replicated-write-tests.md`, per README §5.1. It also has:
     - **the port table:** one row per ported test (76), giving its SGK origin (module, class,
       method), the kinds of change (§2.1) made to it, and the SGK classes it uses with their
       neutral counterparts;
     - the map as used (§2.2), with each row the agent changed and why;
     - what the agent found for each of §2.2's three hazards;
     - the helpers added to `build.py`, with signatures;
     - both checks' whole output;
     - the test count before (109) and after, with the new tests named;
   - the board: §1's row for 03a and the header; §3 and §4 per §2.6;
   - `docs/OPEN_ISSUES.md`, per §2.6;
   - `prompts/INDEX.md`: the campaign's line.

---

## 5. Stop conditions — stop and ask the user

- A ported test would need an assertion removed, replaced or added, a name changed, or its control
  flow changed. This includes a test that cannot be expressed on the neutral client: rule 6 says it
  is recorded, not dropped, and the user decides.
- A test needs a class, column or registry entry the neutral client lacks (§2.3).
- A ported test fails on the neutral client, and passing it would need a change to the layer.
  That may be a real defect: record what fails, and ask.
- A breakage of §3.5 (i) or (j) fails nothing.
- `compare_with_source.py` or the stand-in pool would need a change outside §2.4.
- Anything would start Ray, open a store outside a `tempfile` directory, or edit, run or open a
  store of SGK, ChamPBH or StochasticInstantons. Reading their files through `git show` is the
  only access allowed.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `datastorekit/tests/test_replicated_write.py`, `test_reconcile_at_open.py`,
    `test_prune_at_open.py` (ported) and `test_shard_key_assignment.py` (new);
  - `datastorekit/tests/client/build.py`, by addition only;
  - `docs/extraction/compare_ported_tests.py` (new) and `docs/extraction/compare_with_source.py`;
  - the log, this board, `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.
- No file under `datastorekit/` outside `tests/` changes, and neither does `standin_pool.py`,
  the rest of `tests/client/`, `test_neutral_client.py`, `PROVENANCE.md`, `pyproject.toml` or the
  repository's `README.md`.
- It ports none of 03b's or 04's modules.
- It fixes nothing in the layer, including the four inherited issues, the bare `KeyError` of
  `[02-an-unsupplied-sharded-table-raises-keyerror]`, and anything a ported test reveals.
- It writes no orchestration note and makes no tag.

---

## 7. The log and the board

`logs/03a-port-the-replicated-write-tests.md`, using README §5.1, with the additions of §4.4.

`IMPLEMENTATION_STATE.md`: §1's row for 03a (landed, commit, log), the header, §3 and §4.
