"""Projection: weighted independence scores from assessments.

Pure function of (assessments, weights). No I/O. Used by build and by tests.
"""
from __future__ import annotations
from .load import DIMS

def score(values: dict[str, int], weights: dict[str, float]) -> int:
    num = sum(weights.get(k, 0) * (values[k] / 4) for k in DIMS if k in values)
    den = sum(weights.get(k, 0) for k in DIMS)
    return round(num / den * 100) if den else 0

def table(assessments: list[dict], weights: dict[str, float]) -> dict[str, int]:
    by_ev: dict[str, dict[str, int]] = {}
    for a in assessments:
        by_ev.setdefault(a["evaluator"], {})[a["dimension"]] = a["value"]
    return {e: score(v, weights) for e, v in by_ev.items()}
