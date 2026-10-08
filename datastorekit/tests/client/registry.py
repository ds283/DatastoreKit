"""
The neutral client's registry: the nine names a pool, the reader and the tests are given.

- ``factories``: every storable class, name -> factory, in the order the schema is built;
- ``replicated_tables`` and ``sharded_tables`` (class -> the payload field it is sharded on);
- ``shard_key_type`` (``keypoint``, whose ``__name__`` names its table) and
  ``shard_key_store_id``, which maps a keypoint, or its proxy ``keypoint_alias``, to the
  keypoint's ``store_id``;
- ``read_table_config``: the replicated classes ``read_table`` serves, one with ``tables_arg``
  True and one with it False;
- ``serial_batch_sizes``: how many serials an actor leases at a time, for some tables;
- ``drop_groups`` and ``tables_to_drop``: the drop actions a client would offer, and the tables
  they name.

**The roles** (``docs/client-contract.md`` maps each contract item to the class that supplies
it):

| Class | Kind | Roles |
|---|---|---|
| ``version``, ``store_tag`` | replicated | the layer's two tables, each with its ``label`` column |
| ``keypoint`` | replicated | the shard-key class; ``monotone_flags``; ``read_table`` (``tables_arg`` False) |
| ``keypoint_alias`` | replicated | the shard key's proxy; ``stepping: "exact"``; ``store`` of a replica, no owned rows |
| ``dial_setting`` | replicated | ``stepping: "minimum"``; ``read_table`` (``tables_arg`` True) |
| ``knob_setting`` | replicated | ``stepping: True``; ``timestamp: False`` |
| ``gauge_setting`` | replicated | a leaf with no ``version`` column, got or inserted by its exponent (prompt 03b) |
| ``routing_rule`` | replicated | a leaf with a ``version`` column, got or inserted by three columns (prompt 03b) |
| ``ephemeral_probe`` | replicated | ``register()`` returns ``None`` |
| ``Gadget`` | replicated | ``validate_on_startup`` (the pool's prune), ``validated_column`` with ``revalidate``, ``owned_serials``; a polymorphic ``Parent``; tags and values |
| ``Gadget_tags`` | neither | a replicated class's tag table; ``serial: False`` |
| ``GadgetPart`` | replicated | ``owner_column`` |
| ``Tessera`` | sharded on ``k`` | keyed on the proxy |
| ``Sample`` | sharded on ``k`` | ``validate_on_startup`` (each actor's prune); ``read_batch``; a ``cross_shard`` and ``nullable`` ``Parent``; a ``ParentSet`` |
| ``Sample_tags`` | neither | the sharded class's tag association |
| ``Sample_members`` | neither | the ``ParentSet``'s member table, named by foreign key, with no ``inventory_spec`` |
| ``Trace`` | sharded on ``k`` | tags, values (``TraceStep``) and the validated flag the inventory reads; the polymorphic ``frame``, through ``Gadget``'s type map (prompt 04a) |
| ``Trace_tags``, ``TraceStep`` | neither | ``Trace``'s tag association and value table (prompt 04a) |
| ``Weave`` | sharded on ``k`` | tagged, with no validated flag and no values; a ``Trace`` of its shard; a nullable ``anchor``; a ``ParentSet`` (``strands``) (prompt 04a) |
| ``Weave_tags``, ``Weave_members`` | neither | ``Weave``'s tag association, and its ``ParentSet``'s member table, with serials and nullable members (prompt 04a) |

**The drop groups.** Their union is every table a client would drop: all but the layer's two, the
shard-key class and the two settings (which every Gadget, and so every Sample, may name), and
``ephemeral_probe``, which has no table. The union is closed: ``dependent_tables`` of it is
empty. Each group alone is not: ``samples`` is closed, but ``tesserae`` must be dropped with
``samples`` (a Sample names a Tessera by a declared parent and by its members' foreign key),
``aliases`` with ``tesserae`` and ``samples``, and ``gadgets`` with ``samples``. Two groups hold a
replicated table (``aliases``; ``gadgets``).
``gauge_setting`` and ``routing_rule`` (added by prompt 03b) are in no group either, as leaves a
client would keep.
The sharded family added by prompt 04a is the group ``traces``, closed on its own; ``Weave`` and
``Weave_members`` name a Tessera, so ``aliases`` and ``tesserae`` must be dropped with them too.

Importing this module imports the factories, ``sqlalchemy`` and ``datastorekit``; it starts
nothing.
"""

from typing import Iterable as _Iterable
from typing import List as _List

from datastorekit.tests.client import factories as _f
from datastorekit.tests.client import objects as _objects

__all__ = [
    "factories",
    "replicated_tables",
    "sharded_tables",
    "shard_key_type",
    "shard_key_store_id",
    "read_table_config",
    "serial_batch_sizes",
    "drop_groups",
    "tables_to_drop",
]

factories = {
    "version": _f.version_factory,
    "store_tag": _f.store_tag_factory,
    "keypoint": _f.keypoint_factory,
    "keypoint_alias": _f.keypoint_alias_factory,
    "dial_setting": _f.dial_setting_factory,
    "knob_setting": _f.knob_setting_factory,
    "gauge_setting": _f.gauge_setting_factory,
    "routing_rule": _f.routing_rule_factory,
    "ephemeral_probe": _f.ephemeral_probe_factory,
    "Gadget": _f.Gadget_factory,
    "Gadget_tags": _f.Gadget_tags_factory,
    "GadgetPart": _f.GadgetPart_factory,
    "Tessera": _f.Tessera_factory,
    "Sample": _f.Sample_factory,
    "Sample_tags": _f.Sample_tags_factory,
    "Sample_members": _f.Sample_members_factory,
    # added by prompt 04a (U15)
    "Trace": _f.Trace_factory,
    "Trace_tags": _f.Trace_tags_factory,
    "TraceStep": _f.TraceStep_factory,
    "Weave": _f.Weave_factory,
    "Weave_tags": _f.Weave_tags_factory,
    "Weave_members": _f.Weave_members_factory,
}

replicated_tables = [
    "version",
    "store_tag",
    "keypoint",
    "keypoint_alias",
    "dial_setting",
    "knob_setting",
    "gauge_setting",
    "routing_rule",
    "ephemeral_probe",
    "Gadget",
    "GadgetPart",
]

sharded_tables = {
    "Tessera": "k",
    "Sample": "k",
    "Trace": "k",
    "Weave": "k",
}

read_table_config = {
    "keypoint": {"tables_arg": False},
    "dial_setting": {"tables_arg": True},
}

serial_batch_sizes = {
    "store_tag": 5,
    "keypoint": 10,
    "GadgetPart": 50,
    "Sample": 20,
}

shard_key_type = _objects.keypoint


def shard_key_store_id(obj) -> int:
    """The store_id of the keypoint ``obj`` is, or is a proxy for."""
    if isinstance(obj, _objects.keypoint):
        return obj.store_id
    if isinstance(obj, _objects.keypoint_alias):
        return obj.keypoint.store_id
    raise RuntimeError(
        f'Could not determine the keypoint shard key of an object of type "{type(obj)}"'
    )


drop_groups = {
    "aliases": ["keypoint_alias"],
    "tesserae": ["Tessera"],
    "samples": ["Sample", "Sample_tags", "Sample_members"],
    "gadgets": ["Gadget", "Gadget_tags", "GadgetPart"],
    # added by prompt 04a (U15)
    "traces": [
        "Trace",
        "Trace_tags",
        "TraceStep",
        "Weave",
        "Weave_tags",
        "Weave_members",
    ],
}


def tables_to_drop(actions: _Iterable[str]) -> _List[str]:
    """
    The tables of the drop groups named by ``actions``, each once, in the order the actions and
    then each group's list give them. An action that is not a drop group raises ``ValueError``
    naming it, and the groups there are.
    """
    tables: _List[str] = []
    for action in actions:
        if action not in drop_groups:
            raise ValueError(
                f'Unknown drop action "{action}": the drop actions are {list(drop_groups)}'
            )
        for table in drop_groups[action]:
            if table not in tables:
                tables.append(table)
    return tables
