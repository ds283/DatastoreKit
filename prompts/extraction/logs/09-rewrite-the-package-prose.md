# Log 09 — rewrite the package prose

**Subject:** Rewrite the package prose for this repository · **Commit:** `cad7bc1` ·
**Date:** 2026-10-10 · **Model:** Claude Opus 5.5 · **Result:** landed; unpushed and untagged.

`[01-package-prose-names-sgks-layout]`, open since 01 and assigned here by U33 and U35, widened by
U38, is closed. Every comment and docstring under `datastorekit/` that cited the source
repository's layout, campaigns, logs, audits, issues, commits or `var/` has lost the citation and
kept its explanation, made true for this package (U39). The appendix's **248** lines (181 by tier
A's rules, 9 citing the source's commits, 58 found by reading) are decided line by line: 247
rewritten, 1 kept as a generic mention of the source. My own reading found **81** further lines
that cite the source (33 of them listed by the dispatch note's correction 3): all rewritten. The
two `sys.path` sentences, the two `python tools/shard_key_audit.py` sentences and "a directory
other than the repository root" are true now, and so are correction 4's two and five more that
the reading found false.

The guard's `KNOWN_HITS` is empty (U17), and its 8 tests pass. A new module,
`datastorekit/tests/test_prose_names_no_source.py` (**6** tests, U40), reads every comment and
docstring of the package and fails on any match of four rules, with no allow list. On the
unrewritten tree its first test fails on exactly tier A's 181 lines in 42 files and the other five
pass; after the rewrite all six pass. Only prose changed: the AST of every changed file, with its
docstrings blanked, equals `452b3c9`'s, except the guard (`KNOWN_HITS`' one entry) and the new
module. The suite goes from **480 to 486**, in `venv/` and at the high end (4 `ResourceWarning`
lines). Each of the nine breakages (a)–(i) fails what the prompt says it fails. The issue moves to
the board's §4; the index goes from **5 to 4 open** (0 on this repository's boards).

No client was written, imported or run; nothing was pushed, tagged or downloaded; Ray was never
started; no `git stash` was used in the checkout.

Prompt: [`../09-rewrite-the-package-prose.md`](../09-rewrite-the-package-prose.md), with the
orchestrator's dispatch note §0: five corrections, five additions, its measured facts and its
conventions. Each is followed as given; §2 classifies them. Line numbers are `452b3c9`'s (whose
`datastorekit/` is `efedc8d`'s) unless "at 09's tree" says otherwise.

## 1. What shipped

### 1.1 Tiers A and B, per file

43 files change under `datastorekit/` (the appendix's 42 and the new module); the diff is 638 lines
in, 687 out. No file outside the appendix's 42 needed a rewrite. Per file, the appendix's lines by
tier (A / B / C), the further lines decided in §1.2, and the kind of citation removed:

| File | A | B | C | Further | Citations removed |
|---|---|---|---|---|---|
| `SQL/Datastore.py` | 12 | 0 | 3 | 0 | `prompts/a3-v2-readiness` prompts 02, 03; `prompts/datastore-generic` prompt 06; `prompts/datastore-integrity` prompt 01; `Datastore/SQL/schema.py`; bare "(prompt 03)" |
| `SQL/ShardedPool.py` | 27 | 0 | 6 | 1 | the same campaigns; `docs/…-audit.md` §4.5, V1 case 4; "README U1"/"§6.2 U4"/"the user's decision U1"; "audit §4.1", "the audit's M1 table"; `Datastore/shard_paths.py` ×5; `Datastore.store_inventory`; the registry's `store retire` |
| `SQL/factory_base.py` | 3 | 0 | 0 | 0 | `prompts/datastore-generic` prompts 07, 08; `Datastore/store_inventory.py` |
| `SQL/schema.py` | 10 | 0 | 1 | 0 | `prompts/datastore-generic` prompts 05–07, `…-followup` prompt 01; `Datastore.contract`, `Datastore.store_inventory`, `Datastore/…` paths |
| `_timing.py` | 1 | 0 | 0 | 0 | the source's `utilities.py` (rule 4; the import commit and `PROVENANCE.md` stay) |
| `defaults.py` | 0 | 0 | 0 | 1 | the source's `config/defaults.py` (rule 4) |
| `contract.py` | 2 | 0 | 1 | 0 | `prompts/datastore-generic` prompt 07, "README §6.2, U4"; `Datastore/SQL/schema.py` |
| `replication.py` | 6 | 0 | 3 | 1 | `prompts/datastore-integrity` prompts 01, 02; `prompts/a3-v2-readiness` prompt 03; bare "(prompt 02)"; the `Datastore` package, `Datastore.SQL` |
| `shard_paths.py` | 1 | 0 | 0 | 1 | `Datastore.SQL`; "2026-09-23, 54 rows into the A3 baseline store"; "stay a standalone script" |
| `store_inventory.py` | 8 | 0 | 1 | 2 | `prompts/datastore-generic` 06, 08; `prompts/datastore-integrity` 07, 09a, 09b; bare "(prompt 01)"; "decision D1" ×2; `Datastore.contract` ×2 |
| `store_reader.py` | 5 | 0 | 0 | 0 | `prompts/datastore-generic` 05, 06; `Datastore.SQL.schema.…` ×3 |
| `tools/shard_key_audit.py` | 3 | 0 | 1 | 0 | "the B1 fix"; `Datastore/shard_paths.py`; `Datastore.SQL`; the `sys.path` sentence; and (§2.3) `e.g. "wavenumber"` |
| `tools/sharded_store.py` | 2 | 0 | 0 | 0 | `prompts/datastore-portability/README.md` sections 6.3–6.4; the `sys.path` sentence |
| `tests/real_store_fixtures.py` | 4 | 0 | 2 | 1 | `var/`; `prompts/datastore-generic` 05; "store-fingerprint prompt 02" ×2; "prompt 02's inventory tests", "prompt 01's tests" |
| `tests/schema_description.py` | 8 | 0 | 0 | 4 | `Datastore/…` paths ×6; "store-fingerprint prompt 01"; `prompts/datastore-integrity` README §6.2 D5; `schema_at_base.json`'s history |
| `tests/shard_store_fixtures.py` | 1 | 0 | 0 | 1 | "prompt 03 of the datastore-generic campaign"; "the sweep script's check" |
| `tests/standin_pool.py` | 6 | 0 | 2 | 1 | `var/`; `docs/datastore-integrity-audit/replicated_write_fault_probe.py`, its campaign's README §5 rule 9; "added by a3-v2-readiness prompt 02" ×3; bare "(prompt 02: …)" ×2; "the production table lists" |
| `tests/test_absolute_shard_record_refused.py` | 2 | 3 | 2 | 0 | `prompts/datastore-generic` prompt 04 §2 L3; `b04671f` ×3; the 2026-09-23 incident; "Before/Since prompt 04"; `var/` |
| `tests/test_closed_store_refusals.py` | 2 | 0 | 0 | 1 | `prompts/datastore-generic-followup` prompt 03; `[04-closed-store-refusals-repeat-their-prefix]`; `var/` |
| `tests/test_copy_move_store.py` | 1 | 0 | 1 | 8 | `prompts/datastore-portability` prompt 02 §2 P6 and §3; "Since prompt 01"; `logs/02-copy-and-move-a-store.md`; "Test 2/4/5/6/7"; "P6"; "the log's interruption table" |
| `tests/test_declared_facts.py` | 2 | 0 | 1 | 0 | `prompts/datastore-generic` prompt 07; "README §6.2, U4 and the user's choice for 07"; `var/` |
| `tests/test_delete_store.py` | 3 | 0 | 0 | 12 | `prompts/store-retirement` prompt 01 §3; the A3 backup and `docs/store-retirement-audit.md` §2.7; `logs/01-delete-a-closed-store.md`; `var/`; "Test 1/3/4/5/6"; "R1" ×2; rows D0–D5 of the source's interruption table |
| `tests/test_drop_refuses_dangling_references.py` | 3 | 0 | 2 | 3 | `prompts/datastore-generic-followup` prompt 01; "README §6.1, decision 1"; "README §0.2" ×2; `Datastore.SQL.schema…`; `--drop`; "this prompt's refusal"; `var/` |
| `tests/test_foreign_key_check.py` | 3 | 0 | 0 | 1 | "prompt 06 of `prompts/datastore-integrity` (board item S4)"; `docs/datastore-integrity-audit.md`; `[00-quadsource-tq-serial-has-the-wrong-foreign-key]`; `var/` |
| `tests/test_inventory_declarations.py` | 2 | 0 | 1 | 1 | `prompts/datastore-generic` prompt 08; "audit C1 rows 12 and 13"; "its prompt 08"; `var/`; "and the report" (false) |
| `tests/test_layer_is_generic.py` | 1 | 0 | 0 | 3 | "the repository root"; "SecondaryGWKit's prompt 08"; and §2.3's paragraph, banner, comment and `KNOWN_HITS` entry |
| `tests/test_layer_registry.py` | 4 | 0 | 0 | 4 | `prompts/datastore-generic` prompt 06; `config/datastore.py`, `config.datastore` ×2; `main.py`'s `--drop` and `--help` ×2; `var/` |
| `tests/test_one_timestamp_per_write.py` | 2 | 0 | 0 | 1 | `prompts/datastore-generic` prompt 03, R2; "the commit-point table"; `var/` |
| `tests/test_prune_at_open.py` | 3 | 0 | 1 | 0 | `prompts/a3-v2-readiness` prompt 02, W3, "the user's decision U1"; `Datastore.tests.standin_pool`; `var/` |
| `tests/test_read_only_pool.py` | 6 | 0 | 8 | 7 | `prompts/a3-v2-readiness` prompt 03, O1–O2; `prompts/datastore-generic` prompt 05, README U1; `Datastore.tests.standin_pool`; `var/`; `docs/a3-v2-readiness/readonly_open_probe.py` (M2d); QSI ×2; audit R1, R2 Run 1, R2 Run 2, A2, O2; "the prompt's log"; "the script" ×2; `resolve_run_selection` |
| `tests/test_reconcile_at_open.py` | 6 | 2 | 5 | 1 | `prompts/datastore-integrity` prompt 02; `prompts/a3-v2-readiness` prompt 02; `prompts/datastore-generic` prompt 03, R2; `…-followup` prompt 01; `e53f323` ×2; "prompt 01's / log 01's commit-point table" ×3; "log 01:"; "the audit probe's step 4"; `hot_journal_probe.py`; `var/` |
| `tests/test_replicated_write.py` | 4 | 0 | 2 | 2 | `prompts/datastore-integrity` prompts 01, 02 and "the user's decision, 2026-09-28"; "the prompt establishes"; `utilities.WallclockTimer`; "the audit probe's step 4"; "prompt 01 refused"; `var/` |
| `tests/test_schema_builder.py` | 5 | 0 | 0 | 3 | "store-fingerprint prompt 01" ×2; `prompts/datastore-integrity` README §6.2 D5; `schema_at_datastore-generic-07.json`; `schema_at_base.json`; `[00-build-schema-reads-registration-before-its-none-check]`; `var/` |
| `tests/test_shard_file_name.py` | 2 | 0 | 2 | 0 | `Datastore/shard_paths.py`; `prompts/datastore-portability` prompt 02 §2 P5 and §3; "Until / before prompt 02" |
| `tests/test_shard_key_audit_copy.py` | 5 | 0 | 1 | 0 | `tools/shard_key_audit.py` ×2; `prompts/datastore-portability` prompt 01 §2 P4 and §6; "Before prompt 01"; `Datastore/shard_paths.py`, `Datastore.shard_paths`; "standalone … script" |
| `tests/test_shard_key_audit_refusals.py` | 3 | 4 | 3 | 1 | `tools/shard_key_audit.py` ×2; `prompts/datastore-generic` prompt 04 §2 L2; `a2bd966` ×3, `b04671f`; `[04-the-shard-key-audit-crashes-where-it-should-refuse]` ×2 and its date; "Until / Before prompt 04"; the 2026-09-23 shape |
| `tests/test_shard_paths.py` | 3 | 0 | 1 | 0 | `Datastore/shard_paths.py`; `prompts/datastore-portability` prompt 01 §3; "Prompt §2 P4"; `Datastore.SQL`; "standalone script" |
| `tests/test_sharded_store_script.py` | 3 | 0 | 0 | 0 | `tools/sharded_store.py`; `prompts/datastore-portability` prompt 02 §2 P7 and §3; "the repository root" |
| `tests/test_shardedpool_shard_paths.py` | 3 | 0 | 3 | 13 | `prompts/datastore-portability` prompt 01 §3, P0, §4, §5, §6; "Until prompt 01"; the 2026-09-23 incident, the atol sweep, the A3 baseline store ×2; `Datastore/shard_paths.py`, `Datastore.shard_paths`; README §0.1; "Test 2/4/5/6" |
| `tests/test_store_inventory.py` | 3 | 0 | 2 | 2 | `Datastore/store_inventory.py`; "store-fingerprint prompt 02"; `prompts/datastore-integrity` prompt 09c; "decision D1"; F7; "prompt 01's"; `var/` |
| `tests/test_store_reader.py` | 4 | 0 | 1 | 0 | `Datastore/store_reader.py`; "store-fingerprint prompt 01"; `prompts/datastore-generic` prompt 05 ×2; `var/` |
| `tests/test_store_schema.py` | 4 | 0 | 0 | 2 | `prompts/datastore-generic` prompt 05, S1–S3, README §6.2; `Datastore.SQL.schema…`; "U1" ×2; `store fingerprint`; `var/` |
| `tests/test_version_row_at_open.py` | 3 | 0 | 2 | 0 | `prompts/a3-v2-readiness` prompt 02, W1–W2; `Datastore.tests.standin_pool`; "audit V1 case 3" ×2; `var/` |
| **Total** | **181** | **9** | **58** | **81** | |

By path, the 248 are 96 lines in 12 files of the layer and 152 in 30 files under `tests/`
(correction 2). The diff is the detail.

**How the rewrite was made.** Each file was rebuilt from its `HEAD` blob plus a list of line-range
edits (numbered at `452b3c9`), each edit checking that its range holds the citation it removes;
`black` then ran on the changed files. The edit lists and the script are in the scratchpad, never
committed (§2, deviation 11).

### 1.2 Tier C and the further lines, line by line

Line numbers at `452b3c9`. "Rewritten" means the citation went and the explanation stayed;
"kept" gives the reason.

**Tier C (the appendix's 58 starred lines).**

| Line | Text, in brief | Decision | Reason |
|---|---|---|---|
| `SQL/Datastore.py:583`, `:656`, `:745` | "(prompt 03)" after a read-only comment | rewritten | the source's `a3-v2-readiness` prompt 03 (the same module's `:79`, `:124` name it); removed |
| `SQL/ShardedPool.py:489` | "(the audit's M1 table, row by row, is in the prompt's log)" | rewritten | the source's audit and log; removed |
| `SQL/ShardedPool.py:499` | "prompt 06)" continuing `(prompts/datastore-generic,` | rewritten | the source's; removed with `:498` |
| `SQL/ShardedPool.py:1351` | "(README U1 of" `prompts/datastore-generic` | rewritten | the source's README and U1; removed |
| `SQL/ShardedPool.py:2195` | "generic README §6.2, the user's choice for prompt 07)" | rewritten | the source's; removed |
| `SQL/ShardedPool.py:3134` | "(audit §4.1)" | rewritten | the source's audit; removed |
| `SQL/ShardedPool.py:3222` | "(prompt 03)" | rewritten | the source's; removed |
| `SQL/schema.py:32` | "prompt 07)." continuing `(prompts/datastore-generic,` | rewritten | removed with `:31` |
| `contract.py:3` | "07; README §6.2, U4)." | rewritten | the source's README and U4 (this campaign's U4 is the distribution) beside its campaign; removed |
| `replication.py:17` | "compares its replicated tables across shards (prompt 02)" | rewritten | the source's `datastore-integrity` prompt 02 (the module's `:2` and `:128` name it); removed |
| `replication.py:22`, `:197` | "prompt 03)" continuing `prompts/a3-v2-readiness` | rewritten | removed with the line before |
| `store_inventory.py:4` | "opens the store with ``open_read_only`` (prompt 01)" | rewritten | the source's `store-fingerprint` prompt 01; removed |
| `tools/shard_key_audit.py:9` | "(see the B1 fix in ShardedPool._assign_shard_keys)" | rewritten | the source's audit label; now "(the value ShardedPool._assign_shard_keys writes there)" |
| `tests/real_store_fixtures.py:20` | "A test (or prompt 02's inventory tests) adds rows" | rewritten | the source's `store-fingerprint` prompt 02; removed |
| `tests/real_store_fixtures.py:385` | "so prompt 01's tests read the store they were written against" | rewritten | the source's prompt 01; "so a test written against the defaults reads the store it was written against" |
| `tests/standin_pool.py:314`, `:397` | "(prompt 02: …)" | rewritten | the source's `a3-v2-readiness` prompt 02 (the module's `:195`, `:225`, `:252` name it); the explanation after the colon kept |
| `tests/test_absolute_shard_record_refused.py:9`, `:10` | "54 rows into the A3 baseline store", "Before/Since prompt 04" | rewritten | the source's incident and prompt; history told by what changed (rule 3) |
| `tests/test_copy_move_store.py:5` | "Since prompt 01 a store's ``shards`` table holds bare file names" | rewritten | the source's `datastore-portability` prompt 01; "A store's ``shards`` table holds bare file names" |
| `tests/test_declared_facts.py:3` | "prompt 07; README §6.2, U4 and the user's choice for 07)." | rewritten | the source's; removed |
| `tests/test_drop_refuses_dangling_references.py:3` | "README §6.1, decision 1)." | rewritten | the source's README beside its campaign (this campaign's §6.1 holds D1–D4); removed |
| `tests/test_drop_refuses_dangling_references.py:13` | "exactly the tables README §0.2 measured" | rewritten | the source's README; here the tables are `MEASURED`'s, measured on the neutral client (`:43`) |
| `tests/test_inventory_declarations.py:48` | "prompt 08, when that was a hand-kept list" | rewritten | the source's prompt; "from when that was a hand-kept list" |
| `tests/test_prune_at_open.py:3` | "prompt 02, W3; the user's decision U1)." | rewritten | the source's; removed |
| `tests/test_read_only_pool.py:9` | "the audit probe the source repository's test imported, and keeps that probe's instrument" | **kept** | a generic mention of the source (§1.1): it names no file, campaign, label or commit, as `tests/client/reader.py:3` (this campaign's) says the same; the line is rewrapped only because `:5`–`:6` changed |
| `tests/test_read_only_pool.py:18` | "QSI's whole sequence" | rewritten | the source's reader (rule 1); "the reader's whole sequence" |
| `tests/test_read_only_pool.py:213` | "QSI's whole sequence (the probe's)" | rewritten | "The reader's whole sequence (``reader_sequence``)" |
| `tests/test_read_only_pool.py:240` | "18 times (audit R2 Run 1)" | rewritten | the source's audit; removed (the 18 is asserted at `:249`) |
| `tests/test_read_only_pool.py:273` | "the hits audit R2 Run 1 recorded" | rewritten | "the hits the sequence makes" |
| `tests/test_read_only_pool.py:358` | "(audit R2 Run 2)" | rewritten | removed (with `:357`, §1.2 further lines) |
| `tests/test_read_only_pool.py:625` | "(audit R1)" | rewritten | removed |
| `tests/test_read_only_pool.py:817` | "README U1)." continuing `(prompts/datastore-generic,` | rewritten | removed |
| `tests/test_reconcile_at_open.py:11` | "at every point of prompt 01's commit-point table" | rewritten | the source's log; "at every commit point of the replicated write" (the cases keep their own labels, `P1-C`, `Rn-P3`, …) |
| `tests/test_reconcile_at_open.py:230` | "a row of log 01's commit-point table ("After")" | rewritten | "a commit point of the replicated write" |
| `tests/test_reconcile_at_open.py:335` | "(log 01: _assign_shard_keys self-heals)" | rewritten | "(_assign_shard_keys self-heals)" |
| `tests/test_reconcile_at_open.py:579` | "The audit probe's step 4" | rewritten | "A serial split" |
| `tests/test_reconcile_at_open.py:985` | "hot_journal_probe.py's method" | rewritten | the source's probe; "a hot journal made by a write transaction large enough to spill …" |
| `tests/test_replicated_write.py:410` | "The split of the audit probe's step 4, by hand" | rewritten | "A serial split, by hand" |
| `tests/test_replicated_write.py:618` | "the write that prompt 01 refused" | rewritten | the source's prompt; "the write that the set record refused" |
| `tests/test_shard_file_name.py:5` | "Until prompt 02 the constructor named shard *i* … inline" | rewritten | "The constructor once named …" |
| `tests/test_shard_file_name.py:50` | "the expression the constructor used before prompt 02" | rewritten | "… once used" |
| `tests/test_shard_key_audit_copy.py:6` | "Before prompt 01 the tool attached …" | rewritten | "The tool once attached …" |
| `tests/test_shard_key_audit_refusals.py:16` | "Since `[04-the-shard-key-audit-crashes-where-it-should-refuse]` was closed (2026-10-05)" | rewritten | the source's issue; "Three more shapes are refusals …, where the tool once ended in a traceback" |
| `tests/test_shard_key_audit_refusals.py:118` | "Before prompt 04 the tool read them as B's siblings" | rewritten | "The tool once read them as B's siblings" |
| `tests/test_shard_key_audit_refusals.py:196` | "# [04-the-shard-key-audit-crashes-where-it-should-refuse]: each of these ended …" | rewritten | "each of these once ended …" |
| `tests/test_shard_paths.py:105` | "Prompt §2 P4: … must stay a standalone script" | rewritten | the source's prompt; "The audit tool imports this module, and imports neither ray nor sqlalchemy" |
| `tests/test_shardedpool_shard_paths.py:5` | "Until prompt 01, ``_write_shard_data`` recorded …" | rewritten | "``_write_shard_data`` once recorded …" |
| `tests/test_shardedpool_shard_paths.py:12` | "(measured by prompt 01's" | rewritten | the source's probe P0; removed with `:13` |
| `tests/test_shardedpool_shard_paths.py:141` | "and README §0.1's backup is the same case without the rename" | rewritten | "(a backup copied without the rename is the same case)" |
| `tests/test_store_inventory.py:3` | "prompt 02)" continuing "(store-fingerprint" | rewritten | removed |
| `tests/test_store_inventory.py:870` | "Test 10: prompt 01's never-writes check" | rewritten | "Test 10" is the module's own (its docstring numbers 1–10); "prompt 01's" became "the reader's" |
| `tests/test_store_reader.py:3` | "prompt 01)" continuing "(store-fingerprint" | rewritten | removed |
| `tests/test_version_row_at_open.py:14`, `:290` | "(audit V1 case 3)" | rewritten | the source's audit; removed |

**Correction 3's lines (33).** Each decided by the note's label rule; every one is the source's.

| Line | Text, in brief | Decision | Reason |
|---|---|---|---|
| `tests/test_closed_store_refusals.py:4` | `[04-closed-store-refusals-repeat-their-prefix]` | rewritten | the source's issue; removed with `:3` |
| `tests/test_foreign_key_check.py:9` | "It would have caught `[00-quadsource-tq-serial-has-the-wrong-foreign-key]`" | rewritten | the source's issue, which also named a client's table; "It catches a member's column declared into its owner's table but holding a serial of another table" |
| `tests/test_schema_builder.py:22` | "**The fix** of `[00-build-schema-reads-registration-before-its-none-check]`" | rewritten | "**A registration of ``None``**: …" |
| `tests/test_delete_store.py:13`, `tests/test_copy_move_store.py:10` | `logs/01-delete-a-closed-store.md`, `logs/02-copy-and-move-a-store.md` | rewritten | the source's logs; removed (the order of deletion and of copying stays explained) |
| `tests/test_read_only_pool.py:19` | "the hits R2 Run 1 recorded" | rewritten | "the read-write pool's hits" (the test compares the two) |
| `tests/test_read_only_pool.py:64` | "(O2: importable from the pool's module)" | rewritten | label removed |
| `tests/test_read_only_pool.py:239` | "the instrument, first (A2)" | rewritten | label removed |
| `tests/test_read_only_pool.py:274` | "R2 recorded 1 and 1, 6" | rewritten | removed |
| `store_inventory.py:49`, `:123` | "decision D1" | rewritten | `git blame` names `8bc60a5` on both, unchanged since the import: the source's D1 (this campaign's D1 is "extract the layer"); removed |
| `tests/test_store_inventory.py:394` | "(decision D1)" | rewritten | a ported module, beside the source campaign's numbering; removed |
| `tests/test_store_inventory.py:617` | "(F7)" | rewritten | removed |
| `tests/test_store_schema.py:18` | "5. U1: a read-write open …" | rewritten | the source's U1 (this campaign's U1 is the name), as `:411` beside `prompts/datastore-generic` shows; removed |
| `tests/test_schema_builder.py:10`, `tests/schema_description.py:13` | "§6.2 D5" | rewritten | the source's README beside its campaign; removed |
| `tests/test_copy_move_store.py:44`, `:211` | "prompt §2 P6", "Test 5: every refusal of P6" | rewritten | the source's prompt; "the three layouts:", "Every refusal" |
| `tests/test_shardedpool_shard_paths.py:13`, `:26`, `:68`, `:90`, `:140` | "prompt 01's P0", "prompt §6 item 2", "prompt §6 item 3", "Prompt §5", "the §4 demonstration" | rewritten | the source's prompt; removed |
| `tests/test_shardedpool_shard_paths.py:183` | "The P0 case after the fix" | rewritten | "A store whose primary is moved without its shards is refused, where it once opened on empty shards" |
| `tests/test_delete_store.py:193`, `:536` | "Test 3, and the refusals test 5 requires …: every refusal of R1", "R1:" | rewritten | the source's prompt and label; "Every refusal, …, under ``resume`` too, as ``TestResumeRelaxesOneThingOnly`` requires", "A file that changed …" |
| `tests/test_drop_refuses_dangling_references.py:43` | "the source's were its README §0.2's table" | rewritten | "the source's were measured on its own" |
| `tests/shard_store_fixtures.py:93` | "or the sweep script's check" | rewritten | a tool this package does not have; removed |
| `shard_paths.py:22` | "(2026-09-23, 54 rows into the A3 baseline store)" | rewritten | the source's history (rule 3); "a pool that used them would read and write the original" |
| `tests/test_delete_store.py:8` | "as the backup of the A3 store was (`docs/store-retirement-audit.md` §2.7)" | rewritten | "as in a copy of a primary written before shard records were bare file names" |
| `tests/test_shardedpool_shard_paths.py:9`, `:10` | "That happened on 2026-09-23, when the first run of the atol sweep put 54 rows into the A3 baseline store …" | rewritten | the source's history; the sentence before already says what happened, so the incident is removed |
| `tests/test_shardedpool_shard_paths.py:104` | "the failure that put 54 rows into the A3 baseline store, and the one that makes the retained backup of that store unsafe" | rewritten | "the failure in which a copied store read and wrote the original's shards, and the one that makes a backup of such a store unsafe to open in place" |

**Further lines found by my own reading (48).** None is matched by tier A's rules.

| Line | Text, in brief | Decision | Reason |
|---|---|---|---|
| `replication.py:25` | "This module lives at the top of the ``Datastore`` package" | rewritten | the source's package; `datastorekit` (rewrapped with `:28`) |
| `defaults.py:2` | "from the source repository's `config/defaults.py`" | rewritten | rule 4 drops the source's file name; the import commit and `PROVENANCE.md` stay |
| `tests/schema_description.py:5`, `:7` | "The first witness, ``schema_at_base.json``, was captured …", "It witnessed a refactor …" | rewritten | that witness is the source's and not in this repository; "The source repository's first witness was captured … its witnesses are its history, and are not copied here" |
| `tests/schema_description.py:20` | `<repo>/Datastore/tests/schema_description.py` | rewritten | the source's path (preceded by `/`, so no rule matches); `<repo>/datastorekit/tests/schema_description.py` |
| `tests/standin_pool.py:286` | "with the production table lists" | rewritten | the source's production configuration; false here: "the neutral client's table lists" |
| `tests/test_copy_move_store.py:115`, `:179`, `:408`, `:629` | "Test 2:", "Test 4:", "Test 6:", "Test 7:" | rewritten | the source prompt's §3 test numbers (`:3`); the module numbers nothing itself; label removed |
| `tests/test_copy_move_store.py:409` | "what the log's interruption table says" | rewritten | the source's log; "the one each failure point names" |
| `tests/test_copy_move_store.py:437` | "# (row of the table, the failure, …)" | rewritten | the same table; "(the failure point, …)" |
| `tests/test_delete_store.py:132`, `:450`, `:614` | "Test 1:", "Test 5:", "Test 6:" | rewritten | the source prompt's §3 numbering (`:3`); label removed |
| `tests/test_delete_store.py:370` | "Test 4: … The state left behind is the interruption table's row" | rewritten | label and the source's log removed |
| `tests/test_delete_store.py:401`, `:407`, `:410`, `:422` | "the table's row", "row D0", "rows D1-D4", "row D5" | rewritten | labels of the source log's interruption table; no code uses them; the explanation kept |
| `tests/test_drop_refuses_dangling_references.py:5` | "``--drop`` drops exactly the tables of the groups named" | rewritten | the source's command line; "A drop removes exactly …" |
| `tests/test_drop_refuses_dangling_references.py:248` | "Gadget alone would meet this prompt's refusal" | rewritten | the source's prompt; "the dependents' refusal" |
| `tests/test_inventory_declarations.py:12` | "``resolve()`` and the report go through the declared type map" | rewritten | false here (U16: the report test is not ported; log 04b §7 item 1); "``resolve()`` goes through …" |
| `tests/test_layer_registry.py:6` | "The client keeps them in ``config/datastore.py``" | rewritten | the source's module; "(the neutral client in ``datastorekit/tests/client/registry.py``)" |
| `tests/test_layer_registry.py:9`, `:138` | "``config.datastore``", "# 1. config.datastore" | rewritten | "the client's registry module", "# 1. the client's registry" |
| `tests/test_layer_registry.py:11` | "the groups are in the order the command line offers them" | rewritten | false here (the neutral client has no command line, `:74`); "in the order ``COMMAND_LINE_ORDER`` gives" |
| `tests/test_one_timestamp_per_write.py:17`, `tests/test_reconcile_at_open.py:224` | "the commit-point table" | rewritten | the source's log 01; "every commit point" |
| `tests/test_replicated_write.py:7` | "the invariant the prompt establishes" | rewritten | the source's prompt; "the invariant the replicated write keeps" |
| `tests/test_replicated_write.py:51` | "(utilities.WallclockTimer prints …)" | rewritten | the source's module; `datastorekit._timing.WallclockTimer` |
| `tests/test_read_only_pool.py:88` | "(for the prompt's log)" | rewritten | the source's; removed (the module never prints `MESSAGES`) |
| `tests/test_read_only_pool.py:304`, `:350` | "the script's own RuntimeError", "the RuntimeError the script raises" | rewritten | the source's probe script; here it is the sequence (`client/reader.py:18`); "the sequence's" |
| `tests/test_read_only_pool.py:357` | "resolve_run_selection finds no run" | rewritten | the source's function; "a reader that selects a run by its tag finds no run" |
| `tests/test_shardedpool_shard_paths.py:60`, `:103`, `:157`, `:230` | "Test 2:", "Test 4:", "Test 5:", "Test 6:" | rewritten | the source prompt's §3 tests 2–6 (`:3`); label removed |
| `tests/test_shard_key_audit_refusals.py:117` | "the 2026-09-23 shape" | rewritten | the source's incident; "the shape of a copy of a primary that recorded its shards by absolute path" |
| `tests/test_store_schema.py:13` | "as ``store fingerprint`` does through it" | rewritten | the source's command (its fingerprint stays in SGK, README §1); "``read_inventory``, and so anything built on it, refuses …" |
| `SQL/ShardedPool.py:2590` | "Its one intended caller is the registry's `store retire`, which keeps the store's sidecar behind as its record" | rewritten | the source's command; "Its intended caller is a registry-level tool that retires a store, which keeps its own record of it" |
| `tests/test_layer_is_generic.py:178` | "The names SecondaryGWKit's prompt 08 removed from its inventory" | rewritten | hazard 5: a client's (the source's) campaign; "The names SecondaryGWKit once removed …"; the clients' names stay |
| `tests/test_layer_is_generic.py:189` | "# the hits the layer's frozen prose holds" | rewritten | false once `KNOWN_HITS` is empty (correction 4); "# the hits the layer is known to hold: none, since extraction prompt 09" |
| `tests/test_layer_is_generic.py:212`, `tests/real_store_fixtures.py:393`, `tests/schema_description.py:193`, `tests/test_schema_builder.py:44` | "prompt 01 internalised both", "(prompt 04a)", "(prompt 04a, U20)" ×2 | rewritten | this campaign's prompts in modules ported from the source; qualified "extraction prompt NN" (rule 5) |

The 81 further lines are these 48 and correction 3's 33.

**Lines read and kept.**

| Line | Text, in brief | Reason |
|---|---|---|
| `tests/client/reader.py:3` | "The source repository's test imported an audit probe" | a generic mention of the source; this campaign's text |
| `tests/client/factories.py:826` | "the warning SGK's factory prints" | names the source, generically (rule 4), with no file |
| `tests/test_store_inventory.py:289`, `:342`, `:363`, `:394`, `:504`, `:577`, `:643`, `:692`, `:807`, `:870` | "Test 1:" … "Test 10:" | the module's own vocabulary: its docstring numbers its tests 1–10 (correction 3's rule for a label the module uses) |
| `tests/test_reconcile_at_open.py:524`, `:551`, `:629`, `:908`, `:1017` | `P1-C`, `C-P3`, `P3-K`, `Rn-P3`, `P1` | labels the module's code uses (correction 3) |
| `tests/test_copy_move_store.py:495`, `:580`–`:581` | `C5'`, `M4'`, "state M4" | labels the module's code uses (correction 3) |
| `tests/test_absolute_shard_record_refused.py:6` | "the safety property that the legacy-record tests used to guard" | history with no record cited |
| `tests/test_shard_key_audit_copy.py:15`–`:16`, `tests/test_shardedpool_shard_paths.py:25`–`:26` | "so that it can be run against the unfixed tool / ``ShardedPool`` for the deliberate-breakage record" | names no record of the source; only "(prompt §6 item 2)" went |
| `tests/test_layer_is_generic.py:3`–`:4`, `:14`–`:18`, `:80`–`:81`, `:128`, `:131`, `:319` | "extraction prompt 04b; README §6.2, U17", the clients by name, "README §6.1, D2", "(U17)" | this repository's own citations, and the clients the guard forbids (hazard 5) |
| `tests/test_layer_registry.py:607` and every "(prompt 03a/03b/04a/06 …)" under `tests/client/` | this campaign's prompts | rule 5: written by this campaign, in modules it wrote |

### 1.3 The false sentences (§2.2)

Each is now true at 09's tree, as read from the tools (`grep sys.path` finds no use in either) and
from the tests' `subprocess` calls (`cwd=self.cwd`, an unrelated directory; `PYTHONPATH` removed):

| Where (`452b3c9`) | Now |
|---|---|
| `tools/sharded_store.py:25-26` | "It is run as python -m datastorekit.tools.sharded_store with the package installed, and changes no sys.path." |
| `tools/shard_key_audit.py:24-26` | "The tool is run as `python -m datastorekit.tools.shard_key_audit` with the package installed, and changes no sys.path; it imports only the standard library and datastorekit.shard_paths, so it pulls in neither ray nor sqlalchemy." (`datastorekit/__init__.py` imports only `.object`, which imports only `typing`.) |
| `tests/test_shard_key_audit_copy.py:11`, `tests/test_shard_key_audit_refusals.py:28` | "run here as ``python -m datastorekit.tools.shard_key_audit <primary>``, from an unrelated working directory with no ``PYTHONPATH``" |
| `tests/test_sharded_store_script.py:5-6` | "as a subprocess, ``python -m datastorekit.tools.sharded_store``, from an unrelated working directory, with ``PYTHONPATH`` removed from the environment" |
| `tests/test_layer_is_generic.py:189` (correction 4) | the banner says the list is empty |
| `tests/test_layer_is_generic.py:31` (correction 4) | the "known hits" paragraph no longer says the prose is frozen |

Found false by the reading, and corrected under §2.2's last line: `tests/test_inventory_declarations.py:12`
(the report), `tests/test_layer_registry.py:11` (the command line), `tests/standin_pool.py:286`
(production lists), and `tests/schema_description.py:5`–`:7` and `tests/test_schema_builder.py:9`–`:12`,
which presented `schema_at_base.json` as a witness of this package (it is the source's).

### 1.4 The guard (§2.3)

`datastorekit/tests/test_layer_is_generic.py`: every list of `KNOWN_HITS` is empty, its inner
comment is gone, the comment above it says every list is empty, the banner (correction 4) says
"none, since extraction prompt 09", the docstring's paragraph says the list has been empty since
09 rewrote the layer's prose and that any hit fails by name, and `:71` says "relative to the top of
this repository". `tools/shard_key_audit.py:188`'s comment names no table. The guard's 8 tests pass.
Its one code difference from `452b3c9` is the emptied entry (§4.3).

### 1.5 The new module (§2.4, U40)

`datastorekit/tests/test_prose_names_no_source.py`, not ported, not in `PORTED`. It derives its
file set from the filesystem (`package_files()`, every `.py` under `datastorekit/`, itself
included: 66 files). From each it reads every `COMMENT` token and every docstring (the first
statement of a module, class or function when it is a string, found by `ast`), the docstring read
from its `STRING` token(s) in the source text, one physical line at a time, so that a failure names
the physical line. Runtime strings, f-strings and names are not read. Four rules, each named in a
failure (`file:line rule matched-text`):

| Rule | Pattern |
|---|---|
| a path of the source's layout | `(?<![\w/.])(?:Datastore\|tools\|prompts\|docs)/[\w./\-]*`, skipped when the path, trailing `.,;:` stripped, exists relative to the repository's top |
| a module of the source | `(?<![\w.])Datastore\.(?:SQL\|tests\|replication\|contract\|object\|shard_paths\|store_reader\|store_inventory)(?!\w)` (correction 1) |
| a name of the source | `repository root\|REPO_ROOT\|ObjectFactories\|RunRegistry\|main\.py\|config\.defaults\|utilities\.py` |
| a campaign or directory of the source | the six campaign names, and `(?<![\w/.])var/` |

Six tests (N = 6):

| # | Test | Pins |
|---|---|---|
| 1 | `TestThePackage.test_no_comment_or_docstring_names_the_source` | no prose line matches any rule; every hit, for every file, in one failure |
| 2 | `TestThePackage.test_the_scan_reaches_the_layer_and_the_tests` | the set holds `SQL/ShardedPool.py`, `tests/standin_pool.py`, `tests/test_replicated_write.py` (ported) and the module itself, and at least 60 files |
| 3 | `TestTheRules.test_each_rule_finds_its_form_in_prose` | 20 planted forms, each in a comment, a module docstring and a function docstring, are found by their rule on the right line |
| 4 | `TestTheRules.test_what_is_not_prose_is_not_read` | the same 20 forms in a runtime string, an f-string, a name and call arguments are not found |
| 4 | `TestTheRules.test_what_names_nothing_of_the_source_is_not_found` | `docs/client-contract.md`, `datastorekit/tools/sharded_store.py`, `datastorekit.tools.shard_key_audit`, `Datastore.object_get` (addition 1), `Datastore.set_version` and `Datastore.py`, in each kind of prose, are not found |
| 4 | `TestTheRules.test_the_path_rule_checks_existence` | an existing `docs/` path passes with a full stop after it; a missing one is found |

The planted forms are runtime strings, which the module does not read in itself, and its own prose
describes the rules without quoting a forbidden form (hazard 6). It opens no store, reads no
client, and `tearDownModule` raises if Ray was initialised.

### 1.6 The records

This log; the board (09's row and header; the issue moved from §3 to §4 with its "Closed" line);
`docs/OPEN_ISSUES.md` (the row deleted; 5 → 4, 0 on this repository's boards); `prompts/INDEX.md`
(the campaign's line; 1 → 0).

## 2. Deviations from the prompt

1. **Correction 1: the module rule takes the module name as a whole word** (`(?!\w)`). Without it
   the rules match `Datastore.object_get` on five true lines (`SQL/Datastore.py:590`,
   `contract.py:16`, `:37`, `:44`, `tests/test_version_keyed_lookups.py:6`), and test 1 could not
   pass. With it the rules give exactly the appendix's tier A, 181 lines in 42 files (§4.2).
   **STRUCTURALLY REQUIRED.**
2. **Correction 2: tier B is 9 lines and tier C 58**, not 10 and 57; 96 lines in 12 layer files
   and 152 in 30 test files, not 97 in 13 and 151 in 29. My parse of the appendix gives 248 lines,
   58 starred, in 42 files, and the 9 SHA lines are the note's. Recorded as found.
   **STRUCTURALLY REQUIRED** (an expectation corrected).
3. **Correction 3: further lines.** Its 33 lines are decided in §1.2, each by the note's label
   rule, and my own pass found 48 more (§1.2). Every `logs/` path the rules miss is the source's
   and is gone; that no rule matches `logs/` is recorded in §6, not acted on.
   **STRUCTURALLY REQUIRED** (scope completed under rule 8).
4. **Correction 4: two more sentences go false with §2.3** (`test_layer_is_generic.py:189` and
   `:31`), corrected (§1.3). **STRUCTURALLY REQUIRED.**
5. **Correction 5: every export the module ran in is of the whole tree** (`git archive HEAD`, then
   the rewritten files), so the path rule's existence check sees `docs/`. Recorded as found.
   **STRUCTURALLY REQUIRED.**
6. **Addition 1: the anchor is pinned.** Test 4 (`test_what_names_nothing_of_the_source_is_not_found`)
   asserts that `Datastore.object_get` in a planted comment and docstrings is not found, and
   breakage (i) drops the boundary. **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
7. **Addition 2: the module was written first and run on the unrewritten tree**, in a scratch
   export of `HEAD` with the module copied in, before anything changed in the checkout: test 1
   failed with 181 lines in 42 files, line for line tier A; tests 2–6 passed (§4.2). Then the
   rewrite, in the note's order. **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
8. **Addition 3: the AST check and the measurement scripts are in the scratchpad**, never committed;
   §4.3 and §4.4 give each method. **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
9. **Addition 4: each breakage is recorded as a diff, exactly as applied** (§5), and each replays
   with `git apply --check` and `git apply -R --check` against a whole-tree export of the rewritten
   tree, as recorded in this log. **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
10. **Addition 5: tier C and the further lines in one place, line by line** (§1.2, in three tables
    under one heading, with the lines kept after them); tiers A and B per file (§1.1).
    **IMPLEMENTATION CHOICE**, at the orchestrator's direction.
11. **The rewrite was applied by a scratch script**: each changed file rebuilt from its `HEAD` blob
    plus line-range edits numbered at `452b3c9`, each edit checking that its range holds the
    citation it removes, then `black` on the changed files. Re-running it gives the same tree.
    **IMPLEMENTATION CHOICE.**
12. **The module has six tests, not four**: §2.4's test 4 is three tests (code is not read; what
    names nothing of the source is not found; the path rule checks existence), so that each fails
    under its own breakage. **IMPLEMENTATION CHOICE.**
13. **Test 3 also checks the line each planted form is reported on**, so that a scan that read
    docstrings but misnumbered them fails. **IMPLEMENTATION CHOICE.**
14. **The path rule strips trailing `.,;:` before the existence check**, since prose ends sentences
    with paths; test 4 pins it (`docs/client-contract.md.`). **IMPLEMENTATION CHOICE.**
15. **"Test N" labels: removed where they pointed at the source prompt's numbering**
    (`test_copy_move_store`, `test_delete_store`, `test_shardedpool_shard_paths`, whose docstrings
    cite the source's "§3 tests"), **kept in `test_store_inventory`**, whose own docstring numbers
    its tests 1–10. Correction 3's rule applied to a label that is not a runtime string.
    **IMPLEMENTATION CHOICE.**
16. **Four bare "prompt NN" of this campaign in ported modules are qualified** "extraction prompt
    NN" (rule 5; §1.2). **IMPLEMENTATION CHOICE.**
17. **Breakage (e) was also run together with (b)**, to show test 1 no longer sees (b) (§5).
    **IMPLEMENTATION CHOICE.**
18. **The breakage suites ran three, then two, at a time**, which is why they took 186–554 s against
    about 230 s alone. **IMPLEMENTATION CHOICE.**
19. **`venv-high` was resolved `--offline` from `uv`'s cache**; nothing was downloaded.
    **IMPLEMENTATION CHOICE.**
20. **Slips caught before the commit.** Four edits were first wrong, and the checks I ran on the
    whole diff found each: a range that started a line early in `tools/sharded_store.py` dropped
    "the store is the caller's job." (seen in the diff before any test ran); a closing-line splice
    in `tests/shard_store_fixtures.py` and a range that ended two lines early in
    `tests/test_shard_file_name.py` each repeated a clause (found by a duplicate-word check); and
    the appendix's `SQL/ShardedPool.py:801` was at first left out (found by test 1, and then by a
    check that every appendix and correction 3 line lies inside an edit, which now holds for all
    281). Each was fixed in the edit lists and the tree rebuilt; nothing was run on, or committed
    from, the faulty state except the checks that found it. **UNINTENDED DRIFT** (corrected; no
    effect on any result).

No other UNINTENDED DRIFT was found.

## 3. The hazards (§3)

1. **A docstring keeps its sense.** Every module docstring that opened with a citation now opens
   with what the module is about (e.g. `test_foreign_key_check`: "Every shard of a store written
   the way production writes it passes SQLite's own ``PRAGMA foreign_key_check`` with no row.").
   §1.2's tables give each rewritten sentence; a word-level check (every word the rewrite removed,
   per file, less the citations) found nothing of an explanation dropped.
2. **The AST check** (§4.3) passes for every changed file but the two declared. No docstring was
   turned into a comment or dropped. `black` moved one docstring's closing quotes onto their own
   line (`test_reconcile_at_open.py`, `TestPruningAfterRepair`), which changes only the docstring's
   value.
3. **`--help`** carries the seven phrases verbatim, and no citation (§4.5).
4. **No client vocabulary added.** The guard passes with `KNOWN_HITS` empty; the one client word
   in a test's prose that a citation carried (`quadsource`, `test_foreign_key_check.py:9`) went
   with it.
5. **`test_layer_is_generic.py`**: its vocabulary, rules and the clients' names stay; `:178` is
   decided in §1.2.
6. **The module passes its own scan**; its prose quotes no forbidden form, and its planted forms
   are runtime strings.
7. **A sentence citing both.** Only the source's part went: in `tests/schema_description.py` the
   docstring's `store-fingerprint` and `prompts/datastore-integrity` citations went, and `:193`'s
   "(prompt 04a, U20)", this campaign's, stays (qualified "extraction prompt 04a", rule 5), as in
   `tests/test_schema_builder.py:44`; `tests/test_declared_facts.py:60` ("README §6.2, U22; U20's
   filter", this campaign's) is unchanged.
8. **Line numbers move.** Citations made before 09 are not updated; this log cites `452b3c9`'s
   numbers, and 09's tree where it says so.
9. **`docs/`, `PROVENANCE.md`, `README.md`** are untouched (§4.5, the staged list).

## 4. Verification performed

### 4.1 The suite

| Where | Before (`b5b1586`) | After (this tree) |
|---|---|---|
| `venv/`: Python 3.12.15 / Ray 2.43.0 / SQLAlchemy 2.0.39 / SQLite 3.53.4 | `Ran 480 tests in 520.988s` `OK` | `Ran 486 tests in 229.458s` `OK` |
| scratch `venv-high`: Python 3.13.16 / Ray 2.55.1 / SQLAlchemy 2.0.46 / SQLite 3.53.4, an export of this tree installed editable, run from the export's root (`datastorekit.__file__` is the export's) | (08b's: 480 OK, 4 `ResourceWarning` lines) | `Ran 486 tests in 456.608s` `OK`, **4** `ResourceWarning` lines |

N, the loader's count for the new module, is 6: 480 + 6 = 486. No count fell. The high-end venv:
`uv venv --offline -p /opt/local/bin/python3.13`, `uv pip install --offline "ray==2.55.1"
"sqlalchemy==2.0.46"`, `uv pip install --offline --no-deps -e <export>` (uv 0.12.20).

### 4.2 The module on the unrewritten tree (addition 2)

In a whole-tree export of `HEAD` (`b5b1586`, whose `datastorekit/` is `452b3c9`'s) with the module
copied in, run from the export's root (`datastorekit.__file__` the export's): `Ran 6 tests`,
`FAILED (failures=1)`, test 1 alone, naming 281 hits on **181 lines in 42 files**. Compared with my
parse of the appendix, the 181 are exactly its unstarred lines less the nine SHA lines (none
missing, none extra). Tests 2–6 pass.

### 4.3 Only prose changed (§4.3)

Method: for each `.py` under `datastorekit/` that differs from `452b3c9` (`git diff --name-only
452b3c9 -- datastorekit`, and the untracked module), `ast.dump` of `git show 452b3c9:<path>` and of
the tree's file, each with every module, class and function docstring's value set to `""`, compared.
Output, file by file (paths under `datastorekit/`):

```
SQL/Datastore.py: equal
SQL/ShardedPool.py: equal
SQL/factory_base.py: equal
SQL/schema.py: equal
_timing.py: equal
contract.py: equal
defaults.py: equal
replication.py: equal
shard_paths.py: equal
store_inventory.py: equal
store_reader.py: equal
tests/real_store_fixtures.py: equal
tests/schema_description.py: equal
tests/shard_store_fixtures.py: equal
tests/standin_pool.py: equal
tests/test_absolute_shard_record_refused.py: equal
tests/test_closed_store_refusals.py: equal
tests/test_copy_move_store.py: equal
tests/test_declared_facts.py: equal
tests/test_delete_store.py: equal
tests/test_drop_refuses_dangling_references.py: equal
tests/test_foreign_key_check.py: equal
tests/test_inventory_declarations.py: equal
tests/test_layer_is_generic.py: DIFFERENT
tests/test_layer_registry.py: equal
tests/test_one_timestamp_per_write.py: equal
tests/test_prose_names_no_source.py: NEW (no blob at 452b3c9)
tests/test_prune_at_open.py: equal
tests/test_read_only_pool.py: equal
tests/test_reconcile_at_open.py: equal
tests/test_replicated_write.py: equal
tests/test_schema_builder.py: equal
tests/test_shard_file_name.py: equal
tests/test_shard_key_audit_copy.py: equal
tests/test_shard_key_audit_refusals.py: equal
tests/test_shard_paths.py: equal
tests/test_sharded_store_script.py: equal
tests/test_shardedpool_shard_paths.py: equal
tests/test_store_inventory.py: equal
tests/test_store_reader.py: equal
tests/test_store_schema.py: equal
tests/test_version_row_at_open.py: equal
tools/shard_key_audit.py: equal
tools/sharded_store.py: equal
```

42 equal. `tests/test_layer_is_generic.py` differs, and the unified diff of the two dumps is one
hunk: `KNOWN_HITS["test_no_comment"]`'s
`List(elts=[Constant(value='datastorekit/tools/shard_key_audit.py:188 wavenumber')])` became
`List(elts=[])`. The new module has no blob at `452b3c9`. Comments are not in the AST. Under (h)
the check names `tests/test_shard_paths.py: DIFFERENT` (§5).

### 4.4 The measurement after (§4.4)

- **Tier A's rules: 0.** Test 1 passes.
- **The source's SHAs**: `b04671f`, `a2bd966` and `e53f323` are in no comment or docstring. Every
  7–40-character hex word left in prose is the import commit `6f7f291` (`_timing.py:3`,
  `defaults.py:2`, rule 4); every `[NN-…]` issue name left is this repository's
  (`[01-package-prose-names-sgks-layout]` in the guard's docstring; 05, 02 and 06 in the modules
  08a and 08b added). `test_shard_key_audit_refusals.py:193`'s `"a2bd966"` is code, and stays.
- **Log 03a §8's method**, reimplemented (`tokenize` over every tracked `.py` under
  `datastorekit/`, the physical lines of `COMMENT` and `STRING` tokens matching the board's
  pattern within the token's own span, `Datastore.<module>` with `\b`, the two provenance
  docstrings excluded, an existing `docs/` path not counted, `shard_key_audit.py`'s `e.g.
  "wavenumber"` counted by hand when present). It reproduces 102 / 19 at `8bc60a5`, 114 / 23 at
  `72cf34a`, 124 / 28 at `ae94aaa`, 146 / 35 at `7ceed25`, 155 / 40 at `0c66505` and 155 / 40 at
  `452b3c9`. On this tree, with the new module tracked: **17 lines in 1 file**, every one a runtime
  string of `tests/test_prose_names_no_source.py` (lines at 09's tree), which §2.4 does not read:
  - `:73`, the name rule's pattern string;
  - `:167`–`:179`, thirteen of the planted forms (`Datastore/shard_paths.py`,
    `tools/shard_key_audit.py`, `prompts/a-campaign/README.md`, `docs/no-such-document.md`,
    `Datastore.SQL.ShardedPool`, `Datastore.object`, "the repository root", `REPO_ROOT`,
    `ObjectFactories`, `RunRegistry`, `main.py`, `config.defaults`, `utilities.py`);
  - `:192`, `"datastorekit/tools/sharded_store.py"`, a form test 4 must not find (the method's
    unanchored `tools/` matches it);
  - `:285`–`:286`, test 4's expected message and its planted missing path
    `docs/client-contract.txt`.
- **What remains of each pattern in prose** (comments and docstrings, every file): `Datastore/`,
  `tools/`, `prompts/`, `Datastore.<module>`, "repository root", `REPO_ROOT`, `ObjectFactories`,
  `RunRegistry`, `main.py`, `config.defaults`, `utilities.py`, `var/` and the six campaign names:
  **0** each. `docs/`: 6 lines, all this repository's own existing paths
  (`tests/client/__init__.py:3`, `tests/client/factories.py:3`, `tests/client/registry.py:15`,
  `tests/test_neutral_client.py:4`: `docs/client-contract.md`; `tests/test_layer_is_generic.py:25`,
  `:65`: `docs/extraction/measure_client_vocabulary.py`). `REPO_ROOT` remains only as a name in code
  (`tests/test_layer_is_generic.py`, `test_layer_registry.py`, `test_inventory_declarations.py`,
  `test_store_inventory.py`, `test_store_reader.py`), which §2.4 does not read.
- **Every tier C line** is decided in §1.2 (57 rewritten, 1 kept).
- **The last reading pass** over the 42 files (and the rest of the package): a wide net over all
  4,353 prose lines (labels such as `[A-Z]{1,3}\d+`, `§`, "audit", "probe", "sweep", "baseline",
  "production", "campaign", "fix", "once/until/since", dates, "registry", "config", "command line",
  "prompt", "log", "README", "decision", "issue", "Test N", "script", "standalone", SHAs, and the
  clients' words), 471 lines, read one by one. It found the 48 further lines of §1.2, and after
  their rewrite no citation of the source.

### 4.5 The checks

- `./venv/bin/python docs/extraction/compare_ported_tests.py`: exit 0, its last line
  `OK: 20 module(s) keep their source's tests, classes and assertion skeletons; 1 test(s) declared
  not ported`; the whole output is byte-identical to the run before the rewrite.
- `./venv/bin/black --check datastorekit docs`: `70 files would be left unchanged.` (69 + the module).
- The guard, `datastorekit.tests.test_layer_is_generic`: `Ran 8 tests` `OK`, `KNOWN_HITS` empty.
- `python -m datastorekit.tools.sharded_store --help`: each of hazard 3's seven phrases is present
  (whitespace normalised, as the test reads it), and none of `prompts/`, "repository root",
  "sys.path, so", "sections 6".
- `.py` files under `datastorekit/`: 65 → **66**.
- `git status --short --ignored` before staging: the 43 modified files and the module, plus
  dispatch's ignored entries (`.idea/`, `venv/`, five `__pycache__/`). An empty, untracked `.claude/`
  directory dated 2026-10-09 is in the checkout; it predates this run, git does not list it, and it
  is not touched (§6).

### 4.6 The clients

Read only through `git -C <path> rev-parse` and `status --short`, at the start and at the end:

| Client | Start | End |
|---|---|---|
| SGK `/Users/ds283/Documents/Code/SecondaryGWKit` | `b510bc9` (`handover-remedial`), clean | the same |
| CPBH `/Users/ds283/Documents/Code/ChamPBH` | `52142d7` (`main`), 23 untracked entries | the same |
| SI `/Users/ds283/Documents/Code/StochasticInstantons` | `7bb3efd` (`main`), clean | the same |

No Ray process was running at the start or the end.

## 5. The deliberate-breakage record (§4.6)

**Method.** Each diff below was made against the rewritten tree and applied, never committed, to
its own whole-tree export (`git archive HEAD`, then this tree's 43 changed files and the module),
after `git apply --check`; `git apply -R --check` then held. In each export, run from its root
(`datastorekit.__file__` the export's), the new module and the guard ran alone, and then the whole
suite in `venv/`. A count of failures counts sub-tests.

| | Module (6 tests) | Guard (8) | Whole suite (486) |
|---|---|---|---|
| (a) | `FAILED (failures=1)`: test 1, `datastorekit/SQL/ShardedPool.py:173 a path of the source's layout Datastore/shard_paths.py` | OK | `FAILED (failures=1)`, test 1 only |
| (b) | `FAILED (failures=1)`: test 1, `datastorekit/tests/test_replicated_write.py:23 a campaign or directory of the source var/` | OK | `FAILED (failures=1)`, test 1 only |
| (c) | `FAILED (failures=1)`: test 1, twice over: `datastorekit/SQL/Datastore.py:670 a path of the source's layout prompts/a3-v2-readiness` and `… a campaign or directory of the source a3-v2-readiness` | OK | `FAILED (failures=1)`, test 1 only |
| (d) | **OK** (no rule matches a table name) | `FAILED (failures=1)`: `test_no_comment`, `[] != ['datastorekit/tools/shard_key_audit.py:189 wavenumber']` | `FAILED (failures=1)`, `test_no_comment` only |
| (e) | `FAILED (failures=4)`: test 2, the three test-side files absent and 20 files `not greater than or equal to 60` | OK | `FAILED (failures=4)`, test 2 only |
| (e) + (b) | `FAILED (failures=4)`: test 2 only; **test 1 passes with (b)'s `var/` in place** | OK | — |
| (f) | `FAILED (failures=40)`: test 3, the 20 forms in a module docstring and in a function docstring (the comments still found) | OK | `FAILED (failures=40)`, test 3 only |
| (g) | `FAILED (failures=5)`: test 1 on the six lines of this repository's `docs/` paths (`tests/client/__init__.py:3`, `tests/client/factories.py:3`, `tests/client/registry.py:15`, `tests/test_layer_is_generic.py:25`, `:65`, `tests/test_neutral_client.py:4`); test 4's existence test; test 4's `docs/client-contract.md` in each of three kinds of prose | OK | `FAILED (failures=5)`, the module only |
| (h) | OK | OK | **`Ran 486 tests` `OK`**; §4.3's check names `datastorekit/tests/test_shard_paths.py: DIFFERENT` |
| (i) | `FAILED (failures=4)`: test 1 on correction 1's five lines (`datastorekit/SQL/Datastore.py:589`, `datastorekit/contract.py:15`, `:36`, `:43`, `datastorekit/tests/test_version_keyed_lookups.py:6`, at 09's tree, each `a module of the source Datastore.object`); test 4's `Datastore.object_get` in each of three kinds of prose | OK | `FAILED (failures=4)`, the module only |

Under no breakage did any test outside the module and the guard fail. Line numbers in the table are
at 09's tree.

**(a)** `# see Datastore/shard_paths.py` added to a comment of `SQL/ShardedPool.py`:

```diff
--- a/datastorekit/SQL/ShardedPool.py
+++ b/datastorekit/SQL/ShardedPool.py
@@ -170,6 +170,7 @@
 
         # resolve concerts the supplied db_name to an absolute path, resolving symlinks if necessary
         # this database file will be taken to be the primary database
+        # see Datastore/shard_paths.py
         self._primary_file: PathType = Path(db_name).resolve()
 
         # shard_db_files is a map from shard number -> path representing the database on disk. Every
```

**(b)** "nothing under ``var/``" added to a ported test module's docstring:

```diff
--- a/datastorekit/tests/test_replicated_write.py
+++ b/datastorekit/tests/test_replicated_write.py
@@ -20,7 +20,7 @@
 6. a sharded store still stamps ``datetime.now()``, and writes no record;
 7. no Ray is initialised.
 
-Every store is built in a temporary directory.
+Every store is built in a temporary directory, and nothing under ``var/`` is opened.
 """
 
 import contextlib
```

**(c)** `(prompts/a3-v2-readiness, prompt 03)` restored to its comment in `SQL/Datastore.py`:

```diff
--- a/datastorekit/SQL/Datastore.py
+++ b/datastorekit/SQL/Datastore.py
@@ -667,7 +667,7 @@
         nothing else. A replica's store() may raise ReplicationMismatch, which does not know its
         shard; it is re-raised here naming this actor.
         """
-        # a read-only actor stores nothing
+        # a read-only actor stores nothing (prompts/a3-v2-readiness, prompt 03)
         if getattr(self, "_read_only", False):
             items = objects if isinstance(objects, (list, tuple)) else [objects]
             raise ReadOnlyWrite(
```

**(d)** `tools/shard_key_audit.py:188`'s comment restored as it was:

```diff
--- a/datastorekit/tools/shard_key_audit.py
+++ b/datastorekit/tools/shard_key_audit.py
@@ -186,9 +186,9 @@
     print(f">> shard_keys row count: {len(key_serials)}")
     print(f">> per-shard key distribution: {distribution}")
 
-    # Cross-file check against the actual shard-key table, which lives in the
-    # replicated tables inside each shard database, not in the primary file.
-    # Best-effort: attach one shard file read-only.
+    # Cross-file check against the actual shard-key table (e.g. "wavenumber"),
+    # which lives in the replicated tables inside each shard database, not in
+    # the primary file. Best-effort: attach one shard file read-only.
     cross_file_done = False
     if key_type is not None and shard_files:
         shard_serial, shard_filename = shard_files[0]
```

**(e)** the walk restricted to the layer (the tests skipped):

```diff
--- a/datastorekit/tests/test_prose_names_no_source.py
+++ b/datastorekit/tests/test_prose_names_no_source.py
@@ -94,7 +94,9 @@
 def package_files(top: Path = TOP) -> list:
     """Every ``.py`` file under the package, relative to ``top``, sorted."""
     return sorted(
-        path.relative_to(top).as_posix() for path in (top / PACKAGE).rglob("*.py")
+        path.relative_to(top).as_posix()
+        for path in (top / PACKAGE).rglob("*.py")
+        if "tests" not in path.relative_to(top / PACKAGE).parts
     )
 
 
```

**(f)** docstrings not read (comments only):

```diff
--- a/datastorekit/tests/test_prose_names_no_source.py
+++ b/datastorekit/tests/test_prose_names_no_source.py
@@ -126,7 +126,7 @@
 
 def prose_lines(source: str) -> list:
     """(line, text) of every physical line of prose in ``source``: its comments and docstrings."""
-    spans = _docstring_spans(ast.parse(source))
+    spans = []
     lines = []
     for token in tokenize.generate_tokens(io.StringIO(source).readline):
         if token.type == tokenize.COMMENT:
```

**(g)** the existence check dropped from the path rule:

```diff
--- a/datastorekit/tests/test_prose_names_no_source.py
+++ b/datastorekit/tests/test_prose_names_no_source.py
@@ -152,8 +152,6 @@
     for line, text in prose_lines(source):
         for name, pattern in RULES:
             for match in pattern.finditer(text):
-                if name == _PATH_RULE and _exists(match.group(0), top):
-                    continue
                 found.append(f"{rel}:{line} {name} {match.group(0)}")
     return found
 
```

**(h)** a docstring edit that also changes a statement (an assertion's string):

```diff
--- a/datastorekit/tests/test_shard_paths.py
+++ b/datastorekit/tests/test_shard_paths.py
@@ -1,5 +1,5 @@
 """
-The shard-path resolver, ``datastorekit/shard_paths.py``, as a pure function.
+The shard-path resolver, ``datastorekit/shard_paths.py``, as one pure function.
 
 ``resolve_shard_path(primary, stored)`` is the one definition of where the shard that a
 ``shards.filename`` record names lives. It always returns a file in the primary's directory:
@@ -96,7 +96,7 @@
             self.assertIsNone(shard_file_problem(good))
             self.assertIn("does not exist", shard_file_problem(root / "missing.sqlite"))
             self.assertIn("not a regular file", shard_file_problem(directory))
-            self.assertIn("symbolic link", shard_file_problem(link))
+            self.assertIn("symbolic", shard_file_problem(link))
             self.assertIn("symbolic link", shard_file_problem(dangling))
 
 
```

**(i)** the module rule's trailing boundary dropped:

```diff
--- a/datastorekit/tests/test_prose_names_no_source.py
+++ b/datastorekit/tests/test_prose_names_no_source.py
@@ -64,7 +64,7 @@
         "a module of the source",
         re.compile(
             r"(?<![\w.])Datastore\.(?:SQL|tests|replication|contract|object|shard_paths"
-            r"|store_reader|store_inventory)(?!\w)"
+            r"|store_reader|store_inventory)"
         ),
     ),
     (
```

## 6. Observations not acted on

1. **No rule matches `logs/`** (correction 3). The source's two `logs/` paths are gone; a future one
   would be found only by review, as U40 leaves the source's commits and bare citations. Not a
   defect of the module, which is U40's design; no issue opened.
2. **`tests/test_store_inventory.py:8`** says "solver serials, cosmology names" of what is not
   identity: a client's domain in a test's prose. It cites nothing of the source's records, and the
   guard does not scan tests; left as it is. No issue opened.
3. **`tests/test_shard_key_audit_copy.py:15`–`:16`** says the module does not import
   `datastorekit.shard_paths`; it does not itself, but `shard_store_fixtures`, which it imports, does.
   The sentence's purpose (running the test against an unfixed tool) holds, since the tool is run
   in a subprocess. Left as it is.
4. **An empty `.claude/` directory** (2026-10-09) is in the checkout, untracked and not listed by
   git. It predates this run and is not this prompt's.
5. **The scratch tools** (the edit lists and their applier, the AST check, the word and four-word
   checks, the two measures, the breakage runner) are in the session scratchpad, not in the
   repository.

## 7. Issues

- **Closed:** `[01-package-prose-names-sgks-layout]` (the board's §4).
- **Opened:** none. **Narrowed:** none.

The index is at **4 open**: 0 on this repository's boards, 4 inherited.

## 8. State handed to the next prompt

- `datastorekit/`: prose rewritten; `KNOWN_HITS` empty; `datastorekit/tests/test_prose_names_no_source.py`
  (6 tests). 486 tests at both ends. The version stays `0.2.0`; 10 releases `v0.2.1`.
- The board's §3 holds no issue of this repository; the index says 4, all inherited.
- The port check and `black` (70 files) pass; the clients are as at dispatch.
