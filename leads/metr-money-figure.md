# Lead: kevinnbass/metr-money-figure

Cloned 14 Sep 2026 (depth 1, commit f64df65a1640, authored 2026-09-14 16:55 -0500). Found via https://x.com/kevinnbass/status/2099621874279817638; that tweet is recorded as `discovered_via` on the source record. A third-party investigative ledger behind a rendered figure about METR's funding network. Treated here as leads to re-derive, not as findings.

## What it contains

- `research/money_flows.csv` (150 rows): funder to recipient transfers with measure, date, amount, source URL. Includes 24 bounded negatives (rows M97 to M124) where a named funder's 990 or 990-PF was checked and no METR-named grant found.
- `research/finances.csv` (59 rows): METR and ARC 990 line items with e-file object ids; officer compensation; the $4.55M ARC to METR spin-out transfer.
- `research/board.csv`, `christiano.csv`, `arrivals.csv`: board, advisors, and personnel moves with roles and sources.
- `research/donor_rule.csv` (38 rows): Wayback captures of METR's donor-rule wording from April 2024 to December 2025.
- `research/evaluators.csv` (24 rows): a parallel evaluator scorecard with Coefficient and SFF totals per organization.
- `research/compute_inkind.csv`, `evals.csv`, `lab_statements.csv`, `hf_case.csv`, `aef1.csv`: in-kind credits, engagement ledger, verbatim lab statements, the HF investigation report scored against AEF-1.
- `research/AUDIT-3A.md` to `AUDIT-3D.md`: per-row re-fetch verdicts with SHA-256 artifacts (82 confirmed, 2 differs, 1 unverifiable in 3A).
- `research/STATE.md`: per-question status with routes tried and what would close each.

## What its own audit says about the figure

Audit 3A: the arithmetic recomputes, but the rendered figure's legend labels every Coefficient and SFF pipe as "Good Ventures money", calls SVCF and NPT accounts Coefficient's own, states Redwood worked on both investigations where the cited record does not say so, and prints an unqualified "Direct: $0" that the record search cannot establish. The dataset is stronger than the figure.

## What we imported

Rows tagged `imported` in `data/ledger/` with the originating row id in `notes`. None has been re-derived here. Five negatives (N01 to N05), fourteen transfers, and about twenty relationships. Two assessments changed on the strength of them, each re-dated and carrying open questions: METR funding 4 to 3, METR personnel 3 to 2. Palisade funding 4 to 3 for the same gate.

## Re-derivation status

First pass in `paper/audits/AUDIT-1.md`: 28 of 68 inflow rows confirmed, mostly from metr.org/about, the SFF 2025 recommendations page, ProPublica summaries, and three organizations' own policy pages. One wording difference found (METR's donor rule is now tighter than the imported September 2025 footnote). `python -m bench audit --all-imported` re-fetches and hashes the rest when run with network access.

## Re-derivation plan

1. Fetch each cited 990 e-file object id from the IRS AWS datalake; save with SHA-256; confirm the line items.
2. Fetch the Coefficient index; confirm the METR-string search and the per-evaluator totals.
3. Fetch the SFF recommendation pages and Tallinn's public ledger; confirm recommendations against DAF Schedule I rows.
4. Fetch dated Wayback captures for the donor rule and the team page.
5. Send METR the rows and the two changed assessments for reply.

## What we did not import

Media-outlet bias ratings, amplifier accounts, and anything about journalists. Out of scope for an evaluator independence dataset.
