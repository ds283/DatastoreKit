# Prompt 01 — the base defaults three hooks

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

*Written 2026-10-11 against `460b012`, whose `datastorekit/` is `6d8ee9a`'s (`v0.2.2`).*

**Gate:**
- U1–U3 are taken (README §6.2): as recommended, by the user on 2026-10-11.
- `git status` is clean in this repository, and `origin/main` is an ancestor of `main`.
- `datastorekit/` is `6d8ee9a`'s: `git diff --stat 6d8ee9a HEAD -- datastorekit` is empty.
- The suite gives `Ran 494 tests … OK` in `venv/`.

**Closes:** nothing on a board. **Addresses:** extraction 07a's observation §7.3 (contract §3 does
not say what U32 found about instances), recorded open at `docs/extraction-verification.md:1060`.
**Revisits:** extraction U32, in part (U1). **Opens:** only what the work finds.

**Recommended model:** **Opus.**
- The code change is three deleted decorators and a comment. The risk is not in it but in what it
  must not change: no hook's signature, no message, and nothing a class-registering client meets.
- The tests must fail on `v0.2.2`'s base for the right reason, `TypeError` at instantiation, and
  must not pass for a wrong one, such as a default made an instance method or made to return.
- It starts Ray, for the smoke run only, under README §5 rule 7.
- The contract's §9.5 must supersede §3's first sentence and three rows without rewriting them.

**Read first:**

1. [`README.md`](README.md): all of it, §0.1 and §6.2 especially.
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`.
3. The brief: `/Users/ds283/Documents/Code/ChamPBH/prompts/dk-and-rpk-migration/datastorekit-v0.2.3-brief.md`.
   It is evidence, read as text. Do not act on it beyond this prompt; README §0.1 re-measured it.
4. Extraction U32: `../extraction/README.md` §6.2 (`:585-597`) and that board's decision row
   (`../extraction/IMPLEMENTATION_STATE.md:62`).
5. `docs/client-contract.md`: its head (`:1-55`), §3 (`:113-133`) and §9 (`:278-` end), for the
   form a §9 subsection takes.
6. Item 5 of `docs/adoption/champbh.md` (`:169-238`) and of `docs/adoption/stochasticinstantons.md`
   (`:187-197`), and the adoption README's paragraph on instances (`docs/adoption/README.md:131-142`).
   01 changes none of them; 02 adds their addenda.
7. The code: `datastorekit/SQL/factory_base.py` (all of it); `datastorekit/tests/client/factories.py`
   (`gauge_setting_factory`, `:337-366`, and the module's head); `datastorekit/tests/client/registry.py`;
   `datastorekit/tests/standin_pool.py` (`open_pool`, `:352-376`; `close_pool`, `:413-418`);
   `datastorekit/tests/test_neutral_client.py` (`:60-70`, `:124-130`, `:255-280`);
   `datastorekit/tests/test_store_inventory.py:476-500`; `datastorekit/tests/test_layer_is_generic.py`
   (its docstring); and `docs/extraction/ray_smoke_run.py` (all of it).
8. `actor-names` prompt 01 and its log (`../actor-names/01-a-closed-pool-releases-its-actor-names.md`,
   `../actor-names/logs/01-a-closed-pool-releases-its-actor-names.md`): how a smoke step, a contract
   §9 subsection and a verification subsection were added last time.

Line numbers are at `460b012`, measured on 2026-10-11.

---

## 1. What is wanted

After this prompt, **a factory class that defines `register` and `build` can be instantiated**, and
its instance registered, whatever else it defines:
- `store`, `validate` and `validate_on_startup` are defaulted hooks of `SQLAFactoryBase`, as
  `revalidate` is: static, with today's signatures, raising a bare `NotImplementedError`;
- the base stays an `ABC` with `register` and `build` as its only abstract hooks, so a factory
  class that defines both instantiates, and one that lacks either is still refused;
- a class-registering client (SGK, the neutral client) meets nothing new: every call it makes is
  answered as under `v0.2.2`, `NotImplementedError` included;
- an instance-registering client meets, for a hook its class does not define, exactly what a class
  meets.

The suite sees it, and a revert fails it. The smoke script sees an instance registry sent to real
actors, at both ends.

**Nothing the layer writes changes. No message, refusal or exception changes**, but the one
removed: the `TypeError` on instantiating a factory class that lacks `store`, `validate` or
`validate_on_startup`. `pyproject.toml` stays at `0.2.2`: 02 releases.

### 1.1 What the planner measured

README §0.1 holds the measurements. The ones this prompt rests on:
- no test instantiates a factory or reads `__abstractmethods__`; `_defines` compares by identity
  and is unaffected; `ABSTRACT_HOOKS` (`tests/test_neutral_client.py:64`) names the three;
- the layer calls every hook on the registry entry, and never on `type(factory)` or by a factory's
  `__name__`;
- a prototype (the decorators removed, three scratch tests) gave 497 at the low end; the same three
  tests error with `TypeError` on the unchanged tree; through the pool, a missing `store` or
  `validate` raises a bare `NotImplementedError` for a class and an instance alike;
- `ray.cloudpickle` round-trips an instance registry entry without starting Ray.

---

## 2. What to change

### 2.1 `datastorekit/SQL/factory_base.py` (U1)

- Remove `@abstractmethod` from `store` (`:16-19`), `validate` (`:21-24`) and
  `validate_on_startup` (`:26-29`). Keep `@staticmethod`, the parameter lists, and the bodies
  (`raise NotImplementedError`, with no message) exactly.
- Move the three below the comment on defaulted hooks (`:31-32`), before `revalidate`, and adjust
  the comment so it is true of six hooks. Give each of the three a docstring in the manner of
  `revalidate`'s: what the layer does with it, and when it calls it (contract §3's rows: `store` on
  an `object_store` of the class; `validate` on an `object_validate`; `validate_on_startup` at open
  and at a replicated prune, only for a class whose `register()` declares
  `validate_on_startup: True`).
- `register` and `build` keep `@staticmethod @abstractmethod`. The import of `abstractmethod`
  stays. The base stays `SQLAFactoryBase(ABC)`, and its `__abstractmethods__` becomes exactly
  `{"register", "build"}`.
- **This file is in the layer.** The guard (`test_layer_is_generic`) scans its names, strings,
  docstrings and comments for every client's vocabulary. Write nothing that names a client, a
  client's table or class, or "instance-registering" clients by name.

### 2.2 `datastorekit/tests/test_neutral_client.py` (U2)

- `ABSTRACT_HOOKS = ("register", "build")`; `DEFAULTED_HOOKS` gains `store`, `validate` and
  `validate_on_startup`, in the base's new order. `:259`'s test sums the three lists, so its set of
  hooks is unchanged.
- Add one test, or one assertion in an existing test, that `set(ABSTRACT_HOOKS) ==
  SQLAFactoryBase.__abstractmethods__`, and that every name in `DEFAULTED_HOOKS` is an attribute
  of the base that is not abstract.
- Nothing else in the module changes. The registry and `_defines` stay as they are.

### 2.3 The parameterised factory, and where it lives

A neutral replicated object class with one integer value, and a factory class for it whose
`register`, `build` and `__init__` take `self`, whose constructor takes the name of the value's
column, and which defines nothing else: no `store`, `validate`, `validate_on_startup` or
`inventory_spec`. Its `build` finds the row by its value or inserts it, carrying a payload's
`serial` as `gauge_setting_factory.build` does, and marks the object `_deserialized` or
`_new_insert`.

It must be importable by a Ray worker, for the smoke step (§2.5), so it lives at **module level in
a module under `datastorekit/tests/`**. **Recommended:** a new module
`datastorekit/tests/client/instances.py`, holding the two classes and a function that returns the
registry and the replicated-table list with two instances added under two new names (and,
optionally, `gauge_setting` replaced by `gauge_setting_factory()`). The names are yours. They must
be neutral: check each against `datastorekit/tests/data/client_vocabulary.json`, and say in the
log how. **It is outside `registry.py`**: the neutral client's registry is unchanged.

Hazards of the home:
- `tests/test_store_inventory.py:476-500` counts `inventory_spec` definitions in every module under
  `tests/client/` and pins **12**. The new class defines none, so the count is unchanged. If you
  define one, that test fails: do not.
- The stand-in's `open_pool` (`standin_pool.py:352-376`) passes `replicated_tables` from the
  registry and takes `factories=` by `kwargs.setdefault`. A pool over two new tables needs its own
  `replicated_tables`. Build it with `sp_mod.ShardedPool(…)` inside `cluster.active()`, as
  `open_pool` does, and set `cluster.pool`; or give `open_pool` a `setdefault` for the table lists.
  The second changes test support used by every module; if you choose it, say why in the log
  (IMPLEMENTATION CHOICE), and the suite must stay at 494 + the new tests.

### 2.4 A new test module, `datastorekit/tests/test_factory_instances.py` (U2)

On the stand-in pool and the neutral client, with no Ray, every store in a `tempfile` directory,
and a `tearDownModule` asserting Ray is not initialised, as the other modules do. Tests:

1. **An instance of a class that defines only `register` and `build` (and `inventory_spec`).**
   `gauge_setting_factory()` instantiates. Registered in place of the class (`factories=` of a copy
   of the registry): a get writes a row; the pool is closed; a reopen with the same registry gets
   the same serial, deserialised.
2. **A parameterised factory**, two instances of §2.3's class over two tables differing by the
   constructor's column name. Each gets its rows; the two tables hold different rows (by a value
   got in one and not the other); a reopen finds each table's rows under the same serials; and
   each instance's `register()` names its own column.
3. **The abstract hooks.** `SQLAFactoryBase.__abstractmethods__ == frozenset({"register",
   "build"})`. A subclass defining `build` but not `register`, and one defining `register` but not
   `build`, each raise `TypeError` on instantiation, naming the missing hook.
4. **The defaults.** For `store`, `validate` and `validate_on_startup`, with the arguments contract
   §3 gives each: called on `gauge_setting_factory` and on `gauge_setting_factory()`, each raises
   `NotImplementedError`. Through the pool, on a fresh store for each call: `object_store` of a
   `gauge_setting` raises `NotImplementedError` with `gauge_setting` registered as the class and as
   an instance; so does `object_validate`. (After a failed replicated store the pool's next write is
   refused with `ReplicationInFlight`, as under `v0.2.2`; that is why each call needs its own
   store. Do not test or change it.)
5. **Serialisation.** A registry holding §2.3's two instances and `gauge_setting_factory()`
   round-trips `ray.cloudpickle.dumps` / `loads`. Each copy is an instance of its class with its
   constructor's value, the copies serve a pool as in test 2, and Ray is not initialised afterwards.
6. **`_defines` reads an instance as it reads its class.** Import `_defines` from
   `test_neutral_client`, or restate it, and show: for `gauge_setting_factory` and
   `gauge_setting_factory()` alike, `build` is defined and `store`, `validate`,
   `validate_on_startup` and `revalidate` are not; for §2.3's instance, `register` and `build` are
   defined.

Every test of 1, 2, 5 and the instance half of 4 must **error with `TypeError` at instantiation**
on `v0.2.2`'s base (breakage (a)), and test 3 must fail on it too. Say in the log which fail and
how.

### 2.5 `docs/extraction/ray_smoke_run.py` (U3)

Add a step **I**, "a registry of instances", after step 6, needing no other step:
- on a new store (its own primary, in the script's temporary directory), a read-write pool whose
  registry is §2.3's (two parameterised instances, and `gauge_setting` as an instance);
- a get of one row in each of the two tables and of a `gauge_setting`; the pool closed, and its
  names checked released, as every other step does;
- a reopen, read-write, with the same registry: the same three gets find the same serials; closed
  and dropped.

It passes only if all of that holds. The module docstring's step list gains the step, saying it was
added by `factory-defaults` prompt 01. Nothing else in the script changes.

Run the script under real Ray, per README §5 rule 7, **at both ends** (a scratch venv each, with an
export of your tree installed editable): every step `PASS`, exit 0, no Ray process before or after.
Then once at the high end with breakage (a) applied in the export: step I `FAIL`, naming
`TypeError`, every other step `PASS`, exit 1.

### 2.6 `docs/client-contract.md`

- **At the head**, after `:34-35` (§9.4's line): *"§9.5 is measured from the package at
  `factory-defaults` prompt 01's tree, and its line numbers are that tree's."*
- **A §9.5, "`factory-defaults` prompt 01"**, after §9.4, in §9's form. Its preamble: one change
  (`prompts/factory-defaults/README.md`, decision U1, the user's ruling); nothing the layer writes
  changes, and no message, refusal or exception of the layer's, but the `TypeError` Python raised
  on instantiating a factory class that lacked one of the three. Its rows:
  - **A factory may be an instance.** Supersedes §3's first sentence ("A factory is a class whose
    static methods the layer calls; it is never instantiated, so the abstractness of
    `SQLAFactoryBase` … is never enforced") and its "three defaulted hooks". What holds: the layer
    calls each hook on the registry's entry, class or instance, and never instantiates one itself;
    a class that is instantiated must define `register` and `build`, the base's two abstract hooks;
    the base defaults six. Pinned by tests 1–3 and 6, and smoke step I.
  - **`store`, `validate`, `validate_on_startup`.** Supersedes the "Kind" cell of each of the three
    rows of §3 ("abstract (`:17-20`)", "abstract (`:22-25`)", "abstract (`:27-30`)"). Kind:
    "defaulted: raises `NotImplementedError`", at their lines in your tree. When called and what the
    layer does are §3's, unchanged. Not defined: the base's `NotImplementedError`, from a class or
    an instance alike, reached only when the layer calls the hook. Pinned by test 4.
  - **What a pool's actors receive.** None of §1–§9.4 said. The registry reaches each actor as a
    constructor argument and, under Ray, is serialised with it; a factory instance must be of a
    class defined at module level, and its attributes picklable, as §6 asks of stored objects.
    Pinned by test 5, and smoke step I.
- **The markers.** The contract's head (`:11-13`) says a row of §1–§8 that §9 supersedes "is not
  rewritten, and carries a marker". §9.1 set the form: §1 row 6 ends its cell with
  *"(superseded in part by §9.1)"* (`:69`). §9.3 and §9.4 superseded no row of §1–§8, so set
  none. Append *"(superseded in part by §9.5)"* to §3's first sentence (`:115-116`, at the end of
  that sentence) and to the "Kind" cell of each of the three rows (`:123-125`). That is the only
  change to an existing line: each changed line's diff is the line as it was plus the marker.
- **Nothing else in §1–§9.4 changes.**

### 2.7 `docs/extraction-verification.md`

Add a dated subsection at the end of §8 (before §9, `:1087`): **"8.1 07a §7.3, after
`factory-defaults` prompt 01 (<date>)"**. It says §8's row for 07a §7.3 (`:1060`) was right for the
trees it was taken on, and that from 01's tree the contract says what U32 found about instances, in
§9.5, and the base no longer refuses an instance lacking the three. Add nothing else to §8's table,
and change no line of the document.

Then a subsection of §4, after §4.7: **"4.8 The smoke run with a registry of instances
(`factory-defaults` prompt 01, <date>)"**, in §4.7's form: the environment of each run, the output
of each, the breakage run, and the Ray processes before and after.

### 2.8 Extraction U32

Add, without changing a word of what is there:
- in `../extraction/README.md`, after U32's paragraph (`:597`), an italic line: *"(Revisited in
  part 2026-10-11 by `factory-defaults` U1, on the user's ruling: from `v0.2.3` the base defaults
  `store`, `validate` and `validate_on_startup`, and a client may register instances as they are.
  See `../factory-defaults/README.md` §6.2.)"*;
- in `../extraction/IMPLEMENTATION_STATE.md`, U32's row (`:62`), a dated note in the status cell
  saying the same in a line.

That campaign stays closed. Nothing else on its board changes.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **The guard.** `factory_base.py` is in the layer (§2.1). The guard runs in the suite.
2. **A default made an instance method, or made to return.** Either would pass a careless test 4.
   Breakages (c) and (d) are there to show it does not.
3. **The inventory's count of 12** (§2.3).
4. **The stand-in pool** is test support for every module (§2.3).
5. **Additive documents** (§2.6, §2.7, §2.8). `git diff` of `docs/extraction-verification.md`
   and the two extraction files shows `+` lines only, except U32's board row, whose diff is the row
   as it was plus the note. `git diff` of `docs/client-contract.md` shows `+` lines and exactly four
   changed lines, each the old line plus §2.6's marker; `git diff --word-diff` shows it.
6. **No Ray in the suite.** Test 5 imports `ray.cloudpickle`, which starts nothing; the module's
   `tearDownModule` proves it.
7. **Offline only.** Every venv is made `--offline`. A pin that does not resolve offline is a stop.
8. **The clients.** None is written, run, imported or opened. Record each one's `HEAD` and
   `git status --short` at the start and the end.

---

## 4. Verification

1. **The suite.** `Ran 494 tests … OK` in `venv/` before; after, 494 plus the new tests, `OK`, at
   both ends: `venv/`, and a fresh offline scratch venv (Python 3.13.16, `ray==2.55.1`,
   `sqlalchemy==2.0.46`, `setuptools`) with a `git archive` of your tree installed editable
   (`--no-deps --no-build-isolation`). Record the `ResourceWarning` lines at each end (0 in
   `venv/`; 0 or 4 at the high end is timing, `actor-names` log 01 correction 8).
2. **The checks.** `docs/extraction/compare_ported_tests.py` exits 0 with "20 module(s) … 1 test(s)
   declared not ported"; `black --check datastorekit docs` passes, its file count one or two above
   72 by your new files, said in the log.
3. **The smoke runs** (§2.5): both ends, and the breakage run.
4. **The breakage record.** Each a diff exactly as applied in a scratch export, checked with
   `git apply --check` and `-R --check`, with what failed. None is committed.
   - **(a)** `@abstractmethod` restored on the three: tests 1, 2, 5 and 4's instance half error
     with `TypeError` at instantiation, test 3 fails, and the `ABSTRACT_HOOKS` assertion of §2.2
     fails; nothing else in the suite fails. Smoke step I fails at the high end (§2.5).
   - **(b)** `@abstractmethod` removed from `register` as well: test 3 fails, and the §2.2
     assertion.
   - **(c)** `store`'s default made an instance method (`def store(self, obj, conn, …)`, without
     `@staticmethod`): test 4's call on the class fails with `TypeError`, not
     `NotImplementedError`.
   - **(d)** `validate`'s default returning `None` instead of raising: test 4 fails for `validate`.
   - **(e)** §2.3's two instances built with the same column name: test 2 fails.
5. **The documents.** Every anchor and name §2.6–§2.8 add exists: names by importing them in
   `venv/`, anchors by GitHub's rule. List each in the log.
6. **The clients**, at the start and the end, unchanged (hazard 8).

---

## 5. Acceptance

1. `factory_base.py` is as §2.1 says: every hook's signature and body is as at `v0.2.2`
   (compare the two files' `ast`, ignoring decorators, docstrings and order, and say how in the log).
2. §2.2–§2.8 are done, and the neutral client's `registry.py` and `factories.py` are unchanged.
3. §4.1–§4.6 hold.
4. **The records**, in the same commit:
   - the log `logs/01-the-base-defaults-three-hooks.md`, per README §5.1, with the smoke output, the
     breakage diffs, each name checked, and the clients at the start and the end;
   - this board: §1's row for 01, the header, and the decisions table if any changed;
   - this campaign's README: its header and §2's row for 01;
   - `docs/OPEN_ISSUES.md`: unchanged at **4**, unless the work opens an issue;
   - `prompts/INDEX.md`: the campaign's line.

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count falls, in any venv.
- A test of §2.4 passes on `v0.2.2`'s base where §4.4 (a) says it must not, or fails after the
  change for a reason other than a bug in the test.
- Any change of signature, message, refusal or exception would be needed, or any file under
  `datastorekit/` but `SQL/factory_base.py`, `tests/test_neutral_client.py`, the new test module
  and §2.3's module (and `tests/standin_pool.py`, if §2.3's second route is taken).
- The guard fails on `factory_base.py` and cannot be satisfied by rewording.
- A smoke run fails at either end, other than step I under breakage (a).
- A document cannot say what it must without rewriting a line already in it.
- Anything would push, make or move a tag, download, or write, run, import or open anything of a
  client.

---

## 7. What this prompt changes, and what it does not

- **Files it changes:**
  - `datastorekit/SQL/factory_base.py`;
  - `datastorekit/tests/test_neutral_client.py`; the new `datastorekit/tests/test_factory_instances.py`;
    §2.3's module; `datastorekit/tests/standin_pool.py` only if §2.3's second route is taken;
  - `docs/extraction/ray_smoke_run.py`;
  - `docs/client-contract.md` and `docs/extraction-verification.md`, by addition only;
  - `../extraction/README.md` and `../extraction/IMPLEMENTATION_STATE.md`, by addition only (§2.8);
  - the log, this board, this campaign's README, `docs/OPEN_ISSUES.md` if an issue is opened, and
    `prompts/INDEX.md`.
- **It changes nothing else:** not `pyproject.toml`, `README.md`, `PROVENANCE.md`,
  `docs/adoption/`, the workflow, `CLAUDE.md`, `LICENSE` or `.gitignore`. 02 changes the release's
  files.
- **It touches no client repository.**
- **It makes no tag and pushes nothing.**

---

## 8. After 01

The orchestrator reviews 01 against its commit. 02, the release, is then written against the tree
01 leaves, and carries the adoption addenda (README §6.2, U5).
