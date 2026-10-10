# Orchestrator — prompt 01, a closed pool releases its actor names

Read [`../README.md`](../README.md) first: §0.1, §1, §4, §5 (every rule) and §6.2 (U1–U3). Then
read the extraction campaign's [`prompt-11.md`](../../extraction/orchestrator/prompt-11.md) §0,
corrections 1–3 (the name collision's type at each end, `pgrep` and shells, `address="local"`),
which `docs/extraction/ray_smoke_run.py` now embodies, and its "Conventions", which this note keeps
unless it says otherwise.

**You do not write code.** You may:
- run the suite, the port check, `black --check` and the guards;
- make venvs in the session scratchpad with `uv … --offline`, from the cache the extraction
  campaign filled;
- export the tree with `git archive` into the scratchpad, and run prototypes, the smoke script and
  breakages there, never in this checkout and never committing one;
- start Ray **only** through the smoke script, under README §5 rule 7, with no Ray process up
  before or left after, and never while a suite runs;
- reach the network only for one `git ls-remote origin` at dispatch and one at the review;
- read the three clients only through `git -C <client> rev-parse|status|show|grep`;
- fix small residue in a follow-up commit of your own (§4);
- after the review, and only with the user's approval, push `main` (§5).

**The prompt:** [`01-a-closed-pool-releases-its-actor-names.md`](../01-a-closed-pool-releases-its-actor-names.md)
**Closes:** `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]` · **Narrows:**
nothing · **Opens:** only what the work finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- U1 and U2 are taken (`d06b46a`). 01 is written (`06f582e`).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- `git diff --stat 33778b0 d06b46a -- datastorekit` is empty: the package is `v0.2.1`'s. Under
  `docs/`, only extraction prompt 11's four files differ from `33778b0`.
- `origin/main` is `d06b46a` (`git ls-remote origin`, 2026-10-10), so local `main` is one commit
  ahead of it with this note. The tags are `v0.1.0` (`0ece4aa` → `68db557`), `v0.2.0` (`9eaf542` →
  `240028e`) and `v0.2.1` (`0ba2e4d` → `33778b0`), here and on `origin`, and no other.
- The clients' `HEAD`s: SGK `b510bc9` (branch `handover-remedial`, clean), CPBH `52142d7` (`main`,
  23 untracked entries), SI `7bb3efd` (`main`, clean).
- The index is **5** (1 on this repository's boards, 4 inherited), and will be **4** after.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It changes the close of every pool, and the stand-in every test runs through.** The code change
is a dozen lines. The stand-in's change is what makes the suite see it, and it is always on (U2),
so every test that closes a pool now kills stand-in handles, and every test that opens two pools
in one cluster meets the name reservation. The planner's prototype met no collision over the 486;
the orchestrator's did not either (below). A test that does is a stop (§6), not something to work
around.

**The suite is now the main witness, and Ray the second.** Under the stand-in a regression fails
widely (breakage (a) fails 159 existing tests). Under real Ray the smoke script re-takes the
measurement of extraction prompt 11, reversed.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-10 at `d06b46a`, in `venv/`,
in offline scratch venvs at both ends, in scratch exports with a prototype of §2.1–§2.4, and under
a local Ray started and stopped by the smoke script. Pass them on. Corrections 1–4 change what the
agent does or writes, and are STRUCTURALLY REQUIRED. Corrections 5–8 correct what the prompt
states; the log records each as found.

1. **Breakage (d)'s form.** Keep each shard's name starting `shard{key:04d}`: the stand-in reads
   the shard id from the name's characters 5–8 (`standin_pool.py:170-171`), so a name that does
   not start that way makes every shard's id wrong, and fails far more than test 4. Apply (d) as:
   - `:307`: `name="SerialPoolBroker"` → `name=f"SerialPoolBroker-{id(self)}"`;
   - `:318` and `:592`: `name=f"shard{key:04d}-store"` → `name=f"shard{key:04d}-store-{id(self)}"`
     (the `.options(name=…)` only; `my_name=` unchanged).

   Measured: test 4 fails, and so does one existing test,
   `test_refused_open_closes_engines.TestARefusalAfterTheActorsClosesThem.test_a_new_store_whose_version_write_fails_closes_the_actors`,
   which asserts a stand-in message that carries the actor's name
   (`'shard0000-store-<id>.object_get(version) killed before it ran' != 'shard0000-store.object_get(version) killed before it ran'`).
   That is (d) renaming the actor, not a defect; the log says so.
2. **The contract's head.** The contract's head carries one italic line per §9 subsection, naming
   its tree (`docs/client-contract.md:15`, §9.2's). Read §2.5's "changes no other line of the file"
   as "removes or rewrites no line": §9.3 may add one italic head line in §9.2's form, after
   extraction prompt 11's paragraph (`:17-29`), which is not rewritten. Nothing of §1–§9.2 is
   superseded: no row says what `__exit__` does with the actors, and §9.2's row stays true. §9.3's
   "Supersedes" column says so, row by row.
3. **The index has two more lines to change.** Deleting the §1.3 row (`docs/OPEN_ISSUES.md:32`)
   leaves §1.3 an empty table, and §1.1's line (`:12`) says the issue "is assigned to
   `actor-names`, §1.3". So `docs/OPEN_ISSUES.md`'s diff is: the header (`:6`, 4 open, 0 on this
   repository's boards, 4 inherited); `:12` saying the issue was closed by `actor-names` prompt
   01; and §1.3's table (`:30-32`) replaced by one dated "None open" line. Nothing else.
   `prompts/INDEX.md`'s "Open issues" column for both campaigns changes with it.
4. **Kill only what the pool holds.** The helper kills the handles in `self._shards` (when it is a
   dict) and `self._broker` (read with `getattr`, since a refused open may not have set it), and
   never looks an actor up by name. A refused second open, while another pool is open, collides
   when its broker is created (`:307`): `self._shards` is still the shard count and `self._broker`
   unset, so it kills nothing. The names it collided on are the open pool's, and a kill by name
   would kill them. Measured under real Ray at both ends: after the refused second open, the first
   pool serves the same get. Test 4 asserts it.
5. **Breakage (a) fails more than tests 1, 2 and 6.**
   - **Test 4 fails** in any form: it reopens after closing the first pool.
   - **Test 3 fails** if it builds its store with a pool closed in the same cluster first, as a
     test built like `test_refused_open_closes_engines` does.
   - **159 existing tests fail**, in 11 modules: `test_one_timestamp_per_write` 53,
     `test_reconcile_at_open` 45, `test_replicated_write` 14, `test_prune_at_open` 9,
     `test_version_row_at_open` 9, `test_store_schema` 8, `test_refused_open_closes_engines` 7,
     `test_read_only_pool` 5, `test_version_keyed_lookups` 5, `test_shard_key_assignment` 3,
     `test_declared_facts` 1. Each reopens a store in the cluster that closed it. The agent
     records its own count, which depends on its module only.
6. **Breakage (b) fails more than test 3.** Ten existing tests fail too, five each in
   `test_one_timestamp_per_write` and `test_version_row_at_open`. Each injects a fault on the
   version write of a new store or label (so the open is refused once every actor exists), and
   then opens again in the same cluster.
7. **Line numbers.** The `read_table_config` check of `_open` is `:346-352`, not `:345-351`
   (`:345` is blank). `_Options.remote` is `:168-174`. The rest of the prompt's citations hold at
   `d06b46a`.
8. **The `ResourceWarning` lines at the high end.** The 4 lines (two warnings, each with its
   tracemalloc hint) come from SQLite connections the collector reaches during a test, and when it
   does is timing. Measured: 4 at the high end before; **0** with the prototype, in two runs; and
   0, 4 or 4 under breakages that change only one line. The log records what it sees. A change is
   not a stop; a new kind of warning is recorded and looked at.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **Work in this order:**
  1. the baseline: 486 in `venv/`, and at the high end from a fresh venv with an export of `HEAD`
     installed editable; the port check; `black --check datastorekit docs`, 71 files; the clients'
     `HEAD`s and statuses; Ray's processes, by the script's rule;
  2. §2.1 and §2.2; then the existing 486 at the high end, **before** writing the new module, so
     that a collision in an existing test is seen on its own (a stop);
  3. §2.3; the suite at both ends;
  4. the breakages (a)–(d) and (f), each in its own export at the high end;
  5. §2.4; the smoke run at both ends; then (e);
  6. the documents (§2.5, §2.6), the issue and the index (§2.7), the records;
  7. `venv/`'s suite again, the port check, `black`, the guards, the clients again, Ray's
     processes again.
- **Install, do not set `PYTHONPATH`.** Three modules run the package as a subprocess with a clean
  environment (`test_shard_key_audit_copy` 3 tests, `test_shard_key_audit_refusals` 11,
  `test_sharded_store_script` 5). In an export that is not installed they fail, 19 in all, whatever
  the code. Into each scratch venv: `ray`, `sqlalchemy` and `setuptools` offline, then
  `uv pip install --offline --no-deps --no-build-isolation -e <export>`. The high end is
  `/opt/local/bin/python3.13` with `ray==2.55.1` and `sqlalchemy==2.0.46`; a low-end scratch venv
  for the smoke run is `/opt/local/bin/python3.12` with `ray==2.43.0` and `sqlalchemy==2.0.39`.
  `venv/` is not reinstalled: it already holds this checkout, editable.
- **`__exit__` follows the prompt literally**: its present body, then the kill and the flag, with
  no `try`/`finally`. If the body raises (a shard's `__exit__` fails), the pool is not marked
  closed and its actors are not killed, as before. If the agent thinks that should change, it is
  an observation for the log and a §3 issue, not a change here (rule 4).
- **Do not restructure `_open`'s comprehensions** (`:316-332`, `:590-607`). Under the stand-in an
  actor's constructor runs synchronously, so a constructor that raises does so inside the
  comprehension, and the shards built before it are in no attribute, cannot be killed, and stay
  reserved in that cluster. Under Ray `.remote()` does not raise for a failing constructor, and
  those handles would be collected. No test meets this (the prototype's 492 passed), and hazard 3
  keeps `_open` as it is. The stand-in's docstring sentence on its strictness covers it; if a test
  meets it, it is §6's second stop.
- **The killed flag is read from `handle.__dict__`**, as the prompt warns, and so is anything else
  the stand-in adds to `Handle`. The kill frees a name only if the name's live holder is that
  handle.
- **The smoke script's step N drops the closed pool whatever happens** (in a `finally`), so that
  the collision step and steps 3–6 start with no name held. Under (e) step N then fails on its
  record ("after `__exit__` … 4 of 4 held"), and the log says which assertion failed. Do not
  raise from `close_pool` inside a `finally`: a failure there replaces the step's own exception.
  Put the "no name held" check in each step, after its close. The new step needs a label; the
  agent chooses one, and keeps `"N"`'s and the `needs` lists of steps 3–6.
- **The positive control.** Breakage (a) is the suite's positive control: the log gives its count
  beside the new module's results.

**The facts, checked by the orchestrator.** Pass them on.

- **The prototype.** In an export of `d06b46a`: a `self._closed = False` before `__init__`'s `try`
  (`:203`); a `_kill_actors()` helper (shards then broker, `ray.kill(h, no_restart=True)`, each
  in its own `try`, read as correction 4 says); `__exit__` returning at once when closed, and
  calling the helper and setting the flag after its body; `_close_refused_open` calling the helper
  last. In the stand-in: `ray.kill` patched in `active()`; a `names` dict per cluster, reserved in
  `_Options.remote` after the constructor returns, freed by the kill; a killed handle's call
  returning a `StandinRef` of `StandinActorDied` before the call log and the hooks. A scratch
  six-test module as §2.3.
- **The suite with the prototype:** `Ran 492 tests … OK` at both ends (3.12.15 / 2.43.0 / 2.0.39
  and 3.13.16 / 2.55.1 / 2.0.46, SQLite 3.53.4), installed editable, 0 `ResourceWarning` lines at
  each. So no existing test holds two open pools in one cluster or calls a closed pool's actor.
- **The breakages**, in exports at the high end, each against the prototype:

  | | Change | New module | Other modules |
  |---|---|---|---|
  | (a) | the helper's call removed from `__exit__` | 1, 2, 3, 4, 6 fail | 159 (correction 5) |
  | (b) | the helper's call removed from `_close_refused_open` | 3 fails | 10 (correction 6) |
  | (c) | the early return removed from `__exit__` | 5 fails (the second `__exit__` calls killed handles, and `ray.get` raises `StandinActorDied`) | none |
  | (d) | names per pool (correction 1) | 4 fails | 1 (correction 1) |
  | (f) | the stand-in's killed check removed | 6 fails | none |

  These runs were made with the package not installed, so the 19 subprocess tests failed in each,
  and in the unbroken prototype too; they are left out of the counts above.
- **The smoke run with the prototype's script** (step N reversed, a collision step), each from an
  offline scratch venv with the export installed editable:
  - low end: Ray started in 3.9 s; every step `PASS`; after each read-write `__exit__` 0 of 4
    names held, after the read-only one 0 of 3; the second open in step N worked at once (1.9 s);
    the collision raised `builtins.ValueError`, naming `SerialPoolBroker`, and the first pool then
    served serials `[1, 2]`; 17.4 s in all; exit 0;
  - high end: the same, Ray in 6.5 s, the collision `ray.exceptions.ActorAlreadyExistsError`;
    22.6 s; exit 0;
  - (e), high end: step N `FAIL` with 4 of 4 held after `__exit__`; steps 3–6 `NOT RUN`; exit 1.
    (The prototype's step N did not drop its pool when it failed, so its collision step failed
    too; the addition above avoids that.)
  - No Ray process before or after any run, by the script's rule. `RAY_ADDRESS` unset; no
    `/tmp/ray/ray_current_cluster`.
- **Ray's `ray.kill`** raises `ValueError` for anything that is not an actor handle at both ends
  (`ray/_private/worker.py`), as §2.2 item 1 says. Ray 2.43.0's collision message is the one §2.2
  item 2 quotes (`ray/actor.py:1046-1051`).
- **The clients**, read through `git` at their `HEAD`s: outside each one's own copy of the layer,
  nothing reads a pool's `_shards` or `_broker`, or calls `ray.get_actor` or `ray.kill`, as README
  §0.1 says.
- **The toolchain.** `venv/`: Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39, SQLite 3.53.4,
  `black` 25.1.0, `datastorekit 0.2.1` editable from this checkout. `uv` 0.12.20.
- **Expected counts.**
  - The suite: **486** before, **486 + n** after (n the new module's tests; 6 if one test per
    §2.3 item), at both ends.
  - `compare_ported_tests.py`: exit 0, "20 module(s) … 1 test(s) declared not ported" (the new
    module is not a port, and the check does not count it).
  - `black --check datastorekit docs`: **71** files before, **72** after.
  - The index: **5** now; **4** after.

**What the review exists to establish.**
- **(E1) Scope.** Only §7's files change; under `datastorekit/`, three files, and in
  `SQL/ShardedPool.py` only the flag, `__exit__`, `_close_refused_open` and the helper.
- **(E2) The fix.** A closed pool, read-write or read-only, and a refused open, release their
  names; a second `__exit__` does nothing; two open pools collide; nothing is killed by name.
- **(E3) The stand-in.** Faithful to Ray but for the one strictness it states, always on, and the
  killed flag read from `__dict__`.
- **(E4) The tests.** Six, each failing under its breakage, and (a) failing widely.
- **(E5) Ray.** The smoke script exits 0 at both ends, with the two exception types, fails under
  (e), and leaves no Ray process.
- **(E6) The documents and the close.** Contract §9.3 and the verification document's subsection,
  additive and true at their tree; the issue closed on the extraction board, pointed to here, gone
  from the index.
- **(E7) Both ends.** 486 + n in `venv/` and at the high end.

**Conventions.** Extraction prompt 11's note's, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- record each breakage as a diff relative to the repository root, and check it **as recorded in
  the log** with `git apply --check` and `-R --check` against a scratch export;
- read a client only through `git`, and never import or run its code;
- use a subdirectory of the session scratchpad, never `/tmp`, for venvs and exports; put no
  scratch `.py` under `datastorekit/` or `docs/`;
- a stop goes to the user;
- check `git log` before committing.

And for this prompt:
- **Ray is started only by the smoke script**, from a scratch venv, never while a suite runs.
- **No network.** Every venv and install is `--offline`.
- **No push, no tag, and no change to the GitHub repository's settings.** `pyproject.toml` stays
  at `0.2.1`.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. Record `git status --short
   --ignored` (at writing: `.idea/`, `venv/` and five `__pycache__/` directories).
2. **The baseline.** In `venv/`, `Ran 486 tests … OK` with no `ResourceWarning`; the port check
   exits 0; `black --check datastorekit docs` leaves 71 files unchanged; `pip show datastorekit`
   says `0.2.1`.
3. **The clients.** Each `HEAD` and `git status --short` as the gate says.
4. **The remote.** `git ls-remote origin`: `main` at `d06b46a…` and the three tags as the gate
   says.
5. **Ray.** No Ray process by the script's rule; `RAY_ADDRESS` unset.
6. **The index.** 5 now, and 4 after. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, this board, the extraction board, `docs/OPEN_ISSUES.md`,
  `CLAUDE.md`, `docs/client-contract.md`, `docs/extraction-verification.md`, extraction logs 08b
  and 11;
- `HEAD`, the clients' `HEAD`s and statuses, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's eight corrections and its additions. Correction 1 is
the one that would make breakage (d) fail for the wrong reason, and correction 4 the one that
would make a refused open kill an open pool's actors.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/01-a-closed-pool-releases-its-actor-names.md`, in
  README §5.1's form.
- **The files it may change are the prompt's §7 list, and nothing else.** It must not touch
  `pyproject.toml`, `README.md`, `PROVENANCE.md`, `docs/adoption/`, the other scripts of
  `docs/extraction/`, the workflow, `CLAUDE.md`, `LICENSE`, `.gitignore`, or anything under
  `orchestrator/`.
- **Under `docs/`, no line is removed** except the index's (correction 3).
- **It writes nothing in any client repository, and runs, imports or opens nothing of one.**
- **It reaches no network**, and starts Ray only by the smoke script, leaving no Ray process.
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §6 conditions, in particular an existing test that fails
  once the stand-in reserves names, before the new module is written.

## 3. The review — ten checks

Make the review's venvs and exports fresh, offline, in a subdirectory of the scratchpad of their
own, not the agent's.

1. **Scope (E1).** `git show --stat <commit>` touches only §7's files. `git diff <parent> <commit>
   -- pyproject.toml README.md PROVENANCE.md docs/adoption .github` is empty, and so is the diff of
   `docs/extraction/` other than `ray_smoke_run.py`. `git diff -- datastorekit` names three files.
   No venv, egg-info or scratch file; `git status --short --ignored` as at dispatch. Each client's
   `HEAD` and status as at dispatch.
2. **The fix, by reading (E2).** The flag is set before the `try`. `__exit__`'s body is unchanged
   above the kill. The helper kills shards then broker, each kill in its own `try`, reads
   `_broker` with `getattr`, and looks nothing up by name. `_close_refused_open` calls it last. The
   profile agent is not killed. The docstrings say what the prompt asks, and name no client.
3. **The stand-in, by reading (E3).** `ray.kill` is patched in `active()` beside `ray.get`, and
   refuses a non-`Handle` with `ValueError`. A name is reserved after the constructor returns and
   freed only by the kill of its holder. The collision's message is Ray 2.43.0's, verbatim. A
   killed handle's call is refused before the call log, the faults and the hooks. The killed flag
   is read from `__dict__`. The docstring states the strictness. Nothing is opt-in.
4. **The module, by reading (E4).** Six tests as §2.3, each in one cluster in a `tempfile`
   directory, each keeping the closed or refused pool referenced while it reopens. Test 4 asserts
   that the first pool serves a get after the refused open. The docstring cites the campaign and
   the issue.
5. **The suite at both ends (E7).** In `venv/`, `Ran <486 + n> tests … OK`. In a fresh high-end
   venv with `git archive <commit>` installed editable, the same, with the `ResourceWarning` lines
   counted. The port check and the guards pass; `black --check datastorekit docs` leaves 72
   files.
6. **The breakages (E4).** Extract (a)–(d) and (f) from the log; check each with `git apply
   --check` and `-R --check` against its own export of the commit, install it, and run the suite
   (or the module where the log says). Each fails as the log records, and as §0's table predicts
   up to the agent's module. (d) is in correction 1's form.
7. **Ray (E5).** In the review's own offline venvs at both ends, each with the commit's export
   installed editable: the smoke script exits 0, its output matches the log's step by step, the
   exception's class at each end among it; no Ray process before or after. Then (e) at the high
   end: exit 1, step N failing as the log says.
8. **The documents (E6).** Contract §9.3 in §9's form, each row's `path:line` read at the commit,
   its "Supersedes" column true; the head line, if added, in §9.2's form; `git diff` of the
   contract and of the verification document removes no line. The verification document's new
   subsection is at the end of §4, dated, names this prompt, quotes the runs, and says §4.5 stays
   true of `v0.2.1`. Every relative link and anchor added resolves.
9. **The close (E6).** The extraction board: the entry at the head of §4 with its "Closed" line;
   §3 saying none of this repository is open; the header otherwise unchanged. This board's §4
   pointer, header and row for 01; README's header and §2 row; `prompts/INDEX.md`. The index's diff
   is correction 3's, with the count at 4.
10. **Nothing left behind.** No Ray process. `git tag -l` is the three tags, and `origin` is
    unchanged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 01* paragraph, in the form of
  the extraction board's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on both boards, in the log, in the verification document's
    subsection if it uses the phrase, in the README and in `prompts/INDEX.md`;
  - "reviewed" for 01 in this board's header and row, README §2 and `prompts/INDEX.md`;
  - the notes line, with this note marked "used for 01".
- Anything the review finds that is not residue is opened on this board's §3 and in the index.
- **Report to the user:**
  - what landed: the fix, the stand-in's names and kills, the module, the smoke script's steps,
    §9.3, the verification subsection, and the issue closed;
  - the suite at both ends, and the breakages, with (a)'s count;
  - the smoke run at both ends from the review's own venvs, with the two exception types, and (e);
  - the index at 4;
  - that 02 (`v0.2.2`) is written next, against the tree 01 leaves;
  - **and ask whether to push `main`** (§5).

## 5. Pushing

01 makes no release and no tag. Its commit and the records after it are on local `main` only,
ahead of `origin/main` (`d06b46a`). Pushing is an outward-facing act: **ask the user, and wait for
a clear yes.**

1. With approval, `git push origin main`. It fast-forwards from `d06b46a`. The workflow runs on
   the pushed head at both ends; the smoke script is not collected, so CI does not start Ray.
2. **Read the run** once it has finished (`gh run list --workflow tests.yml --commit <head>`), once,
   when the user says it has finished or returns. Record its URL and both verdict lines on this
   board in a records commit of its own, and push that with approval too.
3. **If either end fails**, record it on this board's §3 with the job's log lines, open it in the
   index, and tell the user. Nothing is reverted without the user.

**Hand on.** 02 is written after this review, against the tree 01 leaves: it releases `v0.2.2`
(U3), and its tag is made only after CI is green on its commit.
