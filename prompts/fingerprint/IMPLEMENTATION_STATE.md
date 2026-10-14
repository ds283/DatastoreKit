# fingerprint campaign — implementation state

**Last updated:** 2026-10-14 · **Status: CLOSED 2026-10-14 — 2 of 2 prompts written and landed (01,
`d1b61d6`; 02, `c8570e8`), each reviewed; `v0.4.0` made, annotated, on `c8570e8` (tag object
`8e7c1d7`) after CI passed there at both ends; U1–U6 taken 2026-10-12 (U1 amended by the user, the
rest as recommended).**

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
| 01 | [The fingerprint moves into the package](01-the-fingerprint-moves-into-the-package.md) | `store_fingerprint.py` (U1–U3); `test_store_fingerprint.py` and the golden (U4); the equivalence check (U5); contract §9.7 | ✍️ yes, 2026-10-12, revised for U1 the same day | ✅ 2026-10-14; reviewed 2026-10-14 | `d1b61d6` | [log](logs/01-the-fingerprint-moves-into-the-package.md) |
| 02 | [Release `v0.4.0`](02-release-v0.4.0.md) | the version, `README.md`, `PROVENANCE.md`, adoption addenda (SGK's saying what it must do); the extraction board's G4; the tag after green CI (U6) | ✍️ yes, 2026-10-14, against `203ecd0` | ✅ 2026-10-14; reviewed 2026-10-14; CI green at both ends (run 38538726292); tagged `v0.4.0` | `c8570e8` | [log](logs/02-release-v0.4.0.md) |

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

**Orchestrator review of prompt 01 (2026-10-14).** Dispatched from `df3fec9` to one Opus
subagent, with the note's six corrections and its additions. Reviewed against its commit
`d1b61d6`, with nothing landed after it. **Every check of the note's §3 passed**, and acceptance
1–4 are met. No stop condition fired. Nothing was pushed by this campaign, and the tags are
`v0.1.0` to `v0.3.0` only.

*At dispatch.* The tree was clean, one worktree, at `df3fec9`; `origin/main` `5f972be` by
`git ls-remote`, at dispatch and at the review. The suite gave `Ran 509 tests … OK` in `venv/` (0
`ResourceWarning` lines), the port check exited 0, and `black --check datastorekit docs` left 76
files. No Ray process was up, and `RAY_ADDRESS` was unset. While writing the note the orchestrator
built a prototype of §2.1–§2.3 in a scratch export (524 at both ends) and ran a scratch extract of
SGK's functions beside it (0 differences, the planner's two digests). It found that a bare
`assertRaises` lets breakage (j) pass test 7 for the string and the dict, which Python's own
comparison refuses (correction 1); that a tag added to a Trace moves Weave's entries, and that
Sample's validated flag is not identity (correction 2); that the changed stores number 28, not 27
(correction 3); that the brief and the audit postdate `c8a7f14` (correction 4); that (f) is
equivalent (correction 5); and line readings and the extract's SHA-256 (correction 6). The clients:
SGK `a5a6f6d` (clean) and SI `5fb4a1d` (clean) throughout; CPBH moved under another session,
`985819c` (23 entries) while the note was written → `a95658b` (29) at dispatch → `1905065` →
`2792a85` (23) at the review, recorded and not stopped on.

*The checks.*
1. **Scope.** `d1b61d6` touches the prompt's §7 files only: under `datastorekit/`, three `A` lines
   (the module, its test module, the golden). The diff over `pyproject.toml`, `README.md`,
   `PROVENANCE.md`, `docs/adoption/`, `docs/extraction/`, `docs/extraction-verification.md`,
   `docs/OPEN_ISSUES.md` and `.github/` is empty. `git status --short --ignored` is as at dispatch.
2. **The module, by reading.** As §2.1 items 1–8: its docstring names no client, format number or
   history; `canonical_json` imported at module scope, no lazy import; `ENCODING_FORMAT = 1` under
   U3's rule in its eight items, the same as §9.7's. The orchestrator's own `ast` comparison
   against a fresh extract (SHA-256 `9b1a8aed…0108`, as correction 6): the five helpers equal;
   `fingerprint_of` differs by its argument, the type and value checks, the removed lazy import,
   `fingerprint_format` for `FINGERPRINT_FORMAT` and the `encoding_format` key; `compare_fingerprints`
   by the versions block; `listing_lines` by the removed import and its first `yield`. The `format`
   text's `JoinedStr` is identical to SGK's. In `venv/`, `fingerprint_format` is
   `POSITIONAL_OR_KEYWORD` with no default.
3. **The equivalence.** The log's script (SHA-256 `4ef9393f…9a2c`, as the log says), beside a
   fresh extract with its three lines (`006459ac…aa4f`, as the log says), run on the commit's
   export in the review's own offline venvs at both ends (3.12.15 / 2.43.0 / 2.0.39 and 3.13.16 /
   2.55.1 / 2.0.46): exit 0, **0 differences**, the baseline and 37 changed stores (28 last-row
   deletions, every comparison non-empty, 14 with `problems` entries; and test 2's nine) at formats
   1 and 6; digests `7656b600…d304` and `bdf09575…9b19`, the planner's. The two ends' outputs agree
   line for line.
4. **The tests, by reading.** 21 tests in eight classes, every store in a `tempfile` directory, a
   `tearDownModule` asserting Ray is not initialised. Test 2 names its expected sets from the
   fixture, with Sample 2 for the local cases, Trace 3 for the value row and the flag, and a seventh
   case, a tag on Trace 4, whose set names Weave's entries (correction 2); test 6's literal is SGK's
   text; test 7 matches each refusal's message and its value (correction 1); test 8 runs a fresh
   interpreter. The golden's name is built from both constants. Nothing is imported from another
   test module, and the prose names the source generically.
5. **The suite at both ends.** `venv/`: `Ran 530 tests … OK`, 0 `ResourceWarning` lines. A fresh
   high-end venv with `git archive d1b61d6` installed editable: `Ran 530 tests … OK`, 4
   `ResourceWarning` lines, outside the new module (timing, `actor-names` log 01 correction 8). The
   port check exits 0 ("20 module(s) … 1 test(s) declared not ported"); the guards pass in both
   suites; `black --check datastorekit docs` leaves 78 files. Run with the layer guard's own scans,
   the new module has no hit; the test module's only hits are the neutral client's `_tags` table
   names in its SQL, which `test_store_inventory` and the client's factories carry too.
6. **The breakages.** (a)–(j) extracted from the log, each `git apply --check` and `-R --check`
   clean against the review's own export of `d1b61d6`, and the new module run under each: (a) and
   (b) fail test 4 twice (the golden, the recomputed digest), and (a) makes the equivalence check
   exit 1 with 80 differences; (c) fails test 6 twice; (d) test 6 once; (e) test 5; (f) `OK`,
   equivalent; (g) test 4's golden and test 5 in all 13 classes; (h) test 7; (j) test 7, five
   entries (`True`, `"1"`, `1.0`, the dict, and the refusal before any read); (i) test 2's orphan
   and row-alone cases. Each as the log records.
7. **The golden.** The log's script, run on the commit's export into a scratch root, writes a file
   byte-identical to the committed one (SHA-256 `03db7149…018e`), digest `7656b600…d304`.
8. **The documents.** Contract: the head line after `:40-41`; §9.7 after §9.6, in §9's form, its
   "Supersedes" none; every `store_fingerprint.py` and `store_inventory.py` citation read at
   `d1b61d6`; `git diff` of the file is `+` lines only (19). The relative link added resolves.
9. **The records.** The log in §5.1's form, with the equivalence and golden scripts, the ten
   breakage diffs, the names checked and the clients at the start and the end; this board's header,
   01's row and its note; the README's header and §2 row; `prompts/INDEX.md`; `docs/OPEN_ISSUES.md`
   unchanged at 4.
10. **Nothing left behind.** No Ray process, before or after. `git tag -l` is the six tags, and
    `origin` is unchanged (`5f972be`).

*Residue fixed in the commit that records this review:* "this commit" → `d1b61d6` on this board
and in the log; "reviewed" for 01 in this board's header and row, README §2 and its header, and
`prompts/INDEX.md`; the notes line. The log's observation 1, that `listing_lines` needs a
fingerprint of this module's (one of the source's own raises `KeyError`), is by design, and goes
into 02's SGK addendum; it is not an issue.

**Prompt 02 (2026-10-14).** The package is ready to be released as `v0.4.0`: `pyproject.toml`
says `0.4.0`; `README.md` and `PROVENANCE.md` describe it; each file under `docs/adoption/` has an
italic head line and a dated `v0.4.0` addendum, added only (`git diff` has no `-` line), stating
the pins (SGK adopts `v0.4.0`; CPBH may stay on `v0.3.0` and SI adopt `v0.3.0`, or either move to
`v0.4.0`), what changed, what it supersedes by `path:line` and what stands, and how to read the
earlier addenda's citations (N = 5 in the README, 6 in each checklist). SGK's addendum separates
the pin, which changes nothing SGK calls, from the call, which changes seven things, and names
SGK's options for the fingerprints it holds without choosing. The extraction board's G4 reads
"`v0.3.0` or later". A wheel built offline from an export is `datastorekit-0.4.0-py3-none-any.whl`,
26 entries, none under `datastorekit/tests/`; against `v0.3.0`'s, its 20 `RECORD` lines under
`datastorekit/` are equal and `store_fingerprint.py`'s is added. Breakages (a)–(c) each fail the
release check. The suite stays at **530** at both ends. §1.1's measure reproduces at SGK
`a5a6f6d` and `c8a7f14`, CPBH `2792a85` and SI `5fb4a1d`. No issue was opened; nothing was pushed
or tagged. See the [log](logs/02-release-v0.4.0.md).

**Orchestrator review of prompt 02 (2026-10-14).** Prompt 02 was written by the orchestrator
against `203ecd0` (`226d2e0`): the plan left it to be written after 01's review, and it had not
been. The note (`692b943`) was dispatched to one Opus subagent, with its four corrections and its
additions. Reviewed against its commit `c8570e8`, with nothing landed after it. **Every check of
the note's §3 passed**, and acceptance 1–6 are met. No stop condition fired. Nothing was pushed
by this campaign, and the tags are `v0.1.0` to `v0.3.0` only.

*At dispatch.* The tree was clean, one worktree, at `692b943`; `origin/main` `5f972be` by
`git ls-remote`, at dispatch and at the review. At `226d2e0` the suite gave `Ran 530 tests … OK`
in `venv/` and at the high end (0 `ResourceWarning` lines each), the port check exited 0, and
`black --check datastorekit docs` left 78 files. No Ray process was up, and `RAY_ADDRESS` was
unset. Writing 02, the orchestrator probed the release offline (a `0.4.0` wheel of 26 entries,
differing from `v0.3.0`'s only by `store_fingerprint.py`'s `RECORD` line, run from outside the
repository) and (a)–(c), and read the clients' fingerprint calls by `ast` through `git`. That
read found two things the plan had not named, which 02 put into SGK's addendum: SGK's
`fingerprint_store` passes `taken` positionally (`RunRegistry/stores.py:1500`), as the test at
`:378` does; and every fingerprint SGK holds lacks `encoding_format`, so the package's comparison
refuses each. The note's corrections gave the line shifts as numbers (1), the full list of
`v0.3.0` statements superseded and standing, with SGK rows `:716` and `:717` the prompt's table
missed (2), the extraction board's rows (3) and SGK's citations (4). The clients were SGK
`a5a6f6d` (clean), CPBH `2792a85` (23 entries) and SI `5fb4a1d` (clean) at dispatch and at the
review.

*The checks.*
1. **Scope.** `c8570e8` touches the prompt's §7 files only: `pyproject.toml`, `README.md`,
   `PROVENANCE.md`, the four adoption files, the extraction board and the records. The diff over
   `datastorekit/`, the contract, the verification document, `docs/extraction/`, `.github/`,
   `CLAUDE.md`, `docs/OPEN_ISSUES.md` and `orchestrator/` is empty.
2. **Additive.** `git diff` of `docs/adoption/` has no `-` line; `pyproject.toml`'s is the version
   line alone; the extraction board's is G4's row alone, its title changed to "SI adopted `v0.3.0`
   or later (…; `fingerprint` U6)" and one dated sentence appended, its earlier text a prefix of
   the new.
3. **The release.** The review's own wheel, from `git archive c8570e8`, built and installed
   offline at the high end (3.13.16 / 2.55.1 / 2.0.46): `datastorekit-0.4.0-py3-none-any.whl`,
   104,424 bytes, 26 entries, none under `tests/`, its file list the log's; `METADATA` 0.4.0,
   `>=3.12`, `ray>=2.43`, `sqlalchemy<2.1,>=2.0.39`. From outside the repository: `0.4.0`,
   `ENCODING_FORMAT` 1, the signature, the hand-built inventory's six keys, recomputed digest,
   refusals, `encoding` entry and listing as the note's facts; no `ray` loaded;
   `datastorekit.tests` refused; `sharded_store --help` exits 0. Against the review's own `v0.3.0`
   wheel, the 20 `RECORD` lines are equal and only `store_fingerprint.py`'s is added
   (`OIGFxRU6…vNg`, 16,093 bytes).
4. **`README.md` and `PROVENANCE.md`, by reading.** As §2.2 and §2.3: the `v0.4.0` status
   paragraph linking §9.7; the pin `v0.4.0` and the six earlier tags remaining, SGK adopting
   `v0.4.0` and CPBH and SI each free to stay on `v0.3.0` or move, advising neither; the
   store-fingerprint item and the extended "What changed"; the new `###` section naming the source
   at `c8a7f14` with the extract's full SHA-256, the differences by decision and 01's equivalence
   result. Nothing says `v0.4.0` is tagged.
5. **The addenda, by reading.** Each italic line follows `object-timestamp` 02's; each addendum is
   placed, dated and named as the additions say. N = 5 in the README and 6 in each checklist, and
   each file's shifts (N, k + N, 2k + N, 3k + N) match the lines added (old `:486` → `:491` in the
   README, `:643` → `:649` in SGK's). SGK's keeps the pin ("nothing SGK calls") apart from the call
   (seven items), names three options for the fingerprints it holds and takes none, ends with a
   "For SGK's prompt 03" table, supersedes `:722` and `:723` (correction 2's `:716`, `:717`), and
   leaves G2 standing; a sample of its SGK citations (`stores.py:1879-1886`, `__init__.py:379-392`,
   `__main__.py:313-318`, `:335-337`, `:414-423`, `stores.py:1541-1543`, the plan's `:244-246` and
   `:255`, the verification document's `:152-157`, the audit's `:204-214`, `GOLDEN` `:74-78`) holds
   at `a5a6f6d`, and none of SGK's six golden files has `encoding_format`. CPBH's and SI's say
   nothing they call changes; G3's reading stands; SI's supersedes G4 and leaves its
   `DatastoreObject.timestamp` rows standing.
6. **Names and links.** The review's own scan: 201 relative links in the six documents and the
   extraction board, 0 bad; every dotted `datastorekit.` name imports in the release venv but
   `datastorekit.tests`, which the wheel leaves out by design.
7. **Both ends.** `venv/`: `pip show` 0.4.0, `Ran 530 tests … OK`, 0 `ResourceWarning` lines, no
   `egg-info`. A fresh high-end venv with `git archive c8570e8` installed editable: `Ran 530 tests
   … OK`, 0 lines. The port check exits 0; `black --check datastorekit docs` leaves 78 files.
8. **The breakages.** (a)–(c) extracted from the log, each `git apply --check` and `-R --check`
   clean, each built from its own export: (a) `Version: 0.3.0`, the module present; (b) 78
   entries, 52 under `tests/`, `datastorekit.tests` importable; (c) 25 entries, the 20 `RECORD`
   lines equal and none added, `ModuleNotFoundError` on the module. Each as the log records.
9. **The records.** The log in §5.1's form, with the release check, the documents' check, the names
   and links, §1.1's measure re-run, (a)–(c), the four supersession tables and the clients at both
   ends; this board's header, 02's row and its note; the README's header and §2 row;
   `prompts/INDEX.md`; `docs/OPEN_ISSUES.md` unchanged at 4.
10. **Nothing left behind.** No Ray process. `git tag -l` is the six tags, and `origin` is
    unchanged (`5f972be`). During check 8 a loop of the review's own ran one `uv build` from the
    checkout, writing `build/` and `datastorekit.egg-info/` there and a wheel and venv beside the
    repositories; the review deleted all four, and re-ran `venv/`'s suite on the clean tree (the
    530 above). No tracked file was touched.

*Residue fixed in the commit that records this review:* "this commit" → `c8570e8` on this board,
in the log's header and §9, in the README and in `prompts/INDEX.md`; "reviewed; awaiting CI for
`v0.4.0`" for 02 in this board's header and row, README §2 and its header, and `prompts/INDEX.md`;
the notes line. The log's observation 2 (SGK's brief says every sidecar is a tombstone, which R0
has since made untrue for two live stores) is for the SGK session with the tag; it is not an
issue here.

*CI (2026-10-14).* `c8570e8` was pushed as `main` with the user's approval, fast-forwarding
`origin/main` from `5f972be`; the records after it (`258a8c3` on) stayed local. The workflow ran on
it, [run 38538726292](https://github.com/ds283/DatastoreKit/actions/runs/38538726292), the first CI
run on 01's code as well as on the release: **both ends passed**. `suite (low)`: Python 3.12.15 /
Ray 2.43.0 / SQLAlchemy 2.0.39, SQLite 3.45.1, `Ran 530 tests … OK`, 0 `ResourceWarning` lines,
and `black` "78 files would be left unchanged". `suite (high)`: Python 3.13.16 / Ray 2.55.1 /
SQLAlchemy 2.0.46, SQLite 3.45.1, `Ran 530 tests … OK`, 4 `ResourceWarning` lines (two unclosed
SQLite connections reported from SQLAlchemy: timing, `actor-names` log 01 correction 8). `v0.4.0`
may be made on `c8570e8`, with the user's approval.

*The tag (2026-10-14).* With the user's approval, `v0.4.0` was made, annotated, on `c8570e8`
(tag object `8e7c1d7`), and pushed; `git ls-remote origin` gives `refs/tags/v0.4.0^{}` as
`c8570e8`. The extraction board's G4 records it. The campaign is closed in the commit that records
this.

**Legend.** ✍️ written · ⏸ held, with what it waits on · ⬜ not written / not landed ·
✅ landed.

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`df3fec9`),
used for 01; [`orchestrator/prompt-02.md`](orchestrator/prompt-02.md) (`692b943`), used for 02.

## 2. Gates outside this repository

None of this campaign's own. SGK's `runregistry-extraction` gate E1 waits on the tag (README §7).
*(2026-10-14: `v0.4.0` is made, annotated, on `c8570e8` (tag object `8e7c1d7`), after CI passed
there at both ends, [run 38538726292](https://github.com/ds283/DatastoreKit/actions/runs/38538726292).
The tag object, the commit and the SGK addendum,
[`docs/adoption/secondarygwkit.md`](../../docs/adoption/secondarygwkit.md#addendum-v040-fingerprint-prompt-02-2026-10-14),
are given to the user for SGK's E1.)* SGK's R1 result (the fingerprint taken both ways) is recorded
here when SGK reports it, in a records commit of its own; a difference is a defect of this
package, opened in §3.

## 3. Active and unresolved issues

No issue is held on this board (2026-10-14: prompts 01 and 02 opened none).

## 4. Resolved issues

None yet.
