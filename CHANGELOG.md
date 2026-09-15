# Evaluator Bench v0 changelog

v0, 15 Sep 2026. Initial public release: an evidence-linked, event-sourced
directory of third-party evaluators for frontier AI, built on ActiveGraph.
Correction window open through 29 Sep 2026.

## Contents

- 26 ranked evaluators + a 2-entry watchlist (`big4`, `hfoai` — expected
  entrants, scored on the same rubric but excluded from rankings and
  homepage statistics).
- 122 sources, 314 signals, 224 assessments; 44 signals carry exact quotes.
- 84 ledger transfer rows, of which 63 are evidential; 49 confirmed.
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
- **External validation is scarce — that is a finding, not a bug.** Of the
  unique sources cited by ranked evaluators, 54% are tier-3 self-published,
  9% are tier-1, and 14% of ranked signals carry exact quotes. The site's
  evidence section derives these figures from the built data.
- **Independence ≠ competence.** Access records what labs granted, not
  capability or entitlement; scores are ordinal projections, not procurement
  truth.
- **Fail-closed verifier.** JSONSchema is a hard dependency; duplicate ids,
  bad dates, and post-clock records are errors, not warnings.
- **Single coder, LLM-assisted.** Built by one curator with Claude (Anthropic);
  curator disclosure completed 2026-09-15 in DISCLOSURE.md (small public
  holdings in Google and Meta, private SpaceX holding with xAI exposure;
  shared-funders field is best-effort "none known").

## Late fixes before v0 (15 Sep 2026, evening)

- Ledger: T13 (ARC to METR $4,553,935) moved from unverifiable to unaudited on two 990 extracts; T15/T16 re-pointed from the Nonprofit Explorer home page to the Founders Pledge e-file XML and the SVCF filer page; T22 (OpenAI Foundation to SecureBio $17.2M) confirmed on SecureBio's own post; T07 (Coefficient to Epoch) confirmed against Epoch's own list, which sums to $25,113,611 including a July 2026 grant made after the snapshot ($24,513,611 without it, the row's figure; the earlier differs flag rested on a mis-sum); T41/T48/T60 relabeled as consortium lot totals; Bass repository path corrected to the master branch; dead Microsoft red-team URL replaced.
- New: CAISI early-access agreements with five labs (CSA note); Epoch discloses investing in semiconductor and AI stocks; SecureBio's no-constraints statement.
- Transfer rows carry a `class`; the hop-0 count is reported by kind: 8 of 26 with lab cash or in-kind, 2 ownership, 2 partnership-only.
- C14: extremes need live evidence. Seven assessments (EquiStamp G and X, Nemesys G, S and R, Microsoft F and G) are held at supportable values and marked evidence-limited; scores moved by 1 to 6 points.
- Dockets page reads a committed validation record bound to the proposal digest.

## Known limits (v0)

- Current source status: 109 of 122 source records are confirmed, 10 are
  unaudited, 1 is imported, and 2 are unverifiable. Current transfer status:
  49 confirmed, 14 unaudited, 5 differing, 14 unverifiable, and 2 superseded.
  The raw audit batches remain in `paper/audits/`; they are historical records,
  not the current projection.
- Exposure is computed only from evidential rows: 12 of 26 ranked evaluators
  have a direct lab tie and 17 have a lab or lab-tied inflow. Of the direct
  ties, 8 are lab cash or in-kind for evaluation work, 2 are ownership, and 2
  are no-fee partnerships or memberships. The latter two categories are not
  reported as evaluator funding.
- Dataset A is single-coded; Dataset B milestone years are coded from
  secondary sources and need primary-source verification.
- The trigger-lag and path-similarity results are hindsight-selected and
  exploratory, not causal.
