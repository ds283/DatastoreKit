# actor-names campaign — implementation state

**Last updated:** 2026-10-11 · **Status: IN PROGRESS — 3 of 3 prompts written (01, 01b, 02), 2 landed
(01, `ac50a8a`, reviewed; 01b, this commit, not yet reviewed); U1–U3 taken 2026-10-10, as
recommended, and U4 2026-10-11; 02 held on 01b's review, and re-measured against its tree. No
issue open on this board: 01b closed `[02-closing-a-pool-can-start-ray]` (§4).**

**Campaign:** [`README.md`](README.md) ·
**Owns:** `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]`, closed by 01 on the
[extraction board](../extraction/IMPLEMENTATION_STATE.md) §4; `[02-closing-a-pool-can-start-ray]`,
closed by 01b in §4 below ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) §1.3

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

### Decisions

**Put to the user (README §6.2), U1–U3 taken 2026-10-10 and U4 2026-10-11:**

| Decision | Recommendation | Status |
|---|---|---|
| **U1** how a closed pool releases its names | `ray.kill` each actor at the end of `__exit__` and of `_close_refused_open`; a closed flag; the names unchanged | **taken** 2026-10-10 |
| **U2** the stand-in pool | stands in `ray.kill`; reserves names per cluster until killed; a killed handle's calls raise; always on | **taken** 2026-10-10 |
| **U3** the release | `v0.2.2` by 02, which the clients adopt in place of `v0.2.1` | **taken** 2026-10-10 (needed by 02) |
| **U4** closing a pool must not start Ray | fix before the release, by 01b: `_kill_actors` kills nothing when a module-level `_ray_is_running()` is false; the stand-in stands it in | **taken** 2026-10-11 (fix first); the form is 01b's recommendation |

## 1. Prompts

| # | Prompt | Covers | Written? | Landed? | Commit | Log |
|---|---|---|---|---|---|---|
| 01 | [A closed pool releases its actor names](01-a-closed-pool-releases-its-actor-names.md) | the kill at `__exit__` and on a refused open, and the closed flag (U1); the stand-in's `ray.kill` and names (U2); a test module; the smoke script's step N reversed and a collision step; contract §9.3; a dated subsection of the verification document; closes the issue | ✍️ yes, 2026-10-10 | ✅ 2026-10-10; reviewed | `ac50a8a` | [log 01](logs/01-a-closed-pool-releases-its-actor-names.md) |
| 01b | [Closing a pool starts no Ray](01b-closing-a-pool-starts-no-ray.md) | `_ray_is_running()` and the guard in `_kill_actors`; the stand-in's patch; tests 7 and 8; the smoke run unchanged at both ends; contract §9.4; a dated subsection of the verification document; closes `[02-closing-a-pool-can-start-ray]` (U4) | ✍️ yes, 2026-10-11 | ✅ 2026-10-11; not yet reviewed | this commit | [log 01b](logs/01b-closing-a-pool-starts-no-ray.md) |
| 02 | [Release `v0.2.2`](02-release-v0.2.2.md) | the version, `README.md`, `PROVENANCE.md`, adoption addenda; the extraction board's G2–G4; the tag after green CI (U3) | ✍️ yes, 2026-10-10; ⏸ held 2026-10-11 on 01b, to be re-measured against its tree | ⬜ | — | — |

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

*The push (2026-10-10).* With the user's approval, `main` was pushed, moving `origin/main` from
`d06b46a` to `049fa1a` (a fast-forward, with no tag). CI passed there at both ends,
[run 38086774849](https://github.com/ds283/DatastoreKit/actions/runs/38086774849):
- low: Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39, `Ran 492 tests in 161.507s` / `OK`, and
  `black` leaving 72 files unchanged;
- high: 3.13.16 / 2.55.1 / 2.0.46, `Ran 492 tests in 167.201s` / `OK`;
- SQLite 3.45.1 at both.

The smoke script is not collected by the suite, so CI started no Ray.

**Legend.** ✍️ written · ⏸ held, with what it waits on · ⬜ not written / not landed ·
✅ landed.

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`7c97125`),
used for 01.

## 2. Gates outside this repository

None of this campaign's own. The extraction campaign's G2–G4 are recorded on its board (README §7).

## 3. Active and unresolved issues

No issue is held on this board (2026-10-11: `[02-closing-a-pool-can-start-ray]` was closed by
01b, §4).

The issue this campaign was opened for was held on the extraction board's §3, with its
measurement; 01 closed it there, and §4 below points to it.

## 4. Resolved issues

- **[02-closing-a-pool-can-start-ray]** — **Closed** (2026-10-11, by `actor-names` prompt 01b,
  this commit; [log 01b](logs/01b-closing-a-pool-starts-no-ray.md)). The guard: a module-level
  `_ray_is_running()` in `SQL/ShardedPool.py` returns `ray.is_initialized()`, and `_kill_actors`
  returns at once, before reading any handle, when it is false, so a close while the process is
  not connected to Ray kills nothing and never reaches Ray's `ray.kill`. The stand-in's patch:
  `StandinCluster.active()` stands in `_ray_is_running` on the module as true, beside `ray.kill`,
  and leaves `ray.is_initialized` alone. The two tests, 7 and 8 of
  `tests/test_closed_pool_releases_its_names.py`: a pool closed with Ray's own `ray.kill` and the
  module's own `_ray_is_running` restored, and `ray.init` stood in, calls no `ray.init` and leaves
  Ray uninitialised; `_ray_is_running` follows `ray.is_initialized()`. The suite is 494 at both
  ends. Breakage (a), the guard removed, fails test 7 alone (`[1, 1, 1, 1] != []`) and starts no
  Ray; (b), the stand-in's patch removed, fails 170 entries; (c), `_ray_is_running` always false,
  fails test 8 alone. The smoke runs: the script, unchanged, exits 0 at both ends, every step
  `PASS`, and exits 1 under (c) at the high end, step N failing with 4 of 4 names held; no Ray
  process before or after any run (`docs/extraction-verification.md` §4.7). Contract §9.4.
  The entry as it was held in §3:

  - **[02-closing-a-pool-can-start-ray]** — *opened 2026-10-11 by the orchestrator, checking prompt
    02's facts at `1925898`; **assigned** to prompt 01b (U4).*
    - **What.** `_kill_actors` (`SQL/ShardedPool.py:419-441`, 01's) calls Ray's `ray.kill` on every
      close. `ray.kill` is one of Ray's auto-init calls (`AUTO_INIT_APIS`, `ray/__init__.py:211-220`
      at 2.43.0, `:208-217` at 2.55.1): when the process is not connected to Ray, it runs `ray.init()`
      first. So a pool closed while the process is not connected to Ray starts a local Ray, which
      stays up until the process exits. The kill then raises, which `_kill_actors` ignores, so the
      close returns normally.
    - **Measured.** At Ray 2.55.1, `ray.kill` of an object that is not a handle, in a process with no
      Ray, started a local Ray ("Started a local Ray instance"), then raised `ValueError`, and
      `ray.is_initialized()` was then true. 2.43.0's source is the same in the lines above.
    - **Impact.** Under real Ray none, since a pool's actors exist only while the process is
      connected. A client's stand-in that patches `ray.get` and not `ray.kill` meets it: SGK's
      `Datastore/tests/standin_pool.py` (`active()`, `:231-247` at `b510bc9`), through
      `ComputeTargets/tests/test_quadsource_policy_main.py`, a "No Ray" test that closes a pool on
      stand-in shards. Once SGK adopted `v0.2.2` as 01 left it, that test would start a local Ray.
      CPBH and SI stand in neither call. Prompt 02 §1.1 states the opposite ("it never starts Ray"),
      from `ray/_private/worker.py`'s `def kill` alone, so 02 is held, and re-measured after 01b.
    - **Next.** 01b (U4): a module-level `_ray_is_running()` guards `_kill_actors`, and the stand-in
      stands it in. A prototype passed 493 at both ends, and the smoke run under real Ray (01b §1.2).

    **How it was found, and a rule broken in finding it.** Writing 02's orchestration note, the
    orchestrator re-checked 02 §1.1's claim with that one probe, from a scratch venv at the high end.
    The probe is not the smoke script, so starting Ray broke README §5 rule 7. It also ran while the
    orchestrator's high-end suite run of `1925898` was in progress, against the rule's "never with
    the suite running". The Ray it started was shut down when the probe's process exited, and no Ray
    process was found afterwards. That suite run (`Ran 492 tests … OK`, 0 `ResourceWarning` lines) is
    not relied on. Nothing else of the campaign repeats the probe: 01b's hazard 1 forbids it, and its
    test stands in `ray.init`.

- **[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]**: **closed** 2026-10-10 by 01
  (`ac50a8a`; [log 01](logs/01-a-closed-pool-releases-its-actor-names.md)). Its entry, with the
  measurement, the fix and how it was verified, is at the head of the
  [extraction board](../extraction/IMPLEMENTATION_STATE.md)'s §4, which opened it.
