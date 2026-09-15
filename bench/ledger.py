"""Ledger: row-level money and role records, and the exposure projection.

Exposure distance d(e) for an entity e:
  0  e is a frontier lab
  1  e holds a direct tie to a lab: investor, observer, board, employee, founder, contractor
  k  otherwise 1 + min over (principals of e, funders of e) of their distance; unattributed if none

An evaluator's inflows are then bucketed by the distance of their source. Amounts
are summed only within one measure and one hop bucket. Undisclosed amounts count
as rows, never as dollars.
"""
from __future__ import annotations
import csv, json, sys, pathlib
from collections import defaultdict
from .load import DATA

LEDGER = DATA / "ledger"
MEASURES = {"grant", "recommendation", "commitment", "transfer", "daf_grant", "in_kind", "investment", "contract"}
ROLES = {"investor", "observer", "board", "advisor", "employee", "founder", "principal", "pays", "contractor", "donor", "office_host", "parent"}
SOURCE_TYPES = {"filing", "index", "ledger", "self", "press"}
AUDIT = {"imported", "confirmed", "differs", "unverifiable"}
DIRECT_LAB_TIES = {"investor", "observer", "board", "employee", "founder", "contractor"}
CONTROL_ROLES = {"principal", "pays", "parent", "investor"}   # influence flows subject -> object

def _read(name: str) -> list[dict]:
    p = LEDGER / name
    if not p.exists(): return []
    with open(p, newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]

def load_ledger() -> dict:
    return dict(entities={e["id"]: e for e in _read("entities.csv")}, transfers=_read("transfers.csv"),
                relationships=_read("relationships.csv"), negatives=_read("negatives.csv"))

def validate(L: dict) -> list[str]:
    errs = []; E = L["entities"]
    for t in L["transfers"]:
        for k in ("from", "to"):
            if t[k] not in E: errs.append(f"L1 transfer {t['row_id']}: unknown entity {t[k]}")
        if t["measure"] not in MEASURES: errs.append(f"L1 transfer {t['row_id']}: bad measure {t['measure']}")
        if not t["source_url"].startswith("http"): errs.append(f"L1 transfer {t['row_id']}: source_url")
        if t["source_type"] not in SOURCE_TYPES: errs.append(f"L1 transfer {t['row_id']}: source_type")
        if t["audit_status"] not in AUDIT: errs.append(f"L1 transfer {t['row_id']}: audit_status")
        if t["amount_usd"] and not t["amount_usd"].replace(".", "").isdigit(): errs.append(f"L1 transfer {t['row_id']}: amount_usd must be numeric or empty")
    for r in L["relationships"]:
        for k in ("subject", "object"):
            if r[k] not in E: errs.append(f"L2 relationship {r['row_id']}: unknown entity {r[k]}")
        if r["role"] not in ROLES: errs.append(f"L2 relationship {r['row_id']}: bad role {r['role']}")
        if r["audit_status"] not in AUDIT: errs.append(f"L2 relationship {r['row_id']}: audit_status")
    for n in L["negatives"]:
        if n["evaluator"] not in E: errs.append(f"L3 negative {n['row_id']}: unknown evaluator {n['evaluator']}")
        if n["source_type"] not in SOURCE_TYPES: errs.append(f"L3 negative {n['row_id']}: source_type")
        if not n["snapshot"]: errs.append(f"L3 negative {n['row_id']}: snapshot date required")
    return errs

def distances(L: dict) -> dict[str, float]:
    E = L["entities"]; d: dict[str, float] = {}
    labs = {i for i, e in E.items() if e["kind"] == "lab"}
    for i in labs: d[i] = 0
    for r in L["relationships"]:
        if r["role"] in DIRECT_LAB_TIES and r["object"] in labs:
            d[r["subject"]] = min(d.get(r["subject"], 9e9), 1)
    # influence edges: who can move money or control into e
    into: dict[str, set[str]] = defaultdict(set)
    for r in L["relationships"]:
        if r["role"] in CONTROL_ROLES: into[r["object"]].add(r["subject"])
    for t in L["transfers"]:
        into[t["to"]].add(t["from"])
    # a person inherits closeness from organizations they lead or founded (one step further away)
    via_org = defaultdict(set)
    for r in L["relationships"]:
        if r["role"] in {"principal", "founder", "board", "employee"} and E[r["subject"]]["kind"] == "person" and r["object"] not in labs:
            via_org[r["subject"]].add(r["object"])
    changed = True
    while changed:
        changed = False
        for e in E:
            if e in labs: continue
            best = d.get(e, 9e9)
            for src in into.get(e, ()):
                if src in d and d[src] + 1 < best: best = d[src] + 1
            for org in via_org.get(e, ()):
                if org in d and d[org] + 1 < best: best = d[org] + 1
            if best < d.get(e, 9e9): d[e] = best; changed = True
    return d

def exposure(L: dict | None = None) -> list[dict]:
    L = L or load_ledger(); E = L["entities"]; d = distances(L)
    out = []
    for eid, e in E.items():
        if e["kind"] != "evaluator": continue
        rows = [t for t in L["transfers"] if t["to"] == eid]
        buckets: dict[str, dict] = {}
        for t in rows:
            hop = d.get(t["from"]); key = "public" if E[t["from"]]["kind"] == "public" else ("unattributed" if hop is None else f"hop{int(hop)}")
            b = buckets.setdefault(key, {"rows": 0, "by_measure": defaultdict(float), "undisclosed": 0, "sources": []})
            b["rows"] += 1; b["sources"].append(t["from"])
            if t["amount_usd"]: b["by_measure"][t["measure"]] += float(t["amount_usd"])
            else: b["undisclosed"] += 1
        # second-hop coverage: for each source of an inflow, does the ledger say anything about who is behind it?
        behind = defaultdict(int)
        for r in L["relationships"]:
            if r["role"] in CONTROL_ROLES | {"employee", "founder"}: behind[r["object"]] += 1
        for t2 in L["transfers"]: behind[t2["to"]] += 1
        srcs = sorted({t["from"] for t in rows})
        traced = [s for s in srcs if behind.get(s, 0) > 0 or E[s]["kind"] in ("lab", "public") or d.get(s, 9e9) <= 1]
        ties = [r for r in L["relationships"] if r["object"] == eid and r["role"] in {"board", "advisor", "donor", "investor", "office_host"} and d.get(r["subject"], 9e9) <= 2]
        negs = [n for n in L["negatives"] if n["evaluator"] == eid]
        out.append(dict(id=eid, name=e["name"], kind_note=e.get("notes",""), inflow_rows=len(rows),
                        buckets={k: {"rows": v["rows"], "undisclosed": v["undisclosed"], "by_measure": dict(v["by_measure"]), "sources": sorted(set(v["sources"]))} for k, v in sorted(buckets.items())},
                        lab_tied_seats=[dict(person=r["subject"], role=r["role"] + (" (former)" if r.get("end") else ""), via=E[r["subject"]]["name"], distance=int(d[r["subject"]]), status=r["audit_status"]) for r in ties],
                        negatives=[dict(claim=n["claim"], searched=n["searched"], snapshot=n["snapshot"], status=n["audit_status"]) for n in negs],
                        confirmed_rows=sum(1 for t in rows if t["audit_status"] == "confirmed"),
                        second_hop=dict(sources=len(srcs), traced=len(traced), untraced=[E[s]["name"] for s in srcs if s not in traced])))
    return out

def main(argv=None) -> int:
    L = load_ledger(); errs = validate(L)
    if errs:
        print("ledger: problems"); [print("  -", e) for e in errs]; return 1
    d = distances(L)
    print("Exposure distance (0 lab, 1 direct tie, k via principals or funders):")
    for e, v in sorted(d.items(), key=lambda x: (x[1], x[0])): print(f"  {int(v)}  {L['entities'][e]['name']}")
    print("\nEvaluator inflows by hop (amounts summed only within one measure; undisclosed counted as rows):")
    ex = exposure(L)
    for x in ex:
        if not x["inflow_rows"] and not x["lab_tied_seats"]: continue
        print(f"  {x['name']}  ({x['inflow_rows']} rows, {x['confirmed_rows']} confirmed)")
        for k, b in x["buckets"].items():
            amts = ", ".join(f"{m} ${v/1e6:.1f}M" for m, v in b["by_measure"].items())
            print(f"     {k:12s} {b['rows']} rows{(' (' + str(b['undisclosed']) + ' undisclosed)') if b['undisclosed'] else ''}  {amts}  from {', '.join(b['sources'])}")
        for s in x["lab_tied_seats"]: print(f"     tie: {s['via']} ({s['role']}, distance {s['distance']}, {s['status']})")
        sh = x["second_hop"]; print(f"     second hop traced for {sh['traced']}/{sh['sources']} sources" + (f"; untraced: {', '.join(sh['untraced'])}" if sh['untraced'] else ""))
        for n in x["negatives"]: print(f"     none found: {n['claim']} [{n['searched']}, {n['snapshot']}, {n['status']}]")
    evs = [x for x in ex]
    coef = sum(1 for x in evs if any("coefficient" in b["sources"] for b in x["buckets"].values()))
    near = sum(1 for x in evs if any(k in ("hop0", "hop1") for k in x["buckets"]))
    rows = sum(x["inflow_rows"] for x in evs); conf = sum(x["confirmed_rows"] for x in evs)
    print(f"\nPopulation: {len(evs)} evaluators; {coef} with Coefficient Giving inflows; {near} with an inflow from a lab or a lab-tied party; {conf}/{rows} inflow rows confirmed.")
    if "--json" in (argv or []):
        (DATA.parent / "dist").mkdir(exist_ok=True)
        (DATA.parent / "dist" / "exposure.json").write_text(json.dumps(dict(distances=d, evaluators=ex), indent=1))
        print("wrote dist/exposure.json")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
