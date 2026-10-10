# Log 11 — verification and close-out

**Subject:** Verify the extraction campaign and close it · **Commit:** this commit ·
**Date:** 2026-10-10 · **Model:** Claude Opus 5.5 · **Result:** landed; unpushed and untagged.
The campaign is closed.

`docs/extraction-verification.md` verifies the campaign from the package as tagged `v0.2.1`
(`33778b0`) and the records of 01–10, in the eleven sections of the prompt's §2.1. For the first
time in the campaign, the package ran under real Ray, and the pin was installed from GitHub.

- **U41.** The new script `docs/extraction/ray_smoke_run.py` starts a local Ray instance of its
  own, runs the neutral client through the layer's real actors, and exits 0 at both ends. Ray
  leaves no process. The script also fails under breakages (a) and (b) as the prompt records.
- **U42.** `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.1`, installed from
  GitHub with no cache, is `33778b0`. Its 20 package `RECORD` lines are identical to those of 10's
  wheel, rebuilt offline from `git archive 33778b0`. (c), the pin at `@v0.2.0`, differs in 13
  lines, and its version check fails.
- **The issue.** The smoke run re-took the planner's finding, and it is opened as
  `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]`, on the board's §3 and in the
  index. The index has **5 open**, 1 of them this repository's.
- **The contract.** `docs/client-contract.md` has one citation corrected in place, U34's
  `SQL/ShardedPool.py:567-574` → `:568-575`. It gains a dated correction note below §8's table and
  a dated italic line after its head.
- **The close.** The campaign is closed on the board, in the campaign README, in
  `prompts/INDEX.md` and in the index.

**No line of the package changed.** `git diff 41c77c1 -- datastorekit pyproject.toml` is empty.
The suite is **486** before and after: in `venv/`, with 0 `ResourceWarning` lines, and at the high
end, with 4. Nothing was pushed or tagged. The network was reached once, for the pin. No client was
written, run, imported or opened. SGK was read only through `git show` and `git grep`, at
`6f7f291` and `b510bc9`.

Prompt: [`../11-verification-and-close-out.md`](../11-verification-and-close-out.md), with the
orchestrator's dispatch note §0: eight corrections, five additions, its checked facts and its
conventions. §2 classifies each.

---

## 1. What shipped

### 1.1 `docs/extraction-verification.md` (§2.1)

A new file, 860 lines. Its head names the campaign, the board, this prompt and its log, the date,
and the package it verifies (`v0.2.1`, `33778b0`, tag object `0ba2e4d`). It says it is additive.
It has the eleven sections of §2.1:

1. what the campaign set out to do and delivered, and the headline;
2. the reconciliation: every prompt with its commit, note, review, suite count and issues; the 46
   other commits from `8bc60a5` to `ec059c8`, classed; the tags and CI; the environment of every
   measurement;
3. each prompt's acceptance, its review's finding, and what holds at `v0.2.1`, with §3.1's
   re-measurements;
4. the smoke run: the command, both ends' full output, the steps, the times, Ray's processes and
   session directories, (a) and (b), and §1.3's measurement re-taken;
5. the pin: the commands, uv's output, `direct_url.json`, the 20 `RECORD` lines, the three checks,
   and (c);
6. the issues: the eight resolved, the one opened, and the four inherited, each re-located at
   `v0.2.1`;
7. the deviations: counts per log and class, every UNINTENDED DRIFT, and every STRUCTURALLY REQUIRED
   entry that changed what a prompt delivered;
8. all 64 observations, each with its disposition at `v0.2.1`;
9. the known gaps: the commit-point labels, with SGK's definitions cited; the contract's line
   numbers; what remains unverified;
10. the reproduction commands;
11. the summary for the board.

### 1.2 `docs/extraction/ray_smoke_run.py` (§2.2, U41)

A new script, 547 lines, `black`-clean. Its module docstring says what it is, how it is run and
what it prints, in the form of the other scripts in `docs/extraction/`.

- **Imports.** It imports `ray`, `sqlalchemy`, the package, and the tests' neutral client
  (`datastorekit.tests.client.build` and `.registry`). It is run from a checkout or an export with
  the package installed editable.
- **Refusals.** It refuses to run (exit 2) when `RAY_ADDRESS` is set, when `ray.is_initialized()`,
  or when `pgrep -f` finds a Ray process whose executable is not a shell (§2 items 3 and 16).
- **Ray.** It calls `ray.init(address="local", num_cpus=4, include_dashboard=False,
  log_to_driver=False)` and `ray.shutdown()` in a `finally`, then waits up to 30 s for Ray's
  processes to go.
- **The store and the pool.** The store is in a `tempfile.TemporaryDirectory()`. The pool is built
  as `StandinCluster.open_pool` builds it, with the label `"standin"`, three shards, the registry,
  `read_table_config` and `serial_batch_sizes`.
- **The patch.** `build.resolve` is patched to `ray.get` with `mock.patch.object`, in the script's
  process only.
- **The steps.** Step 1 writes every class; step 2 makes the keyed vectorized get of the caller's
  dicts. Step N re-takes §1.3's measurement. Step 3 reopens read-write and step 4 opens read-only.
  Step 5 is the refusal with `Weave` left out; step 6 opens read-write after it. After every pool's
  `__exit__` the script records whether its names are held, then drops the pool.
- **Its output.** Each step is caught. It prints `PASS`, `FAIL` (the exception's type and the last
  line of its message) or `NOT RUN` (a step it needs failed). The script exits 0 only if every step
  passes and no Ray process is left. It prints its environment first (addition 2).

### 1.3 `docs/client-contract.md` (§2.4)

The diff is 24 lines added and 1 removed, the U34 line (§4.5 below):
- §8's read-only row: `SQL/ShardedPool.py:567-574` → `:568-575`;
- below §8's table, before "**What is not keyed.**": a dated note, "*Correction (extraction prompt
  11, 2026-10-10; decision U34).*". It says the citation was wrong when written (07a's review), that
  it is corrected in place as a correction under rule 6, and that §8's other two citations hold.
  It gives `v0.2.1`'s lines: the calls `:614-621` (the comment `:614-615`, the call `:616-621`) and
  step 6 `:513-516`;
- after the head's last line (`:15`): an italic paragraph, "*Added by extraction prompt 11
  (2026-10-10).*". It says every line number is its section's tree's, with §6's one citation of
  `tests/standin_pool.py` being 02's tree. It says that 08a, 08b and 09 moved the lines, naming
  `store_inventory.py`, `store_reader.py` and `SQL/factory_base.py`. It says that only `object.py`
  and `SQL/ClientPool.py` of the cited layer files are unchanged, by `git diff --stat 8bc60a5
  33778b0`, and that a line is read at its section's tree.

### 1.4 The records

- **The board.** The header reads **CLOSED (2026-10-10, by prompt 11)**, with all 14 written
  prompts landed and 07b withdrawn. §1's row for 11 is landed. §2 has a dated line under its table,
  and §2's gates are otherwise unchanged. §3 has the issue (§2.5), in place of the sentence "No
  issue of this repository is open on this board" (§2 item 20).
- **The campaign README.** The header says 11 landed and the campaign is closed; §2's row for 11
  says landed and closed; §7 has a dated line.
- **`prompts/INDEX.md`.** The header has "1 campaign: 1 closed". The campaign's line reads
  **closed**, with its open-issue count, 1.
- **`docs/OPEN_ISSUES.md`.** The header now reads **5 open**, 1 on this repository's boards. The
  §1.1 heading says the campaign is closed, and §1.1 holds the issue's row.
- **This log.**

---

## 2. Deviations from the prompt

1. **Correction 1: the name collision is `ValueError` at the low end.** Step N catches
   `ValueError`, requires "is already taken" and `SerialPoolBroker` in the message, and prints the
   exception's module and class. Measured at each end: the low end raises `builtins.ValueError` and
   the high end `ray.exceptions.ActorAlreadyExistsError`. The document's §4.5 and the board's issue
   give both. **STRUCTURALLY REQUIRED.**
2. **Correction 2: a Ray process is a process that is not a shell.** The script, and my own checks
   before and after every run, drop the shells and record the rest. My checks are
   `<scratch>/probe/raycheck.py`, which prints `pgrep -lf`'s raw lines too. No Ray process was up
   before or after any run (§4.2). **STRUCTURALLY REQUIRED.**
3. **Correction 2, as the script applies it: by process, not by line.** The correction's rule
   reads `pgrep -lf`'s output line by line. On the high end's first run, the script and my check
   both counted 20 "Ray processes" after `ray.shutdown()`. They were the continuation lines of two
   other sessions' `zsh -c` commands, PIDs 1150 and 3081, whose command lines span several lines
   and contain the pattern. Every step of that run had passed, and the script exited 1.
   `ps -axo pid=,comm=` found no `gcs_server`, `raylet` or `default_worker.py`.

   So the script now takes PIDs from `pgrep -f` and classes each by its executable,
   `ps -o comm= -p <pid>`. It drops a `zsh`, `bash` or `sh`, with any leading path or `-`, and shows
   each process by PID, executable and first line. My check does the same. Correction 2's
   description, "the command starts with", is this when a command line spans lines.
   **STRUCTURALLY REQUIRED.**
4. **Correction 3: `ray.init(address="local", …)`**, and the script refuses when `RAY_ADDRESS` is
   set. `RAY_ADDRESS` was unset and `/tmp/ray/ray_current_cluster` absent throughout.
   **STRUCTURALLY REQUIRED.**
5. **Correction 4: the pin.** Into a fresh 3.13.16 venv I installed `ray==2.55.1`,
   `sqlalchemy==2.0.46` and `setuptools` (84.0.0) offline first. Then I ran `uv pip install
   --no-cache --no-deps --no-build-isolation`, from a directory outside the repository with
   `PYTHONPATH` unset (§4.3). **The build was not isolated**, so that nothing came from an index:
   with isolation and no cache, the build would need `setuptools>=64` from PyPI. The 20 lines
   compared are content hashes of the package's files, so they do not depend on the backend. The
   sandbox did not refuse the fetch. **STRUCTURALLY REQUIRED.**
6. **Correction 5: (c) is offline, from this repository**:
   `git+file:///Users/ds283/Documents/Code/DatastoreKit@v0.2.0`, with correction 4's flags and
   `--offline` (§5). **STRUCTURALLY REQUIRED.**
7. **Correction 6: `docs/OPEN_ISSUES.md`'s diff.** It is the header's count and date (`:6`), the
   §1.1 heading (`:10`), and the line "None open (since prompt 09, 2026-10-10)." (`:12`), replaced by
   the issue's row. The row needs the table's header and separator, two more lines, as §1.1 had
   them when it last held an issue (`git show efedc8d:docs/OPEN_ISSUES.md`, `| Issue | Hook |`).
   Under `docs/` otherwise, the only removed line is the U34 citation (§4.5). **STRUCTURALLY
   REQUIRED.**
8. **Correction 7: two cited files are unchanged, `SQL/ClientPool.py` and `object.py`**, by
   `git diff --quiet 8bc60a5 33778b0 -- datastorekit/<file>` over the nine layer files the contract
   cites. The test client's files and `tests/standin_pool.py` are absent at `8bc60a5`
   (`git cat-file -e`). Found as stated. The contract's head line says only what holds; that §6's
   one `tests/standin_pool.py` citation is of 02's tree I checked at `e988e69` (`:55-56` is
   `_copy`'s pickle round trip, `:131` the copied call). **STRUCTURALLY REQUIRED** (an
   expectation corrected).
9. **Correction 8: the timings are the machine's load.** `ray.init` took 13.2 s and 15.8 s in the
   recorded runs, and up to 39.0 s under breakage (a). The whole script took 49.7 s and 72.6 s. The
   prompt says about 5 s and 10–13 s. The script asserts no time, and the document records what
   each run measured. **STRUCTURALLY REQUIRED** (an expectation corrected).
10. **Additions 1–5**, each followed as given and each an **IMPLEMENTATION CHOICE**, at the
    orchestrator's direction:
    - the order of work. The baseline came first, then the script and its runs, (a) and (b), the
      pin and (c), the contract, the issue and the index, the document, the closing records, and
      the final checks;
    - the script prints its environment first;
    - each step is caught, and Ray still stops;
    - Ray's session directories are named, and none is deleted (§4.2);
    - the documents' check is a scratch script, not committed (§4.4).
11. **Step N runs between steps 2 and 3**, as its own step: it needs the closed pool of steps 1
    and 2. Steps 3–6 depend on it and on step 1, since they open the same store. **IMPLEMENTATION
    CHOICE.**
12. **Steps 3, 4 and 6 get the keypoint and the alias again through the open pool.** Each checks
    that the alias's serial is step 1's, before the same vectorized get. On the read-only pool this
    runs two replicated read-only gets under real Ray. Step 2 uses step 1's alias object as
    written. **IMPLEMENTATION CHOICE.**
13. **Step 5 reports what the refused constructor printed** under "sharded tables are configured
    in the existing ShardedPool, but were not supplied to the constructor": `['Weave']` at both
    ends. This is 08a's message for the case. Only the exception's type and message are asserted,
    as §2.2 asks. **IMPLEMENTATION CHOICE.**
14. **Step 1 asserts the written counts class by class**, equal to §1.1's list, and step 2 compares
    the serials with step 1's rather than with a literal `[1, 2]`. That follows 08a's correction 5:
    no serial is a literal. Both ends found `[1, 2]`. **IMPLEMENTATION CHOICE.**
15. **(c)'s version check is an assertion** that the installed version is `0.2.1`, run from
    outside the repository. (c) has a venv of its own (`<scratch>/pin/venv-c`), so that the pin's
    venv held only the pin. Both venvs were deleted after. **IMPLEMENTATION CHOICE.**
16. **The script's `pgrep` pattern adds `default_worker\.py`** to the prompt's
    `gcs_server|raylet|ray::`, since correction 2 names it as a Ray process. **IMPLEMENTATION
    CHOICE.**
17. **The smoke and breakage exports are of the working tree**, made by `git ls-files -z -co
    --exclude-standard | tar …` as log 05 §2 item 1 does, because the script was uncommitted. The
    high-end suite at the start ran on `git archive HEAD` (`ec059c8`). Nothing of mine was in the
    tree then, so that export was my tree. The final high-end suite ran on an export of the final
    working tree. **STRUCTURALLY REQUIRED.**
18. **The note's SGK lines for the label tables, measured.** Log 01's "**After (this commit).**"
    table is `:149-169`: its header is at `:149` and its rows `:151-169`, after the caption at
    `:147`. The note says `:150-167`. Log 02's table is `:242-265`, and its rows naming states by
    label are `:245-264`, as the note says. The legend is `:127-131`. The document cites what I
    measured (§4.4). **STRUCTURALLY REQUIRED** (an expectation corrected).
19. **`__exit__` is `SQL/ShardedPool.py:808-820` at `v0.2.1`, not `:808-821`** (the prompt's
    §1.3 and the dispatch note). `:820` is `self._engine.dispose()`, and `:821` is the blank line
    before `def _create_engine` (`git show 33778b0:… | sed -n 819,822p`). Contract §9.2 gives the
    disposal as `:820-821` at 08b's tree, and 09's prose rewrite moved it up one line. The board's
    issue and the document cite `:808-820`. **STRUCTURALLY REQUIRED** (an expectation corrected).
20. **The board's §3 sentence "No issue of this repository is open on this board (2026-10-10,
    since prompt 09)" is replaced by the issue's entry.** The entry makes the sentence false, and
    the board is not a verification document. **STRUCTURALLY REQUIRED.**
21. **The prompt's deviation counts are word counts, and are right as such.** Counted as entries:
    207 entries, of which 72 are STRUCTURALLY REQUIRED, 119 IMPLEMENTATION CHOICE, 3 UNINTENDED
    DRIFT and 13 unlabelled (§4.7). The 67 and 114 miss five entries each whose label is wrapped
    across two lines. The 15 UNINTENDED DRIFT are twelve "No … UNINTENDED DRIFT" sentences and the
    three entries. The document says so (its §7). **STRUCTURALLY REQUIRED** (an expectation
    corrected).
22. **The contract's head line names 09's file counts** (13 layer files, 30 modules under
    `tests/`), from `PROVENANCE.md`'s 08a–09 section and `git diff --name-only 21334c2 cad7bc1`
    (13 layer files, and 31 under `tests/`, one of them 09's new module). **IMPLEMENTATION
    CHOICE.**
23. **The smoke script's drafts had two faults, each found by a run, and fixed before the
    recorded runs.** The committed script is the third form.
    - The first draft's step N held the first pool in a local variable while it dropped
      `self.pool`. The pool was still referenced, so its names stayed held for the 30-second
      wait, and step N failed at the low end, with steps 3–6 not run. That is §1.3's behaviour
      itself, caused by the script.
    - The second draft's `pgrep` reading was line by line (item 3).
    - Four runs preceded the recorded ones. Their outputs are kept in `<scratch>`, and each left
      no Ray process (§4.2).

    Nothing was committed or recorded from them but this item. **UNINTENDED DRIFT**, corrected,
    with no effect on any recorded result.
24. **The final suites overran the tool's 600-second foreground limit.** They ran side by side,
    `venv/` and the high end, and the tool moved them to the background. Their output went to
    scratch files, as the convention asks. I took the verdicts only after both had exited, and ran
    nothing that depended on them in the meantime: only the documents' check, which runs no test
    and starts no Ray. **UNINTENDED DRIFT**, with no effect on any result (as log 10 §2 item 11).

---

## 3. The hazards (§3)

1. **Ray.** Ray was started only by the smoke script, from scratch venvs, eight times: the four
   draft runs of §2 item 23, the two recorded runs and (a) and (b). It was never started with the
   suite running.
   - By correction 2's rule as item 3 applies it, no Ray process was up before or after any run
     (§4.2).
   - I never ran `ray start` and never passed an address other than `"local"`. `RAY_ADDRESS` was
     unset throughout.
2. **The network.** It was used once, for the pin's `uv pip install --no-cache … git+https://…`.
   Every other venv, install and build was `uv … --offline`, (c) included. No `git fetch`, `git
   push` or `git ls-remote` was run.
3. **The package.** `git diff 41c77c1 -- datastorekit pyproject.toml` is empty at the end. The
   patch of `build.resolve` is in the script's process only. The finding is opened, not fixed.
4. **Additive documents.** `git diff` of `docs/client-contract.md` removes one line, the U34 row.
   It adds that row corrected, the note and the head's paragraph. `docs/OPEN_ISSUES.md` is as §2
   item 7 says. `docs/adoption/` and the other four scripts of `docs/extraction/` are unchanged.
5. **No client is touched.** SGK was read through `git show` and `git grep` at `6f7f291` and
   `b510bc9`, for §1.3's lines, the labels and `compare_with_source.py`; the last also reads SGK
   with `git log -1`. CPBH and SI were not read; their `HEAD` and status were taken with `git
   rev-parse` and `git status`. The clients' `HEAD`s and statuses are unchanged (§4.8).
6. **The suite and Ray.** The suite ran at the start and at the end, each time with no Ray process
   up (`raycheck.py` at 18:51:40, before the final suites). It never ran in a smoke venv.
7. **The document's counts.** Each count is one I counted; §4.7 gives how.

---

## 4. Verification performed

### 4.1 The suite

| When | Where | Result | `ResourceWarning` lines |
|---|---|---|---|
| start (18:07–18:14) | `venv/` | `Ran 486 tests in 413.705s` / `OK` | 0 |
| start, side by side | `<scratch>/base-hi`: `git archive HEAD`, editable, 3.13.16 / 2.55.1 / 2.0.46 | `Ran 486 tests in 419.532s` / `OK` | 4 |
| end (from 18:51:45) | `venv/` | `Ran 486 tests in 1004.790s` / `OK` | 0 |
| end, side by side | `<scratch>/final-hi`: an export of the final working tree, editable | `Ran 486 tests in 1038.874s` / `OK` | 4 |

The verdict was taken with `grep -E '^Ran |^OK|^FAILED' <file>`, and the warnings with
`grep -c ResourceWarning`. `pip show datastorekit` in `venv/` gives 0.2.1, editable from this
checkout; `venv/` was not reinstalled.

### 4.2 The smoke runs (U41)

Every run, with my check before and after it (`raycheck.py`: `pgrep -lf`'s raw lines, then
`pgrep -f`'s PIDs classed by `ps -o comm=`). Every run started from no Ray process.

| Run | Ray's session directory | Script's verdict | Ray after (script; my check) |
|---|---|---|---|
| low, draft 1 | `session_2026-10-10_18-23-07_030424_92497` | exit 1: step N FAIL (§2 item 23), 3–6 NOT RUN | 0; 0 |
| low, draft 2 | `session_2026-10-10_18-24-34_869766_95521` | exit 0 | 0; 0 |
| low, draft 2 plus step 5's report | `session_2026-10-10_18-26-31_466943_98624` | exit 0 | 0; 0 |
| high, draft 2 plus step 5's report | `session_2026-10-10_18-27-08_343241_228` | every step PASS; exit 1 on 20 lines of two other sessions' `zsh` commands (§2 item 3) | 20 lines, line-wise; then 0 by PID and `comm` at 18:29:24 |
| **low, recorded** | `session_2026-10-10_18-30-18_915824_5837` | **exit 0**, every step PASS | 0; 0 (18:30:09 before, 18:31:02 after) |
| **high, recorded** | `session_2026-10-10_18-31-08_834636_7580` | **exit 0**, every step PASS | 0; 0 (18:31:03, 18:32:17) |
| (a), high | `session_2026-10-10_18-33-04_166226_10402` | exit 1: steps 2, 3, 4, 6 FAIL | 0; 0 (18:32:58, 18:34:39) |
| (b), high | `session_2026-10-10_18-34-45_032745_13336` | exit 1: step 4 FAIL | 0; 0 (18:34:39, 18:35:28) |

Each recorded run and each breakage ran from its own fresh export and fresh offline venv. The low
end was 3.12.15 / 2.43.0 / 2.0.39, and the high 3.13.16 / 2.55.1 / 2.0.46, with SQLite 3.53.4 at
both. Each ran from the export's root as `env -u PYTHONPATH <venv>/bin/python
docs/extraction/ray_smoke_run.py`. The recorded runs used the committed script (SHA-256
`83c1b37da3a839c617c64f8d98571ab3098bd8741d4bf2ef982b4a0065fd45e0`, `cmp` equal to each export's
copy). Their full output is the document's §4.2 and §4.3:

| | Low | High |
|---|---|---|
| `ray.init` | 13.2 s | 15.8 s |
| Steps 1, 2, N, 3, 4, 5, 6 | 4.6, 0.0, 0.2, 5.8, 6.9, 0.1, 9.2 s | 3.7, 3.1, 3.1, 11.8, 21.4, 0.1, 7.3 s |
| Whole script (`time -p` real) | 49.7 s (51.39) | 72.6 s (73.87) |
| Step N's exception | `builtins.ValueError` | `ray.exceptions.ActorAlreadyExistsError` |
| Names after the first `del` and `gc.collect()` | none, 0.0 s | none, 0.2 s |

The other sessions' directories under `/tmp/ray/` (sixteen before my first run) were not touched,
and none of mine was deleted.

### 4.3 The pin (U42)

- **The command**, from `<scratch>/pin/outside` at 18:36:01, with `PYTHONPATH` unset:
  `uv pip install --no-cache --no-deps --no-build-isolation --python <scratch>/pin/venv/bin/python
  "datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.1"`. Its output is in the
  document's §5.1. It exited 0, installing `datastorekit==0.2.1` from
  `33778b04eafc0b9f01f5e272eb0f9b679eb6f0c7`.
- **`direct_url.json`**: `{"url":"https://github.com/ds283/DatastoreKit","vcs_info":{"vcs":"git",
  "commit_id":"33778b04eafc0b9f01f5e272eb0f9b679eb6f0c7","requested_revision":"v0.2.1"}}`.
- **The dist-info** holds `direct_url.json`, `INSTALLER` (`uv`), `licenses`, `METADATA`, `RECORD`,
  `REQUESTED` (empty), `top_level.txt`, `uv_build.json` (`{}`) and `WHEEL`.
- **10's wheel**, from `git archive 33778b0` by `uv build --offline --wheel`: 97,849 bytes,
  `RECORD` SHA-256 `f840ffa4c28f1d40f6578abb56a033d6faf4356f4877c62f60ebf75ab2d96c5e` (log 10
  §5.3's), 25 lines, 20 under `datastorekit/`.
- **The 20-line comparison**: `grep '^datastorekit/' RECORD | sort` on each side; `diff` is empty,
  and both sorted files have SHA-256 `90fb77bff20556f97a6efa371b22e4f8b3f7e1d3083d6a715c11981e6b556bf1`.
  The lines are the document's §5.2.
- **The three checks**, from outside the repository: `datastorekit.__file__` and
  `datastorekit.SQL.ShardedPool` are under the venv's `site-packages`; the version is `0.2.1`;
  `import datastorekit.tests` raises "ModuleNotFoundError: No module named 'datastorekit.tests'".
- **Deleted**: `<scratch>/pin/venv` was deleted after (c) was measured.

### 4.4 The checks and the documents

**The port check** (`./venv/bin/python docs/extraction/compare_ported_tests.py`), exit 0, at the
start and the end: "OK: 20 module(s) keep their source's tests, classes and assertion skeletons; 1
test(s) declared not ported".

**`compare_with_source.py` at `v0.1.0`.** It ran from `git archive v0.1.0` in `<scratch>/v010`,
with `venv/`'s Python: `/Users/ds283/Documents/Code/DatastoreKit/venv/bin/python
docs/extraction/compare_with_source.py`. Exit 0:

```text
files compared: 31
files ported, checked by compare_ported_tests.py: 20
files with no source, declared: 10
OK: every differing line is classified, and every file is accounted for
```

**The two guards**, alone in `venv/`: `./venv/bin/python -m unittest
datastorekit.tests.test_layer_is_generic datastorekit.tests.test_prose_names_no_source` gives
`Ran 14 tests in 0.672s` / `OK`.

**`black`** (25.1.0): `./venv/bin/black --check datastorekit docs` left 70 files unchanged at the
start, and 71 files unchanged (70 and the smoke script) at the end.

**The documents' check.** `<scratch>/probe/check_docs.py` is a scratch script, not committed.
- It extracts every relative link of `docs/extraction-verification.md` and
  `docs/client-contract.md`, resolves each file, and finds each anchor among the target's headings
  by GitHub's rule. The rule: lower case; drop all but word characters, hyphens and spaces; spaces
  to hyphens; a repeated slug gains `-1`, `-2`; fenced code skipped.
- It then lists every backticked `path:line` of the verification document whose path is a `.py`
  of this repository, carrying a path forward to the bare `:N` that follow it, and prints each line
  from `git show 33778b0:<path>`.

Its output (links in full; citations by their line at `33778b0`, truncated to 90 characters):

```text
ok  docs/extraction-verification.md: ../prompts/extraction/README.md
ok  docs/extraction-verification.md: ../prompts/extraction/IMPLEMENTATION_STATE.md
ok  docs/extraction-verification.md: ../prompts/extraction/11-verification-and-close-out.md
ok  docs/extraction-verification.md: ../prompts/extraction/logs/11-verification-and-close-out.md
links: 4 relative, 0 bad
citations parsed: 58
datastorekit/SQL/ShardedPool.py:1015: [f'Existing ShardedPool was configured with shard key type "{row.key_type}", but provided t]
datastorekit/SQL/ShardedPool.py:3348: [payload_data = [{**value, **shard_key} for value in payload_data]]
datastorekit/SQL/ShardedPool.py:614-621: [# the version row's serial keys the lookups of a class whose factory declares] .. [)]
datastorekit/SQL/ShardedPool.py:307: [self._broker = SerialPoolBroker.options(name="SerialPoolBroker").remote(]
datastorekit/SQL/ShardedPool.py:318: [key: Datastore.options(name=f"shard{key:04d}-store").remote(]
datastorekit/SQL/ShardedPool.py:592: [key: Datastore.options(name=f"shard{key:04d}-store").remote(]
datastorekit/SQL/ShardedPool.py:808-820: [def __exit__(self, exc_type, exc_val, exc_tb):] .. [self._engine.dispose()]
datastorekit/SQL/Datastore.py:142: [self._drop_tables(drop_tables)]
datastorekit/SQL/Datastore.py:438-469: [def _drop_tables(self, tables):] .. [self._inspector = sqla.inspect(self._engine)]
datastorekit/SQL/Datastore.py:143: [self._ensure_tables()]
datastorekit/SQL/Datastore.py:427-430: [def _ensure_tables(self):] .. [tab.create(self._engine)]
datastorekit/SQL/ShardedPool.py:329: [drop_tables=self._drop_tables,]
datastorekit/SQL/ShardedPool.py:234-257: [if not self._primary_file.exists():] .. [)]
datastorekit/SQL/ShardedPool.py:253: [self._write_shard_data()]
datastorekit/SQL/ShardedPool.py:925-984: [def _write_shard_data(self):] .. [conn.commit()]
datastorekit/SQL/ShardedPool.py:315-333: [shard_ids = list(self._shard_db_files.keys())] .. [}]
datastorekit/SQL/ShardedPool.py:277: [self._check_shard_files()]
datastorekit/SQL/ShardedPool.py:1119-1139: [def _check_shard_files(self):] .. [)]
datastorekit/SQL/ShardedPool.py:203-207: [try:] .. [raise]
datastorekit/SQL/ShardedPool.py:209: [def _open(self, version_label: str, drop_tables, read_table_config, read_only):]
datastorekit/SQL/ShardedPool.py:375: [def _close_refused_open(self) -> None:]
datastorekit/store_inventory.py:53-55: [**Shards.** A sharded class is the union of every shard's records. A replicated class is r] .. [lowest-serial shard's, and any shard that differs is a named problem (``replicated-diverge]
datastorekit/store_inventory.py:826-913: [def _combine(] .. [)]
datastorekit/SQL/ShardedPool.py:2936-2967: [def _failure_message(plan: "_RelocationPlan", step: str, e: Exception) -> str:] .. [return message]
datastorekit/SQL/ShardedPool.py:2962-2966: [if isinstance(e, OSError) and e.errno == errno.EXDEV:] .. [)]
datastorekit/tests/test_copy_move_store.py:596: [def test_move_across_filesystems_fails_before_anything_moves(self):]
datastorekit/tests/test_copy_move_store.py:606: [self.assertIn("copy it instead, and then delete the source by hand", message)]
datastorekit/tests/test_shard_key_audit_copy.py:139: [f"    runpy.run_module('datastorekit.tools.shard_key_audit', run_name='__main__')\n"]
datastorekit/tests/test_sharded_store_script.py:95: [f"    runpy.run_module('datastorekit.tools.sharded_store', run_name='__main__')\n"]
datastorekit/tests/test_shard_paths.py:103: [class TestModuleIsStandalone(unittest.TestCase):]
datastorekit/tests/test_shard_paths.py:113-114: [env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}] .. [env["PYTHONPATH"] = str(repo_root)]
datastorekit/SQL/ShardedPool.py:138: [self._job_name: Optional[str] = job_name]
datastorekit/tests/test_reconcile_at_open.py:820: [def interrupted_tolerance_get(self):]
datastorekit/tests/standin_pool.py:284-308: [def open_pool(self, primary: Path, shards: int = 3, **kwargs):] .. [return pool]
datastorekit/tests/client/factories.py:8-9: [- a **leaf** (``version``, ``store_tag``, ``keypoint``, ``dial_setting``, ``knob_setting``] .. [``GadgetPart``, ``Tessera``) is got or inserted by ``build``. An inserted object carries]
datastorekit/tests/test_read_only_pool.py:452-453: [atol = build.get_gauge(pool, ALIAS_GAUGES[0])] .. [rtol = build.get_gauge(pool, ALIAS_GAUGES[1])]
datastorekit/tests/test_read_only_pool.py:496: [tol = objects.SerialHandle(self.facts["gauge_setting"][ALIAS_GAUGES[0]])]
datastorekit/SQL/ShardedPool.py:567-574: [] .. [)]
datastorekit/SQL/ShardedPool.py:568-575: [num_shards = len(self._shard_db_files)] .. []
datastorekit/tests/test_store_inventory.py:8: [3. what is not identity does not matter: labels, timestamps, payload, solver serials, cosm]
datastorekit/tests/test_shard_key_audit_copy.py:13-15: [Everything is in a temporary directory; no Ray, no datastore. This module does not import] .. [deliberate-breakage record.]
datastorekit/tests/test_reconcile_at_open.py:307: ["P1-C": ([("controller", "object_get", cls, "before")], []),]
datastorekit/tests/test_reconcile_at_open.py:375: ["P1-C": ([("controller", "object_get", cls, "before")], []),]
datastorekit/tests/test_reconcile_at_open.py:422: [for point, when in (("P1-C", "before"), ("C-P3", "after")):]
datastorekit/tests/test_reconcile_at_open.py:432: ["P1-C": ([("controller", "object_store", cls, "before")], []),]
datastorekit/tests/test_reconcile_at_open.py:493: ["P1-C": ([("controller", "object_validate", cls, "before")], []),]
datastorekit/tests/test_reconcile_at_open.py:521: [self.assertEqual([(0 if point == "P1-C" else 1,)], validated)]
datastorekit/tests/test_reconcile_at_open.py:542: [for point, when in (("P1-C", "before"), ("C-P3", "after")):]
datastorekit/tests/test_reconcile_at_open.py:327: ["Rn-P3": ([("r1", "object_get", cls, "after")], []),]
datastorekit/tests/test_reconcile_at_open.py:388: ["Rn-P3": ([("r0", "object_get", cls, "after")], []),]
datastorekit/tests/test_reconcile_at_open.py:443: ["Rn-P3": ([("r1", "object_store", cls, "after")], []),]
datastorekit/tests/test_reconcile_at_open.py:512: ["Rn-P3": ([("r1", "object_validate", cls, "after")], []),]
datastorekit/tests/test_reconcile_at_open.py:551: ["""P3-K: the shards agree and there is no record; the reopen writes nothing, and the next]
datastorekit/tests/test_reconcile_at_open.py:629: ["""The other states a ReplicationMismatch leaves at Rn-P3 with the record set: whatever th]
datastorekit/tests/test_reconcile_at_open.py:908: ["""A store of a model interrupted after its last replica committed (Rn-P3): every shard]
datastorekit/tests/test_reconcile_at_open.py:524: ["""The controller's outcome False is not replicated; a failure at P1-C or C-P3 leaves]
```

`docs/client-contract.md` has no relative link. Of the 56 distinct citations, 53 are `v0.2.1`'s and read true at `33778b0`. Three are other trees' and the document names their tree: `SQL/ShardedPool.py:1015` (`e988e69`'s, in §3's row for 02), and `:567-574` and `:568-575` (§8's citation and its correction, `v0.2.0`'s). The contract's own additions cite `v0.2.0`'s `:568-569`, `:570-575`, `:355-360` and `:467-470`, and `v0.2.1`'s `:614-621` and `:513-516`. I read each with `git show 240028e:…` and `git show 33778b0:…` (`sed -n`), before writing them.

**The breakage diffs as recorded.** The two `diff` blocks of §5 were extracted from this log. Each is byte-identical to the diff applied, and against a fresh export of the working tree each passes `git apply --check`, then, once applied, `git apply -R --check`.

### 4.5 The diffs (hazards 3 and 4, correction 6)

- `git diff 41c77c1 -- datastorekit pyproject.toml`: empty (hazard 3).
- `git diff --stat -- docs/adoption docs/extraction datastorekit pyproject.toml .github README.md PROVENANCE.md CLAUDE.md LICENSE .gitignore`: empty. The smoke script is the one new file under `docs/extraction/`.
- `git diff -- docs | grep '^-[^-]'` gives four lines. Three are `docs/OPEN_ISSUES.md`'s: the header (`:6`), the §1.1 heading (`:10`) and "None open (since prompt 09, 2026-10-10)." (`:12`). The fourth is `docs/client-contract.md`'s §8 read-only row, the U34 line (hazard 4 as correction 6 reads it).
- `docs/client-contract.md`: 24 lines added, 1 removed. The additions are the corrected row, the 13-line head paragraph with its blank line, and the 8-line note with its blank line.

### 4.6 The inherited issues (§6.3 of the document)

`<scratch>/probe/fn_compare.py` parses each named function at `8bc60a5`, `240028e` and `33778b0`
from `git show`, removes docstrings, and compares `ast.dump`:

```text
datastorekit/SQL/Datastore.py Datastore.__init__ 8bc60a5->240028e: CODE DIFFERS; lines at 240028e: 39-148
datastorekit/SQL/Datastore.py Datastore._drop_tables 8bc60a5->240028e: same code; lines at 240028e: 439-470
datastorekit/SQL/Datastore.py Datastore._ensure_tables 8bc60a5->240028e: same code; lines at 240028e: 428-431
datastorekit/SQL/Datastore.py Datastore.__init__ 240028e->33778b0: same code; lines at 33778b0: 39-146
datastorekit/SQL/Datastore.py Datastore._drop_tables 240028e->33778b0: same code; lines at 33778b0: 438-469
datastorekit/SQL/Datastore.py Datastore._ensure_tables 240028e->33778b0: same code; lines at 33778b0: 427-430
datastorekit/SQL/ShardedPool.py ShardedPool._write_shard_data 8bc60a5->240028e: same code; lines at 240028e: 880-939
datastorekit/SQL/ShardedPool.py ShardedPool._check_shard_files 8bc60a5->240028e: same code; lines at 240028e: 1072-1092
datastorekit/SQL/ShardedPool.py ShardedPool._failure_message 8bc60a5->240028e: same code; lines at 240028e: 2896-2927
datastorekit/SQL/ShardedPool.py ShardedPool._write_shard_data 240028e->33778b0: same code; lines at 33778b0: 925-984
datastorekit/SQL/ShardedPool.py ShardedPool._check_shard_files 240028e->33778b0: same code; lines at 33778b0: 1119-1139
datastorekit/SQL/ShardedPool.py ShardedPool._failure_message 240028e->33778b0: same code; lines at 33778b0: 2936-2967
datastorekit/store_inventory.py _combine 8bc60a5->240028e: same code; lines at 240028e: 830-917
datastorekit/store_inventory.py _combine 240028e->33778b0: same code; lines at 33778b0: 826-913
```

`Datastore.__init__` differs at 06 only, which added the lookup serial (log 06 §1.1). The open's
order, primary first and actors after, was read at `33778b0:datastorekit/SQL/ShardedPool.py:234-333`.

### 4.7 How the counts were counted

- **Deviations.** `<scratch>/probe/count_devs.py` takes each log's section whose heading matches
  `\d+\. Deviations`. It splits the section into its top-level numbered items, joining each item's
  lines with single spaces, and classes each by the last of the three labels in it. It reports the
  items with no label, or with UNINTENDED DRIFT, and the lines outside any item.
  - It also counts the labels' words over the section's lines, unjoined. That gives the prompt's
    67, 114 and 15.
  - Every unlabelled item (13), every UNINTENDED DRIFT item (3) and every line outside an item was
    read.
  - Then `<scratch>/probe/sr_list.py` listed the 72 STRUCTURALLY REQUIRED items with their first
    words. I read each and decided which changed a delivered file: 46 did. The other 26 corrected
    an expectation, a count in a log, a breakage record or a procedure.
- **Observations.** The numbered items of each log's "Observations not acted on" section, counted
  by reading the extracted sections: 5, 7, 5, 5, 6, 5, 4, 6, 5, 4, 4, 5, 3, which is 64, the
  dispatch note's figure. Each disposition was decided by reading the later logs and the board,
  and by `git grep` or `git show` at `33778b0`:
  - the f-strings, `test_shard_paths`' `PYTHONPATH` and `job_name`;
  - `interrupted_tolerance_get` and the stand-in's `open_pool`;
  - `factories.py`'s docstring, `test_read_only_pool`'s variables, and the two docstrings 09
    rewrote;
  - `.github`'s history, `test_store_inventory.py:8`, `test_shard_key_audit_copy.py` and
    `.claude/`.

  The document's tally (22, 1, 1, 34, 6) was counted from its own table, by the first words of
  each row's last cell.
- **Commits.** `git log --reverse --format='%h %ad %s' --date=short 8bc60a5^..ec059c8` gives 59,
  classed by subject and by the board's notes line. Before `8bc60a5` there are 6, from the root
  `be6a4bf`.

### 4.8 The clients, at the start and the end

| Client | Start | End |
|---|---|---|
| SGK `/Users/ds283/Documents/Code/SecondaryGWKit` | `b510bc9`, branch `handover-remedial`, `git status --short` empty | `b510bc9`, `handover-remedial`, empty (`cmp` of the two `git status --short` listings: equal) |
| CPBH `/Users/ds283/Documents/Code/ChamPBH` | `52142d7`, `main`, 23 untracked entries | `52142d7`, `main`, the same 23 entries (`cmp`: equal) |
| SI `/Users/ds283/Documents/Code/StochasticInstantons` | `7bb3efd`, `main`, empty | `7bb3efd`, `main`, empty (`cmp`: equal) |

CPBH's 23 at the start: `full_run_2026.6.0-refresh.sh`, `full_run_2026.6.0.sh`,
`pilot-2026.6.0-shard0000.db` to `pilot-2026.6.0-shard0015.db`, `pilot-2026.6.0.db`,
`pilot-main.log`, `pilot-out/`, `pilot-plot.log` and `prompts/jordan-normalization/`.

### 4.9 This repository at the end

Ray: no process by `raycheck.py` after the final suites (19:09:43). The port check exits 0 with its line. `black --check datastorekit docs` leaves 71 files unchanged. `git status --short` lists the five changed records and the three new files, and the ignored entries are dispatch's (`.idea/`, `venv/`, five `__pycache__/`). No `build/`, `dist/` or `*.egg-info`. `git log` before the commit: `HEAD` `ec059c8`, nothing new on the branch.

---

## 5. The deliberate-breakage record (§4.5)

Each change was applied, exactly as below, to its own export of the working tree at the high end.
None was committed. In each export, `git apply --check <diff>` passed before applying, and
`git apply -R --check <diff>` after. Both were checked again as recorded here (§4.4).

**(a) 08a reverted**: the copy at `SQL/ShardedPool.py:3348` replaced by the in-place update.

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 9ea48b0..b354f29 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -3345,7 +3345,8 @@ class ShardedPool:
             self._ShardKeyStoreIdGetter(shard_key[shard_key_field])
         ]
 
-        payload_data = [{**value, **shard_key} for value in payload_data]
+        for value in payload_data:
+            value.update(shard_key)
         return self._shards[shard_id].object_get.remote(
             cls_name, payload_data=payload_data
         )
```

The script exits 1. Steps 2, 3, 4 and 6 fail with "the caller's payload dicts changed: keys added
['k']; 2 dicts, of which 2 differ from what was passed (serials found [1, 2])", and steps 1, N and
5 pass. The prompt names step 2; steps 3, 4 and 6 make the same get, so they see the same, as the
dispatch note found.

**(b) the read-only pool's `set_lookup_version` call removed** (`SQL/ShardedPool.py:614-621`).

```diff
diff --git a/datastorekit/SQL/ShardedPool.py b/datastorekit/SQL/ShardedPool.py
index 9ea48b0..52ee0ea 100644
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -611,14 +611,6 @@ class ShardedPool:
         )
         self.actor_states: Dict[int, dict] = dict(zip(self._shards.keys(), states))
 
-        # the version row's serial keys the lookups of a class whose factory declares
-        # key_on_version; it is given as the lookup serial alone, so no actor can insert
-        ray.get(
-            [
-                shard.set_lookup_version.remote(self._version.store_id)
-                for shard in self._shards.values()
-            ]
-        )
 
         # 7. the read_table_config check
         self._read_table_config: Optional[ReadTableConfigType] = read_table_config
```

The script exits 1. Step 4 fails with `ray.exceptions.RayTaskError(RuntimeError)`, from
`ray::Datastore.object_get()` on `shard0002-store`, in the actor's `_keyed_payloads`: 'Datastore
"shard0002-store": cannot look up "Tessera", whose lookups are keyed on the version serial, before
the serial of label "standin" is set: the pool sets it with set_version, or with set_lookup_version
on a read-only pool. Nothing was looked up'. Every other step passes.

The index line `9ea48b0` is `33778b0:datastorekit/SQL/ShardedPool.py` (`git rev-parse --short`).

**(c) the pin at the wrong tag**:

```bash
uv venv --offline -p /opt/local/bin/python3.13 <scratch>/pin/venv-c
uv pip install --offline --python <scratch>/pin/venv-c/bin/python ray==2.55.1 sqlalchemy==2.0.46 setuptools
cd <scratch>/pin/outside && env -u PYTHONPATH uv pip install --offline --no-cache --no-deps \
    --no-build-isolation --python <scratch>/pin/venv-c/bin/python \
    "datastorekit @ git+file:///Users/ds283/Documents/Code/DatastoreKit@v0.2.0"
```

It installs `datastorekit==0.2.0` from `240028e4514efb69ef9bcaac1847fd27a4c9aa3d`, with
`"requested_revision":"v0.2.0"`. The version check raises "AssertionError: version check:
expected 0.2.1, installed 0.2.0", exit 1. 13 of the 20 `RECORD` lines under `datastorekit/`
differ from 10's wheel. They are exactly the 13 layer files of `git diff --name-only 240028e
33778b0 -- datastorekit`, less `tests/`; `diff` of the two sorted lists is empty. The paths are the
same 20.

---

## 6. Observations not acted on

1. **The smoke script cannot see what happens to a dead actor under Ray.** No step kills one, so
   log 08b §6 item 4 (`RayActorError` in `_close_refused_open`) stays unverified. The document's
   §9.3 says so.
2. **A read-only pool's open under Ray took longest of the steps** at the high end (step 4, 21.4
   s; 16.3 s on the earlier run). The machine was loaded, and nothing measured why. Not a defect.
3. **Another session on this machine works with Ray** (a separate project's orchestration, whose
   commands carry the same pattern, §2 item 3). Its shells came and went during this run; no Ray
   process of its own was seen.
4. **The other sessions' Ray session directories under `/tmp/ray/`**, sixteen at the start, are
   left as they were.
5. **The scratch tools** are in `<scratch>/probe/` and not in the repository: `raycheck.py`,
   `sections.py`, `count_devs.py`, `sr_list.py`, `fn_compare.py` and `check_docs.py`. The exports,
   venvs, wheel and outputs are under `<scratch>`.

---

## 7. Issues

- **Opened**: `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]` (board §3), with
  §4.2's measurement at both ends, its cause at `v0.2.1`, SGK's lines and its impact. It is
  assigned to no campaign.
- **Closed, narrowed**: none.
- **`docs/OPEN_ISSUES.md`**: 4 → **5** open, 1 on this repository's boards; the §1.1 heading says
  the campaign is closed.

---

## 8. State handed on

**The campaign is closed**, and this is its last prompt. A later reader starts from
`docs/extraction-verification.md`.
- **`HEAD`** is this commit, unpushed and untagged. `origin/main` is `41c77c1`, and the tags are
  `v0.1.0`, `v0.2.0` and `v0.2.1`, unchanged. Pushing this commit, after the review, is the user's.
- **The suite** is 486, in `venv/` and at the high end. The port check passes over 20 modules with
  one test declared not ported. `black` leaves 71 files unchanged.
- **The smoke script** is `docs/extraction/ray_smoke_run.py`. It is run by hand under §2.2's
  rules, never by the suite.
- **Open**: the one issue of §7, unassigned, and the four inherited issues of
  `docs/OPEN_ISSUES.md` §1.2. G2–G4 are open; each is recorded on the board when it holds, in a
  records commit of its own.
- **Scratch** (not in the repository): `<scratch>` holds `base-hi`, `smoke-lo`, `smoke-hi`,
  `break-a`, `break-b` and `final-hi` (each an export and its venv). It also holds `v010`, `pin/`
  (the wheel, the export of `33778b0`, the `RECORD` extracts and uv's output; the pin's two venvs
  deleted), `breaks/` (the two diffs), `probe/`, and every run's output.
