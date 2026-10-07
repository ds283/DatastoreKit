# DatastoreKit

A sharded SQLite datastore driven by [Ray](https://www.ray.io/) actors. A client project declares
its tables through object factories; DatastoreKit holds the rows across one primary file and a
set of shard files, replicates the small lookup tables to every shard, routes the large tables to
one shard by a shard key, and checks the store's integrity each time it is opened.

**Status: being extracted.** The code does not live here yet. It is the `Datastore` / `ShardedPool`
layer of [SecondaryGWKit](https://github.com/ds283/SecondaryGWKit), made generic there by its
`datastore-generic` campaign (closed 2026-10-06), and is shared in origin with ChamPBH and
StochasticInstantons, each of which carries its own diverged copy. The plan for moving it here,
and for the three projects to depend on one copy, is
[`prompts/extraction/README.md`](prompts/extraction/README.md); its status board is
[`prompts/extraction/IMPLEMENTATION_STATE.md`](prompts/extraction/IMPLEMENTATION_STATE.md).

`RayWorkPool` is not part of this package (yet): reconciling it across the three projects is a
separate unit of work.

## Licence

Apache License 2.0; see [`LICENSE`](LICENSE).
