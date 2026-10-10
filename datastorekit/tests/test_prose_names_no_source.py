"""
The package's prose names nothing of the source repository's layout (extraction prompt 09;
README §6.2, U40).

The package was imported from the source repository at the import commit ``6f7f291``
(``PROVENANCE.md``), and its comments and docstrings, and those of the tests ported with it, once
pointed their reader at the source's files, campaigns and directories, none of which exist here.
Prompt 09 rewrote that prose for this package; this module keeps it so.

**What it reads.** Every ``.py`` file under ``datastorekit/``, the layer and its tests alike, this
module included. ``package_files()`` derives the set from the filesystem, as the layer guard's
``layer_files()`` does, so that a file added to the package is read before anyone commits it. From
each file it reads two kinds of prose, and nothing else:

1. every comment, by ``tokenize``;
2. every docstring (the first statement of a module, class or function, when that statement is a
   string), found by ``ast`` and read from the source text, line by line.

A runtime string, an f-string and a name are code, and are not read.

**What it forbids.** Four rules (``RULES``), each named in a failure:

1. *a path of the source's layout*: a path that begins with the source's package directory, its
   tools directory, or a ``prompts`` or ``docs`` directory (not inside a longer path or a word),
   and that does not exist relative to the top of this repository. This repository's own
   documents, and the package's own modules, exist, and pass;
2. *a module of the source*: a dotted module of the source's package, by its whole module name. A
   method of the package's own class ``Datastore`` is not one;
3. *a name of the source*: the source's top-level names, its factory and registry packages, its
   entry script, its configuration module and its utilities module;
4. *a campaign or directory of the source*: the source's campaign names, and its scratch
   directory as a path.

There is no allow list: a line that matches is rewritten. The source's commits, and bare
citations of its records, are not matched here; they are a matter for review. The source may be
named generically ("the source repository"), and the import commit and ``PROVENANCE.md`` may be
cited.

Each failure names ``file:line rule matched-text``, for every file at once. No store is opened, no
client is read, and no Ray starts.
"""

import ast
import io
import re
import tokenize
import unittest
from pathlib import Path

import ray

# the top of this repository, against which a path in prose is checked
TOP = Path(__file__).resolve().parents[2]

PACKAGE = "datastorekit"

# the four rules, by name; each pattern is matched within one physical line of prose
RULES = (
    (
        "a path of the source's layout",
        re.compile(r"(?<![\w/.])(?:Datastore|tools|prompts|docs)/[\w./\-]*"),
    ),
    (
        "a module of the source",
        re.compile(
            r"(?<![\w.])Datastore\.(?:SQL|tests|replication|contract|object|shard_paths"
            r"|store_reader|store_inventory)(?!\w)"
        ),
    ),
    (
        "a name of the source",
        re.compile(
            r"repository root|REPO_ROOT|ObjectFactories|RunRegistry|main\.py"
            r"|config\.defaults|utilities\.py"
        ),
    ),
    (
        "a campaign or directory of the source",
        re.compile(
            r"a3-v2-readiness|datastore-generic|datastore-integrity|datastore-portability"
            r"|store-fingerprint|store-retirement|(?<![\w/.])var/"
        ),
    ),
)

_PATH_RULE = RULES[0][0]


def tearDownModule():
    if ray.is_initialized():
        raise AssertionError("Ray was initialised by test_prose_names_no_source")


def package_files(top: Path = TOP) -> list:
    """Every ``.py`` file under the package, relative to ``top``, sorted."""
    return sorted(
        path.relative_to(top).as_posix() for path in (top / PACKAGE).rglob("*.py")
    )


def _docstring_spans(tree) -> list:
    """((start line, column), (end line, column)) of every docstring in ``tree``."""
    spans = []
    for node in ast.walk(tree):
        if not isinstance(
            node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            continue
        if not node.body:
            continue
        first = node.body[0]
        if (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        ):
            value = first.value
            spans.append(
                (
                    (value.lineno, value.col_offset),
                    (value.end_lineno, value.end_col_offset),
                )
            )
    return spans


def prose_lines(source: str) -> list:
    """(line, text) of every physical line of prose in ``source``: its comments and docstrings."""
    spans = _docstring_spans(ast.parse(source))
    lines = []
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type == tokenize.COMMENT:
            lines.append((token.start[0], token.string))
        elif token.type == tokenize.STRING and any(
            start <= token.start and token.end <= end for start, end in spans
        ):
            # a docstring, read from the source text one physical line at a time
            for offset, text in enumerate(token.string.split("\n")):
                lines.append((token.start[0] + offset, text))
    return lines


def _exists(match: str, top: Path) -> bool:
    """Whether the path ``match`` names exists relative to ``top``, trailing punctuation aside."""
    path = match.rstrip(".,;:")
    return bool(path) and (top / path).exists()


def scan(rel: str, source: str, top: Path = TOP) -> list:
    """``file:line rule matched-text`` of every match of a rule in the prose of ``source``."""
    found = []
    for line, text in prose_lines(source):
        for name, pattern in RULES:
            for match in pattern.finditer(text):
                if name == _PATH_RULE and _exists(match.group(0), top):
                    continue
                found.append(f"{rel}:{line} {name} {match.group(0)}")
    return found


# ------------------------------------------------------------------------------------------------
# the planted forms: runtime strings, which this module does not read in itself
# ------------------------------------------------------------------------------------------------

# one form of each rule, and the rule that must find it
PLANTED = (
    ("a path of the source's layout", "Datastore/shard_paths.py"),
    ("a path of the source's layout", "tools/shard_key_audit.py"),
    ("a path of the source's layout", "prompts/a-campaign/README.md"),
    ("a path of the source's layout", "docs/no-such-document.md"),
    ("a module of the source", "Datastore.SQL.ShardedPool"),
    ("a module of the source", "Datastore.object"),
    ("a name of the source", "the repository root"),
    ("a name of the source", "REPO_ROOT"),
    ("a name of the source", "ObjectFactories"),
    ("a name of the source", "RunRegistry"),
    ("a name of the source", "main.py"),
    ("a name of the source", "config.defaults"),
    ("a name of the source", "utilities.py"),
    ("a campaign or directory of the source", "a3-v2-readiness"),
    ("a campaign or directory of the source", "datastore-generic"),
    ("a campaign or directory of the source", "datastore-integrity"),
    ("a campaign or directory of the source", "datastore-portability"),
    ("a campaign or directory of the source", "store-fingerprint"),
    ("a campaign or directory of the source", "store-retirement"),
    ("a campaign or directory of the source", "var/stores"),
)

# what is not prose, or names nothing of the source, and must not be found
NOT_FOUND = (
    "docs/client-contract.md",
    "datastorekit/tools/sharded_store.py",
    "datastorekit.tools.shard_key_audit",
    "Datastore.object_get",
    "Datastore.set_version",
    "Datastore.py",
)


def _as_comment(form: str) -> str:
    return f"x = 1\n# see {form}\n"


def _as_module_docstring(form: str) -> str:
    return f'"""\nThe module.\n\nSee {form}.\n"""\n\nx = 1\n'


def _as_function_docstring(form: str) -> str:
    return f'def f():\n    """\n    See {form}.\n    """\n    return 1\n'


def _as_code(form: str) -> str:
    # the same form in a runtime string, an f-string and a name; none is prose
    name = re.sub(r"\W", "_", form)
    return (
        f"x = 1\n"
        f"plain = {form!r}\n"
        f"formatted = f'{{plain}} {form}'\n"
        f"{name} = 2\n"
        f"call({form!r}, key={form!r})\n"
    )


class TestThePackage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = package_files()

    def test_no_comment_or_docstring_names_the_source(self):
        found = []
        for rel in self.files:
            found += scan(rel, (TOP / rel).read_text())
        self.assertEqual([], found, "\n" + "\n".join(found))

    def test_the_scan_reaches_the_layer_and_the_tests(self):
        # a walk that skipped the tests, or came out empty, would pass the scan above
        for rel in (
            "datastorekit/SQL/ShardedPool.py",
            "datastorekit/tests/standin_pool.py",
            "datastorekit/tests/test_replicated_write.py",
            "datastorekit/tests/test_prose_names_no_source.py",
        ):
            with self.subTest(rel=rel):
                self.assertIn(rel, self.files)
        self.assertGreaterEqual(len(self.files), 60)


class TestTheRules(unittest.TestCase):
    def test_each_rule_finds_its_form_in_prose(self):
        for rule, form in PLANTED:
            for kind, source in (
                ("comment", _as_comment(form)),
                ("module docstring", _as_module_docstring(form)),
                ("function docstring", _as_function_docstring(form)),
            ):
                with self.subTest(form=form, kind=kind):
                    found = scan("planted.py", source)
                    self.assertTrue(found, source)
                    self.assertIn(f" {rule} ", found[0])
                    line = 2 if kind == "comment" else 4 if "module" in kind else 3
                    self.assertTrue(found[0].startswith(f"planted.py:{line} "), found)

    def test_what_is_not_prose_is_not_read(self):
        for _, form in PLANTED:
            with self.subTest(form=form):
                self.assertEqual([], scan("planted.py", _as_code(form)))

    def test_what_names_nothing_of_the_source_is_not_found(self):
        for form in NOT_FOUND:
            for kind, source in (
                ("comment", _as_comment(form)),
                ("module docstring", _as_module_docstring(form)),
                ("function docstring", _as_function_docstring(form)),
            ):
                with self.subTest(form=form, kind=kind):
                    self.assertEqual([], scan("planted.py", source))

    def test_the_path_rule_checks_existence(self):
        # the existence check is what lets this repository's own documents through
        self.assertTrue((TOP / "docs" / "client-contract.md").exists())
        self.assertEqual(
            [], scan("planted.py", _as_comment("docs/client-contract.md."))
        )
        self.assertEqual(
            ["planted.py:2 a path of the source's layout docs/client-contract.txt"],
            scan("planted.py", _as_comment("docs/client-contract.txt")),
        )


if __name__ == "__main__":
    unittest.main()
