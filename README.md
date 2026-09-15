# Evaluator Bench

An evidence-linked, event-sourced directory of third-party evaluators for frontier AI, with an independence score you can take apart.

Site: `dist/index.html` (GitHub Pages from `dist/`). Data: `data/`. Log: `graph/events.jsonl`.

## Why

Labs now cite the same six or seven outside groups in every system card. Regulators in the EU and Illinois require "independent" external evaluators without saying what independent means. Nobody publishes a scored, sourced view of the evaluators themselves. This repo does, and it makes every number traceable: score to assessment to signal to source, with the retrieval date and the graph event that recorded it.

## How it is built

The repo is an ActiveGraph project. `data/` holds the human-edited truth as plain JSON. `python -m bench build` turns those files into typed graph objects and relations, streams every creation into `graph/events.jsonl` through a frozen clock and a fixed run id, and projects `dist/bench.json` and `dist/index.html` from the graph. Two builds on the same data produce a byte-identical log, so a diff in the log means data changed.

Object types and their provenance chain:

```
score  --derived_from-->  assessment  --supported_by-->  signal  --cites-->  source
  |                          |                              |
  of evaluator               of evaluator, on dimension     about evaluator, on dimension
```

Each object's ActiveGraph provenance carries the actor, the frozen timestamp, and `evidence`, the event ids of the objects it rests on. `python -m bench inspect grayswan --dim P` walks that chain back from the log rather than from the JSON, which is how a sink misconfiguration that silently dropped events was caught during the first build.

## Commands

```
pip install -e .
python -m bench verify        # integrity checks (the CONTRACT); CI runs this on every PR
python -m bench build         # graph -> graph/events.jsonl, dist/bench.json, dist/index.html
python -m bench scores lab    # ranked table for a preset (lab | regulator | public | equal)
python -m bench inspect metr  # provenance chain for one evaluator, optionally --dim A
python -m bench industries    # cross-industry lifecycle table: trigger-to-rule lags
python -m bench timeline      # stage ladder (Figure 1); build writes dist/timeline.svg
```

## The rubric

Eight dimensions, each 0 to 4 with written anchors in `data/dimensions.json`: funding, governance, personnel, access depth, scope control, publication rights, method transparency, product conflicts. Presets in `data/presets.json` weight them for lab procurement, regulator selection, or public trust. The site lets a reader move the weights and watch the ranking change.

The rubric draws on the AI Evaluator Forum's AEF-1 operating conditions, the auditor-independence rules Illinois SB 315 imports from financial audit, and the Charnock et al. access taxonomy. Two dimensions the field tends to skip are included: who owns the evaluator, and whether it sells remediation to the companies it grades.

## What a score is and is not

A score is a reading of the public record at a date. It is not an endorsement and a low score is not an accusation; it means the record does not yet show the safeguards that would earn a higher one. Confidence tags (high, med, low) flag thin records. Independence is one axis; competence, domain coverage, and turnaround are others.

## Where we are

The site's "Where we are" section and `paper/figures/stage-ladder.svg` place frontier AI on a seven-stage ladder next to fifteen other assurance regimes coded in `data/industries/`. The paper draft that reads the two datasets together is `paper/draft.md`.

## Contributing evidence

PRs change signals and sources, never scores directly. See `CONTRIBUTING.md`. A PR that changes an assessment without a signal on the same evaluator and dimension fails `verify`.

## Layout

```
data/            sources, evaluators, signals, assessments, dimensions, presets, industries
schema/          JSON Schema for each data type
bench/           loader, verifier, ActiveGraph build, projections, CLI
graph/           generated event log (committed; reproducible)
dist/            generated site and JSON projection (committed; served by Pages)
site/            HTML template
paper/           paper concept, novelty check, related work, analysis notes
tests/           pytest
```

## License

Code: Apache-2.0. Data in `data/` and `graph/`: CC BY 4.0. Cite as Evaluator Bench, 2026, with the commit hash.
