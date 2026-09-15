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
