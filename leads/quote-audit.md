# Quote audit

Run: 2026-09-15. Normalizer: `bench.review.fetch_text`; curl fallback where noted (see `leads/quote_audit.py`).
A quote counts as found only if it is an exact substring of the normalized text of at least one cited source.

- signals with a `quote`: 43
- found: 36
- not found: 6
- fetch failed: 1

## Found, with a fetch caveat

- rand.10: `rand-audacious-2024` via fetch_text. rand.org (CloudFront) returned HTTP 403 to fetch_text and to the bare `curl -A Mozilla/5.0` form on the first run of 2026-09-15 but served normally with full browser headers; a re-run the same day fetched normally with fetch_text. Treat this source as flaky in CI.

## Not found

### apollo.13
- checked: `apollo-pbc-mission` (https://www.apolloresearch.ai/blog/apollo-research-is-becoming-a-pbc) via fetch_text
- claim: Mission seats on the PBC board are held by directors independent of the company and its funders, with a mandate to prioritize mission.
- original quote: "held by "mission directors" who are independent to Apollo Research PBC and our funders"
- suggested span: "held by “mission directors” who are independent to Apollo Research PBC and our funders"
- note: Same sentence; the page uses curly quotes (U+201C/U+201D) where the signal used straight quotes.

### averi.10
- checked: `averi-funding` (https://www.averi.org/about) via fetch_text
- claim: Executive director recused from auditing OpenAI for at least two years after leaving and sold eligible shares; team members' individual holdings disclosed; mandatory recusal for material conflicts.
- original quote: "recused from directly auditing OpenAI for at least two years"
- suggested span: "recused from directly auditing OpenAI until two years after his October 2024 departure"
- note: Page wording differs from the signal ('until two years after his October 2024 departure' vs 'for at least two years').

### farai.12
- checked: `far-30m` (https://www.far.ai/blog/30m-multi-funder-support) via fetch_text
- claim: Largest single grant: $28,675,000 over three years from Coefficient Giving (September 2025); over $30 million in 2025 commitments from Coefficient, Schmidt Sciences, SFF, CSET and the Frontier Model Forum's AI Safety Fund.
- original quote: "a grant of $28,675,000 over three years to FAR.AI"
- suggested span: "FAR.AI secured over $30 million of funding commitments in 2025"
- archive: original quote is verbatim in Wayback capture https://web.archive.org/web/2025id_/https://www.openphilanthropy.org/grants/far-ai-general-support/
- note: op-far-general-support (openphilanthropy.org) now 301s to coefficientgiving.org/funds/, a generic page. The original quote is verbatim on a Wayback capture of the OP page (see archive line). The $28,675,000 figure is not on any live cited page.

### metr.21
- checked: `instrumentl-arc-990` (https://www.instrumentl.com/990-report/alignment-research-center) via fetch_text
- claim: Second-hop routes for METR's philanthropic money: ARC (a $4,553,935 grant to METR in its 2024 filing, per a 990 extraction) was itself funded by Coefficient; Longview (a pooled fund named by METR) received a $15,961,273 operational grant from Coefficient; Constellation, which shares people with METR, received $16,750,000.
- original quote: "contributed $4,553,935 in grants during 2024"
- suggested span: "Alignment Research Center, operating as a public charity in Covina, CA, provided $4,553,935 in grants in 2024"
- note: Instrumentl reworded its summary; the page never names METR as recipient (it shows '1 awards in 2024' behind a sign-up wall). op-longview and op-constellation now redirect to coefficientgiving.org/funds/; their figures ($15,961,273; $16,750,000) are verbatim on Wayback captures.

### palisade.11
- checked: `evaluators-ledger` (https://github.com/kevinnbass/metr-money-figure/blob/master/research/evaluators.csv) via fetch_text
- claim: Coefficient Giving's database records two grants totaling $2,123,463 for general support; the imported index total of $3,803,463 is marked differs pending reconciliation.
- original quote: "two grants totaling $2,123,463 to Palisade Research for general support"
- suggested span: "Coefficient name matched: 'Palisade Research' ($1,680,000 2024-06; $2,123,463 2025-05)."
- note: op-palisade cites the generic OP grants index, which never carried Palisade text and now redirects to coefficientgiving.org/funds/. The original quote is verbatim on the Wayback capture of openphilanthropy.org/grants/palisade-research-general-support-2025/ (Amount $2,123,463, May 2025, 'two grants'); that page also lists a separate $1,680,000 2024 grant, so the imported $3,803,463 index total = 1,680,000 + 2,123,463 and the 'differs' flag can be reconciled.

### securebio.01
- checked: `securebio-oaif` (https://securebio.org/blog/three-day-early-warning-system/) via fetch_text
- claim: Labs typically pay for evaluations of their own models; OpenAI covered the cost of the GPT-5.5 assessment.
- original quote: "OpenAI PBC covered SecureBio's costs for the GPT 5.5 evaluation"
- suggested span: null (no supporting span on any cited page)
- note: The cited page never carried this sentence. No SecureBio page states that OpenAI covered the GPT-5.5 assessment; see fixes.securebio.01 for the nearest supported statement (GPT-6 Astra and GPT-5.6 Sol full reports).

## Fetch failed

### grayswan.02
- source: `forbes-grayswan-2024` (https://www.forbes.com/sites/sarahemerson/2024/10/29/this-hacker-team-is-bulletproofing-ai-models-for-companies-like-openai/)
- fetch failed: fetch_text HTTPError: HTTP Error 403: Forbidden; curl -A Mozilla/5.0 returned 54 chars (bot wall); curl with browser headers returned 54 chars (bot wall)
- archive: original quote is verbatim in Wayback capture https://web.archive.org/web/2025id_/https://www.forbes.com/sites/sarahemerson/2024/10/29/this-hacker-team-is-bulletproofing-ai-models-for-companies-like-openai/
- note: forbes.com returns HTTP 403 to fetch_text and a 'Please enable JS' shell to every curl form. The quote is verbatim in the Wayback capture (web.archive.org/web/2025id_/<url>). Suggest adding an `archive` field to forbes-grayswan-2024.

## Fixes

### securebio.01
- new source `securebio-gpt6-astra-report`: Pre-Release Assessment of OpenAI's GPT-6 Astra (full technical report, PDF) (https://securebio.org/resources/gpt-6-astra-assessment.pdf), published 2026-09-14
- quote: "SecureBio received compensation from OpenAI limited to covering the costs of this assessment"
- note: Linked as 'full technical report' from https://securebio.org/blog/gpt-6-astra-pre-release-testing-report/ (published September 14, 2026). Section 'Independent Evaluations' and the AEF-1 checklist (item 2.1, 2.4) state that OpenAI's payment was limited to covering SecureBio's costs (tokens, compute, employee time), agreed in advance, not contingent on findings; the report was reviewed by OpenAI before publication with no substantive edits. Fetched 2026-09-15, SHA-256 dcedf0d32944...; text extracted with pdftotext (poppler) and whitespace-collapsed. CAUTION: bench.review.fetch_text does not extract PDF text, so CI will report this quote NOT FOUND; see 'alternatives' for an HTML span CI can check.
- claim: No SecureBio page states that OpenAI covered the GPT-5.5 assessment. The GPT-5.5 post (securebio.org, April 9, 2026; Substack copy April 23, 2026) carries no funding disclosure and links only OpenAI's system card. The claim should be re-scoped to GPT-6 Astra (this source) or GPT-5.6 Sol (alternative 1), whose full reports carry the same sentence.
- alternative `securebio-gpt56-sol-report` (https://securebio.org/reports/gpt-5-6-sol-assessment.pdf, 2026-07-23): "SecureBio received compensation from OpenAI limited to covering the costs of this assessment" -- Same sentence as the GPT-6 report. The PDF text layer contains zero-width spaces (U+200B) between some words, so the span matches only after stripping U+200B. Also mirrored at /resources/gpt-5-6-sol-assessment.pdf.
- alternative `securebio-ai-principles` (https://securebio.org/ai/principles/, 2026-07-03): "For some engagements with for-profit firms, we request funding to cover the costs of running the assessments" -- HTML page; this span is verbatim under fetch_text, so CI can check it. It supports the general half of the claim ('labs typically pay for evaluations of their own models') but names no model or lab. Substack copy dated 2026-07-03.
