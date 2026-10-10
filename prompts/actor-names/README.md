# Campaign — actor-names

**Written:** 2026-10-10 by Claude Opus 5.5, at the user's request, to fix the one issue the
`extraction` campaign left open on this repository (§0). **Prompt 01 is written** (2026-10-10), and
the user took U1–U3 as recommended the same day (§6). Prompt 02 is written after 01 has landed and been reviewed, against the
tree it leaves.

## 0. Why this campaign exists

`[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]` was opened by extraction prompt 11
on 2026-10-10, from the first run of the package under real Ray. Its measurement, cause and impact
are on the extraction board, [`../extraction/IMPLEMENTATION_STATE.md`](../extraction/IMPLEMENTATION_STATE.md)
§3, and in `docs/extraction-verification.md` §4.5. In brief:
- `ShardedPool` names its actors `SerialPoolBroker` and `shard{key:04d}-store`, in Ray's default
  namespace (`datastorekit/SQL/ShardedPool.py:307`, `:318`, `:592` at `v0.2.1`);
- `__exit__` (`:808-820`) closes each shard and disposes the engine, but releases no actor;
- so a name is freed only when the pool object holding the handles is collected. A store cannot be
  reopened in one Ray session while the previous pool object is still referenced, closed or not:
  `pool = ShardedPool(…)` over a live `pool` builds the new pool before it rebinds the name, and Ray
  refuses it.

It is inherited from SGK, which names the same actors. The suite cannot see it: the stand-in pool
keeps each actor's name but reserves none (`datastorekit/tests/standin_pool.py:162-175`).

### 0.1 Measurements taken by the planner (2026-10-10)

All at `2368535`, whose `datastorekit/` is `33778b0`'s (`v0.2.1`), in scratch exports and offline
scratch venvs at both ends: Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39 and 3.13.16 / 2.55.1 /
2.0.46, SQLite 3.53.4. Nothing was committed.

**How a name can be released**, under a local `ray.init(address="local", …)`. A pool was opened,
written and closed, its actors released, and the store reopened at once **with the closed pool
still referenced**, read-write and read-only, twice each:

| Release | Ray 2.43.0 | Ray 2.55.1 |
|---|---|---|
| `ray.kill(handle, no_restart=True)` on each shard actor and the broker | reopened on the first try, every time | reopened on the first try, every time |
| `handle.__ray_terminate__.remote()`, waited for (a graceful exit after queued work) | reopened on the first try, every time | **refused**: `shard0002-store` still taken after 10 s of retries |

So `ray.kill` frees a name at once at both ends, and a graceful exit does not at 2.55.1.

**A prototype of the fix, under the suite.** In a scratch export:
- `ShardedPool.__exit__` killed each shard actor and the broker after its present body, and set a
  closed flag that makes a second `__exit__` return at once;
- `_close_refused_open` killed what it had made, after its present body;
- the stand-in pool stood in `ray.kill`, reserved each actor's name in its cluster until the handle
  was killed, and logged, without raising, a second creation of a live name and any call to a
  killed handle.

Over the whole suite at the high end:
- `Ran 486 tests … OK`;
- **2,144** stand-in kills (519 brokers; 542, 542 and 541 of the three shards), the positive
  control that the kills were reached;
- **0** calls to a killed handle, **0** creations of a live name, and **0** kills of anything that
  is not a stand-in handle.

So no test touches a closed pool's actors, and no test holds two open pools in one cluster. The
stand-in can reserve names, and refuse calls to killed handles, in every test, not only in a new
module (U2).

**The clients**, read through `git` only, at the adoption checklists' commits (SGK `b510bc9`, CPBH
`52142d7`, SI `7bb3efd`):
- no file outside the layer's own reads a pool's `_shards` or `_broker`, so no client touches an
  actor handle after `__exit__`;
- nothing looks an actor up by name (`ray.get_actor`), in the clients or the package;
- every entry point opens one pool per process. SI's `tests/conftest.py` opens one pool per pytest
  session. No client meets the defect in the code it has now; it is latent.

**A refusal after every actor exists.** `ShardedPool._open` checks `read_table_config` after the
broker and the shards are made and notified (`SQL/ShardedPool.py:345-351`), and the read-only open
checks it last (its step 7, after `:621`). A `read_table_config` naming a sharded class is refused
there; `test_refused_open_closes_engines` already uses it (`:45`, `:238`).

## 1. Scope

**In scope:**
- a closed pool, and a refused open, release their actors' names (U1);
- the stand-in pool standing in `ray.kill` and reserving names (U2), and tests that a regression
  fails;
- `docs/extraction/ray_smoke_run.py` changed to expect the release, and run under real Ray at both
  ends;
- `docs/client-contract.md` §9.3, and a dated subsection of `docs/extraction-verification.md`
  (`CLAUDE.md` rule 6);
- the release of the fix (U3).

**Out of scope:**
- **any client repository** (`CLAUDE.md`). Each adopts in its own campaign;
- **unique actor names, or a namespace per pool** (U1). The fixed names keep one open pool per Ray
  session, which stops two pools on one store from running two serial brokers;
- **the profile agent**, which is the caller's and outlives a pool;
- the four issues inherited from SGK (`docs/OPEN_ISSUES.md` §1.2), and anything else a prompt
  finds: it is recorded, not fixed (§5 rule 4).

## 2. Prompts

| # | Prompt | Covers | Status |
|---|---|---|---|
| 01 | [`01-a-closed-pool-releases-its-actor-names.md`](01-a-closed-pool-releases-its-actor-names.md) | `ShardedPool.__exit__` kills its actors after closing them, and a second `__exit__` does nothing; a refused open kills what it made; the stand-in stands in `ray.kill`, reserves names and refuses calls to killed handles; a test module that a revert fails; the smoke script's step N reversed, and a step that two open pools still collide, run under real Ray at both ends; contract §9.3; a dated subsection of the verification document. **Closes** `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]`. | **written** 2026-10-10; U1, U2 taken |
| 02 | `02-release-v0.2.2.md` (planned) | `pyproject.toml` at `0.2.2`, `README.md`, `PROVENANCE.md`; dated addenda to `docs/adoption/` for the new pin; both ends locally and in CI; **tag `v0.2.2`** on its commit after green CI, not by the prompt. Shaped by U3. | planned |

**Order.** 01 → 02. 02 releases what 01 leaves, and is written after 01 is reviewed.

## 3. Datastores

No prompt opens a store of any client. Tests and the smoke script build their stores in `tempfile`
directories.

## 4. The interfaces between prompts

- **After 01:** `ShardedPool`'s closed flag and its actor release (their names are 01's to choose);
  the stand-in's `ray.kill` and name reservation; the new test module; the smoke script's new
  steps; contract §9.3.
- **After 02:** `pyproject.toml` at `0.2.2`; the adoption addenda. After its CI passes, the tag
  `v0.2.2` on 02's commit.

## 5. The rules this campaign runs under

The project-wide ones in `CLAUDE.md`, plus:

1. **One commit per prompt**, in this repository only.
2. **Every prompt writes a log** to `logs/NN-<name>.md`, using §5.1.
3. **Every prompt updates `IMPLEMENTATION_STATE.md`** in its own commit, plus
   `docs/OPEN_ISSUES.md`.
4. **Do not fix things the prompt did not ask for.** A defect found is recorded with a §3 issue.
5. **No prompt edits a client repository.** Reading one through `git` is allowed. Running a
   client's code or tests, or opening a client's store, is not.
6. **No test needs Ray, imports a client, or opens a store outside a `tempfile` directory.** The
   suite count is recorded before and after each prompt; a count that falls is a stop.
7. **Ray is started only by `docs/extraction/ray_smoke_run.py`**, under extraction prompt 11's
   rules as its script embodies them: `ray.init(address="local", …)`, from a scratch venv, with no
   Ray process up before or left after (shells excluded), and never with the suite running.
8. **Deliberate breakage.** Each prompt names mutations its tests must catch. The log records each
   as a diff, exactly as applied, so the orchestrator can replay it with `git apply`. Mutations are
   never committed.
9. **No tag except where a prompt says so** (02: `v0.2.2`), and none is moved or deleted. No prompt
   pushes.
10. **Verification documents are additive** (`CLAUDE.md` rule 6): a re-run that supersedes a
    measurement is a new dated subsection.

### 5.1 The log template

- the subject, commit and result;
- **What shipped**;
- **Deviations from the prompt**, each classified `STRUCTURALLY REQUIRED`, `IMPLEMENTATION CHOICE`
  or `UNINTENDED DRIFT`;
- **Verification performed**: the suite count before and after, at both ends, and the prompt's own
  checks;
- **The deliberate-breakage record**;
- **Observations not acted on**;
- **State handed to the next prompt**.

## 6. Decisions

### 6.1 Inherited, and not reopened here

The extraction campaign's decisions stand (its README §6), in particular U3 (SGK's layer frozen
from G1 to G2), U4 (clients pin a tagged release), U23 and U28 (a tag is made on its prompt's
commit only after CI passes there, each push and tag with the user's approval), U37 (every client
adopts the release named in the adoption addenda) and U41 (the smoke run).

### 6.2 Decisions this campaign needs

- **U1: how a closed pool releases its names.** *(Taken 2026-10-10, as recommended.)* **Recommended:** at the end of
  `__exit__`, once every shard's `__exit__` has returned and the engine is disposed, `ray.kill`
  each shard actor and the broker (`no_restart=True`), and mark the pool closed so that a second
  `__exit__` returns at once. `_close_refused_open` kills what it made, in the same way. The names
  stay as they are. Measured (§0.1): `ray.kill` frees a name at once at both ends, and no client
  touches a pool's actors after `__exit__`. A closed pool's handles are dead afterwards, which the
  contract says. **Rejected:**
  - a graceful exit (`__ray_terminate__`), which left a name taken for over 10 s at Ray 2.55.1;
  - unique names, or a namespace per pool. Two pools could then be open at once on one store,
    each with its own serial broker handing out the same serials. Today's collision prevents that,
    and the recommended fix keeps it for open pools;
  - dropping the handles (`self._shards = {}`) instead of keeping them killed. It is not needed to
    free the names (the probe reopened with the closed pool's handles still held), and code that
    reads `pool._shards` after `__exit__` would meet an empty dict rather than a dead actor.
- **U2: the stand-in pool.** *(Taken 2026-10-10, as recommended.)* **Recommended:** the stand-in stands in `ray.kill` inside
  `StandinCluster.active()`, as it does `ray.get`. Each `StandinCluster` reserves an actor's name
  when its constructor succeeds, and frees it when the handle is killed. A second creation of a
  live name raises `ValueError` with Ray 2.43.0's message. A call to a killed handle returns a
  reference that raises `StandinActorDied`. **Always on**, in every test: the prototype met no
  collision and no call to a killed handle over the 486 (§0.1), so a regression fails the suite
  widely, not one module only. The stand-in is stricter than Ray in one way, said in its
  docstring: Ray also frees a name when the last handle is collected, and the stand-in only when
  it is killed. **Rejected:** name reservation opt-in per cluster, which would leave only the new
  module able to see a regression; no stand-in change, which is not possible: an unpatched
  `ray.kill` refuses a stand-in handle, and every test that closes a pool would fail.
- **U3: the release.** *(Taken 2026-10-10, as recommended; needed by 02, not 01.)* **Recommended:** **`v0.2.2`**, made by 02 as
  10 made `v0.2.1`, with adoption addenda saying each client adopts `v0.2.2` in place of `v0.2.1`.
  No client has adopted `v0.2.1` (G2–G4 are open), so no pin moves twice. Patch-level, as U36:
  no API is added, nothing the layer writes changes, and the one behaviour that changes (a closed
  pool's handles are dead) is one no client relies on (§0.1). **Rejected:**
  - holding the fix on `main` until another change needs a release. The clients would adopt
    `v0.2.1` with the defect latent, and move again later;
  - `v0.3.0`, treating dead handles after `__exit__` as a change of behaviour.

## 7. Gates outside this repository

The extraction campaign's G2–G4 (each client's adoption) are recorded on the extraction board when
they hold. Under U3, the release they adopt is `v0.2.2`; 02's addenda say so. This
campaign does not wait for them.
