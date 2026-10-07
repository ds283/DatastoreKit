# Orchestrator — prompt 01, import the layer

Read [`../README.md`](../README.md) first: §0.1, §0.2, §1, §3, §4, §5 and §6. This is the
campaign's first note, so it states the conventions in full. They are SGK's
`datastore-generic-followup` notes' (`SecondaryGWKit/prompts/datastore-generic-followup/
orchestrator/prompt-01.md` §0's last list), adapted to a repository with no store, no run
registry and, until this prompt lands, no suite.

**You do not write code.** You may:
- run the suite, the equivalence check and the tests the log names;
- replay the log's deliberate-breakage diffs with `git apply`, and revert them;
- run an in-process check or a probe from the session scratchpad, never committing one;
- read SGK through `git -C /Users/ds283/Documents/Code/SecondaryGWKit show 6f7f291:<path>`;
- fix small residue in a follow-up commit of your own (§4).

**The prompt:** [`01-import-the-layer.md`](../01-import-the-layer.md)
**Closes:** nothing · **Narrows:** nothing · **Opens:** one issue expected (§0, "Prose") ·
**Model:** Opus, as the prompt recommends.

**Gate:**
- G1 holds: the import commit is SGK `6f7f291`. U2–U5 are taken.
- U3's freeze is in force (SGK `b510bc9`), and holds: `git -C SecondaryGWKit diff --stat 6f7f291
  HEAD` over the 15 layer files, `tools/`, `Datastore/tests/shard_store_fixtures.py`,
  `utilities.py` and `config/defaults.py` is empty at SGK `b510bc9` (2026-10-07).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It is the campaign's foundation, and its only code is a move.** Every later prompt and every
client's adoption stands on two things it delivers: the package as imported, and
`compare_with_source.py`, the check that the package still *is* SGK's layer (README §5 rule 8).
The review therefore has two halves:
- **the package is SGK's layer**, under §4's names, changed only by D-imp, D-str, D-tool, D-root,
  D-int and D-fmt;
- **the equivalence check would catch a real difference**, not only pass on this one. A check that
  accepts everything is worse than none, because 02–05 will cite it.

**What moves on purpose:** nothing that behaves. New files only:
`pyproject.toml`, `PROVENANCE.md`, `datastorekit/` (17 modules, two `__init__.py`s, two
internalised modules, nine test files and the import guard), `docs/extraction/compare_with_source.py`,
the log, and the records.

**The equivalence check: the hard part.** The prompt asks for rules, not line lists, and asks
them to be narrow. Two traps, measured by reading the sources:
- **`black` will reflow D-tool lines.** For example `test_shard_key_audit_copy.py:90`,
  `[sys.executable, str(TOOL), str(self.b / "store.sqlite")],`, becomes too long for one line once
  `str(TOOL)` is `"-m", "datastorekit.tools.shard_key_audit"`, and `black` splits it. A
  line-by-line diff then shows a multi-line hunk that no single-line rule matches.
  **Recommended:** a rule is a *substitution applied to the source*. A hunk is classified under a
  rule when the source hunk, with the rule applied, equals the package hunk **token for token**
  (`tokenize`, ignoring `NL`/`NEWLINE`/`INDENT`/`DEDENT` and whitespace). A hunk equal token for
  token with no rule applied is D-fmt. This keeps the rules narrow, and (a)–(d) of the prompt's
  §2.5 fail by construction. It is a recommendation: another design is acceptable if the log shows
  it bites on (a)–(d) and on the orchestrator's (e) below.
- **D-str must not accept the class name.** `Datastore.py:155` holds
  `f"Datastore.set_version: the version serial must be an int, not {serial!r}"`. This is the only
  `"Datastore.`-prefixed string literal in the 17 package files at `6f7f291`; the others are in
  the tests (`test_delete_store.py:339`, `test_shard_paths.py:112`,
  `test_shard_key_audit_copy.py:136`). A rule that accepts a string only when **the whole literal**
  is a dotted name, and its image is a module of the package or an attribute of one, rejects (c).
- **(e), the orchestrator's addition:** a D-str rewrite applied to prose. Rewrite one comment or
  docstring mention of `Datastore/shard_paths.py` (for example `shard_key_audit.py:19`) to
  `datastorekit/shard_paths.py`. The check must exit non-zero and name the line. Record it with
  (a)–(d), as an IMPLEMENTATION CHOICE made at the orchestrator's direction.

**Prose stays, and is recorded once.** The prompt says prose referring to SGK's layout is never
rewritten (D-str). So, after D-tool, some prose in the package is stale:
- `sharded_store.py`'s docstring says "It puts its own repository root on sys.path, so it runs
  from any directory with no PYTHONPATH". The bootstrap it describes is gone (D-tool); `shard_key_
  audit.py:25` says the same.
- Many comments and docstrings name `Datastore/…`, `tools/…` or SGK's repository root;
  `test_sharded_store_script.py:6` says the script runs "from the repository root".

**Leave all of it unchanged** (rule 8). Lines that name a usage, `prog` or `python tools/<name>.py`
command are D-tool and do change (`sharded_store.py:5-6`, `:43`; `shard_key_audit.py:44`).
Open **one** §3 issue for the rest, `[01-package-prose-names-sgks-layout]`, with a count of lines
by file and the two bootstrap sentences quoted. It is fixed after 05, when rule 8 lifts. That is
the one issue expected; the index goes from 4 to 5.

**The facts, checked by the orchestrator on 2026-10-07 at SGK `6f7f291`** (by `git show` and an
export in the orchestrator's scratchpad; no SGK code was run). Pass them on.
- **The 17 files' lengths at `6f7f291`.** README §0.2's table is at `4c34f13`; two files moved in
  SGK's 03. `store_reader.py` is 241 lines (238 there), and `ShardedPool.py` 3,618 (3,627 there).
  The other 15 are as the table says. This is not a stop.
- **The prompt's line numbers hold:** in-function imports at `ShardedPool.py:406`, `:494`,
  `:1299`, `Datastore.py:198` and `store_inventory.py:993`; `config.defaults` at
  `ShardedPool.py:36` and `ProfileAgent.py:10`; `utilities` at `Datastore.py:20` and
  `ProfileAgent.py:11`; `Datastore.py:155`; the bootstrap at `sharded_store.py:34-36` and
  `shard_key_audit.py:52-54`; `test_shard_file_name.py:23`, `:92-101`; `test_shard_paths.py:109`,
  `:112`, `:115`; `test_delete_store.py:339`; `test_shard_key_audit_copy.py:136`.
- **No other client import.** Every import in the 17 files and the nine test files is the
  standard library, `ray`, `sqlalchemy`, `Datastore.*` (relative or absolute), `config.defaults`
  or `utilities`. `test_delete_store.py:33` imports `ray` only to assert
  `ray.is_initialized()` is false (`:625`, `:629`); no test starts Ray.
- **One name is not a path.** `ShardedPool.py:13` is `from Datastore.SQL import Datastore`. Its
  module path maps (`datastorekit.SQL`); the imported name `Datastore`, the class, does not.
- **Three `__init__.py`s exist in SGK**, contrary to the prompt's §2.2: `tools/__init__.py`,
  `Datastore/tests/__init__.py` and `Datastore/SQL/ObjectFactories/__init__.py`, each 0 bytes.
  The package's `datastorekit/tools/__init__.py` and `datastorekit/tests/__init__.py` are therefore
  copies, not new files. Make them empty as the prompt says, and include them in the check (equal
  by 0 bytes). `ObjectFactories/__init__.py` has no counterpart (`base.py` becomes
  `SQL/factory_base.py`). STRUCTURALLY REQUIRED; the log says so.
- **The internalised definitions.** `utilities.py:1` `import time` is the only import
  `WallclockTimer` (`:6`) and `format_time` (`:25`) need; the constants are `:20-22`.
  `utilities.py` also imports `zip_longest` and `print_tb` and defines `grouper` (`:66`) and more;
  none of it goes. `config/defaults.py` is the one line `DEFAULT_STRING_LENGTH = 256`.
- **The tools under `-m`.** `shard_key_audit.py:76` prints `usage: {argv[0]} …`. Under `-m`,
  `argv[0]` is the module's file path. It is not a usage line naming the tool, so it is unchanged,
  and no ported test asserts on it. In the `runpy` probes, `sys.argv[0]` is built from
  `SCRIPT`/`TOOL`. Under D-tool it becomes the module name (or any string); argparse's `prog` is
  fixed, so nothing reads it. List it with the D-tool changes.
- **The breakage for `_assign_shard_keys`** is at `ShardedPool.py:3561`,
  `{"key_serial": item.store_id, "shard_id": new_shard}`. Bind `"key_id"` there.
- **The tools' bootstrap breakage.** D-tool already removes the bootstrap, so the prompt's §3.4
  last item is, in effect, **the package uninstalled** (`pip uninstall -y datastorekit`). There
  is no diff; record the commands. Expect the subprocess tests of `test_sharded_store_script`,
  `test_shard_key_audit_copy` and `test_shard_key_audit_refusals` to fail, since their child runs
  from an unrelated directory with no `PYTHONPATH`. In-process tests still import the package from
  the repository root under `-t .`, and that is not a fault. List every failure, then re-install
  with `pip install -e .` and re-run to 90.
- **`black`.** SGK's venv runs `black` 25.1.0, and SGK's 26 source files of this prompt are clean
  under it. **Install `black==25.1.0`**, so that D-fmt measures the move and not a newer `black`'s
  style. IMPLEMENTATION CHOICE at the orchestrator's direction.
- **The toolchain.** `/opt/local/bin/python3.12` is Python 3.12.15, the same as SGK's venv;
  the machine is `arm64`. Installing from PyPI needs the network.
- **`pyproject.toml`.** The repository root holds `docs/` and `prompts/` beside the package, and
  `docs/extraction/` will hold a `.py`. Name the package explicitly
  (`[tool.setuptools.packages.find] include = ["datastorekit*"]`) rather than rely on
  auto-discovery.
- **Expected counts:** the suite here is **0** before (there are no tests), and **90** after
  (88 + 2). SGK's 88 were measured by the orchestrator on 2026-10-07 at `99456d8`, whose layer,
  tools and tests are `6f7f291`'s: `Ran 88 tests … OK`.
- **The index:** 4 open now (all inherited, §1.2), 5 after.

**What the review exists to establish.**
- **(E1) The files.** Every file of the prompt's §2.3 exists under its name, and nothing else is
  in `datastorekit/` but the two `__init__.py`s, the two internalised modules and the guard.
- **(E2) Equivalence.** `compare_with_source.py` exits 0, and by reading its rules are narrow:
  each is a mapping applied to the source, not a pattern that accepts a class of line.
- **(E3) The check bites.** (a)–(e) each exit non-zero and name the line.
- **(E4) The tests.** 90 pass. Each of the 88 keeps its name, class and assertions; the only
  changes are D-imp, D-str, D-tool and D-root.
- **(E5) No client is reachable.** `import datastorekit…` succeeds and `import Datastore` fails in
  a clean shell; the guard holds and bites.
- **(E6) The pins.** The `key_id` breakage, the `numpy` import and the uninstall each fail as
  recorded.
- **(E7) The records.** The log in README §5.1's form with the prompt's §4.3 additions; the board,
  `prompts/INDEX.md`, the index (5, with the one issue) and `PROVENANCE.md`.

**Conventions.** All of these bind the agent, and the brief says so.
- **Staging and reporting.** Stage by explicit path only, and show `git diff --cached
  --name-only` before committing. `venv/` and `*.egg-info/` are gitignored and must not be staged.
  Count, then paste. A log states only what the diff, the check and the tests show.
- **The SHA.** The agent writes "this commit", and the orchestrator substitutes the SHA in its
  follow-up.
- **The suite.** Use `CLAUDE.md`'s command, from the repository root. Write the output to a file
  in the scratchpad and grep the verdict from it. Run it **in the foreground**, within the turn.
- **Breakage diffs** are recorded so that `git apply` replays them from a clean tree at the
  agent's commit. Check each with `git apply --check` and `-R --check`, and replay in `bash`, not
  zsh. None is committed; after each, `git status` must be clean.
- **SGK is read only through `git show 6f7f291:<path>`** (or `git archive 6f7f291` into the
  scratchpad). Never from SGK's working tree, never by importing it, never by running its code or
  tests (README §5 rule 5).
- **Scratch.** The agent uses its own subdirectory of the session scratchpad, never `/tmp`. The
  prompt's §3.1 runs from `/tmp`; any directory outside this repository that holds no
  `datastorekit/` or `Datastore/` will do, and the scratchpad is one. Python's `tempfile` in tests
  is fine. **No scratch `.py` goes under `datastorekit/`**, even for a moment: the import guard and
  the naming-rule test scan the filesystem.
- **Ray.** The agent starts no Ray. Another project's cluster, if running, is left alone.
- **Stop conditions are real.** A stop goes to the user through the orchestrator, and the agent
  resumes with `SendMessage`. A difference that fits no class, or a test that would need more than
  D-imp, D-str, D-tool or D-root, is a stop, never a widened rule.
- **Other sessions** may land commits on this branch. Check `git log` before committing, and never
  assume `HEAD` is your own.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. `venv/` must not exist yet; if
   it does, record what is in it and tell the agent to recreate it.
2. **The freeze.** Re-run the gate's `git diff --stat` in SGK; it must be empty.
3. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`.
4. **The index.** 4 now, 5 after. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md` and `CLAUDE.md`;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's corrections (the three `__init__.py`s, the lengths, the
uninstall breakage) and additions (breakage (e), `black==25.1.0`, the prose issue).

Tell it plainly:
- **One commit, at the end.** Its log is `logs/01-import-the-layer.md`, in README §5.1's form,
  with the prompt's §4.3 additions.
- **The files it may add or change are the prompt's §6 list, and nothing else**, plus the board's
  §3 and the index for the one issue. In particular it must not touch `README.md`, `CLAUDE.md`,
  `LICENSE`, `.gitignore`, `.idea/`, the campaign README or anything under `orchestrator/`.
- **It edits no client repository, and runs no client code.**
- **It runs no build beyond `pip install -e .`, and starts no Ray.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — nine checks

1. **Scope.** `git show --stat <commit>` touches only the prompt's §6 list and the records. No
   file under `venv/`, no `*.egg-info`, no scratch file.
2. **E1, the files.** `git ls-files datastorekit` lists exactly the prompt's §2.3 files under
   their names, the two `__init__.py`s, `defaults.py`, `_timing.py` and `test_package_imports.py`.
3. **E2, by running.** In a fresh shell, `./venv/bin/python docs/extraction/compare_with_source.py`
   exits 0. Its counts per file and class equal the log's.
4. **E2, by reading.** Read `compare_with_source.py` in full. Each rule is a mapping from source to
   package text, and the import map is §4's four entries and nothing else. D-str accepts a whole
   literal only; D-tool's substitutions name the two tools and the three test modules only; D-root
   names the two tests only; D-int compares the extracted definitions byte for byte. No rule is a
   list of line numbers, and none accepts a line because it merely contains `datastorekit`.
5. **E3, the check bites.** Replay (a)–(e) from the log, one at a time, in `bash`. Each must exit
   non-zero and name the line. Then one of the orchestrator's own, not in the log: change
   `DEFAULT_STRING_LENGTH = 256` to `255` in `datastorekit/defaults.py`; it must fail too. Revert
   each, and check `git status` is clean.
6. **E4, the tests, by running and reading.** `./venv/bin/python -m unittest discover -s
   datastorekit/tests -t .` gives `Ran 90 tests … OK`. Then, per module, the set of
   `Class.test_name` here equals SGK's at `6f7f291` (by `ast`, from `git show`). Read the D-tool
   and D-root hunks in full. Each subprocess test still runs from an unrelated `cwd` with
   `PYTHONPATH` removed, and still asserts what it asserted.
7. **E5, isolation.** From the scratchpad, with `env -u PYTHONPATH`, run the prompt's §3.1 pair:
   the package imports succeed, and `import Datastore` fails with `ModuleNotFoundError`. Read
   `test_package_imports.py`: it walks every module including `tests/`, sees imports inside
   functions, treats a relative import as `datastorekit`, and its second test runs a fresh
   interpreter.
8. **E6, the pins.** Replay the `key_id` diff and the `numpy` diff, and run the uninstall, each in
   `bash`, and check that the failures are the log's. Re-install, and the suite is 90 again.
9. **E7, the records.**
   - The log has every section of README §5.1; `pip freeze` (Python 3.12.15, `ray==2.43.0`,
     `sqlalchemy==2.0.39`, `black==25.1.0`); the check's whole output; the D-tool list; the count
     before (0 here, SGK 88) and after (90); and, for each of the four inherited issues, where its
     code is in the package.
   - `PROVENANCE.md` has the five items of the prompt's §2.8, and the SGK commit's subject line is
     right (`Record the orchestrator's review of datastore-generic-followup prompt 03`).
   - The board has 01's row, and §3 the prose issue. The index counts 5 by counting, matching its
     header. `prompts/INDEX.md`'s row says 01 landed.
   - `black --check` (25.1.0) is clean on `datastorekit/` and `docs/extraction/`.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 01* paragraph, in the form of
  SGK's `datastore-generic-followup` board. Fix small residue in a follow-up commit of its own.
  That includes:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README §2's status column for 01;
  - a list of orchestrator notes on the board, with this note marked "used for 01".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Report to the user:**
  - what landed, and the count, 90;
  - the equivalence check's design, its counts per class, and (a)–(e) plus the orchestrator's own
    breakage failing it;
  - whether the `key_id` breakage was caught, and by which tests (if by none, it is a finding for
    03);
  - the prose issue;
  - that 02 can now be written, against the tree 01 left.
