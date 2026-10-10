# Campaign — extraction

**Written:** 2026-10-07 by Claude Opus 5.5, at the user's request, from a comparison of the three
client projects' datastore layers made the same day (§0.2). **Prompt 01 is written** (2026-10-07):
G1 held and the user took U2–U5 as recommended. Its import commit is SGK `6f7f291`. 01 landed as
`8bc60a5` and was reviewed; **prompt 02 is written** (2026-10-07), with U8 taken, and landed as
`e988e69` and was reviewed. The user took U9–U12 the same day, splitting 03 into 03a and 03b;
**prompt 03a is written** (2026-10-07), and landed as `11247c7` and was reviewed. The user took U13
the same day; **prompt 03b is written** (2026-10-07), and landed as `0d5380c` (2026-10-08) and
was reviewed. The user took U14–U17 on 2026-10-08, splitting 04 into 04a and 04b; **prompt 04a is
written** (2026-10-08). Its orchestrator found a test the neutral client could not pass, and the
user took U18 the same day; its agent stopped on a 03a test the new client breaks, and the user
took U19, and on its second stop U20 and U21. 04a landed as `7ceed25` (2026-10-08) and was
reviewed; **prompt 04b is written** (2026-10-08). Its agent stopped on two tests that cannot hold
over a class that registers `None`, and the user took U22. 04b landed as `0c66505` (2026-10-08)
and was reviewed. The user took U6, U23 and U24 on 2026-10-09; **prompt 05 is written**
(2026-10-09), and landed as `68db557` and was reviewed; CI passed there at both ends, and `v0.1.0` is
tagged on it (U23). The user took U25–U28 the same day; **prompt 06 is written** (2026-10-09),
and landed as `240028e` and was reviewed; CI passed there at both ends, and `v0.2.0` is tagged
on it (U28). The user took U29–U32 the same day, splitting 07 into 07a and 07b; **prompt 07a is
written** (2026-10-09), and landed as `dd45243` and was reviewed. The user took U33–U37 the
same day: the four issues the board holds open are fixed before the campaign closes, in 08a, 08b
and 09, and released by 10 as **`v0.2.1`**, which the clients adopt in place of `v0.2.0`; 07b is
withdrawn, and its verification and close-out are 11's. **Prompt 08a is written** (2026-10-09), and landed as `f938844` (2026-10-10) and was reviewed.
**Prompt 08b is written** (2026-10-10), and landed as `efedc8d` the same day and was reviewed.
The user took U38–U40 the same day; **prompt 09 is written** (2026-10-10), and landed as
`cad7bc1` the same day and was reviewed. **Prompt 10 is written** (2026-10-10), and landed as
`33778b0` the same day and was reviewed; CI passed there at both ends, and `v0.2.1` is tagged
on it. The user took U41 and U42 the same day; **prompt 11 is written** (2026-10-10), and landed as
`39b1348` the same day and was reviewed. **The campaign is closed** (2026-10-10, by prompt 11), with G2–G4 open (§7).
Each later prompt is written after the one before it has landed and been
reviewed, against the tree it left.

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
- the releases `v0.1.0` (05) and `v0.2.0` (06);
- *(U33, 2026-10-09)* the fixes of the four issues the board's §3 holds open (08a, 08b, 09), the
  release `v0.2.1` (10), and the adoption checklists' addenda for it (U37).

**Out of scope:**
- **any edit to SGK, CPBH or SI.** Each adopts in its own campaign (§7);
- **`RayWorkPool`.** The user decided that reconciling it across the three projects and extracting
  it is a separate unit of work (§6.1). Its type-hint import of `ShardedPool` is a client import
  for the adoption campaigns to rewrite;
- **any change to what the layer writes or how it behaves** before 06 (§5 rule 8). This includes
  fixing an inherited issue (`docs/OPEN_ISSUES.md` §1.2) or anything a prompt finds: it is
  recorded, not fixed *(U33 takes the four issues of the board's §3 into scope for 08a–09; the
  issues of `docs/OPEN_ISSUES.md` §1.2 stay out)*;
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
| 03a | [`03a-port-the-replicated-write-tests.md`](03a-port-the-replicated-write-tests.md) | U10's first half of §0.2's 129 write-path tests: `test_replicated_write` (25), `test_reconcile_at_open` (41) and `test_prune_at_open` (10), re-fixtured onto the neutral client. Each test keeps its module, class and method name and its assertions; the changes allowed are R-imp, R-map, R-help, R-value, R-count and R-name (03a §2.1). `docs/extraction/compare_ported_tests.py` checks the names and each test's assertion skeleton against SGK's (U9), and `compare_with_source.py` gains a `PORTED` kind. A new test pins `_assign_shard_keys` against the `key_id` binding, and a ported test reaches `revalidate`. **Acceptance:** the port check passes; `[02-no-test-reaches-revalidate]` and `[01-no-ported-test-pins-the-shard-key-assignment]` close, each by a test a named breakage fails. | **landed** 2026-10-07 (`11247c7`), reviewed |
| 03b | [`03b-port-the-open-and-read-only-tests.md`](03b-port-the-open-and-read-only-tests.md) | The other half: `test_version_row_at_open` (12), `test_read_only_pool` (23, onto `build_store` and a neutral reader sequence, U11; four test names change by the table map, U12), `test_one_timestamp_per_write` (1 defined, 28 run, by inheritance from 03a's modules and `test_version_row_at_open`), `test_absolute_shard_record_refused` (12) and `test_closed_store_refusals` (5): 53 defined, 80 run. Checked the same way. A test that cannot be expressed on the neutral client is a stop, not a silent drop. Two replicated classes are added to the neutral client for it (U13). | **landed** 2026-10-08 (`0d5380c`), reviewed |
| 04a | [`04a-port-the-store-and-inventory-tests.md`](04a-port-the-store-and-inventory-tests.md) | U14's first half of §0.2's 175: `test_store_inventory` (42), `test_store_schema` (13), `test_store_reader` (15), `test_foreign_key_check` (8) and `test_schema_builder` (7), 85 tests, re-fixtured as 03a's were. SGK's `real_store_fixtures` and `schema_description` are ported, the first with neutral row data on a hand-built store with fixed serials, and a neutral schema witness is captured. The neutral client gains a small sharded family for the roles it lacks (U15). **Acceptance:** the port check passes over 15 modules; the suite is 353. | **landed** 2026-10-08 (`7ceed25`), reviewed |
| 04b | [`04b-port-the-declaration-and-registry-tests.md`](04b-port-the-declaration-and-registry-tests.md) | The other half: `test_inventory_declarations` (26, of which one stays in SGK, U16), `test_declared_facts` (25), `test_layer_registry` (20) and `test_drop_refuses_dangling_references` (11), on 04a's fixture. SGK's `test_layer_is_generic` (8) becomes the package's guard. Its forbidden vocabulary is drawn from all three clients' registries, measured read-only and written into the test as data; the test never imports a client, and the hits rule 8 freezes in the layer are pinned (U17). *(At writing: the vocabulary is held in `tests/data/client_vocabulary.json`, written by `docs/extraction/measure_client_vocabulary.py`, and a new `test_parent_set_members` closes `[04a-no-test-pins-a-second-parent-set-member]`.)* **Acceptance:** the port check passes over 20 modules with one test declared not ported; the guard pins exactly one hit; the suite is 444. | **landed** 2026-10-08 (`0c66505`), reviewed |
| 05 | [`05-supported-versions-and-ci.md`](05-supported-versions-and-ci.md) | Dependency ranges in `pyproject.toml`. The whole suite runs at both ends of §0.2's version table (Python 3.12 / Ray 2.43 / SQLAlchemy 2.0.39, and Python 3.13 / Ray 2.55 / SQLAlchemy 2.0.46). A GitHub Actions workflow runs the suite on both. `README.md` gains usage. **Tag `v0.1.0`**, the release SGK adopts (G2). *(At writing: the range is U6's; both ends run locally in fresh scratch venvs (U24) and from an installed wheel, which no longer carries the test package; 05 makes no tag and pushes nothing, and `v0.1.0` is made on 05's commit once CI passes there (U23); 05 opens `[05-a-refused-open-leaves-its-engines-undisposed]`.)* | **landed** 2026-10-09 (`68db557`), reviewed; CI green at both ends; **tagged `v0.1.0`** |
| 06 | [`06-version-keyed-lookups.md`](06-version-keyed-lookups.md) | CPBH's version-keyed lookups (`Datastore.py:329-338`, `:500-555`; `config/version.py:55-71` at CPBH `9b3db51`), as the optional `register()` key `key_on_version`. A lookup of a class that declares it receives the store's version serial under `datastorekit.contract.VERSION_SERIAL_KEY`. A caller that supplies that key itself is refused. `key_on_version` without `version` is refused at schema build. `require_version_serial` is exported for factories. Tests on the neutral client carry over the semantics of CPBH's `test_version_keyed_lookups`. Nothing the layer writes changes. **Tag `v0.2.0`.** *(At writing: the neutral `Tessera` is the keyed class (U25); an actor holds a lookup serial apart from its insert serial, and a read-only pool gives it with `set_lookup_version` (U26); `compare_with_source.py` is retired at `v0.1.0` (U27); 06 makes no tag and pushes nothing, and `v0.2.0` is made on its commit once CI passes there (U28); the suite goes from 444 to 458, the schema witness gains one key, and 06 opens `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]`.)* | **landed** 2026-10-09 (`240028e`), reviewed; CI green at both ends; **tagged `v0.2.0`** |
| 07a | [`07a-the-adoption-checklists.md`](07a-the-adoption-checklists.md) | `docs/adoption/` holds a README and one checklist per client (SGK, CPBH, SI), each measured read-only at a named client commit and against `v0.2.0` (U29), each under the same ten items: <br>• the client and its versions; <br>• what it deletes; <br>• which imports it rewrites; <br>• what leaves the layer, and where it may go; <br>• what its factories must change (U32: a registered instance needs every abstract hook); <br>• its call sites and pool construction (`drop_actions`, `inventory_config`, bare shard keys); <br>• its tests and fixtures; <br>• which of its stores the package refuses, and why (CPBH: D4; SI: U31); <br>• its acceptance (G2–G4); <br>• what goes stale in it. <br>SGK's names every import of the layer from outside `Datastore/`, `RunRegistry/`'s and G2's `fingerprint_store` among them. A script, `docs/extraction/measure_client_imports.py`, counts every client's imports through `git` and `ast`, and each checklist carries its output. *(At writing: three read-only surveys measured SGK at `b510bc9`, CPBH at `52142d7` and SI at `7bb3efd`; 07a measures again.)* | **landed** 2026-10-09 (`dd45243`), reviewed |
| ~~07b~~ | ~~`07b-verification-and-close-out.md`~~ | *Withdrawn 2026-10-09, unwritten (U33, U35): its work is 11's, after the fixes and `v0.2.1`.* | withdrawn |
| 08a | [`08a-two-small-fixes.md`](08a-two-small-fixes.md) | `[02-an-unsupplied-sharded-table-raises-keyerror]`: a reopen whose primary records a sharded table the constructor lacks is refused with the intended `RuntimeError`, not a bare `KeyError`. `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]`: `object_get_vectorized` copies the caller's payloads. A test for each that the unfixed code fails. Nothing the layer writes changes. | **landed** 2026-10-10 (`f938844`), reviewed |
| 08b | [`08b-dispose-engines-on-a-refused-open.md`](08b-dispose-engines-on-a-refused-open.md) | `[05-a-refused-open-leaves-its-engines-undisposed]`: a refused or abandoned open disposes the engines the pool and its actors made, with a test that counts unclosed connections across a refused open (05's measurement: 105 over the 444, at three sites). *(At writing: 109 over the 469 at `2123445`, of which 107 are a raised constructor's and 2 a ported test's directly built actors; the open moves into `_open` under a guard, and `_close_refused_open` closes the actors and disposes the engine.)* | **landed** 2026-10-10 (`efedc8d`), reviewed |
| 09 | [`09-rewrite-the-package-prose.md`](09-rewrite-the-package-prose.md) | `[01-package-prose-names-sgks-layout]`: the package's comments and docstrings that name SGK's layout, campaigns or tables are rewritten for this repository (155 lines in 40 files at 04b), and the guard's `KNOWN_HITS` is emptied (U17). No code changes. *(At writing: still 155 in 40 at `452b3c9` by log 03a §8's method; U38 widens the scope to every citation of the source's layout, campaigns, logs, audits, issues, commits and `var/`, 248 lines in 42 files, of which 57 are found by reading; U39 removes each citation and keeps its explanation, true for this package; U40 adds `test_prose_names_no_source`, which scans every comment and docstring of the package with no allow list.)* | **landed** 2026-10-10 (`cad7bc1`), reviewed |
| 10 | [`10-release-v0.2.1.md`](10-release-v0.2.1.md) | `pyproject.toml` at `0.2.1`, `PROVENANCE.md` and `README.md`; both ends locally and in CI; **tag `v0.2.1`** on its commit after green CI (as U23, U28). Dated addenda to `docs/adoption/` for the new pin and what changed since `v0.2.0` (U37). *(At writing: only `SQL/ShardedPool.py` changed in code since `v0.2.0`, the other 12 changed layer files in prose only; a `0.2.1` wheel builds and installs offline with 25 entries; no client reads its payloads back (log 08a §2.5) or catches the `KeyError` 08a replaced; the addenda supersede 07a's statements by `path:line` and rewrite none.)* | **landed** 2026-10-10 (`33778b0`), reviewed; CI green at both ends; **tagged `v0.2.1`** |
| 11 | [`11-verification-and-close-out.md`](11-verification-and-close-out.md) | A verification document for the campaign, from the package at `v0.2.1` and the records of 01–10; the contract §8 citation corrected (U34); the campaign closed (U30, U33). *(At writing: the document is `docs/extraction-verification.md`; U41 adds a smoke run under a local `ray.init()` at both ends, a script in `docs/extraction/`, which the planner's probe passed in 10–13 s; U42 installs the pin from GitHub, whose 20 package files equal 10's wheel's; the probe found that a closed pool holds its actors' names until it is collected, inherited from SGK, which 11 opens as an issue; the contract's head gains a dated line, since 08a–09 moved lines its head leaves a reader to take as current.)* | **landed** 2026-10-10 (`39b1348`), reviewed; the campaign **closed** |

**Order.** 01 → 02 → 03a → 03b → 04a → 04b → 05 → 06 → 07a → 08a → 08b → 09 → 10 → 11. (03b and 04 could have run in either
order, but never concurrently, since both extend `compare_ported_tests.py`'s table and
`tests/client/build.py`; 03b ran first, and U14 split 04.) 04b needs 04a's fixture and client
classes. 06 needs only 02. It is placed after 05 so that `v0.1.0`
contains exactly SGK's behaviour. 07b was to verify and close after 07a's checklists (U30); U33
put the fixes first. 08a and 08b both change `ShardedPool.py`, so they run in order, never
concurrently. 09 rewrites prose in files 08a and 08b touch, so it follows them. 10 releases what
08a–09 leave, and 11 verifies and closes once `v0.2.1` is tagged.

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
  stand-in pool `datastorekit/tests/standin_pool.py`. 02 names their entry points, and 03a, 03b
  and 04 use them.
- **After 03a:** `docs/extraction/compare_ported_tests.py` and its `PORTED` table; the `PORTED` kind of
  `compare_with_source.py`; the ported modules `test_replicated_write`, `test_reconcile_at_open` and
  `test_prune_at_open`, which 03b's `test_one_timestamp_per_write` subclasses.
- **After 03b:** the neutral client's `gauge_setting` and `routing_rule` (U13), with
  `build.get_gauge` and `build.get_rule`; `datastorekit/tests/client/reader.py`, the neutral
  store, reader sequence and instrument (U11); `PORTED` and `NAME_MAP` over eight modules.
- **After 04a:** the neutral client's sharded family (U15); `datastorekit/tests/real_store_fixtures.py`
  (`build_real_store`, `build_full_store`, `full_rows`, `relabel_serials`, `find_row`, `vary_row`,
  `file_state` and the rest of SGK's public names, on neutral rows); `datastorekit/tests/schema_description.py`
  and the neutral witness under `datastorekit/tests/data/`; `PORTED` over fifteen modules.
- **After 04b:** the package's guard, `datastorekit/tests/test_layer_is_generic.py`, with its
  vocabulary as data (`datastorekit/tests/data/client_vocabulary.json`, written by
  `docs/extraction/measure_client_vocabulary.py`) and its pinned hits (U17); `NOT_PORTED` in
  `compare_ported_tests.py` (U16); `PORTED` over twenty modules.
- **After 05:** `pyproject.toml` at `0.1.0` with U6's range; `.github/workflows/tests.yml`; the
  README's usage. After its CI passes, the tag `v0.1.0` on 05's commit (U23).
- **After 06:** `register()["key_on_version"]`; `datastorekit.contract.VERSION_SERIAL_KEY` and
  `datastorekit.contract.require_version_serial`; `Datastore.set_lookup_version` (U26); the neutral
  `Tessera` keyed (U25); the witness `schema_at_extraction-06.json`; `pyproject.toml` at `0.2.0`.
  After its CI passes, the tag `v0.2.0` on 06's commit (U28).
- **After 07a:** `docs/adoption/` (a README and three checklists) and
  `docs/extraction/measure_client_imports.py`, which 11's verification document cites.
- **After 08a–09** (planned, U35): the layer's three fixes with their tests; the package's prose
  rewritten, and the guard's `KNOWN_HITS` empty. Each prompt names its own interfaces when it is
  written. *(At 09's writing: the prose guard `datastorekit/tests/test_prose_names_no_source.py`,
  U40.)*
- **After 10** (planned): `pyproject.toml` at `0.2.1`; the adoption addenda (U37). After its CI
  passes, the tag `v0.2.1` on 10's commit.
- **After 11** (planned): `docs/extraction-verification.md`, the campaign's verification document,
  and `docs/extraction/ray_smoke_run.py` (U41); the campaign closed.

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
10. **No tag except where a prompt says so** (05: `v0.1.0`; 06: `v0.2.0`; 10: `v0.2.1`), and none
    is moved or deleted.

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
recommended**; the recommendation below is the decision. U1 and U7 were applied at set-up. U6 was
taken on 2026-10-09, when 05 was written.

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
- **U6: the supported range and CI. (taken 2026-10-09, as recommended)** **Recommended:** Python
  ≥ 3.12, Ray and SQLAlchemy ranges covering §0.2's table, and a GitHub Actions matrix at the two
  ends (05). **Rejected:** testing only on the developer's machine. SGK's code has never run on
  Python 3.13 or Ray 2.5x, and two of the three clients run them. *At 05's writing the ranges were
  put as* `ray>=2.43` (no ceiling, so a client can move Ray without a release here) and
  `sqlalchemy>=2.0.39,<2.1` (2.1 is a minor series with breaking changes, and exists). The user
  took them, rejecting a ceiling at the tested ends and floors alone.
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

- **U9: how a re-fixtured test is checked against its source. (taken 2026-10-07, as
  recommended)** 01's tests were checked line by line, but 03 onwards swaps SGK's fixture helpers
  for the neutral client's, so a line-by-line check cannot hold. **Recommended:** a port-check
  script, `docs/extraction/compare_ported_tests.py`. Per module it requires SGK's set of
  `Class.test_name`, and per function that asserts, SGK's sequence of assertion calls, arguments
  ignored. Every other change is listed per test in the log by kind. `compare_with_source.py`
  accounts for these files as `PORTED`. **Rejected:** review by reading alone, under which "keeps
  its assertions" rests on reading 156 tests by eye.
- **U10: split 03. (taken 2026-10-07, as recommended)** 03's 129 tests are 4,580 lines in eight
  modules, and run as 156, since `test_one_timestamp_per_write` re-runs 27 inherited tests.
  **Recommended:** two prompts, each landed and reviewed on its own. 03a takes the replicated
  write, the check at open and the prune at open (76), with the two issues assigned to 03. 03b
  takes the rest (53 defined, 80 run) after 03a, since `test_one_timestamp_per_write` subclasses
  03a's modules. **Rejected:** one prompt, as first planned: a long run and a large diff to review.
- **U11: `test_read_only_pool`'s SGK probe. (taken 2026-10-07, as recommended)** The module
  imports SGK's `docs/a3-v2-readiness/reader_writes_probe.py` to build its store and replay SGK's
  QSI lookup sequence, and one test asserts the outcomes SGK's audit recorded.
  **Recommended:** 03b builds on `build_store` and writes a short neutral lookup sequence over
  the client's classes. The test keeps its name and assertions: a read-only run changes no file,
  and its outcomes equal the read-write run's. The SGK-specific outcome strings become neutral
  ones (R-count). **Rejected:** leaving that one test in SGK, which loses the only test that runs
  a whole reader sequence.
- **U12: test names that are client table names. (taken 2026-10-07, as recommended)** Four test
  names in `test_read_only_pool` are SGK table names (`test_LambdaCDM`, `test_QCD_Cosmology`,
  `test_tolerance`, `test_GkSourcePolicy`). **Recommended:** a name holding a client's table
  identifier changes by the table map only, as U8 did for strings. The log lists each with its SGK
  origin, and 04's guard needs no exemption. **Rejected:** keeping the names and exempting them
  from 04's guard.
- **U13: the roles the neutral client lacks for 03b. (taken 2026-10-07, as recommended)** 03b's
  planner found two roles that no class of 02's client can play.
  - `test_version_row_at_open` needs a replicated class with a `version` column that a get
    inserts, as SGK's `GkSourcePolicy` is. The client's versioned replicated classes,
    `keypoint_alias` and `Gadget`, are written by `object_store`, and play other roles in the same
    test.
  - `test_read_only_pool` needs four different get-inserted replicated classes for U12's four
    test names. The two frames are fixed by `build_store`, and `keypoint` cannot be deleted for a
    miss test. So `tolerance` and `GkSourcePolicy` have no class.

  **Recommended:** 03b adds two replicated classes to the client by addition: `gauge_setting`
  (unversioned) and `routing_rule` (versioned, labelled). `build_store` writes both. 02's tests
  change only in their measured literals. 03a's tests pass unchanged. **Rejected:**
  - a separate prompt to extend the client first, which adds a prompt and a review for a change
    03b alone uses;
  - leaving those tests in SGK, which drops most of `test_read_only_pool`, against U11.

- **U14: splitting 04. (taken 2026-10-08, as recommended)** 04's planner measured 175 tests in
  4,837 lines, and two fixtures of 1,561 lines, one of which (`real_store_fixtures`, 1,350 lines)
  must be rebuilt with neutral row data. That is more than 03a and 03b together. **Recommended:**
  two prompts. 04a ports the fixtures, captures the schema witness, extends the client (U15) and
  ports the five modules that build stores: `test_store_inventory`, `test_store_schema`,
  `test_store_reader`, `test_foreign_key_check` and `test_schema_builder` (85 tests). The fixture's
  rows are designed with `test_store_inventory`, which addresses them. 04b ports the other five
  (90 tests), the guard among them. **Rejected:**
  - three prompts (the fixture and the four small modules; `test_store_inventory` alone; the
    rest), which designs the fixture's rows before their main consumer is ported;
  - one prompt, the largest unit of work by far, and the hardest to review or revert.
- **U15: the roles the neutral client lacks for 04. (taken 2026-10-08, as recommended)** 04's
  planner found roles no class of the client can play: a second factory referencing the
  polymorphic frame parent through the same type map; a sharded class with a value table; a
  tagged sharded class with no validated column, one record and no dependents; a parent-set member
  table with serials and nullable members; and a sharded tagged parent of a sharded child. Also,
  SGK's `TestRevalidate` asserts the warning SGK's factory prints when a model does not validate,
  and the neutral `Gadget_factory` prints none. **Recommended:** 04a adds a small sharded family to
  the client by addition (`Trace`, with its tag and value tables, and `Weave`, with its tag and
  member tables), written by `build_store`, and `Gadget_factory`'s validate prints a warning when
  a Gadget does not validate. 02's and 03's tests change only in measured literals. **Rejected:**
  - weakening the ports: about ten tests would loop over one class, count zero, or assert what
    holds vacuously;
  - leaving those tests in SGK, against rule 6.
- **U16: the test about SGK's report. (taken 2026-10-08, as recommended)**
  `test_inventory_declarations.TestResolve.test_the_report_renders_both_cosmology_types` asserts
  on SGK's `tools.inventory_report`, which stays in SGK (§1). **Recommended:** it is not ported.
  04b records it in its log with the reason, and `compare_ported_tests.py` gains a `NOT_PORTED`
  list (test and reason), so that the omission is declared and checked. 04b adds 25 of that
  module's 26. **Rejected:** a neutral report formatter in the test client, written only to keep
  one test.
- **U17: the guard and the layer's frozen prose. (taken 2026-10-08, as recommended)** A guard
  built from the three clients' vocabulary finds one hit in the layer at `2992945`: the comment
  `e.g. "wavenumber"` at `datastorekit/tools/shard_key_audit.py:188`, which rule 8 freezes until
  after 05. **Recommended:** the guard holds an exact list of known hits (file, line, word, and
  reason), and fails if the hits differ from it in either direction. The list is emptied when the
  prose is rewritten after 05, under `[01-package-prose-names-sgks-layout]`. **Rejected:**
  - adding the comment scan only once rule 8 lifts;
  - rewriting the comment in 04b as an exception to rule 8.
- **U18: the neutral `Sample`'s validated flag in the inventory. (taken 2026-10-08, as
  recommended)** 04a's orchestrator found that
  `test_store_inventory.TestTheFullStore.test_classes_with_tags_validated_and_values` requires, of
  every record of every class, a validated flag and a value count, or neither, as every SGK class
  has. The neutral `Sample` declares `validated` in its `inventory_spec` and has no value table,
  so its records carry a flag and no count. No literal makes the test pass with `Sample` in the
  store (measured on `build_store` at `86640bf`). **Recommended:** 04a deletes `validated` from
  `Sample`'s `inventory_spec`. `Trace` (U15) is then the sharded class whose flag the inventory
  reads, and `Sample` plays SGK's `QuadSourceIntegral` in that test: tagged, with no flag and no
  values. Its column, `validate_on_startup` and the prune are unchanged. Probed: of the 268 tests,
  only `test_neutral_client`'s expected Sample flags change (to `None`), and the contract's
  inventory `validated` row names `Gadget` and `Trace`. **Rejected:**
  - a value table for `Sample`, a seventh new table whose ripple reaches `build_store`, the drop
    groups and the sharded prune;
  - leaving the test in SGK, as U16 does for the report test, which drops the one test of that
    rule.
- **U19: a drop list of 03a's that the new client outgrows. (taken 2026-10-08, as recommended)**
  04a's agent stopped at step 1 (prompt §5, third condition). `Weave` names a `Tessera`, as a
  declared parent (`anchor`) and by `Weave_members`' foreign key (U15, hazard 8), so the layer
  refuses to drop `aliases` and `tesserae` without the `traces` tables
  (`ShardedPool._refuse_drop_that_leaves_references`). 03a's
  `test_reconcile_at_open.TestPruningAfterRepair.test_an_interrupted_store` drops
  `tables_to_drop(["samples", "aliases", "tesserae"])` (`:1108-1114`), "aliases' dependents", and
  errors on both subtests, as does 03b's inheritor in `test_one_timestamp_per_write`: 4 errors.
  **Recommended:** 04a adds `"traces"` to that one list, as R-count (a list of dependents measured
  over the registry), and its docstring's list may say so. No assertion changes. Probed by the
  agent: the two modules give `Ran 69 tests … OK`. **Rejected:**
  - pointing `Weave`'s `anchor` at another class, against §2.2's map and hazard 8;
  - putting `Weave`'s tables in the `tesserae` group, against U15's `traces` group of six.
- **U20: the schema witness and a class with no table. (taken 2026-10-08, as recommended)** 04a's
  agent stopped a second time (prompt §5, fourth condition) on `test_schema_builder`. The client's
  `ephemeral_probe` registers `None`, which no SGK class does. The actor's record of it carries
  `"insert": None` and `build_schema`'s does not, so no one witness matches both descriptions,
  and `test_actor_adds_only_the_inserters` raises `KeyError`, since the actor makes no inserter for
  a class with no table. Both shapes are the layer's, pinned by `TestNoneRegistration`.
  **Recommended:** `test_schema_builder` and `schema_description.actor_with_built_schema` use the
  registry less the classes whose `register()` is `None`, the filter 03a applied to `REPLICATED`,
  and the witness (never committed) is captured again, twice, from it. No assertion changes;
  `TestNoneRegistration` keeps the `None` case. Probed by the agent in a scratch copy: 7 OK.
  **Rejected:** removing `ephemeral_probe` from the client, which loses 02's coverage of a `None`
  registration; and leaving the three tests in SGK.
- **U21: `test_schema_builder`'s witness history. (taken 2026-10-08, as recommended)** Its module
  docstring is SGK's history of SGK's witnesses: it names SGK tables on 12 lines, against §3.5's
  grep, and calls `schema_at_datastore-generic-07.json` the current witness, which is false here.
  **Recommended:** 04a rewrites that run, from "The current one is …" to the end of the history,
  to name `schema_at_extraction-04a.json` as the current witness and to say that SGK's earlier
  witnesses are SGK's history and are not copied (§2.5); the rest of the docstring is ported
  unchanged. **Rejected:** removing only the table names, which keeps a false sentence; and
  mapping them by the table map, which describes changes the neutral client never had.
- **U22: the declared facts and a class with no table. (taken 2026-10-08, as recommended)** 04b's
  agent stopped (prompt §5, first condition) on two tests of `test_declared_facts.TestTheRecords`:
  `test_every_record_of_a_class_with_a_table_carries_the_three_keys` (`22 != 21`) and
  `test_exactly_the_four_declarations_are_not_default` (`KeyError: 'owner_column'`). Both call
  `build_schema` on the whole registry, and the client's `ephemeral_probe` registers `None`, so its
  record has no table and none of the three declared keys. No SGK class registers `None`. This is
  U20's case. **Recommended:** a module constant `WITH_A_TABLE`, the registry less the classes whose
  `register()` is `None` (U20's filter), is what those two `build_schema` calls are given (R-help);
  the other 23 tests keep the whole registry. No assertion, name or control flow changes, and
  `TestNoneRegistration` keeps the `None` case. Probed by the agent in a scratch copy: 25 OK. A
  module-wide filter was probed and fails: `TestTheVersionObject`'s read-only open is refused,
  since the store's `replicated_tables` still names `ephemeral_probe`. **Rejected:** removing
  `ephemeral_probe` from the client (rejected at U20); and declaring the two tests in
  `NOT_PORTED`, which drops the only pin on the declared keys of every record.
- **U23: how `v0.1.0` is reached. (taken 2026-10-09, as recommended)** CI runs only on GitHub,
  where `origin/main` is 26 commits behind, and rule 10 forbids moving a tag. **Recommended:** 05's
  agent verifies both ends locally and makes one commit, with no push and no tag. After the review
  the user pushes `main`, or approves the orchestrator's doing so. Once CI passes at both ends on
  05's commit, `v0.1.0` is made there, annotated, and pushed. If CI fails, a fix prompt lands
  first, and no tag is made on a commit whose CI is red. **Rejected:** the agent tagging in its own
  run, before CI, which would leave a broken `v0.1.0` that cannot be moved.
- **U24: measuring the high end locally. (taken 2026-10-09, as recommended)** The package had never
  run on Python 3.13, Ray 2.5x or SQLAlchemy 2.0.46, and no wheel of them was cached.
  **Recommended:** a throwaway Python 3.13 venv built by `uv` from PyPI with those pins, outside the
  repository, for the planner and for 05's agent. 05 may download PyPI packages into the
  scratchpad, and nothing else. **Rejected:** borrowing SI's venv, which has exactly those versions
  but is a client's environment (§5 rule 5); and leaving the first high-end run to CI.
- **U25: the neutral client's keyed class. (taken 2026-10-09, as recommended)** 02's coverage
  rule (`test_neutral_client.TestCoverageByDeclaration`) requires a factory of the shared client
  to declare every `register()` key the schema builder reads, in both directions, so a test-local
  registry cannot cover `key_on_version`. **Recommended:** the existing `Tessera` (sharded,
  versioned) declares it, and its `build` filters on the serial. Probed by the planner at
  `fe040b2`, with the keying and U26 in a scratch copy: of the 444, only the two witness tests and
  `REGISTER_KEYS`'s test move. **Rejected:** a new keyed class, which moved 16 tests in 6 modules
  (drop groups, round trip, witness) before `build_store` wrote any of its rows.
- **U26: keyed lookups on a read-only pool. (taken 2026-10-09, as recommended)** A read-only
  actor is never given the version serial, as a third guard against inserts (`SQL/Datastore.py`'s
  read-only comment), so it could not key a lookup. **Recommended:** an actor holds a lookup serial
  apart from its insert serial; `set_version` sets both, and a read-only pool calls a new
  `set_lookup_version`, which sets the lookup serial only. All three guards stay. Probed: the
  read-only tests pass, and a keyed `Tessera` is found under its own label read-only.
  **Rejected:** `set_version` on read-only actors too, which drops the third guard; and refusing
  keyed lookups read-only, which changes what a ported read-only test raises.
- **U27: the equivalence check after rule 8 lifts. (taken 2026-10-09)** 06 is the first prompt to
  change the layer, which `compare_with_source.py` compares line by line with SGK. **Recommended
  at writing:** a declared kind for files amended after `v0.1.0`, checked through the tag.
  **Taken instead:** the check is retired at `v0.1.0`. 06 runs it once more, before its change, and
  records that it describes the tagged tree; `compare_ported_tests.py` still runs.
- **U28: how `v0.2.0` is reached. (taken 2026-10-09, as recommended)** As `v0.1.0` was (U23): 06
  makes no tag and pushes nothing; after its review its commit is pushed alone as `main`, and
  `v0.2.0` is made there, annotated, only once CI passes at both ends, each step with the user's
  approval. **Rejected:** the agent tagging in its own run, before CI.
- **U29: the release SGK adopts. (taken 2026-10-09, by the user)** SGK adopts **`v0.2.0`**
  directly, not `v0.1.0`. The two differ only behind `key_on_version`, which no SGK factory
  declares, and in nothing the layer writes, so G2's rehearsal fingerprint is unaffected. G2 now
  reads `v0.2.0`. **Rejected:** `v0.1.0` first, which would make SGK move its pin twice.
  *(Amended 2026-10-09 by U37: every client, SGK included, adopts `v0.2.1`.)*
- **U30: splitting 07. (taken 2026-10-09, as recommended)** The checklists need three client
  repositories measured, read-only and exactly; the verification document and the close-out need
  only this repository. **Recommended:** 07a writes `docs/adoption/`; 07b, after 07a is reviewed,
  writes the verification document and closes the campaign. **Rejected:** one prompt, a long run
  and a large review.
- **U31: SI's stores. (taken 2026-10-09, as recommended)** The package refuses every SI store at
  open (no `replication_in_flight`, absolute shard records, one timestamp per shard on replicated
  rows), as it refuses CPBH's. **Recommended:** as D4, SI's stores are rebuilt, not migrated. SI's
  checklist advises SI to adopt at the start of its P2 campaign, which re-runs the June grids, and
  to tag its last commit on the old layer first, so that its kept stores stay readable from that
  checkout. **Rejected:** a migration tool here, a unit of work for stores that SI is re-running
  anyway; and leaving the checklist silent on it.
- **U32: clients that register factory instances. (taken 2026-10-09, as recommended)** CPBH and SI
  register instances, and `SQLAFactoryBase` is an ABC, so each of their factory classes that defines
  only `register` and `build` raises `TypeError` when instantiated: 20 classes over 24 registry
  entries in CPBH, 16 over 18 in SI. *(Corrected at 07a's review from "16" for both, which mixed
  SI's class count with CPBH's entry count; measured by 07a's orchestrator and agent.)*
  **Recommended:** a client-side change, which the checklists list class by class: define `store`,
  `validate` and `validate_on_startup`, or register the class. *(07a found that every hook of every
  CPBH and SI factory takes `self`, and the quantity factories hold `ObjectType` on the instance, so
  registering the class works only once its hooks can be called without an instance; the checklists
  state both routes.)* The package is unchanged. **Rejected:** making those hooks defaulted in a
  release before CPBH adopts, which changes the contract that SGK's factories and the neutral client
  satisfy, for a fix a client makes in a few lines.
- **U33: the open issues at close. (taken 2026-10-09, by the user)** When 07b was to be written,
  the board held four issues open on this repository:
  `[01-package-prose-names-sgks-layout]`, `[02-an-unsupplied-sharded-table-raises-keyerror]`,
  `[05-a-refused-open-leaves-its-engines-undisposed]` and
  `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]`. **Recommended at the time:**
  close with them open and unassigned, as SGK's closed campaigns left theirs. **Taken instead:**
  fix all four before the campaign closes, and cut a release, which the clients adopt in place of
  `v0.2.0`. 07b is withdrawn unwritten. The four inherited issues of `docs/OPEN_ISSUES.md` §1.2 stay
  out of scope. **Also offered:** seeding a follow-up campaign for the four.
- **U34: the contract's §8 citation. (taken 2026-10-09, as recommended)** 07a's review found that
  `docs/client-contract.md` §8 cites the read-only pool's `set_lookup_version` calls as
  `SQL/ShardedPool.py:567-574`; at `v0.2.0` they are `:568-575`. **Recommended:** the close-out
  prompt corrects it in place, with a dated correction note in §8, and the verification document
  records it. It was wrong when written, so this is a correction, not a superseded measurement
  (`CLAUDE.md` rule 6). Prompts 08a–10 may move these lines again, so the close-out cites the tree
  it verifies. **Rejected:** a §3 issue left for a later campaign.
- **U35: how the fixes are split. (taken 2026-10-09, as recommended)** **Recommended:** 08a the two
  small fixes (the bare `KeyError`; the vectorized get's in-place update); 08b the engine disposal
  alone, since it touches the pool's and actors' open and refusal paths; 09 the prose rewrite; 10
  the release with the adoption addenda; 11 the verification and close-out. Each landed and
  reviewed on its own. **Rejected:** one prompt for the three code fixes, which puts the disposal's
  risk in the same diff as two one-line fixes; and one prompt for all four issues, the hardest to
  review or revert.
- **U36: the fix release's version. (taken 2026-10-09, as recommended)** **Recommended:**
  **`v0.2.1`**. The fixes add no API and change nothing the layer writes; a refused open still
  refuses, with a `RuntimeError` where it raised a `KeyError`. **Rejected:** `v0.3.0`, treating the
  changed exception type and the no-longer-updated payloads as a change of behaviour.
- **U37: how the clients and the checklists follow. (taken 2026-10-09, as recommended)** This
  amends U29 and G2–G4: all three clients adopt `v0.2.1`. **Recommended:** 10 adds a dated section
  to `docs/adoption/README.md` and to each checklist, giving the new pin and what changed since
  `v0.2.0`, for example CPBH's and SI's vectorized-payload hazard gone. 07a's measurements stay as
  written (`CLAUDE.md` rule 6). **Rejected:** re-measuring all three clients against `v0.2.1` in a
  prompt of its own, a 07a-sized run for a release that changes no call a client makes.
- **U38: what the prose rewrite covers. (taken 2026-10-10, as recommended)** At 09's writing the
  board's pattern (log 03a §8) still found 155 comment and docstring lines in 40 files, as at 04b.
  It misses the source's campaign names without a `prompts/` prefix, `var/`, the source's commits
  (`b04671f`, `a2bd966`, `e53f323`), and bare citations of the source's records ("(prompt 03)"
  meaning its `a3-v2-readiness` prompt 03, "audit §4.1", "README U1", "QSI"), which only reading
  finds. No runtime string names the source. **Recommended:** every comment and docstring that
  points at the source's layout, campaigns, logs, audits, issues, commits or `var/`: 248 lines in
  42 files at `452b3c9`, 57 of them found by reading. The import commit's provenance, generic
  mentions of "the source repository", and this repository's own citations stay. **Rejected:** the
  155 only, which leaves "(prompt 03)" reading as this campaign's prompt, the source's SHAs, and
  "nothing under `var/`" in place.
- **U39: what a citation of the source becomes. (taken 2026-10-10, as recommended)**
  **Recommended:** the citation is removed, and the sentence it supported stays and is made true
  for this package (a source path becomes the package's module, a tool is run as
  `python -m datastorekit.tools.<name>`, the removed `sys.path` bootstrap is no longer described).
  `PROVENANCE.md` records the source and the import commit, so the history stays reachable.
  **Rejected:** rewriting each as an attribution ("the source repository's `a3-v2-readiness`
  prompt 03"), which keeps per-line traceability into SGK but leaves its campaign names in the
  package, and would need an allow list in any guard.
- **U40: a guard on the prose. (taken 2026-10-10, as recommended)** **Recommended:** 09 adds a test
  module, `test_prose_names_no_source`, that reads every comment and docstring under
  `datastorekit/`, the layer and its tests, and fails on a path of the source's layout that does
  not exist here, a dotted module of the source, its other names, its campaign names and `var/`,
  each failure naming `file:line`, with no allow list. The source's SHAs and bare citations stay a
  matter for review. `test_layer_is_generic`'s `KNOWN_HITS` is emptied, as U17 says.
  **Rejected:** no new test, which leaves nothing to stop a later prompt bringing such prose back;
  and widening `test_layer_is_generic`, which checks the layer, not the tests, for client
  vocabulary, and would change that module's scope and docstring.
- **U41: the package under real Ray. (taken 2026-10-10, as recommended)** No prompt had started
  Ray: the suite runs the actors through the in-process stand-in, so the package had never run as
  real Ray actors here. **Recommended:** 11's verification includes a smoke run under a local
  `ray.init()`, no cluster, at both version ends, by a script kept in `docs/extraction/` and never
  collected by the suite. It opens a `tempfile` store through the neutral client: write, reopen,
  read-only open, a keyed get and a refused open, and checks that no Ray process is left. A defect
  it finds is opened as an issue, not fixed in 11. **Rejected:** recording the real-Ray path as
  unverified, and leaving SGK's G2 rehearsal as its first measurement.
- **U42: the pin, as a client installs it. (taken 2026-10-10, as recommended)** Every prompt had
  been offline. **Recommended:** 11 installs `datastorekit @
  git+https://github.com/ds283/DatastoreKit@v0.2.1` from GitHub into a scratch venv, with Ray and
  SQLAlchemy from the offline cache and only the package fetched, compares it with 10's wheel, and
  runs it from outside the repository. **Rejected:** staying offline, and relying on 10's wheel and
  the CI run on `33778b0`.

## 7. Gates outside this repository

| Gate | Holds when | Needed by |
|---|---|---|
| **G1** | SGK's `datastore-generic-followup` has closed: its prompt 03 landed and was reviewed. The commit that closes it is the **import commit**. SGK's tree is clean at it, and SGK's suites pass there. **Holds (2026-10-07):** 03 landed as `086c81a` and its review `6f7f291` closed the campaign, so the import commit is **`6f7f291`**. The next commit, `99456d8`, adds only a `.tex` status note. | 01 |
| **G2** | SGK has adopted `v0.2.1` (U37; it was `v0.1.0` until U29, then `v0.2.0`, both 2026-10-09) in a campaign of its own: its 15 layer files and two tools are deleted, it imports `datastorekit` at a pinned tag, its remaining suites pass, and a rehearsal rebuild through the package reproduces its reference fingerprint (run by a person, under SGK's rules). | CPBH's adoption; the end of U3's freeze |
| **G3** | CPBH has adopted `v0.2.1` (U37) in a campaign of its own (07a's checklist and 10's addendum; its stores rebuilt, D4). | — |
| **G4** | SI has adopted `v0.2.1` (U37), when it is next active (07a's checklist and 10's addendum; its stores rebuilt, U31). | — |

The campaign closes at 11 (U33; it was 07b). G2–G4 are recorded on this board as they hold, but this campaign does
not wait for them.

*(2026-10-10, prompt 11: the campaign closed at 11, with G2–G4 open. Each is recorded on the board when it
holds, in a records commit of its own.)*

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
