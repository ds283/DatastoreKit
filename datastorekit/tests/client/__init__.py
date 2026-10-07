"""
The neutral test client: a small registry of storable classes, with abstract names, that supplies
every fact ``docs/client-contract.md`` says a client of ``datastorekit`` supplies, at least once.

It is a fixture of the test suite, not a model of anything. Its tests open it on the stand-in pool
(``datastorekit.tests.standin_pool``), with no Ray, in temporary directories only.

- ``objects``: the stored classes, each a ``DatastoreObject`` named as its table;
- ``factories``: one factory per class, the hooks the layer calls;
- ``registry``: the nine names a pool, the reader and the tests are given (``factories``,
  ``replicated_tables``, ``sharded_tables``, ``shard_key_type``, ``shard_key_store_id``,
  ``read_table_config``, ``serial_batch_sizes``, ``drop_groups`` and ``tables_to_drop``);
- ``build``: helpers that get or store each class through a pool, and ``build_store``, which writes
  a store with every class populated.

The roles each class carries are listed in ``registry``'s docstring.
"""
