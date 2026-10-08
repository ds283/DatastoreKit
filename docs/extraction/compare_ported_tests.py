#!/usr/bin/env python3
"""
The port check of the extraction campaign (prompt 03a §2.4; README §6.2, U9).

A ported test module is re-fixtured onto the neutral test client, so it cannot be compared with
its source line by line, as ``compare_with_source.py`` compares a moved module. This script
checks, mechanically, what re-fixturing must keep (README §5 rule 6): the names of the tests, and
the assertions each one makes. Run it from the repository root with the venv's interpreter:

    ./venv/bin/python docs/extraction/compare_ported_tests.py

For each pair of PORTED, it reads the source module with ``git show`` at the import commit, and the
package module from the tree, parses both with ``ast``, and requires:

1. **The names.** The set of ``Class.method`` of every test method (a method of a class whose name
   begins with ``test``) equals the source's, after NAME_MAP. Every class the source defines at the
   top level is defined at the top level of the package module, under its name after NAME_MAP,
   with the same bases, by name (each base as written, after NAME_MAP).
2. **The assertion skeleton.** A function's *skeleton* is the ordered list, by a walk of its body
   in source order, of: each call ``self.<name>(...)`` or ``<name>(...)`` whose name begins with
   ``assert`` or ``fail``, whether or not it is used as a context manager; each ``raise
   AssertionError``; and each ``self.subTest``. A call ``<anything>.<name>(...)`` of such a name,
   or of ``subTest``, counts as ``self``'s does (``case.assertEqual``, ``super().assertIdentical``,
   ``a_mock.assert_not_called``), so that a helper given the test case as an argument cannot
   assert unseen. A function nested in another is its own function,
   and its body is not part of the enclosing one's skeleton (a lambda is not a function here: its
   body is part of the function it is written in). Every function or method of the source module
   whose skeleton is not empty exists in the package module under the same qualified name (its
   enclosing classes and functions, dotted, after NAME_MAP), and its skeleton is equal to the
   source's. Arguments are not compared, and neither is anything else.
3. **Nothing added that asserts.** A function of the package module whose skeleton is not empty
   is a function of the source module, with the same skeleton: a function the source does not
   have, or one whose skeleton the source has empty, may not assert, so that a new helper cannot
   hide a changed assertion.

NAME_MAP holds the R-name changes (prompt 03a §2.1, U12): per package module, a source class or
method name and the name it was given. It is empty for prompt 03a's modules. Nothing else is
configurable.

Output, per module: the counts of tests, of functions compared and of assertions; each difference,
naming the qualified name and the first position at which the skeletons differ; then a final
``OK`` or ``FAIL`` line. The script exits 0 when every module passes, 1 otherwise, and 2 when it
cannot run (a source cannot be read at the import commit, or a module does not parse). It writes
nothing.
"""

import ast
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SOURCE_REPO = Path("/Users/ds283/Documents/Code/SecondaryGWKit")
IMPORT_COMMIT = "6f7f291"

REPO_ROOT = Path(__file__).resolve().parents[2]

# (source path at the import commit, package path)
PORTED: List[Tuple[str, str]] = [
    (
        "Datastore/tests/test_replicated_write.py",
        "datastorekit/tests/test_replicated_write.py",
    ),
    (
        "Datastore/tests/test_reconcile_at_open.py",
        "datastorekit/tests/test_reconcile_at_open.py",
    ),
    (
        "Datastore/tests/test_prune_at_open.py",
        "datastorekit/tests/test_prune_at_open.py",
    ),
    (
        "Datastore/tests/test_version_row_at_open.py",
        "datastorekit/tests/test_version_row_at_open.py",
    ),
    (
        "Datastore/tests/test_read_only_pool.py",
        "datastorekit/tests/test_read_only_pool.py",
    ),
    (
        "Datastore/tests/test_one_timestamp_per_write.py",
        "datastorekit/tests/test_one_timestamp_per_write.py",
    ),
    (
        "Datastore/tests/test_absolute_shard_record_refused.py",
        "datastorekit/tests/test_absolute_shard_record_refused.py",
    ),
    (
        "Datastore/tests/test_closed_store_refusals.py",
        "datastorekit/tests/test_closed_store_refusals.py",
    ),
    (
        "Datastore/tests/test_store_inventory.py",
        "datastorekit/tests/test_store_inventory.py",
    ),
    (
        "Datastore/tests/test_store_schema.py",
        "datastorekit/tests/test_store_schema.py",
    ),
    (
        "Datastore/tests/test_store_reader.py",
        "datastorekit/tests/test_store_reader.py",
    ),
    (
        "Datastore/tests/test_foreign_key_check.py",
        "datastorekit/tests/test_foreign_key_check.py",
    ),
    (
        "Datastore/tests/test_schema_builder.py",
        "datastorekit/tests/test_schema_builder.py",
    ),
    (
        "Datastore/tests/real_store_fixtures.py",
        "datastorekit/tests/real_store_fixtures.py",
    ),
    (
        "Datastore/tests/schema_description.py",
        "datastorekit/tests/schema_description.py",
    ),
]

# R-name: package path -> {source class or method name: its name in the package}
NAME_MAP: Dict[str, Dict[str, str]] = {
    # prompt 03b, U12: four test names that are the source's table names, by the table map
    "datastorekit/tests/test_read_only_pool.py": {
        "test_LambdaCDM": "test_dial_setting",
        "test_QCD_Cosmology": "test_knob_setting",
        "test_tolerance": "test_gauge_setting",
        "test_GkSourcePolicy": "test_routing_rule",
    },
}


class CannotRun(Exception):
    pass


def git_show(path: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(SOURCE_REPO), "show", f"{IMPORT_COMMIT}:{path}"],
        capture_output=True,
    )
    if result.returncode != 0:
        raise CannotRun(f"cannot read {path} at {IMPORT_COMMIT} in {SOURCE_REPO}")
    return result.stdout.decode("utf-8")


def parse(text: str, where: str) -> ast.Module:
    try:
        return ast.parse(text, filename=where)
    except SyntaxError as e:
        raise CannotRun(f"{where} does not parse: {e}")


# ------------------------------------------------------------------------------------------------
# the names
# ------------------------------------------------------------------------------------------------

FUNCTIONS = (ast.FunctionDef, ast.AsyncFunctionDef)


def top_level_classes(tree: ast.Module) -> Dict[str, ast.ClassDef]:
    return {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}


def test_names(classes: Dict[str, ast.ClassDef], rename) -> set:
    return {
        f"{rename(name)}.{rename(item.name)}"
        for name, node in classes.items()
        for item in node.body
        if isinstance(item, FUNCTIONS) and item.name.startswith("test")
    }


def bases(node: ast.ClassDef, rename) -> List[str]:
    return [
        ".".join(rename(part) for part in ast.unparse(base).split("."))
        for base in node.bases
    ]


# ------------------------------------------------------------------------------------------------
# the assertion skeletons
# ------------------------------------------------------------------------------------------------


def _is_assertion_name(name: str) -> bool:
    return name.startswith("assert") or name.startswith("fail")


class _Skeleton(ast.NodeVisitor):
    """The skeleton of one function's own body, in source order; nested functions and classes
    are not entered."""

    def __init__(self):
        self.items: List[str] = []

    def visit_FunctionDef(self, node):
        pass

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        pass

    def visit_Call(self, node: ast.Call):
        func = node.func
        if isinstance(func, ast.Attribute):
            if _is_assertion_name(func.attr):
                self.items.append(func.attr)
            elif func.attr == "subTest":
                self.items.append("subTest")
        elif isinstance(func, ast.Name) and _is_assertion_name(func.id):
            self.items.append(func.id)
        self.generic_visit(node)

    def visit_Raise(self, node: ast.Raise):
        exc = node.exc
        if isinstance(exc, ast.Call):
            exc = exc.func
        if isinstance(exc, ast.Name) and exc.id == "AssertionError":
            self.items.append("raise AssertionError")
        self.generic_visit(node)


def skeleton(node) -> List[str]:
    visitor = _Skeleton()
    for statement in node.body:
        visitor.visit(statement)
    return visitor.items


def functions(tree: ast.Module, rename) -> Dict[str, List[str]]:
    """Every function and method, at any depth, by qualified name (classes and functions
    dotted; a second definition of one name in one scope is suffixed #2, #3, ...) -> its
    skeleton."""
    out: Dict[str, List[str]] = {}
    scopes: set = set()

    def walk(node, prefix: str):
        for child in ast.iter_child_nodes(node):
            if not isinstance(child, (ast.ClassDef,) + FUNCTIONS):
                walk(child, prefix)
                continue
            name = prefix + rename(child.name)
            qualified = name
            n = 1
            while qualified in scopes:
                n += 1
                qualified = f"{name}#{n}"
            scopes.add(qualified)
            if isinstance(child, FUNCTIONS):
                out[qualified] = skeleton(child)
            walk(child, qualified + ".")

    walk(tree, "")
    return out


def first_difference(a: List[str], b: List[str]) -> Tuple[int, str, str]:
    for i in range(max(len(a), len(b))):
        x = a[i] if i < len(a) else "(nothing)"
        y = b[i] if i < len(b) else "(nothing)"
        if x != y:
            return i + 1, x, y
    raise ValueError("the skeletons are equal")


# ------------------------------------------------------------------------------------------------
# one module
# ------------------------------------------------------------------------------------------------


def check(source_path: str, package_path: str) -> Tuple[List[str], List[str]]:
    """Returns (report lines, differences)."""
    names = NAME_MAP.get(package_path, {})

    def rename(name: str) -> str:
        return names.get(name, name)

    def same(name: str) -> str:
        return name

    source = parse(git_show(source_path), f"{source_path} at {IMPORT_COMMIT}")
    package_file = REPO_ROOT / package_path
    if not package_file.is_file():
        return [], [f"MISSING in the package: {package_path}"]
    package = parse(package_file.read_text(), package_path)

    differences: List[str] = []

    # 1. the names, and the bases of each class
    source_classes = top_level_classes(source)
    package_classes = top_level_classes(package)
    source_tests = test_names(source_classes, rename)
    package_tests = test_names(package_classes, same)
    for name in sorted(source_tests - package_tests):
        differences.append(f"test missing from the package: {name}")
    for name in sorted(package_tests - source_tests):
        differences.append(f"test not in the source: {name}")
    for name, node in source_classes.items():
        mapped = rename(name)
        if mapped not in package_classes:
            differences.append(f"class missing from the package: {mapped}")
            continue
        want = bases(node, rename)
        got = bases(package_classes[mapped], same)
        if want != got:
            differences.append(f"class {mapped}: bases {got}, the source's {want}")

    # 2 and 3. the assertion skeletons
    source_functions = functions(source, rename)
    package_functions = functions(package, same)
    compared = 0
    assertions = 0
    for name, items in source_functions.items():
        if not items:
            continue
        compared += 1
        assertions += len(items)
        if name not in package_functions:
            differences.append(
                f"{name}: asserts in the source ({len(items)}), missing from the package"
            )
            continue
        got = package_functions[name]
        if got != items:
            position, want, have = first_difference(items, got)
            differences.append(
                f"{name}: skeleton differs at position {position}: the source has "
                f"{want}, the package {have} ({len(items)} in the source, {len(got)} in the "
                "package)"
            )
    for name, items in package_functions.items():
        if not items:
            continue
        if name not in source_functions:
            differences.append(
                f"{name}: not in the source, and asserts ({', '.join(items)})"
            )
        elif not source_functions[name]:
            differences.append(
                f"{name}: asserts in the package ({', '.join(items)}), and not in the "
                "source"
            )

    report = [
        f"  tests: {len(package_tests)} (source {len(source_tests)})",
        f"  classes: {len(package_classes)} (source {len(source_classes)})",
        f"  functions compared: {compared}",
        f"  assertions: {assertions}",
    ]
    return report, differences


def main(argv: List[str]) -> int:
    if argv:
        print(f"!! {Path(__file__).name} takes no arguments", file=sys.stderr)
        return 2
    head = subprocess.run(
        ["git", "-C", str(SOURCE_REPO), "log", "-1", "--format=%H %s", IMPORT_COMMIT],
        capture_output=True,
        text=True,
    )
    if head.returncode != 0:
        print(f"!! cannot read {IMPORT_COMMIT} in {SOURCE_REPO}", file=sys.stderr)
        return 2
    print(f"source:  {SOURCE_REPO} at {head.stdout.strip()}")
    print(f"package: {REPO_ROOT}")
    print()

    failed = 0
    for source_path, package_path in PORTED:
        try:
            report, differences = check(source_path, package_path)
        except CannotRun as e:
            print(f"!! {e}", file=sys.stderr)
            return 2
        verdict = "ok" if not differences else f"{len(differences)} difference(s)"
        print(f"{package_path} (from {source_path}): {verdict}")
        for line in report:
            print(line)
        for line in differences:
            print(f"  DIFFERS  {line}")
        if differences:
            failed += 1
    print()
    if failed:
        print(f"FAIL: {failed} of {len(PORTED)} module(s) differ from their source")
        return 1
    print(
        f"OK: {len(PORTED)} module(s) keep their source's tests, classes and assertion "
        "skeletons"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
