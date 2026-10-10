# The client contract

*Measured from the package at `8bc60a5`, whose layer is the source repository's at `6f7f291`
(`PROVENANCE.md`). Every line number below is that tree's; the files it names have not changed
since.*

*§8 is measured from the package at prompt 06's tree (`v0.2.0`). §1–§7 remain as measured at
`8bc60a5`, so their line numbers into the files 06 changes (`contract.py`, `SQL/schema.py`,
`SQL/Datastore.py`, `SQL/ShardedPool.py`) are that tree's.*

*§9 is measured from the package at prompt 08a's tree, and its line numbers are that tree's. Each
of its subsections names the rows of §1–§8 it supersedes; those rows are not rewritten, and carry
a marker.*

*§9.2 is measured from the package at prompt 08b's tree, and its line numbers are that tree's.*

*Added by extraction prompt 11 (2026-10-10). Every line number in §1–§9 is that of the tree its
section states: §1–§7 `8bc60a5`'s (their one citation of the stand-in pool,
`tests/standin_pool.py` in §6, is of prompt 02's tree, `e988e69`, which added that file), §8
`v0.2.0`'s (`240028e`), §9.1 prompt 08a's (`f938844`) and §9.2 prompt 08b's (`efedc8d`). The lines
have moved since those trees.
Prompts 08a and 08b moved `SQL/ShardedPool.py`'s, and prompt 09 rewrote the prose, and so moved the
lines, of 13 layer files and 30 modules under `tests/` (`PROVENANCE.md`, "Prompts 08a, 08b and 09:
fixes and prose (`v0.2.1`)"). Among them are `store_inventory.py`, `store_reader.py` and
`SQL/factory_base.py`, which prompt 06 did not change and which the second paragraph above leaves a
reader to take as unchanged. By `git diff --stat 8bc60a5 33778b0`, the only layer files cited here
that are unchanged are `object.py` and `SQL/ClientPool.py`, and the test client and test modules
cited did not exist at `8bc60a5`. So a line is read at its section's tree (`git show
<tree>:datastorekit/<path>`), and only §8's correction note gives `v0.2.1`'s lines.*

*§9.3 is measured from the package at `actor-names` prompt 01's tree, and its line numbers are
that tree's.*

A client of `datastorekit` gives the layer a fixed set of facts: the arguments of a pool's
constructor, the keys a factory's `register()` returns, the hooks a factory defines, the
inventory declarations, two tables the layer owns, and what its stored objects carry. This
document states each one, where the client gives it, whether it is **required**, **optional** or
**defaulted**, what the layer does with it, and what the layer does when it is wrong or absent.

Each item names the class or argument of the **neutral test client** (`datastorekit/tests/client/`)
that supplies it. The client's tests (`datastorekit/tests/test_neutral_client.py`) show that it
does, and that the layer reads it there.

**Read for.** Some facts are read only for a replicated class, or only for a sharded one. The pool
compares, repairs and prunes **replicated** tables only (`SQL/ShardedPool.py:1123-1126`: "Nothing
in a sharded table is read, repaired or refused on"). A fact read for one kind only is accepted on
the other by the schema builder, and then read by nothing.

Paths are relative to `datastorekit/`.

---

## 1. The pool's constructor

`ShardedPool.__init__` (`SQL/ShardedPool.py:95-114`) takes **16** parameters: six positional and
required, eight defaulted, and two keyword-only (one required, one defaulted). The pool gives every
`Datastore` actor what it needs of them (`:304-320`); a client never constructs an actor itself.

| # | Parameter | Kind (default) | What the layer does with it | When wrong or absent | Neutral client |
|---|---|---|---|---|---|
| 1 | `version_label` | required | The label of the store's `version` row. Found on every shard, read-only, or written once through the recorded replicated write (`:348-354`); every actor is then given its serial (`:355-360`) and stamps it on every row of a `version: True` class. Passed to each actor to name it in a refusal (`:305`). | A read-only pool whose store lacks the label raises `ReadOnlyMiss`, naming the labels it holds (`:529-537`). A read-write pool writes it. | `"standin"`, given by `StandinCluster.open_pool` |
| 2 | `db_name` | required | The primary's path, resolved (`:173`). An absent primary makes a new store, its shards siblings named by `shard_file_name` (`:222-244`); an existing one is opened (`:248-290`). | A directory: `RuntimeError` (`:218-221`). A missing primary with a shard present: `RuntimeError` (`:232-235`). | a path in a `tempfile` directory |
| 3 | `ShardKeyType` | required | A class. Its `__name__` names the shard-key table (`:157`): written to the primary's `shard_key_config` (`:902-905`), compared on every reopen (`:953-969`), and used by the check at open to require that every serial of the primary's `shard_keys` is a row of that table on every shard (`:1507-1525`). A replicated get of that class assigns each new key a shard (`:3243-3246`, `_assign_shard_keys` at `:3505`). | A store made under another name: `RuntimeError` at open (`:957-960`). A get of the class answering objects that are not instances of it: `RuntimeError` (`:3516-3519`). The class must be replicated (§1, row 5), or no key is ever assigned and every sharded call raises `KeyError`. | `registry.shard_key_type` = `objects.keypoint` |
| 4 | `ShardKeyStoreIdGetter` | required | A function from a shard key, or a proxy for one, to the key's `store_id`. Applied to a sharded get's payload field (`:3262`, `:3273`), to `object_get_vectorized`'s and `object_read_batch`'s shard key (`:3295`, `:3322`), and to a sharded object's attribute in a store or validate (`:3415`, `:3500`); the result indexes the pool's shard map. | Whatever it raises propagates. A `store_id` with no assigned shard: `KeyError` from the shard map. | `registry.shard_key_store_id`: a `keypoint`, or its proxy `keypoint_alias` |
| 5 | `replicated_tables` | required | The replicated classes, a list. Written to the primary (`:907-916`) and compared on every reopen (`:971-999`); given to every actor (`:308`). It dispatches a get, store or validate to the replicated write (`:3022`, `:3344`, `:3437`); it is what the check at open compares, with each listed class's tag tables (`:1334-1342`); its classes with `validate_on_startup` are pruned by the pool (`:2094-2103`); `read_table_config` may name only these (`:336-339`). The reader takes the store's own record, not this list (`store_reader.py:143-173`). | A list that differs from the store's record: `RuntimeError` at open (`:996-999`). A class in neither list cannot be got, stored or validated through the pool: `RuntimeError` (`:3028-3030`, `:3352-3354`, `:3445-3447`). A replicated class left out is not compared at open. | `registry.replicated_tables` (11 classes) |
| 6 | `sharded_tables` | required | The sharded classes, mapped to the payload field, and object attribute, that holds the shard key. Written to the primary (`:918-926`) and compared on every reopen (`:1001-1049`). A get is sent to the key's shard (`:3251-3275`), and so are a store and a validate (`:3403-3418`, `:3491-3503`); `object_get_vectorized` and `object_read_batch` accept only these classes (`:3283-3286`, `:3310-3313`); `read_table` refuses them (`:3598-3601`). | A missing field in a payload: `KeyError` (`:3261`, `:3272`); in a shard-key mapping: `RuntimeError` (`:3289-3292`, `:3316-3319`); a missing attribute on an object: `RuntimeError` (`:3409-3412`, `:3494-3497`). A mapping that differs from the store's record: `RuntimeError` (`:1042-1049`), except that a sharded table the store records and the mapping lacks raises `KeyError` at `:1015` before that message is reached *(superseded in part by §9.1)*. | `registry.sharded_tables` = `{"Tessera": "k", "Sample": "k", "Trace": "k", "Weave": "k"}` |
| 7 | `timeout` | defaulted (`None`) | SQLite's busy timeout, for the pool's engine (`:766-768`), every actor's (`:311`; `SQL/Datastore.py:200-202`, `:339-341`), the read-only engine (`:507-509`) and the check at open's (`:1370-1372`). | Not given: SQLite's default. | not given |
| 8 | `shards` | defaulted (`10`) | The number of shards of a **new** store, at least 1 (`:169`, `:226-237`). | For an existing store the primary's records decide; a different number prints a warning (`:287-290`). | `3` (`build_store`'s default), `2`, `1` |
| 9 | `profile_agent` | defaulted (`None`) | A `ProfileAgent` actor handle, given to every actor (`:314`), and cleaned up when the pool exits (`:759-760`). | Not given: no profiling. | not given |
| 10 | `job_name` | defaulted (`None`) | Kept (`:138`). Nothing in the package reads it. | — | not given |
| 11 | `prune_unvalidated` | defaulted (`False`) | Under it, the pool prunes every replicated class whose factory validates at startup, under a "prune" record, after the check at open and before any actor exists (`:275-276`, `:2314-2347`); each actor prunes its sharded classes (`SQL/Datastore.py:459-464`). | A read-only pool given it: `ReadOnlyWrite` before anything is opened (`:486-491`). | not given by `build_store`; a pool may be opened with it |
| 12 | `drop_tables` | defaulted (`None`) | Tables every actor drops when it opens an existing store, in `schema.drop_order`'s order (`:316`; `SQL/Datastore.py:410-441`), then re-creates empty. | A name the registry does not declare as a table: `RuntimeError` before anything is opened (`:705-717`). A drop that leaves another table naming rows of a dropped one (`schema.dependent_tables`): `RuntimeError` before anything is opened (`:719-737`). A read-only pool given any: `ReadOnlyWrite` (`:480-485`). | `registry.tables_to_drop(...)` |
| 13 | `read_table_config` | defaulted (`None`) | Class name → `{"tables_arg": bool}`: the classes `read_table` serves (`:3582-3618`; `SQL/Datastore.py:828-870`). With `tables_arg` true, the actor passes the factory its tables as `tables=` (`SQL/Datastore.py:863-865`). | A class that is not replicated: `RuntimeError` at open (`:334-339`, `:568-573`). A `read_table` with no config, of a sharded class, or of a class not in it: `RuntimeError` (`:3590-3606`). | `registry.read_table_config`: `keypoint` (`tables_arg` False), `dial_setting` (True) |
| 14 | `read_only` | defaulted (`False`) | Opens an existing store with every file `mode=ro`, writing nothing (`:203-209`, `:477-579`). | Refusals of its own: a missing store, a journal, a write (`ReadOnlyWrite`), a miss (`ReadOnlyMiss`). | `StandinCluster.open_pool(..., read_only=True)` |
| 15 | `factories` | **required**, keyword-only | The registry: class name → factory (`:145`). Every table, schema record and hook comes from it: the pool's (`:414`, `:617`, `:711`, `:1166`, `:2320`), every actor's (`:309`; `SQL/Datastore.py:351-397`), the reader's and the inventory's when they are given it (§7). Kept as a copy (`:700-703`). | Not a mapping: the actor raises `RuntimeError` (`SQL/Datastore.py:361-362`). A class it lacks: `RuntimeError` naming it (`SQL/Datastore.py:404-408`). | `registry.factories` (22 classes) |
| 16 | `serial_batch_sizes` | defaulted (`None`), keyword-only | Table → how many serials an actor leases from the broker at a time, given to every actor (`:310`; `SQL/ClientPool.py:109-113`, `:126-131`). | A table it does not name leases 500 at a time (`SQL/ClientPool.py:130`). A name that is no table is never read. | `registry.serial_batch_sizes` |

---

## 2. The keys of `register()`

A factory's `register()` returns a dict, or `None` for a class with no table. The schema builder,
`build_schema(metadata, factories)` (`SQL/schema.py:62-186`), reads **9** keys (`:95-180`). Every
reader of a store builds its tables through it: each actor (`SQL/Datastore.py:382`), the pool
(`SQL/ShardedPool.py:414` and the lines of §1 row 15), the reader (`store_reader.py:220`) and
`dependent_tables` (`SQL/schema.py:352`). A key not among the nine is never read. The table is
named by the registry's key for the factory, and its columns come in the order `serial`,
`version`, `timestamp`, `stepping`, then the factory's own.

| Key | Kind (default) | Read for | What the layer does with it | When wrong or absent | Neutral client |
|---|---|---|---|---|---|
| `validate_on_startup` | defaulted (`False`) | both | Whether the factory's `validate_on_startup` hook runs at open (`:108`). For a **sharded** class each actor reports its unvalidated rows, and prunes them under `prune_unvalidated` (`SQL/Datastore.py:443-477`). For a **replicated** class the actor only reports (`:459-461`); the pool prunes it, under a record, with its unit (`SQL/ShardedPool.py:2094-2103`, `:2314-2347`), and the check at open completes an interrupted prune (`:2349-2440`). A read-only actor reports only (`SQL/Datastore.py:222-261`). | Absent: the hook is never called. | `Gadget` (replicated), `Sample` (sharded) |
| `serial` | defaulted (`True`) | both | An `INTEGER PRIMARY KEY` column `serial` (`:117-122`), leased from the broker for each insert unless the payload gives one (`SQL/Datastore.py:725-742`). | `False`: no `serial`; the table is keyed by the primary key its columns declare, which the check at open compares under (`SQL/ShardedPool.py:1348`). Such a class has no `store_id`, and cannot declare an `inventory_spec` (the inventory reads `serial`, `store_inventory.py:593`). | `serial: False` on `Gadget_tags`, `Sample_tags`, `Sample_members`, `Trace_tags`, `Weave_tags` |
| `version` | defaulted (`False`) | both | A `version` column with a foreign key to the version table's `serial`, indexed (`:125-135`). Every insert carries the pool's version serial (`SQL/Datastore.py:744-745`). | An insert before the pool has set the serial is refused (`SQL/Datastore.py:715-723`). With no version table registered, creating the table fails (no referenced table). | `True` on `keypoint_alias`, `routing_rule`, `Gadget`, `Tessera`, `Sample`, `Trace`, `Weave` |
| `timestamp` | defaulted (`False`) | both | A `timestamp` `DateTime` column (`:137-142`), stamped at insert (`SQL/Datastore.py:746-752`); a replicated write stamps every shard with the one timestamp it chose (`SQL/ShardedPool.py:3088-3089`), and the repair at open copies a row only if its timestamp is the record's start (`:1823-1830`). The inventory reports the earliest and latest (`store_inventory.py:597-599`). | — | `True` on `store_tag`, `keypoint`, `keypoint_alias`, `dial_setting`, `gauge_setting`, `routing_rule`, `Gadget`, `Gadget_tags`, `Tessera`, `Sample`, `Sample_tags`, `Trace`, `Trace_tags`, `Weave`, `Weave_tags`; `False` on the rest |
| `stepping` | defaulted (`False`); `True`, `"minimum"` or `"exact"` | both | A `stepping` `Integer` column (`:144-160`); the record keeps `use_stepping`, and `stepping_mode` (`None` for `True`, else the string). Every insert must carry `stepping` (`SQL/Datastore.py:753-755`). Nothing else in the package reads `stepping_mode`: the modes mean something only to the factory. | An insert without `stepping`: `KeyError` (`SQL/Datastore.py:755`). An unknown string prints a warning and is **ignored**: no column (`SQL/schema.py:145-150`). | `"exact"` on `keypoint_alias`, `"minimum"` on `dial_setting`, `True` on `knob_setting` |
| `columns` | defaulted (`[]`) | both | The factory's own `sqla.Column`s, appended after the prepended ones (`:162-166`). | A column named `serial`, `version`, `timestamp` or `stepping` where that column is prepended: SQLAlchemy's `DuplicateColumnError` at schema build. | every class with a table |
| `owner_column` | optional (`None`) | **replicated only** | The column whose one foreign key names the row this table's rows belong to (`:198-220`). It puts the table in its owner's **unit** (`SQL/ShardedPool.py:2114-2158`): the check at open copies a missing owner with its owned rows as a whole (`:1834-1879`), and a prune of the owner may delete them (`:2185-2236`). | Not a column, or a column with other than one foreign key: `ValueError` at schema build (`SQL/schema.py:206-219`). On a sharded class: accepted, read by nothing. | `GadgetPart` (`gadget_serial`) |
| `monotone_flags` | optional (`()`) | **replicated only** | Boolean columns a get may turn on and nothing turns off (`:223-256`). After an interrupted get, the check at open sets them on a shard where the controlling shard holds them set (`SQL/ShardedPool.py:1700-1706`, `:1773-1785`, `:1938-1955`). | A string, a name that is not a column, or a column that is not `Boolean`: `ValueError` at schema build (`SQL/schema.py:229-255`). On a sharded class: accepted, read by nothing. | `keypoint` (`kp_marked`, `kp_flagged`) |
| `validated_column` | optional (`None`) | **replicated only** | The `Boolean` column of the class's validated flag (`:259-284`). After an interrupted validate of the class, the check at open recomputes it on each shard by the factory's `revalidate` (`SQL/ShardedPool.py:1707`, `:1786-1794`, `:1966-2017`). | Not a column, or not `Boolean`: `ValueError` at schema build (`SQL/schema.py:268-283`). Declared without `revalidate`: the base's `NotImplementedError`, raised at open only when such a repair is made. On a sharded class: accepted, read by nothing. | `Gadget` (`gadget_validated`) |

**`register()` returning `None`** makes a class with no table (`SQL/schema.py:97-104`): its record
holds `"table": None`, and its `build` is given no table and no inserter (`SQL/Datastore.py:394-395`,
`:508-512`). It has no row to compare, prune or count, and the inventory cannot read it. It may be
listed in `replicated_tables`: a get then runs as a replicated write that writes nothing but its
record. *Neutral client:* `ephemeral_probe`.

---

## 3. The factory hooks

A factory is a class whose static methods the layer calls; it is never instantiated, so the
abstractness of `SQLAFactoryBase` (`SQL/factory_base.py`) is never enforced. Subclassing it is how
a factory gets the three defaulted hooks. Ten hooks are called:

| Hook | Kind | Called for | What the layer does with it | When wrong or absent | Neutral client |
|---|---|---|---|---|---|
| `register()` | abstract (`factory_base.py:7-10`) | every class | §2. | — | every factory |
| `build(payload, conn, table, inserter, tables, inserters)` | abstract (`:12-15`) | both | Every get, in the actor, inside one transaction for all of a call's payloads (`SQL/Datastore.py:528-541`). It finds the object or inserts it through `inserter`; a replica's get carries the controller's `serial` in the payload, under which it must insert (§6). The pool also calls the version table's `build` on a `mode=ro` connection with an inserter that raises, to find the version row (`SQL/ShardedPool.py:408-435`). | A `SQLAlchemyError` is printed and re-raised (`SQL/Datastore.py:542-550`). | every factory but the seven association, step and member tables, whose `build` raises |
| `store(obj, conn, table, inserter, tables, inserters)` | abstract (`:17-20`) | both | Every store, in the actor (`SQL/Datastore.py:647-658`). For a replicated class the controlling shard stores the object, and every other shard is given the controller's answer, carrying its serial and those of its owned rows: it inserts under them, or verifies it holds them (`SQL/ShardedPool.py:3361-3401`). | A `ReplicationMismatch` it raises is re-raised naming the actor (`SQL/Datastore.py:656-657`). Not defined: the base's `NotImplementedError`. | `keypoint_alias`, `Gadget` (replicated); `Sample`, `Trace`, `Weave` (sharded) |
| `validate(obj, conn, table, tables)` | abstract (`:22-25`) | both | Every validate, in the actor (`SQL/Datastore.py:782-826`); returns the outcome. For a replicated class, a `True` outcome on the controlling shard is repeated on every other, and each outcome must equal it (`SQL/ShardedPool.py:3454-3489`). | A replica whose outcome differs: `ReplicationMismatch` (`:3470-3482`). `False` or `None` on the controlling shard: nothing is replicated (`:3464-3465`). | `Gadget` (replicated), `Sample`, `Trace` (sharded) |
| `validate_on_startup(conn, table, tables, prune=False)` | abstract (`:27-30`) | both, when `register()` says so | Returns lines describing the unvalidated rows; with `prune=True` deletes them. Called by each actor at open (`SQL/Datastore.py:464`; read-only, `:239-241`) and by the pool's prune of a replicated class (`SQL/ShardedPool.py:2160-2183`, `:2185-2257`), which requires that a second call with `prune=False` reports nothing and that only the class's unit lost rows. | A prune that did not take: `RuntimeError`, the shard rolled back and the record left set (`:2213-2256`). | `Gadget`, `Sample` |
| `revalidate(serial, conn, table, tables)` | defaulted: raises `NotImplementedError` (`:34-48`) | **replicated only** | After an interrupted validate, recompute and write the stored row's validated flag by `validate`'s rule, and return it (`SQL/ShardedPool.py:1966-2017`, the call at `:1992`). A `True` on a shard that held `False` is kept; any other result is rolled back to a savepoint. | A shard holding `True` whose rule gives `False`: refused, `ReplicatedDivergence` (`:2007-2016`). Not defined while `validated_column` is declared: `NotImplementedError` at that open. | `Gadget` |
| `owned_serials(obj)` | defaulted: `None` (`:50-57`) | **replicated only** | The serials of the rows `obj` owns in another table, in order. After a replicated store the controller's and every replica's are compared (`SQL/ShardedPool.py:3377`, `:3386-3394`). | A difference: `ReplicationMismatch`. Not defined: `None` on both sides, so nothing is compared. | `Gadget` (its `GadgetPart` serials) |
| `inventory_spec()` | defaulted: `None` (`:59-62`) | both | An `InventorySpec` (§4), or `None` for a class outside the inventory. Read by `getattr`, so a factory that is not a subclass may lack it (`store_inventory.py:920-930`). It orders and reads the inventory (`:933-1049`), and its declared parents count as references for `dependent_tables` (`SQL/schema.py:366-367`). | §4. | 13 classes |
| `read_batch(payload, conn, table, tables)` | not declared in the base | **sharded only** | `ShardedPool.object_read_batch(cls, shard_key, **payload)` (`SQL/ShardedPool.py:3304-3326`) sends it to the key's shard, with the shard key added to the payload; the actor calls it (`SQL/Datastore.py:563-596`) and takes `len()` of the result (`:583`). | A class not sharded: `RuntimeError` (`SQL/ShardedPool.py:3310-3313`). Not defined: `AttributeError` in the actor. | `Sample` |
| `read_table(conn, table, *args, **kwargs)` | not declared in the base | **replicated only**, those `read_table_config` names | `ShardedPool.read_table(cls, *args, **kwargs)` (`SQL/ShardedPool.py:3582-3618`) sends it to one shard; the actor adds `tables=` when `tables_arg` is true (`SQL/Datastore.py:828-870`). | Not defined: `RuntimeError` (`SQL/Datastore.py:858-861`); §1 row 13 for the rest. | `keypoint` (`tables_arg` False), `dial_setting` (True) |

---

## 4. The inventory's declarations

`store_inventory.py` imports only the standard library, `sqlalchemy` and `contract` at module
scope, so a factory imports these from it.

**`InventorySpec`** (`store_inventory.py:296-333`), **6** fields, all defaulted. `keywords()` hands
them to `read_records` (`:512-807`), which reads them as below; `dependencies()` names every class
the spec references.

| Field | Default | What the layer does with it | When wrong | Neutral client |
|---|---|---|---|---|
| `leaves` | `()` | Columns read into the key, each through `canonical` (`:585-601`, `:718`). | A column the table lacks: `KeyError`. A value that is not `None`, a bool, int, float or string: `TypeError` (`:130-136`). | every spec |
| `parents` | `{}` | Key field → `Parent`, each resolved to the parent's reference digest (`:699-728`). | A parent that cannot be resolved: the row is not a record, and the class has an `unresolved-parent` problem (`:783-793`). | `keypoint_alias`, `Gadget`, `Tessera`, `Sample`, `Trace`, `Weave` |
| `tags` | `None` | `(association table, its column naming this class's serial)`: the row's tag labels, read through the tag table's records (`:604-642`). The tag table is then a dependency (`:331-332`). | Orphan rows: `orphan-tag` problems. | `Gadget`, `Sample`, `Trace`, `Weave` |
| `values` | `None` | `(value table, its column naming this class's serial)`: the count of value rows per row, one `GROUP BY` (`:644-667`). | Orphan rows: an `orphan-value` problem. | `Gadget` (`GadgetPart`), `Trace` (`TraceStep`) |
| `validated` | `None` | The class's validated column, read into the record (`:594-596`, `:772-776`). | A column the table lacks: `KeyError`. | `Gadget`, `Trace` |
| `parent_sets` | `{}` | Key field → `ParentSet` (`:669-697`, `:730-762`). | A row with no members: `empty-parent-set`; orphan members: `orphan-member`. | `Sample` (`members`), `Weave` (`strands`) |

**`Parent`** (`:208-267`), **6** fields: `column` (required), and `of`, `type_column`, `types`,
`nullable`, `cross_shard`. Exactly one of `of` (a class) and `types` (a polymorphic reference's
map from a value of `type_column` to a class) is given, `type_column` with `types` or not at all,
and `types` non-empty, or `ValueError` at construction (`:241-253`). A polymorphic parent's
`type_column` must be one of its class's `leaves`, or `inventory_classes` raises `ValueError`
(`:954-959`). `nullable`: a NULL is a value of the key rather than a missing parent (`:701-702`).
`cross_shard`: the parent row may be on another shard, and is resolved against every shard's rows
of its class (`:704-707`; `_merge_digests`, `:815-827`). *Neutral client:* `of` throughout;
`Gadget.frame` is polymorphic over `dial_setting` and `knob_setting`, and so is `Trace.frame`,
through the same type map; `Sample.anchor` is `nullable` and `cross_shard`, naming a `Tessera`
with no foreign key; `Weave.anchor` is `nullable`, naming a `Tessera` of its own shard.

**`ParentSet`** (`:270-293`), **3** fields: `table` (the member table), `owner` (its column naming
the owning row) and `members` (member field → `Parent`). A polymorphic member raises `ValueError`
at construction (`:287-293`); a member may be `cross_shard`. *Neutral client:* `Sample.members`,
over `Sample_members`, whose rows name a `Tessera` on the Sample's own shard by foreign key; the
member table declares no spec of its own; and `Weave.strands`, over `Weave_members`, whose rows
keep their own serial and name an optional `Tessera` (`anchor`) and an optional `Trace`
(`origin`).

**What the declarations must satisfy together** (`inventory_classes`, `:933-980`): every class a
spec depends on, the tag table included for a tagged class, declares a spec of its own (`:948-953`);
no class references itself (`:961-962`); the references form no cycle (`:972-977`). Each is a
`ValueError`. The inventory reads `serial` of every class it reads (`:593`), so a class with
`serial: False` declares no spec.

---

## 5. The layer's own tables

The layer names these (`contract.py`); a client registers a factory under each name, and the layer
builds their objects only through those factories.

| Item | Kind | What the layer does with it | When wrong or absent | Neutral client |
|---|---|---|---|---|
| `version` (`VERSION_TABLE`), with the label column `label` (`VERSION_LABEL`) and a `serial` | required | The pool finds the row of its `version_label` by a plain select of `serial` and `label` on every shard (`SQL/ShardedPool.py:376-403`), builds the object through the factory's `build` with an inserter that raises (`:405-435`), and otherwise gets it through the recorded replicated write (`:348-354`). Every `version: True` column references `version.serial` (`SQL/schema.py:128-133`). An actor inserts it without leasing a serial (`SQL/Datastore.py:737`). It is compared at open only if it is listed in `replicated_tables`. | Not registered: the open raises `sqlite3.OperationalError` ("no such table: version") at `SQL/ShardedPool.py:380`. A label held twice on a shard, or the shards disagreeing: `RuntimeError` (`:387-399`). | `version_factory`; replicated |
| `store_tag` (`TAG_TABLE`), with the label column `label` (`TAG_LABEL`) | optional: needed by any tagged class | A tag table is recognised by its foreign key into `store_tag` (`SQL/ShardedPool.py:1336-1342`, `:2106-2112`). The inventory reads a tag's label from `store_tag`'s **key** (`store_inventory.py:609-612`), so its spec must have `label` among its leaves; a tagged class depends on it (`:331-332`). A pool gets a tag only if it is listed as replicated. | A spec without the `label` leaf: `KeyError` in the inventory. | `store_tag_factory`; replicated |
| An association table's tag column `tag_serial` (`TAG_SERIAL`) | required of every tag association | The inventory reads a row's tags by it (`store_inventory.py:615-617`). | A table without it: `KeyError` in the inventory. | `Gadget_tags`, `Sample_tags`, `Trace_tags`, `Weave_tags` |
| A replicated class's tag table | — | A table in neither list whose foreign keys, other than into `store_tag`, all name replicated tables, is compared at open (`SQL/ShardedPool.py:1334-1342`) and is part of its class's unit (`:2127-2146`). | — | `Gadget_tags` |

The primary's own tables (`shards`, `shard_key_config`, `shard_keys`, `replicated_tables`,
`sharded_tables`, `replication_in_flight`; `SQL/ShardedPool.py:765-838`) are the pool's, in the
primary's file; no client registers them.

---

## 6. What the layer reads from a stored object

| Item | What the layer does with it | When wrong or absent | Neutral client |
|---|---|---|---|
| The class's name | A store or validate is dispatched by `type(obj).__name__`, which must be the registered name (`SQL/ShardedPool.py:3342`, `:3435`; `SQL/Datastore.py:633`, `:801`). | `RuntimeError` (`SQL/ShardedPool.py:3352-3354`; `SQL/Datastore.py:404-408`). | every stored class is named as its table |
| `DatastoreObject` (`object.py`): `_my_id`, `store_id`, `available` | `_my_id` is the serial, `None` until stored; `store_id` raises before it is set. The pool reads `_my_id` of every replicated answer (`SQL/ShardedPool.py:3156-3158`, `:3206`, `:3233`, `:3370-3375`, `:3383`, `:3457`) and `store_id` of a get's answer (`:3192-3194`, `:3225`), of a shard key (`:3522-3573`) and of the version row (`:357`). | A stored replicated object with no `_my_id`: `RuntimeError` (`:3370-3373`). A replica answering another serial: `ReplicationMismatch` (`:3232-3235`, `:3382-3385`). | `objects.py`: every stored class subclasses it |
| `_new_insert` or `_updated` on a get's answer | A replicated get is copied to the other shards, under its serial, only if its answer has `_my_id` and one of these attributes (`SQL/ShardedPool.py:3152-3159`, `:3177-3237`). | **Silence.** A factory that inserts without setting either leaves the row on the controlling shard alone, with no record; the next open refuses with `ReplicatedDivergence` (`:1204-1211`). | the leaves' `build`s set `_new_insert`; `keypoint`'s sets `_updated` when a flag turns on |
| `serial` in a get's payload | A replica's scalar get receives the controller's serial as `serial=` (`:3227-3230`); a vectorized one in each payload (`:3192`). The factory inserts under it; the actor leases none for it (`SQL/Datastore.py:730-742`). | The database reporting another serial: `RuntimeError` (`SQL/Datastore.py:769-777`). | every get-or-insert `build` |
| The shard key's field and attribute | A sharded get reads `payload[field]`; a sharded store or validate reads `getattr(obj, field)` (§1 row 6). | §1 row 6. | `Tessera.k` (a `keypoint_alias`), `Sample.k`, `Trace.k`, `Weave.k` (a `keypoint`) |
| An instance of `ShardKeyType` | Every answer of a get of the shard-key class (`SQL/ShardedPool.py:3515-3519`). | `RuntimeError`. | `keypoint` |
| The inserter: `inserter(conn, payload) -> serial` | Bound to the actor's `_insert` (`SQL/Datastore.py:697-780`), which adds `version` and `timestamp`, requires `stepping`, leases a serial, inserts and returns it (`None` for a table with no serial). | §2. | — |
| Picklable, defined at module level | Under Ray every argument and result crosses a process boundary; the stand-in pool pickles both (`tests/standin_pool.py:55-56`, `:131`). | An object that does not pickle fails the call. | every class and factory |

---

## 7. The other entry points that take client facts

| Entry point | Signature | Client facts |
|---|---|---|
| `store_reader.open_read_only` | `open_read_only(primary, factories)` (`store_reader.py:176-241`) | The registry. The replicated set is the store's own record; a record naming a class the registry lacks is refused (`:143-173`). |
| `store_inventory.read_inventory` | `read_inventory(primary, factories) -> StoreInventory` (`store_inventory.py:983-1049`) | The registry and its specs. |
| `store_inventory.inventory_specs`, `inventory_classes` | `(factories)` (`:920-930`, `:933-980`) | The specs; the order. |
| `store_inventory.read_records` | `read_records(conn, table, tables, context, **InventorySpec.keywords())` (`:512-807`) | One spec. |
| `SQL.schema.build_schema` | `build_schema(metadata, factories) -> BuiltSchema` (`SQL/schema.py:62-186`) | The registry. |
| `SQL.schema.dependent_tables` | `dependent_tables(dropped, factories) -> List[str]` (`SQL/schema.py:327-382`) | The registry's foreign keys and specs: the tables that must be dropped with `dropped`, transitively, in registry order. A name the registry does not declare: `ValueError` (`:353-359`). |
| `SQL.schema.drop_order` | `drop_order(tables)` (`SQL/schema.py:287-324`) | Tables, not factories: their foreign keys order the drop. A cycle: `ValueError`. |
| `ShardedPool.factories` | property (`SQL/ShardedPool.py:700-703`) | A copy of the registry the pool was given. |

`ShardedPool.copy_store`, `move_store`, `closed_store_files` and `delete_store`, and the two
tools (`python -m datastorekit.tools.sharded_store`, `python -m datastorekit.tools.shard_key_audit`),
take no client facts: they read only the primary's records. The audit reads the shard-key table's
name from the primary's `shard_key_config`.

---

## 8. Version-keyed lookups (`v0.2.0`, prompt 06)

A class may have its lookups **keyed on the version**: a get then finds only a row made under the
label the pool was opened with, and a row made under another label is a miss. The class declares
it in `register()`; the actor hands its factory's `build` the serial to filter on. Nothing the
layer writes changes: an insert carries the version serial as it always has (§2, `version`).

| Item | Kind (default) | What the layer does with it | When wrong or absent | Neutral client |
|---|---|---|---|---|
| `register()["key_on_version"]` | optional (`False`) | A tenth key of `register()`, read by `build_schema` through `_declared_key_on_version` (`SQL/schema.py:186-190`, `:299-319`). The record of a class **with a table** holds it, `True` or `False`; the record of a class with no table does not (`:104-110`, unchanged), so a reader uses `.get`. | Not a `bool`: `ValueError` "which is not a bool" (`:307-310`). `True` on a class that does not register `"version": True`: `ValueError` naming the class, the key and the value (`:311-318`). Both through `_refuse_declaration` (`:201-207`). | `Tessera` (`tests/client/factories.py:930`); no other class |
| `datastorekit.contract.VERSION_SERIAL_KEY` | the layer's (`"_version_serial"`) | The reserved payload key under which the actor puts the lookup serial in a copy of each payload of a keyed get (`contract.py:39`). The actor sets it, so its name is the layer's, not a client's (`contract.py:15-20`). | A caller's payload that already holds it: `KeyError` naming the class and the key, and nothing is looked up (`SQL/Datastore.py:617-623`). | — |
| `datastorekit.contract.require_version_serial(payload, cls_name) -> int` | for a keyed factory's `build` | Returns `payload[VERSION_SERIAL_KEY]` (`contract.py:42-56`). The factory filters its select on it (`table.c.version == require_version_serial(payload, ...)`). | The key absent or `None`: `RuntimeError` naming `cls_name` and the key, saying that a keyed lookup goes through `object_get` and is never made unfiltered (`:49-55`). So a `build` called other than through the actor raises rather than finding a row of any label. | `Tessera_factory.build` (`tests/client/factories.py:951`) |
| The actor's two serials | the layer's | `_version_serial` stamps inserts; `_lookup_serial` keys lookups (`SQL/Datastore.py:91-96`). `set_version(serial)` sets both, with its checks unchanged (`:150-170`). `set_lookup_version(serial)` sets the lookup serial only: an `int` (`TypeError` otherwise), and a change to a different serial raises `RuntimeError` (`:172-190`). It never sets the insert serial. | A keyed get before either is called: `RuntimeError` naming the class and the label and saying that the pool sets the serial with `set_version` or `set_lookup_version`; nothing is built (`:609-615`). | — |
| The keyed get | the layer's | In `object_get`, after the payloads are formed and before the transaction, a class whose record has `key_on_version` (read with `.get(..., False)`) has its payloads replaced by keyed copies (`SQL/Datastore.py:557-561`, `_keyed_payloads` at `:598-625`). The caller's payloads are not changed. Scalar and vectorized gets alike, and so `ShardedPool.object_get` and `object_get_vectorized`, which reach the actor's `object_get`. | §8's refusals above. | `Tessera`, scalar and vectorized |
| A read-write pool | — | `set_version` on every actor once the version row exists (`SQL/ShardedPool.py:355-360`) gives each both serials. | — | `test_version_keyed_lookups.TestThroughThePool` |
| A read-only pool | — | Its actors are never given the insert serial, the third guard against an insert (`SQL/Datastore.py:192-201`). After every actor's `read_only_state` has returned, the pool calls `set_lookup_version` on each with the version row's serial and waits for every call (`SQL/ShardedPool.py:568-575`; step 6 of the comment at `:467-470`). A keyed get then finds the rows of the pool's label. | A keyed miss reaches the inserter, which a read-only actor refuses: `ReadOnlyWrite` for a sharded class, `ReadOnlyMiss` for a replicated one (`SQL/Datastore.py:292-313`); `_insert`'s guard is behind it (`:779-787`). | `TestThroughThePool.test_a_read_only_*` |

*Correction (extraction prompt 11, 2026-10-10; decision U34).* The read-only row above cited the
pool's `set_lookup_version` calls as `SQL/ShardedPool.py:567-574`. That citation was wrong when it
was written, as extraction prompt 07a's review found: at §8's tree (`v0.2.0`, `240028e`) `:567` is
blank, the comment is `:568-569` and the call `:570-575`. It is corrected in place to `:568-575`;
this is a correction, not a superseded measurement (`CLAUDE.md` rule 6). §8's other
`SQL/ShardedPool.py` citations, `:355-360` and `:467-470`, hold at `v0.2.0`. At `v0.2.1`
(`33778b0`) the calls are `SQL/ShardedPool.py:614-621` (the comment `:614-615`, the call
`:616-621`), and step 6 of the comment is `:513-516`.

**What is not keyed.** Only `object_get`. `object_read_batch`, `read_table`, `object_store` and
`object_validate` hand the factory what the caller gives (`SQL/Datastore.py:606-607`, the docstring
of `_keyed_payloads`). A factory that needs its `read_batch` or `read_table` keyed takes the
serial from its caller.

**A replicated keyed class.** The keying is in the actor, so a replicated class may declare it:
every shard's actor holds the same lookup serial, since the version row is replicated and every
actor is given its one serial, so every shard keys alike. The neutral client keys no replicated
class; this route is allowed and is not exercised by the suite.

**The example.** `Tessera` (`tests/client/factories.py:920-967`) is sharded and registers
`"version": True` and `"key_on_version": True`; its `build` adds `table.c.version ==
require_version_serial(payload, "Tessera")` to its select, and its insert is unchanged, since
`_insert` stamps the version. `test_version_keyed_lookups` holds 14 tests of the above, and the
witness `tests/data/schema_at_extraction-06.json` differs from 04a's only by each record's
`key_on_version`.

---

## 9. Changes after `v0.2.0`

Each subsection is measured from the package at the tree of the prompt that names it, and its line
numbers are that tree's. A row names the row of §1–§8 it supersedes, if any.

### 9.1 Prompt 08a

Two fixes. Nothing a client supplies changes, nothing the layer writes, and no message.

| Change | Supersedes | What the layer now does (`SQL/ShardedPool.py`, at 08a's tree) | Pinned by |
|---|---|---|---|
| A reopen whose primary records a sharded table that `sharded_tables` lacks | §1 row 6, its clause "except that a sharded table the store records and the mapping lacks raises `KeyError` at `:1015` before that message is reached" | `_read_shard_data` compares the primary's `sharded_tables` rows with the mapping (`:1020-1034`). A row whose table the mapping lacks is recorded as not supplied (`:1024-1025`) and contributes no key attribute: the loop goes on to the next row (`:1026-1027`). The open is then refused as §1 row 6 says of any other difference: the table is printed under "The following sharded tables are configured in the existing ShardedPool, but were not supplied to the constructor:" (`:1035-1040`), and `RuntimeError` "Mismatch between sharded tables supplied to the constructor and read from the existing ShardedPool" is raised (`:1055-1058`), before any actor exists. No message changed. A table the primary records twice is refused as before: the mismatch `RuntimeError`, the table printed as not supplied although it was. | `tests/test_unsupplied_sharded_table.py` |
| What `object_get_vectorized` does to the caller's payloads | none: §1–§8 never said. §1 rows 4 and 6 cite its shard-key getter and its two refusals; §8's "The caller's payloads are not changed" is of the actor's `_keyed_payloads`, and still holds | `object_get_vectorized` (`:3290-3314`) sends the shard's actor a copy of each payload with the shard key merged in last, `{**value, **shard_key}` (`:3311`), so a payload carrying its own value for the key's field gets the pool's key. The caller's list and dicts are not changed. The payloads' order and count, the routing by `shard_key` (`:3307-3309`) and the two refusals (`:3296-3299`, `:3302-3305`) are unchanged. Before 08a the key was added to each of the caller's dicts in place. | `tests/test_vectorized_get_payloads.py` |

### 9.2 Prompt 08b

One fix. Nothing a client supplies changes, nothing the layer writes, and no message, refusal or
exception.

| Change | Supersedes | What the layer now does (`SQL/ShardedPool.py`, at 08b's tree) | Pinned by |
|---|---|---|---|
| An open that raises | none: §1–§8 never said what a refused open leaves open | `__init__` sets the pool's attributes, then calls `_open` (`:209-372`, the open's lines unchanged) under a guard (`:203-207`): on any exception, `BaseException` included, it calls `_close_refused_open` (`:374-407`) and re-raises the open's exception unchanged. `_close_refused_open` closes each actor built so far by its own `__exit__`, every call submitted before any is waited for, as the pool's `__exit__` closes them (`:809-815`), and then disposes the pool's engine, as `__exit__` does (`:820-821`). Before the actors exist (the dicts at `:316-332`, and `:592-609` for a read-only pool) there is none to close, and before `_create_engine` runs there is no engine. Nothing it meets is raised and nothing is printed, so an actor whose `__exit__` fails does not replace the open's exception. The caller's `profile_agent` is not cleaned up, since it outlives the refused pool, and the broker holds no engine. An open that succeeds is unchanged, and keeps its engines' connections until the pool's `__exit__`. Before 08b a refused open's engines were left for the garbage collector. | `tests/test_refused_open_closes_engines.py` |

### 9.3 `actor-names` prompt 01

One fix ([`prompts/actor-names/README.md`](../prompts/actor-names/README.md), decision U1).
Nothing a client supplies changes, nothing the layer writes, and no message, refusal or exception
of the layer's. What changes is what a closed pool, or a refused open, leaves in the Ray session:
its actors are killed, so their names are free at once, and the handles the pool keeps are dead.
No client reads a pool's `_shards` or `_broker`, or looks an actor up by name (the campaign
README §0.1). The stand-in pool of the tests (`tests/standin_pool.py`) reserves each actor's name
until its handle is killed, and stands in `ray.kill`, so every test meets both.

| Change | Supersedes | What the layer now does (`SQL/ShardedPool.py`, at `actor-names` prompt 01's tree) | Pinned by |
|---|---|---|---|
| `ShardedPool.__exit__` | none: §1–§9.2 never said what `__exit__` does with the actors, or how long a closed pool holds their names. §9.2's row cites `__exit__` for what it closes, and still holds | `__exit__` (`:841-868`) returns at once if the pool is closed (`:851-852`). Otherwise its body is unchanged: each shard actor's `__exit__`, every one waited for (`:854-859`); the profile agent's `clean_up` (`:861-862`); the pool's engine disposed (`:864-865`). Then `_kill_actors` (`:419-441`, called at `:867`) kills each shard actor and then the broker, if there is one (a read-only pool has none, `:621`), with `ray.kill(handle, no_restart=True)`, ignoring anything a kill raises; and the pool is marked closed (`:868`; the flag is set false at `:205`, before the open). Ray frees a killed actor's name at once, so the store can be reopened, read-write or read-only, in the same Ray session while the closed pool is still referenced. The handles stay in `_shards` and `_broker`, and are dead: a call through one fails. A second `__exit__` does nothing. If a shard's `__exit__` raises, `__exit__` raises as before, kills nothing and does not mark the pool closed. The names are unchanged: `SerialPoolBroker` (`:311`) and `shard{key:04d}-store` (`:322`, and `:625` for a read-only pool). Before this prompt a closed pool's names were freed only when the pool object was collected. | `tests/test_closed_pool_releases_its_names.py` (tests 1, 2, 5, 6); `docs/extraction/ray_smoke_run.py` step N |
| A refused open | none. §9.2's row, which says what `_close_refused_open` closes and disposes, still holds; this adds the kill | `_close_refused_open` (`:379-417`) ends, after closing each actor and disposing the engine as §9.2 says, by calling `_kill_actors` (`:417`). It kills only the handles the half-built pool holds: the shard actors once `_shards` is their dict (until then it is the shard count), and the broker once `_broker` is set (`:311`). No actor is looked up by name. So a refused or abandoned open, read-write or read-only, releases the names it took at once, even while its exception, and with it the half-built pool, is held: for example an open refused by the `read_table_config` check after every actor exists (`:350-356`; `:656-663` for a read-only pool). Nothing it meets is raised, so the caller sees the open's own exception, as in §9.2. | `tests/test_closed_pool_releases_its_names.py` (test 3) |
| Two open pools | none: §1–§9.2 never said | The names are fixed, so in one Ray session a second open while a pool is open is still refused by Ray when the second pool creates its broker (`:311`), with Ray's name collision, "The name SerialPoolBroker (namespace=None) is already taken. …": `ValueError` at Ray 2.43.0, and its subclass `ray.exceptions.ActorAlreadyExistsError` at 2.55.1. The refused open has made no actor and set no `_broker`, so its `_close_refused_open` kills nothing, and the open pool goes on serving. One serial broker per store, per Ray session, is kept. | `tests/test_closed_pool_releases_its_names.py` (test 4); `docs/extraction/ray_smoke_run.py` step C |
