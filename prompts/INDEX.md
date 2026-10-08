# Campaign index

One line per campaign under `prompts/`. It is an index: the campaign's `README.md` holds the plan
and its `IMPLEMENTATION_STATE.md` the status; if this file and a board disagree, the board is
right.

**Last updated:** 2026-10-08 · 1 campaign: 1 in progress.

| Campaign | Status | Opened → last board update | Owns | Open issues |
|---|---|---|---|---|
| [`extraction`](extraction/IMPLEMENTATION_STATE.md) | **in progress**: 5 of 9 written (01, 02, 03a, 03b, 04a), 5 landed (01, `8bc60a5`; 02, `e988e69`; 03a, `11247c7`; 03b, `0d5380c`; 04a, this commit), 4 reviewed; G1 holds (import commit SGK `6f7f291`); U2–U5 and U8–U13 taken 2026-10-07, U14–U21 2026-10-08 | 2026-10-07 → 2026-10-08 | moving SGK's generic `Datastore` / `ShardedPool` layer into `datastorekit`; a test suite with no client; `key_on_version`; releases `v0.1.0` and `v0.2.0`; the clients' adoption checklists | §1.1; 2 |
