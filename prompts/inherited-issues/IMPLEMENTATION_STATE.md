# inherited-issues — board

**Last updated:** 2026-10-12 · **Status: OPEN — no prompts; holds 4 issues handed over by SGK on
2026-10-12, each until a campaign takes it over.**

**Plan:** [`README.md`](README.md) ·
**Index:** [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) §1.2

> **Maintenance rule.** Whenever an entry is added to, narrowed in, or closed out of §3 or §4
> below, [`docs/OPEN_ISSUES.md`](../../docs/OPEN_ISSUES.md) is updated **in the same commit**. See
> `CLAUDE.md`.

Code is cited at `6465a6a`, where each defect was read in the package on 2026-10-12. Each entry
names the SGK board entry it came from; SGK's measurements were taken on SGK's copy of the layer,
before `datastorekit` replaced it, and are restated here with the package's names.

---

## 3. Active and unresolved issues

- **[00-a-drop-action-drops-a-replicated-table-outside-the-in-flight-record]** — *opened
  2026-10-02 by SGK's `a3-v2-readiness` orchestrator; read, not measured; handed over 2026-10-12.
  From: SGK `prompts/a3-v2-readiness/IMPLEMENTATION_STATE.md` §4. Unassigned.*
  - **The defect.** A table named in `ShardedPool`'s `drop_tables` is passed to every actor
    (`SQL/ShardedPool.py:344`), and each actor drops it from its own shard in its constructor
    (`SQL/Datastore.py:142` → `_drop_tables`, `:438-470`) and recreates it empty in
    `_ensure_tables` (`:427-430`). Nothing records the drop. For a replicated table this is a
    replicated write made outside the `replication_in_flight` record, and the only one left: the
    version row and the prune at open of a replicated class are the pool's, each under a record
    (`SQL/ShardedPool.py:299-302` for the prune).
  - **Impact (inferred, from the code).** A drop of a replicated table interrupted between actors
    leaves its rows on some shards and not on others. The check at open
    (`_reconcile_replicated_tables`, `SQL/ShardedPool.py:297`) then refuses the store, and there is
    no record to repair it from. In SGK this is reached by `main.py --drop gk-source-policy-records`,
    which maps to a replicated class; SGK's A3 v2 launch passed no `--drop`.
  - **Next step.** The remedy has the shape of the prune's: the pool drops replicated tables
    itself, before any actor exists, under a record, and passes actors only the sharded ones.
    Measure first on stand-in shards (as SGK's audit V1 case 4 did for the prune): interrupt a
    replicated drop between shards and confirm the refusal at open.

- **[00-a-new-stores-first-open-can-leave-a-primary-without-its-shards]** — *opened 2026-10-02
  by SGK's audit 00, V1; handed over 2026-10-12. From: SGK
  `prompts/a3-v2-readiness/IMPLEMENTATION_STATE.md` §4. Unassigned.*
  - **The defect.** For a new store, `ShardedPool` writes the primary and its `shards` table first
    (`SQL/ShardedPool.py:248-271`: `_create_engine`, `_write_shard_data`), and each shard file is
    created afterwards by its actor's constructor (`:332-348`). Interrupted in between, the next
    open finds the primary, reads its shards, and `_check_shard_files` (called at `:292`, defined
    at `:1183`) refuses the store for a shard that does not exist.
  - **Measured** (SGK's `version_window_probe.py`, cases 1 and 2, 2026-10-02): the refusal names
    `shard #0 … which does not exist; shard #1 … which does not exist`, and in the second case
    `shard #1 … which does not exist`.
  - **Narrowed, not closed** (SGK `a3-v2-readiness` prompt 02, 2026-10-03, carried into the
    package): every actor's constructor is submitted at once, so the later shards no longer wait on
    the first actor's constructor, its version insert and a `ray.get`; and the version row is
    written after the last shard file exists.
  - **Impact.** None to data: the store is empty. But a person must delete it before it can be
    built, since an open refuses it and a client's build path typically refuses an existing path
    (SGK's `--build` does; `--build --resume` checks the store first).
  - **Next step.** SGK decided "record only" (its U2, 2026-10-02). Here, either make the first open
    create the shard files before the primary's `shards` rows are committed, or make the refusal
    say that a primary whose shards are all absent and which holds no version row is an
    interrupted creation, safe to delete with `ShardedPool.delete_store(primary, resume=True)`
    (`SQL/ShardedPool.py:2704`; `resume=True` accepts missing shards).

- **[00-the-inventory-cannot-see-a-serial-split]** — *opened 2026-09-25 by SGK's
  `datastore-integrity` audit; handed over 2026-10-12. From: SGK
  `prompts/datastore-integrity/IMPLEMENTATION_STATE.md` §4. Unassigned.*
  - **The defect.** The structured inventory (`store_inventory.py`) compares a replicated class
    across shards by each record's canonical form: key, tags, `validated` and value count
    (`_combine`, `:826`, the `replicated-divergence` problem at `:855`; the module docstring,
    `:54-55`). It does not compare serials, the `source`/`response` flags, timestamps or value
    contents. A store holding a serial split, or shards that disagree on a flag, reads with no
    problem.
  - **Measured** (SGK audit §4.3, `replicated_divergence_probe.py`, 2026-09-25, on the layer as it
    then was in SGK): stores with those differences produced no inventory problem and fingerprinted
    clean.
  - **Impact.** A fingerprint built on `read_inventory` (as SGK's `RunRegistry` store fingerprint
    is) is not evidence that a store's replicated tables agree. The check at open
    (`_reconcile_replicated_tables`) is that evidence for any store the package opens; the
    inventory reads stores it may not open.
  - **Next step.** Decide whether the inventory should report replicated agreement on serials and
    flags as well, or say in its docstring that it does not.

- **[01-cross-filesystem-move-advice-says-delete-by-hand]** — *opened 2026-09-25 by SGK's
  `store-retirement` prompt 01; narrowed and the package's half handed over 2026-10-12, at the
  user's decision. From: SGK `prompts/store-retirement/IMPLEMENTATION_STATE.md` §3, which keeps
  SGK's half. Unassigned.*
  - **The defect.** When `ShardedPool.move_store` fails with `EXDEV`, `_failure_message`
    (`SQL/ShardedPool.py:3000`) appends "copy it instead, and then delete the source by hand"
    (`:3026-3030`); `move_store`'s docstring says the same (`:2683-2684`). The package has
    `ShardedPool.delete_store` (`:2704`), so advising a deletion by hand is its own defect.
  - **Measured.** SGK `store-retirement` log 01, "Observations not acted on", item 1. The text is
    asserted verbatim by `datastorekit/tests/test_copy_move_store.py:606`, in
    `test_move_across_filesystems_fails_before_anything_moves` (`:596`).
  - **Impact.** Low, and only on a failed move across filesystems. Nothing acts on the advice. For
    a client that registers stores, the package's advice can contradict the client's own rule: SGK
    relays the message verbatim from `store move`, and its rule is that a registered store is
    retired, never deleted by hand (SGK's decision 6.1.1). That half, how SGK presents the advice,
    stays on SGK's board.
  - **Next step.** Reword the advice to name `ShardedPool.delete_store` (copy, then delete the
    source with it), in the message and the docstring, and change the test's assertion with it.

---

## 4. Resolved issues

None.
