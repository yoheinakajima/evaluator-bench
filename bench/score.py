"""Projection: weighted independence scores, bands, and coverage from dimension values.

Pure functions of (values, weights). No I/O. Used by build, the verifier, and the tests.

A value may be None (unevidenced under the chosen evidence policy). The score is
computed over the evidenced dimensions only, and the coverage says how many of
the eight that is. Independence has floors: the band, not a numeric cap, carries
them. Any evidenced 0 puts the organization in the disqualifying band, any 1 in
the conditional band; otherwise it is clear. The number ranks within a band.
"""
from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from .load import DIMS

BANDS = ["clear", "conditional", "disqualifying", "unevidenced"]
BAND_DIMS = ["F", "G", "P", "X", "S", "R"]   # the conflict dimensions; access and methods never set a band (D-002)
BAND_LABEL = {"clear": "Clear", "conditional": "Conditional floor", "disqualifying": "Disqualifying floor", "unevidenced": "Unevidenced"}
BAND_DESC = {
    "clear": "No evidenced dimension below 2.",
    "conditional": "At least one evidenced conflict dimension (funding, governance, personnel, role incompatibility, scope, publication) at 1: usable with conditions the card names.",
    "disqualifying": "At least one evidenced conflict dimension at 0: not a candidate for an independence-critical role until the floor moves. Access and methods never set a band.",
    "unevidenced": "No conflict dimension is evidenced under this policy.",
}
BAND_ORDER = {b: i for i, b in enumerate(BANDS)}


def _half_up(x: float) -> int:
    # One rounding rule everywhere (Python and the site): halves round up.
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _check(values: dict, weights: dict) -> None:
    missing = [k for k in DIMS if k not in values]
    if missing:
        raise ValueError(f"score: missing dimensions {missing}; refusing to score a partial record")
    if not sum(weights.get(k, 0) for k in DIMS):
        raise ValueError("score: weights sum to zero")


def score(values: dict[str, int | None], weights: dict[str, float]) -> int | None:
    """Weighted 0-100 score over the evidenced dimensions; None if nothing is evidenced.

    Every dimension key must be present (a silent zero would be a lie); a None value
    means unevidenced and is excluded from both numerator and denominator.
    """
    _check(values, weights)
    ev = [k for k in DIMS if values[k] is not None]
    den = sum(weights.get(k, 0) for k in ev)
    if not ev or not den:
        return None
    num = sum(weights.get(k, 0) * (values[k] / 4) for k in ev)
    return _half_up(num / den * 100)


def band(values: dict[str, int | None]) -> str:
    ev = [values[k] for k in BAND_DIMS if values.get(k) is not None]
    if not ev:
        return "unevidenced"
    if any(v == 0 for v in ev):
        return "disqualifying"
    if any(v == 1 for v in ev):
        return "conditional"
    return "clear"


def coverage(values: dict[str, int | None]) -> int:
    return sum(1 for k in DIMS if values.get(k) is not None)


def score_range(values: dict[str, int | None], weights: dict[str, float]) -> tuple[int, int] | None:
    """What the score could be if every unevidenced dimension were 0, or were 4."""
    if coverage(values) == len(DIMS):
        s = score(values, weights)
        return (s, s) if s is not None else None
    lo = score({k: (0 if values[k] is None else values[k]) for k in DIMS}, weights)
    hi = score({k: (4 if values[k] is None else values[k]) for k in DIMS}, weights)
    return (lo, hi)


def floor_dimension(values: dict[str, int | None]) -> str | None:
    ev = [k for k in DIMS if values.get(k) is not None]
    return min(ev, key=lambda k: values[k]) if ev else None


def sort_key(values: dict[str, int | None], weights: dict[str, float], name: str = "", band_first: bool = True) -> tuple:
    s = score(values, weights)
    return ((BAND_ORDER[band(values)] if band_first else 0), -(s if s is not None else -1), name)


def what_moves(values: dict[str, int | None], weights: dict[str, float]) -> list[dict]:
    """For each dimension below 4, the score if it moved up one anchor."""
    base = score(values, weights)
    out = []
    for k in DIMS:
        v = values.get(k)
        if v is None or v >= 4:
            continue
        nv = dict(values); nv[k] = v + 1
        out.append(dict(dimension=k, from_value=v, to_value=v + 1, score=score(nv, weights), band=band(nv), base=base))
    return out


def table(assessments: list[dict], weights: dict[str, float]) -> dict[str, int | None]:
    """Scores from stored assessment values (the leads-included reading)."""
    by_ev: dict[str, dict[str, int]] = {}
    for a in assessments:
        by_ev.setdefault(a["evaluator"], {})[a["dimension"]] = a["value"]
    return {e: score(v, weights) for e, v in by_ev.items()}
