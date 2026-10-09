# Adopting `datastorekit`

*Written by extraction prompt 07a on 2026-10-09, against the package at **`v0.2.0`** (`240028e`).
The three clients were read through `git` only, at the commits named below; nothing of a client
was imported, run or opened, and no store was opened.*

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
