# extraction campaign — implementation state

**Last updated:** 2026-10-07 · **Status: PLANNED — 0 of 7 prompts written.** The plan is a draft
for the user's review. Prompt 01 waits on gate G1, and on the user's decisions U2–U5 (README
§6.2).

**Campaign:** [`README.md`](README.md) ·
**Source:** SecondaryGWKit's `Datastore/` layer at the import commit (G1; not yet fixed) ·
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
| **U2** history | fresh import plus `PROVENANCE.md` | open |
| **U3** SGK layer freeze from G1 to G2 | freeze | open |
| **U4** distribution | pinned git tag in each client's `requirements.txt` | open |
| **U5** module names | keep SGK's through this campaign | open |
| **U6** supported range and CI | Python ≥ 3.12; GitHub Actions at both ends | open |
| **U7** licence | Apache 2.0 | applied at set-up; changeable |

---

## 1. Prompts

| # | Prompt | Covers | Written? | Landed? | Commit | Log |
|---|---|---|---|---|---|---|
| 01 | Import the layer | package, 15 files and 2 tools, the two internalised dependencies, 88 tests, import guard | ⏸ waits on G1, U2–U5 | ⬜ | — | — |
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
| **G1**: SGK `datastore-generic-followup` closed; the import commit fixed | ⬜ SGK prompt 03 in progress on 2026-10-07 (uncommitted at `21ee420`) |
| **G2**: SGK adopted `v0.1.0`, fingerprint reproduced | ⬜ |
| **G3**: CPBH adopted `v0.2.0` | ⬜ |
| **G4**: SI adopted | ⬜ |

## 3. Active and unresolved issues

None opened by this campaign. The issues the layer carries from SGK are indexed in
[`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) §1.2. They stay on SGK's boards, and are out
of scope here (README §1).

## 4. Resolved issues

None.
