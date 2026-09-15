# AUDIT-4 — imported transfer re-derivation, round 2 (2026-09-15)

The 12 rows blocked by rate limits in round 1, re-fetched with pacing.

- T16 (svcf->metr, daf_grant): **unverifiable** — Cited URL is the generic Nonprofit Explorer homepage (no org- or grant-level data). Fetched SVCF's ProPublica org page (projects.propublica.org/nonprofits/organizations/205205488): it confirms SVCF operates a donor-advised fund but lists no individual grantees; no METR or $20,000
- T30 (eu-budget->transluce, contract): **confirmed** — Transluce 'serving as a contractor to the EU AI Office' (transluce.org/2025-fundraiser)
- T37 (sff->palisade, recommendation): **differs** — ledger=2079627; observed=$1,133,000 (SFF-2025 recommendations, Palisade Research total)
- T38 (tallinn->redwood, daf_grant): **confirmed** — $1,330,000 to Redwood Research on 2021-11-12 via FP-US, 'General support'
- T41 (eu-budget->saferai, contract): **unverifiable** — Fetched safer-ai.org homepage: describes EU standards/policy work (EU AI risk management standards, EU Code of Practice) but mentions no EU funding, grant, or contract of any kind.
- T42 (eu-budget->far-ai, contract): **confirmed** — EC AI Office tender award (EC-CNECT/2025/OP/0032 Lot 1) to FAR.AI-led consortium; amount not stated
- T46 (openai->ukaisi, grant): **unverifiable** — Fetched aisi.gov.uk/grants: the page describes AISI's own outbound grant programmes (Alignment Project, Challenge Fund, Systemic AI Safety Grants). No mention of OpenAI funding to AISI.
- T47 (us-gov->caisi, grant): **confirmed** — $10 million from FY2026 appropriations to CAISI (ifp.org/funding-for-caisi/)
- T53 (salesforce-ventures->hfoai, investment): **differs** — ledger: salesforce-ventures -> hfoai 235000000; observed: $235M Series D round total, Salesforce one of ~9 participants, no per-investor amount
- T56 (anthropic->andon, contract): **unverifiable** — Page confirms Andon Labs 'partnered with Anthropic on Project Vend' (a collaboration). It states no contract, engagement value, or payment.
- T60 (eu-budget->equistamp, contract): **unverifiable** — TED homepage (ted.europa.eu) is a JS shell with no award data. A web search for the Equistamp award surfaced only the tender's Prior Information Notice with maximal lot values (Lot 1: EUR 1.8M); no Equistamp contract award or EUR 1,167,484 figure found.
- T61 (amazon->nemesys, contract): **confirmed** — Nemesys Insights engaged as independent CBRN auditor for Amazon Nova Premier evaluation
