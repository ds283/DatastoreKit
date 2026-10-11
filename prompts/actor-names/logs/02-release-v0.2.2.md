# Log 02 — release `v0.2.2`

**Subject:** Make the package ready to be released as v0.2.2 · **Commit:** this commit ·
**Date:** 2026-10-11 · **Model:** Claude Opus 5.5 · **Result:** landed; unpushed and untagged.

The package is ready to be released as **`v0.2.2`** (U3), the release every client adopts in
place of `v0.2.1`. `pyproject.toml` says `0.2.2`, and nothing else in it changed. `README.md` has a
`v0.2.2` status paragraph, the `v0.2.2` pin, and the "What changed after `v0.2.0`" item extended.
`PROVENANCE.md` has a section for `actor-names` 01 and 01b. Each of the four files under
`docs/adoption/` has an italic line at its head and a dated section, "Addendum: v0.2.2
(actor-names prompt 02, 2026-10-11)". Each section gives the new pin, says what changed for that
client since `v0.2.1`, names by `path:line` every statement it supersedes, and says by how many
lines its italic line moves the `v0.2.1` addendum's citations (correction 2). `git diff` of the
four files has no `-` line. The extraction board's G2–G4 now read `v0.2.2`, each with a dated line
saying the tag waits for CI.

**No line of code changed.** Nothing under `datastorekit/` is touched. The suite stays at **494**:
in `venv/` before and after (`pip show datastorekit` gives `0.2.2` after the offline reinstall),
and at the high end before and after, with 0 `ResourceWarning` lines at every run. A wheel built
offline from an export of the tree is `datastorekit-0.2.2-py3-none-any.whl`, with 25 entries and
none under `datastorekit/tests/`. Against `v0.2.1`'s wheel, of the 20 `RECORD` lines under
`datastorekit/` only `SQL/ShardedPool.py`'s differs. Installed at the high pins and run from
outside the repository, it behaves as the prompt's §1.2 says. Breakage (a) fails the release check
on `0.2.1`, (b) on the test package, and (c), `v0.2.1`'s tree at `0.2.2`, on a `RECORD` with no
line changed and on the missing `_kill_actors` and `_ray_is_running`. §1.1's measure of the clients,
re-run, reproduces line for line.

**No tag was made and nothing was pushed.** Nothing was downloaded: every venv, install and build
is `uv … --offline`. No client was written, run, imported or opened. Ray was never started. No
issue was opened, and the index stays at **4**.

Prompt: [`../02-release-v0.2.2.md`](../02-release-v0.2.2.md), with the orchestrator's dispatch note
§0: three corrections, its additions, its checked facts and its conventions. §2 classifies each.
Line numbers under `datastorekit/` are `v0.2.2`'s tree (`f024fc6`'s `datastorekit/`, which this
commit does not change) unless another tree is named.

`<scratch>` below is `<session scratchpad>/agent02`, outside the repository.

---

## 1. What shipped

### 1.1 `pyproject.toml` (§2.1)

`version = "0.2.1"` → `version = "0.2.2"` (`:7`), the only change. No other file carries the
version.

### 1.2 `README.md` (§2.2)

- **Status.** A new paragraph for **`v0.2.2`**, above `v0.2.1`'s (`:10-21`). It is a fix release
  with one fix, `actor-names` prompt 01: a closed pool, and an open that is refused, release their
  Ray actors' names at once, so a store can be reopened in one Ray session while a closed pool is
  still referenced. A closed pool's handles are dead afterwards, and a second `__exit__` does
  nothing. Two pools open at once still collide. Closing a pool never starts Ray (`actor-names`
  01b), said as "a property the release keeps, not a second fix: `v0.2.1`, which killed no actor
  on a close, never started Ray on one either". No API, nothing written, and no message, refusal or
  exception changes. It links contract §9.3 and §9.4 by their anchors.
- **Installing.** The pin is `@v0.2.2` (`:72`). The sentence at `:62-63` is replaced by one
  sentence (`:75-76`): `v0.2.1`, `v0.2.0` and `v0.1.0` remain tagged and no tag is moved or
  deleted; every client adopts `v0.2.2`, which fixes a defect that all three earlier releases
  carry. It is written as of the tag.
- **Using it.** The item at `:93-94` becomes `:106-109`: "the three fixes of `v0.2.1`, and the fix
  of `v0.2.2`, that a closed pool releases its actors' names, with the property it keeps, that
  closing a pool never starts Ray", still linking §9.
- Nothing else changed.

### 1.3 `PROVENANCE.md` (§2.3)

A new `###` section, "`actor-names` prompts 01 and 01b: a closed pool releases its actor names
(`v0.2.2`)", is added after "Prompts 08a, 08b and 09" (the file's last section), under "After
`v0.1.0`". Nothing above it changed. It says:
- **the fix has no source**: made by 01 (`ac50a8a`), closing
  `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]` (opened by extraction prompt 11,
  closed on the extraction board's §4); what the layer now does; U1; its test module (tests 1–6);
  contract §9.3;
- **SGK's frozen copies carry the defect**: SGK's names at `Datastore/SQL/ShardedPool.py:294`,
  `:305` and `:544`, at `6f7f291` and `b510bc9`; its `__exit__` kills none; "The freeze" (U3), and
  `actor-names` U3 fixing it before G2, as extraction U33 fixed three; SGK receives it by adopting
  `v0.2.2`;
- **01b's guard has no source either**: `f024fc6`, closing `[02-closing-a-pool-can-start-ray]`,
  which 01's kill introduced and no release carried (this board's §4); SGK's `__exit__` calls no
  `ray.kill`, so SGK's copies do not have that defect; tests 7 and 8; contract §9.4;
- **what changed in the package**: `SQL/ShardedPool.py` only, 64 lines added (48 + 16), none
  removed; outside the wheel the stand-in, the new module, the smoke script (by 01) and contract
  §9.3–§9.4; the suite 486 → 494;
- **the files each prompt changes, and its log** (from `git show --stat ac50a8a` and `f024fc6`,
  records excluded).

### 1.4 The addenda (§2.4, U3)

Each file gains an italic line at its head, after extraction prompt 10's, and an unnumbered
section `## Addendum: v0.2.2 (actor-names prompt 02, 2026-10-11)`, anchor
`#addendum-v022-actor-names-prompt-02-2026-10-11`:
- in the README, the italic line is `:12-15` (with a blank, five lines), and the section is at the
  end, after a `---` (`:275`, heading `:277`);
- in each checklist, the italic line is five lines and a blank, after the `v0.2.1` italic line
  (SGK `:21-25`, CPBH `:22-26`, SI `:20-24`). The section follows the `v0.2.1` addendum's table,
  with a `---` of its own above it, and comes before the `---` that precedes the appendix (SGK
  heading `:447`, CPBH `:465`, SI `:435`).

Each section gives:
- the pin `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.2`, and that the client
  adopts `v0.2.2` in place of `v0.2.1` (`actor-names` U3, amending extraction U37);
- what changed for that client, with contract §9.3's and §9.4's rows linked by anchor;
- the rule for line citations: 07a's `datastorekit/` lines are `v0.2.0`'s, the `v0.2.1`
  addendum's `v0.2.1`'s (`33778b0`), and this addendum's `v0.2.2`'s (`f024fc6`);
- a supersession table, with the one sentence correction 2 asks for beside it (k below);
- the README's addendum has a table of the four behaviours and two unchanged, each linked to its
  contract row, and §1.1's measure of the 14 constructions.

| File | Lines added | Lines removed | k (correction 2) |
|---|---|---|---|
| `docs/adoption/README.md` | 95 | 0 | **5**: every line after `:11` at `33778b0` is five lines later here |
| `docs/adoption/secondarygwkit.md` | 96 | 0 | **6**: after `:20` |
| `docs/adoption/champbh.md` | 67 | 0 | **6**: after `:21` |
| `docs/adoption/stochasticinstantons.md` | 66 | 0 | **6**: after `:19` |

The four tables are repeated in §4.

### 1.5 The extraction board's gates (§2.5)

`prompts/extraction/IMPLEMENTATION_STATE.md` §2, rows G2–G4 (`:1537-1539`), and nothing else on
that board:
- titles, exactly: G2 "SGK adopted `v0.2.2` (U37; `actor-names` U3), fingerprint reproduced"; G3
  "CPBH adopted `v0.2.2` (U37; `actor-names` U3)"; G4 "SI adopted `v0.2.2` (U37; `actor-names`
  U3)";
- each status cell gains, at its end, one dated italic sentence: "*(2026-10-11: `v0.2.2` is ready
  to be tagged on `actor-names` prompt 02's commit once CI passes there at both ends, as U23 and
  U28; 02 makes no tag and pushes nothing. <Client>'s addendum is [link to its `v0.2.2`
  anchor].)*". The lines already there are unchanged (`git diff --word-diff` shows only the title
  words and the appended sentence).

### 1.6 The records

- This log.
- This board: the header, and §1's row for 02 (landed, "this commit", log).
- This campaign's README: a sentence in its header, and §2's row for 02.
- `prompts/INDEX.md`: `actor-names`'s status.
- `docs/OPEN_ISSUES.md` is unchanged at **4**: no issue opened.

---

## 2. Deviations from the prompt

1. **Correction 1: `venv/`'s reinstall is `uv pip install --offline --no-deps --python
   venv/bin/python -e .`**, from the repository root, not hazard 6's command with
   `--no-build-isolation`, which cannot build in `venv/` (no `setuptools`; I confirmed
   `import setuptools` raises `ModuleNotFoundError` there at the start). Its output was
   `- datastorekit==0.2.1`, `+ datastorekit==0.2.2`, exit 0. `pip show datastorekit` gives
   `Version: 0.2.2`, editable from this checkout. It wrote `datastorekit.egg-info/` at the root,
   which I deleted at once; afterwards `importlib.metadata.version("datastorekit")` is `0.2.2`, the
   package imports from the source tree, and `git status --short --ignored` lists only dispatch's
   ignored entries. **STRUCTURALLY REQUIRED.**
2. **Correction 2: each `v0.2.2` addendum says how far its italic line moves the `v0.2.1`
   addendum's citations.** Beside each table, one sentence: in the file as extraction prompt 10
   left it (`33778b0`), every line after the insert point is k lines earlier, so the `v0.2.1`
   addendum's citations are read at `33778b0`, or k lines later here, all but the one above the
   insert (README `:3`, SGK `:6`, CPBH `:6`, SI `:5`). k is **5** in the README and **6** in each
   checklist (§1.4): the checklists' italic line wrapped to five lines, the README's to four. I
   checked the shift line by line: each `v0.2.1` citation at `33778b0` equals this tree's line k
   later (19 of 19, §5.7). That sentence is also a row of each table, since the `v0.2.1`
   addendum's own statement "Each `path:line` is this file's as committed with this addendum" is
   no longer true here. **STRUCTURALLY REQUIRED.**
3. **Correction 3: the `RECORD` comparison under (c) is recorded line by line.** Its facts hold as
   the prompt states them: all 20 lines under `datastorekit/` equal `v0.2.1`'s (§6). Recorded as
   found; nothing changed.
4. **The orchestrator's additions** are followed as given, each an **IMPLEMENTATION CHOICE** at
   the orchestrator's direction:
   - the order of work (baseline, `pyproject.toml` and the reinstall, the two documents, the
     addenda, the gates, the release check, (a)–(c), the documents' and link checks, the end);
   - each addendum's supersessions as a table, repeated in §4;
   - placement: the `---` rules, the README's addendum at the end, the heading and its anchor;
   - `PROVENANCE.md`'s new section as a `###`;
   - the contract anchors `#93-actor-names-prompt-01` and `#94-actor-names-prompt-01b`;
   - the gate titles exactly as given, and one dated italic sentence per row;
   - the name-and-link check as a scratch script, never committed;
   - (a), (b) and (c) each built from its own export.
5. **Statements superseded that the prompt's table does not name**, by §2.4's rule. Each is in its
   file's table (§4). **STRUCTURALLY REQUIRED.**
   - In each file, the `v0.2.1` addendum's "Each `path:line` is this file's as committed with this
     addendum" (correction 2): README `:261-263`, SGK `:430-432`, CPBH `:452-454`, SI `:422-424`.
   - In each checklist, the `v0.2.1` table's row giving the package "at `v0.2.1`, with this
     addendum" (SGK `:436`, CPBH `:458`, SI `:428`).
   - In the README, the `v0.2.1` addendum's line-citation rule (`:257-259`, and its table's
     `:273`), and its table's replacements at `v0.2.1` (`:268`, `:269`, `:270`).
   - In SGK's: "SGK's frozen copies carry the three defects, and adopting `v0.2.1` fixes them"
     (`:422-424`); the `v0.2.1` table's "three more differences, none of which changes what SGK's
     calls use" (`:440`); and its item 8 row "extended to `v0.2.1`" (`:442`).
6. **The release check has an assertion script and a `RECORD` comparer** (`<scratch>/probe/`,
   §5.3), as log 10's had the first. `assert_release.py` also asserts the `RECORD` comparison,
   `_kill_actors` and `_ray_is_running`, so that (c) is recorded as failed assertions.
   **IMPLEMENTATION CHOICE.**
7. **The exports are of the working tree before the records were written**, made with `git
   archive $(git stash create)`: commit object `210141e`, whose tree equalled the working tree
   (`git diff --quiet 210141e` held). `git stash create` writes no ref, and `git stash list`
   stayed empty. That tree differs from this commit's in two ways. First, the records (this log,
   this board, this campaign's README, `prompts/INDEX.md`). Second, three table rows added later
   to the SGK, CPBH and SI addenda (item 5's second bullet). Neither is in the wheel or read by the
   suite. `pyproject.toml` and `datastorekit/` are this commit's, so (a)'s and (b)'s diffs apply
   to an export of this commit as recorded. **IMPLEMENTATION CHOICE.**
8. **I checked the wheel's 20 `RECORD` hashes against `f024fc6`'s files**, through `git show`:
   20 of 20 equal (§5.3). Not asked. **IMPLEMENTATION CHOICE.**
9. **SI's addendum adds one fact beyond the prompt's table**: the fixture is session-scoped
   (`tests/conftest.py:36`), so it opens one pool per pytest session, as §1.1 says.
   **IMPLEMENTATION CHOICE.**

---

## 3. The hazards (§3)

1. **Additive documents.** `git diff --numstat -- docs/adoption` gives 95/0, 67/0, 96/0 and 66/0,
   and `git diff -- docs/adoption | grep '^-' | grep -v '^--- '` finds nothing. Each insertion
   was made by a scratch helper (`<scratch>/probe/insert.py`) that adds lines only, after checking
   the line before and after the insert point. The three later rows were inserted the same way
   into this prompt's own text. `git diff 33778b0 -- docs/adoption/<f>` has no removed line in any
   of the four. `docs/client-contract.md` and `docs/extraction-verification.md` are unchanged.
2. **Names and links.** Every one resolves (§5.5). The contract anchors, by GitHub's rule:
   - "9.3 `actor-names` prompt 01" (`docs/client-contract.md:301`), lower-cased, with the `.` and
     the backticks dropped and the spaces made hyphens, is `93-actor-names-prompt-01`;
   - "9.4 `actor-names` prompt 01b" (`:317`) is `94-actor-names-prompt-01b`.

   The script derives every heading's slug that way and finds each anchor among them.
3. **The tag does not exist yet.** No document says `v0.2.2` is tagged:
   - the README and the addenda state the pin, and the README says `v0.2.1`, `v0.2.0` and `v0.1.0`
     "remain tagged";
   - the gates say `v0.2.2` "is ready to be tagged … once CI passes there at both ends", and that
     02 makes no tag.
4. **No client is re-measured beyond §1.1.** I re-ran §1.1's measure (§5.4). It reproduces §1.1
   line for line, so no stop.
5. **Offline only.** Every venv (`uv venv --offline`), install (`uv pip install --offline`) and
   build (`uv build --offline`) resolved from the cache: `setuptools` (the build backend, 84.0.0),
   `ray` 2.55.1 and `sqlalchemy` 2.0.46. Nothing was downloaded.
6. **`venv/`'s metadata.** Reinstalled by correction 1's command, the `egg-info` removed; the suite
   in `venv/` gives 494 OK (§5.1).
7. **No Ray.** The smoke script was not run. The release probes import the pool's module and read
   attributes and source only. The link check imports names and reads no Ray API. At the start and
   the end no Ray process was up (`pgrep -lf 'raylet|gcs_server|ray::'`), `RAY_ADDRESS` and
   `RAY_ENABLE_AUTO_CONNECT` were unset, and there was no `/tmp/ray/ray_current_cluster`. The
   newest session under `/tmp/ray` is from 02:56 today, before this prompt's dispatch (10:53).

---

## 4. The supersession tables

Each is as committed in its addendum. Line numbers are each file's at this commit.

### 4.1 `docs/adoption/README.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `:7-10` | the `v0.2.1` addendum, "at the end", gives the pin **`v0.2.1`** | it gives `v0.2.1`'s pin and changes, true of `v0.2.1`; this addendum, now at the end, gives `v0.2.2` |
| `:213-214` | "Every client adopts **`v0.2.1`** in place of `v0.2.0`" | every client adopts `v0.2.2` in place of `v0.2.1` (`actor-names` U3) |
| `:217` | the pin `…@v0.2.1` | the pin `…@v0.2.2` |
| `:257-259` *(not in the prompt's table)* | "A `datastorekit/` line in an addendum is `v0.2.1`'s" | so in the `v0.2.1` addendum; one in this addendum is `v0.2.2`'s |
| `:261-263` *(correction 2)* | the `v0.2.1` addendum's `path:line`s are "this file's as committed with this addendum" | read at `33778b0`, or five lines later here (all but `:3`) |
| `:268` *(not in the prompt's table)* | at `v0.2.1`, "each checklist with its addendum" | at `v0.2.2`, each checklist with both its addenda |
| `:269` *(not in the prompt's table)* | "all three adopt `v0.2.1` (U37)" | all three adopt `v0.2.2` (U37; `actor-names` U3) |
| `:270` *(not in the prompt's table)* | "the pin `…@v0.2.1`, above" | the pin `…@v0.2.2`, above |
| `:271` | "G2, G3 and G4 each hold when that client has adopted `v0.2.1` (U37)" (the gate statement) | … `v0.2.2` (U37; `actor-names` U3) |
| `:273` *(not in the prompt's table)* | "a `datastorekit/` line in an addendum is at `v0.2.1`" | as `:257-259` |

### 4.2 `docs/adoption/secondarygwkit.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `:16-19` | the `v0.2.1` addendum gives the pin **`v0.2.1`** | true of `v0.2.1`; this addendum gives `v0.2.2` |
| `:375-376` | "SGK adopts **`v0.2.1`** in place of `v0.2.0`", and G2 reads "SGK has adopted `v0.2.1`" | `v0.2.2` in place of `v0.2.1` (`actor-names` U3), and G2 reads "… `v0.2.2`" |
| `:379` | the pin `…@v0.2.1` | the pin `…@v0.2.2` |
| `:422-424` *(not in the prompt's table)* | "SGK's frozen copies carry the three defects, and adopting `v0.2.1` fixes them" | adopting `v0.2.2` fixes them, and 01's defect |
| `:430-432` *(correction 2)* | the `v0.2.1` addendum's `path:line`s are "this file's as committed with this addendum" | read at `33778b0`, or six lines later here (all but `:6`) |
| `:436` *(not in the prompt's table)* | the package "at `v0.2.1`, with this addendum" | at `v0.2.2`, with both addenda |
| `:440` *(not in the prompt's table)* | at `v0.2.1`, "three more differences, none of which changes what SGK's calls use" | at `v0.2.2` also the four of §9.3, none of which changes what SGK's calls use |
| `:442` *(not in the prompt's table)* | item 8's reasoning "extended to `v0.2.1`" | extended to `v0.2.2` |
| `:443` | "G2 holds when SGK has adopted `v0.2.1` (U37)" (the gate statement) | … `v0.2.2` (U37; `actor-names` U3) |

### 4.3 `docs/adoption/champbh.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `:17-20` | the `v0.2.1` addendum gives the pin **`v0.2.1`** | true of `v0.2.1`; this addendum gives `v0.2.2` |
| `:418-419` | "CPBH adopts **`v0.2.1`** in place of `v0.2.0`", and G3 reads "CPBH has adopted `v0.2.1`" | `v0.2.2` in place of `v0.2.1`, and G3 reads "… `v0.2.2`" |
| `:422` | the pin `…@v0.2.1` | the pin `…@v0.2.2` |
| `:452-454` *(correction 2)* | "this file's as committed with this addendum" | read at `33778b0`, or six lines later here (all but `:6`) |
| `:458` *(not in the prompt's table)* | the package "at `v0.2.1`, with this addendum" | at `v0.2.2`, with both addenda |
| `:461` | "G3 holds when CPBH has adopted `v0.2.1` (U37)" (the gate statement) | … `v0.2.2` (U37; `actor-names` U3) |

### 4.4 `docs/adoption/stochasticinstantons.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `:15-18` | the `v0.2.1` addendum gives the pin **`v0.2.1`** | true of `v0.2.1`; this addendum gives `v0.2.2` |
| `:389-390` | "SI adopts **`v0.2.1`** in place of `v0.2.0`", and G4 reads "SI has adopted `v0.2.1`" | `v0.2.2` in place of `v0.2.1`, and G4 reads "… `v0.2.2`" |
| `:393` | the pin `…@v0.2.1` | the pin `…@v0.2.2` |
| `:422-424` *(correction 2)* | "this file's as committed with this addendum" | read at `33778b0`, or six lines later here (all but `:5`) |
| `:428` *(not in the prompt's table)* | the package "at `v0.2.1`, with this addendum" | at `v0.2.2`, with both addenda |
| `:431` | "G4 holds when SI has adopted `v0.2.1` (U37)" (the gate statement) | … `v0.2.2` (U37; `actor-names` U3) |

**Considered and not superseded.** I read each file for statements no longer true of `v0.2.2`.
These stay:
- **Every `datastorekit/` citation of 07a's text and of the `v0.2.1` addendum.** Each is read at
  its own tag, by the files' rules (the link check reads them there, §5.5).
- **README `:267`**, "this addendum gives `v0.2.1`", and each checklist's row for `:21-22` (or
  its kin), "a `datastorekit/` line in this addendum is at `v0.2.1`": both speak of the `v0.2.1`
  addendum, and stay true.
- **README `:232-234`**, "A store that opened under `v0.2.0` opens under `v0.2.1`", and each
  checklist's item 8 line in the `v0.2.1` addendum: still true; this addendum extends them to
  `v0.2.2`.
- **SGK's item 7** (`:264-266`, the stand-in kept) and **`:270-274`** (its `importlib` sites):
  still true; this addendum adds what `v0.2.2` means for that stand-in.
- **CPBH's `:425`**, "`v0.2.1` carries `key_on_version` … unchanged": still true; this addendum
  adds that `v0.2.2` does too.
- **SI's `:408`**, the one payload list "is safe under `v0.2.1`": still true under `v0.2.2`.
- **The adoption README's §3** (the wheel does not ship the stand-in): still true, and the release
  check confirms it.

---

## 5. Verification performed

### 5.1 The suite (§4.1)

Every run in the foreground, its output in `<scratch>/out/`, the verdict grepped from it.

| Where | When | Result | `ResourceWarning` lines | `datastorekit` |
|---|---|---|---|---|
| `venv/` (3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39) | at dispatch, before any change | `Ran 494 tests in 83.008s` `OK` | 0 | 0.2.1 |
| `<scratch>/venv-high-before` (3.13.16 / 2.55.1 / 2.0.46, SQLite 3.53.4, `setuptools`), `git archive HEAD` (`394a974`) installed editable `--no-deps --no-build-isolation` | at dispatch | `Ran 494 tests in 94.451s` `OK` | 0 | 0.2.1 |
| `venv/` | after `pyproject.toml` and the reinstall | `Ran 494 tests in 93.769s` `OK` | 0 | 0.2.2 |
| `<scratch>/venv-high`, the same pins, `git archive 210141e` installed editable `--no-deps --no-build-isolation` | after every document edit | `Ran 494 tests in 95.534s` `OK` | 0 | 0.2.2 |
| `venv/` | after every document edit | `Ran 494 tests in 89.106s` `OK` | 0 | 0.2.2 |
| `venv/` | after the records, before the commit | `Ran 494 tests in 90.462s` `OK` | 0 | 0.2.2 |

The count is **494** before and after, at both ends.

### 5.2 The checks (§4.2)

- `compare_ported_tests.py`, before and after, exit 0, its last line: `OK: 20 module(s) keep their
  source's tests, classes and assertion skeletons; 1 test(s) declared not ported`.
- `./venv/bin/black --check datastorekit docs`, before and after: `72 files would be left
  unchanged.` No `.py` file changed.
- The two guards, `test_layer_is_generic` and `test_prose_names_no_source`, run alone after the
  edits: `Ran 14 tests` `OK`. They are in the suite too.

### 5.3 The release check (§4.3)

**The build.** `git archive 210141e | tar -x -C <scratch>/exports/release` (item 7 of §2), then
`uv build --offline --wheel --out-dir <scratch>/wheels/release <scratch>/exports/release`, exit 0.
For the comparison, `git archive v0.2.1` into `<scratch>/exports/v021`, built the same way.
Nothing was built in the checkout.

| | The release | `v0.2.1`'s, for comparison |
|---|---|---|
| Wheel | `datastorekit-0.2.2-py3-none-any.whl` | `datastorekit-0.2.1-py3-none-any.whl` |
| Size | 98,811 bytes | 97,849 bytes |
| Entries | **25**: none under `datastorekit/tests/`, 3 under `datastorekit/tools/` | 25 |
| SHA-256 | `9b019a7c08a37f140fcb87654789bf7b1198a6cdd57b3c150c123e6f2c803cbc` | `634ecb02e94ac55423e71aac8ba9c5009b9eee4a0e377270747fa380969a27ab` |
| `RECORD` SHA-256 | `7dd75ce12638c7c5afb73a8d766d0393382b4a371d56632dc85d699162600376` | `f840ffa4c28f1d40f6578abb56a033d6faf4356f4877c62f60ebf75ab2d96c5e` (log 10's, §5.3) |
| `WHEEL` | `Generator: setuptools (84.0.0)` | the same |
| `METADATA` | `Name: datastorekit`, **`Version: 0.2.2`**, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43`, `Requires-Dist: sqlalchemy<2.1,>=2.0.39` | `Version: 0.2.1`, the rest the same |

The wheel's bytes are not reproducible across builds; only its SHA-256 is mine to record. The
size equals the orchestrator's.

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
datastorekit-0.2.2.dist-info/licenses/LICENSE
datastorekit-0.2.2.dist-info/METADATA
datastorekit-0.2.2.dist-info/WHEEL
datastorekit-0.2.2.dist-info/top_level.txt
datastorekit-0.2.2.dist-info/RECORD
```

**The `RECORD` comparison** (`<scratch>/probe/compare_record.py`), `v0.2.1`'s wheel against the
release: 20 lines under `datastorekit/` on each side, the same paths, and one differs.

```
DIFFERS datastorekit/SQL/ShardedPool.py  sha256=_Ij01ywRDgBlIQKVX7Elcm5…  sha256=l7kt93NSN8LrJm-NIX1Q_4J…
same    the other 19: SQL/ClientPool.py, SQL/Datastore.py, SQL/ProfileAgent.py,
        SQL/SerialPoolBroker.py, SQL/__init__.py, SQL/factory_base.py, SQL/schema.py, __init__.py,
        _timing.py, contract.py, defaults.py, object.py, replication.py, shard_paths.py,
        store_inventory.py, store_reader.py, tools/__init__.py, tools/shard_key_audit.py,
        tools/sharded_store.py
```

Each of the release's 20 `RECORD` hashes equals the hash of `f024fc6`'s file, read by `git show`
(§2 item 8).

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

$ python -I -c "import importlib.metadata as m; print(m.version(\"datastorekit\"))"
0.2.2
exit=0

$ python -I -c "<the fix: ShardedPool._kill_actors, __exit__.__doc__, _ray_is_running>"
module: <R>/datastorekit/SQL/ShardedPool.py
ShardedPool has _kill_actors: True
ShardedPool.__exit__ docstring, first line: Close the pool: every shard actor's __exit__, waited for (each disposes its engine and
module has _ray_is_running: True
_ray_is_running last line: return ray.is_initialized()
exit=0

$ python -I -c "import datastorekit.tests"
ModuleNotFoundError: No module named 'datastorekit.tests'
exit=1

$ python -I -m datastorekit.tools.sharded_store --help
exit=0
usage: python -m datastorekit.tools.sharded_store [-h] {copy,move} src dst

Copy or move a closed ShardedPool datastore under a new name.
... (34 lines)
```

The `__exit__` docstring's first line is 01's (`datastorekit/SQL/ShardedPool.py:859`).

**The assertions**, `<scratch>/probe/assert_release.py <wheel> <venv python> <v0.2.1's wheel>`:

```
PASS wheel name: datastorekit-0.2.2-py3-none-any.whl
PASS METADATA Version: Version: 0.2.2
PASS no entry under datastorekit/tests/: 0 of 25 entries
PASS 25 entries: 25
PASS RECORD against v0.2.1: only SQL/ShardedPool.py differs: 20 and 20 lines under datastorekit/; differing: ['datastorekit/SQL/ShardedPool.py']
PASS importlib.metadata.version: 0.2.2
PASS ShardedPool has _kill_actors: True
PASS module has _ray_is_running: True
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
RESULT: OK
```

**The release check passes.** `git status --short --ignored` shows no `build/`, `dist/` or
`*.egg-info` in the checkout (§5.8).

### 5.4 §1.1's measure, re-run (hazard 4)

Read through `git` only, at SGK `b510bc9`, CPBH `52142d7` and SI `7bb3efd`.

**Step 1**, `git -C <client> grep -n -E 'ShardedPool\(|\.__exit__\(|ray\.kill|ray\.get_actor'
<commit> -- '*.py' ':!Datastore/**' ':!prompts/**' ':!docs/**'`:

```
== SecondaryGWKit at b510bc9
b510bc9:ComputeTargets/tests/test_reader_read_only.py:91:    """The module-level ``with ShardedPool(...) as pool:`` block."""
b510bc9:ComputeTargets/tests/test_reader_read_only.py:104:            f"{len(found)} module-level `with ShardedPool(...)` blocks"
b510bc9:Quadrature/simple_quadrature.py:45:        super().__exit__(exc_type, exc_val, exc_tb)
b510bc9:Quadrature/supervisors/numeric.py:51:        super().__exit__(exc_type, exc_val, exc_tb)
b510bc9:extract_GkSource_data.py:932:with ShardedPool(
b510bc9:extract_GkWKB_data.py:505:with ShardedPool(
b510bc9:extract_Gk_data.py:453:with ShardedPool(
b510bc9:extract_QuadSourceIntegral_data.py:1294:with ShardedPool(
b510bc9:extract_TkWKB_data.py:493:with ShardedPool(
b510bc9:extract_tensor_source_data.py:421:with ShardedPool(
b510bc9:main.py:4164:with ShardedPool(
== ChamPBH at 52142d7
52142d7:Quadrature/simple_quadrature.py:60:        super().__exit__(exc_type, exc_val, exc_tb)
52142d7:Quadrature/supervisors/ScalarField.py:105:        super().__exit__(exc_type, exc_val, exc_tb)
52142d7:main.py:1338:with ShardedPool(
52142d7:plot_ScalarModel.py:1577:with ShardedPool(
52142d7:plot_by_beta.py:1007:with ShardedPool(
== StochasticInstantons at 7bb3efd
7bb3efd:Quadrature/simple_quadrature.py:60:        super().__exit__(exc_type, exc_val, exc_tb)
7bb3efd:main.py:1345:with ShardedPool(
7bb3efd:plot_GradientCoupledSolutions.py:974:    with ShardedPool(
7bb3efd:plot_InstantonSolutions.py:1207:    with ShardedPool(
7bb3efd:tests/conftest.py:57:    with ShardedPool(
```

**Step 2**, `<scratch>/probe/measure_step2.py`: each of the 14 files read by `git show` and parsed
with `ast` (never imported or run). For each `ShardedPool(` call it finds the `with` whose item it
is, the statements after that `with` in its block, and every later `Name` of the `as` variable in
the file:

```
SecondaryGWKit:main.py:4164: with ... as pool (with at :4164-4381); calls of ShardedPool( in file: 1; statements after it in its block: 0 []; of them naming 'pool': []; any later name 'pool' in the file: []
SecondaryGWKit:extract_GkSource_data.py:932: with ... as pool (with at :932-957); … 1; … 0 []; … []; … []
SecondaryGWKit:extract_GkWKB_data.py:505: with ... as pool (with at :505-530); … 1; … 0 []; … []; … []
SecondaryGWKit:extract_Gk_data.py:453: with ... as pool (with at :453-478); … 1; … 0 []; … []; … []
SecondaryGWKit:extract_QuadSourceIntegral_data.py:1294: with ... as pool (with at :1294-1319); … 1; … 0 []; … []; … []
SecondaryGWKit:extract_TkWKB_data.py:493: with ... as pool (with at :493-518); … 1; … 0 []; … []; … []
SecondaryGWKit:extract_tensor_source_data.py:421: with ... as pool (with at :421-446); … 1; … 0 []; … []; … []
ChamPBH:main.py:1338: with ... as pool (with at :1338-1361); … 1; … 0 []; … []; … []
ChamPBH:plot_ScalarModel.py:1577: with ... as pool (with at :1577-1704); … 1; … 0 []; … []; … []
ChamPBH:plot_by_beta.py:1007: with ... as pool (with at :1007-1146); … 1; … 0 []; … []; … []
StochasticInstantons:main.py:1345: with ... as pool (with at :1345-1365); … 1; … 0 []; … []; … []
StochasticInstantons:plot_GradientCoupledSolutions.py:974: with ... as pool (with at :974-990); … 1; … 0 []; … []; … []
StochasticInstantons:plot_InstantonSolutions.py:1207: with ... as pool (with at :1207-1225); … 1; … 0 []; … []; … []
StochasticInstantons:tests/conftest.py:57: with ... as pool (with at :57-72); calls of ShardedPool( in file: 1; statements after it in its block: 1 [('Expr', 74)]; of them naming 'pool': []; any later name 'pool' in the file: []
constructions: 14; not a with block or used after it: 0
```

(The first line is printed in full; "…" stands for the same labels in the others.)

**The rest of §1.1**, read by `git show` and `git grep`:
- SI's `tests/conftest.py`: `@pytest.fixture(scope="session")` at `:36`, `yield pool` at `:72`
  inside the block, `ray.shutdown()` at `:74` after it.
- No client file outside its layer reads `._shards` or `._broker` (`git grep -E
  '\._shards\b|\._broker\b'`, the same pathspecs): none in any of the three.
- SGK's stand-in at `b510bc9`: `sp_mod = importlib.import_module("Datastore.SQL.ShardedPool")` at
  `Datastore/tests/standin_pool.py:43`; `active()` at `:231-247`, patching `ray.get` (`:233`), the
  two actor classes and `random`; `git grep -E 'ray\.kill|_ray_is_running|is_initialized'` in that
  file finds nothing. `ComputeTargets/tests/test_quadsource_policy_main.py:430-431` is
  `def tearDownModule(): assert not ray.is_initialized()`.
- SGK's names: `Datastore/SQL/ShardedPool.py:294` (`SerialPoolBroker`), `:305` and `:544`
  (`shard{key:04d}-store`), identical at `6f7f291` and `b510bc9`. `git grep ray\.kill` over SGK's
  `Datastore/` finds nothing.

**The measure reproduces §1.1 line for line.** No stop.

### 5.5 Names and links (hazard 2)

**The method.** `<scratch>/probe/check_links.py`, a scratch script adapted from log 10's and never
committed, ran over `README.md`, `PROVENANCE.md`, the four adoption files and the extraction
board's §2 (`prompts/extraction/IMPLEMENTATION_STATE.md:1532-1541`).
- **Links.** Each relative Markdown link is resolved: the file relative to the document, then the
  anchor among the target's headings, outside code fences, by GitHub's rule (§3 item 2).
- **Paths.** Each backticked path under `datastorekit/`, `docs/`, `prompts/` or `.github/` must
  exist, with any `:a-b` suffix within the file. In an adoption file each region is read at its own
  tree:
  - 07a's text: its `datastorekit/` paths at `240028e`;
  - the `v0.2.1` addendum: every path of this repository at `33778b0`;
  - the `v0.2.2` addendum: the working tree.

  In a checklist's `v0.2.2` addendum, each backticked client `.py` path is checked at the client's
  commit through `git show`. A package-relative name there (`SQL/ClientPool.py` and the like) is
  checked as the package's file. A checklist's `docs/` and `prompts/` paths that are not this
  repository's are the client's, and are skipped. SGK's `docs/OPEN_ISSUES.md:685` is SGK's index
  (log 10, observation 1).
- **Names.** Every dotted `datastorekit.` name is listed. `<scratch>/probe/import_names.py` imports
  each in `venv/`, and the bare names the new text uses.

**The output** (summarised; the full report is `<scratch>/out/check-links.txt`):
- **81 relative links, every one resolved.** Among them:
  - `docs/client-contract.md#93-actor-names-prompt-01` and `#94-actor-names-prompt-01b` (README),
    and `../client-contract.md#93-actor-names-prompt-01` and `#94-actor-names-prompt-01b` (each
    addendum), headings `docs/client-contract.md:301` and `:317`;
  - `#addendum-v022-actor-names-prompt-02-2026-10-11` from each file's italic line, from the
    README's addendum to each checklist's, and from each checklist's to the README's;
  - the three gate rows' links to each checklist's new anchor;
  - every existing link (`#9-changes-after-v020`, `#91-prompt-08a`, `#92-prompt-08b`, the
    `v0.2.1` anchors, the README's eight contract anchors, `PROVENANCE.md`, `LICENSE`,
    `.github/workflows/tests.yml`, `datastorekit/tests/client/`, `docs/extraction/`).

  5 external links were not followed.
- **455 backticked paths: 316 checked and present, 139 skipped (a client's, or patterns), 0
  failed.** Among the checked:
  - every `datastorekit/SQL/ShardedPool.py:…` of the README's and SGK's `v0.2.2` addenda, at the
    tree;
  - every `docs/adoption/…:…` of the four new tables;
  - every client path of the three checklist addenda at its commit, among them
    `Datastore/tests/standin_pool.py:231-247`,
    `ComputeTargets/tests/test_quadsource_policy_main.py:430-431`,
    `Datastore/SQL/ShardedPool.py:294` and `tests/conftest.py:36-74`;
  - the `v0.2.1` addenda's `datastorekit/` citations at `33778b0`.
- **22 dotted names, every one importable in `venv/`:** `datastorekit.SQL`, `.SQL.Datastore`,
  `.SQL.Datastore.Datastore` (the actor class), `.SQL.ShardedPool`, `.SQL.factory_base`,
  `.SQL.schema`, `datastorekit.__file__`, `._timing`, `.contract`, `.contract.VERSION_LABEL`,
  `.contract.VERSION_SERIAL_KEY`, `.contract.require_version_serial`, `.defaults`,
  `.replication`, `.shard_paths`, `.store_inventory`, `.store_inventory.read_inventory`,
  `.store_reader`, `.tests`, `.tools`, `.tools.shard_key_audit`, `.tools.sharded_store`.

  The bare names the new text uses are present: `ShardedPool.__exit__`, `._kill_actors`,
  `._close_refused_open`; the module's `_ray_is_running` and `SerialPoolBroker`;
  `datastorekit.tests.standin_pool.StandinCluster.active`; the module
  `test_closed_pool_releases_its_names` and its `TestClosingAPoolStartsNoRay`.
  `ray.is_initialized()` was `False` after the imports.
- **The contract rows** each addendum names exist with those "Change" cells: §9.3's
  "`ShardedPool.__exit__`", "A refused open" and "Two open pools", §9.4's "`ShardedPool._kill_actors`,
  when the process is not connected to Ray". So do the issue names in `PROVENANCE.md` (the
  extraction board's §4 and this board's §4) and the commits `ac50a8a` and `f024fc6`.
- **The `v0.2.2` line citations**, read at the tree: `ShardedPool.py:47-55` is
  `_ray_is_running`; `:428` the call of `_kill_actors` in `_close_refused_open`; `:430-457`
  `_kill_actors`, with `:446-447` the guard; `:857-884` `__exit__`, with `:867-868` the early
  return.

`RESULT: OK` for both scripts.

### 5.6 What changed since `v0.2.1` (§1.1, re-checked)

`git diff --numstat 33778b0 f024fc6 -- datastorekit`: `SQL/ShardedPool.py` 64/0,
`tests/standin_pool.py` 70/2, `tests/test_closed_pool_releases_its_names.py` 262/0. `git show
--stat`: `ac50a8a` 48 lines in `SQL/ShardedPool.py`, `f024fc6` 16. At `v0.2.1` (`33778b0`),
`__exit__` is `SQL/ShardedPool.py:808-820`, with no flag and no kill.

### 5.7 The documents (§4.4)

Every remaining `v0.2.1`, by line, with why it stays:

| File | Lines | Why it stays |
|---|---|---|
| `README.md` | `:16` | the `v0.2.2` paragraph's statement that `v0.2.1` never started Ray on a close |
| | `:23` | history: the `v0.2.1` status paragraph |
| | `:75` | the "remain tagged" sentence |
| | `:106` | "the three fixes of `v0.2.1`", in the extended item |
| `PROVENANCE.md` | `:118`, `:131`, `:138` | history: the `v0.2.1` section |
| `docs/adoption/README.md` | `:8`, `:9` | the `v0.2.1` italic line, superseded (`:7-10`) |
| | `:14`, `:15` | this prompt's italic line |
| | `:208`, `:226`, `:233`, `:267` | history: the `v0.2.1` addendum's heading, table header, store sentence and `:3` row, true of `v0.2.1` |
| | `:213`, `:217`, `:258`, `:268`–`:271`, `:273` | statements this addendum supersedes |
| | `:279`–`:363` (20 lines) | this addendum's own comparisons, and its table |
| `docs/adoption/secondarygwkit.md` | `:17`, `:18` | the `v0.2.1` italic line, superseded (`:16-19`) |
| | `:22`–`:24` | this prompt's italic line |
| | `:369`, `:386`, `:427`, `:437`, `:438`, `:441` | history: the `v0.2.1` addendum, true of `v0.2.1` |
| | `:375`, `:376`, `:379`, `:422`, `:436`, `:442`, `:443` | statements this addendum supersedes |
| | `:449`–`:533` (19 lines) | this addendum's own comparisons, and its table |
| `docs/adoption/champbh.md` | `:18`, `:19` | the `v0.2.1` italic line, superseded |
| | `:23`–`:25` | this prompt's italic line |
| | `:412`, `:425`, `:433`, `:449`, `:459`, `:460` | history: the `v0.2.1` addendum, true of `v0.2.1` |
| | `:418`, `:419`, `:422`, `:458`, `:461` | statements this addendum supersedes |
| | `:467`–`:522` (16 lines) | this addendum's own comparisons, and its table |
| `docs/adoption/stochasticinstantons.md` | `:16`, `:17` | the `v0.2.1` italic line, superseded |
| | `:21`–`:23` | this prompt's italic line |
| | `:383`, `:402`, `:408`, `:419`, `:429`, `:430` | history: the `v0.2.1` addendum, true of `v0.2.1` |
| | `:389`, `:390`, `:393`, `:428`, `:431` | statements this addendum supersedes |
| | `:437`–`:491` (13 lines) | this addendum's own comparisons, and its table |

**The shift (correction 2), checked line by line.** For each citation of the `v0.2.1` addenda
below the insert, its line at `33778b0` equals this tree's line k later:
- README (k 5): `:13`, `:29`, `:40`, `:159`, `:161`, `:178`;
- SGK (k 6): `:21`, `:30`, `:187`, `:203`, `:208`, `:297`, `:306`;
- CPBH (k 6): `:22`, `:259`, `:379`;
- SI (k 6): `:20`, `:260`, `:353`.

All 19 are the same. `git diff 33778b0` of each of the four files has no removed line.

`git diff -- docs/adoption` has no `-` line (hazard 1). `docs/client-contract.md` and
`docs/extraction-verification.md` are unchanged (`git diff --quiet`).

### 5.8 The tree and the clients (§4.6)

- `git status --short --ignored` before staging shows the eleven files of §7's list as modified,
  this log as new, and dispatch's ignored entries: `.idea/`, `venv/`, and five `__pycache__/`
  directories (`datastorekit/`, `datastorekit/SQL/`, `datastorekit/tests/`,
  `datastorekit/tests/client/`, `docs/extraction/`). There is no `build/`, `dist/` or
  `*.egg-info`.
- `git diff --quiet` holds for `datastorekit/`, `docs/client-contract.md`,
  `docs/extraction-verification.md`, `docs/extraction/`, `.github/`, `CLAUDE.md`, `LICENSE` and
  `.gitignore`. On the extraction board only `:1537-1539` changed.
- The tags are `v0.1.0`, `v0.2.0` and `v0.2.1`; `origin/main` is `2fd3ba2`, as at dispatch.

The clients, read only through `git rev-parse`, `git status`, `git grep` and `git show`, were the
same at the start and at the end. `cmp` of the start and end `git status --short` captures is
silent for each.

| Client | Commit | Branch | `git status --short` |
|---|---|---|---|
| SGK | `b510bc9` | `handover-remedial` | 1 entry, `?? prompts/dk-and-rpk-migration/`, not this campaign's (not read) |
| CPBH | `52142d7` | `main` | 23 untracked entries (not read) |
| SI | `7bb3efd` | `main` | empty |

---

## 6. The deliberate-breakage record (§4.5)

**The method.**
1. Each diff below was made with `diff -u` of `pyproject.toml` before and after the one change,
   labelled `a/` and `b/`, and is recorded exactly as applied (`<scratch>/breaks/`).
2. Each has its own export: `git archive 210141e` (whose `pyproject.toml` is this commit's) into
   `<scratch>/exports/break-a` and `break-b`, and `git archive v0.2.1` into `break-c`.
3. In each export, `git apply --check` passed on the clean export, `git apply` applied it, and
   `git apply -R --check` passed on the applied one.
4. Each was built with `uv build --offline --wheel`, installed offline into its own Python 3.13.16
   venv with `ray==2.55.1` and `sqlalchemy==2.0.46`, and checked from `<scratch>/outside` with
   `assert_release.py` against `v0.2.1`'s wheel.

None is committed.

**(a) `pyproject.toml`'s version left at `0.2.1`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -4,7 +4,7 @@
 
 [project]
 name = "datastorekit"
-version = "0.2.2"
+version = "0.2.1"
 description = "A sharded SQLite datastore layer (Datastore / ShardedPool) on Ray and SQLAlchemy"
 requires-python = ">=3.12"
 dependencies = [
```

The wheel is `datastorekit-0.2.1-py3-none-any.whl`, 98,806 bytes, 25 entries, none under
`tests/`, `METADATA` `Version: 0.2.1`.

```
FAIL wheel name: datastorekit-0.2.1-py3-none-any.whl
FAIL METADATA Version: Version: 0.2.1
PASS no entry under datastorekit/tests/: 0 of 25 entries
PASS 25 entries: 25
PASS RECORD against v0.2.1: only SQL/ShardedPool.py differs: 20 and 20 lines under datastorekit/; differing: ['datastorekit/SQL/ShardedPool.py']
FAIL importlib.metadata.version: 0.2.1
PASS ShardedPool has _kill_actors: True
PASS module has _ray_is_running: True
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
RESULT: FAILED (3): wheel name, METADATA Version, importlib.metadata.version
```

**Verdict:** the `METADATA` and `importlib.metadata.version` assertions fail, naming `0.2.1`, as
§4.5 says; the wheel's name fails with them. The fix is in the wheel: only the version is wrong.

**(b) The `exclude` line removed from `pyproject.toml`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -14,4 +14,3 @@
 
 [tool.setuptools.packages.find]
 include = ["datastorekit*"]
-exclude = ["datastorekit.tests", "datastorekit.tests.*"]
```

The wheel is `datastorekit-0.2.2-py3-none-any.whl`, 307,582 bytes, **72 entries, 47 under
`datastorekit/tests/`** (`datastorekit/tests/__init__.py`, `client/…`, `standin_pool.py`,
`test_closed_pool_releases_its_names.py`, …).

```
PASS wheel name: datastorekit-0.2.2-py3-none-any.whl
PASS METADATA Version: Version: 0.2.2
FAIL no entry under datastorekit/tests/: 47 of 72 entries
FAIL 25 entries: 72
FAIL RECORD against v0.2.1: only SQL/ShardedPool.py differs: 20 and 67 lines under datastorekit/; differing: ['datastorekit/SQL/ShardedPool.py', 'datastorekit/tests/__init__.py', … 47 paths under datastorekit/tests/]
PASS importlib.metadata.version: 0.2.2
PASS ShardedPool has _kill_actors: True
PASS module has _ray_is_running: True
FAIL import datastorekit.tests fails: exit=0 (no error)
RESULT: FAILED (4): no entry under datastorekit/tests/, 25 entries, RECORD against v0.2.1: only SQL/ShardedPool.py differs, import datastorekit.tests fails
```

`import datastorekit.tests` resolves to `<R>/datastorekit/tests/__init__.py`, in the venv's
`site-packages`. **Verdict:** the wheel lists files under `datastorekit/tests/`, and `import
datastorekit.tests` succeeds. The counts are the orchestrator's: 72 entries, 47 under `tests/`.

**(c) The wheel built from `git archive v0.2.1` with only its version set to `0.2.2`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -4,7 +4,7 @@
 
 [project]
 name = "datastorekit"
-version = "0.2.1"
+version = "0.2.2"
 description = "A sharded SQLite datastore layer (Datastore / ShardedPool) on Ray and SQLAlchemy"
 requires-python = ">=3.12"
 dependencies = [
```

Applied to an export of `v0.2.1`, where `git apply --check` and `-R --check` pass as recorded. The
wheel is `datastorekit-0.2.2-py3-none-any.whl`, 97,852 bytes, 25 entries, none under `tests/`,
`METADATA` `Version: 0.2.2`.

```
PASS wheel name: datastorekit-0.2.2-py3-none-any.whl
PASS METADATA Version: Version: 0.2.2
PASS no entry under datastorekit/tests/: 0 of 25 entries
PASS 25 entries: 25
FAIL RECORD against v0.2.1: only SQL/ShardedPool.py differs: 20 and 20 lines under datastorekit/; differing: none
PASS importlib.metadata.version: 0.2.2
FAIL ShardedPool has _kill_actors: False
FAIL module has _ray_is_running: False
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
RESULT: FAILED (3): RECORD against v0.2.1: only SQL/ShardedPool.py differs, ShardedPool has _kill_actors, module has _ray_is_running
```

**The 20 `RECORD` lines compared** (correction 3), `v0.2.1`'s wheel against (c)'s: the same 20
paths, and every one the same hash, `SQL/ShardedPool.py`'s included (`sha256=_Ij01ywRDgBlIQKVX7Elcm5…`
on both sides). The paths: `SQL/ClientPool.py`, `SQL/Datastore.py`, `SQL/ProfileAgent.py`,
`SQL/SerialPoolBroker.py`, `SQL/ShardedPool.py`, `SQL/__init__.py`, `SQL/factory_base.py`,
`SQL/schema.py`, `__init__.py`, `_timing.py`, `contract.py`, `defaults.py`, `object.py`,
`replication.py`, `shard_paths.py`, `store_inventory.py`, `store_reader.py`, `tools/__init__.py`,
`tools/shard_key_audit.py` and `tools/sharded_store.py`. The release check's commands at (c):
`ShardedPool has _kill_actors: False`, `__exit__` docstring `None`, `module has _ray_is_running:
False`.

**Verdict:** `METADATA` says `0.2.2`, but the `RECORD` comparison shows no line differing where the
release shows `SQL/ShardedPool.py`'s, `ShardedPool` has no `_kill_actors`, and the module has no
`_ray_is_running`. The check catches a version number with no fix behind it, 01's or 01b's.

---

## 7. Observations not acted on

1. **The `v0.2.1` addenda's own tables now point k lines early** in this tree (correction 2). That
   is the reason for each `v0.2.2` addendum's sentence and table row. They are not rewritten
   (rule 6), and no issue is needed: the reader is told how to read them.
2. **The checklists' italic line is one line longer than the README's** (five and four lines, so k
   is 6 and 5). Both are as wrapped at ~100 columns. Nothing to change.
3. **Several table rows in the new addenda, in the gates and in this log run past 100 columns**, as
   the `v0.2.1` addenda's and the board's rows do. None is a defect.
4. **The scratch tools** are in `<scratch>/probe/`, not in the repository: `insert.py`,
   `measure_step2.py`, `wheel_info.py`, `compare_record.py`, `release_check.sh`,
   `assert_release.py`, `check_links.py` and `import_names.py`. Their outputs are in
   `<scratch>/out/`; the exports, wheels, venvs, diffs and inserted texts are under `<scratch>`.
5. **The dispatch's state counts six `__pycache__/` directories; I found five** at the start and at
   the end (`datastorekit/`, `datastorekit/SQL/`, `datastorekit/tests/`,
   `datastorekit/tests/client/`, `docs/extraction/`), with `.idea/` and `venv/`: seven ignored
   entries in all, as `git status --short --ignored` lists them. A miscount in the hand-off, with
   no effect.

---

## 8. Issues

- **Opened:** none. **Closed:** none. **Narrowed:** none.
- This board's §3 holds no issue. The index is at **4 open**: 0 on this repository's boards and 4
  inherited.

---

## 9. State handed to the next prompt

- `HEAD` is this commit, unpushed and untagged. The tree is clean apart from dispatch's ignored
  entries. `venv/` has `datastorekit 0.2.2` installed editable from this checkout, its `egg-info`
  removed.
- **Not pushed, not tagged.** `origin/main` is `2fd3ba2`, and the tags are `v0.1.0`, `v0.2.0` and
  `v0.2.1`.
- **After the review**, this commit is pushed as `main`, fast-forwarding over `a4290de`,
  `ce2070b`, `394a974` and the review. `v0.2.2` is made on this commit, annotated, only once CI
  passes there at both ends (U23, U28). If CI fails, a fix prompt lands first, and no tag is made
  on a commit whose CI is red.
- **The suite is 494** in `venv/` and at the high end (0 `ResourceWarning` lines at each).
  `compare_ported_tests.py`: 20 modules and one test declared not ported, exit 0. `black --check
  datastorekit docs`: 72 files.
- **For the campaign's close:** every `v0.2.2` addendum's `datastorekit/` citation is at
  `f024fc6`'s tree, which `v0.2.2` will name. G2–G4 stay on the extraction board, recorded when
  each holds.
- **Scratch** (not in the repository): `<scratch>`, holding `exports/` (`head-before`, `release`,
  `v021`, `high`, `break-a`, `break-b`, `break-c`), `wheels/`, the venvs (`venv-high-before`,
  `venv-high`, `venv-release`, `venv-break-a`, `-b`, `-c`), `breaks/` (the three diffs),
  `addenda/` (the inserted texts), `probe/` and `out/`.
