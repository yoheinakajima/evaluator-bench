# Certification: from a manual yes to a signed machine verdict

Version 0, 14 Sep 2026.

## What exists now

- `dockets/<slug>/proposal.json`: an Epistemedia-format proposal drafted from Bench evidence and passed through Epistemedia's own validator.
- `data/certificates/<slug>.json`: an `epistemedia-certificate-v0.1` record binding a verdict to the proposal's exact bytes (SHA-256 and Epistemedia proposal_id), naming the reviewer and listing the checks. Version 0 is manual and unsigned: the operator read each span against the live page and said yes. `bench certificate verify` confirms the binding still holds.
- On the site, a source of type `docket` with a certificate shows an "Epistemedia reviewed (manual v0)" badge wherever it is cited.

A manual v0 certificate carries no evidential credit on epistemedia.org. It is a placeholder with the right shape.

## What it should become

1. **Machine verification.** A verifier fetches each source through a byte-stable capture (Wayback `id_`), records the digest, checks every quoted span appears verbatim, re-runs every calculation from the span-bound inputs, and asks a model, with the fetched text in context, whether each credited atom is supported, qualified, or unsupported. Unresolved atoms must carry no evidence; material literals must be covered. Output: a check list with pass, qualified, fail, pending per item. `bench review` is the rough version of this for pull requests.
2. **Independent review.** A second run by a different model family or a person, with no shared prompt lineage, on the same proposal bytes. Epistemedia's open-docket process already requires a separate reviewer; the certificate records both identities.
3. **Signature.** The realm signs the certificate (Ed25519 over the canonical JSON minus the signature block) with a published key; `certificate_id` is the content hash. Verification is offline: hash the proposal, check the id, check the signature.
4. **Badge and endpoint.** Sites embed the badge with a link to `https://epistemedia.org/certificates/<id>`; the endpoint returns the certificate and the proposal it binds. A badge without a resolvable certificate is nothing.
5. **Expiry and revocation.** Certificates carry `expires_at`; a source that changes or a reviewer retraction issues a superseding certificate that references the old id.

## Verdicts

- `reviewed-as-bounded`: every credited atom checked; the proposal's own limitations and unresolved list stand.
- `needs-evidence`: at least one credited atom failed or a calculation did not reproduce; the proposal may be revised and re-submitted.
- `rejected`: prior art, out of scope, or evidence rules violated.

## What Bench does with it

A reviewed docket becomes a source of type `docket` with the certificate id. Signals that cite it inherit the strongest tier. The verifier in `bench verify` checks that the certificate still binds the proposal bytes. If the certificate is revoked or the proposal changes, the badge comes off and the signal drops to whatever its other sources support.
