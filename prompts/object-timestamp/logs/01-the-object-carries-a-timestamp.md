# Log 01 — the object carries a timestamp

**Subject:** Give DatastoreObject an optional, read-only timestamp · **Commit:** `1b2f91a` ·
**Date:** 2026-10-12 · **Model:** Claude Opus 5.5 · **Result:** landed; unpushed and untagged; not
yet reviewed.

`datastorekit.DatastoreObject` takes a keyword-only `timestamp`, `None` by default, keeps it as
`self._timestamp`, and exposes it as a read-only property with no setter and no deleter (U1). The
layer never sets it and never reads it: a factory that reads a row of a class registered with
`"timestamp": True` may pass the row's `timestamp`. `store_id` and `available` are `v0.2.3`'s,
unchanged by `ast`. No message, refusal or exception changed, and nothing the layer writes or reads.
`pyproject.toml` stays at `0.2.3`.

`TestTheVersionObject`'s expected dict gains `"_timestamp": None` (U2). A new module of **5**
tests, `datastorekit/tests/test_object_timestamp.py`, pins the change on the stand-in pool, with a
neutral stamped class and its static factory in a new module, `datastorekit/tests/client/stamped.py`,
outside the neutral client's registry, which is unchanged (U3). The suite goes from **504 to 509**,
in `venv/` and at the high end. Breakage (a), `v0.2.3`'s `object.py`, fails tests 1, 2, 3 and 5
and `TestTheVersionObject`'s two subtests, and nothing else in the 509; test 4 passes under it,
as the orchestrator's correction 1 says it must. Each of (b)–(e) fails its tests.

Under real Ray, `docs/extraction/ray_smoke_run.py`, unchanged, passes every step at both ends
(exit 0, no Ray process before or after) (U4). `docs/client-contract.md` gains a head line and
§9.6; `docs/extraction-verification.md` gains §4.9. No issue was opened or closed: the index stays
at **4 open**.

No client was written, run, imported or opened; nothing was pushed, tagged or downloaded. Ray was
started only by the smoke script, twice. Another session's Ray instance was up for part of the
prompt; it was not touched, and the smoke runs were taken after it had gone (§3 hazard 6).

Prompt: [`../01-the-object-carries-a-timestamp.md`](../01-the-object-carries-a-timestamp.md), with
the orchestrator's dispatch note §0: five corrections, its additions, its checked facts and its
conventions. §2 classifies each.

`<scratch-ot01>` below is `<session scratchpad>/agent01`, outside the repository. Times are BST,
2026-10-12.

---

## 1. What shipped

### 1.1 The object (§2.1)

`datastorekit/object.py`, 18 lines added and 1 removed (`git diff --numstat`). Line numbers are
`1b2f91a`'s:

- `from datetime import datetime` (`:1`), before the existing `typing` import.
- `__init__(self, store_id: Optional[int], *, timestamp: Optional[datetime] = None)` (`:10-14`),
  which `black` wraps over three lines; its body is `self._my_id = store_id`, as before, and
  `self._timestamp = timestamp` (`:14`).
- `store_id` (`:16-21`) and `available` (`:23-25`), unchanged, in their order, before the new
  property.
- `timestamp` (`:27-38`), `@property`, returning `self._timestamp`, typed `Optional[datetime]`,
  with no setter and no deleter (`DatastoreObject.timestamp.fset` and `.fdel` are `None`). Its own
  docstring says, in neutral terms, that the value is the row's `timestamp`, which the layer stamps
  at insert for a class whose `register()` declares `"timestamp": True`; that a factory that reads
  such a row may pass it by the keyword `timestamp`; when it is `None` (an object not yet stored,
  one built from an insert, one whose factory does not pass it, one whose table has no such
  column); that the layer neither sets nor reads it; and that it is read-only. The class's
  three-line docstring is unchanged.
- The guard (`test_layer_is_generic`) passes on it: it names no client, and no client's class,
  table or figure.

**Acceptance 1, by `ast`** (`<scratch-ot01>/probe/ast_compare.py`, run on `git show
0de2b16:datastorekit/object.py` and on the tree): the class's name, bases and docstring are equal;
its methods are `['__init__', 'store_id', 'available']` at `v0.2.3` and `['__init__', 'store_id',
'available', 'timestamp']` here. `ast.dump` of `store_id` and of `available`, each whole
(decorators, arguments, body), is equal at the two trees. `__init__`'s arguments are equal but for
`kwonlyargs`, `[]` → `[timestamp: Optional[datetime]]` with `kw_defaults` `[None]`; its decorators
and return annotation are equal; its body at `v0.2.3` is a prefix of the tree's, and the one extra
statement is `self._timestamp = timestamp`. The added method `timestamp` is decorated `property`,
takes `self`, returns `Optional[datetime]`, has a docstring, and its body less the docstring is
`return self._timestamp`. The module's only other added statement is `from datetime import
datetime`; none is removed. `store_id` and `available` come before `timestamp`.

### 1.2 `test_declared_facts.py` (§2.2)

In `TestTheVersionObject`, the expected dict is now `{"_my_id": 1, "_timestamp": None, "label":
"standin", "_deserialized": True}`, which `black` splits over six lines (6 added, 1 removed).
Nothing else in the module changed: not its docstring, not the test's name. The port check still
reports "20 module(s) … 1 test(s) declared not ported" (§4.2).

### 1.3 The stamped class and its factory (§2.3)

**`datastorekit/tests/client/stamped.py`**, new (101 lines), outside `registry.py`:

- `STAMPED_TABLE = "stamped_tally"`, the registry name, which is also the class's name and its
  table's; `STAMPED_COLUMN = "tally"`, the integer's column;
- `stamped_tally(store_id, tally, timestamp=None)`: a replicated `DatastoreObject` with one integer,
  `tally`; its constructor passes `timestamp` to `super().__init__` **by keyword**, and its own
  `timestamp` parameter defaults to `None`, so that the factory's insert branch passes nothing;
- `stamped_tally_factory`: a subclass of `SQLAFactoryBase` with **static** `register` and `build`
  only, registered as a class. `register()` declares `"version": False`, `"timestamp": True` and
  `sqla.Column("tally", sqla.Integer, nullable=False)`. `build` selects the row's `serial` and
  `timestamp` by `tally`: found, it returns `stamped_tally(row.serial, tally,
  timestamp=row.timestamp)`, marked `_deserialized`; not found, it inserts `{"tally": tally}`
  (carrying a payload's `serial`, as `gauge_setting_factory.build` and
  `instances.scalar_entry_factory.build` do) and returns the object with **no** timestamp, marked
  `_new_insert`;
- `stamped_registry()`: `(factories, replicated_tables)`, a copy of the registry's factories with
  `stamped_tally_factory` under `STAMPED_TABLE`, and a copy of the registry's replicated tables with
  `STAMPED_TABLE` at the end, as `instances.instance_registry()` does.

Both classes are at module level. No `inventory_spec` is defined, so `test_store_inventory`'s count
of 12 holds (hazard 3). The neutral client's `registry.py`, `objects.py`, `factories.py` and
`instances.py` are unchanged.

### 1.4 The test module (§2.4)

**`datastorekit/tests/test_object_timestamp.py`**, new (257 lines), 5 tests in 5 classes, on the
stand-in pool, every store in a `tempfile` directory. `tearDownModule` asserts Ray is not
initialised, and so do test 2's `tearDown` and test 5's last line. `TestThroughThePool` builds its
pools itself (`open(read_only=False)`), as `test_factory_instances._StoreCase.open` does, with
`stamped_registry()`'s factories and replicated tables and a `read_only` argument;
`standin_pool.py` is unchanged.

| # | Test | What it does |
|---|---|---|
| 1 | `TestTheArgumentAndTheProperty.test_the_timestamp_is_none_by_default_and_what_was_given` | `DatastoreObject(3)`: `timestamp` `None`, `store_id` 3, `available` true. `DatastoreObject(None)`: `timestamp` `None`, `available` false, `store_id` raises `RuntimeError` whose text is exactly "Attempt to read datastore id before it has been set". `DatastoreObject(3, timestamp=STAMP)`, `STAMP = datetime(2026, 10, 12, 9, 30, 15, 123456)`: `assertIs(obj.timestamp, STAMP)`, `store_id` 3, `available` true |
| 2 | `TestThroughThePool.test_the_stamp_is_the_rows_and_the_layer_does_not_fill_it` | On a fresh store: a get of `tally=17` answers a `stamped_tally`, `_new_insert`, `tally` 17, `timestamp` `None`; the pool is closed (in a `finally`). The raw read (`sp.table_columns`, `sp.shard_rows`) finds one value in the `timestamp` column, the same on each of the three shards, a `str`. A read-write reopen: the get answers `_deserialized`, the same serial, and a `datetime` equal to `datetime.fromisoformat` of that text; the same get sent to each shard's actor directly, `ray.get(actor.object_get.remote("stamped_tally", tally=17))` under the stand-in's `ray.get`, answers `_deserialized`, the same serial and the same `datetime` (a sub-test per shard). A read-only reopen answers the same. Last, the raw read is unchanged: nothing rewrote the stamp |
| 3 | `TestReadOnly.test_the_timestamp_cannot_be_assigned_or_deleted` | For `DatastoreObject(3, timestamp=STAMP)` and `stamped_tally(3, 17, timestamp=STAMP)` (a sub-test each): `obj.timestamp = datetime(2000, 1, 1)` raises `AttributeError`, so does `del obj.timestamp`, and `obj.timestamp` is still `STAMP` (`assertIs`) |
| 4 | `TestKeywordOnly.test_a_second_positional_argument_is_refused` | `DatastoreObject(3, STAMP)` raises `TypeError` |
| 5 | `TestSerialisation.test_stamped_and_unstamped_objects_round_trip_cloudpickle` | `stamped_tally(4, 17, timestamp=STAMP)` and `stamped_tally(5, 18)` (a sub-test each) through `ray.cloudpickle.dumps` / `loads`: the copy is a new `stamped_tally` with the same `store_id`, `tally` and `timestamp` (`STAMP`; `None`); Ray is not initialised afterwards |

**Test 2's comparison** is by parsing: the raw read returns SQLite's text, `YYYY-MM-DD
HH:MM:SS.ffffff`, and `datetime.fromisoformat` of it is compared for equality with the `datetime`
each get answers (the orchestrator's addition).

### 1.5 The smoke run (§2.5)

`docs/extraction/ray_smoke_run.py` is unchanged (SHA-256
`032036798e101d610a4ac0185ea4eaa7f1db0fe58f52c48ad9f3707548a6a92a`, as verification §4.8
records, the same in this checkout and in each export). It passed every step at both ends (§4.3).

### 1.6 The documents (§2.6–§2.7)

- **`docs/client-contract.md`**, 15 lines added and none removed. The head gains §9.6's line after
  §9.5's (`:40-41`), in §2.6's words. **§9.6 `object-timestamp` prompt 01** follows §9.5, at the
  end of the file: a preamble (one change, the README's U1, the user's ruling; nothing the layer
  writes or reads changes, and no message, refusal or exception; a client passing `store_id` alone
  meets one more key in `vars()`) and one row, "`DatastoreObject.timestamp`", whose "Supersedes" is
  none (§6's `DatastoreObject` row and §2's `timestamp` row still hold, each said), whose "What
  holds" gives every item §2.6 lists with `object.py:10-14`, `:14`, `:16-25`, `:27-38`,
  `SQL/Datastore.py:809-815` (in `_insert`, `:760-843`) and `SQL/ShardedPool.py:3203`, and whose
  "Pinned by" is `tests/test_object_timestamp.py` (tests 1–5) and `TestTheVersionObject`. No marker
  is set on any row of §1–§9.5.
- **`docs/extraction-verification.md`**, 173 lines added and none removed: **§4.9**, between
  §4.8.3's closing fence and the two blank lines and `---` before `## 5. The pin (U42)`, in §4.8's
  form: an italic preamble, the script unchanged (its SHA-256), the environment of each run, a
  table, what it shows, and the two outputs (§4.9.1, §4.9.2), with the scratch path written
  `<scratch-ot01>`.

### 1.7 The records

- **This campaign's board**: the header (in progress; 01 landed, not yet reviewed) and 01's row
  (landed, `1b2f91a`, the log). The decisions table, §2, §3 and §4 are unchanged: no issue is
  held.
- **This campaign's README**: a sentence in its header, and §2's row for 01 (landed).
- **`prompts/INDEX.md`**: the header (1 in progress) and the campaign's status.
- **`docs/OPEN_ISSUES.md`**: unchanged, **4 open** (no issue opened or closed).
- **This log.**

---

## 2. Deviations from the prompt

1. **Correction 1: test 4 passes under breakage (a).** `v0.2.3`'s constructor refuses a second
   positional argument with the same `TypeError` as U1's form. Test 4 is not bent to fail under
   (a): it matches no message, and folds in no keyword call. Breakage (c) fails it (§5). §2.4's
   last paragraph and §4.4 (a) are read as corrected, and §6's third stop is not applied to it.
   **STRUCTURALLY REQUIRED.**
2. **Correction 2: the column is not `value`.** The column is `tally`, and so are the object's
   attribute and the payload's key: one name for the three, none of them in the vocabulary, rather
   than `instances.scalar_entry`'s precedent of a `value` attribute and key over a differently
   named column, so that no new name of the package is a client's column (§4.5).
   **STRUCTURALLY REQUIRED.**
3. **Correction 3: (d) fails test 3 too.** Test 3 checks `obj.timestamp` is still `STAMP` after the
   refused assignment and deletion, so under (d) it fails in both sub-tests (§5). Recorded as found.
4. **(a) fails test 1 with `AttributeError`, not `TypeError`.** §2.4's last paragraph and the
   orchestrator's prototype give test 1's error under (a) as `TypeError`, at the stamped half.
   Test 1 follows §2.4's order, the unstamped objects first, so under (a) it errors at its first
   read of `timestamp`, `AttributeError: 'DatastoreObject' object has no attribute 'timestamp'`,
   before it reaches the stamped half: `v0.2.3`'s object has no `timestamp` at all. It fails, for
   the reason the change exists, so §6's third stop does not apply. The module's docstring says
   so. Recorded as found; the form is an **IMPLEMENTATION CHOICE**.
5. **Correction 4: the clients moved.** ChamPBH's `HEAD` was `a72ca5e` at this prompt's start, not
   the dispatch's `f5fe207`; SGK and SI were as the dispatch says. During the prompt, other sessions
   committed in SGK (`d03a643`, its index then clean) and in ChamPBH (`70184f1`) (§4.7). Each is
   recorded at the start and the end, and no command of this prompt wrote, ran, imported or opened
   anything of a client. Recorded as found.
6. **Correction 5: line numbers.** Every line the prompt cites held, with the note's readings:
   `_insert` begins at `SQL/Datastore.py:760` (it ends at `:843`), its timestamp block is
   `:809-815`; §4.8.3's closing fence was `docs/extraction-verification.md:1017`, followed by two
   blank lines, `---` at `:1020` and `## 5. The pin (U42)` at `:1022`; `pool._shards` is read only
   on an open pool (test 2's direct gets are inside the read-write reopen). Recorded as found.
7. **The orchestrator's additions**, each followed as given, each an **IMPLEMENTATION CHOICE** at
   the orchestrator's direction: the order of work (the baseline; §2.1 and §2.2, then the existing
   suite at the high end, 504, before the new modules; §2.3 and §2.4 and the suite at both ends;
   the breakages, each in its own export at the high end, (a) with the full suite; the smoke runs;
   the documents and records; the final checks); every export installed editable into a fresh
   offline venv, no `PYTHONPATH`, every scratch-venv command run from the export's root, and
   `datastorekit.__file__` printed once in each venv (§4.1); test 2's comparison by
   `datetime.fromisoformat`; the stamped constructor's `timestamp` passed by keyword and defaulting
   to `None`; the `ast` comparison (§1.1); the vocabulary check by a script (§4.5); the smoke runs
   as `factory-defaults` log 01 §4.3 took them.
8. **Test 2 closes its first pool in a `finally`.** The first run of (a) on the full suite gave the
   expected `failures=2, errors=4`, but 4 `ResourceWarning` lines ("unclosed database"): test 2's
   first get raised with its pool open, and the pool was collected later. With the get inside
   `try` / `finally: self.close(pool)` (its assertions after the close), the rerun of (a) gave the
   same failures and 0 `ResourceWarning` lines (§5). The reopens were already closed in a
   `finally`. **IMPLEMENTATION CHOICE.**
9. **Test 2's pool helper is restated, not imported.** `_StoreCase.open` takes no `read_only`,
   which the read-only reopen needs; the module restates it with that argument (§2.3 allows
   either). **IMPLEMENTATION CHOICE.**
10. **More than §2.4 lists, in tests 2, 3 and 5.** Test 2 also checks the answers' class and
    `tally`, that the raw value is a `str`, that the pool has three shard actors, that each direct
    get is `_deserialized` under the same serial, and, last, that the raw read is unchanged after
    the reopens. Test 3 runs on a `DatastoreObject` and on a `stamped_tally`, to show a subclass
    inherits the read-only property (contract §9.6's "a subclass must not assign
    `self.timestamp`"). Test 5 checks the copy is a new object. **IMPLEMENTATION CHOICE.**
11. **`STAMPED_TABLE` and `STAMPED_COLUMN`** are module constants of `stamped.py`, which the test
    module imports, so that the names are written once. **IMPLEMENTATION CHOICE.**
12. **The gate, as found.** `git diff --stat 0de2b16 HEAD -- datastorekit pyproject.toml docs` is
    not empty: it shows `docs/OPEN_ISSUES.md`, changed by `2a86f92`, which the note's gate allows
    (a later commit touching only `prompts/` or `docs/OPEN_ISSUES.md`); `datastorekit/` alone is
    empty, as the prompt's gate asks. The local `origin/main` ref is `2a86f92`, not the dispatch's
    `83068cb`; it is an ancestor of `main`. No `git fetch` or `ls-remote` was run, so this is the
    ref as the checkout holds it. Recorded as found.
13. **The smoke runs were taken without a stop.** A foreign Ray instance appeared during the prompt
    (§3 hazard 6) and had gone before the runs were due. Recorded as found.

No UNINTENDED DRIFT was found.

---

## 3. The hazards (§3)

1. **The guard.** `test_layer_is_generic` passes in every run of the suite, and on its own at the
   end (§4.2). `object.py`'s new names, strings and docstring name no client, and no client's
   class, table or figure.
2. **A property with a setter, or a positional argument.** Breakage (b), a setter, fails test 3;
   breakage (c), `timestamp` positional-or-keyword, fails test 4 (§5).
3. **The inventory's count of 12.** `stamped.py` defines no `inventory_spec`;
   `test_store_inventory` passes in every run.
4. **The port check** reports "OK: 20 module(s) … 1 test(s) declared not ported" after §2.2, and at
   the end (§4.2).
5. **Additive documents.** `git diff` of `docs/client-contract.md` and
   `docs/extraction-verification.md` shows `+` lines only (0 lines beginning `-` other than the
   `---` header). Nothing else under `docs/` changed.
6. **No Ray in the suite; Ray only through the script.** Test 5 imports `ray.cloudpickle`, which
   starts nothing; test 2's direct actor calls go through the stand-in's `ray.get`. The module's
   `tearDownModule` passes in every run. Ray was started only by the smoke script, from scratch
   venvs, twice, one after the other, with no suite running. **A foreign Ray instance**: at
   01:29:36, by the script's rule (`<scratch-ot01>/probe/raycheck.py` loads the script and runs its
   `ray_processes()`), 24 Ray processes were up: a `gcs_server` and a `raylet` under another
   repository's venv, a `SerialPoolBroker`, `Datastore` actors and workers (session directory
   `/tmp/ray/session_2026-10-12_01-12-29_749310_88798`, created at 01:12, after this prompt's
   start-of-prompt check found none at 01:01). It was not touched, signalled or connected to. By
   01:40:20 it had gone (0 processes), and the smoke runs followed at 01:40:40 and 01:41:04, each
   preceded and followed by 0 (§4.6). The suite runs at 01:29 and after were in-process only.
7. **Offline only.** Every venv and install was `uv … --offline`; every pin resolved offline. No
   `git fetch`, `push` or `ls-remote` was run.
8. **The clients** were read only through `git -C <client> rev-parse`, `status --short` and, for
   the two whose `HEAD` moved, `show -s` of the new `HEAD` (§4.7). The brief in SI was read as a
   text file, once, with the editor's file-read tool, at the prompt's "Read first" item 3; nothing
   was acted on from it.

---

## 4. Verification performed

### 4.1 The suite

Each run in the foreground, from its tree's root, its output to a scratch file, the verdict taken
with `grep -E '^Ran |^OK|^FAILED'` and the warnings with `grep -c ResourceWarning`. High-end venvs:
Python 3.13.16, Ray 2.55.1, SQLAlchemy 2.0.46, `setuptools`, the export installed with `uv pip
install --offline --no-deps --no-build-isolation -e`, `datastorekit.__file__` printed under the
export's `tree/` in each. SQLite is 3.53.4 everywhere. `venv/` (3.12.15 / 2.43.0 / 2.0.39,
`datastorekit 0.2.3` editable from this checkout) was not reinstalled.

| When | Where | Result | `ResourceWarning` lines |
|---|---|---|---|
| start (01:02) | `venv/` | `Ran 504 tests in 288.593s` / `OK` | 0 |
| start (01:06) | `<scratch-ot01>/base-hi`: `git archive HEAD` (`2abea79`) | `Ran 504 tests in 160.480s` / `OK` | 0 |
| after §2.1 and §2.2, before the new modules (01:10) | `<scratch-ot01>/stage2-hi`: an export of the working tree | `Ran 504 tests in 376.207s` / `OK` | 0 |
| after §2.3 and §2.4 (01:19) | `venv/` | `Ran 509 tests in 580.926s` / `OK` | 0 |
| after §2.3 and §2.4 (01:29) | `<scratch-ot01>/stage3-hi`: an export of the working tree | `Ran 509 tests in 193.200s` / `OK` | 0 |
| end (01:49) | `venv/` | `Ran 509 tests in 82.957s` / `OK` | 0 |
| end (01:50) | `<scratch-ot01>/final-hi`: an export of the final working tree, this log included | `Ran 509 tests in 86.273s` / `OK` | 0 |

The stage runs at 01:19 and 01:29 preceded §2 item 8's `finally` and item 4's docstring; the end
runs are of the final tree. The run times vary with the machine's load (the load average was 129 at
01:29, with the foreign Ray instance's workers busy); not measured further. The new module and the
three it touches (`test_object_timestamp`, `test_declared_facts`, `test_layer_is_generic`,
`test_store_inventory`) gave `Ran 80 tests … OK` in `venv/` before the full run.

### 4.2 The checks

- **The port check**, `venv/bin/python docs/extraction/compare_ported_tests.py`: exit 0, "OK: 20
  module(s) keep their source's tests, classes and assertion skeletons; 1 test(s) declared not
  ported", at the start, after §2.2 and at the end.
- **`black --check datastorekit docs`** (25.1.0): 74 files at the start (`v0.2.3`'s count,
  `factory-defaults` log 02); **76** at the end, the two new modules the two more. Every changed
  `.py` file was formatted.
- **The guards**, `test_layer_is_generic` and `test_prose_names_no_source`, with
  `test_store_inventory` and `test_object_timestamp`, run on their own at the end: `Ran 61 tests …
  OK`.
- **Scope** (E1): `git status` shows, under `datastorekit/`, `object.py` and
  `tests/test_declared_facts.py` modified and `tests/client/stamped.py` and
  `tests/test_object_timestamp.py` new; `registry.py`, `objects.py`, `factories.py`,
  `instances.py` and `standin_pool.py` are unchanged. Every changed file is in §7's list.
- **The breakages as recorded** (§5): the five diff blocks of §5, extracted from this log, are
  byte-equal to the diffs applied, and each passed `git apply --check`, `git apply` and `git apply
  -R --check` on a fresh export of the final working tree (`<scratch-ot01>/break-<x>`), where each
  was run once more with the results §5 gives.

### 4.3 The smoke runs

Each from its own fresh export of the working tree and fresh offline venv, from the export's root,
as `env -u PYTHONPATH <venv>/bin/python docs/extraction/ray_smoke_run.py` under `/usr/bin/time -p`.
The script is unchanged (SHA-256 `03203679…a92a`, equal in each export). The full output of each is
in `docs/extraction-verification.md` §4.9.

| Run | Started | Ray's session directory | `ray.init` | Steps (1, 2, N, C, 3, 4, 5, 6, I) | In all | Exit | Ray before; after (script; mine) |
|---|---|---|---|---|---|---|---|
| low (3.12.15 / 2.43.0 / 2.0.39) | 01:40:40 | `session_2026-10-12_01-40-42_088960_8945` | 3.7 s | every one PASS: 0.6, 0.0, 1.2, 1.3, 1.2, 1.2, 0.0, 2.0, 2.7 s | 17.2 s (real 17.38) | **0** | 0; 0 and 0 |
| high (3.13.16 / 2.55.1 / 2.0.46) | 01:41:04 | `session_2026-10-12_01-41-06_472413_9379` | 6.7 s | every one PASS: 1.3, 0.2, 2.4, 2.0, 1.9, 1.7, 0.0, 2.5, 4.4 s | 25.9 s (real 26.67) | **0** | 0; 0 and 0 |

At both ends every step gave §4.8's results: step C's refusal was `builtins.ValueError` at 2.43.0
and `ray.exceptions.ActorAlreadyExistsError` at 2.55.1, and step I's serials were `{'scalar_left':
1, 'scalar_right': 1, 'gauge_setting': 1}`. `RAY_ADDRESS` and `RAY_ENABLE_AUTO_CONNECT` were unset,
and there was no `/tmp/ray/ray_current_cluster`, before and after each run. Ray's session
directories under `/tmp/ray/` were not touched, and none was deleted.

### 4.4 The breakages

§5.

### 4.5 The documents and the names

- **Names**, imported in `venv/` from `<scratch-ot01>` with `python -I` (so that the checkout is
  reached only through the editable install; `datastorekit.__file__` is the checkout's):
  `DatastoreObject` (`__init__`'s signature `(self, store_id: Optional[int], *, timestamp:
  Optional[datetime.datetime] = None)`; `timestamp` a `property` with `fset` and `fdel` `None`,
  starting at `:27` by `co_firstlineno`); `stamped.STAMPED_TABLE`, `STAMPED_COLUMN`,
  `stamped_tally`, `stamped_tally_factory` (its class defines `register` and `build`, each a
  `staticmethod`, and no other hook; `register()` gives `version` `False`, `timestamp` `True` and
  the column `tally`), `stamped_registry` (the stamped class under its name; the replicated tables
  end with it); the five `Test…` classes of the new module and their one test each;
  `test_declared_facts.TestTheVersionObject`. All exist; Ray was not initialised.
- **Anchors**, by GitHub's rule (lower-case; drop what is not a word character, a hyphen or a space;
  spaces to hyphens; headings inside fences skipped), each unique in its file:
  `#96-object-timestamp-prompt-01` (the contract);
  `#49-the-smoke-run-after-object-timestamp-prompt-01-2026-10-12`, `#491-the-output-low-end` and
  `#492-the-output-high-end` (the verification document). No link to an anchor was added.
- **Relative links** added, each resolved from its file: `../prompts/object-timestamp/README.md`
  (the contract); `../prompts/object-timestamp/01-the-object-carries-a-timestamp.md` and
  `../prompts/object-timestamp/logs/01-the-object-carries-a-timestamp.md` (the verification
  document); `logs/01-the-object-carries-a-timestamp.md` (this campaign's board and README);
  `../01-the-object-carries-a-timestamp.md` (this log).
- **`path:line`s** of §9.6 and of §1 above were read at this tree: `object.py:1`, `:10-14`, `:14`,
  `:16-21`, `:23-25`, `:16-25`, `:27-38`; `SQL/Datastore.py:760-843`, `:809-815`;
  `SQL/ShardedPool.py:3203`.
- **Neutral names** (`<scratch-ot01>/probe/vocab_check.py`, which loads
  `datastorekit/tests/data/client_vocabulary.json` and walks every string under each client's
  `registry`, `columns`, `packages` and `extra_names`: 486 strings, 485 case-folded), each name
  checked exactly and case-folded, and each of its `_`-separated parts:
  - the names §2.3 and §2.4 choose (`stamped`, `tally`, `stamped_tally`, `stamped_tally_factory`,
    `stamped_registry`, `STAMPED_TABLE`, `STAMPED_COLUMN`, `STAMP`, `TALLY`, `timestamp`,
    `_timestamp`, `test_object_timestamp`, the five test classes, `stamps_on_every_shard`), with
    `value` as a control: **19 names, 1 hit, the control** (`value`, a column of SGK, CPBH and SI);
  - every identifier and identifier-like string in `object.py`, `stamped.py` and the test module,
    by `ast` (`<scratch-ot01>/probe/new_names.py`; 75 names): **2 hits**, `factories` (the name of
    SGK's registry variable, held as `registry.name`; here `ShardedPool`'s keyword argument and the
    test's attribute, as in every pool test) and `version` (a registry key of all three clients:
    the layer's own `version` table, in the guard's `LAYER_WORDS`; here `register()`'s key
    `"version"`). Both are the layer's own names, used as every neutral factory and pool test uses
    them. No new name is a client's.

### 4.6 Ray's processes

By the script's rule (`<scratch-ot01>/probe/raycheck.py`): **24** at 01:29:36 (the foreign
instance, §3 hazard 6); 0 at 01:40:20, 01:40:40, 01:40:57, 01:41:04, 01:41:31 and
01:52:23 (the end). `pgrep -fl 'gcs_server|raylet|ray::|default_worker\.py'` found none at
01:01 (the start).

### 4.7 The clients

Read only with `git -C <client> rev-parse --short HEAD`, `rev-parse --abbrev-ref HEAD` and
`status --short` (each listing saved and compared with `diff`), and, at the end, `show -s
--format='%h %ad %p %s'` of the two `HEAD`s that had moved.

| Client | Start (01:01) | End (01:52) |
|---|---|---|
| SecondaryGWKit | `718e650`, `handover-remedial`; 93 entries (a large staged change by another session, as the dispatch says) | **`d03a643`**, `handover-remedial`; 0 entries. Another session committed there during this prompt: `d03a643` (01:33:04, "Delete the schema snapshots orphaned by the datastorekit adoption", parent `7d76d3e`), its staged change no longer in the index. This prompt read it only through `git` (`rev-parse`, `status --short`, and `show -s` of its `HEAD`) |
| ChamPBH | `a72ca5e`, `dk-and-rpk-migration`; 23 entries (untracked pilot `.db` files, logs, `pilot-out/`, `prompts/jordan-normalization/`). The dispatch gave `f5fe207`: another session committed there before this prompt started | **`70184f1`**, `dk-and-rpk-migration`; the same 23 entries (`diff` of the two listings empty). Another session committed there during this prompt: `70184f1` (01:46:11, "Record the orchestrator's review of dk-and-rpk-migration prompt 02", parent `6cbf953`); read as SGK was |
| StochasticInstantons | `7bb3efd`, `main`; 3 entries (2 modified, `.documents/OPEN-ISSUES.md` and `.prompts/INDEX.md`; 1 untracked, `.prompts/dk-and-rpk-migration/`) | `7bb3efd`, `main`; the same 3 entries (`diff` empty) |

---

## 5. The deliberate-breakage record (§4.4)

Each diff is relative to the repository root, exactly as applied, to its own fresh export of the
working tree (`<scratch-ot01>/break-<x>/tree`) with its own fresh offline venv at the high end,
installed editable. Each passed `git apply --check`, was applied with `git apply`, and then passed
`git apply -R --check`. (a) ran the whole suite; (b)–(e) ran the new module and
`test_declared_facts` (30 tests). "Entries" are `unittest`'s failures plus errors, a sub-test
counting on its own. Each was run again on the final tree, from the diffs extracted from this log
(§4.2), with the results below. None was committed. 0 `ResourceWarning` lines under every one but
(a)'s first run (§2 item 8).

### (a) `object.py` as `v0.2.3`'s (`git show 0de2b16:datastorekit/object.py`)

```diff
diff --git a/datastorekit/object.py b/datastorekit/object.py
index 50c3111..a51e674 100644
--- a/datastorekit/object.py
+++ b/datastorekit/object.py
@@ -1,4 +1,3 @@
-from datetime import datetime
 from typing import Optional
 
 
@@ -7,11 +6,8 @@ class DatastoreObject:
     Represent an object that can be serialized in a datastore
     """
 
-    def __init__(
-        self, store_id: Optional[int], *, timestamp: Optional[datetime] = None
-    ):
+    def __init__(self, store_id: Optional[int]):
         self._my_id = store_id
-        self._timestamp = timestamp
 
     @property
     def store_id(self) -> int:
@@ -23,16 +19,3 @@ class DatastoreObject:
     @property
     def available(self) -> bool:
         return self._my_id is not None
-
-    @property
-    def timestamp(self) -> Optional[datetime]:
-        """
-        The row's ``timestamp``, as the factory that built this object passed it, or ``None``.
-
-        The layer stamps a row's ``timestamp`` column at insert, for a class whose ``register()``
-        declares ``"timestamp": True``. A factory that reads such a row may pass the value to the
-        object it builds, by the keyword ``timestamp``. It is ``None`` for an object not yet
-        stored, for one built from an insert, for one whose factory does not pass it, and for one
-        whose table has no such column. The layer neither sets nor reads it. It is read-only.
-        """
-        return self._timestamp
```

`Ran 509 tests … FAILED (failures=2, errors=4)`. **Errors** (4): test 1, `AttributeError:
'DatastoreObject' object has no attribute 'timestamp'`, at its first read of `timestamp` (§2 item
4); tests 2, 3 and 5, each `TypeError: DatastoreObject.__init__() got an unexpected keyword
argument 'timestamp'`: test 3 at `DatastoreObject(3, timestamp=STAMP)`, test 5 at
`stamped_tally(4, 17, timestamp=STAMP)` (raised in `stamped_tally.__init__`'s `super().__init__`),
and test 2 at its first get, raised inside the controlling shard's actor, in the stamped factory's
insert branch (`stamped_tally(inserter(conn, data), tally)` passes `timestamp=None` on), and
re-raised by the stand-in's `ray.get` in `_replicated_write`, before any read. **Failures** (2):
`TestTheVersionObject`'s two sub-tests, `{'_my_id': 1, '_timestamp': None, 'label': 'standin',
'_deserialized': True} != {'_my_id': 1, 'label': 'standin', '_deserialized': True}`. **Test 4
passes** (correction 1). **Nothing else in the 509 fails.** The first run (01:34) gave the same
entries with 4 `ResourceWarning` lines; the rerun after §2 item 8 (01:37) and the final run, 0.

### (b) a setter on the property

```diff
diff --git a/datastorekit/object.py b/datastorekit/object.py
index 50c3111..1f18ef1 100644
--- a/datastorekit/object.py
+++ b/datastorekit/object.py
@@ -36,3 +36,7 @@ class DatastoreObject:
         whose table has no such column. The layer neither sets nor reads it. It is read-only.
         """
         return self._timestamp
+
+    @timestamp.setter
+    def timestamp(self, new: Optional[datetime]):
+        self._timestamp = new
```

`FAILED (failures=2)`: test 3, in both sub-tests (`DatastoreObject`, `stamped_tally`),
`AssertionError: AttributeError not raised`, at the assignment. Nothing in `test_declared_facts`
fails.

### (c) the `*` removed: `timestamp` positional-or-keyword

```diff
diff --git a/datastorekit/object.py b/datastorekit/object.py
index 50c3111..da851f1 100644
--- a/datastorekit/object.py
+++ b/datastorekit/object.py
@@ -8,7 +8,7 @@ class DatastoreObject:
     """
 
     def __init__(
-        self, store_id: Optional[int], *, timestamp: Optional[datetime] = None
+        self, store_id: Optional[int], timestamp: Optional[datetime] = None
     ):
         self._my_id = store_id
         self._timestamp = timestamp
```

`FAILED (failures=1)`: test 4, `AssertionError: TypeError not raised`. Nothing in
`test_declared_facts` fails.

### (d) the property returning `None` always

```diff
diff --git a/datastorekit/object.py b/datastorekit/object.py
index 50c3111..d498bff 100644
--- a/datastorekit/object.py
+++ b/datastorekit/object.py
@@ -35,4 +35,4 @@ class DatastoreObject:
         stored, for one built from an insert, for one whose factory does not pass it, and for one
         whose table has no such column. The layer neither sets nor reads it. It is read-only.
         """
-        return self._timestamp
+        return None
```

`FAILED (failures=5)`: test 1, `None is not datetime.datetime(2026, 10, 12, 9, 30, 15, 123456)`
(the stamped half); test 2, `None is not an instance of <class 'datetime.datetime'>`, at the
read-write reopen's get (the insert's `None` passes, as it should); test 3, in both sub-tests,
`None is not datetime.datetime(…)`, at the check after the refused assignment and deletion
(correction 3); test 5, the stamped sub-test, `None != datetime.datetime(…)`. Test 4 passes. Nothing
in `test_declared_facts` fails.

### (e) the stamped factory passing `datetime.now()` instead of the row's timestamp

```diff
diff --git a/datastorekit/tests/client/stamped.py b/datastorekit/tests/client/stamped.py
index 25e2540..03f50e7 100644
--- a/datastorekit/tests/client/stamped.py
+++ b/datastorekit/tests/client/stamped.py
@@ -77,7 +77,7 @@ class stamped_tally_factory(SQLAFactoryBase):
             )
         ).one_or_none()
         if row is not None:
-            obj = stamped_tally(row.serial, tally, timestamp=row.timestamp)
+            obj = stamped_tally(row.serial, tally, timestamp=datetime.now())
             obj._deserialized = True
             return obj
 
```

`FAILED (failures=1)`: test 2, at the read-write reopen's get, `AssertionError:
datetime.datetime(…) != datetime.datetime(…)`, the factory's `now()` against the row's stamp a
fraction of a second earlier (0.123 s, 0.059 s and 0.055 s apart in three runs). A mutation of
test support, not of the layer: test 2 compares with the row, not with any `datetime`.

---

## 6. Observations not acted on

1. **`value` is avoided, not forbidden.** The guard does not scan `tests/`, and does not forbid
   plain-word columns by design (`registry_words`' docstring); `instances.scalar_entry` keeps its
   `value` attribute. This prompt chose `tally` throughout (§2 item 2). Not opened as an issue.
2. **A get that inserts answers `timestamp` `None`** although the actor knows the stamp it wrote
   (`SQL/Datastore.py:809-815`). README §1 puts the layer filling it out of scope; contract §9.6
   states it. By design; no issue.
3. **The suite does not send a stamped object through real Ray.** The stand-in pool pickles every
   result (test 2's objects came through it) and test 5 round-trips `ray.cloudpickle`; the smoke
   script sends only unstamped objects, each now carrying `_timestamp` (U4). By design; no issue.
4. **The local `origin/main` ref** is `2a86f92`, not the dispatch's `83068cb` (§2 item 12). Not
   checked against the remote, since the prompt runs offline; for the orchestrator's `git
   ls-remote` at the review.
5. **The foreign Ray instance** (§3 hazard 6) was another repository's, by its executables' paths;
   it was not inspected further. Two session directories under `/tmp/ray/` from before this
   prompt's start (00:55 and 00:58) and one from the foreign instance (01:12) are not this
   prompt's.
6. **The scratch tools** are in `<scratch-ot01>/probe/`, not in the repository: `mkenv.sh` (an
   export and its venv), `suite.sh`, `breakrun.sh`, `raycheck.py`, `ast_compare.py`,
   `vocab_check.py`, `new_names.py`, `names.py`, `anchors.py` and `sec49.md` (the verification
   subsection as inserted). Each run's output is in `<scratch-ot01>/logs/`, and each diff in
   `<scratch-ot01>/diffs/`.

---

## 7. Issues

- **Opened, narrowed or closed**: none.
- **`docs/OPEN_ISSUES.md`**: unchanged, **4 open**, all on `inherited-issues`' board.

---

## 8. State handed to the next prompt

- **`HEAD`** is `1b2f91a`, unpushed and untagged. The local `origin/main` ref is `2a86f92`; the
  tags are `v0.1.0`, `v0.2.0`, `v0.2.1`, `v0.2.2` and `v0.2.3`, unchanged. `pyproject.toml` is at
  `0.2.3`.
- **The suite** is 509, in `venv/` and at the high end. The port check passes over 20 modules with
  1 test declared not ported. `black` leaves 76 files unchanged.
- **The interfaces** (README §4): `DatastoreObject(store_id, *, timestamp=None)` and its read-only
  `timestamp` property; `datastorekit/tests/client/stamped.py` (`STAMPED_TABLE`, `STAMPED_COLUMN`,
  `stamped_tally`, `stamped_tally_factory`, `stamped_registry()`);
  `tests/test_object_timestamp.py`; contract §9.6 and its head line; verification §4.9.
- **For 02** (`v0.3.0`, U6): what changes for a client is that `DatastoreObject` takes a
  keyword-only `timestamp` and exposes it read-only; a subclass that assigns `self.timestamp` now
  raises `AttributeError` (none of the three clients does, README §0.1); every object has
  `_timestamp` in `vars()`. SI's 24 sites, each passing `timestamp=` by keyword, work unchanged
  once their import is rewritten (README §0.1).
- **Open**: none on this repository's own campaign boards; the four inherited issues of
  `docs/OPEN_ISSUES.md` §1.2.
