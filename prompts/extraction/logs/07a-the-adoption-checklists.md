# Log 07a — the adoption checklists

**Subject:** Write the adoption checklists and the client import measure · **Commit:**
`dd45243` · **Date:** 2026-10-09 · **Model:** Claude Opus 5.5 · **Result:** landed, no tag, nothing
pushed.

`docs/adoption/` now holds a README of what the three clients share and one checklist per client,
each measured read-only at a named client commit against `v0.2.0` (`240028e`), each under the same
ten items. `docs/extraction/measure_client_imports.py` counts a client's imports of its layer
through `git ls-tree`, `git show` and `ast`, and each checklist carries its Markdown output as an
appendix. No package file changed, no test was added, and nothing was written in any client.

The script gives **SGK 233** import statements (41 nested), **CPBH 41** (0) and **SI 48** (1) at
the checklists' commits, and **CPBH 40** at `9b3db51`; all equal the orchestrator's probe. The
suite is **458** before and after. No issue is opened; the index stays at **8**.

Prompt: [`../07a-the-adoption-checklists.md`](../07a-the-adoption-checklists.md), with the
orchestrator's dispatch note §0: eight corrections, three additions, its measured facts and its
conventions. §2 classifies each.

The run was cut off once by an API usage limit, after the SGK and CPBH checklists were written and
before SI's. It resumed on the coordinator's message, with nothing committed (`HEAD` still
`a816632`), the clients unchanged and no Ray up. Every file written before the cut was re-read on
resuming; both checklists were complete up to their appendix headings.

## 1. What shipped

- **`docs/extraction/measure_client_imports.py`** (new). `measure_client_imports.py <client>
  [--commit SHA] [--json]`, `<client>` one of `sgk`, `cpbh`, `si`. Each client's repository,
  default commit, layer files and factory package are constants (`CLIENTS`). It reads the commit
  through `git rev-parse`, `git show -s` (date and subject), `git ls-tree -r -z` and `git show
  <commit>:<path>`, never the working tree, and parses each tracked `.py` blob outside the layer
  with `ast`. It reports:
  - every `import`/`from … import` statement naming a layer module, at any depth, counted once per
    statement; *nested* means not a direct child of the module's body, and the innermost
    enclosing construct is named (`def f`, `class C`, `if`, `if TYPE_CHECKING`, `try`, `with`,
    `loop`); relative imports are resolved; `from P import X` with `P.X` a layer module counts;
    the package root is a layer module;
  - grouped by top-level directory, with `Datastore/` split into the factory package and its other
    subdirectories; by module with the names imported; and every hit (file:line, nested, module,
    names);
  - string literals naming a dotted layer module exactly or as a prefix (a patch target), the
    longest module winning, the bare `Datastore` excluded, and a path into the factory package
    (other than `base`) treated as a factory's;
  - `import_module`/`__import__` calls with such a literal, apart;
  - imports of factory modules, by count and group;
  - for CPBH, imports of `config.version`'s `VERSION_SERIAL_KEY` and `require_version_serial`;
  - files that do not parse (none, in all three).

  Markdown by default, JSON with `--json`; exit 0, or 2 when the client cannot be read. Standard
  library only. `black`-clean.
- **`docs/adoption/README.md`** (new): the pin and the version table against `pyproject.toml`; the
  module map as the import rewrite; what the wheel does not ship; what a client supplies, by
  contract section, with U32's fact (and the second route's precondition, correction 1) and the
  drop-table fact; how a checklist is used; the index of checklists; the re-measure commands.
- **`docs/adoption/secondarygwkit.md`**, **`champbh.md`**, **`stochasticinstantons.md`** (new):
  §2.6's head, then the ten items under one set of names (§2 item 12), then the script's Markdown
  output verbatim, with its command.
- The records: this log, the board (§1's row, the header, §2's gates), `prompts/INDEX.md`.

## 2. Deviations from the prompt

1. **Correction 1: U32's counts and its second route.** CPBH has **20 classes over 24 entries**
   that define only `register` and `build` (measured by an `ast` probe of the 17 factory modules
   and the registry); SI **16 over 18**. Every hook in both clients takes `self`, none is a
   `staticmethod`, and the quantity factories hold `ObjectType` on the instance. The checklists
   give 20/24 and 16/18, and state beside the "register the class" route that it works only once
   the hooks are callable without an instance; the README says the same. The choice is left to
   each client. README §6.2's U32 "16" is recorded in §7. **STRUCTURALLY REQUIRED.**
2. **Correction 2: breakage (c) reads the working tree for the listing and the contents**, and is
   shown on CPBH at `9b3db51` (§6). **STRUCTURALLY REQUIRED.** How the listing is read is §2
   item 13.
3. **Correction 3: (a) and (b)'s expected changes.** (a) matched exactly (SGK 192, CPBH 41, SI 47).
   (b) gave CPBH −13 and SI −12 as expected, and **SGK −21, not −22** (§6, §8). **STRUCTURALLY
   REQUIRED** (expectations corrected).
4. **Correction 4: the import counts.** Found as the orchestrator says: SGK 233 (the planner's
   groups sum to 232; the missing one is
   `ComputeTargets/tests/test_qcd_cosmology_inventory_record.py:33`); CPBH 41 (with the
   `prompts/run-integrity` probe); SI 48 = 22 + 26 in 25 files; SGK's factory-module imports 98
   outside the factory package, 100 with it, not 75; strings 21 exact for SGK (10 literals and 11
   `import_module` calls), 0 for CPBH and SI. Found as stated.
5. **Correction 5: SGK.** Found as stated: a tracked root `.gitignore` (`var/` only, `:3`; made at
   `2c48e43`, last changed at `0d7c05c`), two more under `docs/`, the six root `.sqlite` files
   ignored; 18 staying modules, 320 `def test_` lines; `test_inventory_retired.py:52`'s
   `HELPER_MODULE` used at `:108`, `:115`, `:134`; six more `docs/` probes failing through
   `lookup_keys/common.py`; the test command `CLAUDE.md:106-111`; the tools equal `v0.2.0`'s up to
   D-tool. Found as stated.
6. **Correction 6: CPBH.** Found as stated: the untracked list includes `pilot-out/` and
   `prompts/jordan-normalization/`; Python from `venv/` only; `ShardedPool.inventory()` to `:999`;
   only `main.py:1350` passes `drop_actions`; `pipeline_selection.py:217-219` is a message and the
   `cp -p` is in `.documents/review-remediation-verification.md:1258`; the read-only order differs;
   `CLAUDE.md` holds no counts; `architecture-summary.md` stale well beyond the tree; the
   `VERSION_LABEL` hazard. One sub-fact differs: of the 20 U32 classes, **three** (not two) also
   define `read_table` (`redshift`, the two quantity factories) (§8). Found otherwise as stated.
7. **Correction 7: SI.** Found as stated: the protected list is wider than the layer; Python
   3.13.13 in `pyvenv.cfg`, 3.13.16 the framework; readers of `.timestamp` outside the layer (three
   direct, two by `getattr`) and ten pass-throughs; `--drop` choices in the argument parser; 12
   classes name the parameter `prune_unvalidated`, only `InflatonTrajectory.py:256` reached; the
   plot scripts open read-write; 57 test functions in 11 files (61 collected); the closeout keeps
   the July `phase_a` stores, at `:69-72`; per-point times only. Found as stated.
8. **Correction 8: the package's references.** `object_get_vectorized` at `:3288-3313`,
   `_refuse_drop_that_leaves_references` at `:730-749` and `:716-728`, the constructor at
   `:95-114`, the keyword calls at `:2185-2187` and `:2220-2221`, `store_reader.py:166-172` and
   `shard_paths.py:51-55` hold. One more, measured here: the read-only pool's `set_lookup_version`
   calls are `ShardedPool.py:568-575` (`:567` is blank), which the checklists cite; contract §8
   says `:567-574` (§7). Found otherwise as stated.
9. **Addition 1: the script first, then the checklists from its output**, in the orchestrator's
   order. **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
10. **Addition 2: the citation check by script** (§5.4). **IMPLEMENTATION CHOICE**, at the
    orchestrator's direction.
11. **Addition 3: versions from text.** Python from each `venv/pyvenv.cfg` and link target (and,
    for SI's framework, MacPorts' `patchlevel.h` and its `software/python313` directory name), Ray
    and SQLAlchemy from `requirements.txt` at the commit, agreeing with `*.dist-info` names. No
    interpreter of a client was run. **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
12. **One set of item names for all three checklists**, README §2's ten (client and versions;
    deletes; imports; what leaves the layer and where it may go; factories; call sites and pool
    construction; tests; stores; acceptance; stale), so that §2.6's "read side by side" holds. The
    prompt's §2.4/§2.5 put "Pool construction" at item 4 and, under item 2, "what is CPBH's and
    must leave first"; in the checklists, pool construction is in item 6 and what must leave is
    item 4, which item 2 points at. Nothing of the prompt's content is dropped. **IMPLEMENTATION
    CHOICE.**
13. **(c) lists files with `git ls-files`**, the files tracked in the working tree, and reads each
    one's bytes from disk, in place of `git ls-tree <commit>` and `git show`. A walk of the working
    tree would have read the clients' ignored `venv/` and stores' directories; `ls-files` reaches
    the same fault (the commit named, the working tree measured) and reads no untracked or ignored
    file. **IMPLEMENTATION CHOICE.**
14. **The script's extras**: the enclosing construct of a nested import, the names imported per
    module, the patch-target strings beside exact names, and CPBH's moved-names section (the prompt
    names `config/version.py`'s two names under CPBH's item 3). **IMPLEMENTATION CHOICE.**
15. **SGK's identity paragraph is measured, not quoted.** A probe applying the map to module paths
    found 15 of the 17 equal to `v0.1.0` byte for byte (the tools up to D-tool as well), and, against
    `v0.2.0`, 11 byte-identical, the two tools differing by D-tool, and the four of 06 differing.
    The prompt's "13 of them equal `v0.2.0`'s files" counts the tools among the 13. The checklist
    gives 11 + 2 + 4. **IMPLEMENTATION CHOICE** (a fact stated precisely).
16. **Facts the prompt did not name, stated in the checklists because they bear on adoption**:
    CPBH's and SI's own `SQLAFactoryBase` is not an ABC (`base.py:16-30`), so their 20 and 16
    classes instantiate today and fail only under the package's; the layer calls `store`,
    `validate` and `validate_on_startup` only on the conditions contract §3 gives; CPBH's
    `main.py:46` imports a factory module as a type hint; SI's three import-time instantiations
    fail at import under the ABC; seven of SI's 16 U32 classes are on its protected list; SI's
    `plot_InstantonSolutions.py:697-702` gives one payload list to two vectorized calls; the
    package reads `_new_insert` or `_updated`, not `_deserialized`; SI's factory commits after
    2026-06-21 changing columns (nine, by `git log`). **IMPLEMENTATION CHOICE.**

No UNINTENDED DRIFT was found.

## 3. The seven hazards (§3)

1. **Read a client only through `git`.** Committed trees through `git show`, `git grep`, `git
   ls-tree`, `git ls-files`, `git log` and `git diff --stat` between commits. Untracked or ignored
   files read as text, by name: CPBH's `full_run_2026.6.0.sh` and `full_run_2026.6.0-refresh.sh`
   (untracked); each client's `venv/pyvenv.cfg` (ignored), with `ls -l` of `venv/bin/python*` and
   `ls` of `site-packages` for `*.dist-info` names. Store files named only: SGK's six root
   `.sqlite` (by `ls *.sqlite`, names only), CPBH's 17 `.db` (from `git status`), SI's by `git
   status --ignored` and `ls` of `out-gci-convergence-campaign/` (names only). **No store or
   database file was opened by any means.** SI's ignored `*_compute_times.csv` were named, not
   read. Breakage (c) read tracked files' bytes from the clients' working trees (§2 item 13).
2. **`HEAD` can move.** At the start and the end (and after the resume): SGK `b510bc9`
   (`handover-remedial`), status empty; CPBH `52142d7` (`main`), the same 23 untracked entries; SI
   `7bb3efd` (`main`), status empty. The start and end listings were saved and compared with
   `cmp`: identical.
3. **POSIX classes in `git grep`.** Every count of imports is the script's (`ast`). One `git grep
   -E '\.timestamp\b'` returned nothing because ERE has no `\b`; it was rerun as
   `'\.timestamp([^a-zA-Z_0-9]|$)'`, which found the three readers.
4. **Advice is marked.** Two "Advice:" paragraphs in SGK's (leave `prompts/` as they are), CPBH's
   (a copy is a backup only, from this campaign's README §7) and SI's (U31's three points); every
   other choice is named as the client's, with what each option touches.
5. **The guard.** Nothing under `datastorekit/` changed; the guard passes in the suite.
6. **Instructions inside a client** were read as data: SGK's freeze and run-registry rules, SI's
   protected list and rules, CPBH's test rules are quoted as facts.
7. **The planner's numbers.** Every difference is in §5.3 and §8.

## 4. The probes

All under `<scratch>` = `/private/tmp/claude-35086/-Users-ds283-Documents-Code-DatastoreKit/642e9316-bb8a-428d-a920-9e865405d8a3/scratchpad/agent07a`,
`probe/`, run with `venv/`'s interpreter and `-I`; none committed:
- `factories.py` and `summarise.py`: each registered class's hooks, decorators, first arguments
  and `register()` keys, and the registry's entries (CPBH, SI);
- `layer_client_imports.py`: the client imports inside CPBH's and SI's layers;
- `rewrite_compare.py`: SGK's 17 files with the map applied, against `v0.1.0` and `v0.2.0`;
- `live_pool.py`: SI's tests reaching `live_pool`;
- `pool_calls.py`: calls on a pool in CPBH and SI;
- `check_citations.py`: §5.4.

## 5. Verification performed

### 5.1 The suite and the checks

| | Before | After |
|---|---|---|
| `./venv/bin/python -m unittest discover -s datastorekit/tests -t .` | `Ran 458 tests in 96.288s` / `OK` | `Ran 458 tests in 177.003s` / `OK` |
| `compare_ported_tests.py` | exit 0; "20 module(s) … 1 test(s) declared not ported" | the same |
| `black --check docs` | 3 files unchanged | 4 files unchanged |
| `black --check datastorekit docs` | 65 unchanged | 66 unchanged |

Run in the foreground, each into a scratch file, the verdict grepped. No `compare_with_source.py`
output (U27). No Ray process was up at the start or the end (`pgrep -fl 'raylet|gcs_server'`).

### 5.2 The script (§4.2)

- **Twice per client at the default commit**, Markdown and JSON: byte-identical (`cmp`). SHA-256
  prefixes: SGK `9b4af0f8f00d514c` (md) / `2e31de3203878720` (json); CPBH `b71bc5ecac87403a` /
  `e8d7cd8e84a60944`; SI `0bff52454b8c522b` / `90b009ed99e05a2e`. (Taken before the docstring's
  last edit, which changes no output: the final Markdown runs equal the first byte for byte.)
- **`--commit HEAD~1`**: the output names `99456d82…` (SGK), `9b3db516…` (CPBH), `00d254ee…` (SI),
  with 233, **40** and 48 statements. Only CPBH's moves, since only its `HEAD` adds a layer import
  (`Datastore/tests/test_shard_key_assignment.py:40`).
- `--commit nonexistent` exits **2** with git's message.
- `black --check` clean.

### 5.3 The cross-check (§4.3)

**SGK** (`b510bc9`)

| Group | Planner | Orchestrator | Script |
|---|---|---|---|
| factories | 43 | 43 (23 nested) | 43 (23 nested) |
| `Datastore/tests` | 68 | 68 (4) | 68 (4) |
| `RunRegistry/` | 14 | 14 (6) | 14 (6) |
| `RayTools/RayWorkPool.py:8` | 1 | 1 | 1 |
| `config/model_list.py:4` | 1 | 1 | 1 |
| top-level scripts | 16 | 16 | 16 |
| `DatastoreObject` (root) | 19 | 19 | 19 |
| `ComputeTargets/tests/test_qcd_cosmology_inventory_record.py:33` | — | 1 | 1 |
| `tools/inventory_report.py` | 2 | 2 (1) | 2 (1) |
| `docs/` | 17 | 17 (4) | 17 (4) |
| `prompts/` | 51 | 51 (3) | 51 (3) |
| **total** | 233 (groups sum 232) | 233 (41) | **233 (41)** |
| factory-module imports | 75 | 98 outside / 100 | 98 outside / 100 |
| strings naming a layer module exactly | — | 21 | 21 (10 literals + 11 `import_module`), and 3 patch-target prefixes |

**CPBH** (`52142d7`)

| Group | Planner | Orchestrator | Script |
|---|---|---|---|
| factories (`SQLAFactoryBase`) | 17 | 17 | 17 |
| `DatastoreObject` | 13 | 13 | 13 |
| `ShardedPool` outside tests | 5 | 5 | 5 |
| `ProfileAgent` | 3 | 3 | 3 |
| `Datastore/tests` | 2 | 2 | 2 |
| `prompts/…/datastore_version_probe.py:18` | — | 1 | 1 |
| **total** | 40 (sum) | 41 | **41** (0 nested) |
| at `9b3db51` | — | 40 | **40** |
| moved names (`config.version`) | 3 users | — | 4 imports outside the layer (3 factories, `test_version_keyed_lookups.py:350`), and the layer's own `Datastore.py:85` |
| U32 | 16 classes / 24 entries | 20 / 24 | 20 / 24 |

**SI** (`7bb3efd`)

| Group | Planner | Orchestrator | Script |
|---|---|---|---|
| factories | one each | 22 | 22 |
| outside the factories | 28 in 25 files | 26 in 25 | **26 in 25** |
| nested | — | 1 (`TYPE_CHECKING`) | 1 (`InflationConcepts/DiffusionModel/registry.py:5`) |
| **total** | — | 48 | **48** |
| `DatastoreObject` | — | 18 (12 root, 6 `Datastore.object`) | 18 (12, 6) |
| `tests/conftest.py:25` only test import | yes | — | yes |
| U32 | 16 / 18 | 16 / 18 | 16 / 18 |

The other counts the checklists use, each re-measured: SGK 18 staying modules / 320, 8 moved / 88,
18 ported test modules / 304; CPBH 9 files / 2,686 lines, 27 instances, 7 bare-key gets, 4
`pool.inventory` sites, 3 pool constructions, 6 `inventory()` hooks; SI 9 files / 2,679 lines, 30
instances, 15 bare-key gets, 4 stubs, 14 `timestamp=` calls and 10 pass-throughs, 17 `inventory()`
hooks, 12 `prune_unvalidated` hooks, 57 / 61 `live_pool` tests, 4 pool constructions.

### 5.4 The citations (§4.4)

More than 60 per checklist, so checked by `probe/check_citations.py`: it takes every backticked
`path:line` or `path:a-b` outside the appendix (a bare `:N` resolved against the last path), reads
the line(s) at the client commit (`datastorekit/` paths at `240028e`; CPBH's two untracked run
scripts from disk, as text), and prints the first and last line of each; table-relative factory
paths retry under `Datastore/SQL/ObjectFactories/`. Every printed line was read against its claim.

| Document | Citations | Resolve | Do not |
|---|---|---|---|
| `docs/adoption/secondarygwkit.md` | 122 | 122 | 0 |
| `docs/adoption/champbh.md` | 177 | 177 | 0 |
| `docs/adoption/stochasticinstantons.md` | 201 | 201 | 0 |
| `docs/adoption/README.md` | 11 | 11 | 0 (its CPBH and SI `requirements.txt` lines are checked in their checklists) |

The first runs found 8 abbreviated paths (SGK), and five lines one off or in the wrong file
(`contract.py` lines taken from a concatenated listing; `ShardedPool.py:257` a comment, the call
`:258`; `:340` blank; `:567` blank; a `:256` resolving against the wrong file in SI's). Each was
corrected before the final runs above.

### 5.5 Nothing written outside this repository (§4.5)

`git status --short` in each client at the end equals the start (`cmp`; §3 hazard 2). No `git`
command that writes was run in a client.

### 5.6 The tree

`git status --short` before staging: `?? docs/adoption/`, `?? docs/extraction/measure_client_imports.py`,
and the edited board and index. The ignored entries are dispatch's: `.claude/`, `.idea/`, five
`__pycache__/` directories and `venv/`.

## 6. The deliberate-breakage record (§4.6)

Each diff applied to a scratch copy of the script under `<scratch>/breaks/<x>/docs/extraction/`,
run from the repository root with `venv/`'s interpreter and `-I`; never committed.

**(a) Nested imports skipped (module level only).**

```diff
--- a/docs/extraction/measure_client_imports.py
+++ b/docs/extraction/measure_client_imports.py
@@ -286,7 +286,7 @@
         string_skip = set()
 
         def visit(node: ast.AST, stack: List[ast.AST]) -> None:
-            if isinstance(node, (ast.Import, ast.ImportFrom)):
+            if isinstance(node, (ast.Import, ast.ImportFrom)) and not stack:
                 self.classify_import(path, group, node, context_of(stack))
             elif isinstance(node, ast.Call) and node.args:
                 func = node.func
```

SGK 233 → **192** (132 files; nested 0), CPBH 41 → **41**, SI 48 → **47**. As expected.

**(b) The package root not counted.**

```diff
--- a/docs/extraction/measure_client_imports.py
+++ b/docs/extraction/measure_client_imports.py
@@ -199,7 +199,7 @@
         self.repository = spec["repository"]
         self.given = commit if commit is not None else spec["commit"]
         self.layer_files = tuple(spec["layer"])
-        self.layer_modules = {module_of(p) for p in self.layer_files}
+        self.layer_modules = {module_of(p) for p in self.layer_files} - {"Datastore"}
         # longest first, so that a literal is matched to the most specific module it names
         self.dotted_layer = sorted(
             (m for m in self.layer_modules if "." in m), key=lambda m: (-len(m), m)
```

SGK 233 → **212** (−21: `ComputeTargets/` 11 → 1, `CosmologyConcepts/` 2 → 0, `CosmologyModels/`
1 → 0, `MetadataConcepts/` 5 → 0, `Quadrature/` 1 → 0, `prompts/` 51 → 49); CPBH 41 → **28** (−13);
SI 48 → **36** (−12; the six `from Datastore.object` stay). The `DatastoreObject` groups vanish, as
expected. SGK falls by 21, not the orchestrator's 22: `Datastore/tests/test_layer_is_generic.py:49`
(`from Datastore import contract`) still names the layer module `Datastore.contract`, so it stays
counted under this diff (§8).

**(c) The working tree read in place of `git ls-tree` and `git show`.**

```diff
--- a/docs/extraction/measure_client_imports.py
+++ b/docs/extraction/measure_client_imports.py
@@ -228,15 +228,11 @@
             .decode("utf-8", "replace")
             .strip()
         )
-        listing = git(self.repository, "ls-tree", "-r", "-z", self.full)
-        self.python_files = []
-        for entry in listing.split(b"\x00"):
-            if not entry:
-                continue
-            meta, path = entry.split(b"\t", 1)
-            mode, kind, _ = meta.split(b" ")
+        listing = git(self.repository, "ls-files", "-z")
+        self.python_files = []
+        for path in listing.split(b"\x00"):
             path = path.decode("utf-8", "replace")
-            if kind == b"blob" and mode != b"120000" and path.endswith(".py"):
+            if path.endswith(".py"):
                 self.python_files.append(path)
         self.python_files.sort()
         tracked = set(self.python_files)
@@ -246,7 +242,7 @@
             module_of(p) for p in self.python_files if p.startswith(self.factory_dir)
         } - self.layer_modules
         for path in self.read_files:
-            source = git(self.repository, "show", f"{self.full}:{path}")
+            source = (CODE_DIR / self.repository / path).read_bytes()
             try:
                 tree = ast.parse(source, filename=path)
             except (SyntaxError, ValueError):
```

Run on CPBH with `--commit 9b3db51` (and `--commit HEAD~1`, the same commit): the output's head
still names `9b3db516f3cc…`, but it counts **41** statements in 38 files, against the correct
script's **40** in 37: `Datastore/tests/` 2, `ShardedPool` 6, and the row
`Datastore/tests/test_shard_key_assignment.py:40`, a file tracked only at `52142d7`. "Files read"
is 196 against 195. On SGK and SI at `HEAD~1` it gives 233 and 48, equal to the correct script's,
since their `HEAD~1..HEAD` touch no `.py` file (correction 2).

The three diffs, as recorded here, apply with `git apply --check` and reverse with `git apply -R
--check` against fresh scratch copies of the committed script (§6.1).

### 6.1 The diffs, replayed from this log

Extracted from this file's three fenced `diff` blocks into `<scratch>/replay/`, each checked
against a fresh scratch copy of `docs/extraction/measure_client_imports.py`: each is
byte-identical to the diff applied in §6; each passed `git apply --check`, was applied, passed `git
apply -R --check`, and was reversed, leaving the copy equal to the committed script (`cmp`).

## 7. Observations not acted on

1. **README §6.2's U32 says "16 factory classes" for CPBH and SI alike**, and the board's U32 row
   inherits it; CPBH has 20 classes over 24 entries (correction 1). The campaign README and board
   decision rows are not 07a's to edit (§7).
2. **`docs/client-contract.md` §8 cites `SQL/ShardedPool.py:567-574`** for the read-only pool's
   `set_lookup_version` calls; at `v0.2.0` the code is `:568-575` (`:567` is blank). One line wide;
   left for the orchestrator's residue or 07b, as `client-contract.md` is outside §7's list.
3. **Contract §3 says a factory "is never instantiated", which is true of the layer**, but does not
   say what U32 found: a client that registers instances meets the ABC at its own instantiation.
   The adoption README says it; whether the contract should is a later prompt's.
4. **SI's `plot_InstantonSolutions.py:697-702` passes one `payload_data` list to two
   `object_get_vectorized` calls**, so under the package the second call sees the key the first
   added, the same value. A concrete case for
   `[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]`'s impact; not re-measured.
5. Client defects found while measuring are facts in their checklists, not issues here: SGK's
   twelve broken `docs/` probes; CPBH's `main.py:46` factory-module type hint; SI's unused
   `base._timestamp_column`, its two version labels, and its `prune_unvalidated` name.

## 8. Issues

**Opened, closed, narrowed, changed: none.** The index stays at **8**.

Every difference from the planner's numbers: SGK's groups sum to 232 of 233 (one
`ComputeTargets/tests` import left out); SGK's factory-module imports 98/100, not 75; SGK's
"13 equal `v0.2.0`" is 11 plus the two tools; SGK's staying modules 18, not 19; CPBH's U32 20
classes, not 16; CPBH's `ShardedPool.inventory()` runs to `:999`; CPBH's `drop_actions` only at
`main.py:1350`; CPBH's `pipeline_selection.py:218` a message, not the `cp -p`; SI's 28 statements
outside the factories are 26 (two are factory-module imports); "nothing outside the layer reads
`.timestamp`" is false (five sites); SI's closeout lines `:69-72`, keeping the July stores.
Differences from the orchestrator's: CPBH's U32 classes with `read_table`, three not two; (b) on
SGK −21 not −22 (a definition: the orchestrator's probe dropped any statement naming the root;
the recorded diff removes the root module only, so `from Datastore import contract` still names
`Datastore.contract`); the `set_lookup_version` lines `:568-575`.

## 9. State handed to the next prompt

- `HEAD` is `dd45243`. Nothing pushed; no tag (`v0.1.0`, `v0.2.0` only). The suite is 458.
- `docs/adoption/` and `docs/extraction/measure_client_imports.py` are what 07b's verification
  document cites. The script re-measures any client commit.
- The clients are unchanged: SGK `b510bc9`, CPBH `52142d7` (23 untracked), SI `7bb3efd`.
- G2–G4 are open; each gate row on the board points at its checklist.
- Scratch (not in the repository): `<scratch>/probe/`, `<scratch>/out/` (every run's output,
  the start and end client statuses, the citation listings), `<scratch>/breaks/` (the three copies
  and diffs), `<scratch>/replay/`.
