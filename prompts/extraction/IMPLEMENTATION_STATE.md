# extraction campaign — implementation state

**Last updated:** 2026-10-08 · **Status: IN PROGRESS — 5 of 9 prompts written (01, 02, 03a, 03b, 04a), 4 landed (01, 02, 03a, 03b).**
G1 holds: the import commit is SGK `6f7f291`. The user took U2–U5 as recommended on 2026-10-07,
U8–U13 the same day, and U14–U21 on 2026-10-08 (README §6.2); U10 split 03 into 03a and 03b, and
U14 split 04 into 04a and 04b.

**Campaign:** [`README.md`](README.md) ·
**Source:** SecondaryGWKit's `Datastore/` layer at the import commit `6f7f291` (G1) ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) §1.1

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

### Decisions

**Made by the user, 2026-10-07 (README §6.1):**

| Decision | Decided |
|---|---|
| **D1** | Extract the layer as a separate, reusable component |
| **D2** | `Datastore` / `ShardedPool` first; `RayWorkPool` is a separate unit of work |
| **D3** | A public GitHub repository, `ds283/DatastoreKit` |
| **D4** | ChamPBH's stores are rebuilt on adoption, not migrated |

**Put to the user (README §6.2):**

| Decision | Recommendation | Status |
|---|---|---|
| **U1** name | DatastoreKit / `datastorekit` | applied at set-up; changeable until 01 lands |
| **U2** history | fresh import plus `PROVENANCE.md` | **taken** 2026-10-07 |
| **U3** SGK layer freeze from G1 to G2 | freeze | **taken** 2026-10-07; in force from SGK `b510bc9` (its `CLAUDE.md`, "The datastore layer is frozen") |
| **U4** distribution | pinned git tag in each client's `requirements.txt` | **taken** 2026-10-07 |
| **U5** module names | keep SGK's through this campaign | **taken** 2026-10-07 |
| **U6** supported range and CI | Python ≥ 3.12; GitHub Actions at both ends | open |
| **U7** licence | Apache 2.0 | applied at set-up; changeable |
| **U8** SGK's table names in 01's 88 tests | re-fixture onto the neutral client's names in 02 | **taken** 2026-10-07 |
| **U9** checking a re-fixtured test | a port-check script: names and assertion skeletons | **taken** 2026-10-07 |
| **U10** splitting 03 | 03a (76 tests) and 03b (53 defined, 80 run) | **taken** 2026-10-07 |
| **U11** `test_read_only_pool`'s SGK probe | `build_store` and a neutral reader sequence | **taken** 2026-10-07 |
| **U12** test names that are client table names | renamed by the table map | **taken** 2026-10-07 |
| **U13** roles the neutral client lacks for 03b | 03b adds two replicated classes to the client | **taken** 2026-10-07 |
| **U14** splitting 04 | 04a (85 tests, the fixtures, the client additions) and 04b (90 tests, the guard) | **taken** 2026-10-08 |
| **U15** roles the neutral client lacks for 04 | 04a adds a sharded family (`Trace`, `Weave` and their tables), and `Gadget`'s validate prints a warning | **taken** 2026-10-08 |
| **U16** the test about SGK's report | not ported; declared in a `NOT_PORTED` list of the port check (04b) | **taken** 2026-10-08 |
| **U17** the guard and the layer's frozen prose | a pinned list of known hits, exact in both directions (04b) | **taken** 2026-10-08 |
| **U18** the neutral `Sample`'s validated flag in the inventory | 04a deletes `validated` from `Sample`'s `inventory_spec`; `Trace` takes the sharded flag | **taken** 2026-10-08, at 04a's orchestration |
| **U19** a drop list of 03a's that the new client outgrows | 04a adds `traces` to `test_an_interrupted_store`'s `tables_to_drop` list (R-count) | **taken** 2026-10-08, at 04a's first stop |
| **U20** the schema witness and a class with no table | `test_schema_builder` and `actor_with_built_schema` use the registry less `register() is None`; the witness is captured from it | **taken** 2026-10-08, at 04a's second stop |
| **U21** `test_schema_builder`'s witness history | the docstring names the new witness, and says SGK's are SGK's history | **taken** 2026-10-08, at 04a's second stop |

---

## 1. Prompts

| # | Prompt | Covers | Written? | Landed? | Commit | Log |
|---|---|---|---|---|---|---|
| 01 | [Import the layer](01-import-the-layer.md) | package, 15 files and 2 tools, the two internalised dependencies, 88 tests, import guard | ✍️ yes, 2026-10-07 | ✅ 2026-10-07 | `8bc60a5` | [log](logs/01-import-the-layer.md) |
| 02 | [The neutral test client](02-the-neutral-test-client.md) | `docs/client-contract.md`, the test client, the stand-in pool; 01's tests onto the client's names (U8) | ✍️ yes, 2026-10-07 | ✅ 2026-10-07 | `e988e69` | [log](logs/02-the-neutral-test-client.md) |
| 03a | [Port the replicated-write tests](03a-port-the-replicated-write-tests.md) | 76 tests (replicated write, check at open, prune at open); the port check; the `key_id` pin and `revalidate` | ✍️ yes, 2026-10-07 | ✅ 2026-10-07 | `11247c7` | [log](logs/03a-port-the-replicated-write-tests.md) |
| 03b | [Port the open and read-only tests](03b-port-the-open-and-read-only-tests.md) | 53 tests, 80 run (version row, read-only pool, one timestamp, shard records); the two client classes (U13); the neutral reader sequence (U11) | ✍️ yes, 2026-10-07 | ✅ 2026-10-08 | `0d5380c` | [log](logs/03b-port-the-open-and-read-only-tests.md) |
| 04a | [Port the store and inventory tests](04a-port-the-store-and-inventory-tests.md) | 85 tests (inventory, store schema, reader, foreign keys, schema builder); `real_store_fixtures` and `schema_description` on neutral rows; the schema witness; the client's sharded family (U15) | ✍️ yes, 2026-10-08 | ⬜ | — | — |
| 04b | Port the declaration and registry tests | 90 tests (inventory declarations, declared facts, layer registry, drop refusal); the package guard (U16, U17) | ⬜ | ⬜ | — | — |
| 05 | Supported versions and CI | `pyproject.toml` ranges, both ends, Actions; tag `v0.1.0` | ⬜ | ⬜ | — | — |
| 06 | Version-keyed lookups | `key_on_version`; tag `v0.2.0` | ⬜ | ⬜ | — | — |
| 07 | Close-out and adoption handover | `docs/adoption/` checklists; verification document | ⬜ | ⬜ | — | — |

**Legend.** ✍️ written · ⏸ held, with what it waits on · ⬜ not written / not landed ·
✅ landed.

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`bd9f461`),
used for 01; [`orchestrator/prompt-02.md`](orchestrator/prompt-02.md) (`737ad6e`), used for 02;
[`orchestrator/prompt-03a.md`](orchestrator/prompt-03a.md) (`f7f053d`), used for 03a;
[`orchestrator/prompt-03b.md`](orchestrator/prompt-03b.md) (`72cf34a`), used for 03b.

**Orchestrator review of prompt 01 (2026-10-07).** Dispatched from `bd9f461` to one Opus
subagent, with the note's §0 corrections and additions. Reviewed against its commit `8bc60a5`,
with nothing landed after it. **Every check of the note's §3 passed**, and acceptance 1–3 are met.
No stop condition fired, and the agent ran its suite in the foreground.

*At dispatch.* The note's gate held at `bd9f461`. The tree was clean, and the only worktree was
this checkout. `venv/` did not exist. SGK's frozen files were unchanged from `6f7f291` to SGK
`HEAD` (`b510bc9`), and no Ray process was up.

*The checks.*
1. **Scope.** `8bc60a5` touches 38 files: 35 new, the board, `prompts/INDEX.md` and the index. No
   `venv/`, `*.egg-info` or scratch file.
2. **E1, the files.** `git ls-files datastorekit` gives the prompt's §2.3 files under their
   names, the two empty `__init__.py`s, `defaults.py`, `_timing.py` and the guard: 31 files.
3. **E2, by running.** `compare_with_source.py` exits 0 over 30 files: D-imp −50/+50, D-str
   −4/+4, D-tool −26/+22, D-root −8/+6, D-int −222/+11, D-fmt −1/+0 (one blank line beside the
   removed constants), unclassified 0. Python 3.12.15, `ray==2.43.0`, `sqlalchemy==2.0.39`,
   `black==25.1.0`.
4. **E2, by reading.** The check applies each class to the SGK source as a transformation, runs
   `black` 25.1.0 (it exits 2 under any other version), and requires the package file to equal
   the result byte for byte. This is stricter than the note's token-for-token recommendation.
   - D-imp maps only the module path of an `ast`-found import, at any depth, and only to a
     module that exists.
   - D-str maps a dotted path only as the whole literal, quoted inside a literal, or as the module
     of an import inside a literal, and only to an existing module or a top-level name of one.
   - D-tool and D-root are exact substitutions, restricted to the files they name.
   - D-int rebuilds the module from the named definitions and the imports they use.
   - No rule names a line number.
5. **E3, the check bites.** (a)–(e), replayed from the log, each exit 1 naming the line
   (`ShardedPool.py:953`, `schema.py:52`, `Datastore.py:155`, `shard_paths.py:101`,
   `shard_key_audit.py:19`). The orchestrator's own, `DEFAULT_STRING_LENGTH = 255`, exits 1 naming
   `defaults.py:6`. The tree was clean after each.
6. **E4, the tests.** `Ran 90 tests … OK`. Per module, the set of `Class.test_name` equals SGK's
   at `6f7f291` (7, 4, 10, 22, 26, 5, 3, 11). Read in full: the D-tool and D-root hunks. Every
   subprocess test still runs from its unrelated `cwd` with `PYTHONPATH` removed, and still asserts
   what it did.
7. **E5, isolation.** From the scratchpad with `PYTHONPATH` unset, the four package imports
   succeed, and `import Datastore` raises `ModuleNotFoundError`. The guard walks every module with
   `ast`, at any depth, and takes a relative import as the package.
8. **E6, the pins.**
   - `key_id` at `ShardedPool.py:3561`: **no test fails**, as the log says.
   - `import numpy` in `store_reader.py`: the guard's first test fails.
   - Uninstalling the package: 19 failures, every subprocess test of the three tool modules.
   - After `pip install -e .`, the suite is 90 OK again.
9. **E7, the records.** The log has every section of README §5.1, `pip freeze`, the check's
   output, the D-tool list, the counts (0 → 90; SGK 88), and §4.6's places for the four inherited
   issues. `PROVENANCE.md` has the prompt's §2.8 items, with the right subject line. `black
   --check` is clean on `datastorekit/` and `docs/extraction/`.

*Where the note was wrong, and the agent right.*
- `_timing.py` also needs `from traceback import print_tb`, which `WallclockTimer.__exit__` uses.
  The note said `time` was the only import.
- `config/defaults.py` is 203 lines, not one; only `DEFAULT_STRING_LENGTH` is taken.

*Issues.*
- The agent opened `[01-package-prose-names-sgks-layout]`, as the note expected.
- It also opened `[01-ported-tests-use-sgk-table-names]`. It is a real finding under `CLAUDE.md`
  and rule 4, and it is kept.
- **The review opens a third**, `[01-no-ported-test-pins-the-shard-key-assignment]`. The prompt
  called the `key_id` result "a finding for 03". The log recorded it only under its observations,
  and the defect it would catch is the one that motivated the campaign. The index goes to 7.

*Handed on to 02's author.* `compare_with_source.py` lists a file under `datastorekit/` that is
neither in `FILES` nor in `NEW_FILES` as "NOT ACCOUNTED FOR", but still exits 0. The prompt
required failure only for a missing file. 02 adds the first files with no source, and is the
natural place to make an unaccounted file a failure. Recommended, not opened.

*Residue fixed in this follow-up:* "this commit" → `8bc60a5` in the log, the board and
`prompts/INDEX.md`; README §2's status for 01; this paragraph and the notes line.

**Orchestrator review of prompt 02 (2026-10-07).** Dispatched from `737ad6e` to one Opus
subagent, with the note's four corrections and two additions. The agent was cut off once by a
usage limit, with its work uncommitted; it was resumed with its context, and committed once.
Reviewed against its commit `e988e69`, with nothing landed after it. **Every check of the note's
§3 passed**, and acceptance 1–4 are met. No stop condition fired.

*At dispatch.* The note's gate held at `737ad6e`. The tree was clean, and the only worktree was
this checkout. The suite gave `Ran 90 tests … OK`, and the check exited 0 over 30 files. SGK's
frozen files and its stand-in pool were unchanged from `6f7f291` to SGK `HEAD` (`b510bc9`). No
Ray process was up.

*The checks.*
1. **Scope.** `e988e69` touches 16 files: the prompt's §6 list and the records. No file under
   `datastorekit/` outside `tests/`, no `venv/`, `*.egg-info`, `__pycache__` or scratch file.
2. **E1, the contract.** Every constructor argument, `register()` key, hook, declaration field,
   layer-owned name and entry point the review re-derived is in `docs/client-contract.md`.
   Five "when wrong" lines were read and hold: `stepping` (`SQL/Datastore.py:753-755`),
   `owner_column` (`SQL/schema.py:206-219`), `monotone_flags` (`:229-255`), `validated_column`
   (`:268-283`) and `job_name` (stored at `SQL/ShardedPool.py:138`, read by nothing). The five
   replicated-only items say so. No client's name or table is in it.
3. **E2, the roles.** Read from the registry. `validated_column`, `revalidate`, `owned_serials`
   and `validate_on_startup` are on the replicated `Gadget`, `owner_column` on the replicated
   `GadgetPart`, and `monotone_flags` on the replicated `keypoint`. `Sample` is sharded on `"k"`,
   with `validate_on_startup`, `read_batch`, a nullable `cross_shard` parent and a `ParentSet`.
   The polymorphic parent is `Gadget`'s `frame`. The proxy is `keypoint_alias`. The `stepping`
   forms are on `keypoint_alias`, `dial_setting` and `knob_setting`. `ephemeral_probe` registers
   `None`. `read_table_config` gives `tables_arg` both ways. `__all__` is exactly the nine names.
4. **E2, by running.** `build_store` (3 shards) in a scratch `tempfile` directory fills all 13
   tables. `read_inventory` reads nine classes with no problem, and `ray.is_initialized()` is
   false throughout.
5. **E3, the stand-in pool.** Against SGK's `:1-418`, the only hunks are D-str's three module
   paths (`:43-45`), and D-split's two imports and two renames.
6. **E4, U8.** The word diff of the three files changes exactly the 15 lines, each inside a
   string literal only. Per module, the set of `Class.test_name` of `737ad6e`'s 90 is unchanged
   (by `ast`). `Ran 109 tests … OK`.
7. **E5, the check.** It exits 0 over 31 files with 7 declared with no source: D-imp −50/+50,
   D-str −7/+7, D-tool −26/+22, D-root −8/+6, D-fix −15/+15, D-split −169/+8, D-int −222/+11,
   D-fmt −3/+0, unclassified 0.
   - By reading: D-fix and D-split are transformations of the source, restricted to their files
     (D-split also to its two methods), and an unaccounted or missing file makes `main` return 1.
   - (a)–(i) were replayed in `bash`, and each exits 1. (a)–(e) name the same lines as at 01's
     review. (h) is reported as NOT ACCOUNTED FOR.
   - The orchestrator's own breakage also exits 1, naming `standin_pool.py:293`: a sixth name
     added to D-split's registry import.
   - The tree was clean after each.
8. **E6, the tests bite.**
   - (j) fails two coverage tests.
   - (l) fails `test_audit_of_the_copy_attaches_the_copys_shard`.
   - (m) fails `test_a_replicated_get_is_written_on_the_pinned_controller_then_copied`.
   - (k) and (n) fail nothing, as the log records, and (k)'s issue is open.
9. **Isolation.** From the scratchpad, with `PYTHONPATH` unset, both of §3.3's imports succeed,
   and Ray is not initialised. The import guard passes over the new files.
10. **E7, the records.** The log has every section of README §5.1 and each §4.4 addition,
    including a role table with a row per imported name. The board and the index count 8, and
    match. `black --check` (25.1.0) is clean.

*Where the note was wrong, and the agent right.*
- `QCD_Cosmology` is not in SI's registry. The note repeated the prompt's claim that all three
  clients share it.
- `validate_on_startup` is read for replicated classes as well, by the pool's own prune.
- The drop groups. The note read §2.7's "accepts each group as the client declares it" as
  `dependent_tables` returning `[]` for each group. The agent built the groups for what 04's
  `test_drop_refuses_dangling_references` needs: a dependent reached through a declared parent
  alone, one through a foreign key alone, and one transitively. Only `samples` is closed on its
  own. `dependent_tables` accepts every group (none raises), and the test asserts each group's
  measured dependents. This reading is kept: it fits the prompt's words, and the note's would
  have left 04 nothing to refuse.

*Issues.*
- `[01-ported-tests-use-sgk-table-names]` is closed.
- The agent opened `[02-no-test-reaches-revalidate]`, as the note expected.
- It also opened `[02-an-unsupplied-sharded-table-raises-keyerror]`. The review confirms it:
  `SQL/ShardedPool.py:1015` indexes `self._sharded_tables` by the very rows it has just found
  missing.
- The review adds a measurement to `[01-no-ported-test-pins-the-shard-key-assignment]`.
  `_assign_shard_keys` is now reached, but the `key_id` binding stays invisible while keys are
  assigned in serial order; the index hook is corrected.
- The index stays at 8.

*Residue fixed in this follow-up:*
- "this commit" → `e988e69` in the log, the board and `prompts/INDEX.md`;
- README's header, and its §2 row and status for 02. The row is amended for correction 1, so that
  03's author reads the roles as they were built;
- this paragraph, the notes line, and the issue measurement above.

**Orchestrator review of prompt 03a (2026-10-07).** Dispatched from `f7f053d` to one Opus
subagent, with the note's two corrections and two additions. Reviewed against its commit
`11247c7`, with nothing landed after it. **Every check of the note's §3 passed**, and acceptance
1–4 are met. No stop condition fired.

*At dispatch.* The note's gate held at `f7f053d`. The tree was clean, and the only worktree was
this checkout. The suite gave `Ran 109 tests … OK`, and `compare_with_source.py` exited 0 (31
compared, 7 with no source). SGK's `Datastore/`, `tools/`, `utilities.py` and
`config/defaults.py` were unchanged from `6f7f291` to SGK `HEAD` (`b510bc9`). No Ray process was
up. Before dispatch the orchestrator probed (i) and (j) from the scratchpad: each could bite on
the neutral client.

*The checks.*
1. **Scope.** `11247c7` touches 11 files: the four test modules, `build.py`, the two checks, the
   log, the board, the index and `prompts/INDEX.md`. Nothing under `datastorekit/` outside
   `tests/`, no change to `standin_pool.py`, `objects.py`, `factories.py`, `registry.py` or
   `test_neutral_client.py`, and no `venv/`, `*.egg-info`, `__pycache__` or scratch file.
2. **E1, the names.** By the orchestrator's own `ast` walk, each module's set of `Class.method`
   (25, 41, 10) and each class's bases equal SGK's at `6f7f291`. The 109 are unchanged by name
   from `0d02ea6`. `Ran 188 tests … OK`.
3. **E2, the port check, by reading.** It reads SGK with `git show 6f7f291:` and writes nothing.
   `PORTED` names the three modules, and `NAME_MAP` is empty. The skeleton is taken in source order
   at any depth, nested functions apart and lambdas included. It counts `assert*`/`fail*` calls,
   `raise AssertionError` and `subTest`. Every asserting function is compared by qualified name,
   including `tearDownModule` and helpers such as `run_case` and `refused_reopen`. A new function
   that asserts fails. The exit codes are 0, 1 and 2.
   - It counts an assertion call on any receiver, not only `self`'s: wider than §2.4, and kept
     (log §2 item 5).
4. **E2, by running.** Both checks exit 0. The port check's output equals the log's line for
   line: 125, 148 and 74 assertions in 32, 52 and 16 functions. `compare_with_source.py`'s totals
   are 02's unchanged (D-imp −50/+50 … D-fmt −3/+0), over 31 compared, 3 `PORTED` and 8 with no
   source.
   - (a)–(e) and (o), replayed from the log, each exit 1, naming the test or the file.
   - The orchestrator's own breakage, one `assertEqual` deleted from
     `_ReconcileTestCase.refused_reopen`, exits 1, naming the helper at position 3.
   - The tree was clean after each.
5. **E3, R-map and R-value, by reading.** The diff of `test_prune_at_open` against SGK was read in
   full, and `TestKillAndReopen` and the base classes of the other two modules. Every change is of
   a kind the port table names. R-value keeps SGK's distinctions: tolerances 1e-6, 1e-9 and 1e-10
   become dial levels 6, 9 and 10; scales 1.0 and 2.0 stay. Corrections 1 and 2 are applied as
   the note states. `REPLICATED` filters the registry on `register() is not None`, and the prune
   fixture's Sample is stored validated. The only R-count in a test (#65) is `REPLICATED` itself.
6. **E3, control flow, by measuring.** The orchestrator's own `ast` comparison covers all 158
   functions of the three modules. For each, the sequence of `If`, `For`, `While`, `With` (with
   its item count), `Try`, `Return`, `Raise`, `Break`, `Continue`, conditional expressions,
   comprehensions and nested `def`s equals SGK's. No function is added or missing. This covers the
   port check's blind spot (log §7 item 1) for 03a.
7. **E4, the client.** `build.py` changes by addition only: `make_framed_gadget`,
   `make_sample_on`, two constants and an import. The four modules with `test_neutral_client` ran
   eight times, `Ran 98 tests … OK` each time.
8. **E5, the layer.** Replayed (f)–(i). The failing tests are exactly the log's:
   - (f): `TestWriteOverASetRecord.test_every_path_refuses`;
   - (g): two `TestKillAndReopen` flag tests;
   - (h): one prune test and one reconcile test;
   - (i): `test_validate_of_a_background_model` (three subtests) and
     `TestPruningAfterRepair.test_an_interrupted_validate` (two).

   (f), (g) and (i) show as errors, not failures. Each is the mutated layer's own `RuntimeError`
   or `ReplicatedDivergence`, raised from test code, not a broken fixture.
9. **E6, the closures.** `test_shard_key_assignment.py` assigns keys in the order 2, 3, 1. It
   reads the primary's `shard_keys` with `_read` after closing, and compares it with the map
   before closing and the reopened map. It finds each Sample on that shard's file alone, and
   through the reopened pool. Replayed:
   - (j) fails its three tests on the map comparison and the Samples' shards;
   - (i) fails `test_validate_of_a_background_model`.

   The module passed 40 runs of 40 on the unmutated tree.
10. **E7, the records.** The log has every section of README §5.1 and each §4.4 addition: a port
    table of 76 rows, the map, the hazards, the corrections, the helpers, both checks' output,
    109 → 188 and (a)–(j) and (o). The index counts 6 rows and its header says 6. `black --check`
    (25.1.0) is clean. The vocabulary grep finds none of the 80 client names in the four modules.
    No Ray process was up afterwards.

*Where the note was wrong, and the agent right.*
- (o)'s example pair: the first two assertion calls of
  `test_a_sharded_store_stamps_its_own_time_and_writes_no_record` are both `assertEqual`, so
  swapping them changes no skeleton. The agent swapped the fourth and fifth.
- The sharded test at `test_reconcile_at_open.py:794` is in `TestNoRecordRefuses`, not
  `TestRecordDoesNotExplain`.
- The prose figure. The orchestrator's 108 in 24 was a looser reading of the pattern. The agent's
  method (log §8) reproduces 01's 101 and 02's 104, and gives 114 in 23 after 03a. The review did
  not re-derive it independently.

*Observations, not opened.*
- **(j) reaches `test_prune_at_open` only by chance.** Its pools do not pin a controller, so a
  keypoint get may run on an actor whose serial lease starts at 501. That is inherited from SGK,
  whose redshift serials vary the same way. Under (j), a varying set of prune tests is then
  refused at the reopen. The new module catches (j) every time, and the unmutated tree passed
  every run. Recorded, not opened.
- **The port check still passes a swap of two assertion calls of the same name.** Check 6 does
  not see that either. It is stated in the log (§7 item 1).

*Handed on to 03b's author.*
- Correction 1's `REPLICATED`, which `test_one_timestamp_per_write` inherits through 03a's
  classes.
- Correction 2's reading of the sharded role: Sample stored validated wherever a store is reopened
  under a prune.
- The port check compares bases by name as written, and counts only test methods defined in the
  module. `test_one_timestamp_per_write` subclasses classes of other modules, so its inherited
  tests are not compared there. 03b decides whether they need to be.
- The wider receiver rule (log §2 item 5) brings 03b's `super().assertIdentical()`,
  `mock.assert_not_called()` and `unittest.TestCase().assertRaises` into the skeleton.

*Issues.* `[02-no-test-reaches-revalidate]` and `[01-no-ported-test-pins-the-shard-key-assignment]`
are closed; `[01-package-prose-names-sgks-layout]` stands at 114 lines in 23 files. The review
opens nothing, and the index stays at 6.

*Residue fixed in this follow-up:*
- "this commit" → `11247c7` in the log, the board and `prompts/INDEX.md`;
- README's header, and its §2 status for 03a;
- this paragraph and the notes line.

**Orchestrator review of prompt 03b (2026-10-08).** Dispatched from `72cf34a` to one Opus
subagent, with the note's one correction and four additions. The agent was cut off once by a
usage limit, with its work uncommitted; it was resumed with its context, and committed once.
Reviewed against its commit `0d5380c`, with nothing landed after it. **Every check of the note's
§3 passed**, and acceptance 1–4 are met. No stop condition fired.

*At dispatch.* The note's gate held at `72cf34a`. The tree was clean, and the only worktree was
this checkout. The suite gave `Ran 188 tests … OK`, and both checks exited 0. SGK's `Datastore/`,
`tools/`, `utilities.py`, `config/defaults.py`, `config/sharding.py` and the probe were unchanged
from `6f7f291` to SGK `HEAD` (`b510bc9`). No Ray process was up. Before writing the note the
orchestrator probed a read-only `build_store` from the scratchpad. It found that a miss's payload
is keyed by column name, that `keypoint` can play both of SGK's write roles, and that a missing
`Sample` or `Tessera` table is refused with the table named. It also re-ran 03a's 19 tests under
the ticking clock.

*The checks.*
1. **Scope.** `0d5380c` touches 18 files: the five ported modules, `reader.py`, the client's four
   files, `test_neutral_client.py`, the contract, the two checks, the log, the board, the index
   and `prompts/INDEX.md`. Nothing under `datastorekit/` outside `tests/`. No change to
   `standin_pool.py`, `shard_store_fixtures.py` or 03a's four modules. No `venv/`, `*.egg-info`,
   `__pycache__` or scratch file.
2. **E1, the names.** By the orchestrator's own `ast` walk, with U12's four renames applied, each
   module's test methods and each class's bases equal SGK's at `6f7f291`. The only other name
   change is a helper's, below. `Ran 268 tests … OK`. The loader runs 12, 23, 28, 12 and 5.
3. **E2, the port check, by reading.** `compare_ported_tests.py` gains five `PORTED` pairs and
   `NAME_MAP`'s four entries, keyed by `test_read_only_pool.py`, and nothing else.
   `compare_with_source.py` changes only in `FILES` and `NO_SOURCE`.
4. **E2, by running.**
   - Both checks exit 0. The port check gives 12/7/16/79, 23/5/27/138, 1/9/5/7, 12/3/14/28 and
     5/3/7/21, the note's measurement of SGK. 03a's three are unchanged.
   - `compare_with_source.py` gives 31 compared, 8 `PORTED` and 9 with no source.
   - (a)–(d) and (p), replayed, each exit 1, naming what the log says.
   - The orchestrator's two exit 1: the `assertFalse` deleted from
     `_TickingClock.assertNoShardClock` (named, position 1), and `test_routing_rule` renamed back
     to `test_GkSourcePolicy` (named both ways).
   - The tree was clean after each.
5. **E3, R-map and R-value, by reading.** The miss tests read the payload by column name. The
   deleted gauge (exponent 12) and rule (`rule-high`) are the ones the sequence reaches fourth and
   second, as SGK's were. `test_versioned_rows_carry_the_serial_on_every_shard` keeps its two
   gauge gets, with exponents 10 and 9. Deviation 8 (`test_object_validate` asks for the Gadget
   with the run's tag, where SGK passed `tags=[]`) is an argument change the neutral factory
   requires, and the test still validates an available, stored model.
6. **E3, control flow, by measuring.** The orchestrator's own `ast` comparison covers all 116 of
   SGK's functions in the five modules. Each one's sequence of compound statements, returns,
   raises, comprehensions, lambdas and nested `def`s equals SGK's, except `_load_probe`, which
   goes by the note's direction.
7. **E4, the client.** `objects.py`, `factories.py`, `registry.py` and `build.py` remove no line.
   Both classes come after `knob_setting` in `factories` and `replicated_tables`, in no drop
   group, `read_table_config` or `serial_batch_sizes`. `test_neutral_client.py` changes in `KEPT`
   and `counts` only. The contract changes in counts and class lists only. 03a's modules are
   byte-identical, and pass.
8. **E5, the reader.**
   - `change_counter`, `table_counts`, `file_state`, `state_delta`, `ReplicatedWriteLog`, `Step`
     and `quiet` are the probe's, identical by `ast`. `Recorder` is the probe's without `print`
     (deviation 2).
   - `reader.py` makes no assertion.
   - Run by the orchestrator from the scratchpad:
     - on a read-write copy, only `store.sqlite` changes, with 18 `_replicated_write` calls and
       nothing inserted;
     - on a read-only copy, nothing changes, and every step's outcome equals the read-write
       run's;
     - the sequence stops at `[knob] Gadget` with its own message.
   - With each of the four classes' rows deleted, the `ReadOnlyMiss` comes from the step the test
     expects (the frames, the gauges, the rules), with the payload it asserts.
9. **E6, the layer.** Replayed (e)–(j). The failing tests are exactly the log's:
   - (e): 77 tests (139 failures and errors), including 19 of `test_one_timestamp_per_write`'s 28
     on all three paths;
   - (f): `TestInsertBeforeSetVersion.test_a_versioned_insert_raises_names_the_class_and_writes_nothing`;
   - (g): the five `TestEachMissRaisesReadOnlyMiss` tests;
   - (h): ten of `test_absolute_shard_record_refused`, and three of 01's;
   - (i): the two prefix tests of `test_closed_store_refusals`;
   - (j): `test_every_connection_is_opened_read_only`.
10. **E7, the records.** The log has every section of README §5.1 and each §4.4 addition: a port
    table of 53 rows and the 27 inherited, the map, the hazards, the step table, both checks'
    output and the breakage record. The index has 6 rows, and its header says 6. `black --check`
    (25.1.0) is clean. Neither vocabulary grep finds anything in the five modules or the
    client. No Ray process was up afterwards.

*Where the agent went beyond the prompt, and it is kept.* §2.1 says "No other name changes". The
agent renamed `TestOtherWritesRaiseReadOnlyWrite`'s helper `lcdm` to `dial_frame` (log §2 item
14). The prompt's stop condition is about a ported test's name, and `lcdm` is a helper that
asserts nothing and is named for SGK's `LambdaCDM`. The rename is kept, and recorded here.

*Observations, not opened.*
- **Three of the log's eleven breakage diffs could not be replayed as recorded.** (b), (p) and (h)
  had lost their trailing blank context lines in the log, so `git apply` refused them; each
  replayed with `--recount`. They were regenerated from the tree, making the same changes, and
  replaced in the log in this follow-up. All eleven now pass `git apply --check` as recorded.
- **A comment now attributes the neutral count to SGK's audit.** In
  `test_the_instrument_counts_…`, "enters _replicated_write 18 times (audit R2 Run 1)" gives the
  neutral sequence's count beside SGK's audit run, which recorded 21 (log §2 item 12). The
  sentences after it mix the neutral stop with R2's serials. This is prose only, and is left for
  the rewrite of `[01-package-prose-names-sgks-layout]`.

*Issues.* `[01-package-prose-names-sgks-layout]` stands at 124 lines in 28 files, by log 03a §8's
method, which reproduced 114 in 23 at `72cf34a`. The review did not re-derive it independently.
Nothing was opened or closed, and the index stays at 6.

*Residue fixed in this follow-up:*
- "this commit" → `0d5380c` in the log, the board and `prompts/INDEX.md`;
- the three breakage diffs above, in the log;
- README's header, and its §2 status for 03b;
- this paragraph and the notes line.

## 2. Gates outside this repository (README §7)

| Gate | Status |
|---|---|
| **G1**: SGK `datastore-generic-followup` closed; the import commit fixed | ✅ 2026-10-07: closed at `6f7f291` (03 landed as `086c81a`); the import commit is `6f7f291` |
| **G2**: SGK adopted `v0.1.0`, fingerprint reproduced | ⬜ |
| **G3**: CPBH adopted `v0.2.0` | ⬜ |
| **G4**: SI adopted | ⬜ |

## 3. Active and unresolved issues

The issues the layer carries from SGK are indexed in
[`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) §1.2. They stay on SGK's boards, and are out
of scope here (README §1). Log 01 §4.6 records where each one's code is in the package.

- **[01-package-prose-names-sgks-layout]** *(opened 2026-10-07 by prompt 01)*
  - **The defect.** Comments and docstrings in the package, imported unchanged (D-str leaves prose
    alone; README §5 rule 8), still name SGK's layout: `Datastore/…` and `tools/…` paths, dotted
    mentions such as ``Datastore.SQL``, SGK campaign paths (`prompts/…`, `docs/…`) and "the
    repository root". Two sentences describe the `sys.path` bootstrap that D-tool removed, and are
    now false: `tools/sharded_store.py:25-26` ("It puts its own repository root on sys.path, so it
    runs from any directory with no PYTHONPATH.") and `tools/shard_key_audit.py:25-26` ("the
    repository root is put on sys.path below so that the script still runs standalone, from any
    directory, with no PYTHONPATH.").
  - **Measured** (2026-10-07, at `8bc60a5`; comment and string tokens matching
    `Datastore/|tools/|prompts/|docs/|Datastore.<module>|repository root|REPO_ROOT|ObjectFactories|RunRegistry|main.py|config.defaults|utilities.py`,
    the two internalised modules' provenance docstrings excluded): **101 lines in 19 files**.
    `SQL/ShardedPool.py` 27, `SQL/Datastore.py` 12, `SQL/schema.py` 10, `store_inventory.py` 8,
    `replication.py` 6, `store_reader.py` 5, `tests/test_shard_key_audit_copy.py` 5,
    `SQL/factory_base.py` 3, `tools/shard_key_audit.py` 3, `tests/test_shard_key_audit_refusals.py`
    3, `tests/test_shard_paths.py` 3, `tests/test_sharded_store_script.py` 3,
    `tests/test_shardedpool_shard_paths.py` 3, `contract.py` 2, `tools/sharded_store.py` 2,
    `tests/test_delete_store.py` 2, `tests/test_shard_file_name.py` 2, `shard_paths.py` 1,
    `tests/test_copy_move_store.py` 1. Reproducible with the pattern above.
  - **Impact.** Documentation only: no behaviour. A reader of the package is pointed at files and
    campaigns that do not exist here, and two docstrings misdescribe how the tools find the package.
  - **Next step.** Rewrite the prose once rule 8 lifts (after 05), so that 01–05's equivalence check
    stays mechanical. Unassigned.
  - **Measured by 02 (2026-10-07):** **104 lines in 20 files.** Two additions: the comment
    `tools/shard_key_audit.py:188` (`e.g. "wavenumber"`, a name of SGK's table, moved here from
    `[01-ported-tests-use-sgk-table-names]`; `tools/shard_key_audit.py` 3 → 4); and the stand-in pool
    `tests/standin_pool.py` (new, its prose SGK's under D-split), 2 lines the pattern matches (`:4`,
    `:5`: `docs/datastore-integrity-audit/…`, `prompts/datastore-integrity`). Seven more of its lines
    name SGK's layout or campaigns outside the pattern: `:2` (`var/`), `:195`, `:225`, `:252`
    (`a3-v2-readiness prompt 02`), `:286` ("the production table lists"), `:314`, `:397`
    ("prompt 02"). Log 02 §5 item 5.
  - **Measured by 03a (2026-10-07):** **114 lines in 23 files.** 02's figure, 104 in 20, was
    first reproduced at `03fa97a` (method: log 03a §8; the pattern above with "`Datastore.<module>`"
    read as a module of the layer, this repository's own `docs/` paths not counted, and 02's moved
    comment counted by hand). The three ported modules add 10 lines, all SGK's prose ported
    unchanged under 03a §2.1: `tests/test_reconcile_at_open.py` 5 (`:2`, `:9`, `:733`, `:1061`,
    `:1092`), `tests/test_replicated_write.py` 3 (`:2`, `:6`, `:615`), `tests/test_prune_at_open.py`
    2 (`:2`, `:12`); `tests/test_shard_key_assignment.py` adds none. Their SGK references outside
    the pattern (`var/`, `utilities.WallclockTimer`, SGK's commit `e53f323`, "log 01", "the audit
    probe", `hot_journal_probe.py`) are listed in log 03a §7 item 2.
  - **Measured by 03b (2026-10-08):** **124 lines in 28 files.** 03a's figure, 114 in 23, was first
    reproduced at `72cf34a` by log 03a §8's method. The five ported modules add 10 lines, all SGK's
    prose ported unchanged under 03a §2.1: `tests/test_read_only_pool.py` 5 (`:2`, `:5`, `:29`,
    `:71`, `:816`), `tests/test_version_row_at_open.py` 2 (`:2`, `:10`),
    `tests/test_absolute_shard_record_refused.py` 1 (`:4`), `tests/test_closed_store_refusals.py` 1
    (`:3`), `tests/test_one_timestamp_per_write.py` 1 (`:3`); `tests/client/reader.py` and the
    client's other files add none. Their SGK references outside the pattern (`var/`, "audit
    R1/R2/V1", "QSI", `resolve_run_selection`, SGK's commit `b04671f`) are listed in log 03b §7
    item 1.
- **[02-an-unsupplied-sharded-table-raises-keyerror]** *(opened 2026-10-07 by prompt 02)*
  - **The defect.** Reopening a store whose primary records a sharded table that the constructor's
    `sharded_tables` lacks raises a bare `KeyError('<table>')` from `_read_shard_data`
    (`datastorekit/SQL/ShardedPool.py:1015`, `attr = self._sharded_tables[row.table]`), before the
    list it prints and the `RuntimeError` meant for that case (`:1022-1045`) are reached. Probed with
    `shard_store_fixtures` (log 02 §5 item 1).
  - **Impact.** The open is still refused; the refusal does not say why. Inherited from SGK
    unchanged.
  - **Next step.** Fix once rule 8 lifts (after 05), with a test that opens such a store. Unassigned.

## 4. Resolved issues

- **[01-no-ported-test-pins-the-shard-key-assignment]** *(opened 2026-10-07 by the orchestrator's
  review of 01)*
  - **The defect.** No test in the suite reaches `ShardedPool._assign_shard_keys`
    (`datastorekit/SQL/ShardedPool.py:3505`). Binding `"key_id"` in place of `"key_serial"` in its
    insert (`:3561`) fails none of the 90 (log 01 §4.4, replayed at the review). A probe raising
    at the method's first line also fails none.
  - **Impact.** That binding is the shard-key bug of README §0: the saved shard map could differ
    from the one in memory after a reopen. It was fixed in SGK (`2610abe`) and SI (`20d9a61`), and
    was still in CPBH on 2026-10-07. The package carries the fix, but nothing here would catch its
    return.
  - **Next step.** 03 ports the write-path tests onto the stand-in pool. Its author checks whether
    any of the 129 reaches `_assign_shard_keys` through the package. If none does, 03 adds one
    that writes a sharded object, reopens the store, and compares the shard map on disk with the
    one in memory, and the `key_id` mutation is one of its breakages. Unassigned until 03 is
    written.
  - **Measured by the review of 02 (2026-10-07).** The defect's first sentence no longer holds:
    `build_store`'s gets of `keypoint` reach `_assign_shard_keys` (`SQL/ShardedPool.py:687`,
    `:3246`). But the `key_id` binding still fails none of the 109 (log 02 §4.5 (n), replayed at
    the review). SQLAlchemy ignores the unknown `key_id` parameter, so `key_serial`
    autoincrements, and since the neutral client's keys are assigned in serial order from 1, the
    saved map equals the one in memory. The test 03 adds must assign shard keys out of serial
    order (for example, get a later `keypoint` first), or the mutation stays invisible.
  - **Assigned (2026-10-07):** to prompt 03a (U10). None of 03a's 76 SGK tests compares the
    saved shard map with the one in memory, so 03a adds `test_shard_key_assignment.py`, which
    assigns shard keys out of serial order and which the `key_id` binding must fail (03a §2.5).
  - **Closed (2026-10-07) by prompt 03a** (`11247c7`, log 03a §4). The new module
    `datastorekit/tests/test_shard_key_assignment.py` assigns shard keys out of serial order
    (a get of keypoint A killed on a replica, the store reopened so that the check at open copies
    A with no key, then B and C got and A's key assigned last: the order 2, 3, 1), and requires
    that the map saved in the primary's `shard_keys` equals the map the pool held before closing
    and the reopened pool's, and that every Sample is on the shard that map names after the
    reopen. 01's `key_id` diff (`SQL/ShardedPool.py:3561`) fails its three tests on every run (log
    03a §6.2 (j)).

- **[02-no-test-reaches-revalidate]** *(opened 2026-10-07 by prompt 02)*
  - **The defect.** No test reaches a factory's `revalidate`. Its one call site is
    `ShardedPool._recompute_validated` (`datastorekit/SQL/ShardedPool.py:1992`), called by the check
    at open only after an interrupted validate of a replicated class that declares
    `validated_column`. Making the neutral client's `Gadget_factory.revalidate` return `True`
    without writing fails none of the 109 tests (log 02 §4.5 (k), the diff there).
  - **Impact.** The repair that recomputes a validated flag at open could be broken, or a client's
    `revalidate` could write nothing, and the suite would pass.
  - **Next step.** 03 ports `test_reconcile_at_open` (41 tests), which interrupts a validate of a
    replicated owner. Its author checks that a test there reaches `revalidate` on the neutral
    client's `Gadget`, and makes (k)'s diff one of its breakages. Unassigned until 03 is written.
  - **Assigned (2026-10-07):** to prompt 03a (U10). `test_reconcile_at_open`'s
    `TestKillAndReopen.test_validate_of_a_background_model` expects "validated recomputed"
    actions, and on `Gadget` reaches `revalidate`; (k)'s diff must fail it (03a §2.5).
  - **Closed (2026-10-07) by prompt 03a** (`11247c7`, log 03a §4). The ported
    `test_reconcile_at_open.TestKillAndReopen.test_validate_of_a_background_model` interrupts the
    replicated validate of a `Gadget` and expects `"validated recomputed"` actions, which come from
    `Gadget_factory.revalidate`. 02's breakage (k), replayed as 03a's (i), fails it (three
    subtests) and `TestPruningAfterRepair.test_an_interrupted_validate` (both subtests) (log 03a
    §6.2 (i)).

- **[01-ported-tests-use-sgk-table-names]** *(opened 2026-10-07 by prompt 01)*
  - **The defect.** The ported fixture and tests, imported unchanged (README §5 rule 6), use SGK's
    table names: `tests/shard_store_fixtures.py:25-27` (`KEY_TYPE = "wavenumber"`,
    `REPLICATED = ["version", "wavenumber"]`, `SHARDED = {"GkSource": "k"}`);
    `tests/test_shard_key_audit_copy.py` (3 lines) and `tests/test_shard_key_audit_refusals.py`
    (9 lines) create a `wavenumber` table and a `wavenumber_serial` column; and one comment,
    `tools/shard_key_audit.py:188` (`e.g. "wavenumber"`). `CLAUDE.md` says the package names no
    client table.
  - **Impact.** No behaviour: the names are data in hand-built test stores. But 04's vocabulary guard,
    drawn from the clients' registries, would find them, and README §2 does not say whether the 88
    move onto the neutral client's names.
  - **Next step.** 02 or 04 decides: re-fixture these tests onto the neutral client's names, or
    exempt them from the vocabulary guard with a reason. Unassigned.
  - **Assigned (2026-10-07):** to prompt 02, by the user's decision U8 (README §6.2). 02 moves the
    names in the tests onto the neutral client's (§2.4), and moves the one comment in
    `tools/shard_key_audit.py:188` to `[01-package-prose-names-sgks-layout]`, since package prose
    stays unchanged until 05.
  - **Closed (2026-10-07) by prompt 02** (`e988e69`, log 02 §3). The 15 lines moved onto the
    neutral client's names by the map `wavenumber` → `keypoint`, `wavenumber_serial` →
    `keypoint_serial`, `GkSource` → `Sample`, inside string literals only, as whole identifiers:
    `tests/shard_store_fixtures.py` 3, `tests/test_shard_key_audit_copy.py` 3,
    `tests/test_shard_key_audit_refusals.py` 9. The equivalence check accounts for them as D-fix,
    restricted to those three files. The comment `tools/shard_key_audit.py:188` (`e.g.
    "wavenumber"`) is unchanged, and moved to `[01-package-prose-names-sgks-layout]`.
