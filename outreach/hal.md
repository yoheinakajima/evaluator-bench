# Right of reply: Holistic Agent Leaderboard (Princeton)

Prepared 2026-09-15. Reply requested within 14 days of sending. This is the complete record Evaluator Bench holds about Holistic Agent Leaderboard (Princeton); nothing else feeds the score. Values are derived from the signals' bounds under RULES.md; the default site view uses the standard evidence policy (confirmed sources only).

## How to reply

- Correct a fact: open a pull request adding a signal with a source, or reply with the rows and sources and we file them as a signal marked `source_type: self`.
- Dispute an anchor: say which anchor text you believe applies and which rule in RULES.md decides it; the resolution field records the disagreement even if the value does not change.
- Publish terms: contract terms on scope, access, and publication rights move the relevant dimensions on their own.
- Silence is recorded as silence, not as agreement.

## Current assessments

### Funding: 3/4 (standard policy: 3)
Anchor 3: Mostly philanthropic or public money; some lab-linked pooled funds.
Derivation: Capped at 3 by hal.09 (F.11): University-hosted leaderboard; no lab money found, and no bounded negative on file (no filing or index searched yet).; capped at 3 by hal.10 (F.6): HAL is funded by Coefficient Giving, whose principal is an Anthropic investor, and receives API credits from OpenAI and Google to evaluate their models.. Floors up to 3 from hal.01 do not exceed the cap.
Curator note: Anchor 3 pending a bounded negative (university sponsorship disclosures or a funder index search).
- [for, floors at 4, F.11] No lab money; academic. Sources: Holistic Agent Leaderboard (https://hal.cs.princeton.edu/)
- [against, caps at 3, F.11] University-hosted leaderboard; no lab money found, and no bounded negative on file (no filing or index searched yet). Quote: "HAL is funded by Coefficient Giving , Schmidt Sciences , the Princeton AI Lab" Sources: Holistic Agent Leaderboard (https://hal.cs.princeton.edu/)
- [against, caps at 3, F.6] HAL is funded by Coefficient Giving, whose principal is an Anthropic investor, and receives API credits from OpenAI and Google to evaluate their models. Quote: "We are grateful to OpenAI and Google for providing API credits to evaluate their models" Sources: Holistic Agent Leaderboard (https://hal.cs.princeton.edu/); Anthropic raises $124 million Series A (https://www.anthropic.com/news/anthropic-raises-124-million-to-build-more-reliable-general-ai-systems)
- Document request: Request to the HAL team: the amount or approximate value of the OpenAI and Google API credits received and whether any evaluation depends on them, plus a funder list with amounts so a bounded negative on lab money can be recorded.

### Governance: 2/4 (standard policy: 2)
Anchor 2: For-profit or PBC with a published COI policy.
Derivation: Floored at 2 by hal.05 (G.1): University-hosted; AEF member.. No admissible signal caps it.
Curator note: Anchor 3: university-hosted academic project and AEF member (hal.05). No tier-1 source for an independent board or external review, so 4 is unearned under the tier rule (C10).
- [for, floors at 2, G.1] University-hosted; AEF member. Quote: "By the SAgE team at Princeton University" Sources: Holistic Agent Leaderboard (https://hal.cs.princeton.edu/); AI Evaluator Forum launch and AEF-1 (https://aievaluatorforum.org/)

### Personnel: 2/4 (standard policy: 2)
Anchor 2: Frequent two-way hiring; recusal on request.
Derivation: Capped at 2 by hal.11 (P.4): HAL's author list includes a co-author affiliated with xAI, and its acknowledgments name staff at Anthropic, Google DeepMind and UK AISI; no contributor recusal or cooling-off rule is published.. Floors up to 2 from hal.06 do not exceed the cap.
Curator note: Anchor 3 (provisional): academic staff (hal.06); no lab-tie disclosures or cooling-off periods are documented at any tier, so 4 is unearned under the tier rule (C10). Provisional readings are open to public correction through the contribution path.
- [for, floors at 2, P.6] Academic staff. Quote: "Sayash Kapoor Princeton University Benedikt Stroebl Princeton University" Sources: Holistic Agent Leaderboard (https://hal.cs.princeton.edu/)
- [against, caps at 2, P.4] HAL's author list includes a co-author affiliated with xAI, and its acknowledgments name staff at Anthropic, Google DeepMind and UK AISI; no contributor recusal or cooling-off rule is published. Quote: "Yifei Zhou xAI" Sources: Holistic Agent Leaderboard (https://hal.cs.princeton.edu/)
- Document request: Request to the HAL team at Princeton: the contributor conflict-of-interest or recusal rule that applies to the leaderboard, if any, and the date on which the xAI-affiliated co-author's affiliation began relative to the runs they contributed.

### Access depth (lab-granted): 0/4 (standard policy: 0)
Anchor 0: Public API only.
Derivation: Capped at 0 by hal.04 (A.6): Public API access only..
- [against, caps at 0, A.6] Public API access only. Quote: "We are grateful to OpenAI and Google for providing API credits to evaluate their models" Sources: Holistic Agent Leaderboard (https://hal.cs.princeton.edu/)

### Scope control: 3/4 (standard policy: 3)
Anchor 3: Evaluator sets scope and can add questions.
Derivation: Floored at 3 by hal.07 (S.5): Own benchmark design.. No admissible signal caps it.
- [for, floors at 3, S.5] Own benchmark design. Quote: "We have paused updating HAL leaderboard with new models and are currently focusing on measuring reliability in AI agents" Sources: Holistic Agent Leaderboard (https://hal.cs.princeton.edu/)

### Publication rights: 3/4 (standard policy: 3)
Anchor 3: Publishes; redaction limited to security; redactions disclosed.
Derivation: Floored at 3 by hal.03 (R.5): Results published without review.. No admissible signal caps it.
- [for, floors at 3, R.5] Results published without review. Quote: "The standardized, cost-aware, and third-party leaderboard for evaluating agents" Sources: Holistic Agent Leaderboard (https://hal.cs.princeton.edu/)

### Method transparency: 3/4 (standard policy: 3)
Anchor 3: Tasks or code partly open.
Derivation: Floored at 3 by hal.02 (M.1): Open code and logs.. No admissible signal caps it.
- [for, floors at 3, M.1] Open code and logs. Quote: "HAL is an open-source project and we welcome contributions from the community" Sources: Holistic Agent Leaderboard (https://hal.cs.princeton.edu/)

### Role incompatibility: 3/4 (standard policy: 3)
Anchor 3: Tools are open or free to the ecosystem.
Derivation: Floored at 3 by hal.08 (X.7): No products.. No admissible signal caps it. Held: C16: a 4 needs a tier-1/2 source or two independent sources, one not self-published.
- [for, floors at 4, X.7] No products. Quote: "HAL is an open-source project" Sources: Holistic Agent Leaderboard (https://hal.cs.princeton.edu/)

## Dissent on the card

- Lower: Access is already 0 and cannot go lower, so the weakest movable dimension is Personnel, which should be 1. A co-author is listed at xAI, staff of Anthropic, Google DeepMind and UK AISI are acknowledged on the page, OpenAI and Google supply the API credits, and no recusal or contributor conflict rule exists; lab-affiliated authors on a leaderboard that grades their employers is anchor 1's informal arrangement.
- Higher: Personnel should be 3. Every co-author's affiliation is disclosed on the page, the project sits inside Princeton, whose faculty are bound by a university conflict-of-interest policy, no HAL leader holds a lab role, and the leaderboard's scoring is open code anyone can re-run. Disclosed ties under an institutional policy is anchor 3, not anchor 2.

## Ledger rows naming the organization


## What would move the score

Nothing on independence; access is the gap.

Replies are filed as signals with the date received. Evaluator Bench: https://github.com/yoheinakajima/evaluator-bench
