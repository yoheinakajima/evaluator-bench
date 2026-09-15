from bench.ledger import load_ledger, validate, exposure, distances
from bench.load import load
from bench.verify import LEDGER_ALIAS

def test_ledger_valid():
    assert validate(load_ledger()) == []

def test_every_evaluator_in_ledger():
    L = load_ledger(); d = load()
    ents = {e for e, x in L["entities"].items() if x["kind"] == "evaluator"}
    for eid in d["evaluators"]:
        assert LEDGER_ALIAS.get(eid, eid) in ents, eid

def test_amounts_never_cross_measures():
    for x in exposure(load_ledger()):
        for b in x["buckets"].values():
            assert all(v >= 0 for v in b["by_measure"].values())

def test_labs_are_distance_zero():
    L = load_ledger(); d = distances(L)
    for e, x in L["entities"].items():
        if x["kind"] == "lab": assert d[e] == 0
