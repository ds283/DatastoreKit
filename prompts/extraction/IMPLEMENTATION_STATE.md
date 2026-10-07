# extraction campaign — implementation state

**Last updated:** 2026-10-07 · **Status: IN PROGRESS — 1 of 7 prompts written (01), 1 landed (01).**
G1 holds: the import commit is SGK `6f7f291`. The user took U2–U5 as recommended on 2026-10-07
(README §6.2).

**Campaign:** [`README.md`](README.md) ·
**Source:** SecondaryGWKit's `Datastore/` layer at the import commit `6f7f291` (G1) ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) §1.1

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

### Decisions

**Made by the user, 2026-10-07 (README §6.1):**

| Decision | Decided |
|---|---|
| **D1** | Extract the layer as a separate, reusable component |
| **D2** | `Datastore` / `ShardedPool` first; `RayWorkPool` is a separate unit of work |
| **D3** | A public GitHub repository, `ds283/DatastoreKit` |
| **D4** | ChamPBH's stores are rebuilt on adoption, not migrated |

**Put to the user (README §6.2):**

| Decision | Recommendation | Status |
|---|---|---|
| **U1** name | DatastoreKit / `datastorekit` | applied at set-up; changeable until 01 lands |
| **U2** history | fresh import plus `PROVENANCE.md` | **taken** 2026-10-07 |
| **U3** SGK layer freeze from G1 to G2 | freeze | **taken** 2026-10-07; in force from SGK `b510bc9` (its `CLAUDE.md`, "The datastore layer is frozen") |
| **U4** distribution | pinned git tag in each client's `requirements.txt` | **taken** 2026-10-07 |
| **U5** module names | keep SGK's through this campaign | **taken** 2026-10-07 |
| **U6** supported range and CI | Python ≥ 3.12; GitHub Actions at both ends | open |
| **U7** licence | Apache 2.0 | applied at set-up; changeable |

---

## 1. Prompts

| # | Prompt | Covers | Written? | Landed? | Commit | Log |
|---|---|---|---|---|---|---|
| 01 | [Import the layer](01-import-the-layer.md) | package, 15 files and 2 tools, the two internalised dependencies, 88 tests, import guard | ✍️ yes, 2026-10-07 | ✅ 2026-10-07 | `8bc60a5` | [log](logs/01-import-the-layer.md) |
| 02 | The neutral test client | `docs/client-contract.md`, the test client, the stand-in pool | ⬜ | ⬜ | — | — |
| 03 | Port the write-path tests | 129 tests | ⬜ | ⬜ | — | — |
| 04 | Port the schema and inventory tests | 175 tests; the package guard | ⬜ | ⬜ | — | — |
| 05 | Supported versions and CI | `pyproject.toml` ranges, both ends, Actions; tag `v0.1.0` | ⬜ | ⬜ | — | — |
| 06 | Version-keyed lookups | `key_on_version`; tag `v0.2.0` | ⬜ | ⬜ | — | — |
| 07 | Close-out and adoption handover | `docs/adoption/` checklists; verification document | ⬜ | ⬜ | — | — |

**Legend.** ✍️ written · ⏸ held, with what it waits on · ⬜ not written / not landed ·
✅ landed.

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`bd9f461`),
used for 01.

**Orchestrator review of prompt 01 (2026-10-07).** Dispatched from `bd9f461` to one Opus
subagent, with the note's §0 corrections and additions. Reviewed against its commit `8bc60a5`,
with nothing landed after it. **Every check of the note's §3 passed**, and acceptance 1–3 are met.
No stop condition fired, and the agent ran its suite in the foreground.

*At dispatch.* The note's gate held at `bd9f461`. The tree was clean, and the only worktree was
this checkout. `venv/` did not exist. SGK's frozen files were unchanged from `6f7f291` to SGK
`HEAD` (`b510bc9`), and no Ray process was up.

*The checks.*
1. **Scope.** `8bc60a5` touches 38 files: 35 new, the board, `prompts/INDEX.md` and the index. No
   `venv/`, `*.egg-info` or scratch file.
2. **E1, the files.** `git ls-files datastorekit` gives the prompt's §2.3 files under their
   names, the two empty `__init__.py`s, `defaults.py`, `_timing.py` and the guard: 31 files.
3. **E2, by running.** `compare_with_source.py` exits 0 over 30 files: D-imp −50/+50, D-str
   −4/+4, D-tool −26/+22, D-root −8/+6, D-int −222/+11, D-fmt −1/+0 (one blank line beside the
   removed constants), unclassified 0. Python 3.12.15, `ray==2.43.0`, `sqlalchemy==2.0.39`,
   `black==25.1.0`.
4. **E2, by reading.** The check applies each class to the SGK source as a transformation, runs
   `black` 25.1.0 (it exits 2 under any other version), and requires the package file to equal
   the result byte for byte. This is stricter than the note's token-for-token recommendation.
   - D-imp maps only the module path of an `ast`-found import, at any depth, and only to a
     module that exists.
   - D-str maps a dotted path only as the whole literal, quoted inside a literal, or as the module
     of an import inside a literal, and only to an existing module or a top-level name of one.
   - D-tool and D-root are exact substitutions, restricted to the files they name.
   - D-int rebuilds the module from the named definitions and the imports they use.
   - No rule names a line number.
5. **E3, the check bites.** (a)–(e), replayed from the log, each exit 1 naming the line
   (`ShardedPool.py:953`, `schema.py:52`, `Datastore.py:155`, `shard_paths.py:101`,
   `shard_key_audit.py:19`). The orchestrator's own, `DEFAULT_STRING_LENGTH = 255`, exits 1 naming
   `defaults.py:6`. The tree was clean after each.
6. **E4, the tests.** `Ran 90 tests … OK`. Per module, the set of `Class.test_name` equals SGK's
   at `6f7f291` (7, 4, 10, 22, 26, 5, 3, 11). Read in full: the D-tool and D-root hunks. Every
   subprocess test still runs from its unrelated `cwd` with `PYTHONPATH` removed, and still asserts
   what it did.
7. **E5, isolation.** From the scratchpad with `PYTHONPATH` unset, the four package imports
   succeed, and `import Datastore` raises `ModuleNotFoundError`. The guard walks every module with
   `ast`, at any depth, and takes a relative import as the package.
8. **E6, the pins.**
   - `key_id` at `ShardedPool.py:3561`: **no test fails**, as the log says.
   - `import numpy` in `store_reader.py`: the guard's first test fails.
   - Uninstalling the package: 19 failures, every subprocess test of the three tool modules.
   - After `pip install -e .`, the suite is 90 OK again.
9. **E7, the records.** The log has every section of README §5.1, `pip freeze`, the check's
   output, the D-tool list, the counts (0 → 90; SGK 88), and §4.6's places for the four inherited
   issues. `PROVENANCE.md` has the prompt's §2.8 items, with the right subject line. `black
   --check` is clean on `datastorekit/` and `docs/extraction/`.

*Where the note was wrong, and the agent right.*
- `_timing.py` also needs `from traceback import print_tb`, which `WallclockTimer.__exit__` uses.
  The note said `time` was the only import.
- `config/defaults.py` is 203 lines, not one; only `DEFAULT_STRING_LENGTH` is taken.

*Issues.*
- The agent opened `[01-package-prose-names-sgks-layout]`, as the note expected.
- It also opened `[01-ported-tests-use-sgk-table-names]`. It is a real finding under `CLAUDE.md`
  and rule 4, and it is kept.
- **The review opens a third**, `[01-no-ported-test-pins-the-shard-key-assignment]`. The prompt
  called the `key_id` result "a finding for 03". The log recorded it only under its observations,
  and the defect it would catch is the one that motivated the campaign. The index goes to 7.

*Handed on to 02's author.* `compare_with_source.py` lists a file under `datastorekit/` that is
neither in `FILES` nor in `NEW_FILES` as "NOT ACCOUNTED FOR", but still exits 0. The prompt
required failure only for a missing file. 02 adds the first files with no source, and is the
natural place to make an unaccounted file a failure. Recommended, not opened.

*Residue fixed in this follow-up:* "this commit" → `8bc60a5` in the log, the board and
`prompts/INDEX.md`; README §2's status for 01; this paragraph and the notes line.

## 2. Gates outside this repository (README §7)

| Gate | Status |
|---|---|
| **G1**: SGK `datastore-generic-followup` closed; the import commit fixed | ✅ 2026-10-07: closed at `6f7f291` (03 landed as `086c81a`); the import commit is `6f7f291` |
| **G2**: SGK adopted `v0.1.0`, fingerprint reproduced | ⬜ |
| **G3**: CPBH adopted `v0.2.0` | ⬜ |
| **G4**: SI adopted | ⬜ |

## 3. Active and unresolved issues

The issues the layer carries from SGK are indexed in
[`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) §1.2. They stay on SGK's boards, and are out
of scope here (README §1). Log 01 §4.6 records where each one's code is in the package.

- **[01-package-prose-names-sgks-layout]** *(opened 2026-10-07 by prompt 01)*
  - **The defect.** Comments and docstrings in the package, imported unchanged (D-str leaves prose
    alone; README §5 rule 8), still name SGK's layout: `Datastore/…` and `tools/…` paths, dotted
    mentions such as ``Datastore.SQL``, SGK campaign paths (`prompts/…`, `docs/…`) and "the
    repository root". Two sentences describe the `sys.path` bootstrap that D-tool removed, and are
    now false: `tools/sharded_store.py:25-26` ("It puts its own repository root on sys.path, so it
    runs from any directory with no PYTHONPATH.") and `tools/shard_key_audit.py:25-26` ("the
    repository root is put on sys.path below so that the script still runs standalone, from any
    directory, with no PYTHONPATH.").
  - **Measured** (2026-10-07, at `8bc60a5`; comment and string tokens matching
    `Datastore/|tools/|prompts/|docs/|Datastore.<module>|repository root|REPO_ROOT|ObjectFactories|RunRegistry|main.py|config.defaults|utilities.py`,
    the two internalised modules' provenance docstrings excluded): **101 lines in 19 files**.
    `SQL/ShardedPool.py` 27, `SQL/Datastore.py` 12, `SQL/schema.py` 10, `store_inventory.py` 8,
    `replication.py` 6, `store_reader.py` 5, `tests/test_shard_key_audit_copy.py` 5,
    `SQL/factory_base.py` 3, `tools/shard_key_audit.py` 3, `tests/test_shard_key_audit_refusals.py`
    3, `tests/test_shard_paths.py` 3, `tests/test_sharded_store_script.py` 3,
    `tests/test_shardedpool_shard_paths.py` 3, `contract.py` 2, `tools/sharded_store.py` 2,
    `tests/test_delete_store.py` 2, `tests/test_shard_file_name.py` 2, `shard_paths.py` 1,
    `tests/test_copy_move_store.py` 1. Reproducible with the pattern above.
  - **Impact.** Documentation only: no behaviour. A reader of the package is pointed at files and
    campaigns that do not exist here, and two docstrings misdescribe how the tools find the package.
  - **Next step.** Rewrite the prose once rule 8 lifts (after 05), so that 01–05's equivalence check
    stays mechanical. Unassigned.
- **[01-ported-tests-use-sgk-table-names]** *(opened 2026-10-07 by prompt 01)*
  - **The defect.** The ported fixture and tests, imported unchanged (README §5 rule 6), use SGK's
    table names: `tests/shard_store_fixtures.py:25-27` (`KEY_TYPE = "wavenumber"`,
    `REPLICATED = ["version", "wavenumber"]`, `SHARDED = {"GkSource": "k"}`);
    `tests/test_shard_key_audit_copy.py` (3 lines) and `tests/test_shard_key_audit_refusals.py`
    (9 lines) create a `wavenumber` table and a `wavenumber_serial` column; and one comment,
    `tools/shard_key_audit.py:188` (`e.g. "wavenumber"`). `CLAUDE.md` says the package names no
    client table.
  - **Impact.** No behaviour: the names are data in hand-built test stores. But 04's vocabulary guard,
    drawn from the clients' registries, would find them, and README §2 does not say whether the 88
    move onto the neutral client's names.
  - **Next step.** 02 or 04 decides: re-fixture these tests onto the neutral client's names, or
    exempt them from the vocabulary guard with a reason. Unassigned.
- **[01-no-ported-test-pins-the-shard-key-assignment]** *(opened 2026-10-07 by the orchestrator's
  review of 01)*
  - **The defect.** No test in the suite reaches `ShardedPool._assign_shard_keys`
    (`datastorekit/SQL/ShardedPool.py:3505`). Binding `"key_id"` in place of `"key_serial"` in its
    insert (`:3561`) fails none of the 90 (log 01 §4.4, replayed at the review). A probe raising
    at the method's first line also fails none.
  - **Impact.** That binding is the shard-key bug of README §0: the saved shard map could differ
    from the one in memory after a reopen. It was fixed in SGK (`2610abe`) and SI (`20d9a61`), and
    was still in CPBH on 2026-10-07. The package carries the fix, but nothing here would catch its
    return.
  - **Next step.** 03 ports the write-path tests onto the stand-in pool. Its author checks whether
    any of the 129 reaches `_assign_shard_keys` through the package. If none does, 03 adds one
    that writes a sharded object, reopens the store, and compares the shard map on disk with the
    one in memory, and the `key_id` mutation is one of its breakages. Unassigned until 03 is
    written.

## 4. Resolved issues

None.
