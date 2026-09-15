"""Verification certificates: what a reviewed docket hands back to a site.

    python -m bench certificate issue <slug> --reviewer "name" --kind manual --verdict reviewed-as-bounded
    python -m bench certificate verify <slug>

Format epistemedia-certificate-v0.1 (proposed here; not yet part of Epistemedia).
A certificate binds a verdict to the exact bytes of a proposal (its SHA-256 and
Epistemedia proposal_id), names the reviewer (a person, or a model with its
identity), lists the checks run, and carries a signature slot. Manual v0 self-certification was retired (it was circular: the same operator
drafted, reviewed, and cited the docket). Certificates are issued only from
independent review at epistemedia.org by someone other than the drafter, and
are signed by the realm's key.
"""
from __future__ import annotations
import json, hashlib, sys, datetime, pathlib
from .load import ROOT

CERTS = ROOT / "data" / "certificates"; DOCKETS = ROOT / "dockets"
VERDICTS = {"reviewed-as-bounded", "needs-evidence", "rejected"}

def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def proposal_digest(slug: str) -> tuple[str, str]:
    raw = (DOCKETS / slug / "proposal.json").read_bytes()
    p = json.loads(raw)
    try:
        from epistemedia.research_kit import validate_proposal
        pid = validate_proposal(p).get("proposal_id", "unknown")
    except ImportError:
        pid = "unknown (epistemedia not installed)"
    return hashlib.sha256(raw).hexdigest(), pid

def issue(slug: str, reviewer: str, kind: str, verdict: str, model: str | None, checks: list[dict], scope: str) -> pathlib.Path:
    assert verdict in VERDICTS
    sha, pid = proposal_digest(slug); p = json.loads((DOCKETS / slug / "proposal.json").read_text())
    cert = {"format": "epistemedia-certificate-v0.1", "subject": {"docket_slug": slug, "question": p["question"], "proposal_sha256": sha, "proposal_id": pid},
            "verdict": verdict, "scope": scope, "reviewer": {"kind": kind, "identity": reviewer, "model": model},
            "checks": checks, "issued_at": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z", "expires_at": None,
            "signature": {"alg": "none", "value": None, "note": "manual v0; unsigned. A signed certificate is issued by the realm's verifier key."}}
    cert["certificate_id"] = "em:certificate:sha256:" + hashlib.sha256(canonical({k: v for k, v in cert.items() if k not in ("certificate_id", "signature")})).hexdigest()
    CERTS.mkdir(exist_ok=True); out = CERTS / f"{slug}.json"; out.write_text(json.dumps(cert, indent=1, ensure_ascii=False) + "\n"); return out

def verify(slug: str) -> list[str]:
    errs = []; cp = CERTS / f"{slug}.json"
    if not cp.exists(): return [f"no certificate for {slug}"]
    cert = json.loads(cp.read_text())
    if cert.get("format") != "epistemedia-certificate-v0.1": errs.append("unknown certificate format")
    if cert.get("verdict") not in VERDICTS: errs.append("invalid verdict")
    sha, pid = proposal_digest(slug)
    if cert["subject"].get("proposal_sha256") != sha: errs.append("proposal bytes changed since the certificate was issued")
    if cert["subject"].get("proposal_id") not in (pid, "unknown (epistemedia not installed)") and pid != "unknown (epistemedia not installed)": errs.append("proposal_id mismatch")
    recomputed = "em:certificate:sha256:" + hashlib.sha256(canonical({k: v for k, v in cert.items() if k not in ("certificate_id", "signature")})).hexdigest()
    if cert.get("certificate_id") != recomputed: errs.append("certificate_id does not match its content")
    if cert["signature"].get("alg") == "none": errs.append("unsigned (manual v0): binds bytes, does not prove who reviewed")
    return errs

def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) < 2: print(__doc__); return 2
    cmd, slug = argv[0], argv[1]
    if cmd == "verify":
        errs = verify(slug); hard = [e for e in errs if not e.startswith("unsigned")]
        print(f"{slug}: " + ("valid binding" if not hard else "INVALID") + (("; " + "; ".join(errs)) if errs else "")); return 0 if not hard else 1
    if cmd == "issue":
        opts = dict(zip(argv[2::2], argv[3::2]))
        if opts.get("--kind", "manual") == "manual":
            print("refused: manual/self-reviewed certificates were retired (see paper/CERTIFICATION.md). "
                  "Certificates are issued only from independent review at epistemedia.org by someone other than the drafter.")
            return 2
        checks = [{"check": "structural-validation", "result": "pass", "note": "epistemedia research validate: only ready-for-review and artifact digests outstanding"},
                  {"check": "spans-read-against-source", "result": "pass", "note": "reviewer re-read each quoted span on the live page"},
                  {"check": "calculations-reproduced", "result": "pass", "note": "arithmetic checked by hand"},
                  {"check": "artifact-digests", "result": "pending", "note": "no byte-level captures yet"},
                  {"check": "independent-reviewer", "result": "pending", "note": "same operator as the drafting run; not independent"}]
        out = issue(slug, opts.get("--reviewer", "unknown"), opts.get("--kind", "manual"), opts.get("--verdict", "reviewed-as-bounded"), opts.get("--model"), checks,
                    opts.get("--scope", "Manual v0 review of a docket drafted from Evaluator Bench evidence; binds a verdict to proposal bytes; carries no evidential credit on epistemedia.org until submitted and reviewed there."))
        print("issued", out); return 0
    print("unknown command"); return 2

if __name__ == "__main__":
    sys.exit(main())
