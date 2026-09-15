# Evaluator Bench v0 changelog

v0, 15 Sep 2026. Initial public release: an evidence-linked, event-sourced
directory of third-party evaluators for frontier AI, built on ActiveGraph.
Correction window open through 29 Sep 2026.

## Contents

- 26 ranked evaluators + a 2-entry watchlist (`big4`, `hfoai` — expected
  entrants, scored on the same rubric but excluded from rankings and
  homepage statistics).
- 125 sources, 308 signals, 224 assessments; 39 signals carry exact quotes.
- 84 ledger transfer rows, of which 74 are evidential; 26 confirmed.
- Eight independence dimensions: Funding, Governance, Personnel, Access depth
  (lab-granted), Scope control, Publication rights, Method transparency,
  Role incompatibility.
- Scores are gated ordinal projections (0–100): any dimension at 0 caps the
  total at 40, any at 1 caps at 60. One rounding rule everywhere — halves
  round up. The lab-procurement weighting is the preregistered confirmatory
  preset; the other presets are sensitivity checks.
- Event-sourced build: `graph/events.jsonl` is the append-only log;
  `dist/` is a deterministic projection. The build is byte-identical on
  re-run under the frozen evidence clock (2026-09-15).

## Design decisions

- **No self-certification.** Bench-authored dockets are drafts, not evidence,
  and are never citable by signals. `bench certificate issue` refuses
  manual/self-reviewed issuance; the verifier fails closed on any
  `docket`-type source claiming `confirmed` without an independent, signed
  certificate from review at epistemedia.org by someone other than the drafter.
- **Money measures never cross.** The ledger distinguishes grants, rounds,
  valuations, and revenue; round totals and component detail rows are labeled
  and never summed. Dollar sums include only confirmed and unaudited USD rows;
  imported figures are shown but never summed; euro amounts are shown
  unconverted; contradicted, superseded, and unverifiable rows are excluded
  from every figure and labeled on the site.
- **Tier-gated top scores.** A 4 on Funding, Governance, or Personnel requires
  tier-1 (filing or index) evidence on a cited signal; the verifier enforces
  this (C10).
- **External validation is scarce — that is a finding, not a bug.** 54% of
  sources cited by the ranked population are self-published, 9% are tier-1,
  12% of ranked signals carry exact quotes. The site's evidence section states
  this plainly.
- **Independence ≠ competence.** Access records what labs granted, not
  capability or entitlement; scores are ordinal projections, not procurement
  truth.
- **Fail-closed verifier.** JSONSchema is a hard dependency; duplicate ids,
  bad dates, and post-clock records are errors, not warnings.
- **Single coder, LLM-assisted.** Built by one curator with Claude (Anthropic);
  curator disclosure completed 2026-09-15 in DISCLOSURE.md (small public
  holdings in Google and Meta, private SpaceX holding with xAI exposure;
  shared-funders field is best-effort "none known").

## Known limits (v0)

- Dataset A is single-coded; Dataset B milestone years are coded from
  secondary sources and need primary-source verification.
- The trigger-lag and path-similarity results are hindsight-selected and
  exploratory, not causal.
- 40 imported ledger rows are not yet re-derived from the cited source.
