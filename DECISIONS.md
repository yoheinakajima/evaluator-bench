# Decisions

Dated records of choices that change what the site measures or how it reads. One entry per decision: what, why, what else was considered, what it moves, and how to reverse it. Anything that changes scope, a rule that moves many values, or the way a number is shown gets an entry before the change lands. Smaller rule amendments are logged in `paper/audits/` and the changelog.

## D-005, 15 September 2026: contested-claim drafts leave the navigation

**Decision.** The Dockets page is no longer in the site navigation. One sentence on the Contribute page says what the drafts are; the page and the tooling stay in the repository.

**Why.** No draft has been submitted for review, so the page described a promise, not a feature, and two readers reported the vocabulary as confusing on first contact.

**Reversal.** Restore the navigation entry when the first draft has been independently reviewed.

## D-004, 15 September 2026: evaluation credits are not lab money

**Decision.** Compute, credits, tokens, and pre-release access consumed in evaluating a lab's own model are the substrate of the evaluation, not a payment. They never bound the funding value, never enter the hop buckets of the money matrix, and are not counted as a direct lab tie. They stay in the ledger as `in_kind` rows and appear on the entity page. Only general operating compute that funds an organization's work beyond the evaluation counts, and only above the materiality threshold in RULES F.2.

**Why.** Evaluating a model requires access to it; free credits for that purpose are standard across the field and the row existed only for the organization that disclosed it, which penalized disclosure. If evidence emerges that an organization's operations depend on lab compute, F.2 still applies.

**Considered.** A separate "evaluation credits" class shown as its own column. Rejected for now as a distinction without a consequence; add it if a reader asks for it.

**Moves.** METR's only direct lab tie was the in-kind row; it leaves the hop-0 count. SecureBio's free-API-access signal becomes informational.

**Reversal.** Reinstate the F.2 in-kind cap for evaluation credits with a materiality threshold, and count `in_kind` rows in the hop buckets again.

## D-003, 15 September 2026: the number is hidden until the reader chooses weights

**Decision.** By default the directory shows, for each organization, the band, the coverage count, the weakest dimension, and the eight dimension values. The weighted number and the score bar appear only after the reader presses "Score with these weights," having chosen or accepted a weight preset. The default order is band first, then the weakest dimension.

**Why.** A single default number was being read as a trust score and screenshotted as one. Everything the band and the dimension values say is weight-independent; the number is the part that depends on a persona, so the reader should own it. Entity pages keep the numbers under every preset because anyone that deep is reading, not skimming.

**Considered.** Hiding scores entirely (loses the ranking that procurement readers want); showing the number with a warning (warnings do not survive screenshots).

**Reversal.** Set the scored state to true by default in the template.

## D-002, 15 September 2026: bands are set by the conflict dimensions only

**Decision.** The disqualifying and conditional bands are computed from funding, governance, personnel, role incompatibility, scope control, and publication rights. Access depth and method transparency count in the weighted number but never place an organization in a band.

**Why.** A 0 on access means the labs have not let the organization in; a 0 on methods means it has not published them. Neither is a conflict. Under the previous definition AVERI, the Princeton leaderboard, and MLCommons sat in the disqualifying band beside a lab-owned vendor and a firm that sells the fix to the labs it grades, which is a category error the band label made worse.

**Considered.** A separate "untested" band for access 0 (adds a fourth state readers must learn); keeping access in the band with a different label (the label is not the problem, the grouping is).

**Moves.** AVERI, the Princeton leaderboard, and MLCommons leave the disqualifying band; Palisade, Humane Intelligence, the Center for AI Safety, FAR.AI, SaferAI, Epoch, Andon Labs, EquiStamp, and Dreadnode leave the conditional band where access was their only 1.

**Reversal.** Return access and methods to the band set in `bench/score.py` and the template.

## D-001, 15 September 2026: scope is third-party evaluation of frontier AI for safety-relevant properties

**Decision.** An organization is in scope if it evaluates or red-teams frontier models for safety-relevant properties: dangerous capabilities (biological, chemical, cyber, autonomy), misuse, alignment and scheming, security, safeguards, and incident investigation; or it is a public body or standards body with a role in that layer. Capability and performance leaderboards, and organizations whose only frontier work is capability benchmarking, are out of scope. RULES 11 carries the clause.

**Why.** The project began as a directory of the evaluators labs cite for safety, and the population check showed the criteria as written admitted capability leaderboards (Artificial Analysis, Arena, Vals AI, Mercor, Harvey, the ARC Prize, Terminal-Bench). Scoring those on an independence rubric written for safety assurance would mix two questions.

**Considered.** Keeping the wider population with a "safety" tag (keeps a comparison nobody asked for); deleting the out-of-scope records (destroys history and the event log).

**Moves.** The Holistic Agent Leaderboard (Princeton) and Epoch AI move to `status: out-of-scope`, retained, unranked, shown in their own section and excluded from every statistic. Epoch is the judgment call: its frontier work is capability benchmarking, but the FrontierMath funding-disclosure episode set a norm the safety evaluators now follow, so the case stays on the Cases page. The seven capability leaderboards in the population check are marked out by scope. The ranked population is 24.

**Reversal.** Set the status back to ranked and remove the clause from RULES 11; the records, bounds, and derivations are untouched.
