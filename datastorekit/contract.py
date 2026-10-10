"""
The tables and columns the datastore layer owns as its contract. Each is named once, here.

**Why these are the layer's, not the project's.** Every storable row carries a foreign key to the
version table's ``serial``, which ``datastorekit/SQL/schema.py`` prepends; a pool is opened under a
version label, finds or writes its row before any actor may insert, and gives every actor its
serial. Every tagged class associates its rows with the tag table, through an association table
whose column names a tag's serial, and the check at open and the inventory recognise those
association tables by it. A project cannot choose other names for these without the layer changing,
so they are not declared per project: the layer names them, and a client registers a factory under
each name. The layer builds the objects of these tables through those factories, never by importing
a client's classes.

**Why the version-keyed lookup's payload key is the layer's.** A factory that declares
``key_on_version`` in its ``register()`` is handed, in every payload ``Datastore.object_get``
gives its ``build``, the serial of the version row the pool was opened under, so that its lookup
finds only rows made under that label. The actor sets that key, and refuses a payload that already
holds it, so its name cannot be a client's choice: it is ``VERSION_SERIAL_KEY``, named here, and a
factory reads it through ``require_version_serial``.

This module imports nothing outside the standard library, so that any module of the layer can
import it at module scope.
"""

# the version table: its name, and the column holding the label a pool is opened under
VERSION_TABLE = "version"
VERSION_LABEL = "label"

# the tag table: its name, the column holding a tag's label, and the column of an association
# table that names a tag's serial
TAG_TABLE = "store_tag"
TAG_LABEL = "label"
TAG_SERIAL = "tag_serial"

# the version-keyed lookup (key_on_version): the reserved payload key under which
# Datastore.object_get hands a keyed factory's build the serial of the pool's version label;
# require_version_serial, below, is the one way such a build reads it
VERSION_SERIAL_KEY = "_version_serial"


def require_version_serial(payload, cls_name: str) -> int:
    """
    The version serial that ``Datastore.object_get`` placed in a lookup payload of a class whose
    factory declares ``key_on_version``, under ``VERSION_SERIAL_KEY``. Raises ``RuntimeError``,
    naming ``cls_name`` and the key, if the key is absent or ``None``: a keyed lookup goes through
    ``object_get``, and is never made unfiltered.
    """
    serial = payload.get(VERSION_SERIAL_KEY, None)
    if serial is None:
        raise RuntimeError(
            f'{cls_name}: the lookup payload carries no version serial under "{VERSION_SERIAL_KEY}". '
            "A version-keyed lookup goes through Datastore.object_get, which sets it, and is "
            "never made unfiltered"
        )
    return serial
