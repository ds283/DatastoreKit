# Log 02 — release `v0.5.0`

**Subject:** Make the package ready to be released as v0.5.0 · **Commit:** `f47b9a2` ·
**Date:** 2026-10-21 · **Model:** Claude Opus 5.5 · **Result:** landed; untagged;
reviewed 2026-10-21 (the board's §1).

The package is ready to be released as **`v0.5.0`** (U5, as amended). `pyproject.toml` says
`0.5.0`, and nothing else in it changed. `README.md` has a `v0.5.0` status paragraph, the `v0.5.0`
pin with the pins by client (StochasticInstantons adopts `v0.5.0`; SecondaryGWKit and ChamPBH may
stay on `v0.4.0` or move), the further value tables under "The inventory declarations", and its
"What changed after `v0.2.0`" item extended to `v0.5.0`. `PROVENANCE.md` has a section for
`extra-values` prompt 01, which has no source in a client. Each of the four files under
`docs/adoption/` has an italic line at its head and a dated section, "Addendum: v0.5.0
(extra-values prompt 02, 2026-10-21)", giving the pins, what changed for that client since
`v0.4.0`, a table of every statement it supersedes by `path:line`, what stands, and how to read
the earlier addenda's citations (N, k + N, … as numbers, and the appendix's offset in each
checklist). `git diff` of the four files has no `-` line. **SI's addendum** is the note SI's pin
prompt reads: what SI declares and where, what then holds, and what of SI's own code and tests
moves. **SGK's and ChamPBH's** say that a move changes nothing they call or hold, that their spec
guard then fails, that the format is not bumped for it, and give the one condition in `plain`.
The extraction board's G4 gains one dated sentence; G1, G2 and G3 are unchanged.
`[01-a-new-spec-field-moves-every-spec-guard-digest]` is closed: moved to the board's §4, its row
deleted from `docs/OPEN_ISSUES.md`, which now counts **4**.

**No line of code changed.** Nothing under `datastorekit/` is touched. The suite stays at **538**:
in `venv/` before and after (`pip show datastorekit` gives `0.5.0` after the offline reinstall),
and at the high end. A wheel built offline from an export of the tree is
`datastorekit-0.5.0-py3-none-any.whl`, 105,087 bytes, 26 entries, none under
`datastorekit/tests/`. Against `v0.4.0`'s wheel, 19 of its 21 `RECORD` lines under `datastorekit/`
are equal, none is added or missing, and two differ, `store_fingerprint.py`'s and
`store_inventory.py`'s, each the line the prompt gives. Installed at the high pins and run from
outside the repository, it behaves as the prompt's §1.2 says, the guard's recipe included.
Breakage (a) fails the check on `0.4.0`, (b) on the test package, and (c), `v0.4.0`'s tree at
`0.5.0`, on a `RECORD` with nothing differing, six spec fields and the guard probe. §1.1's measure
of the clients, re-run, reproduces the prompt's table exactly.

**No tag was made and nothing was pushed.** Nothing was downloaded: every venv, install and build
is `uv … --offline`. No client and not RunRegistryKit was written, run, imported or opened. Ray was
never started.

Prompt: [`../02-release-v0.5.0.md`](../02-release-v0.5.0.md), with the orchestrator's dispatch note
§0: three corrections, its additions, its checked facts and its conventions. §2 classifies each.
Line numbers under `datastorekit/` are `v0.5.0`'s tree (`5475cef`'s `datastorekit/`, which this
commit does not change) unless another tree is named; a client's line is that client's at the
commit named: SGK `031bcb4`, CPBH `7055532`, SI `f5f395b`, RunRegistryKit its tag `v0.2.0`.

`<scratch>` below is `<session scratchpad>/agent02`, outside the repository.

---

## 1. What shipped

### 1.1 `pyproject.toml` (§2.1)

`version = "0.4.0"` → `version = "0.5.0"` (`:7`), the only change. No other file carries the
version.

### 1.2 `README.md` (§2.2)

- **Status.** A new paragraph for **`v0.5.0`** (`:10-22`), above `v0.4.0`'s: a minor release with
  one change, `extra-values` prompt 01, at a client's request; a factory's `InventorySpec` may name
  further value tables, `extra_values`, each counted as `values` is into each record's
  `extra_value_counts`, 0 where a row has none; a record of a class that declares none is
  `v0.4.0`'s, byte for byte, and so is every fingerprint of a store read with unchanged specs,
  `ENCODING_FORMAT` staying 1; nothing the pool writes or reads changes, and no message, refusal
  or exception of the pool's, the inventory reading a further table only where a spec declares one
  and gaining one refusal, in `inventory_classes`; a spec now has seven fields, so a client that
  hashes a spec by walking its fields sees every digest move, and the adoption addenda say what to
  do; it adds API, so it is minor. It links `docs/client-contract.md#98-extra-values-prompt-01`
  and `docs/adoption/README.md`.
- **Installing.** The pin is `@v0.5.0` (`:119`). The sentence that was `:108-111` is replaced by
  `:122-125`: `v0.4.0`, `v0.3.0`, `v0.2.3`, `v0.2.2`, `v0.2.1`, `v0.2.0` and `v0.1.0` remain tagged
  and no tag is moved or deleted; StochasticInstantons adopts `v0.5.0`; SecondaryGWKit and ChamPBH
  may stay on `v0.4.0` or move to `v0.5.0`, in a commit of their own, as each chooses; a client
  whose tests pin digests of its specs reads its addendum in `docs/adoption/` first. Clients are
  named, no client path. Written as of the tag.
- **Using it.** "The inventory declarations" (`:148-151`) gains "and, optionally, the further value
  tables its records are counted in, `extra_values`", linking §9.8. "What changed after `v0.2.0`"
  (`:166-178`): `v0.5.0`'s change added, a spec may name further value tables, each counted into
  its records' `extra_value_counts`, carried only where its class declares one, with
  `ENCODING_FORMAT` unchanged, linking §9.8, and still linking §9 (the "; and the change of
  `v0.4.0`" before it became "; the change of `v0.4.0`").
- Nothing else changed.

### 1.3 `PROVENANCE.md` (§2.3)

A new `###` section, "`extra-values` prompt 01: an inventory spec counts more than one value table
(`v0.5.0`)" (`:321`), after the `fingerprint` section, under "After `v0.1.0`". Nothing above it
changed (`git diff` is 55 `+` lines, 0 `-`). It says:
- **it has no source in a client**: the package's own change, at SI's request, its brief
  (`.prompts/dk-and-rpk-migration/datastorekit-second-value-table-brief.md`, SI `f5f395b`, read
  through `git` only), decided by `prompts/extra-values/README.md` §6.2 (U1–U4; U2 the user's
  ruling) and made by `extra-values` prompt 01 (`5475cef`); where it departs from the brief,
  README §0.2;
- **what changed in the package**: `store_inventory.py` (+57 −18, by `git diff --numstat c8570e8
  5475cef`), each change named; `store_fingerprint.py` (+6), the comment, `ENCODING_FORMAT` still
  `1`; nothing added or removed from the wheel; every record of a class that declares no extra
  table unchanged, shown by 01's test 1, which reproduces the format-1 golden through a spec that
  does not declare the field, in every field but `taken`;
- **outside the wheel**: the test module (8 tests), `TraceMark`, the witness, the format-2 golden,
  the test literals, contract §9.8 and its head line; the suite 530 → 538;
- **the files 01 changed** (from `git show --stat 5475cef`, records excluded), and its log.

### 1.4 The addenda (§2.4, U5)

Each file gains an italic line at its head, after `fingerprint` prompt 02's and the blank after it,
and an unnumbered section `## Addendum: v0.5.0 (extra-values prompt 02, 2026-10-21)`, anchor
`#addendum-v050-extra-values-prompt-02-2026-10-21`:
- in the README the italic line is `:32-35`, then a blank; the section is at the end, after a
  `---` (heading `:746`, the file ending at `:899`);
- in each checklist the italic line is five lines and a blank (SGK `:45-49`, CPBH `:46-50`, SI
  `:44-48`). The section follows the `v0.4.0` addendum's last paragraph, with a `---` of its own
  above it, and comes before the `---` that precedes the appendix (headings SGK `:965`, CPBH
  `:803`, SI `:782`; appendix SGK `:1120`, CPBH `:950`, SI `:957`).

Each section gives the pins by client (every client on `v0.4.0`, as read at §1.1's commits, with
the commit that pinned it: SGK `5b81f2e`, CPBH `f41b104`, SI `1b1ca6d`); what changed for that
client since `v0.4.0`, contract §9.8 linked by anchor; the rule for line citations; a supersession
table with the reading of the earlier addenda's citations above it; and a "Standing, not
superseded" paragraph. In particular:
- **README**: the pins; a table of what a client sees (`v0.5.0`'s line numbers of
  `store_inventory.py` and `store_fingerprint.py`); "Nothing any client supplies or stores
  changes"; §1.1's measure, re-run (§5.4), one row per client; **"The spec guard"**: what the
  recipe does, why every digest moves, the one condition, that with it every pin stays valid at
  the same format and a declaring spec moves its digest, the measurement (neutral registry; two
  hand-built specs and a third, declaring, in the two wheels), and that the recipe is
  RunRegistryKit's, whose text is that repository's to amend; the checklists not re-measured (U37).
- **SGK** and **CPBH**: the pin (`v0.4.0`, adopted, or `v0.5.0`); a `###` section "What a move to
  `v0.5.0` changes for SGK" (CPBH) with: nothing the client calls (its `InventorySpec`, `Record`,
  `read_records` and `value_count` sites); no record or fingerprint moves at its format (6, 3);
  item 8; the guard fails, with the guard's `path:line`s; **the format is not bumped for this**,
  with the client's own rule cited; **the edit**, one condition in `plain`, shown as code, and the
  guard's other tests it leaves alone; and one **Advice:**, to make the edit in the commit that
  moves the pin and run the guard before and after it. G2's (G3's) reading and holding stand.
- **SI**: the note SI's pin prompt reads: the pin (`v0.5.0` in place of `v0.4.0`); nothing SI calls
  changes; `### What SI declares, and where` (the keyword, beside `values=`, with the foreign key);
  `### What then holds` (counts, 0 where none; `orphan-value`; `KeyError` for a missing table or
  column; the refusal; SI's fingerprints of the class, none recorded); `### What of SI's own moves`
  (the coverage test's `EXCLUDED`, `READ_THROUGH`/`SLOTS`/`_slot_tables` and its counts; `_as_table`
  and the column test; the report; the spec's comment; the issue SI holds), with one **Advice:**
  (if SI adds a spec guard, use the recipe with the condition); `### Where this release departs
  from SI's brief`, README §0.2's five points. G4 reads as before and is not recorded here.

The shifts, as each addendum states them (correction 1):

| File | Lines added | Lines removed | Head inserted after (at `c8570e8`) | N | k | the `v0.4.0` addendum's | `v0.3.0`'s | `v0.2.3`'s | `v0.2.2`'s | `v0.2.1`'s | the appendix |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `docs/adoption/README.md` | 162 | 0 | `:31` | **5** | 5 | **5** | **10** | **15** | **20** | **25** | — (the addendum is at the end) |
| `docs/adoption/secondarygwkit.md` | 161 | 0 | `:44` | **6** | 6 | **6** | **12** | **18** | **24** | **30** | **161** (N + 155) |
| `docs/adoption/champbh.md` | 153 | 0 | `:45` | **6** | 6 | **6** | **12** | **18** | **24** | **30** | **153** (N + 147) |
| `docs/adoption/stochasticinstantons.md` | 181 | 0 | `:43` | **6** | 6 | **6** | **12** | **18** | **24** | **30** | **181** (N + 175) |

The citations above the insert, which do not shift, are named in each addendum: README `:22-25`
(and `:17-20`, `:12-15`, `:7-10`, `:3` for the earlier ones), SGK `:33-37` (`:27-31`, `:21-25`,
`:16-19`, `:6`), CPBH `:34-38` (`:28-32`, `:22-26`, `:17-20`, `:6`), SI `:32-36` (`:26-30`,
`:20-24`, `:15-18`, `:5`). Checked line by line (§5.7): 816 cited lines, 0 differ.

### 1.5 The extraction board's gate (§2.5)

`prompts/extraction/IMPLEMENTATION_STATE.md` §2, row G4 (`:1539`), and nothing else on that board
(`git diff --numstat`: 1/1). Its status cell gains, at its end, one dated italic sentence: "*(2026-10-21:
`v0.5.0` is ready to be tagged on `extra-values` prompt 02's commit once CI passes there at both
ends, as U23 and U28; 02 makes no tag and pushes nothing. SI adopts `v0.5.0` (`extra-values` U5).
SI's addendum is [link to its `v0.5.0` anchor].)*". `git diff --word-diff` shows only the appended
sentence. The title is unchanged (G4's reading, "`v0.3.0` or later", admits `v0.5.0`). G1, G2 and
G3 (`:1536-1538`) are unchanged.

### 1.6 The issue (§2.6) and the records

- `[01-a-new-spec-field-moves-every-spec-guard-digest]` moved, whole, from the board's §3 to §4,
  with a `**Closed (2026-10-21, 02):**` line naming the SGK and CPBH addenda (by anchor), the README
  addendum's "The spec guard", and the release check that probes it (§5.3); §3 says "None open.".
- `docs/OPEN_ISSUES.md`: the row deleted; §1.4 says "None open (2026-10-21: … closed by
  `extra-values` prompt 02)."; the header **4 open**, all on this repository's boards (§1.2), last
  updated 2026-10-21.
- This log; the board's header, §1's row for 02 (landed, "this commit", log) and a note for 02;
  the campaign README's header and §2's row for 02; `prompts/INDEX.md`'s line for the campaign.

---

## 2. Deviations from the prompt

1. **Correction 1: the earlier addenda's citations, with numbers.** Each italic line goes after the
   `v0.4.0` italic line's blank (after README `:31`, SGK `:44`, CPBH `:45`, SI `:43`), and each
   addendum states the `v0.4.0` addendum's shift N and every earlier one as a number (§1.4's
   table): 5, 10, 15, 20, 25 in the README; 6, 12, 18, 24, 30 in each checklist, with the
   citations above the insert named. Checked line by line (§5.7). **STRUCTURALLY REQUIRED.**
2. **The appendix's own offset**, beyond correction 1. In a checklist the new addendum goes before
   the appendix, so an appendix line moves by N and the addendum's own length, not by N. The
   `v0.4.0` SGK addendum cites appendix rows (`:1230-1232` at `c8570e8`, now `:1391-1393`, 161 lines
   later). Each checklist addendum says so, with its number (SGK 161, CPBH 153, SI 181); only SGK's
   `v0.4.0` addendum cites one. Without it, correction 1's rule would misread those three lines.
   **STRUCTURALLY REQUIRED.**
3. **Correction 2: the `v0.4.0` addenda's pin statements are history.** Each is superseded by
   `path:line` with the pin read at §1.1's commit and the commit that set it (SGK `5b81f2e`, CPBH
   `f41b104`, SI `1b1ca6d`, each by `git log -S'DatastoreKit@v0.4.0' -- requirements.txt`): SGK
   `:752-760` ("SGK's `requirements.txt:17` pins `v0.2.2`", correction 2's `:754`) and `:905`
   (correction 2's `:899`); CPBH `:724-737` ("pins it at `2792a85`", correction 2's `:719`); SI
   `:699-712` ("SI's tree at `5fb4a1d` has no `datastorekit` line"); README `:678-680` (the "Its
   pin" column). SGK's `v0.4.0` account of what changes when SGK calls the package's functions
   (`:798-899`) **stands**, named in SGK's "Standing" paragraph, not re-measured.
   **STRUCTURALLY REQUIRED.**
4. **Beyond the prompt's table**, found by its rule (§2.4's grep) and recorded as found. Each is in
   its file's table. **STRUCTURALLY REQUIRED.**
   - README `:641-642`, in part: "`datastorekit/store_inventory.py` … is unchanged since `v0.2.2`",
     untrue of `v0.5.0`.
   - README `:658-659`, in part: "A digest a client takes with its own code does not move: what it
     reads from the package is unchanged", untrue of a spec guard under `v0.5.0`.
   - SGK `:783-788` and the row `:906`, in part: `store_inventory.py`, "which no release since
     `v0.2.2` has changed", and "every digest and count SGK's code takes is as at `v0.2.2`".
   - In each file, the `v0.4.0` table's rows that give a shift ("five lines later here" and the
     like), which this insert moves by N, and the rows that point at a superseded row ("as
     `:491-506`"), so that every row whose replacement text is no longer true is named.
5. **Correction 3: the release check, measured.** As the correction gives: (b) 79 entries, 53 under
   `datastorekit/tests/`; (c) 26 entries, `Version: 0.5.0`, no `RECORD` line differing or added.
   The constraints file: the cache now holds a `datastorekit` 0.5.0 `.dist-info` as well as
   0.4.0's (left by the planner's or orchestrator's probes), so a file of the highest cached
   versions names `datastorekit==0.5.0`, not a line that refuses `0.5.0`; I left the line out
   regardless, with `ray` and `sqlalchemy`'s (which conflict with the pins asked for), and did not
   reproduce the refusal (§7 item 4). Each wheel installed is the one built here, by path.
   Recorded as found.
6. **The orchestrator's additions**, each an **IMPLEMENTATION CHOICE** at the orchestrator's
   direction:
   - **the order of work**: the baseline (538, port check, `black`, the clients and
     RunRegistryKit, Ray); §1.1's measure; the release check and its breakages; the documents
     (§2.2–§2.6); the reinstall and the suite at both ends; the records. One variation: §2.1
     (`pyproject.toml`) was made first, so that the release check's export (`git stash create`,
     `79294bf`) is this tree's `pyproject.toml` and `datastorekit/`, before any document was
     written;
   - **the probe kept whole in the log**, with its output from both venvs (§5.3); its guard check
     copies RunRegistryKit's `plain` and `spec_digests` from `git show v0.2.0:docs/adoption/README.md`,
     adds the condition as a separate function, `plain_with_condition`, and asserts both outcomes;
   - **the clients' `plain` quoted from `git show`** at `031bcb4` and `7055532`, and compared with
     the recipe (§5.5): by `ast`, docstrings removed, each client's `plain` and `spec_digests` are
     the recipe's; the text differs in the docstring and in `black`'s wrapping of one dict
     comprehension;
   - **the anchors**, derived by GitHub's rule (§3 item 2).
7. **The probe goes beyond §1.2 in three checks**, each in the assertion's output (§5.3): that the
   condition changes nothing under `v0.4.0`; that a third hand-built spec, declaring an extra
   table, moves its digest with the condition and leaves the other's; and the neutral-registry
   measure of §1.1, run in each export with the export's own `datastorekit` (`<scratch>/probe/neutral_guard.py`,
   §5.3), not only in the wheels. **IMPLEMENTATION CHOICE.**
8. **"The format is not bumped for this" is stated as a fact, not as advice.** The prompt's table
   gives it as "**Do not bump it for this**"; hazard 9 asks that what is recommended be marked
   **Advice:**. Each addendum states that the specs did not change, which is what the client's own
   rule for a bump names (SGK `config/fingerprint.py:51-59`, CPBH `:79-80`), and what a bump would
   move. The one recommendation, to make the edit with the pin and run the guard before and after,
   is marked **Advice:**. **IMPLEMENTATION CHOICE.**
9. **The SGK and CPBH addenda show the condition as code**, and name the guard's other tests that it
   leaves alone (SGK `test_a_key_keeps_its_type`; CPBH `test_the_pin_has_one_pair_per_class_with_a_spec`,
   `test_a_key_keeps_its_type` and `test_a_parent_keyed_by_an_int_keeps_its_type`, whose `asdict`
   calls are on a `Parent`). Each read through `git show`. **IMPLEMENTATION CHOICE.**
10. **SI's addendum names more of SI's own code than the prompt lists**: `READ_THROUGH` and the
    `SLOTS` check beside `_slot_tables`; `_as_table` (`:283-297`), which
    `test_each_spec_is_the_identity_its_build_matches` compares with `EXPECTED_SPECS`, and the
    `values` check of `test_every_named_column_is_a_column_of_its_table` (`:351-358`), neither of
    which sees `extra_values`; and the spec's comment (`:152-155`). Each read through `git show`,
    named and none chosen. **IMPLEMENTATION CHOICE.**
11. **"Pool", not "layer", in "nothing … writes or reads changes"** (README status, the README and
    SI addenda, item 8 in SGK's and CPBH's), as contract §9.8 words it: the inventory reads a
    further table where a spec declares one. **IMPLEMENTATION CHOICE.**
12. **README's "What changed after `v0.2.0`"**: to add `v0.5.0`'s change, "; and the change of
    `v0.4.0`" became "; the change of `v0.4.0`", the "and" moving to `v0.5.0`'s. The README is not
    additive-only. **IMPLEMENTATION CHOICE.**
13. **The release check of record is a second export.** I built the release first from
    `git archive 79294bf` (`git stash create` after §2.1 only), ran the check and the breakages on
    it, then again, after every document and record but this log, from `983119f` (`git stash
    create`; `git diff --quiet 983119f` held; `git stash list` stayed empty). The two wheels'
    `RECORD`s are byte-equal (SHA-256 `8fc18a57…c0bf`). §5.3 reports the second. **IMPLEMENTATION
    CHOICE.**
14. **The board's issue is moved whole to §4** with its `**Closed**` line, and §3 says "None open.";
    the index's §1.4 says "None open (…)", in the form of its §1.1 and §1.3. **IMPLEMENTATION
    CHOICE.**

No deviation is UNINTENDED DRIFT.

---

## 3. The hazards (§3)

1. **Additive documents.** `git diff --numstat -- docs/adoption` gives 162/0, 161/0, 153/0 and
   181/0, and `git diff -- docs/adoption | grep '^-' | grep -v '^--- '` finds nothing. Each
   insertion was made by `<scratch>/probe/insert.py`, which adds lines only, after checking the line
   before and after the insert point. One later edit changed only lines this prompt had added
   (SGK's italic line, reworded within its five lines). `docs/client-contract.md` and
   `docs/extraction-verification.md` are unchanged. (`docs/OPEN_ISSUES.md` loses the closed row,
   as §2.6 and `CLAUDE.md` require.)
2. **Names and links.** Every one resolves (§5.6). The contract anchor, by GitHub's rule: "9.8
   `extra-values` prompt 01" (`docs/client-contract.md:391`), lower-cased, every character that is
   not a letter, digit, space, hyphen or underscore dropped (the `.` and the backticks), spaces made
   hyphens, is `98-extra-values-prompt-01`. Each new heading, "Addendum: v0.5.0 (extra-values
   prompt 02, 2026-10-21)", the same way (the `:`, the `.`s, `(`, `)` and `,` dropped), is
   `addendum-v050-extra-values-prompt-02-2026-10-21`. The script derives every heading's slug that
   way and finds each anchor among them.
3. **The tag does not exist yet.** No document says `v0.5.0` is tagged: the README and the addenda
   state the pins, and the README says `v0.4.0` to `v0.1.0` "remain tagged"; G4's sentence says
   `v0.5.0` "is ready to be tagged … once CI passes there at both ends", and that 02 makes no tag.
4. **No client is re-measured beyond §1.1.** I re-ran §1.1's measure with a script of my own
   (§5.4), at the commits §1.1 names, which are the `HEAD`s I read. It reproduces the table. No
   client passes `extra_values`, builds a `Record` positionally, or walks a spec's fields anywhere
   but its guard: no stop. Every client citation an addendum makes was read with `git show
   <commit>:<path>` before it was written (§5.5).
5. **The guard's edit is shown, not run on a client.** On the neutral registry, in an export of
   `v0.4.0` and of this tree, and on hand-built specs in the two installed wheels (§5.3). The
   clients' `plain` was read through `git show` and compared with the recipe (§5.5); no client
   module was imported.
6. **Offline only.** Every venv (`uv venv --offline`), install (`uv pip install --offline`) and
   build (`uv build --offline`) resolved from the cache: `setuptools` 84.0.0 (the build backend),
   `ray` 2.55.1 and `sqlalchemy` 2.0.46, under a constraints file made from the cache
   (`<scratch>/constraints-hi.txt`, 64 lines, `ray`, `sqlalchemy` and `datastorekit` left out).
   Nothing was downloaded.
7. **`venv/`'s metadata.** After §2.1, `pip show` said `0.4.0`. `uv pip install --offline --no-deps
   --python venv/bin/python -e .`, from the repository root, without `--no-build-isolation`
   (`import setuptools` fails in `venv/`): `- datastorekit==0.4.0`, `+ datastorekit==0.5.0`, exit
   0. It wrote `datastorekit.egg-info/`, which I deleted at once. `pip show` then gives
   `Version: 0.5.0`, editable from this checkout; `importlib.metadata.version` is `0.5.0`. The
   suite in `venv/` gives 538 OK after it.
8. **No Ray.** The probes build specs, records and an inventory by hand and run `sharded_store
   --help`; `ray` is not in `sys.modules` after them, and the name check's `ray.is_initialized()`
   is `False`. At the start and the end no Ray process was up (`pgrep -lf
   'gcs_server|raylet|ray::|default_worker\.py'` empty), `RAY_ADDRESS` and
   `RAY_ENABLE_AUTO_CONNECT` were unset, and there was no `/tmp/ray/ray_current_cluster`.
9. **U5's wording.** "May stay or move" is permission throughout (README `:122-125`; the README,
   SGK and CPBH addenda and head lines). Nothing says SGK or CPBH should or should not move. The
   guard's edit is stated as what a move needs; the two recommendations are marked **Advice:**
   (SGK's and CPBH's: make the edit with the pin and run the guard before and after; SI's: if it
   adds a guard, use the recipe with the condition).
10. **Run from the right place.** Every scratch-venv command ran with its export or
    `<scratch>/outside` as the working directory, `PYTHONPATH` unset. `datastorekit.__file__`:
    `venv/`, `<repo>/datastorekit/__init__.py` (editable, as intended); `venv-high`, its export's
    `datastorekit/__init__.py`; `venv-release1`, `venv-release2`, `venv-v040` and each breakage's
    venv, its `site-packages/datastorekit/__init__.py`; the neutral-registry measure, each export's
    own `datastorekit/__init__.py`.
11. **The package names no client.** Nothing under `datastorekit/` changed; the guards pass in
    every suite run.

---

## 4. The supersession tables

Each is as committed in its addendum; the line numbers are each file's as committed with it.
Rather than repeat them here, the four tables are in the files: README `:869-891`, SGK
`:1085-1108`, CPBH `:922-940`, SI `:929-945`, each followed by its "Standing, not superseded"
paragraph. In summary:

| File | Superseded, by `path:line` | Standing, named |
|---|---|---|
| `README.md` | `:27-30` (head line, in part); `:618-634` (pins, in part); `:636-637` (carries); `:641-642` and `:658-659` (in part, §2 item 4); `:678-680` (the pin column); `:705-717` (shift paragraph); rows `:721-734` | G2's, G3's and G4's readings and their row (`:735`); the account of `store_fingerprint` (`:639-667`); the clients' fingerprint functions as read then (`:669-690`); the "Standing" paragraph (`:737-742`); the module map (`:96-100`) |
| `secondarygwkit.md` | `:39-43` (head line); `:752-760` (pin, in part); `:762-763`; `:783-788` (in part); rows `:905`, `:906`; `:923-935` (shift paragraph); rows `:939-953` | G2's reading and holding (`:759-760`, rows `:940`, `:944`); "What changes when SGK calls the package's functions" (`:798-899`); the rest of "What moving the pin changes" (`:775-796`); the "Standing" paragraph (`:955-961`) |
| `champbh.md` | `:40-44`; `:724-737` (in part); `:739-740`; `:766-778`; rows `:782-794` | G3's reading and holding (`:724-727`, rows `:783`, `:787`); "What changed for CPBH since `v0.3.0`" (`:742-758`); the "Standing" paragraph (`:796-799`) |
| `stochasticinstantons.md` | `:38-42`; `:699-712` (in part); `:714-715`; `:744-757`; rows `:761-771` | G4's reading (`:699-701`, rows `:762`, `:772`); "What changed for SI since `v0.3.0`" (`:717-735`); the "Standing" paragraph (`:774-778`) |

**Considered and not superseded.** The grep of §2.4 (`v0.4.0`, `requirements.txt`, `value_count`,
`InventorySpec`, `five addenda`, `RunRegistryKit`) outside the new addenda finds, besides the
tabled lines:
- README `:62`, `:76`, `:81-83` (the pins' rule and 07a's measured `requirements.txt` lines of each
  client's Ray and SQLAlchemy), `:142` (§4's table naming `InventorySpec`, `Parent`, `ParentSet`,
  07a's at `v0.2.0`; contract §4 still holds and §9.8 adds a row), `:566` (SGK's pin as read by the
  `v0.2.3` addendum), and `:690` (CPBH and SI "meet the module only when they adopt
  RunRegistryKit", a condition; §7 item 3): history or true;
- SGK `:74-75`, `:116`, `:216`, `:383`, `:612`, `:659`, the appendix's `InventorySpec` rows: 07a's
  and the earlier addenda's facts of SGK at their commits;
- CPBH `:75`, `:107`, `:300`: facts of CPBH at `52142d7`; `:755-756`, "It meets the module only
  when it adopts RunRegistryKit", named in CPBH's "Standing";
- SI `:70-71`; `:730-731`, the same condition, named in SI's "Standing";
- in each file, the earlier addenda's `four addenda`, `five addenda` and pin statements other than
  those tabled: history true of their release.

---

## 5. Verification performed

### 5.1 The suite (§4.1)

Every run in the foreground, its output in `<scratch>/out/`, the verdict grepped from it.

| Where | When | Result | `ResourceWarning` lines | `datastorekit` |
|---|---|---|---|---|
| `venv/` (3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39, SQLite 3.53.4) | at the start, before any change | `Ran 538 tests in 107.299s` `OK` | 0 | 0.4.0 |
| `venv/` | after `pyproject.toml` and the reinstall | `Ran 538 tests in 101.701s` `OK` | 0 | 0.5.0 |
| `<scratch>/venv-high` (3.13.16 / 2.55.1 / 2.0.46, SQLite 3.53.4, `setuptools` 84.0.0), `git archive d8a497c` (every document of `f47b9a2`'s but the records) installed editable `--no-deps --no-build-isolation` | after the documents | `Ran 538 tests in 100.415s` `OK` | 4 | 0.5.0 |
| `venv/` | after the records, before the commit | `Ran 538 tests in 103.366s` `OK` | 0 | 0.5.0 |

The count is **538** before and after, at both ends. The four high-end lines are two warnings,
unclosed SQLite connections reported from SQLAlchemy (`sql/type_api.py` and `sql/selectable.py:3160`),
each with its tracemalloc hint: timing (the note's facts; `actor-names` log 01, correction 8).
`datastorekit/` at `d8a497c` is `f47b9a2`'s.

### 5.2 The checks (§4.2)

- `compare_ported_tests.py`, before and after, exit 0, its last line: `OK: 20 module(s) keep their
  source's tests, classes and assertion skeletons; 1 test(s) declared not ported`.
- `./venv/bin/black --check datastorekit docs` (black 25.1.0), before and after: `79 files would be
  left unchanged.` No `.py` file changed.
- The guards (`test_layer_is_generic`, `test_prose_names_no_source`, `test_package_imports`) are
  in the suite and pass in every run above.

### 5.3 The release check (§4.3)

**The build.** `git archive 983119f | tar -x -C <scratch>/exports/release2` (§2 item 13), then
`uv build --offline --wheel --out-dir <scratch>/wheels/release2 <scratch>/exports/release2`, exit 0.
For the comparison, `git archive v0.4.0` (`c8570e8`) into `<scratch>/exports/v040`, built the same
way. Nothing was built in the checkout.

| | The release | `v0.4.0`'s, for comparison |
|---|---|---|
| Wheel | `datastorekit-0.5.0-py3-none-any.whl` | `datastorekit-0.4.0-py3-none-any.whl` |
| Size | 105,087 bytes | 104,424 bytes |
| Entries | **26**: none under `datastorekit/tests/` | 26 |
| SHA-256 | `552f72f954ef17d785f5e925ee9f0ea6717809a97d8a31c5b7808d363c94d81d` (the first build, from `79294bf`: `df2e829fae2219e6efa17c8f61ef6565b5828997adfa49affc405caa52d01cbe`) | `dff06c33f64990fd3415fe98daf194654bce841ed94cadffaf4b18252106600f` |
| `RECORD` SHA-256 | `8fc18a5774ca472fa059654e55d815bcfbfa3840c9e00af23c40d4ae566ec0bf`, both builds | `c418fd39978cb3b25bb02ea0daa073aa19b8f86b2fe9d8f41d35d264ff13d5f6`, as `fingerprint` log 02's release (§5.3) |
| `METADATA` | `Version: 0.5.0`, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43`, `Requires-Dist: sqlalchemy<2.1,>=2.0.39` | `Version: 0.4.0`, the rest the same |

The sizes equal the planner's. The wheel's bytes are not reproducible across builds; only its
SHA-256 is mine to record.

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
datastorekit-0.5.0.dist-info/licenses/LICENSE
datastorekit-0.5.0.dist-info/METADATA
datastorekit-0.5.0.dist-info/WHEEL
datastorekit-0.5.0.dist-info/top_level.txt
datastorekit-0.5.0.dist-info/RECORD
```

**The `RECORD` comparison**, `v0.4.0`'s wheel against the release: 21 lines under `datastorekit/`
in each, the same paths; 19 equal, none missing or added, two differing:

```
datastorekit/store_fingerprint.py,sha256=enGZPLYaYQFvoR3LSCJYTk8DtYQRK0eU_97Nb43nzm4,16492   (v0.4.0: …OIGFxRU6…,16093)
datastorekit/store_inventory.py,sha256=DJgAqZr-5LH_4ME69rtdSstFhAHdC8uSlkVUvaK5uE0,47280    (v0.4.0: …4PJPPpQe…,45013)
```

the prompt's lines, to the byte.

**The install.** Each wheel into its own `uv venv --offline -p /opt/local/bin/python3.13`
(`<scratch>/venv-release2`, `<scratch>/venv-v040`), with `uv pip install --offline -c
<scratch>/constraints-hi.txt --python <venv>/bin/python <the wheel> "ray==2.55.1"
"sqlalchemy==2.0.46"`, exit 0, not editable. Python 3.13.16, SQLite 3.53.4.

**The probe**, `<scratch>/probe/release_probe.py` (SHA-256 `c2f82e83…4026`), run as `python -I`
from `<scratch>/outside` with `PYTHONPATH` unset, in each venv. It prints one JSON object of what it
read; **`<scratch>/probe/assert_release.py <wheel> <venv python> <v0.4.0's wheel> <v0.4.0's venv
python> 0.5.0 <scratch>/outside`** reads both wheels, runs the probe in both venvs, runs three
fresh interpreters in the release's venv (`import datastorekit.store_inventory` then `'ray' in
sys.modules`; `import datastorekit.tests`; `-m datastorekit.tools.sharded_store --help`), and
prints PASS or FAIL per check. The probe, whole:

```python
"""extra-values prompt 02's release probe. Run as `python -I release_probe.py` in a venv with a
datastorekit wheel installed, from a directory outside the repository, PYTHONPATH unset. It prints
one JSON object of what it read; `assert_release.py` compares two venvs' objects.

Everything is built by hand from the package's public names; no store is opened, and nothing of
any client is imported. The guard's recipe is RunRegistryKit's `docs/adoption/README.md` §6 at its
`v0.2.0` (`plain` and `spec_digests`, copied verbatim, the docstring shortened); the one condition
is a separate function, `plain_with_condition`.
"""

import dataclasses
import hashlib
import importlib.metadata
import json
import sys
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path

import datastorekit
from datastorekit.store_fingerprint import ENCODING_FORMAT, fingerprint_of
from datastorekit.store_inventory import (
    ClassInventory,
    InventorySpec,
    Parent,
    Record,
    StoreInventory,
    canonical_json,
    inventory_classes,
    inventory_specs,
)


# --- RunRegistryKit v0.2.0, docs/adoption/README.md §6, "The sketch" (verbatim) ---------------
def plain(value):
    """A spec as JSON (RunRegistryKit's recipe)."""
    if dataclasses.is_dataclass(value):
        return {f.name: plain(getattr(value, f.name)) for f in dataclasses.fields(value)}
    if isinstance(value, Mapping):
        return {json.dumps(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    return value


def spec_digests(factories) -> list:
    """[class, SHA-256 of its spec's canonical JSON] for each spec, in registry order."""
    return [
        [name, hashlib.sha256(canonical_json(plain(spec)).encode()).hexdigest()]
        for name, spec in inventory_specs(factories).items()
    ]


# --- the one condition: leave out a field named extra_values whose value is empty -------------
def plain_with_condition(value):
    if dataclasses.is_dataclass(value):
        return {
            f.name: plain_with_condition(getattr(value, f.name))
            for f in dataclasses.fields(value)
            if not (f.name == "extra_values" and len(getattr(value, f.name)) == 0)
        }
    if isinstance(value, Mapping):
        return {json.dumps(k): plain_with_condition(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain_with_condition(v) for v in value]
    return value


def spec_digests_with_condition(factories) -> list:
    return [
        [
            name,
            hashlib.sha256(
                canonical_json(plain_with_condition(spec)).encode()
            ).hexdigest(),
        ]
        for name, spec in inventory_specs(factories).items()
    ]


class Factory:
    """A stand-in factory: an `inventory_spec` hook that builds its spec when called."""

    def __init__(self, make):
        self._make = make

    def inventory_spec(self):
        return self._make()


def two_specs():
    """Two hand-built specs, neither declaring an extra table: one with a tag table, a value
    table and `validated`; one with a parent and a polymorphic parent keyed by `int`."""
    return {
        "Alpha": Factory(
            lambda: InventorySpec(
                leaves=("x", "y"),
                tags=("Alpha_tags", "alpha_serial"),
                values=("AlphaValue", "alpha_serial"),
                validated="validated",
            )
        ),
        "Beta": Factory(
            lambda: InventorySpec(
                leaves=("z", "kind"),
                parents={
                    "alpha": Parent("alpha_serial", of="Alpha"),
                    "thing": Parent(
                        "thing_serial", type_column="kind", types={0: "Alpha", 1: "Alpha"}
                    ),
                },
            )
        ),
    }


def main():
    out = {}
    out["file"] = datastorekit.__file__
    out["version"] = importlib.metadata.version("datastorekit")
    out["encoding_format"] = ENCODING_FORMAT
    out["spec_fields"] = [f.name for f in dataclasses.fields(InventorySpec)]
    out["record_fields"] = [f.name for f in dataclasses.fields(Record)]
    out["keywords"] = sorted(InventorySpec().keywords())

    # a record built without counts, and (where the field exists) one with
    bare = Record(key={"a": 1, "b": "x"}, tags=("t1",), validated=True, value_count=3)
    out["bare_keys"] = list(bare.as_json())
    out["bare_canonical"] = bare.canonical_json()
    try:
        counted = Record(
            key={"a": 1, "b": "x"},
            tags=("t1",),
            validated=True,
            value_count=3,
            extra_value_counts={"T2": 0},
        )
        out["counted_keys"] = list(counted.as_json())
        out["counted_canonical"] = counted.canonical_json()
        out["counted_hash"] = isinstance(hash(counted), int)
        out["counted_in_set"] = len({counted, counted}) == 1
    except TypeError as e:
        out["counted_error"] = f"TypeError: {e}"

    # a hand-built inventory, as fingerprint 02's probe built one
    alpha = ClassInventory(
        name="Alpha",
        replicated=True,
        tagged=True,
        parents={},
        records=(
            Record(key={"x": 1, "y": "one"}, tags=("t1",), validated=True, value_count=2),
            Record(key={"x": 2, "y": "two"}, tags=(), validated=False, value_count=0),
        ),
        count=2,
        earliest_timestamp=datetime(2026, 10, 1, 12, 0, 0),
        latest_timestamp=datetime(2026, 10, 2, 12, 0, 0),
        problems=("orphan-tag: Alpha_tags on shard 0: 1 row(s) name no Alpha",),
    )
    beta = ClassInventory(
        name="Beta",
        replicated=False,
        tagged=False,
        parents={"alpha": "Alpha"},
        records=(),
        count=0,
        earliest_timestamp=None,
        latest_timestamp=None,
        problems=(),
    )
    inv = StoreInventory(
        primary=Path("/nonexistent/primary.sqlite"),
        shards=(0, 1),
        classes={"Alpha": alpha, "Beta": beta},
    )
    fp = fingerprint_of(inv, 1)
    out["fingerprint_digest"] = fp["digest"]
    out["fingerprint_keys"] = sorted(fp)
    out["fingerprint_classes"] = canonical_json(fp["classes"])

    # the guard's recipe over two hand-built specs, plain and with the one condition
    registry = two_specs()
    out["guard_plain"] = spec_digests(registry)
    out["guard_condition"] = spec_digests_with_condition(registry)
    out["guard_plain_alpha"] = canonical_json(plain(registry["Alpha"].inventory_spec()))

    # a spec that declares an extra table moves its digest, with the condition (release only)
    try:
        declaring = {
            "Alpha": Factory(
                lambda: InventorySpec(
                    leaves=("x", "y"),
                    tags=("Alpha_tags", "alpha_serial"),
                    values=("AlphaValue", "alpha_serial"),
                    validated="validated",
                    extra_values={"AlphaNote": "alpha_serial"},
                )
            ),
            "Beta": registry["Beta"],
        }
        out["guard_condition_declaring"] = spec_digests_with_condition(declaring)
    except TypeError as e:
        out["guard_condition_declaring"] = f"TypeError: {e}"

    # the one new refusal, in inventory_classes only
    try:
        refused = {
            "Alpha": Factory(
                lambda: InventorySpec(
                    leaves=("x",),
                    values=("AlphaValue", "alpha_serial"),
                    extra_values={"AlphaValue": "alpha_serial"},
                )
            )
        }
        try:
            out["refusal_specs"] = sorted(inventory_specs(refused))
        except Exception as e:
            out["refusal_specs"] = f"{type(e).__name__}: {e}"
        try:
            out["refusal_classes"] = inventory_classes(refused)
        except Exception as e:
            out["refusal_classes"] = f"{type(e).__name__}: {e}"
    except TypeError as e:
        out["refusal_specs"] = out["refusal_classes"] = f"TypeError: {e}"

    out["ray_after"] = "ray" in sys.modules
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
```

Its output, in the release's venv and in `v0.4.0`'s (`<scratch>/out/probe-both.txt`):

```
release2 {"file": "<scratch>/venv-release2/lib/python3.13/site-packages/datastorekit/__init__.py","version": "0.5.0","encoding_format": 1,"spec_fields": ["leaves","parents","tags","values","validated","parent_sets","extra_values"],"record_fields": ["key","tags","validated","value_count","extra_value_counts"],"keywords": ["extra_values","leaves","parent_sets","parents","tags","validated","values"],"bare_keys": ["key","tags","validated","value_count"],"bare_canonical": "{\"key\":{\"a\":1,\"b\":\"x\"},\"tags\":[\"t1\"],\"validated\":true,\"value_count\":3}","counted_keys": ["key","tags","validated","value_count","extra_value_counts"],"counted_canonical": "{\"extra_value_counts\":{\"T2\":0},\"key\":{\"a\":1,\"b\":\"x\"},\"tags\":[\"t1\"],\"validated\":true,\"value_count\":3}","counted_hash": true,"counted_in_set": true,"fingerprint_digest": "d493e0fe207d8e2175ce1b17fcf33801ee47a183d22a0783527647451f87f754","fingerprint_keys": ["classes","digest","encoding_format","fingerprint_format","problems","taken"],"fingerprint_classes": "{\"Alpha\":{\"count\":2,\"digest\":\"31e8a93d7d5138278d2e0eb6f4d6ace05a38b4466b81732b2fd124e7049cf7b6\",\"tag_sets\":[{\"count\":1,\"digest\":\"10c350ed868d618bac2a953951e2abb878ab7adf05872d94fd03d5ad035b6f4a\",\"tags\":[]},{\"count\":1,\"digest\":\"f9fe06f2219a26abe5b60688bf0f85f18166a7543382e2c1272532af13aa44e4\",\"tags\":[\"t1\"]}]},\"Beta\":{\"count\":0,\"digest\":\"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\",\"tag_sets\":[]}}","guard_plain": [["Alpha","b08c7c511ca3ed79b2437635d99cc22ddce4b513d80ed4a2f278a484380d4ee9"],["Beta","97d99c396701e98dfdcd0a61bf957573fa853dee067f5226e6dfa6b58839e268"]],"guard_condition": [["Alpha","a80feec45b6e85ff368216da57c3e2f69e3c819c492e8aa76f3395a1105dd403"],["Beta","496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116"]],"guard_plain_alpha": "{\"extra_values\":{},\"leaves\":[\"x\",\"y\"],\"parent_sets\":{},\"parents\":{},\"tags\":[\"Alpha_tags\",\"alpha_serial\"],\"validated\":\"validated\",\"values\":[\"AlphaValue\",\"alpha_serial\"]}","guard_condition_declaring": [["Alpha","ff2df82d76226fc9c0d27389d7a1a34d60d434d0e50644bd09504b10ae68afcb"],["Beta","496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116"]],"refusal_specs": ["Alpha"],"refusal_classes": "ValueError: inventory_classes(): Alpha names AlphaValue both as its value table and in its extra_values","ray_after": false}
v040 {"file": "<scratch>/venv-v040/lib/python3.13/site-packages/datastorekit/__init__.py","version": "0.4.0","encoding_format": 1,"spec_fields": ["leaves","parents","tags","values","validated","parent_sets"],"record_fields": ["key","tags","validated","value_count"],"keywords": ["leaves","parent_sets","parents","tags","validated","values"],"bare_keys": ["key","tags","validated","value_count"],"bare_canonical": "{\"key\":{\"a\":1,\"b\":\"x\"},\"tags\":[\"t1\"],\"validated\":true,\"value_count\":3}","counted_error": "TypeError: Record.__init__() got an unexpected keyword argument 'extra_value_counts'","fingerprint_digest": "d493e0fe207d8e2175ce1b17fcf33801ee47a183d22a0783527647451f87f754","fingerprint_keys": ["classes","digest","encoding_format","fingerprint_format","problems","taken"],"fingerprint_classes": "{\"Alpha\":{\"count\":2,\"digest\":\"31e8a93d7d5138278d2e0eb6f4d6ace05a38b4466b81732b2fd124e7049cf7b6\",\"tag_sets\":[{\"count\":1,\"digest\":\"10c350ed868d618bac2a953951e2abb878ab7adf05872d94fd03d5ad035b6f4a\",\"tags\":[]},{\"count\":1,\"digest\":\"f9fe06f2219a26abe5b60688bf0f85f18166a7543382e2c1272532af13aa44e4\",\"tags\":[\"t1\"]}]},\"Beta\":{\"count\":0,\"digest\":\"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\",\"tag_sets\":[]}}","guard_plain": [["Alpha","a80feec45b6e85ff368216da57c3e2f69e3c819c492e8aa76f3395a1105dd403"],["Beta","496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116"]],"guard_condition": [["Alpha","a80feec45b6e85ff368216da57c3e2f69e3c819c492e8aa76f3395a1105dd403"],["Beta","496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116"]],"guard_plain_alpha": "{\"leaves\":[\"x\",\"y\"],\"parent_sets\":{},\"parents\":{},\"tags\":[\"Alpha_tags\",\"alpha_serial\"],\"validated\":\"validated\",\"values\":[\"AlphaValue\",\"alpha_serial\"]}","guard_condition_declaring": "TypeError: InventorySpec.__init__() got an unexpected keyword argument 'extra_values'","refusal_specs": "TypeError: InventorySpec.__init__() got an unexpected keyword argument 'extra_values'","refusal_classes": "TypeError: InventorySpec.__init__() got an unexpected keyword argument 'extra_values'","ray_after": false}
```

The assertions:

```
wheel sha256: 552f72f954ef17d785f5e925ee9f0ea6717809a97d8a31c5b7808d363c94d81d  size: 105087
PASS wheel name: datastorekit-0.5.0-py3-none-any.whl
  METADATA: ['Version: 0.5.0', 'Requires-Python: >=3.12', 'Requires-Dist: ray>=2.43', 'Requires-Dist: sqlalchemy<2.1,>=2.0.39']
PASS METADATA Version: Version: 0.5.0
PASS no entry under datastorekit/tests/: 0 of 26 entries
PASS 26 entries: 26
PASS RECORD against v0.4.0: store_inventory.py and store_fingerprint.py differ, the rest equal: 21 and 21 lines under datastorekit/; equal: 19; differing: ['datastorekit/store_fingerprint.py', 'datastorekit/store_inventory.py']; missing: none; added: none
  release:  datastorekit/store_fingerprint.py,sha256=enGZPLYaYQFvoR3LSCJYTk8DtYQRK0eU_97Nb43nzm4,16492
  v0.4.0:   datastorekit/store_fingerprint.py,sha256=OIGFxRU6LPEKr_W4zngOqHPSPwQCtT28T-aX4kVvcNg,16093
  release:  datastorekit/store_inventory.py,sha256=DJgAqZr-5LH_4ME69rtdSstFhAHdC8uSlkVUvaK5uE0,47280
  v0.4.0:   datastorekit/store_inventory.py,sha256=4PJPPpQevLoGrSzOYobAZKmJHV9da-P96x9IvQ29Tz8,45013
  probe exit 0 (release), 0 (v0.4.0) 
PASS importlib.metadata.version: 0.5.0
PASS imported from site-packages: <scratch>/venv-release2/lib/python3.13/site-packages/datastorekit/__init__.py | v0.4.0 venv: <scratch>/venv-v040/lib/python3.13/site-packages/datastorekit/__init__.py
PASS ENCODING_FORMAT is 1: 1
PASS InventorySpec's seven fields: ['leaves', 'parents', 'tags', 'values', 'validated', 'parent_sets', 'extra_values'] | v0.4.0: ['leaves', 'parents', 'tags', 'values', 'validated', 'parent_sets']
PASS Record's five fields: ['key', 'tags', 'validated', 'value_count', 'extra_value_counts'] | v0.4.0: ['key', 'tags', 'validated', 'value_count']
PASS keywords() holds extra_values: ['extra_values', 'leaves', 'parent_sets', 'parents', 'tags', 'validated', 'values']
PASS a record without counts: four keys: ['key', 'tags', 'validated', 'value_count']
PASS its canonical_json equals v0.4.0's: {"key":{"a":1,"b":"x"},"tags":["t1"],"validated":true,"value_count":3} | v0.4.0: {"key":{"a":1,"b":"x"},"tags":["t1"],"validated":true,"value_count":3}
PASS with extra_value_counts={'T2': 0}: five keys, and it hashes: ['key', 'tags', 'validated', 'value_count', 'extra_value_counts'] {"extra_value_counts":{"T2":0},"key":{"a":1,"b":"x"},"tags":["t1"],"validated":true,"value_count":3} hash=True | v0.4.0: TypeError: Record.__init__() got an unexpected keyword argument 'extra_value_counts'
PASS the hand-built inventory fingerprints to the same digest in both venvs: d493e0fe207d8e2175ce1b17fcf33801ee47a183d22a0783527647451f87f754 | v0.4.0: d493e0fe207d8e2175ce1b17fcf33801ee47a183d22a0783527647451f87f754
PASS the guard's plain digests under the release differ from v0.4.0's, every class: release [['Alpha', 'b08c7c511ca3ed79b2437635d99cc22ddce4b513d80ed4a2f278a484380d4ee9'], ['Beta', '97d99c396701e98dfdcd0a61bf957573fa853dee067f5226e6dfa6b58839e268']] | v0.4.0 [['Alpha', 'a80feec45b6e85ff368216da57c3e2f69e3c819c492e8aa76f3395a1105dd403'], ['Beta', '496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116']]
PASS with the one condition, the release's digests equal v0.4.0's plain ones: release (condition) [['Alpha', 'a80feec45b6e85ff368216da57c3e2f69e3c819c492e8aa76f3395a1105dd403'], ['Beta', '496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116']]
PASS the condition changes nothing under v0.4.0: v0.4.0 (condition) [['Alpha', 'a80feec45b6e85ff368216da57c3e2f69e3c819c492e8aa76f3395a1105dd403'], ['Beta', '496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116']]
PASS a spec declaring an extra table moves its digest with the condition, and only its: [['Alpha', 'ff2df82d76226fc9c0d27389d7a1a34d60d434d0e50644bd09504b10ae68afcb'], ['Beta', '496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116']]
PASS inventory_classes refuses values also in extra_values, naming both: ValueError: inventory_classes(): Alpha names AlphaValue both as its value table and in its extra_values
PASS inventory_specs of it does not: ['Alpha']
PASS ray not in sys.modules after the probe: False
PASS a fresh import of datastorekit.store_inventory loads no ray: exit=0 False 
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
PASS sharded_store --help exits 0: exit=0 usage: python -m datastorekit.tools.sharded_store [-h] {copy,move} src dst
RESULT: OK
```

**The neutral registry** (`<scratch>/probe/neutral_guard.py`): the recipe's `spec_digests` and
the conditioned ones, over `datastorekit.tests.client.registry.factories`, run with each export's
root as the working directory, so that its own `datastorekit` is imported (`<scratch>/exports/v040`
in `venv-v040`, `<scratch>/exports/release1` in `venv-release1`; `datastorekit.__file__` each
export's): 13 classes, the same order; **all 13 differ** plain (`Gadget`, `Sample`, `Tessera`,
`Trace`, `Weave`, `dial_setting`, `gauge_setting`, `keypoint`, `keypoint_alias`, `knob_setting`,
`routing_rule`, `store_tag`, `version`); with the condition, **only `Trace`** differs from
`v0.4.0`'s plain digests; under `v0.4.0` the condition changes none.

**The release check passes.** `git status --short --ignored` shows no `build/`, `dist/` or
`*.egg-info` in the checkout (§5.8).

### 5.4 §1.1's measure, re-run (hazard 4)

`<scratch>/probe/measure_extra_values.py <repo> <commit>` (SHA-256 `7c07e0ff…ab4f`), run with
`/opt/local/bin/python3.13 -I` from `<scratch>/outside`: it lists the commit's `.py` files with
`git ls-tree -r`, outside the top-level `prompts/`, `.prompts/`, `docs/` and `.documents/`, reads
each with `git show <commit>:<path>`, parses it with `ast` (nothing imported or run), and reports
every call of `InventorySpec`, `Record`, `read_records`, `fields`, `is_dataclass` and `asdict` (with
its positional count, keyword names, any `*`/`**`, and whether a `fields`/`is_dataclass`/`asdict` is
`dataclasses`'), every attribute `extra_values`, `extra_value_counts`, `value_count` and `as_json`,
every keyword `extra_values=`/`extra_value_counts=`, where `SPEC_DIGESTS` and `FINGERPRINT_FORMAT`
are assigned, and the `datastorekit` line of `requirements.txt`. The commits are §1.1's, each the
client's `HEAD` when read, at the start and the end.

```
== SecondaryGWKit at 031bcb4
python files parsed: 222 (unparsed: 0)
calls of InventorySpec: 21
  ObjectFactories/BackgroundModel.py:890 InventorySpec positional=0 keywords=['leaves', 'parents', 'tags', 'values', 'validated']
  ObjectFactories/GkNumericIntegration.py:641 InventorySpec positional=0 keywords=['leaves', 'parents', 'tags', 'values', 'validated']
  ObjectFactories/GkSource.py:849 InventorySpec positional=0 keywords=['parents', 'parent_sets', 'tags', 'values', 'validated']
  ObjectFactories/GkSourcePolicy.py:74 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/GkSourcePolicyData.py:183 InventorySpec positional=0 keywords=['parents']
  ObjectFactories/GkWKBIntegration.py:970 InventorySpec positional=0 keywords=['leaves', 'parents', 'tags', 'values', 'validated']
  ObjectFactories/LambdaCDM.py:98 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/OneLoopIntegral.py:348 InventorySpec positional=0 keywords=['parents', 'tags']
  ObjectFactories/QCD_Cosmology.py:134 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/QuadSource.py:552 InventorySpec positional=0 keywords=['parents', 'tags', 'values', 'validated']
  ObjectFactories/QuadSourceIntegral.py:975 InventorySpec positional=0 keywords=['parents', 'tags']
  ObjectFactories/QuadSourcePolicy.py:111 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/TkNumericIntegration.py:643 InventorySpec positional=0 keywords=['leaves', 'parents', 'tags', 'values', 'validated']
  ObjectFactories/TkWKBIntegration.py:968 InventorySpec positional=0 keywords=['leaves', 'parents', 'tags', 'values', 'validated']
  ObjectFactories/integration_metadata.py:63 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/redshift.py:139 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/store_tag.py:53 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/tolerance.py:61 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/version.py:52 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/wavenumber.py:132 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/wavenumber.py:392 InventorySpec positional=0 keywords=['leaves', 'parents']
calls of Record: 2
  tools/tests/test_inventory_report_labels.py:113 Record positional=0 keywords=['key', 'tags', 'validated', 'value_count']
  tools/tests/test_inventory_report_labels.py:89 Record positional=0 keywords=['key', 'tags', 'validated', 'value_count']
calls of read_records: 2
  ObjectFactories/tests/test_quadsource_parent_key.py:453 read_records positional=4 keywords=['parents']
  ObjectFactories/tests/test_wkb_numeric_parent_key.py:991 read_records positional=4 keywords=['parents']
calls of fields: 4
  ObjectFactories/tests/test_fingerprint_format_guard.py:38 dataclasses.fields positional=1 keywords=[] dataclasses
  tools/inventory_report.py:223 self.fields positional=1 keywords=[] NOT-dataclasses
  tools/inventory_report.py:543 self.fields positional=1 keywords=[] NOT-dataclasses
  tools/inventory_report.py:544 self.fields positional=1 keywords=[] NOT-dataclasses
calls of is_dataclass: 1
  ObjectFactories/tests/test_fingerprint_format_guard.py:36 dataclasses.is_dataclass positional=1 keywords=[] dataclasses
calls of asdict: 0
attribute .extra_values: 0
attribute .extra_value_counts: 0
attribute .value_count: 7
  tools/inventory_report.py:556
  tools/inventory_report.py:557
  tools/inventory_report.py:582
  tools/tests/test_inventory_report.py:138
  tools/tests/test_inventory_report.py:165
  tools/tests/test_inventory_report.py:170
  tools/tests/test_inventory_report_labels.py:117
attribute .as_json: 0
keyword extra_values=: 0 []
keyword extra_value_counts=: 0 []
assigned SPEC_DIGESTS: ['config/fingerprint.py:60 = Dict keys=[6]']
assigned FINGERPRINT_FORMAT: ['config/fingerprint.py:49 = 6']
datastorekit pin: ['requirements.txt:17: datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0']
== ChamPBH at 7055532
python files parsed: 169 (unparsed: 0)
calls of InventorySpec: 13
  ObjectFactories/AdiabaticHistory.py:128 InventorySpec positional=0 keywords=['parents', 'tags', 'values', 'validated']
  ObjectFactories/BBNData.py:126 InventorySpec positional=0 keywords=['leaves', 'parents', 'tags', 'values', 'validated']
  ObjectFactories/DimensionfulQuantity.py:46 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/DimensionlessQuantity.py:43 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/ExponentialCoupling.py:48 InventorySpec positional=0 keywords=['parents']
  ObjectFactories/ExponentialPotential.py:56 InventorySpec positional=0 keywords=['leaves', 'parents']
  ObjectFactories/QCD_Cosmology.py:45 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/ScalarHistory.py:226 InventorySpec positional=0 keywords=['leaves', 'parents', 'tags', 'values', 'validated']
  ObjectFactories/integration_metadata.py:40 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/redshift.py:46 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/store_tag.py:37 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/tolerance.py:39 InventorySpec positional=0 keywords=['leaves']
  ObjectFactories/version.py:37 InventorySpec positional=0 keywords=['leaves']
calls of Record: 0
calls of read_records: 0
calls of fields: 1
  ObjectFactories/tests/test_fingerprint_format_guard.py:56 dataclasses.fields positional=1 keywords=[] dataclasses
calls of is_dataclass: 1
  ObjectFactories/tests/test_fingerprint_format_guard.py:54 dataclasses.is_dataclass positional=1 keywords=[] dataclasses
calls of asdict: 2
  ObjectFactories/tests/test_fingerprint_format_guard.py:147 dataclasses.asdict positional=1 keywords=[] dataclasses
  ObjectFactories/tests/test_fingerprint_format_guard.py:148 dataclasses.asdict positional=1 keywords=[] dataclasses
attribute .extra_values: 0
attribute .extra_value_counts: 0
attribute .value_count: 3
  tools/inventory_report.py:364
  tools/inventory_report.py:365
  tools/inventory_report.py:383
attribute .as_json: 0
keyword extra_values=: 0 []
keyword extra_value_counts=: 0 []
assigned SPEC_DIGESTS: ['config/fingerprint.py:88 = Dict keys=[1, 2, 3]']
assigned FINGERPRINT_FORMAT: ['config/fingerprint.py:67 = 3']
datastorekit pin: ['requirements.txt:17: datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0']
== StochasticInstantons at f5f395b
python files parsed: 201 (unparsed: 0)
calls of InventorySpec: 22
  Datastore/SQL/ObjectFactories/CompactionFunction.py:128 InventorySpec positional=0 keywords=['parents', 'values', 'validated']
  Datastore/SQL/ObjectFactories/CosmologicalParams.py:44 InventorySpec positional=0 keywords=['leaves']
  Datastore/SQL/ObjectFactories/DimensionfulQuantity.py:46 InventorySpec positional=0 keywords=['leaves']
  Datastore/SQL/ObjectFactories/DimensionlessQuantity.py:43 InventorySpec positional=0 keywords=['leaves']
  Datastore/SQL/ObjectFactories/FullInstanton.py:109 InventorySpec positional=0 keywords=['leaves', 'parents', 'values', 'validated']
  Datastore/SQL/ObjectFactories/GradientCoupledInstanton.py:158 InventorySpec positional=0 keywords=['leaves', 'parents', 'values', 'validated']
  Datastore/SQL/ObjectFactories/InflatonTrajectory.py:101 InventorySpec positional=0 keywords=['leaves', 'parents', 'values', 'validated']
  Datastore/SQL/ObjectFactories/MasslessDecoupledDiffusion.py:27 InventorySpec positional=0 keywords=[]
  Datastore/SQL/ObjectFactories/N_final.py:29 InventorySpec positional=0 keywords=['leaves']
  Datastore/SQL/ObjectFactories/N_init.py:29 InventorySpec positional=0 keywords=['leaves']
  Datastore/SQL/ObjectFactories/QuadraticPotential.py:33 InventorySpec positional=0 keywords=['parents']
  Datastore/SQL/ObjectFactories/QuarticPotential.py:33 InventorySpec positional=0 keywords=['parents']
  Datastore/SQL/ObjectFactories/SlowRollInstanton.py:108 InventorySpec positional=0 keywords=['leaves', 'parents', 'values', 'validated']
  Datastore/SQL/ObjectFactories/alpha_regularization.py:44 InventorySpec positional=0 keywords=['leaves']
  Datastore/SQL/ObjectFactories/delta_Nstar.py:29 InventorySpec positional=0 keywords=['leaves']
  Datastore/SQL/ObjectFactories/efold.py:29 InventorySpec positional=0 keywords=['leaves']
  Datastore/SQL/ObjectFactories/integration_metadata.py:40 InventorySpec positional=0 keywords=['leaves']
  Datastore/SQL/ObjectFactories/n_collocation_points.py:38 InventorySpec positional=0 keywords=['leaves']
  Datastore/SQL/ObjectFactories/redshift.py:42 InventorySpec positional=0 keywords=['leaves']
  Datastore/SQL/ObjectFactories/store_tag.py:37 InventorySpec positional=0 keywords=['leaves']
  Datastore/SQL/ObjectFactories/tolerance.py:39 InventorySpec positional=0 keywords=['leaves']
  Datastore/SQL/ObjectFactories/version.py:37 InventorySpec positional=0 keywords=['leaves']
calls of Record: 1
  tests/test_inventory_report.py:67 Record positional=0 keywords=['key', 'tags', 'validated', 'value_count']
calls of read_records: 0
calls of fields: 6
  tools/inventory_report.py:293 self.fields positional=2 keywords=[] NOT-dataclasses
  tools/inventory_report.py:307 self.fields positional=2 keywords=[] NOT-dataclasses
  tools/inventory_report.py:325 self.fields positional=2 keywords=[] NOT-dataclasses
  tools/inventory_report.py:392 renderer.fields positional=2 keywords=[] NOT-dataclasses
  tools/inventory_report.py:417 renderer.fields positional=2 keywords=[] NOT-dataclasses
  tools/inventory_report.py:424 renderer.fields positional=2 keywords=[] NOT-dataclasses
calls of is_dataclass: 0
calls of asdict: 0
attribute .extra_values: 0
attribute .extra_value_counts: 0
attribute .value_count: 5
  tests/test_inventory_store.py:306
  tools/inventory_report.py:373
  tools/inventory_report.py:374
  tools/inventory_report.py:405
  tools/inventory_report.py:406
attribute .as_json: 0
keyword extra_values=: 0 []
keyword extra_value_counts=: 0 []
assigned SPEC_DIGESTS: []
assigned FINGERPRINT_FORMAT: []
datastorekit pin: ['requirements.txt:16: datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0']
```

**It reproduces §1.1's table exactly**: SGK 21 `InventorySpec(` calls, each by keyword, none passing
`extra_values`, 2 `Record(` by keyword at `tools/tests/test_inventory_report_labels.py:89` and
`:113`, `dataclasses.fields` and `is_dataclass` only in its guard (`:36`, `:38`), `SPEC_DIGESTS` at
`config/fingerprint.py:60` (format 6 only), `FINGERPRINT_FORMAT = 6` at `:49`, pin
`requirements.txt:17`; CPBH 13, none, its guard's (`:54`, `:56`) and `asdict` at `:147-148`,
`:88` (formats 1, 2 and 3), `:67` = 3, `requirements.txt:17`; SI 22, 1 `Record(` by keyword at
`tests/test_inventory_report.py:67`, no `dataclasses` call, no `SPEC_DIGESTS` or
`FINGERPRINT_FORMAT`, `requirements.txt:16`. Every other `fields` call is a report's own
`self.fields`/`renderer.fields` method. SGK's two `read_records` calls pass four positional
arguments and `parents=`. No client reads `extra_values`, `extra_value_counts` or `as_json`. No
stop.

### 5.5 The client citations, and the guards' `plain` (hazards 4 and 5)

Every client `path:line` in the lines this prompt added was read through `git show <commit>:<path>`
before it was written, against the statement that cites it. In particular:
- **SGK `031bcb4`**: `ObjectFactories/tests/test_fingerprint_format_guard.py` — the docstring
  naming the recipe `:11-16`, `plain` `:33-44`, `spec_digests` `:47-52`,
  `test_every_spec_is_pinned_for_the_current_format` `:56-94`, its message `:90-93` ("A spec
  changed, so bump FINGERPRINT_FORMAT …"), `test_a_key_keeps_its_type` `:96-100`;
  `config/fingerprint.py` — `FINGERPRINT_FORMAT = 6` `:49`, the rule `:51-59` ("a change to any
  `inventory_spec()` bumps FINGERPRINT_FORMAT"), `SPEC_DIGESTS = {` `:60`; `requirements.txt:17`;
  `tools/inventory_report.py:556-557`, `:582`; the two `read_records` calls.
- **CPBH `7055532`**: the guard — docstring `:29-34`, `plain` `:51-62`, `spec_digests` `:65-71`,
  the test `:75-113`, its message `:109-112`, `test_the_pin_has_one_pair_per_class_with_a_spec`
  `:115-119`, `test_a_key_keeps_its_type` `:121-125`, `test_a_parent_keyed_by_an_int_keeps_its_type`
  `:127-148` (its `asdict` `:147-148`); `config/fingerprint.py` — `:67` = 3, the rule `:79-80`,
  `SPEC_DIGESTS` `:88`; `requirements.txt:17`; `tools/inventory_report.py:364-365`, `:383`.
- **SI `f5f395b`**: `Datastore/SQL/ObjectFactories/GradientCoupledInstanton.py` — `inventory_spec`
  `:147-182`, its comment `:152-155`, `InventorySpec(` `:158`, `values=` `:180`,
  `instanton_serial` `:686-692` (`ForeignKey("GradientCoupledInstanton.serial")`);
  `tests/test_inventory_specs.py` — `READ_THROUGH` `:199-205`, `EXCLUDED` `:208-214`, `SLOTS`
  `:216`, `_slot_tables` `:224-228`, `_as_table` `:283-297`, the column test's `values` check
  `:351-358`, the counts `:412`; `tools/inventory_report.py:373-374`, `:405-406`;
  `tests/test_inventory_store.py:306`; `tests/test_inventory_report.py:67`; `requirements.txt:16`;
  the brief, present at `f5f395b`.
- **The pinning commits**, by `git log -S'DatastoreKit@v0.4.0' <commit> -- requirements.txt`: SGK
  `5b81f2e` (2026-10-14), CPBH `f41b104` (2026-10-14), SI `1b1ca6d` (2026-10-21).
- **RunRegistryKit `v0.2.0`** (tag object `895e3c7`, commit `0bae3a3`): `pyproject.toml`'s
  `stores = ["datastorekit>=0.4.0"]` (`:13-15`), which admits `0.5.0`; `docs/adoption/README.md`
  §6, "The Q5 guard" (`:172-243`), the sketch `:193-218`.

**The guards' `plain` is the recipe's.** `<scratch>/probe/compare_plain.py` parses
RunRegistryKit's sketch (`git show v0.2.0:docs/adoption/README.md`, `:194-217`) and each client's
guard module (`git show <commit>:ObjectFactories/tests/test_fingerprint_format_guard.py`, saved to
`<scratch>/guards/`, never imported), drops each function's docstring, and compares `ast.unparse`:

```
sgk-guard.py plain: identical to the recipe, docstring aside
sgk-guard.py spec_digests: identical to the recipe, docstring aside
cpbh-guard.py plain: identical to the recipe, docstring aside
cpbh-guard.py spec_digests: identical to the recipe, docstring aside
```

As text, SGK's `plain` (and CPBH's, its docstring's example `0` for `1`) differs from the recipe's
only in its docstring and in `black`'s wrapping of the dict comprehension (the quoted lines saved
from `git show` to `<scratch>/guards/`):

```diff
--- RunRegistryKit v0.2.0 docs/adoption/README.md, the sketch's plain
+++ SGK 031bcb4 ObjectFactories/tests/test_fingerprint_format_guard.py:33-44
@@ -1,8 +1,10 @@
 def plain(value):
-    """A spec as JSON: dataclasses as objects, sequences as lists, and every mapping key as
-    the JSON of the key, so that 1 ("1") and "1" ('"1"') stay apart."""
+    """A spec as JSON: dataclasses as objects, sequences as lists, and every mapping key as the
+    JSON of the key, so that 1 (`1`) and "1" (`"1"`) stay apart."""
     if dataclasses.is_dataclass(value):
-        return {f.name: plain(getattr(value, f.name)) for f in dataclasses.fields(value)}
+        return {
+            f.name: plain(getattr(value, f.name)) for f in dataclasses.fields(value)
+        }
     if isinstance(value, Mapping):
         return {json.dumps(k): plain(v) for k, v in value.items()}
     if isinstance(value, (list, tuple)):
--- SGK :33-44
+++ CPBH 7055532 :51-62
@@ -1,6 +1,6 @@
 def plain(value):
     """A spec as JSON: dataclasses as objects, sequences as lists, and every mapping key as the
-    JSON of the key, so that 1 (`1`) and "1" (`"1"`) stay apart."""
+    JSON of the key, so that 0 (`0`) and "0" (`"0"`) stay apart."""
     if dataclasses.is_dataclass(value):
         return {
             f.name: plain(getattr(value, f.name)) for f in dataclasses.fields(value)
```

### 5.6 Names and links (hazard 2)

`<scratch>/probe/check_links.py`, never committed, over `README.md`, `PROVENANCE.md`, the four
adoption files and the extraction board: each relative Markdown link outside a code fence is
resolved, the file relative to the document, then the anchor among the target's headings outside
code fences, by GitHub's rule (§3 item 2), a repeated slug gaining `-1`. **232 relative links, 0
unresolved**, among them `docs/client-contract.md#98-extra-values-prompt-01` (README `:22`, `:151`,
`:177`) and `../client-contract.md#98-extra-values-prompt-01` (each addendum), heading
`docs/client-contract.md:391`; `#addendum-v050-extra-values-prompt-02-2026-10-21` from each italic
line, from the README's addendum to each checklist's and back; G4's link to SI's new anchor (board
`:1539`); and every existing link.

`<scratch>/probe/import_names.py`, run in `venv/` from `<scratch>/outside`: every dotted
`datastorekit.` name in `README.md`, `PROVENANCE.md` and the lines added to the adoption files and
the board (13: `datastorekit.__file__`, `_timing`, `contract`, `.require_version_serial`,
`.VERSION_SERIAL_KEY`, `defaults`, `SQL.factory_base`, `SQL.ShardedPool`, `store_fingerprint`,
`store_inventory`, `tools`, `.shard_key_audit`, `.sharded_store`) imports; and the bare names the
new text gives with their module hold: `InventorySpec.extra_values` and `Record.extra_value_counts`
are dataclass fields, `Record.as_json`, `InventorySpec.keywords` and `.dependencies`,
`inventory_classes`, `inventory_specs`, `read_records` (its last keyword `extra_values`),
`read_inventory`, `canonical_json`, `Parent`, `ParentSet`, `ENCODING_FORMAT == 1`.
`ray.is_initialized()` was `False` after. The paths `PROVENANCE.md` names (17) exist.

The `v0.5.0` line citations, read at the tree: `store_inventory.py` — `Record` `:183-215`,
`extra_value_counts` `:194`, `as_json` `:196-205` (its condition `:203-204`), `InventorySpec`
`:304-344`, `extra_values` `:317`, `keywords()` `:319-329`, `read_records`' last keyword `:535`,
`_count_values` `:660-683`, the extra tables in sorted order `:688-692`, the counts per record
`:803-806`, `inventory_classes` `:962-1015`, the refusal `:990-994`; `store_fingerprint.py` — the
comment `:38-70`, its last paragraph `:66-70`, `ENCODING_FORMAT = 1` `:71`.

### 5.7 The documents (§4.4)

Every remaining `v0.4.0`, by line, with why it stays:

| File | Lines | Why it stays |
|---|---|---|
| `README.md` | `:14` | this prompt's paragraph: a record is `v0.4.0`'s |
| | `:24` | history: the `v0.4.0` status paragraph |
| | `:122` | the "remain tagged" sentence |
| | `:124` | SGK's and CPBH's permitted pin (U5) |
| | `:171` | history: "the change of `v0.4.0`", in the extended item |
| `PROVENANCE.md` | `:274` | history: the `fingerprint` section's heading |
| | `:346`, `:352` | this prompt's section: records and the other files are `v0.4.0`'s |
| `docs/adoption/README.md` | `:28` | the `v0.4.0` italic line, superseded (`:27-30`) |
| | `:34` | this prompt's italic line |
| | `:611`–`:742` | the `v0.4.0` addendum: the statements tabled superseded, the rest history true of `v0.4.0` or standing |
| | `:749`–`:897` | this addendum's own text and table (SGK's and CPBH's permitted pin among them) |
| `docs/adoption/secondarygwkit.md` | `:40`, `:41` | the `v0.4.0` italic line, superseded |
| | `:46`, `:47` | this prompt's italic line (SGK's permitted pin) |
| | `:738`–`:961` | the `v0.4.0` addendum: superseded as tabled, or standing, or history |
| | `:968`–`:1115` | this addendum's own text and table |
| `docs/adoption/champbh.md` | `:41`, `:42` | the `v0.4.0` italic line, superseded |
| | `:47`, `:48` | this prompt's italic line (CPBH's permitted pin) |
| | `:716`–`:799` | the `v0.4.0` addendum: superseded as tabled, or standing, or history |
| | `:806`–`:944` | this addendum's own text and table |
| `docs/adoption/stochasticinstantons.md` | `:39`, `:40` | the `v0.4.0` italic line, superseded |
| | `:45` | this prompt's italic line |
| | `:691`–`:778` | the `v0.4.0` addendum: superseded as tabled, or standing, or history |
| | `:785`–`:949` | this addendum's own text and table (SI's pin in place of `v0.4.0`) |

**The shifts (correction 1), checked line by line** by `<scratch>/probe/check_shift.py`: for each
file and each earlier addendum (`v0.2.1` at `33778b0`, `v0.2.2` at `6d8ee9a`, `v0.2.3` at
`0de2b16`, `v0.3.0` at `2f5417e`, `v0.4.0` at `c8570e8`), every own-file citation in that
addendum's text as committed then (an explicit `docs/adoption/<file>:a-b`, a bare `:a-b` in its
"Standing" or "Not superseded" paragraph, or an "all but `:a-b`" of its shift prose) is mapped by
the rule `f47b9a2`'s addendum states (unchanged for a head line above the inserts; the appendix's
offset for an appendix line; otherwise the stated N, k + N, …) and by the true mapping, from `git
diff -U0 <commit> -- <file>` against the tree (every hunk an addition), and its text then compared
with its text now: **816 cited lines in the four files, 0 differ**; the three appendix lines,
SGK's `:1230-1232` at `c8570e8`, are 161 lines later, as stated (`<scratch>/out/check-shift.txt`).

`git diff -- docs/adoption` has no `-` line (hazard 1). `docs/client-contract.md` and
`docs/extraction-verification.md` are unchanged (`git diff --quiet`).

### 5.8 The tree, the clients and RunRegistryKit (§4.6)

- `git status --short --ignored` before staging shows the twelve files of §7's list that this
  prompt changes as modified, this log as new, and the ignored entries at the start: `.idea/`,
  `venv/`, and five `__pycache__/` directories. There is no `build/`, `dist/` or `*.egg-info`. A
  sixth, `datastorekit/tools/__pycache__/`, written when the name check imported the two tools in
  `venv/` (editable from this checkout), was deleted.
- `git diff --quiet` holds for `datastorekit/`, `docs/client-contract.md`,
  `docs/extraction-verification.md`, `docs/extraction/`, `.github/`, `CLAUDE.md`, `LICENSE`,
  `.gitignore`, `prompts/extra-values/orchestrator/` and `prompts/fingerprint/`. On the extraction
  board only `:1539` changed.
- The tags are `v0.1.0`, `v0.2.0`, `v0.2.1`, `v0.2.2`, `v0.2.3`, `v0.3.0` and `v0.4.0`; the local
  `origin/main` is `bda6dbc`, as at dispatch. No `git ls-remote` was run.

The clients and RunRegistryKit, read only through `git rev-parse`, `git status`, `git show`, `git
ls-tree`, `git log` and `git cat-file -e`:

| Repository | At the start (23:08 BST) | At the end (23:40 BST) | `git status --short` |
|---|---|---|---|
| SGK | `031bcb4`, branch `handover-remedial` | `031bcb4`, unchanged | empty at the start and at the end |
| CPBH | `7055532`, branch `jordan-normalization` | `7055532`, unchanged | empty at the start and at the end |
| SI | `f5f395b`, branch `dk-and-rpk-migration` | `f5f395b`, unchanged | empty at the start and at the end |
| RunRegistryKit | `33a2cd2`, branch `main`, tags `v0.1.0`, `v0.2.0` | `33a2cd2`, unchanged, the same tags | empty at the start and at the end |

---

## 6. The deliberate-breakage record (§4.5)

**The method.**
1. Each diff below was made with `diff -u` of `pyproject.toml` before and after the one change,
   labelled `a/` and `b/`, and is recorded exactly as applied (`<scratch>/breaks/`).
2. Each has its own export: `git archive 79294bf` (whose `pyproject.toml` and `datastorekit/` are
   `f47b9a2`'s) into `<scratch>/exports/break-a` and `break-b`, and `git archive v0.4.0` into
   `break-c`.
3. In each export, `git apply --check` passed on the clean export, `git apply` applied it, and
   `git apply -R --check` passed on the applied one. (a) and (b) were checked the same way again on
   a copy of `983119f`'s `pyproject.toml` (byte-equal to `79294bf`'s).
4. Each was built with `uv build --offline --wheel`, installed offline into its own Python 3.13.16
   venv with `ray==2.55.1` and `sqlalchemy==2.0.46`, and checked from `<scratch>/outside` with
   `assert_release.py` against `v0.4.0`'s wheel and venv, expecting `0.5.0`.

None is committed.

**(a) `pyproject.toml`'s version left at `0.4.0`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -4,7 +4,7 @@
 
 [project]
 name = "datastorekit"
-version = "0.5.0"
+version = "0.4.0"
 description = "A sharded SQLite datastore layer (Datastore / ShardedPool) on Ray and SQLAlchemy"
 requires-python = ">=3.12"
 dependencies = [
```

The wheel is `datastorekit-0.4.0-py3-none-any.whl`, 105,083 bytes, 26 entries, none under
`tests/`, `METADATA` `Version: 0.4.0`.

```
wheel sha256: e89496def967e4adb77373aac787d70524cfa365bb8e9693e6a9a8d13d63afde  size: 105083
FAIL wheel name: datastorekit-0.4.0-py3-none-any.whl
  METADATA: ['Version: 0.4.0', 'Requires-Python: >=3.12', 'Requires-Dist: ray>=2.43', 'Requires-Dist: sqlalchemy<2.1,>=2.0.39']
FAIL METADATA Version: Version: 0.4.0
PASS no entry under datastorekit/tests/: 0 of 26 entries
PASS 26 entries: 26
PASS RECORD against v0.4.0: store_inventory.py and store_fingerprint.py differ, the rest equal: 21 and 21 lines under datastorekit/; equal: 19; differing: ['datastorekit/store_fingerprint.py', 'datastorekit/store_inventory.py']; missing: none; added: none
  release:  datastorekit/store_fingerprint.py,sha256=enGZPLYaYQFvoR3LSCJYTk8DtYQRK0eU_97Nb43nzm4,16492
  v0.4.0:   datastorekit/store_fingerprint.py,sha256=OIGFxRU6LPEKr_W4zngOqHPSPwQCtT28T-aX4kVvcNg,16093
  release:  datastorekit/store_inventory.py,sha256=DJgAqZr-5LH_4ME69rtdSstFhAHdC8uSlkVUvaK5uE0,47280
  v0.4.0:   datastorekit/store_inventory.py,sha256=4PJPPpQevLoGrSzOYobAZKmJHV9da-P96x9IvQ29Tz8,45013
  probe exit 0 (release), 0 (v0.4.0) 
FAIL importlib.metadata.version: 0.4.0
PASS imported from site-packages: <scratch>/venv-break-a/lib/python3.13/site-packages/datastorekit/__init__.py | v0.4.0 venv: <scratch>/venv-v040/lib/python3.13/site-packages/datastorekit/__init__.py
PASS ENCODING_FORMAT is 1: 1
PASS InventorySpec's seven fields: ['leaves', 'parents', 'tags', 'values', 'validated', 'parent_sets', 'extra_values'] | v0.4.0: ['leaves', 'parents', 'tags', 'values', 'validated', 'parent_sets']
PASS Record's five fields: ['key', 'tags', 'validated', 'value_count', 'extra_value_counts'] | v0.4.0: ['key', 'tags', 'validated', 'value_count']
PASS keywords() holds extra_values: ['extra_values', 'leaves', 'parent_sets', 'parents', 'tags', 'validated', 'values']
PASS a record without counts: four keys: ['key', 'tags', 'validated', 'value_count']
PASS its canonical_json equals v0.4.0's: {"key":{"a":1,"b":"x"},"tags":["t1"],"validated":true,"value_count":3} | v0.4.0: {"key":{"a":1,"b":"x"},"tags":["t1"],"validated":true,"value_count":3}
PASS with extra_value_counts={'T2': 0}: five keys, and it hashes: ['key', 'tags', 'validated', 'value_count', 'extra_value_counts'] {"extra_value_counts":{"T2":0},"key":{"a":1,"b":"x"},"tags":["t1"],"validated":true,"value_count":3} hash=True | v0.4.0: TypeError: Record.__init__() got an unexpected keyword argument 'extra_value_counts'
PASS the hand-built inventory fingerprints to the same digest in both venvs: d493e0fe207d8e2175ce1b17fcf33801ee47a183d22a0783527647451f87f754 | v0.4.0: d493e0fe207d8e2175ce1b17fcf33801ee47a183d22a0783527647451f87f754
PASS the guard's plain digests under the release differ from v0.4.0's, every class: release [['Alpha', 'b08c7c511ca3ed79b2437635d99cc22ddce4b513d80ed4a2f278a484380d4ee9'], ['Beta', '97d99c396701e98dfdcd0a61bf957573fa853dee067f5226e6dfa6b58839e268']] | v0.4.0 [['Alpha', 'a80feec45b6e85ff368216da57c3e2f69e3c819c492e8aa76f3395a1105dd403'], ['Beta', '496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116']]
PASS with the one condition, the release's digests equal v0.4.0's plain ones: release (condition) [['Alpha', 'a80feec45b6e85ff368216da57c3e2f69e3c819c492e8aa76f3395a1105dd403'], ['Beta', '496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116']]
PASS the condition changes nothing under v0.4.0: v0.4.0 (condition) [['Alpha', 'a80feec45b6e85ff368216da57c3e2f69e3c819c492e8aa76f3395a1105dd403'], ['Beta', '496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116']]
PASS a spec declaring an extra table moves its digest with the condition, and only its: [['Alpha', 'ff2df82d76226fc9c0d27389d7a1a34d60d434d0e50644bd09504b10ae68afcb'], ['Beta', '496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116']]
PASS inventory_classes refuses values also in extra_values, naming both: ValueError: inventory_classes(): Alpha names AlphaValue both as its value table and in its extra_values
PASS inventory_specs of it does not: ['Alpha']
PASS ray not in sys.modules after the probe: False
PASS a fresh import of datastorekit.store_inventory loads no ray: exit=0 False 
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
PASS sharded_store --help exits 0: exit=0 usage: python -m datastorekit.tools.sharded_store [-h] {copy,move} src dst
RESULT: FAILED (3): wheel name, METADATA Version, importlib.metadata.version
```

**Verdict:** the `METADATA` and `importlib.metadata.version` assertions fail, naming `0.4.0`, as
§4.5 says; the wheel's name fails with them. The change is in the wheel (both `RECORD` lines are
the release's, and the module behaves as the release's): only the version is wrong.

**(b) The `exclude` line removed from `pyproject.toml`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -14,4 +14,3 @@
 
 [tool.setuptools.packages.find]
 include = ["datastorekit*"]
-exclude = ["datastorekit.tests", "datastorekit.tests.*"]
```

The wheel is `datastorekit-0.5.0-py3-none-any.whl`, 338,001 bytes, **79 entries, 53 under
`datastorekit/tests/`** (`test_inventory_extra_values.py` among them; the data files are not, being
package data the build does not collect).

```
wheel sha256: 6d885e803c2548a3dea64cf4f67d97c848d869d78f388295e1e63703e079fb68  size: 338001
PASS wheel name: datastorekit-0.5.0-py3-none-any.whl
  METADATA: ['Version: 0.5.0', 'Requires-Python: >=3.12', 'Requires-Dist: ray>=2.43', 'Requires-Dist: sqlalchemy<2.1,>=2.0.39']
PASS METADATA Version: Version: 0.5.0
FAIL no entry under datastorekit/tests/: 53 of 79 entries
FAIL 26 entries: 79
FAIL RECORD against v0.4.0: store_inventory.py and store_fingerprint.py differ, the rest equal: 21 and 74 lines under datastorekit/; equal: 19; differing: ['datastorekit/store_fingerprint.py', 'datastorekit/store_inventory.py']; missing: none; added: ['datastorekit/tests/__init__.py', 'datastorekit/tests/client/__init__.py', 'datastorekit/tests/client/build.py', '…']
  release:  datastorekit/store_fingerprint.py,sha256=enGZPLYaYQFvoR3LSCJYTk8DtYQRK0eU_97Nb43nzm4,16492
  v0.4.0:   datastorekit/store_fingerprint.py,sha256=OIGFxRU6LPEKr_W4zngOqHPSPwQCtT28T-aX4kVvcNg,16093
  release:  datastorekit/store_inventory.py,sha256=DJgAqZr-5LH_4ME69rtdSstFhAHdC8uSlkVUvaK5uE0,47280
  v0.4.0:   datastorekit/store_inventory.py,sha256=4PJPPpQevLoGrSzOYobAZKmJHV9da-P96x9IvQ29Tz8,45013
  probe exit 0 (release), 0 (v0.4.0) 
PASS importlib.metadata.version: 0.5.0
PASS imported from site-packages: <scratch>/venv-break-b/lib/python3.13/site-packages/datastorekit/__init__.py | v0.4.0 venv: <scratch>/venv-v040/lib/python3.13/site-packages/datastorekit/__init__.py
PASS ENCODING_FORMAT is 1: 1
PASS InventorySpec's seven fields: ['leaves', 'parents', 'tags', 'values', 'validated', 'parent_sets', 'extra_values'] | v0.4.0: ['leaves', 'parents', 'tags', 'values', 'validated', 'parent_sets']
PASS Record's five fields: ['key', 'tags', 'validated', 'value_count', 'extra_value_counts'] | v0.4.0: ['key', 'tags', 'validated', 'value_count']
PASS keywords() holds extra_values: ['extra_values', 'leaves', 'parent_sets', 'parents', 'tags', 'validated', 'values']
PASS a record without counts: four keys: ['key', 'tags', 'validated', 'value_count']
PASS its canonical_json equals v0.4.0's: {"key":{"a":1,"b":"x"},"tags":["t1"],"validated":true,"value_count":3} | v0.4.0: {"key":{"a":1,"b":"x"},"tags":["t1"],"validated":true,"value_count":3}
PASS with extra_value_counts={'T2': 0}: five keys, and it hashes: ['key', 'tags', 'validated', 'value_count', 'extra_value_counts'] {"extra_value_counts":{"T2":0},"key":{"a":1,"b":"x"},"tags":["t1"],"validated":true,"value_count":3} hash=True | v0.4.0: TypeError: Record.__init__() got an unexpected keyword argument 'extra_value_counts'
PASS the hand-built inventory fingerprints to the same digest in both venvs: d493e0fe207d8e2175ce1b17fcf33801ee47a183d22a0783527647451f87f754 | v0.4.0: d493e0fe207d8e2175ce1b17fcf33801ee47a183d22a0783527647451f87f754
PASS the guard's plain digests under the release differ from v0.4.0's, every class: release [['Alpha', 'b08c7c511ca3ed79b2437635d99cc22ddce4b513d80ed4a2f278a484380d4ee9'], ['Beta', '97d99c396701e98dfdcd0a61bf957573fa853dee067f5226e6dfa6b58839e268']] | v0.4.0 [['Alpha', 'a80feec45b6e85ff368216da57c3e2f69e3c819c492e8aa76f3395a1105dd403'], ['Beta', '496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116']]
PASS with the one condition, the release's digests equal v0.4.0's plain ones: release (condition) [['Alpha', 'a80feec45b6e85ff368216da57c3e2f69e3c819c492e8aa76f3395a1105dd403'], ['Beta', '496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116']]
PASS the condition changes nothing under v0.4.0: v0.4.0 (condition) [['Alpha', 'a80feec45b6e85ff368216da57c3e2f69e3c819c492e8aa76f3395a1105dd403'], ['Beta', '496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116']]
PASS a spec declaring an extra table moves its digest with the condition, and only its: [['Alpha', 'ff2df82d76226fc9c0d27389d7a1a34d60d434d0e50644bd09504b10ae68afcb'], ['Beta', '496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116']]
PASS inventory_classes refuses values also in extra_values, naming both: ValueError: inventory_classes(): Alpha names AlphaValue both as its value table and in its extra_values
PASS inventory_specs of it does not: ['Alpha']
PASS ray not in sys.modules after the probe: False
PASS a fresh import of datastorekit.store_inventory loads no ray: exit=0 False 
FAIL import datastorekit.tests fails: exit=0 (no error)
PASS sharded_store --help exits 0: exit=0 usage: python -m datastorekit.tools.sharded_store [-h] {copy,move} src dst
RESULT: FAILED (4): no entry under datastorekit/tests/, 26 entries, RECORD against v0.4.0: store_inventory.py and store_fingerprint.py differ, the rest equal, import datastorekit.tests fails
```

**Verdict:** the wheel lists files under `datastorekit/tests/`, and `import datastorekit.tests`
succeeds. The counts are correction 3's: 79 entries, 53 under `tests/`.

**(c) The wheel built from `git archive v0.4.0` with only its version set to `0.5.0`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -4,7 +4,7 @@
 
 [project]
 name = "datastorekit"
-version = "0.4.0"
+version = "0.5.0"
 description = "A sharded SQLite datastore layer (Datastore / ShardedPool) on Ray and SQLAlchemy"
 requires-python = ">=3.12"
 dependencies = [
```

Applied to an export of `v0.4.0`. The wheel is `datastorekit-0.5.0-py3-none-any.whl`, 104,428
bytes, 26 entries, none under `tests/`, `METADATA` `Version: 0.5.0`.

```
wheel sha256: b1fd4a21aa66743366ceef1dc669183a9efdbc0cd935be441868ae4606a97283  size: 104428
PASS wheel name: datastorekit-0.5.0-py3-none-any.whl
  METADATA: ['Version: 0.5.0', 'Requires-Python: >=3.12', 'Requires-Dist: ray>=2.43', 'Requires-Dist: sqlalchemy<2.1,>=2.0.39']
PASS METADATA Version: Version: 0.5.0
PASS no entry under datastorekit/tests/: 0 of 26 entries
PASS 26 entries: 26
FAIL RECORD against v0.4.0: store_inventory.py and store_fingerprint.py differ, the rest equal: 21 and 21 lines under datastorekit/; equal: 21; differing: none; missing: none; added: none
  probe exit 0 (release), 0 (v0.4.0) 
PASS importlib.metadata.version: 0.5.0
PASS imported from site-packages: <scratch>/venv-break-c/lib/python3.13/site-packages/datastorekit/__init__.py | v0.4.0 venv: <scratch>/venv-v040/lib/python3.13/site-packages/datastorekit/__init__.py
PASS ENCODING_FORMAT is 1: 1
FAIL InventorySpec's seven fields: ['leaves', 'parents', 'tags', 'values', 'validated', 'parent_sets'] | v0.4.0: ['leaves', 'parents', 'tags', 'values', 'validated', 'parent_sets']
FAIL Record's five fields: ['key', 'tags', 'validated', 'value_count'] | v0.4.0: ['key', 'tags', 'validated', 'value_count']
FAIL keywords() holds extra_values: ['leaves', 'parent_sets', 'parents', 'tags', 'validated', 'values']
PASS a record without counts: four keys: ['key', 'tags', 'validated', 'value_count']
PASS its canonical_json equals v0.4.0's: {"key":{"a":1,"b":"x"},"tags":["t1"],"validated":true,"value_count":3} | v0.4.0: {"key":{"a":1,"b":"x"},"tags":["t1"],"validated":true,"value_count":3}
FAIL with extra_value_counts={'T2': 0}: five keys, and it hashes: None None hash=None | v0.4.0: TypeError: Record.__init__() got an unexpected keyword argument 'extra_value_counts'
PASS the hand-built inventory fingerprints to the same digest in both venvs: d493e0fe207d8e2175ce1b17fcf33801ee47a183d22a0783527647451f87f754 | v0.4.0: d493e0fe207d8e2175ce1b17fcf33801ee47a183d22a0783527647451f87f754
FAIL the guard's plain digests under the release differ from v0.4.0's, every class: release [['Alpha', 'a80feec45b6e85ff368216da57c3e2f69e3c819c492e8aa76f3395a1105dd403'], ['Beta', '496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116']] | v0.4.0 [['Alpha', 'a80feec45b6e85ff368216da57c3e2f69e3c819c492e8aa76f3395a1105dd403'], ['Beta', '496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116']]
PASS with the one condition, the release's digests equal v0.4.0's plain ones: release (condition) [['Alpha', 'a80feec45b6e85ff368216da57c3e2f69e3c819c492e8aa76f3395a1105dd403'], ['Beta', '496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116']]
PASS the condition changes nothing under v0.4.0: v0.4.0 (condition) [['Alpha', 'a80feec45b6e85ff368216da57c3e2f69e3c819c492e8aa76f3395a1105dd403'], ['Beta', '496177928b5797786f5e73797e12228173a5665a891f2cb9170a403d69815116']]
FAIL a spec declaring an extra table moves its digest with the condition, and only its: TypeError: InventorySpec.__init__() got an unexpected keyword argument 'extra_values'
FAIL inventory_classes refuses values also in extra_values, naming both: TypeError: InventorySpec.__init__() got an unexpected keyword argument 'extra_values'
FAIL inventory_specs of it does not: TypeError: InventorySpec.__init__() got an unexpected keyword argument 'extra_values'
PASS ray not in sys.modules after the probe: False
PASS a fresh import of datastorekit.store_inventory loads no ray: exit=0 False 
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
PASS sharded_store --help exits 0: exit=0 usage: python -m datastorekit.tools.sharded_store [-h] {copy,move} src dst
RESULT: FAILED (9): RECORD against v0.4.0: store_inventory.py and store_fingerprint.py differ, the rest equal, InventorySpec's seven fields, Record's five fields, keywords() holds extra_values, with extra_value_counts={'T2': 0}: five keys, and it hashes, the guard's plain digests under the release differ from v0.4.0's, every class, a spec declaring an extra table moves its digest with the condition, and only its, inventory_classes refuses values also in extra_values, naming both, inventory_specs of it does not
```

**Verdict:** `METADATA` and `importlib.metadata.version` say `0.5.0`, but the `RECORD` comparison
shows no line differing (21 equal), `InventorySpec` has six fields and `Record` four, and the guard
probe's "differs from `v0.4.0`" fails, as do the checks that need the new fields. The check catches
a version number with no change behind it.

---

## 7. Observations not acted on

1. **The earlier addenda's own tables now point N, k + N, … lines early** in this tree, and in a
   checklist the `v0.4.0` addendum's appendix rows N + M early. That is the reason for each
   `v0.5.0` addendum's paragraph and its rows for the rule. They are not rewritten (rule 6), and no
   issue is needed: the reader is told how to read them. This is the fifth head-line shift.
2. **G4.** SI's `requirements.txt:16` at `f5f395b` pins `v0.4.0`, since SI's `1b1ca6d` (its
   `dk-and-rpk-migration` prompt 08, 2026-10-21), and G4 reads "SI has adopted `v0.3.0` or later".
   Whether G4 holds is not this prompt's to judge (§2.5); the board's G4 row records no holding,
   and this prompt's sentence records none.
3. **SGK and CPBH have adopted RunRegistryKit** (each `config/fingerprint.py` imports
   `runregistrykit.fingerprint`, read through `git show`), so the `v0.4.0` addenda's "meets the
   module only when it adopts RunRegistryKit" (README `:689-690`, CPBH `:755-756`, SI `:730-731`)
   is a condition now met for SGK and CPBH; it was left standing as a conditional statement, true,
   and not re-measured.
4. **The `uv` cache holds a `datastorekit` 0.5.0 `.dist-info`** beside 0.4.0's, from earlier probes
   of this release. A constraints file of the cache's highest versions names `datastorekit==0.5.0`,
   so correction 3's refusal ("you require datastorekit<=0.4.0") was not reproduced; the line was
   left out as the prompt says, and every wheel installed is the one built here, by path.
5. **Lines past 100 columns** in the new addenda: the table rows, as in every earlier addendum, and
   three prose lines with a long backticked name (README `:818`, SGK `:1009`, SI `:870`). None is a defect.
6. **The high end gave 4 `ResourceWarning` lines** (§5.1): two unclosed SQLite connections reported
   from SQLAlchemy, timing, in a tree whose `datastorekit/` is 01's, which gave 4 at 01's review.
7. **The scratch tools** are in `<scratch>/probe/`, not in the repository: `insert.py`,
   `make_constraints.py`, `measure_extra_values.py`, `release_probe.py`, `assert_release.py`,
   `neutral_guard.py`, `compare_plain.py`, `check_links.py`, `import_names.py` and
   `check_shift.py`. Their outputs are in `<scratch>/out/`; the exports, wheels, venvs, the three
   diffs (`<scratch>/breaks/`), the inserted texts (`<scratch>/addenda/`) and the guards read
   through `git show` (`<scratch>/guards/`) are under `<scratch>`. `79294bf`, `d8a497c` and
   `983119f` are commit objects `git stash create` wrote with no ref.

---

## 8. Issues

- **Opened:** none. **Closed:** `[01-a-new-spec-field-moves-every-spec-guard-digest]` (board §4).
  **Narrowed:** none.
- The board's §3 holds no issue. The index is at **4 open**, all on `inherited-issues`' board.

---

## 9. State handed to the next prompt

- `HEAD` is `f47b9a2`, unpushed and untagged. The tree is clean apart from the ignored entries at
  the start. `venv/` has `datastorekit 0.5.0` installed editable from this checkout, its
  `egg-info` removed.
- **Not pushed, not tagged.** The local `origin/main` is `bda6dbc`, and the tags are `v0.1.0` to
  `v0.4.0`.
- **After the review**, `f47b9a2` is pushed as `main`. CI's run on it is the tag's gate: `v0.5.0`
  is made on it, annotated, only once CI passes there at both ends (U23, U28). If CI fails, a fix
  prompt lands first, and no tag is made on a commit whose CI is red.
- **The suite is 538** in `venv/` and at the high end. `compare_ported_tests.py`: 20 modules and one
  test declared not ported, exit 0. `black --check datastorekit docs`: 79 files.
- **For the campaign's close** (prompt §8): for SI's pin prompt, the tag object and commit, the SI
  addendum's anchor (`docs/adoption/stochasticinstantons.md#addendum-v050-extra-values-prompt-02-2026-10-21`)
  and README §0.2's points; for SGK and ChamPBH, their addenda's anchors
  (`secondarygwkit.md#…`, `champbh.md#addendum-v050-extra-values-prompt-02-2026-10-21`), each may
  stay on `v0.4.0`, and a move needs the guard's one condition; for RunRegistryKit, that its
  `docs/adoption/README.md` §6 recipe needs the same condition, in a campaign of its own.
