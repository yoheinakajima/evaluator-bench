# Who Pays the Referee? Measuring Third-Party Evaluator Independence in Frontier AI Against Two Centuries of Assurance Regimes

Draft v0.3, 14 September 2026. All numbers regenerate from this repository at the pinned commit. Dataset B milestone years are spot-checked against secondary sources and need primary-source verification before submission.

## Abstract

Frontier AI developers now cite outside evaluators in nearly every model release, and regulators in the European Union and Illinois require "independent" external evaluation without defining it. We ask two questions. How independent are the evaluators the field relies on, measured against criteria that other industries eventually wrote into law? And where does frontier AI sit on the path those industries took from voluntary assurance to regulated independence? We answer with two open datasets. Dataset A scores 28 organizations that evaluate frontier models on eight independence dimensions (funding, governance, personnel, access depth, scope control, publication rights, method transparency, product conflicts), each 0 to 4 with written anchors, each assessment linked to dated, sourced signals and rebuilt from an append-only event log. Dataset B codes the lifecycle of sixteen assurance regimes across fifteen industries as dated milestones: voluntary assurance, trigger incidents, mandates, standards, oversight of assurers, independence rules, access and publication rules. Three findings. First, rules follow public failures quickly: across twenty trigger events the median lag to the next rule is two years and the maximum is ten, while the interval from a regime's first milestone to its first independence rule ranges from five years to more than two centuries. Second, the party being assessed almost always keeps paying the assessor; independence arrived through standards, inspection of assessors, rotation, liability, and public ratings, and the two regimes that removed the payer conflict did so by routing payment through insurers or funding the assessor from a party with opposing incentives. Third, the 2026 frontier AI evaluator population is strongest on scope control and method transparency and weakest on access, funding, and personnel, and it has reached six of seven lifecycle stages in four years while skipping the one every mature regime built: oversight of the evaluators themselves.

## 1. Introduction

In September 2026 the chief executives of the two largest frontier AI developers committed, within hours of each other, to giving outside evaluators employee-level access to their systems and the right to publish findings without editorial control. The commitments name METR as the model evaluator. They do not say who will pay the evaluators, who will select them, or what happens when an evaluator and a lab disagree about what counts as security-sensitive. A month earlier, Illinois enacted the first statutory audit mandate for frontier developers, borrowing its independence test from financial audit: neither party may hold a financial interest in the other. A month before that, the European Union's Code of Practice made external evaluation of systemic-risk models an enforceable obligation, with an access floor of twenty business days and minimally guardrailed model versions.

The organizations these instruments point at are few. The same six or seven groups appear in the system cards of OpenAI, Anthropic, and Google DeepMind. Some are nonprofits that refuse lab money; some are venture-backed companies whose investors also back the labs; one is a business unit of a frontier developer; one is a founder's side project whose chief scientist chairs a lab's safety committee. Nobody has published a scored, sourced account of them.

There is a long literature arguing that AI should learn from the assurance regimes of other industries (Raji et al. 2022; Manheim et al. 2025; Brundage et al. 2026). That argument is made. What is missing is measurement on both sides of the analogy: a coded reading of the AI evaluator population against the criteria other industries adopted, and a coded history of when and why those industries adopted them. This paper supplies both and reports what the comparison says.

Contributions:

1. Dataset A, an evidence-linked scorecard of 26 frontier AI evaluators on eight independence dimensions, with 227 dated signals citing 68 public sources, built as an event-sourced graph so every score traces to its evidence.
2. Dataset B, a lifecycle dataset of sixteen assurance regimes coded as dated milestones of eleven kinds, with per-regime payer, access, and publication models.
3. A stage ladder that places frontier AI on the trajectory other regimes followed, and three empirical regularities about how assurance regimes acquire independence.
4. A reading of what those regularities imply for the design choices now open in AI.

## 2. Related work

Frameworks for third-party evaluation of AI systems have proliferated: audit ecosystem design (Raji et al. 2022), the ASPIRE criteria for external scrutiny (Anderljung et al. 2023), access taxonomies (Casper et al. 2024; Charnock et al. 2026), compliance reviews of safety frameworks (Homewood et al. 2025), and AI Assurance Levels (Brundage et al. 2026). The AI Evaluator Forum's AEF-1 standard specifies minimum operating conditions for independent evaluation. Empirical work on auditors exists for algorithmic bias audits: a field scan and practitioner survey (Costanza-Chock et al. 2022) and a coded analysis of 116 published New York City hiring-tool audits (Groves et al. 2025). Rating efforts score developers' safety frameworks (SaferAI; the Future of Life Institute index), not evaluators. Cross-industry precedent appears in most of these papers as illustration; the systematic search closest in spirit (Anderson-Samways 2024) catalogs US regulatory instruments rather than assurance-provider lifecycles. We are aware of no prior work that codes the frontier evaluator population against independence criteria with sourced evidence, and none that codes assurance-regime lifecycles as comparable dated events. A fuller annotated bibliography is in the repository.

## 3. Datasets

### 3.1 Dataset A: the evaluator scorecard

Population. Organizations that (a) have evaluated or red-teamed a frontier model before or shortly after release and been cited by a developer, government, or regulator for doing so, or (b) have a stated role in the emerging audit layer (standards bodies, regulators, announced entrants). Twenty-six organizations as of v0: ten specialized evaluators, three government bodies, seven assurance or standards organizations, four benchmark and academic groups, and two categories of expected entrant.

Dimensions and anchors. Eight dimensions, each scored 0 to 4 against written anchors. The set draws on AEF-1's five operating conditions, on the auditor-independence rules Illinois SB 315 imports from financial audit, and on the Charnock et al. access taxonomy, with two additions the AI literature tends to omit: who owns the evaluator, and whether it sells remediation to the companies it grades. Anchors are in `data/dimensions.json`.

Evidence model. A signal is one dated claim, for or against, on one dimension, citing at least one source with a URL and a retrieval date. An assessment is a value on one dimension citing at least one signal on that dimension. A score is a weighted total, never stored, recomputed at build time under named weight presets. Integrity is enforced by a verifier: no orphan sources, no assessment without a signal, no 4 without a supporting signal, no 0 without an opposing one. The build writes every object into an append-only event log under a frozen clock; two builds on the same data produce a byte-identical log, and the provenance of every score names the events it rests on.

Coding. Version 0 is single-coder from public sources between 12 and 14 September 2026. Confidence tags (high, medium, low) mark thin records. A second-coder pass with disagreements logged in the rationale fields is scheduled before submission.

### 3.2 Dataset B: assurance-regime lifecycles

Sixteen regimes: financial statement audit, credit ratings, electrical and consumer product safety, pharmaceutical safety and efficacy, aircraft certification, nuclear safety and safeguards, ship classification, cybersecurity assurance, boilers and pressure vessels, food safety, automobile crash safety, sustainability reporting assurance, dietary supplements, crypto exchange proof of reserves, platform and hiring-algorithm audits, and frontier AI evaluation. The first eleven are regimes that reached mandated assurance; the next four were added to avoid selecting on success and include one rollback (supplements), one collapse of voluntary assurance (crypto), one slow voluntary period (sustainability), and one young regime that wrote independence rules at the start (platform audits).

Milestones are coded by kind: voluntary_assurance, trigger, mandate, standards, accreditation (oversight of assessors), independence_rule, delegation_reform, payer_reform, access_expansion, publication_rule, delegation, payer_shift, rollback. Each regime also records its payer model, access model, and publication model. Year granularity. Every milestone cites a source; v0 uses secondary sources with years spot-checked, and each entry is flagged for primary verification.

## 4. Method

Instrument strength and trigger criterion. Every rule milestone carries a strength from 1 (disclosure or voluntary text) to 4 (structural change: separation of functions, rotation, a new inspecting body, payment rerouted, delegation reclaimed). Every trigger carries a harm class and must meet a criterion set before looking at what followed: ten or more deaths, losses above one billion dollars, or a documented integrity failure of the assurance itself.

Stage ladder. Seven stages are defined from milestone kinds: S1 voluntary assurance, S2 trigger, S3 mandate, S4 standards, S5 oversight of assessors, S6 independence rules (independence_rule, delegation_reform, payer_reform), S7 access and publication rules. A regime reaches a stage in the year of the first qualifying milestone. Delegation, payer shifts toward the assessed party, and rollbacks are recorded and displayed but do not advance a stage.

Lags. For each trigger we compute the years to the next milestone of any rule kind (mandate, standards, accreditation, independence_rule, delegation_reform, payer_reform, publication_rule). For each regime we compute the interval from its first milestone to its first S6 milestone.

Paths. Each regime's milestones are ordered by year and written as a sequence of kinds with consecutive repeats collapsed. Similarity between frontier AI's sequence and each regime's opening is one minus the normalized Levenshtein distance over openings of comparable length.

Mechanisms. Each regime is coded before reform and now on who pays the assessor, who selects it, what it sees, what the public reads, and who oversees the assessor.

Scores. Dataset A values are weighted under four presets (lab procurement, regulator selection, public trust, equal) and reported with the distribution per dimension and per organization type.

Everything above is computed by `python -m bench industries`, `python -m bench timeline`, and `python -m bench scores`.

## 5. Results

### 5.1 Where frontier AI sits (Figure 1)

Frontier AI reached S1 in 2022 (pre-release testing of GPT-4 by ARC Evals), S2 in 2025 (the FrontierMath funding disclosure) with a second, more serious trigger in 2026 (the OpenAI agent swarm incident and the first on-site third-party incident investigation), S3 in 2026 (Illinois SB 315, audits from 2028), S4 in 2025 (the EU Code of Practice and AEF-1), S6 in 2026 (SB 315's financial-interest rule), and S7 in 2025 (the Code's access floor, followed by the 2026 embedded-evaluator pledges). It has not reached S5: there is no body that accredits, inspects, or registers frontier AI evaluators.

Four years from voluntary assurance to mandate is the shortest interval in the dataset. The comparable intervals are seven years for automobile crash safety, nine for crypto (a mandate on safeguarding rather than on assurance), nineteen for sustainability assurance, forty-two for boilers, and seventy-eight for electrical product safety. Six of seven stages in four years is faster than any regime in the set.

The empty cell is the informative one. Eight of the fifteen non-AI regimes built an oversight layer for their assessors (a registry, an accreditation program, or an inspector of inspectors): financial audit (PCAOB, 2002), ship classification (IACS, 1968), boilers (National Board, 1919), product safety (OSHA NRTLs, 1988), pharmaceuticals (Good Laboratory Practice inspection, 1978), credit ratings (NRSRO, 1975), food safety (FSMA accredited certifiers, 2011), and cybersecurity (Common Criteria labs, 1999). AI has standards without anyone checking who applies them.

### 5.2 Rules follow triggers fast; drift before triggers is slow

Across twenty trigger events in the fifteen non-AI regimes, the lag from the trigger to the next rule of any kind has a median of two years and a maximum of ten. Seven of twenty are one year. The interval from a regime's first milestone to its first independence rule, where one exists, is 5 years (platform audits), 17 (nuclear), 86 (pharmaceuticals), 94 (aviation), 101 (credit ratings), 158 (financial audit), and 249 (ship classification).

The two clocks run at different speeds. Once a failure is public, regimes act within an election cycle. Before that, they drift for decades. Frontier AI's first triggers arrived in 2025 and 2026. By the pattern in Dataset B, the rules that shape its assurance layer are being written now.

### 5.3 The assessed party keeps paying

In fourteen of the fifteen non-AI regimes, the party being assessed pays the assessor after reform, either directly (audit fees, certification fees, issuer fees, classification fees, user fees) or through delegation to its own staff. Independence, where it arrived, came from auxiliary mechanisms: standards (1939 auditing procedures after McKesson & Robbins), inspection of assessors (PCAOB, GLP), rotation (Sarbanes-Oxley partner rotation; EU firm rotation; DSA auditor rotation), separation of assessment from consulting (Sarbanes-Oxley), liability exposure (Dodd-Frank for rating agencies), and public comparative ratings (NCAP).

Two regimes removed the payer conflict. Boiler inspection routed inspection through insurers from 1866: the inspector is paid by the party that loses money if the boiler explodes. Automobile crash testing at IIHS is funded by insurers and published as ratings from 1995; manufacturers do not pay and cannot opt out. Both models have live AI analogues in proposal form (insurance-backed certification, insurer- or user-funded public ratings), and neither has an AI implementation yet.

### 5.4 Delegation is the recurring failure mode

Five regimes in Dataset B show the assessed party absorbing the assessment function: consulting revenue overtaking audit fees at accounting firms before Enron; sponsors running the trials regulators review; issuer-pays ratings; Organization Designation Authorization letting manufacturers' employees certify aircraft; and frontier AI, where developers run their own safety evaluations and select, scope, and pay the external testers cited in their system cards. In three of the four historical cases a public failure was followed by a reform that reclaimed part of the delegated function (Sarbanes-Oxley 2002, Good Laboratory Practice 1978, the 2020 aircraft certification reforms). Frontier AI's 2026 commitments move in the same direction, from lab-scoped engagements toward embedded evaluators with publication rights, but as pledges rather than rules.

### 5.5 The AI evaluator population in 2026

Under the lab-procurement preset the scores run from 90 (METR) to 35 (Microsoft AI Red Team). Nonprofits average 3.0 or above on funding, governance, scope, publication, methods, and product conflicts, and 2.4 on access. Government bodies score 4 on funding and 1.7 on publication: they see the most and publish the least. Venture-backed evaluators average 1.3 on funding, 1.2 on governance, 1.2 on product conflicts, and 2.0 on access. The two Big Tech units score 0 on funding and governance.

Across all 26, mean scores by dimension are scope control 2.9, method transparency 2.9, product conflicts 2.8, publication rights 2.6, governance 2.5, funding 2.4, personnel 2.4, and access 2.4. Half the population (12 of 26) scores 2 or below on funding, which at anchor 2 means the lab pays per engagement. Hypothesis H4 predicted strength on access and methods and weakness on funding and personnel; the data support the funding and personnel half and reject the access half. Access is a weak dimension for most of the population, which is consistent with the September 2026 pledges targeting exactly that gap.

Signals split 132 for and 95 against. The most frequent against-signal across organizations is that the developer pays for the evaluation of its own model. The most frequent for-signal is publication of a method or a tool.

### 5.6 Paths: which history AI's path resembles

Written as sequences, the regimes do not share a ladder. Financial audit reads mandate, rollback, voluntary, mandate, access, trigger, standards, delegation, trigger, oversight, independence. Nuclear opens with a mandate and adds voluntary peer review twenty years later. Dietary supplements opens with a rollback. Frontier AI's sequence so far is voluntary, delegation, voluntary, trigger, standards, access, trigger, mandate, independence, access.

The opening most similar to AI's is credit ratings (similarity 0.50): voluntary assurance, then the assessed party becomes the client, then a trigger, then oversight without independence, then a second trigger, then independence rules. The next nearest are financial audit and crash safety (0.36 and 0.40) and crypto proof of reserves (0.40), which shares AI's voluntary-trigger opening and then collapsed. The comparison is over openings only and the sequences are short, so this is a hypothesis generator, not a result; it says the nearest analogue is the regime where regulators licensed a payer-conflicted assessor and then met 2008.

### 5.7 Fast responses are mostly weak responses

Pairing each trigger with the next rule and its strength changes the reading of the lag result. Sixteen of the twenty-four non-AI triggers were answered within three years, with a mean instrument strength of 2.9 on the 1 to 4 scale. Two of the sixteen were structural: the PCAOB after Enron, and inspection of testing labs under Good Laboratory Practice after the Industrial Bio-Test fraud. Two triggers were followed by nothing in the dataset (the Target breach; the 2025 analysis of hiring-tool audits). Frontier AI's two triggers have so far been answered by instruments of strength 2 and 1: the EU access floor and the embedded-evaluator pledges.

### 5.8 Money by distance from a lab

A row-level ledger behind the funding and personnel dimensions changes what "no lab money" means. Of 28 evaluators, 17 have at least one traced inflow from a frontier lab or from a party with a direct tie to one (an investor, board observer, employee, founder, or contractor). Eight have Coefficient Giving inflows; Coefficient's principal is an Anthropic Series A investor by his own account. Twenty-eight of 68 inflow rows have been re-derived from the cited source; the rest are imported leads, and the ledger says something about who stands behind 39 of 52 funding sources. The import is pinned to a commit of the third-party ledger and to the post through which it was found. The two evaluators with the most complete self-disclosure, Transluce and AVERI, are also the ones whose disclosures move their own scores down, which is what an honest disclosure regime should look like.

### 5.9 Mechanisms: the AI row

On the five mechanism questions, frontier AI today reads: the assessed party pays, the assessed party selects, access is shallow, the public reads summaries, and nobody oversees the assessors. Fourteen of the fifteen non-AI regimes have an oversight cell filled. The one other regime with AI's exact five-cell pattern is dietary supplements. The two regimes that moved payment and selection to a party with opposing exposure, boiler inspection and crash testing, are also the two where the assessed party never regained control of scope.

## 6. Discussion

What the history predicts. If frontier AI follows the pattern in Dataset B, the two or three years after its first public failures are when its assurance regime takes shape, and the shape will be set by rules written in response to those failures rather than by the voluntary arrangements that preceded them. The instruments in motion now (the EU Code, Illinois SB 315, the embedded-evaluator pledges) fit the pattern in timing. They do not yet fill the S5 cell. Every mature regime in the dataset that kept a payer-conflicted model built an inspector of inspectors; AI has none, and the EU Code's "adequately qualified" and Illinois's "demonstrated competence" are the words regimes use before they build one.

Who pays the referee. The historical answer is that the referee is paid by the team, and the league makes that tolerable by licensing referees, watching them, rotating them, and letting the public see the score. The exceptions are the regimes where a party with opposing financial exposure pays. In AI, the philanthropic model (METR) works at small scale and does not scale to embedded teams at every developer; the lab-fee model (Apollo, SecureBio, Irregular, Gray Swan) scales and carries the conflict; the government model (UK AISI, CAISI, EU AI Office) has depth but publishes little and is exposed to political redirection. The insurer-routed and public-ratings models are untried.

Three design options the data point to, in increasing order of departure from current practice: (1) accredited lab-paid evaluation with a registry and inspection of evaluators, on the PCAOB and NRTL pattern; (2) mandatory publication of evaluator operating conditions per engagement, on the trial-registration pattern, which AEF-1 already specifies and no regulator yet requires; (3) an evaluator funded by parties exposed to model failure, on the boiler-insurance or IIHS pattern.

## 7. Limitations

Triggers were partly selected with hindsight in v0; v0.2 adds an outcome-independent criterion but has not yet enumerated qualifying incidents that were followed by nothing, so the lag results remain biased toward responsiveness. Path similarity is computed over short sequences and openings only. Mechanism coding is single-coder and categorical.

Dataset B uses year granularity and secondary sources in v0; ordering within a year is lost (Illinois SB 315 preceded the July 2026 incident). Regime selection is judgmental; the four added regimes reduce selection on success but do not remove it. Coding milestone kinds involves judgment at the margins (PDUFA is coded as a payer shift toward the assessed party rather than an independence reform). Dataset A scores public records only; private contract terms could raise or lower any score, and evaluators can move their scores by publishing their terms. Version 0 is single-coder. The AI section describes a moving target and is pinned to a date and a commit.

The authors have relationships in the AI investment and research ecosystem, disclosed in the repository, which is the same disclosure this paper asks of evaluators.

## 8. Conclusion

Frontier AI has compressed into four years a passage other industries took decades to make, and it has done so by adopting standards, mandates, and access rules while leaving the evaluators unwatched. The history says failures come first and rules follow within a few years; AI has had its failures. The choice now is which of the three historical answers to the payer problem the field adopts, and whether it builds the oversight layer before or after the next incident. The datasets are open and rebuild from their evidence; we invite evaluators to change their scores by publishing their terms.

## Figures and tables

- Figure 1. Stage ladder: `paper/figures/stage-ladder.svg` (generated).
- Figure 2. Path strips with similarity to AI: `paper/figures/paths.svg`.
- Figure 3. Trigger-to-rule lag against instrument strength: `paper/figures/responses.svg`.
- Figure 4. Mechanism matrix: `paper/figures/mechanisms.svg`.
- Table 1. Trigger-to-rule lags: `python -m bench industries`.
- Table 2. Dataset A scorecard under four presets: `python -m bench scores <preset>`.
- Table 3. Per-dimension means by organization type: computed in `paper/NOTES.md`.

## References

See `paper/related-work.md`. Dataset A sources are in `data/sources/`; Dataset B sources are inline in `data/industries/`.
