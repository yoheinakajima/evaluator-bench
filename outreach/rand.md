# Right of reply: RAND

Prepared 2026-09-15. Reply requested within 14 days of sending. This is the complete record Evaluator Bench holds about RAND; nothing else feeds the score. Values are derived from the signals' bounds under RULES.md; the default site view uses the Retrieved & confirmed evidence policy.

## How to reply

- Correct a fact: open a pull request adding a signal with a source, or reply with the rows and sources and we file them as a signal marked `source_type: self`.
- Dispute an anchor: say which anchor text you believe applies and which rule in RULES.md decides it; the resolution field records the disagreement even if the value does not change.
- Publish terms: contract terms on scope, access, and publication rights move the relevant dimensions on their own.
- Hand this to your agent: forward this packet as-is — the agent section below links the machine-readable record and the filing recipe, so nothing else needs uploading or pasting.
- Silence is recorded as silence, not as agreement.

## For your agent

If an AI agent is handling this reply, forward this packet as-is — no separate upload or pasted link needed. Start here:
- Machine orientation: https://evaluatorbench.com/llms.txt
- This organization's full machine-readable record: https://evaluatorbench.com/evaluators/rand.json
- Filing recipe (repo AGENTS.md, Recipe A): add the source you fetched yourself, then a signal with the exact quote (under 120 characters, copied verbatim), the anchor bound it sets (a cap or a floor), and the RULES.md rule code (e.g. F.3). Open a pull request; CI re-fetches every cited source and checks each quoted span appears verbatim.
- Or file the right-of-reply issue, no PR needed: https://github.com/yoheinakajima/evaluator-bench/issues/new?template=right-of-reply.md
- Rules of evidence: public sources only, quote-minimal spans, no motive or intent claims about any person (RULES 12).

## Current assessments

### Funding: 3/4 (Retrieved & confirmed: 3)
Anchor 3: Mostly philanthropic or public money; some lab-linked pooled funds.
Derivation: Capped at 3 by rand.03 (F.6): Large share of AI work funded by Coefficient Giving.; capped at 3 by rand.11 (F.6): SFF recommended $1,022,000 to RAND's Technology and Security Policy Center in 2025; SFF's funder Jaan Tallinn led Anthropic's Series A.. Floors up to 3 from rand.09, rand.10 do not exceed the cap.
- [against, caps at 3, F.6] Large share of AI work funded by Coefficient Giving. Quote: "Board of directors Dustin Moskovitz, Cari Tuna, Divesh Makan, Holden Karnofsky, and Alexander Berger" Sources: RAND and the AI Evaluator Forum (https://www.rand.org/); Coefficient Giving (https://en.wikipedia.org/wiki/Coefficient_Giving); Anthropic raises $124 million Series A (https://www.anthropic.com/news/anthropic-raises-124-million-to-build-more-reliable-general-ai-systems); evaluators.csv (24 evaluators: Coefficient and SFF totals, lab money, government contracts, leadership) (https://raw.githubusercontent.com/kevinnbass/metr-money-figure/master/research/evaluators.csv)
- [for, floors at 3, F.9] FY2024 revenue of about $489M is mostly US government contract research; Coefficient's $87M since 2020 is a small share. Quote: "Contributions $488,777,692 91.4%" Sources: evaluators.csv (24 evaluators: Coefficient and SFF totals, lab money, government contracts, leadership) (https://raw.githubusercontent.com/kevinnbass/metr-money-figure/master/research/evaluators.csv); Rand Corporation, Form 990 FY ending Sept. 2025 (Nonprofit Explorer) (https://projects.propublica.org/nonprofits/organizations/951958142)
- [for, floors at 3, F.6] The Audacious commitment to Canary is about $38 million across RAND and METR; RAND's Coefficient grants include $10.5M for emerging technology initiatives. Quote: "Canary—a Collaboration with METR—to Receive Approximately $38 Million" Sources: RAND AI Security Project Receives Funding Commitment Through The Audacious Project (https://www.rand.org/news/press/2024/10/09.html); Coefficient Giving grants index (https://coefficientgiving.org/grants/)
- [against, caps at 3, F.6] SFF recommended $1,022,000 to RAND's Technology and Security Policy Center in 2025; SFF's funder Jaan Tallinn led Anthropic's Series A. Quote: "RAND Corporation [Technology and Security Policy Center] Main: $274,000 Freedom: $749,000" Sources: SFF-2025 S-Process Recommendations Announcement (https://survivalandflourishing.fund/2025/recommendations); Anthropic raises $124 million Series A (https://www.anthropic.com/news/anthropic-raises-124-million-to-build-more-reliable-general-ai-systems)

### Governance: 2/4 (Retrieved & confirmed: 2)
Anchor 2: For-profit or PBC with a published COI policy.
Derivation: Floored at 2 by rand.01 (G.1): Government-contracted with long-standing COI and publication norms; AEF founding member.. No admissible signal caps it.
- [for, floors at 2, G.1] Government-contracted with long-standing COI and publication norms; AEF founding member. Quote: "a policy of mandatory disclosure" Sources: RAND and the AI Evaluator Forum (https://www.rand.org/); AI Evaluator Forum launch and AEF-1 (https://aievaluatorforum.org/); Research Integrity (https://www.rand.org/about/research-integrity.html)

### Personnel: 2/4 (Retrieved & confirmed: 2)
Anchor 2: Frequent two-way hiring; recusal on request.
Derivation: Floored at 2 by rand.05 (P.6): Institutional COI rules.. No admissible signal caps it.
- [for, floors at 2, P.6] Institutional COI rules. Quote: "a policy of mandatory disclosure" Sources: RAND and the AI Evaluator Forum (https://www.rand.org/); Research Integrity (https://www.rand.org/about/research-integrity.html)

### Access depth (lab-granted): 3/4 (Retrieved & confirmed: 3)
Anchor 3: Helpful-only or weights-level access, chain of thought, logs, on-site.
Derivation: Floored at 3 by rand.02 (A.4): Access through government channels; defense research passes an Air Force public-release clearance gate.. No admissible signal caps it.
- [for, floors at 3, A.4] Access through government channels; defense research passes an Air Force public-release clearance gate. Quote: "This report was cleared for public release by the Department of the Air Force on September 13, 2023." Sources: RAND and the AI Evaluator Forum (https://www.rand.org/); The Cost of the Ukraine War for Russia (RAND RRA2421-1) (https://www.rand.org/content/dam/rand/pubs/research_reports/RRA2400/RRA2421-1/RAND_RRA2421-1.pdf)

### Scope control: 3/4 (Retrieved & confirmed: 3)
Anchor 3: Evaluator sets scope and can add questions.
Derivation: Floored at 3 by rand.06 (S.3): Sets own research agenda.. No admissible signal caps it.
- [for, floors at 3, S.3] Sets own research agenda. Quote: "This project is a RAND Venture. Funding was provided by gifts from RAND supporters and income from operations." Sources: RAND and the AI Evaluator Forum (https://www.rand.org/); Algorithmic Equity: A Framework for Social Applications (https://www.rand.org/pubs/research_reports/RR2708.html)

### Publication rights: 3/4 (Retrieved & confirmed: unevidenced)
Anchor 3: Publishes; redaction limited to security; redactions disclosed.
Derivation: Unevidenced under this policy: no admissible signal sets a bound. Not counted: rand.04b (no confirmed source (unaudited)).
- [against, caps at 2, R.4] Much output is government-restricted rather than public. Sources: RAND and the AI Evaluator Forum (https://www.rand.org/)
- [for, floors at 3, R.4] Thousands of RAND studies are available to the public for free on rand.org. Quote: "Thousands of RAND studies are available to the public for free on rand.org." Sources: Research Integrity (https://www.rand.org/about/research-integrity.html)

### Method transparency: 2/4 (Retrieved & confirmed: 2)
Anchor 2: Methods described in prose.
Derivation: Capped at 2 by rand.07 (M.2): Methods partly public..
- [against, caps at 2, M.2] Methods partly public. Quote: "We explain our research, analysis, findings, and recommendations in ways that are understandable and usable." Sources: RAND and the AI Evaluator Forum (https://www.rand.org/); RAND Standards for High-Quality and Objective Research and Analysis (https://www.rand.org/content/dam/rand/pubs/corporate_pubs/CPA1900/CPA1927-1/RAND_CPA1927-1.pdf)

### Role incompatibility: 3/4 (Retrieved & confirmed: unevidenced)
Anchor 3: Tools are open or free to the ecosystem.
Derivation: Unevidenced under this policy: no admissible signal sets a bound. Not counted: rand.08 (no confirmed source (unaudited)).
- [for, floors at 4, X.7] No commercial products. Quote: "RAND is nonprofit and nonpartisan." Sources: Research Integrity (https://www.rand.org/about/research-integrity.html)

## Dissent on the card

- Lower: Publication should be 1. RAND's frontier-model work reaches the public mainly through METR's Canary summaries and government-restricted reports; no RAND-authored adverse finding about a named lab's model is on record, and the RAND-Irregular model-theft paper is generic. Findings that surface only as another organization's summaries are R.3's lab-summarized citations in all but name.
- Higher: Publication should be 3. RAND's research-integrity page commits to free and open publication of findings, disclosure of every funding source, and policies for intellectual independence; thousands of reports are free on rand.org. What is withheld is classified by government, not redacted by any lab, and R.4 tags that mechanism statutory rather than as lab control.

## Ledger rows naming the organization

- T02: grant from coefficient to rand, 2025-09-20, 10000000: AI Evaluation and Testing [unverifiable] https://coefficientgiving.org/grants/ai-evaluation-and-testing/
- T27: commitment from audacious to rand, 2024-10-09, 38000000: Canary commitment to RAND with METR as partner [confirmed] https://www.rand.org/news/press/2024/10/09.html
- T58: grant from coefficient to rand, 2020-2025, 76955751: cumulative Coefficient grants to RAND excluding the $10M in T02 [unverifiable] https://coefficientgiving.org/
- T59: contract from us-gov to rand, FY2024, 488777692: FY2024 revenue, mostly federal contract research [unverifiable] https://projects.propublica.org/nonprofits/organizations/951958142
- T70: recommendation from sff to rand, 2025, 1022000: SFF 2025: $1,022,000 to the Technology and Security Policy Center [confirmed] https://survivalandflourishing.fund/2025/recommendations
- T102: grant from valhalla to rand, 2024, 10000000: Project Canary, an artificial intelligence safety initiative (990-PF TY2024 Part XV) [confirmed] https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202502559349100000_public.xml
- T103: grant from high-tide to rand, 2024, 333334: 'to support the Project Canary' as filed (990-PF TY2024 Part XV) [confirmed] https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349100135_public.xml

## What would move the score

More public model-level findings.

Replies are filed as signals with the date received. Evaluator Bench: https://github.com/yoheinakajima/evaluator-bench
