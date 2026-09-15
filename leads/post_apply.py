"""Apply the quote-audit corrections and the primary pledge sources after the bounds files are merged.

    python leads/post_apply.py

Run from the repo root with the venv active, after `python -m bench.apply_bounds`.
Idempotent. Then re-run `python -m bench.apply_bounds` (no arguments) so values are recomputed.
"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT))

def rd(p): return json.loads(p.read_text())
def wr(p, o, indent=1): p.write_text(json.dumps(o, indent=indent, ensure_ascii=False) + "\n")
def sig(eid, sid):
    p = DATA / "signals" / f"{eid}.json"; L = rd(p)
    return p, L, next(s for s in L if s["id"] == sid)
def src(sid): return DATA / "sources" / f"{sid}.json"

audit = rd(ROOT / "leads" / "quote-audit.json")
log = []
import subprocess
def old_quote(eid, sid):
    """The quote as committed before the bounds pass, so a quote an evidence agent already replaced is left alone."""
    try:
        old = json.loads(subprocess.run(["git", "show", f"HEAD:data/signals/{eid}.json"], cwd=ROOT, capture_output=True, text=True).stdout)
        return next((x.get("quote") for x in old if x["id"] == sid), None)
    except Exception:
        return None

# 1. corrected spans where the page was reworded, unless the bounds pass already replaced the quote
for sid, spec in audit.items():
    if sid == "fixes" or spec.get("status") != "not found" or not spec.get("suggested"): continue
    eid = sid.split(".")[0]; p, L, s = sig(eid, sid)
    if s.get("quote") and s.get("quote") != old_quote(eid, sid):
        log.append(f"{sid}: quote already replaced by the bounds pass; audit suggestion not applied"); continue
    s["quote"] = spec["suggested"][:120]; s["quote_source"] = spec["source"]
    if spec["source"] not in s["sources"]: s["sources"].append(spec["source"])
    wr(p, L); log.append(f"{sid}: quote replaced from {spec['source']}")

# 2. archives for pages behind bot walls or redirects
for sid_src, url in {
    "forbes-grayswan-2024": (audit.get("grayswan.02", {}).get("archive_note") or "").split("capture ")[-1].split(" ")[0],
}.items():
    if url.startswith("http"):
        p = src(sid_src); o = rd(p); o["archive"] = url; wr(p, o, 2); log.append(f"{sid_src}: archive recorded")

# 3. securebio.01: re-scope to the GPT-6 Astra report only if the bounds pass found no verbatim source for the claim
fx = audit.get("fixes", {}).get("securebio.01")
p0, L0, s0 = sig("securebio", "securebio.01")
if fx and not (s0.get("quote") and s0.get("quote_source") and s0["quote_source"] != "securebio-oaif"):
    pdf = {k: v for k, v in fx["source"].items()}; pdf["self_of"] = "securebio"
    if not src(pdf["id"]).exists(): wr(src(pdf["id"]), pdf, 2); log.append(f"added source {pdf['id']}")
    alt = next((a for a in fx.get("alternatives", []) if a["id"] == "securebio-ai-principles"), None)
    if alt:
        rec = {k: v for k, v in alt.items() if k != "quote"}; rec["self_of"] = "securebio"; rec.setdefault("retrieved", "2026-09-15")
        if not src(rec["id"]).exists(): wr(src(rec["id"]), rec, 2); log.append(f"added source {rec['id']}")
    p, L, s = sig("securebio", "securebio.01")
    s["claim"] = "Labs pay for pre-release evaluations of their own models: SecureBio's GPT-6 Astra and GPT-5.6 Sol reports state that OpenAI's compensation was limited to covering the costs of the assessment, and its principles page says it requests cost coverage from for-profit firms."
    s["sources"] = [x for x in ["securebio-ai-principles" if alt else None, pdf["id"], "securebio-oaif"] if x]
    s["quote"] = (alt["quote"] if alt else fx["quote"])[:120]; s["quote_source"] = "securebio-ai-principles" if alt else pdf["id"]
    s["as_of"] = "2026-09-14"; s.pop("bound_note", None)
    wr(p, L); log.append("securebio.01: re-scoped to the GPT-6 Astra report")

# 4. the September 2026 pledges: cite the primary statements on metr.05
p, L, s = sig("metr", "metr.05")
for x in ("anthropic-pace-frontier", "anthropic-amodei-x-pace-frontier", "openai-altman-embedded-pledge"):
    if x not in s["sources"]: s["sources"].append(x)
s["quote"] = "a team of embedded third-party evaluators (such as METR )"; s["quote_source"] = "anthropic-pace-frontier"; s["as_of"] = "2026-09-12"
s["claim"] = "Named by Anthropic as the example embedded evaluator: an ongoing, employee-like-access commitment with publication without editorial control; OpenAI's chief executive said OpenAI would do the same on access, without naming an evaluator or publication rights."
wr(p, L); log.append("metr.05: cites the primary pledge statements")

# 5. source status corrections from the bounds pass (re-fetched by Claude on 2026-09-15; recorded in paper/audits/AUDIT-6.md)
for sid_src, status, note in [
    ("gdm-gemini-testing", "unverifiable", "[audit 2026-09-15] the URL resolves to the deepmind.google homepage, which does not mention Dreadnode; the Gemini 3 launch post and press are cited instead. Supports nothing."),
    ("ms-redteam", "confirmed", "[audit 2026-09-15] re-fetched; Microsoft Learn hub is live with PyRIT and describes the team as an internal function of the developer."),
    ("ms-redteam-100", "confirmed", "[audit 2026-09-15] re-fetched; the Security Blog post states the team was formed in 2018 and has red-teamed more than 100 products."),
]:
    p = src(sid_src)
    if p.exists():
        o = rd(p)
        if o.get("audit_status") != status:
            o["audit_status"] = status; o["note"] = (o.get("note", "") + " " + note).strip(); wr(p, o, 2); log.append(f"{sid_src}: audit_status -> {status}")

print("\n".join(log) or "nothing to do")
