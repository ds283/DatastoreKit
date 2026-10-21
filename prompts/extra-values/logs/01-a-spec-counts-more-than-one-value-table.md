# Log 01 — a spec counts more than one value table

**Subject:** Let an inventory spec count more than one value table · **Commit:** this commit ·
**Date:** 2026-10-21 · **Model:** Claude Opus 5.5 · **Result:** landed; unpushed and untagged; not
yet reviewed.

A factory's `InventorySpec` can now name further value tables, `extra_values` (table → its column
naming this class's serial), and each record of such a class carries `extra_value_counts` (table →
its count, 0 where none). `Record.as_json` adds the fifth key `"extra_value_counts"` only when the
mapping is not empty, so a record of a class that declares no extra table is what it was, byte for
byte. The counting is one inner function, `_count_values`, used for `values` and then for each
extra table in sorted order, with `values`' `orphan-value` problem in its words; a replicated class
whose extra counts differ is a `replicated-divergence` through `_combine`'s unchanged comparison.
`inventory_classes` gains one refusal (a spec's `values` table also in its `extra_values`); no spec
construction, `inventory_specs`, `read_records` or `dependent_tables` refuses anything new (U1).
`ENCODING_FORMAT` stays **1**, with the paragraph of U2 after its comment (U2). `pyproject.toml`
stays at `0.4.0`; the pool, `store_reader.py` and `SQL/schema.py` are unchanged.

The neutral client declares the field: a `TraceMark` table under `Trace`, written for `trace-one`
and held twice under Trace 3 in the full store (U3). Its new witness,
`schema_at_extra-values-01.json`, has SHA-256 `971ec253ce78d5f0f7cfeccf13dd0a3b94fc3f5bc9a57b2eadee7b7f2c07d196`,
the planner's; its diff from `schema_at_extraction-06.json` is 117 lines, every one an addition, all
of them `TraceMark`. `NEUTRAL_FORMAT` is 2 and its golden, `store_fingerprint-neutral-2-encoding-1.json`,
has digest `524cefd41ab593f73abe0610558d8444c64f9514c4d1edb5041591737161d14a` and file SHA-256
`848fe4c90bd622bafda061d6e59cf780308b8a7cb6044203f18da2fa43ba9fb8`, the planner's, equal at both
ends. A new module of **8** tests, `tests/test_inventory_extra_values.py`, pins it (U4); its test 1
reproduces the format-1 golden (`7656b600…`), every field but `taken`, through a registry whose
`Trace` spec declares no extra table. The suite goes from **530 to 538**, `OK`, in `venv/` and at
the high end. Each breakage (a)–(i) fails every test §4.4 names, and others as the dispatch note's
correction 2 tabulates.

`docs/client-contract.md` gains a head line and §9.8, by addition only (18 lines added, none
removed). No issue was opened or closed: the index stays at **4 open**.

No client was written, run, imported or opened (SI's brief was read through `git show`); nothing
was pushed, tagged or downloaded; Ray was not started.

Prompt: [`../01-a-spec-counts-more-than-one-value-table.md`](../01-a-spec-counts-more-than-one-value-table.md),
with the orchestrator's dispatch note §0: five corrections, its additions, its checked facts and
its conventions. §2 classifies each.

`<scratch>` below is `<session scratchpad>/agent01`, outside the repository. Times are BST,
2026-10-21.

---

## 1. What shipped

Line numbers are this commit's.

### 1.1 `datastorekit/store_inventory.py` (§2.1, U1), +55 −16

- **`Record`** (`:183-215`): a last field `extra_value_counts: Mapping[str, int] =
  field(default_factory=dict)` (`:194`), under a comment (`:191-193`) saying what it holds and that
  it is empty, and then not in `as_json`, where the class declares no extra table. **`as_json`**
  (`:196-205`) builds the four keys as before into `out`, then adds `"extra_value_counts":
  dict(self.extra_value_counts)` only when it is not empty (`:203-204`). `canonical_json`,
  `identity` and `__hash__` (`:207-215`) are unchanged. The dataclass's explicit `__hash__` is kept
  (a dataclass with `eq=True, frozen=True` does not replace an explicit one), so a record with a
  dict field stays hashable.
- **`InventorySpec`** (`:304-344`): a last field `extra_values: Mapping[str, str] =
  field(default_factory=dict)` (`:317`); `keywords()` a last entry `"extra_values":
  self.extra_values` (`:328`); `dependencies()` unchanged. Its docstring gains a parenthesis
  naming the field (`:307-309`).
- **`read_records`** (`:523-836`): a last keyword `extra_values: Optional[Mapping[str, str]] =
  None` (`:535`), and a docstring item after `values`' (`:549-551`). The block that counted
  `values` is now the inner function `_count_values(value_table_name, parent_column)`
  (`:660-683`): the same `GROUP BY` (`:666-668`), the counts of the serials on the shard returned,
  and the `orphan-value` problem appended in the same words (`:673-682`) for the rest. It is called
  for `values` when given (`:685-687`), then for each extra table in sorted order
  (`:688-692`). Each record gets `extra_value_counts={table: found.get(row.serial, 0) for …}`
  (`:803-806`), an empty dict when none is declared. The comment above the function reads "one
  GROUP BY per value table, never a listing" (it read "one GROUP BY, never a listing"). Nothing
  else of the function changed.
- **`inventory_classes`** (`:962-1015`): after the polymorphic-parent check and before
  `depends[name]`, a spec whose `values` table is a key of its `extra_values` raises `ValueError`
  `"inventory_classes(): <class> names <table> both as its value table and in its extra_values"`
  (`:990-994`); its docstring's list of refusals names it (`:971-973`). No refusal was added to
  `InventorySpec`, `inventory_specs` or `read_records`.
- **The module docstring**: the record's bullets gain `extra_value_counts` (`:24-27`: what it
  holds, 0 where none, absent from `as_json` where the class declares no extra table); the sentence
  after them ("A computed-values field can be added … beside these four …", `:29-30`) is not
  rewritten; "Who defines identity" names "any further value tables" (`:34`); "Shards" reads
  "compared on key, tags, validated flag, value count and extra value counts" (`:58`, the paragraph
  reflowed to `:57-62`); `orphan-value`'s line covers "of the value table or of a further value
  table" (`:68-69`).

### 1.2 `datastorekit/store_fingerprint.py` (§2.2, U2), +6

After `:64` ("A change to a client's specs or registry is that client's ``fingerprint_format``,
never ENCODING_FORMAT."), a blank comment line (`:65`) and the paragraph (`:66-70`) in §2.2's
words, as a comment. `ENCODING_FORMAT = 1` is now `:71`. Nothing else of the file changed.

### 1.3 The neutral client (§2.3, U3)

- **`tests/client/factories.py`** (+39): `TraceMark_factory(SQLAFactoryBase)` (`:1328-1352`),
  between `TraceStep_factory` and `Trace_factory`, with §2.3 item 1's docstring, `register()` and
  `build`. `Trace_factory`'s docstring gains a paragraph on the marks (`:1362-1364`); its `store`
  writes one `TraceMark` row per entry of `obj.marks` after the steps (`:1470-1473`); its
  `inventory_spec` declares `extra_values={"TraceMark": "trace_serial"}` after `validated`
  (`:1511`). The module docstring gains one paragraph naming `TraceMark` among the tables written
  by their owner's `store` (`:25-26`; §2, D9).
- **`tests/client/objects.py`** (+4 −1): `Trace.__init__` gains `marks: Sequence[int] = ()`, last,
  kept as `self.marks = list(marks)`; its docstring says so.
- **`tests/client/build.py`** (+18 −3): `TRACE_MARKS = {"trace-one": (0, 1)}` beside `TRACES`,
  with a comment (`:67-69`); `make_trace` gains `marks: Sequence[int] = ()`, last, passed to
  `Trace`, its docstring saying so; `write_every_class` passes `marks=TRACE_MARKS.get(label, ())`.
  Both calls are written one argument per line.
- **`tests/client/registry.py`** (+5 −2): `"TraceMark": _f.TraceMark_factory` after
  `"TraceStep"`, under a comment (`:95-96`); `"TraceMark"` after `"TraceStep"` in `traces`
  (`:159`); the roles table's `Trace` row names its further value table, and the `Trace_tags`,
  `TraceStep` row is now `Trace_tags`, `TraceStep`, `TraceMark` (kind "neither"), saying that
  `extra-values` prompt 01 added it (`:35-36`).
- **`tests/real_store_fixtures.py`** (+14 −1): in `_full_shard0`, after Trace 4's `TraceStep`
  rows, the two `TraceMark` rows of §2.3 item 6 under a comment (`:601-609`). `_write_shard` and
  `build_real_store` gain a last keyword `factories: Optional[Mapping[str, object]] = None`, the
  neutral registry when `None`, from which `_write_shard` builds its schema; `build_real_store`'s
  docstring says so, and that the primary's table lists are the neutral registry's either way.
  `build_full_store`, its empty-shard cache and `fill_required` are unchanged.

### 1.4 The witness (§2.4)

Captured in `venv/` from this checkout's root, from the tree of §1.1–§1.3, before any test was
amended:

```
./venv/bin/python datastorekit/tests/schema_description.py datastorekit/tests/data/schema_at_extra-values-01.json
shasum -a 256 datastorekit/tests/data/schema_at_extra-values-01.json
971ec253ce78d5f0f7cfeccf13dd0a3b94fc3f5bc9a57b2eadee7b7f2c07d196  datastorekit/tests/data/schema_at_extra-values-01.json
```

The planner's (prompt §1.1). Re-captured into scratch from the trees after D9 and after D11 (the
final tree): the same SHA-256 each time. `WITNESS` (`test_schema_builder.py:47`) names it, and the module's
docstring gains a sentence saying the current witness is now this one, captured by `extra-values`
prompt 01, differing from `schema_at_extraction-06.json`, which is kept, only by the `TraceMark`
table; the sentences about the earlier witnesses stay as written. `schema_at_extraction-06.json` is
unchanged.

**The diff between the two witnesses**, 147 lines with headers and hunk lines; 117 changed lines,
every one an addition (`+`), none removed: the class name in the registry-order list, the whole
`TraceMark` entry (it sorts before `TraceStep`), and the name in the two table lists.

```diff
--- a/datastorekit/tests/data/schema_at_extraction-06.json
+++ b/datastorekit/tests/data/schema_at_extra-values-01.json
@@ -18,6 +18,7 @@
   "Trace",
   "Trace_tags",
   "TraceStep",
+  "TraceMark",
   "Weave",
   "Weave_tags",
   "Weave_members"
@@ -1461,6 +1462,120 @@
     "name": "Trace"
    }
   },
+  "TraceMark": {
+   "has_table": true,
+   "record": {
+    "columns": [
+     {
+      "column": "trace_serial",
+      "of_table": "TraceMark"
+     },
+     {
+      "column": "mark_index",
+      "of_table": "TraceMark"
+     }
+    ],
+    "key_on_version": false,
+    "monotone_flags": [],
+    "name": "TraceMark",
+    "owner_column": null,
+    "serial_col": {
+     "column": "serial",
+     "of_table": "TraceMark"
+    },
+    "table": {
+     "table": "TraceMark"
+    },
+    "use_serial": true,
+    "use_stepping": false,
+    "use_timestamp": false,
+    "use_version": false,
+    "validate_on_startup": false,
+    "validated_column": null
+   },
+   "table": {
+    "columns": [
+     {
+      "autoincrement": "'auto'",
+      "default": null,
+      "foreign_keys": [],
+      "index": null,
+      "name": "serial",
+      "nullable": false,
+      "primary_key": true,
+      "server_default": null,
+      "sqlite_type": "INTEGER",
+      "type": "Integer()",
+      "unique": null
+     },
+     {
+      "autoincrement": "'auto'",
+      "default": null,
+      "foreign_keys": [
+       {
+        "ondelete": null,
+        "onupdate": null,
+        "target": "Trace.serial"
+       }
+      ],
+      "index": true,
+      "name": "trace_serial",
+      "nullable": false,
+      "primary_key": false,
+      "server_default": null,
+      "sqlite_type": "INTEGER",
+      "type": "Integer()",
+      "unique": null
+     },
+     {
+      "autoincrement": "'auto'",
+      "default": null,
+      "foreign_keys": [],
+      "index": null,
+      "name": "mark_index",
+      "nullable": false,
+      "primary_key": false,
+      "server_default": null,
+      "sqlite_type": "INTEGER",
+      "type": "Integer()",
+      "unique": null
+     }
+    ],
+    "constraints": [
+     {
+      "columns": [
+       "serial"
+      ],
+      "kind": "PrimaryKeyConstraint",
+      "name": null
+     },
+     {
+      "columns": [
+       "trace_serial"
+      ],
+      "kind": "ForeignKeyConstraint",
+      "name": null,
+      "targets": [
+       "Trace.serial"
+      ]
+     }
+    ],
+    "ddl": "CREATE TABLE \"TraceMark\" (\n\tserial INTEGER NOT NULL, \n\ttrace_serial INTEGER NOT NULL, \n\tmark_index INTEGER NOT NULL, \n\tPRIMARY KEY (serial), \n\tFOREIGN KEY(trace_serial) REFERENCES \"Trace\" (serial)\n)",
+    "index_ddl": [
+     "CREATE INDEX \"ix_TraceMark_trace_serial\" ON \"TraceMark\" (trace_serial)"
+    ],
+    "indexes": [
+     {
+      "columns": [
+       "trace_serial"
+      ],
+      "name": "ix_TraceMark_trace_serial",
+      "unique": false
+     }
+    ],
+    "name": "TraceMark"
+   }
+  },
   "TraceStep": {
    "has_table": true,
    "record": {
@@ -3220,6 +3335,7 @@
   "Sample_tags",
   "Tessera",
   "Trace",
+  "TraceMark",
   "TraceStep",
   "Trace_tags",
   "Weave",
@@ -3253,6 +3369,7 @@
   "Trace",
   "Trace_tags",
   "TraceStep",
+  "TraceMark",
   "Weave",
   "Weave_tags",
   "Weave_members"
```

### 1.5 The golden (§2.5)

`NEUTRAL_FORMAT = 2` (`test_store_fingerprint.py:57`), its comment unchanged. The golden was
written once, from `venv/`, before any test was amended, by this script (kept here, not in the
repository; `<scratch>/scripts/write_golden.py`), run from the root of the tree under test:

```python
"""Write the neutral store's golden fingerprint at fingerprint_format=2 (extra-values prompt 01).

usage: python write_golden.py <output.json>   (run from the root of the tree under test)
"""
import hashlib
import json
import sys
import tempfile
from pathlib import Path

import datastorekit
from datastorekit.store_fingerprint import ENCODING_FORMAT, fingerprint_of
from datastorekit.store_inventory import read_inventory
from datastorekit.tests.client.registry import factories
from datastorekit.tests.real_store_fixtures import build_full_store

out = Path(sys.argv[1])
with tempfile.TemporaryDirectory() as tmp:
    inventory = read_inventory(build_full_store(Path(tmp)).primary, factories)
    fingerprint = fingerprint_of(inventory, 2, taken=None)
text = json.dumps(fingerprint, indent=2, sort_keys=True) + "\n"
out.write_text(text, encoding="utf-8")
print("datastorekit:", datastorekit.__file__)
print("encoding_format:", ENCODING_FORMAT)
print("digest:", fingerprint["digest"])
print("file sha256:", hashlib.sha256(text.encode("utf-8")).hexdigest())
```

```
datastorekit: /Users/ds283/Documents/Code/DatastoreKit/datastorekit/__init__.py
encoding_format: 1
digest: 524cefd41ab593f73abe0610558d8444c64f9514c4d1edb5041591737161d14a
file sha256: 848fe4c90bd622bafda061d6e59cf780308b8a7cb6044203f18da2fa43ba9fb8
```

Both the planner's. At the high end (`<scratch>/exp-01`, `<scratch>/exp-final` and
`<scratch>/exp-final2`, the final tree), the same script printed the same digest and file SHA-256,
and `cmp` found its output identical to the committed file. Against the format-1 golden: the keys that differ are `classes`,
`digest` and `fingerprint_format`, and of `classes` only `Trace`'s entry.
`store_fingerprint-neutral-1-encoding-1.json` is unchanged. In
`test_another_format_moves_only_the_overall_digest` the "another format" `2` (`:651`, `:652`) is
`NEUTRAL_FORMAT + 1`.

### 1.6 The tests (§2.6, U4)

**Amended literals**, no assertion call added or removed:
- `test_neutral_client.py`, `test_every_declaration_field_is_in_use` (`:310`): the field list
  gains `"extra_values"`, last, with a comment naming the prompt, the list one name per line.
  The module docstring enumerates "every field of `InventorySpec`, `Parent` and `ParentSet` in
  use", which still holds, so it is unchanged.
- `test_store_inventory.py`: `VALUE_TABLES` gains `"TraceMark"`, with a comment (`:80-81`); a new
  module-level `EXTRA_VALUE_CLASSES = ("Trace",)`, with a comment (`:84-86`);
  `test_records_are_json_safe`'s expected set is the four keys `| ({"extra_value_counts"} if name
  in EXTRA_VALUE_CLASSES else set())`, the same one `assertEqual`.
- `test_store_fingerprint.py`: `NEUTRAL_FORMAT = 2`; the two `2`s of §1.5.
- `test_schema_builder.py`: `WITNESS` and the docstring sentence of §1.4.

**The new module**, `datastorekit/tests/test_inventory_extra_values.py` (390 lines). Its docstring
numbers the eight tests and says no test starts Ray or constructs a `ShardedPool`, and every
store is in a temporary directory. A `tearDownModule` raises if Ray was initialised, as
`test_store_fingerprint`'s does. Module-level helpers, none of which asserts:
- `_respecified(factory, extra_values)`: a subclass of `factory` whose `inventory_spec` returns
  `InventorySpec(**{**keywords, "extra_values": dict(extra_values)})`, `keywords` being the
  factory's own spec's `keywords()`; the spec is built when the hook is called;
- `undeclared()`: the neutral registry with `Trace`'s factory so replaced, `extra_values={}`;
- `_TraceNote_factory` and `_GadgetNote_factory`: child tables with `trace_serial` (foreign key
  `Trace.serial`) or `gadget_serial` (foreign key `Gadget.serial`), indexed and not null, and
  `note_index` (`Integer`, not null), no version, no timestamp;
- `wider()`: the neutral registry with `GadgetNote` after `GadgetPart` and `TraceNote` after
  `TraceMark`, `Trace` declaring `{"TraceMark": "trace_serial", "TraceNote": "trace_serial"}` and
  `Gadget` `{"GadgetNote": "gadget_serial"}`;
- `refused()`: the neutral registry with `Trace` declaring `{"TraceStep": "trace_serial"}`;
- `wider_store(directory, added)`: `build_real_store(…, factories=wider())` of `full_rows()`'s
  rows through `fill_required`, then `added`'s rows (each stating every non-null column) appended
  with `with_rows`, and `full_rows()`'s shard keys (correction 1);
- `canonical_lines`, `by_label`, and `FORMAT_1_GOLDEN`, the path of
  `store_fingerprint-neutral-1-encoding-<ENCODING_FORMAT>.json`; `MARKED_TRACE =
  "fixture-trace-3"`.

| # | Test | What it asserts |
|---|---|---|
| 1 | `TestCompatibility.test_the_format_1_golden_and_every_other_class` | `build_full_store()` read through `undeclared()` at format 1 equals `FORMAT_1_GOLDEN` but for `taken`; read through the neutral registry and `undeclared()`, the same classes, and every class but `Trace` the same canonical lines |
| 2 | `TestCounts.test_the_counts` | each Trace's `extra_value_counts` is `{"TraceMark": 2}` for `fixture-trace-3` and `{"TraceMark": 0}` otherwise, and its `value_count` that read through `undeclared()`; every other class's records `{}` and `as_json` keys the four; no problems |
| 3 | `TestTwoTables.test_each_table_is_counted` | through `wider()`, one `TraceNote` row under Trace 3: its counts `{"TraceMark": 2, "TraceNote": 1}`, every other Trace `{"TraceMark": 0, "TraceNote": 0}`; no problems |
| 4 | `TestOrphans.test_an_orphan_row_is_named` | through `wider()`, a `TraceNote` row on shard 1 naming serial 999: the store's one problem is `Trace`'s, starts `orphan-value`, names `TraceNote` and `shard #1`; the fingerprint's `problems` is `{"Trace": {"orphan-value": 1}}` |
| 5 | `TestReplicatedDivergence.test_one_shard_alone_holds_an_extra_row` | through `wider()`, a `GadgetNote` row under Gadget 1 on shard 0 alone: the store's one problem is `Gadget`'s, `replicated-divergence` |
| 6 | `TestTheFingerprintSeesIt.test_one_row_deleted` | `build_full_store()` and the same with `DELETE FROM TraceMark WHERE serial = 2` on shard 0, at `NEUTRAL_FORMAT`: the overall digests differ, every class entry but `Trace`'s is equal and `Trace`'s differs, and `compare_fingerprints` gives entries naming `Trace` alone |
| 7 | `TestTheRefusal.test_refused_by_inventory_classes_only` | `inventory_classes(refused())` raises `ValueError` matching `Trace\b.*\bTraceStep\b`; `inventory_specs` of it returns the spec; `dependent_tables(["Trace"], …)` of it equals the neutral registry's |
| 8 | `TestDependentTables.test_the_same_answer` | for drops of `["Trace"]`, `["TraceMark"]`, `["keypoint"]`, the neutral registry and `undeclared()` give equal answers; a drop of `["Trace"]` takes `TraceMark` |

The module is not a port, and is not in `compare_ported_tests.py`'s `PORTED`.

### 1.7 The contract (§2.7)

`docs/client-contract.md`, +18 −0. At the head, after the §9.7 line, a line: §9.8 is measured from
the package at `extra-values` prompt 01's tree, and its line numbers are that tree's. At the end,
**§9.8 "`extra-values` prompt 01"**, in §9's form: a preamble (one change; the README and U1–U3,
the user's request and ruling; nothing the pool writes or reads changes, nor any message, refusal
or exception of the pool's; a spec that declares no extra table gives the records it gave), and four
rows: `InventorySpec.extra_values` (supersedes §4's "**6** fields" in part, now 7, and adds a row
to its table; pinned by tests 2–4, 6); `Record.extra_value_counts` and `as_json` (supersedes none:
**§1–§9.7 do not state `Record`'s fields**; §9.7's `ENCODING_FORMAT` row cites `as_json` as its
item 1, which the last row reads; pinned by tests 1, 2, 5); the refusal (supersedes none; §4's
"What the declarations must satisfy together" gains one; pinned by test 7); and `ENCODING_FORMAT`'s
item 1 (supersedes §9.7's `ENCODING_FORMAT` row in that part, the paragraph in §2.2's words; pinned
by test 1 and the format-1 golden). No marker is set on any row of §1–§9.7; `git diff` of the file
has 18 `+` lines and no `-` line.

### 1.8 The records

This log; the board (header, §1's row for 01 and a paragraph under it, §3's dated line); the
README (header and §2's row for 01); `prompts/INDEX.md` (the header count, now "1 in progress",
and the campaign's line). `docs/OPEN_ISSUES.md` is unchanged at 4: no issue was opened or closed.

---

## 2. Deviations from the prompt

The dispatch note's five corrections and its additions first, then this prompt's own.

**C1. `fill_required` knows only the neutral schema** — STRUCTURALLY REQUIRED (correction 1).
`wider_store` puts `full_rows()`'s rows through `fill_required` and then appends the test's
`TraceNote` / `GadgetNote` rows, each stating every non-null column, and passes `full_rows()`'s
shard keys to `build_real_store`. `fill_required` and `build_full_store` are unchanged. Tests 3–5
got every count they expect and no problem but the one each makes.

**C2. Breakages fail more than §4.4 names** — STRUCTURALLY REQUIRED (correction 2, a reading of
§6's fourth stop). Every named test fails under its breakage; the extra failures are those the
note's table lists, test for test (§5). Not a stop.

**C3. The brief is read through `git`** — STRUCTURALLY REQUIRED (correction 3). Read with `git -C
…/StochasticInstantons show f5f395b:.prompts/dk-and-rpk-migration/datastorekit-second-value-table-brief.md`
(211 lines), as text; nothing in it was acted on beyond the prompt. Its findings agree with README
§0.1, and its advice differs from this campaign where README §0.2 says.

**C4. `ResourceWarning` at the high end** — STRUCTURALLY REQUIRED (correction 4). 4 lines at the
high end before (at `HEAD`) and after (both the first after-run and the final tree), each time two
warnings of one kind, an unclosed `sqlite3.Connection` reported from inside SQLAlchemy; the frame
it is reported from varies run to run (`util/langhelpers.py:527` before; `sql/visitors.py:126` and
`sql/base.py:2174`, then `sql/crud.py:456` and `sql/base.py:2174`, then `event/base.py:137` and
`sql/selectable.py:3160`, after), which is where the garbage collector happened to run. 0 in
`venv/` before and after.

**C5. Line numbers** — STRUCTURALLY REQUIRED (correction 5), recorded as found at `3e6d550`
(`datastorekit/` unchanged since `c8570e8`): `store_inventory.py`'s docstring is `:1-84`, `Record`
`:177-203`, `InventorySpec` `:292-329`, the counting's comment `:640` and block `:641-663`;
`store_fingerprint.py`'s comment `:38-64`, the constant `:65`; `test_every_declaration_field_is_in_use`
`:310`; `test_value_tables_are_only_counted` `:617`; `NEUTRAL_FORMAT` `:57`; the contract's §9.7 head
line `:43-44`, §9.7 `:372-386`.

**A1. The work order** — IMPLEMENTATION CHOICE, at the orchestrator's direction. Baseline;
§2.1–§2.3; the witness and the golden, each checked against the planner's hashes, before any test
was amended; the amended literals of §2.6 and the suite once (`Ran 530 tests … OK`); the new
module; both ends; the breakages; §2.7 and the records; then the final runs.

**A2. The high-end venv** — IMPLEMENTATION CHOICE, at the orchestrator's direction, with one
variation. A constraints file of the highest version of each package under
`~/.cache/uv/archive-v0/*/*.dist-info` (`<scratch>/make_constraints.py`, 67 packages) holds
`ray==2.59.0` and `sqlalchemy==2.0.54`, which conflict with the pins asked for; those two lines
were left out (`<scratch>/constraints-hi.txt`, 65), and `uv pip install --offline -c … ray==2.55.1
sqlalchemy==2.0.46 setuptools` installed into a venv of `/opt/local/bin/python3.13` (3.13.16).
Each export was installed with `uv pip install --offline --no-deps --no-build-isolation -e`, and
every command run from the export's root under `env -u PYTHONPATH`, `datastorekit.__file__`
printed under it.

**A3. The golden at both ends** — IMPLEMENTATION CHOICE, at the orchestrator's direction (§1.5).

**A4. Test 7 makes the refusal visible** — IMPLEMENTATION CHOICE, at the orchestrator's direction.
`refused()` builds its spec inside the hook, so under (h) the refusal is met in `inventory_specs`;
the test matches the message on both names. Under (h) the test fails at its first assertion: the
moved refusal raises `ValueError` from `inventory_specs`, inside `inventory_classes`, whose message
cannot name the class (§5 (h)). Had the moved message named `Trace`, the next line,
`inventory_specs(factories)`, would raise.

**A5. Neutral names** — IMPLEMENTATION CHOICE, at the orchestrator's direction (§4.5).

**D1. Test 1 is one method** — IMPLEMENTATION CHOICE. §2.6 lists two assertions under test 1 and
§4.1 counts eight tests; both are in one method, which builds one store and reads it through both
registries.

**D2. The new module imports `NEUTRAL_FORMAT` from `test_store_fingerprint`** — IMPLEMENTATION
CHOICE, so that test 6 follows the neutral client's format without a second constant. The loader
finds no test case through it (only the integer is bound).

**D3. Test 4's orphan names serial 999; test 3's and 5's added rows state serial 1** —
IMPLEMENTATION CHOICE.

**D4. Test 6 asserts `Trace`'s entry differs and the comparison is not empty** — IMPLEMENTATION
CHOICE, beside §2.6's three assertions, so that "names `Trace` alone" cannot pass on an empty list.

**D5. The new module's `tearDownModule`** — IMPLEMENTATION CHOICE, as `test_store_fingerprint`'s.

**D6. Comments and docstrings beyond the letter of §2** — IMPLEMENTATION CHOICE: the comment
above `_count_values` reads "per value table"; `_count_values` has a one-line docstring;
`InventorySpec`'s docstring names the field in a parenthesis; comments naming the prompt above
the registry entry, `TRACE_MARKS`, the fixture rows, the `VALUE_TABLES` entry, `EXTRA_VALUE_CLASSES`
and the field list; `build_real_store`'s docstring adds that the primary's table lists are the
neutral registry's either way, which is what `wider()`'s stores rely on.

**D7. `wider()` places its tables** after `GadgetPart` and after `TraceMark`, in the registry's
order — IMPLEMENTATION CHOICE.

**D8. The contract's `Record` row** says "supersedes none", and why: §1–§9.7 do not state
`Record`'s fields (searched: the only mention of `as_json` is §9.7's `ENCODING_FORMAT` row) —
IMPLEMENTATION CHOICE in the form §2.7 offers.

**D9. `factories.py`'s module docstring** gains a paragraph naming `TraceMark` among the tables a
`store` writes (`:25-26`) — IMPLEMENTATION CHOICE. Its paragraph on prompt 04a lists the tables
"written by their owner's `store`", which would otherwise omit one. It was added after the first
high-end run; the witness, the golden and both suites were taken again (§4.1).

**D10. Breakage (i)'s first form** — UNINTENDED DRIFT, corrected before it was recorded. The
first patch for (i) counted the extra tables in Python and dropped their orphan reporting, so it
also errored test 4. That is more than (i) describes. The recorded (i) (§5) counts in Python and
reports orphans in `values`' words; under it only `test_value_tables_are_only_counted` fails, on a
`TraceMark` statement.

**D11. One docstring line reflowed** — UNINTENDED DRIFT, corrected before this commit. My edit
of the "Who defines identity" paragraph of `store_inventory.py`'s docstring had left a
120-character line (`:34`); the paragraph was reflowed to the file's width, the line count
unchanged. Found by a length scan before committing; the suite at both ends, the port check,
`black`, the witness, the golden and the nine breakages were all taken again on this final tree
(§4, §5).

---

## 3. The hazards (§3)

1. **The compatibility property.** Test 1 reproduces the format-1 golden through `undeclared()`,
   on a store that holds the `TraceMark` table and its rows. Under (a) it fails (§5). The golden
   test at format 2 is not the proof, and is not used as one.
2. **The witness and the golden** are the planner's to the byte (§1.4, §1.5); nothing was
   regenerated to pass.
3. **The pool.** `SQL/` is unchanged. `dependent_tables` reads `inventory_specs`, which refuses
   nothing new; test 7 shows it, and test 8 that its answers are unchanged.
4. **The port check.** `test_store_inventory`: 42 tests, 44 functions compared, 127 assertions,
   as before; "OK: 20 module(s) … 1 test(s) declared not ported", exit 0.
5. **The guards.** `test_layer_is_generic` and `test_prose_names_no_source`: 14 tests, OK, on the
   final tree. No new name is client vocabulary (§4.5).
6. **Additive documents.** The contract's diff has no `-` line; `schema_at_extraction-06.json` and
   `store_fingerprint-neutral-1-encoding-1.json` are unchanged (`git diff --stat c8570e8 --` them:
   empty).
7. **No Ray.** No test or script started it: `pgrep -fl 'gcs_server|raylet|ray::|default_worker\.py'`
   empty at the start and the end, `RAY_ADDRESS` unset.
8. **Offline only.** Every venv and install was `--offline` (A2); nothing was downloaded.
9. **The clients.** None written, run, imported or opened (§4.7).

---

## 4. Verification performed

### 4.1 The suite

| | `venv/` (3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39 / SQLite 3.53.4) | high end (3.13.16 / Ray 2.55.1 / SQLAlchemy 2.0.46 / SQLite 3.53.4) |
|---|---|---|
| before (`3e6d550`) | `Ran 530 tests in 99.597s` `OK`; 0 `ResourceWarning` lines | export of `HEAD`: `Ran 530 tests in 101.744s` `OK`; 4 lines (two warnings) |
| after §2.1–§2.5 and the amended literals, before the new module | `Ran 530 tests in 110.035s` `OK` | — |
| after (first) | `Ran 538 tests in 99.113s` `OK`; 0 | export `<scratch>/exp-01` (tree `10c9686`): `Ran 538 tests in 102.320s` `OK`; 4 lines (two warnings) |
| after D9 | `Ran 538 tests in 105.848s` `OK`; 0 | export `<scratch>/exp-final` (tree `4c581f3`): `Ran 538 tests in 104.844s` `OK`; 4 lines (two warnings) |
| after (final tree, D11) | `Ran 538 tests in 110.963s` `OK`; 0 | export `<scratch>/exp-final2` (tree `03a2fb7`): `Ran 538 tests in 106.954s` `OK`; 4 lines (two warnings) |

530 + 8 = 538. Each high-end run printed `datastorekit.__file__` under its export. The exports
were made by `git archive` of a tree written from a scratch copy of the index
(`GIT_INDEX_FILE=<scratch>/idx git add -A datastorekit docs; git write-tree`), so the repository's
own index was never touched.

### 4.2 The checks

- `docs/extraction/compare_ported_tests.py`: "OK: 20 module(s) keep their source's tests, classes
  and assertion skeletons; 1 test(s) declared not ported", exit 0, before and on the final tree.
  It reads SGK's source through `git show`, as it always has.
- `./venv/bin/black --check datastorekit docs`: "78 files would be left unchanged." before, "79
  files would be left unchanged." after. `black` reformatted only the new module.

### 4.3 The reproductions

| | planner | `venv/` | high end |
|---|---|---|---|
| witness SHA-256 | `971ec253…c07d196` | `971ec253ce78d5f0f7cfeccf13dd0a3b94fc3f5bc9a57b2eadee7b7f2c07d196` (and again from the trees after D9 and D11) | — (captured in `venv/`, §2.4) |
| golden digest | `524cefd4…161d14a` | `524cefd41ab593f73abe0610558d8444c64f9514c4d1edb5041591737161d14a` | the same (exp-01, exp-final, exp-final2) |
| golden file SHA-256 | `848fe4c9…43ba9fb8` | `848fe4c90bd622bafda061d6e59cf780308b8a7cb6044203f18da2fa43ba9fb8` | the same; `cmp` identical |

### 4.4 The breakages

§5, each applied in its own export at the high end.

### 4.5 The documents and the names

**Imported in `venv/`** (before D9 and D11, which changed docstrings only): `InventorySpec`'s fields `['leaves', 'parents',
'tags', 'values', 'validated', 'parent_sets', 'extra_values']`; `Record`'s `['key', 'tags',
'validated', 'value_count', 'extra_value_counts']`; `read_records`' last parameter
`extra_values`; `ENCODING_FORMAT` `1`; `Record.as_json`, `.identity`, `.canonical_json`,
`.__hash__`; `inventory_classes`, `inventory_specs`, `read_inventory`, `_combine`,
`fingerprint_of`, `compare_fingerprints`, `dependent_tables`; `TraceMark_factory`,
`Trace_factory.inventory_spec().extra_values` `{'TraceMark': 'trace_serial'}`, `TRACE_MARKS`
`{'trace-one': (0, 1)}`, `make_trace`, `build_real_store`'s last parameter `factories`.

**Line numbers** in §9.8, read at the final tree after D11 (and spans by `inspect.getsourcelines`):
`InventorySpec` `:304-344` (41 lines from 304), `extra_values` `:317`, `keywords()` `:319-329`,
`dependencies()` `:331-344`; `read_records` `:523-836` (314 lines), its keyword `:535`;
`_count_values` `:660-683`, the `values` call `:685-687`, the extra tables `:688-692`, the
problem `:673-682`; `Record` `:183-215` (33 lines), the field `:194`, `as_json` `:196-205`, the
fifth key `:203-204`, `canonical_json` `:207-208`, `identity` `:210-212`, `__hash__` `:214-215`;
the counts built `:803-806`; `_combine`'s comparison `:871-875`; `inventory_classes`
`:962-1015` (54 lines), the refusal `:990-994`, its docstring `:971-973`; `inventory_specs`
`:949-959`; `SQL/schema.py` `dependent_tables` `:359`, reading `inventory_specs` at `:398`;
`store_fingerprint.py`'s comment `:38-70`, the paragraph `:66-70`, `ENCODING_FORMAT = 1` `:71`;
`tests/client/factories.py` `TraceMark_factory` `:1328-1352`, the declaration `:1511`. My first
draft of §9.8 gave `:1325-1347` for the factory; `inspect` showed the span ran to `:1349`, and D9
then moved it by three lines; the row as committed reads `:1328-1352` and `:1511`, re-measured.

**The client vocabulary** (`datastorekit/tests/data/client_vocabulary.json`, 515 strings), by a
script that loads it and tests each name for equality, ignoring case, and lists any vocabulary
string longer than three characters contained in the name (`<scratch>/scripts/vocab_check.py`):

```
TraceMark: not in vocabulary; substrings: []
TraceNote: not in vocabulary; substrings: []
GadgetNote: not in vocabulary; substrings: []
mark_index: not in vocabulary; substrings: []
note_index: not in vocabulary; substrings: []
marks: not in vocabulary; substrings: []
TRACE_MARKS: not in vocabulary; substrings: []
EXTRA_VALUE_CLASSES: not in vocabulary; substrings: ['value']
extra_values: not in vocabulary; substrings: ['value']
extra_value_counts: not in vocabulary; substrings: ['value']
TraceMark_factory: not in vocabulary; substrings: []
_TraceNote_factory: not in vocabulary; substrings: []
_GadgetNote_factory: not in vocabulary; substrings: []
_count_values: not in vocabulary; substrings: ['value']
extra_counts: not in vocabulary; substrings: []
MARKED_TRACE: not in vocabulary; substrings: []
FORMAT_1_GOLDEN: not in vocabulary; substrings: []
FOUR_KEYS: not in vocabulary; substrings: ['keys']
undeclared: not in vocabulary; substrings: []
wider: not in vocabulary; substrings: []
refused: not in vocabulary; substrings: []
wider_store: not in vocabulary; substrings: []
_respecified: not in vocabulary; substrings: []
canonical_lines: not in vocabulary; substrings: []
by_label: not in vocabulary; substrings: ['label']
```

None is client vocabulary. The substrings are the generic words `value`, `keys` and `label`, which
the package already uses throughout (`value_count`, `values`); the guards pass.

### 4.6 Scope

`git status` before committing: modified `store_fingerprint.py`, `store_inventory.py`, the four
neutral-client files, `real_store_fixtures.py`, the four test modules, `docs/client-contract.md`
and the three records; new the witness, the golden, the test module and this log. `git diff --stat
c8570e8 --` the pool, `store_reader.py`, `SQL/schema.py`, `pyproject.toml`, `README.md`,
`PROVENANCE.md`, `docs/adoption`, `docs/extraction`, `docs/extraction-verification.md`, `.github`,
`CLAUDE.md`, `LICENSE`, `.gitignore` and the two kept data files: empty.

### 4.7 Ray's processes and the clients

`pgrep -fl 'gcs_server|raylet|ray::|default_worker\.py'`: nothing, at 21:51 and at 22:15;
`RAY_ADDRESS` unset both times. Tags: seven, `v0.1.0` … `v0.4.0`, unchanged.

| Client | start (21:51) | end (22:15) |
|---|---|---|
| SecondaryGWKit | `031bcb4f128bbb669be22a705fed92a65bb10a4a` (`handover-remedial`), clean | the same, clean |
| ChamPBH | `705553290b3f14651f7b42a504b5b6ebc94d3233` (`jordan-normalization`), clean | the same, clean |
| StochasticInstantons | `f5f395b50316a6aabb0309aea067aa94bfe35fdf` (`dk-and-rpk-migration`), clean | the same, clean |

Read only through `git -C <path> rev-parse | status | show`.

---

## 5. The deliberate-breakage record (§4.4)

Each diff is relative to the repository root, exactly as applied. Each was applied to its own copy
of the export `<scratch>/exp-final2` (whose `store_inventory.py` is the committed one, by `cmp`),
as `git apply --check`, `git apply`, `git apply -R --check`, all three passing; then, from the
copy's root at the high end, `python -m unittest datastorekit.tests.test_inventory_extra_values
datastorekit.tests.test_store_inventory datastorekit.tests.test_store_fingerprint
datastorekit.tests.test_neutral_client` (91 tests), the copy's own `datastorekit` imported. After
this log was written, each diff was extracted from it (`<scratch>/scripts/extract_diffs.py`),
found byte-identical to the patch applied, and checked again with `git apply --check`, then
applied and checked with `git apply -R --check`, against a fresh copy of `<scratch>/exp-final2`,
the tree this commit holds under `datastorekit/` and `docs/` (§5.10). A subtest failure is counted
once per subtest. A first round, on copies of `<scratch>/exp-01` (the tree before D9 and D11,
whose `store_inventory.py` differed only in D11's docstring line), gave the same failures, test
for test, but for (i)'s first form (D10).

### 5.1 (a) `as_json` emits `"extra_value_counts"` on every record

**§4.4 predicts:** tests 1 and 2, the JSON-safe test and the golden test to fail. **Result:** 68
failures. Test 1 (the format-1 golden differs); test 2, 33 subtests (every record of every class
but `Trace` has the fifth key); `test_records_are_json_safe`, the same 33;
`test_the_golden_fingerprint`. Every named test fails; nothing else does. The planner's and the
note's result.

```diff
--- a/datastorekit/store_inventory.py
+++ b/datastorekit/store_inventory.py
@@ -200,8 +200,7 @@
             "validated": self.validated,
             "value_count": self.value_count,
         }
-        if len(self.extra_value_counts) > 0:
-            out["extra_value_counts"] = dict(self.extra_value_counts)
+        out["extra_value_counts"] = dict(self.extra_value_counts)
         return out
 
     def canonical_json(self) -> str:
```

### 5.2 (b) a record's counts hold only the tables with rows for it (no 0)

**§4.4 predicts:** tests 2 and 3 to fail. **Result:** 10 failures. Test 2, 3 subtests (`{} !=
{'TraceMark': 0}`, the three Traces without marks); test 3, 3 subtests (`{} != {'TraceMark': 0,
'TraceNote': 0}`); `test_records_are_json_safe`, 3 subtests (those Traces lose the key); the golden
test. As correction 2.

```diff
--- a/datastorekit/store_inventory.py
+++ b/datastorekit/store_inventory.py
@@ -801,8 +801,9 @@
             ),
             value_count=counts.get(row.serial, 0) if values is not None else None,
             extra_value_counts={
-                extra_table: found.get(row.serial, 0)
+                extra_table: found[row.serial]
                 for extra_table, found in extra_counts.items()
+                if row.serial in found
             },
         )
         out.append(
```

### 5.3 (c) an extra table's orphans not reported

**§4.4 predicts:** test 4 to fail. **Result:** 1 error: test 4, `ValueError: not enough values to
unpack (expected 1, got 0)` at its one-problem unpacking. A failure of the test, as correction 2
says. Nothing else.

```diff
--- a/datastorekit/store_inventory.py
+++ b/datastorekit/store_inventory.py
@@ -686,10 +686,12 @@
     if values is not None:
         counts = _count_values(*values)
     extra = dict(extra_values or {})
+    reported = len(problems)
     extra_counts: Dict[str, Dict[int, int]] = {
         extra_table: _count_values(extra_table, extra[extra_table])
         for extra_table in sorted(extra)
     }
+    del problems[reported:]
 
     # the member rows of each set of parents, grouped by the row that owns them: one read of each
     # member table, never one per row
```

### 5.4 (d) every extra table counted from the `values` table

**§4.4 predicts:** tests 2 and 3 to fail. **Result:** 8 failures, 2 errors. Test 2, 3 subtests
(each Trace's `TraceMark` count is its step count: `{'TraceMark': 1}`, `3`, `4` for 0); test 3
(`{'TraceMark': 2, 'TraceNote': 2}`); tests 4 and 5 error (the `values` orphans reported twice, or
nothing diverging); test 6 (deleting a `TraceMark` row moves nothing: equal digests); the golden
test; `test_store_inventory`'s `test_an_orphan_value_row` (`2 != 1`: the `TraceStep` orphan
reported once per table counted) and `test_store_fingerprint`'s
`test_an_orphan_value_row_is_a_problem_entry_only` (`{'Trace': {'orphan-value': 2}}`). As
correction 2.

```diff
--- a/datastorekit/store_inventory.py
+++ b/datastorekit/store_inventory.py
@@ -687,7 +687,7 @@
         counts = _count_values(*values)
     extra = dict(extra_values or {})
     extra_counts: Dict[str, Dict[int, int]] = {
-        extra_table: _count_values(extra_table, extra[extra_table])
+        extra_table: _count_values(*values)
         for extra_table in sorted(extra)
     }
 
```

### 5.5 (e) `keywords()` omitting `extra_values`

**§4.4 predicts:** tests 2, 3 and 6 to fail. **Result:** 11 failures, 2 errors. Test 2, 4 subtests
(`{} != {'TraceMark': …}`); test 3; test 6 (equal digests); tests 4 and 5 error (no problem to
unpack); `test_records_are_json_safe`, 4 subtests (`Trace` loses the key); the golden test. As
correction 2.

```diff
--- a/datastorekit/store_inventory.py
+++ b/datastorekit/store_inventory.py
@@ -325,7 +325,6 @@
             "values": self.values,
             "validated": self.validated,
             "parent_sets": self.parent_sets,
-            "extra_values": self.extra_values,
         }
 
     def dependencies(self) -> Tuple[str, ...]:
```

### 5.6 (f) `as_json` never emitting the counts

**§4.4 predicts:** tests 5 and 6 and the golden test to fail. **Result:** 6 failures, 1 error. Test
5 errors (no divergence to unpack); test 6 (equal digests); the golden test;
`test_records_are_json_safe`, 4 subtests (`Trace` lacks the key). As correction 2.

```diff
--- a/datastorekit/store_inventory.py
+++ b/datastorekit/store_inventory.py
@@ -200,8 +200,6 @@
             "validated": self.validated,
             "value_count": self.value_count,
         }
-        if len(self.extra_value_counts) > 0:
-            out["extra_value_counts"] = dict(self.extra_value_counts)
         return out
 
     def canonical_json(self) -> str:
```

### 5.7 (g) the refusal removed

**§4.4 predicts:** test 7 to fail. **Result:** 1 failure: test 7, `AssertionError: ValueError not
raised`. Nothing else.

```diff
--- a/datastorekit/store_inventory.py
+++ b/datastorekit/store_inventory.py
@@ -987,11 +987,6 @@
                     f"inventory_classes(): {name}.{field_name} is a polymorphic parent whose "
                     f"type column {parent.type_column} is not one of {name}'s leaves"
                 )
-        if spec.values is not None and spec.values[0] in spec.extra_values:
-            raise ValueError(
-                f"inventory_classes(): {name} names {spec.values[0]} both as its value table "
-                f"and in its extra_values"
-            )
         depends[name] = tuple(d for d in spec.dependencies() if d != name)
         if name in spec.dependencies():
             raise ValueError(f"inventory_classes(): {name} references itself")
```

### 5.8 (h) the refusal moved into `InventorySpec.__post_init__`

**§4.4 predicts:** test 7 (as `inventory_specs` and `dependent_tables` raise) to fail. **Result:**
1 failure: test 7, at its first assertion: `"Trace\b.*\bTraceStep\b" does not match
"InventorySpec(): names TraceStep both as its value table and in its extra_values"`, raised from
`inventory_specs` inside `inventory_classes` (A4). Nothing else.

```diff
--- a/datastorekit/store_inventory.py
+++ b/datastorekit/store_inventory.py
@@ -315,6 +315,13 @@
     validated: Optional[str] = None
     parent_sets: Mapping[str, ParentSet] = field(default_factory=dict)
     extra_values: Mapping[str, str] = field(default_factory=dict)
+
+    def __post_init__(self):
+        if self.values is not None and self.values[0] in self.extra_values:
+            raise ValueError(
+                f"InventorySpec(): names {self.values[0]} both as its value table and in its "
+                f"extra_values"
+            )
 
     def keywords(self) -> Dict[str, Any]:
         """The spec as ``read_records``' keyword arguments."""
@@ -987,11 +994,6 @@
                     f"inventory_classes(): {name}.{field_name} is a polymorphic parent whose "
                     f"type column {parent.type_column} is not one of {name}'s leaves"
                 )
-        if spec.values is not None and spec.values[0] in spec.extra_values:
-            raise ValueError(
-                f"inventory_classes(): {name} names {spec.values[0]} both as its value table "
-                f"and in its extra_values"
-            )
         depends[name] = tuple(d for d in spec.dependencies() if d != name)
         if name in spec.dependencies():
             raise ValueError(f"inventory_classes(): {name} references itself")
```

### 5.9 (i) an extra table's rows selected and counted in Python rather than grouped in SQL

**§4.4 predicts:** the counted-never-listed test, through `TraceMark` in `VALUE_TABLES`, to fail.
**Result:** 1 failure: `test_value_tables_are_only_counted`, `AssertionError: 'count(*)' not found
in 'SELECT "TraceMark".trace_serial \nFROM "TraceMark"'`: through `TraceMark`. Nothing else (D10:
the recorded form keeps the orphan problem).

```diff
--- a/datastorekit/store_inventory.py
+++ b/datastorekit/store_inventory.py
@@ -686,8 +686,29 @@
     if values is not None:
         counts = _count_values(*values)
     extra = dict(extra_values or {})
+    def _count_in_python(value_table_name: str, parent_column: str) -> Dict[int, int]:
+        parent_col = tables[value_table_name].c[parent_column]
+        found: Dict[int, int] = {}
+        orphans: Dict[int, int] = {}
+        for (parent,) in conn.execute(sqla.select(parent_col)):
+            if parent in serials:
+                found[parent] = found.get(parent, 0) + 1
+            else:
+                orphans[parent] = orphans.get(parent, 0) + 1
+        if len(orphans) > 0:
+            problems.append(
+                _problem(
+                    "orphan-value",
+                    name,
+                    f"{sum(orphans.values())} {value_table_name} row(s) on shard #{shard} "
+                    f"name {len(orphans)} {name} row(s) that are not there; e.g. parent "
+                    f"serials {_examples(orphans)}",
+                )
+            )
+        return found
+
     extra_counts: Dict[str, Dict[int, int]] = {
-        extra_table: _count_values(extra_table, extra[extra_table])
+        extra_table: _count_in_python(extra_table, extra[extra_table])
         for extra_table in sorted(extra)
     }
 
```

### 5.10 The diffs as recorded

Each diff of §5.1–§5.9, extracted from this log, against a fresh copy of `<scratch>/exp-final2`;
each reversed after its check, and the copy's `store_inventory.py` then `cmp`-equal to the
committed one.

```
(a) git apply --check: ok; git apply -R --check (applied): ok
(b) git apply --check: ok; git apply -R --check (applied): ok
(c) git apply --check: ok; git apply -R --check (applied): ok
(d) git apply --check: ok; git apply -R --check (applied): ok
(e) git apply --check: ok; git apply -R --check (applied): ok
(f) git apply --check: ok; git apply -R --check (applied): ok
(g) git apply --check: ok; git apply -R --check (applied): ok
(h) git apply --check: ok; git apply -R --check (applied): ok
(i) git apply --check: ok; git apply -R --check (applied): ok
```

---

## 6. Observations not acted on

1. **`test_schema_builder.py`'s docstring** keeps its sentence "The current one is
   `schema_at_extraction-06.json` …", as §2.4 asks, and the new sentence follows it: "The current
   witness is now `schema_at_extra-values-01.json` …". A reader meets both; the second says it
   supersedes. Not an issue.
2. **`real_store_fixtures.py`'s module docstring** describes the full store as holding "value
   rows", which covers `TraceMark`; it does not name the table. Not an issue.
3. **`Record.__eq__`**, generated by the dataclass, now compares `extra_value_counts` too. Two
   records of a class that declares no extra table compare as before; nothing in the package or
   the clients compares records by `==` other than through `canonical_json` (README §0.1, check 2).
   Not an issue.
4. **The high end's `ResourceWarning`** comes from a different SQLAlchemy frame on each run (C4);
   it is the same unclosed `sqlite3.Connection`, at the baseline as after. Not an issue for this
   prompt.

## 7. Issues

None opened, none closed. `docs/OPEN_ISSUES.md` is unchanged at **4 open**.

## 8. State handed to the next prompt

- `HEAD` is this commit, on `main`, unpushed; `origin/main` is `38ebb9f`. No tag was made; seven
  tags, `v0.1.0` … `v0.4.0`. `pyproject.toml` is at `0.4.0`.
- After 01 (README §4): `InventorySpec.extra_values` and `Record.extra_value_counts`;
  `ENCODING_FORMAT` 1 and its paragraph; the neutral client's `TraceMark`; the witness
  `schema_at_extra-values-01.json` (`971ec253…`); the golden
  `store_fingerprint-neutral-2-encoding-1.json` (`524cefd4…`); contract §9.8.
- The suite: **538**, `OK`, at both ends. `black --check datastorekit docs`: 79 files. The port
  check: unchanged.
- For 02: the release's files (`pyproject.toml`, `README.md`, `PROVENANCE.md`, the adoption
  addenda). SI's addendum: `extra_values={"GradientCoupledInstantonValue": "instanton_serial"}`,
  read back as `record.extra_value_counts["GradientCoupledInstantonValue"]` (README §0.2, point 1);
  SI's fingerprints, once it declares the table, are its own `fingerprint_format`'s concern.
