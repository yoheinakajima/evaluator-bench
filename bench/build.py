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
from .load import load, ROOT, DIMS, EVIDENCE_CLOCK
from .score import score

GRAPH_DIR = ROOT / "graph"
DIST = ROOT / "dist"
SITE = ROOT / "site"
BUILD_CLOCK = f"{EVIDENCE_CLOCK}T00:00:00Z"   # frozen evidence clock; bump EVIDENCE_CLOCK in load.py when re-curating
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
    # ledger: entities, transfers, relationships, negatives (row-level provenance)
    from .ledger import load_ledger
    L = load_ledger()
    for eid_, ent in L["entities"].items():
        o = g.add_object("entity", ent, actor="curator"); ids[f"ent:{eid_}"] = o.id
    for t in L["transfers"]:
        rel_data = {k: v for k, v in t.items() if k not in ("from", "to")}
        g.add_relation(ids[f"ent:{t['from']}"], ids[f"ent:{t['to']}"], "funds", rel_data, actor="curator")
    for r in L["relationships"]:
        rel_data = {k: v for k, v in r.items() if k not in ("subject", "object")}
        g.add_relation(ids[f"ent:{r['subject']}"], ids[f"ent:{r['object']}"], r["role"], rel_data, actor="curator")
    for nrow in L["negatives"]:
        o = g.add_object("negative_evidence", nrow, actor="curator")
        g.add_relation(o.id, ids[f"ent:{nrow['evaluator']}"], "bounds", actor="build")
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
    TIER_RANK = {"filing": 1, "index": 1, "ledger": 2, "self": 3, "press": 4, "docket": 5}
    TIER_NAME = {1: "tier 1 (filing/index)", 2: "tier 2 (ledger)", 3: "tier 3 (self)", 4: "tier 4 (press)", 5: "docket draft"}
    def _evidence_tier(a):
        ranks = [TIER_RANK.get(d["sources"][sid2].get("source_type"), 9)
                 for sid in a.get("signals", []) if sid in d["signals"]
                 for sid2 in d["signals"][sid].get("sources", []) if sid2 in d["sources"]]
        return TIER_NAME.get(min(ranks), "unknown") if ranks else "unknown"
    for e in d["evaluators"].values():
        eid = e["id"]
        sigs = [s for s in d["signals"].values() if s["evaluator"] == eid]
        ass = {a["dimension"]: a for a in d["assessments"] if a["evaluator"] == eid}
        bench["evaluators"].append({
            **e,
            "graph_id": ids[f"ev:{eid}"],
            "values": {k: ass[k]["value"] for k in DIMS},
            "assessments": {k: {**ass[k], "graph_id": ids[f"ass:{eid}:{k}"], "evidence_tier": _evidence_tier(ass[k])} for k in DIMS},
            "signals": [{**s, "graph_id": ids[f"sig:{s['id']}"], "source_graph_ids": [ids[f"src:{x}"] for x in s["sources"]]} for s in sigs],
            "scores": scores[eid],
        })
    if write:
        DIST.mkdir(exist_ok=True)
        (DIST / "bench.json").write_text(json.dumps(bench, indent=1, ensure_ascii=False) + "\n")
        from .timeline import write as write_timeline
        rows = write_timeline(DIST)
        from .ledger import exposure, distances
        (DIST / "exposure.json").write_text(json.dumps({"distances": distances(L), "evaluators": exposure(L)}, indent=1, sort_keys=True))
        from .figures import write as write_figures
        write_figures(DIST, ROOT / "paper" / "figures")
        _write_site(bench, rows)
        from .site import render_all
        render_all(bench)
        _write_summary(g, bench)
    return {"graph": g, "bench": bench, "ids": ids}

def _write_site(bench: dict, timeline_rows: list | None = None) -> None:
    tpl = (SITE / "template.html").read_text()
    from .site import release_banner
    html = tpl.replace("<!--__RELEASE_BANNER__-->", release_banner(""))
    html = html.replace("/*__BENCH_JSON__*/null", json.dumps(bench, ensure_ascii=False))
    svg_path = DIST / "timeline.svg"
    html = html.replace("<!--__TIMELINE_SVG__-->", svg_path.read_text() if svg_path.exists() else "")
    html = html.replace("/*__TIMELINE_JSON__*/null", json.dumps(timeline_rows or [], ensure_ascii=False))
    from .timeline import stages_meta, NON_STAGE_KINDS, ORDER
    inds = {p.stem: json.loads(p.read_text()) for p in (ROOT / "data" / "industries").glob("*.json")}
    ordered = [inds[k] for k in ORDER if k in inds] + [inds[k] for k in sorted(set(inds) - set(ORDER))]
    html = html.replace("/*__INDUSTRIES_JSON__*/null", json.dumps(ordered, ensure_ascii=False))
    for name in ("paths", "responses", "mechanisms", "exposure", "graph"):
        fp = DIST / f"{name}.svg"
        html = html.replace(f"<!--__FIG_{name.upper()}__-->", fp.read_text() if fp.exists() else "")
    from .verify import LEDGER_ALIAS
    html = html.replace("/*__LEDGER_MAP__*/null", json.dumps({e["id"]: LEDGER_ALIAS.get(e["id"], e["id"]) for e in bench["evaluators"]}))
    ex_path = DIST / "exposure.json"
    html = html.replace("/*__EXPOSURE_JSON__*/null", ex_path.read_text() if ex_path.exists() else "null")
    html = html.replace("/*__STAGES_JSON__*/null", json.dumps({"stages": stages_meta(), "other": NON_STAGE_KINDS}, ensure_ascii=False))
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
