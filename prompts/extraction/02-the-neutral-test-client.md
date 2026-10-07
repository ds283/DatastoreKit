# Prompt 02 — the neutral test client

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 01 landed (`8bc60a5`), and its review was recorded (`d86a473`).
- U8 is taken (README §6.2): the 88 ported tests move onto the neutral client's names here.
- `git status` is clean in this repository.

**Closes:** `[01-ported-tests-use-sgk-table-names]` (§2.5). **Narrows:** nothing. **Opens:**
only what the work finds. One line moves from the closed issue into
`[01-package-prose-names-sgks-layout]` (§2.5).

**Recommended model:** **Opus**. 03 and 04 port 304 tests onto what this prompt builds, and the
contract document is what every client's adoption reads. It is mostly measurement and design;
little of it is mechanical.

**Read first:**

1. [`README.md`](README.md): §0.1, §0.2 (the test placement table and "What a client must
   supply"), §1, §2 (rows 02–04), §4, §5 (all of it, rules 6, 8 and 9 especially) and §6.2 (U8).
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`, in particular "What this repository is"
   and "Repository mechanics".
3. The board, with 01's review, and [`logs/01-import-the-layer.md`](logs/01-import-the-layer.md)
   as an example of the log's form. Its §7 says what 01 handed on.
4. The package as 01 left it: `datastorekit/`, `PROVENANCE.md` and
   `docs/extraction/compare_with_source.py`.
5. In SGK at `6f7f291`, **read with `git -C /Users/ds283/Documents/Code/SecondaryGWKit show
   6f7f291:<path>`**, never from SGK's working tree:
   - `Datastore/tests/standin_pool.py`, which §2.3 ports in part;
   - `config/datastore.py` and `config/sharding.py`, as an example of a client's registry;
   - the imports of the 18 test modules README §0.2 places in 03 and 04, and the SGK fixtures
     they use (`real_store_fixtures.py`, `schema_description.py`). §2.2's role table needs them.

Line numbers below are at `8bc60a5` for the package, and at `6f7f291` for SGK.

---

## 1. What is wanted

A client of `datastorekit` supplies a fixed set of facts: constructor arguments, `register()`
keys, factory hooks, inventory declarations and two layer-owned tables. Today these are written
down nowhere but in the code. After this prompt:

- `docs/client-contract.md` states each one, says whether it is required, optional or defaulted,
  and what the layer does with it;
- a **neutral test client** under `datastorekit/tests/client/` supplies every one of them at least
  once, with abstract names. Its tests open it on the stand-in pool, write every class, read
  every class back, and reopen;
- the **stand-in pool** (`datastorekit/tests/standin_pool.py`) is SGK's, ported without its SGK
  half, with its defaults pointed at the neutral client;
- the 88 tests 01 ported no longer use SGK's table names (U8);
- `compare_with_source.py` still accounts for every line of every file taken from SGK, and now
  also **fails** on a file under `datastorekit/` that it does not account for.

03 and 04 then port their 304 tests onto the client and the pool without inventing either.

**No behaviour of the layer changes.** No file under `datastorekit/` outside `tests/` is touched
(README §5 rule 8). A defect noticed in the layer is recorded, not fixed.

---

## 2. What to change

### 2.1 `docs/client-contract.md`

**Measure it from the package, `datastorekit/` at `8bc60a5`.** It equals SGK's layer, so this is
the same as measuring SGK's, and needs no client. For each item, find every place the layer reads
it, by `grep` and `ast`, and record:
- its name;
- where the client gives it (constructor argument, `register()` key, factory method, field of a
  declaration, a table the client registers);
- **required**, **optional** or **defaulted**, and the default;
- what the layer does with it, in one or two sentences;
- what the layer does when it is wrong or absent (a `ValueError` at schema build, a refusal at open,
  silence), with the line that does it;
- the neutral client's class or argument that supplies it (§2.2).

**The planner's survey, 2026-10-07, at `8bc60a5`.** This is a check on your measurement, not a
substitute for it. If a count differs, the log says which and why.
- `ShardedPool.__init__` (`SQL/ShardedPool.py:95-114`) takes **16** parameters:
  - `version_label`, `db_name`, `ShardKeyType`, `ShardKeyStoreIdGetter`, `replicated_tables` and
    `sharded_tables`, positional and required;
  - `timeout`, `shards`, `profile_agent`, `job_name`, `prune_unvalidated`, `drop_tables`,
    `read_table_config` and `read_only`, defaulted;
  - `factories`, keyword-only and required, and `serial_batch_sizes`, keyword-only and defaulted.

  `ShardKeyType.__name__` is kept (`:157`) and names the shard-key table. The getter maps a shard
  key, or a proxy for one, to its `store_id` (`:3262` and later).
- `register()` has **9 keys** read by `SQL/schema.py:95-180`: `validate_on_startup`, `serial`,
  `version`, `timestamp`, `stepping` (`True`, `"minimum"` or `"exact"`), `columns`,
  `owner_column`, `monotone_flags` and `validated_column`. A `register()` that returns `None`
  means a class with no table.
- **Factory hooks** called by the layer:
  - five abstract in `SQL/factory_base.py`: `register`, `build`, `store`, `validate`,
    `validate_on_startup`;
  - three defaulted there: `revalidate`, `owned_serials`, `inventory_spec`;
  - two not declared in the base, called only when used: `read_batch`
    (`SQL/Datastore.py:580`) and `read_table` (`:828-870`, through `read_table_config`'s
    `tables_arg`).
- **Declarations** (`store_inventory.py`): `InventorySpec` (`:297`, six fields: `leaves`,
  `parents`, `tags`, `values`, `validated`, `parent_sets`), `Parent` (`:209`, a class `of`, or a
  polymorphic `types` with `type_column`) and `ParentSet` (`:271`, including `cross_shard`).
  Count their fields yourself.
- **The layer-owned tables** (`contract.py`): the client registers a factory under `version`
  (label column `label`) and under `store_tag` (label column `label`). An association table names a
  tag by the column `tag_serial`.
- **The other entry points that take client facts:** at least `store_reader.open_read_only(primary,
  factories)` and `store_inventory.read_inventory(...)`. Find any others.
- **What the layer reads from a stored object**: `DatastoreObject` (`object.py`) and whatever the
  actor and pool read beyond it.

**The document names no client.** Its examples are the neutral client's. One line at its head says
it was measured from the package at `8bc60a5`, whose layer is SGK's at `6f7f291`
(`PROVENANCE.md`).

### 2.2 The neutral client, `datastorekit/tests/client/`

A package of the test suite: objects, factories and a registry, importing only the standard
library, `sqlalchemy`, `ray` (only if a factory needs it as SGK's do) and `datastorekit`. The import
guard (`test_package_imports.py`) already scans it.

**Names fixed by this prompt**, because §2.4's re-fixturing and §2.5's check rule use them:
- the shard-key class is **`keypoint`** (lowercase, like the replicated classes of every client;
  its `__name__` names its table);
- the sharded parent class is **`Sample`**, sharded on the payload field **`"k"`**;
- its tag association is **`Sample_tags`**;
- **the registry module is `datastorekit/tests/client/registry.py`**, exporting exactly:
  `factories`, `replicated_tables`, `sharded_tables`, `shard_key_type`, `shard_key_store_id`,
  `read_table_config`, `serial_batch_sizes`, `drop_groups` and `tables_to_drop`. These are the
  names 03 and 04 import.

**Every other name is yours**, under two constraints:
- Each is abstract, and none is a table name in any client's registry. On 2026-10-07 these included
  `redshift`, `tolerance`, `IntegrationSolver` and `QCD_Cosmology`, which all three clients share.
  Measure the three registries read-only (SGK's `config/datastore.py`; CPBH's and SI's
  `Datastore/SQL/Datastore.py`), and list them in the log. `version` and `store_tag` are the
  layer's, not a client's.
- Each is a **whole, distinctive identifier**, so that 04's vocabulary guard can tell it from a
  client's and from English prose.

**What the client must supply.** Every item of §2.1, at least once. In particular, as README §2
lists:
- the shard-key class, replicated, and its getter (with one proxy class, as SGK's
  `wavenumber_exit_time` is for `wavenumber`);
- replicated leaf tables, one with `monotone_flags`;
- a sharded parent (`Sample`) with `validate_on_startup`, a `validated_column` and `revalidate`;
- an owned value table (`owner_column`) with `owned_serials`;
- a tag association (`Sample_tags`);
- a polymorphic `Parent`, and a `ParentSet`, one of them `cross_shard`;
- `read_table` (with `tables_arg` both ways, through `read_table_config`), `read_batch`, and
  `stepping` in both string modes;
- a class whose `register()` returns `None`;
- `serial: False` and `timestamp: True` somewhere;
- `drop_groups` whose union is every droppable table, and `tables_to_drop`.

**Keep it small.** One class per role where one class can carry several roles. The client is a
fixture, not a model of any science.

**The roles 03 and 04 will need.** Measure what the 18 modules README §0.2 places in 03 and 04
import from SGK (`config.*`, `standin_pool`'s object helpers, `real_store_fixtures`,
`schema_description` and others). In the log, give a table with one row per imported name:
- what it does for the test (for example "build a store with every class populated");
- the neutral client's counterpart, or "**03/04 ports it**" where it is a fixture helper that
  belongs with its tests.

**02 provides at least:**
- the registry (above);
- object constructors for each class;
- one builder, `datastorekit/tests/client/build.py::build_store(directory, shards=3)`, which
  writes a store with every class populated through the stand-in pool and returns its primary's
  path. It is the counterpart of SGK's `build_full_store`, not a port of it.

### 2.3 The stand-in pool, `datastorekit/tests/standin_pool.py`

SGK's `Datastore/tests/standin_pool.py` (581 lines) has two halves:
- **Generic, `:1-420`**: the stand-in actor classes, `StandinCluster`, `open_pool`,
  `open_pool_output`, `close_pool`, `replica_ids`, and the file readers (`table_columns`,
  `shard_rows`, `shard_snapshot`, `store_checksums`, `in_flight_records`).
- **SGK's, from the banner at `:421-423`** ("objects for the two stored replicated classes, and
  one sharded class") to the end: `StandinSerial`, `StandinCosmology`, `make_units`,
  `get_wavenumber`, `get_tolerance`, `make_exit_time`, `get_redshifts`, `make_background_model`
  and `make_policy_data`.

Port the generic half, changed only by:
- D-imp and D-str, as in 01 (`importlib.import_module("Datastore.SQL.ShardedPool")` and its two
  siblings are whole-literal module paths);
- **D-split** (new, §2.6): the SGK half removed, from its banner to the end of the file; and in
  `open_pool` and `open_pool_output` only, the two `from config.… import …` statements replaced
  by one `from datastorekit.tests.client.registry import (factories, replicated_tables,
  sharded_tables, shard_key_type, shard_key_store_id)`, with `shard_key_wavenumber_store_id`
  renamed `shard_key_store_id` where those two methods use it.

Nothing else changes, the docstring included. Its prose names SGK paths; that is
`[01-package-prose-names-sgks-layout]`'s. The neutral counterparts of the SGK helpers live in
`datastorekit/tests/client/`, not in the stand-in pool.

### 2.4 The 88 tests onto the neutral client's names (U8)

01's tests and fixture use SGK's names as data in hand-built stores. Map them:

| SGK | Neutral |
|---|---|
| `wavenumber` | `keypoint` |
| `wavenumber_serial` | `keypoint_serial` |
| `GkSource` | `Sample` |

The planner found them at (`8bc60a5`):
- `tests/shard_store_fixtures.py:25-27`;
- `tests/test_shard_key_audit_copy.py:43`, `:45`, `:104`;
- `tests/test_shard_key_audit_refusals.py:7`, `:65-66`, `:184`, `:186`, `:192`, `:205`, `:227`,
  `:229`.

Re-measure with `grep -nw`. The shard-key field `"k"` stays: it is a field name, not a table, and
the client shards `Sample` on `"k"` too.

**This is re-fixturing (README §5 rule 6).** The rules:
- A name changes **only inside a string literal**, and only as a **whole identifier**.
- A docstring that names the fixture's table changes with it (`test_shard_key_audit_refusals.py:7`).
- An expected string that echoes the fixture's name back changes with it, and nothing else in it.
  An example is `test_shard_key_audit_copy.py:104`'s `"'wavenumber' table (shard #0) row count:
  2"`, which the audit tool builds from `shard_key_config.key_type`.
- No test name, class name, other assertion or control flow changes. Each changed line is listed
  in the log.

**Outside the tests, nothing changes.** `datastorekit/tools/shard_key_audit.py:188` (`e.g.
"wavenumber"`) is package prose under rule 8. Move it to `[01-package-prose-names-sgks-layout]`
(its count goes from 101 to 102 lines, `tools/shard_key_audit.py` from 3 to 4).

### 2.5 The records of U8

- Close `[01-ported-tests-use-sgk-table-names]`: move it to the board's §4 with a dated "Closed"
  line naming this prompt, the map, the count of lines changed and the line moved to the prose
  issue.
- `[01-package-prose-names-sgks-layout]`: its count and the moved line.
- `docs/OPEN_ISSUES.md`: the closed row deleted; the prose row's hook if its count is in it; the
  header's count (7 now, 6 after unless the work opens anything).

### 2.6 `compare_with_source.py`

Three changes, each narrow, each of which must bite (§3.4):

- **D-fix — the re-fixture.** Applied to the four files of §2.4 and nothing else. Inside a string
  literal, each whole identifier of §2.4's map becomes its image. As with 01's rules, it is a
  transformation of the source, so it can only explain a change it makes.
- **D-split — the stand-in pool.** `standin_pool.py` joins `FILES`, and its rule is §2.3's: the
  tail cut at the banner, the two imports replaced, the one name renamed in the two methods.
- **An unaccounted file fails.** Every `.py` under `datastorekit/` is in `FILES`, or in a
  declared set of files with no SGK source. The neutral client's files and the new test module
  join that set; 01's `NEW_FILES` becomes it. Anything else is reported as "NOT ACCOUNTED FOR"
  **and makes the check exit 1**. Generated files (`__pycache__`) are not counted.

01's classes, rules and counts for the files it covers do not change, except where D-fix now
explains a line. The script's docstring describes the two new classes and the new failure.

### 2.7 The neutral client's own tests

New module or modules under `datastorekit/tests/` (for example `test_neutral_client.py`). On the
stand-in pool, with no Ray, in `tempfile` directories:
- **Coverage, by declaration.** `build_schema(registry.factories)` and the specs show every
  `register()` key of §2.1 in use, in each of its forms (each `stepping` mode, `serial: False`, a
  `None` registration and the rest). Every `InventorySpec`, `Parent` and `ParentSet` field is in
  use, and every hook is defined by some factory. This test fails if a role disappears from the
  client.
- **Round trip.** `build_store` writes every class, the pool closes, and it reopens read-write
  with the check at open passing and nothing repaired. `open_read_only` and `read_inventory`
  read it, and every class's rows come back.
- **The registry.** `tables_to_drop` over `drop_groups` gives each group's tables, and
  `schema.dependent_tables` accepts each group as the client declares it.

These are new tests, not ports. Name them by what they show.

**The suite goes from 90 to 90 + the new tests.** Every one of 01's 90 still passes, with its
name.

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s datastorekit/tests -t .` gives `Ran N tests … OK`,
   with N > 90, and 90 of them are 01's, by name.
2. `compare_with_source.py` exits 0. Its whole output goes in the log, with the counts per file and
   class. The counts for 01's files are unchanged except for D-fix lines in §2.4's four files.
3. From the scratchpad with `PYTHONPATH` unset, `import datastorekit.tests.client.registry` and
   `import datastorekit.tests.standin_pool` succeed. Neither starts Ray
   (`ray.is_initialized()` is false afterwards).
4. **The breakage record.** Each item is a diff exactly as applied, with what failed. None is
   committed.
   - **The check:**
     - (a)–(e) of 01, replayed; each still fails.
     - (f) `wavenumber` → `keypoint` in a comment of `datastorekit/tools/shard_key_audit.py`, a
       file D-fix does not cover; it must fail.
     - (g) One extra line in the ported half of `standin_pool.py`; it must fail.
     - (h) An empty `datastorekit/stray.py`; it must fail, as NOT ACCOUNTED FOR.
     - (i) In `test_shard_key_audit_refusals.py`, `keypoint` written into a line that is not a
       string literal, for example a renamed local variable; it must fail.
   - **The tests:**
     - (j) Remove `monotone_flags` from the client's factory that declares it; the coverage test
       fails.
     - (k) Make `revalidate` of `Sample`'s factory return without writing; a round-trip or
       coverage test fails. If none does, say so: that is a finding for 03.
     - (l) In `datastorekit/tools/shard_key_audit.py`, make the row-count message print the
       literal `'wavenumber'` in place of the table it read. `test_shard_key_audit_copy` must now
       fail. Before §2.4 it would have passed, so this shows the re-fixturing took SGK's name out
       of the tests' expectations.
     - (m) A breakage of the stand-in pool that cannot start Ray, chosen by you. For example,
       `_StandinRandom.randrange` ignoring the pinned controller. Name the test it fails. **Do not
       remove the `ray.get` patch:** `ray.get` of a non-reference may initialise Ray.
5. `black --check` (25.1.0) is clean on everything under `datastorekit/` and `docs/extraction/`.

---

## 4. Acceptance

1. `docs/client-contract.md` exists, as §2.1 says. **The log's table maps each contract item to
   the neutral client's class, argument or test that exercises it, and every item is covered**
   (README §2).
2. The neutral client, the stand-in pool and `build_store` exist under §2.2's and §2.3's names, and
   the registry exports exactly §2.2's nine names.
3. §3.1–§3.5 hold.
4. **The records**, in the same commit:
   - the log, `logs/02-the-neutral-test-client.md`, per README §5.1. It also has:
     - the contract's counts against the planner's survey;
     - the three clients' registry names, measured;
     - the role table for 03 and 04;
     - the list of re-fixtured lines;
     - the check's output;
     - the test count before (90) and after, with the new tests named;
     - **the entry points 03 and 04 use** (README §4, "After 02"), each with its signature.
   - this board: §1's row for 02 and the header; §3 and §4 per §2.5;
   - `docs/OPEN_ISSUES.md`, per §2.5;
   - `prompts/INDEX.md`: the campaign's line.

---

## 5. Stop conditions — stop and ask the user

- A contract item cannot be supplied by a neutral client without a change to the layer.
- A ported test fails after §2.4, and passing it would need more than §2.4's map.
- The stand-in pool cannot open the neutral client without a change outside §2.3's D-split.
- A class of difference outside D-imp, D-str, D-tool, D-root, D-int, D-fmt, D-fix and D-split is
  needed to account for a file.
- Anything would start Ray, open a store outside a `tempfile` directory, or edit, run or open a
  store of SGK, ChamPBH or StochasticInstantons. Reading their files is the only access allowed.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `docs/client-contract.md`;
  - `datastorekit/tests/client/` (new);
  - `datastorekit/tests/standin_pool.py` (new);
  - the new test module(s) of §2.7;
  - the four files of §2.4;
  - `docs/extraction/compare_with_source.py`;
  - the log, this board, `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.
- No file under `datastorekit/` outside `tests/` changes, and neither does `PROVENANCE.md`,
  `pyproject.toml` or the repository's `README.md`.
- It ports none of 03's or 04's tests, and no SGK fixture helper beyond §2.3's half of the stand-in
  pool. `real_store_fixtures.py` and `schema_description.py` stay SGK's; 03 and 04 port what they
  need.
- It fixes nothing in the layer, including the four inherited issues and the untested
  `_assign_shard_keys` (`[01-no-ported-test-pins-the-shard-key-assignment]`, 03's). The neutral
  client's shard-key class must be able to reach it, since 03 will pin it there.
- It writes no orchestration note and makes no tag.

---

## 7. The log and the board

`logs/02-the-neutral-test-client.md`, using README §5.1, with the additions of §4.4.

`IMPLEMENTATION_STATE.md`: §1's row for 02 (landed, commit, log), the header, §3 and §4.
