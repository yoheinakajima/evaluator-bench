# Right of reply: Epoch AI

Prepared 2026-09-15. Reply requested within 14 days of sending. This is the complete record Evaluator Bench holds about Epoch AI; nothing else feeds the score. Values are derived from the signals' bounds under RULES.md; the default site view uses the Retrieved & confirmed evidence policy.

## How to reply

- Correct a fact: open a pull request adding a signal with a source, or reply with the rows and sources and we file them as a signal marked `source_type: self`.
- Dispute an anchor: say which anchor text you believe applies and which rule in RULES.md decides it; the resolution field records the disagreement even if the value does not change.
- Publish terms: contract terms on scope, access, and publication rights move the relevant dimensions on their own.
- Hand this to your agent: forward this packet as-is — the agent section below links the machine-readable record and the filing recipe, so nothing else needs uploading or pasting.
- Silence is recorded as silence, not as agreement.

## For your agent

If an AI agent is handling this reply, forward this packet as-is — no separate upload or pasted link needed. Start here:
- Machine orientation: https://evaluatorbench.com/llms.txt
- This organization's full machine-readable record: https://evaluatorbench.com/evaluators/epoch.json
- Filing recipe (repo AGENTS.md, Recipe A): add the source you fetched yourself, then a signal with the exact quote (under 120 characters, copied verbatim), the anchor bound it sets (a cap or a floor), and the RULES.md rule code (e.g. F.3). Open a pull request; CI re-fetches every cited source and checks each quoted span appears verbatim.
- Or file the right-of-reply issue, no PR needed: https://github.com/yoheinakajima/evaluator-bench/issues/new?template=right-of-reply.md
- Rules of evidence: public sources only, quote-minimal spans, no motive or intent claims about any person (RULES 12).

## Current assessments

### Funding: 2/4 (Retrieved & confirmed: 2)
Anchor 2: Labs pay per engagement; otherwise diversified.
Derivation: Conflict: floor 3 from epoch.05 (F.6) against cap 2 from epoch.01, epoch.11, epoch.13 (F.3, F.3, F.3); resolved at 2 by F.3: F.3 fee cap decides; the philanthropic floor is itself limited to 3 by F.6.
Curator note: Anchor 2 on funding given the cited signals. Curator disclosure (2026-09-15): the curator holds small public-market shareholdings in Google and Meta. This evaluator has a confirmed ledger tie to Google (contract row T35). Per the disclosure Rule, this assessment is flagged for public review: the rationale names the holding so readers can weigh it, and any reader can file a correction through the contribution path.
Resolution: F.3 decides 2: F.3 fee cap decides; the philanthropic floor is itself limited to 3 by F.6.
- [against, caps at 2, F.3] OpenAI commissioned and owns most of FrontierMath and had the problems and solutions; a contract barred disclosing this until the o3 launch. Quote: "we cannot share the questions and answers with other parties without written permission from OpenAI" Sources: Clarifying the creation and use of the FrontierMath benchmark (https://epoch.ai/latest/openai-and-frontiermath); OpenAI quietly funded independent math benchmark (https://the-decoder.com/openai-quietly-funded-independent-math-benchmark-before-setting-record-with-o3/)
- [for, floors at 3, F.6] Primarily philanthropically funded (Open Philanthropy). Quote: "Epoch AI, a nonprofit primarily funded by Open Philanthropy" Sources: AI benchmarking organization criticized for waiting to disclose funding from OpenAI (https://techcrunch.com/2025/01/19/ai-benchmarking-organization-criticized-for-waiting-to-disclose-funding-from-openai)
- [against, caps at 2, F.3] Transparency page lists Google DeepMind and OpenAI as paying consultation clients and a $600K Tallinn DAF gift; Coefficient grants of about $24.5M per index. Quote: "Google DeepMind 2026 Evaluating the AI co-mathematician on FrontierMath 2025 Model Evaluations" Sources: Transparency (https://epoch.ai/about/transparency); Coefficient Giving grants index (https://coefficientgiving.org/grants/)
- [against, caps at 2, F.3] Transparency page lists eight Coefficient grants (largest $8,500,000 in April 2025; about $25M cumulative), a $600,000 Tallinn DAF gift, $195,000 from SFF, and paying clients including OpenAI, Google DeepMind, xAI, an Anthropic pilot, the EU AI Office, Sequoia Capital Global Equities and Bridgewater. Quote: "xAI 2025 Model Evaluations Anthropic 2024 Small pilot for new benchmark" Sources: Transparency (https://epoch.ai/about/transparency)
- [for, floors at 2, F.3] Epoch says it charges lab and industry clients at least industry-consultant rates so it is not subsidising their work, and commits to disclosing sponsorship and data-access agreements; its eight Coefficient grants sum to $25.1M by its own list. Quote: "We aim to charge prices at least on par with industry consultants" Sources: Transparency (https://epoch.ai/about/transparency)

### Governance: 2/4 (Retrieved & confirmed: 2)
Anchor 2: For-profit or PBC with a published COI policy.
Derivation: Floored at 2 by epoch.06 (G.1): Nonprofit.. No admissible signal caps it.
- [for, floors at 2, G.1] Nonprofit. Quote: "Epoch AI, a nonprofit primarily funded by Open Philanthropy" Sources: AI benchmarking organization criticized for waiting to disclose funding from OpenAI (https://techcrunch.com/2025/01/19/ai-benchmarking-organization-criticized-for-waiting-to-disclose-funding-from-openai)

### Personnel: 2/4 (Retrieved & confirmed: 2)
Anchor 2: Frequent two-way hiring; recusal on request.
Derivation: Floored at 2 by epoch.09 (P.6): No lab roles found.. No admissible signal caps it.
- [for, floors at 2, P.6] No lab roles found. Sources: AI benchmarking organization criticized for waiting to disclose funding from OpenAI (https://techcrunch.com/2025/01/19/ai-benchmarking-organization-criticized-for-waiting-to-disclose-funding-from-openai)

### Access depth (lab-granted): 1/4 (Retrieved & confirmed: 1)
Anchor 1: Pre-release API with safeguards on.
Derivation: Capped at 1 by epoch.07 (A.1): Cannot share the commissioned set with other labs without OpenAI's permission.. Floors up to 1 from epoch.18 do not exceed the cap.
- [against, caps at 1, A.1] Cannot share the commissioned set with other labs without OpenAI's permission. Quote: "we cannot share the questions and answers with other parties without written permission from OpenAI" Sources: Clarifying the creation and use of the FrontierMath benchmark (https://epoch.ai/latest/openai-and-frontiermath)
- [for, floors at 1, A.1] Epoch reports pre-release access to evaluate GPT-5.4 (March 2026) and Meta's Muse Spark on FrontierMath. Quote: "We had pre-release access to evaluate the model" Sources: GPT-5.4 set a new record on FrontierMath (https://epochai.substack.com/p/gpt-54-set-a-new-record-on-frontiermath); Epoch AI on X: pre-release access to Meta's Muse Spark (https://x.com/EpochAIResearch/status/2041947954202988757)

### Scope control: 3/4 (Retrieved & confirmed: 3)
Anchor 3: Evaluator sets scope and can add questions.
Derivation: Capped at 3 by epoch.17 (S.6): FrontierMath, the asset on which Epoch evaluates OpenAI and other labs, was commissioned and is owned by OpenAI, which holds the problems and solutions outside the 50-problem holdout.. Floors up to 3 from epoch.08 do not exceed the cap.
- [for, floors at 3, S.5] Evaluates any model on FrontierMath at its discretion. Quote: "Epoch AI is free to conduct and publish evaluations of any models using the FrontierMath problem set" Sources: Clarifying the creation and use of the FrontierMath benchmark (https://epoch.ai/latest/openai-and-frontiermath)
- [against, caps at 3, S.6] FrontierMath, the asset on which Epoch evaluates OpenAI and other labs, was commissioned and is owned by OpenAI, which holds the problems and solutions outside the 50-problem holdout. Quote: "OpenAI commissioned Epoch AI to produce 300 advanced math problems for AI evaluation" Sources: Clarifying the creation and use of the FrontierMath benchmark (https://epoch.ai/latest/openai-and-frontiermath)

### Publication rights: 2/4 (Retrieved & confirmed: 2)
Anchor 2: Publishes; lab reviews with broad redaction.
Derivation: Capped at 2 by epoch.02 (R.2): Contributors were not told the funder; disclosure came after the fact.. Floors up to 2 from epoch.03 do not exceed the cap.
- [against, caps at 2, R.2] Contributors were not told the funder; disclosure came after the fact. Quote: "Per our agreement, we needed OpenAI’s permission before publicly disclosing their involvement" Sources: AI benchmarking organization criticized for waiting to disclose funding from OpenAI (https://techcrunch.com/2025/01/19/ai-benchmarking-organization-criticized-for-waiting-to-disclose-funding-from-openai); Clarifying the creation and use of the FrontierMath benchmark (https://epoch.ai/latest/openai-and-frontiermath)
- [for, floors at 2, R.1] After the disclosure failure, created a 50-problem holdout OpenAI cannot see. Quote: "We are finalizing a 50-problem set for which OpenAI will only receive the problem statements and not the solutions" Sources: Clarifying the creation and use of the FrontierMath benchmark (https://epoch.ai/latest/openai-and-frontiermath)

### Method transparency: 3/4 (Retrieved & confirmed: 3)
Anchor 3: Tasks or code partly open.
Derivation: Floored at 3 by epoch.04 (M.1): Rigorous public data on compute, training runs and capability trends.. No admissible signal caps it.
- [for, floors at 3, M.1] Rigorous public data on compute, training runs and capability trends. Sources: AI benchmarking organization criticized for waiting to disclose funding from OpenAI (https://techcrunch.com/2025/01/19/ai-benchmarking-organization-criticized-for-waiting-to-disclose-funding-from-openai)
- [for, informational, M.2] Publishes a transparency page listing donations above $70K and paying clients. Quote: "Here, we list only donations of $70,000 USD or more" Sources: Transparency (https://epoch.ai/about/transparency)

### Role incompatibility: 2/4 (Retrieved & confirmed: 2)
Anchor 2: Consults for labs.
Derivation: Conflict: floor 3 from epoch.10 (X.7) against cap 2 from epoch.16 (X.3); resolved at 2 by X.3: epoch.10's raw floor of 4 is held to 3 by C15/C16 and still exceeds the X.3 cap of 2; X.3 decides because the client list is on Epoch's own page.
Resolution: X.3 decides 2: epoch.10's raw floor of 4 is held to 3 by C15/C16 and still exceeds the X.3 cap of 2; X.3 decides because the client list is on Epoch's own page.
- [for, floors at 4, X.7] No commercial products. Sources: AI benchmarking organization criticized for waiting to disclose funding from OpenAI (https://techcrunch.com/2025/01/19/ai-benchmarking-organization-criticized-for-waiting-to-disclose-funding-from-openai)
- [against, caps at 3, X.5] Epoch states it invests part of its funds in semiconductor and AI stocks as part of a diversified portfolio. Quote: "We invest part of our funds in semiconductor and AI stocks as part of a diversified portfolio" Sources: Transparency (https://epoch.ai/about/transparency)
- [against, caps at 2, X.3] Epoch's transparency page lists paid consultation and evaluation work for OpenAI (2024 to 2026), Google DeepMind (2024 to 2026), xAI (2025) and an Anthropic pilot (2024). Quote: "OpenAI 2026 FrontierMath Data Audit" Sources: Transparency (https://epoch.ai/about/transparency)
- Document request: Which AI stocks Epoch holds and whether they include developers it evaluates.

## Dissent on the card

- Lower: Funding should be 1. OpenAI commissioned and owns FrontierMath, the asset Epoch's reputation rests on, and held approval over disclosing that fact for a year. OpenAI, Google DeepMind, xAI and Anthropic are all paying clients, the revenue split is undisclosed, and Epoch invests in AI stocks. 'Every major lab' as clients with an undisclosed share reads as F.5's material lab revenue, not F.3's occasional fee.
- Higher: Funding should be 3. Coefficient's $25.1M over eight grants dwarfs client fees, and Epoch discloses every donation above $70,000 and every client by name and year. It charges at least consultant rates so labs do not get subsidised work, keeps a 50-problem holdout OpenAI cannot see, and publishes evaluations of every lab's models on the same benchmark, including results OpenAI did not commission.

## Ledger rows naming the organization

- T07: grant from coefficient to epoch, 2021-2025, 24513611: cumulative [confirmed] https://epoch.ai/about/transparency
- T34: contract from openai to epoch, 2024, undisclosed: OpenAI commissioned FrontierMath problems and owns them; paid consultation client per transparency page [confirmed] https://epoch.ai/latest/openai-and-frontiermath
- T35: contract from google to epoch, 2025-2026, undisclosed: Google DeepMind listed as a paying consultation client [confirmed] https://epoch.ai/about/transparency
- T36: daf_grant from tallinn to epoch, 2025-01, 600000: via DAF per Epoch transparency page [confirmed] https://epoch.ai/our-funding
- T74: grant from coefficient to epoch, 2025-04, 8500000: largest single Epoch grant per transparency page [unaudited] https://epoch.ai/about/transparency
- T77: recommendation from sff to epoch, 2026-05, 195000: per Epoch transparency page [unaudited] https://epoch.ai/about/transparency
- T82: contract from xai to epoch, 2025, undisclosed: model evaluations for xAI, paying client per transparency page [unaudited] https://epoch.ai/about/transparency
- T83: contract from anthropic to epoch, 2024, undisclosed: pilot engagement per transparency page [unaudited] https://epoch.ai/about/transparency

## What would move the score

A standing rule against confidential lab funding of any evaluation asset.

Replies are filed as signals with the date received. Evaluator Bench: https://github.com/yoheinakajima/evaluator-bench
