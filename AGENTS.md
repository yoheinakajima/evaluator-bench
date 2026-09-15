# Instructions for agents contributing to Evaluator Bench

You are editing an evidence ledger, not writing prose. Every change you make must be a row or a signal that a machine can check and a person can re-derive. Read CONTRACT.md first. Then follow exactly one of the recipes below, run the checks, and open a pull request whose body follows `.github/PULL_REQUEST_TEMPLATE.md`.

## What you may change

- `data/sources/*.json`: add a source (URL, publisher, published date, retrieved date, `source_type`, `audit_status: confirmed` only if you fetched it yourself in this run).
- `data/signals/<evaluator>.json`: add a signal (one dimension, one direction, one claim, sources, `recorded`, `as_of`, and a `quote` under 120 characters copied exactly from the source).
- `data/assessments/<evaluator>.json`: change a value only when a signal on that dimension supports the new anchor; update `rationale`, `assessed`, `assessor`; keep `open_questions` current.
- `data/ledger/*.csv`: add transfers, relationships, negatives. `audit_status: confirmed` only for rows you re-derived from the cited source in this run.
- `data/industries/*.json`: add milestones with a source; mark strength and, for triggers, harm class and criterion.
- `dockets/<slug>/draft.json`: draft a new Epistemedia docket from Bench evidence.

## What you may not change

Scores, presets, anchors, the CONTRACT, the verifier, or the build. Do not edit `graph/` or `dist/` by hand; they are regenerated. Do not delete rows; supersede them (`superseded_by`) and say why.

## Recipe A: add evidence about an evaluator

1. Fetch the source yourself. Save its URL, the date, and the exact sentence you rely on.
2. Add the source file. Set `source_type` to what the source is (filing, index, ledger, self, press). Set `audit_status: confirmed`.
3. Add the signal with a `quote` copied verbatim and an `as_of` date.
4. If the signal moves an assessment, edit the value and the rationale. Say in the PR which anchor text now applies.
5. Run `python -m bench verify && python -m bench build && pytest -q`. Commit the regenerated `graph/` and `dist/`.

## Recipe B: confirm an imported ledger row

1. Open the row's `source_url`. Read the specific figure or role.
2. If it matches, set `audit_status: confirmed` and append a note with the date and what you saw. If it differs, set `differs` and record both values. If the page is gone, set `unverifiable` and say what you tried.
3. Append a line to `paper/audits/AUDIT-<n>.md` with the verdict.
4. Run the checks and commit.

## Recipe C: draft a docket

1. Choose one contestable claim that Bench evidence bears on. Check `dockets/` and epistemedia.org for prior art.
2. Copy an existing `draft.json`. Every span must be an exact quote from a page you fetched in this run.
3. `python -m bench docket build <slug> && python -m bench docket validate <slug>`. Only the `ready-for-review` and artifact-digest errors may remain.

## Rules of evidence

Public sources only. Public roles only. Quote-minimal spans. Never sum across money measures. Never convert a bounded absence into zero. No motive, intent, or characterization of any person. If you are paid by, employed by, or invested in an evaluator or a lab, say so in the PR body.

## What happens to your PR

CI runs the verifier, rebuilds, checks the log for drift, and runs the tests. `bench review` then re-fetches every source your PR cites and asks a model whether each quoted span appears in the fetched text and whether each claim is supported by it; its report is posted on the PR. A maintainer reads the report and merges or asks for changes. Accepted evidence feeds the next annual update paper (see `paper/ANNUAL.md`).
