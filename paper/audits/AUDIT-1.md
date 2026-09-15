# Audit 1: first re-derivation pass

Date: 14 Sep 2026. Auditor: yohei/claude (assistant session). Method: live fetch of the cited page, read for the specific claim, verdict per row. Artifacts were not hashed in this pass because the fetches ran outside the repository's container; `python -m bench audit` re-fetches and hashes when run with network access.

Ledger import provenance: github.com/kevinnbass/metr-money-figure, commit f64df65a1640, cloned depth 1 on 14 Sep 2026; found via https://x.com/kevinnbass/status/2099621874279817638.

| row | source fetched | verdict | note |
|---|---|---|---|
| R10 Gleave, board, METR | metr.org/about | CONFIRMED | "Advisor and Board Member" |
| R13 Mascorro, advisor, METR | metr.org/about | CONFIRMED | "Advisor" |
| R16 Radford, advisor, METR | metr.org/about | CONFIRMED | "Advisor" |
| R21 Dattani, board, METR | metr.org/about | CONFIRMED | "Advisor and Board Member" |
| R30 Farhi, donor, METR | metr.org/about | CONFIRMED (donor); employment IMPORTED | named among individual supporters; page also states METR cannot accept donations by or at the direction of frontier AI company employees; timing unresolved |
| R17 Karnofsky, former advisor | metr.org/about | CONSISTENT | absent from live page; Wayback capture needed to confirm the earlier listing |
| R19 Christiano, former board | metr.org/about | CONSISTENT | as above |
| T19 OpenAI in-kind ~$400K | metr.org/about (partnership text) | CONSISTENT | page confirms free tokens from partners; the $400K figure is from METR's investigation post |
| T12 SFF 2025 to METR | survivalandflourishing.fund/2025/recommendations | CONFIRMED | $548,000 total; $120,000 speculation; $428,000 match to 2026-09-30 |
| SFF 2025 components (Palisade $1,133,000; FAR AI $919,000; SaferAI $311,000; SecureBio $754,000; RAND TASP $1,022,000; CAIS $289,000) | same page | CONFIRMED | added as rows T67 to T72; cumulative imported rows reduced by these amounts |
| T13 ARC to METR $4,553,935 | projects.propublica.org summaries | PARTIAL | ARC FY2024 revenue $5.22M and expenses $9.05M and METR contributions $13.6M match; Schedule I line not opened |
| metr-donor-rule-history | metr.org/about | DIFFERS (wording tightened) | live text forbids donations by or at the direction of lab employees; the imported Sept 2025 footnote said individual employee donations were accepted |
| Transluce policy (T rows, N rows) | transluce.org/independence-and-transparency-policy | CONFIRMED | 6% and 32% shares; no developer-organization revenue; no paid evaluations |
| AVERI funding and recusal | averi.org/about | CONFIRMED | funders named; no majority donor; director recused from OpenAI audits |
| Apollo seed investors | apolloresearch.ai PBC post | CONFIRMED | 50Y lead; Macroscopic among participants |

Not re-derived in this pass: every Coefficient index total, every 990-PF negative, the DAF Schedule I rows, Tallinn's public ledger, Wayback captures. These remain `imported`.
