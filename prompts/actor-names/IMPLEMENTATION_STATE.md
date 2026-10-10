# actor-names campaign — implementation state

**Last updated:** 2026-10-10 · **Status: IN PROGRESS — 1 of 2 prompts written (01), 1 landed (01,
this commit, not yet reviewed); U1–U3 taken 2026-10-10, as recommended; 02 is written after 01's
review.**

**Campaign:** [`README.md`](README.md) ·
**Owns:** `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]`, closed by 01 on the
[extraction board](../extraction/IMPLEMENTATION_STATE.md) §4 ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) §1.3

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

### Decisions

**Put to the user (README §6.2), taken 2026-10-10:**

| Decision | Recommendation | Status |
|---|---|---|
| **U1** how a closed pool releases its names | `ray.kill` each actor at the end of `__exit__` and of `_close_refused_open`; a closed flag; the names unchanged | **taken** 2026-10-10 |
| **U2** the stand-in pool | stands in `ray.kill`; reserves names per cluster until killed; a killed handle's calls raise; always on | **taken** 2026-10-10 |
| **U3** the release | `v0.2.2` by 02, which the clients adopt in place of `v0.2.1` | **taken** 2026-10-10 (needed by 02) |

## 1. Prompts

| # | Prompt | Covers | Written? | Landed? | Commit | Log |
|---|---|---|---|---|---|---|
| 01 | [A closed pool releases its actor names](01-a-closed-pool-releases-its-actor-names.md) | the kill at `__exit__` and on a refused open, and the closed flag (U1); the stand-in's `ray.kill` and names (U2); a test module; the smoke script's step N reversed and a collision step; contract §9.3; a dated subsection of the verification document; closes the issue | ✍️ yes, 2026-10-10 | ✅ 2026-10-10; not yet reviewed | this commit | [log 01](logs/01-a-closed-pool-releases-its-actor-names.md) |
| 02 | Release `v0.2.2` (planned) | the version, `README.md`, `PROVENANCE.md`, adoption addenda; the tag after green CI (U3) | ⬜ | ⬜ | — | — |

**Legend.** ✍️ written · ⏸ held, with what it waits on · ⬜ not written / not landed ·
✅ landed.

**Orchestrator notes:** none yet.

## 2. Gates outside this repository

None of this campaign's own. The extraction campaign's G2–G4 are recorded on its board (README §7).

## 3. Active and unresolved issues

No issue is held on this board (2026-10-10). The issue this campaign owned was held on the
extraction board's §3, with its measurement; 01 closed it there, and §4 below points to it.

## 4. Resolved issues

- **[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]**: **closed** 2026-10-10 by 01
  (this commit; [log 01](logs/01-a-closed-pool-releases-its-actor-names.md)). Its entry, with the
  measurement, the fix and how it was verified, is at the head of the
  [extraction board](../extraction/IMPLEMENTATION_STATE.md)'s §4, which opened it.
