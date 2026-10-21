# Campaign — extra-values

**Written:** 2026-10-21 by Claude Opus 5.5, at the user's request, from a brief written in a
StochasticInstantons session (§0). **Prompt 01 is written** (2026-10-21). U2 is the user's ruling
of 2026-10-21; the user took U1 and U3–U5 as recommended the same day, and 01 is ready to be
dispatched. Prompt 02, the release, is written after 01 has landed and been reviewed, against the
tree 01 leaves. **Prompt 01 landed** 2026-10-21 (its
[log](logs/01-a-spec-counts-more-than-one-value-table.md)), `5475cef`, and was reviewed the same day;
CI passed on it at both ends. **Prompt 02 is written** (2026-10-21), after U5 was amended by the
user the same day (§0.3).

## 0. Why this campaign exists

**The user's request (2026-10-21).** The `fingerprint` campaign left "a second value table per
spec" out of `v0.4.0`, "until SI's prompt 10 settles it and the user asks"
([`../fingerprint/README.md`](../fingerprint/README.md) §1, out of scope). SI's prompt 10 has
settled it, and the user has asked. The brief that carries the request is
`/Users/ds283/Documents/Code/StochasticInstantons/.prompts/dk-and-rpk-migration/datastorekit-second-value-table-brief.md`,
written 2026-10-21 at DatastoreKit `38ebb9f` and SI `d0ce59c`, committed in SI as `f5f395b`. It is
evidence, not a specification (`CLAUDE.md` rule 7): §0.1 re-measures it here, and §0.2 records
where this campaign departs from it. It leaves the campaign's name, its decisions, its shape, the
field's name and the version to this repository.

**What is missing.** `InventorySpec.values` is one `(value table, its column naming this class's
serial)` pair, or `None` (`store_inventory.py:301`). `read_records` counts it with one `GROUP BY`
per shard (`:641-667`) into `Record.value_count`, which is in every record's canonical line and so
in the fingerprint. A class that owns **two** value tables can have only one of them counted. SI's
`GradientCoupledInstanton` owns two: `GradientCoupledInstantonProfile`, written for every row,
which SI gave the slot, and `GradientCoupledInstantonValue`, written only when full values are
stored, which SI's coverage test therefore excludes (SI `tests/test_inventory_specs.py:208-213`).
A store whose rows of the second table were lost fingerprints the same as one that has them.

**The change.**
1. **`InventorySpec.extra_values`**: a mapping, each further value table to its column naming this
   class's serial, defaulted empty, read exactly as `values` is (U1).
2. **`Record.extra_value_counts`**: per declared table, the number of its rows naming the record's
   row (0 where none), defaulted empty. **`Record.as_json` carries it only where it is not
   empty**, so a record of a class that declares no extra table is what it is today, byte for byte
   (U1).
3. **`ENCODING_FORMAT` stays 1**, and the comment that states its rule says why (U2, the user's
   ruling).
4. **The neutral client declares the field**, as it declares every other field, with its format
   and golden moved on in the way its rule prescribes (U3).
5. **A release** carrying them, with an addendum for each client (prompt 02, U5).

**The constraint: no recorded fingerprint moves.** SGK and ChamPBH have recorded fingerprints;
neither declares a second value table (§0.1). A store read with an unchanged spec must give
records whose `canonical_json` is unchanged, and so an unchanged fingerprint at an unchanged
`ENCODING_FORMAT`. The neutral store's golden at format 1 is the test of it (U3, U4 test 1).

### 0.1 Measurements taken by the planner (2026-10-21)

All at `38ebb9f`, whose `datastorekit/` is `v0.4.0`'s (`c8570e8`). `git status` is clean and
`origin/main` (`38ebb9f`) is an ancestor of `main`. The suite gives `Ran 530 tests … OK` in
`venv/` (Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39, SQLite 3.53.4). Nothing was committed.

**The brief's five checks (its §3) hold.**
1. **`values` is read in one place.** Outside `tests/`, `InventorySpec.values` is read only by
   `keywords()` (`store_inventory.py:311`) and so by `read_records` (`:642-667`). `store_reader`
   reads no spec. `SQL/schema.dependent_tables` (`schema.py:359-`) reads `inventory_specs` and only
   their `dependencies()`, which name parents, parent-set members and the tag table; its docstring
   says a table that belongs to another "names its owner by foreign key and need declare no
   `inventory_spec` of its own, so only the foreign key shows it". `ShardedPool` reaches specs only
   through `dependent_tables` (`ShardedPool.py:835`).
2. **Who reads a `Record`.** In the package: `canonical_json` and `identity` (`:195-200`),
   `_combine`'s replicated comparison on `canonical_json` (`:831-870`) and its duplicate check on
   `identity` (`:873-891`), `store_fingerprint.fingerprint_of` and `listing_lines` (canonical lines,
   `store_fingerprint.py:123`). The clients, read through `git`: each `tools/inventory_report.py`
   reads `record.value_count` by attribute, and every `Record(...)` any of them or this suite builds
   passes keywords (`test_inventory_declarations.py:303-346`; SGK
   `tools/tests/test_inventory_report_labels.py:89`; SI `tests/test_inventory_report.py:66-67`).
   A new field, last and defaulted, breaks none of them.
3. **The golden** (`tests/data/store_fingerprint-neutral-1-encoding-1.json`, digest
   `7656b600965b5911a5046e7c0ebcd4dddce1c8ad277243d211b548487f22d304`) pins the neutral store at
   format 1.
4. **`ENCODING_FORMAT`'s rule** (`store_fingerprint.py:38-64`): its opening sentence is not met by
   a field omitted when empty; its item 1 ("`Record.as_json`'s fields") reads, to the letter, as
   met; and its last sentence but one ("A change that the neutral golden does not see is still a
   bump if it is in the list") gives the literal reading more weight than the brief says. Settled
   by U2.
5. **No Ray.** `read_inventory` opens the store with `open_read_only`; nothing crosses an actor.

**The clients**, read through `git` only: SI `f5f395b`, ChamPBH `7055532`, SGK `031bcb4`, each
clean, each pinned to `v0.4.0` (`requirements.txt`). SI's `GradientCoupledInstanton` spec is as the
brief says at `e2c7b22` (`values=("GradientCoupledInstantonProfile", "parent_serial")`), and its
coverage test asserts 30 entries, 24 specs, 5 read through an owner and 1 excluded. ChamPBH's
coverage test excludes nothing (`EXCLUDED = {}`) and its three value specs each name one table
(`AdiabaticHistory.py`, `BBNData.py`, `ScalarHistory.py`); SGK's seven each name one (the brief's
list, confirmed).

**`test_every_declaration_field_is_in_use`** (`tests/test_neutral_client.py:308-`, written with the
neutral client at `e988e69`) lists `InventorySpec`'s fields as a literal, "so that a field added to
a declaration fails here until it is used", and requires every field to differ from its default in
some spec **of the neutral registry**. So the field cannot be tested on a separate registry alone,
as the brief advises (§0.2, point 2).

**A prototype**, in a scratch export of `38ebb9f`, of U1–U4 as recommended:
- `store_inventory.py` +32 −8 lines: the two fields, `as_json`'s conditional key, the counting
  `GROUP BY` and its `orphan-value` problem made one inner function used for `values` and each
  extra table, the refusal in `inventory_classes`; `store_fingerprint.py` +6, the comment;
- the neutral client: a `TraceMark` table under `Trace` (+32 in `factories.py`, +2 in
  `registry.py`, +2 in `objects.py`, +17 in `build.py`), Trace's spec declaring it, `trace-one`
  carrying two marks, and the full store two `TraceMark` rows under Trace 3 on shard 0
  (`real_store_fixtures.py` +6, with `build_real_store` taking a `factories` argument, +5);
- a new witness `schema_at_extra-values-01.json` (SHA-256 `971ec253…c07d196`): its diff from
  `schema_at_extraction-06.json` is 117 lines, every one an addition, all of them `TraceMark`;
- `NEUTRAL_FORMAT` 2 and a new golden `store_fingerprint-neutral-2-encoding-1.json`: digest
  `524cefd41ab593f73abe0610558d8444c64f9514c4d1edb5041591737161d14a`, the same at both ends; against
  the format-1 golden, only `Trace`'s class entry differs;
- the format-1 golden reproduced, every field but `taken`, by the full store read through the
  neutral registry with Trace's spec less `extra_values` (the `TraceMark` table and its rows still
  in the store);
- a test module of 8 tests (U4, tests 1–8) and amended literals: the field list
  (`test_neutral_client.py`), the JSON-safe key set (`test_store_inventory.py:243`, by class),
  `NEUTRAL_FORMAT` and a test's hard-coded "another format" `2`, which became `NEUTRAL_FORMAT + 1`
  (`test_store_fingerprint.py:57`, `:651-652`), `WITNESS` (`test_schema_builder.py:44`), and
  `VALUE_TABLES` gaining `TraceMark` (`test_store_inventory.py:77-80`; with it, that module
  passes and the port check is unchanged).

Results: the suite gives `Ran 538 tests … OK` at both ends, `venv/` and an offline scratch venv
(Python 3.13.16, Ray 2.55.1, SQLAlchemy 2.0.46, SQLite 3.53.4), with 0 and 4 `ResourceWarning`
lines (`actor-names` log 01 correction 8 treats 4 at the high end as timing). The guards pass;
the port check gives "20 module(s) … 1 test(s) declared not ported"; `black --check datastorekit
docs` passes at 79 files. A mutation that always emits the new key fails the compatibility test,
the JSON-safe test (every class but Trace) and the golden test.

**How the high-end venv was made.** `uv … --offline` resolved Ray 2.55.1's dependencies to
versions the cache does not hold. It installed once each dependency was constrained to the
highest version the cache holds (a constraints file made from `~/.cache/uv/archive-v0/*/*.dist-info`).
01 may do the same.

### 0.2 Where the brief and this repository's records differ

To be reported back to the SI session with the tag:
1. **The field's shape.** The brief advises `extra_values: Mapping[str, Tuple[str, str]]`, a name
   the client chooses for each table. U1 keys the mapping **by the table's name**:
   `extra_values: Mapping[str, str]`, table → column, and `extra_value_counts` keyed the same way.
   A table cannot then be named twice, and no name can be empty, so of the brief's three refusals
   one is left: an extra table that is also the `values` table. For SI:
   `extra_values={"GradientCoupledInstantonValue": "instanton_serial"}`, read back as
   `record.extra_value_counts["GradientCoupledInstantonValue"]`.
2. **The tests are not on a separate registry alone.** The brief asks for a new neutral class or
   registry so that the neutral classes and the golden stay as they are. This repository's
   `test_every_declaration_field_is_in_use` requires the neutral registry to use every field
   (§0.1). So the neutral client declares it (U3), the neutral client's format becomes 2 with a
   new golden beside the old, and the format-1 golden is kept as the test of the compatibility
   property, in a stronger form than the brief's: the old golden is reproduced, byte for byte, by
   the new code reading a store that holds the new table, through a spec that does not declare it.
3. **Where the refusal is.** In `inventory_classes`, beside its other refusals and naming the class,
   not in `InventorySpec.__post_init__`: `dependent_tables`, and so `ShardedPool`'s drop, reads
   `inventory_specs` and never `inventory_classes`, and the brief's §6 rule ("no message, refusal or
   exception of the pool's") holds only if a spec's construction stays as forgiving as it is.
4. **`ENCODING_FORMAT`.** Stays 1, by the user's ruling (U2). The brief understates the literal
   reading (§0.1, check 4); the comment beside the constant and contract §9.8 say how item 1 is
   read, so that the next editor does not have to decide it again.
5. **Everything else the brief measured holds** (§0.1).

### 0.3 Found while writing 02: every client's spec guard moves (2026-10-21)

Measured at `c583c56`, through `git` only for the clients, while writing 02. U5 said ChamPBH and SGK
"need nothing". That is not so for a client that **hashes its specs**:
- SGK (`031bcb4`) and ChamPBH (`7055532`) each have a spec guard,
  `ObjectFactories/tests/test_fingerprint_format_guard.py`, which is RunRegistryKit's recipe (its
  `docs/adoption/README.md` §6, at its `v0.2.0`): `plain` turns each `InventorySpec` into JSON by
  walking `dataclasses.fields`, and `config/fingerprint.py`'s `SPEC_DIGESTS` pins each class's
  SHA-256 per `FINGERPRINT_FORMAT` (SGK 6, ChamPBH 3). SI has none;
- under 01's tree every plain spec gains `"extra_values": {}`, so **every digest moves** though no
  spec changed: all 13 of the neutral registry's, measured at `c8570e8` and at `5475cef`, and the
  same for two hand-built specs in the installed `v0.4.0` and `v0.5.0` wheels. The guard then fails
  naming every class and says to bump the format, which would move the format every fingerprint
  the client holds is compared at;
- **with one condition in `plain`, leaving out `extra_values` where it is empty, every digest is
  `v0.4.0`'s**, and only a spec that declares an extra table moves (`Trace`, on the neutral
  registry).

No record and no fingerprint moves; §0's constraint holds. The defect is in what U5 told the clients.
Opened as `[01-a-new-spec-field-moves-every-spec-guard-digest]` on the board, and settled by U5's
amendment (§6.2): no package change; the SGK and ChamPBH addenda say what a move needs. The same
condition belongs in RunRegistryKit's recipe, which is that repository's to amend.

## 1. Scope

**In scope:**
- `datastorekit/store_inventory.py`: `InventorySpec.extra_values`, `Record.extra_value_counts`,
  `as_json`, `read_records`, the refusal in `inventory_classes`, and the module docstring (U1);
- `datastorekit/store_fingerprint.py`: the comment beside `ENCODING_FORMAT` (U2);
- the neutral client and its fixtures (`tests/client/`, `tests/real_store_fixtures.py`), a new
  schema witness, a new golden fingerprint, and the test literals that name what changed (U3);
- a new test module (U4);
- `docs/client-contract.md`: a §9.8;
- the release (prompt 02, U5), with an addendum to each client's checklist.

**Out of scope:**
- **any client repository** (`CLAUDE.md`). SI adopts the release in a prompt of its own;
- **hashing a value table's rows.** A fingerprint counts value rows, by design; the extra tables
  are counted the same way;
- **any change to the pool**: nothing it writes or reads, and no message, refusal or exception of
  its, changes. A stand-in pool writes the neutral client's new table in the round-trip tests; that
  is the neutral client's change, not the pool's;
- **a check that a value column is a foreign key to its owner.** `values` has none today; SI's own
  test checks its specs. If wanted, it is a request of its own, for both slots;
- the four issues on `inherited-issues` (`docs/OPEN_ISSUES.md` §1.2), in particular
  `[00-the-inventory-cannot-see-a-serial-split]`, and anything else a prompt finds: it is recorded,
  not fixed (§5 rule 4).

## 2. Prompts

| # | Prompt | Covers | Status |
|---|---|---|---|
| 01 | [`01-a-spec-counts-more-than-one-value-table.md`](01-a-spec-counts-more-than-one-value-table.md) | `InventorySpec.extra_values` and `Record.extra_value_counts`, `as_json`'s conditional key, the counting and its orphans, the refusal (U1); the `ENCODING_FORMAT` comment (U2); the neutral client's `TraceMark`, the witness, `NEUTRAL_FORMAT` 2 and its golden (U3); `tests/test_inventory_extra_values.py` and the amended literals (U4); contract §9.8. | **written** 2026-10-21; U1–U4 taken; **landed** 2026-10-21, `5475cef` ([log](logs/01-a-spec-counts-more-than-one-value-table.md)); **reviewed** 2026-10-21 |
| 02 | [`02-release-v0.5.0.md`](02-release-v0.5.0.md) | `pyproject.toml`, `README.md`, `PROVENANCE.md`; dated addenda to `docs/adoption/` (SI's saying what it does; ChamPBH's and SGK's that nothing they call or hold changes, and that a move needs one edit to their spec guard, §0.3); the extraction board's G4 sentence; closes `[01-a-new-spec-field-moves-every-spec-guard-digest]`; both ends locally and in CI; **the tag** on its commit after green CI (U5). | **written** 2026-10-21, against `c583c56`; U5 taken and amended (§0.3) |

**Order.** 01 → 02. 02 releases what 01 leaves. Each is landed and reviewed on its own.

## 3. Datastores

No prompt opens a store of any client. Tests build their stores in `tempfile` directories with the
neutral client's fixtures.

## 4. The interfaces between prompts

- **After 01:** `InventorySpec.extra_values` and `Record.extra_value_counts`, as U1 says;
  `ENCODING_FORMAT` 1 and its comment; the neutral client's `TraceMark`; the witness
  `schema_at_extra-values-01.json`; the golden `store_fingerprint-neutral-2-encoding-1.json`;
  contract §9.8.
- **After 02:** `pyproject.toml` at the version U5 names; the adoption addenda. After its CI
  passes, the tag on 02's commit, and the tag object, the commit and the SI addendum given to the
  user for SI's pin prompt.

## 5. The rules this campaign runs under

The project-wide ones in `CLAUDE.md`, plus:

1. **One commit per prompt**, in this repository only.
2. **Every prompt writes a log** to `logs/NN-<name>.md`, using §5.1.
3. **Every prompt updates `IMPLEMENTATION_STATE.md`** in its own commit, plus
   `docs/OPEN_ISSUES.md`.
4. **Do not fix things the prompt did not ask for.** A defect found is recorded with a §3 issue.
   Nothing rides in the release but U1–U3, unless the user rules otherwise.
5. **No prompt edits, runs or imports a client.** Reading one through `git` is allowed. No
   client's code, tests or stores are run or opened.
6. **No test needs Ray, imports a client, or opens a store outside a `tempfile` directory.** The
   suite count is recorded before and after each prompt; a count that falls is a stop.
7. **Ray is not started** by any prompt of this campaign.
8. **Deliberate breakage.** Each prompt names mutations its tests must catch. The log records each
   as a diff, exactly as applied, so the orchestrator can replay it with `git apply`. Mutations are
   never committed.
9. **No tag except where a prompt says so** (02), and none is moved or deleted. No prompt pushes.
10. **Verification documents are additive** (`CLAUDE.md` rule 6): a re-run that supersedes a
    measurement is a new dated subsection. A contract row is superseded by a §9 row, not rewritten.
11. **A golden fingerprint and a schema witness are never rewritten.** A change is a new file beside
    the old, and a move of the constant that names it (`fingerprint` U3, U4;
    `tests/test_schema_builder.py`'s docstring).

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
and tag with the user's approval) and U36 (a fix release is patch-level). So do `actor-names`
U1–U4, `factory-defaults` U1–U5, `object-timestamp` U1–U6 and `fingerprint` U1–U6. `fingerprint`
U3, the bump rule, is not reopened: U2 records how its item 1 is read.

### 6.2 Decisions this campaign needs

- **U1: the fields, and how they are read.** *(The change is the user's request, 2026-10-21. Taken
  2026-10-21, as recommended.)* **Recommended:**
  - **`InventorySpec.extra_values: Mapping[str, str] = field(default_factory=dict)`**, the spec's
    last field: each further value table → its column naming this class's serial. `keywords()`
    hands it to `read_records`, which takes `extra_values: Optional[Mapping[str, str]] = None`, its
    last keyword. `dependencies()` is unchanged: a value table names its owner by foreign key;
  - **`Record.extra_value_counts: Mapping[str, int] = field(default_factory=dict)`**, the record's
    last field: for each declared table, the number of its rows naming this row, **0 where none**,
    so the mapping has every declared table and is empty only where none is declared. A literal
    `{}` default is not possible: a dataclass refuses a mutable default. `Record.__hash__` is
    written by hand (`canonical_json`), so a dict field keeps a record hashable;
  - **`as_json`** returns today's four keys, and a fifth, `"extra_value_counts"`, a plain `dict`,
    **only when the mapping is not empty**. `canonical_json` sorts keys, so the mapping's order
    does not matter. `identity()` is unchanged (it holds no count). The replicated comparison and
    the record order read `canonical_json`, so both cover the counts with no change;
  - **counting**: one `GROUP BY` per extra table per shard, exactly as `values` is counted, rows
    naming a serial not on the shard an **`orphan-value`** problem in today's words, naming the
    table and the shard. One inner function serves `values` and each extra table, so the two cannot
    drift; extra tables are counted in sorted name order, so problems come in a fixed order;
  - **one refusal**, in `inventory_classes` beside its others: a spec whose `values` table is also
    in its `extra_values` raises `ValueError` naming the class and the table. A table or column
    that does not exist fails when read (`KeyError`), as `values` does.

  **Why keyed by table.** The table's name is what the client already writes in `values`, and is
  unique; a second name per table would be a choice with nothing to decide it, and would need two
  more refusals. **Why omitted when empty.** It is the compatibility property: a record of a class
  that declares nothing is today's. **Why in `inventory_classes`.** §0.2, point 3.

  **Rejected:** `values` becoming a sequence or mapping, and `value_count` a mapping (it changes
  every record of every class with a value table, in every client: SGK seven, ChamPBH three, SI
  five, and so every recorded fingerprint, and bumps `ENCODING_FORMAT` by its first sentence);
  a client-chosen name per table (the brief's; above); emitting the key on every record (moves
  every digest); validating in `__post_init__` (§0.2, point 3); checking that the column is a
  foreign key (out of scope, §1).
- **U2: `ENCODING_FORMAT`.** *(The user's ruling, 2026-10-21: it stays 1, and the comment is
  added.)* `ENCODING_FORMAT` stays **1**. The comment beside it (`store_fingerprint.py:38-64`)
  gains a paragraph after its last sentence: item 1 is read by the rule above it; a field added to
  `Record.as_json` that a record carries only where its class's spec declares what fills it
  (`extra_value_counts`, from `InventorySpec.extra_values`) is not a bump, since a store read with
  the same specs gives the same records; a client whose spec comes to declare it changes its own
  fingerprints, which is its `fingerprint_format`. Contract §9.8 states it in the same words, as a
  row superseding §9.7's `ENCODING_FORMAT` row in that part. Nothing else of the comment changes.
  **Why:** a bump would make `compare_fingerprints` refuse every fingerprint SGK and ChamPBH hold
  as soon as they moved their pins (`store_fingerprint.py:178-227`), for a release that changes
  none of their records.
- **U3: the neutral client declares it.** *(Taken 2026-10-21, as recommended.)* **Recommended:**
  - **a table `TraceMark`** under the sharded `Trace`, a further value table written only for a
    Trace that carries marks, as SI's second table is written only sometimes: columns
    `trace_serial` (`Integer`, foreign key `Trace.serial`, indexed, not null) and `mark_index`
    (`Integer`, not null), no `version`, no `timestamp`; registered after `TraceStep`, in the
    `traces` drop group after `TraceStep`, and in the registry's roles table. `Trace`'s spec gains
    `extra_values={"TraceMark": "trace_serial"}`. The client's `Trace` object gains `marks`, a
    sequence of indices, and its factory's `store` writes one `TraceMark` row each; `build` need not
    read them back. In the round trip, `trace-one` carries marks `(0, 1)`. In the full store, Trace 3 (shard 0) has two
    `TraceMark` rows, serials 1 and 2, and Trace 4 none;
  - **a new schema witness**, `tests/data/schema_at_extra-values-01.json`, captured with
    `schema_description.py`'s `__main__`, `WITNESS` repointed to it; its diff from
    `schema_at_extraction-06.json`, additions only, in 01's log;
  - **`NEUTRAL_FORMAT` 2** and a new golden, `tests/data/store_fingerprint-neutral-2-encoding-1.json`,
    beside the format-1 golden, which is kept and read by U4 test 1;
  - the test literals that name what changed: the field list in
    `test_every_declaration_field_is_in_use`; the key set in `test_records_are_json_safe`, by
    class; `VALUE_TABLES` in `test_store_inventory.py`, which gains `TraceMark`, so that the check
    that value tables are counted and never listed covers it; the "another format" in
    `test_another_format_moves_only_the_overall_digest`.

  **Why.** The neutral registry exercises every declaration field, by a test written for that
  purpose (§0.1). A change to the neutral client's specs is the neutral client's format, never
  `ENCODING_FORMAT` (`fingerprint` U3), so it moves `NEUTRAL_FORMAT` and adds a golden, as its
  comment says (`test_store_fingerprint.py:55-56`). **Why `Trace`:** it already has a value table,
  so the spec shows both slots together, as SI's will. **Rejected:** a separate registry only (the
  brief's; it fails the coverage test, and loosening that test removes the guard for the next
  field); declaring an existing child table (`Trace_tags`, `Sample_members`) as an extra value
  table (it would count a table that is not a value table, and teach the wrong use); a class of its
  own (more schema for no more coverage).
- **U4: the tests.** *(Taken 2026-10-21, as recommended.)* **Recommended:** a new module,
  `datastorekit/tests/test_inventory_extra_values.py`, no Ray, every store in a `tempfile`
  directory, built with `real_store_fixtures`. A **wider** registry, local to the module, adds to
  the neutral one a second extra table under `Trace` (`TraceNote`) and one under `Gadget`
  (`GadgetNote`), each declared; `build_real_store` takes an optional `factories` (default the
  neutral registry's) so that its shards hold the wider registry's tables. Tests:
  1. **compatibility**: the full store read through the neutral registry with `Trace`'s spec less
     `extra_values` gives, at format 1, the format-1 golden, every field but `taken`; and every
     class but `Trace` has the same canonical lines read either way;
  2. **counts**: on the full store, Trace 3's record has `{"TraceMark": 2}`, every other Trace
     `{"TraceMark": 0}`, and its `value_count` as before; every other class's records have
     `extra_value_counts == {}` and `as_json` keys exactly the four;
  3. **two tables**: through the wider registry, each count per table, 0 where a table has no row;
     no problems;
  4. **orphans**: a row of an extra table naming a serial not on its shard gives exactly one
     `orphan-value` problem, naming the table and the shard; the fingerprint counts it by name;
  5. **replicated divergence**: an extra count of the replicated `Gadget` that differs between
     shards gives `replicated-divergence` and no other problem;
  6. **the fingerprint sees it**: one `TraceMark` row deleted changes the overall digest and
     `Trace`'s entry only, and `compare_fingerprints` names `Trace` alone;
  7. **the refusal**: `values` also in `extra_values` raises `ValueError` from `inventory_classes`,
     naming the class and the table; `dependent_tables` and `inventory_specs` of the same registry
     do not raise;
  8. **`dependent_tables`**: the same answer with and without `Trace`'s declaration, for drops of
     `Trace`, `TraceMark` and `keypoint`; `TraceMark` is among the tables a drop of `Trace` takes.

  **Rejected:** tests through `read_records` alone (they would miss the driver, `_combine` and the
  fingerprint); extending `build_full_store` to other registries (its empty shard is cached for the
  neutral schema; `build_real_store` over `fill_required` rows serves).
- **U5: the shape, the release, and who adopts it.** *(Taken 2026-10-21, as recommended. Needed by
  02, not 01.)* **Recommended:**
  - **two prompts**, as the last four campaigns: 01 the change and its evidence, 02 the release,
    written after 01 is reviewed;
  - **`v0.5.0`**, minor: the release adds API (two fields and a keyword), which made `v0.2.0`,
    `v0.3.0` and `v0.4.0` minor;
  - **SI adopts it**, in a pin prompt of its own: pins the release, declares
    `GradientCoupledInstantonValue` under `extra_values`, moves it from its coverage test's
    `EXCLUDED`, shows the count in its report. SI has recorded no fingerprint;
  - **ChamPBH and SGK need nothing.** Each may stay on `v0.4.0` or move, in a commit of its own;
    their recorded fingerprints stay valid either way. Their addenda say so;
  - the tag object, the commit and the SI addendum's anchor are given to the user for SI's pin
    prompt.

  **Rejected:** one prompt for the change and the release; `v0.4.1`, treating added API as a fix.

  **Amended 2026-10-21, by the user** (§0.3), in its fourth item: ChamPBH and SGK may stay on
  `v0.4.0` or move, as before, but **a move needs one edit to each one's spec guard**: its `plain`
  leaves out `extra_values` where it is empty, after which every pin holds at the same format. The
  SGK and ChamPBH addenda say so, and that the format is not bumped for this. Every client is now on
  `v0.4.0` (§0.3's commits), so the addenda give that as the starting pin. **Rejected:** moving
  `extra_values` out of `InventorySpec` (a separate factory hook) so that no spec's fields change:
  the guard would then miss a client that comes to declare an extra table, which does move its
  fingerprints; letting the clients re-pin their digests at the same format, against their own
  guards' rule.

## 7. Gates outside this repository

None of this campaign's own. **SI's pin prompt waits on the tag**: it is written from the tag
object and commit. If SI's adoption finds a difference from what the addendum says, it comes back
to this repository as a defect, opened on this board.
