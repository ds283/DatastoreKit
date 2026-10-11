# factory-defaults campaign — implementation state

**Last updated:** 2026-10-11 · **Status: IN PROGRESS — 2 of 2 prompts written, 1 landed (01,
`f5d8957`, reviewed); U1–U5 taken 2026-10-11, as recommended; 02 is written, against `97c9a8e`,
and ready for its orchestration note.**

**Campaign:** [`README.md`](README.md) ·
**Owns:** no issue. It carries out the user's ruling of 2026-10-11 (README §0), revisits extraction
U32 in part (U1), and addresses extraction 07a's observation §7.3
(`docs/extraction-verification.md` §8) ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md)

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

### Decisions

**Put to the user (README §6.2), U1–U5 taken 2026-10-11:**

| Decision | Recommendation | Status |
|---|---|---|
| **U1** what the base becomes, and how U32 is recorded | `store`, `validate`, `validate_on_startup` lose `@abstractmethod`, stay static with today's signatures and bare `NotImplementedError`; the base stays an `ABC` with `register` and `build` as its only abstract hooks, so a class defining both instantiates; a dated note on extraction U32, not a rewrite | the change: **the user's ruling** 2026-10-11; its form: **taken** 2026-10-11, as recommended |
| **U2** the tests | a new module of instances, a parameterised factory, the two abstract hooks, the defaults (direct and through the pool), a `cloudpickle` round trip and `_defines`; `ABSTRACT_HOOKS` corrected; the neutral registry unchanged | **taken** 2026-10-11 |
| **U3** Ray | a smoke step I registering instances, run under real Ray at both ends, and once with U1 reverted | **taken** 2026-10-11 |
| **U4** the shape | two prompts: 01 the change, 02 the release | **taken** 2026-10-11 |
| **U5** the release, and who adopts it | `v0.2.3`, patch-level; CPBH and SI adopt it (G3, G4); SGK may stay on `v0.2.2` (G2 "`v0.2.2` or later") | the version: **the user's ruling** 2026-10-11; the rest: **taken** 2026-10-11 (needed by 02) |

## 1. Prompts

| # | Prompt | Covers | Written? | Landed? | Commit | Log |
|---|---|---|---|---|---|---|
| 01 | [The base defaults three hooks](01-the-base-defaults-three-hooks.md) | the base (U1); `test_factory_instances.py` and `ABSTRACT_HOOKS` (U2); smoke step I at both ends (U3); contract §9.5 with its markers; verification §4.8 and §8.1; a note on extraction U32 | ✍️ yes, 2026-10-11 | ✅ 2026-10-11; reviewed | `f5d8957` | [log 01](logs/01-the-base-defaults-three-hooks.md) |
| 02 | [Release `v0.2.3`](02-release-v0.2.3.md) | the version, `README.md`, `PROVENANCE.md`, adoption addenda; the extraction board's G2–G4; the tag after green CI (U5) | ✍️ yes, 2026-10-11 | ⬜ | — | — |

**Planning note (2026-10-11, at `460b012`).** The brief's three points of §3 were re-measured, and
hold (README §0.1). A prototype, the three decorators removed and three scratch tests added, gave
`Ran 497 tests … OK` at both ends (Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39 in `venv/`;
3.13.16 / 2.55.1 / 2.0.46 in an offline scratch venv, 0 `ResourceWarning` lines); on the unchanged
tree the three scratch tests error with `TypeError` at instantiation. Through the pool an instance
meets the bare `NotImplementedError` a class meets. Nothing was committed, and Ray was not
started. The clients at planning: SGK `6861a9f` (clean), CPBH `52142d7` (25 untracked entries),
SI `7bb3efd` (clean).

**Orchestrator review of prompt 01 (2026-10-11).** Dispatched from `b8a00ad` to one Opus
subagent, with the note's seven corrections and its additions. Reviewed against its commit
`f5d8957`, with nothing landed after it. **Every check of the note's §3 passed**, and acceptance
1–4 are met. No stop condition fired. Nothing was pushed, and the tags are `v0.1.0`, `v0.2.0`,
`v0.2.1` and `v0.2.2` only.

*At dispatch.* The note's gate held at `b8a00ad`. The tree was clean, and the only worktree was
this checkout. The suite gave `Ran 494 tests … OK` in `venv/` (0 `ResourceWarning` lines). The port
check exited 0, and `black --check datastorekit docs` left 72 files unchanged. The clients were at
SGK `6861a9f`, CPBH `52142d7` (1 modified, 24 untracked) and SI `7bb3efd` (clean). `origin` had
`main` at `460b012` and the four tags. While writing the note, the orchestrator built a prototype
of §2.1–§2.4 in scratch exports. It gave 501 at both ends and failed under (a)–(e) as the prompt
says, with the differences of corrections 3–5. It found:
- an instance made at import would make (a) fail whole modules (correction 1), and the contract
  needs five markers, not four (correction 2);
- (a), (c) and (e) fail tests 6, 6 and 5 too (corrections 3–5); two insertion points
  (correction 6); and what a failed store prints (correction 7).

A local Ray instance started from SGK's venv, for another session's work, was up while the note
was written, so the orchestrator took no smoke run then (note §0). It had gone by the agent's start
(no Ray process at 20:21); the agent took all three runs, and the review took its own.

*The checks.*
1. **Scope.** `f5d8957` touches the prompt's §7 files only: under `datastorekit/`, four
   (`SQL/factory_base.py`, `tests/test_neutral_client.py`, and the new `tests/client/instances.py`
   and `tests/test_factory_instances.py`; §2.3's first route, so `standin_pool.py` is unchanged),
   and under `docs/extraction/` only `ray_smoke_run.py`. The diff over `pyproject.toml`,
   `README.md`, `PROVENANCE.md`, `docs/adoption/` and `.github/` is empty, and so is
   `docs/OPEN_ISSUES.md`'s. The ignored entries are dispatch's. CPBH and SI are as at dispatch.
   SGK's `HEAD` moved, by the other session's own commits, to `cd03ec4` (clean) at the review; the
   agent recorded `f3f0879`, `2d3429c` and `0972599` landing there during its work, and wrote
   nothing there.
2. **The base, by reading.** `register` and `build` keep `@staticmethod @abstractmethod`; the
   three follow the comment on defaulted hooks (`SQL/factory_base.py:16-19`, reworded for six),
   each `@staticmethod` with a docstring saying when the layer calls it, and naming no client. The
   review's own `ast` comparison against `6d8ee9a`: all eight hooks' arguments, bodies less
   docstrings, and returns equal; decorators as U1 says. `__abstractmethods__` is
   `{'register', 'build'}`.
3. **§2.3's module, by reading.** `scalar_entry` and `scalar_entry_factory` at module level; the
   factory defines `__init__`, `register` and `build` only, taking `self`, and no `inventory_spec`;
   no instance is made at import (correction 1), only in `instance_registry()`, which copies the
   neutral registry. `registry.py` and `factories.py` are unchanged. Of the new names, only the
   attribute and payload key `value` is a word of `client_vocabulary.json`, a plain word the guard
   does not forbid (the log's observation 1).
4. **The tests, by reading.** §2.4's six as nine tests (test 4 as four: direct from the class and
   from an instance, and through the pool with each), each store in a temporary directory, with a
   `tearDownModule` asserting Ray is not initialised. Test 4's pool half opens a fresh store per
   call and closes it in a `finally`. Test 6 imports `_defines` alone. `test_neutral_client` has
   the new lists and one new test, `test_the_hook_lists_are_the_bases`.
5. **Both ends.** In `venv/`, `Ran 504 tests … OK`, 0 `ResourceWarning` lines. In the review's own
   offline high-end venv (3.13.16 / 2.55.1 / 2.0.46) with `git archive f5d8957` installed
   editable, `Ran 504 tests … OK`, 0 lines. The port check exits 0 ("20 module(s) … 1 test(s)
   declared not ported"), the guards pass, and `black` leaves 74 files unchanged.
6. **The breakages.** The log's (a)–(e), extracted from it, pass `git apply --check`, apply, and
   pass `-R --check` against their own exports of `f5d8957`. At the high end, each fails as the log
   records:
   - (a), the whole suite: `Ran 504 … FAILED (failures=2, errors=6)`. Errors in tests 1, 2, 5, 6
     and test 4's two instance halves, each `TypeError: Can't instantiate abstract class
     gauge_setting_factory …` (6 lines); failures in test 3's `__abstractmethods__` sub-test and
     `test_the_hook_lists_are_the_bases`. Nothing else; the class halves of test 4 pass;
   - (b): `failures=3`, test 3's `__abstractmethods__` and `lacks_register` sub-tests, and the
     hook-list test;
   - (c): `failures=2, errors=2`, test 4's class halves for `store` (`TypeError … missing 1
     required positional argument: 'obj'`) and test 6 for the instance;
   - (d): `failures=4`, the `validate` case of each half of test 4;
   - (e): `failures=4`, tests 2 and 5.
7. **Ray.** No Ray process was up, and `RAY_ADDRESS` was unset. In the review's own offline venvs
   at both ends, with the commit's export installed editable, the smoke script (SHA-256
   `032036798e10…`, as verification §4.8 records) exits 0 with every step `PASS`; step I gets
   serials `{'scalar_left': 1, 'scalar_right': 1, 'gauge_setting': 1}`, inserted, and finds them
   again after a reopen, 0 of 4 names held after each `__exit__`; step C raises
   `builtins.ValueError` at 2.43.0 and `ray.exceptions.ActorAlreadyExistsError` at 2.55.1. Under
   (a), installed, at the high end: steps 1–6 `PASS`, step I `FAIL` with `builtins.TypeError:
   Can't instantiate abstract class gauge_setting_factory …`, exit 1. 0 Ray processes before and
   after each run.
8. **The documents.** Contract: the head line after §9.4's; §9.5 after §9.4, in §9's form, with
   three rows, every `path:line` it cites true at `f5d8957`; exactly five changed lines, each the
   old line plus `*(superseded in part by §9.5)*` (correction 2). Verification: §4.8 between §4.7
   and `## 5`, quoting both runs and the breakage run; §8.1 between §8's table and `## 9`; no line
   removed. Extraction: the italic note on U32 inside its bullet of README §6.2 (no line removed),
   and U32's board row the old row plus its note. All 12 relative links the commit adds resolve,
   anchors included.
9. **The records.** The log is in README §5.1's form, with the smoke output, the five diffs, the
   names checked and the clients at the start and the end. This board, the README and
   `prompts/INDEX.md` were in step; the index is unchanged at 4.
10. **Nothing left behind.** No Ray process. The tags are the four, and `origin` is unchanged.

*Residue fixed in this follow-up:* "this commit" → `f5d8957` on this board, in the log, the README
and `prompts/INDEX.md`; "reviewed" for 01 in this board's header and row, README's header and §2
row, the log's header and `prompts/INDEX.md`; the notes line. No issue is opened: the log's
observations (a plain word as a test name; a parameterised factory's objects dispatched by their
class's name, contract §6's existing fact; the suite not seeing an actor unpickle) need no work.

*The push (2026-10-11).* With the user's approval, `main` was pushed, moving `origin/main` from
`460b012` to `85f504d` (a fast-forward of four commits, `93446be`, `b8a00ad`, `f5d8957` and
`85f504d`, with no tag). CI passed there at both ends,
[run 38172753163](https://github.com/ds283/DatastoreKit/actions/runs/38172753163):
- low: Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39, `Ran 504 tests in 175.876s` / `OK`, and
  `black` leaving 74 files unchanged;
- high: 3.13.16 / 2.55.1 / 2.0.46, `Ran 504 tests in 165.611s` / `OK`, with 4 `ResourceWarning`
  lines (0 at the low end), which is timing (`actor-names` log 01, correction 8);
- SQLite 3.45.1 at both.

The smoke script is not collected by the suite, so CI started no Ray. 02 (`v0.2.3`) is written
next, against `f5d8957`'s tree.

**Legend.** ✍️ written · ⏸ held, with what it waits on · ⬜ not written / not landed ·
✅ landed.

**Orchestrator notes:** [`orchestrator/prompt-01.md`](orchestrator/prompt-01.md) (`b8a00ad`),
used for 01.

## 2. Gates outside this repository

None of this campaign's own. The extraction campaign's G2–G4 are recorded on its board (README §7).
When `v0.2.3` is tagged, its tag object and commit are given to the user for CPBH's prompt 07.

## 3. Active and unresolved issues

No issue is held on this board (2026-10-11).

## 4. Resolved issues

None yet.
