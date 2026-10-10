"""
A refused or abandoned open closes the connections it made (extraction prompt 08b;
``[05-a-refused-open-leaves-its-engines-undisposed]``).

When ``ShardedPool``'s constructor raises, it closes what the open made before the exception
propagates: every actor built so far is closed by its own ``__exit__``, and the pool's engine is
disposed (``ShardedPool._close_refused_open``). Before 08b neither was done, and each engine's
pooled SQLite connection was closed only when the garbage collector reached it.

**How the tests count.** ``counting()`` wraps the open alone. It replaces ``sqlite3.connect`` and
``sqlite3.dbapi2.connect`` (which SQLAlchemy's SQLite dialect looks up when it connects) with a
wrapper that passes ``factory=`` a ``sqlite3.Connection`` subclass whose ``close()`` sets a flag,
and keeps every connection made; on exit it restores both. A connection is closed when its flag is
set, at the moment the exception reaches the test: nothing waits for the collector, so each count
is exact. Every count is over the list of connections made inside the test's own open, so a
connection another test left open cannot move it. Each test also requires that at least one
connection was counted, and every refusal test asserts the exception's type and message, so that
a cleanup that replaced the open's exception would fail it.

Every test reopens a store the stand-in pool (``datastorekit.tests.standin_pool``) wrote and
closed in ``setUp``, before the counting begins, or creates a new one beside it, in a temporary
directory, inside ``cluster.active()`` with stdout captured. A reopen with arguments other than
the registry's calls ``ShardedPool(...)`` itself. No Ray.
"""

import contextlib
import io
import sqlite3
import tempfile
import unittest
from pathlib import Path

import ray

from datastorekit.contract import VERSION_LABEL, VERSION_TABLE
from datastorekit.replication import ReadOnlyMiss, ReplicatedDivergence
from datastorekit.SQL.schema import StoreSchemaMismatch
from datastorekit.tests import standin_pool as sp
from datastorekit.tests.client import build, registry

MISMATCH = (
    "Mismatch between sharded tables supplied to the constructor and read from the existing "
    "ShardedPool"
)
# a read_table_config naming a sharded class, refused once every actor exists
NOT_REPLICATED_CONFIG = {"Sample": {"tables_arg": False}}
NOT_REPLICATED = (
    "It is only possible to configure a read-table method for a replicated table "
    '(class name="Sample")'
)
INTERRUPTED = "the open interrupted at read_largest_store_ids"


def tearDownModule():
    if ray.is_initialized():
        raise AssertionError("Ray was initialised by test_refused_open_closes_engines")


class _Counted(sqlite3.Connection):
    """A connection that records whether its ``close()`` ran, and the file it was opened on."""

    def __init__(self, database, *args, **kwargs):
        super().__init__(database, *args, **kwargs)
        self.database = str(database)
        self.closed_by_close = False

    def close(self):
        self.closed_by_close = True
        super().close()


@contextlib.contextmanager
def counting():
    """Count the connections made inside the block: yields the list of them, in order."""
    made = []
    saved = (sqlite3.connect, sqlite3.dbapi2.connect)
    real_connect = saved[1]

    def connect(*args, **kwargs):
        kwargs.setdefault("factory", _Counted)
        conn = real_connect(*args, **kwargs)
        if isinstance(conn, _Counted):
            made.append(conn)
        return conn

    sqlite3.connect = connect
    sqlite3.dbapi2.connect = connect
    try:
        yield made
    finally:
        sqlite3.connect, sqlite3.dbapi2.connect = saved


def left_open(made):
    return [conn for conn in made if not conn.closed_by_close]


class _RefusedOpenCase(unittest.TestCase):
    """A store the stand-in pool wrote and closed, in a temporary directory; the stand-in cluster
    stays active for the test."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.directory = Path(tmp.name)
        self.primary = self.directory / "store" / "store.sqlite"

        self.cluster = sp.StandinCluster()
        active = self.cluster.active()
        active.__enter__()
        self.addCleanup(active.__exit__, None, None, None)

        with contextlib.redirect_stdout(io.StringIO()):
            pool = build.open_pool(self.cluster, self.primary)
        self.shard_files = dict(pool._shard_db_files)
        self.cluster.close_pool(pool)

    def tearDown(self):
        self.assertFalse(ray.is_initialized())

    def arguments(self, **overrides):
        """The registry's arguments, as ``build.open_pool`` gives them, with ``overrides``."""
        kwargs = dict(
            version_label="standin",
            db_name=self.primary,
            ShardKeyType=registry.shard_key_type,
            ShardKeyStoreIdGetter=registry.shard_key_store_id,
            replicated_tables=registry.replicated_tables,
            sharded_tables=registry.sharded_tables,
            shards=3,
            factories=registry.factories,
            read_table_config=registry.read_table_config,
            serial_batch_sizes=registry.serial_batch_sizes,
        )
        kwargs.update(overrides)
        return kwargs

    def refused(self, expected, **overrides):
        """
        Open with the registry's arguments and ``overrides``, counting the connections the open
        makes; the open must raise ``expected``. Returns ``(exception, connections made)``. Any
        other exception reaches the runner as it was raised. Every counted connection still open
        is closed in cleanup, after the test's own assertions have read it.
        """
        made = []
        self.addCleanup(self.close_left_open, made)
        pool = None
        with counting() as counted, contextlib.redirect_stdout(io.StringIO()):
            try:
                pool = sp.sp_mod.ShardedPool(**self.arguments(**overrides))
            except expected as e:
                error = e
            finally:
                made.extend(counted)
        if pool is not None:
            self.cluster.close_pool(pool)
            self.fail(f"the open was not refused with {expected.__name__}")
        self.assertGreater(len(made), 0, "the open made no connection")
        return error, made

    @staticmethod
    def close_left_open(made):
        for conn in left_open(made):
            conn.close()

    def assertAllClosed(self, made):
        still_open = left_open(made)
        self.assertEqual(
            len(still_open),
            0,
            f"{len(still_open)} of {len(made)} connections the refused open made are still "
            f"open: {[conn.database for conn in still_open]}",
        )


class TestARefusedOpenClosesItsConnections(_RefusedOpenCase):
    """Refusals made before any actor exists: only the pool's engine has a connection."""

    def test_a_primary_that_differs_is_refused_and_closed(self):
        conn = sqlite3.connect(self.primary)
        try:
            with conn:
                conn.execute("CREATE TABLE extra (x INTEGER)")
        finally:
            conn.close()

        error, made = self.refused(StoreSchemaMismatch)
        primary = Path(self.primary).resolve()
        self.assertTrue(
            str(error).startswith(
                f'Cannot open sharded datastore "{primary}": the primary "{primary}" differs '
                "from the tables this code declares"
            ),
            str(error),
        )
        self.assertIn("extra", error.differences.extra_tables)
        self.assertAllClosed(made)

    def test_a_sharded_tables_mismatch_is_refused_and_closed(self):
        less_one = {
            name: attr
            for name, attr in registry.sharded_tables.items()
            if name != "Sample"
        }
        error, made = self.refused(RuntimeError, sharded_tables=less_one)
        self.assertEqual(str(error), MISMATCH)
        self.assertAllClosed(made)

    def test_a_divergence_at_open_is_refused_and_closed(self):
        conn = sqlite3.connect(self.shard_files[1])
        try:
            with conn:
                conn.execute(f'DELETE FROM "{VERSION_TABLE}"')
        finally:
            conn.close()

        error, made = self.refused(ReplicatedDivergence)
        self.assertIn("its replicated tables differ across shards", str(error))
        self.assertIn(VERSION_TABLE, [d["class_name"] for d in error.differences])
        self.assertAllClosed(made)

    def test_a_read_only_open_of_an_absent_label_is_refused_and_closed(self):
        error, made = self.refused(
            ReadOnlyMiss, read_only=True, version_label="absent-label"
        )
        self.assertEqual(error.class_name, VERSION_TABLE)
        self.assertEqual(error.payload, {VERSION_LABEL: "absent-label"})
        self.assertIn(
            f'was opened read-only, and a lookup of "{VERSION_TABLE}" matched no row',
            str(error),
        )
        self.assertAllClosed(made)


class TestARefusalAfterTheActorsClosesThem(_RefusedOpenCase):
    """Refusals and failures once the actors exist: the pool's engine and each actor's."""

    def test_a_read_table_config_refusal_closes_the_actors(self):
        error, made = self.refused(
            RuntimeError, read_table_config=NOT_REPLICATED_CONFIG
        )
        self.assertEqual(str(error), NOT_REPLICATED)
        self.assertAllClosed(made)

    def test_a_read_only_read_table_config_refusal_closes_the_actors(self):
        error, made = self.refused(
            RuntimeError, read_only=True, read_table_config=NOT_REPLICATED_CONFIG
        )
        self.assertEqual(str(error), NOT_REPLICATED)
        self.assertAllClosed(made)

    def test_a_new_store_whose_version_write_fails_closes_the_actors(self):
        # inside the constructor the cluster has no pool to resolve ``controller`` against, so
        # the controlling shard is pinned with pin_controller, which resolves it against the pool
        # making the write
        pin = self.cluster.pin_controller(0)
        pin.__enter__()
        self.addCleanup(pin.__exit__, None, None, None)
        self.cluster.fault(0, "object_get", VERSION_TABLE, "before")

        error, made = self.refused(
            sp.StandinActorDied, db_name=self.directory / "new" / "store.sqlite"
        )
        self.assertEqual(
            str(error),
            f"shard0000-store.object_get({VERSION_TABLE}) killed before it ran",
        )
        self.assertAllClosed(made)

    def test_an_actor_whose_exit_fails_after_it_ran_does_not_replace_the_refusal(self):
        self.cluster.fault(1, "__exit__", None, "after")
        error, made = self.refused(
            RuntimeError, read_table_config=NOT_REPLICATED_CONFIG
        )
        self.assertNotIsInstance(error, sp.StandinActorDied)
        self.assertEqual(str(error), NOT_REPLICATED)
        self.assertAllClosed(made)

    def test_an_actor_whose_exit_never_ran_does_not_replace_the_refusal(self):
        # shard 1's __exit__ is faulted before it runs, so its engine is never disposed and its
        # connection is the one left open. Under Ray a dead actor's process is gone, and its
        # connection with it; under the stand-in the test closes it, in the cleanup ``refused``
        # registers, so that the module leaves nothing open
        self.cluster.fault(1, "__exit__", None, "before")
        error, made = self.refused(
            RuntimeError, read_table_config=NOT_REPLICATED_CONFIG
        )
        self.assertNotIsInstance(error, sp.StandinActorDied)
        self.assertEqual(str(error), NOT_REPLICATED)

        still_open = left_open(made)
        self.assertEqual(
            [Path(conn.database).resolve() for conn in still_open],
            [Path(self.shard_files[1]).resolve()],
            f"{len(still_open)} of {len(made)} connections are still open",
        )

    def test_an_open_abandoned_by_keyboard_interrupt_closes_the_actors(self):
        # the hook fires once, before the first read_largest_store_ids call: outside the
        # stand-in's own try, so it reaches the constructor as an interrupt of the driver there
        # would. The cleanup's __exit__ calls run the hooks too, and must not raise
        fired = []

        def interrupt(shard_id, method, cls_name, when):
            if method == "read_largest_store_ids" and when == "before" and not fired:
                fired.append(shard_id)
                raise KeyboardInterrupt(INTERRUPTED)

        self.cluster.hooks.append(interrupt)
        self.addCleanup(self.cluster.hooks.remove, interrupt)

        # caught here, under any layer: a KeyboardInterrupt that left the test would end the run
        error, made = self.refused(KeyboardInterrupt)
        self.assertEqual(len(fired), 1)
        self.assertEqual(str(error), INTERRUPTED)
        self.assertAllClosed(made)


class TestAnOpenThatSucceeds(_RefusedOpenCase):
    def test_a_pool_that_opens_keeps_its_connections_until_it_is_closed(self):
        # the pool's engine and each of the three actors' keep a connection while the pool is
        # open; the cleanup of a refused open must not run on success
        with counting() as made, contextlib.redirect_stdout(io.StringIO()):
            pool = sp.sp_mod.ShardedPool(**self.arguments())
        open_while_open = len(left_open(made))
        self.cluster.close_pool(pool)
        open_after_close = len(left_open(made))

        self.assertGreater(len(made), 0)
        self.assertEqual(
            open_while_open,
            1 + len(self.shard_files),
            f"{open_while_open} of {len(made)} connections open while the pool is open",
        )
        self.assertEqual(open_after_close, 0)


if __name__ == "__main__":
    unittest.main()
