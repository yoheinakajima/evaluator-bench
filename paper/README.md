# Paper concept: Who pays the referee?

Working title: **Who Pays the Referee? Measuring Third-Party Evaluator Independence in Frontier AI Against the History of Assurance Regimes**

Status: v0 draft in `draft.md`, 15 Sep 2026. Datasets seeded in this repo; Dataset B needs primary-source verification; Dataset A is single-coded and open to public correction.

## One paragraph

Every mature high-stakes industry ended up with a third-party assurance layer, and nearly every one of those layers started with the assessed party paying the assessor. Financial audit, credit ratings, product safety marks, drug testing labs, aircraft certification, ship classification, and cybersecurity assessment all began as voluntary or payer-conflicted arrangements and acquired independence rules later, usually within a few years of a public failure. Frontier AI evaluation is at the voluntary, payer-conflicted, pre-accreditation stage, and it had its first candidate trigger events in 2025 and 2026. This paper measures where the AI evaluator population sits on the independence dimensions those other regimes eventually regulated, using an open, evidence-linked dataset of 26 ranked evaluators (plus 2 expected entrants on a watchlist), and places that measurement on a coded lifecycle of sixteen assurance regimes. The contribution is the two datasets and the comparison, not another framework.

## Novelty check

The qualitative "AI should learn from other industries' auditors" argument is well covered. The paper cannot rest on it. What exists:

| Prior work | What it does | What it does not do |
|---|---|---|
| Raji, Xu, Honigsberg, Ho, *Outsider Oversight* (AIES 2022) | Designs a third-party audit ecosystem for AI by analogy to financial audit, credit ratings, and other regimes; proposes accreditation, standards, access | No measurement of actual evaluators; pre-frontier; no dated lifecycle data |
| Costanza-Chock, Raji, Buolamwini, *Who Audits the Auditors?* (FAccT 2022) | Field scan of 189 algorithmic-audit organizations; survey of 152 practitioners; recommendations | Bias and fairness audits, not frontier safety; self-report survey rather than evidence coding; no independence scoring |
| Anderljung et al., *Towards Publicly Accountable Frontier LLMs* (2023) | ASPIRE framework for external scrutiny: access, searching attitude, proportionality, independence, resources, expertise | Normative; no scoring of organizations |
| Casper et al., *Black-Box Access is Insufficient* (2024) | Argues for deeper access for audits | Access only; no funding, governance, or personnel dimensions |
| Manheim et al., *The necessity of AI audit standards boards* (AI & Society 2025) | Proposes a standards board, citing aviation, nuclear, accounting, pharma | Qualitative precedent argument; no dataset |
| Anderson-Samways, *AI-relevant regulatory precedents* (IAPS 2024) | Systematic search of US federal agency precedents | Regulatory instruments, not assurance-provider independence; no lifecycle timing |
| Homewood et al., *Third-party compliance reviews for frontier AI safety frameworks* (2025) | Design of compliance reviews | No measurement of reviewers |
| Brundage et al., *Frontier AI Auditing* (arXiv 2601.11699, Jan 2026) | Vision and AI Assurance Levels; cites FAA, UL, melamine, HackerOne precedents | Framework for what audits should be; does not score the current evaluator population; precedents are illustrative, not coded |
| Charnock et al., *Expanding External Access* (arXiv 2601.11916, Jan 2026) | Taxonomy of access levels tied to the EU Code | Access only |
| AI Evaluator Forum, AEF-1 (Dec 2025) | Minimum operating conditions for independent evaluation | A standard, not a measurement of who meets it |
| Groves et al., *Auditing the Audits* (FAccT 2025) | Empirical analysis of 116 NYC Local Law 144 bias audits | Audits of hiring tools, not frontier evaluators; no independence dimensions |
| SaferAI framework ratings; FLI AI Safety Index | Score the labs' frameworks | Score labs, not evaluators |

The gap is empirical and it is two-sided. Nobody has coded the frontier evaluator population against independence criteria with sourced evidence, and nobody has coded the cross-industry history of assurance regimes as dated lifecycle events that can be compared. The paper does both and reports what the comparison says.

Claims the paper should make:

1. An open, evidence-linked scorecard of frontier AI evaluators on eight independence dimensions, rebuilt from an append-only log so every number traces to a source and a date. (Dataset A: this repo, 26 ranked evaluators plus a 2-entry watchlist, 289 signals citing 114 public sources as of v0.4.)
2. A coded lifecycle dataset of sixteen assurance regimes (fifteen non-AI industries plus frontier AI): first voluntary assurance, trigger incidents, mandates, independence rules, accreditation, payer reforms, publication rules. (Dataset B: `data/industries/`.)
3. Three findings the seed already suggests and the full dataset should test:
   - Rules follow triggers fast; drift before the first trigger is slow. In the seed, the median lag from a trigger incident to the next rule is about two years, while the interval from first voluntary assurance to the first independence rule runs from two decades to two centuries.
   - Who pays is almost never changed. Regimes made payer-conflicted assurance tolerable with standards, inspection of assurers, rotation, liability, and public ratings. The exceptions that removed the conflict routed payment through insurers (boilers) or funded assessors from a party with opposite incentives (auto crash ratings).
   - Delegation to the assessed party is the recurring failure mode (ODA in aviation, IBT in drug testing, issuer-paid ratings), and the AI field's default of lab-paid, lab-scoped evaluation is the same structure.
4. A placement: on the eight dimensions, the 2026 AI evaluator population is strong on scope control and method transparency and weak on funding, governance, and personnel.

## Hypotheses

- H1 (lag): Across regimes, the time from a public failure to the next independence rule is short (under five years) and the time from first voluntary assurance to the first independence rule is long (over twenty years).
- H2 (payer persistence): In most regimes the party being assessed still pays the assessor after reform; independence is achieved through auxiliary mechanisms rather than payer change.
- H3 (access precedes independence): Access expansions (inspection rights, on-site presence) tend to arrive before funding or personnel rules.
- H4 (AI placement): The 2026 AI evaluator distribution scores higher on access and method transparency than on funding and personnel, and the highest-scoring evaluators are the ones with philanthropic or public funding.

Each hypothesis is testable from the two datasets and each can fail.

## Method

Dataset A. Eight dimensions with 0 to 4 anchors (see `data/dimensions.json`). Each assessment cites signals; each signal cites sources with retrieval dates. Two coders, with disagreements recorded in the rationale field. Inter-rater agreement reported. Sensitivity analysis over the preset weights.

Dataset B. For each regime, milestones coded by kind: voluntary_assurance, trigger, mandate, standards, independence_rule, accreditation, payer_reform, publication_rule, delegation, delegation_reform, access_expansion, rollback. Year granularity. Each milestone cites a source; the seed uses secondary sources and each entry is to be verified against a primary source before publication. Also coded per regime: payer model, access model, publication model.

Analysis. `python -m bench industries` produces the lifecycle table. Figure 1: regimes on a timeline normalized to first voluntary assurance, with triggers and rules marked. Figure 2: the AI evaluator population as a distribution on each dimension, with the pre-reform profiles of financial audit and drug testing labs coded on the same dimensions for comparison. Table: payer model before and after reform, per regime.

## Risks and limits

- Year granularity hides ordering within a year (Illinois SB 315 preceded the July 2026 incident; the seed table shows both as 2026).
- Selection of regimes is not random. Report the selection rule and include regimes where independence reform did not happen or was reversed (the 1856 UK rollback is one).
- Dataset A scores public records. Private contract terms could raise or lower any score. The paper should say so and invite evaluators to publish their terms, which is itself a finding if they do not.
- Coder conflict of interest: the repo's curators have relationships in the AI ecosystem. Disclose in the paper the same way the rubric asks evaluators to.
- The AI section will date quickly. Pin the paper to a commit hash and a date, and keep the repo as the living version.

## Venue and timeline

- arXiv cs.CY first, then FAccT 2027 or AIES 2027. The datasets are the artifact; the paper is the reading.
- Oct 2026: verify Dataset B milestones against primary sources; add three regimes with no or reversed reform for balance; fold accepted public corrections into Dataset A.
- Nov 2026: analysis notebook, figures, draft.
- Dec 2026: circulate to two evaluator organizations and one regulator contact for factual review, with corrections logged as signals.

## Related files

- `related-work.md`: fuller annotated bibliography.
- `data/industries/`: Dataset B seed.
- `data/`: Dataset A.
