"""
A drop that would leave references is refused (prompts/datastore-generic-followup, prompt 01;
README §6.1, decision 1).

``--drop`` drops exactly the tables of the groups named. Production runs with foreign-key
enforcement off, so SQLite accepts a drop that leaves other tables' rows naming rows that are gone,
and a re-created table can then lease a serial that a stale row still names. A read-write
``ShardedPool`` therefore refuses ``drop_tables`` unless every table that names one of them is
among them. A reference is a foreign key **or** a parent a factory's ``inventory_spec`` declares,
followed transitively (``Datastore.SQL.schema.dependent_tables``).

1. ``TestDependentTables`` -- ``dependent_tables`` on the client's registry, through its drop
   groups: each group alone needs exactly the tables README §0.2 measured, in registry order; each
   group with those tables, and every group together, needs nothing more; a declared parent with no
   foreign key counts, a foreign key with no declared parent counts, and a table behind the first
   level counts; a name the registry does not declare raises ``ValueError``.
2. ``TestThePoolRefuses`` -- through the stand-in pool: a drop that leaves references is refused
   before any actor or engine exists, naming the tables given and every table that must go with
   them, on an existing store (whose files are unchanged) and on an absent one (no file is
   created); the undeclared-table refusal still comes first; a drop that names its dependents is
   accepted, and empties every table it names.

No Ray, nothing under ``var/``.
"""

import contextlib
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sqlalchemy as sqla

from datastorekit.SQL.schema import build_schema, dependent_tables
from datastorekit.replication import ReadOnlyWrite
from datastorekit.store_inventory import inventory_specs
from datastorekit.tests import standin_pool as sp
from datastorekit.tests.real_store_fixtures import build_full_store
from datastorekit.tests.client.registry import drop_groups, factories, tables_to_drop

# the tables each group must be dropped with, in registry order, measured on the neutral client's
# registry (extraction prompt 04b §2.2); the source's were its README §0.2's table
MEASURED = {
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

# the refused drop the pool tests use, and the groups it must be dropped with
REFUSED_GROUP = "tesserae"
WITH_ITS_DEPENDENTS = [REFUSED_GROUP, "samples", "traces"]


def _foreign_key_targets(table: str) -> set:
    tables = build_schema(sqla.MetaData(), factories).tables
    return {fk.column.table.name for fk in tables[table].foreign_keys}


# ------------------------------------------------------------------------------------------------
# 1. the derivation
# ------------------------------------------------------------------------------------------------


class TestDependentTables(unittest.TestCase):
    def test_each_group_alone_needs_its_measured_dependents(self):
        self.assertEqual(list(MEASURED), list(drop_groups))
        for group, tables in drop_groups.items():
            with self.subTest(group=group):
                self.assertEqual(dependent_tables(tables, factories), MEASURED[group])

    def test_each_group_with_its_dependents_needs_nothing_more(self):
        for group, tables in drop_groups.items():
            with self.subTest(group=group):
                self.assertEqual(
                    dependent_tables(list(tables) + MEASURED[group], factories), []
                )

    def test_every_group_together_needs_nothing(self):
        self.assertEqual(
            dependent_tables(tables_to_drop(list(drop_groups)), factories), []
        )

    def test_a_declared_parent_without_a_foreign_key_counts(self):
        # Sample names its Tessera parent across shards, with no foreign key
        self.assertNotIn("Tessera", _foreign_key_targets("Sample"))
        self.assertIn(
            "Tessera",
            inventory_specs(factories)["Sample"].dependencies(),
        )
        self.assertIn(
            "Sample",
            dependent_tables(drop_groups["tesserae"], factories),
        )

    def test_a_foreign_key_without_a_declared_parent_counts(self):
        # Sample_members names its member rows by foreign key, and declares no inventory_spec
        self.assertIsNone(factories["Sample_members"].inventory_spec())
        self.assertNotIn("Sample_members", inventory_specs(factories))
        self.assertIn("Tessera", _foreign_key_targets("Sample_members"))
        self.assertIn(
            "Sample_members",
            dependent_tables(drop_groups["tesserae"], factories),
        )

    def test_dependents_are_followed_transitively(self):
        # Sample_tags names no tesserae table itself, by either kind of reference; it names
        # Sample, which declares a Tessera parent
        tesserae = set(drop_groups["tesserae"])
        self.assertTrue(_foreign_key_targets("Sample_tags").isdisjoint(tesserae))
        self.assertNotIn("Sample_tags", inventory_specs(factories))
        self.assertIn(
            "Sample_tags",
            dependent_tables(drop_groups["tesserae"], factories),
        )

    def test_an_undeclared_name_is_refused(self):
        with self.assertRaises(ValueError) as cm:
            dependent_tables(["Sample", "NotATable"], factories)
        self.assertIn("'NotATable'", str(cm.exception))
        self.assertNotIn("'Sample'", str(cm.exception))


# ------------------------------------------------------------------------------------------------
# 2. the pool's refusal
# ------------------------------------------------------------------------------------------------


def _counts(path: Path, tables) -> dict:
    """The row count of each of ``tables`` in the SQLite file ``path``, or None if it is absent."""
    with contextlib.closing(sqlite3.connect(f"file:{path}?mode=ro", uri=True)) as conn:
        present = {
            r[0]
            for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        }
        return {
            t: (
                conn.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0]
                if t in present
                else None
            )
            for t in tables
        }


class TestThePoolRefuses(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.cluster = sp.StandinCluster()
        stack = contextlib.ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(self.cluster.active())

    def full_store(self, name: str):
        directory = self.root / name
        directory.mkdir()
        return build_full_store(directory)

    @contextlib.contextmanager
    def counting(self):
        """Record every stand-in actor constructed, and every engine the pool makes."""
        constructed = []
        engines = []
        original_remote = sp._Options.remote
        original_engine = sp.sp_mod.ShardedPool._create_engine

        def remote(options, *args, **kw):
            constructed.append(options._name)
            return original_remote(options, *args, **kw)

        def create_engine(pool):
            engines.append(pool)
            return original_engine(pool)

        with (
            mock.patch.object(sp._Options, "remote", remote),
            mock.patch.object(sp.sp_mod.ShardedPool, "_create_engine", create_engine),
        ):
            yield constructed, engines

    def assertRefused(self, primary: Path, drop) -> str:
        """Open ``primary`` read-write with ``drop``; require the refusal, before any actor or
        engine exists, and return its message."""
        with self.counting() as (constructed, engines):
            with self.assertRaises(RuntimeError) as cm:
                self.cluster.open_pool(primary, shards=2, drop_tables=drop)
        self.assertNotIsInstance(cm.exception, ReadOnlyWrite)
        self.assertEqual(constructed, [], "an actor was created")
        self.assertEqual(engines, [], "an engine was made")
        self.assertEqual(self.cluster.calls, [])
        return str(cm.exception)

    def assertTheMessage(self, message: str, primary: Path):
        dropped = drop_groups[REFUSED_GROUP]
        dependents = MEASURED[REFUSED_GROUP]
        prefix = f'Cannot open sharded datastore "{primary.resolve()}": '
        self.assertTrue(message.startswith(prefix), message)
        self.assertEqual(message.count("Cannot open sharded datastore"), 1, message)
        self.assertIn(repr(sorted(dropped)), message)
        self.assertIn(repr(dependents), message)
        self.assertIn("would name rows that are gone", message)
        self.assertIn("must be dropped too", message)
        self.assertTrue(message.endswith("Nothing was opened"), message)
        # tables only: no drop group, and nothing but what was given or derived
        for group in drop_groups:
            self.assertNotIn(group, message)
        self.assertEqual(
            message,
            prefix + f"cannot drop {sorted(dropped)} alone: the rows of {dependents} "
            "would name rows that are gone, so they must be dropped too. Nothing was opened",
        )

    def test_a_drop_that_leaves_references_is_refused_before_anything_is_opened(self):
        store = self.full_store("full")
        before = sp.store_checksums(store.primary)
        message = self.assertRefused(store.primary, tables_to_drop([REFUSED_GROUP]))
        self.assertTheMessage(message, store.primary)
        self.assertEqual(sp.store_checksums(store.primary), before)

    def test_nothing_is_created_for_an_absent_store(self):
        directory = self.root / "absent"
        directory.mkdir()
        primary = directory / "store.sqlite"
        message = self.assertRefused(primary, tables_to_drop([REFUSED_GROUP]))
        self.assertTheMessage(message, primary)
        self.assertEqual(list(directory.iterdir()), [])

    def test_an_undeclared_name_is_refused_first(self):
        # Gadget alone would meet this prompt's refusal; the undeclared name comes first
        self.assertNotEqual(dependent_tables(["Gadget"], factories), [])
        directory = self.root / "absent"
        directory.mkdir()
        primary = directory / "store.sqlite"
        message = self.assertRefused(primary, ["Gadget", "NotATable"])
        self.assertIn("which the registry does not declare as tables", message)
        self.assertIn("'NotATable'", message)
        self.assertNotIn("would name rows that are gone", message)
        self.assertEqual(list(directory.iterdir()), [])

    def test_a_drop_with_its_dependents_is_accepted(self):
        store = self.full_store("full")
        drop = tables_to_drop(WITH_ITS_DEPENDENTS)
        self.assertEqual(dependent_tables(drop, factories), [])
        before = {sid: _counts(path, drop) for sid, path in store.shard_files.items()}
        # the store holds rows in what is dropped, so an empty store cannot pass this test
        self.assertTrue(
            any(n for counts in before.values() for n in counts.values()), before
        )

        pool = self.cluster.open_pool(store.primary, shards=2, drop_tables=drop)
        self.cluster.close_pool(pool)

        # each actor re-creates the tables it dropped: present, and empty, on every shard
        after = {sid: _counts(path, drop) for sid, path in store.shard_files.items()}
        self.assertEqual(
            after, {sid: {t: 0 for t in drop} for sid in store.shard_files}
        )


if __name__ == "__main__":
    unittest.main()
