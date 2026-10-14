"""
The store fingerprint, ``datastorekit/store_fingerprint.py``: ``fingerprint_of``,
``compare_fingerprints``, ``listing_lines`` and ``ENCODING_FORMAT``, on the full real store of
``real_store_fixtures.build_full_store``. Restated, in substance, from the source repository's
fingerprint tests 1–6 (``PROVENANCE.md``), over the neutral store, with tests 7 and 8 added for the
package's argument and imports.

1. the fingerprint is physical: other serials, other shards, the same fingerprint;
2. a difference is localised to the classes and tag sets that changed, and no other; an orphan is
   a ``problems`` entry and nothing else;
3. what is not content (timestamps) does not matter;
4. the fingerprint of ``build_full_store()`` is the golden file for (``NEUTRAL_FORMAT``,
   ``ENCODING_FORMAT``); its shape, and its overall digest recomputed; ``taken`` is outside every
   digest;
5. a listing's lines hash to the digests it lists, and its first line's words are, by position,
   the client's format, the digest and the encoding format;
6. fingerprints of different client formats, or of different encoding formats, are not compared;
7. the client's format is a required ``int`` of at least 1, positional or by keyword;
8. the three functions change neither their arguments nor the store, and importing the module
   loads no Ray.

No test here starts Ray or constructs a ``ShardedPool``, and every store is in a temporary
directory.
"""

import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

import datastorekit
from datastorekit.store_fingerprint import (
    ENCODING_FORMAT,
    compare_fingerprints,
    fingerprint_of,
    listing_lines,
)
from datastorekit.store_inventory import canonical_json, read_inventory
from datastorekit.tests.client.registry import factories as _factories
from datastorekit.tests.real_store_fixtures import (
    FIXED_TIMESTAMP,
    _schema_tables,
    build_full_store,
    file_state,
    full_rows,
    relabel_serials,
)

# stands for a client's fingerprint_format. It is bumped, with a new golden file beside the old
# one, when the neutral client's specs or its full store change what the fingerprint sees
NEUTRAL_FORMAT = 1

# the golden fingerprint of build_full_store() at (NEUTRAL_FORMAT, ENCODING_FORMAT); a golden file
# is never rewritten
GOLDEN = (
    Path(__file__).resolve().parent
    / "data"
    / f"store_fingerprint-neutral-{NEUTRAL_FORMAT}-encoding-{ENCODING_FORMAT}.json"
)

PACKAGE_DIR = Path(datastorekit.__file__).resolve().parent

# the text of the source's entry for a client-format mismatch, for formats 1 and 2, verbatim
FORMAT_TEXT_1_2 = (
    "the recorded fingerprint is format 1 and this one is format 2; fingerprints of different "
    "formats are not compared. Recompute both from the stores"
)

RUN = ("fixture-run",)


def tearDownModule():
    ray = sys.modules.get("ray")
    if ray is not None and ray.is_initialized():
        raise AssertionError("Ray was initialised by test_store_fingerprint")


def without_taken(fingerprint) -> dict:
    out = dict(fingerprint)
    out.pop("taken", None)
    return out


def entries(fingerprint) -> dict:
    """(class, None) -> (count, digest) for each class, and (class, tags) -> (count, digest) for
    each of its tag sets."""
    out = {}
    for name, entry in fingerprint["classes"].items():
        out[(name, None)] = (entry["count"], entry["digest"])
        for tag_set in entry["tag_sets"]:
            out[(name, tuple(tag_set["tags"]))] = (tag_set["count"], tag_set["digest"])
    return out


def changed_entries(before, after) -> set:
    a, b = entries(before), entries(after)
    return {key for key in set(a) | set(b) if a.get(key) != b.get(key)}


def sha256_lines(lines) -> str:
    return hashlib.sha256("".join(line + "\n" for line in lines).encode()).hexdigest()


def parse_listing(text: str):
    """{"words", "classes": {name: {"count", "digest", "lines", "tag_sets": {tags: {"count",
    "digest", "lines"}}}}} from a listing's text, each header read by word position."""
    out = {"classes": {}}
    cls = tag_set = None
    for line in text.splitlines():
        if line.startswith("# fingerprint_format "):
            out["words"] = line.split()
        elif line.startswith("# class "):
            _, _, name, _, count, _, digest = line.split()
            cls = {"count": int(count), "digest": digest, "lines": [], "tag_sets": {}}
            out["classes"][name] = cls
        elif line.startswith("# tags "):
            body, _, rest = line[len("# tags ") :].rpartition(" count ")
            count, _, digest = rest.split()
            tag_set = {"count": int(count), "digest": digest, "lines": []}
            cls["tag_sets"][tuple(json.loads(body))] = tag_set
        else:
            cls["lines"].append(line)
            tag_set["lines"].append(line)
    return out


class _FullStores(unittest.TestCase):
    """A temporary directory, full stores built in it, each in its own directory, and the
    baseline's inventory and fingerprint."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.top = Path(cls._tmp.name).resolve()
        cls._count = 0
        cls.baseline_inventory = cls.inventory()
        cls.baseline = fingerprint_of(cls.baseline_inventory, NEUTRAL_FORMAT)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    @classmethod
    def store(cls, **kwargs):
        cls._count += 1
        directory = cls.top / f"store-{cls._count}"
        directory.mkdir()
        return build_full_store(directory, **kwargs)

    @classmethod
    def inventory(cls, **kwargs):
        return read_inventory(cls.store(**kwargs).primary, _factories)

    @classmethod
    def fingerprint(cls, **kwargs):
        return fingerprint_of(cls.inventory(**kwargs), NEUTRAL_FORMAT)


class TestPhysical(_FullStores):
    """Test 1: the same rows under other serials, and on other shards, give the same
    fingerprint, and compare equal."""

    def test_other_serials_and_other_shards(self):
        relabelled = relabel_serials(*full_rows(), offset=100)
        replicated, sharded, keys = full_rows()
        third = (
            replicated,
            {0: {}, 1: sharded[1], 2: sharded[0]},
            {k: {0: 2, 1: 1}[s] for k, s in keys.items()},
        )
        replicated, sharded, keys = relabel_serials(*full_rows(), offset=37)
        swapped = (
            replicated,
            {0: sharded[1], 1: sharded[0]},
            {k: 1 - s for k, s in keys.items()},
        )
        cases = {
            "other serials": (relabelled, 2),
            "sharded rows on a third shard": (third, 3),
            "other serials, shards swapped": (swapped, 2),
        }
        for label, ((replicated, sharded, keys), shards) in cases.items():
            with self.subTest(case=label):
                other = self.fingerprint(
                    replicated=replicated,
                    sharded=sharded,
                    shard_keys=keys,
                    shards=shards,
                )
                self.assertEqual(without_taken(other), without_taken(self.baseline))
                self.assertEqual(compare_fingerprints(self.baseline, other), [])


class TestLocalised(_FullStores):
    """Test 2: each change moves exactly the entries it names, and the comparison names exactly
    those tag sets.

    The expected sets are read from the full store's rows (``real_store_fixtures``): every
    Sample, Trace and Weave is on shard 0 but Sample 4 and Trace 2. Sample 2 carries the run tag
    alone, as Sample 4 does, and no class references a Sample. Trace 3 carries the run tag and
    ``grid-B``, and is the only Trace that does; Trace 4 carries the run tag alone, and is the
    only one that does; Traces 1 and 2 carry the run tag and ``grid-A``. A reference to a tagged
    parent covers its tags, and Weave 1 names Trace 4 (its ``trace``) and Trace 3 (a strand's
    origin), so a tag added to a Trace changes the Weave too. Its value count and its validated
    flag are not in the reference, so a Trace's steps and flag change the Trace alone.
    """

    def assertLocalised(self, after_inventory, expected, counts):
        """The changed entries are exactly ``expected``, a set of (class, None) and (class,
        tags); every class it does not name has the baseline's records; the overall digest
        changed and the problems did not. The comparison is one ``tag_set`` entry per tag set in
        ``expected``, with the (recorded, current) counts ``counts`` gives it."""
        after = fingerprint_of(after_inventory, NEUTRAL_FORMAT)
        named = {name for name, _ in expected}
        for name in self.baseline_inventory.classes:
            if name not in named:
                self.assertEqual(
                    after_inventory[name].records,
                    self.baseline_inventory[name].records,
                    name,
                )
            else:
                self.assertNotEqual(
                    after_inventory[name].records,
                    self.baseline_inventory[name].records,
                    f"{name}: the change changed nothing",
                )
        self.assertEqual(changed_entries(self.baseline, after), expected)
        self.assertNotEqual(after["digest"], self.baseline["digest"])
        self.assertEqual(after["problems"], self.baseline["problems"])

        comparison = compare_fingerprints(self.baseline, after)
        tag_sets = {(name, tags) for name, tags in expected if tags is not None}
        self.assertEqual(
            {(e["kind"], e["class"], tuple(e["tags"])) for e in comparison},
            {("tag_set", name, tags) for name, tags in tag_sets},
        )
        self.assertEqual(len(comparison), len(tag_sets))
        self.assertEqual(
            {
                (e["class"], tuple(e["tags"])): (e["recorded"], e["current"])
                for e in comparison
            },
            counts,
        )
        return after

    def test_deleting_one_sharded_record(self):
        after = self.assertLocalised(
            self.inventory(
                extra_sql={
                    0: [
                        "DELETE FROM Sample WHERE serial = 2",
                        "DELETE FROM Sample_tags WHERE sample_serial = 2",
                        "DELETE FROM Sample_members WHERE sample_serial = 2",
                    ]
                }
            ),
            {("Sample", None), ("Sample", RUN)},
            {("Sample", RUN): (2, 1)},
        )
        self.assertEqual(self.baseline["classes"]["Sample"]["count"], 3)
        self.assertEqual(after["classes"]["Sample"]["count"], 2)

    def test_deleting_the_row_alone_is_also_a_problem_entry(self):
        """The row goes and its tag and member rows stay, so the one content difference comes with
        a problem entry for each."""
        after = self.fingerprint(extra_sql={0: ["DELETE FROM Sample WHERE serial = 2"]})
        self.assertEqual(
            changed_entries(self.baseline, after), {("Sample", None), ("Sample", RUN)}
        )
        self.assertEqual(
            after["problems"], {"Sample": {"orphan-member": 1, "orphan-tag": 1}}
        )
        comparison = compare_fingerprints(self.baseline, after)
        self.assertEqual(
            [(e["kind"], e["class"]) for e in comparison],
            [("tag_set", "Sample"), ("problems", "Sample"), ("problems", "Sample")],
        )
        self.assertEqual((comparison[0]["recorded"], comparison[0]["current"]), (2, 1))
        self.assertIn(
            "orphan-member problems: 0 recorded, 1 now", comparison[1]["text"]
        )
        self.assertIn("orphan-tag problems: 0 recorded, 1 now", comparison[2]["text"])

    def test_adding_a_tag_to_one_record(self):
        after = self.assertLocalised(
            self.inventory(
                extra_sql={
                    0: [
                        "INSERT INTO Sample_tags (sample_serial, tag_serial) VALUES (2, 5)"
                    ]
                }
            ),
            {
                ("Sample", None),
                ("Sample", RUN),
                ("Sample", ("fixture-run", "weave-tag")),
            },
            {
                ("Sample", RUN): (2, 1),
                ("Sample", ("fixture-run", "weave-tag")): (None, 1),
            },
        )
        self.assertEqual(after["classes"]["Sample"]["count"], 3)

    def test_adding_a_tag_to_a_referenced_record_reaches_its_child(self):
        """Trace 4 is Weave 1's ``trace``: a tag added to it moves the Weave's entries too."""
        self.assertLocalised(
            self.inventory(
                extra_sql={
                    0: [
                        "INSERT INTO Trace_tags (trace_serial, tag_serial) VALUES (4, 2)"
                    ]
                }
            ),
            {
                ("Trace", None),
                ("Trace", RUN),
                ("Trace", ("fixture-run", "grid-A")),
                ("Weave", None),
                ("Weave", ("fixture-run", "weave-tag")),
            },
            {
                ("Trace", RUN): (1, None),
                ("Trace", ("fixture-run", "grid-A")): (2, 3),
                ("Weave", ("fixture-run", "weave-tag")): (1, 1),
            },
        )

    def test_deleting_one_value_row(self):
        after = self.assertLocalised(
            self.inventory(extra_sql={0: ["DELETE FROM TraceStep WHERE serial = 32"]}),
            {("Trace", None), ("Trace", ("fixture-run", "grid-B"))},
            {("Trace", ("fixture-run", "grid-B")): (1, 1)},
        )
        self.assertEqual(
            after["classes"]["Trace"]["count"],
            self.baseline["classes"]["Trace"]["count"],
        )

    def test_flipping_one_validated_flag(self):
        self.assertLocalised(
            self.inventory(
                extra_sql={0: ["UPDATE Trace SET trace_validated = 1 WHERE serial = 3"]}
            ),
            {("Trace", None), ("Trace", ("fixture-run", "grid-B"))},
            {("Trace", ("fixture-run", "grid-B")): (1, 1)},
        )

    def test_an_orphan_value_row_is_a_problem_entry_only(self):
        after = self.fingerprint(
            extra_sql={
                0: [
                    "INSERT INTO TraceStep (serial, trace_serial, step_index, step_value) "
                    "VALUES (9001, 999, 1, 0.0)"
                ]
            }
        )
        self.assertEqual(after["problems"], {"Trace": {"orphan-value": 1}})
        self.assertEqual(changed_entries(self.baseline, after), set())
        self.assertEqual(after["digest"], self.baseline["digest"])
        comparison = compare_fingerprints(self.baseline, after)
        self.assertEqual(
            [(e["kind"], e["class"], e["tags"]) for e in comparison],
            [("problems", "Trace", None)],
        )
        self.assertEqual((comparison[0]["recorded"], comparison[0]["current"]), (0, 1))
        self.assertIn("orphan-value problems: 0 recorded, 1 now", comparison[0]["text"])


class TestNotContent(_FullStores):
    """Test 3: every timestamp changed gives the same fingerprint, and no record line holds one."""

    def test_timestamps(self):
        replicated, sharded, keys = full_rows()
        tables = _schema_tables()
        stamp = datetime(2031, 2, 3, 4, 5, 6)
        changed = 0
        for rows in [replicated] + list(sharded.values()):
            for table, table_rows in rows.items():
                if "timestamp" in tables[table].c:
                    for row in table_rows:
                        row["timestamp"] = stamp
                        changed += 1
        self.assertGreater(changed, 0)
        inventory = self.inventory(
            replicated=replicated, sharded=sharded, shard_keys=keys
        )
        self.assertEqual(inventory["Sample"].earliest_timestamp, stamp)
        after = fingerprint_of(inventory, NEUTRAL_FORMAT)
        self.assertEqual(without_taken(after), without_taken(self.baseline))
        self.assertEqual(compare_fingerprints(self.baseline, after), [])

    def test_no_timestamp_is_in_any_record_line(self):
        self.assertEqual(
            self.baseline_inventory["Sample"].earliest_timestamp, FIXED_TIMESTAMP
        )
        lines = list(listing_lines(self.baseline_inventory, self.baseline))
        for text in (str(FIXED_TIMESTAMP), FIXED_TIMESTAMP.isoformat(), "2026-09-24"):
            for line in lines:
                self.assertNotIn(text, line)


class TestGolden(_FullStores):
    """Test 4: the fingerprint of ``build_full_store()`` is the golden file, its shape, its
    overall digest recomputed, and ``taken`` outside every digest."""

    def test_the_golden_fingerprint(self):
        self.assertTrue(GOLDEN.is_file(), GOLDEN)
        golden = json.loads(GOLDEN.read_text())
        self.assertEqual(golden["fingerprint_format"], NEUTRAL_FORMAT)
        self.assertEqual(golden["encoding_format"], ENCODING_FORMAT)
        self.assertIsNone(golden["taken"])
        self.assertEqual(without_taken(self.baseline), without_taken(golden))
        # and it is deterministic: a second build gives the same
        self.assertEqual(without_taken(self.fingerprint()), without_taken(golden))

    def test_the_shape_and_the_overall_digest(self):
        fp = self.baseline
        self.assertEqual(
            set(fp),
            {
                "fingerprint_format",
                "encoding_format",
                "classes",
                "digest",
                "problems",
                "taken",
            },
        )
        self.assertEqual(fp["fingerprint_format"], NEUTRAL_FORMAT)
        self.assertEqual(fp["encoding_format"], ENCODING_FORMAT)
        self.assertEqual(ENCODING_FORMAT, 1)
        self.assertIsNone(fp["taken"])
        self.assertEqual(fp["problems"], {})
        self.assertEqual(list(fp["classes"]), list(self.baseline_inventory.classes))
        for name, entry in fp["classes"].items():
            with self.subTest(cls=name):
                self.assertEqual(set(entry), {"count", "digest", "tag_sets"})
                self.assertEqual(entry["count"], self.baseline_inventory[name].count)
                self.assertEqual(
                    sum(t["count"] for t in entry["tag_sets"]), entry["count"]
                )
                if not self.baseline_inventory[name].tagged:
                    self.assertEqual([t["tags"] for t in entry["tag_sets"]], [[]])
        self.assertEqual(
            {
                name: [t["tags"] for t in entry["tag_sets"]]
                for name, entry in fp["classes"].items()
                if self.baseline_inventory[name].tagged
            },
            {
                "Gadget": [["fixture-run"], ["fixture-run", "grid-A"]],
                "Sample": [["fixture-run"], ["fixture-run", "grid-A"]],
                "Trace": [
                    ["fixture-run"],
                    ["fixture-run", "grid-A"],
                    ["fixture-run", "grid-B"],
                ],
                "Weave": [["fixture-run", "weave-tag"]],
            },
        )
        # the overall digest hashes the client's format and each class's count and digest, and
        # nothing else: not the encoding format
        overall = {
            "fingerprint_format": NEUTRAL_FORMAT,
            "classes": {
                name: {"count": entry["count"], "digest": entry["digest"]}
                for name, entry in fp["classes"].items()
            },
        }
        self.assertEqual(
            fp["digest"],
            hashlib.sha256(canonical_json(overall).encode("utf-8")).hexdigest(),
        )

    def test_taken_is_copied_and_outside_every_digest(self):
        taken = {"when": "now", "by": "test", "dirty": True}
        given = copy.deepcopy(taken)
        with_taken = fingerprint_of(self.baseline_inventory, NEUTRAL_FORMAT, given)
        self.assertEqual(with_taken["taken"], taken)
        self.assertIsNot(with_taken["taken"], given)
        self.assertEqual(given, taken)
        self.assertEqual(without_taken(with_taken), without_taken(self.baseline))
        self.assertEqual(compare_fingerprints(self.baseline, with_taken), [])
        self.assertEqual(compare_fingerprints(with_taken, self.baseline), [])


class TestListing(_FullStores):
    """Test 5: the lines a listing writes for each class and tag set hash to its digests."""

    def test_the_listing_hashes_to_the_fingerprint(self):
        text = "".join(
            line + "\n"
            for line in listing_lines(self.baseline_inventory, self.baseline)
        )
        listing = parse_listing(text)
        self.assertEqual(
            listing["words"],
            [
                "#",
                "fingerprint_format",
                str(NEUTRAL_FORMAT),
                "digest",
                self.baseline["digest"],
                "encoding_format",
                str(ENCODING_FORMAT),
            ],
        )
        # read by position, as a reader of the first line reads it
        words = listing["words"]
        self.assertEqual(int(words[2]), self.baseline["fingerprint_format"])
        self.assertEqual(words[4], self.baseline["digest"])
        self.assertEqual(int(words[6]), self.baseline["encoding_format"])
        self.assertEqual(list(listing["classes"]), list(self.baseline["classes"]))
        for name, entry in self.baseline["classes"].items():
            listed = listing["classes"][name]
            with self.subTest(cls=name):
                self.assertEqual(listed["count"], entry["count"])
                self.assertEqual(listed["digest"], entry["digest"])
                self.assertEqual(len(listed["lines"]), entry["count"])
                # the class digest is over its records in canonical order: its lines, sorted
                self.assertEqual(sha256_lines(sorted(listed["lines"])), entry["digest"])
                self.assertEqual(
                    set(listed["tag_sets"]),
                    {tuple(t["tags"]) for t in entry["tag_sets"]},
                )
                for tag_set in entry["tag_sets"]:
                    listed_set = listed["tag_sets"][tuple(tag_set["tags"])]
                    self.assertEqual(listed_set["count"], tag_set["count"])
                    self.assertEqual(listed_set["digest"], tag_set["digest"])
                    self.assertEqual(len(listed_set["lines"]), tag_set["count"])
                    self.assertEqual(
                        sha256_lines(listed_set["lines"]), tag_set["digest"]
                    )


class TestVersions(_FullStores):
    """Test 6: two fingerprints of different client formats, or of different encoding formats,
    are not compared."""

    _ABSENT = object()

    def made(self, fmt, encoding=ENCODING_FORMAT):
        """A fingerprint built by hand, as the source's version test builds one, with
        ``encoding_format`` (left out when ``encoding`` is ``_ABSENT``)."""
        out = {
            "fingerprint_format": fmt,
            "classes": {"A": {"count": fmt, "digest": str(fmt) * 64, "tag_sets": []}},
            "digest": str(fmt) * 64,
            "problems": {"A": {"duplicate": fmt}},
            "taken": {"when": str(fmt)},
        }
        if encoding is not self._ABSENT:
            out["encoding_format"] = encoding
        return out

    def test_the_versions(self):
        # different client formats: the source's one entry, verbatim
        comparison = compare_fingerprints(self.made(1), self.made(2))
        self.assertEqual(len(comparison), 1)
        self.assertEqual(comparison[0]["kind"], "format")
        self.assertEqual((comparison[0]["class"], comparison[0]["tags"]), (None, None))
        self.assertEqual((comparison[0]["recorded"], comparison[0]["current"]), (1, 2))
        self.assertIn("Recompute both", comparison[0]["text"])
        self.assertEqual(comparison[0]["text"], FORMAT_TEXT_1_2)

        # different encoding formats
        comparison = compare_fingerprints(self.made(1, 1), self.made(1, 2))
        self.assertEqual(len(comparison), 1)
        self.assertEqual(comparison[0]["kind"], "encoding")
        self.assertEqual((comparison[0]["class"], comparison[0]["tags"]), (None, None))
        self.assertEqual((comparison[0]["recorded"], comparison[0]["current"]), (1, 2))
        self.assertIn("encoding format 1", comparison[0]["text"])
        self.assertIn("Recompute both", comparison[0]["text"])

        # both: two entries, the client's format first
        comparison = compare_fingerprints(self.made(1, 1), self.made(2, 2))
        self.assertEqual([e["kind"] for e in comparison], ["format", "encoding"])
        self.assertEqual(
            [(e["recorded"], e["current"]) for e in comparison], [(1, 2), (1, 2)]
        )

        # a recorded fingerprint with no encoding format
        comparison = compare_fingerprints(
            self.made(1, self._ABSENT), self.made(1, ENCODING_FORMAT)
        )
        self.assertEqual(
            [(e["kind"], e["recorded"], e["current"]) for e in comparison],
            [("encoding", None, ENCODING_FORMAT)],
        )

        # equal versions are compared as before
        self.assertEqual(compare_fingerprints(self.made(1), self.made(1)), [])

    def test_another_encoding_of_the_same_store(self):
        restamped = dict(self.baseline, encoding_format=ENCODING_FORMAT + 1)
        self.assertEqual(restamped["digest"], self.baseline["digest"])
        self.assertEqual(restamped["classes"], self.baseline["classes"])
        comparison = compare_fingerprints(self.baseline, restamped)
        self.assertEqual(
            [(e["kind"], e["recorded"], e["current"]) for e in comparison],
            [("encoding", ENCODING_FORMAT, ENCODING_FORMAT + 1)],
        )


class TestTheFormatArgument(_FullStores):
    """Test 7: the client's format is a required ``int`` of at least 1, positional or by
    keyword. Each refusal is the function's own, naming the function, the argument and the
    value."""

    def test_positional_or_keyword(self):
        self.assertEqual(
            fingerprint_of(self.baseline_inventory, 1),
            fingerprint_of(self.baseline_inventory, fingerprint_format=1),
        )
        self.assertEqual(
            fingerprint_of(self.baseline_inventory, NEUTRAL_FORMAT), self.baseline
        )

    def test_refusals(self):
        with self.assertRaisesRegex(TypeError, "fingerprint_format"):
            fingerprint_of(self.baseline_inventory)
        for value in (True, "1", 1.0, {"when": "now"}):
            with self.subTest(value=value):
                with self.assertRaisesRegex(
                    TypeError, r"^fingerprint_of\(\): fingerprint_format must be an int"
                ) as caught:
                    fingerprint_of(self.baseline_inventory, value)
                self.assertIn(repr(value), str(caught.exception))
        for value in (0, -1):
            with self.subTest(value=value):
                with self.assertRaisesRegex(
                    ValueError,
                    r"^fingerprint_of\(\): fingerprint_format must be at least 1",
                ) as caught:
                    fingerprint_of(self.baseline_inventory, value)
                self.assertIn(repr(value), str(caught.exception))
        # refused before the inventory is read
        with self.assertRaisesRegex(TypeError, r"^fingerprint_of\(\)"):
            fingerprint_of(object(), "1")

    def test_another_format_moves_only_the_overall_digest(self):
        other = fingerprint_of(self.baseline_inventory, 2)
        self.assertEqual(other["fingerprint_format"], 2)
        self.assertEqual(other["classes"], self.baseline["classes"])
        self.assertEqual(entries(other), entries(self.baseline))
        self.assertNotEqual(other["digest"], self.baseline["digest"])


class TestPurity(_FullStores):
    """Test 8: the three functions change neither their arguments nor the store, and importing
    the module loads no Ray."""

    def test_arguments_and_store_unchanged(self):
        store = self.store()
        inventory = read_inventory(store.primary, _factories)
        before = file_state(store.directory)
        inventory_copy = copy.deepcopy(inventory)
        taken = {"when": "now"}
        taken_copy = copy.deepcopy(taken)

        fp = fingerprint_of(inventory, NEUTRAL_FORMAT, taken)
        self.assertEqual(inventory, inventory_copy)
        self.assertEqual(taken, taken_copy)

        # a comparison that reaches every branch of the content comparison
        other = copy.deepcopy(fp)
        other["classes"]["Trace"]["digest"] = "0" * 64
        other["classes"]["Trace"]["tag_sets"][0]["digest"] = "0" * 64
        other["classes"].pop("Weave")
        other["digest"] = "0" * 64
        other["problems"] = {"Trace": {"orphan-value": 1}}
        fp_copy, other_copy = copy.deepcopy(fp), copy.deepcopy(other)
        self.assertGreater(len(compare_fingerprints(fp, other)), 0)
        self.assertEqual((fp, other), (fp_copy, other_copy))

        lines = list(listing_lines(inventory, fp))
        self.assertGreater(len(lines), 0)
        self.assertEqual(inventory, inventory_copy)
        self.assertEqual(fp, fp_copy)

        self.assertEqual(file_state(store.directory), before)

    def test_importing_the_module_loads_no_ray(self):
        code = (
            "import sys; import datastorekit.store_fingerprint; "
            "print(sorted(m for m in ('ray',) if m in sys.modules))"
        )
        env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
        env["PYTHONPATH"] = str(PACKAGE_DIR.parent)
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            env=env,
            cwd=tempfile.gettempdir(),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[]")


if __name__ == "__main__":
    unittest.main()
