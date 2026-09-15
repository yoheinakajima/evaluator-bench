"""Stage ladder: where each assurance regime is, and where frontier AI is.

Seven stages, reached when a milestone of the listed kind first appears:

  S1 voluntary   voluntary_assurance
  S2 trigger     trigger
  S3 mandate     mandate
  S4 standards   standards
  S5 oversight   accreditation                    (an auditor of auditors)
  S6 independence independence_rule, delegation_reform, payer_reform
  (payer_shift, delegation, rollback are recorded but do not advance a stage)
  S7 access      access_expansion, publication_rule

Outputs a JSON table and a deterministic SVG. Used by build to put the
figure on the site and in paper/figures/.
"""
from __future__ import annotations
import json, pathlib, sys
from .load import DATA, ROOT

STAGES = [
    ("S1", "Voluntary", {"voluntary_assurance"}),
    ("S2", "Trigger", {"trigger"}),
    ("S3", "Mandate", {"mandate"}),
    ("S4", "Standards", {"standards"}),
    ("S5", "Oversight", {"accreditation"}),
    ("S6", "Independence", {"independence_rule", "delegation_reform", "payer_reform"}),
    ("S7", "Access", {"access_expansion", "publication_rule"}),
]
ORDER = ["financial-audit","ship-classification","boilers","product-safety","pharmaceuticals","aviation","credit-ratings",
         "nuclear","auto-safety","food-safety","cybersecurity-assurance","sustainability-assurance","dietary-supplements",
         "crypto-reserves","platform-algorithm-audits","frontier-ai"]

def ladder() -> list[dict]:
    rows = []
    regimes = {p.stem: json.loads(p.read_text()) for p in (DATA / "industries").glob("*.json")}
    for rid in ORDER + sorted(set(regimes) - set(ORDER)):
        if rid not in regimes: continue
        o = regimes[rid]; ms = o["milestones"]
        stages = {}
        for code, label, kinds in STAGES:
            ys = [m["year"] for m in ms if m["kind"] in kinds]
            stages[code] = min(ys) if ys else None
        first = min(m["year"] for m in ms)
        reached = [c for c, _, _ in STAGES if stages[c] is not None]
        rollback = any(m["kind"] == "rollback" for m in ms)
        delegation = any(m["kind"] == "delegation" for m in ms)
        rows.append(dict(id=rid, name=o["name"], first=first, stages=stages, reached=len(reached),
                         highest=(reached[-1] if reached else None), rollback=rollback, delegation=delegation,
                         span=max(m["year"] for m in ms) - first,
                         voluntary_to_mandate=(stages["S3"] - stages["S1"]) if stages["S1"] and stages["S3"] and stages["S3"] >= stages["S1"] else None,
                         start_to_independence=(stages["S6"] - first) if stages["S6"] else None))
    return rows

def svg(rows: list[dict]) -> str:
    pad_l, pad_t, cw, rh, name_w = 12, 84, 92, 26, 300
    n = len(rows); w = pad_l + name_w + cw * len(STAGES) + 200; h = pad_t + rh * n + 44
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="Instrument Sans, system-ui, sans-serif" font-size="12">',
         f'<rect width="{w}" height="{h}" fill="#F4F6F3"/>',
         f'<text x="{pad_l}" y="22" font-size="16" fill="#15222E">Stage ladder: year each assurance regime first reached each stage</text>',
         f'<text x="{pad_l}" y="40" fill="#5E6B76">Cell shade: age of the regime when the stage arrived. Light under 10 years, mid 10 to 50, dark over 50.</text>',
         f'<text x="{pad_l}" y="54" fill="#5E6B76">Red dot: a rollback occurred. Amber ring: the assessed party absorbed the assessment function at some point.</text>']
    for j, (code, label, _) in enumerate(STAGES):
        x = pad_l + name_w + j * cw
        o.append(f'<text x="{x + cw/2}" y="{pad_t - 6}" text-anchor="middle" fill="#15222E" font-weight="600">{label}</text>')
    o.append(f'<text x="{pad_l + name_w + len(STAGES)*cw + 12}" y="{pad_t - 6}" fill="#15222E" font-weight="600">Years, voluntary to mandate</text>')
    for i, r in enumerate(rows):
        y = pad_t + i * rh
        ai = r["id"] == "frontier-ai"
        if ai: o.append(f'<rect x="{pad_l-4}" y="{y-2}" width="{w-2*pad_l+8}" height="{rh}" fill="#DCEFEA" rx="3"/>')
        o.append(f'<text x="{pad_l}" y="{y + 16}" fill="#15222E" font-weight="{"600" if ai else "400"}">{r["name"][:40]}</text>')
        for j, (code, _, _) in enumerate(STAGES):
            x = pad_l + name_w + j * cw; yr = r["stages"][code]
            if yr is None:
                o.append(f'<rect x="{x+2}" y="{y+2}" width="{cw-4}" height="{rh-6}" fill="none" stroke="#D3DAD6" stroke-dasharray="3 3"/>')
                continue
            gap = max(0, yr - r["first"])
            fill = "#DCEFEA" if gap < 10 else ("#8CC5BB" if gap <= 50 else "#0F766E")
            tcol = "#15222E" if gap <= 50 else "#FFFFFF"
            o.append(f'<rect x="{x+2}" y="{y+2}" width="{cw-4}" height="{rh-6}" fill="{fill}" rx="2"/>')
            o.append(f'<text x="{x + cw/2}" y="{y + 16}" text-anchor="middle" fill="{tcol}">{yr}</text>')
        xr = pad_l + name_w + len(STAGES) * cw + 12
        vm = r["voluntary_to_mandate"]
        if vm is not None:
            o.append(f'<rect x="{xr}" y="{y+6}" width="{max(2, min(120, vm*1.2))}" height="{rh-14}" fill="#0F766E" opacity="0.7"/>')
            o.append(f'<text x="{xr + max(2, min(120, vm*1.2)) + 4}" y="{y + 16}" fill="#5E6B76">{vm} y</text>')
        marks = []
        if r["rollback"]: marks.append(f'<circle cx="{pad_l + name_w - 14}" cy="{y + 12}" r="3" fill="#9B2C2C"/>')
        if r["delegation"]: marks.append(f'<circle cx="{pad_l + name_w - 26}" cy="{y + 12}" r="4" fill="none" stroke="#B7791F" stroke-width="2"/>')
        o += marks
    o.append(f'<text x="{pad_l}" y="{h - 14}" fill="#5E6B76">Source: data/industries/ (seed, secondary sources). Generated by bench.timeline; regenerate with python -m bench build.</text>')
    o.append('</svg>')
    return "\n".join(o)

def write(dist: pathlib.Path) -> list[dict]:
    rows = ladder()
    dist.mkdir(exist_ok=True)
    (dist / "timeline.json").write_text(json.dumps(rows, indent=1) + "\n")
    s = svg(rows)
    (dist / "timeline.svg").write_text(s)
    figs = ROOT / "paper" / "figures"; figs.mkdir(parents=True, exist_ok=True)
    (figs / "stage-ladder.svg").write_text(s)
    return rows

def main(argv=None) -> int:
    rows = ladder()
    hdr = f"{'regime':36s} " + " ".join(f"{l[:7]:>7s}" for _, l, _ in STAGES) + f" {'reached':>7s} {'v->m':>5s}"
    print(hdr)
    for r in rows:
        cells = " ".join(f"{(str(r['stages'][c]) if r['stages'][c] else '.'):>7s}" for c, _, _ in STAGES)
        vm = "" if r["voluntary_to_mandate"] is None else str(r["voluntary_to_mandate"])
        flags = ("R" if r["rollback"] else "") + ("D" if r["delegation"] else "")
        print(f"{r['name'][:36]:36s} {cells} {r['reached']:>5d}/7 {vm:>5s} {flags}")
    if "--write" in (argv or []):
        write(ROOT / "dist"); print("wrote dist/timeline.json, dist/timeline.svg, paper/figures/stage-ladder.svg")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
