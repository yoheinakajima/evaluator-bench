"""Build the ActiveGraph graph from data/, write the event log and projections.

Object types
  dimension   the eight scoring axes with anchors
  source      a URL with a retrieval date
  evaluator   an organization
  signal      one dated claim, for or against, on one dimension, citing sources
  assessment  a 0..4 value on one dimension, citing signals
  score       a weighted total per preset, citing assessments

Relation types
  signal      --cites-->     source
  signal      --about-->     evaluator
  signal      --on-->        dimension
  assessment  --supported_by--> signal
  assessment  --of-->        evaluator
  assessment  --on-->        dimension
  score       --derived_from--> assessment
  score       --of-->        evaluator

ActiveGraph's provenance carries the creating actor, timestamp, and
``evidence`` (event ids). We pass the creating events of the cited objects as
evidence so every assessment's provenance names the signal events, and every
score's provenance names the assessment events. The clock is frozen and the
run_id is fixed, so graph/events.jsonl is byte-for-byte reproducible from
data/ and any diff in CI means data changed.
"""
from __future__ import annotations
import json, pathlib, shutil
from activegraph import Graph, IDGen, FrozenClock, JSONLEventSink
from .load import load, ROOT, DIMS
from .score import score

GRAPH_DIR = ROOT / "graph"
DIST = ROOT / "dist"
SITE = ROOT / "site"
BUILD_CLOCK = "2026-09-14T00:00:00Z"   # bump when re-curating; keeps the log reproducible
RUN_ID = "evaluator-bench-build"

def build(write: bool = True) -> dict:
    d = load(strict=True)
    g = Graph(ids=IDGen(), clock=FrozenClock(BUILD_CLOCK), run_id=RUN_ID)
    created: dict[str, str] = {}          # object id -> creating event id
    g.add_listener(lambda ev: created.__setitem__(ev.payload["id"], ev.id) if ev.type == "object.created" else None)
    sink_path = GRAPH_DIR / "events.jsonl"
    if write:
        GRAPH_DIR.mkdir(exist_ok=True)
        if sink_path.exists(): sink_path.unlink()
        g.add_sink(JSONLEventSink(sink_path), name="jsonl", queue_capacity=1_000_000, overflow_policy="fail_sink")

    ids: dict[str, str] = {}              # data id -> graph object id
    # dimensions
    for dim in d["dimensions"]:
        o = g.add_object("dimension", dim, actor="build")
        ids[f"dim:{dim['key']}"] = o.id
    # sources
    for s in d["sources"].values():
        o = g.add_object("source", s, actor="curator")
        ids[f"src:{s['id']}"] = o.id
    # evaluators
    for e in d["evaluators"].values():
        o = g.add_object("evaluator", e, actor="curator")
        ids[f"ev:{e['id']}"] = o.id
    # signals
    for s in d["signals"].values():
        src_objs = [ids[f"src:{x}"] for x in s["sources"]]
        o = g.add_object("signal", s, actor=s.get("curator", "curator"),
                         evidence=[created[x] for x in src_objs])
        ids[f"sig:{s['id']}"] = o.id
        for x in src_objs:
            g.add_relation(o.id, x, "cites", actor="build")
        g.add_relation(o.id, ids[f"ev:{s['evaluator']}"], "about", actor="build")
        g.add_relation(o.id, ids[f"dim:{s['dimension']}"], "on", actor="build")
    # assessments
    values: dict[str, dict[str, int]] = {}
    assess_events: dict[str, list[str]] = {}
    for a in d["assessments"]:
        sig_objs = [ids[f"sig:{x}"] for x in a["signals"]]
        o = g.add_object("assessment", a, actor=a.get("assessor", "curator"),
                         evidence=[created[x] for x in sig_objs])
        ids[f"ass:{a['evaluator']}:{a['dimension']}"] = o.id
        for x in sig_objs:
            g.add_relation(o.id, x, "supported_by", actor="build")
        g.add_relation(o.id, ids[f"ev:{a['evaluator']}"], "of", actor="build")
        g.add_relation(o.id, ids[f"dim:{a['dimension']}"], "on", actor="build")
        values.setdefault(a["evaluator"], {})[a["dimension"]] = a["value"]
        assess_events.setdefault(a["evaluator"], []).append(created[o.id])
    # scores (one per evaluator per preset)
    scores: dict[str, dict[str, int]] = {}
    for eid, vals in values.items():
        for pname, p in d["presets"].items():
            v = score(vals, p["weights"])
            o = g.add_object("score", {"evaluator": eid, "preset": pname, "weights": p["weights"], "value": v},
                             actor="build", evidence=assess_events[eid])
            for k in DIMS:
                g.add_relation(o.id, ids[f"ass:{eid}:{k}"], "derived_from", actor="build")
            g.add_relation(o.id, ids[f"ev:{eid}"], "of", actor="build")
            scores.setdefault(eid, {})[pname] = v
    if write:
        g.flush_sinks(); g.close_sinks()

    # projection for the site and for downstream users
    bench = {
        "built_at": BUILD_CLOCK, "version": 1,
        "dimensions": d["dimensions"], "presets": d["presets"], "types": d["types"],
        "sources": d["sources"],
        "evaluators": [],
    }
    for e in d["evaluators"].values():
        eid = e["id"]
        sigs = [s for s in d["signals"].values() if s["evaluator"] == eid]
        ass = {a["dimension"]: a for a in d["assessments"] if a["evaluator"] == eid}
        bench["evaluators"].append({
            **e,
            "graph_id": ids[f"ev:{eid}"],
            "values": {k: ass[k]["value"] for k in DIMS},
            "assessments": {k: {**ass[k], "graph_id": ids[f"ass:{eid}:{k}"]} for k in DIMS},
            "signals": [{**s, "graph_id": ids[f"sig:{s['id']}"], "source_graph_ids": [ids[f"src:{x}"] for x in s["sources"]]} for s in sigs],
            "scores": scores[eid],
        })
    if write:
        DIST.mkdir(exist_ok=True)
        (DIST / "bench.json").write_text(json.dumps(bench, indent=1, ensure_ascii=False) + "\n")
        from .timeline import write as write_timeline
        rows = write_timeline(DIST)
        _write_site(bench, rows)
        _write_summary(g, bench)
    return {"graph": g, "bench": bench, "ids": ids}

def _write_site(bench: dict, timeline_rows: list | None = None) -> None:
    tpl = (SITE / "template.html").read_text()
    html = tpl.replace("/*__BENCH_JSON__*/null", json.dumps(bench, ensure_ascii=False))
    svg_path = DIST / "timeline.svg"
    html = html.replace("<!--__TIMELINE_SVG__-->", svg_path.read_text() if svg_path.exists() else "")
    html = html.replace("/*__TIMELINE_JSON__*/null", json.dumps(timeline_rows or [], ensure_ascii=False))
    (DIST / "index.html").write_text(html)

def _write_summary(g: Graph, bench: dict) -> None:
    objs = g.all_objects(); rels = g.all_relations()
    by_type: dict[str, int] = {}
    for o in objs: by_type[o.type] = by_type.get(o.type, 0) + 1
    lines = ["# Graph summary", "", f"Built at {bench['built_at']} (frozen clock; run_id {RUN_ID})", "",
             "| type | objects |", "|---|---|"] + [f"| {t} | {n} |" for t, n in sorted(by_type.items())]
    lines += ["", f"Relations: {len(rels)}", "", "Rebuild: `python -m bench build`. The event log is reproducible; a diff means data/ changed."]
    (GRAPH_DIR / "README.md").write_text("\n".join(lines) + "\n")

def main(argv=None) -> int:
    r = build(write=True)
    print(f"build: {len(r['graph'].all_objects())} objects, {len(r['graph'].all_relations())} relations -> graph/events.jsonl, dist/bench.json, dist/index.html")
    return 0

if __name__ == "__main__":
    import sys; sys.exit(main())
