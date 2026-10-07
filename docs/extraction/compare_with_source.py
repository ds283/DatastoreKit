#!/usr/bin/env python3
"""
The equivalence check of the extraction campaign (prompt 01 §2.5; README §5 rule 8).

For each file the package took from its source repository at the import commit, it reads the
source with ``git show``, reads the package file, and accounts for every line on which they differ.
Run it from the repository root with the venv's interpreter:

    ./venv/bin/python docs/extraction/compare_with_source.py [--show]

How a difference is classified. Each class of prompt 01 §2.4, and the two of prompt 02 §2.6, is a
*rule*: a transformation applied to the source text. The rules are applied in turn (D-imp, D-str,
D-tool, D-root, D-fix for a module; D-split first for the stand-in pool; D-int for an internalised
one), and then ``black`` (D-fmt). What comes out is the text the package file
must be, byte for byte. Every line a rule changes carries that rule's class; a line changed by two
rules carries the first. The package file is then compared with that text, and any line on which
they differ is UNCLASSIFIED. So a rule can only ever explain a change it makes itself, and nothing
is classified by a line number.

- D-imp: in an ``import`` or ``from ... import`` statement (found with ``ast``, at any depth, so
  imports inside functions are included), the module path is mapped by MODULE_MAP. Only the module
  path's tokens are replaced, and only when its image is a module of the package. Relative imports
  are left alone.
- D-str: in a plain (non-f) string literal, a module path is mapped when (i) it is the whole
  literal, (ii) it is itself quoted inside the literal, or (iii) it follows ``import`` or ``from``
  at the start of the literal or after ``"; "``. Its image must be a module of the package, or a
  name bound at the top level of one ((iii): a module only). Prose is never matched: a mention in
  a docstring or comment is not a whole literal, not quoted, and not an import.
- D-tool: in the two tools, the ``_REPO_ROOT`` / ``sys.path`` bootstrap is removed, and a usage line
  or ``prog=`` naming the tool by its file becomes ``python -m datastorekit.tools.<name>``. In the
  three test modules that run a tool, the tool's path constant is replaced, where the command line,
  ``sys.argv[0]`` and ``runpy.run_path`` use it, by ``-m``, the module name and ``runpy.run_module``;
  the constant and ``REPO_ROOT`` go when nothing else uses them.
- D-root: ``test_shard_file_name`` scans the package's own directory for the naming rule.
- D-int: the internalised modules hold only the named definitions of their source and the imports
  those definitions use, in source order with the source's spacing, under a module docstring that
  names the source file and the import commit.
- D-fix (prompt 02 §2.4, §2.6): in the three files the 88 ported tests were re-fixtured in
  (FIX_FILES), inside a plain (non-f) string literal, each whole identifier of FIX_MAP becomes its
  image: a name of the source's own tables becomes the neutral test client's. Nowhere else: not
  in a comment, a name or an f-string, and in no other file.
- D-split (prompt 02 §2.3): the stand-in pool (kind SPLIT) is the source's generic half. Applied
  first, before D-imp: the source is cut at the banner of its client half (SPLIT_BANNER), to the
  end of the file; and in the two methods SPLIT_METHODS only, the two imports of the source's
  registry become one import of the neutral client's registry (SPLIT_IMPORTS), and the getter's
  name becomes the neutral registry's (SPLIT_RENAME). The blank lines the cut leaves at the end are
  removed by ``black``, so they are D-fmt.
- D-fmt: ``black`` (25.1.0, with no configuration) on the result.

**A ported file is not compared here** (prompt 03a §2.4). A test module re-fixtured onto the neutral
test client (kind PORTED) cannot equal its source line by line: its fixture calls, table names and
expected values change by the classes of prompt 03a §2.1. It is checked by
``compare_ported_tests.py`` instead, which compares its test names and each function's assertion
skeleton with the source's. Here a PORTED entry of FILES requires only that the source exists at the
import commit and the package file exists; its lines are not compared, and no class above applies to
it. Each is reported as "ported: checked by compare_ported_tests.py", and the summary counts them.

**An unaccounted file fails** (prompt 02 §2.6). Every ``.py`` file under ``datastorekit/`` (outside
``__pycache__``) is either in FILES (compared, or PORTED) or declared to have no source (NO_SOURCE).
Any other is reported as NOT ACCOUNTED FOR, and so is a declared file that is missing; either makes
the check fail.

The script exits 0 when every differing line is classified, every file exists on both sides and
every package file is accounted for; 1 otherwise; and 2 when it cannot run (wrong ``black``, or
``git show`` fails). It writes nothing.
"""

import argparse
import ast
import difflib
import io
import re
import subprocess
import sys
import tokenize
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SOURCE_REPO = Path("/Users/ds283/Documents/Code/SecondaryGWKit")
IMPORT_COMMIT = "6f7f291"
BLACK_VERSION = "25.1.0"

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = REPO_ROOT / "datastorekit"

# (source path at the import commit, package path, kind)
MODULE = "module"
INTERNALISED = "internalised"
SPLIT = "split"
PORTED = "ported"
FILES: List[Tuple[str, str, str]] = (
    [
        ("Datastore/__init__.py", "datastorekit/__init__.py", MODULE),
        ("Datastore/object.py", "datastorekit/object.py", MODULE),
        ("Datastore/contract.py", "datastorekit/contract.py", MODULE),
        ("Datastore/replication.py", "datastorekit/replication.py", MODULE),
        ("Datastore/shard_paths.py", "datastorekit/shard_paths.py", MODULE),
        ("Datastore/store_reader.py", "datastorekit/store_reader.py", MODULE),
        ("Datastore/store_inventory.py", "datastorekit/store_inventory.py", MODULE),
        ("Datastore/SQL/__init__.py", "datastorekit/SQL/__init__.py", MODULE),
        ("Datastore/SQL/schema.py", "datastorekit/SQL/schema.py", MODULE),
        ("Datastore/SQL/ShardedPool.py", "datastorekit/SQL/ShardedPool.py", MODULE),
        ("Datastore/SQL/Datastore.py", "datastorekit/SQL/Datastore.py", MODULE),
        ("Datastore/SQL/ClientPool.py", "datastorekit/SQL/ClientPool.py", MODULE),
        (
            "Datastore/SQL/SerialPoolBroker.py",
            "datastorekit/SQL/SerialPoolBroker.py",
            MODULE,
        ),
        ("Datastore/SQL/ProfileAgent.py", "datastorekit/SQL/ProfileAgent.py", MODULE),
        (
            "Datastore/SQL/ObjectFactories/base.py",
            "datastorekit/SQL/factory_base.py",
            MODULE,
        ),
        ("tools/__init__.py", "datastorekit/tools/__init__.py", MODULE),
        ("tools/sharded_store.py", "datastorekit/tools/sharded_store.py", MODULE),
        ("tools/shard_key_audit.py", "datastorekit/tools/shard_key_audit.py", MODULE),
        ("config/defaults.py", "datastorekit/defaults.py", INTERNALISED),
        ("utilities.py", "datastorekit/_timing.py", INTERNALISED),
        ("Datastore/tests/__init__.py", "datastorekit/tests/__init__.py", MODULE),
        (
            "Datastore/tests/shard_store_fixtures.py",
            "datastorekit/tests/shard_store_fixtures.py",
            MODULE,
        ),
    ]
    + [
        (f"Datastore/tests/{name}.py", f"datastorekit/tests/{name}.py", MODULE)
        for name in (
            "test_shard_paths",
            "test_shard_file_name",
            "test_shardedpool_shard_paths",
            "test_copy_move_store",
            "test_delete_store",
            "test_sharded_store_script",
            "test_shard_key_audit_copy",
            "test_shard_key_audit_refusals",
        )
    ]
    + [
        (
            "Datastore/tests/standin_pool.py",
            "datastorekit/tests/standin_pool.py",
            SPLIT,
        ),
    ]
    # prompt 03a: re-fixtured onto the neutral client, checked by compare_ported_tests.py
    + [
        (f"Datastore/tests/{name}.py", f"datastorekit/tests/{name}.py", PORTED)
        for name in (
            "test_replicated_write",
            "test_reconcile_at_open",
            "test_prune_at_open",
        )
    ]
)

# Files in the package that have no source, and are not compared: the import guard (prompt 01),
# the neutral test client and its tests (prompt 02), and the shard-key assignment's test (prompt
# 03a). Every other file under datastorekit/ is in FILES, or the check fails.
NO_SOURCE = {
    "datastorekit/tests/test_package_imports.py",
    "datastorekit/tests/client/__init__.py",
    "datastorekit/tests/client/objects.py",
    "datastorekit/tests/client/factories.py",
    "datastorekit/tests/client/registry.py",
    "datastorekit/tests/client/build.py",
    "datastorekit/tests/test_neutral_client.py",
    "datastorekit/tests/test_shard_key_assignment.py",
}

# D-int: what each internalised module takes from its source.
INTERNALISED_NAMES: Dict[str, List[str]] = {
    "datastorekit/defaults.py": ["DEFAULT_STRING_LENGTH"],
    "datastorekit/_timing.py": [
        "WallclockTimer",
        "SECONDS_PER_MINUTE",
        "SECONDS_PER_HOUR",
        "SECONDS_PER_DAY",
        "format_time",
    ],
}

# D-tool: the tools, and the test modules that run them.
TOOL_FILES = {
    "datastorekit/tools/sharded_store.py",
    "datastorekit/tools/shard_key_audit.py",
}
TOOL_TEST_FILES = {
    "datastorekit/tests/test_sharded_store_script.py",
    "datastorekit/tests/test_shard_key_audit_copy.py",
    "datastorekit/tests/test_shard_key_audit_refusals.py",
}

# D-root: (old, new) substitutions, each of which must apply exactly once. Applied after D-imp.
ROOT_RULES: Dict[str, List[Tuple[str, str]]] = {
    "datastorekit/tests/test_shard_file_name.py": [
        (
            "from datastorekit.shard_paths import shard_file_name\n",
            "import datastorekit\nfrom datastorekit.shard_paths import shard_file_name\n",
        ),
        (
            "REPO_ROOT = Path(__file__).resolve().parents[2]\n",
            "PACKAGE_DIR = Path(datastorekit.__file__).resolve().parent\n",
        ),
        (
            "        for path in sorted(\n"
            '            list((REPO_ROOT / "Datastore").rglob("*.py"))\n'
            '            + list((REPO_ROOT / "tools").rglob("*.py"))\n'
            "        ):\n",
            '        for path in sorted(PACKAGE_DIR.rglob("*.py")):\n',
        ),
        (
            "path.relative_to(REPO_ROOT).parts",
            "path.relative_to(PACKAGE_DIR).parts",
        ),
        (
            'f"{path.relative_to(REPO_ROOT)}:{n}"',
            'f"{path.relative_to(PACKAGE_DIR.parent)}:{n}"',
        ),
        ('["Datastore/shard_paths.py"]', '["datastorekit/shard_paths.py"]'),
    ],
}

# D-fix: the files re-fixtured onto the neutral client's names, and the map, applied to whole
# identifiers inside plain string literals only (prompt 02 §2.4)
FIX_FILES = {
    "datastorekit/tests/shard_store_fixtures.py",
    "datastorekit/tests/test_shard_key_audit_copy.py",
    "datastorekit/tests/test_shard_key_audit_refusals.py",
}
FIX_MAP = {
    "wavenumber": "keypoint",
    "wavenumber_serial": "keypoint_serial",
    "GkSource": "Sample",
}

# D-split: the stand-in pool's source is cut at this banner, to the end; and in these two methods
# only, the source registry's imports become the neutral registry's, and the getter is renamed
SPLIT_BANNER = (
    "# " + "-" * 96 + "\n"
    "# objects for the two stored replicated classes, and one sharded class\n"
)
SPLIT_METHODS = ("open_pool", "open_pool_output")
SPLIT_IMPORTS = (
    "        from config.datastore import factories\n"
    "        from config.sharding import (\n"
    "            replicated_tables,\n"
    "            sharded_tables,\n"
    "            shard_key_type,\n"
    "            shard_key_wavenumber_store_id,\n"
    "        )\n",
    "        from datastorekit.tests.client.registry import (\n"
    "            factories,\n"
    "            replicated_tables,\n"
    "            sharded_tables,\n"
    "            shard_key_type,\n"
    "            shard_key_store_id,\n"
    "        )\n",
)
SPLIT_RENAME = ("shard_key_wavenumber_store_id", "shard_key_store_id")

D_IMP, D_STR, D_TOOL, D_ROOT, D_FIX, D_SPLIT, D_INT, D_FMT = (
    "D-imp",
    "D-str",
    "D-tool",
    "D-root",
    "D-fix",
    "D-split",
    "D-int",
    "D-fmt",
)
UNCLASSIFIED = "UNCLASSIFIED"
CLASSES = [D_IMP, D_STR, D_TOOL, D_ROOT, D_FIX, D_SPLIT, D_INT, D_FMT, UNCLASSIFIED]


class CannotRun(Exception):
    pass


# --------------------------------------------------------------------------------------------
# The module map, and what exists in the package


def map_module(name: str) -> Optional[str]:
    """The image of a source module path under prompt 01 §2.4's map, or None if it is unmapped."""
    if name == "Datastore.SQL.ObjectFactories.base":
        return "datastorekit.SQL.factory_base"
    if name.startswith("Datastore."):
        return "datastorekit." + name[len("Datastore.") :]
    if name == "config.defaults":
        return "datastorekit.defaults"
    if name == "utilities":
        return "datastorekit._timing"
    return None


def module_file(dotted: str) -> Optional[Path]:
    """The package file of a module ``datastorekit.<...>``, or None if there is none."""
    parts = dotted.split(".")
    if parts[0] != "datastorekit":
        return None
    base = REPO_ROOT.joinpath(*parts)
    for candidate in (base.with_suffix(".py"), base / "__init__.py"):
        if candidate.is_file():
            return candidate
    return None


def top_level_names(path: Path) -> set:
    names = set()
    for node in ast.parse(path.read_text()).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                names.add(alias.asname or alias.name.split(".")[0])
    return names


def resolves(dotted: str, module_only: bool) -> bool:
    """True if ``dotted`` is a module of the package, or (unless ``module_only``) a name bound at
    the top level of one."""
    if module_file(dotted) is not None:
        return True
    if module_only or "." not in dotted:
        return False
    owner, attribute = dotted.rsplit(".", 1)
    path = module_file(owner)
    return path is not None and attribute in top_level_names(path)


# --------------------------------------------------------------------------------------------
# Text edits


def line_offsets(text: str) -> List[int]:
    offsets = [0]
    for line in text.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))
    return offsets


def apply_edits(text: str, edits: List[Tuple[int, int, str]]) -> str:
    for start, end, new in sorted(edits, reverse=True):
        text = text[:start] + new + text[end:]
    return text


def tokens(text: str) -> List[tokenize.TokenInfo]:
    return list(tokenize.generate_tokens(io.StringIO(text).readline))


# --------------------------------------------------------------------------------------------
# The rules


def dotted_names(toks, i) -> List[List[tokenize.TokenInfo]]:
    """The dotted names of the import statement whose keyword is ``toks[i]``, as token runs: the
    module of a ``from``, or each imported module of an ``import``. Aliases are skipped.
    """
    runs, run, k = [], [], i + 1
    after_as = False
    while toks[k].type not in (tokenize.NEWLINE, tokenize.ENDMARKER):
        tok = toks[k]
        if tok.type == tokenize.NAME and tok.string in ("import", "as"):
            if run:
                runs.append(run)
                run = []
            if toks[i].string == "from":
                break
            after_as = tok.string == "as"
        elif tok.type == tokenize.NAME and not after_as:
            run.append(tok)
        elif tok.type == tokenize.OP and tok.string == "." and run:
            run.append(tok)
        elif tok.type == tokenize.OP and tok.string == ",":
            if run:
                runs.append(run)
            run, after_as = [], False
        elif tok.type == tokenize.NAME and after_as:
            after_as = False
        k += 1
    if run:
        runs.append(run)
    return runs


def rule_imp(text: str, package_path: str) -> str:
    """D-imp: map the module path of every absolute import statement, at any depth."""
    offsets = line_offsets(text)
    toks = tokens(text)
    index = {tok.start: n for n, tok in enumerate(toks)}
    edits = []
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, ast.ImportFrom) and node.level == 0:
            wanted = {node.module}
        elif isinstance(node, ast.Import):
            wanted = {alias.name for alias in node.names}
        else:
            continue
        i = index[(node.lineno, node.col_offset)]
        for run in dotted_names(toks, i):
            name = "".join(t.string for t in run)
            image = map_module(name)
            if name not in wanted or image is None:
                continue
            if not resolves(image, module_only=True):
                continue
            start = offsets[run[0].start[0] - 1] + run[0].start[1]
            end = offsets[run[-1].end[0] - 1] + run[-1].end[1]
            if text[start:end] == name:
                edits.append((start, end, image))
    return apply_edits(text, edits)


DOTTED = r"(?:Datastore|config)(?:\.[A-Za-z_]\w*)+"
WHOLE = re.compile(rf"{DOTTED}")
QUOTED = re.compile(rf"(['\"])({DOTTED})\1")
IMPORTED = re.compile(rf"(?:^|(?<=; ))(?:import|from) ({DOTTED})(?=;|\s|$)")
STRING_PREFIX = re.compile(r"^([rRuU]*)('''|\"\"\"|'|\")")


def rule_str(text: str, package_path: str) -> str:
    """D-str: map a module path in a plain string literal, when it is the whole literal, quoted
    inside the literal, or the module of an import at the literal's start or after "; ".
    """
    offsets = line_offsets(text)
    edits = []
    for tok in tokens(text):
        if tok.type != tokenize.STRING:
            continue
        prefix = STRING_PREFIX.match(tok.string)
        if prefix is None:  # bytes or other literals
            continue
        quote = prefix.group(2)
        body_start = len(prefix.group(0))
        body = tok.string[body_start : len(tok.string) - len(quote)]
        base = offsets[tok.start[0] - 1] + tok.start[1] + body_start
        found = []  # (start, end, name, module_only) within body
        if WHOLE.fullmatch(body):
            found.append((0, len(body), body, False))
        else:
            for m in QUOTED.finditer(body):
                found.append((m.start(2), m.end(2), m.group(2), False))
            for m in IMPORTED.finditer(body):
                found.append((m.start(1), m.end(1), m.group(1), True))
        for start, end, name, module_only in found:
            image = map_module(name)
            if image is not None and resolves(image, module_only):
                edits.append((base + start, base + end, image))
    return apply_edits(text, edits)


BOOTSTRAP = re.compile(
    r"^_REPO_ROOT = str\(Path\(__file__\)\.resolve\(\)\.parents\[1\]\)\n"
    r"if _REPO_ROOT not in sys\.path:\n"
    r"    sys\.path\.insert\(0, _REPO_ROOT\)\n\n",
    re.M,
)
TOOL_CONSTANT = re.compile(
    r'^(SCRIPT|TOOL) = REPO_ROOT / "tools" / "([a-z_]+)\.py"\n', re.M
)
TEST_REPO_ROOT = re.compile(
    r"^REPO_ROOT = Path\(__file__\)\.resolve\(\)\.parents\[2\]\n", re.M
)


def rule_tool(text: str, package_path: str) -> str:
    """D-tool: run the tools as modules of the installed package."""
    if package_path in TOOL_FILES:
        name = Path(package_path).stem
        text, n = BOOTSTRAP.subn("", text)
        if n != 1:
            return text  # nothing else is changed; the difference shows as unclassified
        text = re.sub(
            rf"^(\s+)python tools/{name}\.py\b",
            rf"\1python -m datastorekit.tools.{name}",
            text,
            flags=re.M,
        )
        text = text.replace(
            f'prog="{name}.py"', f'prog="python -m datastorekit.tools.{name}"'
        )
        return text
    if package_path in TOOL_TEST_FILES:
        m = TOOL_CONSTANT.search(text)
        if m is None:
            return text
        constant, name = m.group(1), m.group(2)
        module = f"datastorekit.tools.{name}"
        text = text.replace(
            f"[sys.executable, str({constant}), ",
            f'[sys.executable, "-m", "{module}", ',
        )
        text = text.replace(
            f"sys.argv = [{{str({constant})!r}}, ", f"sys.argv = ['{module}', "
        )
        text = text.replace(
            f"runpy.run_path({{str({constant})!r}}, ",
            f"runpy.run_module('{module}', ",
        )
        without = TEST_REPO_ROOT.sub("", TOOL_CONSTANT.sub("", text, count=1), count=1)
        if not re.search(rf"\b({constant}|REPO_ROOT)\b", without):
            text = without
        return text
    return text


def rule_root(text: str, package_path: str) -> str:
    """D-root: the substitutions of ROOT_RULES, each applied only if it matches exactly once."""
    for old, new in ROOT_RULES.get(package_path, []):
        if text.count(old) == 1:
            text = text.replace(old, new)
    return text


FIXED_NAME = re.compile(
    r"(?<![A-Za-z0-9_])("
    + "|".join(sorted(map(re.escape, FIX_MAP), key=len, reverse=True))
    + r")(?![A-Za-z0-9_])"
)


def rule_fix(text: str, package_path: str) -> str:
    """D-fix: in the files of FIX_FILES only, inside a plain (non-f) string literal, each whole
    identifier of FIX_MAP becomes its image. Comments, names and f-strings are left alone.
    """
    if package_path not in FIX_FILES:
        return text
    offsets = line_offsets(text)
    edits = []
    for tok in tokens(text):
        if tok.type != tokenize.STRING or STRING_PREFIX.match(tok.string) is None:
            continue
        base = offsets[tok.start[0] - 1] + tok.start[1]
        for m in FIXED_NAME.finditer(tok.string):
            edits.append((base + m.start(1), base + m.end(1), FIX_MAP[m.group(1)]))
    return apply_edits(text, edits)


def rule_split(text: str, package_path: str) -> str:
    """D-split: cut the source at SPLIT_BANNER, to the end; then, in each method of
    SPLIT_METHODS only, replace the registry imports and rename the getter. If the banner is not
    found exactly once, a method is not found exactly once, or a method's imports are not found
    exactly once in it, nothing is changed, and the difference shows as unclassified."""
    if text.count(SPLIT_BANNER) != 1:
        return text
    cut = text[: text.index(SPLIT_BANNER)]

    offsets = line_offsets(cut)
    methods = [
        node
        for node in ast.walk(ast.parse(cut))
        if isinstance(node, ast.FunctionDef) and node.name in SPLIT_METHODS
    ]
    if sorted(node.name for node in methods) != sorted(SPLIT_METHODS):
        return text
    old_imports, new_imports = SPLIT_IMPORTS
    old_name, new_name = SPLIT_RENAME
    spans = [(offsets[n.lineno - 1], offsets[n.end_lineno]) for n in methods]
    for start, end in sorted(spans, reverse=True):
        body = cut[start:end]
        if body.count(old_imports) != 1:
            return text
        body = body.replace(old_imports, new_imports)
        body = re.sub(rf"\b{re.escape(old_name)}\b", new_name, body)
        cut = cut[:start] + body + cut[end:]
    return cut


def module_docstring(text: str) -> Optional[str]:
    """The package file's leading docstring, as source text with its newline, if it has one."""
    tree = ast.parse(text)
    if not tree.body:
        return None
    first = tree.body[0]
    if not (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        return None
    lines = text.splitlines(keepends=True)
    return "".join(lines[first.lineno - 1 : first.end_lineno])


def rule_int(text: str, package_path: str, package_text: str, source_path: str) -> str:
    """D-int: the named definitions of the source, and the imports they use, in source order with
    the source's spacing where nothing between them was dropped; under the package file's module
    docstring, which must name the source file and the import commit."""
    keep = set(INTERNALISED_NAMES[package_path])
    tree = ast.parse(text)
    lines = text.splitlines(keepends=True)

    def bound(node) -> set:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            return {node.name}
        if isinstance(node, ast.Assign):
            return {t.id for t in node.targets if isinstance(t, ast.Name)}
        return set()

    chosen = [node for node in tree.body if bound(node) & keep]
    used = set()
    for node in chosen:
        used |= {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
    kept = []
    for node in tree.body:
        if node in chosen:
            kept.append(node)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            if any((a.asname or a.name.split(".")[0]) in used for a in node.names):
                kept.append(node)
    body = ""
    previous = None
    for node in kept:
        if previous is not None:
            gap = lines[previous.end_lineno : node.lineno - 1]
            body += "".join(gap) if all(not g.strip() for g in gap) else ""
        body += "".join(lines[node.lineno - 1 : node.end_lineno])
        previous = node
    docstring = module_docstring(package_text)
    if (
        docstring is None
        or Path(source_path).name not in docstring
        or IMPORT_COMMIT not in docstring
    ):
        return body
    return docstring + "\n" + body


def rule_fmt(text: str, package_path: str) -> str:
    import black

    return black.format_str(text, mode=black.Mode())


# --------------------------------------------------------------------------------------------
# Applying the rules, and following each line


class Tracked:
    """A text, line by line, with the class of each line (None: the source line, unchanged) and
    the source line it is, if it is one."""

    def __init__(self, text: str):
        self.lines = text.splitlines(keepends=True)
        self.labels: List[Optional[str]] = [None] * len(self.lines)
        self.origin: List[Optional[int]] = list(range(1, len(self.lines) + 1))
        self.source_fate: Dict[int, str] = {}  # source line -> class that changed it

    def text(self) -> str:
        return "".join(self.lines)

    def apply(self, cls: str, new_text: str) -> None:
        new_lines = new_text.splitlines(keepends=True)
        matcher = difflib.SequenceMatcher(None, self.lines, new_lines, autojunk=False)
        labels, origin = [], []
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                labels.extend(self.labels[i1:i2])
                origin.extend(self.origin[i1:i2])
                continue
            for i in range(i1, i2):
                if self.origin[i] is not None:
                    self.source_fate.setdefault(self.origin[i], cls)
            earlier = [label for label in self.labels[i1:i2] if label is not None]
            label = earlier[0] if earlier else cls
            labels.extend([label] * (j2 - j1))
            origin.extend([None] * (j2 - j1))
        self.lines, self.labels, self.origin = new_lines, labels, origin


def git_show(path: str) -> Optional[str]:
    result = subprocess.run(
        ["git", "-C", str(SOURCE_REPO), "show", f"{IMPORT_COMMIT}:{path}"],
        capture_output=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.decode("utf-8")


def compare(source_path: str, package_path: str, kind: str, show: bool, out: list):
    """Returns the per-class counts {class: [source lines, package lines]} and the report lines."""
    counts = {cls: [0, 0] for cls in CLASSES}
    source_text = git_show(source_path)
    package_file = REPO_ROOT / package_path
    if source_text is None:
        out.append(f"  MISSING in the source: {source_path} at {IMPORT_COMMIT}")
        counts[UNCLASSIFIED][0] += 1
        return counts
    if not package_file.is_file():
        out.append(f"  MISSING in the package: {package_path}")
        counts[UNCLASSIFIED][1] += 1
        return counts
    package_text = package_file.read_text()

    tracked = Tracked(source_text)
    if kind in (MODULE, SPLIT):
        rules = [
            (D_IMP, rule_imp),
            (D_STR, rule_str),
            (D_TOOL, rule_tool),
            (D_ROOT, rule_root),
            (D_FIX, rule_fix),
        ]
        if kind == SPLIT:
            rules.insert(0, (D_SPLIT, rule_split))
        for cls, rule in rules:
            tracked.apply(cls, rule(tracked.text(), package_path))
    else:
        tracked.apply(
            D_INT, rule_int(tracked.text(), package_path, package_text, source_path)
        )
    tracked.apply(D_FMT, rule_fmt(tracked.text(), package_path))

    # The source lines each class changed or removed.
    for line, cls in tracked.source_fate.items():
        counts[cls][0] += 1

    # The expected text against the package file: what differs is unclassified.
    package_lines = package_text.splitlines(keepends=True)
    matcher = difflib.SequenceMatcher(
        None, tracked.lines, package_lines, autojunk=False
    )
    package_labels: List[Optional[str]] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            package_labels.extend(tracked.labels[i1:i2])
            continue
        for i in range(i1, i2):
            where = (
                f"{source_path}:{tracked.origin[i]}"
                if tracked.origin[i] is not None
                else f"(expected line {i + 1})"
            )
            out.append(
                f"  UNCLASSIFIED  expected, not in the package  {where}: "
                f"{tracked.lines[i].rstrip()}"
            )
            counts[UNCLASSIFIED][0] += 1
        for j in range(j1, j2):
            out.append(
                f"  UNCLASSIFIED  in the package, not expected  {package_path}:{j + 1}: "
                f"{package_lines[j].rstrip()}"
            )
            counts[UNCLASSIFIED][1] += 1
            package_labels.append(UNCLASSIFIED)
    for j, label in enumerate(package_labels):
        if label is not None and label != UNCLASSIFIED:
            counts[label][1] += 1
            if show or label == D_FMT:
                out.append(
                    f"  {label:<12}  {package_path}:{j + 1}: {package_lines[j].rstrip()}"
                )
    for line, cls in sorted(tracked.source_fate.items()):
        if show or cls == D_FMT:
            out.append(
                f"  {cls:<12}  source line removed or changed  {source_path}:{line}: "
                f"{source_text.splitlines()[line - 1]}"
            )
    return counts


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--show", action="store_true", help="list every classified line, not only D-fmt"
    )
    args = parser.parse_args(argv)

    try:
        import black
    except ImportError:
        print("!! black is not installed in this interpreter", file=sys.stderr)
        return 2
    if black.__version__ != BLACK_VERSION:
        print(
            f"!! black {BLACK_VERSION} is required (D-fmt is measured with it); "
            f"this interpreter has {black.__version__}",
            file=sys.stderr,
        )
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
    print(f"package: {PACKAGE_DIR}")
    print(f"black:   {black.__version__}")
    print()
    print(
        "Lines per file and class, as -source/+package: the source lines a class changed or"
    )
    print("removed, and the package lines it accounts for.")
    print()
    compared_files = [f for f in FILES if f[2] != PORTED]
    ported_files = [f for f in FILES if f[2] == PORTED]
    width = max(len(p) for _, p, _ in compared_files)
    print(f"{'file':<{width}}  " + "  ".join(f"{c:>12}" for c in CLASSES))
    totals = {cls: [0, 0] for cls in CLASSES}
    details = []
    for source_path, package_path, kind in compared_files:
        out = []
        counts = compare(source_path, package_path, kind, args.show, out)
        cells = []
        for cls in CLASSES:
            minus, plus = counts[cls]
            totals[cls][0] += minus
            totals[cls][1] += plus
            cells.append(f"{f'-{minus}/+{plus}' if minus or plus else '.':>12}")
        print(f"{package_path:<{width}}  " + "  ".join(cells))
        if out:
            details.append(f"{package_path} (from {source_path}):")
            details.extend(out)
    print(
        f"{'total':<{width}}  "
        + "  ".join(f"{f'-{t[0]}/+{t[1]}':>12}" for t in totals.values())
    )

    # the ported files: the source at the import commit and the package file must both exist
    ported_missing = []
    ported_lines = []
    for source_path, package_path, _ in ported_files:
        if git_show(source_path) is None:
            ported_missing.append(f"{source_path} at {IMPORT_COMMIT}")
            ported_lines.append(
                f"ported (MISSING in the source): {package_path} (from {source_path})"
            )
        elif not (REPO_ROOT / package_path).is_file():
            ported_missing.append(package_path)
            ported_lines.append(
                f"ported (MISSING in the package): {package_path} (from {source_path})"
            )
        else:
            ported_lines.append(
                f"ported: checked by compare_ported_tests.py: {package_path} "
                f"(from {source_path})"
            )

    compared = {p for _, p, _ in FILES}
    present = {
        str(p.relative_to(REPO_ROOT))
        for p in PACKAGE_DIR.rglob("*.py")
        if "__pycache__" not in p.relative_to(REPO_ROOT).parts
    }
    others = sorted(present - compared)
    unaccounted = [other for other in others if other not in NO_SOURCE]
    missing_new = sorted(NO_SOURCE - present)
    print()
    print(f"files compared: {len(compared_files)}")
    print(f"files ported, checked by compare_ported_tests.py: {len(ported_files)}")
    print(f"files with no source, declared: {len(NO_SOURCE)}")
    for line in ported_lines:
        print(line)
    for other in others:
        note = "no source, declared" if other in NO_SOURCE else "NOT ACCOUNTED FOR"
        print(f"not compared ({note}): {other}")
    for missing in missing_new:
        print(f"not compared (MISSING, declared with no source): {missing}")

    if details:
        print()
        print("Lines listed: D-fmt always, UNCLASSIFIED always, the rest with --show.")
        for line in details:
            print(line)

    bad = totals[UNCLASSIFIED][0] + totals[UNCLASSIFIED][1]
    print()
    if bad or unaccounted or missing_new or ported_missing:
        if bad:
            print(f"FAIL: {bad} line(s) unclassified, or a file missing")
        if ported_missing:
            print(
                f"FAIL: {len(ported_missing)} ported file(s) missing: "
                + ", ".join(ported_missing)
            )
        if unaccounted:
            print(
                f"FAIL: {len(unaccounted)} file(s) under datastorekit/ not accounted for"
            )
        if missing_new:
            print(
                f"FAIL: {len(missing_new)} declared file(s) with no source are missing"
            )
        return 1
    print("OK: every differing line is classified, and every file is accounted for")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
