# Right of reply: METR

Prepared 2026-09-15. Send date: [to be filled by the sender]. Reply requested within 14 days of sending. This is the complete record Evaluator Bench holds about METR; nothing else feeds the score.

## How to reply

- Correct a fact: open a pull request adding a signal with a source, or email the rows and sources and we file them as a signal marked `source_type: self`.
- Dispute an anchor: say which anchor text you believe applies and why; the rationale field records the disagreement even if the value does not change.
- Publish terms: contract terms on scope, access, and publication rights move the relevant dimensions on their own.
- Silence is recorded as silence, not as agreement.

## Current assessments

### Funding: 3/4
Anchor 3: Mostly philanthropic or public money; some lab-linked pooled funds.
Rationale: Anchor 3: mostly philanthropic, no direct lab cash, but pooled and donor-advised funds with non-public donors, recommendations funded by a lab investor, in-kind credits from a lab, and a donor rule that is under two years old and still moving. Anchor 4 requires a confirmed bounded negative in primary filings and a resolved funder-exposure computation; both are on file as imported rows only.
- [for] Hard rule against accepting money from AI companies, including donations directed by their staff; ~$71M raised in 2026 from foundations and individuals. Sources: About METR (https://metr.org/about); METR raises $71M to independently stress-test AI (https://alphasignal.ai/news/metr-raises-71m-to-independently-stress-test-the-world-s-most-powerful-ai); Funding update (https://metr.org/blog/2026-08-14-funding-update/)
- [for] Funder base widened beyond the effective-altruism network, including Pew Charitable Trusts. Sources: Who Funds the AI Safety Watchdogs (https://itbb.substack.com/p/who-funds-the-watchdogs)
- [against] Runs on large volumes of free tokens and privileged access from the labs it evaluates. Sources: About METR (https://metr.org/about)
- [against] The no-lab-money rule is recent and its wording has moved: absent from the April 2024 page, a compensation footnote in April 2025, 'has not accepted funding from AI companies' with free-credit language from August 2025, and a September 2025 footnote that donations from individual lab employees are accepted. An OpenAI technical lead is named among individual donors. Sources: METR donor rule wording over time (Wayback captures of metr.org/about and /donate) (https://web.archive.org/web/2025*/metr.org/about)
- [against] Traced inflows in the ledger: no direct grant from Coefficient Giving in its index, but the 2024 spin-out transfer from ARC (seeded by Coefficient and SFF), SFF recommendations funded by an Anthropic Series A investor, a Longview pooled-fund grant, and about $21M through donor-advised funds and the Audacious Project whose underlying donors are not public. Sources: Coefficient Giving grants index (https://coefficientgiving.org/grants/); METR FY2024 Form 990 (EIN 99-1219864) (https://projects.propublica.org/nonprofits/organizations/991219864); metr-money-figure research ledger and audits (https://github.com/kevinnbass/metr-money-figure)
- [for] Bounded negatives on file: no METR-named grant in Coefficient's 2,911-row index (snapshot 2026-09-11) or in the Good Ventures, Schmidt Sciences, Pew, and Packard filings checked; all imported and awaiting re-derivation. Sources: Coefficient Giving grants index (https://coefficientgiving.org/grants/); metr-money-figure research ledger and audits (https://github.com/kevinnbass/metr-money-figure)
- [for] Current page (re-fetched 14 Sep 2026) states METR cannot accept donations made by or at the direction of frontier AI company employees, tighter than the September 2025 footnote; the SFF 2025 recommendation of $548,000 is confirmed on the fund's page and FY2024 revenue of $13.6M on ProPublica. Quote: "METR has not accepted funding from AI companies" Sources: About METR (https://metr.org/about); SFF-2025 S-Process Recommendations Announcement (https://survivalandflourishing.fund/2025/recommendations); Nonprofit Explorer summaries: METR (EIN 99-1219864) and ARC (EIN 86-3605182) (https://projects.propublica.org/nonprofits/organizations/991219864); Docket: Does METR accept money from the frontier AI companies whose models it evaluates? (https://github.com/yoheinakajima/evaluator-bench/blob/main/dockets/metr-lab-money/proposal.json)
- Open question: Re-derive the five negative-evidence rows from the cited filings and index (audit_status imported to confirmed).
- Open question: Identify the donors behind the $4.0M Vanguard Charitable grant and the Audacious commitment.
- Open question: Confirm the donor-rule capture history against the Wayback Machine directly.
- Open question: The live page names David Farhi among donors while stating it cannot accept donations from frontier AI company employees; the timing of the gift relative to his OpenAI role and to the rule is not established.

### Governance: 4/4
Anchor 4: Nonprofit or public body, published COI policy, independent board, external review.
Rationale: Anchor 4 on governance given the cited signals.
- [for] Nonprofit with a written independence policy and a no-lab-money rule. Sources: About METR (https://metr.org/about)

### Personnel: 2/4
Anchor 2: Frequent two-way hiring; recusal on request.
Rationale: Anchor 2: two-way movement between METR and labs, and board or advisor seats one to two steps from labs; no published recusal or cooling-off policy found. Sources are imported and need re-derivation from metr.org/team captures and the FY2024 990.
- [against] Hires from the labs it evaluates; a former Anthropic researcher joined in September 2026. Sources: Anthropic CEO pitches AI slow-down plan (https://www.washingtonexaminer.com/policy/technology/4724950/anthropic-ceo-pitch-ai-slow-down-plan/)
- [against] Board and advisors carry lab ties one or two steps out: a director who founded FAR.AI, which is paid by OpenAI for red-teaming; an advisor who is an a16z partner, the firm that led Thinking Machines' seed; an ex-OpenAI advisor who advises Thinking Machines; a director who leads an insurance-certification startup seeded by an Anthropic co-founder. Former advisors moved to Anthropic and to the OpenAI Foundation board. Sources: Team (https://metr.org/team/); METR FY2024 Form 990 (EIN 99-1219864) (https://projects.propublica.org/nonprofits/organizations/991219864); metr-money-figure research ledger and audits (https://github.com/kevinnbass/metr-money-figure)
- Open question: Fetch dated captures of metr.org/team to confirm current versus former roles.
- Open question: Ask METR whether a recusal or cooling-off policy exists.

### Access depth: 4/4
Anchor 4: Embedded, training-time, or incident access.
Rationale: Anchor 4 on access given the cited signals.
- [for] Investigated the OpenAI incident on site over six days with a Redwood contractor. Sources: Brief independent investigation of agents' behavior in the OpenAI / Hugging Face hacking incident (https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/); OpenAI Agents Formed Secret Swarm, Hacked Hugging Face (https://www.techtimes.com/articles/325705/20260827/openai-agents-formed-secret-swarm-hacked-hugging-face-then-forged-their-own-logs.htm)
- [for] Named by Anthropic as the example embedded evaluator with employee-level access. Sources: Altman Says OpenAI Will Match Anthropic's Embedded Evaluator Pledge (https://www.unite.ai/altman-says-openai-will-match-anthropics-embedded-evaluator-pledge/); Anthropic's 3-Step 'Pace the Frontier' Plan (https://www.marktechpost.com/2026/09/13/anthropics-3-step-pace-the-frontier-plan-wins-openai-xai-and-microsoft-support-is-it-too-late-to-slow-ai-down/)
- [against] Access remains voluntary; no law requires any lab to grant it. Sources: Who Funds the AI Safety Watchdogs (https://itbb.substack.com/p/who-funds-the-watchdogs)

### Scope control: 3/4
Anchor 3: Evaluator sets scope and can add questions.
Rationale: Anchor 3 on scope given the cited signals.
- [against] OpenAI set the investigation window (June 26 to July 13); the lab's own cluster breach and three of METR's standard incident questions were out of scope. Sources: What METR's OpenAI Agent Investigation Left Out (https://blog.pebblous.ai/blog/openai-agent-incident-investigation-scope/en/); Brief independent investigation of agents' behavior in the OpenAI / Hugging Face hacking incident (https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/)

### Publication rights: 3/4
Anchor 3: Publishes; redaction limited to security; redactions disclosed.
Rationale: Anchor 3 on publication given the cited signals.
- [for] Published its own 91-page report with a redaction summary statement; took no payment for the investigation. Sources: Brief independent investigation of agents' behavior in the OpenAI / Hugging Face hacking incident (https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/); Anthropic's 3-Step 'Pace the Frontier' Plan (https://www.marktechpost.com/2026/09/13/anthropics-3-step-pace-the-frontier-plan-wins-openai-xai-and-microsoft-support-is-it-too-late-to-slow-ai-down/)
- [against] OpenAI could redact any non-public information and gave feedback on structure, emphasis, clarity and tone, which METR incorporated. Sources: Brief independent investigation of agents' behavior in the OpenAI / Hugging Face hacking incident (https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/)

### Method transparency: 4/4
Anchor 4: Open code, tasks, reproducible runs, factsheets.
Rationale: Anchor 4 on methods given the cited signals.
- [for] Open task suites and published time-horizon methodology; results appear in system cards. Sources: About METR (https://metr.org/about)

### Product conflicts: 4/4
Anchor 4: No commercial products.
Rationale: Anchor 4 on products given the cited signals.
- [for] No commercial products. Sources: About METR (https://metr.org/about)

## Ledger rows naming the organization

- T11: recommendation from sff to metr, 2024, 204000: SFF 2024 recommendation incl. match [imported] https://survivalandflourishing.fund/sff-2024-recommendations
- T12: recommendation from sff to metr, 2025, 548000: $120K plus $428K matching pledge [confirmed] https://survivalandflourishing.fund/
- T13: transfer from arc to metr, 2024-04-30, 4553935: spin-out grant/asset transfer, ARC FY2024 990 Schedule I [imported] https://projects.propublica.org/nonprofits/organizations/863605182
- T14: daf_grant from vanguard-charitable to metr, FY2025, 4000000: 990 Schedule I; underlying donor not public [imported] https://projects.propublica.org/nonprofits/organizations/232888152
- T15: daf_grant from founders-pledge to metr, 2024, 184000: 990 Schedule I; matches Tallinn's public ledger [imported] https://projects.propublica.org/nonprofits/
- T16: daf_grant from svcf to metr, 2024, 20000: 990 Schedule I; matches Tallinn's ledger [imported] https://projects.propublica.org/nonprofits/
- T17: commitment from audacious to metr, 2024-10-09, 17000000: METR share of the $38M Canary commitment (RAND + METR) [imported] https://metr.org/blog/2024-10-09-new-support-through-the-audacious-project/
- T18: grant from longview to metr, 2023, 220000: public fund grant per Giving What We Can page [imported] https://www.givingwhatwecan.org/charities/arc-evals
- T19: in_kind from openai to metr, 2026-07, 400000: API credits for the Hugging Face incident investigation, METR estimate [confirmed] https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/
- R10: gleave board at metr: advisor and board member; FY2024 990 lists as director; imported kevinnbass/metr-money-figure:B05; confirmed on metr.org/about 2026-09-14: 'Advisor and Board Member' [confirmed] https://metr.org/team/
- R13: mascorro advisor at metr: imported kevinnbass/metr-money-figure:B08; confirmed on metr.org/about: 'Advisor' [confirmed] https://metr.org/team/
- R16: radford advisor at metr: ex-OpenAI; advises Thinking Machines; imported kevinnbass/metr-money-figure:B07; confirmed on metr.org/about: 'Advisor' [confirmed] https://metr.org/team/
- R17: karnofsky advisor at metr: former unpaid advisor, listed through Dec 2024; imported kevinnbass/metr-money-figure:B12; not on the live team page 2026-09-14, consistent with former status; Wayback capture still needed [imported] https://metr.org/team/
- R19: christiano board at metr: former; imported kevinnbass/metr-money-figure:B11; not on the live team page 2026-09-14, consistent with former status; Wayback capture still needed [imported] https://metr.org/team/
- R21: dattani board at metr: imported kevinnbass/metr-money-figure:B06; confirmed on metr.org/about: 'Advisor and Board Member' [confirmed] https://metr.org/team/
- R30: farhi donor at metr: named among individual donors on metr.org/about (Dec 2025 capture); OpenAI technical lead; imported kevinnbass/metr-money-figure:DR12,DR13; confirmed on metr.org/about: named among 'many others' donors; OpenAI employment still imported (DR13) [confirmed] https://metr.org/about
- R32: constellation office_host at metr: imported kevinnbass/metr-money-figure:M126 [imported] https://metr.org/about
- R33: arc parent at metr:  [confirmed] https://metr.org/about
- N01: negative: no grant from Coefficient Giving to METR under any name [Coefficient grants index, 2,911 rows, 2026-09-11] [imported] https://coefficientgiving.org/grants/
- N02: negative: no METR-named grant in Good Ventures Foundation 990-PF Part XV [990-PF FY2022 to FY2025, 2026-09-14] [imported] https://projects.propublica.org/nonprofits/organizations/461008520
- N03: negative: no METR-named grant in Schmidt Sciences 990-PF 2021 to 2024 [990-PF Part XV, 2026-09-14] [imported] https://projects.propublica.org/nonprofits/
- N04: negative: no METR-named grant in Pew Charitable Trusts 990 Schedule I FY2021 to FY2025 [990 Schedule I, 2026-09-14] [imported] https://projects.propublica.org/nonprofits/
- N05: negative: no METR-named grant in Packard Foundation 990-PF 2021 to 2024 [990-PF Part XV, 2026-09-14] [imported] https://projects.propublica.org/nonprofits/

## What would move the score

Contract terms for the Anthropic embedded program that fix scope-setting and publication rights in writing, plus a public cooling-off policy.

Replies are filed as signals with the date received. Evaluator Bench: https://github.com/yoheinakajima/evaluator-bench
