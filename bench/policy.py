"""Evidence policies and the derivation of assessment values from signal bounds (RULES.md, section 0).

A signal carries a ``bound``: an against-signal caps the value on its dimension,
a for-signal floors it. An evidence policy decides which signals are admissible.
The value under a policy is the smallest admissible cap or, with no cap, the
largest admissible floor; with no admissible signal it is None (unevidenced).
Evidence status clamps what a bound may set (CONTRACT C14); a 0 needs a quoted
span (C15, C17); a 4 needs a span and a tier-1/2 source or two independent
sources with one not self-published (C15, C16). Everything here is a pure
function of the loaded data, so the site, the verifier, and the tests agree.
"""
from __future__ import annotations
from .load import DIMS

PROVENANCE = {"filing": 1, "index": 1, "ledger": 2, "self": 3, "press": 4, "docket": 9}
PROVENANCE_LABEL = {1: "tier 1 (filing/index)", 2: "tier 2 (ledger)", 3: "tier 3 (self)", 4: "tier 4 (press)", 9: "docket draft"}

POLICIES = {
    "leads": {"label": "Leads included", "short": "everything",
              "desc": "Every signal that is not quarantined counts, including imported and unverifiable leads, which can support only a 2. For research, not for citation."},
    "standard": {"label": "Retrieved & confirmed", "short": "confirmed sources",
                 "desc": "A signal counts only if at least one cited source was re-fetched and confirmed. The default: no number moves on a source you cannot open and check."},
    "against_interest": {"label": "Against interest", "short": "no self-serving self-report",
                         "desc": "Retrieved & confirmed, and an organization's own statements count only when they are against its interest or backed by a non-self source."},
    "spans": {"label": "Verified spans", "short": "quoted spans only",
              "desc": "Retrieved & confirmed, and the signal carries a quoted span you can find on the page."},
    "primary": {"label": "Primary only", "short": "filings and indexes",
                "desc": "Only confirmed filings, funder indexes, or third-party ledgers with a quoted span: what can be verified from outside the field."},
}
POLICY_ORDER = ["leads", "standard", "against_interest", "spans", "primary"]
DEFAULT_POLICY = "standard"


def src_status(s: dict | None) -> str:
    return (s or {}).get("audit_status", "unaudited")


ALIAS = {"farai": "far-ai", "grayswan": "gray-swan"}


def is_self(s: dict | None, evaluator: str | None = None) -> bool:
    """A source is self-published for a signal when it is the evaluated organization's own statement.

    ``self_of`` names the entity whose statement it is (an evaluator id or a ledger entity id).
    A lab's or a funder's own statement about an evaluator is a statement, not that evaluator's
    self-report, so it counts as non-self for the against-interest rule and for C16.
    """
    s = s or {}
    if s.get("source_type") != "self":
        return False
    if evaluator is None or not s.get("self_of"):
        return True
    return s["self_of"] in (evaluator, ALIAS.get(evaluator, evaluator))


def signal_evidence(sig: dict, sources: dict) -> dict:
    srcs = [sources[x] for x in sig.get("sources", []) if x in sources]
    st = [src_status(s) for s in srcs]
    eid = sig.get("evaluator")
    return dict(
        sources=srcs,
        all_confirmed=bool(srcs) and all(x == "confirmed" for x in st),
        any_confirmed=any(x == "confirmed" for x in st),
        any_live=any(x in ("confirmed", "unaudited") for x in st),
        quarantined=bool(srcs) and all(x in ("differs", "superseded") for x in st),
        best_provenance=min((PROVENANCE.get(s.get("source_type"), 9) for s in srcs), default=9),
        non_self_confirmed=any(src_status(s) == "confirmed" and not is_self(s, eid) for s in srcs),
        n_confirmed=sum(1 for s in srcs if src_status(s) == "confirmed"),
    )


def admissible(sig: dict, sources: dict, policy: str) -> bool:
    """Does this signal count under the policy? Superseded and quarantined signals never do."""
    if sig.get("superseded_by"):
        return False
    ev = signal_evidence(sig, sources)
    if not ev["sources"] or ev["quarantined"]:
        return False
    if policy == "leads":
        return True
    if not ev["any_confirmed"]:
        return False
    if policy == "standard":
        return True
    q = bool(sig.get("quote"))
    if policy == "against_interest":
        return sig["direction"] == "against" or ev["non_self_confirmed"]
    if policy == "spans":
        return q
    if policy == "primary":
        return q and any(src_status(s) == "confirmed" and PROVENANCE.get(s.get("source_type"), 9) <= 2 for s in ev["sources"])
    raise ValueError(f"unknown policy {policy}")


def why_inadmissible(sig: dict, sources: dict, policy: str) -> str:
    if sig.get("superseded_by"):
        return "superseded"
    ev = signal_evidence(sig, sources)
    if not ev["sources"]:
        return "no source"
    if ev["quarantined"]:
        return "quarantined"
    if not ev["any_confirmed"]:
        return "no confirmed source (" + ", ".join(sorted({src_status(s) for s in ev["sources"]})) + ")"
    if policy == "against_interest":
        return "self-published, in the organization's interest"
    if policy == "spans":
        return "no quoted span"
    if policy == "primary":
        return "no confirmed tier-1/2 source with a span" if sig.get("quote") else "no quoted span"
    return "not admissible"


def clamp_range(sig: dict, sources: dict) -> tuple[int, int]:
    """C14 as a clamp: all confirmed 0..4; any confirmed or unaudited 1..3; leads only 2."""
    ev = signal_evidence(sig, sources)
    if ev["all_confirmed"]:
        return (0, 4)
    if ev["any_live"]:
        return (1, 3)
    return (2, 2)


def effective_bound(sig: dict, sources: dict) -> dict:
    """The declared bound after the status clamp (C14) and the extreme tests (C15, C16, C17)."""
    b = sig.get("bound")
    if not b or ("cap" not in b and "floor" not in b):
        return dict(kind=None, n=None, raw=None, held=[])
    ev = signal_evidence(sig, sources)
    lo, hi = clamp_range(sig, sources)
    held: list[str] = []
    if "cap" in b:
        raw = n = int(b["cap"])
        if n < lo:
            n = lo; held.append("C14: sources not all confirmed")
        if n == 0 and not sig.get("quote"):
            n = 1; held.append("C15: a 0 needs a quoted span")
        # C17: a 0 needs a non-self source or an admission against interest. An against-signal
        # from the organization's own page is the admission, so with a span the test is met.
        return dict(kind="cap", n=n, raw=raw, held=held)
    raw = n = int(b["floor"])
    if n > hi:
        n = hi; held.append("C14: sources not all confirmed")
    if n == 4:
        if not sig.get("quote"):
            n = 3; held.append("C15: a 4 needs a quoted span")
        second = ev["best_provenance"] <= 2 or (ev["n_confirmed"] >= 2 and ev["non_self_confirmed"])
        if not second:
            n = min(n, 3); held.append("C16: a 4 needs a tier-1/2 source or two independent sources, one not self-published")
    return dict(kind="floor", n=n, raw=raw, held=held)


def _rule(sig: dict) -> str:
    return sig.get("rule") or "no rule named"


def derive(a: dict, signals: dict, sources: dict, policy: str) -> dict:
    """Derive one assessment's value under one policy. Pure; no I/O."""
    sigs = [signals[i] for i in a.get("signals", []) if i in signals]
    adm = [s for s in sigs if admissible(s, sources, policy)]
    out = dict(policy=policy, value=None, raw_value=None, binding=[], caps=[], floors=[], informational=[],
               held=[], conflict=False, unevidenced=False, evidence_limited=False,
               admissible=[s["id"] for s in adm],
               inadmissible={s["id"]: why_inadmissible(s, sources, policy) for s in sigs if s not in adm},
               rationale="")
    caps, floors = [], []
    for s in adm:
        eb = effective_bound(s, sources)
        rec = dict(id=s["id"], n=eb["n"], raw=eb["raw"], rule=_rule(s), claim=s["claim"], held=eb["held"])
        if eb["kind"] == "cap":
            caps.append(rec)
        elif eb["kind"] == "floor":
            floors.append(rec)
        else:
            out["informational"].append(s["id"])
        out["held"] += [f"{s['id']}: {h}" for h in eb["held"]]
    out["caps"], out["floors"] = caps, floors
    if not caps and not floors:
        out["unevidenced"] = True
        skipped = "; ".join(f"{k} ({v})" for k, v in out["inadmissible"].items())
        out["rationale"] = "Unevidenced under this policy: no admissible signal sets a bound." + (f" Not counted: {skipped}." if skipped else "")
        return out
    if caps:
        n = min(c["n"] for c in caps); raw = min(c["raw"] for c in caps)
        binding = [c for c in caps if c["n"] == n]
        out["value"], out["raw_value"], out["binding"] = n, raw, [c["id"] for c in binding]
        text = "; ".join(f"capped at {n} by {c['id']} ({c['rule']}): {c['claim']}" for c in binding)
        fl = max((f["n"] for f in floors), default=None)
        if fl is not None and fl > n:
            out["conflict"] = True
            top = [f for f in floors if f["n"] == fl]
            res = a.get("resolution")
            if res and isinstance(res.get("value"), int):
                out["value"] = max(n, min(fl, int(res["value"])))
                text = (f"Conflict: floor {fl} from {', '.join(t['id'] for t in top)} ({', '.join(t['rule'] for t in top)}) "
                        f"against cap {n} from {', '.join(c['id'] for c in binding)} ({', '.join(c['rule'] for c in binding)}); "
                        f"resolved at {out['value']} by {res.get('rule')}: {res.get('note')}")
            else:
                text = (f"Conflict without a resolution: floor {fl} from {', '.join(t['id'] for t in top)} against cap {n} from "
                        f"{', '.join(c['id'] for c in binding)}; the cap stands until a resolution names the rule.")
        elif fl is not None:
            text = text[0].upper() + text[1:] + f". Floors up to {fl} from {', '.join(f['id'] for f in floors if f['n'] == fl)} do not exceed the cap."
        else:
            text = text[0].upper() + text[1:] + "."
    else:
        n = max(f["n"] for f in floors); raw = max(f["raw"] for f in floors)
        binding = [f for f in floors if f["n"] == n]
        out["value"], out["raw_value"], out["binding"] = n, raw, [f["id"] for f in binding]
        text = "; ".join(f"floored at {n} by {f['id']} ({f['rule']}): {f['claim']}" for f in binding)
        text = text[0].upper() + text[1:] + ". No admissible signal caps it."
    held_binding = [h for h in out["held"] if h.split(":")[0] in out["binding"]]
    out["evidence_limited"] = out["raw_value"] != out["value"] or bool(held_binding)
    if held_binding:
        text += " Held: " + "; ".join(h.split(": ", 1)[1] for h in held_binding) + "."
    if out["inadmissible"] and policy != "leads":
        text += " Not counted under this policy: " + "; ".join(f"{k} ({v})" for k, v in out["inadmissible"].items()) + "."
    out["rationale"] = text
    return out


def derive_all(d: dict, policy: str) -> dict[tuple[str, str], dict]:
    return {(a["evaluator"], a["dimension"]): derive(a, d["signals"], d["sources"], policy) for a in d["assessments"]}


def values_by_policy(d: dict) -> dict[str, dict[str, dict[str, int | None]]]:
    out: dict[str, dict[str, dict[str, int | None]]] = {}
    for p in POLICY_ORDER:
        dv = derive_all(d, p)
        out[p] = {}
        for (eid, k), r in dv.items():
            out[p].setdefault(eid, {})[k] = r["value"]
    return out
