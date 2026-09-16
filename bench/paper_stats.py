"""Statistics cited in paper section 5.5, computed from repository data.

Every number in paper/draft.md section 5.5 must equal what this module
computes. tests/test_paper_stats.py is the drift guard: it recomputes these
and fails if the paper text no longer matches.
"""
from __future__ import annotations

import math

from .load import DIMS
from .policy import POLICY_ORDER, values_by_policy, derive
from .score import band


def section_5_5_stats(d: dict) -> dict:
    vbp = values_by_policy(d)
    ranked = [eid for eid, e in d["evaluators"].items()
              if e.get("status", "ranked") == "ranked"]
    rset = set(ranked)

    sigs = [s for s in d["signals"].values() if s.get("evaluator") in rset]
    n_for = sum(1 for s in sigs if s.get("direction") == "for")
    n_against = sum(1 for s in sigs if s.get("direction") == "against")
    n_spans = sum(1 for s in sigs if s.get("quote"))

    src_ids = {s for sg in sigs for s in sg.get("sources", [])}
    src_types = [d["sources"].get(sid, {}).get("source_type") for sid in src_ids]
    n_self = sum(1 for t in src_types if t == "self")
    n_tier1 = sum(1 for t in src_types if t in ("filing", "index"))

    unevidenced = {p: sum(1 for eid in ranked for k in DIMS
                          if vbp[p][eid][k] is None) for p in POLICY_ORDER}

    sigs_all = d["signals"]
    srcs = d["sources"]
    n_held = sum(1 for a in d["assessments"]
                 if a.get("evaluator") in rset
                 and derive(a, sigs_all, srcs, "standard")["evidence_limited"])
    n_resolved = sum(1 for a in d["assessments"]
                     if a.get("evaluator") in rset
                     and a.get("resolution", {}).get("rule"))

    n_funding_le2 = sum(1 for eid in ranked
                        if (vbp["standard"][eid]["F"] if vbp["standard"][eid]["F"] is not None else 99) <= 2)

    means = {}
    for p in ("leads", "standard"):
        means[p] = {}
        for k in DIMS:
            vs = [vbp[p][eid][k] for eid in ranked if vbp[p][eid][k] is not None]
            means[p][k] = sum(vs) / len(vs)
    max_diff = max(abs(means["leads"][k] - means["standard"][k]) for k in DIMS)
    # the paper states an upper bound at two decimals; round the true max up
    max_diff_2dp = math.ceil(max_diff * 100) / 100

    bands = {b: sum(1 for eid in ranked if band(vbp["standard"][eid]) == b)
             for b in ("clear", "conditional", "disqualifying")}

    return {
        "n_ranked": len(ranked),
        "n_signals": len(sigs),
        "n_for": n_for,
        "n_against": n_against,
        "n_spans": n_spans,
        "n_sources": len(src_ids),
        "n_self": n_self,
        "n_tier1": n_tier1,
        "unevidenced": unevidenced,
        "n_held": n_held,
        "n_resolved": n_resolved,
        "n_funding_le2": n_funding_le2,
        "max_leads_std_mean_diff_2dp": max_diff_2dp,
        "bands": bands,
    }

