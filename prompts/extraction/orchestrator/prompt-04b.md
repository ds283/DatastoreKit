# Orchestrator — prompt 04b, port the declaration and registry tests

Read [`../README.md`](../README.md) first: §0.2, §2 (rows 04b and 05), §4, §5 and §6.2 (U14–U21).
Then read [`prompt-04a.md`](prompt-04a.md) §0's "Conventions", which this note keeps unless it says
otherwise, and the board's review of 04a, above all "Where the note was wrong" and the issue it
opened.

**You do not write code.** You may:
- run the suite, both checks and the tests the log names;
- replay the log's deliberate-breakage diffs with `git apply`, and revert them;
- run an in-process check or a probe from the session scratchpad, never committing one;
- read SGK, CPBH and SI through `git -C /Users/ds283/Documents/Code/<repo> show <commit>:<path>`;
- fix small residue in a follow-up commit of your own (§4).

**The prompt:** [`04b-port-the-declaration-and-registry-tests.md`](../04b-port-the-declaration-and-registry-tests.md)
**Closes:** `[04a-no-test-pins-a-second-parent-set-member]` · **Narrows:** nothing · **Changes:**
`[01-package-prose-names-sgks-layout]` (its count) · **Opens:** only what the work finds ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- 04a landed (`7ceed25`) and its review is recorded (`1a54af1`). 04b is written (`a80af57`).
  U16 and U17 are taken; U18–U21 were applied by 04a.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- Nothing outside `prompts/` and `docs/OPEN_ISSUES.md` has changed from `7ceed25` to `a80af57`.
- SGK's `Datastore/`, `tools/`, `utilities.py` and `config/` (`defaults.py`, `sharding.py`,
  `datastore.py`) are unchanged from `6f7f291` to SGK `HEAD` (`b510bc9`). CPBH's `HEAD` is
  `52142d7` and SI's is `00d254e`, the commits the prompt names. SI's `Datastore/SQL/Datastore.py`
  and `Datastore/SQL/ObjectFactories/` are unchanged from log 02's `96d0562` to `00d254e`.
- One prompt at a time in this checkout. 05 is not written.

## 0. What makes this prompt unusual

**Four modules port as 04a's did; the fifth is new in kind.**
- `test_inventory_declarations`, `test_declared_facts`, `test_layer_registry` and
  `test_drop_refuses_dangling_references` re-fixture onto the client and 04a's fixture. Their
  literals measured over the registry are R-count, and §2.2 of the prompt measured them all.
- **`test_layer_is_generic` becomes the package's guard.** For the first time, a file of the
  package holds client words, on purpose, as data. The review checks that the data came from the
  three clients by `git show` alone, that the rule which turns it into a vocabulary is the prompt's,
  and that the pinned hit is exact in both directions.
- **Two classes would pass vacuously** if ported literally (§2.4). The review checks that each
  can fail.
- **The first `NOT_PORTED`** in the port check (U16). The review checks that a declared omission
  is checked both ways.
- **The client, the fixture and the earlier modules do not change.** The prompt's §2.2 says the
  client plays every role. Any change to them is a stop.

**What moves on purpose:**
- five ported modules and `test_parent_set_members.py` under `datastorekit/tests/`;
- `datastorekit/tests/data/client_vocabulary.json`, and `docs/extraction/measure_client_vocabulary.py`;
- `PORTED`, `NOT_PORTED` and the not-ported rules in `compare_ported_tests.py`; `FILES` and
  `NO_SOURCE` in `compare_with_source.py`;
- the records.

Nothing under `datastorekit/` outside `tests/` changes. Neither do `datastorekit/tests/client/`,
`standin_pool.py`, `shard_store_fixtures.py`, `real_store_fixtures.py`, `schema_description.py`,
the witness, or the modules 01–04a ported.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-08 at `a80af57` (package files
as at `7ceed25`, unchanged since), SGK `6f7f291`, CPBH `52142d7` and SI `00d254e`. Pass them on.
Corrections 1 and 5 change what the agent writes, and are STRUCTURALLY REQUIRED. Corrections 2–4
correct what the prompt expects; the log records them as found.

1. **Breakage (k) goes at the end of `store_inventory.py`.** `client/factories.py:37` imports
   `InventorySpec`, `Parent` and `ParentSet` from `datastorekit.store_inventory`. With
   `import datastorekit.tests.client.registry` among the module's imports (probed after line 106),
   the import is circular: `import datastorekit.store_inventory` raises `ImportError` ("partially
   initialized module"), and every test that imports the layer errors, which says nothing.
   Appended as the module's last line, the import completes, and the registry is in
   `sys.modules`. The log records (k) in that form.
   - **Probed:** (k) appended at the end, the 353 give `Ran 353 tests … OK`. 01's import guard
     allows `datastorekit` as a whole, so today nothing catches (k). Only 04b's tests can.
   - **What "both classes fail" means.** `test_read_inventory_loads_only_what_the_registry_loads`
     imports `store_inventory` before its snapshot, and so, under (k), the registry too; it cannot
     fail on (k), in SGK or here. Of `TestTheLayerKnowsNoProject`, expect
     `test_reading_records_loads_no_project_module` to fail. Of `TestTheLayerImportsNoClient`,
     expect `test_a_fresh_interpreter_loads_no_client_registry` and
     `test_no_layer_file_imports_a_registry`. With `test_every_import_is_allowed`, that is four.
     The log names what actually fails.
2. **Breakage (m) also fails `test_no_comment`.** `wavenumber` is an SGK table, not an identifier
   column. With every client's tables emptied it leaves the vocabulary, so the pinned hit is not
   found. Expect `test_the_vocabulary_holds_the_registry_and_the_packages` and `test_no_comment`.
3. **§2.3's "six string hits" are four**, on four lines: `tools/sharded_store.py:5`, `:6` and
   `:39`, and `tools/shard_key_audit.py:44`, each `python -m datastorekit.tools.…`. (The scanners
   report one hit per line and word.) The conclusion stands: `tools` joins `_NOT_PROJECT_PACKAGES`.
4. **The vocabulary summary counts before `LAYER_WORDS`.** By the prompt's method, the union of the
   three registries is **82** tables (80 after `LAYER_WORDS`, less `version` and `store_tag`), the
   identifier columns **301** (300 after it, less `tag_serial`), the packages **16** after
   `_NOT_PROJECT_PACKAGES` (20 before), and the forbidden words **398**, after all of them. The data
   file's summary and the log say which count is which. The one-letter columns are `C`, `G`, `N` and
   `T` (capitals), and `b`, `h` and `z`; the rule excludes the four capitals by length, and the
   three lower-case ones as plain words.
5. **`TestTheVersionObject`'s literal is R-value.** SGK's asserts
   `{"_my_id": 1, "_label": "standin", "_deserialized": True}`. The neutral version object's
   attribute is `label`: `vars(version)` is `{'_my_id': 1, 'label': 'standin', '_deserialized':
   True}`, read-write and read-only (probed). The port table says so.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **(n), a vacuous retarget.** In `test_inventory_declarations`, set `PROJECT_PACKAGES` to SGK's
  tuple (`"CosmologyModels"`, …, `"config"`) and apply (k): the class must then pass. Restore
  `PROJECT_PACKAGES`, apply (k) again: `test_reading_records_loads_no_project_module` fails. This
  shows that §2.4's retarget is what makes the class bite. Record it with (e)–(m).
- **(o), the guard reads its data, not a client.** Point the guard at a copy of the data file with
  `CosmologyModels` removed from every client's packages (a scratch copy, by
  monkeypatching the path from a scratch runner, never by editing the committed file):
  `test_the_vocabulary_holds_the_registry_and_the_packages` fails. If the guard's path cannot be
  pointed elsewhere without editing the module, say so and skip (o); do not add a hook for it.
- **(p), `NOT_PORTED` names a test the source lacks.** Change the entry's method name to one SGK's
  module does not define: `compare_ported_tests.py` exits 1 (§2.5's fourth rule). Record it with
  (a)–(d).
- **Run the measuring script twice from a clean tree**, and `cmp` the two outputs. The script reads
  only `git show` and `git ls-tree` at the three commits; `grep` it for `import` of a client,
  `sys.path`, `open(` on a client path and `subprocess` calls other than `git`. The log quotes the
  result.
- **Work in this order, and run the suite after each step.**
  1. `measure_client_vocabulary.py` and the data file; then `test_layer_is_generic`, with (i),
     (j), (k), (m) and (o).
  2. `NOT_PORTED` in the port check, with (b), (c) and (p); then `test_inventory_declarations`.
  3. `test_declared_facts` and `test_layer_registry`.
  4. `test_drop_refuses_dangling_references`, then `test_parent_set_members`.

  The guard comes first because it is the part with no SGK precedent, and the rest of the work
  must not add a hit to it.

**Addendum (2026-10-08), after the agent's stop.** Correction 6, STRUCTURALLY REQUIRED, the user's
U22 (README §6.2), and a ruling on one choice of the agent's.

6. **U22: two of `TestTheRecords`' tests build the schema of the classes with a table.** The note
   checked `ephemeral_probe` against the inventory (it declares no spec) but not against
   `build_schema`'s records, where it has a record with no table and none of the three declared
   keys (reproduced by the orchestrator: `22 != 21`, and `KeyError: 'owner_column'`). Add a module
   constant `WITH_A_TABLE = {n: f for n, f in factories.items() if f.register() is not None}` to
   `test_declared_facts`, and give it to the `build_schema` calls of
   `test_every_record_of_a_class_with_a_table_carries_the_three_keys` and
   `test_exactly_the_four_declarations_are_not_default` only (R-help, as U20's filter). No
   assertion, name or control flow changes; the port check's counts for the module stay 25, 26
   and 64. Every other test keeps the whole registry. The log records the stop, both probes (the
   module-wide filter that fails `TestTheVersionObject`, and this one), and U22. The review's
   checks 5 and 6 read with it allowed.
7. **`NOT_PORTED`'s fifth rule is kept**, at the user's direction (IMPLEMENTATION CHOICE): an entry
   naming a module that `PORTED` does not hold is a difference. The log states it beside §2.5's
   four, and the review's check 3 reads with it allowed.

**The facts, checked by the orchestrator.** Pass them on.

- **The prompt's survey holds** at SGK `6f7f291`, by the port check's own functions:

  | Module | Lines | Tests | Classes | Functions compared | Assertions |
  |---|---|---|---|---|---|
  | `test_inventory_declarations` | 545 | 26 (8, 10, 6, 2) | 4 | 27 | 62 |
  | `test_declared_facts` | 671 | 25 (3, 9, 2, 4, 2, 3, 1, 1) | 11 | 26 | 64 |
  | `test_layer_registry` | 692 | 20 (3, 2, 2, 3, 2, 5, 1, 2) | 9 | 22 | 93 |
  | `test_drop_refuses_dangling_references` | 307 | 11 (7, 4) | 2 | 13 | 48 |
  | `test_layer_is_generic` | 374 | 8 (3, 3, 2) | 4 | 9 | 17 |

  U16's test's skeleton is `assertNotIn, assertEqual, subTest, assertIn, assertEqual`, so the
  package side gives 25, 26 and 57 for the first. The bases: `_Model(DatastoreObject)`;
  `_TempDir(unittest.TestCase)` and five classes on it; `_LayerTestCase(unittest.TestCase)` and
  three on it; `TestThePruneRefusalNamesItsUnit(_PruneTestCase)`, the one cross-module base.
- **SGK line numbers** of §2.4 and §2.7 hold: `test_inventory_declarations.py:115-117`, `:375-418`,
  `:488`, `:511-541` (child code `:513-526`, `:532-539`); `test_layer_registry.py:624-629` and
  `:643-686`.
- **The package line numbers of (e)–(l)** hold at `7ceed25`: `store_inventory.py:964` (`order:
  List[str] = [name for name in specs if len(depends[name]) == 0]`); `SQL/schema.py:380` (`gone |=
  more`) and `:211` (`if n != 1:`); `SQL/ShardedPool.py:2144` (the `_declares_owner` branch of
  `_unit_tables`); `client/factories.py:1684` (`"origin": Parent("origin_serial", "Trace",
  nullable=True)`) and `:852` (`owned_serials`, reading `parts`); `tools/shard_key_audit.py:188`
  (the pinned comment); `SQL/schema.py:488` and `shard_paths.py:4` (the "N" prose).
- **§2.2's measurements**, re-probed from the scratchpad on `a80af57`:
  - the derived order, the plain sort (it puts `keypoint_alias` fourth), the seven roots, and no
    `inventory_spec` with a parameter. The classes with no spec are `ephemeral_probe` and the eight
    tag, value, step and member tables;
  - the registry less `Gadget`'s three: `ValueError`, "inventory_classes(): Sample references
    Gadget, which declares no inventory_spec"; `read_inventory` on the full store: `RuntimeError`
    naming `replicated_tables` and `['Gadget', 'GadgetPart']`;
  - `dependent_tables` of each group as §2.2 says, and of `["Gadget"]`: `Gadget_tags`,
    `GadgetPart`, `Sample`, `Sample_tags`, `Sample_members`;
  - `FRAME_KINDS`; `Gadget`'s and `Trace`'s `frame` parents are one object's (`is`), `of` `None`,
    `type_column` `frame_kind`; both kinds occur among each class's records, and
    `parent_types["frame"]` is `('frame_kind', {1: 'dial_setting', 2: 'knob_setting'})`;
  - `Weave`'s `parent_sets`; row 702 is `{'serial': 702, 'weave_serial': 1, 'anchor_serial': None,
    'origin_serial': 3}`;
  - the walk, SGK's `walk` with `anchor` and `Weave`: `{'records': 1, 'key': 1, 'member': 1,
    'no_digest': 0}`;
  - the record without `routing_rule`: not replicated, count 6 against 3, problems `['duplicate']`;
    `keypoint` replicated and its records unchanged;
  - the version object (correction 5).
- **The hazards, probed:**
  - **hazard 7 holds.** `_PruneTestCase`, the trigger on `"Gadget"` deleting the least
    `dial_setting`, `prune_unvalidated=True`, three runs: `"dial_setting" lost rows [(1,)], and a
    prune of "Gadget" deletes only from ['Gadget', 'GadgetPart', 'Gadget_tags']`. (`_unit_tables`
    itself gives `['Gadget', 'Gadget_tags', 'GadgetPart']`; the message is in the specs' order, as
    SGK's comment says.)
  - **hazard 8 holds.** A registry less `Weave` and `Weave_tags` cannot open: SQLAlchemy's
    `NoReferencedTableError` on `Weave_members.weave_serial`. Less all three, the stand-in pool
    opens three shards, each with `Trace`, `Trace_tags` and `TraceStep` and no `Weave` table.
  - **hazard 9 holds.** On the full store, `tables_to_drop(["tesserae"])` is refused: `cannot drop
    ['Tessera'] alone: the rows of ['Sample', 'Sample_tags', 'Sample_members', 'Weave', 'Weave_tags',
    'Weave_members'] would name rows that are gone, so they must be dropped too. Nothing was
    opened`. `tables_to_drop(["tesserae", "samples", "traces"])` has no dependents, opens, and
    leaves its ten tables present and empty on both shards.
- **The guard, measured.** A scratch copy of the prompt's measurement (registry keys by `ast`;
  `Column(...)` first arguments over `Datastore/SQL/ObjectFactories/*.py` less `base.py` and
  `__init__.py`, 21, 17 and 22 files; top-level directories with an `__init__.py`, by `git ls-tree`)
  gives correction 4's counts. SGK's three scanners, run from a copy of SGK's guard with that
  vocabulary over the 20 layer files, give no code-name hit, no string hit, and the one comment hit
  `datastorekit/tools/shard_key_audit.py:188 wavenumber`. Without `tools` excluded: correction 3.
  The import scan, with the prompt's `import_allowed`, finds nothing, and the allow-list's five and
  five hold. `{"model_serial", "parent_serial"}` are columns, and `Caching` is SI's package.
- **The vocabulary grep.** The 80 names match SGK's five on 33, 22, 31, 54 and 2 lines, and in
  the package only `tools/shard_key_audit.py`.
- **The prose issue** stands at 146 lines in 35 files, as 04a's review reproduced it; nothing it
  counts has changed since `7ceed25`.
- **The toolchain.** `venv/` from 01: Python 3.12.15, `ray==2.43.0`, `sqlalchemy==2.0.39`,
  `black==25.1.0`, SQLite 3.53.4, the package installed editable. It needs no change.
- **Expected counts.**
  - The suite is **353** before (`Ran 353 tests … OK`, re-run by the orchestrator at `a80af57`), and
    **444** after. The loader gives 25, 25, 20, 11, 8 and 2 for the six new modules.
  - `compare_with_source.py` exits 0 before, with 31 compared, 15 `PORTED` and 9 with no source (55
    tracked `.py` files under `datastorekit/`). After: 31, 20 and 10 (61). The data file is not a
    `.py` file, and `measure_client_vocabulary.py` is not under `datastorekit/`.
  - `compare_ported_tests.py` exits 0 over 15 modules before, and 20 after, with one test declared
    not ported; the fifteen's counts do not change.
  - The index is **7**, and **6** after, unless the work opens an issue.
- **Ray.** No Ray process was up at writing (`pgrep -lf 'gcs_server|raylet|ray::'` empty).

**What the review exists to establish.**
- **(E1) The names.** The five modules hold SGK's `Class.method` sets and class bases, less U16's
  one test, with no rename. The 353 are still there by name.
- **(E2) The port check.** `PORTED` gains five pairs; `NOT_PORTED` is added with §2.5's four rules
  and nothing else changes. It exits 0 over twenty modules. (a), (b), (c) and (p) make it exit 1,
  and (d) makes `compare_with_source.py` exit 1.
- **(E3) The meaning.** Each test's control flow is SGK's, apart from §2.4's expression. Each kind
  in the port table is honest; each R-count literal was measured, not translated.
- **(E4) The guard.** Its data came from the three clients by `git show` at the named commits and
  is reproducible byte for byte; its rule is §2.3's; it pins exactly one hit; it imports no client
  and reads no registry.
- **(E5) The two retargeted classes bite** ((k), (n)).
- **(E6) The issue.** `test_parent_set_members` fails on (l), and the issue moves to §4.
- **(E7) The layer through the tests.** (e)–(m) each fail the tests the log names. A mutation that
  fails nothing has a §3 issue.
- **(E8) The records.** The log, with the prompt's §4.5 additions; the board's §1, §3 and §4;
  `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.

**Conventions.** 04a's note's, unchanged, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff with `git apply --check` and `-R --check` **as recorded in the log**,
  with its trailing context lines, and replay it in `bash`;
- read SGK, CPBH and SI only through `git show` and `git ls-tree`, and never import or run their
  code;
- use a subdirectory of the session scratchpad, never `/tmp`, and put **no scratch `.py` under
  `datastorekit/`**, since the import guard, the new guard and `compare_with_source.py` scan it;
- start no Ray;
- a stop goes to the user;
- check `git log` before committing.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone.
2. **The baseline.** The suite gives `Ran 353 tests … OK`, and both checks exit 0.
3. **The clients.** `git -C SecondaryGWKit diff --stat 6f7f291 HEAD -- Datastore tools
   utilities.py config/defaults.py config/sharding.py config/datastore.py` is empty;
   `git -C ChamPBH cat-file -t 52142d7` and `git -C StochasticInstantons cat-file -t 00d254e` are
   `commit`.
4. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`.
5. **The index.** 7 now, and 6 after unless the work opens an issue. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`, and logs 02,
  03a and 04a;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's five corrections and four additions. Correction 1 is
the one most likely to cost time: (k) placed among the imports breaks every test, and the agent
could take that for the guard working.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/04b-port-the-declaration-and-registry-tests.md`, in
  README §5.1's form, with the prompt's §4.5 additions.
- **The files it may add or change are the prompt's §6 list, and nothing else**, plus any issue
  the work opens. It must not touch:
  - any file under `datastorekit/` outside `tests/`;
  - `datastorekit/tests/client/`, `standin_pool.py`, `shard_store_fixtures.py`,
    `real_store_fixtures.py`, `schema_description.py`, the witness, or the modules 01–04a ported;
  - `PROVENANCE.md`, `pyproject.toml`, `README.md`, `CLAUDE.md` or the campaign README;
  - anything under `orchestrator/`.
- **It edits no client repository, and runs, imports or opens nothing of one.** It reads them only
  through `git show` and `git ls-tree`, at the three commits.
- **It runs no build, and starts no Ray.**
- **Stop and ask** on any of the prompt's §5 conditions. A guard hit other than the pinned one is a
  stop, not an entry for `KNOWN_HITS`.

## 3. The review — twelve checks

1. **Scope.** `git show --stat <commit>` touches only the prompt's §6 list and the records. No file
   under `datastorekit/` outside `tests/`; nothing in `datastorekit/tests/client/`; no change to the
   fixtures, the stand-in pool, the witness or the 01–04a modules. No `venv/`, `*.egg-info`,
   `__pycache__` or scratch file.
2. **E1, the names.** Independently of the agent's script, by `ast`: per module, the set of
   `Class.method` and each class's bases equal SGK's at `6f7f291`, less U16's one test. The 353 are
   unchanged by name from `a80af57`.
   `./venv/bin/python -m unittest discover -s datastorekit/tests -t .` gives `Ran 444 tests …
   OK`. The loader gives 25, 25, 20, 11, 8 and 2.
3. **E2, the port check, by reading.** `git show <commit> -- docs/extraction/compare_ported_tests.py`:
   five pairs added to `PORTED`; `NOT_PORTED` with one entry and its reason; the names rule, the
   skeleton rule, the two "is a difference" rules and the report, as §2.5 says; nothing else.
   `compare_with_source.py` changes only in `FILES` and `NO_SOURCE`.
4. **E2, by running.** Both checks exit 0. The port check's counts equal §0's table (25, 26, 57 for
   the first module) and the fifteen earlier modules' are unchanged; the report prints U16's test
   and its reason. `compare_with_source.py` gives 31, 20 and 10. Replay (a)–(d) and (p), one at a
   time, in `bash`; each exits 1 and names what the prompt says. Then two of the orchestrator's own:
   - delete one `assertEqual` from `TestDependentTables.test_each_group_alone_needs_its_measured_dependents`.
     It must exit 1, naming the test;
   - remove `_LayerTestCase` from `test_layer_is_generic.py`. It must exit 1, "class missing from
     the package".

   `git status` is clean after each.
5. **E3, by reading.** Read the word diff of each module against SGK, after R-imp:
   - in full: `test_layer_is_generic`, `TestTheLayerKnowsNoProject`, `TestTheLayerImportsNoClient`,
     `TestDependentTables`, `TestThePoolRefuses`, `TestTheUnit`, `TestRevalidate`,
     `TestOwnedSerials` and `TestThePruneRefusalNamesItsUnit`;
   - at least `TestTheDerivedOrder`, `TestResolve` and `TestThePoolUsesItsRegistry` of the rest.

   Check:
   - each changed literal against the port table's kind, and each R-count literal against the
     log's measurement and §0's facts;
   - that §2.4's membership expression is the only change of form in the two retargeted classes;
   - that `test_exactly_the_four_declarations_are_not_default` keeps its name and compares three;
   - that the five corrections and four additions are applied as stated.
6. **E3, control flow, by measuring.** From the scratchpad, by `ast`, compare each function of the
   five modules with its SGK counterpart, as at 04a's check 6. Every difference is named in the log
   and is R-help. §2.3's `assertNoHits` keeps one assertion and no new branch; `registry_words` and
   `project_packages` keep their return shapes. Any other difference is a finding.
7. **E4, the data.**
   - Run `measure_client_vocabulary.py` again from a scratch copy of the commit's tree, by the log's
     command, and `cmp` with the committed file. Its size and SHA-256 are the log's.
   - Read the script: it reads the clients only by `git show` and `git ls-tree` at `6f7f291`,
     `52142d7` and `00d254e`; it imports nothing of them and changes no `sys.path`.
   - From the scratchpad, rebuild the vocabulary from the committed file by §2.3's rule and compare
     with this note's own measurement: 82 / 80 tables, 301 / 300 columns, 16 packages, 398 words.
     Each client's registry keys equal log 02 §1.2's lists.
8. **E4, the guard.**
   - It imports no client and nothing from `datastorekit.tests.client`; `grep` it.
   - `KNOWN_HITS` holds the one comment hit with its reason, and empty lists or no entry for the
     other scans.
   - `layer_files()` gives the 20 files; `AUDIT_LIST` is twelve, each in it.
   - `_NOT_PROJECT_PACKAGES` is SGK's three and `tools`, with the comment; `_ALLOWED_MODULES` is
     empty, with the comment.
   - With the guard's own functions, a word added to a layer string (not only a comment) is found:
     add `"GkSource"` to a docstring of `store_reader.py` and run `test_no_string_or_docstring`. It
     must fail, naming the line. Revert.
9. **E5, the two retargeted classes.** Replay (k) as correction 1 has it, and (n). Check the
   failing tests against the log and correction 1. Then a third, of the orchestrator's own: append
   `import datastorekit.tests.client.factories` to `store_reader.py`, and run
   `TestTheLayerImportsNoClient`: it must fail.
10. **E6, the issue.** Replay (l): both tests of `test_parent_set_members` fail, on assertions, not
    on a broken fixture. Read the two tests: the first compares the ordered member map; the second
    asserts that `Weave`'s records change, that no other class's do, and that there is no problem.
11. **E7, the layer.** Replay (e)–(j) and (m), one at a time. Check that the tests that fail are the
    log's. Read one failing test for each, and check that it fails on an assertion or the layer's
    own exception. If any mutation fails nothing, its §3 issue is open.
12. **E8, the records.**
    - The log has every section of README §5.1 and each §4.5 addition:
      - the port table, 89 rows, and U16's test with its reason;
      - the map as used, and every row changed;
      - the ten hazards;
      - every R-count literal before and after, with how it was measured;
      - the guard: command, commits, size, SHA-256, second run, the summary (correction 4), the
        hits and `KNOWN_HITS`;
      - both checks' whole output and the loader's counts;
      - 353 → 444;
      - (a)–(p).
    - The board: 04b's row, the header, `[04a-no-test-pins-a-second-parent-set-member]` in §4 with
      the measurement, and the prose issue's new count with the reproduction of 146 in 35. Reproduce
      the new count by log 03a §8's method.
    - The index: count its rows, and check that the header matches. `prompts/INDEX.md`: the
      campaign's line.
    - `black --check` (25.1.0) is clean on `datastorekit/` and `docs/extraction/`. Ray is not
      running.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 04b* paragraph, in the form
  of 04a's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README's header, and its §2 status for 04b;
  - the notes line, with this note marked "used for 04b";
  - any breakage diff of the log that does not apply as recorded, regenerated from the tree.
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Hand on to 05's author:**
  - the suite is 444, and 05 runs it at both ends of §0.2's version table. The guard's
    `_ALLOWED_ROOTS` is `sys.stdlib_module_names`, which differs between 3.12 and 3.13; a module
    the layer imports that one of them lacks would show there;
  - the two fresh-interpreter classes run `sys.executable` with `PYTHONPATH` at the repository
    root, and the CI workflow must allow that;
  - the data file is a measurement at fixed commits. 05 does not re-measure it; a later re-measure
    adds a new file (§2.3);
  - `KNOWN_HITS` holds one hit until the prose is rewritten after 05;
  - anything the review found about the port check's blind spots.
- **Report to the user:**
  - what landed, and the count 444;
  - the guard: its vocabulary, its one pinned hit, and the scans biting ((i), (j), (m), and the
    orchestrator's string probe);
  - the two retargeted classes biting ((k), (n));
  - the port check over twenty modules with U16's test declared, and (a)–(d) and (p) biting;
  - the control-flow comparison, and anything it found;
  - (e)–(m), with the tests each fails;
  - the issue closed, and the prose issue's new count;
  - that 05 can now be written.
