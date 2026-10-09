"""
The caller's payloads under ``ShardedPool.object_get_vectorized`` (extraction prompt 08a;
``[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]``).

``object_get_vectorized(cls, shard_key, payload_data)`` sends every payload to the shard of
``shard_key`` with the shard key merged into it. Before 08a it merged the key into each of the
caller's dicts in place, so the caller's dicts changed under it. It now sends copies, with the key
merged last, so that a payload carrying its own value for the key's field still gets the pool's.

1. the caller's dicts are unchanged after the call (their contents, compared with a deep copy
   taken before it);
2. the same list passed twice with the same key gives the same rows;
3. the same list passed with a second key, on another shard, gives that shard's rows, and its
   dicts are still unchanged;
4. a payload that carries its own value for the key's field gets the pool's key: the row found is
   the pool key's;
5. the rows of a reused list equal those of a call made with fresh dicts.

Tests 1 and 3 fail on the layer before 08a; tests 2, 4 and 5 pin what the change must keep.

The pools are the real ``ShardedPool``, ``Datastore`` actor code, factories and broker on stand-in
shards (``datastorekit.tests.standin_pool``), on the neutral client's ``Tessera``, sharded on
``k`` and keyed on a ``keypoint_alias``. The stand-in actors run in-process, which is how a test
sees the caller's dicts at all; but the pool merges the key in the driver, before the call to the
actor is made, so under Ray the caller's dicts changed exactly as they do here. Serials are not
fixed between runs (the controlling shard of a replicated write is drawn at random), so every row
is compared with a row from another call, never with a literal serial.

No Ray, and every store in a temporary directory.
"""

import copy
import tempfile
import unittest
from pathlib import Path

import ray

from datastorekit.tests import standin_pool as sp
from datastorekit.tests.client import build

# two keypoints, so two shard keys, each with the alias a Tessera is keyed on
POSITIONS = (1.0, 2.0)
OFFSET = 0.5
WEIGHTS = (0.25, 0.75)


def tearDownModule():
    if ray.is_initialized():
        raise AssertionError("Ray was initialised by test_vectorized_get_payloads")


def payloads():
    """A fresh list of fresh payload dicts."""
    return [{"weight": w} for w in WEIGHTS]


def rows(tesserae):
    """What identifies each row found: its serial, its alias's serial and its weight."""
    return [(t.store_id, t.k.store_id, t.weight) for t in tesserae]


class TestTheCallersPayloads(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.primary = Path(tmp.name) / "store" / "store.sqlite"

        self.cluster = sp.StandinCluster()
        active = self.cluster.active()
        active.__enter__()
        self.addCleanup(active.__exit__, None, None, None)

        self.pool = build.open_pool(self.cluster, self.primary)
        self.addCleanup(self.cluster.close_pool, self.pool)
        self.a1, self.a2 = (
            build.get_alias(self.pool, build.get_keypoint(self.pool, p), OFFSET)
            for p in POSITIONS
        )
        # the two keys are on different shards
        self.assertNotEqual(self.shard_of(self.a1), self.shard_of(self.a2))

    def tearDown(self):
        self.assertFalse(ray.is_initialized())

    def shard_of(self, alias):
        return self.pool._shard_keys[self.pool._ShardKeyStoreIdGetter(alias)]

    def get(self, alias, payload_data):
        return build.resolve(
            self.pool.object_get_vectorized(
                "Tessera", {"k": alias}, payload_data=payload_data
            )
        )

    def test_the_callers_dicts_are_unchanged(self):
        data = payloads()
        before = copy.deepcopy(data)
        found = self.get(self.a1, data)

        self.assertEqual(len(found), len(WEIGHTS))
        self.assertEqual(data, before)
        for d in data:
            self.assertNotIn("k", d)

    def test_the_same_list_twice_with_the_same_key_gives_the_same_rows(self):
        data = payloads()
        first = self.get(self.a1, data)
        second = self.get(self.a1, data)

        self.assertEqual(len({t.store_id for t in first}), len(WEIGHTS))
        self.assertEqual(rows(second), rows(first))
        self.assertEqual(
            [t.k.store_id for t in first], [self.a1.store_id] * len(WEIGHTS)
        )
        self.assertEqual(list(t.weight for t in first), list(WEIGHTS))

    def test_the_same_list_with_a_second_key_gives_that_shards_rows(self):
        data = payloads()
        before = copy.deepcopy(data)
        on_a1 = self.get(self.a1, data)
        on_a2 = self.get(self.a2, data)
        self.assertEqual(data, before)

        fresh_a2 = self.get(self.a2, payloads())
        self.assertEqual(rows(on_a2), rows(fresh_a2))
        self.assertEqual(
            [t.k.store_id for t in on_a2], [self.a2.store_id] * len(WEIGHTS)
        )
        self.assertEqual(
            {t.store_id for t in on_a2} & {t.store_id for t in on_a1}, set()
        )
        # each row is on the second key's shard, and on no other
        a2_shard = self.shard_of(self.a2)
        for sid, shard_rows in sp.shard_rows(self.pool, "Tessera").items():
            serials = {r[0] for r in shard_rows}
            with self.subTest(shard=sid):
                for t in on_a2:
                    self.assertEqual(t.store_id in serials, sid == a2_shard)

    def test_a_payload_carrying_the_key_field_gets_the_pools_key(self):
        (expected,) = self.get(self.a1, [{"weight": WEIGHTS[0]}])

        # the payload names the second key; the pool's key is the first
        (found,) = self.get(self.a1, [{"weight": WEIGHTS[0], "k": self.a2}])

        self.assertEqual(found.store_id, expected.store_id)
        self.assertEqual(found.k.store_id, self.a1.store_id)
        self.assertFalse(getattr(found, "_new_insert", False))

    def test_a_reused_list_gives_the_rows_of_fresh_dicts(self):
        data = payloads()
        self.get(self.a2, data)
        reused = self.get(self.a1, data)
        fresh = self.get(self.a1, payloads())

        self.assertEqual(rows(reused), rows(fresh))
        self.assertEqual(
            [t.k.store_id for t in reused], [self.a1.store_id] * len(WEIGHTS)
        )


if __name__ == "__main__":
    unittest.main()
