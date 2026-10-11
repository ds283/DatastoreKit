# Log 02 — release `v0.2.3`

**Subject:** Make the package ready to be released as v0.2.3 · **Commit:** this commit ·
**Date:** 2026-10-11 · **Model:** Claude Opus 5.5 · **Result:** landed; unpushed and untagged; not
yet reviewed.

The package is ready to be released as **`v0.2.3`** (U5). `pyproject.toml` says `0.2.3`, and
nothing else in it changed. `README.md` has a `v0.2.3` status paragraph, the `v0.2.3` pin with the
pins by client (CPBH and SI adopt `v0.2.3`; SGK may stay on `v0.2.2` or move), and its two "Using
it" items brought up to the base's two abstract and six defaulted hooks. `PROVENANCE.md` has a
section for `factory-defaults` prompt 01. Each of the four files under `docs/adoption/` has an
italic line at its head and a dated section, "Addendum: v0.2.3 (factory-defaults prompt 02,
2026-10-11)", giving the pins, what changed for that client since `v0.2.2`, a table of every
statement it supersedes by `path:line`, and how to read the earlier addenda's citations (N and
k + N, correction 3). `git diff` of the four files has no `-` line. The extraction board's G2–G4
read `v0.2.2` or later (G2) and `v0.2.3` (G3, G4), each with a dated line saying the tag waits for
CI.

**No line of code changed.** Nothing under `datastorekit/` is touched. The suite stays at **504**:
in `venv/` before and after (`pip show datastorekit` gives `0.2.3` after the offline reinstall), 0
`ResourceWarning` lines, and at the high end before and after, 4 lines each (timing). A wheel built
offline from an export of the tree is `datastorekit-0.2.3-py3-none-any.whl`, 25 entries, none under
`datastorekit/tests/`. Against `v0.2.2`'s wheel, of the 20 `RECORD` lines under `datastorekit/`
only `SQL/factory_base.py`'s differs. Installed at the high pins and run from outside the
repository, it behaves as the prompt's §1.2 says, with correction 2's probe: a subclass defining
only `register` and `build` instantiates, and its instance's `store`, `validate` and
`validate_on_startup`, each called with its arity, raise `NotImplementedError` with `args == ()`.
Breakage (a) fails the release check on `0.2.2`, (b) on the test package, and (c), `v0.2.2`'s tree
at `0.2.3`, on a `RECORD` with no line changed, on five abstract methods, and on `TypeError` at
`F()`. §1.1's measure of the clients, re-run, reproduces at every commit; SGK's `HEAD`, which moved
during the work, instantiates no factory.

**No tag was made and nothing was pushed.** Nothing was downloaded: every venv, install and build
is `uv … --offline`. No client was written, run, imported or opened. Ray was never started. No
issue was opened, and the index stays at **4**.

Prompt: [`../02-release-v0.2.3.md`](../02-release-v0.2.3.md), with the orchestrator's dispatch note
§0: four corrections, its additions, its checked facts and its conventions. §2 classifies each.
Line numbers under `datastorekit/` are `v0.2.3`'s tree (`f5d8957`'s `datastorekit/`, which this
commit does not change) unless another tree is named.

`<scratch>` below is `<session scratchpad>/agent02`, outside the repository.

---

## 1. What shipped

### 1.1 `pyproject.toml` (§2.1)

`version = "0.2.2"` → `version = "0.2.3"` (`:7`), the only change. No other file carries the
version.

### 1.2 `README.md` (§2.2)

- **Status.** A new paragraph for **`v0.2.3`** (`:10-19`), above `v0.2.2`'s: a release with one
  change, `factory-defaults` prompt 01, on the user's ruling; `SQLAFactoryBase` keeps `register`
  and `build` abstract and defaults `store`, `validate` and `validate_on_startup`, so a factory
  class that defines the two can be instantiated and its instance registered; a registered
  instance meets, for a hook its class does not define, what a class meets (the base's
  `NotImplementedError`, when the layer calls the hook); a class lacking `register` or `build` is
  still refused, and a client that registers classes meets nothing new; no API, nothing written,
  and no message, refusal or exception of the layer's changes. It links
  `docs/client-contract.md#95-factory-defaults-prompt-01`.
- **Installing.** The pin is `@v0.2.3` (`:83`). The sentence at `:75-76` is replaced by `:86-89`:
  `v0.2.2`, `v0.2.1`, `v0.2.0` and `v0.1.0` remain tagged and no tag is moved or deleted; ChamPBH
  and StochasticInstantons adopt `v0.2.3`, with which their registries of factory instances work
  as they stand; SecondaryGWKit, which registers factory classes, may stay on `v0.2.2` or move, in
  a commit of its own, as it chooses. Clients are named, no client path. Written as of the tag.
- **Using it.** "Each factory's hooks" (`:107-111`): `register` and `build`, the base's two
  abstract hooks, and the six it defaults, with §3's anchor; and that a registry may map a name to
  a factory class or to an instance of one, with §9.5's. "What changed after `v0.2.0`"
  (`:121-124`): `v0.2.3`'s change added, still linking §9.
- Nothing else changed.

### 1.3 `PROVENANCE.md` (§2.3)

A new `###` section, "`factory-defaults` prompt 01: the base defaults three hooks (`v0.2.3`)"
(`:205`), after the `actor-names` section, under "After `v0.1.0`". Nothing above it changed. It
says:
- **the change has no source, and is a departure from it**: SGK's base at `6f7f291` (the file
  map's source of `datastorekit/SQL/factory_base.py`) makes all five hooks
  `@staticmethod @abstractmethod`, and the package carried that over; `factory-defaults` prompt 01
  (`f5d8957`), carrying out U1 on the user's ruling (2026-10-11), defaults three; it revisits
  extraction U32 in part; it fixes no defect of SGK's, which registers classes; what it removes is
  Python's `TypeError` on instantiating a class lacking any of the three; its test module, and
  contract §9.5;
- **what changed in the package**: `datastorekit/SQL/factory_base.py` only (24/6), as the prompt
  says; outside the wheel, `test_neutral_client.py`, the new `tests/client/instances.py` and test
  module, smoke step I, contract §9.5 and its five markers, verification §4.8 and §8.1, the note
  on U32; the suite 494 → 504;
- **the files 01 changes, and its log** (from `git show --stat f5d8957`, records excluded).

It does not describe SGK's adoption (G2 is the extraction board's).

### 1.4 The addenda (§2.4, U5)

Each file gains an italic line at its head, after `actor-names` prompt 02's, and an unnumbered
section `## Addendum: v0.2.3 (factory-defaults prompt 02, 2026-10-11)`, anchor
`#addendum-v023-factory-defaults-prompt-02-2026-10-11`:
- in the README the italic line is `:17-20`, then a blank, and the section is at the end, after a
  `---` (heading `:372`);
- in each checklist the italic line is five lines and a blank, after the `v0.2.2` italic line's
  blank (SGK `:27-31`, CPBH `:28-32`, SI `:26-30`). The section follows the `v0.2.2` addendum's
  table, with a `---` of its own above it, and comes before the `---` that precedes the appendix
  (headings SGK `:543`, CPBH `:532`, SI `:501`).

Each section gives:
- the pins by client (U5): CPBH and SI `…@v0.2.3`; SGK `…@v0.2.2` or `…@v0.2.3`, as SGK chooses, a
  move being a commit of its own; that this amends extraction U37 and `actor-names` U3 for SGK
  only; and how G2, G3 or G4 now read;
- what changed for that client since `v0.2.2`, with contract §9.5 linked by anchor (the README
  addendum's table names its three rows, and two unchanged behaviours);
- §1.1's measure, as re-run (§5.4): in the README as one table, in each checklist for that client;
- the rule for line citations: 07a's `datastorekit/` lines are `v0.2.0`'s, the `v0.2.1`
  addendum's `v0.2.1`'s, the `v0.2.2` addendum's `v0.2.2`'s, and this addendum's `v0.2.3`'s
  (`f5d8957`'s `datastorekit/`);
- a supersession table, with the sentence correction 3 asks for above it:

| File | Lines added | Lines removed | Inserted after (at `6d8ee9a`) | N | k | k + N |
|---|---|---|---|---|---|---|
| `docs/adoption/README.md` | 107 | 0 | `:16` | **5** | 5 | **10** |
| `docs/adoption/secondarygwkit.md` | 92 | 0 | `:26` | **6** | 6 | **12** |
| `docs/adoption/champbh.md` | 90 | 0 | `:27` | **6** | 6 | **12** |
| `docs/adoption/stochasticinstantons.md` | 86 | 0 | `:25` | **6** | 6 | **12** |

So: the `v0.2.2` addendum's citations are read at `6d8ee9a`, or N lines later here, except those
above the insert (the `v0.2.1` italic line it cites: README `:7-10`, SGK `:16-19`, CPBH `:17-20`,
SI `:15-18`); the `v0.2.1` addendum's are read at `33778b0`, or k + N lines later here, except
README `:3`, SGK and CPBH `:6`, SI `:5`. Each addendum states both numbers.

The four tables are repeated in §4.

### 1.5 The extraction board's gates (§2.5)

`prompts/extraction/IMPLEMENTATION_STATE.md` §2, rows G2–G4 (`:1537-1539`), and nothing else on
that board (`git diff --numstat`: 3/3):
- titles, exactly: G2 "SGK adopted `v0.2.2` or later (U37; `actor-names` U3; `factory-defaults`
  U5), fingerprint reproduced"; G3 "CPBH adopted `v0.2.3` (U37; `actor-names` U3;
  `factory-defaults` U5)"; G4 "SI adopted `v0.2.3` (U37; `actor-names` U3; `factory-defaults` U5)";
- each status cell gains, at its end, one dated italic sentence: "*(2026-10-11: `v0.2.3` is ready
  to be tagged on `factory-defaults` prompt 02's commit once CI passes there at both ends, as U23
  and U28; 02 makes no tag and pushes nothing. <Client>'s addendum is [link to its `v0.2.3`
  anchor].)*"; G2's says too that "SGK may stay on `v0.2.2` or move to `v0.2.3`, as it chooses
  (`factory-defaults` U5)". `git diff --word-diff` shows only the title words and the appended
  sentence. The board's header is unchanged.

### 1.6 The records

- This log.
- This board: the header, and §1's row for 02 (landed, "this commit", log).
- This campaign's README: a sentence in its header, and §2's row for 02.
- `prompts/INDEX.md`: `factory-defaults`'s status.
- `docs/OPEN_ISSUES.md` is unchanged at **4**: no issue opened.

---

## 2. Deviations from the prompt

1. **Correction 1: `venv/`'s reinstall is `uv pip install --offline --no-deps --python
   venv/bin/python -e .`**, from the repository root, not hazard 6's command with
   `--no-build-isolation` (`venv/` has no `setuptools`: `import setuptools` raised
   `ModuleNotFoundError` there at the start). Its output: `- datastorekit==0.2.2`,
   `+ datastorekit==0.2.3`, exit 0. `pip show datastorekit` gives `Version: 0.2.3`, editable from
   this checkout. It wrote `datastorekit.egg-info/` at the root, which I deleted at once;
   afterwards `importlib.metadata.version("datastorekit")` is `0.2.3`, the package imports from the
   source tree, and `git status --short --ignored` lists only dispatch's ignored entries.
   **STRUCTURALLY REQUIRED.**
2. **Correction 2: the release probe calls each of the three hooks on the instance with its
   arity** (`store` six arguments, `validate` four, `validate_on_startup` three, each `None`), and
   checks a `NotImplementedError` whose `args` is `()`. Each does (§5.3). Under (c) the probe fails
   earlier, at `F()`, with `TypeError: Can't instantiate abstract class F without an implementation
   for abstract methods 'store', 'validate', 'validate_on_startup'` (§6). **STRUCTURALLY
   REQUIRED.**
3. **Correction 3: N and k + N are stated in each addendum**, as numbers (§1.4): N = 5 in the
   README and 6 in each checklist, k + N = 10 and 12. I checked the shifts line by line with
   `<scratch>/probe/check_shift.py`: every line of every own-file citation in the `v0.2.1` addenda
   (read at `33778b0`) and in the `v0.2.2` addenda (read at `6d8ee9a`) equals this tree's line k + N
   or N later, or the same line where it is above the insert: **106 lines checked, 0 differ**
   (§5.7). Recorded as found. **STRUCTURALLY REQUIRED.**
4. **Correction 4: the grep finds more than the prompt names, and each stays true.** Recorded in
   §4's "Considered and not superseded", with the hits at this tree's lines. Recorded as found.
5. **Statements superseded that the prompt's table does not name**, by §2.4's rule. Each is in its
   file's table (§4), marked there. **STRUCTURALLY REQUIRED.**
   - In each file, the `v0.2.2` addendum's "Each `path:line` is this file's as committed with this
     addendum" (README `:351-355`, SGK `:523-527`, CPBH `:515-519`, SI `:484-488`): no longer true
     once the head line moves its lines.
   - In each file, the `v0.2.2` addendum's table cells that restate the pin, "every client adopts"
     or the gate at `v0.2.2` (README `:360`, `:361`, `:364`-`:366`; SGK `:532`, `:533`, `:536`;
     CPBH `:524`, `:525`, `:527`; SI `:493`, `:494`, `:496`).
   - In SGK's: the `v0.2.1` addendum's "with its docstrings blanked it parses to the same code"
     (`:404-406`), false at `v0.2.3` by the three decorators (checked with `ast`, item 8); its table
     row for `:187-188` (`:445`); and the `v0.2.2` table's rows for `:440` and `:442` (`:537`,
     `:538`), which name `v0.2.2` as the extent of their reasoning.
   - In CPBH's and SI's: the "two routes" sentences (CPBH `:216-227`, SI `:198-206` within the U32
     paragraph), which the prompt's table names as part of the U32 paragraph; I cite them by their
     own lines, and say which part of each paragraph still holds.
6. **The orchestrator's additions** are followed as given, each an **IMPLEMENTATION CHOICE** at the
   orchestrator's direction:
   - the order of work (baseline; `pyproject.toml`, the reinstall and the suite; the two documents;
     the addenda and hazard 1's diff; the gates; the release check and the high end; (a)–(c); the
     documents' and link checks; the end);
   - each addendum's supersessions as a table, repeated in §4;
   - placement: the `---` rules, the README's addendum at the end, the heading and its anchor;
   - `PROVENANCE.md`'s new section as a `###`;
   - the contract anchor `#95-factory-defaults-prompt-01`, and §3's `#3-the-factory-hooks`;
   - the gate titles exactly as given, one dated italic sentence per row, G2's naming U5;
   - the name-and-link check as a scratch script, never committed;
   - (a), (b) and (c) each built from its own export;
   - §1.1's measure by a script of my own (`<scratch>/probe/measure_factories.py`), `ast` reads of
     `git show`, run with `python3.13 -I`.
7. **The exports are of the working tree before the records were written**, made with `git archive
   $(git stash create)`: commit object `d352567`, whose tree equalled the working tree then (`git
   diff --quiet d352567` held). `git stash create` writes no ref, and `git stash list` stayed empty.
   That tree differs from this commit's in two ways: the records (this log, this board, this
   campaign's README, `prompts/INDEX.md`), and one cell of the README addendum's measure table,
   where SGK's row first named only `643c3b2` and now names `643c3b2`, then `af26914` (item 9).
   Neither is in the wheel or read by the suite. `pyproject.toml` and `datastorekit/` are this
   commit's, so (a)'s and (b)'s diffs apply to an export of this commit as recorded.
   **IMPLEMENTATION CHOICE.**
8. **Two checks not asked for.** The release wheel's 20 `RECORD` hashes against `f5d8957`'s files,
   read by `git show`: 20 of 20 equal. And an `ast` comparison of SGK's base at `b510bc9` with the
   package's, docstrings blanked: equal at `6d8ee9a`; at `f5d8957` they differ in exactly the three
   hooks' decorator lists, `['staticmethod', 'abstractmethod']` → `['staticmethod']`, and are
   otherwise equal. That is what SGK's addendum's "The factory base" states. **IMPLEMENTATION
   CHOICE.**
9. **SGK's `HEAD` moved during the work**, by another session's commits, as dispatch foresaw: it was
   `643c3b2` at the start (clean) and `af26914` ("Record the orchestrator's review of
   dk-and-rpk-migration prompt 07") from midway, clean, at the end too. I measured both (§5.4): the
   same as at `789b72d`, and no instantiating call, so no stop. SGK's addendum and the README
   addendum name both. **IMPLEMENTATION CHOICE** (the record; nothing of SGK changed by me).
10. **`PROVENANCE.md` cites the `git diff --numstat` it measured**, and lists 01's files as three
    bullets, as the `actor-names` section does. **IMPLEMENTATION CHOICE.**

---

## 3. The hazards (§3)

1. **Additive documents.** `git diff --numstat -- docs/adoption` gives 107/0, 90/0, 92/0 and 86/0,
   and `git diff -- docs/adoption | grep '^-' | grep -v '^--- '` finds nothing. Each insertion was
   made by `<scratch>/probe/insert.py`, which adds lines only, after checking the line before and
   after the insert point. Three later edits changed only lines this prompt had added (an SGK
   table row's wording, a CPBH bullet's wording, the README table's SGK row), and one SGK row
   (`:533`) was added the same way. `docs/client-contract.md` and
   `docs/extraction-verification.md` are unchanged.
2. **Names and links.** Every one resolves (§5.5). The contract anchor, by GitHub's rule: "9.5
   `factory-defaults` prompt 01" (`docs/client-contract.md:338`), lower-cased, with the `.` and
   the backticks dropped and the spaces made hyphens, is `95-factory-defaults-prompt-01`. Each new
   heading, "Addendum: v0.2.3 (factory-defaults prompt 02, 2026-10-11)", the same way (the `:`,
   `.`, `(`, `)` and `,` dropped) is `addendum-v023-factory-defaults-prompt-02-2026-10-11`. The
   script derives every heading's slug that way and finds each anchor among them.
3. **The tag does not exist yet.** No document says `v0.2.3` is tagged: the README and the addenda
   state the pins, and the README says `v0.2.2`, `v0.2.1`, `v0.2.0` and `v0.1.0` "remain tagged";
   the gates say `v0.2.3` "is ready to be tagged … once CI passes there at both ends", and that 02
   makes no tag.
4. **No client is re-measured beyond §1.1.** I re-ran §1.1's measure with a script of my own
   (§5.4). It reproduces §1.1's table exactly at the checklists' commits and at `789b72d`, and at
   SGK's `HEAD`s read, `643c3b2` and `af26914`, SGK instantiates no factory. No CPBH or SI class
   lacks `register` or `build`. No stop.
5. **Offline only.** Every venv (`uv venv --offline`), install (`uv pip install --offline`) and
   build (`uv build --offline`) resolved from the cache: `setuptools` 84.0.0 (the build backend),
   `ray` 2.55.1 and `sqlalchemy` 2.0.46. Nothing was downloaded.
6. **`venv/`'s metadata.** Reinstalled by correction 1's command, the `egg-info` removed; the suite
   in `venv/` gives 504 OK after it (§5.1).
7. **No Ray.** The smoke script was not run. The release probes import the base and call its hooks
   only; the link check imports names, and `ray.is_initialized()` was `False` after. At the start
   and the end no Ray process was up (`pgrep -lf 'gcs_server|raylet|ray::'` empty), `RAY_ADDRESS`
   and `RAY_ENABLE_AUTO_CONNECT` were unset, and there was no `/tmp/ray/ray_current_cluster`.
8. **U5's wording.** Every statement of SGK's pin is permission, with no advice either way: "may
   stay on `v0.2.2` or move … as it chooses" (README `:88-89`; SGK's addendum, its head line and
   the README addendum; G2's line). None says SGK should or should not move.

---

## 4. The supersession tables

Each is as committed in its addendum. Line numbers are each file's at this commit.

### 4.1 `docs/adoption/README.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/README.md:12-15` | the `v0.2.2` addendum, "at the end", gives the pin **`v0.2.2`** | it gives `v0.2.2`'s pin and changes, true of `v0.2.2`; this addendum, now at the end, gives the pins of `v0.2.3` |
| `docs/adoption/README.md:137-138` | "`SQLAFactoryBase` (`datastorekit/SQL/factory_base.py:5-29`) is an ABC whose `register`, `build`, `store`, `validate` and `validate_on_startup` are abstract" | true through `v0.2.2`. At `v0.2.3` only `register` and `build` are abstract, and the base defaults the other three; "What changed since `v0.2.2`", above |
| `docs/adoption/README.md:141-146` | a client that registers instances "must give each instantiated class all five, or Python refuses to instantiate it (`TypeError`) … (U32)", and "the other route", registering the class itself | at `v0.2.3` an instantiated class needs only `register` and `build`, which every CPBH and SI class defines, so a registry of instances works as it stands and neither route is needed. The paragraph's first sentence, that the layer never instantiates a factory and calls its hooks on what the registry holds (`:135-137`), and its first bullet, that a client that registers classes is unaffected (`:139-140`), still hold |
| `docs/adoption/README.md:289-290` | "Every client adopts **`v0.2.2`** in place of `v0.2.1`" | CPBH and SI adopt `v0.2.3`, and SGK may stay on `v0.2.2` or move (`factory-defaults` U5); "The pins, by client", above |
| `docs/adoption/README.md:293` | the pin `…@v0.2.2` | for CPBH and SI the pin `…@v0.2.3`; for SGK `…@v0.2.2` or `…@v0.2.3` |
| `docs/adoption/README.md:351-355` | the `v0.2.2` addendum's `path:line`s are "this file's as committed with this addendum" | they are read at `6d8ee9a`, or five lines later here (all but `:7-10`) |
| `docs/adoption/README.md:360` | "every client adopts `v0.2.2` in place of `v0.2.1`" | as `:289-290` |
| `docs/adoption/README.md:361` | "the pin `…@v0.2.2`, above" | as `:293` |
| `docs/adoption/README.md:364` | at `v0.2.2`, "each checklist with both its addenda" | at `v0.2.3`, each checklist with its three addenda |
| `docs/adoption/README.md:365` | "all three adopt `v0.2.2` (U37; `actor-names` U3)" | as `:289-290` |
| `docs/adoption/README.md:366` | "the pin `…@v0.2.2`, above" | as `:293` |
| `docs/adoption/README.md:367` | "G2, G3 and G4 each hold when that client has adopted `v0.2.2` (U37; `actor-names` U3)" | G2 holds when SGK has adopted `v0.2.2` or later, and G3 and G4 when CPBH and SI have adopted `v0.2.3` (U37; `actor-names` U3; `factory-defaults` U5) |

Not in the prompt's table: `:351-355` (correction 3), `:360`, `:361`, `:364`, `:365`, `:366`.

### 4.2 `docs/adoption/secondarygwkit.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/secondarygwkit.md:21-25` | the `v0.2.2` addendum gives the pin **`v0.2.2`** | it gives `v0.2.2`'s pin and changes, true of `v0.2.2`; this addendum gives SGK's pins at `v0.2.3` |
| `docs/adoption/secondarygwkit.md:199-200` | `base.py` equals `datastorekit/SQL/factory_base.py` byte for byte | superseded by the `v0.2.1` addendum (its row for `:187-188`, here `:445`): they differ in comments and docstrings. At `v0.2.3` they also differ by the three decorators; "The factory base", above |
| `docs/adoption/secondarygwkit.md:404-406` | the `v0.2.1` addendum's "with its docstrings blanked it parses to the same code" | so through `v0.2.2`; at `v0.2.3` the three decorators differ, which SGK never meets; "The factory base", above |
| `docs/adoption/secondarygwkit.md:445` | the `v0.2.1` addendum's row: they "differ in comments and docstrings (09)" | at `v0.2.3` also by the three decorators |
| `docs/adoption/secondarygwkit.md:460-461` | "SGK adopts **`v0.2.2`** in place of `v0.2.1`", and G2 reads "SGK has adopted `v0.2.2`" | SGK may stay on `v0.2.2` or move to `v0.2.3` (`factory-defaults` U5), and G2 reads "SGK has adopted `v0.2.2` or later" |
| `docs/adoption/secondarygwkit.md:464` | the pin `…@v0.2.2` | `…@v0.2.2` or `…@v0.2.3`, as SGK chooses, above |
| `docs/adoption/secondarygwkit.md:523-527` | the `v0.2.2` addendum's `path:line`s are "this file's as committed with this addendum" | they are read at `6d8ee9a`, or six lines later here (all but `:16-19`) |
| `docs/adoption/secondarygwkit.md:532` | in the `v0.2.2` addendum's table, SGK adopts `v0.2.2` in place of `v0.2.1`, and G2 reads "SGK has adopted `v0.2.2`" | as `:460-461` |
| `docs/adoption/secondarygwkit.md:533` | "the pin `…@v0.2.2`, above" | as `:464` |
| `docs/adoption/secondarygwkit.md:536` | the package "at `v0.2.2`, with both addenda" | at `v0.2.2` or `v0.2.3`, with the three addenda |
| `docs/adoption/secondarygwkit.md:537` | at `v0.2.2`, "also the four of contract §9.3, none of which changes what SGK's calls use" | at `v0.2.3` also the change of contract §9.5, which changes nothing SGK's calls use, since SGK registers classes; "SGK instantiates no factory", above |
| `docs/adoption/secondarygwkit.md:538` | item 8's reasoning "extended to `v0.2.2`" | extended to `v0.2.3`; "Item 8 still holds", above |
| `docs/adoption/secondarygwkit.md:539` | "G2 holds when SGK has adopted `v0.2.2` (U37; `actor-names` U3)" | G2 holds when SGK has adopted `v0.2.2` or later (U37; `actor-names` U3; `factory-defaults` U5) |

Not in the prompt's table: `:404-406`, `:445` (the "add that" of the prompt's row, cited by its own
line), `:523-527` (correction 3), `:532`, `:533`, `:536`, `:537`, `:538`.

### 4.3 `docs/adoption/champbh.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/champbh.md:22-26` | the `v0.2.2` addendum gives the pin **`v0.2.2`** | it gives `v0.2.2`'s pin and changes, true of `v0.2.2`; this addendum gives `v0.2.3` |
| `docs/adoption/champbh.md:40-41` | "its factory base is an ABC, and CPBH registers instances of 20 classes that define only two of its five abstract hooks (U32)" | at `v0.2.3` the base's only abstract hooks are `register` and `build`, which all 23 classes define, so CPBH's instances are accepted; "What changed for CPBH since `v0.2.2`", above |
| `docs/adoption/champbh.md:213-215` | "The package's `SQLAFactoryBase` is an ABC with the five abstract (`datastorekit/SQL/factory_base.py:5-29`). Subclassing it, `sqla_version_factory()` and the other 19 raise `TypeError` at instantiation" | true through `v0.2.2`. At `v0.2.3` the base defaults the three, and each of the 20 instantiates |
| `docs/adoption/champbh.md:216-227` | "The two routes, and what each needs": define the three hooks on each of the 20, or register the class itself | neither is needed at `v0.2.3`: CPBH registers its instances as they stand. The rest of item 5's U32 paragraph (`:206-212`), the counts and CPBH's own base, still holds |
| `docs/adoption/champbh.md:478-479` | "CPBH adopts **`v0.2.2`** in place of `v0.2.1`", and G3 reads "CPBH has adopted `v0.2.2`" | CPBH adopts `v0.2.3` in place of `v0.2.2` (`factory-defaults` U5), and G3 reads "CPBH has adopted `v0.2.3`" |
| `docs/adoption/champbh.md:482` | the pin `…@v0.2.2` | the pin `…@v0.2.3`, above |
| `docs/adoption/champbh.md:515-519` | the `v0.2.2` addendum's `path:line`s are "this file's as committed with this addendum" | they are read at `6d8ee9a`, or six lines later here (all but `:17-20`) |
| `docs/adoption/champbh.md:524` | in the `v0.2.2` addendum's table, CPBH adopts `v0.2.2` in place of `v0.2.1`, and G3 reads "CPBH has adopted `v0.2.2`" | as `:478-479` |
| `docs/adoption/champbh.md:525` | "the pin `…@v0.2.2`, above" | the pin `…@v0.2.3`, above |
| `docs/adoption/champbh.md:527` | the package "at `v0.2.2`, with both addenda" | at `v0.2.3`, with the three addenda |
| `docs/adoption/champbh.md:528` | "G3 holds when CPBH has adopted `v0.2.2` (U37; `actor-names` U3)" | G3 holds when CPBH has adopted `v0.2.3` (U37; `actor-names` U3; `factory-defaults` U5) |

Not in the prompt's table: `:515-519` (correction 3), `:524`, `:525`, `:527`. The prompt's
`:200-221` is cited as `:213-215` and `:216-227`, its superseded parts, with `:206-212` named as
still holding.

### 4.4 `docs/adoption/stochasticinstantons.md`

| `path:line` | The statement | What replaces it |
|---|---|---|
| `docs/adoption/stochasticinstantons.md:20-24` | the `v0.2.2` addendum gives the pin **`v0.2.2`** | it gives `v0.2.2`'s pin and changes, true of `v0.2.2`; this addendum gives `v0.2.3` |
| `docs/adoption/stochasticinstantons.md:36-37` | SI "registers factory instances (16 classes lack three of the five abstract hooks, U32)" | the count holds; at `v0.2.3` the base's only abstract hooks are `register` and `build`, which all 28 classes define, so SI's instances are accepted; "What changed for SI since `v0.2.2`", above |
| `docs/adoption/stochasticinstantons.md:131-132` | the three import-time sites: "under the package's ABC each raises `TypeError` at import" | true through `v0.2.2`; under `v0.2.3` each instantiates. The rest of the paragraph (`:127-131`), the sites themselves, still holds |
| `docs/adoption/stochasticinstantons.md:198-206` | the package's base "is" an ABC (`datastorekit/SQL/factory_base.py:5-29`), "so each raises `TypeError` at instantiation: in the registry, and at the three import-time sites of item 3", and the two routes, "The choice is SI's" | true through `v0.2.2`. At `v0.2.3` each instantiates, and neither route is needed. The rest of item 5's U32 paragraph (`:193-198`), the counts and SI's own base, still holds |
| `docs/adoption/stochasticinstantons.md:448-450` | "SI adopts **`v0.2.2`** in place of `v0.2.1`, when it is next active", and G4 reads "SI has adopted `v0.2.2`" | SI adopts `v0.2.3` in place of `v0.2.2`, when it is next active (`factory-defaults` U5), and G4 reads "SI has adopted `v0.2.3`" |
| `docs/adoption/stochasticinstantons.md:453` | the pin `…@v0.2.2` | the pin `…@v0.2.3`, above |
| `docs/adoption/stochasticinstantons.md:484-488` | the `v0.2.2` addendum's `path:line`s are "this file's as committed with this addendum" | they are read at `6d8ee9a`, or six lines later here (all but `:15-18`) |
| `docs/adoption/stochasticinstantons.md:493` | in the `v0.2.2` addendum's table, SI adopts `v0.2.2` in place of `v0.2.1`, and G4 reads "SI has adopted `v0.2.2`" | as `:448-450` |
| `docs/adoption/stochasticinstantons.md:494` | "the pin `…@v0.2.2`, above" | the pin `…@v0.2.3`, above |
| `docs/adoption/stochasticinstantons.md:496` | the package "at `v0.2.2`, with both addenda" | at `v0.2.3`, with the three addenda |
| `docs/adoption/stochasticinstantons.md:497` | "G4 holds when SI has adopted `v0.2.2` (U37; `actor-names` U3)" | G4 holds when SI has adopted `v0.2.3` (U37; `actor-names` U3; `factory-defaults` U5) |

Not in the prompt's table: `:484-488` (correction 3), `:493`, `:494`, `:496`. The prompt's
`:187-200` is cited as `:198-206`, its superseded part, with `:193-198` named as still holding.

**Considered and not superseded** (correction 4, and my own reading). The grep of §2.4 (`abstract`,
`TypeError`, `instanti`, `U32`, case-insensitive) outside the new addenda finds, at this tree:
- README `:135-142`: the paragraph superseded above, but for its first sentence and first bullet
  (`:135-137`, `:139-140`), which stay true, and say so in the table;
- SGK `:204` (`:203-205`, "the abstractness of `SQLAFactoryBase` is never enforced on them (U32
  does not reach SGK)"): true at `v0.2.3`, and more so;
- CPBH `:41`, `:206-207`, `:212-215`: superseded as tabled, but for `:206-212` (the counts, and
  CPBH's own base, "not an ABC"), which stay true; `:207`'s "all five abstract hooks" names the
  five hooks as the `v0.2.0` base had them, and the count it gives holds;
- CPBH `:250` ("Each call is a `TypeError`", the constructor's keywords): another `TypeError`,
  true;
- CPBH `:700`, `:703`, SI `:87`, `:665`: the file names `AbstractCoupling.py` and
  `AbstractPotential.py`, not statements;
- SI `:37`, `:131-132`, `:193`, `:199`: superseded as tabled, but for the counts and the sites;
- SI `:82` (the `timestamp=` calls) and `:245` (the constructor's keywords): other `TypeError`s,
  true.

And, beyond the grep:
- the "all five" cells of item 5's tables (CPBH `:193-199`, SI `:186-191`): which hooks a class
  defines, facts of the client, unchanged;
- each checklist's `v0.2.2` addendum's statements of what `v0.2.2` carries (SGK `:467`, CPBH
  `:485`): true, and `v0.2.3` carries the same;
- SGK's `v0.2.2` addendum's "adopting `v0.2.2` fixes it" (`:510`) and its table's row for `:422-424`
  (`:534`): true of `v0.2.2` or later;
- every `datastorekit/` citation of 07a's text and of the earlier addenda: each is read at its own
  tag, by the files' rules;
- the README's `:313` (a store that opened under `v0.2.1` opens under `v0.2.2`) and each
  checklist's item 8 lines in the `v0.2.2` addendum: true; each new addendum extends them to
  `v0.2.3`.

---

## 5. Verification performed

### 5.1 The suite (§4.1)

Every run in the foreground, its output in `<scratch>/out/`, the verdict grepped from it.

| Where | When | Result | `ResourceWarning` lines | `datastorekit` |
|---|---|---|---|---|
| `venv/` (3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39, SQLite 3.53.4) | at dispatch, before any change | `Ran 504 tests in 118.246s` `OK` | 0 | 0.2.2 |
| `<scratch>/venv-high-before` (3.13.16 / 2.55.1 / 2.0.46, SQLite 3.53.4, `setuptools` 84.0.0), `git archive HEAD` (`389e13b`) installed editable `--no-deps --no-build-isolation` | at dispatch | `Ran 504 tests in 191.958s` `OK` | 4 | 0.2.2 |
| `venv/` | after `pyproject.toml` and the reinstall | `Ran 504 tests in 131.766s` `OK` | 0 | 0.2.3 |
| `<scratch>/venv-high`, the same pins, `git archive d352567` installed editable `--no-deps --no-build-isolation` | after every document edit | `Ran 504 tests in 111.781s` `OK` | 4 | 0.2.3 |
| `venv/` | after the records, before the commit | `Ran 504 tests in 117.713s` `OK` | 0 | 0.2.3 |

The count is **504** before and after, at both ends. The 4 `ResourceWarning` lines at the high end
are timing (`actor-names` log 01, correction 8; CI saw 4 on `85f504d`).

### 5.2 The checks (§4.2)

- `compare_ported_tests.py`, before and after, exit 0, its last line: `OK: 20 module(s) keep their
  source's tests, classes and assertion skeletons; 1 test(s) declared not ported`.
- `./venv/bin/black --check datastorekit docs` (black 25.1.0), before and after: `74 files would be
  left unchanged.` No `.py` file changed.
- The two guards, `test_layer_is_generic` and `test_prose_names_no_source`, are in the suite and
  pass in every run above.

### 5.3 The release check (§4.3)

**The build.** `git archive d352567 | tar -x -C <scratch>/exports/release` (§2 item 7), then
`uv build --offline --wheel --out-dir <scratch>/wheels/release <scratch>/exports/release`, exit 0.
For the comparison, `git archive v0.2.2` into `<scratch>/exports/v022`, built the same way. Nothing
was built in the checkout.

| | The release | `v0.2.2`'s, for comparison |
|---|---|---|
| Wheel | `datastorekit-0.2.3-py3-none-any.whl` | `datastorekit-0.2.2-py3-none-any.whl` |
| Size | 99,185 bytes | 98,811 bytes |
| Entries | **25**: none under `datastorekit/tests/`, 3 under `datastorekit/tools/` | 25 |
| SHA-256 | `cb13ba88428d019525927440d911796e04b076c5935cf6b97812473ca318748d` | `a6978dfd239bcc73b9d190c11e232755864c8ac760c4a364f0c55fd3ea1a3282` |
| `RECORD` SHA-256 | `bbc538a64c5f90835c521903f3f61b9bf8cfebf1e34571b50de2bc83b42397e5` | `7dd75ce12638c7c5afb73a8d766d0393382b4a371d56632dc85d699162600376` (`actor-names` log 02's, §5.3) |
| `WHEEL` | `Generator: setuptools (84.0.0)` | the same |
| `METADATA` | `Name: datastorekit`, **`Version: 0.2.3`**, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43`, `Requires-Dist: sqlalchemy<2.1,>=2.0.39` | `Version: 0.2.2`, the rest the same |

The wheel's bytes are not reproducible across builds; only its SHA-256 is mine to record. Both
sizes equal the orchestrator's.

**The file list:**

```
datastorekit/__init__.py
datastorekit/_timing.py
datastorekit/contract.py
datastorekit/defaults.py
datastorekit/object.py
datastorekit/replication.py
datastorekit/shard_paths.py
datastorekit/store_inventory.py
datastorekit/store_reader.py
datastorekit/SQL/ClientPool.py
datastorekit/SQL/Datastore.py
datastorekit/SQL/ProfileAgent.py
datastorekit/SQL/SerialPoolBroker.py
datastorekit/SQL/ShardedPool.py
datastorekit/SQL/__init__.py
datastorekit/SQL/factory_base.py
datastorekit/SQL/schema.py
datastorekit/tools/__init__.py
datastorekit/tools/shard_key_audit.py
datastorekit/tools/sharded_store.py
datastorekit-0.2.3.dist-info/licenses/LICENSE
datastorekit-0.2.3.dist-info/METADATA
datastorekit-0.2.3.dist-info/WHEEL
datastorekit-0.2.3.dist-info/top_level.txt
datastorekit-0.2.3.dist-info/RECORD
```

**The `RECORD` comparison**, `v0.2.2`'s wheel against the release: 20 lines under `datastorekit/`
on each side, the same paths, and one differs.

```
DIFFERS datastorekit/SQL/factory_base.py  sha256=plSnmopwl3n4hkeExHNx0N76EYpOH6CAzMT60eZ3CPs,2233  sha256=nAQ3pkZJr5uqKcrSrLDmvLG4CJ5cI04SBjzW92IbhsE,3529
same    the other 19: SQL/ClientPool.py, SQL/Datastore.py, SQL/ProfileAgent.py,
        SQL/SerialPoolBroker.py, SQL/ShardedPool.py, SQL/__init__.py, SQL/schema.py, __init__.py,
        _timing.py, contract.py, defaults.py, object.py, replication.py, shard_paths.py,
        store_inventory.py, store_reader.py, tools/__init__.py, tools/shard_key_audit.py,
        tools/sharded_store.py
```

Each of the release's 20 `RECORD` hashes equals the hash of `f5d8957`'s file, read by `git show`
(§2 item 8).

**The install.** `uv venv --offline -p /opt/local/bin/python3.13 <scratch>/venv-release`, then
`uv pip install --offline --python <scratch>/venv-release/bin/python <the wheel> "ray==2.55.1"
"sqlalchemy==2.0.46"`: "Resolved 20 packages", "Installed 20 packages", exit 0, not editable.
Python 3.13.16, SQLite 3.53.4.

**The commands.** `<scratch>/probe/release_check.sh` ran them with `python -I`, from
`<scratch>/outside`, a directory outside the repository, with `PYTHONPATH` unset. `<R>` is the
venv's `site-packages`.

```
$ python -I -c "<import the package and its 19 submodules, print each __file__>"
datastorekit <R>/datastorekit/__init__.py
datastorekit.SQL <R>/datastorekit/SQL/__init__.py
datastorekit.SQL.ClientPool <R>/datastorekit/SQL/ClientPool.py
datastorekit.SQL.Datastore <R>/datastorekit/SQL/Datastore.py
datastorekit.SQL.ProfileAgent <R>/datastorekit/SQL/ProfileAgent.py
datastorekit.SQL.SerialPoolBroker <R>/datastorekit/SQL/SerialPoolBroker.py
datastorekit.SQL.ShardedPool <R>/datastorekit/SQL/ShardedPool.py
datastorekit.SQL.factory_base <R>/datastorekit/SQL/factory_base.py
datastorekit.SQL.schema <R>/datastorekit/SQL/schema.py
datastorekit._timing <R>/datastorekit/_timing.py
datastorekit.contract <R>/datastorekit/contract.py
datastorekit.defaults <R>/datastorekit/defaults.py
datastorekit.object <R>/datastorekit/object.py
datastorekit.replication <R>/datastorekit/replication.py
datastorekit.shard_paths <R>/datastorekit/shard_paths.py
datastorekit.store_inventory <R>/datastorekit/store_inventory.py
datastorekit.store_reader <R>/datastorekit/store_reader.py
datastorekit.tools <R>/datastorekit/tools/__init__.py
datastorekit.tools.shard_key_audit <R>/datastorekit/tools/shard_key_audit.py
datastorekit.tools.sharded_store <R>/datastorekit/tools/sharded_store.py
20 modules imported
exit=0

$ python -I -c "import importlib.metadata as m; print(m.version(\"datastorekit\"))"
0.2.3
exit=0

$ python -I -c "<the base: __abstractmethods__, the three hooks signatures, static, abstract?>"
__abstractmethods__: ['build', 'register']
register staticmethod () abstract
build staticmethod (payload, conn, table, inserter, tables, inserters) abstract
store staticmethod (obj, conn, table, inserter, tables, inserters) not abstract
validate staticmethod (obj, conn, table, tables) not abstract
validate_on_startup staticmethod (conn, table, tables, prune=False) not abstract
revalidate staticmethod (serial, conn, table, tables) -> bool not abstract
owned_serials staticmethod (obj) -> Optional[List[Optional[int]]] not abstract
inventory_spec staticmethod () not abstract
exit=0

$ python -I -c "<a subclass defining only register and build: instantiate; call the three on the instance with their arity>"
F() -> F
f.store(*[None] * 6) -> NotImplementedError, args=()
f.validate(*[None] * 4) -> NotImplementedError, args=()
f.validate_on_startup(*[None] * 3) -> NotImplementedError, args=()
exit=0

$ python -I -c "import datastorekit.tests"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import datastorekit.tests
ModuleNotFoundError: No module named 'datastorekit.tests'
exit=1

$ python -I -m datastorekit.tools.sharded_store --help
usage: python -m datastorekit.tools.sharded_store [-h] {copy,move} src dst

Copy or move a closed ShardedPool datastore under a new name.

exit=0
```

**The assertions**, `<scratch>/probe/assert_release.py <wheel> <venv python> <v0.2.2's wheel>`:

```
wheel sha256: cb13ba88428d019525927440d911796e04b076c5935cf6b97812473ca318748d
PASS wheel name: datastorekit-0.2.3-py3-none-any.whl
PASS METADATA Version: Version: 0.2.3
PASS no entry under datastorekit/tests/: 0 of 25 entries
PASS 25 entries: 25
PASS RECORD against v0.2.2: only SQL/factory_base.py differs: 20 and 20 lines under datastorekit/; differing: ['datastorekit/SQL/factory_base.py']
PASS importlib.metadata.version: 0.2.3
PASS imported from site-packages: <scratch>/venv-release/lib/python3.13/site-packages/datastorekit/SQL/factory_base.py
PASS __abstractmethods__ is {register, build}: ['build', 'register']
PASS the three keep v0.2.2's signatures, static, not abstract: store staticmethod (obj, conn, table, inserter, tables, inserters) False
validate staticmethod (obj, conn, table, tables) False
validate_on_startup staticmethod (conn, table, tables, prune=False) False
PASS a subclass defining register and build instantiates; its three hooks raise bare NotImplementedError: instantiated F; store NotImplementedError (); validate NotImplementedError (); validate_on_startup NotImplementedError ()
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
PASS sharded_store --help exits 0: exit=0
RESULT: OK
```

**The release check passes.** `git status --short --ignored` shows no `build/`, `dist/` or
`*.egg-info` in the checkout (§5.8).

### 5.4 §1.1's measure, re-run (hazard 4)

`<scratch>/probe/measure_factories.py <repo> <commit>`, run with `/opt/local/bin/python3.13 -I`
from `<scratch>/outside`: it lists the commit's `.py` files with `git ls-tree -r`, reads each with
`git show <commit>:<path>`, parses it with `ast` (nothing imported or run), and finds every
`ClassDef` one of whose bases is a `Name` or `Attribute` named `SQLAFactoryBase`, the
`FunctionDef`s in its body, and every `Call` whose function is a `Name` or `Attribute` naming one
of those classes.

```
== SGK at b510bc9
python files parsed: 462
factory classes (bases name SQLAFactoryBase): 38 (38 names)
lacking one of store/validate/validate_on_startup: 31
lacking register or build: 0 []
calls that instantiate one (by name): 0
of a class lacking one of the three: 0
== SGK at 789b72d
python files parsed: 427
factory classes (bases name SQLAFactoryBase): 38 (38 names)
lacking one of store/validate/validate_on_startup: 31
lacking register or build: 0 []
calls that instantiate one (by name): 0
of a class lacking one of the three: 0
== SGK at 643c3b2
python files parsed: 425
factory classes (bases name SQLAFactoryBase): 38 (38 names)
lacking one of store/validate/validate_on_startup: 31
lacking register or build: 0 []
calls that instantiate one (by name): 0
of a class lacking one of the three: 0
== CPBH at 52142d7
python files parsed: 205
factory classes (bases name SQLAFactoryBase): 23 (23 names)
lacking one of store/validate/validate_on_startup: 20
lacking register or build: 0 []
calls that instantiate one (by name): 27
  Datastore/SQL/Datastore.py: 27 calls, lines 95-121: [(95, 'sqla_version_factory'), (96, 'sqla_store_tag_factory'), (97, 'sqla_redshift_factory'), (98, 'sqla_tolerance_factory'), (99, 'sqla_dimensionless_quantity_factory'), (100, 'sqla_dimensionful_quantity_factory'), (101, 'sqla_dimensionful_quantity_factory'), (102, 'sqla_dimensionful_quantity_factory'), (103, 'sqla_dimensionful_quantity_factory'), (104, 'sqla_dimensionful_quantity_factory'), (105, 'sqla_InversePowerPotential_factory'), (106, 'sqla_StarobinskyPotential_factory'), (107, 'sqla_ExponentialPotential_factory'), (108, 'sqla_ReclinerPotential_factory'), (109, 'sqla_ReflectingPotential_factory'), (110, 'sqla_ExponentialCoupling_factory'), (111, 'sqla_QCDCosmology_factory'), (112, 'sqla_IntegrationSolver_factory'), (113, 'sqla_ScalarModelFactory'), (114, 'sqla_ScalarModelTagAssociation_factory'), (115, 'sqla_ScalarModelValue_factory'), (116, 'sqla_AdiabaticHistoryFactory'), (117, 'sqla_AdiabaticHistoryTagAssociation_factory'), (118, 'sqla_AdiabaticHistoryValue_factory'), (119, 'sqla_BBNDataFactory'), (120, 'sqla_BBNDataTagAssociation_factory'), (121, 'sqla_BBNDataValue_factory')]
of a class lacking one of the three: 24
  Datastore/SQL/Datastore.py: 24
== SI at 7bb3efd
python files parsed: 195
factory classes (bases name SQLAFactoryBase): 28 (28 names)
lacking one of store/validate/validate_on_startup: 16
lacking register or build: 0 []
calls that instantiate one (by name): 33
  CosmologyConcepts/Potentials/registry.py: 2 calls, lines 33-40: [(33, 'sqla_QuadraticPotential_factory'), (40, 'sqla_QuarticPotential_factory')]
  Datastore/SQL/Datastore.py: 30 calls, lines 97-126: [(97, 'sqla_version_factory'), (98, 'sqla_store_tag_factory'), (99, 'sqla_redshift_factory'), (100, 'sqla_tolerance_factory'), (101, 'sqla_efold_factory'), (102, 'sqla_delta_Nstar_factory'), (103, 'sqla_N_init_factory'), (104, 'sqla_N_final_factory'), (105, 'sqla_n_collocation_points_factory'), (106, 'sqla_alpha_regularization_factory'), (107, 'sqla_dimensionful_quantity_factory'), (108, 'sqla_dimensionless_quantity_factory'), (109, 'sqla_dimensionful_quantity_factory'), (110, 'sqla_dimensionful_quantity_factory'), (111, 'sqla_QuadraticPotential_factory'), (112, 'sqla_QuarticPotential_factory'), (113, 'sqla_MasslessDecoupledDiffusion_factory'), (114, 'sqla_IntegrationSolver_factory'), (115, 'sqla_InflatonTrajectory_factory'), (116, 'sqla_InflatonTrajectoryValue_factory'), (117, 'sqla_cosmological_params_factory'), (118, 'sqla_FullInstantonFactory'), (119, 'sqla_FullInstantonValue_factory'), (120, 'sqla_GradientCoupledInstantonFactory'), (121, 'sqla_GradientCoupledInstantonValue_factory'), (122, 'sqla_GradientCoupledInstantonProfileFactory'), (123, 'sqla_SlowRollInstantonFactory'), (124, 'sqla_SlowRollInstantonValue_factory'), (125, 'sqla_CompactionFunctionFactory'), (126, 'sqla_CompactionFunctionSamplesFactory')]
  Datastore/SQL/ObjectFactories/MasslessDecoupledDiffusion.py: 1 calls, lines 71-71: [(71, 'sqla_MasslessDecoupledDiffusion_factory')]
of a class lacking one of the three: 21
  CosmologyConcepts/Potentials/registry.py: 2
  Datastore/SQL/Datastore.py: 18
  Datastore/SQL/ObjectFactories/MasslessDecoupledDiffusion.py: 1
== SGK at af26914
python files parsed: 425
factory classes (bases name SQLAFactoryBase): 38 (38 names)
lacking one of store/validate/validate_on_startup: 31
lacking register or build: 0 []
calls that instantiate one (by name): 0
of a class lacking one of the three: 0
```

**It reproduces §1.1's table exactly**, at SGK `b510bc9` and `789b72d`, CPBH `52142d7` and SI
`7bb3efd`. At SGK's `HEAD`s read during the work, `643c3b2` and `af26914`, the same: no
instantiating call. No stop.

**The rest of §1.1**, read by `git`:
- CPBH's base at `52142d7` (`Datastore/SQL/ObjectFactories/base.py:16-30`) and SI's at `7bb3efd`
  (the same lines): a plain `class SQLAFactoryBase:` whose five hooks are instance methods, each
  `raise NotImplementedError`.
- SGK at `643c3b2` and `af26914`: `0c9e2cf` (2026-10-11, "Adopt datastorekit and delete SGK's copy
  of the datastore layer") is an ancestor (`git merge-base --is-ancestor`);
  `Datastore/SQL/ObjectFactories/base.py` does not exist (`git cat-file -e` fails);
  `requirements.txt:17` is `datastorekit @ git+https://github.com/ds283/DatastoreKit@v0.2.2`; 20
  files import `from datastorekit.SQL.factory_base import SQLAFactoryBase`, and no `.py` file
  imports `Datastore.SQL.ObjectFactories.base` (one string in SGK's own import-rewrite script
  names it).
- SGK's base at `6f7f291`: five `@abstractmethod` lines (`:7`, `:12`, `:17`, `:22`, `:27`).

### 5.5 Names and links (hazard 2)

**The method.** `<scratch>/probe/check_links.py`, a scratch script never committed, over
`README.md`, `PROVENANCE.md`, the four adoption files and the extraction board's §2:
- **Links.** Each relative Markdown link outside a code fence is resolved: the file relative to
  the document, then the anchor among the target's headings, outside code fences, by GitHub's rule
  (§3 item 2).
- **Paths in the added lines** (`git diff -U0 HEAD`): each backticked path, with any `:a-b`, is
  checked in this tree if it is this repository's, or at the client commit the addendum names
  through `git show` (SGK `b510bc9` and `af26914`, CPBH `52142d7`, SI `7bb3efd`).
- **Names.** Every dotted `datastorekit.` name in the six files is imported in `venv/` by
  `<scratch>/probe/import_names.py`, with the bare names the new text uses.

**The output** (summarised; the full reports are `<scratch>/out/check-links.txt` and
`<scratch>/out/import-names.txt`):
- **107 relative links, every one resolved**, among them:
  - `docs/client-contract.md#95-factory-defaults-prompt-01` (README `:19`, `:111`) and
    `../client-contract.md#95-factory-defaults-prompt-01` (each addendum), heading
    `docs/client-contract.md:338`; `docs/client-contract.md#3-the-factory-hooks` (`:110`);
  - `#addendum-v023-factory-defaults-prompt-02-2026-10-11` from each file's italic line, from the
    README's addendum to each checklist's, and from each checklist's to the README's;
  - the three gate rows' links to each checklist's new anchor;
  - every existing link, the earlier addenda's and the README's included.
- **Paths: 147 checked, 0 failed, 2 skipped.** The skipped are `Datastore/SQL/ObjectFactories/base.py`
  in `PROVENANCE.md` (SGK's, at `6f7f291`: checked by hand, present, §5.4) and SGK's `base.py`
  shorthand in its table. Among the checked: `Datastore/SQL/Datastore.py:95-121` at CPBH,
  `:97-126`, `CosmologyConcepts/Potentials/registry.py:33`,
  `Datastore/SQL/ObjectFactories/MasslessDecoupledDiffusion.py:71` and
  `Datastore/SQL/ObjectFactories/base.py:16-30` at SI and CPBH, `requirements.txt:17` at SGK
  `af26914`, and every `datastorekit/` path at this tree. The script's rule for a bare `:a-b` is
  approximate: it gives one the last path named on the line. Three in-file citations it so
  misread (SGK `:187-188` and `:445`, SI `:193-198`) I checked by hand: `:187-188` at `33778b0` is
  the byte-for-byte sentence, `:445` here the `v0.2.1` row for it, and SI `:193-198` the U32
  paragraph's counts and SI's own base. Every own-file citation of the four tables was printed and
  read against the statement it quotes (§4), and the earlier addenda's by `check_shift.py` (§5.7).
- **20 dotted names, every one importable in `venv/`:** `datastorekit.SQL`, `.SQL.Datastore`,
  `.SQL.Datastore.Datastore`, `.SQL.ShardedPool`, `.SQL.factory_base`, `.SQL.schema`,
  `.SQL.schema.dependent_tables`, `._timing`, `.contract`, `.contract.VERSION_LABEL`,
  `.contract.VERSION_SERIAL_KEY`, `.contract.require_version_serial`, `.defaults`,
  `.replication`, `.shard_paths`, `.store_inventory`, `.store_inventory.read_inventory`,
  `.store_reader`, `.tests`, `.tools`; and `datastorekit.tools.sharded_store` and
  `.shard_key_audit`, named in the README's tools section, import from the release's
  `site-packages` (§5.3). The bare names: `SQLAFactoryBase` and its eight hooks, its
  `__abstractmethods__` (`['build', 'register']`); `datastorekit.tests.test_factory_instances` (its
  six test classes, `TestAParameterisedFactory` for "test 2" among them);
  `datastorekit.tests.client.instances` (`scalar_entry`, `scalar_entry_factory`,
  `instance_registry`); `test_neutral_client.ABSTRACT_HOOKS`, `('register', 'build')`.
  `ray.is_initialized()` was `False` after the imports.
- **The contract rows** each addendum names exist with those "Change" cells, in §9.5
  (`docs/client-contract.md:350-352`): "A factory may be an instance", "`store`, `validate`,
  `validate_on_startup`" and "What a pool's actors receive"; and §9.5's preamble says a client
  that registers classes meets nothing new.
- **The `v0.2.3` line citations**, read at the tree: `datastorekit/SQL/factory_base.py:5-80` is the
  class; `:6-9` `register` and `:11-14` `build`, each `@staticmethod @abstractmethod`; `:16-19` the
  comment on defaulted hooks; `:21-50` `store`, `validate` and `validate_on_startup`.

`RESULT: OK` for both scripts, but for the three by-hand citations above.

### 5.6 What changed since `v0.2.2` (§1.1, re-checked)

`git diff --numstat 6d8ee9a f5d8957 -- datastorekit`: `SQL/factory_base.py` 24/6,
`tests/client/instances.py` 98/0, `tests/test_factory_instances.py` 339/0,
`tests/test_neutral_client.py` 23/2. `git diff --quiet f5d8957 HEAD -- datastorekit` holds.

### 5.7 The documents (§4.4)

Every remaining `v0.2.2`, by line, with why it stays:

| File | Lines | Why it stays |
|---|---|---|
| `README.md` | `:21` | history: the `v0.2.2` status paragraph |
| | `:86` | the "remain tagged" sentence |
| | `:88` | SGK's permitted pin (U5) |
| | `:121` | history: "the fix of `v0.2.2`", in the extended item |
| `PROVENANCE.md` | `:160`, `:178` | history: the `actor-names` section (SGK "receives the fix by adopting `v0.2.2`", true of `v0.2.2` or later) |
| `docs/adoption/README.md` | `:13`, `:14` | the `v0.2.2` italic line, superseded (`:12-15`) |
| | `:19`, `:20` | this prompt's italic line |
| | `:282`, `:303`, `:313`, `:348`, `:359`, `:362` | history: the `v0.2.2` addendum's heading, table header, store sentence, line rule and two rows true of `v0.2.2` |
| | `:289`, `:293`, `:360`, `:361`, `:364`–`:367` | statements this addendum supersedes |
| | `:375`–`:470` (27 lines) | this addendum's own text and table |
| `docs/adoption/secondarygwkit.md` | `:22`, `:23` | the `v0.2.2` italic line, superseded |
| | `:28`–`:30` | this prompt's italic line (SGK's permitted pin) |
| | `:453`, `:467`, `:477`, `:499`, `:510`, `:520`, `:531`, `:534` | history: the `v0.2.2` addendum, true of `v0.2.2` |
| | `:460`, `:461`, `:464`, `:532`, `:533`, `:536`–`:539` | statements this addendum supersedes (`:464` and `:533` stay one of SGK's two permitted pins) |
| | `:546`–`:625` (23 lines) | this addendum's own text and table |
| `docs/adoption/champbh.md` | `:23`, `:24` | the `v0.2.2` italic line, superseded |
| | `:29`–`:31` | this prompt's italic line |
| | `:471`, `:485`, `:512`, `:523` | history: the `v0.2.2` addendum, true of `v0.2.2` |
| | `:478`, `:479`, `:482`, `:524`, `:525`, `:527`, `:528` | statements this addendum supersedes |
| | `:535`–`:612` (19 lines) | this addendum's own text and table |
| `docs/adoption/stochasticinstantons.md` | `:21`, `:22` | the `v0.2.2` italic line, superseded |
| | `:27`–`:29` | this prompt's italic line |
| | `:441`, `:471`, `:481`, `:492` | history: the `v0.2.2` addendum, true of `v0.2.2` |
| | `:448`, `:450`, `:453`, `:493`, `:494`, `:496`, `:497` | statements this addendum supersedes |
| | `:504`–`:577` (18 lines) | this addendum's own text and table |

**The shifts (correction 3), checked line by line** by `<scratch>/probe/check_shift.py`: for each
own-file citation of the `v0.2.1` addenda (read at `33778b0`, shifted k + N) and of the `v0.2.2`
addenda (read at `6d8ee9a`, shifted N), every line of the range equals this tree's line, the same
line where it is above the insert: 106 lines in the four files, 0 differ.

`git diff -- docs/adoption` has no `-` line (hazard 1). `docs/client-contract.md` and
`docs/extraction-verification.md` are unchanged (`git diff --quiet`).

### 5.8 The tree and the clients (§4.6)

- `git status --short --ignored` before staging shows the eleven files of §7's list that this
  prompt changes as modified, this log as new, and dispatch's ignored entries: `.idea/`, `venv/`,
  and five `__pycache__/` directories (`datastorekit/`, `datastorekit/SQL/`, `datastorekit/tests/`,
  `datastorekit/tests/client/`, `docs/extraction/`). There is no `build/`, `dist/` or `*.egg-info`.
- `git diff --quiet` holds for `datastorekit/`, `docs/client-contract.md`,
  `docs/extraction-verification.md`, `docs/extraction/`, `.github/`, `CLAUDE.md`, `LICENSE` and
  `.gitignore`. On the extraction board only `:1537-1539` changed.
- The tags are `v0.1.0`, `v0.2.0`, `v0.2.1` and `v0.2.2`; `origin/main` is `85f504d`, as at
  dispatch.

The clients, read only through `git rev-parse`, `git status`, `git ls-tree`, `git show`, `git grep`,
`git log`, `git merge-base` and `git cat-file`:

| Client | At the start | At the end | `git status --short` |
|---|---|---|---|
| SGK | `643c3b2`, branch `handover-remedial` | `af26914`, the same branch | empty at the start and at the end |
| CPBH | `52142d7`, `main` | `52142d7`, unchanged | 25 entries, the same at the end (`cmp` silent): ` M prompts/INDEX.md` and 24 untracked (not read) |
| SI | `7bb3efd`, `main` | `7bb3efd`, unchanged | empty at the start and at the end |

SGK's `HEAD` moved by the other session's commit `af26914` (§2 item 9); CPBH and SI are unchanged.

---

## 6. The deliberate-breakage record (§4.5)

**The method.**
1. Each diff below was made with `diff -u` of `pyproject.toml` before and after the one change,
   labelled `a/` and `b/`, and is recorded exactly as applied (`<scratch>/breaks/`).
2. Each has its own export: `git archive d352567` (whose `pyproject.toml` is this commit's) into
   `<scratch>/exports/break-a` and `break-b`, and `git archive v0.2.2` into `break-c`.
3. In each export, `git apply --check` passed on the clean export, `git apply` applied it, and
   `git apply -R --check` passed on the applied one.
4. Each was built with `uv build --offline --wheel`, installed offline into its own Python 3.13.16
   venv with `ray==2.55.1` and `sqlalchemy==2.0.46`, and checked from `<scratch>/outside` with
   `assert_release.py` against `v0.2.2`'s wheel, and with `release_check.sh`.

None is committed.

**(a) `pyproject.toml`'s version left at `0.2.2`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -4,7 +4,7 @@
 
 [project]
 name = "datastorekit"
-version = "0.2.3"
+version = "0.2.2"
 description = "A sharded SQLite datastore layer (Datastore / ShardedPool) on Ray and SQLAlchemy"
 requires-python = ">=3.12"
 dependencies = [
```

The wheel is `datastorekit-0.2.2-py3-none-any.whl`, 99,186 bytes, 25 entries, none under `tests/`,
`METADATA` `Version: 0.2.2`.

```
wheel sha256: d2e05a5dd81a7c9a80d18f168eb6355ca2a27227484dadcf7c795d6abdeb32af
FAIL wheel name: datastorekit-0.2.2-py3-none-any.whl
FAIL METADATA Version: Version: 0.2.2
PASS no entry under datastorekit/tests/: 0 of 25 entries
PASS 25 entries: 25
PASS RECORD against v0.2.2: only SQL/factory_base.py differs: 20 and 20 lines under datastorekit/; differing: ['datastorekit/SQL/factory_base.py']
FAIL importlib.metadata.version: 0.2.2
PASS imported from site-packages: <scratch>/venv-break-a/lib/python3.13/site-packages/datastorekit/SQL/factory_base.py
PASS __abstractmethods__ is {register, build}: ['build', 'register']
PASS the three keep v0.2.2's signatures, static, not abstract: store staticmethod (obj, conn, table, inserter, tables, inserters) False
validate staticmethod (obj, conn, table, tables) False
validate_on_startup staticmethod (conn, table, tables, prune=False) False
PASS a subclass defining register and build instantiates; its three hooks raise bare NotImplementedError: instantiated F; store NotImplementedError (); validate NotImplementedError (); validate_on_startup NotImplementedError ()
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
PASS sharded_store --help exits 0: exit=0
RESULT: FAILED (3): wheel name, METADATA Version, importlib.metadata.version
```

**Verdict:** the `METADATA` and `importlib.metadata.version` assertions fail, naming `0.2.2`, as
§4.5 says; the wheel's name fails with them. The change is in the wheel (the `RECORD` differs from
`v0.2.2`'s in `SQL/factory_base.py`, and the base behaves as the release's): only the version is
wrong.

**(b) The `exclude` line removed from `pyproject.toml`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -14,4 +14,3 @@
 
 [tool.setuptools.packages.find]
 include = ["datastorekit*"]
-exclude = ["datastorekit.tests", "datastorekit.tests.*"]
```

The wheel is `datastorekit-0.2.3-py3-none-any.whl`, 314,368 bytes, **74 entries, 49 under
`datastorekit/tests/`** (`datastorekit/tests/__init__.py`, `client/instances.py`,
`test_factory_instances.py`, …).

```
wheel sha256: 1854771d221c69f326b3ee4125f7120db372b4cf663058abe823197779cc147f
PASS wheel name: datastorekit-0.2.3-py3-none-any.whl
PASS METADATA Version: Version: 0.2.3
FAIL no entry under datastorekit/tests/: 49 of 74 entries
FAIL 25 entries: 74
FAIL RECORD against v0.2.2: only SQL/factory_base.py differs: 20 and 69 lines under datastorekit/; differing: ['datastorekit/SQL/factory_base.py', 'datastorekit/tests/__init__.py', … 49 paths under datastorekit/tests/]
PASS importlib.metadata.version: 0.2.3
PASS imported from site-packages: <scratch>/venv-break-b/lib/python3.13/site-packages/datastorekit/SQL/factory_base.py
PASS __abstractmethods__ is {register, build}: ['build', 'register']
PASS the three keep v0.2.2's signatures, static, not abstract: store staticmethod (obj, conn, table, inserter, tables, inserters) False
validate staticmethod (obj, conn, table, tables) False
validate_on_startup staticmethod (conn, table, tables, prune=False) False
PASS a subclass defining register and build instantiates; its three hooks raise bare NotImplementedError: instantiated F; store NotImplementedError (); validate NotImplementedError (); validate_on_startup NotImplementedError ()
FAIL import datastorekit.tests fails: exit=0 (no error)
PASS sharded_store --help exits 0: exit=0
RESULT: FAILED (4): no entry under datastorekit/tests/, 25 entries, RECORD against v0.2.2: only SQL/factory_base.py differs, import datastorekit.tests fails
```

`import datastorekit.tests` resolves to `<scratch>/venv-break-b/lib/python3.13/site-packages/datastorekit/tests/__init__.py`.
**Verdict:** the wheel lists files under `datastorekit/tests/`, and `import datastorekit.tests`
succeeds. The counts are the orchestrator's: 74 entries, 49 under `tests/`.

**(c) The wheel built from `git archive v0.2.2` with only its version set to `0.2.3`.**

```diff
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -4,7 +4,7 @@
 
 [project]
 name = "datastorekit"
-version = "0.2.2"
+version = "0.2.3"
 description = "A sharded SQLite datastore layer (Datastore / ShardedPool) on Ray and SQLAlchemy"
 requires-python = ">=3.12"
 dependencies = [
```

Applied to an export of `v0.2.2`, where `git apply --check` and `-R --check` pass as recorded. The
wheel is `datastorekit-0.2.3-py3-none-any.whl`, 98,810 bytes, 25 entries, none under `tests/`,
`METADATA` `Version: 0.2.3`.

```
wheel sha256: ed8e263a94cf41fc8189b561cd9848d38a46de3245da9fa53a0c14996651a292
PASS wheel name: datastorekit-0.2.3-py3-none-any.whl
PASS METADATA Version: Version: 0.2.3
PASS no entry under datastorekit/tests/: 0 of 25 entries
PASS 25 entries: 25
FAIL RECORD against v0.2.2: only SQL/factory_base.py differs: 20 and 20 lines under datastorekit/; differing: none
PASS importlib.metadata.version: 0.2.3
PASS imported from site-packages: <scratch>/venv-break-c/lib/python3.13/site-packages/datastorekit/SQL/factory_base.py
FAIL __abstractmethods__ is {register, build}: ['build', 'register', 'store', 'validate', 'validate_on_startup']
FAIL the three keep v0.2.2's signatures, static, not abstract: store staticmethod (obj, conn, table, inserter, tables, inserters) True
validate staticmethod (obj, conn, table, tables) True
validate_on_startup staticmethod (conn, table, tables, prune=False) True
FAIL a subclass defining register and build instantiates; its three hooks raise bare NotImplementedError:  | TypeError: Can't instantiate abstract class F without an implementation for abstract methods 'store', 'validate', 'validate_on_startup'
PASS import datastorekit.tests fails: exit=1 ModuleNotFoundError: No module named 'datastorekit.tests'
PASS sharded_store --help exits 0: exit=0
RESULT: FAILED (4): RECORD against v0.2.2: only SQL/factory_base.py differs, __abstractmethods__ is {register, build}, the three keep v0.2.2's signatures, static, not abstract, a subclass defining register and build instantiates; its three hooks raise bare NotImplementedError
```

The release check's commands at (c): `__abstractmethods__: ['build', 'register', 'store',
'validate', 'validate_on_startup']`; `store`, `validate` and `validate_on_startup` each
`staticmethod`, with the same signatures as the release's, and `abstract`; and the subclass probe:

```
Traceback (most recent call last):
  File "<string>", line 7, in <module>
    f = F()
TypeError: Can't instantiate abstract class F without an implementation for abstract methods 'store', 'validate', 'validate_on_startup'
exit=1
```

The installed `factory_base.py` has five `@abstractmethod` lines (the release's two). **The 20
`RECORD` lines compared**, `v0.2.2`'s wheel against (c)'s: the same 20 paths, and every one the
same hash, `SQL/factory_base.py`'s included.

**Verdict:** `METADATA` says `0.2.3`, but the `RECORD` comparison shows no line differing where the
release shows `SQL/factory_base.py`'s, `__abstractmethods__` has five names, and the subclass
defining only `register` and `build` raises `TypeError`. The check catches a version number with
no change behind it.

---

## 7. Observations not acted on

1. **The earlier addenda's own tables now point N or k + N lines early** in this tree
   (correction 3). That is the reason for each `v0.2.3` addendum's sentence and table row. They are
   not rewritten (rule 6), and no issue is needed: the reader is told how to read them. Each
   release adds one more layer of this; a fourth addendum would add a third shift.
2. **SGK's `HEAD` moves while the campaign works** (§2 item 9). The SGK addendum names the commits
   read; a reader at a later SGK commit re-measures, as the checklist's head says.
3. **Several table rows in the new addenda, in the gates and in this log run past 100 columns**, as
   the earlier addenda's and the board's rows do. None is a defect.
4. **The scratch tools** are in `<scratch>/probe/`, not in the repository: `insert.py`,
   `measure_factories.py`, `check_shift.py`, `wheel_info.py`, `assert_release.py`,
   `release_check.sh`, `check_links.py`, `import_names.py` and `ast_base.py`. Their outputs are in
   `<scratch>/out/`; the exports, wheels, venvs, diffs and inserted texts are under `<scratch>`.
5. **`check_links.py`'s rule for a bare `:a-b`** is approximate (§5.5); the three it misread were
   checked by hand. Not a defect of the documents.

---

## 8. Issues

- **Opened:** none. **Closed:** none. **Narrowed:** none.
- This board's §3 holds no issue. The index is at **4 open**: 0 on this repository's boards and 4
  inherited.

---

## 9. State handed to the next prompt

- `HEAD` is this commit, unpushed and untagged. The tree is clean apart from dispatch's ignored
  entries. `venv/` has `datastorekit 0.2.3` installed editable from this checkout, its `egg-info`
  removed.
- **Not pushed, not tagged.** `origin/main` is `85f504d`, and the tags are `v0.1.0`, `v0.2.0`,
  `v0.2.1` and `v0.2.2`.
- **After the review**, this commit is pushed as `main`, fast-forwarding over `97c9a8e`, `f01c4e2`,
  `389e13b` and the review. `v0.2.3` is made on this commit, annotated, only once CI passes there at
  both ends (U23, U28). If CI fails, a fix prompt lands first, and no tag is made on a commit whose
  CI is red.
- **The suite is 504** in `venv/` and at the high end (0 and 4 `ResourceWarning` lines).
  `compare_ported_tests.py`: 20 modules and one test declared not ported, exit 0. `black --check
  datastorekit docs`: 74 files.
- **For the campaign's close:** every `v0.2.3` addendum's `datastorekit/` citation is at
  `f5d8957`'s tree, which `v0.2.3` will name. G2–G4 stay on the extraction board, recorded when
  each holds. The tag object and commit go to the user for CPBH's prompt 07, with README §0.2's
  four points.
- **Scratch** (not in the repository): `<scratch>`, holding `exports/` (`head-before`, `release`,
  `v022`, `high`, `break-a`, `break-b`, `break-c`), `wheels/`, the venvs (`venv-high-before`,
  `venv-high`, `venv-release`, `venv-break-a`, `-b`, `-c`), `breaks/` (the three diffs),
  `addenda/` (the inserted texts), `probe/` and `out/`.
