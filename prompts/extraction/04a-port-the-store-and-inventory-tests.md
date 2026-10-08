# Prompt 04a — port the store and inventory tests

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 03b landed (`0d5380c`), and its review was recorded (`2992945`).
- U14–U17 are taken (README §6.2, 2026-10-08):
  - U14 split 04 into this prompt and 04b;
  - U15 adds a small sharded family to the neutral client (§2.3);
  - U16 and U17 are 04b's.
- `git status` is clean in this repository.

**Closes:** nothing. **Narrows:** nothing. **Changes:** `[01-package-prose-names-sgks-layout]`,
whose count grows by the ported modules' prose (§2.8). **Opens:** only what the work finds.

**Recommended model:** **Opus.** This is the campaign's largest prompt.
- Four of the five modules port much as 03a's did.
- The fifth, `test_store_inventory` (42 tests, 1,090 lines), asserts about 200 measured facts of
  SGK's hand-built store. Its fixture, `real_store_fixtures` (1,350 lines), is ported here with
  neutral row data that this prompt designs. The row data and the test's data tables are designed
  together.
- The neutral client gains six tables (§2.3).

**Read first:**

1. [`README.md`](README.md): §0.2, §2 (rows 04a and 04b), §4, §5 (rules 6–9 especially) and §6.2
   (U8–U17).
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`.
3. The board, with the reviews of 02, 03a and 03b. Then:
   - [`logs/02-the-neutral-test-client.md`](logs/02-the-neutral-test-client.md) §1.1–§1.4;
   - [`logs/03a-port-the-replicated-write-tests.md`](logs/03a-port-the-replicated-write-tests.md)
     §1, §2, §7 and §8;
   - [`logs/03b-port-the-open-and-read-only-tests.md`](logs/03b-port-the-open-and-read-only-tests.md)
     §1.4–§1.6, §2 and §3.
4. The package as 03b left it:
   - `datastorekit/tests/client/` (all of it) and `datastorekit/tests/standin_pool.py`;
   - `datastorekit/tests/shard_store_fixtures.py`, and `test_neutral_client.py`;
   - one of 03b's ported modules, for the form of a port;
   - `datastorekit/store_inventory.py`, `datastorekit/SQL/schema.py` and
     `datastorekit/store_reader.py`;
   - `docs/client-contract.md`, `docs/extraction/compare_ported_tests.py` and
     `docs/extraction/compare_with_source.py`.
5. In SGK at `6f7f291`, **read with `git -C /Users/ds283/Documents/Code/SecondaryGWKit show
   6f7f291:<path>`**, never from SGK's working tree:
   - the five modules, under `Datastore/tests/`: `test_store_inventory.py`,
     `test_store_schema.py`, `test_store_reader.py`, `test_foreign_key_check.py` and
     `test_schema_builder.py`;
   - the two fixtures, `Datastore/tests/real_store_fixtures.py` and
     `Datastore/tests/schema_description.py`;
   - `Datastore/tests/data/schema_at_datastore-generic-07.json`, for its form only;
   - for the roles the new classes play: `Datastore/SQL/ObjectFactories/TkNumericIntegration.py`,
     `GkSource.py`, `OneLoopIntegral.py`, `QuadSourceIntegral.py` and `BackgroundModel.py` (its
     warning at `:752`).

Line numbers below are at `2992945` for the package, and at `6f7f291` for SGK.

---

## 1. What is wanted

U14 gave 04a these five modules of §0.2's 175:

| SGK module | Lines | Tests (defined = run) | Per class |
|---|---|---|---|
| `test_store_inventory` | 1,090 | 42 | 6, 3, 2, 2, 6, 5, 3, 4, 5, 4, 2 |
| `test_store_schema` | 492 | 13 | 3, 1, 1, 3, 4, 1 |
| `test_store_reader` | 375 | 15 | 5, 2, 2, 5, 1 |
| `test_foreign_key_check` | 291 | 8 | 5, 2, 1 |
| `test_schema_builder` | 180 | 7 | 5, 2 |
| **total** | 2,428 | **85** | |

These were counted by `ast` at `6f7f291`, with inheritance resolved. No class inherits a test
from another module.

It also takes the two fixtures they import:
- `real_store_fixtures` (1,350 lines) builds a real store on disk by hand, with fixed serials;
- `schema_description` (211 lines) describes the schema the actor builds, compared with a
  witness file.

After this prompt:
- the five modules run in `datastorekit/tests/` under their SGK names, on the neutral client and
  a neutral hand-built store. Each test keeps its SGK class and method name, and its assertions;
- `datastorekit/tests/real_store_fixtures.py` and `datastorekit/tests/schema_description.py` keep
  SGK's public names and signatures. The first holds neutral row data (§2.4);
- `datastorekit/tests/data/schema_at_extraction-04a.json` is the neutral schema witness (§2.5);
- the neutral client has the six tables of §2.3 (U15), and `Gadget`'s validate prints a warning
  when a Gadget does not validate;
- `compare_ported_tests.py` checks fifteen modules, and `compare_with_source.py` accounts for each
  as `PORTED`;
- the suite is **353**: 268 + 85.

**No behaviour of the layer changes.** No file under `datastorekit/` outside `tests/` is touched
(README §5 rule 8). If a ported test fails on the neutral client, and passing it would need a
change to the layer, that is a stop (§5).

---

## 2. What to change

### 2.1 What re-fixturing may change

03a §2.1 governs unchanged: the kinds R-imp, R-map, R-help, R-value, R-count and R-name, and
nothing else. Read it there. Four points are particular to 04a.

- **R-name applies to no test.** No test or class name in the five modules holds one of log 02
  §1.2's 82 client names as a word or as an underscore part. The one that seems to,
  `TestTags.test_a_tag_no_row_carries_is_only_a_store_tag`, names `store_tag`, which is the
  layer's.
  - Some names hold SGK vocabulary that is not a table name: `test_log10_tol_is_used_as_stored`,
    `test_the_last_bit_of_k_changes_the_records`, `test_oneloop_tags_come_from_its_own_table`,
    `test_an_unknown_cosmology_type`, `test_a_dangling_tq_is_reported`,
    `test_a_dangling_exit_time_in_the_policy_data_is_reported`, and the constants
    `ADDED_QUADSOURCE_SERIAL`, `ADDED_TQ_SERIAL` and `GK_SOURCE_TABLES`.
  - **They keep their names.** `NAME_MAP` gains nothing.
- **R-imp covers paths and code in strings.** Three places name SGK's layout:
  - `REPO_ROOT / "Datastore" / "store_inventory.py"` (`test_store_inventory.py:593`);
  - the child processes' code strings and their `PYTHONPATH` (`test_store_inventory.py:1069-1070`,
    `test_store_reader.py:337-338`, whose string imports `config.datastore`);
  - `FACTORIES` (`test_store_inventory.py:81`), which globs SGK's factory directory. In the port
    it names the client's `factories.py`, as R-help.
- **`test_store_inventory`'s data tables are R-count as a whole.** They are:
  - `INVENTORY_CLASSES` (`:56-78`);
  - `VALUE_TABLES` (`:83-91`);
  - `IDENTITY` (`:95-261`, 93 entries);
  - `NON_IDENTITY` (`:264-311`, 39 entries).

  Each is re-derived from the neutral fixture and measured, not translated entry by entry. The
  log states the rule each table follows, and its count before and after.
  - `IDENTITY` still names, for every inventory class, every identity field (leaf, key parent,
    parent-set member and tag), each with a row to vary it to.
  - `NON_IDENTITY` names every non-identity column the neutral classes have.

  SGK has three categories of non-identity column the client lacks: non-identity labels, solver
  serials and descriptive names (18 entries). Each is listed in the log as absent, not invented.
- **The fixtures are R-help modules.** They keep every public name and signature, and their
  mechanics are transcribed. Their row data is new (§2.4).

### 2.2 The map

By role. Where a row says "by role", choose per site, and the log's map as used says which.

| SGK | What the tests use it for | Neutral |
|---|---|---|
| `wavenumber` (`k_inv_Mpc`; flags `is_source`, `is_response`) | the shard key; a float identity; OR-flags | `keypoint` (`kp_position`; `kp_marked`, `kp_flagged`) |
| `redshift` | a second flagged leaf | `keypoint`. No second flagged class exists. A site that needs two distinct flagged classes is listed in the log |
| `tolerance` (`log10_tol`) | a replicated leaf with a float identity, three rows, and no dependents | **`routing_rule`** (`rule_threshold`) |
| `LambdaCDM`, `QCD_Cosmology` | the polymorphic parent's two types | `dial_setting` (kind 1), `knob_setting` (kind 2), through `FRAME_TYPES` |
| `cosmology_type`, `cosmology_serial` | the type column and the reference | `frame_kind`, `frame_serial` |
| `IntegrationSolver`, `GkSourcePolicy`, `QuadSourcePolicy` | replicated leaves, labelled or stepped | `dial_setting`, `knob_setting`, `gauge_setting`, `routing_rule`, by role |
| `wavenumber_exit_time` | the shard key's proxy; stepping; a polymorphic referrer | `keypoint_alias` as the proxy; **`Trace`** as the referrer |
| `BackgroundModel` (+`_tags`, `Value`) | replicated, tagged, validated, with values and a polymorphic parent | `Gadget` (+`Gadget_tags`, `GadgetPart`) |
| `TkNumericIntegration` (+`_tags`, `Value`), and the sharded classes like it | sharded, tagged, validated, with values | **`Trace`** (+`Trace_tags`, `TraceStep`) |
| `GkSource` | a sharded tagged parent of a sharded child, with a parent set | `Trace` as the parent; `Weave` as the child |
| `GkSource_parents` | member rows, with serials and nullable members | **`Weave_members`** |
| `GkWKBIntegration.numeric` | a nullable key parent | `Weave.anchor`; also `Sample.anchor` |
| `OneLoopIntegral` (+`_tags`) | tagged, no validated column, one record, no dependents, sharing serial 1 with another tagged class | **`Weave`** (+`Weave_tags`) |
| `QuadSource`, `QuadSourceIntegral` | cross-shard references; many parents; tagged and not validated | `Sample` (`anchor`, cross-shard) and `Weave`, by role |
| `GkSourcePolicyData` (FK to the proxy), `QuadSource.Tq_serial` (`test_foreign_key_check`) | a sharded-to-replicated foreign key; a same-shard foreign key between sharded tables | `Tessera.alias_serial` → `keypoint_alias`; `Sample_members.tessera_serial` → `Tessera` |
| `Run_fixture` | the tag every tagged record carries | a neutral label of the fixture's (§2.4) |
| `config.datastore.factories`, `config.sharding.*` | the registry | `registry.factories`, `registry.*` |
| `sp.make_units`, `StandinCosmology`, `get_tolerance`, `get_wavenumber`, `make_exit_time`, `make_policy_data` (`test_foreign_key_check`) | a stand-in store | 03's map: `build.get_rule` (or `get_gauge`), `get_keypoint`, `make_alias`, `make_sample_on` |

`version` and `store_tag` are the layer's, and keep their names.

**This map differs from 03b's in one row.** `tolerance` maps to `routing_rule` here, because
04a's tests need its float (`log10_tol` -5, -7, -9 at `test_store_inventory.py:566`, `:580`), and
`gauge_exponent` is an integer. A site that needs only "a replicated leaf with no dependents" may
use `gauge_setting`, and the log says where.

**Hazards the planner saw.** Check each, and say in the log what you found.
1. **`build.build_store` cannot stand for SGK's fixture.** Log 02's role table maps
   `build_full_store` to `build.build_store`. That holds for at most four of 04's ten modules, and
   none of 04a's five that use the fixture. Measured:
   - `build_store`'s timestamps are wall-clock, which breaks `earliest_timestamp` (`:442-445`) and
     `test_timestamps` (`:527`);
   - its serials are leased, and vary with the shard count: `dial_setting` came out 501 at 2
     shards and 2 at 3;
   - it has no `replicated=`, `sharded=`, `shard_keys=`, `missing_*` or `extra_sql` parameter, and
     no `shard_files` or `directory`.

   **So:** every test that SGK built with `real_store_fixtures` uses the ported fixture. Only
   `TestStandinStore` (`test_foreign_key_check.py:209-283`) keeps the pool, as in SGK.
2. **A copied record with a parent set.** A `Sample` or `Weave` copied without its member rows is
   reported as `empty-parent-set`, not `duplicate`, and is dropped. That would break
   `TestDuplicates.test_on_one_shard`, `test_across_shards` and
   `test_other_tags_are_not_a_duplicate`. So the duplicate helpers copy the member rows too, and
   a copy across shards also copies the member rows' targets (R-help).
3. **Validated if and only if it has values** (`:408-413`). In the neutral client, `Sample` is
   validated and has no value table, so `Sample` cannot take that role there. `Gadget` and
   `Trace` have both.
4. **A common tag** (`:406`). Every tagged record of the full store carries the fixture's run
   tag, and one tag is carried by no row (SGK's `unused-tag`).
5. **Divergence spreads through dependents.** If one shard changes a replicated class that has
   dependents (`keypoint`, `dial_setting`, `knob_setting`, `Gadget`), its dependents diverge too.
   Then `set(problems) == {"tolerance"}` (`:821`) cannot hold. The divergence tests use
   `routing_rule` or `gauge_setting`.
6. **SQLite's `DROP COLUMN` refuses an indexed column or one with a foreign key.** So
   `missing_columns` names a plain column, such as `Sample.member_count`, `Trace.step_count` or
   `Tessera.tessera_weight`. SGK's `TkNumericIntegration.stop_Tprime` (`test_store_schema.py:152`,
   `:236`, `:341`) becomes one of these.
7. **Counts must agree.** Each hand-built row's `part_count`, `member_count` and `step_count`
   equals its number of part, member or step rows. Otherwise validate and revalidate disagree with
   the store.
8. **`references()` and `relabel_serials` follow the neutral references.** These are:
   - the undeclared `Sample.anchor_serial` → `Tessera`;
   - `Weave.anchor_serial` → `Tessera`;
   - the polymorphic `frame_serial`, through `frame_kind`;
   - shard keys, remapped through `mapping["keypoint"]`.

   `Sample_members` has no serial, so its rows are relabelled through their references only.
9. **`TestFloats.test_only_canonical_formats_a_float`** (`:589`) counts `def inventory_spec` in
   the factories, and compares the count with `len(INVENTORY_CLASSES)`. The client's
   `_label_factory` serves both `version` and `store_tag`, so its count is one less: 10
   definitions for 11 classes at `2992945`, and 12 for 13 after §2.3. The expected count becomes
   the measured number (R-count), and the log says why.
10. **`TestStandinStore`, measured at `2992945`.**
    - `build.make_sample_on(alias, gadget_serial=1)` on a pool leaves exactly one violation,
      `('Sample', 1, 'Gadget')`, on the shard that holds it. That rowid 1 rests on the first
      `Sample` lease being serial 1, with the controller pinned to the second shard. Shard ids
      iterate 2, 0, 1.
    - The sharded row names `keypoint`, not the proxy, so the test's `exit_rows` reads `keypoint`.
      It is a partial role, and the log says so.
11. **The ripple of §2.3 into 02's and 03's tests.** `build_store` writes the new classes, and
    `test_neutral_client.py`'s literals measure it (§2.3). 03b's `reader.build_full_store` calls
    `write_every_class`. No 03 test is expected to change. Run 03a's and 03b's modules after §2.3,
    before anything else depends on it.

### 2.3 The client additions (U15)

**Six tables, by addition.** They play the roles of §2.2's **bold** rows: `Trace`, `Trace_tags`,
`TraceStep`, `Weave`, `Weave_tags` and `Weave_members`. The names were checked: none occurs as a
word under `datastorekit/` or `docs/` at `2992945`, among log 02 §1.2's 82 names, or among the
three clients' column names.

- **`Trace`**, sharded on `"k"`. `register()` has `"version": True`, `"timestamp": True` and no
  `validate_on_startup`. Its columns:
  - `keypoint_serial` (foreign key to `keypoint.serial`, indexed, not null);
  - `frame_kind` (`Integer`, not null);
  - `frame_serial` (`Integer`, indexed, not null, with no foreign key: it is polymorphic);
  - `trace_label` (`String(DEFAULT_STRING_LENGTH)`, not null);
  - `step_count` (`Integer`, not null);
  - `trace_validated` (`Boolean`, default `False`, not null).

  `inventory_spec()`:
  - `leaves=("trace_label", "frame_kind")`;
  - `parents={"k": Parent("keypoint_serial", "keypoint"), "frame": Parent("frame_serial",
    type_column="frame_kind", types=FRAME_TYPES)}`. This is **the same `FRAME_TYPES` object**
    `Gadget` declares, which 04b's `test_both_referencing_factories_declare_the_one_map` checks
    with `assertIs`;
  - `tags=("Trace_tags", "trace_serial")`;
  - `values=("TraceStep", "trace_serial")`;
  - `validated="trace_validated"`.

  There is no `validate_on_startup`, so the pool's prune and 03a's prune tests do not see `Trace`.
- **`Trace_tags`**: as `Sample_tags`. `"serial": False`; `trace_serial` (foreign key to
  `Trace.serial`) and `TAG_SERIAL` are the primary key.
- **`TraceStep`**, `Trace`'s value table. It keeps the default `serial`, and has
  `"version": False` and `"timestamp": False`. Its columns are `trace_serial` (foreign key to
  `Trace.serial`, indexed, not null), `step_index` (`Integer`, not null) and `step_value`
  (`Float(64)`, not null). It declares no `owner_column`, which is replicated only.
- **`Weave`**, sharded on `"k"`. It has `"version": True` and `"timestamp": True`, no validated
  column and no value table. Its columns:
  - `keypoint_serial` (foreign key to `keypoint`, indexed, not null);
  - `trace_serial` (foreign key to `Trace.serial`, indexed, not null);
  - `anchor_serial` (`Integer`, indexed, nullable, with no foreign key, as `Sample`'s);
  - `weave_label` (`String(DEFAULT_STRING_LENGTH)`, not null).

  `inventory_spec()`:
  - `leaves=("weave_label",)`;
  - `parents={"k": Parent("keypoint_serial", "keypoint"), "trace": Parent("trace_serial",
    "Trace"), "anchor": Parent("anchor_serial", "Tessera", nullable=True)}`;
  - `tags=("Weave_tags", "weave_serial")`;
  - `parent_sets={"strands": ParentSet("Weave_members", "weave_serial", {"anchor":
    Parent("anchor_serial", "Tessera", nullable=True), "origin": Parent("origin_serial", "Trace",
    nullable=True)})}`. A member field shares its name, `anchor`, with a key parent, as SGK's
    `numeric` does (`test_inventory_declarations.py:375-418`, 04b's).
- **`Weave_tags`**: as `Trace_tags`, on `weave_serial`.
- **`Weave_members`**. It keeps the default `serial`, unlike `Sample_members`, so that `find_row`
  and `vary_row` can address a member row. It has `"version": False` and `"timestamp": False`.
  Its columns:
  - `weave_serial` (foreign key to `Weave.serial`, indexed, not null);
  - `anchor_serial` (foreign key to `Tessera.serial`, indexed, nullable);
  - `origin_serial` (foreign key to `Trace.serial`, indexed, nullable).
- **The factories.**
  - `Trace` and `Weave` have a sharded `build` that gets the stored object, or an unstored one,
    and inserts nothing, as `Sample`'s does.
  - Each has a `store` that writes the row, its tags, and its steps or member rows.
  - `Trace` has a `validate`: `step_count` equals the number of its step rows.
  - The tag, step and member tables' `build` raises `NotImplementedError`, as `Sample_tags`' does.
- **`Gadget_factory`'s one change.** When a Gadget does not validate, `_validate_row`
  (`factories.py:804`, which both `validate` and `revalidate` call) prints
  `!! WARNING: Gadget "<label>" did not validate after serialization (expected parts=<n>, number
  stored=<m>)`, after SGK's `BackgroundModel.py:752`. `TestRevalidate` (04b's) asserts the phrase
  `did not validate after serialization`. Nothing else in the factory changes.
- **The registry.**
  - `factories` gains the six after `Sample_members`.
  - `sharded_tables` gains `"Trace": "k"` and `"Weave": "k"`.
  - `replicated_tables`, `read_table_config`, `serial_batch_sizes` and `__all__` are unchanged.
  - A new drop group, `traces`, holds the six tables, in the order `dependent_tables` needs.
- **`build.py`.**
  - Helpers to make and store a `Trace` and a `Weave`.
  - `write_every_class` writes, through the pool:
    - two `Trace`s, on different keypoints, one on each frame kind, one validated, with tags and
      steps;
    - one `Weave`, with tags and member rows, one member with a `None` anchor.

    `build_store` then fills every table.

**What else follows, and nothing more:**
- `test_neutral_client.py` changes only in measured literals: `MEASURED_DEPENDENTS`, `counts`,
  and any other literal measured over the registry or `build_store`. `KEPT` does not change,
  since the new tables are in a group. Every other test of 02's passes unchanged; if one does
  not, stop.
- `docs/client-contract.md` changes only in its client columns: the counts, and the lists of
  classes by property.
- 03a's and 03b's modules are not edited. They pass unchanged. Run them, and say so.
- `objects.py`, `factories.py`, `registry.py` and `build.py` change by addition only, apart from
  the warning above and `write_every_class`.

### 2.4 The fixtures

**`datastorekit/tests/real_store_fixtures.py`**, ported from SGK's.
- **Every public name keeps its signature.** Measured at `6f7f291`:
  - `RowSet` (`:57`), `FIXED_TIMESTAMP` (`:59`) and `RealStore` (`:195`, with `primary`,
    `shard_files`, `replicated`, `sharded` and `.directory`);
  - `with_rows` (`:209`);
  - `build_real_store` (`:294`; `stem="fixture-store"`, `shards=2`, `replicated`, `sharded`,
    `shard_keys`, `missing_tables`, `missing_columns`, `extra_sql`);
  - `expected_row_counts` (`:354`), `independent_row_counts` (`:363`) and `file_state`
    (`:383`);
  - `fill_required` (`:1092`) and `full_rows` (`:1113`);
  - `build_full_store` (`:1188`; `stem="full-store"`, the same keywords);
  - `references` (`:1260`), `relabel_serials` (`:1277`), `find_row` (`:1326`) and `vary_row`
    (`:1341`);
  - the row-set constants `REPLICATED_ROWS`, `SHARDED_ROWS`, `SHARD_KEYS`,
    `FULL_REPLICATED_ROWS`, `FULL_SHARDED_ROWS` and `FULL_SHARD_KEYS`.
- **The mechanics are transcribed.** That is roughly `:194-411` and `:1067-1350`, after R-imp.
  - `_write_primary` writes through `shard_store_fixtures.bare_pool`, with
    `_ShardKeyType_name="keypoint"` and the registry's lists.
  - Rows go in with explicit serials. A `timestamp` a row leaves out is `FIXED_TIMESTAMP`.
  - Replicated rows go into every shard under the same serials.
- **`references()` is derived, not kept by hand.** It takes the schema's foreign keys, and every
  `inventory_spec`'s parents and parent-set members (`of`, or for a polymorphic one, `"frame"`).
  So SGK's `_UNDECLARED_REFERENCES` and `_COSMOLOGY_TABLES` (`:1246-1257`) have no counterpart.
  The log prints the derived map.
- **The default rows** (`REPLICATED_ROWS`, `SHARDED_ROWS`, `SHARD_KEYS`) are the small store
  `test_store_reader` and `test_store_schema` read. SGK's has a `TkNumericIntegration` with tags
  and values on each of shards 0 and 1. The neutral one has a `Trace` with `Trace_tags` and
  `TraceStep` rows there.
- **The full rows** (`FULL_*`) are designed with `test_store_inventory`, which addresses them.
  They hold:
  - fixed serials, at least two `version` rows, and every timestamp `FIXED_TIMESTAMP`;
  - at least one row of every inventory class (13 after §2.3), and rows in every table;
  - a run tag that every tagged record carries, and a tag that no row carries;
  - both frame kinds, each referenced by a `Gadget` and by a `Trace`, and a dial and a knob that
    share a serial, so that a frame kind can be varied;
  - unvalidated rows of `Gadget`, `Trace` and `Sample`;
  - a different value count per parent, for `Gadget` and for `Trace`;
  - exactly one `Weave`, sharing serial 1 with a `Trace`, tagged with a tag of its own beside the
    run tag, and with no dependents;
  - `Weave_members` rows with a `None` `anchor`, and with a `None` `origin`; a `Weave` whose own
    `anchor` is `None`; `Sample` anchors on another shard, and one `None`;
  - for every identity field of every inventory class, a second row it can be varied to;
  - shard keys over two shards, with no sharded row on any further shard;
  - consistent counts (hazard 7).
- **It holds no assertion.** The port check's third rule fails any function of it that asserts.

  The log gives the row counts per table and per row set, as log 03b gave its step table.

**`datastorekit/tests/schema_description.py`**, ported from SGK's. It is R-imp:
- `importlib.import_module("datastorekit.SQL.Datastore")` in place of SGK's module path;
- `registry.factories` in place of `config.datastore.factories`.

Its `__main__` keeps capturing a witness. It names the new file by its argument, as SGK's does.

### 2.5 The witness

`datastorekit/tests/data/schema_at_extraction-04a.json` is the neutral client's schema. It is
captured once, by `schema_description`, from the tree with §2.3 applied, and before
`test_schema_builder` is ported.
- **The log records** the command, the tree it ran on, and the file's size and SHA-256.
- **It is captured a second time**, from a scratch copy of the tree in the session scratchpad, and
  the two captures are compared byte for byte.
- **SGK's witnesses are not copied**, and `test_schema_builder`'s `WITNESS` names the new file.

SGK's rule holds: a witness is never regenerated. A later change to the client's schema adds a new
witness file, and the test then names it. This applies to 06's.

### 2.6 The checks

**`compare_ported_tests.py`:**
- `PORTED` gains seven pairs: the five modules and the two fixtures. The port check then confirms
  that the fixtures keep SGK's classes and assert nothing new.
- `NAME_MAP` is unchanged, and nothing else changes.

**`compare_with_source.py`:**
- `FILES` gains the same seven as `PORTED`.
- `NO_SOURCE` is unchanged. The witness is not a `.py` file, and the client's additions go into
  existing files.
- 01's, 02's, 03a's and 03b's counts do not change.

**The run count**, which neither script sees: per module, `unittest`'s loader runs 42, 13, 15, 8
and 7. Verify it with `unittest.TestLoader().loadTestsFromName(...).countTestCases()`, and put it
in the log.

### 2.7 The other four modules

- **`test_store_schema`** and **`test_store_reader`** use the default store and its variants:
  - SGK's sharded drop group `GK_SOURCE_TABLES` (`test_store_schema.py:62`) becomes `Weave`'s
    tables, or `Sample`'s, by role;
  - the two tables given in reverse declaration order (`:151`) stay reversed, to keep the point
    of `:166`;
  - the expected messages and differences that name a table or column (`test_store_schema.py`
    about 12, `test_store_reader.py` 6) are R-map;
  - the shard file names `fixture-store-shard000N` (`test_store_reader.py:220`, `:228`, `:241`,
    `:255`) keep SGK's stem, which the fixture keeps.
- **`test_foreign_key_check`**:
  - the added rows and their counts (`ADDED_*`, `:62-97`) are R-count on the neutral full rows;
  - `test_the_added_row_is_not_satisfied_by_coincidence` keeps its meaning only if the neutral
    added member row's `tessera_serial` is also a `Sample` serial on that shard. Design it so, and
    say how.
- **`test_schema_builder`** compares with §2.5's witness. `TestNoneRegistration` is client-free.

### 2.8 The records

- `[01-package-prose-names-sgks-layout]`: re-measure by log 03a §8's method. Record the new count,
  and the lines the five modules and the two fixtures add. Update its index hook.
- `docs/OPEN_ISSUES.md`: 6 open now, and 6 after, unless the work opens an issue.
- Log 02's role table says `build_full_store` → `build.build_store`. Do not edit log 02. Hazard
  1's finding goes in this prompt's log, under "State handed to the next prompt", for 04b.

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s datastorekit/tests -t .` gives `Ran 353 tests …
   OK`. The 268 are still there by name, and 02's tests pass with their literals as §2.3 allows.
2. `compare_ported_tests.py` exits 0 over fifteen modules. Its whole output goes in the log.
3. `compare_with_source.py` exits 0, with 31 compared, 15 `PORTED` and 9 with no source. Its whole
   output goes in the log.
4. The loader's run counts are 42, 13, 15, 8 and 7 (§2.6).
5. **The vocabulary.**
   - `grep -nwE` for log 02 §1.2's 80 client names (the 82 less `version` and `store_tag`) finds
     none in the five modules, the two fixtures, or the client's files. SGK's five modules hold
     them on 284, 25, 9, 34 and 12 lines.
   - A second `grep -nwE` looks for SGK's modules and keywords: `CosmologyModels`,
     `CosmologyConcepts`, `ComputeTargets`, `extract_common`, `config\.`, `Planck2018`,
     `k_inv_Mpc`, `log10_tol`, `cosmology_type`, `cosmology_serial`, `model_serial` and
     `Run_fixture`. Each hit is either prose ported unchanged (03a §2.1) or a finding.
6. **The breakage record.** Each item is a diff exactly as applied, with what failed. None is
   committed. Record each diff with its trailing context lines, and check it with `git apply
   --check` as recorded (03b's review found three that had lost theirs).
   - **The checks:**
     - (a) one assertion deleted from a `test_store_inventory` test: `compare_ported_tests.py`
       exits 1, naming it;
     - (b) an assertion call added to a function of `real_store_fixtures.py`: it exits 1, "not in
       the source, and asserts";
     - (c) `real_store_fixtures.py` removed from `FILES`: `compare_with_source.py` exits 1.
   - **The layer, through the ported tests:**
     - (d) `canonical` formats a float with `repr`, not `float.hex` (`store_inventory.py:133`):
       `TestFloats` fails;
     - (e) no `orphan-value` is reported (`store_inventory.py:658`, `if len(orphans) > 0:` made
       false): `TestOldStoresAndOrphans` fails;
     - (f) a key held twice is not a duplicate (`store_inventory.py:880`, `> 1` made `> 2`):
       `TestDuplicates` fails;
     - (g) `schema_differences` ignores an absent column (`SQL/schema.py:468`): the tests of a
       shard that lacks a column fail, in `test_store_schema` and `test_store_reader`;
     - (h) `read_only_url` drops `mode=ro` (`store_reader.py:114`): name what fails;
     - (i) the version column the builder prepends is not indexed (`SQL/schema.py:131`,
       `index=True` removed): `test_schema_builder` fails against the witness.
   - **The client:**
     - (j) `Trace`'s spec without `values`: `TestValueCounts` fails;
     - (k) `Weave`'s parent set without its `anchor` member: name what fails.
   - For (d)–(k), name every test that fails, and say whether its SGK counterpart pins the same
     line. A mutation that fails nothing is a finding: open a §3 issue for it.
7. `black --check` (25.1.0) is clean on everything under `datastorekit/` and `docs/extraction/`.

---

## 4. Acceptance

1. The five modules and the two fixtures are ported under their names, and both checks pass.
2. The client has §2.3's six tables and the warning, and the only other edits are those §2.3
   allows.
3. §3.1–§3.7 hold.
4. **The records**, in the same commit:
   - the log, `logs/04a-port-the-store-and-inventory-tests.md`, per README §5.1. It also has:
     - **the port table:** one row per test (85), giving its SGK origin, the kinds of change made
       to it, and the SGK classes it uses with their neutral counterparts;
     - the map as used (§2.2), with each "by role" choice and every row the agent changed, and
       why;
     - what the agent found for each of §2.2's eleven hazards;
     - the six tables, and every literal of `test_neutral_client.py` and line of
       `docs/client-contract.md` that changed;
     - the fixture's row counts, per table and row set, and the derived `references()` map;
     - `test_store_inventory`'s four data tables: the rule each follows, its count before and
       after, and the absent categories;
     - the witness: the command, the tree, its size and SHA-256, and the second capture;
     - both checks' whole output, and the loader's run counts;
     - the test count before (268) and after (353);
   - the board: §1's row for 04a and the header; §3 per §2.8;
   - `docs/OPEN_ISSUES.md`, per §2.8;
   - `prompts/INDEX.md`: the campaign's line.

---

## 5. Stop conditions — stop and ask the user

- A ported test would need an assertion removed, replaced or added, its name changed, or its
  control flow changed. A test that cannot be expressed on the neutral client is recorded, not
  dropped, and the user decides.
- A test needs a class, column or registry entry beyond §2.3's.
- One of 02's, 03a's or 03b's tests fails with §2.3 applied, other than through a literal §2.3
  names.
- A ported test fails on the neutral client, and passing it would need a change to the layer. That
  may be a real defect: record what fails, and ask.
- `compare_with_source.py`, `compare_ported_tests.py` or the stand-in pool would need a change
  outside §2.6.
- Anything would start Ray, open a store outside a `tempfile` directory, or edit, run or open a
  store of SGK, ChamPBH or StochasticInstantons. Reading their files through `git show` is the only
  access allowed. Do not import or run SGK's fixtures: transcribe from them.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `datastorekit/tests/test_store_inventory.py`, `test_store_schema.py`, `test_store_reader.py`,
    `test_foreign_key_check.py` and `test_schema_builder.py` (ported);
  - `datastorekit/tests/real_store_fixtures.py` and `datastorekit/tests/schema_description.py`
    (ported);
  - `datastorekit/tests/data/schema_at_extraction-04a.json` (new);
  - `datastorekit/tests/client/objects.py`, `factories.py`, `registry.py` and `build.py`, as §2.3
    says;
  - `datastorekit/tests/test_neutral_client.py` and `docs/client-contract.md`, in the literals and
    lines §2.3 names;
  - `docs/extraction/compare_ported_tests.py` and `compare_with_source.py`, as §2.6 says;
  - the log, this board, `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.
- No file under `datastorekit/` outside `tests/` changes. Neither do `standin_pool.py`,
  `shard_store_fixtures.py`, `client/reader.py`, 03a's and 03b's modules, `PROVENANCE.md`,
  `pyproject.toml` or the repository's `README.md`.
- It ports none of 04b's modules, and writes no guard.
- It fixes nothing in the layer, including the four inherited issues, the bare `KeyError` of
  `[02-an-unsupplied-sharded-table-raises-keyerror]`, and anything a ported test reveals.
- It writes no orchestration note and makes no tag.

---

## 7. The log and the board

`logs/04a-port-the-store-and-inventory-tests.md`, using README §5.1, with the additions of §4.4.

`IMPLEMENTATION_STATE.md`: §1's row for 04a (landed, commit, log), the header, and §3.
