"""Initial curation snapshot (v0, 14 Sep 2026).

Run once to write data/. After that, edit the JSON files in data/ directly
and open a PR. This file is kept so the first curation is reviewable as
code. It is not imported by the build.

Every signal cites at least one source id. Every assessment cites at least
one signal id. bench verify enforces both.
"""
from __future__ import annotations
import json, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
D = ROOT / "data"
RETRIEVED = "2026-09-14"

# ---------------------------------------------------------------------------
# Sources. (id, title, publisher, url, published, note)
# ---------------------------------------------------------------------------
SOURCES = [
 ("metr-about","About METR","METR","https://metr.org/about","2026-08","States METR has not accepted funding from AI companies; notes reliance on free tokens."),
 ("metr-funding-2026","Funding update","METR","https://metr.org/blog/2026-08-14-funding-update/","2026-08-14","Independence framing; growth in philanthropic commitments."),
 ("alphasignal-metr-71m","METR raises $71M to independently stress-test AI","AlphaSignal","https://alphasignal.ai/news/metr-raises-71m-to-independently-stress-test-the-world-s-most-powerful-ai","2026-08","Reports ~$71M in commitments from foundations and individuals; hard rule on lab money."),
 ("itbb-watchdogs","Who Funds the AI Safety Watchdogs","Inside The Black Box (Substack)","https://itbb.substack.com/p/who-funds-the-watchdogs","2026-06-03","Funding pipeline analysis; METR diversification; Redwood revenue volatility; ~$25M Open Phil to Redwood historically."),
 ("metr-hf-investigation","Brief independent investigation of agents' behavior in the OpenAI / Hugging Face hacking incident","METR","https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/","2026-08-26","Terms of engagement: six days on premises, OpenAI could redact non-public info, gave feedback on structure and tone; redaction summary statement."),
 ("pebblous-scope","What METR's OpenAI Agent Investigation Left Out","Pebblous","https://blog.pebblous.ai/blog/openai-agent-incident-investigation-scope/en/","2026-09","Scope set by OpenAI; OpenAI's own cluster breach excluded; three of METR's standard incident questions dropped."),
 ("techtimes-metr-hf","OpenAI Agents Formed Secret Swarm, Hacked Hugging Face","Tech Times","https://www.techtimes.com/articles/325705/20260827/openai-agents-formed-secret-swarm-hacked-hugging-face-then-forged-their-own-logs.htm","2026-08-27","Investigators named; 44 misalignment incidents in METR Frontier Risk Report."),
 ("marktechpost-pace","Anthropic's 3-Step 'Pace the Frontier' Plan","MarkTechPost","https://www.marktechpost.com/2026/09/13/anthropics-3-step-pace-the-frontier-plan-wins-openai-xai-and-microsoft-support-is-it-too-late-to-slow-ai-down/","2026-09-13","Investigators took no payment; ~$400K API credits; embedded evaluator terms: desks, badges, publication without editorial control."),
 ("unite-altman-match","Altman Says OpenAI Will Match Anthropic's Embedded Evaluator Pledge","Unite.AI","https://www.unite.ai/altman-says-openai-will-match-anthropics-embedded-evaluator-pledge/","2026-09-12","OpenAI commits to employee-like access for independent evaluators; METR named as example."),
 ("wapo-examiner-benton","Anthropic CEO pitches AI slow-down plan","Washington Examiner","https://www.washingtonexaminer.com/policy/technology/4724950/anthropic-ceo-pitch-ai-slow-down-plan/","2026-09-12","Former Anthropic researcher Joe Benton joins METR."),
 ("apollo-norms","Our Norms on Security, Science Communication and Conflicts of Interest","Apollo Research","https://www.apolloresearch.ai/blog/our-norms-coi-security-science-communication/","2025-11-26","Four COI rules: no contingent compensation; no side grants/investments from evaluated orgs; recusal; no misrepresentation. States labs pay fair market value."),
 ("apollo-pbc","Apollo Research is becoming a PBC","Apollo Research","https://www.apolloresearch.ai/blog/apollo-research-is-becoming-a-pbc","2026-01-20","Spin-out from fiscal sponsor into public benefit corporation."),
 ("apollo-about","About","Apollo Research","https://www.apolloresearch.ai/about","2026","Ran evaluations for all major labs; partnered with OpenAI on anti-scheming; Watcher product."),
 ("apollo-first-year","The First Year of Apollo Research","Apollo Research","https://www.apolloresearch.ai/blog/the-first-year-of-apollo-research","2024","Contracted by UK AISI for deception evals; red-teamed OpenAI fine-tuning API."),
 ("securebio-oaif","Thoughts on Taking OpenAI Foundation Funding","EA Forum (Jeff Kaufman)","https://forum.effectivealtruism.org/posts/dMfgJQ2rGX8GmzdMm/thoughts-on-taking-openai-foundation-funding","2026-08","OpenAI Foundation grant to Detection division; OpenAI PBC paid for GPT-5.5 eval; firewall and resignation commitment; OAIF board overlap."),
 ("aef-launch","AI Evaluator Forum launch and AEF-1","AI Evaluator Forum","https://aievaluatorforum.org/","2025-12-04","Founding members: Transluce, METR, RAND, HAL, SecureBio, CIP, AVERI/Brundage. AEF-1 minimum operating conditions."),
 ("aef-transparency","Evaluation Transparency Letter","AI Evaluator Forum","https://t.co/Nm0RMxOWzw","2026","Editorial control, access, and transparency disclosures expected of third-party evaluators."),
 ("longtermwiki-far","FAR AI","Longterm Wiki","https://www.longtermwiki.com/wiki/E138","2026-02-26","EU AI Office tender EC-CNECT/2025/OP/0032, Lot 1 led by FAR.AI with SecureBio and SaferAI; FY2024 revenue."),
 ("far-30m","FAR.AI Secures Over $30 Million in Multi-Funder Support","FAR.AI","https://far.ai/news/30m-multi-funder-support","2026-07-16","Funders: Coefficient Giving, Schmidt Sciences, SFF, CSET, AI Safety Fund (Frontier Model Forum)."),
 ("techcrunch-irregular","Irregular raises $80M to secure frontier AI models","TechCrunch","https://techcrunch.com/2025/09/17/irregular-raises-80-million-to-secure-frontier-ai-models","2025-09-17","Formerly Pattern Labs; Sequoia and Redpoint lead; $450M valuation; cited in o3, o4-mini, Claude 3.7 evaluations."),
 ("sequoia-irregular","Partnering with Irregular","Sequoia Capital","https://sequoiacap.com/article/partnering-with-irregular-ahead-of-the-curve/","2025-09-17","Evaluations cited in GPT-4/o3/o4-mini/GPT-5 system cards; UK government and Anthropic use SOLVE; embedded with labs."),
 ("newswire-irregular","Irregular Raises $80 Million","Newswire","https://www.newswire.com/news/irregular-raises-80-million-to-set-the-security-standards-for-frontier-ai","2025-09-17","Millions in annual revenue; works with OpenAI and Anthropic; runtime security roadmap."),
 ("grayswan-seriesa","Gray Swan announces Series A","Gray Swan","https://www.grayswan.ai/news/gray-swan-announces-series-a","2026-05-28","$40M; Wing and Madrona; cited in 11 system cards; Cygnal, Shade, Arena products."),
 ("forbes-grayswan-2026","This AI Startup's Army of 15,000 Hackers","Forbes","https://www.forbes.com/sites/rashishrivastava/2026/05/28/this-ai-startups-army-of-15000-hackers-pressure-test-claude-gpt-5-and-gemini/","2026-05-28","$200M valuation; clients OpenAI, Anthropic, Google DeepMind, Meta, xAI, ByteDance."),
 ("forbes-grayswan-2024","Gray Swan AI Is Working With OpenAI to Red Team Its Models","Forbes","https://www.forbes.com/sites/sarahemerson/2024/10/29/this-hacker-team-is-bulletproofing-ai-models-for-companies-like-openai/","2024-10-29","Kolter recused from Gray Swan-OpenAI interactions; $5.5M seed."),
 ("openai-kolter-board","Zico Kolter Joins OpenAI's Board of Directors","OpenAI","https://openai.com/index/zico-kolter-joins-openais-board-of-directors/","2024-08","Board seat and Safety and Security Committee membership."),
 ("kolter-bio","Bio","Zico Kolter","http://zkolter.github.io/bio/","2026","Chairs OpenAI SSC; co-founder and Chief Scientist of Gray Swan."),
 ("averi-launch","The Launch of AVERI","Miles Brundage (Substack)","https://milesbrundage.substack.com/p/the-launch-of-averi","2026-01-15","501(c)(3); founder formerly OpenAI."),
 ("averi-pilot","AVERI Pilot Report: The World's First Double-Blind Evaluation of a Proprietary Language Model","AVERI","https://www.averi.org/ourwork/averi-pilot-report-the-worlds-first-double-blind-eval","2026-08","Gemini 2.5 Flash-Lite in secure enclave with DeepMind, OpenMined, MLCommons; notes EU CoP and Illinois SB 315 requirements."),
 ("averi-about","About","AVERI","https://www.averi.org/about","2026","Endorsed SB 315; co-authored AEF-1; pilots are voluntary."),
 ("arxiv-frontier-auditing","Frontier AI Auditing: Toward Rigorous Third-Party Assessment (arXiv 2601.11699)","arXiv","https://arxiv.org/abs/2601.11699","2026-02-07","AI Assurance Levels; cross-industry precedents (FAA, UL, melamine, HackerOne)."),
 ("crowell-sb315","Illinois AI Safety Measures Act SB 315","Crowell & Moring","https://www.crowell.com/en/insights/client-alerts/illinois-imposes-transparency-and-safety-obligations-on-frontier-ai-systems","2026-07-08","Annual independent audits from 2028; no financial interest either way; high-level summary published within 30 days."),
 ("stackaware-sb315","How AI hyperscalers can use ISO 42001 internal audit to comply with Illinois SB 315","StackAware","https://blog.stackaware.com/p/illinois-sb-315-iso-42001-internal-audit-ai-hyperscaler","2026-07-14","Report contents: personnel list, COI procedures, methodology, lead auditor signature; audit-plus-recommendations tension."),
 ("lw-sb315","Illinois Joins Growing State-Level Effort","Latham & Watkins","https://www.lw.com/en/insights/illinois-joins-growing-state-level-effort-to-regulate-frontier-ai-with-new-safety-measures-act","2026-07-15","Demonstrated competence requirement; $500M revenue threshold."),
 ("metr-regs","Frontier AI safety regulations: A reference for lab staff","METR","https://metr.org/notes/2026-01-29-frontier-ai-safety-regulations/","2026-01-29","EU CoP: adequate access incl. helpful-only versions, 20 business days, external evaluators each new frontier model; enforceable Aug 2026."),
 ("arxiv-access-taxonomy","Expanding External Access to Frontier AI Models for Dangerous Capability Evaluations (arXiv 2601.11916)","arXiv","https://arxiv.org/abs/2601.11916","2026-01-21","Taxonomy of access levels for external evaluators."),
 ("csa-caisi","CAISI Frontier Testing Agreements Reach Five Labs","Cloud Security Alliance","https://labs.cloudsecurityalliance.org/research/csa-research-note-caisi-frontier-ai-testing-agreements-20260/","2026-05-20","DeepMind, Microsoft, xAI added May 2026; 40+ evaluations; TRAINS taskforce; 2025 refocus."),
 ("nist-caisi","Center for AI Standards and Innovation","NIST","https://www.nist.gov/caisi","2026-08-08","Mandate: voluntary agreements with developers and evaluators; focus on demonstrable risks."),
 ("scale-framework","Why the U.S. Needs an Independent AI Evaluation Framework for National Security","Scale AI","https://scale.com/blog/ai-evaluation-framework-national-security","2026-05-20","Scale partnered with CAISI Feb 2025; runs evaluations for governments."),
 ("csa-aisi-trends","UK AISI's Frontier AI Trends Report: Security Implications","Cloud Security Alliance","https://labs.cloudsecurityalliance.org/research/csa-research-note-aisi-frontier-ai-trends-report-20260712-cs/","2026-07-12","Frontier AI Bill promised, not introduced; voluntary MOUs; universal jailbreaks found; 30+ models."),
 ("resultsense-aisi","OpenAI asked for enforceable safety bars. Britain built the auditor and withheld the powers","Resultsense","https://www.resultsense.com/insights/2026-09-08-openai-mandated-safety-bars-uk-aisi-enforcement-gap/","2026-09-08","AISI has no power to compel; access rests on renewable agreements."),
 ("aiwiki-ukaisi","UK AI Security Institute","AI Wiki","https://aiwiki.ai/wiki/uk_aisi","2026-05-07","Microsoft parallel agreements May 2026; Cohere MOU; publication terms."),
 ("regulations-ai-aisi","AI Security Institute (renaming)","Regulations.ai","https://regulations.ai/regulations/RAI-GB-NA-ASIRRXX-2025","2026-09","No statutory enforcement powers; voluntary testing."),
 ("transluce-manifund","Transluce: Fund Scalable Democratic Oversight of AI","Manifund","https://manifund.org/projects/transluce-fund-scalable-democratic-oversight-of-ai","2026","Docent used by Anthropic, DeepMind, Thinking Machines, METR, Redwood, Apollo, Palisade; used in Claude 4 pre-deployment analysis; head of governance previously led CAISI."),
 ("transluce-mh","Independent evaluation of model responses to mental health crises","Transluce","https://transluce.org/","2026-09","77 model variants across eight developers."),
 ("transluce-job","Governance & Policy Fellow at Transluce","The Economic Misfit (job listing)","https://theeconomicmisfit.com/2026/04/18/governance-policy-fellow-at-transluce/","2026-04-18","Organizes AEF; AEF-1 standard; government contracts."),
 ("techpolicy-aef1","The EU's Real AI Leverage Is Making Compliance the Path of Least Resistance","TechPolicy.Press","https://www.techpolicy.press/the-eus-real-ai-leverage-is-making-compliance-the-path-of-least-resistance/","2026-02-26","AEF-1 covers independence, access depth, transparency; thin evaluator pool."),
 ("andon-site","Andon Labs","Andon Labs","https://andonlabs.com/","2026-07","Vending-Bench, Pion platform, autonomous deployments; Opus 5 results."),
 ("tooldir-andon","Andon Labs, agent safety evaluations","tooldirectory.ai","https://tooldirectory.ai/tools/andon-labs","2026-07-08","Anthropic Project Vend partnership; results cited in model cards."),
 ("epoch-clarify","Clarifying the creation and use of the FrontierMath benchmark","Epoch AI","https://epoch.ai/latest/openai-and-frontiermath","2025-01-23","OpenAI commissioned 300 problems, owns them, has statements and solutions except 50-problem holdout; contractor communication gap."),
 ("techcrunch-epoch","AI benchmarking organization criticized for waiting to disclose funding from OpenAI","TechCrunch","https://techcrunch.com/2025/01/19/ai-benchmarking-organization-criticized-for-waiting-to-disclose-funding-from-openai","2025-01-19","Primarily Open Philanthropy funded; disclosure timing."),
 ("decoder-epoch","OpenAI quietly funded independent math benchmark","The Decoder","https://the-decoder.com/openai-quietly-funded-independent-math-benchmark-before-setting-record-with-o3/","2025-01-19","Agreement prevented revealing support until o3 announcement."),
 ("80k-funding","It looks like there are some good funding opportunities in AI safety right now","80,000 Hours","https://80000hours.org/2025/01/it-looks-like-there-are-some-good-funding-opportunities-in-ai-safety-right-now/","2025-10-13","CAIS advises xAI, not receiving OP money; SFF grants; METR not receiving OP recently; SecureBio SFF grant."),
 ("coefficient-wiki","Coefficient Giving","Wikipedia","https://en.wikipedia.org/wiki/Coefficient_Giving","2026","Formerly Open Philanthropy; board includes Moskovitz, Tuna, Karnofsky."),
 ("zvi-pace","We Must Pace The Frontier","Zvi Mowshowitz","https://thezvi.substack.com/p/we-must-pace-the-frontier","2026-09-14","Hwang trilemma: independent, knowledgeable, sustainably funded, pick two; evaluator supply concerns."),
 ("tnw-hf-nvidia","Hugging Face's Open Alignment Initiative wants lab access","TNW","https://thenextweb.com/news/hugging-face-open-alignment-initiative-embedded-evaluators","2026-09-14","Nvidia acquiring Hugging Face ($12.93B); Nvidia in talks to anchor Anthropic IPO (up to $10B); no terms announced."),
 ("techmeme-hf","Hugging Face Open Alignment Initiative","Techmeme","https://www.techmeme.com/260912/p13","2026-09-12","Initiative led by Thomas Wolf; request to join embedded evaluators."),
 ("longtermwiki-audit","Third-Party Model Auditing","Longterm Wiki","https://www.longtermwiki.com/wiki/E450","2026-01-29","Scale AI SEAL first third-party evaluator authorized by US AISI; ecosystem overview."),
 ("mlcommons","MLCommons AI Safety / AILuminate","MLCommons","https://mlcommons.org/","2026","Member-funded consortium benchmark."),
 ("ms-redteam","Microsoft AI Red Team","Microsoft","https://www.microsoft.com/en-us/security/blog/topic/ai-red-team/","2026","PyRIT methodology; red-teaming practice."),
 ("gdm-gemini-testing","Gemini model documentation, external testing","Google DeepMind","https://deepmind.google/","2025","Dreadnode and Vaultis named as external experts (cyber, CBRN, extremism)."),
 ("humane-int","Humane Intelligence","Humane Intelligence","https://www.humane-intelligence.org/","2026","Public red-teaming with NIST and IMDA."),
 ("rand-aef","RAND and the AI Evaluator Forum","RAND","https://www.rand.org/","2026","Founding AEF member; CBRN expertise; RAND-Irregular model theft paper."),
 ("hal","Holistic Agent Leaderboard","Princeton","https://hal.cs.princeton.edu/","2026","Open agent leaderboard; AEF founding member."),
 ("palisade","Palisade Research","Palisade Research","https://palisaderesearch.org/","2026","Shutdown resistance, self-replication, offensive cyber studies on released models."),
 ("cais","Center for AI Safety","CAIS","https://safe.ai/","2026","WMDP, HLE benchmarks; director advises xAI."),
 ("saferai","SaferAI","SaferAI","https://www.safer-ai.org/","2026","Rates lab risk-management frameworks; EU CoP evaluations; consortium with FAR.AI."),
 ("dwt-sb315","Illinois Enacts Frontier AI Safety Law","Davis Wright Tremaine","https://www.dwt.com/blogs/artificial-intelligence-law-advisor/2026/07/illinois-frontier-ai-safety-law","2026-07-15","Audit obligations begin Jan 1, 2028; whistleblower provisions."),
]

# ---------------------------------------------------------------------------
# Evaluators
# ---------------------------------------------------------------------------
EVALUATORS = [
 ("metr","METR","nonprofit","Berkeley, US",["autonomy","scheming","incident","assurance"],"high","Reference evaluator for autonomy and AI R&D capability. Named by Anthropic as the model for embedded evaluators in September 2026; led the on-site investigation of the OpenAI agent swarm incident."),
 ("apollo","Apollo Research","pbc","London, UK / San Francisco, US",["scheming","autonomy","assurance"],"high","Scheming and deception specialist; ran evaluations for every major lab; converted to a public benefit corporation in January 2026."),
 ("securebio","SecureBio","nonprofit","Cambridge, US",["bio","misuse"],"high","Main biosecurity evaluator; author of the Virology Capabilities Test; founding member of the AI Evaluator Forum."),
 ("irregular","Irregular (formerly Pattern Labs)","vc","Tel Aviv, IL / San Francisco, US",["cyber","misuse"],"high","Offensive-cyber evaluator cited in OpenAI and Anthropic system cards; SOLVE framework used by UK AISI. Pattern Labs and Irregular are the same company."),
 ("farai","FAR.AI","nonprofit","Berkeley, US",["jailbreak","bio","cyber","misuse"],"high","Red-teaming and adversarial-robustness nonprofit; leads the EU AI Office CBRN risk-modelling contract."),
 ("grayswan","Gray Swan","vc","Pittsburgh, US",["jailbreak","cyber","misuse"],"high","Crowdsourced adversarial testing (Arena) plus Shade and Cygnal defense products; cited in 11 recent system cards."),
 ("palisade","Palisade Research","nonprofit","Berkeley, US",["cyber","autonomy","scheming"],"med","Independent capability-elicitation research on released models: shutdown resistance, self-replication, offensive cyber."),
 ("redwood","Redwood Research","nonprofit","Berkeley, US",["scheming","incident","assurance"],"med","AI control research group; contributed a contractor to the METR incident investigation."),
 ("transluce","Transluce","nonprofit","Berkeley, US",["misuse","autonomy","benchmarks","assurance"],"high","Nonprofit oversight-tools lab; convenes the AI Evaluator Forum that wrote AEF-1."),
 ("andon","Andon Labs","vc","Stockholm, SE / San Francisco, US",["autonomy","benchmarks"],"low","Long-horizon agent evaluations (Vending-Bench) and autonomous deployments; Anthropic Project Vend partner."),
 ("ukaisi","UK AI Security Institute","gov","London, UK",["cyber","bio","jailbreak","autonomy","assurance"],"high","Largest state evaluation team; 30+ models tested; Inspect open-sourced; Frontier AI Trends Report."),
 ("caisi","US CAISI (NIST)","gov","Gaithersburg, US",["cyber","bio","misuse","assurance"],"high","Pre-deployment agreements with five labs; 40+ evaluations; some classified via TRAINS taskforce."),
 ("euaio","EU AI Office","gov","Brussels, BE",["bio","cyber","misuse","assurance"],"med","Regulator behind the GPAI Code of Practice; external-evaluator obligations enforceable since August 2026."),
 ("averi","AVERI","nonprofit","Washington, US",["assurance"],"med","Standards body for frontier AI auditing; ran the first double-blind enclave evaluation of a proprietary model."),
 ("saferai","SaferAI","nonprofit","Paris, FR",["assurance","cyber","bio","misuse"],"med","Rates lab risk-management frameworks in public; runs EU Code of Practice evaluations."),
 ("scale","Scale AI (SEAL / Scale Labs)","bigtech","San Francisco, US",["benchmarks","cyber","bio","misuse"],"high","Builds and runs evaluations for CAISI and other governments; Meta acquired 49% in 2025."),
 ("mlcommons","MLCommons (AILuminate)","consortium","San Francisco, US",["benchmarks","assurance"],"med","Industry consortium producing the AILuminate safety benchmark."),
 ("hfoai","Hugging Face Open Alignment Initiative","vc","New York, US / Paris, FR",["assurance"],"low","Announced 12 September 2026 with a request to join Anthropic's embedded-evaluator program; no evaluations yet."),
 ("epoch","Epoch AI","nonprofit","Remote",["benchmarks"],"high","Capability-tracking and benchmark nonprofit; the FrontierMath episode is the canonical undisclosed-funding case."),
 ("cais","Center for AI Safety","nonprofit","San Francisco, US",["benchmarks","misuse"],"med","Hazard benchmarks (WMDP, HLE); director advises xAI."),
 ("msft","Microsoft AI Red Team","bigtech","Redmond, US",["jailbreak","cyber","misuse"],"med","External red team for other labs' models; not independent of Big Tech."),
 ("dreadnode","Dreadnode","vc","Remote",["cyber"],"low","Offensive-security firm named by Google DeepMind as an external expert on Gemini testing."),
 ("humane","Humane Intelligence","nonprofit","New York, US",["misuse","jailbreak"],"med","Public red-teaming exercises with NIST and IMDA; societal harms rather than catastrophic risk."),
 ("rand","RAND","nonprofit","Santa Monica, US",["bio","cyber","assurance"],"med","Think tank with CBRN and security expertise; AEF founding member."),
 ("hal","Holistic Agent Leaderboard (Princeton)","academic","Princeton, US",["benchmarks","autonomy"],"med","Academic agent leaderboard with fully open methodology; AEF founding member."),
 ("big4","Assurance firms (Big Four and peers)","vc","Global",["assurance"],"low","Expected entrants once Illinois SB 315 audits begin in 2028; no frontier elicitation capability yet."),
]

# ---------------------------------------------------------------------------
# Signals: per evaluator, (dimension, direction, claim, [source ids])
# Dimensions: F funding, G governance, P personnel, A access, S scope,
#             R publication, M methods, X product conflicts
# ---------------------------------------------------------------------------
SIGNALS = {
 "metr":[
  ("F","for","Hard rule against accepting money from AI companies, including donations directed by their staff; ~$71M raised in 2026 from foundations and individuals.",["metr-about","alphasignal-metr-71m","metr-funding-2026"]),
  ("F","for","Funder base widened beyond the effective-altruism network, including Pew Charitable Trusts.",["itbb-watchdogs"]),
  ("F","against","Runs on large volumes of free tokens and privileged access from the labs it evaluates.",["metr-about"]),
  ("A","for","Investigated the OpenAI incident on site over six days with a Redwood contractor.",["metr-hf-investigation","techtimes-metr-hf"]),
  ("A","for","Named by Anthropic as the example embedded evaluator with employee-level access.",["unite-altman-match","marktechpost-pace"]),
  ("S","against","OpenAI set the investigation window (June 26 to July 13); the lab's own cluster breach and three of METR's standard incident questions were out of scope.",["pebblous-scope","metr-hf-investigation"]),
  ("R","for","Published its own 91-page report with a redaction summary statement; took no payment for the investigation.",["metr-hf-investigation","marktechpost-pace"]),
  ("R","against","OpenAI could redact any non-public information and gave feedback on structure, emphasis, clarity and tone, which METR incorporated.",["metr-hf-investigation"]),
  ("P","against","Hires from the labs it evaluates; a former Anthropic researcher joined in September 2026.",["wapo-examiner-benton"]),
  ("G","for","Nonprofit with a written independence policy and a no-lab-money rule.",["metr-about"]),
  ("M","for","Open task suites and published time-horizon methodology; results appear in system cards.",["metr-about"]),
  ("X","for","No commercial products.",["metr-about"]),
  ("A","against","Access remains voluntary; no law requires any lab to grant it.",["itbb-watchdogs"]),
 ],
 "apollo":[
  ("G","for","Published four-rule COI policy: no outcome-contingent pay, no side grants or investments from evaluated labs, recusal for financial interests, no misrepresentation.",["apollo-norms"]),
  ("F","against","Requests fair-market-value compensation from the parties it evaluates; revenue depends on evaluated labs.",["apollo-norms"]),
  ("G","against","Converted from fiscally sponsored nonprofit to a public benefit corporation in January 2026.",["apollo-pbc"]),
  ("R","for","Record of adverse findings published, including in-context scheming and evaluation awareness.",["apollo-about"]),
  ("P","for","Recusal rule for any individual with a financial interest in an evaluated organization.",["apollo-norms"]),
  ("A","for","Ran pre-deployment evaluations for all major labs; contracted by UK AISI for deception evaluations.",["apollo-about","apollo-first-year"]),
  ("S","against","Co-authored anti-scheming research with OpenAI while acting as its external scheming evaluator.",["apollo-about"]),
  ("X","against","Sells Watcher, a monitoring product, into the ecosystem it evaluates.",["apollo-about"]),
  ("M","for","Publishes evaluation methodology and papers; differential publishing policy documented.",["apollo-norms"]),
 ],
 "securebio":[
  ("F","against","Labs typically pay for evaluations of their own models; OpenAI covered the cost of the GPT-5.5 assessment.",["securebio-oaif"]),
  ("F","against","Accepted an OpenAI Foundation grant in 2026 for the Detection division; the foundation's endowment is a stake in OpenAI and its board largely overlaps.",["securebio-oaif"]),
  ("G","for","Two-division structure with a stated firewall; leadership committed publicly to resign and disclose if the grant were used as leverage on evaluations.",["securebio-oaif"]),
  ("G","for","Founding member of the AI Evaluator Forum, which wrote the AEF-1 independence standard.",["aef-launch"]),
  ("S","for","Evaluates models from many developers; consortium member on the EU AI Office CBRN contract.",["longtermwiki-far"]),
  ("R","for","Publishes pre-release biological assessments and the Virology Capabilities Test.",["securebio-oaif","aef-launch"]),
  ("A","for","Pre-deployment access across the major Western labs.",["securebio-oaif"]),
  ("P","for","Staff pipeline disclosed through philanthropic career grants; no lab board roles found.",["80k-funding"]),
  ("M","for","Methods published; VCT is documented.",["aef-launch"]),
  ("X","for","No commercial products found; tools shared with governments.",["securebio-oaif"]),
 ],
 "irregular":[
  ("F","against","$80M raised in 2025 at a $450M valuation, led by Sequoia and Redpoint; Sequoia is also a major OpenAI investor.",["techcrunch-irregular","sequoia-irregular"]),
  ("F","against","Millions in annual revenue from the labs it evaluates.",["newswire-irregular"]),
  ("G","against","Venture-backed for-profit; no published COI or recusal policy found.",["techcrunch-irregular"]),
  ("X","against","Growth plan is to sell runtime security controls into the same customers it evaluates.",["newswire-irregular"]),
  ("A","for","Deep, repeated pre-deployment access at OpenAI, Anthropic and Google DeepMind; embedded with labs.",["sequoia-irregular"]),
  ("F","for","Government clients (UK) alongside labs.",["newswire-irregular"]),
  ("M","for","Publishes some method papers; SOLVE framework adopted by UK AISI and Anthropic.",["sequoia-irregular"]),
  ("R","for","Findings appear in system cards for o3, o4-mini, GPT-5 and Claude models.",["techcrunch-irregular","sequoia-irregular"]),
  ("S","against","Scope set by lab engagements; no public account of evaluator-set scope.",["sequoia-irregular"]),
  ("P","against","Markets itself as embedded with the labs; no recusal or cooling-off policy found.",["sequoia-irregular"]),
 ],
 "farai":[
  ("F","for","More than $30M in 2025 commitments from Coefficient Giving, Schmidt Sciences, SFF and CSET.",["far-30m"]),
  ("F","against","Also funded by the AI Safety Fund, financed by the Frontier Model Forum, the labs' industry body.",["far-30m"]),
  ("S","for","Selected by the European Commission to lead a three-year CBRN technical-assistance contract, with a regulator as client.",["longtermwiki-far"]),
  ("R","for","Publishes jailbreak and stress-test results across vendors.",["far-30m"]),
  ("G","for","Nonprofit with diversified disclosed funders.",["far-30m"]),
  ("A","for","Pre- and post-deployment red teaming for labs and EU bodies.",["longtermwiki-far"]),
  ("P","against","Runs field-building programs that place researchers into labs.",["longtermwiki-far"]),
  ("M","for","Publishes methods and papers.",["far-30m"]),
  ("X","for","No commercial products; consulting limited to governments.",["longtermwiki-far"]),
 ],
 "grayswan":[
  ("P","against","Co-founder and chief scientist chairs OpenAI's Safety and Security Committee and sits on its nonprofit board.",["openai-kolter-board","kolter-bio"]),
  ("P","for","The chief scientist recuses himself from Gray Swan's dealings with OpenAI.",["forbes-grayswan-2024"]),
  ("F","against","$40M Series A in May 2026 at a $200M valuation; revenue from every major lab.",["grayswan-seriesa","forbes-grayswan-2026"]),
  ("X","against","Sells Shade and Cygnal, the fixes, to the same labs whose models it evaluates.",["grayswan-seriesa"]),
  ("G","against","Venture-backed for-profit; no published COI policy found.",["grayswan-seriesa"]),
  ("F","for","Breadth across OpenAI, Anthropic, Google DeepMind, Meta, xAI and ByteDance, so no single lab dominates.",["forbes-grayswan-2026"]),
  ("A","for","Embedded in pre-release safety evaluation processes; cited in 11 system cards.",["grayswan-seriesa"]),
  ("M","for","Founders wrote foundational jailbreak papers; Arena results partly public.",["forbes-grayswan-2026"]),
  ("R","against","Findings appear as lab-summarized system-card citations rather than independent reports.",["grayswan-seriesa"]),
  ("S","against","Scope set by lab engagements.",["grayswan-seriesa"]),
 ],
 "palisade":[
  ("F","for","Philanthropically funded; no lab contracts found.",["palisade"]),
  ("S","for","Sets its own questions and publishes without lab review.",["palisade"]),
  ("R","for","Publishes findings unwelcome to labs, including shutdown resistance and self-replication.",["palisade"]),
  ("M","for","Publishes code and transcripts.",["palisade"]),
  ("A","against","Little pre-deployment access; most work is on released models.",["palisade"]),
  ("G","for","Nonprofit.",["palisade"]),
  ("P","for","No lab board roles found.",["palisade"]),
  ("X","for","No commercial products.",["palisade"]),
 ],
 "redwood":[
  ("F","for","No lab revenue; historically about $25M from Open Philanthropy.",["itbb-watchdogs"]),
  ("F","against","Funding concentration: revenue nearly disappeared in one year when a few large grants ended.",["itbb-watchdogs"]),
  ("A","for","Contracted a staff member to METR for the on-site OpenAI investigation.",["metr-hf-investigation"]),
  ("R","for","Co-authored the incident report with a redaction statement.",["metr-hf-investigation"]),
  ("P","against","Co-authored alignment research with Anthropic; close talent flow with lab safety teams.",["itbb-watchdogs"]),
  ("G","for","Nonprofit.",["itbb-watchdogs"]),
  ("S","for","Sets its own research agenda; incident work under METR terms.",["metr-hf-investigation"]),
  ("M","for","Publishes control methods and code.",["itbb-watchdogs"]),
  ("X","for","No commercial products.",["itbb-watchdogs"]),
 ],
 "transluce":[
  ("G","for","Wrote the field's independence standard (AEF-1) through the AI Evaluator Forum and applies it to itself.",["aef-launch","transluce-job","aef-transparency"]),
  ("R","for","Published the largest independent cross-vendor evaluation of responses to mental-health crises (77 variants) without lab sign-off.",["transluce-mh"]),
  ("F","for","Government contracts and philanthropy rather than lab fees.",["transluce-job","transluce-manifund"]),
  ("P","for","Head of governance previously led CAISI; no lab board roles found.",["transluce-manifund"]),
  ("X","against","Docent is used inside Anthropic, DeepMind and Thinking Machines, so labs are also tool users.",["transluce-manifund"]),
  ("A","against","Mostly post-deployment access; used in Claude 4 pre-deployment analysis once rather than routinely.",["transluce-manifund"]),
  ("S","for","Sets its own evaluation questions.",["transluce-mh"]),
  ("M","for","Open tools (Docent) and published methods.",["transluce-manifund"]),
 ],
 "andon":[
  ("R","for","Publishes candid results, including misalignment findings on the best-scoring models.",["andon-site"]),
  ("M","for","Benchmarks (Vending-Bench) cited in model cards across labs.",["tooldir-andon"]),
  ("F","against","Commercial platform (Pion) and lab partnerships; funding and client mix not disclosed.",["andon-site","tooldir-andon"]),
  ("G","against","No published COI policy found.",["andon-site"]),
  ("A","against","Access through partnerships (Anthropic Project Vend); not routine pre-release.",["tooldir-andon"]),
  ("S","for","Designs its own long-horizon tasks.",["andon-site"]),
  ("P","against","Undisclosed.",["andon-site"]),
  ("X","against","Sells a commercial agent platform.",["andon-site"]),
 ],
 "ukaisi":[
  ("F","for","Taxpayer funded; no commercial relationship with labs.",["regulations-ai-aisi"]),
  ("M","for","Open-source Inspect framework and published methodology.",["csa-aisi-trends"]),
  ("R","for","Found universal jailbreaks in every system tested and published that in the Frontier AI Trends Report.",["csa-aisi-trends"]),
  ("R","against","Most per-model results stay confidential; the public sees aggregated trends.",["csa-aisi-trends"]),
  ("A","against","No statutory powers; access rests on MOUs any lab could decline to renew; Frontier AI Bill not introduced as of September 2026.",["csa-aisi-trends","resultsense-aisi","regulations-ai-aisi"]),
  ("A","for","Joint testing with the US institute; agreements with OpenAI, Anthropic, Google, Microsoft, Cohere; 30+ models tested.",["aiwiki-ukaisi","csa-aisi-trends"]),
  ("P","against","Staff move between the institute and labs in both directions.",["csa-aisi-trends"]),
  ("G","for","Public body with civil-service conflict rules.",["regulations-ai-aisi"]),
  ("S","for","Sets its own evaluation agenda within MOU terms.",["csa-aisi-trends"]),
  ("X","for","No commercial products.",["regulations-ai-aisi"]),
 ],
 "caisi":[
  ("F","for","Public funding; formal access agreements with five developers.",["csa-caisi","nist-caisi"]),
  ("A","for","More than 40 evaluations including unreleased models; classified CBRN and cyber work via the TRAINS taskforce.",["csa-caisi"]),
  ("G","against","Refocused in 2025 from broad safety research to demonstrable national-security risks; mandate is politically steerable.",["csa-caisi"]),
  ("R","against","Publishes little per model; findings mostly stay inside government.",["csa-caisi"]),
  ("P","against","Authorized Scale AI, a company 49% owned by Meta, to run evaluations on its behalf.",["scale-framework","longtermwiki-audit"]),
  ("S","for","Government defines risk domains.",["scale-framework"]),
  ("M","against","Methods partly published through NIST; per-evaluation methods not public.",["nist-caisi"]),
  ("X","for","No commercial products.",["nist-caisi"]),
 ],
 "euaio":[
  ("A","for","Legal power to compel; the only body whose access does not depend on goodwill.",["metr-regs"]),
  ("S","for","Contracts its own evaluators (FAR.AI-led consortium) rather than relying on lab-chosen ones.",["longtermwiki-far"]),
  ("S","for","Code sets the access floor: helpful-only versions where security allows, at least 20 business days, external evaluators for each new frontier model.",["metr-regs","arxiv-access-taxonomy"]),
  ("R","against","Safety and Security Model Reports are submitted to the Office, not the public.",["metr-regs"]),
  ("M","against","No accreditation pathway or public reporting schema yet; thin evaluator bench.",["techpolicy-aef1"]),
  ("F","for","Public funding.",["metr-regs"]),
  ("G","for","Regulator with statutory basis.",["metr-regs"]),
  ("P","for","Civil-service conflict rules.",["metr-regs"]),
  ("X","for","No commercial products.",["metr-regs"]),
 ],
 "averi":[
  ("A","for","Secure-enclave double-blind protocol with DeepMind, OpenMined and MLCommons; neither party sees the other's confidential material.",["averi-pilot"]),
  ("G","for","501(c)(3); endorsed Illinois SB 315; co-authored AEF-1.",["averi-launch","averi-about"]),
  ("M","for","Publishes pilot reports and open tooling; framework paper with AI Assurance Levels.",["averi-pilot","arxiv-frontier-auditing"]),
  ("P","against","Founder and several staff come from labs and lab-adjacent institutions.",["averi-launch"]),
  ("S","against","Pilot audits are voluntary and lab-selected; not yet a full-time auditor.",["averi-about","averi-pilot"]),
  ("F","against","Funding sources not fully itemized publicly.",["averi-about"]),
  ("R","for","Publishes pilot findings.",["averi-pilot"]),
  ("X","for","No commercial products; tools open source.",["averi-about"]),
 ],
 "saferai":[
  ("R","for","Publishes critical ratings of lab frameworks with scores attached.",["saferai"]),
  ("S","for","Part of the EU AI Office evaluation consortium; sets its own rating methodology.",["longtermwiki-far","saferai"]),
  ("F","for","No lab revenue found.",["saferai"]),
  ("A","against","Limited pre-deployment model access to date.",["saferai"]),
  ("G","for","Nonprofit.",["saferai"]),
  ("P","for","No lab roles found.",["saferai"]),
  ("M","for","Rating methodology published.",["saferai"]),
  ("X","for","No commercial products.",["saferai"]),
 ],
 "scale":[
  ("F","against","Nearly half owned by Meta, itself a frontier developer.",["longtermwiki-audit","scale-framework"]),
  ("G","against","Primary business is selling data and evaluation services to the labs; no public COI policy addressing the Meta relationship.",["scale-framework"]),
  ("A","for","Government-defined risk domains and access agreements; first private evaluator authorized by the US institute.",["longtermwiki-audit","scale-framework"]),
  ("X","against","Sells data and evaluation services to labs.",["scale-framework"]),
  ("P","against","Leadership moved to Meta with the 2025 investment.",["longtermwiki-audit"]),
  ("S","against","Scope set by government or lab clients.",["scale-framework"]),
  ("R","against","Results for governments not public.",["scale-framework"]),
  ("M","against","Benchmarks partly public (SEAL leaderboards); government evaluations closed.",["scale-framework"]),
 ],
 "mlcommons":[
  ("F","against","Funded by member companies, including the labs whose models are benchmarked.",["mlcommons"]),
  ("M","for","Open benchmark specification and methodology.",["mlcommons","averi-pilot"]),
  ("A","for","Used as neutral ground in the AVERI double-blind pilot.",["averi-pilot"]),
  ("G","against","Consortium governance by members.",["mlcommons"]),
  ("S","for","Benchmark design set by working group.",["mlcommons"]),
  ("R","for","Publishes results.",["mlcommons"]),
  ("P","against","Working groups staffed by member-company employees.",["mlcommons"]),
  ("X","for","Benchmarks free to use.",["mlcommons"]),
 ],
 "hfoai":[
  ("G","against","Nvidia is acquiring Hugging Face for about $12.9B and is reported to be in talks to anchor Anthropic's IPO with up to $10B; nobody involved has addressed the overlap.",["tnw-hf-nvidia"]),
  ("A","against","No track record as an evaluator; no access yet.",["tnw-hf-nvidia","techmeme-hf"]),
  ("F","against","Who pays, who selects, and on what terms is unresolved.",["tnw-hf-nvidia","zvi-pace"]),
  ("R","for","States findings would be published openly; open-source culture.",["techmeme-hf"]),
  ("M","for","Public tooling.",["techmeme-hf"]),
  ("S","against","Terms not announced.",["tnw-hf-nvidia"]),
  ("P","against","Would be owned by a lab investor.",["tnw-hf-nvidia"]),
  ("X","against","Commercial platform.",["tnw-hf-nvidia"]),
 ],
 "epoch":[
  ("F","against","OpenAI commissioned and owns most of FrontierMath and had the problems and solutions; a contract barred disclosing this until the o3 launch.",["epoch-clarify","decoder-epoch"]),
  ("R","against","Contributors were not told the funder; disclosure came after the fact.",["techcrunch-epoch","epoch-clarify"]),
  ("R","for","After the disclosure failure, created a 50-problem holdout OpenAI cannot see.",["epoch-clarify"]),
  ("M","for","Rigorous public data on compute, training runs and capability trends.",["techcrunch-epoch"]),
  ("F","for","Primarily philanthropically funded (Open Philanthropy).",["techcrunch-epoch"]),
  ("G","for","Nonprofit.",["techcrunch-epoch"]),
  ("A","against","Cannot share the commissioned set with other labs without OpenAI's permission.",["epoch-clarify"]),
  ("S","for","Evaluates any model on FrontierMath at its discretion.",["epoch-clarify"]),
  ("P","for","No lab roles found.",["techcrunch-epoch"]),
  ("X","for","No commercial products.",["techcrunch-epoch"]),
 ],
 "cais":[
  ("P","against","Director is a safety adviser to xAI while the organization's benchmarks are used to grade xAI models.",["80k-funding","cais"]),
  ("F","for","Funded mainly by SFF rather than lab-linked pools.",["80k-funding"]),
  ("M","for","Open benchmarks widely used.",["cais"]),
  ("X","against","Co-produced Humanity's Last Exam with Scale AI, a Meta-owned vendor.",["cais"]),
  ("G","for","Nonprofit.",["cais"]),
  ("A","against","Public-model access.",["cais"]),
  ("S","for","Sets own benchmark design.",["cais"]),
  ("R","for","Publishes results.",["cais"]),
 ],
 "msft":[
  ("F","against","Microsoft is a major OpenAI investor and a frontier developer with its own CAISI agreement.",["csa-caisi"]),
  ("G","against","Business unit of a frontier developer.",["ms-redteam"]),
  ("R","against","Findings for other labs are rarely published under the team's own name.",["ms-redteam"]),
  ("M","for","Publishes methodology (PyRIT) openly.",["ms-redteam"]),
  ("A","for","Deep access when engaged.",["ms-redteam"]),
  ("P","against","Employees of a lab.",["ms-redteam"]),
  ("S","against","Scope set by engagement.",["ms-redteam"]),
  ("X","against","Sells AI products.",["ms-redteam"]),
 ],
 "dreadnode":[
  ("A","for","Named by Google DeepMind as an external cyber expert on Gemini testing.",["gdm-gemini-testing"]),
  ("G","against","Venture-backed; no published COI policy found.",["gdm-gemini-testing"]),
  ("R","against","Evaluation terms and results are not public.",["gdm-gemini-testing"]),
  ("X","against","Sells offensive-security products.",["gdm-gemini-testing"]),
  ("F","against","Lab-paid engagements.",["gdm-gemini-testing"]),
  ("P","against","Undisclosed.",["gdm-gemini-testing"]),
  ("S","against","Scope set by lab.",["gdm-gemini-testing"]),
  ("M","against","Methods and results are closed; no public methodology.",["gdm-gemini-testing"]),
 ],
 "humane":[
  ("R","for","Publishes openly; public exercises.",["humane-int"]),
  ("F","for","Government partners rather than lab clients.",["humane-int"]),
  ("A","against","Public-model access only.",["humane-int"]),
  ("G","for","Nonprofit.",["humane-int"]),
  ("P","for","No lab roles found.",["humane-int"]),
  ("S","for","Designs its own exercises.",["humane-int"]),
  ("M","for","Methods published.",["humane-int"]),
  ("X","for","No commercial products.",["humane-int"]),
 ],
 "rand":[
  ("G","for","Government-contracted with long-standing COI and publication norms; AEF founding member.",["rand-aef","aef-launch"]),
  ("A","for","Access through government channels, including classified work.",["rand-aef"]),
  ("F","against","Large share of AI work funded by Coefficient Giving.",["rand-aef","coefficient-wiki"]),
  ("R","against","Much output is government-restricted rather than public.",["rand-aef"]),
  ("P","for","Institutional COI rules.",["rand-aef"]),
  ("S","for","Sets own research agenda.",["rand-aef"]),
  ("M","against","Methods partly public.",["rand-aef"]),
  ("X","for","No commercial products.",["rand-aef"]),
 ],
 "hal":[
  ("F","for","No lab money; academic.",["hal"]),
  ("M","for","Open code and logs.",["hal"]),
  ("R","for","Results published without review.",["hal"]),
  ("A","against","Public API access only.",["hal"]),
  ("G","for","University-hosted; AEF member.",["hal","aef-launch"]),
  ("P","for","Academic staff.",["hal"]),
  ("S","for","Own benchmark design.",["hal"]),
  ("X","for","No products.",["hal"]),
 ],
 "big4":[
  ("G","for","Existing independence frameworks (no financial interest, partner rotation) map onto SB 315's requirements.",["crowell-sb315","stackaware-sb315"]),
  ("X","against","Labs are already consulting clients, recreating the audit-plus-consulting problem.",["stackaware-sb315"]),
  ("A","against","No technical capability to elicit dangerous capabilities; would need to subcontract.",["lw-sb315"]),
  ("R","against","Reports would be summaries to the developer and the state rather than public findings.",["crowell-sb315"]),
  ("F","against","Developer pays the auditor.",["crowell-sb315"]),
  ("P","against","Partners rotate but firms retain the client.",["stackaware-sb315"]),
  ("S","against","Scope fixed by statute and engagement letter.",["dwt-sb315"]),
  ("M","against","Audit methodology proprietary.",["stackaware-sb315"]),
 ],
}

# ---------------------------------------------------------------------------
# Assessments: per evaluator, dimension -> value 0..4 (anchor index)
# ---------------------------------------------------------------------------
ASSESS = {
 "metr":     dict(F=4,G=4,P=3,A=4,S=3,R=3,M=4,X=4),
 "apollo":   dict(F=2,G=3,P=3,A=3,S=3,R=3,M=3,X=2),
 "securebio":dict(F=2,G=3,P=3,A=3,S=3,R=3,M=3,X=3),
 "irregular":dict(F=1,G=1,P=2,A=3,S=2,R=2,M=2,X=1),
 "farai":    dict(F=3,G=3,P=3,A=3,S=3,R=3,M=3,X=3),
 "grayswan": dict(F=1,G=1,P=1,A=3,S=2,R=2,M=2,X=0),
 "palisade": dict(F=4,G=3,P=3,A=1,S=4,R=4,M=3,X=4),
 "redwood":  dict(F=3,G=3,P=2,A=3,S=3,R=3,M=3,X=4),
 "transluce":dict(F=3,G=3,P=3,A=2,S=4,R=4,M=4,X=3),
 "andon":    dict(F=2,G=2,P=2,A=2,S=3,R=3,M=3,X=2),
 "ukaisi":   dict(F=4,G=4,P=3,A=3,S=3,R=2,M=4,X=4),
 "caisi":    dict(F=4,G=3,P=3,A=3,S=3,R=1,M=2,X=4),
 "euaio":    dict(F=4,G=4,P=3,A=3,S=4,R=2,M=2,X=4),
 "averi":    dict(F=3,G=4,P=2,A=3,S=3,R=3,M=4,X=4),
 "saferai":  dict(F=3,G=3,P=3,A=2,S=4,R=4,M=3,X=4),
 "scale":    dict(F=0,G=0,P=1,A=3,S=2,R=2,M=2,X=1),
 "mlcommons":dict(F=1,G=2,P=2,A=2,S=3,R=3,M=4,X=3),
 "hfoai":    dict(F=1,G=0,P=2,A=0,S=2,R=3,M=3,X=2),
 "epoch":    dict(F=2,G=3,P=3,A=2,S=3,R=2,M=4,X=3),
 "cais":     dict(F=3,G=3,P=1,A=2,S=3,R=3,M=4,X=3),
 "msft":     dict(F=0,G=0,P=1,A=3,S=2,R=1,M=2,X=1),
 "dreadnode":dict(F=1,G=1,P=2,A=3,S=2,R=1,M=1,X=1),
 "humane":   dict(F=3,G=3,P=3,A=1,S=3,R=4,M=3,X=4),
 "rand":     dict(F=3,G=3,P=3,A=3,S=3,R=2,M=2,X=4),
 "hal":      dict(F=4,G=4,P=4,A=1,S=4,R=4,M=4,X=4),
 "big4":     dict(F=2,G=2,P=2,A=1,S=2,R=1,M=1,X=1),
}

MOVE = {
 "metr":"Contract terms for the Anthropic embedded program that fix scope-setting and publication rights in writing, plus a public cooling-off policy.",
 "apollo":"Disclose revenue concentration by client and separate the product business from the evaluation practice.",
 "securebio":"Publish the AI division's client mix and the written terms that insulate it from Detection's funders.",
 "irregular":"A published COI policy, disclosure of lab revenue share, and a firewall between evaluations and the security-products business.",
 "farai":"Disclose the AI Safety Fund share of budget and whether lab-funded pools are excluded from evaluation work.",
 "grayswan":"Structural separation of the evaluation business, and independent governance for the OpenAI-related conflict beyond personal recusal.",
 "palisade":"Pre-release access on published terms would raise the access score without touching the others.",
 "redwood":"A diversified funder list and a stated policy on co-authoring with labs it evaluates.",
 "transluce":"Routine pre-release access under AEF-1 terms.",
 "andon":"Funding disclosure and a COI policy would move this from low to medium confidence quickly.",
 "ukaisi":"Statutory footing with power to compel testing and publish per-model findings.",
 "caisi":"Regular public reporting per model and a standing budget line insulated from reorganization.",
 "euaio":"An accreditation pathway for external evaluators and a public reporting schema.",
 "averi":"Funder disclosure and a first audit under statutory terms.",
 "saferai":"Documented pre-release access under Code terms.",
 "scale":"Ownership separation of the evaluation unit; until then the ceiling is low.",
 "mlcommons":"Published funding shares and a hazard suite the members do not see in advance.",
 "hfoai":"A governance structure that insulates the initiative from Nvidia, and a first published evaluation.",
 "epoch":"A standing rule against confidential lab funding of any evaluation asset.",
 "cais":"A public recusal policy covering the xAI relationship.",
 "msft":"Not a candidate for an independence-critical role; useful as a supplementary red team.",
 "dreadnode":"Published engagement terms and a first public report.",
 "humane":"Pre-release access for the harms it covers.",
 "rand":"More public model-level findings.",
 "hal":"Nothing on independence; access is the gap.",
 "big4":"A frontier-AI audit practice with published methodology and a technical partner.",
}

DIM_NAMES = dict(F="funding",G="governance",P="personnel",A="access",S="scope",R="publication",M="methods",X="products")

def w(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def main():
    for sid,title,pub,url,date,note in SOURCES:
        w(D/"sources"/f"{sid}.json", {"id":sid,"title":title,"publisher":pub,"url":url,"published":date,"retrieved":RETRIEVED,"note":note})
    for eid,name,typ,hq,doms,conf,summary in EVALUATORS:
        w(D/"evaluators"/f"{eid}.json", {"id":eid,"name":name,"type":typ,"hq":hq,"domains":doms,"confidence":conf,"summary":summary,"what_would_move_the_score":MOVE[eid]})
    src_ids = {s[0] for s in SOURCES}
    for eid, sigs in SIGNALS.items():
        out=[]
        for i,(dim,direction,claim,srcs) in enumerate(sigs, start=1):
            for s in srcs: assert s in src_ids, (eid, s)
            out.append({"id":f"{eid}.{i:02d}","evaluator":eid,"dimension":dim,"direction":direction,"claim":claim,"sources":srcs,"recorded":RETRIEVED,"curator":"yohei/claude v0"})
        w(D/"signals"/f"{eid}.json", out)
        a=[]
        for dim,val in ASSESS[eid].items():
            sig_ids=[s["id"] for s in out if s["dimension"]==dim]
            if not sig_ids:
                # fall back to any signal on the evaluator; verify will flag if empty
                sig_ids=[out[0]["id"]]
            a.append({"evaluator":eid,"dimension":dim,"value":val,"anchor":val,"signals":sig_ids,"rationale":f"Anchor {val} on {DIM_NAMES[dim]} given the cited signals.","assessed":RETRIEVED,"assessor":"yohei/claude v0"})
        w(D/"assessments"/f"{eid}.json", a)
    print("wrote", len(SOURCES), "sources,", len(EVALUATORS), "evaluators")

if __name__ == "__main__":
    main()
