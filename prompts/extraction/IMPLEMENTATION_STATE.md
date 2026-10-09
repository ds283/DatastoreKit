# extraction campaign — implementation state

**Last updated:** 2026-10-09 · **Status: IN PROGRESS — 9 of 10 prompts written (01, 02, 03a, 03b, 04a, 04b, 05, 06, 07a), 9 landed (01, 02, 03a, 03b, 04a, 04b, 05, 06, 07a); `v0.1.0` tagged on `68db557` after green CI (U23); 06 reviewed; `v0.2.0` tagged on `240028e` after green CI (U28); 07a landed (`dd45243`) and reviewed; 07b is not written.**
G1 holds: the import commit is SGK `6f7f291`. The user took U2–U5 as recommended on 2026-10-07,
U8–U13 the same day, U14–U22 on 2026-10-08, and U6, U23–U32 on 2026-10-09 (README §6.2); U10, U14 and U30 split 03, 04
and 07, each into an a and a b prompt.

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
| **U6** supported range and CI | Python ≥ 3.12, `ray>=2.43`, `sqlalchemy>=2.0.39,<2.1`; GitHub Actions at both ends | **taken** 2026-10-09, at 05's writing |
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
| **U22** the declared facts and a class with no table | two `TestTheRecords` tests give `build_schema` the registry less `register() is None` (R-help) | **taken** 2026-10-08, at 04b's stop |
| **U23** how `v0.1.0` is reached | 05 makes no tag and pushes nothing; the tag is made on 05's commit once CI passes there | **taken** 2026-10-09, at 05's writing |
| **U24** measuring the high end locally | a scratch Python 3.13 venv from PyPI, for the planner and 05's agent | **taken** 2026-10-09, at 05's writing |
| **U25** the neutral client's keyed class | `Tessera` declares `key_on_version` | **taken** 2026-10-09, at 06's writing |
| **U26** keyed lookups on a read-only pool | a lookup serial apart from the insert serial; `set_lookup_version` | **taken** 2026-10-09, at 06's writing |
| **U27** the equivalence check after rule 8 lifts | *(recommended: a declared amended-since-release kind)* | **taken** 2026-10-09, otherwise: `compare_with_source.py` retired at `v0.1.0` |
| **U28** how `v0.2.0` is reached | as U23: no tag or push by 06; tagged on its commit after green CI | **taken** 2026-10-09, at 06's writing |
| **U29** the release SGK adopts | `v0.2.0` directly; G2 reads `v0.2.0` | **taken** 2026-10-09, by the user |
| **U30** splitting 07 | 07a the adoption checklists; 07b verification and close-out | **taken** 2026-10-09, at 07a's writing |
| **U31** SI's stores | rebuilt, not migrated, as D4; SI tags its last commit on the old layer | **taken** 2026-10-09, at 07a's writing |
| **U32** clients that register factory instances | client-side: define the three abstract hooks (CPBH 20 classes, 24 entries; SI 16, 18), or register the class once its hooks need no instance | **taken** 2026-10-09, at 07a's writing |

---

## 1. Prompts

| # | Prompt | Covers | Written? | Landed? | Commit | Log |
|---|---|---|---|---|---|---|
| 01 | [Import the layer](01-import-the-layer.md) | package, 15 files and 2 tools, the two internalised dependencies, 88 tests, import guard | ✍️ yes, 2026-10-07 | ✅ 2026-10-07 | `8bc60a5` | [log](logs/01-import-the-layer.md) |
| 02 | [The neutral test client](02-the-neutral-test-client.md) | `docs/client-contract.md`, the test client, the stand-in pool; 01's tests onto the client's names (U8) | ✍️ yes, 2026-10-07 | ✅ 2026-10-07 | `e988e69` | [log](logs/02-the-neutral-test-client.md) |
| 03a | [Port the replicated-write tests](03a-port-the-replicated-write-tests.md) | 76 tests (replicated write, check at open, prune at open); the port check; the `key_id` pin and `revalidate` | ✍️ yes, 2026-10-07 | ✅ 2026-10-07 | `11247c7` | [log](logs/03a-port-the-replicated-write-tests.md) |
| 03b | [Port the open and read-only tests](03b-port-the-open-and-read-only-tests.md) | 53 tests, 80 run (version row, read-only pool, one timestamp, shard records); the two client classes (U13); the neutral reader sequence (U11) | ✍️ yes, 2026-10-07 | ✅ 2026-10-08 | `0d5380c` | [log](logs/03b-port-the-open-and-read-only-tests.md) |
| 04a | [Port the store and inventory tests](04a-port-the-store-and-inventory-tests.md) | 85 tests (inventory, store schema, reader, foreign keys, schema builder); `real_store_fixtures` and `schema_description` on neutral rows; the schema witness; the client's sharded family (U15) | ✍️ yes, 2026-10-08 | ✅ 2026-10-08 | `7ceed25` | [log](logs/04a-port-the-store-and-inventory-tests.md) |
| 04b | [Port the declaration and registry tests](04b-port-the-declaration-and-registry-tests.md) | 89 of 90 tests (inventory declarations, declared facts, layer registry, drop refusal; U16's one not ported); the package guard with its vocabulary as data (U17); `test_parent_set_members` | ✍️ yes, 2026-10-08 | ✅ 2026-10-08 | `0c66505` | [log](logs/04b-port-the-declaration-and-registry-tests.md) |
| 05 | [Supported versions and CI](05-supported-versions-and-ci.md) | `pyproject.toml` at `0.1.0` with U6's range; the 444 in fresh venvs at both ends and from an installed wheel; the workflow; the README's usage; `v0.1.0` tagged after green CI (U23) | ✍️ yes, 2026-10-09 | ✅ 2026-10-09 | `68db557` | [log](logs/05-supported-versions-and-ci.md) |
| 06 | [Version-keyed lookups](06-version-keyed-lookups.md) | `key_on_version` on `Tessera` (U25); the lookup serial and `set_lookup_version` (U26); 14 tests carrying over CPBH's; the witness `schema_at_extraction-06.json`; `compare_with_source.py` retired (U27); `v0.2.0` tagged after green CI (U28) | ✍️ yes, 2026-10-09 | ✅ 2026-10-09 | `240028e` | [log](logs/06-version-keyed-lookups.md) |
| 07a | [The adoption checklists](07a-the-adoption-checklists.md) | `docs/adoption/`: a README and checklists for SGK, CPBH and SI against `v0.2.0` (U29), measured read-only; `measure_client_imports.py`; instances and abstract hooks (U32); SI's stores rebuilt (U31) | ✍️ yes, 2026-10-09 | ✅ 2026-10-09 | `dd45243` | [log](logs/07a-the-adoption-checklists.md) |
| 07b | Verification and close-out | the campaign's verification document; the campaign closed (U30) | ⬜ | ⬜ | — | — |

**Legend.** ✍️ written · ⏸ held, with what it waits on · ⬜ not written / not landed ·
✅ landed.

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`bd9f461`),
used for 01; [`orchestrator/prompt-02.md`](orchestrator/prompt-02.md) (`737ad6e`), used for 02;
[`orchestrator/prompt-03a.md`](orchestrator/prompt-03a.md) (`f7f053d`), used for 03a;
[`orchestrator/prompt-03b.md`](orchestrator/prompt-03b.md) (`72cf34a`), used for 03b;
[`orchestrator/prompt-04a.md`](orchestrator/prompt-04a.md) (`ae94aaa`, with addenda at `66535b2` and
`74c6343`), used for 04a; [`orchestrator/prompt-04b.md`](orchestrator/prompt-04b.md) (`f79f254`,
with an addendum at `7ee9b6e`), used for 04b; [`orchestrator/prompt-05.md`](orchestrator/prompt-05.md)
(`f69921b`), used for 05; [`orchestrator/prompt-06.md`](orchestrator/prompt-06.md) (`0e524b4`),
used for 06; [`orchestrator/prompt-07a.md`](orchestrator/prompt-07a.md) (`a816632`), used for 07a.

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

**Orchestrator review of prompt 04a (2026-10-08).** Dispatched from `ae94aaa` to one Opus
subagent, with the note's four corrections and five additions. The agent stopped twice, uncommitted,
and was resumed with its context each time:
- at its first step, on 03a's `test_an_interrupted_store`, which the new client breaks (U19, the
  note's correction 5, `66535b2`);
- on `test_schema_builder`, which cannot hold over a class that registers `None` (U20 and U21,
  corrections 6 and 7, `74c6343`).

Reviewed against its commit `7ceed25`, with nothing landed after it. **Every check of the note's
§3 passed**, and acceptance 1–4 are met. No other stop condition fired.

*At dispatch.* The note's gate held at `ae94aaa`. The tree was clean, and the only worktree was
this checkout. The suite gave `Ran 268 tests … OK`, and both checks exited 0. SGK's `Datastore/`,
`tools/`, `utilities.py` and `config/` were unchanged from `6f7f291` to SGK `HEAD` (`b510bc9`). No
Ray process was up. While writing the note the orchestrator probed:
- hazards 2, 6 and 10 on `build_store` and a stand-in pool;
- breakage (h), which already failed two of 03b's tests;
- U18's one line, against the 268.

It also found the `Sample` conflict that became U18.

*The checks.*
1. **Scope.** `7ceed25` touches 21 files:
   - the five modules, the two fixtures and the witness;
   - the client's four files, `test_neutral_client.py`, and `test_reconcile_at_open.py` (U19's 3
     lines only);
   - the contract and the two checks;
   - the log, the board, the index and `prompts/INDEX.md`.

   Nothing under `datastorekit/` outside `tests/`. No change to `standin_pool.py`,
   `shard_store_fixtures.py`, `client/reader.py`, or 03b's modules. No `venv/`, `*.egg-info`,
   `__pycache__` or scratch file.
2. **E1, the names.**
   - By the orchestrator's own `ast` walk, each module's test methods and each class's bases equal
     SGK's at `6f7f291`, with no rename.
   - The fixtures define every public name of SGK's, with the same parameter lists.
   - The 268 test ids of `ae94aaa` are all present, and the 85 new ones split 42, 13, 15, 8 and 7.
     `Ran 353 tests … OK`, and the loader gives the same per module.
3. **E2, the port check, by reading.** `compare_ported_tests.py` gains seven `PORTED` pairs and
   nothing else. `compare_with_source.py` gains the same seven in `FILES` and nothing else.
4. **E2, by running.**
   - Both checks exit 0. The port check's counts equal the note's table of SGK's seven, and the
     eight earlier modules' are unchanged.
   - `compare_with_source.py` gives 31 compared, 15 `PORTED` and 9 with no source.
   - All 13 of the log's breakage diffs pass `git apply --check` as recorded. (a), (b), (m) and
     (c), replayed, each exit 1, naming what the log says.
   - The orchestrator's two exit 1:
     - one `assertIn` deleted from `TestTags.test_a_tag_no_row_carries_is_only_a_store_tag`
       (named, position 1);
     - `RealStore` removed ("class missing from the package").
   - The tree was clean after each.
5. **E3, R-map, R-value and R-count, by reading.** Read in full against SGK, after R-imp:
   - `test_foreign_key_check`, `test_schema_builder` and `test_store_schema`;
   - `test_store_inventory` from `TestTags` to `TestDuplicates`;
   - `test_store_reader`'s word diff.

   Every change is of a kind the port table names.
   - The divergence tests use `routing_rule` (hazard 5).
   - The `changed(...)` sets of `TestTags` follow the neutral references: Trace 4 to its Weave,
     and Gadget 2 to Sample 4.
   - The pair given in reverse declaration order is `["Weave_tags", "Sample_members"]`.
   - `test_the_added_row_is_not_satisfied_by_coincidence` keeps SGK's reason. A wrong foreign key
     from `Sample_members.tessera_serial` to `Sample.serial` would be satisfied by the fixture's
     own member rows and not by the added one (deviation 9).
   - Corrections 1–7 and the five additions are applied as stated.
6. **E3, control flow, by measuring.** The orchestrator's own `ast` comparison covers all 138 of
   SGK's functions in the five modules. Each one's sequence of compound statements, returns,
   raises, comprehensions, lambdas and nested `def`s equals SGK's. In the fixtures, only these
   differ:
   - the row builders `_full_shard0` and `_full_shard1` (new data);
   - `references()`, derived as §2.4 directs;
   - `actor_with_built_schema`'s U20 filter.
7. **E4, the client.**
   - The four files remove two lines: U18's, and one line of `write_every_class`'s docstring.
   - The registry has the six after `Sample_members`, `Trace` and `Weave` in `sharded_tables`, and
     the group `traces`. The other names are unchanged.
   - `Trace`'s frame declares the same `FRAME_TYPES` object as `Gadget`'s (`is`, from the
     scratchpad).
   - `test_neutral_client.py` changes in measured literals only: `MEASURED_DEPENDENTS`, the
     `no_serial` list, the polymorphic count, the `sharded_tables` literal, `counts` and U18's
     Sample flags. `KEPT` is unchanged.
8. **E5, the fixture.**
   - The transcribed functions are SGK's line for line, except:
     - `_ShardKeyType_name`;
     - one docstring count;
     - `relabel_serials`' polymorphic target, read through the declared type map (hazard 8).
   - Run by the orchestrator on `build_full_store`:
     - every table has rows, and every timestamp is `FIXED_TIMESTAMP`;
     - each `part_count`, `step_count` and `member_count` equals its rows;
     - `PRAGMA foreign_key_check` is empty on both shards, and `read_inventory` reads 13 classes
       with no problem;
     - the run tag `fixture-run` is on every tagged record, and `unused-tag` on none;
     - one `Gadget` and one `Trace` are unvalidated, and the `Weave`'s anchor is `None`.
   - `references()` was printed and checked against the foreign keys and specs by hand.
   - Seven `IDENTITY` entries, two of them chosen, five at random, each change their class's
     records with no problem. Two `NON_IDENTITY` entries change none.
9. **E6, the witness.** Recaptured from a copy of `7ceed25`'s tree, with the copy's
   `datastorekit` on the path: byte-identical, 73,842 bytes, SHA-256 `c3536a2b…bad6c`, 21 classes
   without `ephemeral_probe`. It is the only witness in the tree, and `WITNESS` names it.
10. **E7, the layer and the client.** Replayed (d)–(l). The failing tests are exactly the log's:
    - (d): five `TestFloats`;
    - (e): `test_an_orphan_value_row`;
    - (f): three `TestDuplicates`;
    - (g): three failures and two errors in `test_store_schema` and `test_store_reader`;
    - (h): three `test_store_reader` tests (eight failures with subtests), with 03b's two;
    - (i): sixteen in the two witness tests;
    - (j): four;
    - (k): `(cls='Weave', field='strands')`;
    - (l): three failures and seven errors, `test_every_class_has_a_record` among them.

    (g)'s errors are the unrefused open failing later, and (l)'s are `find_row` on the deleted
    rows. None is a broken fixture.
11. **E8, the records.**
    - The log has every section of README §5.1 and each §4.4 addition, including:
      - the 85-row port table;
      - the four data tables (93 → 33, 40 → 17, with the 19 absent);
      - the witness, and the superseded capture.
    - `[01-package-prose-names-sgks-layout]` is 146 lines in 35 files, which the orchestrator
      reproduced by log 03a §8's method.
    - The index had 6 rows, and said 6.
    - `black --check` (25.1.0) is clean, re-run by the orchestrator. No Ray process was up
      afterwards.

*Where the note was wrong, and the agent right.*
- **Correction 3 was itself incomplete.** `build_store`'s dial serials vary from run to run: 1
  and 2, or 1 and 501, at either shard count. The conclusion stands.
- **§2.7's wording, passed on unchecked.** It says the added member row's Tessera is also a
  `Sample` serial on that shard. The test asserts the opposite of the added row, and the
  coincidence of the fixture's own rows (deviation 9).
- **What the note did not foresee.** Its U18 probe changed only `Sample`'s spec, so it could not
  see U19's drop ripple. Its witness plan did not foresee a class that registers `None` (U20).
- **One line range.** The history U21 rewrote is SGK `:16-35`, not `:16-34`.

*Kept, though beyond the prompt's letter.*
- Every full-store `Sample` has an anchor, against §2.4's "and one None" (deviation 11).
  `test_resolve_names_every_parent` cannot hold with a `None` parent on `Sample` in
  `QuadSourceIntegral`'s role. `Weave` and its strands carry the `None` key parents.
- `test_across_shards` loops over an empty chain (deviation 14). Its control flow is SGK's, and a
  `Trace` has no same-shard parent to copy.
- Docstrings and comments that described SGK's rows now describe the neutral ones (deviation 21),
  as 03b's R-map of docstrings did.

*Issues.* **The review opens `[04a-no-test-pins-a-second-parent-set-member]`.** The agent recorded
it as an observation (log §7 item 1). The orchestrator measured it: deleting `Weave`'s `origin`
member (`factories.py:1684`) leaves `Ran 353 tests … OK`. `[01-package-prose-names-sgks-layout]`
stands at 146 lines in 35 files. Nothing is closed. The index goes to 7.

*Residue fixed in this follow-up:*
- "this commit" → `7ceed25` in the log, the board and `prompts/INDEX.md`;
- README's header, and its §2 status for 04a;
- the note's line range;
- this paragraph and the notes line.

**Orchestrator review of prompt 04b (2026-10-08).** Dispatched from `f79f254` to one Opus
subagent, with the note's five corrections and four additions. The agent stopped once,
uncommitted, on two `TestTheRecords` tests that cannot hold over a class that registers `None`
(U22, the note's correction 6, `7ee9b6e`; the user also kept the agent's fifth `NOT_PORTED` rule,
correction 7). It was resumed with its context. Reviewed against its commit `0c66505`, with
nothing landed after it. **Every check of the note's §3 passed**, and acceptance 1–4 are met. No
other stop condition fired.

*At dispatch.* The note's gate held at `a80af57`. The tree was clean, and the only worktree was
this checkout. The suite gave `Ran 353 tests … OK`, and both checks exited 0. SGK's layer was
unchanged from `6f7f291` to `b510bc9`, and CPBH's and SI's `HEAD`s were the prompt's `52142d7` and
`00d254e`. No Ray process was up. While writing the note the orchestrator:
- re-measured §2.2 and probed hazards 7, 8 and 9 on the full store and the stand-in pool;
- rebuilt the vocabulary from the three clients by `git show` and scanned the layer with SGK's
  own scanners: 82 tables, 301 columns, 16 packages, 398 words, one comment hit;
- found that (k) among `store_inventory.py`'s imports is a circular import, and that appended it
  fails none of the 353.

*The checks.*
1. **Scope.** `0c66505` touches 14 files: the five ported modules, `test_parent_set_members.py`,
   the data file, `measure_client_vocabulary.py`, the two checks, the log, the board, the index and
   `prompts/INDEX.md`. Nothing under `datastorekit/` outside `tests/`, nothing in `tests/client/`,
   and no fixture, witness or earlier module.
2. **E1, the names.** By the orchestrator's own `ast` walk, each module's test methods and class
   bases equal SGK's at `6f7f291`, less U16's one test. `Ran 444 tests … OK`, and the loader gives
   25, 25, 20, 11, 8 and 2.
3. **E2, by reading.** `compare_ported_tests.py` gains the five `PORTED` pairs, `NOT_PORTED` with
   its one entry, and §2.5's four rules with correction 7's fifth; `compare_with_source.py` gains
   five `FILES` entries and one `NO_SOURCE`.
4. **E2, by running.** Both checks exit 0: twenty modules with one test declared not ported (25,
   26 and 57 for `test_inventory_declarations`, SGK's counts for the other four), and 31, 20 and
   10. All 16 of the log's diffs pass `git apply --check` and `-R --check` as recorded. (a)–(d),
   (p) and (q), replayed, each exit 1, naming what the log says. The orchestrator's two exit 1:
   one `assertEqual` deleted from `test_each_group_alone_needs_its_measured_dependents`, and
   `_LayerTestCase` removed ("class missing from the package").
5. **E3, by reading.** The two retargeted classes change only in `PROJECT_PACKAGES`,
   `FORBIDDEN_MODULES`, the factory prefix and §2.4's `any(...)` membership expression. U22's
   `WITH_A_TABLE` reaches exactly the two `build_schema` calls. `DECLARED` holds the three; the
   test keeps its "four" name.
6. **E3, control flow.** The orchestrator's own `ast` comparison covers SGK's 154 functions. The
   only differences are the log's: U16's test; the generator of §2.4; the guard's `_clients` and
   `extra_names`, `registry_words`' second comprehension, `layer_files`' single filter, and
   `import_allowed` without SGK's `RayTools` branch (D2).
7. **E4, the data.** `measure_client_vocabulary.py`, run from a copy of `0c66505`'s tree to a
   scratch path, gives the committed file byte for byte: 19,733 bytes, SHA-256 `98af1124…7f332e`.
   It reads the clients only by `git show`, `git ls-tree` and `git rev-parse`. Each client's
   registry keys, column names and packages equal the orchestrator's own measurement, and the
   guard's functions give 80 tables, 300 columns, 16 packages and 398 words.
8. **E4, the guard.** It imports only the standard library and `datastorekit.contract`.
   `KNOWN_HITS` holds the one comment hit with its reason; `assertNoHits` is one `assertEqual`
   against it. `layer_files()` gives 20 files, holding the twelve of `AUDIT_LIST`. A client word
   added to `store_reader.py`'s docstring fails `test_no_string_or_docstring`, naming
   `store_reader.py:2 GkSource`.
9. **E5, the retargeted classes.** (k), appended, fails the four tests correction 1 named; (n)
   fails three, all but `test_reading_records_loads_no_project_module`. The orchestrator's own,
   `import datastorekit.tests.client.factories` appended to `store_reader.py`, fails
   `TestTheLayerImportsNoClient`'s two tests and `test_every_import_is_allowed`.
10. **E6, the issue.** (l) fails both tests of `test_parent_set_members`, on assertions, and
    nothing else.
11. **E7, the layer.** Replayed (e)–(j) and (m) on the full suite. The failing tests are exactly
    the log's, including 04a's `test_every_class_has_a_record` under (e), 02's three subtests
    under (f), and under (h) 4 failures and 26 errors of 02's, 03a's and 03b's prune and repair
    tests. The tree was clean after each.
12. **E8, the records.**
    - The log has every section of README §5.1 and each §4.5 addition, including the 89-row port
      table and (a)–(q).
    - `[01-package-prose-names-sgks-layout]` is 155 lines in 40 files. The orchestrator reproduced
      it by log 03a §8's method, with 102 at `8bc60a5` and 146 at `7ceed25` first.
    - The index has 6 rows, and says 6. `black --check` (25.1.0) is clean. No Ray process was up
      afterwards.

*Where the note was wrong, and the agent right.*
- **`ephemeral_probe` and `build_schema`.** The note checked the class against the inventory, not
  against `build_schema`'s records, and so missed the two tests U22 settled.
- **Correction 4** gave the guard's derived counts; the agent's data file holds only what was
  read (82 keys, 325 column names, 20 packages), with the derived counts in its log. That is
  better: the file is a measurement, and the rule is the guard's.

*Kept, though beyond the prompt's letter.*
- `NOT_PORTED`'s fifth rule and its breakage (q) (correction 7).
- `EXTRA_NAMES` read from SGK's guard into the data file, under SGK.
- Two local variables renamed (`tolerance`, `tk_numeric`) so that the vocabulary grep finds no
  client name outside the guard and its data.

*Observations.* The guard's comment on `_NOT_PROJECT_PACKAGES` reads garbled ("and ``config``,
which "config" is an English word") and still calls `Datastore` and `RayTools` "part of the
layer", which here they are not. It is prose of the kind `[01-package-prose-names-sgks-layout]`
rewrites after 05, and is left for it.

*Issues.* `[04a-no-test-pins-a-second-parent-set-member]` is closed (§4).
`[01-package-prose-names-sgks-layout]` stands at 155 lines in 40 files. Nothing is opened. The
index is 6.

*Residue fixed in this follow-up:*
- "this commit" → `0c66505` in the log, the board and `prompts/INDEX.md`;
- README's header, and its §2 status for 04b;
- this paragraph and the notes line.

**Orchestrator review of prompt 05 (2026-10-09).** Dispatched from `f69921b` to one Opus
subagent, with the note's five corrections and five additions. Reviewed against its commit
`68db557`, with nothing landed after it. **Every check of the note's §3 passed**, and acceptance
1–6 are met. No stop condition fired. Nothing was pushed and no tag exists.

*At dispatch.* The note's gate held at `f69921b`. The tree was clean, and the only worktree was
this checkout. The suite gave `Ran 444 tests … OK`, and both checks exited 0 (31, 20 and 10;
twenty modules, one test declared not ported). SGK's layer was unchanged from `6f7f291` to
`b510bc9`, `origin/main` was `47d3ab1`, and no Ray process was up. While writing the note the
orchestrator:
- ran the 444 at both ends in scratch venvs, with 05's `pyproject.toml` applied to a copy of the
  tree, and counted the 105 unclosed connections at both ends with a wrapper of its own;
- found that the checkout's ignored `build/` and `datastorekit.egg-info/` each put the 41 test
  files into a wheel built in place (correction 1), and that `shard_key_audit` has no `--help`
  (correction 2);
- probed (a)–(f), and the Linux and macOS resolves at both ends.

*Mid-run.* At the user's direction the orchestrator deleted the checkout's `build/` and
`datastorekit.egg-info/` (both ignored and untracked; `venv/`'s editable install keeps its own
metadata). The agent was told, and its log records the deletion as the user's and quotes the
ignored listing before and after.

*The checks.*
1. **Scope.** `68db557` touches exactly `pyproject.toml`, `.github/workflows/tests.yml`,
   `README.md`, the log, the board, `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`. The ignored
   entries are `.idea/`, `venv/` and the five `__pycache__/` directories, with no `build/`,
   `dist/` or `*.egg-info`.
2. **E1.** `pyproject.toml` changes in the version, the two dependencies and the `exclude` line
   only.
3. **E2, `venv/`.** `pip show` says `0.1.0`; both checks exit 0 with 04b's counts; `black --check
   datastorekit docs` leaves 64 files unchanged.
4. **E2, both ends.** The orchestrator's own venvs, made by the workflow's install from
   `git archive 68db557`: 3.12.15 / 2.43.0 / 2.0.39 and 3.13.16 / 2.55.1 / 2.0.46, SQLite 3.53.4
   at both, each `Ran 444 tests … OK`.
5. **E3, the release.** A wheel built from `git archive 68db557`: 96,304 bytes, 25 entries, none
   under `tests/`; `RECORD` SHA-256 `a689847e…652330a` with `Generator: setuptools (84.0.0)`, the
   log's and the note's. Installed at the high pins and run from outside the repository with
   `PYTHONPATH` unset, the 20 modules import from `site-packages`, `datastorekit.tests` does not,
   `sharded_store --help` exits 0, and `shard_key_audit` exits 2 with its usage line naming
   `site-packages`.
6. **E4, the workflow.** It is §2.5's with the patch Pythons: one job, `suite`, on
   `ubuntu-24.04`, `fail-fast: false`, the matrix `low` / `high` read back from `yaml.safe_load`
   equal to the table, `permissions: contents: read`, black on `low` only, and no secrets, cache,
   artefacts, other actions or warning filters.
7. **E5, the issue.** The orchestrator's wrapper on `68db557` gives 105 of 40,874 at both ends, as
   58 / 41 / 6. The board's §3 entry and the index row hold it.
8. **E6, the README.** Every name it mentions imports (`ShardedPool`, `SQLAFactoryBase` and its
   seven hooks, `InventorySpec`, `Parent`, `ParentSet`, `datastorekit.contract`'s two table
   names), every relative link and anchor resolves, and its versions equal `pyproject.toml` and
   the matrix. It shows no code beyond the install pin and the development commands.
9. **E7, the breakages.** (a) in a throwaway venv: `FAILED (failures=19)`, 21 lines of `No module
   named 'datastorekit'`. (b) and (c) dry runs exit 1 naming `sqlalchemy>=2.0.39,<2.1`. The log's
   three diffs apply both ways to an export, and (d) exits 1; (e) builds 90,695 bytes, 22 entries,
   and `sharded_store --help` exits 1 with `No module named 'datastorekit.tools'`; (f) builds
   283,617 bytes, 66 entries, 41 under `tests/`, and `import datastorekit.tests` succeeds.
10. **E8, the records.** The log has every section of README §5.1 and §4.6's additions, the five
    corrections and the additions. The index has 7 rows and says 7.
11. **Nothing left behind.** No Ray process; `git tag -l` is empty; `origin` has `main` at
    `47d3ab1` and no tag.

*Issues.* `[05-a-refused-open-leaves-its-engines-undisposed]` is open (§3). Nothing else is
opened. The index is 7.

*Residue fixed in this follow-up:*
- "this commit" → `68db557` in the log, the board and `prompts/INDEX.md`;
- README's header, and its §2 status for 05;
- this paragraph and the notes line.

*`v0.1.0` (note §5, U23).* With the user's approval of each step, `68db557` was pushed alone as
`main` (a fast-forward from `47d3ab1`), and the workflow ran on it,
[run 37922626418](https://github.com/ds283/DatastoreKit/actions/runs/37922626418). Both ends passed:
3.12.15 / 2.43.0 / 2.0.39 and 3.13.16 / 2.55.1 / 2.0.46, each `Ran 444 tests … OK`, with `black`
leaving 64 files unchanged on `low`. CI installed exactly the pins and `datastorekit-0.1.0`.
**Hazard 2's answer:** Ubuntu 24.04's Python links SQLite 3.45.1 at both ends, older than this
machine's 3.53.4 but past 3.35, so `ALTER TABLE … DROP COLUMN` is available, and the five tests
that use it pass. **Hazard 3's:** the suite passes on Linux. The high end printed 194
`ResourceWarning` lines, the issue's. The annotated tag `v0.1.0` (object `0ece4aa`) was then made
on `68db557` and pushed; `git ls-remote` peels it to `68db557`. The rest of `main` is pushed after
this record.

**Orchestrator review of prompt 06 (2026-10-09).** Dispatched from `0e524b4` to one Opus
subagent, with the note's five corrections and three additions. Reviewed against its commit
`240028e`, with nothing landed after it. **Every check of the note's §3 passed**, and acceptance
1–6 are met. No stop condition fired. Nothing was pushed, and `v0.1.0` is the only tag.

*At dispatch.* The note's gate held at `0e524b4`. The tree was clean, and the only worktree was
this checkout. The suite gave `Ran 444 tests … OK` in `venv/`, and both checks exited 0 (31, 20
and 10; twenty modules, one test declared not ported). CPBH's `HEAD` was `52142d7`, `origin/main`
was `fe040b2`, and no Ray process was up. While writing the note the orchestrator applied the
change to a scratch copy and, at the high end in a venv made offline from 05's cache:
- found that only hazard 4's three tests move (45 failures), and that the 444 pass once the
  witness and `REGISTER_KEYS` are updated;
- captured the new witness twice (74,450 bytes, one key on 21 records, no `ephemeral_probe`
  record: correction 3);
- probed tests 1, 3, 4, 5, 8 and 9, and found that an actor with no broker cannot insert
  (correction 2);
- probed (a), (c), (h) and (i) over the 444 (correction 5).

*The checks.*
1. **Scope.** `240028e` touches exactly the prompt's §7 list, 19 files. The ignored entries are
   dispatch's, with `datastorekit.egg-info/` again, written by `venv/`'s reinstall at `0.2.0`
   (log §5.8). No wheel, `dist/`, `build/` or scratch file.
2. **E1, the layer, by reading.** `contract.py` gains `VERSION_SERIAL_KEY` and
   `require_version_serial`, and imports nothing new. `schema.py` gains `_declared_key_on_version`,
   refusing through `_refuse_declaration`, on every record with a table only. `Datastore.py` holds
   `_lookup_serial` beside `_version_serial`. `set_version` sets both, and `set_lookup_version` sets
   only the lookup serial, with the same type check and change refusal. `_keyed_payloads` copies,
   refuses a caller's key and an unset serial, and is reached only for a record that declares the
   key. `_insert`'s guard and the four unkeyed methods are unchanged. `ShardedPool.py` calls
   `set_lookup_version` on every read-only actor after `read_only_state`, waits for every call, and
   gains the two comments; `object_get_vectorized` is unchanged. No new comment or string names a
   client. The refusal reads `registration_data["version"]`, not the table's columns, as CPBH's
   does (the agent's IMPLEMENTATION CHOICE, logged).
3. **E2, the witness.** Captured again from `git archive 240028e` in two fresh interpreters at the
   high end: byte-identical to the committed file, 74,450 bytes, SHA-256 `643128…bcddb8`. Against
   04a's: 21 additions of `key_on_version`, `true` on `Tessera` only, and nothing else. 04a's
   witness, `client_vocabulary.json` and `standin_pool.py` are unchanged from `68db557`.
4. **E3, the 444.** Of the existing test files, only `REGISTER_KEYS`, `WITNESS` with its docstring
   sentence, `Tessera`'s roles row, and `Tessera_factory`'s `register()` and select change, with
   one import line added to `factories.py` (logged, STRUCTURALLY REQUIRED). `compare_ported_tests.py`
   exits 0 with 04b's counts.
5. **E3, the 14, by reading.** Each row of the prompt's §2.7 table is there under its class and
   name. Pools are opened in the labelled form, and actors are `sp.DatastoreClass` with a stand-in
   broker. Everything is in `tempfile` directories, with stdout redirected. The docstring names no
   client.
6. **E4, both ends.** In `venv/`: `pip show` says `0.2.0`; `Ran 458 tests … OK`; the loader gives
   14 for the new module; `black --check datastorekit docs` leaves 65 files unchanged; the layer
   guard passes. In the orchestrator's own offline venvs, with `git archive 240028e` installed
   editable: 3.13.16 / 2.55.1 / 2.0.46 and 3.12.15 / 2.43.0 / 2.0.39, SQLite 3.53.4 at both, each
   `Ran 458 tests … OK`.
7. **E5, the release.** A wheel built offline from `git archive 240028e`: 98,194 bytes, 25 entries,
   none under `tests/`; `Version: 0.2.0` and 05's two `Requires-Dist` lines; `RECORD` SHA-256
   `c12e23bb…ec82355`, the log's, with `Generator: setuptools (84.0.0)`. Installed offline at the
   high pins and run from outside the repository with `PYTHONPATH` unset:
   - `VERSION_SERIAL_KEY` and `require_version_serial` import from `site-packages`;
   - `datastorekit.tests` does not import;
   - `sharded_store --help` exits 0;
   - `shard_key_audit`'s usage line names `site-packages`.
8. **E6, the documents.**
   - `client-contract.md` gains the header line and §8 only, and every line reference in §8 holds
     at `240028e`.
   - `PROVENANCE.md` gains "After `v0.1.0`", naming the changed files, CPBH `52142d7` and its
     lines, and U27.
   - `compare_with_source.py` gains its one paragraph. `pyproject.toml` changes in its version
     only.
   - The README's four changes are there, and its new anchor and links resolve.
9. **E7, the breakages.** The ten diffs, extracted from the log, apply both ways in their own
   exports of `240028e`, and each fails exactly the tests the log names:
   - (a) `Ran 435`, failures 2, errors 12;
   - (b) errors 5, the fifth being `test_a_vectorized_get_that_reaches_an_inserter`;
   - (c) `Ran 435`, errors 13;
   - (d)–(g) and (j) one each;
   - (h) errors 4;
   - (i) failures 4, test 10 among them.

   Each export was reverted.
10. **E8, the records.** The log has every section of README §5.1 and §5.6's additions, the five
    corrections and three additions, `compare_with_source.py`'s last output and both ignored
    listings. The index has 8 rows and says 8.
11. **Nothing left behind.** No Ray process; `git tag -l` is `v0.1.0`; `origin` has `main` at
    `fe040b2` and `v0.1.0` only.

*Findings beyond the prompt*, recorded and not acted on:
- (b) and (i) each fail one test more than the prompt expected, and both are pinned. Under (i) the
  read-write pool under B also finds A's row, so test 4, which compares the read-only results with
  the read-write ones, passes, and test 1 catches it.
- The agent corrected the prompt's impact statement for §2.8's issue by reproduction: a second
  key on the same field overwrites the first.
- Log §7 item 1: `set_version` after `set_lookup_version` moves the lookup serial, a sequence no
  pool makes.

*Issues.* `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]` is open (§3). Nothing
else is opened. The index is 8.

*Residue fixed in this follow-up:*
- "this commit" → `240028e` in the log, the board and `prompts/INDEX.md`;
- README's header, and its §2 status for 06;
- this paragraph and the notes line.

*`v0.2.0` (note §5, U28).* With the user's approval of each step, `240028e` was pushed alone as
`main` (a fast-forward from `fe040b2`, carrying `1f9941f` and `0e524b4`), and the workflow ran on
it, [run 37934881027](https://github.com/ds283/DatastoreKit/actions/runs/37934881027). Both ends passed: 3.12.15 / 2.43.0 / 2.0.39 and 3.13.16 /
2.55.1 / 2.0.46, SQLite 3.45.1 at both, each `Ran 458 tests … OK`, with `black` leaving 65 files
unchanged on `low`. CI installed exactly the pins and `datastorekit-0.2.0`. The high end printed
184 `ResourceWarning` lines, `[05-a-refused-open-leaves-its-engines-undisposed]`'s. The annotated
tag `v0.2.0` (object `9eaf542`) was then made on `240028e` and pushed; `git ls-remote` peels it to
`240028e`. The rest of `main` is pushed after this record.

**Orchestrator review of prompt 07a (2026-10-09).** Dispatched from `a816632` to one Opus
subagent, with the note's eight corrections and three additions. The run was cut off once by an
API usage limit, with nothing committed and the clients unchanged; the same agent was resumed with
its context, re-read what it had written, and finished. Reviewed against its commit `dd45243`, with
nothing landed after it. **Every check of the note's §3 passed**, and acceptance 1–4 are met. No
stop condition fired. Nothing was pushed, and the tags are `v0.1.0` and `v0.2.0` only.

*At dispatch.* The note's gate held at `a816632`. The tree was clean, and the only worktree was
this checkout. The suite gave `Ran 458 tests … OK` in `venv/`, the port check exited 0, and
`black --check docs` left 3 files unchanged. The clients were at SGK `b510bc9` (clean), CPBH
`52142d7` (23 untracked entries) and SI `7bb3efd` (clean). `origin/main` was `102f225`, and no Ray
process was up. While writing the note, the orchestrator measured each client's layer imports with
an `ast` probe of its own (SGK 233, CPBH 41, SI 48; CPBH 40 at `9b3db51`), and had three read-only
fact-checks, one per client, test the prompt's citations, which gave the note's corrections.

*The checks.*
1. **Scope.** `dd45243` touches exactly the prompt's §7 list, 8 files: the four `docs/adoption/`
   files, `measure_client_imports.py`, the log, the board and `prompts/INDEX.md`. Nothing under
   `datastorekit/`, and `docs/OPEN_ISSUES.md` is untouched. The ignored entries are dispatch's.
   Each client's `HEAD` and `git status --short` are as at dispatch.
2. **The suite.** `Ran 458 tests … OK` in `venv/`; the port check exits 0 with 04b's counts;
   `black --check datastorekit docs` leaves 66 files unchanged.
3. **E2, the script.** It imports only the standard library and reaches a client only through
   `git rev-parse`, `show` and `ls-tree`. Run from `git archive dd45243`, twice per client, its
   Markdown and JSON are byte-identical. Totals 233, 41 and 48, and 40 at CPBH `9b3db51`. An
   unknown commit exits 2. **Its 322 import hits equal the orchestrator's probe file by file and
   line by line, nested flags included.**
4. **E3, the citations.** The review's own check extracted 121 citations from SGK's checklist,
   178 from CPBH's, 201 from SI's and 11 from the README (appendices excluded). All resolve at their
   commits: SI's factory table cites short names under `Datastore/SQL/ObjectFactories/`, CPBH's two
   run scripts are untracked and were read as text, and the README's `requirements.txt` lines are
   per client. Twelve per checklist were read by eye against the cited lines, and hold.
5. **E3, the checklists.** Each has §2.6's head and the ten items, in order and named alike, and
   its appendix is the script's Markdown output at its commit, byte for byte, with its command.
   Advice is marked **Advice:**, and choices are named as the client's. Corrections 1 and 5–7 are
   reflected: CPBH 20 classes over 24 entries and SI 16 over 18, with both routes and what each
   needs; SGK's tracked `.gitignore`, 18 staying modules and `HELPER_MODULE`; CPBH's two
   `VERSION_LABEL`s; SI's five `.timestamp` readers, its read-write plot opens and its closeout at
   `:69-72`.
6. **E4, the README.** The `v0.2.0` pin; the version table, SI's interpreter given as 3.13.16 with
   its `pyvenv.cfg`'s 3.13.13 explained; the module map against `PROVENANCE.md`, and each client's
   `Datastore/SQL/__init__.py` rebinding the actor as the package's does; U32 with its second
   route's precondition; the drop refusals at `ShardedPool.py:716-728` and `:730-749`. Every
   relative link in the four files resolves.
7. **E5, the breakages.** The three diffs, extracted from the log, apply both ways to fresh copies
   of the committed script. (a) gives 192, 41 and 47; (b) 212, 28 and 36; (c) gives 41 against 40
   at CPBH `9b3db51`, and equal counts on SGK and SI at `HEAD~1`, as correction 2 says.
8. **E6, the records.** The log has every section of README §5.1 and §5.4's additions: both
   clients' commit and status listings, the cross-check tables, the citations, (a)–(c), the
   differences from the planner's numbers and from the note's, and the untracked files read. The
   board's row, header and G2–G4 rows point at their checklists. The index has 8 rows and says 8.
9. **Nothing left behind.** No Ray process; no client changed; `origin` unchanged.

*Findings beyond the prompt*, recorded and not acted on:
- Two of the note's numbers were wrong, and the agent's are right. Of CPBH's 20 U32 classes,
  **three** define `read_table` (`redshift` and the two quantity factories), not two. Under (b),
  SGK falls by 21, not 22, because `from Datastore import contract` still names the layer module
  `Datastore.contract` (a difference of definition).
- `docs/client-contract.md` §8 cites the read-only pool's `set_lookup_version` calls as
  `SQL/ShardedPool.py:567-574`; at `v0.2.0` they are `:568-575`. One line wide; left for 07b's
  author, whose verification document cites the contract (log §7 item 2).
- CPBH's and SI's own `SQLAFactoryBase` is not an ABC (`base.py:16-30`): its hooks raise
  `NotImplementedError`. This is why their 20 and 16 classes instantiate today (log §2).
- SI's `plot_InstantonSolutions.py:697-702` passes one payload list to two vectorized gets, a
  concrete case of `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]` (log §7
  item 4).

*Issues.* None opened, closed or narrowed. The index is 8.

*Residue fixed in this follow-up:*
- "this commit" → `dd45243` in the log, the board and `prompts/INDEX.md`;
- README's header, and its §2 status for 07a;
- **U32's count**, in README §6.2 and the board's U32 row, with the user's approval: CPBH 20
  classes over 24 entries, SI 16 over 18 (README §6.2 had "16" for both), and the precondition of
  registering the class;
- this paragraph and the notes line.

## 2. Gates outside this repository (README §7)

| Gate | Status |
|---|---|
| **G1**: SGK `datastore-generic-followup` closed; the import commit fixed | ✅ 2026-10-07: closed at `6f7f291` (03 landed as `086c81a`); the import commit is `6f7f291` |
| **G2**: SGK adopted `v0.2.0` (U29), fingerprint reproduced | ⬜ *(2026-10-09: the adoption checklist is [`docs/adoption/secondarygwkit.md`](../../docs/adoption/secondarygwkit.md), measured at SGK `b510bc9` by 07a.)* *(2026-10-09: `v0.1.0` is made, annotated, on 05's commit `68db557` (tag object `0ece4aa`) and pushed, after CI passed there at both ends, [run 37922626418](https://github.com/ds283/DatastoreKit/actions/runs/37922626418): Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39 and 3.13.16 / 2.55.1 / 2.0.46, SQLite 3.45.1 at both, each `Ran 444 tests … OK`. SGK may now adopt it.)* |
| **G3**: CPBH adopted `v0.2.0` | ⬜ *(2026-10-09: the adoption checklist is [`docs/adoption/champbh.md`](../../docs/adoption/champbh.md), measured at CPBH `52142d7` by 07a.)* *(2026-10-09: `v0.2.0` is made, annotated, on 06's commit `240028e` (tag object `9eaf542`) and pushed, after CI passed there at both ends, [run 37934881027](https://github.com/ds283/DatastoreKit/actions/runs/37934881027): Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39 and 3.13.16 / 2.55.1 / 2.0.46, SQLite 3.45.1 at both, each `Ran 458 tests … OK`. CPBH may now adopt it.)* |
| **G4**: SI adopted | ⬜ *(2026-10-09: the adoption checklist is [`docs/adoption/stochasticinstantons.md`](../../docs/adoption/stochasticinstantons.md), measured at SI `7bb3efd` by 07a; its stores are rebuilt, U31.)* |

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
  - **Measured by 04a (2026-10-08):** **146 lines in 35 files.** 03b's figure, 124 in 28, was first
    reproduced at `ae94aaa` by log 03a §8's method (which also gives 114 in 23 at `72cf34a`). The
    five ported modules and the two fixtures add 22 lines, all SGK's prose ported unchanged under
    03a §2.1:
    - `tests/schema_description.py` 9 (`:3`, `:6`, `:9`, `:12`, `:15`, `:16`, `:20`, `:183`,
      `:184`);
    - `tests/test_store_reader.py` 3 (`:2`, `:12`, `:182`);
    - `tests/test_store_schema.py` 3 (`:2`, `:3`, `:411`);
    - `tests/test_foreign_key_check.py` 2 (`:2`, `:4`);
    - `tests/test_schema_builder.py` 2 (`:2`, `:9`);
    - `tests/test_store_inventory.py` 2 (`:2`, `:702`);
    - `tests/real_store_fixtures.py` 1 (`:29`).

    The client's files add none. `test_schema_builder`'s SGK witness history, which named SGK's
    tables, was rewritten under U21. Their SGK references outside the pattern ("store-fingerprint
    prompt 01/02", "S1/S2/S4", `var/`, SGK's witness file names) are listed in log 04a §7 item 4.
  - **Measured by 04b (2026-10-08):** **155 lines in 40 files.** 04a's figure, 146 in 35, was first
    reproduced at `7ceed25` by log 03a §8's method (which also gives 102 in 19 at `8bc60a5`, 114 in
    23 at `72cf34a` and 124 in 28 at `ae94aaa`). The five ported modules add 9 lines:
    - `tests/test_layer_registry.py` 3 (`:2`, `:75`, `:176`);
    - `tests/test_drop_refuses_dangling_references.py` 2 (`:2`, `:10`);
    - `tests/test_layer_is_generic.py` 2 (`:71`, "repository root", SGK's docstring, true here;
      `:200`, `tools/` in `KNOWN_HITS`' entry, the package's own path);
    - `tests/test_inventory_declarations.py` 1 (`:2`);
    - `tests/test_declared_facts.py` 1 (`:2`).

    `test_layer_registry.py:75` is the new comment of `COMMAND_LINE_ORDER`, which names the
    source's `main.py`; the rest is SGK's prose ported unchanged. `test_parent_set_members.py`
    adds none. The guard pins the one comment U17 freezes (`tools/shard_key_audit.py:188`). Their
    SGK references outside the pattern, and `test_inventory_declarations`' docstring that still
    mentions the report U16 left in SGK, are in log 04b §7 and §8.
- **[02-an-unsupplied-sharded-table-raises-keyerror]** *(opened 2026-10-07 by prompt 02)*
  - **The defect.** Reopening a store whose primary records a sharded table that the constructor's
    `sharded_tables` lacks raises a bare `KeyError('<table>')` from `_read_shard_data`
    (`datastorekit/SQL/ShardedPool.py:1015`, `attr = self._sharded_tables[row.table]`), before the
    list it prints and the `RuntimeError` meant for that case (`:1022-1045`) are reached. Probed with
    `shard_store_fixtures` (log 02 §5 item 1).
  - **Impact.** The open is still refused; the refusal does not say why. Inherited from SGK
    unchanged.
  - **Next step.** Fix once rule 8 lifts (after 05), with a test that opens such a store. Unassigned.
- **[05-a-refused-open-leaves-its-engines-undisposed]** *(opened 2026-10-09 by prompt 05)*
  - **The defect.** When an open is refused or abandoned, the engines the pool and its actors made
    are never disposed, and each one's pooled SQLite connection is closed only when the garbage
    collector reaches it. Python 3.13 reports each as a `ResourceWarning` ("unclosed database");
    3.12 reports nothing, but the behaviour is the same. Inherited from SGK unchanged.
  - **Measured** (2026-10-09, by prompt 05, log 05 §4). A scratch wrapper of `sqlite3.connect` and
    `sqlite3.dbapi2.connect` with a `factory=` subclass that records its creation stack and counts,
    on `__del__`, the connections never closed. Over the 444, at both ends (Python 3.12.15 / Ray
    2.43.0 / SQLAlchemy 2.0.39, and 3.13.16 / 2.55.1 / 2.0.46), identically: **105 of 40,874**
    connections are never closed, all opened by the layer's engines, none by the tests' own code:
    - `datastorekit/SQL/ShardedPool.py:858` (`with self._engine.connect() as conn:`, the primary's
      schema check): 58, in tests of `test_reconcile_at_open` 23, `test_prune_at_open` 13,
      `test_store_schema` 9, `test_version_row_at_open` 8, `test_read_only_pool` 4,
      `test_declared_facts` 1;
    - `datastorekit/SQL/Datastore.py:349` (`self._inspector = sqla.inspect(self._engine)`, an
      actor's constructor): 41, in `test_version_row_at_open`;
    - `datastorekit/SQL/ShardedPool.py:870` (`self._shard_file_table.create(self._engine)`): 6, in
      `test_version_row_at_open`.

    Each is in a test whose open is refused or abandoned. A test run by inheritance is counted under
    the module that defines it.
  - **Impact.** A long-lived process that retries refused opens holds one file descriptor, and one
    SQLite connection, per refused engine until the collector runs. No data is affected. Under
    Python 3.13 the suite prints about 170–200 `ResourceWarning` lines (172, 188 and 194 in three
    runs), whose count varies with the collector.
  - **Next step.** Dispose the engines on a refused or abandoned open, once rule 8 lifts (after
    05), with a test that counts unclosed connections across a refused open. Unassigned.

- **[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]** *(opened 2026-10-09 by
  prompt 06)*
  - **The defect.** `ShardedPool.object_get_vectorized` adds the shard key to each of the caller's
    payload dicts in place, `for value in payload_data: value.update(shard_key)`
    (`datastorekit/SQL/ShardedPool.py:3309-3310` at `240028e`; `:3298-3299` at `v0.1.0`). It was
    so before 06, and is inherited from SGK unchanged. It does not affect keying: the actor copies
    each payload before it adds the version serial (`SQL/Datastore.py:598-625`).
  - **Reproduction** (log 06 §4.2; the stand-in pool, `build.open_pool`, two aliases on two
    keypoints). A list `[{"weight": 0.25}, {"weight": 0.75}]` passed to
    `object_get_vectorized("Tessera", {"k": a1}, payload_data=…)` holds `"k": a1` in both dicts
    afterwards. Passed a second time with the same key it returns the same serials. Passed with
    `{"k": a2}` its dicts are overwritten to `a2`; passed then to `pool.object_get("Tessera",
    payload_data=…)`, which routes each dict by its own key, they go to `a2`'s shard.
  - **Impact.** A caller's dicts change under it. A caller that reuses them sees the key in them; a
    later call that routes by each dict's own key (`object_get(..., payload_data=…)`) routes them
    by whichever key was added last; and a caller that passes them to a get whose shard-key field
    differs carries the first key's field into that payload as well (read from the code: every
    sharded class of the neutral client is sharded on `k`, so this was not reproduced).
  - **Next step.** Copy, as the actor's keyed lookup does: `payload_data = [{**value,
    **shard_key} for value in payload_data]`, with a test that passes a list twice. Unassigned.

## 4. Resolved issues

- **[04a-no-test-pins-a-second-parent-set-member]** *(opened 2026-10-08 by the orchestrator's
  review of 04a)*
  - **The defect.** No test fails when `Weave`'s parent set loses its second member. Deleting
    `"origin": Parent("origin_serial", "Trace", nullable=True)` from `Weave_factory.inventory_spec`
    (`datastorekit/tests/client/factories.py:1684`) leaves `Ran 353 tests … OK` (replayed by the
    review). `IDENTITY` holds one entry per key field, and `strands` varies strand 701's `anchor`
    member (log 04a §2 item 13). `Sample`'s parent set has one member. So nothing in the suite
    reads a member after the first.
  - **Impact.** The inventory's handling of a parent set with more than one member is unpinned:
    the order of a member tuple, a `None` in a later member, a later member naming another class.
    A layer change there, or a client declaration that drops a member, would pass the suite.
  - **Next step.** 04b ports `test_inventory_declarations` and `test_declared_facts`, which test
    declarations and resolution. Its author checks whether any of them fails under this deletion.
    If none does, 04b varies strand 702's `origin` in a test of its own, and makes the deletion one
    of its breakages. Unassigned until 04b is written.
  - **Assigned (2026-10-08):** to prompt 04b. None of its five SGK modules varies a second member:
    `test_the_full_store_resolves_no_absent_parent_as_unresolved` walks the member field `anchor`
    only. So 04b adds `datastorekit/tests/test_parent_set_members.py`, whose two tests the
    deletion must fail (04b §2.6).
  - **Closed (2026-10-08) by prompt 04b** (`0c66505`, log 04b §4). The new module
    `datastorekit/tests/test_parent_set_members.py` requires that `Weave`'s
    `parent_sets["strands"]` is `[("anchor", "Tessera"), ("origin", "Trace")]` in that order, and
    that setting `Weave_members` row 702's `origin_serial` from 3 to 1 (`vary_row`, on
    `build_full_store`) changes `Weave`'s records and no other class's, with no problem. Deleting
    the `origin` member from `Weave_factory.inventory_spec` (`client/factories.py:1684`, breakage
    (l)) fails both tests, and nothing else (`Ran 444 tests` / `FAILED (failures=2)`).

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
