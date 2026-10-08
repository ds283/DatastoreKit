#!/usr/bin/env python3
"""
Measure the three clients' vocabulary for the package's guard (extraction prompt 04b §2.3; README
§6.2, U17).

The guard, ``datastorekit/tests/test_layer_is_generic.py``, forbids the layer to name anything of
a client. What a client's words are is measured here, once, from the clients' own repositories,
and held as data in ``datastorekit/tests/data/client_vocabulary.json``. The guard reads that file
and never a client, so the suite runs with no client present.

Each client is read **only** through ``git show`` and ``git ls-tree`` at a fixed commit. Nothing
of a client is imported, run or opened, and no client's working tree is read. For each client the
file holds:

- the commit, in full;
- the registry's keys: the string keys of the dict literal assigned at module level to the
  registry's name in the registry's module, in the order written;
- the column names: the first argument of each ``Column(...)`` call (``sqla.Column`` or a bare
  ``Column``) whose first argument is a string literal, in every module of
  ``Datastore/SQL/ObjectFactories/`` but ``base.py`` and ``__init__.py``, sorted and unique, with
  the modules read;
- the top-level packages: each top-level directory holding an ``__init__.py``, sorted.

Under SGK it also holds ``extra_names``: the names SGK's prompt 08 removed from its inventory,
taken from the set literal ``EXTRA_NAMES`` of SGK's own guard at the same commit.

The file holds the measurement only. Which of these words the guard forbids (an identifier column,
the layer's own words, the packages that are not a project's) is the guard's rule, applied by the
guard. The ``summary`` counts what was read, before any rule.

Run it from the repository root with the venv's interpreter:

    ./venv/bin/python docs/extraction/measure_client_vocabulary.py [--output PATH]

It writes ``datastorekit/tests/data/client_vocabulary.json``, or ``PATH``, and refuses to
overwrite a file that exists: the committed measurement is never edited. A later re-measure writes
a new file, and the guard is pointed at it. Two runs at the same commits give the same bytes. The
script exits 0 when it wrote the file, 1 when it refused to overwrite one, and 2 when it cannot
read a client.
"""

import argparse
import ast
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

CODE_DIR = Path("/Users/ds283/Documents/Code")
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = (
    REPO_ROOT / "datastorekit" / "tests" / "data" / "client_vocabulary.json"
)

FACTORIES_DIR = "Datastore/SQL/ObjectFactories"
NOT_FACTORIES = {"base.py", "__init__.py"}

# client -> (repository, commit, registry module, registry name)
CLIENTS = {
    "SGK": ("SecondaryGWKit", "6f7f291", "config/datastore.py", "factories"),
    "CPBH": ("ChamPBH", "52142d7", "Datastore/SQL/Datastore.py", "_factories"),
    "SI": (
        "StochasticInstantons",
        "00d254e",
        "Datastore/SQL/Datastore.py",
        "_factories",
    ),
}

# where SGK's prompt 08 names live: its own guard, at the same commit
EXTRA_NAMES_FROM = ("SGK", "Datastore/tests/test_layer_is_generic.py", "EXTRA_NAMES")


class CannotRead(Exception):
    pass


def git(repository: str, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(CODE_DIR / repository), *args], capture_output=True
    )
    if result.returncode != 0:
        raise CannotRead(
            f"git {' '.join(args)} failed in {repository}: "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return result.stdout.decode("utf-8")


def show(repository: str, commit: str, path: str) -> ast.Module:
    text = git(repository, "show", f"{commit}:{path}")
    try:
        return ast.parse(text, filename=f"{repository}:{commit}:{path}")
    except SyntaxError as e:
        raise CannotRead(f"{repository}:{commit}:{path} does not parse: {e}")


def module_assignment(tree: ast.Module, name: str) -> ast.expr:
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == name for t in node.targets
        ):
            return node.value
        if (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == name
            and node.value is not None
        ):
            return node.value
    raise CannotRead(f"no module-level assignment to {name}")


def registry_keys(tree: ast.Module, name: str) -> List[str]:
    value = module_assignment(tree, name)
    if not isinstance(value, ast.Dict):
        raise CannotRead(f"{name} is not a dict literal")
    keys = []
    for key in value.keys:
        if not (isinstance(key, ast.Constant) and isinstance(key.value, str)):
            raise CannotRead(f"{name} has a key that is not a string literal")
        keys.append(key.value)
    return keys


def column_names(tree: ast.Module) -> set:
    found = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        func = node.func
        called = (
            func.id
            if isinstance(func, ast.Name)
            else func.attr if isinstance(func, ast.Attribute) else None
        )
        first = node.args[0]
        if (
            called == "Column"
            and isinstance(first, ast.Constant)
            and isinstance(first.value, str)
        ):
            found.add(first.value)
    return found


def measure(repository: str, commit: str, registry_path: str, registry_name: str):
    full = git(repository, "rev-parse", f"{commit}^{{commit}}").strip()
    keys = registry_keys(show(repository, full, registry_path), registry_name)

    listed = git(repository, "ls-tree", "--name-only", full, f"{FACTORIES_DIR}/")
    modules = sorted(
        path
        for path in listed.splitlines()
        if path.endswith(".py") and Path(path).name not in NOT_FACTORIES
    )
    columns = set()
    for path in modules:
        columns |= column_names(show(repository, full, path))

    every = git(repository, "ls-tree", "-r", "--name-only", full)
    packages = sorted(
        {
            parts[0]
            for parts in (path.split("/") for path in every.splitlines())
            if len(parts) == 2 and parts[1] == "__init__.py"
        }
    )
    return {
        "repository": repository,
        "commit": full,
        "registry": {"module": registry_path, "name": registry_name, "keys": keys},
        "columns": {"modules": modules, "names": sorted(columns)},
        "packages": packages,
    }


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    if args.output.exists():
        print(
            f"!! {args.output} exists; a re-measure writes a new file", file=sys.stderr
        )
        return 1

    clients: Dict[str, dict] = {}
    try:
        for client, (
            repository,
            commit,
            registry_path,
            registry_name,
        ) in CLIENTS.items():
            clients[client] = measure(repository, commit, registry_path, registry_name)
        client, path, name = EXTRA_NAMES_FROM
        repository = clients[client]["repository"]
        value = module_assignment(
            show(repository, clients[client]["commit"], path), name
        )
        clients[client]["extra_names"] = {
            "from": f"{path}, {name}",
            "names": sorted(ast.literal_eval(value)),
        }
    except CannotRead as e:
        print(f"!! {e}", file=sys.stderr)
        return 2

    tables = set().union(*(set(c["registry"]["keys"]) for c in clients.values()))
    columns = set().union(*(set(c["columns"]["names"]) for c in clients.values()))
    packages = set().union(*(set(c["packages"]) for c in clients.values()))
    summary = {
        "read, before any rule of the guard": {
            "registry keys, all clients": len(tables),
            "column names, all clients": len(columns),
            "packages, all clients": len(packages),
        },
        "per client": {
            client: {
                "registry keys": len(c["registry"]["keys"]),
                "factory modules": len(c["columns"]["modules"]),
                "column names": len(c["columns"]["names"]),
                "packages": len(c["packages"]),
            }
            for client, c in clients.items()
        },
    }
    data = {
        "written by": "docs/extraction/measure_client_vocabulary.py",
        "what": "the three clients' vocabulary, read by git show at fixed commits, for the "
        "package's guard (extraction prompt 04b, U17)",
        "clients": clients,
        "summary": summary,
    }
    text = json.dumps(data, indent=2, ensure_ascii=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)

    print(f"wrote {args.output} ({len(text.encode('utf-8'))} bytes)")
    for client, c in clients.items():
        counts = summary["per client"][client]
        print(
            f"  {client}: {c['repository']} at {c['commit']}: "
            f"{counts['registry keys']} registry keys, "
            f"{counts['column names']} column names in {counts['factory modules']} modules, "
            f"{counts['packages']} packages"
        )
    print(f"  SGK extra names: {len(clients['SGK']['extra_names']['names'])}")
    read = summary["read, before any rule of the guard"]
    print(
        f"  all clients: {read['registry keys, all clients']} registry keys, "
        f"{read['column names, all clients']} column names, "
        f"{read['packages, all clients']} packages"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
