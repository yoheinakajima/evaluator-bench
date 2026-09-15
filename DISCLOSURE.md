# Curator disclosure

PROCESS.md section 10 asks of the curators what the rubric asks of evaluators. The homepage carries a six-line version of this statement beside the scores; this file is the full one.

## Yohei Nakajima

- Role: Managing Partner, Untapped Capital (pre-seed and seed venture fund); operator of Epistemedia, the claim-adjudication layer this repository drafts dockets into; author of ActiveGraph, which this repository is built on.
- Investments in, advisory roles at, or payments from any evaluator listed in this repository: **none** (confirmed by curator 2026-09-15).
- Investments in, advisory roles at, or payments from any frontier AI developer: small public-market shareholdings in Google and Meta, plus a private holding in SpaceX, which owns xAI, so indirect exposure to a frontier developer; no other private investments in any frontier developer.
- Funders shared with evaluators listed here (any fund that has invested in Untapped Capital and also funds an evaluator): **not yet checked.** The earlier "none known" was a best-effort statement, not a check. The check, Untapped Capital's limited partners against the funder and investor entities in `data/ledger/entities.csv`, is scheduled before the 29 September 2026 freeze; its result, with the date it was run, replaces this line.
- Personal relationships with people named in the ledger: **none** (confirmed by curator 2026-09-15).

## Assistants

This repository is a collaboration between the curator and several models from several developers, each of which is a lab in this ledger. Claude (Anthropic) drafted the initial curation on 14 and 15 September 2026 and the v0.1 pass that assigned a bound and a rule to every signal, captured quoted spans, and wrote each card's dissent. Codex (OpenAI) and Grok (xAI) ran independent verification passes recorded in `paper/audits/`, and Codex made repository changes in its own commits. Gemini (Google) and Muse reviewed the site and the paper and criticized them; their feedback shaped the plan in `paper/PLAN-v0.1.md` and the decisions in `DECISIONS.md`. Anthropic, OpenAI, xAI, and Google are frontier developers evaluated by organizations scored here.

One concern deserves a direct answer: a model built by Anthropic drafted a ranking in which METR, the evaluator Anthropic named in its September 2026 commitment, sits first. Every value on this site is derived from signals whose bounds and rule codes are public, under rules applied to every organization the same way; every span and source is open; the ranking is re-derivable by anyone, with any tool or none; and the against-interest and primary-only views are one click away. If a model's involvement had tilted a value, the place it would show is a bound or a rule, and both are open to correction through the contribution path. The verifier, the audit files, and the review step exist so that this origin can be checked rather than trusted.

## Second coder

None yet. Version 0.1 has one coder. A human second coder on every extreme (every stored 0 or 4) is a gate for a citable tag (`bench gates`); agreement is logged in `data/coding/second-coder.csv` and shown on the status page. The full population follows by v0.2.

## Rule

If a curator holds a financial interest in an evaluator or a lab, the assessments of that evaluator, and of evaluators whose scores turn mainly on that lab, are marked in their rationale so readers can weigh the interest, and are open to public correction through the contribution path. Under this rule the public shareholdings in Google and Meta are a financial interest in two labs in the ledger; the evaluators with confirmed ledger ties to those labs (Epoch, Scale, MLCommons) carry the note in their rationales.
