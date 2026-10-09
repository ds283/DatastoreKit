# Log 06 — version-keyed lookups, ready for `v0.2.0`

**Subject:** Add version-keyed lookups, ready for v0.2.0 · **Commit:** this commit ·
**Date:** 2026-10-09 · **Model:** Claude Opus 5.5 · **Result:** landed, untagged and unpushed
(U28).

A factory may now declare the optional `register()` key `key_on_version`. The actor then hands its
`build`, in a copy of every `object_get` payload, the serial of the version row the pool was opened
under, as `datastorekit.contract.VERSION_SERIAL_KEY`; the `build` filters on it through
`datastorekit.contract.require_version_serial`. An actor holds that **lookup serial** apart from
its insert serial: `set_version` sets both, and a read-only pool gives its actors the lookup serial
alone, through the new `Datastore.set_lookup_version` (U26), so a read-only actor still cannot
insert. The neutral client's `Tessera` is keyed (U25). A new module of 14 tests carries over the
semantics of CPBH's tests and covers the read-only route the source never had. The schema witness
moves to `schema_at_extraction-06.json`, which differs from 04a's by exactly the one key.
`pyproject.toml` is at `0.2.0`, and the README, `client-contract.md` §8, `PROVENANCE.md` and
`compare_with_source.py`'s docstring say so.

The suite goes from **444 to 458**, in `venv/` and at the high end. Of the 444, only the three
tests hazard 4 names moved, and only until the witness and `REGISTER_KEYS` were updated.
`compare_with_source.py` was run for the last time on the untouched tree (U27);
`compare_ported_tests.py` passes after. `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]`
is opened, not fixed.

**No tag was made and nothing was pushed (U28).** `v0.2.0` is made on this commit once CI has
passed at both ends here, after the review.

Prompt: [`../06-version-keyed-lookups.md`](../06-version-keyed-lookups.md), with the orchestrator's
dispatch note §0: five corrections, three additions, its measured facts and its conventions. Each
is followed as given; §2 classifies them.

## 1. What shipped

### 1.1 The layer (§2.1–§2.4)

- **`datastorekit/contract.py`**: `VERSION_SERIAL_KEY = "_version_serial"` (CPBH's value) and
  `require_version_serial(payload, cls_name) -> int`, under a comment saying what they are for. The
  function returns `payload[VERSION_SERIAL_KEY]`, and raises `RuntimeError` naming `cls_name` and
  the key, and saying that a keyed lookup goes through `Datastore.object_get` and is never made
  unfiltered, when the key is absent or `None`. The docstring gains one paragraph: the actor sets
  the key and refuses a caller's, so its name is the layer's. The module still imports nothing.
- **`datastorekit/SQL/schema.py`**: `_declared_key_on_version(cls_name, tab, registration_data)
  -> bool`, in the form of the three `_declared_*` helpers, called after them in `build_schema`.
  It refuses, with `_refuse_declaration`'s `ValueError`, a value that is not a `bool` ("which is
  not a bool"), and `True` on a class that does not register `"version": True`. The record of a
  class with a table holds `"key_on_version"`; the record of a class with no table is unchanged.
  `build_schema`'s docstring names the key beside the three declared facts.
- **`datastorekit/SQL/Datastore.py`**:
  - `_lookup_serial`, beside `_version_serial`, both `None` at construction, each with a comment;
  - `set_version` sets both, its checks and refusals unchanged, and its docstring says so;
  - **`set_lookup_version(serial)`**: `set_version`'s type check (`TypeError`) and its refusal of a
    change to a different serial (`RuntimeError`), on the lookup serial; it never sets
    `_version_serial`;
  - in `object_get`, after `payload_data` is formed and before the transaction, a record whose
    `key_on_version` is set (`.get(..., False)`) has its payloads replaced by
    `self._keyed_payloads(cls_name, payload_data)`;
  - **`_keyed_payloads`**: a `RuntimeError` if `_lookup_serial` is `None`, naming the class and the
    label and saying that the pool sets the serial with `set_version`, or with
    `set_lookup_version` on a read-only pool; for each payload, a `KeyError` naming the class and
    the key if it holds `VERSION_SERIAL_KEY`, and otherwise a copy, `{**p, VERSION_SERIAL_KEY:
    self._lookup_serial}`. Its docstring says that `object_read_batch`, `read_table`,
    `object_store` and `object_validate` are not keyed;
  - the read-only actor's comment gains one sentence: the pool gives it the lookup serial alone,
    which keys lookups and admits no insert.
- **`datastorekit/SQL/ShardedPool.py`**: in `_open_read_only`, after every actor's
  `read_only_state` has returned, `ray.get` of `set_lookup_version.remote(self._version.store_id)`
  on every actor, under a two-line comment. Step 6 of the read-only comment, and its "Afterwards"
  paragraph, each gain a sentence saying so. The read-write constructor is unchanged.

No file under `datastorekit/` other than these four, and the test files below, changed. The layer's
new prose names no client and no SGK path (§3, hazard 5; §7 item 3).

### 1.2 The neutral client (§2.5, U25)

- `Tessera_factory.register()` gains `"key_on_version": True`; its `build` adds `table.c.version ==
  require_version_serial(payload, "Tessera")` to its select; its insert is unchanged. Its
  docstring gains a sentence. `factories.py` gains one import line,
  `from datastorekit.contract import require_version_serial` (§2 item 9).
- `registry.py`'s roles table: `Tessera`'s row adds "`key_on_version` (prompt 06)".
- `test_neutral_client.REGISTER_KEYS` gains `"key_on_version"`.

No other client class, no fixture, `build_store`, the drop groups and `standin_pool.py` are
unchanged.

### 1.3 The witness (§2.6)

`datastorekit/tests/data/schema_at_extraction-06.json`, 74,450 bytes, SHA-256
`643128946640fcc4fba64fb1e650bfe320b3b41a169a7cba78e850a7e9bcddb8` (§5.3). `test_schema_builder`:
`WITNESS` names it, and the docstring's "The current one is …" sentence names it and keeps 04a's as
the earlier witness. `schema_at_extraction-04a.json` is unchanged.

### 1.4 The tests (§2.7): `datastorekit/tests/test_version_keyed_lookups.py`

14 tests in four classes; the loader gives 14. CPBH's tests are at CPBH `52142d7`,
`Datastore/tests/test_version_keyed_lookups.py`.

| # | Class · test | CPBH origin | What it shows |
|---|---|---|---|
| 1 | `TestThroughThePool` · `test_a_keyed_row_is_returned_only_under_its_own_label` | (a) `TestVersionKeyedLookups.test_a_scalar_model_is_returned_only_under_its_own_label` | A `Tessera` got under A is found again under A (`_new_insert` the first time only), is a new row under B, and is A's again when A is reopened; on disk two rows, one under each label's serial |
| 2 | 〃 · `test_the_vectorized_route_is_keyed_too` | (c3) `test_c3_vectorized_lookup_is_keyed_too` | The same through `object_get_vectorized` (`build.get_tesserae`), over two weights |
| 3 | 〃 · `test_an_unkeyed_versioned_class_keeps_one_row_across_labels` | (e) `test_e_parameter_tables_are_not_keyed` | `keypoint_alias` (versioned, replicated, not keyed) has one serial under A and B, and one row on every shard, under A's serial |
| 4 | 〃 · `test_a_read_only_pool_finds_the_rows_of_its_own_label` | new (U26) | Read-only under A finds A's Tessera, and under B finds B's, scalar and vectorized; no file changes |
| 5 | 〃 · `test_a_read_only_miss_under_another_label_is_refused` | new (U26) | A Tessera stored only under A, looked up read-only under B: `ReadOnlyWrite` naming `Tessera` and "an insert", "Nothing was written", no file or row changed |
| 6 | `TestTheActor` · `test_the_callers_payload_is_not_mutated` | (d2) `test_d2_payload_is_copied_and_the_reserved_key_is_the_datastores`, first half | `object_get(…, payload_data=[p])` leaves `p` equal to a copy taken before, without the key |
| 7 | 〃 · `test_a_caller_supplied_serial_is_refused` | (d2), second half | A payload holding `VERSION_SERIAL_KEY`: `KeyError` naming the key, no row written |
| 8 | 〃 · `test_a_keyed_lookup_before_the_serial_is_set_raises` | new | No serial set: a keyed get raises the actor's `RuntimeError` (naming `"Tessera"` and `set_lookup_version`), no file changes; a get of `gauge_setting` on the same actor returns a stored row |
| 9 | 〃 · `test_set_lookup_version_keys_lookups_and_admits_no_insert` | new (U26) | A row written by an actor given `set_version` is found by a second actor on the same file given only `set_lookup_version`, whose `_version_serial` stays `None`; that actor's miss is refused by `_insert`'s guard, and no row is written |
| 10 | 〃 · `test_a_keyed_build_without_the_serial_raises` | (d) `test_d_keyed_build_without_the_serial_raises` | `Tessera_factory.build` called directly with no key: `RuntimeError` naming `Tessera` and the key |
| 11 | `TestTheDeclaration` · `test_only_tessera_is_keyed` | (d3) `test_d3_only_the_compute_targets_are_keyed` | Of the registry's records, exactly `Tessera`'s has `key_on_version` true |
| 12 | 〃 · `test_key_on_version_without_a_version_column_is_refused` | (d4) `test_d4_key_on_version_needs_a_version_column` | `build_schema` raises `ValueError` naming the class and the key; with `"version": True` the same declaration is keyed |
| 13 | 〃 · `test_a_key_on_version_that_is_not_a_bool_is_refused` | new | `"key_on_version": "yes"`: `ValueError` naming the class, the key, and "not a bool" |
| 14 | `TestTheContract` · `test_require_version_serial` | new | `VERSION_SERIAL_KEY == "_version_serial"`; the serial returned; `RuntimeError` naming the class and the key when the key is absent or `None` |

**Not carried over.** CPBH's (b) `test_b_adiabatic_history_is_returned_only_under_its_own_label`,
(c1) `test_c1_failed_bbn_row_is_returned_only_under_its_own_label` and (c2)
`test_c2_successful_bbn_row_is_returned_only_under_its_own_label` test (a)'s semantics on three
classes of CPBH's own, and are (a)'s semantics on one neutral class here (test 1). (f)
`TestOneVersionLabel.test_f_scripts_import_the_label_and_define_none` parses CPBH's scripts, and
is about CPBH alone.

**How the tests are built.** Pools are opened as `test_version_row_at_open.open` and
`test_read_only_pool.open` open theirs: a `sp.StandinCluster()` made active, and
`sp.sp_mod.ShardedPool(version_label=…, …, factories=…)` with the registry, stdout redirected. The
actor tests (6–10) build `sp.DatastoreClass` directly on shard 0 of a store a pool made under A
(which holds the keypoint and alias and no Tessera), with a stand-in broker handle,
`sp.Handle(sp.BrokerClass(name="SerialPoolBroker"), "SerialPoolBroker", cluster, None)`, under the
active cluster (correction 2). Test 9's row is written by a second actor on the same file, given
`set_version`, sharing that broker (§2 item 8). Every store is in a `tempfile` directory; nothing
starts Ray, and `tearDownModule` checks it. The module docstring names no client.

### 1.5 The records of the contract and of provenance (§2.9)

- **`docs/client-contract.md`**: one italic paragraph under the header (§8 is measured at 06's
  tree; §1–§7 remain as at `8bc60a5`, so their line numbers into the four files 06 changes are that
  tree's), and **§8 "Version-keyed lookups (`v0.2.0`, prompt 06)"**: the key, the reserved payload
  key, `require_version_serial`, the two serials, the keyed get, the read-write and read-only
  pools, each with its lines at this commit; what is not keyed; a replicated keyed class (allowed,
  not exercised); and `Tessera` as the example. Nothing else changed.
- **`PROVENANCE.md`**: a section "After `v0.1.0`": `compare_with_source.py` describes `v0.1.0` and
  is retired there (U27); CPBH `52142d7` and the lines carried over (`Datastore/SQL/Datastore.py`
  `:328-338`, `:390`, `:500-509`, `:544-555`; `config/version.py:52-71`; the test module), each
  with where it went; what is new here (the lookup serial, U26); and the files 06 changes.
- **`docs/extraction/compare_with_source.py`**: one paragraph at the top of its docstring; nothing
  else.

### 1.6 The release (§2.10)

- `pyproject.toml`: `version = "0.2.0"`, nothing else.
- `README.md`: the status names `v0.2.0` and what it adds; the install line pins `v0.2.0`, with a
  sentence that `v0.1.0` remains for a client that has not adopted the key; "Using it" gains an
  item for `key_on_version`, naming `VERSION_SERIAL_KEY`, `require_version_serial` and
  `client-contract.md` §8 by anchor; "Developing" says that `compare_with_source.py` describes
  `v0.1.0` and is run on that tag only. §5.6 checks every name.

### 1.7 The records

This log; the board (header, §1's row, §2's G3 line, §3); `docs/OPEN_ISSUES.md` (7 → 8);
`prompts/INDEX.md`.

## 2. Deviations from the prompt

1. **Correction 1: the gate's "`main` equals `origin/main`" does not hold, and need not.** At
   dispatch `origin/main` was `fe040b2`, and `git rev-list --count origin/main..HEAD` gave **2**
   (`1f9941f`, `0e524b4`, both under `prompts/`). Nothing is pushed. **STRUCTURALLY REQUIRED.**
2. **Correction 2: the actor is `sp.DatastoreClass`, with a stand-in broker.** The prompt's
   §2.7 says `Datastore.__ray_actor_class__`; the suite reaches the actor as
   `standin_pool.DatastoreClass` (`Datastore.__ray_metadata__.modified_class`), and tests 6–10 use
   it. An actor with `serial_broker=None` cannot insert a class that takes a serial, so each is
   given a stand-in broker handle (§1.4). **STRUCTURALLY REQUIRED.**
3. **Correction 3: the witness holds no `ephemeral_probe` record.** Neither 04a's nor the new one
   does (U20), so §2.6's "`ephemeral_probe`'s record is unchanged" has nothing to compare; the
   no-table case is pinned by `test_declared_facts.TestTheRecords.test_a_record_with_no_table_is_unchanged`,
   which passes unchanged. Found as the orchestrator said: 21 additions and nothing else (§5.3).
   **STRUCTURALLY REQUIRED** (an expectation corrected).
4. **Correction 4: "22 subtests each" is 21 subtests and one failure of the test itself.** With
   the layer and `Tessera` changed and the witness and `REGISTER_KEYS` not yet: `Ran 444 tests` /
   `FAILED (failures=45)`: 22 `FAIL` lines for each witness test and one for
   `TestCoverageByDeclaration.test_every_register_key_is_declared_by_some_factory`; no error, and
   no other test (§5.1 run 2). **STRUCTURALLY REQUIRED** (an expectation corrected).
5. **Correction 5: breakages (a) and (c) reach fewer of the 444 than the prompt expects**: the
   five tests of `test_neutral_client.TestRoundTrip` and `test_read_only_pool`'s `setUpModule`
   (so `Ran 435`); (h) reaches exactly one of the 444; (i) none. Found so (§6).
   **STRUCTURALLY REQUIRED** (an expectation corrected).
6. **Addition 1: the semantics were probed before the tests were written** (§4.1). The outcomes
   are the orchestrator's: serial 1 under A twice, 3 under B, 2 and 4 by the vectorized route, the
   alias 1 under both, A reopened 1, read-only 1 under A and 3 under B, and `ReadOnlyWrite` for a
   read-only miss under B. **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
7. **Addition 2: the work followed the orchestrator's order**, with the suite run after each step
   that changes a file the suite reads (§5.1). **IMPLEMENTATION CHOICE**, at the orchestrator's
   direction.
8. **Addition 3: the probes are outside `datastorekit/`**, in `<scratch>/probe/`, each printing
   `datastorekit.__file__` (§4). **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
9. **`factories.py` gains an import line** outside `Tessera_factory`:
   `from datastorekit.contract import require_version_serial`, on a line of its own beside the
   module's other import from `contract`, so that the existing line is untouched. `build` cannot
   call the function without it. **STRUCTURALLY REQUIRED.**
10. **The refusal of `key_on_version` without a version column reads the registration**
    (`not registration_data.get("version", False)`), as CPBH's reads `use_version`, rather than
    looking for a column named `version` in the table: a factory's own column of that name, with
    no prepended `version`, carries no foreign key to the version table, and is not keyed.
    **IMPLEMENTATION CHOICE.**
11. **`set_version` gains no new refusal.** It sets the lookup serial beside the insert serial,
    with its present checks unchanged (§2.3). A `set_lookup_version(1)` followed by
    `set_version(2)` therefore moves the lookup serial to 2; no pool makes that sequence (§7
    item 1). **IMPLEMENTATION CHOICE** (the prompt's wording kept).
12. **The tests' details** the prompt left open: the labels `"A"` and `"B"`; test 1 also checks the
    rows on disk; test 3 also checks that `keypoint_alias` registers `version` and not the key, and
    its one row on every shard; test 4 compares each read-only result with what the read-write pool
    returned (so that breakage (i), which makes both A's, leaves it passing, as §4.7 expects),
    by both routes, and checks that no file changed; test 5 checks every file and row unchanged;
    test 8 checks the files unchanged; test 9 checks the reader's `_version_serial` directly; test
    12 also builds the same declaration with `"version": True`; the declarations of 12 and 13 use a
    test-local factory that makes its column afresh on each `register()` (a `Column` belongs to one
    table; the first draft reused one and raised SQLAlchemy's `ArgumentError`).
    **IMPLEMENTATION CHOICE.**
13. **The witness was captured a third time, at the high end**, byte-identical (§5.3).
    **IMPLEMENTATION CHOICE.**
14. **`uv`'s cache.** 05's cache (`<scratch05>/agent05/uv-cache`, in 05's session scratchpad) was
    copied into this session's scratchpad, `<scratch>/uv-cache` (401 MB), and every `uv` command but
    the first two ran with `UV_CACHE_DIR` there; every one ran `--offline`. The first `uv venv
    --offline` and `uv pip install --offline "ray==2.55.1" "sqlalchemy==2.0.46"` of `venv-high`
    read 05's cache in place, before the copy. Nothing was downloaded. **IMPLEMENTATION CHOICE.**
15. **The breakages ran in exports**, five at a time in parallel, each in its own fresh export of
    the staged tree, with `venv/`'s interpreter and `PYTHONPATH` set to the export, which
    `datastorekit.__file__` confirms (§6.1); so each run took about 140 s, against 85 s alone.
    **IMPLEMENTATION CHOICE.**

No UNINTENDED DRIFT was found.

## 3. The six hazards (§3)

1. **A probe imports the installed package, not a copy.** Every probe and capture printed
   `datastorekit.__file__` (§4, §5.3, §6). In the checkout the probes import the checkout (`venv/`'s
   editable install), which is the tree under test. The second witness capture and each breakage
   ran from a copy with `PYTHONPATH` set to it, and resolved to the copy.
2. **The witness.** The comparison by loading both files finds exactly 21 additions,
   `classes/<cls>/record/key_on_version`, `true` on `Tessera` and `false` on the other 20, and
   nothing else (§5.3).
3. **The read-only actor's third guard.** `set_lookup_version` never sets `_version_serial`: test 9
   checks it directly, and (j) fails test 9 (§6). `test_version_row_at_open`'s section 4
   (`TestInsertBeforeSetVersion`) passes unchanged in every run.
4. **A class that declares nothing.** With the layer and `Tessera` changed, exactly the three named
   tests moved (correction 4); after the witness and `REGISTER_KEYS`, `Ran 444 tests` / `OK` (§5.1).
5. **The guard.** `test_layer_is_generic` passes in every run, with `KNOWN_HITS` at its one entry
   (`datastorekit/tools/shard_key_audit.py:188 wavenumber`). `grep -rniE
   "champbh|cpbh|run-integrity|ScalarModel|BBNData" datastorekit` finds only the guard's own
   docstring and its vocabulary data, as before. Provenance is in `PROVENANCE.md`.
6. **Replicated keyed classes.** The keying is in the actor's `object_get`, which every shard's
   actor runs for a replicated get with its own lookup serial; every actor is given the one serial
   (`set_version` read-write, `set_lookup_version` read-only). `client-contract.md` §8 says that the
   route is allowed and not exercised by the suite; the client keys no replicated class.

## 4. The probes

Every probe is under `<scratch>/probe/`, where `<scratch>` is
`/private/tmp/claude-35086/-Users-ds283-Documents-Code-DatastoreKit/72bb2976-ab43-4ba4-976d-bf0b3ff49d79/scratchpad/agent06`,
run from the repository root with `PYTHONPATH` unset. None is committed.

### 4.1 The semantics (addition 1)

`env -u PYTHONPATH ./venv/bin/python <scratch>/probe/probe_semantics.py`, after the layer and
`Tessera` were changed, before the tests were written:

```
datastorekit.__file__ = /Users/ds283/Documents/Code/DatastoreKit/datastorekit/__init__.py
A: Tessera 1 1 new? True False
A: vectorized 0.75: [2] 2
A: alias serial 1
B: alias serial 1
B: Tessera 3 new? True
B: vectorized 0.75: [4]
A again: Tessera 1 new? False
RO A: 1
RO B: 3
A only: 5
RO B miss: ReadOnlyWrite Datastore "shard0002-store" was opened read-only, and an insert of "Tessera" would write to it (payload {'alias_serial': 1, 'tessera_weight': 0.5}). Nothing was written
ray initialised: False
```

### 4.2 The in-place update of `object_get_vectorized` (§2.8)

`env -u PYTHONPATH ./venv/bin/python <scratch>/probe/probe_vectorized_inplace.py`: two keypoints
and their aliases `a1` (serial 1) and `a2` (serial 2) on a store from `build.open_pool`; one list of
two payload dicts.

```
datastorekit.__file__ = /Users/ds283/Documents/Code/DatastoreKit/datastorekit/__init__.py
before: [{'weight': 0.25}, {'weight': 0.75}]
after the first call: [['k', 'weight'], ['k', 'weight']] k is a1: [True, True]
the list passed twice, same key: [1, 2] [1, 2]
the same dicts, another key: [2, 2] dicts now name alias [2, 2]
then pool.object_get(payload_data=...) on them goes to alias [2, 2]
ray initialised: False
```

The dicts gain `k` after the first call; reused with the same key they give the same rows; reused
with another key they are overwritten to it, and a later `pool.object_get(..., payload_data=…)`
routes them by it. Recorded as `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]`
(§8), with the impact measured here: the prompt's "sends them the first key" holds for a get
whose shard-key field differs, which the neutral client cannot show (every sharded class is
sharded on `k`), and not for a second vectorized get on the same field, which overwrites it.

### 4.3 The other probes

- `<scratch>/probe/compare_witnesses.py` (§5.3), run with `python3 -I`.
- `<scratch>/probe/release_check.sh` (§5.5), run from `<scratch>/outside-release`.
- `<scratch>/probe/readme_check.py` (§5.6), run with `./venv/bin/python`.
- `<scratch>/probe/make_breaks.py` and `<scratch>/probe/run_break.sh` (§6).

## 5. Verification performed

### 5.1 The suite

Each run is `<python> -m unittest discover -s datastorekit/tests -t .` from the repository root,
in the foreground, with `PYTHONPATH` unset, its output written to `<scratch>/out/` and the verdict
grepped from it.

| # | When | Venv | Verdict |
|---|---|---|---|
| 1 | at dispatch, before any change | `venv/` (`0.1.0`) | `Ran 444 tests in 82.914s` / `OK` |
| 2 | after the four layer files and `Tessera_factory` (step 2) | `venv/` | `Ran 444 tests in 81.486s` / `FAILED (failures=45)`: `test_build_schema_reproduces_the_witness` 22, `test_actor_build_schema_reproduces_the_witness` 22, `test_every_register_key_is_declared_by_some_factory` 1 |
| 3 | after the witness, `WITNESS`, the docstring sentence, `REGISTER_KEYS` and the roles row (step 3) | `venv/` | `Ran 444 tests in 80.997s` / `OK` |
| 4 | after `test_version_keyed_lookups.py` (step 4) | `venv/` | `Ran 458 tests in 84.271s` / `OK` |
| 5 | the high end (step 6) | `venv-high` (scratch) | `Ran 458 tests in 91.184s` / `OK` |
| 6 | after every change, `venv/` reinstalled at `0.2.0` (step 7) | `venv/` (`0.2.0`) | `Ran 458 tests in 85.767s` / `OK` |

**The count is 444 before and 458 after**, in `venv/` and at the high end. The new module gives
14 by the loader (`loadTestsFromName("datastorekit.tests.test_version_keyed_lookups")`,
`countTestCases()` → `14`). `ResourceWarning` lines: 0 in `venv/`, 186 at the high end
(`[05-a-refused-open-leaves-its-engines-undisposed]`; correction 4 of 05: the line count is not a
measurement).

### 5.2 The venvs

| Venv | Python | Ray | SQLAlchemy | SQLite | `datastorekit` |
|---|---|---|---|---|---|
| `venv/` | 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.43.0 | 2.0.39 | 3.53.4 | editable, the checkout; `0.2.0` after `./venv/bin/python -m pip install --no-deps -e .` (`Successfully uninstalled datastorekit-0.1.0`, `Successfully installed datastorekit-0.2.0`); `pip show`: `Version: 0.2.0` |
| `<scratch>/venv-high` | 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.55.1 | 2.0.46 | 3.53.4 | editable, the checkout, `0.2.0` |
| `<scratch>/venv-release` | 3.13.16 | 2.55.1 | 2.0.46 | — | the wheel of §5.5, not editable |

`venv-high` was made with `uv venv --offline --python /opt/local/bin/python3.13`, then `uv pip
install --offline --python <scratch>/venv-high/bin/python "ray==2.55.1" "sqlalchemy==2.0.46"`
and `uv pip install --offline --no-deps --python <scratch>/venv-high/bin/python -e .` (`uv`
0.12.20; §2 item 14). Its `uv pip freeze`: attrs 26.1.0, certifi 2026.7.22, charset-normalizer
3.5.2, click 8.5.0, datastorekit (editable, the checkout), filelock 4.0.12, idna 3.20, jsonschema
4.26.0, jsonschema-specifications 2025.9.1, msgpack 1.2.3, packaging 26.3, protobuf 7.36.2, pyyaml
6.0.3, ray 2.55.1, referencing 0.37.0, requests 2.34.2, rpds-py 2026.9.1, sqlalchemy 2.0.46,
typing-extensions 4.16.0, urllib3 2.8.0. `venv-release`: `uv venv --offline`, then `uv pip
install --offline --python <scratch>/venv-release/bin/python <the wheel> "ray==2.55.1"
"sqlalchemy==2.0.46"` (`Resolved 20 packages`). Every pin resolved offline.

### 5.3 The witness (§2.6)

**Capture 1**, from the checkout, with step 2's tree (`datastorekit.__file__` =
`/Users/ds283/Documents/Code/DatastoreKit/datastorekit/__init__.py`):

```
env -u PYTHONPATH ./venv/bin/python datastorekit/tests/schema_description.py datastorekit/tests/data/schema_at_extraction-06.json
```

**Capture 2**, from a fresh interpreter on a copy of the tree's `datastorekit/` (without
`__pycache__` and `data/`) at `<scratch>/treecopy`, run from there with `PYTHONPATH=.`
(`datastorekit.__file__` = `<scratch>/treecopy/datastorekit/__init__.py`):

```
PYTHONPATH=. /Users/ds283/Documents/Code/DatastoreKit/venv/bin/python -m datastorekit.tests.schema_description <scratch>/out/witness-capture2.json
```

`cmp`: **byte-identical**. **Capture 3**, at the high end, from the checkout with `venv-high`'s
interpreter: byte-identical too.

| | Bytes | SHA-256 |
|---|---|---|
| `schema_at_extraction-06.json` (captures 1–3) | **74,450** | `643128946640fcc4fba64fb1e650bfe320b3b41a169a7cba78e850a7e9bcddb8` |
| `schema_at_extraction-04a.json` (unchanged) | 73,842 | `c3536a2b0edf73cfbd3cf1fdc38d5135c5ba4f7edf9da257c9ff344ffb9bad6c` |

Both are the orchestrator's figures. **The comparison**, by loading both files and walking them
(`python3 -I <scratch>/probe/compare_witnesses.py <04a> <06>`), quoted whole:

```
added /classes/Gadget/record/key_on_version null -> false
added /classes/GadgetPart/record/key_on_version null -> false
added /classes/Gadget_tags/record/key_on_version null -> false
added /classes/Sample/record/key_on_version null -> false
added /classes/Sample_members/record/key_on_version null -> false
added /classes/Sample_tags/record/key_on_version null -> false
added /classes/Tessera/record/key_on_version null -> true
added /classes/Trace/record/key_on_version null -> false
added /classes/TraceStep/record/key_on_version null -> false
added /classes/Trace_tags/record/key_on_version null -> false
added /classes/Weave/record/key_on_version null -> false
added /classes/Weave_members/record/key_on_version null -> false
added /classes/Weave_tags/record/key_on_version null -> false
added /classes/dial_setting/record/key_on_version null -> false
added /classes/gauge_setting/record/key_on_version null -> false
added /classes/keypoint/record/key_on_version null -> false
added /classes/keypoint_alias/record/key_on_version null -> false
added /classes/knob_setting/record/key_on_version null -> false
added /classes/routing_rule/record/key_on_version null -> false
added /classes/store_tag/record/key_on_version null -> false
added /classes/version/record/key_on_version null -> false
differences: 21
top-level keys: ['class_order', 'classes', 'format', 'metadata_tables', 'table_order'] ['class_order', 'classes', 'format', 'metadata_tables', 'table_order']
classes: 21 21
ephemeral_probe in old/new: False False
```

Exactly the 21 records with a table gain `key_on_version`, `true` on `Tessera` and `false` on the
other 20; no table description, top-level key or other record field changes. Neither file has an
`ephemeral_probe` record (correction 3).

### 5.4 The two checks

**`compare_with_source.py`, its last run (U27)**, on the untouched tree at dispatch
(`./venv/bin/python docs/extraction/compare_with_source.py`): exit **0**. Its output:

```
source:  /Users/ds283/Documents/Code/SecondaryGWKit at 6f7f291e857265e429f5d6f810124fd3bf57ce55 Record the orchestrator's review of datastore-generic-followup prompt 03
package: /Users/ds283/Documents/Code/DatastoreKit/datastorekit
black:   25.1.0

Lines per file and class, as -source/+package: the source lines a class changed or
removed, and the package lines it accounts for.

file                                                        D-imp         D-str        D-tool        D-root         D-fix       D-split         D-int         D-fmt  UNCLASSIFIED
datastorekit/__init__.py                                        .             .             .             .             .             .             .             .             .
datastorekit/object.py                                          .             .             .             .             .             .             .             .             .
datastorekit/contract.py                                        .             .             .             .             .             .             .             .             .
datastorekit/replication.py                                     .             .             .             .             .             .             .             .             .
datastorekit/shard_paths.py                                     .             .             .             .             .             .             .             .             .
datastorekit/store_reader.py                                -3/+3             .             .             .             .             .             .             .             .
datastorekit/store_inventory.py                             -2/+2             .             .             .             .             .             .             .             .
datastorekit/SQL/__init__.py                                    .             .             .             .             .             .             .             .             .
datastorekit/SQL/schema.py                                  -2/+2             .             .             .             .             .             .             .             .
datastorekit/SQL/ShardedPool.py                           -13/+13             .             .             .             .             .             .             .             .
datastorekit/SQL/Datastore.py                               -9/+9             .             .             .             .             .             .             .             .
datastorekit/SQL/ClientPool.py                              -1/+1             .             .             .             .             .             .             .             .
datastorekit/SQL/SerialPoolBroker.py                            .             .             .             .             .             .             .             .             .
datastorekit/SQL/ProfileAgent.py                            -2/+2             .             .             .             .             .             .             .             .
datastorekit/SQL/factory_base.py                                .             .             .             .             .             .             .             .             .
datastorekit/tools/__init__.py                                  .             .             .             .             .             .             .             .             .
datastorekit/tools/sharded_store.py                         -1/+1             .         -7/+3             .             .             .             .             .             .
datastorekit/tools/shard_key_audit.py                       -1/+1             .         -5/+1             .             .             .             .             .             .
datastorekit/defaults.py                                        .             .             .             .             .             .       -202/+5             .             .
datastorekit/_timing.py                                         .             .             .             .             .             .        -20/+6             .             .
datastorekit/tests/__init__.py                                  .             .             .             .             .             .             .             .             .
datastorekit/tests/shard_store_fixtures.py                  -2/+2             .             .             .         -3/+3             .             .             .             .
datastorekit/tests/test_shard_paths.py                      -1/+1         -2/+2             .             .             .             .             .             .             .
datastorekit/tests/test_shard_file_name.py                  -2/+2             .             .         -8/+6             .             .             .             .             .
datastorekit/tests/test_shardedpool_shard_paths.py          -1/+1             .             .             .             .             .             .             .             .
datastorekit/tests/test_copy_move_store.py                  -3/+3             .             .             .             .             .             .             .             .
datastorekit/tests/test_delete_store.py                     -3/+3         -1/+1             .             .             .             .             .             .             .
datastorekit/tests/test_sharded_store_script.py             -2/+2             .         -5/+3             .             .             .             .         -1/+0             .
datastorekit/tests/test_shard_key_audit_copy.py             -1/+1         -1/+1        -6/+14             .         -3/+3             .             .             .             .
datastorekit/tests/test_shard_key_audit_refusals.py         -1/+1             .         -3/+1             .         -9/+9             .             .             .             .
datastorekit/tests/standin_pool.py                              .         -3/+3             .             .             .       -169/+8             .         -2/+0             .
total                                                     -50/+50         -7/+7       -26/+22         -8/+6       -15/+15       -169/+8      -222/+11         -3/+0         -0/+0

files compared: 31
files ported, checked by compare_ported_tests.py: 20
files with no source, declared: 10
ported: checked by compare_ported_tests.py: datastorekit/tests/test_replicated_write.py (from Datastore/tests/test_replicated_write.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_reconcile_at_open.py (from Datastore/tests/test_reconcile_at_open.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_prune_at_open.py (from Datastore/tests/test_prune_at_open.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_version_row_at_open.py (from Datastore/tests/test_version_row_at_open.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_read_only_pool.py (from Datastore/tests/test_read_only_pool.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_one_timestamp_per_write.py (from Datastore/tests/test_one_timestamp_per_write.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_absolute_shard_record_refused.py (from Datastore/tests/test_absolute_shard_record_refused.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_closed_store_refusals.py (from Datastore/tests/test_closed_store_refusals.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_store_inventory.py (from Datastore/tests/test_store_inventory.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_store_schema.py (from Datastore/tests/test_store_schema.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_store_reader.py (from Datastore/tests/test_store_reader.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_foreign_key_check.py (from Datastore/tests/test_foreign_key_check.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_schema_builder.py (from Datastore/tests/test_schema_builder.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/real_store_fixtures.py (from Datastore/tests/real_store_fixtures.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/schema_description.py (from Datastore/tests/schema_description.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_inventory_declarations.py (from Datastore/tests/test_inventory_declarations.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_declared_facts.py (from Datastore/tests/test_declared_facts.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_layer_registry.py (from Datastore/tests/test_layer_registry.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_drop_refuses_dangling_references.py (from Datastore/tests/test_drop_refuses_dangling_references.py)
ported: checked by compare_ported_tests.py: datastorekit/tests/test_layer_is_generic.py (from Datastore/tests/test_layer_is_generic.py)
not compared (no source, declared): datastorekit/tests/client/__init__.py
not compared (no source, declared): datastorekit/tests/client/build.py
not compared (no source, declared): datastorekit/tests/client/factories.py
not compared (no source, declared): datastorekit/tests/client/objects.py
not compared (no source, declared): datastorekit/tests/client/reader.py
not compared (no source, declared): datastorekit/tests/client/registry.py
not compared (no source, declared): datastorekit/tests/test_neutral_client.py
not compared (no source, declared): datastorekit/tests/test_package_imports.py
not compared (no source, declared): datastorekit/tests/test_parent_set_members.py
not compared (no source, declared): datastorekit/tests/test_shard_key_assignment.py

Lines listed: D-fmt always, UNCLASSIFIED always, the rest with --show.
datastorekit/tests/test_sharded_store_script.py (from Datastore/tests/test_sharded_store_script.py):
  D-fmt         source line removed or changed  Datastore/tests/test_sharded_store_script.py:27: 
datastorekit/tests/standin_pool.py (from Datastore/tests/standin_pool.py):
  D-fmt         source line removed or changed  Datastore/tests/standin_pool.py:419: 
  D-fmt         source line removed or changed  Datastore/tests/standin_pool.py:420: 

OK: every differing line is classified, and every file is accounted for
```

It is not run after the change.

**`compare_ported_tests.py`**, after every change: exit **0**, `OK: 20 module(s) keep their
source's tests, classes and assertion skeletons; 1 test(s) declared not ported`. Its result at
dispatch was the same (the orchestrator's measurement). `test_schema_builder` changed only in its
docstring and the `WITNESS` path literal.

### 5.5 The release check (§4.5)

**The build**: a fresh export of the working tree (the staged files and the two new ones),
`git ls-files -z -co --exclude-standard | tar --null -T - -cf - | tar -xf - -C <scratch>/export-release`
(105 files, no `build/`, `dist/` or `*.egg-info`), then
`uv build --offline --wheel --out-dir <scratch>/wheel-release <scratch>/export-release`.

| | |
|---|---|
| Wheel | `datastorekit-0.2.0-py3-none-any.whl` |
| Size | 98,194 bytes |
| Entries | **25**; none under `datastorekit/tests/`; 3 under `datastorekit/tools/` |
| SHA-256 | `f9513e33f0f6fea208888810006b0cbdd323fefa320a70d52b8011795db2d3f4` |
| `RECORD` SHA-256 | `c12e23bb8ba516348205d7ee52e7414c4bb680313b8165369e223246fec82355` |
| `WHEEL` | `Generator: setuptools (84.0.0)` |
| `METADATA` | `Name: datastorekit`, **`Version: 0.2.0`**, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43`, `Requires-Dist: sqlalchemy<2.1,>=2.0.39` |

The 25 entries are 05's list with `0.2.0` in the `dist-info` name: the 20 layer modules, and
`LICENSE`, `METADATA`, `WHEEL`, `top_level.txt` and `RECORD`.

**The commands**, run by `<scratch>/probe/release_check.sh <scratch>/venv-release/bin/python` from
`<scratch>/outside-release` (outside the repository) with `PYTHONPATH` unset. `<R>` is
`<scratch>/venv-release/lib/python3.13/site-packages`:

```
datastorekit <R>/datastorekit/__init__.py
datastorekit._timing <R>/datastorekit/_timing.py
datastorekit.contract <R>/datastorekit/contract.py
datastorekit.defaults <R>/datastorekit/defaults.py
datastorekit.object <R>/datastorekit/object.py
datastorekit.replication <R>/datastorekit/replication.py
datastorekit.shard_paths <R>/datastorekit/shard_paths.py
datastorekit.store_inventory <R>/datastorekit/store_inventory.py
datastorekit.store_reader <R>/datastorekit/store_reader.py
datastorekit.SQL <R>/datastorekit/SQL/__init__.py
datastorekit.SQL.ClientPool <R>/datastorekit/SQL/ClientPool.py
datastorekit.SQL.Datastore <R>/datastorekit/SQL/Datastore.py
datastorekit.SQL.ProfileAgent <R>/datastorekit/SQL/ProfileAgent.py
datastorekit.SQL.SerialPoolBroker <R>/datastorekit/SQL/SerialPoolBroker.py
datastorekit.SQL.ShardedPool <R>/datastorekit/SQL/ShardedPool.py
datastorekit.SQL.factory_base <R>/datastorekit/SQL/factory_base.py
datastorekit.SQL.schema <R>/datastorekit/SQL/schema.py
datastorekit.tools <R>/datastorekit/tools/__init__.py
datastorekit.tools.shard_key_audit <R>/datastorekit/tools/shard_key_audit.py
datastorekit.tools.sharded_store <R>/datastorekit/tools/sharded_store.py
20 modules imported
exit=0

$ from datastorekit.contract import VERSION_SERIAL_KEY, require_version_serial
<R>/datastorekit/contract.py
'_version_serial' 3
RuntimeError: x: the lookup payload carries no version serial under "_version_serial". A version-keyed lookup goes through Datastore.object_get, which sets it, and is never made unfiltered
True
datastorekit 0.2.0
exit=0

$ python -c "import datastorekit.tests"
ModuleNotFoundError: No module named 'datastorekit.tests'
exit=0

$ python -m datastorekit.tools.sharded_store --help
exit=0
usage: python -m datastorekit.tools.sharded_store [-h] {copy,move} src dst

Copy or move a closed ShardedPool datastore under a new name.
... (35 lines)

$ python -m datastorekit.tools.shard_key_audit
usage: <R>/datastorekit/tools/shard_key_audit.py <path-to-primary-database>
exit=2

$ python -m datastorekit.tools.shard_key_audit --help
!! No such file: <scratch>/outside-release/--help
exit=2
```

`python -c "import datastorekit.tests"` exits **1** (the `exit=0` above is the pipe's; rerun alone:
`exit=1`). The tools behave as at 05: `sharded_store --help` exits 0; `shard_key_audit` exits 2 with
its usage line naming `<R>`, and takes `--help` as a path. **The release check passes.**

### 5.6 The README (§2.10)

Every name it mentions, by `env -u PYTHONPATH ./venv/bin/python <scratch>/probe/readme_check.py .`
(exit 0), which imports `ShardedPool`, `SQLAFactoryBase`, `InventorySpec`, `Parent`, `ParentSet`,
`datastorekit.contract` (with `VERSION_SERIAL_KEY` and `require_version_serial`), `build_schema`,
`Datastore`, both tools and the registry module:

```
datastorekit.__file__ = /Users/ds283/Documents/Code/DatastoreKit/datastorekit/__init__.py
ShardedPool is a class: True
factories= keyword-only: True
SQLAFactoryBase hooks: True
InventorySpec, Parent, ParentSet: True
contract version / store_tag: True
VERSION_SERIAL_KEY == '_version_serial': True
require_version_serial callable: True
key_on_version read by build_schema: True
Datastore.set_lookup_version: True
tools' main: True
installed version 0.2.0: True
links: 18 unresolved: []
install pin: ['datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.0']
```

| Name | How checked |
|---|---|
| `datastorekit.SQL.ShardedPool.ShardedPool`, its `factories=` | imported; `KEYWORD_ONLY` in its signature |
| `datastorekit.SQL.factory_base.SQLAFactoryBase` and its hooks | imported; `hasattr` of each |
| `datastorekit.store_inventory.InventorySpec`, `Parent`, `ParentSet` | imported |
| `datastorekit.contract`, `version` and `store_tag` | `VERSION_TABLE`, `TAG_TABLE` |
| `key_on_version`, `"version": True` | `build_schema` of the registry gives `Tessera`'s record `key_on_version` `True`; §5.1 |
| `datastorekit.contract.VERSION_SERIAL_KEY` | imported, `== "_version_serial"` |
| `datastorekit.contract.require_version_serial` | imported, callable; §5.5 calls it from the wheel |
| `object_get` | `Datastore`'s method, which keys (§1.1) |
| `client-contract.md` §8 by anchor `#8-version-keyed-lookups-v020-prompt-06` | the link check: every one of 18 links resolves, anchors by GitHub's slug rule |
| `v0.2.0`, `v0.1.0` | the install pin `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.0`; `pyproject.toml`'s version; `v0.1.0` peels to `68db557` |
| `compare_with_source.py` on `v0.1.0` | its docstring's new paragraph; `PROVENANCE.md` "After `v0.1.0`" |
| the tools' lines | unchanged from 05; `main` of each imported |

### 5.7 `black`

`./venv/bin/black --check datastorekit docs` (25.1.0): `65 files would be left unchanged.` (64 at
dispatch, plus the new test module). Every Python file changed was formatted with it.

### 5.8 The tree

`git status --short --ignored` at dispatch:

```
!! .idea/
!! datastorekit/SQL/__pycache__/
!! datastorekit/__pycache__/
!! datastorekit/tests/__pycache__/
!! datastorekit/tests/client/__pycache__/
!! docs/extraction/__pycache__/
!! venv/
```

After the work, before the records (staged): the 15 files of the prompt's §7 list that are not records, and
the same ignored entries, with one more: `datastorekit.egg-info/`, written by `venv/`'s reinstall
at `0.2.0` (§5.2), as log 05 §9 foresaw. It is ignored and untracked, and was left (§7 item 4).
No `build/` or `dist/` appeared in the checkout. `git worktree list` showed this checkout alone.
No Ray process was up at any point (`pgrep -lf 'gcs_server|raylet|ray::'` empty, at dispatch and
after). Every store a test or probe made was in a `tempfile` directory.

## 6. The deliberate-breakage record (§4.7)

### 6.1 The method

With the prompt's 15 files staged, `<scratch>/probe/make_breaks.py` made each diff by editing the
file in the checkout, taking `git diff -- <file>` against the index, and restoring the file with
`git checkout -- <file>`; `git status` was the staged 15 after it. `git apply --check` of each
passed in the checkout. Each was then run by `<scratch>/probe/run_break.sh <name>` in a **fresh
export** of the checkout (`<scratch>/exports/break-<name>`): `git apply --check`, `git apply`,
`git apply -R --check` (all passed), `datastorekit.__file__` printed (the export's, every time),
the suite with `venv/`'s interpreter and `PYTHONPATH` set to the export, and `git apply -R`. The
checkout was never broken. The diffs below are the files applied, byte for byte, trailing context
lines included; their `index` lines name the staged blobs. They were extracted from this log after
it was written and checked again both ways in a fresh export (§6.3).

### 6.2 The breakages

**(a) No keying**: the `key_on_version` branch of `object_get` removed.

```diff
diff --git a/datastorekit/SQL/Datastore.py b/datastorekit/SQL/Datastore.py
index 779f128..1c8bb2e 100644
--- a/datastorekit/SQL/Datastore.py
+++ b/datastorekit/SQL/Datastore.py
@@ -557,8 +557,6 @@ class Datastore:
             # a class whose factory declares key_on_version: its build is handed a copy of each
             # payload carrying the lookup serial, so that it finds only rows made under this
             # pool's label; the caller's payloads are not changed
-            if record.get("key_on_version", False):
-                payload_data = self._keyed_payloads(cls_name, payload_data)
 
             try:
                 with self._engine.begin() as conn:
```

`Ran 435 tests` / `FAILED (failures=2, errors=12)`. Of the 444 (correction 5): `ERROR` the five of
`test_neutral_client.TestRoundTrip` (`test_a_reopen_passes_the_check_at_open_repairs_nothing_and_writes_nothing`,
`test_a_replicated_get_is_written_on_the_pinned_controller_then_copied`,
`test_build_store_writes_every_class`, `test_every_class_reads_back_through_a_reopened_pool`,
`test_the_reader_and_the_inventory_read_every_class`) and `test_read_only_pool`'s `setUpModule`
(its 23 do not run), each with `require_version_serial`'s `RuntimeError` ("Tessera: the lookup
payload carries no version serial under "_version_serial". …"). Of the 14: `ERROR` 1, 2, 4, 5, 6
and 9 (the same `RuntimeError`); `FAIL` 7 (`KeyError not raised`) and 8 (`'"Tessera"' not found
in 'Tessera: the lookup payload carries no version serial …'`). Tests 3 and 10–14 pass: they make
no keyed get through the actor.

**(b) The insert serial keys lookups**: `_lookup_serial` replaced by `_version_serial` in the copy.

```diff
diff --git a/datastorekit/SQL/Datastore.py b/datastorekit/SQL/Datastore.py
index 779f128..c8bfb09 100644
--- a/datastorekit/SQL/Datastore.py
+++ b/datastorekit/SQL/Datastore.py
@@ -621,7 +621,7 @@ class Datastore:
                     f'the reserved key "{VERSION_SERIAL_KEY}"; the version serial of a keyed '
                     "lookup is set by the datastore, not by its caller"
                 )
-            keyed.append({**p, VERSION_SERIAL_KEY: self._lookup_serial})
+            keyed.append({**p, VERSION_SERIAL_KEY: self._version_serial})
         return keyed
 
     def object_read_batch(self, ObjectClass, **payload):
```

`Ran 458 tests` / `FAILED (errors=5)`: `ERROR` 4 (both subtests, A and B), 5 and 9, each with
`require_version_serial`'s `RuntimeError` (the read-only actor's copy carries `None`), and, of the
444, `test_read_only_pool.TestOtherWritesRaiseReadOnlyWrite.test_a_vectorized_get_that_reaches_an_inserter`,
which gets the same `RuntimeError` in place of `ReadOnlyWrite`. The prompt expected 4, 5 and 9;
the fifth is found and recorded.

**(c) `set_version` does not set `_lookup_serial`.**

```diff
diff --git a/datastorekit/SQL/Datastore.py b/datastorekit/SQL/Datastore.py
index 779f128..30af9a8 100644
--- a/datastorekit/SQL/Datastore.py
+++ b/datastorekit/SQL/Datastore.py
@@ -167,7 +167,6 @@ class Datastore:
                 f'(label "{self._version_label}"), and cannot be changed to {serial}'
             )
         self._version_serial = serial
-        self._lookup_serial = serial
 
     def set_lookup_version(self, serial: int):
         """
```

`Ran 435 tests` / `FAILED (errors=13)`. Of the 444, the same six as (a), with the actor's
`RuntimeError` ("Datastore "shard0002-store": cannot look up "Tessera", whose lookups are keyed on
the version serial, before the serial of label "standin" is set: …"). Of the 14: `ERROR` 1, 2, 4,
5 (each in its read-write setup), and 6, 7 and 9, whose actors are given `set_version` (7: the
actor's refusal of an unset serial comes before the per-payload `KeyError`, as §2.3 orders them).

**(d) The payload keyed in place.**

```diff
diff --git a/datastorekit/SQL/Datastore.py b/datastorekit/SQL/Datastore.py
index 779f128..12a1b8d 100644
--- a/datastorekit/SQL/Datastore.py
+++ b/datastorekit/SQL/Datastore.py
@@ -621,7 +621,8 @@ class Datastore:
                     f'the reserved key "{VERSION_SERIAL_KEY}"; the version serial of a keyed '
                     "lookup is set by the datastore, not by its caller"
                 )
-            keyed.append({**p, VERSION_SERIAL_KEY: self._lookup_serial})
+            p[VERSION_SERIAL_KEY] = self._lookup_serial
+            keyed.append(p)
         return keyed
 
     def object_read_batch(self, ObjectClass, **payload):
```

`Ran 458 tests` / `FAILED (failures=1)`: `FAIL` 6, `{…, 'weight': 0.25, '_version_serial': 1} !=
{…, 'weight': 0.25}`.

**(e) A caller's key overwritten, not refused.**

```diff
diff --git a/datastorekit/SQL/Datastore.py b/datastorekit/SQL/Datastore.py
index 779f128..de1490c 100644
--- a/datastorekit/SQL/Datastore.py
+++ b/datastorekit/SQL/Datastore.py
@@ -615,12 +615,6 @@ class Datastore:
             )
         keyed = []
         for p in payload_data:
-            if VERSION_SERIAL_KEY in p:
-                raise KeyError(
-                    f'Datastore "{self._my_name}": the object_get payload of "{cls_name}" holds '
-                    f'the reserved key "{VERSION_SERIAL_KEY}"; the version serial of a keyed '
-                    "lookup is set by the datastore, not by its caller"
-                )
             keyed.append({**p, VERSION_SERIAL_KEY: self._lookup_serial})
         return keyed
 
```

`Ran 458 tests` / `FAILED (failures=1)`: `FAIL` 7, `KeyError not raised`.

**(f) A `None` lookup serial not refused by the actor.**

```diff
diff --git a/datastorekit/SQL/Datastore.py b/datastorekit/SQL/Datastore.py
index 779f128..94be86e 100644
--- a/datastorekit/SQL/Datastore.py
+++ b/datastorekit/SQL/Datastore.py
@@ -606,7 +606,7 @@ class Datastore:
         Only ``object_get`` is keyed. ``object_read_batch``, ``read_table``, ``object_store`` and
         ``object_validate`` are not: they are handed what the caller gives.
         """
-        if self._lookup_serial is None:
+        if False:
             raise RuntimeError(
                 f'Datastore "{self._my_name}": cannot look up "{cls_name}", whose lookups are '
                 f"keyed on the version serial, before the serial of label "
```

`Ran 458 tests` / `FAILED (failures=1)`: `FAIL` 8. The get still fails, in `Tessera_factory.build`,
with `require_version_serial`'s message, which does not name `"Tessera"` quoted or
`set_lookup_version`: `'"Tessera"' not found in 'Tessera: the lookup payload carries no version
serial under "_version_serial". …'`.

**(g) `build_schema` accepts `key_on_version` without a `version` column.**

```diff
diff --git a/datastorekit/SQL/schema.py b/datastorekit/SQL/schema.py
index 7efb705..bb98d5d 100644
--- a/datastorekit/SQL/schema.py
+++ b/datastorekit/SQL/schema.py
@@ -308,7 +308,7 @@ def _declared_key_on_version(
         raise _refuse_declaration(
             cls_name, "key_on_version", declared, tab, "which is not a bool"
         )
-    if declared and not registration_data.get("version", False):
+    if False:
         raise _refuse_declaration(
             cls_name,
             "key_on_version",
```

`Ran 458 tests` / `FAILED (failures=1)`: `FAIL` 12, `ValueError not raised`.

**(h) The read-only pool does not call `set_lookup_version`.**

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 40b7619..244a339 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -567,12 +567,6 @@ class ShardedPool:
 
         # the version row's serial keys the lookups of a class whose factory declares
         # key_on_version; it is given as the lookup serial alone, so no actor can insert
-        ray.get(
-            [
-                shard.set_lookup_version.remote(self._version.store_id)
-                for shard in self._shards.values()
-            ]
-        )
 
         # 7. the read_table_config check
         self._read_table_config: Optional[ReadTableConfigType] = read_table_config
```

`Ran 458 tests` / `FAILED (errors=4)`: `ERROR` 4 (both subtests) and 5, with the actor's
`RuntimeError` ("… before the serial of label "A" is set …", and "B"), and, of the 444, exactly
`test_read_only_pool.TestOtherWritesRaiseReadOnlyWrite.test_a_vectorized_get_that_reaches_an_inserter`,
with the actor's `RuntimeError` (label `"standin"`) in place of `ReadOnlyWrite`, as the prompt
says.

**(i) `Tessera_factory.build` drops the version filter.**

```diff
diff --git a/datastorekit/tests/client/factories.py b/datastorekit/tests/client/factories.py
index 6de63be..fdc16fb 100644
--- a/datastorekit/tests/client/factories.py
+++ b/datastorekit/tests/client/factories.py
@@ -948,7 +948,6 @@ class Tessera_factory(SQLAFactoryBase):
             sqla.select(table.c.serial).filter(
                 table.c.alias_serial == alias.store_id,
                 table.c.tessera_weight == weight,
-                table.c.version == require_version_serial(payload, "Tessera"),
             )
         ).scalar_one_or_none()
         attributes = {"_deserialized": True}
```

`Ran 458 tests` / `FAILED (failures=4)`: `FAIL` 1 (`1 == 1 : the Tessera stored under A was
returned under B`), 2 (the sets intersect), 5 (`ReadOnlyWrite not raised`: B finds A's row) and
10 (`RuntimeError not raised`: the build no longer reads the serial). None of the 444. Test 4
passes: under (i) the read-write pool under B also finds A's row, and test 4 compares each
read-only result with the read-write one (§2 item 12). The prompt expected 1, 2 and 5; test 10 is
found and recorded.

**(j) `set_lookup_version` also sets `_version_serial`.**

```diff
diff --git a/datastorekit/SQL/Datastore.py b/datastorekit/SQL/Datastore.py
index 779f128..75102d3 100644
--- a/datastorekit/SQL/Datastore.py
+++ b/datastorekit/SQL/Datastore.py
@@ -188,6 +188,7 @@ class Datastore:
                 f'(label "{self._version_label}"), and cannot be changed to {serial}'
             )
         self._lookup_serial = serial
+        self._version_serial = serial
 
     # A READ-ONLY ACTOR (prompts/a3-v2-readiness, prompt 03)
     #
```

`Ran 458 tests` / `FAILED (failures=1)`: `FAIL` 9, `1 is not None` (the reader's
`_version_serial`). Without that assertion the reader's miss would insert, and the test's
`assertRaises` would fail there too.

Every breakage fails at least one test; none fails nothing.

### 6.3 The diffs, replayed from this log

The ten diffs of §6.2 were extracted from this file (a regular expression over its fenced `diff`
blocks, into `<scratch>/replay/`); each is byte-identical to the file applied. In a fresh export of
the staged tree (`<scratch>/exports/replay`), each was checked with `git apply --check`, applied,
checked with `git apply -R --check`, and reversed: all ten passed. `git apply --check` of each also
passed in the checkout, which was left unchanged (`git status`: the staged 15 files).

## 7. Observations not acted on

1. **`set_version` after `set_lookup_version`.** An actor given `set_lookup_version(s)` and then
   `set_version(t)` with `t != s` moves its lookup serial to `t`, since `set_version` keeps its
   present refusals only (§2 item 11). No pool calls both on one actor: a read-write pool calls
   `set_version`, a read-only pool `set_lookup_version`. Not a defect today; a refusal there would
   be a change to `set_version`'s behaviour, which the prompt did not ask for.
2. **`[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]`** (§4.2, §8). Not fixed.
3. **The new prose and `[01-package-prose-names-sgks-layout]`.** Five added lines in the layer
   name `Datastore.object_get`, the actor class's method, which exists here under that name; they
   name no SGK path, campaign or module, and the issue's pattern (`Datastore.<module>`, a module
   of the layer) does not match them. The issue's measurement is not retaken.
4. **`datastorekit.egg-info/`** is in the checkout again (ignored, untracked), written by `venv/`'s
   reinstall (§5.8). A wheel built in place would carry the test files (05's correction 1); every
   wheel here was built from an export. Left for the user, as 05's was.
5. **The read-only keyed miss of a sharded class is a `ReadOnlyWrite`** ("an insert"), as any
   sharded miss is on a read-only pool (`_refuse_insert`); a keyed miss of a replicated class would
   be a `ReadOnlyMiss`. `client-contract.md` §8 says so; no test reaches the replicated case,
   since no replicated class is keyed (hazard 6).
6. **High-end `ResourceWarning`s**: 186 lines in run 5, the 05 issue's, unchanged in kind.

## 8. Issues

- **Opened: `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]`** (§2.8; §4.2), on
  the board's §3, with the line, the reproduction, the impact as measured and the next step.
- **Closed, narrowed, changed:** none. `[05-a-refused-open-leaves-its-engines-undisposed]` and the
  rest are untouched.

The index goes from **7 to 8 open**: 4 on this board, 4 inherited.

## 9. State handed to the next prompt

- `HEAD` is this commit. The tree is clean but for the ignored entries of §5.8. `venv/` has
  `datastorekit 0.2.0` installed editable (with its own pip), and is otherwise unchanged.
- **Not pushed, not tagged (U28).** `origin/main` is `fe040b2`; local `main` is ahead by
  `1f9941f`, `0e524b4` and this commit. Next, after the review, and each step with the user's
  approval: this commit is pushed as `main`; the workflow runs at both ends on it; **only if both
  pass** is `v0.2.0` made here, annotated, and pushed. A red end means a fix prompt first, and no
  tag on this commit.
- **What the CI log must be read for:** each end's `Ran 458 tests … OK`, and `black` leaving 65
  files unchanged on `low`.
- **The suite is 458** in `venv/` and at the high end.
- **`compare_with_source.py` is retired** (U27): its last output is §5.4's. `compare_ported_tests.py`:
  twenty modules, one test declared not ported, exit 0.
- **The witness** is `schema_at_extraction-06.json` (74,450 bytes, SHA-256 `643128946640…bcddb8`);
  04a's stays beside it.
- **The wheel's `RECORD`**: SHA-256 `c12e23bb8ba516348205d7ee52e7414c4bb680313b8165369e223246fec82355`
  (`Generator: setuptools (84.0.0)`), for the review's rebuild from a clean export.
- **Scratch** (not in the repository): `<scratch>` holds `venv-high`, `venv-release`, `uv-cache`,
  `treecopy`, `export-release`, `wheel-release`, `outside-release`, `exports/`, `breaks/` (the ten
  diffs), `out/` (every run's output) and `probe/`.
