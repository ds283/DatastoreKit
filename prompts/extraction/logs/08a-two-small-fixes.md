# Log 08a — two small fixes

**Subject:** Fix the unsupplied-table refusal and the vectorized get's payloads · **Commit:** this
commit · **Date:** 2026-10-10 (started 2026-10-09) · **Model:** Claude Opus 5.5 · **Result:**
landed; unpushed and untagged.

Two defects inherited from SGK, held open since 02 and 06, are fixed (U33, U35):

- **`[02-an-unsupplied-sharded-table-raises-keyerror]`.** A reopen whose primary records a sharded
  table that the constructor's `sharded_tables` lacks is now refused by the intended mismatch
  `RuntimeError`, with the table printed under "configured in the existing ShardedPool, but were
  not supplied to the constructor", not by a bare `KeyError`.
- **`[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]`.** `object_get_vectorized`
  sends copies of the caller's payloads with the shard key merged in last, and leaves the caller's
  dicts as they were.

`ShardedPool.py` changes by the two hunks of the prompt's §2.1 and §2.2 and nothing else. Two new
test modules hold **11** tests: the suite goes from **458 to 469**, in `venv/` and at the high
end. On the unfixed layer, 4 of the 11 fail for the issues' reasons (the first module's two
refusal tests error with `KeyError`; the second module's tests 1 and 3 fail on the changed dicts);
the other 7 pin behaviour the fixes keep. Each of the five breakages of §4.4 is caught, and only by
the new modules. `docs/client-contract.md` gains a header line, §9 with §9.1, and one marker on
§1 row 6. Both issues move to the board's §4; the index goes from **8 to 6 open**.

No client was written, imported or run; nothing was pushed, tagged or downloaded; Ray was never
started.

Prompt: [`../08a-two-small-fixes.md`](../08a-two-small-fixes.md), with the orchestrator's dispatch
note §0: eight corrections, three additions, its measured facts and its conventions. Each is
followed as given; §2 classifies them.

## 1. What shipped

### 1.1 The layer (§2.1, §2.2)

`datastorekit/SQL/ShardedPool.py`, two hunks (`git diff` of the file shows nothing else):

```diff
@@ -1023,6 +1023,8 @@ class ShardedPool:
             for row in sharded_table_data:
                 if row.table not in missing_supplied_sharded:
                     missing_read_sharded.add(row.table)
+                if row.table not in self._sharded_tables:
+                    continue
                 attr = self._sharded_tables[row.table]
                 if row.key_attr != attr:
                     mismatching_key_attr[row.table] = {
@@ -3306,8 +3308,7 @@ class ShardedPool:
             self._ShardKeyStoreIdGetter(shard_key[shard_key_field])
         ]
 
-        for value in payload_data:
-            value.update(shard_key)
+        payload_data = [{**value, **shard_key} for value in payload_data]
         return self._shards[shard_id].object_get.remote(
             cls_name, payload_data=payload_data
         )
```

At 08a's tree (correction 7, confirmed): the guard is `:1026-1027`, after the unchanged membership
test (`:1024-1025`), and `attr = …` is `:1028`; the "not supplied" heading and its list print at
`:1035-1040`; the mismatch refusal raises at `:1056` (message `:1057`), the key-attribute refusal
at `:1060` (message `:1061`). `object_get_vectorized` is `:3290-3314`, its two refusals
`:3296-3299` and `:3302-3305`, the routing `:3307-3309`, and the merge `:3311`. No message, no
refusal and no comment changed. `black` leaves the file unchanged.

### 1.2 The tests (§2.3)

**`datastorekit/tests/test_unsupplied_sharded_table.py`**, 6 tests. Tests 1 and 3–6 use a primary
`shard_store_fixtures.write_new_store` made (one sharded table, `Sample` on `k`) and a bare pool
(`bare_pool`, `_create_engine`, `_read_shard_data`, the engine disposed in `finally`), stdout
captured. Test 2 reopens a store `build.open_pool` wrote and `cluster.close_pool` closed, by calling
`ShardedPool(...)` itself inside `cluster.active()` (correction 3), stdout captured.

| # | Test | Pins | Unfixed layer |
|---|---|---|---|
| 1 | `TestThroughTheFixture.test_a_recorded_table_not_supplied_is_refused_with_the_mismatch` | `[02-…-keyerror]`: `sharded_tables = {}` is refused with the mismatch `RuntimeError` (message compared whole), `Sample` alone printed under the "not supplied" heading, neither other heading printed | **ERROR**, `KeyError: 'Sample'` at `ShardedPool.py:1026` |
| 2 | `TestThroughTheConstructor.test_a_recorded_table_not_supplied_is_refused_with_the_mismatch` | `[02-…-keyerror]`, through the whole constructor: for each of the client's four sharded classes left out (one subtest each), the same refusal and printed name, and no ">> Opened existing sharded datastore" | **ERROR** ×4 subtests, `KeyError: 'Tessera'`, `'Sample'`, `'Trace'`, `'Weave'` at `:1026` (from `__init__` `:260`) |
| 3 | `TestThroughTheFixture.test_a_supplied_table_not_recorded_is_refused_with_the_mismatch` | unchanged behaviour: `{"Sample": "k", "Trace": "k"}` gives the mismatch, `Trace` under "supplied to the constructor, but are not configured" | passes (pin) |
| 4 | `TestThroughTheFixture.test_a_differing_key_attribute_is_refused_naming_both_keys` | unchanged behaviour: `{"Sample": "j"}` gives "Some sharded tables had mismatching key configurations…", printing `Sample: configured key="k", supplied key="j"` | passes (pin) |
| 5 | `TestThroughTheFixture.test_a_table_recorded_twice_is_refused_as_before` | unchanged behaviour (hazard 3): a second `Sample` row, inserted with `sqlite3` (the table then holds `(0, 'Sample', 'k')` and `(1, 'Sample', 'k')`), and `Sample` supplied: the mismatch `RuntimeError`, `Sample` printed as "not supplied" | passes (pin) |
| 6 | `TestThroughTheFixture.test_a_matching_mapping_reads_with_nothing_printed` | unchanged behaviour: the fixture's own mapping reads, prints nothing, raises nothing (the control of tests 1, 3 and 4) | passes (pin) |

**`datastorekit/tests/test_vectorized_get_payloads.py`**, 5 tests, one class
(`TestTheCallersPayloads`). Each opens a store with `build.open_pool` in a temporary directory, gets
two keypoints (positions 1.0 and 2.0) and their aliases `a1` and `a2` (offset 0.5), and checks as a
precondition that the two keys are on different shards. Every row is compared with a row from
another call, never with a literal serial (correction 5). The module docstring says why the
in-process stand-in is faithful (hazard 4).

| # | Test | Pins | Unfixed layer |
|---|---|---|---|
| 1 | `test_the_callers_dicts_are_unchanged` | `[06-…-payloads]`: after a call with `{"k": a1}`, the list equals a deep copy taken before it, and no dict holds `"k"` (contents compared, not identity: §4.4 (e)) | **FAIL**, `Lists differ: [{'weight': 0.25, 'k': <…keypoint_alias…>}, …] != [{'weight': 0.25}, {'weight': 0.75}]` |
| 2 | `test_the_same_list_twice_with_the_same_key_gives_the_same_rows` | kept behaviour: two calls with one list and one key give the same rows (serial, alias serial, weight), two distinct rows, each on `a1`, in the payloads' order | passes (pin) |
| 3 | `test_the_same_list_with_a_second_key_gives_that_shards_rows` | `[06-…-payloads]` and kept routing: the list used with `a1` then `a2` is unchanged; the `a2` call's rows equal a fresh-dict `a2` call's, are keyed on `a2`, share no serial with the `a1` rows, and are on `a2`'s shard and no other (read from the shard files) | **FAIL**, at the dict check, as test 1 |
| 4 | `test_a_payload_carrying_the_key_field_gets_the_pools_key` | kept merge order (correction 1): `[{"weight": 0.25, "k": a2}]` under `{"k": a1}` finds the row a fresh `[{"weight": 0.25}]` under `{"k": a1}` found: the same serial, its `k`'s serial `a1`'s, and not a new insert | passes (pin) |
| 5 | `test_a_reused_list_gives_the_rows_of_fresh_dicts` | kept behaviour: a list used with `a2` then with `a1` gives the rows of a fresh-dict `a1` call, keyed on `a1` | passes (pin) |

Neither module is ported, and neither is added to `PORTED`. Each has a `tearDownModule` that raises
if Ray was initialised, and the stand-in cases assert it in `tearDown`. No store is outside a
`tempfile` directory; no client is imported or named.

### 1.3 The contract (§2.4)

`docs/client-contract.md`:
- after §8's header line, a line saying that §9 is measured from the package at 08a's tree, and
  that its subsections name the rows of §1–§8 they supersede, which are not rewritten and carry a
  marker;
- **§9, Changes after `v0.2.0`**, with **§9.1 (prompt 08a)**: a table of two rows. The first
  supersedes §1 row 6's clause "except that a sharded table the store records and the mapping
  lacks raises `KeyError` at `:1015` before that message is reached", and gives what the layer now
  does at `:1020-1034`, `:1024-1025`, `:1026-1027`, `:1035-1040` and `:1055-1058`, including the
  duplicate row's refusal. The second supersedes **no row** (correction 2): no row of §1–§8 says
  what `object_get_vectorized` does to the caller's payloads; §1 rows 4 and 6 cite its getter and
  its refusals, and §8's "The caller's payloads are not changed" is of the actor's
  `_keyed_payloads`, which stays true. It gives `:3290-3314`, `:3311`, `:3307-3309`, `:3296-3299`
  and `:3302-3305`. Each row names its test module;
- the marker *(superseded in part by §9.1)* in §1 row 6, at the end of the superseded clause.

No other text of §1–§8 changed.

### 1.4 The records

This log; the board (header, 08a's row, the two issues moved from §3 to §4 with their closing
lines); `docs/OPEN_ISSUES.md` (the two rows deleted, 8 → 6, the date); `prompts/INDEX.md` (the
campaign's line, its open-issue count 4 → 2, the dates).

## 2. Deviations from the prompt

1. **The date.** The run crossed midnight: the baseline suite finished on 2026-10-10. The board's
   closing lines read "Closed (2026-10-10, prompt 08a)", where the prompt's §5 gives
   "2026-10-09"; the board's row, header and the two indexes carry 2026-10-10. **STRUCTURALLY
   REQUIRED.**
2. **Correction 1: the vectorized module's tests 2, 4 and 5 are pins, and test 4 compares the row
   found.** Found as the note says: on the unfixed layer only tests 1 and 3 fail (§4.2). Test 4
   compares the row found with the pool key's row, by serial and by its `k`'s serial, and checks it
   is not a new insert; under (d) it fails with `2 != 1`, a new row (§5). **STRUCTURALLY
   REQUIRED.**
3. **Correction 2: §9.1's row for the vectorized get supersedes no row.** Read so: §1 row 4 cites
   the getter at `:3295`, row 6 the two refusals, and §8's sentence is of the actor. The marker is
   on §1 row 6 only. **STRUCTURALLY REQUIRED.**
4. **Correction 3: the constructor test calls `ShardedPool(...)` itself**, inside
   `cluster.active()`, with the registry's arguments, `shards=3`, `read_table_config` and
   `serial_batch_sizes`, and `sharded_tables` less one class. **STRUCTURALLY REQUIRED.**
5. **Correction 4: the clients' sites** are as the note measured (§3); SI's calls pass a bare
   `delta_Nstar`, refused before the payload line under the package, fixed or not. The prompt's
   "unaffected, since each call now merges its own key" holds once SI converts them, as it must to
   adopt. **STRUCTURALLY REQUIRED** (an expectation corrected).
6. **Correction 5: no serial is a literal.** Every row is compared with a row from another call
   (§1.2). **STRUCTURALLY REQUIRED.**
7. **Correction 6: (b)'s open.** Found as the note says (§5 (b)). Recorded, no change.
8. **Correction 7: line numbers at 08a's tree.** Confirmed by `grep -n` on the fixed file (§1.1);
   §9.1 and this log cite them.
9. **Correction 8: `ResourceWarning`s at the high end.** 188 lines over the 469 (§4.1); the new
   modules alone give 8 lines, 4 warnings, one per refused constructor open of test 2
   (`[05-a-refused-open-leaves-its-engines-undisposed]`, 08b's). Not a stop.
10. **Addition 1: the tests were written before the fix and run on the unfixed layer first**, in
    the note's order: baseline, client reading, the two modules on the unfixed layer, the fixes,
    the contract, the high end and (a)–(e), then the final checks and the records. The "unfixed
    layer" was the checkout before the fix: its `datastorekit/` equals `88cac61`'s and `240028e`'s
    (`git diff --quiet` of each against `HEAD`, both empty), and `venv/`'s editable install
    imports it. No `git stash` was used. **IMPLEMENTATION CHOICE**, at the orchestrator's
    direction.
11. **Addition 2: the probes are outside `datastorekit/`**, under `<scratch>/probe/`, each printing
    `datastorekit.__file__` (§4.5 hazard 1). **IMPLEMENTATION CHOICE**, at the orchestrator's
    direction.
12. **Addition 3: each breakage is recorded as a diff, exactly as applied** (§5), and replays with
    `git apply --check` and `-R --check`. **IMPLEMENTATION CHOICE**, at the orchestrator's
    direction.
13. **Breakage (e) fails test 3 as well as test 1** (§4.4 names test 1). Test 3 also requires the
    dicts unchanged after its two calls, which (e) changes. **STRUCTURALLY REQUIRED** (an
    expectation corrected).
14. **The first module's test 2 leaves out each of the four sharded classes**, as subtests of one
    test, on one store; and it catches only the `RuntimeError`, so that a `KeyError` reaches the
    runner as raised (an ERROR, as (a) expects) and a pool that opens is closed before the test
    fails (so (b) leaves none open). **IMPLEMENTATION CHOICE.**
15. **The first module has a sixth test**, a matching mapping read with nothing printed: a pin, and
    the control of tests 1, 3 and 4. **IMPLEMENTATION CHOICE.**
16. **The contract's marker** is at the end of the superseded clause, inside §1 row 6's "When wrong
    or absent" cell, not after the row's last cell, which names the neutral client's mapping.
    **IMPLEMENTATION CHOICE.**
17. **Exports.** The high end and the breakages ran from a `git archive HEAD` export with the four
    changed files copied in (the tree being uncommitted); `cmp` of every tracked file and the two
    new modules against the checkout found no difference. The breakage diffs were made in a scratch
    `git` repository built from that export, so their `index` lines name the blob `4215bb8`, the
    fixed `ShardedPool.py` (`git hash-object` of the checkout's file). **IMPLEMENTATION CHOICE.**
18. **`uv`'s cache.** `venv-high` was resolved `--offline` from `uv`'s default cache
    (`~/.cache/uv`); nothing was downloaded. **IMPLEMENTATION CHOICE.**
19. **The breakage suites ran three, then two, at a time**, which is why they took 417 s and 249 s
    against 150–290 s alone. **IMPLEMENTATION CHOICE.**

No UNINTENDED DRIFT was found.

## 3. The clients (§2.5)

Read only through `git -C <client> show|grep|status|rev-parse|branch`; nothing imported, run or
written. Commits and statuses, the same at the start and at the end:

| Client | Commit | Branch | `git status --short` |
|---|---|---|---|
| SGK | `b510bc9` | `handover-remedial` | empty |
| CPBH | `52142d7` | `main` | 23 untracked entries (none read) |
| SI | `7bb3efd` | `main` | empty |

**The sites**, by `git grep -n object_get_vectorized HEAD`, then each read:
- **SGK: 17 calls in `main.py`** (`:1770`, `:1996`, `:2191`, `:2268`, `:2587`, `:2929`, `:2977`,
  `:3037`, `:3077`, `:3166`, `:3463`, `:3518`, `:3560`, `:3689`, `:3786`, `:3827`, `:3961`; 19 lines
  name the method, `:2158` and `:2582` being comments). Each is `task_builder=lambda x:
  pool.object_get_vectorized("<class>", x["shard_key"], payload_data=x["payload"])` in a
  `RayWorkPool` whose handlers are `None`, over a work list built just before as a comprehension
  of fresh dicts. A text scan (`<scratch>/probe/scan_sites.py`, run with `python3 -I` on `git show`
  output) found no later line naming any of the 17 work lists (the first site, `:1770`, read in
  full, reads `query_queue.results` zipped with its binned inputs). **No line reads a payload list back.**
  Beyond `main.py`: `ComputeTargets/tests/test_quadsource_integral_parent_main.py:638-644` is a
  stand-in of the method that already copies (`dict(payload, **shard_key)`), called at `:926` with
  a literal list; `Datastore/tests/test_read_only_pool.py:600` passes a literal list (a module this
  package ported); the other `ComputeTargets/tests/` hits are `ast` scans of `main.py`.
- **CPBH: 7 calls in `main.py`** (`:196`, `:358`, `:408`, `:476`, `:614`, `:666`, `:739`), each
  with `x["shard_key"]`, a bare `beta_value` (`"shard_key": key`, binned on `coupling.shard_key`),
  so refused by the package's shard-key test before the payload line, fixed or not (CPBH's
  checklist, item 6).
- **SI: 15 calls**, 10 in `main.py` (`:224`, `:252`, `:319`, `:448`, `:592`, `:874`, `:903`,
  `:967`, `:1018`, `:1044`; `:419` is a docstring), 3 in `plot_InstantonSolutions.py` (`:697`,
  `:700`, `:733`), 2 in `plotting/fetch.py` (`:127`, `:166`; `:143` is a docstring); 4 test stubs
  of the signature. Every one passes a bare `delta_Nstar` (SI's checklist, item 6). The `main.py`
  lists are built inside each lambda; `fetch.py`'s and the plot's are built just before and only
  the results are read after. `plot_InstantonSolutions.py:697-702` passes one list to two calls:
  under the package, once converted to the mapping form, each call now merges its own key into
  copies.

**Finding: no client reads a payload list back after a vectorized get.** No stop. Neither fix
changes anything a client stores.

## 4. Verification performed

### 4.1 The suite

Each run is `<python> -m unittest discover -s datastorekit/tests -t .` from the tree's root, in the
foreground, `PYTHONPATH` unset (or set to the export for the breakages), output written to
`<scratch>/out/` and the verdict grepped.

| # | When | Venv | Verdict | `ResourceWarning` lines |
|---|---|---|---|---|
| 1 | at dispatch, before any change | `venv/` | `Ran 458 tests in 164.733s` / `OK` | 0 |
| 2 | the two new modules alone, before the fix | `venv/` | `Ran 6 tests` / `FAILED (errors=5)`; `Ran 5 tests` / `FAILED (failures=2)` (§4.2) | — |
| 3 | after the two fixes | `venv/` | `Ran 469 tests in 289.438s` / `OK` | 0 |
| 4 | the high end, the fixed export | `venv-high` | `Ran 469 tests in 291.233s` / `OK` | 188 |
| 5 | the two new modules alone, the high end | `venv-high` | `Ran 11 tests` / `OK` | 8 |
| 6 | the final tree, with the records | `venv/` | `Ran 469 tests in 150.518s` / `OK` | 0 |

**458 before, 469 after, at both ends; N = 11** (`loadTestsFromNames` of the two modules,
`countTestCases()` → `11`). The 458 pass unchanged in every run with the fixes.

### 4.2 The new tests on the unfixed layer (hazard 2)

Run in the checkout after the modules were written and before either fix, `datastorekit.__file__`
= the checkout's (`venv/`'s editable install):
- `test_unsupplied_sharded_table`: `Ran 6 tests` / `FAILED (errors=5)`. **ERROR** test 1
  (`KeyError: 'Sample'`) and test 2's four subtests (`KeyError: 'Tessera'`, `'Sample'`, `'Trace'`,
  `'Weave'`), each raised at `ShardedPool.py:1026` (`attr = self._sharded_tables[row.table]`),
  through `__init__` `:260` for test 2. Tests 3–6 pass.
- `test_vectorized_get_payloads`: `Ran 5 tests` / `FAILED (failures=2)`. **FAIL** test 1 and test
  3, each at the dict comparison: `Lists differ: [{'weight': 0.25, 'k': <…keypoint_alias…>}, …] !=
  [{'weight': 0.25}, {'weight': 0.75}]`. Tests 2, 4 and 5 pass.

With the fixes, all 11 pass. So the four tests that fail do so for the issues' reasons, and the
seven others are declared pins (tests 3–6 of the first module, tests 2, 4 and 5 of the second).

### 4.3 The venvs

| Venv | Python | Ray | SQLAlchemy | SQLite | `datastorekit` |
|---|---|---|---|---|---|
| `venv/` | 3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.43.0 | 2.0.39 | 3.53.4 | 0.2.0, editable, the checkout; `black` 25.1.0 |
| `<scratch>/venv-high` | 3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)] | 2.55.1 | 2.0.46 | 3.53.4 | 0.2.0, editable, `<scratch>/exports/fixed` |

`venv-high`: `uv` 0.12.20; `uv venv --offline -p /opt/local/bin/python3.13 <scratch>/venv-high`;
`uv pip install --offline --python <scratch>/venv-high/bin/python "ray==2.55.1"
"sqlalchemy==2.0.46"`; `uv pip install --offline --no-deps --python … -e <scratch>/exports/fixed`.
Every pin resolved offline. `uv pip freeze`: attrs 26.1.0, certifi 2026.7.22, charset-normalizer
3.5.2, click 8.5.0, datastorekit (editable, the export), filelock 4.0.12, idna 3.20, jsonschema
4.26.0, jsonschema-specifications 2025.9.1, msgpack 1.2.3, packaging 26.3, protobuf 7.36.2, pyyaml
6.0.3, ray 2.55.1, referencing 0.37.0, requests 2.34.2, rpds-py 2026.9.1, sqlalchemy 2.0.46,
typing-extensions 4.16.0, urllib3 2.8.0.

### 4.4 The checks

- **The port check** (in place of `compare_with_source.py`, retired by U27): `./venv/bin/python
  docs/extraction/compare_ported_tests.py` exits 0 before and after, its 106 lines byte-identical;
  its last line: `OK: 20 module(s) keep their source's tests, classes and assertion skeletons; 1
  test(s) declared not ported`. Neither new module is in `PORTED`.
- **`black`**: `black --check datastorekit docs` leaves **66** files unchanged before and **68**
  after; `black` on the three changed Python files left them unchanged.
- **The layer guard**: `test_layer_is_generic` passes (`Ran 8 tests` / `OK`), `KNOWN_HITS` at its
  one entry (`datastorekit/tools/shard_key_audit.py:188 wavenumber`). The new modules name no
  client; their words were also checked against `tests/data/client_vocabulary.json`, and the only
  matches are generic English words of that file (`from`, `name`, `registry`, …), not client
  identifiers.

### 4.5 The hazards (§3)

1. **The editable install.** Every probe and every breakage printed `datastorekit.__file__`: the
   checkout's for runs in it, the export's for the high end and for each breakage (§5).
2. **The unfixed layer is the reference.** §4.2.
3. **The duplicate row.** The guard is after the membership test (§1.1); test 5 of the first module
   pins the refusal, and passes on the unfixed layer, the fixed layer and under (b).
4. **The stand-in pool runs in-process.** The second module's docstring says so, and why the test is
   faithful: the merge is in the driver, before the call is made.
5. **No other line of `ShardedPool.py`.** `git diff` of the file is the two hunks of §1.1.
6. **Prose.** No comment or docstring of the layer changed; `KNOWN_HITS` is unchanged.
7. **Line numbers.** §9.1 and this log cite 08a's tree (§1.1); earlier citations are of their own
   trees, and are not rewritten.

## 5. The deliberate-breakage record (§4.4)

**The method.** `<scratch>/probe/make_breaks.py` wrote each breakage into a scratch `git`
repository made from the fixed export (`<scratch>/breaks/repo`), took `git diff`, and restored the
file; the repository was clean after. `<scratch>/probe/run_break.sh <name>` then made a fresh copy
of that tree (`<scratch>/exports/break-<name>`), ran `git apply --check`, `git apply` and
`git apply -R --check` (all passed for all five), printed `datastorekit.__file__` (the copy's,
every time), ran the whole suite with `venv/`'s interpreter and `PYTHONPATH` set to the copy, and
reversed the diff with `git apply -R`. The checkout was never broken. The diffs below are the
files applied, byte for byte.

**(a) The guard removed** (the unfixed loop).

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 4215bb8..a5f2a1a 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -1023,8 +1023,6 @@ class ShardedPool:
             for row in sharded_table_data:
                 if row.table not in missing_supplied_sharded:
                     missing_read_sharded.add(row.table)
-                if row.table not in self._sharded_tables:
-                    continue
                 attr = self._sharded_tables[row.table]
                 if row.key_attr != attr:
                     mismatching_key_attr[row.table] = {
```

`Ran 469 tests` / `FAILED (errors=5)`: **ERROR** the first module's test 1 (`KeyError: 'Sample'`)
and test 2's four subtests (`KeyError: 'Tessera'`, `'Sample'`, `'Trace'`, `'Weave'`). The other 464,
the 458 among them, pass.

**(b) The guard placed before the membership test**, so an unsupplied table is skipped unrecorded.

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 4215bb8..dc3065a 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -1021,10 +1021,10 @@ class ShardedPool:
             mismatching_key_attr = {}
             missing_supplied_sharded = set(self._sharded_tables.keys())
             for row in sharded_table_data:
-                if row.table not in missing_supplied_sharded:
-                    missing_read_sharded.add(row.table)
                 if row.table not in self._sharded_tables:
                     continue
+                if row.table not in missing_supplied_sharded:
+                    missing_read_sharded.add(row.table)
                 attr = self._sharded_tables[row.table]
                 if row.key_attr != attr:
                     mismatching_key_attr[row.table] = {
```

`Ran 469 tests` / `FAILED (failures=5)`: **FAIL** test 1 (`AssertionError: RuntimeError not
raised`) and test 2's four subtests (`AssertionError: the store opened without <class>`). The other
464 pass; test 5 (the duplicate row) passes, since its table is supplied. **What the open does
instead** (`<scratch>/probe/probe_b.py`, with (b) applied to its copy): through the fixture,
`_read_shard_data` returns, having printed nothing; through the constructor, for each of `Tessera`,
`Sample`, `Trace` and `Weave` left out, the pool prints `>> Opened existing sharded datastore
"<primary>" with 3 shards` and opens, its `_sharded_tables` lacking the class. Ray was never
initialised.

**(c) The in-place update restored.**

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 4215bb8..35d57df 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -3308,7 +3308,8 @@ class ShardedPool:
             self._ShardKeyStoreIdGetter(shard_key[shard_key_field])
         ]
 
-        payload_data = [{**value, **shard_key} for value in payload_data]
+        for value in payload_data:
+            value.update(shard_key)
         return self._shards[shard_id].object_get.remote(
             cls_name, payload_data=payload_data
         )
```

`Ran 469 tests` / `FAILED (failures=2)`: **FAIL** the second module's tests 1 and 3, each at the
dict comparison. The other 467 pass.

**(d) The merge order reversed** (`{**shard_key, **value}`).

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 4215bb8..65b1257 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -3308,7 +3308,7 @@ class ShardedPool:
             self._ShardKeyStoreIdGetter(shard_key[shard_key_field])
         ]
 
-        payload_data = [{**value, **shard_key} for value in payload_data]
+        payload_data = [{**shard_key, **value} for value in payload_data]
         return self._shards[shard_id].object_get.remote(
             cls_name, payload_data=payload_data
         )
```

`Ran 469 tests` / `FAILED (failures=1)`: **FAIL** the second module's test 4, `AssertionError: 2 !=
1`: the payload's own `k` (`a2`) won, and the get inserted a new row on `a1`'s shard instead of
finding `a1`'s. The other 468 pass.

**(e) The list copied and its dicts updated in place.**

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 4215bb8..74212b6 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -3308,7 +3308,9 @@ class ShardedPool:
             self._ShardKeyStoreIdGetter(shard_key[shard_key_field])
         ]
 
-        payload_data = [{**value, **shard_key} for value in payload_data]
+        payload_data = list(payload_data)
+        for value in payload_data:
+            value.update(shard_key)
         return self._shards[shard_id].object_get.remote(
             cls_name, payload_data=payload_data
         )
```

`Ran 469 tests` / `FAILED (failures=2)`: **FAIL** the second module's tests 1 and 3, each at the
dict comparison (§2 item 13). The other 467 pass.

**No existing test catches any of the five** (as the note found over the 458): the 458 pass under
every one. Every breakage fails at least one new test, and each fails exactly the tests §4.4
expects, with (e)'s test 3 in addition.

## 6. Observations not acted on

1. **The duplicate row's message misdescribes the case.** A table the primary records twice, and
   the constructor supplies, is refused with the mismatch `RuntimeError` and printed under "The
   following sharded tables are configured in the existing ShardedPool, but were not supplied to
   the constructor", although it was supplied: the membership test reads the set the loop
   discards from. `sharded_tables.table` carries no unique constraint
   (`_create_engine`; `shard_store_fixtures.write_hand_built_primary`), but the layer writes one
   row per key of the constructor's mapping (`_write_shard_data`), so only a hand-edited primary holds a duplicate. Unchanged by
   08a, as the prompt's §2.1 requires, and pinned by test 5. No issue is opened: the open is
   refused, and the case needs a primary edited by hand.
2. **High-end `ResourceWarning`s**: 188 lines over the 469, of which 8 (4 warnings) are the first
   module's four refused constructor opens: `[05-a-refused-open-leaves-its-engines-undisposed]`,
   08b's.
3. **CPBH's and SI's bare shard keys** are refused by the package before the payload line, so
   neither fix reaches their calls until they convert to the mapping form (their checklists, item
   6). Already recorded there; 10's addenda (U37) are where "the vectorized-payload hazard gone"
   is said.
4. **`docs/adoption/stochasticinstantons.md:255-256`** says the package "adds it to each payload
   dict in place (`datastorekit/SQL/ShardedPool.py:3309-3310`; …)". True of `v0.2.0`, against which
   it was measured; 10's addendum (U37) records the change, and the checklist is not rewritten
   (`CLAUDE.md` rule 6).

## 7. Issues

- **Closed:** `[02-an-unsupplied-sharded-table-raises-keyerror]` and
  `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]`, each moved to the board's §4
  with a "Closed (2026-10-10, prompt 08a)" line naming its fix and its test module.
- **Opened, narrowed, changed:** none.

The index goes from **8 to 6 open**: 2 on this board (`[01-package-prose-names-sgks-layout]`, 09's;
`[05-a-refused-open-leaves-its-engines-undisposed]`, 08b's), 4 inherited.

## 8. State handed to the next prompt

- `HEAD` is this commit. The tree is clean but for the ignored entries of dispatch (`.idea/`, the
  `__pycache__/` directories, `venv/`). `venv/` is unchanged.
- **Not pushed, not tagged.** `origin/main` is `102f225`; the tags are `v0.1.0` and `v0.2.0`. The
  version stays `0.2.0`; 10 releases `v0.2.1`.
- **The suite is 469** in `venv/` and at the high end. `compare_ported_tests.py`: 20 modules, one
  test declared not ported, exit 0. `black --check datastorekit docs`: 68 files.
- **For 08b:** `ShardedPool.py`'s line numbers from `:1026` on are 08a's (+2 to `:3309`, then +1).
  The first module's test 2 refuses four constructor opens per run, so it adds four undisposed
  engines' warnings at the high end; a test that counts unclosed connections across the suite will
  see them.
- **For 09:** the two new modules' prose names no SGK path or campaign; `KNOWN_HITS` is unchanged.
- **For 10:** `docs/client-contract.md` §9 exists with §9.1; 08b and 10 add their own subsections.
- **Scratch** (not in the repository): `<scratch>` =
  `/private/tmp/claude-35086/-Users-ds283-Documents-Code-DatastoreKit/fc638bd4-0b25-4add-8958-6f46edf57049/scratchpad/agent-08a`,
  holding `venv-high`, `exports/` (`fixed`, `break-a` … `break-e`), `breaks/` (the five diffs and
  the scratch repository), `out/` (every run's output) and `probe/`.
