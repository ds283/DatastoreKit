# DatastoreKit

A sharded SQLite datastore driven by [Ray](https://www.ray.io/) actors. A client project declares
its tables through object factories; DatastoreKit holds the rows across one primary file and a
set of shard files, replicates the small lookup tables to every shard, routes the large tables to
one shard by a shard key, and checks the store's integrity each time it is opened.

## Status

**`v0.2.0`** adds **version-keyed lookups**: a class whose factory declares the optional
`register()` key `key_on_version` is looked up under the pool's version label only, so a row made
under another label is a miss. A class that does not declare it behaves as in `v0.1.0`, and
nothing the layer writes changes.

**`v0.1.0`** is the `Datastore` / `ShardedPool` layer of
[SecondaryGWKit](https://github.com/ds283/SecondaryGWKit) at its commit `6f7f291`, moved here with
its behaviour unchanged ([`PROVENANCE.md`](PROVENANCE.md) gives the file map and the only
differences allowed, and where `v0.2.0`'s feature comes from). Its tests were ported with it, onto
a neutral test client, so that the suite needs no client project.

The plan for the package, and for its three client projects to depend on one copy of the layer, is
[`prompts/extraction/README.md`](prompts/extraction/README.md); its status board is
[`prompts/extraction/IMPLEMENTATION_STATE.md`](prompts/extraction/IMPLEMENTATION_STATE.md).

`RayWorkPool` is not part of this package (yet): reconciling it across the three projects is a
separate unit of work.

## Supported versions

| | Declared (`pyproject.toml`) | Tested: low end | Tested: high end |
|---|---|---|---|
| Python | `>=3.12` | 3.12.15 | 3.13.16 |
| Ray | `>=2.43` | 2.43.0 | 2.55.1 |
| SQLAlchemy | `>=2.0.39,<2.1` | 2.0.39 | 2.0.46 |

- The suite runs at both tested ends, in CI on Ubuntu 24.04
  ([`.github/workflows/tests.yml`](.github/workflows/tests.yml)), and on macOS where it is
  developed.
- On Python 3.13 the Ray floor is in effect **2.45.0**, the first Ray release with wheels for
  3.13 (2.43.0, 2.44.0 and 2.44.1 have none).
- Ray has no ceiling, so that a client can move Ray without a release here. Newer releases of Ray,
  and of SQLAlchemy in its 2.0 series, are allowed but not tested. SQLAlchemy 2.1 is excluded.
- **A client pins its own Ray and SQLAlchemy**, in its own `requirements.txt`.

## Installing

A client depends on a tagged release, pinned in its `requirements.txt`:

```text
datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.0
```

`v0.1.0` remains, for a client that has not adopted `key_on_version`.

An editable install (`pip install -e`) is for developing this package, never for a client's
production runs: a production run must be reproducible from its pin.

## Using it

A client gives the layer a fixed set of facts. [`docs/client-contract.md`](docs/client-contract.md)
states each one: where the client gives it, whether it is required, optional or defaulted, what
the layer does with it, and what happens when it is wrong or absent.

- **The pool's constructor arguments**: `ShardedPool` (`datastorekit.SQL.ShardedPool`), its
  version label, primary file, shard-key class and getter, and its replicated and sharded classes
  ([§1](docs/client-contract.md#1-the-pools-constructor)).
- **A registry of factories**, class name → factory, given to the pool as `factories=` and to the
  reader and the inventory (§1, row 15; [§7](docs/client-contract.md#7-the-other-entry-points-that-take-client-facts)).
- **Each factory's `register()`**, the dict of keys that describes its table, or `None` for a
  class with no table ([§2](docs/client-contract.md#2-the-keys-of-register)).
- **Each factory's hooks**: `build`, `store`, `validate` and `validate_on_startup`, and the
  defaulted `revalidate`, `owned_serials` and `inventory_spec`, from `SQLAFactoryBase`
  (`datastorekit.SQL.factory_base`) ([§3](docs/client-contract.md#3-the-factory-hooks)).
- **The inventory declarations**: an `InventorySpec` per class, with its `Parent`s and
  `ParentSet`s (`datastorekit.store_inventory`) ([§4](docs/client-contract.md#4-the-inventorys-declarations)).
- **The two tables the layer owns**: `version` and `store_tag`, named in `datastorekit.contract`,
  each registered by the client under that name ([§5](docs/client-contract.md#5-the-layers-own-tables)).
- **Version-keyed lookups**, optional: a factory whose `register()` declares
  `"key_on_version": True` (with `"version": True`) is handed the version serial in every
  `object_get` payload, under `datastorekit.contract.VERSION_SERIAL_KEY`, and its `build` filters
  on it through `datastorekit.contract.require_version_serial`
  ([§8](docs/client-contract.md#8-version-keyed-lookups-v020-prompt-06)).

The worked example is the neutral test client, [`datastorekit/tests/client/`](datastorekit/tests/client/).
Its registry module, [`datastorekit/tests/client/registry.py`](datastorekit/tests/client/registry.py),
holds what a pool is given, and lists the role each class plays. The test client lives in this
repository only; it is not part of the installed package.

## The tools

- `python -m datastorekit.tools.sharded_store {copy,move} SRC DST`: copy or move a closed
  `ShardedPool` datastore under a new name.
- `python -m datastorekit.tools.shard_key_audit /path/to/primary.sqlite`: a read-only consistency
  check of a `ShardedPool` datastore's `shard_keys` table.

## Developing

From the repository root, with Python 3.12 or later:

```bash
python3 -m venv venv
./venv/bin/pip install -e . "ray==2.43.0" "sqlalchemy==2.0.39" "black==25.1.0"
./venv/bin/python -m unittest discover -s datastorekit/tests -t .
```

The suite needs no Ray cluster and opens stores only in temporary directories. Its tools' tests
run the package in a child interpreter, so the package must be installed (editable) in the venv
that runs them. CI runs the suite at both tested ends, and `black --check datastorekit docs`.

The two checks under [`docs/extraction/`](docs/extraction/), `compare_with_source.py` and
`compare_ported_tests.py`, compare the package with its source repository, and
`measure_client_vocabulary.py` beside them reads the client projects. They read those
repositories through `git`, at the local paths they name, so they run locally only, not in CI.
`compare_with_source.py` describes the package as tagged `v0.1.0`, and is run on that tag only
(for example from a `git worktree` of it); it is retired for later trees.

## Licence

Apache License 2.0; see [`LICENSE`](LICENSE).
