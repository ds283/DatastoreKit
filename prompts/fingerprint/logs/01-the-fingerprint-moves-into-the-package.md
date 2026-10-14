# Log 01 — the fingerprint moves into the package

**Subject:** Move the store fingerprint into the package, with its own version · **Commit:** this
commit · **Date:** 2026-10-14 · **Model:** Claude Opus 5.5 · **Result:** landed; unpushed and
untagged; not yet reviewed.

`datastorekit/store_fingerprint.py` is new: the source's five fingerprint functions and three
helpers (SGK `RunRegistry/stores.py:1164-1400` at `c8a7f14`), changed only as the prompt's §2.1
says. `fingerprint_of(inventory, fingerprint_format, taken=None)` takes the client's format as a
required argument, positional or by keyword, refused unless an `int` of at least 1 (U1); every
fingerprint carries `"encoding_format": ENCODING_FORMAT` beside the digest and outside the object it
hashes, which is the source's exactly; `compare_fingerprints` refuses on either version, with the
source's `format` entry verbatim and a new `encoding` entry; the listing's first line gains
` encoding_format <e>` at its end (U2). `ENCODING_FORMAT = 1`, under a comment stating its bump rule
in U3's eight items (U3). `store_inventory.py` and every other existing file under `datastorekit/`
are unchanged; no message, refusal or exception of the layer's changed. `pyproject.toml` stays at
`0.3.0`.

A new module of **21** tests, `datastorekit/tests/test_store_fingerprint.py`, and a golden
fingerprint of the neutral full store, `datastorekit/tests/data/store_fingerprint-neutral-1-encoding-1.json`
(digest `7656b600965b5911a5046e7c0ebcd4dddce1c8ad277243d211b548487f22d304`, the planner's), pin it
(U4). The suite goes from **509 to 530**, `OK`, in `venv/` and at the high end. Each breakage
(a)–(e), (g)–(j) fails the test it is named to catch, and (f) is equivalent (correction 5).

**The equivalence check** (U5): the source's section, extracted by `git show` into scratch and
loaded by path, run beside the package's module on the neutral full store and **37** changed stores
(correction 3's 28, and test 2's nine), at client formats 1 and 6: **0 differences**, at both ends.
Every fingerprint equals the source's but for `encoding_format`; every comparison is equal; the
68-line listing is the source's but for its first line's added field.

`docs/client-contract.md` gains a head line and §9.7, by addition only (19 lines added, none
removed). No issue was opened or closed: the index stays at **4 open**.

No client was written, run, imported or opened, but for the source's extract (U5); nothing was
pushed, tagged or downloaded; Ray was not started.

Prompt: [`../01-the-fingerprint-moves-into-the-package.md`](../01-the-fingerprint-moves-into-the-package.md),
with the orchestrator's dispatch note §0: six corrections, its additions, its checked facts and its
conventions. §2 classifies each.

`<scratch-fp01>` below is `<session scratchpad>/agent01`, outside the repository. Times are BST,
2026-10-14.

---

## 1. What shipped

### 1.1 The module (§2.1)

**`datastorekit/store_fingerprint.py`**, new, 351 lines. Line numbers are this commit's.

- **The module docstring** (`:1-30`), written for the package: a fingerprint is a pure function of
  a `StoreInventory`; a record's canonical line is `record.canonical_json()`; a digest is SHA-256
  over canonical lines, each followed by `"\n"`, in the inventory's order, sorted by canonical
  JSON, so a listing's lines hash to the digests it lists; problems are counted by name beside the
  digests, never in them. Then the two versions: the client's `fingerprint_format` (given, bumped
  by the client, in the overall digest) and this package's `encoding_format` (beside the digest,
  not in it). It names no client, no client format number and no client history, and says what
  the module imports.
- **Imports at module scope** (`:32-36`): `hashlib`, `collections.Counter`, `typing`'s `Any`,
  `Mapping`, `Optional`, and `from datastorekit.store_inventory import canonical_json`. The
  source's two function-level imports and their comment are gone.
- **`ENCODING_FORMAT = 1`** (`:65`), under a comment (`:38-64`) that states README §6.2 U3 in
  full: what the constant versions; the general rule; the eight items, in U3's order; that a bump
  adds a new golden beside the old in the same commit and never rewrites it (`tests/data/`); that
  the release says so in its provenance record and in an addendum to every client's adoption
  checklist; that a change the golden does not see is still a bump if listed; and that a change to
  a client's specs or registry is the client's `fingerprint_format`, never this one. Contract §9.7
  states the same items in the same order (§1.4).
- **`fingerprint_of(inventory, fingerprint_format: int, taken: Optional[Mapping[str, Any]] =
  None) -> dict`** (`:86-154`): no `*`, no default for the format. Before anything is read, a
  `bool` or a non-`int` raises `TypeError("fingerprint_of(): fingerprint_format must be an int,
  not <type name> <repr>")` (`:109-113`), and an `int` below 1 `ValueError("fingerprint_of():
  fingerprint_format must be at least 1, not <repr>")` (`:114-118`): each names the function, the
  argument and the value. Then the source's body, `fingerprint_format` where it read
  `FINGERPRINT_FORMAT` (twice), and the returned dict gaining `"encoding_format":
  ENCODING_FORMAT` after `"fingerprint_format"` (`:149`). The `overall` object (`:140-146`) is the
  source's exactly. Its docstring is the source's list of keys, with `encoding_format` added,
  `fingerprint_format` "as given", and `taken` "the caller's mapping, copied, or `None`", naming
  no keys of it; and it states the refusals.
- **`compare_fingerprints(recorded, current) -> list`** (`:178-319`): a list `versions` (`:194`);
  the `format` entry (`:195-209`), the source's exactly (kind, `None` class and tags, the two
  values, its text verbatim), appended if the two `.get("fingerprint_format")` differ; the
  `encoding` entry (`:210-225`), appended if the two `.get("encoding_format")` differ, with the
  text "the recorded fingerprint is encoding format *r* and this one is encoding format *c*;
  fingerprints encoded by different releases of datastorekit are not compared. Recompute both from
  the stores with one release"; `if versions: return versions` (`:226-227`). Then the source's body
  from `out = []` on, unchanged (`:229-319`). Its docstring is the source's, with the two versions
  and the `encoding` kind added.
- **`listing_lines(inventory, fingerprint)`** (`:322-351`): the source's body, its first line
  `f"# fingerprint_format {…} digest {…} encoding_format {fingerprint['encoding_format']}"`
  (`:336-340`), the encoding format read from the fingerprint (the orchestrator's addition) and
  placed after the digest. Its docstring is the source's, saying so and naming the word positions.
- **The helpers** `_sha256_lines` (`:68-74`), `_tag_sets` (`:77-83`), `_tags_text`, `_difference`
  and `_presence` (`:157-175`): the source's, unchanged, docstrings included (none named anything
  of the source).
- **Nothing else** of the source's file: not `TAKEN_KEYS`, `write_listing`, `fingerprint_store`
  or the history comment. Nothing is added to `datastorekit/__init__.py`.

**Acceptance 1, by `ast`** (`<scratch-fp01>/probe/ast_compare.py`, run on the extract with its
prepended lines and on the module): each `FunctionDef` with its docstring removed and its return
and argument annotations cleared, compared by `ast.dump`, with a `difflib` of `ast.unparse` where
they differ. The two files define the same eight functions in the same order. Result:

```
extract functions: ['_sha256_lines', '_tag_sets', 'fingerprint_of', '_tags_text', '_difference', '_presence', 'compare_fingerprints', 'listing_lines']
module functions:  ['_sha256_lines', '_tag_sets', 'fingerprint_of', '_tags_text', '_difference', '_presence', 'compare_fingerprints', 'listing_lines']
extract other top-level statements: ['Import', 'ImportFrom', 'FINGERPRINT_FORMAT']
module other top-level statements:  ['Expr', 'Import', 'ImportFrom', 'ImportFrom', 'ImportFrom', 'ENCODING_FORMAT']

_sha256_lines: EQUAL

_tag_sets: EQUAL

fingerprint_of: differs
    --- extract
    +++ module
    @@ -1,2 +1,5 @@
    -def fingerprint_of(inventory, taken=None):
    -    from datastorekit.store_inventory import canonical_json
    +def fingerprint_of(inventory, fingerprint_format, taken=None):
    +    if isinstance(fingerprint_format, bool) or not isinstance(fingerprint_format, int):
    +        raise TypeError(f'fingerprint_of(): fingerprint_format must be an int, not {type(fingerprint_format).__name__} {fingerprint_format!r}')
    +    if fingerprint_format < 1:
    +        raise ValueError(f'fingerprint_of(): fingerprint_format must be at least 1, not {fingerprint_format!r}')
    @@ -11,2 +14,2 @@
    -    overall = {'fingerprint_format': FINGERPRINT_FORMAT, 'classes': {name: {'count': entry['count'], 'digest': entry['digest']} for name, entry in classes.items()}}
    -    return {'fingerprint_format': FINGERPRINT_FORMAT, 'classes': classes, 'digest': hashlib.sha256(canonical_json(overall).encode('utf-8')).hexdigest(), 'problems': problems, 'taken': dict(taken) if taken is not None else None}
    +    overall = {'fingerprint_format': fingerprint_format, 'classes': {name: {'count': entry['count'], 'digest': entry['digest']} for name, entry in classes.items()}}
    +    return {'fingerprint_format': fingerprint_format, 'encoding_format': ENCODING_FORMAT, 'classes': classes, 'digest': hashlib.sha256(canonical_json(overall).encode('utf-8')).hexdigest(), 'problems': problems, 'taken': dict(taken) if taken is not None else None}

_tags_text: EQUAL

_difference: EQUAL

_presence: EQUAL

compare_fingerprints: differs
    --- extract
    +++ module
    @@ -1,0 +2 @@
    +    versions = []
    @@ -5 +6,7 @@
    -        return [_difference('format', None, None, recorded_format, current_format, f'the recorded fingerprint is format {recorded_format!r} and this one is format {current_format!r}; fingerprints of different formats are not compared. Recompute both from the stores')]
    +        versions.append(_difference('format', None, None, recorded_format, current_format, f'the recorded fingerprint is format {recorded_format!r} and this one is format {current_format!r}; fingerprints of different formats are not compared. Recompute both from the stores'))
    +    recorded_encoding = recorded.get('encoding_format')
    +    current_encoding = current.get('encoding_format')
    +    if recorded_encoding != current_encoding:
    +        versions.append(_difference('encoding', None, None, recorded_encoding, current_encoding, f'the recorded fingerprint is encoding format {recorded_encoding!r} and this one is encoding format {current_encoding!r}; fingerprints encoded by different releases of datastorekit are not compared. Recompute both from the stores with one release'))
    +    if versions:
    +        return versions

listing_lines: differs
    --- extract
    +++ module
    @@ -2,2 +2 @@
    -    from datastorekit.store_inventory import canonical_json
    -    yield f"# fingerprint_format {fingerprint['fingerprint_format']} digest {fingerprint['digest']}"
    +    yield f"# fingerprint_format {fingerprint['fingerprint_format']} digest {fingerprint['digest']} encoding_format {fingerprint['encoding_format']}"
```

So `_sha256_lines`, `_tag_sets`, `_tags_text`, `_difference` and `_presence` are equal, and the
three functions differ exactly as §2.1 items 4–6 say: `fingerprint_of` by its argument, the two
checks, the removed lazy import, `fingerprint_format` for `FINGERPRINT_FORMAT` (twice) and the
added key; `compare_fingerprints` by the versions block before `out = []` (the `format` entry's
call is identical, appended rather than returned); `listing_lines` by the removed import and its
first `yield`. The module's other top-level statements are its docstring, its four imports and
`ENCODING_FORMAT`; the extract's are the three prepended lines.

**How the prose passes the guards.** The source's section comment and docstrings were rewritten,
not copied, where they named anything of the source: its campaign name (`store-fingerprint`) and
its package name (in the lazy import's comment) are gone with the comment and the import; its
`FINGERPRINT_FORMAT` became "the client's format" / "``fingerprint_format``, as given"; its
`taken` keys are not named; "store-local" became "belong to one store and not to its content";
`fingerprint_of(inventory)` in the listing's docstring became `fingerprint_of(inventory,
fingerprint_format)`. The guard's fragment `_tags` occurs only in the name `_tags_text`, which the
string and comment scans do not read, and in no docstring or comment. `test_layer_is_generic`
(its `layer_files()` lists the new module), `test_prose_names_no_source` and
`test_package_imports` pass on it (§4.2).

### 1.2 The golden (§2.2)

`datastorekit/tests/data/store_fingerprint-neutral-1-encoding-1.json`, 193 lines, SHA-256
`03db714952565e0997cb7be43115a930db6a1b13ac62bc8de10eff35b11a018e`, digest
`7656b600965b5911a5046e7c0ebcd4dddce1c8ad277243d211b548487f22d304` (the planner's, §1.1). Keys
`classes`, `digest`, `encoding_format` (1), `fingerprint_format` (1), `problems` (`{}`), `taken`
(`null`); 13 classes; tagged: `Gadget` (2 sets), `Sample` (2), `Trace` (3), `Weave` (1). Written
once, in `venv/`, after the equivalence check had passed at both ends, by this script
(`<scratch-fp01>/probe/write_golden.py`, run as `venv/bin/python -I write_golden.py <repository>`
from `<scratch-fp01>/probe`), which refuses to overwrite and stops on any other digest:

```python
"""Write the golden fingerprint of the neutral full store (fingerprint prompt 01, section 2.2).

usage: python -I write_golden.py <repository root>
"""

import json
import sys
import tempfile
from pathlib import Path

from datastorekit.store_fingerprint import ENCODING_FORMAT, fingerprint_of
from datastorekit.store_inventory import read_inventory
from datastorekit.tests.client.registry import factories
from datastorekit.tests.real_store_fixtures import build_full_store

NEUTRAL_FORMAT = 1
EXPECTED = "7656b600965b5911a5046e7c0ebcd4dddce1c8ad277243d211b548487f22d304"

root = Path(sys.argv[1])
target = (
    root
    / "datastorekit"
    / "tests"
    / "data"
    / f"store_fingerprint-neutral-{NEUTRAL_FORMAT}-encoding-{ENCODING_FORMAT}.json"
)
if target.exists():
    sys.exit(f"{target} exists: a golden is never rewritten")
with tempfile.TemporaryDirectory() as tmp:
    inventory = read_inventory(build_full_store(Path(tmp)).primary, factories)
    fingerprint = fingerprint_of(inventory, fingerprint_format=NEUTRAL_FORMAT)
if fingerprint["digest"] != EXPECTED:
    sys.exit(f"digest {fingerprint['digest']} is not the planner's {EXPECTED}")
target.write_text(json.dumps(fingerprint, indent=2, sort_keys=True) + "\n")
print(target, fingerprint["digest"])
```

### 1.3 The test module (§2.3)

**`datastorekit/tests/test_store_fingerprint.py`**, new, 711 lines, **21 tests** in 8 classes. Its
docstring numbers its tests 1–8 and says no test starts Ray or constructs a `ShardedPool`, and every
store is in a temporary directory; `tearDownModule` asserts Ray is not initialised (if it was ever
imported). `NEUTRAL_FORMAT = 1`, under a comment saying it stands for a client's format and is
bumped, with a new golden beside the old, when the neutral client's specs or full store change what
the fingerprint sees. `GOLDEN` is built from `NEUTRAL_FORMAT` and `ENCODING_FORMAT`. The stores are
built by `_FullStores`, which restates `test_store_inventory._Stores` (the source's names:
`baseline_inventory`, an inventory, and `baseline`, its fingerprint), so nothing is imported from
another test module.

| # | Class | Tests | What each does |
|---|---|---|---|
| 1 | `TestPhysical` | `test_other_serials_and_other_shards` | Three sub-tests, as `TestKeysArePhysical` builds them: `relabel_serials(offset=100)`; the sharded rows moved to a third shard (`shards=3`); `relabel_serials(offset=37)` with the two shards swapped. Each: the fingerprint equals the baseline's but for `taken`, and `compare_fingerprints` gives `[]` |
| 2 | `TestLocalised` | 7 | `assertLocalised`: the changed entries are exactly the named set; every class it does not name has the baseline's records, and every class it names has changed records; the overall digest changed and `problems` did not; the comparison is one `tag_set` entry per tag set named, with the stated (recorded, current) counts. The cases are §2.3 below |
| 3 | `TestNotContent` | `test_timestamps`, `test_no_timestamp_is_in_any_record_line` | Every `timestamp` of every row set to 2031-02-03 04:05:06 (the inventory's `earliest_timestamp` shows it took): the fingerprint is equal but for `taken`, and the comparison `[]`. No line of the baseline's listing contains `str(FIXED_TIMESTAMP)`, its `isoformat()` or `2026-09-24` |
| 4 | `TestGolden` | `test_the_golden_fingerprint`, `test_the_shape_and_the_overall_digest`, `test_taken_is_copied_and_outside_every_digest` | `GOLDEN` is a file; its formats are `NEUTRAL_FORMAT` and `ENCODING_FORMAT`, its `taken` `None`; the baseline and a second build equal it but for `taken`. The key set exactly; `encoding_format` `ENCODING_FORMAT` (and `ENCODING_FORMAT` 1), `fingerprint_format` `NEUTRAL_FORMAT`; `problems` `{}`; classes in the inventory's order, each with keys `count`, `digest`, `tag_sets`, its count the inventory's, its tag-set counts summing to it, an untagged class's tag sets `[[]]`; the four tagged classes' tag sets as listed in §1.2; the overall digest equal to SHA-256 of `canonical_json({"fingerprint_format": NEUTRAL_FORMAT, "classes": {name: {"count", "digest"}}})`, recomputed. `taken` given (`{"when", "by", "dirty"}`) is equal and not the same object, the caller's is unchanged, the fingerprint is otherwise the baseline's, and the comparison is `[]` both ways |
| 5 | `TestListing` | `test_the_listing_hashes_to_the_fingerprint` | The baseline's listing, joined and parsed by word position (`parse_listing`, as the source's): the first line's words are exactly `#`, `fingerprint_format`, `1`, `digest`, the digest, `encoding_format`, `1`, and words 2, 4 and 6 read back as the format, digest and encoding format; the classes in order; each class header's count and digest are the fingerprint's, its record lines number its count, and sorted they hash to its digest; each tag-set header's count and digest are the fingerprint's, and its lines hash to its digest |
| 6 | `TestVersions` | `test_the_versions`, `test_another_encoding_of_the_same_store` | On fingerprints built as the source's `TestFormats` builds them, plus `encoding_format`: formats 1 and 2, exactly one entry, kind `format`, class and tags `None`, `(1, 2)`, its text containing "Recompute both" and equal to the source's text written as a literal (`FORMAT_TEXT_1_2`); encodings 1 and 2, one `encoding` entry, `(1, 2)`; both, `format` then `encoding`; a recorded fingerprint with no `encoding_format`, one `encoding` entry `(None, ENCODING_FORMAT)`; equal versions, `[]`. The baseline against itself re-stamped `encoding_format` 2 (every digest equal): only the `encoding` entry |
| 7 | `TestTheFormatArgument` | `test_positional_or_keyword`, `test_refusals`, `test_another_format_moves_only_the_overall_digest` | `fingerprint_of(inventory, 1) == fingerprint_of(inventory, fingerprint_format=1)`, and equal to the baseline. Missing: `assertRaisesRegex(TypeError, "fingerprint_format")`. `True`, `"1"`, `1.0`, `{"when": "now"}` (sub-tests): `assertRaisesRegex(TypeError, r"^fingerprint_of\(\): fingerprint_format must be an int")`, and the value's `repr` in the message. `0`, `-1`: the same for `ValueError`, `…must be at least 1`. And `fingerprint_of(object(), "1")` raises the function's own `TypeError`: refused before the inventory is read. At format 2, every class entry and tag-set entry equals the baseline's, `fingerprint_format` is 2, and the overall digest differs |
| 8 | `TestPurity` | `test_arguments_and_store_unchanged`, `test_importing_the_module_loads_no_ray` | On a store of its own: `file_state` taken after `read_inventory`; deep copies of the inventory and `taken`; `fingerprint_of` leaves both equal to their copies; `compare_fingerprints` of the fingerprint and an altered deep copy (a class digest, a tag-set digest, a class removed, the overall digest and `problems` changed, so every branch runs) leaves both equal to copies; `listing_lines`, consumed, leaves the inventory and the fingerprint equal; `file_state` is unchanged. In a fresh interpreter (as `test_package_imports` runs one), `import datastorekit.store_fingerprint` leaves `"ray"` out of `sys.modules` |

**Test 2's cases and their expected sets.** Derived from the full store's rows
(`real_store_fixtures._full_shard0`, `_full_shard1`, `FULL_REPLICATED_ROWS`), stated in the test's
class docstring and literals, and checked against correction 2's measured table:

- *the run tag* is `fixture-run` (tag 1); `grid-A` 2, `grid-B` 4, `weave-tag` 5. Samples 1, 2 are
  on shard 0, Sample 4 on shard 1; Sample 1 carries `(fixture-run, grid-A)`, Samples 2 and 4
  `(fixture-run,)`, so `Sample (fixture-run,)` counts 2. No class references a Sample.
- Traces 1 (shard 0) and 2 (shard 1) carry `(fixture-run, grid-A)`, Trace 3 `(fixture-run,
  grid-B)` alone, Trace 4 `(fixture-run,)` alone. Weave 1 names Trace 4 (`trace`) and Trace 3
  (strand 702's origin), and `reference_digest` covers a tagged parent's tags
  (`store_inventory.py:162-170`) but not its `validated` or `value_count`.

| Test | Change (shard 0 `extra_sql`) | Expected changed entries | Comparison |
|---|---|---|---|
| `test_deleting_one_sharded_record` | `Sample` 2 deleted with its `Sample_tags` and `Sample_members` rows | `(Sample, None)`, `(Sample, (fixture-run,))` | one `tag_set`, `(2, 1)`; Sample's count 3 → 2 |
| `test_deleting_the_row_alone_is_also_a_problem_entry` | `Sample` 2's row alone | the same two | `tag_set` `(2, 1)`, then `problems` `orphan-member` and `orphan-tag` (0 → 1 each); `problems` exactly `{"Sample": {"orphan-member": 1, "orphan-tag": 1}}` |
| `test_adding_a_tag_to_one_record` | tag 5 (`weave-tag`) added to `Sample` 2 | `(Sample, None)`, `(Sample, (fixture-run,))`, `(Sample, (fixture-run, weave-tag))` | two `tag_set`, `(2, 1)` and `(None, 1)` |
| `test_adding_a_tag_to_a_referenced_record_reaches_its_child` | tag 2 (`grid-A`) added to `Trace` 4 | `(Trace, None)`, `(Trace, (fixture-run,))`, `(Trace, (fixture-run, grid-A))`, `(Weave, None)`, `(Weave, (fixture-run, weave-tag))` | three `tag_set`: Trace `(fixture-run,)` `(1, None)`, Trace `(fixture-run, grid-A)` `(2, 3)`, Weave `(1, 1)` |
| `test_deleting_one_value_row` | `TraceStep` 32 deleted (Trace 3's) | `(Trace, None)`, `(Trace, (fixture-run, grid-B))` | one `tag_set`, `(1, 1)`; Trace's count unchanged |
| `test_flipping_one_validated_flag` | `Trace` 3's `trace_validated` set to 1 | the same two | one `tag_set`, `(1, 1)` |
| `test_an_orphan_value_row_is_a_problem_entry_only` | a `TraceStep` (serial 9001, `trace_serial` 999) | none; the overall digest equal | one entry, `("problems", "Trace", None)`, `(0, 1)`; `problems` exactly `{"Trace": {"orphan-value": 1}}` |

Every expected set and comparison above is also what the source's code gives for the same store
(§4.3: these are among the equivalence check's changes, with Trace 3's tag and Sample 4's flag).

**Not a port.** The module is not in `docs/extraction/compare_ported_tests.py`'s `PORTED`; the port
check reports "20 module(s) … 1 test(s) declared not ported" at the start and the end (§4.2).

### 1.4 The contract (§2.5)

`docs/client-contract.md`, **19 lines added, none removed** (`git diff --numstat`: `19 0`; no line
of the diff begins with a single `-`):

- **the head line**, after §9.6's (`:40-41`) and before the intro paragraph, which is unchanged:
  "*§9.7 is measured from the package at `fingerprint` prompt 01's tree, and its line numbers are
  that tree's.*";
- **§9.7 `fingerprint` prompt 01**, after §9.6, at the end of the file: its preamble (one change,
  the README's U1–U3, the user's ruling; nothing the layer writes or reads, and no message, refusal
  or exception of the layer's, changes; what a client gives is its own `fingerprint_format`, which
  it keeps and bumps) and four rows, each "Supersedes: none":
  - **`fingerprint_of`**: the signature and its two refusals (with their texts), the keys, what
    each digest is over, the overall digest's object, what is outside every digest, purity and
    imports; **what a client supplies**; pinned by tests 1–4, 7, 8;
  - **`compare_fingerprints`**: the two versions (both texts), the comparison body, the six entry
    kinds, and that `taken` is never compared; pinned by tests 2, 4, 6;
  - **`listing_lines`**: its lines and its first line's seven words; pinned by test 5;
  - **`ENCODING_FORMAT` and when it is bumped**: U3's rule and its eight items in the module
    comment's order, each naming the function or field of `store_inventory.py` or
    `store_fingerprint.py` it means, with its lines at this tree; a bump adds a golden beside the
    old (`tests/data/`), and the release says so in `PROVENANCE.md` and an addendum to every
    client's checklist; pinned by test 4.

No marker is set on any row of §1–§9.6.

### 1.5 The records

- **This campaign's board**: the header (in progress; 01 landed, not yet reviewed), §1's row for 01
  (landed, this commit, the log), a note under §1, and §3's line dated. The decisions table is
  unchanged: no decision changed.
- **This campaign's README**: a sentence in its header, and §2's row for 01.
- **`prompts/INDEX.md`**: the header (1 in progress) and the campaign's line.
- **`docs/OPEN_ISSUES.md`**: unchanged, **4 open** (no issue opened or closed).
- **This log.**

---

## 2. Deviations from the prompt

1. **Correction 1: test 7 matches the refusal's message, and (j)'s prediction is corrected.** Test
   7 asserts each refusal with `assertRaisesRegex`: the missing argument against
   `"fingerprint_format"` (Python's own message names it), each type refusal against
   `^fingerprint_of\(\): fingerprint_format must be an int`, each value refusal against `…must be at
   least 1`, and the value's `repr` in each message. Under (j) the type check is gone and the `< 1`
   check kept: `True` and `1.0` are **hashed**, and `"1"` and the dict are refused by Python's
   comparison (`'<' not supported between instances of 'str' and 'int'`), whose message does not
   name the function (measured in `<scratch-fp01>/break-j`, §5). So (j) fails all four sub-tests,
   and the "refused before the inventory is read" check too; a bare `assertRaises(TypeError)` would
   have failed only two. §4.4 (j)'s "the dict, the string and the bool are hashed" is read as
   corrected. **STRUCTURALLY REQUIRED.**
2. **Correction 2: test 2's cascades.** The deleted record and the added tag are on `Sample` 2,
   which nothing references by tags and whose changes are local (measured); the value row and the
   validated flag are on `Trace` 3, since only `Gadget` and `Trace` declare `validated`
   (`tests/client/factories.py:911`, `:1472`) and `Sample`'s flag is not identity
   (`test_store_inventory.NON_IDENTITY`). A seventh case adds a tag to `Trace` 4 and **names
   Weave's entries** in its expected set, so the cascade through `reference_digest` is pinned
   rather than avoided. `assertLocalised` takes the expected set of (class, tags) entries, not one
   class, so that it can name two. **STRUCTURALLY REQUIRED.**
3. **Correction 3: 28 changed stores, not 27.** Deleting the last row of every table with rows: 11
   replicated tables, 10 on shard 0, 7 on shard 1, **28** stores, every comparison non-empty, **14**
   with `problems` entries, at formats 1 and 6, at both ends (§4.3). The equivalence check adds test
   2's nine changes (37 changed stores). The stop is on a difference, of which there were none.
   Recorded as found.
4. **Correction 4: the brief and the audit were read at SGK `a5a6f6d`**, by `git -C … show
   a5a6f6d:<path>`; SGK's code and fingerprint tests at `c8a7f14`. Recorded as found.
5. **Correction 5: (f) is equivalent.** `read_records` builds every record's tags as
   `tuple(sorted(…))` (`store_inventory.py:765-767`), so sorting again in `_tag_sets` changes
   nothing on any inventory `read_inventory` gives: under (f) the module gives `OK` (§5). Recorded as
   equivalent, not as a gap.
6. **Correction 6: line numbers.** Every line the prompt cites held, with the note's readings. The
   extract `sed -n 1164,1400p` is 237 lines, SHA-256
   `9b1a8aedb006ffa9c2635038eda2e87cad451106283d022a94f8038cd8eb0108`, the note's; it begins at
   `_sha256_lines` and ends with `listing_lines`' `yield from lines` and a blank line. The contract's
   §9.6 head line was `:40-41`, and §9.7 went at the end (after `:367`). Recorded as found.
7. **The orchestrator's additions**, each followed as given, each an **IMPLEMENTATION CHOICE** at
   the orchestrator's direction: the order of work (§4: the baseline; §2.1 and the guards with
   `test_package_imports` at the high end; the equivalence check at both ends before the golden;
   §2.2, §2.3 and the suite at both ends; the breakages, each in its own export; §2.5 and the
   records; the final checks); every scratch venv made `uv … --offline`, the export installed
   editable with `--no-deps --no-build-isolation`, no `PYTHONPATH`, every command run from the
   export's root under `env -u PYTHONPATH`, and `datastorekit.__file__` printed in each; the extract
   loaded with `importlib.util.spec_from_file_location` under the scratch name `scratch_extract`,
   both SHA-256s recorded; the listing's encoding field read from the fingerprint; the test
   module's prose naming the source generically; `_Stores` restated, not imported; the `ast`
   comparison (§1.1); the vocabulary check by a script (§4.5).
8. **More tests than the prototype's 15: 21.** Test 2 has seven cases (correction 2's first, second,
   third, fifth, sixth and last rows, and the Trace-tag cascade); test 3 two (timestamps; no
   timestamp in any line); test 6 two (the hand-built versions; the re-stamped store); test 7 three
   (positional and keyword; the refusals; another format). **IMPLEMENTATION CHOICE.**
9. **Test 7 checks more than §2.3 lists**: the value's `repr` in each refusal's message, and a
   refusal before the inventory is read (`fingerprint_of(object(), "1")`). Test 4 also checks the
   tagged classes' tag sets and the per-class keys; test 5 also the tag-set headers' counts and
   digests. **IMPLEMENTATION CHOICE.**
10. **The refusals' texts** are this prompt's choice within §2.1 item 4 ("fingerprint_of():
    fingerprint_format must be an int, not <type> <value>"; "… must be at least 1, not <value>"),
    in the form of the package's other refusals (`canonical()`'s). **IMPLEMENTATION CHOICE.**
11. **The bump-rule comment states U3 in full**, beyond §2.1 item 3's list: also the release's
    provenance record and checklist addenda, and that a change the golden does not see is still a
    bump. §2.1 item 3 asks for "README §6.2 U3 in full"; contract §9.7 says the same.
    **IMPLEMENTATION CHOICE.**
12. **The equivalence check also compares** `taken` given (`{"when", "who"}`), and the listing line
    by line, at both formats. The low end ran in `venv/` against this checkout's tree (the note
    allows either). **IMPLEMENTATION CHOICE.**
13. **A client moved, as the dispatch said it might.** ChamPBH was at `a95658b`
    (`read-only-plots`) with 29 entries at the start, as the dispatch gives, and another session
    committed there twice during this prompt (`2792a85` at the end, 23 entries); SGK and SI were
    as given at both ends (§4.7). Nothing of this prompt wrote, ran, imported or opened anything of
    a client. Recorded as found.
14. **The gate, as found.** `git diff --stat 2f5417e HEAD -- datastorekit pyproject.toml docs` was
    empty; the local `origin/main` ref is `5f972be`, an ancestor of `main`; the tags are `v0.1.0`
    to `v0.3.0`, six, and no other. No `git fetch` or `ls-remote` was run (offline). Recorded as
    found.

No UNINTENDED DRIFT was found.

---

## 3. The hazards (§3)

1. **The digest.** The `overall` object is the source's exactly (`ast`, §1.1); test 4 recomputes
   it, and the equivalence check compares it with the source's: equal at formats 1 and 6, the
   format 1 digest `7656b600…d304` and format 6 `bdf09575e8f8930677b4f040b4ba0d298dfc7277da9fb5205a31102d2d619b19`,
   both the planner's. Breakages (a) and (b) fail test 4, and (a) fails the equivalence check.
2. **The guards.** `test_layer_is_generic`, `test_prose_names_no_source` and `test_package_imports`
   pass on the module and the test module, in every suite run and on their own (§4.2).
3. **The source's text.** The `format` entry is the source's call verbatim (`ast`); test 6 holds
   the text as a literal, and (d) fails it.
4. **The listing's word positions.** Test 5 reads words 2, 4 and 6; (e) fails it; the equivalence
   check finds the first line the source's plus ` encoding_format 1`.
5. **`store_inventory.py` is not changed**, nor any other existing file under `datastorekit/`
   (`git status`: three new files there).
6. **The port check** passes unchanged (§4.2).
7. **Additive documents.** `git diff docs/client-contract.md`: `+` lines only. Nothing else under
   `docs/` changed.
8. **No Ray.** No test or script of this prompt starts Ray: the module's `tearDownModule` passes;
   `names.py` printed `ray.is_initialized()` `False` after importing everything; no Ray process
   was up at the start or the end (§4.6).
9. **Offline only.** Every venv and install was `uv … --offline`; every pin resolved.
10. **The clients** were read only through `git -C <client> rev-parse`, `status --short` and `show`
    (§4.7). The source's extract was run in scratch, as U5 allows; nothing of a client was
    imported as a module of the client, installed, committed or opened.

---

## 4. Verification performed

### 4.1 The suite

Each run in the foreground, from its tree's root, its output to a scratch file, the verdict taken
with `grep -E '^Ran |^OK|^FAILED'` and the warnings with `grep -c ResourceWarning`
(`<scratch-fp01>/probe/suite.sh`). High-end venvs: Python 3.13.16, Ray 2.55.1, SQLAlchemy 2.0.46,
`setuptools`, the export installed with `uv pip install --offline --no-deps --no-build-isolation
-e`, `datastorekit.__file__` printed under the export's `tree/` in each
(`<scratch-fp01>/probe/mkenv.sh`). `venv/` is Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39,
`black` 25.1.0, `datastorekit 0.3.0` editable from this checkout, not reinstalled. SQLite 3.53.4
everywhere.

| When | Where | Result | `ResourceWarning` lines |
|---|---|---|---|
| start (01:36) | `venv/` | `Ran 509 tests in 84.279s` / `OK` | 0 |
| start (01:38) | `<scratch-fp01>/base-hi`: `git archive HEAD` (`df3fec9`) | `Ran 509 tests in 97.660s` / `OK` | 0 |
| after §2.1 (01:41) | `<scratch-fp01>/stage2-hi`: the guards and `test_package_imports` alone | `Ran 16 tests` / `OK` | 0 |
| after §2.3 (01:45) | `venv/` | `Ran 530 tests in 92.078s` / `OK` | 0 |
| after §2.3 (01:46) | `<scratch-fp01>/stage3-hi`: an export of the working tree | `Ran 530 tests in 92.765s` / `OK` | 4 |
| end (01:56) | `venv/` | `Ran 530 tests in 84.726s` / `OK` | 0 |
| end (01:58) | `<scratch-fp01>/final-hi`: an export of the final working tree, this log included | `Ran 530 tests in 93.753s` / `OK` | 4 |

The 4 `ResourceWarning` lines at the high end ("unclosed database", from SQLAlchemy's frames) were
printed, in both runs, after test 519 of 530 in run order, in `test_version_row_at_open`, not in
the new module (whose 21 tests come earlier, and gave 0 in every breakage run):
`actor-names` log 01 correction 8 treats 0 or 4 at the high end as timing, and the prototype gave
4 there too.

### 4.2 The checks

- **The port check**, `venv/bin/python docs/extraction/compare_ported_tests.py`: exit 0, "OK: 20
  module(s) keep their source's tests, classes and assertion skeletons; 1 test(s) declared not
  ported", at the start and the end.
- **`black --check datastorekit docs`** (25.1.0): 76 files at the start; **78** at the end, the
  module and its test module the two more. Both were formatted with `black` before the runs above.
- **The guards**, `test_layer_is_generic`, `test_prose_names_no_source` and `test_package_imports`,
  run on their own after §2.1 at the high end (16 tests, `OK`), and at the end in `venv/`
  with `test_store_fingerprint` and `test_store_inventory`: `Ran 79 tests … OK`.
- **Scope** (E1): `git status --short` shows, under `datastorekit/`, exactly three new files (the
  module, its test module, the golden) and no other change; outside it, `docs/client-contract.md`,
  this log, the board, the README and `prompts/INDEX.md`. Every changed file is in §7's list.
- **The breakages as recorded** (§5): the ten diff blocks, extracted from this log, each passed
  `git apply --check`, `git apply`, and `git apply -R --check` on a fresh copy of the final
  working tree's export (`<scratch-fp01>/recheck/tree-<x>`, each a copy of
  `<scratch-fp01>/final-hi/tree`). Each block is byte-equal to the diff applied in §5, and the
  file it gives is equal (`cmp`) to that breakage's file. The module did not change after the
  breakage runs, so the tests were not run again under them.

### 4.3 The equivalence check (§2.4)

**The extract.** `git -C /Users/ds283/Documents/Code/SecondaryGWKit show
c8a7f14:RunRegistry/stores.py | sed -n 1164,1400p > <scratch-fp01>/extract/sgk_section.py`: 237
lines, SHA-256 `9b1a8aedb006ffa9c2635038eda2e87cad451106283d022a94f8038cd8eb0108`. With three
lines prepended (`import hashlib`, `from collections import Counter`, `FINGERPRINT_FORMAT = None  #
set by the equivalence script before each call`) it is `<scratch-fp01>/extract/sgk_fingerprint.py`,
240 lines, SHA-256 `006459acf94e023e2b64b1a7813e222628752f7bb6464c3d043afce0a767aa4f`; `diff` of its
lines 4– with the extract is empty. It imports `canonical_json` from the package inside its
functions, as the source's does. It is loaded by path under the scratch module name
`scratch_extract`; nothing of the source is imported as a module of the source, installed or
committed, and no store, test or working-tree file of the source was opened.

**The script**, `<scratch-fp01>/extract/equivalence.py` (SHA-256
`4ef9393fea1b3c06cc2c2aa1b3d5699ae8e38890955800ea93b53c0a61f39a2c`), run as `python -I
equivalence.py`:

```python
"""The equivalence check of fingerprint prompt 01, section 2.4 (U5).

The source's five fingerprint functions, extracted verbatim into ``sgk_fingerprint.py`` beside this
script (three lines prepended), are loaded by path under a scratch module name and run beside the
package's ``datastorekit.store_fingerprint`` on the neutral full store and on changed stores, at
client formats 1 and 6. Every store is built in a temporary directory.

usage: python -I equivalence.py
"""

import copy
import hashlib
import importlib.util
import sys
import tempfile
from pathlib import Path

import datastorekit
from datastorekit import store_fingerprint as pkg
from datastorekit.store_inventory import read_inventory
from datastorekit.tests.client.registry import factories
from datastorekit.tests.real_store_fixtures import build_full_store, full_rows

HERE = Path(__file__).resolve().parent
EXTRACT = HERE / "sgk_fingerprint.py"

spec = importlib.util.spec_from_file_location("scratch_extract", EXTRACT)
sgk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sgk)

FORMATS = (1, 6)

differences = []


def check(label, ok, detail=""):
    if not ok:
        differences.append(f"{label}: {detail}")
    return ok


def sgk_fingerprint(inventory, fmt, taken=None):
    sgk.FINGERPRINT_FORMAT = fmt
    try:
        return sgk.fingerprint_of(inventory, taken)
    finally:
        sgk.FINGERPRINT_FORMAT = None


def without_encoding(fp):
    out = dict(fp)
    out.pop("encoding_format")
    return out


def changes():
    """(label, build_full_store keyword arguments), the baseline first."""
    out = [("baseline", {})]
    # the last row of every table that has rows, among the replicated rows and on each shard
    replicated, sharded, keys = full_rows()
    for table in replicated:
        if replicated[table]:
            r = copy.deepcopy(replicated)
            r[table] = r[table][:-1]
            out.append(
                (
                    f"replicated {table}: last row deleted",
                    dict(replicated=r, sharded=copy.deepcopy(sharded), shard_keys=keys),
                )
            )
    for shard in sorted(sharded):
        for table in sharded[shard]:
            if sharded[shard][table]:
                s = copy.deepcopy(sharded)
                s[shard][table] = s[shard][table][:-1]
                out.append(
                    (
                        f"shard {shard} {table}: last row deleted",
                        dict(
                            replicated=copy.deepcopy(replicated),
                            sharded=s,
                            shard_keys=keys,
                        ),
                    )
                )
    # the changes of section 2.3 test 2 (orchestrator's correction 2's table)
    sql = {
        "Sample 2 deleted with its tag and member rows": {
            0: [
                "DELETE FROM Sample WHERE serial = 2",
                "DELETE FROM Sample_tags WHERE sample_serial = 2",
                "DELETE FROM Sample_members WHERE sample_serial = 2",
            ]
        },
        "Sample 2's row alone deleted": {0: ["DELETE FROM Sample WHERE serial = 2"]},
        "tag 5 added to Sample 2": {
            0: ["INSERT INTO Sample_tags (sample_serial, tag_serial) VALUES (2, 5)"]
        },
        "tag 2 added to Trace 3": {
            0: ["INSERT INTO Trace_tags (trace_serial, tag_serial) VALUES (3, 2)"]
        },
        "tag 2 added to Trace 4": {
            0: ["INSERT INTO Trace_tags (trace_serial, tag_serial) VALUES (4, 2)"]
        },
        "TraceStep 32 deleted": {0: ["DELETE FROM TraceStep WHERE serial = 32"]},
        "Trace 3 validated": {
            0: ["UPDATE Trace SET trace_validated = 1 WHERE serial = 3"]
        },
        "Sample 4 validated (shard 1)": {
            1: ["UPDATE Sample SET sample_validated = 1 WHERE serial = 4"]
        },
        "an orphan TraceStep": {
            0: [
                "INSERT INTO TraceStep (serial, trace_serial, step_index, step_value) "
                "VALUES (9001, 999, 1, 0.0)"
            ]
        },
    }
    for label, statements in sql.items():
        out.append((label, dict(extra_sql=statements)))
    return out


def main():
    print("datastorekit:", datastorekit.__file__)
    print("python:", sys.version.split()[0])
    print(
        "extract:",
        EXTRACT.name,
        hashlib.sha256(EXTRACT.read_bytes()).hexdigest(),
    )
    print("package ENCODING_FORMAT:", pkg.ENCODING_FORMAT)

    with tempfile.TemporaryDirectory() as tmp:
        stores = []
        for n, (label, kwargs) in enumerate(changes()):
            directory = Path(tmp) / f"store-{n}"
            directory.mkdir()
            inventory = read_inventory(
                build_full_store(directory, **kwargs).primary, factories
            )
            stores.append((label, inventory))
        print(f"stores: 1 baseline + {len(stores) - 1} changed")

        for fmt in FORMATS:
            base_label, base_inventory = stores[0]
            base_pkg = pkg.fingerprint_of(base_inventory, fmt)
            base_sgk = sgk_fingerprint(base_inventory, fmt)
            print(f"\nformat {fmt}: baseline digest {base_pkg['digest']}")
            check(
                f"format {fmt} baseline: keys",
                set(base_pkg) == set(base_sgk) | {"encoding_format"},
                f"{sorted(base_pkg)} vs {sorted(base_sgk)}",
            )
            check(
                f"format {fmt} baseline: encoding_format",
                base_pkg["encoding_format"] == pkg.ENCODING_FORMAT,
            )
            check(
                f"format {fmt} baseline: fingerprint",
                without_encoding(base_pkg) == base_sgk,
            )
            # taken given
            taken = {"when": "now", "who": "scratch"}
            check(
                f"format {fmt} baseline with taken",
                without_encoding(pkg.fingerprint_of(base_inventory, fmt, taken))
                == sgk_fingerprint(base_inventory, fmt, taken),
            )
            # the listing: every line but the first equal; the first SGK's plus the field
            lines_pkg = list(pkg.listing_lines(base_inventory, base_pkg))
            lines_sgk = list(sgk.listing_lines(base_inventory, base_sgk))
            check(
                f"format {fmt} listing: line count",
                len(lines_pkg) == len(lines_sgk),
                f"{len(lines_pkg)} vs {len(lines_sgk)}",
            )
            check(f"format {fmt} listing: lines 2-", lines_pkg[1:] == lines_sgk[1:])
            check(
                f"format {fmt} listing: first line",
                lines_pkg[0]
                == lines_sgk[0] + f" encoding_format {pkg.ENCODING_FORMAT}",
                f"{lines_pkg[0]!r} vs {lines_sgk[0]!r}",
            )
            print(f"  listing: {len(lines_pkg)} lines; first: {lines_pkg[0]}")

            rows_deleted = nonempty = with_problems = 0
            for label, inventory in stores[1:]:
                fp_pkg = pkg.fingerprint_of(inventory, fmt)
                fp_sgk = sgk_fingerprint(inventory, fmt)
                same_fp = check(
                    f"format {fmt} {label}: fingerprint",
                    without_encoding(fp_pkg) == fp_sgk,
                )
                cmp_pkg = pkg.compare_fingerprints(base_pkg, fp_pkg)
                cmp_sgk = sgk.compare_fingerprints(base_sgk, fp_sgk)
                same_cmp = check(
                    f"format {fmt} {label}: comparison",
                    cmp_pkg == cmp_sgk,
                    f"{cmp_pkg} vs {cmp_sgk}",
                )
                if "last row deleted" in label:
                    rows_deleted += 1
                    if cmp_pkg:
                        nonempty += 1
                    if any(e["kind"] == "problems" for e in cmp_pkg):
                        with_problems += 1
                kinds = sorted({e["kind"] for e in cmp_pkg})
                print(
                    f"  {label}: fingerprint {'equal' if same_fp else 'DIFFERS'}, "
                    f"comparison {'equal' if same_cmp else 'DIFFERS'} "
                    f"({len(cmp_pkg)} entries: {', '.join(kinds) or 'none'})"
                )
            print(
                f"  changed stores: {len(stores) - 1}, of them {rows_deleted} with a last row "
                f"deleted: {nonempty} with a non-empty comparison, {with_problems} with "
                f"problems entries"
            )

    print(f"\ndifferences: {len(differences)}")
    for d in differences:
        print("  " + d)
    return 1 if differences else 0


if __name__ == "__main__":
    sys.exit(main())
```

**The runs.**

| Run | Where | Exit | Differences |
|---|---|---|---|
| high end, after §2.1 (01:42) | `<scratch-fp01>/stage2-hi`, the export's root | 0 | 0 |
| low end, after §2.1 (01:43) | `venv/`, from `<scratch-fp01>/extract`, this checkout's tree | 0 | 0 |
| high end, end (02:00) | `<scratch-fp01>/final-hi`, the final tree | 0 | 0 |
| low end, end (02:00) | `venv/`, from `<scratch-fp01>/extract`, this checkout's final tree | 0 | 0 |

At both ends, every run: the baseline digest at format 1 `7656b600…d304` and at format 6
`bdf09575…9b19`, the planner's; the listing 68 lines; 37 changed stores, every fingerprint and
comparison equal; of the 28 last-row deletions, 28 non-empty comparisons and 14 with `problems`
entries. The low end's output equals the high end's line for line but for the package's path and
Python's version. Under breakage (a) the script exits 1 with **80** differences (§5).

**The output**, high end (after §2.1):

```
datastorekit: <scratch-fp01>/stage2-hi/tree/datastorekit/__init__.py
python: 3.13.16
extract: sgk_fingerprint.py 006459acf94e023e2b64b1a7813e222628752f7bb6464c3d043afce0a767aa4f
package ENCODING_FORMAT: 1
stores: 1 baseline + 37 changed

format 1: baseline digest 7656b600965b5911a5046e7c0ebcd4dddce1c8ad277243d211b548487f22d304
  listing: 68 lines; first: # fingerprint_format 1 digest 7656b600965b5911a5046e7c0ebcd4dddce1c8ad277243d211b548487f22d304 encoding_format 1
  replicated version: last row deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  replicated store_tag: last row deleted: fingerprint equal, comparison equal (4 entries: problems, tag_set)
  replicated keypoint: last row deleted: fingerprint equal, comparison equal (7 entries: problems, tag_set)
  replicated routing_rule: last row deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  replicated dial_setting: last row deleted: fingerprint equal, comparison equal (5 entries: problems, tag_set)
  replicated gauge_setting: last row deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  replicated keypoint_alias: last row deleted: fingerprint equal, comparison equal (3 entries: problems, tag_set)
  replicated Gadget: last row deleted: fingerprint equal, comparison equal (5 entries: problems, tag_set)
  replicated Gadget_tags: last row deleted: fingerprint equal, comparison equal (3 entries: tag_set)
  replicated GadgetPart: last row deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  replicated knob_setting: last row deleted: fingerprint equal, comparison equal (9 entries: problems, tag_set)
  shard 0 Trace: last row deleted: fingerprint equal, comparison equal (5 entries: problems, tag_set)
  shard 0 Trace_tags: last row deleted: fingerprint equal, comparison equal (3 entries: tag_set)
  shard 0 TraceStep: last row deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  shard 0 Tessera: last row deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  shard 0 Sample: last row deleted: fingerprint equal, comparison equal (3 entries: problems, tag_set)
  shard 0 Sample_members: last row deleted: fingerprint equal, comparison equal (2 entries: problems, tag_set)
  shard 0 Sample_tags: last row deleted: fingerprint equal, comparison equal (2 entries: tag_set)
  shard 0 Weave: last row deleted: fingerprint equal, comparison equal (3 entries: problems, tag_set)
  shard 0 Weave_members: last row deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  shard 0 Weave_tags: last row deleted: fingerprint equal, comparison equal (2 entries: tag_set)
  shard 1 Trace: last row deleted: fingerprint equal, comparison equal (3 entries: problems, tag_set)
  shard 1 Trace_tags: last row deleted: fingerprint equal, comparison equal (2 entries: tag_set)
  shard 1 TraceStep: last row deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  shard 1 Tessera: last row deleted: fingerprint equal, comparison equal (3 entries: problems, tag_set)
  shard 1 Sample: last row deleted: fingerprint equal, comparison equal (3 entries: problems, tag_set)
  shard 1 Sample_members: last row deleted: fingerprint equal, comparison equal (2 entries: problems, tag_set)
  shard 1 Sample_tags: last row deleted: fingerprint equal, comparison equal (2 entries: tag_set)
  Sample 2 deleted with its tag and member rows: fingerprint equal, comparison equal (1 entries: tag_set)
  Sample 2's row alone deleted: fingerprint equal, comparison equal (3 entries: problems, tag_set)
  tag 5 added to Sample 2: fingerprint equal, comparison equal (2 entries: tag_set)
  tag 2 added to Trace 3: fingerprint equal, comparison equal (3 entries: tag_set)
  tag 2 added to Trace 4: fingerprint equal, comparison equal (3 entries: tag_set)
  TraceStep 32 deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  Trace 3 validated: fingerprint equal, comparison equal (1 entries: tag_set)
  Sample 4 validated (shard 1): fingerprint equal, comparison equal (0 entries: none)
  an orphan TraceStep: fingerprint equal, comparison equal (1 entries: problems)
  changed stores: 37, of them 28 with a last row deleted: 28 with a non-empty comparison, 14 with problems entries

format 6: baseline digest bdf09575e8f8930677b4f040b4ba0d298dfc7277da9fb5205a31102d2d619b19
  listing: 68 lines; first: # fingerprint_format 6 digest bdf09575e8f8930677b4f040b4ba0d298dfc7277da9fb5205a31102d2d619b19 encoding_format 1
  replicated version: last row deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  replicated store_tag: last row deleted: fingerprint equal, comparison equal (4 entries: problems, tag_set)
  replicated keypoint: last row deleted: fingerprint equal, comparison equal (7 entries: problems, tag_set)
  replicated routing_rule: last row deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  replicated dial_setting: last row deleted: fingerprint equal, comparison equal (5 entries: problems, tag_set)
  replicated gauge_setting: last row deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  replicated keypoint_alias: last row deleted: fingerprint equal, comparison equal (3 entries: problems, tag_set)
  replicated Gadget: last row deleted: fingerprint equal, comparison equal (5 entries: problems, tag_set)
  replicated Gadget_tags: last row deleted: fingerprint equal, comparison equal (3 entries: tag_set)
  replicated GadgetPart: last row deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  replicated knob_setting: last row deleted: fingerprint equal, comparison equal (9 entries: problems, tag_set)
  shard 0 Trace: last row deleted: fingerprint equal, comparison equal (5 entries: problems, tag_set)
  shard 0 Trace_tags: last row deleted: fingerprint equal, comparison equal (3 entries: tag_set)
  shard 0 TraceStep: last row deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  shard 0 Tessera: last row deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  shard 0 Sample: last row deleted: fingerprint equal, comparison equal (3 entries: problems, tag_set)
  shard 0 Sample_members: last row deleted: fingerprint equal, comparison equal (2 entries: problems, tag_set)
  shard 0 Sample_tags: last row deleted: fingerprint equal, comparison equal (2 entries: tag_set)
  shard 0 Weave: last row deleted: fingerprint equal, comparison equal (3 entries: problems, tag_set)
  shard 0 Weave_members: last row deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  shard 0 Weave_tags: last row deleted: fingerprint equal, comparison equal (2 entries: tag_set)
  shard 1 Trace: last row deleted: fingerprint equal, comparison equal (3 entries: problems, tag_set)
  shard 1 Trace_tags: last row deleted: fingerprint equal, comparison equal (2 entries: tag_set)
  shard 1 TraceStep: last row deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  shard 1 Tessera: last row deleted: fingerprint equal, comparison equal (3 entries: problems, tag_set)
  shard 1 Sample: last row deleted: fingerprint equal, comparison equal (3 entries: problems, tag_set)
  shard 1 Sample_members: last row deleted: fingerprint equal, comparison equal (2 entries: problems, tag_set)
  shard 1 Sample_tags: last row deleted: fingerprint equal, comparison equal (2 entries: tag_set)
  Sample 2 deleted with its tag and member rows: fingerprint equal, comparison equal (1 entries: tag_set)
  Sample 2's row alone deleted: fingerprint equal, comparison equal (3 entries: problems, tag_set)
  tag 5 added to Sample 2: fingerprint equal, comparison equal (2 entries: tag_set)
  tag 2 added to Trace 3: fingerprint equal, comparison equal (3 entries: tag_set)
  tag 2 added to Trace 4: fingerprint equal, comparison equal (3 entries: tag_set)
  TraceStep 32 deleted: fingerprint equal, comparison equal (1 entries: tag_set)
  Trace 3 validated: fingerprint equal, comparison equal (1 entries: tag_set)
  Sample 4 validated (shard 1): fingerprint equal, comparison equal (0 entries: none)
  an orphan TraceStep: fingerprint equal, comparison equal (1 entries: problems)
  changed stores: 37, of them 28 with a last row deleted: 28 with a non-empty comparison, 14 with problems entries

differences: 0
```

### 4.4 The breakages

§5.

### 4.5 The documents and the names

- **Names**, imported in `venv/` from `<scratch-fp01>/probe` with `python -I`
  (`<scratch-fp01>/probe/names.py`; `datastorekit.__file__` is the checkout's), with their spans by
  `inspect.getsourcelines`:

  ```
  datastorekit: /Users/ds283/Documents/Code/DatastoreKit/datastorekit/__init__.py
  store_fingerprint.fingerprint_of: :86-154
  store_fingerprint.compare_fingerprints: :178-319
  store_fingerprint.listing_lines: :322-351
  store_fingerprint._sha256_lines: :68-74
  store_fingerprint._tag_sets: :77-83
  store_inventory.canonical: :120-134
  store_inventory.canonical_json: :150-154
  store_inventory.digest: :157-159
  store_inventory.reference_digest: :162-170
  store_inventory.read_records: :508-803
  store_inventory._merge_digests: :811-823
  store_inventory._combine: :826-913
  store_inventory._problem: :499-500
  store_inventory.read_inventory: :979-1045
  store_inventory.Record.as_json: :187-193
  store_inventory.Record.canonical_json: :195-196
  ENCODING_FORMAT: 1
  signature: (inventory, fingerprint_format: int, taken: Optional[Mapping[str, Any]] = None) -> dict
  Record fields: ['key', 'tags', 'validated', 'value_count']
  golden: datastorekit/tests/data/store_fingerprint-neutral-1-encoding-1.json True
  test classes: ['TestGolden', 'TestListing', 'TestLocalised', 'TestNotContent', 'TestPhysical', 'TestPurity', 'TestTheFormatArgument', 'TestVersions']
  ray initialised: False
  ```

  `_reference` is nested in `read_records` and was read at `store_inventory.py:695`. Every
  function, field and line §9.7 cites is above, or was read at this tree: `store_inventory.py:60-70`
  (the problem names), `:746-754` (the parent-set digest), `:756-761`, `:763-774`, `:765-767`,
  `:836`, `:893`; `store_fingerprint.py:32-36`, `:38-64`, `:65`, `:109-113`, `:114-118`,
  `:127-134`, `:136-138`, `:140-146`, `:147-154`, `:151`, `:153`, `:194-227`, `:229-319`,
  `:336-340`, `:343`, `:347-350`, `:351`. `tests/client/factories.py:911` and `:1472` (§2 item 2)
  are `validated="gadget_validated"` and `validated="trace_validated"`.
- **Relative links** added, each resolved from its file: `../prompts/fingerprint/README.md` (the
  contract); `logs/01-the-fingerprint-moves-into-the-package.md` (the board and the README);
  `../01-the-fingerprint-moves-into-the-package.md` (this log). `PROVENANCE.md` exists.
- **Anchors**: §9.7's heading gives `#97-fingerprint-prompt-01`, unique in the contract. No link to
  an anchor was added.
- **Neutral names** (`<scratch-fp01>/probe/vocab_check.py`, which loads
  `datastorekit/tests/data/client_vocabulary.json` and walks every string under each client's
  `registry` keys, `columns` names, `packages` and `extra_names`: 429 strings, 428 case-folded).
  Every identifier (`ast` names, attributes, definitions, arguments, aliases) and every word of
  every string constant (docstrings included) of the two new modules, checked exactly, case-folded
  and by each `_`/`-`-separated part: 579 names, **20 hits**, none a client's table or identifier
  column. In the module (310 names, 10 hits): `name`, `value`, `type`, `version`, `validated` and
  the parts of `__name__` and `value_count` (plain words, or the layer's own `LAYER_WORDS` and
  `Record` field), and `b`, `n`, `t` (the source's one-letter locals, kept by U1). In the test
  module, besides those: `label`, `source` (in prose: "the source repository"), `c`, `tag_serial`
  (the layer's own `contract.TAG_SERIAL`, in the test's SQL), `orphan-value` (the layer's problem
  name), and the parts `value` / `validated` of `step_value`, `trace_validated` and two test names
  (the neutral client's columns). The names this prompt chose (`store_fingerprint`,
  `fingerprint_of`, `compare_fingerprints`, `listing_lines`, `ENCODING_FORMAT`, `encoding_format`,
  `fingerprint_format`, `NEUTRAL_FORMAT`, `GOLDEN`, `FORMAT_TEXT_1_2`, `RUN`, `versions`, the test
  classes) have no hit. The layer guard, which forbids tables and identifier columns, passes.

### 4.6 Ray's processes

`pgrep -fl 'gcs_server|raylet|ray::|default_worker\.py'` found none at 01:36 (the start) and at
02:00 (the end); `RAY_ADDRESS` was unset throughout. No command of this prompt starts Ray.

### 4.7 The clients

Read only with `git -C <client> rev-parse --short HEAD`, `rev-parse --abbrev-ref HEAD` and `status
--short` (each listing saved, and compared with `diff` at the end), and `show` of SGK's code, tests,
brief and audit (correction 4).

| Client | Start (01:36) | End (02:00) |
|---|---|---|
| SecondaryGWKit | `a5a6f6d`, `handover-remedial`; 0 entries | `a5a6f6d`, `handover-remedial`; 0 entries (unchanged) |
| ChamPBH | `a95658b`, `read-only-plots`; 29 entries (as the dispatch gives; another session works there) | **`2792a85`**, `read-only-plots`; 23 entries: the 29 less six tracked files (`.documents/OPEN_ISSUES.md`, `.documents/architecture-summary.md`, `.documents/review-remediation-verification.md`, `CLAUDE.md`, `prompts/INDEX.md`, `prompts/read-only-plots/IMPLEMENTATION_STATE.md`), now committed. Another session committed there during this prompt: `1905065` (01:36:40, "Close the read-only-plots campaign with a handover") and `2792a85` (01:43:09, "Record the review of read-only-plots prompt 04"). Read only through `git` (`rev-parse`, `status --short`, `log --oneline` of the two) |
| StochasticInstantons | `5fb4a1d`, `dk-and-rpk-migration`; 0 entries | `5fb4a1d`, `dk-and-rpk-migration`; 0 entries (unchanged) |

---

## 5. The deliberate-breakage record (§4.4)

Each diff is relative to the repository root, exactly as applied, to its own fresh export of the
working tree (`<scratch-fp01>/break-<x>/tree`) with its own fresh offline venv at the high end,
installed editable (`<scratch-fp01>/probe/breakrun.sh`, the replacements in
`<scratch-fp01>/probe/breaks.py`). Each diff was made from the change, then passed `git apply -R
--check` on the broken tree; the file was restored, and the diff passed `git apply --check`, was
applied with `git apply`, and the result compared equal (`cmp`) to the breakage. The new module's
21 tests were then run. "Entries" are `unittest`'s failures plus errors, a sub-test counting on its
own. 0 `ResourceWarning` lines under every one. None was committed. They were re-checked from this
log at the end (§4.2).

### (a) `"encoding_format"` added to the `overall` object

```diff
diff --git a/datastorekit/store_fingerprint.py b/datastorekit/store_fingerprint.py
--- a/datastorekit/store_fingerprint.py
+++ b/datastorekit/store_fingerprint.py
@@ -139,6 +139,7 @@
 
     overall = {
         "fingerprint_format": fingerprint_format,
+        "encoding_format": ENCODING_FORMAT,
         "classes": {
             name: {"count": entry["count"], "digest": entry["digest"]}
             for name, entry in classes.items()
```

`Ran 21 tests … FAILED (failures=2)`: test 4, `test_the_golden_fingerprint` (the baseline against the golden: the digests differ) and `test_the_shape_and_the_overall_digest` (`'baaa547d…b648' != '7656b600…d304'`, the fingerprint's digest against the one recomputed over the source's object). **§2.4 fails**: the equivalence script, run in this export at the high end, exits 1 with **80** differences: at each format, the baseline's fingerprint, the fingerprint with `taken`, the listing's first line, and the 37 changed stores' fingerprints (every comparison stays equal, since only the overall digest moves on both sides). Its digests: format 1 `baaa547ddf0a8c0bc9c388cf284a4b84bc3040d7f70e0e2b0f34cbb3cc7eb648`, format 6 `adb1d053a055cda229e73b8450d4c7937071ec56f0f31c8f4d49114b24a5a55f`.

### (b) the overall object's key `"fingerprint_format"` renamed `"format"`

```diff
diff --git a/datastorekit/store_fingerprint.py b/datastorekit/store_fingerprint.py
--- a/datastorekit/store_fingerprint.py
+++ b/datastorekit/store_fingerprint.py
@@ -138,7 +138,7 @@
             problems[name] = dict(sorted(kinds.items()))
 
     overall = {
-        "fingerprint_format": fingerprint_format,
+        "format": fingerprint_format,
         "classes": {
             name: {"count": entry["count"], "digest": entry["digest"]}
             for name, entry in classes.items()
```

`FAILED (failures=2)`: test 4, `test_the_golden_fingerprint` and `test_the_shape_and_the_overall_digest` (`'4e369282…c604' != '7656b600…d304'`).

### (c) `compare_fingerprints` checking `fingerprint_format` only (the `encoding` block removed)

```diff
diff --git a/datastorekit/store_fingerprint.py b/datastorekit/store_fingerprint.py
--- a/datastorekit/store_fingerprint.py
+++ b/datastorekit/store_fingerprint.py
@@ -205,22 +205,6 @@
                 f"the recorded fingerprint is format {recorded_format!r} and this one is format "
                 f"{current_format!r}; fingerprints of different formats are not compared. "
                 f"Recompute both from the stores",
-            )
-        )
-    recorded_encoding = recorded.get("encoding_format")
-    current_encoding = current.get("encoding_format")
-    if recorded_encoding != current_encoding:
-        versions.append(
-            _difference(
-                "encoding",
-                None,
-                None,
-                recorded_encoding,
-                current_encoding,
-                f"the recorded fingerprint is encoding format {recorded_encoding!r} and this "
-                f"one is encoding format {current_encoding!r}; fingerprints encoded by "
-                f"different releases of datastorekit are not compared. Recompute both from "
-                f"the stores with one release",
             )
         )
     if versions:
```

`FAILED (failures=2)`: test 6, `test_the_versions` (`0 != 1`, at the encoding mismatch) and `test_another_encoding_of_the_same_store` (`[] != [('encoding', 1, 2)]`).

### (d) the `format` entry's text changed by one word ("not" → "never")

```diff
diff --git a/datastorekit/store_fingerprint.py b/datastorekit/store_fingerprint.py
--- a/datastorekit/store_fingerprint.py
+++ b/datastorekit/store_fingerprint.py
@@ -203,7 +203,7 @@
                 recorded_format,
                 current_format,
                 f"the recorded fingerprint is format {recorded_format!r} and this one is format "
-                f"{current_format!r}; fingerprints of different formats are not compared. "
+                f"{current_format!r}; fingerprints of different formats are never compared. "
                 f"Recompute both from the stores",
             )
         )
```

`FAILED (failures=1)`: test 6, `test_the_versions`, at the literal: `'…are never compared. Recompute both from the stores' != '…are not compared. Recompute both from the stores'` (its "Recompute both" check passes first).

### (e) `encoding_format` placed before `digest` in the listing's first line

```diff
diff --git a/datastorekit/store_fingerprint.py b/datastorekit/store_fingerprint.py
--- a/datastorekit/store_fingerprint.py
+++ b/datastorekit/store_fingerprint.py
@@ -335,8 +335,8 @@
     """
     yield (
         f"# fingerprint_format {fingerprint['fingerprint_format']} "
-        f"digest {fingerprint['digest']} "
-        f"encoding_format {fingerprint['encoding_format']}"
+        f"encoding_format {fingerprint['encoding_format']} "
+        f"digest {fingerprint['digest']}"
     )
     for name, cls in inventory.classes.items():
         entry = fingerprint["classes"][name]
```

`FAILED (failures=1)`: test 5, `test_the_listing_hashes_to_the_fingerprint`, at the first line's words (`['#', …, '1', 'encoding_format', '1', 'digest', '7656b60…'] != ['#', …, '1', 'digest', '7656b600…', 'encoding_format', '1']`).

### (f) `_tag_sets` grouping by sorted tags

```diff
diff --git a/datastorekit/store_fingerprint.py b/datastorekit/store_fingerprint.py
--- a/datastorekit/store_fingerprint.py
+++ b/datastorekit/store_fingerprint.py
@@ -79,7 +79,7 @@
     that carry exactly that set, in the records' own order."""
     groups = {}
     for record in records:
-        groups.setdefault(tuple(record.tags), []).append(record.canonical_json())
+        groups.setdefault(tuple(sorted(record.tags)), []).append(record.canonical_json())
     return sorted(groups.items())
 
 
```

`Ran 21 tests … OK`: **equivalent, not a gap** (correction 5). `read_records` builds every `Record`'s tags as `tuple(sorted(…))` (`store_inventory.py:765-767`), and a record is made nowhere else, so on any inventory `read_inventory` gives, `tuple(sorted(record.tags)) == tuple(record.tags)` and nothing changes.

### (g) `_sha256_lines` omitting the newline after the last line (`"\n".join(lines)`)

```diff
diff --git a/datastorekit/store_fingerprint.py b/datastorekit/store_fingerprint.py
--- a/datastorekit/store_fingerprint.py
+++ b/datastorekit/store_fingerprint.py
@@ -68,9 +68,7 @@
 def _sha256_lines(lines) -> str:
     """SHA-256 (hex) of ``lines``, each followed by a newline."""
     hasher = hashlib.sha256()
-    for line in lines:
-        hasher.update(line.encode("utf-8"))
-        hasher.update(b"\n")
+    hasher.update("\n".join(lines).encode("utf-8"))
     return hasher.hexdigest()
 
 
```

`FAILED (failures=14)`: test 4, `test_the_golden_fingerprint` (every class and tag-set digest differs from the golden), and test 5, `test_the_listing_hashes_to_the_fingerprint`, in all 13 class sub-tests (the lines, each followed by a newline, no longer hash to the class digest). Test 4's recomputed overall digest passes, as it should: it hashes the fingerprint's own class entries.

### (h) `fingerprint_format` given a default of `1`

```diff
diff --git a/datastorekit/store_fingerprint.py b/datastorekit/store_fingerprint.py
--- a/datastorekit/store_fingerprint.py
+++ b/datastorekit/store_fingerprint.py
@@ -84,7 +84,7 @@
 
 
 def fingerprint_of(
-    inventory, fingerprint_format: int, taken: Optional[Mapping[str, Any]] = None
+    inventory, fingerprint_format: int = 1, taken: Optional[Mapping[str, Any]] = None
 ) -> dict:
     """
     The fingerprint of ``inventory``, what ``read_inventory`` returns, at the client's
```

`FAILED (failures=1)`: test 7, `test_refusals`, at the missing format: `TypeError not raised`.

### (j) the integer check removed (the `< 1` check kept)

```diff
diff --git a/datastorekit/store_fingerprint.py b/datastorekit/store_fingerprint.py
--- a/datastorekit/store_fingerprint.py
+++ b/datastorekit/store_fingerprint.py
@@ -106,11 +106,6 @@
       word before the first colon). Outside every digest;
     - ``taken``: ``taken``, the caller's mapping, copied, or ``None``. Outside every digest.
     """
-    if isinstance(fingerprint_format, bool) or not isinstance(fingerprint_format, int):
-        raise TypeError(
-            f"fingerprint_of(): fingerprint_format must be an int, not "
-            f"{type(fingerprint_format).__name__} {fingerprint_format!r}"
-        )
     if fingerprint_format < 1:
         raise ValueError(
             f"fingerprint_of(): fingerprint_format must be at least 1, not "
```

`FAILED (failures=5)`: test 7, `test_refusals`, in all four sub-tests and at the last check (correction 1): `True` and `1.0` are hashed (`TypeError not raised`; probed in this export, digests `2523ed96590f…` and `46a42f83b79b…`); `"1"` and `{"when": "now"}` raise Python's `TypeError: '<' not supported between instances of 'str' and 'int'` (and `'dict'`), which does not match `^fingerprint_of\(\): fingerprint_format must be an int`; and `fingerprint_of(object(), "1")` raises the same comparison error, which does not match `^fingerprint_of\(\)`. With a bare `assertRaises(TypeError)` only the two hashed values would fail.

### (i) `problems` counted by the whole problem string

```diff
diff --git a/datastorekit/store_fingerprint.py b/datastorekit/store_fingerprint.py
--- a/datastorekit/store_fingerprint.py
+++ b/datastorekit/store_fingerprint.py
@@ -133,7 +133,7 @@
                 for tags, group in _tag_sets(cls.records)
             ],
         }
-        kinds = Counter(problem.split(":", 1)[0] for problem in cls.problems)
+        kinds = Counter(problem for problem in cls.problems)
         if kinds:
             problems[name] = dict(sorted(kinds.items()))
 
```

`FAILED (failures=2)`: test 2, `test_an_orphan_value_row_is_a_problem_entry_only` (`{'Trace': {'orphan-value: Trace: 1 TraceStep row(s) on shard #0 …': 1}} != {'Trace': {'orphan-value': 1}}`) and `test_deleting_the_row_alone_is_also_a_problem_entry` (the same, for `orphan-member` and `orphan-tag`).

---

## 6. Observations not acted on

1. **`listing_lines` needs a fingerprint of this module's.** It reads `fingerprint['encoding_format']`
   (the orchestrator's addition), so a fingerprint made by the source's own code, which has no such
   key, raises `KeyError` there. Any client that writes listings with the package's function must
   make its fingerprints with the package's `fingerprint_of` too. By design; for 02's addendum to
   the source repository. No issue.
2. **Two fingerprints that both lack `encoding_format` compare as before**: both versions read
   `None`, so they are equal (U2 asks only that one without it differ from one with it). The
   source's `TestFormats` relies on this. By design; no issue.
3. **`taken` is copied with `dict()`**, so a `taken` that is not a mapping but a sequence of pairs
   is accepted, as in the source. Unchanged by U1; no issue.
4. **`test_store_fingerprint` builds about 20 full stores** in under 2 s; it adds about 1–2 s to
   the suite. Not measured further.
5. **The scratch tools** are in `<scratch-fp01>/probe/` and `<scratch-fp01>/extract/`, not in the
   repository: `suite.sh`, `mkenv.sh`, `breakrun.sh`, `breaks.py`, `write_golden.py`,
   `ast_compare.py`, `vocab_check.py`, `names.py`; `sgk_section.py`, `sgk_fingerprint.py`,
   `equivalence.py`. Each run's output is in `<scratch-fp01>/logs/`, and each diff in
   `<scratch-fp01>/diffs/`.

---

## 7. Issues

- **Opened, narrowed or closed**: none.
- **`docs/OPEN_ISSUES.md`**: unchanged, **4 open**, all on `inherited-issues`' board.

---

## 8. State handed to the next prompt

- **`HEAD`** is this commit, unpushed and untagged. The local `origin/main` ref is `5f972be`; the
  tags are `v0.1.0` to `v0.3.0`, unchanged. `pyproject.toml` is at `0.3.0`.
- **The suite** is 530, in `venv/` and at the high end. The port check passes over 20 modules with
  1 test declared not ported. `black` leaves 78 files unchanged.
- **The interfaces** (README §4): `datastorekit.store_fingerprint` with `fingerprint_of(inventory,
  fingerprint_format, taken=None)`, `compare_fingerprints(recorded, current)`,
  `listing_lines(inventory, fingerprint)` and `ENCODING_FORMAT` (1); the golden
  `tests/data/store_fingerprint-neutral-1-encoding-1.json`; contract §9.7 and its head line; the
  equivalence record above (§4.3), for the orchestrator to replay.
- **For 02** (`v0.4.0`, U6): what changes for the source repository when it calls the package's
  code is as README §0.2 says: the required format (its positional `fingerprint_of(inventory,
  taken)` must become `fingerprint_of(inventory, 6, taken)` or pass `taken=` by keyword, or it is
  refused with `TypeError`); `encoding_format` in every fingerprint (its shape test and golden
  comparison); the comparison's `encoding` entry; the listing's first line, whose words 2 and 4 are
  unchanged; and §6 item 1 above. `PROVENANCE.md` should name the module's source (SGK `c8a7f14`,
  `RunRegistry/stores.py:1164-1400`, extract SHA-256 `9b1a8aed…0108`).
- **Open**: none on this repository's own campaign boards; the four inherited issues of
  `docs/OPEN_ISSUES.md` §1.2.
