"""What changed between two revisions: the raw material for the annual update paper.

    python -m bench changelog --since <git ref> [--until HEAD]

Reports evaluators added, assessment value changes with the signals behind
them, score movement per preset, sources added by tier and audit status,
ledger rows added and rows promoted from imported to confirmed, milestones
added, and dockets added. Everything comes from git, so the report is
reproducible from two commit hashes.
"""
from __future__ import annotations
import json, csv, io, subprocess, sys
from .load import ROOT, DIMS
from .score import score

def _git(*a): return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True).stdout

def _tree(ref: str, prefix: str) -> dict[str, str]:
    files = [f for f in _git("ls-tree", "-r", "--name-only", ref, "--", prefix).split() if f.endswith((".json", ".csv"))]
    return {f: _git("show", f"{ref}:{f}") for f in files}

def _json_dir(ref, prefix): return {k: json.loads(v) for k, v in _tree(ref, prefix).items() if v.strip()}
def _csv(ref, path):
    raw = _git("show", f"{ref}:{path}"); return list(csv.DictReader(io.StringIO(raw))) if raw.strip() else []

def report(since: str, until: str = "HEAD") -> str:
    L = []
    ev0, ev1 = _json_dir(since, "data/evaluators"), _json_dir(until, "data/evaluators")
    ids0 = {v["id"] for v in ev0.values()}; ids1 = {v["id"] for v in ev1.values()}
    L.append(f"# Changes {since[:12]} to {until[:12]}\n")
    L.append(f"Evaluators: {len(ids0)} -> {len(ids1)}; added: {', '.join(sorted(ids1 - ids0)) or 'none'}; removed: {', '.join(sorted(ids0 - ids1)) or 'none'}\n")
    a0 = {(a["evaluator"], a["dimension"]): a for f in _json_dir(since, "data/assessments").values() for a in f}
    a1 = {(a["evaluator"], a["dimension"]): a for f in _json_dir(until, "data/assessments").values() for a in f}
    changes = [(k, a0[k]["value"], a1[k]["value"], a1[k].get("rationale", "")) for k in a1 if k in a0 and a0[k]["value"] != a1[k]["value"]]
    L.append(f"## Assessment changes ({len(changes)})")
    for (e, d), o, n, r in sorted(changes): L.append(f"- {e}.{d}: {o} -> {n}. {r}")
    try:
        presets = json.loads(_git("show", f"{until}:data/presets.json"))
        v0 = {}; v1 = {}
        for (e, d), a in a0.items(): v0.setdefault(e, {})[d] = a["value"]
        for (e, d), a in a1.items(): v1.setdefault(e, {})[d] = a["value"]
        L.append("\n## Score movement (lab procurement preset)")
        moves = [(e, score(v0[e], presets["lab"]["weights"]), score(v1[e], presets["lab"]["weights"])) for e in v1 if e in v0 and len(v0[e]) == 8 and len(v1[e]) == 8]
        for e, s0, s1 in sorted(moves, key=lambda x: abs(x[2] - x[1]), reverse=True):
            if s0 != s1: L.append(f"- {e}: {s0} -> {s1}")
    except Exception as ex: L.append(f"(score movement unavailable: {ex})")
    s0, s1 = _json_dir(since, "data/sources"), _json_dir(until, "data/sources")
    new_src = [v for k, v in s1.items() if k not in s0]
    L.append(f"\n## Sources added ({len(new_src)})")
    by = {}
    for v in new_src: by[(v.get("source_type", "unset"), v.get("audit_status", "unaudited"))] = by.get((v.get("source_type", "unset"), v.get("audit_status", "unaudited")), 0) + 1
    for (t, st), n in sorted(by.items()): L.append(f"- {t}, {st}: {n}")
    for name in ("transfers", "relationships", "negatives"):
        r0 = {r["row_id"]: r for r in _csv(since, f"data/ledger/{name}.csv")}; r1 = {r["row_id"]: r for r in _csv(until, f"data/ledger/{name}.csv")}
        added = [k for k in r1 if k not in r0]; promoted = [k for k in r1 if k in r0 and r0[k].get("audit_status") != "confirmed" and r1[k].get("audit_status") == "confirmed"]
        L.append(f"\n## Ledger {name}: {len(added)} added, {len(promoted)} promoted to confirmed" + (f" ({', '.join(promoted)})" if promoted else ""))
    m0 = sum(len(v["milestones"]) for v in _json_dir(since, "data/industries").values() if "milestones" in v); m1 = sum(len(v["milestones"]) for v in _json_dir(until, "data/industries").values() if "milestones" in v)
    L.append(f"\n## Milestones: {m0} -> {m1}")
    d0 = set(_git("ls-tree", "-r", "--name-only", since, "--", "dockets").split()); d1 = set(_git("ls-tree", "-r", "--name-only", until, "--", "dockets").split())
    L.append(f"\n## Dockets: {len({p.split('/')[1] for p in d0 if p.count('/') >= 2})} -> {len({p.split('/')[1] for p in d1 if p.count('/') >= 2})}")
    return "\n".join(L) + "\n"

def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if "--since" not in argv: print("usage: bench changelog --since <ref> [--until <ref>]"); return 2
    since = argv[argv.index("--since") + 1]; until = argv[argv.index("--until") + 1] if "--until" in argv else "HEAD"
    print(report(since, until)); return 0

if __name__ == "__main__":
    sys.exit(main())
