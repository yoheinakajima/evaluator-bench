import pathlib, re
from bench.load import ROOT
from bench.figures import funding_graph
DIST = ROOT / "dist"

def test_pages_exist():
    from bench.ledger import load_ledger
    L = load_ledger()
    for eid in L["entities"]:
        assert (DIST / "entity" / f"{eid}.html").exists(), eid
    for name in ("evaluators", "entities", "regimes", "sources", "ledger", "rubric", "cases", "method", "exclusions", "status", "contribute", "dockets", "paper"):
        assert (DIST / name / "index.html").exists()
    assert (DIST / "og.png").exists()
    assert (DIST / "style.css").exists() and (DIST / "site.js").exists()

def test_focus_fades_non_neighbours():
    s = funding_graph(focus="coefficient")
    assert 'data-node="coefficient"' in s
    assert s.count('opacity="0.12"') > 20  # most nodes faded
    assert 'data-node="moskovitz" data-tip' in s and 'data-node="moskovitz" data-tip="' in s
    # neighbour is not faded
    i = s.index('data-node="moskovitz"'); seg = s[i:i+200]
    assert 'opacity="0.12"' not in seg.split("style")[0]

def test_build_is_deterministic_for_dist():
    import subprocess, hashlib
    from bench.build import build
    def digest():
        h = hashlib.sha256()
        for p in sorted(DIST.rglob("*")):
            if p.is_file(): h.update(p.relative_to(DIST).as_posix().encode()); h.update(p.read_bytes())
        return h.hexdigest()
    build(write=True); a = digest(); build(write=True); b = digest()
    assert a == b

def test_status_page_shows_hop0_by_kind():
    html = (DIST / "status" / "index.html").read_text()
    assert 'direct lab tie (hop 0), any kind</td><td class="num">12 of 26' in html
    assert 'lab cash or in-kind for evaluation work</td><td class="num">8' in html
    assert 'owns a stake or is acquiring the evaluator</td><td class="num">2' in html
    assert 'no-fee partnership or membership only</td><td class="num">2' in html
    assert 'hop 0 or 1)</td><td class="num">17 of 26' in html

def test_evidence_summary_is_generated_from_the_current_projection():
    import json
    from bench.site import evidence_summary
    bench = json.loads((DIST / "bench.json").read_text())
    assert evidence_summary(bench) in (DIST / "method" / "index.html").read_text()


def test_homepage_carries_byline_competence_and_policies():
    html = (DIST / "index.html").read_text()
    assert 'id="byline"' in html and "Not quality, coverage, or competence" in html
    assert '"default_policy": "standard"' in html and 'rel="canonical"' in html and 'property="og:image"' in html
    assert ".bar{display:block" in html, "the independence bar must render (it was inline with zero height)"


def test_status_statistics_cover_ranked_only():
    html = (DIST / "status" / "index.html").read_text()
    assert "covers the 26 ranked organizations" in html
    ledger = (DIST / "ledger" / "index.html").read_text()
    assert "RANKED = " in ledger and "Watchlist entries are excluded" in ledger

def test_evidence_limited_is_computed_and_marked():
    """Every stored value is its leads-included derivation; the evidence_limited flag is the
    computed 'held' state (C14 clamps, C15 spans, C16 second sources), never typed by hand."""
    from bench.load import load
    from bench.policy import derive
    d = load(strict=False)
    st = lambda sid: d["sources"].get(sid, {}).get("audit_status", "unaudited")
    for a in d["assessments"]:
        r = derive(a, d["signals"], d["sources"], "leads")
        if a.get("unevidenced"):
            assert r["value"] is None, (a["evaluator"], a["dimension"]); continue
        assert r["value"] == a["value"], (a["evaluator"], a["dimension"])
        assert bool(a.get("evidence_limited")) == r["evidence_limited"], (a["evaluator"], a["dimension"])
        if a["value"] in (0, 4):
            bind = [d["signals"][i] for i in r["binding"]]
            assert all(s.get("quote") and all(st(x) == "confirmed" for x in s["sources"]) for s in bind), (a["evaluator"], a["dimension"])
    marked = [a for a in d["assessments"] if a.get("evidence_limited")]
    assert len(marked) >= 7 and all(a["value"] in (1, 2, 3) for a in marked)

def test_docket_status_is_recorded_not_computed():
    from bench.docket import recorded_status
    for d in (ROOT / "dockets").iterdir():
        if d.is_dir() and (d / "proposal.json").exists():
            assert "not installed" not in recorded_status(d.name)
            assert (d / "validation.json").exists(), d.name
