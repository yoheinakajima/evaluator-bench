"""`bench inspect <evaluator-id> [--dim F]`: walk the provenance chain.

score -> assessment -> signal -> source, with graph object ids and the
creating event ids, read back from graph/events.jsonl so what you see is
what the log says, not what data/ says.
"""
from __future__ import annotations
import json, sys
from .load import ROOT, DIMS

def load_log():
    objs, rels, created = {}, [], {}
    with open(ROOT / "graph" / "events.jsonl") as f:
        for line in f:
            rec = json.loads(line); ev = rec["event"]
            if ev["type"] == "object.created":
                o = ev["payload"]["object"]; objs[o["id"]] = o; created[o["id"]] = ev["id"]
            elif ev["type"] == "relation.created":
                rels.append(ev["payload"].get("relation") or ev["payload"])
    return objs, rels, created

def inspect(eid: str, dim: str | None = None, preset: str = "lab") -> str:
    objs, rels, created = load_log()
    ev = next((o for o in objs.values() if o["type"] == "evaluator" and o["data"]["id"] == eid), None)
    if not ev: return f"no evaluator '{eid}' in graph/events.jsonl"
    out = [f"{ev['data']['name']}  [{ev['id']}, created by {created[ev['id']]}]"]
    sc = next(o for o in objs.values() if o["type"] == "score" and o["data"]["evaluator"] == eid and o["data"]["preset"] == preset)
    out.append(f"  score ({preset}) = {sc['data']['value']}  [{sc['id']}, evidence: {', '.join(sc['provenance']['evidence'])}]")
    for a in (o for o in objs.values() if o["type"] == "assessment" and o["data"]["evaluator"] == eid):
        if dim and a["data"]["dimension"] != dim: continue
        out.append(f"    {a['data']['dimension']} = {a['data']['value']}/4  [{a['id']}, by {a['provenance']['created_by']} at {a['provenance']['timestamp']}]")
        for sid in a["data"]["signals"]:
            s = next(o for o in objs.values() if o["type"] == "signal" and o["data"]["id"] == sid)
            out.append(f"      {s['data']['direction']:7s} {s['data']['claim']}  [{s['id']}]")
            for src_id in s["data"]["sources"]:
                src = next(o for o in objs.values() if o["type"] == "source" and o["data"]["id"] == src_id)
                out.append(f"              source: {src['data']['title']} ({src['data']['publisher']}, {src['data']['published']}; retrieved {src['data']['retrieved']})  {src['data']['url']}  [{src['id']}]")
    return "\n".join(out)

def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv: print("usage: bench inspect <evaluator-id> [--dim K] [--preset NAME]"); return 2
    eid = argv[0]; dim = None; preset = "lab"
    if "--dim" in argv: dim = argv[argv.index("--dim") + 1]
    if "--preset" in argv: preset = argv[argv.index("--preset") + 1]
    print(inspect(eid, dim, preset)); return 0
