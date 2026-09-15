"""Corpus-wide quote audit for Evaluator Bench (leads/quote_audit.py).

For every signal in data/signals/*.json that carries a `quote`, fetch each cited
source with the exact normalizer CI uses (bench.review.fetch_text) and check
that the quote is a verbatim substring of the normalized text.

Fallback ladder when fetch_text raises or returns a bot wall:
  1. curl -sL -A "Mozilla/5.0" URL, then the same tag-strip / whitespace-collapse
     normalization (method "curl");
  2. curl again with a full browser header set (Accept, Accept-Language, a Chrome
     UA, --compressed). Still recorded as method "curl", with a note, because
     some CDNs (rand.org) 403 the bare Mozilla/5.0 form;
  3. if everything fails, or the quote is still absent, look at a Wayback
     Machine capture (web.archive.org/web/<year>id_/URL). This never changes
     the status; it only adds a note, since CI does not consult the archive.

Run from the repo root with the venv active:

    python leads/quote_audit.py [--cache DIR] [--no-network]

Writes leads/quote-audit.json and leads/quote-audit.md. Fetched texts are
cached under --cache so the suggestion pass can be re-run without re-fetching.

SUGGESTED spans below were chosen by hand after reading the cached text for
each not-found signal. The script verifies each one is an exact substring of
the fetched, normalized text and at most 120 characters before writing it; a
suggestion that fails verification is written as null and flagged.
"""
from __future__ import annotations
import argparse, glob, html, json, os, re, subprocess, sys, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bench.review import fetch_text  # noqa: E402

RUN_DATE = "2026-09-15"
BOT_WALL = re.compile(r"Please enable JS|Request blocked|403 ERROR|Access Denied|Just a moment|Attention Required", re.I)
MIN_BODY = 1000  # a normalized body shorter than this is treated as a shell / bot wall

# Hand-chosen replacement spans for signals whose quote was not found.
# signal id -> {"source": <source id>, "span": <exact span>, "note": <why>}
SUGGESTED: dict[str, dict] = {
    "apollo.13": {
        "source": "apollo-pbc-mission",
        "span": "held by “mission directors” who are independent to Apollo Research PBC and our funders",
        "note": "Same sentence; the page uses curly quotes (U+201C/U+201D) where the signal used straight quotes.",
    },
    "averi.10": {
        "source": "averi-funding",
        "span": "recused from directly auditing OpenAI until two years after his October 2024 departure",
        "note": "Page wording differs from the signal ('until two years after his October 2024 departure' vs 'for at least two years').",
    },
    "farai.12": {
        "source": "far-30m",
        "span": "FAR.AI secured over $30 million of funding commitments in 2025",
        "note": "op-far-general-support (openphilanthropy.org) now 301s to coefficientgiving.org/funds/, a generic page. The original quote is verbatim on a Wayback capture of the OP page (see archive line). The $28,675,000 figure is not on any live cited page.",
    },
    "metr.21": {
        "source": "instrumentl-arc-990",
        "span": "Alignment Research Center, operating as a public charity in Covina, CA, provided $4,553,935 in grants in 2024",
        "note": "Instrumentl reworded its summary; the page never names METR as recipient (it shows '1 awards in 2024' behind a sign-up wall). op-longview and op-constellation now redirect to coefficientgiving.org/funds/; their figures ($15,961,273; $16,750,000) are verbatim on Wayback captures.",
    },
    "palisade.11": {
        "source": "evaluators-ledger",
        "span": "Coefficient name matched: 'Palisade Research' ($1,680,000 2024-06; $2,123,463 2025-05).",
        "note": "op-palisade cites the generic OP grants index, which never carried Palisade text and now redirects to coefficientgiving.org/funds/. The original quote is verbatim on the Wayback capture of openphilanthropy.org/grants/palisade-research-general-support-2025/ (Amount $2,123,463, May 2025, 'two grants'); that page also lists a separate $1,680,000 2024 grant, so the imported $3,803,463 index total = 1,680,000 + 2,123,463 and the 'differs' flag can be reconciled.",
    },
}

# Extra notes for signals whose status is decided by the fetch ladder rather than a span.
NOTES: dict[str, str] = {
    "rand.10": "rand.org (CloudFront) returned HTTP 403 to fetch_text and to the bare `curl -A Mozilla/5.0` form on the first run of 2026-09-15 but served normally with full browser headers; a re-run the same day fetched normally with fetch_text. Treat this source as flaky in CI.",
    "grayswan.02": "forbes.com returns HTTP 403 to fetch_text and a 'Please enable JS' shell to every curl form. The quote is verbatim in the Wayback capture (web.archive.org/web/2025id_/<url>). Suggest adding an `archive` field to forbes-grayswan-2024.",
    "securebio.01": "The cited page never carried this sentence. No SecureBio page states that OpenAI covered the GPT-5.5 assessment; see fixes.securebio.01 for the nearest supported statement (GPT-6 Astra and GPT-5.6 Sol full reports).",
}

# Fixes for TASK 2 (new source record + replacement quote), written verbatim under "fixes".
FIXES: dict[str, dict] = {
    "securebio.01": {
        "source": {
            "id": "securebio-gpt6-astra-report",
            "title": "Pre-Release Assessment of OpenAI's GPT-6 Astra (full technical report, PDF)",
            "publisher": "SecureBio",
            "url": "https://securebio.org/resources/gpt-6-astra-assessment.pdf",
            "published": "2026-09-14",
            "retrieved": "2026-09-15",
            "source_type": "self",
            "audit_status": "confirmed",
            "note": "Linked as 'full technical report' from https://securebio.org/blog/gpt-6-astra-pre-release-testing-report/ (published September 14, 2026). Section 'Independent Evaluations' and the AEF-1 checklist (item 2.1, 2.4) state that OpenAI's payment was limited to covering SecureBio's costs (tokens, compute, employee time), agreed in advance, not contingent on findings; the report was reviewed by OpenAI before publication with no substantive edits. Fetched 2026-09-15, SHA-256 dcedf0d32944...; text extracted with pdftotext (poppler) and whitespace-collapsed. CAUTION: bench.review.fetch_text does not extract PDF text, so CI will report this quote NOT FOUND; see 'alternatives' for an HTML span CI can check.",
        },
        "quote": "SecureBio received compensation from OpenAI limited to covering the costs of this assessment",
        "claim_note": "No SecureBio page states that OpenAI covered the GPT-5.5 assessment. The GPT-5.5 post (securebio.org, April 9, 2026; Substack copy April 23, 2026) carries no funding disclosure and links only OpenAI's system card. The claim should be re-scoped to GPT-6 Astra (this source) or GPT-5.6 Sol (alternative 1), whose full reports carry the same sentence.",
        "alternatives": [
            {
                "id": "securebio-gpt56-sol-report",
                "title": "Pre-Release Assessment of OpenAI's GPT-5.6 Sol (full technical report, PDF)",
                "publisher": "SecureBio",
                "url": "https://securebio.org/reports/gpt-5-6-sol-assessment.pdf",
                "published": "2026-07-23",
                "retrieved": "2026-09-15",
                "source_type": "self",
                "audit_status": "confirmed",
                "quote": "SecureBio received compensation from OpenAI limited to covering the costs of this assessment",
                "note": "Same sentence as the GPT-6 report. The PDF text layer contains zero-width spaces (U+200B) between some words, so the span matches only after stripping U+200B. Also mirrored at /resources/gpt-5-6-sol-assessment.pdf.",
            },
            {
                "id": "securebio-ai-principles",
                "title": "SecureBio's principles and practices for model assessment",
                "publisher": "SecureBio",
                "url": "https://securebio.org/ai/principles/",
                "published": "2026-07-03",
                "retrieved": "2026-09-15",
                "source_type": "self",
                "audit_status": "confirmed",
                "quote": "For some engagements with for-profit firms, we request funding to cover the costs of running the assessments",
                "note": "HTML page; this span is verbatim under fetch_text, so CI can check it. It supports the general half of the claim ('labs typically pay for evaluations of their own models') but names no model or lab. Substack copy dated 2026-07-03.",
            },
        ],
    },
}


def normalize_html(raw: str) -> str:
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(re.sub(r"\s+", " ", t))


def curl_text(url: str, browser_headers: bool = False) -> str:
    cmd = ["curl", "-sL", "--max-time", "45"]
    if browser_headers:
        cmd += ["--compressed", "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "-H", "Accept-Language: en-US,en;q=0.9",
                "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"]
    else:
        cmd += ["-A", "Mozilla/5.0"]
    raw = subprocess.run(cmd + [url], capture_output=True, text=True, errors="ignore").stdout
    return normalize_html(raw)


def wayback_text(url: str) -> tuple[str | None, str | None]:
    """Nearest capture to 2025-01-01, then to 2026-01-01. Returns (text, capture_url)."""
    for year in ("2025", "2026"):
        cap = f"https://web.archive.org/web/{year}id_/{url}"
        t = curl_text(cap, browser_headers=True)
        if t and len(t.strip()) >= 200 and not re.search(r"Wayback Machine has not archived", t):
            return t, cap
    return None, None


def usable(t: str | None) -> bool:
    return bool(t) and len(t.strip()) >= MIN_BODY and not BOT_WALL.search(t[:2000])


def load_corpus():
    signals = []
    for p in sorted(glob.glob(str(ROOT / "data/signals/*.json"))):
        signals.extend(json.load(open(p)))
    sources = {}
    for p in glob.glob(str(ROOT / "data/sources/*.json")):
        d = json.load(open(p)); sources[d["id"]] = d
    return signals, sources


class Fetcher:
    def __init__(self, cache: Path, network: bool = True):
        self.cache = cache; cache.mkdir(parents=True, exist_ok=True)
        self.network = network; self.memo: dict[str, dict] = {}

    def _path(self, url: str, kind: str = "live") -> Path:
        return self.cache / f"{kind}-{hashlib.sha256(url.encode()).hexdigest()[:16]}.json"

    def get(self, url: str) -> dict:
        """{"text": str|None, "method": "fetch_text"|"curl"|None, "error": str|None, "note": str|None}"""
        if url in self.memo: return self.memo[url]
        meta = self._path(url)
        if meta.exists():
            self.memo[url] = json.load(open(meta)); return self.memo[url]
        if not self.network:
            self.memo[url] = {"url": url, "text": None, "method": None, "error": "no network (cache miss)", "note": None}; return self.memo[url]
        res = {"url": url, "text": None, "method": None, "error": None, "note": None}
        first = None
        try:
            text, _sha = fetch_text(url)
            if usable(text):
                res["text"], res["method"] = text, "fetch_text"
            else:
                first = f"fetch_text returned {len(text.strip())} chars" + (" (bot wall)" if BOT_WALL.search(text[:2000]) else "")
        except Exception as ex:
            first = f"fetch_text {type(ex).__name__}: {str(ex)[:100]}"
        if res["text"] is None:
            ct = curl_text(url)
            if usable(ct):
                res["text"], res["method"], res["note"] = ct, "curl", f"{first}; used curl -A Mozilla/5.0"
            else:
                second = f"curl -A Mozilla/5.0 returned {len(ct.strip())} chars" + (" (bot wall)" if BOT_WALL.search(ct[:2000]) else "")
                cb = curl_text(url, browser_headers=True)
                if usable(cb):
                    res["text"], res["method"], res["note"] = cb, "curl", f"{first}; {second}; used curl with full browser headers"
                else:
                    third = f"curl with browser headers returned {len(cb.strip())} chars" + (" (bot wall)" if BOT_WALL.search(cb[:2000]) else "")
                    res["error"] = f"{first}; {second}; {third}"
        json.dump(res, open(meta, "w"))
        self.memo[url] = res; return res

    def wayback(self, url: str) -> dict:
        meta = self._path(url, "wayback")
        if meta.exists(): return json.load(open(meta))
        if not self.network: return {"text": None, "capture": None}
        t, cap = wayback_text(url); res = {"text": t, "capture": cap}
        json.dump(res, open(meta, "w")); return res


def audit(fetcher: Fetcher):
    signals, sources = load_corpus()
    out: dict[str, dict] = {}
    for s in signals:
        q = s.get("quote")
        if not q: continue
        checked = []; found_in = None
        for sid in dict.fromkeys(s["sources"]):  # de-dupe repeated source ids, keep order
            src = sources.get(sid)
            if not src:
                checked.append((sid, {"text": None, "method": None, "error": "missing source record", "note": None})); continue
            r = fetcher.get(src["url"]); checked.append((sid, r))
            if r["text"] and q in r["text"]:
                found_in = (sid, r); break
        rec: dict
        if found_in:
            sid, r = found_in
            rec = {"source": sid, "status": "found", "method": r["method"], "suggested": None}
            if r.get("note"): rec["note"] = r["note"]
        else:
            fetched = [(sid, r) for sid, r in checked if r["text"]]
            if fetched:
                sid, r = fetched[0]
                rec = {"source": sid, "status": "not found", "method": r["method"], "suggested": None}
                sug = SUGGESTED.get(s["id"])
                if sug:
                    ssrc = sources.get(sug["source"]); sres = fetcher.get(ssrc["url"]) if ssrc else None
                    if sres and sres["text"] and sug["span"] in sres["text"] and len(sug["span"]) <= 120:
                        rec["source"], rec["suggested"], rec["method"] = sug["source"], sug["span"], sres["method"]
                        rec["note"] = sug.get("note")
                    else:
                        rec["suggestion_error"] = f"hand-picked span for {sug['source']} not verified as exact substring (<=120 chars)"
                # Archive check (note only): does any cited URL's Wayback capture carry the original quote?
                for csid, _ in checked:
                    csrc = sources.get(csid)
                    if not csrc: continue
                    wb = fetcher.wayback(csrc["url"])
                    if wb["text"] and q in wb["text"]:
                        rec["archive_note"] = f"original quote is verbatim in Wayback capture {wb['capture']}"; break
            else:
                sid, r = checked[0]
                rec = {"source": sid, "status": f"fetch failed: {r['error']}", "method": "curl", "suggested": None}
                wb = fetcher.wayback(sources[sid]["url"]) if sid in sources else {"text": None, "capture": None}
                if wb["text"]:
                    rec["archive_note"] = (f"original quote is verbatim in Wayback capture {wb['capture']}" if q in wb["text"]
                                           else f"Wayback capture {wb['capture']} fetched but quote not found there either")
        if s["id"] in NOTES: rec["note"] = (rec.get("note") + " " if rec.get("note") else "") + NOTES[s["id"]]
        out[s["id"]] = rec
    return out, signals, sources


def load_fixes() -> dict:
    return dict(FIXES)


def write_reports(results: dict, signals: list, sources: dict):
    fixes = load_fixes()
    payload = dict(results)
    if fixes: payload["fixes"] = fixes
    (ROOT / "leads/quote-audit.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    by_id = {s["id"]: s for s in signals}
    found = [k for k, v in results.items() if v["status"] == "found"]
    notfound = [k for k, v in results.items() if v["status"] == "not found"]
    failed = [k for k, v in results.items() if v["status"].startswith("fetch failed")]
    L = ["# Quote audit", "",
         f"Run: {RUN_DATE}. Normalizer: `bench.review.fetch_text`; curl fallback where noted (see `leads/quote_audit.py`).",
         "A quote counts as found only if it is an exact substring of the normalized text of at least one cited source.", "",
         f"- signals with a `quote`: {len(results)}", f"- found: {len(found)}", f"- not found: {len(notfound)}",
         f"- fetch failed: {len(failed)}", ""]
    edge = [k for k in found if results[k].get("note")]
    if edge:
        L += ["## Found, with a fetch caveat", ""]
        for k in edge:
            v = results[k]; L += [f"- {k}: `{v['source']}` via {v['method']}. {v['note']}"]
        L.append("")
    if notfound:
        L += ["## Not found", ""]
        for k in notfound:
            v = results[k]; s = by_id[k]; src = sources.get(v["source"], {})
            L += [f"### {k}", f"- checked: `{v['source']}` ({src.get('url','?')}) via {v['method']}",
                  f"- claim: {s['claim']}", f"- original quote: \"{s['quote']}\"",
                  "- suggested span: " + (f"\"{v['suggested']}\"" if v.get("suggested") else "null (no supporting span on any cited page)")]
            if v.get("suggestion_error"): L.append(f"- WARNING: {v['suggestion_error']}")
            if v.get("archive_note"): L.append(f"- archive: {v['archive_note']}")
            if v.get("note"): L.append(f"- note: {v['note']}")
            L.append("")
    if failed:
        L += ["## Fetch failed", ""]
        for k in failed:
            v = results[k]; src = sources.get(v["source"], {})
            L += [f"### {k}", f"- source: `{v['source']}` ({src.get('url','?')})", f"- {v['status']}"]
            if v.get("archive_note"): L.append(f"- archive: {v['archive_note']}")
            if v.get("note"): L.append(f"- note: {v['note']}")
            L.append("")
    if fixes:
        L += ["## Fixes", ""]
        for k, f in fixes.items():
            L += [f"### {k}", f"- new source `{f['source']['id']}`: {f['source']['title']} ({f['source']['url']}), published {f['source'].get('published')}",
                  f"- quote: \"{f['quote']}\"", f"- note: {f['source'].get('note','')}"]
            if f.get("claim_note"): L.append(f"- claim: {f['claim_note']}")
            for alt in f.get("alternatives", []):
                L.append(f"- alternative `{alt['id']}` ({alt['url']}, {alt.get('published')}): \"{alt['quote']}\" -- {alt.get('note','')}")
            L.append("")
    (ROOT / "leads/quote-audit.md").write_text("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.environ.get("QUOTE_AUDIT_CACHE", str(ROOT.parent / ".quote-audit-cache")))
    ap.add_argument("--no-network", action="store_true")
    a = ap.parse_args()
    f = Fetcher(Path(a.cache), network=not a.no_network)
    results, signals, sources = audit(f)
    write_reports(results, signals, sources)
    c = {"found": 0, "not found": 0, "fetch failed": 0}
    for v in results.values(): c["fetch failed" if v["status"].startswith("fetch") else v["status"]] += 1
    print(json.dumps(c))
    for k, v in results.items():
        if v["status"] != "found" or v.get("note"):
            print(k, "|", v["source"], "|", v["status"], "|", v["method"], "|", "suggested:", repr(v.get("suggested")), "|", v.get("suggestion_error", ""), "|", v.get("archive_note", ""))


if __name__ == "__main__":
    main()
