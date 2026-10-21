# Prompt 02 — release `v0.5.0`

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

*Written 2026-10-21 against `c583c56`, whose `datastorekit/` and `docs/` are `5475cef`'s (prompt
01's).*

**Gate:**
- 01 landed (`5475cef`) and was reviewed (`dde3201`).
- **01 is pushed, and CI is green on it**: `origin/main` is `c583c56`; run 39680233763, on
  `dde3201`, passed at both ends. Unlike `fingerprint` 02, this prompt is not the first CI run on
  the code it releases. The tag still waits on CI at 02's own commit (§1).
- U5 is taken, **as amended by the user on 2026-10-21** (README §6.2): `v0.5.0`, minor; SI adopts
  it; SGK and ChamPBH may stay on `v0.4.0` or move, and **a move needs one edit to each one's spec
  guard** (§1.1, README §0.3).
- `git status` is clean in this repository, and `origin/main` is an ancestor of `main`.
- This board's §3 holds one issue, `[01-a-new-spec-field-moves-every-spec-guard-digest]`, assigned
  to this prompt; `docs/OPEN_ISSUES.md` counts 5.

**Closes:** `[01-a-new-spec-field-moves-every-spec-guard-digest]`, by saying in the SGK and ChamPBH
addenda what the move needs (§2.4). **Changes:** nothing in the package but its version.
**Opens:** only what the work finds.

**Recommended model:** **Opus.**
- No line of code changes. The work is three short edits, four dated addenda and one gate sentence.
- The addenda are not alike. SI's is the note SI's pin prompt reads: what it declares, where, and
  what of its own tests that moves. SGK's and ChamPBH's must say, precisely and without advice
  beyond what is marked **Advice:**, that nothing they call changes, that no fingerprint they hold
  moves, and that their spec guard fails on the move unless it is edited, with the edit.
- Each file's head gains a line, which moves every citation below it, including the `v0.4.0`
  addendum's own table. The addendum says how to read those, as `fingerprint` 02 did.
- The release check and both ends of the suite are run as `fingerprint` 02 ran them, offline.

**Read first:**

1. [`README.md`](README.md): §0 (§0.1–§0.3), §1, §2, §4, §5 (rules 4, 5, 9, 10 and 11), §6.1, §6.2
   (U1–U3, and U5 with its amendment) and §7.
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`, above all "Releases".
3. This board: the review of 01, and §3's issue. Log 01
   (`logs/01-a-spec-counts-more-than-one-value-table.md`), §1, §6 and §8.
4. `fingerprint` prompt 02 (`../fingerprint/02-release-v0.4.0.md`) and its log
   (`../fingerprint/logs/02-release-v0.4.0.md`). 02 is that prompt again, for one change. Their
   release check, their addenda's form, their supersession tables and their breakages are this
   prompt's.
5. The files 02 changes, as they stand: `pyproject.toml`, `README.md`, `PROVENANCE.md`,
   `docs/adoption/README.md` and the three checklists. In each, read the head and the `v0.4.0`
   addendum in full.
6. `docs/client-contract.md` §9.8, which 02 points at and does not change.
7. The extraction board's §2 (G1–G4), `../extraction/IMPLEMENTATION_STATE.md:1536-1541`.
8. Read through `git show` only (README §5 rule 5):
   - SGK at `031bcb4` and ChamPBH at `7055532`: `ObjectFactories/tests/test_fingerprint_format_guard.py`
     and `config/fingerprint.py`;
   - SI at `f5f395b`: `Datastore/SQL/ObjectFactories/GradientCoupledInstanton.py` (the spec,
     `:147-182`; the value table's `instanton_serial`, `:686-692`), `tests/test_inventory_specs.py`
     (`:195-240`, `:405-415`) and `tools/inventory_report.py`; and the brief,
     `.prompts/dk-and-rpk-migration/datastorekit-second-value-table-brief.md`;
   - RunRegistryKit (`/Users/ds283/Documents/Code/RunRegistryKit`) at its tag `v0.2.0`:
     `pyproject.toml` and `docs/adoption/README.md` §6, the guard's recipe. RunRegistryKit is not a
     client of this campaign and nothing of it is changed here.

Facts below are at `c583c56`, measured on 2026-10-21.

---

## 1. What is wanted

02 makes the package ready to be released as **`v0.5.0`** (U5). After it:

- `pyproject.toml` says `0.5.0`;
- `README.md` and `PROVENANCE.md` describe `v0.5.0`;
- `docs/adoption/` carries a dated addendum, in its README and in each checklist, giving the pin
  and what changed for that client since `v0.4.0`; SI's says what SI does to adopt it; SGK's and
  ChamPBH's say what a move needs;
- the extraction board's G4 gains a dated sentence. G1, G2 and G3 are not changed;
- the issue `[01-a-new-spec-field-moves-every-spec-guard-digest]` is closed: moved to this board's
  §4 and its row deleted from the index.

**No line of code changes.** Nothing under `datastorekit/` is touched, and the suite stays at
**538**.

**02 makes no tag and pushes nothing** (extraction U23, U28; README §5 rule 9). After its review,
its commit is pushed as `main`. `v0.5.0` is made on it, annotated, only once CI passes there at
both ends. If CI fails, a fix prompt lands first, and no tag is ever made on a commit whose CI is
red. The tag is not this prompt's work.

### 1.1 What changed since `v0.4.0`, measured

One prompt changed the package after `v0.4.0` (`c8570e8`): 01, `5475cef` (U1–U4; U2 the user's
ruling).

- **In the wheel, two modules changed and none was added**: `datastorekit/store_inventory.py`
  (+57 −18: the two fields, `as_json`'s conditional key, `read_records`' keyword and its counting,
  the refusal in `inventory_classes`, the docstrings) and `datastorekit/store_fingerprint.py` (+6:
  the comment beside `ENCODING_FORMAT`, which stays `1`). `git diff --stat c8570e8 5475cef --
  datastorekit` lists those two and, outside the wheel, the neutral client, the fixtures, two new
  data files and the tests.
- **Outside the wheel**: `datastorekit/tests/test_inventory_extra_values.py` (8 tests: 530 → 538),
  the neutral client's `TraceMark`, the witness `schema_at_extra-values-01.json`, the golden
  `store_fingerprint-neutral-2-encoding-1.json`, and contract §9.8 with its head line.

**What a client sees** (contract §9.8):
- **`InventorySpec.extra_values`**, the spec's last field, default `{}`: each further value table →
  its column naming the class's serial, counted as `values` is.
- **`Record.extra_value_counts`**, the record's last field, default `{}`: for each declared table,
  its rows naming the record's row, 0 where none. **`as_json` carries it only where it is not
  empty**, so a record of a class that declares no extra table is `v0.4.0`'s, byte for byte, and
  so is every fingerprint of a store read with unchanged specs. `ENCODING_FORMAT` stays `1`.
- **One new refusal**, in `inventory_classes` only: a spec whose `values` table is also in its
  `extra_values`. No spec's construction refuses, and nothing of the pool changes.
- **A spec's dataclass fields are seven**, where they were six. That is invisible to the package,
  and to every client that does not walk them. **Two clients walk them** (below).

This is added API, so the release is minor (U5, reading extraction U36 and `fingerprint` U6).

**What the clients do with it**, read through `git` only. The planner's measure: a script of `ast`
reads of every `.py` file from `git show <commit>:<path>`, outside each client's `prompts/`,
`.prompts/`, `docs/` and `.documents/`, finding every call of `InventorySpec`, `Record`,
`read_records`, `dataclasses.fields`, `is_dataclass` and `asdict`, and every attribute
`extra_values`, `extra_value_counts`, `value_count` and `as_json`, and where `SPEC_DIGESTS` and
`FINGERPRINT_FORMAT` are assigned.

| Client, commit | Its pin | `InventorySpec(` | `Record(` | A spec's fields walked | `extra_*` read |
|---|---|---|---|---|---|
| SGK `031bcb4` (`handover-remedial`, clean) | `v0.4.0` (`requirements.txt:17`) | 21, none passing `extra_values` | 2, by keyword (`tools/tests/test_inventory_report_labels.py:89`, `:113`) | **yes**: `ObjectFactories/tests/test_fingerprint_format_guard.py:33-44` (`plain`), pinned by `config/fingerprint.py:60` (`SPEC_DIGESTS`), format 6 (`:49`) | none |
| CPBH `7055532` (`jordan-normalization`, clean) | `v0.4.0` (`requirements.txt:17`) | 13, none passing `extra_values` | none | **yes**: `ObjectFactories/tests/test_fingerprint_format_guard.py:51-62`, pinned by `config/fingerprint.py:88`, format 3 (`:67`); its `asdict` calls (`:147-148`) are on a `Parent`, which is unchanged | none |
| SI `f5f395b` (`dk-and-rpk-migration`, clean) | `v0.4.0` (`requirements.txt:16`) | 22, none passing `extra_values` | 1, by keyword (`tests/test_inventory_report.py:67`) | no | none |

(The other `fields` calls the measure finds, in each client's `tools/inventory_report.py`, are the
report's own `fields()` method, not `dataclasses.fields`.)

**The spec guard** (`[01-a-new-spec-field-moves-every-spec-guard-digest]`, README §0.3). SGK's and
ChamPBH's guards are RunRegistryKit's recipe (its `docs/adoption/README.md` §6, at its `v0.2.0`):
`plain` turns a spec into JSON by walking `dataclasses.fields`, and the SHA-256 of each class's
plain spec is pinned per `FINGERPRINT_FORMAT`. Under `v0.5.0` every plain spec gains
`"extra_values": {}`, so **every class's digest moves**, though no spec changed, and the guard
fails naming every class, saying to bump `FINGERPRINT_FORMAT`. A bump would change the format
number every fingerprint they hold is compared at, for a release that changes none of their
records. The planner measured:
- on the neutral registry, the recipe's digests at `v0.4.0` (an export of `c8570e8`) and at
  `5475cef`: all 13 classes differ; with `plain` leaving out `extra_values` where it is empty, only
  `Trace`, whose spec does declare one, differs;
- on two hand-built specs, in the two installed wheels (§1.2): the recipe's digests under
  `v0.5.0` differ from `v0.4.0`'s; with that one condition, they are equal.

So **the edit is one condition in `plain`**: leave out a field named `extra_values` whose value is
empty. With it, every pin a client holds stays valid at the same format, and a spec that comes to
declare an extra table moves its digest, as the guard means it to. The client's own guard is the
client's code; this repository changes none of it. The same edit belongs in RunRegistryKit's
recipe, in a campaign of that repository's own (§8).

**SI** declares nothing yet and has no guard and no recorded fingerprint. Its adoption (U5) is: the
pin; `extra_values={"GradientCoupledInstantonValue": "instanton_serial"}` in
`GradientCoupledInstanton`'s spec (`Datastore/SQL/ObjectFactories/GradientCoupledInstanton.py:147-182`, `InventorySpec(` at `:158`,
`values=` at `:180`; the column `instanton_serial` is a foreign key to
`GradientCoupledInstanton.serial`, `:686-692`); its coverage test, which excludes the table
(`tests/test_inventory_specs.py:208-214`) and reads a slot as a pair (`_slot_tables`, `:224-228`, beside `SLOTS`, `:216`;
the counts asserted at `:412`); and, as it chooses, its report (`tools/inventory_report.py`, which
reads `value_count`). What SI changes is SI's.

**RunRegistryKit**, which SGK and ChamPBH also pin (`runregistrykit[stores]` at `v0.2.0`),
requires `datastorekit>=0.4.0` in its `stores` extra (its `pyproject.toml`), so `v0.5.0` resolves
beside it.

**The clients' pins and `HEAD`s move** (other sessions work there). Record what you read, and
compare nothing but the table's facts.

### 1.2 The release check, probed

The planner probed the release on this machine, offline, as `fingerprint` 02 did.
- **The build.** From a `git archive` of `c583c56` with only `version = "0.5.0"` changed,
  `uv build --offline --wheel` gives `datastorekit-0.5.0-py3-none-any.whl` (105,087 bytes). It has
  26 entries, none under `datastorekit/tests/`. `METADATA` says `Version: 0.5.0`,
  `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43` and `Requires-Dist:
  sqlalchemy<2.1,>=2.0.39`.
- **Against `v0.4.0`'s wheel**, built from `git archive v0.4.0` (104,424 bytes, 26 entries): of
  the 21 `RECORD` lines under `datastorekit/`, 19 are equal, none is added or missing, and two
  differ:

  ```
  datastorekit/store_fingerprint.py,sha256=enGZPLYaYQFvoR3LSCJYTk8DtYQRK0eU_97Nb43nzm4,16492
  datastorekit/store_inventory.py,sha256=DJgAqZr-5LH_4ME69rtdSstFhAHdC8uSlkVUvaK5uE0,47280
  ```

  (`v0.4.0`'s: `…OIGFxRU6…,16093` and `…4PJPPpQe…,45013`.)
- **The install.** Each wheel into its own `uv venv --offline -p /opt/local/bin/python3.13`, with
  `"ray==2.55.1" "sqlalchemy==2.0.46"`, offline. With the cache's constraints file, leave out its
  `datastorekit` line: the cache holds `v0.4.0`'s wheel, and the line refuses `0.5.0`.
- **The run**, from a directory outside the repository with `PYTHONPATH` unset and `python -I`, in
  the release's venv:
  - `datastorekit` imports from the venv's `site-packages`; `importlib.metadata.version` is
    `0.5.0`; `ENCODING_FORMAT` is `1`;
  - `InventorySpec`'s fields are `leaves, parents, tags, values, validated, parent_sets,
    extra_values`; `Record`'s are `key, tags, validated, value_count, extra_value_counts`;
    `InventorySpec().keywords()` holds `extra_values`;
  - a `Record` built without counts has `as_json` keys `key, tags, validated, value_count`, and its
    `canonical_json` is the same string the `v0.4.0` wheel gives for the same record; with
    `extra_value_counts={"T2": 0}` the keys are five, and the record hashes;
  - a hand-built `StoreInventory` (as `fingerprint` 02's probe built one) fingerprints to the same
    digest in both venvs;
  - the guard's recipe (RunRegistryKit's `plain` and `spec_digests`, copied into the probe) over two
    hand-built specs: under `v0.5.0` its digests differ from `v0.4.0`'s; with the one condition of
    §1.1, they are equal to `v0.4.0`'s plain ones;
  - `inventory_classes` of a hand-built registry whose spec names its `values` table in its
    `extra_values` raises `ValueError` naming both; `inventory_specs` of it does not;
  - in a fresh interpreter, `import datastorekit.store_inventory` leaves `ray` out of
    `sys.modules`; `import datastorekit.tests` raises `ModuleNotFoundError`; `python -m
    datastorekit.tools.sharded_store --help` exits 0.

The wheel's bytes are not reproducible across builds (file times). Record the SHA-256 of yours,
and do not compare it with the planner's. The `RECORD` lines are content hashes, and do compare.

---

## 2. What to change

### 2.1 `pyproject.toml`

`version = "0.5.0"` (`:7`). Nothing else. No other file carries the version.

### 2.2 `README.md`

- **Status.** A paragraph for **`v0.5.0`**, above `v0.4.0`'s (`README.md:10-20`):
  - a minor release with one change, `extra-values` prompt 01, at a client's request: a factory's
    `InventorySpec` may name further value tables (`extra_values`), each counted as `values` is,
    into each record's `extra_value_counts`;
  - a record of a class that declares none is `v0.4.0`'s, byte for byte, and so is every
    fingerprint of a store read with unchanged specs; `ENCODING_FORMAT` stays 1;
  - nothing the layer writes or reads changes, and no message, refusal or exception of the
    layer's; the inventory gains one refusal, in `inventory_classes`;
  - a spec now has seven fields: a client that hashes a spec by walking its fields sees every
    digest move, and the addenda say what to do;
  - it adds API, so it is a minor release;
  - it points at contract §9.8 by its anchor.
- **Installing.** The pin is `v0.5.0` (`:105`). Replace `:108-111` with what U5 says, as of the
  tag: `v0.4.0`, `v0.3.0`, `v0.2.3`, `v0.2.2`, `v0.2.1`, `v0.2.0` and `v0.1.0` remain tagged, and
  no tag is moved or deleted; StochasticInstantons adopts `v0.5.0`; SecondaryGWKit and ChamPBH may
  stay on `v0.4.0` or move to `v0.5.0`, in a commit of their own, as each chooses; a client whose
  tests pin digests of its specs reads its addendum first. Name no client's paths.
- **Using it.** "The inventory declarations" (`:134-135`) names the further value tables and links
  §9.8 by anchor; **"What changed after `v0.2.0`"** (`:150-159`) adds `v0.5.0`'s change, still
  linking §9.
- **Nothing else changes.** Check every name and anchor the README mentions.

### 2.3 `PROVENANCE.md`

Add, after "`fingerprint` prompt 01: the store fingerprint moves into the package (`v0.4.0`)"
(`:274`, the file's last section, ending at `:319`), a `###` section **"`extra-values` prompt 01:
an inventory spec counts more than one value table (`v0.5.0`)"**. It says:
- **It has no source in a client.** It is the package's own change, at StochasticInstantons'
  request (its brief, SI `f5f395b`, `.prompts/dk-and-rpk-migration/datastorekit-second-value-table-brief.md`),
  decided by `prompts/extra-values/README.md` §6.2 (U1–U4; U2 the user's ruling) and made by
  `extra-values` prompt 01 (`5475cef`). Where it departs from the brief: README §0.2.
- **What changed in the package**: §1.1's two modules, with what each change is; nothing added or
  removed from the wheel; every record of a class that declares no extra table unchanged, shown by
  01's test 1, which reproduces the format-1 golden through a spec that does not declare the field.
- **Outside the wheel**: §1.1's list; the suite from 530 to 538.
- **The files 01 changed, and its log.**

Change nothing above it.

### 2.4 The addenda (U5)

Each addendum is dated, says it was written by `extra-values` prompt 02, and is added. **Nothing
already in the file is rewritten** (`CLAUDE.md` rule 6): 07a's text and the `v0.2.1` to `v0.4.0`
addenda all stay as written, true of their releases. Each file gains two things.

1. **An italic line at its head**, after `fingerprint` 02's (`docs/adoption/README.md:27-30`,
   `secondarygwkit.md:39-43`, `champbh.md:40-44`, `stochasticinstantons.md:38-42`). It says that the
   addendum below gives the pin and what changed since `v0.4.0`, and that it supersedes the
   statements it names.
2. **A section `## Addendum: v0.5.0 (extra-values prompt 02, <date>)`**, unnumbered, after the
   `v0.4.0` addendum. In each checklist it goes before `## Appendix: the script's output`
   (`secondarygwkit.md:959`, `champbh.md:797`, `stochasticinstantons.md:776`), in the form the
   `v0.4.0` addendum took there. In the README it goes at the end (`:737`). The date is the day
   you write it.

Each addendum states:
- **the pin, by client** (U5 as amended): every client is on `v0.4.0` (§1.1's table). SI adopts
  `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.5.0`, by a pin prompt of its own;
  SGK and CPBH may stay on `v0.4.0` or move to `v0.5.0`, as each chooses, a move being a commit of
  the client's own. G2 ("`v0.2.2` or later"), G3 ("`v0.2.3` or later") and G4 ("`v0.3.0` or later")
  read as before;
- **what changed since `v0.4.0`, for that client** (below), with contract §9.8 as the detail,
  linked by anchor;
- **which statements it supersedes**, each by `path:line` of the file it is in. At least: the head
  line that says the `v0.4.0` addendum gives the pins; the `v0.4.0` addendum's pin statements, and
  its statements of what the client's `requirements.txt` pins (each client has since moved to
  `v0.4.0`); and its rows of the same;
- **how to read the earlier addenda's citations**, as the `v0.4.0` addendum did: this addendum's
  head line moves every line below it, so the `v0.4.0` addendum's `path:line`s are read at
  `c8570e8`, or N lines later here (say N, and which citations are above the insert), and the
  rule that addendum states for the earlier ones still holds, each shift N more, as a number;
- **line citations.** A `datastorekit/` line this addendum cites is `v0.5.0`'s tree, whose
  `datastorekit/` is `5475cef`'s and 02's. A client's line is that client's at the commit named.

What each addendum says:

| File | States | Supersedes, at least (each in part, by `path:line`) |
|---|---|---|
| `README.md` | the pins by client; what changed, §1.1's "What a client sees", linked to contract §9.8; nothing any client supplies or stores changes, and no message of the layer's; §1.1's measure, per client, in one table; **the spec guard**: what the recipe does, why every digest moves, the one condition, and that with it every pin stays valid at the same format and a declaring spec moves its digest; that the recipe is RunRegistryKit's, whose own text is that repository's to amend; the checklists are not re-measured (as U37), and each has its own addendum | the `v0.4.0` addendum's pins and its rows that give the pins or count the addenda ("each checklist with its five addenda") |
| `secondarygwkit.md` | SGK is on `v0.4.0` (`requirements.txt:17` at `031bcb4`) and may stay or move to `v0.5.0`. **What the move changes for SGK**: nothing it calls; no record and no fingerprint of a store read with SGK's specs, at format 6; and **its spec guard**, `ObjectFactories/tests/test_fingerprint_format_guard.py` (`plain`, `:33-44`; `SPEC_DIGESTS`, `config/fingerprint.py:60`), which then fails naming every class and saying to bump the format. **Do not bump it for this**: the specs did not change. The edit is the one condition in `plain` (§1.1), after which every pin at format 6 holds. **Advice:** make the edit in the commit that moves the pin, and run the guard before and after it. G2's reading and its holding stand | the `v0.4.0` addendum's pin statements (SGK adopts `v0.4.0` in place of `v0.2.2`; `requirements.txt:17` pins `v0.2.2`), in part, and its rows of the same; **not** its account of the fingerprint functions, which holds at `v0.5.0` |
| `champbh.md` | CPBH is on `v0.4.0` (`requirements.txt:17` at `7055532`) and may stay or move to `v0.5.0`; the same as SGK's, for CPBH's guard (`ObjectFactories/tests/test_fingerprint_format_guard.py:51-62`; `SPEC_DIGESTS`, `config/fingerprint.py:88`; format 3); its `asdict` of a `Parent` (`:147-148`) is unchanged. G3's reading and its holding stand | the `v0.4.0` addendum's pin statements (CPBH has adopted `v0.3.0`, may stay or move to `v0.4.0`), in part, and its rows of the same |
| `stochasticinstantons.md` | **the note SI's pin prompt reads.** SI adopts `v0.5.0` in place of `v0.4.0` (`requirements.txt:16` at `f5f395b`). What it declares and where: `extra_values={"GradientCoupledInstantonValue": "instanton_serial"}` in `GradientCoupledInstanton`'s spec, beside `values=` (§1.1's lines). What then holds: each `GradientCoupledInstanton` record carries `extra_value_counts`, `{"GradientCoupledInstantonValue": n}`, n the record's rows, 0 where none (a row stored without full values); orphans of the table are `orphan-value` problems; the table and its column are read when the inventory is (a store lacking either: `KeyError`); naming `GradientCoupledInstantonProfile` in both slots is refused by `inventory_classes`. What of SI's own moves: its coverage test's exclusion and slot reader and the counts it asserts; its report, if SI chooses to show the counts; the issue SI holds, `[gci-value-table-outside-the-inventory]`, which is SI's to close. SI has recorded no fingerprint and has no spec guard; **Advice:** if it adds one, use the recipe with §1.1's condition. Where this release departs from SI's brief: README §0.2, each point. G4 reads as before and is not recorded here | the `v0.4.0` addendum's pin statements (SI adopts `v0.3.0` or `v0.4.0`), in part, and its rows of the same; not G4's reading |

**The line numbers here are the planner's at `c583c56`.** Check each against the file before citing
it, and cite what you find, in the file as committed with your addendum. A statement the table does
not name that is no longer true of `v0.5.0` is superseded too, and recorded in the log: grep each
file for `v0.4.0`, `requirements.txt`, `value_count`, `InventorySpec`, `five addenda` and
`RunRegistryKit`.

### 2.5 The extraction board's gate

On `../extraction/IMPLEMENTATION_STATE.md` §2, **G4**'s status cell gains one dated italic sentence
at its end, in the form of the `v0.4.0` "ready to be tagged" sentence: `v0.5.0` is ready to be
tagged on `extra-values` 02's commit once CI passes there at both ends (as U23 and U28); 02 makes no
tag and pushes nothing; SI adopts `v0.5.0` (`extra-values` U5); and SI's addendum, by anchor. Its
title is unchanged: G4's reading, "`v0.3.0` or later", admits `v0.5.0`.

The text already there stays as it is, and the row's diff is the row as it was with its sentence
added. **G1, G2 and G3 are unchanged.** That campaign stays closed. Whether G4 already holds (SI
pinned `v0.4.0` at its `1b1ca6d`) is not this prompt's to judge: record what you read as an
observation.

### 2.6 The issue

Close `[01-a-new-spec-field-moves-every-spec-guard-digest]`: move its entry from this board's §3 to
§4 with a `**Closed (date, 02):**` line naming the addenda that carry the edit and the release
check that probes it; delete its row from `docs/OPEN_ISSUES.md`, and correct the count (4) and the
date there.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **Additive documents.** Everything under `docs/` is additive (`CLAUDE.md` rule 6). An addendum
   that rewrites a line of 07a's or of an earlier addendum fails acceptance. `git diff` of each
   file under `docs/adoption/` shows `+` lines only.
2. **A name or link that does not exist.** Check every module, name, file, anchor and contract row
   that the README, `PROVENANCE.md` and the addenda mention: names by importing them in `venv/`,
   anchors by finding the heading by GitHub's rule. Contract §9.8's heading is "9.8 `extra-values`
   prompt 01"; derive its anchor, and say how. Each new addendum's own anchor is derived the same
   way.
3. **The tag does not exist yet.** The README, the addenda and the gate name `v0.5.0` as of the
   tag. Nothing may say it is tagged.
4. **No client is re-measured beyond §1.1.** Re-run §1.1's measure yourself, read-only through
   `git` (a script of your own in the scratchpad, run with `python -I`, that reads `git show` and
   imports nothing of a client), at the commits §1.1 names and at the `HEAD`s you read, and record
   it. If a client at the `HEAD` you read passes `extra_values`, builds a `Record` positionally, or
   walks a spec's fields anywhere but its guard, stop. Every client citation an addendum makes is
   checked with `git show <commit>:<path>` before it is written.
5. **The guard's edit is shown, not run on a client.** Its effect is shown on the neutral registry
   and on hand-built specs in the two wheels (§1.2), never by importing a client's code (README §5
   rule 5). Quote the clients' `plain` from `git show` and say it is the recipe's.
6. **Offline only.** Every venv and the build are `--offline`. A pin, or the build backend, that
   does not resolve offline is a stop.
7. **`venv/`'s metadata.** After §2.1, `pip show datastorekit` in `venv/` still says `0.4.0`.
   Reinstall it offline from the repository root, **without** `--no-build-isolation`: `uv pip
   install --offline --no-deps --python venv/bin/python -e .`, delete the `datastorekit.egg-info/`
   it writes, and run the suite in `venv/` again. Nothing else is built in the checkout.
8. **No Ray.** This prompt starts no Ray (README §5 rule 7).
9. **U5's wording.** "May stay or move" is permission, not advice. No document says SGK or CPBH
   should or should not move. The guard's edit is a fact of what a move needs; anything recommended
   is marked **Advice:**, as the checklists' convention requires.
10. **Run from the right place.** Every scratch-venv command runs with its export, or a directory
    outside the repository, as the working directory. Print `datastorekit.__file__` once in each
    venv and record it.
11. **The package names no client.** The guards cover `datastorekit/`, which 02 does not touch.

---

## 4. Verification

1. **The suite.** In `venv/`, `Ran 538 tests … OK` before and after, with `pip show` saying `0.5.0`
   after. Also at the high end: a fresh offline scratch venv (Python 3.13.16, `ray==2.55.1`,
   `sqlalchemy==2.0.46`, `setuptools`) with a `git archive` of your tree installed editable
   (`--no-deps --no-build-isolation`) gives `Ran 538 tests … OK`. Record the `ResourceWarning`
   lines at each end: 0 in `venv/`; 0, 2 or 4 at the high end, which is timing.
2. **The checks.** `compare_ported_tests.py` exits 0 with "20 module(s) … 1 test(s) declared not
   ported"; `black --check datastorekit docs` leaves 79 files unchanged; the guards pass (they are
   in the suite).
3. **The release check**, as §1.2. Build from clean `git archive`s of your tree and of `v0.4.0`,
   never in this checkout, and install each at the high pins, offline. Record the wheels' names,
   sizes, entry counts and SHA-256s, the release's file list, `METADATA`'s lines, the `RECORD`
   comparison, each check of §1.2's run with its output, and the probe script. `git status` shows
   no `build/`, `dist/` or `*.egg-info` afterwards.
4. **The documents.** List every remaining `v0.4.0` in `README.md`, `PROVENANCE.md` and
   `docs/adoption/*.md`, each with why it stays. Confirm `git diff` of the four files under
   `docs/adoption/` has no `-` line, and that `docs/client-contract.md` and
   `docs/extraction-verification.md` are unchanged.
5. **The breakage record.** Each a change exactly as applied in a scratch export, with what failed.
   None is committed. Check each diff with `git apply --check` and `-R --check` as recorded.
   - **(a)** `pyproject.toml`'s version left at `0.4.0`: the `METADATA` and
     `importlib.metadata.version` assertions fail, naming `0.4.0`.
   - **(b)** the `exclude` line removed from `pyproject.toml`: the wheel lists files under
     `datastorekit/tests/`, and `import datastorekit.tests` succeeds.
   - **(c)** the wheel built from `git archive v0.4.0` with only its version set to `0.5.0`: its
     `METADATA` says `0.5.0`, but the `RECORD` comparison shows no line differing; `InventorySpec`
     has six fields; and the guard probe's "differs from `v0.4.0`" fails. The check must catch a
     version number with no change behind it.
6. **The clients.** Record each client's `HEAD` and `git status --short`, and RunRegistryKit's, at
   the start and the end. None is written, run, imported or opened.

---

## 5. Acceptance

1. `pyproject.toml` says `0.5.0`, and nothing else in it changed.
2. `README.md` and `PROVENANCE.md` are as §2.2 and §2.3 say, and every name in them exists.
3. Each of the four files under `docs/adoption/` has its italic line and its addendum, per §2.4,
   and no line of it is rewritten. SI's addendum states each item of §2.4 for SI, and SGK's and
   CPBH's state the guard's edit, each client citation true at the commit it names.
4. The extraction board's G4 is as §2.5 says, and G1, G2 and G3 are unchanged.
5. The issue is closed as §2.6 says.
6. §4.1–§4.6 hold.
7. **The records**, in the same commit:
   - the log `logs/02-release-v0.5.0.md`, per README §5.1. Besides its sections it has the release
     check, the documents' check (§4.4), every name and link checked (hazard 2), §1.1's measure
     re-run (hazard 4), (a)–(c), each addendum's supersession table, and the clients at the start
     and the end;
   - this board: §1's row for 02, the header, and §3/§4;
   - this campaign's README: its header and §2's row for 02;
   - `docs/OPEN_ISSUES.md`, per §2.6;
   - `prompts/INDEX.md`: the campaign's line.

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 538, in any venv.
- The release check fails in a way (a)–(c) do not explain.
- §1.1's measure, re-run, differs as hazard 4 says.
- An addendum cannot say what it must without rewriting a line already in its file.
- Anything would change a file under `datastorekit/`, `docs/client-contract.md`,
  `docs/extraction-verification.md`, `docs/extraction/`, the workflow, or any file not in §7.
- Anything would push, make or move a tag, download, start Ray, or write, run, import or open
  anything of a client or of RunRegistryKit.

---

## 7. What this prompt changes, and what it does not

- **Files it changes:**
  - `pyproject.toml`, `README.md` and `PROVENANCE.md`;
  - `docs/adoption/README.md`, `secondarygwkit.md`, `champbh.md` and `stochasticinstantons.md`,
    by addition only;
  - the extraction board's §2 (G4), per §2.5;
  - the log, this board, this campaign's README (its header and §2's row for 02),
    `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.
- **It changes nothing else:** no file under `datastorekit/`; not `docs/client-contract.md`,
  `docs/extraction-verification.md`, `docs/extraction/`, the workflow, `CLAUDE.md`, `LICENSE` or
  `.gitignore`.
- **It touches no client repository, and not RunRegistryKit.**
- **It makes no tag and pushes nothing.**

---

## 8. After 02

The campaign closes when `v0.5.0` is tagged on 02's commit after green CI. The orchestrator records
that on this board and on the extraction board's G4, closes the campaign in its header, README and
`prompts/INDEX.md`, in a records commit of its own, and pushes it with the user's approval. It then
gives the user:
- **for SI's pin prompt**: the tag object and commit, the SI addendum's anchor, and README §0.2's
  points, to report back to the SI session;
- **for SGK and ChamPBH**: their addenda's anchors, saying that each may stay on `v0.4.0`, and that
  a move needs the guard's one condition;
- **for RunRegistryKit**: that its `docs/adoption/README.md` §6 recipe needs the same condition, in
  a campaign of that repository's own.

If SI's adoption finds a difference from what its addendum says, it comes back to this repository as
a defect, opened on this board (README §7).
