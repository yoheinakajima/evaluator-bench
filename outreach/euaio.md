# Right of reply: EU AI Office

Prepared 2026-09-15. Reply requested within 14 days of sending. This is the complete record Evaluator Bench holds about EU AI Office; nothing else feeds the score. Values are derived from the signals' bounds under RULES.md; the default site view uses the Retrieved & confirmed evidence policy.

## How to reply

- Correct a fact: open a pull request adding a signal with a source, or reply with the rows and sources and we file them as a signal marked `source_type: self`.
- Dispute an anchor: say which anchor text you believe applies and which rule in RULES.md decides it; the resolution field records the disagreement even if the value does not change.
- Publish terms: contract terms on scope, access, and publication rights move the relevant dimensions on their own.
- Hand this to your agent: forward this packet as-is — the agent section below links the machine-readable record and the filing recipe, so nothing else needs uploading or pasting.
- Silence is recorded as silence, not as agreement.

## For your agent

If an AI agent is handling this reply, forward this packet as-is — no separate upload or pasted link needed. Start here:
- Machine orientation: https://evaluatorbench.com/llms.txt
- This organization's full machine-readable record: https://evaluatorbench.com/evaluators/euaio.json
- Filing recipe (repo AGENTS.md, Recipe A): add the source you fetched yourself, then a signal with the exact quote (under 120 characters, copied verbatim), the anchor bound it sets (a cap or a floor), and the RULES.md rule code (e.g. F.3). Open a pull request; CI re-fetches every cited source and checks each quoted span appears verbatim.
- Or file the right-of-reply issue, no PR needed: https://github.com/yoheinakajima/evaluator-bench/issues/new?template=right-of-reply.md
- Rules of evidence: public sources only, quote-minimal spans, no motive or intent claims about any person (RULES 12).

## Current assessments

### Funding: 3/4 (Retrieved & confirmed: 3)
Anchor 3: Mostly philanthropic or public money; some lab-linked pooled funds.
Derivation: Capped at 3 by euaio.10 (F.12): Public budget under the Digital Europe Programme; EUR 7.37M awarded across six lots to contracted evaluators. No confirmed negative on file.. Floors up to 3 from euaio.06, euaio.14 do not exceed the cap.
Curator note: Anchor 3 pending a confirmed bounded negative; funding is public by construction but the gate asks for the row.
- [for, floors at 3, F.9] Public funding. Quote: "established within the Commission as part of the administrative structure of the Directorate-General" Sources: Frontier AI safety regulations: A reference for lab staff (https://metr.org/notes/2026-01-29-frontier-ai-safety-regulations/); Commission Decision Establishing the European AI Office (https://digital-strategy.ec.europa.eu/en/library/commission-decision-establishing-european-ai-office)
- [against, caps at 3, F.12] Public budget under the Digital Europe Programme; EUR 7.37M awarded across six lots to contracted evaluators. No confirmed negative on file. Quote: "The €9,080,000 tender is divided into six lots" Sources: TED 864574-2025 Technical Assistance for AI Safety (https://ted.europa.eu/); The EU AI Act Newsletter #77: AI Office Tender (https://artificialintelligenceact.substack.com/p/the-eu-ai-act-newsletter-77-ai-office)
- [for, floors at 3, F.9] Commission Decision C(2024) 390 Article 8 funds the AI Office from DG CONNECT staff, Digital Europe Programme administrative appropriations, and DEP Specific Objective 2 'Artificial Intelligence' for operational expenditure, naming no non-Union source. Quote: "Operational expenditure of the Office shall be covered by the financial resources allocated to Specific Objective 2" Sources: Commission Decision of 24 January 2024 establishing the European Artificial Intelligence Office, C/2024/1459 (Official Journal PDF) (https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A32024D01459); Commission Decision Establishing the European AI Office (https://digital-strategy.ec.europa.eu/en/library/commission-decision-establishing-european-ai-office)
- Document request: Add a confirmed bounded negative from a primary source to restore anchor 4.

### Governance: 3/4 (Retrieved & confirmed: 3)
Anchor 3: Nonprofit or public body with a COI policy.
Derivation: Floored at 3 by euaio.12 (G.2): AI Office staff are Commission officials bound by the EU Staff Regulations, which require screening of actual or potential conflicts of interest (Article 11a) and restrict post-employment activity for two years (Article 16).. No admissible signal caps it.
Curator note: Anchor 3: public body with a statutory basis (euaio.07). No tier-1 source for an independent board or external review, so 4 is unearned under the tier rule (C10). Whether a formal COI policy is published is an open question.
- [for, floors at 2, G.1] Regulator with statutory basis. Quote: "established within the European Commission as the foundation for a single AI governance system" Sources: Frontier AI safety regulations: A reference for lab staff (https://metr.org/notes/2026-01-29-frontier-ai-safety-regulations/); European AI Office (https://digital-strategy.ec.europa.eu/en/policies/ai-office)
- [for, floors at 3, G.2] AI Office staff are Commission officials bound by the EU Staff Regulations, which require screening of actual or potential conflicts of interest (Article 11a) and restrict post-employment activity for two years (Article 16). Quote: "a concrete procedure for properly screening new staff for actual or potential conflicts of interest" Sources: New EU Staff Regulations adopted: Small steps on revolving door, giant leaps still needed (https://corporateeurope.org/en/revolving-doors/2013/07/new-eu-staff-regulations-adopted-small-steps-revolving-door-giant-leaps); Staff Regulations of Officials of the European Union (consolidated text) (https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:01962R0031-20240101)

### Personnel: 3/4 (Retrieved & confirmed: 3)
Anchor 3: Recusal policy and disclosure of lab ties.
Derivation: Floored at 3 by euaio.08 (P.5): Civil-service conflict rules.. No admissible signal caps it.
- [for, floors at 3, P.5] Civil-service conflict rules. Quote: "Article 16 of the old staff regulations included a two-year notification period after staff leave their EU job" Sources: Frontier AI safety regulations: A reference for lab staff (https://metr.org/notes/2026-01-29-frontier-ai-safety-regulations/); New EU Staff Regulations adopted: Small steps on revolving door, giant leaps still needed (https://corporateeurope.org/en/revolving-doors/2013/07/new-eu-staff-regulations-adopted-small-steps-revolving-door-giant-leaps); Staff Regulations of Officials of the European Union (consolidated text) (https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:01962R0031-20240101)

### Access depth (lab-granted): 3/4 (Retrieved & confirmed: 3)
Anchor 3: Helpful-only or weights-level access, chain of thought, logs, on-site.
Derivation: Floored at 3 by euaio.01 (A.2): Legal power to compel; the only body whose access does not depend on goodwill.. No admissible signal caps it.
- [for, floors at 3, A.2] Legal power to compel; the only body whose access does not depend on goodwill. Quote: "may request access to the general-purpose AI model concerned through APIs or further appropriate technical means" Sources: Frontier AI safety regulations: A reference for lab staff (https://metr.org/notes/2026-01-29-frontier-ai-safety-regulations/); Article 92: Power to conduct evaluations (AI Act Service Desk) (https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-92)

### Scope control: 4/4 (Retrieved & confirmed: 4)
Anchor 4: Evaluator sets scope, can investigate incidents, can refuse sign-off.
Derivation: Floored at 4 by euaio.13 (S.4): The AI Office holds the legal power under the AI Act to evaluate general-purpose models with systemic risk and to compel access and information; scope for those evaluations is set by the regulator, not the developer.. No admissible signal caps it.
- [for, floors at 3, S.3] Contracts its own evaluators (FAR.AI-led consortium) rather than relying on lab-chosen ones. Quote: "FAR AI was selected by the European Commission's AI Office to lead CBRN risk research under tender EC-CNECT/2025/OP/0032" Sources: FAR AI (https://www.longtermwiki.com/wiki/E138)
- [for, floors at 3, S.4] Code sets the access floor: helpful-only versions where security allows, at least 20 business days, external evaluators for each new frontier model. Quote: "A developer should engage independent external evaluators for each new frontier model" Sources: Frontier AI safety regulations: A reference for lab staff (https://metr.org/notes/2026-01-29-frontier-ai-safety-regulations/); Expanding External Access to Frontier AI Models for Dangerous Capability Evaluations (arXiv 2601.11916) (https://arxiv.org/abs/2601.11916)
- [for, floors at 3, S.3] Contract notice TED 864574-2025, Technical Assistance for AI Safety, published 26 December 2025; contractors self-report include METR, FAR.AI, SecureBio, SaferAI and Epoch. Quote: "This tender has been split into six lots" Sources: TED notice 864574-2025: Artificial Intelligence Act: Technical Assistance for AI Safety (https://ted.europa.eu/en/notice/-/detail/864574-2025); TED 864574-2025 Technical Assistance for AI Safety (https://ted.europa.eu/); Forthcoming call for tenders: Artificial Intelligence Act - Technical Assistance for AI Safety (https://digital-strategy.ec.europa.eu/en/news/forthcoming-call-tenders-artificial-intelligence-act-technical-assistance-ai-safety); The EU AI Act Newsletter #77: AI Office Tender (https://artificialintelligenceact.substack.com/p/the-eu-ai-act-newsletter-77-ai-office)
- [for, floors at 4, S.4] The AI Office holds the legal power under the AI Act to evaluate general-purpose models with systemic risk and to compel access and information; scope for those evaluations is set by the regulator, not the developer. Quote: "may request access to the general-purpose AI model concerned through APIs or further appropriate technical means" Sources: Frontier AI safety regulations: A reference for lab staff (https://metr.org/notes/2026-01-29-frontier-ai-safety-regulations/); Article 92: Power to conduct evaluations (AI Act Service Desk) (https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-92)

### Publication rights: 2/4 (Retrieved & confirmed: 2)
Anchor 2: Publishes; lab reviews with broad redaction.
Derivation: Capped at 2 by euaio.04 (R.4): Safety and Security Model Reports are submitted to the Office, not the public..
- [against, caps at 2, R.4] Safety and Security Model Reports are submitted to the Office, not the public. Quote: "Signatories commit to reporting to the AI Office information about their model" Sources: Frontier AI safety regulations: A reference for lab staff (https://metr.org/notes/2026-01-29-frontier-ai-safety-regulations/); General-Purpose AI Code of Practice: Safety and Security chapter (mirror) (https://code-of-practice.ai/?section=safety-security)

### Method transparency: 2/4 (Retrieved & confirmed: 2)
Anchor 2: Methods described in prose.
Derivation: Capped at 2 by euaio.05 (M.2): No accreditation pathway or public reporting schema yet; thin evaluator bench..
- [against, caps at 2, M.2] No accreditation pathway or public reporting schema yet; thin evaluator bench. Quote: "the pool of qualified evaluators remains thin" Sources: The EU's Real AI Leverage Is Making Compliance the Path of Least Resistance (https://www.techpolicy.press/the-eus-real-ai-leverage-is-making-compliance-the-path-of-least-resistance/)

### Role incompatibility: 4/4 (Retrieved & confirmed: 4)
Anchor 4: No commercial products.
Derivation: Floored at 4 by euaio.09 (X.7): No commercial products.. No admissible signal caps it.
- [for, floors at 4, X.7] No commercial products. Quote: "It also enforces the rules for GPAI models and supports the governance bodies in Member States" Sources: Frontier AI safety regulations: A reference for lab staff (https://metr.org/notes/2026-01-29-frontier-ai-safety-regulations/); European AI Office (https://digital-strategy.ec.europa.eu/en/policies/ai-office); The EU AI Act Newsletter #77: AI Office Tender (https://artificialintelligenceact.substack.com/p/the-eu-ai-act-newsletter-77-ai-office)

## Dissent on the card

- Lower: Scope (S) at 2 could be 1. The public record shows the Office has run no evaluation of any frontier model; the only scope it has exercised is a procurement of technical assistance whose deliverables are shaped by the Code that signatory labs themselves negotiated. Until the Office uses Article 92, the labs effectively define what is tested through their own Safety and Security Model Reports, which is the anchor-1 picture.
- Higher: Scope (S) at 2 could be 3. Article 92 gives the Office the legal power to evaluate any general-purpose model and to compel access, including source code, with fines for refusal, and enforcement has been live since August 2026. The Office set the six risk lots of the tender itself. A body that writes the questions and can compel answers is at least anchor 3; section 9 holds it down only for lack of a published run.

## Ledger rows naming the organization

- T48: contract from eu-budget to euaio, 2025-12, 7373017: EU AI Office: total awarded across six lots of TED 864574-2025 to contracted evaluators (outflow from the Office, recorded on the Office row for visibility) [confirmed] https://ted.europa.eu/en/notice/-/detail/864574-2025
- N10: negative: no grant from Coefficient Giving in its index [Coefficient grants index, 2,911 rows, 2026-09-11] [imported] https://coefficientgiving.org/grants/
- N27: negative: Commission Decision C(2024) 390 Article 8 names only Union budget sources for the AI Office: DG CONNECT staff, Digital Europe Programme administrative appropriations for external staff, and DEP Specific Objective 2 for operational expenditure [Commission Decision of 24 January 2024 establishing the European AI Office, C/2024/1459, Article 8 (Official Journal PDF), 2026-09-15] [confirmed] https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A32024D01459

## What would move the score

An accreditation pathway for external evaluators and a public reporting schema.

Replies are filed as signals with the date received. Evaluator Bench: https://github.com/yoheinakajima/evaluator-bench
