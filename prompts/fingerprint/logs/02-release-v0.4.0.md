# Log 02 — release `v0.4.0`

**Subject:** Make the package ready to be released as v0.4.0 · **Commit:** this commit ·
**Date:** 2026-10-14 · **Model:** Claude Opus 5.5 · **Result:** landed; unpushed and untagged; not
yet reviewed.

The package is ready to be released as **`v0.4.0`** (U6). `pyproject.toml` says `0.4.0`, and
nothing else in it changed. `README.md` has a `v0.4.0` status paragraph, the `v0.4.0` pin with the
pins by client (SecondaryGWKit adopts `v0.4.0`; ChamPBH may stay on `v0.3.0` and
StochasticInstantons adopt `v0.3.0`, or either may move to `v0.4.0`), a "store fingerprint" item
under "Using it", and its "What changed after `v0.2.0`" item extended to `v0.4.0`. `PROVENANCE.md`
has a section for `fingerprint` prompt 01, naming the module's source, SGK
`RunRegistry/stores.py:1164-1400` at `c8a7f14`. Each of the four files under `docs/adoption/` has
an italic line at its head and a dated section, "Addendum: v0.4.0 (fingerprint prompt 02,
2026-10-14)", giving the pins, what changed for that client since `v0.3.0`, a table of every
statement it supersedes by `path:line`, what stands, and how to read the earlier addenda's
citations (N, k + N, 2k + N and 3k + N, as numbers). `git diff` of the four files has no `-` line.
**SGK's addendum** is the note SGK's `runregistry-extraction` prompt 03 reads: it separates what
moving the pin changes (nothing SGK calls) from what changes when SGK calls the package's
functions (seven numbered items, each with SGK's `path:line` at `a5a6f6d`), names SGK's options
for the fingerprints it holds and makes no choice, and ends with a table for SGK's 03. The
extraction board's G4 reads "SI adopted `v0.3.0` or later (… `fingerprint` U6)", with a dated
line saying the tag waits for CI; G1, G2 and G3 are unchanged.

**No line of code changed.** Nothing under `datastorekit/` is touched. The suite stays at **530**:
in `venv/` before and after (`pip show datastorekit` gives `0.4.0` after the offline reinstall), and
at the high end before and after. A wheel built offline from an export of the tree is
`datastorekit-0.4.0-py3-none-any.whl`, 26 entries, none under `datastorekit/tests/`. Against
`v0.3.0`'s wheel, its 20 `RECORD` lines under `datastorekit/` are equal and one is added,
`store_fingerprint.py`'s. Installed at the high pins and run from outside the repository, it
behaves as the prompt's §1.2 says. Breakage (a) fails the release check on `0.3.0`, (b) on the
test package, and (c), `v0.3.0`'s tree at `0.4.0`, on a `RECORD` with nothing added and
`ModuleNotFoundError` for `datastorekit.store_fingerprint`. §1.1's measure of the clients, re-run,
reproduces the prompt's table exactly.

**No tag was made and nothing was pushed.** Nothing was downloaded: every venv, install and build
is `uv … --offline`. No client was written, run, imported or opened. Ray was never started. No
issue was opened, and the index stays at **4**.

Prompt: [`../02-release-v0.4.0.md`](../02-release-v0.4.0.md), with the orchestrator's dispatch note
§0: four corrections, its additions, its checked facts and its conventions. §2 classifies each.
Line numbers under `datastorekit/` are `v0.4.0`'s tree (`d1b61d6`'s `datastorekit/`, which this
commit does not change) unless another tree is named; an SGK line is SGK's at `a5a6f6d`.

`<scratch>` below is `<session scratchpad>/agent02`, outside the repository.

---

## 1. What shipped

### 1.1 `pyproject.toml` (§2.1)

`version = "0.3.0"` → `version = "0.4.0"` (`:7`), the only change. No other file carries the
version.

### 1.2 `README.md` (§2.2)

- **Status.** A new paragraph for **`v0.4.0`** (`:10-20`), above `v0.3.0`'s: a minor release with
  one change, `fingerprint` prompt 01, on the user's ruling; the new module
  `datastorekit.store_fingerprint` takes a store's fingerprint from what `read_inventory` returns
  (`fingerprint_of`), compares two (`compare_fingerprints`) and lists one (`listing_lines`); the
  client gives its own `fingerprint_format`, which it keeps and bumps, and the package records its
  own `ENCODING_FORMAT` beside it, outside the digest; a comparison refuses two fingerprints whose
  formats of either kind differ; nothing the layer writes or reads changes, no message, refusal or
  exception, and `store_inventory` is unchanged, so a client that does not import the module meets
  nothing new; it adds API, so it is minor. It links `docs/client-contract.md#97-fingerprint-prompt-01`.
- **Installing.** The pin is `@v0.4.0` (`:105`). The sentence at `:96-99` (as `object-timestamp` 02
  left it) is replaced by `:108-111`: `v0.3.0`, `v0.2.3`, `v0.2.2`, `v0.2.1`, `v0.2.0` and `v0.1.0`
  remain tagged and no tag is moved or deleted; SecondaryGWKit adopts `v0.4.0`; ChamPBH may stay on
  `v0.3.0` and StochasticInstantons adopt `v0.3.0`, or either may move to `v0.4.0`, in a commit of
  its own, as it chooses: neither calls the new module, and nothing they call changes. Clients are
  named, no client path. Written as of the tag.
- **Using it.** A new item after "The inventory declarations": **the store fingerprint**,
  optional (`:136-142`): the three functions with their signatures, the client's
  `fingerprint_format` (an `int` of at least 1, bumped when its specs or registry change what the
  fingerprint sees), and the package's `ENCODING_FORMAT`, never bumped by a client, linking §9.7.
  "What changed after `v0.2.0`" (`:150-159`): `v0.4.0`'s change added, a new module the layer
  never calls, with `ENCODING_FORMAT` beside the client's format, linking §9.7, and still linking
  §9 (the "; and the change of `v0.3.0`" before it became "; the change of `v0.3.0`").
- Nothing else changed.

### 1.3 `PROVENANCE.md` (§2.3)

A new `###` section, "`fingerprint` prompt 01: the store fingerprint moves into the package
(`v0.4.0`)" (`:274`), after the `object-timestamp` section, under "After `v0.1.0`". Nothing above
it changed. It says:
- **its source is SGK, after the import commit**: SGK's `RunRegistry/stores.py:1164-1400` at
  `c8a7f14` (2026-10-12; `RunRegistry/` unchanged from there to `a5a6f6d`), the five functions and
  three helpers by name; the extract's SHA-256 `9b1a8aedb006ffa9c2635038eda2e87cad451106283d022a94f8038cd8eb0108`
  (re-computed here: `git show c8a7f14:RunRegistry/stores.py | sed -n 1164,1400p | shasum -a 256`);
  the user's ruling of 2026-10-12, SGK's D3, carried out by `fingerprint` 01 (`d1b61d6`); not under
  `compare_with_source.py`, retired at `v0.1.0`, its comparison being 01's equivalence check;
- **the differences from the source**, each of README §6.2's U1–U3, the module-scope import and
  the rewritten prose; every digest, count and comparison entry is the source's (01's log §4.3, 0
  differences); `store_inventory.py` unchanged since `v0.2.2`;
- **what changed in the package**: one module (351 lines), every other file in the wheel
  `v0.3.0`'s; outside the wheel, the test module (21 tests), the golden and contract §9.7; the
  suite 509 → 530;
- **the files 01 changes, and its log** (from `git show --stat d1b61d6`, records excluded).

### 1.4 The addenda (§2.4, U6)

Each file gains an italic line at its head, after `object-timestamp` prompt 02's and the blank
after it, and an unnumbered section `## Addendum: v0.4.0 (fingerprint prompt 02, 2026-10-14)`,
anchor `#addendum-v040-fingerprint-prompt-02-2026-10-14`:
- in the README the italic line is `:27-30`, then a blank, and the section is at the end, after a
  `---` (heading `:606`, the file ending at `:737`);
- in each checklist the italic line is five lines and a blank (SGK `:39-43`, CPBH `:40-44`, SI
  `:38-42`). The section follows the `v0.3.0` addendum's last paragraph, with a `---` of its own
  above it, and comes before the `---` that precedes the appendix (headings SGK `:732`, CPBH
  `:710`, SI `:685`; appendix SGK `:959`, CPBH `:797`, SI `:776`).

Each section gives:
- the pins by client (U6): SGK `…@v0.4.0`, in place of `v0.2.2`, by its `runregistry-extraction`
  prompt 03; CPBH `…@v0.3.0` (adopted; G3 holds since 2026-10-13) or `…@v0.4.0`; SI `…@v0.3.0` or
  `…@v0.4.0`, when it is next active; a move being a commit of the client's own; that U6 amends
  `object-timestamp` U6 for G4 and keeps it for G2 and G3; G4 now "SI has adopted `v0.3.0` or
  later"; G2's and G3's readings unchanged, and both holding;
- what changed for that client since `v0.3.0`, with contract §9.7 linked by anchor (the README
  addendum's table gives what a client that imports the module gets, with `v0.4.0`'s line numbers
  of `store_fingerprint.py`);
- §1.1's measure, as re-run (§5.4): in the README as one table, one row per client; in each
  checklist for that client;
- in the README, that a client's own fingerprints have no `encoding_format` and are refused by the
  package's comparison, so a client that moves to the package's functions recomputes those it
  holds or keeps comparing them with its own code; and that `ENCODING_FORMAT` is the package's,
  bumped under §9.7, a bump being said in the releasing addendum to every checklist;
- the rule for line citations: 07a's `datastorekit/` lines are `v0.2.0`'s, …, the `v0.3.0`
  addendum's `v0.3.0`'s, and this addendum's `v0.4.0`'s (`d1b61d6`'s `datastorekit/`);
- a supersession table, with the reading of the earlier addenda's citations above it, and a
  "Standing, not superseded" paragraph:

| File | Lines added | Lines removed | Inserted after (at `2f5417e`) | N | k | k + N | 2k + N | 3k + N |
|---|---|---|---|---|---|---|---|---|
| `docs/adoption/README.md` | 140 | 0 | `:26` | **5** | 5 | **10** | **15** | **20** |
| `docs/adoption/secondarygwkit.md` | 233 | 0 | `:38` | **6** | 6 | **12** | **18** | **24** |
| `docs/adoption/champbh.md` | 93 | 0 | `:39` | **6** | 6 | **12** | **18** | **24** |
| `docs/adoption/stochasticinstantons.md` | 97 | 0 | `:37` | **6** | 6 | **12** | **18** | **24** |

So: the `v0.3.0` addendum's citations are read at `2f5417e`, or N lines later here, except those
above the insert (the `v0.2.3` italic line it cites: README `:17-20`, SGK `:27-31`, CPBH `:28-32`,
SI `:26-30`; SI's rows for `:44-45` and later are below it, and shift); the `v0.2.3` addendum's at
`0de2b16`, or k + N lines later, except README `:12-15`, SGK `:21-25`, CPBH `:22-26`, SI
`:20-24`; the `v0.2.2` addendum's at `6d8ee9a`, or 2k + N, except README `:7-10`, SGK `:16-19`,
CPBH `:17-20`, SI `:15-18`; the `v0.2.1` addendum's at `33778b0`, or 3k + N, except README `:3`,
SGK and CPBH `:6`, SI `:5`. Each addendum states the four numbers. Checked line by line (§5.7):
505 lines, 0 differ.

**The SGK addendum's shape** (the orchestrator's addition): under its pin and "What changed since
`v0.3.0`", a `###` section "What moving the pin changes: nothing SGK calls" (`:769`; SGK's own
three functions and their 20 calls; `canonical_json` and `read_inventory` unchanged since
`v0.2.2`; `v0.2.3` and `v0.3.0` ask nothing; no suite count changes, as read; item 8); a `###`
section "What changes when SGK calls the package's functions" (`:792`), items (1)–(7) as the
prompt's §2.4 lists them, each with SGK's `path:line` at `a5a6f6d`, checked by `git show` (§5.5),
with SGK's options under (3); the sentence that item 9's fingerprint statements still hold; and a
`###` table "For SGK's prompt 03" (`:895`), each item at the pin (03) and at the call (06). It
quotes no refusal text of the package's beyond §9.7's: item (1) says the refusal names the
argument's type and value.

The four tables are repeated in §4.

### 1.5 The extraction board's gate (§2.5)

`prompts/extraction/IMPLEMENTATION_STATE.md` §2, row G4 (`:1539`), and nothing else on that board
(`git diff --numstat`: 1/1):
- the title, exactly: "SI adopted `v0.3.0` or later (U37; `actor-names` U3; `factory-defaults` U5;
  `object-timestamp` U6; `fingerprint` U6)";
- the status cell gains, at its end, one dated italic sentence: "*(2026-10-14: `v0.4.0` is ready to
  be tagged on `fingerprint` prompt 02's commit once CI passes there at both ends, as U23 and U28;
  02 makes no tag and pushes nothing. SI may adopt `v0.3.0` or `v0.4.0`, as it chooses
  (`fingerprint` U6). SI's addendum is [link to its `v0.4.0` anchor].)*". `git diff --word-diff`
  shows only `or later`, `U6; \`fingerprint\`` and the appended sentence. G1, G2 and G3
  (`:1536-1538`) and the board's header are unchanged.

### 1.6 The records

- This log.
- This board: the header, §1's row for 02 (landed, "this commit", log), a note for prompt 02, and
  §3's dated line.
- This campaign's README: a sentence in its header, and §2's row for 02.
- `prompts/INDEX.md`: `fingerprint`'s status.
- `docs/OPEN_ISSUES.md` is unchanged at **4**: no issue opened.

---

## 2. Deviations from the prompt

1. **Correction 1: the earlier addenda's citations, with numbers.** Each italic line goes after
   the `v0.3.0` italic line's blank (after README `:26`, SGK `:38`, CPBH `:39`, SI `:37`), and each
   addendum states N, k + N, 2k + N and 3k + N as numbers (§1.4): 5, 10, 15, 20 in the README and
   6, 12, 18, 24 in each checklist, with the citations above the insert named. Checked line by
   line (§5.7). **STRUCTURALLY REQUIRED.**
2. **Correction 2: what each `v0.3.0` addendum says that `v0.4.0` supersedes, and what stands.**
   Each item of the correction's list is in its file's table, cited in the file as committed (N
   lines after the correction's numbers): README `:22-25` (above the insert), `:491-506`,
   `:508-509`, `:576-584`, `:589`, `:592-598`; SGK `:33-37`, `:649-669` (in part), `:671`,
   `:701-709`, `:713-721`, **`:722`** and **`:723`** (the correction's `:716` and `:717`, which the
   prompt's table misses); CPBH `:34-38`, `:636-648` (in part), `:650-651`, `:685-693`,
   `:697-705`; SI `:32-36`, `:601-607`, `:609-610`, `:654-662`, `:674`, `:676-681`. **Standing, not
   superseded**, each named in its addendum's paragraph: G2's reading and holding (SGK `:651-653`,
   `:725-728`) and SGK's "What changed for SGK since `v0.2.3`" (`:673-693`); G3's reading (CPBH
   `:638`, row `:706`) and CPBH's account of the object (`:653-677`); SI's head-line row (`:666`),
   its rows on `DatastoreObject.timestamp` (`:667-673`) and its "does not leave the layer"
   (`:641`); the README's `DatastoreObject.timestamp` account (`:511-562`) and "Not superseded"
   (`:600-602`). Nothing advises SGK, CPBH or SI either way. **STRUCTURALLY REQUIRED.**
3. **Beyond correction 2's list**, found by its rule and recorded as found. Each is in its file's
   table. **STRUCTURALLY REQUIRED.**
   - README `:588`, in part: the row for `:17-20` says "this addendum, now at the end", which the
     `v0.4.0` addendum makes untrue.
   - README `:590`: the row for `:398-399`, "`v0.3.0` carries those and `v0.2.3`'s change,
     unchanged", the carry-over sentence `:508-509` restated as a row; superseded with it.
   - README `:591` and SI `:675`: the rows for the `v0.2.3` addendum's shift paragraph, giving five
     and ten (six and twelve) lines, which this insert moves by N. (SGK's and CPBH's are within
     correction 2's ranges, `:716` and `:700`.)
4. **The shift paragraphs are cited to their own extent**: README `:576-584`, SGK `:701-709`, CPBH
   `:685-693`, SI `:654-662`. Correction 2's ranges (`:571-581`, `:695-705`, `:679-689`, `:648-658`
   before the insert) ran two lines further, over the blank and the table's header row.
   **IMPLEMENTATION CHOICE.**
5. **Correction 3: the extraction board.** §2 is `:1532-1541`, G1–G4 `:1536-1539`; G4's title and
   status cell are as the correction says; the sentence goes after the `v0.3.0` "is made"
   sentence. Recorded as found.
6. **Correction 4: SGK's call sites.** My own measure (§5.4) gives the prompt's §1.1 table exactly
   at `a5a6f6d` and `c8a7f14`. `retire_store`'s test of a mismatch is
   `RunRegistry/tests/test_store_retire.py:460-479` (`test_a_mismatch_in_problems_alone`), and the
   refusal it exercises is `RunRegistry/stores.py:1871-1893`; the addendum cites both. SGK 03's
   acceptance 3 is SGK README `:216-217` (it runs onto `:217`); the addendum cites `:216-217`.
   Recorded as found.
7. **The orchestrator's additions** are followed as given, each an **IMPLEMENTATION CHOICE** at the
   orchestrator's direction:
   - the order of work (baseline and measure; `pyproject.toml`, the reinstall and the suite; the
     two documents; the italic lines and addenda, and hazard 1's diff; G4; the release check and
     the high end; (a)–(c); the documents' and link checks; the end);
   - each addendum's supersessions as a table with a "Standing, not superseded" paragraph, the
     tables repeated in §4;
   - the SGK addendum's shape (§1.4): the two sections, items (1)–(7) with SGK's `path:line`s,
     SGK's options under (3) with no choice made, and the table "For SGK's prompt 03";
   - placement: the `---` rules, the README's addendum at the end, the heading and its anchor;
   - the README addendum's table of §1.1, one row per client, SGK's sites summarised by count and
     file with the two positional `taken` calls named;
   - `PROVENANCE.md`'s new section as a `###`;
   - the contract anchors `#97-fingerprint-prompt-01`, `#9-changes-after-v020` and
     `#4-the-inventorys-declarations`;
   - G4's title exactly as given, one dated italic sentence in its status cell;
   - the name-and-link check as a scratch script, never committed;
   - (a), (b) and (c) each built from its own export;
   - §1.1's measure by a script of my own (`<scratch>/probe/measure_fingerprint.py`), `ast` reads
     of `git show`, run with `python3.13 -I`.
8. **What the SGK addendum says beyond the prompt's list**, each checked through `git show` at
   `a5a6f6d` (§5.5). **IMPLEMENTATION CHOICE.**
   - Under (1), what the positional `taken` in `fingerprint_store` reaches: `python -m RunRegistry
     store fingerprint` would fail; `retire_store` refuses with "a fresh fingerprint could not be
     taken" (`RunRegistry/stores.py:1879-1886`); `Run.finish(..., fingerprint=True)`, which never
     raises for a fingerprint, would record the `TypeError` as `fingerprint_error`
     (`RunRegistry/__init__.py:379-392`).
   - Under (3), **which stores the refusal reaches**: SGK's audit
     (`docs/runregistry-extraction-audit.md:204-214`) found its 14 sidecars then all tombstones,
     never fingerprinted again, which the brief repeats (`datastorekit-fingerprint-brief.md:97-100`);
     but SGK's R0 (its 02, `74eff08`) since recorded fingerprints made by SGK's code in two live
     stores' sidecars, "retired by the user after 09"
     (`docs/runregistry-extraction-verification.md:152-157`; `store_sidecars_02.txt:17`,
     `:69-70`, `:88`), and R1 runs at 03's tree. So the item bites on those, and on any other SGK
     counts.
   - A third option, **(c) retire such a store before SGK calls the package's functions**, beside
     the orchestrator's two examples, (a) recompute through `store fingerprint --write` (or the
     next `Run.finish(..., fingerprint=True)`) and (b) keep SGK's comparison for old fingerprints.
     Each says what it touches; none is chosen or advised.
   - `###` subheadings for the two halves and the table, so that SGK's 03 can cite each.
9. **Two SGK ranges are cited to their last non-blank line**: `parse_listing` `:114-135` and
   `_fingerprint_problems` `:416-436`, where the prompt gives `:114-136` and `:416-437` (the next
   line is blank in each). **IMPLEMENTATION CHOICE.**
10. **The release check of record is a second export.** I built the release first from
    `git archive $(git stash create)` = `86128d8` (working tree after the document edits, before
    four small edits to lines this prompt added under `docs/adoption/` and before the records),
    then again, after those edits, from `75d9e58` (`git stash create`, `git diff --quiet` with the
    working tree held; `git stash list` stayed empty). The two wheels' `RECORD`s are byte-equal
    (SHA-256 `c418fd39…d5f6`); §5.3 reports the second, and the high end's final run is on it. The
    records written after are not in the wheel. `pyproject.toml` and `datastorekit/` are this
    commit's in both, so (a)'s and (b)'s diffs apply to an export of this commit as recorded
    (re-checked on `75d9e58`). **IMPLEMENTATION CHOICE.**
11. **README's "What changed after `v0.2.0`"**: to add `v0.4.0`'s change to the list, "; and the
    change of `v0.3.0`" became "; the change of `v0.3.0`", the "and" moving to `v0.4.0`'s. The
    README is not additive-only. **IMPLEMENTATION CHOICE.**

---

## 3. The hazards (§3)

1. **Additive documents.** `git diff --numstat -- docs/adoption` gives 140/0, 233/0, 93/0 and 97/0,
   and `git diff -- docs/adoption | grep '^-' | grep -v '^--- '` finds nothing. Each insertion was
   made by `<scratch>/probe/insert.py`, which adds lines only, after checking the line before and
   after the insert point. Later edits changed only lines this prompt had added (two rewraps, the
   four shift-paragraph ranges, SGK's "no earlier run's `status.json`", and SGK's appendix rows
   `:1230-1232` named in its "Standing" paragraph). `docs/client-contract.md` and
   `docs/extraction-verification.md` are unchanged.
2. **Names and links.** Every one resolves (§5.6). The contract anchor, by GitHub's rule: "9.7
   `fingerprint` prompt 01" (`docs/client-contract.md:372`), lower-cased, with the `.` and the
   backticks dropped and the spaces made hyphens, is `97-fingerprint-prompt-01`. Each new heading,
   "Addendum: v0.4.0 (fingerprint prompt 02, 2026-10-14)", the same way (the `:`, `.`, `(`, `)` and
   `,` dropped), is `addendum-v040-fingerprint-prompt-02-2026-10-14`. "4. The inventory's
   declarations" (`:143`) is `4-the-inventorys-declarations`. The script derives every heading's
   slug that way and finds each anchor among them.
3. **The tag does not exist yet.** No document says `v0.4.0` is tagged: the README and the addenda
   state the pins, and the README says `v0.3.0` to `v0.1.0` "remain tagged"; G4's sentence says
   `v0.4.0` "is ready to be tagged … once CI passes there at both ends", and that 02 makes no tag.
4. **No client is re-measured beyond §1.1.** I re-ran §1.1's measure with a script of my own
   (§5.4). It reproduces §1.1's table exactly at SGK `a5a6f6d` and `c8a7f14`, CPBH `2792a85` and SI
   `5fb4a1d`. CPBH and SI define and call none of the three; a `git grep` of their whole trees for
   the three names and `store_fingerprint` finds nothing. No stop. Every SGK citation the addendum
   makes was read with `git show a5a6f6d:<path>` (§5.5).
5. **Offline only.** Every venv (`uv venv --offline`), install (`uv pip install --offline`) and
   build (`uv build --offline`) resolved from the cache: `setuptools` 84.0.0 (the build backend),
   `ray` 2.55.1 and `sqlalchemy` 2.0.46. Nothing was downloaded.
6. **`venv/`'s metadata.** After §2.1, `pip show datastorekit` said `0.3.0`. `uv pip install
   --offline --no-deps --python venv/bin/python -e .`, from the repository root, without
   `--no-build-isolation` (`venv/` has no `setuptools`: `import setuptools` raised
   `ModuleNotFoundError` there at the start): `- datastorekit==0.3.0`, `+ datastorekit==0.4.0`,
   exit 0. It wrote `datastorekit.egg-info/` at the root, which I deleted at once. `pip show` then
   gives `Version: 0.4.0`, editable from this checkout; `importlib.metadata.version` is `0.4.0` and
   the package imports from the source tree. The suite in `venv/` gives 530 OK after it (§5.1).
7. **No Ray.** The smoke script was not run. The release probes build an inventory by hand,
   fingerprint it and run `sharded_store --help`; `ray` is not in `sys.modules` after them, and the
   name check's `ray.is_initialized()` is `False`. At the start and the end no Ray process was up
   (`pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` empty), `RAY_ADDRESS` and
   `RAY_ENABLE_AUTO_CONNECT` were unset, and there was no `/tmp/ray/ray_current_cluster`.
8. **U6's wording.** Every statement of CPBH's and SI's pins is permission, with no advice either
   way: "may stay on `v0.3.0` … or either may move to `v0.4.0`, … as it chooses" (README
   `:108-111`; each addendum and its head line; G4's line). SGK's addendum names SGK's options under
   (3), "each SGK's to take or not; this addendum makes no choice", and marks nothing **Advice:**,
   since it recommends nothing.
9. **Run from the right place.** Every scratch-venv command ran with its export or
   `<scratch>/outside` as the working directory, `PYTHONPATH` unset. `datastorekit.__file__`:
   `venv/`, `<repo>/datastorekit/__init__.py` (editable, as intended); `venv-high-before`,
   `venv-high` and `venv-high2`, their exports' `datastorekit/__init__.py`; `venv-release`,
   `venv-release2` and each breakage's venv, its `site-packages/datastorekit/__init__.py`.
10. **The package names no client.** Nothing under `datastorekit/` changed; the guards pass in
    every suite run. `PROVENANCE.md` and `docs/adoption/` name the clients, as they may.

---

## 4. The supersession tables

Each is as committed in its addendum. Line numbers are each file's as committed with this
addendum.

### 4.1 `docs/adoption/README.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/README.md:22-25` | the `v0.3.0` addendum, "at the end", gives "the pins by client" | it gives `v0.3.0`'s pins and changes, true of `v0.3.0`; this addendum, now at the end, gives the pins of `v0.4.0` |
| `docs/adoption/README.md:491-506` | in part, the pins: "SI adopts `v0.3.0`", G4 reading "SI has adopted `v0.3.0`", the pin `…@v0.3.0`; "CPBH may stay on `v0.2.3` or move to `v0.3.0`"; "SGK may stay on `v0.2.2` or move to `v0.2.3` or `v0.3.0`" | SGK adopts `v0.4.0` in place of `v0.2.2`, by its `runregistry-extraction` prompt 03; CPBH, which has adopted `v0.3.0`, may stay on it or move to `v0.4.0`; SI adopts `v0.3.0` or `v0.4.0`, and G4 reads "SI has adopted `v0.3.0` or later" (`fingerprint` U6); "The pins, by client", above. G2's and G3's readings stand |
| `docs/adoption/README.md:508-509` | "`v0.3.0` carries `key_on_version`, `v0.2.0`'s feature, `v0.2.1`'s three fixes, `v0.2.2`'s fix and `v0.2.3`'s change, unchanged" | true of `v0.3.0`; `v0.4.0` carries those and `v0.3.0`'s change, unchanged |
| `docs/adoption/README.md:576-584` | the `v0.3.0` addendum's `path:line`s are "this file's as committed with this addendum", and the earlier addenda's are read 5, 10 and 15 lines later | they are read at `2f5417e`, or 5 lines later here; the `v0.2.3` addendum's 10, the `v0.2.2` addendum's 15, and the `v0.2.1` addendum's 20; above |
| `docs/adoption/README.md:588` | in part, the row for `:17-20`: "this addendum, now at the end, gives the pins of `v0.3.0`" | the `v0.3.0` addendum gives the pins of `v0.3.0`; this addendum is now at the end, and gives those of `v0.4.0` |
| `docs/adoption/README.md:589` | the row for `:387-396`, giving `v0.3.0`'s pins and G4 "SI has adopted `v0.3.0`" | as `:491-506` |
| `docs/adoption/README.md:590` | the row for `:398-399`: "`v0.3.0` carries those and `v0.2.3`'s change, unchanged" | as `:508-509` |
| `docs/adoption/README.md:591` | the row for `:454-460`: read "at `0de2b16`, or five lines later here; the `v0.2.2` addendum's ten, and the `v0.2.1` addendum's fifteen" | at `0de2b16`, or ten lines later here; the `v0.2.2` addendum's fifteen, and the `v0.2.1` addendum's twenty; above |
| `docs/adoption/README.md:592` | the row for `:467`: "as `:387-396`" | as `:491-506` |
| `docs/adoption/README.md:593` | the row for `:468`: "for SI the pin `…@v0.3.0`; for CPBH `…@v0.2.3` or `…@v0.3.0`; for SGK `…@v0.2.2`, `…@v0.2.3` or `…@v0.3.0`" | for SGK the pin `…@v0.4.0`; for CPBH `…@v0.3.0` or `…@v0.4.0`; for SI `…@v0.3.0` or `…@v0.4.0` |
| `docs/adoption/README.md:594` | the row for `:469`: the `v0.2.2` addendum's citations are read "at `6d8ee9a`, or ten lines later here" | at `6d8ee9a`, or fifteen lines later here (all but `:7-10`) |
| `docs/adoption/README.md:595` | the rows for `:470-471`: "as `:467` and `:468`" | as `:592` and `:593` |
| `docs/adoption/README.md:596` | the row for `:472`: "at `v0.3.0`, each checklist with its four addenda" | at `v0.4.0`, each checklist with its five addenda |
| `docs/adoption/README.md:597` | the rows for `:473-474`: "as `:467` and `:468`" | as `:592` and `:593` |
| `docs/adoption/README.md:598` | the row for `:475`: G2 when SGK has adopted `v0.2.2` or later; G3 when CPBH has adopted `v0.2.3` or later; "G4 when SI has adopted `v0.3.0` (U37; `actor-names` U3; `factory-defaults` U5; `object-timestamp` U6)" | G2 and G3 as before; G4 when SI has adopted `v0.3.0` or later (U37; `actor-names` U3; `factory-defaults` U5; `object-timestamp` U6; `fingerprint` U6) |

**Standing, not superseded:** in `:491-506`, G2's reading, "SGK has adopted `v0.2.2` or later",
and G3's, "CPBH has adopted `v0.2.3` or later", with G2 holding; the `v0.3.0` addendum's account of
`DatastoreObject.timestamp` (`:511-562`), true of `v0.4.0`, whose `datastorekit/object.py` is
`v0.3.0`'s; and its "Not superseded" (`:600-602`). §2's module map (`:91-95`) maps the modules a
client's own layer has, and `store_fingerprint` is not one of them: the map gains no row, and stays
true.

### 4.2 `docs/adoption/secondarygwkit.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/secondarygwkit.md:33-37` | the `v0.3.0` addendum gives "SGK's pin, `v0.2.2`, `v0.2.3` or `v0.3.0` as SGK chooses" | it gives `v0.3.0`'s pins and changes, true of `v0.3.0`; this addendum gives SGK's pin at `v0.4.0`: `v0.4.0`, by its `runregistry-extraction` prompt 03 |
| `docs/adoption/secondarygwkit.md:649-669` | in part: "SGK may stay on **`v0.2.2`** or move to **`v0.2.3`** or **`v0.3.0`**, as SGK chooses", and the pins `…@v0.2.2`, `…@v0.2.3` or `…@v0.3.0` | SGK adopts `v0.4.0` in place of `v0.2.2`, by its `runregistry-extraction` prompt 03 (`fingerprint` U6); the pin `…@v0.4.0`; "The pin", above. The rest stands: a move is a commit of SGK's own, and G2's reading and its holding (`:651-653`) |
| `docs/adoption/secondarygwkit.md:671` | "`v0.3.0` carries `v0.2.1`'s three fixes, `v0.2.2`'s fix and `v0.2.3`'s change unchanged" | true of `v0.3.0`; `v0.4.0` carries those and `v0.3.0`'s change, unchanged |
| `docs/adoption/secondarygwkit.md:701-709` | the `v0.3.0` addendum's `path:line`s are "this file's as committed with this addendum", and the earlier addenda's are read 6, 12 and 18 lines later | they are read at `2f5417e`, or 6 lines later here; the `v0.2.3` addendum's 12, the `v0.2.2` addendum's 18, and the `v0.2.1` addendum's 24; above |
| `docs/adoption/secondarygwkit.md:713` | the row for `:27-31`: "this addendum gives SGK's pins at `v0.3.0`: `v0.2.2`, `v0.2.3` or `v0.3.0`, as SGK chooses" | the `v0.3.0` addendum gives those, true of `v0.3.0`; this addendum gives `v0.4.0`, above |
| `docs/adoption/secondarygwkit.md:714` | in part, the row for `:557-559`: "SGK may stay on `v0.2.2` or move to `v0.2.3` or `v0.3.0`, as SGK chooses (`object-timestamp` U6)" | SGK adopts `v0.4.0` (`fingerprint` U6), as `:649-669`. The row's G2 reading stands |
| `docs/adoption/secondarygwkit.md:715` | the row for `:561-569`: "`…@v0.2.2`, `…@v0.2.3` or `…@v0.3.0`, above" | `…@v0.4.0`, above |
| `docs/adoption/secondarygwkit.md:716` | the row for `:609-615`: read "at `0de2b16`, or six lines later here; the `v0.2.2` addendum's twelve, and the `v0.2.1` addendum's eighteen" | at `0de2b16`, or twelve lines later here; the `v0.2.2` addendum's eighteen, and the `v0.2.1` addendum's twenty-four; above |
| `docs/adoption/secondarygwkit.md:717` | in part, the row for `:623`: "or move to `v0.2.3` or `v0.3.0` (`object-timestamp` U6)" | as `:714` |
| `docs/adoption/secondarygwkit.md:718` | the row for `:624`: "as `:561-569`" | as `:715` |
| `docs/adoption/secondarygwkit.md:719` | the row for `:625`: the `v0.2.2` addendum's citations are read "at `6d8ee9a`, or twelve lines later here" | at `6d8ee9a`, or eighteen lines later here (all but `:16-19`) |
| `docs/adoption/secondarygwkit.md:720` | the rows for `:626-627`: "as `:623` and `:624`" | as `:717` and `:718` |
| `docs/adoption/secondarygwkit.md:721` | the row for `:628`: "at `v0.2.2`, `v0.2.3` or `v0.3.0`, with the four addenda" | at `v0.4.0`, with the five addenda |
| `docs/adoption/secondarygwkit.md:722` | the row for `:629`: "at `v0.3.0` also the change of contract §9.6, which changes nothing SGK's calls use" | at `v0.4.0` also the change of contract §9.7, which changes nothing SGK's calls use until SGK calls the package's functions, its prompt 06; "What moving the pin changes" and "What changes when SGK calls the package's functions", above |
| `docs/adoption/secondarygwkit.md:723` | the row for `:630`: item 8's reasoning "extended to `v0.3.0`" | extended to `v0.4.0`, since nothing the layer writes or reads changes; "Item 8 still holds", above |

**Standing, not superseded:** G2's reading and its holding, in the `v0.3.0` addendum's pin
(`:651-653`, "G2's reading is unchanged, 'SGK has adopted `v0.2.2` or later', and **G2 holds**")
and its "Standing" paragraph (`:725-728`), which are `fingerprint` U6's reading too; the `v0.3.0`
addendum's "What changed for SGK since `v0.2.3`" (`:673-693`), true of `v0.4.0`, whose
`datastorekit/object.py` is `v0.3.0`'s; item 9's fingerprint statements (`:333-360`), of SGK's
own code; and item 2's import table (`:112`) and the appendix's rows (`:1230-1232`), which count
SGK's imports of `canonical_json` and `read_inventory` at `b510bc9`, true of that commit.

### 4.3 `docs/adoption/champbh.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/champbh.md:34-38` | the `v0.3.0` addendum gives "CPBH's pin, `v0.2.3` or `v0.3.0` as CPBH chooses" | it gives `v0.3.0`'s pins and changes, true of `v0.3.0`; this addendum gives CPBH's pins at `v0.4.0`: `v0.3.0`, which CPBH has adopted, or `v0.4.0`, as CPBH chooses |
| `docs/adoption/champbh.md:636-648` | in part: "CPBH may stay on **`v0.2.3`** or move to **`v0.3.0`**, as CPBH chooses", and the pins `…@v0.2.3` or `…@v0.3.0` | CPBH has adopted `v0.3.0` (G3 holds, 2026-10-13), and may stay on it or move to `v0.4.0` (`fingerprint` U6); the pins `…@v0.3.0` or `…@v0.4.0`; "The pin", above. The rest stands: a move is a commit of CPBH's own, and G3's reading (`:638`) |
| `docs/adoption/champbh.md:650-651` | "`v0.3.0` carries `key_on_version`, `v0.2.0`'s feature, `v0.2.1`'s three fixes, `v0.2.2`'s fix and `v0.2.3`'s change, unchanged" | true of `v0.3.0`; `v0.4.0` carries those and `v0.3.0`'s change, unchanged |
| `docs/adoption/champbh.md:685-693` | the `v0.3.0` addendum's `path:line`s are "this file's as committed with this addendum", and the earlier addenda's are read 6, 12 and 18 lines later | they are read at `2f5417e`, or 6 lines later here; the `v0.2.3` addendum's 12, the `v0.2.2` addendum's 18, and the `v0.2.1` addendum's 24; above |
| `docs/adoption/champbh.md:697` | the row for `:28-32`: "this addendum gives CPBH's pins at `v0.3.0`: `v0.2.3` or `v0.3.0`, as CPBH chooses" | the `v0.3.0` addendum gives those, true of `v0.3.0`; this addendum gives `v0.3.0` or `v0.4.0`, above |
| `docs/adoption/champbh.md:698` | in part, the row for `:546-548`: "CPBH may stay on `v0.2.3` or move to `v0.3.0` (`object-timestamp` U6)" | CPBH has adopted `v0.3.0`, and may stay on it or move to `v0.4.0` (`fingerprint` U6), as `:636-648`. The row's G3 reading stands |
| `docs/adoption/champbh.md:699` | the row for `:550-552`: "`…@v0.2.3` or `…@v0.3.0`, as CPBH chooses, above" | `…@v0.3.0` or `…@v0.4.0`, as CPBH chooses, above |
| `docs/adoption/champbh.md:700` | the row for `:598-604`: read "at `0de2b16`, or six lines later here; the `v0.2.2` addendum's twelve, and the `v0.2.1` addendum's eighteen" | at `0de2b16`, or twelve lines later here; the `v0.2.2` addendum's eighteen, and the `v0.2.1` addendum's twenty-four; above |
| `docs/adoption/champbh.md:701` | the row for `:612`: "as `:546-548`" | as `:698` |
| `docs/adoption/champbh.md:702` | the row for `:613`: "as `:550-552`" | as `:699` |
| `docs/adoption/champbh.md:703` | the row for `:614`: the `v0.2.2` addendum's citations are read "at `6d8ee9a`, or twelve lines later here" | at `6d8ee9a`, or eighteen lines later here (all but `:17-20`) |
| `docs/adoption/champbh.md:704` | the rows for `:615-616`: "as `:546-548` and `:550-552`" | as `:698` and `:699` |
| `docs/adoption/champbh.md:705` | the row for `:617`: "at `v0.2.3` or `v0.3.0`, as CPBH chooses, with the four addenda" | at `v0.3.0` or `v0.4.0`, as CPBH chooses, with the five addenda |

**Standing, not superseded:** G3's reading, "CPBH has adopted `v0.2.3` or later", in the `v0.3.0`
addendum's pin (`:638`) and its row (`:706`), which is `fingerprint` U6's reading too, G3 holding
(2026-10-13, the extraction board); and the `v0.3.0` addendum's account of the object (`:653-677`),
true of `v0.4.0`, whose `datastorekit/object.py` is `v0.3.0`'s.

### 4.4 `docs/adoption/stochasticinstantons.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/stochasticinstantons.md:32-36` | the `v0.3.0` addendum gives the pin **`v0.3.0`** | it gives `v0.3.0`'s pin and changes, true of `v0.3.0`; this addendum gives SI's pins at `v0.4.0`: `v0.3.0` or `v0.4.0`, as SI chooses |
| `docs/adoption/stochasticinstantons.md:601-607` | "SI adopts **`v0.3.0`** in place of `v0.2.3`, when it is next active", G4 reads "SI has adopted `v0.3.0`", and the pin `…@v0.3.0` | SI adopts `v0.3.0` or `v0.4.0`, as SI chooses, when it is next active (`fingerprint` U6), and G4 reads "SI has adopted `v0.3.0` or later"; the pins `…@v0.3.0` or `…@v0.4.0`; "The pin", above |
| `docs/adoption/stochasticinstantons.md:609-610` | "`v0.3.0` carries `key_on_version`, `v0.2.0`'s feature, `v0.2.1`'s three fixes, `v0.2.2`'s fix and `v0.2.3`'s change, unchanged" | true of `v0.3.0`; `v0.4.0` carries those and `v0.3.0`'s change, unchanged |
| `docs/adoption/stochasticinstantons.md:654-662` | the `v0.3.0` addendum's `path:line`s are "this file's as committed with this addendum", and the earlier addenda's are read 6, 12 and 18 lines later | they are read at `2f5417e`, or 6 lines later here; the `v0.2.3` addendum's 12, the `v0.2.2` addendum's 18, and the `v0.2.1` addendum's 24; above |
| `docs/adoption/stochasticinstantons.md:674` | the row for `:515-521`: "SI adopts `v0.3.0` in place of `v0.2.3`, when it is next active (`object-timestamp` U6), and G4 reads 'SI has adopted `v0.3.0`'; the pin `…@v0.3.0`" | as `:601-607` |
| `docs/adoption/stochasticinstantons.md:675` | the row for `:563-569`: read "at `0de2b16`, or six lines later here; the `v0.2.2` addendum's twelve, and the `v0.2.1` addendum's eighteen" | at `0de2b16`, or twelve lines later here; the `v0.2.2` addendum's eighteen, and the `v0.2.1` addendum's twenty-four; above |
| `docs/adoption/stochasticinstantons.md:676` | the row for `:577`: "as `:515-521`" | as `:601-607` |
| `docs/adoption/stochasticinstantons.md:677` | the row for `:578`: "the pin `…@v0.3.0`, above" | the pins `…@v0.3.0` or `…@v0.4.0`, above |
| `docs/adoption/stochasticinstantons.md:678` | the row for `:579`: the `v0.2.2` addendum's citations are read "at `6d8ee9a`, or twelve lines later here" | at `6d8ee9a`, or eighteen lines later here (all but `:15-18`) |
| `docs/adoption/stochasticinstantons.md:679` | the rows for `:580-581`: "as `:515-521`" | as `:601-607` |
| `docs/adoption/stochasticinstantons.md:680` | the row for `:582`: "at `v0.3.0`, with the four addenda" | at `v0.3.0` or `v0.4.0`, as SI chooses, with the five addenda |
| `docs/adoption/stochasticinstantons.md:681` | the row for `:583`: "G4 holds when SI has adopted `v0.3.0` (U37; `actor-names` U3; `factory-defaults` U5; `object-timestamp` U6)" | G4 holds when SI has adopted `v0.3.0` or later (U37; `actor-names` U3; `factory-defaults` U5; `object-timestamp` U6; `fingerprint` U6) |

**Standing, not superseded:** the `v0.3.0` addendum's account of `DatastoreObject.timestamp`, true
of `v0.4.0`, whose `datastorekit/object.py` is `v0.3.0`'s: its "What changed for SI since `v0.2.3`"
(`:612-646`), with its line that `DatastoreObject.timestamp` "does not leave the layer" (`:641`);
its row for the `v0.2.3` addendum's head line (`:666`); and its rows for `:44-45` to `:160`
(`:667-673`), each a statement about `DatastoreObject.timestamp` that `v0.3.0` superseded.

**Considered and not superseded.** The grep of §2.4 (`v0.3.0`, `fingerprint`, `store_inventory`,
`four addenda`, `RunRegistry`) outside the new addenda finds, in the files as committed:
- README `:92`, `:99` (the module map and its note, the prompt's `:87`, `:94`): they map the
  modules a client's own layer has, and `store_fingerprint` is not one; named in the addendum.
  `:259-260` (`RunRegistry/` lines of a pool-free check): facts of SGK, true;
- SGK `:82` (`Datastore/store_inventory.py` among the 17 layer files), `:112` and the appendix's
  `RunRegistry/` rows (`:1224-1241`; `:1230-1232` named in the addendum), `:133-137`, `:251`,
  `:277-279`, `:305`, `:371`, `:375`, `:408`, `:427`: facts of SGK at `b510bc9`, true of it; item
  9's fingerprint paragraph (`:333-360`): of SGK's own code, true, named in the addendum;
- CPBH `:100`, `:165`, `:291` (`datastorekit.store_inventory` and `read_inventory`): what CPBH
  imports or calls on adoption, unchanged;
- SI: none beyond the `v0.3.0` addendum's rows;
- in each file, the earlier addenda's `four addenda`, `v0.3.0` and pin statements other than those
  tabled: history true of their release.

---

## 5. Verification performed

### 5.1 The suite (§4.1)

Every run in the foreground, its output in `<scratch>/out/`, the verdict grepped from it.

| Where | When | Result | `ResourceWarning` lines | `datastorekit` |
|---|---|---|---|---|
| `venv/` (3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39, SQLite 3.53.4) | at the start, before any change | `Ran 530 tests in 87.010s` `OK` | 0 | 0.3.0 |
| `<scratch>/venv-high-before` (3.13.16 / 2.55.1 / 2.0.46, SQLite 3.53.4, `setuptools` 84.0.0), `git archive 692b943` installed editable `--no-deps --no-build-isolation` | at the start | `Ran 530 tests in 88.583s` `OK` | 0 | 0.3.0 |
| `venv/` | after `pyproject.toml` and the reinstall | `Ran 530 tests in 94.722s` `OK` | 0 | 0.4.0 |
| `<scratch>/venv-high`, the same pins, `git archive 86128d8` installed editable | after the document edits | `Ran 530 tests in 89.747s` `OK` | 4 | 0.4.0 |
| `<scratch>/venv-high2`, the same pins, `git archive 75d9e58` installed editable | after the last document edit | `Ran 530 tests in 92.001s` `OK` | 4 | 0.4.0 |
| `venv/` | after the records, before the commit | `Ran 530 tests in 84.269s` `OK` | 0 | 0.4.0 |

The count is **530** before and after, at both ends. The four high-end `ResourceWarning` lines are
two warnings, `unclosed database in <sqlite3.Connection …>` raised from SQLAlchemy's
`sql/type_api.py:975`, each with its tracemalloc hint: timing (`actor-names` log 01, correction 8).

### 5.2 The checks (§4.2)

- `compare_ported_tests.py`, before and after, exit 0, its last line: `OK: 20 module(s) keep their
  source's tests, classes and assertion skeletons; 1 test(s) declared not ported`.
- `./venv/bin/black --check datastorekit docs` (black 25.1.0), before and after: `78 files would be
  left unchanged.` No `.py` file changed.
- The guards (`test_layer_is_generic`, `test_prose_names_no_source`, `test_package_imports`) are
  in the suite and pass in every run above.

### 5.3 The release check (§4.3)

**The build.** `git archive 75d9e58 | tar -x -C <scratch>/exports/release2` (§2 item 10), then
`uv build --offline --wheel --out-dir <scratch>/wheels/release2 <scratch>/exports/release2`, exit 0.
For the comparison, `git archive v0.3.0` into `<scratch>/exports/v030`, built the same way. Nothing
was built in the checkout.

| | The release | `v0.3.0`'s, for comparison |
|---|---|---|
| Wheel | `datastorekit-0.4.0-py3-none-any.whl` | `datastorekit-0.3.0-py3-none-any.whl` |
| Size | 104,424 bytes | 99,488 bytes |
| Entries | **26**: none under `datastorekit/tests/`, 3 under `datastorekit/tools/` | 25 |
| SHA-256 | `3cb0cd23049f424c707c3500fca76f535a450acfd4410d5c33b1c8b8af06ab34` (the first build, from `86128d8`: `fbbe389909e58f94720a44d3ac533f60da24b01d6e8c4cbb0d61c0224af3a1dc`) | `f9052d5123c5d77ca4e2cca6a101761b258d555e2830953dd384e8ed37f75757` |
| `RECORD` SHA-256 | `c418fd39978cb3b25bb02ea0daa073aa19b8f86b2fe9d8f41d35d264ff13d5f6`, both builds | `d22f7935599a858f7f65feb945a8948c69dd4860dbe5c758342d8a5c5dce2144`, as `object-timestamp` log 02's release (§5.3) |
| `WHEEL` | `Generator: setuptools (84.0.0)` | the same |
| `METADATA` | `Name: datastorekit`, **`Version: 0.4.0`**, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43`, `Requires-Dist: sqlalchemy<2.1,>=2.0.39` | `Version: 0.3.0`, the rest the same |

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
datastorekit/store_fingerprint.py
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
datastorekit-0.4.0.dist-info/licenses/LICENSE
datastorekit-0.4.0.dist-info/METADATA
datastorekit-0.4.0.dist-info/WHEEL
datastorekit-0.4.0.dist-info/top_level.txt
datastorekit-0.4.0.dist-info/RECORD
```

**The `RECORD` comparison**, `v0.3.0`'s wheel against the release: 20 lines under `datastorekit/`
in `v0.3.0`'s, 21 in the release's; the 20 paths are the same and every line equal; the one added
is

```
datastorekit/store_fingerprint.py,sha256=OIGFxRU6LPEKr_W4zngOqHPSPwQCtT28T-aX4kVvcNg,16093
```

the orchestrator's line.

**The install.** `uv venv --offline -p /opt/local/bin/python3.13 <scratch>/venv-release2`, then
`uv pip install --offline --python <scratch>/venv-release2/bin/python <the wheel> "ray==2.55.1"
"sqlalchemy==2.0.46"`: 20 packages, exit 0, not editable. Python 3.13.16, SQLite 3.53.4.

**The probe**, `<scratch>/probe/release_probe.py`, run as `python -I` from `<scratch>/outside`
with `PYTHONPATH` unset: it imports the package, reads the metadata version, `ENCODING_FORMAT` and
`inspect.signature(fingerprint_of)`; builds a `StoreInventory` by hand from
`datastorekit.store_inventory`'s dataclasses, two classes ("Alpha", replicated and tagged, with two
records and one `orphan-tag` problem; "Beta", empty, naming a parent), its primary a path that does
not exist; and fingerprints, compares and lists it. **The assertions**,
`<scratch>/probe/assert_release.py <wheel> <venv python> <v0.3.0's wheel> 0.4.0 <scratch>/outside`,
which also runs three fresh interpreters (`import datastorekit.store_fingerprint` then `'ray' in
sys.modules`; `import datastorekit.tests`; `-m datastorekit.tools.sharded_store --help`):

```
wheel sha256: 3cb0cd23049f424c707c3500fca76f535a450acfd4410d5c33b1c8b8af06ab34  size: 104424
PASS wheel name: datastorekit-0.4.0-py3-none-any.whl
PASS METADATA Version: Version: 0.4.0
PASS no entry under datastorekit/tests/: 0 of 26 entries
PASS 26 entries: 26
PASS store_fingerprint.py in the wheel: True
PASS RECORD against v0.3.0: the 20 lines equal, store_fingerprint.py's added: 20 and 21 lines under datastorekit/; differing: none; missing: none; added: ['datastorekit/store_fingerprint.py']
  added line: datastorekit/store_fingerprint.py,sha256=OIGFxRU6LPEKr_W4zngOqHPSPwQCtT28T-aX4kVvcNg,16093
  probe exit 0 
PASS importlib.metadata.version: 0.4.0
PASS imported from site-packages: <scratch>/venv-release2/lib/python3.13/site-packages/datastorekit/__init__.py
PASS ENCODING_FORMAT is 1: 1
PASS signature: (inventory, fingerprint_format: int, taken: Optional[Mapping[str, Any]] = None) -> dict [('inventory', 'POSITIONAL_OR_KEYWORD', 'no default'), ('fingerprint_format', 'POSITIONAL_OR_KEYWORD', 'no default'), ('taken', 'POSITIONAL_OR_KEYWORD', 'None')]
PASS six keys, encoding_format 1, taken None: ['classes', 'digest', 'encoding_format', 'fingerprint_format', 'problems', 'taken']; 1; None
PASS digest recomputed equal: True
PASS keyword equal to positional: True
PASS format 6: digest differs, classes equal: (True, True)
PASS refusals: ['True: TypeError: fingerprint_of(): fingerprint_format must be an int, not bool True', "'1': TypeError: fingerprint_of(): fingerprint_format must be an int, not str '1'", '1.0: TypeError: fingerprint_of(): fingerprint_format must be an int, not float 1.0', "{'when': 'now'}: TypeError: fingerprint_of(): fingerprint_format must be an int, not dict {'when': 'now'}", '0: ValueError: fingerprint_of(): fingerprint_format must be at least 1, not 0', "missing: TypeError: fingerprint_of() missing 1 required positional argument: 'fingerprint_format'"]
PASS against a copy without encoding_format: [('encoding', None, 1)]
PASS against one with a taken: []
PASS listing words 2, 4, 6: # fingerprint_format 1 digest 4ee28a094016ca7ca941a89c1f12eb648d6a79463108a419b13c1ddabd55a6ed encoding_format 1 -> ('1', True, '1')
PASS inventory unchanged: True
PASS ray not in sys.modules after the probe: False
PASS a fresh import of datastorekit.store_fingerprint loads no ray: exit=0 False 
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
PASS sharded_store --help exits 0: exit=0 usage: python -m datastorekit.tools.sharded_store [-h] {copy,move} src dst
RESULT: OK
```

**The release check passes.** `git status --short --ignored` shows no `build/`, `dist/` or
`*.egg-info` in the checkout (§5.8).

### 5.4 §1.1's measure, re-run (hazard 4)

`<scratch>/probe/measure_fingerprint.py <repo> <commit>` (SHA-256 `6491af76e0da742c…`), run with
`/opt/local/bin/python3.13 -I` from `<scratch>/outside`: it lists the commit's `.py` files with
`git ls-tree -r`, outside `prompts/`, `.prompts/`, `docs/` and `.documents/`, reads each with `git
show <commit>:<path>`, parses it with `ast` (nothing imported or run), and reports every
`FunctionDef` named `fingerprint_of`, `compare_fingerprints` or `listing_lines` with its
arguments, every call of a name or attribute so named with its positional count and keyword
names (and any `*`/`**`), and the `datastorekit` line of `requirements.txt`.

```
== SecondaryGWKit at a5a6f6d
python files parsed: 224 (unparsed: 0)
def fingerprint_of: 1
  RunRegistry/stores.py:1182 (inventory, taken)
def compare_fingerprints: 1
  RunRegistry/stores.py:1256 (recorded, current)
def listing_lines: 1
  RunRegistry/stores.py:1376 (inventory, fingerprint)
calls of fingerprint_of: 10 {'1 positional': 8, '2 positional': 2}
  ObjectFactories/tests/test_quadsource_policy_key.py:413 positional=1 keywords=[]
  ObjectFactories/tests/test_quadsource_policy_key.py:416 positional=1 keywords=[]
  ObjectFactories/tests/test_quadsource_policy_key.py:419 positional=1 keywords=[]
  RunRegistry/stores.py:1500 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:147 positional=1 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:162 positional=1 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:196 positional=1 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:336 positional=1 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:378 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:566 positional=1 keywords=[]
calls of compare_fingerprints: 9 {'2 positional': 9}
  RunRegistry/stores.py:1529 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:219 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:254 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:447 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:176 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:338 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:381 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:455 positional=2 keywords=[]
  RunRegistry/tests/test_store_retire.py:471 positional=2 keywords=[]
calls of listing_lines: 1 {'2 positional': 1}
  RunRegistry/stores.py:1432 positional=2 keywords=[]
datastorekit pin: ['requirements.txt:17: datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.2']
== SecondaryGWKit at c8a7f14
python files parsed: 222 (unparsed: 0)
def fingerprint_of: 1
  RunRegistry/stores.py:1182 (inventory, taken)
def compare_fingerprints: 1
  RunRegistry/stores.py:1256 (recorded, current)
def listing_lines: 1
  RunRegistry/stores.py:1376 (inventory, fingerprint)
calls of fingerprint_of: 10 {'1 positional': 8, '2 positional': 2}
  ObjectFactories/tests/test_quadsource_policy_key.py:413 positional=1 keywords=[]
  ObjectFactories/tests/test_quadsource_policy_key.py:416 positional=1 keywords=[]
  ObjectFactories/tests/test_quadsource_policy_key.py:419 positional=1 keywords=[]
  RunRegistry/stores.py:1500 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:147 positional=1 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:162 positional=1 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:196 positional=1 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:336 positional=1 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:378 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:566 positional=1 keywords=[]
calls of compare_fingerprints: 9 {'2 positional': 9}
  RunRegistry/stores.py:1529 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:219 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:254 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:447 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:176 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:338 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:381 positional=2 keywords=[]
  RunRegistry/tests/test_store_fingerprint.py:455 positional=2 keywords=[]
  RunRegistry/tests/test_store_retire.py:471 positional=2 keywords=[]
calls of listing_lines: 1 {'2 positional': 1}
  RunRegistry/stores.py:1432 positional=2 keywords=[]
datastorekit pin: ['requirements.txt:17: datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.2']
== ChamPBH at 2792a85
python files parsed: 150 (unparsed: 0)
def fingerprint_of: 0
def compare_fingerprints: 0
def listing_lines: 0
calls of fingerprint_of: 0 {}
calls of compare_fingerprints: 0 {}
calls of listing_lines: 0 {}
datastorekit pin: ['requirements.txt:17: datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.3.0']
== StochasticInstantons at 5fb4a1d
python files parsed: 199 (unparsed: 0)
def fingerprint_of: 0
def compare_fingerprints: 0
def listing_lines: 0
calls of fingerprint_of: 0 {}
calls of compare_fingerprints: 0 {}
calls of listing_lines: 0 {}
datastorekit pin: none
```

**It reproduces §1.1's table exactly**, at every commit read: SGK `a5a6f6d` and `c8a7f14`, CPBH
`2792a85` and SI `5fb4a1d`. Beyond the script, a `git grep -E
'store_fingerprint|fingerprint_of|compare_fingerprints|listing_lines'` of CPBH's and SI's whole
trees at those commits (the excluded directories included) finds nothing, and SGK's whole tree at
`a5a6f6d` names `datastorekit.store_fingerprint` nowhere. No stop.

### 5.5 The SGK citations (hazard 4, the SGK addendum)

`<scratch>/probe/sgk_cites.py` reads every backticked SGK `path:line` in the lines this prompt added
to `secondarygwkit.md` and `README.md` and prints the cited lines through `git show a5a6f6d:<path>`:
36 distinct citations, every file present and every range within it (`<scratch>/out/sgk-cites.txt`).
Each was read against the statement that cites it. The bare continuations its rule cannot tie to a
path (`:162`, `:196`, `:336`, `:566`, `:416`, `:419`, `:350-356`, `:360-362`, `:74-78`,
`:120-122`, `:255`, and `store_sidecars_02.txt`'s `:69-70`, `:88`) were read by hand: each is the
call, test, assignment or line the addendum says. In particular, at `a5a6f6d`:
`RunRegistry/stores.py:1500-1508` passes `inventory` and a `taken` dict literal positionally;
`:1197` and `:1383` import `canonical_json`, `:1493` `read_inventory`, from
`datastorekit.store_inventory`; `:206` is `FINGERPRINT_FORMAT = 6`, under the history comment
`:194-205`; `RunRegistry/tests/test_store_fingerprint.py:360-362` is the five-key set, `:74-78`
`GOLDEN` (`full_store_fingerprint_datastore-integrity-09c.json`); the six golden files have the
keys `classes`, `digest`, `fingerprint_format`, `problems`, `taken` and formats 1–6, none
`encoding_format`.

### 5.6 Names and links (hazard 2)

**The method.** `<scratch>/probe/check_links.py`, a scratch script never committed, over
`README.md`, `PROVENANCE.md`, the four adoption files and the extraction board's §2: each relative
Markdown link outside a code fence is resolved, the file relative to the document, then the anchor
among the target's headings outside code fences, by GitHub's rule (§3 item 2), a repeated slug
gaining `-1`. `<scratch>/probe/import_names.py` imports in `venv/`, from `<scratch>/outside`, every
dotted `datastorekit.` name in `README.md`, `PROVENANCE.md` and the lines added to the adoption
files and the board.

**The output** (`<scratch>/out/check-links.txt`, `<scratch>/out/import-names.txt`):
- **151 relative links, every one resolved**, among them `docs/client-contract.md#97-fingerprint-prompt-01`
  (README `:20`, `:142`, `:158`) and `../client-contract.md#97-fingerprint-prompt-01` (each
  addendum), heading `docs/client-contract.md:372`; `docs/client-contract.md#4-the-inventorys-declarations`
  (README `:135`); `#addendum-v040-fingerprint-prompt-02-2026-10-14` from each file's italic line,
  from the README's addendum to each checklist's, and from each checklist's to the README's; G4's
  link to SI's new anchor (board `:1539`); every existing link.
- **13 names, every one importable in `venv/`**: `datastorekit.store_fingerprint`,
  `datastorekit.store_inventory`, `datastorekit.SQL.ShardedPool`, `datastorekit.SQL.factory_base`,
  `datastorekit.contract`, `.VERSION_SERIAL_KEY`, `.require_version_serial`,
  `datastorekit.defaults`, `datastorekit._timing`, `datastorekit.tools`, `.sharded_store`,
  `.shard_key_audit`, and `datastorekit.__file__`. `ray.is_initialized()` was `False` after. The
  bare names the documents give with the module (`fingerprint_of`, `compare_fingerprints`,
  `listing_lines`, `ENCODING_FORMAT`, `read_inventory`, `canonical_json`) are exercised by the
  release probe (§5.3).
- **The `v0.4.0` line citations**, read at the tree: `datastorekit/store_fingerprint.py:38-64` the
  bump rule's comment, `:65` `ENCODING_FORMAT = 1`, `:86-154` `fingerprint_of`, `:109-118` its two
  refusals, `:140-146` the overall object, `:147-154` the returned keys, `:194-227` the versions
  block, `:336-340` the listing's first line; the contract's §9.7 cites the same.

### 5.7 The documents (§4.4)

Every remaining `v0.3.0`, by line, with why it stays:

| File | Lines | Why it stays |
|---|---|---|
| `README.md` | `:22` | history: the `v0.3.0` status paragraph |
| | `:108` | the "remain tagged" sentence |
| | `:109`, `:110` | CPBH's and SI's permitted pins (U6) |
| | `:153` | history: "the change of `v0.3.0`", in the extended item |
| `PROVENANCE.md` | `:242` | history: the `object-timestamp` section's heading |
| | `:308` | this prompt's section: every other file in the wheel is `v0.3.0`'s |
| `docs/adoption/README.md` | `:23` | the `v0.3.0` italic line, superseded (`:22-25`) |
| | `:29` | this prompt's italic line |
| | `:484`–`:602` | the `v0.3.0` addendum: the statements tabled in §4.1 superseded, the rest history true of `v0.3.0` or standing |
| | `:609`–`:735` | this addendum's own text and table (CPBH's and SI's permitted pins among them) |
| `docs/adoption/secondarygwkit.md` | `:34`, `:35` | the `v0.3.0` italic line, superseded |
| | `:40`, `:41` | this prompt's italic line |
| | `:641`–`:723` | the `v0.3.0` addendum: superseded as tabled in §4.2, or standing, or history true of `v0.3.0` |
| | `:735`–`:953` | this addendum's own text and tables |
| `docs/adoption/champbh.md` | `:35`, `:36` | the `v0.3.0` italic line, superseded |
| | `:41`–`:43` | this prompt's italic line (CPBH's permitted pin) |
| | `:628`–`:705` | the `v0.3.0` addendum: superseded as tabled in §4.3, or standing, or history |
| | `:713`–`:793` | this addendum's own text and table |
| `docs/adoption/stochasticinstantons.md` | `:33`, `:34` | the `v0.3.0` italic line, superseded |
| | `:39`–`:41` | this prompt's italic line (SI's permitted pin) |
| | `:593`–`:681` | the `v0.3.0` addendum: superseded as tabled in §4.4, or standing, or history |
| | `:688`–`:772` | this addendum's own text and table |

**The shifts (correction 1), checked line by line** by `<scratch>/probe/check_shift.py`: for each
file and each earlier addendum (`v0.2.1` at `33778b0`, `v0.2.2` at `6d8ee9a`, `v0.2.3` at
`0de2b16`, `v0.3.0` at `2f5417e`), every own-file citation in that addendum's text as committed
then (an explicit `docs/adoption/<file>:a-b`, or a bare `:a-b` in a row of this file or in its
shift prose), each line of the range mapped by the stated rule (0 at or above the insert point of
that commit, `:11`/`:20`/`:21`/`:19` at `33778b0` up to `:26`/`:38`/`:39`/`:37` at `2f5417e`;
3k + N, 2k + N, k + N or N below it), compared with this tree's line: **505 lines in the four
files, 0 differ** (`<scratch>/out/check-shift.txt`).

`git diff -- docs/adoption` has no `-` line (hazard 1). `docs/client-contract.md` and
`docs/extraction-verification.md` are unchanged (`git diff --quiet`).

### 5.8 The tree and the clients (§4.6)

- `git status --short --ignored` before staging shows the eleven files of §7's list that this prompt
  changes as modified, this log as new, and the ignored entries at the start: `.idea/`, `venv/`,
  and five `__pycache__/` directories. There is no `build/`, `dist/` or `*.egg-info`. A sixth,
  `datastorekit/tools/__pycache__/`, written when the name check imported the two tools in
  `venv/` (editable from this checkout), was deleted.
- `git diff --quiet` holds for `datastorekit/`, `docs/client-contract.md`,
  `docs/extraction-verification.md`, `docs/extraction/`, `.github/`, `CLAUDE.md`, `LICENSE`,
  `.gitignore`, `docs/OPEN_ISSUES.md` and `prompts/fingerprint/orchestrator/`. On the extraction
  board only `:1539` changed.
- The tags are `v0.1.0`, `v0.2.0`, `v0.2.1`, `v0.2.2`, `v0.2.3` and `v0.3.0`; the local
  `origin/main` is `5f972be`, as at dispatch. No `git ls-remote` was run.

The clients, read only through `git rev-parse`, `git status`, `git ls-tree`, `git show`, `git grep`,
`git log` and `git diff --stat` between two of their commits:

| Client | At the start (08:58 BST) | At the end (09:27 BST) | `git status --short` |
|---|---|---|---|
| SGK | `a5a6f6d`, branch `handover-remedial` | `a5a6f6d`, unchanged | empty at the start and at the end |
| CPBH | `2792a85`, branch `read-only-plots` | `2792a85`, unchanged | 23 entries, the same at the end (`cmp` silent) |
| SI | `5fb4a1d`, branch `dk-and-rpk-migration` | `5fb4a1d`, unchanged | empty at the start and at the end |

---

## 6. The deliberate-breakage record (§4.5)

**The method.**
1. Each diff below was made with `diff -u` of `pyproject.toml` before and after the one change,
   labelled `a/` and `b/`, and is recorded exactly as applied (`<scratch>/breaks/`).
2. Each has its own export: `git archive 86128d8` (whose `pyproject.toml` is this commit's) into
   `<scratch>/exports/break-a` and `break-b`, and `git archive v0.3.0` into `break-c`.
3. In each export, `git apply --check` passed on the clean export, `git apply` applied it, and
   `git apply -R --check` passed on the applied one. (a) and (b) were checked the same way again on
   an export of `75d9e58`'s `pyproject.toml`.
4. Each was built with `uv build --offline --wheel`, installed offline into its own Python 3.13.16
   venv with `ray==2.55.1` and `sqlalchemy==2.0.46`, and checked from `<scratch>/outside` with
   `assert_release.py` against `v0.3.0`'s wheel, expecting `0.4.0`.

None is committed.

**(a) `pyproject.toml`'s version left at `0.3.0`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -4,7 +4,7 @@
 
 [project]
 name = "datastorekit"
-version = "0.4.0"
+version = "0.3.0"
 description = "A sharded SQLite datastore layer (Datastore / ShardedPool) on Ray and SQLAlchemy"
 requires-python = ">=3.12"
 dependencies = [
```

The wheel is `datastorekit-0.3.0-py3-none-any.whl`, 104,420 bytes, 26 entries, none under
`tests/`, `METADATA` `Version: 0.3.0`.

```
wheel sha256: e5662f5f84d2296492839069c87ccd823836aa431d1bf21cc22aad989f1ba5a7  size: 104420
FAIL wheel name: datastorekit-0.3.0-py3-none-any.whl
FAIL METADATA Version: Version: 0.3.0
PASS no entry under datastorekit/tests/: 0 of 26 entries
PASS 26 entries: 26
PASS store_fingerprint.py in the wheel: True
PASS RECORD against v0.3.0: the 20 lines equal, store_fingerprint.py's added: 20 and 21 lines under datastorekit/; differing: none; missing: none; added: ['datastorekit/store_fingerprint.py']
  added line: datastorekit/store_fingerprint.py,sha256=OIGFxRU6LPEKr_W4zngOqHPSPwQCtT28T-aX4kVvcNg,16093
  probe exit 0 
FAIL importlib.metadata.version: 0.3.0
PASS imported from site-packages: <scratch>/venv-break-a/lib/python3.13/site-packages/datastorekit/__init__.py
PASS ENCODING_FORMAT is 1: 1
PASS signature: (inventory, fingerprint_format: int, taken: Optional[Mapping[str, Any]] = None) -> dict [('inventory', 'POSITIONAL_OR_KEYWORD', 'no default'), ('fingerprint_format', 'POSITIONAL_OR_KEYWORD', 'no default'), ('taken', 'POSITIONAL_OR_KEYWORD', 'None')]
PASS six keys, encoding_format 1, taken None: ['classes', 'digest', 'encoding_format', 'fingerprint_format', 'problems', 'taken']; 1; None
PASS digest recomputed equal: True
PASS keyword equal to positional: True
PASS format 6: digest differs, classes equal: (True, True)
PASS refusals: ['True: TypeError: fingerprint_of(): fingerprint_format must be an int, not bool True', "'1': TypeError: fingerprint_of(): fingerprint_format must be an int, not str '1'", '1.0: TypeError: fingerprint_of(): fingerprint_format must be an int, not float 1.0', "{'when': 'now'}: TypeError: fingerprint_of(): fingerprint_format must be an int, not dict {'when': 'now'}", '0: ValueError: fingerprint_of(): fingerprint_format must be at least 1, not 0', "missing: TypeError: fingerprint_of() missing 1 required positional argument: 'fingerprint_format'"]
PASS against a copy without encoding_format: [('encoding', None, 1)]
PASS against one with a taken: []
PASS listing words 2, 4, 6: # fingerprint_format 1 digest 4ee28a094016ca7ca941a89c1f12eb648d6a79463108a419b13c1ddabd55a6ed encoding_format 1 -> ('1', True, '1')
PASS inventory unchanged: True
PASS ray not in sys.modules after the probe: False
PASS a fresh import of datastorekit.store_fingerprint loads no ray: exit=0 False 
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
PASS sharded_store --help exits 0: exit=0 usage: python -m datastorekit.tools.sharded_store [-h] {copy,move} src dst
RESULT: FAILED (3): wheel name, METADATA Version, importlib.metadata.version
```

**Verdict:** the `METADATA` and `importlib.metadata.version` assertions fail, naming `0.3.0`, as
§4.5 says; the wheel's name fails with them. The change is in the wheel (`store_fingerprint.py`'s
`RECORD` line is the release's, and the module behaves as the release's): only the version is
wrong.

**(b) The `exclude` line removed from `pyproject.toml`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -14,4 +14,3 @@
 
 [tool.setuptools.packages.find]
 include = ["datastorekit*"]
-exclude = ["datastorekit.tests", "datastorekit.tests.*"]
```

The wheel is `datastorekit-0.4.0-py3-none-any.whl`, 332,079 bytes, **78 entries, 52 under
`datastorekit/tests/`** (`test_store_fingerprint.py` among them; the golden `.json` is not, being
package data the build does not collect).

```
wheel sha256: ffc003156a64f6e411a2bd68c20fdfb488b4b9cc248f65275df35b69d9435117  size: 332079
PASS wheel name: datastorekit-0.4.0-py3-none-any.whl
PASS METADATA Version: Version: 0.4.0
FAIL no entry under datastorekit/tests/: 52 of 78 entries
FAIL 26 entries: 78
PASS store_fingerprint.py in the wheel: True
FAIL RECORD against v0.3.0: the 20 lines equal, store_fingerprint.py's added: 20 and 73 lines under datastorekit/; differing: none; missing: none; added: ['datastorekit/store_fingerprint.py', 'datastorekit/tests/__init__.py', 'datastorekit/tests/client/__init__.py', 'datastorekit/tests/client/build.py', '…']

  probe exit 0 
PASS importlib.metadata.version: 0.4.0
PASS imported from site-packages: <scratch>/venv-break-b/lib/python3.13/site-packages/datastorekit/__init__.py
PASS ENCODING_FORMAT is 1: 1
PASS signature: (inventory, fingerprint_format: int, taken: Optional[Mapping[str, Any]] = None) -> dict [('inventory', 'POSITIONAL_OR_KEYWORD', 'no default'), ('fingerprint_format', 'POSITIONAL_OR_KEYWORD', 'no default'), ('taken', 'POSITIONAL_OR_KEYWORD', 'None')]
PASS six keys, encoding_format 1, taken None: ['classes', 'digest', 'encoding_format', 'fingerprint_format', 'problems', 'taken']; 1; None
PASS digest recomputed equal: True
PASS keyword equal to positional: True
PASS format 6: digest differs, classes equal: (True, True)
PASS refusals: ['True: TypeError: fingerprint_of(): fingerprint_format must be an int, not bool True', "'1': TypeError: fingerprint_of(): fingerprint_format must be an int, not str '1'", '1.0: TypeError: fingerprint_of(): fingerprint_format must be an int, not float 1.0', "{'when': 'now'}: TypeError: fingerprint_of(): fingerprint_format must be an int, not dict {'when': 'now'}", '0: ValueError: fingerprint_of(): fingerprint_format must be at least 1, not 0', "missing: TypeError: fingerprint_of() missing 1 required positional argument: 'fingerprint_format'"]
PASS against a copy without encoding_format: [('encoding', None, 1)]
PASS against one with a taken: []
PASS listing words 2, 4, 6: # fingerprint_format 1 digest 4ee28a094016ca7ca941a89c1f12eb648d6a79463108a419b13c1ddabd55a6ed encoding_format 1 -> ('1', True, '1')
PASS inventory unchanged: True
PASS ray not in sys.modules after the probe: False
PASS a fresh import of datastorekit.store_fingerprint loads no ray: exit=0 False 
FAIL import datastorekit.tests fails: exit=0 (no error)
PASS sharded_store --help exits 0: exit=0 usage: python -m datastorekit.tools.sharded_store [-h] {copy,move} src dst
RESULT: FAILED (4): no entry under datastorekit/tests/, 26 entries, RECORD against v0.3.0: the 20 lines equal, store_fingerprint.py's added, import datastorekit.tests fails
```

**Verdict:** the wheel lists files under `datastorekit/tests/`, and `import datastorekit.tests`
succeeds. The counts are the orchestrator's: 78 entries, 52 under `tests/`.

**(c) The wheel built from `git archive v0.3.0` with only its version set to `0.4.0`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -4,7 +4,7 @@
 
 [project]
 name = "datastorekit"
-version = "0.3.0"
+version = "0.4.0"
 description = "A sharded SQLite datastore layer (Datastore / ShardedPool) on Ray and SQLAlchemy"
 requires-python = ">=3.12"
 dependencies = [
```

Applied to an export of `v0.3.0`, where `git apply --check` and `-R --check` pass as recorded. The
wheel is `datastorekit-0.4.0-py3-none-any.whl`, 99,490 bytes, 25 entries, none under `tests/`,
`METADATA` `Version: 0.4.0`.

```
wheel sha256: b92d308136a78cdd8d5593f6bb1609a883c469f39eda2e1b65f0a6f715721acb  size: 99490
PASS wheel name: datastorekit-0.4.0-py3-none-any.whl
PASS METADATA Version: Version: 0.4.0
PASS no entry under datastorekit/tests/: 0 of 25 entries
FAIL 26 entries: 25
FAIL store_fingerprint.py in the wheel: False
FAIL RECORD against v0.3.0: the 20 lines equal, store_fingerprint.py's added: 20 and 20 lines under datastorekit/; differing: none; missing: none; added: none
  probe exit 0 
PASS importlib.metadata.version: 0.4.0
PASS imported from site-packages: <scratch>/venv-break-c/lib/python3.13/site-packages/datastorekit/__init__.py
FAIL ENCODING_FORMAT is 1: ModuleNotFoundError: No module named 'datastorekit.store_fingerprint'
FAIL signature: None None
FAIL six keys, encoding_format 1, taken None: None; None; None
FAIL digest recomputed equal: None
FAIL keyword equal to positional: None
FAIL format 6: digest differs, classes equal: None
FAIL refusals: 
FAIL against a copy without encoding_format: None
FAIL against one with a taken: None
FAIL listing words 2, 4, 6: None -> None
FAIL inventory unchanged: None
FAIL ray not in sys.modules after the probe: None
FAIL a fresh import of datastorekit.store_fingerprint loads no ray: exit=1  ModuleNotFoundError: No module named 'datastorekit.store_fingerprint'
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
PASS sharded_store --help exits 0: exit=0 usage: python -m datastorekit.tools.sharded_store [-h] {copy,move} src dst
RESULT: FAILED (16): 26 entries, store_fingerprint.py in the wheel, RECORD against v0.3.0: the 20 lines equal, store_fingerprint.py's added, ENCODING_FORMAT is 1, signature, six keys, encoding_format 1, taken None, digest recomputed equal, keyword equal to positional, format 6: digest differs, classes equal, refusals, against a copy without encoding_format, against one with a taken, listing words 2, 4, 6, inventory unchanged, ray not in sys.modules after the probe, a fresh import of datastorekit.store_fingerprint loads no ray
```

**Verdict:** `METADATA` and `importlib.metadata.version` say `0.4.0`, but the `RECORD` comparison
shows no line added where the release adds `store_fingerprint.py`'s (25 entries, the 20 lines
under `datastorekit/` all `v0.3.0`'s), and `import datastorekit.store_fingerprint` raises
`ModuleNotFoundError: No module named 'datastorekit.store_fingerprint'`, in the probe and in a fresh
interpreter. The check catches a version number with no change behind it.

---

## 7. Observations not acted on

1. **The earlier addenda's own tables now point N, k + N, 2k + N or 3k + N lines early** in this
   tree (correction 1). That is the reason for each `v0.4.0` addendum's paragraph and its rows for
   the rule. They are not rewritten (rule 6), and no issue is needed: the reader is told how to read
   them. Each release adds one more layer; this is the fourth shift.
2. **SGK's brief says every sidecar SGK holds is a tombstone** (`datastorekit-fingerprint-brief.md:97-100`,
   after its audit `:204-214`), which SGK's R0 has since made untrue for two live stores (§2 item
   8). The SGK addendum states both; the brief is SGK's document, not this repository's. No issue.
3. **Several table rows in the new addenda, the gate and this log run past 100 columns**, as the
   earlier addenda's and the board's rows do, and five prose lines of the SGK addendum, each by a
   long backticked SGK path. None is a defect.
4. **The high end gave 4 `ResourceWarning` lines after, 0 before** (§5.1): two unclosed SQLite
   connections reported from SQLAlchemy, timing, in a tree whose `datastorekit/` is unchanged.
5. **The scratch tools** are in `<scratch>/probe/`, not in the repository: `insert.py`,
   `measure_fingerprint.py`, `release_probe.py`, `assert_release.py`, `wheel_info.py`,
   `check_links.py`, `import_names.py`, `sgk_cites.py` and `check_shift.py`. Their outputs are in
   `<scratch>/out/`; the exports, wheels, venvs, diffs and inserted texts are under `<scratch>`.
   `86128d8` and `75d9e58` are commit objects `git stash create` wrote with no ref.

---

## 8. Issues

- **Opened:** none. **Closed:** none. **Narrowed:** none.
- This board's §3 holds no issue. The index is at **4 open**, all on `inherited-issues`' board.

---

## 9. State handed to the next prompt

- `HEAD` is this commit, unpushed and untagged. The tree is clean apart from the ignored entries at
  the start. `venv/` has `datastorekit 0.4.0` installed editable from this checkout, its `egg-info`
  removed.
- **Not pushed, not tagged.** The local `origin/main` is `5f972be`, and the tags are `v0.1.0`,
  `v0.2.0`, `v0.2.1`, `v0.2.2`, `v0.2.3` and `v0.3.0`.
- **After the review**, this commit is pushed as `main`, fast-forwarding over the campaign's
  planning, 01 (`d1b61d6`) and its review, 02's writing, the note and the review. So CI's run on it
  is the first on 01's code as well as on the release. `v0.4.0` is made on it, annotated, only once
  CI passes there at both ends (U23, U28). If CI fails, a fix prompt lands first, and no tag is made
  on a commit whose CI is red.
- **The suite is 530** in `venv/` and at the high end. `compare_ported_tests.py`: 20 modules and one
  test declared not ported, exit 0. `black --check datastorekit docs`: 78 files.
- **For the campaign's close** (prompt §8): the tag object and commit, the SGK addendum's anchor
  (`docs/adoption/secondarygwkit.md#addendum-v040-fingerprint-prompt-02-2026-10-14`), README §0.2's
  six points, and the two found here: `fingerprint_store`'s positional `taken`
  (`RunRegistry/stores.py:1500`), and every fingerprint SGK holds lacking `encoding_format`, which
  reaches at least R0's two live stores (§2 item 8).
- **Scratch** (not in the repository): `<scratch>`, holding `exports/` (`head-before`, `release`,
  `release2`, `v030`, `high`, `high2`, `break-a`, `break-b`, `break-c`, `recheck-a`, `recheck-b`),
  `wheels/`, the venvs (`venv-high-before`, `venv-high`, `venv-high2`, `venv-release`,
  `venv-release2`, `venv-break-a`, `-b`, `-c`), `breaks/` (the three diffs), `addenda/` (the
  inserted texts), `probe/` and `out/`.
