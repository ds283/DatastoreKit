# Campaign index

One line per campaign under `prompts/`. It is an index: the campaign's `README.md` holds the plan
and its `IMPLEMENTATION_STATE.md` the status; if this file and a board disagree, the board is
right.

**Last updated:** 2026-10-09 · 1 campaign: 1 in progress.

| Campaign | Status | Opened → last board update | Owns | Open issues |
|---|---|---|---|---|
| [`extraction`](extraction/IMPLEMENTATION_STATE.md) | **in progress**: 10 of 14 written (01, 02, 03a, 03b, 04a, 04b, 05, 06, 07a, 08a), 9 landed (01, `8bc60a5`; 02, `e988e69`; 03a, `11247c7`; 03b, `0d5380c`; 04a, `7ceed25`; 04b, `0c66505`; each reviewed; 05, `68db557`, reviewed, CI green at both ends, tagged `v0.1.0`; 06, `240028e`, reviewed, CI green at both ends, tagged `v0.2.0`; 07a, `dd45243`, the adoption checklists, reviewed); 07b withdrawn: the four open issues are fixed (08a, 08b, 09) and released as `v0.2.1` (10) before 11 closes (U33); G1 holds (import commit SGK `6f7f291`); U2–U5 and U8–U13 taken 2026-10-07, U14–U22 2026-10-08, U6 and U23–U37 2026-10-09 | 2026-10-07 → 2026-10-09 | moving SGK's generic `Datastore` / `ShardedPool` layer into `datastorekit`; a test suite with no client; `key_on_version`; releases `v0.1.0`, `v0.2.0` and `v0.2.1`; the clients' adoption checklists | §1.1; 4 |
