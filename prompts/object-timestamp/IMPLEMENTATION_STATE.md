# object-timestamp campaign — implementation state

**Last updated:** 2026-10-12 · **Status: PLANNED — 1 of 2 prompts written (01), 0 landed; U1–U6
taken 2026-10-12, as recommended; 01 is ready to be dispatched.**

**Campaign:** [`README.md`](README.md) ·
**Owns:** no issue. It carries out the user's ruling of 2026-10-12 (README §0) ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md)

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

### Decisions

**Put to the user (README §6.2), U1–U6 taken 2026-10-12:**

| Decision | Recommendation | Status |
|---|---|---|
| **U1** the form of the change | `DatastoreObject(store_id, *, timestamp=None)`: keyword-only, stored as `_timestamp`; a read-only `timestamp` property; a docstring saying a factory fills it from the row and the layer never sets or reads it | the change: **the user's ruling** 2026-10-12; its form: **taken** 2026-10-12, as recommended |
| **U2** the version object's `vars()` test | `TestTheVersionObject`'s expected dict (`tests/test_declared_facts.py:643-646`) gains `"_timestamp": None`; nothing else in it changes | **taken** 2026-10-12 |
| **U3** the tests | a neutral replicated stamped class and static factory outside the registry; `tests/test_object_timestamp.py`: the argument and property, the stamp read back through the pool and from every shard, read-only, keyword-only, `cloudpickle` | **taken** 2026-10-12 |
| **U4** Ray | no new smoke step; the script run unchanged under real Ray at both ends | **taken** 2026-10-12 |
| **U5** the shape | two prompts: 01 the change, 02 the release | **taken** 2026-10-12 |
| **U6** the release, and who adopts it | `v0.3.0`, minor (added API, as U36 drew the line); SI adopts it (G4); ChamPBH and SGK may stay on their pins (G3 "`v0.2.3` or later", G2 "`v0.2.2` or later") | **taken** 2026-10-12 (needed by 02) |

## 1. Prompts

| # | Prompt | Covers | Written? | Landed? | Commit | Log |
|---|---|---|---|---|---|---|
| 01 | [The object carries a timestamp](01-the-object-carries-a-timestamp.md) | `object.py` (U1); `TestTheVersionObject`'s dict (U2); the stamped class, `test_object_timestamp.py` (U3); the smoke run at both ends (U4); contract §9.6; verification §4.9 | ✍️ yes, 2026-10-12 | ⬜ | — | — |
| 02 | Release `v0.3.0` (planned) | the version, `README.md`, `PROVENANCE.md`, adoption addenda; the extraction board's G2–G4; the tag after green CI (U6) | ⬜ | ⬜ | — | — |

**Planning note (2026-10-12, at `83068cb`).** The brief's four points of §3 were re-measured
(README §0.1). Points 2–4 hold. Point 1 holds for the layer, but the suite pins `vars()` of the
version object (`tests/test_declared_facts.py:643-646`), which the brief's search excluded (U2). A
prototype, `object.py` changed as U1 recommends and two scratch tests added, gave `Ran 506 tests`
with the two subtests of `TestTheVersionObject` failing and nothing else, at both ends (Python
3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39 in `venv/`; 3.13.16 / 2.55.1 / 2.0.46 in an offline
scratch venv). With that test's dict corrected, it and the scratch tests pass at both ends; a
stamped row's timestamp came back through the pool, from each of three shards, and through a
read-only reopen. Nothing was committed, and Ray was not started. The clients at planning: SGK
`ede4062` (clean), ChamPBH `0e64ef0` (29 entries in `git status --short`), SI `7bb3efd` (3
entries).

**Legend.** ✍️ written · ⏸ held, with what it waits on · ⬜ not written / not landed ·
✅ landed.

**Orchestrator notes:** none yet.

## 2. Gates outside this repository

None of this campaign's own. The extraction campaign's G2–G4 are recorded on its board (README §7).
When the release is tagged, its tag object and commit are given to the user for SI's prompt 08.

## 3. Active and unresolved issues

No issue is held on this board (2026-10-12).

## 4. Resolved issues

None yet.
