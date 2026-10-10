"""
The structured inventory, ``datastorekit/store_inventory.py`` ``read_inventory``, on the full real
store of ``real_store_fixtures.build_full_store``.

1. the keys are physical: the same content under other serials, on other shards, gives an equal
   inventory;
2. every identity column matters: changing one changes the class's records;
3. what is not identity does not matter: labels, timestamps, payload, solver serials, cosmology
   names, version foreign keys;
4. floats: the stored bits, through ``canonical`` and nothing else;
5. tags: a record's own association rows, and a tagged parent's digest covers them;
6. value counts: per parent, from one ``GROUP BY``;
7. replicated divergence is a named problem naming the shard;
8. orphans are named problems, and change nothing else;
9. duplicates are a named problem, and both are kept;
10. read-only and no Ray.

No test here starts Ray or constructs a ``ShardedPool``, and every store is in a temporary
directory.
"""

import ast
import copy
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from datetime import datetime
from pathlib import Path
from unittest import mock

import sqlalchemy as sqla

import datastorekit.store_inventory as store_inventory
from datastorekit.store_inventory import (
    canonical,
    canonical_json,
    read_inventory,
)
from datastorekit.tests.real_store_fixtures import (
    build_full_store,
    file_state,
    find_row,
    full_rows,
    relabel_serials,
    vary_row,
)
from datastorekit.tests.client.registry import factories as _factories

# the classes of the inventory, in the order it reads them. The layer derives this order
# (``inventory_classes``); this literal pins the derivation, so that it is not compared with itself
INVENTORY_CLASSES = (
    "version",
    "store_tag",
    "keypoint",
    "dial_setting",
    "knob_setting",
    "gauge_setting",
    "routing_rule",
    "keypoint_alias",
    "Gadget",
    "Tessera",
    "Sample",
    "Trace",
    "Weave",
)

REPO_ROOT = Path(__file__).resolve().parents[2]
# the directory of the neutral client, whose factories.py holds its factories
FACTORIES = REPO_ROOT / "datastorekit" / "tests" / "client"

VALUE_TABLES = (
    "GadgetPart",
    "TraceStep",
)

# class -> key field -> (table, serial, column, a new value) that changes that one identity column
# of one row. Each list is read from the class's build() lookup, optional filters included
IDENTITY = {
    "version": {"label": ("version", 2, "label", "2023.1.1")},
    "store_tag": {"label": ("store_tag", 3, "label", "renamed-tag")},
    "keypoint": {"kp_position": ("keypoint", 3, "kp_position", 0.25)},
    "dial_setting": {
        "dial_level": ("dial_setting", 2, "dial_level", 7),
        "stepping": ("dial_setting", 2, "stepping", 2),
    },
    "knob_setting": {
        "knob_turns": ("knob_setting", 1, "knob_turns", 9),
        "stepping": ("knob_setting", 1, "stepping", 3),
    },
    "gauge_setting": {"gauge_exponent": ("gauge_setting", 2, "gauge_exponent", 12)},
    "routing_rule": {
        "rule_label": ("routing_rule", 3, "rule_label", "renamed-rule"),
        "rule_threshold": ("routing_rule", 3, "rule_threshold", -11.0),
        "rule_mode": ("routing_rule", 3, "rule_mode", "prefer-other"),
    },
    "keypoint_alias": {
        "ka_offset": ("keypoint_alias", 3, "ka_offset", 0.375),
        "stepping": ("keypoint_alias", 3, "stepping", 1),
        "keypoint": ("keypoint_alias", 4, "keypoint_serial", 3),
    },
    "Gadget": {
        "gadget_label": ("Gadget", 2, "gadget_label", "renamed-gadget"),
        # Gadget 2's frame is knob setting 1; dial setting 1 shares its serial, so the variation
        # changes the type the reference is resolved through, and does not make it unresolved
        "frame_kind": ("Gadget", 2, "frame_kind", 1),
        "frame": ("Gadget", 1, "frame_serial", 2),
    },
    "Tessera": {
        "tessera_weight": ("Tessera", 5, "tessera_weight", 0.875),
        "k": ("Tessera", 4, "alias_serial", 3),
    },
    "Sample": {
        "sample_code": ("Sample", 2, "sample_code", "renamed-sample"),
        "k": ("Sample", 2, "keypoint_serial", 3),
        "gadget": ("Sample", 2, "gadget_serial", 2),
        # Sample 2's anchor is Tessera 5 (shard 1, a cross-shard parent); Tessera 4 is real and on
        # shard 1 too, so the variation changes the identity it resolves to
        "anchor": ("Sample", 2, "anchor_serial", 4),
        # Sample_members has no serial of its own, so its row cannot be addressed: the set is
        # varied through the Tessera its members name. Tessera 2 is a member of Samples 1 and 2,
        # and is named by nothing else
        "members": ("Tessera", 2, "tessera_weight", 0.875),
    },
    "Trace": {
        "trace_label": ("Trace", 3, "trace_label", "renamed-trace"),
        # Trace 3's frame is knob setting 1, which shares its serial with dial setting 1
        "frame_kind": ("Trace", 3, "frame_kind", 1),
        "k": ("Trace", 3, "keypoint_serial", 3),
        "frame": ("Trace", 1, "frame_serial", 2),
    },
    "Weave": {
        "weave_label": ("Weave", 1, "weave_label", "renamed-weave"),
        "k": ("Weave", 1, "keypoint_serial", 3),
        # Weave 1's Trace is 4; Trace 1 is real and on shard 0, the Weave's own shard
        "trace": ("Weave", 1, "trace_serial", 1),
        # Weave 1 has no anchor: it gains Tessera 3, which is real and on shard 0
        "anchor": ("Weave", 1, "anchor_serial", 3),
        # Weave 1's strand 701 (anchor Tessera 1, no origin) gains anchor Tessera 2, which is real
        # and on shard 0, so the variation changes the identity the set resolves to and does not
        # make a member unresolved. It is the member field that shares its name with a key parent
        "strands": ("Weave_members", 701, "anchor_serial", 2),
    },
}

# (table, serial, column, a new value): columns that are not identity
NON_IDENTITY = [
    # payload and provenance
    ("Gadget", 1, "part_count", 9),
    ("GadgetPart", 1, "part_index", 9),
    ("GadgetPart", 1, "part_value", 7.0),
    ("Sample", 1, "member_count", 9),
    ("Sample", 1, "sample_validated", False),
    ("Trace", 1, "step_count", 9),
    ("TraceStep", 11, "step_index", 9),
    ("TraceStep", 11, "step_value", 7.0),
    # version foreign keys
    ("keypoint_alias", 1, "version", 2),
    ("routing_rule", 1, "version", 2),
    ("Gadget", 1, "version", 2),
    ("Tessera", 1, "version", 2),
    ("Sample", 1, "version", 2),
    ("Trace", 1, "version", 2),
    ("Weave", 1, "version", 2),
    # the marked and flagged flags, which accumulate by OR
    ("keypoint", 1, "kp_marked", False),
    ("keypoint", 2, "kp_flagged", False),
]


def records_of(inventory):
    return {name: c.records for name, c in inventory.classes.items()}


def changed(before, after):
    """The classes whose records differ."""
    return {n for n in before if before[n] != after[n]}


def kinds(problems):
    return [p.split(":", 1)[0] for p in problems]


class _Stores(unittest.TestCase):
    """A temporary directory, and a builder of full stores in it, each in its own directory."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls._tmp.name).resolve()
        cls._count = 0
        cls.baseline = cls.inventory()
        cls.base = records_of(cls.baseline)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    @classmethod
    def store(cls, **kwargs):
        cls._count += 1
        directory = cls.root / f"store-{cls._count}"
        directory.mkdir()
        return build_full_store(directory, **kwargs)

    @classmethod
    def inventory(cls, **kwargs):
        return read_inventory(cls.store(**kwargs).primary, _factories)

    def varied(self, table, serial, column, value, **kwargs):
        replicated, sharded, keys = full_rows()
        vary_row(replicated, sharded, table, serial, column, value)
        return self.inventory(
            replicated=replicated, sharded=sharded, shard_keys=keys, **kwargs
        )


class TestTheFullStore(_Stores):
    def test_every_class_has_a_record(self):
        self.assertEqual(tuple(self.baseline.classes), INVENTORY_CLASSES)
        for name in INVENTORY_CLASSES:
            with self.subTest(cls=name):
                self.assertGreater(self.baseline[name].count, 0)
                self.assertEqual(
                    self.baseline[name].count, len(self.baseline[name].records)
                )

    def test_the_full_store_has_no_problem(self):
        self.assertEqual(self.baseline.problems, ())

    def test_records_are_json_safe(self):
        for name, cls in self.baseline.classes.items():
            for record in cls.records:
                with self.subTest(cls=name):
                    text = json.dumps(record.as_json(), allow_nan=False)
                    self.assertEqual(
                        set(json.loads(text)),
                        {"key", "tags", "validated", "value_count"},
                    )
                    for leaf in record.key.values():
                        self.assertIsInstance(leaf, (str, int, bool, type(None)))

    def test_classes_with_tags_validated_and_values(self):
        tagged = {
            "Gadget",
            "Sample",
            "Trace",
            "Weave",
        }
        validated = tagged - {"Sample", "Weave"}
        for name, cls in self.baseline.classes.items():
            with self.subTest(cls=name):
                self.assertEqual(cls.tagged, name in tagged)
                for record in cls.records:
                    if name not in tagged:
                        self.assertEqual(record.tags, ())
                    else:
                        self.assertIn("fixture-run", record.tags)
                        self.assertEqual(record.tags, tuple(sorted(record.tags)))
                    if name in validated:
                        self.assertIsInstance(record.validated, bool)
                        self.assertIsNotNone(record.value_count)
                    else:
                        self.assertIsNone(record.validated)
                        self.assertIsNone(record.value_count)
        # unvalidated rows are recorded, with their flag
        for name in ("Gadget", "Trace"):
            self.assertIn(False, [r.validated for r in self.baseline[name].records])

    def test_replicated_and_sharded(self):
        from datastorekit.tests.client.registry import replicated_tables

        for name, cls in self.baseline.classes.items():
            self.assertEqual(cls.replicated, name in replicated_tables)

    def test_resolve_names_every_parent(self):
        qsi = self.baseline["Sample"]
        for record in qsi.records:
            resolved = self.baseline.resolve("Sample", record)
            for field in qsi.parents:
                self.assertIn("key", resolved[field], field)


class TestKeysArePhysical(_Stores):
    """Test 1: the same content, built with other serials and on other shards, is equal."""

    def assertSameInventory(self, other):
        self.assertEqual(tuple(other.classes), tuple(self.baseline.classes))
        for name in self.baseline.classes:
            with self.subTest(cls=name):
                self.assertEqual(other[name].records, self.baseline[name].records)
                self.assertEqual(other[name].count, self.baseline[name].count)
                self.assertEqual(other[name].problems, ())
                self.assertEqual(
                    other[name].earliest_timestamp,
                    self.baseline[name].earliest_timestamp,
                )

    def test_different_serial_assignments(self):
        replicated, sharded, keys = relabel_serials(*full_rows(), offset=100)
        base_replicated, base_sharded, _ = full_rows()
        # every replicated class, and every sharded one, really has other serials
        for table in ("Gadget", "keypoint_alias", "routing_rule"):
            self.assertTrue(
                {r["serial"] for r in replicated[table]}.isdisjoint(
                    {r["serial"] for r in base_replicated[table]}
                )
            )
        self.assertTrue(
            {r["serial"] for r in sharded[0]["Sample"]}.isdisjoint(
                {r["serial"] for r in base_sharded[0]["Sample"]}
            )
        )
        self.assertSameInventory(
            self.inventory(replicated=replicated, sharded=sharded, shard_keys=keys)
        )

    def test_sharded_rows_on_different_shards(self):
        replicated, sharded, keys = full_rows()
        moved = {0: {}, 1: sharded[1], 2: sharded[0]}
        moved_keys = {k: {0: 2, 1: 1}[s] for k, s in keys.items()}
        self.assertSameInventory(
            self.inventory(
                replicated=replicated, sharded=moved, shard_keys=moved_keys, shards=3
            )
        )

    def test_replicated_serials_permuted_and_rows_moved(self):
        replicated, sharded, keys = relabel_serials(*full_rows(), offset=37)
        moved = {0: sharded[1], 1: sharded[0]}
        moved_keys = {k: 1 - s for k, s in keys.items()}
        self.assertSameInventory(
            self.inventory(replicated=replicated, sharded=moved, shard_keys=moved_keys)
        )


class TestIdentityColumnsMatter(_Stores):
    """Test 2: each identity column, one at a time, changes the class's records."""

    def test_the_key_fields_are_the_lookup_columns(self):
        for name in INVENTORY_CLASSES:
            with self.subTest(cls=name):
                fields = {f for r in self.baseline[name].records for f in r.key}
                self.assertEqual(fields, set(IDENTITY[name]))

    def test_each_identity_column_changes_the_records(self):
        for name, fields in IDENTITY.items():
            for field, (table, serial, column, value) in fields.items():
                with self.subTest(cls=name, field=field):
                    after = self.varied(table, serial, column, value)[name].records
                    self.assertNotEqual(after, self.base[name])
                    self.assertNotEqual(
                        Counter(r.key[field] for r in after),
                        Counter(r.key[field] for r in self.base[name]),
                    )


class TestNonIdentityDoesNotMatter(_Stores):
    """Test 3: labels, timestamps, payload, solver serials, names and version keys."""

    def test_non_identity_columns(self):
        for table, serial, column, value in NON_IDENTITY:
            with self.subTest(table=table, column=column):
                self.assertEqual(
                    records_of(self.varied(table, serial, column, value)), self.base
                )

    def test_timestamps(self):
        replicated, sharded, keys = full_rows()
        tables = store_inventory_tables()
        stamp = datetime(2030, 1, 2, 3, 4, 5)
        for rows in [replicated] + list(sharded.values()):
            for table, table_rows in rows.items():
                if "timestamp" in tables[table].c:
                    for row in table_rows:
                        row["timestamp"] = stamp
        after = self.inventory(replicated=replicated, sharded=sharded, shard_keys=keys)
        self.assertEqual(records_of(after), self.base)
        self.assertEqual(after["Sample"].earliest_timestamp, stamp)


def store_inventory_tables():
    from datastorekit.tests.client.registry import factories as _factories
    from datastorekit.SQL.schema import build_schema

    return build_schema(sqla.MetaData(), _factories).tables


class TestFloats(_Stores):
    """Test 4: the stored bits, through ``canonical`` only."""

    def test_canonical(self):
        self.assertEqual(canonical(0.1), (0.1).hex())
        self.assertEqual(canonical(-5.0), "-0x1.4000000000000p+2")
        self.assertEqual(canonical(3), 3)
        self.assertIs(canonical(True), True)
        self.assertEqual(canonical("all"), "all")
        self.assertIsNone(canonical(None))
        self.assertNotEqual(canonical(0.1), canonical(math.nextafter(0.1, 1.0)))
        for bad in (datetime(2026, 1, 1), b"x", [1.0]):
            with self.assertRaises(TypeError):
                canonical(bad)

    def test_canonical_json(self):
        self.assertEqual(
            canonical_json({"b": 1.0, "a": [0.5, "x", None]}),
            '{"a":["0x1.0000000000000p-1","x",null],"b":"0x1.0000000000000p+0"}',
        )

    def test_the_last_bit_of_k_changes_the_records(self):
        after = self.varied("keypoint", 3, "kp_position", math.nextafter(0.5, 1.0))
        self.assertIn("keypoint", changed(self.base, records_of(after)))
        self.assertIn("keypoint_alias", changed(self.base, records_of(after)))

    def test_log10_tol_is_used_as_stored(self):
        self.assertEqual(
            sorted(r.key["rule_threshold"] for r in self.base["routing_rule"]),
            sorted(float.hex(v) for v in (-5.0, -7.0, -9.0)),
        )

    def test_every_float_leaf_goes_through_canonical(self):
        real = store_inventory.canonical

        def marked(value):
            out = real(value)
            return "F:" + out if isinstance(value, float) else out

        with mock.patch.object(store_inventory, "canonical", marked):
            inventory = self.inventory()
        self.assertEqual(
            sorted(r.key["rule_threshold"] for r in inventory["routing_rule"].records),
            sorted("F:" + float.hex(v) for v in (-5.0, -7.0, -9.0)),
        )
        self.assertTrue(
            all(
                r.key["kp_position"].startswith("F:")
                for r in inventory["keypoint"].records
            )
        )

    def test_only_canonical_formats_a_float(self):
        """No code of the inventory but ``canonical`` calls ``float.hex``, ``.hex()``, ``round``,
        ``format`` or ``repr``, and no factory's ``inventory_spec`` formats anything.
        """
        tree = ast.parse(
            (REPO_ROOT / "datastorekit" / "store_inventory.py").read_text()
        )
        offenders = []
        for func in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
            if func.name == "canonical":
                continue
            for node in ast.walk(func):
                if isinstance(node, ast.Attribute) and node.attr == "hex":
                    offenders.append(f"store_inventory.{func.name}")
                if isinstance(node, ast.Name) and node.id in ("round", "format"):
                    offenders.append(f"store_inventory.{func.name}")
        canonical_def = [
            n
            for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name == "canonical"
        ]
        self.assertEqual(len(canonical_def), 1)
        self.assertTrue(
            any(
                isinstance(n, ast.Attribute) and n.attr == "hex"
                for n in ast.walk(canonical_def[0])
            )
        )

        builders = 0
        for path in sorted(FACTORIES.glob("*.py")):
            # base.py's hook declares no class: it returns None
            if path.name == "base.py":
                continue
            for func in ast.walk(ast.parse(path.read_text())):
                if isinstance(func, ast.FunctionDef) and func.name == "inventory_spec":
                    builders += 1
                    for node in ast.walk(func):
                        if isinstance(node, (ast.JoinedStr, ast.FormattedValue)):
                            offenders.append(f"{path.name}: an f-string")
                        if isinstance(node, ast.Attribute) and node.attr in (
                            "hex",
                            "format",
                        ):
                            offenders.append(f"{path.name}: .{node.attr}")
                        if isinstance(node, ast.Name) and node.id in (
                            "float",
                            "round",
                            "repr",
                            "str",
                            "format",
                        ):
                            offenders.append(f"{path.name}: {node.id}")
        # one hook fewer than classes: the client's _label_factory serves version and store_tag
        self.assertEqual(builders, 12)
        self.assertEqual(offenders, [])


class TestTags(_Stores):
    """Test 5: tags come from each record's own association table, and a tagged parent's digest
    covers them."""

    def _with(self, shard, table, row):
        replicated, sharded, keys = full_rows()
        target = replicated if shard is None else sharded[shard]
        target.setdefault(table, []).append(row)
        return records_of(
            self.inventory(replicated=replicated, sharded=sharded, shard_keys=keys)
        )

    def test_adding_a_tag_changes_that_record_and_nothing_else(self):
        after = self._with(0, "Sample_tags", {"sample_serial": 2, "tag_serial": 4})
        self.assertEqual(changed(self.base, after), {"Sample"})
        gone = set(self.base["Sample"]) - set(after["Sample"])
        new = set(after["Sample"]) - set(self.base["Sample"])
        self.assertEqual((len(gone), len(new)), (1, 1))
        (gone,), (new,) = gone, new
        self.assertEqual(new.key, gone.key)
        self.assertEqual(new.validated, gone.validated)
        self.assertEqual(new.value_count, gone.value_count)
        self.assertEqual(gone.tags, ("fixture-run",))
        self.assertEqual(new.tags, ("fixture-run", "grid-B"))

    def test_a_tagged_parents_digest_covers_its_tags(self):
        """Two Trace rows can differ only in their tags, so a Weave's reference to its Trace
        changes when a tag is added to the Trace."""
        after = self._with(0, "Trace_tags", {"trace_serial": 4, "tag_serial": 4})
        # Trace 4 is Weave 1's Trace, and no strand of it names Trace 4, so only the Weave's trace
        # field changes; no other class names a Trace
        self.assertEqual(
            changed(self.base, after),
            {"Trace", "Weave"},
        )
        gone = set(self.base["Weave"]) - set(after["Weave"])
        new = set(after["Weave"]) - set(self.base["Weave"])
        self.assertEqual((len(gone), len(new)), (1, 1))
        (gone,), (new,) = gone, new
        self.assertEqual(
            {f for f in gone.key if gone.key[f] != new.key[f]},
            {"trace"},
        )

    def test_a_tag_on_the_background_model_reaches_its_children(self):
        after = self._with(None, "Gadget_tags", {"gadget_serial": 2, "tag_serial": 4})
        # Gadget 2 is the parent of Sample 4 only, and no class names a Sample
        self.assertEqual(
            changed(self.base, after),
            {
                "Gadget",
                "Sample",
            },
        )

    def test_oneloop_tags_come_from_its_own_table(self):
        (record,) = self.base["Weave"]
        self.assertEqual(record.tags, ("fixture-run", "weave-tag"))
        # Trace 1 has the same serial as Weave 1, and other tags
        after = self._with(0, "Trace_tags", {"trace_serial": 1, "tag_serial": 4})
        self.assertEqual(changed(self.base, after), {"Trace"})
        after = self._with(0, "Weave_tags", {"weave_serial": 1, "tag_serial": 4})
        self.assertEqual(changed(self.base, after), {"Weave"})
        (record,) = after["Weave"]
        self.assertEqual(record.tags, ("fixture-run", "grid-B", "weave-tag"))

    def test_a_tag_no_row_carries_is_only_a_store_tag(self):
        labels = {r.key["label"] for r in self.base["store_tag"]}
        self.assertIn("unused-tag", labels)
        carried = {t for c in self.base.values() for r in c for t in r.tags}
        self.assertNotIn("unused-tag", carried)


class TestValueCounts(_Stores):
    """Test 6: each record carries its own value count."""

    # value table -> (the parent class, the value serial deleted)
    DELETIONS = {
        "GadgetPart": ("Gadget", 4),
        "TraceStep": ("Trace", 12),
    }

    def test_the_counts_are_per_parent(self):
        expected = {
            "Gadget": [3, 2],
            "Trace": [3, 4, 2, 1],
        }
        for name, counts in expected.items():
            with self.subTest(cls=name):
                self.assertEqual(
                    Counter(r.value_count for r in self.base[name]), Counter(counts)
                )

    def test_deleting_a_value_row_lowers_one_count_by_one(self):
        for table, (name, serial) in self.DELETIONS.items():
            with self.subTest(table=table):
                replicated, sharded, keys = full_rows()
                for rows in [replicated] + list(sharded.values()):
                    if table in rows:
                        rows[table] = [r for r in rows[table] if r["serial"] != serial]
                after = records_of(
                    self.inventory(
                        replicated=replicated, sharded=sharded, shard_keys=keys
                    )
                )
                self.assertEqual(changed(self.base, after), {name})
                gone = set(self.base[name]) - set(after[name])
                new = set(after[name]) - set(self.base[name])
                self.assertEqual((len(gone), len(new)), (1, 1))
                (gone,), (new,) = gone, new
                self.assertEqual((new.key, new.tags), (gone.key, gone.tags))
                self.assertEqual(new.value_count, gone.value_count - 1)

    def test_value_tables_are_only_counted(self):
        """No statement reads a *Value table except one GROUP BY count."""
        statements = []

        def capture(conn, cursor, statement, parameters, context, executemany):
            statements.append(statement)

        store = self.store()
        sqla.event.listen(sqla.engine.Engine, "before_cursor_execute", capture)
        try:
            read_inventory(store.primary, _factories)
        finally:
            sqla.event.remove(sqla.engine.Engine, "before_cursor_execute", capture)

        touching = [
            s
            for s in statements
            if any(re.search(rf'\b"?{t}"?\b', s) for t in VALUE_TABLES)
            and not s.startswith("PRAGMA")
        ]
        self.assertGreater(len(touching), 0)
        for statement in touching:
            self.assertIn("count(*)", statement)
            self.assertIn("GROUP BY", statement)


class TestReplicatedDivergence(_Stores):
    """Test 7: a replicated row changed on one shard only is named, with its shard."""

    def _diverged(self, statements, shards=2):
        inventory = self.inventory(extra_sql=statements, shards=shards)
        return inventory, {
            n: [p for p in c.problems if p.startswith("replicated-divergence")]
            for n, c in inventory.classes.items()
            if len(c.problems) > 0
        }

    def test_a_changed_row(self):
        inventory, problems = self._diverged(
            {1: ["UPDATE routing_rule SET rule_threshold = -10.0 WHERE serial = 3"]}
        )
        self.assertEqual(set(problems), {"routing_rule"})
        (problem,) = problems["routing_rule"]
        self.assertIn("shard #1 differs from shard #0", problem)
        # the records are the lowest-serial shard's
        self.assertEqual(inventory["routing_rule"].records, self.base["routing_rule"])

    def test_a_changed_tag_set(self):
        inventory, problems = self._diverged(
            {
                1: [
                    "DELETE FROM Gadget_tags WHERE gadget_serial = 1 "
                    "AND tag_serial = 2"
                ]
            }
        )
        self.assertIn("Gadget", problems)
        self.assertIn("shard #1", problems["Gadget"][0])
        self.assertEqual(inventory["Gadget"].records, self.base["Gadget"])

    def test_a_changed_value_count(self):
        _, problems = self._diverged({1: ["DELETE FROM GadgetPart WHERE serial = 5"]})
        self.assertEqual(set(problems), {"Gadget"})
        self.assertIn("shard #1", problems["Gadget"][0])

    def test_the_right_shard_of_three(self):
        _, problems = self._diverged(
            {2: ["UPDATE routing_rule SET rule_threshold = -10.0 WHERE serial = 3"]},
            shards=3,
        )
        (problem,) = problems["routing_rule"]
        self.assertIn("shard #2 differs from shard #0", problem)
        self.assertNotIn("shard #1", problem)


class TestOldStoresAndOrphans(_Stores):
    """Test 8: each case is a named problem, and nothing else changes. On a three-shard store,
    whose shard 2 holds only replicated rows."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.three = records_of(cls.inventory(shards=3))

    def check(self, name, kind, shard, expected=None, cascade=None, **kwargs):
        """
        ``cascade``: class -> how many of its records name
        a row this case takes away, through a parent on another shard. Such a class's only
        problems are ``unresolved-parent``, and its records are the baseline's less exactly that
        many; nothing else about it changes.
        """
        cascade = cascade or {}
        inventory = self.inventory(shards=3, **kwargs)
        problems = [
            p
            for cls_name, c in inventory.classes.items()
            if cls_name not in cascade
            for p in c.problems
        ]
        self.assertEqual(len(problems), 1, problems)
        self.assertEqual(kinds(inventory[name].problems), [kind])
        self.assertIn(f"shard #{shard}", inventory[name].problems[0])
        after = records_of(inventory)
        for other, lost in cascade.items():
            self.assertEqual(
                set(kinds(inventory[other].problems)), {"unresolved-parent"}
            )
            self.assertLessEqual(set(after[other]), set(self.three[other]))
            self.assertEqual(len(after[other]), len(self.three[other]) - lost)
        if expected is None:
            self.assertEqual(changed(self.three, after), set(cascade))
        else:
            self.assertEqual(changed(self.three, after), {name} | set(cascade))
            self.assertEqual(after[name], expected)
        return inventory[name].problems[0]

    def test_an_orphan_value_row(self):
        problem = self.check(
            "Trace",
            "orphan-value",
            0,
            extra_sql={
                0: [
                    "INSERT INTO TraceStep (serial, trace_serial, step_index, step_value) "
                    "VALUES (9001, 999, 1, 0.0)"
                ]
            },
        )
        self.assertIn("999", problem)

    def test_a_tag_row_whose_parent_is_missing(self):
        problem = self.check(
            "Trace",
            "orphan-tag",
            0,
            extra_sql={
                0: [
                    "INSERT INTO Trace_tags (trace_serial, tag_serial) "
                    "VALUES (999, 1)"
                ]
            },
        )
        self.assertIn("999", problem)

    def test_a_tag_row_whose_tag_is_missing(self):
        problem = self.check(
            "Trace",
            "orphan-tag",
            1,
            extra_sql={
                1: [
                    "INSERT INTO Trace_tags (trace_serial, tag_serial) "
                    "VALUES (2, 999)"
                ]
            },
        )
        self.assertIn("999", problem)

    def test_a_reference_that_cannot_be_resolved(self):
        replicated, sharded, keys = full_rows()
        row = copy.deepcopy(find_row(replicated, sharded, "Trace", 1))
        row.update(serial=77, frame_serial=999)
        sharded[0]["Trace"].append(row)
        problem = self.check(
            "Trace",
            "unresolved-parent",
            0,
            replicated=replicated,
            sharded=sharded,
            shard_keys=keys,
        )
        self.assertIn("77", problem)
        self.assertIn("frame", problem)

    def test_an_unknown_cosmology_type(self):
        replicated, sharded, keys = full_rows()
        row = copy.deepcopy(find_row(replicated, sharded, "Gadget", 1))
        row.update(serial=9, frame_kind=7)
        replicated["Gadget"].append(row)
        inventory = self.inventory(
            shards=3, replicated=replicated, sharded=sharded, shard_keys=keys
        )
        problems = inventory["Gadget"].problems
        self.assertEqual(kinds(problems), ["unresolved-parent"] * 3)
        for shard, problem in enumerate(problems):
            self.assertIn(f"shard #{shard}", problem)
            self.assertIn("frame", problem)
        self.assertEqual(records_of(inventory), self.three)


class TestDuplicates(_Stores):
    """Test 9: two records with the same key and tags are a named problem, and both are kept."""

    def _duplicate(self, table, serial, new_serial, shard, tag_table=None, column=None):
        replicated, sharded, keys = full_rows()
        row = copy.deepcopy(find_row(replicated, sharded, table, serial))
        row["serial"] = new_serial
        target = replicated if shard is None else sharded[shard]
        target.setdefault(table, []).append(row)
        if tag_table is not None:
            for rows in [replicated] + list(sharded.values()):
                for tag in [t for t in rows.get(tag_table, []) if t[column] == serial]:
                    target.setdefault(tag_table, []).append(
                        dict(tag, **{column: new_serial})
                    )
        return self.inventory(replicated=replicated, sharded=sharded, shard_keys=keys)

    def test_on_one_shard(self):
        inventory = self._duplicate("Trace", 1, 9, 0, "Trace_tags", "trace_serial")
        self.assertEqual(kinds(inventory["Trace"].problems), ["duplicate"])
        self.assertIn("#0/1", inventory["Trace"].problems[0])
        self.assertIn("#0/9", inventory["Trace"].problems[0])
        self.assertEqual(
            inventory["Trace"].count,
            self.baseline["Trace"].count + 1,
        )

    def test_across_shards(self):
        # A copy of a record on shard 1 is the same record only if shard 1 holds the same chain:
        # every same-shard parent it names, with theirs, copied there under their own serials.
        # Trace 1's parents (its keypoint and its frame) are replicated, so its chain is empty
        replicated, sharded, keys = full_rows()
        for table, column in ():
            sharded[1].setdefault(table, []).extend(
                copy.deepcopy(row) for row in sharded[0][table] if row[column] == 1
            )
        row = copy.deepcopy(find_row(replicated, sharded, "Trace", 1))
        row["serial"] = 9
        sharded[1]["Trace"].append(row)
        for tag in [t for t in sharded[0]["Trace_tags"] if t["trace_serial"] == 1]:
            sharded[1]["Trace_tags"].append(dict(tag, trace_serial=9))
        inventory = self.inventory(
            replicated=replicated, sharded=sharded, shard_keys=keys
        )
        self.assertEqual(kinds(inventory["Trace"].problems), ["duplicate"])
        self.assertIn("#1/9", inventory["Trace"].problems[0])

    def test_a_replicated_class(self):
        inventory = self._duplicate("routing_rule", 1, 4, None)
        self.assertEqual(kinds(inventory["routing_rule"].problems), ["duplicate"])
        self.assertEqual(inventory["routing_rule"].count, 4)

    def test_other_tags_are_not_a_duplicate(self):
        replicated, sharded, keys = full_rows()
        row = copy.deepcopy(find_row(replicated, sharded, "Trace", 1))
        row["serial"] = 9
        sharded[0]["Trace"].append(row)
        inventory = self.inventory(
            replicated=replicated, sharded=sharded, shard_keys=keys
        )
        self.assertEqual(inventory.problems, ())


class TestReadOnlyAndNoRay(_Stores):
    """Test 10: the reader's never-writes check across a full read_inventory, and no Ray."""

    def test_read_inventory_writes_nothing(self):
        store = self.store()
        before = file_state(store.directory)
        inventory = read_inventory(store.primary, _factories)
        self.assertGreater(inventory["Sample"].count, 0)
        after = file_state(store.directory)
        self.assertEqual(before, after)
        self.assertFalse(
            any(n.endswith(("-journal", "-wal", "-shm")) for n in after[0])
        )

    def test_no_ray(self):
        store = self.store()
        code = (
            "import json, sys\n"
            "from datastorekit.store_inventory import read_inventory\n"
            "from datastorekit.tests.client.registry import factories\n"
            "inventory = read_inventory(sys.argv[1], factories)\n"
            "import ray\n"
            "print(json.dumps({'ray': ray.is_initialized(), "
            "'sample': inventory['Sample'].count}))\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", code, str(store.primary)],
            cwd=str(self.root),
            env=dict(os.environ, PYTHONPATH=str(REPO_ROOT)),
            capture_output=True,
            text=True,
            timeout=300,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(report, {"ray": False, "sample": 3})


if __name__ == "__main__":
    unittest.main()
