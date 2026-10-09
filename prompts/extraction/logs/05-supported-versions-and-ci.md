# Log 05 — supported versions and CI, ready for `v0.1.0`

**Subject:** Declare the supported range and add CI for v0.1.0 · **Commit:** this commit ·
**Date:** 2026-10-09 · **Model:** Claude Opus 5.5 · **Result:** landed, untagged and unpushed
(U23).

`pyproject.toml` is at `0.1.0` and declares U6's range (`requires-python = ">=3.12"`,
`ray>=2.43`, `sqlalchemy>=2.0.39,<2.1`). The distribution excludes the test package. A GitHub
Actions workflow, `.github/workflows/tests.yml`, runs the suite at both ends of README §0.2's
version table. The repository's `README.md` says what the package is, what it supports, how a
client installs it and how a client uses it.

The 444 pass in a fresh venv at each end (Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39, and
Python 3.13.16 / Ray 2.55.1 / SQLAlchemy 2.0.46), and in `venv/`. A wheel built from a clean
export holds the layer's 20 files and `LICENSE` and nothing of the tests. Installed into a third
venv and run from outside the repository, it imports every layer module and runs both tools.
`[05-a-refused-open-leaves-its-engines-undisposed]` is opened with §2.6's measurement, the same at
both ends. No file under `datastorekit/` changed. Both checks give 04b's results.

**No tag was made and nothing was pushed (U23).** `v0.1.0` is made on this commit once CI has
passed at both ends here (README §6.2 U23; the board's §2).

Prompt: [`../05-supported-versions-and-ci.md`](../05-supported-versions-and-ci.md), with the
orchestrator's dispatch note §0: five corrections, five additions, its measured facts and the
conventions. Each is followed as given; §2 classifies them.

## 1. What shipped

- **`pyproject.toml`** (§2.1, §2.4), and nothing else in it:

  ```diff
  -version = "0.1.0.dev0"
  +version = "0.1.0"
   ...
  -    "ray",
  -    "sqlalchemy>=2.0",
  +    "ray>=2.43",
  +    "sqlalchemy>=2.0.39,<2.1",
   ...
   include = ["datastorekit*"]
  +exclude = ["datastorekit.tests", "datastorekit.tests.*"]
  ```

  `requires-python = ">=3.12"` is unchanged. No classifier, URL or licence field.
- **`.github/workflows/tests.yml`** (new, §2.5):
  - triggers `push` to `main`, `pull_request` and `workflow_dispatch`;
  - `permissions: contents: read`;
  - one job, `suite`, on `ubuntu-24.04`, with `fail-fast: false` and a matrix of exactly two
    `include` entries:

    | `name` | `python` | `ray` | `sqlalchemy` |
    |---|---|---|---|
    | `low` | `"3.12.15"` | `"2.43.0"` | `"2.0.39"` |
    | `high` | `"3.13.16"` | `"2.55.1"` | `"2.0.46"` |

  - steps:
    1. `actions/checkout@v7`;
    2. `actions/setup-python@v7` with `python-version: ${{ matrix.python }}`;
    3. `python -m pip install --upgrade pip`, then
       `python -m pip install -e . "ray==${{ matrix.ray }}" "sqlalchemy==${{ matrix.sqlalchemy }}"`;
    4. one `python -c` printing `sys.version`, `ray.__version__`, `sqlalchemy.__version__` and
       `sqlite3.sqlite_version`;
    5. `python -m unittest discover -s datastorekit/tests -t .`;
    6. `if: matrix.name == 'low'`: `python -m pip install black==25.1.0` and
       `black --check datastorekit docs`.
  - No secrets, no cache, no artefact upload, no other action. Nothing of hazard 6 runs.
- **`README.md`**, rewritten from its "being extracted" state (§2.7). It keeps the opening
  paragraph, the `RayWorkPool` note and the licence, and gains Status, Supported versions,
  Installing, Using it, The tools and Developing (§5.5 lists every name it mentions).
- **The records**: this log; the board (header, §1's row, §2's G2 line, §3); `docs/OPEN_ISSUES.md`;
  `prompts/INDEX.md`.

Nothing under `datastorekit/` changed, and nothing under `docs/` but `OPEN_ISSUES.md`.
`PROVENANCE.md`, `CLAUDE.md`, `LICENSE`, `.gitignore` and the campaign README are unchanged.

## 2. Deviations from the prompt

1. **Correction 1: every wheel is built from a clean export, never in this checkout.** The release
   check, the final rebuild and breakages (d), (e) and (f) each ran from a fresh directory made by

   ```bash
   git ls-files -z -co --exclude-standard | tar --null -T - -cf - | tar -xf - -C <fresh dir>
   ```

   and `uv build --wheel --out-dir <scratch> <fresh dir>`. Each export held 100 files and no
   `build/` or `*.egg-info` before its build. A breakage was applied in its own export only. The
   agent did not delete the checkout's ignored `build/` or `datastorekit.egg-info/`; the editable
   installs rewrote the second (its `PKG-INFO` said `Version: 0.1.0`), as expected. **Late in the
   run, after the records were drafted, the user had both deleted** (the orchestrator's message
   mid-run; no other change). The agent did not delete them, and made no `build/` or `dist/` in
   the checkout. `venv/`'s suite was run again after the deletion (§5.1, run 9).
   **STRUCTURALLY REQUIRED.**
2. **Correction 2: `shard_key_audit` has no `--help`.** The release check runs it with no argument
   (exit 2, and its usage line names the release venv's `site-packages`) and with `--help` (exit 2,
   `!! No such file: <cwd>/--help`). For both tools,
   `python -c "import datastorekit.tools.<name> as m; print(m.__file__)"` names `site-packages`
   (§5.3). (e) is shown on `sharded_store --help` and on `shard_key_audit` by its message (§6).
   The README's line for that tool is taken from its docstring's first line and its "Usage:" line.
   **STRUCTURALLY REQUIRED.**
3. **Correction 3: (a) runs in a fourth, throwaway venv**, `venv-a`: Python 3.13.16 with
   `ray==2.55.1` and `sqlalchemy==2.0.46` and no package, the suite run from the repository root
   with `PYTHONPATH` unset. The three venvs verified with were never changed (§5.2: their
   `uv pip freeze` is byte-identical before and after (b)–(f)). **STRUCTURALLY REQUIRED.**
4. **Correction 4: the `ResourceWarning` line count is not a measurement.** The plain high-end run
   printed **194** lines (the planner saw 188, the orchestrator 172). §4's wrapper count is the
   measurement: 105 never closed, as the prompt and the orchestrator found. Recorded as found.
   **STRUCTURALLY REQUIRED** (an expectation corrected).
5. **Correction 5: `origin/main` (`47d3ab1`) is 28 commits behind `f69921b`**, the `HEAD` at
   dispatch (`git rev-list --count origin/main..HEAD`), and so 29 behind this commit. This changes
   nothing done here. **STRUCTURALLY REQUIRED** (an expectation corrected).
6. **The matrix pins the patch releases** `"3.12.15"` and `"3.13.16"`, the interpreters tested
   here. `actions/python-versions`' `versions-manifest.json` (read with `gh api`, 2026-10-09)
   lists both as stable, with `python-3.12.15-linux-24.04-x64.tar.gz` and
   `python-3.13.16-linux-24.04-x64.tar.gz`. **IMPLEMENTATION CHOICE**, at the orchestrator's
   direction.
7. **The wheel is recorded by its `RECORD` and `Generator:` line** as well as its SHA-256 (§5.3).
   Two builds of the same tree gave two wheel SHA-256s and byte-identical `RECORD`s, as the
   orchestrator found. **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
8. **`venv/` was reinstalled with its own pip**: `./venv/bin/python -m pip install --no-deps -e .`,
   after which `./venv/bin/pip show datastorekit` says `Version: 0.1.0` (§5.2).
   **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
9. **The README's links were checked**: every relative link names a file or directory that exists,
   and every `#anchor` matches a heading of its target by GitHub's slug rule (§5.5).
   **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
10. **The work followed the orchestrator's order** (pyproject; the two venvs and §2.6; the release
    check; the workflow; the README; (a)–(f); `venv/` again, the checks, `black`, the records),
    with the suite run after each step that changes a file the suite can see (§5.1).
    **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
11. **`uv`'s cache was put in the scratchpad** (`UV_CACHE_DIR=<scratch>/agent05/uv-cache`) for
    every `uv` command, so that every PyPI download landed in the scratchpad (U24).
    **IMPLEMENTATION CHOICE.**
12. **Workflow details the prompt left open**: the job's display name is
    `suite (${{ matrix.name }})`; the matrix's entries are `include` items keyed `name`, `python`,
    `ray`, `sqlalchemy`; steps 3–6 carry names; a two-line comment at the top says the checks
    under `docs/extraction/` run locally only. **IMPLEMENTATION CHOICE.**
13. **README details the prompt left open**:
    - the Ray-on-3.13 sentence names the three Ray releases below 2.45.0 that have no 3.13 wheel
      (2.43.0, 2.44.0, 2.44.1), measured with `uv pip compile` (§5.4);
    - "Using it" gives each item's `docs/client-contract.md` section by anchor, and says the test
      client is not part of the installed package (§2.4's exclusion);
    - "Developing" names `measure_client_vocabulary.py` beside the two checks, since it too reads
      other repositories.

    **IMPLEMENTATION CHOICE.**
14. **(b) was run at the low end and (c) at the high end**, each with `--dry-run` against the
    verified venv (which a dry run does not change). (d) was run with `--dry-run` from its own
    export against the low venv. **IMPLEMENTATION CHOICE.**
15. **The breakage diffs' `git apply -R --check`** was run in each breakage's export after
    `git apply` (the checkout was never broken); `git apply --check` was run both in the checkout,
    against the staged tree, and in the export (§6.1). **IMPLEMENTATION CHOICE.**

No UNINTENDED DRIFT was found.

## 3. The six hazards (§2.2)

1. **The tools' tests need the package installed.** Confirmed by (a): with the pins alone,
   `Ran 444 tests` / `FAILED (failures=19)`, the 19 being exactly the three tool modules' (§6).
   Every venv the suite passed in has the package installed editable, and so does CI's step 3.
   The setuptools editable finder maps the whole `datastorekit/` directory, so
   `datastorekit.tests` stays importable from an editable install despite the exclusion (checked
   from the scratchpad: `datastorekit.tests.__file__` is the checkout's). The exclusion acts on
   the wheel only, which is what is wanted.
2. **SQLite.** Every local run linked SQLite **3.53.4** (low, high, `venv/`). The Linux Python of
   `actions/setup-python` links another, which step 4 prints. The answer is in the CI log after the
   push.
3. **Linux is not measured.** Nothing here stands in for it. All runs were on macOS (Darwin, arm64).
   The tag waits for CI (U23).
4. **The newest versions are not tested.** The README states the two tested ends, says newer
   releases inside the range are allowed but not tested, and says a client pins its own Ray and
   SQLAlchemy. No third job was added.
5. **Python 3.13 reports unclosed connections.** 194 `ResourceWarning` lines in the plain high-end
   run, none at the low end. They are warnings; the workflow sets no `-W error` or
   `PYTHONWARNINGS`. §4 measures them.
6. **The checks cannot run in CI.** The workflow runs the suite and `black --check` only. Both
   checks ran here (§5.6).

## 4. The unclosed connections (§2.6)

**Method.** A scratch runner (`<scratch>/agent05/probe/measure_unclosed.py`, outside the
repository), run from the repository root with each venv's interpreter and `PYTHONPATH` unset:
- `sqlite3.connect` and `sqlite3.dbapi2.connect` are replaced by a wrapper that passes
  `factory=_Tracked`, a subclass of `sqlite3.Connection` (no caller passed a factory of its own:
  the count of those is 0);
- at creation `_Tracked` records the innermost stack frame under `datastorekit/` but not
  `datastorekit/tests/` (the layer's site), the innermost frame under `datastorekit/` at all, the
  outermost `test_*.py` frame (the module that defines the running test method), and the test id
  the runner is running (from `startTest`);
- `close()` marks it closed; `__del__` counts it if it never was;
- the suite runs through `unittest`'s discovery and `TextTestRunner`; after it, `gc.collect()`
  twice, and any tracked connection still alive is reported separately (none was).

The child interpreters of the tools' tests are not wrapped.

**Result, identical at both ends** (the two reports are equal but for `sys.version`):

| End | Tests | Connections opened | Never closed | Alive at the end |
|---|---|---|---|---|
| low (3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39) | 444 OK | 40,874 | **105** | 0 |
| high (3.13.16, Ray 2.55.1, SQLAlchemy 2.0.46) | 444 OK | 40,874 | **105** | 0 |

| Opened at | Never closed | By the module that defines the test |
|---|---|---|
| `SQL/ShardedPool.py:858` (`with self._engine.connect() as conn:`, the primary's schema check) | 58 | `test_reconcile_at_open` 23, `test_prune_at_open` 13, `test_store_schema` 9, `test_version_row_at_open` 8, `test_read_only_pool` 4, `test_declared_facts` 1 |
| `SQL/Datastore.py:349` (`self._inspector = sqla.inspect(self._engine)`) | 41 | `test_version_row_at_open` 41 |
| `SQL/ShardedPool.py:870` (`self._shard_file_table.create(self._engine)`) | 6 | `test_version_row_at_open` 6 |

- **The innermost `datastorekit/` frame** of each of the 105 is the layer's site above: no
  connection left unclosed was opened in the tests' own code, and there is no fourth site.
- **By the running test's module**, the inherited tests of `test_one_timestamp_per_write` (03b)
  appear under it: `Datastore.py:349` 23 + 18, `ShardedPool.py:858` 9 under `test_prune_at_open`
  and 7 under `test_one_timestamp_per_write`, `ShardedPool.py:870` 3 + 3. The table above counts by
  the defining module, as the orchestrator does.
- **The one under `test_declared_facts`** is opened through a helper that module imports from
  `test_prune_at_open` (`_PruneTestCase`, `:55`), so the innermost test file of its stack is
  `test_prune_at_open` (14 by that rule). The outermost is `test_declared_facts`.

This is the prompt's table exactly. Recorded as `[05-a-refused-open-leaves-its-engines-undisposed]`
(§8). Not fixed (rule 8).

## 5. Verification performed

### 5.1 The suite (§3.1)

Each run is `<python> -m unittest discover -s datastorekit/tests -t .` from the repository root,
in the foreground, with `PYTHONPATH` unset, its output written to the scratchpad and the verdict
grepped from it.

| # | When | Venv | Python | Ray | SQLAlchemy | SQLite | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | before any change | `venv/` (`0.1.0.dev0`) | 3.12.15 | 2.43.0 | 2.0.39 | 3.53.4 | `Ran 444 tests in 78.794s` / `OK` |
| 2 | after `pyproject.toml` and the reinstall | `venv/` (`0.1.0`) | 3.12.15 | 2.43.0 | 2.0.39 | 3.53.4 | `Ran 444 tests in 81.939s` / `OK` |
| 3 | step 2 | `venv-low` (scratch) | 3.12.15 | 2.43.0 | 2.0.39 | 3.53.4 | `Ran 444 tests in 85.815s` / `OK` |
| 4 | step 2 | `venv-high` (scratch) | 3.13.16 | 2.55.1 | 2.0.46 | 3.53.4 | `Ran 444 tests in 80.702s` / `OK` |
| 5 | §4, wrapped | `venv-high` | | | | | `Ran 444 tests in 85.296s` / `OK` |
| 6 | §4, wrapped | `venv-low` | | | | | `Ran 444 tests in 89.397s` / `OK` |
| 7 | (a), no package | `venv-a` (throwaway) | 3.13.16 | 2.55.1 | 2.0.46 | | `Ran 444 tests in 78.392s` / `FAILED (failures=19)` |
| 8 | after every change | `venv/` | 3.12.15 | 2.43.0 | 2.0.39 | 3.53.4 | `Ran 444 tests in 83.664s` / `OK` |
| 9 | after the user's deletion of `build/` and `datastorekit.egg-info/` (§2 item 1) | `venv/` | 3.12.15 | 2.43.0 | 2.0.39 | 3.53.4 | `Ran 444 tests in 82.073s` / `OK` |

`sys.version`: low `3.12.15 (main, Oct  3 2026, 08:34:37) [Clang 21.0.0 (clang-2100.3.34.2)]`;
high `3.13.16 (main, Oct  3 2026, 08:14:15) [Clang 21.0.0 (clang-2100.3.34.2)]`; `venv/` as low.

**The count is 444 before and 444 after, in every venv.** `ResourceWarning` lines: 0 in runs 1–3
and 8, 194 in run 4 (and none printed in the wrapped runs 5–6).

The README and the workflow changed after runs 3–4; neither is read by the suite, and runs 8 and
9 are on the final tree.

`uv pip freeze` of each scratch venv (taken before (b)–(f), and byte-identical after):
- **low**: aiosignal 1.4.0, attrs 26.1.0, black 25.1.0, certifi 2026.7.22, charset-normalizer
  3.5.2, click 8.5.0, datastorekit (editable, the checkout), filelock 4.0.12, frozenlist 1.8.0,
  idna 3.20, jsonschema 4.26.0, jsonschema-specifications 2025.9.1, msgpack 1.2.3,
  mypy-extensions 1.1.0, packaging 26.3, pathspec 1.1.1, platformdirs 4.12.4, protobuf 7.36.2,
  pyyaml 6.0.3, ray 2.43.0, referencing 0.37.0, requests 2.34.2, rpds-py 2026.9.1, sqlalchemy
  2.0.39, typing-extensions 4.16.0, urllib3 2.8.0;
- **high**: as low, less aiosignal and frozenlist, with ray 2.55.1 and sqlalchemy 2.0.46;
- **release**: as high, less black, mypy-extensions, pathspec and platformdirs, with
  `datastorekit @ file://…/wheel-release/datastorekit-0.1.0-py3-none-any.whl`.

### 5.2 The installs, and the workflow step each stands for (§2.3, §2.5)

All `uv` commands ran with `UV_CACHE_DIR=<scratch>/agent05/uv-cache` (`uv` 0.12.20). `<scratch>`
is `/private/tmp/claude-35086/-Users-ds283-Documents-Code-DatastoreKit/c3ccb842-7f0a-4f30-8010-09b9494c3df6/scratchpad`.

| Command, as run | Stands for |
|---|---|
| `./venv/bin/python -m pip install --no-deps -e .` (repository root; `Successfully uninstalled datastorekit-0.1.0.dev0`, `Successfully installed datastorekit-0.1.0`) | — (`venv/`'s reinstall, §2.3); `./venv/bin/pip show datastorekit`: `Name: datastorekit`, `Version: 0.1.0`, `Requires: ray, sqlalchemy` |
| `uv venv --python /opt/local/bin/python3.12 <scratch>/agent05/venv-low` | step 2 (`setup-python`, 3.12.15) |
| `uv venv --python /opt/local/bin/python3.13 <scratch>/agent05/venv-high` | step 2 (`setup-python`, 3.13.16) |
| — (`uv` venvs carry no pip) | step 3's `python -m pip install --upgrade pip`: no local counterpart |
| `uv pip install --python <scratch>/agent05/venv-low/bin/python -e . "ray==2.43.0" "sqlalchemy==2.0.39" "black==25.1.0"` (repository root; `Resolved 26 packages`, exit 0) | step 3, low, with step 6's `black` in the same resolve |
| `uv pip install --python <scratch>/agent05/venv-high/bin/python -e . "ray==2.55.1" "sqlalchemy==2.0.46" "black==25.1.0"` (`Resolved 24 packages`, exit 0) | step 3, high |
| `<venv>/bin/python -c "import sys, sqlite3, ray, sqlalchemy; print('python', sys.version); print('ray', ray.__version__); print('sqlalchemy', sqlalchemy.__version__); print('sqlite', sqlite3.sqlite_version)"`, at each end (the workflow's command verbatim) | step 4; output in §5.1 |
| `<venv>/bin/python -m unittest discover -s datastorekit/tests -t .`, at each end | step 5; runs 3 and 4 |
| `<scratch>/agent05/venv-low/bin/black --check datastorekit docs` → `All done!` / `64 files would be left unchanged.`, exit 0 | step 6 (low only) |
| — | step 1 (`actions/checkout@v7`): the checkout itself |

One resolve per end installed the package with its pins, so each end's pins satisfy the declared
range (§2.3).

### 5.3 The release check (§2.4)

**The build**, from a fresh export of the working tree (correction 1), after step 1:
`uv build --wheel --out-dir <scratch>/agent05/wheel-release <scratch>/agent05/export-release`, exit
0.

| | |
|---|---|
| Wheel | `datastorekit-0.1.0-py3-none-any.whl` |
| Size | 96,304 bytes |
| Entries | 25 |
| SHA-256 | `748515c47ee45732f0e56505a427e54a9bcb5317972a3ee26831c4f4a16e6d11` |
| `RECORD` SHA-256 | `a689847ec47869c479304270fe5c4709595c35668136cb1e7f134fedd652330a` |
| `WHEEL` | `Generator: setuptools (84.0.0)` |
| `METADATA` | `Name: datastorekit`, `Version: 0.1.0`, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43`, `Requires-Dist: sqlalchemy<2.1,>=2.0.39` |

**Rebuilt from a fresh export of the final tree** (README and workflow included, before the
records): 96,304 bytes, 25 entries, SHA-256
`ca165eca15fdc0c45277064bb945c5f1f2dd9384221348de33c31e28728c59d0`, and the **same `RECORD`**
(`a689847e…652330a`, byte-identical) and the same file list. Only the zip's timestamps differ.

**The file list** (25 entries, none under `datastorekit/tests/`):

```
datastorekit/__init__.py
datastorekit/_timing.py
datastorekit/contract.py
datastorekit/defaults.py
datastorekit/object.py
datastorekit/replication.py
datastorekit/shard_paths.py
datastorekit/store_inventory.py
datastorekit/store_reader.py
datastorekit/SQL/ClientPool.py
datastorekit/SQL/Datastore.py
datastorekit/SQL/ProfileAgent.py
datastorekit/SQL/SerialPoolBroker.py
datastorekit/SQL/ShardedPool.py
datastorekit/SQL/__init__.py
datastorekit/SQL/factory_base.py
datastorekit/SQL/schema.py
datastorekit/tools/__init__.py
datastorekit/tools/shard_key_audit.py
datastorekit/tools/sharded_store.py
datastorekit-0.1.0.dist-info/licenses/LICENSE
datastorekit-0.1.0.dist-info/METADATA
datastorekit-0.1.0.dist-info/WHEEL
datastorekit-0.1.0.dist-info/top_level.txt
datastorekit-0.1.0.dist-info/RECORD
```

Its 20 `.py` files are exactly the guard's `layer_files()` (20; every one in the wheel, and no
other `.py` in it), checked with `datastorekit.tests.test_layer_is_generic.layer_files` from
`venv/`.

**The install**: `uv venv --python /opt/local/bin/python3.13 <scratch>/agent05/venv-release`, then
`uv pip install --python <scratch>/agent05/venv-release/bin/python <the wheel> "ray==2.55.1"
"sqlalchemy==2.0.46"` (`Resolved 20 packages`, exit 0), not editable.

**The commands**, run by `<scratch>/agent05/probe/release_check.sh` from
`<scratch>/agent05/outside-release` (a directory outside the repository) with `PYTHONPATH` unset.
`<R>` is `<scratch>/agent05/venv-release/lib/python3.13/site-packages`:

```
$ python -c "<import each of the 20 layer modules, print each __file__>"
datastorekit <R>/datastorekit/__init__.py
datastorekit._timing <R>/datastorekit/_timing.py
datastorekit.contract <R>/datastorekit/contract.py
datastorekit.defaults <R>/datastorekit/defaults.py
datastorekit.object <R>/datastorekit/object.py
datastorekit.replication <R>/datastorekit/replication.py
datastorekit.shard_paths <R>/datastorekit/shard_paths.py
datastorekit.store_inventory <R>/datastorekit/store_inventory.py
datastorekit.store_reader <R>/datastorekit/store_reader.py
datastorekit.SQL <R>/datastorekit/SQL/__init__.py
datastorekit.SQL.ClientPool <R>/datastorekit/SQL/ClientPool.py
datastorekit.SQL.Datastore <R>/datastorekit/SQL/Datastore.py
datastorekit.SQL.ProfileAgent <R>/datastorekit/SQL/ProfileAgent.py
datastorekit.SQL.SerialPoolBroker <R>/datastorekit/SQL/SerialPoolBroker.py
datastorekit.SQL.ShardedPool <R>/datastorekit/SQL/ShardedPool.py
datastorekit.SQL.factory_base <R>/datastorekit/SQL/factory_base.py
datastorekit.SQL.schema <R>/datastorekit/SQL/schema.py
datastorekit.tools <R>/datastorekit/tools/__init__.py
datastorekit.tools.shard_key_audit <R>/datastorekit/tools/shard_key_audit.py
datastorekit.tools.sharded_store <R>/datastorekit/tools/sharded_store.py
20 modules imported
exit=0

$ python -c "import datastorekit.tests"
ModuleNotFoundError: No module named 'datastorekit.tests'
exit=1

$ python -c "import datastorekit.tools.sharded_store as m; print(m.__file__)"
<R>/datastorekit/tools/sharded_store.py
exit=0

$ python -c "import datastorekit.tools.shard_key_audit as m; print(m.__file__)"
<R>/datastorekit/tools/shard_key_audit.py
exit=0

$ python -m datastorekit.tools.sharded_store --help
exit=0
usage: python -m datastorekit.tools.sharded_store [-h] {copy,move} src dst

Copy or move a closed ShardedPool datastore under a new name.
... (35 lines)

$ python -m datastorekit.tools.shard_key_audit
usage: <R>/datastorekit/tools/shard_key_audit.py <path-to-primary-database>
exit=2

$ python -m datastorekit.tools.shard_key_audit --help
!! No such file: <scratch>/agent05/outside-release/--help
exit=2

$ <the wheel file list>
25 entries; 0 under datastorekit/tests/; 3 under datastorekit/tools/
```

The release check passes. The wheel, the exports and the venvs are in the scratchpad only. No
`dist/` appeared in the checkout (§5.8).

### 5.4 The workflow (§2.5, §3.4)

- **Parses as YAML**: `<scratch>/agent05/venv-high/bin/python -c "import yaml, sys;
  yaml.safe_load(open(sys.argv[1]))" .github/workflows/tests.yml` exits 0 (PyYAML 6.0.3, from the
  high venv, by Ray's dependency).
- **Its structure, read back from the parse**: triggers `{'push': {'branches': ['main']},
  'pull_request': None, 'workflow_dispatch': None}` (PyYAML reads the key `on` as `True`, YAML
  1.1; GitHub reads it as `on`); `permissions: {'contents': 'read'}`; one job, `suite`;
  `runs-on: ubuntu-24.04`; `fail-fast: False`; the only actions `actions/checkout@v7` and
  `actions/setup-python@v7`.
- **The matrix equals §2.3's table**, with the patch Pythons (addition 1): the parsed `include`
  list is `==` to `[{name: low, python: "3.12.15", ray: "2.43.0", sqlalchemy: "2.0.39"}, {name:
  high, python: "3.13.16", ray: "2.55.1", sqlalchemy: "2.0.46"}]` → `True`.
- **The Actions** (`gh api repos/actions/<name>/releases/latest`, 2026-10-09): `checkout`
  `v7.0.1`, `setup-python` `v7.0.0`. `ds283/DatastoreKit` is `public`, default branch `main`;
  `actions/permissions` gives `enabled: true`, `allowed_actions: all`. Read only.
- **The replay** of steps 3–6 at both ends is §5.2.
- **The pins resolve on Linux** (`uv pip compile --only-binary ray --python-platform …`, from the
  scratchpad): low on 3.12 and high on 3.13 resolve on `x86_64-manylinux_2_28` and
  `aarch64-apple-darwin`. On 3.13, `ray==2.43.0`, `2.44.0` and `2.44.1` have no solution on either
  platform, and `ray==2.45.0` resolves on both (the README's sentence).

### 5.5 The README (§2.7)

Every name the README mentions, checked by `<scratch>/agent05/probe/readme_check.py`, run with
`./venv/bin/python` from the repository root (exit 0):

| Name | How checked |
|---|---|
| `datastorekit.SQL.ShardedPool.ShardedPool` | imported (a class) |
| its `factories=` argument | `inspect.signature(ShardedPool.__init__)`: `KEYWORD_ONLY` |
| `datastorekit.SQL.factory_base.SQLAFactoryBase` | imported |
| the hooks `register`, `build`, `store`, `validate`, `validate_on_startup`, `revalidate`, `owned_serials`, `inventory_spec` | `hasattr(SQLAFactoryBase, …)`, all `True` |
| `datastorekit.store_inventory.InventorySpec`, `Parent`, `ParentSet` | imported |
| `datastorekit.contract` naming `version` and `store_tag` | `VERSION_TABLE == "version"`, `TAG_TABLE == "store_tag"` |
| `datastorekit/tests/client/registry.py` (the registry module) | `datastorekit.tests.client.registry.factories` imported (a dict) |
| `python -m datastorekit.tools.sharded_store {copy,move} SRC DST` | `datastorekit.tools.sharded_store.main` imported; the line is its `--help` usage and description (§5.3) |
| `python -m datastorekit.tools.shard_key_audit /path/to/primary.sqlite` | `datastorekit.tools.shard_key_audit.main` imported; the line is its docstring's "Usage:" line and first line (correction 2) |
| `register()` returning `None`; `pip install -e`; the Developing commands | `docs/client-contract.md` §2; CLAUDE.md's test command; `venv/` was made this way (log 01 §3) |

**Links** (all exist; anchors by GitHub's slug rule against the target's headings):
`PROVENANCE.md`; `prompts/extraction/README.md`; `prompts/extraction/IMPLEMENTATION_STATE.md`;
`.github/workflows/tests.yml`; `docs/client-contract.md` and its anchors
`#1-the-pools-constructor`, `#2-the-keys-of-register`, `#3-the-factory-hooks`,
`#4-the-inventorys-declarations`, `#5-the-layers-own-tables`,
`#7-the-other-entry-points-that-take-client-facts`; `datastorekit/tests/client/` (a directory);
`datastorekit/tests/client/registry.py`; `docs/extraction/` (a directory); `LICENSE`. Two are
external: `https://www.ray.io/` (kept from before) and `https://github.com/ds283/SecondaryGWKit`
(kept from before).

**Its versions equal `pyproject.toml`'s and the workflow's**: declared `>=3.12`, `>=2.43`,
`>=2.0.39,<2.1`; tested 3.12.15 / 2.43.0 / 2.0.39 and 3.13.16 / 2.55.1 / 2.0.46. The install line
is CLAUDE.md's, at `v0.1.0`, written as of the tag (U23).

### 5.6 The two checks (§3.2)

At dispatch and after every change, from `venv/`; the two outputs are byte-identical:

- `compare_with_source.py`: exit 0; `files compared: 31`, `files ported, checked by
  compare_ported_tests.py: 20`, `files with no source, declared: 10`, `OK: every differing line
  is classified, and every file is accounted for`.
- `compare_ported_tests.py`: exit 0; `OK: 20 module(s) keep their source's tests, classes and
  assertion skeletons; 1 test(s) declared not ported`.

### 5.7 `black` (§3.6)

`./venv/bin/black --check datastorekit docs` (25.1.0): `64 files would be left unchanged.`, before
and after; and from the low scratch venv (§5.2). No Python file changed.

### 5.8 The tree

`git status --short --ignored` at dispatch:

```
!! .idea/
!! build/
!! datastorekit.egg-info/
!! datastorekit/SQL/__pycache__/
!! datastorekit/__pycache__/
!! datastorekit/tests/__pycache__/
!! datastorekit/tests/client/__pycache__/
!! docs/extraction/__pycache__/
!! venv/
```

After the work, before the records were written (staged):

```
A  .github/workflows/tests.yml
M  README.md
M  pyproject.toml
!! .idea/
!! build/
!! datastorekit.egg-info/
!! datastorekit/SQL/__pycache__/
!! datastorekit/__pycache__/
!! datastorekit/tests/__pycache__/
!! datastorekit/tests/client/__pycache__/
!! docs/extraction/__pycache__/
!! venv/
```

The same ignored entries; no `dist/`, no new `*.egg-info`.

**After the user's deletion of `build/` and `datastorekit.egg-info/`** (§2 item 1), with the log
written and before the board's records, as found:

```
A  .github/workflows/tests.yml
M  README.md
M  pyproject.toml
?? prompts/extraction/logs/05-supported-versions-and-ci.md
!! .idea/
!! datastorekit/SQL/__pycache__/
!! datastorekit/__pycache__/
!! datastorekit/tests/__pycache__/
!! datastorekit/tests/client/__pycache__/
!! docs/extraction/__pycache__/
!! venv/
```

No `build/`, `dist/` or `*.egg-info` (no editable install was made after the deletion). The
records of this commit add no ignored entry. No Ray process was up at any point
(`pgrep -lf 'gcs_server|raylet|ray::'` empty, before and after). Every store the suite made was in
a `tempfile` directory.

## 6. The deliberate-breakage record (§3.7)

### 6.1 The method

- **(a)–(c)** change no file. (a) installs into the throwaway `venv-a`; (b) and (c) are
  `uv pip install --dry-run` against the verified venvs, whose `uv pip freeze` was compared before
  and after (byte-identical).
- **(d)–(f)** are diffs to `pyproject.toml`. With this prompt's three files staged, each was made
  by editing the file, taking `git diff pyproject.toml` against the index, and restoring the file
  with `git checkout -- pyproject.toml`. `git apply --check` passed in the checkout. Each was then
  run by `<scratch>/agent05/probe/run_break.sh` in a **fresh export** of the checkout (correction
  1): `git apply --check`, `git apply`, `git apply -R --check`, the run, `git apply -R`. The
  checkout was never broken; `git status` was the staged three files after each.
- The diffs below are the files applied, byte for byte, trailing context lines included. They
  were extracted from this log after it was written and checked again both ways, in a fresh
  export (§6.3). Their `index` line names the staged blob `5bca032`, which is this commit's
  `pyproject.toml`.

### 6.2 The breakages

**(a) The workflow's install without the package.** In `venv-a` (Python 3.13.16):
`uv pip install --python <scratch>/agent05/venv-a/bin/python "ray==2.55.1" "sqlalchemy==2.0.46"`
(`Resolved 19 packages`, no `datastorekit`), then the suite from the repository root with
`PYTHONPATH` unset: **`Ran 444 tests in 78.392s` / `FAILED (failures=19)`**, all failures, no
errors; 21 lines say `No module named 'datastorekit'`. The 19:
- `test_shard_key_audit_refusals.TestTheAuditRefuses` (11): `test_a_current_store_is_still_audited`,
  `test_a_primary_naming_another_stores_shards_by_absolute_path`,
  `test_a_primary_naming_its_own_siblings_by_absolute_path`,
  `test_a_primary_whose_shard_key_config_is_empty`, `test_a_primary_without_shard_key_config`,
  `test_a_record_that_is_unusable_in_a_later_shard_is_refused_too`,
  `test_a_shard_0_that_is_not_a_database`, `test_a_shard_0_without_the_shard_key_table`,
  `test_a_shard_key_config_without_key_type`, `test_a_shard_keys_table_without_key_serial`,
  `test_a_shards_table_without_filename`;
- `test_shard_key_audit_copy.TestAuditOfACopiedStore` (3):
  `test_audit_does_not_fall_back_to_the_original_when_the_copy_lacks_shard_0`,
  `test_audit_of_the_copy_attaches_the_copys_shard`, `test_tool_imports_no_heavy_dependency`;
- `test_sharded_store_script.TestShardedStoreScript` (5):
  `test_copy_succeeds_from_another_directory_without_pythonpath`,
  `test_help_carries_the_three_statements`, `test_move_succeeds`,
  `test_ray_is_imported_but_never_initialised`, `test_refusal_exits_nonzero_and_writes_nothing`.

**(b) The SQLAlchemy floor.** `uv pip install --dry-run --python <scratch>/agent05/venv-low/bin/python
-e . "ray==2.43.0" "sqlalchemy==2.0.38"` (repository root): exit **1**,

```
error: No solution found when resolving dependencies
  cause: Because only datastorekit==0.1.0 is available and datastorekit==0.1.0 depends on sqlalchemy>=2.0.39,<2.1, we can conclude that all versions of datastorekit depend on sqlalchemy>=2.0.39,<2.1.
         And because you require sqlalchemy==2.0.38 and datastorekit, we can conclude that your requirements are unsatisfiable.
```

**(c) The SQLAlchemy cap.** `uv pip install --dry-run --python <scratch>/agent05/venv-high/bin/python
-e . "ray==2.55.1" "sqlalchemy==2.1.4"`: exit **1**,

```
error: No solution found when resolving dependencies
  cause: Because only datastorekit==0.1.0 is available and datastorekit==0.1.0 depends on sqlalchemy>=2.0.39,<2.1, we can conclude that all versions of datastorekit depend on sqlalchemy>=2.0.39,<2.1.
         And because you require sqlalchemy==2.1.4 and datastorekit, we can conclude that your requirements are unsatisfiable.
```

**(d) The Python floor.** The diff:

```diff
diff --git a/pyproject.toml b/pyproject.toml
index 5bca032..5d30668 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -6,7 +6,7 @@ build-backend = "setuptools.build_meta"
 name = "datastorekit"
 version = "0.1.0"
 description = "A sharded SQLite datastore layer (Datastore / ShardedPool) on Ray and SQLAlchemy"
-requires-python = ">=3.12"
+requires-python = ">=3.13"
 dependencies = [
     "ray>=2.43",
     "sqlalchemy>=2.0.39,<2.1",
```

Applied in its export, `uv pip install --dry-run --python <scratch>/agent05/venv-low/bin/python -e .
"ray==2.43.0" "sqlalchemy==2.0.39" "black==25.1.0"` from the export: exit **1**,

```
error: No solution found when resolving dependencies
  cause: Because the current Python version (3.12.15) does not satisfy Python>=3.13 and datastorekit==0.1.0 depends on Python>=3.13, we can conclude that datastorekit==0.1.0 cannot be used.
         And because only datastorekit==0.1.0 is available and you require datastorekit, we can conclude that your requirements are unsatisfiable.
```

**(e) An exclusion too broad.** The diff:

```diff
diff --git a/pyproject.toml b/pyproject.toml
index 5bca032..f74fc0f 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -14,4 +14,4 @@ dependencies = [
 
 [tool.setuptools.packages.find]
 include = ["datastorekit*"]
-exclude = ["datastorekit.tests", "datastorekit.tests.*"]
+exclude = ["datastorekit.t*"]
```

Built from its export: 90,695 bytes, **22 entries, none under `datastorekit/tools/` or
`datastorekit/tests/`**. Installed into a fresh `venv-e` at the high pins, the release check
**fails**:
- the module loop stops at `ModuleNotFoundError: No module named 'datastorekit.tools'`, exit 1;
- `python -m datastorekit.tools.sharded_store --help`: **exit 1**, `Error while finding module
  specification for 'datastorekit.tools.sharded_store' (ModuleNotFoundError: No module named
  'datastorekit.tools')`;
- `python -m datastorekit.tools.shard_key_audit`, with no argument and with `--help`: exit 1, the
  same message for `datastorekit.tools.shard_key_audit`, in place of the usage line and the "No
  such file" line;
- `import datastorekit.tests` also raises `ModuleNotFoundError`.

**(f) The test package shipped.** The diff:

```diff
diff --git a/pyproject.toml b/pyproject.toml
index 5bca032..dd5ab8a 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -14,4 +14,3 @@ dependencies = [
 
 [tool.setuptools.packages.find]
 include = ["datastorekit*"]
-exclude = ["datastorekit.tests", "datastorekit.tests.*"]
```

Built from its export: 283,617 bytes, **66 entries, 41 under `datastorekit/tests/`**. Installed into
a fresh `venv-f` at the high pins, the release check **fails**: `python -c "import
datastorekit.tests"` **exits 0**, and the wheel lists files under `datastorekit/tests/`. Everything
else passes as in §5.3 (20 modules import; `sharded_store --help` exit 0; `shard_key_audit` exit
2 with the usage line and the "No such file" line).

### 6.3 The diffs, replayed from this log

The three diffs were extracted from this file; each is byte-identical to the file applied. In a
fresh export of the staged tree, each was checked with `git apply --check`, applied, checked with
`git apply -R --check`, and reversed: all passed. `git apply --check` of each also passed in the
checkout, which was left unchanged.

## 7. Observations not acted on

1. **CI resolves the transitive dependencies afresh.** Only Python, Ray and SQLAlchemy are pinned;
   `pip` picks the newest allowed `protobuf`, `msgpack`, `click` and the rest on each CI run, as
   `uv` did here on 2026-10-09 (§5.1's freeze). A CI failure at an end could come from one of
   them. Not a defect; the workflow is §2.5's.
2. **The wrapped runs printed no `ResourceWarning`**, though they counted 105 unclosed at the high
   end, while the plain high-end run printed 194 lines. The count is the measurement (correction
   4); why the warning lines vanish under the `factory=` subclass was not investigated.
3. **`shard_key_audit` takes `--help` as a path** (correction 2). Frozen by rule 8; for the prose
   and tool rewrite after 05 to consider.
4. **The editable install exposes `datastorekit.tests`** (§3 hazard 1). Intended, and what lets the
   suite and its child interpreters run; noted so that no one reads it as the exclusion failing.

## 8. Issues

- **Opened: `[05-a-refused-open-leaves-its-engines-undisposed]`** (§4; the board's §3).
- **Closed, narrowed, changed:** none. `[01-package-prose-names-sgks-layout]` is unchanged: no file
  under `datastorekit/` changed.

The index goes from **6 to 7 open**: 3 on this board, 4 inherited.

## 9. State handed to the next prompt

- `HEAD` is this commit. The tree is clean. `venv/` has `datastorekit 0.1.0` installed editable
  (with its own pip), and is otherwise unchanged. The checkout has no `build/` and no
  `datastorekit.egg-info/` (deleted at the user's direction mid-run, §2 item 1); a later editable
  install may recreate the second.
- **Not pushed, not tagged (U23).** `origin/main` is `47d3ab1`, 29 commits behind this commit.
  Next, after the review: the user pushes `main` (or approves the orchestrator's doing so); the
  workflow runs at both ends on this commit; **only if both pass** is `v0.1.0` made here,
  annotated, and pushed. A red end means a fix prompt first, and no tag on this commit.
- **What the CI log must be read for:** each end's step 4 (the Linux SQLite version, hazard 2) and
  each end's `Ran 444 tests … OK`.
- **The suite is 444** at both ends and in `venv/`. 06 records 444 as its "before".
- **The checks**: `compare_with_source.py` 31 / 20 / 10, exit 0; `compare_ported_tests.py` twenty
  modules, one test declared not ported, exit 0.
- **Rule 8 lifts after this prompt** (README §5): 06 adds behaviour only behind a `register()` key.
- **The wheel's `RECORD`**: SHA-256 `a689847ec47869c479304270fe5c4709595c35668136cb1e7f134fedd652330a`
  (`Generator: setuptools (84.0.0)`), for the review's rebuild from a clean export.
- **Scratch** (not in the repository): `<scratch>/agent05/` holds the venvs (`venv-low`,
  `venv-high`, `venv-release`, `venv-a`, `venv-e`, `venv-f`), the exports, the wheels, `uv`'s cache
  and the probes (`measure_unclosed.py`, `release_check.sh`, `run_break.sh`, `readme_check.py`).
