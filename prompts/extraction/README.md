# Campaign — extraction

**Written:** 2026-10-07 by Claude Opus 5.5, at the user's request, from a comparison of the three
client projects' datastore layers made the same day (§0.2). **Prompt 01 is written** (2026-10-07):
G1 held and the user took U2–U5 as recommended. Its import commit is SGK `6f7f291`. 01 landed as
`8bc60a5` and was reviewed; **prompt 02 is written** (2026-10-07), with U8 taken, and landed as
`e988e69` and was reviewed. Each later
prompt is written after the one before it has landed and been reviewed, against the tree it left.

## 0. Why this campaign exists

Three projects run the same `RayWorkPool` / `Datastore` / `ShardedPool` framework, each from its
own copy:

- **SecondaryGWKit (SGK)** carries the developed copy. Since September 2026 it has had:
  - relative shard paths;
  - copy, move and delete of closed stores;
  - checked and recorded replicated writes, with repair or refusal at open;
  - a read-only pool;
  - a structured inventory;
  - refusal of a store whose schema differs.

  Its `datastore-generic` campaign (closed 2026-10-06) then made the layer generic again. Seventeen
  files name no SGK table and import no SGK package other than `config.defaults` and `utilities`,
  and a guard test (`Datastore/tests/test_layer_is_generic.py`) keeps it so.
- **ChamPBH (CPBH)** and **StochasticInstantons (SI)** carry copies close to SGK's of late 2025
  (§0.2).

The copies have already let a serious fix fall through:
- **The shard-key fix.** `_assign_shard_keys` inserted `key_id` into a table keyed by `key_serial`,
  so the β→shard map saved on disk could differ from the one in memory after a reopen. It was fixed
  in SI (`20d9a61`) and in SGK (`2610abe`). SI wrote `shard-key-assignment-bug.md` so that another
  instance could find and apply the fix in a sister codebase. On 2026-10-07 CPBH still carried the
  bug.
- **Absolute shard paths.** Both CPBH and SI still record them. A copied CPBH primary therefore
  writes into the original's shards.

**The user decided on 2026-10-07 (§6.1)** to extract the layer as a separate, reusable component,
starting with `Datastore` / `ShardedPool` only. This campaign:
- builds that component, `datastorekit`, from SGK's layer;
- gives it a test suite that needs no client;
- adds the one generic feature a client needs that SGK lacks (CPBH's version-keyed lookups);
- hands each client a checklist for adopting it.

Each client adopts it in a campaign of its own, in its own repository (§7).

### 0.1 What "extraction" means here

The package is SGK's layer, **moved, not rewritten**. Through prompt 05, every module of the
package equals its SGK source at the import commit, except for:
- the mechanical import rewrite of §4;
- the two internalised client dependencies.

A stored byte does not change. So SGK's adoption (gate G2) can be checked the way SGK checked its
own generic campaign: a rehearsal rebuild through the package must reproduce SGK's store
fingerprint. Improvements, including fixes for the inherited issues in `docs/OPEN_ISSUES.md`
§1.2, come after, in campaigns of their own.

### 0.2 Measurements taken by the planner (2026-10-07, read-only)

**The layer**, as SGK's guard defines it (`layer_files()` at `21ee420`), is 17 files. This
campaign takes 15 of them, together with two tools that import only the layer:

| SGK file | Lines (at `4c34f13`) |
|---|---|
| `Datastore/__init__.py`, `object.py`, `contract.py` | 1, 21, 27 |
| `Datastore/replication.py`, `shard_paths.py` | 300, 122 |
| `Datastore/store_reader.py`, `store_inventory.py` | 238, 1049 |
| `Datastore/SQL/__init__.py`, `schema.py` | 1, 513 |
| `Datastore/SQL/ShardedPool.py`, `Datastore.py` | 3627, 895 |
| `Datastore/SQL/ClientPool.py`, `SerialPoolBroker.py`, `ProfileAgent.py` | 219, 149, 340 |
| `Datastore/SQL/ObjectFactories/base.py` | 62 |
| `tools/sharded_store.py`, `tools/shard_key_audit.py` | 80, 278 |

The two `RayTools/` files of the guard's list are excluded (§1).

**Client dependencies of those files.** Only two, both allow-listed by SGK's guard:
- `config.defaults.DEFAULT_STRING_LENGTH`, at `ShardedPool.py:36` and `ProfileAgent.py:10`. It is
  256 in all three clients.
- `utilities.WallclockTimer` (`Datastore.py:20`) and `utilities.format_time`
  (`ProfileAgent.py:11`).

**How far the copies have diverged** (changed lines by `diff`, against SI):

| File | CPBH vs SI | SGK vs SI |
|---|---|---|
| `ShardedPool.py` | 55 | 4,628 |
| `Datastore.py` | 170 | 679 |
| `ClientPool.py` | 41 | 56 |
| `SerialPoolBroker.py`, `ProfileAgent.py` | 0 | 15 each |
| `ObjectFactories/base.py` | 5 | 73 |
| `RayTools/RayWorkPool.py` (for the later unit of work) | 32 | 39 |

**Runtime versions** of the clients' `venv`s:

| Client | Python | Ray | SQLAlchemy |
|---|---|---|---|
| SGK | 3.12.15 | 2.43.0 | 2.0.39 |
| CPBH | 3.13.16 | 2.53.0 | 2.0.46 |
| SI | 3.13.16 | 2.55.1 | 2.0.46 |

SGK's layer has never run on Python 3.13 or Ray 2.5x.

**SGK's tests, by module, and where each goes.**
- Counts are `def test_` lines at `21ee420`, plus prompt 03's uncommitted module. Inherited test
  classes are not counted, so SGK's own count is higher (its board expects 739 after its prompt
  03).
- Each module is placed by its imports. The prompt that ports it re-checks the placement test by
  test.

| Goes to | Modules (tests) | Total |
|---|---|---|
| **01**: no client import | `test_shard_paths` (7), `test_shard_file_name` (4), `test_shardedpool_shard_paths` (10), `test_copy_move_store` (22), `test_delete_store` (26), `test_sharded_store_script` (5), `test_shard_key_audit_copy` (3), `test_shard_key_audit_refusals` (11); fixture `shard_store_fixtures.py` | 88 |
| **03**: the write path, on the stand-in pool | `test_replicated_write` (25), `test_reconcile_at_open` (41), `test_prune_at_open` (10), `test_version_row_at_open` (12), `test_read_only_pool` (23), `test_one_timestamp_per_write` (1 + inherited), `test_absolute_shard_record_refused` (12), `test_closed_store_refusals` (5) | 129 |
| **04**: schema, reader, registry and inventory | `test_schema_builder` (7), `test_store_schema` (13), `test_store_reader` (15), `test_store_inventory` (42), `test_inventory_declarations` (26, partly about SGK's report), `test_declared_facts` (25), `test_layer_registry` (20), `test_drop_refuses_dangling_references` (11), `test_foreign_key_check` (8), `test_layer_is_generic` (8, re-written as the package's guard) | 175 |
| **Stays in SGK**: about SGK's factories or SGK's tooling | `test_backgroundmodelvalue_roundtrip`, `test_database_errors_reach_the_caller`, `test_exact_identity_lookups`, `test_factory_select_columns`, `test_gksource_parent_set`, `test_integral_read_batch`, `test_inventory_consumers`, `test_inventory_report`, `test_inventory_report_labels`, `test_inventory_retired`, the four `test_quadsource_*`, `test_read_path_mechanics`, `test_value_reads_parent_key`, `test_wkb_numeric_parent_key`, `test_wkb_parent_foreign_key` | 320 |

**The fixtures:**
- `shard_store_fixtures.py` and `schema_description.py` import no client.
- `standin_pool.py` (581 lines) imports the layer by module name at its top. It reaches SGK's
  config and classes only inside `open_pool` and its object helpers, from about `:287`.
- `real_store_fixtures.py` (1,350 lines) is SGK's.

**What a client must supply** to the layer at `4c34f13`:
- constructor arguments;
- `register()` keys;
- factory hooks;
- `inventory_spec`;
- the layer-owned `version` and `store_tag` tables.

These were surveyed the same day. Prompt 02 writes them down as `docs/client-contract.md`, and
measures the survey again before doing so.

## 1. Scope

**In scope:**
- the package `datastorekit`: SGK's 15 layer files and two tools, moved under the names of §4;
- `pyproject.toml`; the two internalised dependencies; `PROVENANCE.md`;
- a neutral test client and stand-in pool under `datastorekit/tests/`;
- SGK's tests of the layer's own behaviour, re-fixtured onto the neutral client;
- the package's guard test; the supported-version statement and CI;
- version-keyed lookups (`key_on_version`), ported from CPBH as an optional `register()` key;
- `docs/client-contract.md`, and the per-client adoption checklists;
- the releases `v0.1.0` (05) and `v0.2.0` (06).

**Out of scope:**
- **any edit to SGK, CPBH or SI.** Each adopts in its own campaign (§7);
- **`RayWorkPool`.** The user decided that reconciling it across the three projects and extracting
  it is a separate unit of work (§6.1). Its type-hint import of `ShardedPool` is a client import
  for the adoption campaigns to rewrite;
- **any change to what the layer writes or how it behaves** before 06 (§5 rule 8). This includes
  fixing an inherited issue (`docs/OPEN_ISSUES.md` §1.2) or anything a prompt finds: it is
  recorded, not fixed;
- **renaming the layer's modules to PEP 8 names** (U5);
- `RunRegistry/`, sidecars, fingerprints and `tools/inventory_report.py`, which are SGK's.
  **The fingerprint function** (`RunRegistry/stores.py`) stays in SGK, and so do its tests. The
  registry is itself a candidate for a later extraction, but not alongside this one (§8.2);
- **CPBH's bare shard key** in `object_get_vectorized`. CPBH converts its seven callers to the dict
  form when it adopts; it is not added here;
- **any store of any client.** Tests build their stores in temporary directories (§3).

## 2. Prompts

| # | Prompt | Covers | Status |
|---|---|---|---|
| 01 | [`01-import-the-layer.md`](01-import-the-layer.md) | The package skeleton (`pyproject.toml`, `datastorekit/`), SGK's 15 files and two tools at the import commit, under §4's names. The two client dependencies are internalised: `datastorekit.defaults.DEFAULT_STRING_LENGTH = 256`, and `datastorekit._timing` holding `WallclockTimer` and `format_time`, copied from SGK's `utilities.py`. `PROVENANCE.md` records the source commit and the file map. The 88 client-free tests and `shard_store_fixtures.py` are ported. A first guard test checks that the package imports only the standard library, `ray`, `sqlalchemy` and itself. **Acceptance:** <br>• `import datastorekit` works in a fresh venv with no client on `sys.path`; <br>• a script compares each package module with its SGK source, and finds no difference beyond the rewrite map and the two internalisations; the script is kept in `docs/extraction/` and its output in the log; <br>• the 88 tests pass. | **landed** 2026-10-07 (`8bc60a5`), reviewed |
| 02 | `02-the-neutral-test-client.md` | `docs/client-contract.md`, re-measured: every constructor argument, `register()` key, hook, declaration and layer-owned table, saying which are required, optional or defaulted. A neutral test client under `datastorekit/tests/client/` that exercises each item at least once, with abstract names: <br>• a shard-key class; <br>• replicated leaf tables, one with `monotone_flags`; <br>• a sharded parent with `validate_on_startup`; <br>• a replicated owner with `validated_column`, `revalidate` and `owned_serials`, and its replicated value table (`owner_column`) *(amended at 02's review: the layer reads these, and `monotone_flags`, for replicated classes only)*; <br>• a tag association; <br>• a polymorphic `Parent`; <br>• `read_table`, `read_batch` and `stepping`. <br>The generic part of `standin_pool.py` is ported with its defaults pointed at that client. The 88 tests of 01 move onto the client's names (U8), and the equivalence check gains the two classes this needs and fails on an unaccounted file. **Acceptance:** the log's table maps each contract item to the fixture that exercises it, and every item is covered. | **landed** 2026-10-07 (`e988e69`), reviewed |
| 03 | `03-port-the-write-path-tests.md` | The 129 write-path tests of §0.2, re-fixtured onto the neutral client: replicated writes, the check at open (compare, repair, refuse), the prune at open, the version row, the read-only pool, and shard records. Each test keeps its name and its assertions. A test that cannot be expressed on the neutral client is listed in the log with the reason, and is not dropped silently. | not written |
| 04 | `04-port-the-schema-and-inventory-tests.md` | The 175 tests of §0.2 for the schema builder, the schema refusal, the reader, the registry, drop refusal and the inventory, re-fixtured the same way. SGK's `test_layer_is_generic` becomes the package's guard. Its forbidden vocabulary is drawn from all three clients' registries, measured read-only and written into the test as data; the test never imports a client. | not written |
| 05 | `05-supported-versions-and-ci.md` | Dependency ranges in `pyproject.toml`. The whole suite runs at both ends of §0.2's version table (Python 3.12 / Ray 2.43 / SQLAlchemy 2.0.39, and Python 3.13 / Ray 2.55 / SQLAlchemy 2.0.46). A GitHub Actions workflow runs the suite on both. `README.md` gains usage. **Tag `v0.1.0`**, the release SGK adopts (G2). | not written |
| 06 | `06-version-keyed-lookups.md` | CPBH's version-keyed lookups (`Datastore.py:329-338`, `:500-555`; `config/version.py:55-71` at CPBH `9b3db51`), as the optional `register()` key `key_on_version`. A lookup of a class that declares it receives the store's version serial under `datastorekit.contract.VERSION_SERIAL_KEY`. A caller that supplies that key itself is refused. `key_on_version` without `version` is refused at schema build. `require_version_serial` is exported for factories. Tests on the neutral client carry over the semantics of CPBH's `test_version_keyed_lookups`. Nothing the layer writes changes. **Tag `v0.2.0`.** | not written |
| 07 | `07-close-out-and-adoption-handover.md` | `docs/adoption/` holds one checklist per client (SGK, CPBH, SI), each saying: <br>• which imports to rewrite; <br>• where its factories move to; <br>• what its factories must change; <br>• what its call sites and test harness must change; <br>• which of its stores the new layer will refuse, and why. <br>SGK's checklist also names every import of the layer from outside `Datastore/`. In particular, `RunRegistry/` imports `Datastore.SQL.ShardedPool.ShardedPool` three times, `Datastore.store_inventory.canonical_json` twice and `Datastore.store_inventory.read_inventory` once (counted at `21ee420`), and G2's rehearsal fingerprint runs through `RunRegistry/stores.py::fingerprint_store`. Also: SGK's `docs/` scripts that import the layer, and `RayTools/RayWorkPool.py`'s type-hint import. 07 re-counts them. <br>Also a verification document for the campaign, and the campaign closed. | not written |

**Order.** 01 → 02 → 03 and 04 (either order, but never concurrently, since both edit the
stand-in pool) → 05 → 06 → 07. 06 needs only 02. It is placed after 05 so that `v0.1.0`
contains exactly SGK's behaviour.

## 3. Datastores

**No prompt opens a store of any client**, whether a production, pilot, science or rehearsal
store, read-only or not. Tests build their stores in `tempfile` directories. A measurement that
needs a client's code (02's contract survey, 04's vocabulary) **reads source files**; it does not
import a client or run a client's tests. The rehearsal rebuild that proves G2 is SGK's, run by a
person under SGK's rules.

## 4. The interfaces between prompts

**Fixed by this plan:**

- **The package** is `datastorekit`, distributed as `datastorekit` from this repository.
- **The module map.** SGK's module names are kept (U5). The rewrite is mechanical:

  | SGK | `datastorekit` |
  |---|---|
  | `Datastore` (`__init__`, `object`, `contract`, `replication`, `shard_paths`, `store_reader`, `store_inventory`) | `datastorekit.<same>` |
  | `Datastore.SQL.<ShardedPool, Datastore, ClientPool, SerialPoolBroker, ProfileAgent, schema>` | `datastorekit.SQL.<same>` |
  | `Datastore.SQL.ObjectFactories.base` | `datastorekit.SQL.factory_base` |
  | `tools.sharded_store`, `tools.shard_key_audit` | `datastorekit.tools.<same>`, run as `python -m datastorekit.tools.<name>` |
  | `config.defaults.DEFAULT_STRING_LENGTH` | `datastorekit.defaults.DEFAULT_STRING_LENGTH` |
  | `utilities.WallclockTimer`, `utilities.format_time` | `datastorekit._timing.<same>` |

  A client's factories leave the layer's directory. Where they go is the client's choice, made in
  its adoption campaign.
- **After 01:** `datastorekit/tests/shard_store_fixtures.py`; the import guard
  `datastorekit/tests/test_package_imports.py`; `docs/extraction/compare_with_source.py` and
  `PROVENANCE.md`.
- **After 02:** `docs/client-contract.md`; the neutral client `datastorekit/tests/client/`; the
  stand-in pool `datastorekit/tests/standin_pool.py`. 02 names their entry points, and 03 and 04
  use them.
- **After 06:** `register()["key_on_version"]`; `datastorekit.contract.VERSION_SERIAL_KEY` and
  `datastorekit.contract.require_version_serial`.

## 5. The rules this campaign runs under

The project-wide ones in `CLAUDE.md`, plus:

1. **One commit per prompt**, in this repository only.
2. **Every prompt writes a log** to `logs/NN-<name>.md`, using §5.1.
3. **Every prompt updates `IMPLEMENTATION_STATE.md`** in its own commit, plus
   `docs/OPEN_ISSUES.md`.
4. **Do not fix things the prompt did not ask for.** This applies above all to behaviour inherited
   from SGK: a defect found in it is recorded, with a §3 issue, not fixed (rule 8).
5. **No prompt edits a client repository** (`CLAUDE.md`). Reading one is allowed. Running a
   client's code or tests, or opening a client's store, is not.
6. **Ported tests keep their names and assertions.** A ported test is re-fixtured only. The log
   lists each with its SGK origin (module, class, method). A test that cannot be expressed without
   a client is recorded with the reason, not dropped silently.
7. **No test needs a Ray cluster, imports a client, or opens a store outside a `tempfile`
   directory.** The suite count is recorded before and after each prompt; a count that falls is a
   stop.
8. **Equivalence with the source, through 05.** Every package module equals its SGK source at the
   import commit, modulo §4's map and the two internalisations. `compare_with_source.py` checks
   this, and each prompt runs it. Any other difference is a stop. 06 adds behaviour only behind a
   `register()` key that no SGK factory declares, and writes nothing new.
9. **Deliberate breakage.** Each prompt names mutations its tests must catch. The log records each
   as a diff, exactly as applied, so the orchestrator can replay it with `git apply`. Mutations are
   never committed.
10. **No tag except where a prompt says so** (05: `v0.1.0`; 06: `v0.2.0`), and none is moved or
    deleted.

### 5.1 The log template

- the subject, commit and result;
- **What shipped**;
- **Deviations from the prompt**, each classified;
- **Verification performed**: suite count before and after, and the output of
  `compare_with_source.py`;
- **The deliberate-breakage record**;
- **Observations not acted on**;
- **State handed to the next prompt**.

## 6. Decisions

### 6.1 Made by the user (2026-10-07), and not reopened here

- **D1: extract the layer as a separate, reusable component**, rather than copy SGK's layer into
  each client.
- **D2: `Datastore` / `ShardedPool` first.** `RayWorkPool` has diverged across the three projects.
  Reconciling and extracting it is a separate unit of work.
- **D3: a public GitHub repository**, `ds283/DatastoreKit`, under `/Users/ds283/Documents/Code/`.
  The user offered the names DataKit and DatastoreKit; DatastoreKit was taken at set-up (U1).
- **D4: CPBH's stores are rebuilt, not migrated.** The science store costs a few hours. This is
  recorded for CPBH's adoption checklist (07); it is not this campaign's to act on.

### 6.2 Decisions this campaign needs

Each is put with a recommendation. **U2–U5 were taken by the user on 2026-10-07, each as
recommended**; the recommendation below is the decision. U1 and U7 were applied at set-up. U6 is
open until 05 is written.

- **U1: the name.** *Taken at set-up, changeable until 01 lands:* the repository is
  **DatastoreKit**, the package `datastorekit`. "DataKit" names many unrelated tools, and
  "datastore" says what this is.
- **U2: history. (taken, as recommended)** **Recommended:** a fresh import, with `PROVENANCE.md` naming SGK's import commit
  and the file map. SGK's history stays the record of how the layer came to be, reachable through
  that commit. **Rejected:** `git filter-repo` over SGK to carry the 17 files' history here. It
  would bring many commits whose messages refer to SGK campaigns, boards and stores that do not
  exist in this repository, and file renames make the result hard to follow.
- **U3: SGK's layer is frozen from the import commit until SGK adopts (G2). (taken, as recommended)** **Recommended:**
  between G1 and G2, SGK lands no change to its 15 layer files or the two tools. A defect found
  there in that time is recorded on SGK's board, and fixed here after G2. **Rejected:** mirroring
  SGK changes here as they land. That makes the import commit a moving target and breaks rule 8's
  check. In force from SGK `b510bc9` (2026-10-07), a section of SGK's `CLAUDE.md` naming the frozen files.
- **U4: distribution. (taken, as recommended)** **Recommended:** clients pin a tag in `requirements.txt`
  (`datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.1.0`); an editable install is for
  developing the package only (`CLAUDE.md`, "Releases"). **Rejected:**
  - a git submodule, which is awkward to update and easy to leave detached;
  - a vendored copy with a pinned hash, as CPBH does for `PRyM/`, which is the drift this campaign
    exists to end;
  - an unpinned editable install shared by all three clients, under which a change made for one
    client silently changes another's production run;
  - publishing to PyPI, which is not needed for three private consumers, and can come later.
- **U5: module names. (taken, as recommended)** **Recommended:** keep SGK's names (`SQL`, `ShardedPool.py`, …) through
  this campaign, so that rule 8's check stays mechanical and every client's rewrite is a prefix
  substitution. **Rejected for now:** PEP 8 names (`datastorekit.sql.sharded_pool`). They are a
  later, separate change, once the clients are on the package.
- **U6: the supported range and CI.** **Recommended:** Python ≥ 3.12, Ray and SQLAlchemy ranges
  covering §0.2's table, and a GitHub Actions matrix at the two ends (05). **Rejected:** testing
  only on the developer's machine. SGK's code has never run on Python 3.13 or Ray 2.5x, and two of
  the three clients run them.
- **U7: the licence.** *Applied at set-up, changeable:* Apache 2.0, as CPBH and SI use. SGK has no
  licence file, and a public repository needs one.
- **U8: SGK's table names in the 88 tests 01 ported. (taken 2026-10-07, as recommended)** 01
  found that its fixture and two of its test modules use SGK's table names as data
  (`[01-ported-tests-use-sgk-table-names]`). **Recommended:** 02 moves them onto the neutral
  client's names, as re-fixturing under rule 6: a name changes only inside a string literal, and an
  expected string changes only where it echoes the fixture's name back. The equivalence check
  gains a class for it, restricted to those files (02 §2.4, §2.6). The issue then closes in 02, and
  04's vocabulary guard needs no exemption. **Rejected:** keeping SGK's names and exempting the
  files from 04's guard, which leaves a client's vocabulary in the package's tests for good.

## 7. Gates outside this repository

| Gate | Holds when | Needed by |
|---|---|---|
| **G1** | SGK's `datastore-generic-followup` has closed: its prompt 03 landed and was reviewed. The commit that closes it is the **import commit**. SGK's tree is clean at it, and SGK's suites pass there. **Holds (2026-10-07):** 03 landed as `086c81a` and its review `6f7f291` closed the campaign, so the import commit is **`6f7f291`**. The next commit, `99456d8`, adds only a `.tex` status note. | 01 |
| **G2** | SGK has adopted `v0.1.0` in a campaign of its own: its 15 layer files and two tools are deleted, it imports `datastorekit` at a pinned tag, its remaining suites pass, and a rehearsal rebuild through the package reproduces its reference fingerprint (run by a person, under SGK's rules). | CPBH's adoption; the end of U3's freeze |
| **G3** | CPBH has adopted `v0.2.0` in a campaign of its own (07's checklist; its stores rebuilt, D4). | — |
| **G4** | SI has adopted, when it is next active. | — |

The campaign closes at 07. G2–G4 are recorded on this board as they hold, but this campaign does
not wait for them.

**CPBH in the meantime.** The shard-key bug was fixed in CPBH's own copy on 2026-10-07, outside
this campaign, so that CPBH runs made before G3 keep a correct shard map. CPBH's absolute shard
paths remain until G3. Until then, a copy of a CPBH store, in any directory, still opens the
original's shards, so a copy is a backup only and is never run against.

## 8. Later units of work

These are recorded so that their planning starts from what is known. **None of them is in this
campaign's scope**, and none is planned yet.

### 8.1 `RayWorkPool`

Reconciling and extracting `RayTools/RayWorkPool.py` is a separate unit of work (D2). §0.2's
diff counts suggest the three copies are closer than expected: 39 changed lines between SGK and
SI, and 32 between CPBH and SI. SI already has SGK's split of the store and persist handlers.

### 8.2 SGK's run registry (assessed 2026-10-07, read-only, at `21ee420`)

The user raised `RunRegistry/` as another shared service that could be extracted, but **not at
the same time as DatastoreKit**. What the planner found:

**Size and shape.** 3,346 lines in three modules, in two layers:

| Module | Lines | What it does | Imports outside the standard library |
|---|---|---|---|
| `RunRegistry/__init__.py` | 646 | **Run records:** `var/runs/<id>/` holding a manifest (written once), a status file (mutable), an append-only checkpoint ledger and logs; liveness by `kill -0` plus heartbeat; git and script-hash provenance; `list_runs` | none |
| `RunRegistry/__main__.py` | 515 | Command line: `list` and the `store …` commands | through `stores` |
| `RunRegistry/stores.py` | 2,185 | **Store management:** the `<stem>.manifest.json` sidecar; create and adopt; copy and move with history; the store fingerprint; `store retire` and `store amend`; finding a store's references in runs and other sidecars | the layer: `ShardedPool` (×3), `store_inventory` (`read_inventory`, `canonical_json`); and SGK's `config.datastore.factories`, inside `fingerprint_store` (`:1494`) |

SGK's `main.py` does not import the registry. Pipeline runs are registered by drivers (for
example `docs/gktk-remedial/scoped_pipeline_run.py`) and under the six rules in SGK's
`CLAUDE.md`. CPBH and SI have no registry, so there is nothing to reconcile: it would be an
extraction only.

**What extraction would have to solve:**
1. **The root.** `REPO_ROOT = dirname(dirname(__file__))` (`__init__.py:56`) fixes `var/runs`,
   `var/datastores` (`stores.py:185`) and the directory git provenance is read from. In an
   installed package that is the package's own directory. The client's root has to be given (an
   argument, an environment variable, or `git rev-parse` from the working directory). This is
   the main change to the run-records layer.
2. **The fingerprint's registry.** `fingerprint_store` imports `config.datastore.factories`. It has
   to be given the registry, as the layer's reader is (`open_read_only(primary, factories)`).
3. **The store layer sits on DatastoreKit.** Fingerprint, copy, move and retire call the layer, so
   this half can move only after G2, once SGK imports `datastorekit`.
4. **The policy is prose.** SGK's six registry rules in `CLAUDE.md` (liveness never by command-line
   pattern; launch detached, manifest first; do not babysit; and the rest) are half of what the
   registry is. They would ship as package documentation that each client's `CLAUDE.md` cites.

**Tests** (282 by `def test_`):
- **About 82 port cleanly:** `test_run_registry` (23), `test_store_amend_residuals` (9),
  `test_store_command_line` (2), `test_store_retire_references` (10), `test_store_amend` (21) and
  `test_store_sidecar` (17). The last two use only `shard_store_fixtures`, which 01 ports.
- **About 101 port after a fixture swap:** `test_store_copy_move` (27), `test_store_fingerprint`
  (33) and `test_store_retire` (41). They need 02's neutral client in place of SGK's real-store
  fixtures.
- **About 97 stay in SGK.** They test SGK's own pipeline and drivers: `test_killed_handler`,
  `test_pipeline_adoption`, `test_prune_on_resume`, `test_build_rehearsal_scope` and
  `test_quadsource_atol_sweep_prepare`.

**The planner's recommendation, for when it is planned:**
- **One package, two tiers.** The run-records core needs nothing beyond the standard library. A
  `stores` submodule, installed as an optional extra, depends on `datastorekit`. A client can then
  take the run records without the store sidecars.
- **Not inside DatastoreKit.** The layer does the copying, moving and deleting. Sidecars, history
  and retirement are provenance policy on top of that. Putting them in the layer would bring
  registry concepts back into a layer that has just been cleared of client knowledge.
- **When.**
  - The run records can be extracted at any time; they do not depend on this campaign. They would
    serve CPBH's long production runs, which its `CLAUDE.md` says have no registry today.
  - The store tier waits for G2 and a release containing 02's neutral client.
  - The first prompt fixes the root (item 1).
