# Open issues — project-wide index

One line per open issue, pointing at the board that holds it. The board is right if the two
disagree. See `CLAUDE.md` for the maintenance rule.

**Last updated:** 2026-10-21 · **5 open**, all on this repository's boards (§1.2, §1.4).

## 1. By campaign

### 1.1 `extraction` ([board](../prompts/extraction/IMPLEMENTATION_STATE.md)): campaign closed 2026-10-10 (prompt 11)

None open (2026-10-10: its one issue was closed by `actor-names` prompt 01).

### 1.2 `inherited-issues` ([board](../prompts/inherited-issues/IMPLEMENTATION_STATE.md)): issues handed over by SGK, 2026-10-12

Opened in SGK while the layer was SGK's code, and handed to this repository by SGK's
`dk-and-rpk-migration` prompt 09 (SGK `5943492`). The board holds each in full, measured against
the package. None is assigned to a campaign.

| Issue | Hook |
|---|---|
| `[00-a-drop-action-drops-a-replicated-table-outside-the-in-flight-record]` | Actors drop a replicated table in their constructors, outside the in-flight record, so an interrupted drop leaves shards the check at open refuses |
| `[00-a-new-stores-first-open-can-leave-a-primary-without-its-shards]` | An interrupted first open leaves a primary whose next open is refused for a missing shard |
| `[00-the-inventory-cannot-see-a-serial-split]` | The inventory compares replicated classes by key, tags, `validated` and count, not by serial |
| `[01-cross-filesystem-move-advice-says-delete-by-hand]` | A failed cross-filesystem move advises deleting the source by hand, though `delete_store` exists |

### 1.3 `actor-names` ([board](../prompts/actor-names/IMPLEMENTATION_STATE.md)): campaign closed 2026-10-11 (`v0.2.2`)

`actor-names` prompt 01 closed the one issue assigned to it, on the `extraction` board (2026-10-10).

None open (2026-10-11: `[02-closing-a-pool-can-start-ray]` was closed by `actor-names` prompt 01b).

### 1.4 `extra-values` ([board](../prompts/extra-values/IMPLEMENTATION_STATE.md)): campaign in progress (`v0.5.0`)

Assigned to its prompt 02.

| Issue | Hook |
|---|---|
| `[01-a-new-spec-field-moves-every-spec-guard-digest]` | A client's spec guard that walks a spec's fields sees every digest move under `v0.5.0`; the SGK and ChamPBH addenda must give the one-condition edit |
