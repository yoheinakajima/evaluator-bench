# Evaluator Bench

Status: v0.1 candidate, preview window through 29 Sep 2026. See `CHANGELOG.md` for what changed, `RULES.md` for how a value is made, `paper/PLAN-v0.1.md` for the plan this release follows, and `LAUNCH.md` for the operator steps.

An evidence-linked, event-sourced directory of third-party evaluators of frontier AI for safety-relevant properties: 27 organizations on file, 24 ranked, 1 expected entrant on a watchlist, 2 retained out of scope as capability benchmarks. Each carries an independence score you can take apart, under an evidence policy you choose, with a row-level ledger of who pays whom. Scope and every change to it are recorded in `DECISIONS.md`.

Site: `dist/index.html` (GitHub Pages from `dist/`, at evaluatorbench.com). Data: `data/`. Log: `graph/events.jsonl`.

## Why

Labs now cite the same six or seven outside groups in every system card. Regulators in the EU and Illinois require "independent" external evaluators without saying what independent means. Nobody publishes a scored, sourced view of the evaluators themselves. This repo does, and it makes every number traceable: score to assessment to signal to source, with the retrieval date, the rule that turned the signal into a value, and the graph event that recorded it.

## How a value is made

Nobody types a value. Every signal carries a `bound` (an against-signal caps the value on its dimension, a for-signal floors it) and the `RULES.md` rule code that says so. The value is the smallest admissible cap or, with no cap, the largest admissible floor. Where a floor and a cap disagree, the assessment carries a resolution naming the rule, and the card shows the conflict. A 0 needs a quoted span; a 4 needs a span and a tier-1 or tier-2 source or two independent sources with one not self-published; a bound from sources that were not all confirmed cannot set an extreme. The verifier fails if a stored value disagrees with its derivation.

The reader chooses what counts. Under the default policy, standard, a signal moves a number only if at least one of its sources was re-fetched and confirmed; imported and unverifiable leads stay visible and count for nothing. Against interest admits an organization's own statements only when they are against its interest. Verified spans requires a quoted span. Primary only admits confirmed filings, indexes, and third-party ledgers with a span: what can be verified from outside the field. A dimension with no admissible signal renders as a dash and is excluded from the score; the coverage count sits beside every score.

Independence has floors, so the band comes first: an evidenced 0 on a conflict dimension (funding, governance, personnel, role incompatibility, scope, publication) is a disqualifying floor, a 1 a conditional floor, otherwise clear. Access and methods count in the number but never set a band. On the directory the number is hidden until the reader chooses weights; the band, the coverage, and the eight values show by default.

## How it is built

The repo is an ActiveGraph project. `data/` holds the human-edited truth as plain JSON. `python -m bench build` turns those files into typed graph objects and relations, derives every value under every policy, streams every creation into `graph/events.jsonl` through a frozen clock and a fixed run id, and projects `dist/bench.json` and the site from the graph. Two builds on the same data produce a byte-identical log, so a diff in the log means data changed.

Object types and their provenance chain:

```
score  --derived_from-->  assessment  --supported_by-->  signal  --cites-->  source
  |                          |                              |
  per policy and preset      value derived from bounds      bound + rule + quoted span
```

`python -m bench inspect grayswan --dim P` walks that chain back from the log rather than from the JSON.

## Commands

```
pip install -e .
python -m bench verify        # integrity checks (the CONTRACT); CI runs this on every PR
python -m bench build         # graph -> graph/events.jsonl, dist/bench.json, dist/
python -m bench scores lab [--policy standard] [--by-type]   # band-first table for a preset and policy
python -m bench gates         # the gates for a citable tag; release refuses while any fails
python -m bench inspect metr  # provenance chain for one evaluator, optionally --dim A
python -m bench industries    # cross-industry lifecycle table: trigger-to-rule lags
python -m bench timeline      # stage ladder (Figure 1); build writes dist/timeline.svg
python -m bench paths         # path signatures, nearest analogues to AI, trigger-response strength, mechanisms
python -m bench exposure      # ledger check and inflows by hop distance from a lab, per evaluator
python -m bench audit T12 R10 # re-fetch cited sources, hash them into data/artifacts.csv (needs network)
python -m bench review --all  # re-fetch every quoted source and check the spans; --base origin/main for a PR
python -m bench outreach --all   # right-of-reply packets for every ranked organization and named person
python -m bench docket build metr-lab-money   # Bench draft -> Epistemedia proposal; validate with `docket validate`
python -m bench certificate verify metr-lab-money   # check a certificate still binds its proposal bytes
python -m bench changelog --since v0.1        # what changed between two revisions (input to the annual paper)
python -m bench release --stage published --tag v0.1   # refused until `bench gates` passes
```

## The rubric

Eight dimensions, each 0 to 4 with written anchors in `data/dimensions.json`: funding, governance, personnel, access depth (lab-granted), scope control, publication rights, method transparency, role incompatibility. Presets in `data/presets.json` weight them for lab procurement, regulator selection, or public trust, each with a written derivation. The site lets a reader move the weights and switch the evidence policy and watch the ranking change.

The rubric draws on the AI Evaluator Forum's AEF-1 operating conditions, the auditor-independence rules Illinois SB 315 imports from financial audit, and the Charnock et al. access taxonomy. Two dimensions the field tends to skip are included: who owns the evaluator, and whether it sells remediation to the companies it grades. The tie-breaks that turn a claim into an anchor are in `RULES.md`; roles (referee, government, vendor, first-party, benchmark) are derived from the same rules, and the population criteria and every candidate checked are in `data/exclusions.json`.

## Ledger and exposure

Funding, governance, and personnel claims rest on `data/ledger/`: one transfer or role per row, source type and audit status on every row, bounded "none found" rows with the corpus and snapshot date. `python -m bench exposure` reports each evaluator's inflows by measure and by hop distance from a frontier lab, and lists board, advisor, donor, and investor ties within two hops. The process is in `paper/PROCESS.md`; open questions in `paper/OPEN-QUESTIONS.md`.

## What a score is and is not

A score is a reading of the public record at a date under a stated evidence policy. It is not an endorsement and a low score is not an accusation; it means the record does not yet show the safeguards that would earn a higher one. Confidence tags (high, med, low) flag thin records, and every card carries a dissent: the strongest case that its weakest dimension should be one notch lower, and one notch higher. Independence is one axis; competence, domain coverage, and turnaround are others.

## Where we are

The site's regimes page places frontier AI next to fifteen other assurance regimes coded in `data/industries/`: a stage ladder, ordered path strips with a nearest-analogue ranking, a trigger-response strength plot, and a mechanism matrix. Dataset B is coded from secondary sources at year granularity with hindsight-selected triggers; the caveat sits on the figure. `paper/CRITIQUE.md` records what was wrong with the first version and what changed. The paper draft is `paper/draft.md`.

## Site structure

`index.html` is the directory: three lists (independent referees, government institutes, commercial and first-party), with the evidence policy, the weights, and the band-first sort as controls, a four-paragraph guide to reading it, and a teaser for the regimes work. Topic pages hold the rest: the rubric and rules, the regimes, the money matrix and funding graph, the cases, the method and disclosure, the population check, and the status page with the gates for a citable tag and the right-of-reply log. Every entity, regime, and source has its own page. An entity page shows the scorecard with the derivation and binding signal on every dimension, the values under each policy, the dissent, every ledger row in and out, and the funding graph focused on that node.

## Contested claims

Bench is an index with a scoring policy. Claims that will be contested are drafted as proposals for independent review by a third party, Epistemedia (epistemedia.org), where a reviewer other than the drafter checks each quoted span; `dockets/` holds the drafts and `bench docket` builds and validates them. A draft is not evidence and none has been reviewed yet, so the page is off the site's navigation until one has (decision D-005). See `paper/EPISTEMEDIA.md`.

## Contributing evidence

PRs change signals, sources and ledger rows, never values directly. Agents get step-by-step recipes in `AGENTS.md`; the PR template is machine-read; CI runs the verifier, the build, the drift check, the tests, and `bench review`, which re-fetches every cited source and checks quoted spans and claims. See `CONTRIBUTING.md`. A PR that changes a value without a signal whose bound derives it fails `verify`. Accepted evidence feeds the annual update paper (`paper/ANNUAL.md`), generated from `bench changelog` between two tagged commits.

## Layout

```
data/            sources, evaluators, signals, assessments, dimensions, presets, industries, ledger, cases, guide, exclusions, outreach log, second-coder log
schema/          JSON Schema for each data type
bench/           loader, verifier, policy derivation, roles, gates, ActiveGraph build, projections, CLI
graph/           generated event log (committed; reproducible)
dist/            generated site (committed; served by Pages)
site/            HTML templates and static assets
paper/           paper draft, plan, process, critique, audits, open questions
outreach/        right-of-reply packets (generated; sending is a human action)
leads/           agent outputs awaiting or after merge (bounds files, quote audit, population check)
tests/           pytest
```

## License

Code: Apache-2.0. Data in `data/` and `graph/`: CC BY 4.0. Cite as Evaluator Bench, 2026, with the commit hash.
