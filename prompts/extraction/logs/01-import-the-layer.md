# Log 01 — import the layer

**Subject:** Import SGK's datastore layer as the package datastorekit · **Commit:** `8bc60a5` ·
**Date:** 2026-10-07 · **Model:** Claude Opus 5.5 · **Result:** landed. The package is SGK's layer at
`6f7f291` under README §4's names; `compare_with_source.py` exits 0; `Ran 90 tests … OK`.

Prompt: [`../01-import-the-layer.md`](../01-import-the-layer.md), with the orchestrator's notes for
this prompt (corrections and additions, followed as given except where §2 says otherwise).

## 1. What shipped

35 new files (`pyproject.toml`, 31 under `datastorekit/`, the check, `PROVENANCE.md`, this log), and
three records changed (`IMPLEMENTATION_STATE.md`, `prompts/INDEX.md`, `docs/OPEN_ISSUES.md`).

- **`pyproject.toml`**: setuptools build; name `datastorekit`; version `0.1.0.dev0`;
  `requires-python = ">=3.12"`; dependencies `ray` and `sqlalchemy>=2.0`, no upper bounds. The
  package is named explicitly (`[tool.setuptools.packages.find] include = ["datastorekit*"]`), so
  `datastorekit/tests/` is in it and `docs/`, `prompts/` are not.
- **`datastorekit/`**, 31 files:
  - the 15 layer files under §2.3's names (`__init__`, `object`, `contract`, `replication`,
    `shard_paths`, `store_reader`, `store_inventory`; `SQL/__init__`, `schema`, `ShardedPool`,
    `Datastore`, `ClientPool`, `SerialPoolBroker`, `ProfileAgent`; `SQL/factory_base`);
  - `tools/__init__.py` (empty), `tools/sharded_store.py`, `tools/shard_key_audit.py`;
  - `defaults.py` (`DEFAULT_STRING_LENGTH = 256`) and `_timing.py` (`WallclockTimer`,
    `SECONDS_PER_MINUTE/HOUR/DAY`, `format_time`, and the imports `time` and `traceback.print_tb`);
  - `tests/__init__.py` (empty), `tests/shard_store_fixtures.py` and the eight test modules of §2.6;
  - `tests/test_package_imports.py`, the import guard of §2.7 (2 tests).
- **`docs/extraction/compare_with_source.py`**, the equivalence check of §2.5 (§4.3 below).
- **`PROVENANCE.md`**: the source repository and its URL, the import commit with its subject, the
  file map, the classes of difference, how to re-run the check, and the U3 freeze.
- **This log**, the board's row for 01, its header and §3, `prompts/INDEX.md`, and
  `docs/OPEN_ISSUES.md` (two issues opened; §6).

The ported tests, each with its SGK origin. Module, class and method names are SGK's at `6f7f291`,
unchanged: `Datastore/tests/<module>.py` there, `datastorekit/tests/<module>.py` here. 88 tests,
in 22 classes:

| Module | Class | Tests | Methods |
|---|---|---|---|
| `test_copy_move_store` | `TestCopy` | 2 | `test_copy_to_a_new_directory_and_stem_reads_its_own_files`, `test_no_other_table_is_changed` |
| `test_copy_move_store` | `TestInterruption` | 5 | `test_copy`, `test_copy_rewrite_is_one_transaction`, `test_move`, `test_move_across_filesystems_fails_before_anything_moves`, `test_move_rewrite_is_one_transaction` |
| `test_copy_move_store` | `TestMove` | 3 | `test_new_directory_new_stem`, `test_new_directory_same_stem`, `test_same_directory_new_stem` |
| `test_copy_move_store` | `TestNothingElseIsTouched` | 2 | `test_copy`, `test_move` |
| `test_copy_move_store` | `TestRefusals` | 10 | `test_copy_temporary_name_or_its_journal_exists`, `test_destination_is_an_existing_directory`, `test_destination_is_the_source`, `test_destination_names_or_their_journals_exist`, `test_move_into_a_directory_holding_a_source_shard_name`, `test_source_journal_files`, `test_source_primary_missing_or_not_a_regular_file`, `test_source_shard_missing_symlinked_irregular_or_shared`, `test_source_shard_record_unusable`, `test_source_with_no_shards_or_no_shard_zero` |
| `test_delete_store` | `TestInterruption` | 1 | `test_every_point_of_interruption` |
| `test_delete_store` | `TestNewStyleStore` | 2 | `test_deletes_exactly_its_files_and_nothing_beside_them`, `test_lists_its_shards_in_ascending_serial_then_its_primary` |
| `test_delete_store` | `TestNoRay` | 1 | `test_ray_is_imported_and_never_initialised` |
| `test_delete_store` | `TestRecheckBeforeEachUnlink` | 4 | `test_a_primary_that_became_a_symbolic_link`, `test_a_shard_that_became_a_directory`, `test_a_shard_that_became_a_symbolic_link`, `test_a_shard_that_vanished` |
| `test_delete_store` | `TestRefusals` | 13 | `test_file_outside_the_primary_directory`, `test_journal_beside_a_shard`, `test_journal_beside_the_primary`, `test_missing_shard`, `test_no_shard_recorded`, `test_primary_is_a_directory`, `test_primary_is_a_symbolic_link`, `test_primary_missing`, `test_record_resolves_to_a_non_regular_file`, `test_record_resolves_to_a_symbolic_link`, `test_shards_table_cannot_be_read`, `test_two_serials_share_a_file`, `test_unusable_record` |
| `test_delete_store` | `TestResumeRelaxesOneThingOnly` | 5 | `test_a_journal_is_still_refused`, `test_a_missing_primary_is_still_refused`, `test_a_symbolic_link_is_still_refused`, `test_resume_on_a_whole_store_deletes_all_of_it`, `test_the_resumed_list_is_what_is_deleted` |
| `test_shard_file_name` | `TestShardFileName` | 4 | `test_a_new_store_written_through_the_fixtures_is_named_by_it`, `test_reproduces_the_constructors_old_names`, `test_returns_a_bare_name_independent_of_the_directory`, `test_the_pattern_is_written_once_outside_the_tests` |
| `test_shard_key_audit_copy` | `TestAuditOfACopiedStore` | 3 | `test_audit_does_not_fall_back_to_the_original_when_the_copy_lacks_shard_0`, `test_audit_of_the_copy_attaches_the_copys_shard`, `test_tool_imports_no_heavy_dependency` |
| `test_shard_key_audit_refusals` | `TestTheAuditRefuses` | 11 | `test_a_current_store_is_still_audited`, `test_a_primary_naming_another_stores_shards_by_absolute_path`, `test_a_primary_naming_its_own_siblings_by_absolute_path`, `test_a_primary_whose_shard_key_config_is_empty`, `test_a_primary_without_shard_key_config`, `test_a_record_that_is_unusable_in_a_later_shard_is_refused_too`, `test_a_shard_0_that_is_not_a_database`, `test_a_shard_0_without_the_shard_key_table`, `test_a_shard_key_config_without_key_type`, `test_a_shard_keys_table_without_key_serial`, `test_a_shards_table_without_filename` |
| `test_shard_paths` | `TestModuleIsStandalone` | 1 | `test_import_pulls_in_no_heavy_dependency` |
| `test_shard_paths` | `TestResolveShardPath` | 5 | `test_bare_name_resolves_to_the_sibling`, `test_non_string_record_is_refused`, `test_refused_records`, `test_relative_primary_is_refused`, `test_result_is_absolute_and_in_the_primarys_directory` |
| `test_shard_paths` | `TestShardFileProblem` | 1 | `test_each_kind_of_unusable_shard` |
| `test_sharded_store_script` | `TestShardedStoreScript` | 5 | `test_copy_succeeds_from_another_directory_without_pythonpath`, `test_help_carries_the_three_statements`, `test_move_succeeds`, `test_ray_is_imported_but_never_initialised`, `test_refusal_exits_nonzero_and_writes_nothing` |
| `test_shardedpool_shard_paths` | `TestCopiedStore` | 2 | `test_copied_directory_reads_its_own_shards_not_the_originals`, `test_copied_with_a_renamed_primary_reads_its_own_shards` |
| `test_shardedpool_shard_paths` | `TestFailClosed` | 5 | `test_missing_shard_of_a_new_store_is_refused_by_name`, `test_moved_store_with_no_shards_is_refused`, `test_record_that_is_not_a_bare_name_is_refused_on_read`, `test_symlinked_shard_is_refused`, `test_two_records_resolving_to_one_file_are_refused` |
| `test_shardedpool_shard_paths` | `TestNoSideEffect` | 1 | `test_reading_a_new_store_leaves_the_primary_unchanged` |
| `test_shardedpool_shard_paths` | `TestRoundTrip` | 2 | `test_new_store_records_bare_names_and_survives_a_move`, `test_renaming_the_primary_alone_keeps_its_shards` |

Checked by `ast` against SGK's source: the same classes and methods, in the same order, in all
eight modules. The bodies of eight methods differ, and only by D-imp, D-str, D-tool or D-root
(the equivalence check accounts for every line): `test_import_pulls_in_no_heavy_dependency`,
`test_the_pattern_is_written_once_outside_the_tests`, `test_file_outside_the_primary_directory`,
`test_ray_is_imported_but_never_initialised`, and the three of `test_shard_key_audit_copy`. The
helpers `run_script` (`test_sharded_store_script`) and `audit` (`test_shard_key_audit_refusals`)
carry the other D-tool command changes.

### 1.1 The D-tool command changes

| File | SGK at `6f7f291` | Here |
|---|---|---|
| `tools/sharded_store.py:5-6` (docstring usage) | `python tools/sharded_store.py copy SRC DST` / `move SRC DST` | `python -m datastorekit.tools.sharded_store copy SRC DST` / `move SRC DST` |
| `tools/sharded_store.py:34-37` | the `_REPO_ROOT` / `sys.path.insert` bootstrap and the blank line after it | removed |
| `tools/sharded_store.py:43` | `prog="sharded_store.py",` | `prog="python -m datastorekit.tools.sharded_store",` |
| `tools/shard_key_audit.py:44` (docstring usage) | `python tools/shard_key_audit.py /path/to/primary.sqlite` | `python -m datastorekit.tools.shard_key_audit /path/to/primary.sqlite` |
| `tools/shard_key_audit.py:52-55` | the bootstrap and one blank line | removed |
| `test_sharded_store_script.py:28-29` | `REPO_ROOT = …parents[2]`, `SCRIPT = REPO_ROOT / "tools" / "sharded_store.py"` | removed (nothing else used them) |
| `test_sharded_store_script.py:50` (`run_script`) | `[sys.executable, str(SCRIPT), *map(str, args)]` | `[sys.executable, "-m", "datastorekit.tools.sharded_store", *map(str, args)]` |
| `test_sharded_store_script.py:95` (the `runpy` probe's `sys.argv`) | `sys.argv = [{str(SCRIPT)!r}, 'copy', …]` | `sys.argv = ['datastorekit.tools.sharded_store', 'copy', …]` |
| `test_sharded_store_script.py:97` | `runpy.run_path({str(SCRIPT)!r}, run_name='__main__')` | `runpy.run_module('datastorekit.tools.sharded_store', run_name='__main__')` |
| `test_shard_key_audit_copy.py:34-35` | `REPO_ROOT`, `TOOL = REPO_ROOT / "tools" / "shard_key_audit.py"` | removed |
| `test_shard_key_audit_copy.py:90`, `:112` | `[sys.executable, str(TOOL), str(self.b / "store.sqlite")]` | `[sys.executable, "-m", "datastorekit.tools.shard_key_audit", str(self.b / "store.sqlite")]` (black splits it over six lines) |
| `test_shard_key_audit_copy.py:130` | `sys.argv = [{str(TOOL)!r}, …]` | `sys.argv = ['datastorekit.tools.shard_key_audit', …]` |
| `test_shard_key_audit_copy.py:132` | `runpy.run_path({str(TOOL)!r}, run_name='__main__')` | `runpy.run_module('datastorekit.tools.shard_key_audit', run_name='__main__')` |
| `test_shard_key_audit_refusals.py:47-48` | `REPO_ROOT`, `TOOL` | removed |
| `test_shard_key_audit_refusals.py:94` (`audit`) | `[sys.executable, str(TOOL), str(primary)]` | `[sys.executable, "-m", "datastorekit.tools.shard_key_audit", str(primary)]` |

Every subprocess still runs from an unrelated directory (`self.cwd`, under the test's temporary
directory) with `PYTHONPATH` removed. In the `runpy` probes `sys.argv[0]` is now the module name:
`argparse`'s `prog` is fixed and `shard_key_audit.main` checks only `len(argv)`, so nothing reads
it. Under `-m`, `shard_key_audit.py:72` prints `usage: {argv[0]} …` with the module's file path;
it is not a usage line naming the tool, so it is unchanged, and no ported test asserts on it.

### 1.2 D-root

- `test_shard_file_name.py`: `import datastorekit`; `REPO_ROOT = Path(__file__).resolve().parents[2]`
  became `PACKAGE_DIR = Path(datastorekit.__file__).resolve().parent`; the scan of
  `REPO_ROOT / "Datastore"` and `REPO_ROOT / "tools"` became one scan of `PACKAGE_DIR`, with
  `tests` excluded relative to it; the sites are named relative to `PACKAGE_DIR.parent`; the
  expected single site is `["datastorekit/shard_paths.py"]`.
- `test_shard_paths.py:109`: **unchanged.** `repo_root = Path(__file__).resolve().parents[2]` is
  this repository's root here, which holds `datastorekit/`, so the child imports the package from
  it with `PYTHONPATH` set to it. The prompt allows any directory; this one needed no change.

## 2. Deviations from the prompt

1. **The two `__init__.py` files are copies, not new files.** SGK has `tools/__init__.py` and
   `Datastore/tests/__init__.py`, both 0 bytes, contrary to §2.2. Ours are empty as the prompt says,
   and the equivalence check compares them with their sources (equal). SGK's
   `Datastore/SQL/ObjectFactories/__init__.py` has no counterpart. **STRUCTURALLY REQUIRED.**
2. **`_timing.py` takes two imports, `time` and `traceback.print_tb`.** The orchestrator's note said
   `import time` is the only import the definitions need. `WallclockTimer.__exit__` calls
   `print_tb` (`utilities.py:17`), so the prompt's "and the imports they need" takes
   `from traceback import print_tb` too (`utilities.py:3`). `zip_longest` (`:2`) is used only by
   `grouper` and is not taken. **STRUCTURALLY REQUIRED.**
3. **`config/defaults.py` is not one line at `6f7f291`.** The note said it is; it is 203 lines with
   many constants and comments. `defaults.py` takes line 1, `DEFAULT_STRING_LENGTH = 256`, and
   nothing else, as §2.3 says. Recorded so the note's fact is corrected; no effect on the work.
   **IMPLEMENTATION CHOICE** (none needed beyond the prompt's own rule).
4. **The two internalised modules' docstrings do not name SGK.** D-int asks for "a module docstring
   naming their source". `CLAUDE.md` says the package names no client "in code, strings, docstrings
   or comments". Each docstring names the source *file* (`config/defaults.py`, `utilities.py`) and
   the import commit `6f7f291`, calls it "the source repository", and points to `PROVENANCE.md`,
   which names SGK. The equivalence check requires both the file name and the commit in the
   docstring. **IMPLEMENTATION CHOICE.**
5. **The last breakage of §3.4 is the package uninstalled, with no diff.** D-tool already removes
   the bootstrap, as the note says. The commands are recorded in §4.4. **STRUCTURALLY REQUIRED.**
6. **Breakage (e)**, a D-str-style rewrite of prose, is added to (a)–(d) at the orchestrator's
   direction. **IMPLEMENTATION CHOICE** (orchestrator's).
7. **`black==25.1.0`** is installed rather than the latest `black`, at the orchestrator's direction,
   so that D-fmt measures the move and not a newer style. The check refuses to run (exit 2) under
   any other version. **IMPLEMENTATION CHOICE** (orchestrator's).
8. **The equivalence check's design.** It follows the note's recommendation in spirit (each rule is
   a substitution applied to the source) but compares **exactly**, not token for token: the source
   with every rule applied is passed through `black` 25.1.0 itself, and the result must equal the
   package file byte for byte. D-fmt is therefore exactly "what `black` changed", with no tolerance.
   (a)–(e) fail by construction (§4.3). **IMPLEMENTATION CHOICE.**
9. **Placeholder-free f-strings after D-tool.** `f"    runpy.run_module('datastorekit.tools.<name>',
   run_name='__main__')\n"` keeps its `f` prefix, though it has no placeholder now, so that the
   change is the substitution inside the literal and nothing else. **IMPLEMENTATION CHOICE.**
10. **A second §3 issue.** The notes expect one issue (the prose). The work also found that the
    ported fixtures and tests use SGK's table names (`wavenumber`, `GkSource`, `wavenumber_serial`),
    which `CLAUDE.md` says the package never names. Per `CLAUDE.md` rule 4 it is recorded and
    opened, not fixed: `[01-ported-tests-use-sgk-table-names]`. The index goes from 4 to **6**, not
    5. **IMPLEMENTATION CHOICE**, flagged for the orchestrator.

No UNINTENDED DRIFT was found.

## 3. The venv

`venv/` created with `/opt/local/bin/python3.12` (Python 3.12.15, arm64). Installed `ray==2.43.0`,
`sqlalchemy==2.0.39`, `black==25.1.0`, then `pip install -e .`. `pip freeze` (after the re-install
of §4.4):

```
aiosignal==1.4.0
attrs==26.1.0
black==25.1.0
certifi==2026.7.22
charset-normalizer==3.5.2
click==8.5.0
-e git+https://github.com/ds283/DatastoreKit.git@bd9f461edf6aa272399cb98b91d348ece8b42083#egg=datastorekit
filelock==4.0.12
frozenlist==1.8.0
idna==3.20
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
msgpack==1.2.3
mypy_extensions==1.1.0
packaging==26.3
pathspec==1.1.1
platformdirs==4.12.3
protobuf==7.36.2
PyYAML==6.0.3
ray==2.43.0
referencing==0.37.0
requests==2.34.2
rpds-py==2026.9.1
SQLAlchemy==2.0.39
typing_extensions==4.16.0
urllib3==2.8.0
```

The editable install is setuptools' finder hook
(`__editable___datastorekit_0_1_0_dev0_finder.py`); it maps `datastorekit` alone and puts no
directory on `sys.path`.

## 4. Verification performed

### 4.1 Imports from a clean shell (§3.1)

From the session scratchpad (`…/scratchpad/agent-01/elsewhere`, outside this repository, holding
no `datastorekit/` or `Datastore/`), in `env -u PYTHONPATH bash --noprofile --norc`:

```
PYTHONPATH=unset cwd=/private/tmp/claude-35086/…/scratchpad/agent-01/elsewhere
$ venv/bin/python -c "import datastorekit, datastorekit.SQL.ShardedPool, datastorekit.store_inventory, datastorekit.tools.sharded_store"
import ok /Users/ds283/Documents/Code/DatastoreKit/datastorekit/__init__.py
exit 0
$ venv/bin/python -c "import Datastore"
ModuleNotFoundError: No module named 'Datastore'
exit 1
```

### 4.2 The suite (§3.2)

`./venv/bin/python -m unittest discover -s datastorekit/tests -t .` from the repository root:
**`Ran 90 tests in 5.917s` / `OK`.**

- **Before:** 0 here (no tests existed). SGK's 88, measured by the orchestrator at SGK `99456d8`
  (whose layer, tools and tests are `6f7f291`'s): `Ran 88 tests … OK`.
- **After:** 90 = the 88 + the 2 of `test_package_imports`. By module, from the loader: 7, 4, 10,
  22, 26, 5, 3, 11 (as §2.6), and 2.

### 4.3 The equivalence check (§3.3)

`./venv/bin/python docs/extraction/compare_with_source.py`, exit **0**. Its whole output:

```
source:  /Users/ds283/Documents/Code/SecondaryGWKit at 6f7f291e857265e429f5d6f810124fd3bf57ce55 Record the orchestrator's review of datastore-generic-followup prompt 03
package: /Users/ds283/Documents/Code/DatastoreKit/datastorekit
black:   25.1.0

Lines per file and class, as -source/+package: the source lines a class changed or
removed, and the package lines it accounts for.

file                                                        D-imp         D-str        D-tool        D-root         D-int         D-fmt  UNCLASSIFIED
datastorekit/__init__.py                                        .             .             .             .             .             .             .
datastorekit/object.py                                          .             .             .             .             .             .             .
datastorekit/contract.py                                        .             .             .             .             .             .             .
datastorekit/replication.py                                     .             .             .             .             .             .             .
datastorekit/shard_paths.py                                     .             .             .             .             .             .             .
datastorekit/store_reader.py                                -3/+3             .             .             .             .             .             .
datastorekit/store_inventory.py                             -2/+2             .             .             .             .             .             .
datastorekit/SQL/__init__.py                                    .             .             .             .             .             .             .
datastorekit/SQL/schema.py                                  -2/+2             .             .             .             .             .             .
datastorekit/SQL/ShardedPool.py                           -13/+13             .             .             .             .             .             .
datastorekit/SQL/Datastore.py                               -9/+9             .             .             .             .             .             .
datastorekit/SQL/ClientPool.py                              -1/+1             .             .             .             .             .             .
datastorekit/SQL/SerialPoolBroker.py                            .             .             .             .             .             .             .
datastorekit/SQL/ProfileAgent.py                            -2/+2             .             .             .             .             .             .
datastorekit/SQL/factory_base.py                                .             .             .             .             .             .             .
datastorekit/tools/__init__.py                                  .             .             .             .             .             .             .
datastorekit/tools/sharded_store.py                         -1/+1             .         -7/+3             .             .             .             .
datastorekit/tools/shard_key_audit.py                       -1/+1             .         -5/+1             .             .             .             .
datastorekit/defaults.py                                        .             .             .             .       -202/+5             .             .
datastorekit/_timing.py                                         .             .             .             .        -20/+6             .             .
datastorekit/tests/__init__.py                                  .             .             .             .             .             .             .
datastorekit/tests/shard_store_fixtures.py                  -2/+2             .             .             .             .             .             .
datastorekit/tests/test_shard_paths.py                      -1/+1         -2/+2             .             .             .             .             .
datastorekit/tests/test_shard_file_name.py                  -2/+2             .             .         -8/+6             .             .             .
datastorekit/tests/test_shardedpool_shard_paths.py          -1/+1             .             .             .             .             .             .
datastorekit/tests/test_copy_move_store.py                  -3/+3             .             .             .             .             .             .
datastorekit/tests/test_delete_store.py                     -3/+3         -1/+1             .             .             .             .             .
datastorekit/tests/test_sharded_store_script.py             -2/+2             .         -5/+3             .             .         -1/+0             .
datastorekit/tests/test_shard_key_audit_copy.py             -1/+1         -1/+1        -6/+14             .             .             .             .
datastorekit/tests/test_shard_key_audit_refusals.py         -1/+1             .         -3/+1             .             .             .             .
total                                                     -50/+50         -4/+4       -26/+22         -8/+6      -222/+11         -1/+0         -0/+0

files compared: 30
not compared (new in the package): datastorekit/tests/test_package_imports.py

Lines listed: D-fmt always, UNCLASSIFIED always, the rest with --show.
datastorekit/tests/test_sharded_store_script.py (from Datastore/tests/test_sharded_store_script.py):
  D-fmt         source line removed or changed  Datastore/tests/test_sharded_store_script.py:27: 

OK: every differing line is classified
```

Per class, over the 30 files (`-source/+package` lines): D-imp −50/+50, D-str −4/+4,
D-tool −26/+22, D-root −8/+6, D-int −222/+11, D-fmt −1/+0, UNCLASSIFIED 0.

- D-int's −222 are the source lines not taken: 202 of `config/defaults.py` and 20 of
  `utilities.py` (`zip_longest`'s import and `grouper`). Its +11 are the two docstrings and the
  blank line after each.
- **The one D-fmt line beyond a rewritten line** is a blank line,
  `test_sharded_store_script.py:27` in SGK. Removing the `REPO_ROOT` / `SCRIPT` constants (D-tool)
  left three blank lines before `def _clean_env`, and `black` keeps two. No other line was
  reformatted outside the lines the rewrite moved; the only reflow of a rewritten line is
  `test_shard_key_audit_copy`'s two command lists (D-tool, split by `black`).
- `--show` lists every classified line; the D-str, D-tool and D-root lines it lists are those of
  §1.1, §1.2 and the four strings `test_shard_paths.py:111-112`, `test_delete_store.py:339` and
  `test_shard_key_audit_copy.py:136`. `Datastore.py:155` (`f"Datastore.set_version: …"`) is not
  touched.

**How the check is built** (its docstring has the detail). Each class is a rule applied to the
source text; the rules run in order, then `black`; the result must equal the package file byte
for byte, and any line on which they differ is UNCLASSIFIED. Each line a rule changes carries that
rule's class (the first, if two touch it). So no rule can explain a change it does not make.
- D-imp finds import statements with `ast` (so at any depth) and replaces only the module path's
  tokens, only when the image is a module of the package.
- D-str looks only at plain string literals, and maps a dotted path only when it is the whole
  literal, is itself quoted inside the literal, or follows `import`/`from` at the literal's start
  or after `"; "`. The image must be a module, or a name bound at a module's top level (an import
  only: a module). So `"Datastore.set_version"` is refused even as a whole literal:
  `datastorekit/__init__.py` binds no `set_version`.
- D-tool and D-root are substitutions of the text the prompt names, in the files it names.
- D-int keeps only the named top-level definitions and the imports they use, and requires the
  docstring to name the source file and commit.
- A file missing on either side is a failure. Package files the check does not compare are listed
  (`test_package_imports.py`, as new).

### 4.4 The deliberate-breakage record (§3.4)

Each diff below is exactly as applied, taken with `git diff` against the staged tree that this
commit records. Each was checked with `git apply --check` and `git apply -R --check`, applied, run,
and reverted with `git apply -R` in `bash`; after each, `git diff` was empty. None is committed.
For (a)–(e), each excerpt is the check's table row for the broken file (columns D-imp, D-str,
D-tool, D-root, D-int, D-fmt, UNCLASSIFIED), the lines it names, and its verdict.

**(a) a changed literal in `ShardedPool.py`** — check exits **1**:

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 8d1fd81..3a16b99 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -950,7 +950,7 @@ class ShardedPool:
                     self._shard_key_config_table.c.key_type,
                 )
             )
-            num_config = 0
+            num_config = 1
             for row in shard_key_configs:
                 num_config += 1
                 if num_config == 1:
```
```
datastorekit/SQL/ShardedPool.py                           -13/+13             .             .             .             .             .         -1/+1

  UNCLASSIFIED  expected, not in the package  Datastore/SQL/ShardedPool.py:953:             num_config = 0
  UNCLASSIFIED  in the package, not expected  datastorekit/SQL/ShardedPool.py:953:             num_config = 1
FAIL: 2 line(s) unclassified, or a file missing
```

**(b) an extra import in `schema.py`** (a package import, the kind a loose import rule would
accept) — check exits **1**:

```diff
diff --git a/datastorekit/SQL/schema.py b/datastorekit/SQL/schema.py
index 25e44ba..1f3256e 100644
--- a/datastorekit/SQL/schema.py
+++ b/datastorekit/SQL/schema.py
@@ -49,6 +49,7 @@ import sqlalchemy as sqla
 
 from datastorekit.contract import VERSION_TABLE
 from datastorekit.store_inventory import inventory_specs
+from datastorekit.replication import ReadOnlyMiss
 
 
 class BuiltSchema(NamedTuple):
```
```
datastorekit/SQL/schema.py                                  -2/+2             .             .             .             .             .         -0/+1

  UNCLASSIFIED  in the package, not expected  datastorekit/SQL/schema.py:52: from datastorekit.replication import ReadOnlyMiss
FAIL: 1 line(s) unclassified, or a file missing
```

**(c) `Datastore.set_version` rewritten to `datastorekit.set_version` in `Datastore.py`** — check
exits **1**:

```diff
diff --git a/datastorekit/SQL/Datastore.py b/datastorekit/SQL/Datastore.py
index 83f33ea..4a789a2 100644
--- a/datastorekit/SQL/Datastore.py
+++ b/datastorekit/SQL/Datastore.py
@@ -152,7 +152,7 @@ class Datastore:
         """
         if isinstance(serial, bool) or not isinstance(serial, int):
             raise TypeError(
-                f"Datastore.set_version: the version serial must be an int, not {serial!r}"
+                f"datastorekit.set_version: the version serial must be an int, not {serial!r}"
             )
         if self._version_serial is not None and self._version_serial != serial:
             raise RuntimeError(
```
```
datastorekit/SQL/Datastore.py                               -9/+9             .             .             .             .             .         -1/+1

  UNCLASSIFIED  expected, not in the package  Datastore/SQL/Datastore.py:155:                 f"Datastore.set_version: the version serial must be an int, not {serial!r}"
  UNCLASSIFIED  in the package, not expected  datastorekit/SQL/Datastore.py:155:                 f"datastorekit.set_version: the version serial must be an int, not {serial!r}"
FAIL: 2 line(s) unclassified, or a file missing
```

**(d) a deleted line in `shard_paths.py`** — check exits **1**:

```diff
diff --git a/datastorekit/shard_paths.py b/datastorekit/shard_paths.py
index c5354a8..fcb5e96 100644
--- a/datastorekit/shard_paths.py
+++ b/datastorekit/shard_paths.py
@@ -98,7 +98,6 @@ def resolve_shard_path(primary: Union[str, Path], stored: str) -> Path:
             f"shard record {stored!r} is not a string (type {type(stored).__name__})"
         )
 
-    name = _require_bare_name(stored, stored)
 
     return primary.parent / name
 
```
```
datastorekit/shard_paths.py                                     .             .             .             .             .             .         -1/+0

  UNCLASSIFIED  expected, not in the package  Datastore/shard_paths.py:101:     name = _require_bare_name(stored, stored)
FAIL: 1 line(s) unclassified, or a file missing
```

**(e) (the orchestrator's) a D-str rewrite of prose in `shard_key_audit.py`'s docstring** — check
exits **1**:

```diff
diff --git a/datastorekit/tools/shard_key_audit.py b/datastorekit/tools/shard_key_audit.py
index 96b9deb..8bbeb4c 100644
--- a/datastorekit/tools/shard_key_audit.py
+++ b/datastorekit/tools/shard_key_audit.py
@@ -16,7 +16,7 @@ This script only ever opens databases read-only (sqlite3 `mode=ro` URIs). It
 is structurally incapable of modifying a datastore.
 
 The shard file it attaches for the cross-file check is found exactly as
-ShardedPool finds it, by the one resolver in Datastore/shard_paths.py: the
+ShardedPool finds it, by the one resolver in datastorekit/shard_paths.py: the
 `shards` record's file name, in the primary's own directory. A record that is
 not a bare file name, an absolute path included, is refused, so auditing a
 copied store can never check the original's shard in place of the copy's.
```
```
datastorekit/tools/shard_key_audit.py                       -1/+1             .         -5/+1             .             .             .         -1/+1

  UNCLASSIFIED  expected, not in the package  tools/shard_key_audit.py:19: ShardedPool finds it, by the one resolver in Datastore/shard_paths.py: the
  UNCLASSIFIED  in the package, not expected  datastorekit/tools/shard_key_audit.py:19: ShardedPool finds it, by the one resolver in datastorekit/shard_paths.py: the
FAIL: 2 line(s) unclassified, or a file missing
```

**(f) `_assign_shard_keys` binding `key_id` instead of `key_serial`** (`ShardedPool.py:3561`):

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 8d1fd81..0a6a83e 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -3558,7 +3558,7 @@ class ShardedPool:
                 # insert a new record for this key
                 result = conn.execute(
                     sqla.insert(self._shard_key_table),
-                    {"key_serial": item.store_id, "shard_id": new_shard},
+                    {"key_id": item.store_id, "shard_id": new_shard},
                 )
                 assigned_serial = result.inserted_primary_key[0]
 
```

Result: **`Ran 90 tests` / `OK`. No test fails.** A probe confirms why: with
`raise RuntimeError("probe: _assign_shard_keys reached")` as the method's first line, the suite is
still `Ran 90 tests` / `OK` and the message appears nowhere in its output. None of the 88 reaches
`_assign_shard_keys`: they build primaries by hand or with `write_new_store` (the constructor's
new-store branch without its actors), and never store a shard-keyed object (no actors, no Ray). This is a finding for 03, not a stop (§3.4). The probe's diff:

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 8d1fd81..9b5d2d5 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -3503,6 +3503,7 @@ class ShardedPool:
         return [self._shards[shard_id].object_validate.remote(item)]
 
     def _assign_shard_keys(self, obj):
+        raise RuntimeError("probe: _assign_shard_keys reached")
         if isinstance(obj, list):
             data = obj
         else:
```

**(g) `import numpy` added to `store_reader.py`**:

```diff
diff --git a/datastorekit/store_reader.py b/datastorekit/store_reader.py
index 46de102..784cf4b 100644
--- a/datastorekit/store_reader.py
+++ b/datastorekit/store_reader.py
@@ -46,6 +46,7 @@ from dataclasses import dataclass
 from pathlib import Path
 from typing import Iterator, Mapping, Tuple, Union
 
+import numpy
 import sqlalchemy as sqla
 
 from datastorekit.SQL.ShardedPool import ShardedPool
```

Result: `Ran 90 tests` / `FAILED (failures=1)`. The one failure is the guard,
`test_package_imports.TestPackageImports.test_every_import_is_stdlib_ray_sqlalchemy_or_the_package`:
`['datastorekit/store_reader.py:49: numpy'] != []`. `numpy` is not installed in the venv, so any
test that imported `store_reader` would also fail; none did. The layer imports `store_reader` only
inside functions (`ShardedPool.py:406`, `:494`, `:1299`, `Datastore.py:198`) that the 88 do not
reach.

**(h) the package uninstalled.** There is no diff: D-tool already removed the bootstrap. Commands,
from the repository root:

```bash
./venv/bin/pip uninstall -y datastorekit     # Successfully uninstalled datastorekit-0.1.0.dev0
./venv/bin/python -m unittest discover -s datastorekit/tests -t .
./venv/bin/pip install -e .
./venv/bin/python -m unittest discover -s datastorekit/tests -t .
```

Uninstalled: `Ran 90 tests` / `FAILED (failures=19)`, every one a subprocess that runs a tool from
an unrelated directory with no `PYTHONPATH`, failing with `No module named 'datastorekit'`:

- `test_shard_key_audit_copy` (3): `test_audit_does_not_fall_back_to_the_original_when_the_copy_lacks_shard_0`, `test_audit_of_the_copy_attaches_the_copys_shard`, `test_tool_imports_no_heavy_dependency`
- `test_shard_key_audit_refusals` (11): `test_a_current_store_is_still_audited`, `test_a_primary_naming_another_stores_shards_by_absolute_path`, `test_a_primary_naming_its_own_siblings_by_absolute_path`, `test_a_primary_whose_shard_key_config_is_empty`, `test_a_primary_without_shard_key_config`, `test_a_record_that_is_unusable_in_a_later_shard_is_refused_too`, `test_a_shard_0_that_is_not_a_database`, `test_a_shard_0_without_the_shard_key_table`, `test_a_shard_key_config_without_key_type`, `test_a_shard_keys_table_without_key_serial`, `test_a_shards_table_without_filename`
- `test_sharded_store_script` (5): `test_copy_succeeds_from_another_directory_without_pythonpath`, `test_help_carries_the_three_statements`, `test_move_succeeds`, `test_ray_is_imported_but_never_initialised`, `test_refusal_exits_nonzero_and_writes_nothing`

The in-process tests import the package from the repository root under `-t .`, and pass, as the
note expects. Re-installed: `Ran 90 tests` / `OK`.

### 4.5 `black` (§3.5)

`./venv/bin/black --check datastorekit docs/extraction` → `32 files would be left unchanged.`

### 4.6 The inherited issues (`docs/OPEN_ISSUES.md` §1.2), in the package as imported

All four are in the package unchanged. The rows stay in §1.2.

| Issue | Where its code is here |
|---|---|
| `[00-a-drop-action-drops-a-replicated-table-outside-the-in-flight-record]` | **In the package.** The mechanism: each actor drops the tables it is given in its constructor, `datastorekit/SQL/Datastore.py:140` (`self._drop_tables(drop_tables)`; the method at `:410-440`), and recreates them in `_ensure_tables` (`:141`, `:399`), outside any in-flight record; `ShardedPool` hands every actor the same list (`SQL/ShardedPool.py:316`). Which table is dropped (SGK's `--drop` names and the replicated table they map to) is the client's, not here. |
| `[00-a-new-stores-first-open-can-leave-a-primary-without-its-shards]` | **In the package.** `ShardedPool.__init__` writes the new primary and its `shards` table first (`SQL/ShardedPool.py:216-240`, `_write_shard_data()` at `:240`); the actors that create the shard files are made afterwards (`:316`); the next open is refused by `_check_shard_files` (`:1061`). |
| `[00-the-inventory-cannot-see-a-serial-split]` | **In the package.** `datastorekit/store_inventory.py`: a replicated class is compared across shards on key, tags, validated flag and value count only (module docstring `:53-56`; `_combine`, `:830`). The fingerprint that relies on it stays in SGK (`RunRegistry/stores.py`). |
| `[01-cross-filesystem-move-advice-says-delete-by-hand]` | **In the package.** `ShardedPool._failure_message`, `SQL/ShardedPool.py:2885`; the `EXDEV` branch and its advice "copy it instead, and then delete the source by hand" at `:2911-2914`. The ported test that asserts the text verbatim is `datastorekit/tests/test_copy_move_store.py:599` (`test_move_across_filesystems_fails_before_anything_moves`, the assertion at `:609`). The registry command that passes the advice on stays in SGK. |

## 5. Observations not acted on

1. **No ported test reaches `_assign_shard_keys`** (§4.4 (f)): the shard-key fix that motivated
   the campaign is not pinned by the 88. 03's write-path tests on the stand-in pool are where it
   can be. Not opened as an issue: the plan already gives 03 the write path; recorded for 03's
   author.
2. **Prose in the package still names SGK's layout** (paths such as `Datastore/shard_paths.py` and
   `tools/…`, dotted mentions such as ``Datastore.SQL``, SGK campaign paths `prompts/…` and
   `docs/…`, and "the repository root"). Left unchanged (D-str; README §5 rule 8). Opened as
   `[01-package-prose-names-sgks-layout]`, with the count by file. Two sentences describe the
   bootstrap D-tool removed, and are now false:
   - `tools/sharded_store.py:25-26`: "It puts its own repository root on sys.path, so it runs from
     any directory with no PYTHONPATH."
   - `tools/shard_key_audit.py:25-26`: "the repository root is put on sys.path below so that the
     script still runs standalone, from any directory, with no PYTHONPATH."
3. **The ported fixtures and tests use SGK's table names**: `shard_store_fixtures.py:25-27`
   (`KEY_TYPE = "wavenumber"`, `REPLICATED = ["version", "wavenumber"]`,
   `SHARDED = {"GkSource": "k"}`); `test_shard_key_audit_copy.py` (3 lines) and
   `test_shard_key_audit_refusals.py` (9 lines) create a `wavenumber` table and a
   `wavenumber_serial` column; one comment in `tools/shard_key_audit.py:188` (`e.g. "wavenumber"`).
   `CLAUDE.md` says the package names no client table, and 04's vocabulary guard will be drawn from
   the clients' registries, so it would find these. They are SGK's tests, ported unchanged (rule 6),
   so nothing is changed here. Opened as `[01-ported-tests-use-sgk-table-names]`.
4. **Two placeholder-free f-strings** (§2 item 9) would be flagged by a linter (`F541`). Cosmetic,
   and left for when rule 8 lifts.
5. **`test_shard_paths.TestModuleIsStandalone`** still imports the package through `PYTHONPATH` set
   to the repository root, not through the install. It tests the same files either way; the
   guard's second test does the same with `PYTHONPATH` set to the package's parent.

## 6. Issues opened

- `[01-package-prose-names-sgks-layout]` (§5 item 2).
- `[01-ported-tests-use-sgk-table-names]` (§5 item 3).

Both on the board's §3 and in `docs/OPEN_ISSUES.md` §1.1; the index is at **6 open**.

## 7. State handed to the next prompt

- `HEAD` is `8bc60a5`. The tree is clean; `venv/` exists (Python 3.12.15, `ray==2.43.0`,
  `sqlalchemy==2.0.39`, `black==25.1.0`, `datastorekit` installed editable). `venv/` and
  `datastorekit.egg-info/` are gitignored.
- The suite: **90** (`Ran 90 tests … OK`). 02 records 90 as its "before".
- `compare_with_source.py` exits 0. A prompt that adds a file under `datastorekit/` with no source
  (02's neutral client, the stand-in pool) adds it to `NEW_FILES`, or the check lists it as
  "NOT ACCOUNTED FOR" (a note, not a failure). A file 02–05 port from SGK goes into `FILES`.
- The interfaces of README §4 "After 01": `datastorekit/tests/shard_store_fixtures.py`,
  `datastorekit/tests/test_package_imports.py`, `docs/extraction/compare_with_source.py`,
  `PROVENANCE.md`.
- For 03: no ported test reaches `_assign_shard_keys` (§5 item 1).
- For 04: the vocabulary issue (§5 item 3).
