#!/usr/bin/env python3
"""
Measure a client's imports of its datastore layer, for its adoption checklist (extraction prompt
07a §2.2; ``docs/adoption/``).

A client adopts ``datastorekit`` by deleting its own copy of the layer and rewriting every import
of it by the module map (``PROVENANCE.md``). This script finds those imports. It reads **one
client at one commit, through ``git ls-tree`` and ``git show`` only**: the client's working tree
is never read, and nothing of the client is imported, run or opened. Each tracked ``.py`` file is
parsed with ``ast``.

What it reports, for the files outside the layer's own:

- **Imports of a layer module.** Every ``import M`` and ``from M import ...`` statement that names
  one, wherever it stands: at module level, or nested in a function, a class, an ``if`` (``if
  TYPE_CHECKING:`` among them), a ``try`` or a ``with``. A statement is *nested* when it is not a
  direct child of the module's body; the innermost enclosing construct is given. Relative imports
  are resolved against the file's package. ``from P import X``, where ``P.X`` is a layer module,
  counts as an import of ``P.X``. The package root (``from Datastore import DatastoreObject``)
  is a layer module. A statement is counted once, however many layer modules it names.
- **String literals** whose whole value is a layer module's dotted name, or such a name followed
  by ``.`` and more (a ``mock.patch`` target), for the layer modules whose name has a dot; the
  longest such module is the one named. The bare word ``Datastore`` is also the actor's class
  name, so it is not matched alone, and a path into the factory package (other than its
  ``base``) names a factory, not the layer.
- **``importlib.import_module`` (and ``__import__``) calls** whose first argument is such a
  literal. These are listed apart from the other literals.
- **Imports of the client's factory modules**, the modules of the factory package other than the
  layer's ``base.py``, the package itself included. They are not layer imports, and are given by
  count only.
- **Names that move into the package**, where a client has them: imports of a client module's
  names that ``datastorekit`` now provides (each client's ``moved`` entry in ``CLIENTS``).
- The files that do not parse, by name.

Each client's repository, default commit, layer files and factory package are constants below,
measured by prompt 07a. The layer modules are the layer files' dotted names.

Run it from the repository root with the venv's interpreter:

    ./venv/bin/python docs/extraction/measure_client_imports.py <client> [--commit SHA] [--json]

where ``<client>`` is ``sgk``, ``cpbh`` or ``si``. It prints Markdown, or JSON with ``--json``.
Two runs at one commit give the same bytes. It exits 0 on success and 2 when it cannot read the
client. It imports only the standard library. It names clients, so it lives here, beside
``measure_client_vocabulary.py``, and never under ``datastorekit/``.
"""

import argparse
import ast
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import List, Optional

CODE_DIR = Path("/Users/ds283/Documents/Code")
SCRIPT = "docs/extraction/measure_client_imports.py"

# the layer each of CPBH and SI carries: nine files
_NINE = (
    "Datastore/__init__.py",
    "Datastore/object.py",
    "Datastore/SQL/__init__.py",
    "Datastore/SQL/ClientPool.py",
    "Datastore/SQL/Datastore.py",
    "Datastore/SQL/ProfileAgent.py",
    "Datastore/SQL/SerialPoolBroker.py",
    "Datastore/SQL/ShardedPool.py",
    "Datastore/SQL/ObjectFactories/base.py",
)

CLIENTS = {
    "sgk": {
        "name": "SecondaryGWKit (SGK)",
        "repository": "SecondaryGWKit",
        "commit": "b510bc9",
        # PROVENANCE.md's seventeen files
        "layer": (
            "Datastore/__init__.py",
            "Datastore/object.py",
            "Datastore/contract.py",
            "Datastore/replication.py",
            "Datastore/shard_paths.py",
            "Datastore/store_reader.py",
            "Datastore/store_inventory.py",
            "Datastore/SQL/__init__.py",
            "Datastore/SQL/schema.py",
            "Datastore/SQL/ShardedPool.py",
            "Datastore/SQL/Datastore.py",
            "Datastore/SQL/ClientPool.py",
            "Datastore/SQL/SerialPoolBroker.py",
            "Datastore/SQL/ProfileAgent.py",
            "Datastore/SQL/ObjectFactories/base.py",
            "tools/sharded_store.py",
            "tools/shard_key_audit.py",
        ),
        "factories": "Datastore/SQL/ObjectFactories/",
        "moved": {},
    },
    "cpbh": {
        "name": "ChamPBH (CPBH)",
        "repository": "ChamPBH",
        "commit": "52142d7",
        "layer": _NINE,
        "factories": "Datastore/SQL/ObjectFactories/",
        # the version-keyed lookup's two names, now datastorekit.contract's (prompt 06)
        "moved": {"config.version": ("VERSION_SERIAL_KEY", "require_version_serial")},
    },
    "si": {
        "name": "StochasticInstantons (SI)",
        "repository": "StochasticInstantons",
        "commit": "7bb3efd",
        "layer": _NINE,
        "factories": "Datastore/SQL/ObjectFactories/",
        "moved": {},
    },
}


class CannotRead(Exception):
    pass


def git(repository: str, *args: str) -> bytes:
    path = CODE_DIR / repository
    if not path.is_dir():
        raise CannotRead(f"{path} is not a directory")
    result = subprocess.run(["git", "-C", str(path), *args], capture_output=True)
    if result.returncode != 0:
        raise CannotRead(
            f"git {' '.join(args)} failed in {repository}: "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return result.stdout


def module_of(path: str) -> str:
    """The dotted module name of a ``.py`` path; a package's ``__init__.py`` names the package."""
    parts = path[: -len(".py")].split("/")
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def package_of(path: str) -> List[str]:
    """The package a relative import in ``path`` is resolved against."""
    parts = path[: -len(".py")].split("/")
    return parts[:-1]


def group_of(path: str) -> str:
    """The group a file's hits are counted under: its top-level directory, except that the
    layer's directory is split into the factory package and its other subdirectories."""
    parts = path.split("/")
    if len(parts) == 1:
        return "(top level)"
    if path.startswith("Datastore/SQL/ObjectFactories/"):
        return "Datastore/SQL/ObjectFactories/"
    if parts[0] == "Datastore" and len(parts) > 2:
        return "/".join(parts[:2]) + "/"
    return parts[0] + "/"


def context_of(stack: List[ast.AST]) -> Optional[str]:
    """``None`` for a direct child of the module's body; otherwise the innermost enclosing
    construct."""
    for node in reversed(stack):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return f"def {node.name}"
        if isinstance(node, ast.ClassDef):
            return f"class {node.name}"
        if isinstance(node, ast.If):
            test = node.test
            name = (
                test.id
                if isinstance(test, ast.Name)
                else test.attr if isinstance(test, ast.Attribute) else None
            )
            return "if TYPE_CHECKING" if name == "TYPE_CHECKING" else "if"
        if isinstance(node, (ast.Try, ast.TryStar)):
            return "try"
        if isinstance(node, (ast.With, ast.AsyncWith)):
            return "with"
        if isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            return "loop"
    return "nested" if len(stack) > 0 else None


def alias_text(alias: ast.alias) -> str:
    return alias.name if alias.asname is None else f"{alias.name} as {alias.asname}"


class Measure:
    def __init__(self, client: str, commit: Optional[str]):
        spec = CLIENTS[client]
        self.client = client
        self.spec = spec
        self.repository = spec["repository"]
        self.given = commit if commit is not None else spec["commit"]
        self.layer_files = tuple(spec["layer"])
        self.layer_modules = {module_of(p) for p in self.layer_files}
        # longest first, so that a literal is matched to the most specific module it names
        self.dotted_layer = sorted(
            (m for m in self.layer_modules if "." in m), key=lambda m: (-len(m), m)
        )
        self.factory_dir = spec["factories"]
        self.factory_package = module_of(self.factory_dir + "__init__.py")
        self.moved = spec["moved"]

        self.imports: List[dict] = []
        self.strings: List[dict] = []
        self.import_module_calls: List[dict] = []
        self.factory_imports: List[dict] = []
        self.moved_imports: List[dict] = []
        self.unparsed: List[str] = []

    # --- reading -------------------------------------------------------------------------------

    def read(self) -> None:
        self.full = (
            git(self.repository, "rev-parse", f"{self.given}^{{commit}}")
            .decode()
            .strip()
        )
        self.subject = (
            git(self.repository, "show", "-s", "--format=%cs %s", self.full)
            .decode("utf-8", "replace")
            .strip()
        )
        listing = git(self.repository, "ls-tree", "-r", "-z", self.full)
        self.python_files = []
        for entry in listing.split(b"\x00"):
            if not entry:
                continue
            meta, path = entry.split(b"\t", 1)
            mode, kind, _ = meta.split(b" ")
            path = path.decode("utf-8", "replace")
            if kind == b"blob" and mode != b"120000" and path.endswith(".py"):
                self.python_files.append(path)
        self.python_files.sort()
        tracked = set(self.python_files)
        self.layer_absent = [p for p in self.layer_files if p not in tracked]
        self.read_files = [p for p in self.python_files if p not in self.layer_files]
        self.factory_modules = {
            module_of(p) for p in self.python_files if p.startswith(self.factory_dir)
        } - self.layer_modules
        for path in self.read_files:
            source = git(self.repository, "show", f"{self.full}:{path}")
            try:
                tree = ast.parse(source, filename=path)
            except (SyntaxError, ValueError):
                self.unparsed.append(path)
                continue
            self.scan(path, tree)

    # --- classifying ---------------------------------------------------------------------------

    def is_factory(self, module: str) -> bool:
        return module == self.factory_package or module in self.factory_modules

    def resolve_from(self, path: str, node: ast.ImportFrom) -> str:
        if node.level == 0:
            return node.module or ""
        base = package_of(path)
        if node.level > 1:
            base = base[: len(base) - (node.level - 1)]
        return ".".join(base + ([node.module] if node.module else []))

    def names_layer_module(self, value: str) -> Optional[str]:
        """The layer module ``value`` names, the longest that matches, or ``None``. A path into
        the factory package (other than the layer's ``base``) names a factory, not the layer.
        """
        for module in self.dotted_layer:
            if value == module or value.startswith(module + "."):
                inside = value == self.factory_package or value.startswith(
                    self.factory_package + "."
                )
                if inside and len(module) <= len(self.factory_package):
                    return None
                return module
        return None

    def scan(self, path: str, tree: ast.Module) -> None:
        group = group_of(path)
        string_skip = set()

        def visit(node: ast.AST, stack: List[ast.AST]) -> None:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                self.classify_import(path, group, node, context_of(stack))
            elif isinstance(node, ast.Call) and node.args:
                func = node.func
                called = (
                    func.attr
                    if isinstance(func, ast.Attribute)
                    else func.id if isinstance(func, ast.Name) else None
                )
                first = node.args[0]
                if (
                    called in ("import_module", "__import__")
                    and isinstance(first, ast.Constant)
                    and isinstance(first.value, str)
                ):
                    module = self.names_layer_module(first.value)
                    if module is not None:
                        string_skip.add(id(first))
                        self.import_module_calls.append(
                            {
                                "file": path,
                                "line": node.lineno,
                                "group": group,
                                "call": called,
                                "argument": first.value,
                                "module": module,
                            }
                        )
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and id(node) not in string_skip
            ):
                module = self.names_layer_module(node.value)
                if module is not None:
                    self.strings.append(
                        {
                            "file": path,
                            "line": node.lineno,
                            "group": group,
                            "literal": node.value,
                            "module": module,
                            "exact": node.value == module,
                        }
                    )
            child_stack = stack if isinstance(node, ast.Module) else stack + [node]
            for child in ast.iter_child_nodes(node):
                visit(child, child_stack)

        visit(tree, [])

    def classify_import(
        self, path: str, group: str, node: ast.AST, context: Optional[str]
    ) -> None:
        layer: List[str] = []
        factory = False
        if isinstance(node, ast.Import):
            names = [alias_text(a) for a in node.names]
            for alias in node.names:
                if alias.name in self.layer_modules:
                    layer.append(alias.name)
                elif self.is_factory(alias.name):
                    factory = True
            statement = "import"
            module_text = ", ".join(a.name for a in node.names)
        else:
            module = self.resolve_from(path, node)
            names = [alias_text(a) for a in node.names]
            if module in self.layer_modules:
                layer.append(module)
            if self.is_factory(module):
                factory = True
            for alias in node.names:
                sub = f"{module}.{alias.name}"
                if sub in self.layer_modules:
                    layer.append(sub)
                elif self.is_factory(sub):
                    factory = True
            statement = "from"
            module_text = ("." * node.level) + (node.module or "")
            for moved_module, moved_names in self.moved.items():
                if module == moved_module and any(
                    a.name in moved_names for a in node.names
                ):
                    self.moved_imports.append(
                        {
                            "file": path,
                            "line": node.lineno,
                            "group": group,
                            "module": module,
                            "names": names,
                        }
                    )
        hit = {
            "file": path,
            "line": node.lineno,
            "group": group,
            "nested": context,
            "statement": statement,
            "written": module_text,
        }
        if layer:
            self.imports.append(dict(hit, modules=sorted(set(layer)), names=names))
        if factory:
            self.factory_imports.append(hit)

    # --- reporting -----------------------------------------------------------------------------

    def data(self) -> dict:
        order = lambda h: (h["group"], h["file"], h["line"])
        imports = sorted(self.imports, key=order)
        groups = sorted({h["group"] for h in imports})
        by_group = []
        for group in groups:
            hits = [h for h in imports if h["group"] == group]
            by_group.append(
                {
                    "group": group,
                    "statements": len(hits),
                    "nested": sum(1 for h in hits if h["nested"] is not None),
                    "files": len({h["file"] for h in hits}),
                }
            )
        modules = Counter(m for h in imports for m in h["modules"])
        by_module = []
        for module in sorted(modules):
            names = Counter(
                n
                for h in imports
                if module in h["modules"] and h["statement"] == "from"
                for n in h["names"]
            )
            by_module.append(
                {
                    "module": module,
                    "statements": modules[module],
                    "names": {n: names[n] for n in sorted(names)},
                }
            )
        factory_groups = Counter(h["group"] for h in self.factory_imports)
        outside = sum(
            1
            for h in self.factory_imports
            if not h["file"].startswith(self.factory_dir)
        )
        return {
            "written by": SCRIPT,
            "client": self.client,
            "name": self.spec["name"],
            "repository": str(CODE_DIR / self.repository),
            "commit": self.full,
            "commit given": self.given,
            "commit date and subject": self.subject,
            "layer files": list(self.layer_files),
            "layer files absent at this commit": self.layer_absent,
            "layer modules": sorted(self.layer_modules),
            "factory package": self.factory_dir,
            "files read": len(self.read_files),
            "totals": {
                "layer imports": len(imports),
                "layer imports nested": sum(
                    1 for h in imports if h["nested"] is not None
                ),
                "files with a layer import": len({h["file"] for h in imports}),
                "string literals": len(self.strings),
                "string literals, exact": sum(1 for s in self.strings if s["exact"]),
                "import_module calls": len(self.import_module_calls),
                "factory imports": len(self.factory_imports),
                "factory imports outside the factory package": outside,
                "moved names imports": len(self.moved_imports),
                "files that do not parse": len(self.unparsed),
            },
            "by group": by_group,
            "by module": by_module,
            "imports": imports,
            "string literals": sorted(self.strings, key=order),
            "import_module calls": sorted(self.import_module_calls, key=order),
            "factory imports by group": {
                g: factory_groups[g] for g in sorted(factory_groups)
            },
            "moved names": {m: list(n) for m, n in self.moved.items()},
            "moved names imports": sorted(self.moved_imports, key=order),
            "files that do not parse": sorted(self.unparsed),
        }


def markdown(d: dict) -> str:
    t = d["totals"]
    out: List[str] = []
    w = out.append
    w(f"# Imports of the layer: {d['name']} at `{d['commit'][:7]}`")
    w("")
    w(
        f"Written by `{d['written by']}`, reading through `git ls-tree` and `git show` only."
    )
    w("")
    w(f"- **Repository:** `{d['repository']}`")
    w(
        f"- **Commit:** `{d['commit']}` (given as `{d['commit given']}`), "
        f"{d['commit date and subject']}"
    )
    w(
        f"- **Layer files** ({len(d['layer files'])}): "
        + ", ".join(f"`{p}`" for p in d["layer files"])
    )
    absent = d["layer files absent at this commit"]
    w(
        "- **Layer files absent at this commit:** "
        + (", ".join(f"`{p}`" for p in absent) if absent else "none")
    )
    w(f"- **Factory package:** `{d['factory package']}` (its `base.py` is the layer's)")
    w(
        f"- **Files read:** {d['files read']} tracked `.py` files outside the layer; "
        f"{t['files that do not parse']} do not parse"
    )
    w("")
    w("## Totals")
    w("")
    w("| What | Count |")
    w("|---|---|")
    w(
        f"| Import statements naming a layer module | **{t['layer imports']}** "
        f"in {t['files with a layer import']} files |"
    )
    w(f"| of which nested (not at module level) | {t['layer imports nested']} |")
    w(
        f"| String literals naming a layer module | {t['string literals']} "
        f"({t['string literals, exact']} exactly its name) |"
    )
    w(
        f"| `import_module` / `__import__` calls naming a layer module | "
        f"{t['import_module calls']} |"
    )
    w(
        f"| Import statements naming a factory module (not layer imports) | "
        f"{t['factory imports']} ({t['factory imports outside the factory package']} "
        f"outside `{d['factory package']}`) |"
    )
    if d["moved names"]:
        w(
            f"| Imports of names that move into the package | {t['moved names imports']} |"
        )
    w("")
    w("## Layer imports, by group")
    w("")
    w("| Group | Statements | Nested | Files |")
    w("|---|---|---|---|")
    for g in d["by group"]:
        w(f"| `{g['group']}` | {g['statements']} | {g['nested']} | {g['files']} |")
    w(
        f"| **total** | **{t['layer imports']}** | **{t['layer imports nested']}** | "
        f"**{t['files with a layer import']}** |"
    )
    w("")
    w("## Layer imports, by module")
    w("")
    w("A statement naming two layer modules is counted under each.")
    w("")
    w("| Module | Statements | Names imported by `from` (statements) |")
    w("|---|---|---|")
    for m in d["by module"]:
        names = ", ".join(f"`{n}` {c}" for n, c in m["names"].items()) or "—"
        w(f"| `{m['module']}` | {m['statements']} | {names} |")
    w("")
    w("## Every layer import")
    w("")
    current = None
    for h in d["imports"]:
        if h["group"] != current:
            if current is not None:
                w("")
            current = h["group"]
            count = next(g for g in d["by group"] if g["group"] == current)
            w(f"### `{current}` ({count['statements']})")
            w("")
            w("| File:line | Nested | Module | Names |")
            w("|---|---|---|---|")
        nested = h["nested"] if h["nested"] is not None else "—"
        if h["statement"] == "from":
            names = ", ".join(f"`{n}`" for n in h["names"])
            module = f"`{h['written']}`"
        else:
            names = "—"
            module = ", ".join(f"`{n}`" for n in h["names"])
        w(f"| `{h['file']}:{h['line']}` | {nested} | {module} | {names} |")
    w("")
    w("## String literals naming a layer module")
    w("")
    if d["string literals"]:
        w("| File:line | Literal | Exact |")
        w("|---|---|---|")
        for s in d["string literals"]:
            literal = s["literal"].replace("|", "\\|").replace("\n", " ")
            w(
                f"| `{s['file']}:{s['line']}` | `{literal}` | "
                f"{'yes' if s['exact'] else 'no'} |"
            )
    else:
        w("None.")
    w("")
    w("## `import_module` calls naming a layer module")
    w("")
    if d["import_module calls"]:
        w("| File:line | Call | Argument |")
        w("|---|---|---|")
        for c in d["import_module calls"]:
            w(f"| `{c['file']}:{c['line']}` | `{c['call']}` | `{c['argument']}` |")
    else:
        w("None.")
    w("")
    w("## Imports of factory modules, by group (count only)")
    w("")
    if d["factory imports by group"]:
        w("| Group | Statements |")
        w("|---|---|")
        for g, c in d["factory imports by group"].items():
            w(f"| `{g}` | {c} |")
        w(f"| **total** | **{t['factory imports']}** |")
    else:
        w("None.")
    if d["moved names"]:
        w("")
        w("## Imports of names that move into the package")
        w("")
        for m, names in d["moved names"].items():
            w(f"`{m}`: " + ", ".join(f"`{n}`" for n in names) + ".")
        w("")
        if d["moved names imports"]:
            w("| File:line | Module | Names |")
            w("|---|---|---|")
            for h in d["moved names imports"]:
                names = ", ".join(f"`{n}`" for n in h["names"])
                w(f"| `{h['file']}:{h['line']}` | `{h['module']}` | {names} |")
        else:
            w("None.")
    w("")
    w("## Files that do not parse")
    w("")
    if d["files that do not parse"]:
        for p in d["files that do not parse"]:
            w(f"- `{p}`")
    else:
        w("None.")
    return "\n".join(out) + "\n"


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("client", choices=sorted(CLIENTS))
    parser.add_argument("--commit", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    measure = Measure(args.client, args.commit)
    try:
        measure.read()
    except CannotRead as e:
        print(f"!! {e}", file=sys.stderr)
        return 2
    data = measure.data()
    if args.json:
        sys.stdout.write(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
    else:
        sys.stdout.write(markdown(data))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
