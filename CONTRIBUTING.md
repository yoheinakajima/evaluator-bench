# Contributing evidence

What moves a value is a signal with a source, a quoted span, and a bound. Open a PR that does one of these:

**Add a signal.** Append to `data/signals/<evaluator>.json`:

```json
{
  "id": "metr.23",
  "evaluator": "metr",
  "dimension": "P",
  "direction": "for",
  "claim": "Published a cooling-off policy for staff moving to frontier labs.",
  "sources": ["metr-cooling-off-2026"],
  "recorded": "2026-10-01",
  "as_of": "2026-10-01",
  "curator": "your-handle",
  "quote": "under 120 characters, copied exactly from the page",
  "quote_source": "metr-cooling-off-2026",
  "bound": {"floor": 3},
  "rule": "P.5"
}
```

and add the source to `data/sources/metr-cooling-off-2026.json` with a URL, the date you retrieved it, its `source_type`, and `press_kind` if it is press. The value is derived: run `python -m bench verify`, and if it says the stored value must change, set the value and anchor in `data/assessments/<evaluator>.json` to what it derives, add the signal id to that assessment's `signals`, and add a `resolution` naming the rule if a floor and a cap now disagree.

**Correct a claim.** Add a new signal with `superseded_by` set on the old one, or fix the old one if it was a transcription error. Say which in the PR.

**Add an evaluator.** Create `data/evaluators/<id>.json` (with a dissent), a signals file with bounds and rules, and an assessments file with all eight dimensions. Add the ledger entity. `verify` will tell you what is missing. Do not add a hypothetical organization.

**Check a population candidate.** Add an entry to `data/exclusions.json` with the criterion and the URL that decided it (RULES 11).

**Add an industry milestone** for the paper dataset in `data/industries/`. Primary sources preferred; mark secondary ones.

Then run:

```
python -m bench verify && python -m bench build && pytest -q
```

and commit the regenerated `graph/` and `dist/`. CI rebuilds and fails if the committed log differs from a clean build.

Rules of the road:

- Public evidence only. No private communications, no screenshots of paywalled pages.
- Claims are paraphrased in your own words. Quotes stay under 120 characters and must appear verbatim on the page.
- An evaluator's own statement about itself counts as a source, labeled as such; under the against-interest policy it counts only when it is against the evaluator's interest.
- Disagreements about a value are resolved by the rule in RULES.md and recorded in the resolution, not by averaging.
- People are recorded by public role only. An open question about a person is a document request.
- If you work for or are paid by an evaluator or a lab, say so in the PR. That disclosure is the same thing this repo asks of the evaluators.
