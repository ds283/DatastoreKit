# Open issues — project-wide index

One line per open issue, pointing at the board that holds it. The board is right if the two
disagree. See `CLAUDE.md` for the maintenance rule.

**Last updated:** 2026-10-07 · **7 open**: 3 on this repository's boards, 4 inherited (§1.2).

## 1. By campaign

### 1.1 `extraction` ([board](../prompts/extraction/IMPLEMENTATION_STATE.md))

| Issue | Hook |
|---|---|
| `[01-package-prose-names-sgks-layout]` | 101 prose lines in the package name SGK's paths and campaigns; two describe the removed `sys.path` bootstrap |
| `[01-ported-tests-use-sgk-table-names]` | The ported fixture and tests use SGK's table names (`wavenumber`, `GkSource`), which 04's vocabulary guard would find |
| `[01-no-ported-test-pins-the-shard-key-assignment]` | No test reaches `_assign_shard_keys`, so the `key_id` binding of the shard-key bug fails none of the 90; for 03 |

### 1.2 Inherited from SecondaryGWKit, on SGK's boards

These are open issues in the layer's code as SGK carries it. They move here with the code, but
their measurements stay on SGK's boards, in `/Users/ds283/Documents/Code/SecondaryGWKit/prompts/`.
The extraction campaign does not act on them (its README §1). Each is re-checked against the
package once 01 lands, and taken over by a board here when a campaign is planned to address it.

| Issue | SGK board | Hook |
|---|---|---|
| `[00-a-drop-action-drops-a-replicated-table-outside-the-in-flight-record]` | `a3-v2-readiness` | Actors drop a replicated table in their constructors, outside the in-flight record, so an interrupted drop leaves shards the check at open refuses |
| `[00-a-new-stores-first-open-can-leave-a-primary-without-its-shards]` | `a3-v2-readiness` | An interrupted first open leaves a primary whose next open is refused for a missing shard |
| `[00-the-inventory-cannot-see-a-serial-split]` | `datastore-integrity` | The inventory compares replicated classes by key, tags, `validated` and count, not by serial |
| `[01-cross-filesystem-move-advice-says-delete-by-hand]` | `store-retirement` | A failed cross-filesystem move advises deleting the source by hand |
