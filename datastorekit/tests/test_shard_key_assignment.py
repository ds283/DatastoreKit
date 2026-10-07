"""
The shard map saved on disk is the one the pool held (prompt 03a §2.5).

``ShardedPool._assign_shard_keys`` gives each new shard-key object a shard, in memory
(``_shard_keys``) and in the primary's ``shard_keys`` table (``key_serial``, ``shard_id``). The
saved row must name the object's own serial: a reopened pool reads its map from that table, and
every sharded row of the object was written on the shard the map in memory named. If the insert
bound the serial under a name the table does not have, SQLAlchemy would drop it and
``key_serial`` would autoincrement, so the saved map would hold the right shards under the wrong
serials. That cannot be seen while keys are assigned in serial order from 1, since the
autoincremented serials then equal the objects' own.

So the fixture assigns keys **out of serial order**, through the layer's own paths and the
stand-in pool's faults alone:

1. a get of keypoint A is killed on a replica, so that A is inserted (serial 1) and the write is
   left in flight with no shard key assigned to A;
2. the store is reopened: the check at open copies A to the replica and clears the record, and
   assigns no key;
3. one get inserts keypoints B and C (serials 2 and 3), and their keys are assigned; then a get of
   A assigns A's key last.

The keys are therefore assigned in the order 2, 3, 1, and an autoincremented ``key_serial`` would
give 1, 2, 3. One Sample is then stored on each keypoint's shard, and the store is closed and
reopened.

The tests require that the map saved in the primary equals the map the pool held before it was
closed and the map the reopened pool reads; and that every Sample is found, after the reopen, on
the shard that map names, and on no other.

No Ray, and every store is in a temporary directory.
"""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import ray

from datastorekit.tests import standin_pool as sp
from datastorekit.tests.client import build
from datastorekit.tests.client.objects import SerialHandle

# the keypoints: A is inserted first, and has its shard key assigned last
POSITION_A = 0.25
POSITIONS_B_C = (0.5, 1.0)


def tearDownModule():
    if ray.is_initialized():
        raise AssertionError("Ray was initialised by test_shard_key_assignment")


class TestShardKeysAssignedOutOfSerialOrder(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.primary = Path(tmp.name) / "store" / "store.sqlite"

        self.cluster = sp.StandinCluster()
        active = self.cluster.active()
        active.__enter__()
        self.addCleanup(active.__exit__, None, None, None)
        self.addCleanup(self.close)

        # 1. the get of A, killed on one replica: A is held by the controller and the other
        # replica, the record is left set, and no shard key is assigned
        pool = self.cluster.open_pool(self.primary)
        self.shard_ids = list(pool._shards.keys())
        self.files = dict(pool._shard_db_files)
        self.cluster.controller = self.shard_ids[1]
        self.replica = self.cluster.replica_ids()[0]
        self.cluster.fault(self.replica, "object_get", "keypoint", "before")
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(sp.StandinActorDied):
                build.get_keypoint(pool, POSITION_A)
        self.cluster.clear_faults()
        self.cluster.controller = None
        self.close()

        # 2. the reopen copies A to the replica and assigns no key
        self.pool = self.cluster.open_pool(self.primary)
        self.copied = [
            (a["action"], a["class_name"], a["shard"])
            for a in self.pool.reconciliation["repaired"]
        ]
        self.keys_after_reopen = dict(self.pool._shard_keys)

        # 3. B and C, new, get their keys; then A gets its key, last
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            b, c = build.get_keypoints(self.pool, POSITIONS_B_C)
            a = build.get_keypoint(self.pool, POSITION_A)
        self.printed = printed.getvalue()
        self.points = {"A": a, "B": b, "C": c}
        self.assignment_order = list(self.pool._shard_keys)

        # one Sample on each keypoint, on the shard the map in memory names
        self.samples = {}
        for name, point in self.points.items():
            sample = build.store_sample(
                self.pool,
                build.make_sample(point, SerialHandle(1), f"sample-{name}"),
            )
            self.samples[name] = sample
        self.map_in_memory = dict(self.pool._shard_keys)
        self.close()

        # the map saved in the primary, read from the closed store
        self.map_on_disk = dict(
            sp._read(self.primary, 'SELECT key_serial, shard_id FROM "shard_keys"')
        )

        self.pool = self.cluster.open_pool(self.primary)
        self.map_reopened = dict(self.pool._shard_keys)

    def close(self):
        self.cluster.clear_faults()
        if self.cluster.pool is not None:
            self.cluster.close_pool()
        self.pool = None

    def test_the_keys_were_assigned_out_of_serial_order(self):
        """The fixture's premise: A was copied by the check at open with no key, and the keys were
        then assigned in an order that is not the order of the serials."""
        a, b, c = (self.points[n].store_id for n in ("A", "B", "C"))
        self.assertEqual([("copied", "keypoint", self.replica)], self.copied)
        self.assertEqual({}, self.keys_after_reopen)
        self.assertEqual([1, 2, 3], [a, b, c])
        self.assertEqual([b, c, a], self.assignment_order)
        self.assertNotIn("MISMATCH", self.printed)

    def test_the_saved_map_is_the_map_in_memory_and_the_reopened_map(self):
        serials = sorted(p.store_id for p in self.points.values())
        self.assertEqual(serials, sorted(self.map_in_memory))
        self.assertEqual(self.map_in_memory, self.map_on_disk)
        self.assertEqual(self.map_in_memory, self.map_reopened)

    def test_every_sample_is_on_the_shard_the_reopened_map_names(self):
        for name, point in self.points.items():
            with self.subTest(keypoint=name):
                sample = self.samples[name]
                shard = self.map_reopened[point.store_id]
                # the Sample's row is on that shard's file, and on no other
                holders = [
                    sid
                    for sid, path in sorted(self.files.items())
                    if sp._read(
                        path,
                        'SELECT serial FROM "Sample" WHERE serial = ? AND sample_code = ?',
                        (sample.store_id, sample.code),
                    )
                ]
                self.assertEqual([shard], holders)
                # and the reopened pool, which reads it from the shard its map names, finds it
                found = build.read_samples(self.pool, point)
                self.assertEqual(
                    [(sample.store_id, sample.code)],
                    [(s.store_id, s.code) for s in found],
                )


if __name__ == "__main__":
    unittest.main()
