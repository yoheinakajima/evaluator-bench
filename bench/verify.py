"""Integrity checks. Exit non-zero on any failure. Run in CI on every PR.

The checks are the CONTRACT (see CONTRACT.md). What the verifier actually
guarantees: structural integrity (ids resolve, citations exist, values are
anchors), evidence-tier gates (a 4 on F/G/P needs tier-1 evidence; a 4 on F
needs a confirmed bounded negative), ledger hygiene (supersession targets
exist, disputed rows never enter sums), and date discipline (no record dated
after the frozen evidence clock). It does NOT guarantee that a cited source
supports the claim's wording, that weights are the right weights, or that a
score is true; that is what public review and the contribution path are for.
"""
from __future__ import annotations
import sys
from .load import load, DIMS, EVIDENCE_CLOCK

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
        if e.get("role") not in ("referee","government","vendor","benchmark","lab-team","expected-entrant"):
            errs.append(f"C4 evaluator {e['id']}: unknown role {e.get('role')}")
        if e.get("status", "ranked") not in ("ranked","watchlist"):
            errs.append(f"C4 evaluator {e['id']}: unknown status {e.get('status')}")
        if e.get("status") == "watchlist" and e.get("role") != "expected-entrant":
            errs.append(f"C4 evaluator {e['id']}: watchlist entries must have role expected-entrant")
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
        led = LEDGER_ALIAS.get(a["evaluator"], a["evaluator"])
        if a["dimension"] == "F" and a["value"] == 4 and led in in_ledger and led not in neg_ok:
            errs.append(f"C8 assessment ({a['evaluator']}, F): value 4 requires a confirmed negative-evidence row in data/ledger/negatives.csv")
    # C9: every evaluator is an entity in the ledger, so nobody is exempt from exposure
    for eid_ in ev:
        if LEDGER_ALIAS.get(eid_, eid_) not in in_ledger: errs.append(f"C9 evaluator {eid_}: no ledger entity (add to data/ledger/entities.csv)")
    # C14: extremes need live evidence. A value of 0 or 4 needs at least one non-superseded signal
    # on that dimension whose sources are all confirmed; a value of 1 or 3 needs at least one signal
    # with a confirmed or unaudited source. Signals whose every source is imported, unverifiable,
    # or differs support nothing. An assessment that cannot meet the rule is set to the nearest
    # supportable value and marked evidence_limited; the site shows the mark.
    for a in ass:
        sigs = [d["signals"][i] for i in a["signals"] if i in d["signals"] and not d["signals"][i].get("superseded_by")]
        st = lambda sid: d["sources"].get(sid, {}).get("audit_status", "unaudited")
        conf = [s for s in sigs if s["sources"] and all(st(x) == "confirmed" for x in s["sources"])]
        live = [s for s in sigs if any(st(x) in ("confirmed", "unaudited") for x in s["sources"])]
        v = a["value"]
        if v in (0, 4) and not conf: errs.append(f"C14 assessment ({a['evaluator']}, {a['dimension']}): value {v} needs a signal whose sources are all confirmed; set to {1 if v == 0 else 3} and mark evidence_limited")
        elif v in (1, 3) and not live: errs.append(f"C14 assessment ({a['evaluator']}, {a['dimension']}): value {v} needs a signal with a confirmed or unaudited source; set to 2 and mark evidence_limited")
    # C10: PROCESS tier rule — a 4 on F/G/P needs tier-1 evidence (filing or index)
    # on at least one cited signal. Self pages and press cannot anchor a 4.
    for a in ass:
        if a["dimension"] in ("F", "G", "P") and a["value"] == 4:
            tiers = {src[s2]["source_type"] for s in a.get("signals", []) if s in sig
                     for s2 in sig[s].get("sources", []) if s2 in src}
            if not (tiers & {"filing", "index"}):
                errs.append(f"C10 assessment ({a['evaluator']}, {a['dimension']}): value 4 needs a tier-1 (filing/index) source on a cited signal; found {sorted(tiers) or 'none'}")
    # C11: dates are plausible (YYYY, YYYY-MM, or YYYY-MM-DD) and no record is dated
    # after the frozen evidence clock
    import datetime, re
    def _d(v):
        for fmt, rx in (("%Y-%m-%d", r"^\d{4}-\d{2}-\d{2}$"), ("%Y-%m", r"^\d{4}-\d{2}$"), ("%Y", r"^\d{4}$")):
            if re.match(rx, str(v)):
                try: return datetime.datetime.strptime(str(v), fmt).date()
                except ValueError: return None
        return None
    clock = datetime.date.fromisoformat(EVIDENCE_CLOCK)
    for s in src.values():
        for k in ("published", "retrieved"):
            v = s.get(k)
            if v and _d(v) is None: errs.append(f"C11 source {s['id']}: bad date {k}={v!r}")
            elif v and _d(v) > clock: errs.append(f"C11 source {s['id']}: {k}={v} after evidence clock {EVIDENCE_CLOCK}")
    for s in sig.values():
        for k in ("recorded", "as_of"):
            v = s.get(k)
            if v and _d(v) is None: errs.append(f"C11 signal {s['id']}: bad date {k}={v!r}")
            elif v and _d(v) > clock: errs.append(f"C11 signal {s['id']}: {k}={v} after evidence clock {EVIDENCE_CLOCK}")
    # C12: presets are complete and sum to 100 — weights are a modeling choice, but they
    # must at least be coherent; silent weight changes are a headline risk
    for pname, p in d["presets"].items():
        w = p.get("weights", {})
        if set(w) != set(DIMS): errs.append(f"C12 preset {pname}: weights must cover exactly {DIMS}")
        if abs(sum(w.values()) - 100) > 1e-9: errs.append(f"C12 preset {pname}: weights sum to {sum(w.values())}, not 100")
    return errs

LEDGER_ALIAS = {"farai": "far-ai", "grayswan": "gray-swan"}

def main(argv=None) -> int:
    errs = run()
    if errs:
        print(f"verify: {len(errs)} problem(s)")
        for e in errs: print("  -", e)
        return 1
    d = load(strict=False)
    nq = sum(1 for s in d["signals"].values() if s.get("quote")); print(f"verify: quotes on {nq}/{len(d['signals'])} signals (a quote is an exact span from the source; fill them as sources are re-derived)")
    for s in d["sources"].values():
        if s.get("source_type") == "docket":
            # C13 fail closed: a docket-type source may never be 'confirmed' without an
            # independent, signed certificate from review at epistemedia.org by
            # someone other than the drafter (see paper/CERTIFICATION.md).
            cert = s.get("certificate")
            if s.get("audit_status") == "confirmed" and not cert:
                errs.append(f"docket source {s['id']}: confirmed with no independent certificate (self-certification loop)")
            elif cert:
                from .certificate import verify as cverify
                slug = s["id"].replace("docket-", "")
                cerrs = cverify(slug)
                if cerrs: errs.append(f"docket source {s['id']}: CERTIFICATE PROBLEM: " + "; ".join(cerrs))
    if errs:
        print(f"verify: {len(errs)} problem(s)")
        for e in errs: print("  -", e)
        return 1
    print(f"verify: ok ({len(d['sources'])} sources, {len(d['signals'])} signals, {len(d['assessments'])} assessments, {len(d['evaluators'])} evaluators)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
