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

### `actor-names` prompts 01 and 01b: a closed pool releases its actor names (`v0.2.2`)

**The fix has no source.** It was made here, by `actor-names` prompt 01 (`ac50a8a`), and closed
`[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]`. Extraction prompt 11 opened that
issue, from the first run of the package under real Ray, and 01 closed it on the extraction board,
`prompts/extraction/IMPLEMENTATION_STATE.md` §4. A closed pool, and an open that is refused, now
kill their shard actors and their broker with `ray.kill(handle, no_restart=True)`, so the actors'
names are free at once. A closed pool's handles are dead, and a second `__exit__` does nothing.
The names are unchanged, so two pools open at once in one Ray session still collide (decision U1,
`prompts/actor-names/README.md` §6.2). Its test module is
`datastorekit/tests/test_closed_pool_releases_its_names.py` (tests 1–6), and
`docs/client-contract.md` §9.3 gives the detail.

**SGK's frozen copies carry the defect.** SGK names the same actors, `SerialPoolBroker` and
`shard{key:04d}-store`, at `Datastore/SQL/ShardedPool.py:294`, `:305` and `:544`, at both
`6f7f291` and `b510bc9`, and its `__exit__` kills none of them. "The freeze" above (decision U3)
says that a defect found during the freeze is fixed here after G2. Decision U3 of `actor-names`
fixed this one before it, as decision U33 of the extraction campaign fixed three. SGK receives the
fix by adopting `v0.2.2`.

**01b's guard has no source either.** `actor-names` prompt 01b (`f024fc6`) closed
`[02-closing-a-pool-can-start-ray]`, which 01's kill introduced and which no release carried: it
was opened and closed on `prompts/actor-names/IMPLEMENTATION_STATE.md` (§4). A module-level
`_ray_is_running()` returns `ray.is_initialized()`, and `_kill_actors` kills nothing when it is
false, so closing a pool in a process that is not connected to Ray never reaches Ray's `ray.kill`,
which would start a local Ray first. SGK's `__exit__` calls no `ray.kill`, so SGK's frozen copies do
not have that defect. Its tests are tests 7 and 8 of the same module, and
`docs/client-contract.md` §9.4 gives the detail.

**What changed in the package**: `datastorekit/SQL/ShardedPool.py` only, by addition: 64 lines,
48 by 01 and 16 by 01b, and none removed (`git diff --numstat 33778b0 f024fc6 -- datastorekit`).
In this repository only, outside the wheel, the stand-in pool (`datastorekit/tests/standin_pool.py`),
the new test module, the smoke script `docs/extraction/ray_smoke_run.py` (by 01) and the contract's
§9.3 and §9.4 changed too. The suite went from 486 to 494.

**The files each prompt changes:**
- **01**: `datastorekit/SQL/ShardedPool.py`; `datastorekit/tests/standin_pool.py`; the new
  `datastorekit/tests/test_closed_pool_releases_its_names.py`; `docs/extraction/ray_smoke_run.py`;
  `docs/client-contract.md` (§9.3); `docs/extraction-verification.md` (§4.6). The log is
  `prompts/actor-names/logs/01-a-closed-pool-releases-its-actor-names.md`.
- **01b**: `datastorekit/SQL/ShardedPool.py`; `datastorekit/tests/standin_pool.py`;
  `datastorekit/tests/test_closed_pool_releases_its_names.py` (tests 7 and 8);
  `docs/client-contract.md` (§9.4); `docs/extraction-verification.md` (§4.7). The log is
  `prompts/actor-names/logs/01b-closing-a-pool-starts-no-ray.md`.

### `factory-defaults` prompt 01: the base defaults three hooks (`v0.2.3`)

**The change has no source, and is a departure from it.** SGK's base,
`Datastore/SQL/ObjectFactories/base.py` at `6f7f291` (the file map's source of
`datastorekit/SQL/factory_base.py`), makes all five of its hooks, `register`, `build`, `store`,
`validate` and `validate_on_startup`, `@staticmethod @abstractmethod`, and the package carried that
over. `factory-defaults` prompt 01 (`f5d8957`), carrying out decision U1 of
`prompts/factory-defaults/README.md` §6.2 on the user's ruling (2026-10-11), makes `store`,
`validate` and `validate_on_startup` defaulted, as the base already defaulted `revalidate`,
`owned_serials` and `inventory_spec`. It revisits decision U32 of the extraction campaign in part
(`prompts/extraction/README.md` §6.2, and U32's row on its board). It fixes no defect of SGK's:
SGK registers factory classes, which are never instantiated, so its base's abstractness was never
enforced on it. What it removes is Python's `TypeError` on instantiating a factory class that lacks
any of the three, which a client that registers factory instances met. Its test module is
`datastorekit/tests/test_factory_instances.py`, and `docs/client-contract.md` §9.5 gives the
detail.

**What changed in the package**: `datastorekit/SQL/factory_base.py` only (24 lines added and 6
removed, `git diff --numstat 6d8ee9a f5d8957 -- datastorekit/SQL`): three `@abstractmethod` lines
removed, the comment on defaulted hooks moved above the three and reworded, and a docstring added
to each of the three. Every hook's arguments and body are unchanged. In this repository only,
outside the wheel, `datastorekit/tests/test_neutral_client.py` changed (its `ABSTRACT_HOOKS` is
now `register` and `build`); `datastorekit/tests/client/instances.py` and its test module are new;
the smoke script `docs/extraction/ray_smoke_run.py` gained step I, a registry of instances under
real Ray; and the contract gained §9.5 and its five markers, the verification document §4.8 and
§8.1, and extraction U32 a dated note. The suite went from 494 to 504.

**The files 01 changes:**
- `datastorekit/SQL/factory_base.py`; `datastorekit/tests/test_neutral_client.py`; the new
  `datastorekit/tests/client/instances.py` and `datastorekit/tests/test_factory_instances.py`;
- `docs/extraction/ray_smoke_run.py`; `docs/client-contract.md` (§9.5);
  `docs/extraction-verification.md` (§4.8 and §8.1);
- `prompts/extraction/README.md` and `prompts/extraction/IMPLEMENTATION_STATE.md` (the notes on
  U32).

The log is `prompts/factory-defaults/logs/01-the-base-defaults-three-hooks.md`.

### `object-timestamp` prompt 01: the object carries a timestamp (`v0.3.0`)

**The change has no source in SGK.** SGK's `Datastore/object.py` at `6f7f291` (the file map's
source of `datastorekit/object.py`) takes `store_id` alone, and the package carried it over.
StochasticInstantons (SI), checked out at `/Users/ds283/Documents/Code/StochasticInstantons` and
read through `git` only, has a
`DatastoreObject` of its own, `Datastore/object.py`. That file was added at SI `3e56d39`
(2026-06-15) taking `store_id` alone; since SI `51b04f8` (2026-06-21, "Surface row-creation
timestamps via DatastoreObject") it has taken a `timestamp` and exposed it as a read-only property.
SI asked the package for the same (`prompts/object-timestamp/README.md` §0, the brief). Decision U1
of `prompts/object-timestamp/README.md` §6.2, on the user's ruling (2026-10-12), adds it, carried
out by `object-timestamp` prompt 01 (`1b2f91a`): **keyword-only**, where SI's is
positional-or-keyword. The layer never sets the value and never reads it; a factory that reads a
row may pass the row's `timestamp`. It fixes no defect. Its test module is
`datastorekit/tests/test_object_timestamp.py`, and `docs/client-contract.md` §9.6 gives the detail.

**What changed in the package**: `datastorekit/object.py` only (18 lines added and 1 removed,
`git diff --numstat 0de2b16 1b2f91a -- datastorekit/object.py`): the `datetime` import, the
keyword-only `timestamp` argument of `__init__` and its assignment to `self._timestamp`, and the
read-only `timestamp` property with its docstring. `store_id` and `available` are unchanged. In
this repository only, outside the wheel, one expected dict of
`datastorekit/tests/test_declared_facts.py` (`TestTheVersionObject`, decision U2) gained
`"_timestamp": None`; `datastorekit/tests/client/stamped.py` and its test module are new; and the
contract gained §9.6, and the verification document §4.9. The suite went from 504 to 509.

**The files 01 changes:**
- `datastorekit/object.py`; `datastorekit/tests/test_declared_facts.py`; the new
  `datastorekit/tests/client/stamped.py` and `datastorekit/tests/test_object_timestamp.py`;
- `docs/client-contract.md` (§9.6); `docs/extraction-verification.md` (§4.9).

The log is `prompts/object-timestamp/logs/01-the-object-carries-a-timestamp.md`.

### `fingerprint` prompt 01: the store fingerprint moves into the package (`v0.4.0`)

**Its source is SGK, after the import commit.** `datastorekit/store_fingerprint.py` comes from
SGK's `RunRegistry/stores.py:1164-1400` at `c8a7f14` (2026-10-12; `RunRegistry/` is unchanged from
there to SGK's `a5a6f6d`, `git diff --stat c8a7f14 a5a6f6d -- RunRegistry`): the five functions
`_sha256_lines`, `_tag_sets`, `fingerprint_of`, `compare_fingerprints` and `listing_lines`, and the
helpers `_tags_text`, `_difference` and `_presence`. The extract (`git show
c8a7f14:RunRegistry/stores.py`, lines 1164-1400, 237 lines) has SHA-256
`9b1a8aedb006ffa9c2635038eda2e87cad451106283d022a94f8038cd8eb0108`. The move is the user's ruling
of 2026-10-12, SGK's D3 (`prompts/fingerprint/README.md` §0), and was made by `fingerprint` prompt
01 (`d1b61d6`). Unlike `v0.1.0`'s files, this one is not under `compare_with_source.py`, which is
retired at `v0.1.0`; its comparison with the source is the equivalence check in 01's log (§4.3).

**The differences from the source**, each a decision of `prompts/fingerprint/README.md` §6.2:
- the client's format is a required argument of `fingerprint_of`, positional or by keyword, refused
  unless an `int` of at least 1, where the source read its own `FINGERPRINT_FORMAT` (U1);
- every fingerprint carries `encoding_format` beside the digest, outside the object the digest
  hashes; `compare_fingerprints` refuses two fingerprints whose `fingerprint_format` or
  `encoding_format` differ, keeping the source's `format` entry verbatim and adding an `encoding`
  entry; and the listing's first line gains ` encoding_format <e>` at its end (U2);
- `ENCODING_FORMAT = 1`, the package's version of the encoding and the algorithm, under a comment
  stating its bump rule, which contract §9.7 states too (U3);
- `canonical_json` is imported from `datastorekit.store_inventory` at module scope, where the
  source imported it inside two functions;
- the prose is rewritten for the package, naming no client, and the source's history comment of
  its own formats is left out.

Every digest, count and comparison entry is the source's: the equivalence check of 01's log §4.3,
on the neutral client's full store and 37 changed stores, at client formats 1 and 6, at both tested
ends, found 0 differences, every fingerprint equal to the source's but for `encoding_format`.
`datastorekit/store_inventory.py` is unchanged (`git diff --stat v0.2.2 d1b61d6 --
datastorekit/store_inventory.py` is empty).

**What changed in the package**: one module added, `datastorekit/store_fingerprint.py` (351
lines); every other file in the wheel is `v0.3.0`'s (`git diff --stat 2f5417e d1b61d6 --
datastorekit` lists the module, its test module and the golden only). In this repository only,
outside the wheel, `datastorekit/tests/test_store_fingerprint.py` (21 tests) and the golden
fingerprint `datastorekit/tests/data/store_fingerprint-neutral-1-encoding-1.json` are new, and the
contract gained §9.7 and its head line. The suite went from 509 to 530.

**The files 01 changes:**
- the new `datastorekit/store_fingerprint.py`, `datastorekit/tests/test_store_fingerprint.py` and
  `datastorekit/tests/data/store_fingerprint-neutral-1-encoding-1.json`;
- `docs/client-contract.md` (§9.7 and its head line).

The log is `prompts/fingerprint/logs/01-the-fingerprint-moves-into-the-package.md`.
