"""
Every shard of a store written the way production writes it passes SQLite's own ``PRAGMA
foreign_key_check`` with no row.

Nothing in production turns foreign-key enforcement on (``PRAGMA foreign_keys`` reads 0), so a
declared foreign key is documentation, and a wrong one is a false statement nothing checks.
``foreign_key_check`` works whether or not enforcement is on, so this test changes nothing about
production's connections. It catches a member's column declared into its owner's table but holding a
serial of another table, given rows the wrong key does not satisfy by coincidence (below). Here the
member is ``Sample_members.tessera_serial``, declared into ``Tessera``; the wrong key would name
``Sample``.

What is checked, and on which stores:

  * ``TestFullStore`` -- ``real_store_fixtures.build_full_store`` on the test's own ``sharded`` rows,
    which are the fixture's rows plus one ``Sample`` and its ``Sample_members`` row, whose
    ``tessera_serial`` is a ``Tessera`` serial on its shard and **not** a ``Sample`` serial there.
    The fixture's own ``Sample_members`` rows have ``tessera_serial`` equal to a ``Sample`` serial
    on the same shard (shard 0: 1 and 2, shard 1: 4), so the wrong key passes on them by
    coincidence; the added row is what makes this test fail on a tree with the wrong key. The
    fixture module's default rows are unchanged. The test asserts that property of the row rather
    than assuming it.
  * ``TestStandinStore`` -- a store written through ``ShardedPool`` on the stand-in shards of
    ``standin_pool``: a replicated keypoint and a ``Sample`` (a sharded class) that names it, so
    that the row written by the real ``store()`` resolves its keypoint on the shard it is on. The
    stand-in Sample's ``gadget_serial`` is a placeholder that no ``Gadget`` row backs, so that one
    reference is declared and expected to be reported; the test asserts that it is the *only*
    violation, and that none names ``keypoint``.
  * ``TestTheCheckSeesAViolation`` -- two dangling references, to show the check reports a row
    when there is one (a check that cannot fail proves nothing).

**What this cannot see.** ``foreign_key_check`` sees only a declared foreign key, and a key can be
declared only to a table in the same file. So three references are not checked, because each may
name a row on another shard:

  * ``Sample.anchor_serial`` -- a ``Tessera`` that may be on another shard;
  * ``Weave.anchor_serial`` -- a ``Tessera``, declared to the inventory and not to the schema;
  * ``shard_keys`` -- the primary's table naming a shard for each keypoint serial, which are
    replicated rows of the shards, in another file.

It also cannot see a *right-looking wrong* reference: a key that names a table that does hold the
serial on that shard by coincidence passes (the reason for the added row above).

No Ray: every store is in a temporary directory.
"""

import sqlite3
import tempfile
import unittest
from pathlib import Path
from typing import Dict, List

import ray

import datastorekit.tests.standin_pool as sp
from datastorekit.tests import real_store_fixtures as rsf
from datastorekit.tests.client import build

# a Sample on shard 0 (keypoint 1, aliases 1 and 4), whose one member row names Tessera 3 (shard
# 0: Tesserae 1, 2 and 3; Samples 1 and 2). Its anchor is Tessera 4, on shard 1
ADDED_QUADSOURCE_SERIAL = 10
ADDED_TQ_SERIAL = 3
ADDED_TR_SERIAL = 4


def violations(path: Path) -> List[tuple]:
    """``PRAGMA foreign_key_check`` on ``path``, opened ``mode=ro``: (table, rowid, parent, fk id)
    for each row that violates a declared foreign key."""
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        return conn.execute("PRAGMA foreign_key_check").fetchall()
    finally:
        conn.close()


def all_violations(store: rsf.RealStore) -> Dict[int, List[tuple]]:
    return {serial: violations(path) for serial, path in store.shard_files.items()}


def own_rows(extra_shard0=None):
    """The full store's rows, plus the added ``Sample`` and its member row (and ``extra_shard0``'s
    rows)."""
    replicated, sharded, keys = rsf.full_rows()
    added = {
        "Sample": [
            {
                "serial": ADDED_QUADSOURCE_SERIAL,
                "version": 1,
                "keypoint_serial": 1,
                "gadget_serial": 1,
                "anchor_serial": ADDED_TR_SERIAL,
                "sample_code": "fixture-sample-added",
                "member_count": 1,
                "sample_validated": True,
            }
        ],
        "Sample_members": [
            {
                "sample_serial": ADDED_QUADSOURCE_SERIAL,
                "tessera_serial": ADDED_TQ_SERIAL,
            }
        ],
    }
    sharded[0] = rsf.with_rows(sharded[0], added)
    if extra_shard0 is not None:
        sharded[0] = rsf.with_rows(sharded[0], extra_shard0)
    return replicated, sharded, keys


def serials(rows: rsf.RowSet, table: str) -> List[int]:
    return [row["serial"] for row in rows.get(table, [])]


class _TempDirCase(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)


class TestFullStore(_TempDirCase):
    def build(self, extra_shard0=None) -> rsf.RealStore:
        replicated, sharded, keys = own_rows(extra_shard0)
        return rsf.build_full_store(
            self.root, replicated=replicated, sharded=sharded, shard_keys=keys
        )

    def test_the_added_row_is_not_satisfied_by_coincidence(self):
        """The member row's ``tessera_serial`` is a Tessera serial on its shard and no ``Sample``
        serial there: it is what lets this module fail on the wrong key."""
        _, sharded, _ = own_rows()
        rows = sharded[0]
        self.assertIn(ADDED_TQ_SERIAL, serials(rows, "Tessera"))
        self.assertNotIn(ADDED_TQ_SERIAL, serials(rows, "Sample"))
        # ... whereas the fixture's own rows would satisfy the wrong key by coincidence
        for shard, default in rsf.full_rows()[1].items():
            for row in default["Sample_members"]:
                self.assertIn(row["tessera_serial"], serials(default, "Sample"))
                self.assertIn(row["tessera_serial"], serials(default, "Tessera"))

    def test_the_added_rows_are_in_the_written_shard(self):
        store = self.build()
        conn = sqlite3.connect(f"file:{store.shard_files[0]}?mode=ro", uri=True)
        try:
            self.assertEqual(
                [(ADDED_QUADSOURCE_SERIAL, ADDED_TQ_SERIAL, ADDED_TR_SERIAL)],
                conn.execute(
                    'SELECT "Sample".serial, tessera_serial, anchor_serial FROM "Sample" '
                    'JOIN "Sample_members" ON sample_serial = "Sample".serial '
                    'WHERE "Sample".serial = ?',
                    (ADDED_QUADSOURCE_SERIAL,),
                ).fetchall(),
            )
        finally:
            conn.close()

    def test_every_shard_passes_foreign_key_check(self):
        store = self.build()
        self.assertEqual(2, len(store.shard_files))
        self.assertEqual({0: [], 1: []}, all_violations(store))

    def test_the_default_stores_pass_too(self):
        full = rsf.build_full_store(self.root, stem="default-full")
        self.assertEqual({0: [], 1: []}, all_violations(full))
        real = rsf.build_real_store(self.root, stem="default-real")
        self.assertEqual({0: [], 1: []}, all_violations(real))

    def test_a_relabelled_store_passes(self):
        """``relabel_serials`` follows the schema's declared keys, so the relabelled data is
        consistent with them. (It cannot, by itself, tell a right key from a wrong one.)
        """
        replicated, sharded, keys = own_rows()
        replicated, sharded, keys = rsf.relabel_serials(replicated, sharded, keys)
        store = rsf.build_full_store(
            self.root, replicated=replicated, sharded=sharded, shard_keys=keys
        )
        self.assertEqual({0: [], 1: []}, all_violations(store))


class TestTheCheckSeesAViolation(_TempDirCase):
    def test_a_dangling_tq_is_reported(self):
        """``tessera_serial`` 4 is a Tessera row, but on shard 1: not in this shard's ``Tessera``."""
        replicated, sharded, keys = own_rows()
        for row in sharded[0]["Sample_members"]:
            if row["sample_serial"] == ADDED_QUADSOURCE_SERIAL:
                row["tessera_serial"] = 4
        store = rsf.build_full_store(
            self.root, replicated=replicated, sharded=sharded, shard_keys=keys
        )
        result = all_violations(store)
        self.assertEqual([], result[1])
        self.assertEqual(1, len(result[0]))
        table, _rowid, parent, _fk = result[0][0]
        self.assertEqual(("Sample_members", "Tessera"), (table, parent))

    def test_a_dangling_exit_time_in_the_policy_data_is_reported(self):
        replicated, sharded, keys = own_rows()
        self.assertGreater(len(sharded[0]["Tessera"]), 0)
        sharded[0]["Tessera"][0]["alias_serial"] = 999
        store = rsf.build_full_store(
            self.root, replicated=replicated, sharded=sharded, shard_keys=keys
        )
        result = all_violations(store)
        self.assertEqual([], result[1])
        self.assertEqual(1, len(result[0]))
        table, _rowid, parent, _fk = result[0][0]
        self.assertEqual(("Tessera", "keypoint_alias"), (table, parent))


class TestStandinStore(_TempDirCase):
    def test_a_store_written_by_the_real_write_path_passes(self):
        cluster = sp.StandinCluster()
        with cluster.active():
            primary = self.root / "standin" / "store.sqlite"
            pool = cluster.open_pool(primary)
            try:
                cluster.controller = list(pool._shards.keys())[1]
                atol = build.get_gauge(pool, 10)
                rtol = build.get_gauge(pool, 9)
                k = build.get_keypoint(pool, 0.5)
                exit_time = build.resolve(pool.object_store(build.make_alias(k, 1.5)))
                policy = build.get_rule(pool, "standin-rule", 1.5, "prefer-direct")
                stored = build.resolve(
                    pool.object_store(build.make_sample_on(exit_time, gadget_serial=1))
                )
                shard_files = {
                    sid: Path(pool._shard_db_files[sid]) for sid in pool._shards.keys()
                }
                holder_shard = pool._shard_keys[exit_time.keypoint.store_id]
            finally:
                cluster.close_pool()

        self.assertGreaterEqual(len(shard_files), 2)
        for sid, path in shard_files.items():
            with self.subTest(shard=sid):
                found = violations(path)
                # the stand-in Gadget is the one reference no row backs (module docstring)
                self.assertEqual(
                    [], [row for row in found if row[2] != "Gadget"], found
                )
                # (the last field of a row is the foreign key's index in the table, which moves
                # when a key is added, so it is not compared)
                self.assertEqual(
                    ([] if sid != holder_shard else [("Sample", 1, "Gadget")]),
                    [row[:3] for row in found],
                )

        # the Sample is on one shard only, and the keypoint it names is on every shard
        holders = []
        for sid, path in shard_files.items():
            conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
            try:
                policy_rows = conn.execute(
                    'SELECT keypoint_serial FROM "Sample"'
                ).fetchall()
                exit_rows = conn.execute('SELECT serial FROM "keypoint"').fetchall()
            finally:
                conn.close()
            self.assertEqual([(exit_time.keypoint.store_id,)], exit_rows)
            if policy_rows:
                holders.append(sid)
                self.assertEqual([(exit_time.keypoint.store_id,)], policy_rows)
        self.assertEqual(1, len(holders))
        self.assertIsNotNone(stored.store_id)


def tearDownModule():
    if ray.is_initialized():
        raise RuntimeError(
            "test_foreign_key_check: ray was initialised by this module's tests, which must not "
            "happen (README §5 rule 9)"
        )
