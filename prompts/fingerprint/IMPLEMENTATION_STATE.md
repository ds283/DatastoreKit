# fingerprint campaign — implementation state

**Last updated:** 2026-10-14 · **Status: IN PROGRESS — 1 of 2 prompts written (01), 1 landed (01,
this commit; not yet reviewed); U1–U6 taken 2026-10-12 (U1 amended by the user, the rest as
recommended); 02 is written after 01's review.**

**Campaign:** [`README.md`](README.md) ·
**Owns:** no issue. It carries out the user's ruling of 2026-10-12, SGK's D3 (README §0) ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md)

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

### Decisions

**Put to the user (README §6.2), U1–U6 taken 2026-10-12:**

| Decision | Recommendation | Status |
|---|---|---|
| **U1** the module and its functions | `datastorekit/store_fingerprint.py`; `fingerprint_of(inventory, fingerprint_format, taken=None)`, the format a required `int` ≥ 1, positional or by keyword; `compare_fingerprints` and `listing_lines` with SGK's signatures; the helpers private; prose rewritten, SGK's history left out; `canonical_json` imported at module scope | the move: **the user's ruling** 2026-10-12; its form: **taken** 2026-10-12, **amended by the user** from the recommended keyword-only format to a plain signature; SGK rewrites its positional `fingerprint_of(inventory, taken)` |
| **U2** the version | `ENCODING_FORMAT = 1`; `encoding_format` beside the digest, outside the hashed object; a mismatch of either version refused, one entry each (`format`, SGK's verbatim; `encoding`, new); the listing's first line gains ` encoding_format <e>` at its end | **taken** 2026-10-12 |
| **U3** the bump rule | any change that can give the same store, specs and client format a different fingerprint, or change what the comparison or listing reads; eight items, stated beside the constant and in contract §9.7; a bump adds a golden beside the old | **taken** 2026-10-12 |
| **U4** the tests | `tests/test_store_fingerprint.py`, eight tests over the neutral full store; a golden `tests/data/store_fingerprint-neutral-1-encoding-1.json`, keyed on `NEUTRAL_FORMAT` and `ENCODING_FORMAT`; no Ray | **taken** 2026-10-12 |
| **U5** the equivalence check | SGK's five functions extracted by `git show c8a7f14` into scratch, run beside the package's on the neutral store (formats 1 and 6; 27 changed stores); recorded in 01's log; nothing of SGK imported or committed (amends §5 rule 5 for this one read) | **taken** 2026-10-12 |
| **U6** the shape, release and adoption | two prompts; `v0.4.0`, minor (added API); SGK adopts it (its E1, 03, 06), its addendum naming what changes for it; ChamPBH and SI may stay | **taken** 2026-10-12 (needed by 02) |

## 1. Prompts

| # | Prompt | Covers | Written? | Landed? | Commit | Log |
|---|---|---|---|---|---|---|
| 01 | [The fingerprint moves into the package](01-the-fingerprint-moves-into-the-package.md) | `store_fingerprint.py` (U1–U3); `test_store_fingerprint.py` and the golden (U4); the equivalence check (U5); contract §9.7 | ✍️ yes, 2026-10-12, revised for U1 the same day | ✅ 2026-10-14; not yet reviewed | this commit | [log](logs/01-the-fingerprint-moves-into-the-package.md) |
| 02 | Release `v0.4.0` (planned) | the version, `README.md`, `PROVENANCE.md`, adoption addenda (SGK's saying what it must do); the tag after green CI (U6) | ⬜ | ⬜ | — | — |

**Planning note (2026-10-12, at `5f972be`).** The brief's citations into SGK hold at `c8a7f14`,
and `RunRegistry/` is unchanged to SGK's `a5a6f6d`. A prototype module in a scratch export,
compared with a verbatim extract of SGK's five functions run in scratch, gave equal fingerprints at
formats 1 and 6 (adding `encoding_format` only) and equal comparisons on 27 changed stores, at both
ends (Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39 in `venv/`; 3.13.16 / 2.55.1 / 2.0.46 in an
offline scratch venv). With it in the tree the suite gave `Ran 509 tests … OK` at both ends, the
guards included. Three of SGK's tests pin what the change touches (README §0.1): the fingerprint's
key set, its golden, and the listing's first line by word position, which U2's appended field
keeps. Nothing was committed, and Ray was not started. The clients at planning: SGK `a5a6f6d`
(clean), ChamPBH `5bb2be6` (23 entries in `git status --short`), SI `5fb4a1d` (clean).

**Prompt 01 (2026-10-14).** `datastorekit/store_fingerprint.py` holds the source's five functions
and three helpers, changed only as the prompt's §2.1 says (by `ast`: the five helpers equal; the
three functions differ by the format argument and its checks, `encoding_format`, the versions
block and the listing's first line). The golden is the planner's digest, `7656b600…d304`. The
equivalence check against the source's extract gave **0 differences** at both ends, at formats 1
and 6, on the baseline and 37 changed stores (correction 3's 28, and test 2's nine). The suite goes
from 509 to **530** at both ends; each breakage (a)–(j) fails its test, and (f) is equivalent. No
issue was opened. See the [log](logs/01-the-fingerprint-moves-into-the-package.md).

**Legend.** ✍️ written · ⏸ held, with what it waits on · ⬜ not written / not landed ·
✅ landed.

**Orchestrator notes:** none yet.

## 2. Gates outside this repository

None of this campaign's own. SGK's `runregistry-extraction` gate E1 waits on the tag (README §7).
When it is made, its tag object, its commit and the SGK addendum are given to the user. SGK's R1
result (the fingerprint taken both ways) is recorded here when SGK reports it.

## 3. Active and unresolved issues

No issue is held on this board (2026-10-14: prompt 01 opened none).

## 4. Resolved issues

None yet.
