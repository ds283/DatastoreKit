"""
The refusal of a reopen whose ``sharded_tables`` differs from the store's record (extraction
prompt 08a; ``[02-an-unsupplied-sharded-table-raises-keyerror]``).

``ShardedPool._read_shard_data`` compares the sharded tables the primary records with the mapping
the constructor was given. A table the store records and the mapping lacks is listed under "The
following sharded tables are configured in the existing ShardedPool, but were not supplied to the
constructor:" and the open is refused with the mismatch ``RuntimeError``. Before 08a the loop
indexed the mapping with that table first, so the open was refused with a bare ``KeyError`` and
nothing was printed. Tests 1 and 2 pin the refusal, through the fixture's primary and through the
whole constructor.

Tests 3-6 pin the rest of the comparison, which 08a does not change: a supplied but unrecorded
table, a differing key attribute, a table the primary records twice (refused, and listed as "not
supplied", although it was), and a matching mapping, which reads with nothing printed.

Tests 1 and 3-6 use the primaries ``shard_store_fixtures.write_new_store`` writes (one sharded
table, ``Sample`` on ``k``) and a bare pool, with no actors. Test 2 reopens a store the stand-in
pool wrote (``datastorekit.tests.standin_pool``) through ``ShardedPool`` itself, given the neutral
client's registry less one sharded class. No Ray, and every store in a temporary directory.
"""

import contextlib
import io
import sqlite3
import tempfile
import unittest
from pathlib import Path

import ray

from datastorekit.tests import standin_pool as sp
from datastorekit.tests import shard_store_fixtures as fx
from datastorekit.tests.client import build, registry

MISMATCH = (
    "Mismatch between sharded tables supplied to the constructor and read from the existing "
    "ShardedPool"
)
KEY_MISMATCH = (
    "Some sharded tables had mismatching key configurations in the existing ShardedPool"
)
NOT_SUPPLIED = (
    "The following sharded tables are configured in the existing ShardedPool, but were not "
    "supplied to the constructor:"
)
NOT_CONFIGURED = (
    "The following sharded tables are supplied to the constructor, but are not configured in the "
    "existing ShardedPool:"
)
DIFFERENT_KEY = (
    "The following sharded tables were configured with a different key attribute in the "
    "existing ShardedPool:"
)


def tearDownModule():
    if ray.is_initialized():
        raise AssertionError("Ray was initialised by test_unsupplied_sharded_table")


def listed_under(printed: str, heading: str):
    """The indented names printed under ``heading``, in order, or None if it was not printed."""
    lines = printed.splitlines()
    if heading not in lines:
        return None
    names = []
    for line in lines[lines.index(heading) + 1 :]:
        if not line.startswith("  "):
            break
        names.append(line.strip())
    return names


class _FixtureCase(unittest.TestCase):
    """A primary ``write_new_store`` made, in a temporary directory."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.primary = Path(tmp.name) / "store" / "store.sqlite"
        fx.write_new_store(self.primary)

    def read(self, sharded_tables):
        """``_read_shard_data`` on a bare pool given ``sharded_tables``: (exception, printed)."""
        pool = fx.bare_pool(self.primary)
        pool._sharded_tables = dict(sharded_tables)
        out = io.StringIO()
        pool._create_engine()
        try:
            with contextlib.redirect_stdout(out):
                pool._read_shard_data()
        except Exception as e:
            return e, out.getvalue()
        finally:
            pool._engine.dispose()
        return None, out.getvalue()


class TestThroughTheFixture(_FixtureCase):
    def test_a_recorded_table_not_supplied_is_refused_with_the_mismatch(self):
        pool = fx.bare_pool(self.primary)
        pool._sharded_tables = {}
        out = io.StringIO()
        pool._create_engine()
        try:
            with contextlib.redirect_stdout(out):
                with self.assertRaises(RuntimeError) as ctx:
                    pool._read_shard_data()
        finally:
            pool._engine.dispose()

        self.assertNotIsInstance(ctx.exception, KeyError)
        self.assertEqual(str(ctx.exception), MISMATCH)
        printed = out.getvalue()
        self.assertEqual(listed_under(printed, NOT_SUPPLIED), ["Sample"])
        self.assertIsNone(listed_under(printed, NOT_CONFIGURED))
        self.assertIsNone(listed_under(printed, DIFFERENT_KEY))

    def test_a_supplied_table_not_recorded_is_refused_with_the_mismatch(self):
        error, printed = self.read({"Sample": "k", "Trace": "k"})
        self.assertIsInstance(error, RuntimeError)
        self.assertEqual(str(error), MISMATCH)
        self.assertEqual(listed_under(printed, NOT_CONFIGURED), ["Trace"])
        self.assertIsNone(listed_under(printed, NOT_SUPPLIED))

    def test_a_differing_key_attribute_is_refused_naming_both_keys(self):
        error, printed = self.read({"Sample": "j"})
        self.assertIsInstance(error, RuntimeError)
        self.assertEqual(str(error), KEY_MISMATCH)
        self.assertEqual(
            listed_under(printed, DIFFERENT_KEY),
            ['Sample: configured key="k", supplied key="j"'],
        )
        self.assertIsNone(listed_under(printed, NOT_SUPPLIED))
        self.assertIsNone(listed_under(printed, NOT_CONFIGURED))

    def test_a_table_recorded_twice_is_refused_as_before(self):
        conn = sqlite3.connect(self.primary)
        try:
            with conn:
                conn.execute(
                    'INSERT INTO sharded_tables (serial, "table", key_attr) VALUES (?, ?, ?)',
                    (1, "Sample", "k"),
                )
            rows = conn.execute(
                'SELECT serial, "table", key_attr FROM sharded_tables ORDER BY serial'
            ).fetchall()
        finally:
            conn.close()
        self.assertEqual(rows, [(0, "Sample", "k"), (1, "Sample", "k")])

        # the second row is listed as "not supplied", although the table was supplied: the
        # existing message, which 08a does not change
        error, printed = self.read({"Sample": "k"})
        self.assertIsInstance(error, RuntimeError)
        self.assertEqual(str(error), MISMATCH)
        self.assertEqual(listed_under(printed, NOT_SUPPLIED), ["Sample"])
        self.assertIsNone(listed_under(printed, NOT_CONFIGURED))

    def test_a_matching_mapping_reads_with_nothing_printed(self):
        error, printed = self.read(fx.SHARDED)
        self.assertIsNone(error)
        self.assertEqual(printed, "")


class TestThroughTheConstructor(unittest.TestCase):
    """A store the stand-in pool wrote, closed, then reopened by ``ShardedPool`` itself with the
    registry's ``sharded_tables`` less one class (``StandinCluster.open_pool`` passes the
    registry's mapping, so it cannot be given another)."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.primary = Path(tmp.name) / "store" / "store.sqlite"

        self.cluster = sp.StandinCluster()
        active = self.cluster.active()
        active.__enter__()
        self.addCleanup(active.__exit__, None, None, None)

        pool = build.open_pool(self.cluster, self.primary)
        self.cluster.close_pool(pool)

    def tearDown(self):
        self.assertFalse(ray.is_initialized())

    def reopen(self, sharded_tables):
        return sp.sp_mod.ShardedPool(
            version_label="standin",
            db_name=self.primary,
            ShardKeyType=registry.shard_key_type,
            ShardKeyStoreIdGetter=registry.shard_key_store_id,
            replicated_tables=registry.replicated_tables,
            sharded_tables=sharded_tables,
            shards=3,
            factories=registry.factories,
            read_table_config=registry.read_table_config,
            serial_batch_sizes=registry.serial_batch_sizes,
        )

    def test_a_recorded_table_not_supplied_is_refused_with_the_mismatch(self):
        self.assertGreater(len(registry.sharded_tables), 1)
        for left_out in registry.sharded_tables:
            with self.subTest(left_out=left_out):
                less_one = {
                    name: attr
                    for name, attr in registry.sharded_tables.items()
                    if name != left_out
                }
                out = io.StringIO()
                # any exception but the RuntimeError reaches the runner as it was raised
                try:
                    with contextlib.redirect_stdout(out):
                        pool = self.reopen(less_one)
                except RuntimeError as e:
                    error = e
                else:
                    self.cluster.close_pool(pool)
                    self.fail(f"the store opened without {left_out}")

                self.assertNotIsInstance(error, KeyError)
                self.assertEqual(str(error), MISMATCH)
                printed = out.getvalue()
                self.assertEqual(listed_under(printed, NOT_SUPPLIED), [left_out])
                self.assertIsNone(listed_under(printed, NOT_CONFIGURED))
                self.assertNotIn(">> Opened existing sharded datastore", printed)


if __name__ == "__main__":
    unittest.main()
