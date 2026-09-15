"""Regression tests for the v1 repair pass (2026-09-15): fail-closed verifier,
ledger hygiene, gated scoring, and the retired self-certification loop."""
import json, pathlib

import pytest

from bench import load, verify
from bench.score import score, _half_up
from bench.ledger import load_ledger, exposure, evidential, summable
from bench.certificate import main as cert_main

ROOT = pathlib.Path(__file__).resolve().parents[1]
W = {"F": 30, "G": 20, "P": 15, "A": 15, "S": 5, "R": 5, "M": 5, "X": 5}


def test_half_up_rounding():
    assert _half_up(2.5) == 3
    assert _half_up(2.4) == 2
    assert _half_up(0.5) == 1
    # scores are non-negative; halves round up, matching the site's Math.round


def test_hal_gate_regression():
    vals = {"F": 3, "G": 3, "P": 3, "A": 1, "S": 4, "R": 4, "M": 4, "X": 4}
    assert score(vals, W) == 60, "access floor of 1 must cap the gated total at 60"
    assert score(vals, W, gated=False) == 73


def test_gated_is_default_and_caps():
    vals = {k: 4 for k in "FGPASRMX"}; vals["F"] = 0
    assert score(vals, W) == 40
    assert score(vals, W, gated=False) == 70  # raw compensatory is uncapped


def test_missing_dimensions_raise():
    with pytest.raises(ValueError):
        score({"F": 4}, W)
    with pytest.raises(ValueError):
        score({k: 4 for k in "FGPASRMX"}, {"F": 0})


def test_c10_tier1_gate_on_dataset():
    d = load.load()
    tiers = {s["id"]: s.get("source_type") for s in d["sources"].values()}
    sigs = d["signals"]
    for eid, e in d["evaluators"].items():
        avals = [a for a in d["assessments"] if a.get("evaluator") == eid]
        vals = {a["dimension"]: a["value"] for a in avals}
        for dim in "FGP":
            if vals.get(dim) != 4:
                continue
            got = set()
            for a in avals:
                if a["dimension"] == dim:
                    for sid in a["signals"]:
                        for src in sigs[sid]["sources"]:
                            got.add(tiers.get(src))
            assert {"filing", "index"} & got, f"C10: {eid}.{dim}=4 without tier-1 evidence"


def test_certificate_manual_issue_refused():
    assert cert_main(["issue", "metr-lab-money"]) == 2
    assert cert_main(["issue", "metr-lab-money", "--kind", "manual"]) == 2


def test_quarantined_rows_excluded_from_exposure():
    L = load_ledger()
    by_id = {t["row_id"]: t for t in L["transfers"]}
    # T10 superseded, T81 superseded, T54/T02 unverifiable: none may be evidential
    for rid in ("T10", "T81", "T54", "T02"):
        assert not evidential(by_id[rid]), rid
    ex = {x["id"]: x for x in exposure(L)}
    # every counted inflow row is evidential: no leakage from quarantined rows
    for x in ex.values():
        n = sum(1 for t in L["transfers"] if evidential(t) and t["to"] == x["id"])
        assert x["inflow_rows"] == n, x["id"]
    assert by_id["T55"]["audit_status"] == "unverifiable"
    assert not evidential(by_id["T55"])


def test_eur_rows_never_summed():
    L = load_ledger()
    by_id = {t["row_id"]: t for t in L["transfers"]}
    for rid in ("T42", "T48", "T60"):
        t = by_id[rid]
        assert t["currency"] == "EUR"
        assert not summable(t), f"{rid} is EUR and must not enter USD sums"


def test_components_not_additive():
    L = load_ledger()
    by_id = {t["row_id"]: t for t in L["transfers"]}
    for rid in ("T72", "T73", "T74"):
        t = by_id[rid]
        assert t["component_of"], rid
        assert not summable(t), f"{rid} is a component detail and must not be summed"


def test_no_duplicate_ids_in_dataset():
    d = load.load()
    ids = [s["id"] for s in d["sources"].values()]
    assert len(ids) == len(set(ids)), "duplicate source ids"
    sigs = list(d["signals"].keys())
    assert len(sigs) == len(set(sigs)), "duplicate signal ids"
    assert verify.run() == []


def test_evidence_clock_enforced():
    clock = load.EVIDENCE_CLOCK
    d = load.load()
    for s in d["sources"].values():
        for k in ("published", "retrieved"):
            v = s.get(k)
            if v and len(v) >= 4:
                assert v <= clock, f"source {s['id']}: {k}={v} after evidence clock {clock}"
    for sid, g in d["signals"].items():
        v = g.get("recorded")
        if v:
            assert v <= clock, f"signal {sid}: recorded={v} after evidence clock {clock}"


def test_watchlist_excluded_from_rankings():
    d = load.load()
    watch = {eid: e for eid, e in d["evaluators"].items() if e.get("status") == "watchlist"}
    assert set(watch) == {"big4", "hfoai"}
    watch = list(watch.values())
    for e in watch:
        assert e["role"] == "expected-entrant"
