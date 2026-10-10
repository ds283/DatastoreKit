# actor-names campaign — implementation state

**Last updated:** 2026-10-10 · **Status: IN PROGRESS — 1 of 2 prompts written (01), 1 landed (01,
`ac50a8a`, reviewed); U1–U3 taken 2026-10-10, as recommended; 02 is written after 01's
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
| 01 | [A closed pool releases its actor names](01-a-closed-pool-releases-its-actor-names.md) | the kill at `__exit__` and on a refused open, and the closed flag (U1); the stand-in's `ray.kill` and names (U2); a test module; the smoke script's step N reversed and a collision step; contract §9.3; a dated subsection of the verification document; closes the issue | ✍️ yes, 2026-10-10 | ✅ 2026-10-10; reviewed | `ac50a8a` | [log 01](logs/01-a-closed-pool-releases-its-actor-names.md) |
| 02 | Release `v0.2.2` (planned) | the version, `README.md`, `PROVENANCE.md`, adoption addenda; the tag after green CI (U3) | ⬜ | ⬜ | — | — |

**Orchestrator review of prompt 01 (2026-10-10).** Dispatched from `7c97125` to one Opus
subagent, with the note's eight corrections and its additions. Reviewed against its commit
`ac50a8a`, with nothing landed after it. **Every check of the note's §3 passed**, and acceptance
1–8 are met. No stop condition fired. Nothing was pushed, and the tags are `v0.1.0`, `v0.2.0` and
`v0.2.1` only.

*At dispatch.* The note's gate held at `7c97125`. The tree was clean, and the only worktree was
this checkout. The suite gave `Ran 486 tests … OK` in `venv/` (0 `ResourceWarning` lines). The port
check exited 0, and `black --check datastorekit docs` left 71 files unchanged. The clients were at
SGK `b510bc9` (clean), CPBH `52142d7` (23 untracked entries) and SI `7bb3efd` (clean). `origin`
had `main` at `d06b46a` and the three tags. No Ray process was up, `RAY_ADDRESS` was unset and
there was no `/tmp/ray/ray_current_cluster`. While writing the note, the orchestrator built a
prototype of §2.1–§2.4 in scratch exports. It gave 492 at both ends and passed the smoke run under
a local Ray at both ends. It found:
- breakage (d) must keep the `shard{key:04d}` prefix, which the stand-in parses (correction 1);
- the contract's head may gain a line for §9.3 (correction 2), and the index has two more lines to
  change (correction 3);
- a kill by name would let a refused second open kill the open pool's actors (correction 4);
- (a) and (b) fail more existing tests than the prompt said (corrections 5 and 6); two line numbers
  were off by one (correction 7); and the high end's `ResourceWarning` count is timing
  (correction 8).

*The checks.*
1. **Scope.** `ac50a8a` touches the prompt's §7 files only, and under `datastorekit/` three files.
   The diff over `pyproject.toml`, `README.md`, `PROVENANCE.md`, `docs/adoption/`, `.github/` and
   the other four scripts of `docs/extraction/` is empty. The ignored entries are dispatch's. Each
   client's `HEAD` and `git status --short` are as at dispatch.
2. **The fix, by reading.** `SQL/ShardedPool.py` gains 48 lines and loses none. The flag is set
   before the `try` (`:205`). `__exit__`'s body is unchanged, with the early return above it
   (`:851-852`) and the kill and flag after it (`:867-868`), and no `try`/`finally`.
   `_kill_actors` (`:419-441`) kills shards, then the broker read with `getattr`, each kill in its
   own `try`, and looks nothing up by name. `_close_refused_open` calls it last (`:417`). The
   profile agent is not killed.
3. **The stand-in, by reading.** `ray.kill` is patched in `active()` beside `ray.get`, and refuses
   a non-`Handle` with Ray's `ValueError`. A taken name is refused before the constructor runs,
   with Ray 2.43.0's message verbatim, and reserved after it returns. The kill frees a name only if
   the handle holds it. A killed handle's call is refused before the call log, the faults and the
   hooks. The flag is read from `__dict__`. The docstring states the strictness. Nothing is opt-in.
4. **The module, by reading.** Six tests as §2.3, each in one cluster in a temporary directory,
   each keeping the closed or refused pool referenced while it reopens. Test 4 asserts that the
   first pool serves a get, writing nothing, after the refused open.
5. **Both ends.** In `venv/`, `Ran 492 tests … OK`, with 0 `ResourceWarning` lines. In the review's
   own offline high-end venv with `git archive ac50a8a` installed editable, `Ran 492 tests … OK`,
   with **4** `ResourceWarning` lines. The agent saw 0, which bears out correction 8. The port
   check exits 0, the two guards pass (14 tests), and `black` leaves 72 files unchanged.
6. **The breakages.** The log's (a)–(d) and (f) pass `git apply --check`, apply, and pass `-R
   --check` against their own exports of `ac50a8a`. The whole suite under each, at the high end,
   fails as the log records:
   - (a): `failures=4, errors=162`. The new module's tests 1, 2, 4 and 6 fail, and 159 entries in
     the 11 modules of correction 5;
   - (b): 11 errors. Test 3 fails, and five entries each in `test_one_timestamp_per_write` and
     `test_version_row_at_open`;
   - (c): test 5 alone;
   - (d): test 4, and the one test of `test_refused_open_closes_engines` correction 1 names;
   - (f): test 6 alone (its four entries).
7. **Ray.** In the review's own offline venvs at both ends, each with the commit's export
   installed editable, the smoke script exits 0, with every step `PASS`, step for step as
   verification §4.6 records. Step C raises `builtins.ValueError` at 2.43.0 and
   `ray.exceptions.ActorAlreadyExistsError` at 2.55.1, and the first pool then serves `[1, 2]`.
   Under (e) at the high end, step N fails with 4 of 4 names held and the collision, steps C and
   3–6 are not run, and the script exits 1. No Ray process was up before or left after any run.
8. **The documents.** Contract §9.3 has three rows in §9's form. Every `path:line` it cites reads
   true at `ac50a8a`, and its "Supersedes" column is true. The head gains one italic line, after
   extraction prompt 11's paragraph. Neither the contract nor the verification document loses a
   line. Verification §4.6 is dated and names the prompt, quotes all three runs, and says §4.5
   stays true of `v0.2.1`. The script's SHA-256 it quotes is the commit's. All 14 relative links
   the commit adds resolve, anchors included.
9. **The close.** The issue is at the head of the extraction board's §4 with its Closed line. That
   board's §3 says none of this repository's is open, and its header is unchanged. This board's §3
   and §4, header and row, the README's header and §2 row, and `prompts/INDEX.md` are in step. The
   index's diff is correction 3's, at 4 open.
10. **Nothing left behind.** No Ray process. The tags are the three, and `origin` is unchanged.

*Findings beyond the prompt*, recorded and not acted on:
- **Test 3 refuses an open of a new store** (log 01 §2 item 11), so it passes under (a) and fails
  only under (b). Correction 5 had allowed for either form.
- **Step C needs step N**, so under (e) it is not run, rather than run with no name held as the
  note's addition intended. Step N still drops both pools in a `finally`. This changes only what
  (e) reports.
- The agent's recorded runs were of working-tree exports made before its commit (log 01 §2 item
  18). The review's runs used `ac50a8a` itself, and agree with the log.
- The log's two observations (`__exit__` that raises kills nothing; actors built before a failing
  constructor cannot be killed) are as the note foresaw. No issue was opened for either.

*Issues.* `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]` is closed. None is
opened. The index is 4, none of them this repository's.

*Residue fixed in this follow-up:*
- "this commit" → `ac50a8a` in this board's header, row and §4, the extraction board's Closed
  line, the README's header and §2 row, the log's header and §8, and `prompts/INDEX.md`;
- "reviewed" for 01 in this board's header and row, the README's header and §2 row, and
  `prompts/INDEX.md`;
- this paragraph and the notes line.

`main` is ahead of `origin/main` (`d06b46a`) by this note, `ac50a8a` and this record, and is pushed
only with the user's approval. 02 (`v0.2.2`) is written next, against the tree 01 leaves.

**Legend.** ✍️ written · ⏸ held, with what it waits on · ⬜ not written / not landed ·
✅ landed.

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`7c97125`),
used for 01.

## 2. Gates outside this repository

None of this campaign's own. The extraction campaign's G2–G4 are recorded on its board (README §7).

## 3. Active and unresolved issues

No issue is held on this board (2026-10-10). The issue this campaign owned was held on the
extraction board's §3, with its measurement; 01 closed it there, and §4 below points to it.

## 4. Resolved issues

- **[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]**: **closed** 2026-10-10 by 01
  (`ac50a8a`; [log 01](logs/01-a-closed-pool-releases-its-actor-names.md)). Its entry, with the
  measurement, the fix and how it was verified, is at the head of the
  [extraction board](../extraction/IMPLEMENTATION_STATE.md)'s §4, which opened it.
