# Log 01 — the base defaults three hooks

**Subject:** Default store, validate and validate_on_startup in the factory base · **Commit:**
`f5d8957` · **Date:** 2026-10-11 · **Model:** Claude Opus 5.5 · **Result:** landed; unpushed and
untagged; reviewed 2026-10-11 (the board's §1).

`SQLAFactoryBase` keeps `register` and `build` as its only abstract hooks, and defaults `store`,
`validate` and `validate_on_startup` as it defaults `revalidate`, `owned_serials` and
`inventory_spec`: static, with their `v0.2.2` parameters and their bare `raise
NotImplementedError` (U1). A factory class that defines `register` and `build` can now be
instantiated and its instance registered; one that lacks either is still refused with `TypeError`.
No hook's signature or body, no message, refusal or exception of the layer's, and nothing the layer
writes changed. `pyproject.toml` stays at `0.2.2`.

A new module of **9** tests, `datastorekit/tests/test_factory_instances.py`, and one new test in
`test_neutral_client.py` (whose `ABSTRACT_HOOKS` is now `("register", "build")`) pin it (U2). A
parameterised factory lives in a new module, `datastorekit/tests/client/instances.py`, outside the
neutral client's registry, which is unchanged. The suite goes from **494 to 504**, in `venv/` and
at the high end. Breakage (a), the three decorators restored, fails exactly the 8 entries
correction 3 predicts and nothing else in the 504; each of (b)–(e) fails its tests.

Under real Ray, `docs/extraction/ray_smoke_run.py` has a new step **I**, a registry of instances.
It passes at both ends (exit 0, no Ray process before or after); with (a) applied it fails, naming
`TypeError`, while every other step passes (exit 1). `docs/client-contract.md` gains a head line,
§9.5 and five markers; `docs/extraction-verification.md` gains §4.8 and §8.1; extraction U32 gets
a dated note in its README and its board row. No issue was opened or closed: the index stays at
**4 open**.

No client was written, run, imported or opened; nothing was pushed, tagged or downloaded. Ray was
started only by the smoke script, three times, and the foreign Ray instance of the dispatch note
had gone before this prompt started.

Prompt: [`../01-the-base-defaults-three-hooks.md`](../01-the-base-defaults-three-hooks.md), with
the orchestrator's dispatch note §0: seven corrections, its additions, its checked facts and its
conventions. §2 classifies each.

`<scratch-fd01>` below is `<session scratchpad>/agent01`, outside the repository.

---

## 1. What shipped

### 1.1 The base (§2.1)

`datastorekit/SQL/factory_base.py`, 24 lines added and 6 removed (`git diff --numstat`). Line
numbers are `f5d8957`'s:

- `register` (`:6-9`) and `build` (`:11-14`) keep `@staticmethod @abstractmethod`, unchanged. The
  import of `abstractmethod` stays, and the class is still `SQLAFactoryBase(ABC)`. Its
  `__abstractmethods__` is `frozenset({"register", "build"})`.
- `store` (`:21-30`), `validate` (`:32-40`) and `validate_on_startup` (`:42-50`) lose
  `@abstractmethod` and keep `@staticmethod`, their parameter lists and their bodies, a bare
  `raise NotImplementedError`. Each gains a docstring in `revalidate`'s manner: what it does, when
  the layer calls it (a store of the class; a validate; at open and in a replicated prune, only for
  a class whose `register()` declares `validate_on_startup: True`), and, for the first two, what a
  replicated call does.
- The comment on defaulted hooks (`:16-19`) now stands above the six. Its two sentences are as
  they were; a third says the layer calls each hook on the registry's entry, class or instance alike,
  only in the case its docstring names, and that one not defined raises `NotImplementedError` or
  returns its default. The order of the hooks is unchanged: the comment moved up past the three,
  which puts them below it (§2 item 9).
- The guard (`test_layer_is_generic`) passes on it: no client, client table or class is named.

**Acceptance 1, by `ast`** (`<scratch-fd01>/probe/ast_compare.py`): the file at `6d8ee9a` (`git
show`) and in the tree, each parsed, the class's `FunctionDef`s matched by name. For every one of
the eight hooks, `ast.dump` of its `args`, of its body less a leading docstring, and of its return
annotation are equal at the two trees. The whole `FunctionDef` (decorators and docstrings included)
is equal for `register`, `build`, `revalidate`, `owned_serials` and `inventory_spec`; for the
three it differs only by the decorator list, `['staticmethod', 'abstractmethod']` →
`['staticmethod']`, and the docstring. The class's bases are `['ABC']` at both, and its hooks are
the same eight in the same order.

### 1.2 `test_neutral_client.py` (§2.2)

23 lines added and 2 removed. `ABSTRACT_HOOKS = ("register", "build")`; `DEFAULTED_HOOKS` is
`store`, `validate`, `validate_on_startup`, `revalidate`, `owned_serials`, `inventory_spec`, the
base's order. The test that sums the three lists sees the same ten hooks. One new test,
`TestCoverageByDeclaration.test_the_hook_lists_are_the_bases` (`:287`), asserts
`set(ABSTRACT_HOOKS) == SQLAFactoryBase.__abstractmethods__`, and, for each of `DEFAULTED_HOOKS`
in a sub-test, that the base has it and that it is not abstract (`__isabstractmethod__` false).
Nothing else in the module changed.

### 1.3 The parameterised factory (§2.3)

**`datastorekit/tests/client/instances.py`**, new (98 lines), outside `registry.py`:

- `scalar_entry(store_id, value)`: a `DatastoreObject` with one integer value;
- `scalar_entry_factory(column)`: a subclass of `SQLAFactoryBase` whose `__init__`, `register` and
  `build` take `self` and are all it defines. `register` declares `version: False`, `timestamp:
  True` and one `Integer` column named by the constructor. `build` finds the row by its value or
  inserts it, carrying a payload's `serial`, and marks the object `_deserialized` or
  `_new_insert`, as `gauge_setting_factory.build` does;
- `SCALAR_TABLES = {"scalar_left": "left_value", "scalar_right": "right_value"}` and
  `SCALAR_VALUES = {"scalar_left": 7, "scalar_right": 11}`;
- `instance_registry()`: `(factories, replicated_tables)`, a copy of the registry's factories with
  `gauge_setting` mapped to `gauge_setting_factory()` and each name of `SCALAR_TABLES` to
  `scalar_entry_factory(column)`, and the registry's replicated tables with the two names added at
  the end. **The instances are made here, on each call, never at import** (correction 1).

Both classes are at module level. No `inventory_spec` is defined, so
`test_store_inventory`'s count of 12 holds (hazard 3).

### 1.4 The test module (§2.4)

**`datastorekit/tests/test_factory_instances.py`**, new, 9 tests in 6 classes, on the stand-in pool
and the neutral client, every store in a `tempfile` directory. `tearDownModule` asserts Ray is not
initialised, and so does each store test's `tearDown`. Pools are built by the module's own
`_StoreCase.open`, `sp.sp_mod.ShardedPool(…)` inside `cluster.active()`, with `cluster.pool` set,
as `StandinCluster.open_pool` builds one (§2.3's first route; `standin_pool.py` is unchanged).
No instance is made at import. `_defines` is imported alone from `test_neutral_client`.

| # | Test | What it does |
|---|---|---|
| 1 | `TestAnInstanceOfAClass.test_an_instance_registered_in_place_of_its_class` | `gauge_setting_factory()` in a copy of the registry; a get inserts (`_new_insert`) and the row is on every shard; closed; a reopen with the same registry gets the same serial, `_deserialized` |
| 2 | `TestAParameterisedFactory.test_two_instances_over_two_tables` | from `instance_registry()`: each instance's `column` and `register()` name its own column (sub-tests); each table gets its value, inserted; closed; each table holds its own value on every shard and not the other's; a reopen finds each under the same serial, `_deserialized` |
| 3 | `TestTheAbstractHooks.test_register_and_build_are_the_only_abstract_hooks` | `__abstractmethods__ == frozenset({"register", "build"})`; a subclass with `build` only and one with `register` only each raise `TypeError` naming the class and the missing hook (three sub-tests) |
| 4a | `TestTheDefaults.test_the_defaults_raise_from_the_class` | `store`, `validate`, `validate_on_startup` called on `gauge_setting_factory` with contract §3's arguments each raise `NotImplementedError` with no arguments |
| 4b | `….test_the_defaults_raise_from_an_instance` | the same on `gauge_setting_factory()` |
| 4c | `….test_through_the_pool_with_the_class_registered` | on a new store for each, `object_store` and then `object_validate` of a `gauge_setting` got through the pool raise `NotImplementedError` at the caller's `resolve` (`ray.get`), the class registered; stdout and stderr redirected around the call; each pool closed in a `finally` |
| 4d | `….test_through_the_pool_with_an_instance_registered` | the same with `gauge_setting_factory()` registered |
| 5 | `TestSerialisation.test_a_registry_of_instances_round_trips_cloudpickle` | `instance_registry()`'s factories through `ray.cloudpickle.dumps` / `loads`: the copies are new instances of their classes, each parameterised one with its column; every class in the registry comes back as itself; the copies serve test 2's checks; Ray is not initialised afterwards |
| 6 | `TestDefinesReadsAnInstanceAsItsClass.test_defines_of_a_class_and_of_its_instance` | for `gauge_setting_factory` and `gauge_setting_factory()`: `register` and `build` defined, `store`, `validate`, `validate_on_startup` and `revalidate` not; for `scalar_entry_factory("left_value")`: `register` and `build` defined, the six defaults not |

### 1.5 The smoke script (§2.5)

`docs/extraction/ray_smoke_run.py`, 115 lines added and none removed (SHA-256
`032036798e101d610a4ac0185ea4eaa7f1db0fe58f52c48ad9f3707548a6a92a`):

- **Step I** (`step_instances`, `:545`; label `"I"`, title "a registry of instances", `needs`
  `[]`, `:609`): on its own store (`INSTANCES_STORE = "instances.sqlite"`, `:131`, beside the
  other steps' in the temporary directory), it imports `datastorekit.tests.client.instances`
  inside the step, makes `instance_registry()`, checks that the three entries are instances, and
  prints them. It opens a read-write pool (`open_instance_pool`, `:497`, with the client's
  `sharded_tables`, `read_table_config` and `serial_batch_sizes`, three shards, the label
  `"standin"`), gets a row of each table and a `gauge_setting` (`get_instances`, `:520`), each of
  which must be `_new_insert`; closes the pool, checks its names released and drops it; reopens
  with the same registry, and the same gets must each be `_deserialized` under the same serial;
  closes, checks and drops again. Each pool is closed and dropped in a `finally`.
- **The docstring's step list** gains item I, saying it was added by `factory-defaults` prompt 01.
  Step 6's line keeps its full stop: `docs/` is additive (§2 item 13).
- Nothing else changed: `main`, the refusals, the start and stop of Ray, the process check and
  steps 1–6 are as they were.

### 1.6 The documents (§2.6–§2.8)

- **`docs/client-contract.md`**, 24 lines added and 5 changed. The head gains §9.5's line after
  §9.4's. §3's first sentence (`:119`) and second (`:120`) end with *(superseded in part by §9.5)*
  inside the full stop, and so does the "Kind" cell of the `store`, `validate` and
  `validate_on_startup` rows (`:126-128`) after its text (correction 2). **§9.5 `factory-defaults`
  prompt 01** follows §9.4: a preamble and three rows, "A factory may be an instance",
  "`store`, `validate`, `validate_on_startup`" and "What a pool's actors receive", each with its
  "Supersedes", its `path:line`s at this tree, and what pins it.
- **`docs/extraction-verification.md`**, 264 lines added and none removed: **§4.8**, after §4.7
  (step I, the three runs' environment and output, and the Ray processes), and **§8.1**, after §8's
  tally (07a §7.3 addressed from this tree; §8's table and tally unchanged).
- **`prompts/extraction/README.md`**: three lines added after U32's paragraph, inside its bullet,
  the italic note in §2.8's words. **`prompts/extraction/IMPLEMENTATION_STATE.md`**: U32's row
  (`:62`) is the row as it was plus a dated italic note in its status cell. Nothing else on that
  board changed.

### 1.7 The records

- **This campaign's board**: the header (in progress; 01 landed, not yet reviewed) and 01's row
  (landed, `f5d8957`, the log). The decisions table, §2, §3 and §4 are unchanged: no issue is
  held.
- **This campaign's README**: a sentence in its header, and §2's row for 01 (landed).
- **`prompts/INDEX.md`**: the header (1 in progress, 2 closed) and the campaign's status.
- **`docs/OPEN_ISSUES.md`**: unchanged, **4 open** (no issue opened or closed).
- **This log.**

---

## 2. Deviations from the prompt

1. **Correction 1: no factory instance is made at import.** `instances.py` makes its instances in
   `instance_registry()`, the test module in its tests, and the smoke script imports
   `instances` inside step I. Under (a) the new module fails test by test, and the smoke script
   fails at step I alone (§5). **STRUCTURALLY REQUIRED.**
2. **Correction 2: five markers, not four.** At the end of §3's first sentence and of its second,
   and at the end of each of the three "Kind" cells. `git diff --word-diff` shows each of the five
   changed lines as the old line plus `{+*(superseded in part by §9.5)*+}` and, for the two
   sentences, the full stop moved after it (`[-enforced.-]{+enforced *(superseded in part by
   §9.5)*.+}`). §9.5's first row names both sentences. **STRUCTURALLY REQUIRED.**
3. **Correction 3: (a) fails test 6 too; test 4's form.** Test 4 is four tests: the direct calls
   on the class and on an instance, and the pool calls with the class and with an instance
   registered. Under (a) the two class tests pass (`v0.2.2`'s behaviour), and the suite gives
   `Ran 504 tests … FAILED (failures=2, errors=6)`: errors in tests 1, 2, 4b, 4d, 5 and 6, each
   `TypeError: Can't instantiate abstract class gauge_setting_factory without an implementation for
   abstract methods 'store', 'validate', 'validate_on_startup'` (6 lines), raised at an
   instantiation (test 2 and 5's in `instance_registry()`, whose first instance is the gauge's);
   failures in test 3 (its `__abstractmethods__` sub-test) and in §2.2's test; nothing else.
   Recorded as found; the form is an **IMPLEMENTATION CHOICE**.
4. **Correction 4: (c) fails test 6 and test 4's pool half.** Measured on the two modules:
   `FAILED (failures=2, errors=2)`. Errors: 4a's `store` sub-test and 4c's `object_store`
   sub-test, each `TypeError: SQLAFactoryBase.store() missing 1 required positional argument:
   'obj'`. Failures: test 6, `True is not false : store`, for `gauge_setting_factory()` and for the
   parameterised instance (two entries). The note's `failures=1, errors=2` counts test 6 once; mine
   has two assertions on instances. The first run of (c) gave `errors=3`: 4c's erroring sub-test
   left its pool open, and the next sub-test's open collided on `SerialPoolBroker` in the same
   cluster. Test 4's pool half now closes each pool in a `finally` (item 11), and the re-run gave
   the count above. Recorded as found.
5. **Correction 5: (e) fails test 5 too.** Tests 2 and 5 each fail twice: the instance's column
   (`'left_value' != 'right_value'`, sub-test `scalar_right`) and the table's columns
   (`'right_value' not found in ['serial', 'timestamp', 'left_value']`). Recorded as found.
6. **Correction 6: where the verification subsections go.** §4.8 is between §4.7's last line and the
   `---` before `## 5. The pin (U42)`; §8.1 between §8's tally and the `---` before `## 9. Known
   gaps`. Every other line number the prompt cites held. Recorded as found.
7. **Correction 7: test 4's pool half redirects stdout and stderr** around the failing call; the
   stand-in prints the actor's traceback there, as at `v0.2.2`. Recorded as found.
8. **The orchestrator's additions**, each followed as given, each an **IMPLEMENTATION CHOICE** at
   the orchestrator's direction: the order of work (the baseline; §2.1 and §2.2 with the existing
   suite at the high end, 495, before the new modules; §2.3 and §2.4 with the suite at both ends;
   the breakages; §2.5 and the smoke runs; the documents and records; the final checks); every
   export installed editable into a fresh offline venv, no `PYTHONPATH`; `_defines` imported
   alone; test 4's pool half on a fresh store per call; the parameterised factory's objects got and
   never stored; the `ast` comparison (§1.1); the vocabulary check (§4.5).
9. **The comment moved, not the hooks.** §2.1 says to move the three below the comment. The three
   already stood before `revalidate`, so the comment was moved up, above `store`, which gives the
   order §2.1 asks for (`register`, `build`, the comment, `store`, `validate`,
   `validate_on_startup`, `revalidate`, …) with a smaller diff. **IMPLEMENTATION CHOICE.**
10. **§2.3's first route.** The test module builds its pools itself; `standin_pool.py` is
    unchanged. **IMPLEMENTATION CHOICE.**
11. **Test 4's pool half closes each pool in a `finally`**, so that a sub-test that errors does not
    leave its pool's names reserved for the next (item 4). **IMPLEMENTATION CHOICE.**
12. **Ten new tests, not eight.** Test 4 is four tests (item 3), so the suite is 494 + 10 = 504.
    Tests 1 and 2 also check `_new_insert` on the first get and `_deserialized` on the reopen, and
    read each table's values on every shard. **IMPLEMENTATION CHOICE.**
13. **The smoke script's step list keeps step 6's line**, full stop and all, and adds item I after
    it: under `docs/` no line is removed. **STRUCTURALLY REQUIRED.**
14. **Step I imports `instances` inside the step and opens its pools through its own helper**, so
    that `main`'s imports and `Smoke`'s constructor are unchanged; it prints the registry's
    instances and the serials the first pool inserted. **IMPLEMENTATION CHOICE.**
15. **§9.5's third row** also says that §6's last row ("Picklable, defined at module level") still
    holds, and that the stand-in pool passes a constructor's arguments as they are
    (`tests/standin_pool.py:209-211`), so the suite sees serialisation only through test 5.
    **IMPLEMENTATION CHOICE.**
16. **The note on U32 in the extraction README** is three continuation lines of U32's bullet, so
    that it renders inside that item. **IMPLEMENTATION CHOICE.**
17. **The smoke runs were taken without a stop.** The dispatch expected the foreign Ray instance to
    block them. It had gone by this prompt's start: `pgrep -fl` found no Ray process at 20:21, and
    the script's rule none at 20:25:56, 20:42:51, or before and after each run (§3 hazard 7).
    Recorded as found.

No UNINTENDED DRIFT was found.

---

## 3. The hazards (§3)

1. **The guard.** `test_layer_is_generic` and `test_prose_names_no_source` pass in every run of the
   suite, and on their own at the end (§4.2). `factory_base.py`'s new comment and docstrings name
   no client, table or class of a client.
2. **A default made an instance method, or made to return.** Breakages (c) and (d) each fail test
   4 (§5): (c) with `TypeError` where `NotImplementedError` is required, on the class, directly and
   through the pool, and test 6; (d) in all four of test 4's `validate` cases.
3. **The inventory's count of 12.** `instances.py` defines no `inventory_spec`;
   `test_store_inventory` passes in every run.
4. **The stand-in pool** is unchanged (§2.3's first route).
5. **Additive documents.** `git diff` of `docs/extraction-verification.md`,
   `docs/extraction/ray_smoke_run.py` and `prompts/extraction/README.md` shows `+` lines only.
   `prompts/extraction/IMPLEMENTATION_STATE.md`'s one changed line is U32's row plus its note.
   `docs/client-contract.md` shows `+` lines and exactly five changed lines, each the old line plus
   a marker (§2 item 2). `docs/adoption/` and the other scripts of `docs/extraction/` are
   unchanged.
6. **No Ray in the suite.** Test 5 imports `ray.cloudpickle`, which starts nothing; the module's
   `tearDownModule` and test 5's own assertion pass in every run.
7. **Ray, and offline only.** Ray was started only by the smoke script, from scratch venvs, three
   times, one after another, with no suite running. By the script's rule (my
   `<scratch-fd01>/probe/raycheck.py` loads the script's `ray_processes()` and runs it), no Ray
   process was up before or after any run, nor at 20:25:56, 20:42:51 and at the end (§4.6).
   `RAY_ADDRESS` and `RAY_ENABLE_AUTO_CONNECT` were unset and there was no
   `/tmp/ray/ray_current_cluster` throughout. Every venv and install was `uv … --offline`; every
   pin resolved offline. No `git fetch`, `push` or `ls-remote` was run.
8. **The clients** were read only with `git -C <client> rev-parse` and `status --short` (§4.7).

---

## 4. Verification performed

### 4.1 The suite

Each run in the foreground, from its tree's root, its output to a scratch file, the verdict taken
with `grep -E '^Ran |^OK|^FAILED'` and the warnings with `grep -c ResourceWarning`. High-end venvs:
Python 3.13.16, Ray 2.55.1, SQLAlchemy 2.0.46, `setuptools`, the export installed with `uv pip
install --offline --no-deps --no-build-isolation -e`. SQLite is 3.53.4 everywhere. `venv/`
(3.12.15 / 2.43.0 / 2.0.39, `datastorekit 0.2.2` editable from this checkout) was not reinstalled.

| When | Where | Result | `ResourceWarning` lines |
|---|---|---|---|
| start (20:22) | `venv/` | `Ran 494 tests in 90.606s` / `OK` | 0 |
| start (20:23) | `<scratch-fd01>/base-hi`: `git archive HEAD` (`b8a00ad`) | `Ran 494 tests in 102.401s` / `OK` | 0 |
| after §2.1 and §2.2, before the new modules (20:26) | `<scratch-fd01>/stage2-hi`: an export of the working tree | `Ran 495 tests in 182.928s` / `OK` | 0 |
| after §2.3 and §2.4 (20:33) | `venv/` | `Ran 504 tests in 145.939s` / `OK` | 0 |
| after §2.3 and §2.4 (20:35) | `<scratch-fd01>/stage3-hi`: an export of the working tree | `Ran 504 tests in 119.782s` / `OK` | 0 |
| end (20:54) | `venv/` | `Ran 504 tests in 110.155s` / `OK` | 0 |
| end (20:56) | `<scratch-fd01>/final-hi`: an export of the final working tree, this log included | `Ran 504 tests in 150.339s` / `OK` | 0 |

The stage runs at 20:33 and 20:35 preceded item 11's `finally` in test 4; the end runs are of the
final tree. The run times vary with the machine's load (another session was working in a client's
checkout); not measured further.

### 4.2 The checks

- **The port check**, `venv/bin/python docs/extraction/compare_ported_tests.py`: exit 0, "OK: 20
  module(s) keep their source's tests, classes and assertion skeletons; 1 test(s) declared not
  ported", at the start and at the end. The new module is not a port.
- **`black --check datastorekit docs`** (25.1.0): 72 files at the start; **74** at the end, the
  two new modules the two more. Every changed `.py` file was formatted.
- **The guards**, `test_layer_is_generic` and `test_prose_names_no_source`, with
  `test_store_inventory`, run on their own at the end: `Ran 56 tests … OK`.
- **Scope** (E1): `git status` shows, under `datastorekit/`, `SQL/factory_base.py` and
  `tests/test_neutral_client.py` modified and `tests/client/instances.py` and
  `tests/test_factory_instances.py` new; `registry.py`, `factories.py` and `standin_pool.py` are
  unchanged. Every changed file is in §7's list.
- **The breakages as recorded** (§5): the five diff blocks of §5, extracted from this log, are
  byte-equal to the diffs applied, and each passed `git apply --check`, `git apply`, `git apply -R
  --check` and `git apply -R`, one after another, on a fresh export of the final working tree
  (`<scratch-fd01>/recorded-check`).

### 4.3 The smoke runs

Each from its own fresh export of the working tree and fresh offline venv, from the export's root,
as `env -u PYTHONPATH <venv>/bin/python docs/extraction/ray_smoke_run.py` under `/usr/bin/time -p`.
The script is `f5d8957`'s (SHA-256 `03203679…a92a`, equal in each export). The full output of
each is in `docs/extraction-verification.md` §4.8.

| Run | Started | Ray's session directory | `ray.init` | Steps (1, 2, N, C, 3, 4, 5, 6, I) | In all | Exit | Ray before; after (script; mine) |
|---|---|---|---|---|---|---|---|
| low (3.12.15 / 2.43.0 / 2.0.39) | 20:43:18 | `session_2026-10-11_20-43-20_087521_39121` | 4.1 s | every one PASS: 0.9, 0.0, 1.4, 1.5, 1.5, 1.4, 0.0, 1.8, 3.0 s | 19.0 s (real 19.34) | **0** | 0; 0 and 0 |
| high (3.13.16 / 2.55.1 / 2.0.46) | 20:43:43 | `session_2026-10-11_20-43-45_431275_39477` | 6.8 s | every one PASS: 1.5, 0.1, 1.9, 1.6, 1.6, 2.1, 0.0, 2.0, 4.3 s | 24.9 s (real 25.29) | **0** | 0; 0 and 0 |
| (a), high | 20:44:15 | `session_2026-10-11_20-44-16_911206_40041` | 5.5 s | 1–6 PASS; **I FAIL** | 17.7 s (real 17.97) | **1** | 0; 0 and 0 |

Step I's lines:

```text
LOW:  PASS  step I (3.0 s): serials {'scalar_left': 1, 'scalar_right': 1, 'gauge_setting': 1}, inserted, and found again after a reopen; after each __exit__, 0 of 4 held
HIGH: PASS  step I (4.3 s): serials {'scalar_left': 1, 'scalar_right': 1, 'gauge_setting': 1}, inserted, and found again after a reopen; after each __exit__, 0 of 4 held
(a):  FAIL  step I (0.0 s): builtins.TypeError: Can't instantiate abstract class gauge_setting_factory without an implementation for abstract methods 'store', 'validate', 'validate_on_startup'
```

At both ends each step I line was preceded by `the registry's instances: scalar_left:
scalar_entry_factory('left_value'), scalar_right: scalar_entry_factory('right_value'),
gauge_setting: gauge_setting_factory()`, and steps 1–6 gave §4.7's results (step C's refusal was
`builtins.ValueError` at 2.43.0 and `ray.exceptions.ActorAlreadyExistsError` at 2.55.1). Before the
real runs, step I was run once on the stand-in pool with a stand-in `ray` (`get` and `get_actor`),
from `<scratch-fd01>/probe/dry_step_i.py`, which starts no Ray: it passed. Ray's session
directories under `/tmp/ray/` were not touched, and none was deleted.

### 4.4 The breakages

§5.

### 4.5 The documents and the names

- **Names**, imported in `venv/` from `/private/tmp` (so that the checkout is reached only through
  the editable install): `SQLAFactoryBase` (its `__abstractmethods__` is `['build', 'register']`;
  `store`, `validate` and `validate_on_startup` start at `:21`, `:32`, `:42` by
  `co_firstlineno`); `instances.instance_registry`, `scalar_entry`, `scalar_entry_factory`,
  `SCALAR_TABLES`, `SCALAR_VALUES`; `factories.gauge_setting_factory`;
  `test_neutral_client._defines`, `ABSTRACT_HOOKS`, `DEFAULTED_HOOKS`; `ray.cloudpickle`; the six
  `Test…` classes of the new module; and, from the smoke script loaded by path, `INSTANCES_STORE`,
  step `("I", "a registry of instances")` and `Smoke.step_instances`, `open_instance_pool` and
  `get_instances`. All exist; Ray was not initialised.
- **Anchors**, by GitHub's rule (lower-case; drop what is not a word character, a hyphen or a space;
  spaces to hyphens), each unique in its file: `#95-factory-defaults-prompt-01` (the contract);
  `#48-the-smoke-run-with-a-registry-of-instances-factory-defaults-prompt-01-2026-10-11`,
  `#481-the-output-low-end`, `#482-the-output-high-end`, `#483-breakage-a-under-ray` and
  `#81-07a-73-after-factory-defaults-prompt-01-2026-10-11` (the verification document). No link to
  an anchor was added.
- **Relative links** added, each resolved from its file: `../prompts/factory-defaults/README.md`
  (the contract); `../prompts/factory-defaults/01-the-base-defaults-three-hooks.md` and
  `../prompts/factory-defaults/logs/01-the-base-defaults-three-hooks.md` (the verification
  document); `../factory-defaults/README.md` (the extraction board);
  `logs/01-the-base-defaults-three-hooks.md` (this campaign's board and README);
  `../01-the-base-defaults-three-hooks.md` (this log).
- **`path:line`s** of §9.5 and of §1 above were read at this tree: `SQL/factory_base.py:5-80`,
  `:6-9`, `:11-14`, `:16-19`, `:21-30`, `:32-40`, `:42-50`, `:52-80`; `SQL/schema.py:99`;
  `SQL/Datastore.py:266`, `:492`, `:565`, `:711`, `:876`; `SQL/ShardedPool.py:156`, `:337`, `:645`,
  `:2289`, `:2324-2325`; `tests/standin_pool.py:209-211`.
- **Neutral names** (`<scratch-fd01>/probe/vocab_check.py`, which loads
  `datastorekit/tests/data/client_vocabulary.json`, the union of the three clients' registry keys,
  column names, packages and extra names, 429 words): each new identifier, table and column name,
  exactly and case-folded, and each of its `_`-separated parts. No name is in the vocabulary, but
  `value`, the object's attribute and the payload's key: a plain-word column of a client, which the
  guard's rule does not forbid ("A plain-word column, such as `source` or `value`, cannot be told
  from English", `registry_words`' docstring). `left_value` and `right_value` have `value` as a
  part, and are not in the vocabulary. §6 item 1.

### 4.6 Ray's processes

By the script's rule (`<scratch-fd01>/probe/raycheck.py`): 0 at 20:25:56, 20:42:51, 20:43:18,
20:43:37, 20:43:43, 20:44:09, 20:44:15, 20:44:33 and 20:59:24 (the end). `pgrep -fl
'gcs_server|raylet|ray::|default_worker\.py'` found none at 20:21.

### 4.7 The clients

Read only with `git -C <client> rev-parse --short HEAD`, `rev-parse --abbrev-ref HEAD` and
`status --short`.

| Client | Start (20:21) | End (20:59) |
|---|---|---|
| SecondaryGWKit | `6861a9f`, `handover-remedial`; 1 modified (`docs/dk-and-rpk-migration-verification.md`), 18 untracked (17 `docs/dk-and-rpk-migration/rehearsal/*_05.txt`, and `prompts/dk-and-rpk-migration/logs/05-rehearse-through-datastorekit.md`) | **`0972599`**, `handover-remedial`; 1 modified (`requirements.txt`, one line added), 0 untracked. Three commits landed there during this prompt, by the other session: `f3f0879` (20:22:36, "Rehearse the reference build through datastorekit (R1)"), `2d3429c` (20:33:38) and `0972599` (20:52:41, "Write the orchestrator note for dk-and-rpk-migration prompt 06"). This prompt read it only through `git` |
| ChamPBH | `52142d7`, `main`; 1 modified (`prompts/INDEX.md`), 24 untracked | `52142d7`, `main`; the same 1 modified and 24 untracked (`diff` of the two listings empty) |
| StochasticInstantons | `7bb3efd`, `main`, clean | `7bb3efd`, `main`, clean |

SGK's status at the start was not the dispatch note's (0 modified, 17 untracked), and its `HEAD`
moved during this prompt: another session was working there, as the note said, and committed
three times. Its `HEAD` at the start was the note's. CPBH and SI are unchanged.

---

## 5. The deliberate-breakage record (§4.4)

Each diff is relative to the repository root, exactly as applied, to its own fresh export of the
working tree (`<scratch-fd01>/break-<x>/tree`) with its own fresh offline venv at the high end,
installed editable. Each passed `git apply --check`, was applied with `git apply`, and then passed
`git apply -R --check`. (a) ran the whole suite; (b)–(e) ran the two modules,
`test_factory_instances` and `test_neutral_client` (29 tests). "Entries" are `unittest`'s failures
plus errors, a sub-test counting on its own. Each was run again on the final code (20:48–20:52),
with the results below; (c)'s run is the one after §2 item 11. None was committed. 0
`ResourceWarning` lines under every one.

### (a) `@abstractmethod` restored on the three — the positive control

```diff
diff --git a/datastorekit/SQL/factory_base.py b/datastorekit/SQL/factory_base.py
index 41c3cdc..b8ce611 100644
--- a/datastorekit/SQL/factory_base.py
+++ b/datastorekit/SQL/factory_base.py
@@ -19,6 +19,7 @@ class SQLAFactoryBase(ABC):
     # NotImplementedError, or returns its default, as below.
 
     @staticmethod
+    @abstractmethod
     def store(obj, conn, table, inserter, tables, inserters):
         """
         Store ``obj``, an object of this factory's class, through ``inserter``, and return the
@@ -30,6 +31,7 @@ class SQLAFactoryBase(ABC):
         raise NotImplementedError
 
     @staticmethod
+    @abstractmethod
     def validate(obj, conn, table, tables):
         """
         Validate ``obj``, an object of this factory's class, and return the outcome. The layer
@@ -40,6 +42,7 @@ class SQLAFactoryBase(ABC):
         raise NotImplementedError
 
     @staticmethod
+    @abstractmethod
     def validate_on_startup(conn, table, tables, prune=False):
         """
         Return lines describing the stored rows that are not validated, and, with ``prune``,
```

`Ran 504 tests … FAILED (failures=2, errors=6)`. **Errors** (6), each `TypeError: Can't instantiate
abstract class gauge_setting_factory without an implementation for abstract methods 'store',
'validate', 'validate_on_startup'`, raised at an instantiation: test 1 (`factories[GAUGE_TABLE] =
gauge_setting_factory()`), test 2 and test 5 (`instance_registry()`'s `factories["gauge_setting"] =
_f.gauge_setting_factory()`), 4b (`gauge_setting_factory()`), 4d (`_with_gauge_instance()`), test 6
(`(gauge_setting_factory, gauge_setting_factory())`). **Failures** (2): test 3's
`__abstractmethods__` sub-test (`{'build', 'register'} != frozenset({…, 'store', 'validate',
'validate_on_startup'})`; its two `TypeError` sub-tests pass), and `test_neutral_client`'s
`test_the_hook_lists_are_the_bases`. 4a and 4c pass. **Nothing else in the 504 fails.** Under Ray,
step I fails (§4.3).

### (b) `@abstractmethod` removed from `register`

```diff
diff --git a/datastorekit/SQL/factory_base.py b/datastorekit/SQL/factory_base.py
index 41c3cdc..b76fe4d 100644
--- a/datastorekit/SQL/factory_base.py
+++ b/datastorekit/SQL/factory_base.py
@@ -4,7 +4,6 @@ from typing import List, Optional
 
 class SQLAFactoryBase(ABC):
     @staticmethod
-    @abstractmethod
     def register():
         raise NotImplementedError
 
```

`FAILED (failures=3)`: test 3's `__abstractmethods__` sub-test (`{'register', 'build'} !=
frozenset({'build'})`) and its `lacks_register` sub-test (`TypeError not raised`), and
`test_the_hook_lists_are_the_bases`.

### (c) `store`'s default made an instance method

```diff
diff --git a/datastorekit/SQL/factory_base.py b/datastorekit/SQL/factory_base.py
index 41c3cdc..b168002 100644
--- a/datastorekit/SQL/factory_base.py
+++ b/datastorekit/SQL/factory_base.py
@@ -18,8 +18,7 @@ class SQLAFactoryBase(ABC):
     # alike, only in the case its docstring names; a hook the factory does not define then raises
     # NotImplementedError, or returns its default, as below.
 
-    @staticmethod
-    def store(obj, conn, table, inserter, tables, inserters):
+    def store(self, obj, conn, table, inserter, tables, inserters):
         """
         Store ``obj``, an object of this factory's class, through ``inserter``, and return the
         object as stored. The layer calls it, in an actor, for every store of an object of the
```

`FAILED (failures=2, errors=2)`: 4a's `store` sub-test and 4c's `object_store` sub-test error with
`TypeError: SQLAFactoryBase.store() missing 1 required positional argument: 'obj'` (the layer's own
call, `factory.store(obj, conn=…, …)`, binds `obj` to `self` on a class); test 6 fails twice, `True
is not false : store`, for `gauge_setting_factory()` and for `scalar_entry_factory("left_value")`,
whose `store` is now a bound method. 4b and 4d pass: an instance's call binds `self` and reaches the
`NotImplementedError` (§2 item 4).

### (d) `validate`'s default returning `None`

```diff
diff --git a/datastorekit/SQL/factory_base.py b/datastorekit/SQL/factory_base.py
index 41c3cdc..3cad904 100644
--- a/datastorekit/SQL/factory_base.py
+++ b/datastorekit/SQL/factory_base.py
@@ -37,7 +37,7 @@ class SQLAFactoryBase(ABC):
         calls it on the controlling shard, and, when that outcome is true, on every other shard,
         whose outcome must equal it.
         """
-        raise NotImplementedError
+        return None
 
     @staticmethod
     def validate_on_startup(conn, table, tables, prune=False):
```

`FAILED (failures=4)`: the `validate` case of each of 4a, 4b, 4c and 4d, `NotImplementedError not
raised`.

### (e) §2.3's two instances on one column name

```diff
diff --git a/datastorekit/tests/client/instances.py b/datastorekit/tests/client/instances.py
index 3defd1a..e0733b5 100644
--- a/datastorekit/tests/client/instances.py
+++ b/datastorekit/tests/client/instances.py
@@ -93,6 +93,6 @@ def instance_registry() -> Tuple[Dict[str, object], List[str]]:
     factories = dict(_registry.factories)
     factories["gauge_setting"] = _f.gauge_setting_factory()
     for name, column in SCALAR_TABLES.items():
-        factories[name] = scalar_entry_factory(column)
+        factories[name] = scalar_entry_factory("left_value")
     replicated_tables = list(_registry.replicated_tables) + list(SCALAR_TABLES)
     return factories, replicated_tables
```

`FAILED (failures=4)`: tests 2 and 5, each twice: `'left_value' != 'right_value'` (sub-test
`scalar_right`) and `'right_value' not found in ['serial', 'timestamp', 'left_value'] : (0,
'scalar_right')`.

---

## 6. Observations not acted on

1. **`value` is a client's plain-word column.** The parameterised object's attribute and its
   payload key are `value`, which one client's registry has as a column (§4.5). The guard does not
   forbid plain words, by design, and does not scan `tests/`; the neutral client already uses plain
   words of the kind. Not opened as an issue.
2. **A parameterised factory's objects can be got, but not stored or validated, through the pool**
   under two registry names: the pool dispatches a store and a validate by `type(obj).__name__`
   (`SQL/ShardedPool.py:3455`, `:3548`), and `scalar_entry` is neither `scalar_left` nor
   `scalar_right`. `scalar_entry_factory` defines neither hook, so nothing reaches it, and no test
   tries. It is contract §6's first row ("must be the registered name"), an existing fact; no issue.
3. **The suite cannot see an actor unpickle a registry.** The stand-in pool passes constructor
   arguments as they are (`tests/standin_pool.py:209-211`); test 5's round trip and smoke step I
   cover it. Contract §9.5's third row says so. By U3's design; no issue.
4. **A Ray session directory not of this prompt**,
   `/tmp/ray/session_2026-10-11_20-24-26_375548_24732`, appeared between the start and the first
   check by the script's rule; no Ray process was found at 20:25:56. This prompt started no Ray
   then, and touched nothing under `/tmp/ray/`.
5. **The scratch tools** are in `<scratch-fd01>/probe/`, not in the repository: `mkenv.sh` (an
   export and its venv), `suite.sh`, `breakrun.sh`, `mkbreak.py` (which wrote the five diffs),
   `raycheck.py`, `dry_step_i.py`, `ast_compare.py` and `vocab_check.py`. Each run's output is in
   `<scratch-fd01>/logs/`, and each diff in `<scratch-fd01>/diffs/`.

---

## 7. Issues

- **Opened, narrowed or closed**: none.
- **`docs/OPEN_ISSUES.md`**: unchanged, **4 open**, 0 on this repository's boards, 4 inherited.

---

## 8. State handed to the next prompt

- **`HEAD`** is `f5d8957`, unpushed and untagged. `origin/main` is `460b012`; the tags are
  `v0.1.0`, `v0.2.0`, `v0.2.1` and `v0.2.2`, unchanged. `pyproject.toml` is at `0.2.2`.
- **The suite** is 504, in `venv/` and at the high end. The port check passes over 20 modules with
  1 test declared not ported. `black` leaves 74 files unchanged.
- **The interfaces** (README §4): the base's two abstract and six defaulted hooks;
  `datastorekit/tests/client/instances.py` (`scalar_entry`, `scalar_entry_factory`,
  `SCALAR_TABLES`, `SCALAR_VALUES`, `instance_registry()`); `tests/test_factory_instances.py`;
  `ABSTRACT_HOOKS` and `DEFAULTED_HOOKS` in `test_neutral_client.py`; the smoke script's step I;
  contract §9.5 and its five markers; verification §4.8 and §8.1; the notes on extraction U32.
- **For 02** (`v0.2.3`, U5): what changes for a client is that a factory class defining `register`
  and `build` can be instantiated and registered; an instance meets, for a hook its class does not
  define, what a class meets; and a registered instance must be of a module-level class with
  picklable attributes (contract §9.5). SI's three instantiations at import stop raising too
  (README §0.2 item 3). Every factory valid under `v0.2.2` is valid under this tree.
- **Open**: none on this repository's boards; the four inherited issues of `docs/OPEN_ISSUES.md`
  §1.2.
