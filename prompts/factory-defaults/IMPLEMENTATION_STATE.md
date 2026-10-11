# factory-defaults campaign — implementation state

**Last updated:** 2026-10-11 · **Status: PLANNED — 1 of 2 prompts written (01), 0 landed; U1–U5 taken
2026-10-11, as recommended; 01 is ready to be dispatched.**

**Campaign:** [`README.md`](README.md) ·
**Owns:** no issue. It carries out the user's ruling of 2026-10-11 (README §0), revisits extraction
U32 in part (U1), and addresses extraction 07a's observation §7.3
(`docs/extraction-verification.md` §8) ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md)

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

### Decisions

**Put to the user (README §6.2), U1–U5 taken 2026-10-11:**

| Decision | Recommendation | Status |
|---|---|---|
| **U1** what the base becomes, and how U32 is recorded | `store`, `validate`, `validate_on_startup` lose `@abstractmethod`, stay static with today's signatures and bare `NotImplementedError`; the base stays an `ABC` with `register` and `build` as its only abstract hooks, so a class defining both instantiates; a dated note on extraction U32, not a rewrite | the change: **the user's ruling** 2026-10-11; its form: **taken** 2026-10-11, as recommended |
| **U2** the tests | a new module of instances, a parameterised factory, the two abstract hooks, the defaults (direct and through the pool), a `cloudpickle` round trip and `_defines`; `ABSTRACT_HOOKS` corrected; the neutral registry unchanged | **taken** 2026-10-11 |
| **U3** Ray | a smoke step I registering instances, run under real Ray at both ends, and once with U1 reverted | **taken** 2026-10-11 |
| **U4** the shape | two prompts: 01 the change, 02 the release | **taken** 2026-10-11 |
| **U5** the release, and who adopts it | `v0.2.3`, patch-level; CPBH and SI adopt it (G3, G4); SGK may stay on `v0.2.2` (G2 "`v0.2.2` or later") | the version: **the user's ruling** 2026-10-11; the rest: **taken** 2026-10-11 (needed by 02) |

## 1. Prompts

| # | Prompt | Covers | Written? | Landed? | Commit | Log |
|---|---|---|---|---|---|---|
| 01 | [The base defaults three hooks](01-the-base-defaults-three-hooks.md) | the base (U1); `test_factory_instances.py` and `ABSTRACT_HOOKS` (U2); smoke step I at both ends (U3); contract §9.5 with its markers; verification §4.8 and §8.1; a note on extraction U32 | ✍️ yes, 2026-10-11 | ⬜ | — | — |
| 02 | Release `v0.2.3` (planned) | the version, `README.md`, `PROVENANCE.md`, adoption addenda; the extraction board's G2–G4; the tag after green CI (U5) | ⬜ | ⬜ | — | — |

**Planning note (2026-10-11, at `460b012`).** The brief's three points of §3 were re-measured, and
hold (README §0.1). A prototype, the three decorators removed and three scratch tests added, gave
`Ran 497 tests … OK` at both ends (Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39 in `venv/`;
3.13.16 / 2.55.1 / 2.0.46 in an offline scratch venv, 0 `ResourceWarning` lines); on the unchanged
tree the three scratch tests error with `TypeError` at instantiation. Through the pool an instance
meets the bare `NotImplementedError` a class meets. Nothing was committed, and Ray was not
started. The clients at planning: SGK `6861a9f` (clean), CPBH `52142d7` (25 untracked entries),
SI `7bb3efd` (clean).

**Legend.** ✍️ written · ⏸ held, with what it waits on · ⬜ not written / not landed ·
✅ landed.

**Orchestrator notes:** none yet.

## 2. Gates outside this repository

None of this campaign's own. The extraction campaign's G2–G4 are recorded on its board (README §7).
When `v0.2.3` is tagged, its tag object and commit are given to the user for CPBH's prompt 07.

## 3. Active and unresolved issues

No issue is held on this board (2026-10-11).

## 4. Resolved issues

None yet.
