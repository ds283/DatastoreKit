"""
The fingerprint of a store: a small, comparable summary of what its structured inventory holds.

A fingerprint is a pure function of a ``StoreInventory``, what ``store_inventory.read_inventory``
returns. It reads nothing, opens nothing and needs no Ray. ``fingerprint_of`` makes one,
``compare_fingerprints`` says how two differ, and ``listing_lines`` writes out the lines a
fingerprint's digests are taken over.

**What it holds.** A record's canonical line is ``record.canonical_json()``, which is
``canonical_json(record.as_json())``: its key, its tags, ``validated`` and ``value_count``, and no
timestamp. A digest is the SHA-256 of records' canonical lines, each followed by ``"\\n"``, in the
order the inventory gives, which is sorted by canonical JSON. So a listing written as those lines
hashes to the digests it lists, and filtering a class's lines to one tag set keeps them sorted.
Problems are counted by name beside the digests, never in them: their text names shards and
serials, which belong to one store and not to its content.

**Two versions.** A fingerprint carries two numbers, and two fingerprints are compared only when
both are equal:

- ``fingerprint_format`` is the **client's**. The client gives it to ``fingerprint_of``, and bumps
  it when what goes into its fingerprint changes: its factories' inventory specs, or its registry.
  It is in the object the overall digest hashes;
- ``encoding_format`` is **this package's**, ``ENCODING_FORMAT``. It versions how the package turns
  rows into records and canonical lines (``store_inventory``) and how this module digests,
  compares and lists them. It is beside the overall digest, and not in it. When it is bumped is
  stated beside the constant.

This module imports only the standard library and ``store_inventory``'s ``canonical_json``, at
module scope. ``store_inventory`` loads ``sqlalchemy``, and not Ray.
"""

import hashlib
from collections import Counter
from typing import Any, Mapping, Optional

from datastorekit.store_inventory import canonical_json

# The version of the encoding: how ``store_inventory`` makes a record and its canonical line from
# a store's rows, and how this module digests, compares and lists them. Every fingerprint records
# it as ``encoding_format``, beside the overall digest and outside the object that digest hashes.
#
# ENCODING_FORMAT is bumped by any change that can make the same store, read with the same specs
# and the same client format, give a different fingerprint, or make ``compare_fingerprints`` or
# ``listing_lines`` read one differently. That is, a change to:
#
# 1. what a record contains: ``Record.as_json``'s fields or their values, including
#    ``value_count`` and ``validated``;
# 2. how a leaf or a key becomes text: ``canonical``, ``canonical_json``, ``digest``;
# 3. how a reference becomes a key's value: ``reference_digest``, the parent-set digest, how a
#    polymorphic, nullable or cross-shard parent resolves;
# 4. which rows become records, and which shard's copy of a replicated class is used;
# 5. the order of a class's records, or how they are grouped into tag sets;
# 6. the names of the problems (a fingerprint counts problems by name);
# 7. how a digest is formed: ``_sha256_lines``, the per-tag-set grouping, the overall digest's
#    object;
# 8. the fingerprint's keys, or what ``compare_fingerprints`` and ``listing_lines`` read from it.
#
# A bump adds a new golden fingerprint of the neutral test store beside the old one, in the same
# commit, and never rewrites the old (``tests/data/``, each file named for the client format and
# the encoding format it was taken at). The release that carries a bump says so in its provenance
# record and in an addendum to every client's adoption checklist, since every client's
# fingerprints then differ from those it holds. A change that the neutral golden does not see is
# still a bump if it is in the list: the golden is a guard, not the rule. A change to a client's
# specs or registry is that client's ``fingerprint_format``, never ENCODING_FORMAT.
#
# Item 1 is read by the rule above it. A field added to ``Record.as_json`` that a record carries
# only where its class's spec declares what fills it (``extra_value_counts``, from
# ``InventorySpec.extra_values``) is not a bump: a store read with the same specs gives the same
# records. A client whose spec comes to declare it changes its own fingerprints, which is its
# ``fingerprint_format``.
ENCODING_FORMAT = 1


def _sha256_lines(lines) -> str:
    """SHA-256 (hex) of ``lines``, each followed by a newline."""
    hasher = hashlib.sha256()
    for line in lines:
        hasher.update(line.encode("utf-8"))
        hasher.update(b"\n")
    return hasher.hexdigest()


def _tag_sets(records) -> list:
    """``[(tags, lines)]``: each distinct tag set, sorted, with the canonical lines of the records
    that carry exactly that set, in the records' own order."""
    groups = {}
    for record in records:
        groups.setdefault(tuple(record.tags), []).append(record.canonical_json())
    return sorted(groups.items())


def fingerprint_of(
    inventory, fingerprint_format: int, taken: Optional[Mapping[str, Any]] = None
) -> dict:
    """
    The fingerprint of ``inventory``, what ``read_inventory`` returns, at the client's
    ``fingerprint_format``. Pure: it reads nothing.

    ``fingerprint_format`` is required, positionally or by keyword, and must be an ``int`` of at
    least 1: a ``bool`` or anything that is not an ``int`` raises ``TypeError``, and an ``int``
    below 1 ``ValueError``, before the inventory is read. The fingerprint is a dict of:

    - ``fingerprint_format``: ``fingerprint_format``, as given;
    - ``encoding_format``: ``ENCODING_FORMAT``. Outside every digest;
    - ``classes``: for every class, in the inventory's order, its ``count``, its ``digest`` over
      every record, and ``tag_sets``, one ``{"tags", "count", "digest"}`` per distinct tag set,
      sorted by tags. A class with no association table has one, with ``tags`` ``[]``; an empty
      class has none;
    - ``digest``: SHA-256 of ``canonical_json({"fingerprint_format", "classes": {name: {"count",
      "digest"}}})``;
    - ``problems``: per class that has any, the number of its named problems of each kind (the
      word before the first colon). Outside every digest;
    - ``taken``: ``taken``, the caller's mapping, copied, or ``None``. Outside every digest.
    """
    if isinstance(fingerprint_format, bool) or not isinstance(fingerprint_format, int):
        raise TypeError(
            f"fingerprint_of(): fingerprint_format must be an int, not "
            f"{type(fingerprint_format).__name__} {fingerprint_format!r}"
        )
    if fingerprint_format < 1:
        raise ValueError(
            f"fingerprint_of(): fingerprint_format must be at least 1, not "
            f"{fingerprint_format!r}"
        )

    classes = {}
    problems = {}
    for name, cls in inventory.classes.items():
        lines = [record.canonical_json() for record in cls.records]
        classes[name] = {
            "count": len(lines),
            "digest": _sha256_lines(lines),
            "tag_sets": [
                {
                    "tags": list(tags),
                    "count": len(group),
                    "digest": _sha256_lines(group),
                }
                for tags, group in _tag_sets(cls.records)
            ],
        }
        kinds = Counter(problem.split(":", 1)[0] for problem in cls.problems)
        if kinds:
            problems[name] = dict(sorted(kinds.items()))

    overall = {
        "fingerprint_format": fingerprint_format,
        "classes": {
            name: {"count": entry["count"], "digest": entry["digest"]}
            for name, entry in classes.items()
        },
    }
    return {
        "fingerprint_format": fingerprint_format,
        "encoding_format": ENCODING_FORMAT,
        "classes": classes,
        "digest": hashlib.sha256(canonical_json(overall).encode("utf-8")).hexdigest(),
        "problems": problems,
        "taken": dict(taken) if taken is not None else None,
    }


def _tags_text(tags) -> str:
    return "[" + ", ".join(tags) + "]"


def _difference(kind, name, tags, recorded, current, text) -> dict:
    return {
        "kind": kind,
        "class": name,
        "tags": None if tags is None else list(tags),
        "recorded": recorded,
        "current": current,
        "text": text,
    }


def _presence(recorded, current) -> str:
    if recorded is None:
        return "is only in the current fingerprint"
    return "is only in the recorded fingerprint"


def compare_fingerprints(recorded, current) -> list:
    """
    The differences between two fingerprints, one entry per difference. Pure.

    Two fingerprints are compared only if both versions are equal: the client's
    ``fingerprint_format`` and this package's ``encoding_format`` (a key that is absent is
    ``None``, so a fingerprint without ``encoding_format`` differs from one with it). If either
    differs, the answer is one entry per version that differs, ``format`` and then ``encoding``,
    and nothing else is compared, because the remedy is to recompute both from the stores.
    Otherwise each entry names the class, the tag set (or that a tag set, or a class, is present in
    only one) and the two counts, ``None`` where absent. Equal overall digests give no content
    entry. Differences in ``problems`` are entries of their own, compared whatever the digests say,
    because problems are outside every digest. ``taken`` is never compared. Each entry is
    ``{"kind", "class", "tags", "recorded", "current", "text"}``, ``kind`` being ``format``,
    ``encoding``, ``class``, ``tag_set``, ``digest`` or ``problems``.
    """
    versions = []
    recorded_format = recorded.get("fingerprint_format")
    current_format = current.get("fingerprint_format")
    if recorded_format != current_format:
        versions.append(
            _difference(
                "format",
                None,
                None,
                recorded_format,
                current_format,
                f"the recorded fingerprint is format {recorded_format!r} and this one is format "
                f"{current_format!r}; fingerprints of different formats are not compared. "
                f"Recompute both from the stores",
            )
        )
    recorded_encoding = recorded.get("encoding_format")
    current_encoding = current.get("encoding_format")
    if recorded_encoding != current_encoding:
        versions.append(
            _difference(
                "encoding",
                None,
                None,
                recorded_encoding,
                current_encoding,
                f"the recorded fingerprint is encoding format {recorded_encoding!r} and this "
                f"one is encoding format {current_encoding!r}; fingerprints encoded by "
                f"different releases of datastorekit are not compared. Recompute both from "
                f"the stores with one release",
            )
        )
    if versions:
        return versions

    out = []
    if recorded.get("digest") != current.get("digest"):
        before = recorded.get("classes") or {}
        after = current.get("classes") or {}
        names = list(after) + [name for name in before if name not in after]
        for name in names:
            old, new = before.get(name), after.get(name)
            if old is None or new is None:
                out.append(
                    _difference(
                        "class",
                        name,
                        None,
                        None if old is None else old.get("count"),
                        None if new is None else new.get("count"),
                        f"{name}: the class {_presence(old, new)}",
                    )
                )
                continue
            if old.get("digest") == new.get("digest"):
                continue
            old_sets = {tuple(t["tags"]): t for t in old.get("tag_sets") or []}
            new_sets = {tuple(t["tags"]): t for t in new.get("tag_sets") or []}
            found = False
            for tags in sorted(set(old_sets) | set(new_sets)):
                a, b = old_sets.get(tags), new_sets.get(tags)
                if (
                    a is not None
                    and b is not None
                    and a.get("digest") == b.get("digest")
                ):
                    continue
                found = True
                counts = (
                    None if a is None else a.get("count"),
                    None if b is None else b.get("count"),
                )
                if a is None or b is None:
                    text = (
                        f"{name}: tag set {_tags_text(tags)} {_presence(a, b)} "
                        f"({counts[0]} recorded, {counts[1]} now)"
                    )
                else:
                    text = (
                        f"{name}: tag set {_tags_text(tags)} differs: {counts[0]} recorded, "
                        f"{counts[1]} now"
                    )
                out.append(_difference("tag_set", name, tags, *counts, text))
            if not found:
                out.append(
                    _difference(
                        "class",
                        name,
                        None,
                        old.get("count"),
                        new.get("count"),
                        f"{name}: the class digest differs, though no tag set's does "
                        f"({old.get('count')} recorded, {new.get('count')} now)",
                    )
                )
        if not out:
            out.append(
                _difference(
                    "digest",
                    None,
                    None,
                    recorded.get("digest"),
                    current.get("digest"),
                    "the overall digests differ, though no class's does",
                )
            )

    before = recorded.get("problems") or {}
    after = current.get("problems") or {}
    names = list(after) + [name for name in before if name not in after]
    for name in names:
        old, new = before.get(name) or {}, after.get(name) or {}
        for kind in sorted(set(old) | set(new)):
            if old.get(kind, 0) != new.get(kind, 0):
                out.append(
                    _difference(
                        "problems",
                        name,
                        None,
                        old.get(kind, 0),
                        new.get(kind, 0),
                        f"{name}: {kind} problems: {old.get(kind, 0)} recorded, "
                        f"{new.get(kind, 0)} now",
                    )
                )
    return out


def listing_lines(inventory, fingerprint):
    """
    The full listing of ``inventory``, generated on demand and never stored: a header line for
    the fingerprint, then per class a header and, per tag set, a header and the canonical record
    lines. Header lines begin ``#``; record lines begin ``{``. The lines under a tag-set header hash
    (SHA-256, each line followed by a newline) to that tag set's digest, and a class's record lines,
    sorted bytewise, hash to the class's digest. ``fingerprint`` is ``fingerprint_of(inventory,
    fingerprint_format)``.

    The first line is ``# fingerprint_format <f> digest <d> encoding_format <e>``, each value read
    from ``fingerprint``. The encoding format is the last field, so that a reader of the line's
    words by position finds the client's format at word 2 and the digest at word 4 (counting the
    ``#`` as word 0), and the encoding format at word 6.
    """
    yield (
        f"# fingerprint_format {fingerprint['fingerprint_format']} "
        f"digest {fingerprint['digest']} "
        f"encoding_format {fingerprint['encoding_format']}"
    )
    for name, cls in inventory.classes.items():
        entry = fingerprint["classes"][name]
        yield f"# class {name} count {entry['count']} digest {entry['digest']}"
        by_tags = {tuple(t["tags"]): t for t in entry["tag_sets"]}
        for tags, lines in _tag_sets(cls.records):
            recorded = by_tags[tags]
            yield (
                f"# tags {canonical_json(list(tags))} count {recorded['count']} "
                f"digest {recorded['digest']}"
            )
            yield from lines
