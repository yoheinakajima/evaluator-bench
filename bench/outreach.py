"""Record packets for a named organization or person: everything Bench holds about them.

    python -m bench outreach <evaluator-id> [...]    # organizations
    python -m bench outreach --people [<entity-id> ...]   # materially-named people (RULES 12), or the named ones
    python -m bench outreach --all                   # every ranked organization, the watchlist, and materially-named people

Used before a citable tag (every ranked organization and every materially-named
person receives their card and a reply window: RULES.md section 12 and the
gates in bench/gates.py), after first publication when a published score moves by more
than one anchor (PROCESS.md section 8), or whenever someone asks for their record.

Writes outreach/<id>.md and keeps data/outreach-log.csv current: a row per
recipient with the packet path; the contacted, channel, and replied columns
are filled in by the person who sends it. Sending is a human action.
"""
from __future__ import annotations
import csv, json, sys, pathlib, datetime
from .load import ROOT, DATA, load, DIMS
from .ledger import load_ledger
from .verify import LEDGER_ALIAS
from .gates import material_people

OUT = ROOT / "outreach"
LOG = DATA / "outreach-log.csv"
LOG_COLS = ["id", "name", "kind", "packet", "contacted", "channel", "replied", "status", "notes"]


def _rows_naming(lid: str, L: dict) -> list[dict]:
    return ([t for t in L["transfers"] if lid in (t["from"], t["to"])]
            + [r for r in L["relationships"] if lid in (r["subject"], r["object"])]
            + [n for n in L["negatives"] if n["evaluator"] == lid])


def _row_line(r: dict) -> str:
    if "measure" in r:
        return f"- {r['row_id']}: {r.get('measure')} from {r.get('from')} to {r.get('to')}, {r.get('date')}, {r.get('amount_usd') or 'undisclosed'}: {r.get('purpose')} [{r['audit_status']}] {r['source_url']}"
    if "role" in r:
        return f"- {r['row_id']}: {r.get('subject')} {r.get('role')} at {r.get('object')}: {r.get('notes')} [{r['audit_status']}] {r['source_url']}"
    return f"- {r['row_id']}: negative: {r.get('claim')} [{r.get('searched')}, {r.get('snapshot')}] [{r['audit_status']}] {r['source_url']}"


HOW = ["## How to reply", "",
       "- Correct a fact: open a pull request adding a signal with a source, or reply with the rows and sources and we file them as a signal marked `source_type: self`.",
       "- Dispute an anchor: say which anchor text you believe applies and which rule in RULES.md decides it; the resolution field records the disagreement even if the value does not change.",
       "- Publish terms: contract terms on scope, access, and publication rights move the relevant dimensions on their own.",
       "- Silence is recorded as silence, not as agreement.", ""]


def packet(eid: str, d: dict, L: dict) -> str:
    from .policy import derive, DEFAULT_POLICY
    e = d["evaluators"][eid]; dims = {x["key"]: x for x in d["dimensions"]}
    sig = [s for s in d["signals"].values() if s["evaluator"] == eid]
    ass = {a["dimension"]: a for a in d["assessments"] if a["evaluator"] == eid}
    lid = LEDGER_ALIAS.get(eid, eid)
    today = datetime.date.today().isoformat()
    o = [f"# Right of reply: {e['name']}", "", f"Prepared {today}. Reply requested within 14 days of sending. This is the complete record Evaluator Bench holds about {e['name']}; nothing else feeds the score. Values are derived from the signals' bounds under RULES.md; the default site view uses the standard evidence policy (confirmed sources only).", ""]
    o += HOW + ["## Current assessments", ""]
    for k in DIMS:
        a = ass[k]; r = derive(a, d["signals"], d["sources"], DEFAULT_POLICY)
        o.append(f"### {dims[k]['label']}: {a['value']}/4 (standard policy: {'unevidenced' if r['value'] is None else r['value']})")
        o.append(f"Anchor {a['value']}: {dims[k]['anchors'][a['value']]}")
        o.append(f"Derivation: {r['rationale']}")
        if a.get("rationale"): o.append(f"Curator note: {a['rationale']}")
        if a.get("resolution"): o.append(f"Resolution: {a['resolution'].get('rule')} decides {a['resolution'].get('value')}: {a['resolution'].get('note')}")
        for s in sig:
            if s["dimension"] == k:
                srcs = "; ".join(f"{d['sources'][x]['title']} ({d['sources'][x]['url']})" for x in s["sources"] if x in d["sources"])
                b = s.get("bound"); bt = ("caps at " + str(b["cap"]) if b and "cap" in b else ("floors at " + str(b["floor"]) if b and "floor" in b else "informational"))
                o.append(f"- [{s['direction']}, {bt}, {s.get('rule', 'no rule')}] {s['claim']}" + (f' Quote: "{s["quote"]}"' if s.get("quote") else "") + f" Sources: {srcs}")
        for q in a.get("open_questions", []): o.append(f"- Document request: {q}")
        o.append("")
    if e.get("dissent"):
        o += ["## Dissent on the card", "", f"- Lower: {e['dissent']['lower']}", f"- Higher: {e['dissent']['higher']}", ""]
    o += ["## Ledger rows naming the organization", ""] + [_row_line(r) for r in _rows_naming(lid, L)]
    o += ["", "## What would move the score", "", e.get("what_would_move_the_score", ""), "", "Replies are filed as signals with the date received. Evaluator Bench: https://github.com/yoheinakajima/evaluator-bench"]
    return "\n".join(o) + "\n"


def person_packet(pid: str, d: dict, L: dict) -> str:
    E = L["entities"]; p = E[pid]; today = datetime.date.today().isoformat()
    name = p["name"]
    o = [f"# Right of reply: {name}", "", f"Prepared {today}. Reply requested within 14 days of sending. Evaluator Bench records public roles only and asserts no motive (RULES.md section 12). This is everything the ledger and the signals say that names you.", ""]
    o += HOW + ["## Ledger rows", ""] + ([_row_line(r) for r in _rows_naming(pid, L)] or ["- none"])
    mentions = []
    for s in d["signals"].values():
        if name.split(" (")[0] in s["claim"] or any(name.split(" (")[0] in q for a in d["assessments"] if a["evaluator"] == s["evaluator"] for q in a.get("open_questions", [])):
            mentions.append(f"- {s['id']} ({d['evaluators'][s['evaluator']]['name']}, {s['dimension']}, {s['direction']}): {s['claim']}")
    docreq = [f"- {d['evaluators'][a['evaluator']]['name']}, {a['dimension']}: {q}" for a in d["assessments"] for q in a.get("open_questions", []) if name.split(" (")[0] in q]
    o += ["", "## Signals that name you", ""] + (mentions or ["- none"])
    o += ["", "## Document requests", ""] + (docreq or ["- none"])
    o += ["", "Replies are filed as signals with the date received. Evaluator Bench: https://github.com/yoheinakajima/evaluator-bench"]
    return "\n".join(o) + "\n"


def update_log(entries: list[dict]) -> None:
    rows = {}
    if LOG.exists():
        with open(LOG, newline="") as f:
            for r in csv.DictReader(f): rows[r["id"]] = r
    for e in entries:
        r = rows.get(e["id"], {c: "" for c in LOG_COLS}); r.update({k: v for k, v in e.items() if v is not None})
        r.setdefault("status", ""); r["status"] = r["status"] or "packet ready, not sent"
        rows[e["id"]] = r
    with open(LOG, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LOG_COLS); w.writeheader()
        for r in sorted(rows.values(), key=lambda r: (r["kind"], r["name"].lower())): w.writerow({c: r.get(c, "") for c in LOG_COLS})


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    d = load(strict=False); L = load_ledger(); OUT.mkdir(exist_ok=True)
    entries = []
    orgs, people = [], []
    if "--all" in argv:
        orgs = list(d["evaluators"]); people = material_people(d, L)
    elif "--people" in argv:
        named = [a for a in argv if a != "--people"]
        people = named or material_people(d, L)
    else:
        orgs = argv
    if not orgs and not people: print("usage: bench outreach <evaluator-id> [...] | --people [<entity-id> ...] | --all"); return 2
    for eid in orgs:
        p = OUT / f"{eid}.md"; p.write_text(packet(eid, d, L)); print("wrote", p)
        entries.append(dict(id=eid, name=d["evaluators"][eid]["name"], kind="organization", packet=str(p.relative_to(ROOT))))
    for pid in people:
        p = OUT / f"person-{pid}.md"; p.write_text(person_packet(pid, d, L)); print("wrote", p)
        entries.append(dict(id=pid, name=L["entities"][pid]["name"], kind="person", packet=str(p.relative_to(ROOT))))
    update_log(entries); print("log:", LOG)
    return 0


if __name__ == "__main__":
    sys.exit(main())
