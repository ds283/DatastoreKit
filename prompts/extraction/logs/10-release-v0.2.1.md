# Log 10 — release `v0.2.1`

**Subject:** Make the package ready to be released as v0.2.1 · **Commit:** this commit ·
**Date:** 2026-10-10 · **Model:** Claude Opus 5.5 · **Result:** landed; unpushed and untagged.

The package is ready to be released as **`v0.2.1`** (U36), the release every client adopts in
place of `v0.2.0` (U37). `pyproject.toml` says `0.2.1`, and nothing else in it changed.
`README.md` has a `v0.2.1` status paragraph, the `v0.2.1` pin, and a link to contract §9.
`PROVENANCE.md` has a section for 08a, 08b and 09. Each of the four files under `docs/adoption/`
has an italic line at its head and a dated section, "Addendum: v0.2.1 (extraction prompt 10,
2026-10-10)". Each section gives the new pin, says what changed for that client since `v0.2.0`,
and names by `path:line` every statement it supersedes. `git diff` of the four files has no `-`
line. The board's gates G2–G4 now read `v0.2.1`, each with a dated line saying the tag waits for
CI.

**No line of code changed.** Nothing under `datastorekit/` is touched. The suite stays at
**486**: in `venv/` before and after (`pip show datastorekit` gives `0.2.1` after the offline
reinstall), and at the high end (4 `ResourceWarning` lines). A wheel built offline from an export
of the tree is `datastorekit-0.2.1-py3-none-any.whl`, with 25 entries and none under
`datastorekit/tests/`. Installed at the high pins and run from outside the repository, it behaves
as the prompt's §1.2 says. Breakage (a) fails the release check on `0.2.0`, and (b) fails it on
the test package. The `KeyError` measure (hazard 4) reproduces §1.1's sites. No client's code
depends on the `KeyError`.

**No tag was made and nothing was pushed.** Nothing was downloaded: every venv and build is
`uv … --offline`. No client was written, run, imported or opened. Ray was never started. No issue
was opened, and the index stays at **4**.

Prompt: [`../10-release-v0.2.1.md`](../10-release-v0.2.1.md), with the orchestrator's dispatch note
§0: five corrections, four additions, its checked facts and its conventions. Each is followed as
given, and §2 classifies them. Line numbers under `datastorekit/` are `v0.2.1`'s tree (`cad7bc1`'s
`datastorekit/`, which this commit does not change) unless `v0.2.0` is named.

## 1. What shipped

### 1.1 `pyproject.toml` (§2.1)

`version = "0.2.0"` → `version = "0.2.1"`, the only change. No other file carries the version.

### 1.2 `README.md` (§2.2)

- **Status.** There is a new paragraph for **`v0.2.1`**, above `v0.2.0`'s. It is a fix release:
  - the three defects of 08a and 08b, each in one clause;
  - the prose rewritten for this repository (09);
  - no API added or removed, nothing the layer writes changed, and no message changed;
  - the one exception type that changes, `KeyError` → `RuntimeError`;
  - a link to contract [§9](../../../docs/client-contract.md#9-changes-after-v020).
- **Installing.** The pin is `@v0.2.1`. The sentence "`v0.1.0` remains, for a client that has not
  adopted `key_on_version`" is replaced. The new sentence says that `v0.2.0` and `v0.1.0` remain
  tagged and no tag is moved or deleted, and that every client adopts `v0.2.1`, which fixes defects
  that both earlier releases carry. It is written as of the tag.
- **Using it.** One new item, "What changed after `v0.2.0`", linking `#9-changes-after-v020`.
- Nothing else changed. The "Supported versions" table and "Developing" are as they were.

### 1.3 `PROVENANCE.md` (§2.3)

A new section, "Prompts 08a, 08b and 09: fixes and prose (`v0.2.1`)", is added after "Prompt 06".
Nothing above it changed. It has three parts:
- **The three fixes.** A table names each issue with its prompt, commit and test module. It says
  they have no source, that SGK's frozen copies still carry them (U3's freeze; U33 fixed them before
  G2), and that SGK receives them by adopting `v0.2.1`.
- **09 changed prose only.** It names 12 layer files and `SQL/ShardedPool.py`, and the test modules.
  With docstrings blanked, the AST is the same before and after (my own check, §5.6). From `v0.2.1`
  no layer file equals its SGK source in its comments, except the seven 09 did not touch. "The
  differences allowed" is not extended.
- **The files each prompt changes, and its log.**

### 1.4 The addenda (§2.4, U37)

Each file gains an italic line at its head and an unnumbered section,
`## Addendum: v0.2.1 (extraction prompt 10, 2026-10-10)`.
- In the README, the italic line comes after 07a's italic line, and the section comes after §6.
- In each checklist, the italic line comes after the bullet list under the title, and the section
  comes after item 10 and before the appendix. The ten items keep their numbers.

Each section gives:
- the pin `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.1`, and that the client
  adopts `v0.2.1` (U37);
- what changed for that client, with contract §9's rows as the detail;
- a supersession table (addition 2);
- the rule for line citations.

The four tables are repeated in §4.

| File | Lines added | Lines removed |
|---|---|---|
| `docs/adoption/README.md` | 74 | 0 |
| `docs/adoption/secondarygwkit.md` | 83 | 0 |
| `docs/adoption/champbh.md` | 58 | 0 |
| `docs/adoption/stochasticinstantons.md` | 57 | 0 |

### 1.5 The records

- This log.
- The board: §1's row for 10, the header, and §2's gates G2–G4 (§2.5). Each gate title says
  `v0.2.1` (U37). Each gate gains a dated line: `v0.2.1` is ready to be tagged on 10's commit once
  CI passes there at both ends (as U23, U28), 10 makes no tag, and the line names the client's
  addendum. The lines recording `v0.1.0` and `v0.2.0` are unchanged.
- `prompts/INDEX.md`: the campaign's line.
- `docs/OPEN_ISSUES.md` is unchanged at **4**: no issue opened.

## 2. Deviations from the prompt

1. **Correction 1: `venv/`'s reinstall is `uv pip install --offline --no-deps --python
   ./venv/bin/python -e .`**, not hazard 7's `pip install --no-deps -e .`, which would download
   `setuptools`. Its output was `- datastorekit==0.2.0`, `+ datastorekit==0.2.1`, exit 0.
   `pip show datastorekit` gives `Version: 0.2.1`, with the editable location in this checkout.
   **STRUCTURALLY REQUIRED.**
2. **Correction 2: the reinstall wrote `datastorekit.egg-info/` at the root, and I removed it.**
   After the removal:
   - `importlib.metadata.version("datastorekit")` is `0.2.1`;
   - the package imports from the source tree;
   - `git status --short --ignored` lists exactly dispatch's entries.

   **STRUCTURALLY REQUIRED.**
3. **Correction 3: every citation of log 08a's client measurement says "log 08a §3"**: in the
   README's addendum, in each checklist's addendum, and in this log. Log 08a has no §2.5.
   `PROVENANCE.md` does not cite it. **STRUCTURALLY REQUIRED.**
4. **Correction 4: the contract's rows have no anchors.** Each behaviour links its subsection
   (`#91-prompt-08a` or `#92-prompt-08b`), and the row is named by its "Change" cell. Recorded as
   found. **STRUCTURALLY REQUIRED.**
5. **Correction 5: "The campaign closes at 07b" is one line**, 07a's `:156`, and G2's `v0.2.0` is
   `:154`. They are cited separately, at their committed numbers (item 7). **STRUCTURALLY
   REQUIRED.**
6. **Additions 1–4** are followed as given: the order of work, a supersession table per addendum,
   the name-and-link check as a scratch script, and separate exports for (a) and (b). Each is an
   **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
7. **The supersession tables cite each file's line numbers as committed.** §2.4 puts the italic
   line at each file's head, so every later line moves down by five: after `:5` in the README,
   `:14` in SGK's, `:15` in CPBH's and `:13` in SI's. Citing the planner's numbers would make the
   tables false in the file they are in. Each table cites the committed number and says that
   07a's file (`dd45243`) has each line five lines earlier. The mapping:
   - README: `:8`→`:13`, `:24-26`→`:29-31`, `:35`→`:40`, `:154`→`:159`, `:156`→`:161`,
     `:174`→`:178-179`;
   - SGK: `:17`→`:21-22`, `:25-27`→`:30-32`, `:292-297`→`:297-302`, `:301`→`:306`;
   - CPBH: `:18`→`:22-23`, `:254-255`→`:259-260`, `:374`→`:379`;
   - SI: `:16`→`:20-21`, `:255-257`→`:260-262`, `:348`→`:353`;
   - `:3`, `:6`, `:6` and `:5` are above the insert and do not move.

   The line-citation rule is cited as the two lines that hold it (`:21-22`, not `:17`'s one).
   **STRUCTURALLY REQUIRED.**
8. **Two SGK statements the prompt's table does not name are superseded**, by §2.4's "a statement
   the table does not name, that is no longer true of `v0.2.1`, is superseded too":
   - `secondarygwkit.md:187-188` (07a's `:182-183`) says "`Datastore/SQL/ObjectFactories/base.py`
     equals `datastorekit/SQL/factory_base.py` byte for byte". 09 rewrote `factory_base.py`'s
     docstrings. My AST check (§5.6) gives it as prose-only, so its code is SGK's and the point of
     item 5 stands.
   - `secondarygwkit.md:203-207` (07a's `:198-202`) says "No call changes behaviour", with the one
     difference a read-only open makes. At `v0.2.1` there are three more differences, though none
     changes what SGK's calls use.

   Both are in SGK's table (§4.2). **STRUCTURALLY REQUIRED.**
9. **§1.1's account of one archived script is not exact.** §1.1 says the two archived scripts
   with a `try` around a `ShardedPool(` each catch any exception and record its type. Read through
   `git grep -A` at `b510bc9`:
   - `m4c_open_rw.py:38` does: `except BaseException as e: result["raised"] = type(e).__name__`;
   - `m7_messages.py:184` catches `ReadOnlyMiss` only (`:197`), and records its message and fields.

   The sites are §1.1's, and neither catches `KeyError` around a pool, so no stop condition
   applies. SGK's addendum says what each catches. **STRUCTURALLY REQUIRED** (an expectation
   corrected).
10. **The dispatch note's lines for `object_get_vectorized` are one too low.** At `cad7bc1` the
    method is `:3327-3351` (the `def` at `:3327`, the closing `)` at `:3351`), its membership test
    `:3339`, and the payload copy `:3348`. The note gives `:3326-3350`, `:3338` and `:3347`. The
    CPBH and SI addenda cite what I found. The conclusion is unchanged: a bare key is refused
    before the payload line. **STRUCTURALLY REQUIRED** (an expectation corrected).
11. **The high-end suite overran the tool's 600-second foreground limit.** It ran 663 s, so the
    tool moved it to the background. Its output went to the scratch file as the convention asks.
    I took its verdict only after it exited (exit 0), and ran nothing that depended on it in the
    meantime. Building (a) and (b) ran while it finished. **UNINTENDED DRIFT**, with no effect on
    any result.
12. **The exports are of the working tree before the records were written**, made with
    `git archive $(git stash create)`. That is commit object `612b73a`, whose tree equals the
    working tree at the time (`git diff --quiet 612b73a` held). `git stash create` writes no ref,
    and `git stash list` stayed empty. It does not touch the index or the working tree. That tree
    differs from this commit's in the records (this log, the board, `prompts/INDEX.md`). It also
    differs in three later edits to lines this prompt added: the rewrap of one bullet in
    `PROVENANCE.md`, and the one-sentence form of the `KeyError` and refused-open bullets in the
    three checklist addenda (§2.4's "one sentence"). None of these is in the wheel or read by the
    suite. A wheel rebuilt offline from `git archive` of the committed tree has the same `RECORD`
    SHA-256, `f840ffa4…` (§5.3). **IMPLEMENTATION CHOICE.** I found the stale sentence after the
    first commit, and amended that commit once to correct it, before anything else landed.
13. **The release check has an assertion script.** `assert_release.py` (§5.3) asserts the wheel's
    name, its `Version`, its entry count, that no entry is under `datastorekit/tests/`,
    `importlib.metadata.version`, and that `import datastorekit.tests` fails. This lets (a) and (b)
    be recorded as failed assertions (§4.5). **IMPLEMENTATION CHOICE.**
14. **`PROVENANCE.md` also names 09's test modules and gives the file count, 30.** §2.3 names the
    layer files only. **IMPLEMENTATION CHOICE**, so that "the files each prompt changes" is
    complete.
15. **I read `origin` with `git ls-remote --tags origin`**, to confirm the dispatch state: `v0.1.0`
    peels to `68db557` and `v0.2.0` to `240028e`, with no other tags. It reads refs only, and
    downloads and writes nothing. **IMPLEMENTATION CHOICE.**

## 3. The hazards (§3)

1. **Additive documents.** `git diff --numstat -- docs/adoption` gives 74/0, 83/0, 58/0 and 57/0,
   and `git diff -- docs/adoption | grep '^-' | grep -v '^--- '` finds nothing. Each insert was made
   by a scratch helper that only adds lines, and the later wording fixes changed only lines this
   prompt added. `docs/client-contract.md` is unchanged (`git diff --quiet`).
2. **Names and links.** Every one resolves (§5.5).
3. **The tag does not exist yet.** No document says `v0.2.1` is tagged:
   - the README and the addenda state the pin, and say that `v0.2.0` and `v0.1.0` "remain tagged";
   - the gates say `v0.2.1` "is ready to be tagged … once CI passes there", and that 10 makes no
     tag.
4. **No client is re-measured.** The addenda cite 07a's measurements, log 08a §3 and my re-run of
   §1.1's `KeyError` measure (§5.4). That measure gives §1.1's sites exactly. §2 item 9 records the
   one inexact description, which does not change the finding.
5. **Offline only.** Every venv (`uv venv --offline`), install (`uv pip install --offline`) and
   build (`uv build --offline`) resolved from the cache. `setuptools` (the build backend), `ray`
   2.55.1 and `sqlalchemy` 2.0.46 resolved offline. Nothing was downloaded.
6. **`shard_key_audit` has no `--help`.** It exits 2 with `!! No such file: <cwd>/--help`, as at
   05 (§5.3). This is not a failure.
7. **`venv/`'s metadata.** I reinstalled with correction 1's command and removed the `egg-info`
   (correction 2). `pip show datastorekit` gives `Version: 0.2.1`, and the suite gives 486 OK
   (§5.1).

## 4. The supersession tables (addition 2)

Each table is as committed in its addendum. Line numbers are each file's at this commit; 07a's
numbers are in §2 item 7.

### 4.1 `docs/adoption/README.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `:3` | written "against the package at **`v0.2.0`** (`240028e`)" | 07a's measurements stay true of `v0.2.0`; the addendum gives `v0.2.1` |
| `:13` | each checklist says what its client must do "to depend on `datastorekit` at `v0.2.0`" | at `v0.2.1`: each checklist with its addendum |
| `:29-31` | "All three adopt **`v0.2.0`**" | all three adopt `v0.2.1` (U37) |
| `:40` | the pin `…@v0.2.0` | the pin `…@v0.2.1` |
| `:159` | "G2 (SGK has adopted `v0.2.0`, U29)" | G2, G3 and G4 each hold when that client has adopted `v0.2.1` (U37) |
| `:161` | "The campaign closes at 07b" | it closes at extraction prompt 11 (U33); 07b was withdrawn unwritten |
| `:178-179` | "one under `datastorekit/` is at `v0.2.0` (`240028e`)" | still so for 07a's text; a `datastorekit/` line in an addendum is at `v0.2.1` |

### 4.2 `docs/adoption/secondarygwkit.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `:6` | the package at **`v0.2.0`** | at `v0.2.1`, with the addendum |
| `:21-22` | a `datastorekit/` line is the package's at `v0.2.0` | still so for 07a's text; a `datastorekit/` line in the addendum is at `v0.2.1` |
| `:30-32` | against `v0.2.0`, 11 byte-identical, the tools by D-tool, four by 06's additions | `v0.2.0`'s count. At `v0.2.1` only the six 09 did not touch can be byte-identical |
| `:187-188` *(not in the prompt's table)* | `base.py` equals `factory_base.py` byte for byte | they differ in comments and docstrings (09) |
| `:203-207` *(not in the prompt's table)* | "No call changes behaviour", and the one read-only difference | three more differences, none changing what SGK's calls use |
| `:208-211` | the in-place update "is SGK's own behaviour, unchanged" | `v0.2.1` sends copies, and SGK reads nothing back (log 08a §3) |
| `:297-302` | item 8's reasoning, through `v0.2.0` | extended to `v0.2.1`: nothing written changes (§9.1, §9.2), and 09 changes no code |
| `:306` | G2 holds when SGK has adopted `v0.2.0` | `v0.2.1` (U37) |

### 4.3 `docs/adoption/champbh.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `:6` | the package at **`v0.2.0`** | at `v0.2.1`, with the addendum |
| `:22-23` | a `datastorekit/` line is the package's at `v0.2.0` | still so for 07a's text; the addendum's lines are at `v0.2.1` |
| `:259-260` | "It also adds that mapping to every payload dict in place" | `v0.2.1` sends copies, and leaves CPBH's dicts as passed |
| `:379` | G3 holds when CPBH has adopted `v0.2.0` | `v0.2.1` (U37) |

### 4.4 `docs/adoption/stochasticinstantons.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `:5` | the package at **`v0.2.0`** | at `v0.2.1`, with the addendum |
| `:20-21` | a `datastorekit/` line is the package's at `v0.2.0` | still so for 07a's text; the addendum's lines are at `v0.2.1` |
| `:260-262` | the package "adds it to each payload dict in place" | `v0.2.1` sends copies, and leaves SI's dicts as passed; `plot_InstantonSolutions.py:697-702` is safe (log 08a §3) |
| `:353` | G4 holds when SI has adopted `v0.2.0` | `v0.2.1` (U37) |

**Considered and not superseded.** I read every statement in the four files for whether it is
still true of `v0.2.1`. These stay:
- **Every `datastorekit/` line citation in 07a's text.** Each is read at `v0.2.0`, by the files'
  own rule.
- **SGK's `:220` "The 8 modules moved verbatim".** 09 rewrote those modules' prose, but the sentence
  says how they came here at 01, and SGK still deletes them.
- **SGK's `:190`, "`v0.2.0`'s one feature reaches none of SGK's classes".** This is still true: the
  feature is unchanged in `v0.2.1`.
- **SGK's inherited issues (`:355-359`).** They are still four, and still inherited.
- **CPBH's and SI's item 8 refusal orders.** Every refusal raises the same exception at `v0.2.1`
  (contract §9.2: no refusal or exception changes). The `KeyError` path sits behind the
  `StoreSchemaMismatch` that stops every CPBH and SI store first.
- **The adoption README's §4 table of contract §1–§8.** It lists what a client gives, and §9 adds
  nothing a client gives.

## 5. Verification performed

`<scratch>` = `/private/tmp/claude-35086/-Users-ds283-Documents-Code-DatastoreKit/62950adb-e9b5-4588-9835-f20b562d2b04/scratchpad/agent10`.

### 5.1 The suite (§4.1)

Every run was in the foreground (but see §2 item 11), with its output in `<scratch>/out/` and the
verdict grepped from it.

| Where | When | Result | `ResourceWarning` lines | `datastorekit` |
|---|---|---|---|---|
| `venv/` (3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39) | before any change | `Ran 486 tests in 210.339s` `OK` | 0 | 0.2.0 |
| `venv/` | after `pyproject.toml` and the reinstall | `Ran 486 tests in 321.987s` `OK` | 0 | 0.2.1 |
| `venv/` | after every document edit | `Ran 486 tests in 205.172s` `OK` | 0 | 0.2.1 |
| `<scratch>/venv-high` (3.13.16 / 2.55.1 / 2.0.46, SQLite 3.53.4), `git archive 612b73a` installed editable | after every document edit | `Ran 486 tests in 663.242s` `OK` | 4 | 0.2.1 |

The count is **486** before and after, at both ends. The guard (`test_layer_is_generic`, with every
`KNOWN_HITS` list empty) and `test_prose_names_no_source` are in it.

### 5.2 The checks (§4.2)

`compare_ported_tests.py`, before and after, exit 0, its last line:

```
OK: 20 module(s) keep their source's tests, classes and assertion skeletons; 1 test(s) declared not ported
```

`./venv/bin/black --check datastorekit docs`, before and after: `70 files would be left
unchanged.` No `.py` file changed, so `black` had nothing to format.

### 5.3 The release check (§4.3)

**The build.** I exported commit object `612b73a` (§2 item 12) with
`git archive 612b73a | tar -x -C <scratch>/exports/release`, then ran
`uv build --offline --wheel --out-dir <scratch>/wheels/release <scratch>/exports/release` (exit 0).
Nothing was built in the checkout.

| | |
|---|---|
| Wheel | `datastorekit-0.2.1-py3-none-any.whl` |
| Size | 97,849 bytes |
| Entries | **25**: none under `datastorekit/tests/`, 3 under `datastorekit/tools/` |
| SHA-256 | `883fa2c41fa2dd616e30b1e9eac04319b7695e765c186682887818584e6aed14` |
| `RECORD` SHA-256 | `f840ffa4c28f1d40f6578abb56a033d6faf4356f4877c62f60ebf75ab2d96c5e` |
| `WHEEL` | `Generator: setuptools (84.0.0)` |
| `METADATA` | `Name: datastorekit`, **`Version: 0.2.1`**, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43`, `Requires-Dist: sqlalchemy<2.1,>=2.0.39` |

**The file list:**

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
datastorekit-0.2.1.dist-info/licenses/LICENSE
datastorekit-0.2.1.dist-info/METADATA
datastorekit-0.2.1.dist-info/WHEEL
datastorekit-0.2.1.dist-info/top_level.txt
datastorekit-0.2.1.dist-info/RECORD
```

The size, 97,849 bytes, is the orchestrator's. Only the SHA-256 is mine to record; wheel bytes are
not reproducible across builds.

**The install.** `uv venv --offline -p /opt/local/bin/python3.13 <scratch>/venv-release`, then
`uv pip install --offline --python <scratch>/venv-release/bin/python <the wheel> "ray==2.55.1"
"sqlalchemy==2.0.46"`. The install resolved 20 packages and installed 20, exit 0, not editable.
Python 3.13.16, SQLite 3.53.4.

**The commands.** `<scratch>/probe/release_check.sh` ran them from `<scratch>/outside-release`, a
directory outside the repository, with `PYTHONPATH` unset. `<R>` is the venv's `site-packages`.

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

$ python -c "from datastorekit.contract import VERSION_SERIAL_KEY, require_version_serial; ..."
<R>/datastorekit/contract.py
'_version_serial' 3
exit=0

$ python -c "import datastorekit.tests"
ModuleNotFoundError: No module named 'datastorekit.tests'
exit=1

$ python -c "import importlib.metadata as m; print(m.version(\"datastorekit\"))"
0.2.1
exit=0

$ python -m datastorekit.tools.sharded_store --help
exit=0
usage: python -m datastorekit.tools.sharded_store [-h] {copy,move} src dst

Copy or move a closed ShardedPool datastore under a new name.
... (34 lines)

$ python -m datastorekit.tools.shard_key_audit
usage: <R>/datastorekit/tools/shard_key_audit.py <path-to-primary-database>
exit=2

$ python -m datastorekit.tools.shard_key_audit --help
!! No such file: <cwd>/--help
exit=2
```

The first two `exit=0` lines are a pipe's. The first script prints "20 modules imported" only once
all 20 have imported, and the `contract` import, run again without the pipe, exits 0.
`sharded_store --help` prints 34 lines. 05 printed 35, and 09 rewrote the tool's prose.

**The assertions**, from `<scratch>/probe/assert_release.py <wheel> <venv python>`:

```
PASS wheel name: datastorekit-0.2.1-py3-none-any.whl
PASS METADATA Version: Version: 0.2.1
PASS no entry under datastorekit/tests/: 0 of 25 entries
PASS 25 entries: 25
PASS importlib.metadata.version: 0.2.1
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
RESULT: OK
```

**The release check passes.** `git status --short --ignored` lists no `build/`, `dist/` or
`*.egg-info` in the checkout (§5.8).

### 5.4 The `KeyError` measure (hazard 4)

The three clients were read through `git -C <client> grep` only, at the checklists' commits:
1. `git grep -n 'except KeyError\|except (.*KeyError' <commit> -- '*.py'`, in the whole tree and
   then with `':!Datastore/'`;
2. `git grep -n -B3 'ShardedPool(' <commit> -- '*.py' ':!Datastore/'`, filtered for a `try:` line.

```
== SecondaryGWKit at b510bc9: measure 1 (except KeyError), all
b510bc9:RunRegistry/__init__.py:606:    except (KeyError, TypeError, ValueError):
b510bc9:RunRegistry/tests/test_run_registry.py:489:                except (ValueError, KeyError, TypeError):
-- outside Datastore/:
b510bc9:RunRegistry/__init__.py:606:    except (KeyError, TypeError, ValueError):
b510bc9:RunRegistry/tests/test_run_registry.py:489:                except (ValueError, KeyError, TypeError):
== SecondaryGWKit: measure 2 (try within 3 lines before ShardedPool( ), outside Datastore/
b510bc9:prompts/datastore-generic/orchestrator/measure-07/scripts/m7_messages.py-184-        try:
b510bc9:prompts/datastore-generic/orchestrator/measure-09/scripts/m4c_open_rw.py-38-    try:

== ChamPBH at 52142d7: measure 1 (except KeyError), all
-- outside Datastore/:
== ChamPBH: measure 2 (try within 3 lines before ShardedPool( ), outside Datastore/

== StochasticInstantons at 7bb3efd: measure 1 (except KeyError), all
-- outside Datastore/:
== StochasticInstantons: measure 2 (try within 3 lines before ShardedPool( ), outside Datastore/
```

Each SGK site was read through `git grep -B/-A`:
- `RunRegistry/__init__.py:604-607` reads `manifest["created"]` in `_created_epoch`;
- `RunRegistry/tests/test_run_registry.py:487-490` reads a status file's JSON (`"units_done"`);
- `m7_messages.py:184-198` catches `ReadOnlyMiss` only;
- `m4c_open_rw.py:38-46` catches `BaseException` and records `type(e).__name__`.

**These are §1.1's sites, and no client catches the `KeyError` around a pool.** CPBH and SI catch
`KeyError` nowhere, not even inside their own `Datastore/`. No stop.

### 5.5 Names and links (hazard 2)

**The method.** `<scratch>/probe/check_links.py`, a scratch script that is never committed, ran
over `README.md`, `PROVENANCE.md` and the four adoption files. It does three things:
- **Links.** It resolves every relative Markdown link: the file relative to the document, then the
  anchor among the target's headings, outside code fences, by GitHub's rule (lower-case; drop every
  character that is not a letter, digit, space, hyphen or underscore; spaces to hyphens; duplicates
  suffixed). This is the rule behind the README's existing `#8-version-keyed-lookups-v020-prompt-06`.
- **Paths.** It checks every backticked path under `datastorekit/`, `docs/`, `prompts/` or
  `.github/`, and a `:line` or `:a-b` suffix against the file's length.
  - In a checklist's 07a text, `datastorekit/` paths are checked at `240028e` through `git show`,
    since that text cites `v0.2.0`.
  - A checklist's `docs/` and `prompts/` paths are checked only when they are this repository's
    (`docs/adoption/`, `docs/extraction/`, `docs/client-contract.md`, `prompts/extraction/`). The
    others are the client's.
- **Names.** It lists every dotted `datastorekit.` name. `<scratch>/probe/import_names.py` imports
  each in `venv/`, resolving by the longest importable module prefix and then `getattr`. It also
  imports the bare names the new text uses.

**The output** (summarised; the full report is `<scratch>/out/check-links.txt`):
- **43 relative links, every one resolved.** Among them:
  - `docs/client-contract.md#9-changes-after-v020` (README ×2, each addendum), heading
    `docs/client-contract.md:249`;
  - `../client-contract.md#91-prompt-08a` and `#92-prompt-08b`, headings `:254` and `:263`;
  - each checklist's `#addendum-v021-extraction-prompt-10-2026-10-10`, from its own italic line and
    from the README's addendum;
  - `README.md#addendum-v021-extraction-prompt-10-2026-10-10` from each checklist;
  - the README's existing eight contract anchors, `PROVENANCE.md`, `LICENSE`,
    `.github/workflows/tests.yml`, `datastorekit/tests/client/` and its `registry.py`, and
    `docs/extraction/`.

  There are 2 external links (`https://github.com/ds283/SecondaryGWKit`, `https://www.ray.io/`).
  They were not followed.
- **335 backticked paths.**
  - 198 checked and present. 65 of them are 07a's `datastorekit/` citations, checked at
    `240028e`; 35 carry a line suffix checked at the working tree. Among those 35 are every
    `datastorekit/SQL/ShardedPool.py:…` citation of the addenda and every `docs/adoption/…:…` of
    the supersession tables.
  - 133 are a client's paths, and were not checked here.
  - 4 are patterns (`datastorekit/<same>` and the like).
  - None failed.
- **22 dotted names, every one importable in `venv/`:**
  - `datastorekit.SQL`, `.SQL.Datastore`, `.SQL.Datastore.Datastore` (the actor class),
    `.SQL.ShardedPool`, `.SQL.factory_base`, `.SQL.schema`;
  - `datastorekit.__file__`, `._timing`, `.contract`, `.contract.VERSION_LABEL`,
    `.contract.VERSION_SERIAL_KEY`, `.contract.require_version_serial`, `.defaults`,
    `.replication`, `.shard_paths`, `.store_inventory`, `.store_inventory.read_inventory`,
    `.store_reader`, `.tests`, `.tools`, `.tools.shard_key_audit`, `.tools.sharded_store`.

  The bare names the new text uses are also present:
  - `ShardedPool.object_get_vectorized`, `._close_refused_open`, `._open` and `._read_shard_data`;
  - `datastorekit.replication.ReadOnlyMiss`;
  - `test_layer_is_generic.KNOWN_HITS` (all four lists empty);
  - the four new test modules.
- **The contract rows** each addendum names exist under §9.1 and §9.2 with those "Change" cells.
  So do the issue names in `PROVENANCE.md` (the board's §4) and the commits `f938844`, `efedc8d`
  and `cad7bc1`.
- **The `v0.2.1` line citations** in the addenda were read at the tree:
  - `ShardedPool.py:203-207` is the guard around `_open`;
  - `:375-408` is `_close_refused_open`;
  - `:1071-1072` is the `continue` for a table the mapping lacks;
  - `:1100-1103` is the mismatch `RuntimeError`;
  - `:3327-3351` is `object_get_vectorized`, with `:3339` the membership test and `:3348` the copy.

`RESULT: OK` for both scripts.

### 5.6 What changed since `v0.2.0` (§1.1, re-checked)

`<scratch>/probe/ast_check.py` compares each layer file at two commits through `git show`. It
reports a file as unchanged (byte-equal), prose-only (`ast.dump` equal with every module, class
and function docstring blanked), or code.
- **`240028e` → `cad7bc1`:**
  - unchanged, 7: `SQL/ClientPool.py`, `SQL/ProfileAgent.py`, `SQL/SerialPoolBroker.py`,
    `SQL/__init__.py`, `__init__.py`, `object.py`, `tools/__init__.py`;
  - prose-only, 12: `SQL/Datastore.py`, `SQL/factory_base.py`, `SQL/schema.py`, `_timing.py`,
    `contract.py`, `defaults.py`, `replication.py`, `shard_paths.py`, `store_inventory.py`,
    `store_reader.py`, `tools/shard_key_audit.py`, `tools/sharded_store.py`;
  - code, 1: `SQL/ShardedPool.py`.
- **`efedc8d` → `cad7bc1` (09 alone):** 13 prose-only, `SQL/ShardedPool.py` among them, and 7
  unchanged.
- `git diff --stat 240028e efedc8d -- datastorekit/` touches only `SQL/ShardedPool.py` (+50 −2)
  and the three new test modules. `test_prose_names_no_source.py` is the fourth added since
  `v0.2.0`.

### 5.7 The documents (§4.4)

Every remaining `v0.2.0`, by line, with why it stays:

| File | Lines | Why it stays |
|---|---|---|
| `README.md` | `:19` | history: the `v0.2.0` status paragraph |
| | `:27` | history: "where `v0.2.0`'s feature comes from" |
| | `:62` | the "remain tagged" sentence |
| | `:93` | the name of contract §9, "Changes after `v0.2.0`" |
| `PROVENANCE.md` | `:89` | history: 06's section title |
| | `:139` | history: the seven files "unchanged since `v0.2.0`" |
| `docs/adoption/README.md` | `:3`, `:13`, `:29`, `:30`, `:40`, `:159`, `:179` | statements the addendum supersedes (`:30` is inside `:29-31`) |
| | `:9`, `:10` | the italic line: "since `v0.2.0`", "true of `v0.2.0`" |
| | `:206`, `:208`, `:215`, `:221`, `:227`, `:228`, `:252`, `:262`–`:268` | the addendum's own comparisons with `v0.2.0`, and its table |
| `docs/adoption/secondarygwkit.md` | `:6`, `:22`, `:30`, `:32`, `:297`, `:306` | statements the addendum supersedes |
| | `:190` | history, still true: `v0.2.0`'s feature reaches no SGK class |
| | `:18`, `:19` | the italic line |
| | `:366`, `:369`, `:376`, `:381`, `:391`, `:415`, `:420`, `:430`–`:437` | the addendum's own comparisons, and its table |
| `docs/adoption/champbh.md` | `:6`, `:23`, `:379` | statements the addendum supersedes |
| | `:19`, `:20` | the italic line |
| | `:409`, `:412`, `:419`, `:421`, `:430`, `:442`, `:452`–`:455` | the addendum's own comparisons, and its table |
| `docs/adoption/stochasticinstantons.md` | `:5`, `:21`, `:353` | statements the addendum supersedes |
| | `:17`, `:18` | the italic line |
| | `:380`, `:383`, `:390`, `:399`, `:412`, `:422`–`:425` | the addendum's own comparisons, and its table |

`git diff -- docs/adoption` has no `-` line (hazard 1), and `docs/client-contract.md` is
unchanged.

### 5.8 The tree and the clients (§4.6)

- `git status --short --ignored` at the end, before staging, shows the ten files of §7's list
  as modified or new, and the ignored entries of dispatch: `.idea/`, `venv/`, and the five
  `__pycache__/` directories (`datastorekit/`, `datastorekit/SQL/`, `datastorekit/tests/`,
  `datastorekit/tests/client/`, `docs/extraction/`). There is no `build/`, `dist/` or `*.egg-info`.
- `git diff --quiet` holds for `datastorekit/`, `docs/client-contract.md`, `docs/extraction/`,
  `.github/`, `CLAUDE.md`, `LICENSE`, `.gitignore`, `prompts/extraction/README.md` and
  `prompts/extraction/orchestrator/`.
- No Ray process was up at the start or the end (`pgrep -x raylet`, `pgrep -x gcs_server`,
  `pgrep -f 'ray::'`).

The clients, read only through `git rev-parse` and `git status`, and through `git grep` for §5.4,
were the same at the start and at the end. `cmp` of the two `git status --short` captures is
silent.

| Client | Commit | Branch | `git status --short` |
|---|---|---|---|
| SGK | `b510bc9` | `handover-remedial` | empty |
| CPBH | `52142d7` | `main` | 23 untracked entries (none read) |
| SI | `7bb3efd` | `main` | empty |

## 6. The deliberate-breakage record (§4.5)

**The method** (addition 4):
1. Each breakage has its own export, `git archive 612b73a` into `<scratch>/exports/break-a` or
   `break-b`.
2. The diff below was checked there with `git apply --check`, applied with `git apply`, and the
   applied export checked with `git apply -R --check`.
3. Each export was built with `uv build --offline --wheel`, installed offline into its own Python
   3.13.16 venv with `ray==2.55.1` and `sqlalchemy==2.0.46`, and checked with `assert_release.py`
   from `<scratch>/outside-release`.

Neither breakage is committed.

**(a) `pyproject.toml`'s version left at `0.2.0`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -4,7 +4,7 @@
 
 [project]
 name = "datastorekit"
-version = "0.2.1"
+version = "0.2.0"
 description = "A sharded SQLite datastore layer (Datastore / ShardedPool) on Ray and SQLAlchemy"
 requires-python = ">=3.12"
 dependencies = [
```

`git apply --check` passed on the clean export, and `git apply -R --check` on the applied one. The
wheel is `datastorekit-0.2.0-py3-none-any.whl`, 97,852 bytes, 25 entries, none under `tests/`,
`METADATA` `Version: 0.2.0`.

```
FAIL wheel name: datastorekit-0.2.0-py3-none-any.whl
FAIL METADATA Version: Version: 0.2.0
PASS no entry under datastorekit/tests/: 0 of 25 entries
PASS 25 entries: 25
FAIL importlib.metadata.version: 0.2.0
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
RESULT: FAILED (3): wheel name, METADATA Version, importlib.metadata.version
```

**Verdict:** the `METADATA` and `importlib.metadata.version` assertions fail, naming `0.2.0`, as
§4.5 says. The wheel's name fails with them.

**(b) The `exclude` line removed from `pyproject.toml`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -14,4 +14,3 @@
 
 [tool.setuptools.packages.find]
 include = ["datastorekit*"]
-exclude = ["datastorekit.tests", "datastorekit.tests.*"]
```

`git apply --check` passed on the clean export, and `git apply -R --check` on the applied one. The
wheel is `datastorekit-0.2.1-py3-none-any.whl`, 301,799 bytes, **71 entries, 46 under
`datastorekit/tests/`** (`datastorekit/tests/__init__.py`, `real_store_fixtures.py`,
`schema_description.py`, …).

```
PASS wheel name: datastorekit-0.2.1-py3-none-any.whl
PASS METADATA Version: Version: 0.2.1
FAIL no entry under datastorekit/tests/: 46 of 71 entries
FAIL 25 entries: 71
PASS importlib.metadata.version: 0.2.1
FAIL import datastorekit.tests fails: exit=0 (no error)
RESULT: FAILED (3): no entry under datastorekit/tests/, 25 entries, import datastorekit.tests fails
```

**Verdict:** the wheel lists files under `datastorekit/tests/`, and `import datastorekit.tests`
succeeds, as at 05's (f). The counts are the orchestrator's: 71 entries, 46 under `tests/`.

## 7. Observations not acted on

1. **SGK's checklist says `docs/OPEN_ISSUES.md:685`** (`secondarygwkit.md:347`), which is SGK's
   index, not this repository's 26-line one. The checklist's rule, that a `path:line` with no
   commit named is SGK's, makes it right. Only the link check's prefix filter had to learn it.
   Nothing to change.
2. **Several pre-existing lines of `README.md` and `PROVENANCE.md` run past 100 columns** (tables
   and long link lines). One long line in SGK's addendum carries an unbreakable path,
   `m7_messages.py:184`. None is a defect.
3. **The scratch tools** are in `<scratch>/probe/`, not in the repository:
   - the insertion helper;
   - `ast_check.py`, `wheel_info.py`, `release_check.sh` and `assert_release.py`;
   - `check_links.py` and `import_names.py`.

   Their outputs are in `<scratch>/out/`, and the exports, wheels and venvs are under `<scratch>`.

## 8. Issues

- **Opened:** none. **Closed:** none. **Narrowed:** none.
- The board's §3 holds no issue of this repository. The index is at **4 open**: 0 on this
  repository's boards and 4 inherited.

## 9. State handed to the next prompt

- `HEAD` is this commit. The tree is clean apart from dispatch's ignored entries. `venv/` has
  `datastorekit 0.2.1` installed editable from this checkout, and its `egg-info` was removed.
- **Not pushed, not tagged.** `origin/main` is `102f225`, and the tags are `v0.1.0` and `v0.2.0`.
- **After the review**, this commit is pushed as `main`, which fast-forwards over 07a–09, their
  reviews and the notes. `v0.2.1` is made on it, annotated, only once CI passes there at both
  ends (as U23, U28). If CI fails, a fix prompt lands first, and no tag is made on a commit whose
  CI is red (rule 10).
- **The suite is 486** in `venv/` and at the high end (4 `ResourceWarning` lines).
  `compare_ported_tests.py`: 20 modules and one test declared not ported, exit 0.
  `black --check datastorekit docs`: 70 files.
- **For 11:**
  - every addendum's `datastorekit/` citation is at `cad7bc1`'s tree, which `v0.2.1` will name;
  - the contract's §8 citation (U34) is still `:567-574`, untouched here;
  - SGK's addendum cites `m7_messages.py` as catching `ReadOnlyMiss` only (§2 item 9);
  - the dispatch note's `object_get_vectorized` lines were one low (§2 item 10).
- **Scratch** (not in the repository): `<scratch>` as above, holding:
  - `exports/` (`release`, `high`, `break-a`, `break-b`);
  - `wheels/`;
  - `venv-release`, `venv-high`, `venv-break-a` and `venv-break-b`;
  - `breaks/` (the two diffs), `addenda/` (the inserted texts), `probe/` and `out/`.
