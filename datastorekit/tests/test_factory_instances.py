"""
A factory may be an instance (``factory-defaults`` prompt 01, decision U1).

``SQLAFactoryBase`` is an ``ABC`` whose only abstract hooks are ``register`` and ``build``. The
base defaults ``store``, ``validate`` and ``validate_on_startup`` as it defaults ``revalidate``,
``owned_serials`` and ``inventory_spec``: static, raising ``NotImplementedError`` (or returning
``None``). A factory class that defines ``register`` and ``build`` can therefore be instantiated,
and its instance registered in place of the class. The layer calls each hook on the registry's
entry, class or instance alike (``docs/client-contract.md`` §9.5):

1. ``gauge_setting_factory``, which defines only ``register``, ``build`` and ``inventory_spec``,
   instantiates, and its instance, registered in place of the class, serves a get that writes a
   row; a reopen with the same registry gets the same serial, deserialised;
2. a parameterised factory (``tests/client/instances.py``), one class registered as two instances
   over two tables that differ by the constructor's column name: each table gets its own rows, the
   two hold different rows, a reopen finds each table's rows under the same serials, and each
   instance's ``register()`` names its own column;
3. the base's abstract hooks are exactly ``register`` and ``build``: a subclass lacking either
   raises ``TypeError`` on instantiation, naming it;
4. ``store``, ``validate`` and ``validate_on_startup`` raise ``NotImplementedError`` when called
   on ``gauge_setting_factory`` and on an instance of it; and through the pool, on a fresh store
   for each call, ``object_store`` and ``object_validate`` of a ``gauge_setting`` raise
   ``NotImplementedError`` with its factory registered as the class and as an instance. The class
   and the instance are tested apart, so that the class's half shows ``v0.2.2``'s behaviour on its
   own;
5. a registry holding instances round-trips ``ray.cloudpickle``, and the copies, each an instance
   of its class with its constructor's value, serve a pool as in test 2;
6. ``_defines`` of ``test_neutral_client`` reads an instance as it reads its class.

Under a base whose three hooks are abstract (``v0.2.2``'s), tests 1, 2, 5, 6 and the instance
halves of 4 error with ``TypeError`` where they instantiate, and test 3 fails. No instance is made
when this module, or ``tests/client/instances.py``, is imported, so each test fails on its own.

On the stand-in pool and the neutral client, every store in a temporary directory. Serials are not
fixed between runs, so each is compared with one read from another call, never with a literal.
``ray.cloudpickle`` is imported from Ray, which it does not start. No Ray.
"""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import ray
from ray import cloudpickle

from datastorekit.SQL.factory_base import SQLAFactoryBase
from datastorekit.tests import standin_pool as sp
from datastorekit.tests.client import build, instances, registry
from datastorekit.tests.client.factories import gauge_setting_factory
from datastorekit.tests.client.objects import gauge_setting
from datastorekit.tests.test_neutral_client import _defines

GAUGE_TABLE = "gauge_setting"
GAUGE_EXPONENT = build.GAUGE_EXPONENTS[0]
THREE = ("store", "validate", "validate_on_startup")


def tearDownModule():
    if ray.is_initialized():
        raise AssertionError("Ray was initialised by test_factory_instances")


def _with_gauge_instance() -> dict:
    """A copy of the registry's factories with ``gauge_setting`` registered as an instance."""
    factories = dict(registry.factories)
    factories[GAUGE_TABLE] = gauge_setting_factory()
    return factories


def _three_calls(factory, obj) -> dict:
    """Each of the three defaulted hooks, called on ``factory`` with contract §3's arguments."""
    return {
        "store": lambda: factory.store(
            obj, conn=None, table=None, inserter=None, tables={}, inserters={}
        ),
        "validate": lambda: factory.validate(obj, conn=None, table=None, tables={}),
        "validate_on_startup": lambda: factory.validate_on_startup(
            conn=None, table=None, tables={}, prune=False
        ),
    }


def _new_insert(obj) -> bool:
    return getattr(obj, "_new_insert", False) is True


def _deserialized(obj) -> bool:
    return getattr(obj, "_deserialized", False) is True and not _new_insert(obj)


class _StoreCase(unittest.TestCase):
    """A temporary directory and one stand-in cluster, active for the test."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.directory = Path(tmp.name)

        self.cluster = sp.StandinCluster()
        active = self.cluster.active()
        active.__enter__()
        self.addCleanup(active.__exit__, None, None, None)

    def tearDown(self):
        self.assertFalse(ray.is_initialized())

    def open(self, name: str, factories: dict, replicated_tables=None):
        """
        A read-write pool on the store ``name`` with ``factories`` and ``replicated_tables`` (the
        registry's by default), built as ``StandinCluster.open_pool`` builds one.
        """
        primary = self.directory / name / "store.sqlite"
        with contextlib.redirect_stdout(io.StringIO()):
            pool = sp.sp_mod.ShardedPool(
                version_label="standin",
                db_name=primary,
                ShardKeyType=registry.shard_key_type,
                ShardKeyStoreIdGetter=registry.shard_key_store_id,
                replicated_tables=(
                    registry.replicated_tables
                    if replicated_tables is None
                    else replicated_tables
                ),
                sharded_tables=registry.sharded_tables,
                shards=3,
                factories=factories,
            )
        self.cluster.pool = pool
        return pool

    def close(self, pool):
        self.cluster.close_pool(pool)

    def values_on_every_shard(self, pool, table: str, column: str) -> set:
        """The values of ``column`` in ``table``, the same on every shard."""
        found = set()
        for sid, path in sorted(pool._shard_db_files.items()):
            columns = sp.table_columns(path, table)
            self.assertIn(column, columns, (sid, table))
            index = columns.index(column)
            values = {row[index] for row in sp.shard_rows(pool, table)[sid]}
            if found:
                self.assertEqual(values, found, (sid, table))
            found = values
        return found

    def get_scalar(self, pool, name: str, value: int):
        return build.resolve(pool.object_get(name, value=value))

    def serve_instances(self, factories: dict, replicated_tables: list):
        """
        Test 2's checks, on the store ``"instances"``: each of the two tables gets its value; the
        two hold different rows; a reopen with the same registry finds each under its serial.
        """
        pool = self.open("instances", factories, replicated_tables)
        first = {}
        for name, value in instances.SCALAR_VALUES.items():
            got = self.get_scalar(pool, name, value)
            self.assertTrue(_new_insert(got), name)
            self.assertEqual(got.value, value)
            first[name] = got.store_id
        self.close(pool)

        # each table holds its own value, and not the other's
        left, right = instances.SCALAR_TABLES.items()
        left_values = self.values_on_every_shard(pool, *left)
        right_values = self.values_on_every_shard(pool, *right)
        self.assertEqual(left_values, {instances.SCALAR_VALUES[left[0]]})
        self.assertEqual(right_values, {instances.SCALAR_VALUES[right[0]]})
        self.assertNotEqual(left_values, right_values)

        pool = self.open("instances", factories, replicated_tables)
        for name, value in instances.SCALAR_VALUES.items():
            got = self.get_scalar(pool, name, value)
            self.assertTrue(_deserialized(got), name)
            self.assertEqual(got.store_id, first[name], name)
        self.close(pool)
        return first


class TestAnInstanceOfAClass(_StoreCase):
    """Test 1."""

    def test_an_instance_registered_in_place_of_its_class(self):
        factories = _with_gauge_instance()
        self.assertIsInstance(factories[GAUGE_TABLE], gauge_setting_factory)

        pool = self.open("gauge", factories)
        got = build.get_gauge(pool, GAUGE_EXPONENT)
        self.assertTrue(_new_insert(got))
        self.assertEqual(
            self.values_on_every_shard(pool, GAUGE_TABLE, "gauge_exponent"),
            {GAUGE_EXPONENT},
        )
        self.close(pool)

        pool = self.open("gauge", factories)
        again = build.get_gauge(pool, GAUGE_EXPONENT)
        self.assertTrue(_deserialized(again))
        self.assertEqual(again.store_id, got.store_id)
        self.close(pool)


class TestAParameterisedFactory(_StoreCase):
    """Test 2."""

    def test_two_instances_over_two_tables(self):
        factories, replicated_tables = instances.instance_registry()
        for name, column in instances.SCALAR_TABLES.items():
            with self.subTest(name=name):
                factory = factories[name]
                self.assertIsInstance(factory, instances.scalar_entry_factory)
                self.assertEqual(factory.column, column)
                self.assertEqual(
                    [c.name for c in factory.register()["columns"]], [column]
                )
        self.serve_instances(factories, replicated_tables)


class TestTheAbstractHooks(unittest.TestCase):
    """Test 3."""

    def test_register_and_build_are_the_only_abstract_hooks(self):
        with self.subTest(part="__abstractmethods__"):
            self.assertEqual(
                SQLAFactoryBase.__abstractmethods__, frozenset({"register", "build"})
            )

        class lacks_register(SQLAFactoryBase):
            @staticmethod
            def build(payload, conn, table, inserter, tables, inserters):
                return None

        class lacks_build(SQLAFactoryBase):
            @staticmethod
            def register():
                return None

        for cls, missing in ((lacks_register, "register"), (lacks_build, "build")):
            with self.subTest(part=cls.__name__):
                with self.assertRaises(TypeError) as raised:
                    cls()
                message = str(raised.exception)
                self.assertIn(cls.__name__, message)
                self.assertIn(f"'{missing}'", message)


class TestTheDefaults(_StoreCase):
    """Test 4: called directly, and through the pool, from the class and from an instance."""

    def assertEachRaises(self, factory):
        obj = gauge_setting(None, GAUGE_EXPONENT)
        for hook, call in _three_calls(factory, obj).items():
            with self.subTest(hook=hook):
                with self.assertRaises(NotImplementedError) as raised:
                    call()
                self.assertEqual(raised.exception.args, ())

    def test_the_defaults_raise_from_the_class(self):
        self.assertEachRaises(gauge_setting_factory)

    def test_the_defaults_raise_from_an_instance(self):
        self.assertEachRaises(gauge_setting_factory())

    def assertPoolRaises(self, factories: dict, label: str):
        """``object_store``, then ``object_validate``, of a gauge setting, each on a new store."""
        for call in ("object_store", "object_validate"):
            with self.subTest(call=call):
                pool = self.open(f"{label}-{call}", factories)
                # closed whatever happens, so that the next sub-test can open its own pool
                try:
                    got = build.get_gauge(pool, GAUGE_EXPONENT)
                    # the actor's traceback, printed by the stand-in, is v0.2.2's output
                    printed = io.StringIO()
                    with self.assertRaises(NotImplementedError) as raised:
                        with (
                            contextlib.redirect_stdout(printed),
                            contextlib.redirect_stderr(printed),
                        ):
                            build.resolve(getattr(pool, call)(got))
                    self.assertEqual(raised.exception.args, ())
                finally:
                    self.close(pool)

    def test_through_the_pool_with_the_class_registered(self):
        factories = dict(registry.factories)
        self.assertIs(factories[GAUGE_TABLE], gauge_setting_factory)
        self.assertPoolRaises(factories, "class")

    def test_through_the_pool_with_an_instance_registered(self):
        self.assertPoolRaises(_with_gauge_instance(), "instance")


class TestSerialisation(_StoreCase):
    """Test 5."""

    def test_a_registry_of_instances_round_trips_cloudpickle(self):
        factories, replicated_tables = instances.instance_registry()
        copies = cloudpickle.loads(cloudpickle.dumps(factories))

        self.assertEqual(list(copies), list(factories))
        self.assertIsInstance(copies[GAUGE_TABLE], gauge_setting_factory)
        self.assertIsNot(copies[GAUGE_TABLE], factories[GAUGE_TABLE])
        for name, column in instances.SCALAR_TABLES.items():
            with self.subTest(name=name):
                self.assertIsInstance(copies[name], instances.scalar_entry_factory)
                self.assertIsNot(copies[name], factories[name])
                self.assertEqual(copies[name].column, column)
        # the classes the registry names travel by reference
        for name, factory in factories.items():
            if isinstance(factory, type):
                self.assertIs(copies[name], factory, name)

        self.serve_instances(copies, replicated_tables)
        self.assertFalse(ray.is_initialized())


class TestDefinesReadsAnInstanceAsItsClass(unittest.TestCase):
    """Test 6."""

    def test_defines_of_a_class_and_of_its_instance(self):
        for factory in (gauge_setting_factory, gauge_setting_factory()):
            with self.subTest(factory=factory):
                self.assertTrue(_defines(factory, "register"))
                self.assertTrue(_defines(factory, "build"))
                for hook in THREE + ("revalidate",):
                    self.assertFalse(_defines(factory, hook), hook)

        factory = instances.scalar_entry_factory("left_value")
        self.assertTrue(_defines(factory, "register"))
        self.assertTrue(_defines(factory, "build"))
        for hook in THREE + ("revalidate", "owned_serials", "inventory_spec"):
            self.assertFalse(_defines(factory, hook), hook)


if __name__ == "__main__":
    unittest.main()
