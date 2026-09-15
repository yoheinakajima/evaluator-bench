# Evaluator Bench v1.0 repair changelog

Owner-directed repair pass, 15 Sep 2026. Implements the adversarial review
(`review/report.md` in the author's working files) plus two external feedback
reports. Deviation from `AGENTS.md` (no deletions, no verifier/build changes)
is explicitly authorized by the project owner for this pass and recorded here.

## Self-certification loop: removed

- Deleted `data/certificates/metr-lab-money.json` (self-issued "manual v0").
- Deleted `data/sources/docket-metr-lab-money.json` (`confirmed` docket source).
- `metr.18` cites only its three primary sources.
- Removed the "Epistemedia reviewed (manual v0)" badge from `site/template.html` and `bench/site.py`.
- `docket` source type re-tiered to "docket draft (not evidence)".
- `paper/EPISTEMEDIA.md` and `paper/CERTIFICATION.md` rewritten: docket drafts are not citable evidence; only an independent review at epistemedia.org by someone other than the drafter can ever produce a citable source, and then only as a secondary summary, never the strongest tier.
- `bench certificate issue` refuses manual/self-reviewed issuance.
- `bench verify` now fails closed: a `docket`-type source with `audit_status: confirmed` and no independent signed certificate is a verification error.

## Ledger

- New columns on `transfers.csv`: `currency` (USD/EUR), `superseded_by`, `component_of`, `round_total`.
- T10 (Palisade $3.8M, contradicted) superseded by T75 ($2.12M research-pass figure); T81 (duplicate $40M round) superseded by T21.
- T72/T73/T74 marked `component_of` T03/T04/T06: detail rows, never summed.
- T42/T48/T60: `currency=EUR`; euro amounts no longer sit silently in the USD column and are excluded from USD sums.
- T54 (Nvidia→hfoai $12.9B acquisition rumor) and T02 (grant page 404) moved to `unverifiable` and quarantined.
- `exposure()` now excludes `differs`/`unverifiable`/superseded rows from buckets; dollar sums include only confirmed + unaudited USD rows (imported figures are never summed — they were someone else's homework); components never summed; EUR shown unconverted.
- `distances()` influence edges use evidential rows only.
- `money()` on the site labels round totals, EUR, components, superseded and quarantined rows explicitly.
- Headline stat corrected: **17** of 28 (not 18) have a hop0/hop1 inflow — hfoai's only lab-tied inflow was the quarantined Nvidia rumor.

## Verifier / scoring

- `bench verify` is fail-closed: JSONSchema is a hard dependency (no silent skip);
  duplicate source/evaluator/signal ids are errors.
- New C10 enforces the PROCESS tier rule the old verifier ignored: a 4 on F/G/P
  needs a tier-1 (filing/index) source on a cited signal. Six violations found;
  fixed by downgrading (see Evidence).
- New C11: dates must be YYYY, YYYY-MM, or YYYY-MM-DD, and no record may be dated
  after the frozen evidence clock (`EVIDENCE_CLOCK = "2026-09-15"` in
  `bench/load.py`; the 2026-09-15 research-pass dates are genuine curation dates,
  so the clock was bumped from 2026-09-14 rather than falsifying them).
- New C12: every preset's weights must cover exactly the 8 dimensions and sum to 100.
- `bench score` raises on missing dimensions instead of silently scoring a zero;
  new `gated` option applies independence floors (any 0 caps at 40, any 1 at 60).
- The verifier docstring no longer promises "a PR that changes a score without
  changing a signal fails" — it states what is actually checked.
- One rounding rule everywhere: halves round up (Python `Decimal` ROUND_HALF_UP
  matching JS `Math.round`).

## Evidence

- Six PROCESS tier-rule violations fixed (C10 now enforces what the old verifier
  ignored): euaio.G, metr.G, hal.G, averi.G, hal.P, ukaisi.G downgraded 4 → 3 with
  rationales citing the anchor clause actually in evidence. No 4 now rests on a
  self page or press alone.
- Cherry-picked citations repaired: transluce.P now cites transluce.12 (against)
  alongside .04 and drops 3 → 2; palisade.P cites palisade.10 (against) alongside
  .07; irregular.F cites irregular.11 (the $6.8M old-name grant, against) alongside
  the exculpatory .12 — the name-search miss does not rebut the old-name row.
- Four quote/claim mismatches narrowed to what the quotes support (caisi.11,
  ukaisi.12, farai.14, metr.20); unquoted figures are flagged "span not yet captured".
- Every assessment now carries a computed `evidence_tier` (best tier among cited
  signals' sources), displayed on each scorecard row — imported-only and
  self-only assessments are visible as such.

## Population / methodology

- Access re-labelled "Access depth (lab-granted)": granted access, not an
  institutional right or capability measure; a low score can mean labs did not
  grant access, not that the evaluator lacks competence.
- Population split by role in every table: referee, government, vendor,
  benchmark, lab-team (first-party), expected-entrant. Role filter chips on the
  homepage; role column on the evaluators page. Watchlist (big4, hfoai) is
  unranked, excluded from all averages, shown in its own section.
- big4 and hfoai carry `status: watchlist`; verifier C4 requires watchlist
  entries to have role expected-entrant.
- Type fixes: scale bigtech → vc; equistamp/nemesys vc → private (new type:
  "Private company, capital structure undisclosed"); big4 vc → hypothetical
  (new type: "Hypothetical composite, not a real organization").
- Product-conflict dimension re-labelled "Role incompatibility": selling to an
  evaluated lab is a structural role conflict, not proof of a failed evaluation.
- lab-procurement is the pre-registered confirmatory preset; the others are
  sensitivity checks.

## Paper / site

- `paper/draft.md` v0.4 rewritten from one verify/build/industries/paths run:
  26 ranked evaluators + 2 watchlist; 289 signals (156 for / 133 against)
  citing 114 public sources; METR 81 → MSFT 35 under the gated lab-procurement
  preset; dimension means S 2.92, M 2.88, X 2.81, R 2.58, A 2.50, P 2.35,
  G 2.27, F 2.19.
- H4 verdict corrected: README and draft agreed the draft had "rejected the
  access half"; on current data access (2.50) and methods (2.88) sit above
  funding (2.19) and personnel (2.35) — H4 is supported, with access mid-pack.
  README's "weak on scope control" fixed (scope is the strongest dimension).
- Title drops "Two Centuries".
- Trigger-lag median removed from the abstract; the lag pattern is reported as
  a hindsight-selected description, not a causal finding, pending an
  outcome-independent trigger enumeration.
- EU Code and Illinois SB 315 de-duplicated to one milestone each (AI: 5 of 7
  stages, not 6); `bench industries` S6 fixed to exclude accreditation, so
  start-to-independence reads 5/17/92/94/101/158/249 and matches the timeline.
- "Six of seven stages, fastest" softened with the prospective-observation
  caveat; "fourteen of fifteen" payer regimes corrected to thirteen;
  "twenty-four triggers" corrected to twenty; path similarity updated
  (credit ratings and crypto tie at distance 0.56) and presented as a
  hypothesis generator; the supplements mechanism match caveated as coarse.
- Legal claims softened: EU Code described as a voluntary code supporting the
  AI Act (not an enforceable obligation); "first" dropped from the Illinois
  mandate; "Nobody has published" → "We are aware of no public".
- `paper/README.md` and `paper/NOTES.md` reconciled to the same numbers.

## Process

- `DISCLOSURE.md`: curator-conflict fields marked "pending curator confirmation
  (requested 2026-09-15)" — publication blocked until filled by the curator.
  Site Method section now discloses single-coder/LLM-assisted construction
  (Claude, Anthropic) prominently.
- `pyproject.toml`: pinned `activegraph==1.10.0`, `jsonschema==4.26.0`,
  `markdown==3.9`; epistemedia documented as an optional `dockets` extra
  (all imports already degrade gracefully without it).
- `.github/workflows/pages.yml`: now installs pinned deps, verifies, builds,
  diffs graph/ and dist/ against the committed copies, runs pytest, then
  deploys — a stale site can no longer ship.
- `tests/test_repair.py`: 12 new tests (half-up rounding, HAL gate regression,
  gated default, missing-dimension refusal, C10 tier-1 gate on the dataset,
  certificate manual-issue refusal, quarantined/EUR/component exclusion from
  exposure and sums, duplicate-id check, evidence-clock enforcement,
  watchlist split). Full suite: 24 passed.
- The `bench industries` S6 column excluded accreditation (S5) from the
  independence computation; ship classification now reads 2009/249 and matches
  the stage ladder.
- Site: hop explainer on the first screen; new "How good is the evidence"
  section (54% self-published sources, 9% tier-1, 12% quote coverage,
  top-5 concentration); cases carry per-case citations; the quarantined
  Hugging Face/Nvidia acquisition narrative removed; homepage stats computed
  over the 26 ranked evaluators only; correction window through 29 Sep 2026
  stated in the Method section.

## Verification

- `python -m bench verify`: ok (125 sources, 308 signals, 224 assessments, 28 evaluators).
- `python -m bench build`: 942 objects, 2957 relations; second clean build
  byte-identical (`graph/events.jsonl` md5 9665626169792b01d5df98028cd43083).
- `pytest -q`: 24 passed.
- `dist/` audited: no self-certification badges, no stale docket pages
  (deleted `dist/source/docket-metr-lab-money.html`), no "third-party"
  population claims, footer review date 15 Sep 2026.
