# Critique of the v0 approach, and what changed in v0.2

Written 14 Sep 2026 after the first full build. Kept so reviewers can see what the authors already know is weak.

## Problems in v0

1. **The ladder implies a sequence regimes do not follow.** Financial audit went mandate, rollback, voluntary, mandate. Nuclear had a mandate before any voluntary layer. "Reached six of seven" treats stages as a checklist and hides order and reversals.
2. **First-year-reached erases instrument strength.** AI's "Independence 2026" is one clause in one state, effective 2028, for developers over $500M revenue. The cell renders it like Sarbanes-Oxley.
3. **Triggers were selected with hindsight.** Incidents known to precede rules were coded as triggers, then the lag to rules was measured. The two-year median is partly an artifact.
4. **Lag was measured to any rule.** A disclosure requirement counted the same as a structural reform, which inflates apparent responsiveness.
5. **The evaluator score is compensatory.** A Big Tech unit can offset a 0 on funding with a 4 on methods. Independence has floors.
6. **Signal counts were padded.** "Nonprofit." as a for-signal on small organizations inflated for-counts, which the site then displayed.
7. **The ladder shows legal forms, not incentives.** The thesis is about who pays, selects, sees, publishes, and watches the watcher. None of that was visible.
8. **Regime boundaries are fuzzy** (cybersecurity bundles Common Criteria, PCI, FedRAMP, SOC 2) and **regime ages are not comparable** (first milestone is whatever the coder chose to start with).
9. **Year granularity** loses ordering inside 2026, where most of AI's milestones sit.

## What v0.2 does about it

- Every rule milestone now carries `strength` 1 to 4 (disclosure, standard or private rule, statutory mandate or accreditation, structural change) and a `jurisdiction`. Addresses 2 and 4.
- Every trigger carries a `harm` class and a `trigger_criterion` applied before looking at outcomes: ten or more deaths, losses above $1B, or a documented integrity failure of the assurance itself. Triggers that met the criterion and were followed by nothing are now the main open coding task. Addresses 3 partially; the selection bias is named, not removed.
- `bench paths` produces path signatures (ordered kind sequences with repeats collapsed) and ranks regimes by edit distance between their opening moves and AI's. Order and reversals are first-class. Addresses 1.
- `bench paths` also pairs each trigger with the next rule and reports lag against strength. Result on the seed: 16 responses within three years, mean strength 2.9, two structural. Addresses 4.
- Each regime carries a `mechanisms` block (pays, selects, access, publishes, oversees) before and now, rendered as a matrix. Addresses 7.
- The site has a gated scoring mode (any 0 caps at 40, any 1 at 60) and shows each evaluator's weakest dimension and its score range across presets instead of for/against counts. Addresses 5 and 6.
- The ladder stays, with a caveat paragraph, because first-arrival years are still useful for the placement claim; it is no longer the only view.

## Still open

- Outcome-independent trigger enumeration (search each regime for qualifying incidents, not just remembered ones).
- Month-level dates for AI milestones and any regime with a dense reform period.
- Splitting bundled regimes (cybersecurity into its schemes; AI into model evals, org audits, and government testing).
- A second coder on strength, harm class, and mechanisms, with agreement reported.
- Anchors that separate legal form from conduct in the governance dimension.

## v0.3 addendum: the money side was thin

A third-party ledger (kevinnbass/metr-money-figure) showed what tier-1 evidence looks like for the funding and personnel dimensions: 990 e-file object ids, funder index snapshots with row counts, DAF Schedule I rows, Wayback captures of policy wording, and per-row audit verdicts with hashed artifacts. Against that, v0.2 scored funding from press and self-statements and had no representation of second-order exposure (funders who hold lab equity, board members whose organizations are lab contractors) or of bounded negatives. v0.3 adds the ledger, the exposure projection, and a verify gate. The scores it changed moved down, which is the direction a stricter evidence standard should push a self-reported "no lab money" claim. The same ledger's own audit also shows the other failure mode: a rendered figure that overclaims what its rows support. The rows are the product; the picture is a reading.
