# Right of reply: US CAISI (NIST)

Prepared 2026-09-15. Reply requested within 14 days of sending. This is the complete record Evaluator Bench holds about US CAISI (NIST); nothing else feeds the score. Values are derived from the signals' bounds under RULES.md; the default site view uses the standard evidence policy (confirmed sources only).

## How to reply

- Correct a fact: open a pull request adding a signal with a source, or reply with the rows and sources and we file them as a signal marked `source_type: self`.
- Dispute an anchor: say which anchor text you believe applies and which rule in RULES.md decides it; the resolution field records the disagreement even if the value does not change.
- Publish terms: contract terms on scope, access, and publication rights move the relevant dimensions on their own.
- Silence is recorded as silence, not as agreement.

## Current assessments

### Funding: 3/4 (standard policy: 3)
Anchor 3: Mostly philanthropic or public money; some lab-linked pooled funds.
Derivation: Capped at 3 by caisi.10 (F.9): Public appropriation of about $10M in FY2026; free pre-deployment access from labs is in-kind. No confirmed primary-filing negative on lab money is on file.. Floors up to 3 from caisi.01 do not exceed the cap.
Curator note: Anchor 3 pending a confirmed bounded negative (appropriations text); access from labs is in-kind.
- [for, floors at 3, F.9] Public funding; formal access agreements with five developers. Quote: "CAISI, which operates within NIST at the Department of Commerce" Sources: CAISI Frontier Testing Agreements Reach Five Labs (https://labs.cloudsecurityalliance.org/research/csa-research-note-caisi-frontier-ai-testing-agreements-20260/); Center for AI Standards and Innovation (https://www.nist.gov/caisi)
- [against, caps at 3, F.9] Public appropriation of about $10M in FY2026; free pre-deployment access from labs is in-kind. No confirmed primary-filing negative on lab money is on file. Quote: "As of FY2026, CAISI has approximately $15 million in funding: $10 million from FY2026 appropriations" Sources: Funding for CAISI (https://ifp.org/funding-for-caisi/); Center for AI Standards and Innovation (https://www.nist.gov/caisi)
- Document request: Add a confirmed bounded negative from a primary source to restore anchor 4.

### Governance: 3/4 (standard policy: 3)
Anchor 3: Nonprofit or public body with a COI policy.
Derivation: Capped at 3 by caisi.09 (G.5): Appropriation of about $10M in FY2026 within NIST's AI line; the director resigned in July 2026 and the NIST director is acting head.; capped at 3 by caisi.11 (G.5): The CAISI director resigned on 20 July 2026, three months after appointment — the third leadership change in six months.. Floors up to 3 from caisi.15 do not exceed the cap. Not counted under this policy: caisi.03 (no confirmed source (unaudited)).
- [against, caps at 3, G.5] Refocused in 2025 from broad safety research to demonstrable national-security risks; mandate is politically steerable. Quote: "repositioned the center as CAISI, shifting emphasis toward national security and cybersecurity risk reduction" Sources: CAISI Frontier Testing Agreements Reach Five Labs (https://labs.cloudsecurityalliance.org/research/csa-research-note-caisi-frontier-ai-testing-agreements-20260/)
- [against, caps at 3, G.5] Appropriation of about $10M in FY2026 within NIST's AI line; the director resigned in July 2026 and the NIST director is acting head. Quote: "$10 million from FY2026 appropriations" Sources: Funding for CAISI (https://ifp.org/funding-for-caisi/); evaluators.csv (24 evaluators: Coefficient and SFF totals, lab money, government contracts, leadership) (https://github.com/kevinnbass/metr-money-figure/blob/master/research/evaluators.csv)
- [against, caps at 3, G.5] The CAISI director resigned on 20 July 2026, three months after appointment — the third leadership change in six months. Quote: "resigned from his role as director just three months after he was picked for the job" Sources: What Will It Cost for the US to Be Ready for the Next Big AI Breakthrough? (https://ifp.org/funding-for-caisi/); Trump's head of AI safety agency CAISI resigns after months on job (https://www.cnbc.com/2026/07/20/trumps-head-of-ai-safety-agency-caisi-resigns-after-months-on-job.html)
- [for, floors at 3, G.2] CAISI is a NIST center whose staff are bound by the federal conflict-of-interest statute, 18 U.S.C. 208. Quote: "18 U.S. Code § 208 - Acts affecting a personal financial interest" Sources: 18 U.S. Code § 208 - Acts affecting a personal financial interest (https://www.law.cornell.edu/uscode/text/18/208); Center for AI Standards and Innovation (https://www.nist.gov/caisi)

### Personnel: 3/4 (standard policy: 3)
Anchor 3: Recusal policy and disclosure of lab ties.
Derivation: Floored at 3 by caisi.14 (P.5): CAISI staff are NIST federal employees bound by the criminal conflict-of-interest statute (18 U.S.C. 208) and the post-employment statute (18 U.S.C. 207), which restricts former employees for one to two years after leaving.. No admissible signal caps it.
- [against, informational, section 9] Authorized Scale AI, a company 49% owned by Meta, to run evaluations on its behalf. Quote: "Scale AI SEAL : Safety, Evaluation, and Alignment Lab; first third-party evaluator authorized by US AISI" Sources: Why the U.S. Needs an Independent AI Evaluation Framework for National Security (https://scale.com/blog/ai-evaluation-framework-national-security); Third-Party Model Auditing (https://www.longtermwiki.com/wiki/E450); Scale AI not winding down following Meta deal, interim CEO says (https://www.cnbc.com/2025/06/18/scale-ai-not-winding-down-following-meta-deal-interim-ceo-says.html)
- [for, floors at 3, P.5] CAISI staff are NIST federal employees bound by the criminal conflict-of-interest statute (18 U.S.C. 208) and the post-employment statute (18 U.S.C. 207), which restricts former employees for one to two years after leaving. Quote: "within 1 year after the termination of his or her service or employment as such officer or employee" Sources: 18 U.S. Code § 208 - Acts affecting a personal financial interest (https://www.law.cornell.edu/uscode/text/18/208); 18 U.S. Code § 207 - Restrictions on former officers, employees, and elected officials (https://www.law.cornell.edu/uscode/text/18/207); Center for AI Standards and Innovation (https://www.nist.gov/caisi)

### Access depth (lab-granted): 3/4 (standard policy: 3)
Anchor 3: Helpful-only or weights-level access, chain of thought, logs, on-site.
Derivation: Floored at 3 by caisi.12 (A.4): Five labs now give CAISI pre-deployment access (OpenAI and Anthropic since September 2025; Google DeepMind, Microsoft and xAI from 5 May 2026), including versions with guardrails stripped back; more than 40 evaluations completed, one of a foreign model without developer cooperation.. No admissible signal caps it. Not counted under this policy: caisi.02 (no confirmed source (unaudited)).
- [for, floors at 3, A.4] More than 40 evaluations including unreleased models; classified CBRN and cyber work via the TRAINS taskforce. Quote: "completed more than 40 evaluations — including assessments of frontier models not yet available to the public" Sources: CAISI Frontier Testing Agreements Reach Five Labs (https://labs.cloudsecurityalliance.org/research/csa-research-note-caisi-frontier-ai-testing-agreements-20260/)
- [for, floors at 3, A.4] Five labs now give CAISI pre-deployment access (OpenAI and Anthropic since September 2025; Google DeepMind, Microsoft and xAI from 5 May 2026), including versions with guardrails stripped back; more than 40 evaluations completed, one of a foreign model without developer cooperation. Quote: "provide CAISI with model access that includes versions with safety guardrails stripped back" Sources: CAISI Frontier Testing Agreements Reach Five Labs (https://labs.cloudsecurityalliance.org/research/csa-research-note-caisi-frontier-ai-testing-agreements-20260/)

### Scope control: 3/4 (standard policy: 3)
Anchor 3: Evaluator sets scope and can add questions.
Derivation: Capped at 3 by caisi.13 (S.4): Participation is voluntary and agreements were jointly scoped with the two founding labs; the center can only assess models developers choose to share.. Floors up to 3 from caisi.06 do not exceed the cap.
- [for, floors at 3, S.4] Government defines risk domains. Quote: "The government defines the risk domains it wants evaluated" Sources: Why the U.S. Needs an Independent AI Evaluation Framework for National Security (https://scale.com/blog/ai-evaluation-framework-national-security)
- [against, caps at 3, S.4] Participation is voluntary and agreements were jointly scoped with the two founding labs; the center can only assess models developers choose to share. Quote: "CAISI’s authority to conduct these evaluations rests entirely on voluntary participation" Sources: CAISI Frontier Testing Agreements Reach Five Labs (https://labs.cloudsecurityalliance.org/research/csa-research-note-caisi-frontier-ai-testing-agreements-20260/)

### Publication rights: 2/4 (standard policy: unevidenced)
Anchor 2: Publishes; lab reviews with broad redaction.
Derivation: Unevidenced under this policy: no admissible signal sets a bound. Not counted: caisi.04 (no confirmed source (unaudited)).
- [against, caps at 2, R.4] Publishes little per model; findings mostly stay inside government. Quote: "voluntary agreements, unclassified evaluations, no mandatory disclosure of findings" Sources: CAISI Frontier Testing Agreements Reach Five Labs (https://labs.cloudsecurityalliance.org/research/csa-research-note-caisi-frontier-ai-testing-agreements-20260/)

### Method transparency: 2/4 (standard policy: 2)
Anchor 2: Methods described in prose.
Derivation: Capped at 2 by caisi.07 (M.2): Methods partly published through NIST; per-evaluation methods not public..
- [against, caps at 2, M.2] Methods partly published through NIST; per-evaluation methods not public. Quote: "CAISI published a write-up on how AI models can cheat on agentic evaluations" Sources: Center for AI Standards and Innovation (https://www.nist.gov/caisi)

### Role incompatibility: 3/4 (standard policy: 3)
Anchor 3: Tools are open or free to the ecosystem.
Derivation: Conflict: floor 4 from caisi.08 (X.7) against cap 3 from caisi.16 (X.6); resolved at 3 by X.6: The specific co-production rule (X.6) decides over the general legal-form floor: 3.
Resolution: X.6 decides 3: The specific co-production rule (X.6) decides over the general legal-form floor: 3.
- [for, floors at 4, X.7] No commercial products. Quote: "lead unclassified evaluations of AI capabilities that may pose risks to national security" Sources: Center for AI Standards and Innovation (https://www.nist.gov/caisi); CAISI Frontier Testing Agreements Reach Five Labs (https://labs.cloudsecurityalliance.org/research/csa-research-note-caisi-frontier-ai-testing-agreements-20260/)
- [against, caps at 3, X.6] CAISI partnered with Scale AI in February 2025 to jointly develop evaluation methods for frontier models, and authorized Scale SEAL as a third-party evaluator; Meta has held 49% of Scale AI since June 2025. Quote: "Scale partnered with the U.S. Center for AI Standards and Innovation (CAISI), jointly developing new evaluation methods" Sources: Why the U.S. Needs an Independent AI Evaluation Framework for National Security (https://scale.com/blog/ai-evaluation-framework-national-security); Scale AI not winding down following Meta deal, interim CEO says (https://www.cnbc.com/2025/06/18/scale-ai-not-winding-down-following-meta-deal-interim-ceo-says.html); Third-Party Model Auditing (https://www.longtermwiki.com/wiki/E450)

## Dissent on the card

- Lower: Publication (R) at 2 could be 1. For the five partner labs, no per-model evaluation has been published; the public write-ups concern a foreign model tested without cooperation and two vulnerability disclosures the labs had already fixed. CSA records "no mandatory disclosure of findings". Under R.4, a public body that publishes nothing per model for the labs it has agreements with scores 1, and the DeepSeek report is the exception rather than the practice.
- Higher: Publication (R) at 2 could be 3. CAISI has published a full per-model evaluation (DeepSeek V4 Pro), named vulnerabilities in ChatGPT Agent and Anthropic's Constitutional Classifiers, and states that it publishes findings from its assessments. No lab-edited summary or lab redaction is documented. That is closer to anchor 3 (publishes, redaction limited to security) than to the anchor-2 picture of broad lab redaction.

## Ledger rows naming the organization

- T47: grant from us-gov to caisi, FY2026, 10000000: appropriation within the NIST AI line [confirmed] https://ifp.org/funding-for-caisi/
- T79: grant from us-gov to caisi, FY2026, 15000000: about $15M available: $10M appropriated plus a Technology Modernization Fund loan [unaudited] https://ifp.org/funding-for-caisi/
- N09: negative: no grant from Coefficient Giving in its index [Coefficient grants index, 2,911 rows, 2026-09-11] [imported] https://coefficientgiving.org/grants/
- N18: negative: no CAISI contract to METR, Apollo, or other private evaluators found [CAISI announcements and spending search, 2026-09-14] [imported] https://www.nist.gov/caisi

## What would move the score

Regular public reporting per model and a standing budget line insulated from reorganization.

Replies are filed as signals with the date received. Evaluator Bench: https://github.com/yoheinakajima/evaluator-bench
