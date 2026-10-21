# Orchestrator — prompt 02, release `v0.5.0`

Read [`../README.md`](../README.md) first: §0 (§0.1–§0.3), §1, §2, §4, §5 (every rule), §6.1, §6.2
(U1–U3, and U5 with its amendment) and §7. Then read [`prompt-01.md`](prompt-01.md), whose
"Conventions" and §4–§5 this note keeps unless it says otherwise, and `fingerprint`'s
[`prompt-02.md`](../../fingerprint/orchestrator/prompt-02.md), the note for the release this one
repeats: its §0, its additions, and its §3–§5. Then read this board's review of 01 and its §3.

**You do not write code.** You may:
- run the suite, the port check, `black --check` and the guards;
- make venvs in the session scratchpad with `uv … --offline`, from the cache, and nothing else:
  **no download**;
- export the tree with `git archive` into the scratchpad, and build wheels, run probes and replay
  breakages there, never in this checkout and never committing one;
- **start no Ray** (README §5 rule 7);
- reach the network only for one `git ls-remote origin` at dispatch and one at the review, and for
  the pushes, the tag and the CI read of §5, each with the user's approval;
- read the three clients and RunRegistryKit only through `git -C <repo> rev-parse|status|show|grep|ls-tree|log`;
- fix small residue in a follow-up commit of your own (§4).

**The prompt:** [`02-release-v0.5.0.md`](../02-release-v0.5.0.md)
**Closes:** `[01-a-new-spec-field-moves-every-spec-guard-digest]` · **Changes:** nothing in the
package but its version · **Opens:** only what the work finds · **Model:** Opus, as the prompt
recommends.

**Gate:**
- 01 landed (`5475cef`), was reviewed (`dde3201`), and is pushed with CI green at both ends (run
  39680233763, on `dde3201`). 02 was written against `c583c56` (`bda6dbc`), with U5 amended by the
  user.
- `HEAD` here is the commit that adds this note, or a later one that touches only `prompts/` or
  `docs/OPEN_ISSUES.md`. If a later commit touches anything else, re-check every fact below that
  it could move, and hand the agent the corrections as an addendum.
- `git diff --stat 5475cef HEAD -- datastorekit docs/client-contract.md docs/adoption pyproject.toml
  README.md PROVENANCE.md .github` is empty.
- `origin/main` is `bda6dbc` (pushed 2026-10-21, with the user's approval), and `main` is ahead of
  it by this note only. The tags are the seven, `v0.1.0` to `v0.4.0` (`8e7c1d7` → `c8570e8`), here
  and on `origin`, and no other.
- The clients, read 2026-10-21, each clean and as at 02's writing: SGK `031bcb4`
  (`handover-remedial`), CPBH `7055532` (`jordan-normalization`), SI `f5f395b`
  (`dk-and-rpk-migration`), each pinning `v0.4.0`. RunRegistryKit `33a2cd2` (`main`), clean, tags
  `v0.1.0` and `v0.2.0`. A changed `HEAD` there is recorded, not stopped on, unless the prompt's §6
  fires at the `HEAD` read.
- The index is **5**: four on `inherited-issues`, one here, assigned to 02. After 02 it is **4**.
- No Ray process; `RAY_ADDRESS` unset.
- One prompt at a time in this checkout. 02 is the campaign's last.

## 0. What makes this prompt unusual

**No line of code changes, so the suite cannot catch a bad edit.** What stands in for it, as at
`fingerprint` 02: the release check from a clean export; hazard 1's `git diff`, `+` lines only under
`docs/adoption/`; and reading, that every statement is true of `v0.5.0` and of the client at the
commit it names, and that every superseded statement is named by `path:line`.

**Two addenda carry a fact the plan did not have.** SGK's and ChamPBH's must say that nothing they
call or hold changes, **and** that their spec guard fails on the move unless `plain` leaves out an
empty `extra_values`, and that the format is not bumped for it. The edit is shown on the neutral
registry and on hand-built specs in the wheels, never by running a client (hazard 5). SI's addendum
is the note SI's pin prompt reads: what to declare, where, and what of SI's own tests moves.

**Unlike `fingerprint` 02, the code is already pushed and CI-green.** The push after this review
carries only 02 and its records; CI's run on 02's commit is the tag's gate.

**What moves on purpose:** the prompt's §7 list, and nothing else.

**Corrections to the prompt**, checked by the orchestrator on 2026-10-21 at `bda6dbc`, with wheels
built offline from exports and installed at the high end, and by reading the clients through `git`.
Pass them on. Correction 1 changes what the agent writes, and is STRUCTURALLY REQUIRED; corrections
2 and 3 complete what the prompt states.

1. **How the earlier addenda's citations are read, with numbers.** The `v0.4.0` italic lines are
   `docs/adoption/README.md:27-30`, `secondarygwkit.md:39-43`, `champbh.md:40-44` and
   `stochasticinstantons.md:38-42`, each followed by one blank line, so each `v0.4.0` addendum's own
   k (its italic line and the blank) is **5** in the README and **6** in each checklist. 02's italic
   line goes after that blank (after `:31`, `:44`, `:45` and `:43`). With 02's N lines (blank
   included), the `v0.4.0` addendum's citations are read at `c8570e8`, or **N** lines later here,
   except those above the insert (its citations of the `v0.3.0` head line); the `v0.3.0`
   addendum's at `2f5417e`, or **k + N** later; and so on, each earlier one k more, as that addendum
   states. The agent states each shift as a number per file, and the review checks them.
2. **The `v0.4.0` addenda's statements of a client's pin are history now.** Each says what the
   client's `requirements.txt` pinned then (SGK `:754`, "pins `v0.2.2`"; CPBH `:719`, "pins it at
   `2792a85`" for `v0.3.0`; SGK's table row `:899`). Every client has since pinned `v0.4.0` (SGK
   `5b81f2e`, CPBH `f41b104`, SI `1b1ca6d`, each by `git log -- requirements.txt`). Supersede those
   by `path:line` with the pin read at the commit §1.1 names. SGK's `v0.4.0` account of what
   changes when SGK calls the package's functions (its 06, since done) is true of `v0.4.0` and of
   `v0.5.0`, and **stands**: 02 does not re-measure SGK's adoption of `v0.4.0`.
3. **The release check, measured.** As prompt §1.2, and:
   - **(b)** with the `exclude` line removed, the wheel has **79** entries, **53** under
     `datastorekit/tests/` (one more test module than at `v0.4.0`'s 78 and 52);
   - **(c)** a wheel from `git archive v0.4.0` with only its version set to `0.5.0`: 26 entries,
     `METADATA` `Version: 0.5.0`, and **no** `RECORD` line under `datastorekit/` differing from or
     added to `v0.4.0`'s;
   - the cache's constraints file must lose its `datastorekit` line before a `0.5.0` wheel will
     install (the prompt says so; measured: `uv` refuses with "you require datastorekit<=0.4.0").

**Additions.** Each is an IMPLEMENTATION CHOICE at the orchestrator's direction, and the log says so.
- **Work in this order:** the baseline (538 in `venv/`; the port check; `black`, 79 files; the
  clients and RunRegistryKit; Ray); §1.1's measure re-run (hazard 4); the release check and its
  breakages, **before** the documents, so that each addendum is written from a measured release;
  §2.1–§2.6; `venv/`'s reinstall (hazard 7) and the suite at both ends; the records.
- **The probe in the log.** Keep the probe script whole in the log, with its output from both
  venvs, as `fingerprint` log 02 §5.3 did. Its guard check copies RunRegistryKit's `plain` and
  `spec_digests` from `git show v0.2.0:docs/adoption/README.md`, adds the one condition as a
  separate function, and asserts both outcomes.
- **Quote the clients' `plain` from `git show`**, at the commits §1.1 names, and show by `diff`
  against RunRegistryKit's recipe that each is the recipe (docstring aside).
- **Anchors.** `9.8 \`extra-values\` prompt 01` → `#98-extra-values-prompt-01`; each new addendum's
  `## Addendum: v0.5.0 (extra-values prompt 02, 2026-10-21)` →
  `#addendum-v050-extra-values-prompt-02-2026-10-21`. The agent derives both by GitHub's rule and
  says how.

**The facts, checked by the orchestrator.** Pass them on.
- **The suite** at `5475cef`'s tree: `Ran 538 tests … OK` in `venv/` (0 `ResourceWarning` lines)
  and in an offline Python 3.13.16 venv (4 lines), at 01's review; CI the same at both ends.
- **The wheels**: the release 105,087 bytes, 26 entries; `v0.4.0`'s 104,424 bytes, 26 entries; two
  `RECORD` lines differ, as prompt §1.2 gives them.
- **The probe**, in the two installed wheels: version `0.5.0`; seven spec fields, five record
  fields; a record without counts has `v0.4.0`'s keys and the same canonical line; with counts five
  keys, and it hashes; the guard's plain digests differ from `v0.4.0`'s, and with the condition are
  equal.
- **The clients**: as prompt §1.1's table, re-read at `bda6dbc`'s writing.
- **Expected counts.** The suite **538** before and after; `compare_ported_tests.py` unchanged;
  `black --check datastorekit docs` **79**; the index **5** before, **4** after.

**What the review exists to establish.**
- **(E1) Scope.** Only §7's files change; nothing under `datastorekit/`.
- **(E2) The release.** The wheel is `0.5.0`, carries 01's two modules, and nothing of the tests.
- **(E3) The addenda.** Each true of `v0.5.0` and of its client at the commit named; SGK's and
  ChamPBH's give the guard's condition and say not to bump; SI's gives each item of §2.4; every
  superseded statement named; `+` lines only.
- **(E4) The issue closed**, on the board and in the index.
- **(E5) Both ends.** 538 in `venv/` (with `pip show` `0.5.0`) and at the high end.

**Conventions.** Prompt 01's note's, and all bind the agent. And for this prompt: **Ray is not
started; no network; no push, no tag, no change to the GitHub repository's settings.**

## 1. Before you dispatch

1. **The tree.** Branch and `HEAD` recorded; `git status --short` and `git diff --cached` empty; one
   worktree; `git status --short --ignored` recorded (`.idea/`, `venv/`, five `__pycache__/`).
2. **The baseline** is 01's review's (only `prompts/` has moved since): 538 OK in `venv/`; port
   check 0; `black` 79; `pip show datastorekit` `0.4.0`.
3. **The clients and RunRegistryKit**: each `HEAD` and status recorded.
4. **The remote**: `main` at `bda6dbc…` and the seven tags.
5. **Ray**: none; `RAY_ADDRESS` unset.
6. **The index**: 5. Tell the agent it becomes 4.

## 2. Dispatch

One fresh-context subagent, on **Opus**, in this checkout. Give it the prompt, the campaign README,
this board, `docs/OPEN_ISSUES.md`, `CLAUDE.md`, `fingerprint` prompt 02 and its log; `HEAD`, the
clients' and RunRegistryKit's `HEAD`s, the counts; and §0 of this note, up to "## 1. Before you
dispatch", as a copy in the session scratchpad. The agent does not read `orchestrator/`, nor the
orchestrator's scratch.

Tell it plainly:
- **One commit, at the end.** Its log is `logs/02-release-v0.5.0.md`, in README §5.1's form.
- **The files it may change are the prompt's §7 list, and nothing else.**
- **Under `docs/`, no line is removed.**
- **It writes nothing in any client repository or in RunRegistryKit, and runs, imports or opens
  nothing of one.**
- **It reaches no network and starts no Ray.**
- **It pushes nothing and makes no tag.**
- **Stop and ask** on any of the prompt's §6 conditions.

## 3. The review — ten checks

Fresh, offline, in a subdirectory of the scratchpad of the review's own.

1. **Scope (E1).** `git show --stat <commit>`: §7's files only; `git diff <parent> <commit> --
   datastorekit docs/client-contract.md docs/extraction-verification.md docs/extraction .github` is
   empty; `pyproject.toml`'s diff is the version line alone.
2. **The release (E2).** Rebuild from `git archive <commit>` and from `git archive v0.4.0`; the
   wheel's name, entries, `METADATA` and `RECORD` comparison as correction 3 and prompt §1.2; run
   the log's probe in a fresh venv of each, from outside the repository, with `python -I`.
3. **The breakages.** (a)–(c) from the log, each checked with `git apply --check` and `-R --check`,
   and each failing as the log records.
4. **The README and `PROVENANCE.md`**, by reading: as §2.2 and §2.3; every anchor resolves; nothing
   says `v0.5.0` is tagged.
5. **The addenda (E3)**, by reading, against the clients at the commits named (`git show`): the
   guard's condition and its quoted `plain` in SGK's and ChamPBH's; SI's items; the pins;
   correction 2's supersessions; correction 1's shifts as numbers, checked against the files.
6. **Additive.** `git diff <parent> <commit> -- docs/adoption` has no `-` line.
7. **The gate.** G4's row is the row as it was with one sentence added; G1–G3 unchanged.
8. **The issue (E4).** Moved to §4 with its closing line; its index row deleted; the index 4, its
   date 2026-10-21.
9. **Both ends (E5).** 538 in `venv/` with `pip show` `0.5.0` and no `datastorekit.egg-info/` left;
   538 in a fresh high-end venv with the commit's export installed editable. Port check, `black` 79.
10. **The records and nothing left behind.** The log, board, README, `prompts/INDEX.md`; no Ray;
    seven tags; `origin` unchanged; no `build/`, `dist/` or `*.egg-info`.

## 4. After the review

Record it on the board as a §1 *Orchestrator review of prompt 02* paragraph; fix residue ("this
commit" → the SHA; "reviewed"; the notes line) in a follow-up commit of its own. Report to the
user what landed, the release check, both ends, and the index at 4, and **ask whether to push
`main`** (§5).

## 5. Pushing and the tag

As `fingerprint`'s note §5. With the user's approval, push `main` (a fast-forward from `bda6dbc`).
Read the CI run once, when the user says it has finished, and record it. **Only if both ends are
green**, and with the user's approval, make `v0.5.0`, annotated, on 02's commit (not on a records
commit after it), push the tag, and check `git ls-remote origin` gives `refs/tags/v0.5.0^{}` as
02's commit. Then record the tag on this board and on the extraction board's G4, close the campaign
in its header, README and `prompts/INDEX.md`, in a records commit of its own, pushed with approval;
and give the user prompt §8's hand-ons.
