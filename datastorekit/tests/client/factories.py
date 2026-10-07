"""
The neutral client's factories: one per stored class, each a ``SQLAFactoryBase`` whose static
methods are the hooks the layer calls (``docs/client-contract.md``).

Every lookup is exact, and every factory follows the same few rules, so that the client is small
and its behaviour is easy to state:

- a **leaf** (``version``, ``store_tag``, ``keypoint``, ``dial_setting``, ``knob_setting``,
  ``GadgetPart``, ``Tessera``) is got or inserted by ``build``. An inserted object carries
  ``_new_insert``; a ``keypoint`` whose flags a get turned on carries ``_updated``. A ``serial`` in
  the payload (a replica's get) is the serial the row is inserted under;
- a **computed** class (``keypoint_alias``, ``Gadget``, ``Sample``) is found by ``build``, which
  returns an unstored object (``store_id`` None) on a miss and inserts nothing; ``store`` inserts
  it. A replicated computed class's ``store`` is given an object that already carries a serial on
  every shard but the controlling one, and inserts it under that serial or verifies that it holds
  it, raising ``ReplicationMismatch`` on a difference;
- an **association** table (``Gadget_tags``, ``Sample_tags``, ``Sample_members``) is written by its
  owner's ``store``, and has no ``build`` of its own.

This module imports only the standard library, ``sqlalchemy`` and ``datastorekit``.
"""

from typing import List, Optional

import sqlalchemy as sqla
from sqlalchemy.exc import SQLAlchemyError

from datastorekit.SQL.factory_base import SQLAFactoryBase
from datastorekit.contract import TAG_LABEL, TAG_SERIAL, TAG_TABLE, VERSION_LABEL
from datastorekit.defaults import DEFAULT_STRING_LENGTH
from datastorekit.replication import ReplicationMismatch, differing_columns
from datastorekit.store_inventory import InventorySpec, Parent, ParentSet
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

# the polymorphic parent of a Gadget: the value of its frame_kind column names the frame's class
FRAME_KINDS = {"dial_setting": 1, "knob_setting": 2}
FRAME_TYPES = {kind: name for name, kind in FRAME_KINDS.items()}


def _new(obj, attributes: dict):
    for key, value in attributes.items():
        setattr(obj, key, value)
    return obj


def _tag_serials(tags) -> List[int]:
    return sorted(tag.store_id for tag in tags)


def _stored_tag_serials(conn, tag_table, owner_column: str, serial: int) -> List[int]:
    return sorted(
        conn.execute(
            sqla.select(tag_table.c[TAG_SERIAL]).filter(
                tag_table.c[owner_column] == serial
            )
        )
        .scalars()
        .all()
    )


def _stored_tags(conn, tables, tag_table, owner_column: str, serial: int):
    tag_rows = tables[TAG_TABLE]
    return [
        tag_entry(store_id=row.serial, label=row.label)
        for row in conn.execute(
            sqla.select(tag_rows.c.serial, tag_rows.c[TAG_LABEL].label("label"))
            .select_from(
                tag_table.join(tag_rows, tag_rows.c.serial == tag_table.c[TAG_SERIAL])
            )
            .filter(tag_table.c[owner_column] == serial)
            .order_by(tag_rows.c.serial)
        )
    ]


# ------------------------------------------------------------------------------------------------
# the layer's two tables
# ------------------------------------------------------------------------------------------------


class _label_factory(SQLAFactoryBase):
    """A table of labels, got or inserted by its label: the layer's ``version`` and ``store_tag``.
    Each subclass names its object class and its label column, which the layer fixes
    (``datastorekit.contract``)."""

    entry = None
    label_column = None

    @classmethod
    def build(cls, payload, conn, table, inserter, tables, inserters):
        label = payload[cls.label_column]
        store_id = conn.execute(
            sqla.select(table.c.serial).filter(table.c[cls.label_column] == label)
        ).scalar_one_or_none()
        attributes = {"_deserialized": True}
        if store_id is None:
            data = {cls.label_column: label}
            if "serial" in payload:
                data["serial"] = payload["serial"]
            store_id = inserter(conn, data)
            attributes = {"_new_insert": True}
        return _new(cls.entry(store_id=store_id, label=label), attributes)

    @classmethod
    def inventory_spec(cls):
        # a label row's identity is its label; the inventory reads a tag's label from this key
        return InventorySpec(leaves=(cls.label_column,))


class version_factory(_label_factory):
    entry = version_entry
    label_column = VERSION_LABEL

    @staticmethod
    def register():
        return {
            "version": False,
            "timestamp": False,
            "columns": [
                sqla.Column(
                    VERSION_LABEL, sqla.String(DEFAULT_STRING_LENGTH), nullable=False
                )
            ],
        }


class store_tag_factory(_label_factory):
    entry = tag_entry
    label_column = TAG_LABEL

    @staticmethod
    def register():
        return {
            "version": False,
            "timestamp": True,
            "columns": [
                sqla.Column(
                    TAG_LABEL, sqla.String(DEFAULT_STRING_LENGTH), nullable=False
                )
            ],
        }


# ------------------------------------------------------------------------------------------------
# replicated leaves
# ------------------------------------------------------------------------------------------------


class keypoint_factory(SQLAFactoryBase):
    """The shard-key class. Its two flags only ever turn on, so it declares them monotone."""

    @staticmethod
    def register():
        return {
            "version": False,
            "timestamp": True,
            "columns": [
                sqla.Column("kp_position", sqla.Float(64), nullable=False),
                sqla.Column("kp_marked", sqla.Boolean, default=False, nullable=False),
                sqla.Column("kp_flagged", sqla.Boolean, default=False, nullable=False),
            ],
            "monotone_flags": ("kp_marked", "kp_flagged"),
        }

    @staticmethod
    def build(payload, conn, table, inserter, tables, inserters):
        position = payload["position"]
        marked = bool(payload.get("marked", False))
        flagged = bool(payload.get("flagged", False))

        row = conn.execute(
            sqla.select(table.c.serial, table.c.kp_marked, table.c.kp_flagged).filter(
                table.c.kp_position == position
            )
        ).one_or_none()

        if row is None:
            data = {"kp_position": position, "kp_marked": marked, "kp_flagged": flagged}
            if "serial" in payload:
                data["serial"] = payload["serial"]
            store_id = inserter(conn, data)
            attributes = {"_new_insert": True}
        else:
            store_id = row.serial
            attributes = {"_deserialized": True}
            now_marked = marked or row.kp_marked
            now_flagged = flagged or row.kp_flagged
            if (now_marked and not row.kp_marked) or (
                now_flagged and not row.kp_flagged
            ):
                conn.execute(
                    sqla.update(table)
                    .where(table.c.serial == store_id)
                    .values(kp_marked=now_marked, kp_flagged=now_flagged)
                )
                attributes["_updated"] = True
            marked, flagged = now_marked, now_flagged

        return _new(keypoint(store_id, position, marked, flagged), attributes)

    @staticmethod
    def read_table(conn, table, marked: Optional[bool] = None):
        # read_table_config gives this class tables_arg False: no ``tables`` is passed
        query = sqla.select(
            table.c.serial, table.c.kp_position, table.c.kp_marked, table.c.kp_flagged
        )
        if marked is not None:
            query = query.filter(table.c.kp_marked == marked)
        return [
            keypoint(row.serial, row.kp_position, row.kp_marked, row.kp_flagged)
            for row in conn.execute(query.order_by(table.c.kp_position))
        ]

    @staticmethod
    def inventory_spec():
        # the flags accumulate and are not identity
        return InventorySpec(leaves=("kp_position",))


class dial_setting_factory(SQLAFactoryBase):
    """A leaf with ``stepping: "minimum"``: a get is served by the row of its level with the
    smallest stepping at least the one asked for, and inserts the one asked for on a miss.
    """

    @staticmethod
    def register():
        # "version" is left to its default (False)
        return {
            "timestamp": True,
            "stepping": "minimum",
            "columns": [sqla.Column("dial_level", sqla.Integer, nullable=False)],
        }

    @staticmethod
    def build(payload, conn, table, inserter, tables, inserters):
        level = payload["level"]
        stepping = payload.get("stepping", 0)
        row = conn.execute(
            sqla.select(table.c.serial, table.c.stepping)
            .filter(table.c.dial_level == level, table.c.stepping >= stepping)
            .order_by(table.c.stepping, table.c.serial)
            .limit(1)
        ).one_or_none()
        if row is not None:
            return _new(
                dial_setting(row.serial, level, row.stepping), {"_deserialized": True}
            )
        data = {"dial_level": level, "stepping": stepping}
        if "serial" in payload:
            data["serial"] = payload["serial"]
        store_id = inserter(conn, data)
        return _new(dial_setting(store_id, level, stepping), {"_new_insert": True})

    @staticmethod
    def read_table(conn, table, *, tables, level: Optional[int] = None):
        # read_table_config gives this class tables_arg True: the actor passes ``tables``, and a
        # call without it is a TypeError here
        if tables["dial_setting"] is not table:
            raise RuntimeError(
                "dial_setting.read_table: tables does not hold this table"
            )
        query = sqla.select(table.c.serial, table.c.dial_level, table.c.stepping)
        if level is not None:
            query = query.filter(table.c.dial_level == level)
        return [
            dial_setting(row.serial, row.dial_level, row.stepping)
            for row in conn.execute(
                query.order_by(table.c.dial_level, table.c.stepping)
            )
        ]

    @staticmethod
    def inventory_spec():
        return InventorySpec(leaves=("dial_level", "stepping"))


class knob_setting_factory(SQLAFactoryBase):
    """A leaf with ``stepping: True`` (a stepping column and no mode): got or inserted exactly."""

    @staticmethod
    def register():
        return {
            "version": False,
            "timestamp": False,
            "stepping": True,
            "columns": [sqla.Column("knob_turns", sqla.Integer, nullable=False)],
        }

    @staticmethod
    def build(payload, conn, table, inserter, tables, inserters):
        turns = payload["turns"]
        stepping = payload.get("stepping", 0)
        store_id = conn.execute(
            sqla.select(table.c.serial).filter(
                table.c.knob_turns == turns, table.c.stepping == stepping
            )
        ).scalar_one_or_none()
        attributes = {"_deserialized": True}
        if store_id is None:
            data = {"knob_turns": turns, "stepping": stepping}
            if "serial" in payload:
                data["serial"] = payload["serial"]
            store_id = inserter(conn, data)
            attributes = {"_new_insert": True}
        return _new(knob_setting(store_id, turns, stepping), attributes)

    @staticmethod
    def inventory_spec():
        return InventorySpec(leaves=("knob_turns", "stepping"))


class ephemeral_probe_factory(SQLAFactoryBase):
    """The class with no table: ``register()`` returns ``None``. A get builds the object from its
    payload alone; the layer hands ``build`` no table and no inserter."""

    @staticmethod
    def register():
        return None

    @staticmethod
    def build(payload, conn, table, inserter, tables, inserters):
        if table is not None or inserter is not None:
            raise RuntimeError(
                "ephemeral_probe.build: a class with no table was given one"
            )
        return ephemeral_probe(note=payload.get("note", ""))


# ------------------------------------------------------------------------------------------------
# the shard key's proxy
# ------------------------------------------------------------------------------------------------


class keypoint_alias_factory(SQLAFactoryBase):
    """A replicated computed class with ``stepping: "exact"``, naming one keypoint. A sharded
    class keyed on an alias is placed on its keypoint's shard (``registry.shard_key_store_id``).
    """

    @staticmethod
    def register():
        return {
            "version": True,
            "timestamp": True,
            "stepping": "exact",
            "columns": [
                sqla.Column(
                    "keypoint_serial",
                    sqla.Integer,
                    sqla.ForeignKey("keypoint.serial"),
                    index=True,
                    nullable=False,
                ),
                sqla.Column("ka_offset", sqla.Float(64), nullable=False),
            ],
        }

    @staticmethod
    def build(payload, conn, table, inserter, tables, inserters):
        k = payload["keypoint"]
        offset = payload["offset"]
        stepping = payload.get("stepping", 0)
        store_id = conn.execute(
            sqla.select(table.c.serial).filter(
                table.c.keypoint_serial == k.store_id,
                table.c.ka_offset == offset,
                table.c.stepping == stepping,
            )
        ).scalar_one_or_none()
        obj = keypoint_alias(store_id, k, offset, stepping)
        if store_id is not None:
            obj._deserialized = True
        return obj

    @staticmethod
    def store(obj, conn, table, inserter, tables, inserters):
        payload = {
            "keypoint_serial": obj.keypoint.store_id,
            "ka_offset": obj.offset,
            "stepping": obj.stepping,
        }
        if obj._my_id is not None:
            # a replica: insert under the controller's serial, or verify that it is held
            serial = obj._my_id
            row = (
                conn.execute(sqla.select(table).filter(table.c.serial == serial))
                .mappings()
                .one_or_none()
            )
            if row is not None:
                differing = differing_columns(payload, row)
                if len(differing) > 0:
                    raise ReplicationMismatch(
                        None,
                        "keypoint_alias",
                        serial,
                        serial,
                        detail=f"the row under this serial differs in {differing}",
                    )
                return obj
            others = (
                conn.execute(
                    sqla.select(table.c.serial).filter(
                        *[table.c[name] == value for name, value in payload.items()]
                    )
                )
                .scalars()
                .all()
            )
            if len(others) > 0:
                raise ReplicationMismatch(
                    None,
                    "keypoint_alias",
                    serial,
                    others[0],
                    detail="the key is held under another serial",
                )
            payload["serial"] = serial

        obj._my_id = inserter(conn, payload)
        return obj

    @staticmethod
    def inventory_spec():
        return InventorySpec(
            leaves=("ka_offset", "stepping"),
            parents={"keypoint": Parent("keypoint_serial", "keypoint")},
        )


# ------------------------------------------------------------------------------------------------
# the replicated owner, its tags and its value rows
# ------------------------------------------------------------------------------------------------


class Gadget_tags_factory(SQLAFactoryBase):
    """The tag table of the replicated Gadget: no serial of its own."""

    @staticmethod
    def register():
        return {
            "serial": False,
            "version": False,
            "stepping": False,
            "timestamp": True,
            "columns": [
                sqla.Column(
                    "gadget_serial",
                    sqla.Integer,
                    sqla.ForeignKey("Gadget.serial"),
                    index=True,
                    nullable=False,
                    primary_key=True,
                ),
                sqla.Column(
                    TAG_SERIAL,
                    sqla.Integer,
                    sqla.ForeignKey(f"{TAG_TABLE}.serial"),
                    index=True,
                    nullable=False,
                    primary_key=True,
                ),
            ],
        }

    @staticmethod
    def build(payload, conn, table, inserter, tables, inserters):
        raise NotImplementedError("Gadget_tags rows are written by Gadget's store")


class GadgetPart_factory(SQLAFactoryBase):
    """The value rows a Gadget owns: ``owner_column`` names the Gadget each belongs to."""

    @staticmethod
    def register():
        return {
            "version": False,
            "timestamp": False,
            "owner_column": "gadget_serial",
            "columns": [
                sqla.Column(
                    "gadget_serial",
                    sqla.Integer,
                    sqla.ForeignKey("Gadget.serial"),
                    index=True,
                    nullable=False,
                ),
                sqla.Column("part_index", sqla.Integer, nullable=False),
                sqla.Column("part_value", sqla.Float(64), nullable=False),
            ],
        }

    @staticmethod
    def build(payload, conn, table, inserter, tables, inserters):
        gadget_serial = payload["gadget_serial"]
        part_index = payload["part_index"]
        row = conn.execute(
            sqla.select(table.c.serial, table.c.part_value).filter(
                table.c.gadget_serial == gadget_serial,
                table.c.part_index == part_index,
            )
        ).one_or_none()
        if row is not None:
            return _new(
                GadgetPart(row.serial, part_index, row.part_value),
                {"_deserialized": True},
            )
        data = {
            "gadget_serial": gadget_serial,
            "part_index": part_index,
            "part_value": payload["part_value"],
        }
        if "serial" in payload:
            data["serial"] = payload["serial"]
        store_id = inserter(conn, data)
        return _new(
            GadgetPart(store_id, part_index, payload["part_value"]),
            {"_new_insert": True},
        )


class Gadget_factory(SQLAFactoryBase):
    """
    The replicated owner class. A Gadget is validated when it holds as many ``GadgetPart`` rows
    as its ``part_count`` says; ``validate`` and ``revalidate`` apply that one rule, and
    ``validate_on_startup`` reports, or prunes, the Gadgets that fail it, with their tag and part
    rows. ``owned_serials`` gives the serials of its parts, which a replica must store them under.
    """

    @staticmethod
    def register():
        return {
            "version": True,
            "timestamp": True,
            "stepping": False,
            "validate_on_startup": True,
            # after an interrupted validate, the pool's check at open recomputes it by revalidate()
            "validated_column": "gadget_validated",
            "columns": [
                sqla.Column(
                    "gadget_label", sqla.String(DEFAULT_STRING_LENGTH), nullable=False
                ),
                # the polymorphic parent: frame_kind names the class, frame_serial the row. No
                # foreign key, since the class differs from row to row
                sqla.Column("frame_kind", sqla.Integer, index=True, nullable=False),
                sqla.Column("frame_serial", sqla.Integer, index=True, nullable=False),
                sqla.Column("part_count", sqla.Integer, nullable=False),
                sqla.Column(
                    "gadget_validated", sqla.Boolean, default=False, nullable=False
                ),
            ],
        }

    @staticmethod
    def _key(obj) -> dict:
        return {
            "gadget_label": obj.label,
            "frame_kind": FRAME_KINDS[type(obj.frame).__name__],
            "frame_serial": obj.frame.store_id,
        }

    @staticmethod
    def _parts(conn, tables, serial: int) -> List[GadgetPart]:
        parts = tables["GadgetPart"]
        return [
            GadgetPart(row.serial, row.part_index, row.part_value)
            for row in conn.execute(
                sqla.select(parts.c.serial, parts.c.part_index, parts.c.part_value)
                .filter(parts.c.gadget_serial == serial)
                .order_by(parts.c.part_index)
            )
        ]

    @staticmethod
    def build(payload, conn, table, inserter, tables, inserters):
        obj = Gadget(None, payload["label"], payload["frame"], payload.get("tags", ()))
        key = Gadget_factory._key(obj)
        wanted = _tag_serials(obj.tags)
        for serial in (
            conn.execute(
                sqla.select(table.c.serial)
                .filter(
                    table.c.gadget_validated == True,
                    *[table.c[name] == value for name, value in key.items()],
                )
                .order_by(table.c.serial)
            )
            .scalars()
            .all()
        ):
            tags = tables["Gadget_tags"]
            if _stored_tag_serials(conn, tags, "gadget_serial", serial) == wanted:
                obj._my_id = serial
                obj.parts = Gadget_factory._parts(conn, tables, serial)
                obj.validated = True
                obj._deserialized = True
                break
        return obj

    @staticmethod
    def store(obj, conn, table, inserter, tables, inserters):
        payload = {
            **Gadget_factory._key(obj),
            "part_count": len(obj.parts),
            "gadget_validated": False,
        }
        tag_table = tables["Gadget_tags"]
        part_table = tables["GadgetPart"]
        replica = obj._my_id is not None

        if replica:
            serial = obj._my_id
            wanted = _tag_serials(obj.tags)

            def mismatch(replica_serial, detail):
                return ReplicationMismatch(
                    None, "Gadget", serial, replica_serial, detail=detail
                )

            row = (
                conn.execute(sqla.select(table).filter(table.c.serial == serial))
                .mappings()
                .one_or_none()
            )
            if row is not None:
                # the validated flag is not compared: store writes False, validate sets it
                differing = differing_columns(
                    {k: v for k, v in payload.items() if k != "gadget_validated"}, row
                )
                if len(differing) > 0:
                    raise mismatch(
                        serial, f"the row under this serial differs in {differing}"
                    )
                held = _stored_tag_serials(conn, tag_table, "gadget_serial", serial)
                if held != wanted:
                    raise mismatch(
                        serial, f"its tags are {held}, the controller's {wanted}"
                    )
                stored = {
                    p.store_id: (p.part_index, p.part_value)
                    for p in Gadget_factory._parts(conn, tables, serial)
                }
                expected = {p._my_id: (p.part_index, p.part_value) for p in obj.parts}
                if stored != expected:
                    raise mismatch(
                        serial,
                        f"its part rows are {sorted(stored)}, the controller's "
                        f"{sorted(expected)}",
                    )
                return obj

            # the key held under another serial, among validated rows with these tags
            for other in (
                conn.execute(
                    sqla.select(table.c.serial).filter(
                        table.c.gadget_validated == True,
                        *[
                            table.c[name] == payload[name]
                            for name in ("gadget_label", "frame_kind", "frame_serial")
                        ],
                    )
                )
                .scalars()
                .all()
            ):
                if (
                    _stored_tag_serials(conn, tag_table, "gadget_serial", other)
                    == wanted
                ):
                    raise mismatch(other, "the key is held under another serial")

            part_serials = [p._my_id for p in obj.parts]
            if any(s is None for s in part_serials):
                raise mismatch(
                    serial, "the controller's object does not carry its part serials"
                )
            taken = (
                conn.execute(
                    sqla.select(part_table.c.serial).filter(
                        part_table.c.serial.in_(part_serials)
                    )
                )
                .scalars()
                .all()
            )
            if len(taken) > 0:
                raise mismatch(
                    serial, f"part serials {sorted(taken)} are already taken"
                )
            payload["serial"] = serial

        store_id = inserter(conn, payload)
        obj._my_id = store_id

        for tag in obj.tags:
            inserters["Gadget_tags"](
                conn, {"gadget_serial": store_id, TAG_SERIAL: tag.store_id}
            )
        for part in obj.parts:
            data = {
                "gadget_serial": store_id,
                "part_index": part.part_index,
                "part_value": part.part_value,
            }
            if replica:
                data["serial"] = part._my_id
            part._my_id = inserters["GadgetPart"](conn, data)
        return obj

    @staticmethod
    def _validate_row(serial: int, conn, table, tables) -> bool:
        """The one rule: as many part rows as part_count. Writes the flag and returns it."""
        expected = conn.execute(
            sqla.select(table.c.part_count).filter(table.c.serial == serial)
        ).scalar_one()
        parts = tables["GadgetPart"]
        held = conn.execute(
            sqla.select(sqla.func.count(parts.c.serial)).filter(
                parts.c.gadget_serial == serial
            )
        ).scalar()
        validated = held == expected
        conn.execute(
            sqla.update(table)
            .where(table.c.serial == serial)
            .values(gadget_validated=validated)
        )
        return validated

    @staticmethod
    def validate(obj, conn, table, tables):
        if not obj.available:
            raise RuntimeError("Gadget.validate: the object has not been stored")
        return Gadget_factory._validate_row(obj.store_id, conn, table, tables)

    @staticmethod
    def revalidate(serial, conn, table, tables) -> bool:
        return Gadget_factory._validate_row(serial, conn, table, tables)

    @staticmethod
    def owned_serials(obj) -> Optional[List[Optional[int]]]:
        parts = getattr(obj, "parts", None)
        if parts is None:
            return None
        return [getattr(part, "_my_id", None) for part in parts]

    @staticmethod
    def validate_on_startup(conn, table, tables, prune=False):
        unvalidated = list(
            conn.execute(
                sqla.select(table.c.serial, table.c.gadget_label, table.c.part_count)
                .filter(
                    sqla.or_(
                        table.c.gadget_validated == False,
                        table.c.gadget_validated == None,
                    )
                )
                .order_by(table.c.serial)
            )
        )
        if len(unvalidated) == 0:
            return []

        msgs = [">> Gadget", "     unvalidated rows:"]
        for row in unvalidated:
            msgs.append(
                f'       -- "{row.gadget_label}" (store_id={row.serial}, '
                f"part_count={row.part_count})"
            )
        if prune:
            serials = [row.serial for row in unvalidated]
            try:
                for name, column in (
                    ("GadgetPart", "gadget_serial"),
                    ("Gadget_tags", "gadget_serial"),
                ):
                    owned = tables[name]
                    conn.execute(sqla.delete(owned).where(owned.c[column].in_(serials)))
                conn.execute(sqla.delete(table).where(table.c.serial.in_(serials)))
            except SQLAlchemyError:
                msgs.append(
                    "!!        DATABASE ERROR encountered when pruning these rows"
                )
            else:
                msgs.append("     ** Note: these rows have been pruned.")
        return msgs

    @staticmethod
    def inventory_spec():
        return InventorySpec(
            leaves=("gadget_label", "frame_kind"),
            parents={
                "frame": Parent(
                    "frame_serial", type_column="frame_kind", types=FRAME_TYPES
                )
            },
            tags=("Gadget_tags", "gadget_serial"),
            values=("GadgetPart", "gadget_serial"),
            validated="gadget_validated",
        )


# ------------------------------------------------------------------------------------------------
# the sharded classes
# ------------------------------------------------------------------------------------------------


class Tessera_factory(SQLAFactoryBase):
    """A sharded leaf, keyed on a keypoint_alias (the shard key's proxy)."""

    @staticmethod
    def register():
        return {
            "version": True,
            "timestamp": True,
            "columns": [
                sqla.Column(
                    "alias_serial",
                    sqla.Integer,
                    sqla.ForeignKey("keypoint_alias.serial"),
                    index=True,
                    nullable=False,
                ),
                sqla.Column("tessera_weight", sqla.Float(64), nullable=False),
            ],
        }

    @staticmethod
    def build(payload, conn, table, inserter, tables, inserters):
        alias = payload["k"]
        weight = payload["weight"]
        store_id = conn.execute(
            sqla.select(table.c.serial).filter(
                table.c.alias_serial == alias.store_id,
                table.c.tessera_weight == weight,
            )
        ).scalar_one_or_none()
        attributes = {"_deserialized": True}
        if store_id is None:
            store_id = inserter(
                conn, {"alias_serial": alias.store_id, "tessera_weight": weight}
            )
            attributes = {"_new_insert": True}
        return _new(Tessera(store_id, alias, weight), attributes)

    @staticmethod
    def inventory_spec():
        return InventorySpec(
            leaves=("tessera_weight",),
            parents={"k": Parent("alias_serial", "keypoint_alias")},
        )


class Sample_tags_factory(SQLAFactoryBase):
    """The tag association of the sharded Sample."""

    @staticmethod
    def register():
        return {
            "serial": False,
            "version": False,
            "timestamp": True,
            "columns": [
                sqla.Column(
                    "sample_serial",
                    sqla.Integer,
                    sqla.ForeignKey("Sample.serial"),
                    index=True,
                    nullable=False,
                    primary_key=True,
                ),
                sqla.Column(
                    TAG_SERIAL,
                    sqla.Integer,
                    sqla.ForeignKey(f"{TAG_TABLE}.serial"),
                    index=True,
                    nullable=False,
                    primary_key=True,
                ),
            ],
        }

    @staticmethod
    def build(payload, conn, table, inserter, tables, inserters):
        raise NotImplementedError("Sample_tags rows are written by Sample's store")


class Sample_members_factory(SQLAFactoryBase):
    """The member table of Sample's set of parents: one row per Tessera a Sample is keyed on,
    each on the Sample's own shard. It declares no inventory_spec; it names its rows by foreign
    key."""

    @staticmethod
    def register():
        return {
            "serial": False,
            "version": False,
            "timestamp": False,
            "columns": [
                sqla.Column(
                    "sample_serial",
                    sqla.Integer,
                    sqla.ForeignKey("Sample.serial"),
                    index=True,
                    nullable=False,
                    primary_key=True,
                ),
                sqla.Column(
                    "tessera_serial",
                    sqla.Integer,
                    sqla.ForeignKey("Tessera.serial"),
                    index=True,
                    nullable=False,
                    primary_key=True,
                ),
            ],
        }

    @staticmethod
    def build(payload, conn, table, inserter, tables, inserters):
        raise NotImplementedError("Sample_members rows are written by Sample's store")


class Sample_factory(SQLAFactoryBase):
    """
    The sharded parent class, sharded on ``k`` (a keypoint). A Sample is validated when it holds
    as many member rows as its ``member_count`` says. ``validate_on_startup`` reports, or (in each
    actor, under ``prune_unvalidated``) prunes, the Samples that fail it, with their tag and member
    rows. ``read_batch`` reads every Sample of one keypoint.
    """

    @staticmethod
    def register():
        return {
            "version": True,
            "timestamp": True,
            "validate_on_startup": True,
            "columns": [
                sqla.Column(
                    "keypoint_serial",
                    sqla.Integer,
                    sqla.ForeignKey("keypoint.serial"),
                    index=True,
                    nullable=False,
                ),
                sqla.Column(
                    "gadget_serial",
                    sqla.Integer,
                    sqla.ForeignKey("Gadget.serial"),
                    index=True,
                    nullable=False,
                ),
                # a Tessera that may be on another shard: no foreign key
                sqla.Column("anchor_serial", sqla.Integer, index=True, nullable=True),
                sqla.Column(
                    "sample_code", sqla.String(DEFAULT_STRING_LENGTH), nullable=False
                ),
                sqla.Column("member_count", sqla.Integer, nullable=False),
                sqla.Column(
                    "sample_validated", sqla.Boolean, default=False, nullable=False
                ),
            ],
        }

    @staticmethod
    def _populated(conn, tables, row, k, gadget) -> Sample:
        members = tables["Sample_members"]
        member_serials = (
            conn.execute(
                sqla.select(members.c.tessera_serial)
                .filter(members.c.sample_serial == row.serial)
                .order_by(members.c.tessera_serial)
            )
            .scalars()
            .all()
        )
        obj = Sample(
            row.serial,
            k,
            gadget,
            row.sample_code,
            tags=_stored_tags(
                conn, tables, tables["Sample_tags"], "sample_serial", row.serial
            ),
            members=[SerialHandle(s) for s in member_serials],
            anchor=(
                SerialHandle(row.anchor_serial)
                if row.anchor_serial is not None
                else None
            ),
            validated=bool(row.sample_validated),
        )
        obj._deserialized = True
        return obj

    @staticmethod
    def build(payload, conn, table, inserter, tables, inserters):
        k = payload["k"]
        gadget = payload["gadget"]
        code = payload["code"]
        tags = payload.get("tags", ())
        wanted = _tag_serials(tags)
        for row in conn.execute(
            sqla.select(table)
            .filter(
                table.c.keypoint_serial == k.store_id,
                table.c.gadget_serial == gadget.store_id,
                table.c.sample_code == code,
                table.c.sample_validated == True,
            )
            .order_by(table.c.serial)
        ).all():
            held = _stored_tag_serials(
                conn, tables["Sample_tags"], "sample_serial", row.serial
            )
            if held == wanted:
                return Sample_factory._populated(conn, tables, row, k, gadget)
        return Sample(None, k, gadget, code, tags=tags)

    @staticmethod
    def store(obj, conn, table, inserter, tables, inserters):
        store_id = inserter(
            conn,
            {
                "keypoint_serial": obj.k.store_id,
                "gadget_serial": obj.gadget.store_id,
                "anchor_serial": (
                    obj.anchor.store_id if obj.anchor is not None else None
                ),
                "sample_code": obj.code,
                "member_count": len(obj.members),
                "sample_validated": False,
            },
        )
        obj._my_id = store_id
        for tag in obj.tags:
            inserters["Sample_tags"](
                conn, {"sample_serial": store_id, TAG_SERIAL: tag.store_id}
            )
        for member in obj.members:
            inserters["Sample_members"](
                conn, {"sample_serial": store_id, "tessera_serial": member.store_id}
            )
        return obj

    @staticmethod
    def validate(obj, conn, table, tables):
        if not obj.available:
            raise RuntimeError("Sample.validate: the object has not been stored")
        members = tables["Sample_members"]
        expected = conn.execute(
            sqla.select(table.c.member_count).filter(table.c.serial == obj.store_id)
        ).scalar_one()
        held = conn.execute(
            sqla.select(sqla.func.count()).filter(
                members.c.sample_serial == obj.store_id
            )
        ).scalar()
        validated = held == expected
        conn.execute(
            sqla.update(table)
            .where(table.c.serial == obj.store_id)
            .values(sample_validated=validated)
        )
        return validated

    @staticmethod
    def validate_on_startup(conn, table, tables, prune=False):
        unvalidated = list(
            conn.execute(
                sqla.select(table.c.serial, table.c.sample_code)
                .filter(
                    sqla.or_(
                        table.c.sample_validated == False,
                        table.c.sample_validated == None,
                    )
                )
                .order_by(table.c.serial)
            )
        )
        if len(unvalidated) == 0:
            return []

        msgs = [">> Sample", "     unvalidated rows:"]
        for row in unvalidated:
            msgs.append(f'       -- "{row.sample_code}" (store_id={row.serial})')
        if prune:
            serials = [row.serial for row in unvalidated]
            try:
                for name in ("Sample_members", "Sample_tags"):
                    owned = tables[name]
                    conn.execute(
                        sqla.delete(owned).where(owned.c.sample_serial.in_(serials))
                    )
                conn.execute(sqla.delete(table).where(table.c.serial.in_(serials)))
            except SQLAlchemyError:
                msgs.append(
                    "!!        DATABASE ERROR encountered when pruning these rows"
                )
            else:
                msgs.append("     ** Note: these rows have been pruned.")
        return msgs

    @staticmethod
    def read_batch(payload, conn, table, tables):
        # the pool adds the shard key to the payload: every Sample of that keypoint, in serial
        # order, each with its tags and members; validated ones only unless asked otherwise
        k = payload["k"]
        query = sqla.select(table).filter(table.c.keypoint_serial == k.store_id)
        if payload.get("validated_only", True):
            query = query.filter(table.c.sample_validated == True)
        return [
            Sample_factory._populated(
                conn, tables, row, k, SerialHandle(row.gadget_serial)
            )
            for row in conn.execute(query.order_by(table.c.serial)).all()
        ]

    @staticmethod
    def inventory_spec():
        return InventorySpec(
            leaves=("sample_code",),
            parents={
                "k": Parent("keypoint_serial", "keypoint"),
                "gadget": Parent("gadget_serial", "Gadget"),
                # a NULL anchor is a value of the key; one that is set may be on another shard
                "anchor": Parent(
                    "anchor_serial", "Tessera", nullable=True, cross_shard=True
                ),
            },
            tags=("Sample_tags", "sample_serial"),
            validated="sample_validated",
            parent_sets={
                "members": ParentSet(
                    table="Sample_members",
                    owner="sample_serial",
                    members={"piece": Parent("tessera_serial", "Tessera")},
                )
            },
        )
