"""
Factory instances for the neutral client (added by ``factory-defaults`` prompt 01).

The neutral client's registry (``registry``) maps every name to a factory class. A client may map a
name to an instance of a factory class instead, and the layer calls each hook on the registry's
entry, class or instance alike (``docs/client-contract.md`` §9.5). This module holds what the
tests of instances (``tests/test_factory_instances.py``) and step I of
``docs/extraction/ray_smoke_run.py`` need, apart from the registry, so that the registry, and
every count its tests pin, is unchanged:

- ``scalar_entry``: a replicated stored class with one integer value;
- ``scalar_entry_factory``: a parameterised factory. Its constructor takes the name of the value's
  column, and its ``__init__``, ``register`` and ``build`` take ``self`` and are all it defines: it
  has no ``store``, ``validate``, ``validate_on_startup`` or ``inventory_spec``, so the base's
  defaults answer for them. One class serves two tables, each through an instance of its own;
- ``instance_registry()``: a copy of the registry's factories, with ``gauge_setting`` registered as
  an instance of its factory class and an instance of ``scalar_entry_factory`` under each name of
  ``SCALAR_TABLES``, and a copy of the replicated tables with those names added.

Both classes are defined at module level, so that a Ray worker unpickles an instance by reference
to its class, with its attributes by value. **No instance is made at import**, only inside
``instance_registry()``: under a base that refuses to instantiate such a class, importing this
module still works, and each caller fails where it makes an instance.

Importing this module imports the factories, ``sqlalchemy`` and ``datastorekit``; it starts
nothing.
"""

from typing import Dict, List, Optional, Tuple

import sqlalchemy as sqla

from datastorekit.SQL.factory_base import SQLAFactoryBase
from datastorekit.object import DatastoreObject
from datastorekit.tests.client import factories as _f
from datastorekit.tests.client import registry as _registry

# the two tables an instance of scalar_entry_factory serves: the registry name -> the value's column
SCALAR_TABLES = {"scalar_left": "left_value", "scalar_right": "right_value"}

# the value got in each table by the tests and the smoke step: each is got in one table only
SCALAR_VALUES = {"scalar_left": 7, "scalar_right": 11}


class scalar_entry(DatastoreObject):
    """A replicated stored class with one integer value, served by ``scalar_entry_factory``."""

    def __init__(self, store_id: Optional[int], value: int):
        super().__init__(store_id)
        self.value = value


class scalar_entry_factory(SQLAFactoryBase):
    """
    A factory of ``scalar_entry`` whose constructor names the value's column. Its hooks take
    ``self``, so it is registered as an instance; it defines only ``register`` and ``build``.
    """

    def __init__(self, column: str):
        self.column = column

    def register(self):
        return {
            "version": False,
            "timestamp": True,
            "columns": [sqla.Column(self.column, sqla.Integer, nullable=False)],
        }

    def build(self, payload, conn, table, inserter, tables, inserters):
        value = payload["value"]
        store_id = conn.execute(
            sqla.select(table.c.serial).filter(table.c[self.column] == value)
        ).scalar_one_or_none()
        obj = scalar_entry(store_id, value)
        if store_id is None:
            data = {self.column: value}
            if "serial" in payload:
                data["serial"] = payload["serial"]
            obj = scalar_entry(inserter(conn, data), value)
            obj._new_insert = True
        else:
            obj._deserialized = True
        return obj


def instance_registry() -> Tuple[Dict[str, object], List[str]]:
    """
    ``(factories, replicated_tables)``: a copy of the registry's factories, with
    ``gauge_setting`` mapped to ``gauge_setting_factory()`` and each name of ``SCALAR_TABLES``
    to ``scalar_entry_factory(column)``, and a copy of the registry's replicated tables with the
    names of ``SCALAR_TABLES`` added at the end. The instances are made here, on each call.
    """
    factories = dict(_registry.factories)
    factories["gauge_setting"] = _f.gauge_setting_factory()
    for name, column in SCALAR_TABLES.items():
        factories[name] = scalar_entry_factory(column)
    replicated_tables = list(_registry.replicated_tables) + list(SCALAR_TABLES)
    return factories, replicated_tables
