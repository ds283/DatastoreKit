"""
The neutral test client (``datastorekit.tests.client``), on the stand-in pool.

The client supplies every fact ``docs/client-contract.md`` says a client supplies. These tests
show that it does, and that the layer reads each fact where the client declares it:

1. ``TestCoverageByDeclaration`` -- the registry, through the schema builder and the inventory's
   declarations: every ``register()`` key in use, in each of its forms; the replicated-only
   declarations on replicated classes, where the pool's own derivations find them; every factory
   hook defined by some factory of the kind the layer calls it for; every field of
   ``InventorySpec``, ``Parent`` and ``ParentSet`` in use; the shard key, its proxy and the layer's
   two tables. A role that disappears from the client fails one of these;
2. ``TestRoundTrip`` -- ``build_store`` writes every class through the stand-in pool; the store
   reopens read-write with the check at open passing, nothing repaired and nothing written, and
   every class reads back through the pool; ``open_read_only`` and ``read_inventory`` read every
   class; a replicated get is written on the pinned controlling shard and copied to every other;
3. ``TestTheRegistry`` -- the nine names; ``tables_to_drop`` over ``drop_groups``; and
   ``dependent_tables``, which accepts every group and finds, for each, the tables it must be
   dropped with.

No Ray, and every store is in a temporary directory.
"""

import contextlib
import dataclasses
import sqlite3
import tempfile
import unittest
from pathlib import Path

import ray
import sqlalchemy as sqla

from datastorekit.SQL.ShardedPool import ShardedPool
from datastorekit.SQL.factory_base import SQLAFactoryBase
from datastorekit.SQL.schema import build_schema, dependent_tables
from datastorekit.contract import TAG_LABEL, TAG_SERIAL, TAG_TABLE, VERSION_LABEL
from datastorekit.contract import VERSION_TABLE
from datastorekit.store_inventory import (
    InventorySpec,
    Parent,
    ParentSet,
    inventory_classes,
    inventory_specs,
    read_inventory,
)
from datastorekit.store_reader import open_read_only
from datastorekit.tests import standin_pool as sp
from datastorekit.tests.client import build, registry
from datastorekit.tests.client.objects import keypoint, keypoint_alias

REGISTER_KEYS = (
    "validate_on_startup",
    "serial",
    "version",
    "timestamp",
    "stepping",
    "columns",
    "owner_column",
    "monotone_flags",
    "validated_column",
)
ABSTRACT_HOOKS = ("register", "build", "store", "validate", "validate_on_startup")
DEFAULTED_HOOKS = ("revalidate", "owned_serials", "inventory_spec")
UNDECLARED_HOOKS = ("read_batch", "read_table")

NINE = {
    "factories",
    "replicated_tables",
    "sharded_tables",
    "shard_key_type",
    "shard_key_store_id",
    "read_table_config",
    "serial_batch_sizes",
    "drop_groups",
    "tables_to_drop",
}

# the tables each drop group alone must be dropped with, in registry order
MEASURED_DEPENDENTS = {
    "aliases": [
        "Tessera",
        "Sample",
        "Sample_tags",
        "Sample_members",
        "Weave",
        "Weave_tags",
        "Weave_members",
    ],
    "tesserae": [
        "Sample",
        "Sample_tags",
        "Sample_members",
        "Weave",
        "Weave_tags",
        "Weave_members",
    ],
    "samples": [],
    "gadgets": ["Sample", "Sample_tags", "Sample_members"],
    "traces": [],
}
# the tables no drop group names
KEPT = [
    "version",
    "store_tag",
    "keypoint",
    "dial_setting",
    "knob_setting",
    "gauge_setting",
    "routing_rule",
]


def tearDownModule():
    if ray.is_initialized():
        raise AssertionError("Ray was initialised by test_neutral_client")


def _built():
    return build_schema(sqla.MetaData(), registry.factories)


def _defines(factory, hook: str) -> bool:
    """Whether ``factory`` defines ``hook`` itself, rather than inheriting the base's default."""
    own = getattr(factory, hook, None)
    if own is None:
        return False
    base = getattr(SQLAFactoryBase, hook, None)
    return base is None or own is not base


def _pool_derivations():
    """The pool's own reading of the registry, with no store: a ShardedPool made without its
    constructor, holding only the two table lists its derivations read."""
    pool = object.__new__(ShardedPool)
    pool._replicated_tables = list(registry.replicated_tables)
    pool._sharded_tables = dict(registry.sharded_tables)
    return pool


def _rows(path: Path, table: str):
    with contextlib.closing(sqlite3.connect(f"file:{path}?mode=ro", uri=True)) as conn:
        return conn.execute(f'SELECT * FROM "{table}" ORDER BY 1').fetchall()


# ------------------------------------------------------------------------------------------------
# 1. coverage, by declaration
# ------------------------------------------------------------------------------------------------


class TestCoverageByDeclaration(unittest.TestCase):
    def test_every_register_key_is_declared_by_some_factory(self):
        declared = set()
        for factory in registry.factories.values():
            registration = factory.register()
            if registration is not None:
                declared |= set(registration)
        self.assertEqual(set(REGISTER_KEYS) - declared, set())
        # and nothing the schema builder does not read
        self.assertEqual(declared - set(REGISTER_KEYS), set())

    def test_each_form_of_a_registration_is_in_use(self):
        records = _built().records
        with_table = [r for r in records.values() if r["table"] is not None]
        self.assertEqual(
            [n for n, r in records.items() if r["table"] is None], ["ephemeral_probe"]
        )
        for key in ("use_serial", "use_version", "use_timestamp", "use_stepping"):
            with self.subTest(key=key):
                self.assertEqual({r[key] for r in with_table}, {True, False})
        # stepping: True (no mode), "minimum" and "exact"
        self.assertEqual(
            {r["stepping_mode"] for r in with_table if r["use_stepping"]},
            {None, "minimum", "exact"},
        )
        self.assertEqual(
            {
                n: r["stepping_mode"]
                for n, r in records.items()
                if r.get("use_stepping")
            },
            {
                "keypoint_alias": "exact",
                "dial_setting": "minimum",
                "knob_setting": None,
            },
        )
        self.assertTrue(all(len(r["columns"]) > 0 for r in with_table))
        # a class with no serial is keyed by its declared primary key
        no_serial = [n for n, r in records.items() if r.get("use_serial") is False]
        self.assertEqual(
            no_serial,
            [
                "Gadget_tags",
                "Sample_tags",
                "Sample_members",
                "Trace_tags",
                "Weave_tags",
            ],
        )

    def test_the_replicated_only_declarations_are_where_the_pool_reads_them(self):
        built = _built()
        pool = _pool_derivations()
        specs = {s["name"]: s for s in pool._replicated_table_specs(built)}
        replicated = set(registry.replicated_tables)

        # monotone_flags: on a replicated leaf, as the pool's check at open reads it
        flagged = {
            n: s["monotone_flags"] for n, s in specs.items() if s["monotone_flags"]
        }
        self.assertEqual(flagged, {"keypoint": ("kp_marked", "kp_flagged")})

        # validated_column, revalidate and owned_serials: on one replicated owner
        validated = {
            n: s["validated_column"] for n, s in specs.items() if s["validated_column"]
        }
        self.assertEqual(validated, {"Gadget": "gadget_validated"})
        owner = registry.factories["Gadget"]
        self.assertTrue(_defines(owner, "revalidate"))
        self.assertTrue(_defines(owner, "owned_serials"))

        # owner_column: on a replicated table, naming the owner; with the owner's tag table it
        # is the owner's unit, which the pool copies and prunes as a whole
        owned = {n: s["owner_column"] for n, s in specs.items() if s["owner_column"]}
        self.assertEqual(owned, {"GadgetPart": "gadget_serial"})
        self.assertIn("GadgetPart", replicated)
        self.assertEqual(
            ShardedPool._unit_tables("Gadget", list(specs.values())),
            ["Gadget", "Gadget_tags", "GadgetPart"],
        )

        # nothing of these is declared on a class the pool does not compare
        for name, record in built.records.items():
            if name in specs or record["table"] is None:
                continue
            with self.subTest(name=name):
                self.assertIsNone(record["owner_column"])
                self.assertEqual(record["monotone_flags"], ())
                self.assertIsNone(record["validated_column"])
                self.assertFalse(_defines(registry.factories[name], "revalidate"))
                self.assertFalse(_defines(registry.factories[name], "owned_serials"))

    def test_validate_on_startup_is_declared_by_a_replicated_and_a_sharded_class(self):
        built = _built()
        at_startup = [n for n, r in built.records.items() if r["validate_on_startup"]]
        self.assertEqual(at_startup, ["Gadget", "Sample"])
        # the pool prunes the replicated one; each actor prunes the sharded one
        self.assertEqual(
            ShardedPool._replicated_prune_classes(registry.replicated_tables, built),
            ["Gadget"],
        )
        self.assertIn("Sample", registry.sharded_tables)
        for name in at_startup:
            self.assertTrue(_defines(registry.factories[name], "validate_on_startup"))

    def test_every_hook_is_defined_by_a_factory_of_the_kind_it_is_called_for(self):
        for hook in ABSTRACT_HOOKS + DEFAULTED_HOOKS + UNDECLARED_HOOKS:
            with self.subTest(hook=hook):
                self.assertTrue(
                    any(_defines(f, hook) for f in registry.factories.values()), hook
                )
        # store and validate: on a replicated class and on a sharded class
        for hook in ("store", "validate"):
            definers = {n for n, f in registry.factories.items() if _defines(f, hook)}
            self.assertTrue(definers & set(registry.replicated_tables), hook)
            self.assertTrue(definers & set(registry.sharded_tables), hook)
        # read_batch: a sharded class only (ShardedPool.object_read_batch)
        self.assertEqual(
            {n for n, f in registry.factories.items() if _defines(f, "read_batch")},
            {"Sample"},
        )
        # read_table: exactly the classes read_table_config names, each replicated
        self.assertEqual(
            {n for n, f in registry.factories.items() if _defines(f, "read_table")},
            set(registry.read_table_config),
        )

    def test_read_table_config_takes_tables_arg_both_ways(self):
        self.assertEqual(
            {c["tables_arg"] for c in registry.read_table_config.values()},
            {True, False},
        )
        self.assertTrue(
            set(registry.read_table_config) <= set(registry.replicated_tables)
        )

    def test_every_declaration_field_is_in_use(self):
        specs = inventory_specs(registry.factories)
        # the fields, counted, so that a field added to a declaration fails here until it is used
        self.assertEqual(
            [f.name for f in dataclasses.fields(InventorySpec)],
            ["leaves", "parents", "tags", "values", "validated", "parent_sets"],
        )
        self.assertEqual(
            [f.name for f in dataclasses.fields(Parent)],
            ["column", "of", "type_column", "types", "nullable", "cross_shard"],
        )
        self.assertEqual(
            [f.name for f in dataclasses.fields(ParentSet)],
            ["table", "owner", "members"],
        )

        defaults = InventorySpec()
        for field in dataclasses.fields(InventorySpec):
            with self.subTest(field=field.name):
                self.assertTrue(
                    any(
                        getattr(s, field.name) != getattr(defaults, field.name)
                        for s in specs.values()
                    )
                )

        parents = [p for s in specs.values() for p in s.parents.values()]
        members = [
            p
            for s in specs.values()
            for ps in s.parent_sets.values()
            for p in ps.members.values()
        ]
        self.assertTrue(any(p.of is not None for p in parents))
        polymorphic = [p for p in parents if p.types is not None]
        self.assertEqual(len(polymorphic), 2)
        self.assertEqual(polymorphic[0].type_column, "frame_kind")
        self.assertEqual(
            set(polymorphic[0].types.values()), {"dial_setting", "knob_setting"}
        )
        self.assertIn("frame_kind", specs["Gadget"].leaves)
        crossing = [p for p in parents + members if p.cross_shard]
        self.assertEqual([p.of for p in crossing], ["Tessera"])
        self.assertIn("Tessera", registry.sharded_tables)
        self.assertTrue(any(p.nullable for p in parents))

        parent_set = specs["Sample"].parent_sets["members"]
        self.assertEqual(
            (parent_set.table, parent_set.owner), ("Sample_members", "sample_serial")
        )
        # the member table names its members by foreign key, and declares no inventory_spec
        self.assertNotIn("Sample_members", specs)
        member_targets = {
            fk.column.table.name
            for fk in _built().tables["Sample_members"].foreign_keys
        }
        self.assertEqual(member_targets, {"Sample", "Tessera"})

    def test_the_inventory_derives_an_order_from_the_declarations(self):
        order = inventory_classes(registry.factories)
        self.assertEqual(set(order), set(inventory_specs(registry.factories)))
        for name, spec in inventory_specs(registry.factories).items():
            for dependency in spec.dependencies():
                self.assertLess(order.index(dependency), order.index(name))

    def test_the_shard_key_and_its_proxy(self):
        self.assertIs(registry.shard_key_type, keypoint)
        self.assertEqual(registry.shard_key_type.__name__, "keypoint")
        self.assertIn("keypoint", registry.replicated_tables)
        self.assertIn("keypoint", _built().tables)
        self.assertIn("keypoint_alias", registry.replicated_tables)
        self.assertEqual(
            registry.sharded_tables,
            {"Tessera": "k", "Sample": "k", "Trace": "k", "Weave": "k"},
        )

        point = keypoint(7, 0.5)
        self.assertEqual(registry.shard_key_store_id(point), 7)
        self.assertEqual(registry.shard_key_store_id(keypoint_alias(11, point, 0.1)), 7)
        with self.assertRaises(RuntimeError):
            registry.shard_key_store_id(object())

    def test_the_layer_owned_tables(self):
        built = _built()
        for name, label in ((VERSION_TABLE, VERSION_LABEL), (TAG_TABLE, TAG_LABEL)):
            with self.subTest(table=name):
                self.assertIn(name, registry.replicated_tables)
                self.assertIn(label, built.tables[name].c)
                self.assertTrue(built.records[name]["use_serial"])
        # every tag association names a tag by the layer's column, through a foreign key
        for name in ("Gadget_tags", "Sample_tags"):
            with self.subTest(table=name):
                column = built.tables[name].c[TAG_SERIAL]
                self.assertEqual(
                    {fk.column.table.name for fk in column.foreign_keys}, {TAG_TABLE}
                )
        # the replicated class's tag table is the one the pool finds and compares
        specs = _pool_derivations()._replicated_table_specs(built)
        self.assertEqual(
            [s["name"] for s in specs],
            [n for n in registry.replicated_tables if n in built.tables]
            + ["Gadget_tags"],
        )
        self.assertEqual(
            inventory_specs(registry.factories)["Sample"].tags,
            ("Sample_tags", "sample_serial"),
        )


# ------------------------------------------------------------------------------------------------
# 2. the round trip
# ------------------------------------------------------------------------------------------------


class TestRoundTrip(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.primary = build.build_store(self.root / "store", shards=3)
        self.shard_files = {
            int(p.stem[-4:]): p for p in sorted(self.primary.parent.glob("*-shard*"))
        }
        self.cluster = sp.StandinCluster()
        stack = contextlib.ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(self.cluster.active())

    def tearDown(self):
        self.assertFalse(ray.is_initialized())

    def test_build_store_writes_every_class(self):
        tables = _built().tables
        self.assertEqual(len(self.shard_files), 3)
        self.assertEqual(
            sorted(p.name for p in self.primary.parent.iterdir()),
            [
                "store-shard0000.sqlite",
                "store-shard0001.sqlite",
                "store-shard0002.sqlite",
                "store.sqlite",
            ],
        )
        for name in tables:
            with self.subTest(table=name):
                held = sum(len(_rows(p, name)) for p in self.shard_files.values())
                self.assertGreater(held, 0)
        # the replicated tables and the replicated class's tag table: the same on every shard
        for name in [n for n in registry.replicated_tables if n in tables] + [
            "Gadget_tags"
        ]:
            with self.subTest(replicated=name):
                copies = [_rows(p, name) for p in self.shard_files.values()]
                self.assertTrue(all(c == copies[0] for c in copies), name)
        # the flag a second get turned on is on, on every shard
        for path in self.shard_files.values():
            self.assertEqual(
                _rows(path, "keypoint")[1][-2:], (1, 0)  # kp_marked, kp_flagged
            )

    def test_a_reopen_passes_the_check_at_open_repairs_nothing_and_writes_nothing(self):
        before = sp.store_checksums(self.primary)
        pool = build.open_pool(self.cluster, self.primary, shards=3)
        try:
            self.assertIsNone(pool.reconciliation["record"])
            self.assertEqual(pool.reconciliation["repaired"], [])
            self.assertFalse(pool.reconciliation["cleared"])
            self.assertEqual(pool.reconciliation["hot_journals"], [])
            self.assertEqual(
                pool.reconciliation["compared"],
                [n for n in registry.replicated_tables if n in _built().tables]
                + ["Gadget_tags"],
            )
            self.assertEqual(pool.pruned, [])
        finally:
            self.cluster.close_pool(pool)
        self.assertEqual(sp.store_checksums(self.primary), before)

    def test_every_class_reads_back_through_a_reopened_pool(self):
        pool = build.open_pool(self.cluster, self.primary, shards=3)
        try:
            calls = len(self.cluster.calls)
            points = build.get_keypoints(pool, build.KEYPOINT_POSITIONS)
            self.assertTrue(all(p.available for p in points))
            self.assertFalse(any(hasattr(p, "_new_insert") for p in points))
            self.assertEqual(
                [p.position for p in build.resolve(pool.read_table("keypoint"))],
                list(build.KEYPOINT_POSITIONS),
            )
            self.assertEqual(
                [
                    (d.level, d.stepping)
                    for d in build.resolve(pool.read_table("dial_setting"))
                ],
                sorted(build.DIAL_LEVELS),
            )
            # "minimum": a get asking for stepping 0 is served by the row of stepping 1
            self.assertEqual(build.get_dial(pool, 3, 0).stepping, 1)
            knob = build.get_knob(pool, *build.KNOB_TURNS)
            self.assertFalse(hasattr(knob, "_new_insert"))
            self.assertEqual(build.get_probe(pool, "again").note, "again")
            north, south = build.get_tags(pool, "tag-north", "tag-south")

            aliases = [
                build.resolve(
                    pool.object_get(
                        "keypoint_alias",
                        keypoint=p,
                        offset=build.ALIAS_OFFSET,
                        stepping=build.ALIAS_STEPPING,
                    )
                )
                for p in points
            ]
            self.assertTrue(all(a.available for a in aliases))

            dial = build.get_dial(pool, 3, 1)
            gadget = build.get_gadget(pool, "gadget-one", dial, [north])
            self.assertTrue(gadget.available and gadget.validated)
            self.assertEqual([p.part_value for p in gadget.parts], [1.5, 2.5, 3.5])
            # the unvalidated Gadget is not served
            self.assertFalse(
                build.get_gadget(pool, "gadget-two", knob, [north, south]).available
            )

            for i, (point, alias) in enumerate(zip(points, aliases)):
                tesserae = build.get_tesserae(pool, alias, build.TESSERA_WEIGHTS)
                self.assertFalse(any(hasattr(t, "_new_insert") for t in tesserae))
                sample = build.get_sample(pool, point, gadget, f"sample-{i}", [south])
                self.assertTrue(sample.available and sample.validated)
                self.assertEqual(
                    [m.store_id for m in sample.members],
                    sorted(t.store_id for t in tesserae),
                )
                self.assertEqual(sample.anchor is None, i == 0)
                read = build.read_samples(pool, point)
                self.assertEqual([s.code for s in read], [f"sample-{i}"])
                every = build.read_samples(pool, point, validated_only=False)
                self.assertEqual(
                    sorted(s.code for s in every),
                    sorted(
                        [f"sample-{i}"] + ([build.UNVALIDATED_SAMPLE] if i == 1 else [])
                    ),
                )
            self.assertGreater(len(self.cluster.calls), calls)
        finally:
            self.cluster.close_pool(pool)

    def test_the_reader_and_the_inventory_read_every_class(self):
        built = _built()
        with open_read_only(self.primary, registry.factories) as store:
            self.assertEqual(store.replicated_tables, tuple(registry.replicated_tables))
            self.assertEqual(set(store.tables), set(built.tables))
            for name in built.tables:
                with self.subTest(table=name):
                    held = 0
                    for shard in store.shards:
                        with shard.engine.connect() as conn:
                            held += conn.execute(
                                sqla.select(sqla.func.count()).select_from(
                                    shard.tables[name]
                                )
                            ).scalar()
                    self.assertGreater(held, 0)

        inventory = read_inventory(self.primary, registry.factories)
        self.assertEqual(inventory.problems, ())
        self.assertEqual(inventory.shards, (0, 1, 2))
        counts = {name: c.count for name, c in inventory.classes.items()}
        self.assertEqual(
            counts,
            {
                "version": 1,
                "store_tag": 3,
                "keypoint": 3,
                "dial_setting": 2,
                "knob_setting": 1,
                "gauge_setting": 2,
                "routing_rule": 2,
                "keypoint_alias": 3,
                "Gadget": 2,
                "Tessera": 6,
                "Sample": 4,
                "Trace": 2,
                "Weave": 1,
            },
        )
        gadgets = {r.key["gadget_label"]: r for r in inventory["Gadget"].records}
        self.assertEqual(
            {k: (r.validated, r.value_count, r.tags) for k, r in gadgets.items()},
            {
                "gadget-one": (True, 3, ("tag-north",)),
                "gadget-two": (False, 1, ("tag-north", "tag-south")),
            },
        )
        self.assertEqual(
            {
                inventory["Gadget"].parent_class("frame", r.key)
                for r in gadgets.values()
            },
            {"dial_setting", "knob_setting"},
        )
        samples = {r.key["sample_code"]: r for r in inventory["Sample"].records}
        self.assertEqual(
            {k: r.validated for k, r in samples.items()},
            {
                "sample-0": None,
                "sample-1": None,
                "sample-2": None,
                build.UNVALIDATED_SAMPLE: None,
            },
        )
        self.assertIsNone(samples["sample-0"].key["anchor"])
        for code in ("sample-1", "sample-2"):
            resolved = inventory.resolve("Sample", samples[code])
            self.assertEqual(resolved["anchor"]["class"], "Tessera")
            self.assertEqual(len(resolved["members"]["set"]), 2)
        self.assertTrue(inventory["Sample"].replicated is False)
        self.assertTrue(inventory["Gadget"].replicated is True)

    def test_a_replicated_get_is_written_on_the_pinned_controller_then_copied(self):
        primary = self.root / "pinned" / "store.sqlite"
        pool = build.open_pool(self.cluster, primary, shards=3)
        try:
            shard_ids = list(pool._shards.keys())
            # not the first in the pool's order, so that a draw of index 0 is not the pin
            self.cluster.controller = shard_ids[1]
            self.cluster.calls.clear()
            dial = build.get_dial(pool, 9, 4)
            # the actors' calls: the broker's serial leases are not shard calls
            calls = [
                (c["shard"], c["method"], c["class"], c["kwargs"])
                for c in self.cluster.calls
                if c["shard"] is not None
            ]
            self.assertEqual(
                calls[0],
                (
                    self.cluster.controller,
                    "object_get",
                    "dial_setting",
                    ["insert_timestamp", "level", "stepping"],
                ),
            )
            self.assertEqual(
                calls[1:],
                [
                    (
                        sid,
                        "object_get",
                        "dial_setting",
                        ["insert_timestamp", "level", "serial", "stepping"],
                    )
                    for sid in self.cluster.replica_ids()
                ],
            )
            files = pool._shard_db_files
        finally:
            self.cluster.close_pool(pool)
        for sid, path in files.items():
            rows = _rows(path, "dial_setting")
            self.assertEqual([r[0] for r in rows], [dial.store_id], sid)


# ------------------------------------------------------------------------------------------------
# 3. the registry
# ------------------------------------------------------------------------------------------------


class TestTheRegistry(unittest.TestCase):
    def test_the_registry_exports_exactly_the_nine_names(self):
        self.assertEqual(set(registry.__all__), NINE)
        self.assertEqual(len(registry.__all__), 9)
        public = {n for n in vars(registry) if not n.startswith("_")}
        self.assertEqual(public, NINE)

    def test_tables_to_drop_gives_each_groups_tables(self):
        for group, tables in registry.drop_groups.items():
            with self.subTest(group=group):
                self.assertEqual(registry.tables_to_drop([group]), tables)
                self.assertEqual(registry.tables_to_drop([group, group]), tables)
        every = registry.tables_to_drop(list(registry.drop_groups))
        self.assertEqual(len(every), len(set(every)))
        self.assertEqual(
            set(every), {t for tables in registry.drop_groups.values() for t in tables}
        )
        self.assertEqual(registry.tables_to_drop([]), [])
        with self.assertRaises(ValueError) as cm:
            registry.tables_to_drop(["samples", "no-such-group"])
        self.assertIn('"no-such-group"', str(cm.exception))

    def test_dependent_tables_accepts_each_group_as_declared(self):
        declared = _built().tables
        self.assertEqual(list(MEASURED_DEPENDENTS), list(registry.drop_groups))
        for group, tables in registry.drop_groups.items():
            with self.subTest(group=group):
                self.assertTrue(set(tables) <= set(declared))
                found = dependent_tables(tables, registry.factories)
                self.assertEqual(found, MEASURED_DEPENDENTS[group])
                # what a group must be dropped with is itself in the groups
                self.assertEqual(
                    dependent_tables(tables + found, registry.factories), []
                )
        every = registry.tables_to_drop(list(registry.drop_groups))
        self.assertEqual(dependent_tables(every, registry.factories), [])
        # the union is every table but the kept ones
        self.assertEqual([n for n in declared if n not in every], KEPT)
        # a group holds a replicated table, and a group holds a sharded one
        self.assertTrue(set(every) & set(registry.replicated_tables))
        self.assertTrue(set(every) & set(registry.sharded_tables))

    def test_an_undeclared_name_is_refused_by_dependent_tables(self):
        with self.assertRaises(ValueError) as cm:
            dependent_tables(["Sample", "NotATable"], registry.factories)
        self.assertIn("'NotATable'", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
