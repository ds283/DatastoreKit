# Prompt 01 — the object carries a timestamp

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

*Written 2026-10-12 against `83068cb`, whose `datastorekit/` is `0de2b16`'s (`v0.2.3`).*

**Gate:**
- U1–U4 are taken (README §6.2): as recommended, by the user on 2026-10-12.
- `git status` is clean in this repository, and `origin/main` is an ancestor of `main`.
- `datastorekit/` is `0de2b16`'s: `git diff --stat 0de2b16 HEAD -- datastorekit` is empty.
- The suite gives `Ran 504 tests … OK` in `venv/`.

**Closes:** nothing on a board. **Opens:** only what the work finds.

**Recommended model:** **Sonnet** is enough for the code; **Opus** if the same agent writes the
contract and verification subsections, as it should.
- The code change is a dozen lines in one file. The risk is not in it but in what must not change:
  no message, nothing the layer writes or reads, and nothing a caller that passes `store_id` alone
  meets but the one new key in `vars()`.
- The tests must fail on `v0.2.3`'s object for the right reason, and must not pass for a wrong one,
  such as a property with a setter, or a positional argument.
- It starts Ray, for the smoke run only, under README §5 rule 7.
- The contract's §9.6 adds a row without rewriting §6's.

**Read first:**

1. [`README.md`](README.md): all of it, §0.1 and §6.2 especially.
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`.
3. The brief:
   `/Users/ds283/Documents/Code/StochasticInstantons/.prompts/dk-and-rpk-migration/datastorekit-v0.2.4-brief.md`.
   It is evidence, read as text. Do not act on it beyond this prompt; README §0.1 re-measured it,
   and README §0.2 records where this campaign departs from it.
4. `docs/client-contract.md`: its head (`:1-39`), §2's `timestamp` row (`:101`), §6 (`:201-214`)
   and §9 (`:281-` end), for the form a §9 subsection takes.
5. Item 2 of `docs/adoption/stochasticinstantons.md` (`:78-105`), and item 4's line (`:154`). 01
   changes neither; 02 adds the addendum.
6. The code: `datastorekit/object.py` (all of it); `datastorekit/SQL/Datastore.py:764-830` (the
   inserter, which stamps the row); `datastorekit/tests/client/objects.py` (its head and
   `version_entry`); `datastorekit/tests/client/instances.py` (all of it: the model for §2.3's
   module); `datastorekit/tests/test_factory_instances.py` (its head, `_StoreCase` at `:93-180`,
   and test 5 at `:296-318`); `datastorekit/tests/standin_pool.py` (`open_pool`, `:352-376`;
   `close_pool`, `:413-418`; `table_columns` and `shard_rows`, `:443-460`);
   `datastorekit/tests/test_declared_facts.py` (its docstring and `TestTheVersionObject`,
   `:592-646`); `datastorekit/tests/test_store_inventory.py:476-500`;
   `datastorekit/tests/test_layer_is_generic.py` (its docstring and `:91`); and
   `docs/extraction/ray_smoke_run.py` (its docstring and how it is run).
7. `factory-defaults` prompt 01 and its log (`../factory-defaults/01-the-base-defaults-three-hooks.md`,
   `../factory-defaults/logs/01-the-base-defaults-three-hooks.md`): how a neutral module outside the
   registry, a contract §9 subsection and a verification subsection were added last time.

Line numbers are at `83068cb`, measured on 2026-10-12.

---

## 1. What is wanted

After this prompt, **`datastorekit.DatastoreObject` carries an optional timestamp**:
- `DatastoreObject(store_id)` behaves as under `v0.2.3`, and its `timestamp` is `None`;
- `DatastoreObject(store_id, timestamp=t)` keeps `t`, and `obj.timestamp` returns it;
- `timestamp` is keyword-only, and read-only;
- the layer never sets it and never reads it. A factory that reads a row of a class registered
  with `"timestamp": True` may pass the row's `timestamp`; nothing else fills it.

The suite sees it, and a revert fails it. The smoke script, unchanged, runs every step under real
Ray at both ends.

**Nothing the layer writes or reads changes. No message, refusal or exception changes.** The only
thing a caller that passes `store_id` alone can observe is one more key, `_timestamp`, in its
object's `vars()`. `pyproject.toml` stays at `0.2.3`: 02 releases.

### 1.1 What the planner measured

README §0.1 holds the measurements. The ones this prompt rests on:
- the layer reads `_my_id`, `_new_insert`, `_updated` and the shard key's field of an object, and
  compares replicas by `_my_id` alone; it has no `vars`, `__dict__` or `__eq__` of an object;
- the suite has one test that pins an object's `vars()`: `TestTheVersionObject`
  (`tests/test_declared_facts.py:643-646`), which fails in its two subtests under the change, and
  passes with `"_timestamp": None` added to its expected dict (U2);
- a prototype gave 506 tests with only those two failures, at both ends; with the dict corrected,
  the affected modules pass at both ends;
- a get that inserts cannot know the row's timestamp (the inserter adds it inside the actor,
  `SQL/Datastore.py:809-815`), so a factory's object from an insert has `timestamp` `None`; a get
  that finds the row can pass it.

---

## 2. What to change

### 2.1 `datastorekit/object.py` (U1)

- `__init__(self, store_id: Optional[int], *, timestamp: Optional[datetime] = None)`, setting
  `self._my_id = store_id` as now and `self._timestamp = timestamp`. Import `datetime` from
  `datetime`.
- A property, `timestamp`, returning `self._timestamp`, typed `Optional[datetime]`, with **no
  setter and no deleter**.
- `store_id` and `available` unchanged: their bodies, their message, and their order before the new
  property.
- A docstring that says, in neutral terms: the value is the row's `timestamp`, which the layer
  stamps at insert for a class whose `register()` declares `"timestamp": True`; a factory that reads
  such a row may pass it; it is `None` for an object not yet stored, for one built from an insert,
  for one whose factory does not pass it, and for one whose table has no such column; the layer
  neither sets nor reads it. Extend the class docstring or give the property its own; keep the
  file's style (it has one three-line docstring now).
- **This file is in the layer.** The guard (`test_layer_is_generic`, which scans `object.py` at
  `:91`) checks its names, strings, docstrings and comments for every client's vocabulary. Name no
  client, and no client's class, table or figure.

### 2.2 `datastorekit/tests/test_declared_facts.py` (U2)

In `TestTheVersionObject` (`:643-646`), the expected dict becomes `{"_my_id": 1, "_timestamp": None,
"label": "standin", "_deserialized": True}`. Nothing else in the module changes: not its docstring,
not the test's name.

This module is ported (`docs/extraction/compare_ported_tests.py`, `PORTED`). The port check
compares assertion skeletons, not arguments, so it must still report "20 module(s) … 1 test(s)
declared not ported" (§4.2). If it does not, stop.

### 2.3 The stamped class and its factory, and where they live (U3)

A neutral **replicated** stored class with one integer value, subclassing `DatastoreObject`, whose
constructor takes `store_id`, the value and `timestamp=None`, and passes `timestamp` to
`super().__init__` by keyword. A factory class for it with **static** `register` and `build` only
(it is registered as a class, as SGK registers its factories):
- `register()` declares `"version": False`, `"timestamp": True`, and the value's column;
- `build` selects the row's `serial` and `timestamp` by the value. If it finds the row, it returns
  the object with `timestamp=row.timestamp`, marked `_deserialized`. If not, it inserts (carrying a
  payload's `serial`, as `gauge_setting_factory.build` and `instances.scalar_entry_factory.build`
  do), and returns the object with **no** timestamp, marked `_new_insert`.

**Recommended home:** a new module `datastorekit/tests/client/stamped.py`, holding the two classes
at module level and a function returning `(factories, replicated_tables)`: a copy of the registry's
factories with the class added under a new name, and a copy of the replicated tables with that name
at the end, as `instances.instance_registry()` does. The names are yours. They must be neutral:
check each against `datastorekit/tests/data/client_vocabulary.json`, and say in the log how. **It is
outside `registry.py`**: the neutral client's registry, objects and factories are unchanged.

Hazards of the home:
- `tests/test_store_inventory.py:476-500` counts `inventory_spec` definitions in every module under
  `tests/client/` and pins **12**. The new factory defines none. If you define one, that test
  fails: do not.
- Build pools with your own `replicated_tables`, as `test_factory_instances._StoreCase.open` does
  (`:109-131`). Reuse that helper by import, or restate it; do not change `standin_pool.py`.

### 2.4 A new test module, `datastorekit/tests/test_object_timestamp.py` (U3)

On the stand-in pool, with no Ray, every store in a `tempfile` directory, and a `tearDownModule`
asserting Ray is not initialised, as the other modules do. Tests:

1. **The argument and the property.** `DatastoreObject(3)` has `timestamp` `None`, `store_id` 3 and
   `available` true; `DatastoreObject(None)` has `timestamp` `None`, `available` false, and
   `store_id` raises the `RuntimeError` it raised before. `DatastoreObject(3, timestamp=t)` for a
   `datetime` `t` with microseconds returns `t` itself (`assertIs`).
2. **Through the pool, on the stamped class** (§2.3), on a fresh store:
   - a get that inserts answers `_new_insert`, and `timestamp` `None`: the layer does not fill it;
   - the pool closed, the row's `timestamp` column holds one value, the same on every shard (read
     with `table_columns` and `shard_rows`, or `test_factory_instances._StoreCase.values_on_every_shard`);
   - a reopen, read-write, and a get of the same value answers `_deserialized`, the same serial, and
     a `datetime` `timestamp` equal to that value (SQLite returns the column as text to a raw read;
     compare by parsing it, or by `str`, and say which in the log);
   - with the reopened pool, a get of the same value sent to **each shard's actor directly**
     (`ray.get(pool._shards[k].object_get.remote(<name>, value=…))`, under the stand-in's
     `ray.get`) answers the same `timestamp` on every shard;
   - a reopen read-only answers the same `timestamp`.
3. **Read-only.** On a stamped object, `obj.timestamp = …` raises `AttributeError`, and so does
   `del obj.timestamp`; `obj.timestamp` is unchanged afterwards.
4. **Keyword-only.** `DatastoreObject(3, t)` raises `TypeError`.
5. **Serialisation.** A stamped object and an unstamped one each round-trip
   `ray.cloudpickle.dumps` / `loads`: the copy is an instance of its class with the same
   `store_id`, value and `timestamp` (`None` for the unstamped one), and Ray is not initialised
   afterwards.

Every test must fail on `v0.2.3`'s `object.py` (breakage (a)), and the log must say how each fails.
On the unchanged object, test 1's stamped half, 2, 3 and 5 should error with `TypeError` where
they pass `timestamp=`; test 4 should fail because the call succeeds.

### 2.5 The smoke run (U4)

**No change to `docs/extraction/ray_smoke_run.py`.** Run it under real Ray, per README §5 rule 7,
**at both ends** (a scratch venv each, with an export of your tree installed editable, as
`factory-defaults` log 01 records): every step `PASS`, exit 0, no Ray process of yours before or
after. Record the script's SHA-256, unchanged since `factory-defaults` prompt 01 (verification
§4.8). Another session's Ray may be running on this machine; record it and do not touch it, as
§4.8 did.

### 2.6 `docs/client-contract.md`

- **At the head**, after `:37-38` (§9.5's line): *"§9.6 is measured from the package at
  `object-timestamp` prompt 01's tree, and its line numbers are that tree's."*
- **A §9.6, "`object-timestamp` prompt 01"**, after §9.5, in §9's form. Its preamble: one change
  (`prompts/object-timestamp/README.md`, decision U1, the user's ruling); nothing the layer writes
  or reads changes, and no message, refusal or exception. Its one row:
  - **Change:** `DatastoreObject.timestamp`. **Supersedes:** none: §6 lists what the layer reads
    from a stored object, and its `DatastoreObject` row still holds, since the layer reads nothing
    new. §2's `timestamp` row, which says the layer stamps the column, still holds. **What holds**
    (`object.py`, at 01's tree): the constructor's keyword-only `timestamp`, `None` by default; the
    read-only property; who fills it (a factory, from the row it read; never the layer); when it is
    `None`; that a get which inserts cannot know the stamp, since the actor adds it inside the
    inserter (`SQL/Datastore.py`, at 01's tree); that a replicated row's stamp is the same on every
    shard (§2), so an object read from any shard carries the same value; and that a subclass must
    not assign `self.timestamp`, which now raises `AttributeError`. **Pinned by:**
    `tests/test_object_timestamp.py` (tests 1–5); `tests/test_declared_facts.py`,
    `TestTheVersionObject`, for `vars()` of an unstamped object.
- **No marker** is set on any row of §1–§9.5, since §9.6 supersedes none. **Nothing in §1–§9.5
  changes**: the diff of the file is `+` lines only.

### 2.7 `docs/extraction-verification.md`

Add a subsection of §4, after §4.8 (before §5, `:1019-1022`): **"4.9 The smoke run after
`object-timestamp` prompt 01 (<date>)"**, in §4.8's form: an italic preamble naming the prompt and
its log and saying §4.1–§4.8 stay true of their trees; that the script is unchanged (its SHA-256);
the environment of each run; the output of each; and the Ray processes before and after. Change no
line of the document.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **The guard.** `object.py` is in the layer (§2.1). The guard runs in the suite.
2. **A property with a setter, or a positional argument.** Either would pass a careless test.
   Breakages (b) and (c) are there to show the tests do not.
3. **The inventory's count of 12** (§2.3).
4. **The port check** (§2.2).
5. **Additive documents** (§2.6, §2.7). `git diff` of `docs/client-contract.md` and
   `docs/extraction-verification.md` shows `+` lines only.
6. **No Ray in the suite.** Test 5 imports `ray.cloudpickle`, which starts nothing; the module's
   `tearDownModule` proves it. Test 2's direct actor calls go through the stand-in.
7. **Offline only.** Every venv is made `--offline`. A pin that does not resolve offline is a stop.
8. **The clients.** None is written, run, imported or opened. Record each one's `HEAD` and
   `git status --short` at the start and the end.

---

## 4. Verification

1. **The suite.** `Ran 504 tests … OK` in `venv/` before; after, 504 plus the new tests, `OK`, at
   both ends: `venv/`, and a fresh offline scratch venv (Python 3.13.16, `ray==2.55.1`,
   `sqlalchemy==2.0.46`, `setuptools`) with a `git archive` of your tree installed editable
   (`--no-deps --no-build-isolation`). Record the `ResourceWarning` lines at each end (0 in
   `venv/`; 0 or 4 at the high end is timing, `actor-names` log 01 correction 8).
2. **The checks.** `docs/extraction/compare_ported_tests.py` exits 0 with "20 module(s) … 1 test(s)
   declared not ported"; `black --check datastorekit docs` passes, its file count above `v0.2.3`'s
   by your new files, said in the log (read `v0.2.3`'s count from `factory-defaults` log 02).
3. **The smoke runs** (§2.5), at both ends.
4. **The breakage record.** Each a diff exactly as applied in a scratch export, checked with
   `git apply --check` and `-R --check`, with what failed. None is committed.
   - **(a)** `object.py` reverted to `v0.2.3`'s (`git show 0de2b16:datastorekit/object.py`):
     every test of §2.4 fails or errors, as §2.4's last paragraph says, and `TestTheVersionObject`
     fails (its dict now names `_timestamp`); nothing else in the suite fails.
   - **(b)** a setter added to the property: test 3 fails.
   - **(c)** the `*` removed, so `timestamp` is positional-or-keyword: test 4 fails.
   - **(d)** the property returning `None` always: tests 1, 2 and 5 fail.
   - **(e)** the stamped factory's `build` passing `timestamp=datetime.now()` instead of the row's:
     test 2 fails. (A mutation of test support, not of the layer: it shows test 2 compares with the
     row, not with any `datetime`.)
5. **The documents.** Every anchor and name §2.6–§2.7 add exists: names by importing them in
   `venv/`, anchors by GitHub's rule. List each in the log.
6. **The clients**, at the start and the end, unchanged (hazard 8).

---

## 5. Acceptance

1. `object.py` is as §2.1 says. Compare its `ast` with `v0.2.3`'s: `store_id` and `available` are
   unchanged, `__init__` differs by the keyword-only parameter and the one assignment, and the only
   other additions are the import, the property and docstrings. Say how in the log.
2. §2.2–§2.7 are done, and the neutral client's `registry.py`, `objects.py`, `factories.py` and
   `instances.py` are unchanged.
3. §4.1–§4.6 hold.
4. **The records**, in the same commit:
   - the log `logs/01-the-object-carries-a-timestamp.md`, per README §5.1, with the smoke output,
     the breakage diffs, each name checked, and the clients at the start and the end;
   - this board: §1's row for 01, the header, and the decisions table if any changed;
   - this campaign's README: its header and §2's row for 01;
   - `docs/OPEN_ISSUES.md`: unchanged at **4**, unless the work opens an issue;
   - `prompts/INDEX.md`: the campaign's line.

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count falls, in any venv.
- Any test outside §2.2's other than the new module fails after the change.
- A test of §2.4 passes on `v0.2.3`'s object where §4.4 (a) says it must not, or fails after the
  change for a reason other than a bug in the test.
- Any change of message, refusal or exception would be needed, or any file under `datastorekit/`
  but `object.py`, `tests/test_declared_facts.py`, the new test module and §2.3's module.
- The port check fails after §2.2.
- The guard fails on `object.py` and cannot be satisfied by rewording.
- A smoke run fails at either end.
- A document cannot say what it must without rewriting a line already in it.
- Anything would push, make or move a tag, download, or write, run, import or open anything of a
  client.

---

## 7. What this prompt changes, and what it does not

- **Files it changes:**
  - `datastorekit/object.py`;
  - `datastorekit/tests/test_declared_facts.py` (one dict); the new
    `datastorekit/tests/test_object_timestamp.py`; §2.3's module;
  - `docs/client-contract.md` and `docs/extraction-verification.md`, by addition only;
  - the log, this board, this campaign's README, `docs/OPEN_ISSUES.md` if an issue is opened, and
    `prompts/INDEX.md`.
- **It changes nothing else:** not `docs/extraction/ray_smoke_run.py`, `pyproject.toml`,
  `README.md`, `PROVENANCE.md`, `docs/adoption/`, the workflow, `CLAUDE.md`, `LICENSE` or
  `.gitignore`. 02 changes the release's files.
- **It touches no client repository.**
- **It makes no tag and pushes nothing.**

---

## 8. After 01

The orchestrator reviews 01 against its commit. 02, the release, is then written against the tree
01 leaves, and carries the adoption addenda (README §6.2, U6).
