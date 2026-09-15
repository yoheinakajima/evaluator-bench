# Evaluator Bench changelog

## 15 Sep 2026, later: scope, bands, the hidden number, evaluation credits, checked-and-not-found

Recorded as decisions D-001 to D-005 in `DECISIONS.md`.

- **Scope** is third-party evaluation of frontier models for safety-relevant properties (RULES 11). Epoch AI and the Princeton Holistic Agent Leaderboard are retained with `status: out-of-scope`, unranked and excluded from every statistic; the seven capability leaderboards in the population check are marked out by scope. Ranked population: 24.
- **Bands** are set by the conflict dimensions only (funding, governance, personnel, role incompatibility, scope, publication). Access and methods still count in the number but never set a band; AVERI, MLCommons, and the organizations whose only 1 was on access move bands accordingly.
- **The number is hidden** on the directory until the reader chooses weights and presses "Score with these weights"; the band, the coverage, the weakest dimension, and the eight values show by default, and the default order is band first, then the weakest dimension.
- **Evaluation credits** consumed in testing a lab's own model are not lab money (RULES F.2): they never bound funding, never enter the hop buckets, and are not a direct lab tie. They stay in the ledger and on the entity page. METR's only hop-0 row was such a row.
- **Checked and not found**: every bounded negative now names the question it answers and what prompted it, and renders that way on cards; the term stays in the glossary.
- **Contested-claim drafts** leave the navigation; one sentence on the Contribute page says what they are.
- **Disclosure** names the collaboration: Claude drafted; Codex, Grok, Gemini, and Muse reviewed and criticized; all four developers are labs in the ledger; and answers directly the concern about an Anthropic model ranking the evaluator Anthropic named first.
- Re-derivation pass on the open questions that public records can settle is under way (`leads/rederive.json`); document requests to organizations and people go with the reply packets.
- Numbers after these decisions (standard policy, lab preset, 24 ranked): 13 clear, 8 conditional, 3 disqualifying; direct lab ties 10 of 24 (6 cash, 2 ownership, 2 partnership), lab or lab-tied 15 of 24; 10 conflicts resolved by rule; 10 assessments held; gates: 21 binding signals without a span, 15 extremes awaiting a second coder, 51 reply packets (24 organizations, 27 people), none sent.

## v0.1 candidate, 15 Sep 2026 (evening): values derived, evidence policies, bands, gates

Follows `paper/PLAN-v0.1.md`, written the same day against the v0 preview and two independent reviews. Nothing in the data was deleted; every v0 signal is still here with a bound and a rule attached.

### What changed in how a value is made

- **Bounds and rules.** Every signal now declares the anchor it supports (`bound`: a cap for an against-signal, a floor for a for-signal) and the `RULES.md` rule code that says so. The stored value is the derivation: the smallest cap or, with no cap, the largest floor. The verifier fails on a stored value that disagrees with its derivation (C22, C23) or an `evidence_limited` flag that disagrees with the computed held state (C24). The 170 boilerplate rationales ("Anchor N on X given the cited signals") are gone; the derivation text is generated on every card and the curator's prose, where it exists, sits beside it.
- **RULES.md.** Written tie-breaks per dimension, applied to every organization the same way: a 20% stake is ownership (F.1, G.6), in-kind lab compute counts only above a materiality threshold (F.2), lab fees cap funding at 2 unless a published 10% cap applies (F.3), pooled and lab-investor-linked philanthropy caps at 3 (F.6), legal form alone floors governance at 2 (G.1), "no lab roles found" floors personnel at 2 (P.6), a 4 on scope needs incident or sign-off rights (S.5), a 4 on publication needs no lab pre-review plus a published adverse finding (R.5), a 4 on methods needs a third-party re-run or factsheets (M.1), paid consultation for a lab caps role incompatibility at 2 (X.3). The anchor texts for funding 0 and role incompatibility 1 were amended to match.
- **Extremes need spans and second sources.** A 0 is effective only with a quoted span from a confirmed source (C15, C17). A 4 is effective only with a span and a tier-1 or tier-2 source or two independent sources with one not the evaluator's own (C15, C16). Bounds that fail are held at 1 or 3 and the card says which rule held them. In v0, 32 assessments sat at 0 or 4; 29 rested on a single signal, 28 without a span, 24 only on the organization's own statements.
- **Evidence policies.** The reader chooses what counts: leads included, standard (at least one confirmed source; the default), against interest (an evaluator's own statements count only against it), verified spans, primary only. A dimension with no admissible signal renders as a dash and is excluded from the score; coverage is shown beside every number. Self-published sources now name whose statement they are (`self_of`), so a lab's own statement about an evaluator is not discounted as that evaluator's self-report.
- **Bands replace numeric caps.** Any evidenced 0 is a disqualifying floor, any 1 a conditional floor, otherwise clear; the band sorts first and the number ranks within it. The 40 and 60 caps are gone.
- **Roles are derived** (RULES 10) from type and the role-incompatibility value; list placement (referees, government, commercial and first-party) follows. Andon Labs and EquiStamp move from referee to vendor under the rule.
- **The hypothetical Big Four composite is no longer scored.** Its six SB 315 sources, cited by nothing else, were removed; the discussion of the large assurance firms moved to the paper.
- **Population criteria and a checked candidate list** (`data/exclusions.json`, RULES 11): 45 candidates, 21 in scope for the next batch, including several evaluators named in current system cards.
- **Weights carry derivations**; "pre-registered" is dropped because no timestamped registration exists outside the repository.

### Evidence work

- A bound, a rule, and where the page could be fetched a quoted span, on every signal; second sources sought for every floor of 4; mechanism tags on access and publication; a dissent (one notch lower, one notch higher) on every card; open questions about named people rewritten as document requests (RULES 12).
- Corpus-wide quote audit: 36 of 43 existing spans found verbatim; 6 replaced with spans that are on the page today (Apollo curly quotes; AVERI recusal wording; FAR.AI, METR, Palisade after Open Philanthropy pages moved to coefficientgiving.org); one Forbes page behind a bot wall, archived. The SecureBio "OpenAI covered the GPT-5.5 evaluation" quote was not on the cited page; the signal is re-scoped to the GPT-6 Astra and GPT-5.6 Sol reports, which carry the sentence, with SecureBio's principles page as the CI-checkable source.
- Primary sources for the September 2026 pledges replace the aggregators: Anthropic's commitment (essay and announcement) covers access, METR by name, and publication without editorial control; OpenAI's chief executive's statement covers access only. The paper's opening paragraph is corrected accordingly.
- Press sources are split into primary and aggregator; MarkTechPost and a law-firm alert were recoded from self to press.

### Site

- Homepage: byline and holdings beside the scores; competence chip; evidence-policy selector; three lists by derived role with a one-list toggle; band and coverage on every row; sort by weakest dimension; a four-paragraph guide; the regimes work moved to its own page with the Dataset B caveat on the figure. The essay sections moved to topic pages: rubric and rules, cases, method, money, population.
- Cards: the derivation and the binding signal on every dimension, values under each policy, held and conflict flags, mechanism tags, dissent, and "what would move the score, and by how much" computed from the weights.
- Status page: the gates for a citable tag, what counts under each policy, the right-of-reply log (organizations and named people), and the second-coder log. Every statistic covers the ranked population only.
- Fixed: HTTPS now enforced on the custom domain; the independence bar rendered at zero height; no favicon, Open Graph, or canonical tags; phone navigation hid nine of eleven links; figures scrolled sideways with no cue.

### Process

- `bench gates` lists what stands between the preview and a citable tag; `bench release --stage published` refuses while any gate fails.
- `bench outreach --all` writes right-of-reply packets for every ranked organization and every named person; `data/outreach-log.csv` records contact; sending is a human action.
- `bench review --all` re-fetches every quoted source; `bench scores --policy --by-type` prints band-first tables.
- Disclosure: shared funders are marked "not yet checked" rather than "none known"; the check is scheduled before the freeze. One coder; a second coder on every extreme is a gate.

### Numbers at this build

- 27 organizations (26 ranked, 1 watchlist); 357 signals (309 with a quoted span); 194 sources; 216 assessments, 1 unevidenced even with leads included (Redwood personnel).
- Ranked population, standard policy, lab preset: 8 clear, 12 conditional, 6 disqualifying; METR 79 to Scale 36. Unevidenced assessments under standard 6 of 208; against interest 52; verified spans 27; primary only 187.
- 94 values moved when the rules were applied to the v0 record; 12 floor-cap conflicts resolved by a named rule; 8 assessments held at a supportable anchor by the span or second-source tests.
- Gates: 23 binding signals still without a span; 16 extremes awaiting a second coder; 53 reply packets generated, none sent.

### Known limits (v0.1 candidate)

- Single coder with AI assistance; the rules are the curator's rules. Second coder pending.
- Under the primary-only policy almost nothing is evidenced; that is the finding, shown as a table.
- Dataset B unchanged: secondary sources, year granularity, hindsight-selected triggers.
- Paper section 5.5 and the abstract's third result are regenerated from the build at the pinned commit.

## v0, 15 Sep 2026 (initial release)

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
