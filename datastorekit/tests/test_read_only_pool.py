"""
A read-only pool, ``ShardedPool(read_only=True)`` (prompts/a3-v2-readiness, prompt 03, O1–O2).

The real ``ShardedPool``, ``Datastore`` actor code, factories and broker run on stand-in shards
(``Datastore.tests.standin_pool``) in temporary directories, with no Ray and nothing under
``var/``. The store is the neutral client's full store, and the lookup sequence is a reader's on
the neutral client: both are **imported** from ``datastorekit.tests.client.reader``
(``build_full_store``, ``reader_sequence``, ``other_sharded_lookups``), which stands in for the
audit probe the source repository's test imported, and keeps that probe's instrument. Importing it
runs nothing.

The instrument is the SHA-256 of every file in the store's directory
(``standin_pool.store_checksums``), which also sees a file appear or go. Beside it, an engine
listener records every SQL statement any engine issues, so that "before any INSERT" is observed
and not inferred; and the connection test records what every connection is opened with.

1. Nothing written on a full store: the instrument counts first, on a read-write pool (the
   primary changes), and then QSI's whole sequence on a read-only pool changes no file, enters
   ``_replicated_write`` never, and returns the hits R2 Run 1 recorded.
2. Each insert-on-miss raises ``ReadOnlyMiss`` naming class and payload, with no INSERT issued and
   no file changed: ``store_tag``, ``dial_setting``, ``knob_setting``, ``gauge_setting``,
   ``routing_rule``.
3. Each other write raises ``ReadOnlyWrite``: ``object_store``, ``object_validate``, a new shard
   key, a vectorized get that reaches an inserter, ``drop_tables``, ``prune_unvalidated=True``,
   and the backstop (a hit that writes a flag, refused by the ``mode=ro`` file).
4. At open: a missing primary; an empty and a hot journal beside a shard; a primary holding a
   record (a ``get`` and a ``prune``); an absent version label; diverged shards; a shard lacking a
   validating class's table, and one lacking a non-validating class's, each refused with
   ``StoreSchemaMismatch`` naming the table (prompts/datastore-generic, prompt 05: only a
   read-write open recovers a table a shard lacks); every connection ``mode=ro``.
5. No Ray is initialised.
"""

import contextlib
import hashlib
import io
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import ray
import sqlalchemy as sqla

from datastorekit.SQL.schema import StoreSchemaMismatch
from datastorekit.tests import standin_pool as sp
from datastorekit.tests.client import build
from datastorekit.tests.client import objects
from datastorekit.tests.client import reader as rw
from datastorekit.tests.client.registry import factories
from datastorekit.tests.client.reader import DEFAULT_GAUGE
from datastorekit.tests.client.registry import (
    read_table_config,
    replicated_tables,
    sharded_tables,
    shard_key_type,
    shard_key_store_id,
)

# the pool module's names, as a reader imports them (O2: importable from the pool's module)
ShardedPool = sp.sp_mod.ShardedPool
ReadOnlyMiss = sp.sp_mod.ReadOnlyMiss
ReadOnlyWrite = sp.sp_mod.ReadOnlyWrite
ReplicatedDivergence = sp.sp_mod.ReplicatedDivergence

# a child that dies inside a write transaction on a shard after its page cache has spilled,
# leaving a hot journal: transcribed from docs/a3-v2-readiness/readonly_open_probe.py (M2d)
HOT_JOURNAL_CHILD = r"""
import os, sqlite3, sys
conn = sqlite3.connect(sys.argv[1], isolation_level=None)
conn.execute("PRAGMA cache_size=2")
conn.execute("BEGIN IMMEDIATE")
conn.execute("CREATE TABLE probe_spill (x BLOB)")
for i in range(400):
    conn.execute("INSERT INTO probe_spill VALUES (randomblob(4000))")
conn.execute("UPDATE gauge_setting SET gauge_exponent = gauge_exponent")
os._exit(0)
"""

_WRITE_VERBS = ("INSERT", "UPDATE", "DELETE", "REPLACE", "CREATE", "DROP", "ALTER")

_MODULE = {}

# the text of every exception a test below raises on purpose, by case (for the prompt's log)
MESSAGES = {}


def setUpModule():
    tmp = tempfile.TemporaryDirectory()
    _MODULE["tmp"] = tmp
    full = Path(tmp.name) / "full"
    cluster = sp.StandinCluster()
    with cluster.active():
        _MODULE["facts"] = rw.build_full_store(full / "store.sqlite", cluster)
    rw.FACTS.update(_MODULE["facts"])
    _MODULE["full"] = full


def tearDownModule():
    _MODULE["tmp"].cleanup()
    if ray.is_initialized():
        raise AssertionError("Ray was initialised by test_read_only_pool")


@contextlib.contextmanager
def quiet():
    with (
        contextlib.redirect_stdout(io.StringIO()),
        contextlib.redirect_stderr(io.StringIO()),
    ):
        yield


@contextlib.contextmanager
def statements():
    """Every SQL statement any SQLAlchemy engine issues inside the block, as (url, statement)."""
    seen = []

    def before(conn, cursor, statement, parameters, context, executemany):
        seen.append((str(conn.engine.url), statement))

    sqla.event.listen(sqla.engine.Engine, "before_cursor_execute", before)
    try:
        yield seen
    finally:
        sqla.event.remove(sqla.engine.Engine, "before_cursor_execute", before)


def writes_in(seen):
    return [s for _, s in seen if s.lstrip().split(" ", 1)[0].upper() in _WRITE_VERBS]


def execute(path: Path, *statements_):
    conn = sqlite3.connect(path)
    try:
        for statement in statements_:
            conn.execute(statement)
        conn.commit()
    finally:
        conn.close()


def sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class _ReadOnlyTestCase(unittest.TestCase):
    """A fresh copy of the full store per test, and the stand-in cluster active."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self._copies = 0

        self.cluster = sp.StandinCluster()
        active = self.cluster.active()
        active.__enter__()
        self.addCleanup(active.__exit__, None, None, None)
        self.facts = _MODULE["facts"]
        self._open = []
        self.addCleanup(self._close_all)

    def tearDown(self):
        self.assertFalse(ray.is_initialized())

    def _close_all(self):
        for pool in self._open:
            with quiet():
                pool.__exit__(None, None, None)
        self._open = []

    def copy(self) -> Path:
        """A copy of the full store, alone in its own directory; its primary."""
        self._copies += 1
        d = self.root / f"copy-{self._copies}"
        shutil.copytree(_MODULE["full"], d)
        return d / "store.sqlite"

    def shards(self, primary: Path):
        return sorted(Path(primary).parent.glob("store-shard*.sqlite"))

    def open(self, primary: Path, label: str = "standin", **kwargs):
        """Open ``primary``; return (pool, what the constructor printed)."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            pool = ShardedPool(
                version_label=label,
                db_name=primary,
                ShardKeyType=shard_key_type,
                ShardKeyStoreIdGetter=shard_key_store_id,
                replicated_tables=replicated_tables,
                sharded_tables=sharded_tables,
                shards=3,
                read_table_config=read_table_config,
                factories=factories,
                **kwargs,
            )
        self.cluster.pool = pool
        self._open.append(pool)
        return pool, out.getvalue()

    def close(self, pool):
        with quiet():
            pool.__exit__(None, None, None)
        self._open.remove(pool)

    def run_sequence(self, pool, directory: Path, others: bool = True):
        """QSI's whole sequence (the probe's), then the other readers' sharded lookups. Returns
        (the recorder's rows, the _replicated_write log, what stopped the sequence)."""
        log = rw.ReplicatedWriteLog()
        rec = rw.Recorder(directory, log)
        stopped = None
        with log.active():
            try:
                with quiet():
                    rw.reader_sequence(pool, rec)
            except RuntimeError as e:
                stopped = e
            if others:
                with quiet():
                    rw.other_sharded_lookups(pool, rec)
        return rec.rows, log.entries, stopped


# ------------------------------------------------------------------------------------------------
# 1. nothing written, on a full store; the instrument first
# ------------------------------------------------------------------------------------------------


class TestNothingWrittenOnAFullStore(_ReadOnlyTestCase):
    def test_the_instrument_counts_a_read_write_pool_then_read_only_writes_nothing(
        self,
    ):
        # the instrument, first (A2): the same sequence on a read-write pool changes the primary,
        # through its in-flight commits, and enters _replicated_write 18 times (audit R2 Run 1)
        rw_primary = self.copy()
        before = sp.store_checksums(rw_primary)
        pool, _ = self.open(rw_primary)
        rw_rows, rw_log, rw_stopped = self.run_sequence(pool, rw_primary.parent)
        self.close(pool)
        after = sp.store_checksums(rw_primary)
        changed = sorted(n for n in before if before[n] != after.get(n))
        self.assertEqual(changed, ["store.sqlite"])
        self.assertEqual(len(rw_log), 18)
        self.assertIs(type(rw_stopped), RuntimeError)

        # the read-only pool: every file byte-identical, open to close
        ro_primary = self.copy()
        before = sp.store_checksums(ro_primary)
        with statements() as seen:
            pool, printed = self.open(ro_primary, read_only=True)
            ro_rows, ro_log, ro_stopped = self.run_sequence(pool, ro_primary.parent)
            self.close(pool)
        self.assertEqual(sp.store_checksums(ro_primary), before)
        self.assertEqual(ro_log, [])
        self.assertEqual(writes_in(seen), [])
        self.assertIn("read-only", printed)

        # every step changed no file, and each step's outcome is the read-write run's
        for name, delta, writes, outcome in ro_rows:
            self.assertEqual(delta, {}, name)
            self.assertEqual(writes, [], name)
        self.assertEqual(
            [(name, outcome) for name, _, _, outcome in ro_rows],
            [(name, outcome) for name, _, _, outcome in rw_rows],
        )

        # the hits audit R2 Run 1 recorded, and the stop at knob_setting's background. The
        # serials are the store's (stand-in serials vary between builds; R2 recorded 1 and 1, 6)
        outcomes = dict((name, outcome) for name, _, _, outcome in ro_rows)
        self.assertEqual(
            outcomes["[dial] Gadget"],
            f"ok [available=True, serial={self.facts['Gadget']}]",
        )
        self.assertEqual(
            outcomes["[dial] read_table keypoint x2"],
            "ok [1 marked, 2 unmarked]",
        )
        self.assertEqual(
            outcomes["[dial] keypoint_alias x3"],
            "ok [3 of 3 available]",
        )
        self.assertEqual(
            outcomes["[dial] read_table dial_setting"],
            "ok [2 row(s)]",
        )
        self.assertEqual(
            outcomes["[dial] routing_rule x2"],
            "ok [serials {}, {}]".format(*self.facts["routing_rule"]),
        )
        self.assertEqual(
            outcomes["[dial] work item: Sample, the stored row"],
            "ok [available=True]",
        )
        self.assertIn(
            "Could not locate suitable gadget",
            outcomes["[knob] Gadget"],
        )
        # stopped by the script's own RuntimeError, not by a ReadOnlyMiss (also a RuntimeError)
        self.assertIs(type(ro_stopped), RuntimeError)
        self.assertEqual(str(ro_stopped), str(rw_stopped))

    def test_a_replicated_get_is_one_call_to_the_drawn_shard(self):
        primary = self.copy()
        pool, _ = self.open(primary, read_only=True)
        for shard_id in (0, 1, 2):
            with self.subTest(shard=shard_id):
                self.cluster.controller = shard_id
                n = len(self.cluster.calls)
                tol = build.get_gauge(pool, DEFAULT_GAUGE)
                calls = self.cluster.calls[n:]
                self.assertEqual(
                    [(c["shard"], c["method"], c["class"]) for c in calls],
                    [(shard_id, "object_get", "gauge_setting")],
                )
                self.assertIsNone(calls[0]["insert_timestamp"])
                self.assertEqual(
                    tol.store_id, self.facts["gauge_setting"][DEFAULT_GAUGE]
                )


# ------------------------------------------------------------------------------------------------
# 2. each insert-on-miss raises ReadOnlyMiss
# ------------------------------------------------------------------------------------------------


class TestEachMissRaisesReadOnlyMiss(_ReadOnlyTestCase):
    def assert_miss(self, primary, run, cls_name, check_payload):
        before = sp.store_checksums(primary)
        with statements() as seen:
            pool, _ = self.open(primary, read_only=True)
            with self.assertRaises(ReadOnlyMiss) as ctx:
                run(pool)
            self.close(pool)
        e = ctx.exception
        self.assertEqual(e.class_name, cls_name)
        check_payload(e.payload)
        self.assertIn(f'a lookup of "{cls_name}" matched no row', str(e))
        self.assertIn("Nothing was written", str(e))
        self.assertEqual(writes_in(seen), [])
        self.assertEqual(sp.store_checksums(primary), before)
        return e

    def sequence(self, pool):
        # not run_sequence, which stops at the RuntimeError the script raises for a model with no
        # background: ReadOnlyMiss is a RuntimeError too, and must reach the test
        rec = rw.Recorder(Path(pool.primary).parent, rw.ReplicatedWriteLog())
        with quiet():
            rw.reader_sequence(pool, rec)

    def test_store_tag(self):
        # with the run's store_tag deleted, resolve_run_selection finds no run and makes no
        # store_tag lookup (audit R2 Run 2); the lookup is made directly, as it would be
        from datastorekit.tests.client.reader import run_label_tag

        primary = self.copy()
        label = run_label_tag("not-in-this-store")
        e = self.assert_miss(
            primary,
            lambda pool: ray.get(pool.object_get("store_tag", label=label)),
            "store_tag",
            lambda payload: self.assertEqual(payload, {"label": label}),
        )
        MESSAGES["store_tag"] = str(e)

    def test_dial_setting(self):
        primary = self.copy()
        for path in self.shards(primary):
            execute(path, "DELETE FROM dial_setting")
        e = self.assert_miss(
            primary,
            self.sequence,
            "dial_setting",
            lambda payload: self.assertEqual(payload["dial_level"], rw.DIAL_FRAME[0]),
        )
        MESSAGES["dial_setting"] = str(e)

    def test_knob_setting(self):
        primary = self.copy()
        for path in self.shards(primary):
            execute(path, "DELETE FROM knob_setting")
        e = self.assert_miss(
            primary,
            self.sequence,
            "knob_setting",
            lambda payload: (
                self.assertEqual(payload["knob_turns"], rw.KNOB_FRAME[0]),
                self.assertAlmostEqual(payload["stepping"], rw.KNOB_FRAME[1]),
            ),
        )
        MESSAGES["knob_setting"] = str(e)

    def test_gauge_setting(self):
        primary = self.copy()
        exponent = DEFAULT_GAUGE
        for path in self.shards(primary):
            execute(
                path, f"DELETE FROM gauge_setting WHERE gauge_exponent = {exponent!r}"
            )
        e = self.assert_miss(
            primary,
            self.sequence,
            "gauge_setting",
            lambda payload: self.assertAlmostEqual(payload["gauge_exponent"], exponent),
        )
        MESSAGES["gauge_setting"] = str(e)

    def test_routing_rule(self):
        primary = self.copy()
        serial = self.facts["routing_rule"][1]
        for path in self.shards(primary):
            execute(path, f"DELETE FROM routing_rule WHERE serial = {serial}")
        e = self.assert_miss(
            primary,
            self.sequence,
            "routing_rule",
            lambda payload: self.assertEqual(
                payload["rule_label"], rw.RULE_HIGH["label"]
            ),
        )
        MESSAGES["routing_rule"] = str(e)


# ------------------------------------------------------------------------------------------------
# 3. every other write raises ReadOnlyWrite
# ------------------------------------------------------------------------------------------------


class TestOtherWritesRaiseReadOnlyWrite(_ReadOnlyTestCase):
    def dial_frame(self, pool):
        with quiet():
            return ray.get(
                pool.object_get(
                    "dial_setting", level=rw.DIAL_FRAME[0], stepping=rw.DIAL_FRAME[1]
                )
            )

    def exit_time(self, pool):
        from datastorekit.tests.client.objects import keypoint_alias

        from datastorekit.tests.client.reader import ALIAS_GAUGES

        k = ray.get(pool.read_table("keypoint", marked=True))[0]
        # the alias names its keypoint alone: the frame and the two gauges are got, as hits, and
        # not passed
        frame = self.dial_frame(pool)
        atol = build.get_gauge(pool, ALIAS_GAUGES[0])
        rtol = build.get_gauge(pool, ALIAS_GAUGES[1])
        return ray.get(
            pool.object_get(
                keypoint_alias,
                keypoint=k,
                offset=build.ALIAS_OFFSET,
                stepping=build.ALIAS_STEPPING,
            )
        )

    def assert_refused(self, primary, attempt, expect_class=None):
        before = sp.store_checksums(primary)
        pool, _ = self.open(primary, read_only=True)
        with statements() as seen:
            n = len(self.cluster.calls)
            with self.assertRaises(ReadOnlyWrite) as ctx:
                attempt(pool)
            calls = self.cluster.calls[n:]
        self.close(pool)
        self.assertEqual(writes_in(seen), [])
        self.assertEqual(sp.store_checksums(primary), before)
        if expect_class is not None:
            self.assertEqual(ctx.exception.class_name, expect_class)
        self.assertIn("Nothing was written", str(ctx.exception))
        return ctx.exception, calls

    def test_object_store_sharded_and_replicated(self):
        primary = self.copy()
        pool, _ = self.open(primary, read_only=True)
        exit_time = self.exit_time(pool)
        frame = self.dial_frame(pool)
        self.close(pool)

        e, calls = self.assert_refused(
            primary,
            lambda p: p.object_store(build.make_sample_on(exit_time)),
            "Sample",
        )
        self.assertEqual(calls, [])
        MESSAGES["object_store"] = str(e)

        from datastorekit.tests.client.reader import ALIAS_GAUGES

        tol = objects.SerialHandle(self.facts["gauge_setting"][ALIAS_GAUGES[0]])
        _, calls = self.assert_refused(
            primary,
            lambda p: p.object_store([build.make_alias(exit_time.keypoint, 3.0e7)]),
            "keypoint_alias",
        )
        self.assertEqual(calls, [])

    def test_object_validate(self):
        primary = self.copy()
        pool, _ = self.open(primary, read_only=True)
        from datastorekit.tests.client.objects import Gadget

        model = ray.get(
            pool.object_get(
                Gadget,
                label=rw.FRAMES[0][1],
                frame=self.dial_frame(pool),
                tags=build.get_tags(pool, rw.run_label_tag(rw.RUN)),
            )
        )
        self.assertTrue(model.available)
        self.close(pool)
        e, calls = self.assert_refused(
            primary, lambda p: p.object_validate(model), "Gadget"
        )
        self.assertEqual(calls, [])
        MESSAGES["object_validate"] = str(e)

    def test_the_actors_refuse_store_and_validate_themselves(self):
        primary = self.copy()
        pool, _ = self.open(primary, read_only=True)
        exit_time = self.exit_time(pool)
        actor = pool._shards[0].obj
        with self.assertRaises(ReadOnlyWrite) as ctx:
            actor.object_store(build.make_sample_on(exit_time))
        self.assertEqual(ctx.exception.store, "shard0000-store")
        with self.assertRaises(ReadOnlyWrite):
            actor.object_validate(exit_time)

    def test_a_new_shard_key(self):
        # a keypoint on every shard with no row in the primary's shard_keys: written by a
        # read-write pool, then its key deleted while the store is closed (the check at open
        # compares keys against keypoints, not keypoints against keys)
        primary = self.copy()
        pool, _ = self.open(primary)
        with quiet():
            k = ray.get(
                pool.object_get(
                    "keypoint",
                    position=3.0e8,
                    marked=True,
                    flagged=True,
                )
            )
        self.close(pool)
        execute(primary, f"DELETE FROM shard_keys WHERE key_serial = {k.store_id}")

        e, calls = self.assert_refused(
            primary,
            lambda p: ray.get(
                p.object_get(
                    "keypoint",
                    position=3.0e8,
                    marked=True,
                    flagged=True,
                )
            ),
            "keypoint",
        )
        self.assertEqual(
            [(c["method"], c["class"]) for c in calls], [("object_get", "keypoint")]
        )
        self.assertIn("assigning a shard key", str(e))
        MESSAGES["shard key"] = str(e)

    def test_a_vectorized_get_that_reaches_an_inserter(self):
        primary = self.copy()
        pool, _ = self.open(primary, read_only=True)
        exit_time = self.exit_time(pool)
        self.close(pool)
        e, _ = self.assert_refused(
            primary,
            lambda p: ray.get(
                p.object_get_vectorized(
                    "Tessera",
                    {"k": exit_time},
                    payload_data=[
                        {
                            "weight": 0.875,
                        }
                    ],
                )
            ),
            "Tessera",
        )
        self.assertIn("an insert", str(e))
        MESSAGES["vectorized"] = str(e)

    def test_drop_actions_and_prune_refuse_before_anything_is_opened(self):
        # on a path where no store exists: the refusal is ReadOnlyWrite, not the missing
        # primary's, so it came first; nothing was created
        missing = self.root / "nowhere" / "store.sqlite"
        for kwargs, what in (
            ({"drop_tables": ["Sample"]}, "drop_tables"),
            ({"prune_unvalidated": True}, "prune_unvalidated=True"),
        ):
            with self.subTest(what=what):
                with self.assertRaises(ReadOnlyWrite) as ctx:
                    self.open(missing, read_only=True, **kwargs)
                self.assertIn(what, str(ctx.exception))
                self.assertFalse(missing.parent.exists())
                self.assertEqual(self.cluster.calls, [])
                MESSAGES[what] = str(ctx.exception)

        # and on an existing store, every file unchanged
        primary = self.copy()
        before = sp.store_checksums(primary)
        for kwargs in (
            {"drop_tables": ["Sample"]},
            {"prune_unvalidated": True},
        ):
            with self.assertRaises(ReadOnlyWrite):
                self.open(primary, read_only=True, **kwargs)
        self.assertEqual(sp.store_checksums(primary), before)
        self.assertEqual(self.cluster.calls, [])

    def test_the_backstop_a_flag_update_on_a_hit(self):
        # the store's position = 0.5 is a marked keypoint only; asking for it as a flagged keypoint
        # too makes the factory update its flag on a hit (audit R1). The UPDATE reaches SQLite,
        # and the mode=ro file refuses it
        primary = self.copy()
        before = sp.store_checksums(primary)
        pool, _ = self.open(primary, read_only=True)
        payload = {"position": 0.5, "marked": True, "flagged": True}
        with statements() as seen, quiet():
            with self.assertRaises(ReadOnlyWrite) as ctx:
                ray.get(pool.object_get("keypoint", **payload))
        e = ctx.exception
        self.assertEqual(e.class_name, "keypoint")
        self.assertIn("SQLite refused the write", str(e))
        self.assertIn("attempt to write a readonly database", str(e))
        self.assertTrue(e.store.startswith("shard000"))
        self.assertEqual(
            [s.split(" ", 1)[0] for s in writes_in(seen)], ["UPDATE"]
        )  # it did reach SQLite

        # chained, naming the actor: the actor object called directly keeps the cause
        actor = pool._shards[2].obj
        with quiet():
            with self.assertRaises(ReadOnlyWrite) as ctx:
                actor.object_get("keypoint", **payload)
        self.assertEqual(ctx.exception.store, "shard0002-store")
        self.assertIsInstance(ctx.exception.__cause__, sqla.exc.OperationalError)
        self.assertEqual(
            ctx.exception.__cause__.orig.sqlite_errorcode, sqlite3.SQLITE_READONLY
        )
        self.close(pool)
        self.assertEqual(sp.store_checksums(primary), before)
        MESSAGES["backstop"] = str(e)


# ------------------------------------------------------------------------------------------------
# 4. at open
# ------------------------------------------------------------------------------------------------


class TestAtOpen(_ReadOnlyTestCase):
    def test_a_missing_primary_creates_nothing(self):
        missing = self.root / "nowhere" / "deeper" / "store.sqlite"
        with self.assertRaises(RuntimeError) as ctx:
            self.open(missing, read_only=True)
        self.assertIn("does not exist", str(ctx.exception))
        self.assertFalse((self.root / "nowhere").exists())
        self.assertEqual(self.cluster.calls, [])
        MESSAGES["missing primary"] = str(ctx.exception)

        # the instrument: a read-write pool on the same path creates the store
        pool, _ = self.open(missing)
        self.assertTrue(missing.exists())
        self.close(pool)

    def test_an_empty_journal_beside_a_shard_is_refused(self):
        primary = self.copy()
        journal = primary.with_name("store-shard0001.sqlite-journal")
        journal.write_bytes(b"")
        before = sp.store_checksums(primary)
        with self.assertRaises(RuntimeError) as ctx:
            self.open(primary, read_only=True)
        self.assertIn(str(journal), str(ctx.exception))
        self.assertEqual(sp.store_checksums(primary), before)
        self.assertEqual(self.cluster.calls, [])
        MESSAGES["empty journal"] = str(ctx.exception)

    def test_an_empty_journal_beside_the_primary_is_refused(self):
        primary = self.copy()
        for suffix in ("-journal", "-wal", "-shm"):
            with self.subTest(suffix=suffix):
                journal = primary.with_name(primary.name + suffix)
                journal.write_bytes(b"")
                before = sp.store_checksums(primary)
                with self.assertRaises(RuntimeError) as ctx:
                    self.open(primary, read_only=True)
                self.assertIn(str(journal), str(ctx.exception))
                self.assertEqual(sp.store_checksums(primary), before)
                self.assertEqual(self.cluster.calls, [])
                journal.unlink()

    def test_a_hot_journal_beside_a_shard_is_refused_and_not_rolled_back(self):
        primary = self.copy()
        shard1 = primary.with_name("store-shard0001.sqlite")
        child = subprocess.run(
            [sys.executable, "-c", HOT_JOURNAL_CHILD, str(shard1)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(child.returncode, 0, child.stderr)
        journal = shard1.with_name(shard1.name + "-journal")
        self.assertTrue(journal.exists())
        self.assertGreater(journal.stat().st_size, 0)

        # the instrument: a read-write open of a copy rolls the journal back, which the SHA-256
        # sees (and the journal goes)
        witness = self.root / "hot-witness"
        shutil.copytree(primary.parent, witness)
        w_shard, w_journal = witness / shard1.name, witness / journal.name
        w_before = sha(w_shard)
        conn = sqlite3.connect(str(w_shard))
        conn.execute("SELECT count(*) FROM sqlite_master").fetchone()
        conn.close()
        self.assertNotEqual(sha(w_shard), w_before)
        self.assertFalse(w_journal.exists())

        before = sp.store_checksums(primary)
        shard_sha, journal_sha = sha(shard1), sha(journal)
        with self.assertRaises(RuntimeError) as ctx:
            self.open(primary, read_only=True)
        self.assertIn(str(journal), str(ctx.exception))
        self.assertEqual(sha(shard1), shard_sha)
        self.assertEqual(sha(journal), journal_sha)
        self.assertEqual(sp.store_checksums(primary), before)
        MESSAGES["hot journal"] = str(ctx.exception)

    def _record(self, primary, operation, cls_name, controller):
        execute(
            primary,
            "INSERT INTO replication_in_flight (operation, class_name, controller_shard, "
            f"store_id, started) VALUES ('{operation}', '{cls_name}', "
            f"{'NULL' if controller is None else controller}, NULL, '2026-10-03 09:00:00')",
        )

    def test_a_record_of_any_operation_is_refused_by_name_and_not_cleared(self):
        for operation, cls_name, controller in (
            ("get", "gauge_setting", 1),
            ("prune", "Gadget", None),
        ):
            with self.subTest(operation=operation):
                primary = self.copy()
                self._record(primary, operation, cls_name, controller)
                before = sp.store_checksums(primary)
                with (
                    mock.patch.object(
                        ShardedPool,
                        "_complete_interrupted_prune",
                        side_effect=AssertionError("completed"),
                    ) as complete,
                    mock.patch.object(
                        ShardedPool,
                        "_reconcile_replicated_tables",
                        side_effect=AssertionError("reconciled"),
                    ) as reconcile,
                ):
                    with self.assertRaises(ReadOnlyWrite) as ctx:
                        self.open(primary, read_only=True)
                text = str(ctx.exception)
                self.assertIn(f'operation="{operation}"', text)
                self.assertIn(f'class="{cls_name}"', text)
                self.assertIn("The record was not cleared", text)
                complete.assert_not_called()
                reconcile.assert_not_called()
                self.assertEqual(sp.store_checksums(primary), before)
                self.assertEqual(
                    sp._read(
                        primary,
                        "SELECT operation, class_name FROM replication_in_flight",
                    ),
                    [(operation, cls_name)],
                )
                self.assertEqual(self.cluster.calls, [])
                MESSAGES[f"record {operation}"] = text

    def test_an_absent_version_label_is_refused_naming_the_labels_present(self):
        primary = self.copy()
        before = sp.store_checksums(primary)
        with self.assertRaises(ReadOnlyMiss) as ctx:
            self.open(primary, label="2025.1.1", read_only=True)
        e = ctx.exception
        self.assertEqual(e.class_name, "version")
        self.assertEqual(e.payload, {"label": "2025.1.1"})
        self.assertIn("['standin']", str(e))
        self.assertEqual(sp.store_checksums(primary), before)
        self.assertEqual(self.cluster.calls, [])
        MESSAGES["version"] = str(e)

    def test_diverged_shards_are_refused_and_nothing_repaired(self):
        primary = self.copy()
        serial = self.facts["gauge_setting"][DEFAULT_GAUGE]
        execute(
            primary.with_name("store-shard0002.sqlite"),
            f"DELETE FROM gauge_setting WHERE serial = {serial}",
        )
        before = sp.store_checksums(primary)
        with self.assertRaises(ReplicatedDivergence) as ctx:
            self.open(primary, read_only=True)
        self.assertIn('class "gauge_setting"', str(ctx.exception))
        self.assertEqual(sp.store_checksums(primary), before)

    def test_a_shard_lacking_a_table_is_refused_naming_it(self):
        """A shard that lacks a table (what an interrupted drop leaves) is refused by the reader
        the pool opens through, naming the shard and the table, before any actor is built; no
        file changes. Only a read-write open recovers such a store (prompts/datastore-generic,
        README U1)."""
        constructed = []
        original = sp._Options.remote

        def counting(options, *args, **kw):
            constructed.append(options._name)
            return original(options, *args, **kw)

        for cls_name, validates in (("Sample", True), ("Tessera", False)):
            with self.subTest(table=cls_name, validates=validates):
                primary = self.copy()
                shard1 = primary.with_name("store-shard0001.sqlite")
                execute(shard1, f'DROP TABLE "{cls_name}"')
                before = sp.store_checksums(primary)
                with mock.patch.object(sp._Options, "remote", counting):
                    with self.assertRaises(StoreSchemaMismatch) as ctx:
                        self.open(primary, read_only=True)
                e = ctx.exception
                self.assertEqual(e.differences.absent_tables, (cls_name,))
                self.assertIn(f'shard #1 "{str(shard1.resolve())}"', str(e))
                self.assertIn(f'it lacks the table(s) "{cls_name}"', str(e))
                self.assertEqual([], constructed, "an actor was created")
                self.assertEqual(self.cluster.calls, [])
                self.assertEqual(sp.store_checksums(primary), before)
                MESSAGES[f"absent table {cls_name}"] = str(e)

    def test_every_connection_is_opened_read_only(self):
        # A checksum cannot see a read-write open of a shard with no journal: it writes nothing.
        # So what every connection is opened with is recorded: the sqlite3 connections the pool
        # makes itself, and every SQLAlchemy engine connection
        primary = self.copy()
        sqlite_calls = []
        engine_urls = []
        real_connect = sqlite3.connect

        def recording_connect(*args, **kwargs):
            sqlite_calls.append((args, kwargs))
            return real_connect(*args, **kwargs)

        def on_engine_connect(conn):
            engine_urls.append(str(conn.engine.url))

        sqla.event.listen(sqla.engine.Engine, "engine_connect", on_engine_connect)
        try:
            with mock.patch(
                "datastorekit.SQL.ShardedPool.sqlite3.connect", recording_connect
            ):
                pool, _ = self.open(primary, read_only=True)
                self.run_sequence(pool, primary.parent, others=False)
                self.close(pool)
        finally:
            sqla.event.remove(sqla.engine.Engine, "engine_connect", on_engine_connect)

        self.assertGreater(len(sqlite_calls), 0)
        for args, kwargs in sqlite_calls:
            self.assertTrue(
                str(args[0]).startswith("file:") and str(args[0]).endswith("?mode=ro"),
                args,
            )
            self.assertTrue(kwargs.get("uri", False), kwargs)
        self.assertGreater(len(engine_urls), 0)
        for url in engine_urls:
            self.assertIn("?mode=ro&uri=true", url)
        # every shard and the primary were opened, all of them mode=ro
        opened = {u.split("file:", 1)[1].split("?", 1)[0] for u in engine_urls}
        self.assertEqual(
            opened,
            {str(primary.resolve())} | {str(p.resolve()) for p in self.shards(primary)},
        )


if __name__ == "__main__":
    unittest.main()
