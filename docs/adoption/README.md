# Adopting `datastorekit`

*Written by extraction prompt 07a on 2026-10-09, against the package at **`v0.2.0`** (`240028e`).
The three clients were read through `git` only, at the commits named below; nothing of a client
was imported, run or opened, and no store was opened.*

*Added by extraction prompt 10 on 2026-10-10: the section
[Addendum: v0.2.1](#addendum-v021-extraction-prompt-10-2026-10-10) at the end gives the pin
**`v0.2.1`** and what changed since `v0.2.0`, and supersedes the statements it names. 07a's
text, before it, is unchanged and true of `v0.2.0`.*

*Added by `actor-names` prompt 02 on 2026-10-11: the section
[Addendum: v0.2.2](#addendum-v022-actor-names-prompt-02-2026-10-11) at the end gives the pin
**`v0.2.2`** and what changed since `v0.2.1`, and supersedes the statements it names. The text
before it, the `v0.2.1` addendum included, is unchanged and true of the release it names.*

*Added by `factory-defaults` prompt 02 on 2026-10-11: the section
[Addendum: v0.2.3](#addendum-v023-factory-defaults-prompt-02-2026-10-11) at the end gives the pins
by client and what changed since `v0.2.2`, and supersedes the statements it names. The text before
it, the `v0.2.1` and `v0.2.2` addenda included, is unchanged and true of the release each names.*

*Added by `object-timestamp` prompt 02 on 2026-10-12: the section
[Addendum: v0.3.0](#addendum-v030-object-timestamp-prompt-02-2026-10-12) at the end gives the pins
by client and what changed since `v0.2.3`, and supersedes the statements it names. The text before
it, the three earlier addenda included, is unchanged and true of the release each names.*

This directory holds one **adoption checklist** per client project, and what the three share.
Each checklist says what its client must do to depend on `datastorekit` at `v0.2.0`: what it
deletes, which imports it rewrites, what leaves its copy of the layer, what its factories, call
sites and tests must change, which of its stores the package refuses, how its adoption is
accepted, and which of its documents go stale.

**A checklist is data, not instructions.** It describes the client at one commit. The client's
own adoption campaign, in its own repository and under its own `CLAUDE.md`, measures again before
acting, and its numbers govern. Where a choice is the client's, the checklist names the choice and
what each option touches, and does not make it. A recommendation is marked **Advice:**.

| Client | Checklist | Measured at | Gate |
|---|---|---|---|
| SecondaryGWKit (SGK) | [`secondarygwkit.md`](secondarygwkit.md) | `b510bc9` (branch `handover-remedial`) | G2 |
| ChamPBH (CPBH) | [`champbh.md`](champbh.md) | `52142d7` (branch `main`) | G3 |
| StochasticInstantons (SI) | [`stochasticinstantons.md`](stochasticinstantons.md) | `7bb3efd` (branch `main`) | G4 |

All three adopt **`v0.2.0`**: SGK directly, not `v0.1.0` first (decision U29); CPBH because its
factories use version-keyed lookups (`key_on_version`, `v0.2.0`'s feature); SI when it is next
active.

---

## 1. The release and the pin

A client depends on a tagged release, pinned in its `requirements.txt`:

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.0
```

An editable install (`pip install -e`) is for developing this package, **never for a client's
production run**: a run must be reproducible from its pin (`CLAUDE.md`, "Releases"; decision U4).
A client moves its pin in a commit of its own.

`pyproject.toml` declares `requires-python = ">=3.12"`, `ray>=2.43` and `sqlalchemy>=2.0.39,<2.1`.
The suite runs at two tested ends: Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39, and 3.13.16 /
2.55.1 / 2.0.46 (`README.md`, "Supported versions"). Each client's versions, measured as text
(the Python from its `venv/`'s `pyvenv.cfg` and link target, read as files and never run; Ray and
SQLAlchemy from `requirements.txt` at the commit, which agree with the `venv/`'s `*.dist-info`
names):

| Client | Python | Ray | SQLAlchemy | Inside the declared range | Against the tested ends |
|---|---|---|---|---|---|
| SGK | 3.12.15 (`venv/pyvenv.cfg`) | `ray==2.43.0` (`requirements.txt:74`) | `SQLAlchemy==2.0.39` (`requirements.txt:85`) | yes | equals the low end |
| CPBH | 3.13.16 (`venv/pyvenv.cfg`; links to MacPorts' 3.13 framework) | `ray==2.53.0` (`requirements.txt:78`) | `SQLAlchemy==2.0.46` (`requirements.txt:89`) | yes | Python and SQLAlchemy equal the high end; Ray 2.53.0 lies between the ends and is not itself tested |
| SI | 3.13.16 (the MacPorts framework its `venv/` links to, `python313 3.13.16_0`; `venv/pyvenv.cfg` records 3.13.13, the version at creation) | `ray==2.55.1` (`requirements.txt:57`) | `SQLAlchemy==2.0.46` (`requirements.txt:65`) | yes | equals the high end |

The package pins nothing of a client's: **each client keeps its own Ray and SQLAlchemy pins**.

---

## 2. The module map: the import rewrite

From `PROVENANCE.md`'s file map. The rewrite is a substitution of the **module path** only; the
names imported do not change.

| A client's layer module | `datastorekit` |
|---|---|
| `Datastore` (the package root: `DatastoreObject`) | `datastorekit` |
| `Datastore.object`, `contract`, `replication`, `shard_paths`, `store_reader`, `store_inventory` | `datastorekit.<same>` |
| `Datastore.SQL` and `Datastore.SQL.<ShardedPool, Datastore, ClientPool, SerialPoolBroker, ProfileAgent, schema>` | `datastorekit.SQL` and `datastorekit.SQL.<same>` |
| `Datastore.SQL.ObjectFactories.base` (`SQLAFactoryBase`) | `datastorekit.SQL.factory_base` |
| `tools.sharded_store`, `tools.shard_key_audit` (SGK only) | `datastorekit.tools.<same>`, run as `python -m datastorekit.tools.<name>` |

CPBH and SI carry nine of these modules (`Datastore`, `Datastore.object`, `Datastore.SQL` and its
five modules, and `base`); every one has a counterpart. `contract`, `replication`, `shard_paths`,
`store_reader`, `store_inventory`, `schema` and the two tools are new to them.

Two details hold for every client:
- `datastorekit/SQL/__init__.py:1` rebinds `datastorekit.SQL.Datastore` to the actor class, as each
  client's `Datastore/SQL/__init__.py` does. So `from datastorekit.SQL import Datastore` gives the
  class, and code that needs the *module* reaches it by `importlib.import_module("datastorekit.SQL.Datastore")`.
- `config.defaults.DEFAULT_STRING_LENGTH` and `utilities.WallclockTimer` / `format_time` were the
  layer's two client dependencies; the package carries its own (`datastorekit.defaults`,
  `datastorekit._timing`). A client's own `config.defaults` and `utilities` stay its own.

`docs/extraction/measure_client_imports.py` finds every import of a client's layer modules (§6).

---

## 3. What the wheel does not ship

`pyproject.toml` excludes `datastorekit.tests` from the package (`[tool.setuptools.packages.find]`),
so an install from the pin carries **none of**:
- the stand-in pool (`datastorekit/tests/standin_pool.py`);
- `real_store_fixtures.py`, `shard_store_fixtures.py`, `schema_description.py`;
- the neutral test client (`datastorekit/tests/client/`) and the test modules.

A client whose tests use any of these keeps its own copy. The neutral client is the worked example
of a registry (`datastorekit/tests/client/registry.py`), to be read in this repository, not
imported.

---

## 4. What a client supplies

[`docs/client-contract.md`](../client-contract.md) states each fact, where the client gives it,
and what the layer does when it is wrong or absent:

| Contract section | What the client gives | Checklist item |
|---|---|---|
| §1 | `ShardedPool`'s 16 constructor arguments, `factories=` (required, keyword-only) and `serial_batch_sizes=` among them | 6 |
| §2 | each factory's `register()` keys (ten, with §8's `key_on_version`) | 5 |
| §3 | the factory hooks | 5 |
| §4 | `InventorySpec`, `Parent`, `ParentSet`: the inventory's declarations | 4, 6 |
| §5 | the `version` and `store_tag` tables, and `tag_serial` | 5 |
| §6 | what the layer reads from a stored object | 2, 5 |
| §7 | the registry given to `open_read_only`, `read_inventory` and the schema helpers | 6, 8 |
| §8 | `key_on_version`, `VERSION_SERIAL_KEY`, `require_version_serial` | 3, 5 |

Two facts hold for every client, and each checklist says how they reach it.

**The layer never instantiates a factory** (contract §3). Whatever the registry maps a class name
to, the layer calls its hooks on that object directly, for example `factory.register()` at
`datastorekit/SQL/schema.py:101`. `SQLAFactoryBase` (`datastorekit/SQL/factory_base.py:5-29`) is
an ABC whose `register`, `build`, `store`, `validate` and `validate_on_startup` are abstract.
- A client that registers **classes** (SGK) is unaffected: a class is never instantiated, so its
  abstract methods are never enforced.
- A client that registers **instances** (CPBH, SI) must give each instantiated class all five, or
  Python refuses to instantiate it (`TypeError`) at the line that builds the instance (U32). The
  other route, registering the class itself, works only once the class's hooks can be called
  without an instance. In CPBH and SI every hook of every factory takes `self`, none is a
  `staticmethod`, and the quantity factories hold their `ObjectType` on the instance. Which route
  a client takes is the client's choice; each checklist lists the classes.

**The pool takes table names, not drop groups.** `ShardedPool(drop_tables=[...])` takes the tables
to drop. A name the registry does not declare as a table is refused before anything is opened
(`_refuse_undeclared_drop_tables`, `datastorekit/SQL/ShardedPool.py:716-728`), and so is a drop
that would leave another table naming rows of a dropped one, by foreign key or by a parent an
`inventory_spec` declares, followed transitively (`_refuse_drop_that_leaves_references`,
`datastorekit/SQL/ShardedPool.py:730-749`). `datastorekit.SQL.schema.dependent_tables(dropped,
factories)` names the tables that must go with a drop (contract §7). A client's drop groups, such
as a command line's `--drop` choices, therefore become lists of tables, each closed under
`dependent_tables`, and a drop group that is not closed is refused.

---

## 5. How a checklist is used

- **It is measured at the named client commit.** The client's adoption campaign measures again
  before acting, and its numbers govern. §6's script re-measures the imports at any commit.
- **A client's adoption is one campaign in its own repository**, under its own `CLAUDE.md`. No
  prompt of this repository edits a client, and no prompt of a client edits this repository
  (`CLAUDE.md`, "A client's change is not made here"). A defect the client finds in the package is
  reported here and fixed here, in a release.
- **The pin moves in a commit of its own** (`CLAUDE.md`, "Releases").
- **The gates.** G2 (SGK has adopted `v0.2.0`, U29), G3 (CPBH), G4 (SI) are recorded on this
  campaign's board, [`prompts/extraction/IMPLEMENTATION_STATE.md`](../../prompts/extraction/IMPLEMENTATION_STATE.md)
  §2, as they hold. The campaign closes at 07b and does not wait for them.

Each checklist has the same ten items, in the same order and under the same names, so the three
can be read side by side:

1. The client and its versions
2. What it deletes
3. Which imports it rewrites
4. What leaves the layer, and where it may go
5. What its factories must change
6. Its call sites and pool construction
7. Its tests and fixtures
8. Which of its stores the package refuses, and why
9. Its acceptance
10. What goes stale in it

Every fact carries the client's commit and a `path:line`, or comes from §6's script, whose
Markdown output is each checklist's appendix. A `path:line` with no other commit named is at the
checklist's client commit; one under `datastorekit/` is at `v0.2.0` (`240028e`).

---

## 6. Re-measuring the imports

```bash
./venv/bin/python docs/extraction/measure_client_imports.py sgk  [--commit SHA] [--json]
./venv/bin/python docs/extraction/measure_client_imports.py cpbh [--commit SHA] [--json]
./venv/bin/python docs/extraction/measure_client_imports.py si   [--commit SHA] [--json]
```

It reads the client at `/Users/ds283/Documents/Code/<repository>` through `git ls-tree` and `git
show` only, never its working tree, and parses each tracked `.py` file with `ast`. It reports every
import statement that names a layer module, at module level or nested, with the file, the line, the
enclosing construct, the module and the names; string literals and `import_module` calls that name
one; imports of the client's factory modules, by count; and, for CPBH, imports of the two names
that move into `datastorekit.contract`. Its docstring gives the rules. It exits 0 on success and 2
when it cannot read the client, and two runs at one commit give the same bytes.

At the checklists' commits it gives **SGK 233** import statements, **CPBH 41** and **SI 48**.

---

## Addendum: v0.2.1 (extraction prompt 10, 2026-10-10)

*Written by extraction prompt 10 on 2026-10-10, and added to 07a's text, which stays as written
and true of `v0.2.0` (`CLAUDE.md` rule 6). No client was re-measured (decision U37).*

**The pin.** Every client adopts **`v0.2.1`** in place of `v0.2.0` (decision U37, which amends U29
and G2–G4):

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.1
```

**What changed since `v0.2.0`.** Only `datastorekit/SQL/ShardedPool.py` changed in code. Twelve
other layer files changed in their comments and docstrings only (extraction prompt 09), and seven
are unchanged. Nothing a client supplies changes, no API is added or removed, nothing the layer
writes changes, and no message changes. Three behaviours differ, each described in
[`docs/client-contract.md` §9](../client-contract.md#9-changes-after-v020):

| Behaviour | At `v0.2.0` | At `v0.2.1` | Contract row |
|---|---|---|---|
| A reopen whose primary records a sharded table that `sharded_tables` lacks | a bare `KeyError` | refused with the intended `RuntimeError` "Mismatch between sharded tables supplied to the constructor and read from the existing ShardedPool" (`datastorekit/SQL/ShardedPool.py:1071-1072`, `:1100-1103`) | [§9.1](../client-contract.md#91-prompt-08a), "A reopen whose primary records a sharded table that `sharded_tables` lacks" |
| `object_get_vectorized` and the caller's payloads | the shard key added to each of the caller's dicts, in place | each shard is sent copies, `{**value, **shard_key}` (`datastorekit/SQL/ShardedPool.py:3348`); the caller's list and dicts are left as they were passed | [§9.1](../client-contract.md#91-prompt-08a), "What `object_get_vectorized` does to the caller's payloads" |
| An open that raises | its engines left for the garbage collector | the actors built so far are closed and the pool's engine disposed, then the open's exception is re-raised unchanged (`datastorekit/SQL/ShardedPool.py:203-207`, `:375-408`) | [§9.2](../client-contract.md#92-prompt-08b), "An open that raises" |

**Nothing any client supplies or stores changes.** A store that opened under `v0.2.0` opens under
`v0.2.1`, and a store refused under `v0.2.0` is refused under `v0.2.1`, by the same exception but
for the `KeyError` above.

**What the clients do with the three**, from the records:
- **Payloads.** No client reads a payload list back after a vectorized get (log 08a §3, at the
  checklists' commits). CPBH and SI pass a bare shard key, which the package refuses before the
  payload line in both releases (their checklists, item 6).
- **The `KeyError`. No client's code depends on it.** Extraction prompt 10 measured the three
  clients read-only through `git grep`, at the checklists' commits: `except KeyError` and `except
  (…KeyError…)` outside each client's `Datastore/`, then a `try` within three lines before a
  `ShardedPool(`. CPBH and SI catch `KeyError` nowhere. SGK catches it in two places,
  `RunRegistry/__init__.py:606` (a manifest's `created` field) and
  `RunRegistry/tests/test_run_registry.py:489` (a status file's JSON), neither around a pool. The
  only `try` around a `ShardedPool(` outside SGK's layer is in two of SGK's archived measurement
  scripts under `prompts/datastore-generic/orchestrator/`: one catches `ReadOnlyMiss` only, the
  other any exception, recording its type.
- **The refused open.** A client that retries refused opens no longer holds a file descriptor per
  refused engine until the collector runs.

**The checklists are not re-measured** (U37). Each has an addendum of its own, after its item 10:
[SGK's](secondarygwkit.md#addendum-v021-extraction-prompt-10-2026-10-10),
[CPBH's](champbh.md#addendum-v021-extraction-prompt-10-2026-10-10) and
[SI's](stochasticinstantons.md#addendum-v021-extraction-prompt-10-2026-10-10).

**Line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, read at that tag
(`240028e`). A `datastorekit/` line in an addendum is `v0.2.1`'s, whose `datastorekit/` is the tree
of extraction prompt 09's commit `cad7bc1`.

**What this addendum supersedes**, in this file. Each `path:line` is this file's as committed with
this addendum. In 07a's file (`dd45243`) every line after `:5` is five lines earlier, since the
italic line at the head adds five.

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/README.md:3` | written "against the package at **`v0.2.0`** (`240028e`)" | 07a's measurements stay true of `v0.2.0`; this addendum gives `v0.2.1` |
| `docs/adoption/README.md:13` | each checklist says what its client must do "to depend on `datastorekit` at `v0.2.0`" | at `v0.2.1`: each checklist with its addendum |
| `docs/adoption/README.md:29-31` | "All three adopt **`v0.2.0`**" | all three adopt `v0.2.1` (U37) |
| `docs/adoption/README.md:40` | the pin `…@v0.2.0` | the pin `…@v0.2.1`, above |
| `docs/adoption/README.md:159` | "G2 (SGK has adopted `v0.2.0`, U29)" | G2, G3 and G4 each hold when that client has adopted `v0.2.1` (U37) |
| `docs/adoption/README.md:161` | "The campaign closes at 07b" | it closes at extraction prompt 11 (U33); 07b was withdrawn unwritten |
| `docs/adoption/README.md:178-179` | "one under `datastorekit/` is at `v0.2.0` (`240028e`)" | still so for 07a's text; a `datastorekit/` line in an addendum is at `v0.2.1` |

---

## Addendum: v0.2.2 (actor-names prompt 02, 2026-10-11)

*Written by `actor-names` prompt 02 on 2026-10-11, and added after extraction prompt 10's `v0.2.1`
addendum. 07a's text and the `v0.2.1` addendum stay as written, each true of the release it names
(`CLAUDE.md` rule 6). No checklist was re-measured (as decision U37); the clients' pool
constructions below were read through `git` only.*

**The pin.** Every client adopts **`v0.2.2`** in place of `v0.2.1` (decision U3 of the
`actor-names` campaign, which amends extraction decision U37 and G2–G4):

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.2
```

**What changed since `v0.2.1`.** Only `datastorekit/SQL/ShardedPool.py` changed in the package:
64 lines added and none removed, by `actor-names` prompts 01 and 01b. Nothing a client supplies
changes, no API is added or removed, nothing the layer writes changes, and no message, refusal or
exception of the layer's changes. Four behaviours differ, all from 01, and two are unchanged. Each
is a row of [`docs/client-contract.md` §9.3](../client-contract.md#93-actor-names-prompt-01) or
[§9.4](../client-contract.md#94-actor-names-prompt-01b):

| Behaviour | At `v0.2.1` | At `v0.2.2` | Contract row |
|---|---|---|---|
| A closed pool's actor names | held until the pool object is collected: a reopen in the same Ray session while the closed pool is referenced is refused by Ray | released at once: `__exit__` kills each shard actor and the broker with `ray.kill(handle, no_restart=True)` (`datastorekit/SQL/ShardedPool.py:857-884`; `_kill_actors`, `:430-457`), so the store can be reopened while the closed pool is still referenced | [§9.3](../client-contract.md#93-actor-names-prompt-01), "`ShardedPool.__exit__`" |
| A closed pool's handles | live, with their engines disposed | dead: a call through `pool._shards` or `pool._broker` fails, and so does a pool method that reaches an actor | [§9.3](../client-contract.md#93-actor-names-prompt-01), "`ShardedPool.__exit__`" |
| A second `__exit__` | runs the body again | does nothing (`datastorekit/SQL/ShardedPool.py:867-868`) | [§9.3](../client-contract.md#93-actor-names-prompt-01), "`ShardedPool.__exit__`" |
| An open that is refused | closes the actors it made and disposes its engine (§9.2), and holds their names until it is collected | also kills the actors it made (`datastorekit/SQL/ShardedPool.py:428`), so it releases their names at once, even while its exception is held | [§9.3](../client-contract.md#93-actor-names-prompt-01), "A refused open" |
| *Unchanged:* two pools open at once in one Ray session | collide | still collide, since the names are fixed: the second open is refused by Ray when it creates its broker, with `ValueError` at Ray 2.43.0 and `ray.exceptions.ActorAlreadyExistsError` at 2.55.1 | [§9.3](../client-contract.md#93-actor-names-prompt-01), "Two open pools" |
| *Unchanged:* closing a pool in a process not connected to Ray | kills nothing, since a close calls no `ray.kill`, and so starts no Ray | kills nothing, and starts no Ray: `_kill_actors` returns before any `ray.kill` (`datastorekit/SQL/ShardedPool.py:446-447`) when `_ray_is_running()` (`:47-55`), which returns `ray.is_initialized()`, is false. Ray's `ray.kill` is one of its auto-init calls, and would run `ray.init()` first. This is `actor-names` prompt 01b's guard: a property the release keeps, not a second fix | [§9.4](../client-contract.md#94-actor-names-prompt-01b), "`ShardedPool._kill_actors`, when the process is not connected to Ray" |

**Nothing any client supplies or stores changes.** A store that opened under `v0.2.1` opens under
`v0.2.2`, and a store refused under `v0.2.1` is refused under `v0.2.2`, by the same exception and
message.

**What the clients do with a closed pool.** `actor-names` prompt 02 read the three clients through
`git` only, at the checklists' commits (SGK `b510bc9`, CPBH `52142d7`, SI `7bb3efd`): `git grep -n
-E 'ShardedPool\(|\.__exit__\(|ray\.kill|ray\.get_actor'` over each client's `.py` files outside
its `Datastore/`, `prompts/` and `docs/`, then an `ast` read, from `git show`, of each file that
constructs a pool.
- **Every construction is a `with ShardedPool(…) as pool:` block**, the only construction in its
  file, and nothing after the block names `pool`. There are 14:
  - SGK 7: `main.py:4164`, and `extract_GkSource_data.py:932`, `extract_GkWKB_data.py:505`,
    `extract_Gk_data.py:453`, `extract_QuadSourceIntegral_data.py:1294`, `extract_TkWKB_data.py:493`
    and `extract_tensor_source_data.py:421`;
  - CPBH 3: `main.py:1338`, `plot_ScalarModel.py:1577` and `plot_by_beta.py:1007`;
  - SI 4: `main.py:1345`, `plot_GradientCoupledSolutions.py:974`, `plot_InstantonSolutions.py:1207`
    and `tests/conftest.py:57`.

  13 are the last statement of their block. SI's `live_pool` fixture yields the pool inside its
  block, and calls `ray.shutdown()` after it.
- **No client calls a pool's `__exit__` directly, or `ray.kill` or `ray.get_actor`**, and none reads
  a pool's `_shards` or `_broker`. The five `super().__exit__` calls the grep finds, two each in SGK
  and CPBH and one in SI, are in `Quadrature/` classes, not pools. SGK's grep also matches a
  docstring and a message that name the block (`ComputeTargets/tests/test_reader_read_only.py:91`,
  `:104`); neither is a construction.
- **So no client uses a closed pool**, and none meets a dead handle. Each opens one pool per process
  (SI's fixture one per pytest session), so none met the defect either: for each client the fix is
  latent.

**The checklists are not re-measured** (as U37). Each has an addendum of its own, after its `v0.2.1`
addendum: [SGK's](secondarygwkit.md#addendum-v022-actor-names-prompt-02-2026-10-11),
[CPBH's](champbh.md#addendum-v022-actor-names-prompt-02-2026-10-11) and
[SI's](stochasticinstantons.md#addendum-v022-actor-names-prompt-02-2026-10-11).

**Line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, read at that tag
(`240028e`), and one in the `v0.2.1` addendum stays `v0.2.1`'s (`33778b0`). A `datastorekit/` line
in this addendum is `v0.2.2`'s, whose `datastorekit/` is the tree of `actor-names` prompt 01b's
commit `f024fc6`; prompt 02 does not change it.

**What this addendum supersedes**, in this file. Each `path:line` is this file's as committed with
this addendum. In the file as extraction prompt 10 left it (`33778b0`), every line after `:11` is
five lines earlier, since this addendum's italic line at the head adds five: so the `v0.2.1`
addendum's citations, which are that file's, are read at `33778b0`, or five lines later here (all
but `:3`, which is above the insert).

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/README.md:7-10` | the `v0.2.1` addendum, "at the end", gives the pin **`v0.2.1`** | it gives `v0.2.1`'s pin and changes, true of `v0.2.1`; this addendum, now at the end, gives `v0.2.2` |
| `docs/adoption/README.md:213-214` | "Every client adopts **`v0.2.1`** in place of `v0.2.0`" | every client adopts `v0.2.2` in place of `v0.2.1` (`actor-names` U3); "The pin", above |
| `docs/adoption/README.md:217` | the pin `…@v0.2.1` | the pin `…@v0.2.2`, above |
| `docs/adoption/README.md:257-259` | "A `datastorekit/` line in an addendum is `v0.2.1`'s" | so in the `v0.2.1` addendum; one in this addendum is `v0.2.2`'s ("Line citations", above) |
| `docs/adoption/README.md:261-263` | the `v0.2.1` addendum's `path:line`s are "this file's as committed with this addendum" | they are read at `33778b0`, or five lines later here (all but `:3`) |
| `docs/adoption/README.md:268` | at `v0.2.1`, "each checklist with its addendum" | at `v0.2.2`, each checklist with both its addenda |
| `docs/adoption/README.md:269` | "all three adopt `v0.2.1` (U37)" | all three adopt `v0.2.2` (U37; `actor-names` U3) |
| `docs/adoption/README.md:270` | "the pin `…@v0.2.1`, above" | the pin `…@v0.2.2`, above |
| `docs/adoption/README.md:271` | "G2, G3 and G4 each hold when that client has adopted `v0.2.1` (U37)" | G2, G3 and G4 each hold when that client has adopted `v0.2.2` (U37; `actor-names` U3) |
| `docs/adoption/README.md:273` | "a `datastorekit/` line in an addendum is at `v0.2.1`" | as `:257-259` |

---

## Addendum: v0.2.3 (factory-defaults prompt 02, 2026-10-11)

*Written by `factory-defaults` prompt 02 on 2026-10-11, and added after `actor-names` prompt 02's
`v0.2.2` addendum. 07a's text, the `v0.2.1` addendum and the `v0.2.2` addendum stay as written,
each true of the release it names (`CLAUDE.md` rule 6). No checklist was re-measured (as decision
U37); the clients' factory classes below were read through `git` only.*

**The pins, by client.** For the first time the clients' pins differ (decision U5 of the
`factory-defaults` campaign, which amends extraction decision U37 and `actor-names` decision U3,
"every client adopts the release named", for SGK only):
- **CPBH and SI adopt `v0.2.3`** in place of `v0.2.2`, and G3 and G4 read "CPBH has adopted
  `v0.2.3`" and "SI has adopted `v0.2.3`":

  ```text
  datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.3
  ```

- **SGK may stay on `v0.2.2` or move to `v0.2.3`**, as SGK chooses, a move being a commit of its
  own, and G2 reads "SGK has adopted `v0.2.2` or later". `v0.2.3` changes nothing SGK meets
  (below).

`v0.2.3` carries `key_on_version`, `v0.2.0`'s feature, `v0.2.1`'s three fixes and `v0.2.2`'s fix,
unchanged.

**What changed since `v0.2.2`.** Only `datastorekit/SQL/factory_base.py` changed in the package,
by `factory-defaults` prompt 01 (`f5d8957`), on the user's ruling: three `@abstractmethod` lines
removed, the comment on defaulted hooks moved above the three and reworded, and a docstring added
to each. Every hook's arguments and body are `v0.2.2`'s. Nothing a client supplies changes, no API
is added or removed, nothing the layer writes changes, and no message, refusal or exception of the
layer's changes. What changes is Python's: it no longer refuses to instantiate a factory class
that lacks `store`, `validate` or `validate_on_startup`. Each row below is a row of
[`docs/client-contract.md` §9.5](../client-contract.md#95-factory-defaults-prompt-01):

| What | At `v0.2.2` | At `v0.2.3` | Contract row |
|---|---|---|---|
| A factory class that defines `register` and `build` but not all of `store`, `validate` and `validate_on_startup` | `SQLAFactoryBase` makes all five abstract, so Python refuses to instantiate the class, with `TypeError`, at the line that makes the instance | it can be instantiated, and its instance registered. The base (`datastorekit/SQL/factory_base.py:5-80`) has `register` (`:6-9`) and `build` (`:11-14`) as its only abstract hooks, and defaults the three (`:21-50`), static, as it defaults `revalidate`, `owned_serials` and `inventory_spec` | [§9.5](../client-contract.md#95-factory-defaults-prompt-01), "A factory may be an instance" |
| A hook that a registered instance's class does not define | — (no such instance could be made) | what a class meets: the base's bare `NotImplementedError`, reached only when the layer calls the hook (a store of the class, a validate of it, or, for a class whose `register()` declares `validate_on_startup: True`, an actor's open or a replicated prune), from a class or an instance alike | [§9.5](../client-contract.md#95-factory-defaults-prompt-01), "`store`, `validate`, `validate_on_startup`" |
| *Unchanged:* a factory class lacking `register` or `build` | refused at instantiation, `TypeError` | still refused at instantiation, `TypeError` | [§9.5](../client-contract.md#95-factory-defaults-prompt-01), "A factory may be an instance" |
| *Unchanged:* a client that registers factory classes | the layer calls each hook on the class, and never instantiates a factory | the same: such a client meets nothing new, `NotImplementedError` included | [§9.5](../client-contract.md#95-factory-defaults-prompt-01), its preamble |
| *Now stated:* what a pool's actors receive | the same, but unstated | the registry reaches each actor as a constructor argument, serialised under Ray, so a registered instance must be of a class defined at module level, with picklable attributes | [§9.5](../client-contract.md#95-factory-defaults-prompt-01), "What a pool's actors receive" |

**Nothing any client supplies or stores changes.** A store that opened under `v0.2.2` opens under
`v0.2.3`, and a store refused under `v0.2.2` is refused under `v0.2.3`, by the same exception and
message.

**What the clients do with it.** `factory-defaults` read the three clients through `git` only: a
script parsed every `.py` file, from `git show <commit>:<path>`, with `ast`, importing and running
nothing of a client, and found each class whose bases name `SQLAFactoryBase`, the methods it
defines, and every call of such a class by name. The planner measured it, and prompt 02 re-ran it,
on 2026-10-11:

| Client, commit | Factory classes | Lacking `store`, `validate` or `validate_on_startup` | Lacking `register` or `build` | Calls that instantiate one | Of a class lacking one of the three |
|---|---|---|---|---|---|
| SGK `b510bc9` (its checklist's) | 38 | 31 | none | 0 | 0 |
| SGK `643c3b2`, then `af26914` (its `HEAD` when read, 2026-10-11) | 38 | 31 | none | 0 | 0 |
| CPBH `52142d7` | 23 | 20 | none | 27, all in its registry (`Datastore/SQL/Datastore.py:95-121`) | 24 |
| SI `7bb3efd` | 28 | 16 | none | 33: 30 in its registry (`Datastore/SQL/Datastore.py:97-126`), and three at import (`CosmologyConcepts/Potentials/registry.py:33`, `:40`; `Datastore/SQL/ObjectFactories/MasslessDecoupledDiffusion.py:71`) | 21: 18 registry entries and the three at import |

- **CPBH**: under `v0.2.2` each of the 24 calls raises `TypeError` where the registry is built.
  Under `v0.2.3` each instantiates, since every CPBH class defines `register` and `build`. CPBH's
  registry of instances works as it stands.
- **SI**: the same for its 18 registry entries, and its three instantiations at import stop
  raising too.
- **SGK** instantiates no factory, at its checklist's commit or at its `HEAD`: it registers classes.
  `v0.2.3` changes nothing SGK meets.

**The checklists are not re-measured** (as U37). Each has an addendum of its own, after its `v0.2.2`
addendum: [SGK's](secondarygwkit.md#addendum-v023-factory-defaults-prompt-02-2026-10-11),
[CPBH's](champbh.md#addendum-v023-factory-defaults-prompt-02-2026-10-11) and
[SI's](stochasticinstantons.md#addendum-v023-factory-defaults-prompt-02-2026-10-11).

**Line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, read at that tag
(`240028e`), one in the `v0.2.1` addendum stays `v0.2.1`'s (`33778b0`), and one in the `v0.2.2`
addendum stays `v0.2.2`'s (`6d8ee9a`). A `datastorekit/` line in this addendum is `v0.2.3`'s, whose
`datastorekit/` is the tree of `factory-defaults` prompt 01's commit `f5d8957`; prompt 02 does not
change it. A client's line is that client's at the commit named.

**What this addendum supersedes**, in this file. Each `path:line` is this file's as committed with
this addendum. In the file as `actor-names` prompt 02 left it (`6d8ee9a`), every line after `:16`
is five lines earlier, since this addendum's italic line at the head adds five. So the `v0.2.2`
addendum's citations, which are that file's, are read at `6d8ee9a`, or five lines later here (all
but `:7-10`, which is above the insert). The `v0.2.1` addendum's citations, which the `v0.2.2`
addendum reads at `33778b0` or five lines later, are read at `33778b0`, or ten lines later here
(all but `:3`).

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/README.md:12-15` | the `v0.2.2` addendum, "at the end", gives the pin **`v0.2.2`** | it gives `v0.2.2`'s pin and changes, true of `v0.2.2`; this addendum, now at the end, gives the pins of `v0.2.3` |
| `docs/adoption/README.md:137-138` | "`SQLAFactoryBase` (`datastorekit/SQL/factory_base.py:5-29`) is an ABC whose `register`, `build`, `store`, `validate` and `validate_on_startup` are abstract" | true through `v0.2.2`. At `v0.2.3` only `register` and `build` are abstract, and the base defaults the other three; "What changed since `v0.2.2`", above |
| `docs/adoption/README.md:141-146` | a client that registers instances "must give each instantiated class all five, or Python refuses to instantiate it (`TypeError`) … (U32)", and "the other route", registering the class itself | at `v0.2.3` an instantiated class needs only `register` and `build`, which every CPBH and SI class defines, so a registry of instances works as it stands and neither route is needed. The paragraph's first sentence, that the layer never instantiates a factory and calls its hooks on what the registry holds (`:135-137`), and its first bullet, that a client that registers classes is unaffected (`:139-140`), still hold |
| `docs/adoption/README.md:289-290` | "Every client adopts **`v0.2.2`** in place of `v0.2.1`" | CPBH and SI adopt `v0.2.3`, and SGK may stay on `v0.2.2` or move (`factory-defaults` U5); "The pins, by client", above |
| `docs/adoption/README.md:293` | the pin `…@v0.2.2` | for CPBH and SI the pin `…@v0.2.3`; for SGK `…@v0.2.2` or `…@v0.2.3` |
| `docs/adoption/README.md:351-355` | the `v0.2.2` addendum's `path:line`s are "this file's as committed with this addendum" | they are read at `6d8ee9a`, or five lines later here (all but `:7-10`) |
| `docs/adoption/README.md:360` | "every client adopts `v0.2.2` in place of `v0.2.1`" | as `:289-290` |
| `docs/adoption/README.md:361` | "the pin `…@v0.2.2`, above" | as `:293` |
| `docs/adoption/README.md:364` | at `v0.2.2`, "each checklist with both its addenda" | at `v0.2.3`, each checklist with its three addenda |
| `docs/adoption/README.md:365` | "all three adopt `v0.2.2` (U37; `actor-names` U3)" | as `:289-290` |
| `docs/adoption/README.md:366` | "the pin `…@v0.2.2`, above" | as `:293` |
| `docs/adoption/README.md:367` | "G2, G3 and G4 each hold when that client has adopted `v0.2.2` (U37; `actor-names` U3)" | G2 holds when SGK has adopted `v0.2.2` or later, and G3 and G4 when CPBH and SI have adopted `v0.2.3` (U37; `actor-names` U3; `factory-defaults` U5) |

---

## Addendum: v0.3.0 (object-timestamp prompt 02, 2026-10-12)

*Written by `object-timestamp` prompt 02 on 2026-10-12, and added after `factory-defaults` prompt
02's `v0.2.3` addendum. 07a's text and the `v0.2.1`, `v0.2.2` and `v0.2.3` addenda stay as written,
each true of the release it names (`CLAUDE.md` rule 6). No checklist was re-measured (as decision
U37); the clients' stored objects below were read through `git` only.*

**The pins, by client.** The clients' pins differ three ways (decision U6 of the `object-timestamp`
campaign, which amends `factory-defaults` decision U5 for CPBH and SI, and keeps it for SGK):
- **SI adopts `v0.3.0`** in place of `v0.2.3`, when it is next active, and G4 reads "SI has adopted
  `v0.3.0`":

  ```text
  datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.3.0
  ```

- **CPBH may stay on `v0.2.3` or move to `v0.3.0`**, as CPBH chooses, and G3 reads "CPBH has
  adopted `v0.2.3` or later".
- **SGK may stay on `v0.2.2` or move to `v0.2.3` or `v0.3.0`**, as SGK chooses, and G2 reads, as
  before, "SGK has adopted `v0.2.2` or later". G2 holds (2026-10-12, the extraction board).

A move is a commit of the client's own. Neither CPBH nor SGK reads the value back, and nothing they
call changes (below).

`v0.3.0` carries `key_on_version`, `v0.2.0`'s feature, `v0.2.1`'s three fixes, `v0.2.2`'s fix and
`v0.2.3`'s change, unchanged.

**What changed since `v0.2.3`.** Only `datastorekit/object.py` changed in the package, by
`object-timestamp` prompt 01 (`1b2f91a`), on the user's ruling: 18 lines added and 1 removed.
`store_id` and `available` are `v0.2.3`'s. The release adds API, a constructor argument and a
property of a public class, so it is minor (U6). Nothing a client supplies changes, nothing the
layer writes or reads changes, and no message, refusal or exception of the layer's changes. The
detail is the one row of
[`docs/client-contract.md` §9.6](../client-contract.md#96-object-timestamp-prompt-01),
"`DatastoreObject.timestamp`":

| What | At `v0.2.3` | At `v0.3.0` |
|---|---|---|
| `DatastoreObject(store_id, timestamp=t)` | `TypeError`: an unexpected keyword argument | accepted: `timestamp` is keyword-only, `None` by default, and kept as `self._timestamp` (`datastorekit/object.py:10-14`) |
| `obj.timestamp` | `AttributeError`: the base has no such attribute | what the object was given, or `None`: a read-only property (`datastorekit/object.py:27-38`), with no setter and no deleter |
| Who fills it | — | a factory, from the row it read: one that reads a row of a class whose `register()` declares `"timestamp": True` may pass the row's `timestamp`. **The layer never sets it and never reads it.** It is `None` for an object not yet stored, one built from an insert, one whose factory does not pass it, and one whose table has no such column |
| *Now met:* `vars()` of a stored object | `_my_id`, and the subclass's own attributes | one more key, `_timestamp`, `None` unless given |
| *Now met:* a subclass that assigns or deletes `self.timestamp` | sets or deletes an attribute of its own | `AttributeError`: the property has no setter or deleter |
| *Unchanged:* a second positional argument | `TypeError` | `TypeError`, with the same message |

**Nothing any client supplies or stores changes.** A store that opened under `v0.2.3` opens under
`v0.3.0`, and a store refused under `v0.2.3` is refused under `v0.3.0`, by the same exception and
message. An object pickled under an earlier release and unpickled under `v0.3.0` would have no
`_timestamp`, and reading its `timestamp` would raise `AttributeError`; no client writes a pickled
`DatastoreObject` to disk (below).

**What the clients do with it.** `object-timestamp` read the three clients through `git` only: a
script parsed every `.py` file outside each client's `prompts/`, `.prompts/`, `docs/` and
`.documents/`, from `git show <commit>:<path>`, with `ast`, importing and running nothing of a
client, and found where `DatastoreObject` comes from, the classes descending from it by name, every
`DatastoreObject.__init__(…)` call by its arguments, and every `timestamp` defined or assigned on a
class. The planner measured it, and prompt 02 re-ran it, on 2026-10-12:

| Client, commit | `DatastoreObject` from | Descendants | `DatastoreObject.__init__` calls: `store_id` alone / with `timestamp=` / other | `timestamp` defined or assigned on a descendant |
|---|---|---|---|---|
| SGK `d03a643`, and `e3a7077`, then `cf978c6` (its `HEAD` when read) | the package (`from datastorekit import DatastoreObject`, 19 imports) | 30 | 38 / 0 / 0 | none; no `timestamp` on any class |
| CPBH `64ef9aa`, and `cb0c675`, then `0f1c25b` (its `HEAD` when read) | its own (`Datastore/object.py:19`), which takes `store_id` alone | 31 | 19 / 0 / 0 | none; no `timestamp` on any class |
| SI `7bb3efd` | its own (`Datastore/object.py:20`), whose `__init__` takes `timestamp` positional-or-keyword (`:25-30`) and whose `timestamp` is a read-only property (`:43-45`) | 34 | 9 / 14 / 0; and ten calls in deeper descendants pass `timestamp=` through, by keyword | none. Its own `DatastoreObject` defines one (`:30`, `:44`) and leaves with its layer; the other 17 sites (`def timestamp` on four plot adapters and one test stand-in, and `self.timestamp = …` in twelve test stand-ins) are on classes that do not descend from it |

- **SI**: its 14 direct calls and its ten pass-throughs (its checklist, item 2) pass `timestamp=` by
  keyword, so each works under `v0.3.0` as it stands once its import is rewritten. Its reads of
  `.timestamp` get what its factories pass, as today: 18 of its factory modules pass `timestamp=`,
  and the layer fills nothing. Its plot adapters and test stand-ins are not `DatastoreObject`s, and
  are unaffected. `v0.3.0` removes the obligation of its checklist's item 2 paragraph on
  `DatastoreObject.timestamp`, and `DatastoreObject.timestamp` no longer leaves the layer (item 4).
- **CPBH and SGK** pass `store_id` alone, and define or assign no `timestamp` on a descendant.
  `v0.3.0` changes nothing they meet but one key in `vars()`, which neither reads: CPBH's one
  `vars(` is of a module (`Datastore/tests/test_compare_stores.py:735`), and SGK's two `__dict__`s
  are of classes.
- **No client writes a pickled `DatastoreObject` to disk.** A `git grep` of `pickle`, `joblib`,
  `shelve` and `dill` dumps finds in-memory round trips, commented-out lines, and SI's one
  `joblib.dump` (`regression_InstantonOutputs.py:370`), of regression models.
- **The pins, as read:** SGK's `requirements.txt:17` pins `v0.2.2` at `e3a7077` and `cf978c6`;
  CPBH has no `datastorekit` line at `0f1c25b`, and SI none at `7bb3efd`.

**The checklists are not re-measured** (as U37). Each has an addendum of its own, after its `v0.2.3`
addendum: [SGK's](secondarygwkit.md#addendum-v030-object-timestamp-prompt-02-2026-10-12),
[CPBH's](champbh.md#addendum-v030-object-timestamp-prompt-02-2026-10-12) and
[SI's](stochasticinstantons.md#addendum-v030-object-timestamp-prompt-02-2026-10-12).

**Line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, read at that tag
(`240028e`), one in the `v0.2.1` addendum stays `v0.2.1`'s (`33778b0`), one in the `v0.2.2`
addendum `v0.2.2`'s (`6d8ee9a`), and one in the `v0.2.3` addendum `v0.2.3`'s (`0de2b16`). A
`datastorekit/` line in this addendum is `v0.3.0`'s, whose `datastorekit/` is the tree of
`object-timestamp` prompt 01's commit `1b2f91a`; prompt 02 does not change it. A client's line is
that client's at the commit named.

**What this addendum supersedes**, in this file. Each `path:line` below is this file's as committed
with this addendum. In the file as `factory-defaults` prompt 02 left it (`0de2b16`), every line after
`:21` is five lines earlier, since this addendum's italic line at the head adds five (N = 5). So:
- the `v0.2.3` addendum's citations, which are that file's, are read at `0de2b16`, or **5** lines
  later here (all but `:12-15`, which is above the insert);
- the `v0.2.2` addendum's, which the `v0.2.3` addendum reads at `6d8ee9a` or five lines later, are
  read at `6d8ee9a`, or **10** lines later here (all but `:7-10`);
- the `v0.2.1` addendum's, which the `v0.2.3` addendum reads at `33778b0` or ten lines later, are
  read at `33778b0`, or **15** lines later here (all but `:3`).

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/README.md:17-20` | the `v0.2.3` addendum, "at the end", gives "the pins by client" | it gives `v0.2.3`'s pins and changes, true of `v0.2.3`; this addendum, now at the end, gives the pins of `v0.3.0` |
| `docs/adoption/README.md:387-396` | "CPBH and SI adopt `v0.2.3`", G3 and G4 reading "CPBH has adopted `v0.2.3`" and "SI has adopted `v0.2.3`", the pin `…@v0.2.3`; and SGK "may stay on `v0.2.2` or move to `v0.2.3`" | SI adopts `v0.3.0`, and G4 reads "SI has adopted `v0.3.0`"; CPBH may stay on `v0.2.3` or move to `v0.3.0`, and G3 reads "CPBH has adopted `v0.2.3` or later"; SGK may stay on `v0.2.2` or move to `v0.2.3` or `v0.3.0`, and G2's reading is unchanged (`object-timestamp` U6); "The pins, by client", above |
| `docs/adoption/README.md:398-399` | "`v0.2.3` carries `key_on_version`, `v0.2.0`'s feature, `v0.2.1`'s three fixes and `v0.2.2`'s fix, unchanged" | true of `v0.2.3`; `v0.3.0` carries those and `v0.2.3`'s change, unchanged |
| `docs/adoption/README.md:454-460` | the `v0.2.3` addendum's `path:line`s are "this file's as committed with this addendum", and the earlier addenda's are read five and ten lines later | they are read at `0de2b16`, or five lines later here; the `v0.2.2` addendum's ten, and the `v0.2.1` addendum's fifteen; above |
| `docs/adoption/README.md:467` | the row for `:289-290`: "CPBH and SI adopt `v0.2.3`, and SGK may stay on `v0.2.2` or move (`factory-defaults` U5)" | as `:387-396` |
| `docs/adoption/README.md:468` | the row for `:293`: "for CPBH and SI the pin `…@v0.2.3`; for SGK `…@v0.2.2` or `…@v0.2.3`" | for SI the pin `…@v0.3.0`; for CPBH `…@v0.2.3` or `…@v0.3.0`; for SGK `…@v0.2.2`, `…@v0.2.3` or `…@v0.3.0` |
| `docs/adoption/README.md:469` | the row for `:351-355`: the `v0.2.2` addendum's citations "are read at `6d8ee9a`, or five lines later here" | at `6d8ee9a`, or ten lines later here (all but `:7-10`) |
| `docs/adoption/README.md:470-471` | the rows for `:360` and `:361`, "as `:289-290`" and "as `:293`" | as `:467` and `:468` |
| `docs/adoption/README.md:472` | the row for `:364`: "at `v0.2.3`, each checklist with its three addenda" | at `v0.3.0`, each checklist with its four addenda |
| `docs/adoption/README.md:473-474` | the rows for `:365` and `:366`, "as `:289-290`" and "as `:293`" | as `:467` and `:468` |
| `docs/adoption/README.md:475` | the row for `:367`: "G2 holds when SGK has adopted `v0.2.2` or later, and G3 and G4 when CPBH and SI have adopted `v0.2.3` (U37; `actor-names` U3; `factory-defaults` U5)" | G2 holds when SGK has adopted `v0.2.2` or later, as before; G3 when CPBH has adopted `v0.2.3` or later, and G4 when SI has adopted `v0.3.0` (U37; `actor-names` U3; `factory-defaults` U5; `object-timestamp` U6) |

**Not superseded:** §2's module-map row for `DatastoreObject` (`:86`), "`Datastore` (the package
root: `DatastoreObject`)" → `datastorekit`, maps a module, which `v0.3.0` does not move; it stays
true.
