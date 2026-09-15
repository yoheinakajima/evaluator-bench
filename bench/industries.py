"""Cross-industry lifecycle table from data/industries/.

For each regime: first voluntary assurance, first trigger incident, first
mandate, first independence rule or accreditation, and the lags between
them. This is the seed for the paper's Figure 1.
"""
from __future__ import annotations
import json, pathlib, sys
from .load import DATA

def first(ms, kinds):
    ys = [m["year"] for m in ms if m["kind"] in kinds]
    return min(ys) if ys else None

def rows():
    out = []
    for p in sorted((DATA / "industries").glob("*.json")):
        o = json.loads(p.read_text()); ms = o["milestones"]
        v = first(ms, {"voluntary_assurance"})
        t = first(ms, {"trigger"})
        m = first(ms, {"mandate"})
        r = first(ms, {"independence_rule", "accreditation", "delegation_reform", "payer_reform", "publication_rule"})
        start = min(x for x in [v, m, t] if x is not None)
        triggers = sorted(mm["year"] for mm in ms if mm["kind"] == "trigger")
        def lag(target):
            if target is None: return None
            prior = [y for y in triggers if y <= target]
            return (target - max(prior)) if prior else None
        rule_years = sorted(mm["year"] for mm in ms if mm["kind"] in {"independence_rule","accreditation","delegation_reform","payer_reform","publication_rule","mandate","standards"})
        # lag from each trigger to the next rule of any kind
        lags = []
        for ty in triggers:
            nxt = [y for y in rule_years if y >= ty]
            if nxt: lags.append(min(nxt) - ty)
        out.append(dict(id=o["id"], name=o["name"], voluntary=v, trigger=t, mandate=m, independence=r,
                        to_mandate=(m - start) if m else None, to_independence=(r - start) if r else None,
                        trigger_to_rule=lag(r), trigger_lags=lags, payer=o["payer"]))
    return out

def main(argv=None) -> int:
    rs = rows()
    print(f"{'regime':32s} {'volunt.':>7s} {'trigger':>7s} {'mandate':>7s} {'indep.':>7s} {'->ind':>6s} {'trig->rule lags':>16s}")
    for r in rs:
        f = lambda x: "" if x is None else str(x)
        print(f"{r['name'][:32]:32s} {f(r['voluntary']):>7s} {f(r['trigger']):>7s} {f(r['mandate']):>7s} {f(r['independence']):>7s} {f(r['to_independence']):>6s} {','.join(map(str,r['trigger_lags'])):>16s}")
    alll = [x for r in rs if r['id']!='frontier-ai' for x in r['trigger_lags']]
    if alll:
        alll.sort(); med = alll[len(alll)//2]
        print(f"\nTrigger to next rule, all non-AI regimes: n={len(alll)}, median {med} years, max {max(alll)}; drift before the first trigger is measured in decades.")
    if "--json" in (argv or []):
        print(json.dumps(rs, indent=1))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
