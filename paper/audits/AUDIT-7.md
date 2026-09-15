# AUDIT-7: re-derivation of eight open questions from primary records, 15 September 2026

Scope: the eight open questions in `paper/OPEN-QUESTIONS.md` and `paper/PROCESS.md` that a public filing, a statute, or a corporate register could settle without asking the organization. Work was done by Claude in one pass, every fact traced to a URL opened on 2026-09-15, every quoted span checked as an exact substring of `bench.review.fetch_text` output (or, where that tool cannot read the page — gzip-served renders, a POST-only API, OCR on a scanned PDF — recorded as such). Raw output: `leads/rederive.json`, `leads/rederive.md`. Applied by `leads/apply_rederive.py`, reasoned through by hand rather than merged mechanically. Settled: 3 of 8. Partial: 5 of 8. Nothing came back fully open, though three sub-questions have no public record to settle them at all (recorded below).

## What moved

**METR negatives N02, N04, N05 confirmed; N03 corrected; N01 replaced.** Good Ventures, Pew, and Packard's 990/990-PF filings for the relevant years, pulled from IRS e-file XML, name no METR or Model Evaluation and Threat Research grant; N03's wording was wrong (Schmidt Sciences does not file a 990; the negative now names the three Schmidt-family foundations that do). N01, "no grant in Coefficient's index," could not be re-derived: coefficientgiving.org/grants/ has been 404 since the November 2025 rebrand, in every Wayback capture and live. Two substitute negatives replace it: 2,737 archived Open Philanthropy grant-page slugs have no METR page (N22), and ProPublica's full-text index of e-filed 990s names METR in eight filings, none from the checked funders (N23).

**METR's largest single confirmed grant: Vanguard Charitable, $4,000,000, FY2025.** Schedule I of Vanguard's 990 for the year ending June 2025 names METR at $4,000,000; the same filing pays ARC $1,500,000 (the ARC row is now in the ledger as a second-hop route, T101). The underlying donor is not public, consistent with a donor-advised fund; T14 moves from unverifiable to confirmed. The Audacious/Canary share (~$17M) stays unconfirmed at the METR level: TED Foundation's own 990-PFs show it does not fund grantees directly, and the two Audacious partner filings found (Valhalla $10M, High Tide $333,334) pay RAND, not METR (new signal metr.26, recorded as informational rather than forced into a for/against bound it doesn't earn).

**Irregular / Pattern Labs' $6.8M grant: settled.** Good Ventures' FY2024 990-PF records a $4,533,333 grant to Pattern Labs Tech Inc dated 2024-03-05, "developing software tools, products and analysis focused on global security," with the remaining $2,266,667 paid in FY2025 — $6,800,000 against the imported index's $6,799,999. The same filing lists a $3,000,000 equity stake in the company among Good Ventures' corporate holdings, a second-hop ownership tie now in the ledger (T90). T09 moves from differs to confirmed.

**Palisade's two grants: settled, and the "contradicted" flag on T10 was wrong.** $1,680,000 (June 2024) plus $2,123,463 (May 2025, two grants) sum to exactly $3,803,463, the figure T10 already carried. T75 is promoted to confirmed; T10's note is corrected.

**SecureBio's full grant history is in the ledger for the first time.** Six Open Philanthropy awards, November 2022 to March 2025, about $9.48M total, of which only $55,548 sits in the AI focus area; the rest is biosecurity work outside this project's scope. Payments are visible in Good Ventures' 990-PFs across three fiscal years.

**Apollo:** the $4.41M index total decomposes into two confirmed grants ($1,535,480 and $2,178,700) and a third, $696,000, that exists only in a since-removed third-party index and stays imported. The seed round's size and Macroscopic Ventures' stake are not derivable from public records: no Form D in EDGAR, no share allotment at Companies House, and the PBC is a Delaware entity that publishes no cap table — this is genuinely bounded-open, not merely untried (new negative N25). The board's mission-seat structure is named; only the first mission director is; the rest of the board is not published anywhere fetched (new signal apollo.18, capped under a new rule, G.8).

**CAISI's public funding is now a primary-source floor; a full lab-money negative is not yet possible.** The FY2026 Commerce-Justice-Science appropriations text funds CAISI's work within a $55M NIST AI line. USAspending's award search returns nothing for CAISI under any of three keywords, but USAspending records federal outflows only and cannot show a lab paying NIST; a NIST CRADA or reimbursable-agreement register, which could, was not searchable online. New negative N26 states exactly that boundary rather than overclaiming it.

**The EU AI Office's funding source is settled by statute.** Commission Decision C(2024) 390, Article 8, names only Digital Europe Programme and DG CONNECT staff funding, no non-Union source (new negative N27, new signal euaio.14).

**UK AISI's Alignment Project: the pool is not AISI's own budget.** AISI's Clarification Questions and grant-agreement template both state the funding agreement runs between each funder and the host organisation directly, with AISI as selector and, for its own tranche, statutory grantor under the Science and Technology Act 1965. OpenAI's £5.6m therefore funds grants under OpenAI's own agreement, not AISI's core budget — corroborating T46's existing framing rather than changing it. Whether the Alignment Project team is organisationally separate from AISI's evaluation work is not stated anywhere fetched, and stays open.

## Rules added

Two rule codes the pass needed did not exist: **F.13** (confirmed bounded negatives covering part, but not all, of a funder base float the funding floor to 3, short of what F.12 requires for a 4) and **G.8** (a disclosed board structure with an undisclosed full membership caps governance at 3, short of G.7's requirement for a 4). Both are in `RULES.md`.

## What did not change

No stored assessment value moved: `python -m bench.apply_bounds --recompute-only` reports nothing changed. Every new signal's bound (floor 3 or cap 3) sits at or looser than the value each evaluator's dimension already carried from other, tighter evidence. The pass improves the evidence tier, the quote count, and the confirmed-row share behind existing numbers; it does not, on its own, move any card.

## Numbers, before and after this pass

| | Before | After |
|---|---|---|
| Sources | 194 (100 self, 21 tier-1 among ranked citations) | 247 (232 confirmed) |
| Ledger transfers | 84 (49 confirmed) | 103 (70 confirmed) |
| Checked and not found (bounded negatives) | 21 | 27 |
| Signals (ranked + retained) | 357 | 369 |
| Signals with a quoted span | 309 | 320 |

## What stays open, and why nothing further can close it from a desk

- **METR's Audacious/Canary share at the METR level** (metr.26): TED does not fund grantees directly, and neither Audacious partner filing found names METR; the number rests on METR's and RAND's own statements until a TY2025 partner filing, due late 2026, surfaces.
- **Apollo's seed round size and Macroscopic's stake** (N25): no Form D, no UK share allotment, no public cap table for a Delaware PBC. Only Apollo's or Macroscopic's own disclosure closes this.
- **Apollo's full board** beyond the first mission director and the UK subsidiary's two officers: not published anywhere fetched.
- **CAISI's lab-money negative, in full**: bounded to USAspending and NIST's public MOU announcements; a NIST procurement or CRADA register, if one is searchable, would close it.
- **The UK Alignment Project's organisational separation** from AISI's evaluation teams: no page states it either way.

## Pages that blocked the pass

coefficientgiving.org (403 live, 404 to the site's own former grant pages, and 404 in every Wayback capture since 2025-12-06); ProPublica's `download-xml` (403) and `full_text` (gzip-encoded, unreadable to `fetch_text` without local decompression — every filing read this way is noted); congress.gov and commerce.gov (403); the Wayback `id_` raw mode (compressed bytes); USAspending (POST-only API); the ProPublica organization-search API (answers a zero-result query with HTTP 404); Apollo's team-page director filter (client-rendered, no text to a reader without JavaScript).
