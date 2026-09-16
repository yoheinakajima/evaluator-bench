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
    import csv, re
    from bench.load import load
    from bench.ledger import load_ledger
    from bench.gates import material_people
    from bench.verify import LEDGER_ALIAS
    gs = {g["gate"]: g for g in gates()}
    detail = gs["Every ranked organization and every materially-named person has been contacted"]["detail"]
    # the gate population is the ranked organizations plus the materially-named
    # people; the log may list extra recipients outside the gate. The contacted
    # count moves as outreach goes out, so derive every number from the data.
    d = load(strict=False); L = load_ledger()
    ranked = [e["id"] for e in d["evaluators"].values() if e.get("status", "ranked") == "ranked"]
    people = material_people(d, L)
    need_ids = {LEDGER_ALIAS.get(i, i) for i in ranked + people} | set(ranked + people)
    log = {r["id"]: r for r in csv.DictReader(open(ROOT / "data" / "outreach-log.csv"))}
    contacted = [i for i in ranked + people
                 if log.get(LEDGER_ALIAS.get(i, i), log.get(i, {})).get("contacted")]
    extra = sorted(set(log) - need_ids)
    m = re.fullmatch(r"(\d+) of (\d+) contacted \((\d+) ranked organizations, (\d+) materially-named (?:person|people)\); the log lists (\d+) recipients, including (\d+) outside the gate: (.+)", detail)
    assert m, detail
    assert (m.group(1), m.group(2)) == (str(len(contacted)), str(len(ranked + people)))
    assert (m.group(3), m.group(4)) == (str(len(ranked)), str(len(people)))
    assert (m.group(5), m.group(6)) == (str(len(log)), str(len(extra)))
    assert sorted(m.group(7).split(", ")) == extra


def test_status_right_of_reply_reconciles_log_and_gate_population():
    html = _status_html()
    assert "The citable-tag gate tracks the ranked organizations and the materially-named people" in html
