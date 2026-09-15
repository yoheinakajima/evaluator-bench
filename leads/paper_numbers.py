"""Print the Dataset A numbers for paper section 5.5 and the abstract from the current build.

    python leads/paper_numbers.py

Reads dist/bench.json (so run after `python -m bench build`). Standard policy, lab preset,
ranked population only. Prints a drafted section 5.5 for the curator to paste and edit.
"""
import json, pathlib, statistics as st
from collections import Counter
ROOT = pathlib.Path(__file__).resolve().parents[1]
B = json.loads((ROOT / "dist" / "bench.json").read_text())
DIMS = ["F", "G", "P", "A", "S", "R", "M", "X"]
LABEL = {"F": "funding", "G": "governance", "P": "personnel", "A": "access", "S": "scope control", "R": "publication rights", "M": "method transparency", "X": "role incompatibility"}
ranked = [e for e in B["evaluators"] if e.get("status", "ranked") == "ranked"]
pol = B["default_policy"]
def vals(e, p=pol): return e["values_by_policy"][p]
def mean(xs): xs = [x for x in xs if x is not None]; return (sum(xs) / len(xs)) if xs else None

rows = sorted(ranked, key=lambda e: ({"clear": 0, "conditional": 1, "disqualifying": 2, "unevidenced": 3}[e["band"]], -(e["scores"]["lab"] if e["scores"]["lab"] is not None else -1), e["name"]))
bands = Counter(e["band"] for e in ranked)
print("== band-first table (lab preset, standard policy) ==")
for e in rows: print(f"{e['scores']['lab'] if e['scores']['lab'] is not None else '-':>3}  {e['band']:13s} {e['coverage']}/8  {e['name']}")
print("\nbands:", dict(bands))
means = {k: mean([vals(e)[k] for e in ranked]) for k in DIMS}
print("dimension means (standard):", {k: round(v, 2) if v is not None else None for k, v in means.items()})
means_leads = {k: mean([vals(e, "leads")[k] for e in ranked]) for k in DIMS}
print("dimension means (leads):", {k: round(v, 2) for k, v in means_leads.items()})
dark = {k: sum(1 for e in ranked if vals(e)[k] is None) for k in DIMS}
print("unevidenced per dimension (standard):", dark, "total", sum(dark.values()))
print("\nby type (standard):")
for t in sorted({e["type"] for e in ranked}):
    g = [e for e in ranked if e["type"] == t]
    print(f"  {t:12s} n={len(g)} " + " ".join(f"{k}:{mean([vals(e)[k] for e in g]):.2f}" if mean([vals(e)[k] for e in g]) is not None else f"{k}:-" for k in DIMS))
print("\nby list group (standard):")
for grp in B["group_order"]:
    g = [e for e in ranked if e["list_group"] == grp]
    print(f"  {grp:12s} n={len(g)} bands={dict(Counter(e['band'] for e in g))} " + " ".join(f"{k}:{mean([vals(e)[k] for e in g]):.2f}" if mean([vals(e)[k] for e in g]) is not None else f"{k}:-" for k in DIMS))
sig = [s for e in ranked for s in e["signals"]]
print("\nsignals (ranked):", len(sig), "for", sum(1 for s in sig if s["direction"] == "for"), "against", sum(1 for s in sig if s["direction"] == "against"), "with quote", sum(1 for s in sig if s.get("quote")))
srcs = {x for s in sig for x in s["sources"]}
print("unique sources (ranked):", len(srcs), "self", sum(1 for x in srcs if B["sources"][x].get("source_type") == "self"), "tier1", sum(1 for x in srcs if B["sources"][x].get("source_type") in ("filing", "index")))
held = [(e["id"], k) for e in ranked for k in DIMS if e["assessments"][k]["derived"]["leads"]["h"]]
print("assessments held by C14/C15/C16 (leads):", len(held))
conf = [(e["id"], k) for e in ranked for k in DIMS if e["assessments"][k]["derived"]["leads"]["c"]]
print("conflicts resolved by rule:", len(conf), conf)
ext = [(e["id"], k, e["values"][k]) for e in ranked for k in DIMS if e["values"][k] in (0, 4)]
print("extremes (stored):", len(ext), ext)
print("\nunder each policy, unevidenced ranked assessments:")
for p in B["policy_order"]:
    print(f"  {p:17s}", sum(1 for e in ranked for k in DIMS if e['values_by_policy'][p][k] is None), "of", len(ranked) * 8)
low = [e for e in ranked if e["values"]["F"] is not None and e["values"]["F"] <= 2]
print("\nfunding <= 2 (leads):", len(low))
top = rows[:5]; bottom = rows[-3:]
print("\n== drafted 5.5 ==")
order = sorted(means.items(), key=lambda kv: -(kv[1] if kv[1] is not None else -1))
print(f"Under the lab-procurement preset and the standard evidence policy, {bands.get('clear', 0)} of {len(ranked)} ranked organizations are in the clear band, {bands.get('conditional', 0)} carry a conditional floor (an evidenced 1), and {bands.get('disqualifying', 0)} carry a disqualifying floor (an evidenced 0). Within the clear band the highest scores are {', '.join(f'{e['name']} ({e['scores']['lab']}, {e['coverage']}/8 evidenced)' for e in top)}; the disqualifying band holds {', '.join(f'{e['name']} ({e['scores']['lab']})' for e in rows if e['band'] == 'disqualifying')}. "
      f"Across the {len(ranked)}, mean values by dimension under the standard policy are " + ", ".join(f"{LABEL[k]} {v:.2f}" for k, v in order if v is not None) + f"; {sum(dark.values())} of {len(ranked) * 8} assessments are unevidenced under that policy and excluded from the means. "
      f"Under leads included the means are " + ", ".join(f"{LABEL[k]} {v:.2f}" for k, v in sorted(means_leads.items(), key=lambda kv: -kv[1])) + ".")
