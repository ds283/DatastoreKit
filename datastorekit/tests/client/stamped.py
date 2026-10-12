"""
A stored class whose factory passes the row's timestamp (added by ``object-timestamp`` prompt 01).

``DatastoreObject`` takes a keyword-only ``timestamp`` and exposes it read-only; the layer never
sets it and never reads it (``docs/client-contract.md`` §9.6). A factory that reads a row of a
class registered with ``"timestamp": True`` may pass the row's ``timestamp``. The neutral client's
registry has no such factory, and is not changed to have one, so that the objects every other
module gets, and every count the registry's tests pin, are unchanged. This module holds what the
tests of the timestamp (``tests/test_object_timestamp.py``) need, apart from the registry:

- ``stamped_tally``: a replicated stored class with one integer, ``tally``, whose constructor
  passes ``timestamp`` to ``DatastoreObject`` by keyword;
- ``stamped_tally_factory``: its factory, registered as a class, whose hooks are static and are
  ``register`` and ``build`` only. ``register`` declares ``"version": False``,
  ``"timestamp": True`` and the integer's column. ``build`` reads the row's ``serial`` and
  ``timestamp`` by the integer: if it finds the row, it returns the object with the row's
  ``timestamp``, marked ``_deserialized``; if not, it inserts (under a payload's ``serial``, if one
  is given) and returns the object with no timestamp, marked ``_new_insert``, since the actor adds
  the stamp inside the inserter and the factory does not know it;
- ``stamped_registry()``: a copy of the registry's factories with ``stamped_tally_factory`` added
  under ``STAMPED_TABLE``, and a copy of the replicated tables with that name added at the end.

Both classes are defined at module level, so that they pickle by reference, as Ray would need.
``stamped_tally_factory`` defines no ``inventory_spec``. Importing this module imports the
registry, ``sqlalchemy`` and ``datastorekit``; it starts nothing.
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple

import sqlalchemy as sqla

from datastorekit.SQL.factory_base import SQLAFactoryBase
from datastorekit.object import DatastoreObject
from datastorekit.tests.client import registry as _registry

# the registry name of the stamped class, which is also its class's name and its table's
STAMPED_TABLE = "stamped_tally"

# the column that holds the integer
STAMPED_COLUMN = "tally"


class stamped_tally(DatastoreObject):
    """A replicated stored class with one integer, served by ``stamped_tally_factory``."""

    def __init__(
        self,
        store_id: Optional[int],
        tally: int,
        timestamp: Optional[datetime] = None,
    ):
        super().__init__(store_id, timestamp=timestamp)
        self.tally = tally


class stamped_tally_factory(SQLAFactoryBase):
    """
    The factory of ``stamped_tally``: static ``register`` and ``build`` only. A row it finds is
    returned with the row's ``timestamp``; a row it inserts, with none.
    """

    @staticmethod
    def register():
        return {
            "version": False,
            "timestamp": True,
            "columns": [sqla.Column(STAMPED_COLUMN, sqla.Integer, nullable=False)],
        }

    @staticmethod
    def build(payload, conn, table, inserter, tables, inserters):
        tally = payload[STAMPED_COLUMN]
        row = conn.execute(
            sqla.select(table.c.serial, table.c.timestamp).filter(
                table.c[STAMPED_COLUMN] == tally
            )
        ).one_or_none()
        if row is not None:
            obj = stamped_tally(row.serial, tally, timestamp=row.timestamp)
            obj._deserialized = True
            return obj

        data = {STAMPED_COLUMN: tally}
        if "serial" in payload:
            data["serial"] = payload["serial"]
        obj = stamped_tally(inserter(conn, data), tally)
        obj._new_insert = True
        return obj


def stamped_registry() -> Tuple[Dict[str, object], List[str]]:
    """
    ``(factories, replicated_tables)``: a copy of the registry's factories with
    ``stamped_tally_factory`` added under ``STAMPED_TABLE``, and a copy of the registry's
    replicated tables with ``STAMPED_TABLE`` added at the end.
    """
    factories = dict(_registry.factories)
    factories[STAMPED_TABLE] = stamped_tally_factory
    replicated_tables = list(_registry.replicated_tables) + [STAMPED_TABLE]
    return factories, replicated_tables
