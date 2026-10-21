# extra-values campaign — implementation state

**Last updated:** 2026-10-21 · **Status: IN PROGRESS — 1 of 2 prompts written (01), 1 landed (01,
`5475cef`, reviewed); U2 the user's ruling 2026-10-21; U1, U3–U5 taken 2026-10-21, as
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
| 01 | [A spec counts more than one value table](01-a-spec-counts-more-than-one-value-table.md) | `extra_values` and `extra_value_counts` (U1); the `ENCODING_FORMAT` comment (U2); the neutral client's `TraceMark`, witness, `NEUTRAL_FORMAT` 2 and golden (U3); the new test module and amended literals (U4); contract §9.8 | ✍️ yes, 2026-10-21 | ✅ 2026-10-21; reviewed | `5475cef` | [log](logs/01-a-spec-counts-more-than-one-value-table.md) |
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

**Orchestrator review of prompt 01 (2026-10-21).** Dispatched from `3e6d550` to one Opus
subagent, with the note's five corrections and its additions. Reviewed against its commit
`5475cef`, with nothing landed after it. **Every check of the note's §3 passed**, and acceptance
1–3 are met. No stop condition fired. Nothing was pushed by this campaign, and the tags are
`v0.1.0` to `v0.4.0` only.

*At dispatch.* The tree was clean, one worktree, at `3e6d550`; `origin/main` `38ebb9f` by
`git ls-remote`, at writing and at the review. The suite gave `Ran 530 tests … OK` in `venv/` (0
`ResourceWarning` lines), the port check exited 0, and `black --check datastorekit docs` left 78
files. No Ray process was up, and `RAY_ADDRESS` was unset. While writing the note the orchestrator
built a prototype of §2.1–§2.6 from the prompt alone in a scratch export (538 at both ends), which
reproduced the planner's witness and format-2 golden to the byte, and ran breakages (a)–(i) on it.
It found that `fill_required` knows only the neutral schema, so the wider registry's rows must be
added after it, with the full store's shard keys (correction 1); that most breakages fail more
tests than §4.4 names, which is not a stop (correction 2); that the brief is to be read through
`git` (correction 3); that 0, 2 or 4 `ResourceWarning` lines at the high end are timing
(correction 4); and line readings (correction 5). The clients, SGK `031bcb4`, CPBH `7055532` and SI
`f5f395b`, were clean and unchanged at writing, at dispatch and at the review.

*The checks.*
1. **Scope.** `5475cef` touches the prompt's §7 files only: under `datastorekit/`, three `A` lines
   (the witness, the golden, the test module) and ten `M`. The diff over `pyproject.toml`,
   `README.md`, `PROVENANCE.md`, `docs/adoption/`, `docs/extraction/`,
   `docs/extraction-verification.md`, `.github/`, `datastorekit/SQL/`, `store_reader.py` and the two
   earlier data files is empty; `docs/OPEN_ISSUES.md` is untouched. `git status --short --ignored`
   is as at dispatch.
2. **The change, by reading.** Both fields last and defaulted by `default_factory`; `as_json`'s
   fifth key only when the mapping is not empty; `canonical_json`, `identity`, `__hash__` and
   `dependencies()` unchanged; one inner function, `_count_values`, counting `values` and then each
   extra table in sorted order, with today's `orphan-value` text; the refusal in
   `inventory_classes` alone, in §2.1 item 4's words and in its docstring. The diff of
   `store_fingerprint.py` is §2.2's paragraph, word for word. The module docstring names no
   client.
3. **The neutral client.** Its code in the five client and fixture files is the orchestrator's
   prototype line for line; the differences are comments and docstrings only (the agent's D6, D9).
4. **The reproductions.** The witness, recaptured in `venv/` from the commit's export, is
   byte-identical to the committed file (SHA-256 `971ec253…c07d196`). The log's golden script, run
   on the commit's export in `venv/` and in the review's own offline venv (3.13.16 / 2.55.1 /
   2.0.46), wrote files byte-identical to the committed golden at both ends: digest
   `524cefd4…14a`, file `848fe4c9…fb8`, the planner's.
5. **The tests, by reading.** Eight tests, one per item of U4, each store in a `tempfile` directory,
   with a `tearDownModule` asserting Ray is not initialised. Correction 1 is applied without
   changing `fill_required`; test 1 reads the format-1 golden by a name built from
   `ENCODING_FORMAT`; test 7 matches both names and builds its spec when the hook is called. The
   amended literals are as §2.6, and the port check confirms no assertion call moved. The module
   imports `NEUTRAL_FORMAT` alone from `test_store_fingerprint` (D2), no `Test*` class.
6. **The suite.** `Ran 538 tests … OK` in `venv/` (0 `ResourceWarning` lines) and in the review's
   high-end venv with the commit's export installed editable (4 lines, two warnings of the kind
   correction 4 names). The port check: "OK: 20 module(s) … 1 test(s) declared not ported";
   `black --check datastorekit docs`: 79 files.
7. **The breakages.** (a)–(i) extracted from the log, each passing `git apply --check` and, once
   applied, `-R --check`, in its own export, and the four modules run (91 tests): (a) 68 failures,
   test 1 among them; (b) 10; (c) 1 error, test 4; (d) 8 failures and 2 errors; (e) 11 and 2; (f) 6
   and 1; (g) test 7; (h) test 7; (i) `test_value_tables_are_only_counted` alone. Each as the log
   records, and each covering the tests correction 2's table names.
8. **The documents.** The contract's head line follows §9.7's; §9.8 follows §9.7 in §9's form,
   with four rows as §2.7 and the `ENCODING_FORMAT` row in §2.2's words; its `path:line` citations
   were read at the commit and hold; its relative link resolves. Its diff is `+` lines only.
9. **The records.** The log is in §5.1's form, with the witness diff, the golden's script, the
   nine breakage diffs, the names checked against the vocabulary, and the clients at the start and
   the end. The board, README, `prompts/INDEX.md` and the index (4) are as acceptance 3 asks.
10. **Nothing left behind.** No Ray process; seven tags; `origin` unchanged.

*Residue fixed in the review's records commit.* "this commit" → `5475cef` in the log, the board
and the README; "reviewed" for 01 here, in README §2 and in `prompts/INDEX.md`; the notes line.
The heading of the log's §1.1 gave `store_inventory.py` as "+55 −16", counted before the agent's
D11 reflow; the commit's numstat is **+57 −18**, and the heading now says so (the agent reported
this itself).

*Observations, none an issue.* The agent's four (log §6) stand. The agent made its own constraints
file from the cache; it did not read the orchestrator's scratch.

**Legend.** ✍️ written · ⏸ held, with what it waits on · ⬜ not written / not landed ·
✅ landed.

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`3e6d550`),
used for 01.

## 2. Gates outside this repository

None of this campaign's own. SI's pin prompt waits on the tag (README §7). When it is made, its tag
object, its commit and the SI addendum are given to the user.

## 3. Active and unresolved issues

No issue is held on this board (2026-10-21: prompt 01 opened none).

## 4. Resolved issues

None yet.
