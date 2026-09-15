"""Projection: weighted independence scores from assessments.

Pure function of (assessments, weights). No I/O. Used by build and by tests.
"""
from __future__ import annotations
from .load import DIMS

def score(values: dict[str, int], weights: dict[str, float], *, gated: bool = True) -> int:
    """Weighted 0-100 score from 0-4 dimension values.

    Raises ValueError if any dimension is missing (a silent zero would be a lie).
    Gating is the default: independence floors apply (any 0 caps at 40, any 1 at 60).
    Pass gated=False for the raw compensatory score (sensitivity analysis only). With gated=True, any 0 caps the score at 40,
    any 1 caps it at 60 (floors, not averages).
    """
    missing = [k for k in DIMS if k not in values]
    if missing:
        raise ValueError(f"score: missing dimensions {missing}; refusing to score a partial record")
    num = sum(weights.get(k, 0) * (values[k] / 4) for k in DIMS)
    den = sum(weights.get(k, 0) for k in DIMS)
    if not den:
        raise ValueError("score: weights sum to zero")
    s = num / den * 100
    if gated:
        if any(values[k] == 0 for k in DIMS): s = min(s, 40)
        elif any(values[k] == 1 for k in DIMS): s = min(s, 60)
    return _half_up(s)

def _half_up(x: float) -> int:
    # One rounding rule everywhere (Python and the site): halves round up.
    from decimal import Decimal, ROUND_HALF_UP
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

def table(assessments: list[dict], weights: dict[str, float], *, gated: bool = True) -> dict[str, int]:
    by_ev: dict[str, dict[str, int]] = {}
    for a in assessments:
        by_ev.setdefault(a["evaluator"], {})[a["dimension"]] = a["value"]
    return {e: score(v, weights, gated=gated) for e, v in by_ev.items()}
