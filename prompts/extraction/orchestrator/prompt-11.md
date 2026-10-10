# Orchestrator — prompt 11, verification and close-out

Read [`../README.md`](../README.md) first: §1, §2 (every row), §4, §5 (rules 4, 5, 7 and 10),
§6.2 (U27, U30, U33, U34, U37, U41 and U42) and §7. Then read [`prompt-10.md`](prompt-10.md)
§0's "Conventions", which this note keeps unless it says otherwise, and the board's review of 10
with its `v0.2.1` record.

**You do not write code.** You may:
- run the suite, the port check, `black --check`, the guards and `compare_with_source.py` from a
  `git archive v0.1.0` export;
- make venvs in the session scratchpad with `uv pip install --offline`, from the cache 05's work
  filled;
- export the tree with `git archive` into the scratchpad, and run probes, the smoke script and
  breakages there, never in this checkout and never committing one;
- start Ray **only** as the prompt's §3 allows the agent: a local instance from a scratch venv,
  stopped by the same process, with no Ray process up before or left after;
- reach the network only for one `git ls-remote origin` at dispatch and at the review, and for
  the review's own replay of the pin (§3 check 6);
- read the three clients only through `git -C <client> rev-parse|status|show|grep`, at SGK
  `6f7f291` and `b510bc9` and the clients' `HEAD`s;
- fix small residue in a follow-up commit of your own (§4);
- after the review, and only with the user's approval, push `main` as §5 says.

**The prompt:** [`11-verification-and-close-out.md`](../11-verification-and-close-out.md)
**Closes:** the campaign (U30, U33) · **Narrows:** nothing · **Changes:** nothing · **Opens:**
`[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]`, and only what else the work
finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- 10 landed (`33778b0`) and was reviewed (`92ad43d`). CI passed there at both ends, and `v0.2.1`
  is tagged on it (tag object `0ba2e4d`), recorded at `41c77c1`. 11 is written (`7209e5c`).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- From `41c77c1` to `7209e5c` only four files under `prompts/` changed. So `datastorekit/`,
  `docs/`, `README.md`, `PROVENANCE.md` and `pyproject.toml` are `33778b0`'s
  (`git diff --stat 33778b0 7209e5c -- datastorekit docs pyproject.toml` is empty), and the
  prompt's facts "at `41c77c1`" are the tree's.
- `origin/main` is `41c77c1`, an ancestor of local `main`, which is one commit ahead of it at
  `7209e5c` (two with this note). `git ls-remote origin` gives `v0.1.0` peeling to `68db557`,
  `v0.2.0` to `240028e` and `v0.2.1` (tag object `0ba2e4d`) to `33778b0`, the local tags'.
- The clients' `HEAD`s: SGK `b510bc9` (branch `handover-remedial`, clean), CPBH `52142d7`
  (`main`, 23 untracked entries), SI `7bb3efd` (`main`, clean).
- The board's §3 holds no issue of this repository, and the index is **4**, all inherited.
- One prompt at a time in this checkout. 11 is the campaign's last.

## 0. What makes this prompt unusual

**It is the first prompt to start Ray and the first to reach the network** (U41, U42). Each is
done for one purpose, and each has a hazard that the prompt's own text does not close. Corrections
1–5 below are about those two things.

**The package does not change, so the suite cannot catch a bad document.** It passes whatever the
verification document says. What stands in for it:
- the smoke script, which is the only thing that runs the layer as real Ray actors;
- the pin, which is the only thing that sees what a client's `requirements.txt` installs;
- hazard 3's `git diff`, which must be empty over `datastorekit/` and `pyproject.toml`;
- reading: the document's every count recounted, every `path:line` read at its tree, every link
  resolved.

The review is therefore mostly reading, and the two runs.

**It closes the campaign with the gates open.** G2–G4 have not held, and the campaign does not
wait for them (README §7). After this prompt a gate is recorded on the board when it holds, in a
records commit of its own.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-10 at `7209e5c`, in `venv/`,
in offline scratch venvs at both ends, under a local Ray started and stopped by the probe, and in
scratch exports. Pass them on. Corrections 1–6 change what the agent does or writes, and are
STRUCTURALLY REQUIRED. Corrections 7 and 8 correct what the prompt states; the log records each as
found.

1. **`ActorAlreadyExistsError` does not exist at the low end.** At Ray 2.43.0,
   `ray.exceptions` has no `ActorAlreadyExistsError`. The second open of §1.3 raises the builtin
   `ValueError`, with the same message: "The name SerialPoolBroker (namespace=None) is already
   taken. Please use a different name or get the existing actor using …". At 2.55.1 it raises
   `ray.exceptions.ActorAlreadyExistsError`, whose base is `ValueError`. Probed at both ends.
   - The script's §1.3 step asserts **`ValueError` with "is already taken" and
     `SerialPoolBroker` in its message**, and prints the exception's module and class at each end.
     A script that names `ray.exceptions.ActorAlreadyExistsError` fails at the low end with
     `AttributeError`.
   - The document's §4 and the board's issue give both types, one per end.
   - Wherever the prompt says `ActorAlreadyExistsError` (§1.3, §2.2), read "the name collision,
     `ValueError` at 2.43.0 and its subclass `ActorAlreadyExistsError` at 2.55.1".
2. **The prompt's `pgrep` matches shells, not only Ray.** `pgrep -lf 'gcs_server|raylet|ray::'`
   matches any process whose command line contains one of those words. That includes:
   - the shell that runs the command, since the Bash tool's `zsh -c` wrapper carries the
     command's own text;
   - other sessions' shells on this machine. At writing, another session (a separate project's
     orchestration) was running commands that contain the same pattern.

   Probed: the probe's own `pgrep`, run from Python, listed the orchestrator's `zsh -c` wrapper
   before one run and another session's after another, with no Ray process up either time.
   - **A Ray process is a line whose command is not a shell.** The script drops every line whose
     command starts with `zsh`, `bash` or `sh`, with or without `/bin/` or a leading `-`, and
     prints what it dropped. It refuses only on what is left.
   - The agent applies the same rule to its own before-and-after checks, and records the raw
     output too. A Ray process up is a `raylet`, a `gcs_server`, a `ray::…` process or a
     `default_worker.py`, under any venv. That is hazard 1's stop.
   - Without this, the script refuses on its own caller whenever the agent runs `pgrep` and the
     script in one command.
3. **`ray.init()` with no address may connect to a cluster.** With no `address`, Ray first tries
   `RAY_ADDRESS`, then the last cluster `ray start` recorded in `/tmp/ray/ray_current_cluster`.
   Neither is set at writing (`RAY_ADDRESS` unset; no such file). Another session on this machine
   works with Ray, so this can change.
   - **Use `ray.init(address="local", num_cpus=4, include_dashboard=False,
     log_to_driver=False)`.** `"local"` always starts a new local instance, and never connects to
     an existing one. That is what hazard 1's "never connect to a cluster (`address=`)" means.
   - The script also refuses to run when `RAY_ADDRESS` is set.
   - Probed at both ends: it starts a local instance at `127.0.0.1` in 7–11 s, and
     `ray.shutdown()` leaves no Ray process.
4. **The prompt's pin command installs the planner's cached build.** The planner's probe left
   two things in `uv`'s cache:
   - the GitHub clone (`~/.cache/uv/git-v1/db/8a829ebb94aa772b`, with a checkout of `33778b0`);
   - the wheel it built from it (`~/.cache/uv/sdists-v9/git/2db414d934ea4a35/33778b04eafc0b9f`).

   So `uv pip install --no-deps "datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.1"`
   would fetch only the tag's ref from GitHub, and install the cached wheel. With `--offline` it
   refuses ("Remote Git fetches are not allowed because network connectivity is disabled"), so
   the tag is resolved remotely, but the bytes are the planner's.
   - **Into the fresh 3.13.16 venv, install `ray==2.55.1`, `sqlalchemy==2.0.46` and `setuptools`
     offline first.** `setuptools` is the build backend, 84.0.0 from the cache.
   - **Then, from a directory outside the repository, run:**
     `uv pip install --no-cache --no-deps --no-build-isolation --python <venv>/bin/python
     "datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.1"`.
     - `--no-cache` clones from GitHub afresh, into a temporary cache.
     - `--no-build-isolation` builds with the venv's `setuptools`, so nothing comes from PyPI.
       With isolation and no cache, the build would need `setuptools>=64` from an index. That is
       a download, which §6 makes a stop.
   - Probed offline, with the same flags and `git+file:///Users/ds283/Documents/Code/DatastoreKit@v0.2.1`:
     - it installs `datastorekit==0.2.1` from `33778b04eafc0b9f01f5e272eb0f9b679eb6f0c7`;
     - `direct_url.json` records `"requested_revision":"v0.2.1"` and that commit;
     - the dist-info adds `INSTALLER`, `REQUESTED`, `direct_url.json` and `uv_build.json`, as
       §1.2 says;
     - the 20 `RECORD` lines under `datastorekit/` are identical to those of the wheel built from
       `git archive 33778b0` with `uv build --offline --wheel`;
     - from outside the repository with `PYTHONPATH` unset, the package imports from
       `site-packages`, the version is `0.2.1`, and `import datastorekit.tests` raises
       `ModuleNotFoundError`.

     Only the transport differs from the agent's run. The `https` transport is the planner's.
   - The log says the build was not isolated, and why. The 20 lines are content hashes of the
     package's files, so they do not depend on the backend's version.
   - If the sandbox refuses the fetch, lift it for that one command, and say so in the log. At
     writing, `git ls-remote origin` worked from inside the sandbox.
5. **Breakage (c) would reach the network a second time.** §4.5(c) installs the pin at `@v0.2.0`.
   From GitHub that is a second fetch, which hazard 2 forbids ("used once"; "nothing is
   downloaded but the package at the tag").
   - **Install (c) from this repository instead:** `git+file:///Users/ds283/Documents/Code/DatastoreKit@v0.2.0`,
     with correction 4's flags, offline. The local `v0.2.0` is `origin`'s (`9eaf542`, peeling to
     `240028e`, by `git ls-remote origin`).
   - Probed: it installs `datastorekit-0.2.0.dist-info`. The version check names `0.2.0`. Its
     `RECORD` has 20 lines under `datastorekit/`, of which **13 differ** from 10's wheel. Those
     are the 13 layer files 08a–09 changed (`git diff --stat 240028e 33778b0`).
   - (c) is the record of a wrong pin, not a second test of GitHub.
6. **Hazard 4 forbids what §2.5 and §2.6 require of `docs/OPEN_ISSUES.md`.** Hazard 4 says the
   only line removed under `docs/` is the U34 citation. But the index's rule (`CLAUDE.md`) rewrites
   three of its lines:
   - the header's count and date (`:6`);
   - the §1.1 heading (`:10`), which §2.6 says names the campaign as closed;
   - "None open (since prompt 09, 2026-10-10)." (`:12`), which the issue's row replaces.

   The index is not a verification document. **Read hazard 4 as:**
   - under `docs/` other than `docs/OPEN_ISSUES.md`, the only removed line is the U34 citation;
   - `docs/OPEN_ISSUES.md`'s diff is those three lines and the new row, and nothing else.
7. **Two cited files are unchanged, not one.** §1.4 says that of the files the contract cites,
   only `SQL/ClientPool.py` is unchanged from `8bc60a5` to `33778b0`. `object.py` is cited too
   (`docs/client-contract.md:183`) and is also unchanged. The contract also cites test modules
   (`tests/client/factories.py`, `tests/client/objects.py`, `tests/standin_pool.py` and four
   test modules) that did not exist at `8bc60a5`. The head's italic line (§2.4) says only what
   holds, by `git diff --stat 8bc60a5 33778b0`.
8. **The timings are this machine's load, not the package's.** At writing, `ray.init` took
   15–20 s and the probe's whole sequence 40–72 s. The prompt says about 5 s and 10–13 s. Another
   session was running a suite. The script asserts no timing. The document records what each run
   measured, and when.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **Work in this order:**
  1. the baseline: 486 in `venv/` and at the high end, side by side, with no Ray up; the port
     check; `black --check datastorekit docs`, 70 files; `compare_with_source.py` at `v0.1.0`; the
     clients' `HEAD`s and statuses; Ray's processes (correction 2);
  2. the smoke script; then its runs at both ends, each from a fresh offline venv with an export
     of the working tree installed editable;
  3. (a) and (b), each in its own export at the high end;
  4. the pin (correction 4) and (c) (correction 5);
  5. the contract (§2.4);
  6. the issue (§2.5) and the index;
  7. the document;
  8. the closing records (§2.6);
  9. `venv/`'s suite again, the port check, `black`, the documents' checks, the clients again,
     Ray's processes again.
- **The script prints its environment first:** Python, Ray, SQLAlchemy and SQLite versions,
  `importlib.metadata.version("datastorekit")` (the package has no `__version__`), and
  `datastorekit.__file__`. Its output is
  then self-describing, and §4 of the document can quote it.
- **Each step is caught, and Ray still stops.** A step that raises prints `FAIL` with the
  exception's type and message, and the script goes on to drop the pool (`del` and
  `gc.collect()`) and `ray.shutdown()` in its `finally`. Under breakage (b) the failure arrives as
  `ray.exceptions.RayTaskError(RuntimeError)` from an actor (probed). A step that depends on a
  failed one is reported as not run, not as passed.
- **Ray's own files.** `ray.init` writes a session directory under `/tmp/ray/`, Ray's default.
  The log names the session directories its runs made. Nothing of them is deleted, and no other
  session's is touched.
- **Keep the documents' check as a scratch script**, never committed, as 10's was. It extracts
  every relative link and anchor from `docs/extraction-verification.md` and
  `docs/client-contract.md`, resolves each file, and finds each anchor among the target's headings
  by GitHub's rule. It also lists every `path:line` the document cites at `v0.2.1`, and prints
  each line from `git show 33778b0:<path>`. The log gives its method and its output.

**The facts, checked by the orchestrator.** Pass them on.

- **§1.1 reproduces at both ends**, from scratch venvs made offline with an export of `33778b0`
  installed editable: low 3.12.15 / 2.43.0 / 2.0.39, high 3.13.16 / 2.55.1 / 2.0.46, SQLite 3.53.4
  at both. The probe built the pool as the prompt says, and patched `build.resolve` to `ray.get`.
  - Step 1: `write_every_class` gives the prompt's counts, class by class.
  - Step 2: the keyed vectorized get of the first alias's two Tesserae finds serials `[1, 2]`, and
    the caller's dicts are unchanged.
  - Steps 3 and 4: the same serials after a read-write reopen and from a read-only pool.
  - Step 5: an open with `Weave` left out of `sharded_tables` is refused with `RuntimeError`
    "Mismatch between sharded tables supplied to the constructor and read from the existing
    ShardedPool".
  - Step 6: a read-write open after it works.
  - At 2.55.1, `ray.init` prints a `FutureWarning` about an environment variable it will stop
    overriding. It is Ray's, and harmless.
- **§1.3 reproduces at both ends**, with correction 1's types:
  - after `__exit__`, with the pool referenced, `SerialPoolBroker` and `shard0000-store` to
    `shard0002-store` are all found by `ray.get_actor`;
  - a second open then fails on `SerialPoolBroker`;
  - after `del` and `gc.collect()`, none is found;
  - after the refused open's exception is dropped, none is found, and step 6 opens.
- **The cause's lines hold at `v0.2.1`:** `SQL/ShardedPool.py:307` (the broker), `:318`
  (read-write shards), `:592` (read-only shards) and `:808-821` (`__exit__`, which releases no
  actor). SGK names the same actors at `Datastore/SQL/ShardedPool.py:294`, `:305` and `:544`, at
  both `6f7f291` and `b510bc9`.
- **Breakages (a) and (b) reproduce**, at the high end, each as a diff to an export of
  `33778b0`:
  - (a): `:3348`'s `payload_data = [{**value, **shard_key} for value in payload_data]` replaced by
    `for value in payload_data:` / `value.update(shard_key)`. Step 2's dicts come back with `'k'`
    added, holding the alias. Steps 3 and 4 see the same.
  - (b): `:614-621` deleted, the comment and the call. Step 4 raises from `shard0002-store`:
    `cannot look up "Tessera", whose lookups are keyed on the version serial, before the serial of
    label "standin" is set: the pool sets it with set_version, or with set_lookup_version on a
    read-only pool. Nothing was looked up`.

  Ray was stopped after each, with no process left.
- **The contract's lines** (§1.4) hold.
  - At `240028e`, `SQL/ShardedPool.py:568-569` is the comment and `:570-575` the
    `set_lookup_version` call. `:355-360` is `set_version` on every actor, and `:467-470` is step
    6 of the comment.
  - At `33778b0`, the call is `:614-621` and step 6 `:513-516`.
  - The head's last line is `docs/client-contract.md:15` (§9.2's). §8's table ends at `:228`;
    "**What is not keyed.**" follows at `:230`. The correction note goes between the two.
  - `PROVENANCE.md`'s section on 08a–09 is "Prompts 08a, 08b and 09: fixes and prose (`v0.2.1`)",
    at `:118`.
- **The commit-point labels.** `git -C <SGK> grep -l 'Rn-P3' 6f7f291 -- 'prompts/*'` gives the
  prompt's three files. That grep cannot find the table that defines the labels, which writes
  them with an en dash (`Rn`–`P3`). The definitions are:
  - **the definition:** SGK `prompts/datastore-integrity/logs/01-checked-replicated-write.md` at
    `6f7f291`, "## The commit points of each replicated path" (`:125`). Its legend is `:127`, and
    its table of the paths after the change is `:150-167`, where `P1`–`C`, `C`–`P3`, `Rn`–`P3`
    and `P3`–`K` are its rows;
  - **where they name the tests:** log 02 of the same campaign, `:245-264`, a table from each
    state to the `TKR` tests by label ("P1-C", "C-P3").

  The document cites both, by path and line at `6f7f291`. `test_reconcile_at_open` uses the
  labels from `:307`, as the prompt says.
- **§1.5's records hold.**
  - §4 of the board holds eight resolved issues.
  - The words of the three labels over the thirteen logs' §2 give 67 STRUCTURALLY REQUIRED,
    114 IMPLEMENTATION CHOICE and 15 UNINTENDED DRIFT, one or two per log.
  - A count of list items in the "Observations not acted on" sections gives 64.

  These are word and item counts, as the prompt warns. The agent counts entries.
- **The equivalence check at `v0.1.0` reproduces.** From a `git archive v0.1.0` export,
  `venv/bin/python docs/extraction/compare_with_source.py` exits 0 with the prompt's four lines.
  It also runs `git -C <SGK> log -1` on the import commit, a read of the kind hazard 5 allows.
- **The toolchain.**
  - `venv/`: Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39, SQLite 3.53.4, `black` 25.1.0, with
    `datastorekit 0.2.1` installed editable from this checkout.
  - `uv` 0.12.20.
  - The high end, `uv venv --offline -p /opt/local/bin/python3.13`, is Python 3.13.16, Ray 2.55.1,
    SQLAlchemy 2.0.46 and SQLite 3.53.4. The low-end scratch venv uses `/opt/local/bin/python3.12`
    (3.12.15).
- **Expected counts.**
  - The suite: **486**, before and after, at both ends; 4 `ResourceWarning` lines at the high end,
    none in `venv/`.
  - `compare_ported_tests.py`: exit 0, "20 module(s) … 1 test(s) declared not ported".
  - `black --check datastorekit docs`: **70** files before, **71** after.
  - The index: **4** now; **5** after, 1 of them this repository's.
- **Ray.** No Ray process was up at writing, by correction 2's rule.

**What the review exists to establish.**
- **(E1) Scope.** Only the prompt's §7 files change, and nothing under `datastorekit/`.
- **(E2) The smoke run.** The script runs under real Ray at both ends, exits 0, re-takes §1.3,
  leaves no Ray process, and fails under (a) and (b) as recorded.
- **(E3) The pin.** What GitHub serves at `v0.2.1` is 10's wheel, by the 20 lines, and (c) is
  told apart from it.
- **(E4) The contract.** One line corrected and two additions, dated, and true at their trees.
- **(E5) The document.** Eleven sections. Every count recounted, every `path:line` true at its
  named tree, every link resolved, and every log disagreement said.
- **(E6) The issue and the close.** The issue on the board and in the index, with its
  measurement; the campaign closed in the four places §2.6 names.
- **(E7) Both ends.** 486 in `venv/` and at the high end, with no Ray up.

**Conventions.** 10's note's, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff **as recorded in the log** with `git apply --check` and `-R --check`
  against a scratch export;
- read a client only through `git`, and never import or run its code;
- use a subdirectory of the session scratchpad, never `/tmp`, for venvs, exports, wheels and
  probes, and put **no scratch `.py` under `datastorekit/` or `docs/`**: the smoke script is the
  only new `.py`, and it is the prompt's;
- a stop goes to the user;
- check `git log` before committing.

And for this prompt, in place of 10's:
- **Ray is started only by the smoke script**, with correction 3's call, from a scratch venv,
  never from `venv/` while its suite runs, and never with the suite running anywhere.
- **The network is used once**, for correction 4's install. Every other venv, install and build is
  `--offline`. (c) is offline (correction 5).
- **No push, no tag, and no change to the GitHub repository's settings.**
- **Nothing is built in the checkout.** `venv/` is not reinstalled: it already holds `0.2.1`.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. Record `git status --short
   --ignored` (at writing: `.idea/`, `venv/` and five `__pycache__/` directories).
2. **The baseline.** In `venv/`, the suite gives `Ran 486 tests … OK`; the port check exits 0;
   `black --check datastorekit docs` leaves 70 files unchanged; `pip show datastorekit` says
   `0.2.1`.
3. **The clients.** Each `HEAD` is the gate's, and `git status --short` is as the gate says.
4. **The remote.** `git ls-remote origin` shows `main` at `41c77c1…`, and the three tags as the
   gate says, and no other.
5. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`, raw and with correction 2's rule
   applied. Record `RAY_ADDRESS` and whether `/tmp/ray/ray_current_cluster` exists.
6. **uv's cache.** Record that `~/.cache/uv/git-v1/db/8a829ebb94aa772b` exists (correction 4).
7. **The index.** 4 now, and 5 after. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `PROVENANCE.md`, `docs/client-contract.md`, and every log under `logs/`;
- `HEAD`, the clients' `HEAD`s and statuses, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's eight corrections and five additions. Corrections 1–3
are the ones that would break the smoke run, and correction 4 the one that would make U42's
install the planner's.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/11-verification-and-close-out.md`, in README
  §5.1's form, with the prompt's §5 item 8 and §8 additions.
- **The files it may change are the prompt's §7 list, and nothing else.** It must not touch:
  - anything under `datastorekit/`, or `pyproject.toml`, `README.md` or `PROVENANCE.md`;
  - `docs/adoption/`, the other scripts of `docs/extraction/`, or the workflow;
  - `CLAUDE.md`, `LICENSE` or `.gitignore`;
  - anything under `orchestrator/`.
- **Under `docs/`, it removes one line** (U34), besides the index's three (correction 6).
- **It writes nothing in any client repository, and runs, imports or opens nothing of one.**
- **It reaches the network once**, for the pin (correction 4).
- **It starts Ray only by the smoke script**, at each end, and leaves no Ray process.
- **It pushes nothing, makes no tag, and changes no setting of the GitHub repository.**
- **Stop and ask** on any of the prompt's §6 conditions, and on a Ray process up by correction 2's
  rule before a run.

## 3. The review — twelve checks

Make the review's venvs and exports fresh, offline, in a subdirectory of the scratchpad of their
own, not the agent's.

1. **Scope.** `git show --stat <commit>` touches only:
   - `docs/extraction-verification.md` and `docs/extraction/ray_smoke_run.py`, both new;
   - `docs/client-contract.md` and `docs/OPEN_ISSUES.md`;
   - the log, the board, the campaign README and `prompts/INDEX.md`.

   No venv, wheel, `dist/`, `build/`, `*.egg-info` or scratch file. `git status --short --ignored`
   lists the same entries as at dispatch. Each client's `HEAD` and `git status --short` are as at
   dispatch.
2. **E1 and E4, the diffs.**
   - `git diff <parent> <commit> -- datastorekit pyproject.toml README.md PROVENANCE.md
     docs/adoption .github` is empty, and so is the diff of the other scripts of
     `docs/extraction/`.
   - `docs/client-contract.md`'s diff is the one citation (`:567-574` → `:568-575`), the note
     after §8's table and the head's italic line, and nothing else.
   - `docs/OPEN_ISSUES.md`'s is correction 6's three lines and the new row.
3. **E4, the contract, by reading.** Each addition is dated and says it is extraction prompt 11's.
   The note says the citation was wrong when written (07a's review), is corrected in place (U34;
   rule 6), and gives `v0.2.1`'s `:614-621` and `:513-516`. The italic line is true by
   `git diff --stat 8bc60a5 33778b0`, and says nothing correction 7 corrects.
4. **E2, the script, by reading.** A module docstring in the form of the other scripts. It is not
   collected by the suite: its name does not match `test*.py`, and `docs/` is not under `-s
   datastorekit/tests`. It refuses on `ray.is_initialized()`, on `RAY_ADDRESS`, and on a Ray
   process by correction 2's rule. It calls correction 3's `ray.init`, and `ray.shutdown()` in a
   `finally`. Every store is in a `TemporaryDirectory`. It patches only `build.resolve`, in its
   own process. The §1.3 step asserts correction 1's `ValueError`. It exits 0 only if every step
   passes. `black --check` passes on it.
5. **E2, the runs.** In the review's own offline venvs at both ends, each with `git archive
   <commit>` installed editable:
   - the script exits 0, and its output matches the log's step by step, the exception's class
     at each end among it;
   - the process check before and after gives no Ray process.
6. **E3, the pin.** Into the review's own fresh 3.13.16 venv, with correction 4's command, from
   outside the repository: the 20 lines equal those of a wheel built from `git archive 33778b0`,
   and the log's. `direct_url.json` is the log's. The three checks hold. This is the review's one
   use of the network beyond `ls-remote`. Delete the venv after.
7. **E2 and E3, the breakages.** Extract (a), (b) and (c) from the log. Check (a)'s and (b)'s
   diffs with `git apply --check` and `-R --check` against their own exports of the commit, and
   run the script under each at the high end:
   - (a): step 2 fails, naming `'k'`;
   - (b): step 4 fails with the actor's `RuntimeError`.

   Replay (c) offline as correction 5 says: `0.2.0`, and 13 of the 20 lines differ.
8. **E5, the document, by reading and by running.**
   - Eleven sections, in §2.1's order, with a head naming the campaign, the board, the prompt, the
     date, `v0.2.1` and `33778b0`.
   - §2's tables agree with `git log --oneline 8bc60a5..<parent>`: every commit is listed and
     classed. The tags, CI runs and counts are the board's.
   - §3's re-measurements are the log's, and the review's own runs agree.
   - §6's four inherited issues are re-located at `v0.2.1` by `path:line` that the review reads
     at `33778b0`.
   - §7's counts: recount the entries of three logs' §2 by hand, 04a's, 08b's and 09's among
     them, and compare.
   - §8: pick ten items across the logs, and check each disposition against the later logs and
     the board.
   - §9 cites SGK's log 01 table and log 02 for the labels, at `6f7f291`.
   - The review's own link check resolves every relative link and anchor in the document and the
     contract. Every `path:line` it cites at `v0.2.1` is read at `33778b0`.
9. **E6, the issue.** On the board's §3, in the form of §4's entries: the defect, the
   measurement at both ends from the script, the cause at `v0.2.1`, SGK's lines, the impact, and
   no assignment. The index's row is under §1.1, with the header at 5 (1 of this repository) and
   the date.
10. **E6, the close.** The board's header says **CLOSED** (2026-10-10, by prompt 11), with all 14
    written prompts landed and 07b withdrawn. §1's row for 11, and §2's dated line. The README's
    header, §2's row for 11, and §7's dated line. `prompts/INDEX.md`'s line says **closed**, with
    1 open issue. The index's §1.1 heading says the campaign is closed.
11. **E7, both ends.** In `venv/`, `Ran 486 tests … OK`. In a fresh high-end venv with `git
    archive <commit>` installed editable, `Ran 486 tests … OK`, with 4 `ResourceWarning` lines.
    No Ray process up during either. The port check exits 0 with 04b's counts. `black --check
    datastorekit docs` leaves 71 files unchanged.
12. **Nothing left behind.** No Ray process, by correction 2's rule. The agent's pin venv is gone.
    `git tag -l` is the three tags, and `origin` is unchanged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 11* paragraph, in the form of
  10's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log, in the document's head if it uses the
    phrase, in the README and in `prompts/INDEX.md`;
  - "reviewed" for 11, in the board's header, its row, README §2 and `prompts/INDEX.md`;
  - the notes line, with this note marked "used for 11".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
  The campaign is closed, so such an issue is assigned to no campaign, and the review says so.
- **Report to the user:**
  - what landed: the verification document, the smoke script, the contract's correction and two
    additions, the issue, and the close;
  - the smoke run at both ends, from the review's own venvs, with the two exception types;
  - the pin's 20 lines, and (c);
  - (a) and (b);
  - the 486 at both ends;
  - the campaign closed with G2–G4 open, and the index at 5;
  - **and ask whether to push `main`** (§5).

## 5. Pushing the close

11 makes no release and no tag (rule 10). Its commit and the records after it are on local `main`
only, ahead of `origin/main` (`41c77c1`). Pushing is an outward-facing act: **ask the user, and
wait for a clear yes.**

1. With approval, `git push origin main`. It fast-forwards from `41c77c1`, carrying 11's prompt,
   this note, 11's commit and the review's records. The workflow runs on the pushed head, at both
   ends; the script is not collected by the suite, so CI does not start Ray.
2. **Read the run** once it has finished: `gh run list --workflow tests.yml --commit <head>`. Do not
   poll in a loop. Ask the user to say when it has finished, or check once when they return.
   Record its URL and both verdict lines on the board in a records commit of its own, and push
   that with approval too.
3. **If either end fails**, record the failure on the board's §3 with the job's log lines, open it
   in the index, and tell the user. No tag is involved, and nothing is reverted without the user.

**Hand on.** There is no next prompt. A later campaign starts from:
- `docs/extraction-verification.md`, the campaign's record, and its §9's known gaps;
- `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]`, open and unassigned;
- the four inherited issues, still SGK's (U33);
- G2–G4, recorded on this board as they hold, each in a records commit of its own.
