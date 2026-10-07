# Provenance

`datastorekit` was imported from **SecondaryGWKit** (SGK):

- **Repository:** <https://github.com/ds283/SecondaryGWKit>, checked out at
  `/Users/ds283/Documents/Code/SecondaryGWKit`.
- **Import commit:** `6f7f291` (`6f7f291e857265e429f5d6f810124fd3bf57ce55`), 2026-10-07,
  "Record the orchestrator's review of datastore-generic-followup prompt 03". It closed SGK's
  `datastore-generic-followup` campaign (gate G1 of `prompts/extraction/README.md` §7).

This is a fresh import (decision U2): SGK's history is not carried here. How the layer came to be
is SGK's history, reachable through the import commit. The import was made by
`prompts/extraction/01-import-the-layer.md`.

## The file map

| SGK at `6f7f291` | Here |
|---|---|
| `Datastore/__init__.py`, `object.py`, `contract.py`, `replication.py`, `shard_paths.py`, `store_reader.py`, `store_inventory.py` | `datastorekit/<same>` |
| `Datastore/SQL/__init__.py`, `schema.py`, `ShardedPool.py`, `Datastore.py`, `ClientPool.py`, `SerialPoolBroker.py`, `ProfileAgent.py` | `datastorekit/SQL/<same>` |
| `Datastore/SQL/ObjectFactories/base.py` | `datastorekit/SQL/factory_base.py` |
| `tools/__init__.py` (empty) | `datastorekit/tools/__init__.py` (empty) |
| `tools/sharded_store.py`, `tools/shard_key_audit.py` | `datastorekit/tools/<same>`, run as `python -m datastorekit.tools.<name>` |
| `config/defaults.py`'s `DEFAULT_STRING_LENGTH` | `datastorekit/defaults.py` (that one constant, nothing else) |
| `utilities.py`'s `WallclockTimer`, `format_time` and `SECONDS_PER_*` | `datastorekit/_timing.py` (those, and the imports they use: `time` and `traceback.print_tb`) |
| `Datastore/tests/__init__.py` (empty) | `datastorekit/tests/__init__.py` (empty) |
| `Datastore/tests/shard_store_fixtures.py` and `test_shard_paths`, `test_shard_file_name`, `test_shardedpool_shard_paths`, `test_copy_move_store`, `test_delete_store`, `test_sharded_store_script`, `test_shard_key_audit_copy`, `test_shard_key_audit_refusals` | `datastorekit/tests/<same>` |

SGK's `Datastore/SQL/ObjectFactories/__init__.py` (empty) has no counterpart: `base.py` is the only
module taken from that package, and it moved up to `datastorekit/SQL/factory_base.py`.

`datastorekit/tests/test_package_imports.py` is new here, and has no source.

## The differences allowed

Every package file above equals its SGK source at `6f7f291` except for these classes of
difference (prompt 01 §2.4). Nothing else differs.

- **D-imp, the import rewrite.** In every `import` and `from … import` statement, inside functions
  too, the module path is mapped: `Datastore.SQL.ObjectFactories.base` → `datastorekit.SQL.factory_base`;
  `Datastore.<x>` → `datastorekit.<x>`; `config.defaults` → `datastorekit.defaults`;
  `utilities` → `datastorekit._timing`. Relative imports are unchanged.
- **D-str, module paths in strings.** A string that names a module by its dotted path is mapped the
  same way (a `mock.patch` target, an import run in a child interpreter, the module names the
  "heavy modules" probes look for). The class name `Datastore` is not a module path, and prose that
  refers to SGK's layout is not rewritten.
- **D-tool, how the tools are run.** The tools' `_REPO_ROOT` / `sys.path` bootstrap is removed, and
  their usage and `prog` lines name `python -m datastorekit.tools.<name>`. The three test modules
  that run a tool run it with `-m` (and `runpy.run_module`) instead of by its file path. What each
  test asserts is unchanged.
- **D-root, the package's root in a test.** `test_shard_file_name` scans the package's directory
  (`Path(datastorekit.__file__).parent`, `tests` excluded) for the shard naming rule, and expects
  it at `datastorekit/shard_paths.py`.
- **D-int, the internalised definitions.** `defaults.py` and `_timing.py` hold SGK's definitions
  byte for byte, under a module docstring naming their source.
- **D-fmt, formatting.** `black` 25.1.0, with no configuration.

## Re-running the check

From the repository root, in the venv (which must have `black==25.1.0`):

```bash
./venv/bin/python docs/extraction/compare_with_source.py          # counts per file and class
./venv/bin/python docs/extraction/compare_with_source.py --show   # and every classified line
```

It reads each source file with `git -C /Users/ds283/Documents/Code/SecondaryGWKit show
6f7f291:<path>`, applies each class of difference as a rule to the source, and compares the result
with the package file. It exits 0 only when every differing line is accounted for by a class and
every file exists on both sides. The rules are described in the script's docstring.

## The freeze (decision U3)

From `6f7f291` until SGK has adopted the package (gate G2), SGK's copies of the files above do not
change. A defect found in them in that time is recorded on SGK's board and fixed here after G2. The
freeze is in force from SGK `b510bc9` (a section of SGK's `CLAUDE.md` naming the frozen files).
