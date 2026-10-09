# Prompt 05 — supported versions and CI, ready for `v0.1.0`

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 04b landed (`0c66505`), and its review was recorded (`18c102c`).
- U6, U23 and U24 are taken (README §6.2, 2026-10-09).
- `git status` is clean in this repository.

**Closes:** nothing. **Narrows:** nothing. **Changes:** nothing.
**Opens:** `[05-a-refused-open-leaves-its-engines-undisposed]` (§2.6), and anything else the work
finds.

**Recommended model:** **Opus.**
- The code is small: `pyproject.toml`, one workflow file and the README.
- Its weight is in running the suite in three new places: a fresh venv at each end of the version
  table, and an installed wheel. Each fails in its own way if it is set up wrongly, and the
  failures look like the layer's (§2.2, hazard 1).

**Read first:**

1. [`README.md`](README.md): §0.2 (the runtime versions), §1, §2 (rows 05 and 06), §4, §5 (rules
   7, 8 and 10 especially), §6.2 (U4, U6, U23 and U24) and §7 (G2).
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`, above all "Releases" and "Repository
   mechanics".
3. The board, with the review of 04b. Then
   [`logs/04b-port-the-declaration-and-registry-tests.md`](logs/04b-port-the-declaration-and-registry-tests.md)
   §10, and [`logs/01-import-the-layer.md`](logs/01-import-the-layer.md) on how `venv/` was built.
4. The repository as 04b left it:
   - `pyproject.toml`, `README.md`, `PROVENANCE.md`, `.gitignore`;
   - `docs/client-contract.md`, which the README's usage points at;
   - `datastorekit/tests/test_package_imports.py`, `test_sharded_store_script.py`,
     `test_shard_key_audit_copy.py` and `test_shard_key_audit_refusals.py`, the tests that run a
     child interpreter;
   - `datastorekit/tests/client/`, the worked example of a client.

Facts below are at `18c102c` (the package unchanged since `0c66505`), measured on 2026-10-09.

---

## 1. What is wanted

05 makes the package ready to be released as `v0.1.0`, the release SGK adopts (G2). After it:

- `pyproject.toml` declares the supported range (U6) and the version `0.1.0`;
- the distribution holds the layer and its two tools, and not the test package (§2.4);
- a GitHub Actions workflow runs the 444 at both ends of §0.2's version table;
- the repository's `README.md` says what the package is, what it supports, how a client installs
  it, and how a client uses it;
- **the suite has run, and passed, in a fresh venv at each end, and the layer and its tools work
  from an installed wheel**, all on this machine, before anything reaches GitHub.

**05 makes no tag and pushes nothing (U23).** After its review, the user pushes `main`, or approves
the orchestrator's doing so. CI must then pass at both ends on 05's commit, and only then is
`v0.1.0` made, annotated, on that commit, and pushed. If CI fails, a fix prompt lands first; no
tag is ever made on a commit whose CI is red, since rule 10 forbids moving one. The tag is not this
prompt's work, and the orchestrator's note says how it is made.

**No behaviour of the layer changes.** No file under `datastorekit/` is touched (README §5 rule 8),
so `compare_with_source.py` and `compare_ported_tests.py` give 04b's results. The suite stays at
**444**: 05 adds no test.

---

## 2. What to change

### 2.1 `pyproject.toml` (U6)

- `version = "0.1.0"` (from `"0.1.0.dev0"`).
- `requires-python = ">=3.12"`, unchanged.
- `dependencies = ["ray>=2.43", "sqlalchemy>=2.0.39,<2.1"]`.
  - **No Ray ceiling**, so that a client can move Ray without a release here. The two ends are
    what CI tests; the README says so.
  - **SQLAlchemy is capped below 2.1**, which exists (2.1.4 on PyPI today) and is a minor series
    with breaking changes.
- The package list, per §2.4.
- Nothing else. No classifiers, URLs or licence field are asked for: `setuptools>=64`'s licence
  handling differs across versions, and the `LICENSE` file is already in the wheel.

### 2.2 What the planner measured

On this machine (macOS, arm64), from the session scratchpad, with nothing in the repository
written:

- **The low end is `venv/`:** Python 3.12.15, `ray` 2.43.0, `sqlalchemy` 2.0.39, SQLite 3.53.4,
  the package installed editable (01). `Ran 444 tests … OK`, with no `ResourceWarning`.
- **The high end** is a scratch venv made with `uv` from MacPorts' `/opt/local/bin/python3.13`
  (3.13.16), with `ray==2.55.1`, `sqlalchemy==2.0.46` and `black==25.1.0` from PyPI. Its SQLite is
  3.53.4 as well.
  - With the repository on `PYTHONPATH` only, 19 tests fail (hazard 1).
  - With the package installed editable (`uv pip install --no-deps -e .`): **`Ran 444 tests …
    OK`**, with 188 lines of `ResourceWarning` (hazard 5).
- **Linux wheels exist for both ends.** `uv pip compile --python-platform x86_64-manylinux_2_28`
  resolves `ray==2.43.0` with `sqlalchemy==2.0.39` on 3.12, and `ray==2.55.1` with
  `sqlalchemy==2.0.46` on 3.13.
  - **Ray 2.43.0 has no wheel for 3.13.** The first release with one is 2.45.0, on Linux and on
    macOS. So on 3.13 the declared floor is in effect 2.45.
- **The newest releases today** are `ray` 2.59.0, `sqlalchemy` 2.0.54 in the 2.0 series, and 2.1.4.
  An unpinned install inside the declared range resolves to the first two, neither of which is
  tested (hazard 4).
- **The wheel**, built from the tree with `uv build --wheel`, holds 66 entries. 41 of them are
  under `datastorekit/tests/`, but neither `tests/data/` file is among them (§2.4).
- **The two Actions**, by `gh api repos/actions/<name>/releases/latest`: `actions/checkout`
  `v7.0.1` and `actions/setup-python` `v7.0.0`. Actions are enabled on `ds283/DatastoreKit`, which
  is public, with default branch `main`. `origin/main` is at `47d3ab1`, 26 commits behind local
  `main` at `18c102c`.

**Hazards.** Check each, and say in the log what you found.

1. **The tools' tests need the package installed.** `test_sharded_store_script`,
   `test_shard_key_audit_copy` and `test_shard_key_audit_refusals` run `python -m
   datastorekit.tools.…` in a child interpreter. Some of them clear `PYTHONPATH` and change
   directory on purpose (`test_copy_succeeds_from_another_directory_without_pythonpath`). Without
   an install, the 19 fail with `No module named 'datastorekit'`. Every venv you run the suite in
   has the package installed, editable, and so does CI.
2. **SQLite.** The suite has only ever run on SQLite 3.53.4. Five places use `ALTER TABLE … DROP
   COLUMN` (`test_shard_key_audit_refusals.py:213`, `real_store_fixtures.py:260`, `:758`,
   `test_store_schema.py:340`, `:469`), and 04a's hazard 6 depended on how SQLite refuses one. The
   Python that `actions/setup-python` installs on `ubuntu-24.04` links a SQLite this machine
   cannot test. The workflow prints `sqlite3.sqlite_version` at each end; the log of the CI run
   (after the push) is where the answer is.
3. **Linux is not measured.** The tests were written and run on macOS: temporary directories under
   `/private/var`, and a case-insensitive file system. CI is the first Linux run. Nothing here can
   stand in for it, which is why the tag waits for it (U23).
4. **The newest versions are not tested.** The README states the two tested ends and says that a
   client pins its own Ray and SQLAlchemy. A third CI job for "the newest allowed" was not chosen
   (U6), and is not added.
5. **Python 3.13 reports unclosed connections** (§2.6). They are warnings; they do not fail a
   test, and CI must not be configured to treat them as errors.
6. **The checks cannot run in CI.** `compare_with_source.py`, `compare_ported_tests.py` and
   `measure_client_vocabulary.py` read SGK, CPBH and SI through `git`. They run here, as every
   prompt runs them. The workflow runs the suite and `black --check`, and nothing that needs a
   client.

### 2.3 The fresh venvs, at both ends (U24)

Make two venvs **in the session scratchpad**, never under the repository, with `uv`:

| End | Interpreter | Pins |
|---|---|---|
| low | `/opt/local/bin/python3.12` | `ray==2.43.0`, `sqlalchemy==2.0.39`, `black==25.1.0` |
| high | `/opt/local/bin/python3.13` | `ray==2.55.1`, `sqlalchemy==2.0.46`, `black==25.1.0` |

- In each, install the package **editable, together with its pins, in one resolve**:
  `uv pip install --python <venv>/bin/python -e . "ray==…" "sqlalchemy==…" "black==25.1.0"`.
  This is the workflow's install step (§2.5). One resolve also checks that the pins satisfy
  `pyproject.toml`'s declared range.
- Run the suite from the repository root with each venv's interpreter. Both must give `Ran 444
  tests … OK`. Record each venv's `sys.version`, `ray.__version__`, `sqlalchemy.__version__` and
  `sqlite3.sqlite_version`.
- U24 allows downloads from PyPI into the scratchpad for this, and for §2.4's build. It allows
  nothing else. The project's `venv/` is not rebuilt. After §2.1, reinstall the package in it
  editable with `--no-deps`, so that its metadata says `0.1.0`, and run the suite there too.

### 2.4 The distribution

`[tool.setuptools.packages.find]` keeps `include = ["datastorekit*"]` and gains
`exclude = ["datastorekit.tests", "datastorekit.tests.*"]`.
- **Why:** the test package is not a client's to import. It needs this repository's data files,
  which the wheel does not carry, so shipped it cannot run, and the guard's data names three
  clients' tables.
- **Check it does not break the editable installs.** The suite imports `datastorekit.tests` from
  the repository root (`-t .`), and the child interpreters that import the client get
  `PYTHONPATH` at the repository root. Run the whole suite in all three venvs after the change.

**The release check.** Build the wheel from the tree with `uv build --wheel --out-dir <scratch>`.
Install it, not editable, into a third fresh scratch venv, at the high end's pins. Then, from a
directory outside the repository, with `PYTHONPATH` unset:
- `import datastorekit` and every layer module import (the 20 of the guard's `layer_files()`, as
  module names);
- `python -m datastorekit.tools.sharded_store --help` and `python -m
  datastorekit.tools.shard_key_audit --help` exit 0;
- `import datastorekit.tests` raises `ModuleNotFoundError`;
- the wheel's file list holds the 20 layer files, `LICENSE`, and nothing under `datastorekit/tests/`.

Record the wheel's name, size, entry count and SHA-256, and each command's output. The wheel is not
committed, and neither is `build/`, `dist/` or any `*.egg-info` (`.gitignore` covers them; check
`git status`).

### 2.5 The workflow

`.github/workflows/tests.yml`:
- **Triggers:** `push` to `main`, `pull_request`, and `workflow_dispatch`.
- **One job, `suite`, on `ubuntu-24.04`**, with a matrix of exactly two entries, named `low` and
  `high`, holding §2.3's Python, Ray and SQLAlchemy versions. `fail-fast: false`, so that one end's
  failure does not hide the other's.
- **Steps:**
  1. `actions/checkout@v7`;
  2. `actions/setup-python@v7`, with the matrix's Python;
  3. `python -m pip install --upgrade pip`, then
     `python -m pip install -e . "ray==${{ matrix.ray }}" "sqlalchemy==${{ matrix.sqlalchemy }}"`;
  4. print `sys.version`, `ray.__version__`, `sqlalchemy.__version__` and
     `sqlite3.sqlite_version` (hazard 2);
  5. `python -m unittest discover -s datastorekit/tests -t .`;
  6. on `low` only: `python -m pip install black==25.1.0` and `black --check datastorekit docs`.
- **Permissions:** `contents: read`. No secrets, no cache, no artefact upload, no other action.
- It runs nothing of §2.2's hazard 6.

**Replay it here.** The steps can't be run by GitHub from this machine, so run steps 3–6 by hand,
with `uv` in place of `pip`, in §2.3's venvs. The log records the commands as run, and which step
of the workflow each stands for. A workflow step with no local counterpart is named in the log.

Validate the file as YAML: `python -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))"`, with
PyYAML from one of the scratch venvs, since Ray depends on it. Check also that the matrix's values
equal §2.3's table.

### 2.6 The unclosed connections, recorded (rule 8)

Under Python 3.13, `sqlite3` warns when a connection is garbage-collected unclosed. The planner
attributed them with a scratch wrapper. It replaced `sqlite3.connect` and `sqlite3.dbapi2.connect`
(SQLAlchemy calls the second) with a `factory=` subclass that records the stack at creation and
counts, on `__del__`, those never closed. Over the 444 at the high end, **105** connections are
never closed. All of them are opened by the layer's engines:

| Opened at | Count | In tests of |
|---|---|---|
| `SQL/Datastore.py:349` (`sqla.inspect(self._engine)`) | 41 | `test_version_row_at_open` |
| `SQL/ShardedPool.py:858` (the primary's schema check) | 58 | `test_reconcile_at_open` 23, `test_prune_at_open` 13, `test_store_schema` 9, `test_version_row_at_open` 8, `test_read_only_pool` 4, `test_declared_facts` 1 |
| `SQL/ShardedPool.py:870` | 6 | `test_version_row_at_open` |

Each is in a test whose open is refused or abandoned. The engine is then never disposed, and its
pooled connection is closed only by the garbage collector. This is inherited behaviour, the same
under 3.12, where nothing reports it.

- **Re-measure it** with a wrapper of your own, from the scratchpad, at both ends. The log gives
  the counts per site at each end and the method.
- **Open `[05-a-refused-open-leaves-its-engines-undisposed]`** on the board's §3, with the
  measurement, an impact statement (a long-lived process that retries refused opens holds a file
  descriptor per refused engine until the collector runs; no data is affected) and the next step
  (dispose the engines on a refused open, after rule 8 lifts). Add its index row.
- **Do not fix it.** No file under `datastorekit/` changes (rule 8).

### 2.7 The README

The repository's `README.md` is rewritten from its "being extracted" state. It keeps the opening
paragraph's description of what the package does, the `RayWorkPool` note and the licence. It
gains:

- **Status.** `v0.1.0` is SecondaryGWKit's layer at `6f7f291`, moved here with its behaviour
  unchanged (`PROVENANCE.md`), its tests ported onto a neutral client. Say what comes next in one
  sentence: version-keyed lookups in `v0.2.0`. Point at the campaign README and its board.
- **Supported versions.** A table with the declared range (§2.1) and the two tested ends (§2.3).
  Say that on Python 3.13 Ray's floor is in effect 2.45.0 (§2.2), that newer releases inside the
  range are allowed but not tested, and that a client pins its own Ray and SQLAlchemy.
- **Installing.** The pinned form CLAUDE.md gives, `datastorekit @
  git+https://github.com/ds283/DatastoreKit@v0.1.0`, in a client's `requirements.txt`. Add one
  sentence: an editable install is for developing this package, never for a client's production
  runs. Write it as of the tag: the README is committed before the tag exists (U23), and is true
  once it does.
- **Using it.** What a client supplies, in a short list: the pool's constructor arguments, a
  registry of factories, each factory's `register()` and hooks, the inventory declarations, and
  the two tables the layer owns. Point at `docs/client-contract.md` for each item. The neutral test
  client (`datastorekit/tests/client/`) is the worked example; name its registry module.
  - Any code shown names only things that exist. Check each name the README mentions by importing
    it, and list them in the log.
  - Do not write a client from scratch in the README. A sketch that is not run goes stale.
- **The tools.** `python -m datastorekit.tools.sharded_store` and `python -m
  datastorekit.tools.shard_key_audit`, one line each, from their `--help`.
- **Developing.** How to make a venv, install editable, and run the suite (CLAUDE.md's command);
  that CI runs it at both ends; and that the two checks under `docs/extraction/` need the source
  repositories, so they run locally only.

No other prose file changes. `PROVENANCE.md` and `CLAUDE.md` stay as they are.

---

## 3. Verification

1. **The suite, four times:** in `venv/` (after the editable reinstall), in the low and high
   scratch venvs, and again in `venv/` after every change. Each gives `Ran 444 tests … OK`. The log
   records each venv's versions.
2. `compare_with_source.py` exits 0 with 31 compared, 20 `PORTED` and 10 with no source.
   `compare_ported_tests.py` exits 0 over twenty modules, with one test declared not ported. Both
   are unchanged from 04b.
3. **The release check** of §2.4 passes, with its record.
4. **The workflow**, replayed as §2.5 says, at both ends; the file parses as YAML; the matrix equals
   §2.3.
5. **§2.6's measurement** at both ends.
6. `black --check` (25.1.0) is clean on `datastorekit/` and `docs/`.
7. **The breakage record.** Each item is a change exactly as applied, with what failed. None is
   committed, and `git status` is clean after each. A diff to a tracked file is recorded with its
   trailing context lines and checked with `git apply --check` as recorded.
   - **(a) The workflow's install without the package:** step 3 with `-e .` removed (the pins
     installed alone), in the high scratch venv. Expect the 19 tests of hazard 1 to fail.
   - **(b) The SQLAlchemy floor:** step 3 with `sqlalchemy==2.0.38`. The resolver refuses, naming
     the conflict with `>=2.0.39`.
   - **(c) The SQLAlchemy cap:** step 3 with `sqlalchemy==2.1.4`. The resolver refuses.
   - **(d) The Python floor:** `requires-python = ">=3.13"` in `pyproject.toml`. The low end's
     install refuses.
   - **(e) An exclusion too broad:** `exclude = ["datastorekit.t*"]`, which also drops
     `datastorekit.tools`. The release check fails: the tools' `--help` exits non-zero.
   - **(f) The test package shipped:** the `exclude` removed. The release check fails:
     `import datastorekit.tests` succeeds, and the wheel lists files under `datastorekit/tests/`.

   For (b)–(d), use `uv pip install --dry-run` or a throwaway venv; never change the three venvs
   you verify with.

---

## 4. Acceptance

1. `pyproject.toml` declares §2.1's range and version, and §2.4's exclusion.
2. The suite passes at both ends in fresh venvs, and in `venv/`. The release check passes.
3. The workflow is §2.5's and parses. Its steps were replayed at both ends.
4. `[05-a-refused-open-leaves-its-engines-undisposed]` is open, with the measurement.
5. §3.1–§3.7 hold.
6. **The records**, in the same commit:
   - the log, `logs/05-supported-versions-and-ci.md`, per README §5.1. It also has:
     - the versions of every venv, and each suite's verdict line;
     - every install command as run, and the workflow step each stands for;
     - the release check: the wheel's name, size, entry count and SHA-256, its file list, and
       each command's output;
     - §2.6's measurement at both ends;
     - every name the README mentions, with how it was checked;
     - the six hazards;
     - both checks' summary lines;
     - (a)–(f);
     - the test count before and after (444, 444);
   - the board: §1's row for 05 and the header, §3 per §2.6, and a line in §2 under G2 saying
     that `v0.1.0` is ready to be tagged once CI passes (U23), with no tag made;
   - `docs/OPEN_ISSUES.md`: 6 open now, and 7 after, unless the work opens another;
   - `prompts/INDEX.md`: the campaign's line.

---

## 5. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 444, in any venv. A failure at the high end is not
  "fixed" in the layer or the tests: record what fails, and ask.
- Passing anything would need a change under `datastorekit/`, to the checks, or to any file not in
  §6.
- A pin of §2.3 does not resolve, or the declared range of §2.1 cannot be satisfied by both ends.
- The release check fails in a way (e) or (f) does not explain.
- §2.6's measurement finds a connection the layer's tests open and leave unclosed outside those
  three sites, or a site in the tests' own code. Record it; do not fix it; ask whether it joins the
  issue.
- Anything would push to GitHub, make or move a tag, change the repository's settings, start Ray,
  open a store outside a `tempfile` directory, or edit, run, import or open a store of SGK, ChamPBH
  or StochasticInstantons.
- A download other than PyPI packages into the scratchpad (U24) would be needed.

---

## 6. What this prompt does not do

- **Files it creates or changes:**
  - `pyproject.toml`;
  - `.github/workflows/tests.yml` (new);
  - `README.md`;
  - the log, this board, `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.
- It changes nothing else:
  - no file under `datastorekit/`, in the layer or its tests;
  - nothing under `docs/` but `OPEN_ISSUES.md`;
  - none of `PROVENANCE.md`, `CLAUDE.md`, `LICENSE`, `.gitignore` or the campaign README.
- It makes no tag, and pushes nothing (U23).
- It fixes nothing in the layer, including §2.6's issue and the inherited ones.
- It does not rewrite the layer's prose. Rule 8 lifts after this prompt, and 06 adds behaviour only
  behind a `register()` key. The prose rewrite of `[01-package-prose-names-sgks-layout]`, and with
  it U17's pinned hit, is later work.
- It writes no orchestration note.

---

## 7. The log and the board

`logs/05-supported-versions-and-ci.md`, using README §5.1, with the additions of §4.6.

`IMPLEMENTATION_STATE.md`: §1's row for 05 (landed, commit, log), the header, §2's G2 line, and §3.
