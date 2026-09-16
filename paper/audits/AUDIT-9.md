# AUDIT-9: second-coder pass over every remaining stored 0 or 4, 15 September 2026

Scope: the 15 ranked assessments with stored value 0 or 4 (and evidence, i.e. not
unevidenced) that had no second-coder row in `data/coding/second-coder.csv` — the full
set failing gate "Every extreme has a second coder" as of 2026-09-15.

Method (AGENTS.md Recipes A/B): each binding signal's quoted span was checked as an exact
substring of a fresh `bench.review.fetch_text` fetch of its `quote_source` URL, with the
surrounding context read to confirm the span supports the signal's claim. No new signals
or sources were needed: every binding span verified verbatim, and every 4's binding
signal already carries at least two sources (AGENTS.md's "a 4 needs a span and a second
source"). Rows were appended to `data/coding/second-coder.csv`; the coder field records
the independent pass. Nothing disagrees with any stored value; no assessment moved.

| extreme | binding signal(s) | source fetched | sha | verdict | note |
|---|---|---|---|---|---|
| averi.A (0) | averi.16 | https://www.averi.org/ourwork/averi-pilot-report-the-worlds-first-double-blind-eval | 75c7a18eac5a | CONFIRMED | "The pilot tested Gemini 2.5 Flash-Lite"; page context confirms the only completed engagement was the enclave pilot, no weights access — cap 0 stands |
| euaio.S (4) | euaio.13 | https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-92 | 3c3415415373 | CONFIRMED | span is Article 92(3): the Commission may request access to the GPAI model via APIs or technical means — legal access power under S.4 |
| euaio.X (4) | euaio.09 | https://digital-strategy.ec.europa.eu/en/policies/ai-office | c8dcb4a6edb3 | CONFIRMED | span confirms the AI Office enforces GPAI rules as a public body; no commercial products — X.7 floor 4 |
| grayswan.X (0) | grayswan.04 | https://www.grayswan.ai/news/gray-swan-announces-series-a | 9c727043168e | CONFIRMED | span names Cygnal and Shade; page confirms Gray Swan sells them to enterprises/labs it evaluates — X.1 cap 0 |
| metr.A (4) | metr.04 | https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/ | a113698311d0 | CONFIRMED | span confirms two METR staff plus a Redwood contractor worked on premises at OpenAI over six days — A.5 floor 4 |
| metr.X (4) | metr.22 | https://projects.propublica.org/nonprofits/organizations/991219864 | cab41da17a3a | CONFIRMED | span is the extracted FY2024 990 revenue table: contributions $13,603,035, program services $0 — X.7 floor 4 |
| mlcommons.A (0) | mlcommons.10 | https://www.averi.org/ourwork/averi-pilot-report-the-worlds-first-double-blind-eval | 75c7a18eac5a | CONFIRMED | span confirms AVERI, OpenMined and MLCommons could not see the model's weights; only documented engagement was the released-model pilot — A.1 cap 0 |
| msft.G (0) | msft.02, msft.09 | https://learn.microsoft.com/en-us/security/ai-red-team/ ; https://www.microsoft.com/en-us/security/blog/2025/01/13/3-takeaways-from-red-teaming-100-generative-ai-products/ | 93f37088044d ; f328cd18687a | CONFIRMED (both) | both spans confirm Microsoft's AI Red Team is a Microsoft business unit operating since 2018 — G.6 cap 0 |
| msft.P (0) | msft.06 | https://learn.microsoft.com/en-us/security/ai-red-team/ | 93f37088044d | CONFIRMED | span confirms the red team is a Microsoft unit — P.7 cap 0 |
| palisade.R (4) | palisade.03 | https://palisaderesearch.org/ | 0601ddf86087 | CONFIRMED | span is the shutdown-resistance finding quote; Palisade publishes findings unwelcome to labs — R.5 floor 4 |
| redwood.A (4) | redwood.03 | https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/ | a113698311d0 | CONFIRMED | span names the Redwood Research staff member contracting with METR for the on-site investigation — A.5 floor 4 |
| scale.F (0) | scale.01 | https://www.cnbc.com/2025/06/18/scale-ai-not-winding-down-following-meta-deal-interim-ceo-says.html | 95512e5ec457 | CONFIRMED | span confirms Meta's 49% stake after the $14.3B investment — F.1 cap 0 |
| scale.G (0) | scale.10 | https://www.cnbc.com/2025/06/18/scale-ai-not-winding-down-following-meta-deal-interim-ceo-says.html | 95512e5ec457 | CONFIRMED | span confirms Meta 49% stake plus founder departure for Meta — G.6 cap 0 |
| scale.P (0) | scale.05 | https://www.cnbc.com/2025/06/18/scale-ai-not-winding-down-following-meta-deal-interim-ceo-says.html | 95512e5ec457 | CONFIRMED | span confirms founder Alexandr Wang departed Scale for Meta under the deal — P.7 cap 0 |
| ukaisi.X (4) | ukaisi.10 | https://regulations.ai/regulations/RAI-GB-NA-ASIRRXX-2025 | d560159ea362 | CONFIRMED | span confirms the Institute is an advisory technical research body, not a formal regulator; no commercial products — X.7 floor 4 |

## Outcome

15 of 15 extremes second-coded; 16 binding spans, all CONFIRMED verbatim against live
fetches. Stored values unchanged; gate "Every extreme has a second coder" now passes.
Remaining gate work: the quoted-span gate (21 binding signals without spans) and the
outreach gate were out of scope for this pass.
