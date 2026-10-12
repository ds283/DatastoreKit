from datetime import datetime
from typing import Optional


class DatastoreObject:
    """
    Represent an object that can be serialized in a datastore
    """

    def __init__(
        self, store_id: Optional[int], *, timestamp: Optional[datetime] = None
    ):
        self._my_id = store_id
        self._timestamp = timestamp

    @property
    def store_id(self) -> int:
        if self._my_id is None:
            raise RuntimeError("Attempt to read datastore id before it has been set")

        return self._my_id

    @property
    def available(self) -> bool:
        return self._my_id is not None

    @property
    def timestamp(self) -> Optional[datetime]:
        """
        The row's ``timestamp``, as the factory that built this object passed it, or ``None``.

        The layer stamps a row's ``timestamp`` column at insert, for a class whose ``register()``
        declares ``"timestamp": True``. A factory that reads such a row may pass the value to the
        object it builds, by the keyword ``timestamp``. It is ``None`` for an object not yet
        stored, for one built from an insert, for one whose factory does not pass it, and for one
        whose table has no such column. The layer neither sets nor reads it. It is read-only.
        """
        return self._timestamp
