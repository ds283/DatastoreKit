"""
The package's import guard: ``datastorekit`` imports only the standard library, ``ray``,
``sqlalchemy`` and itself.

Every module under ``datastorekit/`` (the tests included) is parsed with ``ast``, and every module
it imports is collected, including imports inside functions and classes. A relative import is an
import of the package itself. The root of each imported module must be in
``sys.stdlib_module_names``, or be ``ray``, ``sqlalchemy`` or ``datastorekit``.

The second test checks, in a fresh interpreter, that importing ``datastorekit.shard_paths`` loads
neither ``ray`` nor ``sqlalchemy``: the standalone tool that reads shard records depends on it.

This guard is about imports only. Nothing is opened and Ray is never started.
"""

import ast
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import datastorekit

PACKAGE_DIR = Path(datastorekit.__file__).resolve().parent
ALLOWED_ROOTS = {"ray", "sqlalchemy", "datastorekit"}


def imported_modules(path: Path):
    """Every module ``path`` imports, as (line, dotted name); relative imports name the package."""
    tree = ast.parse(path.read_text(), filename=str(path))
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom):
            if node.level > 0:
                found.append((node.lineno, "datastorekit"))
            else:
                found.append((node.lineno, node.module))
    return found


class TestPackageImports(unittest.TestCase):
    def test_every_import_is_stdlib_ray_sqlalchemy_or_the_package(self):
        modules = sorted(PACKAGE_DIR.rglob("*.py"))
        self.assertGreater(len(modules), 0)
        allowed = set(sys.stdlib_module_names) | ALLOWED_ROOTS
        offending = []
        for path in modules:
            for line, name in imported_modules(path):
                if name.split(".")[0] not in allowed:
                    offending.append(
                        f"{path.relative_to(PACKAGE_DIR.parent)}:{line}: {name}"
                    )
        self.assertEqual(offending, [], "\n".join(offending))

    def test_shard_paths_loads_neither_ray_nor_sqlalchemy(self):
        code = (
            "import sys; import datastorekit.shard_paths; "
            "print(sorted(m for m in ('ray', 'sqlalchemy') if m in sys.modules))"
        )
        env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
        env["PYTHONPATH"] = str(PACKAGE_DIR.parent)
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            env=env,
            cwd=tempfile.gettempdir(),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[]")


if __name__ == "__main__":
    unittest.main()
