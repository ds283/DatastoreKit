# Prompt 08a — two small fixes

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 07a landed (`dd45243`) and was reviewed (`88cac61`).
- U33–U37 are taken (README §6.2, 2026-10-09).
- `git status` is clean in this repository, and `origin/main` is an ancestor of `main`.

**Closes:** `[02-an-unsupplied-sharded-table-raises-keyerror]` and
`[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]`, both assigned here by U33 and
U35. **Narrows:** nothing. **Changes:** nothing. **Opens:** only what the work finds.

**Recommended model:** **Opus.**
- The code is two short changes.
- The weight is in the tests: each must fail on the unfixed layer for the reason the issue gives.
- The records must stay true: the contract, the board and the index.

**Read first:**

1. [`README.md`](README.md): §1 (the U33 lines), §2 (rows 08a–11), §4, §5 (rules 4, 6, 7, 9 and
   10), §6.2 (U17, U33–U37).
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`.
3. The board's §3 entries for the two issues, in full, and its review of 07a.
4. Log 02 §5 item 1 and log 06 §4.2, where the two defects were found and reproduced.
5. The layer:
   - `datastorekit/SQL/ShardedPool.py`: `_read_shard_data` (`:941`), its sharded-table loop
     (`:1012-1060`), and `object_get_vectorized` (`:3288-3313`);
   - `datastorekit/SQL/Datastore.py`'s `object_get` and `_keyed_payloads` (`:598-625`), which copy
     a payload before adding to it. This is the form the second fix follows.
6. The fixtures: `datastorekit/tests/shard_store_fixtures.py` (`bare_pool`, `read_pool`,
   `write_new_store`), `datastorekit/tests/standin_pool.py` (`StandinCluster`), and
   `datastorekit/tests/client/build.py` (`open_pool`, `get_keypoint`, `get_alias`,
   `get_tesserae`). Read `datastorekit/tests/test_version_keyed_lookups.py`'s `_StandinCase` as the
   model of a module that opens pools in its own tests.
7. [`docs/client-contract.md`](../../docs/client-contract.md): its header, §1 row 6, and §8, the
   model for a section added after the first measurement.

Line numbers here are the package's at `88cac61`, whose `datastorekit/` equals `v0.2.0`'s
(`240028e`).

---

## 1. What is wanted

Two defects, inherited from SGK unchanged, that the board has held open since 02 and 06. U33
fixes them before the campaign closes, and U36 releases them as `v0.2.1`. Each fix is a few lines.
Each comes with a test module whose tests the unfixed layer fails.

- **The bare `KeyError`.** A reopen whose primary records a sharded table that the constructor's
  `sharded_tables` lacks is refused with a bare `KeyError('<table>')`. The refusal meant for that
  case is never reached: the printed list and the `RuntimeError`.
- **The in-place update.** `object_get_vectorized` adds the shard key to each of the caller's
  payload dicts in place, so the caller's dicts change under it.

**Nothing the layer writes changes.** No refusal is added or removed, and no message changes: the
first fix lets an existing message be reached. No client call changes meaning (§2.5).

**08a changes no prose beyond the lines it touches** (09 rewrites the package's prose), and no
file under `docs/adoption/` (10 adds the addenda, U37). It makes no tag and pushes nothing.

---

## 2. What to change

### 2.1 The refusal of an unsupplied sharded table (`ShardedPool.py:1020-1032`)

The loop reads each row of the primary's `sharded_tables` table:

```python
            missing_read_sharded = set()
            mismatching_key_attr = {}
            missing_supplied_sharded = set(self._sharded_tables.keys())
            for row in sharded_table_data:
                if row.table not in missing_supplied_sharded:
                    missing_read_sharded.add(row.table)
                attr = self._sharded_tables[row.table]
                ...
```

A table the store records and the constructor lacks is added to `missing_read_sharded`. The very
next line then indexes `self._sharded_tables` with it and raises. **The fix:** a row whose table the
constructor does not supply contributes no key attribute, and the loop goes on to the next row:

```python
                if row.table not in missing_supplied_sharded:
                    missing_read_sharded.add(row.table)
                if row.table not in self._sharded_tables:
                    continue
                attr = self._sharded_tables[row.table]
```

- **Keep the existing membership test as it is**, and add the guard after it. The two tests differ
  for a table recorded twice. `sharded_tables.table` has no unique constraint
  (`shard_store_fixtures.write_hand_built_primary` declares none, nor does `_create_engine`). The
  existing test reports a duplicate row as "configured but not supplied" and refuses it. That
  behaviour must not change.
- The prints and the two `RuntimeError`s that follow (`:1033-1060`) are unchanged.
- Probed by the planner, on a scratch copy at `88cac61`:
  - through `bare_pool` and `_read_shard_data`, with `write_new_store` (`Sample` recorded) and
    `sharded_tables = {}`: the unfixed layer raises `KeyError: 'Sample'` and prints nothing. The
    fixed layer prints "The following sharded tables are configured in the existing ShardedPool,
    but were not supplied to the constructor:" and `  Sample`, then raises `RuntimeError:
    Mismatch between sharded tables supplied to the constructor and read from the existing
    ShardedPool`;
  - through the whole constructor, on a stand-in store reopened without `Sample` (or without
    `Weave`): the same. Unfixed, `KeyError` at `ShardedPool.py:1026`; fixed, the `RuntimeError`
    at `:1056`, with the printed list naming the table;
  - a supplied but unrecorded table, a differing key attribute, and a matching set behave alike
    before and after;
  - a second `sharded_tables` row for `Sample` (inserted with `sqlite3` into a primary
    `write_new_store` made) is refused alike before and after: the mismatch `RuntimeError`, with
    `Sample` printed as "configured in the existing ShardedPool, but were not supplied". The
    message misdescribes the case, and 08a does not change it. Record it under "Observations not
    acted on".

### 2.2 The vectorized get copies (`ShardedPool.py:3309-3310`)

```python
        for value in payload_data:
            value.update(shard_key)
```

becomes

```python
        payload_data = [{**value, **shard_key} for value in payload_data]
```

- **The shard key is merged last**, as `update` did, so a payload that carries its own value for
  the key's field gets the pool's, as before.
- The order of the payloads and their count are unchanged. Nothing else in the method changes: its
  two refusals and the routing by `shard_key` stay as they are.
- Probed by the planner, through the stand-in pool (`build.open_pool`; two keypoints, their aliases
  `a1` and `a2`; one list `[{"weight": 0.25}, {"weight": 0.75}]` passed three times, with `a1`,
  `a1`, `a2`). The unfixed layer leaves `"k"` in both dicts. The fixed layer leaves them
  `[{'weight': 0.25}, {'weight': 0.75}]`. Both give serials `[1, 2]`, `[1, 2]` and `[501, 502]`
  (`a2`'s shard), and Ray was never initialised.
- With both changes in place, the planner's copy gave `Ran 458 tests … OK` in `venv/`.

### 2.3 The tests: two new modules

The port check requires each ported module's set of tests to equal SGK's
(`compare_ported_tests.py`: "test not in the source"). So the new tests go in **two new modules**,
named for what they pin. Neither is ported, and neither is added to `PORTED`.

**`datastorekit/tests/test_unsupplied_sharded_table.py`.** At least these, each in a `tempfile`
directory with stdout captured:
1. Through `shard_store_fixtures` (`write_new_store`, then `bare_pool` with `_sharded_tables`
   lacking `Sample`, `_create_engine`, `_read_shard_data`, the engine disposed in `finally`): a
   `RuntimeError` whose message is the mismatch message. What was printed names `Sample` under the
   "configured in the existing ShardedPool, but were not supplied" line. **No `KeyError`.**
2. Through the constructor, on a store the stand-in pool wrote (`build.open_pool`, closed), reopened
   by `ShardedPool(...)` with the client registry's `sharded_tables` less one class: the same
   refusal and the same printed name. Ray is never initialised.
3. A supplied but unrecorded table: the mismatch `RuntimeError`, the "supplied to the constructor,
   but are not configured" line naming it. This pins behaviour 08a does not change.
4. A differing key attribute: "Some sharded tables had mismatching key configurations", naming the
   table and both keys. This is also unchanged.
5. A table recorded twice (a second row inserted with `sqlite3` into a primary `write_new_store`
   made): refused as before, as §2.1's last probe gives.

**`datastorekit/tests/test_vectorized_get_payloads.py`.** On the stand-in pool, as `_StandinCase`
does:
1. **The caller's dicts are unchanged**: equal, after the call, to a deep copy taken before it.
   Check the dicts' contents, not the list's identity, since a copy of the list alone would pass a
   check of identity (§4.4, (e)).
2. The same list passed twice with the same key gives the same rows (serials and objects).
3. The same list passed with a second key, on another shard, gives that shard's rows, and the
   dicts are still unchanged.
4. A payload that carries its own value for the key's field gets the pool's key, as before: the
   row found is the pool key's.
5. The rows equal those of a call made with fresh dicts.

The exact count and names are the agent's. The log lists each test with the issue it pins, and
says which tests fail on the unfixed layer (§4.4).

Every test, in either module, meets README §5 rule 7: no Ray, no client, no store outside a
`tempfile` directory. Their names, docstrings and strings name no client (`CLAUDE.md`).

### 2.4 The contract: a §9, added (`docs/client-contract.md`)

The contract describes the layer at named trees. §1–§7 describe `8bc60a5`, and §8 describes
`v0.2.0`. 08a changes what §1 row 6 says of the unsupplied table: "except that a sharded table the
store records and the mapping lacks raises `KeyError` at `:1015` before that message is reached".
Under `CLAUDE.md` rule 6 that row is not rewritten. Instead:
- a header line, after §8's, saying that §9 is measured from the package at 08a's tree, and that it
  supersedes the rows it names;
- a new **§9, Changes after `v0.2.0`**, with a subsection **9.1 (prompt 08a)**. Its table names, for
  each change, the row it supersedes (§1 row 6; and §1 row 4 or row 6 for the vectorized get, as
  the agent finds they read), what the layer now does, with line numbers at 08a's tree, and the
  test module that pins it;
- at the end of §1 row 6 only, the marker *"(superseded in part by §9.1)"*. No other §1–§8 text
  changes.

08b and 10 will add their own subsections to §9.

### 2.5 The clients: read, not changed

The second fix changes what a caller observes. Measure, read-only through `git`, that no client
reads a payload list back after a vectorized get:
- SGK at `b510bc9`;
- CPBH at `52142d7`;
- SI at `7bb3efd`.

The planner found that SGK's 17 calls in `main.py` each pass `x["payload"]` from a work item
built just before, and that no line reads those lists after the call. SI's
`plot_InstantonSolutions.py:697-702` passes one list to two calls: unaffected, since each call now
merges its own key. CPBH passes a bare `beta_value` and is refused by the package either way (its
checklist, item 6). Record each client's sites by count and the finding in the log. Neither fix
changes anything a client stores. **If a client does read its payloads back**, stop (§6).

---

## 3. Hazards

Check each, and say in the log what you found.

1. **`venv/`'s `datastorekit` is an editable install of this checkout.** A probe run from a
   scratch copy imports the checkout unless the copy comes first on `sys.path`. Print
   `datastorekit.__file__` in every probe.
2. **The unfixed layer is the reference for every test.** Write each test, then run it on the
   unfixed layer (a scratch copy at `88cac61`, or `git stash` of the two code lines only), and
   record that it fails, and how, before the fix makes it pass. A test that passes on both is
   either a pin of unchanged behaviour (2.3's tests 3–5 of the first module) or wrong.
3. **The duplicate row.** The guard of §2.1 goes after the existing membership test, not in place
   of it (2.3's test 5).
4. **The stand-in pool runs in-process.** That is why the in-place update is visible to a test at
   all. Under Ray the update also happened in the driver, before the remote call, so the test is
   faithful. Say so in the module's docstring.
5. **No other line of `ShardedPool.py` changes**, no message among them. `git diff` of the file
   shows the two hunks of §2.1 and §2.2 and nothing else.
6. **Prose.** Do not rewrite comments or docstrings outside the lines you change. That is 09's
   (`[01-package-prose-names-sgks-layout]`), and the guard's `KNOWN_HITS` stays at its one entry.
7. **Line numbers move.** The first fix adds two lines at `:1025`; the second removes one at
   `:3309`. Contract and board citations made before 08a are of their own trees. Cite 08a's tree
   in §9 and in the log.

---

## 4. Verification

1. **The suite, in `venv/`** (Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39): `Ran 458 tests
   … OK` before. After, `458 + N` OK, where N is the new tests; the loader gives N for the two new
   modules together. The count falls nowhere.
2. **The high end**, in a fresh venv in the session scratchpad: Python 3.13.16 / Ray 2.55.1 /
   SQLAlchemy 2.0.46, made with `uv pip install --offline` from the cache 05's work filled. The
   planner resolved it offline on 2026-10-09. Install a `git archive` of your tree as an editable
   install, and run the suite: `458 + N` OK. **No download**; a pin that does not resolve offline
   is a stop.
3. **The checks.** `compare_ported_tests.py` exits 0 with "20 module(s) … 1 test(s) declared not
   ported", unchanged. `black --check datastorekit docs` leaves 68 files unchanged (66 + the two
   modules). The layer guard passes with `KNOWN_HITS` at its one entry.
4. **The deliberate-breakage record.** Each is a diff to `ShardedPool.py`, applied in a scratch
   copy, never committed. Record which tests fail under each:
   - **(a)** The guard of §2.1 removed (the unfixed loop): the first module's tests 1 and 2 error
     with `KeyError`.
   - **(b)** The guard placed before the membership test, with `continue`, so an unsupplied table
     is skipped unrecorded: tests 1 and 2 fail, since the open is no longer refused there. Record
     what the open does instead.
   - **(c)** The in-place update restored: the second module's test 1 fails, and test 3 with it.
   - **(d)** The merge order reversed (`{**shard_key, **value}`): test 4 fails.
   - **(e)** The list copied and its dicts updated in place (`payload_data = list(payload_data)`,
     then the old loop): test 1 fails.

   For each, record the verdict line over the whole suite, and that the existing 458 are unaffected
   except where the log says.
5. **The clients** (§2.5): the sites read, by count, with the finding. Each client's `git status
   --short` is as at the start.

---

## 5. Acceptance

1. The two code changes of §2.1 and §2.2, and nothing else in `datastorekit/` outside the two new
   test modules.
2. The two modules, with every test of §2.3, each failing on the unfixed layer as §4.4 records or
   pinning unchanged behaviour as §2.3 says.
3. `docs/client-contract.md`'s header line, §9.1 and the one marker.
4. §4.1–§4.5 hold.
5. **The records**, in the same commit:
   - the log, `logs/08a-two-small-fixes.md`, per README §5.1;
   - the board: 08a's row and the header; the two issues moved from §3 to §4, each with a dated
     "Closed (2026-10-09, prompt 08a)" line naming its fix and its test module;
   - `docs/OPEN_ISSUES.md`: the two rows deleted, the count **8 → 6**, and the date;
   - `prompts/INDEX.md`: the campaign's line, and its open-issue count.

---

## 6. Stop conditions — stop and ask the user

- An existing test fails with either fix in place, or the suite's count falls.
- Either fix cannot be made without changing a message, a refusal, or another line of the layer.
- A client reads a payload list back after a vectorized get (§2.5).
- The high end does not resolve offline.
- Anything would write in a client repository, push, tag, download, or start Ray.

---

## 7. What this prompt changes, and what it does not

- **Files it creates or changes:**
  - `datastorekit/SQL/ShardedPool.py` (§2.1, §2.2);
  - `datastorekit/tests/test_unsupplied_sharded_table.py` and
    `datastorekit/tests/test_vectorized_get_payloads.py` (new);
  - `docs/client-contract.md` (§2.4);
  - the log, the board, `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.
- **It changes nothing else.** In particular, it does not change:
  - any other file under `datastorekit/`, `standin_pool.py`, the fixtures or the client;
  - `compare_ported_tests.py`, `PROVENANCE.md`, `README.md`, `pyproject.toml`, `docs/adoption/`;
  - the campaign README, `CLAUDE.md` or the workflow.
- **It touches no client repository.**
- It makes no tag and pushes nothing. The version stays `0.2.0`; 10 releases.

---

## 8. The log and the board

`logs/08a-two-small-fixes.md`, using README §5.1. There is no `compare_with_source.py` output
(U27); its place holds the port check's output, and the test-by-test record of §2.3 and §4.4. The
log also lists the clients' commits and statuses, at the start and the end.

`IMPLEMENTATION_STATE.md`: §1's row for 08a (landed, commit, log), the header, and §3/§4 for the
two issues.
