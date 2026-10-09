# Orchestrator — prompt 08a, two small fixes

Read [`../README.md`](../README.md) first: §1, §2 (rows 08a–11), §4, §5 (rules 4, 6, 7, 9 and 10)
and §6.2 (U17, U33–U37). Then read [`prompt-06.md`](prompt-06.md) §0's "Conventions" and
[`prompt-07a.md`](prompt-07a.md) §0's, which this note keeps unless it says otherwise, and the
board's review of 07a.

**You do not write code.** You may:
- run the suite, the port check, `black --check` and the layer guard;
- make venvs in the session scratchpad with `uv pip install --offline`, from the cache 05's work
  filled, and nothing else: **no download** (the prompt's §4.2);
- export the tree with `git archive` into the scratchpad, and run probes and breakages there,
  never in this checkout and never committing one;
- read the three clients only through `git -C <client> show|grep|ls-tree|log|status`;
- fix small residue in a follow-up commit of your own (§4).

You push nothing and make no tag: 08a makes no release (10 does, U36).

**The prompt:** [`08a-two-small-fixes.md`](../08a-two-small-fixes.md)
**Closes:** `[02-an-unsupplied-sharded-table-raises-keyerror]` and
`[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]` · **Narrows:** nothing ·
**Changes:** nothing · **Opens:** only what the work finds · **Model:** Opus, as the prompt
recommends.

**Gate:**
- 07a landed (`dd45243`) and was reviewed (`88cac61`). 08a is written (`8a1cae9`). U33–U37 are
  taken.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- Nothing under `datastorekit/` has changed from `240028e` to `8a1cae9` (only `docs/adoption/`,
  `measure_client_imports.py` and `prompts/` have), so the layer is `v0.2.0`'s.
- `origin/main` is `102f225`, an ancestor of local `main`, 5 commits behind it; `origin` holds
  `v0.1.0` and `v0.2.0` only.
- The clients' `HEAD`s are the prompt's: SGK `b510bc9` (branch `handover-remedial`), CPBH
  `52142d7` (`main`), SI `7bb3efd` (`main`).
- One prompt at a time in this checkout. 08b is not written.

## 0. What makes this prompt unusual

**The code is three lines; the weight is in the tests' proof.** Each new test must be shown to fail
on the unfixed layer for the reason the issue gives, or be a declared pin of behaviour the fix must
keep. A test that passes on both trees and pins nothing is wrong. The review re-runs the new
modules against the unfixed layer itself.

**It is the first prompt to close an issue by changing inherited behaviour.** 06 added behaviour
behind a key no client declares; 08a changes what every caller of two paths observes. Nothing the
layer writes changes, and no message changes, so `git diff` of `ShardedPool.py` must show the two
hunks and nothing else.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-09 at `8a1cae9`, in scratch
exports with the two fixes applied as the prompt's §2.1 and §2.2 give them, in `venv/` and in an
offline high-end venv; the clients read only through `git`. Pass them on. Corrections 1–3 change
what the agent writes, and are STRUCTURALLY REQUIRED. The rest correct or complete what the prompt
states; the log records each as found.

1. **The vectorized module's tests 2, 4 and 5 pass on the unfixed layer.** Only tests 1 and 3
   fail there. Tests 2, 4 and 5 pin behaviour the fix must keep, as tests 3–5 of the first module
   do; hazard 2's "or wrong" does not apply to them, and the log names them as pins. **Test 4 is
   caught by (d) alone, and only if it checks the row found.** Probed, through the stand-in pool,
   with a payload `{"weight": 0.25, "k": a2}` under the pool key `{"k": a1}`:
   - unfixed and fixed: the row found is `a1`'s (serial 1, its `k` the alias of `a1`);
   - under (d): a **new** row, serial 3, whose `k` is `a2`'s alias, inserted on `a1`'s shard.

   So test 4 must compare the row found with the pool key's row (its serial and its `k`'s
   serial), not only check that a `Tessera` came back.
2. **The contract's §9.1 row for the vectorized get supersedes no row.** No row of §1–§8 says what
   `object_get_vectorized` does to the caller's payloads: §1 row 4 cites the getter applied to its
   shard key (`:3295`), and row 6 its two refusals (`:3283-3286`, `:3289-3292`), both at `8bc60a5`.
   §8's "The keyed get" row says "The caller's payloads are not changed" of the actor's
   `_keyed_payloads`, and that stays true. So §9.1's row for the second fix says that it adds a
   fact §1–§8 never stated, and names no superseded row; the marker goes on §1 row 6 only, as the
   prompt says. If the agent reads the rows otherwise, it says why in the log.
3. **A test that reopens with another `sharded_tables` calls `ShardedPool(...)` itself.**
   `StandinCluster.open_pool` and `open_pool_output` both pass `sharded_tables=` from the registry
   and forward `**kwargs`, so giving another mapping through them is a duplicate keyword. Probed:
   inside `cluster.active()`, with stdout redirected, `sp.sp_mod.ShardedPool(version_label=
   "standin", db_name=primary, ShardKeyType=registry.shard_key_type, ShardKeyStoreIdGetter=
   registry.shard_key_store_id, replicated_tables=registry.replicated_tables, sharded_tables=
   <less one>, shards=3, factories=registry.factories, read_table_config=…,
   serial_batch_sizes=…)` on a store `build.open_pool` wrote and `cluster.close_pool` closed. Ray
   was never initialised.
4. **SI's vectorized gets pass a bare key, as CPBH's do** (§2.5). All 15 of SI's calls pass a bare
   `delta_Nstar` (SI's checklist, item 6, `docs/adoption/stochasticinstantons.md:250-259`),
   `plot_InstantonSolutions.py:697` and `:700` among them. Under the package they are refused by
   the shard-key test before the payload line, fixed or not. So "unaffected, since each call now
   merges its own key" holds once SI has converted them to the mapping form, which it must do to
   adopt. The finding is unchanged: no client reads a payload list back. The measured sites:
   - **SGK:** 17 calls in `main.py` (19 lines name the method; `:2158` and `:2582` are comments).
     Beyond `main.py`, `ComputeTargets/tests/test_quadsource_integral_parent_main.py:638-644` is a
     stand-in of the method that already copies (`dict(payload, **shard_key)`), called at `:926`
     with a literal list; `Datastore/tests/test_read_only_pool.py:600` passes a literal list, and
     is a module this package ported. The other three `ComputeTargets/tests/` modules name the
     method in `ast` scans of `main.py` only.
   - **CPBH:** 7 calls in `main.py`, each a bare `beta_value`.
   - **SI:** 10 calls in `main.py` (`:419` is a docstring), 3 in `plot_InstantonSolutions.py`, 2
     in `plotting/fetch.py` (`:143` is a docstring); 4 test stubs of the signature.
5. **Serials are not fixed between runs.** With `cluster.controller` unset, the controlling shard
   of a replicated write is drawn at random, so a keypoint's or an alias's serial, and the shard
   map, vary from run to run. Measured: the second keypoint was serial 2 in one run and 11 in
   another; the second alias 2 in one and 501 in another. The `Tessera` serials happened to agree
   (`[1, 2]`, `[1, 2]`, `[501, 502]`, the prompt's). **Tests compare rows with rows from another
   call**, or pin `cluster.controller`; no serial is a literal unless the controller is pinned.
6. **Breakage (b): what the open does instead.** Probed: through the fixture, `_read_shard_data`
   returns with nothing printed; through the constructor, the pool prints `>> Opened existing
   sharded datastore "<path>" with 3 shards` and opens, without the class, for each of `Sample`,
   `Weave` and `Tessera` left out. The duplicate-row case is refused alike, since its table is
   supplied.
7. **Line numbers at 08a's tree.** The guard is `ShardedPool.py:1026-1027`, and `attr = …` moves
   to `:1028`; the mismatch refusal raises at `:1056` (message `:1057`), the key-attribute refusal
   at `:1060` (`:1061`); `object_get_vectorized` is `:3290`, and the merge `:3311`. Hazard 7's
   "adds two lines at `:1025`" means after it. These are what §9.1 and the log cite.
8. **A refused constructor leaves its engines undisposed** (`[05-a-refused-open-leaves-its-engines-undisposed]`,
   08b's). The first module's constructor test refuses an open, so at the high end it adds
   `ResourceWarning` lines to the suite's output. That is expected and 08b's; it is not this
   prompt's to fix, and not a stop. The log records the high end's count.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **Write the tests before the fix, and run them on the unfixed tree first.** Order:
  1. the baseline (458; the port check; `black --check datastorekit docs`, 66 files; the clients'
     `HEAD`s and statuses);
  2. §2.5's client reading, recorded by count;
  3. the two test modules, on the unfixed layer. Record which tests fail and how (expected: the
     first module's tests 1 and 2 error with `KeyError`; the second's tests 1 and 3 fail; every
     other test passes);
  4. the two fixes. The suite: `458 + N` OK;
  5. the contract's §9.1;
  6. the high end; (a)–(e), each in its own scratch export;
  7. `venv/`'s suite again, the port check, `black`, the guard, the clients again, the records.
- **Name the probes' files outside `datastorekit/`**, and run them with the copy's root first on
  `sys.path`, printing `datastorekit.__file__` (hazard 1).
- **Record each breakage as a diff, exactly as applied**, so that the review can replay it with
  `git apply` against an export of the commit.

**The facts, checked by the orchestrator.** Pass them on.

- **The prompt's line references hold** at `8a1cae9`: `_read_shard_data` `:941`, the loop
  `:1020-1032` with the `KeyError` at `:1026`, the refusals `:1033-1060`; `object_get_vectorized`
  `:3288-3313`, the update `:3309-3310`; `Datastore.py:598-625`. The contract's §1 row 6 reads
  "raises `KeyError` at `:1015` before that message is reached" (`8bc60a5`'s line), and its header
  has the §8 line after which the new one goes.
- **The prompt's probes reproduce.** In a scratch export with the two fixes, through
  `shard_store_fixtures` and through the constructor:
  - an unsupplied `Sample` (`sharded_tables={}`): unfixed, `KeyError: 'Sample'`, nothing printed;
    fixed, the "configured in the existing ShardedPool, but were not supplied" line, `  Sample`,
    then `RuntimeError: Mismatch between sharded tables …`. Through the constructor the same for
    `Sample`, `Weave` and `Tessera`;
  - a supplied but unrecorded table, a differing key attribute (`Sample: configured key="k",
    supplied key="j"`), a matching set, and a second `Sample` row (inserted with `sqlite3`; the
    table then holds `(0, 'Sample', 'k')` and `(1, 'Sample', 'k')`): alike before and after;
  - the vectorized get: unfixed, `"k"` in both dicts after the first call and `a2`'s after the
    third; fixed, the dicts equal their deep copy throughout; the rows alike;
  - Ray never initialised.
- **The suite with both fixes:** `Ran 458 tests … OK` in `venv/` (112 s) and at the high end
  (139 s, with **184** `ResourceWarning` lines, as at 06's CI).
- **Breakages over the 458** (no new tests): (a) and (c) are each the unfixed layer for one fix,
  so the 458 pass under each. Under (b), (d) and (e), each applied to the fixed export, the 458
  also pass (`Ran 458 tests … OK` each). **No existing test catches any of the five**, so only
  the new modules do, and §4.4's record of which new tests fail under each is the whole of the
  evidence.
- **The high end resolves offline.** `uv` 0.12.20, `uv venv --offline -p
  /opt/local/bin/python3.13`, then `uv pip install --offline "ray==2.55.1" "sqlalchemy==2.0.46"`
  and `uv pip install --offline --no-deps -e <export>`: Python 3.13.16, Ray 2.55.1, SQLAlchemy
  2.0.46, SQLite 3.53.4.
- **The toolchain.** `venv/`: Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39, `black` 25.1.0,
  `datastorekit 0.2.0` installed editable from this checkout.
- **The layer guard** scans the layer's modules, not its tests; a new test's prose is checked by
  the review's reading, under `CLAUDE.md`'s rule that nothing in the package names a client.
- **Expected counts.**
  - The suite: **458** before; **458 + N** after, at both ends, N the loader's count for the two
    new modules (at least 10).
  - `compare_ported_tests.py`: exit 0, "20 module(s) … 1 test(s) declared not ported", unchanged.
  - `black --check datastorekit docs`: **66** files before, **68** after.
  - The index is **8**, and **6** after, unless the work opens an issue.
- **The clients' trees.** SGK and SI clean; CPBH's 23 untracked entries (17 `.db` files, two
  logs, two run scripts, `pilot-out/`, `prompts/jordan-normalization/`). None is read.
- **Ray.** No Ray process was up at writing.

**What the review exists to establish.**
- **(E1) The layer.** `ShardedPool.py`'s diff is §2.1's guard, after the membership test, and
  §2.2's merge, key last; nothing else in `datastorekit/` outside the two new modules.
- **(E2) The tests.** Each test of §2.3 is there; the unfixed layer fails exactly the tests the log
  says, for the issue's reason; the rest are named pins. No Ray, no client, `tempfile` only.
- **(E3) Both ends.** `458 + N` in `venv/` and at the high end, in the review's own venv.
- **(E4) The contract.** The header line, §9 with §9.1, and the one marker; nothing else in §1–§8;
  §9.1's line numbers true at the commit.
- **(E5) The breakages.** (a)–(e) each fail as recorded.
- **(E6) The clients.** Read, not changed; no client reads a payload list back.
- **(E7) The records.**

**Conventions.** 06's and 07a's notes', unchanged, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff **as recorded in the log** with `git apply --check` and `-R --check`
  against a scratch export;
- read a client only through `git`, and never import or run its code;
- use a subdirectory of the session scratchpad, never `/tmp`, for venvs, exports and probes, and
  put **no scratch `.py` under `datastorekit/` or `docs/`**;
- start no Ray;
- a stop goes to the user;
- check `git log` before committing.

And for this prompt:
- **No download of any kind.** Every venv is made `--offline`. A pin that does not resolve offline
  is a stop.
- **No `git stash` in this checkout.** The prompt's hazard 2 allows a stash of the two code lines;
  use a scratch export instead, so that the checkout never holds a half-state.
- **No push, no tag.**

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. Record `git status --short
   --ignored` (at writing: `.claude/`, `.idea/`, `venv/` and five `__pycache__/` directories).
2. **The baseline.** In `venv/`, the suite gives `Ran 458 tests … OK`; the port check exits 0;
   `black --check datastorekit docs` leaves 66 files unchanged.
3. **The clients.** Each `HEAD` is the gate's, and `git status --short` is as §0's facts say.
4. **The remote.** `git ls-remote origin` shows `main` at `102f225…`, `v0.1.0` peeling to
   `68db557…` and `v0.2.0` to `240028e…`, and no other tag.
5. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`.
6. **The index.** 8 now, and 6 after unless the work opens an issue. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `docs/client-contract.md`, and logs 02 and 06;
- `HEAD`, the clients' `HEAD`s and statuses, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's eight corrections and three additions. Correction 1 is
the one most likely to be missed: a test 4 that only checks that a `Tessera` came back passes under
(d) too.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/08a-two-small-fixes.md`, in README §5.1's form,
  with the prompt's §8 additions.
- **The files it may add or change are the prompt's §7 list, and nothing else.** It must not touch
  any other file under `datastorekit/` (`standin_pool.py`, the fixtures, the client, the guard
  among them), `compare_ported_tests.py`, `PROVENANCE.md`, `README.md`, `pyproject.toml`,
  `docs/adoption/`, `CLAUDE.md`, the campaign README, the workflow, or anything under
  `orchestrator/`.
- **It writes nothing in any client repository, and runs, imports or opens nothing of one.**
- **It downloads nothing.**
- **It pushes nothing and makes no tag.**
- **It starts no Ray.**
- **Stop and ask** on any of the prompt's §6 conditions.

## 3. The review — eleven checks

Make the review's venv fresh, offline, in a subdirectory of the scratchpad of its own, not the
agent's.

1. **Scope.** `git show --stat <commit>` touches exactly: `ShardedPool.py`, the two new test
   modules, `docs/client-contract.md`, the log, the board, `docs/OPEN_ISSUES.md` and
   `prompts/INDEX.md`. `git status --short --ignored` lists the same entries as at dispatch. Each
   client's `HEAD` and `git status --short` are as at dispatch.
2. **E1, by reading.** `git diff 8a1cae9 <commit> -- datastorekit/SQL/ShardedPool.py` is two
   hunks: the guard after the membership test, and the merge with the key last. No message, no
   comment and no other line changes.
3. **E2, the tests, by reading.** Each test of §2.3 is there, under a name that says what it pins;
   correction 1's test 4 compares the row found with the pool key's; the constructor test calls
   `ShardedPool(...)` inside `cluster.active()` (correction 3); no serial is a literal unless the
   controller is pinned (correction 5); everything in `tempfile` directories, stdout captured; the
   vectorized module's docstring says hazard 4's sentence; nothing names a client.
4. **E2, the tests, by running against the unfixed layer.** In a `git archive <commit>` export,
   restore `ShardedPool.py` from `8a1cae9` and run the two new modules: exactly the tests the log
   says fail, and for the issue's reason (`KeyError: 'Sample'` or the changed dicts). Then each
   fix alone: each module fails only under the other's absence.
5. **E3, both ends.** In `venv/`: `Ran 458 + N tests … OK`, the loader giving N for the two
   modules. In a fresh offline high-end venv with the export installed editable: the same, and the
   `ResourceWarning` count against the log's.
6. **The checks.** The port check exits 0 with 04b's counts; `black --check datastorekit docs`
   leaves 68 files unchanged; the layer guard passes with `KNOWN_HITS` at its one entry.
7. **E4, the contract.** `git diff 8a1cae9 <commit> -- docs/client-contract.md` adds the header
   line, §9 with §9.1, and the marker at the end of §1 row 6, and nothing else. Every line
   reference in §9.1 holds at the commit (correction 7). §9.1's vectorized row reflects
   correction 2.
8. **E5, the breakages.** Replay (a)–(e) as the log records them, each in its own export. Each
   fails as recorded; (b) as correction 6 says; (d) fails test 4 by the row found (correction 1).
   The 458 are unaffected except where the log says.
9. **E6, the clients.** The log's counts are correction 4's, or it explains the difference; no
   client changed.
10. **E7, the records.**
    - The log has every section of README §5.1, the port check's output in place of
      `compare_with_source.py`'s, the test-by-test record of §2.3 and §4.4, the clients' commits
      and statuses at the start and the end, and the duplicate row under "Observations not acted
      on".
    - The board: 08a's row, the header, and the two issues moved from §3 to §4, each with its
      "Closed (2026-10-09, prompt 08a)" line naming its fix and its test module.
    - `docs/OPEN_ISSUES.md`: 2 rows on this repository, the header saying 6 open and today's date.
    - `prompts/INDEX.md`: the campaign's line, and its open-issue count of 2.
11. **Nothing left behind.** No Ray process; `git tag -l` is `v0.1.0` and `v0.2.0`; `origin`
    unchanged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 08a* paragraph, in the form of
  07a's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log, in `prompts/INDEX.md`, and in
    `docs/client-contract.md`'s header line and §9.1 if it names 08a's tree that way;
  - README's header, and its §2 status for 08a ("landed, reviewed");
  - the notes line, with this note marked "used for 08a".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Report to the user:** the two fixes; the tests, which fail unfixed and which are pins; the 458
  + N at both ends; (a)–(e); the contract's §9.1; the clients' reading; the index at 6; and that
  08b can be written.

**Hand on to 08b's author:**
- `ShardedPool.py`'s lines move from 08a: +2 from `:1026`, −1 from `:3311`. 05's measured sites of
  the undisposed engines (`:858`, `:870` at `v0.1.0`) are to be re-measured at 08a's tree.
- `test_unsupplied_sharded_table`'s constructor test is a refused open made through the stand-in
  pool; a test that counts unclosed connections across a refused open can take it as its model.
- At the high end the suite printed 184 `ResourceWarning` lines before 08a's tests; the log gives
  the count after.
