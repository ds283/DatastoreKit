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
| 01 | [Import the layer](01-import-the-layer.md) | package, 15 files and 2 tools, the two internalised dependencies, 88 tests, import guard | ✍️ yes, 2026-10-07 | ✅ 2026-10-07 | this commit | [log](logs/01-import-the-layer.md) |
| 02 | The neutral test client | `docs/client-contract.md`, the test client, the stand-in pool | ⬜ | ⬜ | — | — |
| 03 | Port the write-path tests | 129 tests | ⬜ | ⬜ | — | — |
| 04 | Port the schema and inventory tests | 175 tests; the package guard | ⬜ | ⬜ | — | — |
| 05 | Supported versions and CI | `pyproject.toml` ranges, both ends, Actions; tag `v0.1.0` | ⬜ | ⬜ | — | — |
| 06 | Version-keyed lookups | `key_on_version`; tag `v0.2.0` | ⬜ | ⬜ | — | — |
| 07 | Close-out and adoption handover | `docs/adoption/` checklists; verification document | ⬜ | ⬜ | — | — |

**Legend.** ✍️ written · ⏸ held, with what it waits on · ⬜ not written / not landed ·
✅ landed.

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
  - **Measured** (2026-10-07, at this commit; comment and string tokens matching
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

## 4. Resolved issues

None.
