"""Machine review of a contribution: re-fetch cited sources, check spans, judge support.

    python -m bench review --base origin/main [--out review.md]

For every signal added or changed since --base, the reviewer:
  1. fetches each cited source URL (records SHA-256 of the response),
  2. checks that the signal's `quote` appears verbatim in the fetched text,
  3. asks a model whether the fetched text supports the claim (pass / qualified / unsupported),
  4. checks assessment changes cite a signal on that dimension.
Without ANTHROPIC_API_KEY it runs steps 1, 2 and 4 and marks step 3 "not run".
The report is advisory: a maintainer merges. It is the rough machine half of
the certification described in paper/CERTIFICATION.md.
"""
from __future__ import annotations
import json, os, re, subprocess, sys, hashlib, urllib.request, html
from .load import ROOT, load

def _git(*a): return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout

def changed_signals(base: str) -> list[dict]:
    d = load(strict=False); out = []
    for path in _git("diff", "--name-only", base, "--", "data/signals").split():
        old = _git("show", f"{base}:{path}")
        try: old_ids = {s["id"]: s for s in json.loads(old)} if old.strip() else {}
        except json.JSONDecodeError: old_ids = {}
        for s in json.loads((ROOT / path).read_text()):
            if s["id"] not in old_ids or old_ids[s["id"]] != s: out.append(s)
    return out

def changed_assessments(base: str) -> list[tuple]:
    out = []
    for path in _git("diff", "--name-only", base, "--", "data/assessments").split():
        old = _git("show", f"{base}:{path}")
        old_v = {a["dimension"]: a for a in json.loads(old)} if old.strip() else {}
        for a in json.loads((ROOT / path).read_text()):
            o = old_v.get(a["dimension"])
            if not o or o["value"] != a["value"]: out.append((a["evaluator"], a["dimension"], o["value"] if o else None, a["value"], a["signals"]))
    return out

def fetch_text(url: str) -> tuple[str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "evaluator-bench-review/0.1"})
    with urllib.request.urlopen(req, timeout=30) as r: raw = r.read()
    text = re.sub(r"<[^>]+>", " ", raw.decode("utf-8", "ignore")); text = html.unescape(re.sub(r"\s+", " ", text))
    return text, hashlib.sha256(raw).hexdigest()

def ask_model(claim: str, quote: str, text: str) -> str:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key: return "not run (no ANTHROPIC_API_KEY)"
    body = {"model": "claude-sonnet-4-6", "max_tokens": 300, "messages": [{"role": "user", "content":
        f"You are checking an evidence ledger. Source text (truncated):\n\n{text[:12000]}\n\nClaim: {claim}\nQuoted span: {quote}\n\nAnswer with one word first (pass, qualified, or unsupported), then one sentence on why. 'pass' means the source text supports the claim as stated; 'qualified' means it supports a narrower version; 'unsupported' means it does not."}]}
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=json.dumps(body).encode(), headers={"content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01"})
    with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read())["content"][0]["text"].strip()

def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    base = argv[argv.index("--base") + 1] if "--base" in argv else "HEAD~1"
    out = argv[argv.index("--out") + 1] if "--out" in argv else None
    d = load(strict=False); lines = ["## Machine review", f"base: `{base}`", ""]
    sigs = changed_signals(base); lines.append(f"{len(sigs)} signal(s) added or changed")
    for s in sigs:
        lines.append(f"\n### {s['id']} ({s['dimension']}, {s['direction']})\n{s['claim']}")
        for sid in s["sources"]:
            src = d["sources"].get(sid)
            if not src: lines.append(f"- {sid}: MISSING source record"); continue
            try:
                text, sha = fetch_text(src["url"]); lines.append(f"- {src['url']} fetched, sha256 {sha[:12]}")
                q = s.get("quote", "")
                lines.append(f"  - quote {'FOUND' if q and q in text else ('NOT FOUND' if q else 'missing: add a quote')}")
                lines.append(f"  - support: {ask_model(s['claim'], q, text)}")
            except Exception as ex: lines.append(f"- {src['url']}: fetch failed ({type(ex).__name__})")
    ch = changed_assessments(base); lines.append(f"\n{len(ch)} assessment change(s)")
    for ev, dim, old, new, sig_ids in ch:
        ok = any(x["id"] in sig_ids for x in sigs if x["evaluator"] == ev and x["dimension"] == dim)
        lines.append(f"- {ev}.{dim}: {old} -> {new}: " + ("cites a new or changed signal on this dimension" if ok else "NO new signal on this dimension in this PR"))
    report = "\n".join(lines); print(report)
    if out: (ROOT / out).write_text(report)
    return 0

if __name__ == "__main__":
    sys.exit(main())
