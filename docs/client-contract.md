# The client contract

*Measured from the package at `8bc60a5`, whose layer is the source repository's at `6f7f291`
(`PROVENANCE.md`). Every line number below is that tree's; the files it names have not changed
since.*

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
| 5 | `replicated_tables` | required | The replicated classes, a list. Written to the primary (`:907-916`) and compared on every reopen (`:971-999`); given to every actor (`:308`). It dispatches a get, store or validate to the replicated write (`:3022`, `:3344`, `:3437`); it is what the check at open compares, with each listed class's tag tables (`:1334-1342`); its classes with `validate_on_startup` are pruned by the pool (`:2094-2103`); `read_table_config` may name only these (`:336-339`). The reader takes the store's own record, not this list (`store_reader.py:143-173`). | A list that differs from the store's record: `RuntimeError` at open (`:996-999`). A class in neither list cannot be got, stored or validated through the pool: `RuntimeError` (`:3028-3030`, `:3352-3354`, `:3445-3447`). A replicated class left out is not compared at open. | `registry.replicated_tables` (9 classes) |
| 6 | `sharded_tables` | required | The sharded classes, mapped to the payload field, and object attribute, that holds the shard key. Written to the primary (`:918-926`) and compared on every reopen (`:1001-1049`). A get is sent to the key's shard (`:3251-3275`), and so are a store and a validate (`:3403-3418`, `:3491-3503`); `object_get_vectorized` and `object_read_batch` accept only these classes (`:3283-3286`, `:3310-3313`); `read_table` refuses them (`:3598-3601`). | A missing field in a payload: `KeyError` (`:3261`, `:3272`); in a shard-key mapping: `RuntimeError` (`:3289-3292`, `:3316-3319`); a missing attribute on an object: `RuntimeError` (`:3409-3412`, `:3494-3497`). A mapping that differs from the store's record: `RuntimeError` (`:1042-1049`), except that a sharded table the store records and the mapping lacks raises `KeyError` at `:1015` before that message is reached. | `registry.sharded_tables` = `{"Tessera": "k", "Sample": "k"}` |
| 7 | `timeout` | defaulted (`None`) | SQLite's busy timeout, for the pool's engine (`:766-768`), every actor's (`:311`; `SQL/Datastore.py:200-202`, `:339-341`), the read-only engine (`:507-509`) and the check at open's (`:1370-1372`). | Not given: SQLite's default. | not given |
| 8 | `shards` | defaulted (`10`) | The number of shards of a **new** store, at least 1 (`:169`, `:226-237`). | For an existing store the primary's records decide; a different number prints a warning (`:287-290`). | `3` (`build_store`'s default), `2`, `1` |
| 9 | `profile_agent` | defaulted (`None`) | A `ProfileAgent` actor handle, given to every actor (`:314`), and cleaned up when the pool exits (`:759-760`). | Not given: no profiling. | not given |
| 10 | `job_name` | defaulted (`None`) | Kept (`:138`). Nothing in the package reads it. | — | not given |
| 11 | `prune_unvalidated` | defaulted (`False`) | Under it, the pool prunes every replicated class whose factory validates at startup, under a "prune" record, after the check at open and before any actor exists (`:275-276`, `:2314-2347`); each actor prunes its sharded classes (`SQL/Datastore.py:459-464`). | A read-only pool given it: `ReadOnlyWrite` before anything is opened (`:486-491`). | not given by `build_store`; a pool may be opened with it |
| 12 | `drop_tables` | defaulted (`None`) | Tables every actor drops when it opens an existing store, in `schema.drop_order`'s order (`:316`; `SQL/Datastore.py:410-441`), then re-creates empty. | A name the registry does not declare as a table: `RuntimeError` before anything is opened (`:705-717`). A drop that leaves another table naming rows of a dropped one (`schema.dependent_tables`): `RuntimeError` before anything is opened (`:719-737`). A read-only pool given any: `ReadOnlyWrite` (`:480-485`). | `registry.tables_to_drop(...)` |
| 13 | `read_table_config` | defaulted (`None`) | Class name → `{"tables_arg": bool}`: the classes `read_table` serves (`:3582-3618`; `SQL/Datastore.py:828-870`). With `tables_arg` true, the actor passes the factory its tables as `tables=` (`SQL/Datastore.py:863-865`). | A class that is not replicated: `RuntimeError` at open (`:334-339`, `:568-573`). A `read_table` with no config, of a sharded class, or of a class not in it: `RuntimeError` (`:3590-3606`). | `registry.read_table_config`: `keypoint` (`tables_arg` False), `dial_setting` (True) |
| 14 | `read_only` | defaulted (`False`) | Opens an existing store with every file `mode=ro`, writing nothing (`:203-209`, `:477-579`). | Refusals of its own: a missing store, a journal, a write (`ReadOnlyWrite`), a miss (`ReadOnlyMiss`). | `StandinCluster.open_pool(..., read_only=True)` |
| 15 | `factories` | **required**, keyword-only | The registry: class name → factory (`:145`). Every table, schema record and hook comes from it: the pool's (`:414`, `:617`, `:711`, `:1166`, `:2320`), every actor's (`:309`; `SQL/Datastore.py:351-397`), the reader's and the inventory's when they are given it (§7). Kept as a copy (`:700-703`). | Not a mapping: the actor raises `RuntimeError` (`SQL/Datastore.py:361-362`). A class it lacks: `RuntimeError` naming it (`SQL/Datastore.py:404-408`). | `registry.factories` (14 classes) |
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
| `serial` | defaulted (`True`) | both | An `INTEGER PRIMARY KEY` column `serial` (`:117-122`), leased from the broker for each insert unless the payload gives one (`SQL/Datastore.py:725-742`). | `False`: no `serial`; the table is keyed by the primary key its columns declare, which the check at open compares under (`SQL/ShardedPool.py:1348`). Such a class has no `store_id`, and cannot declare an `inventory_spec` (the inventory reads `serial`, `store_inventory.py:593`). | `serial: False` on `Gadget_tags`, `Sample_tags`, `Sample_members` |
| `version` | defaulted (`False`) | both | A `version` column with a foreign key to the version table's `serial`, indexed (`:125-135`). Every insert carries the pool's version serial (`SQL/Datastore.py:744-745`). | An insert before the pool has set the serial is refused (`SQL/Datastore.py:715-723`). With no version table registered, creating the table fails (no referenced table). | `True` on `keypoint_alias`, `Gadget`, `Tessera`, `Sample` |
| `timestamp` | defaulted (`False`) | both | A `timestamp` `DateTime` column (`:137-142`), stamped at insert (`SQL/Datastore.py:746-752`); a replicated write stamps every shard with the one timestamp it chose (`SQL/ShardedPool.py:3088-3089`), and the repair at open copies a row only if its timestamp is the record's start (`:1823-1830`). The inventory reports the earliest and latest (`store_inventory.py:597-599`). | — | `True` on `store_tag`, `keypoint`, `keypoint_alias`, `dial_setting`, `Gadget`, `Gadget_tags`, `Tessera`, `Sample`, `Sample_tags`; `False` on the rest |
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
| `build(payload, conn, table, inserter, tables, inserters)` | abstract (`:12-15`) | both | Every get, in the actor, inside one transaction for all of a call's payloads (`SQL/Datastore.py:528-541`). It finds the object or inserts it through `inserter`; a replica's get carries the controller's `serial` in the payload, under which it must insert (§6). The pool also calls the version table's `build` on a `mode=ro` connection with an inserter that raises, to find the version row (`SQL/ShardedPool.py:408-435`). | A `SQLAlchemyError` is printed and re-raised (`SQL/Datastore.py:542-550`). | every factory but the three association tables, whose `build` raises |
| `store(obj, conn, table, inserter, tables, inserters)` | abstract (`:17-20`) | both | Every store, in the actor (`SQL/Datastore.py:647-658`). For a replicated class the controlling shard stores the object, and every other shard is given the controller's answer, carrying its serial and those of its owned rows: it inserts under them, or verifies it holds them (`SQL/ShardedPool.py:3361-3401`). | A `ReplicationMismatch` it raises is re-raised naming the actor (`SQL/Datastore.py:656-657`). Not defined: the base's `NotImplementedError`. | `keypoint_alias`, `Gadget` (replicated); `Sample` (sharded) |
| `validate(obj, conn, table, tables)` | abstract (`:22-25`) | both | Every validate, in the actor (`SQL/Datastore.py:782-826`); returns the outcome. For a replicated class, a `True` outcome on the controlling shard is repeated on every other, and each outcome must equal it (`SQL/ShardedPool.py:3454-3489`). | A replica whose outcome differs: `ReplicationMismatch` (`:3470-3482`). `False` or `None` on the controlling shard: nothing is replicated (`:3464-3465`). | `Gadget` (replicated), `Sample` (sharded) |
| `validate_on_startup(conn, table, tables, prune=False)` | abstract (`:27-30`) | both, when `register()` says so | Returns lines describing the unvalidated rows; with `prune=True` deletes them. Called by each actor at open (`SQL/Datastore.py:464`; read-only, `:239-241`) and by the pool's prune of a replicated class (`SQL/ShardedPool.py:2160-2183`, `:2185-2257`), which requires that a second call with `prune=False` reports nothing and that only the class's unit lost rows. | A prune that did not take: `RuntimeError`, the shard rolled back and the record left set (`:2213-2256`). | `Gadget`, `Sample` |
| `revalidate(serial, conn, table, tables)` | defaulted: raises `NotImplementedError` (`:34-48`) | **replicated only** | After an interrupted validate, recompute and write the stored row's validated flag by `validate`'s rule, and return it (`SQL/ShardedPool.py:1966-2017`, the call at `:1992`). A `True` on a shard that held `False` is kept; any other result is rolled back to a savepoint. | A shard holding `True` whose rule gives `False`: refused, `ReplicatedDivergence` (`:2007-2016`). Not defined while `validated_column` is declared: `NotImplementedError` at that open. | `Gadget` |
| `owned_serials(obj)` | defaulted: `None` (`:50-57`) | **replicated only** | The serials of the rows `obj` owns in another table, in order. After a replicated store the controller's and every replica's are compared (`SQL/ShardedPool.py:3377`, `:3386-3394`). | A difference: `ReplicationMismatch`. Not defined: `None` on both sides, so nothing is compared. | `Gadget` (its `GadgetPart` serials) |
| `inventory_spec()` | defaulted: `None` (`:59-62`) | both | An `InventorySpec` (§4), or `None` for a class outside the inventory. Read by `getattr`, so a factory that is not a subclass may lack it (`store_inventory.py:920-930`). It orders and reads the inventory (`:933-1049`), and its declared parents count as references for `dependent_tables` (`SQL/schema.py:366-367`). | §4. | 9 classes |
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
| `parents` | `{}` | Key field → `Parent`, each resolved to the parent's reference digest (`:699-728`). | A parent that cannot be resolved: the row is not a record, and the class has an `unresolved-parent` problem (`:783-793`). | `keypoint_alias`, `Gadget`, `Tessera`, `Sample` |
| `tags` | `None` | `(association table, its column naming this class's serial)`: the row's tag labels, read through the tag table's records (`:604-642`). The tag table is then a dependency (`:331-332`). | Orphan rows: `orphan-tag` problems. | `Gadget`, `Sample` |
| `values` | `None` | `(value table, its column naming this class's serial)`: the count of value rows per row, one `GROUP BY` (`:644-667`). | Orphan rows: an `orphan-value` problem. | `Gadget` (`GadgetPart`) |
| `validated` | `None` | The class's validated column, read into the record (`:594-596`, `:772-776`). | A column the table lacks: `KeyError`. | `Gadget`, `Sample` |
| `parent_sets` | `{}` | Key field → `ParentSet` (`:669-697`, `:730-762`). | A row with no members: `empty-parent-set`; orphan members: `orphan-member`. | `Sample` (`members`) |

**`Parent`** (`:208-267`), **6** fields: `column` (required), and `of`, `type_column`, `types`,
`nullable`, `cross_shard`. Exactly one of `of` (a class) and `types` (a polymorphic reference's
map from a value of `type_column` to a class) is given, `type_column` with `types` or not at all,
and `types` non-empty, or `ValueError` at construction (`:241-253`). A polymorphic parent's
`type_column` must be one of its class's `leaves`, or `inventory_classes` raises `ValueError`
(`:954-959`). `nullable`: a NULL is a value of the key rather than a missing parent (`:701-702`).
`cross_shard`: the parent row may be on another shard, and is resolved against every shard's rows
of its class (`:704-707`; `_merge_digests`, `:815-827`). *Neutral client:* `of` throughout;
`Gadget.frame` is polymorphic over `dial_setting` and `knob_setting`; `Sample.anchor` is
`nullable` and `cross_shard`, naming a `Tessera` with no foreign key.

**`ParentSet`** (`:270-293`), **3** fields: `table` (the member table), `owner` (its column naming
the owning row) and `members` (member field → `Parent`). A polymorphic member raises `ValueError`
at construction (`:287-293`); a member may be `cross_shard`. *Neutral client:* `Sample.members`,
over `Sample_members`, whose rows name a `Tessera` on the Sample's own shard by foreign key; the
member table declares no spec of its own.

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
| An association table's tag column `tag_serial` (`TAG_SERIAL`) | required of every tag association | The inventory reads a row's tags by it (`store_inventory.py:615-617`). | A table without it: `KeyError` in the inventory. | `Gadget_tags`, `Sample_tags` |
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
| The shard key's field and attribute | A sharded get reads `payload[field]`; a sharded store or validate reads `getattr(obj, field)` (§1 row 6). | §1 row 6. | `Tessera.k` (a `keypoint_alias`), `Sample.k` (a `keypoint`) |
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
