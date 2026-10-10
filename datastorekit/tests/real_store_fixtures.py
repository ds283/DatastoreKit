"""
A small **real** ShardedPool store on disk, for tests of the read-only reader and what is built on
it, in a directory the caller gives. No Ray, no actor.

``shard_store_fixtures`` makes a primary with placeholder shards, which are text files and cannot
be read as databases. This module makes shards that are SQLite databases:

- the primary is written by ``ShardedPool._write_shard_data`` itself, on a pool made without its
  constructor (``shard_store_fixtures.bare_pool``), with the replicated and sharded table lists of
  the neutral client's registry. The shard-key rows are then added through the pool's own
  ``shard_keys`` table;
- every shard holds every table ``build_schema`` declares, created on a temporary read-write
  engine that is disposed before the builder returns. No journal file is left behind;
- replicated rows (``REPLICATED_ROWS``) are copied into every shard, with the same serials, as
  ``ShardedPool`` replicates them;
- sharded rows (``SHARDED_ROWS``) go into the shard their key names. Shards 0 and 1 each hold a
  ``Trace`` with ``Trace_tags`` rows and ``TraceStep`` rows.

**Adding rows.** The row sets are plain data: table name -> list of column -> value dicts, with
explicit serials. A test adds rows by passing its own ``replicated`` / ``sharded`` mappings to
``build_real_store``, usually built with ``with_rows`` from the defaults. A ``timestamp`` column
that a row leaves out is filled with ``FIXED_TIMESTAMP``, as ``Datastore._insert`` fills it with the
time; every other value is the row's own.

**A store whose schema differs.** ``build_real_store`` and ``build_full_store`` take
``missing_tables``, ``missing_columns`` and ``extra_sql``, which build a shard that lacks a declared
table or column, or has a table or column the code does not declare. The current code writes no such
shard; the refusal tests use them to show that every reader refuses one by name.

**The full store.** ``build_full_store`` builds a store holding at least one row of every class of
the structured inventory, with tags, unvalidated rows and value rows (``FULL_REPLICATED_ROWS``,
``FULL_SHARDED_ROWS``). It leaves the defaults above as they are. ``relabel_serials`` gives the same
content under other serials, and ``vary_row`` changes one column of one row.

Ported by prompt 04a of the extraction campaign: the mechanics are the source's, and the rows are
the neutral client's, designed with ``test_store_inventory``, which addresses them.

This module is not a test module (no ``test_`` prefix); the test modules import it.
"""

import copy
import hashlib
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Tuple

import sqlalchemy as sqla

from datastorekit.tests.client.registry import factories as _factories
from datastorekit.SQL.schema import build_schema
from datastorekit.shard_paths import shard_file_name
from datastorekit.store_inventory import inventory_specs
from datastorekit.tests.client.factories import FRAME_KINDS
from datastorekit.tests.shard_store_fixtures import bare_pool
from datastorekit.tests.client.registry import replicated_tables, sharded_tables

RowSet = Dict[str, List[Dict[str, object]]]

FIXED_TIMESTAMP = datetime(2026, 9, 24, 12, 0, 0)

# the polymorphic frame's type values (the client's FRAME_KINDS): a dial setting and a knob setting
_DIAL_KIND = FRAME_KINDS["dial_setting"]

REPLICATED_ROWS: RowSet = {
    "version": [{"serial": 1, "label": "2025.1.1"}],
    "store_tag": [
        {"serial": 1, "label": "fixture-run"},
        {"serial": 2, "label": "grid-A"},
        {"serial": 3, "label": "unused-tag"},
    ],
    "keypoint": [
        {"serial": 1, "kp_position": 0.1, "kp_marked": True, "kp_flagged": True},
        {"serial": 2, "kp_position": 1.0, "kp_marked": True, "kp_flagged": True},
    ],
    "routing_rule": [
        {
            "serial": 1,
            "version": 1,
            "rule_label": "rule-a",
            "rule_threshold": -5.0,
            "rule_mode": "prefer-direct",
        },
        {
            "serial": 2,
            "version": 1,
            "rule_label": "rule-b",
            "rule_threshold": -7.0,
            "rule_mode": "prefer-direct",
        },
    ],
    "dial_setting": [{"serial": 1, "dial_level": 3, "stepping": 1}],
    "gauge_setting": [{"serial": 1, "gauge_exponent": 4}],
    "keypoint_alias": [
        {
            "serial": 1,
            "version": 1,
            "stepping": 0,
            "keypoint_serial": 1,
            "ka_offset": 0.125,
        },
        {
            "serial": 2,
            "version": 1,
            "stepping": 0,
            "keypoint_serial": 2,
            "ka_offset": 0.125,
        },
    ],
    "Gadget": [
        {
            "serial": 1,
            "version": 1,
            "gadget_label": "fixture-gadget",
            "frame_kind": _DIAL_KIND,
            "frame_serial": 1,
            "part_count": 3,
            "gadget_validated": True,
        }
    ],
    "Gadget_tags": [{"gadget_serial": 1, "tag_serial": 1}],
    "GadgetPart": [
        {"serial": s, "gadget_serial": 1, "part_index": i, "part_value": 1.0 / s}
        for s, i in ((1, 0), (2, 1), (3, 2))
    ],
}


def _trace(serial: int, keypoint_serial: int, steps: int) -> RowSet:
    """One validated Trace on the dial frame, with two tags and ``steps`` steps, step serials
    offset by ``serial``."""
    return {
        "Trace": [
            {
                "serial": serial,
                "version": 1,
                "keypoint_serial": keypoint_serial,
                "frame_kind": _DIAL_KIND,
                "frame_serial": 1,
                "trace_label": f"fixture-trace-{serial}",
                "step_count": steps,
                "trace_validated": True,
            }
        ],
        "Trace_tags": [
            {"trace_serial": serial, "tag_serial": 1},
            {"trace_serial": serial, "tag_serial": 2},
        ],
        "TraceStep": [
            {
                "serial": 10 * serial + i,
                "trace_serial": serial,
                "step_index": i,
                "step_value": 1.0 / i,
            }
            for i in range(1, steps + 1)
        ],
    }


# shard serial -> rows in that shard. The shard key is the keypoint (the registry's
# shard_key_type): keypoint 1 lives on shard 0 and keypoint 2 on shard 1 (SHARD_KEYS)
SHARDED_ROWS: Dict[int, RowSet] = {
    0: _trace(serial=1, keypoint_serial=1, steps=3),
    1: _trace(serial=2, keypoint_serial=2, steps=4),
}

# keypoint serial -> shard serial, written to the primary's shard_keys table
SHARD_KEYS: Dict[int, int] = {1: 0, 2: 1}


@dataclass(frozen=True)
class RealStore:
    """A store built by ``build_real_store``: its primary and its shard files, by serial."""

    primary: Path
    shard_files: Dict[int, Path]
    replicated: RowSet
    sharded: Dict[int, RowSet]

    @property
    def directory(self) -> Path:
        return self.primary.parent


def with_rows(base: RowSet, extra: RowSet) -> RowSet:
    """A copy of ``base`` with ``extra``'s rows appended, table by table."""
    out = copy.deepcopy(base)
    for table, rows in extra.items():
        out.setdefault(table, []).extend(copy.deepcopy(rows))
    return out


def _write_primary(
    primary: Path, shard_files: Dict[int, Path], shard_keys: Mapping[int, int]
) -> None:
    pool = bare_pool(primary)
    pool._ShardKeyType_name = "keypoint"
    pool._replicated_tables = list(replicated_tables)
    pool._sharded_tables = dict(sharded_tables)
    pool._shard_db_files = dict(shard_files)
    pool._create_engine()
    try:
        pool._write_shard_data()
        if len(shard_keys) > 0:
            with pool._engine.begin() as conn:
                conn.execute(
                    sqla.insert(pool._shard_key_table),
                    [
                        {"key_serial": key, "shard_id": shard}
                        for key, shard in sorted(shard_keys.items())
                    ],
                )
    finally:
        pool._engine.dispose()


def _insert_rows(conn, tables: Mapping[str, sqla.Table], rows: RowSet) -> None:
    for name, table_rows in rows.items():
        if len(table_rows) == 0:
            continue
        table = tables[name]
        payload = []
        for row in table_rows:
            row = dict(row)
            if "timestamp" in table.c and "timestamp" not in row:
                row["timestamp"] = FIXED_TIMESTAMP
            payload.append(row)
        conn.execute(sqla.insert(table), payload)


def _write_shard(
    path: Path,
    rows: List[RowSet],
    missing_tables: Iterable[str],
    missing_columns: Mapping[str, Iterable[str]],
    extra_sql: Iterable[str] = (),
) -> None:
    metadata = sqla.MetaData()
    built = build_schema(metadata, _factories)
    missing_tables = set(missing_tables)

    engine = sqla.create_engine(f"sqlite:///{path}", future=True)
    try:
        created = [t for n, t in built.tables.items() if n not in missing_tables]
        metadata.create_all(engine, tables=created)
        with engine.begin() as conn:
            for row_set in rows:
                _insert_rows(conn, built.tables, row_set)
    finally:
        engine.dispose()

    # a shard whose table lacks a column the code declares. The column is dropped after the
    # rows are written, so that the rest of each row is still there (SQLite >= 3.35). Then any
    # extra statements (a column or a table the code does not declare) are run
    statements = [
        f'ALTER TABLE "{table}" DROP COLUMN "{column}"'
        for table, columns in missing_columns.items()
        for column in columns
    ] + list(extra_sql)
    if len(statements) > 0:
        conn = sqlite3.connect(path)
        try:
            with conn:
                for statement in statements:
                    conn.execute(statement)
        finally:
            conn.close()


def build_real_store(
    directory: Path,
    stem: str = "fixture-store",
    shards: int = 2,
    replicated: Optional[RowSet] = None,
    sharded: Optional[Dict[int, RowSet]] = None,
    shard_keys: Optional[Mapping[int, int]] = None,
    missing_tables: Optional[Mapping[int, Iterable[str]]] = None,
    missing_columns: Optional[Mapping[int, Mapping[str, Iterable[str]]]] = None,
    extra_sql: Optional[Mapping[int, Iterable[str]]] = None,
) -> RealStore:
    """
    Build a real store in ``directory`` (which must exist) and return it.

    ``replicated`` rows go into every shard with the same serials; ``sharded[n]`` rows go into
    shard ``n`` only. Both default to this module's row sets. ``missing_tables[n]`` lists tables
    shard ``n`` is created without; ``missing_columns[n][table]`` lists columns dropped from that
    table on shard ``n``. No row may be given for a missing table. ``extra_sql[n]`` lists SQL
    statements run on shard ``n`` last, e.g. to add a column or a table the code does not declare.
    """
    replicated = copy.deepcopy(REPLICATED_ROWS if replicated is None else replicated)
    sharded = copy.deepcopy(SHARDED_ROWS if sharded is None else sharded)
    shard_keys = dict(SHARD_KEYS if shard_keys is None else shard_keys)
    missing_tables = {} if missing_tables is None else missing_tables
    missing_columns = {} if missing_columns is None else missing_columns
    extra_sql = {} if extra_sql is None else extra_sql

    if shards < 2:
        raise ValueError("a real store fixture has at least two shards")
    unknown = set(sharded) - set(range(shards))
    if unknown:
        raise ValueError(
            f"sharded rows name shards {sorted(unknown)} that do not exist"
        )

    primary = (Path(directory) / f"{stem}.sqlite").resolve()
    shard_files = {
        serial: primary.parent / shard_file_name(primary, serial)
        for serial in range(shards)
    }

    for serial, path in shard_files.items():
        _write_shard(
            path,
            [replicated, sharded.get(serial, {})],
            missing_tables.get(serial, ()),
            missing_columns.get(serial, {}),
            extra_sql.get(serial, ()),
        )

    _write_primary(primary, shard_files, shard_keys)

    return RealStore(
        primary=primary,
        shard_files=shard_files,
        replicated=replicated,
        sharded=sharded,
    )


def expected_row_counts(store: RealStore, serial: int) -> Dict[str, int]:
    """Rows this fixture put in each table of shard ``serial`` (tables it left empty omitted)."""
    counts: Dict[str, int] = {}
    for row_set in (store.replicated, store.sharded.get(serial, {})):
        for table, rows in row_set.items():
            counts[table] = counts.get(table, 0) + len(rows)
    return counts


def independent_row_counts(path: Path) -> Dict[str, int]:
    """Every table's row count in the file ``path``, read with stdlib ``sqlite3`` ``mode=ro``,
    independently of the reader and of SQLAlchemy."""
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        names = [
            r[0]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' "
                "AND name NOT LIKE 'sqlite_%' ORDER BY name"
            )
        ]
        return {
            name: conn.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
            for name in names
        }
    finally:
        conn.close()


def file_state(directory: Path) -> Tuple[List[str], Dict[str, Tuple[str, int, int]]]:
    """The directory listing, and each file's (SHA-256, size, st_mtime_ns)."""
    listing = sorted(p.name for p in Path(directory).iterdir())
    state = {}
    for name in listing:
        path = Path(directory) / name
        st = path.lstat()
        state[name] = (
            hashlib.sha256(path.read_bytes()).hexdigest(),
            st.st_size,
            st.st_mtime_ns,
        )
    return listing, state


# ---------------------------------------------------------------------------------------------
# a full store: every inventory class
# ---------------------------------------------------------------------------------------------
#
# ``build_full_store`` builds a store holding at least one row of every class of the structured
# inventory (datastorekit/store_inventory.py inventory_classes), with tags wherever the class has an
# association table, unvalidated rows, and value rows. It adds to the defaults above and leaves them
# as they are, so a test written against the defaults reads the store it was written against.
#
# Every row states the columns of its key and its references explicitly. Any other non-nullable
# column a row leaves out is filled by ``fill_required`` with a placeholder of its type.
#
# ``relabel_serials`` gives the same content under different serials, and ``vary_row`` changes one
# column of one row, so that tests can build two stores that differ in exactly one respect.
#
# The neutral rows (extraction prompt 04a). Every serial of a sharded table is unique across the
# shards, as a store's are. The rows hold:
#
# - two version rows; a run tag ("fixture-run") that every tagged record carries, and a tag no row
#   carries ("unused-tag");
# - both frame kinds, each referenced by a Gadget and by a Trace; dial setting 1 and knob setting
#   1 share serial 1, so that a frame kind can be varied to the other and still resolve;
# - unvalidated rows of Gadget (2), Trace (3) and Sample (4), and a different value count per
#   parent, for Gadget (3, 2) and for Trace (3, 4, 2, 1). Every part, step and member count equals
#   the rows it counts;
# - exactly one Weave, sharing serial 1 with Trace 1 (which no Weave names), tagged with "weave-tag"
#   beside the run tag, with no anchor, and with two strands: one with no origin, one with no anchor;
# - every Sample anchored on a Tessera of the other shard (a cross-shard parent), and every
#   Sample_members row naming a Tessera whose serial is also a Sample serial on its shard (so that
#   a foreign key wrongly declared into Sample would hold on them by coincidence);
# - for every identity field of every inventory class, a second row it can be varied to.

_KNOB_KIND = FRAME_KINDS["knob_setting"]

FULL_REPLICATED_ROWS: RowSet = with_rows(
    REPLICATED_ROWS,
    {
        "version": [{"serial": 2, "label": "2024.9.9"}],
        "store_tag": [
            {"serial": 4, "label": "grid-B"},
            {"serial": 5, "label": "weave-tag"},
        ],
        "keypoint": [
            {"serial": 3, "kp_position": 0.5, "kp_marked": True, "kp_flagged": True}
        ],
        "routing_rule": [
            {
                "serial": 3,
                "version": 1,
                "rule_label": "rule-c",
                "rule_threshold": -9.0,
                "rule_mode": "prefer-direct",
            }
        ],
        "dial_setting": [{"serial": 2, "dial_level": 5, "stepping": 0}],
        "knob_setting": [{"serial": 1, "knob_turns": 7, "stepping": 2}],
        "gauge_setting": [{"serial": 2, "gauge_exponent": 8}],
        "keypoint_alias": [
            {
                "serial": 3,
                "version": 1,
                "stepping": 0,
                "keypoint_serial": 3,
                "ka_offset": 0.125,
            },
            {
                "serial": 4,
                "version": 1,
                "stepping": 0,
                "keypoint_serial": 1,
                "ka_offset": 0.25,
            },
        ],
        "Gadget": [
            {
                "serial": 2,
                "version": 1,
                "gadget_label": "fixture-gadget-knob",
                "frame_kind": _KNOB_KIND,
                "frame_serial": 1,
                "part_count": 2,
                "gadget_validated": False,
            }
        ],
        "Gadget_tags": [
            {"gadget_serial": 1, "tag_serial": 2},
            {"gadget_serial": 2, "tag_serial": 1},
        ],
        "GadgetPart": [
            {"serial": s, "gadget_serial": 2, "part_index": i, "part_value": 1.0 / s}
            for s, i in ((4, 0), (5, 1))
        ],
    },
)


def _values(table: str, parent_column: str, parent: int, serials_and_index) -> RowSet:
    return {
        table: [
            {
                "serial": serial,
                parent_column: parent,
                "step_index": index,
                "step_value": 0.5 * index,
            }
            for serial, index in serials_and_index
        ]
    }


def _tags(table: str, parent_column: str, parent: int, tags) -> RowSet:
    return {table: [{parent_column: parent, "tag_serial": t} for t in tags]}


def _merge(*row_sets: RowSet) -> RowSet:
    out: RowSet = {}
    for rows in row_sets:
        out = with_rows(out, rows)
    return out


def _members(sample: int, tesserae) -> RowSet:
    return {
        "Sample_members": [
            {"sample_serial": sample, "tessera_serial": t} for t in tesserae
        ]
    }


# the Weave's strands: Weave_members serial -> (anchor Tessera serial or None, origin Trace serial
# or None), each naming rows of the Weave's own shard
_WEAVE_STRANDS: Dict[int, Tuple[Optional[int], Optional[int]]] = {
    701: (1, None),
    702: (None, 3),
}


def _weave_members(weave: int) -> RowSet:
    return {
        "Weave_members": [
            {
                "serial": serial,
                "weave_serial": weave,
                "anchor_serial": anchor,
                "origin_serial": origin,
            }
            for serial, (anchor, origin) in _WEAVE_STRANDS.items()
        ]
    }


def _full_shard0() -> RowSet:
    return _merge(
        SHARDED_ROWS[0],
        {
            "Tessera": [
                {"serial": 1, "version": 1, "alias_serial": 1, "tessera_weight": 0.5},
                {"serial": 2, "version": 1, "alias_serial": 1, "tessera_weight": 0.75},
                {"serial": 3, "version": 1, "alias_serial": 4, "tessera_weight": 0.5},
            ]
        },
        # two validated Samples, each anchored on a Tessera of shard 1
        {
            "Sample": [
                {
                    "serial": 1,
                    "version": 1,
                    "keypoint_serial": 1,
                    "gadget_serial": 1,
                    "anchor_serial": 4,
                    "sample_code": "fixture-sample-1",
                    "member_count": 2,
                    "sample_validated": True,
                },
                {
                    "serial": 2,
                    "version": 1,
                    "keypoint_serial": 1,
                    "gadget_serial": 1,
                    "anchor_serial": 5,
                    "sample_code": "fixture-sample-2",
                    "member_count": 1,
                    "sample_validated": True,
                },
            ]
        },
        _members(1, (1, 2)),
        _members(2, (2,)),
        _tags("Sample_tags", "sample_serial", 1, (1, 2)),
        _tags("Sample_tags", "sample_serial", 2, (1,)),
        # an unvalidated Trace on the knob frame, with fewer steps; the Weave's strand names it
        {
            "Trace": [
                {
                    "serial": 3,
                    "version": 1,
                    "keypoint_serial": 1,
                    "frame_kind": _KNOB_KIND,
                    "frame_serial": 1,
                    "trace_label": "fixture-trace-3",
                    "step_count": 2,
                    "trace_validated": False,
                },
                # the Weave's own Trace
                {
                    "serial": 4,
                    "version": 1,
                    "keypoint_serial": 1,
                    "frame_kind": _DIAL_KIND,
                    "frame_serial": 2,
                    "trace_label": "fixture-trace-4",
                    "step_count": 1,
                    "trace_validated": True,
                },
            ]
        },
        _tags("Trace_tags", "trace_serial", 3, (1, 4)),
        _tags("Trace_tags", "trace_serial", 4, (1,)),
        _values("TraceStep", "trace_serial", 3, ((31, 1), (32, 2))),
        _values("TraceStep", "trace_serial", 4, ((41, 1),)),
        # Weave 1 shares its serial with Trace 1, and carries different tags, so reading its tags
        # from the wrong association table is visible
        {
            "Weave": [
                {
                    "serial": 1,
                    "version": 1,
                    "keypoint_serial": 1,
                    "trace_serial": 4,
                    "anchor_serial": None,
                    "weave_label": "fixture-weave-1",
                }
            ]
        },
        _weave_members(1),
        _tags("Weave_tags", "weave_serial", 1, (1, 5)),
    )


def _full_shard1() -> RowSet:
    return _merge(
        SHARDED_ROWS[1],
        {
            "Tessera": [
                {"serial": 4, "version": 1, "alias_serial": 2, "tessera_weight": 0.5},
                {"serial": 5, "version": 1, "alias_serial": 3, "tessera_weight": 0.75},
            ]
        },
        # an unvalidated Sample, on the unvalidated Gadget, anchored on a Tessera of shard 0
        {
            "Sample": [
                {
                    "serial": 4,
                    "version": 1,
                    "keypoint_serial": 2,
                    "gadget_serial": 2,
                    "anchor_serial": 1,
                    "sample_code": "fixture-sample-4",
                    "member_count": 1,
                    "sample_validated": False,
                }
            ]
        },
        _members(4, (4,)),
        _tags("Sample_tags", "sample_serial", 4, (1,)),
    )


# shard serial -> sharded rows. Keypoint 1 (aliases 1 and 4) is on shard 0; keypoints 2 and 3
# (aliases 2 and 3) are on shard 1
FULL_SHARDED_ROWS: Dict[int, RowSet] = {0: _full_shard0(), 1: _full_shard1()}

FULL_SHARD_KEYS: Dict[int, int] = {1: 0, 2: 1, 3: 1}


_SCHEMA: Dict[str, Mapping[str, sqla.Table]] = {}


def _schema_tables() -> Mapping[str, sqla.Table]:
    """The ``build_schema`` tables, built once per process. Read, never created from."""
    if "tables" not in _SCHEMA:
        _SCHEMA["tables"] = build_schema(sqla.MetaData(), _factories).tables
    return _SCHEMA["tables"]


def _placeholder(column: sqla.Column):
    kind = column.type
    if isinstance(kind, sqla.Boolean):
        return False
    if isinstance(kind, sqla.Integer):
        return 0
    if isinstance(kind, sqla.Float):
        return 0.5
    if isinstance(kind, sqla.String):
        return "fixture"
    if isinstance(kind, sqla.DateTime):
        return FIXED_TIMESTAMP
    raise TypeError(f"no placeholder for column {column!r}")


def fill_required(rows: RowSet) -> RowSet:
    """A copy of ``rows`` in which every non-nullable, non-key column a row leaves out holds a
    placeholder of its type, and a nullable column that another row of the same table states is
    ``None`` (one insert takes one set of columns). Columns a row states are never changed.
    """
    tables = _schema_tables()
    out = copy.deepcopy(rows)
    for name, table_rows in out.items():
        table = tables[name]
        stated = {c for row in table_rows for c in row}
        for row in table_rows:
            for column in table.columns:
                if column.name in row or column.primary_key:
                    continue
                if not column.nullable:
                    row[column.name] = _placeholder(column)
                elif column.name in stated and column.name != "timestamp":
                    row[column.name] = None
    return out


def full_rows() -> Tuple[RowSet, Dict[int, RowSet], Dict[int, int]]:
    """Fresh copies of the full store's replicated rows, sharded rows and shard keys."""
    return (
        copy.deepcopy(FULL_REPLICATED_ROWS),
        copy.deepcopy(FULL_SHARDED_ROWS),
        dict(FULL_SHARD_KEYS),
    )


_EMPTY_SHARD: Dict[str, bytes] = {}


def _empty_shard_bytes() -> bytes:
    """An empty shard file holding every ``build_schema`` table, made once per process. Creating
    the tables commits once per statement, so a copy of this is much faster than ``create_all``.
    """
    if "bytes" not in _EMPTY_SHARD:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.sqlite"
            metadata = sqla.MetaData()
            build_schema(metadata, _factories)
            engine = sqla.create_engine(f"sqlite:///{path}", future=True)
            try:
                metadata.create_all(engine)
            finally:
                engine.dispose()
            _EMPTY_SHARD["bytes"] = path.read_bytes()
    return _EMPTY_SHARD["bytes"]


def _write_full_shard(
    path: Path,
    rows: List[RowSet],
    missing_tables: Iterable[str],
    missing_columns: Mapping[str, Iterable[str]],
    extra_sql: Iterable[str],
) -> None:
    """As ``_write_shard``, from a copy of the empty shard. Rows for a missing table are skipped
    (replicated rows are written to every shard), and the table is then dropped."""
    missing_tables = set(missing_tables)
    path.write_bytes(_empty_shard_bytes())
    tables = _schema_tables()
    engine = sqla.create_engine(f"sqlite:///{path}", future=True)
    try:
        with engine.begin() as conn:
            for row_set in rows:
                _insert_rows(
                    conn,
                    tables,
                    {t: r for t, r in row_set.items() if t not in missing_tables},
                )
    finally:
        engine.dispose()

    statements = (
        [f'DROP TABLE "{table}"' for table in sorted(missing_tables)]
        + [
            f'ALTER TABLE "{table}" DROP COLUMN "{column}"'
            for table, columns in missing_columns.items()
            for column in columns
        ]
        + list(extra_sql)
    )
    if len(statements) > 0:
        conn = sqlite3.connect(path)
        try:
            with conn:
                for statement in statements:
                    conn.execute(statement)
        finally:
            conn.close()


def build_full_store(
    directory: Path,
    stem: str = "full-store",
    shards: int = 2,
    replicated: Optional[RowSet] = None,
    sharded: Optional[Dict[int, RowSet]] = None,
    shard_keys: Optional[Mapping[int, int]] = None,
    missing_tables: Optional[Mapping[int, Iterable[str]]] = None,
    missing_columns: Optional[Mapping[int, Mapping[str, Iterable[str]]]] = None,
    extra_sql: Optional[Mapping[int, Iterable[str]]] = None,
) -> RealStore:
    """
    A store like ``build_real_store``'s, with the full store's rows (or the ones given), through
    ``fill_required``. Its primary is written the same way. Its shards are copies of one empty
    shard, filled with the rows; a table in ``missing_tables[n]`` is dropped from shard ``n``
    after the rows are written, and its rows are skipped there.
    """
    base_replicated, base_sharded, base_keys = full_rows()
    replicated = fill_required(base_replicated if replicated is None else replicated)
    sharded = {
        n: fill_required(rows)
        for n, rows in (base_sharded if sharded is None else sharded).items()
    }
    shard_keys = dict(base_keys if shard_keys is None else shard_keys)
    missing_tables = {} if missing_tables is None else missing_tables
    missing_columns = {} if missing_columns is None else missing_columns
    extra_sql = {} if extra_sql is None else extra_sql

    if shards < 2:
        raise ValueError("a real store fixture has at least two shards")
    unknown = set(sharded) - set(range(shards))
    if unknown:
        raise ValueError(
            f"sharded rows name shards {sorted(unknown)} that do not exist"
        )

    primary = (Path(directory) / f"{stem}.sqlite").resolve()
    shard_files = {
        serial: primary.parent / shard_file_name(primary, serial)
        for serial in range(shards)
    }
    for serial, path in shard_files.items():
        _write_full_shard(
            path,
            [replicated, sharded.get(serial, {})],
            missing_tables.get(serial, ()),
            missing_columns.get(serial, {}),
            extra_sql.get(serial, ()),
        )
    _write_primary(primary, shard_files, shard_keys)

    return RealStore(
        primary=primary, shard_files=shard_files, replicated=replicated, sharded=sharded
    )


# a polymorphic reference is resolved through its type column, per row: references() names its
# target by this word, and _polymorphic() holds its type column and type map
_FRAME = "frame"


def _polymorphic() -> Dict[str, Dict[str, Tuple[str, Mapping[object, str]]]]:
    """table -> column -> (type column, type value -> table), for every polymorphic parent the
    factories' ``inventory_spec`` declare."""
    out: Dict[str, Dict[str, Tuple[str, Mapping[object, str]]]] = {}
    for name, spec in inventory_specs(_factories).items():
        for parent in spec.parents.values():
            if parent.types is not None:
                out.setdefault(name, {})[parent.column] = (
                    parent.type_column,
                    parent.types,
                )
    return out


def references() -> Dict[str, Dict[str, str]]:
    """table -> column -> the table whose serial it holds: the schema's foreign keys, and every
    parent and parent-set member the factories' ``inventory_spec`` declare. A polymorphic parent's
    column maps to ``"frame"``, and is resolved through its type column.
    """
    out: Dict[str, Dict[str, str]] = {}
    for name, table in _schema_tables().items():
        refs = {}
        for column in table.columns:
            for fk in column.foreign_keys:
                refs[column.name] = fk.column.table.name
        out[name] = refs
    for name, spec in inventory_specs(_factories).items():
        for parent in spec.parents.values():
            out[name][parent.column] = _FRAME if parent.types is not None else parent.of
        for parent_set in spec.parent_sets.values():
            for member in parent_set.members.values():
                out[parent_set.table][member.column] = member.of
    return out


def relabel_serials(
    replicated: RowSet,
    sharded: Dict[int, RowSet],
    shard_keys: Mapping[int, int],
    offset: int = 100,
) -> Tuple[RowSet, Dict[int, RowSet], Dict[int, int]]:
    """
    The same content under different serials. In every table the serials are reversed in order
    and moved by a per-table offset, and every reference follows them. Replicated rows get the
    same new serials on every shard, as ``ShardedPool`` replicates them.
    """
    replicated = copy.deepcopy(replicated)
    sharded = copy.deepcopy(sharded)
    row_sets = [replicated] + [sharded[n] for n in sorted(sharded)]

    olds: Dict[str, List[int]] = {}
    for rows in row_sets:
        for table, table_rows in rows.items():
            for row in table_rows:
                if "serial" in row:
                    olds.setdefault(table, []).append(row["serial"])

    mapping: Dict[str, Dict[int, int]] = {}
    for index, table in enumerate(sorted(olds)):
        serials = sorted(set(olds[table]))
        base = offset * (index + 1)
        mapping[table] = {
            old: base + len(serials) - position for position, old in enumerate(serials)
        }

    refs = references()
    polymorphic = _polymorphic()
    for rows in row_sets:
        for table, table_rows in rows.items():
            for row in table_rows:
                if "serial" in row:
                    row["serial"] = mapping[table][row["serial"]]
                for column, target in refs.get(table, {}).items():
                    if column not in row:
                        continue
                    if target == _FRAME:
                        type_column, types = polymorphic[table][column]
                        target = types[row[type_column]]
                    row[column] = mapping.get(target, {}).get(row[column], row[column])

    new_keys = {
        mapping["keypoint"].get(key, key): shard for key, shard in shard_keys.items()
    }
    return replicated, sharded, new_keys


def find_row(
    replicated: RowSet, sharded: Dict[int, RowSet], table: str, serial: int
) -> Dict[str, object]:
    """The one row of ``table`` with ``serial``, wherever it is."""
    found = [
        row
        for rows in [replicated] + list(sharded.values())
        for row in rows.get(table, [])
        if row.get("serial") == serial
    ]
    if len(found) != 1:
        raise KeyError(f"{len(found)} rows of {table} have serial {serial}")
    return found[0]


def vary_row(
    replicated: RowSet,
    sharded: Dict[int, RowSet],
    table: str,
    serial: int,
    column: str,
    value: object,
) -> None:
    """Set ``column`` of the row of ``table`` with ``serial`` to ``value``, in place."""
    find_row(replicated, sharded, table, serial)[column] = value
