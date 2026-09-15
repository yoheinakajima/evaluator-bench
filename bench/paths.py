"""Second-generation analyses of Dataset B that do not assume a linear ladder.

paths()      the ordered sequence of milestone kinds per regime (a path signature)
analogues()  regimes whose opening sequence most resembles frontier AI's so far
responses()  every trigger paired with the next rule, with lag and strength
mechanisms() who pays / selects / sees / publishes / oversees, before and now

`python -m bench paths` prints all four.
"""
from __future__ import annotations
import json, sys
from .load import DATA
from .timeline import ORDER

LETTER = {"proposal": "", "voluntary_assurance": "V", "trigger": "T", "mandate": "M", "standards": "S", "accreditation": "O",
          "independence_rule": "I", "delegation_reform": "I", "payer_reform": "I", "access_expansion": "A",
          "publication_rule": "A", "delegation": "D", "payer_shift": "P", "rollback": "R"}
LETTER_LABEL = {"V": "voluntary", "T": "trigger", "M": "mandate", "S": "standards", "O": "oversight", "I": "independence",
                "A": "access/publication", "D": "delegation", "P": "payer shift", "R": "rollback"}
KIND_ORDER = ["rollback", "proposal", "voluntary_assurance", "delegation", "payer_shift", "trigger", "mandate", "standards",
              "accreditation", "independence_rule", "delegation_reform", "payer_reform", "access_expansion", "publication_rule"]
RULE_KINDS = {"mandate", "standards", "accreditation", "independence_rule", "delegation_reform", "payer_reform", "publication_rule", "access_expansion"}

def _regimes() -> list[dict]:
    d = {p.stem: json.loads(p.read_text()) for p in (DATA / "industries").glob("*.json")}
    return [d[k] for k in ORDER if k in d] + [d[k] for k in sorted(set(d) - set(ORDER))]

def paths() -> list[dict]:
    out = []
    for o in _regimes():
        ms = sorted(o["milestones"], key=lambda m: (m["year"], KIND_ORDER.index(m["kind"]) if m["kind"] in KIND_ORDER else 99))
        ms = [m for m in ms if LETTER[m["kind"]]]  # proposals are context, not assurance events
        raw = "".join(LETTER[m["kind"]] for m in ms)
        sig = "".join(c for i, c in enumerate(raw) if i == 0 or c != raw[i - 1])  # collapse repeats: structure, not count
        out.append(dict(id=o["id"], name=o["name"], letters=sig, raw=raw,
                        steps=[dict(year=m["year"], kind=m["kind"], letter=LETTER[m["kind"]], event=m["event"], source=m["source"],
                                    strength=m.get("strength"), harm=m.get("harm")) for m in ms]))
    return out

def _lev(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

def analogues(target_id: str = "frontier-ai") -> list[dict]:
    ps = {p["id"]: p for p in paths()}
    t = ps[target_id]["letters"]; n = len(t)
    out = []
    for pid, p in ps.items():
        if pid == target_id: continue
        s = p["letters"]; best = None
        lo = max(1, min(len(s), n - 2)); hi = min(len(s), n + 2)
        for L in range(lo, hi + 1):  # compare against openings of similar length
            prefix = s[:L]; d = _lev(t, prefix) / max(n, L)
            if best is None or d < best[0]: best = (d, prefix)
        out.append(dict(id=pid, name=p["name"], distance=round(best[0], 3), matched_opening=best[1], full=s))
    return sorted(out, key=lambda x: x["distance"])

def responses() -> list[dict]:
    out = []
    for o in _regimes():
        ms = sorted(o["milestones"], key=lambda m: m["year"])
        for i, m in enumerate(ms):
            if m["kind"] != "trigger": continue
            nxt = next((x for x in ms[i + 1:] if x["kind"] in RULE_KINDS), None)
            nxt_same_year = [x for x in ms if x["kind"] in RULE_KINDS and x["year"] == m["year"] and x is not m]
            cand = nxt_same_year[0] if nxt_same_year and (nxt is None or nxt["year"] > m["year"]) else nxt
            out.append(dict(regime=o["id"], name=o["name"], year=m["year"], trigger=m["event"], harm=m.get("harm"),
                            lag=(cand["year"] - m["year"]) if cand else None, response=cand["event"] if cand else None,
                            response_kind=cand["kind"] if cand else None, strength=cand.get("strength") if cand else None,
                            response_year=cand["year"] if cand else None))
    return out

def mechanisms() -> list[dict]:
    return [dict(id=o["id"], name=o["name"], **o["mechanisms"]) for o in _regimes() if "mechanisms" in o]

def main(argv=None) -> int:
    print("Path signatures (V voluntary, T trigger, M mandate, S standards, O oversight, I independence, A access/publication, D delegation, P payer shift, R rollback)")
    for p in paths(): print(f"  {p['name'][:36]:36s} {p['letters']}")
    print("\nNearest openings to frontier AI's path so far:")
    for a in analogues()[:6]: print(f"  {a['distance']:.2f}  {a['name'][:36]:36s} opening {a['matched_opening']}")
    print("\nTrigger -> next rule (lag years, strength 1..4):")
    rs = responses()
    for r in rs:
        print(f"  {r['name'][:28]:28s} {r['year']}  lag {str(r['lag']) if r['lag'] is not None else '-':>2s}  strength {str(r['strength']) if r['strength'] else '-'}  {r['response_kind'] or 'none'}")
    fast = [r for r in rs if r["lag"] is not None and r["lag"] <= 3 and r["regime"] != "frontier-ai"]
    if fast:
        from statistics import mean
        print(f"\n  responses within 3 years: n={len(fast)}, mean strength {mean(r['strength'] for r in fast):.2f}; structural (4): {sum(1 for r in fast if r['strength']==4)}")
    print("\nMechanisms now (pays/selects/access/publishes/oversees):")
    for m in mechanisms(): n = m["now"]; print(f"  {m['name'][:36]:36s} {n['pays']:>2s} {n['selects']:>4s} {n['access']:>8s} {n['publishes']:>7s} {n['oversees']:>9s}")
    if "--json" in (argv or []):
        print(json.dumps(dict(paths=paths(), analogues=analogues(), responses=rs, mechanisms=mechanisms()), indent=1))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
