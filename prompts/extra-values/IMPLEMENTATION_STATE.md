# extra-values campaign — implementation state

**Last updated:** 2026-10-21 · **Status: IN PROGRESS — 2 of 2 prompts written, 2 landed (01,
`5475cef`, reviewed; CI green at both ends, run 39680233763; 02, `f47b9a2`, reviewed, `v0.5.0` ready to
be tagged on it once CI passes there at both ends); U2 the user's ruling 2026-10-21; U1, U3–U5 taken
2026-10-21, as recommended, U5 amended by the user the same day; no issue open
(`[01-a-new-spec-field-moves-every-spec-guard-digest]` closed by 02).**

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
| **U5** the shape, release and adoption | two prompts; `v0.5.0`, minor (added API); SI adopts it in a pin prompt of its own; ChamPBH and SGK may stay, recorded fingerprints valid; **amended**: a move needs one edit to each one's spec guard (README §0.3) | **taken** 2026-10-21 (needed by 02); **amended by the user** 2026-10-21 |

## 1. Prompts

| # | Prompt | Covers | Written? | Landed? | Commit | Log |
|---|---|---|---|---|---|---|
| 01 | [A spec counts more than one value table](01-a-spec-counts-more-than-one-value-table.md) | `extra_values` and `extra_value_counts` (U1); the `ENCODING_FORMAT` comment (U2); the neutral client's `TraceMark`, witness, `NEUTRAL_FORMAT` 2 and golden (U3); the new test module and amended literals (U4); contract §9.8 | ✍️ yes, 2026-10-21 | ✅ 2026-10-21; reviewed; CI green at both ends (run 39680233763) | `5475cef` | [log](logs/01-a-spec-counts-more-than-one-value-table.md) |
| 02 | [Release `v0.5.0`](02-release-v0.5.0.md) | the version, `README.md`, `PROVENANCE.md`, adoption addenda (SI's saying what it does; ChamPBH's and SGK's that nothing they call or hold changes, and the spec guard's one edit); G4's sentence; closes `[01-a-new-spec-field-moves-every-spec-guard-digest]`; the tag after green CI (U5) | ✍️ yes, 2026-10-21, against `c583c56` | ✅ 2026-10-21; reviewed; untagged | `f47b9a2` | [log](logs/02-release-v0.5.0.md) |

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

*CI (2026-10-21).* With the user's approval, `main` was pushed, fast-forwarding `origin/main`
from `38ebb9f` to `dde3201` (`d401e84`, `3e6d550`, `5475cef` and the review's records). The
workflow ran on `dde3201`, [run 39680233763](https://github.com/ds283/DatastoreKit/actions/runs/39680233763),
the first CI run on 01's code: **both ends passed**. `suite (low)`: Python 3.12.15 / Ray 2.43.0 /
SQLAlchemy 2.0.39, SQLite 3.45.1, `Ran 538 tests … OK`, 0 `ResourceWarning` lines, and `black`
"79 files would be left unchanged". `suite (high)`: Python 3.13.16 / Ray 2.55.1 / SQLAlchemy
2.0.46, SQLite 3.45.1, `Ran 538 tests … OK`, 4 `ResourceWarning` lines (two unclosed SQLite
connections reported from SQLAlchemy: timing, the note's correction 4). Nothing is tagged; 02
(`v0.5.0`) is written next, against the tree 01 left.

**Prompt 02 (2026-10-21).** The package is ready to be released as `v0.5.0`: `pyproject.toml`
says `0.5.0`; `README.md` and `PROVENANCE.md` describe it; each of the four files under
`docs/adoption/` gains an italic line at its head and a dated addendum, by addition only (`git
diff` has no `-` line), SI's the note its pin prompt reads, SGK's and ChamPBH's giving the spec
guard's one condition and that the format is not bumped for it; the extraction board's G4 gains a
dated sentence. No line of code changed. The suite is `Ran 538 tests … OK` in `venv/` (0
`ResourceWarning` lines; `pip show` `0.5.0` after the offline reinstall) and at the high end (4
lines, timing). The release check, offline from an export: `datastorekit-0.5.0-py3-none-any.whl`,
26 entries, none under `tests/`; against `v0.4.0`'s wheel two `RECORD` lines differ
(`store_inventory.py`, `store_fingerprint.py`) and 19 are equal; the probe, in the two installed
wheels, gives the prompt's §1.2 in every check, the guard's recipe included. Breakages (a)–(c) fail
the check as §4.5 says. §1.1's measure of the clients, re-run through `git`, reproduces the
prompt's table. `[01-a-new-spec-field-moves-every-spec-guard-digest]` is closed (§4). Nothing was
pushed or tagged, no client or RunRegistryKit was written, run or opened, and Ray was not started.
See the [log](logs/02-release-v0.5.0.md).

**Orchestrator review of prompt 02 (2026-10-21).** Dispatched from `62c69d7` to one Opus
subagent, with the note's three corrections and its additions. Reviewed against its commit
`f47b9a2`, with nothing landed after it. **Every check of the note's §3 passed**, and acceptance
1–7 are met. No stop condition fired. Nothing was pushed or tagged; `origin/main` is `bda6dbc`,
and the tags are `v0.1.0` to `v0.4.0` only.

*At dispatch.* The tree was clean, one worktree, at `62c69d7`; `origin/main` `bda6dbc`. The
baseline was 01's review's (538 in `venv/`, port check 0, `black` 79). While writing the note the
orchestrator built the release wheel and `v0.4.0`'s offline and probed both installed, and built
breakages (b) and (c): (b) 79 entries, 53 under `tests/`; (c) a `0.5.0` wheel with `v0.4.0`'s
`RECORD`. It found that each `v0.4.0` head line is followed by a blank, so k = 5 and 6
(correction 1), and that the `v0.4.0` addenda's statements of each client's pin are now history
(correction 2). The clients (SGK `031bcb4`, CPBH `7055532`, SI `f5f395b`) and RunRegistryKit
(`33a2cd2`) were clean and unchanged at writing, at dispatch and at the review.

*The checks.*
1. **Scope.** `f47b9a2` touches the prompt's §7 files only. The diff over `datastorekit/`,
   `docs/client-contract.md`, `docs/extraction-verification.md`, `docs/extraction/`, `.github/`,
   `CLAUDE.md` and `orchestrator/` is empty; `pyproject.toml`'s is the version line alone.
2. **The release.** Rebuilt offline from `git archive f47b9a2` and `git archive v0.4.0`: 105,087
   and 104,424 bytes, 26 entries each, none under `tests/`; of the 21 `RECORD` lines, the two the
   prompt names differ and 19 are equal. The log's probe (SHA-256 `c2f82e83…`, as the log says),
   run with `python -I` from outside the repository in fresh venvs of each wheel, gave the log's
   output in every field at both versions, `file` aside: seven spec fields against six; a record
   without counts with `v0.4.0`'s keys and canonical line; the hand-built inventory's digest
   `d493e0fe…` in both; the guard's plain digests differing, and equal with the condition; the
   refusal. A fresh import loads no Ray; `import datastorekit.tests` fails; `sharded_store --help`
   exits 0.
3. **The breakages.** (a)–(c) extracted from the log, each passing `git apply --check` and, once
   applied, `-R --check`, and built: (a) a `0.4.0` wheel; (b) 79 entries, 53 under `tests/`; (c) a
   `0.5.0` wheel whose `RECORD` equals `v0.4.0`'s and whose `InventorySpec` has six fields. Each as
   the log records.
4. **The README and `PROVENANCE.md`**, by reading: as §2.2 and §2.3; §9.8's anchor resolves;
   nothing says `v0.5.0` is tagged.
5. **The addenda**, by reading. SGK's and ChamPBH's give the one condition as code, say the format
   is not bumped, citing each client's own rule, and mark one **Advice:**; SI's gives the
   declaration, what then holds, what of SI's moves, and §0.2's departures. Their client
   citations, read through `git show` at `031bcb4`, `7055532` and `f5f395b`, hold. The shifts: 15
   lines the `v0.4.0` addenda cite, across the four files, are each at `c8570e8`'s line + 5
   (README) or + 6 (checklists).
6. **Additive.** `git diff` of `docs/adoption/` has no `-` line.
7. **The gate.** G4's row is the row as it was with one dated sentence appended; G1–G3 and the
   rest of that board unchanged.
8. **The issue.** In §4 with its closing line; its index row gone; the index **4**, dated
   2026-10-21.
9. **Both ends.** `Ran 538 tests … OK` in `venv/` (0 `ResourceWarning` lines, `pip show` `0.5.0`
   editable, no `egg-info` left) and in the review's high-end venv with `f47b9a2`'s export
   installed editable (4 lines, timing). Port check: "OK: 20 module(s) … 1 test(s) declared not
   ported"; `black`: 79 files.
10. **Nothing left behind.** No Ray process; seven tags; `origin` unchanged; no `build/`, `dist/`
    or `*.egg-info` in the checkout.

*Residue fixed in the review's records commit.* "this commit" → `f47b9a2` on the board, in the
log, in the README and in `prompts/INDEX.md`; "reviewed" for 02 there; the notes line.

*Observations, none an issue.* The agent's six (log §7) stand. Its second, whether G4 holds now
that SI pins `v0.4.0` (SI `1b1ca6d`), is for the user, when SI's adoption is accepted against its
checklist §9.

**Legend.** ✍️ written · ⏸ held, with what it waits on · ⬜ not written / not landed ·
✅ landed.

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`3e6d550`),
used for 01; [`orchestrator/prompt-02.md`](orchestrator/prompt-02.md) (`62c69d7`), used for 02.

## 2. Gates outside this repository

None of this campaign's own. SI's pin prompt waits on the tag (README §7). When it is made, its tag
object, its commit and the SI addendum are given to the user.

## 3. Active and unresolved issues

None open.

## 4. Resolved issues

- **[01-a-new-spec-field-moves-every-spec-guard-digest]** — *opened 2026-10-21 by the
  orchestrator, while writing 02; measured against 01's tree (`5475cef`) and the clients through
  `git`. Assigned to 02.*
  - **The defect.** U5 told ChamPBH and SGK that they "need nothing" to move to `v0.5.0`. Each has a
    spec guard (`ObjectFactories/tests/test_fingerprint_format_guard.py`, at SGK `031bcb4` and
    ChamPBH `7055532`), RunRegistryKit's recipe (its `docs/adoption/README.md` §6, `v0.2.0`), which
    hashes each `InventorySpec` by walking `dataclasses.fields` and pins the digests per
    `FINGERPRINT_FORMAT` (`config/fingerprint.py`'s `SPEC_DIGESTS`; SGK format 6, ChamPBH 3).
    01's `extra_values` is a seventh field, so every plain spec gains `"extra_values": {}`.
  - **Measured.** The recipe on the neutral registry: all 13 classes' digests differ between
    `c8570e8` and `5475cef`; with `plain` leaving out an empty `extra_values`, only `Trace`'s,
    which declares one. The same on two hand-built specs in the installed `v0.4.0` and `v0.5.0`
    wheels: differing plain, equal with the condition.
  - **Impact.** On moving its pin, each client's guard fails naming every class and says to bump
    `FINGERPRINT_FORMAT`; a bump would move the format of every fingerprint it holds, for a
    release that changes none of its records. No record or fingerprint moves, and SI (no guard) is
    not affected. RunRegistryKit's recipe has the same exposure, in that repository.
  - **Next step.** U5 as amended (README §0.3, §6.2): 02's SGK and ChamPBH addenda give the one
    condition, and say not to bump the format for it. Closed by 02.
  - **Closed (2026-10-21, 02):** by `extra-values` prompt 02, `f47b9a2`. The SGK and ChamPBH
    addenda ([`docs/adoption/secondarygwkit.md`](../../docs/adoption/secondarygwkit.md#addendum-v050-extra-values-prompt-02-2026-10-21),
    [`docs/adoption/champbh.md`](../../docs/adoption/champbh.md#addendum-v050-extra-values-prompt-02-2026-10-21))
    each say that a move to `v0.5.0` changes nothing the client calls or holds, that its spec guard
    then fails, that the format is not bumped for it, and give the edit: `plain` leaves out a field
    named `extra_values` whose value is empty; the README addendum's "The spec guard" gives it for
    every client. The release check probes it (log 02, §5.3): RunRegistryKit's `plain` and
    `spec_digests`, copied from its `v0.2.0` tag, over two hand-built specs in the installed
    `v0.4.0` and `v0.5.0` wheels, give differing digests, and with the condition equal ones; a spec
    declaring an extra table moves its digest with the condition; and on the neutral registry all
    13 classes differ, and with the condition only `Trace`. No package change. The same condition
    in RunRegistryKit's recipe is that repository's, in a campaign of its own (prompt 02 §8).
