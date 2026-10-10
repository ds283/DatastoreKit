#!/usr/bin/env python3
"""
Run the package under real Ray, once, on a store in a temporary directory: a smoke run, not a
test (extraction prompt 11 §2.2, decision U41).

The suite runs the layer's actors through the in-process stand-in pool and never starts Ray. This
script starts a local Ray instance of its own, opens a ``ShardedPool`` on the neutral test client
(``datastorekit.tests.client``) as ``standin_pool.StandinCluster.open_pool`` builds one (the
registry, its ``read_table_config`` and ``serial_batch_sizes``, the label ``"standin"``, three
shards), and runs these steps, each an assertion that prints ``PASS`` or ``FAIL`` with what it saw:

1. a read-write pool is opened, and ``build.write_every_class`` writes every class;
2. a keyed vectorized get (``object_get_vectorized``) of the first alias's two Tesserae finds the
   serials step 1 wrote, and leaves the caller's payload dicts as they were passed;

   the pool is closed, and whether its actors' names are still held is recorded;

N. the names: with the closed pool still referenced, a second read-write open is refused by Ray's
   name collision (``ValueError`` at Ray 2.43, its subclass ``ActorAlreadyExistsError`` at 2.55),
   naming ``SerialPoolBroker``; the names are still held after the refused open's exception is
   dropped, and free once the pool is dropped (``del`` and ``gc.collect()``). This is the
   behaviour of ``[11-a-closed-pool-holds-its-actor-names-until-it-is-collected]``, and the step
   passes when it is as measured;
3. the store is reopened read-write, and the same get finds the same serials;
4. a read-only pool finds the same serials (its lookup serial is given by ``set_lookup_version``);
5. an open with ``Weave`` left out of ``sharded_tables`` is refused with ``RuntimeError``
   "Mismatch between sharded tables supplied to the constructor and read from the existing
   ShardedPool", and the exception is dropped;
6. a read-write open after the refusal works, and the same get finds the same serials.

After each pool's ``__exit__`` the script records whether its names are held, and then drops the
pool before the next open. A step that raises prints ``FAIL`` with the exception's type and the
last line of its message, and the script goes on; a step that needs a failed one is reported as
``NOT RUN``.

**What it starts and touches.** It refuses to run when ``RAY_ADDRESS`` is set, when Ray is already
initialised, or when ``pgrep`` finds a Ray process (a ``gcs_server``, ``raylet``, ``ray::`` or
``default_worker.py`` process, found by ``pgrep -f``; a process whose executable is a ``zsh``,
``bash`` or ``sh`` shell is dropped and printed, since a shell's command line may carry those
words). It starts Ray with ``ray.init(address="local", num_cpus=4, include_dashboard=False,
log_to_driver=False)``, which always starts a new local instance and never connects to a cluster,
and calls ``ray.shutdown()`` in a ``finally``. Ray writes its session directory under its
default, ``/tmp/ray/``; the script prints it, and deletes nothing. Every store is in a
``tempfile.TemporaryDirectory()``. The neutral client's helpers resolve references with the
stand-in's ``standin_get``, so the script patches ``build.resolve`` to ``ray.get`` in its own
process; nothing of the package changes.

**How it is run.** With the package importable from a checkout or an export (an editable install),
since it imports the tests' neutral client, which no wheel carries:

    python docs/extraction/ray_smoke_run.py

**What it prints:** the environment (Python, Ray, SQLAlchemy and SQLite versions, the installed
``datastorekit`` version and where it is imported from), the Ray processes before, the start of
Ray, each step's verdict with what it saw and its time, the Ray processes after ``ray.shutdown()``,
and a summary. It exits 0 only when every step passes and no Ray process is left; 1 otherwise; 2
when it refuses to run.

It is never collected by the suite, which stays free of Ray (``CLAUDE.md``).
"""

import contextlib
import copy
import gc
import importlib.metadata
import io
import os
import platform
import sqlite3
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path
from typing import Dict, List, Optional
from unittest import mock

# the pgrep pattern, and the shells whose command lines it may match
RAY_PATTERN = r"gcs_server|raylet|ray::|default_worker\.py"
SHELLS = ("zsh", "bash", "sh")

# what build.write_every_class writes, class by class
EXPECTED_WRITTEN = {
    "store_tag": 3,
    "keypoint": 3,
    "dial_setting": 2,
    "knob_setting": 1,
    "gauge_setting": 2,
    "routing_rule": 2,
    "ephemeral_probe": 1,
    "keypoint_alias": 3,
    "Gadget": 2,
    "Tessera": 6,
    "Sample": 4,
    "Trace": 2,
    "Weave": 1,
}

SHARDS = 3
BROKER = "SerialPoolBroker"
SHARD_NAMES = [f"shard{key:04d}-store" for key in range(SHARDS)]
MISMATCH = (
    "Mismatch between sharded tables supplied to the constructor and read from the "
    "existing ShardedPool"
)
LEFT_OUT = "Weave"
NOT_SUPPLIED = (
    "sharded tables are configured in the existing ShardedPool, but were not supplied to "
    "the constructor"
)
# how long a dropped pool's names, or a stopped instance's processes, are waited for
WAIT_SECONDS = 30.0


class StepFailed(Exception):
    """An assertion of a step that did not hold."""


def ray_processes() -> Dict[str, List[str]]:
    """
    The processes ``pgrep -f`` finds for Ray's pattern, by pid, split by each one's executable
    (``ps -o comm=``): the shells, dropped, and the rest. A command line may span several lines
    (a shell's ``-c`` script), so a process is classed by its executable, not by a line of
    ``pgrep -l``'s output; each is shown by its pid, executable and first line.
    """
    found = subprocess.run(
        ["pgrep", "-f", RAY_PATTERN], capture_output=True, text=True, check=False
    )
    shells, ray_lines = [], []
    for pid in found.stdout.split():
        comm = subprocess.run(
            ["ps", "-o", "comm=", "-p", pid],
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
        if not comm:
            continue  # gone since pgrep listed it
        command = subprocess.run(
            ["ps", "-o", "command=", "-p", pid],
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
        first = command.splitlines()[0] if command else ""
        line = f"{pid} {comm}: {first[:160]}"
        name = comm.lstrip("-").rsplit("/", 1)[-1]
        (shells if name in SHELLS else ray_lines).append(line)
    return {"shells": shells, "ray": ray_lines}


def print_processes(when: str, procs: Dict[str, List[str]]) -> None:
    print(f"Ray processes {when}: {len(procs['ray'])}")
    for line in procs["ray"]:
        print(f"    ray:     {line}")
    for line in procs["shells"]:
        print(f"    dropped: {line}")


def last_line(exc: BaseException) -> str:
    """The exception's message, by its last non-empty line (a RayTaskError's is its cause's)."""
    lines = [line.strip() for line in str(exc).splitlines() if line.strip()]
    return lines[-1] if lines else ""


def type_name(exc: BaseException) -> str:
    return f"{type(exc).__module__}.{type(exc).__qualname__}"


class Smoke:
    """The run's state: the store, the pool open now, and the steps' verdicts."""

    def __init__(self, ray, build, registry, ShardedPool, directory: Path):
        self.ray = ray
        self.build = build
        self.registry = registry
        self.ShardedPool = ShardedPool
        self.primary = directory / "store.sqlite"
        self.pool = None
        self.pool_names: List[str] = []
        self.last_printed = ""
        self.written: Optional[Dict[str, list]] = None
        self.reference: Optional[List[int]] = None
        self.verdicts: List[tuple] = []

    # ---------------------------------------------------------------------------------------------
    # pools and names
    # ---------------------------------------------------------------------------------------------

    def open_pool(self, read_only: bool = False, sharded_tables=None):
        """A pool as ``StandinCluster.open_pool`` builds it, with what it printed."""
        printed = io.StringIO()
        self.last_printed = ""
        # what a refused constructor printed is kept too (finally)
        with self.keep_printed(printed), contextlib.redirect_stdout(printed):
            pool = self.ShardedPool(
                version_label="standin",
                db_name=self.primary,
                ShardKeyType=self.registry.shard_key_type,
                ShardKeyStoreIdGetter=self.registry.shard_key_store_id,
                replicated_tables=self.registry.replicated_tables,
                sharded_tables=(
                    self.registry.sharded_tables
                    if sharded_tables is None
                    else sharded_tables
                ),
                shards=SHARDS,
                factories=self.registry.factories,
                read_table_config=self.registry.read_table_config,
                serial_batch_sizes=self.registry.serial_batch_sizes,
                read_only=read_only,
            )
        self.pool = pool
        self.pool_names = SHARD_NAMES if read_only else [BROKER] + SHARD_NAMES
        return printed.getvalue()

    @contextlib.contextmanager
    def keep_printed(self, printed: io.StringIO):
        try:
            yield
        finally:
            self.last_printed = printed.getvalue()

    def names_held(self, names: List[str]) -> Dict[str, bool]:
        held = {}
        for name in names:
            try:
                self.ray.get_actor(name)
                held[name] = True
            except ValueError:
                held[name] = False
        return held

    @staticmethod
    def describe(held: Dict[str, bool]) -> str:
        found = [name for name, h in held.items() if h]
        return f"{len(found)} of {len(held)} held" + (
            f" ({', '.join(found)})" if found else ""
        )

    def close_pool(self) -> Dict[str, bool]:
        """The open pool's ``__exit__``; then whether its names are held, the pool referenced."""
        with contextlib.redirect_stdout(io.StringIO()):
            self.pool.__exit__(None, None, None)
        held = self.names_held(self.pool_names)
        print(f"    after __exit__, the pool referenced: {self.describe(held)}")
        return held

    def drop_pool(self) -> tuple:
        """Drop the pool (``del`` and ``gc.collect()``) and wait for its names to be free."""
        names = self.pool_names
        self.pool = None
        gc.collect()
        start = time.monotonic()
        held = self.names_held(names)
        while any(held.values()) and time.monotonic() - start < WAIT_SECONDS:
            time.sleep(0.1)
            held = self.names_held(names)
        waited = time.monotonic() - start
        print(
            f"    after del and gc.collect(): {self.describe(held)}, after {waited:.1f} s"
        )
        return held, waited

    def get_reference_tesserae(self, alias) -> List[int]:
        """
        The keyed vectorized get of step 2, of the alias's two Tesserae: the serials found. It
        fails when the caller's payload dicts are not as they were passed.
        """
        payloads = [{"weight": w} for w in self.build.TESSERA_WEIGHTS]
        before = copy.deepcopy(payloads)
        found = self.ray.get(
            self.pool.object_get_vectorized(
                "Tessera", {"k": alias}, payload_data=payloads
            )
        )
        serials = [t.store_id for t in found]
        added = sorted(
            {key for p in payloads for key in p} - {key for p in before for key in p}
        )
        if payloads != before:
            raise StepFailed(
                f"the caller's payload dicts changed: keys added {added}; "
                f"{len(payloads)} dicts, of which {sum(p != b for p, b in zip(payloads, before))} "
                f"differ from what was passed (serials found {serials})"
            )
        return serials

    def the_alias(self):
        """The first keypoint's alias, got again through the open pool, and checked."""
        point = self.build.get_keypoint(self.pool, self.build.KEYPOINT_POSITIONS[0])
        alias = self.build.get_alias(
            self.pool, point, self.build.ALIAS_OFFSET, self.build.ALIAS_STEPPING
        )
        first = self.written["keypoint_alias"][0]
        if alias.store_id != first.store_id:
            raise StepFailed(
                f"the alias got again has serial {alias.store_id}, not {first.store_id}"
            )
        return alias

    def same_serials(self, alias) -> str:
        serials = self.get_reference_tesserae(alias)
        if serials != self.reference:
            raise StepFailed(f"serials {serials}, not {self.reference}")
        return f"serials {serials}, the caller's dicts unchanged"

    # ---------------------------------------------------------------------------------------------
    # the steps
    # ---------------------------------------------------------------------------------------------

    def step_1(self) -> str:
        self.open_pool()
        self.written = self.build.write_every_class(self.pool)
        counts = {cls: len(objs) for cls, objs in self.written.items()}
        seen = ", ".join(f"{cls} {n}" for cls, n in counts.items())
        if counts != EXPECTED_WRITTEN:
            raise StepFailed(f"wrote {seen}; expected {EXPECTED_WRITTEN}")
        self.reference = [t.store_id for t in self.written["Tessera"][:2]]
        return f"wrote {seen}"

    def step_2(self) -> str:
        try:
            alias = self.written["keypoint_alias"][0]
            serials = self.get_reference_tesserae(alias)
            if serials != self.reference:
                raise StepFailed(f"serials {serials}, not step 1's {self.reference}")
            return f"serials {serials} (step 1's), the caller's dicts unchanged"
        finally:
            self.close_pool()

    def step_names(self) -> str:
        """The closed pool of steps 1 and 2 is still referenced: a second open collides."""
        seen = []
        held = self.names_held(self.pool_names)
        if not all(held.values()):
            raise StepFailed(f"before the second open: {self.describe(held)}")
        seen.append(f"before the second open, {self.describe(held)}")
        # a refused open never reaches open_pool's assignment, so self.pool stays the first pool,
        # and the first pool is referenced there alone
        collision = None
        try:
            self.open_pool()
        except ValueError as exc:
            collision = (type_name(exc), last_line(exc))
        else:
            # the second pool is open, in place of the first: close it and drop it
            self.close_pool()
            self.drop_pool()
            raise StepFailed("the second open was not refused")
        gc.collect()
        kind, message = collision
        print(f"    the second open raised {kind}: {message}")
        if "is already taken" not in message or BROKER not in message:
            raise StepFailed(f"{kind}: {message}")
        seen.append(f"the second open raised {kind} naming {BROKER}")
        held = self.names_held(self.pool_names)
        print(
            f"    after the exception is dropped, the pool referenced: {self.describe(held)}"
        )
        if not all(held.values()):
            raise StepFailed(f"after the refused open: {self.describe(held)}")
        seen.append(f"after the exception was dropped, {self.describe(held)}")
        held, waited = self.drop_pool()
        if any(held.values()):
            raise StepFailed(f"after del and gc.collect(): {self.describe(held)}")
        seen.append(f"after del and gc.collect(), none held ({waited:.1f} s)")
        return "; ".join(seen)

    def reopen_and_get(self, read_only: bool) -> str:
        held = self.names_held([BROKER] + SHARD_NAMES)
        if any(held.values()):
            raise StepFailed(f"before the open: {self.describe(held)}")
        self.open_pool(read_only=read_only)
        try:
            return self.same_serials(self.the_alias())
        finally:
            self.close_pool()
            self.drop_pool()

    def step_3(self) -> str:
        return self.reopen_and_get(read_only=False)

    def step_4(self) -> str:
        return "read-only: " + self.reopen_and_get(read_only=True)

    def step_5(self) -> str:
        wanting = {
            cls: field
            for cls, field in self.registry.sharded_tables.items()
            if cls != LEFT_OUT
        }
        refusal = None
        try:
            self.open_pool(sharded_tables=wanting)
        except RuntimeError as exc:
            refusal = (type(exc) is RuntimeError, type_name(exc), last_line(exc))
        else:
            self.close_pool()
            self.drop_pool()
            raise StepFailed(f"the open with {LEFT_OUT} left out was not refused")
        finally:
            self.pool = None
            gc.collect()
        exact, kind, message = refusal
        lines = self.last_printed.splitlines()
        heading = [i for i, line in enumerate(lines) if NOT_SUPPLIED in line]
        listed = [line.strip() for line in lines[heading[0] + 1 :]] if heading else []
        print(f"    the constructor printed, as not supplied: {listed[:1]}")
        if not exact or MISMATCH not in message:
            raise StepFailed(f"{kind}: {message}")
        held = self.names_held([BROKER] + SHARD_NAMES)
        print(f"    after the exception is dropped: {self.describe(held)}")
        if any(held.values()):
            raise StepFailed(f"after the refusal: {self.describe(held)}")
        return f"{kind}: {message}; {self.describe(held)}"

    def step_6(self) -> str:
        return "read-write open after the refusal: " + self.reopen_and_get(
            read_only=False
        )

    # ---------------------------------------------------------------------------------------------
    # the run
    # ---------------------------------------------------------------------------------------------

    STEPS = [
        ("1", "write every class (read-write)", "step_1", []),
        ("2", "keyed vectorized get, the caller's dicts", "step_2", ["1"]),
        ("N", "a closed pool holds its names (prompt 11 §1.3)", "step_names", ["1"]),
        ("3", "reopen read-write, the same get", "step_3", ["1", "N"]),
        ("4", "read-only pool, the same get", "step_4", ["1", "N"]),
        ("5", f"refused open, {LEFT_OUT} left out", "step_5", ["1", "N"]),
        ("6", "read-write open after the refusal", "step_6", ["1", "N"]),
    ]

    def run(self) -> bool:
        passed: Dict[str, bool] = {}
        for label, title, method, needs in self.STEPS:
            failed_needs = [n for n in needs if not passed.get(n, False)]
            if failed_needs:
                passed[label] = False
                self.verdicts.append((label, "NOT RUN"))
                print(
                    f"NOT RUN  step {label}: {title}: needs step {', '.join(failed_needs)}"
                )
                continue
            start = time.monotonic()
            print(f"step {label}: {title}")
            # every step's failure is reported, and the run goes on
            try:
                seen = getattr(self, method)()
                verdict = "PASS"
            except Exception as exc:
                seen = f"{type_name(exc)}: {last_line(exc)}"
                verdict = "FAIL"
                if not isinstance(exc, StepFailed):
                    traceback.print_exc(limit=3, file=sys.stdout)
            elapsed = time.monotonic() - start
            passed[label] = verdict == "PASS"
            self.verdicts.append((label, verdict))
            print(f"{verdict}  step {label} ({elapsed:.1f} s): {seen}")
        return all(passed.values())

    def close_whatever_is_open(self) -> None:
        if self.pool is None:
            return
        with contextlib.suppress(Exception):
            with contextlib.redirect_stdout(io.StringIO()):
                self.pool.__exit__(None, None, None)
        self.pool = None
        gc.collect()


def main(argv: List[str]) -> int:
    started = time.monotonic()
    import ray
    import sqlalchemy

    import datastorekit
    from datastorekit.SQL.ShardedPool import ShardedPool
    from datastorekit.tests.client import build, registry

    print("Environment:")
    print(f"    Python       {platform.python_version()} ({sys.executable})")
    print(f"    Ray          {ray.__version__}")
    print(f"    SQLAlchemy   {sqlalchemy.__version__}")
    print(f"    SQLite       {sqlite3.sqlite_version}")
    print(f"    datastorekit {importlib.metadata.version('datastorekit')}")
    print(f"    imported from {datastorekit.__file__}")

    if os.environ.get("RAY_ADDRESS"):
        print(f"REFUSED: RAY_ADDRESS is set ({os.environ['RAY_ADDRESS']!r})")
        return 2
    if ray.is_initialized():
        print("REFUSED: Ray is already initialised in this process")
        return 2
    before = ray_processes()
    print_processes("before", before)
    if before["ray"]:
        print("REFUSED: a Ray process is up")
        return 2

    ok = False
    t0 = time.monotonic()
    context = ray.init(
        address="local", num_cpus=4, include_dashboard=False, log_to_driver=False
    )
    try:
        node, session = None, None
        with contextlib.suppress(Exception):
            node = context.address_info.get("node_ip_address")
            session = context.address_info.get("session_dir")
        print(
            f"Ray started in {time.monotonic() - t0:.1f} s, at {node}; "
            f"session directory {session}"
        )
        with tempfile.TemporaryDirectory() as directory:
            smoke = Smoke(ray, build, registry, ShardedPool, Path(directory))
            try:
                with mock.patch.object(build, "resolve", ray.get):
                    ok = smoke.run()
            finally:
                smoke.close_whatever_is_open()
                del smoke
                gc.collect()
    finally:
        ray.shutdown()

    start = time.monotonic()
    after = ray_processes()
    while after["ray"] and time.monotonic() - start < WAIT_SECONDS:
        time.sleep(0.5)
        after = ray_processes()
    print(f"ray.shutdown(); waited {time.monotonic() - start:.1f} s for its processes")
    print_processes("after", after)

    print(
        f"Summary: {'every step passed' if ok else 'a step did not pass'}; "
        f"{len(after['ray'])} Ray process(es) left; {time.monotonic() - started:.1f} s in all"
    )
    return 0 if ok and not after["ray"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
