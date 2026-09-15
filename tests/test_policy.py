"""The derivation model (RULES.md section 0): bounds, policies, clamps, bands, roles."""
import pytest
from bench.policy import derive, admissible, effective_bound, clamp_range, POLICY_ORDER
from bench.score import score, band, coverage, score_range, what_moves, sort_key
from bench.roles import derive_role, list_group

SRC = {
    "filing": {"id": "filing", "source_type": "filing", "audit_status": "confirmed"},
    "self": {"id": "self", "source_type": "self", "audit_status": "confirmed"},
    "press": {"id": "press", "source_type": "press", "press_kind": "primary", "audit_status": "confirmed"},
    "unaudited": {"id": "unaudited", "source_type": "press", "press_kind": "primary", "audit_status": "unaudited"},
    "imported": {"id": "imported", "source_type": "index", "audit_status": "imported"},
    "unverifiable": {"id": "unverifiable", "source_type": "ledger", "audit_status": "unverifiable"},
}
W = {"F": 30, "G": 20, "P": 15, "A": 15, "S": 5, "R": 5, "M": 5, "X": 5}


def sig(id, direction, bound, sources, quote=None, rule="T.1"):
    s = dict(id=id, evaluator="x", dimension="F", direction=direction, claim="claim text here", sources=sources, recorded="2026-09-15", bound=bound, rule=rule)
    if quote: s["quote"] = quote
    return s


def assess(ids, **kw):
    return dict(evaluator="x", dimension="F", value=0, anchor=0, signals=ids, assessed="2026-09-15", **kw)


def test_cap_wins_over_floor():
    S = {"a": sig("a", "for", {"floor": 2}, ["self"]), "b": sig("b", "against", {"cap": 2}, ["press"])}
    r = derive(assess(["a", "b"]), S, SRC, "leads")
    assert r["value"] == 2 and r["binding"] == ["b"] and not r["conflict"]
    S["a"]["bound"] = {"floor": 3}
    assert derive(assess(["a", "b"]), S, SRC, "leads")["conflict"], "a floor above a cap is a conflict that needs a resolution"


def test_floor_only_when_no_cap():
    S = {"a": sig("a", "for", {"floor": 3}, ["self"])}
    assert derive(assess(["a"]), S, SRC, "leads")["value"] == 3


def test_conflict_needs_resolution():
    S = {"a": sig("a", "for", {"floor": 3}, ["self"]), "b": sig("b", "against", {"cap": 1}, ["press"])}
    r = derive(assess(["a", "b"]), S, SRC, "leads")
    assert r["conflict"] and r["value"] == 1                       # the cap stands until resolved
    r2 = derive(assess(["a", "b"], resolution={"rule": "F.3", "value": 2, "note": "fees"}), S, SRC, "leads")
    assert r2["value"] == 2 and r2["conflict"]


def test_status_clamps_c14():
    assert clamp_range(sig("a", "for", {"floor": 4}, ["unaudited"]), SRC) == (1, 3)
    assert clamp_range(sig("a", "for", {"floor": 4}, ["imported"]), SRC) == (2, 2)
    assert clamp_range(sig("a", "for", {"floor": 4}, ["filing"]), SRC) == (0, 4)
    eb = effective_bound(sig("a", "against", {"cap": 0}, ["unaudited"], quote="q"), SRC)
    assert eb["n"] == 1 and any(h.startswith("C14") for h in eb["held"])


def test_extremes_need_spans_and_second_sources():
    # a 0 without a span is held at 1
    eb = effective_bound(sig("a", "against", {"cap": 0}, ["self"]), SRC)
    assert eb["n"] == 1 and any(h.startswith("C15") for h in eb["held"])
    # a 0 with a span from the organization's own page stands (admission against interest)
    assert effective_bound(sig("a", "against", {"cap": 0}, ["self"], quote="q"), SRC)["n"] == 0
    # a 4 with a span but one self source is held at 3 (C16)
    eb = effective_bound(sig("a", "for", {"floor": 4}, ["self"], quote="q"), SRC)
    assert eb["n"] == 3 and any(h.startswith("C16") for h in eb["held"])
    # a 4 with a span and a filing stands; so does self plus primary press
    assert effective_bound(sig("a", "for", {"floor": 4}, ["filing"], quote="q"), SRC)["n"] == 4
    assert effective_bound(sig("a", "for", {"floor": 4}, ["self", "press"], quote="q"), SRC)["n"] == 4


def test_policies():
    s_self_for = sig("a", "for", {"floor": 3}, ["self"])
    s_self_against = sig("b", "against", {"cap": 2}, ["self"], quote="q")
    s_lead = sig("c", "against", {"cap": 1}, ["unverifiable"])
    s_prim = sig("d", "for", {"floor": 3}, ["filing"], quote="q")
    assert admissible(s_lead, SRC, "leads") and not admissible(s_lead, SRC, "standard")
    assert admissible(s_self_for, SRC, "standard") and not admissible(s_self_for, SRC, "against_interest")
    assert admissible(s_self_against, SRC, "against_interest")
    assert not admissible(s_self_for, SRC, "spans") and admissible(s_self_against, SRC, "spans")
    assert admissible(s_prim, SRC, "primary") and not admissible(s_self_against, SRC, "primary")
    S = {"a": s_self_for, "c": s_lead}
    assert derive(assess(["a", "c"]), S, SRC, "leads")["value"] == 2      # lead supports only a 2
    assert derive(assess(["a", "c"]), S, SRC, "standard")["value"] == 3   # lead not counted
    assert derive(assess(["c"]), S, SRC, "standard")["unevidenced"]


def test_score_with_unevidenced_dimensions():
    full = {k: 4 for k in "FGPASRMX"}
    assert score(full, W) == 100 and band(full) == "clear" and coverage(full) == 8
    half = dict(full); half["F"] = None; half["G"] = None
    assert score(half, W) == 100 and coverage(half) == 6 and score_range(half, W) == (50, 100)
    assert score({k: None for k in "FGPASRMX"}, W) is None and band({k: None for k in "FGPASRMX"}) == "unevidenced"
    with pytest.raises(ValueError):
        score({"F": 4}, W)


def test_bands_replace_numeric_caps():
    v = {"F": 3, "G": 3, "P": 3, "A": 1, "S": 4, "R": 4, "M": 4, "X": 4}
    assert band(v) == "clear" and score(v, W) == 73                # access never sets a band (D-002); the number is not capped
    v["S"] = 1
    assert band(v) == "conditional"
    v["F"] = 0
    assert band(v) == "disqualifying"
    assert band({"F": 3, "G": 3, "P": 3, "A": 0, "S": 3, "R": 3, "M": 0, "X": 3}) == "clear"
    assert sort_key({"F": 0, **{k: 4 for k in "GPASRMX"}}, W) > sort_key({k: 2 for k in "FGPASRMX"}, W)  # band first


def test_what_moves_reports_band_changes():
    v = {"F": 1, "G": 3, "P": 3, "A": 3, "S": 3, "R": 3, "M": 3, "X": 3}
    m = {x["dimension"]: x for x in what_moves(v, W)}
    assert m["F"]["band"] == "clear" and m["G"]["band"] == "conditional"


def test_roles_follow_the_rule():
    assert derive_role({"type": "gov"}, 4) == "government"
    assert derive_role({"type": "bigtech"}, 1) == "lab-team"
    assert derive_role({"type": "vc"}, 4) == "vendor"
    assert derive_role({"type": "nonprofit"}, 1) == "vendor"        # sells to labs
    assert derive_role({"type": "nonprofit"}, 3) == "referee"
    assert derive_role({"type": "private"}, 2) == "vendor"          # consults for labs
    assert derive_role({"type": "nonprofit", "role": "benchmark"}, 4) == "benchmark"
    assert list_group({"type": "consortium"}, "benchmark") == "commercial"
    assert list_group({"type": "academic"}, "benchmark") == "referee"
