# Prompt 02 — release `v0.4.0`

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

*Written 2026-10-14 against `203ecd0`, whose `datastorekit/` and `docs/` are `d1b61d6`'s (prompt
01's).*

**Gate:**
- 01 landed (`d1b61d6`) and was reviewed (`203ecd0`).
- **01 is not pushed.** `origin/main` is `5f972be`, and CI has not yet run on 01's tree. The first
  CI run on it is the one on 02's commit, after 02's review; the tag waits on that run (§1).
- U6 is taken (README §6.2): `v0.4.0`, minor; SGK adopts it (its `runregistry-extraction` prompts 03
  and 06, gate E1); ChamPBH and SI may stay on their pins or move.
- `git status` is clean in this repository, and `origin/main` is an ancestor of `main`.
- This board's §3 holds no issue, and `docs/OPEN_ISSUES.md` counts 4, all on `inherited-issues`'
  board.

**Closes:** nothing. **Narrows:** nothing. **Changes:** nothing in the package but its version.
**Opens:** only what the work finds.

**Recommended model:** **Opus.**
- No line of code changes. The work is three short edits, four dated addenda and one gate.
- The addenda are not alike. For SGK the release is the one it waits on (its gate E1), and the
  addendum is the "SGK-facing note" its prompt 03 must read item by item (§1.1): it must say
  exactly what changes when SGK moves its pin (nothing it calls) and what changes when SGK calls
  the package's functions (seven things, two of which the plan did not foresee). For CPBH and SI
  nothing they call changes.
- Each file's head gains a line, which moves every citation below it, including the `v0.3.0`
  addendum's own table. The addendum says how to read those, as `object-timestamp` 02 did.
- The release check and both ends of the suite are run as `object-timestamp` 02 ran them, offline.

**Read first:**

1. [`README.md`](README.md): §0 (§0.1 and §0.2 especially), §1, §2, §4, §5 (rules 4, 5, 9, 10 and
   11), §6.2 (U1–U3 and U6), §6.1 and §7.
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`, above all "Releases".
3. This board's review of 01, and log 01 (`logs/01-the-fingerprint-moves-into-the-package.md`),
   §1, §6 and §8.
4. `object-timestamp` prompt 02 (`../object-timestamp/02-release-v0.3.0.md`) and its log
   (`../object-timestamp/logs/02-release-v0.3.0.md`). 02 is that prompt again, for one change.
   Their release check, their addenda's form and their breakages are this prompt's.
5. The files 02 changes, as they stand: `pyproject.toml`, `README.md`, `PROVENANCE.md`,
   `docs/adoption/README.md` and the three checklists. In each, read the head, and the `v0.3.0`
   addendum in full; in SGK's checklist, also item 9 (`:322-354`, the fingerprint by which G2 was
   accepted) and item 10 (`:356-378`).
6. `docs/client-contract.md` §9.7, which 02 points at and does not change.
7. The extraction board's §2 (G1–G4), `../extraction/IMPLEMENTATION_STATE.md:1532-1541`. G2 holds
   (2026-10-12: SGK on `v0.2.2`) and G3 holds (2026-10-13: CPBH on `v0.3.0`).
8. SGK's side, through `git show` only: `prompts/runregistry-extraction/README.md` at SGK
   `a5a6f6d`, its §2 rows and plans for 03, 04 and 06 (`:131-132`, `:209-232`, `:240-…`), and the
   brief, `prompts/runregistry-extraction/datastorekit-fingerprint-brief.md`, §3 and the lines
   that ask for the note (`:47-48`, `:134`).

Facts below are at `203ecd0`, measured on 2026-10-14.

---

## 1. What is wanted

02 makes the package ready to be released as **`v0.4.0`** (U6). After it:

- `pyproject.toml` says `0.4.0`;
- `README.md` and `PROVENANCE.md` describe `v0.4.0`;
- `docs/adoption/` carries a dated addendum, in its README and in each checklist, giving the pin
  and what changed for that client since `v0.3.0`; SGK's says what SGK must do to adopt it;
- the extraction board's G4 says that SI adopts `v0.3.0` or later, and that the tag waits for CI.
  G1, G2 and G3 are not changed.

**No line of code changes.** Nothing under `datastorekit/` is touched, and the suite stays at
**530**.

**02 makes no tag and pushes nothing** (U23, U28; README §5 rule 9). After its review, its commit
is pushed as `main`, carrying 01 with it. `v0.4.0` is made on it, annotated, only once CI passes
there at both ends, as `v0.3.0` was. If CI fails, a fix prompt lands first, and no tag is ever made
on a commit whose CI is red. The tag is not this prompt's work.

### 1.1 What changed since `v0.3.0`, measured

One prompt changed the package after `v0.3.0` (`2f5417e`): 01, `d1b61d6` (U1–U3, the user's
ruling).

- **In the wheel, one module is new**: `datastorekit/store_fingerprint.py` (351 lines):
  `fingerprint_of(inventory, fingerprint_format, taken=None)`, `compare_fingerprints(recorded,
  current)`, `listing_lines(inventory, fingerprint)` and `ENCODING_FORMAT = 1`, with its bump rule
  beside it. Every other file under `datastorekit/` is `v0.3.0`'s: `git diff --stat 2f5417e
  d1b61d6 -- datastorekit` lists the module, its test module and the golden only. In particular
  `store_inventory.py`, layer B, is unchanged, and has been since `v0.2.2` (`git diff --stat
  v0.2.2 d1b61d6 -- datastorekit/store_inventory.py` is empty).
- **Outside the wheel**: `datastorekit/tests/test_store_fingerprint.py` (21 tests: 509 → 530) and
  the golden `datastorekit/tests/data/store_fingerprint-neutral-1-encoding-1.json`; the contract's
  §9.7 and its head line. The smoke script is unchanged, and no test needs Ray.

**What a client sees** (contract §9.7). Nothing the layer writes or reads changes, and no message,
refusal or exception of the layer's. A client that does not import `datastorekit.store_fingerprint`
meets nothing new. One that does gets:
- **`fingerprint_of(inventory, fingerprint_format, taken=None)`**, pure, over what `read_inventory`
  returns. The client's format is required, positional or by keyword; a `bool` or non-`int` raises
  `TypeError`, an `int` below 1 `ValueError`, before anything is read.
- **Every fingerprint** has exactly the keys `fingerprint_format`, `encoding_format`, `classes`,
  `digest`, `problems` and `taken`. The overall digest hashes `{"fingerprint_format", "classes":
  {name: {"count", "digest"}}}` exactly, so `encoding_format`, `problems` and `taken` are outside
  every digest.
- **`compare_fingerprints`** refuses two fingerprints whose `fingerprint_format` or
  `encoding_format` differ: one entry of kind `format` (the source's text verbatim) and/or one of
  kind `encoding`, and nothing else compared. **A fingerprint without `encoding_format` (one made
  by any code but this module's) is refused against one with it.**
- **`listing_lines`**' first line is `# fingerprint_format <f> digest <d> encoding_format <e>`. It
  reads `fingerprint["encoding_format"]`, so it needs a fingerprint of this module's (log 01, §6
  item 1: one of the source's raises `KeyError`).
- **`ENCODING_FORMAT`**, the package's version of layers B and C, bumped under contract §9.7's rule;
  a client never bumps it, and keeps its own `fingerprint_format`.

This is added API, so the release is minor (U6, reading extraction U36 and `factory-defaults` U5).

**What the clients do with it**, read through `git` only. The planner's measure: a script of `ast`
reads of every `.py` file from `git show <commit>:<path>`, outside each client's `prompts/`,
`.prompts/`, `docs/` and `.documents/`, finding every `def` and every call of a function named
`fingerprint_of`, `compare_fingerprints` or `listing_lines`, with each call's positional and
keyword arguments.

| Client, commit | Its pin | Defines | Calls |
|---|---|---|---|
| SGK `a5a6f6d` (`handover-remedial`, clean); the same at `c8a7f14` | `v0.2.2` (`requirements.txt:17`) | all three, its own (`RunRegistry/stores.py:1182`, `:1256`, `:1376`) | `fingerprint_of` ×10: two with `taken` **positional** (`RunRegistry/stores.py:1500`, in `fingerprint_store`; `RunRegistry/tests/test_store_fingerprint.py:378`), eight with the inventory alone (`test_store_fingerprint.py:147`, `:162`, `:196`, `:336`, `:566`; `ObjectFactories/tests/test_quadsource_policy_key.py:413`, `:416`, `:419`); `compare_fingerprints` ×9 (`stores.py:1529`; `test_store_fingerprint.py:176`, `:219`, `:254`, `:338`, `:381`, `:447`, `:455`; `RunRegistry/tests/test_store_retire.py:471`); `listing_lines` ×1 (`stores.py:1432`, in `write_listing`) |
| CPBH `2792a85` (`read-only-plots`, 23 untracked entries) | `v0.3.0` (`requirements.txt:17`); G3 holds | none | none |
| SI `5fb4a1d` (`dk-and-rpk-migration`, clean) | none | none | none |

So:
- **Moving SGK's pin changes nothing SGK calls.** SGK's own three functions stay SGK's until its
  prompt 06; what they import from the package (`canonical_json`, `read_inventory`) is unchanged
  since `v0.2.2`; and `v0.2.3` and `v0.3.0` ask nothing of SGK (their addenda). So no SGK suite
  count changes with the pin (SGK 03's acceptance 2), and every SGK digest is as at `v0.2.2`.
- **When SGK calls the package's functions** (its 06), seven things change for it; §2.4's SGK row
  lists them. Two the plan did not name: **`fingerprint_store`'s own call** (`stores.py:1500-1508`)
  passes `taken` positionally, like the test at `:378`, and is refused with `TypeError`; and
  **every fingerprint SGK already holds**, in every store's sidecar and in its golden files, has no
  `encoding_format`, so the package's `compare_fingerprints` refuses each against a fresh one with
  one `encoding` entry. `fingerprint_store` returns that as its comparison (`stores.py:1529`), and
  `retire_store` refuses a store whose comparison is not empty (`test_store_retire.py:460-479`). How
  SGK meets that (re-recording each sidecar's fingerprint with the package's code, or otherwise) is
  SGK's choice; the addendum names it and what each option touches, and makes no choice.
- **CPBH and SI** define and call none of the three. They meet the module only when they adopt
  RunRegistryKit, whose `[stores]` extra will require this release (README §7).

**The clients' pins and `HEAD`s move** (other sessions work there). Record what you read, and
compare nothing but the table's facts.

### 1.2 The release check, probed

The planner probed the release on this machine, offline, as `object-timestamp` 02 did.
- **The build.** From a `git archive` of `203ecd0` with only `version = "0.4.0"` changed,
  `uv build --offline --wheel` gives `datastorekit-0.4.0-py3-none-any.whl` (104,424 bytes). It has
  26 entries, none under `datastorekit/tests/`. `METADATA` says `Version: 0.4.0`,
  `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43` and `Requires-Dist:
  sqlalchemy<2.1,>=2.0.39`.
- **The install.** `uv venv --offline -p /opt/local/bin/python3.13`, then `uv pip install
  --offline <wheel> "ray==2.55.1" "sqlalchemy==2.0.46"` (Python 3.13.16, SQLite 3.53.4).
- **The run**, from a directory outside the repository with `PYTHONPATH` unset and `python -I`:
  - `datastorekit` imports from the venv's `site-packages`;
  - `importlib.metadata.version("datastorekit")` is `0.4.0`;
  - `datastorekit.store_fingerprint.ENCODING_FORMAT` is `1`;
  - `inspect.signature(fingerprint_of)` is `(inventory, fingerprint_format: int, taken:
    Optional[Mapping[str, Any]] = None) -> dict`, `fingerprint_format` `POSITIONAL_OR_KEYWORD` with
    no default;
  - on a hand-built `StoreInventory` of two classes (one with two records, one empty), made from
    `datastorekit.store_inventory`'s dataclasses and naming a primary that does not exist:
    `fingerprint_of(inv, 1)` has exactly the six keys, `encoding_format` 1 and `taken` `None`; its
    digest equals the SHA-256 of `canonical_json` of the overall object, recomputed; by keyword it
    is equal; at format 6 the digest differs and `classes` is equal; `True`, `"1"`, `1.0` and a
    dict raise `TypeError` with "must be an int", `0` raises `ValueError` with "must be at least
    1", and a missing format raises `TypeError`; against a copy without `encoding_format`, the
    comparison is one entry, `("encoding", None, 1)`; against one with a `taken`, `[]`; the
    listing's first line's words 2, 4 and 6 are `1`, the digest and `1`;
  - in a fresh interpreter, `import datastorekit.store_fingerprint` leaves `ray` out of
    `sys.modules`;
  - `import datastorekit.tests` raises `ModuleNotFoundError`;
  - `python -m datastorekit.tools.sharded_store --help` exits 0.
- **Against `v0.3.0`'s wheel**, built from `git archive v0.3.0` (99,488 bytes, 25 entries): its 20
  `RECORD` lines under `datastorekit/` are all equal in the release's, which has one more,
  `datastorekit/store_fingerprint.py` (16,093 bytes).
- **Breakage (b), probed:** with the `exclude` line removed, the wheel has 78 entries, 52 of them
  under `datastorekit/tests/` (the golden `.json` is not among them: it is package data, which the
  build does not collect).
- **Breakage (c), probed:** a wheel built from `git archive v0.3.0` with only its version set to
  `0.4.0` has 25 entries and no `RECORD` line differing from `v0.3.0`'s.

The wheel's bytes are not reproducible across builds (file times). Record the SHA-256 of yours,
and do not compare it with the planner's. The `RECORD` lines are content hashes, and do compare.

---

## 2. What to change

### 2.1 `pyproject.toml`

`version = "0.4.0"` (`:7`). Nothing else. No other file carries the version.

### 2.2 `README.md`

- **Status.** A paragraph for **`v0.4.0`**, above `v0.3.0`'s (`README.md:10-18`):
  - it is a minor release with one change, `fingerprint` prompt 01, on the user's ruling: a new
    module, `datastorekit.store_fingerprint`, takes a store's fingerprint from what
    `read_inventory` returns (`fingerprint_of`), compares two (`compare_fingerprints`) and lists
    one (`listing_lines`);
  - the client gives its own format number, which it keeps and bumps; the package records its own
    `ENCODING_FORMAT` beside it in every fingerprint, outside the digest, and a comparison refuses
    two fingerprints whose formats of either kind differ;
  - nothing the layer writes or reads changes, no message, refusal or exception of the layer's,
    and `store_inventory` is unchanged; a client that does not import the module meets nothing
    new;
  - it adds API, so it is a minor release;
  - it points at contract §9.7 for the detail, by its anchor.
- **Installing.** The pin is `v0.4.0` (`:93`). Replace `:96-99` with what U6 says, as of the tag:
  - `v0.3.0`, `v0.2.3`, `v0.2.2`, `v0.2.1`, `v0.2.0` and `v0.1.0` remain tagged, and no tag is
    moved or deleted;
  - SecondaryGWKit adopts `v0.4.0`; ChamPBH may stay on `v0.3.0` and StochasticInstantons adopt
    `v0.3.0`, or either may move to `v0.4.0`, in a commit of its own, as it chooses: neither
    calls the new module, and nothing they call changes.

  Name no client's paths. The README is committed before the tag exists, and is true once it does.
- **Using it.** Two items:
  - a new item, after "The inventory declarations" (`:122-123`): **the store fingerprint**,
    optional: `datastorekit.store_fingerprint`'s three functions, what the client gives (its
    `fingerprint_format`) and what it never bumps (`ENCODING_FORMAT`), linking §9.7 by anchor;
  - **"What changed after `v0.2.0`"** (`:131-137`) adds `v0.4.0`'s change, still linking §9.
- **Nothing else changes.** Check every name and anchor the README mentions, as
  `object-timestamp` 02 did.

### 2.3 `PROVENANCE.md`

Add, after "`object-timestamp` prompt 01: the object carries a timestamp (`v0.3.0`)" (`:242`, the
file's last section, which ends at `:272`), a `###` section **"`fingerprint` prompt 01: the store
fingerprint moves into the package (`v0.4.0`)"**. It says:
- **Its source is SGK, after the import commit.** SGK's `RunRegistry/stores.py:1164-1400` at
  `c8a7f14` (2026-10-12; `RunRegistry/` is unchanged from there to SGK's `a5a6f6d`): the five
  functions `_sha256_lines`, `_tag_sets`, `fingerprint_of`, `compare_fingerprints` and
  `listing_lines`, and the helpers `_tags_text`, `_difference` and `_presence`. The extract's
  SHA-256 is `9b1a8aedb006ffa9c2635038eda2e87cad451106283d022a94f8038cd8eb0108` (log 01). The move
  is the user's ruling of 2026-10-12, SGK's D3 (`prompts/fingerprint/README.md` §0), and was made
  by `fingerprint` prompt 01 (`d1b61d6`). Unlike `v0.1.0`'s files, this one is not under
  `compare_with_source.py`, which is retired at `v0.1.0`.
- **The differences from the source**, each a decision of `prompts/fingerprint/README.md` §6.2:
  the client's format a required argument, checked, where the source read its
  `FINGERPRINT_FORMAT` (U1); `encoding_format` beside the digest, both versions refused on
  mismatch, the listing's first line's appended field (U2); `ENCODING_FORMAT` and its bump rule
  (U3); `canonical_json` imported at module scope; prose rewritten for the package, and the
  source's history comment left out. Every digest, count and comparison entry is the source's: the
  equivalence check of log 01 §4.3 (37 changed stores and the baseline, formats 1 and 6, at both
  ends) found 0 differences. `store_inventory.py` is unchanged.
- **The files 01 changed, and its log.**

Change nothing above it. `PROVENANCE.md` is outside the package, so it may name SGK and its paths.

### 2.4 The addenda (U6)

Each addendum is dated, says it was written by `fingerprint` prompt 02, and is added. **Nothing
already in the file is rewritten** (`CLAUDE.md` rule 6): 07a's text and the `v0.2.1`, `v0.2.2`,
`v0.2.3` and `v0.3.0` addenda all stay as written, true of their releases. Each file gains two
things.

1. **An italic line at its head**, after `object-timestamp` 02's (`docs/adoption/README.md:22-25`,
   `secondarygwkit.md:33-37`, `champbh.md:34-38`, `stochasticinstantons.md:32-36`). It says that
   the addendum below gives the pin and what changed since `v0.3.0`, and that it supersedes the
   statements it names.
2. **A section `## Addendum: v0.4.0 (fingerprint prompt 02, <date>)`**, unnumbered, after the
   `v0.3.0` addendum. In each checklist it goes before `## Appendix: the script's output`
   (`secondarygwkit.md:726`, `champbh.md:704`, `stochasticinstantons.md:679`), in the form the
   `v0.3.0` addendum took there. In the README it goes at the end (the `v0.3.0` addendum ends the
   file, at `:597`). The date is the day you write it.

Each addendum states:
- **the pin, by client** (U6): for SGK, `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.4.0`,
  in place of `v0.2.2`, by its `runregistry-extraction` prompt 03; for CPBH, `v0.3.0` (which it
  has) or `v0.4.0`, CPBH's choice; for SI, `v0.3.0` or `v0.4.0`, SI's choice, when it is next
  active; a move being a commit of the client's own. G2 ("`v0.2.2` or later") and G3 ("`v0.2.3` or
  later") read as before and hold; G4 reads "SI has adopted `v0.3.0` or later". That amends
  `object-timestamp` U6 for G4, and keeps it for G2 and G3 (README §6.1);
- **what changed since `v0.3.0`, for that client** (below), with contract §9.7 as the detail,
  linked by anchor;
- **which statements it supersedes**, each by `path:line` of the file it is in. At least: the head
  line that says `v0.3.0`'s addendum gives the pins; the `v0.3.0` addendum's pin, and its
  statements that the client adopts or may move to `v0.3.0`, and of the gate where they change
  (G4); and its rows of the same;
- **how to read the earlier addenda's citations.** This addendum's head line moves every line
  below it, so the `v0.3.0` addendum's `path:line`s, which are that file's as `object-timestamp` 02
  committed it, are read at `2f5417e`, or N lines later here (say N, and which citations are above
  the insert). The `v0.3.0` addendum did the same for the three before it; say that its rule still
  holds, shifted by N, with each shift as a number;
- **line citations.** A `datastorekit/` line in 07a's text stays `v0.2.0`'s, one in the `v0.2.1`
  addendum `v0.2.1`'s, and so on to the `v0.3.0` addendum, `v0.3.0`'s. A line this addendum cites
  is `v0.4.0`'s tree, whose `datastorekit/` is `d1b61d6`'s and 02's. An SGK line is SGK's at the
  commit named.

What each addendum says:

| File | States | Supersedes, at least (each in part, by `path:line`) |
|---|---|---|
| `README.md` | the pins by client (U6); what changed, §1.1's "What a client sees", linked to contract §9.7; nothing any client supplies or stores changes, and no message; §1.1's measure, per client, in one table; that a client's fingerprints made by its own code have no `encoding_format` and are refused against the package's (so a client that moves to the package's functions recomputes those it holds, or keeps comparing them with its own code), and that `ENCODING_FORMAT` is the package's, bumped under contract §9.7, a bump being said in a release's addendum to every checklist; the checklists are not re-measured (as U37), and each has its own addendum | the `v0.3.0` addendum's pins (`:486-501`), its sentence that `v0.3.0` carries the earlier releases' changes, and its table rows that give the pins and gates or count the addenda ("each checklist with its four addenda") |
| `secondarygwkit.md` | **the note SGK's prompt 03 reads** (SGK README `:216`). The pin: SGK adopts `v0.4.0` in place of `v0.2.2` (its 03); G2 still holds, its reading unchanged. **What the pin alone changes: nothing SGK calls** (§1.1): `v0.2.3` and `v0.3.0` ask nothing of SGK (their addenda); SGK's own fingerprint code keeps running, and `store_inventory`, which it reads, is unchanged since `v0.2.2`; no SGK suite count changes; every digest is as at `v0.2.2`. **What changes when SGK calls the package's functions** (its 06), each with SGK's `path:line` at `a5a6f6d`: (1) `fingerprint_format` is required: every one of the ten `fingerprint_of` calls gains it, and the two that pass `taken` positionally (`RunRegistry/stores.py:1500`, `RunRegistry/tests/test_store_fingerprint.py:378`) would hash nothing and raise `TypeError`, naming the dict; (2) every fingerprint has `encoding_format`: `TestGolden.test_the_shape`'s key set (`test_store_fingerprint.py:358-374`) and `test_the_golden_fingerprint` (`:350-356`, whose golden has none) are SGK's to change; `_fingerprint_problems` (`stores.py:416-437`) allows the extra key; (3) `compare_fingerprints` gives an `encoding` entry when the encoding formats differ, and **every fingerprint SGK already holds**, in each store's sidecar and in its goldens, has none, so each is refused against a fresh one: `fingerprint_store`'s comparison (`stores.py:1510-1529`) is then that one entry, and `retire_store` refuses the store until its recorded fingerprint is one of the package's (`test_store_retire.py:460-479`); how SGK meets that is its choice, the options named and none made; `TestFormats` (`:434-457`) keeps its answer, both sides lacking the key; (4) the listing's first line gains ` encoding_format <e>` at its end, and `parse_listing`'s `words[2]` and `words[4]` (`:114-136`) are unchanged; (5) `listing_lines` needs a fingerprint of the package's `fingerprint_of` (log 01 §6 item 1); (6) `FINGERPRINT_FORMAT`, its history comment (`stores.py:194-206`) and its bumps stay SGK's, and SGK never bumps `ENCODING_FORMAT`; (7) SGK's R1 (its 04) takes each store's fingerprint both ways at format 6, and 01's equivalence check found the package's equal to SGK's code on every field but `encoding_format`; a difference there is a defect of this package, reported here (README §7). Item 9's fingerprint statements (`:327-354`) still hold, of SGK's own code | the `v0.3.0` addendum's pin (`:643-…`, in part: the choice of `v0.2.2`, `v0.2.3` or `v0.3.0`) and the pins below it, and its table rows that give the pin or count the addenda; **not** G2's reading or its holding, which stand (as `object-timestamp` 02's correction 2) |
| `champbh.md` | CPBH has adopted `v0.3.0` (G3 holds, 2026-10-13, the extraction board) and may stay or move to `v0.4.0` (U6); nothing changes for CPBH: it defines and calls none of the three functions (§1.1's measure at the `HEAD` you read); it meets the module only when it adopts RunRegistryKit; item 8 still holds | the `v0.3.0` addendum's pin (`:630-…`, in part) and its table rows that give the pin or count the addenda; not G3's reading, which stands |
| `stochasticinstantons.md` | SI adopts `v0.3.0` or `v0.4.0`, as it chooses, when it is next active, and G4 reads "SI has adopted `v0.3.0` or later"; nothing changes for SI: it defines and calls none of the three functions; it meets the module only when it adopts RunRegistryKit; the `v0.3.0` addendum's account of `DatastoreObject.timestamp` holds at `v0.4.0` | the `v0.3.0` addendum's pin and G4 statement (`:595-…`) and its table rows that give them or count the addenda |

**The line numbers here are the planner's at `203ecd0`.** Check each against the file before citing
it, and cite what you find, in the file as committed with your addendum. A statement the table does
not name that is no longer true of `v0.4.0` is superseded too, and recorded in the log: grep each
file for `v0.3.0`, `fingerprint`, `store_inventory`, `four addenda` and `RunRegistry` (planner's
grep: the hits above; SGK's item 2's `store_inventory.py`, its import tables, and item 9's
fingerprint paragraph, which describe SGK's code and stay true; the README's module map
(`:87`, `:94`), which maps modules a client has and so does not gain `store_fingerprint`).

### 2.5 The extraction board's gate

On `../extraction/IMPLEMENTATION_STATE.md` §2:
- **G4**'s title says "SI adopted `v0.3.0` or later (U37; `actor-names` U3; `factory-defaults` U5;
  `object-timestamp` U6; `fingerprint` U6)";
- its status cell gains one dated italic sentence at its end, in the form of the `v0.3.0` "ready to
  be tagged" sentence: `v0.4.0` is ready to be tagged on `fingerprint` 02's commit once CI passes
  there at both ends (as U23 and U28); 02 makes no tag and pushes nothing; SI may adopt `v0.3.0` or
  `v0.4.0`, as it chooses; and SI's addendum, by anchor.

The text already there stays as it is, and the row's diff is the row as it was with its title
changed and its sentence added. **G1, G2 and G3 are unchanged**: G2 and G3 hold, and their readings
("`v0.2.2` or later", "`v0.2.3` or later") already admit `v0.4.0`. So is the rest of that board.
That campaign stays closed. SGK's gate E1 is SGK's board's, not this repository's.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **Additive documents.** Everything under `docs/` is additive (`CLAUDE.md` rule 6). An addendum
   that rewrites a line of 07a's or of an earlier addendum fails acceptance. `git diff` of each
   file under `docs/adoption/` shows `+` lines only.
2. **A name or link that does not exist.** Check every module, name, file, anchor and contract row
   that the README, `PROVENANCE.md` and the addenda mention: names by importing them in `venv/`,
   and anchors by finding the heading by GitHub's rule. The log lists each, with how it was
   checked. Contract §9.7's heading is "9.7 `fingerprint` prompt 01"; derive its anchor, and say
   how. Each new addendum's own anchor is derived the same way.
3. **The tag does not exist yet.** The README, the addenda and the gate name `v0.4.0` as of the
   tag. Nothing may say it is tagged.
4. **No client is re-measured beyond §1.1.** Re-run §1.1's measure yourself, read-only through
   `git` (a script of your own in the scratchpad, run with `python -I`, that reads `git show` and
   imports nothing of the client), at SGK `a5a6f6d` and `c8a7f14` and at the `HEAD`s of all three
   you read, and record it. If SGK's counts or sites differ at `a5a6f6d`, stop. If CPBH or SI at
   the `HEAD` you read defines or calls any of the three, stop. A citation the SGK addendum makes
   is checked with `git show a5a6f6d:<path>` before it is written.
5. **Offline only.** Every venv and the build are `--offline`. A pin, or the build backend, that
   does not resolve offline is a stop.
6. **`venv/`'s metadata.** After §2.1, `pip show datastorekit` in `venv/` still says `0.3.0`, since
   the editable install records the version when it is installed. Reinstall it offline, from the
   repository root, **without** `--no-build-isolation`, since `venv/` has no `setuptools`
   (`object-timestamp` 02's note, correction 1): `uv pip install --offline --no-deps --python
   venv/bin/python -e .`. That writes a `datastorekit.egg-info/` at the root, which you delete
   afterwards. Then run the suite in `venv/` again. Nothing else is built in the checkout.
7. **No Ray.** This prompt starts no Ray. The smoke script is not run: no code changes, and 01
   started none (README §5 rule 7).
8. **U6's wording.** "CPBH may stay on `v0.3.0`" and "SI may adopt `v0.3.0`" are permission, not
   advice. No document says CPBH or SI should or should not move. SGK's addendum names SGK's
   choices (§2.4, its item 3) and makes none of them; anything it recommends is marked **Advice:**,
   as the checklists' convention requires.
9. **Run from the right place.** Every scratch-venv command runs with its export, or a directory
   outside the repository, as the working directory. Print `datastorekit.__file__` once in each
   venv and record it.
10. **The package names no client.** The guards cover `datastorekit/`, which 02 does not touch.
    `PROVENANCE.md` and `docs/adoption/` may name the clients, and do.

---

## 4. Verification

1. **The suite.** In `venv/`, `Ran 530 tests … OK` before and after, with `pip show` saying `0.4.0`
   after. Also at the high end: a fresh offline scratch venv (Python 3.13.16, `ray==2.55.1`,
   `sqlalchemy==2.0.46`, `setuptools`) with a `git archive` of your tree installed editable
   (`--no-deps --no-build-isolation`) gives `Ran 530 tests … OK`. Record the `ResourceWarning`
   lines at each end: 0 in `venv/`; 0 or 4 at the high end, which is timing (`actor-names` log 01,
   correction 8).
2. **The checks.**
   - `compare_ported_tests.py` exits 0 with "20 module(s) … 1 test(s) declared not ported".
   - `black --check datastorekit docs` leaves 78 files unchanged.
   - The guards pass; they are in the suite.
3. **The release check**, as §1.2. Build from a clean `git archive` of your tree, never in this
   checkout, and install at the high pins, offline. Record:
   - the wheel's name, size, entry count and SHA-256, and its file list;
   - `METADATA`'s `Version`, `Requires-Python` and `Requires-Dist` lines;
   - each check of §1.2's run, with its output, and the probe script;
   - the `RECORD` comparison with a wheel built from `git archive v0.3.0`.

   `git status` shows no `build/`, `dist/` or `*.egg-info` afterwards.
4. **The documents.** List every remaining `v0.3.0` in `README.md`, `PROVENANCE.md` and
   `docs/adoption/*.md`, each with why it stays: history, a statement an addendum supersedes,
   CPBH's or SI's permitted pin, or the README's "remain tagged". Also confirm:
   - `git diff` of the four files under `docs/adoption/` has no `-` line;
   - `docs/client-contract.md` and `docs/extraction-verification.md` are unchanged.
5. **The breakage record.** Each item is a change exactly as applied in a scratch export, with
   what failed. None is committed. Check each diff with `git apply --check` and `-R --check` as
   recorded.
   - **(a)** `pyproject.toml`'s version left at `0.3.0`: the release check's `METADATA` and
     `importlib.metadata.version` assertions fail, naming `0.3.0`.
   - **(b)** the `exclude` line removed from `pyproject.toml`: the wheel lists files under
     `datastorekit/tests/`, and `import datastorekit.tests` succeeds.
   - **(c)** the wheel built from `git archive v0.3.0` with only its version set to `0.4.0`: its
     `METADATA` says `0.4.0`, but the `RECORD` comparison with `v0.3.0`'s wheel shows no line
     differing or added, where the release adds `store_fingerprint.py`'s; and `import
     datastorekit.store_fingerprint` raises `ModuleNotFoundError`. The check must catch a version
     number with no change behind it.
6. **The clients.** Record each client's `HEAD` and `git status --short`, at the start and the end.
   None is written, run, imported or opened.

---

## 5. Acceptance

1. `pyproject.toml` says `0.4.0`, and nothing else in it changed.
2. `README.md` and `PROVENANCE.md` are as §2.2 and §2.3 say, and every name in them exists.
3. Each of the four files under `docs/adoption/` has its italic line and its addendum, per §2.4,
   and no line of it is rewritten. SGK's addendum states each of §2.4's items for SGK, each SGK
   citation true at `a5a6f6d`.
4. The extraction board's G4 is as §2.5 says, and G1, G2 and G3 are unchanged.
5. §4.1–§4.6 hold.
6. **The records**, in the same commit:
   - the log `logs/02-release-v0.4.0.md`, per README §5.1. Besides its sections it has the release
     check, the documents' check (§4.4), every name and link checked (hazard 2), §1.1's measure
     re-run (hazard 4), (a)–(c), each addendum's supersession table, and the clients at the start
     and the end;
   - this board: §1's row for 02 (written, landed, commit, log), and the header;
   - this campaign's README: its header and §2's row for 02;
   - `docs/OPEN_ISSUES.md`: unchanged at **4**, unless the work opens an issue;
   - `prompts/INDEX.md`: the campaign's line.

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 530, in any venv.
- The release check fails in a way (a)–(c) do not explain.
- §1.1's measure, re-run, differs for SGK at `a5a6f6d`; or CPBH or SI, at the `HEAD` you read,
  defines or calls one of the three functions.
- An addendum cannot say what it must without rewriting a line already in its file.
- Anything would change a file under `datastorekit/`, `docs/client-contract.md`,
  `docs/extraction-verification.md`, `docs/extraction/`, the workflow, or any file not in §7.
- Anything would push, make or move a tag, download, start Ray, or write, run, import or open
  anything of a client.

---

## 7. What this prompt changes, and what it does not

- **Files it changes:**
  - `pyproject.toml`, `README.md` and `PROVENANCE.md`;
  - `docs/adoption/README.md`, `secondarygwkit.md`, `champbh.md` and `stochasticinstantons.md`,
    by addition only;
  - the extraction board's §2 (G4), per §2.5;
  - the log, this board, this campaign's README (its header and §2's row for 02),
    `docs/OPEN_ISSUES.md` if an issue is opened, and `prompts/INDEX.md`.
- **It changes nothing else:** no file under `datastorekit/`; not `docs/client-contract.md`,
  `docs/extraction-verification.md`, `docs/extraction/`, the workflow, `CLAUDE.md`, `LICENSE` or
  `.gitignore`.
- **It touches no client repository.**
- **It makes no tag and pushes nothing.** The orchestrator's note says how the push and the tag are
  made after the review.

---

## 8. After 02

The campaign closes when `v0.4.0` is tagged on 02's commit after green CI. The orchestrator records
that on this board and on the extraction board's G4, closes the campaign in its header, README and
`prompts/INDEX.md`, in a records commit of its own, and pushes it with the user's approval. It then
gives the user, for SGK's gate E1: the tag object and commit, the SGK addendum's anchor, and README
§0.2's six points to report back to the SGK session, with two more found here (§1.1): SGK's
`fingerprint_store` also passes `taken` positionally (`RunRegistry/stores.py:1500`), and every
fingerprint SGK holds lacks `encoding_format`, so the package's comparison refuses each until it is
recomputed. SGK's R1 result, when it comes, is recorded on this board (README §7).
