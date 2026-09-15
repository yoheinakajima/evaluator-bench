# Certification: from a manual yes to a signed machine verdict

Version 1, 15 Sep 2026.

## Policy

A Bench-authored docket can never certify itself. The operator who drafts a
docket cannot be its reviewer, and no certificate the Bench issues to its own
draft carries evidential weight. Concretely:

- `bench certificate issue` refuses manual/self-reviewed issuance.
- A `docket`-type source may never carry `audit_status: confirmed` without an
  independent, signed certificate from a review at epistemedia.org by someone
  other than the drafter; the verifier fails the build otherwise.
- No "Epistemedia reviewed" badge is shown anywhere. Docket drafts are labeled
  drafts.

## What exists now

- `dockets/<slug>/proposal.json`: an Epistemedia-format proposal drafted from Bench evidence and passed through Epistemedia's own validator. Drafts only; none have been submitted.
- Docket drafts are working documents for future submission. They are not findings, not sources, and not citable evidence.

## What it should become

1. **Machine verification.** A verifier fetches each source through a byte-stable capture (Wayback `id_`), records the digest, checks every quoted span appears verbatim, re-runs every calculation from the span-bound inputs, and asks a model, with the fetched text in context, whether each credited atom is supported, qualified, or unsupported. Unresolved atoms must carry no evidence; material literals must be covered. Output: a check list with pass, qualified, fail, pending per item. `bench review` is the rough version of this for pull requests.
2. **Independent review.** A second run by a different model family or a person, with no shared prompt lineage, on the same proposal bytes. Epistemedia's open-docket process already requires a separate reviewer; the certificate records both identities. The reviewer must not be the drafter.
3. **Signature.** The realm signs the certificate (Ed25519 over the canonical JSON minus the signature block) with a published key; `certificate_id` is the content hash. Verification is offline: hash the proposal, check the id, check the signature.
4. **Badge and endpoint.** Sites embed the badge with a link to `https://epistemedia.org/certificates/<id>`; the endpoint returns the certificate and the proposal it binds. A badge without a resolvable certificate is nothing. No badge is shown until this exists.
5. **Expiry and revocation.** Certificates carry `expires_at`; a source that changes or a reviewer retraction issues a superseding certificate that references the old id.

## Verdicts

- `reviewed-as-bounded`: every credited atom checked; the proposal's own limitations and unresolved list stand.
- `needs-evidence`: at least one credited atom failed or a calculation did not reproduce; the proposal may be revised and re-submitted.
- `rejected`: prior art, out of scope, or evidence rules violated.

## What Bench does with it

An independently reviewed docket (reviewed at epistemedia.org by someone other than the drafter, signed certificate) may be recorded as a source of type `docket` as a *secondary summary* of that review — never the strongest tier, never `confirmed` unless the primary sources were re-derived. The verifier in `bench verify` fails the build if a docket-type source claims `confirmed` without such a certificate.
