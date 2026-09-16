# Right of reply: Microsoft AI Red Team

Prepared 2026-09-15. Reply requested within 14 days of sending. This is the complete record Evaluator Bench holds about Microsoft AI Red Team; nothing else feeds the score. Values are derived from the signals' bounds under RULES.md; the default site view uses the Retrieved & confirmed evidence policy.

## How to reply

- Correct a fact: open a pull request adding a signal with a source, or reply with the rows and sources and we file them as a signal marked `source_type: self`.
- Dispute an anchor: say which anchor text you believe applies and which rule in RULES.md decides it; the resolution field records the disagreement even if the value does not change.
- Publish terms: contract terms on scope, access, and publication rights move the relevant dimensions on their own.
- Hand this to your agent: forward this packet as-is — the agent section below links the machine-readable record and the filing recipe, so nothing else needs uploading or pasting.
- Silence is recorded as silence, not as agreement.

## For your agent

If an AI agent is handling this reply, forward this packet as-is — no separate upload or pasted link needed. Start here:
- Machine orientation: https://evaluatorbench.com/llms.txt
- This organization's full machine-readable record: https://evaluatorbench.com/evaluators/msft.json
- Filing recipe (repo AGENTS.md, Recipe A): add the source you fetched yourself, then a signal with the exact quote (under 120 characters, copied verbatim), the anchor bound it sets (a cap or a floor), and the RULES.md rule code (e.g. F.3). Open a pull request; CI re-fetches every cited source and checks each quoted span appears verbatim.
- Or file the right-of-reply issue, no PR needed: https://github.com/yoheinakajima/evaluator-bench/issues/new?template=right-of-reply.md
- Rules of evidence: public sources only, quote-minimal spans, no motive or intent claims about any person (RULES 12).

## Current assessments

### Funding: 1/4 (Retrieved & confirmed: unevidenced)
Anchor 1: Material revenue or investment from evaluated labs or their investors.
Derivation: Unevidenced under this policy: no admissible signal sets a bound. Not counted: msft.01 (no confirmed source (unaudited)).
Curator note: Anchor 0 on funding given the cited signals. Evidence-limited: the cited sources are imported or unaudited only, so the value is held at 1 (the reading on the record would be 0) until a live source is confirmed.
- [against, caps at 0, F.1] Microsoft is a major OpenAI investor and a frontier developer with its own CAISI agreement. Quote: "Google (DeepMind), Microsoft, and xAI signed agreements with the US Center for AI Standards and Innovation (CAISI)" Sources: CAISI Frontier Testing Agreements Reach Five Labs (https://labs.cloudsecurityalliance.org/research/csa-research-note-caisi-frontier-ai-testing-agreements-20260/)

### Governance: 0/4 (Retrieved & confirmed: 0)
Anchor 0: Unit or subsidiary of a lab or a lab's investor.
Derivation: Capped at 0 by msft.02 (G.6): Business unit of a frontier developer.; capped at 0 by msft.09 (G.6): Microsoft's AI red team has operated since 2018 as an internal function and reports having red-teamed more than 100 generative AI products; it is separate from product teams, not from the developer..
Curator note: Anchor 0 on governance given the cited signals.
- [against, caps at 0, G.6] Business unit of a frontier developer. Quote: "guidance and best practices from the industry leading Microsoft AI Red Team" Sources: Microsoft AI Red Team (Microsoft Learn) (https://learn.microsoft.com/en-us/security/ai-red-team/)
- [against, caps at 0, G.6] Microsoft's AI red team has operated since 2018 as an internal function and reports having red-teamed more than 100 generative AI products; it is separate from product teams, not from the developer. Quote: "The AI red team was formed in 2018 to address the growing landscape of AI safety and security risks" Sources: Microsoft AI Red Team (Microsoft Learn) (https://learn.microsoft.com/en-us/security/ai-red-team/); 3 takeaways from red teaming 100 generative AI products (https://www.microsoft.com/en-us/security/blog/2025/01/13/3-takeaways-from-red-teaming-100-generative-ai-products/)

### Personnel: 0/4 (Retrieved & confirmed: 0)
Anchor 0: Leaders hold governance roles at an evaluated lab, no recusal.
Derivation: Capped at 0 by msft.06 (P.7): Employees of a lab..
- [against, caps at 0, P.7] Employees of a lab. Quote: "guidance and best practices from the industry leading Microsoft AI Red Team" Sources: Microsoft AI Red Team (Microsoft Learn) (https://learn.microsoft.com/en-us/security/ai-red-team/)

### Access depth (lab-granted): 3/4 (Retrieved & confirmed: 3)
Anchor 3: Helpful-only or weights-level access, chain of thought, logs, on-site.
Derivation: Floored at 3 by msft.05 (A.5): Deep access when engaged.. No admissible signal caps it. Held: C16: a 4 needs a tier-1/2 source or two independent sources, one not self-published.
- [for, floors at 4, A.5] Deep access when engaged. Quote: "red teaming has become a key part of Microsoft’s approach to generative AI product development" Sources: Microsoft AI Red Team (Microsoft Learn) (https://learn.microsoft.com/en-us/security/ai-red-team/); 3 takeaways from red teaming 100 generative AI products (https://www.microsoft.com/en-us/security/blog/2025/01/13/3-takeaways-from-red-teaming-100-generative-ai-products/)

### Scope control: 2/4 (Retrieved & confirmed: 2)
Anchor 2: Scope negotiated per engagement.
Derivation: Capped at 2 by msft.07 (S.2): Scope set by engagement..
- [against, caps at 2, S.2] Scope set by engagement. Sources: Microsoft AI Red Team (Microsoft Learn) (https://learn.microsoft.com/en-us/security/ai-red-team/)

### Publication rights: 2/4 (Retrieved & confirmed: 2)
Anchor 2: Publishes; lab reviews with broad redaction.
Derivation: Capped at 2 by msft.03 (R.3): Findings for other labs are rarely published under the team's own name..
- [against, caps at 2, R.3] Findings for other labs are rarely published under the team's own name. Quote: "Microsoft’s AI red team is excited to share our whitepaper" Sources: Microsoft AI Red Team (Microsoft Learn) (https://learn.microsoft.com/en-us/security/ai-red-team/); 3 takeaways from red teaming 100 generative AI products (https://www.microsoft.com/en-us/security/blog/2025/01/13/3-takeaways-from-red-teaming-100-generative-ai-products/)

### Method transparency: 3/4 (Retrieved & confirmed: 3)
Anchor 3: Tasks or code partly open.
Derivation: Floored at 3 by msft.04 (M.1): Publishes methodology (PyRIT) openly.. No admissible signal caps it.
- [for, floors at 3, M.1] Publishes methodology (PyRIT) openly. Quote: "Microsoft's Open Automation Framework to Red Team Generative AI Systems (PyRIT)" Sources: Microsoft AI Red Team (Microsoft Learn) (https://learn.microsoft.com/en-us/security/ai-red-team/)

### Role incompatibility: 1/4 (Retrieved & confirmed: 1)
Anchor 1: Sells products or services other than the evaluation itself to labs or to their customers.
Derivation: Capped at 1 by msft.08 (X.2): Sells AI products..
- [against, caps at 1, X.2] Sells AI products. Quote: "What is Azure AI Content Safety?" Sources: Microsoft AI Red Team (Microsoft Learn) (https://learn.microsoft.com/en-us/security/ai-red-team/)

## Dissent on the card

- Lower: Governance (1 to 0). The Microsoft AI Red Team is an internal function formed in 2018 inside a frontier developer, described on Microsoft's own Learn hub and Security Blog; G.6 and F.1 place a business unit of a developer at 0. Only the unaudited status of two pages that load and say exactly this holds the value at 1; both are the organization's own admissions.
- Higher: Publication rights (1 to 2). The team publishes under its own name: a whitepaper on lessons from red teaming more than 100 generative AI products, case studies, and the open-source PyRIT toolkit. R.3's second clause caps an organization that publishes its own reports on other work at 2, not 1, even where findings on other labs' models stay inside system cards.

## Ledger rows naming the organization

- T64: transfer from microsoft to msft, , undisclosed: business unit of Microsoft, corporate budget [confirmed] https://www.microsoft.com/en-us/security/blog/topic/ai-red-team/

## What would move the score

Not a candidate for an independence-critical role; useful as a supplementary red team.

Replies are filed as signals with the date received. Evaluator Bench: https://github.com/yoheinakajima/evaluator-bench
