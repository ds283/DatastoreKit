"""
The neutral client's stored classes. Each class's ``__name__`` is the name of its table, because
the layer dispatches a store or a validate by ``type(obj).__name__``, and names the shard-key table
by ``shard_key_type.__name__``.

Every class is defined at module level, so that the stand-in pool can pickle it, as Ray would.
Each stored class is a ``DatastoreObject``: the layer reads ``_my_id`` and ``store_id`` of what a
factory returns, and a replicated get's answer is copied to the other shards when it carries
``_new_insert`` or ``_updated`` (set by the factories, never here).
"""

from typing import List, Optional, Sequence

from datastorekit.object import DatastoreObject


class SerialHandle:
    """Anything a factory reads only a ``store_id`` from: a row read back by serial."""

    def __init__(self, store_id: int):
        self.store_id = store_id
        self._my_id = store_id


class version_entry(DatastoreObject):
    """A row of the layer's ``version`` table."""

    def __init__(self, store_id: Optional[int], label: str):
        super().__init__(store_id)
        self.label = label


class tag_entry(DatastoreObject):
    """A row of the layer's ``store_tag`` table."""

    def __init__(self, store_id: Optional[int], label: str):
        super().__init__(store_id)
        self.label = label


class keypoint(DatastoreObject):
    """The shard-key class: a replicated leaf, with two flags a get may turn on."""

    def __init__(
        self,
        store_id: Optional[int],
        position: float,
        marked: bool = False,
        flagged: bool = False,
    ):
        super().__init__(store_id)
        self.position = position
        self.marked = marked
        self.flagged = flagged


class keypoint_alias(DatastoreObject):
    """The shard key's proxy: a replicated class naming one ``keypoint``. A sharded class keyed on
    an alias is placed on its keypoint's shard. Unstored (``store_id`` None) until stored.
    """

    def __init__(
        self,
        store_id: Optional[int],
        keypoint: keypoint,
        offset: float,
        stepping: int = 0,
    ):
        super().__init__(store_id)
        self.keypoint = keypoint
        self.offset = offset
        self.stepping = stepping


class dial_setting(DatastoreObject):
    """A replicated leaf, with a ``stepping`` column of mode ``"minimum"``."""

    def __init__(self, store_id: Optional[int], level: int, stepping: int = 0):
        super().__init__(store_id)
        self.level = level
        self.stepping = stepping


class knob_setting(DatastoreObject):
    """A replicated leaf, with a ``stepping`` column of no mode (``stepping: True``)."""

    def __init__(self, store_id: Optional[int], turns: int, stepping: int = 0):
        super().__init__(store_id)
        self.turns = turns
        self.stepping = stepping


class gauge_setting(DatastoreObject):
    """A replicated leaf with no ``version`` column, got or inserted by its exponent (added by
    prompt 03b)."""

    def __init__(self, store_id: Optional[int], exponent: int):
        super().__init__(store_id)
        self.exponent = exponent


class routing_rule(DatastoreObject):
    """A replicated leaf with a ``version`` column, got or inserted by its label, threshold and
    mode together (added by prompt 03b)."""

    def __init__(
        self, store_id: Optional[int], label: str, threshold: float, mode: str
    ):
        super().__init__(store_id)
        self.label = label
        self.threshold = threshold
        self.mode = mode


class ephemeral_probe:
    """The class whose ``register()`` returns ``None``: it has no table, and is never stored."""

    def __init__(self, note: str):
        self.note = note


class GadgetPart(DatastoreObject):
    """One value row of a ``Gadget``: the table that declares ``owner_column``."""

    def __init__(self, store_id: Optional[int], part_index: int, part_value: float):
        super().__init__(store_id)
        self.part_index = part_index
        self.part_value = part_value


class Gadget(DatastoreObject):
    """
    The replicated owner class: tagged, with value rows (``GadgetPart``) it owns, a validated
    flag the pool recomputes after an interrupted validate, and a polymorphic parent (``frame``, a
    ``dial_setting`` or a ``knob_setting``). Unstored (``store_id`` None) until stored.
    """

    def __init__(
        self,
        store_id: Optional[int],
        label: str,
        frame,
        tags: Sequence[tag_entry] = (),
        parts: Optional[List[GadgetPart]] = None,
        validated: bool = False,
    ):
        super().__init__(store_id)
        self.label = label
        self.frame = frame
        self.tags = list(tags)
        self.parts = list(parts) if parts is not None else []
        self.validated = validated


class Tessera(DatastoreObject):
    """A sharded class keyed on a ``keypoint_alias`` (the proxy): its ``k`` is an alias."""

    def __init__(self, store_id: Optional[int], k, weight: float):
        super().__init__(store_id)
        self.k = k
        self.weight = weight


class Sample(DatastoreObject):
    """
    The sharded parent class, sharded on ``k`` (a ``keypoint``): tagged (``Sample_tags``), keyed on
    a ``Gadget``, on a set of ``Tessera`` members on its own shard (``Sample_members``) and on an
    optional ``anchor``, a ``Tessera`` that may be on another shard. Unstored (``store_id`` None)
    until stored.
    """

    def __init__(
        self,
        store_id: Optional[int],
        k,
        gadget,
        code: str,
        tags: Sequence[tag_entry] = (),
        members: Sequence = (),
        anchor=None,
        validated: bool = False,
    ):
        super().__init__(store_id)
        self.k = k
        self.gadget = gadget
        self.code = code
        self.tags = list(tags)
        self.members = list(members)
        self.anchor = anchor
        self.validated = validated


# ------------------------------------------------------------------------------------------------
# the sharded family (added by prompt 04a, U15)
# ------------------------------------------------------------------------------------------------


class TraceStep(DatastoreObject):
    """One value row of a ``Trace``: a sharded class's value table (added by prompt 04a)."""

    def __init__(self, store_id: Optional[int], step_index: int, step_value: float):
        super().__init__(store_id)
        self.step_index = step_index
        self.step_value = step_value


class Trace(DatastoreObject):
    """
    A sharded class, sharded on ``k`` (a ``keypoint``): tagged (``Trace_tags``), with value rows
    (``TraceStep``) and a validated flag, and a polymorphic parent (``frame``, a ``dial_setting``
    or a ``knob_setting``), as ``Gadget`` has. Unstored (``store_id`` None) until stored (added by
    prompt 04a).
    """

    def __init__(
        self,
        store_id: Optional[int],
        k,
        frame,
        label: str,
        tags: Sequence[tag_entry] = (),
        steps: Optional[List[TraceStep]] = None,
        validated: bool = False,
    ):
        super().__init__(store_id)
        self.k = k
        self.frame = frame
        self.label = label
        self.tags = list(tags)
        self.steps = list(steps) if steps is not None else []
        self.validated = validated


class Weave(DatastoreObject):
    """
    A sharded class, sharded on ``k`` (a ``keypoint``): tagged (``Weave_tags``), keyed on a
    ``Trace`` of its own shard, on an optional ``anchor`` (a ``Tessera``), and on a set of
    ``strands`` (``Weave_members``), each a pair ``(anchor, origin)`` of an optional ``Tessera``
    and an optional ``Trace``. It has no validated flag and no value table. Unstored (``store_id``
    None) until stored (added by prompt 04a).
    """

    def __init__(
        self,
        store_id: Optional[int],
        k,
        trace,
        label: str,
        tags: Sequence[tag_entry] = (),
        strands: Sequence = (),
        anchor=None,
    ):
        super().__init__(store_id)
        self.k = k
        self.trace = trace
        self.label = label
        self.tags = list(tags)
        self.strands = list(strands)
        self.anchor = anchor
