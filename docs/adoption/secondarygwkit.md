# Adoption checklist: SecondaryGWKit (SGK)

- **Client:** SecondaryGWKit, `/Users/ds283/Documents/Code/SecondaryGWKit`, at **`b510bc9`**
  (`b510bc90b66985532d28996ab4e5b13b0ff71709`, branch `handover-remedial`, "Freeze the datastore
  layer while it moves to DatastoreKit").
- **Package:** `datastorekit` at **`v0.2.0`** (`240028e`).
- **How it was measured:** read-only, by DatastoreKit's extraction prompt 07a on 2026-10-09,
  through `git show`, `git grep`, `git ls-tree` and `git log` only, and by
  `docs/extraction/measure_client_imports.py` (the appendix). Nothing of SGK was imported, run or
  opened, and no store was opened. **SGK's adoption campaign measures again before acting, and its
  numbers govern.**
- **This is data, not instructions.** It describes SGK at `b510bc9`. SGK's campaign decides what to
  do, under SGK's `CLAUDE.md`. A recommendation is marked **Advice:**; a choice that is SGK's is
  named as SGK's.

*Added by extraction prompt 10 on 2026-10-10: the section
[Addendum: v0.2.1](#addendum-v021-extraction-prompt-10-2026-10-10), after item 10, gives the pin
**`v0.2.1`** and what changed for SGK since `v0.2.0`, and supersedes the statements it names.
07a's text is unchanged and true of `v0.2.0`.*

Unless another commit is named, a `path:line` is SGK's at `b510bc9`, and one under
`datastorekit/` is the package's at `v0.2.0`.

**In one paragraph.** SGK's layer *is* the package's source. Its 17 layer files are byte-identical
from the import commit `6f7f291` to `b510bc9` (`git diff --stat 6f7f291 b510bc9` over them is
empty). With the module map applied to the module paths of their imports, measured by a probe
in 07a's scratchpad:
- 15 of them equal `v0.1.0`'s files byte for byte, and the two tools equal them up to
  `PROVENANCE.md`'s D-tool (how a tool is run) as well;
- against `v0.2.0`, 11 are byte-identical, the two tools differ by D-tool, and `contract.py`,
  `SQL/schema.py`, `SQL/ShardedPool.py` and `SQL/Datastore.py` differ by prompt 06's additions
  only (`v0.1.0` and `v0.2.0` differ in exactly those four). SGK registers factory *classes*, declares no `key_on_version`, and
already passes `factories=`, `drop_tables=` and `serial_batch_sizes=`. So the adoption is mostly
mechanical: delete, rewrite imports, and sort out the tests and fixtures that stay.

---

## 1. The client and its versions

- `b510bc9` on `handover-remedial`; `git status --short` is empty at the start and at the end of
  07a's measurement. Six `.sqlite` files at the root (`physics-test-n20-lambdacdm-zend0p1*.sqlite`)
  are **ignored** (`!!`), not untracked; they were named only.
- **Python 3.12.15** (`venv/pyvenv.cfg`, read as text: `version = 3.12.15`; `venv/bin/python3.12`
  links to MacPorts' 3.12 framework); **`ray==2.43.0`** (`requirements.txt:74`);
  **`SQLAlchemy==2.0.39`** (`requirements.txt:85`). These are exactly the package's tested low end.
- **Ignores.** A tracked root `.gitignore` holds `var/` only (`.gitignore:3`; made at SGK
  `2c48e43`, last changed at `0d7c05c`); two more are tracked under `docs/` (`docs/derivation/.gitignore`,
  `docs/handover/sources/.gitignore`). `*.sqlite` and the rest are ignored through
  `.git/info/exclude`, which is not tracked.
- **There is no CI**: no `.github/` directory is tracked.
- SGK's test command is `CLAUDE.md:106-111` (in "Repository mechanics", `CLAUDE.md:104-114`).

## 2. What it deletes

**The 17 files of `PROVENANCE.md`'s file map:**
- `Datastore/__init__.py`, `Datastore/object.py`, `Datastore/contract.py`,
  `Datastore/replication.py`, `Datastore/shard_paths.py`, `Datastore/store_reader.py`,
  `Datastore/store_inventory.py`;
- `Datastore/SQL/__init__.py`, `Datastore/SQL/schema.py`, `Datastore/SQL/ShardedPool.py`,
  `Datastore/SQL/Datastore.py`, `Datastore/SQL/ClientPool.py`, `Datastore/SQL/SerialPoolBroker.py`,
  `Datastore/SQL/ProfileAgent.py`;
- `Datastore/SQL/ObjectFactories/base.py`;
- `tools/sharded_store.py`, `tools/shard_key_audit.py`.

Two of them are non-empty `__init__.py` files:
- `Datastore/__init__.py:1` re-exports `DatastoreObject` (`from .object import DatastoreObject`);
- `Datastore/SQL/__init__.py:1` rebinds `Datastore.SQL.Datastore` to the actor class (`from
  .Datastore import Datastore`).

With both gone, `Datastore/` and `Datastore/SQL/` hold no `__init__.py`, and become namespace
packages holding the factories (`Datastore/SQL/ObjectFactories/`, whose own `__init__.py` stays)
and the tests (`Datastore/tests/`, likewise). Whether the factories then move is SGK's choice
(item 4).

**`tools/__init__.py` stays** (empty, 0 bytes): `tools/inventory_report.py` stays in SGK, and
`main.py:93` imports it (`from tools.inventory_report import format_inventory_report`).

## 3. Which imports it rewrites

The script counts **233** import statements of the 17 modules, in **138** files, outside the
layer's own files (appendix). **41** of them are nested (not direct children of a module's body).
By group:

| Group | Statements | Nested | What they are |
|---|---|---|---|
| `Datastore/SQL/ObjectFactories/` | 43 | 23 | 20 files: `SQLAFactoryBase` ×21, `InventorySpec`/`Parent`/`ParentSet` ×20 (inside each `inventory_spec`), `ReplicationMismatch`/`differing_columns` ×2 (`Datastore/SQL/ObjectFactories/BackgroundModel.py:579`, `Datastore/SQL/ObjectFactories/wavenumber.py:329`, under `if`) |
| `Datastore/tests/` | 68 | 4 | 37 files; item 7 says which stay |
| `RunRegistry/` | 14 | 6 | `stores.py`: `ShardedPool` ×3 (`RunRegistry/stores.py:1084`, `:1121`, `:1814`), `canonical_json` ×2 (`RunRegistry/stores.py:1197`, `RunRegistry/stores.py:1383`) and `read_inventory` ×1 inside `fingerprint_store` (`RunRegistry/stores.py:1493`), which is **G2's fingerprint**; its tests, 8 more |
| `(top level)` | 16 | 0 | `main.py:58`, `main.py:59`, `main.py:92`; the six `extract_*.py` scripts and `extract_common.py:44` |
| `ComputeTargets/` | 11 | 0 | `DatastoreObject` ×10; `ComputeTargets/tests/test_qcd_cosmology_inventory_record.py:33` (`read_inventory`) |
| `CosmologyConcepts/`, `CosmologyModels/`, `MetadataConcepts/`, `Quadrature/` | 2, 1, 5, 1 | 0 | `DatastoreObject` ×9 |
| `RayTools/` | 1 | 0 | `RayTools/RayWorkPool.py:8`, `ShardedPool`, a type hint |
| `config/` | 1 | 0 | `config/model_list.py:4`, `ShardedPool` |
| `tools/` | 2 | 1 | `tools/inventory_report.py:82` and `:162` (`build_schema`, in `_schema_tables`) |
| `docs/` | 17 | 4 | 13 files; see below |
| `prompts/` | 51 | 3 | 31 files of historical measurement scripts (appendix) |
| **total** | **233** | **41** | |

`DatastoreObject` is imported from the package root (`from Datastore import DatastoreObject`) 19
times, in `ComputeTargets/` (10), `CosmologyConcepts/` (2), `CosmologyModels/` (1),
`MetadataConcepts/` (5) and `Quadrature/` (1); and from `Datastore.object` twice more
(`Datastore/tests/test_declared_facts.py:50` among them). Each becomes `from datastorekit import
DatastoreObject`.

**`docs/`, live and historical.** Of the 17 statements:
- **Reached by SGK's own code or by G2:**
  - `docs/handover/quadsource_atol_sweep.py:693` (`resolve_shard_path`, inside
    `assert_store_is_self_consistent`). It is the **G2 rehearsal's launcher**
    (`docs/a3-v2-readiness-verification.md:64`), and four RunRegistry test modules load it by path
    (`RunRegistry/tests/test_build_rehearsal_scope.py:42`,
    `RunRegistry/tests/test_prune_on_resume.py:41`,
    `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:39`,
    `RunRegistry/tests/test_killed_handler.py:29`).
  - `docs/source-remediation-verification/analyse_greens_and_source.py:35` and
    `docs/source-remediation-verification/run_quadsource_integrals.py:41` (`ShardedPool`), named by
    `ComputeTargets/tests/test_main_plumbing.py:965-966` and
    `ComputeTargets/tests/test_gksource_parent_set_main.py:70`, `:74`.
- **Already failing at `b510bc9`:** ten statements in six files import `_factories` from
  `Datastore.SQL.Datastore`, which left that module at SGK `19f07ee` ("Give the datastore layer its
  registries instead of importing them"): `docs/datastore-integrity-audit/fk_sweep_probe.py:8`,
  `docs/datastore-integrity-audit/lookup_keys/common.py:18`,
  `docs/datastore-integrity-audit/lookup_keys/probe_03_column_existence.py:25`,
  `docs/datastore-integrity-audit/tq_fk_probe.py:8`, `docs/tolerance-convergence/inventory.py:196`,
  `docs/tolerance-convergence/order_audit.py:1253`, and the `build_schema` imports beside four of
  them. Six more probes fail transitively, through `from common import …` of `lookup_keys/common.py`
  (`docs/datastore-integrity-audit/lookup_keys/probe_01_tagged_read_batch.py:27`,
  `docs/datastore-integrity-audit/lookup_keys/probe_01b_fix_shape.py:24`,
  `docs/datastore-integrity-audit/lookup_keys/probe_04_exit_time_and_solver.py:18`,
  `docs/datastore-integrity-audit/lookup_keys/probe_04b_exact_match_fix_shape.py:27`,
  `docs/datastore-integrity-audit/lookup_keys/probe_05_value_lookups_and_read_batch.py:15`,
  `docs/datastore-integrity-audit/lookup_keys/probe_06_oneloop_tags_and_redshift_zero.py:18`); they import no layer module
  themselves, so the script does not count them.
- **The other four:** `docs/a3-v2-readiness/readonly_open_probe.py:53`,
  `docs/a3-v2-readiness/rehearsal/store_soundness.py:19`,
  `docs/datastore-integrity-audit/replicated_divergence_probe.py:16`,
  `docs/datastore-integrity-audit/replicated_write_fault_probe.py:159` (with three
  `importlib.import_module` calls at `:37-39`).

Which `docs/` scripts SGK keeps runnable is SGK's choice.

**`prompts/`: 51 statements in 31 files**, all under `prompts/`, historical measurement scripts of
SGK's campaigns. They are listed in the appendix. **Advice:** leave them as the record of the tree
they measured; nothing here asks SGK to rewrite them.

**Strings and `importlib`.** 13 string literals and 11 `import_module` calls name a layer module
(appendix): 21 name one exactly, 3 are `mock.patch` targets inside one
(`Datastore/tests/test_delete_store.py:339`, `Datastore/tests/test_layer_registry.py:432`,
`Datastore/tests/test_read_only_pool.py:882`). Every one of the three patch targets is in a module
item 7 deletes. The `import_module` calls of staying code are item 7's.

## 4. What leaves the layer, and where it may go

**Nothing of SGK's is inside the 17 files.** SGK's `datastore-generic` campaign moved it out
(`19f07ee`):
- the registry, `config/datastore.py`: `factories` (`config/datastore.py:91`, 38 classes, each
  registered as a class), `drop_groups` (`config/datastore.py:133`), `serial_batch_sizes`
  (`config/datastore.py:152`) and `tables_to_drop` (`config/datastore.py:194`);
- the sharding facts, `config/sharding.py`: `replicated_tables` (`config/sharding.py:3`),
  `sharded_tables` (`config/sharding.py:19`), `read_table_config` (`config/sharding.py:37`),
  `shard_key_type` (`config/sharding.py:45`) and its getter (`config/sharding.py:50`).

**Where the factories go is SGK's choice.** They are under `Datastore/SQL/ObjectFactories/` (21
modules besides `base.py` and `__init__.py`). The options, and what each touches:
- **Keep them where they are, under namespace packages.** Every `Datastore.SQL.ObjectFactories.<m>`
  import stays as it is. `Datastore` and `Datastore.SQL` become namespace packages (item 2).
- **Keep them where they are, with empty `__init__.py` files** in place of the two deleted ones.
  The same imports stand, and the packages stay regular.
- **Move them.** Every import of a factory module changes, and so does every path that reaches a
  factory by file:
  - `Datastore/tests/test_factory_select_columns.py:96` (`FACTORY_DIR`), which
    `Datastore/tests/test_value_reads_parent_key.py:59` imports and globs at
    `Datastore/tests/test_value_reads_parent_key.py:790`;
  - `ComputeTargets/tests/test_cosmology_representation_key.py:56`, `:448`;
  - `ComputeTargets/tests/test_run_identity.py:90`;
  - `docs/datastore-integrity-audit/lookup_keys/probe_01b_fix_shape.py:27` and
    `docs/datastore-integrity-audit/lookup_keys/probe_03_column_existence.py:28` (both already
    failing, item 3).

The script counts **98** import statements of factory modules outside
`Datastore/SQL/ObjectFactories/` (and 100 with the two inside it): `config/` 20,
`Datastore/tests/` 46, `ComputeTargets/` 17, `docs/` 15 (appendix). This is the count the planner
gave as 75.

## 5. What its factories must change

- **Nothing but the import** of `SQLAFactoryBase`, and of `InventorySpec`, `Parent`, `ParentSet`,
  `ReplicationMismatch` and `differing_columns` (item 3). `Datastore/SQL/ObjectFactories/base.py`
  equals `datastorekit/SQL/factory_base.py` byte for byte.
- **No SGK factory declares `key_on_version`** (`git grep key_on_version b510bc9` finds nothing),
  so `v0.2.0`'s one feature reaches none of SGK's classes.
- SGK registers **classes**, not instances (`config/datastore.py:91-131`, no call among the 38
  values), so the abstractness of `SQLAFactoryBase` is never enforced on them (U32 does not reach
  SGK).

## 6. Its call sites and pool construction

- **The pool is constructed seven times** in SGK's scripts: `main.py:4164` and the six
  `extract_*.py` (`extract_GkSource_data.py:932`, `extract_GkWKB_data.py:505`,
  `extract_Gk_data.py:453`, `extract_QuadSourceIntegral_data.py:1294`, `extract_TkWKB_data.py:493`,
  `extract_tensor_source_data.py:421`). `main.py` already passes `drop_tables=`, `factories=` and
  `serial_batch_sizes=` (`main.py:4176`, `main.py:4178`, `main.py:4179`); the constructor's
  signature is the package's (`datastorekit/SQL/ShardedPool.py:95-114`).
- **No call changes behaviour.** The one difference a read-only open makes: after every actor's
  `read_only_state`, a read-only pool calls `set_lookup_version` on each actor and waits
  (`datastorekit/SQL/ShardedPool.py:568-575`). It sets an in-memory serial only and writes nothing.
  The six `extract_*.py` open read-only (`read_only=True`, for example
  `extract_GkSource_data.py:942`).
- `object_get_vectorized`'s in-place update of the caller's payloads
  (`datastorekit/SQL/ShardedPool.py:3309-3310`; DatastoreKit's
  `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]`) is SGK's own behaviour,
  unchanged.

## 7. Its tests and fixtures

`Datastore/tests/` holds 44 test modules and 7 other entries (`__init__.py`, `data/`,
`inventory_report_parsing.py`, `real_store_fixtures.py`, `schema_description.py`,
`shard_store_fixtures.py`, `standin_pool.py`).

**Delete: the tests the package now carries.**
- The **8 modules moved verbatim**, 88 `def test_` lines (`PROVENANCE.md`): `test_shard_paths`,
  `test_shard_file_name`, `test_shardedpool_shard_paths`, `test_copy_move_store`,
  `test_delete_store`, `test_sharded_store_script`, `test_shard_key_audit_copy`,
  `test_shard_key_audit_refusals`.
- The **18 test modules ported**, 304 `def test_` lines (`docs/extraction/compare_ported_tests.py`'s
  `PORTED`): `test_replicated_write`, `test_reconcile_at_open`, `test_prune_at_open`,
  `test_version_row_at_open`, `test_read_only_pool`, `test_one_timestamp_per_write`,
  `test_absolute_shard_record_refused`, `test_closed_store_refusals`, `test_store_inventory`,
  `test_store_schema`, `test_store_reader`, `test_foreign_key_check`, `test_schema_builder`,
  `test_inventory_declarations`, `test_declared_facts`, `test_layer_registry`,
  `test_drop_refuses_dangling_references`, and `test_layer_is_generic`. The last imports the layer
  at module level, and its `layer_files()` (`Datastore/tests/test_layer_is_generic.py:60`) would
  find only `RayTools/` once the layer is gone; the package's own guard replaces it.
- **Keep one test of those modules:**
  `test_inventory_declarations.TestResolve.test_the_report_renders_both_cosmology_types`, the one
  test `compare_ported_tests.py`'s `NOT_PORTED` declares (U16). It asserts on SGK's
  `tools.inventory_report`, so it moves to a module of SGK's own when `test_inventory_declarations`
  is deleted.

**Keep, and rewrite their imports:**
- the **18 staying modules**, 320 `def test_` lines: `test_backgroundmodelvalue_roundtrip` (6),
  `test_database_errors_reach_the_caller` (21), `test_exact_identity_lookups` (18),
  `test_factory_select_columns` (9), `test_gksource_parent_set` (38), `test_integral_read_batch`
  (10), `test_inventory_consumers` (11), `test_inventory_report` (18),
  `test_inventory_report_labels` (19), `test_inventory_retired` (7),
  `test_quadsource_integral_parent_key` (24), `test_quadsource_parent_key` (34),
  `test_quadsource_policy_foreign_key` (4), `test_quadsource_policy_key` (19),
  `test_read_path_mechanics` (20), `test_value_reads_parent_key` (18),
  `test_wkb_numeric_parent_key` (39), `test_wkb_parent_foreign_key` (5);
- **SGK's copies of the fixtures**, which the wheel does not ship (`docs/adoption/README.md` §3):
  - `real_store_fixtures.py`: imported by nine staying modules of `Datastore/tests/`
    (`test_gksource_parent_set`, `test_inventory_consumers`, `test_inventory_report`,
    `test_inventory_report_labels`, the four `test_quadsource_*` and `test_wkb_parent_foreign_key`), by `ComputeTargets/tests/test_qcd_cosmology_inventory_record.py`, and by
    `RunRegistry/tests/test_store_fingerprint.py` and `RunRegistry/tests/test_store_retire.py`;
  - `shard_store_fixtures.py`: imported by `real_store_fixtures.py` and by six RunRegistry test
    files (`RunRegistry/tests/store_fixtures.py`, `test_quadsource_atol_sweep_prepare.py`,
    `test_store_amend.py`, `test_store_copy_move.py`, `test_store_retire.py`,
    `test_store_sidecar.py`);
  - `standin_pool.py`: of staying code, imported by
    `ComputeTargets/tests/test_quadsource_policy_main.py` (and by three `docs/a3-v2-readiness/`
    probes);
  - `schema_description.py`: its only importer is `test_schema_builder`, which is deleted above.
    Whether SGK keeps it is SGK's choice.

**The `importlib` and `__ray_metadata__` sites in what stays**, each naming a layer module by a
string that the import rewrite must reach:
- `Datastore/tests/standin_pool.py:43-48`: `importlib.import_module("Datastore.SQL.ShardedPool")`,
  `"Datastore.SQL.Datastore"` and `"Datastore.SQL.SerialPoolBroker"`, then
  `__ray_metadata__.modified_class` of the actor and the broker;
- `Datastore/tests/test_wkb_numeric_parent_key.py:88` (`import_module("Datastore.SQL.Datastore")`,
  for the module that `Datastore/SQL/__init__.py` shadows) and
  `Datastore/tests/test_wkb_numeric_parent_key.py:909-911` (`__ray_metadata__.modified_class`, then
  the actor's `_drop_tables`, which the package keeps, `datastorekit/SQL/Datastore.py:439`);
- `Datastore/tests/schema_description.py:185-187` (the same pattern), if it is kept.

The package keeps the shadowing (`datastorekit/SQL/__init__.py:1`), so the module is still reached
by `importlib.import_module("datastorekit.SQL.Datastore")`.

**`Datastore/tests/test_inventory_retired.py` reads two files that are deleted.**
- `Datastore/tests/test_inventory_retired.py:75` parses the source file `Datastore/SQL/Datastore.py`
  (the actor's methods are read from its source).
- `HELPER_MODULE = "Datastore/tests/test_store_inventory.py"` (`Datastore/tests/test_inventory_retired.py:52`),
  a ported module, is used at `Datastore/tests/test_inventory_retired.py:108`, `:115` and `:134`.

Both fail once the files are gone. How to change the test is SGK's choice.

**Path-dependent tests.** `Datastore/tests/test_value_reads_parent_key.py:808` reaches test
modules by path (`root / (test_module.replace(".", "/") + ".py")`); a move of `Datastore/tests/`
reaches it. Item 4 lists the paths that reach factories by file.

## 8. Which of its stores the package refuses, and why

**None is refused.** The reasoning, from the measurements above:
- SGK's 17 files are byte-identical from `6f7f291` to `b510bc9` (the paragraph at the head).
- `v0.1.0` equals SGK's layer at `6f7f291` up to `PROVENANCE.md`'s allowed differences
  (`compare_with_source.py`, run for the last time by prompt 06), none of which changes what is
  written.
- `v0.2.0` adds `key_on_version` behind a `register()` key no SGK factory declares (item 5). The
  key lives in the in-memory schema record (`datastorekit/SQL/schema.py:186-190`); nothing the
  layer writes changes (`docs/client-contract.md` §8; decision U29).

So every SGK store the package's code opened before (it is the same code) opens as before. G2's
rehearsal (item 9) is the measurement of this.

## 9. Its acceptance (G2)

G2 holds when SGK has adopted `v0.2.0` in a campaign of its own (decision U29):
1. its 17 layer files are deleted, and it imports `datastorekit` at the pinned tag;
2. **its remaining suites pass**;
3. **a rehearsal rebuild through the package reproduces the reference fingerprint**, run by a
   person under SGK's run-registry rules (`CLAUDE.md:75-102`).

**The reference** (`docs/a3-v2-readiness-verification.md:25-27`): format 6, digest
`39809dcac5c7b231c6b4468f9ea6cc48a4ad9c3a52d469f18f43291f781b55d2`, all 21 classes equal. It was
reproduced by `datastore-generic`'s rehearsal rebuild, E7, at SGK `53d4e18`
(`prompts/datastore-generic/IMPLEMENTATION_STATE.md:1410`, "the fingerprint matches").

**The rehearsal command**, `docs/a3-v2-readiness-verification.md`'s §1.1
(`docs/a3-v2-readiness-verification.md:58`), run from the repository root, detached, verbatim:

```bash
nohup sh -c 'PYTHONPATH=. ./venv/bin/python -u docs/handover/quadsource_atol_sweep.py \
    --build --rehearsal [--resume] \
    --database var/datastores/a3-v2-readiness-07-<store>.sqlite \
    --job-name a3-v2-readiness-07 --atol 1e-32 --rtol 1e-7 --cpus 6 \
    --register <slug> --purpose "<one line>" --campaign a3-v2-readiness --prompt 07; \
  echo "** driver exit status $?"' \
  > var/runs/a3-v2-readiness-07-<slug>.launch.log 2>&1 &
disown
```

(`docs/a3-v2-readiness-verification.md:64-71`). The store, slug, purpose and campaign are SGK's to
choose for the adoption's run.

**The fingerprint** is taken through `python -m RunRegistry store fingerprint`
(`RunRegistry/__main__.py:6`), which calls `fingerprint_store` and so `read_inventory`
(`RunRegistry/stores.py:1493`), one of the rewritten imports.

## 10. What goes stale in it

- **`CLAUDE.md:47-73`**, "The datastore layer is frozen — it is moving to DatastoreKit". The freeze
  ends when SGK's adoption lands (`CLAUDE.md:72-73`); the section names the 17 files
  (`CLAUDE.md:57-62`).
- **`CLAUDE.md:106-111`**, the test command (in "Repository mechanics", `CLAUDE.md:104-114`). It
  runs `ComputeTargets/tests`; what `Datastore/tests/` holds after item 7, and where it lives, is
  SGK's choice.
- **Prose naming the two tools by their SGK paths**, beyond `CLAUDE.md:62`:
  `RunRegistry/stores.py:5` (`tools/sharded_store.py`); `docs/OPEN_ISSUES.md:685`;
  `docs/backport-modules-verification.md:217`; `docs/datastore-generic-audit.md:180`;
  `docs/store-retirement-audit.md:118`. After adoption the tools run as `python -m
  datastorekit.tools.sharded_store` and `python -m datastorekit.tools.shard_key_audit`.
- **Run provenance.** `git_provenance()` (`RunRegistry/__init__.py:97-111`) records SGK's `git rev-parse
  HEAD` and whether the tree was dirty, and nothing of the installed `datastorekit`. A run's
  `datastorekit` version is therefore implied only by `requirements.txt` at that HEAD, and only if
  the venv was installed from it. Whether to record it is SGK's choice.
- **The inherited issues.** Four open issues of the layer are on SGK's boards and indexed in
  DatastoreKit's `docs/OPEN_ISSUES.md` §1.2 (`[00-a-drop-action-drops-a-replicated-table-outside-the-in-flight-record]`,
  `[00-a-new-stores-first-open-can-leave-a-primary-without-its-shards]`,
  `[00-the-inventory-cannot-see-a-serial-split]`, `[01-cross-filesystem-move-advice-says-delete-by-hand]`).
  After adoption the code they describe is DatastoreKit's.

---

## Addendum: v0.2.1 (extraction prompt 10, 2026-10-10)

*Written by extraction prompt 10 on 2026-10-10, and added to 07a's text, which stays as written
and true of `v0.2.0` (`CLAUDE.md` rule 6). SGK was not re-measured (decision U37); what this
section says of SGK comes from 07a's measurements, log 08a §3 and the `KeyError` measure below.*

**The pin.** SGK adopts **`v0.2.1`** in place of `v0.2.0` (decision U37, which amends U29), and G2
reads "SGK has adopted `v0.2.1`":

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.1
```

**What changed for SGK since `v0.2.0`.** The three changes are
[`docs/client-contract.md` §9](../client-contract.md#9-changes-after-v020)'s rows, and
[`README.md`'s addendum](README.md#addendum-v021-extraction-prompt-10-2026-10-10) gives them for
every client.
- **The files.** At `v0.2.1`, SGK's 17 layer files and the package differ, beyond what the
  paragraph at the head lists against `v0.2.0`, also by:
  - 08a's and 08b's code in `SQL/ShardedPool.py`;
  - 09's prose, its comments and docstrings, in 11 of the 17: `contract.py`, `replication.py`,
    `shard_paths.py`, `store_reader.py`, `store_inventory.py`, `SQL/schema.py`,
    `SQL/ShardedPool.py`, `SQL/Datastore.py`, `SQL/ObjectFactories/base.py` (the package's
    `SQL/factory_base.py`) and both tools.

  So only the six that 09 did not touch, `__init__.py`, `object.py`, `SQL/__init__.py`,
  `SQL/ClientPool.py`, `SQL/SerialPoolBroker.py` and `SQL/ProfileAgent.py`, can equal SGK's
  sources byte for byte (with the module map applied, as at the head). Each was among the 11
  byte-identical against `v0.2.0`, and none has changed since. The count of 11 is `v0.2.0`'s.
- **The factory base.** `datastorekit/SQL/factory_base.py` now differs from SGK's
  `Datastore/SQL/ObjectFactories/base.py` in its comments and docstrings; with its docstrings
  blanked it parses to the same code. SGK's factories still change nothing but their imports.
- **The vectorized get.** `object_get_vectorized` sends each shard copies of the caller's payloads
  (`datastorekit/SQL/ShardedPool.py:3348`), and no longer adds the shard key to the caller's dicts.
  SGK's 17 calls in `main.py` each pass a work list built just before, and no line reads a payload
  list back (log 08a §3).
- **The `KeyError`.** A reopen whose primary records a sharded table that `sharded_tables` lacks is
  refused with the intended `RuntimeError`, not a bare `KeyError`
  (`datastorekit/SQL/ShardedPool.py:1071-1072`, `:1100-1103`), and SGK's code does not depend on
  the `KeyError`: measured through `git grep` at `b510bc9`, SGK catches `KeyError` only at
  `RunRegistry/__init__.py:606` and `RunRegistry/tests/test_run_registry.py:489`, neither around a
  pool, and the only `try` around a `ShardedPool(` outside its layer is in two archived
  measurement scripts, `prompts/datastore-generic/orchestrator/measure-07/scripts/m7_messages.py:184`
  (which catches `ReadOnlyMiss` only) and
  `prompts/datastore-generic/orchestrator/measure-09/scripts/m4c_open_rw.py:38` (which catches any
  exception and records its type).
- **The refused open.** An open that raises closes the actors it built and disposes the pool's
  engine (`datastorekit/SQL/ShardedPool.py:203-207`, `:375-408`): a client that retries refused
  opens no longer holds a file descriptor per refused engine until the collector runs.
- **Item 8 still holds: no SGK store is refused.** The fixes change nothing the layer writes
  (contract [§9.1](../client-contract.md#91-prompt-08a),
  [§9.2](../client-contract.md#92-prompt-08b)), and 09 changes no code, so every SGK store opens as
  under `v0.2.0`. G2's rehearsal (item 9) is the measurement.
- **SGK's frozen copies carry the three defects**, and adopting `v0.2.1` fixes them. "The freeze"
  of `PROVENANCE.md` (decision U3) says a defect found during the freeze is fixed in DatastoreKit
  after G2; decision U33 fixed these three before it.

**Line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, read at that tag
(`240028e`). A `datastorekit/` line in this addendum is `v0.2.1`'s, whose `datastorekit/` is the
tree of extraction prompt 09's commit `cad7bc1`.

**What this addendum supersedes**, in this file. Each `path:line` is this file's as committed with
this addendum. In 07a's file (`dd45243`) every line after `:14` is five lines earlier, since the
italic line under the title adds five.

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/secondarygwkit.md:6` | the package at **`v0.2.0`** | at `v0.2.1`, with this addendum |
| `docs/adoption/secondarygwkit.md:21-22` | a `datastorekit/` line is the package's at `v0.2.0` | still so for 07a's text; a `datastorekit/` line in this addendum is at `v0.2.1` |
| `docs/adoption/secondarygwkit.md:30-32` | against `v0.2.0`, 11 files byte-identical, the tools by D-tool, four by prompt 06's additions | `v0.2.0`'s count. At `v0.2.1` only the six can be byte-identical; "The files", above |
| `docs/adoption/secondarygwkit.md:187-188` | `base.py` equals `datastorekit/SQL/factory_base.py` byte for byte | they differ in comments and docstrings (09); "The factory base", above |
| `docs/adoption/secondarygwkit.md:203-207` | "No call changes behaviour", and the one difference a read-only open makes | three more differences, none of which changes what SGK's calls use: "The vectorized get", "The `KeyError`" and "The refused open", above |
| `docs/adoption/secondarygwkit.md:208-211` | the in-place update of the caller's payloads "is SGK's own behaviour, unchanged" | `v0.2.1` sends copies, and SGK reads nothing back; "The vectorized get", above |
| `docs/adoption/secondarygwkit.md:297-302` | item 8's reasoning, through `v0.2.0` | extended to `v0.2.1`; "Item 8 still holds", above |
| `docs/adoption/secondarygwkit.md:306` | G2 holds when SGK has adopted `v0.2.0` | G2 holds when SGK has adopted `v0.2.1` (U37) |

---

## Appendix: the script's output

Made by, from DatastoreKit's repository root:

```bash
./venv/bin/python docs/extraction/measure_client_imports.py sgk
```

# Imports of the layer: SecondaryGWKit (SGK) at `b510bc9`

Written by `docs/extraction/measure_client_imports.py`, reading through `git ls-tree` and `git show` only.

- **Repository:** `/Users/ds283/Documents/Code/SecondaryGWKit`
- **Commit:** `b510bc90b66985532d28996ab4e5b13b0ff71709` (given as `b510bc9`), 2026-10-07 Freeze the datastore layer while it moves to DatastoreKit
- **Layer files** (17): `Datastore/__init__.py`, `Datastore/object.py`, `Datastore/contract.py`, `Datastore/replication.py`, `Datastore/shard_paths.py`, `Datastore/store_reader.py`, `Datastore/store_inventory.py`, `Datastore/SQL/__init__.py`, `Datastore/SQL/schema.py`, `Datastore/SQL/ShardedPool.py`, `Datastore/SQL/Datastore.py`, `Datastore/SQL/ClientPool.py`, `Datastore/SQL/SerialPoolBroker.py`, `Datastore/SQL/ProfileAgent.py`, `Datastore/SQL/ObjectFactories/base.py`, `tools/sharded_store.py`, `tools/shard_key_audit.py`
- **Layer files absent at this commit:** none
- **Factory package:** `Datastore/SQL/ObjectFactories/` (its `base.py` is the layer's)
- **Files read:** 445 tracked `.py` files outside the layer; 0 do not parse

## Totals

| What | Count |
|---|---|
| Import statements naming a layer module | **233** in 138 files |
| of which nested (not at module level) | 41 |
| String literals naming a layer module | 13 (10 exactly its name) |
| `import_module` / `__import__` calls naming a layer module | 11 |
| Import statements naming a factory module (not layer imports) | 100 (98 outside `Datastore/SQL/ObjectFactories/`) |

## Layer imports, by group

| Group | Statements | Nested | Files |
|---|---|---|---|
| `(top level)` | 16 | 0 | 8 |
| `ComputeTargets/` | 11 | 0 | 11 |
| `CosmologyConcepts/` | 2 | 0 | 2 |
| `CosmologyModels/` | 1 | 0 | 1 |
| `Datastore/SQL/ObjectFactories/` | 43 | 23 | 20 |
| `Datastore/tests/` | 68 | 4 | 37 |
| `MetadataConcepts/` | 5 | 0 | 5 |
| `Quadrature/` | 1 | 0 | 1 |
| `RayTools/` | 1 | 0 | 1 |
| `RunRegistry/` | 14 | 6 | 6 |
| `config/` | 1 | 0 | 1 |
| `docs/` | 17 | 4 | 13 |
| `prompts/` | 51 | 3 | 31 |
| `tools/` | 2 | 1 | 1 |
| **total** | **233** | **41** | **138** |

## Layer imports, by module

A statement naming two layer modules is counted under each.

| Module | Statements | Names imported by `from` (statements) |
|---|---|---|
| `Datastore` | 22 | `DatastoreObject` 19, `contract` 1 |
| `Datastore.SQL` | 1 | `ShardedPool as _unused` 1 |
| `Datastore.SQL.ClientPool` | 1 | `SerialPoolManager` 1 |
| `Datastore.SQL.Datastore` | 12 | `_drop_actions` 2, `_factories` 10 |
| `Datastore.SQL.ObjectFactories.base` | 21 | `SQLAFactoryBase` 21 |
| `Datastore.SQL.ProfileAgent` | 7 | `ProfileAgent` 7 |
| `Datastore.SQL.ShardedPool` | 28 | `ShardedPool` 26, `ShardedPool as _unused` 1 |
| `Datastore.SQL.schema` | 35 | `SchemaDifferences` 1, `StoreSchemaMismatch` 6, `build_schema` 31, `dependent_tables` 1, `drop_order` 2, `schema_differences` 4 |
| `Datastore.contract` | 3 | `TAG_LABEL` 1, `TAG_SERIAL` 1, `TAG_TABLE` 2, `VERSION_LABEL` 1, `VERSION_TABLE` 1, `contract` 1 |
| `Datastore.object` | 2 | `DatastoreObject` 2 |
| `Datastore.replication` | 10 | `ReadOnlyMiss` 1, `ReadOnlyWrite` 2, `ReplicatedDivergence` 4, `ReplicationInFlight` 1, `ReplicationMismatch` 6, `differing_columns` 2 |
| `Datastore.shard_paths` | 15 | `resolve_shard_path` 3, `shard_file_name` 13, `shard_file_problem` 1 |
| `Datastore.store_inventory` | 68 | `ClassInventory` 2, `InventorySpec` 23, `Parent` 15, `ParentSet` 3, `Record` 3, `ShardContext` 4, `StoreInventory` 3, `_merge_digests` 1, `canonical` 1, `canonical_json` 3, `digest` 1, `inventory_classes` 3, `inventory_specs` 5, `read_inventory` 29, `read_records` 4, `reference_digest` 2 |
| `Datastore.store_reader` | 10 | `open_read_only` 9, `read_only_url` 2 |

## Every layer import

### `(top level)` (16)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `extract_GkSource_data.py:34` | — | `Datastore.SQL.ProfileAgent` | `ProfileAgent` |
| `extract_GkSource_data.py:35` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `extract_GkWKB_data.py:32` | — | `Datastore.SQL.ProfileAgent` | `ProfileAgent` |
| `extract_GkWKB_data.py:33` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `extract_Gk_data.py:29` | — | `Datastore.SQL.ProfileAgent` | `ProfileAgent` |
| `extract_Gk_data.py:30` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `extract_QuadSourceIntegral_data.py:40` | — | `Datastore.SQL.ProfileAgent` | `ProfileAgent` |
| `extract_QuadSourceIntegral_data.py:41` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `extract_TkWKB_data.py:28` | — | `Datastore.SQL.ProfileAgent` | `ProfileAgent` |
| `extract_TkWKB_data.py:29` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `extract_common.py:44` | — | `Datastore.store_inventory` | `read_inventory` |
| `extract_tensor_source_data.py:28` | — | `Datastore.SQL.ProfileAgent` | `ProfileAgent` |
| `extract_tensor_source_data.py:29` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `main.py:58` | — | `Datastore.SQL.ProfileAgent` | `ProfileAgent` |
| `main.py:59` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `main.py:92` | — | `Datastore.store_inventory` | `read_inventory` |

### `ComputeTargets/` (11)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `ComputeTargets/BackgroundModel.py:24` | — | `Datastore` | `DatastoreObject` |
| `ComputeTargets/GkNumericIntegration.py:14` | — | `Datastore` | `DatastoreObject` |
| `ComputeTargets/GkSource.py:13` | — | `Datastore` | `DatastoreObject` |
| `ComputeTargets/GkSourcePolicyData.py:12` | — | `Datastore` | `DatastoreObject` |
| `ComputeTargets/GkWKBIntegration.py:13` | — | `Datastore` | `DatastoreObject` |
| `ComputeTargets/OneLoopIntegral.py:7` | — | `Datastore` | `DatastoreObject` |
| `ComputeTargets/QuadSource.py:16` | — | `Datastore` | `DatastoreObject` |
| `ComputeTargets/QuadSourceIntegral.py:17` | — | `Datastore` | `DatastoreObject` |
| `ComputeTargets/TkNumericIntegration.py:14` | — | `Datastore` | `DatastoreObject` |
| `ComputeTargets/TkWKBIntegration.py:10` | — | `Datastore` | `DatastoreObject` |
| `ComputeTargets/tests/test_qcd_cosmology_inventory_record.py:33` | — | `Datastore.store_inventory` | `read_inventory` |

### `CosmologyConcepts/` (2)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `CosmologyConcepts/redshift.py:6` | — | `Datastore` | `DatastoreObject` |
| `CosmologyConcepts/wavenumber.py:11` | — | `Datastore` | `DatastoreObject` |

### `CosmologyModels/` (1)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `CosmologyModels/base.py:3` | — | `Datastore` | `DatastoreObject` |

### `Datastore/SQL/ObjectFactories/` (43)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `Datastore/SQL/ObjectFactories/BackgroundModel.py:90` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/BackgroundModel.py:579` | if | `Datastore.replication` | `ReplicationMismatch`, `differing_columns` |
| `Datastore/SQL/ObjectFactories/BackgroundModel.py:888` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec`, `Parent` |
| `Datastore/SQL/ObjectFactories/GkNumericIntegration.py:14` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/GkNumericIntegration.py:639` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec`, `Parent` |
| `Datastore/SQL/ObjectFactories/GkSource.py:48` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/GkSource.py:847` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec`, `Parent`, `ParentSet` |
| `Datastore/SQL/ObjectFactories/GkSourcePolicy.py:3` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/GkSourcePolicy.py:72` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec` |
| `Datastore/SQL/ObjectFactories/GkSourcePolicyData.py:9` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/GkSourcePolicyData.py:181` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec`, `Parent` |
| `Datastore/SQL/ObjectFactories/GkWKBIntegration.py:64` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/GkWKBIntegration.py:968` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec`, `Parent` |
| `Datastore/SQL/ObjectFactories/LambdaCDM.py:4` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/LambdaCDM.py:96` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec` |
| `Datastore/SQL/ObjectFactories/OneLoopIntegral.py:11` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/OneLoopIntegral.py:346` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec`, `Parent` |
| `Datastore/SQL/ObjectFactories/QCD_Cosmology.py:21` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/QCD_Cosmology.py:132` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec` |
| `Datastore/SQL/ObjectFactories/QuadSource.py:14` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/QuadSource.py:550` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec`, `Parent` |
| `Datastore/SQL/ObjectFactories/QuadSourceIntegral.py:17` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/QuadSourceIntegral.py:973` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec`, `Parent` |
| `Datastore/SQL/ObjectFactories/QuadSourcePolicy.py:3` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/QuadSourcePolicy.py:109` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec` |
| `Datastore/SQL/ObjectFactories/TkNumericIntegration.py:16` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/TkNumericIntegration.py:641` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec`, `Parent` |
| `Datastore/SQL/ObjectFactories/TkWKBIntegration.py:60` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/TkWKBIntegration.py:966` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec`, `Parent` |
| `Datastore/SQL/ObjectFactories/integration_metadata.py:3` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/integration_metadata.py:61` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec` |
| `Datastore/SQL/ObjectFactories/redshift.py:8` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/redshift.py:137` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec` |
| `Datastore/SQL/ObjectFactories/store_tag.py:3` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/store_tag.py:51` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec` |
| `Datastore/SQL/ObjectFactories/tolerance.py:5` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/tolerance.py:59` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec` |
| `Datastore/SQL/ObjectFactories/version.py:3` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/version.py:50` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec` |
| `Datastore/SQL/ObjectFactories/wavenumber.py:11` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/SQL/ObjectFactories/wavenumber.py:130` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec` |
| `Datastore/SQL/ObjectFactories/wavenumber.py:329` | if | `Datastore.replication` | `ReplicationMismatch`, `differing_columns` |
| `Datastore/SQL/ObjectFactories/wavenumber.py:390` | def inventory_spec | `Datastore.store_inventory` | `InventorySpec`, `Parent` |

### `Datastore/tests/` (68)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `Datastore/tests/real_store_fixtures.py:52` | — | `Datastore.SQL.schema` | `build_schema` |
| `Datastore/tests/real_store_fixtures.py:53` | — | `Datastore.shard_paths` | `shard_file_name` |
| `Datastore/tests/shard_store_fixtures.py:22` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `Datastore/tests/shard_store_fixtures.py:23` | — | `Datastore.shard_paths` | `shard_file_name` |
| `Datastore/tests/test_absolute_shard_record_refused.py:35` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `Datastore/tests/test_absolute_shard_record_refused.py:36` | — | `Datastore.shard_paths` | `resolve_shard_path`, `shard_file_name` |
| `Datastore/tests/test_absolute_shard_record_refused.py:37` | — | `Datastore.store_reader` | `open_read_only` |
| `Datastore/tests/test_closed_store_refusals.py:26` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `Datastore/tests/test_closed_store_refusals.py:27` | — | `Datastore.shard_paths` | `shard_file_name` |
| `Datastore/tests/test_closed_store_refusals.py:28` | — | `Datastore.store_reader` | `open_read_only` |
| `Datastore/tests/test_copy_move_store.py:29` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `Datastore/tests/test_copy_move_store.py:30` | — | `Datastore.shard_paths` | `shard_file_name` |
| `Datastore/tests/test_declared_facts.py:43` | — | `Datastore.contract` | `TAG_LABEL`, `TAG_SERIAL`, `TAG_TABLE`, `VERSION_LABEL`, `VERSION_TABLE` |
| `Datastore/tests/test_declared_facts.py:50` | — | `Datastore.object` | `DatastoreObject` |
| `Datastore/tests/test_declared_facts.py:51` | — | `Datastore.replication` | `ReplicationMismatch` |
| `Datastore/tests/test_declared_facts.py:52` | — | `Datastore.SQL.ObjectFactories.base` | `SQLAFactoryBase` |
| `Datastore/tests/test_declared_facts.py:53` | — | `Datastore.SQL.schema` | `build_schema` |
| `Datastore/tests/test_delete_store.py:35` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `Datastore/tests/test_delete_store.py:36` | — | `Datastore.shard_paths` | `shard_file_name` |
| `Datastore/tests/test_drop_refuses_dangling_references.py:35` | — | `Datastore.SQL.schema` | `build_schema`, `dependent_tables` |
| `Datastore/tests/test_drop_refuses_dangling_references.py:36` | — | `Datastore.replication` | `ReadOnlyWrite` |
| `Datastore/tests/test_drop_refuses_dangling_references.py:37` | — | `Datastore.store_inventory` | `inventory_specs` |
| `Datastore/tests/test_exact_identity_lookups.py:62` | — | `Datastore.SQL.schema` | `build_schema` |
| `Datastore/tests/test_factory_select_columns.py:740` | — | `Datastore.SQL.schema` | `build_schema` |
| `Datastore/tests/test_gksource_parent_set.py:58` | — | `Datastore.store_inventory` | `read_inventory` |
| `Datastore/tests/test_integral_read_batch.py:62` | — | `Datastore.SQL.schema` | `build_schema` |
| `Datastore/tests/test_inventory_consumers.py:33` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `Datastore/tests/test_inventory_declarations.py:29` | — | `Datastore.contract` | `TAG_TABLE` |
| `Datastore/tests/test_inventory_declarations.py:30` | — | `Datastore.store_inventory` | `ClassInventory`, `InventorySpec`, `Parent`, `ParentSet`, `Record`, `StoreInventory`, `inventory_classes`, `inventory_specs`, `read_inventory`, `reference_digest` |
| `Datastore/tests/test_inventory_report.py:26` | — | `Datastore.store_inventory` | `read_inventory` |
| `Datastore/tests/test_inventory_report_labels.py:39` | — | `Datastore.store_inventory` | `Record`, `StoreInventory`, `digest`, `read_inventory`, `reference_digest` |
| `Datastore/tests/test_inventory_retired.py:30` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `Datastore/tests/test_layer_is_generic.py:49` | — | `Datastore` | `contract` |
| `Datastore/tests/test_layer_is_generic.py:50` | — | `Datastore.SQL.schema` | `build_schema` |
| `Datastore/tests/test_layer_registry.py:52` | — | `Datastore.SQL.ClientPool` | `SerialPoolManager` |
| `Datastore/tests/test_layer_registry.py:53` | — | `Datastore.SQL.schema` | `build_schema`, `drop_order` |
| `Datastore/tests/test_layer_registry.py:54` | — | `Datastore.replication` | `ReadOnlyWrite` |
| `Datastore/tests/test_layer_registry.py:55` | — | `Datastore.store_inventory` | `read_inventory` |
| `Datastore/tests/test_layer_registry.py:56` | — | `Datastore.store_reader` | `open_read_only` |
| `Datastore/tests/test_prune_at_open.py:44` | — | `Datastore.replication` | `ReplicatedDivergence` |
| `Datastore/tests/test_prune_at_open.py:302` | def test_the_set_of_classes_is_read_from_the_factories | `Datastore.SQL.schema` | `build_schema` |
| `Datastore/tests/test_quadsource_integral_parent_key.py:52` | — | `Datastore.store_inventory` | `read_inventory` |
| `Datastore/tests/test_quadsource_parent_key.py:47` | — | `Datastore.store_inventory` | `Parent`, `ShardContext`, `_merge_digests`, `read_inventory`, `read_records` |
| `Datastore/tests/test_quadsource_policy_key.py:357` | def read_the_store | `Datastore.store_inventory` | `read_inventory` |
| `Datastore/tests/test_read_only_pool.py:52` | — | `Datastore.SQL.schema` | `StoreSchemaMismatch` |
| `Datastore/tests/test_read_path_mechanics.py:56` | — | `Datastore.SQL.schema` | `build_schema` |
| `Datastore/tests/test_reconcile_at_open.py:46` | — | `Datastore.SQL.schema` | `StoreSchemaMismatch` |
| `Datastore/tests/test_reconcile_at_open.py:47` | — | `Datastore.replication` | `ReplicatedDivergence`, `ReplicationMismatch` |
| `Datastore/tests/test_replicated_write.py:37` | — | `Datastore.replication` | `ReplicationInFlight`, `ReplicationMismatch` |
| `Datastore/tests/test_schema_builder.py:50` | — | `Datastore.SQL.schema` | `build_schema` |
| `Datastore/tests/test_shard_file_name.py:20` | — | `Datastore.shard_paths` | `shard_file_name` |
| `Datastore/tests/test_shard_paths.py:24` | — | `Datastore.shard_paths` | `resolve_shard_path`, `shard_file_problem` |
| `Datastore/tests/test_sharded_store_script.py:21` | — | `Datastore.shard_paths` | `shard_file_name` |
| `Datastore/tests/test_store_inventory.py:38` | — | `Datastore.store_inventory as store_inventory` | — |
| `Datastore/tests/test_store_inventory.py:39` | — | `Datastore.store_inventory` | `canonical`, `canonical_json`, `read_inventory` |
| `Datastore/tests/test_store_inventory.py:532` | def store_inventory_tables | `Datastore.SQL.schema` | `build_schema` |
| `Datastore/tests/test_store_reader.py:34` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `Datastore/tests/test_store_reader.py:35` | — | `Datastore.SQL.schema` | `StoreSchemaMismatch` |
| `Datastore/tests/test_store_reader.py:36` | — | `Datastore.store_reader` | `open_read_only` |
| `Datastore/tests/test_store_schema.py:43` | — | `Datastore.SQL.schema` | `SchemaDifferences`, `StoreSchemaMismatch`, `build_schema`, `schema_differences` |
| `Datastore/tests/test_store_schema.py:49` | — | `Datastore.store_inventory` | `read_inventory` |
| `Datastore/tests/test_store_schema.py:50` | — | `Datastore.store_reader` | `open_read_only`, `read_only_url` |
| `Datastore/tests/test_store_schema.py:233` | def test_a_refusal_yields_nothing_and_disposes_every_engine | `Datastore.store_reader as store_reader` | — |
| `Datastore/tests/test_value_reads_parent_key.py:58` | — | `Datastore.SQL.schema` | `build_schema` |
| `Datastore/tests/test_version_row_at_open.py:41` | — | `Datastore.SQL.schema` | `build_schema` |
| `Datastore/tests/test_version_row_at_open.py:42` | — | `Datastore.replication` | `ReplicatedDivergence` |
| `Datastore/tests/test_wkb_numeric_parent_key.py:81` | — | `Datastore.SQL.schema` | `build_schema`, `drop_order` |
| `Datastore/tests/test_wkb_numeric_parent_key.py:82` | — | `Datastore.store_inventory` | `Parent`, `ShardContext`, `read_records` |

### `MetadataConcepts/` (5)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `MetadataConcepts/GkSourcePolicy.py:3` | — | `Datastore` | `DatastoreObject` |
| `MetadataConcepts/QuadSourcePolicy.py:3` | — | `Datastore` | `DatastoreObject` |
| `MetadataConcepts/store_tag.py:1` | — | `Datastore` | `DatastoreObject` |
| `MetadataConcepts/tolerance.py:3` | — | `Datastore` | `DatastoreObject` |
| `MetadataConcepts/version.py:1` | — | `Datastore` | `DatastoreObject` |

### `Quadrature/` (1)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `Quadrature/integration_metadata.py:3` | — | `Datastore` | `DatastoreObject` |

### `RayTools/` (1)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `RayTools/RayWorkPool.py:8` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |

### `RunRegistry/` (14)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `RunRegistry/stores.py:1084` | def copy_store | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `RunRegistry/stores.py:1121` | def move_store | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `RunRegistry/stores.py:1197` | def fingerprint_of | `Datastore.store_inventory` | `canonical_json` |
| `RunRegistry/stores.py:1383` | def listing_lines | `Datastore.store_inventory` | `canonical_json` |
| `RunRegistry/stores.py:1493` | def fingerprint_store | `Datastore.store_inventory` | `read_inventory` |
| `RunRegistry/stores.py:1814` | def retire_store | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `RunRegistry/tests/store_fixtures.py:19` | — | `Datastore.shard_paths` | `shard_file_name` |
| `RunRegistry/tests/test_quadsource_atol_sweep_prepare.py:29` | — | `Datastore.shard_paths` | `shard_file_name` |
| `RunRegistry/tests/test_store_copy_move.py:30` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `RunRegistry/tests/test_store_copy_move.py:31` | — | `Datastore.shard_paths` | `shard_file_name` |
| `RunRegistry/tests/test_store_fingerprint.py:49` | — | `Datastore.store_inventory` | `read_inventory` |
| `RunRegistry/tests/test_store_retire.py:45` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `RunRegistry/tests/test_store_retire.py:46` | — | `Datastore.shard_paths` | `shard_file_name` |
| `RunRegistry/tests/test_store_retire.py:47` | — | `Datastore.store_inventory` | `read_inventory` |

### `config/` (1)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `config/model_list.py:4` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |

### `docs/` (17)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `docs/a3-v2-readiness/readonly_open_probe.py:53` | — | `Datastore.store_reader` | `open_read_only`, `read_only_url` |
| `docs/a3-v2-readiness/rehearsal/store_soundness.py:19` | — | `Datastore.store_inventory` | `read_inventory` |
| `docs/datastore-integrity-audit/fk_sweep_probe.py:8` | — | `Datastore.SQL.Datastore` | `_factories` |
| `docs/datastore-integrity-audit/fk_sweep_probe.py:9` | — | `Datastore.SQL.schema` | `build_schema` |
| `docs/datastore-integrity-audit/lookup_keys/common.py:18` | — | `Datastore.SQL.Datastore` | `_factories` |
| `docs/datastore-integrity-audit/lookup_keys/common.py:19` | — | `Datastore.SQL.schema` | `build_schema` |
| `docs/datastore-integrity-audit/lookup_keys/probe_03_column_existence.py:25` | — | `Datastore.SQL.Datastore` | `_factories` |
| `docs/datastore-integrity-audit/lookup_keys/probe_03_column_existence.py:26` | — | `Datastore.SQL.schema` | `build_schema` |
| `docs/datastore-integrity-audit/replicated_divergence_probe.py:16` | — | `Datastore.store_inventory` | `read_inventory` |
| `docs/datastore-integrity-audit/replicated_write_fault_probe.py:159` | def main | `Datastore.store_inventory` | `read_inventory` |
| `docs/datastore-integrity-audit/tq_fk_probe.py:8` | — | `Datastore.SQL.Datastore` | `_factories` |
| `docs/datastore-integrity-audit/tq_fk_probe.py:9` | — | `Datastore.SQL.schema` | `build_schema` |
| `docs/handover/quadsource_atol_sweep.py:693` | def assert_store_is_self_consistent | `Datastore.shard_paths` | `resolve_shard_path` |
| `docs/source-remediation-verification/analyse_greens_and_source.py:35` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `docs/source-remediation-verification/run_quadsource_integrals.py:41` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `docs/tolerance-convergence/inventory.py:196` | def keyed_object_types | `Datastore.SQL.Datastore` | `_factories` |
| `docs/tolerance-convergence/order_audit.py:1253` | def d3_tables | `Datastore.SQL.Datastore` | `_factories` |

### `prompts/` (51)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `prompts/datastore-generic-followup/measure/scripts/f1_groups.py:3` | — | `Datastore.SQL.schema` | `build_schema` |
| `prompts/datastore-generic-followup/measure/scripts/f1_groups.py:4` | — | `Datastore.store_inventory` | `inventory_specs` |
| `prompts/datastore-generic-followup/measure/scripts/f2_closure.py:6` | — | `Datastore.SQL.schema` | `build_schema` |
| `prompts/datastore-generic-followup/measure/scripts/f2_closure.py:7` | — | `Datastore.store_inventory` | `inventory_specs` |
| `prompts/datastore-generic-followup/measure/scripts/r2_resolve.py:6` | — | `Datastore.store_inventory` | `read_inventory` |
| `prompts/datastore-generic-followup/orchestrator/measure-03/scripts/m3_messages.py:13` | — | `Datastore` | — |
| `prompts/datastore-generic-followup/orchestrator/measure-03/scripts/m3_messages.py:14` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `prompts/datastore-generic-followup/orchestrator/measure-03/scripts/m3_messages.py:15` | — | `Datastore.shard_paths` | `shard_file_name` |
| `prompts/datastore-generic-followup/orchestrator/measure-03/scripts/m3_messages.py:16` | — | `Datastore.store_reader` | `open_read_only` |
| `prompts/datastore-generic/orchestrator/measure-05/scripts/m1_clean_stores.py:8` | — | `Datastore.SQL.Datastore` | `_factories` |
| `prompts/datastore-generic/orchestrator/measure-05/scripts/m1_clean_stores.py:9` | — | `Datastore.SQL.schema` | `build_schema`, `schema_differences` |
| `prompts/datastore-generic/orchestrator/measure-05/scripts/m2_messages.py:11` | — | `Datastore.SQL.Datastore` | `_factories` |
| `prompts/datastore-generic/orchestrator/measure-05/scripts/m2_messages.py:12` | — | `Datastore.SQL.schema` | `build_schema`, `schema_differences`, `StoreSchemaMismatch` |
| `prompts/datastore-generic/orchestrator/measure-05/scripts/m2_messages.py:13` | — | `Datastore.store_reader` | `open_read_only` |
| `prompts/datastore-generic/orchestrator/measure-05/scripts/m4_fingerprint.py:15` | — | `Datastore.store_inventory` | `read_inventory` |
| `prompts/datastore-generic/orchestrator/measure-05/scripts/m5_refixtures.py:9` | — | `Datastore.SQL.Datastore` | `_factories` |
| `prompts/datastore-generic/orchestrator/measure-05/scripts/m5_refixtures.py:10` | — | `Datastore.SQL.schema` | `build_schema` |
| `prompts/datastore-generic/orchestrator/measure-05/scripts/m5_refixtures.py:11` | — | `Datastore.store_inventory` | `read_inventory` |
| `prompts/datastore-generic/orchestrator/measure-05/scripts/m6_u1.py:9` | — | `Datastore.SQL.Datastore` | `_factories` |
| `prompts/datastore-generic/orchestrator/measure-05/scripts/m6_u1.py:10` | — | `Datastore.SQL.schema` | `build_schema`, `schema_differences` |
| `prompts/datastore-generic/orchestrator/measure-05/scripts/run_shims.py:10` | — | `Datastore.SQL.schema` | `StoreSchemaMismatch` |
| `prompts/datastore-generic/orchestrator/measure-05/scripts/run_shims.py:11` | — | `Datastore.store_inventory as inv` | — |
| `prompts/datastore-generic/orchestrator/measure-06/scripts/m11_orphans.py:7` | — | `Datastore.SQL.Datastore` | `_drop_actions` |
| `prompts/datastore-generic/orchestrator/measure-06/scripts/m1_fingerprint.py:14` | — | `Datastore.store_inventory` | `read_inventory` |
| `prompts/datastore-generic/orchestrator/measure-06/scripts/m3_drop_order.py:12` | — | `Datastore.SQL.schema` | `build_schema` |
| `prompts/datastore-generic/orchestrator/measure-06/scripts/m3b_pool_drop.py:16` | — | `Datastore.SQL.ShardedPool as spm` | — |
| `prompts/datastore-generic/orchestrator/measure-06/scripts/m3b_pool_drop.py:24` | if | `Datastore.SQL.Datastore` | `_drop_actions` |
| `prompts/datastore-generic/orchestrator/measure-06/scripts/m8_messages.py:15` | — | `Datastore.store_reader` | `open_read_only` |
| `prompts/datastore-generic/orchestrator/measure-06/scripts/m8_messages.py:16` | — | `Datastore.store_inventory` | `read_inventory` |
| `prompts/datastore-generic/orchestrator/measure-07/scripts/m1_fingerprint.py:14` | — | `Datastore.store_inventory` | `read_inventory` |
| `prompts/datastore-generic/orchestrator/measure-07/scripts/m2_open_behaviour.py:27` | — | `Datastore.SQL` | `ShardedPool as _unused` |
| `prompts/datastore-generic/orchestrator/measure-07/scripts/m3_units.py:15` | — | `Datastore.SQL.schema` | `build_schema` |
| `prompts/datastore-generic/orchestrator/measure-07/scripts/m3_units.py:16` | — | `Datastore.SQL.ShardedPool` | `ShardedPool` |
| `prompts/datastore-generic/orchestrator/measure-07/scripts/m7_messages.py:23` | — | `Datastore.replication` | `ReadOnlyMiss`, `ReplicatedDivergence`, `ReplicationMismatch` |
| `prompts/datastore-generic/orchestrator/measure-07/scripts/m7_messages.py:263` | def test_orphan_tag | `Datastore.store_inventory` | `read_inventory` |
| `prompts/datastore-generic/orchestrator/measure-07/scripts/m8_build_schema_keys.py:8` | — | `Datastore.SQL.schema` | `build_schema` |
| `prompts/datastore-generic/orchestrator/measure-07/scripts/m9_revalidate.py:19` | — | `Datastore.object` | `DatastoreObject` |
| `prompts/datastore-generic/orchestrator/measure-07/scripts/m9_revalidate.py:20` | — | `Datastore.SQL.schema` | `build_schema` |
| `prompts/datastore-generic/orchestrator/measure-08/scripts/m1_fingerprint.py:19` | — | `Datastore.store_inventory as si` | — |
| `prompts/datastore-generic/orchestrator/measure-08/scripts/m1_fingerprint.py:20` | — | `Datastore.store_inventory` | `read_inventory` |
| `prompts/datastore-generic/orchestrator/measure-08/scripts/m3_resolve.py:13` | — | `Datastore.store_inventory` | `read_inventory` |
| `prompts/datastore-generic/orchestrator/measure-08/scripts/m4_order.py:18` | — | `Datastore.store_inventory` | `inventory_classes`, `inventory_specs` |
| `prompts/datastore-generic/orchestrator/measure-08/scripts/m4b_order_matters.py:15` | — | `Datastore.store_inventory as si` | — |
| `prompts/datastore-generic/orchestrator/measure-08/scripts/m5_imports.py:37` | — | `Datastore.store_inventory as si` | — |
| `prompts/datastore-generic/orchestrator/measure-08/scripts/m5b_read_records_alone.py:11` | — | `Datastore.store_inventory` | `ShardContext`, `read_records` |
| `prompts/datastore-generic/orchestrator/measure-08/scripts/m7_messages.py:12` | — | `Datastore.store_inventory as si` | — |
| `prompts/datastore-generic/orchestrator/measure-08/scripts/m7_messages.py:13` | — | `Datastore.store_inventory` | `Parent`, `ParentSet`, `ShardContext`, `read_records` |
| `prompts/datastore-generic/orchestrator/measure-08/scripts/m7_messages.py:48` | if | `Datastore.store_inventory` | `InventorySpec`, `inventory_classes` |
| `prompts/datastore-generic/orchestrator/measure-08/scripts/m7b_reduced_registry.py:10` | — | `Datastore.store_inventory` | `read_inventory` |
| `prompts/datastore-generic/orchestrator/measure-09/scripts/m4_build.py:8` | — | `Datastore` | — |
| `prompts/datastore-generic/orchestrator/measure-09/scripts/m4_inventory.py:11` | — | `Datastore.store_inventory as si` | — |

### `tools/` (2)

| File:line | Nested | Module | Names |
|---|---|---|---|
| `tools/inventory_report.py:82` | — | `Datastore.store_inventory` | `ClassInventory`, `Record`, `StoreInventory` |
| `tools/inventory_report.py:162` | def _schema_tables | `Datastore.SQL.schema` | `build_schema` |

## String literals naming a layer module

| File:line | Literal | Exact |
|---|---|---|
| `Datastore/tests/test_delete_store.py:339` | `Datastore.SQL.ShardedPool.resolve_shard_path` | no |
| `Datastore/tests/test_layer_is_generic.py:356` | `Datastore.SQL.ObjectFactories.base` | yes |
| `Datastore/tests/test_layer_registry.py:432` | `Datastore.SQL.ClientPool.ClientPool` | no |
| `Datastore/tests/test_layer_registry.py:592` | `Datastore.SQL.ShardedPool` | yes |
| `Datastore/tests/test_layer_registry.py:593` | `Datastore.SQL.Datastore` | yes |
| `Datastore/tests/test_layer_registry.py:594` | `Datastore.SQL.ClientPool` | yes |
| `Datastore/tests/test_layer_registry.py:595` | `Datastore.store_reader` | yes |
| `Datastore/tests/test_layer_registry.py:596` | `Datastore.store_inventory` | yes |
| `Datastore/tests/test_layer_registry.py:618` | `Datastore.SQL.ObjectFactories.base` | yes |
| `Datastore/tests/test_read_only_pool.py:882` | `Datastore.SQL.ShardedPool.sqlite3.connect` | no |
| `prompts/datastore-generic/orchestrator/measure-08/scripts/m5_imports.py:14` | `Datastore.store_inventory` | yes |
| `prompts/datastore-generic/orchestrator/measure-08/scripts/m5_imports.py:15` | `Datastore.store_reader` | yes |
| `prompts/datastore-generic/orchestrator/measure-08/scripts/m5_imports.py:16` | `Datastore.contract` | yes |

## `import_module` calls naming a layer module

| File:line | Call | Argument |
|---|---|---|
| `Datastore/tests/schema_description.py:185` | `import_module` | `Datastore.SQL.Datastore` |
| `Datastore/tests/standin_pool.py:43` | `import_module` | `Datastore.SQL.ShardedPool` |
| `Datastore/tests/standin_pool.py:44` | `import_module` | `Datastore.SQL.Datastore` |
| `Datastore/tests/standin_pool.py:45` | `import_module` | `Datastore.SQL.SerialPoolBroker` |
| `Datastore/tests/test_layer_registry.py:66` | `import_module` | `Datastore.SQL.Datastore` |
| `Datastore/tests/test_schema_builder.py:160` | `import_module` | `Datastore.SQL.Datastore` |
| `Datastore/tests/test_wkb_numeric_parent_key.py:88` | `import_module` | `Datastore.SQL.Datastore` |
| `docs/datastore-integrity-audit/replicated_write_fault_probe.py:37` | `import_module` | `Datastore.SQL.ShardedPool` |
| `docs/datastore-integrity-audit/replicated_write_fault_probe.py:38` | `import_module` | `Datastore.SQL.Datastore` |
| `docs/datastore-integrity-audit/replicated_write_fault_probe.py:39` | `import_module` | `Datastore.SQL.SerialPoolBroker` |
| `prompts/datastore-generic/orchestrator/measure-07/scripts/m2_open_behaviour.py:30` | `import_module` | `Datastore.SQL.ShardedPool` |

## Imports of factory modules, by group (count only)

| Group | Statements |
|---|---|
| `ComputeTargets/` | 17 |
| `Datastore/SQL/ObjectFactories/` | 2 |
| `Datastore/tests/` | 46 |
| `config/` | 20 |
| `docs/` | 15 |
| **total** | **100** |

## Files that do not parse

None.
