# object-timestamp campaign — implementation state

**Last updated:** 2026-10-12 · **Status: IN PROGRESS — 2 of 2 prompts written (01, 02), 2 landed (01,
`1b2f91a`, reviewed; 02, `2f5417e`, the release `v0.3.0`, reviewed; awaiting CI for `v0.3.0`);
U1–U6 taken 2026-10-12, as recommended; `v0.3.0` is made on `2f5417e` only once CI passes there at
both ends.**

**Campaign:** [`README.md`](README.md) ·
**Owns:** no issue. It carries out the user's ruling of 2026-10-12 (README §0) ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md)

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

### Decisions

**Put to the user (README §6.2), U1–U6 taken 2026-10-12:**

| Decision | Recommendation | Status |
|---|---|---|
| **U1** the form of the change | `DatastoreObject(store_id, *, timestamp=None)`: keyword-only, stored as `_timestamp`; a read-only `timestamp` property; a docstring saying a factory fills it from the row and the layer never sets or reads it | the change: **the user's ruling** 2026-10-12; its form: **taken** 2026-10-12, as recommended |
| **U2** the version object's `vars()` test | `TestTheVersionObject`'s expected dict (`tests/test_declared_facts.py:643-646`) gains `"_timestamp": None`; nothing else in it changes | **taken** 2026-10-12 |
| **U3** the tests | a neutral replicated stamped class and static factory outside the registry; `tests/test_object_timestamp.py`: the argument and property, the stamp read back through the pool and from every shard, read-only, keyword-only, `cloudpickle` | **taken** 2026-10-12 |
| **U4** Ray | no new smoke step; the script run unchanged under real Ray at both ends | **taken** 2026-10-12 |
| **U5** the shape | two prompts: 01 the change, 02 the release | **taken** 2026-10-12 |
| **U6** the release, and who adopts it | `v0.3.0`, minor (added API, as U36 drew the line); SI adopts it (G4); ChamPBH and SGK may stay on their pins (G3 "`v0.2.3` or later", G2 "`v0.2.2` or later") | **taken** 2026-10-12 (needed by 02) |

## 1. Prompts

| # | Prompt | Covers | Written? | Landed? | Commit | Log |
|---|---|---|---|---|---|---|
| 01 | [The object carries a timestamp](01-the-object-carries-a-timestamp.md) | `object.py` (U1); `TestTheVersionObject`'s dict (U2); the stamped class, `test_object_timestamp.py` (U3); the smoke run at both ends (U4); contract §9.6; verification §4.9 | ✍️ yes, 2026-10-12 | ✅ 2026-10-12; reviewed | `1b2f91a` | [log 01](logs/01-the-object-carries-a-timestamp.md) |
| 02 | [Release `v0.3.0`](02-release-v0.3.0.md) | the version, `README.md`, `PROVENANCE.md`, adoption addenda; the extraction board's G3 and G4; the tag after green CI (U6) | ✍️ yes, 2026-10-12 | ✅ 2026-10-12; reviewed; awaiting CI for `v0.3.0`; not tagged, not pushed | `2f5417e` | [log 02](logs/02-release-v0.3.0.md) |

**Planning note (2026-10-12, at `83068cb`).** The brief's four points of §3 were re-measured
(README §0.1). Points 2–4 hold. Point 1 holds for the layer, but the suite pins `vars()` of the
version object (`tests/test_declared_facts.py:643-646`), which the brief's search excluded (U2). A
prototype, `object.py` changed as U1 recommends and two scratch tests added, gave `Ran 506 tests`
with the two subtests of `TestTheVersionObject` failing and nothing else, at both ends (Python
3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39 in `venv/`; 3.13.16 / 2.55.1 / 2.0.46 in an offline
scratch venv). With that test's dict corrected, it and the scratch tests pass at both ends; a
stamped row's timestamp came back through the pool, from each of three shards, and through a
read-only reopen. Nothing was committed, and Ray was not started. The clients at planning: SGK
`ede4062` (clean), ChamPBH `0e64ef0` (29 entries in `git status --short`), SI `7bb3efd` (3
entries).

**Orchestrator review of prompt 01 (2026-10-12).** Dispatched from `2abea79` to one Opus
subagent, with the note's five corrections and its additions. Reviewed against its commit
`1b2f91a`, with nothing landed after it. **Every check of the note's §3 passed**, and acceptance
1–4 are met. No stop condition fired. Nothing was pushed by this campaign, and the tags are
`v0.1.0`, `v0.2.0`, `v0.2.1`, `v0.2.2` and `v0.2.3` only.

*At dispatch.* While the note was written, another session committed `6465a6a` (the extraction
board's G2) and `2a86f92` (the `inherited-issues` board) on `main` in this checkout, and pushed
them: `origin/main` was `83068cb` by the note's first `git ls-remote` and is `2a86f92` at the
review. Both touch only `prompts/` and `docs/OPEN_ISSUES.md`, which the gate allows, and the index
stays at 4. The note's gate sentence that `main` is ahead of `origin/main` by `251986b` and the note
alone was therefore stale when committed; nothing the agent relied on moved. The tree was clean,
one worktree; the suite gave `Ran 504 tests … OK` in `venv/` (0 `ResourceWarning` lines), the
port check exited 0, and `black --check datastorekit docs` left 74 files. No Ray process was up.
The clients moved under other sessions throughout (correction 4): SGK `ede4062` at planning →
`f78e8b6` → `718e650` at dispatch → `d03a643` (clean) at the review; CPBH `0e64ef0` → `d7791c5` →
`f5fe207` → `a72ca5e` at the agent's start → `70184f1` at its end → `e287a40` (24 entries) at the
review; SI `7bb3efd` (3 entries) throughout. While writing the note the orchestrator built a
prototype of §2.1–§2.4 in a scratch export: 509 at both ends, the unchanged smoke script passing
every step under real Ray at both ends, and breakages (a)–(e) as the note's table gives. It found
that test 4 passes under (a) (correction 1), that `value` is a column of all three clients
(correction 2), that (d) fails test 3 too (correction 3), and two readings of line numbers
(correction 5).

*The checks.*
1. **Scope.** `1b2f91a` touches the prompt's §7 files only: under `datastorekit/`, four
   (`object.py`, `tests/test_declared_facts.py`, and the new `tests/client/stamped.py` and
   `tests/test_object_timestamp.py`). The diff over `pyproject.toml`, `README.md`, `PROVENANCE.md`,
   `docs/adoption/`, `docs/extraction/` and `.github/` is empty, and so is that of the neutral
   client's `registry.py`, `objects.py`, `factories.py`, `instances.py` and of `standin_pool.py`.
   The ignored entries are dispatch's. The agent read the clients only through `git` and wrote
   nothing there (its log §4.7).
2. **The object, by reading.** `__init__(self, store_id, *, timestamp=None)`, one new assignment,
   a `timestamp` property with a docstring that says who fills it, when it is `None`, and that the
   layer neither sets nor reads it, naming no client. The review's `ast` comparison against
   `0de2b16`: `store_id` and `available` equal; `__init__`'s positional arguments equal, one new
   keyword-only `timestamp` defaulting to `None`, and its body the old assignment plus
   `self._timestamp = timestamp`; the module's only other additions the `datetime` import and the
   property; the class docstring unchanged. In `venv/`, `DatastoreObject.timestamp.fset` and
   `.fdel` are `None`, and `inspect.signature` gives `timestamp` as `KEYWORD_ONLY`, default `None`.
3. **§2.3's module, by reading.** `stamped.py`: module-level `stamped_tally` (one integer, `tally`;
   `timestamp` passed to `super().__init__` by keyword) and `stamped_tally_factory` (static
   `register` and `build` only; no `inventory_spec`); `stamped_registry()` copies the registry's
   factories and replicated tables. The column, attribute and key are `tally`. The review's
   vocabulary script finds none of `stamped_tally`, `stamped_tally_factory`, `stamped_registry`,
   `STAMPED_TABLE`, `STAMPED_COLUMN`, `tally`, `STAMP`, `TALLY` in any client's `registry`,
   `columns` or `packages`, case-insensitively.
4. **The tests, by reading.** The five of §2.4, each store in a `tempfile` directory, with a
   `tearDownModule` asserting Ray is not initialised. Test 2 reads the raw stamp on every shard,
   compares by `datetime.fromisoformat`, gets directly from each of the three shard actors of the
   open reopened pool, reopens read-only, and checks the raw stamp unchanged at the end; test 3
   checks the value unchanged after the refused assignment and deletion, on the base and the
   subclass. `test_declared_facts.py` changes by the one dict (split by `black`).
5. **The suite at both ends.** `Ran 509 tests … OK` in `venv/` and in a fresh high-end venv
   (3.13.16 / 2.55.1 / 2.0.46) with `git archive 1b2f91a` installed editable, run from the export's
   root (`datastorekit.__file__` under it); 0 `ResourceWarning` lines at each. The port check: "OK:
   20 module(s) … 1 test(s) declared not ported". `black --check datastorekit docs`: 76 files.
6. **The breakages.** (a)–(e) extracted from the log's §5, each passing `git apply --check` and
   `-R --check` against the review's export, and run there: (a), the full suite, `Ran 509 …
   FAILED (failures=2, errors=4)`, errors in tests 1–3 and 5, failures in `TestTheVersionObject`'s
   two subtests, test 4 passing, nothing else; (b) test 3's two subtests; (c) test 4; (d) tests 1,
   2, 3 (two subtests) and 5, five entries; (e) test 2. Each as the log records; 0
   `ResourceWarning` lines under each. The export was restored after each and compared with the
   commit. **The note's correction 1 was wrong in one detail**: it gave all four errors under (a)
   as `TypeError`, but test 1's is `AttributeError` at its first read of `timestamp`, as the
   agent's deviation 4 records (the prototype's count of three `TypeError` lines against four
   errors showed it too). It fails for the right reason.
7. **Ray.** No Ray process before either run. From the review's own offline venvs, each with an
   export of `1b2f91a` installed editable, run from its root under `env -u PYTHONPATH` and
   `/usr/bin/time -p`, the script (SHA-256 `03203679…a92a`, unchanged) gave at the low end (3.12.15
   / 2.43.0 / 2.0.39) and the high end each step 1, 2, N, C, 3, 4, 5, 6 and I `PASS`, "every step
   passed; 0 Ray process(es) left", exit 0, `real` 19.76 s and 27.93 s; step C named
   `builtins.ValueError` and `ray.exceptions.ActorAlreadyExistsError` respectively, as §4.9 records.
   No Ray process after either. Another session's Ray instance was up during the agent's work
   (from 01:29:36 to before 01:40:20); the agent did not touch it and ran the script after it had
   gone.
8. **The documents.** Contract: the head line after §9.5's; §9.6 in §9's form, "Supersedes" none
   with its reason; its citations read at `1b2f91a` (`object.py:10-14`, `:14`, `:16-25`, `:27-38`;
   `SQL/Datastore.py:809-815`, `:760-843`; `SQL/ShardedPool.py:3203`); `+` lines only.
   Verification: §4.9 after §4.8.3's closing fence and before `---` and `## 5`, with the
   environment and output of both runs and the script's SHA-256; `+` lines only. The relative
   links added resolve.
9. **The records.** The log in §5.1's form, with the breakage diffs, the smoke output, the names
   checked and the clients at the start and the end; this board's header and row, the README's
   header and §2 row, and `prompts/INDEX.md`; `docs/OPEN_ISSUES.md` unchanged at 4.
10. **Nothing left behind.** No Ray process. `git tag -l` is the five tags. `origin` holds
    `2a86f92`, pushed by the other session (above), not by this campaign.

Residue fixed in the commit that records this review: "this commit" → `1b2f91a` on this board, in
the log, in the README and in `prompts/INDEX.md`; "reviewed" for 01 here, in README §2 and in
`prompts/INDEX.md`; the notes line.

*The push (2026-10-12).* With the user's approval, `main` was pushed, moving `origin/main` from
`2a86f92` to `d88615e` (a fast-forward of three commits, `2abea79`, `1b2f91a` and `d88615e`, with
no tag). CI passed there at both ends,
[run 38190920683](https://github.com/ds283/DatastoreKit/actions/runs/38190920683):
- low: Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39, `Ran 509 tests in 175.661s` / `OK`, and
  `black` leaving 76 files unchanged;
- high: 3.13.16 / 2.55.1 / 2.0.46, `Ran 509 tests in 163.609s` / `OK`;
- 0 `ResourceWarning` lines in the run's log; SQLite 3.45.1 at both.

**Orchestrator review of prompt 02 (2026-10-12).** Dispatched from `b56fdde` to one Opus
subagent, with the note's six corrections and its additions. Reviewed against its commit
`2f5417e`, with nothing landed after it. **Every check of the note's §3 passed**, and acceptance
1–6 are met. No stop condition fired. Nothing was pushed by this campaign, and the tags are
`v0.1.0`, `v0.2.0`, `v0.2.1`, `v0.2.2` and `v0.2.3` only.

*At dispatch.* `HEAD` `b56fdde`, the tree clean, one worktree. `origin/main` `75c237e` by `git
ls-remote` at the note's writing and at the review. The note's baseline at `778c95a`: `Ran 509
tests … OK` in `venv/` (0 `ResourceWarning` lines) and at the high end (0); the port check exit 0;
`black --check datastorekit docs` 76 files. No Ray process. While the note was written the
orchestrator built `0.3.0` wheels offline from exports, ran the release probe and breakages
(a)–(c) at the high pins, and re-ran the prompt's §1.1 measure through `git` at SGK `d03a643` and
`e3a7077`, CPBH `64ef9aa` and `cb0c675`, and SI `7bb3efd`, each exactly the prompt's table. It
found that hazard 6's reinstall is refused in `venv/` (no `setuptools`; correction 1, as at
`factory-defaults` 02), that SGK's G2 statement is still true and is not to be superseded
(correction 2), that SI's checklist `:80-81` (at `0de2b16`) is superseded too (correction 3), that
SGK's and CPBH's `HEAD`s had moved (correction 4), that SI's `Datastore/object.py` was added at SI
`3e56d39` and gained its `timestamp` at `51b04f8` (correction 5), and the line shifts as numbers
(correction 6). The clients moved under other sessions throughout: SGK `e3a7077` → `cf978c6`
(clean), CPBH `cb0c675` → `0f1c25b` (23 untracked entries), SI `7bb3efd` (3 entries) throughout.

*The checks.*
1. **Scope.** `2f5417e` touches the prompt's §7 files only: `pyproject.toml`, `README.md`,
   `PROVENANCE.md`, the four files under `docs/adoption/`, the extraction board, the log, this
   board, the campaign README and `prompts/INDEX.md`. The diff over `datastorekit/`,
   `docs/client-contract.md`, `docs/extraction-verification.md`, `docs/extraction/`, `.github/`,
   `CLAUDE.md`, `LICENSE`, `.gitignore` and `docs/OPEN_ISSUES.md` is empty. No wheel, `build/`,
   `dist/` or `egg-info` in the checkout. `git status --short --ignored` showed one entry more than
   at dispatch, `datastorekit/tools/__pycache__/` (three `cpython-312` files written at 03:05 by
   the agent's name check in `venv/`); ignored bytecode, removed by the review.
2. **Additive.** `git diff b56fdde 2f5417e -- docs/adoption/` has no `-` line (127, 97, 88 and 98
   lines added). `pyproject.toml`'s diff is `:7` alone. The extraction board's diff is G3's and
   G4's rows alone: G3's title gains "or later" and "`object-timestamp` U6", G4's `v0.3.0` and the
   same, each row one dated italic sentence, every earlier sentence kept; G1 and G2 unchanged.
3. **The release.** From `git archive 2f5417e`, `uv build --offline --wheel` gives
   `datastorekit-0.3.0-py3-none-any.whl`, 99,488 bytes: 25 entries, none under `tests/`, the
   licence; `METADATA` `Version: 0.3.0`, `Requires-Python: >=3.12`, `ray>=2.43`,
   `sqlalchemy<2.1,>=2.0.39`. Installed offline into a fresh 3.13.16 venv at `ray==2.55.1` and
   `sqlalchemy==2.0.46` and run from outside the repository with `python -I`: imported from
   `site-packages`; metadata `0.3.0`; `timestamp` `KEYWORD_ONLY`, default `None`; `fset` and
   `fdel` `None`; the stamped object returns its `t`, the unstamped `None`, `vars()` `{'_my_id':
   3, '_timestamp': None}`; the positional `TypeError` and the assignment's `AttributeError` with
   the messages the note gives, and a subclass's assignment and deletion refused; `pickle`
   round-trips; `datastorekit.tests` refused; `sharded_store --help` exit 0. Against the review's
   own `v0.2.3` wheel, of the 20 `RECORD` lines under `datastorekit/` only `object.py`'s differs.
   The file list is the log's.
4. **`README.md` and `PROVENANCE.md`, by reading.** The `v0.3.0` status paragraph above
   `v0.2.3`'s, which is unchanged, says each thing the note's check 4 lists and links §9.6 by
   anchor. The pin is `v0.3.0`; the sentence replacing `:86-89` names the five earlier tags, SI's
   adoption and CPBH's and SGK's permission, names no client path, advises neither way, and does not
   say `v0.3.0` is tagged. "What changed after `v0.2.0`" adds `v0.3.0`'s change, linking §9.6 and
   still §9. `PROVENANCE.md`'s new `###` section follows the `factory-defaults` section and says
   what check 4 asks, with correction 5's commits; one sentence is wrapped short ("read through
   `git` only, has a" ends a line), which renders the same.
5. **The addenda, by reading.** In each of the four files the italic line follows
   `factory-defaults` 02's, and the addendum, unnumbered and dated 2026-10-12, sits after the
   `v0.2.3` addendum's table between two `---` rules (in the README, at the end). Each gives its
   pin per U6; says what changed for its client, linking §9.6; cites every superseded statement by a
   `path:line` that the review read in the committed file (the README's `:387-396`, `:398-399`,
   `:454-460`, `:467-475`; SGK's `:557-569`, `:609-615`, `:623-630`; CPBH's `:546-552`, `:598-604`,
   `:612-618`; SI's `:44-45`, `:86-88`, `:104`, `:106`, `:111`, `:160`, `:515-521`, `:563-569`,
   `:577-583`); and states N = 5, 10, 15 in the README and 6, 12, 18 in each checklist, the lines
   the italic lines added. SGK's names `:559` and `:631` as standing and says G2 holds (correction
   2); SI's supersedes `:86-87` in a row of its own (correction 3), and says its 24 sites work as
   they stand, that its factories go on passing the value, and that item 2 asks nothing more and
   item 4's line no longer leaves the layer; CPBH's and SGK's say nothing changes that they meet,
   with no instruction to either. The claims about the clients re-read through `git`: SGK's two
   `__dict__` reads at `e3a7077` are of classes; SI's one `__dict__` outside its records is in a
   docstring (`tests/test_plot_extraction_golden.py:114`), so "no SI `.py` file … reads a
   `__dict__`" holds; CPBH's item 5 table is `:189-207` and item 8's `ReplicatedDivergence` point
   `:351-354`, as its addendum cites.
6. **Names and links.** The review's own extraction of every relative link in `README.md`,
   `PROVENANCE.md`, the four adoption files and the extraction board's §2: 128 links, each file
   found and each anchor a heading by GitHub's rule, 0 bad. The new anchors
   (`#addendum-v030-object-timestamp-prompt-02-2026-10-12` in each file,
   `#96-object-timestamp-prompt-01`, `#9-changes-after-v020`) all resolve. The diff adds no dotted
   `datastorekit.` name.
7. **Both ends.** In `venv/`: `pip show datastorekit` `0.3.0`; no `datastorekit.egg-info/`; `Ran
   509 tests in 96.318s` / `OK`, 0 `ResourceWarning` lines. In a fresh high-end venv (3.13.16 /
   2.55.1 / 2.0.46) with `git archive 2f5417e` installed editable and run from the export's root:
   `Ran 509 tests in 99.296s` / `OK`, 0 lines. The port check: "OK: 20 module(s) … 1 test(s)
   declared not ported". `black --check datastorekit docs`: 76 files.
8. **The breakages.** (a)–(c) extracted from the log's §6, each passing `git apply --check` and
   `-R --check` against its own export (of `2f5417e` for (a) and (b), of `v0.2.3` for (c)), built
   offline and probed at the high pins: (a) `Version: 0.2.3` and metadata `0.2.3`, `RECORD`
   differing from `v0.2.3`'s in `object.py` only; (b) 76 entries, 51 under `datastorekit/tests/`,
   `import datastorekit.tests` succeeding; (c) `Version: 0.3.0`, all 20 `RECORD` lines equal to
   `v0.2.3`'s, `store_id` alone in the signature, no property, and `TypeError` on the keyword.
   Each as the log records and the note's table predicts.
9. **The records.** The log in §5.1's form, with the release check, the documents' check, the
   names and links, §1.1's measure re-run at every commit read, (a)–(c), the clients at both ends,
   the six corrections and the additions, and the four supersession tables; this board's header and
   row, the README's header and §2 row, and `prompts/INDEX.md`; `docs/OPEN_ISSUES.md` unchanged at
   4.
10. **Nothing left behind.** No Ray process before or after any check. `git tag -l` is the five
    tags; `origin` holds `75c237e`.

Residue fixed in the commit that records this review: "this commit" → `2f5417e` on this board, in
the log (but where §1.6 quotes what the board said), in the README and in `prompts/INDEX.md`;
"reviewed; awaiting CI for `v0.3.0`" for 02 here, in README §2 and its header, and in
`prompts/INDEX.md`; the notes line; and the stray `__pycache__/` of check 1, which is not tracked.

*The push (2026-10-12).* With the user's approval, `2f5417e` was pushed as `main`
(`git push origin 2f5417e:refs/heads/main`), moving `origin/main` from `75c237e` to `2f5417e`, a
fast-forward over `778c95a`, `b56fdde` and `2f5417e`, with no tag; `30d2fc8`, the review's record,
stayed local. CI passed on `2f5417e` at both ends,
[run 38220924369](https://github.com/ds283/DatastoreKit/actions/runs/38220924369):
- low: Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39, `Ran 509 tests in 246.964s` / `OK`, and
  `black` leaving 76 files unchanged;
- high: 3.13.16 / 2.55.1 / 2.0.46, `Ran 509 tests in 165.180s` / `OK`;
- 0 `ResourceWarning` lines in the run's log; SQLite 3.45.1 at both.

`v0.3.0` may now be made on `2f5417e`, with the user's approval (U23, U28).

**Legend.** ✍️ written · ⏸ held, with what it waits on · ⬜ not written / not landed ·
✅ landed.

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`2abea79`),
used for 01; [`orchestrator/prompt-02.md`](orchestrator/prompt-02.md) (`b56fdde`), used for 02.

## 2. Gates outside this repository

None of this campaign's own. The extraction campaign's G2–G4 are recorded on its board (README §7).
When the release is tagged, its tag object and commit are given to the user for SI's prompt 08.

## 3. Active and unresolved issues

No issue is held on this board (2026-10-12).

## 4. Resolved issues

None yet.
