"""Re-fetch cited sources, hash the response, record a verdict skeleton.

    python -m bench audit T12 R10 N01   # or --all-imported

Writes data/artifacts.csv (row_id, url, fetched_at, sha256, status, bytes) and
prints a markdown table to paste into paper/audits/. Verdicts are entered by a
person after reading; this script only proves what was fetched and when.
Runs where the network allows; inside restricted sandboxes it records the
attempt and the error.
"""
from __future__ import annotations
import csv, hashlib, sys, datetime, urllib.request, pathlib
from .ledger import load_ledger
from .load import DATA

ART = DATA / "artifacts.csv"

def fetch(url: str, timeout: int = 20) -> tuple[str, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": "evaluator-bench-audit/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return str(r.status), r.read()

def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    L = load_ledger()
    rows = {r["row_id"]: r for r in L["transfers"] + L["relationships"] + L["negatives"]}
    ids = [r for r in rows if rows[r]["audit_status"] == "imported"] if "--all-imported" in argv else [a for a in argv if a in rows]
    if not ids: print("usage: bench audit <row ids> | --all-imported"); return 2
    exists = ART.exists()
    with open(ART, "a", newline="") as f:
        w = csv.writer(f)
        if not exists: w.writerow(["row_id", "url", "fetched_at", "sha256", "status", "bytes"])
        print("| row | url | status | sha256 |\n|---|---|---|---|")
        for rid in ids:
            url = rows[rid]["source_url"]; ts = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"
            try:
                status, body = fetch(url); h = hashlib.sha256(body).hexdigest(); n = len(body)
            except Exception as ex:  # network refused, 403, etc.
                status, h, n = f"error: {type(ex).__name__}", "", 0
            w.writerow([rid, url, ts, h, status, n]); print(f"| {rid} | {url} | {status} | {h[:12]} |")
    print(f"\nrecorded in {ART}; add verdicts to paper/audits/ after reading each page")
    return 0

if __name__ == "__main__":
    sys.exit(main())
