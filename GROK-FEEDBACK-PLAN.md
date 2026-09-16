# Grok feedback — fix plan (status as of merge, 2026-09-15)

Grok's evening review (2026-09-15) was accepted as the final pre-release audit. All phases were implemented and merged into `main` (now `f03e43f`) on 2026-09-15. The file was reconstructed on 2026-09-16 after the original working copy was lost; statuses reflect the merged state.

## Phase A — product/build fixes (PR #15, merged `9ce7881`)
1. One epistemology: entity pages hid composite numbers behind "Reveal weighted scores"; numbers live only in `data-score` attributes. ✔
2. "Clear" legend: "Clear means no disqualifying conflict is on file, not a pass" everywhere the chip appears. ✔
3. Score-button state bug: did not reproduce in repo code (stale-deploy artifact); both reveal controls exercised. ✔
4. Sparkline/dimension-bar legend added. ✔
5. Denominator frozen at single live definition: 6 of 192 (ranked orgs × 8 dims); "202 of 208" was never in the repo. ✔
6. Lab derivation shortened to persona line; AEF-1/SB 315 moved to Method. ✔
7. Banner line: "the re-derivation pass did not move values; earlier v0.1 rules and scope decisions did." ✔

## Phase B — content drift and status (PR #16, merged `752efee`)
1. Paper §5.5 corrected to repo-computed values: 164 for / 166 against; 287 of 330 spans; 234 sources (107 self, 66 filings/indexes); primary-only 167; held assessments 6 (ranked, standard policy); mean bound 0.06; funding ≤2: 10 of 24. `bench/paper_stats.py` + `tests/test_paper_stats.py` guard against drift. ✔
2. Status Population card: 45 checked (23 out, 14 in-scope candidates, 8 unclear), linking to full exclusions table; exclusions page added to nav. ✔
3. Gates dashboard: explicit live PASS/FAIL from `bench.gates.gates()`; `tests/test_gates.py`. ✔
4. 51 vs 54 reconciled: 51 in the gate (24 ranked orgs, 27 named people); log lists 54, incl. 3 non-ranked orgs outside the gate (epoch, hal, hfoai). ✔
5. HTTP 314/44 vs HTTPS 330/287: stale Pages deploy, not a repo bug; fixed by the post-merge Pages rebuild. ✔

## Phase C — homepage compaction (PR #17, merged `d02bf45`)
`/` is now controls + three compact lists (one row per org: name, band chip, weakest dimension, "Open →") + watchlist/out-of-scope in the same style. Full cards live only on entity pages. ✔

## Phase D — deployment
Stale HTTP was Pages' HTTP cache of a pre-launch deploy; `http://evaluatorbench.com/status/` already 301-redirects to HTTPS (Enforce HTTPS on). Post-merge Pages rebuild completed successfully — nothing further. ✔

## Phase E — research/judgment
1. **METR funding (PR #19, merged `f03e43f`):** `funding_tension` paragraph on the default card — F.13 case for 3 plus full against-case. **Value stays 3; the 2-vs-3 flip is the curator's call.** Curator's decision, 2026-09-15: keep 3 — no METR-specific rule change; the value drops only if new evidence arrives. Item closed.
2. **Shared funders:** public-record check done (see summary below). Approved wording applied to DISCLOSURE.md + Method disclosure card in PR #20 (draft, 2026-09-15) — approve to merge.
3. **Second coding (PR #18, merged `31cbeca`):** all 15 un-second-coded 0/4 extremes independently verified; gate now 15/15. ✔
4. **Byline:** "Their review is recorded in paper/audits/ as part of the independence record, not as assurance of correctness" on homepage, Method disclosure card, DISCLOSURE.md. ✔

### Shared-funder research summary (2026-09-15, read-only)
- Untapped Capital public portfolio vs every evaluator funder in `data/ledger/` (Coefficient, Good Ventures, SFF, Audacious, OpenAI Foundation, AI Safety Fund, Schmidt Sciences): **zero overlap found**.
- Ledger `sff` is Survival and Flourishing Fund (both interpretations checked).
- One proximity (not a finding): only publicly named Untapped LP (Anne Wojcicki Foundation, per PitchBook) is a partner on Audacious Project's About page; Audacious funds RAND/METR's Canary — no record connects them.
- Genuinely uncheckable without the curator: full LP roster (private), individual LPs' affiliations, OpenAI Foundation's full grantee list (not public).
- Proposed disclosure (pending curator approval): "no overlap found in public records (checked 2026-09-15)… the full limited-partner roster is private, so overlap through undisclosed LPs remains unchecked."

## Remaining open items (owner's call; out of scope for agents)
1. ~~METR funding 2-vs-3 flip~~ — closed 2026-09-15: keep 3, no METR-specific rule.
2. Shared-funder disclosure wording — applied in PR #20 (draft); approve to merge.
3. Binding-spans gate: 8 signals without spans (PR #21, draft, shrank 21 -> 8). Assessment corrections in #21: cais.A 1->0, humane.A 1->0, rand.R 2->3 (rand.04 superseded by rand.04b — claim was contradicted by rand.org). rand.08 quote_source corrected to rand-integrity (was misattributed to rand-aef); rand X stays held at 3, now unevidenced under standard policy. redwood.08 needs a primary source (current source doesn't support the claim).
4. Outreach gate: 0/51 contacted — do not email without explicit instruction.
5. Batch 3 (deferred), Recipe D candidate work (unauthorized).

## Follow-up (2026-09-15): binding spans round 2, disclosure move, merge-state check
- **Binding spans:** saferai.07 resolved (tracker-frame span, verified verbatim from a live fetch of safer-ai.org this run). 7 remain unresolvable this run: equistamp.07, farai.07, farai.11 (TED notice 864574 and longtermwiki E138 pages could not be fetched; TED source URL is the homepage, not the notice URL — retry should search TED for notice "864574-2025"), msft.07 (Learn landing page has no scope text; retry the "Lessons from red teaming 100 generative AI products" paper), palisade.09 (archived OP award pages not fetched; use the two archived award URLs, do not use coefficientgiving.org), redwood.08 (no primary source fetched; best lead is the genuine redwoodresearch/redwood-control-arena README), saferai.04 (homepage fetched; ratings methodology pages not fetched). Nothing fabricated.
- **New gate finding:** "Every extreme has a second coder" now FAILS — 15 of 17, missing cais.A and humane.A (extreme set grew after the rand.08 reclassification).
- **Disclosure move:** homepage byline shortened to the curator + four-model-review conflict-log sentence; holdings / shared-funders / full-disclosure block moved to a "Disclosures" section below the evaluator lists, above the footer. Method page card unchanged.
- **Merge-state check (workstream 2):** verify ok, build ok, 60/60 pytest on origin/main; committed dist/ matches a clean rebuild exactly (only expected template-driven diff). Repair-commit staleness resolved.
- Paper §5.5 drift guard did its job: adding the saferai.07 span moved quoted-span count 300→301; paper/draft.md updated, tests green.
