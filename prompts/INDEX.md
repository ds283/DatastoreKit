# Campaign index

One line per campaign under `prompts/`. It is an index: the campaign's `README.md` holds the plan
and its `IMPLEMENTATION_STATE.md` the status; if this file and a board disagree, the board is
right.

**Last updated:** 2026-10-10 · 2 campaigns: 1 planned, 1 closed.

| Campaign | Status | Opened → last board update | Owns | Open issues |
|---|---|---|---|---|
| [`extraction`](extraction/IMPLEMENTATION_STATE.md) | **closed** 2026-10-10 by prompt 11: 14 of 14 written prompts landed (01, `8bc60a5`; 02, `e988e69`; 03a, `11247c7`; 03b, `0d5380c`; 04a, `7ceed25`; 04b, `0c66505`; 05, `68db557`, tagged `v0.1.0`; 06, `240028e`, tagged `v0.2.0`; 07a, `dd45243`; 08a, `f938844`; 08b, `efedc8d`; 09, `cad7bc1`; 10, `33778b0`, tagged `v0.2.1`; 01–10 each reviewed, and each tag made after CI was green at both ends; 11, `39b1348`, reviewed, the verification document `docs/extraction-verification.md`, a smoke run under real Ray at both ends and the pin installed from GitHub); 07b withdrawn (U33); G1 holds (import commit SGK `6f7f291`); G2–G4 open, recorded on the board as they hold; U2–U5 and U8–U13 taken 2026-10-07, U14–U22 2026-10-08, U6 and U23–U37 2026-10-09, U38–U42 2026-10-10 | 2026-10-07 → 2026-10-10 | moving SGK's generic `Datastore` / `ShardedPool` layer into `datastorekit`; a test suite with no client; `key_on_version`; releases `v0.1.0`, `v0.2.0` and `v0.2.1`; the clients' adoption checklists | §1.1; 0 (its one issue, `[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]`, assigned to `actor-names` 2026-10-10) |
| [`actor-names`](actor-names/IMPLEMENTATION_STATE.md) | **planned**: 1 of 2 written (01, ready to dispatch); 0 landed; 02, the release `v0.2.2`, planned; U1–U3 taken 2026-10-10 | 2026-10-10 → 2026-10-10 | a closed pool, and a refused open, releasing their Ray actors' names; the stand-in pool reserving names; the release `v0.2.2` (U3) | §1.3; 1 (`[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]`, held on the extraction board) |
