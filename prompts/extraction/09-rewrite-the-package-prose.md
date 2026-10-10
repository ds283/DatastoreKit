# Prompt 09 — rewrite the package prose

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 08b landed (`efedc8d`) and was reviewed (`452b3c9`).
- `git status` is clean in this repository, and `origin/main` is an ancestor of `main`.

**Closes:** `[01-package-prose-names-sgks-layout]`, assigned here by U33 and U35, and widened by
U38. **Narrows:** nothing. **Changes:** nothing. **Opens:** only what the work finds.

**Recommended model:** **Opus.**
- No line of code changes. The work is about 250 lines of prose in 42 files, and each line needs
  judgment: what it cites, what the sentence still has to say once the citation goes, and whether
  that sentence is true of this package.
- About a quarter of the lines are found only by reading, not by a pattern.
- A new test module guards the result. Its rules must catch what this prompt removes and pass
  everything this repository legitimately says.

**Read first:**

1. [`README.md`](README.md): §1, §2 (rows 09–11), §4, §5 (rules 4, 6, 7, 9 and 10), §6.2 (U17,
   U33–U40).
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`.
3. The board's §3 entry for the issue, in full, and its review of 08b.
4. `PROVENANCE.md`: what it records of the source, so that a citation removed here stays reachable.
5. Log 03a §8 (the prose measure's method) and log 04b §8 (its last re-measure).
6. `datastorekit/tests/test_layer_is_generic.py`: its docstring, `KNOWN_HITS` (`:192-203`) and
   `assertNoHits` (`:323-327`).
7. `datastorekit/tests/test_sharded_store_script.py:115-128`, which asserts phrases of
   `tools/sharded_store.py`'s module docstring (hazard 3).

Line numbers here are the package's at `452b3c9`, whose `datastorekit/` is `efedc8d`'s.

---

## 1. What is wanted

The package's comments and docstrings were imported from the source repository unchanged, and
ported tests carried their prose with them (README §5 rules 6 and 8). So the package still points
its reader at the source's files, campaigns, logs, audits, issues and commits, none of which
exist here. "`(prompts/a3-v2-readiness, prompt 03)`" sends the reader to a directory this
repository does not have. "`(prompt 03)`" in the same module means the same campaign, but reads as
this campaign's prompt 03. Several sentences are now false:
- `tools/sharded_store.py:25-26` and `tools/shard_key_audit.py:24-26` describe a `sys.path`
  bootstrap that was removed at 01 (D-tool);
- `test_shard_key_audit_copy.py:11` and `test_shard_key_audit_refusals.py:28` say the tool is run
  as `python tools/shard_key_audit.py`. Both tests run `python -m datastorekit.tools.shard_key_audit`
  (`:89-91`, `:92`).

**09 rewrites that prose for this repository (U38, U39), and adds a test that keeps it so
(U40).** Every comment and docstring that names the source's layout, campaigns, logs, audits,
issues, commits or `var/` loses the citation and keeps its explanation, made true for this
package. The guard's `KNOWN_HITS` is emptied (U17). **No line of code changes.**

09 changes no file outside `datastorekit/` except the records. It does not change
`docs/client-contract.md` (its line citations are of their own trees, `CLAUDE.md` rule 6),
`PROVENANCE.md`, `README.md` or `docs/adoption/`. It makes no tag and pushes nothing.

### 1.1 The measurement, at `452b3c9`

**The board's pattern.** Log 03a §8's method, reimplemented, reproduces every recorded figure:
- 102 lines in 19 files at `8bc60a5`;
- 114 in 23 at `72cf34a`;
- 124 in 28 at `ae94aaa`;
- 146 in 35 at `7ceed25`;
- 155 in 40 at `0c66505`.

At `452b3c9` it still gives **155 lines in 40 files**, since 05–08b added no such line. All 155 are
comments (30) or docstrings (124), plus the one string that is `KNOWN_HITS`' own entry.

**What U38 takes in.** The pattern misses four kinds of reference, and counts two lines that are
true here.
- **What it misses:**
  - the source's campaign names without a `prompts/` prefix;
  - `var/`;
  - the source's commits: `b04671f`, `a2bd966` and `e53f323`;
  - bare citations of the source's records that only reading finds.
- **The two lines true here:** `test_layer_is_generic.py:71` ("repository root", of this
  repository) and the `KNOWN_HITS` string.

The planner measured in three tiers:

| Tier | How found | Lines | Files |
|---|---|---|---|
| A | §2.4's rules, applied to every comment and docstring under `datastorekit/` | 181 | 42 |
| B | The source's commit SHAs, in comments and docstrings, not already in A | 10 | — |
| C | Reading: bare `prompt NN`, `log NN`, `README §…`/`U1`, `audit …`, audit labels, the source's issue names, in imported or ported files | 57 | — |
| | **Together** | **248** | **42** |

Of the 248, 97 are in 13 files of the layer, and 151 in 29 test files. The appendix lists every
line, with tier C's starred. Tier C is the planner's reading, and the agent confirms or rejects it
line by line (§2.1, rule 8).

**What is not in scope, and stays:**
- **The import commit's provenance.** `defaults.py:2-3` and `_timing.py:2-4` name
  `6f7f291` and `PROVENANCE.md`. `_timing.py:3` is in tier A only because it names the source's
  `utilities.py` (§2.1, rule 4).
- **Generic mentions of "the source repository".** 23 lines outside the 248 say what the source
  did, with no file, campaign or commit.
- **This repository's own citations:**
  - "added by prompt 03b";
  - `README §6.2, U25`;
  - `D2`;
  - "extraction prompt 08a";
  - `docs/client-contract.md`;
  - `docs/extraction/measure_client_vocabulary.py`.

  There are about 80 lines of these outside the 248, most in `tests/client/`, the guard and the
  modules this campaign wrote.
- **The tool's own "audit"** (`shard_key_audit`'s messages and the tests that read them).
- **Code.** No runtime string names the source's layout. Every string that is not a docstring,
  f-strings included, was scanned. `test_shard_key_audit_refusals.py:193` (`"a2bd966"`) is a
  string the test asserts the tool does *not* print. It is code, and stays.

---

## 2. What to change

### 2.1 The rules of the rewrite (U39)

1. **What goes.** A comment or docstring names none of these:
   - **the source's files and modules:** `Datastore/…`, `tools/…`, its `docs/…` and `prompts/…`
     paths, dotted `Datastore.<module>`, `ObjectFactories`, `RunRegistry`, `main.py`,
     `config.defaults`, `utilities.py`, and "the repository root" meaning the source's;
   - **its campaigns, prompts, logs, READMEs, boards and decisions:** "`prompts/datastore-generic`
     prompt 06", "(prompt 03)" meaning the source's, "README U1", "the user's decision U1";
   - **its audits and their labels:** "audit §4.1", "audit R2 Run 1", "V1 case 3", "the B1 fix",
     "S1–S3", "O1–O2", "W1–W2", "§2 P4", "L3", "QSI";
   - **its issues:** `[04-the-shard-key-audit-crashes-where-it-should-refuse]`;
   - **its commits:** `b04671f`, `a2bd966`, `e53f323`;
   - **its `var/` directory.**
2. **The citation goes; the explanation stays, true for this package.**
   - A module path becomes the package's: `datastorekit/shard_paths.py`, or
     `datastorekit.shard_paths`.
   - A tool is run as `python -m datastorekit.tools.<name>`.
   - "Nothing under `var/`" becomes what holds here (every store is in a temporary directory), or
     goes if the sentence already says so.
   - A citation in parentheses that carried nothing else is simply removed.
3. **History is told without the source's records.**
   - "Before prompt 04 the tool read them as B's siblings" becomes what the test pins, without the
     prompt.
   - Where the history is the point, it is said by what changed, not by when or by which commit:
     "every store written before shard records were bare file names" in place of "before
     `b04671f`".
4. **The source may be named, generically.** "The source repository", "inherited from the source
   repository" and "at the import commit `6f7f291` (`PROVENANCE.md`)" are allowed. The two
   internalised modules keep their import commit and their pointer to `PROVENANCE.md`, which
   holds the file map, and drop the source's file names: `_timing.py:3` (`utilities.py`) and
   `defaults.py:2` (`config/defaults.py`).
5. **This repository's own citations stay** (§1.1). After the rewrite, every bare "prompt NN"
   left in a file is this campaign's. Where one in a module imported from the source could still
   be read as the source's, it is qualified as "extraction prompt NN".
6. **Only comments and docstrings change.** No statement, expression, name, runtime string, test
   name or assertion changes. §4.3's check proves it, file by file. The two exceptions are §2.3's
   `KNOWN_HITS` entry and §2.4's new module.
7. **Keep the content.** Do not delete an explanation because it carries a citation, and do not
   rewrite prose that names nothing of the source. A sentence that spans lines is rewrapped whole,
   within its comment block or docstring paragraph, and nothing else is restyled. The rewrite adds
   no client vocabulary (the guard's scans).
8. **Scope.** The appendix's 248 lines, read line by line.
   - A tier A or B line is rewritten.
   - A tier C line is rewritten if it cites the source's records, and left if it is this
     repository's or the tool's own, with the reason in the log.
   - A further line the agent finds that cites the source is in scope too, and is recorded.

### 2.2 The false sentences

Each is corrected to what is true at `efedc8d`:

| Where | Says | True |
|---|---|---|
| `tools/sharded_store.py:25-26` | "It puts its own repository root on sys.path, so it runs from any directory with no PYTHONPATH." | It is run as `python -m datastorekit.tools.sharded_store` with the package installed. It changes no `sys.path`. |
| `tools/shard_key_audit.py:24-26` | "the repository root is put on sys.path below so that the script still runs standalone, from any directory, with no PYTHONPATH." | The same, `shard_key_audit`. It imports only the standard library and `datastorekit.shard_paths`, so it pulls in neither `ray` nor `sqlalchemy`. |
| `tests/test_shard_key_audit_copy.py:11`, `tests/test_shard_key_audit_refusals.py:28` | "run here as ``python tools/shard_key_audit.py <primary>``" | Run as `python -m datastorekit.tools.shard_key_audit <primary>`, from an unrelated working directory with no `PYTHONPATH`. |
| `tests/test_sharded_store_script.py:5-6` | "from a directory other than the repository root" | From an unrelated working directory, with `PYTHONPATH` removed. |

Each claim in the "True" column was read from the tools (`grep sys.path` finds no use in either)
and from the tests' `subprocess` calls. A sentence the agent finds false that is not listed here
is corrected too, and recorded.

### 2.3 The guard's known hit (U17)

`tools/shard_key_audit.py:188`'s comment (`e.g. "wavenumber"`, a name of a client's table) is
rewritten under §2.1, so the guard's `test_no_comment` stops finding its one known hit.
`assertNoHits` requires the hits to equal `KNOWN_HITS` in both directions, so the list must be
emptied in the same commit:
- **`KNOWN_HITS`:** each scan's list is empty. The mechanism stays, so that a future hit fails by
  name.
- **The comment inside it** (`:197-199`) goes, and the comment above it (`:192`) says the lists
  are empty.
- **The docstring's "known hits" paragraph** (`:31-35`) says that the list has been empty since
  09, and that any hit fails.
- **`:71`** ("relative to the repository root") is true of this repository, but §2.4's rule
  forbids the phrase, and there is no allow list. It is reworded ("relative to the top of this
  repository").

### 2.4 The new test: `datastorekit/tests/test_prose_names_no_source.py` (U40)

A new module. It is not ported, and is not added to `PORTED`.

**What it reads.** Every `.py` file under `datastorekit/`, the layer and its tests alike, the
module itself included. The set is derived from the filesystem, as `layer_files()` derives its
set. From each file it reads:
- every `COMMENT` token;
- every docstring: the first statement of a module, class or function, when it is a string, by
  `ast`.

It reads no other string. Runtime strings, f-strings and names are code (§2.1, rule 6).

**What it forbids.** Four rules, each named in a failure:

| Rule | Matches |
|---|---|
| a path of the source's layout | `Datastore/`, `tools/`, `prompts/` or `docs/` beginning a path (not preceded by a word character, `/` or `.`) that does not exist relative to this repository's top. So `docs/client-contract.md` and `datastorekit/tools/sharded_store.py` pass, and `docs/datastore-integrity-audit.md`, `tools/shard_key_audit.py` and `prompts/a3-v2-readiness` fail |
| a module of the source | `Datastore.` followed by `SQL`, `tests`, `replication`, `contract`, `object`, `shard_paths`, `store_reader` or `store_inventory`, not preceded by a word character or `.` |
| a name of the source | `repository root`, `REPO_ROOT`, `ObjectFactories`, `RunRegistry`, `main.py`, `config.defaults`, `utilities.py` |
| a campaign or directory of the source | `a3-v2-readiness`, `datastore-generic`, `datastore-integrity`, `datastore-portability`, `store-fingerprint`, `store-retirement`, and `var/` as a path |

These are tier A's rules, which give the 181 lines of §1.1 at `452b3c9`. There is **no allow
list**. The source's commit SHAs and the bare citations of tier C are not matched: they are found
by reading, and the review reads them.

**At least these tests:**

| # | Pins | Fails if |
|---|---|---|
| 1 | No comment or docstring in the package matches any rule; each failure names `file:line rule matched-text`, for every file at once | a line of the appendix is left, or one comes back |
| 2 | The scan reaches the layer and the tests: its file set includes `SQL/ShardedPool.py`, `tests/standin_pool.py`, a ported test module and the module itself, and holds at least 60 files | the walk skips the tests, or comes out empty |
| 3 | Each rule finds its form in a planted comment, a planted module docstring and a planted function docstring (source strings held by the test as runtime strings, so that the module passes its own scan) | a rule, or the docstring reading, is dropped |
| 4 | What is not prose is not read: the same forms in a runtime string, an f-string and a name are not found; a `docs/` path that exists here and a `datastorekit/tools/` path are not found | the scan reads code, or the existence check is lost |

The module's names, docstrings and strings name no client, and its own prose passes its own scan
(hazard 6). No Ray, no store, no client. `tearDownModule` checks that Ray was never initialised.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **A docstring that loses its citation must keep its sense.** Many docstrings open with a
   citation as their subject ("Tests for prompt 06 of `prompts/datastore-integrity` (board item
   S4): every shard…"). Rewrite them so that the first sentence says what the module or class is
   about.
2. **The equivalence of code is checked mechanically** (§4.3). A docstring-only function, an
   `r"""` docstring, a docstring with a backslash, and a comment between decorators are all prose.
   An edit that turns a docstring into a comment, or one that drops a docstring, changes the AST
   and fails the check. Leave each docstring a docstring.
3. **`tools/sharded_store.py`'s docstring is its `--help`** (`description=__doc__`, `:40`), and
   `test_help_carries_the_three_statements` asserts seven of its phrases. Keep each of those
   phrases verbatim: "handles the primary and its shards and nothing else", "<stem>.manifest.json
   is neither copied nor moved", "cannot tell whether a process has the store open", "rollback
   journal", "the caller's job", "A registry-level tool is the place that does both" and "does
   not consult the registry". Only the citation of `:22-23` goes, with the false sentence of
   §2.2. Read `--help` after.
4. **The guard scans the layer's prose for client vocabulary.** A rewritten sentence that
   introduces a client's table, column or package name fails `test_no_string_or_docstring` or
   `test_no_comment`, now with no known hit to absorb it.
5. **`test_layer_is_generic.py` is itself in scope.** Its `:71`, the comments in and above
   `KNOWN_HITS` and its docstring's paragraph change (§2.3). Its vocabulary, its rules and its
   naming of the clients stay: "SecondaryGWKit", "ChamPBH" and "StochasticInstantons" there name
   the clients whose vocabulary it forbids, which is this repository's own fact. A clause there
   that cites a client's campaign (`:178`, "SecondaryGWKit's prompt 08") is decided under §2.1
   rule 8 as a further line, and recorded.
6. **The new module must pass its own scan.** Its docstring explains the rules without quoting a
   forbidden form literally ("a path beginning with the source's package directory", not the
   path). Its planted forms are runtime strings, which it does not read.
7. **A sentence may cite this campaign and the source at once** ("(prompt 04a, U20)" sits beside
   source citations in `schema_description.py`). Only the source's part goes.
8. **Line numbers move.** A docstring that shrinks moves every line after it. Citations made
   before 09, on the board, in the logs and in `docs/client-contract.md` §1–§9, are of their own
   trees, and are not updated (`CLAUDE.md` rule 6). Cite 09's tree in the log.
9. **Do not touch `docs/`, `PROVENANCE.md` or `README.md`.** Their mentions of the source are the
   record of the extraction, not the package's prose.

---

## 4. Verification

1. **The suite, in `venv/`** (Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39): `Ran 480 tests …
   OK` before. After, `480 + N` OK, where N is the loader's count for the new module. The count
   falls nowhere.
2. **The high end**, in a fresh venv in the session scratchpad: Python 3.13.16 / Ray 2.55.1 /
   SQLAlchemy 2.0.46, made with `uv pip install --offline` from the cache 05's work filled, with a
   `git archive` of your tree installed editable. Expect `480 + N` OK and 4 `ResourceWarning`
   lines, as at 08b. **No download**; a pin that does not resolve offline is a stop.
3. **Only prose changed.** For every `.py` file the commit changes under `datastorekit/`, compare
   its `ast.dump` at `452b3c9` and at your tree with every docstring's value replaced by `""`.
   Every file must compare equal, except:
   - `tests/test_layer_is_generic.py`, whose one difference is `KNOWN_HITS`' emptied entry;
   - the new module.

   Comments are not in the AST, so they need no comparison. Record the check's output, file by
   file. (The planner probed the check: a citation removed from a docstring compares equal, and
   08b's change to `ShardedPool.py` compares different.)
4. **The measurement, after.**
   - Tier A's rules give **0** hits (this is test 1).
   - The source's SHAs `b04671f`, `a2bd966` and `e53f323` appear in no comment or docstring.
   - Log 03a §8's method finds only lines that are not the source's: it reads every string, so it
     counts the new module's planted strings, and its unanchored `tools/` matches a
     `datastorekit/tools/` path. List each line it finds, and why it stays.
   - Every tier C line is rewritten or recorded as kept, with its reason.
   - A last reading pass over the 42 files finds no citation of the source.

   Record what remains of each pattern, line by line, and why it stays.
5. **The checks.**
   - `compare_ported_tests.py` exits 0 with "20 module(s) … 1 test(s) declared not ported",
     unchanged. It compares assertion skeletons, which prose does not touch.
   - `black --check datastorekit docs` leaves 70 files unchanged (69 + the module).
   - The layer guard passes with `KNOWN_HITS` empty.
   - `python -m datastorekit.tools.sharded_store --help` carries hazard 3's phrases, and no
     citation.
6. **The deliberate-breakage record.** Each is a diff applied in a scratch copy, never committed.
   Record which tests fail under each, and the verdict over the whole suite. Expected (not probed:
   the planner probed only the rules on today's tree):
   - **(a)** `# see Datastore/shard_paths.py` added to a comment of `SQL/ShardedPool.py`: test 1
     fails, naming the line and "a path of the source's layout".
   - **(b)** "nothing under ``var/``" added to a ported test module's docstring: test 1 fails
     (the tests are scanned).
   - **(c)** `(prompts/a3-v2-readiness, prompt 03)` restored to its comment in
     `SQL/Datastore.py`: test 1 fails, twice over (a path and a campaign).
   - **(d)** `tools/shard_key_audit.py:188`'s comment restored as it was: the guard's
     `test_no_comment` fails (`KNOWN_HITS` is empty), and the new module passes (it is not one of
     its rules).
   - **(e)** the walk restricted to the layer (the tests skipped): test 2 fails, and test 1 no
     longer sees (b).
   - **(f)** docstrings not read (comments only): test 3 fails.
   - **(g)** the existence check dropped from the path rule: test 1 fails on this repository's own
     `docs/` citations (`docs/client-contract.md` in `tests/client/` and `test_neutral_client.py`,
     `docs/extraction/measure_client_vocabulary.py` in the guard), and test 4 fails.
   - **(h)** one docstring edit that also changes a statement: §4.3's check names the file. The
     suite may pass.

   For each, record the verdict line over the whole suite.
7. **The clients.** None is read; 09 changes no call a client makes. Record each client's `HEAD`
   and `git status --short`, at the start and the end, as unchanged.

---

## 5. Acceptance

1. The appendix's lines are rewritten under §2.1, with every tier C line decided and recorded, and
   §2.2's sentences true.
2. §4.3: only prose changed, except the two declared files.
3. §2.3: `KNOWN_HITS` empty, and the guard passes.
4. §2.4: the new module, with every test of its table, passing; §4.4's measurement at 0.
5. §4.1, §4.2, §4.5–§4.7 hold.
6. **The records**, in the same commit:
   - the log, `logs/09-rewrite-the-package-prose.md`, per README §5.1;
   - the board: 09's row and the header; the issue moved from §3 to §4, with a dated "Closed
     (…, prompt 09)" line naming the count rewritten, the guard emptied and the new module;
   - `docs/OPEN_ISSUES.md`: its row deleted, the count **5 → 4** (0 on this repository's boards,
     4 inherited), and the date;
   - `prompts/INDEX.md`: the campaign's line, and its open-issue count (**1 → 0**).

---

## 6. Stop conditions — stop and ask the user

- An existing test fails after the rewrite, or the suite's count falls.
- A line cannot be made true for this package without changing code, or without changing a
  phrase a test asserts.
- §4.3 finds a code difference that the rewrite needs and §2.1 does not allow.
- A tier C line cannot be decided between the source's records and this repository's.
- §2.4's rules flag a line that is true here and cannot be reworded without losing its sense
  (there is no allow list to put it in).
- The high end does not resolve offline.
- Anything would write in a client repository, push, tag, download, or start Ray.

---

## 7. What this prompt changes, and what it does not

- **Files it creates or changes:**
  - the comments and docstrings of the appendix's 42 files under `datastorekit/`, and any further
    file whose prose §2.1 rule 8 finds;
  - `KNOWN_HITS`, its comment and the docstring of `datastorekit/tests/test_layer_is_generic.py`
    (§2.3);
  - `datastorekit/tests/test_prose_names_no_source.py` (new);
  - the log, the board, `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.
- **It changes nothing else.** In particular, it does not change:
  - any line of code, runtime string, test name or assertion (§4.3);
  - `docs/` (the contract and `docs/adoption/` among them), `compare_ported_tests.py`,
    `PROVENANCE.md`, `README.md` or `pyproject.toml`;
  - the campaign README, `CLAUDE.md` or the workflow.
- **It touches no client repository.**
- It makes no tag and pushes nothing. The version stays `0.2.0`; 10 releases.

---

## 8. The log and the board

`logs/09-rewrite-the-package-prose.md`, using README §5.1. There is no `compare_with_source.py`
output (U27). In its place go:
- the port check's output;
- §4.3's check, file by file;
- §4.4's measurement after, with what remains and why;
- tier C's decisions, line by line;
- §2.2's corrections;
- the deliberate-breakage record.

A per-file summary of what was rewritten is enough for tiers A and B (lines, and the kind of
citation removed); the diff is the detail. The log also lists the clients' commits and statuses,
at the start and the end.

`IMPLEMENTATION_STATE.md`: §1's row for 09 (landed, commit, log), the header, and §3/§4 for the
issue.

---

## Appendix — the 248 lines, at `452b3c9`

Paths are under `datastorekit/`. A starred line is tier C (found by reading). An unstarred line is
tier A or B. The guard's `KNOWN_HITS` lines (§2.3) are listed apart.

| File | Lines | At |
|---|---|---|
| `SQL/Datastore.py` | 15 | 60, 68, 79, 124, 153, 192, 409, 441, 477, 517, 583*, 656*, 671, 745*, 847 |
| `SQL/ShardedPool.py` | 33 | 122, 132, 176, 215, 239, 353, 419, 484, 489*, 498, 499*, 801, 880, 937, 1152, 1153, 1351*, 1352, 1482, 1723, 2125, 2128, 2194, 2195*, 2521, 2550, 3097, 3099, 3134*, 3222*, 3388, 3480, 3591 |
| `SQL/factory_base.py` | 3 | 31, 56, 57 |
| `SQL/schema.py` | 11 | 7, 14, 20, 25, 31, 32*, 39, 40, 42, 174, 519 |
| `_timing.py` | 1 | 3 |
| `contract.py` | 3 | 2, 3*, 6 |
| `replication.py` | 9 | 2, 17*, 21, 22*, 28, 128, 196, 197*, 244 |
| `shard_paths.py` | 1 | 28 |
| `store_inventory.py` | 9 | 4*, 6, 19, 30, 72, 82, 222, 227, 273 |
| `store_reader.py` | 5 | 7, 8, 34, 38, 194 |
| `tools/shard_key_audit.py` | 4 | 9*, 19, 24, 25 |
| `tools/sharded_store.py` | 2 | 22, 25 |
| `tests/real_store_fixtures.py` | 6 | 3, 20*, 29, 31, 379, 385* |
| `tests/schema_description.py` | 8 | 3, 6, 9, 12, 15, 16, 183, 184 |
| `tests/shard_store_fixtures.py` | 1 | 91 |
| `tests/standin_pool.py` | 8 | 2, 4, 5, 195, 225, 252, 314*, 397* |
| `tests/test_absolute_shard_record_refused.py` | 7 | 4, 7, 9*, 10*, 26, 28, 123 |
| `tests/test_closed_store_refusals.py` | 2 | 3, 18 |
| `tests/test_copy_move_store.py` | 2 | 3, 5* |
| `tests/test_declared_facts.py` | 3 | 2, 3*, 27 |
| `tests/test_delete_store.py` | 3 | 3, 9, 16 |
| `tests/test_drop_refuses_dangling_references.py` | 5 | 2, 3*, 10, 13*, 23 |
| `tests/test_foreign_key_check.py` | 3 | 2, 4, 45 |
| `tests/test_inventory_declarations.py` | 3 | 2, 17, 48* |
| `tests/test_layer_is_generic.py` | 1 | 71 |
| `tests/test_layer_registry.py` | 4 | 2, 31, 75, 176 |
| `tests/test_one_timestamp_per_write.py` | 2 | 3, 28 |
| `tests/test_prune_at_open.py` | 4 | 2, 3*, 12, 28 |
| `tests/test_read_only_pool.py` | 14 | 2, 5, 6, 9*, 18*, 29, 71, 213*, 240*, 273*, 358*, 625*, 816, 817* |
| `tests/test_reconcile_at_open.py` | 13 | 2, 9, 11*, 31, 230*, 335*, 579*, 733, 746, 912, 985*, 1061, 1092 |
| `tests/test_replicated_write.py` | 6 | 2, 6, 23, 410*, 615, 618* |
| `tests/test_schema_builder.py` | 5 | 2, 9, 11, 20, 25 |
| `tests/test_shard_file_name.py` | 4 | 2, 3, 5*, 50* |
| `tests/test_shard_key_audit_copy.py` | 6 | 2, 4, 6*, 8, 11, 15 |
| `tests/test_shard_key_audit_refusals.py` | 10 | 2, 4, 6, 11, 16*, 28, 118*, 134, 178, 196* |
| `tests/test_shard_paths.py` | 4 | 2, 3, 105*, 106 |
| `tests/test_sharded_store_script.py` | 3 | 2, 3, 6 |
| `tests/test_shardedpool_shard_paths.py` | 6 | 3, 5*, 12*, 16, 25, 141* |
| `tests/test_store_inventory.py` | 5 | 2, 3*, 18, 702, 870* |
| `tests/test_store_reader.py` | 5 | 2, 3*, 12, 19, 182 |
| `tests/test_store_schema.py` | 4 | 2, 3, 29, 411 |
| `tests/test_version_row_at_open.py` | 5 | 2, 10, 14*, 27, 290* |

**Apart (§2.3):** `tests/test_layer_is_generic.py:31-35` (the docstring's paragraph) and
`:192-203` (`KNOWN_HITS` and its comments), and `tools/shard_key_audit.py:188` (`e.g.
"wavenumber"`), which no tier's rule matches; log 03a §8 counts it by hand, and the guard's
`KNOWN_HITS` names it.
