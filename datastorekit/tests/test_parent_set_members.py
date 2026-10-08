"""
A parent set's second member is read (extraction prompt 04b §2.6; it closes
``[04a-no-test-pins-a-second-parent-set-member]``).

The neutral ``Weave`` declares one parent set, ``strands``, whose member rows (``Weave_members``)
name two parents: ``anchor``, a ``Tessera``, and ``origin``, a ``Trace``. The inventory keeps a
set's members in the order the spec declares them, and a record's set in that order. The ported
tests read only the first member: ``IDENTITY`` varies strand 701's ``anchor``, and
``test_the_full_store_resolves_no_absent_parent_as_unresolved`` walks the field ``anchor``. These
tests pin the second:

1. ``Weave``'s ``parent_sets["strands"]`` holds both members, ``anchor`` then ``origin``, each
   with its class;
2. on ``build_full_store``, changing the ``origin`` of one member row (``Weave_members`` 702)
   changes ``Weave``'s records, and no other class's, with no problem.

No Ray; stores are built in temporary directories.
"""

import tempfile
import unittest
from pathlib import Path

from datastorekit.store_inventory import read_inventory
from datastorekit.tests.client.registry import factories
from datastorekit.tests.real_store_fixtures import build_full_store, full_rows, vary_row

# the member row varied, its column, and the Trace it is pointed at in place of its own
MEMBER_ROW = 702
MEMBER_COLUMN = "origin_serial"
OTHER_ORIGIN = 1


class TestTheSecondMember(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls._tmp.name).resolve()
        cls.baseline = cls.inventory("baseline")

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    @classmethod
    def inventory(cls, name, **kwargs):
        directory = cls.root / name
        directory.mkdir()
        return read_inventory(build_full_store(directory, **kwargs).primary, factories)

    def test_the_set_declares_both_members_in_order(self):
        self.assertEqual(
            [("anchor", "Tessera"), ("origin", "Trace")],
            list(self.baseline["Weave"].parent_sets["strands"].items()),
        )

    def test_varying_the_second_member_changes_only_the_weave(self):
        replicated, sharded, keys = full_rows()
        vary_row(
            replicated,
            sharded,
            "Weave_members",
            MEMBER_ROW,
            MEMBER_COLUMN,
            OTHER_ORIGIN,
        )
        varied = self.inventory(
            "varied", replicated=replicated, sharded=sharded, shard_keys=keys
        )
        before = {n: c.records for n, c in self.baseline.classes.items()}
        after = {n: c.records for n, c in varied.classes.items()}
        self.assertEqual(
            {"Weave"}, {n for n in before if before[n] != after[n]}, "changed classes"
        )
        self.assertEqual((), varied.problems)


if __name__ == "__main__":
    unittest.main()
