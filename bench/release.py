"""Release stage shown across the site.

    python -m bench release --stage preview --until 2026-09-28 --note "..."
    python -m bench release --stage published --tag v0
    python -m bench release --stage preview --until 2026-09-29 --packets-sent 2026-09-15   # only after the packets were sent

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
    prev = json.loads(PATH.read_text()) if PATH.exists() else {}
    rec = {"stage": stage, "set_on": datetime.date.today().isoformat(), "window_until": o.get("--until"), "tag": o.get("--tag"), "note": o.get("--note", ""),
           "packets_sent": o.get("--packets-sent", prev.get("packets_sent"))}   # date the right-of-reply packets were sent; null until a person sends them
    PATH.write_text(json.dumps(rec, indent=1) + "\n"); print("wrote", PATH, rec); return 0

if __name__ == "__main__":
    sys.exit(main())
