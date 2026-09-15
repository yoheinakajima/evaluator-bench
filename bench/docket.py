"""Bridge to Epistemedia: turn a Bench docket draft into a validated research proposal.

    python -m bench docket build metr-lab-money     # dockets/<slug>/draft.json -> proposal.json
    python -m bench docket validate metr-lab-money  # run Epistemedia's fail-closed validator if installed

A draft is a proposal in Epistemedia's v0.2 format with one relaxation: results
may omit claim atoms. `build` generates the atom closure the validator wants,
one credited atom per material literal (proposition, reported values, scope
fields), each bound to the result's spans, and keeps any hand-written atoms
(including unresolved ones, which must carry no evidence). It also stamps the
license block and completion time. What it cannot do is fetch and hash the
sources; that step runs through `epistemedia research submit` on a networked
machine, which is where the artifact digests come from.

Bench and Epistemedia divide the work: Bench keeps the index, the ledger, and
the scoring policy; Epistemedia adjudicates one contestable claim at a time
with source spans and a separate reviewer. A reviewed docket is the strongest
kind of source a Bench signal can cite.
"""
from __future__ import annotations
import json, sys, datetime, pathlib
from .load import ROOT

DOCKETS = ROOT / "dockets"
REPORTED = ("comparison", "denominator", "numerator", "rate")
SCOPE = ("dataset_or_population", "metric_scope", "time", "tool_and_retrieval_path")

def close_result(r: dict) -> dict:
    atoms = [a for a in r.get("claim_atoms", []) if a.get("status") in ("supported", "qualified")]
    kept = [a for a in r.get("claim_atoms", []) if a.get("status") not in ("supported", "qualified")]
    for a in kept: a["source_ids"] = []; a["exact_span_ids"] = []
    have = {a["text"] for a in atoms}
    src, spans = list(r["source_ids"]), list(r["exact_span_ids"])
    n = len(atoms) + len(kept)
    def add(text, kind):
        nonlocal n
        if text and text not in have:
            n += 1; atoms.append({"atom_id": f"{r['result_id']}-atom-{n}", "kind": kind, "status": "supported", "text": text, "source_ids": src, "exact_span_ids": spans}); have.add(text)
    add(r["proposition"], "finding")
    for f in REPORTED: add(str(r["reported_value"].get(f, "")), "comparison")
    for f in SCOPE: add(str(r["scope"].get(f, "")), "date" if f == "time" else "metadata")
    for m in r["scope"].get("models_or_agents", []): add(str(m), "metadata")
    # every credited atom must bind within the result's closure; widen the result closure to the union
    for a in atoms:
        a["source_ids"] = [s for s in a["source_ids"] if s in src] or src
        a["exact_span_ids"] = [s for s in a["exact_span_ids"] if s in spans] or spans
    r["claim_atoms"] = atoms + kept
    if r.get("calculation_status") not in ("reproduced", "not-applicable-no-derived-value"):
        r["calculation_status"] = "reproduced" if r.get("calculation_ids") else "not-applicable-no-derived-value"
    return r

def build(slug: str) -> pathlib.Path:
    d = DOCKETS / slug; p = json.loads((d / "draft.json").read_text())
    p["results"] = [close_result(r) for r in p["results"]]
    p.setdefault("license", {"bundle": "CC0-1.0", "source_material": "Each source retains its recorded license and treatment; spans are quote-minimal."})
    p.setdefault("runtime", {})
    if p["runtime"].get("completed_at", "unknown") == "unknown":
        p["runtime"]["completed_at"] = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    out = d / "proposal.json"; out.write_text(json.dumps(p, indent=1, ensure_ascii=False) + "\n"); return out

def validate(slug: str) -> dict:
    try:
        from epistemedia.research_kit import validate_proposal
    except ImportError:
        return {"valid": False, "errors": ["epistemedia package not installed: git clone https://github.com/yoheinakajima/epistemedia && pip install -e epistemedia"]}
    return validate_proposal(json.loads((DOCKETS / slug / "proposal.json").read_text()))

def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) < 2: print("usage: bench docket {build|validate} <slug>"); return 2
    cmd, slug = argv[0], argv[1]
    if cmd == "build":
        print("wrote", build(slug)); return 0
    if cmd == "validate":
        r = validate(slug); errs = r.get("errors", [])
        print(f"valid: {r.get('valid')}; {len(errs)} error(s)")
        for e in errs: print("  -", e)
        pend = [e for e in errs if "artifact digest" in e]
        if errs and len(pend) == len(errs): print("\nOnly artifact digests remain: run the networked submit step to fill them.")
        return 0 if r.get("valid") else 1
    print("unknown command"); return 2

if __name__ == "__main__":
    sys.exit(main())
