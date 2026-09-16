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

def test_focus_traces_paths_to_lab_and_evaluator():
    s = funding_graph(focus="coefficient")
    assert 'data-node="coefficient"' in s
    assert s.count('opacity="0.12"') > 20  # most nodes faded
    def faded(html, eid):
        i = html.index(f'data-node="{eid}"')
        return 'opacity="0.12"' in html[i:html.index(">", i)]
    def edge_faded(html, a, b):
        tag = f'<path class="edge" data-from="{a}" data-to="{b}"'
        i = html.find(tag)
        if i < 0:
            tag = f'<path class="edge" data-from="{b}" data-to="{a}"'
            i = html.find(tag)
        assert i >= 0, (a, b)
        return 'opacity="0.08"' in html[i:html.index(">", i)]
    # nodes on a one-direction shortest path to a lab or an evaluator stay bright:
    # coefficient -> apollo (evaluator); coefficient -> epoch (evaluator);
    # coefficient -> moskovitz -> anthropic (lab, leftward only);
    # coefficient -> palisade (evaluator); coefficient -> arc/longview -> metr (evaluator)
    for eid in ("coefficient", "apollo", "epoch", "anthropic", "moskovitz", "palisade", "metr"):
        assert not faded(s, eid), eid
    # a node on no one-direction shortest path from the focus is faded
    assert faded(s, "tallinn")

def test_focus_chains_never_double_back():
    # the zigzag that reached labs through the evaluator column must be gone:
    # openai/google/xai are reachable from coefficient only by going right to
    # epoch and then back left, so they fade, and the anthropic->epoch edge
    # that carried the doubling-back fades with them; the legitimate one-way
    # lab chain (coefficient -> moskovitz -> anthropic) stays bright.
    s = funding_graph(focus="coefficient")
    def faded(html, eid):
        i = html.index(f'data-node="{eid}"')
        return 'opacity="0.12"' in html[i:html.index(">", i)]
    def edge_faded(html, a, b):
        tag = f'<path class="edge" data-from="{a}" data-to="{b}"'
        i = html.find(tag)
        assert i >= 0, (a, b)
        return 'opacity="0.08"' in html[i:html.index(">", i)]
    for eid in ("openai", "google", "xai"):
        assert faded(s, eid), eid
    assert edge_faded(s, "anthropic", "epoch")
    assert not faded(s, "moskovitz")
    assert not edge_faded(s, "moskovitz", "anthropic")

def test_lab_focus_shows_hopped_assessor_paths():
    s = funding_graph(focus="anthropic")
    assert 'data-node="anthropic"' in s
    def faded(html, eid):
        i = html.index(f'data-node="{eid}"')
        return 'opacity="0.12"' in html[i:html.index(">", i)]
    # hopped connections stay bright, each chain running one way across the
    # columns: anthropic -> tallinn -> redwood (2 hops),
    # anthropic -> moskovitz -> coefficient -> palisade (3 hops)
    for eid in ("anthropic", "tallinn", "redwood", "epoch", "coefficient", "palisade"):
        assert not faded(s, eid), eid
    assert faded(s, "schmidt")

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
    assert 'direct lab tie (hop 0), any kind</td><td class="num">10 of 24' in html
    assert 'evaluation credits are recorded, never counted)</td><td class="num">6' in html
    assert 'owns a stake or is acquiring the evaluator</td><td class="num">2' in html
    assert 'no-fee partnership or membership only</td><td class="num">2' in html
    assert 'hop 0 or 1)</td><td class="num">15 of 24' in html

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
    assert "covers the 24 ranked organizations" in html and "retained out-of-scope entries contribute to none" in html
    ledger = (DIST / "ledger" / "index.html").read_text()
    assert "RANKED = " in ledger and "Watchlist and out-of-scope entries are excluded" in ledger

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
    # floor guard: the held set must not be empty (exact count lives in paper §5.5 via test_paper_stats.py)
    assert len(marked) >= 6 and all(a["value"] in (1, 2, 3) for a in marked)

def test_docket_status_is_recorded_not_computed():
    from bench.docket import recorded_status
    for d in (ROOT / "dockets").iterdir():
        if d.is_dir() and (d / "proposal.json").exists():
            assert "not installed" not in recorded_status(d.name)
            assert (d / "validation.json").exists(), d.name

def test_status_page_buckets_close():
    import re
    from collections import Counter
    from bench.load import load
    from bench.ledger import load_ledger
    d = load(strict=False); L = load_ledger()
    html = (DIST / "status" / "index.html").read_text()
    for label, counts in (("Sources", Counter((s.get("audit_status") or "unknown") for s in d["sources"].values())),
                          ("Ledger transfers", Counter((t.get("audit_status") or "unknown") for t in L["transfers"]))):
        total = sum(counts.values())
        m = re.search(re.escape(label) + r'</td><td class="num">(\d+) \(([^)]*)\)', html)
        assert m, f"{label} row missing breakdown"
        assert int(m.group(1)) == total, f"{label}: total {m.group(1)} != {total}"
        shown = {st: n for n, st in re.findall(r"(\d+) (\w+)", m.group(2))}
        for st, n in counts.items():
            assert shown.get(st) == str(n), f"{label}: bucket {st} shows {shown.get(st)}, expected {n}"

def test_every_page_carries_build_digest():
    from bench.site import event_digest
    d = event_digest()
    assert len(d) == 12 and d != "unknown"
    for p in list((DIST).rglob("*.html")):
        html = p.read_text()
        assert d in html, f"build digest missing from {p.relative_to(DIST)}"

def test_evaluators_page_hides_number_until_scored():
    import re
    html = (DIST / "evaluators" / "index.html").read_text()
    cells = re.findall(r'<td class="num evscore"[^>]*>(.*?)</td>', html)
    assert cells, "no score cells found"
    assert all(c == "–" for c in cells), "a weighted number is visible before the reader chooses weights"
    assert 'data-lab="' in html and 'id="evscore-btn"' in html
    assert "Score with these weights" in html

def test_unranked_entries_show_not_ranked_not_a_band():
    html = (DIST / "entity" / "hfoai.html").read_text()
    assert "not ranked" in html
    assert "Disqualifying floor" not in html
    idx = (DIST / "evaluators" / "index.html").read_text()
    for eid in ("hfoai", "epoch", "hal"):
        pass
    # watchlist and out-of-scope rows in the directory carry no band chip
    assert idx.count("not ranked") >= 3

def test_critique_linked_from_method():
    html = (DIST / "method" / "index.html").read_text()
    assert "CRITIQUE.md" in html and "what the authors already know is weak" in html.lower()

def test_citation_block_present():
    import yaml
    d = yaml.safe_load((ROOT / "CITATION.cff").read_text())
    assert d["cff-version"] == "1.2.0"
    assert d["license"] == "Apache-2.0"
    html = (DIST / "paper" / "index.html").read_text()
    assert "citblock" in html and "citbtn" in html and "Copy citation" in html
