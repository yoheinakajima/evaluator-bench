"""One-off migration to the bounds model (v0.1): merge leads/bounds/*.json into data/.

    python -m bench.apply_bounds [--placeholders] [--only metr,scale]

--placeholders writes a provisional bound on every signal that has none
(cap or floor equal to the stored value, rule "PLACEHOLDER") so the pipeline
runs end to end before the curated bounds land; the verifier rejects
placeholders (C22), so they never reach a tagged release.

Without the flag, every leads/bounds/<evaluator>.json is applied: bounds,
rules, quotes, quote_source, new sources (with press_kind), new signals,
changed source lists, mechanism tags, resolutions, dissent, and rewritten
open questions. Then every stored assessment value is set to its derivation
under the leads-included policy, evidence_limited is recomputed, boilerplate
rationales are dropped, and roles are re-derived (RULES 10). Like
bench/seed_v0.py this file is history once run; edits go to data/ directly.
"""
from __future__ import annotations
import json, re, sys, pathlib
from .load import ROOT, DATA, load, DIMS

BOUNDS = ROOT / "leads" / "bounds"
BOILER = re.compile(r"^Anchor \d (on|from) [a-z ]+ given the cited (signals|rows)\.?$|^Anchor \d on \w+ given the cited signals\.$")

def _read(p): return json.loads(p.read_text())
def _write(p, obj): p.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")

def placeholders() -> int:
    n = 0
    for p in sorted((DATA / "signals").glob("*.json")):
        sigs = _read(p); ass = {a["dimension"]: a for a in _read(DATA / "assessments" / p.name)}
        for s in sigs:
            if "bound" in s: continue
            v = ass[s["dimension"]]["value"]
            s["bound"] = {"cap": v} if s["direction"] == "against" else {"floor": v}
            s["rule"] = "PLACEHOLDER"; n += 1
        _write(p, sigs)
    return n

def apply_file(f: pathlib.Path, report: list[str]) -> None:
    b = _read(f); eid = b["evaluator"]
    sp = DATA / "signals" / f"{eid}.json"; ap = DATA / "assessments" / f"{eid}.json"; ep = DATA / "evaluators" / f"{eid}.json"
    sigs = _read(sp); ass = _read(ap); e = _read(ep)
    by_id = {s["id"]: s for s in sigs}
    # new sources first, so signal source lists resolve
    for ns in b.get("new_sources", []) or []:
        p = DATA / "sources" / f"{ns['id']}.json"
        if p.exists():
            report.append(f"{eid}: source {ns['id']} already exists; kept the existing record")
            continue
        rec = {k: v for k, v in ns.items() if k not in ("spans",)}
        if rec.get("source_type") != "press": rec.pop("press_kind", None)
        _write(p, rec); report.append(f"{eid}: added source {ns['id']}")
    for spec_id, spec in (b.get("signals") or {}).items():
        s = by_id.get(spec_id)
        if not s:
            report.append(f"{eid}: signal {spec_id} in bounds file but not in data; skipped"); continue
        s["bound"] = spec.get("bound")
        if spec.get("rule"): s["rule"] = spec["rule"]
        else: s.pop("rule", None)
        if spec.get("bound_note"): s["bound_note"] = spec["bound_note"]
        if spec.get("quote"):
            q = spec["quote"].strip()
            if len(q) <= 120: s["quote"] = q
            else: report.append(f"{eid}: quote for {spec_id} is {len(q)} chars; truncated to the first sentence"); s["quote"] = q[:120]
            if spec.get("quote_source"): s["quote_source"] = spec["quote_source"]
        if spec.get("sources"): s["sources"] = list(dict.fromkeys(spec["sources"]))
    for ns in b.get("new_signals", []) or []:
        if ns["id"] in by_id: report.append(f"{eid}: new signal {ns['id']} collides; skipped"); continue
        ns.setdefault("recorded", "2026-09-15"); ns.setdefault("curator", "yohei/claude v0.5")
        sigs.append(ns); by_id[ns["id"]] = ns
        for a in ass:
            if a["dimension"] == ns["dimension"] and ns["id"] not in a["signals"]: a["signals"].append(ns["id"])
        report.append(f"{eid}: added signal {ns['id']} ({ns['dimension']} {ns['direction']})")
    for dim, spec in (b.get("assessments") or {}).items():
        for a in ass:
            if a["dimension"] != dim: continue
            if spec.get("mechanism"): a["mechanism"] = spec["mechanism"]
            if spec.get("resolution"): a["resolution"] = spec["resolution"]
    for c in b.get("conflicts", []) or []:
        for a in ass:
            if a["dimension"] == c.get("dimension") and c.get("resolution"): a["resolution"] = c["resolution"]
    for dim, qs in (b.get("open_question_rewrites") or {}).items():
        for a in ass:
            if a["dimension"] == dim and qs: a["open_questions"] = list(qs)
    if b.get("dissent") and b["dissent"].get("lower") and b["dissent"].get("higher"):
        e["dissent"] = {"lower": b["dissent"]["lower"].strip(), "higher": b["dissent"]["higher"].strip()}
    _write(sp, sigs); _write(ap, ass); _write(ep, e)

def recompute(report: list[str]) -> None:
    from .policy import derive
    from .roles import derive_role, list_group
    d = load(strict=False)
    for p in sorted((DATA / "assessments").glob("*.json")):
        ass = _read(p); changed = False
        for a in ass:
            r = derive(a, d["signals"], d["sources"], "leads")
            if r["value"] is None:
                if not a.get("unevidenced"): a["unevidenced"] = True; report.append(f"{a['evaluator']}.{a['dimension']}: no bound derives a value; marked unevidenced (last reading {a['value']} kept, never shown)")
                a.pop("evidence_limited", None); continue
            if a.get("unevidenced"): a.pop("unevidenced", None)
            if r["value"] != a["value"]:
                report.append(f"{a['evaluator']}.{a['dimension']}: {a['value']} -> {r['value']} ({r['rationale'][:120]})")
                a["value"] = a["anchor"] = r["value"]; a["assessed"] = "2026-09-15"; a["assessor"] = "rules v0.1 (RULES.md)"; changed = True
            if bool(a.get("evidence_limited")) != bool(r["evidence_limited"]):
                if r["evidence_limited"]: a["evidence_limited"] = True
                else: a.pop("evidence_limited", None)
                changed = True
            if a.get("rationale") and BOILER.match(a["rationale"].strip()):
                a.pop("rationale", None); changed = True
        _write(p, ass)
    d = load(strict=False)
    xval = {(a["evaluator"], a["dimension"]): a["value"] for a in d["assessments"]}
    for p in sorted((DATA / "evaluators").glob("*.json")):
        e = _read(p); want = derive_role(e, xval.get((e["id"], "X")))
        if e.get("role") != want: report.append(f"{e['id']}: role {e.get('role')} -> {want} (RULES 10)"); e["role"] = want
        e["list_group"] = list_group(e, want)
        _write(p, e)

def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    report: list[str] = []
    if "--placeholders" in argv:
        print(f"placeholders written on {placeholders()} signals"); return 0
    only = None
    if "--only" in argv: only = set(argv[argv.index("--only") + 1].split(","))
    files = [] if "--recompute-only" in argv else sorted(BOUNDS.glob("*.json"))
    for f in files:
        if only and f.stem not in only: continue
        apply_file(f, report)
    recompute(report)
    print("\n".join(report) if report else "nothing changed")
    print(f"applied {len(files)} bounds file(s)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
