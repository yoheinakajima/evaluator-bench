# Instructions for agents contributing to Evaluator Bench

You are editing an evidence ledger, not writing prose. Every change you make must be a row or a signal that a machine can check and a person can re-derive. Read CONTRACT.md and RULES.md first. Then follow exactly one of the recipes below, run the checks, and open a pull request whose body follows `.github/PULL_REQUEST_TEMPLATE.md`.

## How a value is made

Nobody types a value. Each signal carries a `bound`: an against-signal sets a cap (`{"cap": n}`), a for-signal sets a floor (`{"floor": n}`), and the `rule` field names the RULES.md rule that says so (for example `"F.3"`). The value on a dimension is the smallest cap or, with no cap, the largest floor, over the signals that count under the evidence policy. A 0 needs a quoted span; a 4 needs a span and a second source. If your signal changes a value, the verifier will tell you what the stored value must become; set it to that and say so in the pull request.

## What you may change

- `data/sources/*.json`: add a source (URL, publisher, published date, retrieved date, `source_type`, `press_kind` for press, `audit_status: confirmed` only if you fetched it yourself in this run).
- `data/signals/<evaluator>.json`: add a signal (one dimension, one direction, one claim, sources, `recorded`, `as_of`, `bound`, `rule`, and a `quote` under 120 characters copied exactly from the source with `quote_source` naming which source).
- `data/assessments/<evaluator>.json`: set the value to what the verifier derives; add a `resolution` (rule, value, note) if a floor and a cap now disagree; keep `open_questions` current as document requests (RULES 12); set `mechanism` on access and publication.
- `data/evaluators/<evaluator>.json`: the dissent paragraphs; never the role (it is derived).
- `data/ledger/*.csv`: add transfers, relationships, negatives. `audit_status: confirmed` only for rows you re-derived from the cited source in this run.
- `data/industries/*.json`: add milestones with a source; mark strength and, for triggers, harm class and criterion.
- `data/exclusions.json`: add a population candidate with the criterion checked and the URL that decided it.
- `dockets/<slug>/draft.json`: draft a new Epistemedia docket from Bench evidence.

## What you may not change

Anchors, rules, presets, the CONTRACT, the verifier, or the build. Do not edit `graph/` or `dist/` by hand; they are regenerated. Do not delete rows; supersede them (`superseded_by`) and say why. Do not add a hypothetical organization.

## Recipe A: add evidence about an evaluator

1. Fetch the source yourself. Save its URL, the date, and the exact sentence you rely on.
2. Add the source file. Set `source_type` to what the source is (filing, index, ledger, self, press) and `press_kind` (primary, aggregator) for press. Set `audit_status: confirmed`.
3. Add the signal with a `quote` copied verbatim, `quote_source`, an `as_of` date, a `bound`, and a `rule`.
4. Run `python -m bench verify`. If it reports that the stored value must change, edit the value (and `anchor`) in `data/assessments/`, add the signal id to that assessment's `signals`, and add a `resolution` if the verifier reports a conflict. Say in the PR which anchor text now applies.
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

## Recipe D: check a population candidate

1. Read RULES.md section 11. Search for the organization in frontier system cards, government evaluation reports, statutes and codes, and developer citations of leaderboards, within the 24 months to the evidence clock.
2. Add an entry to `data/exclusions.json` with the criterion met (or none), the URL that decided it, a one-line note, and the result: in-scope-candidate, out, or unclear. Do not score it.

## Rules of evidence

Public sources only. Public roles only. Quote-minimal spans. Never sum across money measures. Never convert a bounded absence into zero. No motive, intent, or characterization of any person; an open question about a person is a document request. If you are paid by, employed by, or invested in an evaluator or a lab, say so in the PR body.

## What happens to your PR

CI runs the verifier, rebuilds, checks the log for drift, and runs the tests. `bench review` then re-fetches every source your PR cites and asks a model whether each quoted span appears in the fetched text and whether each claim is supported by it; its report is posted on the PR. A maintainer reads the report and merges or asks for changes. Accepted evidence feeds the next annual update paper (see `paper/ANNUAL.md`).
