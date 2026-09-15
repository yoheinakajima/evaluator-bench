"""Right-of-reply packets: everything an evaluator needs to see before a score is published.

    python -m bench outreach [<evaluator-id> ...]   # default: every evaluator whose score moved since the first commit

Writes outreach/<evaluator>.md with the current assessments, the signals and
sources behind them, the ledger rows naming the organization, the open
questions, and how to reply (a PR, an email filed as a signal, or silence,
which is recorded as silence). PROCESS.md section 8: two weeks before a score
is published or moves by more than one anchor.
"""
from __future__ import annotations
import json, sys, pathlib, datetime
from .load import ROOT, load, DIMS
from .ledger import load_ledger
from .verify import LEDGER_ALIAS

OUT = ROOT / "outreach"

def packet(eid: str, d: dict, L: dict) -> str:
    e = d["evaluators"][eid]; dims = {x["key"]: x for x in d["dimensions"]}
    sig = [s for s in d["signals"].values() if s["evaluator"] == eid]
    ass = {a["dimension"]: a for a in d["assessments"] if a["evaluator"] == eid}
    lid = LEDGER_ALIAS.get(eid, eid)
    rows = [t for t in L["transfers"] if lid in (t["from"], t["to"])] + [r for r in L["relationships"] if lid in (r["subject"], r["object"])] + [n for n in L["negatives"] if n["evaluator"] == lid]
    today = datetime.date.today().isoformat()
    o = [f"# Right of reply: {e['name']}", "", f"Prepared {today}. Send date: [to be filled by the sender]. Reply requested within 14 days of sending. This is the complete record Evaluator Bench holds about {e['name']}; nothing else feeds the score.", "",
         "## How to reply", "", "- Correct a fact: open a pull request adding a signal with a source, or email the rows and sources and we file them as a signal marked `source_type: self`.",
         "- Dispute an anchor: say which anchor text you believe applies and why; the rationale field records the disagreement even if the value does not change.",
         "- Publish terms: contract terms on scope, access, and publication rights move the relevant dimensions on their own.",
         "- Silence is recorded as silence, not as agreement.", "", "## Current assessments", ""]
    for k in DIMS:
        a = ass[k]; o.append(f"### {dims[k]['label']}: {a['value']}/4")
        o.append(f"Anchor {a['value']}: {dims[k]['anchors'][a['value']]}"); o.append(f"Rationale: {a['rationale']}")
        for s in sig:
            if s["dimension"] == k:
                srcs = "; ".join(f"{d['sources'][x]['title']} ({d['sources'][x]['url']})" for x in s["sources"] if x in d["sources"])
                o.append(f"- [{s['direction']}] {s['claim']}" + (f' Quote: "{s["quote"]}"' if s.get("quote") else "") + f" Sources: {srcs}")
        for q in a.get("open_questions", []): o.append(f"- Open question: {q}")
        o.append("")
    o.append("## Ledger rows naming the organization"); o.append("")
    for r in rows:
        o.append(f"- {r['row_id']}: " + (f"{r.get('measure')} from {r.get('from')} to {r.get('to')}, {r.get('date')}, {r.get('amount_usd') or 'undisclosed'}: {r.get('purpose')}" if "measure" in r else (f"{r.get('subject')} {r.get('role')} at {r.get('object')}: {r.get('notes')}" if "role" in r else f"negative: {r.get('claim')} [{r.get('searched')}, {r.get('snapshot')}]")) + f" [{r['audit_status']}] {r['source_url']}")
    o += ["", "## What would move the score", "", e.get("what_would_move_the_score", ""), "", "Replies are filed as signals with the date received. Evaluator Bench: https://github.com/yoheinakajima/evaluator-bench"]
    return "\n".join(o) + "\n"

def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    d = load(strict=False); L = load_ledger(); OUT.mkdir(exist_ok=True)
    ids = argv or ["metr", "transluce", "apollo", "ukaisi", "saferai", "averi", "palisade", "caisi", "euaio", "hal"]
    for eid in ids:
        (OUT / f"{eid}.md").write_text(packet(eid, d, L)); print("wrote", OUT / f"{eid}.md")
    return 0

if __name__ == "__main__":
    sys.exit(main())
