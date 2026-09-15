"""python -m bench {build|verify|inspect|scores|industries|timeline|paths|exposure|audit|docket|certificate|review|changelog|outreach|release}"""
from __future__ import annotations
import sys

def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    cmd = argv[0] if argv else "help"
    if cmd == "build":
        from .build import main as m; return m(argv[1:])
    if cmd == "verify":
        from .verify import main as m; return m(argv[1:])
    if cmd == "inspect":
        from .inspect_cli import main as m; return m(argv[1:])
    if cmd == "scores":
        from .load import load; from .score import table
        d = load(strict=False); preset = argv[1] if len(argv) > 1 else "lab"
        t = table(d["assessments"], d["presets"][preset]["weights"])
        for eid, v in sorted(t.items(), key=lambda x: -x[1]): print(f"{v:3d}  {d['evaluators'][eid]['name']}")
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
