# Campaign — fingerprint

**Written:** 2026-10-12 by Claude Opus 5.5, at the user's request, from a brief written in a
SecondaryGWKit session (§0). **Prompt 01 is written** (2026-10-12). The user took U2–U6 as
recommended the same day, and U1 amended to a plain signature (§6.2); 01 was revised to match, and
is ready to be dispatched. Prompt 02, the release, is written after 01 has landed and been
reviewed, against the tree 01 leaves. **Prompt 01 landed** 2026-10-14 as `d1b61d6` (its
[log](logs/01-the-fingerprint-moves-into-the-package.md)), and was reviewed the same day.

## 0. Why this campaign exists

**The user's ruling (2026-10-12, SGK's D3).** SGK's `RunRegistry` moves to a repository of its own,
RunRegistryKit, shared by the three clients, and the store fingerprint splits by layer:
- **what goes into a fingerprint** stays in each client: its factories' `inventory_spec()`s, its
  registry, and a format number of its own;
- **how a fingerprint is encoded and digested** is this package's, **with a version of its own**;
- **when and where a fingerprint is taken and recorded** is RunRegistryKit's, which is handed a
  client's fingerprinter and treats the result as opaque.

The brief that carries the ruling is
`/Users/ds283/Documents/Code/SecondaryGWKit/prompts/runregistry-extraction/datastorekit-fingerprint-brief.md`,
written 2026-10-12 at DatastoreKit `d88615e` and SGK `c8a7f14`. Its reasoning is SGK's
`docs/runregistry-extraction-audit.md` §3. It is evidence, not a specification (`CLAUDE.md` rule
7): §0.1 re-measures it here, and where it and this repository's records disagree, the records are
right (§0.2). It leaves the campaign's name, its decisions, its shape and the version number to
this repository.

**What is missing.** A fingerprint is made in three layers. **A, the content** (which classes, and
each class's identity), is the client's: its factories' `inventory_spec()`s and its registry.
**B, the encoding** (a row becomes a `Record` and then a canonical line: `canonical`,
`canonical_json`, `reference_digest`, `Record.as_json`, the parent-set digest, the choice of a
replicated class's shard, the problem names), is this package's `store_inventory.py`. **C, the
algorithm** (SHA-256 per class and per tag set over canonical lines; the overall digest; problems
and `taken` outside every digest; `compare_fingerprints`; `listing_lines`), is still SGK's, in
`RunRegistry/stores.py:1164-1390` at `c8a7f14`. Layer C is a pure function of a `StoreInventory`.

**One number versions both A and B today, and it is the client's.** SGK's `FINGERPRINT_FORMAT`
went 1 → 6. Every bump came from a change to what SGK puts in a key, and three of them also
extended layer B to carry it (SGK's audit §3.2). Layer B has no version of its own. So a release of
this package that changed `canonical` would change every digest while each client's format stayed
the same, and `compare_fingerprints` would report a content difference in every class rather than
a format mismatch. One client's acceptance test has caught such a change so far: SGK's rehearsal
digest `39809dca…`, reproduced at every pin move. With three clients that is not enough, and the
gap is the package's to close.

**The change.**
1. **Layer C moves into the package**, as a module of its own beside `store_inventory`
   (`datastorekit/store_fingerprint.py`, U1): `fingerprint_of`, `compare_fingerprints`,
   `listing_lines`, and their helpers `_sha256_lines` and `_tag_sets`. Where SGK's code reads its
   `FINGERPRINT_FORMAT`, the package's takes the **client's format number** as an argument. The
   package names no client format.
2. **A version for layers B and C together**, `ENCODING_FORMAT`, recorded in every fingerprint as
   `encoding_format`, **beside** the overall digest and not inside what it hashes (U2).
   `compare_fingerprints` refuses to compare two fingerprints whose client format **or** encoding
   format differ.
3. **A rule for when `ENCODING_FORMAT` is bumped**, in the client contract and beside the constant
   (U3).
4. **A release** carrying all three, with an addendum for SGK saying what it must do to adopt it
   (prompt 02, U6).

**The constraint: SGK's digest must not move.** SGK's reference fingerprint is format 6, digest
`39809dcac5c7b231c6b4468f9ea6cc48a4ad9c3a52d469f18f43291f781b55d2`, 21 classes. So the object the
overall digest hashes stays exactly `{"fingerprint_format": <client format>, "classes": {name:
{"count", "digest"}}}`; the per-class and per-tag-set counts and digests stay as they are; and
`problems` and `taken` stay outside every digest. This package's tests cannot name SGK, so the
check of SGK's digest is SGK's: its R1 rehearsal (its prompt 04) fingerprints each store both ways,
with SGK's own code and with the package's at format 6, and requires every digest and count to be
equal. A difference there comes back to this repository as a defect.

### 0.1 Measurements taken by the planner (2026-10-12)

All at `5f972be`, whose `datastorekit/` is `v0.3.0`'s (`2f5417e`): `git diff --stat 2f5417e HEAD
-- datastorekit` is empty. The suite gives `Ran 509 tests … OK` in `venv/` (Python 3.12.15, Ray
2.43.0, SQLAlchemy 2.0.39). Nothing was committed.

**The brief's citations into SGK hold at `c8a7f14`.** `git show c8a7f14:RunRegistry/stores.py`:
`_sha256_lines` at `:1164`, `_tag_sets` at `:1173`, `fingerprint_of` at `:1182`,
`compare_fingerprints` at `:1256`, `listing_lines` at `:1376`, the file 2185 lines long. The
history comment is `:194-205`, `FINGERPRINT_FORMAT = 6` at `:206`. The section imports `hashlib`
and `Counter` at module scope, and `canonical_json` from `datastorekit.store_inventory` inside
`fingerprint_of` and `listing_lines`, "here, not at module scope: … `import RunRegistry` must not"
import sqlalchemy. Nothing else of layer B is read: `record.canonical_json()`, `record.tags`,
`cls.records`, `cls.problems` and `inventory.classes`. `RunRegistry/` is unchanged between
`c8a7f14` and SGK's `HEAD`, `a5a6f6d` (`git diff --stat`). SGK's three `store_inventory.py`
commits since format 6 are as the brief says, and `4c34f13`'s message records the fingerprint
unchanged.

**Which of SGK's callers meet the new signature.** Read through `git grep` at `c8a7f14`, outside
`prompts/` and `docs/`: `fingerprint_of` is called in `RunRegistry/stores.py:1500` (by
`fingerprint_store`), in `RunRegistry/tests/test_store_fingerprint.py` (seven sites, one of them
passing `taken` **positionally**, `:378`) and in `ObjectFactories/tests/test_quadsource_policy_key.py:411-419`;
`compare_fingerprints` in `stores.py:1529`, `test_store_fingerprint.py` and `test_store_retire.py:471`;
`listing_lines` in `stores.py:1432` (`write_listing`). Three of SGK's tests pin what this change
touches:
- `TestGolden.test_the_shape` (`test_store_fingerprint.py:358-374`) pins the fingerprint's key set
  as exactly `{"fingerprint_format", "classes", "digest", "problems", "taken"}`;
- `TestGolden.test_the_golden_fingerprint` (`:350-356`) compares the fingerprint with a golden file
  that has no `encoding_format`;
- `parse_listing` (`:114-136`) reads the listing's first line by word position: `words[2]` is the
  format and `words[4]` the digest. A field inserted before the digest would break it; a field
  appended after it does not (U2).

`TestFormats` (`:434-457`) builds fingerprints with no `encoding_format` on either side, and
asserts one `format` entry whose text contains "Recompute both". Under U2 both sides' encoding
format is absent, so equal, and the test's answer is unchanged. SGK's sidecar check,
`_fingerprint_problems` (`stores.py:416-437`), checks four keys and allows others, so a fingerprint
with `encoding_format` passes it unchanged.

**A prototype.** In a scratch export of `5f972be`, a module `datastorekit/fingerprint.py` was
written: SGK's five functions with `fingerprint_of(inventory, *, fingerprint_format, taken=None)`,
`encoding_format` beside the digest, `compare_fingerprints` checking both versions before SGK's
comparison body, and the listing's first line ending `… digest <d> encoding_format <n>`. It was
compared with **a verbatim copy of SGK's five functions**, extracted with `git show
c8a7f14:RunRegistry/stores.py` into a scratch file, given `FINGERPRINT_FORMAT` and the imports it
names, and run in scratch only (U5). Nothing of SGK was imported, and no SGK store was opened. On
the neutral client's full store (`tests/real_store_fixtures.build_full_store`, 13 classes, no
problems):
1. at format 1 and at format 6, the prototype's fingerprint equals SGK's in every field SGK's has,
   and adds `encoding_format` only. Digests: format 1 `7656b600965b5911…`, format 6
   `bdf09575e8f89306…`;
2. the same store under other serials (`relabel_serials`) and a second build give an equal
   fingerprint; their comparison is `[]`;
3. on **27 changed stores**, each with the last row of one table deleted (every table of shard 0,
   shard 1 and the replicated rows that has rows), both implementations give equal fingerprints and
   **equal comparisons**, every one non-empty, 13 of them with `problems` entries;
4. a client format mismatch gives one `format` entry; an encoding mismatch, or a recorded
   fingerprint without `encoding_format`, one `encoding` entry;
5. the listing's 68 lines begin with `# fingerprint_format 1 digest 7656b600… encoding_format 1`,
   whose `words[2]` and `words[4]` are SGK's;
6. `fingerprint_format` given as `True`, `"1"` or `1.0` raises `TypeError`, as `0` raises
   `ValueError`, and given positionally raises `TypeError`.

Results, at both ends:
- **low end** (`venv/`) and **high end** (Python 3.13.16 / Ray 2.55.1 / SQLAlchemy 2.0.46, SQLite
  3.53.4; an offline scratch venv with the export installed editable): items 1–6 hold identically,
  the digests equal;
- with the prototype in the tree, and no new test, the suite gives `Ran 509 tests … OK` at both
  ends (`ResourceWarning` lines: 0 low, 4 high; `actor-names` log 01 correction 8 treats 0 or 4
  at the high end as timing);
- the guards (`test_layer_is_generic`, `test_prose_names_no_source`, `test_package_imports`) pass
  on the self-contained prototype. Run over SGK's section **as it stands**, they fail on exactly
  two lines of prose: the section comment naming SGK's campaign `store-fingerprint`, and the lazy
  import's comment naming SGK's package. Both are rewritten in the move (U1).

**What the neutral store exercises.** Its specs (`tests/client/factories.py`) have a polymorphic
parent (`Gadget.frame`, `Trace.frame`), a nullable and cross-shard parent (`Sample.anchor`), two
parent sets (`Sample.members`, `Weave.strands`), four tagged classes, two value tables, two
validated columns, and replicated and sharded classes. So a golden fingerprint of it covers every
part of layer B that `read_records` uses (U4).

**The clients**, read through `git` only: SGK `a5a6f6d` (clean; `requirements.txt:17` pins
`v0.2.2`); ChamPBH `5bb2be6` (23 entries in `git status --short`); SI `5fb4a1d` (clean).

### 0.2 Where the brief and this repository's records differ

None that changes the request. To be reported back to the SGK session with the tag:
1. **The tree.** The brief was written at `d88615e`, with `object-timestamp` in progress. That
   campaign is closed: `v0.3.0` was made on `2f5417e` (tag object `bf0a3b2`). `datastorekit/` is
   unchanged since `d88615e`; only `pyproject.toml`'s version moved. SGK's plan already moves its
   pin through `v0.2.3` and `v0.3.0` to this release.
2. **The signature.** The brief writes `fingerprint_of(inventory, taken=None)` with the format as
   a parameter. U1 makes it `fingerprint_of(inventory, fingerprint_format, taken=None)`, the
   format required and checked to be an integer. SGK's positional
   `fingerprint_of(inventory, taken)` (`test_store_fingerprint.py:378`) must be rewritten: it
   would pass its `taken` dict as the format, which the check refuses with `TypeError`.
3. **The name.** SGK's audit calls the version `inventory_format`. U2 names it `encoding_format`,
   since it versions the encoding and the algorithm and not the inventory's whole structure (whose
   timestamps, problem texts and members are outside every digest).
4. **The listing's first line** gains ` encoding_format <n>` at its end (U2), so that SGK's
   `parse_listing` reads it unchanged.
5. **SGK's own tests that will need changing** when SGK calls the package's code (its prompt 06):
   `test_the_shape`'s key set, and the golden comparison (its golden files have no
   `encoding_format`). These are SGK's; the addendum names them (02).
6. **The version.** By this repository's criteria a release that adds API is minor (U6): the brief
   leaves the number open, and U6 recommends `v0.4.0`.

## 1. Scope

**In scope:**
- `datastorekit/store_fingerprint.py`: the moved functions, the client's format as an argument,
  `ENCODING_FORMAT` and its bump rule (U1–U3);
- `datastorekit/tests/test_store_fingerprint.py` and a golden fingerprint of the neutral store in
  `datastorekit/tests/data/` (U4);
- the equivalence check against SGK's code, in scratch, recorded in 01's log (U5);
- `docs/client-contract.md`: a §9.7 holding the fingerprint's form and the bump rule;
- the release (prompt 02, U6), with adoption addenda, the SGK one saying what SGK must do.

**Out of scope:**
- **any client repository** (`CLAUDE.md`). SGK adopts the release in its own campaign
  (`runregistry-extraction`, prompts 03, 04 and 06);
- **any change to layer B.** `store_inventory.py` is not changed: not `canonical`, not
  `Record`, not the problem names. If 01 finds that the moved code needs a change there, it stops;
- **a fixture for RunRegistryKit** (the brief's §4, advice). A supported, shipped store fixture
  would be a new public surface: factories in the wheel, under the layer guard, with a schema to
  keep stable for another package's tests. RunRegistryKit treats a fingerprint as opaque, and can
  write its own small neutral factories, as this package's tests do. If it asks, that is a separate
  request;
- **a canonical form of an `InventorySpec`** (the brief's §4). SGK stringifies a polymorphic
  `Parent.types`'s keys itself, and asks nothing;
- **a second value table per spec** (the brief's §4), until SI's prompt 10 settles it and the user
  asks;
- **a convenience that reads a store and fingerprints it.** `read_inventory` and `fingerprint_of`
  compose in one line, and the client's fingerprinter is where they meet;
- **Ray.** The fingerprint is a pure function of an inventory, and `read_inventory` needs no Ray.
  Nothing crosses an actor, so no smoke run (U4);
- the four issues inherited from SGK (`docs/OPEN_ISSUES.md` §1.2), and anything else a prompt
  finds: it is recorded, not fixed (§5 rule 4). A later fix of
  `[00-the-inventory-cannot-see-a-serial-split]` that changes a record, a line or a problem name
  would bump `ENCODING_FORMAT` under U3.

## 2. Prompts

| # | Prompt | Covers | Status |
|---|---|---|---|
| 01 | [`01-the-fingerprint-moves-into-the-package.md`](01-the-fingerprint-moves-into-the-package.md) | `datastorekit/store_fingerprint.py`: the moved functions, the client's format as a required argument (U1); `ENCODING_FORMAT`, `encoding_format` beside the digest, both versions refused on mismatch, the listing's first line (U2); the bump rule (U3); `tests/test_store_fingerprint.py` and the golden (U4); the equivalence check against SGK's code, in scratch (U5); contract §9.7. | **written** 2026-10-12; U1–U5 taken; **landed** 2026-10-14, `d1b61d6` ([log](logs/01-the-fingerprint-moves-into-the-package.md)); **reviewed** 2026-10-14 |
| 02 | Release `v0.4.0` (planned) | `pyproject.toml`, `README.md`, `PROVENANCE.md` (the module's source, SGK `c8a7f14`); dated addenda to `docs/adoption/` (the README and the three checklists; SGK's says what it must do to adopt); both ends locally and in CI; **the tag** on its commit after green CI, not by the prompt. | not written; U6 taken |

**Order.** 01 → 02. 02 releases what 01 leaves. Each is landed and reviewed on its own.

## 3. Datastores

No prompt opens a store of any client. Tests build their stores in `tempfile` directories with the
neutral client's fixtures.

## 4. The interfaces between prompts

- **After 01:** `datastorekit.store_fingerprint` with `fingerprint_of`, `compare_fingerprints`,
  `listing_lines` and `ENCODING_FORMAT` (`1`); the golden fingerprint of the neutral store, at the
  neutral format and `ENCODING_FORMAT` 1; contract §9.7; the equivalence record in 01's log.
- **After 02:** `pyproject.toml` at the version U6 names; the adoption addenda. After its CI passes,
  the tag on 02's commit, and the tag object, the commit and the SGK addendum given to the user for
  SGK's gate E1.

## 5. The rules this campaign runs under

The project-wide ones in `CLAUDE.md`, plus:

1. **One commit per prompt**, in this repository only.
2. **Every prompt writes a log** to `logs/NN-<name>.md`, using §5.1.
3. **Every prompt updates `IMPLEMENTATION_STATE.md`** in its own commit, plus
   `docs/OPEN_ISSUES.md`.
4. **Do not fix things the prompt did not ask for.** A defect found is recorded with a §3 issue.
   Nothing rides in the release but U1–U3, unless the user rules otherwise.
5. **No prompt edits a client repository.** Reading one through `git` is allowed. Running a
   client's code or tests, or opening a client's store, is not, with **one exception** (U5):
   01 may run a copy of SGK's five fingerprint functions, extracted with `git show` at `c8a7f14`
   into a scratch file outside this repository, on the neutral client's stores, to compare with the
   package's. Nothing of SGK is imported, installed or committed.
6. **No test needs Ray, imports a client, or opens a store outside a `tempfile` directory.** The
   suite count is recorded before and after each prompt; a count that falls is a stop.
7. **Ray is not started** by any prompt of this campaign (U4).
8. **Deliberate breakage.** Each prompt names mutations its tests must catch. The log records each
   as a diff, exactly as applied, so the orchestrator can replay it with `git apply`. Mutations are
   never committed.
9. **No tag except where a prompt says so** (02), and none is moved or deleted. No prompt pushes.
10. **Verification documents are additive** (`CLAUDE.md` rule 6): a re-run that supersedes a
    measurement is a new dated subsection. A contract row is superseded by a §9 row, not rewritten.
11. **A golden fingerprint is never rewritten.** A change to it is a new file beside the old one,
    and a bump of the number that names it (U3, U4).

### 5.1 The log template

- the subject, commit and result;
- **What shipped**;
- **Deviations from the prompt**, each classified `STRUCTURALLY REQUIRED`, `IMPLEMENTATION CHOICE`
  or `UNINTENDED DRIFT`;
- **Verification performed**: the suite count before and after, at both ends, and the prompt's own
  checks;
- **The deliberate-breakage record**;
- **Observations not acted on**;
- **State handed to the next prompt**.

## 6. Decisions

### 6.1 Inherited, and not reopened here

The extraction campaign's decisions stand (its README §6), in particular U4 (clients pin a tagged
release), U23 and U28 (a tag is made on its prompt's commit only after CI passes there, each push
and tag with the user's approval) and U36 (a fix release is patch-level; U6 reads it). So do
`actor-names` U1–U4, `factory-defaults` U1–U5 and `object-timestamp` U1–U6. The G2–G4 wording of
`object-timestamp` U6 stands (G2 holds since 2026-10-12).

### 6.2 Decisions this campaign needs

- **U1: the module and its functions.** *(The move is the user's ruling, 2026-10-12. Its form
  taken 2026-10-12, amended by the user: a plain signature, not a keyword-only format; SGK fixes its
  own call sites.)* **Taken:**
  - a module **`datastorekit/store_fingerprint.py`**, beside `store_inventory.py` and
    `store_reader.py`, whose names it follows. It imports the standard library and
    `canonical_json` from `datastorekit.store_inventory` **at module scope**. Nothing is added to
    `datastorekit/__init__.py`;
  - **`fingerprint_of(inventory, fingerprint_format, taken=None)`**: `fingerprint_format`
    positional-or-keyword and required, an `int` of at least 1 (a `bool` or anything else raises
    `TypeError`, an `int` below 1 `ValueError`, each naming the value); `taken` a mapping copied
    with `dict()`, or `None`. Its body otherwise SGK's, with `fingerprint_format` where SGK's reads
    `FINGERPRINT_FORMAT`;
  - **`compare_fingerprints(recorded, current)`** and **`listing_lines(inventory, fingerprint)`**:
    SGK's signatures, and SGK's bodies but for U2;
  - `_sha256_lines`, `_tag_sets`, `_tags_text`, `_difference` and `_presence`: SGK's, private;
  - **docstrings rewritten for the package**: what each function returns, in SGK's terms where
    they are generic, naming no client and no client's history. SGK's history comment
    (`stores.py:194-205`) stays out, as the brief advises; it is SGK's and moves to SGK's client
    module. The `taken` docstring says it is the caller's mapping, outside every digest, and names
    no keys.

  **Why required.** The client's format is what the overall digest hashes, so forgetting it must
  fail, not default. **Why validate:** the format sits in the hashed object, and `canonical_json`
  would accept a string or a bool there silently, giving a digest that no integer format
  reproduces. SGK's sidecar check already requires an integer. The check also makes SGK's one
  positional `fingerprint_of(inventory, taken)` (`test_store_fingerprint.py:378`) fail loudly, with
  `TypeError`, rather than hash its `taken` dict as the format; SGK rewrites that call when it
  adopts (§0.2, point 2).

  **Why module scope.** SGK imported `canonical_json` lazily for its own reason, that `import
  RunRegistry` must not load sqlalchemy. In the package, sqlalchemy is a dependency, and
  `store_inventory` is imported at module scope by `SQL/schema.py:49`. Importing it loads
  sqlalchemy and `datastorekit.contract`, and not Ray: it imports the reader, which imports the
  pool, only inside `read_inventory`. So the new module loads no Ray either, and a lazy import
  would be a constraint with no reason here. RunRegistryKit's core imports nothing of this package
  (its `[stores]` extra does, SGK's audit §5.3), and a client that wants its fingerprinter cheap to
  import can import inside it.

  **Rejected:** a keyword-only format (the planner's first recommendation, 2026-10-12: it shaped
  the package's signature around one client's existing call site, which is the client's to fix);
  a defaulted format; the name `fingerprint.py` (the package names its store modules `store_*`);
  putting the functions in `store_inventory.py`, which would join layer C to the module whose
  float-formatting guard (`tests/test_store_inventory.py:446-500`) and docstring are about layer B;
  exporting from `datastorekit/__init__.py`, which exports only `DatastoreObject`; a lazy import.
- **U2: the version, where it sits, and what reads it.** *(Taken 2026-10-12, as recommended.)* **Recommended:**
  - a module constant **`ENCODING_FORMAT = 1`**, public, with its bump rule (U3) beside it;
  - every fingerprint carries **`"encoding_format": ENCODING_FORMAT`**, a key of the fingerprint's
    dictionary beside `fingerprint_format` and `digest`. It is **not** in the object the overall
    digest hashes, which stays `{"fingerprint_format", "classes"}` exactly, so that an unchanged
    inventory and client format give SGK's digest;
  - **`compare_fingerprints` refuses** when either version differs: it checks `fingerprint_format`,
    then `encoding_format`, and if either differs it returns one entry per version that differs and
    compares nothing else. A `fingerprint_format` mismatch keeps SGK's entry exactly: kind
    `format`, its `recorded` and `current`, and its text verbatim ("… fingerprints of different
    formats are not compared. Recompute both from the stores"). An `encoding_format` mismatch is an
    entry of kind **`encoding`**, whose text says the two were encoded by different releases of
    this package and are not compared, and to recompute both from the stores with one release. A
    fingerprint without `encoding_format` (one made before this release) differs from one with it,
    and is refused: no reader of old fingerprints is asked for (the brief, §3);
  - **`listing_lines`'s first line** becomes `# fingerprint_format <f> digest <d> encoding_format
    <e>`: the new field appended, so the first five words are SGK's. Nothing else in a listing
    changes.

  **Rejected:** the version inside the hashed object (it moves SGK's digest); the name
  `inventory_format` (§0.2, point 3); one `format` entry for either mismatch (a reader could not
  tell which side moved, and the remedy differs: the client's content, or the package's release);
  returning only the first mismatch (two numbers that moved are both worth saying); accepting a
  fingerprint without `encoding_format` as version 1 (a version-aware reader, which SGK's standing
  rule refuses and nothing asks for); the field before `digest` in the listing (it breaks SGK's
  `parse_listing`).
- **U3: when `ENCODING_FORMAT` is bumped.** *(Taken 2026-10-12, as recommended.)* **Recommended:** the rule is stated twice, in the same
  words: in a comment beside the constant, and in contract §9.7. **`ENCODING_FORMAT` is bumped by
  any change that can make the same store, read with the same specs and the same client format,
  give a different fingerprint, or make `compare_fingerprints` or `listing_lines` read one
  differently.** That is, a change to:
  1. what a record contains: `Record.as_json`'s fields or their values, including `value_count`
     and `validated`;
  2. how a leaf or a key becomes text: `canonical`, `canonical_json`, `digest`;
  3. how a reference becomes a key's value: `reference_digest`, the parent-set digest, how a
     polymorphic, nullable or cross-shard parent resolves;
  4. which rows become records, and which shard's copy of a replicated class is used;
  5. the order of a class's records, or how they are grouped into tag sets;
  6. the names of the problems (a fingerprint counts problems by name);
  7. how a digest is formed: `_sha256_lines`, the per-tag-set grouping, the overall digest's object;
  8. the fingerprint's keys, or what `compare_fingerprints` and `listing_lines` read from it.

  A bump adds a new golden fingerprint beside the old (§5 rule 11), in the same commit, and the
  release that carries it says so in `PROVENANCE.md` and in an addendum to every checklist, since
  every client's fingerprints then differ from those it holds. A change to a client's specs or registry is the
  client's format, never `ENCODING_FORMAT`. A change that the neutral golden does not see is still
  a bump if it is in the list: the golden is a guard, not the rule. **Rejected:** a rule stated only
  in the contract (the next editor of `store_inventory.py` reads the code); "any change to
  `store_inventory.py`" (most of its changes, such as the refusals of `bc8bffc`, move no digest,
  and a needless bump makes every client recompute).
- **U4: the tests.** *(Taken 2026-10-12, as recommended.)* **Recommended:** a new module, `datastorekit/tests/test_store_fingerprint.py`,
  always run, with no Ray, every store from `tests/real_store_fixtures.build_full_store` in a
  `tempfile` directory; and a golden fingerprint of the neutral store,
  `datastorekit/tests/data/store_fingerprint-neutral-1-encoding-1.json`. The neutral client's
  format is a constant of the test module, `NEUTRAL_FORMAT = 1`, standing for a client's: it is
  bumped, with a new golden, when the neutral client's specs or full store change what the
  fingerprint sees. Tests, ported in substance from SGK's `test_store_fingerprint` tests 1–6 and
  restated over the neutral store:
  1. **physical**: other serials, and the same rows on other shards, give an equal fingerprint and
     an empty comparison;
  2. **localised**: each of a deleted record, a tag added to one record, a deleted value row and a
     flipped validated flag moves exactly the class and tag-set entries it names, and the
     comparison names exactly those; an orphan gives a `problems` entry;
  3. **not content**: every timestamp changed gives an equal fingerprint;
  4. **the golden**: the fingerprint of `build_full_store()` at `NEUTRAL_FORMAT` equals the golden
     file for (`NEUTRAL_FORMAT`, `ENCODING_FORMAT`), which exists, and a second build gives the
     same; the shape is exactly `{"fingerprint_format", "encoding_format", "classes", "digest",
     "problems", "taken"}`; the overall digest is SHA-256 of `canonical_json` of the
     `{"fingerprint_format", "classes": {name: {"count", "digest"}}}` object, recomputed in the
     test; `taken` is copied and outside every digest;
  5. **the listing**: its lines under each header hash to the digests the header names, a class's
     record lines sorted hash to its digest, and the first line's words 2, 4 and 6 are the client
     format, the digest and the encoding format;
  6. **the versions**: a client-format mismatch gives exactly SGK's one `format` entry; an encoding
     mismatch one `encoding` entry; both, two entries in that order; a fingerprint without
     `encoding_format` one `encoding` entry; equal versions compare as before;
  7. **the arguments**: `fingerprint_format` missing, a `bool`, a string, a float, a mapping (a
     `taken` passed in its place) or `0` is refused as U1 says; given positionally or by keyword,
     it gives the same fingerprint; the fingerprint's `fingerprint_format` is the one given, and a
     different format gives a different overall digest with every class's entries unchanged;
  8. **purity**: `fingerprint_of`, `compare_fingerprints` and `listing_lines` open nothing and
     change neither argument; in a fresh interpreter, importing `datastorekit.store_fingerprint`
     loads no `ray` (as `import datastorekit.store_inventory` loads none today, measured
     2026-10-12).

  **Rejected:** a hand-built `StoreInventory` as the only golden (it would miss
  `reference_digest`, parent sets and the shard choice, which only a store exercises); keying the
  golden on `ENCODING_FORMAT` alone (a change to the neutral client would then look like an
  encoding change); a smoke step under Ray (nothing crosses an actor).
- **U5: the equivalence check against SGK's code.** *(Taken 2026-10-12, as recommended.)* **Recommended:** 01 extracts SGK's five
  functions with `git show c8a7f14:RunRegistry/stores.py`, lines `1164-1400`, into a scratch file
  outside this repository, prepends the imports they name and `FINGERPRINT_FORMAT`, and runs them
  beside the package's on the neutral store: at formats 1 and 6, every field of SGK's fingerprint
  equal, the package's adding `encoding_format` only; and on at least the 27 changed stores of
  §0.1's prototype, equal comparisons. The log records the script, its output and the extract's
  SHA-256. Nothing of SGK is imported, installed or committed, and no SGK store is opened. This
  amends §5 rule 5 for this one read, which earlier campaigns did not need. **Rejected:** no check
  here, leaving it all to SGK's R1 (a defect would then be found a campaign later, in another
  repository, after a tag); a committed copy of SGK's code as a test oracle (it names SGK's history
  in the package, and would be a second copy to keep).
- **U6: the shape, the release, and who adopts it.** *(Taken 2026-10-12, as recommended. Needed by 02, not 01.)* **Recommended:**
  - **two prompts**, as the last three campaigns: 01 the module and its evidence, 02 the release,
    written after 01 is reviewed;
  - **`v0.4.0`**, minor: the release adds a module and a constant. That is added API, which
    extraction U36 and `factory-defaults` U5 gave as the reason a release was *not* patch-level,
    and which made `v0.2.0` and `v0.3.0` minor;
  - **SGK adopts it**, by moving its pin from `v0.2.2` (its prompt 03) and calling the package's
    function from its client module (its prompt 06). The SGK addendum says what changes for it:
    the required format, and its positional `fingerprint_of(inventory, taken)` to rewrite;
    `encoding_format` in every fingerprint; the comparison's `encoding`
    entry; the listing's first line; the two tests of SGK's that pin the shape and the golden
    (§0.2, point 5); and that nothing in `v0.2.3` and `v0.3.0` asks anything of SGK;
  - **ChamPBH and SI may stay on their pins or move**, each in a commit of its own: nothing they
    call changes, and they meet the module only when they adopt RunRegistryKit;
  - the tag object, the commit and the SGK addendum's anchor are given to the user for SGK's gate
    E1.

  **Rejected:** one prompt for the module and the release; `v0.3.1`, treating a module as a patch;
  requiring ChamPBH or SI to move.

## 7. Gates outside this repository

None of this campaign's own. **SGK's `runregistry-extraction` waits on the tag** (its gate E1):
its prompts 03 and 04 are written when the tag exists, and cite it. RunRegistryKit's `[stores]`
extra will require `datastorekit>=` this release by name. When SGK's R1 has taken the fingerprint
both ways, its result is recorded on this board, in a records commit of its own; a difference is a
defect of this package, opened on this board.
