"""
A closed pool, and a refused open, release their actors' names (``actor-names`` prompt 01;
``[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]``).

``ShardedPool`` gives its actors fixed names in Ray's namespace: the broker ``SerialPoolBroker``
and each shard ``shard{key:04d}-store``. Before this campaign ``__exit__`` released none of them,
and a name was freed only when the pool object holding the handles was collected, so a store
could not be reopened in one Ray session while a closed pool was still referenced. Now
``__exit__`` kills each shard actor and the broker once it has closed them, a refused open kills
what it made, and a second ``__exit__`` does nothing. The names do not change, so two pools open
at once still collide.

1. a read-write pool releases its names at ``__exit__``: the store reopens read-write while the
   closed pool is referenced, and a get through the new pool finds what the first wrote;
2. a read-only pool releases its names at ``__exit__``, and a read-write open follows;
3. an open refused once every actor exists (a ``read_table_config`` naming a sharded class)
   releases its names while its exception, whose traceback holds the half-built pool, is held;
4. two open pools still collide: a second open raises ``ValueError`` naming ``SerialPoolBroker``,
   the first pool still serves a get, and once it is closed an open works;
5. a second ``__exit__`` raises nothing and calls no actor;
6. a closed pool's handles are dead: a call through one raises ``StandinActorDied`` on
   ``ray.get``;
7. a pool closed while this process is not connected to Ray starts no Ray (``actor-names`` prompt
   01b; ``[02-closing-a-pool-can-start-ray]``): with Ray's own ``ray.kill`` and the pool's own
   ``_ray_is_running`` restored, as a stand-in that does not stand in ``ray.kill`` leaves them,
   and ``ray.init`` replaced by a function that records its call and raises, ``__exit__`` returns,
   ``ray.init`` is never called, the actors are not killed, and Ray is not initialised;
8. the pool's ``_ray_is_running`` follows ``ray.is_initialized()``: true when it is true, false
   when it is false (``actor-names`` prompt 01b).

Ray's ``ray.kill`` is one of its auto-init calls: when the process is not connected to Ray it runs
``ray.init()`` first. So ``_kill_actors`` kills nothing when ``_ray_is_running()`` is false. The
stand-in makes ``_ray_is_running`` true inside ``active()``, so tests 7 and 8 use the module's own
function, captured when this module is imported, outside any ``active()``. Test 7's replacement of
``ray.init`` is what keeps it from starting Ray, even if the guard is removed: Ray's auto-init calls
``ray.init()`` through the ``ray`` module's attribute.

Each test opens its pools in one ``StandinCluster``, which stands for one Ray session: it reserves
each actor's name until the handle is killed, and refuses a call to a killed handle
(``datastorekit.tests.standin_pool``). Every store is in a temporary directory, and the pools are
the real ``ShardedPool``, ``Datastore`` actor code, factories and broker on stand-in shards. Serials
are not fixed between runs, so each is compared with one read from another call, never with a
literal. No Ray.
"""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import ray

from datastorekit.tests import standin_pool as sp
from datastorekit.tests.client import build

BROKER = "SerialPoolBroker"
TAKEN = "is already taken"
# a read_table_config naming a sharded class, refused once every actor exists
NOT_REPLICATED_CONFIG = {"Sample": {"tables_arg": False}}
NOT_REPLICATED = (
    "It is only possible to configure a read-table method for a replicated table "
    '(class name="Sample")'
)
POSITION = 0.25
KEYPOINT_TABLE = "keypoint"

# Ray's own ray.kill and the pool's own _ray_is_running, captured when this module is imported,
# outside any StandinCluster.active(), which stands in both
RAY_KILL = ray.kill
RAY_IS_RUNNING = sp.sp_mod._ray_is_running


def tearDownModule():
    if ray.is_initialized():
        raise AssertionError(
            "Ray was initialised by test_closed_pool_releases_its_names"
        )


class _OneSessionCase(unittest.TestCase):
    """A temporary directory, and one stand-in cluster, active for the test."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.primary = Path(tmp.name) / "store" / "store.sqlite"

        self.cluster = sp.StandinCluster()
        active = self.cluster.active()
        active.__enter__()
        self.addCleanup(active.__exit__, None, None, None)

    def tearDown(self):
        self.assertFalse(ray.is_initialized())

    def open(self, **kwargs):
        return build.open_pool(self.cluster, self.primary, **kwargs)

    def close(self, pool):
        self.cluster.close_pool(pool)

    def keypoint_serial(self, pool) -> int:
        return build.get_keypoint(pool, POSITION).store_id

    def assertFoundNotWritten(self, pool, serial: int):
        """A get through ``pool`` finds the keypoint of ``serial``, and writes no row."""
        before = sp.shard_rows(pool, KEYPOINT_TABLE)
        self.assertEqual(self.keypoint_serial(pool), serial)
        self.assertEqual(sp.shard_rows(pool, KEYPOINT_TABLE), before)


class TestAClosedPoolReleasesItsNames(_OneSessionCase):
    def test_a_read_write_pool_releases_its_names_at_exit(self):
        first = self.open()
        serial = self.keypoint_serial(first)
        self.close(first)

        # the closed pool is still referenced, by `first`
        second = self.open()
        try:
            self.assertFoundNotWritten(second, serial)
        finally:
            self.close(second)
        self.assertIsNotNone(first)

    def test_a_read_only_pool_releases_its_names_at_exit(self):
        writer = self.open()
        serial = self.keypoint_serial(writer)
        self.close(writer)

        # a read-only pool refuses a miss, so its get finds the row or raises
        reader = self.open(read_only=True)
        try:
            self.assertEqual(self.keypoint_serial(reader), serial)
        finally:
            self.close(reader)

        # both closed pools are still referenced
        second = self.open()
        try:
            self.assertFoundNotWritten(second, serial)
        finally:
            self.close(second)
        self.assertIsNotNone(writer)
        self.assertIsNotNone(reader)

    def test_a_refused_open_releases_its_names(self):
        # the refusal comes after the broker and every shard actor exist. The exception is held
        # with its traceback, whose frames hold the half-built pool
        held = []
        try:
            self.open(read_table_config=NOT_REPLICATED_CONFIG)
        except RuntimeError as e:
            held.append(e)
        self.assertEqual(len(held), 1, "the open was not refused")
        self.assertEqual(str(held[0]), NOT_REPLICATED)
        self.assertIsNotNone(held[0].__traceback__)

        pool = self.open()
        try:
            serial = self.keypoint_serial(pool)
            self.assertFoundNotWritten(pool, serial)
        finally:
            self.close(pool)
        self.assertEqual(len(held), 1)


class TestTwoOpenPoolsStillCollide(_OneSessionCase):
    def test_a_second_open_while_a_pool_is_open_is_refused_by_name(self):
        first = self.open()
        serial = self.keypoint_serial(first)
        try:
            with self.assertRaises(ValueError) as refused:
                self.open()
            self.assertIn(TAKEN, str(refused.exception))
            self.assertIn(BROKER, str(refused.exception))

            # the refused open killed nothing of the open pool's
            self.assertFoundNotWritten(first, serial)
        finally:
            self.close(first)

        # once the first is closed (and still referenced), an open works
        third = self.open()
        try:
            self.assertFoundNotWritten(third, serial)
        finally:
            self.close(third)
        self.assertIsNotNone(first)


class TestAfterExit(_OneSessionCase):
    def test_a_second_exit_does_nothing(self):
        pool = self.open()
        self.keypoint_serial(pool)
        self.close(pool)

        calls = len(self.cluster.calls)
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            pool.__exit__(None, None, None)
        self.assertEqual(len(self.cluster.calls), calls)
        self.assertEqual(printed.getvalue(), "")

    def test_a_closed_pools_handles_are_dead(self):
        pool = self.open()
        self.keypoint_serial(pool)
        self.close(pool)

        calls = len(self.cluster.calls)
        for key, handle in pool._shards.items():
            with self.subTest(shard=key):
                ref = handle.read_largest_store_ids.remote()
                with self.assertRaises(sp.StandinActorDied) as died:
                    ray.get(ref)
                self.assertIn(handle.name, str(died.exception))
                self.assertIn("read_largest_store_ids", str(died.exception))
        self.assertEqual(len(self.cluster.calls), calls)


class TestClosingAPoolStartsNoRay(_OneSessionCase):
    def test_a_pool_closed_while_not_connected_to_ray_starts_no_ray(self):
        pool = self.open()
        self.keypoint_serial(pool)
        held = dict(self.cluster.names)

        inits = []

        def refused_init(*args, **kwargs):
            inits.append(1)
            raise RuntimeError("ray.init() called while closing a pool")

        # ray.init is stood in first and restored last, so that Ray's own ray.kill is never in
        # place without it: Ray's auto-init would call it, and this replacement refuses
        returned = False
        with mock.patch.object(ray, "init", refused_init):
            with mock.patch.object(ray, "kill", RAY_KILL):
                with mock.patch.object(sp.sp_mod, "_ray_is_running", RAY_IS_RUNNING):
                    self.close(pool)
                    returned = True

        self.assertEqual(inits, [])
        self.assertTrue(returned)
        self.assertFalse(ray.is_initialized())
        # the pool is marked closed, and its actors were not killed: their names are still held
        self.assertTrue(pool._closed)
        self.assertEqual(self.cluster.names, held)

    def test_ray_is_running_follows_ray_is_initialized(self):
        # inside active(), the module's attribute is the stand-in's; the captured function is
        # the module's own
        self.assertIsNot(sp.sp_mod._ray_is_running, RAY_IS_RUNNING)

        with mock.patch.object(ray, "is_initialized", lambda: True):
            self.assertIs(RAY_IS_RUNNING(), True)
        with mock.patch.object(ray, "is_initialized", lambda: False):
            self.assertIs(RAY_IS_RUNNING(), False)


if __name__ == "__main__":
    unittest.main()
