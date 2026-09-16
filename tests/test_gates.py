"""The Status page gates dashboard must reflect the live output of bench.gates,
and the outreach gate must reconcile the log size with the gate population."""
from bench.gates import gates
from bench.load import ROOT

DIST = ROOT / "dist"


def _status_html():
    return (DIST / "status" / "index.html").read_text()


def test_status_gates_table_uses_live_gates_output():
    html = _status_html()
    gs = gates()
    assert len(gs) == 6
    for g in gs:
        assert g["gate"] in html, f"gate missing from status page: {g['gate']}"
        assert (">PASS<" if g["ok"] else ">FAIL<") in html, (
            f"gate {g['gate']!r} should render "
            f"{'PASS' if g['ok'] else 'FAIL'} on the status page")
        assert g["detail"] in html


def test_outreach_gate_reconciles_log_and_gate_population():
    gs = {g["gate"]: g for g in gates()}
    detail = gs["Every ranked organization and named person has been contacted"]["detail"]
    # the gate population is 51 (24 ranked organizations + 27 named people);
    # the log lists 54 recipients, so the detail must name both numbers
    assert "0 of 51 contacted" in detail
    assert "24 ranked organizations, 27 named people" in detail
    assert "54 recipients" in detail
    assert "non-ranked organization" in detail


def test_status_right_of_reply_reconciles_log_and_gate_population():
    html = _status_html()
    assert "The citable-tag gate tracks 51 of these" in html
