# Prompt 01 — a closed pool releases its actor names

**Campaign:** [`README.md`](README.md) · **Board:** [`IMPLEMENTATION_STATE.md`](IMPLEMENTATION_STATE.md)

**Gate:**
- U1 and U2 are taken (README §6.2). If either is taken otherwise than recommended, this prompt is
  amended before it is dispatched.
- `git status` is clean in this repository, and `origin/main` is an ancestor of `main`.
- `datastorekit/` is `33778b0`'s (`v0.2.1`): `git diff --stat 33778b0 HEAD -- datastorekit` is empty.

**Closes:** `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]`. **Narrows:** nothing.
**Opens:** only what the work finds.

**Recommended model:** **Opus.**
- The code change is small, but it is in the pool's close and refusal paths, which every test and
  every client run through.
- The stand-in pool's change touches every test that closes a pool, and must stay faithful to Ray.
- It starts Ray, for the smoke run only, under README §5 rule 7.

**Read first:**

1. [`README.md`](README.md): all of it, §0.1 and §6.2 especially.
2. `/Users/ds283/Documents/Code/DatastoreKit/CLAUDE.md`.
3. The issue's entry on the extraction board, [`../extraction/IMPLEMENTATION_STATE.md`](../extraction/IMPLEMENTATION_STATE.md)
   §3, and `docs/extraction-verification.md` §4 (the smoke run, §4.5 the issue's measurement).
4. Extraction log 08b (`../extraction/logs/08b-dispose-engines-on-a-refused-open.md`), §1 and §2:
   how `_close_refused_open` came to be, and its test module.
5. Extraction log 11 (`../extraction/logs/11-verification-and-close-out.md`), §2 items 1–4 and
   23: how the smoke script finds Ray's processes, starts Ray and catches the name collision.
6. The code: `datastorekit/SQL/ShardedPool.py` (`__init__` and `_open`, `:95-373`;
   `_close_refused_open`, `:375-408`; `_open_read_only`, `:525-636`; `__exit__`, `:808-820`),
   `datastorekit/tests/standin_pool.py` (all of it), `datastorekit/tests/test_refused_open_closes_engines.py`
   and `docs/extraction/ray_smoke_run.py`.
7. `docs/client-contract.md` §9 (its form), and `docs/OPEN_ISSUES.md`.

Line numbers are at `2368535`, whose `datastorekit/` is `33778b0`'s, measured on 2026-10-10.

---

## 1. What is wanted

After this prompt, **a closed pool releases its actors' names**, and so does a refused open:
- a store can be reopened in the same Ray session while the closed pool object is still
  referenced, read-write or read-only;
- a refused open leaves no name taken, even while its exception, and so the half-built pool, is
  held;
- a second `__exit__` does nothing;
- **two open pools still collide**: a second open while a pool is open is refused by Ray, naming
  `SerialPoolBroker`, as today. The names do not change (U1).

The suite sees it. The stand-in pool reserves names and kills handles as Ray does (U2), so a revert
of the fix fails the suite. The smoke script sees it under real Ray, at both ends.

**Nothing the layer writes changes.** No API is added. `pyproject.toml` stays at `0.2.1`: 02
releases.

### 1.1 What the planner measured

README §0.1 holds the measurements. The ones this prompt rests on:
- `ray.kill(handle, no_restart=True)` frees a name at once at Ray 2.43.0 and 2.55.1. A graceful
  `__ray_terminate__` left `shard0002-store` taken for over 10 s at 2.55.1. Use `ray.kill`.
- A prototype of §2.1 and §2.2 passed the 486 at the high end. Its stand-in killed 2,144 handles,
  met **no** call to a killed handle and **no** second creation of a live name, and was handed
  nothing to kill that was not a stand-in handle.
- No client reads `_shards` or `_broker` outside the layer, or looks an actor up by name.

---

## 2. What to change

### 2.1 `datastorekit/SQL/ShardedPool.py` (U1)

1. **A closed flag.** `__init__` sets it false before `self._open(...)` (`:203`), so that it exists
   whenever a pool object does.
2. **`__exit__`** (`:808-820`):
   - returns at once if the pool is closed;
   - otherwise runs its present body unchanged: every shard's `__exit__`, waited for; the profile
     agent's `clean_up`; the engine disposed;
   - then kills each shard actor and the broker, if there is one (a read-only pool has none,
     `:588`), with `ray.kill(handle, no_restart=True)`, and marks the pool closed.

   The handles stay in `self._shards` and `self._broker`, killed (U1: not dropped).
3. **`_close_refused_open`** (`:375-408`) kills what it made, after its present body: each shard
   actor built so far, and the broker if it exists. `self._shards` is the shard count until the
   actors exist, and `self._broker` may not be set yet (the broker is made at `:307`, after the
   check at open). Like the rest of the method, a kill that raises is ignored, so the caller sees
   the open's own exception.
4. **One helper** does the killing for both. It kills the shards first and the broker last, and it
   never raises.
5. **The profile agent is not killed.** It is the caller's, and outlives a pool.
6. **The prose.** `__exit__` gains a docstring saying what it closes, that it releases the actors'
   names, that the handles are dead afterwards, and that a second call does nothing.
   `_close_refused_open`'s docstring says it releases the names too. No other prose changes. The
   prose guard (`test_prose_names_no_source`) and the layer guard (`test_layer_is_generic`) must
   still pass: name nothing of the source repository or of any client.

### 2.2 `datastorekit/tests/standin_pool.py` (U2)

1. **`ray.kill` is stood in**, inside `StandinCluster.active()`, beside `ray.get` (`:232`). The
   stand-in kill marks the handle killed and frees its name in its cluster. Killing a handle
   twice, or killing a killed one, does nothing. Anything that is not a stand-in `Handle` raises
   `ValueError`, as Ray's `ray.kill` refuses what is not an actor handle.
2. **Names are reserved per `StandinCluster`.** `_Options.remote` (`:168-175`) reserves its name
   once the actor's constructor has returned: a constructor that raises reserves nothing. A second
   creation of a name that a live handle holds raises `ValueError` with Ray 2.43.0's message:
   `The name {name} (namespace=None) is already taken. Please use a different name or get the
   existing actor using ray.get_actor('{name}', namespace='None')`.
3. **A killed handle is dead.** A call to it returns a `StandinRef` that raises `StandinActorDied`,
   naming the actor and the method, without running anything. It is not added to the cluster's
   call log and runs no hook.
   - **Careful:** `Handle.__getattr__` (`:147-160`) answers every attribute the handle lacks with
     a `_Method`. A killed flag must be read from the instance's `__dict__`, never with
     `getattr(handle, "killed", False)`, which is always truthy. The planner's first measurement
     made exactly this mistake.
4. **Always on** (U2). No test opts in or out.
5. **The module docstring** says what is stood in, as it does for `ray.get`, and the one way the
   stand-in is stricter than Ray: Ray also frees a name when the last handle is collected, and the
   stand-in only when the handle is killed.

### 2.3 A new test module, `datastorekit/tests/test_closed_pool_releases_its_names.py`

On the neutral client and the stand-in pool, as `test_refused_open_closes_engines` is built. Each
test opens its pools in one `StandinCluster` (one Ray session), in a `tempfile` directory, and
**keeps the closed or refused pool referenced** while it reopens:

1. **A read-write pool releases its names at `__exit__`.** Open, write, close, keep the pool; a
   read-write reopen works, and a get through it finds what was written.
2. **A read-only pool releases its names at `__exit__`.** As 1, with a read-only pool first, then a
   read-write reopen.
3. **A refused open releases its names.** An open with a `read_table_config` naming a sharded class
   (refused after every actor exists, `SQL/ShardedPool.py:345-351`), with the exception held (for
   example as `assertRaises`' context's `exception`); then an open works.
4. **Two open pools still collide.** With a pool open, a second open raises `ValueError` naming
   `SerialPoolBroker`. The first pool still serves a get afterwards, and once it is closed an open
   works.
5. **A second `__exit__` does nothing.** It raises nothing, and adds nothing to the cluster's call
   log.
6. **A closed pool's handles are dead.** A call through one of its `_shards` handles after
   `__exit__` raises `StandinActorDied` on `ray.get`.

Name and word the tests as the suite's other modules are. The module's docstring says what it pins
and cites this campaign and the issue.

### 2.4 `docs/extraction/ray_smoke_run.py`

The script asserts today's behaviour in its step N: names held after `__exit__` while the pool is
referenced. After §2.1 that step fails. Change the script to assert the fixed behaviour, and keep
the rest:
- **Step N, reversed:** after the read-write pool's `__exit__`, with the pool still referenced, no
  name is held, and a second read-write open works at once. The step drops the second pool before
  the next.
- **A new step, "two open pools collide":** with a pool open, a second open raises `ValueError`
  with "is already taken" and `SerialPoolBroker` in its message (the builtin `ValueError` at
  2.43.0, `ActorAlreadyExistsError` at 2.55.1, extraction log 11 §2 item 1). The first pool then
  serves the same get.
- **The record after each `__exit__`** expects no name held, for every pool.
- The script keeps dropping each pool before the next open: a client should be able to omit it now,
  but the script's other steps do not test that.
- Its docstring, and the issue reference in it, say what is now measured. The steps before and
  after (1–6) are unchanged.

Run it at both ends under README §5 rule 7, each from a fresh offline venv with an export of the
working tree installed editable, as extraction prompt 11 did (`docs/extraction-verification.md`
§10.2). It exits 0 at both.

### 2.5 `docs/client-contract.md`

A new subsection, **§9.3**, in §9's form ("Each subsection is measured from the package at the tree
of the prompt that names it"), headed for this campaign's prompt 01. Its rows:
- `ShardedPool.__exit__`: what it closes; that it releases the actors' names, so the store can be
  reopened in the same Ray session while the closed pool is referenced; that the handles are dead
  afterwards; that a second call does nothing. By `path:line` at this prompt's tree.
- A refused open: that it releases the names it took (beside §9.2's engine disposal).
- Two open pools: still refused by Ray's name collision, since the names are fixed.

It names the row of §1–§9 it supersedes, if any, and changes no other line of the file.

### 2.6 `docs/extraction-verification.md`

A new dated subsection at the end of §4, after §4.5, saying it was added by `actor-names` prompt 01
(`CLAUDE.md` rule 6). It gives the smoke run's new output at both ends (step N reversed, the new
step), and says that §4.5's measurement was of `v0.2.1` and stays true of it. Nothing above it
changes.

### 2.7 The issue

- **On the extraction board** (`../extraction/IMPLEMENTATION_STATE.md`): the entry moves from §3 to
  the head of §4 with a "**Closed** (date, by `actor-names` prompt 01, this commit)" line naming
  the fix, the test module and the smoke run. §3 then says no issue of this repository is open on
  that board. The board's header is otherwise unchanged: that campaign stays closed.
- **On this campaign's board:** §4 gets a pointer to it.
- **`docs/OPEN_ISSUES.md`:** its row in §1.3 is deleted; the count becomes 4 (0 on this
  repository's boards); the date is updated.

---

## 3. Hazards

Check each, and say in the log what you found.

1. **Ray.** README §5 rule 7. Ray is started only by the smoke script, at each end and for (e),
   with no Ray process up before or left after, by the script's own check. The suite never runs
   while Ray is up.
2. **No network.** Every venv and install is `uv … --offline`.
3. **The package changes in `SQL/ShardedPool.py` only**, and there only in `__init__`'s flag,
   `__exit__`, `_close_refused_open` and the new helper. `git diff -- datastorekit` outside the
   three files of §7 is empty.
4. **The stand-in stays faithful.** It must not make a test pass that Ray would fail. Its new
   strictness (a name held until killed) is said in its docstring.
5. **Additive documents.** Under `docs/`, the contract gains §9.3 and the verification document a
   subsection, and neither loses a line. `docs/OPEN_ISSUES.md` changes by its rule.
6. **No client is touched.** Nothing of a client is written, run, imported or opened.
7. **A count that falls is a stop.** The suite is 486 before. After, it is 486 plus the new
   module's tests, at both ends.

---

## 4. Verification

1. **The suite.** In `venv/`, `Ran 486 tests … OK` before, and `Ran <486 + n> tests … OK` after,
   where n is the new module's count. The same at the high end, in a fresh offline venv (Python
   3.13 / Ray 2.55.1 / SQLAlchemy 2.0.46) with an export of your tree installed editable. Record the
   `ResourceWarning` lines at each end (0 and 4 before). If the count changes, say why.
2. **The checks.** `compare_ported_tests.py` exits 0 with "20 module(s) … 1 test(s) declared not
   ported". `black --check datastorekit docs` passes (71 files before; 72 after, with the new
   module). The two guards pass.
3. **The smoke run** at both ends, as §2.4: exit 0, its full output, its time, and Ray's processes
   before and after.
4. **The breakage record.** Each is a diff, exactly as applied, to its own scratch export, never
   committed, checked with `git apply --check` and `-R --check` as recorded. Run the suite under
   each, or the named module where said, and record which tests fail:
   - **(a)** the kill removed from `__exit__`. The new module's tests 1, 2 and 6 fail, and, since
     the stand-in reserves names in every test, most modules that reopen a store fail too: record
     the count.
   - **(b)** the kill removed from `_close_refused_open`. Test 3 fails.
   - **(c)** the closed flag's early return removed from `__exit__`. Test 5 fails.
   - **(d)** the broker named per pool (`name=f"SerialPoolBroker-{id(self)}"`, and the same for the
     shards). Test 4 fails.
   - **(e)** under real Ray, at the high end only: (a) applied, and the smoke script run. Step N
     fails, naming the collision.
   - **(f)** in the stand-in, a call to a killed handle allowed to run. Test 6 fails.
5. **The documents.** Every relative link and anchor in what you add resolves. Every `path:line`
   you cite is read at your tree.
6. **The clients.** Record each client's `HEAD` and `git status --short`, at the start and the end,
   unchanged.

---

## 5. Acceptance

1. A closed pool, read-write or read-only, and a refused open release their actors' names. A second
   `__exit__` does nothing. Two open pools still collide.
2. The stand-in pool stands in `ray.kill`, reserves names and refuses calls to killed handles, in
   every test.
3. The new module's six tests pass, and §4.4's breakages fail as stated.
4. The smoke script exits 0 at both ends under real Ray, with step N reversed and the new step, and
   leaves no Ray process.
5. The contract has §9.3, and the verification document its subsection.
6. The issue is closed on the extraction board, pointed to from this board, and gone from the
   index.
7. §4.1–§4.6 hold.
8. **The records**, in the same commit: the log `logs/01-a-closed-pool-releases-its-actor-names.md`
   per README §5.1, with the smoke runs, the breakage record and the clients at both ends; this
   campaign's board (its row for 01, §4, and the header); the extraction board (§2.7);
   `docs/OPEN_ISSUES.md`; `prompts/INDEX.md`; and this campaign's README (its header and §2's row
   for 01).

---

## 6. Stop conditions — stop and ask the user

- The suite fails, or its count falls, in any venv, other than under a breakage.
- An existing test fails once the stand-in reserves names or refuses calls to killed handles. The
  planner measured none; one would mean a test holds two open pools or touches a closed pool, and
  whether that test or U2 gives way is the user's call.
- The smoke script fails at either end, other than under (e).
- `ray.kill` does not free a name at once at either end.
- A Ray process is up before a run, or left after one.
- Anything would change a file outside §7, push, make or move a tag, download anything, or write,
  run, import or open anything of a client.

---

## 7. What this prompt changes, and what it does not

- **Files it adds:** `datastorekit/tests/test_closed_pool_releases_its_names.py` and the log.
- **Files it changes:**
  - `datastorekit/SQL/ShardedPool.py`, by §2.1 only;
  - `datastorekit/tests/standin_pool.py`, by §2.2 only;
  - `docs/extraction/ray_smoke_run.py`, by §2.4;
  - `docs/client-contract.md`, by §2.5, and `docs/extraction-verification.md`, by §2.6;
  - `docs/OPEN_ISSUES.md`;
  - this campaign's board and README (its header and §2's row for 01), the extraction board
    (§2.7), and `prompts/INDEX.md`.
- **It changes nothing else:** not `pyproject.toml`, `README.md`, `PROVENANCE.md`, `docs/adoption/`,
  the other scripts of `docs/extraction/`, the workflow, `CLAUDE.md`, `LICENSE` or `.gitignore`.
- **It touches no client repository.**
- **It makes no tag and pushes nothing.**
