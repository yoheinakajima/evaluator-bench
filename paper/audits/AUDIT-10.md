# AUDIT-10: second-coder pass over the two newly extreme assessments, 15 September 2026

Scope: the 2 ranked assessments with stored value 0 (and evidence, i.e. not unevidenced)
that had no second-coder row in `data/coding/second-coder.csv` — the full set failing gate
"Every extreme has a second coder" as of 2026-09-15.

Why they are new: PR #21 added quoted spans to `cais.06` and `humane.03`, making those
signals bind under the default policy; the verifier then re-derived `cais.A` and
`humane.A` from 1 (evidence-limited) to 0 (A.6 cap). They did not exist as extremes in
AUDIT-9's 15, which were already second-coded.

Method (AGENTS.md Recipes A/B): each binding signal's quoted span was checked as an exact
substring of a fresh `bench.review.fetch_text` fetch of its `quote_source` URL, with the
surrounding context read to confirm the span supports the signal's claim. Rows were
appended to `data/coding/second-coder.csv`; the coder field records the independent pass.
Nothing disagrees with any stored value; no assessment moved.

| extreme | binding signal(s) | source fetched | sha | verdict | note |
|---|---|---|---|---|---|
| cais.A (0) | cais.06 | https://safe.ai/research | c3fd6378c256 | CONFIRMED | span is the AgentHarm project description: CAIS evaluates leading LLMs' compliance with malicious requests via jailbreaks and publicly releases the benchmark; no privileged access claimed anywhere on the page — A.6 cap 0 |
| humane.A (0) | humane.03 | https://www.humane-intelligence.org/ | 0eb3f6c367e8 | CONFIRMED | span is the "Impact By the numbers" line; page context is hosted red-teaming/bias-bounty events (incl. Zindi) and a data-collection web app — event-based public evaluation work, no weights or privileged access anywhere — A.6 cap 0 |

## Outcome

2 of 2 extremes second-coded; both CONFIRMED verbatim against live fetches. Stored values
unchanged; gate "Every extreme has a second coder" now passes 17/17. This is an audit
record only: no values were changed in this pass; verifier-driven value changes belong to
a separate evidence PR.
