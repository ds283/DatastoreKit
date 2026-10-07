"""
Helpers that get or store each of the neutral client's classes through a pool, and
``build_store``, which writes a store with every class populated through the stand-in pool.

Every helper resolves the pool's references with the stand-in pool's own ``ray.get``
(``standin_pool.standin_get``), never with ``ray.get`` itself, so a helper called outside
``StandinCluster.active()`` cannot start Ray.

``build_store`` is the counterpart, for the neutral client, of a fixture that builds a store with
every class populated. It is written for this client, through the pool, and holds no rows written
by hand: every row is written by the layer and the client's factories.
"""

from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

from datastorekit.tests import standin_pool as _sp
from datastorekit.tests.client import registry
from datastorekit.tests.client.objects import (
    Gadget,
    GadgetPart,
    Sample,
    SerialHandle,
    Tessera,
    dial_setting,
    ephemeral_probe,
    keypoint,
    keypoint_alias,
    knob_setting,
    tag_entry,
    version_entry,
)

# what build_store writes
TAG_LABELS = ("tag-north", "tag-south", "tag-unused")
KEYPOINT_POSITIONS = (0.25, 0.5, 1.0)
# the keypoint whose flag a second get turns on
MARKED_POSITION = 0.5
ALIAS_OFFSET = 0.125
ALIAS_STEPPING = 1
TESSERA_WEIGHTS = (0.5, 0.75)
DIAL_LEVELS = ((3, 1), (5, 0))  # (level, stepping)
KNOB_TURNS = (7, 2)  # (turns, stepping)
GADGETS = {
    # label: (frame, tags, part values, validated)
    "gadget-one": ("dial", ("tag-north",), (1.5, 2.5, 3.5), True),
    "gadget-two": ("knob", ("tag-north", "tag-south"), (4.0,), False),
}
UNVALIDATED_SAMPLE = "sample-unvalidated"


def resolve(refs):
    """The stand-in pool's ``ray.get``: the value of a reference, or a list of them."""
    return _sp.standin_get(refs)


def open_pool(cluster: "_sp.StandinCluster", primary: Path, shards: int = 3, **kwargs):
    """``cluster.open_pool`` with the registry's ``read_table_config`` and
    ``serial_batch_sizes``, which ``StandinCluster.open_pool`` does not pass by default.
    """
    kwargs.setdefault("read_table_config", registry.read_table_config)
    kwargs.setdefault("serial_batch_sizes", registry.serial_batch_sizes)
    return cluster.open_pool(primary, shards=shards, **kwargs)


# ------------------------------------------------------------------------------------------------
# the replicated classes
# ------------------------------------------------------------------------------------------------


def get_version(pool, label: str) -> version_entry:
    return resolve(pool.object_get("version", label=label))


def get_tags(pool, *labels: str) -> List[tag_entry]:
    return [resolve(pool.object_get("store_tag", label=label)) for label in labels]


def get_keypoint(
    pool, position: float, marked: bool = False, flagged: bool = False
) -> keypoint:
    return resolve(
        pool.object_get("keypoint", position=position, marked=marked, flagged=flagged)
    )


def get_keypoints(
    pool, positions: Iterable[float], marked: bool = False, flagged: bool = False
) -> List[keypoint]:
    """One vectorized replicated get (``payload_data``)."""
    return resolve(
        pool.object_get(
            "keypoint",
            payload_data=[
                {"position": p, "marked": marked, "flagged": flagged} for p in positions
            ],
        )
    )


def get_dial(pool, level: int, stepping: int = 0) -> dial_setting:
    return resolve(pool.object_get("dial_setting", level=level, stepping=stepping))


def get_knob(pool, turns: int, stepping: int = 0) -> knob_setting:
    return resolve(pool.object_get("knob_setting", turns=turns, stepping=stepping))


def get_probe(pool, note: str) -> ephemeral_probe:
    return resolve(pool.object_get("ephemeral_probe", note=note))


def make_alias(k: keypoint, offset: float, stepping: int = 0) -> keypoint_alias:
    """An unstored ``keypoint_alias``, as a computation would leave it."""
    return keypoint_alias(None, k, offset, stepping)


def get_alias(pool, k: keypoint, offset: float, stepping: int = 0) -> keypoint_alias:
    """The stored alias: found by a get, or stored (a replicated store) on a miss."""
    alias = resolve(
        pool.object_get("keypoint_alias", keypoint=k, offset=offset, stepping=stepping)
    )
    if alias.available:
        return alias
    return resolve(pool.object_store(alias))


def make_gadget(
    label: str, frame, tags: Sequence[tag_entry], values: Sequence[float]
) -> Gadget:
    """An unstored ``Gadget`` with one unstored part per value, as a computation would leave
    it."""
    return Gadget(
        None,
        label,
        frame,
        tags=tags,
        parts=[GadgetPart(None, i, v) for i, v in enumerate(values)],
    )


def store_gadget(pool, gadget: Gadget, validate: bool = True) -> Gadget:
    """Store ``gadget`` (a replicated store), then validate it (a replicated validate) unless
    ``validate`` is False. Returns the stored object, which carries its serials."""
    stored = resolve(pool.object_store(gadget))
    if validate:
        if resolve(pool.object_validate(stored)) is not True:
            raise RuntimeError(f'build: Gadget "{stored.label}" did not validate')
        stored.validated = True
    return stored


def get_gadget(pool, label: str, frame, tags: Sequence[tag_entry]) -> Gadget:
    """A replicated get that inserts nothing: the stored, validated Gadget, or an unstored one."""
    return resolve(pool.object_get("Gadget", label=label, frame=frame, tags=tags))


# ------------------------------------------------------------------------------------------------
# the sharded classes
# ------------------------------------------------------------------------------------------------


def get_tesserae(
    pool, alias: keypoint_alias, weights: Iterable[float]
) -> List[Tessera]:
    """A vectorized sharded get, on the alias's keypoint's shard (``object_get_vectorized``)."""
    return resolve(
        pool.object_get_vectorized(
            "Tessera", {"k": alias}, payload_data=[{"weight": w} for w in weights]
        )
    )


def make_sample(
    k: keypoint,
    gadget: Gadget,
    code: str,
    tags: Sequence[tag_entry] = (),
    members: Sequence[Tessera] = (),
    anchor: Optional[Tessera] = None,
) -> Sample:
    """An unstored ``Sample``, as a computation would leave it."""
    return Sample(None, k, gadget, code, tags=tags, members=members, anchor=anchor)


def store_sample(pool, sample: Sample, validate: bool = True) -> Sample:
    """Store ``sample`` on its keypoint's shard, then validate it unless ``validate`` is False."""
    stored = resolve(pool.object_store(sample))
    if validate:
        if resolve(pool.object_validate(stored)) is not True:
            raise RuntimeError(f'build: Sample "{stored.code}" did not validate')
        stored.validated = True
    return stored


def get_sample(
    pool, k: keypoint, gadget: Gadget, code: str, tags: Sequence[tag_entry] = ()
) -> Sample:
    """A sharded get: the stored, validated Sample, or an unstored one."""
    return resolve(
        pool.object_get("Sample", k=k, gadget=gadget, code=code, tags=list(tags))
    )


def read_samples(pool, k: keypoint, validated_only: bool = True) -> List[Sample]:
    """Every Sample of keypoint ``k``, by the factory's ``read_batch``."""
    return resolve(
        pool.object_read_batch("Sample", {"k": k}, validated_only=validated_only)
    )


# ------------------------------------------------------------------------------------------------
# the store
# ------------------------------------------------------------------------------------------------


def write_every_class(pool) -> Dict[str, list]:
    """
    Write at least one row of every class with a table into the open ``pool``, and get the class
    with none, through the layer and the factories only. Returns the objects written, by class.

    - three tags, one of them used by nothing;
    - three keypoints, by one vectorized get; then one of them got again with its flag on, which
      updates it on every shard;
    - two dial settings and one knob setting (the two frame classes), and one probe;
    - one alias per keypoint, each stored on a miss;
    - two Gadgets, with tags and parts: one validated, one left unvalidated;
    - two Tesserae per alias;
    - one validated Sample per keypoint, keyed on the validated Gadget, on both Tesserae of its own
      keypoint's alias as members, and on an anchor: the first Tessera of the next keypoint's
      alias (on another shard when there are enough shards), or none for the first keypoint;
      and one unvalidated Sample, keyed on the unvalidated Gadget.
    """
    written: Dict[str, list] = {}

    tags = {t.label: t for t in get_tags(pool, *TAG_LABELS)}
    written["store_tag"] = list(tags.values())

    points = get_keypoints(pool, KEYPOINT_POSITIONS)
    marked = get_keypoint(pool, MARKED_POSITION, marked=True)
    points = [marked if p.store_id == marked.store_id else p for p in points]
    written["keypoint"] = points

    dials = [get_dial(pool, level, stepping) for level, stepping in DIAL_LEVELS]
    knob = get_knob(pool, *KNOB_TURNS)
    written["dial_setting"] = dials
    written["knob_setting"] = [knob]
    written["ephemeral_probe"] = [get_probe(pool, "standin")]

    aliases = [get_alias(pool, p, ALIAS_OFFSET, ALIAS_STEPPING) for p in points]
    written["keypoint_alias"] = aliases

    frames = {"dial": dials[0], "knob": knob}
    gadgets = {}
    for label, (frame, tag_labels, values, validated) in GADGETS.items():
        gadget = make_gadget(
            label, frames[frame], [tags[t] for t in tag_labels], values
        )
        gadgets[label] = store_gadget(pool, gadget, validate=validated)
    written["Gadget"] = list(gadgets.values())

    tesserae = [get_tesserae(pool, alias, TESSERA_WEIGHTS) for alias in aliases]
    written["Tessera"] = [t for group in tesserae for t in group]

    samples = []
    good = gadgets["gadget-one"]
    for i, point in enumerate(points):
        anchor = None if i == 0 else tesserae[(i + 1) % len(points)][0]
        sample = make_sample(
            point,
            good,
            f"sample-{i}",
            tags=[tags["tag-south"]],
            members=tesserae[i],
            anchor=anchor,
        )
        samples.append(store_sample(pool, sample))
    unvalidated = make_sample(
        points[1],
        gadgets["gadget-two"],
        UNVALIDATED_SAMPLE,
        members=tesserae[1][:1],
    )
    samples.append(store_sample(pool, unvalidated, validate=False))
    written["Sample"] = samples
    return written


def build_store(directory, shards: int = 3) -> Path:
    """
    Write a store with every class populated, through the stand-in pool, in ``directory`` (which
    must be temporary), close it, and return its primary's path (``directory / "store.sqlite"``).

    The pool is opened with the registry, its ``read_table_config`` and its
    ``serial_batch_sizes``, under the stand-in's version label. What is written is
    ``write_every_class``'s.
    """
    primary = Path(directory) / "store.sqlite"
    cluster = _sp.StandinCluster()
    with cluster.active():
        pool = open_pool(cluster, primary, shards=shards)
        try:
            write_every_class(pool)
        finally:
            cluster.close_pool(pool)
    return primary


# ------------------------------------------------------------------------------------------------
# the fixtures of the ported write-path tests (added by prompt 03a)
# ------------------------------------------------------------------------------------------------

# the knob setting a framed Gadget is written on, and the keypoint positions its parts are got
# over
FRAME_TURNS = 1
PART_POSITIONS = (1.0e4, 1.0e2, 1.0)


def make_framed_gadget(
    pool,
    tags: Sequence[tag_entry],
    positions: Sequence[float] = PART_POSITIONS,
    scale: float = 1.0,
    label: str = "standin-gadget",
) -> Gadget:
    """
    An unstored ``Gadget`` labelled ``label``, with ``tags`` and one part per position of
    ``positions``, as a computation would leave it. Its frame (a ``knob_setting``) and its
    keypoints (one vectorized get, every keypoint marked) are got through ``pool``, both
    replicated gets. Part ``i`` has the value ``scale * (1 + position)`` of its keypoint, so that
    a ``scale`` other than 1 gives a Gadget whose row and tags are the same and whose parts
    differ.
    """
    points = get_keypoints(pool, positions, marked=True)
    frame = get_knob(pool, FRAME_TURNS)
    return make_gadget(label, frame, tags, [scale * (1.0 + p.position) for p in points])


def make_sample_on(
    alias: keypoint_alias, gadget_serial: int = 1, code: str = "standin-sample"
) -> Sample:
    """
    An unstored ``Sample`` with no tags and no members, on the keypoint that ``alias`` names (so
    on that keypoint's shard), keyed on a Gadget given only by its serial
    (``objects.SerialHandle``): the factory reads only its ``store_id``, and the layer enforces
    no foreign key across a store.
    """
    return make_sample(alias.keypoint, SerialHandle(gadget_serial), code)
