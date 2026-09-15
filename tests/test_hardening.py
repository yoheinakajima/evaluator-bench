"""Regression tests for the pre-release hardening pass (2026-09-15): fail-closed verifier,
ledger hygiene, banded scoring, and the retired self-certification loop."""
import json, pathlib

import pytest

from bench import load, verify
from bench.score import score, band, _half_up
from bench.ledger import load_ledger, exposure, evidential, summable
from bench.certificate import main as cert_main

ROOT = pathlib.Path(__file__).resolve().parents[1]
W = {"F": 30, "G": 20, "P": 15, "A": 15, "S": 5, "R": 5, "M": 5, "X": 5}


def test_half_up_rounding():
    assert _half_up(2.5) == 3
    assert _half_up(2.4) == 2
    assert _half_up(0.5) == 1
    # scores are non-negative; halves round up, matching the site's Math.round


def test_hal_band_regression():
    vals = {"F": 3, "G": 3, "P": 3, "A": 1, "S": 4, "R": 4, "M": 4, "X": 4}
    assert band(vals) == "conditional", "an access value of 1 is a conditional floor"
    assert score(vals, W) == 73, "the number is no longer capped; the band carries the floor"


def test_disqualifying_band():
    vals = {k: 4 for k in "FGPASRMX"}; vals["F"] = 0
    assert band(vals) == "disqualifying"
    assert score(vals, W) == 70


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
    # T10 superseded, T81 superseded, T02 unverifiable: none may be evidential.
    # T54 was quarantined until the 2026-09-15 grok pass confirmed the $12.93bn
    # figure on TNW/Fortune, so it is evidential now and no longer belongs here.
    for rid in ("T10", "T81", "T02"):
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
    assert set(watch) == {"hfoai"}   # the hypothetical Big Four composite is no longer scored (RULES 11)
    watch = list(watch.values())
    for e in watch:
        assert e["role"] == "expected-entrant"


def test_verify_fails_closed_on_uncertified_docket(monkeypatch, capsys):
    """A docket-type source claiming 'confirmed' with no independent certificate
    must make verify.main() return 1, not print 'verify: ok' (C13)."""
    d = load.load(strict=False)
    d["sources"] = dict(d["sources"])
    d["sources"]["docket-bad"] = {
        "id": "docket-bad", "title": "bad docket", "url": "https://example.com/x",
        "retrieved": "2026-09-15", "source_type": "docket", "audit_status": "confirmed",
    }
    monkeypatch.setattr(verify, "load", lambda strict=False: d)
    assert verify.main() == 1
    out = capsys.readouterr().out
    assert "verify: ok" not in out
    assert "docket-bad" in out


def test_superseded_rows_labeled():
    """Rows with a superseding row carry audit_status 'superseded', not a
    live status (T10 -> T75, T81 -> T21)."""
    L = load_ledger()
    rows = {t["row_id"]: t for t in L["transfers"]}
    for rid, live in (("T10", "T75"), ("T81", "T21")):
        assert rows[rid]["audit_status"] == "superseded", rid
        assert rows[rid]["superseded_by"] == live, rid
        assert not evidential(rows[rid])


def test_watchlist_excluded_from_status_denominator():
    """The 'lab-tied' headline stat covers the ranked population only (17/26),
    not 17/28. Figure fell from 17 to 14 on 2026-09-15 when the imported-row
    verification pass quarantined 23 unsupported rows, then rose back to 17
    when the grok pass confirmed three more direct lab ties (T52 Meta->Scale,
    T56 Anthropic->Andon, T63 Google->MLCommons) — now on confirmed evidence."""
    from bench.ledger import exposure
    from bench.verify import LEDGER_ALIAS
    d = load.load(strict=False)
    ranked = {LEDGER_ALIAS.get(e["id"], e["id"]) for e in d["evaluators"].values() if e.get("status", "ranked") == "ranked"}
    assert len(ranked) == 26
    ex = exposure()
    near = sum(1 for x in ex if x["id"] in ranked and any(k in ("hop0", "hop1") for k in x["buckets"]))
    assert near == 17
