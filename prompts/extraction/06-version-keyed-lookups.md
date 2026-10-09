# Prompt 06 — version-keyed lookups, ready for `v0.2.0`

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 05 landed (`68db557`), was reviewed (`487ec4c`), and `v0.1.0` is tagged on it after green CI
  (`fe040b2`).
- U25–U28 are taken (README §6.2, 2026-10-09).
- `git status` is clean in this repository, and `main` equals `origin/main`.

**Closes:** nothing. **Narrows:** nothing. **Changes:** nothing.
**Opens:** `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]` (§2.8), and anything
else the work finds.

**Recommended model:** **Opus.**
- The behaviour is small: one optional `register()` key, read in two places.
- Its weight is in three things the source never had:
  - the package's late version serial (`set_version`);
  - its read-only pool, whose actors are never given that serial (U26);
  - a schema witness that must change by exactly one key.

**Read first:**

1. [`README.md`](README.md): §1, §2 (rows 06 and 07), §4, §5 (rules 6–10), §6.2 (U13, U20, U22,
   U23 and U25–U28) and §7.
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`, above all "Releases" and "Repository
   mechanics".
3. The board, with the review of 05 and its `v0.1.0` paragraph. Then
   [`logs/05-supported-versions-and-ci.md`](logs/05-supported-versions-and-ci.md) §5.3 and §9, and
   [`logs/04a-port-the-store-and-inventory-tests.md`](logs/04a-port-the-store-and-inventory-tests.md)
   on how a schema witness is captured.
4. The repository as `v0.1.0` left it:
   - `datastorekit/SQL/schema.py`, `datastorekit/SQL/Datastore.py`, `datastorekit/contract.py`,
     and in `datastorekit/SQL/ShardedPool.py` the read-only open (`:439-579`) and
     `object_get_vectorized` (`:3277-3302`);
   - `datastorekit/tests/client/` (`factories.py:919-962`, `Tessera_factory`; `registry.py`'s
     roles table), `test_neutral_client.py` (`REGISTER_KEYS`), `test_schema_builder.py`,
     `schema_description.py`, `test_declared_facts.py`, `test_version_row_at_open.py` and
     `test_read_only_pool.py` (their labelled `open` helpers);
   - `docs/client-contract.md`, `PROVENANCE.md`, `README.md` and `pyproject.toml`.
5. The source of the feature, in ChamPBH (CPBH), **read only through `git show`** at CPBH `52142d7`:
   - `Datastore/SQL/Datastore.py:328-338` (the key, refused without a `version` column),
     `:390` (a class with no table), `:500-509` (the keyed copy in `object_get`) and `:544-555`
     (`_with_version_serial`);
   - `config/version.py:52-71` (`VERSION_SERIAL_KEY`, `require_version_serial`);
   - `Datastore/tests/test_version_keyed_lookups.py` (470 lines, ten tests in
     `TestVersionKeyedLookups` and one in `TestOneVersionLabel`).

   `Datastore.py` is unchanged from `9b3db51`, the commit README §2 cites, to `52142d7`.

Facts below are at `fe040b2`, whose package equals `68db557` (`v0.1.0`). They were measured on
2026-10-09, from scratch copies in the session scratchpad, with nothing in the repository written.

---

## 1. What is wanted

06 adds CPBH's version-keyed lookups to the layer, as the optional `register()` key
`key_on_version`, and makes the package ready to be released as `v0.2.0`, the release CPBH adopts
(G3). After it:

- **a factory that declares `key_on_version: True` receives the store's version serial** in every
  `object_get` payload, under `datastorekit.contract.VERSION_SERIAL_KEY`. Its `build` filters on it
  through `datastorekit.contract.require_version_serial`, so it finds only rows made under the
  label the pool was opened with;
- this holds for **a read-write pool and a read-only one** alike (U26);
- **the neutral client's `Tessera` is keyed** (U25), and a new test module carries over the
  semantics of CPBH's tests;
- **nothing changes for a class that does not declare the key**, and nothing the layer writes
  changes. No SGK or SI factory declares it.

**Rule 8 has lifted** (README §5): this is the first prompt that changes the layer.
`compare_with_source.py` is retired at `v0.1.0` (U27): it is run once more, at the start, and is
not run after. `compare_ported_tests.py` still runs.

**06 makes no tag and pushes nothing (U28).** After its review, its commit is pushed alone as
`main`. `v0.2.0` is made on it, annotated, only once CI passes at both ends there, as `v0.1.0` was
(U23; the board's `v0.1.0` paragraph).

---

## 2. What to change

### 2.1 The contract: `datastorekit/contract.py`

Add, under a comment saying what they are for:
- `VERSION_SERIAL_KEY = "_version_serial"`, CPBH's value, so that a CPBH factory moves by its
  import alone.
- `require_version_serial(payload, cls_name: str) -> int`. It returns
  `payload[VERSION_SERIAL_KEY]`. If the key is absent or `None`, it raises `RuntimeError` naming
  `cls_name` and the key, and saying that a keyed lookup goes through `object_get` and is never
  made unfiltered (CPBH `config/version.py:58-71`).

The module still imports nothing outside the standard library. Its docstring gains one paragraph
saying why the key is the layer's: the actor sets it, so its name cannot be a client's choice.

### 2.2 The declaration: `datastorekit/SQL/schema.py`

- `build_schema` reads `key_on_version` (default `False`) through a new
  `_declared_key_on_version(cls_name, tab, registration_data) -> bool`, in the form of the three
  `_declared_*` helpers. It refuses with `_refuse_declaration`'s `ValueError`:
  - a value that is not a `bool` ("which is not a bool");
  - `True` when the table has no `version` column. CPBH raised `RuntimeError` here; the package's
    declarations raise `ValueError`, naming the class, the key and the value.
- **The record of a class with a table** holds `"key_on_version"`: `True` or `False`. **The record
  of a class with no table is unchanged**: it holds no new key, so that
  `test_declared_facts.TestTheRecords.test_a_record_with_no_table_is_unchanged` holds. CPBH added
  `False` there (`:390`); a reader uses `.get`.
- `build_schema`'s docstring names the new key beside the three declared facts.

### 2.3 The lookup: `datastorekit/SQL/Datastore.py` (U26)

**Two serials.** The actor keeps `_version_serial`, which stamps inserts and which a read-only
actor never holds (`:164-172`'s third guard). It gains `_lookup_serial`, which keys lookups.
- `set_version(serial)` sets both, with its present checks and refusals unchanged.
- **New `set_lookup_version(serial)`** sets `_lookup_serial` only. It takes `set_version`'s type
  check and refuses a change to a different serial in the same way. It never sets
  `_version_serial`.

**In `object_get`**, after `payload_data` is formed and before the transaction (`:515-526`), if
the record's `key_on_version` is set (read with `.get(..., False)`):
- if `_lookup_serial` is `None`, raise `RuntimeError` naming the class and the label, and saying
  that the pool sets the serial with `set_version` or `set_lookup_version`. Nothing is built and
  nothing is unfiltered;
- for each payload: if it holds `VERSION_SERIAL_KEY`, raise `KeyError` naming the class and the
  key, as CPBH does (`:550-553`); otherwise use a **copy**, `{**p, VERSION_SERIAL_KEY:
  self._lookup_serial}`. The caller's payload is not mutated.

Put the copy in a private method, as CPBH's `_with_version_serial`. Its docstring and comments
name no client. `object_read_batch`, `read_table`, `object_store` and `object_validate` are not
keyed (CPBH keys neither); the method's docstring says so.

### 2.4 The read-only pool: `datastorekit/SQL/ShardedPool.py` (U26)

In `_open_read_only`, after every actor's `read_only_state` has returned (`:561-564`), call
`set_lookup_version` on every actor with `self._version.store_id`, and wait for every call. Step
5/6's comment (`:464-469`) and the class's read-only comment gain one line saying so.

The read-write constructor is unchanged: `set_version` gives a read-write actor both serials.

### 2.5 The neutral client (U25)

- **`Tessera_factory.register()`** gains `"key_on_version": True`. Tessera is sharded and already
  carries a `version` column. **Its `build`** adds `table.c.version ==
  require_version_serial(payload, "Tessera")` to its select (`factories.py:943-947`). Its insert is
  unchanged: `_insert` stamps the version.
- **`registry.py`'s roles table**: `Tessera`'s row adds "`key_on_version` (prompt 06)".
- **`test_neutral_client.REGISTER_KEYS`** gains `"key_on_version"`. That test, and 02's coverage
  rule, require a factory of the shared client to declare every key the schema builder reads, so a
  test-local registry cannot cover it (U25).

No other client class changes. `build_store`, the drop groups and the fixtures do not change.

### 2.6 The schema witness

Adding the key changes every record of a class with a table, so `test_schema_builder`'s two
witness tests fail (probed: 22 subtests each). Under the witness rule (that module's docstring,
and 04a's log), **no witness is edited or regenerated to make a test pass.** Instead:
- capture `datastorekit/tests/data/schema_at_extraction-06.json` with `schema_description.py`, as
  04a captured its witness: twice, from two fresh interpreters, byte-identical;
- check its difference from `schema_at_extraction-04a.json`, by loading both and comparing them.
  The **only** difference allowed is:
  - each of the 21 records with a table gains `"key_on_version"`, `true` on `Tessera` and `false`
    on the other 20;
  - `ephemeral_probe`'s record (no table) and every table description are unchanged.

  Anything else is a stop. The log quotes the comparison;
- point `WITNESS` at the new file, and rewrite the docstring's "The current one is …" sentence to
  name it, keeping 04a's as the earlier witness.

`schema_at_extraction-04a.json` stays, unchanged.

### 2.7 The tests: `datastorekit/tests/test_version_keyed_lookups.py` (new)

The suite goes from **444 to 458**: these 14 tests, and no other change of count.
- Pools are opened as `test_version_row_at_open.open` and `test_read_only_pool.open` open them: a
  `sp.StandinCluster()`, made active, and `sp.sp_mod.ShardedPool(version_label=…, …)` with the
  client's registry. `standin_pool.open_pool` fixes its label, and it does not change.
- An actor is the undecorated `Datastore.__ray_actor_class__` on a file in a `tempfile` directory.
- No Ray, nothing outside a `tempfile` directory, and stdout redirected where a constructor prints.
- The module docstring says what CPBH's tests are carried over from (by test, not by CPBH's
  names), and names no client.

| # | Class | Test | CPBH origin | What it shows |
|---|---|---|---|---|
| 1 | `TestThroughThePool` | `test_a_keyed_row_is_returned_only_under_its_own_label` | (a) | A `Tessera` got under A is found under A, is a new row under B, and is A's again when A is reopened (scalar `object_get`) |
| 2 | 〃 | `test_the_vectorized_route_is_keyed_too` | (c3) | The same through `object_get_vectorized` |
| 3 | 〃 | `test_an_unkeyed_versioned_class_keeps_one_row_across_labels` | (e) | A `keypoint_alias` (versioned, replicated, not keyed) has one row and one serial under A and B |
| 4 | 〃 | `test_a_read_only_pool_finds_the_rows_of_its_own_label` | — (U26) | Read-only under A finds A's Tesserae; under B finds B's |
| 5 | 〃 | `test_a_read_only_miss_under_another_label_is_refused` | — (U26) | A Tessera stored only under A, looked up read-only under B, raises `ReadOnlyWrite` (a sharded miss) and writes nothing |
| 6 | `TestTheActor` | `test_the_callers_payload_is_not_mutated` | (d2) | `object_get(…, payload_data=[p])` leaves `p` equal to a copy taken before, without the key |
| 7 | 〃 | `test_a_caller_supplied_serial_is_refused` | (d2) | A payload holding `VERSION_SERIAL_KEY` raises `KeyError` naming the key |
| 8 | 〃 | `test_a_keyed_lookup_before_the_serial_is_set_raises` | — | No `set_version`: a keyed get raises the actor's `RuntimeError` (its message names `set_lookup_version`) and inserts nothing; a get of `gauge_setting` (no `version` column) on the same actor is not refused |
| 9 | 〃 | `test_set_lookup_version_keys_lookups_and_admits_no_insert` | — (U26) | After `set_lookup_version` only: a keyed get that finds a row returns it; an insert into a versioned class is still refused by `_insert`'s guard |
| 10 | 〃 | `test_a_keyed_build_without_the_serial_raises` | (d) | `Tessera_factory.build` called directly with a payload lacking the key raises `RuntimeError` |
| 11 | `TestTheDeclaration` | `test_only_tessera_is_keyed` | (d3) | Of the registry's records, exactly `Tessera`'s has `key_on_version` `True` |
| 12 | 〃 | `test_key_on_version_without_a_version_column_is_refused` | (d4) | `build_schema` raises `ValueError` naming the class and the key |
| 13 | 〃 | `test_a_key_on_version_that_is_not_a_bool_is_refused` | — | `"key_on_version": "yes"` raises `ValueError` |
| 14 | `TestTheContract` | `test_require_version_serial` | — | `VERSION_SERIAL_KEY == "_version_serial"`; `require_version_serial` returns the serial, and raises `RuntimeError` naming the class when the key is absent or `None` |

CPBH's (b), (c1) and (c2) test its own three classes; their semantics are (a)'s, on one neutral
class. CPBH's (f) is about its scripts. Neither is carried over, and the log says so.

### 2.8 What the probe found, to record and not fix

`ShardedPool.object_get_vectorized` adds the shard key to each of the caller's payload dicts in
place (`value.update(shard_key)`, `:3298-3299`). This was so before 06. A caller that reuses its
list sees the key in it. It does not affect keying, which copies in the actor.
- **Open `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]`** on the board's §3,
  with the line, a reproduction (a list passed twice), the impact (a caller's dicts change; a
  caller that passes the same dicts to a different shard key's get sends them the first key), and
  the next step (copy, as 2.3 does). Add its index row.
- **Do not fix it.** Test 6 is at the actor for this reason, and its docstring says so.

### 2.9 The records of the contract, and of provenance

- **`docs/client-contract.md`** is a measured document, and rule 6 makes it additive:
  - add **§8 "Version-keyed lookups (`v0.2.0`, prompt 06)"**, measured from 06's tree. It covers
    the key, the reserved payload key, `require_version_serial`, the two serials and the
    read-only pool, what is not keyed, and the refusals, each with its lines, and `Tessera` as the
    client's example;
  - add one italic line under the header saying that §8 is measured at 06's tree, and that §1–§7
    remain as at `8bc60a5`, so their line numbers into the files 06 changes are that tree's;
  - change nothing else.
- **`PROVENANCE.md`** gains a section "After `v0.1.0`". It names:
  - the files 06 changes;
  - CPBH `52142d7` and the lines carried over (§0 item 5 above);
  - that `compare_with_source.py` describes the tree at `v0.1.0` and is retired there (U27).

  `PROVENANCE.md` is outside the package, so it may name CPBH; no file under `datastorekit/`
  may.
- **`docs/extraction/compare_with_source.py`** gains, at the top of its docstring, one paragraph:
  it checks the package as tagged `v0.1.0`, was retired there (README §6.2, U27), and is run on
  that tag (for example from a `git worktree` of it) if it is run again. Nothing else in it
  changes.

### 2.10 The release

- `pyproject.toml`: `version = "0.2.0"`. Nothing else.
- `README.md`:
  - the status names `v0.2.0` and what it adds;
  - the install line pins `v0.2.0`, with one sentence saying that `v0.1.0` remains for a client
    that has not adopted the key;
  - "Using it" gains one item for `key_on_version`, naming `VERSION_SERIAL_KEY`,
    `require_version_serial` and `client-contract.md` §8;
  - "Developing" says that `compare_with_source.py` describes `v0.1.0` and is run on that tag
    only.

  Every name it mentions is checked by importing it, as 05 did.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **A probe script imports the installed package, not your copy.** `python <dir>/probe.py` puts
   the script's directory on `sys.path`, not the working directory, so an editable install shadows
   a scratch copy. The planner's first behaviour probe was wrong for this reason. Use `-m`, or set
   `PYTHONPATH` to the copy, and print `datastorekit.__file__`.
2. **The witness.** §2.6. A difference beyond the one key means the change reaches more than it
   should.
3. **The read-only actor's third guard.** `set_lookup_version` must not set `_version_serial`
   (test 9; breakage (j)). `test_version_row_at_open`'s section 4 still passes unchanged.
4. **A class that declares nothing.** Every one of the 444 passes unchanged except the three
   §2.5–§2.6 name: the two witness tests and `REGISTER_KEYS`'s test. Probed at 3 with Tessera keyed
   and the two serials in place. Any other is a stop.
5. **The guard.** `test_layer_is_generic` scans the layer's prose and strings. A comment crediting
   CPBH, or naming one of its classes, in a layer file is a hit, and a stop. Provenance goes in
   `PROVENANCE.md`. `KNOWN_HITS` stays at its one entry.
6. **Replicated keyed classes.** The keying is in the actor, so a replicated class may declare
   it. Each shard keys with the same serial, since the version row is replicated and every actor
   is given the one serial. The client keys no replicated class, and §8 says that this route is
   allowed but not exercised by the suite.

---

## 4. Verification

1. **The suite.** In `venv/`: `Ran 444 tests … OK` before, and **`Ran 458 tests … OK`** after,
   after `./venv/bin/python -m pip install --no-deps -e .` (so that `pip show` says `0.2.0`). The
   loader gives 14 for the new module.
2. **The high end.** A fresh scratch venv at the high pins (Python 3.13.16, `ray==2.55.1`,
   `sqlalchemy==2.0.46`), made with `uv pip install --offline` from the cache 05's work filled:
   `Ran 458 tests … OK`. U24 allowed downloads for 05 only. If the offline resolve fails, stop and
   ask; do not download. CI runs both ends after the push (U28).
3. **The checks.**
   - `compare_with_source.py` once, **before any change**: exit 0, with 31 compared, 20 `PORTED`
     and 10 with no source. This is its last run (U27).
   - `compare_ported_tests.py` **after**: exit 0 over twenty modules, with one test declared not
     ported. `test_schema_builder` changes only in a string literal and its docstring.
4. **The witness**, §2.6: captured twice and byte-identical; its comparison with 04a's; its size
   and SHA-256.
5. **The release check**, as 05's (log 05 §5.3; built from a clean export, never in this
   checkout):
   - 25 entries and nothing under `tests/`;
   - `METADATA` says `Version: 0.2.0`;
   - installed at the high pins and run from outside the repository with `PYTHONPATH` unset,
     `from datastorekit.contract import VERSION_SERIAL_KEY, require_version_serial` works, and
     the tools behave as at 05.

   Use the offline cache for the install.
6. `black --check datastorekit docs` (25.1.0) is clean.
7. **The breakage record.** Each item is a diff exactly as applied, with what failed, checked with
   `git apply --check` and `-R --check` as recorded. None is committed, and `git status` is clean
   after each.
   - **(a)** No keying: the `key_on_version` branch of `object_get` removed. Every keyed get then
     reaches `require_version_serial` without the key. Expect every test that makes a keyed get to
     fail or error, and many of the 444, since `build_store` gets Tesserae.
   - **(b)** The insert serial keys lookups: `_lookup_serial` replaced by `_version_serial` in the
     copy. Expect 4, 5 and 9, which hold only the lookup serial.
   - **(c)** `set_version` does not set `_lookup_serial`. Expect 1, 2, 4 and 5 to error, and many
     of the 444, since `build_store` gets Tesserae on a read-write pool.
   - **(d)** The payload keyed in place (`p[VERSION_SERIAL_KEY] = …` on the caller's dict). Expect
     6.
   - **(e)** A caller's key overwritten, not refused. Expect 7.
   - **(f)** A `None` lookup serial not refused by the actor. Expect 8: the get still fails, but in
     `Tessera_factory.build`, with `require_version_serial`'s message, not the actor's.
   - **(g)** `build_schema` accepts `key_on_version` without a `version` column. Expect 12.
   - **(h)** The read-only pool does not call `set_lookup_version`. Expect 4 and 5, and
     `test_read_only_pool`'s `test_a_vectorized_get_that_reaches_an_inserter` (probed: it raises
     the actor's `RuntimeError` in place of `ReadOnlyWrite`).
   - **(i)** `Tessera_factory.build` drops the version filter. Expect 1, 2 and 5.
   - **(j)** `set_lookup_version` also sets `_version_serial`. Expect 9.

   The log names exactly what each fails. A breakage that fails nothing is a §3 issue.

---

## 5. Acceptance

1. `key_on_version`, the two serials, `set_lookup_version`, `VERSION_SERIAL_KEY` and
   `require_version_serial` are as §2.1–§2.4 say.
2. `Tessera` is keyed, `REGISTER_KEYS` names the key, and the new witness differs from 04a's by
   exactly the one key.
3. The suite is 458 in `venv/` and at the high end. `compare_ported_tests.py` passes. The release
   check passes at `0.2.0`.
4. `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]` is open, with its
   reproduction.
5. §4.1–§4.7 hold.
6. **The records**, in the same commit:
   - the log, `logs/06-version-keyed-lookups.md`, per README §5.1. It also has:
     - the 14 tests, each with its CPBH origin or "new", and the CPBH tests not carried over;
     - every probe and its command, with `datastorekit.__file__` printed (hazard 1);
     - the witness record (§4.4);
     - the six hazards;
     - each venv's versions and verdict line;
     - `compare_with_source.py`'s last output and `compare_ported_tests.py`'s summary;
     - the release check's record;
     - every name the README mentions, with how it was checked;
     - (a)–(j);
     - the test count before and after (444, 458);
   - the board: §1's row for 06 and the header, §3 per §2.8, and the G3 line in §2 saying that
     `v0.2.0` is ready to be tagged once CI passes (U28), with no tag made;
   - `docs/OPEN_ISSUES.md`: 7 open now, and 8 after, unless the work opens another;
   - `prompts/INDEX.md`: the campaign's line.

---

## 6. Stop conditions — stop and ask the user

- The suite fails or its count differs from 458, or a test of the 444 other than §3 hazard 4's
  three changes.
- The new witness differs from 04a's beyond the one key.
- The guard finds a hit other than its pinned one.
- Passing anything would need a change to a file not in §7, or to `standin_pool.py`, a fixture, or
  any ported test's assertions.
- A pin does not resolve offline, or anything would need a download.
- Anything would push to GitHub, make or move a tag, change the repository's settings, start Ray,
  open a store outside a `tempfile` directory, or edit, run, import or open a store of SGK, CPBH or
  SI. CPBH is read through `git show` only.

---

## 7. What this prompt changes, and what it does not

- **Files it creates or changes:**
  - `datastorekit/contract.py`, `datastorekit/SQL/schema.py`, `datastorekit/SQL/Datastore.py`,
    `datastorekit/SQL/ShardedPool.py`;
  - `datastorekit/tests/client/factories.py` (`Tessera_factory` only) and
    `datastorekit/tests/client/registry.py` (the roles table only);
  - `datastorekit/tests/test_neutral_client.py` (`REGISTER_KEYS` only);
  - `datastorekit/tests/test_schema_builder.py` (`WITNESS` and the docstring sentence only);
  - `datastorekit/tests/data/schema_at_extraction-06.json` (new);
  - `datastorekit/tests/test_version_keyed_lookups.py` (new);
  - `docs/client-contract.md` (§8 and the header line only);
  - `docs/extraction/compare_with_source.py` (the docstring paragraph only);
  - `PROVENANCE.md`, `README.md`, `pyproject.toml`;
  - the log, this board, `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.
- **It changes nothing else:**
  - not `standin_pool.py` or any fixture, nor any other test module;
  - not `schema_at_extraction-04a.json` or the guard's data;
  - not `CLAUDE.md`, `LICENSE`, `.gitignore`, the workflow or the campaign README.
- It makes no tag and pushes nothing (U28).
- It fixes no other issue, inherited or open, including §2.8's and
  `[05-a-refused-open-leaves-its-engines-undisposed]`.
- It does not rewrite the layer's prose (`[01-package-prose-names-sgks-layout]`). New prose it
  writes names no client and no SGK path.
- It writes no orchestration note.

---

## 8. The log and the board

`logs/06-version-keyed-lookups.md`, using README §5.1, with the additions of §5.6.

`IMPLEMENTATION_STATE.md`: §1's row for 06 (landed, commit, log), the header, §2's G3 line, and §3.
