# Prompt 10 — release `v0.2.1`

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 09 landed (`cad7bc1`) and was reviewed (`ffe843c`; the user's decision on its finding is
  recorded at `98fb497`).
- `git status` is clean in this repository, and `origin/main` is an ancestor of `main`.
- The board's §3 holds no issue of this repository.

**Closes:** nothing. **Narrows:** nothing. **Changes:** nothing. **Opens:** only what the work
finds.

**Recommended model:** **Opus.**
- No line of code changes. The work is four short edits and four dated addenda.
- Each addendum must say exactly what changed for its client between `v0.2.0` and `v0.2.1`, no
  more, and must leave the checklist it extends as it was written (`CLAUDE.md` rule 6).
- The release check and both ends of the suite are run as 05 and 06 ran them, offline.

**Read first:**

1. [`README.md`](README.md): §1, §2 (rows 08a–11), §4, §5 (rules 4, 5, 9 and 10), §6.2 (U3, U23,
   U28, U29, U33, U36 and U37) and §7.
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`, above all "Releases".
3. The board: §2 (the gates), §4's three entries closed by 08a, 08b and 09, and the reviews of
   08a, 08b and 09.
4. Logs 05 §5.3 and 06 (the release check), log 08a §2.5 (what the clients do with their payloads),
   and the "State handed to the next prompt" of logs 08a, 08b and 09.
5. The files 10 changes, as they stand: `pyproject.toml`, `README.md`, `PROVENANCE.md`,
   `docs/adoption/README.md` and the three checklists.
6. `docs/client-contract.md` §9, which 10 points at and does not change.

Facts below are at `98fb497`, whose `datastorekit/` is `cad7bc1`'s, measured on 2026-10-10.

---

## 1. What is wanted

10 makes the package ready to be released as **`v0.2.1`** (U36), the release all three clients
adopt in place of `v0.2.0` (U37). After it:

- `pyproject.toml` says `0.2.1`;
- `README.md` and `PROVENANCE.md` describe `v0.2.1`;
- `docs/adoption/` carries a dated addendum, in its README and in each checklist, giving the new
  pin and what changed for that client since `v0.2.0`;
- the board's gates say that each client adopts `v0.2.1`, and that the tag waits for CI.

**No line of code changes.** Nothing under `datastorekit/` is touched, and the suite stays at
**486**.

**10 makes no tag and pushes nothing** (as U23 and U28). After its review, its commit is pushed as
`main`. `v0.2.1` is made on it, annotated, only once CI passes at both ends there, as `v0.1.0` and
`v0.2.0` were. If CI fails, a fix prompt lands first; no tag is ever made on a commit whose CI is
red (rule 10). The tag is not this prompt's work.

### 1.1 What changed since `v0.2.0`, measured

Three prompts changed the package after `v0.2.0` (`240028e`). **Only `SQL/ShardedPool.py` changed
in code.** With every docstring blanked, the AST of each of the other 12 changed layer files equals
`v0.2.0`'s, so they differ in comments and docstrings only. Seven layer files are unchanged:
`__init__.py`, `object.py`, `SQL/__init__.py`, `SQL/ClientPool.py`, `SQL/SerialPoolBroker.py`,
`SQL/ProfileAgent.py` and `tools/__init__.py`.

| Prompt | Commit | Closed | What changed | Code |
|---|---|---|---|---|
| 08a | `f938844` | `[02-an-unsupplied-sharded-table-raises-keyerror]`, `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]` | A reopen whose primary records a sharded table that `sharded_tables` lacks is refused with the intended `RuntimeError` ("Mismatch between sharded tables …"), not a bare `KeyError`. `object_get_vectorized` sends each shard copies of the caller's payloads, `{**value, **shard_key}`, and no longer adds the key to the caller's dicts. | `SQL/ShardedPool.py` |
| 08b | `efedc8d` | `[05-a-refused-open-leaves-its-engines-undisposed]` | An open that raises closes the actors it built and disposes the pool's engine, then re-raises the open's exception unchanged. | `SQL/ShardedPool.py` |
| 09 | `cad7bc1` | `[01-package-prose-names-sgks-layout]` | The comments and docstrings that cited the source's layout, campaigns, logs, audits, issues and commits are rewritten for this package; the guard's `KNOWN_HITS` is empty. | none |

Four test modules were added: `test_unsupplied_sharded_table`, `test_vectorized_get_payloads`,
`test_refused_open_closes_engines` and `test_prose_names_no_source`. The suite went from 458 to 486.

**What a client sees.** Nothing a client supplies changes. No API is added or removed. Nothing the
layer writes changes, and no message changes (contract §9.1, §9.2). Three behaviours differ:
- **the exception type of one refusal**, `KeyError` → `RuntimeError`, for an unsupplied sharded
  table;
- **the caller's payload dicts** are left as they were passed;
- **a refused open** leaves no engine for the garbage collector.

**What the clients do with them**, read through `git` only:
- **Payloads.** Log 08a §2.5 measured all three clients at their checklist commits, and no client
  reads a payload list back after a vectorized get.
  - SGK's 17 calls each pass a list built just before.
  - SI's `plot_InstantonSolutions.py:697-702` passes one list to two calls. Under `v0.2.1`, once SI
    converts to the mapping form, each call merges its own key into copies.
  - CPBH and SI pass a bare shard key, which the package refuses before the payload line in both
    releases (their checklists, item 6).
- **`KeyError`.** The planner's measure, at the same commits:
  1. `git -C <client> grep -n 'except KeyError\|except (.*KeyError' <commit> -- '*.py'`, outside
     the client's `Datastore/`;
  2. then `git grep -B3 'ShardedPool('` for a `try` around a construction.

  The results:
  - CPBH and SI catch `KeyError` nowhere outside their layer.
  - SGK catches it in two places, `RunRegistry/__init__.py:606` (a manifest's `created` field) and
    `RunRegistry/tests/test_run_registry.py:489` (a status file's JSON), neither around a pool.
  - The only `try` around a `ShardedPool(` construction outside SGK's layer is in two of SGK's
    archived measurement scripts, `prompts/datastore-generic/orchestrator/measure-07/scripts/m7_messages.py:184`
    and `…/measure-09/scripts/m4c_open_rw.py:38`. Each catches any exception and records its type.
  - **So no client's code depends on the `KeyError`.**

### 1.2 The release check, probed

The planner probed the release on this machine, offline.
- **The build.** From a `git archive` of `98fb497` with only `version = "0.2.1"` changed,
  `uv build --offline --wheel` gives `datastorekit-0.2.1-py3-none-any.whl`. It has 25 entries,
  none under `datastorekit/tests/`, and `…dist-info/licenses/LICENSE` is among them. `METADATA`
  says `Version: 0.2.1`, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43` and
  `Requires-Dist: sqlalchemy<2.1,>=2.0.39`.
- **The install.** `uv venv --offline -p /opt/local/bin/python3.13`, then `uv pip install
  --offline <wheel> "ray==2.55.1" "sqlalchemy==2.0.46"`.
- **The run**, from a directory outside the repository with `PYTHONPATH` unset:
  - the guard's 20 layer modules import, from the venv's `site-packages`;
  - `from datastorekit.contract import VERSION_SERIAL_KEY, require_version_serial` works;
  - `import datastorekit.tests` raises `ModuleNotFoundError`;
  - `importlib.metadata.version("datastorekit")` is `0.2.1`;
  - `python -m datastorekit.tools.sharded_store --help` exits 0;
  - `shard_key_audit` has no `--help`, as at 05 (log 05 §2, correction 2). `--help` exits 2 with
    `!! No such file: <cwd>/--help`, which is its refusal of a path that does not exist.

The wheel's bytes are not reproducible across builds (file times). Record the SHA-256 of yours; do
not compare it with the planner's.

---

## 2. What to change

### 2.1 `pyproject.toml`

`version = "0.2.1"`. Nothing else. No other file carries the version: the package defines no
`__version__`.

### 2.2 `README.md`

- **Status.** A paragraph for **`v0.2.1`**, above `v0.2.0`'s.
  - It is a fix release: the three defects 08a and 08b fixed, each in one clause, and the
    package's prose rewritten for this repository (09).
  - No API changes, nothing the layer writes changes, and no message changes.
  - The one exception type that changes is the `KeyError` → `RuntimeError`.
  - It points at [`docs/client-contract.md`](docs/client-contract.md) §9 for the detail.
- **Installing.** The pin is `v0.2.1`. Replace the sentence "`v0.1.0` remains, for a client that
  has not adopted `key_on_version`" with one saying:
  - `v0.2.0` and `v0.1.0` remain tagged, and no tag is moved or deleted;
  - every client adopts `v0.2.1`, which fixes defects both earlier releases carry.

  Write it as of the tag: the README is committed before the tag exists, and is true once it does.
- **Using it.** One item: what changed after `v0.2.0` is in contract §9 ("Changes after
  `v0.2.0`"). Link the section's anchor, as the README's other contract links do.
- **Nothing else changes**, the "Supported versions" table and "Developing" included. Every name
  the README mentions is checked by importing it, or by finding the file or anchor, as 05 and 06
  did.

### 2.3 `PROVENANCE.md`

Add, under "After `v0.1.0`" and after "Prompt 06", a section **"Prompts 08a, 08b and 09: fixes and
prose (`v0.2.1`)"**. It says:
- **The three fixes have no source.** They were made here, each closing an issue of this
  repository's board. Name each issue, its prompt and commit, and its test module. Each fixes
  behaviour that SGK's frozen copies still carry: §"The freeze" (U3) says a defect found during
  the freeze is fixed here after G2, and U33 fixed these three before it. SGK receives them by
  adopting `v0.2.1`.
- **09 changed prose only.** Comments and docstrings were rewritten in 12 layer files and in
  `SQL/ShardedPool.py`. From `v0.2.1` no layer file equals its SGK source in its comments, except
  the seven 09 did not touch (§1.1). §"The differences allowed" describes `v0.1.0` and is not
  extended.
- **The files each prompt changes**, and its log.

Change nothing above it. `PROVENANCE.md` is outside the package, so it may name SGK and its paths.

### 2.4 The addenda (U37)

Each addendum is dated, says it was written by extraction prompt 10, and is added. **Nothing
already in the file is rewritten** (`CLAUDE.md` rule 6): 07a's measurements stay as written, true
of `v0.2.0`. Each file gains two things:
1. **An italic line at its head**, saying that the addendum below gives the pin `v0.2.1` and what
   changed since `v0.2.0`, and that it supersedes the statements it names. In the README it goes
   after 07a's italic line; in a checklist, after the bullet list under the title.
2. **A section `## Addendum: v0.2.1 (extraction prompt 10, 2026-10-10)`**, unnumbered, so that the
   ten items keep their numbers. In each checklist it goes after item 10 and before the appendix.
   In the README it goes after §6.

Each addendum states:
- **the pin**, `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.1`, in place of
  `v0.2.0`'s, and that the client adopts `v0.2.1` (U37);
- **what changed since `v0.2.0`, for that client** (below), with contract §9's rows as the
  detail;
- **which statements it supersedes**, each by `path:line` of the file it is in;
- **line citations.** Every `datastorekit/` line the file cites stays `v0.2.0`'s and is read at
  that tag. A line the addendum cites is at `v0.2.1`'s tree, which is `cad7bc1`'s and 10's.

What each addendum says:

| File | Supersedes | States |
|---|---|---|
| `README.md` | `:3` and `:8` ("against … `v0.2.0`"), `:24-26` ("All three adopt `v0.2.0`"), `:35` (the pin), `:154` (G2 "adopted `v0.2.0`, U29"), `:155-156` ("The campaign closes at 07b": it closes at 11, U33), `:174` (`datastorekit/` lines are `v0.2.0`'s) | the pin; the three behaviours of §1.1, each a link to its contract row; nothing any client supplies or stores changes; the `KeyError` finding of §1.1; that the checklists are not re-measured (U37) and each has its own addendum |
| `secondarygwkit.md` | `:6` and `:17` (`v0.2.0`); `:25-27`, the byte-identity count against `v0.2.0`; `:203-206`, "the in-place update … is SGK's own behaviour, unchanged"; `:292-297`, item 8's reasoning, which it extends; `:301` (G2 adopts `v0.2.0`) | at `v0.2.1`, SGK's 17 files and the package differ also by: <br>• 08a's and 08b's code in `SQL/ShardedPool.py`; <br>• 09's prose in 11 of SGK's 17 (both tools among them). <br>So only the six 09 did not touch (`__init__.py`, `object.py`, `SQL/__init__.py`, `ClientPool.py`, `SerialPoolBroker.py`, `ProfileAgent.py`) can equal SGK's sources byte for byte, and the count at `:25-27` is `v0.2.0`'s. Item 8 still holds: the fixes change nothing the layer writes (contract §9.1, §9.2), and 09 changes no code, so every SGK store opens as under `v0.2.0`. G2's rehearsal is the measurement. SGK's vectorized calls read nothing back (log 08a §2.5). SGK's frozen copies carry the three defects, which adoption fixes. |
| `champbh.md` | `:6` and `:18` (`v0.2.0`); `:254-255`, "It also adds that mapping to every payload dict in place"; `:374` (G3 adopts `v0.2.0`) | the bare-`beta_value` refusal of item 6 is unchanged, and CPBH still converts its 7 calls to the mapping form. Once it has, the package sends copies, and CPBH's dicts are left as they were. The in-place hazard is gone. |
| `stochasticinstantons.md` | `:5` and `:16` (`v0.2.0`); `:255-257`, "and adds it to each payload dict in place"; `:348` (G4 adopts `v0.2.0`) | as CPBH's, for SI's 15 calls, and that `plot_InstantonSolutions.py:697-702`'s one list passed to two calls is safe under `v0.2.1` (log 08a §2.5) |

For every checklist, the engine disposal (08b) is one sentence: a client that retries refused opens
no longer holds a file descriptor per refused engine until the collector runs. The `KeyError`
change is one sentence that names the finding of §1.1.

**The line numbers in the table are the planner's at `98fb497`.** Check each against the file
before citing it, and cite what you find. A statement the table does not name, that is no longer
true of `v0.2.1`, is superseded too, and recorded in the log.

### 2.5 The board's gates

The gate titles of §2, for G2, G3 and G4, say `v0.2.1` (U37). Each gains a dated line: `v0.2.1` is
ready to be tagged on 10's commit once CI passes there (as U23, U28), and no tag is made. The two
lines recording `v0.1.0` and `v0.2.0` stay as they are.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **Additive documents.** Everything under `docs/` is additive (`CLAUDE.md` rule 6). An addendum
   that rewrites a line of 07a's, even to correct a pin, fails acceptance. `git diff` of each file
   under `docs/adoption/` shows `+` lines only.
2. **A name or link that does not exist.** Every module, name, file, anchor and contract row the
   README, `PROVENANCE.md` and the addenda mention is checked: names by importing them in `venv/`,
   anchors by finding the heading. The log lists each with how it was checked. Contract §9's
   anchor is `#9-changes-after-v020`; confirm it the way the README's existing anchors were
   confirmed.
3. **The tag does not exist yet.** The README, the addenda and the gates name `v0.2.1` as of the
   tag. Nothing may say it is tagged.
4. **No client is re-measured** (U37). The addenda cite log 08a §2.5 and §1.1's `KeyError`
   measure. Re-run that measure yourself, read-only through `git`, and record it. If any result
   differs from §1.1, stop.
5. **Offline only.** Every venv and the build are `--offline`, from the cache 05's work filled. A
   pin, or the build backend, that does not resolve offline is a stop.
6. **`shard_key_audit` has no `--help`** (§1.2). The release check records its message, as 05's
   did. It is not a failure.
7. **`venv/`'s metadata.** After §2.1, reinstall the package in `venv/` with
   `./venv/bin/python -m pip install --no-deps -e .`, so that `pip show datastorekit` says `0.2.1`,
   and run the suite there again.

---

## 4. Verification

1. **The suite.** In `venv/`, `Ran 486 tests … OK` before and after, with `pip show` saying `0.2.1`
   after. At the high end, in a fresh offline scratch venv (Python 3.13.16, `ray==2.55.1`,
   `sqlalchemy==2.0.46`) with a `git archive` of your tree installed editable: `Ran 486 tests …
   OK`, with 4 `ResourceWarning` lines, as at 09.
2. **The checks.**
   - `compare_ported_tests.py` exits 0 with "20 module(s) … 1 test(s) declared not ported".
   - `black --check datastorekit docs` leaves 70 files unchanged.
   - The guard and `test_prose_names_no_source` pass; they are in the suite.
3. **The release check**, as §1.2, built from a clean `git archive` of your tree, never in this
   checkout, and installed at the high pins, offline. Record:
   - the wheel's name, size, entry count and SHA-256, and its file list;
   - `METADATA`'s `Version`, `Requires-Python` and `Requires-Dist` lines;
   - each command of §1.2 with its output.

   Nothing is built in the checkout. `git status` shows no `build/`, `dist/` or `*.egg-info`.
4. **The documents.** List every remaining `v0.2.0` in `README.md`, `PROVENANCE.md` and
   `docs/adoption/*.md`, each with why it stays: history, a statement the addendum supersedes, or
   the README's "remain tagged". Also confirm:
   - `git diff` of the four files under `docs/adoption/` has no `-` line;
   - `docs/client-contract.md` is unchanged.
5. **The breakage record.** Each item is a change exactly as applied, in a scratch export, with
   what failed. None is committed. Check each diff with `git apply --check` and `-R --check` as
   recorded.
   - **(a)** `pyproject.toml`'s version left at `0.2.0`: the release check's `METADATA` and
     `importlib.metadata.version` assertions fail, naming `0.2.0`.
   - **(b)** the `exclude` line removed from `pyproject.toml`: the wheel lists files under
     `datastorekit/tests/`, and `import datastorekit.tests` succeeds (as 05's (f)).
6. **The clients.** Record each client's `HEAD` and `git status --short`, at the start and the
   end, unchanged. None is written, run, imported or opened. They are read only through `git` at
   the checklists' commits (hazard 4).

---

## 5. Acceptance

1. `pyproject.toml` says `0.2.1`, and nothing else in it changed.
2. `README.md` and `PROVENANCE.md` are as §2.2 and §2.3 say, and every name in them exists.
3. Each of the four files under `docs/adoption/` has its italic line and its addendum, per §2.4,
   and no line of it is rewritten.
4. §4.1–§4.6 hold.
5. **The records**, in the same commit:
   - the log, `logs/10-release-v0.2.1.md`, per README §5.1. In place of `compare_with_source.py`'s
     output it has:
     - the port check's output;
     - the release check;
     - the documents' check (§4.4);
     - every name and link checked (hazard 2);
     - the `KeyError` measure (hazard 4);
     - (a) and (b);
     - the clients' commits and statuses, at the start and the end;
   - the board: §1's row for 10 (landed, commit, log), the header, and §2's gates (§2.5);
   - `docs/OPEN_ISSUES.md`: unchanged at **4**, unless the work opens an issue;
   - `prompts/INDEX.md`: the campaign's line.

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 486, in any venv.
- The release check fails in a way (a) or (b) does not explain.
- §1.1's `KeyError` measure, re-run, finds a client that catches the `KeyError` around a pool.
- An addendum cannot say what it must without rewriting a line of 07a's.
- Anything would change a file under `datastorekit/`, `docs/client-contract.md`, the workflow, or
  any file not in §7.
- Anything would push, make or move a tag, download, start Ray, or write, run, import or open
  anything of a client.

---

## 7. What this prompt changes, and what it does not

- **Files it changes:**
  - `pyproject.toml`, `README.md` and `PROVENANCE.md`;
  - `docs/adoption/README.md`, `secondarygwkit.md`, `champbh.md` and `stochasticinstantons.md`,
    by addition only;
  - the log, the board, `docs/OPEN_ISSUES.md` if an issue is opened, and `prompts/INDEX.md`.
- **It changes nothing else:**
  - no file under `datastorekit/`;
  - not `docs/client-contract.md`, whose §8 citation 11 corrects (U34);
  - not `docs/extraction/`, the workflow, `CLAUDE.md`, `LICENSE`, `.gitignore` or the campaign
    README.
- **It touches no client repository.**
- **It makes no tag and pushes nothing.** The orchestrator's note says how the push and the tag are
  made after the review.
- It writes no verification document; that is 11's.

---

## 8. The log and the board

`logs/10-release-v0.2.1.md`, using README §5.1, with §5.5's additions. The log also lists the
clients' commits and statuses, at the start and the end.

`IMPLEMENTATION_STATE.md`: §1's row for 10, the header, and §2's gates.
