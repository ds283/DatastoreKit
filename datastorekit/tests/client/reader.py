"""
The neutral store, reader sequence and instrument that ``test_read_only_pool`` runs (prompt 03b;
README §6.2, U11). The source repository's test imported an audit probe for its store and for one
of its readers' lookup sequences; this module stands in for that probe on the neutral client, and
the test imports it as ``rw``, so that its calls keep their shape.

- **The instrument**, transcribed from the probe with its behaviour unchanged: ``change_counter``,
  ``table_counts``, ``file_state`` and ``state_delta`` read a store's files (as bytes, or through
  ``standin_pool._read``, which opens them ``mode=ro``); ``ReplicatedWriteLog`` wraps
  ``ShardedPool._replicated_write`` for the length of a ``with`` block; ``Step`` and ``Recorder``
  record, for each step of a sequence, the files it changed, the replicated writes it made and its
  outcome.
- **The store.** ``build_full_store`` writes ``build.write_every_class``'s store, then, through the
  pool, what the sequence asks for that it lacks: the two gauges of the work items, and one
  validated Sample tagged with the run's tag. It returns the store's facts, keyed by class.
- **The sequence.** ``reader_sequence`` is a reader's lookups, in order: the run's tag; the two
  frames, ``dial_setting`` then ``knob_setting``; then, for each frame, four gauges, the frame's
  validated ``Gadget`` (or the sequence's own ``RuntimeError`` when there is none), ``read_table``
  of ``keypoint`` twice, those keypoints' aliases, ``read_table`` of ``dial_setting``, the two
  rules, and one work item's sharded lookups. On the full store the second frame has no validated
  Gadget, so the sequence stops there. Every replicated lookup is a hit on the full store, and every
  sharded one is a hit or a miss that inserts nothing, so a read-write run inserts nothing.
- ``other_sharded_lookups``: three sharded lookups that miss and insert nothing.

Nothing here asserts: the test makes every assertion. Everything this module passes to an actor is
defined at module level (in ``objects``), since the stand-in pool pickles it, as Ray would. Like
``build``, it resolves the pool's references with the stand-in pool's own ``ray.get``
(``build.resolve``), and imports no ``ray``.
"""

import contextlib
import hashlib
import io
from pathlib import Path
from typing import Dict, List


from datastorekit.tests import standin_pool as sp
from datastorekit.tests.client import build
from datastorekit.tests.client.objects import SerialHandle

# the run whose tag the sequence resolves, and the label of a run's tag
RUN = "north"


def run_label_tag(run: str) -> str:
    """The label of run ``run``'s ``store_tag``."""
    return f"tag-{run}"


# the frames the sequence gets, in its order, and the label of the Gadget it asks for on each:
# build_store's validated Gadget is on the dial frame, its unvalidated one on the knob frame
DIAL_FRAME = build.DIAL_LEVELS[0]  # (level, stepping)
KNOB_FRAME = build.KNOB_TURNS  # (turns, stepping)
FRAMES = (("dial", "gadget-one"), ("knob", "gadget-two"))

# the four gauges the sequence gets on each frame, in its order: two for the alias step (each a
# gauge build_store writes), then two for the work items, which build_full_store writes
ALIAS_GAUGES = build.GAUGE_EXPONENTS
WORK_GAUGES = (10, 12)
SEQUENCE_GAUGES = ALIAS_GAUGES + WORK_GAUGES
# the gauge a test gets, deletes or makes differ: the sequence's last
DEFAULT_GAUGE = WORK_GAUGES[1]

# the two rules the sequence gets on each frame, in its order: build_store's two
RULE_LOW, RULE_HIGH = (
    dict(label=label, threshold=threshold, mode=mode)
    for label, threshold, mode in build.ROUTING_RULES
)

# the Sample build_full_store stores for the run, and a code no Sample has
RUN_SAMPLE_CODE = "sample-run"
MISSED_SAMPLE_CODE = "sample-elsewhere"


# ------------------------------------------------------------------------------------------------
# the instrument (transcribed from the probe)
# ------------------------------------------------------------------------------------------------


def change_counter(path: Path) -> int:
    with open(path, "rb") as f:
        header = f.read(28)
    return int.from_bytes(header[24:28], "big")


def table_counts(path: Path) -> Dict[str, int]:
    names = [
        r[0]
        for r in sp._read(
            path, "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
    ]
    return {n: sp._read(path, f'SELECT count(*) FROM "{n}"')[0][0] for n in names}


def file_state(directory: Path) -> Dict[str, dict]:
    out = {}
    for p in sorted(directory.iterdir()):
        if not p.is_file():
            continue
        entry = {"sha": hashlib.sha256(p.read_bytes()).hexdigest()[:12]}
        if p.suffix == ".sqlite":
            entry["counter"] = change_counter(p)
            entry["rows"] = table_counts(p)
        out[p.name] = entry
    return out


def state_delta(before: Dict[str, dict], after: Dict[str, dict]) -> Dict[str, dict]:
    """Per file: change-counter delta, rows inserted (+) or deleted (-) per table, files that
    appeared or went."""
    delta = {}
    for name in sorted(set(before) | set(after)):
        if name not in before:
            delta[name] = {"appeared": True}
            continue
        if name not in after:
            delta[name] = {"went": True}
            continue
        b, a = before[name], after[name]
        d = {}
        if "counter" in b:
            d["commits"] = a["counter"] - b["counter"]
            rows = {}
            for t in sorted(set(b["rows"]) | set(a["rows"])):
                n = a["rows"].get(t, 0) - b["rows"].get(t, 0)
                if n != 0:
                    rows[t] = n
            if rows:
                d["rows"] = rows
            new_tables = sorted(set(a["rows"]) - set(b["rows"]))
            if new_tables:
                d["new_tables"] = new_tables
        if a["sha"] != b["sha"]:
            d["changed"] = True
        if d.get("commits") or d.get("rows") or d.get("changed") or d.get("new_tables"):
            delta[name] = d
    return delta


class ReplicatedWriteLog:
    """Wraps ``ShardedPool._replicated_write`` for the duration of a ``with`` block."""

    def __init__(self):
        self.entries: List[dict] = []

    @contextlib.contextmanager
    def active(self):
        original = sp.sp_mod.ShardedPool._replicated_write
        log = self

        def wrapped(pool, operation, cls_name, submit_controller, replication, **kw):
            ref, answer = original(
                pool, operation, cls_name, submit_controller, replication, **kw
            )
            answers = answer if isinstance(answer, list) else [answer]
            log.entries.append(
                {
                    "operation": operation,
                    "class": cls_name,
                    "inserted": sum(
                        1
                        for a in answers
                        if hasattr(a, "_new_insert") or hasattr(a, "_updated")
                    ),
                    "serials": [
                        getattr(a, "store_id", None)
                        for a in answers
                        if hasattr(a, "_new_insert") or hasattr(a, "_updated")
                    ],
                }
            )
            return ref, answer

        sp.sp_mod.ShardedPool._replicated_write = wrapped
        try:
            yield self
        finally:
            sp.sp_mod.ShardedPool._replicated_write = original

    def since(self, n: int) -> List[dict]:
        return self.entries[n:]


class Step:
    """Records one step: file deltas, replicated writes, and any exception."""

    def __init__(self, recorder: "Recorder", name: str):
        self.recorder = recorder
        self.name = name

    def __enter__(self):
        self.detail = None
        self.before = file_state(self.recorder.directory)
        self.n = len(self.recorder.log.entries)
        return self

    def __exit__(self, exc_type, exc, tb):
        after = file_state(self.recorder.directory)
        delta = state_delta(self.before, after)
        writes = self.recorder.log.since(self.n)
        outcome = "ok" if exc is None else f"raised {exc_type.__name__}: {exc}"
        if self.detail is not None:
            outcome += f" [{self.detail}]"
        self.recorder.rows.append((self.name, delta, writes, outcome))
        return False


class Recorder:
    def __init__(self, directory: Path, log: ReplicatedWriteLog):
        self.directory = directory
        self.log = log
        self.rows = []

    def step(self, name: str) -> Step:
        return Step(self, name)


# ------------------------------------------------------------------------------------------------
# the store
# ------------------------------------------------------------------------------------------------


@contextlib.contextmanager
def quiet():
    with contextlib.redirect_stdout(io.StringIO()):
        yield


def build_full_store(primary: Path, cluster: sp.StandinCluster) -> dict:
    """Write every row the reader sequence asks for, through the pool, and close the store."""
    pool = build.open_pool(cluster, primary)
    with quiet():
        written = build.write_every_class(pool)
        run_tag = build.resolve(pool.object_get("store_tag", label=run_label_tag(RUN)))
        gauges = {g.exponent: g for g in written["gauge_setting"]}
        gauges.update({e: build.get_gauge(pool, e) for e in WORK_GAUGES})
        gadgets = {g.label: g for g in written["Gadget"]}
        rules = {r.label: r for r in written["routing_rule"]}
        # the run's Sample, on the marked keypoint, keyed on the validated Gadget
        k = next(p for p in written["keypoint"] if p.position == build.MARKED_POSITION)
        sample = build.store_sample(
            pool,
            build.make_sample(
                k, gadgets[FRAMES[0][1]], RUN_SAMPLE_CODE, tags=[run_tag]
            ),
        )
    facts = {
        "store_tag": run_tag.store_id,
        "dial_setting": written["dial_setting"][0].store_id,
        "knob_setting": written["knob_setting"][0].store_id,
        "Gadget": gadgets[FRAMES[0][1]].store_id,
        "validated": gadgets[FRAMES[0][1]].validated,
        "unvalidated": gadgets[FRAMES[1][1]].store_id,
        "keypoint_alias": [a.store_id for a in written["keypoint_alias"]],
        "routing_rule": (
            rules[RULE_LOW["label"]].store_id,
            rules[RULE_HIGH["label"]].store_id,
        ),
        "Sample": sample.store_id,
        "gauge_setting": {e: g.store_id for e, g in gauges.items()},
    }
    cluster.close_pool(pool)
    return facts


# ------------------------------------------------------------------------------------------------
# the reader's sequence
# ------------------------------------------------------------------------------------------------


def reader_sequence(pool, rec: Recorder):
    """A reader's lookups, in order: the run's tag, the frames, then each frame's lookups."""
    with rec.step("the run's tag (store_tag)") as s:
        tags = [build.resolve(pool.object_get("store_tag", label=run_label_tag(RUN)))]
        s.detail = f"serial={tags[0].store_id}"
    with rec.step("the frames (dial_setting, knob_setting)"):
        frames = {
            "dial": build.resolve(
                pool.object_get(
                    "dial_setting", level=DIAL_FRAME[0], stepping=DIAL_FRAME[1]
                )
            ),
            "knob": build.resolve(
                pool.object_get(
                    "knob_setting", turns=KNOB_FRAME[0], stepping=KNOB_FRAME[1]
                )
            ),
        }

    for label, gadget_label in FRAMES:
        frame = frames[label]
        with rec.step(f"[{label}] gauge_setting x4"):
            alias_a, alias_b, work_a, work_b = [
                build.resolve(pool.object_get("gauge_setting", exponent=e))
                for e in SEQUENCE_GAUGES
            ]
        with rec.step(f"[{label}] Gadget") as s:
            gadget = build.resolve(
                pool.object_get("Gadget", label=gadget_label, frame=frame, tags=tags)
            )
            s.detail = f"available={gadget.available}, serial={gadget._my_id}"
            if not gadget.available:
                raise RuntimeError(
                    "Could not locate suitable gadget instance in the datastore"
                )
        with rec.step(f"[{label}] read_table keypoint x2") as s:
            marked_k = build.resolve(pool.read_table("keypoint", marked=True))
            unmarked_k = build.resolve(pool.read_table("keypoint", marked=False))
            s.detail = f"{len(marked_k)} marked, {len(unmarked_k)} unmarked"
        with rec.step(
            f"[{label}] keypoint_alias x{len(marked_k) + len(unmarked_k)}"
        ) as s:
            aliases = [
                build.resolve(
                    pool.object_get(
                        "keypoint_alias",
                        keypoint=k,
                        offset=build.ALIAS_OFFSET,
                        stepping=build.ALIAS_STEPPING,
                    )
                )
                for k in marked_k + unmarked_k
            ]
            s.detail = (
                f"{sum(a.available for a in aliases)} of {len(aliases)} available"
            )
        with rec.step(f"[{label}] read_table dial_setting") as s:
            dials = build.resolve(pool.read_table("dial_setting"))
            s.detail = f"{len(dials)} row(s)"
        with rec.step(f"[{label}] routing_rule x2") as s:
            rule_low = build.resolve(pool.object_get("routing_rule", **RULE_LOW))
            rule_high = build.resolve(pool.object_get("routing_rule", **RULE_HIGH))
            s.detail = f"serials {rule_low.store_id}, {rule_high.store_id}"

        # one work item: the first marked keypoint
        k = marked_k[0]
        with rec.step(f"[{label}] work item: object_read_batch Sample") as s:
            batch = build.resolve(
                pool.object_read_batch("Sample", {"k": k}, validated_only=True)
            )
            s.detail = f"{len(batch)} row(s)"
        with rec.step(f"[{label}] work item: Sample, the stored row") as s:
            hit = build.resolve(
                pool.object_get(
                    "Sample", k=k, gadget=gadget, code=RUN_SAMPLE_CODE, tags=tags
                )
            )
            s.detail = f"available={hit.available}"
        with rec.step(f"[{label}] work item: Sample, a miss") as s:
            miss = build.resolve(
                pool.object_get(
                    "Sample", k=k, gadget=gadget, code=MISSED_SAMPLE_CODE, tags=tags
                )
            )
            s.detail = f"available={miss.available}"
        CONTEXT.update(label=label, gadget=gadget, k=k, tags=tags)


CONTEXT = {}
FACTS = {}


def other_sharded_lookups(pool, rec: Recorder):
    """Three more sharded lookups of the last frame's work item, each a miss that inserts nothing:
    a code no Sample has, the run's Sample asked for under no tag, and the unvalidated Sample.
    """
    c = CONTEXT
    label = c["label"]
    # the Gadgets are named by the serials the store was built with, not looked up through the
    # pool, so that this step's counts are the sharded lookups' alone
    validated = SerialHandle(FACTS["Gadget"])
    unvalidated = SerialHandle(FACTS["unvalidated"])
    for name, payload in (
        (
            "Sample of a code no Sample has",
            dict(k=c["k"], gadget=validated, code=MISSED_SAMPLE_CODE, tags=c["tags"]),
        ),
        (
            "Sample under no tag",
            dict(k=c["k"], gadget=validated, code=RUN_SAMPLE_CODE, tags=[]),
        ),
        (
            "Sample that is not validated",
            dict(k=c["k"], gadget=unvalidated, code=build.UNVALIDATED_SAMPLE, tags=[]),
        ),
    ):
        with rec.step(f"[{label}] other readers: {name}") as s:
            obj = build.resolve(pool.object_get("Sample", **payload))
            s.detail = f"available={obj.available}"
