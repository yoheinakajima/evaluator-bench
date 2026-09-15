"""Integrity checks. Exit non-zero on any failure. Run in CI on every PR.

The checks are the CONTRACT (see CONTRACT.md). A PR that changes a score
without changing a signal fails here.
"""
from __future__ import annotations
import sys
from .load import load, DIMS

def run(data: dict | None = None) -> list[str]:
    d = data or load(strict=False)
    errs: list[str] = list(d["errors"])
    src, ev, sig, ass = d["sources"], d["evaluators"], d["signals"], d["assessments"]
    dims = {x["key"]: x for x in d["dimensions"]}
    # C1: every source has url + retrieved date
    for s in src.values():
        if not s.get("url","").startswith("http"): errs.append(f"C1 source {s['id']}: url missing or not http")
        if not s.get("retrieved"): errs.append(f"C1 source {s['id']}: retrieved date missing")
    # C2: every signal cites >=1 existing source and names an existing evaluator + dimension
    for s in sig.values():
        if s["evaluator"] not in ev: errs.append(f"C2 signal {s['id']}: unknown evaluator {s['evaluator']}")
        if s["dimension"] not in dims: errs.append(f"C2 signal {s['id']}: unknown dimension {s['dimension']}")
        if s["direction"] not in ("for","against"): errs.append(f"C2 signal {s['id']}: direction must be for/against")
        if not s.get("sources"): errs.append(f"C2 signal {s['id']}: cites no source")
        for x in s.get("sources", []):
            if x not in src: errs.append(f"C2 signal {s['id']}: unknown source {x}")
    # C3: every assessment cites >=1 signal on the same evaluator and dimension; value in 0..4 and == anchor
    seen = {}
    for a in ass:
        key = (a["evaluator"], a["dimension"])
        if key in seen: errs.append(f"C3 duplicate assessment {key}")
        seen[key] = a
        if a["evaluator"] not in ev: errs.append(f"C3 assessment {key}: unknown evaluator")
        if a["dimension"] not in dims: errs.append(f"C3 assessment {key}: unknown dimension")
        if not (isinstance(a["value"], int) and 0 <= a["value"] <= 4): errs.append(f"C3 assessment {key}: value out of range")
        if a.get("anchor") != a["value"]: errs.append(f"C3 assessment {key}: anchor must equal value")
        if not a.get("signals"): errs.append(f"C3 assessment {key}: cites no signal")
        for sid in a.get("signals", []):
            s = sig.get(sid)
            if not s: errs.append(f"C3 assessment {key}: unknown signal {sid}"); continue
            if s["evaluator"] != a["evaluator"]: errs.append(f"C3 assessment {key}: signal {sid} belongs to {s['evaluator']}")
            if s["dimension"] != a["dimension"]: errs.append(f"C3 assessment {key}: signal {sid} is on dimension {s['dimension']}")
        if not a.get("rationale"): errs.append(f"C3 assessment {key}: rationale missing")
    # C4: every evaluator has all 8 dimensions assessed and >=1 signal
    for e in ev.values():
        for k in DIMS:
            if (e["id"], k) not in seen: errs.append(f"C4 evaluator {e['id']}: no assessment for {k}")
        if not any(s["evaluator"] == e["id"] for s in sig.values()): errs.append(f"C4 evaluator {e['id']}: no signals")
        if e.get("confidence") not in ("high","med","low"): errs.append(f"C4 evaluator {e['id']}: confidence must be high/med/low")
        if e.get("type") not in d["types"]: errs.append(f"C4 evaluator {e['id']}: unknown type {e.get('type')}")
    # C5: no orphan sources
    used = {x for s in sig.values() for x in s.get("sources", [])}
    for sid in src:
        if sid not in used: errs.append(f"C5 source {sid}: cited by no signal")
    # C6: a 4 on any dimension needs at least one 'for' signal; a 0 needs at least one 'against'
    for a in ass:
        dirs = {sig[s]["direction"] for s in a.get("signals", []) if s in sig}
        if a["value"] == 4 and "for" not in dirs: errs.append(f"C6 assessment {(a['evaluator'],a['dimension'])}: value 4 without a 'for' signal")
        if a["value"] == 0 and "against" not in dirs: errs.append(f"C6 assessment {(a['evaluator'],a['dimension'])}: value 0 without an 'against' signal")
    # C7: ledger integrity
    try:
        from .ledger import load_ledger, validate as lvalidate
        L = load_ledger(); errs += lvalidate(L)
        neg_ok = {n["evaluator"] for n in L["negatives"] if n["source_type"] in ("filing", "index") and n["audit_status"] == "confirmed"}
        in_ledger = {e for e, x in L["entities"].items() if x["kind"] == "evaluator"}
    except Exception as ex:  # pragma: no cover
        errs.append(f"C7 ledger failed to load: {ex}"); neg_ok = set(); in_ledger = set()
    # C8: a 4 on funding needs a confirmed bounded negative in a primary filing or index
    for a in ass:
        if a["dimension"] == "F" and a["value"] == 4 and a["evaluator"] in in_ledger and a["evaluator"] not in neg_ok:
            errs.append(f"C8 assessment ({a['evaluator']}, F): value 4 requires a confirmed negative-evidence row in data/ledger/negatives.csv")
    return errs

def main(argv=None) -> int:
    errs = run()
    if errs:
        print(f"verify: {len(errs)} problem(s)")
        for e in errs: print("  -", e)
        return 1
    d = load(strict=False)
    print(f"verify: ok ({len(d['sources'])} sources, {len(d['signals'])} signals, {len(d['assessments'])} assessments, {len(d['evaluators'])} evaluators)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
