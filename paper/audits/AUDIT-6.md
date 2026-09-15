# AUDIT-6: the v0.1 evidence pass, 15 September 2026

Scope: every signal in `data/signals/` (314 at v0, 357 after this pass), every source cited by one (122 at v0, 194 after), and the migration of every value to the bounds model in `RULES.md`. Work was done by Claude in six parallel passes under the curator's instructions, with every quoted span checked as an exact substring of the text `bench.review.fetch_text` returns (or a documented fallback), and merged by `bench/apply_bounds.py` and `leads/post_apply.py`. Raw pass outputs are in `leads/bounds/`, `leads/quote-audit.json`, `leads/primary-sources.json`, and `leads/exclusions.json`.

## Quote audit of the v0 spans (43 signals)

- 36 found verbatim on the cited page.
- 6 not on the page as cited, replaced with spans that are: `apollo.13` (the page uses curly quotes), `averi.10` (recusal wording changed to "until two years after his October 2024 departure"), `farai.12` and `metr.21` and `palisade.11` (the Open Philanthropy grant pages now redirect to a generic coefficientgiving.org page that returns 403; spans moved to the organizations' own pages, Instrumentl, or the imported ledger).
- 1 blocked: `grayswan.02` on forbes.com sits behind a bot wall for every fetch method; the span is verbatim in the Wayback capture recorded in the source's `archive` field, and a Forbes Australia mirror was added as a confirmed second source.
- `securebio.01`: the v0 quote ("OpenAI PBC covered SecureBio's costs for the GPT 5.5 evaluation") is not on the cited blog post. Two passes disagreed on the remedy: one found the sentence verbatim in a SecureBio staff post on the EA Forum, now cited; the other found the same fact in the GPT-6 Astra and GPT-5.6 Sol full reports (PDF), which carry "SecureBio received compensation from OpenAI limited to covering the costs of this assessment". The EA Forum source is cited because the CI normalizer can read it; the PDF finding is recorded here.

## Source status changes

- `ms-redteam`, `ms-redteam-100`: unaudited to confirmed. Re-fetched 2026-09-15; both pages load and support their claims (the Learn hub with PyRIT; the Security Blog post stating the team was formed in 2018 and has red-teamed more than 100 products).
- `gdm-gemini-testing`: confirmed to unverifiable. The URL resolves to the deepmind.google homepage, which does not mention Dreadnode. Dreadnode's claims are now sourced to Google's Gemini 3 launch post, Time, SecurityWeek, Dreadnode's Series A page, and the AIRTBench paper and repository.
- `marktechpost-pace`, `dwt-sb315`: source type self to press (aggregator). Every press source now carries `press_kind`.
- Every self-published source now carries `self_of`, the entity whose statement it is, so a lab's or funder's statement about an evaluator is not treated as that evaluator's self-report under the against-interest policy or the second-source test.
- Removed: the six SB 315 commentary sources cited only by the hypothetical Big Four composite, with the composite itself (RULES 11).

## Primary sources for the September 2026 pledges

- `anthropic-pace-frontier` (darioamodei.com, 2026-09-12) and `anthropic-amodei-x-pace-frontier`: employee-like access, METR named, publication without editorial control, redaction limited to what cannot be published for security reasons. No anthropic.com post existed as of 2026-09-15.
- `openai-altman-embedded-pledge` (x.com/sama, 2026-09-12): "we will do the same" on employee-like access; no evaluator named, no publication commitment. No openai.com post matched on or before the evidence clock; the November 2025 external-testing page describes review for confidentiality and accuracy before publication.
- The paper's opening paragraph now states the two commitments separately.

## The bounds pass

- 357 signals carry a bound and a rule code; 9 are informational (null bound with a note under RULES 9, A.3, or F.11).
- 46 signals added where a rule needed a fact the record already held on another dimension, or where a rule-required cap had no signal (lab-investor-linked funders under F.6, paid consultation under X.3, co-authoring under S.6, lab-set windows under S.1).
- 78 sources added and six composite-only sources removed, for a net increase of 72: filings (ProPublica 990s for METR, Palisade, Redwood, RAND, SecureBio, HAL's host), statutory texts (AI Act Article 92; 18 USC 207 and 208; EU Staff Regulations), organizations' own policy pages (METR's conflict-of-interest policy, SecureBio's conflict policy and principles, UK AISI's Inspect page), and named-outlet press as second sources for floors of 4.
- 94 stored values moved when the rules were applied. The largest systematic movers: governance and personnel fell where only legal form or "no lab roles found" was on record (G.1, P.6); access fell where the deepest documented engagement was a pre-release API or a released model (A.1); publication fell where "publishes" was the only fact (R.7); scope 4s became 3s without incident or sign-off rights (S.5); several 4s on methods and role incompatibility became 3s for lack of a second source (C16).
- 12 conflicts between a floor and a cap, each resolved by a named rule on the card: caisi.X, dreadnode.M, epoch.F, epoch.X, farai.X, humane.X, metr.P, nemesys.F, saferai.X, securebio.F, securebio.X, transluce.F.
- 8 assessments held at a supportable anchor by C14, C15, or C16 (listed by `python -m bench verify`).
- 1 assessment unevidenced even with leads included: Redwood personnel, whose only signal recorded a co-authoring fact that belongs to scope.
- Roles re-derived: Andon Labs and SecureBio to vendor (RULES 10).
- Open questions about named people rewritten as document requests (RULES 12); reply packets generated for every ranked organization and every named person (`data/outreach-log.csv`; none sent yet).

## Rules amended during the pass

Gaps the passes hit were closed in `RULES.md` before the merge and the files rebuilt against the amended text: F.4b (grants from a lab's owner), F.11 (in-kind without a dependency statement), R.6 (funder approval over disclosure), R.7 ("publishes" alone), X.8 (undisclosed earned revenue), section 9 (mis-dimensioned facts; the statutory carve-out for public bodies), X.2 (the evaluation fee itself is scored on funding, not role incompatibility).

## Follow-ups

- PDF sources: `metr-coi-policy`, the SecureBio full reports, and several filings are PDFs. `bench review` now reads them when `pdftotext` is installed; CI does not have it yet, so those spans report as not checkable there.
- URLs to repoint: `metr-team` (redirects to a stub; metr.org/about carries the roster), `ted-864574` (the TED homepage; the notice itself is JavaScript-only), the four openphilanthropy.org grant pages (redirect to a generic page; Wayback captures recorded where found).
- Pages behind bot walls for every method: forbes.com, rand.org (intermittent), premieralts.com, dealroom.co, the Wayback JS shell for `metr-donor-rule-history`.
- `python -m bench review --all` over the whole corpus (309 quoted signals, every cited page fetched, `pdftotext` available): 303 spans found verbatim on a cited page, 6 not found. Of the six: `andon.09` was a transient PitchBook refusal (found on re-fetch); `farai.15`, `farai.16` and `metr.21` were re-spanned to sentences that are on the page today; `palisade.11` and `saferai.09` quoted the imported ledger through its GitHub blob page, which the fetcher cannot read, so the source now points at the raw file and carries its true status, imported. Fetch failures by host: coefficientgiving.org (4), forbes.com (3), premieralts.com (2), axios, the-decoder, pitchbook, openai.com, dealroom, aiwiki (1 each). Report: `paper/audits/REVIEW-ALL-2026-09-15.md`; the reviewer now prints one verdict per signal.
