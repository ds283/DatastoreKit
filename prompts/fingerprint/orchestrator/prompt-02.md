# Orchestrator — prompt 02, release `v0.4.0`

Read [`../README.md`](../README.md) first: §0, §1, §2, §4, §5 (every rule), §6.1 and §6.2 (U1–U3
and U6), and §7. Then read [`prompt-01.md`](prompt-01.md), whose "Conventions" and §4–§5 this note
keeps unless it says otherwise, and `object-timestamp`'s
[`prompt-02.md`](../../object-timestamp/orchestrator/prompt-02.md), the note for the release this
one repeats: its §0, its additions, and its §5, which this note's §5 follows. Then read this board's
review of 01.

**You do not write code.** You may:
- run the suite, the port check, `black --check` and the guards;
- make venvs in the session scratchpad with `uv … --offline`, from the cache the extraction
  campaign filled, and nothing else: **no download**;
- export the tree with `git archive` into the scratchpad, and build wheels, run probes and replay
  breakages there, never in this checkout and never committing one;
- **start no Ray** (README §5 rule 7). No code changes, so the smoke script is not run;
- reach the network only for one `git ls-remote origin` at dispatch and one at the review, and for
  the pushes, the tag and the CI read of §5, each with the user's approval;
- read the three clients only through `git -C <client> rev-parse|status|show|grep|ls-tree|log|cat-file|merge-base`;
- fix small residue in a follow-up commit of your own (§4).

**The prompt:** [`02-release-v0.4.0.md`](../02-release-v0.4.0.md)
**Closes:** nothing · **Narrows:** nothing · **Changes:** nothing in the package but its version ·
**Opens:** only what the work finds · **Model:** Opus, as the prompt recommends.

**Gate:**
- 01 landed (`d1b61d6`) and was reviewed (`203ecd0`). **It is not pushed**: `origin/main` is
  `5f972be`, and CI has never run on 01's tree. 02 was written against `203ecd0` (`226d2e0`).
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- `git diff --stat d1b61d6 HEAD -- datastorekit docs pyproject.toml README.md PROVENANCE.md
  .github` is empty: everything 02 reads or edits, but the extraction board, is 01's tree. And
  `git diff --stat 2f5417e HEAD -- docs/adoption README.md PROVENANCE.md pyproject.toml .github`
  is empty: the files 02 edits are `v0.3.0`'s (both measured at `226d2e0`).
- `origin/main` is `5f972be` (`git ls-remote origin`, 2026-10-14), an ancestor of `main`, which is
  ahead of it by `6ef38f6`, `04a2ed9`, `7298262`, `df3fec9`, `d1b61d6`, `203ecd0`, `226d2e0` and
  this note. The tags are `v0.1.0` (`0ece4aa` → `68db557`), `v0.2.0` (`9eaf542` → `240028e`),
  `v0.2.1` (`0ba2e4d` → `33778b0`), `v0.2.2` (`c32d027` → `6d8ee9a`), `v0.2.3` (`8dac562` →
  `0de2b16`) and `v0.3.0` (`bf0a3b2` → `2f5417e`), here and on `origin`, and no other.
- The clients, read while this note was written (2026-10-14), as at 01's review:
  - SGK `a5a6f6d` (branch `handover-remedial`), clean; `requirements.txt:17` pins `v0.2.2`;
    `git diff --stat c8a7f14 a5a6f6d -- RunRegistry ObjectFactories` is empty;
  - CPBH `2792a85` (branch `read-only-plots`), 23 untracked entries; `requirements.txt:17` pins
    `v0.3.0`;
  - SI `5fb4a1d` (branch `dk-and-rpk-migration`), clean; no `datastorekit` line.

  SGK's and CPBH's `HEAD`s move under other sessions. A changed `HEAD` or status there is not this
  campaign's doing, and is recorded, not stopped on, unless the prompt's §6 fires at the `HEAD`
  read.
- This board's §3 holds no issue, and the index is **4** (all four on `inherited-issues`' board).
  It stays 4 unless the work opens an issue.
- No Ray process (`pgrep -lf 'gcs_server|raylet|ray::|default_worker\.py'` empty); `RAY_ADDRESS`
  and `RAY_ENABLE_AUTO_CONNECT` unset; no `/tmp/ray/ray_current_cluster`.
- One prompt at a time in this checkout. 02 is the campaign's last.

## 0. What makes this prompt unusual

**No line of code changes, so the suite cannot catch a bad edit.** It passes whatever the
documents say. What stands in for it, as at `object-timestamp` 02:
- the release check, from a clean export, which alone sees `0.4.0` and the module behind it;
- hazard 1's `git diff`, which must show `+` lines only under `docs/adoption/`;
- reading: every statement an addendum makes is true of `v0.4.0` and of the client at the commit
  it names, every statement it supersedes is named by `path:line`, and every name and link
  resolves.

**One client must act, and the note it reads is this prompt's.** For CPBH and SI nothing they call
changes. For SGK the release is its gate E1, and SGK's prompt 03 reads the SGK addendum item by
item (SGK README `:216` at `a5a6f6d`): every item must be either something SGK does or something
shown not to apply. So the SGK addendum's two halves must not blur: **moving the pin changes
nothing SGK calls**, and no SGK suite count changes; **calling the package's functions** (SGK's
06) changes seven things. Two of the seven were found writing 02 and are not in the plan: SGK's
production `fingerprint_store` passes `taken` positionally (`RunRegistry/stores.py:1500`), and
every fingerprint SGK already holds lacks `encoding_format`, so the package's comparison refuses
each, and `retire_store` with it. The addendum names SGK's options for the second and makes no
choice (hazard 8).

**The gates.** G2 (SGK, `v0.2.2` or later) and G3 (CPBH, `v0.2.3` or later) hold, and their
readings admit `v0.4.0`: unchanged. G4 reads "SI adopted `v0.3.0`"; U6 lets SI adopt `v0.3.0` or
`v0.4.0`, so G4 becomes "`v0.3.0` or later". SGK's E1 is SGK's board's.

**The push carries more than 02.** `origin/main` is `5f972be`. Pushing 02's commit as `main`
fast-forwards over the campaign's planning, 01 and its review, 02's writing, this note and 02. So
CI's run on 02's commit is **the first CI run on 01's code** (the module, its 21 tests and the
golden) as well as on the release. The tree CI tests is 02's.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-14 at `226d2e0` (whose
`datastorekit/`, `docs/`, `README.md`, `PROVENANCE.md` and `pyproject.toml` are `203ecd0`'s and,
under `datastorekit/` and `docs/client-contract.md`, `d1b61d6`'s), in `venv/`, in offline scratch
venvs and exports at the high end, with wheels built offline from exports, and by reading the
clients through `git`. Pass them on. Corrections 1 and 2 change what the agent writes, and are
STRUCTURALLY REQUIRED. Corrections 3 and 4 complete what the prompt states; the log records each
as found.

1. **How the earlier addenda's citations are read, with numbers.** The `v0.3.0` italic lines are
   `docs/adoption/README.md:22-25`, `secondarygwkit.md:33-37`, `champbh.md:34-38` and
   `stochasticinstantons.md:32-36`, each followed by one blank line; 02's italic line goes after
   that blank, so its insert is after `:26`, `:38`, `:39` and `:37`. The `v0.3.0` addenda each say
   their italic line added k lines (k = 5 in the README, 6 in each checklist), and read the
   `v0.2.3` addendum's citations k lines later, the `v0.2.2` addendum's 2k and the `v0.2.1`
   addendum's 3k. After 02's italic line of N lines (blank included):
   - the `v0.3.0` addendum's citations are read at `2f5417e`, or **N** lines later here, except
     those above the insert: the `v0.2.3` italic line it cites (`README.md:17-20`,
     `secondarygwkit.md:27-31`, `champbh.md:28-32`, `stochasticinstantons.md:26-30`). SI's rows
     for `:44-45` and later are below the insert, and shift;
   - the `v0.2.3` addendum's at `0de2b16`, or **k + N** lines later, except `README.md:12-15`,
     `secondarygwkit.md:21-25`, `champbh.md:22-26`, `stochasticinstantons.md:20-24`;
   - the `v0.2.2` addendum's at `6d8ee9a`, or **2k + N** lines later, except `README.md:7-10`,
     `secondarygwkit.md:16-19`, `champbh.md:17-20`, `stochasticinstantons.md:15-18`;
   - the `v0.2.1` addendum's at `33778b0`, or **3k + N** lines later, except `:3`, `:6`, `:6` and
     `:5` respectively.

   The agent states N, k + N, 2k + N and 3k + N for each file as numbers, and the review checks
   them against the file as committed.
2. **Exactly what each `v0.3.0` addendum says that `v0.4.0` supersedes, and what stands.** Read at
   `226d2e0`, before 02's insert (so N lines earlier than the file as 02 commits it). The prompt's
   table gives the pins; this is the full list the orchestrator found, and the agent checks each
   and records any it finds beyond it.
   - **README.** Superseded: the head line `:22-25` ("at the end", the pins by client); the pins
     `:486-501` (SI adopts `v0.3.0` and G4 reads "`v0.3.0`"; CPBH "may stay on `v0.2.3` or move to
     `v0.3.0`"; SGK "may stay on `v0.2.2` or move to `v0.2.3` or `v0.3.0`"); the carry-over
     sentence `:503-504`; the shift paragraph `:571-581`; and table rows `:584`, `:587`, `:588`,
     `:590`, `:592` (pins), `:589` (the `v0.2.2` shift), `:591` ("each checklist with its four
     addenda": at `v0.4.0` five) and `:593` (G2/G3/G4: G4 becomes "`v0.3.0` or later"; G2 and G3
     unchanged). **Stands:** `:595-597` (the module map's `DatastoreObject` row), and the
     addendum's account of `DatastoreObject.timestamp`, true of `v0.4.0`.
   - **SGK.** Superseded: the head line `:33-37`; the pin paragraph and its three code blocks
     `:643-663` (in part: "may stay on `v0.2.2` or move to `v0.2.3` or `v0.3.0`" becomes "adopts
     `v0.4.0` in place of `v0.2.2`, by its `runregistry-extraction` prompt 03"); the carry-over
     `:665`; the shift paragraph `:695-705`; rows `:707`–`:715`; and two rows the prompt's table
     does not name: **`:716`** ("at `v0.3.0` also the change of contract §9.6, which changes
     nothing SGK's calls use": at `v0.4.0` also §9.7's, which changes nothing SGK's calls use
     until SGK calls the package's functions, its 06), and **`:717`** (item 8's reasoning extended
     to `v0.3.0`: extended to `v0.4.0`, since nothing the layer reads changes). **Stands, not
     superseded:** G2's reading and holding (`:645-647`'s G2 sentence and the "Standing" paragraph
     `:719-722`), as `object-timestamp` 02's correction 2; and the "What changed for SGK since
     `v0.2.3`" account, true of `v0.4.0`.
   - **CPBH.** Superseded: the head line `:34-38`; the pin `:630-642` in part ("may stay on
     `v0.2.3` or move to `v0.3.0`": CPBH has adopted `v0.3.0`, G3 holding since 2026-10-13, and
     may stay or move to `v0.4.0`); the carry-over `:644-645`; the shift paragraph `:679-689`; rows
     `:691`–`:699` (`:699`, "with the four addenda"). **Stands:** G3's reading "`v0.2.3` or later"
     (`:632`, row `:700`), and the addendum's account of the object.
   - **SI.** Superseded: the head line `:32-36`; the pin and G4 `:595-601` ("SI adopts `v0.3.0`",
     G4 "SI has adopted `v0.3.0`": SI adopts `v0.3.0` or `v0.4.0`, G4 "`v0.3.0` or later"); the
     carry-over `:603-604`; the shift paragraph `:648-658`; rows `:668`, `:670`–`:673`, `:674`
     ("with the four addenda") and `:675` (G4). **Stands:** rows `:660` (head line), `:661`–`:667`
     (the `DatastoreObject.timestamp` statements, true of `v0.4.0`, whose `object.py` is
     `v0.3.0`'s), and `:635` (it "does not leave the layer").
3. **The extraction board's rows.** §2 is `prompts/extraction/IMPLEMENTATION_STATE.md:1532-1541`;
   G1–G4 are `:1536`–`:1539`. G4's title cell ends "(U37; `actor-names` U3; `factory-defaults` U5;
   `object-timestamp` U6)"; its status cell ends with the `v0.3.0` "is made" sentence, after which
   the new sentence goes.
4. **SGK's call sites, as the orchestrator's own measure found them** (below). The prompt's §1.1
   table is exact at SGK `a5a6f6d` and `c8a7f14`. `retire_store`'s test of a mismatch is
   `RunRegistry/tests/test_store_retire.py:460-479`; SGK's prompt 03's acceptance 3, which reads
   the note, is SGK README `:216`.

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says
so.

- **Work in this order:**
  1. the baseline: 530 in `venv/`, and at the high end from a fresh venv with an export of `HEAD`
     installed editable; the port check; `black --check datastorekit docs`, 78 files; the clients'
     `HEAD`s and statuses; §1.1's measure (hazard 4);
  2. `pyproject.toml`; `venv/`'s reinstall (hazard 6), the `egg-info` removed; the suite;
  3. `README.md` and `PROVENANCE.md`;
  4. the four addenda and italic lines; then hazard 1's `git diff`;
  5. the extraction board's G4;
  6. the release check; the high end;
  7. (a)–(c);
  8. the documents' check (§4.4) and the name-and-link check (hazard 2);
  9. `venv/`'s suite again, the port check, `black`, the clients again, the records.
- **Give each addendum's supersessions as a table** (`path:line`, the statement in brief, what
  replaces it), as the earlier addenda do, followed by a **"Standing, not superseded"** paragraph
  naming correction 2's standing statements. The log repeats the four tables.
- **The SGK addendum's shape.** Under its pin: a section **"What moving the pin changes: nothing
  SGK calls"**, then **"What changes when SGK calls the package's functions"**, the prompt's seven
  items numbered (1)–(7), each with SGK's `path:line` at `a5a6f6d`, checked by `git show`; under
  (3), SGK's options for the fingerprints it holds, as a list with what each touches (for
  instance: recompute each store's recorded fingerprint with the package's code, through SGK's
  own `store fingerprint --write`; or keep comparing a recorded fingerprint with SGK's own code
  until it is recomputed), and no choice made. Then a short table, "For SGK's prompt 03", of every
  item and whether it applies at the pin (03) or at the call (06). The addendum quotes neither of
  the package's refusal texts beyond what contract §9.7 states.
- **Placement.** In each checklist the `v0.3.0` addendum is preceded by a `---` rule
  (`secondarygwkit.md:633`, `champbh.md:620`, `stochasticinstantons.md:585`) and followed by one
  before the appendix (`:724`, `:702`, `:677`). The `v0.4.0` addendum goes after the `v0.3.0`
  addendum's last paragraph and before that second rule, with a `---` of its own above it. In the
  README it goes at the end (the `v0.3.0` addendum ends the file at `:597`), after a `---`. Its
  heading is `## Addendum: v0.4.0 (fingerprint prompt 02, <date>)`; by GitHub's rule the anchor is
  `#addendum-v040-fingerprint-prompt-02-<yyyy-mm-dd>`.
- **The README addendum's table of §1.1.** One row per client, with the commit read, its pin, what
  it defines and what it calls, as the prompt's §1.1 table; SGK's call sites summarised by count
  and file, with the two positional `taken` calls named.
- **`PROVENANCE.md`'s new section is a `###`**, as `:89`, `:118`, `:160`, `:205` and `:242` are,
  under "After `v0.1.0`", after the `object-timestamp` section, which ends the file at `:272`.
- **The contract's anchors**, by GitHub's rule (lower-case; drop backticks and punctuation other
  than hyphens; spaces to hyphens): §9.7 "9.7 `fingerprint` prompt 01"
  (`docs/client-contract.md:372`) is `#97-fingerprint-prompt-01`; §9 is `#9-changes-after-v020`,
  as `README.md:137` already links it; §4 "4. The inventory's declarations" (`:143`) is
  `#4-the-inventorys-declarations`. From `docs/adoption/` the path is `../client-contract.md#…`;
  from the root, `docs/client-contract.md#…`.
- **The gate title**, exactly: G4 "SI adopted `v0.3.0` or later (U37; `actor-names` U3;
  `factory-defaults` U5; `object-timestamp` U6; `fingerprint` U6)". Its status cell gains one dated
  italic sentence at its end, in the form of the `v0.3.0` "ready to be tagged" sentence, linking
  SI's new addendum by anchor, and saying that SI may adopt `v0.3.0` or `v0.4.0` (U6). G1, G2 and
  G3's rows and everything else on that board, its header included, are unchanged.
- **Keep the name-and-link check as a scratch script**, never committed: every relative link and
  anchor in `README.md`, `PROVENANCE.md`, the four adoption files and the extraction board's §2,
  each file resolved and each anchor found among its target's headings by GitHub's rule; every
  dotted `datastorekit.` name imported in `venv/`.
- **Build (a)'s, (b)'s and (c)'s wheels from their own exports**, each with the prompt's change
  and only that. Record (a) and (b) as diffs to `pyproject.toml` that `git apply --check` and `-R
  --check` accept against an export of the commit; (c) is the version line applied to an export of
  `v0.3.0`, and is recorded so that it applies there. Run the release probe in each wheel's venv,
  and record each output.
- **§1.1's measure.** The orchestrator's own, a script of `ast` reads from `git show` run with
  `python3 -I`, gave the prompt's table exactly (below). The agent writes its own, and records its
  essentials and its output.

**The facts, checked by the orchestrator.** Pass them on.

- **The suite** at `226d2e0`: `Ran 530 tests … OK` in `venv/` (104 s), 0 `ResourceWarning` lines;
  and at the high end from a fresh offline venv with an export installed editable
  (`--no-deps --no-build-isolation`), run from the export's root (`datastorekit.__file__` under
  it), `Ran 530 tests … OK` (106 s), 0 `ResourceWarning` lines. The port check exits 0 ("OK: 20
  module(s) … 1 test(s) declared not ported"); `black --check datastorekit docs` leaves 78 files
  unchanged. `venv/` has no `setuptools` (`import setuptools` raises `ModuleNotFoundError`), so
  hazard 6's form, without `--no-build-isolation`, is the one that runs.
- **§1.1 reproduces**, read through `git` at SGK `a5a6f6d` and `c8a7f14`, CPBH `2792a85` and SI
  `5fb4a1d`, outside `prompts/`, `.prompts/`, `docs/` and `.documents/`:
  - SGK, both commits: one `def` each of `fingerprint_of(inventory, taken)`
    (`RunRegistry/stores.py:1182`), `compare_fingerprints(recorded, current)` (`:1256`) and
    `listing_lines(inventory, fingerprint)` (`:1376`); `fingerprint_of` called 10 times, 2 with two
    positional arguments (`stores.py:1500`, `tests/test_store_fingerprint.py:378`) and 8 with one,
    none by keyword; `compare_fingerprints` 9 times, each two positional; `listing_lines` once
    (`stores.py:1432`);
  - CPBH and SI: none of the three defined or called.
  - `fingerprint_store` (`stores.py:1500-1508`) passes the inventory and a `taken` dict literal
    positionally; its comparison is `stores.py:1510-1529`, with `_fingerprint_problems`
    (`:416-437`) checking four keys and allowing others. `TestGolden` is `:347-382`
    (`test_the_golden_fingerprint` `:350-356`, `test_the_shape` `:358-374`, the positional call in
    `test_taken_is_outside_every_digest` `:376-381`); `TestFormats` `:434-457`; `parse_listing`
    `:114-136`.
- **The package.** `git diff --stat 2f5417e d1b61d6 -- datastorekit`: the module (351 lines), its
  test module (711) and the golden (193), all added. `git diff --stat v0.2.2 d1b61d6 --
  datastorekit/store_inventory.py` is empty. Only `pyproject.toml:7` carries the version.
- **§1.2 reproduces.** From a `git archive` of `203ecd0` (whose tree under everything 02 reads is
  `226d2e0`'s) with only `version = "0.4.0"`, `uv build --offline --wheel` gives
  `datastorekit-0.4.0-py3-none-any.whl`, 104,424 bytes (not reproducible; compare `RECORD` lines,
  not hashes):
  - 26 entries, none under `datastorekit/tests/`; `datastorekit-0.4.0.dist-info/licenses/LICENSE`;
  - `METADATA`: `Version: 0.4.0`, `Requires-Python: >=3.12`, `Requires-Dist: ray>=2.43`,
    `Requires-Dist: sqlalchemy<2.1,>=2.0.39`;
  - installed offline with `ray==2.55.1` and `sqlalchemy==2.0.46` into a Python 3.13.16 venv
    (SQLite 3.53.4) and run from a directory outside the repository with `PYTHONPATH` unset and
    `python -I`: the package imports from `site-packages`; the metadata version is `0.4.0`;
    `ENCODING_FORMAT` is `1`; the signature is as the prompt says, `fingerprint_format`
    `POSITIONAL_OR_KEYWORD` with no default; on a hand-built two-class inventory, the six keys,
    `encoding_format` 1, the digest recomputed equal, keyword equal to positional, format 6 a
    different digest with `classes` equal; `True`, `"1"`, `1.0` and a dict each `TypeError:
    fingerprint_of(): fingerprint_format must be an int, not <type> <value>`, `0` `ValueError: …
    must be at least 1, not 0`, missing `TypeError: fingerprint_of() missing 1 required positional
    argument: 'fingerprint_format'`; against a copy without `encoding_format`, `[("encoding", None,
    1)]`; against one with a `taken`, `[]`; the listing's first line `# fingerprint_format 1 digest
    <d> encoding_format 1`, words 2, 4 and 6 as the prompt says; `ray` not in `sys.modules` after
    the probe, nor in a fresh interpreter after `import datastorekit.store_fingerprint`; `import
    datastorekit.tests` raises `ModuleNotFoundError`; `python -m datastorekit.tools.sharded_store
    --help` exits 0. No Ray process after.
  - Against `git archive v0.3.0`'s wheel (99,488 bytes, 25 entries): its 20 `RECORD` lines under
    `datastorekit/` are each in the release's unchanged, and the release adds one,
    `datastorekit/store_fingerprint.py,sha256=OIGFxRU6LPEKr_W4zngOqHPSPwQCtT28T-aX4kVvcNg,16093`.
- **The breakages**, each from its own export:

  | | Change | Measured |
  |---|---|---|
  | (a) | version left at `0.3.0` | `METADATA` `Version: 0.3.0`, 26 entries; its `RECORD` differs from `v0.3.0`'s wheel's only by `store_fingerprint.py`'s line: the version alone is wrong |
  | (b) | `exclude = ["datastorekit.tests", "datastorekit.tests.*"]` deleted (`pyproject.toml:17`) | 78 entries, 52 under `datastorekit/tests/` (the golden `.json` not among them); `import datastorekit.tests` succeeds from `site-packages` |
  | (c) | `v0.3.0`'s tree at `0.4.0` | `Version: 0.4.0`, 25 entries; all 20 `RECORD` lines under `datastorekit/` equal `v0.3.0`'s, none added; `import datastorekit.store_fingerprint` raises `ModuleNotFoundError` |

- **The line numbers the prompt cites hold at `226d2e0`**, with corrections 1–4's readings:
  `README.md:10-18`, `:93`, `:96-99`, `:122-123`, `:131-137`; `PROVENANCE.md:242` (the file is 272
  lines, and that section is its last); the italic lines and appendices
  (`secondarygwkit.md:726`, `champbh.md:704`, `stochasticinstantons.md:679`); the README addendum
  ending the file at `:597`; SGK item 9 `:322-354` and item 10 `:356-378`; the SGK, CPBH and SI pin
  paragraphs `:643`, `:630`, `:595`; the README's module map `:87`, `:94`; contract §9.7 at `:372`.
- **The toolchain.** `venv/`: Python 3.12.15, Ray 2.43.0, SQLAlchemy 2.0.39, SQLite 3.53.4,
  `black` 25.1.0, `datastorekit 0.3.0` editable from this checkout, no `setuptools`. `uv` 0.12.20.
  The high end, `uv venv --offline -p /opt/local/bin/python3.13`: 3.13.16, 2.55.1, 2.0.46, SQLite
  3.53.4.
- **Expected counts.**
  - The suite: **530**, before and after, at both ends; 0 `ResourceWarning` lines in `venv/`, 0
    or 4 at the high end (timing).
  - `compare_ported_tests.py`: exit 0, "20 module(s) … 1 test(s) declared not ported".
  - `black --check datastorekit docs`: **78** files, before and after.
  - The index: **4**, unchanged unless the work opens an issue.
- **Ray.** None up. Nothing in this prompt calls one of Ray's auto-init APIs: the release probes
  build an inventory by hand, fingerprint it and run `sharded_store --help` only.

**What the review exists to establish.**
- **(E1) Scope.** Only the prompt's §7 files change. Nothing under `datastorekit/`, and not the
  contract, the verification document, `docs/extraction/` or the workflow.
- **(E2) The release.** A wheel from a clean export of the commit is `0.4.0`, holds 01's module and
  no tests, and behaves as §1.2 says from outside the repository.
- **(E3) The documents.** `pyproject.toml`, `README.md` and `PROVENANCE.md` as §2.1–§2.3 say; the
  change stated as added API that the layer neither writes nor reads; U6's pins exactly, advising
  CPBH and SI neither way; nothing says `v0.4.0` is tagged; every name and link resolves.
- **(E4) The addenda.** Each additive, dated and placed as the additions say; each states its pin,
  what changed for its client, what it supersedes by `path:line` and what stands (corrections 1
  and 2), true at the file. **The SGK addendum** separates the pin from the call, carries the
  seven items with true SGK citations, and names SGK's options without choosing.
- **(E5) Both ends.** 530 in `venv/` (now `0.4.0`) and at the high end.
- **(E6) The breakages.** (a)–(c) fail as recorded.
- **(E7) The records**, and the extraction board's G4.

**Conventions.** `object-timestamp` 02's note's, and all bind the agent:
- stage by explicit path, and show `git diff --cached --name-only` before committing;
- write "this commit" for the SHA;
- run the suite in the foreground, with its output written to a scratch file and the verdict
  grepped from it;
- check each breakage diff **as recorded in the log** with `git apply --check` and `-R --check`
  against a scratch export;
- read a client only through `git`, and never import or run its code;
- use a subdirectory of the session scratchpad, never `/tmp`, for venvs, exports, wheels and
  probes; put no scratch `.py` under `datastorekit/` or `docs/`;
- run every scratch-venv command with its export, or a directory outside the repository, as the
  working directory (the prompt's hazard 9);
- a stop goes to the user, through the orchestrator;
- check `git log` before committing.

And for this prompt:
- **Start no Ray.** Nothing calls `ray.init`, `ray.kill`, `ray.get` or any other of Ray's auto-init
  APIs outside the suite.
- **No download of any kind.** Every venv and build is `--offline`.
- **Nothing is built in the checkout** but `venv/`'s editable reinstall, whose `egg-info` is
  removed.
- **No push, no tag, and no change to the GitHub repository's settings.**

## 1. Before you dispatch

1. **The tree.** Record the branch and `HEAD`. `git status --short` and `git diff --cached` must
   be empty, and `git worktree list` must show this checkout alone. Record `git status --short
   --ignored` (at writing: `.idea/`, `venv/` and five `__pycache__/` directories, one of them
   `docs/extraction/__pycache__/`).
2. **The baseline.** In `venv/`, `Ran 530 tests … OK` with no `ResourceWarning`; the port check
   exits 0; `black --check datastorekit docs` leaves 78 files unchanged; `pip show datastorekit`
   says `0.3.0`. (Taken at writing; re-take only if `HEAD` has moved outside `prompts/`.)
3. **The clients.** Each `HEAD` and `git status --short`, recorded.
4. **The remote.** `git ls-remote origin`: `main` at `5f972be…` and the six tags as the gate says.
5. **Ray.** No Ray process; `RAY_ADDRESS` and `RAY_ENABLE_AUTO_CONNECT` unset.
6. **The index.** 4 now, and 4 after unless the work opens an issue. Tell the agent both.

## 2. Dispatch

Dispatch one fresh-context subagent, on **Opus**, in this checkout. Give it:
- the prompt, the campaign README, this board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`,
  `PROVENANCE.md`, log 01 (§1, §6 and §8), `object-timestamp` prompt 02 and its log;
- `HEAD`, the clients' `HEAD`s and statuses, the counts and the index count;
- §0 of this note, up to "## 1. Before you dispatch" only, as a copy in the session scratchpad.
  The agent does not read `orchestrator/`.

Tell it that the prompt governs, with §0's four corrections and its additions. Correction 2 is the
one that would have it supersede a statement that is still true (G2, G3, SI's object rows), or
miss two SGK rows (`:716`, `:717`). The SGK addendum is the note SGK's prompt 03 reads item by
item: the two halves, pin and call, must not blur.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/02-release-v0.4.0.md`, in README §5.1's form, with
  the prompt's §5 item 6 additions.
- **The files it may change are the prompt's §7 list, and nothing else.** It must not touch:
  - anything under `datastorekit/`;
  - `docs/client-contract.md`, `docs/extraction-verification.md`, `docs/extraction/` or the
    workflow;
  - `CLAUDE.md`, `LICENSE` or `.gitignore`;
  - on the extraction board, anything but G4's row;
  - anything under `orchestrator/`.
- **Under `docs/adoption/` it adds lines only.**
- **It writes nothing in any client repository, and runs, imports or opens nothing of one.**
- **It downloads nothing, and starts no Ray.**
- **It pushes nothing, makes no tag, and changes no setting of the GitHub repository.**
- **Stop and ask** on any of the prompt's §6 conditions.

## 3. The review — ten checks

Make the review's venvs, exports and wheels fresh, offline, in a subdirectory of the scratchpad of
their own, not the agent's.

1. **Scope (E1).** `git show --stat <commit>` touches only `pyproject.toml`, `README.md`,
   `PROVENANCE.md`, the four files under `docs/adoption/`, the extraction board, the log, this
   board, the campaign README, `prompts/INDEX.md`, and `docs/OPEN_ISSUES.md` only if an issue is
   opened. `git diff <parent> <commit> -- datastorekit docs/client-contract.md
   docs/extraction-verification.md docs/extraction .github CLAUDE.md` is empty. No wheel,
   `dist/`, `build/`, `*.egg-info` or scratch file; `git status --short --ignored` as at dispatch.
   Each client's `HEAD` and status recorded.
2. **Additive (E1, E4).** `git diff <parent> <commit> -- docs/adoption/` has no `-` line.
   `pyproject.toml`'s diff is the version line alone. The extraction board's diff is G4's row
   alone, keeping every sentence it had.
3. **The release (E2).** From `git archive <commit>`, build the wheel offline and install it into a
   fresh high-end venv, offline. Check §1.2's facts as the facts above give them: 26 entries, none
   under `tests/`; the licence; `METADATA`; from outside the repository, `0.4.0`,
   `ENCODING_FORMAT`, the signature, the hand-built inventory's fingerprint, digest, refusals,
   comparison and listing, no `ray` loaded, `datastorekit.tests` refused, `sharded_store --help`.
   The `RECORD` comparison with the review's own `v0.3.0` wheel: the 20 lines equal, and only
   `store_fingerprint.py`'s added, with the hash above. Compare the wheel's file list with the
   log's.
4. **`README.md` and `PROVENANCE.md`, by reading (E3).**
   - Status: a `v0.4.0` paragraph above `v0.3.0`'s, which is unchanged, saying what §2.2 lists and
     linking §9.7 by anchor.
   - The pin is `v0.4.0`; the sentence replacing `:96-99` says the six earlier tags remain, none
     moved or deleted, that SecondaryGWKit adopts `v0.4.0`, and that ChamPBH may stay on `v0.3.0`
     and StochasticInstantons adopt `v0.3.0`, or either move, as it chooses. It names no client
     path, advises neither way, and nothing says `v0.4.0` is tagged.
   - "Using it": the store-fingerprint item, and "What changed after `v0.2.0`" with `v0.4.0`'s
     change, still linking §9.
   - `PROVENANCE.md`'s new `###` section follows the `object-timestamp` section; it names the
     source (SGK `RunRegistry/stores.py:1164-1400` at `c8a7f14`, the extract's full SHA-256), the
     ruling, the differences by decision, the equivalence check's result, and 01's files and log.
     Nothing above it changes.
5. **The addenda, by reading (E4).** For each of the four files:
   - the italic line is after `object-timestamp` 02's; the addendum is placed as the additions
     say, unnumbered, dated, and names `fingerprint` prompt 02;
   - it gives its pin per U6, with `object-timestamp` U6 amended for G4 and kept for G2 and G3;
   - what it says changed for its client is true of `d1b61d6`'s package and of the client at the
     commit it names, and links §9.7;
   - each superseded statement is cited by a `path:line` that holds in the file as committed, and
     each standing one of correction 2 is named as standing, not superseded;
   - correction 1's sentence is there, with N, k + N, 2k + N and 3k + N as numbers, each equal to
     the lines the italic lines added;
   - **SGK's**: the pin and the call kept apart; the seven items, each SGK citation checked by the
     review with `git show a5a6f6d:<path>`; the two positional `taken` calls named; the
     fingerprints SGK holds, with its options and no choice; the "For SGK's prompt 03" table;
     G2 standing; rows `:716` and `:717` superseded (correction 2);
   - CPBH's and SI's say nothing changes that they call, with no instruction to either; SI's
     supersedes G4 and leaves its object rows standing.
6. **Names and links, by running (E3, E4).** The review's own extraction of every relative link
   and anchor in the six documents and the extraction board's §2: each file exists, and each anchor
   is a heading by GitHub's rule. Every dotted `datastorekit.` name imports in the review's release
   venv. The list matches the log's.
7. **Both ends (E5).** In `venv/`: `pip show datastorekit` says `0.4.0`; `Ran 530 tests … OK`; no
   `datastorekit.egg-info/` at the root. In a fresh high-end venv with `git archive <commit>`
   installed editable: `Ran 530 tests … OK`, with the `ResourceWarning` lines counted (0 or 4). The
   port check exits 0. `black --check datastorekit docs` leaves 78 files unchanged.
8. **The breakages (E6).** Replay (a)–(c) as the log records them, each in its own export, against
   the facts' table. (c) must show all 20 `RECORD` lines equal to `v0.3.0`'s, none added, and
   `ModuleNotFoundError` on the module.
9. **The records (E7).**
   - The log: every section of README §5.1, with the release check, the documents' check (§4.4),
     every name and link, §1.1's measure re-run, (a)–(c), the clients at both ends, the four
     corrections and the additions, and each addendum's supersession table.
   - The extraction board: G4 as the additions say; the rest unchanged.
   - This board: 02's row (landed, commit, log) and the header. The README's header and §2 row;
     `prompts/INDEX.md`'s line. `docs/OPEN_ISSUES.md` unchanged at 4, or as opened.
10. **Nothing left behind.** No Ray process. `git tag -l` is the six tags, and `origin` is
    unchanged.

## 4. After the review

- **Record it on the board** as a §1 *Orchestrator review of prompt 02* paragraph, in the form of
  01's. Fix small residue in a follow-up commit of its own:
  - "this commit" → the SHA, on this board, the extraction board, the log, the README and
    `prompts/INDEX.md`;
  - "reviewed; awaiting CI for `v0.4.0`" for 02 in this board's header and row, README §2 and
    `prompts/INDEX.md`;
  - the notes line, with this note marked "used for 02".
- Anything the review finds that is not residue is opened on this board's §3 and in the index.
  **An issue open against 02's commit is a stop for the tag**: tell the user, and nothing in §5
  runs until they decide.
- **Report to the user:**
  - what landed: `0.4.0`, the README, `PROVENANCE.md`, the four addenda and G4;
  - the release check and its `RECORD` comparison, and the 530 at both ends, from the review's own
    venvs;
  - §1.1's measure, re-run, and the two SGK findings the addendum carries;
  - (a)–(c);
  - that the push carries 01 and the campaign's records with 02, so CI's run is the first on 01's
    code (§0);
  - **and ask for approval to push 02's commit** (§5).

## 5. Reaching `v0.4.0`

`object-timestamp` 02's note §5, with `v0.4.0` for `v0.3.0`, 02's commit for that 02's, and
`5f972be` for `75c237e`. Each push and the tag is an outward-facing act: **ask the user, and wait
for a clear yes, before each.** Approval of one is not approval of the next.

1. **Push 02's commit as `main`:** `git push origin <02's SHA>:refs/heads/main`. It fast-forwards
   from `5f972be`. The workflow runs on 02's commit at both ends; the smoke script is not
   collected, so CI starts no Ray.
2. **Read the run** once it has finished: `gh run list --workflow tests.yml --commit <02's SHA>`
   and `gh run view <id> --log`. Do not poll: ask the user to say when it has finished, or check
   once when they return. From each job's log, record the versions it prints (SQLite's among
   them), the suite's verdict (`Ran 530 tests … OK`) and black's line on `low`.
3. **If either end fails**, stop. No tag. Record the failure on this board's §3 with the job's log
   lines, open it in the index, and tell the user that a fix prompt is needed. A failure in 01's
   tests is 01's, found late because 01 was not pushed alone; it is recorded the same way. The tag
   goes on the fix's commit once its CI passes.
4. **If both pass**, with the user's approval:
   - `git tag -a v0.4.0 <02's SHA> -m "datastorekit 0.4.0: the store fingerprint (datastorekit.store_fingerprint), with the client's format as an argument and the package's ENCODING_FORMAT beside the digest"`;
   - `git push origin v0.4.0`;
   - check that `git ls-remote origin refs/tags/v0.4.0^{}` is 02's SHA.
5. **Record it, and close the campaign** (the prompt's §8), in a records commit of its own:
   - the extraction board's G4: one dated italic sentence, in the form of the `v0.3.0` "is made"
     sentences: `v0.4.0` made, annotated, on 02's SHA, the tag object, the run's URL and both
     ends' versions and counts; that SI may adopt `v0.3.0` or `v0.4.0` (U6). G1–G3 are unchanged;
   - this board: the review paragraph's last line, 02's row, the header (**CLOSED**), and §2:
     the tag for SGK's E1;
   - the campaign README's header and §2 row, and `prompts/INDEX.md`'s line: closed, with the
     tag; the count in `docs/OPEN_ISSUES.md` unchanged;
   - then **push the rest of `main`** (`git push origin main`), with approval.
6. **Hand the user**, for SGK's gate E1: the tag object and commit; the SGK addendum's anchor
   (`docs/adoption/secondarygwkit.md#addendum-v040-fingerprint-prompt-02-<date>`); README §0.2's
   six points to report back to the SGK session; and the two the prompt's §8 adds (SGK's
   `fingerprint_store` passes `taken` positionally, `RunRegistry/stores.py:1500`; every
   fingerprint SGK holds lacks `encoding_format`, and the package's comparison refuses each until
   it is recomputed).

**Hand on.** `v0.4.0` is on 02's commit once §5 has run. SGK adopts it in its `runregistry-extraction`
prompt 03 and calls it in 06; its R1 (04) takes the fingerprint both ways, and its result is
recorded on this board when SGK reports it (README §7), a difference opened here as a defect. CPBH
may stay on `v0.3.0` and SI adopt `v0.3.0`, or either move (U6), each in a campaign of its own, in
its own repository; G4 is recorded on the extraction board when it holds. No campaign of this
repository is open after this one but `inherited-issues`' board, which has no prompts.
