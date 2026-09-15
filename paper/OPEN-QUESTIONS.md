# Open questions

One entry per question. Status: SETTLED (rows cited, figure-ready), PARTIAL (rows exist, a named gap remains), OPEN (nothing settles it). "Tried" lists routes already used. "Closes it" names what would settle it.

## Q1. Does any of METR's money originate with people or funds holding stakes in the labs it evaluates? PARTIAL
- Rows: ledger T11-T19, T21, T101, R01-R08, N01-N05, N22-N24 (T14 and T21 confirmed; N02, N04, N05 confirmed; N01 replaced by N22/N23; N03 corrected to name the three Schmidt-family filers).
- Known: no direct grant from Coefficient in its index (index no longer public; substitute corpora checked instead); SFF recommendations funded by an Anthropic Series A investor; ARC spin-out transfer seeded by Coefficient and SFF; Vanguard Charitable confirmed at $4,000,000 (FY2025 Schedule I), donor not public; TED Foundation confirms it does not fund grantees directly, and the Audacious/Canary partner payments found (Valhalla, High Tide) go to RAND, not METR.
- Tried: Good Ventures, Pew, Packard, Schmidt-family, and TED Foundation 990/990-PF filings (IRS e-file XML and ProPublica full-text renders); Wayback CDX index of former Open Philanthropy grant pages; ProPublica's cross-filing full-text search.
- Closes it: METR's own dated funder list with amounts, the DAF sponsors' donor attributions, or a TY2025 Audacious partner filing (due late 2026).

## Q2. When did METR's no-lab-money rule take effect, and what does it exclude? PARTIAL
- Rows: source metr-donor-rule-history (imported DR01-DR12); metr-about re-fetched 2026-09-14; metr-coi-policy (v1.0, 28 Aug 2026) added in the evidence pass, giving a dated recusal and board-eligibility policy.
- Known: no rule on the April 2024 page; footnote wording appears April 2025 and changes through September 2025. The live page now says METR cannot accept donations by or at the direction of frontier AI company employees, and its donor list includes a person who holds an OpenAI role; free credits accepted. Document request (RULES 12): the date of that gift and the version of the donor rule in force on that date, from METR or the donor; no inference is drawn until one arrives.
- Closes it: METR's own dated policy document, or direct Wayback re-derivation.

## Q3. What are the terms of the Anthropic embedded-evaluator engagement (scope, selection, pay, publication)? OPEN
- Rows: sources anthropic-pace-frontier, anthropic-amodei-x-pace-frontier, openai-altman-embedded-pledge (primary statements, added 15 Sep evening) alongside unite-altman-match, marktechpost-pace (aggregator press).
- Closes it: the written agreement, or a METR post describing it in the style of the OpenAI investigation terms.

## Q4. Which evaluators have lab investors or lab-tied board members, across the whole population? PARTIAL
- Rows: R10-R29, T20-T26.
- Known for METR, Gray Swan, Irregular (now also a $3,000,000 Good Ventures equity stake, T90), Apollo (Macroscopic investment, imported; round size and stake bounded-open per N25), FAR.AI (AISF), SecureBio (OAIF).
- Closes it: a board and investor pass over all 24 ranked evaluators from team pages, Companies House, and round announcements.

## Q5. Did Coefficient Giving fund Irregular, and for what? SETTLED
- Rows: T09 (confirmed), T88, T89 (Good Ventures payments), T90 (equity stake).
- Good Ventures' FY2024 990-PF records a $4,533,333 grant to Pattern Labs Tech Inc dated 2024-03-05, "developing software tools, products and analysis focused on global security," with $2,266,667 paid in FY2025 — $6,800,000 against the index's $6,799,999. The same filing lists a $3,000,000 equity stake. See `paper/audits/AUDIT-7.md`.

## Q6. What is the dollar value of in-kind compute and access across evaluators? OPEN
- Note: as of decision D-004, in-kind evaluation credits are not scored as lab money and are recorded on entity pages rather than in the funding value; this question is now about the ledger's descriptive coverage, not about a value any card carries.
- Rows: T19 (METR, ~$400K for one investigation).
- Closes it: evaluators reporting credits received per year; labs reporting credits granted.

## Q7. Which trigger incidents met the Dataset B criterion and were followed by nothing? OPEN
- Closes it: per-regime enumeration from incident databases, coded before looking at what followed.

## Q8. Per-evaluator gaps after the population pass PARTIAL
- Rows: ledger T01-T103, R01-R66, N01-N27; population summary from `bench exposure`: 24 ranked evaluators, 10 with a direct lab tie (hop 0), 15 with an inflow from a lab or a lab-tied party, 70 of 103 ledger transfer rows confirmed.
- No ledger rows yet: Dreadnode, Humane Intelligence, assurance firms. HAL is retained out of scope (decision D-001) and no longer tracked here. Closes it: team pages, 990s or Companies House, round announcements.
- Transluce: employee-donor shares confirmed from its own policy; names and sizes not public. Closes it: the FY2026 disclosure.
- Apollo: seed round size and Macroscopic's share — checked against EDGAR and Companies House on 15 Sep 2026 (N25); genuinely not in the public record for a Delaware PBC. Closes it: Apollo's or Macroscopic's own disclosure.
- SaferAI: the unnamed major AI company advisory client. Closes it: SaferAI naming it.
- Irregular: purpose of the Coefficient grant — settled, see Q5.
- UK AISI: whether Alignment Project money touches evaluation work — the payer structure is settled (funds go directly to the host organisation under each funder's own agreement, not into AISI's core budget); whether the Alignment Project team is organisationally separate from AISI's evaluation teams is not stated anywhere fetched. Closes it: AISI naming the team's reporting line.
- CAISI, EU AI Office: EU AI Office's funding source is settled by statute (N27). CAISI's public funding is now a primary-source floor (N26), but a full negative on lab money needs a NIST procurement or CRADA register, not searchable online. Closes it: NIST publishing that register, or naming it.

## Q9. Research pass of 15 Sep 2026 (see paper/audits/AUDIT-2.md) PARTIAL
- Closed or extended: Audacious funder collective (second hop for METR and RAND); Gray Swan Series A investors; Alignment Project backers; Epoch's client list incl. xAI; G42 as SaferAI client; component grants for FAR.AI, Redwood, Epoch; CAISI's FY2026 total.
- Contradictions to reconcile: Coefficient to Palisade ($2.12M vs $3.80M) — resolved, see Q10; Coefficient to Apollo ($1.5M self-report vs $4.41M index) — resolved, see Q10. Coefficient to Irregular — resolved, see Q5.
- Unchanged gaps: Farhi; SaferAI's client; Kolter recusal text; DAF Schedule I lines; Transluce donors; SEAL and CAISI terms.

## Q10. Re-derivation pass of 15 Sep 2026, evening (see paper/audits/AUDIT-7.md) PARTIAL
- Settled: Irregular's $6.8M grant (Q5); Palisade's two grants sum to the existing $3,803,463 figure, the "contradicted" flag was wrong; SecureBio's full grant history, previously absent from the ledger entirely.
- Closed or extended: METR's five negatives re-derived from primary filings (four confirmed, one corrected, one replaced with two substitutes after the source index went offline); METR's largest confirmed single grant identified (Vanguard Charitable, $4,000,000, FY2025); the EU AI Office's funding source settled by statute; CAISI's public funding grounded in the FY2026 appropriations text; UK AISI's Alignment Project payer structure clarified.
- Bounded-open, not merely untried: Apollo's seed round size and Macroscopic's stake (no Form D, no UK share allotment, a Delaware PBC with no public cap table); METR's Audacious/Canary share at the METR level (TED does not fund grantees directly, and neither traced partner payment names METR); CAISI's full lab-money negative (USAspending cannot see a CRADA or reimbursable agreement).
- Two new rule codes: F.13 (partial bounded negatives), G.8 (undisclosed board composition).
