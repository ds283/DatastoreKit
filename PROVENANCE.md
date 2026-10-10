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

## After `v0.1.0`

`v0.1.0` (tag on `68db557`) is the last tree the sections above describe: through it, every
package file equals its SGK source at `6f7f291` up to the differences listed. From prompt 06 on,
the package changes in its own right, and each change is recorded here.

**`docs/extraction/compare_with_source.py` describes the tree at `v0.1.0`, and is retired there**
(decision U27, `prompts/extraction/README.md` §6.2). It was run for the last time by prompt 06,
before its change. To run it again, run it on that tag (for example from a `git worktree` of
`v0.1.0`); on a later tree it fails by design. `compare_ported_tests.py` still runs.

### Prompt 06: version-keyed lookups (`v0.2.0`)

The optional `register()` key `key_on_version` comes from **ChamPBH** (CPBH),
<https://github.com/ds283/ChamPBH>, checked out at `/Users/ds283/Documents/Code/ChamPBH`, at
`52142d7` (`52142d75aebe00855804e2daff4f63aee50ffc3e`, 2026-10-07), read through `git show` only.
The three files below are unchanged in CPBH from `9b3db51`, the commit the campaign's plan cites,
to `52142d7`. What was carried over, and how:

| CPBH at `52142d7` | Here |
|---|---|
| `Datastore/SQL/Datastore.py:328-338`: the key, read in the schema build, refused without a `version` column (`RuntimeError`) | `datastorekit/SQL/schema.py`: `_declared_key_on_version`, in `build_schema`, refusing with the package's `ValueError`, and refusing a value that is not a `bool` |
| `:390`: `False` in the record of a class with no table | not carried over: that record is unchanged, and a reader uses `.get` |
| `:500-509`: the keyed copy of each payload in `object_get` | `datastorekit/SQL/Datastore.py`: `object_get`, with `_keyed_payloads` |
| `:544-555`: `_with_version_serial`, refusing a caller's key with `KeyError` | `_keyed_payloads`, keyed on the actor's lookup serial, and refusing a lookup before that serial is set |
| `config/version.py:52-71`: `VERSION_SERIAL_KEY` and `require_version_serial` | `datastorekit/contract.py`, the same key `"_version_serial"`, so a CPBH factory moves by its import alone |
| `Datastore/tests/test_version_keyed_lookups.py` (470 lines: ten tests in `TestVersionKeyedLookups`, one in `TestOneVersionLabel`) | `datastorekit/tests/test_version_keyed_lookups.py`: 14 tests on the neutral client's `Tessera`; tests (a), (c3), (d), (d2), (d3), (d4) and (e) are carried over by their semantics, (b), (c1), (c2) and (f) are not (log 06 §1.4) |

What is new here, with no CPBH source: the actor's lookup serial apart from its insert serial, and
`Datastore.set_lookup_version`, which a read-only pool calls (U26), since CPBH has no read-only pool
and SGK's actor receives its serial late, through `set_version`.

The files prompt 06 changes: `datastorekit/contract.py`, `datastorekit/SQL/schema.py`,
`datastorekit/SQL/Datastore.py` and `datastorekit/SQL/ShardedPool.py`; in the test client,
`datastorekit/tests/client/factories.py` (`Tessera_factory`) and `registry.py` (its roles table);
`datastorekit/tests/test_neutral_client.py` (`REGISTER_KEYS`) and `test_schema_builder.py`
(`WITNESS`); and the new `datastorekit/tests/test_version_keyed_lookups.py` and witness
`datastorekit/tests/data/schema_at_extraction-06.json`. The log is
`prompts/extraction/logs/06-version-keyed-lookups.md`.

### Prompts 08a, 08b and 09: fixes and prose (`v0.2.1`)

**The three fixes have no source.** They were made here, each closing an issue of this repository's
board, `prompts/extraction/IMPLEMENTATION_STATE.md` §4:

| Issue | Prompt, commit | What the layer now does | Test module |
|---|---|---|---|
| `[02-an-unsupplied-sharded-table-raises-keyerror]` | 08a, `f938844` | a reopen whose primary records a sharded table that `sharded_tables` lacks is refused with the intended `RuntimeError`, not a bare `KeyError` | `datastorekit/tests/test_unsupplied_sharded_table.py` |
| `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]` | 08a, `f938844` | `object_get_vectorized` sends each shard copies of the caller's payloads, and leaves the caller's dicts as they were passed | `datastorekit/tests/test_vectorized_get_payloads.py` |
| `[05-a-refused-open-leaves-its-engines-undisposed]` | 08b, `efedc8d` | an open that raises closes the actors it built and disposes the pool's engine, then re-raises its exception unchanged | `datastorekit/tests/test_refused_open_closes_engines.py` |

`docs/client-contract.md` §9 gives each in detail. Each fixes behaviour that SGK's frozen copies
still carry. "The freeze" above (decision U3) says that a defect found during the freeze is fixed
here after G2; decision U33 fixed these three before it. SGK receives them by adopting `v0.2.1`.

**Prompt 09 changed prose only.** It closed `[01-package-prose-names-sgks-layout]` (`cad7bc1`):
the comments and docstrings that cited SGK's layout, campaigns, logs, audits, issues and commits
were rewritten in 12 layer files and in `SQL/ShardedPool.py`, and in the test modules; the guard's
`KNOWN_HITS` is empty, and the new `datastorekit/tests/test_prose_names_no_source.py` scans every
comment and docstring of the package. With every docstring blanked, each of those 13 layer files
parses to the same AST before and after 09. From `v0.2.1`, no layer file equals its SGK source in
its comments except the seven that 09 did not touch, which are unchanged since `v0.2.0`:
`__init__.py`, `object.py`, `SQL/__init__.py`, `SQL/ClientPool.py`, `SQL/SerialPoolBroker.py`,
`SQL/ProfileAgent.py` and `tools/__init__.py`. "The differences allowed" above describes `v0.1.0`
and is not extended.

**The files each prompt changes:**
- **08a**: `datastorekit/SQL/ShardedPool.py`; the new
  `datastorekit/tests/test_unsupplied_sharded_table.py` and
  `datastorekit/tests/test_vectorized_get_payloads.py`; `docs/client-contract.md` (§9, §9.1). The
  log is `prompts/extraction/logs/08a-two-small-fixes.md`.
- **08b**: `datastorekit/SQL/ShardedPool.py`; the new
  `datastorekit/tests/test_refused_open_closes_engines.py`; `docs/client-contract.md` (§9.2). The
  log is `prompts/extraction/logs/08b-dispose-engines-on-a-refused-open.md`.
- **09**: the comments and docstrings of 13 layer files (`_timing.py`, `contract.py`,
  `defaults.py`, `replication.py`, `shard_paths.py`, `store_inventory.py`, `store_reader.py`,
  `SQL/Datastore.py`, `SQL/ShardedPool.py`, `SQL/factory_base.py`, `SQL/schema.py`,
  `tools/shard_key_audit.py` and `tools/sharded_store.py`) and of 30 modules under
  `datastorekit/tests/`, `test_layer_is_generic.py`'s `KNOWN_HITS` among them; the new
  `datastorekit/tests/test_prose_names_no_source.py`. The log is
  `prompts/extraction/logs/09-rewrite-the-package-prose.md`.
