"""Gates for a citable tag (paper/PLAN-v0.1.md, section 7).

    python -m bench gates          # print pass/fail per gate
    python -m bench gates --json   # machine-readable

A release may be published only when every gate passes (bench/release.py
refuses otherwise, unless --override names a reason, which is recorded).
The status page renders the same table.
"""
from __future__ import annotations
import csv, json, re, sys
from .load import ROOT, DATA, load, DIMS
from .policy import derive, DEFAULT_POLICY, POLICY_ORDER
from .verify import LEDGER_ALIAS

OUTREACH = DATA / "outreach-log.csv"
SECOND = DATA / "coding" / "second-coder.csv"


def _csv(p):
    if not p.exists(): return []
    with open(p, newline="") as f: return [dict(r) for r in csv.DictReader(f)]


def _person_mentioned(text: str, name: str) -> bool:
    """True if an individual personal name appears in text.

    Group entities ("Anthropic employees (personal holdings)", "... (unnamed)")
    are never individual recipients, so they never match.
    """
    if not text or "(" in name or "employees" in name.lower():
        return False
    parts = name.split()
    if len(parts) < 2 or not all(p[:1].isupper() for p in parts):
        return False
    first, last = parts[0], parts[-1]
    return bool(re.search(r"\b%s\b.*\b%s\b" % (re.escape(first), re.escape(last)), text, re.I | re.S)
                or re.search(r"\b%s\b" % re.escape(last), text, re.I))


def material_people(d: dict | None = None, L: dict | None = None) -> list[str]:
    """Person entities in outreach scope under RULES 12.

    Personal outreach is reserved for the case where the bench's own claim
    text names an individual in a signal binding under the default policy —
    i.e. we publish an assertion about a person that moves a score. People
    named only inside a quoted evidence span, in background role mentions,
    or in document requests are covered by the public correction channel;
    document requests are directed to the relevant organization, which can
    route to the individual.
    """
    from .ledger import load_ledger
    d = d or load(strict=False)
    L = L or load_ledger()
    ranked = {e["id"] for e in d["evaluators"].values() if e.get("status", "ranked") == "ranked"}
    found: set[str] = set()
    for a in d["assessments"]:
        if a["evaluator"] not in ranked:
            continue
        r = derive(a, d["signals"], d["sources"], DEFAULT_POLICY)
        for sid in r["binding"]:
            claim = d["signals"][sid].get("claim") or ""
            for pid, e in L["entities"].items():
                if e["kind"] != "person" or pid in found:
                    continue
                if _person_mentioned(claim, e["name"]):
                    found.add(pid)
    return sorted(found)


def gates(d: dict | None = None) -> list[dict]:
    d = d or load(strict=False)
    ranked = [e for e in d["evaluators"].values() if e.get("status", "ranked") == "ranked"]
    rids = {e["id"] for e in ranked}
    out = []
    # 1. every binding signal under the default policy carries a quoted span
    missing = []
    missing_extreme = []
    for a in d["assessments"]:
        if a["evaluator"] not in rids: continue
        r = derive(a, d["signals"], d["sources"], DEFAULT_POLICY)
        for sid in r["binding"]:
            if not d["signals"][sid].get("quote"):
                missing.append(sid)
                if r["value"] in (0, 4): missing_extreme.append(sid)
    detail = f"{len(missing)} binding signal(s) without a span" + (": " + ", ".join(missing[:12]) + ("..." if len(missing) > 12 else "") if missing else "")
    if missing and not missing_extreme:
        detail += "; all bind to non-extreme values (1-3), so no displayed score violates the clamp rule"
    elif missing_extreme:
        detail += "; WARNING: bind(s) to an extreme value: " + ", ".join(sorted(set(missing_extreme)))
    out.append(dict(gate="Every binding signal has a quoted span", ok=not missing, detail=detail))
    # 2. every extreme (stored 0 or 4) has a second coder
    coded = {(r["evaluator"], r["dimension"]) for r in _csv(SECOND) if r.get("coder")}
    ext = [(a["evaluator"], a["dimension"]) for a in d["assessments"] if a["evaluator"] in rids and a["value"] in (0, 4) and not a.get("unevidenced")]
    unc = [f"{e}.{k}" for e, k in ext if (e, k) not in coded]
    out.append(dict(gate="Every extreme has a second coder", ok=not unc, detail=f"{len(ext) - len(unc)} of {len(ext)} extremes second-coded" + (": missing " + ", ".join(unc[:12]) + ("..." if len(unc) > 12 else "") if unc else "")))
    # 3. every ranked organization and every materially-named person has been contacted, with a date
    log = {r["id"]: r for r in _csv(OUTREACH)}
    from .ledger import load_ledger
    L = load_ledger()
    people = material_people(d, L)
    need = [e["id"] for e in ranked] + people
    unsent = [i for i in need if not log.get(LEDGER_ALIAS.get(i, i), log.get(i, {})).get("contacted")]
    need_ids = {LEDGER_ALIAS.get(i, i) for i in need} | set(need)
    extra = sorted(set(log) - need_ids)
    extra_txt = ("; the log lists " + str(len(log)) + " recipients, including "
                 + str(len(extra)) + " outside the gate: "
                 + ", ".join(extra)) if extra else ""
    out.append(dict(gate="Every ranked organization and every materially-named person has been contacted", ok=not unsent, detail=f"{len(need) - len(unsent)} of {len(need)} contacted ({len(ranked)} ranked organizations, {len(people)} materially-named {'person' if len(people) == 1 else 'people'}){extra_txt}"))
    # 4. the default policy is standard and the primary-only view is live
    out.append(dict(gate="Default policy is Standard and the Primary-only view is live", ok=DEFAULT_POLICY == "standard" and "primary" in POLICY_ORDER, detail=f"default {DEFAULT_POLICY}; policies {', '.join(POLICY_ORDER)}"))
    # 5. RULES.md is published and every conflict cites a rule
    rules = (ROOT / "RULES.md").exists()
    bad = []
    for a in d["assessments"]:
        r = derive(a, d["signals"], d["sources"], "leads")
        if r["conflict"] and not (a.get("resolution") or {}).get("rule"): bad.append(f"{a['evaluator']}.{a['dimension']}")
    out.append(dict(gate="RULES.md is published and every conflict cites a rule", ok=rules and not bad, detail=("RULES.md present" if rules else "RULES.md missing") + ("; conflicts without a rule: " + ", ".join(bad) if bad else "; every conflict resolved by rule")))
    # 6. the homepage carries the byline and the competence chip
    tpl = (ROOT / "site" / "template.html").read_text()
    out.append(dict(gate="Homepage carries the byline and the competence chip", ok='id="byline"' in tpl and "Not quality, coverage, or competence" in tpl, detail="checked in site/template.html"))
    return out


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    gs = gates()
    if "--json" in argv:
        print(json.dumps(gs, indent=1)); return 0 if all(g["ok"] for g in gs) else 1
    for g in gs: print(f"[{'PASS' if g['ok'] else 'FAIL'}] {g['gate']}: {g['detail']}")
    ok = all(g["ok"] for g in gs)
    print("gates:", "all pass; a citable tag may be cut" if ok else "not citable yet")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
