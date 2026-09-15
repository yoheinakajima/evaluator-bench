"""python -m bench {build|verify|gates|inspect|scores|industries|timeline|paths|exposure|audit|docket|certificate|review|changelog|outreach|release}"""
from __future__ import annotations
import sys

def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    cmd = argv[0] if argv else "help"
    if cmd == "build":
        from .build import main as m; return m(argv[1:])
    if cmd == "verify":
        from .verify import main as m; return m(argv[1:])
    if cmd == "gates":
        from .gates import main as m; return m(argv[1:])
    if cmd == "inspect":
        from .inspect_cli import main as m; return m(argv[1:])
    if cmd == "scores":
        from .load import load, DIMS
        from .policy import values_by_policy, DEFAULT_POLICY, POLICY_ORDER
        from .score import score, band, coverage, BAND_ORDER
        d = load(strict=False); preset = argv[1] if len(argv) > 1 and not argv[1].startswith("--") else "lab"
        pol = argv[argv.index("--policy") + 1] if "--policy" in argv else DEFAULT_POLICY
        w = d["presets"][preset]["weights"]; vbp = values_by_policy(d)[pol]
        rows = []
        for eid, e in d["evaluators"].items():
            if e.get("status", "ranked") != "ranked": continue
            v = vbp[eid]; s = score(v, w); rows.append((BAND_ORDER[band(v)], -(s if s is not None else -1), e["name"], s, band(v), coverage(v), v))
        print(f"preset {preset}, policy {pol}: band first, then score; coverage is evidenced dimensions of 8")
        for _, _, name, s, b, c, v in sorted(rows):
            print(f"{(str(s) if s is not None else '-'):>3s}  {b:13s} {c}/8  {name:40s} " + " ".join(f"{k}:{'-' if v[k] is None else v[k]}" for k in DIMS))
        if "--by-type" in argv:
            import statistics as st
            for t in sorted({e["type"] for e in d["evaluators"].values()}):
                grp = [vbp[eid] for eid, e in d["evaluators"].items() if e["type"] == t and e.get("status", "ranked") == "ranked"]
                if not grp: continue
                print(f"{t:12s} n={len(grp)} " + " ".join(f"{k}:{st.mean([x[k] for x in grp if x[k] is not None]):.2f}" if any(x[k] is not None for x in grp) else f"{k}:-" for k in DIMS))
        return 0
    if cmd == "release":
        from .release import main as m; return m(argv[1:])
    if cmd == "outreach":
        from .outreach import main as m; return m(argv[1:])
    if cmd == "review":
        from .review import main as m; return m(argv[1:])
    if cmd == "changelog":
        from .changelog import main as m; return m(argv[1:])
    if cmd == "certificate":
        from .certificate import main as m; return m(argv[1:])
    if cmd == "docket":
        from .docket import main as m; return m(argv[1:])
    if cmd == "audit":
        from .audit import main as m; return m(argv[1:])
    if cmd == "exposure":
        from .ledger import main as m; return m(argv[1:])
    if cmd == "paths":
        from .paths import main as m; return m(argv[1:])
    if cmd == "timeline":
        from .timeline import main as m; return m(argv[1:])
    if cmd == "industries":
        from .industries import main as m; return m(argv[1:])
    print(__doc__); return 0 if cmd in ("help", "-h", "--help") else 2

if __name__ == "__main__":
    sys.exit(main())
