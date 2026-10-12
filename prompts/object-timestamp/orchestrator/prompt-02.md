# Orchestrator — prompt 02, release `v0.3.0`

Read [`../README.md`](../README.md) first: §0, §1, §2, §4, §5 (every rule), §6.1 and §6.2 (U1 and
U6), and §7. Then read [`prompt-01.md`](prompt-01.md), whose "Conventions" and §4–§5 this note
keeps unless it says otherwise, and `factory-defaults`'
[`prompt-02.md`](../../factory-defaults/orchestrator/prompt-02.md), the note for the release this
one repeats: its §0, its additions, and its §5, which this note's §5 follows. Then read this board's
review of 01.

**You do not write code.** You may:
- run the suite, the port check, `black --check` and the guards;
- make venvs in the session scratchpad with `uv … --offline`, from the cache the extraction
  campaign filled, and nothing else: **no download**;
- export the tree with `git archive` into the scratchpad, and build wheels, run probes and replay
  breakages there, never in this checkout and never committing one;
- **start no Ray.** No code changes, so the smoke script is not run (the prompt's hazard 7);
- reach the network only for one `git ls-remote origin` at dispatch and one at the review, and for
  the pushes, the tag and the CI read of §5, each with the user's approval;
- read the three clients only through `git -C <client> rev-parse|status|show|grep|ls-tree|log|cat-file|merge-base`;
- fix small residue in a follow-up commit of your own (§4).

**The prompt:** [`02-release-v0.3.0.md`](../02-release-v0.3.0.md)
**Closes:** nothing · **Narrows:** nothing · **Changes:** nothing in the package but its version ·
**Opens:** only what the work finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- 01 landed (`1b2f91a`), was reviewed (`d88615e`) and passed CI there at both ends,
  [run 38190920683](https://github.com/ds283/DatastoreKit/actions/runs/38190920683), recorded at
  `75c237e`. 02 was written against `75c237e` (`778c95a`).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- `git diff --stat 1b2f91a HEAD -- datastorekit docs pyproject.toml README.md PROVENANCE.md
  .github` is empty: everything 02 reads or edits, but the extraction board, is 01's tree. And
  `git diff --stat 0de2b16 HEAD -- docs/adoption README.md PROVENANCE.md pyproject.toml .github`
  is empty: the files 02 edits are `v0.2.3`'s (both measured at `778c95a`).
- `origin/main` is `75c237e` (`git ls-remote origin`, 2026-10-12), an ancestor of `main`, which is
  ahead of it by `778c95a` and this note. The tags are `v0.1.0` (`0ece4aa` → `68db557`), `v0.2.0`
  (`9eaf542` → `240028e`), `v0.2.1` (`0ba2e4d` → `33778b0`), `v0.2.2` (`c32d027` → `6d8ee9a`) and
  `v0.2.3` (`8dac562` → `0de2b16`), here and on `origin`, and no other.
- The clients' `HEAD`s, read while this note was written: SGK `e3a7077` (branch
  `handover-remedial`, clean); CPBH `cb0c675` (branch `dk-and-rpk-migration`, 23 untracked entries:
  run scripts, pilot `.db` files and logs, `pilot-out/`, `prompts/jordan-normalization/`); SI
  `7bb3efd` (`main`, 2 modified, `.documents/OPEN-ISSUES.md` and `.prompts/INDEX.md`, and 1
  untracked, `.prompts/dk-and-rpk-migration/`). SGK and CPBH have both moved since the prompt was
  written (correction 4). A changed `HEAD` or status there is not this campaign's doing, and is
  recorded, not stopped on, unless the prompt's §6 fires at the `HEAD` read.
- This board's §3 holds no issue, and the index is **4** (all four on `inherited-issues`' board).
  It stays 4 unless the work opens an issue.
- No Ray process (`pgrep -lf 'gcs_server|raylet|ray::'` empty); `RAY_ADDRESS` and
  `RAY_ENABLE_AUTO_CONNECT` unset; no `/tmp/ray/ray_current_cluster`.
- One prompt at a time in this checkout. 02 is the campaign's last.

## 0. What makes this prompt unusual

**No line of code changes, so the suite cannot catch a bad edit.** It passes whatever the
documents say. What stands in for it, as at `factory-defaults` 02:
- the release check, from a clean export, which alone sees `0.3.0` and the change behind it;
- hazard 1's `git diff`, which must show `+` lines only under `docs/adoption/`;
- reading: every statement an addendum makes is true of `v0.3.0`, every statement it supersedes is
  named by `path:line`, and every name and link resolves.

**The release removes an obligation from SI, and changes nothing CPBH or SGK meets.** For SI it
removes item 2's `DatastoreObject.timestamp` paragraph's burden: its 24 sites work as they stand
once their import is rewritten, and `DatastoreObject.timestamp` no longer leaves the layer (item
4). What it does not do: the layer still never sets or reads the value, so SI's factories must go
on passing it, as they do today; and a `vars()` of any client's object now has `_timestamp`.

**The pins differ by client three ways.** SI adopts `v0.3.0`; CPBH may stay on `v0.2.3` or move;
SGK, which has adopted `v0.2.2` (G2 holds, 2026-10-12), may stay or move to `v0.2.3` or `v0.3.0`
(U6). The README, each addendum and the gates must say U6 exactly, and none may advise CPBH or SGK
either way (hazard 8).

**G2 holds, and is unchanged.** "SGK adopted `v0.2.2` or later" is already U6's reading. Nothing in
02 rewrites or supersedes it (correction 2).

**The acceptance finishes elsewhere.** `v0.3.0` is made on 02's commit only once CI has passed
there at both ends (§5). It is the commit SI's prompt 08 will pin.

**The push carries more than 02.** `origin/main` is `75c237e`. Pushing 02's commit as `main`
fast-forwards over `778c95a`, this note and 02 itself. None of them but 02 changes a file CI reads,
so the tree CI tests is 02's.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-12 at `778c95a` (whose
`datastorekit/`, `docs/`, `README.md`, `PROVENANCE.md` and `pyproject.toml` are `75c237e`'s and
`1b2f91a`'s), in `venv/`, in offline scratch venvs and exports at the high end, with wheels built
offline from exports, and by reading the clients through `git`. Pass them on. Corrections 1 and 2
change what the agent does or writes, and are STRUCTURALLY REQUIRED. Corrections 3–6 correct or
complete what the prompt states; the log records each as found.

1. **Hazard 6's reinstall cannot run, as at `factory-defaults` 02.** `venv/` still has no
   `setuptools` (`import setuptools` raises `ModuleNotFoundError`), so `uv pip install --offline
   --no-deps --no-build-isolation --python venv/bin/python -e .` is refused. Probed on a scratch
   `python3.12 -m venv` against an export at `0.3.0`: uv refuses, and suggests installing
   `setuptools` into the environment, which would change `venv/`, which this prompt does not do.
   **Use `factory-defaults` 02's form (its correction 1), `uv pip install --offline --no-deps
   --python venv/bin/python -e .`, from the repository root, without `--no-build-isolation`.**
   Probed the same way: it installs `datastorekit==0.3.0` editable, `pip show` says `Version:
   0.3.0`, and it writes `datastorekit.egg-info/` at the root, which is deleted afterwards. The
   high-end scratch venv of §4.1 has `setuptools`, so `--no-build-isolation` is right there.
2. **SGK's G2 statement is not superseded.** The prompt's table (§2.4, SGK's row) and its list
   ("at least … its gate statement") would have SGK's addendum supersede the `v0.2.3` addendum's G2
   statement. But that statement (`secondarygwkit.md:553`, "G2 reads 'SGK has adopted `v0.2.2` or
   later'", and the table's `:625`) is exactly U6's reading, and G2 holds (the extraction board,
   2026-10-12). Superseding a true statement with itself would be noise. SGK's addendum:
   - supersedes the `v0.2.3` addendum's pin **in part**: the choice is now `v0.2.2`, `v0.2.3` or
     `v0.3.0`, SGK's (`:551-563`, and the table rows that give the pin, `:617-618` and `:620-621`);
   - says G2's reading is unchanged and that **G2 holds** (2026-10-12, recorded at `6465a6a`, the
     extraction board), and cites `:553` and `:625` as standing, not superseded;
   - says nothing that advises SGK to stay or move.

   For CPBH and SI the gate statements are superseded as the prompt says (G3 "`v0.2.3` or later",
   G4 "`v0.3.0`").
3. **SI's item 2 has one more statement that `v0.3.0` makes untrue.** Besides the prompt's list,
   `stochasticinstantons.md:80-81`: "The package's `DatastoreObject` (`datastorekit/object.py:9`)
   takes `store_id` only." True of `v0.2.0`, whose line it cites; at `v0.3.0` the package's takes a
   keyword-only `timestamp` too (`datastorekit/object.py:10-14` at `1b2f91a`). Supersede it in the
   same row as, or a row beside, item 2's others. The statement that SI's own `DatastoreObject`
   takes `timestamp` and exposes it, "added at SI `51b04f8`" (`:78-80`), still holds, and so does
   `:102-103` (the test stand-ins).
4. **The clients moved under the prompt.** SGK `d03a643` → `e3a7077` (clean), CPBH `64ef9aa` →
   `cb0c675` (23 untracked). §1.1's measure reproduces exactly at all four commits and at SI
   `7bb3efd` (below). The agent records the `HEAD`s it reads, and hazard 4's stop is judged at
   those; the addenda name the commit they were read at.
5. **`PROVENANCE.md`: where SI's `DatastoreObject` gained its timestamp.** §2.3 says SI's
   `Datastore/object.py` was "added at SI `51b04f8`, 2026-06-21". Read through `git log
   --diff-filter=A`: the file was added at SI `3e56d39` (2026-06-15, "Add initial implementation of
   StochasticInstantons codebase") taking `store_id` alone; `51b04f8` (2026-06-21, "Surface
   row-creation timestamps via DatastoreObject") gave it `timestamp`. Say the latter: SI's
   `DatastoreObject` has taken a `timestamp` since SI `51b04f8`. SGK's `Datastore/object.py` at
   `6f7f291` takes `store_id` alone, as the prompt says (read through `git show`).
6. **How the earlier addenda's citations are read, with numbers.** The `v0.2.3` italic lines are
   `docs/adoption/README.md:17-20`, `secondarygwkit.md:27-31`, `champbh.md:28-32` and
   `stochasticinstantons.md:26-30`, each followed by one blank line; 02's italic line goes after
   that blank, so its insert is after `:21`, `:32`, `:33` and `:31`. The `v0.2.3` addenda each say
   their italic line added k lines (k = 5 in the README, 6 in each checklist), and read the
   `v0.2.2` addendum's citations k lines later and the `v0.2.1` addendum's 2k lines later. After
   02's italic line of N lines (blank included):
   - the `v0.2.3` addendum's citations are read at `0de2b16`, or **N** lines later here, except
     those above the insert: the `v0.2.2` italic line it cites (`README.md:12-15`,
     `secondarygwkit.md:21-25`, `champbh.md:22-26`, `stochasticinstantons.md:20-24`);
   - the `v0.2.2` addendum's at `6d8ee9a`, or **k + N** lines later, except `README.md:7-10`,
     `secondarygwkit.md:16-19`, `champbh.md:17-20`, `stochasticinstantons.md:15-18`;
   - the `v0.2.1` addendum's at `33778b0`, or **2k + N** lines later, except `:3`, `:6`, `:6` and
     `:5` respectively.

   The agent states N, k + N and 2k + N for each file as numbers, and the review checks them
   against the file as committed.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **Work in this order:**
  1. the baseline: 509 in `venv/`, and at the high end from a fresh venv with an export of `HEAD`
     installed editable; the port check; `black --check datastorekit docs`, 76 files; the clients'
     `HEAD`s and statuses; §1.1's measure (hazard 4);
  2. `pyproject.toml`; `venv/`'s reinstall (correction 1), the `egg-info` removed; the suite;
  3. `README.md` and `PROVENANCE.md`;
  4. the four addenda and italic lines; then hazard 1's `git diff`;
  5. the extraction board's gates;
  6. the release check; the high end;
  7. (a)–(c);
  8. the documents' check (§4.4) and the name-and-link check (hazard 2);
  9. `venv/`'s suite again, the port check, `black`, the clients again, the records.
- **Give each addendum's supersessions as a table** (`path:line`, the statement in brief, what
  replaces it), as the earlier addenda do. The log repeats the four tables, with any statement
  found that the prompt's table does not name (correction 3 among them).
- **Where the `v0.2.3` addenda state the pin and the gate**, cited as they stand after 02's italic
  line (that is, N lines later than here):
  - README: the pins, `:379-391`; the carry-over sentence, `:393-394`; and in its table, the rows
    that give pins or gates directly (`:462-463`, `:470`) or by reference ("as `:289-290`", "as
    `:293`": `:465-466`, `:468-469`). Row `:467` ("each checklist with its three addenda") is
    superseded too: at `v0.3.0` each has four.
  - SGK: `:551-563`, and table rows `:617-618`, `:620-621` (pin; correction 2 for the gate rows
    `:553`, `:625`); `:622` ("at `v0.2.2` or `v0.2.3`, with the three addenda").
  - CPBH: `:540-546`, and table rows `:606-607`, `:609-612`.
  - SI: `:509-515`, and table rows `:571-572`, `:574-577`.
- **Placement.** In each checklist the `v0.2.3` addendum is preceded by a `---` rule
  (`secondarygwkit.md:541`, `champbh.md:530`, `stochasticinstantons.md:499`) and followed by one
  before the appendix (`:627`, `:614`, `:579`). The `v0.3.0` addendum goes after the `v0.2.3`
  addendum's table and before that second rule, with a `---` of its own above it. In the README it
  goes at the end (the `v0.2.3` table ends the file at `:470`), after a `---`. Its heading is
  `## Addendum: v0.3.0 (object-timestamp prompt 02, <date>)`; by GitHub's rule the anchor is
  `#addendum-v030-object-timestamp-prompt-02-<yyyy-mm-dd>`.
- **The README's v0.3.0 table of §1.1.** One row per client, with the commit read, where
  `DatastoreObject` comes from, the descendants, the three call counts, and the `timestamp`
  definitions or assignments on a descendant, as the prompt's §1.1 table; with SI's other
  `def timestamp` and `self.timestamp =` sites summarised (none a descendant), not listed.
- **`PROVENANCE.md`'s new section is a `###`**, as `:89`, `:118`, `:160` and `:205` are, under
  "After `v0.1.0`", after the `factory-defaults` section, which ends the file at `:240`.
- **The contract's anchors**, by GitHub's rule (lower-case; drop backticks and punctuation other
  than hyphens; spaces to hyphens): §9.6 "9.6 `object-timestamp` prompt 01"
  (`docs/client-contract.md:357`) is `#96-object-timestamp-prompt-01`; §6 "6. What the layer reads
  from a stored object" (`:204`) is `#6-what-the-layer-reads-from-a-stored-object`; §9 is
  `#9-changes-after-v020`, as `README.md:125` already links it. From `docs/adoption/` the path is
  `../client-contract.md#…`; from the root, `docs/client-contract.md#…`.
- **The gate titles**, exactly: G3 "CPBH adopted `v0.2.3` or later (U37; `actor-names` U3;
  `factory-defaults` U5; `object-timestamp` U6)"; G4 "SI adopted `v0.3.0` (U37; `actor-names` U3;
  `factory-defaults` U5; `object-timestamp` U6)". Each row's status cell gains one dated italic
  sentence at its end, in the form of the `v0.2.3` "ready to be tagged" sentences
  (`prompts/extraction/IMPLEMENTATION_STATE.md:1538-1539`), linking its client's new addendum by
  anchor; G3's says too that CPBH may stay on `v0.2.3` or move (U6). G1 and G2's rows (`:1536-1537`)
  and everything else on that board, its header included, are unchanged.
- **Keep the name-and-link check as a scratch script**, never committed, as `factory-defaults` log
  02 did: every relative link and anchor in `README.md`, `PROVENANCE.md`, the four adoption files
  and the extraction board's §2, each file resolved and each anchor found among its target's
  headings by GitHub's rule; every dotted `datastorekit.` name imported in `venv/`.
- **Build (a)'s, (b)'s and (c)'s wheels from their own exports**, each with the prompt's change
  and only that. Record (a) and (b) as diffs to `pyproject.toml` that `git apply --check` and `-R
  --check` accept against an export of the commit; (c) is the version line applied to an export of
  `v0.2.3`, and is recorded so that it applies there. Run the release probe in each wheel's venv,
  and record each output.
- **§1.1's measure.** The orchestrator's own, a script of `ast` reads from `git show` run with
  `python3 -I`, gave the prompt's table exactly (below). The agent writes its own, and records its
  essentials and its output.

**The facts, checked by the orchestrator.** Pass them on.

- **The suite** at `778c95a`: `Ran 509 tests … OK` in `venv/` (104 s), 0 `ResourceWarning` lines;
  and at the high end from a fresh offline venv with an export installed editable
  (`--no-deps --no-build-isolation`), run from the export's root (`datastorekit.__file__` under
  it), `Ran 509 tests … OK` (108 s), 0 `ResourceWarning` lines. The port check exits 0 ("OK: 20 module(s) …
  1 test(s) declared not ported"); `black --check datastorekit docs` leaves 76 files unchanged.
- **§1.1 reproduces**, read through `git` at SGK `d03a643` and `e3a7077`, CPBH `64ef9aa` and
  `cb0c675`, and SI `7bb3efd`:
  - SGK, both commits: `DatastoreObject` imported from `datastorekit` 19 times, no class of its
    own; 30 descendants; 38 `DatastoreObject.__init__` calls, each `store_id` alone; no
    `timestamp` defined or assigned on any class; no factory passes `timestamp=`;
  - CPBH, both commits: imported from `Datastore` 13 times and `.object` once, its own class at
    `Datastore/object.py:19`; 31 descendants; 19 calls, each `store_id` alone; no `timestamp`
    defined or assigned on any class;
  - SI: imported from `Datastore` 12, `Datastore.object` 6 and `.object` once, its own class at
    `Datastore/object.py:20`; 34 descendants; 23 direct calls, 9 `store_id` alone and 14 with
    `timestamp=` (keyword), none other; 10 `__init__` calls passing `timestamp=` in deeper
    descendants; `timestamp` defined or assigned on a class at 19 sites, none a descendant: its own
    `DatastoreObject` (`:30`, `:44`), the four plot adapters, the stand-in
    `tests/test_plot_adapters_golden.py:870` (`_FakeThirdAdapter`, a `def`), and the 12
    `self.timestamp =` sites of README §0.1; 18 factory modules pass `timestamp=`.
  - No `super().__init__` in a class whose bases name `DatastoreObject` directly, in any client.
  - SGK `requirements.txt:17` pins `v0.2.2` at `e3a7077`; CPBH has no `datastorekit` line at
    `cb0c675`; SI has none.
- **The package.** `git diff --numstat 0de2b16 1b2f91a -- datastorekit/object.py`: 18 added, 1
  removed. Only `pyproject.toml:7` carries the version.
- **§1.2 reproduces.** From a `git archive` of `778c95a` with only `version = "0.3.0"`,
  `uv build --offline --wheel` gives `datastorekit-0.3.0-py3-none-any.whl`, 99,488 bytes (the bytes
  are not reproducible; compare `RECORD` lines, not hashes):
  - 25 entries, none under `datastorekit/tests/`; `datastorekit-0.3.0.dist-info/licenses/LICENSE`;
  - `METADATA`: `Version: 0.3.0`, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43`,
    `Requires-Dist: sqlalchemy<2.1,>=2.0.39`;
  - installed offline with `ray==2.55.1` and `sqlalchemy==2.0.46` into a Python 3.13.16 venv
    (SQLite 3.53.4) and run from a directory outside the repository with `PYTHONPATH` unset and
    `python -I`: the package imports from `site-packages`; the metadata version is `0.3.0`;
    `inspect.signature(DatastoreObject)` is `store_id` `POSITIONAL_OR_KEYWORD` and `timestamp`
    `KEYWORD_ONLY`, default `None`; `DatastoreObject.timestamp` is a `property` with `fset` and
    `fdel` `None`; `DatastoreObject(3, timestamp=t).timestamp is t`; `DatastoreObject(3).timestamp`
    is `None` and its `vars()` is `{'_my_id': 3, '_timestamp': None}`; `DatastoreObject(3, t)`
    raises `TypeError: DatastoreObject.__init__() takes 2 positional arguments but 3 were given`;
    assigning `timestamp` raises `AttributeError: property 'timestamp' of 'DatastoreObject' object
    has no setter`; a stamped object round-trips `pickle` with its timestamp; `import
    datastorekit.tests` raises `ModuleNotFoundError`; `python -m datastorekit.tools.sharded_store
    --help` exits 0. No Ray process after.
  - Against `git archive v0.2.3`'s wheel (99,185 bytes): 20 `RECORD` lines under `datastorekit/`
    each side, the same paths, and only `object.py`'s differs (1,306 bytes against 491).
- **The breakages**, each from its own export, at the high pins:

  | | Change | Measured |
  |---|---|---|
  | (a) | version left at `0.2.3` | `METADATA` `Version: 0.2.3`, 25 entries; its `RECORD` differs from `v0.2.3`'s wheel's in `object.py` only: the version alone is wrong |
  | (b) | `exclude = ["datastorekit.tests", "datastorekit.tests.*"]` deleted (`pyproject.toml:17`) | 76 entries, 51 under `datastorekit/tests/`; `import datastorekit.tests` succeeds from `site-packages` |
  | (c) | `v0.2.3`'s tree at `0.3.0` | `Version: 0.3.0`; all 20 `RECORD` lines under `datastorekit/` equal `v0.2.3`'s; `inspect.signature(DatastoreObject)` has `store_id` alone; `DatastoreObject(3, timestamp=t)` raises `TypeError: … got an unexpected keyword argument 'timestamp'`; `DatastoreObject.timestamp` does not exist |

- **The line numbers the prompt cites hold at `778c95a`**, with correction 6's readings:
  `README.md:10-19`, `:83`, `:86-89`, `:121-125`; `PROVENANCE.md:205` (the file is 240 lines, and
  that section is its last); the italic lines and appendices (`secondarygwkit.md:629`,
  `champbh.md:616`, `stochasticinstantons.md:581`); the README addendum ending the file at `:470`;
  `docs/adoption/README.md:81` (the module map's `Datastore` row: it maps a module, and stays
  true); SGK `:551-562`, CPBH `:540-545`, SI `:509-514`, `:35-41`, `:39`, `:78-105`, `:134-160` and
  `:154`; CPBH `:345-348` and SI `:319`; the extraction board's §2 at `:1532-1541`, whose G1–G4 rows
  are `:1536-1539`; contract §9.6 at `:357`. The prompt's grep finds, beyond its table: SGK `:78`,
  `:102-103`, `:111`, `:115` (import counts, unchanged) and `:238` (a test's name); CPBH `:104` and
  the factory table `:183-195`; SI `:113`, `:152-153` (`base._timestamp_column`, a different
  thing, still leaving the layer) and `:176-191`; README `:142`, `:407`, `:409`, `:430` (`TypeError`
  of U32, already superseded or history). None is superseded but by the prompt's table and
  correction 3; the log lists each with why it stays.
- **The toolchain.** `venv/`: Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39, SQLite 3.53.4,
  `black` 25.1.0, `datastorekit 0.2.3` editable from this checkout, no `setuptools`. `uv` 0.12.20.
  The high end, `uv venv --offline -p /opt/local/bin/python3.13`: 3.13.16, 2.55.1, 2.0.46, SQLite
  3.53.4.
- **Expected counts.**
  - The suite: **509**, before and after, at both ends; 0 `ResourceWarning` lines in `venv/`, 0
    or 4 at the high end (timing).
  - `compare_ported_tests.py`: exit 0, "20 module(s) … 1 test(s) declared not ported".
  - `black --check datastorekit docs`: **76** files, before and after.
  - The index: **4**, unchanged unless the work opens an issue.
- **Ray.** None up. Nothing in this prompt calls one of Ray's auto-init APIs: the release probes
  construct `DatastoreObject`s and run `sharded_store --help` only.

**What the review exists to establish.**
- **(E1) Scope.** Only the prompt's §7 files change. Nothing under `datastorekit/`, and not the
  contract, the verification document, `docs/extraction/` or the workflow.
- **(E2) The release.** A wheel from a clean export of the commit is `0.3.0`, holds 01's object and
  no tests, and behaves as §1.2 says from outside the repository.
- **(E3) The documents.** `pyproject.toml`, `README.md` and `PROVENANCE.md` as §2.1–§2.3 say (with
  correction 5); the change stated as added API that the layer neither sets nor reads; U6's pins
  exactly, advising CPBH and SGK neither way; nothing says `v0.3.0` is tagged; every name and link
  resolves.
- **(E4) The addenda.** Each additive, dated and placed as the additions say; each states its pin,
  what changed for its client, what it supersedes by `path:line` (with corrections 2 and 3), and
  the line shifts (correction 6), true at the file.
- **(E5) Both ends.** 509 in `venv/` (now `0.3.0`) and at the high end.
- **(E6) The breakages.** (a)–(c) fail as recorded.
- **(E7) The records**, and the extraction board's gates.

**Conventions.** `factory-defaults` 02's note's, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff **as recorded in the log** with `git apply --check` and `-R --check`
  against a scratch export;
- read a client only through `git`, and never import or run its code;
- use a subdirectory of the session scratchpad, never `/tmp`, for venvs, exports, wheels and
  probes; put no scratch `.py` under `datastorekit/` or `docs/`;
- run every scratch-venv command with its export, or a directory outside the repository, as the
  working directory (the prompt's hazard 9);
- a stop goes to the user, through the orchestrator;
- check `git log` before committing.

And for this prompt:
- **Start no Ray.** Nothing calls `ray.init`, `ray.kill`, `ray.get` or any other of Ray's auto-init
  APIs outside the suite.
- **No download of any kind.** Every venv and build is `--offline`; `venv/`'s reinstall is
  correction 1's.
- **Nothing is built in the checkout** but `venv/`'s editable reinstall, whose `egg-info` is
  removed.
- **No push, no tag, and no change to the GitHub repository's settings.**

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. Record `git status --short
   --ignored` (at writing: `.idea/`, `venv/` and five `__pycache__/` directories, one of them
   `docs/extraction/__pycache__/`).
2. **The baseline.** In `venv/`, `Ran 509 tests … OK` with no `ResourceWarning`; the port check
   exits 0; `black --check datastorekit docs` leaves 76 files unchanged; `pip show datastorekit`
   says `0.2.3`. (Taken at writing; re-take only if `HEAD` has moved outside `prompts/`.)
3. **The clients.** Each `HEAD` and `git status --short`, recorded (correction 4).
4. **The remote.** `git ls-remote origin`: `main` at `75c237e…` and the five tags as the gate says.
5. **Ray.** No Ray process; `RAY_ADDRESS` and `RAY_ENABLE_AUTO_CONNECT` unset.
6. **The index.** 4 now, and 4 after unless the work opens an issue. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, this board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `PROVENANCE.md`, log 01 (§1 and §8), `factory-defaults` prompt 02 and its log;
- `HEAD`, the clients' `HEAD`s and statuses, the counts and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's six corrections and its additions. Correction 1 is the
one that would stop it: the prompt's own reinstall fails in `venv/`. Correction 2 is the one that
would have it supersede a statement that is still true, of a gate that holds.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/02-release-v0.3.0.md`, in README §5.1's form, with
  the prompt's §5 item 6 additions.
- **The files it may change are the prompt's §7 list, and nothing else.** It must not touch:
  - anything under `datastorekit/`;
  - `docs/client-contract.md`, `docs/extraction-verification.md`, `docs/extraction/` or the
    workflow;
  - `CLAUDE.md`, `LICENSE` or `.gitignore`;
  - on the extraction board, anything but G3's and G4's rows;
  - anything under `orchestrator/`.
- **Under `docs/adoption/` it adds lines only.**
- **It writes nothing in any client repository, and runs, imports or opens nothing of one.**
- **It downloads nothing, and starts no Ray.**
- **It pushes nothing, makes no tag, and changes no setting of the GitHub repository.**
- **Stop and ask** on any of the prompt's §6 conditions.

## 3. The review — ten checks

Make the review's venvs, exports and wheels fresh, offline, in a subdirectory of the scratchpad of
their own, not the agent's.

1. **Scope (E1).** `git show --stat <commit>` touches only `pyproject.toml`, `README.md`,
   `PROVENANCE.md`, the four files under `docs/adoption/`, the extraction board, the log, this
   board, the campaign README, `prompts/INDEX.md`, and `docs/OPEN_ISSUES.md` only if an issue is
   opened. `git diff <parent> <commit> -- datastorekit docs/client-contract.md
   docs/extraction-verification.md docs/extraction .github CLAUDE.md` is empty. No wheel,
   `dist/`, `build/`, `*.egg-info` or scratch file; `git status --short --ignored` as at dispatch.
   Each client's `HEAD` and status recorded (correction 4).
2. **Additive (E1, E4).** `git diff <parent> <commit> -- docs/adoption/` has no `-` line.
   `pyproject.toml`'s diff is the version line alone. The extraction board's diff is G3's and G4's
   rows alone, each keeping every sentence it had.
3. **The release (E2).** From `git archive <commit>`, build the wheel offline and install it into a
   fresh high-end venv, offline. Check §1.2's facts as the facts above give them: 25 entries, none
   under `tests/`; the licence; `METADATA`; from outside the repository, `0.3.0`, the signature,
   the property's `fset` and `fdel`, the stamped and unstamped objects and `vars()`, the
   positional `TypeError`, the assignment's `AttributeError`, `pickle`, `datastorekit.tests`
   refused, `sharded_store --help`. The `RECORD` comparison with the review's own `v0.2.3` wheel:
   only `object.py`'s line differs. Compare the wheel's file list with the log's.
4. **`README.md` and `PROVENANCE.md`, by reading (E3).**
   - Status: a `v0.3.0` paragraph above `v0.2.3`'s, which is unchanged. It says the release is
     minor with one change, `object-timestamp` 01 on the user's ruling; the keyword-only argument
     and read-only property; that the layer never sets or reads it and a factory may pass the row's
     value; what a client can now meet (`_timestamp` in `vars()`, `AttributeError` from a subclass
     assigning `self.timestamp`); that nothing the layer writes or reads changes, and no message;
     that it adds API; and links §9.6 by anchor.
   - The pin is `v0.3.0`; the sentence replacing `:86-89` says the five earlier tags remain, none
     moved or deleted, that StochasticInstantons adopts `v0.3.0`, and that ChamPBH may stay on
     `v0.2.3` and SecondaryGWKit on `v0.2.2`, or either move, in a commit of its own, as it
     chooses. It names no client path, advises neither way, and nothing says `v0.3.0` is tagged.
   - "Using it": the "What changed after `v0.2.0`" item adds `v0.3.0`'s change, still linking §9.
   - `PROVENANCE.md`'s new `###` section follows the `factory-defaults` section; it says the change
     has no source in SGK (SGK's `object.py` at `6f7f291` takes `store_id` alone), that SI's own
     has taken `timestamp` since SI `51b04f8` (correction 5), positional-or-keyword where the
     package's is keyword-only; that it fixes no defect; and lists 01's files and log. Nothing
     above it changes.
5. **The addenda, by reading (E4).** For each of the four files:
   - the italic line is after `factory-defaults` 02's; the addendum is placed as the additions say,
     unnumbered, dated, and names `object-timestamp` prompt 02;
   - it gives its pin per U6, with `factory-defaults` U5 amended for G3 (and G4) and kept for G2;
   - what it says changed for its client is the prompt's row, true of `1b2f91a`'s package and of
     the client at the commit it names, and links §9.6;
   - each superseded statement is cited by a `path:line` that holds in the file as committed; the
     italic line moved them, so check each against the committed file;
   - correction 6's sentence is there, with N, k + N and 2k + N as numbers, each equal to the lines
     the italic lines added;
   - SI's says its 24 sites work as they stand once the import is rewritten, that its factories
     must go on passing the value, that item 2's paragraph asks nothing more of SI and
     `DatastoreObject.timestamp` no longer leaves the layer, and supersedes `:80-81` (correction
     3); CPBH's and SGK's say nothing changes that they meet, with no instruction to either;
     SGK's says G2 holds and supersedes neither `:553` nor `:625` (correction 2).
6. **Names and links, by running (E3, E4).** The review's own extraction of every relative link
   and anchor in the six documents and the extraction board's §2: each file exists, and each anchor
   is a heading by GitHub's rule. Every dotted `datastorekit.` name imports in the review's release
   venv. The list matches the log's.
7. **Both ends (E5).** In `venv/`: `pip show datastorekit` says `0.3.0`; `Ran 509 tests … OK`; no
   `datastorekit.egg-info/` at the root. In a fresh high-end venv with `git archive <commit>`
   installed editable: `Ran 509 tests … OK`, with the `ResourceWarning` lines counted (0 or 4). The
   port check exits 0. `black --check datastorekit docs` leaves 76 files unchanged.
8. **The breakages (E6).** Replay (a)–(c) as the log records them, each in its own export, against
   the facts' table. (c) must show all 20 `RECORD` lines equal to `v0.2.3`'s, no `timestamp` in the
   signature, and `TypeError` on the keyword.
9. **The records (E7).**
   - The log: every section of README §5.1, with the release check, the documents' check (§4.4),
     every name and link, §1.1's measure re-run, (a)–(c), the clients at both ends, the six
     corrections and the additions, and each addendum's supersession table.
   - The extraction board: G3 and G4 as the additions say; the rest unchanged.
   - This board: 02's row (landed, commit, log) and the header. The README's header and §2 row;
     `prompts/INDEX.md`'s line. `docs/OPEN_ISSUES.md` unchanged at 4, or as opened.
10. **Nothing left behind.** No Ray process. `git tag -l` is the five tags, and `origin` is
    unchanged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 02* paragraph, in the form of
  01's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on this board, the extraction board, the log, the README and
    `prompts/INDEX.md`;
  - "reviewed; awaiting CI for `v0.3.0`" for 02 in this board's header and row, README §2 and
    `prompts/INDEX.md`;
  - the notes line, with this note marked "used for 02".
- Anything the review finds that is not residue is opened on this board's §3 and in the index.
  **An issue open against 02's commit is a stop for the tag**: tell the user, and nothing in §5
  runs until they decide.
- **Report to the user:**
  - what landed: `0.3.0`, the README, `PROVENANCE.md`, the four addenda and the gates;
  - the release check and its `RECORD` comparison, and the 509 at both ends, from the review's own
    venvs;
  - §1.1's measure, re-run;
  - (a)–(c);
  - that the push carries `778c95a` and this note with 02 (§0);
  - **and ask for approval to push 02's commit** (§5).

## 5. Reaching `v0.3.0`

`factory-defaults` 02's note §5, with `v0.3.0` for `v0.2.3`, 02's commit for that 02's, and
`75c237e` for `85f504d`. Each push and the tag is an outward-facing act: **ask the user, and wait
for a clear yes, before each.** Approval of one is not approval of the next.

1. **Push 02's commit as `main`:** `git push origin <02's SHA>:refs/heads/main`. It fast-forwards
   from `75c237e`. The workflow runs on 02's commit at both ends; the smoke script is not
   collected, so CI starts no Ray.
2. **Read the run** once it has finished: `gh run list --workflow tests.yml --commit <02's SHA>`
   and `gh run view <id> --log`. Do not poll: ask the user to say when it has finished, or check
   once when they return. From each job's log, record the versions it prints (SQLite's among
   them), the suite's verdict (`Ran 509 tests … OK`) and black's line on `low`.
3. **If either end fails**, stop. No tag. Record the failure on this board's §3 with the job's log
   lines, open it in the index, and tell the user that a fix prompt is needed. The tag goes on the
   fix's commit once its CI passes.
4. **If both pass**, with the user's approval:
   - `git tag -a v0.3.0 <02's SHA> -m "datastorekit 0.3.0: DatastoreObject takes an optional, keyword-only timestamp and exposes it as a read-only property; the layer never sets or reads it"`;
   - `git push origin v0.3.0`;
   - check that `git ls-remote origin refs/tags/v0.3.0^{}` is 02's SHA.
5. **Record it, and close the campaign** (the prompt's §8), in a records commit of its own:
   - the extraction board's G3 and G4: one dated italic sentence each, in the form of the `v0.2.3`
     "is made" sentences: `v0.3.0` made, annotated, on 02's SHA, the tag object, the run's URL and
     both ends' versions and counts; for G4 that SI may now adopt it, for G3 that CPBH may adopt
     `v0.2.3` or `v0.3.0` (U6). G2 is unchanged;
   - this board: the review paragraph's last line, 02's row, and the header: **CLOSED**;
   - the campaign README's header and §2 row, and `prompts/INDEX.md`'s line: closed, with the
     tag; the count in `docs/OPEN_ISSUES.md` unchanged;
   - then **push the rest of `main`** (`git push origin main`), with approval.
6. **Hand the user** the tag object and commit, for SI's prompt 08, with README §0.2's four points
   to report back to the StochasticInstantons session, and the fifth of the prompt's §8 (SI's
   sixth `def timestamp`, the stand-in `tests/test_plot_adapters_golden.py:870`).

**Hand on.** `v0.3.0` is on 02's commit once §5 has run. SI adopts it in its prompt 08; CPBH may
stay on `v0.2.3` and SGK on `v0.2.2`, or either move (U6), each in a campaign of its own, in its
own repository; G3 and G4 are recorded on the extraction board as they hold. No campaign of this
repository is open after this one but `inherited-issues`' board, which has no prompts.
