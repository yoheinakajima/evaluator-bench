# Process: how a score gets to be trusted

Version 0.3, 14 Sep 2026. This replaces "we read the press and scored it" with a chain that a reviewer, an evaluator, or a critic can re-derive. The model for the money side is the row-level discipline in github.com/kevinnbass/metr-money-figure; the model for the rest is financial-audit evidence practice.

## 1. Evidence tiers

Every source carries a `source_type`:

| tier | type | examples | what it can support |
|---|---|---|---|
| 1 | filing | IRS 990 / 990-PF e-files (with object id), Companies House, SEC Form D, court records, TED tender notices | amounts, dates, officers, related organizations |
| 1 | index | a funder's own grants database with a snapshot date and row count | presence or absence of a grant on that date |
| 2 | ledger | a third party's row-level dataset with cited sources; Wayback captures | leads; becomes tier 1 once re-derived |
| 3 | self | the organization's own site, blog, report, or filing narrative | policies, claims about itself, self-reported funders |
| 4 | press | news, interviews, secondary summaries | roles by their own account, round sizes, statements |

A 4 on funding, governance, or personnel needs at least one tier-1 row. A 0 needs a tier-1 or tier-3 row that the organization has not disputed. Tier 4 alone supports a 2 or a 3.

## 2. The ledger, not the adjective

Money and roles go in `data/ledger/` as rows before they go in a signal. Rules:

- One transfer per row; `measure` is one of grant, recommendation, commitment, transfer, daf_grant, in_kind, investment, contract. Never sum across measures. A recommendation is not a payment; a commitment is not a payment; in-kind is not cash.
- Amounts are numbers or empty. Empty means undisclosed and is reported as a row count, never as a dollar figure.
- Ceilings and floors are labelled as such. A ceiling is never a headline number.
- One role per row, dated where public, public roles only, no motive asserted.
- A person's tie to a lab is coded as the role, not as a judgment about it.

## 3. Bounded negatives

"None found" is a claim with a scope. A negative row names the corpus searched (filing type and years, or index name and row count), the snapshot date, the query, and the source. It supports "not in that corpus on that date" and nothing more. Absence in a 990 filed for 2024 says nothing about a 2026 grant. Absence in a funder's index says nothing about a donor-advised fund routed through a community foundation. The verifier requires a confirmed negative before funding can score 4.

## 4. Audit status

Every ledger row and every source carries `audit_status`:

- `unaudited`: cited from a search result or snippet at curation time; the page has not been fetched in full. Does not satisfy any gate.
- `imported`: copied from another project's ledger; cited to its row id; not re-derived here. Does not satisfy any gate.
- `confirmed`: re-fetched from the cited source by a named person on a date; artifact saved with a SHA-256 in `data/artifacts.csv` (to be added).
- `differs`: re-fetch produced a different number or date; both recorded; the row is quarantined until resolved.
- `unverifiable`: the cited source is gone or paywalled and no substitute exists; the row stays but is flagged.

An audit pass takes a list of row ids, re-fetches each source, records verdicts, and files a dated `paper/audits/AUDIT-<n>.md`. Two independent passes before a release. The figure repo's own audit found 82 of 85 rows confirmed and flagged its rendered figure for overclaiming; that is the standard.

## 5. Exposure by hop

`python -m bench exposure` computes, for each evaluator, inflows by measure and by hop distance from a frontier lab: hop 0 the lab itself; hop 1 an investor, board member, observer, employee, founder, or contractor of a lab; further hops through principals and funders. Board seats, advisors, donors, investors, and office hosts within two hops are listed with their distance. Nothing is added across hops or measures. This is the second-order view the rubric's funding and personnel dimensions were missing.

## 6. Time

Policies move. Signals carry `as_of`; sources carry `capture` (a Wayback URL) where the live page has changed. An evaluator's donor rule is scored as of a date, and the history of the wording is itself evidence. Assessments are re-dated when re-scored; the event log keeps the old ones.

## 7. Open questions

`paper/OPEN-QUESTIONS.md` keeps one entry per unresolved question in the STATE format: status (SETTLED, PARTIAL, OPEN), rows that bear on it, routes already tried, and the single document or event that would close it. Nobody repeats a dead route.

## 8. Right of reply

First publication is one batch. Every score is marked provisional through a public preview window (two weeks), and the reply channel is the same for named organizations and everyone else: a pull request with evidence or the right-of-reply issue template, filed as a signal with the date received. No individual notices go out for changes made while the work was unpublished; those are edits, not events.

After first publication, a score that moves by more than one anchor relative to the last tagged release triggers a record packet to that organization (`bench outreach <id>`) with fourteen days to reply before the change is tagged. Replies are filed as signals; silence is recorded as silence.

## 9. What stays out

Non-public individuals; private communications; screenshots of paywalled pages; inferred motives; any statement about a person's intent. Only what a filing, a page, or the person's own words say.

## 10. Disclosure

Curators state their own relationships to evaluators and labs in the repository. The same disclosure the rubric asks of evaluators.

## 12. What unverified evidence may do to a score

Every source and ledger row carries an audit status. The status limits what a value can be, not just what a sum may include:

- `confirmed`: re-derived from the cited source by a curator or the audit step. Supports any value, subject to the tier rule (a 4 on Funding, Governance or Personnel needs tier-1 evidence, C10).
- `unaudited`: cited from retrieved text or a search result; page not fetched in full here. Supports values 1 to 3 only.
- `imported`: copied from another project's ledger. Supports nothing on its own; it is a lead.
- `differs`, `unverifiable`, `superseded`: quarantined. Support nothing and are excluded from every sum and figure; they stay visible with both values so the disagreement is on the record.

A value of 0 or 4 therefore needs at least one non-superseded signal whose sources are all confirmed; a value of 1 or 3 needs at least one signal with a confirmed or unaudited source; 2 is always supportable (C14). When an assessment cannot meet this, the verifier fails and the curator sets the value to the nearest supportable anchor and marks it `evidence_limited`. The rationale keeps the reading the record would give if the sources held up, and the site shows the mark. The value moves back the moment a live source is confirmed. This keeps a weakly sourced extreme from moving a ranking in either direction, without pretending the weak evidence does not exist.
