# Orchestrator — prompt 06, version-keyed lookups

Read [`../README.md`](../README.md) first: §1, §2 (rows 06 and 07), §4, §5 (rules 6–10), §6.2
(U20, U22, U23 and U25–U28) and §7 (G3). Then read [`prompt-05.md`](prompt-05.md) §0's
"Conventions" and §5, which this note keeps unless it says otherwise, and the board's review of 05
with its `v0.1.0` paragraph.

**You do not write code.** You may:
- run the suite and both checks;
- make venvs in the session scratchpad with `uv pip install --offline`, from the cache 05's work
  filled, and nothing else: **no download** (the prompt's §4.2);
- build wheels from a clean export in the scratchpad, never in this checkout (05's correction 1);
- replay the log's breakage record, and revert it;
- run a probe from the session scratchpad, never committing one;
- read CPBH only through `git -C /Users/ds283/Documents/Code/ChamPBH show 52142d7:<path>`;
- fix small residue in a follow-up commit of your own (§4);
- after the review, and only with the user's approval of each push, push and tag as §5 says.

**The prompt:** [`06-version-keyed-lookups.md`](../06-version-keyed-lookups.md)
**Closes:** nothing · **Narrows:** nothing · **Changes:** nothing · **Opens:**
`[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]`, and only what else the work
finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- 05 landed (`68db557`), was reviewed (`487ec4c`), and `v0.1.0` is tagged on it (tag object
  `0ece4aa`) after green CI (`fe040b2`). 06 is written (`1f9941f`). U25–U28 are taken.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- Nothing outside `prompts/` has changed from `68db557` to `1f9941f`, so the package is `v0.1.0`'s.
- `origin/main` is `fe040b2`, an ancestor of local `main` (correction 1).
- CPBH's `Datastore/SQL/Datastore.py`, `config/version.py` and
  `Datastore/tests/test_version_keyed_lookups.py` are as the prompt cites them at `52142d7`, which
  is CPBH's `HEAD`.
- One prompt at a time in this checkout. 07 is not written.

## 0. What makes this prompt unusual

**It is the first prompt to change the layer.** Rule 8 has lifted, and `compare_with_source.py`
runs once, before the change, and is then retired (U27). From here the review's evidence that the
layer changed only as asked is:
- the diff, read line by line against the prompt's §2.1–§2.4;
- the schema witness, which must move by exactly one key;
- hazard 4: of the 444, exactly three tests move.

**It adds behaviour on two routes the source never had**: the package's late `set_version`, and
the read-only pool, whose actors are never given the insert serial (U26). The keying is in the
actor, so a mistake in the two-serial split shows up as a read-only open that cannot find its own
rows, or as a read-only actor that could insert.

**Its acceptance finishes elsewhere**, as 05's did: CI runs on GitHub after the review, and
`v0.2.0` is made only once CI has passed at both ends on 06's commit (U28). §5 says how.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-09 at `1f9941f` (package
files as at `68db557`), with `uv` 0.12.20 and MacPorts' Python 3.12.15 and 3.13.16. Pass them on.
Corrections 1 and 2 change what the agent does, and are STRUCTURALLY REQUIRED. Corrections 3–5
correct what the prompt expects; the log records them as found.

1. **The gate's "`main` equals `origin/main`" does not hold, and need not.** `origin/main` is
   `fe040b2`. Local `main` is ahead of it by `1f9941f` (the prompt) and this note's commit, both
   under `prompts/` only. 06 pushes nothing, so this changes nothing the agent does; the log
   records `git rev-list --count origin/main..HEAD` at dispatch.
2. **The undecorated actor, and its broker.** The prompt's §2.7 says "the undecorated
   `Datastore.__ray_actor_class__`". The suite reaches the actor as `standin_pool.DatastoreClass`
   (`Datastore.__ray_metadata__.modified_class`), and both exist and construct at both Ray ends.
   **Use `sp.DatastoreClass`**, as the suite does.

   An actor built with `serial_broker=None` cannot insert a class that takes a serial: its lease
   raises `RuntimeError: SerialLeaseManager (table="gauge_setting"): leased serial number is None`.
   So tests 8 and 9 need a broker. **Probed:** under an active `sp.StandinCluster()`,
   `sp.Handle(sp.BrokerClass(name="SerialPoolBroker"), "SerialPoolBroker", cluster, None)` passed
   as `serial_broker=` gives:
   - test 8: a keyed `Tessera` get on a fresh actor raises the actor's `RuntimeError`, and a get of
     `gauge_setting` on the same actor returns a `gauge_setting` (serial 1);
   - test 9: a `Tessera` written through a second actor on the same file, given `set_version(1)`,
     is found by a third given only `set_lookup_version(1)`; a miss on that third actor is refused
     by `_insert`'s guard ("cannot insert into "Tessera" before the version serial is set").

   The row that test 9 finds must therefore be written by another actor, on the same file, that
   holds the insert serial. How the test does so is the agent's choice, and the log says which.
3. **The witness holds no `ephemeral_probe` record.** The prompt's §2.6 says that
   `ephemeral_probe`'s record is unchanged in the comparison. The witness is captured from the
   registry less the classes whose `register()` is `None` (U20), so neither 04a's witness nor the
   new one has that record. The no-table case is pinned by
   `test_declared_facts.TestTheRecords.test_a_record_with_no_table_is_unchanged`, which must pass
   unchanged. **Probed** (with the change applied to a scratch copy, captured twice at the high
   end, byte-identical): the comparison finds exactly 21 additions,
   `classes/<cls>/record/key_on_version`, `true` on `Tessera` and `false` on the other 20, and
   nothing else. The file is **74,450 bytes**, SHA-256
   `643128946640fcc4fba64fb1e650bfe320b3b41a169a7cba78e850a7e9bcddb8` (04a's is 73,842).
   `schema_description.dumps` sorts keys, so this does not depend on where the record gains the
   key.
4. **"22 subtests each" is 21 subtests and one failure of the test itself.** Probed: each witness
   test gives 22 `FAIL` lines, one per class with a table and one for the whole test, and with
   `TestCoverageByDeclaration.test_every_register_key_is_declared_by_some_factory` the run is
   `Ran 444 tests … FAILED (failures=45)`. No error, and no other test moves (hazard 4 holds).
5. **Breakages (a) and (c) reach fewer of the 444 than the prompt expects.** `build_store` gets
   Tesserae, but the fixtures most modules use (`real_store_fixtures`) are hand-built and make no
   get. Probed, each on the 444 with the change in place:
   - **(a)** and **(c)**: the five tests of `test_neutral_client.TestRoundTrip` error, and
     `test_read_only_pool`'s `setUpModule` errors, so its 23 tests do not run (`Ran 421`). Over the
     458 expect `Ran 435`, with those six errors and the new tests that make a keyed get through a
     pool;
   - **(h)**: of the 444, exactly `test_read_only_pool.TestOtherWritesRaiseReadOnlyWrite.test_a_vectorized_get_that_reaches_an_inserter`,
     with the actor's `RuntimeError` in place of `ReadOnlyWrite`, as the prompt says;
   - **(i)**: none of the 444.

   The log records each as found, with its verdict line.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **Probe the semantics before writing the tests.** The orchestrator's probe of tests 1, 3, 4 and 5
  (through the pool, labels `A` and `B`, at the high end) gave:
  - under A a `Tessera` got twice is serial 1 both times;
  - under B the same payload is a new row (serial 3), and the vectorized get of a second weight
    gives 2 under A and 4 under B;
  - the `keypoint_alias` is serial 1 under both labels;
  - A reopened finds serial 1 again;
  - read-only under A finds 1, and under B finds 3;
  - read-only under B, a `Tessera` stored only under A raises `ReadOnlyWrite` (sharded miss)
    naming the shard and the insert;
  - Ray was never initialised.

  The agent's tests may differ in their values, but not in these outcomes.
- **Work in this order, and run the suite after each step that changes a file.**
  1. `compare_with_source.py`, once, on the untouched tree (its last run).
  2. `contract.py`, `schema.py`, `Datastore.py`, `ShardedPool.py`; then `Tessera_factory`. The
     suite: exactly the three tests of hazard 4 move.
  3. The witness (§2.6), `WITNESS`, the docstring sentence, `REGISTER_KEYS`. The suite: 444 OK.
  4. `test_version_keyed_lookups.py`. The suite: 458 OK.
  5. The records of the contract and of provenance (§2.9); the release (§2.10).
  6. The high end; the release check; (a)–(j).
  7. `venv/`'s suite again, the port check, `black --check`, the records.
- **Name the probes' files outside `datastorekit/`**, and run them with `-m` from the copy's root
  or with `PYTHONPATH` set to it, printing `datastorekit.__file__` (hazard 1). `venv/`'s
  `datastorekit` is an editable install of this checkout, and a scratch script run by path
  imports it.

**The facts, checked by the orchestrator.** Pass them on.

- **The prompt's line references hold** at `1f9941f`: `Datastore.py:164-172` (the read-only
  comment), `:515-526` (`payload_data`), `:146-162` (`set_version`), `:697-723` (`_insert`'s
  guard); `ShardedPool.py:436-475` (the read-only comment, step 5 at `:464-469`), `:561-564`
  (`read_only_state`), `:3277-3302` (`object_get_vectorized`, the in-place update at
  `:3298-3299`); `factories.py:919-962` (`Tessera_factory`); and CPBH `52142d7`'s
  `Datastore.py:328-338`, `:390`, `:500-509`, `:544-555` and `config/version.py:52-71`. CPBH's
  test module is 470 lines, with ten tests in `TestVersionKeyedLookups` and one in
  `TestOneVersionLabel`.
- **The change, probed** in a scratch copy of `1f9941f` (the prompt's §2.1–§2.5 as written, the
  read-only pool calling `set_lookup_version` after `read_only_state`, `Tessera`'s `build`
  filtering on `require_version_serial`), at the high end:
  - before the witness and `REGISTER_KEYS`: `FAILED (failures=45)`, as correction 4;
  - after them: `Ran 444 tests … OK`;
  - the layer guard passes with its one pinned hit, and `compare_ported_tests.py` exits 0 over
    twenty modules, one test declared not ported, with `WITNESS` and the docstring sentence
    changed.
- **The high end resolves offline.** `uv pip install --offline "ray==2.55.1"
  "sqlalchemy==2.0.46"` into a fresh Python 3.13.16 venv succeeds, and so does `uv pip install
  --offline --no-deps -e <copy>` (the build backend is cached). SQLite is 3.53.4.
- **The toolchain.** `venv/`: Python 3.12.15, `ray` 2.43.0, `sqlalchemy` 2.0.39, `black` 25.1.0,
  `datastorekit 0.1.0` installed editable from this checkout.
- **Expected counts.**
  - The suite is **444** before and **458** after, in `venv/` and at the high end, each run about
    85–120 seconds.
  - `compare_with_source.py`, before the change: exit 0, "files compared: 31", "files ported,
    checked by compare_ported_tests.py: 20", "files with no source, declared: 10". After 06 it
    would fail on the tree (a new test module, and changed layer files), which is U27's reason for
    retiring it; it is not run after.
  - `compare_ported_tests.py`: exit 0, "20 module(s) … 1 test(s) declared not ported", before and
    after.
  - `black --check datastorekit docs`: "64 files would be left unchanged" before, **65** after.
  - The index is **7**, and **8** after, unless the work opens another issue.
- **Ray.** No Ray process was up at writing (`pgrep -lf 'gcs_server|raylet|ray::'` empty).

**What the review exists to establish.**
- **(E1) The layer.** The diff to the four layer files is §2.1–§2.4's, and nothing else: no
  behaviour for a class that does not declare the key, and all three read-only guards kept.
- **(E2) The witness.** The new witness differs from 04a's by exactly the one key, 04a's is
  unchanged, and the new one is reproduced by the review's own capture.
- **(E3) The tests.** The 14 show the prompt's §2.7 table, and the other 444 pass with only hazard
  4's three changed. The port check passes.
- **(E4) Both ends.** 458 in `venv/` and at the high end, in the review's own venvs.
- **(E5) The release.** A wheel built from a clean export holds the layer and its tools, at
  `0.2.0`, and its new names import from outside the repository.
- **(E6) The documents.** `client-contract.md` §8, `PROVENANCE.md`, `README.md` and
  `compare_with_source.py`'s paragraph are true at the commit; additive where rule 6 says so; no
  file under `datastorekit/` names a client.
- **(E7) The breakages.** (a)–(j) each fail as recorded.
- **(E8) The records.**

**Conventions.** 05's note's, unchanged, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff to a tracked file with `git apply --check` and `-R --check` **as
  recorded in the log**, with its trailing context lines;
- read CPBH only through `git show`, and never import or run its code;
- use a subdirectory of the session scratchpad, never `/tmp`, for venvs, exports, wheels and probes,
  and put **no scratch `.py` under `datastorekit/`**;
- start no Ray;
- a stop goes to the user;
- check `git log` before committing.

And for this prompt:
- **No push, no tag, and no change to the GitHub repository's settings** (U28).
- **No download of any kind.** Every venv is made `--offline`. A pin that does not resolve offline
  is a stop.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. Record `git status --short
   --ignored` (at writing: `.idea/`, `venv/` and five `__pycache__/` directories).
2. **The baseline.** In `venv/`, the suite gives `Ran 444 tests … OK`, and both checks exit 0 with
   the counts above.
3. **CPBH.** `git -C ChamPBH rev-parse HEAD` is `52142d7…`, or the three files are unchanged from
   it to `HEAD`.
4. **The remote.** `git ls-remote origin` shows `main` at `fe040b2…` and `v0.1.0` peeling to
   `68db557…`, and no other tag.
5. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`.
6. **The index.** 7 now, and 8 after unless the work opens another issue. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`, and logs 04a and
  05;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's five corrections and three additions. Correction 2 is
the one most likely to cost time: an actor made with no broker fails its first insert with a
lease error that looks like the keying's.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/06-version-keyed-lookups.md`, in README §5.1's
  form, with the prompt's §5.6 additions.
- **The files it may add or change are the prompt's §7 list, and nothing else**, plus any issue
  the work opens. It must not touch:
  - `standin_pool.py`, any fixture, or any test module but the three §7 names and the new one;
  - `schema_at_extraction-04a.json` or `client_vocabulary.json`;
  - `CLAUDE.md`, `LICENSE`, `.gitignore`, the workflow or the campaign README;
  - anything under `orchestrator/`.
- **It pushes nothing, makes no tag, and changes no setting of the GitHub repository.**
- **It edits no client repository, and runs, imports or opens nothing of one.** CPBH is read
  through `git show` only.
- **It downloads nothing.**
- **It starts no Ray.**
- **Stop and ask** on any of the prompt's §6 conditions.

## 3. The review — eleven checks

Make the review's venvs fresh, offline, in a subdirectory of the scratchpad of their own, not the
agent's.

1. **Scope.** `git show --stat <commit>` touches exactly the prompt's §7 list: four layer files,
   `factories.py`, `registry.py`, `test_neutral_client.py`, `test_schema_builder.py`, the new
   witness and the new test module, `docs/client-contract.md`, `compare_with_source.py`,
   `PROVENANCE.md`, `README.md`, `pyproject.toml`, the log, the board, `docs/OPEN_ISSUES.md` and
   `prompts/INDEX.md`. No wheel, `dist/`, `build/`, `*.egg-info` or scratch file. `git status
   --short --ignored` lists the same entries as at dispatch.
2. **E1, by reading.** `git show <commit> -- datastorekit/contract.py datastorekit/SQL`:
   - `contract.py` imports nothing new outside the standard library; `VERSION_SERIAL_KEY ==
     "_version_serial"`; `require_version_serial` refuses an absent and a `None` key;
   - `schema.py`: `_declared_key_on_version` in the form of the three helpers, both refusals
     through `_refuse_declaration`, the key on every record with a table and on none without;
   - `Datastore.py`: `_lookup_serial` beside `_version_serial`; `set_version` sets both and keeps
     its checks; `set_lookup_version` sets only the lookup serial, with `set_version`'s type check
     and change refusal; `object_get` copies, refuses a caller's key and a `None` serial, and
     touches nothing for a class that does not declare the key; `_insert`'s guard reads
     `_version_serial`, unchanged; `object_read_batch`, `read_table`, `object_store` and
     `object_validate` are unchanged;
   - `ShardedPool.py`: `set_lookup_version` on every read-only actor after `read_only_state`, every
     call waited for; the two comments; nothing else, and `object_get_vectorized` unchanged
     (§2.8);
   - no comment or string in these files names CPBH, a CPBH class or campaign, or SGK.
3. **E2, the witness.** Capture it again from `git archive <commit>` with `schema_description.py`,
   in two fresh interpreters: byte-identical to the committed file, 74,450 bytes, SHA-256
   `643128…bcddb8` (correction 3). Load it and 04a's, and compare: exactly 21 additions of
   `key_on_version`, `true` on `Tessera` only. `git diff 68db557 <commit> --
   datastorekit/tests/data/schema_at_extraction-04a.json` is empty.
4. **E3, the 444.** `git diff 68db557 <commit> -- datastorekit/tests` touches only §7's test files.
   In `test_neutral_client.py` only `REGISTER_KEYS` changes; in `test_schema_builder.py` only
   `WITNESS` and the docstring sentence; in `registry.py` only `Tessera`'s roles row; in
   `factories.py` only `Tessera_factory`'s `register()` and `build` select.
   `compare_ported_tests.py` exits 0 with 04b's counts.
5. **E3, the 14, by reading.** Each test of §2.7's table is there, under its class and name, and
   shows what its row says. Pools are opened by the labelled form, actors by `sp.DatastoreClass`
   with a stand-in broker (correction 2), everything in `tempfile` directories, stdout redirected.
   The module docstring names no client, and says what each test carries over by test.
6. **E4, both ends.** In `venv/`: `pip show datastorekit` says `0.2.0`; `Ran 458 tests … OK`; the
   loader gives 14 for the new module; `black --check datastorekit docs` leaves 65 files
   unchanged. In a fresh high-end venv (3.13.16 / 2.55.1 / 2.0.46, offline) with `git archive
   <commit>` installed editable: `Ran 458 tests … OK`. If the agent's log ran a low end too, it
   agrees.
7. **E5, the release.** From `git archive <commit>`, build the wheel and install it into a fresh
   high-end venv, offline. 25 entries, none under `tests/`; `METADATA` says `Version: 0.2.0` and
   05's two `Requires-Dist` lines. From outside the repository with `PYTHONPATH` unset:
   `from datastorekit.contract import VERSION_SERIAL_KEY, require_version_serial` works,
   `datastorekit.tests` does not import, and the tools behave as at 05 (`sharded_store --help`
   exits 0; `shard_key_audit` exits 2 with its usage line naming `site-packages`). Compare the
   `RECORD` with the log's.
8. **E6, the documents, by reading.**
   - `client-contract.md`: `git diff 68db557 <commit>` adds the header line and §8 only; every line
     reference in §8 is checked against the commit's files.
   - `PROVENANCE.md`: the section "After `v0.1.0`", naming the files changed, CPBH `52142d7` and
     its lines, and U27.
   - `compare_with_source.py`: one docstring paragraph, and nothing else.
   - `README.md`: the status, the `v0.2.0` pin with the `v0.1.0` sentence, the "Using it" item,
     the "Developing" sentence; every name it mentions imports from the release venv, and every
     relative link resolves.
   - `pyproject.toml`: the version only.
   - The layer guard passes with `KNOWN_HITS` at its one entry.
9. **E7, the breakages.** Replay (a)–(j) as the log records them, each in its own export. Each
   fails as recorded, and (a), (c), (h) and (i) as correction 5 says over the 444. `git status`
   is clean after each.
10. **E8, the records.**
    - The log has every section of README §5.1 and §5.6's additions, the five corrections and the
      three additions, `compare_with_source.py`'s last output and both `git status --ignored`
      listings.
    - The board: 06's row, the header, the G3 line in §2 (ready to tag once CI passes; no tag
      made), and the issue in §3 with its reproduction.
    - `docs/OPEN_ISSUES.md`: count its rows; the header says 8 (or more, as opened) and today's
      date.
    - `prompts/INDEX.md`: the campaign's line.
11. **Nothing left behind.** No Ray process is up. `git tag -l` is `v0.1.0` alone, and
    `git ls-remote origin` shows `main` at `fe040b2` and `v0.1.0` only.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 06* paragraph, in the form of
  05's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README's header, and its §2 status for 06 ("landed, reviewed; awaiting CI for `v0.2.0`");
  - the notes line, with this note marked "used for 06".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Report to the user:**
  - what landed: the key, the two serials, the read-only pool, `Tessera`, the 14 tests, the
    witness, the documents and `0.2.0`;
  - the 458 in `venv/` and at the high end, from the review's own venvs;
  - the witness comparison;
  - the issue opened;
  - (a)–(j);
  - **and ask for approval to push** (§5).

## 5. Reaching `v0.2.0` (U28)

05's note §5, with `v0.2.0` for `v0.1.0` and 06's commit for 05's. Each push and the tag is an
outward-facing act: **ask the user, and wait for a clear yes, before each.** Approval of one is not
approval of the next.

1. **Push 06's commit as `main`:** `git push origin <06's SHA>:refs/heads/main`. It fast-forwards
   from `fe040b2`, carrying `1f9941f` and this note's commit with it. The workflow runs on 06's
   commit, both ends.
2. **Read the run** once it has finished: `gh run list --workflow tests.yml --commit <06's SHA>`
   and `gh run view <id> --log`. Do not poll in a loop; ask the user to say when it has finished,
   or check once when they return. From each job's log, record the versions step 4 prints, SQLite's
   among them, the suite's verdict line (`Ran 458 tests … OK`), and black's line on `low`.
3. **If either end fails**, stop. No tag. Record the failure on the board's §3 with the job's log
   lines, and tell the user that a fix prompt is needed; the tag goes on the fix's commit once its
   CI passes.
4. **If both pass**, with the user's approval:
   - `git tag -a v0.2.0 <06's SHA> -m "datastorekit 0.2.0: version-keyed lookups (key_on_version)"`;
   - `git push origin v0.2.0`;
   - check that `git ls-remote origin refs/tags/v0.2.0^{}` is 06's SHA.
5. **Then push the rest of `main`** (`git push origin main`), with approval.
6. **Record it**, in a commit of its own, before step 5's push or as part of it: the board's G3
   line (`v0.2.0` made on 06's SHA, with the run's URL and both ends' versions); the review
   paragraph's last line; README §2's status for 06; `prompts/INDEX.md`.

**Hand on to 07's author:**
- `v0.2.0` is on 06's commit. CPBH adopts it (G3); SGK may adopt `v0.1.0` or `v0.2.0`, which
  differ only behind `key_on_version`.
- CPBH's checklist names `config/version.py`'s `VERSION_SERIAL_KEY` and `require_version_serial`
  as moving to `datastorekit.contract`, its factories' `key_on_version` as unchanged, and
  `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]` as a caller-side hazard until
  it is fixed.
- `compare_with_source.py` is retired (U27); 07 does not run it.
