# Prompt 01 — a spec counts more than one value table

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

*Written 2026-10-21 against `38ebb9f`, whose `datastorekit/` is `c8570e8`'s (`v0.4.0`).*

**Gate:**
- U1, U3 and U4 are taken (README §6.2): by the user on 2026-10-21, as recommended. U2 is the
  user's ruling of the same day.
- `git status` is clean in this repository, and `origin/main` is an ancestor of `main`.
- `datastorekit/` is `c8570e8`'s: `git diff --stat c8570e8 HEAD -- datastorekit` is empty.
- The suite gives `Ran 530 tests … OK` in `venv/`.

**Closes:** nothing on a board. **Opens:** only what the work finds.

**Recommended model:** **Opus**.
- The code is small (about 40 lines in `store_inventory.py`), and the risk is in what must not
  change: every record of every class that declares no extra table, byte for byte, and so every
  fingerprint a client holds. Test 1 and the format-1 golden are the proof, and must fail for the
  right reason when the property is broken (§4.4).
- The neutral client's change must reproduce the planner's witness and golden exactly (§1.1), so
  §2.3 is to be followed to the column.
- The contract's §9.8 states how `ENCODING_FORMAT`'s item 1 is read, for the next editor.

**Read first:**

1. [`README.md`](README.md): all of it, §0.1, §0.2 and §6.2 especially.
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`.
3. The brief:
   `/Users/ds283/Documents/Code/StochasticInstantons/.prompts/dk-and-rpk-migration/datastorekit-second-value-table-brief.md`.
   It is evidence, read as text. Do not act on it beyond this prompt; README §0.1 re-measured it,
   and §0.2 records where this campaign departs from it.
4. `datastorekit/store_inventory.py`: its docstring (`:1-115`); `Record` (`:178-203`);
   `InventorySpec` (`:293-333`); `read_records` (`:508-803`), the value counting (`:641-667`) and
   the record built (`:763-774`); `_combine` (`:826-913`); `inventory_specs` and
   `inventory_classes` (`:916-976`).
5. `datastorekit/store_fingerprint.py:1-65`: the docstring and the comment beside
   `ENCODING_FORMAT`.
6. The neutral client: `tests/client/registry.py` (its docstring's roles table, `:15-56`; the
   registry, `:74-98`; `drop_groups`, `:149-162`); `tests/client/factories.py` (`TraceStep_factory`,
   `:1298-1322`; `Trace_factory`, `:1325-1473`); `tests/client/objects.py` (`Trace`, `:207-232`);
   `tests/client/build.py` (`TRACES`, `:61-66`; `write_every_class`'s traces, `:325-330`;
   `make_trace`, `:411-424`).
7. `datastorekit/tests/real_store_fixtures.py`: its docstring; `_write_shard` and
   `build_real_store` (`:233-329`); `_full_shard0` (`:527-612`); `fill_required` and `full_rows`
   (`:676-704`); `build_full_store` (`:772-831`).
8. The tests this prompt amends: `test_neutral_client.py` (its docstring;
   `test_every_declaration_field_is_in_use`, `:308-`); `test_store_inventory.py` (`VALUE_TABLES`,
   `:77-80`; `test_records_are_json_safe`, `:236-247`; the counted-never-listed test, `:615-638`);
   `test_store_fingerprint.py` (`:55-65`; `test_another_format_moves_only_the_overall_digest`,
   `:650-655`); `test_schema_builder.py` (its docstring, `:1-21`; `WITNESS`, `:44`);
   `schema_description.py` (its docstring and `__main__`).
9. `docs/client-contract.md`: its head (`:1-61`), §4 (`:143-187`) and §9.7 (`:372-`), for the form
   a §9 subsection takes and the rows §9.8 supersedes in part.
10. `fingerprint` prompt 01's log (`../fingerprint/logs/01-the-fingerprint-moves-into-the-package.md`):
    how both ends, a golden, and the breakage record were recorded last time.

Line numbers are at `38ebb9f`, measured on 2026-10-21.

---

## 1. What is wanted

After this prompt, **a factory's spec can name further value tables**, and the inventory counts
each as it counts `values`:
- `InventorySpec(…, extra_values={"<table>": "<its column naming this class's serial>", …})`;
- each record of such a class carries `extra_value_counts`, every declared table → its count, 0
  where none, and its `as_json` has a fifth key, `"extra_value_counts"`;
- a record of any other class is what it is today, byte for byte, and so is its fingerprint;
- an extra table's orphan rows are an `orphan-value` problem; a replicated class whose extra count
  differs between shards is a `replicated-divergence`;
- `ENCODING_FORMAT` is 1, and the comment beside it says why this is not a bump.

The neutral client declares the field, its format is 2 with a new golden, and the format-1 golden
is reproduced by a spec that does not declare it.

**Nothing else in the package changes**: no message, refusal or exception of the pool's, and
nothing the pool writes or reads. `pyproject.toml` stays at `0.4.0`: 02 releases.

### 1.1 What the planner measured

README §0.1 holds the measurements. The ones this prompt rests on, from a prototype of U1–U4 as
recommended, in a scratch export of `38ebb9f`:
- the suite gave `Ran 538 tests … OK` at both ends (530 plus the 8 tests of §2.6), with 0 and 4
  `ResourceWarning` lines;
- the witness of §2.4, captured in `venv/`: SHA-256
  `971ec253ce78d5f0f7cfeccf13dd0a3b94fc3f5bc9a57b2eadee7b7f2c07d196`, its diff from
  `schema_at_extraction-06.json` 117 lines, all additions, all `TraceMark`;
- the golden of §2.5: digest `524cefd41ab593f73abe0610558d8444c64f9514c4d1edb5041591737161d14a`,
  the same at both ends, file SHA-256
  `848fe4c90bd622bafda061d6e59cf780308b8a7cb6044203f18da2fa43ba9fb8`; against the format-1 golden
  (digest `7656b600…`), only `Trace`'s class entry differs;
- the format-1 golden reproduced, every field but `taken`, through a registry whose `Trace` spec
  omits `extra_values`;
- the guards, the port check and `black --check datastorekit docs` (79 files) pass.

---

## 2. What to change

### 2.1 `datastorekit/store_inventory.py` (U1)

1. **`Record`** gains a last field, `extra_value_counts: Mapping[str, int] =
   field(default_factory=dict)`, with a comment saying what it holds and that it is empty, and then
   not in `as_json`, where the class declares no extra table. **`as_json`** builds today's four
   keys exactly as now, then adds `"extra_value_counts": dict(self.extra_value_counts)` only when
   the mapping is not empty. `canonical_json`, `identity` and `__hash__` are not changed.
2. **`InventorySpec`** gains a last field, `extra_values: Mapping[str, str] =
   field(default_factory=dict)`, and `keywords()` a last entry `"extra_values": self.extra_values`.
   `dependencies()` is not changed. Its docstring is not changed beyond what is needed to mention
   the field.
3. **`read_records`** gains a last keyword, `extra_values: Optional[Mapping[str, str]] = None`, and
   a line in its docstring's list after `values`'. The block at `:641-667` becomes **one inner
   function** that, for a `(value table, parent column)`, runs today's `GROUP BY`, returns the
   counts of the serials on this shard, and appends today's `orphan-value` problem, in today's words,
   for the rest. It is called for `values` when it is not `None`, and then for each extra table in
   **sorted** table order. Each record gets `extra_value_counts` = `{table: counts.get(serial, 0)}`
   for every declared table (an empty dict when none is declared). Nothing else of the function
   changes.
4. **`inventory_classes`** gains one refusal, beside its others and in their form: a spec whose
   `values` table is also a key of its `extra_values` raises `ValueError`
   `"inventory_classes(): <class> names <table> both as its value table and in its extra_values"`.
   Add it to the docstring's list of refusals. **No refusal is added to `InventorySpec`,
   `inventory_specs` or `read_records`** (README §0.2, point 3).
5. **The module docstring**: the record's bullets gain `extra_value_counts` (what it holds; absent
   from `as_json` where the class declares no extra table); the sentence after them ("A
   computed-values field can be added … beside these four …") still holds and is not rewritten;
   the "Who defines identity" paragraph names the further value tables; the "Shards" paragraph's
   "compared on key, tags, validated flag and value count" names the extra counts too;
   `orphan-value`'s line covers an extra table's rows.

### 2.2 `datastorekit/store_fingerprint.py` (U2)

After the comment's last sentence ("A change to a client's specs or registry is that client's
``fingerprint_format``, never ENCODING_FORMAT."), a blank comment line and one paragraph:

> Item 1 is read by the rule above it. A field added to ``Record.as_json`` that a record carries
> only where its class's spec declares what fills it (``extra_value_counts``, from
> ``InventorySpec.extra_values``) is not a bump: a store read with the same specs gives the same
> records. A client whose spec comes to declare it changes its own fingerprints, which is its
> ``fingerprint_format``.

`ENCODING_FORMAT` stays `1`. Nothing else of the file changes.

### 2.3 The neutral client (U3)

Exactly as follows, so that §2.4's witness and §2.5's golden are the planner's:
1. **`factories.py`**: `TraceMark_factory(SQLAFactoryBase)`, after `TraceStep_factory` and before
   `Trace_factory`. Its docstring: a second child table of the sharded `Trace`, one row per mark,
   written only for a Trace that carries marks: a further value table its `inventory_spec` counts
   (`extra_values`). `register()` returns `{"version": False, "timestamp": False, "columns":
   [sqla.Column("trace_serial", sqla.Integer, sqla.ForeignKey("Trace.serial"), index=True,
   nullable=False), sqla.Column("mark_index", sqla.Integer, nullable=False)]}`. `build` raises
   `NotImplementedError("TraceMark rows are written by Trace's store")`, as `TraceStep_factory`'s
   does.
2. **`Trace_factory`**: `store` writes, after the steps, one `TraceMark` row per entry of
   `obj.marks`, `{"trace_serial": store_id, "mark_index": index}`, through `inserters["TraceMark"]`.
   `inventory_spec` gains `extra_values={"TraceMark": "trace_serial"}`, after `validated`. Its
   docstring mentions the marks.
3. **`objects.py`**: `Trace.__init__` gains a last keyword `marks: Sequence[int] = ()`, kept as
   `self.marks = list(marks)`; its docstring mentions it.
4. **`build.py`**: `TRACE_MARKS = {"trace-one": (0, 1)}`, beside `TRACES`, with a comment;
   `make_trace` gains a last keyword `marks: Sequence[int] = ()`, passed to `Trace`;
   `write_every_class` passes `marks=TRACE_MARKS.get(label, ())`.
5. **`registry.py`**: `"TraceMark": _f.TraceMark_factory` after `"TraceStep"`; `"TraceMark"` after
   `"TraceStep"` in the `traces` drop group; the roles table's `Trace` row names its extra value
   table, and the `Trace_tags`, `TraceStep` row becomes a row naming `TraceMark` too (kind
   "neither"), saying which prompt added it.
6. **`real_store_fixtures.py`**: in `_full_shard0`, after `Trace 4`'s `TraceStep` rows,
   `{"TraceMark": [{"serial": 1, "trace_serial": 3, "mark_index": 0}, {"serial": 2,
   "trace_serial": 3, "mark_index": 1}]}`. `build_real_store` and `_write_shard` gain a last
   keyword `factories: Optional[Mapping[str, object]] = None`, the neutral registry when `None`,
   from which `_write_shard` builds its schema; the docstring says so. `build_full_store`, its
   empty-shard cache and `fill_required` are not changed.

### 2.4 The schema witness (U3)

Capture `datastorekit/tests/data/schema_at_extra-values-01.json` with `schema_description.py`'s
`__main__` in `venv/`, from your tree, as its docstring says. Its SHA-256 must be the planner's
(§1.1); if not, stop. Repoint `WITNESS` in `test_schema_builder.py` at it, and add to that module's
docstring a sentence saying the current witness is this one, captured by `extra-values` prompt 01,
differing from `schema_at_extraction-06.json` only by the `TraceMark` table; the sentences about
the earlier witnesses stay as written. `schema_at_extraction-06.json` is not changed. The log
carries the diff between the two witnesses.

### 2.5 The neutral client's format and its golden (U3)

`NEUTRAL_FORMAT = 2` in `test_store_fingerprint.py`; its comment is unchanged.
`datastorekit/tests/data/store_fingerprint-neutral-2-encoding-1.json` is `fingerprint_of` of
`read_inventory(build_full_store(<tmp>).primary, factories)` with the neutral registry, at
`fingerprint_format=2`, `taken` `None`, written with `json.dumps(…, indent=2, sort_keys=True)` and a
final newline by a script you keep in the log, not in the repository. Its digest and its file's
SHA-256 must be the planner's (§1.1); if not, stop. `store_fingerprint-neutral-1-encoding-1.json` is
not changed (README §5 rule 11). In `test_another_format_moves_only_the_overall_digest`, the
"another format" `2` (`:651`, `:652`) becomes `NEUTRAL_FORMAT + 1`.

### 2.6 The tests (U4)

**Amended literals**, each naming what changed, with no assertion added or removed (the port check
compares the assertion calls of `test_store_inventory`):
- `test_every_declaration_field_is_in_use`: the `InventorySpec` field list gains
  `"extra_values"`, last;
- `test_store_inventory.py`: `VALUE_TABLES` gains `"TraceMark"`; `test_records_are_json_safe`'s
  key set is the four keys, plus `"extra_value_counts"` for a class of a module-level tuple
  `EXTRA_VALUE_CLASSES = ("Trace",)`, with a comment;
- `test_neutral_client.py`'s docstring, if what it enumerates changes.

**A new module**, `datastorekit/tests/test_inventory_extra_values.py`. Its docstring numbers its
tests and says that no test starts Ray or constructs a `ShardedPool`, and every store is in a
temporary directory. Module-level helpers, none of which asserts:
- `undeclared()`: the neutral registry with `Trace`'s factory replaced by a subclass whose
  `inventory_spec` is the neutral one's with `extra_values={}` (built from `spec.keywords()`);
- `wider()`: the neutral registry with two child tables added, `TraceNote` under `Trace`
  (`trace_serial`) and `GadgetNote` under `Gadget` (`gadget_serial`), each with one more integer
  column, and `Trace` and `Gadget` replaced by subclasses whose specs declare
  `{"TraceMark": "trace_serial", "TraceNote": "trace_serial"}` and `{"GadgetNote":
  "gadget_serial"}`;
- a store of `wider()`: `build_real_store(…, factories=wider())` with `fill_required` of
  `full_rows()`'s rows plus the rows a test adds;
- `FORMAT_1_GOLDEN`, the path of `store_fingerprint-neutral-1-encoding-<ENCODING_FORMAT>.json`.

Tests, README §6.2 U4:
1. **Compatibility.** `build_full_store()` read through `undeclared()` gives, at
   `fingerprint_format=1`, a fingerprint equal to `FORMAT_1_GOLDEN`'s in every field but `taken`.
   Read through the neutral registry and through `undeclared()`, every class but `Trace` has equal
   canonical lines.
2. **Counts.** On `build_full_store()` through the neutral registry: Trace 3's record (its
   `trace_label` from the fixture) has `extra_value_counts == {"TraceMark": 2}`, each other Trace's
   `{"TraceMark": 0}`, and each Trace's `value_count` is what it is through `undeclared()`; every
   record of every other class has `extra_value_counts == {}` and `as_json` keys exactly
   `{"key", "tags", "validated", "value_count"}`; no problems.
3. **Two tables.** Through `wider()`, with one `TraceNote` row under Trace 3: Trace 3's counts are
   `{"TraceMark": 2, "TraceNote": 1}`, and a Trace with neither `{"TraceMark": 0, "TraceNote": 0}`;
   no problems.
4. **Orphans.** Through `wider()`, a `TraceNote` row on shard 1 naming a serial no Trace has gives
   exactly one problem of `Trace`, starting `orphan-value`, naming `TraceNote` and `shard #1`; the
   fingerprint's `problems` is `{"Trace": {"orphan-value": 1}}`.
5. **Replicated divergence.** Through `wider()`, a `GadgetNote` row on shard 0 alone gives `Gadget`
   exactly one problem, `replicated-divergence`.
6. **The fingerprint sees it.** `build_full_store()` and the same with one `TraceMark` row deleted
   (`extra_sql`), at `NEUTRAL_FORMAT`: the overall digests differ, every class entry but `Trace`'s
   is equal, and `compare_fingerprints` names `Trace` alone.
7. **The refusal.** A registry whose `Trace` spec declares `extra_values={"TraceStep":
   "trace_serial"}`: `inventory_classes` raises `ValueError` whose message names `Trace` and
   `TraceStep`; `inventory_specs` and `dependent_tables(["Trace"], …)` of the same registry do not
   raise.
8. **`dependent_tables`.** For drops of `["Trace"]`, `["TraceMark"]` and `["keypoint"]`, the
   neutral registry and `undeclared()` give equal answers, and a drop of `["Trace"]` takes
   `TraceMark`.

The test is not a port: it is not added to `docs/extraction/compare_ported_tests.py`'s `PORTED`.

### 2.7 `docs/client-contract.md`

- **At the head**, after the §9.7 line: *"§9.8 is measured from the package at `extra-values`
  prompt 01's tree, and its line numbers are that tree's."*
- **A §9.8, "`extra-values` prompt 01"**, after §9.7, in §9's form. Its preamble: one change
  (`prompts/extra-values/README.md`, decisions U1–U3, the user's request and ruling); nothing the
  pool writes or reads changes, and no message, refusal or exception of the pool's; a spec that
  declares no extra table gives the records it gave. Rows:
  - **`InventorySpec.extra_values`**. Supersedes §4's "**6** fields" in part (now 7) and adds to its
    table: default `{}`; each table → its column, counted as `values` is, one `GROUP BY` per table
    per shard; orphans an `orphan-value` problem; a missing table or column a `KeyError` when read;
    neutral client `Trace` (`TraceMark`). Pinned by tests 2–4, 6.
  - **`Record.extra_value_counts` and `as_json`**. Supersedes none, or the line where the contract
    states `Record`'s fields, if it does (say which in the log): what it holds; `as_json`'s fifth
    key only when it is not empty; `identity` unchanged; the replicated comparison covering it.
    Pinned by tests 1, 2, 5.
  - **The refusal** in `inventory_classes`, and that no spec's construction refuses. Pinned by
    test 7.
  - **`ENCODING_FORMAT`'s item 1**. Supersedes §9.7's `ENCODING_FORMAT` row in that part: §2.2's
    paragraph, in the same words; `ENCODING_FORMAT` 1. Pinned by test 1 and the format-1 golden.
- **No marker** is set on any row of §1–§9.7. **Nothing in §1–§9.7 changes**: the diff of the file
  is `+` lines only.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **The compatibility property.** A record of a class that declares no extra table must be
   today's. Test 1 against the format-1 golden is its proof; the golden test at format 2 is not.
2. **The witness and the golden** are reproductions, not outputs (§2.4, §2.5): a difference from
   the planner's is a stop, not a new file.
3. **The pool.** `dependent_tables` reads `inventory_specs`; a refusal there, or in a spec's
   construction, would be a new refusal of the pool's drop. Test 7 checks it.
4. **The port check.** `test_store_inventory`'s assertion calls are unchanged; only literals move.
5. **The guards** (`test_layer_is_generic`, `test_prose_names_no_source`) scan the changed
   docstrings and comments. `TraceMark`, `TraceNote` and `GadgetNote` must not be client vocabulary.
6. **Additive documents.** `git diff` of `docs/client-contract.md` shows `+` lines only;
   `schema_at_extraction-06.json` and `store_fingerprint-neutral-1-encoding-1.json` are unchanged.
7. **No Ray.** No test or script of this prompt starts Ray.
8. **Offline only.** Every venv is made `--offline` (README §0.1 says how the high end was made).
   A pin that does not resolve offline is a stop.
9. **The clients.** None is written, run, imported or opened. Record each one's `HEAD` and
   `git status --short` at the start and the end.

---

## 4. Verification

1. **The suite.** `Ran 530 tests … OK` in `venv/` before; after, 538 (530 plus §2.6's eight), `OK`,
   at both ends: `venv/`, and a fresh offline scratch venv (Python 3.13.16, `ray==2.55.1`,
   `sqlalchemy==2.0.46`, `setuptools`) with a `git archive` of your tree installed editable
   (`--no-deps --no-build-isolation`), `datastorekit.__file__` printed under the export. Record
   the `ResourceWarning` lines at each end (0 in `venv/`; 0 or 4 at the high end is timing). A
   different count is explained in the log, test by test.
2. **The checks.** `docs/extraction/compare_ported_tests.py` exits 0 with "20 module(s) … 1 test(s)
   declared not ported"; `./venv/bin/black --check datastorekit docs` passes, at 79 files (78 at
   `38ebb9f` plus the new module).
3. **The reproductions** (§2.4, §2.5): the witness's SHA-256, the golden's digest at both ends, the
   golden file's SHA-256.
4. **The breakage record.** Each a diff exactly as applied in a scratch export, checked with
   `git apply --check` and `-R --check`, with what failed. None is committed.
   - **(a)** `as_json` emits `"extra_value_counts"` on every record: tests 1 and 2, the JSON-safe
     test and the golden test fail (measured by the planner).
   - **(b)** a record's counts hold only the tables with rows for it (no 0): tests 2 and 3 fail.
   - **(c)** an extra table's orphans not reported: test 4 fails.
   - **(d)** every extra table counted from the `values` table: tests 2 and 3 fail.
   - **(e)** `keywords()` omitting `extra_values`: tests 2, 3 and 6 fail.
   - **(f)** `as_json` never emitting the counts: tests 5 and 6 and the golden test fail.
   - **(g)** the refusal removed: test 7 fails.
   - **(h)** the refusal moved into `InventorySpec.__post_init__`: test 7 fails (`inventory_specs`
     and `dependent_tables` raise).
   - **(i)** an extra table's rows selected and counted in Python rather than grouped in SQL: the
     counted-never-listed test fails, through `TraceMark` in `VALUE_TABLES`.
5. **The documents.** Every name §2.7 cites exists at your tree: fields and functions by importing
   them in `venv/`, line numbers by reading them. List each in the log.
6. **The clients**, at the start and the end, unchanged (hazard 9).

---

## 5. Acceptance

1. §2.1–§2.7 are done, and every file under `datastorekit/` that §7 does not list is unchanged.
2. §4.1–§4.6 hold.
3. **The records**, in the same commit:
   - the log `logs/01-a-spec-counts-more-than-one-value-table.md`, per README §5.1, with the
     witness diff, the golden's script, the breakage diffs, each name checked, and the clients at
     the start and the end;
   - this board: §1's row for 01, the header, and the decisions table if any changed;
   - this campaign's README: its header and §2's row for 01;
   - `docs/OPEN_ISSUES.md`: unchanged at **4**, unless the work opens an issue;
   - `prompts/INDEX.md`: the campaign's line.

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count falls, in any venv.
- The witness's SHA-256, or the golden's digest or file SHA-256, is not the planner's (§1.1).
- Test 1 fails after the change, or passes under breakage (a).
- A test of §2.6 passes under a breakage of §4.4 that it is named to catch, or fails after the
  change for a reason other than a bug in the test.
- Any change to the pool, to `dependencies()`, or to any message, refusal or exception but §2.1
  item 4's would be needed.
- An amendment of §2.6 would add or remove an assertion call of `test_store_inventory`, or the
  port check fails.
- The guards fail and cannot be satisfied by rewording.
- A document cannot say what it must without rewriting a line already in it.
- Anything would start Ray, push, make or move a tag, download, or write, run, import or open
  anything of a client.

---

## 7. What this prompt changes, and what it does not

- **Files it changes:**
  - `datastorekit/store_inventory.py` and `datastorekit/store_fingerprint.py` (its comment only);
  - the neutral client: `datastorekit/tests/client/factories.py`, `objects.py`, `build.py`,
    `registry.py`; `datastorekit/tests/real_store_fixtures.py`;
  - the new `datastorekit/tests/data/schema_at_extra-values-01.json` and
    `datastorekit/tests/data/store_fingerprint-neutral-2-encoding-1.json`;
  - the new `datastorekit/tests/test_inventory_extra_values.py`, and the amendments of §2.4–§2.6 to
    `test_neutral_client.py`, `test_store_inventory.py`, `test_store_fingerprint.py` and
    `test_schema_builder.py`;
  - `docs/client-contract.md`, by addition only;
  - the log, this board, this campaign's README, `docs/OPEN_ISSUES.md` if an issue is opened, and
    `prompts/INDEX.md`.
- **It changes nothing else:** not the pool, `store_reader.py`, `SQL/schema.py`, `pyproject.toml`,
  `README.md`, `PROVENANCE.md`, `docs/adoption/`, `docs/extraction/`, the workflow, `CLAUDE.md`,
  `LICENSE` or `.gitignore`. 02 changes the release's files.
- **It touches no client repository.**
- **It makes no tag and pushes nothing.**

---

## 8. After 01

The orchestrator reviews 01 against its commit, and replays §4.3 and §4.4. 02, the release, is then
written against the tree 01 leaves, and carries the adoption addenda: SI's saying what it does
(README §6.2, U5), ChamPBH's and SGK's that nothing changes for them.
