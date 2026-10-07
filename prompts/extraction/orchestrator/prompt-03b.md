# Orchestrator — prompt 03b, port the open and read-only tests

Read [`../README.md`](../README.md) first: §0.2, §2 (rows 03b and 04), §4, §5 and §6.2 (U9–U13).
Then read [`prompt-03a.md`](prompt-03a.md) §0's "Conventions", which this note keeps unless it says
otherwise, and the board's review of 03a, above all its "Handed on to 03b's author".

**You do not write code.** You may:
- run the suite, both checks and the tests the log names;
- replay the log's deliberate-breakage diffs with `git apply`, and revert them;
- run an in-process check or a probe from the session scratchpad, never committing one;
- read SGK through `git -C /Users/ds283/Documents/Code/SecondaryGWKit show 6f7f291:<path>`;
- fix small residue in a follow-up commit of your own (§4).

**The prompt:** [`03b-port-the-open-and-read-only-tests.md`](../03b-port-the-open-and-read-only-tests.md)
**Closes:** nothing · **Narrows:** nothing · **Changes:** `[01-package-prose-names-sgks-layout]`
(its count) · **Opens:** only what the work finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- 03a landed (`11247c7`) and its review is recorded (`e35ade2`). 03b is written (`19adaa2`), and
  U9–U13 are taken.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- SGK's `Datastore/`, `tools/`, `utilities.py`, `config/defaults.py`, `config/sharding.py` and
  `docs/a3-v2-readiness/reader_writes_probe.py` are unchanged from `6f7f291` to SGK `HEAD`
  (`b510bc9`, 2026-10-07). The prompt reads SGK at `6f7f291` regardless.
- One prompt at a time in this checkout. 04 is not written; it must not run beside 03b
  (README §2, "Order").

## 0. What makes this prompt unusual

**It has three parts of different kinds, and the review weighs them differently.**
- **Four modules port almost mechanically.** `test_absolute_shard_record_refused` and
  `test_closed_store_refusals` name no client table. `test_one_timestamp_per_write` defines one test
  and runs 27 more by inheriting 03a's classes and `test_version_row_at_open`'s.
  `test_version_row_at_open` needs one new role, a versioned replicated class a get inserts.
- **One module's fixture is designed, not ported.** `test_read_only_pool` ran SGK's probe: its
  store, QSI's lookup sequence and the outcomes SGK's audit recorded. Under U11 the store, the
  sequence and the outcome strings are new (`client/reader.py`). The port check sees none of
  this, since the assertions stay and only their literals change. So the review measures the
  sequence itself: what each step looks up, in what order, and what it gives on the full store.
- **The neutral client changes for the first time since 02** (U13). Two classes are added by
  addition. The change reaches 02's tests, the contract document and, through `REPLICATED`, every
  module of 03a. The review checks that the ripple is confined to the literals §2.3 names.

**What moves on purpose:**
- five ported modules and `client/reader.py` (new) under `datastorekit/tests/`;
- additions to `client/objects.py`, `factories.py`, `registry.py` and `build.py`, with the one
  change to `write_every_class`;
- two literals of `test_neutral_client.py`, and client columns of `docs/client-contract.md`;
- `PORTED`, `NAME_MAP`, `FILES` and `NO_SOURCE` in the two checks;
- the records.

Nothing under `datastorekit/` outside `tests/` changes. Neither do `standin_pool.py`,
`shard_store_fixtures.py` or 03a's four modules.

**Correction to the prompt**, checked by the orchestrator on 2026-10-07 at `19adaa2` (package
files as at `e35ade2`, unchanged since) and SGK `6f7f291`. Pass it on. It is STRUCTURALLY REQUIRED,
and the log says so.

1. **The instrument needs `table_counts` as well.** §2.4 lists `file_state`, `state_delta` and
   `change_counter`, then `ReplicatedWriteLog`, `Step` and `Recorder`. But `file_state` (probe
   `:149-159`) calls `table_counts` (`:139-146`) for every `.sqlite` file, and `Step` records its
   delta. So `table_counts` is transcribed too, reading through `standin_pool._read` as the probe
   does.

   `Recorder.print` (`:313-340`) uses two more helpers, `describe_delta` (`:194`) and
   `summarise_writes` (`:264`). `test_read_only_pool` never calls `print`. So the agent either
   transcribes `print` with both helpers, or leaves all three out. The log says which, and it is
   an IMPLEMENTATION CHOICE.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **(p), the bases are compared as written.** In `test_one_timestamp_per_write`, write one class's
  base by a direct import (for example `from datastorekit.tests.test_reconcile_at_open import
  TestKillAndReopen`, then `class TestRepairAtOpen(_TickingClock, TestKillAndReopen)`):
  `compare_ported_tests.py` exits 1, naming the class. Record it with (a)–(d). The port keeps SGK's
  module aliases (`reconcile_at_open`, `prune_at_open`, `replicated_write`, `version_row_at_open`),
  so that its bases read as SGK's do. This is the hand-on from 03a's review: the check compares a
  cross-module base by its dotted name, and this shows that it does.
- **A second vocabulary grep, for what §3.5 cannot see.** §3.5 greps for table names. SGK's
  modules also import client modules and use client keywords, and some imports are inside test
  bodies:
  - modules: `CosmologyModels`, `CosmologyConcepts`, `ComputeTargets`, `extract_common` and
    `config.` (`config.datastore`, `config.defaults`, `config.sharding`);
  - keywords and constants: `Planck2018`, `DEFAULT_[A-Z_]*TOL`, `k_inv_Mpc`, `log10_tol`,
    `log10_max_z`, `Levin_threshold`, `numeric_policy`, `is_source`, `is_response` and `units`
    as a keyword.

  The log gives `grep -nwE` for these over the five modules and `reader.py`. Each hit is either
  prose ported unchanged (03a §2.1) or a finding.
- **Keep what a version-row test writes.** In `TestNewStore.test_versioned_rows_carry_the_serial_on_every_shard`
  (SGK `:236`), SGK gets two tolerances (`1.0e-10`, `1.0e-9`) and builds its exit time from them.
  The neutral alias takes no gauge. Keep the two `get_gauge` calls anyway, with distinct
  exponents (R-value). They are the test's unversioned replicated inserts, and
  `TestVersionRowOfANewStore` checks them under the ticking clock. The log says where each one
  went.
- **`_load_probe` goes.** `reader.py` is importable as `datastorekit.tests.client.reader`, so
  `rw = _load_probe()`, `REPO_ROOT`, `PROBE` and `_load_probe` (`test_read_only_pool.py:64-78`)
  become `from datastorekit.tests.client import reader as rw` (R-help). A plain import pickles by
  reference, as the probe's registration under `sys.modules` was meant to. §2.1's allowance for
  `_load_probe`'s comment then has nothing to rewrite, and the log says so. If the agent keeps a
  loader, it says why.

**The facts, checked by the orchestrator.** Pass them on.

- **The prompt's survey holds** at `19adaa2` and SGK `6f7f291`:
  - module lengths 634, 909, 169, 189 and 169; the probe 890;
  - tests by `ast`, per class in file order:
    - `test_version_row_at_open`: 12 (3, 4, 1, 2, 1, 1);
    - `test_read_only_pool`: 23 (2, 5, 7, 9);
    - `test_absolute_shard_record_refused`: 12 (2, 10);
    - `test_closed_store_refusals`: 5 (4, 1);
    - `test_one_timestamp_per_write`: 1, defined in `TestVersionRowOfANewStore`. Its name,
      `test_the_version_row_is_its_serial_and_label`, overrides none of `TestNewStore`'s three. So
      28 run.
  - The package's line numbers for (e)–(j) hold:
    - (e) `SQL/Datastore.py:684` is `if insert_timestamp is None:`. The read-only
      short-circuit at `:682-683` comes before it, and the mutation leaves that alone;
    - (f) `:718`;
    - (g) `:278-279`;
    - (h) `shard_paths.py:101`;
    - (i) `SQL/ShardedPool.py:2932`;
    - (j) `:378`. The read-only open reaches it through `_find_version_row` (`:529`, step 5 of the
      read-only open), so (j) is the prompt's first choice.
  - `docs/client-contract.md:67-68` are the `version` and `timestamp` rows. Their client column
    lists the classes by name. The `inventory_spec()` row (`:98`) and the contract's other client
    columns are the agent's to check.
  - `test_neutral_client.py:87` is `KEPT`. `:520-534` is the `counts` literal.
  - None of the six new names occurs as a word under `datastorekit/` or `docs/`.
- **The probe**, for the transcription, at `6f7f291`:

  | Item | Probe lines |
  |---|---|
  | `change_counter` | `:133` |
  | `table_counts` | `:139` |
  | `file_state` | `:149` |
  | `state_delta` | `:162` |
  | `describe_delta` | `:194` |
  | `ReplicatedWriteLog` | `:220` |
  | `summarise_writes` | `:264` |
  | `Step` | `:279` |
  | `Recorder` | `:303` |
  | `build_full_store` | `:347` |
  | `qsi_sequence` | `:454` |
  | `CONTEXT`, `FACTS` | `:647-648` |
  | `other_sharded_lookups` | `:651` |

  SGK's full store holds eight tolerances (`ALL_TOLERANCES`, `:76-85`). QSI's four per frame are
  the two `HEXIT` and the two `QUADRATURE` ones (`:471-474`).
- **R-map's size.** These are the lines of SGK's five modules that hold one of the 80 client names
  as whole words: `test_version_row_at_open` 12, `test_read_only_pool` 55,
  `test_one_timestamp_per_write` 1 (the comment at `:43`), and the two small modules 0.

  Counted as occurrences, by name: `GkSourcePolicy` 15, `LambdaCDM` 12, `tolerance` 10,
  `BackgroundModel` 9, `wavenumber` 8, `redshift` 6, `QCD_Cosmology` 6, `wavenumber_exit_time`
  5, `GkSourcePolicyData` 5, `GkNumericValue` 2, `OneLoopIntegral` 1, `GkSource` 1.

  `test_read_only_pool`'s module docstring names four of them (`:21-22`). That is R-map, not
  §2.1's rewrite.
- **Hazard 1 holds, re-run.** SGK's `test_one_timestamp_per_write.py:1-119` was run from the
  scratchpad on `19adaa2`, with the imports rewritten and the version-row module left out:
  `Ran 19 tests … OK`.
- **Hazard 2.** Both new classes register `"timestamp": True`, so `assertNoShardClock` reads them,
  and `_VersionTickingClock.tearDown` compares them whole on every shard. Each version-row store
  builds every table from the registry, so both tables exist there.
- **Hazards 3 and 4, probed on a read-only `build_store`.**
  - **The miss payload is the inserter's row, keyed by column name.** It is not the get's
    keywords. A get of the first frame with every `dial_setting` row deleted raises `ReadOnlyMiss`
    with `payload == {'dial_level': 3, 'stepping': 1}`. The same for `knob_setting` gives
    `{'knob_turns': 7, 'stepping': 2}`. So SGK's `payload["name"]`, `["log10_max_z"]`,
    `["log10_tol"]` and `["label"]` map to column names: `dial_level`, `knob_turns` (with the
    payload's other key, `stepping`, for the lambda's second assertion), `gauge_exponent` and
    `rule_label`. The
    `store_tag` payload is the layer's. No file changed.
  - **Gadget.** `Gadget_factory.build` (`factories.py:588-611`) returns only a validated Gadget,
    and otherwise an unstored one. `gadget-one` (on the dial frame) is available with serial 1, and
    `gadget-two` (on the knob frame) is not. Test it with `.available`: `.store_id` of an unstored
    object raises `RuntimeError`, which `run_sequence` would take for the sequence's own stop.
  - **Sample.** A get of `Sample` that misses inserts nothing (`factories.py:1010-1031`).
  - **Every gauge any read-only test gets must be in the full store**, or the get is a
    `ReadOnlyMiss`. That is the sequence's four, and also whatever stands for SGK's `exit_time`
    helper's two (`HEXIT`, among QSI's four), and `test_a_replicated_get_is_one_call_to_the_drawn_shard`'s.
- **Hazard 5 holds, probed.** A `build_store` with keypoint 1.0 deleted from every shard: the
  read-only open raises `ReplicatedDivergence`, and no file changes.
- **`keypoint` can play both of its write roles, probed** on a read-only `build_store`:
  - the backstop: a get of keypoint 1.0 with `flagged=True` raises `ReadOnlyWrite` naming
    `keypoint` and `shard0000-store`, "SQLite refused the write…";
  - a new shard key: a keypoint got on a read-write pool, then its `shard_keys` row deleted. The
    read-only open passes, and the get raises `ReadOnlyWrite` "assigning a shard key of
    `keypoint`".

  No file changed in either.
- **The absent-table tests hold, probed.** `DROP TABLE "Sample"`, and separately `"Tessera"`, on
  shard 1 of a `build_store`, then a read-only open. It raises `StoreSchemaMismatch` with
  `absent_tables == (<the table>,)`. No actor call is made, and no file changes. `Sample`
  validates at startup and `Tessera` does not, as the map says.
- **A trap in `test_every_connection_is_opened_read_only`.** It patches
  `"datastorekit.SQL.ShardedPool.sqlite3.connect"`. That sets `connect` on the shared `sqlite3`
  module, so every connection made during the run is recorded and must be `mode=ro`, including
  the instrument's and the sequence's own. Read files only through `standin_pool._read` (which
  opens `mode=ro`) or the pool, as the probe does.
- **The port check, applied to SGK's five** with its own functions and an empty name map, gives
  these counts. After R-name, the package side must give the same:

  | Module | Tests | Classes | Functions compared | Assertions |
  |---|---|---|---|---|
  | `test_version_row_at_open` | 12 | 7 | 16 | 79 |
  | `test_read_only_pool` | 23 | 5 | 27 | 138 |
  | `test_one_timestamp_per_write` | 1 | 9 | 5 | 7 |
  | `test_absolute_shard_record_refused` | 12 | 3 | 14 | 28 |
  | `test_closed_store_refusals` | 5 | 3 | 7 | 21 |

  - The skeleton counts a call to any name beginning `assert`, so `assert_miss` and
    `assert_refused` are in it. `test_QCD_Cosmology`'s skeleton is `assert_miss, assertEqual,
    assertAlmostEqual`, the last two from the lambda, so (c) bites.
  - `NAME_MAP`'s renaming applies to every name segment: classes, methods, nested functions and
    the parts of a base.
- **The toolchain.** `venv/` from 01: Python 3.12.15, `ray==2.43.0`, `sqlalchemy==2.0.39`,
  `black==25.1.0`, the package installed editable. It needs no change.
- **Expected counts.**
  - The suite is **188** before (`Ran 188 tests … OK`, re-run by the orchestrator at `19adaa2`),
    and **268** after.
  - `compare_with_source.py` exits 0 before, with 31 files compared, 3 `PORTED` and 8 with no
    source (42 tracked `.py` files under `datastorekit/`). After: 31, 8 and 9 (48).
  - `compare_ported_tests.py` exits 0 over 3 modules before, and 8 after.
  - The index is **6**, and stays 6 unless the work opens an issue.
- **The prose issue** stands at 114 lines in 23 files, by log 03a §8's method. The agent first
  reproduces 114 in 23 at `19adaa2`, then measures after, and the log gives both figures.
- **Ray.** No Ray process was up at writing (`pgrep -lf 'gcs_server|raylet|ray::'` empty).

**What the review exists to establish.**
- **(E1) The names.** The five modules hold SGK's `Class.method` sets and class bases, after U12's
  four renames and nothing else. The 188 are still there by name.
- **(E2) The port check.** Its only changes are `PORTED` (five pairs) and `NAME_MAP` (four
  entries). It exits 0 over eight modules with the table's counts. (a)–(c) and (p) make it exit 1,
  and (d) makes `compare_with_source.py` exit 1.
- **(E3) The meaning.** Each test's control flow is SGK's. Each kind in the port table is honest.
  R-value keeps SGK's equalities and differences.
- **(E4) The client.** Additions only, as §2.3 says. Of the existing tests, only `KEPT` and
  `counts` change. 03a's modules are unchanged and pass. The contract changes only in client
  columns.
- **(E5) The reader.** The instrument is the probe's, line for line, after R-imp. The sequence
  meets hazards 3 and 4, and its outcome strings are measured from it.
- **(E6) The layer through the tests.** (e)–(j) each fail the tests the log names. A mutation that
  fails nothing has a §3 issue.
- **(E7) The records.** The log, with the prompt's §4.4 additions; the board's §1 and §3;
  `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.

**Conventions.** 03a's note's, unchanged, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff with `git apply --check` and `-R --check`, and replay it in `bash`;
- read SGK only through `git show`, and never import or run its probe;
- use a subdirectory of the session scratchpad, never `/tmp`, and put **no scratch `.py` under
  `datastorekit/`**, since the import guard and `compare_with_source.py` scan it;
- start no Ray;
- a stop goes to the user;
- check `git log` before committing.

One addition: **work in this order, and run the suite after each step.**
1. The two classes, with `test_neutral_client.py`'s literals, the contract, and 03a's modules
   run unchanged.
2. The three small modules.
3. `test_version_row_at_open`, then `test_one_timestamp_per_write`.
4. `reader.py`, run from the scratchpad on a read-write and a read-only copy of its store, before
   the test module uses it.
5. `test_read_only_pool`.

A ripple of the client change then shows up before any port depends on it, and a fault in the
sequence shows up before 23 tests do.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone.
2. **The baseline.** The suite gives `Ran 188 tests … OK`, and both checks exit 0.
3. **SGK.** `git -C SecondaryGWKit diff --stat 6f7f291 HEAD -- Datastore tools utilities.py
   config/defaults.py config/sharding.py docs/a3-v2-readiness/reader_writes_probe.py` is empty.
4. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`.
5. **The index.** 6 now, and 6 after unless the work opens an issue. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`, log 02 and
  log 03a;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's correction and four additions. The payload fact is
the one most likely to be missed: `ReadOnlyMiss.payload` is keyed by column name, so a literal
port of the payload lambdas fails with a `KeyError` inside the assertion.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/03b-port-the-open-and-read-only-tests.md`, in
  README §5.1's form, with the prompt's §4.4 additions.
- **The files it may add or change are the prompt's §6 list, and nothing else**, plus any issue
  the work opens. It must not touch:
  - any file under `datastorekit/` outside `tests/`;
  - `standin_pool.py`, `shard_store_fixtures.py`, or 03a's four modules;
  - `PROVENANCE.md`, `pyproject.toml`, `README.md`, `CLAUDE.md` or the campaign README;
  - anything under `orchestrator/`.
- **It edits no client repository, and runs no client code.** It reads SGK through `git show`,
  and transcribes from the probe without importing it.
- **It runs no build, and starts no Ray.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — ten checks

1. **Scope.** `git show --stat <commit>` touches only the prompt's §6 list and the records. No file
   under `datastorekit/` outside `tests/`. No change to `standin_pool.py`,
   `shard_store_fixtures.py` or 03a's four modules. No `venv/`, `*.egg-info`, `__pycache__` or
   scratch file.
2. **E1, the names.** Independently of the agent's script, by `ast`: per module, the set of
   `Class.method` and each class's bases equal SGK's at `6f7f291`, with U12's four renames applied
   and no other. Per module, the 188 are unchanged by name from `19adaa2`.
   `./venv/bin/python -m unittest discover -s datastorekit/tests -t .` gives `Ran 268 tests …
   OK`. The loader gives 12, 23, 28, 12 and 5 per module.
3. **E2, the port check, by reading.** `git show <commit> -- docs/extraction/compare_ported_tests.py`
   adds five pairs to `PORTED` and four entries to `NAME_MAP`, keyed by
   `datastorekit/tests/test_read_only_pool.py`, and changes nothing else.
   `compare_with_source.py` changes only in `FILES` and `NO_SOURCE`.
4. **E2, by running.** Both checks exit 0. The port check's counts equal §0's table, and 03a's
   three modules' counts are unchanged (125, 148, 74). `compare_with_source.py` gives 31, 8 and 9,
   with 02's totals unchanged. Replay (a)–(d) and (p), one at a time, in `bash`; each exits 1 and
   names what the prompt says. Then two of the orchestrator's own:
   - delete the `assertFalse` from `_TickingClock.assertNoShardClock`. It must exit 1, naming
     that helper;
   - rename `test_routing_rule` back to `test_GkSourcePolicy` in the module. It must exit 1, naming
     the test both ways.

   `git status` is clean after each.
5. **E3, R-map and R-value, by reading.** Read the word diff of each module against SGK, after
   R-imp:
   - in full: the three small modules, `TestEachMissRaisesReadOnlyMiss`,
     `TestNothingWrittenOnAFullStore`, `TestInsertBeforeSetVersion` and
     `test_versioned_rows_carry_the_serial_on_every_shard`;
   - at least `TestAtOpen` and `TestOtherWritesRaiseReadOnlyWrite` of the rest.

   Check:
   - each changed literal against the port table's kind;
   - that R-value keeps SGK's distinctions: two tolerances, two policies with different labels and
     thresholds, and the deleted gauge and rule being the ones the sequence reaches;
   - that the payload lambdas read column names (§0's payload fact);
   - that §0's additions are applied as stated.
6. **E3, control flow, by measuring.** From the scratchpad, by `ast`, compare each function of the
   five modules with its SGK counterpart, as at 03a's check 6. Compare the sequence of `If`, `For`,
   `While`, `With` (with its item count), `Try`, `Return`, `Raise`, `Break`, `Continue`,
   conditional expressions, comprehensions and nested `def`s. Every difference is named in the log
   and is R-help. `_load_probe`'s removal is one. Any other difference is a finding.
7. **E4, the client.**
   - `objects.py`, `factories.py` and `registry.py` change by addition only.
   - `build.py` changes by addition, plus the gauges and rules in `write_every_class` after
     `knob_setting`.
   - The registry places both classes in `replicated_tables` after `knob_setting`. Neither is in a
     drop group, `read_table_config` or `serial_batch_sizes`, and `__all__` is unchanged.
   - `test_neutral_client.py`'s diff is `KEPT` and `counts` only.
   - The contract's diff is in client columns only.
   - 02's 19 pass by name, and 03a's 79 pass with their modules byte-identical to `19adaa2`.
8. **E5, the reader.**
   - Diff each transcribed function against the probe's lines, as the log gives them. Only R-imp
     (`sp` is the package's stand-in pool) and §0's correction may differ.
   - `reader.py` holds no `assert*`/`fail*` call and no `raise AssertionError`.
   - Run `build_full_store` and `reader_sequence` from the scratchpad, on a read-write and a
     read-only copy:
     - the read-write run changes only `store.sqlite`, and its `_replicated_write` count is the
       test's literal;
     - each step's outcome is the same on both runs;
     - the sequence stops at the knob frame's Gadget, with the sequence's own message.
   - For each of the four miss tests, the `ReadOnlyMiss` comes from the step the log's step table
     says, and no earlier step inserts on a miss.
9. **E6, the layer.** Replay (e)–(j), one at a time. Check that the tests that fail are the
   log's. Read one failing test for each, and check that it fails on an assertion or the layer's
   own exception, not on a broken fixture. (e) is expected to fail tests on each of the three
   paths that `test_one_timestamp_per_write` covers (repair, prune and version row); if a path
   fails none, the log says why. If any mutation fails nothing, its §3 issue is open.
10. **E7, the records.**
    - The log has every section of README §5.1 and each §4.4 addition:
      - the port table, 53 rows and the 27 inherited;
      - the map as used;
      - the five hazards;
      - the two classes and every literal and contract line changed;
      - the step table and the probe lines;
      - the docstring sentences;
      - both checks' whole output and the loader's counts;
      - 188 → 268;
      - (a)–(j) and (p).
    - The board: 03b's row, the header, and the prose issue's new count with the reproduction of
      114.
    - The index: count its rows, and check that the header matches. `prompts/INDEX.md`: the
      campaign's line.
    - `black --check` (25.1.0) is clean on `datastorekit/` and `docs/extraction/`. Ray is not
      running, and each module's `tearDownModule` holds.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 03b* paragraph, in the form
  of 03a's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README's header, and its §2 status for 03b;
  - the notes line, with this note marked "used for 03b".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Hand on to 04's author:**
  - the client now has 16 classes. Any literal 04 measures over the registry or `build_store` (its
    inventory and drop tests) is measured after 03b;
  - `NAME_MAP` is in use, and how its renaming reaches every name segment;
  - `reader.py` is a fixture with no source. 04 should not grow it;
  - anything the review found about the port check's blind spots, since 04 ports 175 tests
    through it.
- **Report to the user:**
  - what landed, and the count 268;
  - the client change, and its ripple;
  - the reader sequence's design, and its step table in brief;
  - the port check over eight modules, and (a)–(d), (p) and the orchestrator's two breakages
    biting;
  - the control-flow comparison, and anything it found;
  - (e)–(j), with the tests each fails;
  - the prose issue's new count;
  - that 04 can now be written.
