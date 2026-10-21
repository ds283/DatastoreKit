# extra-values campaign — implementation state

**Last updated:** 2026-10-21 · **Status: IN PROGRESS — 1 of 2 prompts written (01), 1 landed (01,
this commit; not yet reviewed); U2 the user's ruling 2026-10-21; U1, U3–U5 taken 2026-10-21, as
recommended; 02 is written after 01's review.**

**Campaign:** [`README.md`](README.md) ·
**Owns:** no issue. It carries out the user's request of 2026-10-21, from SI's brief (README §0) ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md)

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

### Decisions

**Put to the user (README §6.2), U1–U5 taken 2026-10-21:**

| Decision | Recommendation | Status |
|---|---|---|
| **U1** the fields, and how they are read | `InventorySpec.extra_values: Mapping[str, str]` (table → column), `Record.extra_value_counts: Mapping[str, int]` (table → count, 0 where none), both last and defaulted empty; `as_json`'s fifth key only when not empty; one `GROUP BY` per table per shard through one inner function shared with `values`, orphans `orphan-value`; one refusal (`values` also in `extra_values`) in `inventory_classes`, none at construction | the change: **the user's request** 2026-10-21; its form: **taken** 2026-10-21, as recommended |
| **U2** `ENCODING_FORMAT` | stays 1; a paragraph after the comment's last sentence says item 1 is read by the rule above it, and why an omitted-when-empty field is not a bump; contract §9.8 states it | **the user's ruling** 2026-10-21 |
| **U3** the neutral client declares it | `TraceMark` under `Trace`, declared in Trace's spec, written for `trace-one` and two rows in the full store; witness `schema_at_extra-values-01.json`; `NEUTRAL_FORMAT` 2 and golden `store_fingerprint-neutral-2-encoding-1.json` beside the format-1 golden, which is kept as the compatibility test; the test literals that name what changed | **taken** 2026-10-21 |
| **U4** the tests | `tests/test_inventory_extra_values.py`, eight tests: compatibility against the format-1 golden, counts, two tables, orphans, replicated divergence, the fingerprint, the refusal, `dependent_tables`; `build_real_store` taking `factories`; no Ray | **taken** 2026-10-21 |
| **U5** the shape, release and adoption | two prompts; `v0.5.0`, minor (added API); SI adopts it in a pin prompt of its own; ChamPBH and SGK need nothing, may stay, recorded fingerprints valid | **taken** 2026-10-21 (needed by 02) |

## 1. Prompts

| # | Prompt | Covers | Written? | Landed? | Commit | Log |
|---|---|---|---|---|---|---|
| 01 | [A spec counts more than one value table](01-a-spec-counts-more-than-one-value-table.md) | `extra_values` and `extra_value_counts` (U1); the `ENCODING_FORMAT` comment (U2); the neutral client's `TraceMark`, witness, `NEUTRAL_FORMAT` 2 and golden (U3); the new test module and amended literals (U4); contract §9.8 | ✍️ yes, 2026-10-21 | ✅ 2026-10-21; not yet reviewed | this commit | [log](logs/01-a-spec-counts-more-than-one-value-table.md) |
| 02 | Release `v0.5.0` (planned) | the version, `README.md`, `PROVENANCE.md`, adoption addenda (SI's saying what it does; ChamPBH's and SGK's that nothing changes); the tag after green CI (U5) | ⬜ | ⬜ | — | — |

**Planning note (2026-10-21, at `38ebb9f`).** The brief's five checks hold (README §0.1). One
finding departs from it: `test_every_declaration_field_is_in_use` requires the neutral registry to
use every `InventorySpec` field, so the neutral client must declare the new one, and its format and
golden move on (README §0.2, point 2; U3). A prototype of U1–U4 in a scratch export gave
`Ran 538 tests … OK` at both ends (Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39 in `venv/`;
3.13.16 / 2.55.1 / 2.0.46 in an offline scratch venv), 0 and 4 `ResourceWarning` lines; the
format-1 golden reproduced through a spec that does not declare the field; a new golden digest
`524cefd4…`, equal at both ends; a witness whose diff from the current one is additions only. The
guards, the port check and `black` passed. Nothing was committed, and Ray was not started. The
clients at planning: SI `f5f395b`, ChamPBH `7055532`, SGK `031bcb4`, each clean and on `v0.4.0`.

**Prompt 01 (2026-10-21).** `InventorySpec.extra_values` and `Record.extra_value_counts` as U1
says, the counting one inner function shared with `values`, the refusal in `inventory_classes`
alone; `ENCODING_FORMAT` 1 with the paragraph of U2; the neutral client's `TraceMark` (U3); eight
tests in `tests/test_inventory_extra_values.py` and the amended literals (U4); contract §9.8, by
addition. The witness (`971ec253…c07d196`) and the format-2 golden (digest `524cefd4…14a`, file
`848fe4c9…fb8`) are the planner's, to the byte, at both ends; test 1 reproduces the format-1 golden
through a spec that does not declare the field. The suite goes from 530 to **538** at both ends;
each breakage (a)–(i) fails the tests §4.4 names, and others as the dispatch note's correction 2
says. No issue was opened. See the [log](logs/01-a-spec-counts-more-than-one-value-table.md).

**Legend.** ✍️ written · ⏸ held, with what it waits on · ⬜ not written / not landed ·
✅ landed.

**Orchestrator notes:** none yet.

## 2. Gates outside this repository

None of this campaign's own. SI's pin prompt waits on the tag (README §7). When it is made, its tag
object, its commit and the SI addendum are given to the user.

## 3. Active and unresolved issues

No issue is held on this board (2026-10-21: prompt 01 opened none).

## 4. Resolved issues

None yet.
