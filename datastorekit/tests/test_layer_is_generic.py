"""
The package's guard: the layer names nothing of any client, and imports nothing but the standard
library, ``ray``, ``sqlalchemy`` and itself (extraction prompt 04b; README §6.2, U17). Ported from
SecondaryGWKit's guard of its own layer (its ``test_layer_is_generic``, at the import commit).

**What the layer is.** Every module under ``datastorekit/`` but its tests, the factory contract
``datastorekit/SQL/factory_base.py`` among them. A client's factories are not in the layer: the
neutral test client's are under ``datastorekit/tests/``. ``layer_files()`` derives the set from the
filesystem, not from ``git ls-files`` and not from a list, so that a module added to the layer is
checked before anyone commits it or adds it here. ``test_the_derived_files_hold_the_audits_list``
pins that the derived set still holds the source's audited list, so that a derivation that came out
empty or narrow cannot pass.

**What it forbids.** The vocabulary of the three clients (SecondaryGWKit, ChamPBH and
StochasticInstantons): their registries' tables, their identifier columns, their packages, and the
names SecondaryGWKit's own inventory once used, less ``LAYER_WORDS`` (the layer's own words, each
with its reason). In strings and comments it also forbids the two monotone flags' phrases and the
naming conventions SecondaryGWKit's guard forbade. For each file, by ``ast`` and ``tokenize``:

1. ``test_no_code_name``: names, attributes, definitions, arguments, keywords and imported names;
2. ``test_no_string_or_docstring``: every string constant, docstrings and f-string text included;
3. ``test_no_comment``: every comment.

**The vocabulary is data.** It was measured from the three clients, read-only through ``git show``
at fixed commits, by ``docs/extraction/measure_client_vocabulary.py``, and is held in
``datastorekit/tests/data/client_vocabulary.json`` (``VOCABULARY``). This module reads that file,
never a client and never a registry, so it runs with no client present. Which of the measured words
are forbidden is this module's rule (``registry_words``, ``project_packages``). A re-measure writes
a new file, and ``VOCABULARY`` is pointed at it.

**The known hits.** ``KNOWN_HITS`` lists, by the scan that finds it, each hit the layer is known to
hold, with its reason. Each scan must find exactly its known hits: a new hit fails, and so does a
known hit that is no longer found. The list has been empty since extraction prompt 09 rewrote the
layer's prose (``[01-package-prose-names-sgks-layout]``), so any hit fails, by name.

**What it allows.** ``test_every_import_is_allowed``: the standard library, ``ray`` and
``sqlalchemy``, and the package's own modules, except its tests (the neutral client among them).
``test_the_allow_list`` pins that list without a mutation. No other entry exists: an English word
that collides with a name is reworded in the layer, not allowed here.

What a module *loads* when it runs is not checked here; the fresh-interpreter tests of
``test_inventory_declarations`` and ``test_layer_registry`` do that, on the neutral client, and
``test_package_imports`` checks the whole package's imports.

Each failure names ``file:line word``, for every file at once. No store is opened, and no Ray
starts.
"""

import ast
import io
import json
import re
import sys
import tokenize
import unittest
from pathlib import Path

from datastorekit import contract

REPO_ROOT = Path(__file__).resolve().parents[2]

# the layer's one module of the factory contract; a client's factories are not in the layer
_FACTORY_CONTRACT = "datastorekit/SQL/factory_base.py"

# the three clients' vocabulary, measured read-only (docs/extraction/measure_client_vocabulary.py)
VOCABULARY = Path(__file__).resolve().parent / "data" / "client_vocabulary.json"


def layer_files() -> list:
    """The layer's modules, relative to the top of this repository, sorted."""
    found = set()
    for path in (REPO_ROOT / "datastorekit").rglob("*.py"):
        rel = path.relative_to(REPO_ROOT)
        if rel.parts[:2] == ("datastorekit", "tests"):
            continue
        found.add(rel.as_posix())
    return sorted(found)


# the source's audited list, by the package's module map; its RayWorkPool is not in the package
# (README §6.1, D2)
AUDIT_LIST = {
    "datastorekit/SQL/ShardedPool.py",
    "datastorekit/SQL/Datastore.py",
    "datastorekit/SQL/ClientPool.py",
    "datastorekit/store_inventory.py",
    "datastorekit/store_reader.py",
    "datastorekit/SQL/schema.py",
    "datastorekit/SQL/SerialPoolBroker.py",
    "datastorekit/SQL/ProfileAgent.py",
    "datastorekit/object.py",
    "datastorekit/replication.py",
    "datastorekit/shard_paths.py",
    "datastorekit/contract.py",
}

# ------------------------------------------------------------------------------------------------
# the vocabulary the layer may not use
# ------------------------------------------------------------------------------------------------

# the layer's own words, each of which is also a table or a column of a client's registry, and so
# would be flagged; each is allowed for a stated reason
LAYER_WORDS = {
    # the version and tag tables and their columns: the layer's contract, named once in
    # datastorekit.contract
    contract.VERSION_TABLE,
    contract.VERSION_LABEL,
    contract.TAG_TABLE,
    contract.TAG_LABEL,
    contract.TAG_SERIAL,
    # the column every table has, and the version column that schema.py prepends to every table
    "serial",
    "version",
    # the column the check at open compares, which every replicated write stamps
    "timestamp",
    # the replication action record's own key
    "stepping",
    # the record's own field and ``read_records``' keyword, and the flag the check at open
    # recomputes: the layer defines it, it does not assume a column of that name
    "validated",
}

# packages that are part of the layer, and ``config``, which "config" is an English word. ``tools``
# is a client's package and also the layer's own subpackage, ``datastorekit.tools``, whose module
# paths the layer's strings name ("python -m datastorekit.tools.…")
_NOT_PROJECT_PACKAGES = {"Datastore", "RayTools", "config", "tools"}

# the naming conventions SecondaryGWKit's guard forbade: a tag table, a value table, a run label
FRAGMENTS = ("_tags", "*Value", "Run_<")

# the two monotone flags SecondaryGWKit declares, which are plain words and so not in the column
# list
FLAG_PHRASES = re.compile(
    r"\b(source|response)\s+(or|and)\s+(source|response)\b|\b(source|response)\s+flags?\b"
)

_WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _clients() -> dict:
    """The measured vocabulary, per client, read from ``VOCABULARY``."""
    return json.loads(VOCABULARY.read_text())["clients"]


def project_packages() -> set:
    """The clients' top-level packages, less the ones that are not a project's."""
    return {
        name
        for client in _clients().values()
        for name in client["packages"]
        if name not in _NOT_PROJECT_PACKAGES
    }


def registry_words() -> tuple:
    """(tables, identifier columns) of the three clients' registries, less the layer's own.

    A column is an identifier if it has an underscore, or a capital and more than one character:
    ``model_serial``, ``k_inv_Mpc``. A plain-word column, such as ``source`` or ``value``, cannot
    be told from English; ``FLAG_PHRASES`` checks the two declared flags instead. Neither can a
    one-letter column: the clients have ``C``, ``G``, ``N`` and ``T``, and the layer's prose says
    "shard #N" and "*N* shard files"."""
    clients = _clients()
    tables = {
        name for client in clients.values() for name in client["registry"]["keys"]
    } - LAYER_WORDS
    columns = {
        name
        for client in clients.values()
        for name in client["columns"]["names"]
        if "_" in name or (name.lower() != name and len(name) > 1)
    } - LAYER_WORDS
    return tables, columns


def extra_names() -> set:
    """The names SecondaryGWKit once removed from its inventory, which are not tables or identifier
    columns: its guard's ``EXTRA_NAMES``, held under it in ``VOCABULARY``."""
    return set(_clients()["SGK"]["extra_names"]["names"])


def forbidden_words() -> set:
    tables, columns = registry_words()
    return tables | columns | project_packages() | extra_names()


# ------------------------------------------------------------------------------------------------
# the hits the layer is known to hold: none, since extraction prompt 09
# ------------------------------------------------------------------------------------------------

# each scanning test's expected hits, exactly, each with its reason; every list is empty, so any
# hit fails, by name
KNOWN_HITS = {
    "test_no_code_name": [],
    "test_no_string_or_docstring": [],
    "test_no_comment": [],
    "test_every_import_is_allowed": [],
}

# ------------------------------------------------------------------------------------------------
# the imports the layer may make
# ------------------------------------------------------------------------------------------------

# the standard library, and the two third-party packages the layer is built on
_ALLOWED_ROOTS = set(sys.stdlib_module_names) | {"ray", "sqlalchemy"}

# empty: the source allowed two client modules, and extraction prompt 01 internalised both
# (datastorekit.defaults and datastorekit._timing), which are the package's own
_ALLOWED_MODULES = set()


def import_allowed(module: str) -> bool:
    root = module.split(".")[0]
    if root in _ALLOWED_ROOTS or module in _ALLOWED_MODULES:
        return True
    if root == "datastorekit":
        # the layer's own modules, and nothing of the package's tests or its test client
        return not (
            module == "datastorekit.tests" or module.startswith("datastorekit.tests.")
        )
    return False


# ------------------------------------------------------------------------------------------------
# the scans
# ------------------------------------------------------------------------------------------------


def _text_hits(text: str, forbidden: set) -> list:
    """(line offset in ``text``, word) of every forbidden word, flag phrase and fragment."""
    hits = [
        (m.start(), m.group(0)) for m in _WORD.finditer(text) if m.group(0) in forbidden
    ]
    hits += [(m.start(), repr(m.group(0))) for m in FLAG_PHRASES.finditer(text)]
    hits += [
        (m.start(), repr(f)) for f in FRAGMENTS for m in re.finditer(re.escape(f), text)
    ]
    return [(text.count("\n", 0, at), w) for at, w in hits]


def _code_names(node) -> list:
    if isinstance(node, ast.Name):
        return [node.id]
    if isinstance(node, ast.Attribute):
        return [node.attr]
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return [node.name]
    if isinstance(node, ast.arg):
        return [node.arg]
    if isinstance(node, ast.keyword) and node.arg is not None:
        return [node.arg]
    if isinstance(node, ast.alias):
        return [n for n in (node.name.split(".")[-1], node.asname) if n]
    return []


def scan_code_names(rel: str, tree, forbidden: set) -> list:
    found = set()
    for node in ast.walk(tree):
        for name in _code_names(node):
            if {name, *name.split("_")} & forbidden:
                found.add((node.lineno, name))
    return [f"{rel}:{line} {name}" for line, name in sorted(found)]


def scan_strings(rel: str, tree, forbidden: set) -> list:
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            # the line within a multi-line string is exact for a docstring, approximate for a
            # string with escaped or joined lines
            found += [
                (node.lineno + off, w) for off, w in _text_hits(node.value, forbidden)
            ]
    return [f"{rel}:{line} {w}" for line, w in sorted(set(found))]


def scan_comments(rel: str, source: str, forbidden: set) -> list:
    found = []
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type == tokenize.COMMENT:
            found += [
                (token.start[0], w) for _, w in _text_hits(token.string, forbidden)
            ]
    return [f"{rel}:{line} {w}" for line, w in sorted(set(found))]


def _absolute(rel: str, node: ast.ImportFrom) -> str:
    """The module a ``from`` import names, with a relative import resolved against ``rel``."""
    if not node.level:
        return node.module
    package = Path(rel).parent.parts
    base = package[: len(package) - (node.level - 1)]
    return ".".join(base + ((node.module,) if node.module else ()))


def scan_imports(rel: str, tree) -> list:
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            modules = [_absolute(rel, node)]
        else:
            continue
        found += [f"{rel}:{node.lineno} {m}" for m in modules if not import_allowed(m)]
    return found


class _LayerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = layer_files()
        cls.forbidden = forbidden_words()
        cls.sources = {rel: (REPO_ROOT / rel).read_text() for rel in cls.files}
        cls.trees = {rel: ast.parse(src) for rel, src in cls.sources.items()}

    def assertNoHits(self, found):
        # exactly the known hits of the calling test, in both directions (U17)
        self.assertEqual(
            KNOWN_HITS.get(self._testMethodName, []), found, "\n" + "\n".join(found)
        )


class TestTheLayer(_LayerTestCase):
    def test_the_derived_files_hold_the_audits_list(self):
        self.assertLessEqual(AUDIT_LIST, set(self.files))

    def test_no_test_and_no_client_factory_is_in_it(self):
        self.assertIn(_FACTORY_CONTRACT, self.files)
        for rel in self.files:
            self.assertFalse(rel.startswith("datastorekit/tests/"), rel)
            if "factor" in Path(rel).name:
                self.assertEqual(_FACTORY_CONTRACT, rel)

    def test_the_vocabulary_holds_the_registry_and_the_packages(self):
        # a vocabulary that came out empty would pass every scan below
        tables, columns = registry_words()
        self.assertLessEqual({"BackgroundModel", "redshift", "tolerance"}, tables)
        self.assertLessEqual({"model_serial", "parent_serial"}, columns)
        self.assertLessEqual(
            {"CosmologyModels", "MetadataConcepts", "Caching"}, project_packages()
        )
        self.assertFalse(LAYER_WORDS & self.forbidden)


class TestTheLayerNamesNoProjectWord(_LayerTestCase):
    def test_no_code_name(self):
        found = []
        for rel in self.files:
            found += scan_code_names(rel, self.trees[rel], self.forbidden)
        self.assertNoHits(found)

    def test_no_string_or_docstring(self):
        found = []
        for rel in self.files:
            found += scan_strings(rel, self.trees[rel], self.forbidden)
        self.assertNoHits(found)

    def test_no_comment(self):
        found = []
        for rel in self.files:
            found += scan_comments(rel, self.sources[rel], self.forbidden)
        self.assertNoHits(found)


class TestTheLayerImportsNoProjectPackage(_LayerTestCase):
    def test_every_import_is_allowed(self):
        found = []
        for rel in self.files:
            found += scan_imports(rel, self.trees[rel])
        self.assertNoHits(found)

    def test_the_allow_list(self):
        # an allow-list that grew silently would pass every scan above
        for module in (
            "datastorekit.defaults",
            "datastorekit._timing",
            "datastorekit.SQL.factory_base",
            "datastorekit.tools.shard_key_audit",
            "sqlalchemy.exc",
        ):
            with self.subTest(allowed=module):
                self.assertTrue(import_allowed(module))
        for module in (
            "datastorekit.tests.client.registry",
            "datastorekit.tests.client.factories",
            "config.datastore",
            "CosmologyModels.model_ids",
            "MetadataConcepts",
        ):
            with self.subTest(refused=module):
                self.assertFalse(import_allowed(module))


if __name__ == "__main__":
    unittest.main()
