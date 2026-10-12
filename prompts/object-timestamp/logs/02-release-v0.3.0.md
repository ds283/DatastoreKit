# Log 02 — release `v0.3.0`

**Subject:** Make the package ready to be released as v0.3.0 · **Commit:** this commit ·
**Date:** 2026-10-12 · **Model:** Claude Opus 5.5 · **Result:** landed; unpushed and untagged; not
yet reviewed.

The package is ready to be released as **`v0.3.0`** (U6). `pyproject.toml` says `0.3.0`, and
nothing else in it changed. `README.md` has a `v0.3.0` status paragraph, the `v0.3.0` pin with the
pins by client (SI adopts `v0.3.0`; CPBH may stay on `v0.2.3` and SGK on `v0.2.2`, or either may
move), and its "What changed after `v0.2.0`" item extended to `v0.3.0`. `PROVENANCE.md` has a
section for `object-timestamp` prompt 01. Each of the four files under `docs/adoption/` has an
italic line at its head and a dated section, "Addendum: v0.3.0 (object-timestamp prompt 02,
2026-10-12)", giving the pins, what changed for that client since `v0.2.3`, a table of every
statement it supersedes by `path:line`, and how to read the earlier addenda's citations (N, k + N
and 2k + N, correction 6). `git diff` of the four files has no `-` line. The extraction board's G3
reads "`v0.2.3` or later" and G4 "`v0.3.0`", each with a dated line saying the tag waits for CI;
G1 and G2 are unchanged.

**No line of code changed.** Nothing under `datastorekit/` is touched. The suite stays at **509**:
in `venv/` before and after (`pip show datastorekit` gives `0.3.0` after the offline reinstall), and
at the high end before and after, 0 `ResourceWarning` lines at every run. A wheel built offline from
an export of the tree is `datastorekit-0.3.0-py3-none-any.whl`, 25 entries, none under
`datastorekit/tests/`. Against `v0.2.3`'s wheel, of the 20 `RECORD` lines under `datastorekit/` only
`object.py`'s differs. Installed at the high pins and run from outside the repository, it behaves as
the prompt's §1.2 says. Breakage (a) fails the release check on `0.2.3`, (b) on the test package,
and (c), `v0.2.3`'s tree at `0.3.0`, on a `RECORD` with no line changed, a signature with no
`timestamp`, and `TypeError` at `DatastoreObject(3, timestamp=t)`. §1.1's measure of the clients,
re-run, reproduces at every commit read, SGK's and CPBH's `HEAD`s included.

**No tag was made and nothing was pushed.** Nothing was downloaded: every venv, install and build
is `uv … --offline`. No client was written, run, imported or opened. Ray was never started. No
issue was opened, and the index stays at **4**.

Prompt: [`../02-release-v0.3.0.md`](../02-release-v0.3.0.md), with the orchestrator's dispatch note
§0: six corrections, its additions, its checked facts and its conventions. §2 classifies each. Line
numbers under `datastorekit/` are `v0.3.0`'s tree (`1b2f91a`'s `datastorekit/`, which this commit
does not change) unless another tree is named.

`<scratch>` below is `<session scratchpad>/agent02`, outside the repository.

---

## 1. What shipped

### 1.1 `pyproject.toml` (§2.1)

`version = "0.2.3"` → `version = "0.3.0"` (`:7`), the only change. No other file carries the
version.

### 1.2 `README.md` (§2.2)

- **Status.** A new paragraph for **`v0.3.0`** (`:10-18`), above `v0.2.3`'s: a minor release with
  one change, `object-timestamp` prompt 01, on the user's ruling; `DatastoreObject` takes an
  optional, keyword-only `timestamp` and exposes it as a read-only property; the layer never sets
  or reads it (a factory reading a row of a class registered with `"timestamp": True` may pass the
  row's value, `None` otherwise); what a client can now meet, `_timestamp` in `vars()` and
  `AttributeError` from a subclass that assigns `self.timestamp`; nothing the layer writes or reads
  changes, and no message, refusal or exception; it adds API, so it is minor. It links
  `docs/client-contract.md#96-object-timestamp-prompt-01`.
- **Installing.** The pin is `@v0.3.0` (`:93`). The sentence at `:86-89` is replaced by `:96-99`:
  `v0.2.3`, `v0.2.2`, `v0.2.1`, `v0.2.0` and `v0.1.0` remain tagged and no tag is moved or deleted;
  StochasticInstantons adopts `v0.3.0`; ChamPBH may stay on `v0.2.3` and SecondaryGWKit on
  `v0.2.2`, or either may move, in a commit of its own, as it chooses: neither reads the value back,
  and nothing they call changes. Clients are named, no client path. Written as of the tag.
- **Using it.** "What changed after `v0.2.0`" (`:131-135`): `v0.3.0`'s change added, that a stored
  object may carry its row's `timestamp`, which a factory passes and the layer never sets or reads,
  linking §9.6, and still linking §9.
- Nothing else changed.

### 1.3 `PROVENANCE.md` (§2.3)

A new `###` section, "`object-timestamp` prompt 01: the object carries a timestamp (`v0.3.0`)"
(`:242`), after the `factory-defaults` section, under "After `v0.1.0`". Nothing above it changed.
It says:
- **the change has no source in SGK**: SGK's `Datastore/object.py` at `6f7f291` takes `store_id`
  alone, and the package carried it over; SI's own `Datastore/object.py`, added at SI `3e56d39`
  (2026-06-15) taking `store_id` alone, has taken a `timestamp` and exposed it read-only since SI
  `51b04f8` (2026-06-21) (correction 5); SI asked the package for the same; U1, on the user's
  ruling, adds it keyword-only, where SI's is positional-or-keyword; the layer never sets or reads
  it; it fixes no defect; its test module and contract §9.6;
- **what changed in the package**: `datastorekit/object.py` only (18/1), as the prompt says; outside
  the wheel, `TestTheVersionObject`'s dict (U2), the new `tests/client/stamped.py` and test module,
  contract §9.6 and verification §4.9; the suite 504 → 509;
- **the files 01 changes, and its log** (from `git show --stat 1b2f91a`, records excluded).

### 1.4 The addenda (§2.4, U6)

Each file gains an italic line at its head, after `factory-defaults` prompt 02's, and an unnumbered
section `## Addendum: v0.3.0 (object-timestamp prompt 02, 2026-10-12)`, anchor
`#addendum-v030-object-timestamp-prompt-02-2026-10-12`:
- in the README the italic line is `:22-25`, then a blank, and the section is at the end, after a
  `---` (heading `:479`, the file ending at `:597`);
- in each checklist the italic line is five lines and a blank, after the `v0.2.3` italic line's
  blank (SGK `:33-37`, CPBH `:34-38`, SI `:32-36`). The section follows the `v0.2.3` addendum's
  table, with a `---` of its own above it, and comes before the `---` that precedes the appendix
  (headings SGK `:635`, CPBH `:622`, SI `:587`; appendix SGK `:726`, CPBH `:704`, SI `:679`).

Each section gives:
- the pins by client (U6): SI `…@v0.3.0`; CPBH `…@v0.2.3` or `…@v0.3.0`; SGK `…@v0.2.2`, `…@v0.2.3`
  or `…@v0.3.0`; a move being a commit of the client's own; that U6 amends `factory-defaults` U5 for
  CPBH and SI and keeps it for SGK; how G3 and G4 now read; G2's reading unchanged, and G2 holding;
- what changed for that client since `v0.2.3`, with contract §9.6 linked by anchor (the README
  addendum's table gives the row's parts at `v0.2.3` and at `v0.3.0`);
- §1.1's measure, as re-run (§5.4): in the README as one table, in each checklist for that client;
- the rule for line citations: 07a's `datastorekit/` lines are `v0.2.0`'s, the `v0.2.1` addendum's
  `v0.2.1`'s, the `v0.2.2` addendum's `v0.2.2`'s, the `v0.2.3` addendum's `v0.2.3`'s, and this
  addendum's `v0.3.0`'s (`1b2f91a`'s `datastorekit/`);
- a supersession table, with the reading of the earlier addenda's citations above it:

| File | Lines added | Lines removed | Inserted after (at `0de2b16`) | N | k | k + N | 2k + N |
|---|---|---|---|---|---|---|---|
| `docs/adoption/README.md` | 127 | 0 | `:21` | **5** | 5 | **10** | **15** |
| `docs/adoption/secondarygwkit.md` | 97 | 0 | `:32` | **6** | 6 | **12** | **18** |
| `docs/adoption/champbh.md` | 88 | 0 | `:33` | **6** | 6 | **12** | **18** |
| `docs/adoption/stochasticinstantons.md` | 98 | 0 | `:31` | **6** | 6 | **12** | **18** |

So: the `v0.2.3` addendum's citations are read at `0de2b16`, or N lines later here, except those
above the insert (the `v0.2.2` italic line it cites: README `:12-15`, SGK `:21-25`, CPBH `:22-26`,
SI `:20-24`); the `v0.2.2` addendum's at `6d8ee9a`, or k + N lines later, except README `:7-10`,
SGK `:16-19`, CPBH `:17-20`, SI `:15-18`; the `v0.2.1` addendum's at `33778b0`, or 2k + N lines
later, except README `:3`, SGK and CPBH `:6`, SI `:5`. Each addendum states the three numbers.
Checked line by line (§5.7): 222 lines, 0 differ.

The four tables are repeated in §4.

### 1.5 The extraction board's gates (§2.5)

`prompts/extraction/IMPLEMENTATION_STATE.md` §2, rows G3 and G4 (`:1538-1539`), and nothing else on
that board (`git diff --numstat`: 2/2):
- titles, exactly: G3 "CPBH adopted `v0.2.3` or later (U37; `actor-names` U3; `factory-defaults`
  U5; `object-timestamp` U6)"; G4 "SI adopted `v0.3.0` (U37; `actor-names` U3; `factory-defaults`
  U5; `object-timestamp` U6)";
- each status cell gains, at its end, one dated italic sentence: "*(2026-10-12: `v0.3.0` is ready to
  be tagged on `object-timestamp` prompt 02's commit once CI passes there at both ends, as U23 and
  U28; 02 makes no tag and pushes nothing. <Client>'s addendum is [link to its `v0.3.0` anchor].)*";
  G3's says too that "CPBH may stay on `v0.2.3` or move to `v0.3.0`, as it chooses
  (`object-timestamp` U6)". `git diff --word-diff` shows only the title words and the appended
  sentence. G1 and G2 (`:1536-1537`) and the board's header are unchanged.

### 1.6 The records

- This log.
- This board: the header, and §1's row for 02 (landed, "this commit", log).
- This campaign's README: a sentence in its header, and §2's row for 02.
- `prompts/INDEX.md`: `object-timestamp`'s status.
- `docs/OPEN_ISSUES.md` is unchanged at **4**: no issue opened.

---

## 2. Deviations from the prompt

1. **Correction 1: `venv/`'s reinstall is `uv pip install --offline --no-deps --python
   venv/bin/python -e .`**, from the repository root, not hazard 6's command with
   `--no-build-isolation` (`venv/` has no `setuptools`: `import setuptools` raised
   `ModuleNotFoundError` there at the start). Its output: `- datastorekit==0.2.3`,
   `+ datastorekit==0.3.0`, exit 0. `pip show datastorekit` gives `Version: 0.3.0`, editable from
   this checkout. It wrote `datastorekit.egg-info/` at the root, which I deleted at once; afterwards
   `importlib.metadata.version("datastorekit")` is `0.3.0`, the package imports from the source
   tree, and `git status --short --ignored` lists only dispatch's ignored entries.
   **STRUCTURALLY REQUIRED.**
2. **Correction 2: SGK's G2 statement is not superseded.** SGK's addendum supersedes the `v0.2.3`
   addendum's pin in part (`:557-559`, its "or move to `v0.2.3`"; the pins `:561-569`; the table rows
   `:623`, in part, `:624`, `:626-627`, `:628`), and names `:559`'s G2 reading and the row `:631` as
   standing, not superseded, with G2 holding (2026-10-12, recorded at `6465a6a`). Nothing advises
   SGK to stay or move. **STRUCTURALLY REQUIRED.**
3. **Correction 3: SI's `:80-81` (here `:86-87`)**, "The package's `DatastoreObject`
   (`datastorekit/object.py:9`) takes `store_id` only", is superseded in its own row of SI's table,
   beside item 2's others; `:78-80` (here `:84-86`) and `:102-103` (here `:108-109`) are named as
   still holding. Recorded as found.
4. **Correction 4: the clients moved under the prompt, and again during the work.** CPBH was
   `0f1c25b` at my start (dispatch read `cb0c675`; `0f1c25b`, "Write dk-and-rpk-migration prompts 05
   and 06", is another session's), and stayed there. SGK was `e3a7077` at my start and `cf978c6` at
   the end ("Record the review of runregistry-extraction prompt 01", another session's, by way of
   `d94d66b` and `a45aefc`). I re-ran §1.1's measure at every one, with the same result (§5.4), so no
   stop. The addenda name the commits read. Recorded as found.
5. **Correction 5: `PROVENANCE.md`** says SI's `DatastoreObject` file was added at SI `3e56d39`
   (2026-06-15) taking `store_id` alone, and has taken a `timestamp` since SI `51b04f8` (2026-06-21),
   both read through `git log --diff-filter=A` and `git show`. Recorded as found.
6. **Correction 6: N, k + N and 2k + N are stated in each addendum**, as numbers (§1.4): N = 5 in
   the README and 6 in each checklist; k + N = 10 and 12; 2k + N = 15 and 18. Checked line by line
   with `<scratch>/probe/check_shift.py` (§5.7): 222 lines, 0 differ. **STRUCTURALLY REQUIRED.**
7. **Statements superseded that the prompt's table does not name**, by §2.4's rule. Each is in its
   file's table (§4). **STRUCTURALLY REQUIRED.**
   - In each file, the `v0.2.3` addendum's "Each `path:line` is this file's as committed with this
     addendum", with its shift numbers (README `:454-460`, SGK `:609-615`, CPBH `:598-604`, SI
     `:563-569`), and its table row giving the `v0.2.2` addendum's shift (README `:469`, SGK `:625`,
     CPBH `:614`, SI `:579`): no longer true once the head line moves its lines.
   - In each file, the `v0.2.3` addendum's italic head line (README `:17-20`, SGK `:27-31`, CPBH
     `:28-32`, SI `:26-30`), which gives `v0.2.3`'s pin (and, in the README, says "at the end").
   - In the README: the table rows that give pins or gates by reference (`:470-471`, `:473-474`),
     and `:472` ("each checklist with its three addenda"), as the orchestrator's additions list.
   - In SGK's: the rows `:629` (at `v0.2.3` "also the change of contract §9.5, which changes nothing
     SGK's calls use") and `:630` (item 8's reasoning "extended to `v0.2.3`"), which name `v0.2.3`
     as the extent of their reasoning; each is extended to `v0.3.0`.
   - In SI's: the one paragraph's clause cited as `:44-45`, not the prompt's `:39` (here `:45`):
     the clause starts on the line before ("Unlike CPBH, …"). And the `getattr` reads (`:106`) and
     item 2's last line (`:111`) each have a row of their own.
8. **The orchestrator's additions** are followed as given, each an **IMPLEMENTATION CHOICE** at the
   orchestrator's direction:
   - the order of work (baseline; `pyproject.toml`, the reinstall and the suite; the two documents;
     the addenda and hazard 1's diff; the gates; the release check and the high end; (a)–(c); the
     documents' and link checks; the end);
   - each addendum's supersessions as a table, repeated in §4;
   - the `v0.2.3` addenda's pin and gate statements cited as they stand after the italic line;
   - placement: the `---` rules, the README's addendum at the end, the heading and its anchor;
   - the README's `v0.3.0` table of §1.1, one row per client, SI's other sites summarised;
   - `PROVENANCE.md`'s new section as a `###`;
   - the contract anchors `#96-object-timestamp-prompt-01` and `#9-changes-after-v020`;
   - the gate titles exactly as given, one dated italic sentence per row, G3's with CPBH's choice;
   - the name-and-link check as a scratch script, never committed;
   - (a), (b) and (c) each built from its own export;
   - §1.1's measure by a script of my own (`<scratch>/probe/measure_objects.py`), `ast` reads of
     `git show`, run with `python3.13 -I`.
9. **The exports are of the working tree before the records were written**, made with `git archive
   $(git stash create)`: commit object `2337dff`, whose tree equalled the working tree then (`git
   diff --quiet 2337dff` held). `git stash create` writes no ref, and `git stash list` stayed empty.
   That tree differs from this commit's in the records (this log, this board, this campaign's
   README, `prompts/INDEX.md`) and in four later edits to lines this prompt added under
   `docs/adoption/`: SI's row for `:86-87` reworded (so that its `:84-86` follows this file's path,
   not `datastorekit/object.py`'s); SGK's `cf978c6` added to the SGK addendum's measure bullet and
   pin sentence, and to the README addendum's table row and pins bullet, with one bullet rewrapped.
   None is in the wheel. `pyproject.toml` and `datastorekit/` are this commit's, so (a)'s and (b)'s
   diffs apply to an export of this commit as recorded. The suite in `venv/` was run on the final
   tree (§5.1). **IMPLEMENTATION CHOICE.**
10. **Checks not asked for.** The cross-release pickle the README addendum states: a
    `DatastoreObject(3)` pickled under (c)'s install (`v0.2.3`'s code) and unpickled under the
    release has `vars()` `{'_my_id': 3}`, and its `timestamp` raises `AttributeError: 'DatastoreObject'
    object has no attribute '_timestamp'`; under `v0.2.3`, `DatastoreObject(3).timestamp` raises
    `AttributeError: 'DatastoreObject' object has no attribute 'timestamp'`, which the README
    addendum's table states. And a `git grep` of `pickle`, `joblib`, `cloudpickle`, `shelve` and
    `dill` dumps in each client at the `HEAD` read: in-memory round trips (SGK's tests and stand-in
    pool), commented-out lines (CPBH and SI `Datastore/SQL/Datastore.py`), and SI's
    `regression_InstantonOutputs.py:370`, of regression models. **IMPLEMENTATION CHOICE.**
11. **The README addendum states, beyond the prompt's list, the cross-release pickle and the
    clients' pins as read**, each checked (item 10, §5.4). And the CPBH addendum names item 8's
    `ReplicatedDivergence` on `timestamp` (`:351-354`) as unchanged, the stamp being the actor's,
    not the object's. **IMPLEMENTATION CHOICE.**

---

## 3. The hazards (§3)

1. **Additive documents.** `git diff --numstat -- docs/adoption` gives 127/0, 97/0, 88/0 and 98/0,
   and `git diff -- docs/adoption | grep '^-' | grep -v '^--- '` finds nothing. Each insertion was
   made by `<scratch>/probe/insert.py`, which adds lines only, after checking the line before and
   after the insert point. Later edits changed only lines this prompt had added (§2 item 9, and
   CPBH's citation of item 5's table, first `:189-201`, corrected to `:189-207`, its full extent).
   `docs/client-contract.md` and `docs/extraction-verification.md` are unchanged.
2. **Names and links.** Every one resolves (§5.5). The contract anchor, by GitHub's rule: "9.6
   `object-timestamp` prompt 01" (`docs/client-contract.md:357`), lower-cased, with the `.` and the
   backticks dropped and the spaces made hyphens, is `96-object-timestamp-prompt-01`. Each new
   heading, "Addendum: v0.3.0 (object-timestamp prompt 02, 2026-10-12)", the same way (the `:`,
   `.`, `(`, `)` and `,` dropped) is `addendum-v030-object-timestamp-prompt-02-2026-10-12`. The
   script derives every heading's slug that way and finds each anchor among them.
3. **The tag does not exist yet.** No document says `v0.3.0` is tagged: the README and the addenda
   state the pins, and the README says `v0.2.3`, `v0.2.2`, `v0.2.1`, `v0.2.0` and `v0.1.0` "remain
   tagged"; the gates say `v0.3.0` "is ready to be tagged … once CI passes there at both ends", and
   that 02 makes no tag.
4. **No client is re-measured beyond §1.1.** I re-ran §1.1's measure with a script of my own
   (§5.4). It reproduces §1.1's table exactly at SI `7bb3efd`, at SGK `d03a643`, `e3a7077` and
   `cf978c6`, and at CPBH `64ef9aa`, `cb0c675` and `0f1c25b`. No SGK or CPBH call passes anything but
   `store_id`, and no descendant defines or assigns `timestamp`. No stop.
5. **Offline only.** Every venv (`uv venv --offline`), install (`uv pip install --offline`) and
   build (`uv build --offline`) resolved from the cache: `setuptools` 84.0.0 (the build backend),
   `ray` 2.55.1 and `sqlalchemy` 2.0.46. Nothing was downloaded.
6. **`venv/`'s metadata.** Reinstalled by correction 1's command, the `egg-info` removed; the suite
   in `venv/` gives 509 OK after it (§5.1).
7. **No Ray.** The smoke script was not run. The release probes construct `DatastoreObject`s and
   run `sharded_store --help` only, and `ray.is_initialized()` is `False` after them; the name
   check imports names, `ray.is_initialized()` `False` after. At the start and the end no Ray
   process was up (`pgrep -lf 'gcs_server|raylet|ray::'` empty), `RAY_ADDRESS` and
   `RAY_ENABLE_AUTO_CONNECT` were unset, and there was no `/tmp/ray/ray_current_cluster`.
8. **U6's wording.** Every statement of CPBH's and SGK's pins is permission, with no advice either
   way: "may stay … or move …, as it chooses" (README `:97-99`; each addendum and its head line; the
   README addendum; G3's line). None says CPBH or SGK should or should not move.
9. **Run from the right place.** Every scratch-venv command ran with its export or
   `<scratch>/outside` as the working directory, `PYTHONPATH` unset. `datastorekit.__file__`:
   `venv/`, `<repo>/datastorekit/__init__.py` (editable, as intended); `venv-high-before` and
   `venv-high`, the export's `datastorekit/__init__.py`; `venv-release` and each breakage's venv,
   its `site-packages/datastorekit/__init__.py`.

---

## 4. The supersession tables

Each is as committed in its addendum. Line numbers are each file's at this commit.

### 4.1 `docs/adoption/README.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/README.md:17-20` | the `v0.2.3` addendum, "at the end", gives "the pins by client" | it gives `v0.2.3`'s pins and changes, true of `v0.2.3`; this addendum, now at the end, gives the pins of `v0.3.0` |
| `docs/adoption/README.md:387-396` | "CPBH and SI adopt `v0.2.3`", G3 and G4 reading "CPBH has adopted `v0.2.3`" and "SI has adopted `v0.2.3`", the pin `…@v0.2.3`; and SGK "may stay on `v0.2.2` or move to `v0.2.3`" | SI adopts `v0.3.0`, and G4 reads "SI has adopted `v0.3.0`"; CPBH may stay on `v0.2.3` or move to `v0.3.0`, and G3 reads "CPBH has adopted `v0.2.3` or later"; SGK may stay on `v0.2.2` or move to `v0.2.3` or `v0.3.0`, and G2's reading is unchanged (`object-timestamp` U6); "The pins, by client", above |
| `docs/adoption/README.md:398-399` | "`v0.2.3` carries `key_on_version`, `v0.2.0`'s feature, `v0.2.1`'s three fixes and `v0.2.2`'s fix, unchanged" | true of `v0.2.3`; `v0.3.0` carries those and `v0.2.3`'s change, unchanged |
| `docs/adoption/README.md:454-460` | the `v0.2.3` addendum's `path:line`s are "this file's as committed with this addendum", and the earlier addenda's are read five and ten lines later | they are read at `0de2b16`, or five lines later here; the `v0.2.2` addendum's ten, and the `v0.2.1` addendum's fifteen; above |
| `docs/adoption/README.md:467` | the row for `:289-290`: "CPBH and SI adopt `v0.2.3`, and SGK may stay on `v0.2.2` or move (`factory-defaults` U5)" | as `:387-396` |
| `docs/adoption/README.md:468` | the row for `:293`: "for CPBH and SI the pin `…@v0.2.3`; for SGK `…@v0.2.2` or `…@v0.2.3`" | for SI the pin `…@v0.3.0`; for CPBH `…@v0.2.3` or `…@v0.3.0`; for SGK `…@v0.2.2`, `…@v0.2.3` or `…@v0.3.0` |
| `docs/adoption/README.md:469` | the row for `:351-355`: the `v0.2.2` addendum's citations "are read at `6d8ee9a`, or five lines later here" | at `6d8ee9a`, or ten lines later here (all but `:7-10`) |
| `docs/adoption/README.md:470-471` | the rows for `:360` and `:361`, "as `:289-290`" and "as `:293`" | as `:467` and `:468` |
| `docs/adoption/README.md:472` | the row for `:364`: "at `v0.2.3`, each checklist with its three addenda" | at `v0.3.0`, each checklist with its four addenda |
| `docs/adoption/README.md:473-474` | the rows for `:365` and `:366`, "as `:289-290`" and "as `:293`" | as `:467` and `:468` |
| `docs/adoption/README.md:475` | the row for `:367`: "G2 holds when SGK has adopted `v0.2.2` or later, and G3 and G4 when CPBH and SI have adopted `v0.2.3` (U37; `actor-names` U3; `factory-defaults` U5)" | G2 holds when SGK has adopted `v0.2.2` or later, as before; G3 when CPBH has adopted `v0.2.3` or later, and G4 when SI has adopted `v0.3.0` (U37; `actor-names` U3; `factory-defaults` U5; `object-timestamp` U6) |

Not in the prompt's table: `:17-20`, `:454-460`, `:469` (correction 6's shift); `:470-474` by the
orchestrator's additions. The module-map row (`:86`) is named as not superseded.

### 4.2 `docs/adoption/secondarygwkit.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/secondarygwkit.md:27-31` | the `v0.2.3` addendum gives "SGK's pin, `v0.2.2` or `v0.2.3` as SGK chooses" | it gives `v0.2.3`'s pins and changes, true of `v0.2.3`; this addendum gives SGK's pins at `v0.3.0`: `v0.2.2`, `v0.2.3` or `v0.3.0`, as SGK chooses |
| `docs/adoption/secondarygwkit.md:557-559` | in part: "SGK may stay on **`v0.2.2`** or move to **`v0.2.3`**, as SGK chooses" | SGK may stay on `v0.2.2` or move to `v0.2.3` or `v0.3.0`, as SGK chooses (`object-timestamp` U6); "The pin", above. The rest of the sentence stands: a move is a commit of SGK's own, and G2 reads "SGK has adopted `v0.2.2` or later" |
| `docs/adoption/secondarygwkit.md:561-569` | the pins `…@v0.2.2` or `…@v0.2.3` | `…@v0.2.2`, `…@v0.2.3` or `…@v0.3.0`, above |
| `docs/adoption/secondarygwkit.md:609-615` | the `v0.2.3` addendum's `path:line`s are "this file's as committed with this addendum", and the earlier addenda's are read six and twelve lines later | they are read at `0de2b16`, or six lines later here; the `v0.2.2` addendum's twelve, and the `v0.2.1` addendum's eighteen; above |
| `docs/adoption/secondarygwkit.md:623` | in part, the row for `:460-461`: SGK "may stay on `v0.2.2` or move to `v0.2.3` (`factory-defaults` U5)" | or move to `v0.2.3` or `v0.3.0` (`object-timestamp` U6). The row's G2 reading stands |
| `docs/adoption/secondarygwkit.md:624` | the row for `:464`: "`…@v0.2.2` or `…@v0.2.3`, as SGK chooses, above" | as `:561-569` |
| `docs/adoption/secondarygwkit.md:625` | the row for `:523-527`: the `v0.2.2` addendum's citations "are read at `6d8ee9a`, or six lines later here" | at `6d8ee9a`, or twelve lines later here (all but `:16-19`) |
| `docs/adoption/secondarygwkit.md:626-627` | the rows for `:532` and `:533`, "as `:460-461`" and "as `:464`" | as `:623` and `:624` |
| `docs/adoption/secondarygwkit.md:628` | the row for `:536`: "at `v0.2.2` or `v0.2.3`, with the three addenda" | at `v0.2.2`, `v0.2.3` or `v0.3.0`, with the four addenda |
| `docs/adoption/secondarygwkit.md:629` | the row for `:537`: at `v0.2.3` "also the change of contract §9.5, which changes nothing SGK's calls use" | at `v0.3.0` also the change of contract §9.6, which changes nothing SGK's calls use, since SGK passes `store_id` alone; "SGK passes `store_id` alone", above |
| `docs/adoption/secondarygwkit.md:630` | the row for `:538`: item 8's reasoning "extended to `v0.2.3`" | extended to `v0.3.0`; "Item 8 still holds", above |

Standing, not superseded (correction 2): `:559`'s G2 reading and the row `:631`. Not in the
prompt's table: `:27-31`, `:609-615`, `:625`, `:629`, `:630`.

### 4.3 `docs/adoption/champbh.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/champbh.md:28-32` | the `v0.2.3` addendum gives the pin **`v0.2.3`** | it gives `v0.2.3`'s pin and changes, true of `v0.2.3`; this addendum gives CPBH's pins at `v0.3.0`: `v0.2.3` or `v0.3.0`, as CPBH chooses |
| `docs/adoption/champbh.md:546-548` | "CPBH adopts **`v0.2.3`** in place of `v0.2.2`", and G3 reads "CPBH has adopted `v0.2.3`" | CPBH may stay on `v0.2.3` or move to `v0.3.0` (`object-timestamp` U6), and G3 reads "CPBH has adopted `v0.2.3` or later"; "The pin", above |
| `docs/adoption/champbh.md:550-552` | the pin `…@v0.2.3` | `…@v0.2.3` or `…@v0.3.0`, as CPBH chooses, above |
| `docs/adoption/champbh.md:598-604` | the `v0.2.3` addendum's `path:line`s are "this file's as committed with this addendum", and the earlier addenda's are read six and twelve lines later | they are read at `0de2b16`, or six lines later here; the `v0.2.2` addendum's twelve, and the `v0.2.1` addendum's eighteen; above |
| `docs/adoption/champbh.md:612` | the row for `:478-479`: CPBH adopts `v0.2.3` in place of `v0.2.2`, and G3 reads "CPBH has adopted `v0.2.3`" | as `:546-548` |
| `docs/adoption/champbh.md:613` | the row for `:482`: "the pin `…@v0.2.3`, above" | as `:550-552` |
| `docs/adoption/champbh.md:614` | the row for `:515-519`: the `v0.2.2` addendum's citations "are read at `6d8ee9a`, or six lines later here" | at `6d8ee9a`, or twelve lines later here (all but `:17-20`) |
| `docs/adoption/champbh.md:615-616` | the rows for `:524` and `:525`, "as `:478-479`" and "the pin `…@v0.2.3`, above" | as `:546-548` and `:550-552` |
| `docs/adoption/champbh.md:617` | the row for `:527`: "at `v0.2.3`, with the three addenda" | at `v0.2.3` or `v0.3.0`, as CPBH chooses, with the four addenda |
| `docs/adoption/champbh.md:618` | the row for `:528`: "G3 holds when CPBH has adopted `v0.2.3` (U37; `actor-names` U3; `factory-defaults` U5)" | G3 holds when CPBH has adopted `v0.2.3` or later (U37; `actor-names` U3; `factory-defaults` U5; `object-timestamp` U6) |

Not in the prompt's table: `:28-32`, `:598-604`, `:614`.

### 4.4 `docs/adoption/stochasticinstantons.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/stochasticinstantons.md:26-30` | the `v0.2.3` addendum gives the pin **`v0.2.3`** | it gives `v0.2.3`'s pin and changes, true of `v0.2.3`; this addendum gives `v0.3.0` |
| `docs/adoption/stochasticinstantons.md:44-45` | in the one paragraph, "SI's `DatastoreObject` carries a `timestamp`, which the package's lacks" | true through `v0.2.3`. At `v0.3.0` the package's carries one too, keyword-only; "What changed for SI since `v0.2.3`", above |
| `docs/adoption/stochasticinstantons.md:86-87` | "The package's `DatastoreObject` (`datastorekit/object.py:9`) takes `store_id` only" | true of `v0.2.0`, whose line it cites, through `v0.2.3`; the sentence before it (`:84-86`), that SI's own takes `timestamp` and exposes it, still holds. At `v0.3.0` the package's takes `store_id` and a keyword-only `timestamp` (`datastorekit/object.py:10-14`) |
| `docs/adoption/stochasticinstantons.md:88` | "the 14 direct calls `DatastoreObject.__init__(…, timestamp=…)` raise `TypeError`" | under `v0.3.0` each is accepted as it stands. The sites (`:89-96`) and the ten pass-throughs (`:97-102`) still hold |
| `docs/adoption/stochasticinstantons.md:104` | the direct reads of `.timestamp` "would raise `AttributeError` without it" | under `v0.3.0` they get what SI's factories pass. The sites still hold |
| `docs/adoption/stochasticinstantons.md:106` | the reads by `getattr`, which "would quietly get `None`" | the same |
| `docs/adoption/stochasticinstantons.md:111` | "Whether SI drops the timestamp or keeps it on its own classes is SI's choice" | under `v0.3.0` SI keeps it on the package's `DatastoreObject`, its sites as they stand (the user's ruling, `object-timestamp` README §0); whether its factories pass it stays SI's. The test stand-ins (`:108-109`) still hold |
| `docs/adoption/stochasticinstantons.md:160` | item 4: "**`DatastoreObject.timestamp`** (item 2)" leaves the layer | it does not leave the layer: the package's object carries it. The rest of item 4 still holds |
| `docs/adoption/stochasticinstantons.md:515-521` | "SI adopts **`v0.2.3`** in place of `v0.2.2`, when it is next active", G4 reads "SI has adopted `v0.2.3`", and the pin `…@v0.2.3` | SI adopts `v0.3.0` in place of `v0.2.3`, when it is next active (`object-timestamp` U6), and G4 reads "SI has adopted `v0.3.0`"; the pin `…@v0.3.0`, above |
| `docs/adoption/stochasticinstantons.md:563-569` | the `v0.2.3` addendum's `path:line`s are "this file's as committed with this addendum", and the earlier addenda's are read six and twelve lines later | they are read at `0de2b16`, or six lines later here; the `v0.2.2` addendum's twelve, and the `v0.2.1` addendum's eighteen; above |
| `docs/adoption/stochasticinstantons.md:577` | the row for `:448-450`: SI adopts `v0.2.3` in place of `v0.2.2`, and G4 reads "SI has adopted `v0.2.3`" | as `:515-521` |
| `docs/adoption/stochasticinstantons.md:578` | the row for `:453`: "the pin `…@v0.2.3`, above" | the pin `…@v0.3.0`, above |
| `docs/adoption/stochasticinstantons.md:579` | the row for `:484-488`: the `v0.2.2` addendum's citations "are read at `6d8ee9a`, or six lines later here" | at `6d8ee9a`, or twelve lines later here (all but `:15-18`) |
| `docs/adoption/stochasticinstantons.md:580-581` | the rows for `:493` and `:494`, "as `:448-450`" and "the pin `…@v0.2.3`, above" | as `:515-521` |
| `docs/adoption/stochasticinstantons.md:582` | the row for `:496`: "at `v0.2.3`, with the three addenda" | at `v0.3.0`, with the four addenda |
| `docs/adoption/stochasticinstantons.md:583` | the row for `:497`: "G4 holds when SI has adopted `v0.2.3` (U37; `actor-names` U3; `factory-defaults` U5)" | G4 holds when SI has adopted `v0.3.0` (U37; `actor-names` U3; `factory-defaults` U5; `object-timestamp` U6) |

Not in the prompt's table: `:26-30`, `:86-87` (correction 3), `:563-569`, `:579`; and `:106`,
`:111` as rows of their own.

**Considered and not superseded.** The grep of §2.4 (`timestamp`, `DatastoreObject`, `v0.2.3`,
`TypeError`) outside the new addenda finds, at this tree:
- README `:86` (the module map's `Datastore` row): maps a module, true (named in the addendum);
  `:147`, `:412`, `:414`, `:435` (`TypeError` of U32): already superseded by the `v0.2.3` addendum,
  or history of `v0.2.2`;
- SGK `:84` (`Datastore/__init__.py:1` re-exports `DatastoreObject`), `:108-109`, `:117`, `:121`
  (import counts) and `:244` (a test's name, `test_one_timestamp_per_write`): facts of SGK at
  `b510bc9`, true; every import-map row naming `DatastoreObject`: a module path, unchanged;
- CPBH `:110` (import counts), the factory table's `timestamp` column (`:189-207`), `:351-354`
  (`ReplicatedDivergence` on `timestamp`, the actor's stamp): true, and the last named in the
  addendum; `:221`, `:256` (other `TypeError`s): already superseded or true;
- SI `:84-86` and `:108-109` (named as holding), `:119` (import counts), `:158-159`
  (`base._timestamp_column`, a different thing, which still leaves the layer), the factory table
  (`:182-197`), `:325` (the replicated stamp), `:138`, `:205`, `:251` (other `TypeError`s): true or
  already superseded;
- in each checklist, the `v0.2.3` addendum's statements of what `v0.2.3` carries and its findings
  for that client: true of `v0.2.3`.

---

## 5. Verification performed

### 5.1 The suite (§4.1)

Every run in the foreground, its output in `<scratch>/out/`, the verdict grepped from it.

| Where | When | Result | `ResourceWarning` lines | `datastorekit` |
|---|---|---|---|---|
| `venv/` (3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39, SQLite 3.53.4) | at dispatch, before any change | `Ran 509 tests in 86.444s` `OK` | 0 | 0.2.3 |
| `<scratch>/venv-high-before` (3.13.16 / 2.55.1 / 2.0.46, SQLite 3.53.4, `setuptools` 84.0.0), `git archive HEAD` (`b56fdde`) installed editable `--no-deps --no-build-isolation` | at dispatch | `Ran 509 tests in 99.793s` `OK` | 0 | 0.2.3 |
| `venv/` | after `pyproject.toml` and the reinstall | `Ran 509 tests in 98.710s` `OK` | 0 | 0.3.0 |
| `<scratch>/venv-high`, the same pins, `git archive 2337dff` installed editable `--no-deps --no-build-isolation` | after the document edits | `Ran 509 tests in 91.842s` `OK` | 0 | 0.3.0 |
| `venv/` | after the records, before the commit | `Ran 509 tests in 85.585s` `OK` | 0 | 0.3.0 |

The count is **509** before and after, at both ends.

### 5.2 The checks (§4.2)

- `compare_ported_tests.py`, before and after, exit 0, its last line: `OK: 20 module(s) keep their
  source's tests, classes and assertion skeletons; 1 test(s) declared not ported`.
- `./venv/bin/black --check datastorekit docs` (black 25.1.0), before and after: `76 files would be
  left unchanged.` No `.py` file changed.
- The two guards, `test_layer_is_generic` and `test_prose_names_no_source`, are in the suite and
  pass in every run above.

### 5.3 The release check (§4.3)

**The build.** `git archive 2337dff | tar -x -C <scratch>/exports/release` (§2 item 9), then
`uv build --offline --wheel --out-dir <scratch>/wheels/release <scratch>/exports/release`, exit 0.
For the comparison, `git archive v0.2.3` into `<scratch>/exports/v023`, built the same way. Nothing
was built in the checkout.

| | The release | `v0.2.3`'s, for comparison |
|---|---|---|
| Wheel | `datastorekit-0.3.0-py3-none-any.whl` | `datastorekit-0.2.3-py3-none-any.whl` |
| Size | 99,488 bytes | 99,185 bytes |
| Entries | **25**: none under `datastorekit/tests/`, 3 under `datastorekit/tools/` | 25 |
| SHA-256 | `63b3ebef0c567ae8f7924121846e738875eda8d025897ccddaa596db8e070a39` | `0ed5d04cc14474fbd0adcaa3d2f8f4d877622631eab5dcb5792baae34aac5eb0` |
| `RECORD` SHA-256 | `d22f7935599a858f7f65feb945a8948c69dd4860dbe5c758342d8a5c5dce2144` | `bbc538a64c5f90835c521903f3f61b9bf8cfebf1e34571b50de2bc83b42397e5` (`factory-defaults` log 02's release, §5.3) |
| `WHEEL` | `Generator: setuptools (84.0.0)` | the same |
| `METADATA` | `Name: datastorekit`, **`Version: 0.3.0`**, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43`, `Requires-Dist: sqlalchemy<2.1,>=2.0.39` | `Version: 0.2.3`, the rest the same |

The wheel's bytes are not reproducible across builds; only its SHA-256 is mine to record. Both
sizes equal the orchestrator's.

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
datastorekit-0.3.0.dist-info/licenses/LICENSE
datastorekit-0.3.0.dist-info/METADATA
datastorekit-0.3.0.dist-info/WHEEL
datastorekit-0.3.0.dist-info/top_level.txt
datastorekit-0.3.0.dist-info/RECORD
```

**The `RECORD` comparison**, `v0.2.3`'s wheel against the release: 20 lines under `datastorekit/`
on each side, the same paths, and one differs.

```
DIFFERS datastorekit/object.py  sha256=fdnKd2nZPKgNFkhq5jAxXl997LE2mOVTXo4jHz3Dmb4,491  sha256=rYwM2_twFZ76N_8Gh2X4jbCPJO03FayWzx-k-3ekmvI,1306
same    the other 19: SQL/ClientPool.py, SQL/Datastore.py, SQL/ProfileAgent.py,
        SQL/SerialPoolBroker.py, SQL/ShardedPool.py, SQL/__init__.py, SQL/factory_base.py,
        SQL/schema.py, __init__.py, _timing.py, contract.py, defaults.py, replication.py,
        shard_paths.py, store_inventory.py, store_reader.py, tools/__init__.py,
        tools/shard_key_audit.py, tools/sharded_store.py
```

**The install.** `uv venv --offline -p /opt/local/bin/python3.13 <scratch>/venv-release`, then
`uv pip install --offline --python <scratch>/venv-release/bin/python <the wheel> "ray==2.55.1"
"sqlalchemy==2.0.46"`: "Resolved 20 packages", "Installed 20 packages", exit 0, not editable.
Python 3.13.16, SQLite 3.53.4.

**The commands.** `<scratch>/probe/release_check.sh` ran them with `python -I`, from
`<scratch>/outside`, a directory outside the repository, with `PYTHONPATH` unset. `<R>` is the
venv's `site-packages`.

```
$ python -I -c "<import the package and its 19 submodules, print each __file__>"
datastorekit <R>/datastorekit/__init__.py
datastorekit.SQL <R>/datastorekit/SQL/__init__.py
datastorekit.SQL.ClientPool <R>/datastorekit/SQL/ClientPool.py
datastorekit.SQL.Datastore <R>/datastorekit/SQL/Datastore.py
datastorekit.SQL.ProfileAgent <R>/datastorekit/SQL/ProfileAgent.py
datastorekit.SQL.SerialPoolBroker <R>/datastorekit/SQL/SerialPoolBroker.py
datastorekit.SQL.ShardedPool <R>/datastorekit/SQL/ShardedPool.py
datastorekit.SQL.factory_base <R>/datastorekit/SQL/factory_base.py
datastorekit.SQL.schema <R>/datastorekit/SQL/schema.py
datastorekit._timing <R>/datastorekit/_timing.py
datastorekit.contract <R>/datastorekit/contract.py
datastorekit.defaults <R>/datastorekit/defaults.py
datastorekit.object <R>/datastorekit/object.py
datastorekit.replication <R>/datastorekit/replication.py
datastorekit.shard_paths <R>/datastorekit/shard_paths.py
datastorekit.store_inventory <R>/datastorekit/store_inventory.py
datastorekit.store_reader <R>/datastorekit/store_reader.py
datastorekit.tools <R>/datastorekit/tools/__init__.py
datastorekit.tools.shard_key_audit <R>/datastorekit/tools/shard_key_audit.py
datastorekit.tools.sharded_store <R>/datastorekit/tools/sharded_store.py
20 modules imported
exit=0

$ python -I -c "import importlib.metadata as m; print(m.version(\"datastorekit\"))"
0.3.0
exit=0

$ python -I -c "<inspect.signature(DatastoreObject); the timestamp property, fset, fdel>"
store_id POSITIONAL_OR_KEYWORD (no default)
timestamp KEYWORD_ONLY default=None
timestamp: property fset= None fdel= None
exit=0

$ python -I -c "<DatastoreObject(3, timestamp=t), DatastoreObject(3), vars(), pickle>"
D(3, timestamp=t).timestamp is t: True
D(3).timestamp: None vars: {'_my_id': 3, '_timestamp': None}
pickle round-trip: DatastoreObject 3 True 2026-10-12 01:02:03
exit=0

$ python -I -c "<DatastoreObject(3, t)>"
TypeError: DatastoreObject.__init__() takes 2 positional arguments but 3 were given
exit=1

$ python -I -c "<o = DatastoreObject(3); o.timestamp = t>"
AttributeError: property 'timestamp' of 'DatastoreObject' object has no setter
exit=1

$ python -I -c "import datastorekit.tests"
ModuleNotFoundError: No module named 'datastorekit.tests'
exit=1

$ python -I -m datastorekit.tools.sharded_store --help
usage: python -m datastorekit.tools.sharded_store [-h] {copy,move} src dst

Copy or move a closed ShardedPool datastore under a new name.

exit=0
```

**The assertions**, `<scratch>/probe/assert_release.py <wheel> <venv python> <v0.2.3's wheel>`:

```
wheel sha256: 63b3ebef0c567ae8f7924121846e738875eda8d025897ccddaa596db8e070a39
PASS wheel name: datastorekit-0.3.0-py3-none-any.whl
PASS METADATA Version: Version: 0.3.0
PASS no entry under datastorekit/tests/: 0 of 25 entries
PASS 25 entries: 25
PASS RECORD against v0.2.3: only object.py differs: 20 and 20 lines under datastorekit/; differing: ['datastorekit/object.py']
PASS importlib.metadata.version: 0.3.0
PASS imported from site-packages: <scratch>/venv-release/lib/python3.13/site-packages/datastorekit/object.py
PASS signature: store_id POSITIONAL_OR_KEYWORD, timestamp KEYWORD_ONLY default None: [('store_id', 'POSITIONAL_OR_KEYWORD', <class 'inspect._empty'>), ('timestamp', 'KEYWORD_ONLY', None)]
PASS timestamp is a property with no setter and no deleter: property None None
PASS stamped returns t; unstamped None with vars {_my_id, _timestamp}; pickle round-trip: True 3 True; None {'_my_id': 3, '_timestamp': None}; True 3
PASS a second positional argument raises TypeError: TypeError: DatastoreObject.__init__() takes 2 positional arguments but 3 were given
PASS assigning or deleting timestamp raises AttributeError, on the base and a subclass: AttributeError: property 'timestamp' of 'DatastoreObject' object has no setter; AttributeError: property 'timestamp' of 'DatastoreObject' object has no deleter; AttributeError: property 'timestamp' of 'S' object has no setter; AttributeError: property 'timestamp' of 'S' object has no deleter
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
PASS sharded_store --help exits 0: exit=0
PASS Ray not initialised by the probes: False
RESULT: OK
```

**The release check passes.** `git status --short --ignored` shows no `build/`, `dist/` or
`*.egg-info` in the checkout (§5.8).

### 5.4 §1.1's measure, re-run (hazard 4)

`<scratch>/probe/measure_objects.py <repo> <commit>`, run with `/opt/local/bin/python3.13 -I` from
`<scratch>/outside`: it lists the commit's `.py` files with `git ls-tree -r`, outside `prompts/`,
`.prompts/`, `docs/` and `.documents/`, reads each with `git show <commit>:<path>`, parses it with
`ast` (nothing imported or run), and reports: each `from X import DatastoreObject`; any class of
that name; the classes descending from it by base name, transitively; every
`DatastoreObject.__init__(…)` call (store_id alone / with `timestamp=` by keyword / other), and
every `super().__init__(…)` in a class whose bases name `DatastoreObject`; other `__init__` calls in
a descendant passing `timestamp=`; every `def timestamp`, class-level `timestamp`/`_timestamp`, and
`.timestamp`/`._timestamp` assignment or deletion, with its class and whether it descends; the
files under `ObjectFactories/` passing `timestamp=`; `vars(` calls and `__dict__` reads; and the
`datastorekit` line of `requirements.txt`.

```
== StochasticInstantons at 7bb3efd
python files parsed: 195
DatastoreObject imported from: {'.object': 1, 'Datastore': 12, 'Datastore.object': 6}
own class DatastoreObject: ['Datastore/object.py:20']
descendants (by name): 34 classes, 34 names
DatastoreObject.__init__ calls: 23: {'store_id alone': 9, 'with timestamp=': 14}
super().__init__ in a class whose bases name DatastoreObject: 0: {}
__init__ calls passing timestamp= in deeper descendants: 10
  CosmologyConcepts/FieldValues.py:26 (phi_value)
  CosmologyConcepts/FieldValues.py:33 (pi_value)
  InflationConcepts/DiffusionModel/__init__.py:76 (MasslessDecoupledDiffusion)
  InflationConcepts/N_final.py:17 (N_final)
  InflationConcepts/N_init.py:17 (N_init)
  InflationConcepts/QuadraticPotential.py:20 (QuadraticPotential)
  InflationConcepts/QuarticPotential.py:20 (QuarticPotential)
  InflationConcepts/delta_Nstar.py:22 (delta_Nstar)
  InflationConcepts/inflaton_mass.py:15 (inflaton_mass)
  InflationConcepts/quartic_coupling.py:14 (quartic_coupling)
timestamp defined or assigned: 19 sites; on a descendant (DatastoreObject itself excluded): 0
  Datastore/object.py:30 self._timestamp = in class DatastoreObject -> OWN DatastoreObject
  Datastore/object.py:44 def timestamp in class DatastoreObject -> OWN DatastoreObject
  plotting/adapters/base.py:84 def timestamp in class InstantonAdapter -> not a descendant
  plotting/adapters/full.py:60 def timestamp in class FullInstantonAdapter -> not a descendant
  plotting/adapters/gradient.py:132 def timestamp in class GradientCoupledAdapter -> not a descendant
  plotting/adapters/slow_roll.py:65 def timestamp in class SlowRollInstantonAdapter -> not a descendant
  tests/test_plot_adapters_golden.py:141 self.timestamp = in class _FullInstantonStub -> not a descendant
  tests/test_plot_adapters_golden.py:186 self.timestamp = in class _SlowRollInstantonStub -> not a descendant
  tests/test_plot_adapters_golden.py:870 def timestamp in class _FakeThirdAdapter -> not a descendant
  tests/test_plot_diagnostics_figures.py:75 self.timestamp = in class _FullInstantonStub -> not a descendant
  tests/test_plot_diagnostics_figures.py:91 self.timestamp = in class _SlowRollInstantonStub -> not a descendant
  tests/test_plot_diagnostics_figures.py:119 self.timestamp = in class _GCIStub -> not a descendant
  tests/test_plot_gradient_adapter.py:152 self.timestamp = in class _GCIStub -> not a descendant
  tests/test_plot_gradient_adapter.py:584 self.timestamp = in class _FullInstantonStub -> not a descendant
  tests/test_plot_gradient_adapter.py:612 self.timestamp = in class _SlowRollInstantonStub -> not a descendant
  tests/test_plot_gradient_coupled_driver.py:210 self.timestamp = in class _GCIStub -> not a descendant
  tests/test_plot_gradient_coupled_driver.py:246 self.timestamp = in class _HomogeneousStub -> not a descendant
  tests/test_plot_spatial_figures.py:118 self.timestamp = in class _GCIStub -> not a descendant
  tests/test_plot_spatial_movies.py:127 self.timestamp = in class _GCIStub -> not a descendant
factory modules (under ObjectFactories/) passing timestamp=: 18
vars( / __dict__ sites: 0
datastorekit pin: none
== SecondaryGWKit at d03a643
python files parsed: 222
DatastoreObject imported from: {'datastorekit': 19}
own class DatastoreObject: none
descendants (by name): 30 classes, 30 names
DatastoreObject.__init__ calls: 38: {'store_id alone': 38}
super().__init__ in a class whose bases name DatastoreObject: 0: {}
__init__ calls passing timestamp= in deeper descendants: 0
timestamp defined or assigned: 0 sites; on a descendant (DatastoreObject itself excluded): 0
factory modules (under ObjectFactories/) passing timestamp=: 0
vars( / __dict__ sites: 2
  ComputeTargets/tests/test_cosmology_representation_key.py:218 LambdaCDM_GenericEOS.__dict__ in TestTheDeclaration
  ComputeTargets/tests/test_cosmology_representation_key.py:221 QCD_Cosmology.__dict__ in TestTheDeclaration
datastorekit pin: ['requirements.txt:17: datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.2']
== SecondaryGWKit at e3a7077
python files parsed: 222
DatastoreObject imported from: {'datastorekit': 19}
own class DatastoreObject: none
descendants (by name): 30 classes, 30 names
DatastoreObject.__init__ calls: 38: {'store_id alone': 38}
super().__init__ in a class whose bases name DatastoreObject: 0: {}
__init__ calls passing timestamp= in deeper descendants: 0
timestamp defined or assigned: 0 sites; on a descendant (DatastoreObject itself excluded): 0
factory modules (under ObjectFactories/) passing timestamp=: 0
vars( / __dict__ sites: 2
  ComputeTargets/tests/test_cosmology_representation_key.py:218 LambdaCDM_GenericEOS.__dict__ in TestTheDeclaration
  ComputeTargets/tests/test_cosmology_representation_key.py:221 QCD_Cosmology.__dict__ in TestTheDeclaration
datastorekit pin: ['requirements.txt:17: datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.2']
== ChamPBH at 64ef9aa
python files parsed: 151
DatastoreObject imported from: {'.object': 1, 'Datastore': 13}
own class DatastoreObject: ['Datastore/object.py:19']
descendants (by name): 31 classes, 31 names
DatastoreObject.__init__ calls: 19: {'store_id alone': 19}
super().__init__ in a class whose bases name DatastoreObject: 0: {}
__init__ calls passing timestamp= in deeper descendants: 0
timestamp defined or assigned: 0 sites; on a descendant (DatastoreObject itself excluded): 0
factory modules (under ObjectFactories/) passing timestamp=: 0
vars( / __dict__ sites: 1
  Datastore/tests/test_compare_stores.py:735 vars(...) in None
datastorekit pin: none
== ChamPBH at cb0c675
python files parsed: 149
DatastoreObject imported from: {'.object': 1, 'Datastore': 13}
own class DatastoreObject: ['Datastore/object.py:19']
descendants (by name): 31 classes, 31 names
DatastoreObject.__init__ calls: 19: {'store_id alone': 19}
super().__init__ in a class whose bases name DatastoreObject: 0: {}
__init__ calls passing timestamp= in deeper descendants: 0
timestamp defined or assigned: 0 sites; on a descendant (DatastoreObject itself excluded): 0
factory modules (under ObjectFactories/) passing timestamp=: 0
vars( / __dict__ sites: 1
  Datastore/tests/test_compare_stores.py:735 vars(...) in None
datastorekit pin: none
== ChamPBH at 0f1c25b
python files parsed: 149
DatastoreObject imported from: {'.object': 1, 'Datastore': 13}
own class DatastoreObject: ['Datastore/object.py:19']
descendants (by name): 31 classes, 31 names
DatastoreObject.__init__ calls: 19: {'store_id alone': 19}
super().__init__ in a class whose bases name DatastoreObject: 0: {}
__init__ calls passing timestamp= in deeper descendants: 0
timestamp defined or assigned: 0 sites; on a descendant (DatastoreObject itself excluded): 0
factory modules (under ObjectFactories/) passing timestamp=: 0
vars( / __dict__ sites: 1
  Datastore/tests/test_compare_stores.py:735 vars(...) in None
datastorekit pin: none
== SecondaryGWKit at cf978c6
python files parsed: 222
DatastoreObject imported from: {'datastorekit': 19}
own class DatastoreObject: none
descendants (by name): 30 classes, 30 names
DatastoreObject.__init__ calls: 38: {'store_id alone': 38}
super().__init__ in a class whose bases name DatastoreObject: 0: {}
__init__ calls passing timestamp= in deeper descendants: 0
timestamp defined or assigned: 0 sites; on a descendant (DatastoreObject itself excluded): 0
factory modules (under ObjectFactories/) passing timestamp=: 0
vars( / __dict__ sites: 2
  ComputeTargets/tests/test_cosmology_representation_key.py:218 LambdaCDM_GenericEOS.__dict__ in TestTheDeclaration
  ComputeTargets/tests/test_cosmology_representation_key.py:221 QCD_Cosmology.__dict__ in TestTheDeclaration
datastorekit pin: ['requirements.txt:17: datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.2']
```

**It reproduces §1.1's table exactly**, at every commit read: SI `7bb3efd`; SGK `d03a643`,
`e3a7077` and `cf978c6`; CPBH `64ef9aa`, `cb0c675` and `0f1c25b`. No SGK or CPBH call passes
anything but `store_id`, and no descendant defines or assigns `timestamp`. No stop.

**The rest of §1.1**, read by `git`: SI's five `.timestamp` reads (`plotting/adapters/full.py:61`,
`gradient.py:133`, `slow_roll.py:66`, `plotting/provenance.py:41`, `plotting/figures/spatial.py:259`)
are as item 2 lists them; CPBH's `Datastore/object.py` at `0f1c25b` takes `store_id` alone; SGK's
`Datastore/object.py` at `6f7f291` takes `store_id` alone; SI's at `3e56d39` has no `timestamp`, and
at `51b04f8` takes one (correction 5); the pickle grep of §2 item 10.

### 5.5 Names and links (hazard 2)

**The method.** `<scratch>/probe/check_links.py`, a scratch script never committed (`factory-defaults`
02's, with this prompt's client commits), over `README.md`, `PROVENANCE.md`, the four adoption files
and the extraction board's §2:
- **Links.** Each relative Markdown link outside a code fence is resolved: the file relative to the
  document, then the anchor among the target's headings, outside code fences, by GitHub's rule
  (§3 item 2).
- **Paths in the added lines** (`git diff -U0 HEAD`): each backticked path, with any `:a-b`, is
  checked in this tree if it is this repository's, or at the client commit the text names through
  `git show` (SGK `cf978c6`, `e3a7077`, `d03a643`, `6f7f291`; CPBH `0f1c25b`, `52142d7`; SI
  `7bb3efd`).
- **Names.** `<scratch>/probe/import_names.py` imports in `venv/`, from `<scratch>/outside`, every
  `datastorekit` name the README, `PROVENANCE.md` and the new addenda mention.

**The output** (the full reports are `<scratch>/out/check-links.txt` and
`<scratch>/out/import-names.txt`):
- **128 relative links, every one resolved**, among them `docs/client-contract.md#96-object-timestamp-prompt-01`
  (README `:18`, `:136`) and `../client-contract.md#96-object-timestamp-prompt-01` (each addendum),
  heading `docs/client-contract.md:357`; `#addendum-v030-object-timestamp-prompt-02-2026-10-12` from
  each file's italic line, from the README's addendum to each checklist's, and from each checklist's
  to the README's; the two gate rows' links to their checklists' new anchors; every existing link.
- **Paths: 203 checked, 0 skipped, 1 flagged.** The flagged one is SI's `:84-86` in the row for
  `:86-87`, which the script's approximate rule for a bare `:a-b` (the last path named on the line)
  gives to `datastorekit/object.py`, quoted in that row's statement; it is this file's `:84-86`,
  the sentence that SI's own `DatastoreObject` takes `timestamp`, checked by hand
  (`<scratch>/probe/print_cites.py`, which printed every own-file line each new table cites, read
  against the statement it quotes).
- **17 names, every one importable in `venv/`:** `datastorekit.DatastoreObject`,
  `datastorekit.object.DatastoreObject` and its `timestamp`, `store_id` and `available`;
  `datastorekit.SQL.ShardedPool`; `datastorekit.SQL.factory_base.SQLAFactoryBase`;
  `datastorekit.store_inventory`; `datastorekit.contract`, `.VERSION_SERIAL_KEY` and
  `.require_version_serial`; `datastorekit.tools.sharded_store` and `.shard_key_audit`;
  `datastorekit.tests.test_object_timestamp`, `datastorekit.tests.client.stamped`,
  `datastorekit.tests.test_declared_facts.TestTheVersionObject`,
  `datastorekit.tests.client.registry`. `inspect.signature(DatastoreObject)` is `(store_id:
  Optional[int], *, timestamp: Optional[datetime.datetime] = None)`. `ray.is_initialized()` was
  `False` after.
- **The contract row** the addenda name exists: §9.6's one row, "`DatastoreObject.timestamp`"
  (`docs/client-contract.md:367`), and §9.6's preamble says a client passing `store_id` alone meets
  nothing new but `_timestamp` in `vars()`.
- **The `v0.3.0` line citations**, read at the tree: `datastorekit/object.py:10-14` is `__init__`,
  `:14` the assignment, `:27-38` the property.

### 5.6 What changed since `v0.2.3` (§1.1, re-checked)

`git diff --numstat 0de2b16 1b2f91a -- datastorekit`: `object.py` 18/1, `tests/client/stamped.py`
101/0, `tests/test_declared_facts.py` 6/1, `tests/test_object_timestamp.py` 257/0. `git diff
--quiet 1b2f91a HEAD -- datastorekit docs` held at the start.

### 5.7 The documents (§4.4)

Every remaining `v0.2.3`, by line, with why it stays:

| File | Lines | Why it stays |
|---|---|---|
| `README.md` | `:20` | history: the `v0.2.3` status paragraph |
| | `:96` | the "remain tagged" sentence |
| | `:97` | CPBH's permitted pin (U6) |
| | `:133` | history: "the change of `v0.2.3`", in the extended item |
| `PROVENANCE.md` | `:205` | history: the `factory-defaults` section's heading |
| `docs/adoption/README.md` | `:18` | the `v0.2.3` italic line, superseded (`:17-20`) |
| | `:24` | this prompt's italic line |
| | `:377`–`:475` | the `v0.2.3` addendum: the statements tabled in §4.1 superseded, the rest history true of `v0.2.3` |
| | `:482`–`:593` | this addendum's own text and table (CPBH's and SGK's permitted pins among them) |
| `docs/adoption/secondarygwkit.md` | `:28`, `:29` | the `v0.2.3` italic line, superseded |
| | `:34`–`:36` | this prompt's italic line (SGK's permitted pins) |
| | `:549`–`:630` | the `v0.2.3` addendum: superseded as tabled in §4.2, or history true of `v0.2.3` |
| | `:638`–`:718` | this addendum's own text and table |
| `docs/adoption/champbh.md` | `:29`, `:30` | the `v0.2.3` italic line, superseded |
| | `:35`–`:38` | this prompt's italic line (CPBH's permitted pin) |
| | `:538`–`:618` | the `v0.2.3` addendum: superseded as tabled in §4.3, or history |
| | `:625`–`:700` | this addendum's own text and table |
| `docs/adoption/stochasticinstantons.md` | `:27`, `:28` | the `v0.2.3` italic line, superseded |
| | `:33`–`:35` | this prompt's italic line |
| | `:507`–`:583` | the `v0.2.3` addendum: superseded as tabled in §4.4, or history |
| | `:590`–`:675` | this addendum's own text and table |

**The shifts (correction 6), checked line by line** by `<scratch>/probe/check_shift.py`: for each
own-file citation of the `v0.2.1` addenda (read at `33778b0`), the `v0.2.2` addenda (at `6d8ee9a`)
and the `v0.2.3` addenda (at `0de2b16`), every line of the range, mapped through each later head
insert, equals this tree's line: 222 lines in the four files, 0 differ. The shifts used are 2k + N,
k + N and N, or 0 for exactly the citations above the insert that §1.4 names.

`git diff -- docs/adoption` has no `-` line (hazard 1). `docs/client-contract.md` and
`docs/extraction-verification.md` are unchanged (`git diff --quiet`).

### 5.8 The tree and the clients (§4.6)

- `git status --short --ignored` before staging shows the eleven files of §7's list that this prompt
  changes as modified, this log as new, and dispatch's ignored entries: `.idea/`, `venv/`, and five
  `__pycache__/` directories. There is no `build/`, `dist/` or `*.egg-info`.
- `git diff --quiet` holds for `datastorekit/`, `docs/client-contract.md`,
  `docs/extraction-verification.md`, `docs/extraction/`, `.github/`, `CLAUDE.md`, `LICENSE` and
  `.gitignore`. On the extraction board only `:1538-1539` changed.
- The tags are `v0.1.0`, `v0.2.0`, `v0.2.1`, `v0.2.2` and `v0.2.3`; `origin/main` is `75c237e`, as
  at dispatch.

The clients, read only through `git rev-parse`, `git status`, `git ls-tree`, `git show`, `git grep`,
`git log` and `git diff --stat` between two of their commits:

| Client | At the start | At the end | `git status --short` |
|---|---|---|---|
| SGK | `e3a7077`, branch `handover-remedial` | `cf978c6`, the same branch | empty at the start and at the end |
| CPBH | `0f1c25b`, branch `dk-and-rpk-migration` (dispatch read `cb0c675`) | `0f1c25b`, unchanged | 23 untracked entries, the same at the end (`cmp` silent) |
| SI | `7bb3efd`, `main` | `7bb3efd`, unchanged | 3 entries (` M .documents/OPEN-ISSUES.md`, ` M .prompts/INDEX.md`, `?? .prompts/dk-and-rpk-migration/`), the same at the end |

SGK's and CPBH's `HEAD`s moved by other sessions' commits (§2 item 4); SI is unchanged.

---

## 6. The deliberate-breakage record (§4.5)

**The method.**
1. Each diff below was made with `diff -u` of `pyproject.toml` before and after the one change,
   labelled `a/` and `b/`, and is recorded exactly as applied (`<scratch>/breaks/`).
2. Each has its own export: `git archive 2337dff` (whose `pyproject.toml` is this commit's) into
   `<scratch>/exports/break-a` and `break-b`, and `git archive v0.2.3` into `break-c`.
3. In each export, `git apply --check` passed on the clean export, `git apply` applied it, and
   `git apply -R --check` passed on the applied one.
4. Each was built with `uv build --offline --wheel`, installed offline into its own Python 3.13.16
   venv with `ray==2.55.1` and `sqlalchemy==2.0.46`, and checked from `<scratch>/outside` with
   `assert_release.py` against `v0.2.3`'s wheel, and with `release_check.sh`.

None is committed.

**(a) `pyproject.toml`'s version left at `0.2.3`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -4,7 +4,7 @@
 
 [project]
 name = "datastorekit"
-version = "0.3.0"
+version = "0.2.3"
 description = "A sharded SQLite datastore layer (Datastore / ShardedPool) on Ray and SQLAlchemy"
 requires-python = ">=3.12"
 dependencies = [
```

The wheel is `datastorekit-0.2.3-py3-none-any.whl`, 99,491 bytes, 25 entries, none under `tests/`,
`METADATA` `Version: 0.2.3`.

```
wheel sha256: 5f11d0f69a0c58dca48b013df7615af7465ddf49c70291de0c7584f4d90ea86c
FAIL wheel name: datastorekit-0.2.3-py3-none-any.whl
FAIL METADATA Version: Version: 0.2.3
PASS no entry under datastorekit/tests/: 0 of 25 entries
PASS 25 entries: 25
PASS RECORD against v0.2.3: only object.py differs: 20 and 20 lines under datastorekit/; differing: ['datastorekit/object.py']
FAIL importlib.metadata.version: 0.2.3
PASS imported from site-packages: <scratch>/venv-break-a/lib/python3.13/site-packages/datastorekit/object.py
PASS signature: store_id POSITIONAL_OR_KEYWORD, timestamp KEYWORD_ONLY default None: [('store_id', 'POSITIONAL_OR_KEYWORD', <class 'inspect._empty'>), ('timestamp', 'KEYWORD_ONLY', None)]
PASS timestamp is a property with no setter and no deleter: property None None
PASS stamped returns t; unstamped None with vars {_my_id, _timestamp}; pickle round-trip: True 3 True; None {'_my_id': 3, '_timestamp': None}; True 3
PASS a second positional argument raises TypeError: TypeError: DatastoreObject.__init__() takes 2 positional arguments but 3 were given
PASS assigning or deleting timestamp raises AttributeError, on the base and a subclass: AttributeError: property 'timestamp' of 'DatastoreObject' object has no setter; AttributeError: property 'timestamp' of 'DatastoreObject' object has no deleter; AttributeError: property 'timestamp' of 'S' object has no setter; AttributeError: property 'timestamp' of 'S' object has no deleter
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
PASS sharded_store --help exits 0: exit=0
PASS Ray not initialised by the probes: False
RESULT: FAILED (3): wheel name, METADATA Version, importlib.metadata.version
```

**Verdict:** the `METADATA` and `importlib.metadata.version` assertions fail, naming `0.2.3`, as
§4.5 says; the wheel's name fails with them. The change is in the wheel (the `RECORD` differs from
`v0.2.3`'s in `object.py`, and the object behaves as the release's): only the version is wrong.

**(b) The `exclude` line removed from `pyproject.toml`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -14,4 +14,3 @@
 
 [tool.setuptools.packages.find]
 include = ["datastorekit*"]
-exclude = ["datastorekit.tests", "datastorekit.tests.*"]
```

The wheel is `datastorekit-0.3.0-py3-none-any.whl`, 319,775 bytes, **76 entries, 51 under
`datastorekit/tests/`** (`datastorekit/tests/__init__.py`, `client/stamped.py`,
`test_object_timestamp.py`, …).

```
wheel sha256: 33f35d3c4b8e2028b1748dd5dc9a9efb50173956e5edd457981966ca028c9a62
PASS wheel name: datastorekit-0.3.0-py3-none-any.whl
PASS METADATA Version: Version: 0.3.0
FAIL no entry under datastorekit/tests/: 51 of 76 entries
FAIL 25 entries: 76
FAIL RECORD against v0.2.3: only object.py differs: 20 and 71 lines under datastorekit/; differing: ['datastorekit/object.py', 'datastorekit/tests/__init__.py', … 51 paths under datastorekit/tests/]
PASS importlib.metadata.version: 0.3.0
PASS imported from site-packages: <scratch>/venv-break-b/lib/python3.13/site-packages/datastorekit/object.py
PASS signature: store_id POSITIONAL_OR_KEYWORD, timestamp KEYWORD_ONLY default None: [('store_id', 'POSITIONAL_OR_KEYWORD', <class 'inspect._empty'>), ('timestamp', 'KEYWORD_ONLY', None)]
PASS timestamp is a property with no setter and no deleter: property None None
PASS stamped returns t; unstamped None with vars {_my_id, _timestamp}; pickle round-trip: True 3 True; None {'_my_id': 3, '_timestamp': None}; True 3
PASS a second positional argument raises TypeError: TypeError: DatastoreObject.__init__() takes 2 positional arguments but 3 were given
PASS assigning or deleting timestamp raises AttributeError, on the base and a subclass: AttributeError: property 'timestamp' of 'DatastoreObject' object has no setter; AttributeError: property 'timestamp' of 'DatastoreObject' object has no deleter; AttributeError: property 'timestamp' of 'S' object has no setter; AttributeError: property 'timestamp' of 'S' object has no deleter
FAIL import datastorekit.tests fails: exit=0 (no error)
PASS sharded_store --help exits 0: exit=0
PASS Ray not initialised by the probes: False
RESULT: FAILED (4): no entry under datastorekit/tests/, 25 entries, RECORD against v0.2.3: only object.py differs, import datastorekit.tests fails
```

**Verdict:** the wheel lists files under `datastorekit/tests/`, and `import datastorekit.tests`
succeeds. The counts are the orchestrator's: 76 entries, 51 under `tests/`.

**(c) The wheel built from `git archive v0.2.3` with only its version set to `0.3.0`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -4,7 +4,7 @@
 
 [project]
 name = "datastorekit"
-version = "0.2.3"
+version = "0.3.0"
 description = "A sharded SQLite datastore layer (Datastore / ShardedPool) on Ray and SQLAlchemy"
 requires-python = ">=3.12"
 dependencies = [
```

Applied to an export of `v0.2.3`, where `git apply --check` and `-R --check` pass as recorded. The
wheel is `datastorekit-0.3.0-py3-none-any.whl`, 99,182 bytes, 25 entries, none under `tests/`,
`METADATA` `Version: 0.3.0`.

```
wheel sha256: 2457b58cb821034c2b7404c50f586ceb76a9ca16ffcc6a4027e655505a6e6ce6
PASS wheel name: datastorekit-0.3.0-py3-none-any.whl
PASS METADATA Version: Version: 0.3.0
PASS no entry under datastorekit/tests/: 0 of 25 entries
PASS 25 entries: 25
FAIL RECORD against v0.2.3: only object.py differs: 20 and 20 lines under datastorekit/; differing: none
PASS importlib.metadata.version: 0.3.0
PASS imported from site-packages: <scratch>/venv-break-c/lib/python3.13/site-packages/datastorekit/object.py
FAIL signature: store_id POSITIONAL_OR_KEYWORD, timestamp KEYWORD_ONLY default None: [('store_id', 'POSITIONAL_OR_KEYWORD', <class 'inspect._empty'>)]
FAIL timestamp is a property with no setter and no deleter: AttributeError: 'NoneType' object has no attribute 'fset'
FAIL stamped returns t; unstamped None with vars {_my_id, _timestamp}; pickle round-trip: TypeError: DatastoreObject.__init__() got an unexpected keyword argument 'timestamp'
PASS a second positional argument raises TypeError: TypeError: DatastoreObject.__init__() takes 2 positional arguments but 3 were given
FAIL assigning or deleting timestamp raises AttributeError, on the base and a subclass: assigned; deleted; assigned; deleted
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
PASS sharded_store --help exits 0: exit=0
PASS Ray not initialised by the probes: False
RESULT: FAILED (5): RECORD against v0.2.3: only object.py differs, signature: store_id POSITIONAL_OR_KEYWORD, timestamp KEYWORD_ONLY default None, timestamp is a property with no setter and no deleter, stamped returns t; unstamped None with vars {_my_id, _timestamp}; pickle round-trip, assigning or deleting timestamp raises AttributeError, on the base and a subclass
```

The release check's commands at (c):

```
$ python -I -c "<inspect.signature(DatastoreObject); the timestamp property, fset, fdel>"
store_id POSITIONAL_OR_KEYWORD (no default)
timestamp: absent fset= - fdel= -
exit=0

$ python -I -c "<DatastoreObject(3, timestamp=t), DatastoreObject(3), vars(), pickle>"
Traceback (most recent call last):
  File "<string>", line 5, in <module>
    a = D(3, timestamp=t)
TypeError: DatastoreObject.__init__() got an unexpected keyword argument 'timestamp'
exit=1

$ python -I -c "<DatastoreObject(3, t)>"
TypeError: DatastoreObject.__init__() takes 2 positional arguments but 3 were given
exit=1

$ python -I -c "<o = DatastoreObject(3); o.timestamp = t>"
exit=0

$ python -I -c "import datastorekit.tests"
ModuleNotFoundError: No module named 'datastorekit.tests'
exit=1

$ python -I -m datastorekit.tools.sharded_store --help
usage: python -m datastorekit.tools.sharded_store [-h] {copy,move} src dst

Copy or move a closed ShardedPool datastore under a new name.

exit=0
```

**Verdict:** `METADATA` says `0.3.0`, but the `RECORD` comparison shows no line differing where the
release shows `object.py`'s, `inspect.signature(DatastoreObject)` has `store_id` alone, there is no
`timestamp` property, `DatastoreObject(3, timestamp=t)` raises `TypeError: DatastoreObject.__init__()
got an unexpected keyword argument 'timestamp'`, and assigning or deleting `timestamp` succeeds. The
check catches a version number with no change behind it.

---

## 7. Observations not acted on

1. **The earlier addenda's own tables now point N, k + N or 2k + N lines early** in this tree
   (correction 6). That is the reason for each `v0.3.0` addendum's paragraph and its rows for the
   rule. They are not rewritten (rule 6), and no issue is needed: the reader is told how to read
   them. Each release adds one more layer of this; a fifth addendum would add a fourth shift.
2. **SGK's and CPBH's `HEAD`s move while the campaign works** (§2 item 4). The addenda name the
   commits read; a reader at a later commit re-measures, as each checklist's head says.
3. **Several table rows in the new addenda, in the gates and in this log run past 100 columns**, as
   the earlier addenda's and the board's rows do, and two prose lines of the README addendum by
   one column. None is a defect.
4. **`check_links.py`'s rule for a bare `:a-b`** is approximate (§5.5); the one it misread was
   checked by hand. Not a defect of the documents.
5. **The scratch tools** are in `<scratch>/probe/`, not in the repository: `insert.py`,
   `measure_objects.py`, `print_cites.py`, `check_shift.py`, `wheel_info.py`, `assert_release.py`,
   `release_check.sh`, `check_links.py` and `import_names.py`. Their outputs are in `<scratch>/out/`;
   the exports, wheels, venvs, diffs and inserted texts are under `<scratch>`.

---

## 8. Issues

- **Opened:** none. **Closed:** none. **Narrowed:** none.
- This board's §3 holds no issue. The index is at **4 open**, all on `inherited-issues`' board.

---

## 9. State handed to the next prompt

- `HEAD` is this commit, unpushed and untagged. The tree is clean apart from dispatch's ignored
  entries. `venv/` has `datastorekit 0.3.0` installed editable from this checkout, its `egg-info`
  removed.
- **Not pushed, not tagged.** `origin/main` is `75c237e`, and the tags are `v0.1.0`, `v0.2.0`,
  `v0.2.1`, `v0.2.2` and `v0.2.3`.
- **After the review**, this commit is pushed as `main`, fast-forwarding over `778c95a`, `b56fdde`
  and the review. `v0.3.0` is made on this commit, annotated, only once CI passes there at both ends
  (U23, U28). If CI fails, a fix prompt lands first, and no tag is made on a commit whose CI is red.
- **The suite is 509** in `venv/` and at the high end (0 `ResourceWarning` lines at each).
  `compare_ported_tests.py`: 20 modules and one test declared not ported, exit 0. `black --check
  datastorekit docs`: 76 files.
- **For the campaign's close:** every `v0.3.0` addendum's `datastorekit/` citation is at
  `1b2f91a`'s tree, which `v0.3.0` will name. G3 and G4 stay on the extraction board, recorded when
  each holds. The tag object and commit go to the user for SI's prompt 08, with README §0.2's four
  points and the sixth `def timestamp` (`tests/test_plot_adapters_golden.py:870`, not a
  `DatastoreObject`).
- **Scratch** (not in the repository): `<scratch>`, holding `exports/` (`head-before`, `release`,
  `v023`, `high`, `break-a`, `break-b`, `break-c`), `wheels/`, the venvs (`venv-high-before`,
  `venv-high`, `venv-release`, `venv-break-a`, `-b`, `-c`), `breaks/` (the three diffs),
  `addenda/` (the inserted texts), `probe/` and `out/`.
