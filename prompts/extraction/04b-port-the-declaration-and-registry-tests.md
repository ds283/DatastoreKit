# Prompt 04b — port the declaration and registry tests, and write the package's guard

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 04a landed (`7ceed25`), and its review was recorded (`1a54af1`).
- U16 and U17 are taken (README §6.2, 2026-10-08), and so are U18–U21, which 04a applied.
- `git status` is clean in this repository.

**Closes:** `[04a-no-test-pins-a-second-parent-set-member]` (§2.6). **Narrows:** nothing.
**Changes:** `[01-package-prose-names-sgks-layout]`, whose count grows by the ported modules' prose
(§2.9). **Opens:** only what the work finds.

**Recommended model:** **Opus.**
- Four of the five modules port much as 04a's did, on 04a's fixture.
- The fifth, `test_layer_is_generic`, becomes the package's guard. Its vocabulary is measured from
  the three clients, read-only, and held as data. It pins the one hit that rule 8 freezes in the
  layer (U17).
- Two classes of tests ask that the layer load no client module. Ported literally, they would pass
  without testing anything; §2.4 retargets them on the neutral client.

**Read first:**

1. [`README.md`](README.md): §0.2, §2 (rows 04b and 05), §4, §5 (rules 6–9 especially) and §6.2
   (U8–U21).
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`, above all "The package knows nothing about
   any client".
3. The board, with the reviews of 03b and 04a, and the issue `[04a-no-test-pins-a-second-parent-set-member]`.
   Then:
   - [`logs/04a-port-the-store-and-inventory-tests.md`](logs/04a-port-the-store-and-inventory-tests.md)
     §1–§3, §7 and §9;
   - [`logs/03a-port-the-replicated-write-tests.md`](logs/03a-port-the-replicated-write-tests.md)
     §2.1's kinds, as 04a's prompt restates them, and §8 (the prose method);
   - [`logs/02-the-neutral-test-client.md`](logs/02-the-neutral-test-client.md) §1.2 (the three
     clients' registries).
4. The package as 04a left it:
   - `datastorekit/tests/client/` (all of it), `standin_pool.py` and `real_store_fixtures.py`;
   - `datastorekit/tests/test_prune_at_open.py` (`_PruneTestCase`, which a ported class
     subclasses) and `test_package_imports.py` (01's import guard);
   - `datastorekit/store_inventory.py`, `datastorekit/SQL/schema.py`, and in
     `datastorekit/SQL/ShardedPool.py` the drop refusals and `_unit_tables`;
   - `docs/extraction/compare_ported_tests.py` and `compare_with_source.py`.
5. In SGK at `6f7f291`, **read with `git -C /Users/ds283/Documents/Code/SecondaryGWKit show
   6f7f291:<path>`**, never from SGK's working tree: the five modules under `Datastore/tests/`,
   `test_inventory_declarations.py`, `test_declared_facts.py`, `test_layer_registry.py`,
   `test_drop_refuses_dangling_references.py` and `test_layer_is_generic.py`.

Line numbers below are at `1a54af1` for the package (unchanged since `7ceed25`), and at `6f7f291`
for SGK.

---

## 1. What is wanted

U14 gave 04b these five modules of §0.2's 175:

| SGK module | Lines | Tests | Per class |
|---|---|---|---|
| `test_inventory_declarations` | 545 | 26, of which 25 are ported (U16) | 8, 10, 6, 2 |
| `test_declared_facts` | 671 | 25 | 3, 9, 2, 4, 2, 3, 1, 1 |
| `test_layer_registry` | 692 | 20 | 3, 2, 2, 3, 2, 5, 1, 2 |
| `test_drop_refuses_dangling_references` | 307 | 11 | 7, 4 |
| `test_layer_is_generic` | 374 | 8 | 3, 3, 2 |
| **total** | 2,589 | **90**, of which **89** are ported | |

They were counted by `ast` at `6f7f291`. One class inherits across modules:
`test_declared_facts.TestThePruneRefusalNamesItsUnit` subclasses `test_prune_at_open._PruneTestCase`,
which 03a ported.

After this prompt:
- the five modules run in `datastorekit/tests/` under their SGK names, on the neutral client and
  04a's fixture. Each test keeps its SGK class and method name, and its assertions. The one
  exception is U16's test, which is declared not ported;
- `datastorekit/tests/test_layer_is_generic.py` is the package's guard (§2.3). It scans every
  module of the layer for the three clients' vocabulary. That vocabulary is held as data in
  `datastorekit/tests/data/client_vocabulary.json`, written by
  `docs/extraction/measure_client_vocabulary.py`;
- `datastorekit/tests/test_parent_set_members.py` (new, with no source) closes
  `[04a-no-test-pins-a-second-parent-set-member]` (§2.6);
- `compare_ported_tests.py` checks twenty modules and has a `NOT_PORTED` list (U16), and
  `compare_with_source.py` accounts for every new file;
- the suite is **444**: 353 + 89 + 2.

**No behaviour of the layer changes, and the client does not change.** No file under
`datastorekit/` outside `tests/` is touched (README §5 rule 8), and neither is
`datastorekit/tests/client/`. The measurements in §2.2 show that the client as 04a left it plays
every role. If a test needs a change to either, that is a stop (§5).

---

## 2. What to change

### 2.1 What re-fixturing may change

03a §2.1 governs, as 04a's prompt restated it: the kinds R-imp, R-map, R-help, R-value, R-count and
R-name, and nothing else. Four points are particular to 04b.

- **R-name applies to no test.** No test or class name in the five modules holds one of log 02
  §1.2's 82 client names as a word or as an underscore part. `NAME_MAP` gains nothing.
  - Some names hold SGK vocabulary that is not a table name. They keep their names:
    `test_the_full_store_resolves_both_cosmology_types`, `test_a_background_model_names_its_value_rows`
    and `test_the_report_renders_both_cosmology_types` (U16's, not ported).
  - **`test_exactly_the_four_declarations_are_not_default` keeps its name, though the neutral
    client has three** (§2.2, hazard 4). The number is SGK's count, not a client name. Rule 6
    keeps the name, and the log says so.
- **R-imp covers code in strings.** Two modules run a child interpreter whose code imports SGK
  (`test_inventory_declarations.py:513-526`, `:532-539`; `test_layer_registry.py:624-629`). Its
  `PYTHONPATH` and `cwd` are the repository root, as 04a's `test_no_ray` has them.
- **Literals measured over the registry or the fixture are R-count.** They are re-measured on the
  tree, never translated entry by entry: `ORDER`, `DECLARED`, `COMMAND_LINE_ORDER`, `MEASURED`,
  and the counts of the absent-parent walk. The log gives each one's value before and after, and
  how it was measured.
- **The guard's vocabulary is data, not R-map** (§2.3). The guard module and its data file are the
  only files of the package that name client words. §3.5's grep exempts exactly those two.

### 2.2 The map, and what the planner measured

By role, as 04a's map (log 04a §1.1). The rows 04b uses:

| SGK | What the tests use it for | Neutral |
|---|---|---|
| `config.datastore.factories`, `drop_groups`, `tables_to_drop`; `config.sharding.*` | the registry | `datastorekit.tests.client.registry` |
| `BackgroundModel` (+`_tags`, `Value`) | the replicated owner: `validated_column`, `revalidate`, `owned_serials`, the prune, a unit of three tables | `Gadget` (+`Gadget_tags`, `GadgetPart`) |
| `redshift`, `wavenumber` (`source`, `response`) | the classes with `monotone_flags` | `keypoint` (`kp_marked`, `kp_flagged`), the only one |
| `tolerance` | a replicated leaf with no dependents | `routing_rule`, as in 04a; `dial_setting` where 03a's `_PruneTestCase` has it (§2.7) |
| `LambdaCDM`, `QCD_Cosmology`; `COSMOLOGY_TYPES`, `LAMBDACDM_IDENTIFIER`, `QCD_EOS_IDENTIFIER` | the polymorphic parent's two types and its map | `dial_setting`, `knob_setting`; `factories.FRAME_TYPES`, `FRAME_KINDS` |
| `wavenumber_exit_time`, `BackgroundModel` (the two referencing factories) | the one shared map | `Gadget`, `Trace` |
| `GkWKBIntegration.numeric` (key) and `GkSource`'s member `numeric` | a nullable key parent, and a member field of the same name | `Weave.anchor`, and `Weave`'s member `anchor` |
| `OneLoopIntegral` (+`_tags`) | a class a registry can leave out | `Weave` (+`Weave_tags`, `Weave_members`) |
| `QuadSourceIntegral` (+`_tags`) | a class left in, beside it | `Trace` (+`Trace_tags`) |
| `GkSource` | a sharded table a drop names | `Sample` |
| `QuadSourceIntegral` → `TkWKBIntegration`, with no foreign key | a declared parent without a foreign key | `Sample` → `Tessera` (`anchor_serial`) |
| `GkSource_parents` | a foreign key without a declared parent | `Sample_members` → `Tessera` |
| `QuadSourceIntegral_tags` | a dependent behind the first level | `Sample_tags` (→ `Sample` → `Tessera`) |
| the drop groups (`tk-numeric`, …) | `drop_groups` | `aliases`, `tesserae`, `samples`, `gadgets`, `traces` |

**Measured by the planner** on `1a54af1`, from the scratchpad, with nothing written:
- **The derived order** (`inventory_classes`) is `version`, `store_tag`, `keypoint`,
  `dial_setting`, `knob_setting`, `gauge_setting`, `routing_rule`, `keypoint_alias`, `Gadget`,
  `Tessera`, `Sample`, `Trace`, `Weave`.
  - **A plain sort differs from it**: it places `keypoint_alias` fourth. So
    `test_roots_come_first_unlike_a_plain_sort`'s `assertNotEqual` holds.
  - The roots are the first seven. Every `inventory_spec` takes no parameter.
- **The registry less `Gadget`, `Gadget_tags` and `GadgetPart`:**
  - `inventory_classes` raises `ValueError`, "Sample references Gadget, which declares no
    inventory_spec";
  - `read_inventory` on 04a's full store raises `RuntimeError` naming `replicated_tables` and
    `Gadget`.
- **Dropping every group's tables** from shard 0 of the full store with `PRAGMA foreign_keys = ON`:
  sorted by `drop_order`, it succeeds with 14 lines printed; unsorted (`drop_order` patched to the
  identity), it raises `IntegrityError`. Patch `drop_order` on the module from
  `importlib.import_module("datastorekit.SQL.Datastore")`, as SGK does: the dotted import binds
  the actor class.
- **The record without `routing_rule`** (deleted from the primary's `replicated_tables`):
  `routing_rule` is combined as sharded, with count 6 against 3 and one `duplicate` problem.
  `keypoint`'s records are unchanged.
- **The compared tables** are `version`, `store_tag`, `keypoint`, `keypoint_alias`,
  `dial_setting`, `knob_setting`, `gauge_setting`, `routing_rule`, `Gadget`, `GadgetPart` and
  `Gadget_tags`. The only unit of more than one table is `Gadget`'s, `['Gadget', 'Gadget_tags',
  'GadgetPart']`.
- **The non-default declarations** are three:
  - `keypoint`: `monotone_flags=('kp_marked', 'kp_flagged')`;
  - `Gadget`: `validated_column='gadget_validated'`;
  - `GadgetPart`: `owner_column='gadget_serial'`.
- **The version object** on a reopen, read-write and read-only, is
  `{'_my_id': 1, 'label': 'standin', '_deserialized': True}`. (On a fresh store it carries
  `_new_insert` in place of `_deserialized`.)
- **`dependent_tables`** of each group:
  - `aliases`: `Tessera`, `Sample`, `Sample_tags`, `Sample_members`, `Weave`, `Weave_tags`,
    `Weave_members`;
  - `tesserae`: the same less `Tessera`;
  - `gadgets`: `Sample`, `Sample_tags`, `Sample_members`;
  - `samples` and `traces`: none.

  This is `test_neutral_client.MEASURED_DEPENDENTS` after 04a. Also:
  - `Sample`'s foreign keys name `keypoint`, `version` and `Gadget`, and its spec also names
    `Tessera`;
  - `Sample_members`' foreign keys name `Sample` and `Tessera`;
  - `Sample_tags`' foreign keys name `Sample` and `store_tag`;
  - `dependent_tables(["Gadget"])` is not empty.
- **The absent-parent walk** of `test_the_full_store_resolves_no_absent_parent_as_unresolved`,
  with the field `anchor` and the class `Weave`, gives 1 record, 1 key and 1 member, and
  `no_digest` 0.
  - The key parent and the member field now share a name within one class, where SGK's shared it
    across two. The walk tells them apart as SGK's does: by the class of the key, and by being in
    a set.
- **The frame map**: `FRAME_KINDS == {'dial_setting': 1, 'knob_setting': 2}`. `Gadget`'s and
  `Trace`'s `frame` parents hold the same `FRAME_TYPES` object (`is`), with `type_column
  'frame_kind'` and `of` `None`. Both frame kinds occur in each class's records.
- **The second member.** Varying `Weave_members` row 702's `origin_serial` (3 → 1) changes
  `Weave`'s records and no other class's, with no problem. `ClassInventory.parent_sets` of `Weave`
  is `{'strands': {'anchor': 'Tessera', 'origin': 'Trace'}}`.

**Hazards the planner saw.** Check each, and say in the log what you found.
1. **`TestTheLayerKnowsNoProject` and `TestTheLayerImportsNoClient` would test nothing as written**
   (§2.4).
2. **`assertNoHits` must become exact in both directions without a second assertion** (§2.3).
3. **The guard needs no client to run.** It reads its vocabulary from the data file, never from a
   client's registry and never from the neutral client's. The neutral client's names are allowed
   in the layer's tests; they are not the layer's concern.
4. **`DECLARED` has three entries** (above), so `test_exactly_the_four_declarations_are_not_default`
   compares three. `TestTheFlags`' first literal names `keypoint` alone.
5. **`TestRevalidate` reads `Gadget`.**
   - The label is `gadget_label`, the flag `gadget_validated`, and the value table `GadgetPart`
     on `gadget_serial`.
   - Every `Gadget` of the fixture validates when nothing is deleted, the unvalidated one
     included, because 04a's counts agree (hazard 7 there).
   - The warning is the one 04a added (U15).
   - `_Model` must satisfy `Gadget_factory.validate`, which reads `available` and `store_id`.
6. **`TestOwnedSerials` reads `.parts`, not `._values`** (`Gadget_factory.owned_serials`,
   `factories.py:852`). The helper `_Owner` sets `parts` (R-help).
7. **`TestThePruneRefusalNamesItsUnit`** subclasses 03a's `_PruneTestCase`, whose store holds dial
   settings in SGK's tolerances' role (`test_prune_at_open.py:115-116`). Its trigger deletes from
   `dial_setting`. The expected text names `Gadget`'s unit in the specs' order. Measure it; the
   planner expects `['Gadget', 'GadgetPart', 'Gadget_tags']`.
8. **`TestThePoolUsesItsRegistry` must leave out three tables, not two.** `Weave_members` has a
   foreign key to `Weave`, so a registry that keeps it without `Weave` cannot build its schema.
   The tuple is R-count; the two `assertNotIn` and two `assertIn` name `Weave`, `Weave_tags`,
   `Trace` and `Trace_tags`.
9. **`REFUSED_GROUP` is sharded, as SGK's is.** `tesserae`, whose dependents are six, with
   `WITH_ITS_DEPENDENTS = [REFUSED_GROUP, "samples", "traces"]`. `test_an_undeclared_name_is_refused_first`
   uses `Gadget`, which is replicated with dependents, in `GkSourcePolicy`'s place.
10. **`build_store` does not stand for the fixture** (log 04a §9). Every test SGK built with
    `real_store_fixtures` uses 04a's port.

### 2.3 The guard (U17)

`datastorekit/tests/test_layer_is_generic.py` is SGK's guard, ported, with these changes. Each is
R-help unless it says otherwise, and the log lists each.

**What the layer is.** `layer_files()` gives every `.py` file under `datastorekit/` but
`datastorekit/tests/`, sorted, from the filesystem.
- At `1a54af1` that is 20 files.
- The factory contract `datastorekit/SQL/factory_base.py` is among them. The client's factories
  are under `tests/`, so the SGK exclusion of `ObjectFactories/` has no counterpart.
- `AUDIT_LIST` is SGK's thirteen, mapped by §4 of the README, less `RayTools/RayWorkPool.py`
  (excluded, D2): twelve files (R-count).
- `test_no_test_and_no_client_factory_is_in_it` keeps its two branches. Its factory branch reads
  the one factory module of the layer, `factory_base.py`.

**The vocabulary is data.**
- `docs/extraction/measure_client_vocabulary.py` (new) reads the three clients only through
  `git show` at fixed commits. It never imports them, and it writes
  `datastorekit/tests/data/client_vocabulary.json`. The commits are:
  - **SGK `6f7f291`**: the registry in `config/datastore.py`, `factories`;
  - **CPBH `52142d7`**: `Datastore/SQL/Datastore.py`, `_factories`;
  - **SI `00d254e`**: `Datastore/SQL/Datastore.py`, `_factories`. Its registry and factories are
    unchanged from log 02's `96d0562`.
- For each client the file holds:
  - the commit;
  - the registry's keys;
  - the column names, from the first string argument of each `Column(...)` call in
    `Datastore/SQL/ObjectFactories/*.py` (less `base.py` and `__init__.py`);
  - the top-level packages (a directory with an `__init__.py`).

  SGK's `EXTRA_NAMES` (the names its prompt 08 removed) are held under SGK.
- The script is run once. The log records its command, its output, and the file's size and SHA-256,
  and a second run must give the same bytes. A later re-measure adds a new file and repoints the
  guard; it never edits this one (as 04a's witness rule).
- `registry_words()` and `project_packages()` read the file:
  - **tables:** the union of the three registries' keys;
  - **identifier columns:** a column with an underscore, or with a capital and more than one
    character;
  - **packages:** the union of the packages, less `_NOT_PROJECT_PACKAGES`.

  The functions keep their names and return shapes.
- **Why one character.** SI has a column `N`, SGK has `G` and `T`, and the layer's prose says
  "shard #N" and "*N* shard files" (`SQL/schema.py:488`, `shard_paths.py:4`). A one-letter name
  cannot be told from prose, as SGK's docstring says of plain-word columns. The comment in the
  module says so.
- `_NOT_PROJECT_PACKAGES` is SGK's (`Datastore`, `RayTools`, `config`) plus `tools`, which is also
  `datastorekit.tools`; the comment says so. Without `tools`, six string hits come from the layer's
  own subpackage.
- `LAYER_WORDS`, `EXTRA_NAMES`, `FRAGMENTS` and `FLAG_PHRASES` are SGK's.
- **Measured by the planner** with this method, scanning the 20 files with SGK's three scanners:
  - 82 tables, 301 identifier columns, 16 packages, 398 words;
  - **no code-name hit, no string hit, and one comment hit**:
    `datastorekit/tools/shard_key_audit.py:188 wavenumber`, the comment U17 names.

**The pinned hits are exact in both directions.**
- A module constant `KNOWN_HITS` maps each scanning test's method name to its expected hits, each
  with its reason:
  - `test_no_comment`: `["datastorekit/tools/shard_key_audit.py:188 wavenumber"]`, frozen by rule 8
    until after 05, under `[01-package-prose-names-sgks-layout]`;
  - the other scans: empty.
- `assertNoHits(found)` keeps one assertion:
  `self.assertEqual(KNOWN_HITS.get(self._testMethodName, []), found, …)`. So a new hit fails, and so
  does a pinned hit that is no longer found. The skeleton is unchanged, and the port check sees no
  difference.

**The imports.** `import_allowed` allows the standard library, `ray`, `sqlalchemy`, and
`datastorekit` itself, except `datastorekit.tests`. `_ALLOWED_MODULES` is empty, since 01
internalised both of SGK's entries, and the comment says so. `test_the_allow_list` keeps its two
loops:
- allowed: `datastorekit.defaults`, `datastorekit._timing`, `datastorekit.SQL.factory_base`,
  `datastorekit.tools.shard_key_audit` and `sqlalchemy.exc`;
- refused: `datastorekit.tests.client.registry`, `datastorekit.tests.client.factories`,
  `config.datastore`, `CosmologyModels.model_ids` and `MetadataConcepts`.

This overlaps 01's `test_package_imports.py`. Both stay: 01's checks the whole package and the
fresh interpreter, and the guard checks the layer by its own definition.

**`test_the_vocabulary_holds_the_registry_and_the_packages`** keeps SGK's literals where the data
holds them: `{"BackgroundModel", "redshift", "tolerance"}` ⊆ tables, and
`{"model_serial", "parent_serial"}` ⊆ columns. It adds nothing. The package literal is R-value:
`tools` is now a layer word, so `{"CosmologyModels", "MetadataConcepts", "Caching"}`.

### 2.4 The two classes that ask the layer to load no client

SGK's `TestTheLayerKnowsNoProject` (`test_inventory_declarations.py:511-541`) and
`TestTheLayerImportsNoClient` (`test_layer_registry.py:643-686`) look for SGK's packages in
`sys.modules`. No client is on this repository's path, so ported literally they would pass whatever
the layer did. The client here is `datastorekit.tests.client`.
- **`PROJECT_PACKAGES`** (`test_inventory_declarations.py:488`) becomes `("datastorekit.tests",)`.
  The membership test, in the child's code and in the comprehension, reads `m ==
  p or m.startswith(p + ".")` for a `p` of it, in place of `m.split(".")[0] in …` (R-help). That
  is an expression, not control flow, and the log says so. `test_read_inventory_loads_only_what_the_registry_loads`
  imports the registry before its snapshot, as SGK's does, so the test asks that `read_inventory`
  load nothing more of the client.
- **`TestTheLayerImportsNoClient`:**
  - `LAYER_MODULES` and `LAYER_FILES` map by README §4;
  - `FORBIDDEN_MODULES` is `{"datastorekit.tests.client.registry",
    "datastorekit.tests.client.factories"}`;
  - the factory-directory test reads `m.startswith("datastorekit.tests")` with
    `ALLOWED_FACTORY_MODULES` empty;
  - `FORBIDDEN_PACKAGES` is the three clients' packages from the guard's data file, less
    `_NOT_PROJECT_PACKAGES`;
  - in `test_no_layer_file_imports_a_registry`, the `node.module == "config"` branch reads
    `"datastorekit.tests.client"`.
- **Probe both before relying on them.** Add `import datastorekit.tests.client.registry` to
  `store_inventory.py` (breakage (k)): both classes must fail.

### 2.5 `NOT_PORTED` (U16)

`compare_ported_tests.py` gains `NOT_PORTED`: a list of (package path, `Class.method`, reason).
Its one entry is `test_inventory_declarations.py`'s `TestResolve.test_the_report_renders_both_cosmology_types`,
"asserts on SGK's `tools.inventory_report`, which stays in SGK (README §1)".
- **The names rule.** The source's tests less `NOT_PORTED` equal the package's.
- **The skeleton rule.** A declared function is not compared.
- **A declared test that the package does define** is a difference.
- **A declared test that the source does not define** is a difference.
- **The report** prints each declared test and its reason, and the module's line gives the source
  count and the number not ported.

### 2.6 Closing `[04a-no-test-pins-a-second-parent-set-member]`

`datastorekit/tests/test_parent_set_members.py` (new; `NO_SOURCE` in `compare_with_source.py`)
uses 04a's fixture and holds two tests:
- one requires `Weave`'s `parent_sets["strands"]` to be `{"anchor": "Tessera", "origin":
  "Trace"}`, in that order;
- one varies `Weave_members` row 702's `origin_serial` with `vary_row`. It requires that `Weave`'s
  records change, that no other class's do, and that there is no problem.

Breakage (l), the `origin` member deleted from `Weave_factory.inventory_spec`
(`factories.py:1684`), must fail both. The issue moves to §4 with the measurement, and its index row
goes.

### 2.7 The modules, one by one

- **`test_inventory_declarations`.**
  - `ORDER` is §2.2's derived order (R-count).
  - The tables that declare no spec (`:115-117`) are `GadgetPart`, `Sample_tags` and
    `Sample_members`, by role.
  - `test_the_reader_refuses_a_registry_before_the_order_is` drops `Gadget`'s three tables.
  - The walk's field is `anchor` and its class `Weave`, with counts 1 and 1 (R-count). Its
    docstring describes them.
  - The cosmology tests read `FRAME_KINDS` and `FRAME_TYPES` from `datastorekit.tests.client.factories`
    (R-imp), and the classes `Gadget` and `Trace`.
  - §2.4 for the last class, and §2.5 for the report test.
- **`test_declared_facts`.**
  - `DECLARED` is §2.2's three. `bare_pool` keeps SGK's `NoShardKeyClass`.
  - `TestTheUnit` expects `Gadget`'s unit.
  - The hand-built registries (`Owner`, `Member`, `Flagged`, …) are client-free and unchanged.
  - §2.2's hazards 5–7.
- **`test_layer_registry`.**
  - `COMMAND_LINE_ORDER` is `list(registry.drop_groups)` as a literal, and its comment says that
    the neutral client has no command line (R-help).
  - `tables_to_drop`'s two examples use `samples` twice, then `gadgets` and `tesserae`.
  - `DROP` is `["Sample", "NotATable"]`.
  - The batch sizes name `GadgetPart` and `keypoint`.
  - The recorded-set test uses `routing_rule` and `keypoint`.
  - §2.2's hazard 8, and §2.4.
- **`test_drop_refuses_dangling_references`.**
  - `MEASURED` is §2.2's dependents, in the registry's group order.
  - The three structural tests use the rows of §2.2's map: `Sample` → `Tessera`; `Sample_members`;
    `Sample_tags` behind `Sample`.
  - §2.2's hazard 9.
- **`test_layer_is_generic`**: §2.3.

### 2.8 The checks

**`compare_ported_tests.py`:**
- `PORTED` gains the five pairs;
- `NOT_PORTED` is added, as §2.5 says;
- `NAME_MAP` is unchanged.

**`compare_with_source.py`:**
- `FILES` gains the five as `PORTED`;
- `NO_SOURCE` gains `test_parent_set_members.py`;
- the data file is not a `.py` file, and needs nothing;
- 01's, 02's, 03a's, 03b's and 04a's counts do not change.

**Applied to SGK's five** with the port check's own functions:

| Module | Tests | Classes | Functions compared | Assertions |
|---|---|---|---|---|
| `test_inventory_declarations` | 26 | 4 | 27 | 62 |
| `test_declared_facts` | 25 | 11 | 26 | 64 |
| `test_layer_registry` | 20 | 9 | 22 | 93 |
| `test_drop_refuses_dangling_references` | 11 | 2 | 13 | 48 |
| `test_layer_is_generic` | 8 | 4 | 9 | 17 |

After the port, the package side gives the same, except `test_inventory_declarations`: 25 tests,
26 functions compared, 57 assertions. U16's test's skeleton is `assertNotIn, assertEqual, subTest,
assertIn, assertEqual`, five items.

**The run count**, per module, by `unittest`'s loader: 25, 25, 20, 11, 8 and 2.

### 2.9 The records

- `[01-package-prose-names-sgks-layout]`: re-measure by log 03a §8's method, first reproducing 146
  lines in 35 files at `1a54af1`. Record the new count, and the lines the five modules add.
  Update its index hook.
- `[04a-no-test-pins-a-second-parent-set-member]`: closed, per §2.6.
- `docs/OPEN_ISSUES.md`: 7 open now, and 6 after, unless the work opens one.

---

## 3. Verification

1. `./venv/bin/python -m unittest discover -s datastorekit/tests -t .` gives `Ran 444 tests …
   OK`. The 353 are still there by name.
2. `compare_ported_tests.py` exits 0 over twenty modules, with one test declared not ported. Its
   whole output goes in the log.
3. `compare_with_source.py` exits 0, with 31 compared, 20 `PORTED` and 10 with no source (61
   tracked `.py` files). Its whole output goes in the log.
4. The loader's run counts are those of §2.8.
5. **The vocabulary.**
   - `grep -nwE` for log 02 §1.2's 80 client names finds none in the four other modules or in
     `test_parent_set_members.py`. Only the guard and its data file hold them, and the log gives
     their counts.
   - The second grep of 04a's §3.5, over the same files, finds nothing outside prose ported
     unchanged.
   - SGK's five hold the 80 names on 33, 22, 31, 54 and 2 lines.
6. **The data file**, measured twice, gives the same bytes. Its summary equals §2.3's: 82 tables,
   301 identifier columns, 16 packages and 398 words. If it differs, the log says why.
7. **The breakage record.** Each item is a diff exactly as applied, with what failed. None is
   committed. Record each diff with its trailing context lines, and check it with `git apply
   --check` as recorded.
   - **The checks:**
     - (a) one assertion deleted from a `test_declared_facts` test: `compare_ported_tests.py`
       exits 1, naming it;
     - (b) the `NOT_PORTED` entry removed: it exits 1, naming the test as missing from the package;
     - (c) U16's test added back to the package module (a stub that asserts): it exits 1;
     - (d) the guard module removed from `FILES`: `compare_with_source.py` exits 1.
   - **The layer, through the ported tests:**
     - (e) no roots-first step in `inventory_classes` (`store_inventory.py:964`, `order` starts
       empty): `TestTheDerivedOrder` fails;
     - (f) `dependent_tables` follows one level only (a `break` after `gone |= more`,
       `SQL/schema.py:380`): `TestDependentTables` fails;
     - (g) an `owner_column` with no foreign key accepted (`SQL/schema.py:211`, `n != 1` made
       `n > 1`): `test_an_owner_column_with_no_foreign_key` fails;
     - (h) `_unit_tables` ignores a declared owner (`SQL/ShardedPool.py:2144`, `and False`):
       `TestTheUnit` and `TestThePruneRefusalNamesItsUnit` fail.
   - **The guard:**
     - (i) a client word added to a layer comment (`# GkSource` in `store_reader.py`): `test_no_comment`
       fails, naming the line;
     - (j) the pinned comment reworded (`shard_key_audit.py:188`, "wavenumber" removed):
       `test_no_comment` fails, the pinned hit missing;
     - (k) `import datastorekit.tests.client.registry` added to `store_inventory.py`:
       `test_every_import_is_allowed` and §2.4's two classes fail;
     - (m) the data file's tables emptied for all three clients:
       `test_the_vocabulary_holds_the_registry_and_the_packages` fails.
   - **The issue:** (l) the `origin` member deleted (`factories.py:1684`): both tests of
     `test_parent_set_members` fail.
   - For (e)–(m), name every test that fails, and say whether its SGK counterpart pins the same
     line. A mutation that fails nothing is a finding: open a §3 issue for it.
8. `black --check` (25.1.0) is clean on everything under `datastorekit/` and `docs/extraction/`.

---

## 4. Acceptance

1. The five modules are ported under their names, with U16's one test declared not ported, and
   both checks pass.
2. The guard holds §2.3's vocabulary as data, and pins exactly §2.3's one hit.
3. `test_parent_set_members` closes `[04a-no-test-pins-a-second-parent-set-member]`.
4. §3.1–§3.8 hold.
5. **The records**, in the same commit:
   - the log, `logs/04b-port-the-declaration-and-registry-tests.md`, per README §5.1. It also has:
     - **the port table:** one row per test (89), giving its SGK origin, the kinds of change made
       to it, and the SGK classes it uses with their neutral counterparts; and U16's test with its
       reason;
     - the map as used (§2.2), with each "by role" choice and every row the agent changed, and why;
     - what the agent found for each of §2.2's ten hazards;
     - every R-count literal, before and after, and how it was measured;
     - the guard: the data file's command, commits, size, SHA-256 and second run; the vocabulary
       summary; the scan's hits; `KNOWN_HITS`;
     - both checks' whole output, and the loader's run counts;
     - the test count before (353) and after (444);
   - the board: §1's row for 04b and the header; §3 and §4 per §2.9;
   - `docs/OPEN_ISSUES.md`, per §2.9;
   - `prompts/INDEX.md`: the campaign's line.

---

## 5. Stop conditions — stop and ask the user

- A ported test would need an assertion removed, replaced or added, its name changed, or its
  control flow changed, beyond §2.3 and §2.4. A test that cannot be expressed on the neutral client
  is recorded, not dropped, and the user decides.
- A test needs a change to `datastorekit/tests/client/`, to the fixture, or to any module 02–04a
  ported.
- The guard finds a hit other than §2.3's one, or misses that one. Do not add a hit to
  `KNOWN_HITS`, and do not change the vocabulary's rule, to make it pass.
- A ported test fails on the neutral client, and passing it would need a change to the layer. That
  may be a real defect: record what fails, and ask.
- `compare_with_source.py`, `compare_ported_tests.py` or the stand-in pool would need a change
  outside §2.8.
- Anything would start Ray, open a store outside a `tempfile` directory, or edit, run, import or
  open a store of SGK, ChamPBH or StochasticInstantons. Reading their files through `git show`,
  which the measuring script does, is the only access allowed.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `datastorekit/tests/test_inventory_declarations.py`, `test_declared_facts.py`,
    `test_layer_registry.py`, `test_drop_refuses_dangling_references.py` and
    `test_layer_is_generic.py` (ported);
  - `datastorekit/tests/test_parent_set_members.py` (new);
  - `datastorekit/tests/data/client_vocabulary.json` (new);
  - `docs/extraction/measure_client_vocabulary.py` (new);
  - `docs/extraction/compare_ported_tests.py` and `compare_with_source.py`, as §2.8 says;
  - the log, this board, `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.
- It changes nothing else:
  - no file under `datastorekit/` outside `tests/`;
  - nothing in `datastorekit/tests/client/`;
  - none of `standin_pool.py`, `shard_store_fixtures.py`, `real_store_fixtures.py` or
    `schema_description.py`;
  - neither the witness nor the modules 01–04a ported;
  - none of `PROVENANCE.md`, `pyproject.toml` or the repository's `README.md`.
- It does not rewrite the layer's prose, so the pinned hit stays. U17's list is emptied when the
  prose is rewritten after 05.
- It fixes nothing in the layer, including the inherited issues and
  `[02-an-unsupplied-sharded-table-raises-keyerror]`.
- It writes no orchestration note and makes no tag.

---

## 7. The log and the board

`logs/04b-port-the-declaration-and-registry-tests.md`, using README §5.1, with the additions of §4.5.

`IMPLEMENTATION_STATE.md`: §1's row for 04b (landed, commit, log), the header, §3 and §4.
