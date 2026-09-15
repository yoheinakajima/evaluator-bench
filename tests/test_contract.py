import json, subprocess, sys, pathlib, hashlib
from bench import verify, load
from bench.score import score, table

ROOT = pathlib.Path(__file__).resolve().parents[1]

def test_verify_clean():
    assert verify.run() == []

def test_score_bounds_and_weights():
    assert score({k: 4 for k in "FGPASRMX"}, {k: 1 for k in "FGPASRMX"}) == 100
    assert score({k: 0 for k in "FGPASRMX"}, {k: 1 for k in "FGPASRMX"}) == 0
    assert score({k: 2 for k in "FGPASRMX"}, {"F": 10, "G": 0, "P": 0, "A": 0, "S": 0, "R": 0, "M": 0, "X": 0}) == 50

def test_projection_matches_data():
    d = load.load()
    bench = json.loads((ROOT / "dist" / "bench.json").read_text())
    t = table(d["assessments"], d["presets"]["lab"]["weights"])
    for e in bench["evaluators"]:
        assert e["scores"]["lab"] == t[e["id"]]

def test_log_reproducible(tmp_path):
    before = hashlib.md5((ROOT / "graph" / "events.jsonl").read_bytes()).hexdigest()
    subprocess.run([sys.executable, "-m", "bench", "build"], cwd=ROOT, check=True, capture_output=True)
    after = hashlib.md5((ROOT / "graph" / "events.jsonl").read_bytes()).hexdigest()
    assert before == after, "committed event log differs from a clean rebuild; commit the regenerated graph/ and dist/"

def test_every_score_has_provenance():
    objs = {}
    for line in (ROOT / "graph" / "events.jsonl").read_text().splitlines():
        ev = json.loads(line)["event"]
        if ev["type"] == "object.created":
            o = ev["payload"]["object"]; objs[o["id"]] = o
    for o in objs.values():
        if o["type"] in ("score", "assessment", "signal"):
            assert o["provenance"]["evidence"], f"{o['id']} has no evidence in provenance"
