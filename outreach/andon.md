# Right of reply: Andon Labs

Prepared 2026-09-15. Reply requested within 14 days of sending. This is the complete record Evaluator Bench holds about Andon Labs; nothing else feeds the score. Values are derived from the signals' bounds under RULES.md; the default site view uses the standard evidence policy (confirmed sources only).

## How to reply

- Correct a fact: open a pull request adding a signal with a source, or reply with the rows and sources and we file them as a signal marked `source_type: self`.
- Dispute an anchor: say which anchor text you believe applies and which rule in RULES.md decides it; the resolution field records the disagreement even if the value does not change.
- Publish terms: contract terms on scope, access, and publication rights move the relevant dimensions on their own.
- Silence is recorded as silence, not as agreement.

## Current assessments

### Funding: 2/4 (standard policy: 2)
Anchor 2: Labs pay per engagement; otherwise diversified.
Derivation: Capped at 2 by andon.03 (F.10): Commercial platform (Pion) and lab partnerships; funding and client mix not disclosed..
- [against, caps at 2, F.10] Commercial platform (Pion) and lab partnerships; funding and client mix not disclosed. Quote: "Introducing Pion: Run and grow real businesses autonomously" Sources: Andon Labs (https://andonlabs.com/); Andon Labs, agent safety evaluations (https://tooldirectory.ai/tools/andon-labs)
- [against, caps at 3, F.10] Funding is unclear: one database reports about $500K from seven investors after YC W24, another lists no rounds; no announcement found. Quote: "Andon Labs has raised $500K." Sources: Andon Labs profile (https://pitchbook.com/profiles/company/541549-09); Andon Labs: Autonomous organizations without humans in the loop (https://www.ycombinator.com/companies/andon-labs)

### Governance: 1/4 (standard policy: 1)
Anchor 1: Private for-profit with no published COI policy.
Derivation: Capped at 1 by andon.04 (G.1): No published COI policy found..
- [against, caps at 1, G.1] No published COI policy found. Quote: "Winter 2024 Active Machine Learning AI San Francisco" Sources: Andon Labs (https://andonlabs.com/); Andon Labs: Autonomous organizations without humans in the loop (https://www.ycombinator.com/companies/andon-labs)

### Personnel: 2/4 (standard policy: 2)
Anchor 2: Frequent two-way hiring; recusal on request.
Derivation: Capped at 2 by andon.07 (P.6): Undisclosed..
- [against, caps at 2, P.6] Undisclosed. Sources: Andon Labs (https://andonlabs.com/)

### Access depth (lab-granted): 1/4 (standard policy: 1)
Anchor 1: Pre-release API with safeguards on.
Derivation: Capped at 1 by andon.05 (A.1): Access through partnerships (Anthropic Project Vend); not routine pre-release..
- [against, caps at 1, A.1] Access through partnerships (Anthropic Project Vend); not routine pre-release. Quote: "Anthropic partnered with Andon Labs , an AI safety evaluation company" Sources: Andon Labs, agent safety evaluations (https://tooldirectory.ai/tools/andon-labs); Project Vend: Can Claude run a small shop? (And why does that matter?) (https://www.anthropic.com/research/project-vend-1)

### Scope control: 3/4 (standard policy: 3)
Anchor 3: Evaluator sets scope and can add questions.
Derivation: Floored at 3 by andon.06 (S.5): Designs its own long-horizon tasks.. No admissible signal caps it.
- [for, floors at 3, S.5] Designs its own long-horizon tasks. Quote: "The data comes from our deployment of real-world autonomous organizations" Sources: Andon Labs (https://andonlabs.com/)

### Publication rights: 2/4 (standard policy: 2)
Anchor 2: Publishes; lab reviews with broad redaction.
Derivation: Floored at 2 by andon.01 (R.7): Publishes candid results, including misalignment findings on the best-scoring models.. No admissible signal caps it.
- [for, floors at 2, R.7] Publishes candid results, including misalignment findings on the best-scoring models. Quote: "Opus 5 on Vending-Bench: Once Again the Best Capitalist, Once Again Misaligned" Sources: Andon Labs (https://andonlabs.com/); Publications (https://andonlabs.com/publications)

### Method transparency: 2/4 (standard policy: 2)
Anchor 2: Methods described in prose.
Derivation: Floored at 2 by andon.11 (M.2): Vending-Bench is described in a public paper (arXiv 2502.15840); the simulated environment is run by Andon as a service and its code is not published.. No admissible signal caps it.
- [for, informational, section 9] Benchmarks (Vending-Bench) cited in model cards across labs. Quote: "Vending-Bench results are cited in frontier-lab model cards and press" Sources: Andon Labs, agent safety evaluations (https://tooldirectory.ai/tools/andon-labs)
- [for, floors at 2, M.2] Vending-Bench is described in a public paper (arXiv 2502.15840); the simulated environment is run by Andon as a service and its code is not published. Quote: "In this paper, we present Vending-Bench, a simulated environment" Sources: Vending-Bench: A Benchmark for Long-Term Coherence of Autonomous Agents (arXiv 2502.15840) (https://arxiv.org/abs/2502.15840); Andon Labs (https://andonlabs.com/)

### Role incompatibility: 2/4 (standard policy: 2)
Anchor 2: Consults for labs.
Derivation: Capped at 2 by andon.08 (X.1): Sells a commercial agent platform..
- [against, caps at 2, X.1] Sells a commercial agent platform. Quote: "Agents that run any company fully autonomously" Sources: Andon Labs (https://andonlabs.com/); Pion | Andon Labs (https://andonlabs.com/pion)
- [against, caps at 1, X.2] Operates AI-run vending and retail deployments inside Anthropic and xAI offices as commercial partnerships while benchmarking those labs' models. Quote: "offering custom evaluations and deployments to AI labs and agent builders" Sources: Andon Labs, agent safety evaluations (https://tooldirectory.ai/tools/andon-labs); Andon Labs (https://andonlabs.com/); Project Vend: Can Claude run a small shop? (And why does that matter?) (https://www.anthropic.com/research/project-vend-1); Anthropic's office launched an AI-run vending machine. It evolved into AI-run stores and cafes within a year (https://fortune.com/2026/06/02/anthropic-office-vending-machine-ai-agents-vendo-andon-lukas-petersson/)

## Dissent on the card

- Lower: Role incompatibility (X) at 1 could be 0. Andon sells Pion, a platform for running businesses autonomously, and deploys agents inside Anthropic and xAI offices while grading those labs' models on Vending-Bench; its own site says "Safety from humans in the loop is a mirage" and pitches the deployments as the safety layer. If a lab buys that layer, it is a monitoring product sold to an evaluated lab, which is anchor 0.
- Higher: Role incompatibility (X) at 1 could be 2. No payment from any lab is documented: Anthropic describes Project Vend as a research partnership, the ledger records no fee, and Pion has no named customer. Absent a priced engagement, the record supports research collaboration with labs rather than services sold to them, which is closer to the anchor-2 consulting picture than to a vendor relationship.

## Ledger rows naming the organization

- T55: investment from yc to andon, 2024, 500000: YC W24; about $500K reported by one database, unfunded per another [unverifiable] https://pitchbook.com/profiles/company/541549-09
- T56: partnership from anthropic to andon, 2025, undisclosed: Project Vend partnership; AI-run vending deployed inside Anthropic offices [confirmed] https://tooldirectory.ai/tools/andon-labs
- R63: yc investor at andon:  [unverifiable] https://pitchbook.com/profiles/company/541549-09

## What would move the score

Funding disclosure and a COI policy would move this from low to medium confidence quickly.

Replies are filed as signals with the date received. Evaluator Bench: https://github.com/yoheinakajima/evaluator-bench
