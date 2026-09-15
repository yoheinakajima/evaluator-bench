# Contributing evidence

What moves a score is a signal with a source. Open a PR that does one of these:

**Add a signal.** Append to `data/signals/<evaluator>.json`:

```json
{
  "id": "metr.14",
  "evaluator": "metr",
  "dimension": "P",
  "direction": "for",
  "claim": "Published a cooling-off policy for staff moving to frontier labs.",
  "sources": ["metr-cooling-off-2026"],
  "recorded": "2026-10-01",
  "curator": "your-handle",
  "quote": "optional, under 120 characters"
}
```

and add the source to `data/sources/metr-cooling-off-2026.json` with a URL and the date you retrieved it. If the claim changes an assessment, edit the value in `data/assessments/<evaluator>.json`, add the signal id to that assessment's `signals`, and update the rationale.

**Correct a claim.** Add a new signal with `superseded_by` set on the old one, or fix the old one if it was a transcription error. Say which in the PR.

**Add an evaluator.** Create `data/evaluators/<id>.json`, a signals file, and an assessments file with all eight dimensions. `verify` will tell you what is missing.

**Add an industry milestone** for the paper dataset in `data/industries/`. Primary sources preferred; mark secondary ones.

Then run:

```
python -m bench verify && python -m bench build
```

and commit the regenerated `graph/` and `dist/`. CI rebuilds and fails if the committed log differs from a clean build.

Rules of the road:

- Public evidence only. No private communications, no screenshots of paywalled pages.
- Claims are paraphrased in your own words. Quotes, if any, stay under 120 characters.
- An evaluator's own statement about itself counts as a source, labeled as such.
- Disagreements about a value are resolved in the PR thread and recorded in the rationale, not by averaging.
- If you work for or are paid by an evaluator or a lab, say so in the PR. That disclosure is the same thing this repo asks of the evaluators.
