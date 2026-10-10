# The extraction campaign: verification

**Campaign:** [`prompts/extraction/README.md`](../prompts/extraction/README.md) ·
**Board:** [`prompts/extraction/IMPLEMENTATION_STATE.md`](../prompts/extraction/IMPLEMENTATION_STATE.md) ·
**Written by:** [extraction prompt 11](../prompts/extraction/11-verification-and-close-out.md),
log [`11-verification-and-close-out.md`](../prompts/extraction/logs/11-verification-and-close-out.md) ·
**Date:** 2026-10-10 · **Verifies:** the package as tagged **`v0.2.1`**, commit `33778b0` (tag object
`0ba2e4d`), and the records of prompts 01–10.

*This document is additive from the day it is committed (`CLAUDE.md` rule 6): a later measurement is
added as a new dated subsection, and what is here is not rewritten.*

Every fact below carries a commit, a `path:line` at a named tree, or a command and its output. A
statement of a log is cited by log and section ("log 05 §5.3" is
`prompts/extraction/logs/05-supported-versions-and-ci.md` §5.3). Where this document and a log
disagree, it says which is right and why; it does not rewrite the log. `<scratch>` stands for the
scratch directory of prompt 11's run (`<session scratchpad>/agent11/work`), outside the repository.

---

## 1. What this document is

**What the campaign set out to do** (README §0, §1, §6.1). Three client projects, SecondaryGWKit
(SGK), ChamPBH (CPBH) and StochasticInstantons (SI), each carried its own copy of one
`Datastore` / `ShardedPool` layer, and the copies had let a serious fix fall through (README §0,
the shard-key fix). The user decided on 2026-10-07:
- **D1:** extract the layer as a separate, reusable component;
- **D2:** `Datastore` / `ShardedPool` first, with `RayWorkPool` a separate unit of work;
- **D3:** a public repository, `ds283/DatastoreKit`;
- **D4:** CPBH's stores are rebuilt on adoption, not migrated.

The campaign was to build the package from SGK's layer, moved and not rewritten (README §0.1), give
it a suite that needs no client, add CPBH's version-keyed lookups, and hand each client an adoption
checklist. U33 (2026-10-09) added the fixes of the four issues the board then held open, and a fix
release.

**What it delivered.**
- The package `datastorekit`: SGK's 15 layer files and two tools at SGK `6f7f291`, under README
  §4's names (`PROVENANCE.md`), with two internalised definitions.
- A suite of **486** tests on a neutral test client and an in-process stand-in pool, none needing a
  Ray cluster or a client (§3).
- `docs/client-contract.md`, the facts a client supplies; `docs/adoption/`, a checklist per client.
- Three releases, each tagged on its prompt's commit after CI passed there at both ends (§2.3):
  `v0.1.0` (SGK's behaviour), `v0.2.0` (`key_on_version`), `v0.2.1` (three fixes and the prose).

**The headline, at `v0.2.1`.**
- **The suite** gives `Ran 486 tests … OK` in `venv/` (Python 3.12.15 / Ray 2.43.0 / SQLAlchemy
  2.0.39, 0 `ResourceWarning` lines) and at the high end (3.13.16 / 2.55.1 / 2.0.46, 4 lines),
  before and after this prompt's work (§3.1).
- **Under real Ray** (U41), for the first time: `docs/extraction/ray_smoke_run.py` writes every
  class of the neutral client, reopens, opens read-only, makes a keyed vectorized get and a refused
  open, and exits 0 at both ends, leaving no Ray process (§4).
- **The pin** (U42) `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.1`, installed
  from GitHub as a client installs it, is `33778b0`, and its 20 package files are prompt 10's
  wheel's, hash for hash (§5).
- **One issue is opened**, `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]`,
  found by the smoke run's probe and inherited from SGK (§6.2). Eight issues were opened and
  resolved on the board (§6.1). The four issues inherited from SGK stay open and out of scope
  (§6.3).
- **What remains** (§9): gates G2–G4 (each client's adoption, in its own campaign); the new issue,
  assigned to no campaign; a multi-node Ray cluster and each client's own suites, unverified; and
  two documented gaps, the commit-point labels and the contract's line numbers.

---

## 2. Reconciliation

### 2.1 The prompts

Each prompt landed as one commit, was reviewed in a commit of its own, and was dispatched from an
orchestration note (the board's notes line, §1). Counts are each log's "after", re-read from its
header; the closed and opened issues are the board's §3 and §4. 07b was withdrawn unwritten (U33).

| Prompt | Commit | Note | Review | Suite after | Closed | Opened |
|---|---|---|---|---|---|---|
| 01 | `8bc60a5` | `bd9f461` | `d86a473` | 90 | — | `[01-package-prose-names-sgks-layout]`, `[01-ported-tests-use-sgk-table-names]`; the review, `[01-no-ported-test-pins-the-shard-key-assignment]` |
| 02 | `e988e69` | `737ad6e` | `03fa97a` | 109 | `[01-ported-tests-use-sgk-table-names]` | `[02-no-test-reaches-revalidate]`, `[02-an-unsupplied-sharded-table-raises-keyerror]` |
| 03a | `11247c7` | `f7f053d` | `e35ade2` | 188 | `[02-no-test-reaches-revalidate]`, `[01-no-ported-test-pins-the-shard-key-assignment]` | — |
| 03b | `0d5380c` | `72cf34a` | `2992945` | 268 | — | — |
| 04a | `7ceed25` | `ae94aaa`, addenda `66535b2`, `74c6343` | `1a54af1` | 353 | — | the review, `[04a-no-test-pins-a-second-parent-set-member]` |
| 04b | `0c66505` | `f79f254`, addendum `7ee9b6e` | `18c102c` | 444 | `[04a-no-test-pins-a-second-parent-set-member]` | — |
| 05 | `68db557` | `f69921b` | `487ec4c` | 444 | — | `[05-a-refused-open-leaves-its-engines-undisposed]` |
| 06 | `240028e` | `0e524b4` | `ad785f1` | 458 | — | `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]` |
| 07a | `dd45243` | `a816632` | `88cac61` | 458 | — | — |
| ~~07b~~ | — | — | — | — | *withdrawn 2026-10-09 (U33, U35)* | — |
| 08a | `f938844` | `484ad41` | `2123445` | 469 | `[02-an-unsupplied-sharded-table-raises-keyerror]`, `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]` | — |
| 08b | `efedc8d` | `f24ded1` | `452b3c9` | 480 | `[05-a-refused-open-leaves-its-engines-undisposed]` | — |
| 09 | `cad7bc1` | `b5b1586` | `ffe843c` | 486 | `[01-package-prose-names-sgks-layout]` | — |
| 10 | `33778b0` | `208d702` | `92ad43d` | 486 | — | — |
| 11 | the commit that adds this document | `ec059c8` | — | 486 | the campaign (U30, U33) | `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]` |

The suite started at 0: 01 ported 88 tests and added 2 (the import guard), so 90 (log 01 §4.2).

### 2.2 Every other commit

`git log --reverse --format='%h %s' 8bc60a5^..ec059c8` lists **59** commits, the commit before 11's
being `ec059c8`. Thirteen are the prompts of §2.1. The other 46, by class:

| Class | Count | Commits |
|---|---|---|
| prompt written | 13 | `5d4f0b5` (02, U8), `0d02ea6` (03a, U9–U12), `19adaa2` (03b, U13), `86640bf` (04a, U14–U17), `a80af57` (04b), `2255206` (05, U6, U23, U24), `1f9941f` (06, U25–U28), `2f7ed03` (07a, U29–U32), `8a1cae9` (08a, U33–U37), `9f9c970` (08b), `21334c2` (09, U38–U40), `29bf379` (10), `7209e5c` (11, U41, U42) |
| note | 13 | `737ad6e`, `f7f053d`, `72cf34a`, `ae94aaa` (with U18), `f79f254`, `f69921b`, `0e524b4`, `a816632`, `484ad41`, `f24ded1`, `b5b1586`, `208d702`, `ec059c8` |
| review | 13 | `d86a473`, `03fa97a`, `e35ade2`, `2992945`, `1a54af1`, `18c102c`, `487ec4c`, `ad785f1`, `88cac61`, `2123445`, `452b3c9`, `ffe843c`, `92ad43d` |
| records (a tag recorded) | 3 | `fe040b2` (`v0.1.0`), `102f225` (`v0.2.0`), `41c77c1` (`v0.2.1`) |
| decision | 4 | `66535b2` (U19, 04a's first stop, with a note addendum), `74c6343` (U20, U21, 04a's second stop, with a second addendum), `7ee9b6e` (U22, 04b's stop, with an addendum), `98fb497` (the user's decision on the commit-point labels) |

13 + 13 + 13 + 13 + 3 + 4 = 59. Before `8bc60a5` are six: the repository's start (`be6a4bf`), the
plan (`b5aee75`, `54e9d64`), 01's prompt (`c31b20c`), the SGK freeze recorded (`47d3ab1`) and 01's
note (`bd9f461`) (`git log --reverse --format='%h %s' 8bc60a5`).

### 2.3 Tags and CI

Each tag is annotated, made on its prompt's commit after the workflow passed there at both ends,
and pushed (board, the review of 05, 06 and 10). `git for-each-ref refs/tags --format='%(refname:short)
%(objectname:short) %(*objectname:short)'` gives:

| Tag | Tag object | Commit | CI run | Suite in CI |
|---|---|---|---|---|
| `v0.1.0` | `0ece4aa` | `68db557` (05) | [run 37922626418](https://github.com/ds283/DatastoreKit/actions/runs/37922626418) | 444 |
| `v0.2.0` | `9eaf542` | `240028e` (06) | [run 37934881027](https://github.com/ds283/DatastoreKit/actions/runs/37934881027) | 458 |
| `v0.2.1` | `0ba2e4d` | `33778b0` (10) | [run 38054748108](https://github.com/ds283/DatastoreKit/actions/runs/38054748108) | 486 |

CI ran Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39 and 3.13.16 / 2.55.1 / 2.0.46, with Ubuntu
24.04's SQLite 3.45.1, at each tag (board). At 11's dispatch `origin/main` was `41c77c1`. This
prompt pushes nothing and makes no tag.

### 2.4 The environment

Every measurement of §3–§5 was made on 2026-10-10, 18:07–18:37 BST and again at the end (log 11
§4), on one machine: macOS 27.0.1 (build 26A434), arm64, `git` 2.56.0, `uv` 0.12.20. Every venv
but `venv/` was made by `uv venv --offline`, with its packages installed `--offline` from `uv`'s
cache, except the one install of §5.

| Venv | Python | Ray | SQLAlchemy | SQLite | `datastorekit` | Used for |
|---|---|---|---|---|---|---|
| `venv/` (the repository's) | 3.12.15 | 2.43.0 | 2.0.39 | 3.53.4 | 0.2.1, editable from the checkout | the suite (low end), the two checks, `black` 25.1.0 |
| `<scratch>/base-hi/venv` | 3.13.16 | 2.55.1 | 2.0.46 | 3.53.4 | 0.2.1, editable from `git archive` of the tree | the suite at the high end |
| `<scratch>/smoke-lo/venv` | 3.12.15 | 2.43.0 | 2.0.39 | 3.53.4 | 0.2.1, editable from an export of the working tree | §4, low end |
| `<scratch>/smoke-hi/venv` | 3.13.16 | 2.55.1 | 2.0.46 | 3.53.4 | as above | §4, high end |
| `<scratch>/break-a/venv`, `break-b/venv` | 3.13.16 | 2.55.1 | 2.0.46 | 3.53.4 | as above, with a breakage applied | §4.4 |
| `<scratch>/pin/venv` (deleted after) | 3.13.16 | 2.55.1 | 2.0.46 | — | 0.2.1 from GitHub, not editable | §5 |
| `<scratch>/pin/venv-c` (deleted after) | 3.13.16 | 2.55.1 | 2.0.46 | — | 0.2.0 from this repository's `v0.2.0` | §5.4 |

The low-end interpreters are `/opt/local/bin/python3.12`, the high-end `/opt/local/bin/python3.13`.
An export of the working tree is `git ls-files -z -co --exclude-standard | tar --null -T - -cf - |
tar -xf - -C <dir>` (log 05 §2 item 1), which carries the uncommitted smoke script.

---

## 3. Each prompt's acceptance, at `v0.2.1`

The acceptance is README §2's and the prompt's own; the review is the board's §1 paragraph for it,
every one of which found "every check of the note's §3 passed". The last column says what holds at
`v0.2.1` and how it was re-measured here, or why it was not.

| Prompt | Acceptance, in brief | What its review found | At `v0.2.1` |
|---|---|---|---|
| 01 | `import datastorekit` in a fresh venv with no client; `compare_with_source.py` finds no difference but the map and the two internalisations; the 88 tests pass | the check exits 0 over 30 files and bites ((a)–(e)); the `key_id` binding fails no test, so the review opened `[01-no-ported-test-pins-the-shard-key-assignment]` | **Re-measured.** The pin imports in a fresh venv with no client on the path (§5.3). `compare_with_source.py` at `v0.1.0` exits 0 (§3.1); it is retired after `v0.1.0` (U27), so it describes that tree. The 88 are among the 486 at both ends. |
| 02 | the contract, and every item of it exercised by the neutral client | the contract re-derived and complete; `[02-an-unsupplied-sharded-table-raises-keyerror]` confirmed at `SQL/ShardedPool.py:1015` (`e988e69`'s tree) | **Re-measured** in the suite (`test_neutral_client`'s coverage tests), and under real Ray: the smoke run opens the neutral client's three-shard store and writes every class (§4). The contract's §1–§9 were not re-measured (U37's reasoning: nothing a client supplies changed); its lines are its sections' trees' (§9.2). |
| 03a | the port check passes; the two issues close, each by a test a named breakage fails | names, skeletons and control flow equal SGK's; (i) and (j) fail the tests that close the issues | **Re-measured:** the port check exits 0 (§3.1); `test_shard_key_assignment` and `test_validate_of_a_background_model` pass in the 486. The breakages were not re-run (their tests are unchanged in code since; 09 changed prose only). |
| 03b | 53 defined, 80 run, checked the same way | as 03a; three of the log's eleven diffs regenerated (trailing blank context) | **Re-measured** by the port check and the suite. |
| 04a | the port check over 15 modules; the suite 353 | the fixture, witness and client by reading and running; opened `[04a-no-test-pins-a-second-parent-set-member]` | **Re-measured** by the port check and the suite. |
| 04b | the port check over 20 with one test not ported; the guard pins exactly one hit; 444 | the vocabulary file reproduced byte for byte; the guard's retargeted tests bite | **Re-measured:** the port check gives "20 module(s) … 1 test(s) declared not ported". The guard now pins no hit: 09 emptied `KNOWN_HITS` (U17), and its 8 tests pass (§3.1). |
| 05 | U6's range; both ends; CI; the README; `v0.1.0` | wheel of 25 entries, none under `tests/`; CI green (run 37922626418) | **Re-measured:** both ends locally (§3.1). `git diff 68db557 33778b0 -- pyproject.toml .github` changes only the version line, so the range and the workflow are 05's. CI was not re-run here; at `v0.2.1` it is run 38054748108. |
| 06 | `key_on_version`, the lookup serial, `set_lookup_version`; 458; `v0.2.0` | the witness recaptured byte for byte; ten breakages as logged | **Re-measured** in the suite, and under real Ray: the keyed vectorized get finds serials `[1, 2]` read-write and read-only; with the read-only pool's `set_lookup_version` call removed, the read-only get is refused by the actor (§4.4 (b)). |
| 07a | the checklists, measured read-only at named client commits against `v0.2.0` | the script's 322 import hits equal the orchestrator's probe; every citation resolves | **Not re-measured.** U37 decided that 10's addenda give `v0.2.1` and the clients are not re-measured; this prompt reads no client but SGK, at two commits, through `git`. |
| 08a | the two fixes, each with a test the unfixed code fails | the two hunks only; (a)–(e) fail as logged | **Re-measured** in the suite, and under real Ray: the caller's dicts are unchanged by the vectorized get (step 2), and the refusal with `Weave` left out is the `RuntimeError`, `Weave` printed as not supplied (step 5). With 08a's copy reverted, steps 2, 3, 4 and 6 fail naming the key `'k'` (§4.4 (a)). |
| 08b | a refused open disposes what it made, with a test that counts connections | 2 connections never closed over the 480, both a ported test's | **Re-measured:** the high end prints 4 `ResourceWarning` lines (§3.1), 08b's figure. Under real Ray the refused opens of step N and step 5 left no name held once dropped (§4). |
| 09 | the prose rewritten; `KNOWN_HITS` empty; `test_prose_names_no_source` | only prose changed, by an AST check; tier A gone | **Re-measured:** the two guards give `Ran 14 tests … OK` alone in `venv/`, and pass in the 486 at both ends (§3.1). |
| 10 | `0.2.1`, `README.md`, `PROVENANCE.md`, the addenda; the tag after CI | the wheel's `RECORD` `f840ffa4…6c5e`; the addenda by reading | **Re-measured:** the wheel built offline from `git archive 33778b0` has that `RECORD`, and the pin from GitHub has its 20 package lines (§5). |

### 3.1 What was re-measured here

| Check | Command (from the repository root unless said) | Result |
|---|---|---|
| The suite, low end | `./venv/bin/python -m unittest discover -s datastorekit/tests -t .` | `Ran 486 tests in 413.705s` / `OK`, 0 `ResourceWarning` lines, before; `Ran 486 tests in 1004.790s` / `OK`, 0, at the end (log 11 §4.1) |
| The suite, high end | the same, from `<scratch>/base-hi/tree` (`git archive HEAD`) with its venv | `Ran 486 tests in 419.532s` / `OK`, 4 `ResourceWarning` lines; at the end, from an export of the final working tree, `Ran 486 tests in 1038.874s` / `OK`, 4 |
| The port check | `./venv/bin/python docs/extraction/compare_ported_tests.py` | exit 0: "OK: 20 module(s) keep their source's tests, classes and assertion skeletons; 1 test(s) declared not ported" |
| The layer guard and the prose guard | `./venv/bin/python -m unittest datastorekit.tests.test_layer_is_generic datastorekit.tests.test_prose_names_no_source` | `Ran 14 tests in 0.672s` / `OK` (8 and 6) |
| `black` | `./venv/bin/black --check datastorekit docs` (25.1.0) | 70 files unchanged before; 71 after, with the smoke script |
| The equivalence check at `v0.1.0` | from `git archive v0.1.0` in `<scratch>/v010`: `<repo>/venv/bin/python docs/extraction/compare_with_source.py` | exit 0: "files compared: 31", "files ported, checked by compare_ported_tests.py: 20", "files with no source, declared: 10", "OK: every differing line is classified, and every file is accounted for" |
| The package | `git diff 41c77c1 -- datastorekit pyproject.toml` | empty |

The equivalence check reads SGK through `git -C <SGK> show 6f7f291:<path>` and `git log -1` only.
The suite was run with no Ray process up anywhere.

---

## 4. The package under Ray (U41)

### 4.1 The script and the runs

`docs/extraction/ray_smoke_run.py` is a script, not a test; the suite never collects it. It starts
a local Ray instance with `ray.init(address="local", num_cpus=4, include_dashboard=False,
log_to_driver=False)` and stops it in a `finally`. `address="local"` always starts a new instance
and never connects to one. It refuses to run when `RAY_ADDRESS` is set, when Ray is initialised,
or when `pgrep -f` finds a Ray process whose executable is not a shell. Its store is in a
`tempfile.TemporaryDirectory()`. It builds the pool as `standin_pool.StandinCluster.open_pool`
does, with the registry's `read_table_config` and `serial_batch_sizes` and three shards, and
patches the neutral client's `build.resolve` to `ray.get` in its own process. Its docstring gives
the steps.

Each end ran from a fresh offline venv with a fresh export of the working tree installed editable,
with `PYTHONPATH` unset, from the export's root:

```bash
cd <scratch>/smoke-<end>/tree
env -u PYTHONPATH <scratch>/smoke-<end>/venv/bin/python docs/extraction/ray_smoke_run.py
```

The script run is the committed one (SHA-256 `83c1b37d…45e0`). Its first drafts, and what they
showed, are in log 11 §2.

| | Low end | High end |
|---|---|---|
| Python / Ray / SQLAlchemy / SQLite | 3.12.15 / 2.43.0 / 2.0.39 / 3.53.4 | 3.13.16 / 2.55.1 / 2.0.46 / 3.53.4 |
| Started (BST) | 18:30:18 | 18:31:08 |
| `ray.init` | 13.2 s | 15.8 s |
| The script, in all | 49.7 s (`time -p`: real 51.39) | 72.6 s (real 73.87) |
| Exit code | 0 | 0 |
| Ray's session directory | `/tmp/ray/session_2026-10-10_18-30-18_915824_5837` | `/tmp/ray/session_2026-10-10_18-31-08_834636_7580` |
| Ray processes before and after (the script's own check, and log 11's) | 0 and 0 | 0 and 0 |

The prompt expected `ray.init` in about 5 s and the sequence in 10–13 s (prompt 11 §1.1). The times
here are this machine's load at the time, as the dispatch note found (15–20 s and 40–72 s); the
script asserts no time. At 2.55.1, `ray.init` prints a `FutureWarning` about an environment
variable it will stop overriding; it is Ray's.

### 4.2 The output, low end

```text
2026-10-10 18:30:26,253	INFO worker.py:1841 -- Started a local Ray instance.
Environment:
    Python       3.12.15 (<scratch>/smoke-lo/venv/bin/python)
    Ray          2.43.0
    SQLAlchemy   2.0.39
    SQLite       3.53.4
    datastorekit 0.2.1
    imported from <scratch>/smoke-lo/tree/datastorekit/__init__.py
Ray processes before: 0
Ray started in 13.2 s, at 127.0.0.1; session directory /tmp/ray/session_2026-10-10_18-30-18_915824_5837
step 1: write every class (read-write)
PASS  step 1 (4.6 s): wrote store_tag 3, keypoint 3, dial_setting 2, knob_setting 1, gauge_setting 2, routing_rule 2, ephemeral_probe 1, keypoint_alias 3, Gadget 2, Tessera 6, Sample 4, Trace 2, Weave 1
step 2: keyed vectorized get, the caller's dicts
    after __exit__, the pool referenced: 4 of 4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store)
PASS  step 2 (0.0 s): serials [1, 2] (step 1's), the caller's dicts unchanged
step N: a closed pool holds its names (prompt 11 §1.3)
    the second open raised builtins.ValueError: The name SerialPoolBroker (namespace=None) is already taken. Please use a different name or get the existing actor using ray.get_actor('SerialPoolBroker', namespace='None')
    after the exception is dropped, the pool referenced: 4 of 4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store)
    after del and gc.collect(): 0 of 4 held, after 0.0 s
PASS  step N (0.2 s): before the second open, 4 of 4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store); the second open raised builtins.ValueError naming SerialPoolBroker; after the exception was dropped, 4 of 4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store); after del and gc.collect(), none held (0.0 s)
step 3: reopen read-write, the same get
    after __exit__, the pool referenced: 4 of 4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store)
    after del and gc.collect(): 0 of 4 held, after 0.0 s
PASS  step 3 (5.8 s): serials [1, 2], the caller's dicts unchanged
step 4: read-only pool, the same get
    after __exit__, the pool referenced: 3 of 3 held (shard0000-store, shard0001-store, shard0002-store)
    after del and gc.collect(): 0 of 3 held, after 0.0 s
PASS  step 4 (6.9 s): read-only: serials [1, 2], the caller's dicts unchanged
step 5: refused open, Weave left out
    the constructor printed, as not supplied: ['Weave']
    after the exception is dropped: 0 of 4 held
PASS  step 5 (0.1 s): builtins.RuntimeError: Mismatch between sharded tables supplied to the constructor and read from the existing ShardedPool; 0 of 4 held
step 6: read-write open after the refusal
    after __exit__, the pool referenced: 4 of 4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store)
    after del and gc.collect(): 0 of 4 held, after 0.0 s
PASS  step 6 (9.2 s): read-write open after the refusal: serials [1, 2], the caller's dicts unchanged
ray.shutdown(); waited 0.2 s for its processes
Ray processes after: 0
Summary: every step passed; 0 Ray process(es) left; 49.7 s in all
real 51.39
user 11.11
sys 5.32
exit=0
```

### 4.3 The output, high end

```text
2026-10-10 18:31:22,082	INFO worker.py:2012 -- Started a local Ray instance.
<scratch>/smoke-hi/venv/lib/python3.13/site-packages/ray/_private/worker.py:2051: FutureWarning: Tip: In future versions of Ray, Ray will no longer override accelerator visible devices env var if num_gpus=0 or num_gpus=None (default). To enable this behavior and turn off this error message, set RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO=0
  warnings.warn(
Environment:
    Python       3.13.16 (<scratch>/smoke-hi/venv/bin/python)
    Ray          2.55.1
    SQLAlchemy   2.0.46
    SQLite       3.53.4
    datastorekit 0.2.1
    imported from <scratch>/smoke-hi/tree/datastorekit/__init__.py
Ray processes before: 0
Ray started in 15.8 s, at 127.0.0.1; session directory /tmp/ray/session_2026-10-10_18-31-08_834636_7580
step 1: write every class (read-write)
PASS  step 1 (3.7 s): wrote store_tag 3, keypoint 3, dial_setting 2, knob_setting 1, gauge_setting 2, routing_rule 2, ephemeral_probe 1, keypoint_alias 3, Gadget 2, Tessera 6, Sample 4, Trace 2, Weave 1
step 2: keyed vectorized get, the caller's dicts
    after __exit__, the pool referenced: 4 of 4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store)
PASS  step 2 (3.1 s): serials [1, 2] (step 1's), the caller's dicts unchanged
step N: a closed pool holds its names (prompt 11 §1.3)
    the second open raised ray.exceptions.ActorAlreadyExistsError: The name SerialPoolBroker (namespace=None) is already taken. Please use a different name or get the existing actor using ray.get_actor('SerialPoolBroker', namespace='None')
    after the exception is dropped, the pool referenced: 4 of 4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store)
    after del and gc.collect(): 0 of 4 held, after 0.2 s
PASS  step N (3.1 s): before the second open, 4 of 4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store); the second open raised ray.exceptions.ActorAlreadyExistsError naming SerialPoolBroker; after the exception was dropped, 4 of 4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store); after del and gc.collect(), none held (0.2 s)
step 3: reopen read-write, the same get
    after __exit__, the pool referenced: 4 of 4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store)
    after del and gc.collect(): 0 of 4 held, after 0.0 s
PASS  step 3 (11.8 s): serials [1, 2], the caller's dicts unchanged
step 4: read-only pool, the same get
    after __exit__, the pool referenced: 3 of 3 held (shard0000-store, shard0001-store, shard0002-store)
    after del and gc.collect(): 0 of 3 held, after 0.0 s
PASS  step 4 (21.4 s): read-only: serials [1, 2], the caller's dicts unchanged
step 5: refused open, Weave left out
    the constructor printed, as not supplied: ['Weave']
    after the exception is dropped: 0 of 4 held
PASS  step 5 (0.1 s): builtins.RuntimeError: Mismatch between sharded tables supplied to the constructor and read from the existing ShardedPool; 0 of 4 held
step 6: read-write open after the refusal
    after __exit__, the pool referenced: 4 of 4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store)
    after del and gc.collect(): 0 of 4 held, after 0.0 s
PASS  step 6 (7.3 s): read-write open after the refusal: serials [1, 2], the caller's dicts unchanged
ray.shutdown(); waited 0.1 s for its processes
Ray processes after: 0
Summary: every step passed; 0 Ray process(es) left; 72.6 s in all
real 73.87
user 11.66
sys 5.23
exit=0
```

### 4.4 The steps, and what each shows

| Step | What it asserts | Low end | High end |
|---|---|---|---|
| 1 | a read-write pool opens a new store, and `build.write_every_class` writes 3 tags, 3 keypoints, 2 dials, 1 knob, 2 gauges, 2 rules, 1 probe, 3 aliases, 2 Gadgets, 6 Tesserae, 4 Samples, 2 Traces and 1 Weave | PASS | PASS |
| 2 | `object_get_vectorized("Tessera", {"k": alias}, payload_data=…)` of the first alias's two Tesserae (a keyed get) finds step 1's serials, `[1, 2]`, and leaves the caller's dicts equal to a deep copy taken before | PASS | PASS |
| N | the closed pool still referenced: a second read-write open is refused naming `SerialPoolBroker`; the names are held after the exception is dropped, and free after `del` and `gc.collect()` (§4.5) | PASS: `builtins.ValueError` | PASS: `ray.exceptions.ActorAlreadyExistsError` |
| 3 | the store reopened read-write: the keypoint and alias got again have step 1's serials, and the same get finds `[1, 2]` | PASS | PASS |
| 4 | a read-only pool: the same, through the lookup serial `set_lookup_version` gives it | PASS | PASS |
| 5 | an open with `Weave` left out of `sharded_tables` raises exactly `RuntimeError` "Mismatch between sharded tables supplied to the constructor and read from the existing ShardedPool"; the constructor printed `Weave` as not supplied; no name is held | PASS | PASS |
| 6 | a read-write open after the refusal, and the same get | PASS | PASS |

**Two breakages**, each a diff exactly as applied to its own export of the working tree, at the high
end, never committed (log 11 §5 gives both diffs, which pass `git apply --check` and `-R --check`):

- **(a) 08a reverted**: `payload_data = [{**value, **shard_key} for value in payload_data]`
  (`SQL/ShardedPool.py:3348`) replaced by `for value in payload_data:` / `value.update(shard_key)`.
  Exit 1. Steps 2, 3, 4 and 6 fail: "the caller's payload dicts changed: keys added ['k']; 2 dicts,
  of which 2 differ from what was passed (serials found [1, 2])". Steps 1, N and 5 pass.
- **(b) the read-only pool's `set_lookup_version` call removed** (`SQL/ShardedPool.py:614-621`, the
  comment and the call). Exit 1. Step 4 fails with `ray.exceptions.RayTaskError(RuntimeError)`
  from an actor: 'Datastore "shard0002-store": cannot look up "Tessera", whose lookups are keyed on
  the version serial, before the serial of label "standin" is set: the pool sets it with
  set_version, or with set_lookup_version on a read-only pool. Nothing was looked up'. Every other
  step passes.

Ray was stopped after each, with no Ray process left (log 11 §4.2).

### 4.5 A closed pool holds its actors' names (§6.2)

Re-taken by step N, and by the record after every pool's `__exit__`:

| | Low end (2.43.0) | High end (2.55.1) |
|---|---|---|
| After the read-write pool's `__exit__`, the pool referenced | 4 of 4 names held: `SerialPoolBroker`, `shard0000-store`, `shard0001-store`, `shard0002-store` | the same |
| A second read-write open | refused: `builtins.ValueError` | refused: `ray.exceptions.ActorAlreadyExistsError` (a subclass of `ValueError`) |
| Its message | "The name SerialPoolBroker (namespace=None) is already taken. Please use a different name or get the existing actor using ray.get_actor('SerialPoolBroker', namespace='None')" | the same |
| After that exception is dropped, the first pool still referenced | 4 of 4 held | 4 of 4 held |
| After `del` and `gc.collect()` | none held, after 0.0 s | none held, after 0.2 s |
| A read-only pool after `__exit__`, referenced | 3 of 3 shard names held (no broker) | the same |
| After it is dropped | none held, after 0.0 s | none held, after 0.0 s |

The times are a poll every 0.1 s. The cause is `SQL/ShardedPool.py:307` (the broker's name), `:318`
and `:592` (the read-write and read-only shards' names) and `__exit__` at `:808-820`, which
releases no actor, at `33778b0`. SGK names the same actors at `Datastore/SQL/ShardedPool.py:294`,
`:305` and `:544`, at `6f7f291` and `b510bc9`. The smoke script drops every pool before the next
open, so it records the behaviour without failing on it.

### 4.6 The smoke run after the fix (`actor-names` prompt 01, 2026-10-10)

*Added by [`actor-names` prompt 01](../prompts/actor-names/01-a-closed-pool-releases-its-actor-names.md)
(log [`01-a-closed-pool-releases-its-actor-names.md`](../prompts/actor-names/logs/01-a-closed-pool-releases-its-actor-names.md)),
under `CLAUDE.md` rule 6. §4.1–§4.5 above are of `v0.2.1` (`33778b0`) and the script as extraction
prompt 11 committed it, and stay true of them: at `v0.2.1` a closed pool holds its actors' names
until it is collected, as §4.5 measured. This subsection is of `actor-names` prompt 01's tree, where
`ShardedPool.__exit__` and a refused open kill the pool's actors (`docs/client-contract.md` §9.3).*

That prompt changed the script (SHA-256 `e9be6ffaf35ce05fabfd4788a90a9101c761b4b57bdd0baf58464d16d51cc331`)
in two steps, and in the record after every `__exit__`; steps 1–6 are as before:

- **step N, reversed.** With the closed pool of steps 1 and 2 still referenced, none of its names
  is held, and a second read-write open works at once. That pool is closed, none of its names is
  held, and both pools are dropped, in a `finally`. If the second open is refused, the step fails
  naming the collision and the record;
- **step C, new: two open pools collide.** With a pool open, a second read-write open raises
  `ValueError` with "is already taken" and `SerialPoolBroker` in its message, and the first pool
  then serves step 2's get;
- **the record after each `__exit__`**, the pool still referenced, now expects no name held, for
  every pool: step N checks step 2's pool's, and steps N, C, 3, 4 and 6 their own, after the
  close. Each pool is still dropped before the next open.

Each end ran from a fresh offline venv with a fresh export of the working tree installed editable
(`--no-deps --no-build-isolation`, after `ray`, `sqlalchemy` and `setuptools`), with `PYTHONPATH`
unset, from the export's root: §10.2's commands, with an export of the working tree in place of
`git archive HEAD`. `<scratch01>` is the prompt's scratch directory
(`<session scratchpad>/agent-01`).

| | Low end | High end |
|---|---|---|
| Python / Ray / SQLAlchemy / SQLite | 3.12.15 / 2.43.0 / 2.0.39 / 3.53.4 | 3.13.16 / 2.55.1 / 2.0.46 / 3.53.4 |
| Started (BST) | 21:15:21 | 21:15:40 |
| `ray.init` | 4.0 s | 5.1 s |
| The script, in all | 13.2 s (`time -p`: real 13.44) | 15.6 s (real 15.79) |
| Exit code | 0 | 0 |
| Ray's session directory | `/tmp/ray/session_2026-10-10_21-15-23_174455_99956` | `/tmp/ray/session_2026-10-10_21-15-41_686311_458` |
| Ray processes before and after (the script's own check, and the log's, by the same rule) | 0 and 0 | 0 and 0 |

**What it shows**, at both ends:

| | Low end (2.43.0) | High end (2.55.1) |
|---|---|---|
| After the read-write pool's `__exit__`, the pool referenced | 0 of 4 names held | the same |
| A second read-write open, the closed pool referenced | works at once: 1.2 s | works at once: 1.4 s |
| A second open while a pool is open (step C) | refused: `builtins.ValueError` | refused: `ray.exceptions.ActorAlreadyExistsError` |
| Its message | "The name SerialPoolBroker (namespace=None) is already taken. Please use a different name or get the existing actor using ray.get_actor('SerialPoolBroker', namespace='None')" | the same |
| The open pool after that refusal | serves step 2's get: serials `[1, 2]` | the same |
| A read-only pool after `__exit__`, referenced | 0 of 3 shard names held | the same |
| After a refused open (step 5) | 0 of 4 held | the same |

#### 4.6.1 The output, low end

```text
2026-10-10 21:15:26,255	INFO worker.py:1841 -- Started a local Ray instance.
Environment:
    Python       3.12.15 (<scratch01>/smoke-lo/venv/bin/python)
    Ray          2.43.0
    SQLAlchemy   2.0.39
    SQLite       3.53.4
    datastorekit 0.2.1
    imported from <scratch01>/smoke-lo/tree/datastorekit/__init__.py
Ray processes before: 0
Ray started in 4.0 s, at 127.0.0.1; session directory /tmp/ray/session_2026-10-10_21-15-23_174455_99956
step 1: write every class (read-write)
PASS  step 1 (0.7 s): wrote store_tag 3, keypoint 3, dial_setting 2, knob_setting 1, gauge_setting 2, routing_rule 2, ephemeral_probe 1, keypoint_alias 3, Gadget 2, Tessera 6, Sample 4, Trace 2, Weave 1
step 2: keyed vectorized get, the caller's dicts
    after __exit__, the pool referenced: 0 of 4 held
PASS  step 2 (0.0 s): serials [1, 2] (step 1's), the caller's dicts unchanged
step N: a closed pool releases its names
    a second read-write open, the first pool referenced: opened in 1.2 s
    after __exit__, the pool referenced: 0 of 4 held
    after del and gc.collect(): 0 of 4 held, after 0.0 s
PASS  step N (1.2 s): after __exit__, the pool referenced, 0 of 4 held; a second read-write open worked at once (1.2 s); after its __exit__, 0 of 4 held
step C: two open pools collide
    the second open raised builtins.ValueError: The name SerialPoolBroker (namespace=None) is already taken. Please use a different name or get the existing actor using ray.get_actor('SerialPoolBroker', namespace='None')
    after __exit__, the pool referenced: 0 of 4 held
    after del and gc.collect(): 0 of 4 held, after 0.0 s
PASS  step C (1.3 s): the second open raised builtins.ValueError naming SerialPoolBroker; the first pool then: serials [1, 2], the caller's dicts unchanged; after its __exit__, 0 of 4 held
step 3: reopen read-write, the same get
    after __exit__, the pool referenced: 0 of 4 held
    after del and gc.collect(): 0 of 4 held, after 0.0 s
PASS  step 3 (1.2 s): serials [1, 2], the caller's dicts unchanged
step 4: read-only pool, the same get
    after __exit__, the pool referenced: 0 of 3 held
    after del and gc.collect(): 0 of 3 held, after 0.0 s
PASS  step 4 (1.2 s): read-only: serials [1, 2], the caller's dicts unchanged
step 5: refused open, Weave left out
    the constructor printed, as not supplied: ['Weave']
    after the exception is dropped: 0 of 4 held
PASS  step 5 (0.0 s): builtins.RuntimeError: Mismatch between sharded tables supplied to the constructor and read from the existing ShardedPool; 0 of 4 held
step 6: read-write open after the refusal
    after __exit__, the pool referenced: 0 of 4 held
    after del and gc.collect(): 0 of 4 held, after 0.0 s
PASS  step 6 (1.2 s): read-write open after the refusal: serials [1, 2], the caller's dicts unchanged
ray.shutdown(); waited 0.0 s for its processes
Ray processes after: 0
Summary: every step passed; 0 Ray process(es) left; 13.2 s in all
real 13.44
user 3.68
sys 1.01
exit=0
```

#### 4.6.2 The output, high end

```text
2026-10-10 21:15:45,740	INFO worker.py:2012 -- Started a local Ray instance.
<scratch01>/smoke-hi/venv/lib/python3.13/site-packages/ray/_private/worker.py:2051: FutureWarning: Tip: In future versions of Ray, Ray will no longer override accelerator visible devices env var if num_gpus=0 or num_gpus=None (default). To enable this behavior and turn off this error message, set RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO=0
  warnings.warn(
Environment:
    Python       3.13.16 (<scratch01>/smoke-hi/venv/bin/python)
    Ray          2.55.1
    SQLAlchemy   2.0.46
    SQLite       3.53.4
    datastorekit 0.2.1
    imported from <scratch01>/smoke-hi/tree/datastorekit/__init__.py
Ray processes before: 0
Ray started in 5.1 s, at 127.0.0.1; session directory /tmp/ray/session_2026-10-10_21-15-41_686311_458
step 1: write every class (read-write)
PASS  step 1 (1.0 s): wrote store_tag 3, keypoint 3, dial_setting 2, knob_setting 1, gauge_setting 2, routing_rule 2, ephemeral_probe 1, keypoint_alias 3, Gadget 2, Tessera 6, Sample 4, Trace 2, Weave 1
step 2: keyed vectorized get, the caller's dicts
    after __exit__, the pool referenced: 0 of 4 held
PASS  step 2 (0.2 s): serials [1, 2] (step 1's), the caller's dicts unchanged
step N: a closed pool releases its names
    a second read-write open, the first pool referenced: opened in 1.4 s
    after __exit__, the pool referenced: 0 of 4 held
    after del and gc.collect(): 0 of 4 held, after 0.0 s
PASS  step N (1.5 s): after __exit__, the pool referenced, 0 of 4 held; a second read-write open worked at once (1.4 s); after its __exit__, 0 of 4 held
step C: two open pools collide
    the second open raised ray.exceptions.ActorAlreadyExistsError: The name SerialPoolBroker (namespace=None) is already taken. Please use a different name or get the existing actor using ray.get_actor('SerialPoolBroker', namespace='None')
    after __exit__, the pool referenced: 0 of 4 held
    after del and gc.collect(): 0 of 4 held, after 0.0 s
PASS  step C (1.4 s): the second open raised ray.exceptions.ActorAlreadyExistsError naming SerialPoolBroker; the first pool then: serials [1, 2], the caller's dicts unchanged; after its __exit__, 0 of 4 held
step 3: reopen read-write, the same get
    after __exit__, the pool referenced: 0 of 4 held
    after del and gc.collect(): 0 of 4 held, after 0.0 s
PASS  step 3 (1.3 s): serials [1, 2], the caller's dicts unchanged
step 4: read-only pool, the same get
    after __exit__, the pool referenced: 0 of 3 held
    after del and gc.collect(): 0 of 3 held, after 0.0 s
PASS  step 4 (1.3 s): read-only: serials [1, 2], the caller's dicts unchanged
step 5: refused open, Weave left out
    the constructor printed, as not supplied: ['Weave']
    after the exception is dropped: 0 of 4 held
PASS  step 5 (0.0 s): builtins.RuntimeError: Mismatch between sharded tables supplied to the constructor and read from the existing ShardedPool; 0 of 4 held
step 6: read-write open after the refusal
    after __exit__, the pool referenced: 0 of 4 held
    after del and gc.collect(): 0 of 4 held, after 0.0 s
PASS  step 6 (1.3 s): read-write open after the refusal: serials [1, 2], the caller's dicts unchanged
ray.shutdown(); waited 0.1 s for its processes
Ray processes after: 0
Summary: every step passed; 0 Ray process(es) left; 15.6 s in all
real 15.79
user 4.16
sys 1.10
exit=0
```

#### 4.6.3 The fix reverted, under Ray

The prompt's breakage (e): its breakage (a), the `_kill_actors()` call removed from `__exit__`
(the log's §5 gives the diff), applied to a fresh export of the working tree, and the script run at
the high end as above. Step N fails on the collision and on its record, 4 of 4 names held after
`__exit__`; steps C and 3–6 are not run; the script exits 1, and Ray leaves no process:

```text
2026-10-10 21:16:10,579	INFO worker.py:2012 -- Started a local Ray instance.
<scratch01>/break-e/venv/lib/python3.13/site-packages/ray/_private/worker.py:2051: FutureWarning: Tip: In future versions of Ray, Ray will no longer override accelerator visible devices env var if num_gpus=0 or num_gpus=None (default). To enable this behavior and turn off this error message, set RAY_ACCEL_ENV_VAR_OVERRIDE_ON_ZERO=0
  warnings.warn(
Environment:
    Python       3.13.16 (<scratch01>/break-e/venv/bin/python)
    Ray          2.55.1
    SQLAlchemy   2.0.46
    SQLite       3.53.4
    datastorekit 0.2.1
    imported from <scratch01>/break-e/tree/datastorekit/__init__.py
Ray processes before: 0
Ray started in 4.8 s, at 127.0.0.1; session directory /tmp/ray/session_2026-10-10_21-16-06_706126_720
step 1: write every class (read-write)
PASS  step 1 (1.1 s): wrote store_tag 3, keypoint 3, dial_setting 2, knob_setting 1, gauge_setting 2, routing_rule 2, ephemeral_probe 1, keypoint_alias 3, Gadget 2, Tessera 6, Sample 4, Trace 2, Weave 1
step 2: keyed vectorized get, the caller's dicts
    after __exit__, the pool referenced: 4 of 4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store)
PASS  step 2 (0.2 s): serials [1, 2] (step 1's), the caller's dicts unchanged
step N: a closed pool releases its names
    the second open raised ray.exceptions.ActorAlreadyExistsError: The name SerialPoolBroker (namespace=None) is already taken. Please use a different name or get the existing actor using ray.get_actor('SerialPoolBroker', namespace='None')
    after del and gc.collect(): 0 of 4 held, after 0.0 s
FAIL  step N (0.1 s): __main__.StepFailed: after __exit__, the pool referenced, 4 of 4 held (SerialPoolBroker, shard0000-store, shard0001-store, shard0002-store); the second open raised ray.exceptions.ActorAlreadyExistsError: The name SerialPoolBroker (namespace=None) is already taken. Please use a different name or get the existing actor using ray.get_actor('SerialPoolBroker', namespace='None')
NOT RUN  step C: two open pools collide: needs step N
NOT RUN  step 3: reopen read-write, the same get: needs step N
NOT RUN  step 4: read-only pool, the same get: needs step N
NOT RUN  step 5: refused open, Weave left out: needs step N
NOT RUN  step 6: read-write open after the refusal: needs step N
ray.shutdown(); waited 0.1 s for its processes
Ray processes after: 0
Summary: a step did not pass; 0 Ray process(es) left; 8.8 s in all
real 9.00
user 3.93
sys 0.86
exit=1
```

---

## 5. The pin (U42)

### 5.1 The install

Into a fresh venv, offline from `uv`'s cache:

```bash
uv venv --offline -p /opt/local/bin/python3.13 <scratch>/pin/venv
uv pip install --offline --python <scratch>/pin/venv/bin/python ray==2.55.1 sqlalchemy==2.0.46 setuptools
```

which installed `ray==2.55.1`, `sqlalchemy==2.0.46` and `setuptools==84.0.0`. Then, from
`<scratch>/pin/outside`, a directory outside the repository, with `PYTHONPATH` unset, the one
network use of the campaign:

```bash
env -u PYTHONPATH uv pip install --no-cache --no-deps --no-build-isolation \
    --python <scratch>/pin/venv/bin/python \
    "datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.1"
```

```text
Using Python 3.13.16 environment at: <scratch>/pin/venv
Resolved 1 package in 596ms
   Updating https://github.com/ds283/DatastoreKit (v0.2.1)
    Updated https://github.com/ds283/DatastoreKit (33778b04eafc0b9f01f5e272eb0f9b679eb6f0c7)
   Building datastorekit @ git+https://github.com/ds283/DatastoreKit@33778b04eafc0b9f01f5e272eb0f9b679eb6f0c7
      Built datastorekit @ git+https://github.com/ds283/DatastoreKit@33778b04eafc0b9f01f5e272eb0f9b679eb6f0c7
Prepared 1 package in 3.69s
Installed 1 package in 7ms
 + datastorekit==0.2.1 (from git+https://github.com/ds283/DatastoreKit@33778b04eafc0b9f01f5e272eb0f9b679eb6f0c7)
```

Exit 0, at 18:36. `--no-cache` clones from GitHub afresh, into a temporary cache, so the bytes are
GitHub's and not an earlier build's; `--no-deps` fetches nothing but the package;
`--no-build-isolation` builds with the venv's `setuptools`, so nothing comes from an index. The
build backend's version does not matter to the comparison below, which is of content hashes.

`datastorekit-0.2.1.dist-info/direct_url.json`:

```json
{"url":"https://github.com/ds283/DatastoreKit","vcs_info":{"vcs":"git","commit_id":"33778b04eafc0b9f01f5e272eb0f9b679eb6f0c7","requested_revision":"v0.2.1"}}
```

### 5.2 The 20 package files, against 10's wheel

10's wheel was rebuilt offline from `git archive 33778b0` with `uv build --offline --wheel`:
`datastorekit-0.2.1-py3-none-any.whl`, 97,849 bytes, `Generator: setuptools (84.0.0)`, its
`RECORD`'s SHA-256 `f840ffa4c28f1d40f6578abb56a033d6faf4356f4877c62f60ebf75ab2d96c5e`, log 10
§5.3's. The installed `RECORD`'s 20 lines under `datastorekit/`, sorted, are **identical** to the
wheel's (`diff` empty; the sorted 20 lines hash to `90fb77bf…6bf1` on both sides):

```text
datastorekit/__init__.py,sha256=d4jFn_10vTntTdrL55Uv5OL8ivVXos6RMnAS7LzHB2I,36
datastorekit/_timing.py,sha256=nVIt3BwSNrdsPFCrS7PCLny4GDRU45lmS36meB51D5c,1926
datastorekit/contract.py,sha256=mL4c_XiNgz_Dae6qcbd4VF0fvqOYKP9Rnlklcv_20u0,2955
datastorekit/defaults.py,sha256=_KNG84HSR3dfI0F6fyeP2EwEZgdWyefF-ZX2gg1ZfnQ,170
datastorekit/object.py,sha256=fdnKd2nZPKgNFkhq5jAxXl997LE2mOVTXo4jHz3Dmb4,491
datastorekit/replication.py,sha256=DE3emp78TeM_mNe1moIEJzDLNjg0z7ENEDdev8MQcus,11822
datastorekit/shard_paths.py,sha256=ClF3DbF59OE9GP0XrSZKTeR5h1aguDT0UwDbI4sVqNA,5744
datastorekit/SQL/__init__.py,sha256=0NJQ5xLlijsctKyX-P_eoirep49eu4xFItZcUNZEFcE,33
datastorekit/SQL/ClientPool.py,sha256=fg3CYaKr-kLe03RHu5Fek_8Q_SRAifQEeru3l7cdiFY,6847
datastorekit/SQL/Datastore.py,sha256=Xs7WY7byYchDTmHs7DphIgBXcklgWC1aeC02-pPdUC4,40188
datastorekit/SQL/factory_base.py,sha256=plSnmopwl3n4hkeExHNx0N76EYpOH6CAzMT60eZ3CPs,2233
datastorekit/SQL/ProfileAgent.py,sha256=qA4iGTOlkDhDIYAyM_bCxGHAjx6CWkGsRznNUlyGSWg,12633
datastorekit/SQL/schema.py,sha256=otRLZyAEpXTEfAPlE-EE_ub7ct4N2NK_49s1Xo2h1WE,23111
datastorekit/SQL/SerialPoolBroker.py,sha256=kUUErdUfmjBhYR8U-M98gn50SifYASfWBkr8I6XvQ7w,5524
datastorekit/SQL/ShardedPool.py,sha256=_Ij01ywRDgBlIQKVX7Elcm51DOyxc0SRJUvmgaXA0IE,167575
datastorekit/store_inventory.py,sha256=4PJPPpQevLoGrSzOYobAZKmJHV9da-P96x9IvQ29Tz8,45013
datastorekit/store_reader.py,sha256=rjf-qnRJLiiB84IfRCX5zlHlRa4EHag_Fp_HdqR3vAg,9668
datastorekit/tools/__init__.py,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0
datastorekit/tools/shard_key_audit.py,sha256=5ZFbqwBunfsG7XNs7UbmkqYsWkOG43A-JI_3DbY602U,11723
datastorekit/tools/sharded_store.py,sha256=1TJ6mNS5b7e36ImUGOW92_M3xTayV06OrLanHVIUgWs,2854
```

The installed `RECORD` as a whole differs from the wheel's: the installer adds `INSTALLER`
(`uv`), `REQUESTED`, `direct_url.json` and `uv_build.json` to the `dist-info`. The 20 lines are the
comparison, not the file's hash (prompt 11 §1.2).

### 5.3 The three checks

From `<scratch>/pin/outside`, with `PYTHONPATH` unset:

```text
datastorekit.__file__ <scratch>/pin/venv/lib/python3.13/site-packages/datastorekit/__init__.py
ShardedPool module <scratch>/pin/venv/lib/python3.13/site-packages/datastorekit/SQL/ShardedPool.py
version 0.2.1
ModuleNotFoundError: No module named 'datastorekit.tests'
```

The package imports from `site-packages`; `importlib.metadata.version("datastorekit")` is `0.2.1`;
the test package is not installed. The venv was deleted after.

### 5.4 The wrong pin, (c)

`@v0.2.0`, installed offline from this repository (`git+file:///Users/ds283/Documents/Code/DatastoreKit@v0.2.0`,
with §5.1's flags and `--offline`) into a venv of its own, so that the network is reached once: it
installs `datastorekit==0.2.0` from `240028e4514efb69ef9bcaac1847fd27a4c9aa3d`, with
`"requested_revision":"v0.2.0"`. The version check, an assertion that the installed version is
`0.2.1`, fails: "AssertionError: version check: expected 0.2.1, installed 0.2.0". Its `RECORD` has
20 lines under `datastorekit/`, with the same paths; **13 differ** from 10's wheel by hash:
`_timing.py`, `contract.py`, `defaults.py`, `replication.py`, `shard_paths.py`,
`store_inventory.py`, `store_reader.py`, `SQL/Datastore.py`, `SQL/factory_base.py`,
`SQL/schema.py`, `SQL/ShardedPool.py`, `tools/shard_key_audit.py` and `tools/sharded_store.py`.
They are exactly the layer files of `git diff --name-only 240028e 33778b0 -- datastorekit`. The
venv was deleted after.

---

## 6. Issues

### 6.1 Resolved on the board (§4), eight

| Issue | Opened by | Closed by | Pinned by |
|---|---|---|---|
| `[01-ported-tests-use-sgk-table-names]` | 01 | 02, `e988e69` (U8: the 15 lines re-fixtured onto the client's names) | no test of its own; `test_layer_is_generic`'s vocabulary guard since 04b |
| `[01-no-ported-test-pins-the-shard-key-assignment]` | the review of 01 | 03a, `11247c7` | `datastorekit/tests/test_shard_key_assignment.py` (three tests the `key_id` binding fails) |
| `[02-no-test-reaches-revalidate]` | 02 | 03a, `11247c7` | `test_reconcile_at_open.TestKillAndReopen.test_validate_of_a_background_model` |
| `[04a-no-test-pins-a-second-parent-set-member]` | the review of 04a | 04b, `0c66505` | `datastorekit/tests/test_parent_set_members.py` |
| `[02-an-unsupplied-sharded-table-raises-keyerror]` | 02 | 08a, `f938844` | `datastorekit/tests/test_unsupplied_sharded_table.py`; under Ray, the smoke run's step 5 |
| `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]` | 06 | 08a, `f938844` | `datastorekit/tests/test_vectorized_get_payloads.py`; under Ray, the smoke run's step 2 |
| `[05-a-refused-open-leaves-its-engines-undisposed]` | 05 | 08b, `efedc8d` | `datastorekit/tests/test_refused_open_closes_engines.py` |
| `[01-package-prose-names-sgks-layout]` | 01 | 09, `cad7bc1` | `datastorekit/tests/test_prose_names_no_source.py`, and `test_layer_is_generic` with `KNOWN_HITS` empty |

### 6.2 Opened by 11

`[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]`, on the board's §3 with its
measurement (§4.5), cause, SGK's lines and impact: a client that opens two pools in one process,
or reopens a store while it still holds a closed pool, is refused by Ray. It is inherited from
SGK, not fixed, and assigned to no campaign. `docs/OPEN_ISSUES.md` §1.1 has its row.

### 6.3 The four inherited issues, at `v0.2.1`

They are SGK's, indexed in `docs/OPEN_ISSUES.md` §1.2, and out of scope (U33). Log 01 §4.6 gave
their code at `8bc60a5`. Read at `33778b0`; whether 08a, 08b or 09 changed the code each describes
was decided by comparing each function's AST, docstrings removed, at `8bc60a5`, `240028e` and
`33778b0` (log 11 §4.6), and by reading.

| Issue | Its code at `v0.2.1` (`33778b0`) | Changed by 08a, 08b or 09? |
|---|---|---|
| `[00-a-drop-action-drops-a-replicated-table-outside-the-in-flight-record]` | each actor drops its `drop_tables` in its constructor, `datastorekit/SQL/Datastore.py:142` (`self._drop_tables(drop_tables)`; the method `:438-469`), and recreates them by `_ensure_tables` (`:143`; `:427-430`), outside any in-flight record; the pool gives every actor the same list (`SQL/ShardedPool.py:329`) | No. `_drop_tables` and `_ensure_tables` are the same code at all three trees; `Datastore.__init__` changed only at 06 (the lookup serial), not since |
| `[00-a-new-stores-first-open-can-leave-a-primary-without-its-shards]` | a new store's primary and its `shards` table are written first (`SQL/ShardedPool.py:234-257`, `_write_shard_data()` at `:253`, the method `:925-984`); the shards' actors, which create the shard files, are made afterwards (`:315-333`); the next open is refused by `_check_shard_files` (`:277`; the method `:1119-1139`) | The order and the two methods, no. 08b put the open under a guard (`:203-207`, `_open` from `:209`, `_close_refused_open` from `:375`) that closes the actors and disposes the engine when the open raises; it deletes no file, so an interrupted first open still leaves the primary |
| `[00-the-inventory-cannot-see-a-serial-split]` | `datastorekit/store_inventory.py`: a replicated class is compared across shards on key, tags, validated flag and value count (the module docstring, `:53-55`; `_combine`, `:826-913`) | No. `_combine` is the same code at all three trees; 09 changed the module's prose only |
| `[01-cross-filesystem-move-advice-says-delete-by-hand]` | `ShardedPool._failure_message`, `SQL/ShardedPool.py:2936-2967`; the `EXDEV` branch and "copy it instead, and then delete the source by hand" at `:2962-2966`. The ported test asserting it is `datastorekit/tests/test_copy_move_store.py:596` (the assertion `:606`) | No: the same code at all three trees |

---

## 7. Deviations across the campaign

**How they were counted.** An entry is a numbered item of a log's §2, "Deviations from the
prompt", at its top level. Its class is the last of the three labels in its text; an entry naming
none is "unlabelled". The sentence "No (other) UNINTENDED DRIFT was found" that ends most §2s is not
an entry. A scratch parser listed every entry with its label, and each unlabelled entry and each
UNINTENDED DRIFT was read (log 11 §4.7).

| Log | Entries | STRUCTURALLY REQUIRED | IMPLEMENTATION CHOICE | UNINTENDED DRIFT | Unlabelled |
|---|---|---|---|---|---|
| 01 | 10 | 3 | 7 | 0 | 0 |
| 02 | 11 | 3 | 7 | 0 | 1 (item 11) |
| 03a | 11 | 3 | 7 | 0 | 1 (item 11) |
| 03b | 17 | 4 | 12 | 0 | 1 (item 17) |
| 04a | 25 | 12 | 13 | 0 | 0 |
| 04b | 16 | 8 | 8 | 0 | 0 |
| 05 | 15 | 5 | 10 | 0 | 0 |
| 06 | 15 | 6 | 9 | 0 | 0 |
| 07a | 16 | 3 | 8 | 0 | 5 (items 4–8) |
| 08a | 19 | 7 | 9 | 0 | 3 (items 7–9) |
| 08b | 17 | 4 | 10 | 1 | 2 (items 4, 15) |
| 09 | 20 | 5 | 14 | 1 | 0 |
| 10 | 15 | 9 | 5 | 1 | 0 |
| **All** | **207** | **72** | **119** | **3** | **13** |

The unlabelled entries are facts recorded "as found" (a correction of the note found to hold, or a
fact differing from the prompt) or, in 02, 03a and 03b, a statement that the ported prose was left
unchanged as the prompt said. Prompt 11 §1.5 gave 67, 114 and "one or two" UNINTENDED DRIFT per log;
those are counts of the labels' words, as it warned. They are right as word counts: five entries
of each of the first two classes have their label wrapped across two lines, which a line-by-line
count misses (72 − 5 = 67, 119 − 5 = 114), and the 15 occurrences of "UNINTENDED DRIFT" are the
twelve "No … UNINTENDED DRIFT" sentences and the three entries.

**Every UNINTENDED DRIFT entry:**
- **log 08b §2 item 9**: the new test module was first written into `datastorekit/tests/` beside
  the unfixed layer, and moved to the scratchpad before anything ran; corrected at once, with no
  effect on any result.
- **log 09 §2 item 20**: four edits were first wrong (a range a line early, a splice and a range
  that repeated a clause, one appendix line left out), each found by the agent's own checks before
  the commit and rebuilt; no effect on any result.
- **log 10 §2 item 11**: the high-end suite overran the tool's 600-second foreground limit and was
  moved to the background; its verdict was taken only after it exited 0.

Two logs record a slip caught before anything depended on it, and class it as no drift: log 03a
§2 (a duplicated `build_store` body, put right before anything ran) and log 04a §2 (a heredoc that
wrote nothing; a replacement that left `_factories` undefined, which the module's first run
showed).

**Every STRUCTURALLY REQUIRED entry that changed what a prompt delivered.** The other 26 corrected
an expectation, a count or a procedure and changed no file the prompt delivered.

| Log, item | What it changed |
|---|---|
| 01 §2 item 1 | `tools/__init__.py` and `tests/__init__.py` are copies of SGK's empty files, compared by the check |
| 01 §2 item 2 | `_timing.py` takes `traceback.print_tb` as well as `time` |
| 02 §2 item 1 | the replicated-only declarations sit on replicated classes of the client, and the contract says so |
| 02 §2 item 2 | `build_schema(sqla.MetaData(), factories)`; three files re-fixtured; a test written for breakage (m) |
| 02 §2 item 10 | the prose issue measured at 104 lines, not 102 |
| 03a §2 item 1 | each module's `REPLICATED` filters out the class with no table |
| 03a §2 item 2 | the prune fixture's Sample is stored validated |
| 03a §2 item 9, 03b §2 item 16, 04a §2 item 25 | `black`'s rewrapping of the ported modules |
| 03b §2 item 1 | `table_counts` transcribed with the instrument |
| 03b §2 item 7 | the miss payloads checked by column name |
| 03b §2 item 8 | `test_object_validate` asks for the Gadget with the run's tag |
| 04a §2 item 1 | U18: `Sample`'s `inventory_spec` loses `validated` |
| 04a §2 items 2, 4 | `NON_IDENTITY`'s 40 entries, and `stop_Tprime`'s nine lines mapped to `Trace.step_count`, as measured |
| 04a §2 item 5 | U19: `traces` added to one drop list of 03a's |
| 04a §2 item 6 | U20: the schema witness from the registry less `register() is None` |
| 04a §2 items 9–12 | `test_foreign_key_check`'s added rows; every full-store Sample anchored; `IDENTITY["Sample"]["members"]` |
| 04a §2 item 16 | `builders` compared with 12 |
| 04b §2 item 5 | `TestTheVersionObject`'s literal |
| 04b §2 item 6 | U22: `WITH_A_TABLE` for two `build_schema` calls |
| 04b §2 item 9 | `import_allowed` without SGK's `RayTools` branch |
| 04b §2 item 11 | §2.4's membership test written as an expression |
| 05 §2 item 2 | the README's line for `shard_key_audit`, which has no `--help` |
| 06 §2 item 2 | the new tests reach the actor as `sp.DatastoreClass` with a stand-in broker |
| 06 §2 item 9 | `factories.py` gains the `require_version_serial` import |
| 07a §2 item 1 | U32's counts in the checklists (CPBH 20 classes over 24 entries, SI 16 over 18), and both routes |
| 08a §2 item 1 | the records' dates, 2026-10-10 |
| 08a §2 items 3, 4, 6 | contract §9.1 supersedes no row for the vectorized get; the constructor test calls `ShardedPool(...)`; no serial is a literal |
| 08b §2 items 1, 3 | test 7 pins the controller with `pin_controller(0)`; test 10 catches its `KeyboardInterrupt` |
| 09 §2 items 1, 3, 4 | the prose guard's module rule takes a whole word; the further lines rewritten; two sentences made true |
| 10 §2 items 1, 2 | `venv/` reinstalled with `uv … --offline`, and its `egg-info` removed |
| 10 §2 items 3, 5, 7, 8 | the addenda cite "log 08a §3", cite the committed line numbers, and supersede two more SGK statements |

---

## 8. Observations not acted on

Every item of every log's "Observations not acted on", **64** in all (01: 5, 02: 7, 03a: 5, 03b: 5,
04a: 6, 04b: 5, 05: 4, 06: 6, 07a: 5, 08a: 4, 08b: 4, 09: 5, 10: 3; counted as the numbered items
of each section). The disposition at `v0.2.1` is decided from the later logs, the board and a read
of `33778b0`, and changes nothing.

| Log, item | Observation | At `v0.2.1` |
|---|---|---|
| 01 §5.1 | no ported test reaches `_assign_shard_keys` | **addressed**: opened by 01's review as `[01-no-ported-test-pins-the-shard-key-assignment]`, closed by 03a |
| 01 §5.2 | the package's prose names SGK's layout; two sentences false | **addressed**: opened as `[01-package-prose-names-sgks-layout]`, closed by 09 |
| 01 §5.3 | the ported tests use SGK's table names | **addressed**: opened as `[01-ported-tests-use-sgk-table-names]`, closed by 02 (U8) |
| 01 §5.4 | two placeholder-free f-strings | **still an observation**: `tests/test_shard_key_audit_copy.py:139`, `tests/test_sharded_store_script.py:95` |
| 01 §5.5 | `test_shard_paths.TestModuleIsStandalone` imports through `PYTHONPATH` | **still an observation** (`tests/test_shard_paths.py:103`, `:113-114`) |
| 02 §5.1 | an unsupplied sharded table raises `KeyError` | **addressed**: `[02-an-unsupplied-sharded-table-raises-keyerror]`, closed by 08a |
| 02 §5.2 | `revalidate` is reached by no test | **addressed**: `[02-no-test-reaches-revalidate]`, closed by 03a |
| 02 §5.3 | `job_name` is read by nothing | **still an observation**: kept at `SQL/ShardedPool.py:138`, read nowhere; contract §1 row 10 says so |
| 02 §5.4 | the `key_id` binding fails no test | **addressed** by 03a's `test_shard_key_assignment` |
| 02 §5.5 | the stand-in pool's prose names SGK | **addressed**: added to the prose issue, closed by 09 |
| 02 §5.6 | CPBH's `replicated_tables` names `LambdaCDM` | **addressed** in CPBH's checklist (`docs/adoption/champbh.md:192`, `:342`); the client's to fix |
| 02 §5.7 | two designed behaviours that look like defects (an unknown `stepping` string ignored; a get answer without `_new_insert`/`_updated` not replicated) | **still observations**, recorded in the contract (§2 `stepping`; §6) |
| 03a §7.1 | the port check's blind spot (order, loops, arguments) | **still an observation**; each review measured control flow separately |
| 03a §7.2 | the prose issue re-measured | **addressed** by 09 |
| 03a §7.3 | breakage (j) reaches `test_prune_at_open` only by chance | **still an observation**; `test_shard_key_assignment` catches (j) every time |
| 03a §7.4 | `interrupted_tolerance_get` keeps a client word inside an identifier | **still so** (`tests/test_reconcile_at_open.py:820`); the guard matches whole identifiers |
| 03a §7.5 | `StandinCluster.open_pool` passes no `serial_batch_sizes` | **still so** (`tests/standin_pool.py:284-308`); `build.open_pool` passes it |
| 03b §7.1 | the prose issue re-measured | **addressed** by 09 |
| 03b §7.2 | breakage (e) breaks far beyond its module | a record of 03b's breakage; nothing to address |
| 03b §7.3 | the full store's serials vary between builds | **still so** (the stand-in draws the controller at random); 08a's tests read serials, as its correction 5 required |
| 03b §7.4 | `factories.py`'s docstring omits the two new leaves; `client/__init__.py` names no class; `NAME_MAP`'s docstring sentence | **still so**: the leaves list at `tests/client/factories.py:8-9` omits `gauge_setting` and `routing_rule`; the other two still hold and are true |
| 03b §7.5 | `test_read_only_pool` keeps unused variables | **still so** (`tests/test_read_only_pool.py:452-453`, `:496`) |
| 04a §7.1 | the `origin` member of `Weave`'s parent set is varied by no test | **addressed**: opened by 04a's review, closed by 04b |
| 04a §7.2 | a class that registers `None` makes the two schema records differ | **still so**: the layer's behaviour, pinned by `TestNoneRegistration`; U20 settled the test |
| 04a §7.3 | the port check cannot see a loop that runs zero times | **still an observation** |
| 04a §7.4 | the prose issue re-measured | **addressed** by 09 |
| 04a §7.5 | §2.4's "and one None" Sample anchor is not in the full store | **still so** (log 04a §2 item 11); `Weave` carries the `None` key parents |
| 04a §7.6 | two of hazard 1's figures differ from the note | a correction of a note; nothing open |
| 04b §7.1 | `test_inventory_declarations`' docstring says "resolve() and the report" | **addressed** by 09: no longer in the docstring at `33778b0` |
| 04b §7.2 | `test_layer_registry`'s prose names SGK's command line and config | **addressed** by 09: no `config/datastore.py`, `config.datastore` or `main.py` in it at `33778b0` |
| 04b §7.3 | `FORBIDDEN_PACKAGES` cannot bite here by itself | **still so**, by design |
| 04b §7.4 | `test_read_inventory_loads_only_what_the_registry_loads` cannot fail on (k) | **still so** |
| 04b §7.5 | two scratch probes are in the scratchpad | not in the repository; nothing to address |
| 05 §7.1 | CI resolves the transitive dependencies afresh | **still so**: the workflow is 05's (`git diff 68db557 33778b0 -- .github` is empty) |
| 05 §7.2 | the wrapped runs printed no `ResourceWarning` | **superseded** by 08b's fix (4 lines remain, §3.1); why the lines vanished was not investigated |
| 05 §7.3 | `shard_key_audit` takes `--help` as a path | **still so** (log 10 §5.3; review of 10, check 3) |
| 05 §7.4 | the editable install exposes `datastorekit.tests` | **still so**, as intended; the smoke script relies on it, and the pin does not carry it (§5.3) |
| 06 §7.1 | `set_version` after `set_lookup_version` moves the lookup serial | **still an observation**; no pool makes that sequence |
| 06 §7.2 | `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]` | **addressed**: closed by 08a |
| 06 §7.3 | five new prose lines name `Datastore.object_get` | **addressed** by 09: the prose guard's module rule takes a whole word, and its test 4 pins that this is not found (log 09 §2 items 1, 6) |
| 06 §7.4 | `datastorekit.egg-info/` in the checkout | **no longer true**: `git status --short --ignored` at 11's dispatch lists none |
| 06 §7.5 | a read-only keyed miss of a sharded class is a `ReadOnlyWrite` | **still so**, as contract §8 says |
| 06 §7.6 | 186 `ResourceWarning` lines at the high end | **addressed** by 08b (4 lines) |
| 07a §7.1 | README §6.2's U32 said "16" for CPBH and SI alike | **addressed** at 07a's review (README §6.2 and the board's U32 row) |
| 07a §7.2 | contract §8 cites `SQL/ShardedPool.py:567-574` | **addressed** by 11 (U34): corrected in place to `:568-575`, `v0.2.0`'s lines, with a dated note |
| 07a §7.3 | contract §3 does not say what U32 found about instances | **still an observation**: the adoption README says it; the contract is unchanged there |
| 07a §7.4 | SI passes one payload list to two vectorized gets | **addressed** by 08a's copy; SI must also convert its bare keys to adopt (08a §6 item 3) |
| 07a §7.5 | client defects found while measuring | **still the clients'**, as facts in their checklists |
| 08a §6.1 | the duplicate row's message misdescribes the case | **still an observation**, pinned by `test_unsupplied_sharded_table`'s test 5 |
| 08a §6.2 | 188 `ResourceWarning` lines over the 469 | **addressed** by 08b |
| 08a §6.3 | CPBH's and SI's bare shard keys are refused before the payload line | **still so**: the clients' to convert (their checklists, item 6; 10's addenda) |
| 08a §6.4 | `docs/adoption/stochasticinstantons.md:255-256` describes the in-place update | **addressed** by 10's addendum (U37) |
| 08b §6.1 | `TestInsertBeforeSetVersion`'s two connections | **still so**: the 4 `ResourceWarning` lines of §3.1 |
| 08b §6.2 | an actor constructor that raises under the stand-in | **still an observation** |
| 08b §6.3 | `ReadOnlyMiss` is among the 107 raised constructors | a correction of the prompt's list; nothing open |
| 08b §6.4 | under Ray, a dead actor's `__exit__` raises `RayActorError`, which `_close_refused_open` ignores | **still unverified**: the smoke run kills no actor (§9.3) |
| 09 §6.1 | no rule of the prose guard matches `logs/` | **still so**, by U40's design |
| 09 §6.2 | `tests/test_store_inventory.py:8` names a client's domain in prose | **still so** |
| 09 §6.3 | `tests/test_shard_key_audit_copy.py` says it does not import `datastorekit.shard_paths` | **still so** (`:13-15`); its purpose holds |
| 09 §6.4 | an empty `.claude/` directory in the checkout | **still so**: untracked, empty, dated 2026-10-09 |
| 09 §6.5 | 09's scratch tools are in its scratchpad | not in the repository; nothing to address |
| 10 §7.1 | SGK's checklist cites SGK's `docs/OPEN_ISSUES.md:685` | **still so**, and right by the checklist's rule |
| 10 §7.2 | some lines of `README.md` and `PROVENANCE.md` run past 100 columns | **still so**; not a defect |
| 10 §7.3 | 10's scratch tools are in its scratchpad | not in the repository; nothing to address |

Tally, by the last column's first words: 22 addressed (by a prompt, a review or a decision), 1
superseded, 1 no longer true, 34 still so or still observations, and 6 records or corrections with
nothing open. Each of the 34 was left as an observation by its log, and no later log or review
opened it as an issue.

---

## 9. Known gaps

### 9.1 The commit-point labels

`datastorekit/tests/test_reconcile_at_open.py` uses commit-point labels as runtime strings, the
keys of its cases and the points of its loops: `"P1-C"` (`:307`, `:375`, `:422`, `:432`, `:493`,
`:521`, `:542`), `"Rn-P3"` (`:327`, `:388`, `:443`, `:512`) and `"C-P3"` (`:422`, `:542`); and `P3-K`
(`:551`), `Rn-P3` (`:629`, `:908`), `P1-C` and `C-P3` (`:524`) in docstrings (`git grep -n -E
'P1-C|C-P3|Rn-P3|P3-K' 33778b0`). **No file of this repository defines them.** They are defined in
SGK's records, read through `git show` at `6f7f291`:
- **the definition**: `prompts/datastore-integrity/logs/01-checked-replicated-write.md`, "## The
  commit points of each replicated path" (`:125`). Its legend (`:127-131`) defines `P` (a commit
  on the primary), `C` (the controlling shard's), `R1`…`Rn` (the replicas') and `K`
  (`_assign_shard_keys`'s commit); its "**After (this commit).**" table (`:147`, the table
  `:149-169`) has the crash points `P1`–`C`, `C`–`P3`, `Rn`–`P3` and `P3`–`K` as rows. The table
  writes them with an en dash, so a search for `Rn-P3` does not find it;
- **where they name the tests**: `prompts/datastore-integrity/logs/02-repair-or-refuse-at-open.md`,
  the table `:242-265`, from each state of log 01's table to the `TestKillAndReopen` test and
  sub-test that exercises it ("P1-C", "C-P3", "Rn-P3"; rows `:245-264`).

`git -C <SGK> grep -l 'Rn-P3' 6f7f291 -- 'prompts/*'` finds three files, log 02 among them (prompt
11 §1.5); the definition is log 01's. The user decided on 2026-10-10 (`98fb497`; the board, the
review of 09) that no issue is opened and that this document records the gap.

### 9.2 The contract's line numbers

Every line number in `docs/client-contract.md` is its section's stated tree's: §1–§7 `8bc60a5`'s,
§8 `v0.2.0`'s, §9.1 08a's, §9.2 08b's. Since those trees, 08a and 08b moved `SQL/ShardedPool.py`'s
lines, and 09 moved the lines of every file it rewrote. By `git diff --stat 8bc60a5 33778b0`, the
only layer files the contract cites that are unchanged are `object.py` and `SQL/ClientPool.py`
(prompt 11 §1.4 named `SQL/ClientPool.py` alone; `object.py`, cited at `docs/client-contract.md:183`
before this prompt's additions, is unchanged too). The contract's head now says so, in a dated line
added by this prompt, and §8 has a dated correction of its one wrong citation (U34). The contract's
§1–§9 were not re-measured at `v0.2.1`, since nothing a client supplies changed (U37's reasoning).

### 9.3 What remains unverified

- **G2–G4.** No client has adopted the package. G2 (SGK, with its rehearsal fingerprint), G3
  (CPBH) and G4 (SI) are each that client's campaign, in its own repository (README §7). After the
  close, a gate is recorded on the board when it holds, in a records commit of its own.
- **A multi-node Ray cluster.** The smoke run is one local instance on one machine (§4). Nothing
  here has run the package on a cluster, on several nodes or with remote workers.
- **Each client's own suites under the package.** No client's tests were run, against any release.
- **The dead-actor path under Ray** (log 08b §6 item 4): `_close_refused_open` ignoring
  `RayActorError` is pinned under the stand-in only.

---

## 10. Reproduction

From a clean checkout of the commit that adds this document, at the repository root, with no Ray
process up and `RAY_ADDRESS` unset. `S` is an empty scratch directory outside the repository;
`SGK` is `/Users/ds283/Documents/Code/SecondaryGWKit`. Every `uv` command but §10.4's first install
is offline.

### 10.1 The suite and the checks (§3.1)

```bash
./venv/bin/python -m unittest discover -s datastorekit/tests -t .
./venv/bin/python docs/extraction/compare_ported_tests.py
./venv/bin/python -m unittest datastorekit.tests.test_layer_is_generic datastorekit.tests.test_prose_names_no_source
./venv/bin/black --check datastorekit docs
git diff 41c77c1 -- datastorekit pyproject.toml

mkdir -p $S/v010 && git archive v0.1.0 | tar -x -C $S/v010
(cd $S/v010 && "$OLDPWD"/venv/bin/python docs/extraction/compare_with_source.py)

mkdir -p $S/hi/tree && git archive HEAD | tar -x -C $S/hi/tree
uv venv --offline -p /opt/local/bin/python3.13 $S/hi/venv
uv pip install --offline --python $S/hi/venv/bin/python ray==2.55.1 sqlalchemy==2.0.46
uv pip install --offline --python $S/hi/venv/bin/python -e $S/hi/tree
(cd $S/hi/tree && $S/hi/venv/bin/python -m unittest discover -s datastorekit/tests -t .)
```

### 10.2 The smoke run (§4)

```bash
for end in lo:3.12:2.43.0:2.0.39 hi:3.13:2.55.1:2.0.46; do
  IFS=: read e py ray sqla <<< "$end"
  mkdir -p $S/smoke-$e/tree && git archive HEAD | tar -x -C $S/smoke-$e/tree
  uv venv --offline -p /opt/local/bin/python$py $S/smoke-$e/venv
  uv pip install --offline --python $S/smoke-$e/venv/bin/python ray==$ray sqlalchemy==$sqla
  uv pip install --offline --python $S/smoke-$e/venv/bin/python -e $S/smoke-$e/tree
  (cd $S/smoke-$e/tree && env -u PYTHONPATH $S/smoke-$e/venv/bin/python docs/extraction/ray_smoke_run.py)
  echo "exit=$?"
done
```

Run the two ends one after the other: the script refuses to start while another instance's Ray
processes are up.

### 10.3 The breakages (§4.4)

Each diff is log 11 §5's, saved to a file; each is applied to its own export, at the high end:

```bash
mkdir -p $S/break-a/tree && git archive HEAD | tar -x -C $S/break-a/tree
(cd $S/break-a/tree && git apply --check $S/a.diff && git apply $S/a.diff && git apply -R --check $S/a.diff)
uv venv --offline -p /opt/local/bin/python3.13 $S/break-a/venv
uv pip install --offline --python $S/break-a/venv/bin/python ray==2.55.1 sqlalchemy==2.0.46
uv pip install --offline --python $S/break-a/venv/bin/python -e $S/break-a/tree
(cd $S/break-a/tree && env -u PYTHONPATH $S/break-a/venv/bin/python docs/extraction/ray_smoke_run.py)
```

and the same with `break-b` and `$S/b.diff`.

### 10.4 The pin (§5)

```bash
mkdir -p $S/wheel10 $S/export-33778b0 $S/outside
git archive 33778b0 | tar -x -C $S/export-33778b0
uv build --offline --wheel --out-dir $S/wheel10 $S/export-33778b0
unzip -p $S/wheel10/datastorekit-0.2.1-py3-none-any.whl datastorekit-0.2.1.dist-info/RECORD \
    | grep '^datastorekit/' | sort > $S/rec-10.txt

uv venv --offline -p /opt/local/bin/python3.13 $S/pin
uv pip install --offline --python $S/pin/bin/python ray==2.55.1 sqlalchemy==2.0.46 setuptools
(cd $S/outside && env -u PYTHONPATH uv pip install --no-cache --no-deps --no-build-isolation \
    --python $S/pin/bin/python "datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.1")
cat $S/pin/lib/python3.13/site-packages/datastorekit-0.2.1.dist-info/direct_url.json
grep '^datastorekit/' $S/pin/lib/python3.13/site-packages/datastorekit-0.2.1.dist-info/RECORD \
    | sort | diff $S/rec-10.txt - && echo "20 lines identical"
(cd $S/outside && env -u PYTHONPATH $S/pin/bin/python -c "
import importlib.metadata as m, datastorekit
print(datastorekit.__file__, m.version('datastorekit'))
import datastorekit.tests")   # the last line raises ModuleNotFoundError

# (c), the wrong pin, offline from this repository
REPO=$(pwd)
uv venv --offline -p /opt/local/bin/python3.13 $S/pin-c
uv pip install --offline --python $S/pin-c/bin/python ray==2.55.1 sqlalchemy==2.0.46 setuptools
(cd $S/outside && env -u PYTHONPATH uv pip install --offline --no-cache --no-deps --no-build-isolation \
    --python $S/pin-c/bin/python "datastorekit @ git+file://$REPO@v0.2.0")
grep '^datastorekit/' $S/pin-c/lib/python3.13/site-packages/datastorekit-0.2.0.dist-info/RECORD \
    | sort | diff $S/rec-10.txt - | grep -c '^>'   # 13
git diff --name-only 240028e 33778b0 -- datastorekit | grep -v '^datastorekit/tests/'
```

### 10.5 The inherited issues and the labels (§6.3, §9.1)

```bash
git show 33778b0:datastorekit/SQL/Datastore.py | sed -n '142,143p;427,469p'
git show 33778b0:datastorekit/SQL/ShardedPool.py | sed -n '234,257p;277p;307p;315,333p;592p;808,820p;2936,2967p'
git show 33778b0:datastorekit/store_inventory.py | sed -n '53,55p'
git grep -n -E 'P1-C|C-P3|Rn-P3|P3-K' 33778b0 -- datastorekit/tests/test_reconcile_at_open.py
git -C $SGK show 6f7f291:Datastore/SQL/ShardedPool.py | sed -n '294p;305p;544p'
git -C $SGK show 6f7f291:prompts/datastore-integrity/logs/01-checked-replicated-write.md | sed -n '125,169p'
git -C $SGK show 6f7f291:prompts/datastore-integrity/logs/02-repair-or-refuse-at-open.md | sed -n '242,265p'
```

---

## 11. Summary for the board

- The campaign delivered `datastorekit` from SGK's layer, with a suite of 486 on a neutral client,
  the client contract, three adoption checklists, and three releases tagged after green CI:
  `v0.1.0` (`68db557`), `v0.2.0` (`240028e`), `v0.2.1` (`33778b0`).
- At `v0.2.1` the suite passes at both ends (486; 0 and 4 `ResourceWarning` lines), the port check
  passes over 20 modules, `black` is clean over 71 files, and the equivalence check at `v0.1.0`
  still exits 0.
- Under real Ray, at both ends, the smoke script's seven steps pass and Ray leaves no process; it
  catches 08a's revert and the read-only pool's missing `set_lookup_version`.
- The pin from GitHub resolves to `33778b0`, and its 20 package files are 10's wheel's.
- One issue is opened: a closed pool holds its actors' names until it is collected (inherited from
  SGK; unassigned). Eight board issues were resolved; the four inherited stay out of scope.
- 207 deviations over 13 logs (72 STRUCTURALLY REQUIRED, 119 IMPLEMENTATION CHOICE, 3 UNINTENDED
  DRIFT, 13 unlabelled), and 64 observations, each with its disposition.
- Gaps: G2–G4; a multi-node cluster; the clients' suites; the commit-point labels, defined in SGK's
  records; the contract's line numbers, now stated in its head.
