"""Role classification, derived from type and the role-incompatibility value (RULES.md section 10).

Role is not typed in; `python -m bench verify` rejects a stored role that disagrees with
this function. List placement on the site (referee, government, commercial) follows.
"""
from __future__ import annotations

ROLE_LABEL = {"referee": "Independent referee", "government": "Government institute", "vendor": "Vendor / red-team co.",
              "benchmark": "Benchmark or consortium", "lab-team": "First-party lab team", "expected-entrant": "Expected entrant"}
GROUP_LABEL = {"referee": "Independent referees", "government": "Government institutes", "commercial": "Commercial and first-party"}
GROUP_DESC = {
    "referee": "Nonprofits, public benefit corporations, and academic groups whose work is evaluation or research and who sell nothing to the labs they grade. Lab fees for the evaluation itself keep an organization here; they lower its funding value instead.",
    "government": "Public bodies. Publication and access are scored on outcome and tagged statutory where the constraint is the law, not a lab.",
    "commercial": "Vendors, first-party lab teams, and consortia funded by the labs they benchmark. Competent testers can sit here; the rubric measures structure, not skill.",
}
GROUP_ORDER = ["referee", "government", "commercial"]


def derive_role(e: dict, x_value: int | None) -> str:
    """The role RULES.md section 10 assigns. Benchmarks and expected entrants keep their stored role."""
    if e.get("status") == "watchlist" or e.get("role") == "expected-entrant":
        return "expected-entrant"
    if e.get("role") == "benchmark":
        return "benchmark"
    t = e.get("type")
    if t == "gov":
        return "government"
    if t == "bigtech":
        return "lab-team"
    if t == "vc":
        return "vendor"
    if x_value is not None and x_value <= 1:
        return "vendor"
    if t == "private" and x_value is not None and x_value <= 2:
        return "vendor"
    return "referee"


def list_group(e: dict, role: str) -> str:
    """Which of the three default lists an organization is compared in."""
    if role == "government":
        return "government"
    if role in ("vendor", "lab-team"):
        return "commercial"
    if role == "benchmark":
        return "commercial" if e.get("type") in ("consortium", "vc", "bigtech", "private") else "referee"
    return "referee"
