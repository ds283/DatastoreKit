"""
Further value tables, ``InventorySpec.extra_values`` and ``Record.extra_value_counts`` (added by
``extra-values`` prompt 01), on the full real store of ``real_store_fixtures.build_full_store`` and
on stores of a wider registry.

1. **compatibility**: the full store read through a registry whose ``Trace`` spec declares no
   extra table gives, at format 1, the format-1 golden in every field but ``taken``; every class
   but ``Trace`` has the same canonical lines read through either registry;
2. **counts**: through the neutral registry, each ``Trace`` record counts its ``TraceMark`` rows,
   0 where none, and keeps its ``value_count``; every other class's records carry no counts, and
   their ``as_json`` keys are the four they were;
3. **two tables**: a spec declaring two extra tables counts each, 0 where a table has no row;
4. **orphans**: an extra table's row naming a serial not on its shard is one ``orphan-value``
   problem, naming the table and the shard, and the fingerprint counts it by name;
5. **replicated divergence**: an extra count of the replicated ``Gadget`` that differs between
   shards is one ``replicated-divergence`` problem;
6. **the fingerprint sees it**: one ``TraceMark`` row deleted moves the overall digest and
   ``Trace``'s entry alone;
7. **the refusal**: a spec naming its value table in its ``extra_values`` too is refused by
   ``inventory_classes``, naming the class and the table, and not by ``inventory_specs`` or
   ``dependent_tables``;
8. **``dependent_tables``**: the same answer with and without ``Trace``'s declaration, and a drop
   of ``Trace`` takes ``TraceMark``.

No test here starts Ray or constructs a ``ShardedPool``, and every store is in a temporary
directory.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

import sqlalchemy as sqla

from datastorekit.SQL.factory_base import SQLAFactoryBase
from datastorekit.SQL.schema import dependent_tables
from datastorekit.store_fingerprint import (
    ENCODING_FORMAT,
    compare_fingerprints,
    fingerprint_of,
)
from datastorekit.store_inventory import (
    InventorySpec,
    inventory_classes,
    inventory_specs,
    read_inventory,
)
from datastorekit.tests.client.registry import factories as _factories
from datastorekit.tests.real_store_fixtures import (
    build_full_store,
    build_real_store,
    fill_required,
    full_rows,
    with_rows,
)
from datastorekit.tests.test_store_fingerprint import NEUTRAL_FORMAT

# the golden fingerprint of build_full_store() at client format 1, taken before any spec declared
# a further value table; a spec that declares none must still reproduce it
FORMAT_1_GOLDEN = (
    Path(__file__).resolve().parent
    / "data"
    / f"store_fingerprint-neutral-1-encoding-{ENCODING_FORMAT}.json"
)

# the full store's Trace whose TraceMark rows it holds, by its label
MARKED_TRACE = "fixture-trace-3"

FOUR_KEYS = {"key", "tags", "validated", "value_count"}


def tearDownModule():
    ray = sys.modules.get("ray")
    if ray is not None and ray.is_initialized():
        raise AssertionError("Ray was initialised by test_inventory_extra_values")


# ---------------------------------------------------------------------------------------------
# registries
# ---------------------------------------------------------------------------------------------


def _respecified(factory, extra_values):
    """A subclass of ``factory`` whose ``inventory_spec`` is ``factory``'s with ``extra_values``
    in place of its own. The spec is built when the hook is called, as a factory builds it.
    """
    keywords = factory.inventory_spec().keywords()

    class _Respecified(factory):
        @staticmethod
        def inventory_spec():
            return InventorySpec(**{**keywords, "extra_values": dict(extra_values)})

    return _Respecified


def undeclared():
    """The neutral registry with ``Trace``'s spec declaring no extra table."""
    out = dict(_factories)
    out["Trace"] = _respecified(_factories["Trace"], {})
    return out


class _TraceNote_factory(SQLAFactoryBase):
    """A second further value table of ``Trace``, in the wider registry only."""

    @staticmethod
    def register():
        return {
            "version": False,
            "timestamp": False,
            "columns": [
                sqla.Column(
                    "trace_serial",
                    sqla.Integer,
                    sqla.ForeignKey("Trace.serial"),
                    index=True,
                    nullable=False,
                ),
                sqla.Column("note_index", sqla.Integer, nullable=False),
            ],
        }


class _GadgetNote_factory(SQLAFactoryBase):
    """A further value table of the replicated ``Gadget``, in the wider registry only."""

    @staticmethod
    def register():
        return {
            "version": False,
            "timestamp": False,
            "columns": [
                sqla.Column(
                    "gadget_serial",
                    sqla.Integer,
                    sqla.ForeignKey("Gadget.serial"),
                    index=True,
                    nullable=False,
                ),
                sqla.Column("note_index", sqla.Integer, nullable=False),
            ],
        }


def wider():
    """The neutral registry with ``TraceNote`` (under ``Trace``) and ``GadgetNote`` (under
    ``Gadget``) added, each declared in its owner's ``extra_values``."""
    out = {}
    for name, factory in _factories.items():
        out[name] = factory
        if name == "GadgetPart":
            out["GadgetNote"] = _GadgetNote_factory
        if name == "TraceMark":
            out["TraceNote"] = _TraceNote_factory
    out["Trace"] = _respecified(
        _factories["Trace"],
        {"TraceMark": "trace_serial", "TraceNote": "trace_serial"},
    )
    out["Gadget"] = _respecified(_factories["Gadget"], {"GadgetNote": "gadget_serial"})
    return out


def refused():
    """The neutral registry with ``Trace``'s value table named in its ``extra_values`` too."""
    out = dict(_factories)
    out["Trace"] = _respecified(_factories["Trace"], {"TraceStep": "trace_serial"})
    return out


# ---------------------------------------------------------------------------------------------
# stores
# ---------------------------------------------------------------------------------------------


def wider_store(directory: Path, added=None):
    """A store of ``wider()``: the full store's rows through ``fill_required``, then ``added``
    (shard -> rows of the wider registry's own tables, each row stating every non-null column)
    appended to that shard's rows, with the full store's shard keys."""
    replicated, sharded, keys = full_rows()
    sharded = {n: fill_required(rows) for n, rows in sharded.items()}
    for n, rows in (added or {}).items():
        sharded[n] = with_rows(sharded.get(n, {}), rows)
    return build_real_store(
        directory,
        replicated=fill_required(replicated),
        sharded=sharded,
        shard_keys=keys,
        factories=wider(),
    )


def canonical_lines(inventory) -> dict:
    """class -> its records' canonical lines, in order."""
    return {
        name: [r.canonical_json() for r in cls.records]
        for name, cls in inventory.classes.items()
    }


def by_label(inventory) -> dict:
    """Each Trace record by its label."""
    return {r.key["trace_label"]: r for r in inventory["Trace"].records}


class _Stores(unittest.TestCase):
    """A temporary directory, each store built in a directory of its own in it."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.top = Path(cls._tmp.name).resolve()
        cls._count = 0

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    @classmethod
    def directory(cls) -> Path:
        cls._count += 1
        out = cls.top / f"store-{cls._count}"
        out.mkdir()
        return out

    @classmethod
    def full(cls, factories=None, **kwargs):
        store = build_full_store(cls.directory(), **kwargs)
        return read_inventory(
            store.primary, _factories if factories is None else factories
        )

    @classmethod
    def wide(cls, added=None):
        return read_inventory(wider_store(cls.directory(), added).primary, wider())


class TestCompatibility(_Stores):
    """Test 1: a spec that declares no extra table gives the records it gave."""

    def test_the_format_1_golden_and_every_other_class(self):
        store = build_full_store(self.directory())
        plain_inventory = read_inventory(store.primary, undeclared())
        golden = json.loads(FORMAT_1_GOLDEN.read_text())
        current = fingerprint_of(plain_inventory, 1)
        golden.pop("taken")
        current.pop("taken")
        self.assertEqual(current, golden)

        declared = canonical_lines(read_inventory(store.primary, _factories))
        plain = canonical_lines(plain_inventory)
        self.assertEqual(set(declared), set(plain))
        for name in declared:
            if name == "Trace":
                continue
            with self.subTest(cls=name):
                self.assertEqual(declared[name], plain[name])


class TestCounts(_Stores):
    """Test 2: each Trace counts its TraceMark rows; no other class carries counts."""

    def test_the_counts(self):
        store = build_full_store(self.directory())
        inventory = read_inventory(store.primary, _factories)
        plain = by_label(read_inventory(store.primary, undeclared()))
        traces = by_label(inventory)
        self.assertIn(MARKED_TRACE, traces)
        for label, record in traces.items():
            with self.subTest(trace=label):
                self.assertEqual(
                    record.extra_value_counts,
                    {"TraceMark": 2 if label == MARKED_TRACE else 0},
                )
                self.assertEqual(record.value_count, plain[label].value_count)
        for name, cls in inventory.classes.items():
            if name == "Trace":
                continue
            for record in cls.records:
                with self.subTest(cls=name):
                    self.assertEqual(record.extra_value_counts, {})
                    self.assertEqual(set(record.as_json()), FOUR_KEYS)
        self.assertEqual(inventory.problems, ())


class TestTwoTables(_Stores):
    """Test 3: two extra tables are each counted, 0 where a table has no row."""

    def test_each_table_is_counted(self):
        serial = 3  # the full store's MARKED_TRACE, on shard 0
        inventory = self.wide(
            {0: {"TraceNote": [{"serial": 1, "trace_serial": serial, "note_index": 0}]}}
        )
        traces = by_label(inventory)
        self.assertEqual(
            traces[MARKED_TRACE].extra_value_counts, {"TraceMark": 2, "TraceNote": 1}
        )
        others = [r for label, r in traces.items() if label != MARKED_TRACE]
        self.assertGreater(len(others), 0)
        for record in others:
            with self.subTest(trace=record.key["trace_label"]):
                self.assertEqual(
                    record.extra_value_counts, {"TraceMark": 0, "TraceNote": 0}
                )
        self.assertEqual(inventory.problems, ())


class TestOrphans(_Stores):
    """Test 4: an extra table's orphan rows are an orphan-value problem, counted by name."""

    def test_an_orphan_row_is_named(self):
        inventory = self.wide(
            {1: {"TraceNote": [{"serial": 1, "trace_serial": 999, "note_index": 0}]}}
        )
        (problem,) = inventory.problems
        self.assertEqual(inventory["Trace"].problems, (problem,))
        self.assertTrue(problem.startswith("orphan-value"), problem)
        self.assertIn("TraceNote", problem)
        self.assertIn("shard #1", problem)
        fingerprint = fingerprint_of(inventory, NEUTRAL_FORMAT)
        self.assertEqual(fingerprint["problems"], {"Trace": {"orphan-value": 1}})


class TestReplicatedDivergence(_Stores):
    """Test 5: a replicated class whose extra count differs between shards diverges."""

    def test_one_shard_alone_holds_an_extra_row(self):
        inventory = self.wide(
            {0: {"GadgetNote": [{"serial": 1, "gadget_serial": 1, "note_index": 0}]}}
        )
        (problem,) = inventory.problems
        self.assertEqual(inventory["Gadget"].problems, (problem,))
        self.assertTrue(problem.startswith("replicated-divergence"), problem)


class TestTheFingerprintSeesIt(_Stores):
    """Test 6: one TraceMark row deleted moves the overall digest and Trace's entry alone."""

    def test_one_row_deleted(self):
        before = fingerprint_of(self.full(), NEUTRAL_FORMAT)
        after = fingerprint_of(
            self.full(extra_sql={0: ["DELETE FROM TraceMark WHERE serial = 2"]}),
            NEUTRAL_FORMAT,
        )
        self.assertNotEqual(before["digest"], after["digest"])
        self.assertEqual(set(before["classes"]), set(after["classes"]))
        for name in before["classes"]:
            if name == "Trace":
                continue
            with self.subTest(cls=name):
                self.assertEqual(before["classes"][name], after["classes"][name])
        self.assertNotEqual(before["classes"]["Trace"], after["classes"]["Trace"])
        differences = compare_fingerprints(before, after)
        self.assertGreater(len(differences), 0)
        self.assertEqual({d["class"] for d in differences}, {"Trace"})


class TestTheRefusal(unittest.TestCase):
    """Test 7: the value table named in extra_values too is refused by inventory_classes alone."""

    def test_refused_by_inventory_classes_only(self):
        factories = refused()
        with self.assertRaisesRegex(ValueError, r"Trace\b.*\bTraceStep\b"):
            inventory_classes(factories)
        specs = inventory_specs(factories)
        self.assertEqual(specs["Trace"].extra_values, {"TraceStep": "trace_serial"})
        self.assertEqual(
            dependent_tables(["Trace"], factories),
            dependent_tables(["Trace"], _factories),
        )


class TestDependentTables(unittest.TestCase):
    """Test 8: dependent_tables gives the same answer with and without Trace's declaration."""

    def test_the_same_answer(self):
        plain = undeclared()
        for dropped in (["Trace"], ["TraceMark"], ["keypoint"]):
            with self.subTest(dropped=dropped):
                self.assertEqual(
                    dependent_tables(dropped, _factories),
                    dependent_tables(dropped, plain),
                )
        self.assertIn("TraceMark", dependent_tables(["Trace"], _factories))


if __name__ == "__main__":
    unittest.main()
