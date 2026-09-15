import pathlib, re
from bench.load import ROOT
from bench.figures import funding_graph
DIST = ROOT / "dist"

def test_pages_exist():
    from bench.ledger import load_ledger
    L = load_ledger()
    for eid in L["entities"]:
        assert (DIST / "entity" / f"{eid}.html").exists(), eid
    for name in ("evaluators", "entities", "regimes", "sources"):
        assert (DIST / name / "index.html").exists()
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

def test_status_page_shows_hop0_next_to_hop01():
    html = (DIST / "status" / "index.html").read_text()
    assert 'direct inflow from a lab (hop 0)</td><td class="num">9 of 26' in html
    assert 'hop 0 or 1)</td><td class="num">14 of 26' in html
