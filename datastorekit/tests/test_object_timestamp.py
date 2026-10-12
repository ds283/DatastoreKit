"""
The object carries a timestamp (``object-timestamp`` prompt 01, decision U1).

``DatastoreObject(store_id, *, timestamp=None)`` keeps ``timestamp`` and exposes it as a read-only
property. The layer never sets it and never reads it: a factory that reads a row of a class
registered with ``"timestamp": True`` may pass the row's ``timestamp``
(``docs/client-contract.md`` §9.6). The stamped class and its factory are
``tests/client/stamped.py``'s, outside the neutral client's registry:

1. ``DatastoreObject(3)`` has ``timestamp`` ``None``, ``store_id`` 3 and ``available`` true;
   ``DatastoreObject(None)`` has ``timestamp`` ``None``, ``available`` false, and its
   ``store_id`` raises the ``RuntimeError`` it raised before; ``DatastoreObject(3, timestamp=t)``
   returns ``t`` itself;
2. through the pool, on the stamped class, on a fresh store: a get that inserts answers
   ``_new_insert`` with ``timestamp`` ``None``, since the layer does not fill it; the row's
   ``timestamp`` column then holds one value, the same on every shard; after a read-write reopen a
   get answers ``_deserialized``, the same serial, and a ``datetime`` equal to that value, and so
   does a get sent to each shard's actor directly; a read-only reopen answers the same;
3. assigning ``timestamp`` raises ``AttributeError``, and so does deleting it; the value is
   unchanged afterwards;
4. a second positional argument raises ``TypeError``;
5. a stamped and an unstamped object each round-trip ``ray.cloudpickle``.

Under ``v0.2.3``'s ``DatastoreObject``, which takes ``store_id`` alone and has no ``timestamp``,
test 1 errors with ``AttributeError`` at its first read of ``timestamp``, and tests 2, 3 and 5
error with ``TypeError`` where they pass ``timestamp=``; test 4 passes there, since that
constructor refuses a second positional argument too (it is the test a positional-or-keyword
``timestamp`` fails).

The raw read of a shard returns the ``timestamp`` column as SQLite's text; it is compared with a
get's answer by ``datetime.fromisoformat``. Serials are not fixed between runs, so each is compared
with one read from another call. On the stand-in pool, every store in a temporary directory.
``ray.cloudpickle`` is imported from Ray, which it does not start. No Ray.
"""

import contextlib
import io
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

import ray
from ray import cloudpickle

from datastorekit.object import DatastoreObject
from datastorekit.tests import standin_pool as sp
from datastorekit.tests.client import build, registry
from datastorekit.tests.client.stamped import (
    STAMPED_COLUMN,
    STAMPED_TABLE,
    stamped_registry,
    stamped_tally,
)

# a datetime with microseconds, which SQLite's text keeps and a get must return as it was
STAMP = datetime(2026, 10, 12, 9, 30, 15, 123456)

# the integer the stamped class's row is got by
TALLY = 17


def tearDownModule():
    if ray.is_initialized():
        raise AssertionError("Ray was initialised by test_object_timestamp")


def _new_insert(obj) -> bool:
    return getattr(obj, "_new_insert", False) is True


def _deserialized(obj) -> bool:
    return getattr(obj, "_deserialized", False) is True and not _new_insert(obj)


class TestTheArgumentAndTheProperty(unittest.TestCase):
    """Test 1."""

    def test_the_timestamp_is_none_by_default_and_what_was_given(self):
        stored = DatastoreObject(3)
        self.assertIsNone(stored.timestamp)
        self.assertEqual(stored.store_id, 3)
        self.assertTrue(stored.available)

        unstored = DatastoreObject(None)
        self.assertIsNone(unstored.timestamp)
        self.assertFalse(unstored.available)
        with self.assertRaises(RuntimeError) as raised:
            unstored.store_id
        self.assertEqual(
            str(raised.exception),
            "Attempt to read datastore id before it has been set",
        )

        stamped = DatastoreObject(3, timestamp=STAMP)
        self.assertIs(stamped.timestamp, STAMP)
        self.assertEqual(stamped.store_id, 3)
        self.assertTrue(stamped.available)


class TestThroughThePool(unittest.TestCase):
    """Test 2."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.directory = Path(tmp.name)

        self.cluster = sp.StandinCluster()
        active = self.cluster.active()
        active.__enter__()
        self.addCleanup(active.__exit__, None, None, None)

        self.factories, self.replicated_tables = stamped_registry()

    def tearDown(self):
        self.assertFalse(ray.is_initialized())

    def open(self, read_only: bool = False):
        """
        A pool on the store ``"stamped"`` with the stamped registry, built as
        ``StandinCluster.open_pool`` builds one, read-write unless ``read_only``.
        """
        primary = self.directory / "stamped" / "store.sqlite"
        with contextlib.redirect_stdout(io.StringIO()):
            pool = sp.sp_mod.ShardedPool(
                version_label="standin",
                db_name=primary,
                ShardKeyType=registry.shard_key_type,
                ShardKeyStoreIdGetter=registry.shard_key_store_id,
                replicated_tables=self.replicated_tables,
                sharded_tables=registry.sharded_tables,
                shards=3,
                factories=self.factories,
                read_only=read_only,
            )
        self.cluster.pool = pool
        return pool

    def close(self, pool):
        self.cluster.close_pool(pool)

    def get(self, pool):
        return build.resolve(pool.object_get(STAMPED_TABLE, **{STAMPED_COLUMN: TALLY}))

    def stamps_on_every_shard(self, pool) -> set:
        """The raw values of the stamped table's ``timestamp`` column, the same on every shard."""
        found = set()
        for sid, path in sorted(pool._shard_db_files.items()):
            columns = sp.table_columns(path, STAMPED_TABLE)
            self.assertIn("timestamp", columns, sid)
            index = columns.index("timestamp")
            values = {row[index] for row in sp.shard_rows(pool, STAMPED_TABLE)[sid]}
            if found:
                self.assertEqual(values, found, sid)
            found = values
        return found

    def test_the_stamp_is_the_rows_and_the_layer_does_not_fill_it(self):
        # a get that inserts: the factory cannot know the stamp the actor adds
        pool = self.open()
        try:
            inserted = self.get(pool)
        finally:
            self.close(pool)
        self.assertIsInstance(inserted, stamped_tally)
        self.assertTrue(_new_insert(inserted))
        self.assertEqual(inserted.tally, TALLY)
        self.assertIsNone(inserted.timestamp)
        serial = inserted.store_id

        # the row's stamp: one value, the same on every shard
        raw = self.stamps_on_every_shard(pool)
        self.assertEqual(len(raw), 1)
        (text,) = raw
        self.assertIsInstance(text, str)
        stamp = datetime.fromisoformat(text)

        # a read-write reopen: the factory reads the row, and passes its stamp
        pool = self.open()
        try:
            found = self.get(pool)
            self.assertIsInstance(found, stamped_tally)
            self.assertTrue(_deserialized(found))
            self.assertEqual(found.store_id, serial)
            self.assertIsInstance(found.timestamp, datetime)
            self.assertEqual(found.timestamp, stamp)

            # each shard's actor, asked directly, answers the same stamp
            self.assertEqual(len(pool._shards), 3)
            for sid, actor in sorted(pool._shards.items()):
                with self.subTest(shard=sid):
                    direct = ray.get(
                        actor.object_get.remote(
                            STAMPED_TABLE, **{STAMPED_COLUMN: TALLY}
                        )
                    )
                    self.assertTrue(_deserialized(direct))
                    self.assertEqual(direct.store_id, serial)
                    self.assertEqual(direct.timestamp, stamp)
        finally:
            self.close(pool)

        # a read-only reopen answers the same
        pool = self.open(read_only=True)
        try:
            found = self.get(pool)
            self.assertTrue(_deserialized(found))
            self.assertEqual(found.store_id, serial)
            self.assertEqual(found.timestamp, stamp)
        finally:
            self.close(pool)

        # nothing above wrote the stamp again
        self.assertEqual(self.stamps_on_every_shard(pool), raw)


class TestReadOnly(unittest.TestCase):
    """Test 3."""

    def test_the_timestamp_cannot_be_assigned_or_deleted(self):
        for obj in (
            DatastoreObject(3, timestamp=STAMP),
            stamped_tally(3, TALLY, timestamp=STAMP),
        ):
            with self.subTest(cls=type(obj).__name__):
                with self.assertRaises(AttributeError):
                    obj.timestamp = datetime(2000, 1, 1)
                with self.assertRaises(AttributeError):
                    del obj.timestamp
                self.assertIs(obj.timestamp, STAMP)


class TestKeywordOnly(unittest.TestCase):
    """Test 4."""

    def test_a_second_positional_argument_is_refused(self):
        with self.assertRaises(TypeError):
            DatastoreObject(3, STAMP)


class TestSerialisation(unittest.TestCase):
    """Test 5."""

    def test_stamped_and_unstamped_objects_round_trip_cloudpickle(self):
        for obj, stamp in (
            (stamped_tally(4, TALLY, timestamp=STAMP), STAMP),
            (stamped_tally(5, TALLY + 1), None),
        ):
            with self.subTest(store_id=obj.store_id):
                copy = cloudpickle.loads(cloudpickle.dumps(obj))
                self.assertIsNot(copy, obj)
                self.assertIsInstance(copy, stamped_tally)
                self.assertEqual(copy.store_id, obj.store_id)
                self.assertEqual(copy.tally, obj.tally)
                self.assertEqual(copy.timestamp, stamp)
        self.assertFalse(ray.is_initialized())
