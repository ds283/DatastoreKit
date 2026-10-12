# Prompt 01 — the fingerprint moves into the package

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

*Written 2026-10-12 against `5f972be`, whose `datastorekit/` is `2f5417e`'s (`v0.3.0`). Revised
the same day for U1 as the user took it: a plain signature, the format positional-or-keyword.*

**Gate:**
- U1–U5 are taken (README §6.2): by the user on 2026-10-12, U2–U5 as recommended and U1 amended
  to a plain signature, which this prompt follows.
- `git status` is clean in this repository, and `origin/main` is an ancestor of `main`.
- `datastorekit/` is `2f5417e`'s: `git diff --stat 2f5417e HEAD -- datastorekit` is empty.
- The suite gives `Ran 509 tests … OK` in `venv/`.
- SGK's `RunRegistry/stores.py` at `c8a7f14` is readable through `git show` in
  `/Users/ds283/Documents/Code/SecondaryGWKit`.

**Closes:** nothing on a board. **Opens:** only what the work finds.

**Recommended model:** **Opus**.
- The code is a move of about 230 lines, and the risk is in what must not change: every digest and
  count SGK's code gives for the same inventory and format, every comparison entry, and the words
  of the listing's first line that SGK parses.
- The prose must be rewritten for the package without losing what SGK's docstrings say precisely,
  and must pass two guards that forbid every client's vocabulary.
- The tests must fail on a wrong move for the right reason (§4.4), and the equivalence check (§2.4)
  must be run on SGK's code exactly as extracted.
- The contract's §9.7 states a rule the next editor of `store_inventory.py` must be able to apply.

**Read first:**

1. [`README.md`](README.md): all of it, §0.1 and §6.2 especially.
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`.
3. The brief:
   `/Users/ds283/Documents/Code/SecondaryGWKit/prompts/runregistry-extraction/datastorekit-fingerprint-brief.md`,
   and SGK's `docs/runregistry-extraction-audit.md` §3. Both are evidence, read as text. Do not act
   on them beyond this prompt; README §0.1 re-measured them, and §0.2 records where this campaign
   departs from them.
4. SGK's code, through `git show c8a7f14:<path>` in the SGK checkout, never by opening the working
   tree's files: `RunRegistry/stores.py:1150-1400` (the section), `:185-207` (the format and its
   history comment, which stay in SGK), `:416-437` (`_fingerprint_problems`, for the shape SGK's
   sidecar checks); `RunRegistry/tests/test_store_fingerprint.py` (its docstring, its helpers
   `:88-136`, and its tests 1–6, `:138-457`), for what to restate.
5. The package: `datastorekit/store_inventory.py` (its docstring; `canonical`, `canonical_json`
   and `digest`, `:120-159`; `Record`, `:178-203`; `ClassInventory` and `StoreInventory`,
   `:371-497`); `datastorekit/tests/real_store_fixtures.py` (`build_full_store`, `:772-831`;
   `full_rows`, `:697-706`; `relabel_serials`, `:868-917`; `find_row` and `vary_row`, `:919-`);
   `datastorekit/tests/test_store_inventory.py` (its docstring; `_Stores`, `:189-221`; the tests
   that change a store, `:363-392`, `:504-641`, `:692-806`, for how to build each change);
   `datastorekit/tests/test_package_imports.py:60-` (a fresh-interpreter import test); the head
   of `datastorekit/tests/test_layer_is_generic.py` and of
   `datastorekit/tests/test_prose_names_no_source.py` (`RULES`, `:58-84`).
6. `docs/client-contract.md`: its head (`:1-61`), §4 (`:140-184`) and §9 (`:284-` end), for the
   form a §9 subsection takes.
7. `object-timestamp` prompt 01 and its log (`../object-timestamp/01-the-object-carries-a-timestamp.md`,
   `../object-timestamp/logs/01-the-object-carries-a-timestamp.md`): how a new test module, a
   contract §9 subsection and both ends were recorded last time.

Line numbers are at `5f972be` here and `c8a7f14` in SGK, measured on 2026-10-12.

---

## 1. What is wanted

After this prompt, **the package computes a store's fingerprint**:
- `datastorekit.store_fingerprint.fingerprint_of(inventory, fingerprint_format, taken=None)`
  gives, for an inventory and a client's format, exactly what SGK's `fingerprint_of` gives at that
  format, plus one key, `encoding_format`;
- `compare_fingerprints(recorded, current)` gives SGK's answer whenever both fingerprints carry
  the same `fingerprint_format` and `encoding_format`, and refuses otherwise;
- `listing_lines(inventory, fingerprint)` gives SGK's lines, its first line ending
  ` encoding_format <e>`;
- `ENCODING_FORMAT` is `1`, and the rule for bumping it is stated beside it and in contract §9.7.

The suite sees it, a golden fingerprint of the neutral store pins it, and a wrong move fails it.
SGK's code, run in scratch, agrees with it on the neutral store.

**Nothing else in the package changes**: not `store_inventory.py`, not any message, refusal or
exception of the layer. `pyproject.toml` stays at `0.3.0`: 02 releases.

### 1.1 What the planner measured

README §0.1 holds the measurements. The ones this prompt rests on:
- a prototype of this module, compared with a verbatim extract of SGK's five functions, gave equal
  fingerprints at formats 1 and 6 and equal comparisons on 27 changed stores, at both ends. Digests
  of the neutral full store: format 1 `7656b600965b5911a5046e7c0ebcd4dddce1c8ad277243d211b548487f22d304`,
  format 6 `bdf09575e8f8930677b4f040b4ba0d298dfc7277da9fb5205a31102d2d619b19`;
- with the prototype in the tree, the suite gave 509, `OK`, at both ends;
- the guards fail on SGK's section as it stands on exactly two lines of prose (SGK's campaign name
  in the section comment, SGK's package name in the lazy import's comment);
- `import datastorekit.store_inventory` loads `sqlalchemy` and not `ray`.

---

## 2. What to change

### 2.1 `datastorekit/store_fingerprint.py` (U1–U3)

A new module. **Its code is SGK's** (`RunRegistry/stores.py:1164-1400` at `c8a7f14`), changed only
as follows:

1. **The module docstring**, written for the package: a fingerprint is a pure function of a
   `StoreInventory` (`read_inventory`'s answer); what it holds, from SGK's section comment
   (`:1150-1162`) and `fingerprint_of`'s docstring, in neutral terms: a record's canonical line is
   `record.canonical_json()`; a digest is SHA-256 over canonical lines, each followed by `"\n"`, in
   the inventory's order, which is sorted by canonical JSON, so a listing's lines hash to the
   digests it lists; problems are counted by name beside the digests, never in them, since their
   text names shards and serials. Then the **two versions**: the client's `fingerprint_format`,
   which the client gives and bumps when what goes into its fingerprint changes, and which is in
   the overall digest; and this package's `encoding_format`, which is beside the digest and not in
   it. Name no client, no client's format number and no client's history.
2. **Imports at module scope:** `hashlib`, `collections.Counter`, the `typing` names you use, and
   `from datastorekit.store_inventory import canonical_json`. Remove SGK's two function-level
   imports of it and their comment.
3. **`ENCODING_FORMAT = 1`**, after the imports, under a comment that states the bump rule of
   README §6.2 U3 in full: the general rule and its eight items, that a bump adds a new golden
   fingerprint beside the old in the same commit, and that a change to a client's specs or registry
   is the client's format, never this one. Keep it in step with §2.5's §9.7: the same items, in the
   same order.
4. **`fingerprint_of(inventory, fingerprint_format: int, taken: Optional[Mapping[str, Any]] =
   None) -> dict`**: no `*`; the format is required, and has no default. Before reading the inventory: a `fingerprint_format` that is a `bool`, or not
   an `int`, raises `TypeError`; an `int` below 1 raises `ValueError`. Each message names the
   function, the argument and the value given. Then SGK's body, with `fingerprint_format` where SGK
   reads `FINGERPRINT_FORMAT`, and the returned dict gaining `"encoding_format": ENCODING_FORMAT`
   after `"fingerprint_format"`. **The `overall` object is SGK's exactly**: `{"fingerprint_format":
   fingerprint_format, "classes": {name: {"count", "digest"}}}`. Its docstring: SGK's list of keys,
   with `encoding_format` added and `taken` described as "the caller's mapping, copied, or `None`",
   naming no keys of it.
5. **`compare_fingerprints(recorded, current) -> list`**. First the versions: for
   `fingerprint_format`, then `encoding_format`, if the two fingerprints' values differ
   (`.get()`, so an absent key is `None`), one entry. The `fingerprint_format` entry is **SGK's
   exactly**: kind `"format"`, `class` and `tags` `None`, `recorded` and `current` the two values,
   and SGK's text verbatim. The `encoding_format` entry has kind `"encoding"`, the same fields, and
   a text in SGK's form: the recorded fingerprint is encoding format *r* and this one *c*;
   fingerprints encoded by different releases of `datastorekit` are not compared; recompute both
   from the stores with one release. If either entry was made, return the entries and compare
   nothing else. Otherwise SGK's body from `out = []` on, unchanged. Its docstring: SGK's, with the
   two versions and the `encoding` kind added.
6. **`listing_lines(inventory, fingerprint)`**. SGK's body, the first line becoming
   `f"# fingerprint_format {…} digest {…} encoding_format {…}"`: the new field **after** the
   digest, so the line's words 2 and 4 are SGK's. Its docstring: SGK's, saying so.
7. **The helpers** `_sha256_lines`, `_tag_sets`, `_tags_text`, `_difference` and `_presence`:
   SGK's, unchanged but for their docstrings' wording where it names anything of SGK.
8. **Nothing else** of SGK's file: not `TAKEN_KEYS`, not `write_listing`, not
   `fingerprint_store`, not the history comment.

**This file is in the layer.** The guards scan it: `test_layer_is_generic` (names, strings,
docstrings and comments against every client's vocabulary) and `test_prose_names_no_source`
(comments and docstrings against SGK's paths, modules, names and campaigns, `store-fingerprint`
among them). `test_package_imports` checks its imports. Say in the log how each passed, and how
you chose words that SGK's prose used and the guard forbids.

### 2.2 The golden fingerprint (U4)

`datastorekit/tests/data/store_fingerprint-neutral-1-encoding-1.json`: `fingerprint_of` of the
neutral full store, `read_inventory(build_full_store(<tmp>).primary, factories)` with the neutral
registry, at `fingerprint_format=1`, `taken` `None`; written with `json.dumps(…, indent=2,
sort_keys=True)` and a final newline, by a script you keep in the log, not in the repository. Its
digest must be the planner's (§1.1); if it is not, stop. It is written once and never rewritten
(README §5 rule 11).

### 2.3 A new test module, `datastorekit/tests/test_store_fingerprint.py` (U4)

Its docstring numbers its tests, as `test_store_inventory`'s does, and says no test starts Ray or
constructs a `ShardedPool`, and every store is in a temporary directory. A constant
`NEUTRAL_FORMAT = 1` stands for a client's format: say in a comment that it is bumped, with a new
golden beside the old, when the neutral client's specs or full store change what the fingerprint
sees. `GOLDEN` names the file for (`NEUTRAL_FORMAT`, `ENCODING_FORMAT`), built from both. Stores
are built as `test_store_inventory._Stores` builds them; reuse it by import or restate it. Tests,
README §6.2 U4, each restating SGK's in substance over the neutral store:

1. **Physical.** `relabel_serials` of `full_rows()`, and the same rows moved to other shards (as
   `test_store_inventory.TestKeysArePhysical` moves them), each give a fingerprint equal to the
   baseline's but for `taken`, and `compare_fingerprints` gives `[]`.
2. **Localised.** For each change — one sharded record deleted; one tag added to one record of a
   tagged class; one value row deleted; one validated flag flipped — the set of changed
   `(class, None)` and `(class, tags)` entries is exactly the set you name for it, derived from the
   fixture's rows and stated in the test, and the comparison's entries name exactly those. An orphan
   value row gives a fingerprint whose `problems` is exactly `{<class>: {"orphan-value": 1}}`, and
   a comparison with one `problems` entry and no content entry for that class. Name each expected set
   in the log, and how you derived it.
3. **Not content.** Every `timestamp` of every row changed gives an equal fingerprint, and no record
   line contains a timestamp.
4. **The golden.** `GOLDEN` exists; the baseline equals it but for `taken`, and so does a second
   build; the key set is exactly `{"fingerprint_format", "encoding_format", "classes", "digest",
   "problems", "taken"}`; `encoding_format` is `ENCODING_FORMAT` and `fingerprint_format`
   `NEUTRAL_FORMAT`; classes are in the inventory's order and each count is the inventory's;
   each class's tag-set counts sum to its count, and an untagged class has one tag set, `[]`; the
   overall digest equals SHA-256 of `canonical_json({"fingerprint_format": NEUTRAL_FORMAT,
   "classes": {name: {"count", "digest"}}})`, recomputed in the test; `taken` given is copied (a
   different object, equal), and outside every digest and the comparison.
5. **The listing.** For the baseline: the first line's words are `#`, `fingerprint_format`, the
   format, `digest`, the digest, `encoding_format`, the encoding format, exactly seven; each
   class header's count and digest are the fingerprint's; the record lines under each tag-set
   header hash to that header's digest, and a class's record lines, sorted, hash to its digest.
   Parse the listing in the test, as SGK's `parse_listing` does, by word position.
6. **The versions.** On two fingerprints built as SGK's `TestFormats` builds them, plus
   `encoding_format`: client formats 1 and 2 give exactly one entry, kind `format`, `(1, 2)`, its
   text containing "Recompute both" and equal to SGK's text for those values (write SGK's expected
   text into the test as a literal); encoding formats 1 and 2 one entry, kind `encoding`; both
   differing, two entries, `format` then `encoding`; a recorded fingerprint without
   `encoding_format`, one `encoding` entry with `recorded` `None`; equal versions, `[]`. And on the
   neutral store: the baseline compared with itself re-stamped with another `encoding_format` gives
   only the `encoding` entry, though every digest is equal.
7. **The arguments.** `fingerprint_of(inventory, 1)` and `fingerprint_of(inventory,
   fingerprint_format=1)` give equal fingerprints. A missing `fingerprint_format` raises
   `TypeError`; so do `True`, `"1"`, `1.0` and a `taken`-shaped dict passed in its place
   (`fingerprint_of(inventory, {"when": "now"})`, the call SGK must rewrite); `0` and `-1` raise
   `ValueError`. At
   `fingerprint_format=2` every class's entries equal the baseline's, and the overall digest
   differs.
8. **Purity and imports.** `fingerprint_of`, `compare_fingerprints` and `listing_lines` leave their
   arguments equal to deep copies taken before the call, and the store's files unchanged
   (`real_store_fixtures.file_state`); in a fresh interpreter (`subprocess`, as
   `test_package_imports` does), `import datastorekit.store_fingerprint` leaves `"ray"` out of
   `sys.modules`.

**The test is not a port.** It is not added to `docs/extraction/compare_ported_tests.py`'s
`PORTED`: SGK's fingerprint tests were not in the import (`PROVENANCE.md`). The port check must
still report "20 module(s) … 1 test(s) declared not ported".

### 2.4 The equivalence check against SGK's code (U5)

In a scratch directory **outside this repository**:
1. `git -C /Users/ds283/Documents/Code/SecondaryGWKit show c8a7f14:RunRegistry/stores.py | sed -n
   1164,1400p` into a file; record its SHA-256. Prepend `import hashlib`, `from collections import
   Counter` and a `FINGERPRINT_FORMAT` the script sets; nothing else in it changes. It imports
   `canonical_json` from the package, as SGK's does.
2. A script that, for the neutral full store and for **every** change of §0.1's prototype (the last
   row of each table with rows deleted, on each shard and among the replicated rows: 27 stores),
   asserts at `FINGERPRINT_FORMAT` 1 and 6 that the package's fingerprint, less `encoding_format`,
   equals SGK's, and that `compare_fingerprints` of the baseline with each gives equal lists from
   both. Add the changes of §2.3 test 2.
3. Run it at both ends (§4.1's venvs), with your tree's package. Record the script in full, its
   output, and the two digests of §1.1.

Nothing of SGK is imported as a module of SGK, installed or committed, and no SGK store, test or
working-tree file is opened.

### 2.5 `docs/client-contract.md`

- **At the head**, after the §9.6 line: *"§9.7 is measured from the package at `fingerprint`
  prompt 01's tree, and its line numbers are that tree's."*
- **The intro paragraph** (`:43-`, "A client of `datastorekit` gives the layer a fixed set of
  facts …") is not rewritten.
- **A §9.7, "`fingerprint` prompt 01"**, after §9.6, in §9's form. Its preamble: one change
  (`prompts/fingerprint/README.md`, decisions U1–U3, the user's ruling); nothing the layer writes
  or reads changes, and no message, refusal or exception of the layer's; what a client gives is
  its own format number, which it keeps and bumps. Rows:
  - **`fingerprint_of`**. Supersedes none. What holds (`store_fingerprint.py`, at 01's tree): the
    signature and its refusals; the fingerprint's keys; what each digest is over; the overall
    digest's object; what is outside every digest. **What a client supplies:** its
    `fingerprint_format`, an `int` ≥ 1 it bumps when its specs or registry change what the
    fingerprint sees; never `ENCODING_FORMAT`. Pinned by tests 1–4, 7, 8.
  - **`compare_fingerprints`**. The two versions, the entry kinds (`format`, `encoding`, `class`,
    `tag_set`, `digest`, `problems`), and that `taken` is never compared. Pinned by tests 2, 4, 6.
  - **`listing_lines`**. Its lines, and its first line's seven words. Pinned by test 5.
  - **`ENCODING_FORMAT` and when it is bumped**: the rule of README §6.2 U3, its eight items in the
    order of §2.1 item 3, each naming the function or field of `store_inventory.py` or
    `store_fingerprint.py` it means, at 01's tree; that a bump adds a golden beside the old
    (`tests/data/`), and that the release carrying it says so to every client. Pinned by test 4
    (the golden is keyed on it).
- **No marker** is set on any row of §1–§9.6. **Nothing in §1–§9.6 changes**: the diff of the file
  is `+` lines only.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **The digest.** The overall digest hashes SGK's object exactly. One more key in it, a renamed
   key, or `encoding_format` placed inside it, moves every client's digest. Test 4 recomputes it,
   and §2.4 compares it with SGK's.
2. **The guards** (§2.1, last paragraph). Both run in the suite.
3. **SGK's text.** The `format` entry's text is SGK's verbatim; SGK's `TestFormats` reads it.
4. **The listing's word positions** (§2.1 item 6).
5. **`store_inventory.py` is not changed.** If the move seems to need it, stop.
6. **The port check** (§2.3, last paragraph).
7. **Additive documents.** `git diff` of `docs/client-contract.md` shows `+` lines only.
8. **No Ray.** No test or script of this prompt starts Ray; each venv's run ends with Ray not
   initialised.
9. **Offline only.** Every venv is made `--offline`. A pin that does not resolve offline is a stop.
10. **The clients.** None is written, run (but §2.4's extract), imported or opened. Record each
    one's `HEAD` and `git status --short` at the start and the end.

---

## 4. Verification

1. **The suite.** `Ran 509 tests … OK` in `venv/` before; after, 509 plus the new tests, `OK`, at
   both ends: `venv/`, and a fresh offline scratch venv (Python 3.13.16, `ray==2.55.1`,
   `sqlalchemy==2.0.46`, `setuptools`) with a `git archive` of your tree installed editable
   (`--no-deps --no-build-isolation`). Record the `ResourceWarning` lines at each end (0 in
   `venv/`; 0 or 4 at the high end is timing, `actor-names` log 01 correction 8).
2. **The checks.** `docs/extraction/compare_ported_tests.py` exits 0 with "20 module(s) … 1 test(s)
   declared not ported"; `./venv/bin/black --check datastorekit docs` passes, at 78 files (76 at
   `5f972be`, measured 2026-10-12, plus the module and its test).
3. **The equivalence check** (§2.4), at both ends.
4. **The breakage record.** Each a diff exactly as applied in a scratch export, checked with
   `git apply --check` and `-R --check`, with what failed. None is committed.
   - **(a)** `"encoding_format"` added to the `overall` object: test 4 fails (the recomputed digest
     and the golden), and §2.4 fails.
   - **(b)** the overall object's key `"fingerprint_format"` renamed: test 4 fails.
   - **(c)** `compare_fingerprints` checking `fingerprint_format` only: test 6 fails.
   - **(d)** the `format` entry's text changed by one word: test 6 fails.
   - **(e)** `encoding_format` placed before `digest` in the listing's first line: test 5 fails.
   - **(f)** `_tag_sets` grouping by sorted tags (`tuple(sorted(record.tags))`) — a change a reader
     might think harmless. Say whether the tests catch it, and why: `Record.tags` is already sorted,
     so it may change nothing; if it changes nothing, record that it is equivalent, not a gap.
   - **(g)** `_sha256_lines` omitting the newline after the last line: tests 4 and 5 fail.
   - **(h)** `fingerprint_format` given a default of `1`: test 7 fails (the missing format).
   - **(j)** the integer check removed: test 7 fails (the dict, the string and the bool are hashed).
   - **(i)** `problems` counted by the whole problem string, not its name: test 2's orphan case
     fails (its `problems` dict).
5. **The documents.** Every name §2.5 cites exists at your tree: functions and fields by importing
   them in `venv/`, line numbers by reading them. List each in the log.
6. **The clients**, at the start and the end, unchanged (hazard 10).

---

## 5. Acceptance

1. `store_fingerprint.py` is as §2.1 says. Compare its functions' `ast`, docstrings removed, with
   those of SGK's extract (§2.4 item 1): `_sha256_lines`, `_tag_sets`, `_tags_text`, `_difference`
   and `_presence` are equal; `fingerprint_of`, `compare_fingerprints` and `listing_lines` differ
   only as §2.1 items 4–6 say. Say how in the log, and list every difference.
2. §2.2–§2.5 are done; `store_inventory.py`, the neutral client and every other file under
   `datastorekit/` are unchanged.
3. §4.1–§4.6 hold.
4. **The records**, in the same commit:
   - the log `logs/01-the-fingerprint-moves-into-the-package.md`, per README §5.1, with the
     equivalence script and its output, the golden's script, the breakage diffs, each name checked,
     and the clients at the start and the end;
   - this board: §1's row for 01, the header, and the decisions table if any changed;
   - this campaign's README: its header and §2's row for 01;
   - `docs/OPEN_ISSUES.md`: unchanged at **4**, unless the work opens an issue;
   - `prompts/INDEX.md`: the campaign's line.

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count falls, in any venv.
- The golden's digest is not the planner's (§1.1), or §2.4 finds any difference from SGK's.
- A test of §2.3 passes under a breakage of §4.4 that it is named to catch, or fails after the
  change for a reason other than a bug in the test.
- Any change to `store_inventory.py`, or to any file under `datastorekit/` but the new module, its
  test module and the golden, would be needed; or any change of the layer's messages, refusals or
  exceptions.
- The guards fail on the new module and cannot be satisfied by rewording.
- The port check fails.
- A document cannot say what it must without rewriting a line already in it.
- Anything would start Ray, push, make or move a tag, download, or write, run (but §2.4), import or
  open anything of a client.

---

## 7. What this prompt changes, and what it does not

- **Files it changes:**
  - the new `datastorekit/store_fingerprint.py`;
  - the new `datastorekit/tests/test_store_fingerprint.py` and
    `datastorekit/tests/data/store_fingerprint-neutral-1-encoding-1.json`;
  - `docs/client-contract.md`, by addition only;
  - the log, this board, this campaign's README, `docs/OPEN_ISSUES.md` if an issue is opened, and
    `prompts/INDEX.md`.
- **It changes nothing else:** not `store_inventory.py`, `pyproject.toml`, `README.md`,
  `PROVENANCE.md`, `docs/adoption/`, `docs/extraction/`, `docs/extraction-verification.md`, the
  workflow, `CLAUDE.md`, `LICENSE` or `.gitignore`. 02 changes the release's files.
- **It touches no client repository.**
- **It makes no tag and pushes nothing.**

---

## 8. After 01

The orchestrator reviews 01 against its commit, and replays §2.4. 02, the release, is then written
against the tree 01 leaves, and carries the adoption addenda, SGK's saying what it must do (README
§6.2, U6).
