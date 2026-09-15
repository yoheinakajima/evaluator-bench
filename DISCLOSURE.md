# Curator disclosure

PROCESS.md section 10 asks of the curators what the rubric asks of evaluators. The homepage carries a six-line version of this statement beside the scores; this file is the full one.

## Yohei Nakajima

- Role: Managing Partner, Untapped Capital (pre-seed and seed venture fund); operator of Epistemedia, the claim-adjudication layer this repository drafts dockets into; author of ActiveGraph, which this repository is built on.
- Investments in, advisory roles at, or payments from any evaluator listed in this repository: **none** (confirmed by curator 2026-09-15).
- Investments in, advisory roles at, or payments from any frontier AI developer: small public-market shareholdings in Google and Meta, plus a private holding in SpaceX, which owns xAI, so indirect exposure to a frontier developer; no other private investments in any frontier developer.
- Funders shared with evaluators listed here (any fund that has invested in Untapped Capital and also funds an evaluator): **not yet checked.** The earlier "none known" was a best-effort statement, not a check. The check, Untapped Capital's limited partners against the funder and investor entities in `data/ledger/entities.csv`, is scheduled before the 29 September 2026 freeze; its result, with the date it was run, replaces this line.
- Personal relationships with people named in the ledger: **none** (confirmed by curator 2026-09-15).

## Assistant

The initial curation was drafted by Claude (Anthropic) across sessions on 14 and 15 September 2026, directed by the curator, with independent verification passes by other tools (Codex, Grok) recorded in `paper/audits/`. The v0.1 pass that assigned a bound and a rule to every signal, captured quoted spans, and wrote each card's dissent was also drafted by Claude on 15 September 2026 under `RULES.md`, with the curator reviewing. Anthropic is a frontier developer evaluated by several organizations scored here, and appears in the ledger as a lab entity. Every value is derived from signals under published rules and re-derivable without the assistant; the verifier, the audit files, and the review step exist so that this origin can be checked rather than trusted.

## Second coder

None yet. Version 0.1 has one coder. A human second coder on every extreme (every stored 0 or 4) is a gate for a citable tag (`bench gates`); agreement is logged in `data/coding/second-coder.csv` and shown on the status page. The full population follows by v0.2.

## Rule

If a curator holds a financial interest in an evaluator or a lab, the assessments of that evaluator, and of evaluators whose scores turn mainly on that lab, are marked in their rationale so readers can weigh the interest, and are open to public correction through the contribution path. Under this rule the public shareholdings in Google and Meta are a financial interest in two labs in the ledger; the evaluators with confirmed ledger ties to those labs (Epoch, Scale, MLCommons) carry the note in their rationales.
