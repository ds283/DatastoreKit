# Orchestrator — prompt 04a, port the store and inventory tests

Read [`../README.md`](../README.md) first: §0.2, §2 (rows 04a and 04b), §4, §5 and §6.2 (U9–U18).
Then read [`prompt-03b.md`](prompt-03b.md) §0's "Conventions", which this note keeps unless it says
otherwise, and the board's review of 03b, above all its observations and "Hand on to 04's author"
(§4 of 03b's note).

**You do not write code.** You may:
- run the suite, both checks and the tests the log names;
- replay the log's deliberate-breakage diffs with `git apply`, and revert them;
- run an in-process check or a probe from the session scratchpad, never committing one;
- read SGK through `git -C /Users/ds283/Documents/Code/SecondaryGWKit show 6f7f291:<path>`;
- fix small residue in a follow-up commit of your own (§4).

**The prompt:** [`04a-port-the-store-and-inventory-tests.md`](../04a-port-the-store-and-inventory-tests.md)
**Closes:** nothing · **Narrows:** nothing · **Changes:** `[01-package-prose-names-sgks-layout]`
(its count) · **Opens:** only what the work finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- 03b landed (`0d5380c`) and its review is recorded (`2992945`). 04a is written (`86640bf`).
  U14–U17 are taken, and U18 was taken on 2026-10-08 at this note's writing (§0, correction 1).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- SGK's `Datastore/`, `tools/`, `utilities.py` and `config/` (`defaults.py`, `sharding.py`,
  `datastore.py`) are unchanged from `6f7f291` to SGK `HEAD` (`b510bc9`, 2026-10-07). The prompt
  reads SGK at `6f7f291` regardless.
- One prompt at a time in this checkout. 04b is not written; it must not run beside 04a.

## 0. What makes this prompt unusual

**It is the campaign's largest prompt, and most of its weight is in one fixture.**
- **Four modules port much as 03a's did.** `test_store_schema`, `test_store_reader`,
  `test_foreign_key_check` and `test_schema_builder` re-fixture onto the ported fixture and the
  neutral witness.
- **`test_store_inventory` and `real_store_fixtures` are designed together.** SGK's test asserts
  about 200 facts of SGK's hand-built store; the ported fixture holds new, neutral rows; and the
  test's four data tables (`INVENTORY_CLASSES`, `VALUE_TABLES`, `IDENTITY`, `NON_IDENTITY`) are
  re-derived from those rows (R-count as a whole). The port check sees the assertions, not
  whether the rows give them meaning. So the review measures the rows: that each identity field
  has a row to vary to, that each fact a test asserts is true of the rows for the reason SGK's was.
- **The client changes for the second time** (U15, and U18 below): six tables by addition, a
  warning in `Gadget_factory`, and one line removed from `Sample`'s `inventory_spec`. The ripple
  reaches 02's literals, the contract and `build_store`, which 03a's and 03b's modules use. The
  review checks that it stops at the literals named.
- **A witness is captured** for the first time in this repository, and SGK's rule (never
  regenerated) starts to bind here.

**What moves on purpose:**
- five ported modules and two ported fixtures under `datastorekit/tests/`, and the witness under
  `datastorekit/tests/data/`;
- additions to `client/objects.py`, `factories.py`, `registry.py` and `build.py`; the warning in
  `Gadget_factory._validate_row`; `write_every_class`; and U18's one line;
- measured literals of `test_neutral_client.py`, and client columns of `docs/client-contract.md`;
- `PORTED` and `FILES` in the two checks;
- the records.

Nothing under `datastorekit/` outside `tests/` changes. Neither do `standin_pool.py`,
`shard_store_fixtures.py`, `client/reader.py`, or 03a's and 03b's nine modules.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-08 at `86640bf` (package files
as at `2992945`, unchanged since) and SGK `6f7f291`. Pass them on. Each is STRUCTURALLY REQUIRED,
and the log says so.

1. **U18: `Sample`'s `inventory_spec` drops `validated`.** `TestTheFullStore.test_classes_with_tags_validated_and_values`
   (SGK `test_store_inventory.py:386-416`) requires, of every record of every class, that it has
   a validated flag *and* a value count, or neither: `validated` is the tagged classes less
   `QuadSourceIntegral` and `OneLoopIntegral`, and for those it asserts `assertIsInstance(record.validated,
   bool)` and `assertIsNotNone(record.value_count)`, for the rest `assertIsNone` of both. Every SGK
   class keeps that rule. The neutral `Sample` does not: its spec declares
   `validated="sample_validated"` (`factories.py:1225`) and no `values`, so on `build_store` its
   four records carry a `bool` and `value_count` `None`. No literal of the test makes it pass with
   `Sample` in the store, and §2.4 requires `Sample` rows there. Hazard 3 saw the role, not the
   test. **The user took U18 on 2026-10-08** (README §6.2):
   - delete that one line. The column, `register()`, `validate`, `validate_on_startup` and the
     pool's prune are unchanged;
   - `Trace` (U15) is then the sharded class whose flag the inventory reads, and `Sample` plays
     SGK's `QuadSourceIntegral` in that test: tagged, no inventory flag, no values. So
     `validated` there is the tagged classes less `Sample` and `Weave`, and the "unvalidated rows
     are recorded" tuple (`:415`, SGK's three classes) holds `Gadget` and `Trace` (R-count; the log
     says so);
   - **probed** (the line deleted on `86640bf`, the suite run, the tree restored): of the 268, only
     `test_neutral_client.TestRoundTrip.test_the_reader_and_the_inventory_read_every_class` fails,
     on the expected flags of the four Samples (`test_neutral_client.py:561-569`), which become
     `None`. That literal is one §2.3 now allows. Any other failure of 02's, 03a's or 03b's tests
     from it is a stop;
   - `docs/client-contract.md:119` (the inventory's `validated` row) names `Gadget`, `Trace` in
     its client column. The registry's and the factory's docstrings say the same, if they say
     anything;
   - §2.3's "change by addition only, apart from the warning and `write_every_class`" gains this
     one deletion. §5's second and third stop conditions read with it allowed.
2. **`NON_IDENTITY` has 40 entries, not 39** (`ast`, `:264-311`). The three categories the client
   lacks are **19** entries, not 18: compute-target labels 9 (`:265-274`), solver serials 6
   (`:290-296`) and descriptive names and labels 4 (`:297-301`). The other three categories are
   payload and provenance 14, version foreign keys 5 and the OR-flags 2. `IDENTITY` holds the
   prompt's 93 entries over 21 classes; `INVENTORY_CLASSES` 21 and `VALUE_TABLES` 7.
3. **Hazard 1's figures.** Re-run three times each at `86640bf`: `build_store`'s two dial settings
   came out serials 1 and 501 at both 2 and 3 shards. What varies is the sharded serials and their
   shards: `Sample` holds 1, 2, 21 and 22 at 2 shards, with 21 and 22 changing shard between runs,
   and 1, 21, 22 and 41 at 3. The conclusion stands: `build_store` cannot stand for the fixture.
4. **Line numbers.** `stop_Tprime` is at `test_store_schema.py:152`, `:164`, `:191`, `:341`,
   `:343`, `:345` and `test_store_reader.py:231`, `:234`, `:236` (the prompt's "`:236`" is the
   reader's). `RealStore` is at `:196` (its decorator at `:195`). `TestStandinStore` is
   `test_foreign_key_check.py:208-283`.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **(l), a class of rows the test needs, emptied.** In the fixture, give `FULL_SHARDED_ROWS` no
  `Weave` row (and so none of its tags or members), and run `test_store_inventory`: name what
  fails. At least `test_every_class_has_a_record` must. This shows that the test reads the
  fixture's rows, not a literal copied from them. Record it with (d)–(k).
- **(m), the port check sees a fixture function that starts to assert.** This is (b) of §3.6,
  applied to `schema_description.py` as well as `real_store_fixtures.py`: both must make
  `compare_ported_tests.py` exit 1, "not in the source, and asserts".
- **Breakage (h) already bites.** Probed at `86640bf`: `read_only_url` without `mode=ro`
  (`store_reader.py:114`) fails 03b's `test_every_connection_is_opened_read_only` and
  `test_the_backstop_a_flag_update_on_a_hit`. So (h) is not a "fails nothing" finding, whatever the
  five modules do. The log names every test that fails, and says which, if any, of the five do.
- **Prefer classes that avoid hazard 2.** `Trace` is sharded, tagged, validated, with values and
  no parent set, so a copy of a `Trace` without member rows is still a duplicate. Where SGK's
  `TestDuplicates` uses `QuadSourceIntegral`, `Trace` plays it with the least R-help; if the agent
  uses `Sample` or `Weave` instead, the member rows are copied as hazard 2 says, by a helper, and
  the test body's control flow stays SGK's. `test_other_tags_are_not_a_duplicate` copies the row
  in its own body (`:1040-1048`), so it needs a class with no parent set. The log says which class
  played each test.
- **A second vocabulary grep, with the prompt's list.** §3.5's second grep (`CosmologyModels`,
  `CosmologyConcepts`, `ComputeTargets`, `extract_common`, `config\.`, `Planck2018`, `k_inv_Mpc`,
  `log10_tol`, `cosmology_type`, `cosmology_serial`, `model_serial`, `Run_fixture`) matches SGK's
  seven files on 33, 1, 2, 1, 1, 50 and 1 lines. Imports inside test bodies are among them
  (`from config.sharding import replicated_tables`, `test_store_inventory.py:419`;
  `store_inventory_tables`, `:530-534`). Each hit after the port is prose ported unchanged
  (03a §2.1) or a finding.

**The facts, checked by the orchestrator.** Pass them on.

- **The prompt's survey holds** at `86640bf` and SGK `6f7f291`:
  - module lengths 1,090, 492, 375, 291 and 180; the fixtures 1,350 and 211;
  - tests by `ast`, per class in file order: 42 (6, 3, 2, 2, 6, 5, 3, 4, 5, 4, 2), 13 (3, 1, 1, 3,
    4, 1), 15 (5, 2, 2, 5, 1), 8 (5, 2, 1) and 7 (5, 2). No class inherits a test across modules;
  - the SGK line numbers of §2.1 (`:56-78`, `:81`, `:83-91`, `:95-261`, `:264-311`, `:566`,
    `:580`, `:589`, `:593`, `:1069-1070`; `test_store_reader.py:337-338`), §2.2's hazards
    (`:406`, `:408-413`, `:442-445`, `:527`, `:821`), §2.7's (`test_store_schema.py:62`, `:151`,
    `:166`; `test_store_reader.py:220`, `:228`, `:241`, `:255`; `test_foreign_key_check.py:62-97`)
    and `BackgroundModel.py:752`, after correction 4;
  - the package line numbers of (d)–(i): `store_inventory.py:133` (`return float.hex(value)`),
    `:658` (`if len(orphans) > 0:`), `:880` (`… if len(where) > 1}`), `SQL/schema.py:468`
    (`if len(absent) > 0:`), `store_reader.py:114` and `SQL/schema.py:131` (`index=True` in the
    prepended `version` column); `factories.py:804` is `Gadget_factory._validate_row`;
  - hazard 9: 10 `def inventory_spec` in `factories.py` for 11 inventory classes, and 12 for 13
    after §2.3;
  - none of the six table names, their columns (`trace_label`, `step_count`, `trace_validated`,
    `trace_serial`, `step_index`, `step_value`, `weave_label`, `weave_serial`, `origin_serial`),
    the group `traces` or the field `strands` occurs as a word under `datastorekit/` or `docs/`.
- **The hazards, probed** from the scratchpad on `build_store` and a stand-in pool:
  - **hazard 2 holds.** A `Sample` copied on its shard with its tags and no member rows gives
    `empty-parent-set: Sample: 1 row(s) on shard #0 have no member rows …`; with its member rows
    copied too, `duplicate: Sample: 1 key-and-tag set(s) are held by more than one record`;
  - **hazard 6 holds, for the tables SQLAlchemy writes.** On SQLite 3.53.4 (the venv's), `DROP
    COLUMN` refuses an indexed column ("error in index … no such column") and a column named by a
    table-level `FOREIGN KEY` ("unknown column … in foreign key definition"), and drops a plain
    one. (A column-level `REFERENCES` is dropped; the schema does not write one.)
  - **hazard 10 holds.** `cluster.open_pool`, the controller set to the second shard id (shard
    ids iterate 2, 0, 1, so the controller is 0), `get_keypoint(pool, 0.5)`, `get_alias`, then
    `object_store(build.make_sample_on(alias, gadget_serial=1))`: `PRAGMA foreign_key_check`
    gives `[('Sample', 1, 'Gadget', 0)]` on the holder (shard 2) and nothing elsewhere; every shard
    holds keypoint 1 and alias 1; Ray is not initialised;
  - **the inventory on `build_store`** reads 11 classes. `Gadget` records carry a flag and a
    count, `Sample`'s a flag and no count (correction 1), and the rest neither.
- **The checks applied to SGK's seven**, with the port check's own functions and an empty name
  map. After the port, the package side must give the same:

  | Module | Tests | Classes | Functions compared | Assertions |
  |---|---|---|---|---|
  | `test_store_inventory` | 42 | 12 | 44 | 127 |
  | `test_store_schema` | 13 | 8 | 17 | 64 |
  | `test_store_reader` | 15 | 6 | 17 | 65 |
  | `test_foreign_key_check` | 8 | 4 | 8 | 25 |
  | `test_schema_builder` | 7 | 4 | 8 | 29 |
  | `real_store_fixtures` | 0 | 1 | 0 | 0 |
  | `schema_description` | 0 | 0 | 0 | 0 |

  Every test class's bases are module-local (`_Stores`, `_TempDir`, `_PoolTestCase`, `_TempStore`,
  `_TempDirCase`, or `unittest.TestCase`).
- **The vocabulary.** The 80 names match SGK's five on 284, 25, 9, 34 and 12 lines, as §3.5 says,
  and the two fixtures on 102 and 0. In the package today they match only the frozen comment
  `tools/shard_key_audit.py:188` (U17's, 04b's).
- **The prose issue** stands at 124 lines in 28 files at `86640bf`, by log 03a §8's method,
  reproduced by the orchestrator (the same script gives 114 in 23 at `72cf34a`). SGK's seven hold
  up to 37 lines the pattern matches (8, 3, 4, 2, 4, 6 and 10), some of them code in strings that
  R-imp rewrites (`test_store_inventory.py:1069`, `test_store_reader.py:337`). The agent first
  reproduces 124 in 28, then measures after, and the log gives both. `test_schema_builder`'s
  docstring is SGK's witness history (`:1-40`), naming SGK's witness files and campaigns: prose,
  ported unchanged.
- **The toolchain.** `venv/` from 01: Python 3.12.15, `ray==2.43.0`, `sqlalchemy==2.0.39`,
  `black==25.1.0`, SQLite 3.53.4, the package installed editable. It needs no change.
- **Expected counts.**
  - The suite is **268** before (`Ran 268 tests … OK`, re-run by the orchestrator at `86640bf`),
    and **353** after.
  - `compare_with_source.py` exits 0 before, with 31 files compared, 8 `PORTED` and 9 with no
    source (48 tracked `.py` files under `datastorekit/`). After: 31, 15 and 9 (55). It scans
    `.py` files only, so the witness is not an unaccounted file.
  - `compare_ported_tests.py` exits 0 over 8 modules before, and 15 after; the eight's counts do
    not change.
  - The index is **6**, and stays 6 unless the work opens an issue.
- **Ray.** No Ray process was up at writing (`pgrep -lf 'gcs_server|raylet|ray::'` empty).

**What the review exists to establish.**
- **(E1) The names.** The five modules hold SGK's `Class.method` sets and class bases, with no
  rename; the fixtures keep SGK's public names and signatures. The 268 are still there by name.
- **(E2) The port check.** Its only change is `PORTED` (seven pairs). It exits 0 over fifteen
  modules with the table's counts. (a), (b), (m) make it exit 1, and (c) makes
  `compare_with_source.py` exit 1.
- **(E3) The meaning.** Each test's control flow is SGK's. Each kind in the port table is honest.
  R-value and R-count keep SGK's distinctions: what a test varies is an identity field, what it
  deletes is the row it names, and what it expects to change changes for SGK's reason.
- **(E4) The client.** §2.3's six tables and the warning, U18's line, and the literals named; 02's,
  03a's and 03b's modules otherwise unchanged and passing.
- **(E5) The fixture.** Transcribed mechanics; neutral rows with the properties §2.4 lists;
  `references()` derived; no assertion.
- **(E6) The witness.** Captured twice, byte-identical, from a tree with §2.3 and U18 applied, and
  it is what `test_schema_builder` reads.
- **(E7) The layer through the tests.** (d)–(i) each fail the tests the log names; (j), (k) and (l)
  likewise. A mutation that fails nothing has a §3 issue.
- **(E8) The records.** The log, with the prompt's §4.4 additions; the board's §1 and §3;
  `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.

**Conventions.** 03b's note's, unchanged, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff with `git apply --check` and `-R --check` **as recorded in the log**,
  with its trailing context lines, and replay it in `bash`;
- read SGK only through `git show`, and never import or run SGK's fixtures;
- use a subdirectory of the session scratchpad, never `/tmp`, and put **no scratch `.py` under
  `datastorekit/`**, since the import guard and `compare_with_source.py` scan it;
- start no Ray;
- a stop goes to the user;
- check `git log` before committing.

One addition: **work in this order, and run the suite after each step.**
1. The client: the six tables, the warning, U18's line, `write_every_class`, and the literals of
   `test_neutral_client.py` and the contract. Run 02's, 03a's and 03b's modules unchanged.
2. `schema_description.py`, then the witness, captured twice, before `test_schema_builder` is
   ported.
3. `real_store_fixtures.py`: the mechanics, then the default rows, with `test_store_schema` and
   `test_store_reader`.
4. `test_foreign_key_check` and `test_schema_builder`.
5. The full rows, designed with `test_store_inventory`, which is ported last.

A ripple of the client change then shows up before any port depends on it, and the full rows are
designed against the four modules that read the default rows already passing.

**Addendum (2026-10-08), after the agent's first stop.** Correction 5, STRUCTURALLY REQUIRED, the
user's U19 (README §6.2).

5. **03a's `test_an_interrupted_store` drops `traces` too.** With §2.3 applied, `Weave` names a
   `Tessera` (its `anchor`, and `Weave_members.anchor_serial`), so the layer refuses to drop
   `aliases` and `tesserae` without the `traces` tables. `test_reconcile_at_open.py:1108-1114`
   passes `tables_to_drop(["samples", "aliases", "tesserae"])`; add `"traces"` to that list
   (R-count: the list is aliases' dependents, measured over the registry). The docstring's list of
   those dependents may gain `traces`. No other line of 03a's or 03b's modules changes; the port
   check's counts for `test_reconcile_at_open` stay 148 in 52 functions, and
   `compare_with_source.py` still accounts for it as `PORTED`. This is the one exception to "03a's
   and 03b's modules are not edited" (§2.3, §6), and the log lists it with the client's ripple.
   The review's checks 1 and 7 read with it allowed.

**Addendum (2026-10-08), after the agent's second stop.** Two more corrections, the user's U20 and
U21 (README §6.2).

6. **U20, STRUCTURALLY REQUIRED: the witness is of the classes with a table.** The client's
   `ephemeral_probe` registers `None`. Its record differs between `build_schema` (no `insert` key)
   and the actor (`"insert": None`), so no one witness matches both, and
   `test_actor_adds_only_the_inserters` raises `KeyError` on it (reproduced by the orchestrator:
   2 failures and 1 error of 7). `test_schema_builder`'s registry, and the registry
   `schema_description.actor_with_built_schema` and its `__main__` use, are
   `{n: f for n, f in registry.factories.items() if f.register() is not None}` (R-help, as 03a's
   `REPLICATED`). Capture the witness again, twice, from that registry; the first capture is
   superseded and is not committed. The log records both captures, the superseded one's SHA-256,
   and why. No assertion changes.
7. **U21, IMPLEMENTATION CHOICE at the user's direction: the witness history.** In
   `test_schema_builder`'s module docstring, rewrite the run from "The current one is …" to the end
   of SGK's witness history (SGK `:16-35`) so that it names `schema_at_extraction-04a.json` as the
   current witness, captured by this prompt, and says that SGK's earlier witnesses are SGK's
   history and are not copied (§2.5). The rest of the docstring is ported unchanged. The log quotes
   the sentence before and after.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone.
2. **The baseline.** The suite gives `Ran 268 tests … OK`, and both checks exit 0.
3. **SGK.** `git -C SecondaryGWKit diff --stat 6f7f291 HEAD -- Datastore tools utilities.py
   config/defaults.py config/sharding.py config/datastore.py` is empty.
4. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`.
5. **The index.** 6 now, and 6 after unless the work opens an issue. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`, and logs 02,
  03a and 03b;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's four corrections and five additions. Correction 1 is
the one most likely to be missed: without it, `test_classes_with_tags_validated_and_values`
cannot pass, and the agent would take the failure for a stop.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/04a-port-the-store-and-inventory-tests.md`, in
  README §5.1's form, with the prompt's §4.4 additions.
- **The files it may add or change are the prompt's §6 list, and nothing else**, plus any issue
  the work opens. It must not touch:
  - any file under `datastorekit/` outside `tests/`;
  - `standin_pool.py`, `shard_store_fixtures.py`, `client/reader.py`, or 03a's and 03b's modules;
  - `PROVENANCE.md`, `pyproject.toml`, `README.md`, `CLAUDE.md` or the campaign README;
  - anything under `orchestrator/`.
- **It edits no client repository, and runs no client code.** It reads SGK through `git show`,
  and transcribes from SGK's fixtures without importing them.
- **It runs no build, and starts no Ray.**
- **Stop and ask** on any of the prompt's §5 conditions, read with correction 1.

## 3. The review — eleven checks

1. **Scope.** `git show --stat <commit>` touches only the prompt's §6 list and the records. No file
   under `datastorekit/` outside `tests/`. No change to `standin_pool.py`,
   `shard_store_fixtures.py`, `client/reader.py`, or 03a's and 03b's modules. No `venv/`,
   `*.egg-info`, `__pycache__` or scratch file.
2. **E1, the names.** Independently of the agent's script, by `ast`: per module, the set of
   `Class.method` and each class's bases equal SGK's at `6f7f291`. The fixtures define every
   public name of §2.4, and each function's parameter list (names, order, defaults) equals SGK's.
   The 268 are unchanged by name from `86640bf`.
   `./venv/bin/python -m unittest discover -s datastorekit/tests -t .` gives `Ran 353 tests …
   OK`. The loader gives 42, 13, 15, 8 and 7 per module.
3. **E2, the port check, by reading.** `git show <commit> -- docs/extraction/compare_ported_tests.py`
   adds seven pairs to `PORTED` and changes nothing else. `compare_with_source.py` changes only in
   `FILES`.
4. **E2, by running.** Both checks exit 0. The port check's counts equal §0's table, and the
   eight earlier modules' counts are unchanged. `compare_with_source.py` gives 31, 15 and 9, with
   02's totals unchanged. Replay (a)–(c) and (m), one at a time, in `bash`; each exits 1 and names
   what the prompt says. Then two of the orchestrator's own:
   - delete one `assertIn` from `TestTags.test_a_tag_no_row_carries_is_only_a_store_tag`. It must
     exit 1, naming the test;
   - remove `real_store_fixtures.py`'s `RealStore` class. It must exit 1, "class missing from the
     package".

   `git status` is clean after each.
5. **E3, R-map, R-value and R-count, by reading.** Read the word diff of each module against SGK,
   after R-imp:
   - in full: `test_foreign_key_check`, `test_schema_builder`, `TestTheFullStore`, `TestTags`,
     `TestValueCounts`, `TestReplicatedDivergence`, `TestOldStoresAndOrphans` and `TestDuplicates`;
   - at least `TestSchemaDifferences` and `TestADifferingSchemaIsRefused` of the rest.

   Check:
   - each changed literal against the port table's kind;
   - that the expected `changed(...)` sets of `TestTags` follow the neutral references, and that
     each extra class in them is there for SGK's reason (a parent's tag reaching a child's
     identity);
   - that the divergence tests use a replicated class with no replicated dependents (hazard 5);
   - that the two tables `missing_tables` gives are still in reverse declaration order;
   - that `test_the_added_row_is_not_satisfied_by_coincidence` still holds for its reason (§2.7);
   - that correction 1 and §0's additions are applied as stated.
6. **E3, control flow, by measuring.** From the scratchpad, by `ast`, compare each function of the
   five modules and the two fixtures with its SGK counterpart, as at 03b's check 6: the sequence
   of `If`, `For`, `While`, `With` (with its item count), `Try`, `Return`, `Raise`, `Break`,
   `Continue`, conditional expressions, comprehensions, lambdas and nested `def`s. Every difference
   is named in the log and is R-help. The fixture's row builders are new data and are compared by
   name only; its mechanics (§2.4's line ranges) are compared in full. Any other difference is a
   finding.
7. **E4, the client.**
   - `objects.py`, `factories.py`, `registry.py` and `build.py` change by addition, apart from the
     warning, `write_every_class` and U18's one deleted line, which is the only line removed.
   - The registry: the six after `Sample_members` in `factories`; `"Trace": "k"` and
     `"Weave": "k"` in `sharded_tables`; the group `traces`; `replicated_tables`,
     `read_table_config`, `serial_batch_sizes` and `__all__` unchanged.
   - `Trace`'s frame `Parent` uses the same `FRAME_TYPES` object as `Gadget`'s (`is`, from the
     scratchpad).
   - `test_neutral_client.py`'s diff is measured literals only (`MEASURED_DEPENDENTS`, `counts`,
     the Sample flags of correction 1, and any other the log names and justifies).
   - The contract's diff is in client columns only.
   - 02's tests pass by name, and 03a's and 03b's modules are byte-identical to `86640bf`, and
     pass.
8. **E5, the fixture.**
   - Diff `_write_primary`, `_insert_rows`, `_write_shard`, `build_real_store`,
     `expected_row_counts`, `independent_row_counts`, `file_state`, `with_rows`, `fill_required`,
     `full_rows`, `_write_full_shard`, `build_full_store`, `relabel_serials`, `find_row` and
     `vary_row` against SGK's, after R-imp. Each difference is named in the log.
   - From the scratchpad, on `build_full_store` in a `tempfile` directory: every table has a row;
     every timestamp is `FIXED_TIMESTAMP`; every tagged record carries the run tag and one tag
     carries none; each `part_count` and `step_count` equals its rows (hazard 7);
     `read_inventory` reports no problem; `PRAGMA foreign_key_check` is empty on every shard; and
     the log's row counts per table are right.
   - Print `references()`, and check it against the schema's foreign keys and the specs' parents
     by hand.
   - Pick five `IDENTITY` entries and two `NON_IDENTITY` entries, and vary each with `vary_row`:
     each identity change changes its class's records, and each non-identity change changes none.
9. **E6, the witness.** Recapture it from a scratch copy of the commit's tree, by the log's
   command, and compare byte for byte. Its size and SHA-256 are the log's. `test_schema_builder`'s
   `WITNESS` names it, and no SGK witness is in the tree.
10. **E7, the layer and the client.** Replay (d)–(l), one at a time. Check that the tests that
    fail are the log's. Read one failing test for each, and check that it fails on an assertion or
    the layer's own exception, not on a broken fixture. If any mutation fails nothing, its §3 issue
    is open.
11. **E8, the records.**
    - The log has every section of README §5.1 and each §4.4 addition:
      - the port table, 85 rows;
      - the map as used, with the "by role" choices and the class that played each duplicate test;
      - the eleven hazards;
      - the six tables, U18's line, and every literal and contract line changed;
      - the fixture's row counts and the derived `references()` map;
      - the four data tables: rule, count before and after, and the absent categories (19);
      - the witness: command, tree, size, SHA-256 and the second capture;
      - both checks' whole output and the loader's counts;
      - 268 → 353;
      - (a)–(m).
    - The board: 04a's row, the header, and the prose issue's new count with the reproduction of
      124.
    - The index: count its rows, and check that the header matches. `prompts/INDEX.md`: the
      campaign's line.
    - `black --check` (25.1.0) is clean on `datastorekit/` and `docs/extraction/`. Ray is not
      running, and each module's `tearDownModule` holds.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 04a* paragraph, in the form
  of 03b's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README's header, and its §2 status for 04a;
  - the notes line, with this note marked "used for 04a";
  - any breakage diff of the log that does not apply as recorded, regenerated from the tree.
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Hand on to 04b's author:**
  - the client now has 22 classes, and U18 took `Sample`'s inventory flag. Any literal 04b
    measures over the registry, `build_store` or the full rows (its drop, declaration and
    registry tests) is measured after 04a;
  - `Trace` and `Gadget` share `FRAME_TYPES`, and `Weave`'s member field `anchor` shares a key
    parent's name, for `test_both_referencing_factories_declare_the_one_map` and SGK's
    `numeric` test (`test_inventory_declarations.py:375-418`);
  - hazard 1's finding, from the log: `build.build_store` does not stand for SGK's fixture, and
    04b's four modules that use the fixture use the port;
  - the witness rule: 04b changes no schema, so it captures no witness;
  - anything the review found about the port check's blind spots.
- **Report to the user:**
  - what landed, and the count 353;
  - the client change, U18, and its ripple;
  - the fixture's design, and its row counts in brief;
  - the port check over fifteen modules, and (a)–(c), (m) and the orchestrator's two breakages
    biting;
  - the control-flow comparison, and anything it found;
  - (d)–(l), with the tests each fails;
  - the prose issue's new count;
  - that 04b can now be written.
