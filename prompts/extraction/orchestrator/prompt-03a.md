# Orchestrator — prompt 03a, port the replicated-write tests

Read [`../README.md`](../README.md) first: §0.2, §2 (rows 03a, 03b, 04), §4, §5 and §6.2 (U9–U12).
Then read [`prompt-01.md`](prompt-01.md) §0's last list and [`prompt-02.md`](prompt-02.md) §0's
"Conventions", which this note keeps unless it says otherwise, and the board's reviews of 01 and
02.

**You do not write code.** You may:
- run the suite, both checks and the tests the log names;
- replay the log's deliberate-breakage diffs with `git apply`, and revert them;
- run an in-process check or a probe from the session scratchpad, never committing one;
- read SGK through `git -C /Users/ds283/Documents/Code/SecondaryGWKit show 6f7f291:<path>`;
- fix small residue in a follow-up commit of your own (§4).

**The prompt:** [`03a-port-the-replicated-write-tests.md`](../03a-port-the-replicated-write-tests.md)
**Closes:** `[02-no-test-reaches-revalidate]` and `[01-no-ported-test-pins-the-shard-key-assignment]`
· **Narrows:** nothing · **Changes:** `[01-package-prose-names-sgks-layout]` (its count) ·
**Opens:** only what the work finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- 02 landed (`e988e69`) and its review is recorded (`03fa97a`). 03a is written (`0d02ea6`), and
  U9–U12 are taken.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- SGK's `Datastore/` (layer, tests and stand-in pool), `tools/`, `utilities.py` and
  `config/defaults.py` are unchanged from `6f7f291` to SGK `HEAD` (`b510bc9`, 2026-10-07). The
  prompt reads SGK at `6f7f291` regardless.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It is the first prompt whose code is neither moved nor new.** 01 moved files and 02 wrote a
client. 03a rewrites 2,510 lines of SGK tests onto that client, and nothing mechanical can say the
rewrite kept their meaning. The port check (U9) says the names and the sequence of assertion calls
are kept. It does not see arguments, control flow, or which object a test asserts about. So the
review has three halves:
- **the port check is sound**, and bites on the prompt's (a)–(e) and on the orchestrator's own;
- **each test still tests what it tested**: the port table's kinds are honest, R-map and R-count
  change only what the fixture wrote, and no test's control flow changes;
- **the two closures are real**: (i) and (j) each fail a named test, and the shard-key test checks
  the saved map against the one in memory, after a reopen.

**What moves on purpose:** three ported modules and one new one under `datastorekit/tests/`;
additions to `tests/client/build.py`; `docs/extraction/compare_ported_tests.py` (new) and
`compare_with_source.py` (the `PORTED` kind); the records. No file under `datastorekit/` outside
`tests/` changes, and neither does `standin_pool.py` or the rest of `tests/client/`.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-07 at `0d02ea6` (package
files as at `e988e69`) and SGK `6f7f291`. Pass them on; each is STRUCTURALLY REQUIRED, and the log
says so.

1. **`REPLICATED` must leave out `ephemeral_probe`.** Each module defines
   `REPLICATED = list(replicated_tables) + ["BackgroundModel_tags"]` (`test_replicated_write.py:42`,
   `test_reconcile_at_open.py:53`, `test_prune_at_open.py:49`). The literal port,
   `list(registry.replicated_tables) + ["Gadget_tags"]`, names 10 tables. But `ephemeral_probe`
   registers `None` and has no table, so the check at open compares 9: measured on a reopened
   `build_store`, `reconciliation["compared"]` is `['version', 'store_tag', 'keypoint',
   'keypoint_alias', 'dial_setting', 'knob_setting', 'Gadget', 'GadgetPart', 'Gadget_tags']`.
   With the literal port:
   - every helper that iterates `REPLICATED` fails on the missing table: `shard_rows` builds
     `ORDER BY` with no columns, and `_read` of `SELECT … FROM "ephemeral_probe"` finds no table.
     That is `assertIdentical`, `all_keys` and `run_case` in `test_reconcile_at_open`, and
     `replicated_rows` and `assertIdentical` in `test_prune_at_open`;
   - `TestCleanStoreUntouched.test_opening_a_clean_store_writes_nothing` asserts
     `assertEqual(REPLICATED, rec["compared"])`.

   **So:** each module's `REPLICATED` names the replicated tables that have a table, then
   `Gadget_tags`, in that order. It may be an explicit list, or the registry filtered on
   `register() is not None`; the log says which. It is **R-count**: the constant names what the
   store holds, and the assertions that use it do not change. It is not a stop.
2. **The sharded "stored" role (`GkSourcePolicyData` → `Sample`) has one trap.** SGK's
   `GkSourcePolicyData` declares no `validate_on_startup`. The neutral `Sample` does, so under
   `prune_unvalidated=True` each actor prunes an **unvalidated** Sample. SGK's prune fixture stores
   its policy data unvalidated (`_PruneTestCase.build`, `test_prune_at_open.py:119`), and two tests
   then require the prune to leave the sharded rows alone:
   - `TestUninterruptedPrune.test_every_shard_identical_and_no_record_left` asserts
     `assertEqual(sharded, self.sharded_rows())` (`:284`);
   - `test_a_prune_with_nothing_to_prune_writes_nothing` asserts the checksums unchanged (`:299`).

   A literal port with `store_sample(…, validate=False)` fails both. That is not a layer defect,
   and not a stop: it is a role chosen wrongly. **So:** in `_PruneTestCase.build`, the Sample is
   stored **validated**. That is `store_sample`'s default. A Sample with no members validates
   (`member_count` 0 equals the 0 member rows: `Sample_factory.validate`,
   `tests/client/factories.py:1060-1078`). The change is R-help.

   `Tessera`, which like `GkSourcePolicyData` is keyed on the proxy and does not prune, cannot take
   this role. Its factory has no `store` (abstract in `SQLAFactoryBase`, `SQL/factory_base.py:18`),
   so it is inserted by a get only, and `factories.py` may not change (§2.3).

   **Where a test measures the store itself, the bare `object_store` stays.** That is
   `TestShardedWritesUnchanged.test_a_sharded_store_stamps_its_own_time_and_writes_no_record`
   (`test_replicated_write.py:677`) and `TestRecordDoesNotExplain.test_a_difference_in_a_sharded_table_is_not_looked_at`
   (`test_reconcile_at_open.py:794`). Neither prunes, and a validate inside the first one's
   measured window would add a call.

   SGK's `make_policy_data` gives its object `StandinSerial` handles for its source and policy
   (SGK `standin_pool.py:564`). `Sample_factory.store` reads only `gadget.store_id`, and the
   layer enforces no foreign key, so `objects.SerialHandle` may stand for the Gadget in the same
   way. A stored Gadget would add a row to every `Gadget` count of the prune tests. The log says
   which the agent used, and where.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **(o), the port check bites on order.** Swap two assertion calls of different names in one
  ported test (for example the first two of
  `TestShardedWritesUnchanged.test_a_sharded_store_stamps_its_own_time_and_writes_no_record`):
  `compare_ported_tests.py` exits 1, naming the test and the position. Record it with (a)–(e).
- **The port check's blind spot is stated in the log.** It compares the sequence of assertion
  calls, so an assertion wrapped in `if False:`, or a loop that runs zero times, passes it. The
  log says so in "Observations not acted on". It does not try to close it. The review measures
  control flow separately (§3, check 6), and the agent should expect that.

**The facts, checked by the orchestrator.** Pass them on.

- **The prompt's survey holds** at `0d02ea6` and SGK `6f7f291`:
  - module lengths 720, 1,172 and 618; SGK's stand-in pool 581;
  - tests by `ast`, with inheritance resolved: `test_replicated_write` 25 (2, 7, 4, 7, 3, 2 in
    file order), `test_reconcile_at_open` 41 (12, 3, 3, 9, 8, 2, 2, 2), `test_prune_at_open` 10
    (3, 2, 1, 3, 1). Defined equals run in all three;
  - `test_validate_of_a_background_model` at `test_reconcile_at_open.py:486`; the shard key's
    self-heal at `:330-343`; the death inside `_assign_shard_keys` at `:548-568`;
  - in the package: `_assign_shard_keys` called at `SQL/ShardedPool.py:687` and `:3246`, defined at
    `:3505`, its insert at `:3561`; `raise ReplicationInFlight` at `:3097`; the monotone-flag
    loop from `:1938`; `_clear_in_flight_record("prune", cls_name)` at `:2341` (and again at
    `:2422`, the completion of an interrupted prune: (h) is the one at `:2341`); `revalidate`
    called at `:1992`; `Gadget_factory.validate_on_startup` at `tests/client/factories.py:761-799`,
    deleting parts, then tags, then the owner, inside `except SQLAlchemyError`.
- **R-name:** no test or class name in the three modules is one of the 82 registry names (log 02
  §1.2). `background` or `exit_time` occurs in 17 test names (10, 6, 1); neither is a table
  identifier, and `grep -w` does not match them to `BackgroundModel` or `wavenumber_exit_time`.
  Those names stay.
- **R-map's size.** Lines holding one of the 80 client names (the 82 less `version` and
  `store_tag`), as whole words: `test_replicated_write` 67, `test_reconcile_at_open` 84,
  `test_prune_at_open` 32. By name: `BackgroundModel` 59, `tolerance` 48, `BackgroundModelValue`
  31, `redshift` 20, `wavenumber_exit_time` 13, `BackgroundModel_tags` 10, `wavenumber` 7,
  `GkSourcePolicyData` 5, `GkSourcePolicy` 3, `TkNumericIntegration` 2, `GkSource` 2,
  `IntegrationSolver` 1. §3.4's grep must find none afterwards. `tolerance` and `redshift` are also
  English words: a docstring that uses one as a word still fails §3.4's grep, and is mapped.
- **The stand-in pool keeps every generic name the modules use:** `StandinCluster`,
  `StandinActorDied`, `StandinRef`, `sp_mod`, `ds_mod`, `DatastoreClass`, `_Options`, `_read`,
  `shard_rows`, `shard_snapshot`, `store_checksums`, `in_flight_records`. The SGK helpers
  `get_tolerance`, `get_redshifts`, `get_wavenumber`, `make_units`, `StandinCosmology`,
  `make_exit_time`, `make_background_model` and `make_policy_data` are gone (D-split), and are
  replaced by R-help.
- **Hazard 1 (the shard key is the flagged class) is benign, measured.**
  - `_assign_shard_keys` writes the primary directly, and makes no actor call, so no count of
    `cluster.calls` sees it.
  - Of the 12 `store_checksums` sites in `test_reconcile_at_open` and the 12 in
    `test_prune_at_open`, only `:560-568` spans a successful get of the shard-key class. It does
    in SGK too, since `wavenumber` is SGK's shard key, and it asserts that the files change.
  - `shard_snapshot` and `shard_rows` read shards, not the primary.

  The agent still checks each test, and says so in the log.
- **(i) bites, probed.** A store of an unvalidated Gadget whose replicated validate is killed at a
  replica (`fault(r0, "object_validate", "Gadget", "before")`) leaves the record. The reopen
  repairs it with `("validated recomputed", "Gadget", r0)`, and every shard holds
  `gadget_validated = 1`. With `Gadget_factory.revalidate` patched to return `True` without
  writing, the reopen raises `ReplicatedDivergence`. So the ported
  `test_validate_of_a_background_model` will fail under (i).
- **(j) can bite through the stand-in's faults alone, probed.**
  1. Kill a get of keypoint A at a replica (`fault(r0, "object_get", "keypoint", "before")`).
     A is then on the controller and r1 with serial 1, and has no shard key.
  2. Reopen; the check at open copies A to r0.
  3. Get a new keypoint B (serial 2), and then A again.

  The keys are then assigned in the order 2, 1. On the unmutated tree, memory, disk and the
  reopened pool all give `{1: 0, 2: 2}`. Under the `key_id` binding, the layer prints two
  `MISMATCH` lines, memory holds `{2: 2, 1: 0}`, and disk and the reopened pool hold `{1: 2, 2: 0}`.
  This is one route the prompt's §2.5 allows. The agent chooses its own and says why it works; the
  route needs no `mock` of the layer.
- **The toolchain.** `venv/` from 01: Python 3.12.15, `ray==2.43.0`, `sqlalchemy==2.0.39`,
  `black==25.1.0`, the package installed editable. It needs no change.
- **Expected counts.**
  - The suite is **109** before (`Ran 109 tests … OK`, re-run by the orchestrator at `0d02ea6`),
    and 109 + 76 + the new module's tests after.
  - `compare_with_source.py` exits 0 before, with `files compared: 31` and `files with no
    source, declared: 7` (38 tracked `.py` files). After, 31 compared, 3 `PORTED` and 8 with no
    source (42).
  - The index is **8** now, and **6** after the two closures, unless the work opens anything.
- **The prose issue's pattern** is on the board's §3. By the orchestrator's reading of it (comment
  and string tokens), the three SGK modules hold 3, 5 and 2 matching lines. The orchestrator's
  reproduction over the package gives 108 lines in 24 files, not the board's 104 in 20, so its
  reading differs from 01's in some detail. The agent first reproduces **104 in 20** at
  `03fa97a` with its own method, then measures after, and the log gives both figures and the
  method.
- **Ray.** No Ray process was up at writing (`pgrep -lf 'gcs_server|raylet|ray::'` empty).

**What the review exists to establish.**
- **(E1) The names.** The three modules hold SGK's `Class.method` sets and class bases exactly.
  The 109 are still there by name.
- **(E2) The port check.** It does what §2.4 says: names, bases, the assertion skeleton of every
  asserting function, and no new asserting function. It exits 0, and (a)–(d) and (o) each make it
  exit 1. `compare_with_source.py` has the `PORTED` kind, exits 0, and (e) makes it exit 1.
- **(E3) The meaning.** Each test's control flow is SGK's. Each kind in the port table is honest.
  R-value keeps SGK's equalities and differences. Corrections 1 and 2 are applied as stated.
- **(E4) The client.** `build.py` changes by addition only. Nothing else in `tests/client/`, and
  not `standin_pool.py`, changes. 02's 19 tests pass unchanged.
- **(E5) The layer through the tests.** (f)–(j) each fail the tests the log names.
- **(E6) The closures.** The new module compares the saved map with the reopened and in-memory
  maps, and checks each Sample's shard after the reopen. (j) fails it. (i) fails
  `test_validate_of_a_background_model`.
- **(E7) The records.** The log, with the prompt's §4.4 additions, the board's §3 and §4,
  `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.

**Conventions.** Prompt 02's note's, unchanged, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff with `git apply --check` and `-R --check`, and replay it in `bash`;
- read SGK only through `git show`;
- use a subdirectory of the session scratchpad, never `/tmp`, and put **no scratch `.py` under
  `datastorekit/`**, since the import guard and `compare_with_source.py` scan it;
- start no Ray;
- a stop goes to the user;
- check `git log` before committing.

One addition: **port module by module, and run the port check after each.** Start with
`test_prune_at_open` (10 tests, the smallest), then `test_replicated_write`, then
`test_reconcile_at_open`. A design fault in the check, or a wrong role in the map, then shows
up on 10 tests, not on 76.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone.
2. **The baseline.** The suite gives `Ran 109 tests … OK`, and `compare_with_source.py` exits 0.
3. **SGK.** `git -C SecondaryGWKit diff --stat 6f7f291 HEAD -- Datastore tools utilities.py
   config/defaults.py` is empty.
4. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`.
5. **The index.** 8 now, and 6 after the closures. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md` and log 02;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's two corrections and two additions. Correction 2 is the
one most likely to be missed: a literal port of the prune fixture fails two tests in a way that
looks like a layer defect.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/03a-port-the-replicated-write-tests.md`, in README
  §5.1's form, with the prompt's §4.4 additions.
- **The files it may add or change are the prompt's §6 list, and nothing else**, plus any issue
  the work opens. It must not touch any file under `datastorekit/` outside `tests/`, nor
  `standin_pool.py`, `objects.py`, `factories.py`, `registry.py`, `test_neutral_client.py`,
  `PROVENANCE.md`, `pyproject.toml`, `README.md`, `CLAUDE.md`, the campaign README, or anything
  under `orchestrator/`.
- **It edits no client repository, and runs no client code.** It reads SGK through `git show`.
- **It runs no build, and starts no Ray.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — ten checks

1. **Scope.** `git show --stat <commit>` touches only the prompt's §6 list and the records. No
   file under `datastorekit/` outside `tests/`; no change to `standin_pool.py`, `objects.py`,
   `factories.py`, `registry.py` or `test_neutral_client.py`; no `venv/`, `*.egg-info`,
   `__pycache__` or scratch file.
2. **E1, the names.** Independently of the agent's script, by `ast`: per module, the set of
   `Class.method` and each test class's bases equal SGK's at `6f7f291`. Per module of the 109,
   the set is unchanged from `0d02ea6`.
   `./venv/bin/python -m unittest discover -s datastorekit/tests -t .` gives `Ran N tests … OK`,
   and N equals the log's.
3. **E2, the port check, by reading.** Read `compare_ported_tests.py` in full.
   - It reads SGK with `git show 6f7f291:`, and writes nothing.
   - `PORTED` names the three modules, and `NAME_MAP` is empty.
   - The skeleton is taken in source order, at any depth (inside `with`, `for`, `if`, nested
     functions and lambdas). It includes `assert*`/`fail*` calls on any receiver, `raise
     AssertionError` and `self.subTest`.
   - Every SGK function or method that asserts is compared by qualified name, including module
     level ones (`tearDownModule`) and helpers whose names do not begin with `assert` (`run_case`,
     `interrupt`, `refused_reopen`, `build`).
   - A new function that asserts fails the check.
   - Exit codes are 0, 1 and 2, as §2.4 says.
4. **E2, by running.** Both checks exit 0, with counts equal to the log's. 01's and 02's
   per-class counts in `compare_with_source.py` are unchanged. Replay (a)–(e) and (o), one at a
   time, in `bash`; each exits 1 naming what the prompt says. Then one of the orchestrator's own:
   in a ported asserting helper with no test name (for example `_ReconcileTestCase.refused_reopen`),
   delete one `assertEqual`. It must exit 1, naming the helper. `git status` is clean after each.
5. **E3, R-map and R-value, by reading.** Read the word diff of each module against SGK, after
   R-imp, in full for `test_prune_at_open` and for at least one class of each of the other two
   (`TestKillAndReopen`, `TestIdempotentReplicaStores`). Check:
   - each changed literal against the port table's kind for that test;
   - that R-value keeps SGK's equalities and differences (two scales, two tolerances, two
     positions);
   - that R-count literals were recomputed, not copied (spot-check three by running the fixture
     in the scratchpad);
   - that `REPLICATED` and the prune fixture follow corrections 1 and 2.
6. **E3, control flow, by measuring.** From the scratchpad, by `ast`, compare each test method
   and each asserting helper with its SGK counterpart. Take the sequence of compound-statement node
   types (`If`, `For`, `While`, `With`, `Try`, and the `subTest` loops), ignoring the code inside
   the R-help helpers. Every difference is named in the log and is R-help; any other is a
   finding. This covers the port check's blind spot (§0, the second addition).
7. **E4, the client.** `git show <commit> -- datastorekit/tests/client/build.py` adds only, and
   each added parameter has a default that keeps the old behaviour. 02's 19 tests pass, by name.
8. **E5, the layer.** Replay (f)–(i), one at a time, and check that the tests that fail are the
   log's. Read one failing test for each, and check that it fails on an assertion, not on an
   error in the fixture.
9. **E6, the closures.** Read `test_shard_key_assignment.py`. It assigns keys out of serial order
   (or from a serial other than 1), and the log says why that works. It reads the primary's
   `shard_keys` with `standin_pool._read` after closing. It compares that with the reopened
   pool's `_shard_keys` and the map held before closing. It finds every Sample on the shard the
   map names after the reopen. Replay (j): it fails, and the failure is the map comparison.
   Replay (i): `test_validate_of_a_background_model` fails.
10. **E7, the records.**
    - The log has every section of README §5.1 and each §4.4 addition: the port table, 76 rows;
      the map as used; the three hazards; corrections 1 and 2; the `build.py` helpers with
      signatures; both checks' whole output; the counts 109 → N, with the new tests named; and
      (a)–(j) and (o).
    - The board: 03a's row; the two issues in §4 with "Closed" lines naming the test and the
      breakage; the prose issue's new count, with the method that reproduces 104.
    - The index: count it, and check that the header matches (6, unless the work opened issues).
      `prompts/INDEX.md`: the campaign's line.
    - `black --check` (25.1.0) is clean on `datastorekit/` and `docs/extraction/`. Ray is not
      running, and the suite never started it: each module's `tearDownModule` holds.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 03a* paragraph, in the form
  of 02's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README §2's status for 03a;
  - the notes line, with this note marked "used for 03a".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Hand on to 03b's author:**
  - correction 1's `REPLICATED`, which `test_one_timestamp_per_write` inherits through 03a's
    classes;
  - correction 2's reading of the sharded role;
  - whether `compare_ported_tests.py` handles a test class that subclasses another module's.
    03b's `test_one_timestamp_per_write` needs that, and 03a's three modules do not exercise it.
- **Report to the user:**
  - what landed, and the count N;
  - the port check's design, its counts, and (a)–(e), (o) and the orchestrator's own breakage
    biting;
  - the control-flow comparison, and anything it found;
  - the two closures, with the tests (i) and (j) fail;
  - the prose issue's new count;
  - that 03b and 04 can now be written, in either order but not concurrently.
