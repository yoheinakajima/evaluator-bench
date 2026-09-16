# Right of reply: Palisade Research

Prepared 2026-09-15. Reply requested within 14 days of sending. This is the complete record Evaluator Bench holds about Palisade Research; nothing else feeds the score. Values are derived from the signals' bounds under RULES.md; the default site view uses the Retrieved & confirmed evidence policy.

## How to reply

- Correct a fact: open a pull request adding a signal with a source, or reply with the rows and sources and we file them as a signal marked `source_type: self`.
- Dispute an anchor: say which anchor text you believe applies and which rule in RULES.md decides it; the resolution field records the disagreement even if the value does not change.
- Publish terms: contract terms on scope, access, and publication rights move the relevant dimensions on their own.
- Hand this to your agent: forward this packet as-is — the agent section below links the machine-readable record and the filing recipe, so nothing else needs uploading or pasting.
- Silence is recorded as silence, not as agreement.

## For your agent

If an AI agent is handling this reply, forward this packet as-is — no separate upload or pasted link needed. Start here:
- Machine orientation: https://evaluatorbench.com/llms.txt
- This organization's full machine-readable record: https://evaluatorbench.com/evaluators/palisade.json
- Filing recipe (repo AGENTS.md, Recipe A): add the source you fetched yourself, then a signal with the exact quote (under 120 characters, copied verbatim), the anchor bound it sets (a cap or a floor), and the RULES.md rule code (e.g. F.3). Open a pull request; CI re-fetches every cited source and checks each quoted span appears verbatim.
- Or file the right-of-reply issue, no PR needed: https://github.com/yoheinakajima/evaluator-bench/issues/new?template=right-of-reply.md
- Rules of evidence: public sources only, quote-minimal spans, no motive or intent claims about any person (RULES 12).

## Current assessments

### Funding: 3/4 (Retrieved & confirmed: 3)
Anchor 3: Mostly philanthropic or public money; some lab-linked pooled funds.
Derivation: Capped at 3 by palisade.09 (F.6): About $3.8M in cumulative Coefficient Giving grants per the index snapshot; Coefficient's principal is an Anthropic Series A investor and board observer by his own account. No bounded negative on lab money is on file.; capped at 3 by palisade.13 (F.6): SFF recommended $1,133,000 to Palisade in 2025 (plus a $928,000 matching pledge); SFF's funder Jaan Tallinn led Anthropic's Series A.; capped at 3 by palisade.14 (F.6): Coefficient / Open Philanthropy recommended $1,680,000 (June 2024) and two grants totaling $2,123,463 (May 2025) to Palisade for general support per archived grant pages, $3,803,463 in all; Coefficient's principal funder is an Anthropic investor.. Floors up to 3 from palisade.01 do not exceed the cap. Not counted under this policy: palisade.11 (no confirmed source (imported, unaudited)).
Curator note: Anchor 3: philanthropic, no lab contracts found, but the main traced funder is two steps from a lab investor and no primary-filing negative is on file.
- [for, floors at 3, F.11] Philanthropically funded; no lab contracts found. Quote: "Contributions $2,887,428 89.3%" Sources: Palisade Research (https://palisaderesearch.org/); Palisade Research Inc, Form 990 FY2024 (Nonprofit Explorer) (https://projects.propublica.org/nonprofits/organizations/931591014); Donate | Palisade Research (https://palisaderesearch.org/donate)
- [against, caps at 3, F.6] About $3.8M in cumulative Coefficient Giving grants per the index snapshot; Coefficient's principal is an Anthropic Series A investor and board observer by his own account. No bounded negative on lab money is on file. Sources: Coefficient Giving grants index (https://coefficientgiving.org/grants/); metr-money-figure research ledger and audits (https://github.com/kevinnbass/metr-money-figure/tree/master)
- [against, caps at 3, F.6] Coefficient Giving's database records two grants totaling $2,123,463 for general support; the imported index total of $3,803,463 is marked differs pending reconciliation. Quote: "$2,123,463 2025-05" Sources: Palisade Research grants (https://www.openphilanthropy.org/grants/); evaluators.csv (24 evaluators: Coefficient and SFF totals, lab money, government contracts, leadership) (https://raw.githubusercontent.com/kevinnbass/metr-money-figure/master/research/evaluators.csv)
- [against, caps at 3, F.6] SFF recommended $1,133,000 to Palisade in 2025 (plus a $928,000 matching pledge); SFF's funder Jaan Tallinn led Anthropic's Series A. Quote: "Palisade Research Main: $477,000 Freedom: $441,000 Fairness: $0 Mean: $216,000 $1,133,000" Sources: SFF-2025 S-Process Recommendations Announcement (https://survivalandflourishing.fund/2025/recommendations); Anthropic raises $124 million Series A (https://www.anthropic.com/news/anthropic-raises-124-million-to-build-more-reliable-general-ai-systems)
- [against, caps at 3, F.6] Coefficient / Open Philanthropy recommended $1,680,000 (June 2024) and two grants totaling $2,123,463 (May 2025) to Palisade for general support per archived grant pages, $3,803,463 in all; Coefficient's principal funder is an Anthropic investor. Quote: "Open Philanthropy recommended two grants totaling $2,123,463 to Palisade Research for general support." Sources: Palisade Research — General Support (Wayback capture 2024-08-05 of the Open Philanthropy grant page) (https://web.archive.org/web/20240805094803/https://www.openphilanthropy.org/grants/palisade-research-general-support/); Palisade Research — General Support (2025) (Wayback capture 2025-10-05 of the Open Philanthropy grant page) (https://web.archive.org/web/20251005184735/https://www.openphilanthropy.org/grants/palisade-research-general-support-2025/); Wayback CDX index of openphilanthropy.org/grants/p* (status 200, one row per URL) (http://web.archive.org/cdx/search/cdx?url=openphilanthropy.org/grants/p*&collapse=urlkey&fl=original&filter=statuscode:200&limit=20000)
- Document request: Request to Palisade Research: the Form 990 Schedule B or a donor list naming contributors above $5,000 for 2024 and 2025, and any policy on accepting money from AI developers.
- Document request: Request to Coefficient Giving: the grant pages for the two Palisade Research general-support grants ($1,680,000 June 2024; $2,123,463 May 2025) so the $2,123,463 figure can be verified against the superseded $3,803,463 index total.

### Governance: 2/4 (Retrieved & confirmed: 2)
Anchor 2: For-profit or PBC with a published COI policy.
Derivation: Floored at 2 by palisade.06 (G.1): Nonprofit.. No admissible signal caps it.
- [for, floors at 2, G.1] Nonprofit. Quote: "Palisade Research is a nonprofit based in Berkeley, California" Sources: Palisade Research (https://palisaderesearch.org/); About Palisade Research (https://palisaderesearch.org/about)

### Personnel: 2/4 (Retrieved & confirmed: 2)
Anchor 2: Frequent two-way hiring; recusal on request.
Derivation: Capped at 2 by palisade.10 (P.3): Founder and executive director previously worked on Anthropic's security team; SFF recommendations of about $3.2M.. Floors up to 2 from palisade.07 do not exceed the cap.
Curator note: Anchor 3 (provisional): no lab board roles found (palisade.07), but the founder and executive director previously worked on Anthropic’s security team (palisade.10) — a former, disclosed lab tie, not a current one. Provisional readings are open to public correction through the contribution path.
- [for, floors at 2, P.6] No lab board roles found. Sources: Palisade Research (https://palisaderesearch.org/)
- [against, caps at 2, P.3] Founder and executive director previously worked on Anthropic's security team; SFF recommendations of about $3.2M. Quote: "In 2022, Jeffrey was helping to build out the security team at Anthropic" Sources: evaluators.csv (24 evaluators: Coefficient and SFF totals, lab money, government contracts, leadership) (https://raw.githubusercontent.com/kevinnbass/metr-money-figure/master/research/evaluators.csv); About Palisade Research (https://palisaderesearch.org/about)
- Document request: Request to Palisade Research: a written statement of any cooling-off or recusal rule for staff formerly employed by evaluated developers, and the start and end dates of the executive director's Anthropic employment as published on the about page.

### Access depth (lab-granted): 1/4 (Retrieved & confirmed: 1)
Anchor 1: Pre-release API with safeguards on.
Derivation: Capped at 1 by palisade.05 (A.1): Little pre-deployment access; most work is on released models..
- [against, caps at 1, A.1] Little pre-deployment access; most work is on released models. Quote: "As the companies shipped model after model, Palisade kept finding what researchers had been warning about for years" Sources: Palisade Research (https://palisaderesearch.org/); About Palisade Research (https://palisaderesearch.org/about)

### Scope control: 3/4 (Retrieved & confirmed: 3)
Anchor 3: Evaluator sets scope and can add questions.
Derivation: Floored at 3 by palisade.02 (S.5): Sets its own questions and publishes without lab review.. No admissible signal caps it.
- [for, floors at 3, S.5] Sets its own questions and publishes without lab review. Quote: "So Jeffrey assembled a team to investigate emerging AI behavior and strategic capabilities." Sources: Palisade Research (https://palisaderesearch.org/); About Palisade Research (https://palisaderesearch.org/about)

### Publication rights: 4/4 (Retrieved & confirmed: 4)
Anchor 4: Full editorial control, record of adverse findings, redaction statements.
Derivation: Floored at 4 by palisade.03 (R.5): Publishes findings unwelcome to labs, including shutdown resistance and self-replication.. No admissible signal caps it.
- [for, floors at 4, R.5] Publishes findings unwelcome to labs, including shutdown resistance and self-replication. Quote: "the first time AI models have been observed preventing themselves from being shut down despite explicit instructions" Sources: Palisade Research (https://palisaderesearch.org/); OpenAI's Skynet moment: Models defy human commands, actively resist orders to shut down (https://www.computerworld.com/article/3999190/openais-skynet-moment-models-defy-human-commands-actively-resist-orders-to-shut-down.html); These AI Models From OpenAI Defy Shutdown Commands, Sabotage Scripts (https://www.techrepublic.com/article/news-openai-models-defy-shutdown-commands/)

### Method transparency: 3/4 (Retrieved & confirmed: 3)
Anchor 3: Tasks or code partly open.
Derivation: Floored at 3 by palisade.04 (M.1): Publishes code and transcripts.. No admissible signal caps it.
- [for, floors at 3, M.1] Publishes code and transcripts. Quote: "View Published Paper Code Access Paper" Sources: Palisade Research (https://palisaderesearch.org/); Shutdown resistance in reasoning models (https://palisaderesearch.org/research/shutdown-resistance); Language Models Can Autonomously Hack and Self-Replicate (https://palisaderesearch.org/research/self-replication)

### Role incompatibility: 3/4 (Retrieved & confirmed: 3)
Anchor 3: Tools are open or free to the ecosystem.
Derivation: Capped at 3 by palisade.12 (X.7): Palisade's FY2024 Form 990 reports $344,829 (10.7% of revenue) from program services; the counterparty is not disclosed.. Floors up to 3 from palisade.08 do not exceed the cap.
- [for, floors at 4, X.7] No commercial products. Sources: Palisade Research (https://palisaderesearch.org/)
- [against, caps at 3, X.7] Palisade's FY2024 Form 990 reports $344,829 (10.7% of revenue) from program services; the counterparty is not disclosed. Quote: "Program Services $344,829 10.7%" Sources: Palisade Research Inc, Form 990 FY2024 (Nonprofit Explorer) (https://projects.propublica.org/nonprofits/organizations/931591014)

## Dissent on the card

- Lower: Access should be 0. Every published Palisade study (shutdown resistance, specification gaming, self-replication, Badllama) ran on released models through public APIs or open weights; no system card names Palisade as a pre-release tester and no engagement with a lab is on record. 'Little' pre-deployment access, with none documented, is anchor 0, and the 1 rests only on the claim's wording.
- Higher: Access should be 2. Palisade's work is cited by Anthropic's CEO and briefed to Congress, and labs have responded to its findings; if any developer supplied early checkpoints or extended API windows for the shutdown or hacking studies, that is anchor 2. The record says 'little', not none, and a single documented pre-release run with extended time would move it.

## Ledger rows naming the organization

- T10: recommendation from coefficient to palisade, 2021-2025, 3803463: cumulative [superseded] https://coefficientgiving.org/
- T37: recommendation from sff to palisade, 2023-2024, 2079627: SFF recommendations 2023 to 2024 (cumulative minus the confirmed 2025 row) [differs] https://survivalandflourishing.fund/
- T66: recommendation from sff to palisade, 2025, 1133000: SFF 2025: $1,133,000 incl. $205,000 speculation grant and $928,000 matching pledge [confirmed] https://survivalandflourishing.fund/2025/recommendations
- T75: grant from coefficient to palisade, 2025-05, 2123463: two grants totaling $2,123,463 for general support (Open Philanthropy grant page, archived) [confirmed] https://web.archive.org/web/20251005184735/https://www.openphilanthropy.org/grants/palisade-research-general-support-2025/
- T91: recommendation from coefficient to palisade, 2024-06, 1680000: general support (Open Philanthropy grant page, archived; amount updated August 2024) [confirmed] https://web.archive.org/web/20240805094803/https://www.openphilanthropy.org/grants/palisade-research-general-support/
- R45: ladish principal at palisade: founder; imported kevinnbass/metr-money-figure:EV19 [imported] https://palisaderesearch.org/about

## What would move the score

Pre-release access on published terms would raise the access score without touching the others.

Replies are filed as signals with the date received. Evaluator Bench: https://github.com/yoheinakajima/evaluator-bench
