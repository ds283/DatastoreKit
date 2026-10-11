from abc import ABC, abstractmethod
from typing import List, Optional


class SQLAFactoryBase(ABC):
    @staticmethod
    @abstractmethod
    def register():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def build(payload, conn, table, inserter, tables, inserters):
        raise NotImplementedError

    # Hooks the datastore layer calls. They are not abstract, so a factory that has no use for one
    # need not define it. The layer calls each on the registry's entry, a class or an instance
    # alike, only in the case its docstring names; a hook the factory does not define then raises
    # NotImplementedError, or returns its default, as below.

    @staticmethod
    def store(obj, conn, table, inserter, tables, inserters):
        """
        Store ``obj``, an object of this factory's class, through ``inserter``, and return the
        object as stored. The layer calls it, in an actor, for every store of an object of the
        class. A replicated store calls it on the controlling shard, and then on every other shard
        with the controlling shard's answer, which carries the serials it must insert under or
        verify.
        """
        raise NotImplementedError

    @staticmethod
    def validate(obj, conn, table, tables):
        """
        Validate ``obj``, an object of this factory's class, and return the outcome. The layer
        calls it, in an actor, for every validate of an object of the class. A replicated validate
        calls it on the controlling shard, and, when that outcome is true, on every other shard,
        whose outcome must equal it.
        """
        raise NotImplementedError

    @staticmethod
    def validate_on_startup(conn, table, tables, prune=False):
        """
        Return lines describing the stored rows that are not validated, and, with ``prune``,
        delete them. The layer calls it only for a class whose ``register()`` declares
        ``validate_on_startup: True``: in each actor when a store is opened, and in the pool's
        prune of such a class when it is replicated.
        """
        raise NotImplementedError

    @staticmethod
    def revalidate(serial, conn, table, tables) -> bool:
        """
        Recompute the validated flag of the stored row ``serial`` from stored rows alone, write
        it, and return it, by the same rule as ``validate`` applies to an object. A factory whose
        ``register()`` declares ``validated_column`` implements it: the check at open calls it,
        on each shard, after an interrupted validate.
        """
        raise NotImplementedError

    @staticmethod
    def owned_serials(obj) -> Optional[List[Optional[int]]]:
        """
        The serials of the rows ``obj`` owns in another table, in order, or ``None`` if it owns
        none. A replicated store's controlling shard assigns them, and every replica must answer
        with the same; the pool compares the two after a replicated store.
        """
        return None

    @staticmethod
    def inventory_spec():
        """
        How the inventory reads this factory's class: an ``InventorySpec``
        (``datastorekit/store_inventory.py``) naming the key's leaf columns, its parent references
        and its association and value tables, or ``None`` where the class is not a class of the
        inventory. It holds no connection and reads nothing; the inventory derives which classes it
        reads, and in what order, from these declarations.
        """
        return None
