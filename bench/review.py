"""Machine review of a contribution: re-fetch cited sources, check spans, judge support.

    python -m bench review --base origin/main [--out review.md]
    python -m bench review --all [--out review.md]      # every signal that carries a quote, whole corpus

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
        # A deletion is part of the PR diff but has no working-tree payload to review.
        if not (ROOT / path).is_file():
            continue
        old = _git("show", f"{base}:{path}")
        try: old_ids = {s["id"]: s for s in json.loads(old)} if old.strip() else {}
        except json.JSONDecodeError: old_ids = {}
        for s in json.loads((ROOT / path).read_text()):
            if s["id"] not in old_ids or old_ids[s["id"]] != s: out.append(s)
    return out

def changed_assessments(base: str) -> list[tuple]:
    out = []
    for path in _git("diff", "--name-only", base, "--", "data/assessments").split():
        # Deletions have no current assessment to compare or review.
        if not (ROOT / path).is_file():
            continue
        old = _git("show", f"{base}:{path}")
        old_v = {a["dimension"]: a for a in json.loads(old)} if old.strip() else {}
        for a in json.loads((ROOT / path).read_text()):
            o = old_v.get(a["dimension"])
            if not o or o["value"] != a["value"]: out.append((a["evaluator"], a["dimension"], o["value"] if o else None, a["value"], a["signals"]))
    return out

def fetch_text(url: str) -> tuple[str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; evaluator-bench-review/0.2; +https://evaluatorbench.com)"})
    with urllib.request.urlopen(req, timeout=30) as r: raw = r.read(); ctype = r.headers.get("Content-Type", "")
    if raw[:5] == b"%PDF-" or "application/pdf" in ctype:
        # PDF sources: use poppler's pdftotext when installed; otherwise the span cannot be checked here
        try:
            out = subprocess.run(["pdftotext", "-layout", "-", "-"], input=raw, capture_output=True, timeout=60).stdout.decode("utf-8", "ignore")
            text = html.unescape(re.sub(r"\s+", " ", out.replace("\u200b", "")))
        except (FileNotFoundError, subprocess.TimeoutExpired):
            text = ""
        return text, hashlib.sha256(raw).hexdigest()
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw.decode("utf-8", "ignore"), flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text); text = html.unescape(re.sub(r"\s+", " ", text))
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
    d = load(strict=False); lines = ["## Machine review", f"base: `{base}`" if "--all" not in argv else "scope: every signal with a quote", ""]
    sigs = [s for s in d["signals"].values() if s.get("quote")] if "--all" in argv else changed_signals(base)
    lines.append(f"{len(sigs)} signal(s) " + ("checked" if "--all" in argv else "added or changed"))
    verdicts = {"found": 0, "not_found": 0, "fetch_failed": 0, "no_quote": 0}
    for s in sigs:
        lines.append(f"\n### {s['id']} ({s['dimension']}, {s['direction']})\n{s['claim']}")
        q = s.get("quote", ""); found_on = None; failed = 0
        order = ([s["quote_source"]] if s.get("quote_source") in s["sources"] else []) + [x for x in s["sources"] if x != s.get("quote_source")]
        for sid in order:
            src = d["sources"].get(sid)
            if not src: lines.append(f"- {sid}: MISSING source record"); continue
            try:
                text, sha = fetch_text(src["url"]); lines.append(f"- {sid} {src['url']} fetched, sha256 {sha[:12]}" + (" (PDF)" if src["url"].lower().endswith(".pdf") else ""))
                if q and q in text and found_on is None:
                    found_on = sid; lines.append(f"  - quote FOUND on {sid}")
                    lines.append(f"  - support: {ask_model(s['claim'], q, text)}")
            except Exception as ex: failed += 1; lines.append(f"- {sid} {src['url']}: fetch failed ({type(ex).__name__})")
        if not q: verdicts["no_quote"] += 1; lines.append("- verdict: no quote; add a span")
        elif found_on: verdicts["found"] += 1
        elif failed and failed == len(order): verdicts["fetch_failed"] += 1; lines.append("- verdict: quote NOT CHECKABLE (every cited page failed to fetch)")
        else: verdicts["not_found"] += 1; lines.append("- verdict: quote NOT FOUND on any fetched page" + (f"; {failed} page(s) failed to fetch" if failed else ""))
    lines.append(f"\nverdicts: {verdicts['found']} found, {verdicts['not_found']} not found, {verdicts['fetch_failed']} not checkable, {verdicts['no_quote']} without a quote")
    ch = [] if "--all" in argv else changed_assessments(base); lines.append(f"\n{len(ch)} assessment change(s)")
    for ev, dim, old, new, sig_ids in ch:
        ok = any(x["id"] in sig_ids for x in sigs if x["evaluator"] == ev and x["dimension"] == dim)
        lines.append(f"- {ev}.{dim}: {old} -> {new}: " + ("cites a new or changed signal on this dimension" if ok else "NO new signal on this dimension in this PR"))
    report = "\n".join(lines); print(report)
    if out: (ROOT / out).write_text(report)
    return 0

if __name__ == "__main__":
    sys.exit(main())
