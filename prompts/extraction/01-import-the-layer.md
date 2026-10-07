# Prompt 01 — import the layer

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- G1 holds. SGK's `datastore-generic-followup` closed at **`6f7f291`**, which is the **import
  commit**.
- U2–U5 are taken (README §6.2).
- `git status` is clean in this repository.

**Closes:** nothing. **Opens:** only what the work finds.

**Recommended model:** **Opus**. The work is mechanical, but it is the base every later prompt and
every client's adoption stands on. The equivalence check (§2.5) has to be written so that it would
catch a real difference, not only pass on this one.

**Read first:**

1. [`README.md`](README.md): §0.1, §0.2, §1, §4 (the module map), §5 (all of it, rule 8
   especially) and §6.
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`, in particular "What this repository is"
   and "Repository mechanics".
3. In SGK at `6f7f291`, **read with `git -C /Users/ds283/Documents/Code/SecondaryGWKit show
   6f7f291:<path>`**, never from SGK's working tree, which may have moved on:
   - the 15 layer files and two tools of README §0.2;
   - `utilities.py` (`WallclockTimer`, `format_time` and the three `SECONDS_PER_*` constants
     `format_time` uses);
   - `config/defaults.py` (`DEFAULT_STRING_LENGTH = 256`);
   - `Datastore/tests/shard_store_fixtures.py` and the eight test modules of §2.6.

Line numbers below are at `6f7f291`.

---

## 1. What is wanted

The package `datastorekit` exists in this repository. Every module of it is SGK's module at
`6f7f291`, changed only in the ways §2.4 lists. A script proves that, line by line. The 88 SGK
tests that need no client run here and pass, in a venv that cannot see any client.

**No behaviour changes.** A defect noticed in SGK's code is recorded, not fixed (README §5 rules 4
and 8).

---

## 2. What to change

### 2.1 The venv

Create `venv/` (it is gitignored) with **Python 3.12** (`/opt/local/bin/python3.12`), and install
**`ray==2.43.0`** and **`sqlalchemy==2.0.39`**. These are SGK's versions (README §0.2), so a
failure here is caused by the move, not by the runtime. 05 adds the other end of the range. Also
install `black`. Record `pip freeze` in the log.

### 2.2 The package skeleton

- `pyproject.toml`: a setuptools build; name `datastorekit`; version `0.1.0.dev0`;
  `requires-python = ">=3.12"`; dependencies `ray` and `sqlalchemy>=2.0`, with no upper bounds
  yet, since 05 sets the ranges. The package includes `datastorekit/tests/`.
- `pip install -e .` into the venv, so the tests import the package the way a client will.
- New, empty `__init__.py` files where SGK has none: `datastorekit/tools/__init__.py` and
  `datastorekit/tests/__init__.py`.

### 2.3 The files, under README §4's names

| SGK at `6f7f291` | Here |
|---|---|
| `Datastore/__init__.py`, `object.py`, `contract.py`, `replication.py`, `shard_paths.py`, `store_reader.py`, `store_inventory.py` | `datastorekit/<same>` |
| `Datastore/SQL/__init__.py`, `schema.py`, `ShardedPool.py`, `Datastore.py`, `ClientPool.py`, `SerialPoolBroker.py`, `ProfileAgent.py` | `datastorekit/SQL/<same>` |
| `Datastore/SQL/ObjectFactories/base.py` | `datastorekit/SQL/factory_base.py` |
| `tools/sharded_store.py`, `tools/shard_key_audit.py` | `datastorekit/tools/<same>` |
| `config/defaults.py`'s `DEFAULT_STRING_LENGTH` | `datastorekit/defaults.py` (that one constant, nothing else) |
| `utilities.py`'s `WallclockTimer`, `format_time` and `SECONDS_PER_*` | `datastorekit/_timing.py` (those, and the imports they need, nothing else) |
| `Datastore/tests/shard_store_fixtures.py` and the eight modules of §2.6 | `datastorekit/tests/<same>` |

### 2.4 The differences allowed, and no others

Each class of difference below is allowed in the files it names. A difference that fits none of
them is a stop (§5).

- **D-imp — import rewrite.** In every `import` and `from … import` statement, **including
  imports inside functions** (for example `ShardedPool.py:406`, `:494`, `:1299`, `Datastore.py:198`
  and `store_inventory.py:993`), the module paths are mapped:
  - `Datastore.SQL.ObjectFactories.base` → `datastorekit.SQL.factory_base`;
  - `Datastore.<x>` → `datastorekit.<x>`;
  - `config.defaults` → `datastorekit.defaults`;
  - `utilities` → `datastorekit._timing`.

  Relative imports (`from .Datastore import Datastore`, `from .object import …`) are unchanged.
- **D-str — module paths in strings.** A string that names a module by its dotted path is mapped
  the same way. Examples: `mock.patch("Datastore.SQL.ShardedPool.resolve_shard_path", …)`
  (`test_delete_store.py:339`), and the `'Datastore.SQL'` in the "heavy modules" probes
  (`test_shard_paths.py:111-112`, `test_shard_key_audit_copy.py:136`).

  **The class name `Datastore` is not a module path**, and is never rewritten. An example is
  `"Datastore.set_version: …"` (`Datastore.py:155`). Neither is prose that refers to SGK's layout.
- **D-tool — how the tools are run.** In both tools:
  - the `_REPO_ROOT` / `sys.path.insert` bootstrap is removed (`sharded_store.py:34-36` and the
    same in `shard_key_audit.py`);
  - each usage or `prog` line naming `python tools/<name>.py` or `<name>.py` becomes
    `python -m datastorekit.tools.<name>`.

  In the three test modules that run the tools (`test_sharded_store_script`,
  `test_shard_key_audit_copy`, `test_shard_key_audit_refusals`):
  - a `[sys.executable, str(SCRIPT_or_TOOL), …]` command becomes
    `[sys.executable, "-m", "datastorekit.tools.<name>", …]`;
  - a `runpy.run_path(path, run_name="__main__")` probe becomes
    `runpy.run_module("datastorekit.tools.<name>", run_name="__main__")`;
  - the `REPO_ROOT` / `SCRIPT` / `TOOL` constants go if nothing else uses them.

  **What each such test asserts does not change.** The test still runs the tool in a subprocess,
  from an unrelated working directory, with no `PYTHONPATH`. That now works because the package is
  installed, not because of a path insertion. Each changed command is listed in the log.
- **D-root — the package's root in a test.** `test_shard_file_name.py:23-101` scans
  `REPO_ROOT / "Datastore"` and `REPO_ROOT / "tools"` for the naming rule. It scans the
  package's directory (`Path(datastorekit.__file__).parent`) instead, with `tests` excluded as
  before. The expected single site is `datastorekit/shard_paths.py`. `test_shard_paths.py:109`'s
  `repo_root` is the cwd of a subprocess; it becomes whatever directory lets the child import the
  installed package, which is any directory.
- **D-int — the internalised definitions.** `defaults.py` and `_timing.py` hold SGK's definitions
  byte for byte, plus a module docstring naming their source.
- **D-fmt — formatting.** `black` on every package file, as `CLAUDE.md` says. SGK's tree is
  black-clean, so this should change nothing beyond the lines the rewrite moved. Any reformatted
  line beyond those is reported.

### 2.5 The equivalence check

`docs/extraction/compare_with_source.py`, kept in the repository, run from the root as
`./venv/bin/python docs/extraction/compare_with_source.py`. For each file of §2.3:

- it reads the SGK source with `git -C <SGK> show 6f7f291:<path>`; the SGK path and the commit
  are constants at the top of the script;
- it reads the package file;
- it diffs them line by line;
- it puts **every** differing line in exactly one class of §2.4, by rule, not by a list of line
  numbers;
- it prints, for each file, the count per class and **every line it could not classify**.

It exits non-zero if any line is unclassified, or if a file of §2.3 is missing on either side.

The rules must be narrow. An import rule matches only an import statement whose only change is the
mapped path. A string rule matches only a quoted dotted path that the map takes to its image.

**Show that the check bites.** With the tree otherwise correct, introduce each of these changes
separately, show that the script exits non-zero and names the line, then revert:
- (a) one changed literal in `ShardedPool.py`;
- (b) an extra import in `schema.py`;
- (c) `Datastore.set_version` wrongly rewritten to `datastorekit.set_version` in `Datastore.py`;
- (d) a deleted line in `shard_paths.py`.

These four are in the log's breakage record (§3).

### 2.6 The tests: the 88 client-free tests

| Module | Tests at `6f7f291` |
|---|---|
| `test_shard_paths` | 7 |
| `test_shard_file_name` | 4 |
| `test_shardedpool_shard_paths` | 10 |
| `test_copy_move_store` | 22 |
| `test_delete_store` | 26 |
| `test_sharded_store_script` | 5 |
| `test_shard_key_audit_copy` | 3 |
| `test_shard_key_audit_refusals` | 11 |

The orchestrator ran them in SGK on 2026-10-07 at `99456d8`, whose layer, tools and tests are
`6f7f291`'s: **`Ran 88 tests … OK`**, in 5 s.

Each test keeps its name, its class and its assertions (README §5 rule 6). The only changes are
D-imp, D-str, D-tool and D-root.

### 2.7 The package's import guard

New `datastorekit/tests/test_package_imports.py`. It parses every module under `datastorekit/`
with `ast` (tests included) and collects every imported module, including imports inside
functions. It asserts that each one's root is:
- in `sys.stdlib_module_names`;
- `ray` or `sqlalchemy`;
- or `datastorekit`.

A second test checks that importing `datastorekit.shard_paths` in a fresh interpreter loads
neither `ray` nor `sqlalchemy`. This is the property SGK's `test_shard_paths` pins, checked here
for the package's own root.

This guard is only about imports. The vocabulary guard comes in 04.

### 2.8 `PROVENANCE.md`

At the repository root:
- the source repository, its URL, and the import commit `6f7f291`, with its subject line;
- §2.3's table;
- §2.4's classes;
- how to re-run §2.5;
- the U3 freeze: from `6f7f291` until G2, SGK's copies of these files do not change.

---

## 3. Verification

1. In a **fresh shell with no `PYTHONPATH`**, from `/tmp`:
   ```bash
   /Users/ds283/Documents/Code/DatastoreKit/venv/bin/python -c "import datastorekit, datastorekit.SQL.ShardedPool, datastorekit.store_inventory, datastorekit.tools.sharded_store"
   ```
   succeeds. With `-c "import Datastore"` in the same setting, it fails with
   `ModuleNotFoundError`, which shows that no client is on the path.
2. `./venv/bin/python -m unittest discover -s datastorekit/tests -t .` gives
   **`Ran 90 tests … OK`**: the 88, plus the two of §2.7.
3. `compare_with_source.py` exits 0. Its whole output, the counts per file and class, goes in
   the log.
4. **The breakage record.** Each item is a diff exactly as applied, with what failed. None is
   committed.
   - §2.5's (a)–(d), each failing the equivalence check;
   - `datastorekit/SQL/ShardedPool.py`'s `_assign_shard_keys` binding `key_id` instead of
     `key_serial`. This shows the ported tests still exercise the real code, through the package;
     name the test or tests that fail. If none fails, say so: that is a finding for 03, not a stop;
   - an `import numpy` added to `datastorekit/store_reader.py`, failing §2.7's guard;
   - the `sys.path` bootstrap removed from `datastorekit/tools/sharded_store.py` **and** the
     package uninstalled from the venv, failing `test_sharded_store_script`. Re-install afterwards.
5. `black --check` is clean on everything under `datastorekit/` and `docs/extraction/`.

---

## 4. Acceptance

1. §2.3's files exist under their names, plus the two new `__init__.py` files and
   `pyproject.toml`.
2. §3.1–§3.5 hold.
3. **The records**, in the same commit:
   - the log, `logs/01-import-the-layer.md`, per README §5.1. It also has `pip freeze`, the
     equivalence output, the list of D-tool command changes, and the test count before (SGK, 88)
     and after (here, 90);
   - this board: §1's row for 01 and the header;
   - `prompts/INDEX.md`: the campaign's line;
   - `docs/OPEN_ISSUES.md`, if the work opens anything;
   - **§1.2 of `docs/OPEN_ISSUES.md`:** for each of the four inherited issues, the log says
     whether the code it names is in the package as imported, and where. The rows stay; the log
     records the check.

---

## 5. Stop conditions — stop and ask the user

- A package file differs from its source in a way none of §2.4's classes covers, and making it
  fit would mean changing behaviour.
- A ported test fails, and passing it would need a change beyond D-imp, D-str, D-tool or D-root.
- The layer at `6f7f291` imports a module that is not in README §0.2's list of client
  dependencies, and is not the standard library, `ray`, `sqlalchemy` or the layer itself.
- Python 3.12 with Ray 2.43.0 and SQLAlchemy 2.0.39 cannot be installed.
- Anything would require editing, running or opening a store of SGK, ChamPBH or
  StochasticInstantons. Reading SGK files through `git show` is the only access this prompt has.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `pyproject.toml`;
  - `datastorekit/`, as §2.3 and §2.7 list;
  - `docs/extraction/compare_with_source.py`;
  - `PROVENANCE.md`;
  - the log, this board and `prompts/INDEX.md`;
  - `docs/OPEN_ISSUES.md`, if needed.

  `.gitignore` already excludes `venv/`.
- It ports no test that imports a client, and builds no neutral client (02).
- It sets no dependency range, adds no CI and makes no tag (05).
- It does not touch the repository's `README.md`. Usage text is 05's.
- It fixes nothing in SGK's code, including the four inherited issues.

---

## 7. The log and the board

`logs/01-import-the-layer.md`, using README §5.1, with the additions of §4.3.

`IMPLEMENTATION_STATE.md`: §1's row for 01 (landed, commit, log) and the header.
