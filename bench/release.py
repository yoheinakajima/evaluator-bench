"""Release stage shown across the site.

    python -m bench release --stage preview --until 2026-09-28 --note "..."
    python -m bench release --stage published --tag v0

Writes data/release.json. The build reads it and renders a banner on every
page: in preview, the window end date and how to reply; when published, the
tag and the date, and a pointer to the next annual update.
"""
from __future__ import annotations
import json, sys, datetime
from .load import ROOT

PATH = ROOT / "data" / "release.json"

def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    o = dict(zip(argv[0::2], argv[1::2]))
    stage = o.get("--stage", "preview")
    if stage == "published":
        from .gates import gates
        gs = gates(); failed = [g for g in gs if not g["ok"]]
        if failed and "--override" not in o:
            print("release: refused; the gates for a citable tag are not met (python -m bench gates). Use --override \"reason\" to record an exception.")
            for g in failed: print("  -", g["gate"] + ":", g["detail"])
            return 1
    rec = {"stage": stage, "set_on": datetime.date.today().isoformat(), "window_until": o.get("--until"), "tag": o.get("--tag"), "note": o.get("--note", ""), "gates_override": o.get("--override")}
    PATH.write_text(json.dumps(rec, indent=1) + "\n"); print("wrote", PATH, rec); return 0

if __name__ == "__main__":
    sys.exit(main())
