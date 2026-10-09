"""
Version-keyed lookups: the optional ``register()`` key ``key_on_version`` (extraction prompt 06;
README §6.2, U25 and U26).

A factory that declares ``"key_on_version": True`` is handed, in every payload
``Datastore.object_get`` gives its ``build``, the serial of the version row the pool was opened
under, as ``datastorekit.contract.VERSION_SERIAL_KEY``; its ``build`` filters on it through
``datastorekit.contract.require_version_serial``. A row made under one label is then found under
that label only. The neutral client's ``Tessera`` (sharded, versioned) is keyed.

The semantics are carried over from the version-keyed lookup tests of the client project the
feature comes from (``PROVENANCE.md`` names it and its tests), onto the neutral client:

- a keyed row is returned under its own label, is a new row under another, and is its own label's
  again when that label is reopened (1); the same through the vectorized route (2);
- a class that carries a ``version`` column and does not declare the key keeps one row across
  labels (3);
- the caller's payload is not changed (6), and a caller that supplies the reserved key itself is
  refused (7);
- a keyed factory's ``build``, called directly with no serial, raises (10);
- exactly the classes that declare the key are keyed (11), and the key without a ``version``
  column is refused at schema build (12).

The source's three tests of one label on each of three of its classes are (1)'s semantics on one
neutral class here, and its test of its scripts' imports is about that project alone; neither is
carried over. The rest is new: the read-only pool, whose actors hold a lookup serial and no insert
serial (4, 5, 9); the actor's refusal of a keyed lookup before any serial is set (8); a
``key_on_version`` that is not a bool (13); and the contract's two names (14).

The pools are the real ``ShardedPool``, ``Datastore`` actor code, factories and broker on stand-in
shards (``datastorekit.tests.standin_pool``), opened under the labels ``A`` and ``B``. The actor
tests build the undecorated actor class (``standin_pool.DatastoreClass``) directly on a shard file
of a store the pool made, with a stand-in broker handle, since an actor with no broker cannot
lease a serial. Test 6 is at the actor, not through the pool, because the pool's vectorized route
adds the shard key to the caller's payloads before the actor sees them
(``[06-a-vectorized-get-adds-the-shard-key-to-the-callers-payloads]``).

No Ray, and every store in a temporary directory.
"""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import ray
import sqlalchemy as sqla

from datastorekit.SQL.schema import build_schema
from datastorekit.contract import VERSION_SERIAL_KEY, require_version_serial
from datastorekit.tests import standin_pool as sp
from datastorekit.tests.client import build
from datastorekit.tests.client.registry import (
    factories,
    replicated_tables,
    sharded_tables,
    shard_key_type,
    shard_key_store_id,
)

ReadOnlyWrite = sp.sp_mod.ReadOnlyWrite

LABEL_A = "A"
LABEL_B = "B"

# the keypoint and alias every Tessera below is keyed on, and the weights it is got with
POSITION = 1.0
OFFSET = 0.5
WEIGHT = 0.25
WEIGHTS = (0.25, 0.75)
OTHER_WEIGHT = 0.5


def tearDownModule():
    if ray.is_initialized():
        raise AssertionError("Ray was initialised by test_version_keyed_lookups")


@contextlib.contextmanager
def quiet():
    with (
        contextlib.redirect_stdout(io.StringIO()),
        contextlib.redirect_stderr(io.StringIO()),
    ):
        yield


def tessera_rows(files):
    """Every Tessera row of every shard, as (serial, version, alias serial, weight), by serial."""
    rows = []
    for path in files.values():
        rows.extend(
            sp._read(
                path,
                'SELECT serial, version, alias_serial, tessera_weight FROM "Tessera"',
            )
        )
    return sorted(rows)


class _StandinCase(unittest.TestCase):
    """The stand-in cluster active, in a temporary directory."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.primary = self.root / "store" / "store.sqlite"

        self.cluster = sp.StandinCluster()
        active = self.cluster.active()
        active.__enter__()
        self.addCleanup(active.__exit__, None, None, None)
        self._open = []
        self.addCleanup(self._close_all)

    def tearDown(self):
        self.assertFalse(ray.is_initialized())

    def _close_all(self):
        for pool in self._open:
            with quiet():
                pool.__exit__(None, None, None)
        self._open = []

    def open(self, label: str, **kwargs):
        """Open (or create) the store under ``label``, as test_version_row_at_open and
        test_read_only_pool open theirs, and return the pool."""
        with quiet():
            pool = sp.sp_mod.ShardedPool(
                version_label=label,
                db_name=self.primary,
                ShardKeyType=shard_key_type,
                ShardKeyStoreIdGetter=shard_key_store_id,
                replicated_tables=replicated_tables,
                sharded_tables=sharded_tables,
                shards=3,
                factories=factories,
                **kwargs,
            )
        self.cluster.pool = pool
        self._open.append(pool)
        self.files = dict(pool._shard_db_files)
        return pool

    def close(self, pool):
        with quiet():
            pool.__exit__(None, None, None)
        self._open.remove(pool)
        if self.cluster.pool is pool:
            self.cluster.pool = None


# ------------------------------------------------------------------------------------------------
# through the pool
# ------------------------------------------------------------------------------------------------


class TestThroughThePool(_StandinCase):
    def alias(self, pool):
        """The keypoint_alias every Tessera is keyed on: found, or stored on a miss."""
        k = build.get_keypoint(pool, POSITION)
        return build.get_alias(pool, k, OFFSET)

    def get(self, pool, alias, weight=WEIGHT):
        return ray.get(pool.object_get("Tessera", k=alias, weight=weight))

    def test_a_keyed_row_is_returned_only_under_its_own_label(self):
        pool = self.open(LABEL_A)
        serial_a = pool._version.store_id
        alias = self.alias(pool)
        t_a = self.get(pool, alias)
        self.assertTrue(getattr(t_a, "_new_insert", False))
        again = self.get(pool, alias)
        self.assertEqual(again.store_id, t_a.store_id)
        self.assertFalse(getattr(again, "_new_insert", False))
        self.close(pool)

        pool = self.open(LABEL_B)
        serial_b = pool._version.store_id
        self.assertNotEqual(serial_a, serial_b)
        t_b = self.get(pool, self.alias(pool))
        self.assertNotEqual(
            t_b.store_id,
            t_a.store_id,
            f"the Tessera stored under {LABEL_A} was returned under {LABEL_B}",
        )
        self.assertTrue(getattr(t_b, "_new_insert", False))
        self.close(pool)

        pool = self.open(LABEL_A)
        t_a2 = self.get(pool, self.alias(pool))
        self.assertEqual(t_a2.store_id, t_a.store_id)
        self.assertFalse(getattr(t_a2, "_new_insert", False))
        self.close(pool)

        # two rows on disk, one under each label's serial
        self.assertEqual(
            tessera_rows(self.files),
            [
                (t_a.store_id, serial_a, alias.store_id, WEIGHT),
                (t_b.store_id, serial_b, alias.store_id, WEIGHT),
            ],
        )

    def test_the_vectorized_route_is_keyed_too(self):
        pool = self.open(LABEL_A)
        alias = self.alias(pool)
        got_a = build.get_tesserae(pool, alias, WEIGHTS)
        self.assertEqual(len({t.store_id for t in got_a}), len(WEIGHTS))
        again = build.get_tesserae(pool, alias, WEIGHTS)
        self.assertEqual([t.store_id for t in again], [t.store_id for t in got_a])
        self.close(pool)

        pool = self.open(LABEL_B)
        got_b = build.get_tesserae(pool, self.alias(pool), WEIGHTS)
        self.assertEqual(
            {t.store_id for t in got_b} & {t.store_id for t in got_a}, set()
        )
        self.assertEqual(
            [getattr(t, "_new_insert", False) for t in got_b], [True] * len(WEIGHTS)
        )
        self.close(pool)

        pool = self.open(LABEL_A)
        got_a2 = build.get_tesserae(pool, self.alias(pool), WEIGHTS)
        self.assertEqual([t.store_id for t in got_a2], [t.store_id for t in got_a])
        self.close(pool)

    def test_an_unkeyed_versioned_class_keeps_one_row_across_labels(self):
        pool = self.open(LABEL_A)
        serial_a = pool._version.store_id
        self.assertTrue(factories["keypoint_alias"].register()["version"])
        self.assertFalse(
            factories["keypoint_alias"].register().get("key_on_version", False)
        )
        alias_a = self.alias(pool)
        self.close(pool)

        pool = self.open(LABEL_B)
        self.assertNotEqual(pool._version.store_id, serial_a)
        alias_b = self.alias(pool)
        self.assertEqual(alias_b.store_id, alias_a.store_id)
        rows = sp.shard_rows(pool, "keypoint_alias")
        self.close(pool)

        # one row, under the first label's serial, on every shard (the class is replicated)
        for sid, shard in rows.items():
            with self.subTest(shard=sid):
                self.assertEqual(len(shard), 1)
                self.assertEqual(shard[0][0], alias_a.store_id)
        version = sp.table_columns(self.files[0], "keypoint_alias").index("version")
        self.assertEqual({shard[0][version] for shard in rows.values()}, {serial_a})

    def write_under_both_labels(self):
        """A Tessera got under A, and the same payload got under B: (A's, B's) serials."""
        pool = self.open(LABEL_A)
        t_a = self.get(pool, self.alias(pool))
        self.close(pool)
        pool = self.open(LABEL_B)
        t_b = self.get(pool, self.alias(pool))
        self.close(pool)
        return t_a.store_id, t_b.store_id

    def test_a_read_only_pool_finds_the_rows_of_its_own_label(self):
        serial_a, serial_b = self.write_under_both_labels()
        before = sp.store_checksums(self.primary)

        for label, expected in ((LABEL_A, serial_a), (LABEL_B, serial_b)):
            with self.subTest(label=label):
                pool = self.open(label, read_only=True)
                alias = self.alias(pool)
                found = self.get(pool, alias)
                self.assertEqual(found.store_id, expected)
                vectorized = build.get_tesserae(pool, alias, [WEIGHT])
                self.assertEqual([t.store_id for t in vectorized], [expected])
                self.close(pool)

        self.assertEqual(sp.store_checksums(self.primary), before)

    def test_a_read_only_miss_under_another_label_is_refused(self):
        self.write_under_both_labels()
        pool = self.open(LABEL_A)
        only_a = self.get(pool, self.alias(pool), OTHER_WEIGHT)
        self.close(pool)
        rows = tessera_rows(self.files)
        before = sp.store_checksums(self.primary)

        pool = self.open(LABEL_B, read_only=True)
        alias = self.alias(pool)
        with self.assertRaises(ReadOnlyWrite) as ctx:
            self.get(pool, alias, OTHER_WEIGHT)
        self.close(pool)

        self.assertEqual(ctx.exception.class_name, "Tessera")
        self.assertIn("an insert", str(ctx.exception))
        self.assertIn("Nothing was written", str(ctx.exception))
        self.assertEqual(sp.store_checksums(self.primary), before)
        self.assertEqual(tessera_rows(self.files), rows)
        self.assertIn(only_a.store_id, [r[0] for r in rows])


# ------------------------------------------------------------------------------------------------
# at the actor
# ------------------------------------------------------------------------------------------------


class TestTheActor(_StandinCase):
    """Actors built directly on shard 0 of a store the pool made under label A, which holds the
    keypoint and alias and no Tessera."""

    def setUp(self):
        super().setUp()
        pool = self.open(LABEL_A)
        self.serial = pool._version.store_id
        self.alias = build.get_alias(pool, build.get_keypoint(pool, POSITION), OFFSET)
        self.close(pool)
        self.db = self.files[0]
        self.broker = sp.Handle(
            sp.BrokerClass(name="SerialPoolBroker"),
            "SerialPoolBroker",
            self.cluster,
            None,
        )
        self._actors = 0

    def actor(self):
        """An actor on shard 0, as the pool builds one, with no serial set."""
        self._actors += 1
        with quiet():
            actor = sp.DatastoreClass(
                version_label=LABEL_A,
                db_name=self.db,
                replicated_tables=list(replicated_tables),
                factories=factories,
                my_name=f"probe{self._actors:04d}-store",
                serial_broker=self.broker,
            )
        self.addCleanup(self._exit, actor)
        return actor

    def _exit(self, actor):
        with quiet():
            actor.__exit__(None, None, None)

    def payload(self, weight=WEIGHT):
        return {"k": self.alias, "weight": weight}

    def test_the_callers_payload_is_not_mutated(self):
        actor = self.actor()
        actor.set_version(self.serial)
        p = self.payload()
        before = dict(p)
        got = actor.object_get("Tessera", payload_data=[p])
        self.assertEqual(len(got), 1)
        self.assertEqual(p, before)
        self.assertNotIn(VERSION_SERIAL_KEY, p)

    def test_a_caller_supplied_serial_is_refused(self):
        actor = self.actor()
        actor.set_version(self.serial)
        with self.assertRaises(KeyError) as ctx:
            actor.object_get(
                "Tessera", **{**self.payload(), VERSION_SERIAL_KEY: self.serial}
            )
        self.assertIn(VERSION_SERIAL_KEY, str(ctx.exception))
        self.assertEqual(tessera_rows({0: self.db}), [])

    def test_a_keyed_lookup_before_the_serial_is_set_raises(self):
        actor = self.actor()
        before = sp.store_checksums(self.primary)
        with self.assertRaises(RuntimeError) as ctx:
            actor.object_get("Tessera", **self.payload())
        self.assertIn('"Tessera"', str(ctx.exception))
        self.assertIn("set_lookup_version", str(ctx.exception))
        self.assertEqual(sp.store_checksums(self.primary), before)
        self.assertEqual(tessera_rows({0: self.db}), [])

        # a class with no version column is not refused on the same actor
        gauge = actor.object_get("gauge_setting", exponent=5)
        self.assertIsNotNone(gauge.store_id)

    def test_set_lookup_version_keys_lookups_and_admits_no_insert(self):
        # the row is written by an actor that holds the insert serial
        writer = self.actor()
        writer.set_version(self.serial)
        written = writer.object_get("Tessera", **self.payload())
        self.assertTrue(getattr(written, "_new_insert", False))

        reader = self.actor()
        reader.set_lookup_version(self.serial)
        self.assertIsNone(reader._version_serial)
        found = reader.object_get("Tessera", **self.payload())
        self.assertEqual(found.store_id, written.store_id)
        self.assertFalse(getattr(found, "_new_insert", False))

        # a miss reaches the insert, which the insert serial's guard refuses
        rows = tessera_rows({0: self.db})
        with self.assertRaises(RuntimeError) as ctx:
            reader.object_get("Tessera", **self.payload(OTHER_WEIGHT))
        self.assertIn("before the version serial is set", str(ctx.exception))
        self.assertEqual(tessera_rows({0: self.db}), rows)

    def test_a_keyed_build_without_the_serial_raises(self):
        actor = self.actor()
        actor.set_version(self.serial)
        with actor._engine.begin() as conn:
            with self.assertRaises(RuntimeError) as ctx:
                factories["Tessera"].build(
                    payload=self.payload(),
                    conn=conn,
                    table=actor._tables["Tessera"],
                    inserter=actor._inserters["Tessera"],
                    tables=actor._tables,
                    inserters=actor._inserters,
                )
        self.assertIn("Tessera", str(ctx.exception))
        self.assertIn(VERSION_SERIAL_KEY, str(ctx.exception))
        self.assertEqual(tessera_rows({0: self.db}), [])


# ------------------------------------------------------------------------------------------------
# the declaration
# ------------------------------------------------------------------------------------------------


def _factory(**keys):
    """A factory whose register() gives ``keys`` and one column of its own, made afresh on each
    call (a column belongs to one table)."""

    class _Factory:
        @staticmethod
        def register():
            return {**keys, "columns": [sqla.Column("x", sqla.Integer)]}

    return _Factory


class TestTheDeclaration(unittest.TestCase):
    def test_only_tessera_is_keyed(self):
        records = build_schema(sqla.MetaData(), factories).records
        keyed = {
            name
            for name, record in records.items()
            if record.get("key_on_version", False)
        }
        self.assertEqual(keyed, {"Tessera"})
        self.assertIs(records["Tessera"]["key_on_version"], True)

    def test_key_on_version_without_a_version_column_is_refused(self):
        unversioned = _factory(version=False, key_on_version=True)
        with self.assertRaises(ValueError) as ctx:
            build_schema(sqla.MetaData(), {"unversioned": unversioned})
        self.assertIn('"unversioned"', str(ctx.exception))
        self.assertIn("key_on_version", str(ctx.exception))

        # the same registration with a version column is keyed
        built = build_schema(
            sqla.MetaData(),
            {"versioned": _factory(version=True, key_on_version=True)},
        )
        self.assertIs(built.records["versioned"]["key_on_version"], True)

    def test_a_key_on_version_that_is_not_a_bool_is_refused(self):
        loosely_keyed = _factory(version=True, key_on_version="yes")
        with self.assertRaises(ValueError) as ctx:
            build_schema(sqla.MetaData(), {"loosely_keyed": loosely_keyed})
        self.assertIn('"loosely_keyed"', str(ctx.exception))
        self.assertIn("key_on_version", str(ctx.exception))
        self.assertIn("not a bool", str(ctx.exception))


# ------------------------------------------------------------------------------------------------
# the contract
# ------------------------------------------------------------------------------------------------


class TestTheContract(unittest.TestCase):
    def test_require_version_serial(self):
        self.assertEqual(VERSION_SERIAL_KEY, "_version_serial")
        self.assertEqual(
            require_version_serial({"weight": 1.0, VERSION_SERIAL_KEY: 7}, "keyed"), 7
        )
        for payload in ({"weight": 1.0}, {"weight": 1.0, VERSION_SERIAL_KEY: None}):
            with self.subTest(payload=payload):
                with self.assertRaises(RuntimeError) as ctx:
                    require_version_serial(payload, "keyed")
                self.assertIn("keyed", str(ctx.exception))
                self.assertIn(VERSION_SERIAL_KEY, str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
