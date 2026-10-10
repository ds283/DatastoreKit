# Prompt 11 — verification and close-out

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- 10 landed (`33778b0`) and was reviewed (`92ad43d`). CI passed there at both ends, and `v0.2.1`
  is tagged on it (tag object `0ba2e4d`), recorded at `41c77c1`.
- `git status` is clean in this repository, and `origin/main` is an ancestor of `main`.
- The tags on `origin` are `v0.1.0`, `v0.2.0` and `v0.2.1`, peeling to `68db557`, `240028e` and
  `33778b0`.

**Closes:** the campaign (U30, U33). **Narrows:** nothing. **Changes:** nothing. **Opens:**
`[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]` (§1.3), and only what else the
work finds.

**Recommended model:** **Opus.**
- This is a verification prompt, and its document is the one a later reader starts from.
- It changes no line of the package. It writes one document and one script, makes two dated
  corrections to the contract, and closes the board.
- For the first time in this campaign it starts Ray (U41) and reaches the network (U42), each
  once, for one purpose, under the rules of §3.

**Read first:**

1. [`README.md`](README.md): §0, §1, §2 (every row), §4, §5, §6 (D1–D4, and U3, U17, U23, U27,
   U28, U30, U33, U34, U37, U41 and U42) and §7.
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`: "Releases", the "Repository mechanics" and
   rules 4 and 6.
3. The board, every section. In §1, read the reviews of 09 and 10 in full, and the "Findings beyond
   the prompt" of every review.
4. Every log, `logs/01-…` to `logs/10-…`, at least §1 ("What shipped"), the deviations, the
   observations not acted on, and the state handed on. Log 01 §4.6 (where the inherited issues'
   code is), log 05 §5.3 and log 10 §5.3 (the release checks).
5. `docs/client-contract.md` (its head and §8), `PROVENANCE.md`, `README.md`, `docs/OPEN_ISSUES.md`
   and `docs/adoption/README.md`'s addendum.

Facts below are at `41c77c1`, whose `datastorekit/` is `33778b0`'s (`v0.2.1`), measured on
2026-10-10.

---

## 1. What is wanted

11 verifies the campaign, from the package as tagged `v0.2.1` and the records of 01–10, in **one
document**, `docs/extraction-verification.md`. It makes the two corrections to the contract that
U34 and the contract's head need. It records one finding as an issue, and **closes the campaign**.

**The package does not change.** Nothing under `datastorekit/` is touched, the suite stays at
**486**, and no tag is made (rule 10). 11 pushes nothing.

Two things are done for the first time in this campaign, each because the user decided so on
2026-10-10:
- **U41: a smoke run under real Ray.** Until now the suite has run the actors only through the
  in-process stand-in. 11 runs the package under a local `ray.init()` (no cluster) at both ends,
  with a script kept in `docs/extraction/`.
- **U42: the pin, installed as a client installs it.** 11 installs
  `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.1` from GitHub, and compares
  what is installed with 10's wheel.

### 1.1 The smoke run (U41), probed

The planner probed the run on this machine, at both ends, each in a scratch venv made offline with
an export of `33778b0` installed editable.
- **The ends.** Low: Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39. High: 3.13.16 / 2.55.1 /
  2.0.46. SQLite is 3.53.4 at both.
- **The start.** `ray.init(num_cpus=4, include_dashboard=False, log_to_driver=False)` starts a
  local instance in about 5 s. It needs no network beyond the loopback, and `ray.shutdown()`
  leaves no process: `pgrep -lf 'gcs_server|raylet|ray::'` is empty after.
- **The sequence**, in a `tempfile` directory, with a pool constructed directly from
  `datastorekit.tests.client.registry` (as `standin_pool.StandinCluster.open_pool` builds it,
  with the registry's `read_table_config` and `serial_batch_sizes`):
  1. a read-write pool is opened, and `build.write_every_class(pool)` writes every class: 3 tags,
     3 keypoints, 2 dials, 1 knob, 2 gauges, 2 rules, 1 probe, 3 aliases, 2 Gadgets, 6 Tesserae,
     4 Samples, 2 Traces and 1 Weave;
  2. a keyed vectorized get of two Tesserae finds serials 1 and 2. The caller's payload dicts are
     unchanged afterwards (08a);
  3. the pool is closed and reopened read-write, and the same get finds the same serials;
  4. a read-only pool finds the same serials (U26's lookup serial);
  5. an open with one sharded table left out of `sharded_tables` is refused with `RuntimeError`
     "Mismatch between sharded tables supplied to the constructor and read from the existing
     ShardedPool" (08a; 08b's cleanup runs on real actors);
  6. a read-write open after the refusal works.

  It ran in 10–13 s at each end.
- **The helpers.** `build`'s helpers resolve through the stand-in's `standin_get`. Under real Ray
  the probe gave them `ray.get` with `unittest.mock.patch.object(build, "resolve", ray.get)`. That
  patches the client's test helper, not the package.

### 1.2 The pin (U42), probed

Into a fresh Python 3.13.16 venv, with `ray==2.55.1` and `sqlalchemy==2.0.46` installed offline
first:
- `uv pip install --no-deps "datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.1"`
  fetched only the package. It installed `datastorekit==0.2.1` from
  `git+https://github.com/ds283/DatastoreKit@33778b04eafc0b9f01f5e272eb0f9b679eb6f0c7`.
  `direct_url.json` records `"requested_revision":"v0.2.1"` and that commit.
- **What is installed is 10's wheel.** The installed `RECORD`'s 20 lines under `datastorekit/` are
  identical, hash and size, to those of the wheel built from `git archive 33778b0`. The installed
  `RECORD` as a whole differs, because the installer adds `INSTALLER`, `REQUESTED`,
  `direct_url.json` and `uv_build.json`. Compare the 20 lines, not the file's hash.
- From a directory outside the repository, with `PYTHONPATH` unset, the package imports from
  `site-packages`, the version is `0.2.1`, and `import datastorekit.tests` raises
  `ModuleNotFoundError`.

### 1.3 A finding: a closed pool holds its actor names

The probe's first form opened each pool into the same variable, and its second read-write open
raised `ray.exceptions.ActorAlreadyExistsError`: "The name SerialPoolBroker (namespace=None) is
already taken".
- **The cause.** `ShardedPool` gives its actors fixed names in Ray's default namespace:
  - `SerialPoolBroker` (`SQL/ShardedPool.py:307`);
  - `shard{key:04d}-store`, read-write (`:318`) and read-only (`:592`).

  `__exit__` (`:808-821`) calls each shard's `__exit__`, cleans up the profile agent and disposes
  the engine. It releases no actor.
- **When the names are freed.** A name is freed only when the pool object holding the handles is
  collected. Measured:
  - after `__exit__`, with the pool still referenced, `ray.get_actor("SerialPoolBroker")` finds the
    broker;
  - after `del pool` and `gc.collect()`, it is gone at once (0.0 s at both ends);
  - with the read-only pool still referenced, the next open failed on `shard0002-store`;
  - once the refused open's exception was dropped, the names were free, and step 6 opened.
- **So, in one Ray session:**
  - two pools cannot be open at once, on any stores;
  - a pool cannot be reopened while the previous pool object is still referenced, closed or not.
    `pool = ShardedPool(…)` over a live `pool` builds the new pool before it rebinds, so it fails.
- **It is inherited.** SGK `b510bc9` names the same actors (`Datastore/SQL/ShardedPool.py:294`,
  `:305`, `:544`). Nothing on SGK's boards or in this repository records it. The contract does not
  say how long a closed pool holds its names.

**11 opens it as `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]`** (rule 4), on
the board's §3 and in the index, with the measurement above, re-taken by the smoke script. It is
not fixed, and it is assigned to no campaign. The smoke script drops each pool (`del` and
`gc.collect()`) before it opens the next, and its step 5 drops the exception. The document says
so.

### 1.4 The contract

- **U34.** §8's read-only row cites the `set_lookup_version` calls as `SQL/ShardedPool.py:567-574`.
  At `v0.2.0` (§8's tree) they are `:568-575`: the comment at `:568-569` and the call at
  `:570-575`. At `v0.2.1` they are `:614-621`: the comment at `:614-615` and the call at
  `:616-621`.
  - The other `SQL/ShardedPool.py` citations of §8 hold at `v0.2.0`: `:355-360` (`set_version` on
    every actor) and `:467-470` (step 6 of the comment).
  - At `v0.2.1`, step 6 is `:513-516`.
- **The head.** The contract's head says §1–§7 are `8bc60a5`'s, and that "their line numbers into
  the files 06 changes" are that tree's. That leaves a reader to take §1–§7's line numbers into
  every other file as current. They are not. 09 rewrote the prose, and so moved the lines, of
  files §1–§7 cite that 06 did not change: `store_inventory.py`, `store_reader.py` and
  `SQL/factory_base.py`. 08a and 08b moved `SQL/ShardedPool.py`'s.

  Of the files the contract cites, only `SQL/ClientPool.py` is unchanged from `8bc60a5` to
  `33778b0`. Its §1–§9 are not re-measured here (U37's reasoning: nothing a client supplies
  changed).

### 1.5 The records to collect

- **Prompts and commits.** 01 `8bc60a5`, 02 `e988e69`, 03a `11247c7`, 03b `0d5380c`, 04a
  `7ceed25`, 04b `0c66505`, 05 `68db557`, 06 `240028e`, 07a `dd45243`, 08a `f938844`, 08b
  `efedc8d`, 09 `cad7bc1`, 10 `33778b0`. 07b was withdrawn unwritten. Each has a review commit and
  an orchestration note (the board's notes line).
- **Tags and CI.**
  - `v0.1.0` on `68db557`, after [run 37922626418](https://github.com/ds283/DatastoreKit/actions/runs/37922626418) (444);
  - `v0.2.0` on `240028e`, after [run 37934881027](https://github.com/ds283/DatastoreKit/actions/runs/37934881027) (458);
  - `v0.2.1` on `33778b0`, after [run 38054748108](https://github.com/ds283/DatastoreKit/actions/runs/38054748108) (486).
- **The suite** went from 88 at 01 to 486 at 10. Each log records its count before and after.
- **Issues.** Eight were opened and resolved on this board (§4). The four inherited issues of
  `docs/OPEN_ISSUES.md` §1.2 stay out of scope (U33). Log 01 §4.6 says where each one's code was
  at import.
- **Deviations.** Every log's §2 classifies its deviations. A count of the three labels' words
  over the thirteen §2s gives 67 STRUCTURALLY REQUIRED and 114 IMPLEMENTATION CHOICE, and one or
  two UNINTENDED DRIFT per log, some of which say "none". A word is not an entry. Count the
  entries yourself.
- **Observations not acted on**: about 64 items across the thirteen logs.
- **The commit-point labels** (the user's decision at `98fb497`). `test_reconcile_at_open` uses
  `P1-C`, `C-P3` and `Rn-P3` as runtime strings (from `:307`), and `P3-K` and `P1` in docstrings.
  No file of this repository defines them. Their table is in SGK's records. `git -C <SGK> grep -l
  'Rn-P3' 6f7f291 -- 'prompts/*'` finds `prompts/datastore-integrity/logs/02-repair-or-refuse-at-open.md`
  among three files. Find the defining table, and cite it.
- **The equivalence check at `v0.1.0`.** `docs/extraction/compare_with_source.py`, run from a
  `git archive v0.1.0` export with `venv/`'s Python, exits 0:
  - "files compared: 31";
  - "files ported, checked by compare_ported_tests.py: 20";
  - "files with no source, declared: 10";
  - "OK: every differing line is classified, and every file is accounted for".

  These are 06's last-run counts (U27). It reads SGK through `git show` only.

---

## 2. What to write

### 2.1 `docs/extraction-verification.md`

A new file, named as SGK names its verification documents. It is additive from the day it is
committed (`CLAUDE.md` rule 6). Its head names the campaign, the board, this prompt, the date, and
the package it verifies: `v0.2.1`, `33778b0`.

| § | Section | What it holds |
|---|---|---|
| 1 | What this document is | What the campaign set out to do (README §0, §1, D1–D4), what it delivered, and the headline. That covers the three releases, the suite at both ends, the smoke run, the pin, the issue opened, and what remains. |
| 2 | Reconciliation | **Git history:** a table of every prompt, its commit, review commit and note, the suite count after it, and what it closed or opened. Every other commit on `main` from `8bc60a5` to the commit before 11's, classed: prompt written, note, review, records, decision. **Tags and CI**, as §1.5. **The environment** of every measurement below. |
| 3 | Each prompt's acceptance, at `v0.2.1` | A table: the prompt; its acceptance in brief (README §2 and the prompt's own); what its review found; and what holds at `v0.2.1`, with how it was re-measured or why it cannot be. Re-measure here: the suite at both ends; the port check; the layer guard and the prose guard (in the suite); `black`; §1.5's equivalence check at `v0.1.0`; the wheel's contents (or §5's pin). |
| 4 | The package under Ray (U41) | §2.2's script: the command, the ends, every step's output, the timing, and Ray's processes before and after. §1.3's measurement, re-taken. |
| 5 | The pin (U42) | §2.3's commands and output; the 20 `RECORD` lines compared with 10's wheel. |
| 6 | Issues | The eight resolved, one line each, with the prompt and commit that closed it and the test that pins it, if any. The one 11 opens. The four inherited, each re-located at `v0.2.1` (file and lines). Say whether 08a, 08b or 09 changed the code each describes; read, do not run. |
| 7 | Deviations across the campaign | A table of counts per log and class. Then every UNINTENDED DRIFT entry in one line each, with its log, and every STRUCTURALLY REQUIRED entry that changed what a prompt delivered. |
| 8 | Observations not acted on | Every item of every log's "Observations not acted on", one line each, with its log. Give its disposition at `v0.2.1`: addressed (by which prompt or decision), opened as an issue, still an observation, or no longer true. Decide from the later logs and the board, never by changing anything. |
| 9 | Known gaps | **The commit-point labels:** where the module uses them, that they are defined nowhere here, and where SGK defines them (§1.5; the user's decision). **The contract's line numbers** are each section's tree's (§2.4). **What remains unverified:** G2–G4; a multi-node Ray cluster; each client's own suites under the package. |
| 10 | Reproduction | Every command of §3–§5, verbatim, runnable from a clean checkout of the commit that adds this document. |
| 11 | Summary for the board | Five to ten lines. |

Every fact carries a commit, a `path:line` at a named tree, or a command and its output. A
statement of a log is cited by log and section. Where the document and a log disagree, the
document says which is right and why. It does not rewrite the log.

### 2.2 `docs/extraction/ray_smoke_run.py` (U41)

A script, not a test. It is never collected by the suite, which stays free of Ray (`CLAUDE.md`).
Write it in the form of the other scripts in `docs/extraction/`: a module docstring saying what it
is, how it is run and what it prints, and `black`-clean.
- **How it is run:** with the package importable from a checkout or export, as
  `python docs/extraction/ray_smoke_run.py`. It imports `datastorekit.tests.client` (the neutral
  client), so it needs the tests in the tree, not an installed wheel.
- **It starts Ray itself**, `ray.init(num_cpus=4, include_dashboard=False, log_to_driver=False)`,
  and calls `ray.shutdown()` in a `finally`. It refuses to run if `ray.is_initialized()` is already
  true, or if `pgrep` finds a Ray process before it starts.
- **Every store is in a `tempfile.TemporaryDirectory()`.**
- **The steps are §1.1's**, each an assertion that prints `PASS` or `FAIL` with what it saw:
  - step 2 asserts the caller's payload dicts equal what was passed;
  - step 4 asserts the read-only serials equal the read-write ones;
  - step 5 asserts the exception's type and message;
  - after each pool's `__exit__`, the script records whether its names are held, then drops it.

  It also re-takes §1.3's measurement, as its own named step: a second open while the closed pool
  is referenced raises `ActorAlreadyExistsError`, and the names are free after `del` and
  `gc.collect()`.
- **Its exit code** is 0 only if every step passes. The §1.3 step passes when the behaviour is as
  measured, so the script records the issue's behaviour without failing on it.
- **What it touches.** It patches `build.resolve` to `ray.get` (§1.1). It changes nothing of the
  package, and nothing else of the client.

### 2.3 The pin (U42)

As §1.2, in a fresh scratch venv, from a directory outside the repository. Record the command,
uv's output, `direct_url.json`, the 20-line comparison, and the three checks. **Nothing but the
package is fetched**: install `ray` and `sqlalchemy` offline first, then the package with
`--no-deps`. The venv is deleted after, and nothing of it is committed.

### 2.4 The contract

Two additions, each dated and saying it was made by extraction prompt 11. Nothing else of the file
changes.
- **U34, in place.** In §8's read-only row, `SQL/ShardedPool.py:567-574` becomes `:568-575`, the
  lines at §8's tree. Below §8's table, a dated note says:
  - that this citation was wrong when written (07a's review found it);
  - that it is corrected in place (U34; a correction, not a superseded measurement, rule 6);
  - that at `v0.2.1` the calls are `:614-621` and step 6 of the comment is `:513-516`.
- **The head.** An italic line after the head's last one says:
  - every line number in §1–§9 is its section's stated tree's;
  - since those trees, 08a and 08b moved `SQL/ShardedPool.py`'s lines, and 09 moved the lines of
    every layer file it rewrote (`PROVENANCE.md`'s 08a–09 section), which includes files the
    head's second paragraph leaves a reader to take as unchanged;
  - so a line is read at its section's tree (`git show <tree>:datastorekit/<path>`), and only
    §8's correction note gives `v0.2.1`'s lines.

  Confirm the files the line names against `git diff --stat 8bc60a5 33778b0`.

### 2.5 The issue (§1.3)

On the board's §3, in the form of the closed entries of §4:
- the defect;
- the measurement, from §2.2's script at both ends;
- its cause, by `path:line` at `v0.2.1`;
- that it is inherited, with SGK's lines;
- **the impact**: a client that opens two pools in one process, or reopens while holding a closed
  pool, is refused by Ray;
- the next step: none assigned.

Add its row to `docs/OPEN_ISSUES.md` §1.1 (1 open on this repository, 5 in all), with the header's
count and date.

### 2.6 Closing the campaign

- **The board.**
  - Its header says **CLOSED** (2026-10-10, by prompt 11), with all 14 written prompts landed
    and 07b withdrawn.
  - §1's row for 11.
  - §2's gates are unchanged: G2–G4 have not held, and the campaign does not wait for them
    (README §7).
  - Add a dated line under §2: after the close, a gate is recorded on this board when it holds,
    in a records commit of its own.
- **The campaign README.**
  - Its header and §2's row for 11.
  - A dated line under §7: the campaign closed at 11, with the gates open.
- **`prompts/INDEX.md`**: the campaign's line, **closed**, with its open-issue count.
- **`docs/OPEN_ISSUES.md`**: §2.5's row. The §1.1 heading says the campaign is closed.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **Ray is started once, by the script, at each end, and stopped by it.** Before and after every
   run, `pgrep -lf 'gcs_server|raylet|ray::'` is empty. If a Ray process is up before you start,
   stop and ask. Never `ray start`, never connect to a cluster (`address=`), and never run the
   suite with Ray up.
2. **The network is used once**, for §2.3's `uv pip install` of the package from GitHub. Every
   other venv, install and build is `--offline`. Nothing is downloaded but the package at the
   tag. `git fetch` and `git push` are not run.
3. **The package does not change.** `git diff 41c77c1 -- datastorekit pyproject.toml` is empty at
   the end. A finding is recorded, not fixed (rule 4). The smoke script's patch of `build.resolve`
   is in the script's process only.
4. **Additive documents.** Under `docs/`, the only lines removed are the one `:567-574` → `:568-575`
   (U34). `git diff` of `docs/client-contract.md` shows that line, the note and the head's italic
   line, and nothing else. `docs/adoption/` is unchanged.
5. **No client is touched.** SGK is read only through `git -C <SGK> show|grep` at `6f7f291` and
   `b510bc9`, for §1.3's lines, §1.5's labels and `compare_with_source.py`. No client is written,
   run, imported or opened.
6. **The suite is not run under the smoke script's venv with Ray up.** Run the suite in `venv/`
   and at the high end before the smoke run, and in `venv/` again at the end.
7. **The document is long.** Its tables are built from the records, never from memory. Each count
   it states is one you counted, and the log says how.

---

## 4. Verification

1. **The suite.** In `venv/`, `Ran 486 tests … OK` before and after. At the high end, in a fresh
   offline scratch venv with a `git archive` of your tree installed editable: `Ran 486 tests …
   OK`, with 4 `ResourceWarning` lines.
2. **The checks.**
   - `compare_ported_tests.py` exits 0 with "20 module(s) … 1 test(s) declared not ported".
   - `black --check datastorekit docs` leaves **71** files unchanged (70 and the script).
   - `compare_with_source.py` at `v0.1.0`, as §1.5.
3. **The smoke run** at both ends, as §2.2, each from a fresh offline venv with an export of your
   tree installed editable. The script exits 0. Record its full output, its time, and Ray's
   processes before and after.
4. **The pin**, as §2.3.
5. **The breakage record.** Each is a change exactly as applied, in a scratch export at the high
   end, never committed. Check each diff with `git apply --check` and `-R --check` as recorded.
   - **(a)** `object_get_vectorized` updates the caller's payloads in place again (08a reverted:
     `for value in payload_data: value.update(shard_key)` in place of the copy at
     `SQL/ShardedPool.py:3348`). The script's step 2 fails, naming the key added to the caller's
     dicts. Probed.
   - **(b)** The read-only pool's `set_lookup_version` call removed (`SQL/ShardedPool.py:614-621`).
     The script's step 4 fails, with the actor's `RuntimeError`: it "cannot look up "Tessera" …
     before the serial of label … is set". Probed.
   - **(c)** The pin at the wrong tag, `@v0.2.0`. The version check fails, naming `0.2.0`, and the
     20 lines differ from 10's wheel.
6. **The documents.**
   - Every relative link and anchor in `docs/extraction-verification.md` and the contract's
     additions resolves, checked by a scratch script as 10's was.
   - Every `path:line` the document cites at `v0.2.1` is read at `33778b0`.
   - Every count it states is recounted, and the log says how.
7. **The clients.** Record each client's `HEAD` and `git status --short`, at the start and the end,
   unchanged.

---

## 5. Acceptance

1. `docs/extraction-verification.md` holds §2.1's eleven sections, and every fact in it carries its
   source.
2. `docs/extraction/ray_smoke_run.py` exits 0 at both ends under real Ray, leaves no Ray process,
   and re-takes §1.3's measurement.
3. The pin installs from GitHub, and its 20 package files are 10's wheel's.
4. The contract has §2.4's two additions and one corrected citation, and nothing else changed.
5. `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]` is open on the board and in the
   index, with its measurement.
6. The campaign is closed on the board, in the README, in `prompts/INDEX.md` and in the index.
7. §4.1–§4.7 hold.
8. **The records**, in the same commit:
   - the log, `logs/11-verification-and-close-out.md`, per README §5.1. In place of
     `compare_with_source.py`'s output it has:
     - the port check and `compare_with_source.py` at `v0.1.0`;
     - the smoke runs;
     - the pin;
     - the documents' checks;
     - (a)–(c);
     - the clients' commits and statuses, at the start and the end;
   - the board, as §2.5 and §2.6;
   - `docs/OPEN_ISSUES.md`, as §2.5;
   - `prompts/INDEX.md` and the campaign README, as §2.6.

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count differs from 486, in any venv.
- The smoke script fails at either end in a way that is not §1.3's behaviour. A defect found is
  opened, not fixed (U41). Stop before writing it up, and report.
- The pin does not install, or its 20 package files differ from 10's wheel.
- A Ray process is up before a run, or is left after one.
- Anything would change a file under `datastorekit/`, `pyproject.toml`, `docs/adoption/`, the
  workflow, or any file not in §7.
- Anything would push, make or move a tag, connect to a Ray cluster, download anything but §2.3's
  package, or write, run, import or open anything of a client.

---

## 7. What this prompt changes, and what it does not

- **Files it adds:** `docs/extraction-verification.md`, `docs/extraction/ray_smoke_run.py` and the
  log.
- **Files it changes:**
  - `docs/client-contract.md`, by §2.4 only;
  - `docs/OPEN_ISSUES.md`;
  - the board, the campaign README (its header, §2's row for 11 and §7's line), and
    `prompts/INDEX.md`.
- **It changes nothing else:**
  - no file under `datastorekit/`;
  - not `pyproject.toml`, `README.md` or `PROVENANCE.md`;
  - not `docs/adoption/`, the other scripts of `docs/extraction/` or the workflow;
  - not `CLAUDE.md`, `LICENSE` or `.gitignore`.
- **It touches no client repository.**
- **It makes no tag and pushes nothing.**

---

## 8. The log and the board

`logs/11-verification-and-close-out.md`, using README §5.1, with §5 item 8's additions. The log also
lists the clients' commits and statuses, at the start and the end, and Ray's processes before and
after each run.

`IMPLEMENTATION_STATE.md`: §1's row for 11, the header (**CLOSED**), §2's dated line, and §3's
issue.
