# Orchestrator — prompt 02, the neutral test client

Read [`../README.md`](../README.md) first: §0.2, §1, §2 (rows 02–04), §4, §5 and §6.2 (U8). Then
read [`prompt-01.md`](prompt-01.md) §0's last list, "Conventions", which this note keeps unless it
says otherwise, and the board's *Orchestrator review of prompt 01*.

**You do not write code.** You may:
- run the suite, the equivalence check and the tests the log names;
- replay the log's deliberate-breakage diffs with `git apply`, and revert them;
- run an in-process check or a probe from the session scratchpad, never committing one;
- read SGK through `git -C /Users/ds283/Documents/Code/SecondaryGWKit show 6f7f291:<path>`, and
  CPBH and SI through `git show` at the commits of §0;
- fix small residue in a follow-up commit of your own (§4).

**The prompt:** [`02-the-neutral-test-client.md`](../02-the-neutral-test-client.md)
**Closes:** `[01-ported-tests-use-sgk-table-names]` · **Narrows:** nothing · **Opens:** one issue
expected (§0, breakage (k)) · **Model:** Opus, as the prompt recommends.

**Gate:**
- 01 landed (`8bc60a5`) and its review is recorded (`d86a473`). 02 is written (`5d4f0b5`), and U8
  is taken.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- SGK's frozen files, and `Datastore/tests/standin_pool.py`, are unchanged from `6f7f291` to SGK
  `HEAD` (`b510bc9`, 2026-10-07). The prompt reads SGK at `6f7f291` regardless.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**It is the first prompt that designs anything.** 01 moved files. 02 writes down the contract a
client supplies, and builds the client that 03 and 04 port 304 tests onto. A client that declares
a key where the layer never reads it satisfies a coverage test and exercises nothing, and 03 finds
out only when its tests have no class to run on. So the review has three halves:
- **the contract is right**: every item the layer reads, with where it reads it and what it does
  when the item is wrong or absent, measured from the package and not copied from the prompt;
- **the client exercises it**: each item is declared on a class of the kind the layer reads it
  for, and a test reaches it;
- **01's guarantees still hold**: the 90 pass by name, the check still accounts for every line,
  and it now also fails on a file it does not account for.

**What moves on purpose:** new files under `datastorekit/tests/` (the client, the stand-in pool,
the new tests); 15 lines in three test files (U8); the check; `docs/client-contract.md`; the
records. No file under `datastorekit/` outside `tests/` changes.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-07 at `5d4f0b5` (package
files as at `8bc60a5`) and SGK `6f7f291`. Pass them on; each is STRUCTURALLY REQUIRED, and the log
says so.

1. **The replicated-integrity keys are read for replicated classes only.** The prompt (and README
   §2's row) puts `validated_column` and `revalidate` on the sharded parent `Sample`, and leaves
   the owned value table's kind open. But the layer reads `owner_column`, `monotone_flags` and
   `validated_column` only in `_replicated_specs` (`SQL/ShardedPool.py:1334-1362`), which covers
   the replicated tables and their tag tables. It calls `revalidate` only from
   `_recompute_validated` (`:1966`, `:1992`), after an interrupted *replicated* validate. It calls
   `owned_serials` only in the replicated store's check (`:3377`, `:3386`). The comment at
   `:1125-1126` says that nothing in a sharded table is read, repaired or refused on. On a
   sharded class, `build_schema` accepts these declarations (`SQL/schema.py:170-178`), and nothing
   else reads them. SGK declares them where the layer reads them:
   - `monotone_flags` on the replicated `redshift` and `wavenumber`;
   - `validated_column`, `revalidate` and `owned_serials` on the replicated `BackgroundModel`;
   - `owner_column` on the replicated `BackgroundModelValue`.

   **So:** `validated_column` with `revalidate`, and `owned_serials`, go on a **replicated** owner
   class. `owner_column` goes on its **replicated** value table, and `monotone_flags` on a
   replicated leaf, as the prompt already says. `Sample` keeps `validate_on_startup`. That hook
   *is* read for sharded classes, and the prune at open applies only to them
   (`SQL/Datastore.py:458-460`). `Sample` may declare a validated column of its own as well. The
   contract document says, for each of these five items, that it is read only for replicated
   classes. 03's `test_reconcile_at_open` (41 tests) needs exactly these roles.
2. **`build_schema` takes two arguments**: `build_schema(metadata, factories)`
   (`SQL/schema.py:62`). §2.7's `build_schema(registry.factories)` means
   `build_schema(sqla.MetaData(), registry.factories)`.
3. **§2.4 has three files, not four.** `tests/shard_store_fixtures.py`,
   `tests/test_shard_key_audit_copy.py` and `tests/test_shard_key_audit_refusals.py`.
   `tools/shard_key_audit.py` is not re-fixtured: breakage (f) relies on D-fix not covering it.
   Read "the four files of §2.4" as these three wherever it appears (§2.6 D-fix, §3.2, §6).
4. **Breakage (m) must fail a test that exists in the agent's commit.** `_StandinRandom.randrange`
   matters only to a test that pins a controller (`controller` or `pin_controller`). None of 01's
   90 does, and §2.7's tests need not. Either a new test pins one, or the agent picks a breakage
   that the round trip reaches. Either way, the log names the test it fails.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **(n), informational: replay 01's `key_id` diff** (log 01 §4.4; `SQL/ShardedPool.py:3561`) on
  the agent's tree, and record which tests fail, if any. Reading the shard-key class through
  `object_get` reaches `_assign_shard_keys` (`:687`, `:3246`), so `build_store` will call it. The
  question is whether any test then compares the saved shard map with the one in memory. If any
  test fails, add a dated "Measured by 02" line to `[01-no-ported-test-pins-the-shard-key-
  assignment]` on the board, and correct its index hook. Otherwise record the result in the log
  only. 03 still owns the issue. A test written to pin it is 03's, not 02's.
- **(k) is expected to fail nothing.** `revalidate` is called only when the check at open finds an
  interrupted validate (correction 1), and neither the round trip nor a coverage test makes one.
  If nothing fails, **open a §3 issue** for 03, `[02-no-test-reaches-revalidate]` or similar,
  with the diff and the one call site. Do not record it only under observations: 01's review
  had to open the `key_id` issue for exactly that reason.

**The facts, checked by the orchestrator.** Pass them on.

- **The planner's survey holds** at `8bc60a5`:
  - `ShardedPool.__init__` at `SQL/ShardedPool.py:95-114`, 16 parameters, split 6 / 8 / 2 as
    §2.1 says; `ShardKeyType.__name__` at `:157`; the getter first used at `:3262`.
  - Nine `register()` keys, read at `SQL/schema.py:95-180`.
  - Hooks: the five abstract (`SQL/factory_base.py:7-29`), three defaulted (`:34-62`);
    `read_batch` at `SQL/Datastore.py:580`; `read_table` at `:828-870`, with `tables_arg` at
    `:864`.
  - `Parent` at `store_inventory.py:209` has **six** fields: `column`, `of`, `type_column`,
    `types`, `nullable`, `cross_shard`. `ParentSet` at `:271` has **three**: `table`, `owner`,
    `members`. `InventorySpec` at `:297` has six.
- **`cross_shard` is a field of `Parent`**, not of `ParentSet`. A `ParentSet` member is a `Parent`
  and may be `cross_shard`, but may not be polymorphic (`:287-293`, a `ValueError`). A polymorphic
  parent's `type_column` must also be one of its class's `leaves` (`inventory_classes`, `:955`).
  Every class a spec depends on, including `store_tag` for a tagged class, must declare an
  `inventory_spec` (`:950`). SGK puts `cross_shard` on sharded classes' parents (`QuadSource`,
  `QuadSourceIntegral`).
- **`stepping`.** The layer accepts `True`, `"minimum"` or `"exact"` (`SQL/schema.py:144-160`),
  adds the column and records `stepping_mode`. Nothing else in the package reads `stepping_mode`:
  the modes mean something only to a factory. An unknown string **prints a warning and is
  ignored** (`:146-150`). That is the "when wrong" behaviour, and the contract says so. SGK uses
  only `"exact"`.
- **`dependent_tables(dropped, factories)`** (`SQL/schema.py:327`). "Accepts each group as the
  client declares it" means that it returns `[]` for each group, so that each group is closed
  under dependence. It raises `ValueError` for a name the registry does not declare. A
  `cross_shard` parent or a `ParentSet` member into another class's group breaks that closure.
  Design the groups with that in mind. SGK's groups hold one replicated table
  (`"gk-source-policy-records": ["GkSourcePolicy"]`), and the inherited issue
  `[00-a-drop-action-drops-a-replicated-table-outside-the-in-flight-record]` concerns dropping
  one. Whether the neutral client's groups hold a replicated table is the agent's choice, made
  from what 04's `test_drop_refuses_dangling_references` needs; the log says which.
- **The stand-in pool at `6f7f291`** is 581 lines. The banner is at `:421-423`, after two blank
  lines (`:419-420`). After the cut, `black` removes the trailing blank lines: count them as D-split
  or D-fmt, and say which. The two `from config.… import` blocks are at `:287-293` and `:317-323`.
  `shard_key_wavenumber_store_id` is used at `:302` and `:335`. The module paths at `:43-45` are
  whole literals, so D-str maps them. D-imp maps only through `MODULE_MAP`, and refuses
  `config.*`, so D-split must act on those imports before D-imp does. The pool pickles every
  argument and result (`_copy`, `:55`, used at `:131`). So **the client's objects and factories
  are defined at module level** in `datastorekit/tests/client/`, never inside a test.
- **§2.4's lines** are as the prompt says (15 lines: 3 + 3 + 9), every occurrence is a plain
  `STRING` token, and none is an f-string. 01's D-str skips f-strings; D-fix may do the same, and
  the log says so. `tools/shard_key_audit.py:188` is a `COMMENT`. Breakage (l)'s message is the
  f-string at `tools/shard_key_audit.py:220`, `f">> '{key_type}' table (shard #{shard_serial})
  row count: "`.
- **Nothing in 01's tests scans `datastorekit/tests/client/` for anything but imports.** The
  naming rule (`test_shard_file_name.py:87-101`) skips `tests/`. The import guard
  (`test_package_imports.py:27`) allows the standard library, `ray`, `sqlalchemy` and
  `datastorekit`.
- **The clients' registries**, to be read with `git show` at these commits (2026-10-07):
  - SGK `6f7f291`: `config/datastore.py` (`factories` at `:91`, `drop_groups` at `:133`,
    `serial_batch_sizes` at `:152`, `tables_to_drop` after it) and `config/sharding.py`;
  - CPBH `52142d7`: `Datastore/SQL/Datastore.py` and `config/sharding.py`;
  - SI `96d0562`: `Datastore/SQL/Datastore.py` and `config/sharding.py`.
- **The toolchain.** `venv/` exists from 01: Python 3.12.15, `ray==2.43.0`,
  `sqlalchemy==2.0.39`, `black==25.1.0`, the package installed editable. It needs no change.
- **Expected counts.** The suite is **90** before (`Ran 90 tests … OK`, re-run by the orchestrator
  at `5d4f0b5`), and 90 + the new tests after. `compare_with_source.py` exits 0 over 30 files
  before. The index is **7** now: 6 after the closure, and 7 if (k)'s issue is opened, as
  expected.
- **Ray.** No Ray process was up at writing (`pgrep -lf 'gcs_server|raylet|ray::'` empty).

**What the review exists to establish.**
- **(E1) The contract.** `docs/client-contract.md` covers every item the package reads. Each has
  its kind (required, optional, defaulted), its line, and its behaviour when wrong or absent. The
  five replicated-only items say so. It names no client.
- **(E2) The client exercises it.** Each contract item maps to a class of the right kind and to a
  test that reaches it. The registry exports exactly the nine names. `build_store` writes every
  class.
- **(E3) The stand-in pool** is SGK's generic half, changed only by D-imp, D-str and D-split.
- **(E4) U8.** The 15 lines change only inside string literals, as whole identifiers. The 90 pass
  with their names. Nothing outside the three test files changes.
- **(E5) The check.** It exits 0. D-fix and D-split are transformations, restricted to their
  files. An unaccounted file makes it exit 1. (a)–(i) each bite.
- **(E6) The tests bite.** (j), (l) and (m) fail as recorded. (k) and (n) are recorded, and (k)'s
  issue is opened if nothing failed.
- **(E7) The records.** The log, with the prompt's §4.4 additions. The board's §3 and §4,
  `docs/OPEN_ISSUES.md` and `prompts/INDEX.md`.

**Conventions.** Prompt 01's note's, unchanged, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff with `git apply --check` and `-R --check`, and replay it in `bash`;
- read SGK, CPBH and SI only through `git show`;
- use a subdirectory of the session scratchpad, never `/tmp`, and put **no scratch `.py` under
  `datastorekit/`**, since breakage (h) and the import guard scan it;
- start no Ray;
- a stop goes to the user;
- check `git log` before committing.

One addition: **the contract document is measured, not transcribed.** Each line number in it is
read from the package at the agent's tree. Where the agent's count differs from §2.1's survey or
from this note, the log says which, and why.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone.
2. **The baseline.** The suite gives `Ran 90 tests … OK`, and `compare_with_source.py` exits 0.
3. **SGK.** Re-run 01's freeze `git diff --stat`, adding `Datastore/tests/standin_pool.py`. It
   must be empty.
4. **Ray.** Record `pgrep -lf 'gcs_server|raylet|ray::'`.
5. **The index.** 7 now; 6 after the closure; 7 with (k)'s issue. Tell the agent all three.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, the board, `docs/OPEN_ISSUES.md`, `CLAUDE.md` and log 01;
- `HEAD`, the counts and the index counts;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's four corrections and two additions. Correction 1 is
the one that matters: the replicated-integrity roles go on replicated classes.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/02-the-neutral-test-client.md`, in README §5.1's
  form, with the prompt's §4.4 additions.
- **The files it may add or change are the prompt's §6 list, and nothing else**, plus the board
  entry (n) may touch and (k)'s issue. It must not touch any file under `datastorekit/` outside
  `tests/`, nor `PROVENANCE.md`, `pyproject.toml`, `README.md`, `CLAUDE.md`, the campaign README,
  or anything under `orchestrator/`.
- **It edits no client repository, and runs no client code.** It reads them through `git show`.
- **It runs no build, and starts no Ray.**
- **Stop and ask** on any of the prompt's §5 conditions.

## 3. The review — ten checks

1. **Scope.** `git show --stat <commit>` touches only the prompt's §6 list and the records. No
   file under `datastorekit/` outside `tests/`, no `venv/`, `*.egg-info`, `__pycache__` or scratch
   file.
2. **E1, the contract, by measuring.** Re-derive the items independently: every keyword argument
   of `ShardedPool.__init__`; every `registration_data.get` key; every `factory.<hook>` call and
   `getattr(factory, …)`; every field of the three declarations; the names in `contract.py`; every
   public function taking `factories`. Each is in the document, with a line that holds at the
   commit. Spot-check five "when wrong" lines by reading them. `grep -nw` for the three clients'
   registry names finds none in the document.
3. **E2, the roles.** Read `datastorekit/tests/client/` in full. Each of the five replicated-only
   items is on a class in `replicated_tables`. `Sample` is in `sharded_tables` on `"k"`. Then check
   the following, each on the class the log names:
   - the shard-key proxy, and the polymorphic `Parent`;
   - a `ParentSet`, and a `cross_shard` parent;
   - each `stepping` form, `serial: False`, `timestamp: True` and a `None` registration;
   - `read_table` with `tables_arg` both ways, and `read_batch`.

   `registry.py` exports exactly the nine names (`dir()` against `__all__`, or by reading). No name
   is a table of any client's registry (the log's measured list).
4. **E2, by running.** `build_store` into a scratch `tempfile` directory, under the stand-in pool,
   then `read_inventory`: every registered class with a table has rows, and `ray.is_initialized()`
   is false throughout.
5. **E3, the stand-in pool.** Diff it against SGK's `:1-420`, after the D-imp and D-str rewrites.
   The only other hunks are D-split's two imports and its two renames.
6. **E4, U8.** `git show <commit> -- <the three files>` changes exactly the 15 lines, each only
   inside a string literal. The per-module `Class.test_name` sets equal 01's.
   `./venv/bin/python -m unittest discover -s datastorekit/tests -t .` gives `Ran N tests … OK`,
   and N equals the log's.
7. **E5, the check, by reading and running.** It exits 0, with counts per class equal to the
   log's. 01's files' counts are unchanged, except for D-fix in the three files. Read D-fix and
   D-split: each is a transformation of the source, restricted to its files. An unaccounted
   `.py` makes `main` return 1, and `__pycache__` is skipped. Replay (a)–(i), one at a time, in
   `bash`. Then one of the orchestrator's own: in `standin_pool.py`, rename
   `shard_key_store_id` in a third place (or in a line outside the two methods); it must fail.
   `git status` is clean after each.
8. **E6, the tests bite.** Replay (j), (l) and (m), and check the failures are the log's. Replay
   (k) and (n), and check the log's account. If (k) failed nothing, its issue is open.
9. **Isolation.** From the scratchpad, with `env -u PYTHONPATH`, run §3.3's two imports, and check
   that `ray.is_initialized()` is false afterwards. The import guard passes over the new files.
10. **E7, the records.**
    - The log has every section of README §5.1 and each of the prompt's §4.4 additions: the
      contract's counts against the survey; the three registries' names; the role table for 03
      and 04, with an entry for each imported name of the 18 modules; the 15 re-fixtured lines;
      the check's whole output; the counts 90 → N, with the new tests named; and the entry points
      with their signatures.
    - Board: 02's row; `[01-ported-tests-use-sgk-table-names]` in §4 with its "Closed" line; the
      prose issue at 102 lines, with `tools/shard_key_audit.py` at 4; (k)'s issue, if opened.
    - Index: count it, and check that the header matches. `prompts/INDEX.md`: the campaign's line.
    - `black --check` (25.1.0) is clean on `datastorekit/` and `docs/extraction/`.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 02* paragraph, in the form of
  01's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log and in `prompts/INDEX.md`;
  - README §2's status for 02;
  - the notes line, with this note marked "used for 02".
- Anything the review finds that is not residue is opened on the board's §3 and in the index.
- **Correction 1 changes README §2's row for 02** ("a sharded parent with … a `validated_column`
  and `revalidate`"). Amend the row in the follow-up so that 03's author reads the roles as built,
  and say so in the review paragraph.
- **Report to the user:**
  - what landed, and the count N;
  - the contract's size: items by kind, and any differences from the survey;
  - the client's classes, and where the replicated-only roles sit;
  - the check's two new classes, and the unaccounted-file failure biting;
  - (k) and (n): what they showed, and the issue opened;
  - that 03 and 04 can now be written, against the tree 02 left.
