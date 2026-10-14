# Orchestrator — prompt 01, the fingerprint moves into the package

Read [`../README.md`](../README.md) first: §0 (with §0.1 and §0.2), §1, §4, §5 (every rule) and
§6.2 (U1–U5). Then read `object-timestamp`'s [`prompt-01.md`](../../object-timestamp/orchestrator/prompt-01.md),
whose "Conventions", additions on installing and on breakages, and §3–§5 this note keeps unless it
says otherwise. **Unlike that note's prompt, this one starts no Ray** (README §5 rule 7, U4): there
is no smoke run, and nothing of the smoke script's rule applies but its check that no Ray process
is up.

**You do not write code.** You may:
- run the suite, the port check, `black --check` and the guards;
- make venvs in the session scratchpad with `uv … --offline`, from the cache the extraction
  campaign filled;
- export the tree with `git archive` into the scratchpad, and run prototypes, the equivalence
  check and breakages there, never in this checkout and never committing one;
- run SGK's extracted functions in scratch, under README §5 rule 5's one exception (U5), and
  nothing else of SGK;
- reach the network only for one `git ls-remote origin` at dispatch and one at the review;
- read the three clients only through `git -C <client> rev-parse|status|show|grep|log|diff`;
- fix small residue in a follow-up commit of your own (§4);
- after the review, and only with the user's approval, push `main` (§5).

**The prompt:** [`01-the-fingerprint-moves-into-the-package.md`](../01-the-fingerprint-moves-into-the-package.md)
**Closes:** nothing on a board · **Carries out:** the user's ruling of 2026-10-12, SGK's D3
(README §0) · **Opens:** only what the work finds · **Model:** Opus, as the prompt recommends (the
same agent moves the code, rewrites its prose under two guards, writes the tests and contract
§9.7, and runs the equivalence check).

**Gate:**
- U1–U6 are taken, and 01 is written and revised for U1 (`6ef38f6`, `04a2ed9`).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- `git diff --stat 2f5417e HEAD -- datastorekit pyproject.toml docs` is empty: the package and its
  documents are `v0.3.0`'s.
- `origin/main` is `5f972be` (`git ls-remote origin`, 2026-10-14), an ancestor of `main`, which is
  ahead of it by `6ef38f6`, `04a2ed9`, `7298262` and this note. The tags are `v0.1.0` (`0ece4aa` →
  `68db557`), `v0.2.0` (`9eaf542` → `240028e`), `v0.2.1` (`0ba2e4d` → `33778b0`), `v0.2.2`
  (`c32d027` → `6d8ee9a`), `v0.2.3` (`8dac562` → `0de2b16`) and `v0.3.0` (`bf0a3b2` → `2f5417e`),
  here and on `origin`, and no other.
- The clients, read while this note was written (2026-10-14):
  - SGK `a5a6f6d` (branch `handover-remedial`), clean, as at planning. `git diff --stat c8a7f14
    a5a6f6d -- RunRegistry` is empty;
  - CPBH `985819c` (branch `read-only-plots`), 23 untracked entries (pilot `.db` files, logs,
    `pilot-out/`, two run scripts, `prompts/jordan-normalization/`); `5bb2be6` at planning;
  - SI `5fb4a1d` (branch `dk-and-rpk-migration`), clean, as at planning.
- No Ray process is up by the smoke script's rule (`pgrep -f
  'gcs_server|raylet|ray::|default_worker\.py'`, shells dropped), and `RAY_ADDRESS` is unset.
- The index is **4** (all four on `inherited-issues`' board), and stays 4 unless the work opens an
  issue.
- One prompt at a time in this checkout.

## 0. What makes this prompt unusual

**The code is a move; the risk is in what must not change.** About 230 lines of SGK's come in
almost verbatim. What changes is small: the format becomes an argument with a type check,
`encoding_format` is added beside the digest, the comparison refuses on either version, and the
listing's first line gains a field at its end. What must not change is every digest, count and
comparison entry SGK's code gives, and the words of the listing's first line that SGK parses. The
equivalence check (§2.4) is the evidence for the first; the golden and tests 4–6 pin it here.

**No Ray, and one exception to the client rule.** Nothing in this prompt starts Ray (README §5
rule 7). The agent runs a scratch extract of SGK's five functions (U5) and nothing else of SGK; it
reads SGK's brief and audit as text, through `git show`.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-14 at `7298262` (whose
`datastorekit/` is `2f5417e`'s), in `venv/`, in offline scratch venvs at both ends, and in a scratch
export with a prototype of §2.1–§2.4. Pass them on. Corrections 1 and 2 change what the agent
writes or how it judges a result, and are STRUCTURALLY REQUIRED. Corrections 3–6 correct what the
prompt states; the log records each as found.

1. **Test 7 must match the refusal's message, and breakage (j) is mispredicted.** With the type
   check removed but the `< 1` check kept, `"1"` and a dict still raise `TypeError`, from Python's
   comparison (`'<' not supported between instances of 'str' and 'int'`), and only `True` and
   `1.0` are hashed. So a test 7 that asserts a bare `assertRaises(TypeError)` passes under (j)
   for the string and the dict, for the wrong reason (measured: 2 subtests fail, not 4). Test 7
   must check that each refusal is the function's own: `assertRaisesRegex(TypeError,
   "fingerprint_format")`, or a match on the function's name, as §2.1 item 4 requires each message
   to name the function, the argument and the value. Then (j) fails all four (`True`, `"1"`, `1.0`,
   the dict), measured. The missing argument's own `TypeError` from Python names
   `fingerprint_format` too. (j)'s prediction, "the dict, the string and the bool are hashed", is
   wrong as written: under (j) the bool and the float are hashed; the string and the dict are
   refused by the comparison, with a message that does not name the function.
2. **Test 2's changes: know the cascades before naming each expected set.** A reference digest
   covers its parent's tags (`store_inventory.py:162`, `reference_digest`), and `Weave` 1's key
   names both Traces of shard 0 (its `trace` is Trace 4; its strands name Trace 3). Measured on the
   neutral full store at `NEUTRAL_FORMAT` 1:

   | Change (`extra_sql`, shard 0 unless said) | Changed entries | Comparison |
   |---|---|---|
   | `Sample` 2 deleted with its `Sample_tags` and `Sample_members` rows | `(Sample, None)`, `(Sample, (fixture-run,))` | one `tag_set`, `(2, 1)` |
   | `Sample` 2's row alone deleted | the same | the `tag_set` entry, and two `problems` entries (`orphan-member`, `orphan-tag`) |
   | a tag (serial 5, `weave-tag`) added to `Sample` 2 | `Sample` and its sets `(fixture-run,)` and `(fixture-run, weave-tag)` | two `tag_set`, `(2, 1)` and `(None, 1)` |
   | a tag added to `Trace` 3, or to `Trace` 4 | **`Trace` and `Weave`** (two tag sets of `Trace`, one of `Weave`) | three `tag_set`, one of them `Weave`'s |
   | `TraceStep` 32 deleted | `(Trace, None)`, `(Trace, (fixture-run, grid-B))` | one `tag_set`, `(1, 1)` |
   | `Trace` 3's `trace_validated` set to 1 | the same | one `tag_set`, `(1, 1)` |
   | `Sample` 4's `sample_validated` set to 1 (shard 1) | **none** | `[]` |
   | an orphan `TraceStep` (serial 9001, `trace_serial` 999) | none | one `problems` entry; `problems` `{"Trace": {"orphan-value": 1}}` |

   So: a tag added to a Trace is not local to one class, and a test that restates SGK's
   `assertLocalised` (every class but one unchanged) fails on it. Either choose a record nothing
   references by tags (`Sample` 2, measured local), or name `Weave`'s entries in the expected set,
   as §2.3 allows ("derived from the fixture's rows"); the log says which. Only `Gadget` and `Trace`
   declare `validated` (`tests/client/factories.py:911`, `:1472`); `Sample`'s flag is not identity
   (`test_store_inventory.py`'s `NON_IDENTITY`), so a test that flips it fails as "changed
   nothing", which is a bug in the test, not a stop. Deleting a record's row alone adds problem
   entries; delete its tag and member rows with it for the content-only case.
3. **The changed stores number 28, not 27.** Deleting the last row of every table that has rows,
   in `full_rows()`'s replicated rows and each shard's: 11 replicated tables, 10 on shard 0, 7 on
   shard 1, **28** stores, every comparison non-empty, **14** with `problems` entries, at formats 1
   and 6 and at both ends. The planner's 27 / 13 is not reproduced by this enumeration. U5 says "at
   least the 27"; §2.4's "27 stores" is a count, not a criterion. The agent enumerates every table
   with rows as above, records its count, and the stop (§6, second) is on a **difference from
   SGK's**, not on the count.
4. **The brief and the audit are not at `c8a7f14`.** The brief was added at SGK `526036c`, and the
   audit changed at `c522c7a`, both after `c8a7f14`. Read both with `git -C
   /Users/ds283/Documents/Code/SecondaryGWKit show a5a6f6d:<path>` (SGK's `HEAD` at dispatch), not
   by opening the working tree. SGK's code and `RunRegistry/tests/test_store_fingerprint.py` are
   unchanged from `c8a7f14` to `a5a6f6d`; read them at `c8a7f14`, as the prompt says.
5. **Breakage (f) is equivalent.** `read_records` builds every `Record`'s tags as
   `tuple(sorted(…))` (`store_inventory.py:765-767`), so (f) changes nothing on any inventory
   `read_inventory` gives: measured, test module `OK` under it. Record it as equivalent, with that
   citation, not as a gap. (The prompt lists (h), (j), (i) in that order; keep its labels.)
6. **Line numbers.** Every line the prompt cites holds at `7298262`, in the package, the tests, the
   documents and SGK at `c8a7f14`, with these readings:
   - `Record` is `:179` (its decorator `:178`); `ClassInventory` `:372` (decorator `:371`);
     `StoreInventory` ends before `_problem` at `:499`;
   - in SGK's `stores.py` at `c8a7f14` (2185 lines): `FINGERPRINT_FORMAT = 6` at `:206`, the
     section comment `:1152-1162`, `_sha256_lines` `:1164`, `listing_lines` `:1376-1399`, and
     `check_listing_path` at `:1402`, so `sed -n 1164,1400p` takes the five functions and the
     three helpers and nothing after. **Its SHA-256 is
     `9b1a8aedb006ffa9c2635038eda2e87cad451106283d022a94f8038cd8eb0108`**;
   - the contract's §9.6 head line is `:40-41`, and the intro paragraph (`:43`) follows it; §9.7
     goes after §9.6, at the file's end (`:367`).

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **Work in this order:**
  1. the baseline: 509 in `venv/`, and at the high end from a fresh venv with an export of `HEAD`
     installed editable; the port check; `black --check datastorekit docs`, 76 files; the
     clients' `HEAD`s and statuses; Ray's processes, by the script's rule; `RAY_ADDRESS`;
  2. §2.1, then the guards and `test_package_imports` alone at the high end;
  3. the equivalence check (§2.4) at both ends, **before** the golden is written, so that the
     golden is written from a module already shown equal to SGK's;
  4. §2.2 and §2.3; the suite at both ends;
  5. the breakages (a)–(j), each in its own export at the high end, on the new module ((a) also
     re-runs §2.4);
  6. §2.5, the records;
  7. `venv/`'s suite again, the port check, `black`, the guards, the clients again, Ray's
     processes again.
- **Install, do not set `PYTHONPATH`, and run from the export's root.** As `object-timestamp`'s
  note: `ray`, `sqlalchemy` and `setuptools` offline into each scratch venv, then `uv pip install
  --offline --no-deps --no-build-isolation -e <export>`. High end `/opt/local/bin/python3.13`,
  `ray==2.55.1`, `sqlalchemy==2.0.46`; low end `/opt/local/bin/python3.12`, `ray==2.43.0`,
  `sqlalchemy==2.0.39`. `venv/` is not reinstalled. Run every scratch-venv command with the export
  as the working directory, under `env -u PYTHONPATH`, and print `datastorekit.__file__` once in
  each venv. The equivalence check at the low end may run in `venv/` against this checkout's tree,
  or in a low-end scratch venv; the log says which.
- **The extract is loaded, not imported as SGK's.** Write it to a scratch file outside this
  repository, prepend the three lines §2.4 names, and load it with `importlib.util` by path
  (`spec_from_file_location`) under a scratch module name. Record both SHA-256s: the 237 extracted
  lines (correction 6) and the file with its prepended lines.
- **The listing's encoding field is read from the fingerprint**, as its other two fields are:
  `fingerprint['encoding_format']`, not the constant. Then a listing is self-consistent with the
  fingerprint it is given.
- **The test module's prose is scanned too.** `test_prose_names_no_source` reads every `.py` under
  `datastorekit/`, the tests included: its rules forbid `RunRegistry` and `store-fingerprint` in a
  comment or docstring, and a path beginning `prompts/` or `docs/` that does not exist here. Name
  the source generically ("the source repository's fingerprint tests"), never by SGK's path,
  package or campaign. SGK's `format` text, written into test 6 as a literal, is a runtime string
  and is not read by either guard.
- **If `_Stores` is imported** from `test_store_inventory`, import that name alone, never a `Test*`
  class, so that nothing is collected twice; and note that its `baseline` is an inventory, not a
  fingerprint. The prototype restated it (SGK's names: `baseline_inventory`, `baseline`).
- **The `ast` comparison of acceptance 1.** For instance: parse the extract and the module; for
  each function name in both, `ast.dump` of the `FunctionDef` with its docstring removed (and, for
  a fair comparison, its `returns` annotation and argument annotations cleared, since §2.1 item 4
  adds them); compare. Expect the five helpers equal; `fingerprint_of` differing by its arguments,
  the type and value checks, the removed lazy import, `fingerprint_format` for `FINGERPRINT_FORMAT`
  (twice) and the added `encoding_format` key; `compare_fingerprints` by the versions block before
  `out = []`; `listing_lines` by the removed import and its first `yield`. The log gives the
  script's essentials and every difference.
- **Neutral names.** Check each new identifier, the test module's constants and any table or tag
  name a test writes against `datastorekit/tests/data/client_vocabulary.json`, by a script that
  loads it (walking each client's `registry`, `columns` and `packages`), and quote the result.

**The facts, checked by the orchestrator.** Pass them on.

- **The prototype**, in an export of `7298262`: `datastorekit/store_fingerprint.py` as §2.1 (SGK's
  bodies; `fingerprint_of(inventory, fingerprint_format: int, taken=None)` with the type and value
  checks before reading; `encoding_format` after `fingerprint_format` in the returned dict;
  `compare_fingerprints` gathering a `format` and an `encoding` entry, in that order, and returning
  them if any; the listing's first line `# fingerprint_format <f> digest <d> encoding_format <e>`;
  `canonical_json` imported at module scope); its docstrings minimal, the bump-rule comment
  elided. The golden written by a script as §2.2. `tests/test_store_fingerprint.py` with 15 tests:
  1 physical, 5 localised (correction 2's first, third, fifth, sixth and last rows), 1 not content,
  3 golden (the golden and a second build; the shape and the recomputed digest; `taken`), 1
  listing, 1 versions, 1 arguments (with `assertRaisesRegex`, correction 1), 2 purity.
- **The golden.** `fingerprint_of(read_inventory(build_full_store(<tmp>).primary, factories),
  fingerprint_format=1)`: digest
  `7656b600965b5911a5046e7c0ebcd4dddce1c8ad277243d211b548487f22d304`, the planner's; the file,
  `json.dumps(…, indent=2, sort_keys=True) + "\n"`, is 193 lines, SHA-256
  `03db714952565e0997cb7be43115a930db6a1b13ac62bc8de10eff35b11a018e`. 13 classes; the tagged
  ones are `Gadget` (2 sets), `Sample` (2), `Trace` (3) and `Weave` (1).
- **The equivalence check**, prototype against the extract, at both ends (3.12.15 / 2.43.0 /
  2.0.39 and 3.13.16 / 2.55.1 / 2.0.46, SQLite 3.53.4): at formats 1 and 6, the baseline equal in
  every field of SGK's, the package's adding `encoding_format` only (format 6 digest
  `bdf09575e8f8930677b4f040b4ba0d298dfc7277da9fb5205a31102d2d619b19`, the planner's); the 28
  changed stores (correction 3) and four of test 2's changes, every fingerprint and every
  comparison equal; the listing 68 lines, all but the first equal to SGK's, the first ending
  ` encoding_format 1`. **0 differences.**
- **The suite.**
  - At `7298262`, `venv/`: `Ran 509 tests … OK`, 0 `ResourceWarning` lines (96 s).
  - With the prototype: `Ran 524 tests … OK` at both ends, installed editable; `ResourceWarning`
    lines 0 low, 4 high (`actor-names` log 01 correction 8: 0 or 4 at the high end is timing).
  - The guards and `test_package_imports` pass with the prototype. Run over SGK's section as it
    stands, the layer guard's comment scan finds `RunRegistry` in the lazy import's comment, and
    the prose guard finds that and `store-fingerprint` in the section comment: two lines, as the
    planner found. No string or name of SGK's section is in the vocabulary (`taken`'s keys
    included), but §2.1 item 4 says to name none of `taken`'s keys anyway.
- **The breakages**, in the prototype's export at the high end, on the new module (15 tests):

  | | Change | Fails |
  |---|---|---|
  | (a) | `"encoding_format"` in `overall` | test 4: the golden, and the recomputed digest; §2.4 differs |
  | (b) | `overall`'s `"fingerprint_format"` renamed `"format"` | test 4: the golden, and the recomputed digest |
  | (c) | the `encoding_format` check skipped | test 6 |
  | (d) | "are not compared" → "are never compared" in the `format` text | test 6 (the literal) |
  | (e) | `encoding_format` before `digest` in the first line | test 5 |
  | (f) | `tuple(sorted(record.tags))` in `_tag_sets` | **none: equivalent** (correction 5) |
  | (g) | `_sha256_lines` as `"\n".join(lines)` | tests 4 (the golden) and 5 |
  | (h) | `fingerprint_format: int = 1` | test 7 (the missing format) |
  | (j) | the type check skipped (`if False:`) | test 7: `True`, `"1"`, `1.0`, the dict, with `assertRaisesRegex`; only `True` and `1.0` with a bare `assertRaises` (correction 1) |
  | (i) | `Counter(problem for …)` (the whole string) | test 2's orphan case |
- **The checks.** `compare_ported_tests.py`: exit 0, "OK: 20 module(s) … 1 test(s) declared not
  ported", at `7298262` and with the prototype. `black --check datastorekit docs`: 76 files at
  `7298262`, 78 with the prototype's two modules.
- **The toolchain.** `venv/`: Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39, SQLite 3.53.4,
  `black` 25.1.0, `datastorekit 0.3.0` editable from this checkout. `uv` 0.12.20.
- **Expected counts.**
  - The suite: **509** before; **509 + n** after, at both ends (n = 15 in the prototype's form).
  - `compare_ported_tests.py`: unchanged.
  - `black --check datastorekit docs`: **76** before, **78** after.
  - The index: **4**, unchanged unless an issue is opened.

**What the review exists to establish.**
- **(E1) Scope.** Only §7's files change; under `datastorekit/`, exactly three new files (the
  module, its test module, the golden), and no other file.
- **(E2) The module.** SGK's code, changed only as §2.1 items 1–8 say; the prose neutral and true;
  the bump rule beside the constant in the same items and order as §9.7.
- **(E3) The equivalence.** §2.4 replayed by the orchestrator from the log's script, on the
  commit's export, at both ends: 0 differences.
- **(E4) The tests.** Each of §2.3's eight, failing under its breakages as correction 1 and the
  table say; (f) recorded as equivalent; the golden's digest the planner's.
- **(E5) The documents.** Contract §9.7 and its head line, additive, each citation true at the
  commit.
- **(E6) Both ends.** 509 + n in `venv/` and at the high end.

**Conventions.** `object-timestamp` prompt 01's note's, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- record each breakage as a diff relative to the repository root, and check it **as recorded in
  the log** with `git apply --check` and `-R --check` against a scratch export;
- read a client only through `git`, and never import or run its code, but for §2.4's extract;
- use a subdirectory of the session scratchpad, never `/tmp`, for venvs, exports and the extract;
  put no scratch `.py` under `datastorekit/` or `docs/`;
- a stop goes to the user, through the orchestrator;
- check `git log` before committing.

And for this prompt:
- **Ray is not started**, by anything.
- **No network.** Every venv and install is `--offline`.
- **No push, no tag, and no change to the GitHub repository's settings.** `pyproject.toml` stays
  at `0.3.0`.

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. Record `git status --short
   --ignored` (at writing: `.idea/`, `venv/` and five `__pycache__/` directories).
2. **The baseline.** In `venv/`, `Ran 509 tests … OK` with no `ResourceWarning`; the port check
   exits 0; `black --check datastorekit docs` leaves 76 files unchanged; `pip show datastorekit`
   says `0.3.0`. (Taken at writing; re-take only if `HEAD` has moved outside `prompts/`.)
3. **The clients.** Each `HEAD` and `git status --short`, recorded. A change there that is not the
   agent's is recorded, not stopped on (`object-timestamp` note, correction 4).
4. **The remote.** `git ls-remote origin`: `main` at `5f972be…` and the six tags as the gate says.
5. **Ray.** Record the Ray processes by the script's rule, and `RAY_ADDRESS` (unset).
6. **The index.** 4, and 4 after unless an issue is opened. Tell the agent.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, this board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `docs/client-contract.md`, `object-timestamp` prompt 01 and its log;
- `HEAD`, the clients' `HEAD`s and statuses, the counts and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's six corrections and its additions. Correction 1 is the
one that would let breakage (j) pass test 7 for a wrong reason; correction 2 the one that would
send it to a false stop on test 2.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/01-the-fingerprint-moves-into-the-package.md`, in
  README §5.1's form.
- **The files it may change are the prompt's §7 list, and nothing else.** It must not touch
  `store_inventory.py` or any other existing file under `datastorekit/`, `pyproject.toml`,
  `README.md`, `PROVENANCE.md`, `docs/adoption/`, `docs/extraction/`,
  `docs/extraction-verification.md`, the workflow, `CLAUDE.md`, `LICENSE`, `.gitignore`, or
  anything under `orchestrator/`.
- **Under `docs/`, no line is removed.**
- **It writes nothing in any client repository, and runs, imports or opens nothing of one**, but
  §2.4's extract, run in scratch.
- **It reaches no network and starts no Ray.**
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §6 conditions, read with corrections 1–3.

## 3. The review — ten checks

Make the review's venvs and exports fresh, offline, in a subdirectory of the scratchpad of their
own, not the agent's, and run from each export's root.

1. **Scope (E1).** `git show --stat <commit>` touches only §7's files. `git diff <parent> <commit>
   -- pyproject.toml README.md PROVENANCE.md docs/adoption docs/extraction
   docs/extraction-verification.md .github` is empty. `git diff --name-status <parent> <commit> --
   datastorekit` is three `A` lines. No venv, egg-info or scratch file; `git status --short
   --ignored` as at dispatch. Each client's `HEAD` and status recorded.
2. **The module, by reading (E2).** The docstring as §2.1 item 1, naming no client, format number
   or history; the imports at module scope and no lazy import; `ENCODING_FORMAT = 1` under the
   bump rule, its eight items in U3's order and matching §9.7's; the signature, its checks before
   any read, and their messages; the returned dict and `overall` exactly; the version entries and
   SGK's `format` text verbatim against the extract; the listing's first line. Re-run the `ast`
   comparison against the extract. In `venv/`: `inspect.signature(fingerprint_of)`'s
   `fingerprint_format` is `POSITIONAL_OR_KEYWORD` with no default.
3. **The equivalence (E3).** Extract the script from the log, re-extract SGK's lines from
   `c8a7f14` and check their SHA-256 against the log's and correction 6's, and run it at both ends
   on the commit's export: 0 differences, the two digests the planner's, the store count the
   log's.
4. **The tests, by reading (E4).** §2.3's eight, each store in a `tempfile` directory, with a
   `tearDownModule` asserting Ray is not initialised; test 2's expected sets stated in the test
   and true of the fixture (correction 2); test 6's literal SGK's text; test 7 matching the
   messages (correction 1); test 8's fresh interpreter; the golden's name built from both
   constants; no `Test*` class imported from another module; the prose neutral.
5. **The suite at both ends (E6).** In `venv/`, `Ran <509 + n> tests … OK`. In a fresh high-end
   venv with `git archive <commit>` installed editable, the same, with the `ResourceWarning` lines
   counted. The port check and the guards pass; `black --check datastorekit docs` leaves 78
   files.
6. **The breakages (E4).** Extract (a)–(j) from the log; check each with `git apply --check` and
   `-R --check` against its own export of the commit, install it, and run the new module. Each
   fails as the log records, and as §0's table predicts up to the agent's form; (f) passes, and is
   recorded as equivalent; (a) also makes the equivalence check differ.
7. **The golden.** Its digest is `7656b600…f22d304`; regenerate it from the log's script on the
   commit's export and compare bytes with the committed file.
8. **The documents (E5).** Contract: the head line after `:40-41`; §9.7 in §9's form, after §9.6,
   its `path:line` citations read at the commit, its "Supersedes" none; its bump rule the same
   eight items as the module's comment; `git diff` of the file `+` lines only. Every relative link
   and anchor added resolves.
9. **The records.** The log in §5.1's form with the equivalence script and output, the golden's
   script, the breakage diffs, the names checked, the clients at the start and the end; this
   board's header and 01's row; the README's header and §2 row; `prompts/INDEX.md`;
   `docs/OPEN_ISSUES.md` at 4, or as an opened issue requires.
10. **Nothing left behind.** No Ray process. `git tag -l` is the six tags, and `origin` is
    unchanged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 01* paragraph, in the form of
  `object-timestamp`'s board. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on the board, in the log, in the contract if it uses the phrase, in
    the README and in `prompts/INDEX.md`;
  - "reviewed" for 01 in this board's header and row, README §2 and `prompts/INDEX.md`;
  - the notes line, with this note marked "used for 01".
- Anything the review finds that is not residue is opened on this board's §3 and in the index.
- **Report to the user:**
  - what landed: `datastorekit/store_fingerprint.py`, `ENCODING_FORMAT` and its rule, the golden,
    the tests, contract §9.7;
  - the equivalence check replayed at both ends, and the golden's digest;
  - the suite at both ends, and the breakages;
  - the index at 4;
  - that 02 (`v0.4.0`) is written next, against the tree 01 leaves;
  - **and ask whether to push `main`** (§5).

## 5. Pushing

As `object-timestamp`'s notes: 01 makes no release and no tag. Its commit and the records after it
are on local `main` only, ahead of `origin/main` (`5f972be`). **Ask the user, and wait for a clear
yes.** With approval, `git push origin main`, a fast-forward. Read the CI run once, when the user
says it has finished, and record its URL and both verdict lines on this board in a records commit
of its own, pushed with approval too. If either end fails, record it in §3 and the index, and tell
the user. Nothing is reverted without the user.

**Hand on.** 02 is written after this review, against the tree 01 leaves: it releases `v0.4.0`
(U6), carries the adoption addenda (SGK's saying what it must do), and its tag is made only after
CI is green on its commit. The tag object, the commit and the SGK addendum's anchor then go to the
user for SGK's gate E1.
