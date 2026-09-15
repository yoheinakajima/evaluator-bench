# Evaluator Bench and Epistemedia

Checked 14 Sep 2026 against epistemedia.org, its agent submission protocol, the reviewed open docket, and the `epistemedia` package at commit 4e86baf.

## Different shapes, same discipline

Epistemedia's unit is one contestable claim, adjudicated: exact spans from pinned editions, lineage that collapses echoes to roots, a named policy, a skeptical lens, and a separate reviewer who re-fetches every credited source before anything reaches the public library. A proposal gets zero credit until that review.

Evaluator Bench's unit is a population: 28 organizations scored under a rubric, with a ledger behind the scores. The rubric is what Epistemedia would call an application policy; the scoreboard is a projection. Bench as a whole is not a docket and should not be submitted as one.

The claim layer is where they meet. Every Bench signal is a dated claim with sources; every ledger row is a transfer or role with a source and an audit status; every bounded negative is what Epistemedia calls a negative result that must not be converted to zero. Those map one to one onto Epistemedia's sources, spans, results, counterevidence, and negative_results.

## The bridge

`python -m bench docket build <slug>` turns `dockets/<slug>/draft.json` into an Epistemedia v0.2 proposal, generating the claim-atom closure the validator requires; `bench docket validate <slug>` runs Epistemedia's own fail-closed validator. The first docket, `metr-lab-money`, passes everything except the two things that require a networked run: the `ready-for-review` stamp from `epistemedia research complete`, and one artifact SHA-256 per source from `epistemedia research submit`. Reviewed dockets on epistemedia.org use Wayback `id_` captures so digests are byte-stable; the submit step should do the same.

Flow in both directions:

1. Bench surfaces a contestable claim (a signal that press repeats without its boundary, or a ledger negative that a rendered figure overstates).
2. A docket draft is written from Bench's sources and spans, built, validated, then submitted through Epistemedia's protocol on a networked machine and reviewed there — by someone else, not the Bench operator.
3. Only a docket reviewed at epistemedia.org by an independent reviewer may be cited by a Bench signal, and only as a secondary summary of that review — never as the strongest tier, and never with `audit_status: confirmed` unless the underlying primary sources were themselves re-derived. Bench drafts are not citable evidence, and the Bench never certifies its own drafts.

## Candidate dockets from Bench

Each is one question, contestable, with roots already in the ledger.

1. Does METR accept money from the frontier AI companies it evaluates? (drafted: `dockets/metr-lab-money`)
2. Did Coefficient Giving fund METR? A third-party figure implies yes by routing; the index reports no direct grant; the figure's own audit flags the overclaim. An echo-collapse case in the style of Case 002.
3. What share of Transluce's revenue came from lab employees in FY2025, and from labs as organizations? Its own policy page answers both; the claim "Transluce is independently funded" circulates without the split.
4. Is Gray Swan an independent evaluator of OpenAI? Roots: the board announcement, the recusal statement, the Series A release naming OpenAI as a client, and the system cards that call it external.
5. How fast do assurance rules follow public failures? Dataset B's lag claim, with the hindsight-selection problem stated as the unresolved item.
6. Does Illinois SB 315 require auditor independence, and from when? A date and scope claim (financial-interest clause, 2028 start, $500M threshold) that summaries compress.

## What Bench should borrow

Wayback `id_` captures with digests for every source; quote-minimal spans instead of paraphrase-only signals (the ledger's `quote` field exists and is mostly empty); the rule that an unresolved atom carries no evidence; and the separate-reviewer promotion step, which is the same thing `audit_status: confirmed` is trying to be.
