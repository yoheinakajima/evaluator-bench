# Unresolved after the 15 Sep 2026 verification run

Handoff list from the verification agent. Two categories: (A) attempted, and the cited page does not support the recorded figure; these need a better source or a different route to the primary document. (B) not attempted because the fetch route failed during the run; a later pass should be able to do these. Statuses below are as of the run; several were resolved afterwards (T13 to unaudited on two 990 extracts; T07 confirmed against Epoch's own list; T22 confirmed on SecureBio's post) and the ledger is authoritative.

## A1. Ledger transfers marked unverifiable (16 rows, after grok pass)
Each was re-fetched; the cited page does not support the recorded figure/relationship.
Resolved in the grok pass (see AUDIT-5): T22, T36, T41, T46, T48, T52, T54, T56, T60, T63 confirmed; T07 differs.
A better agent could look for the primary source (990 filings, grant databases, press releases) for:
- **T01** coefficient -> arc | grant | 1515000 | cited: https://coefficientgiving.org/ | Homepage states aggregate grantmaking only ('over $7 billion in grants since 2014'); no per-grantee figures.
- **T02** coefficient -> rand | grant | 10000000 | cited: https://coefficientgiving.org/grants/ai-evaluation-and-testing/ | Per-award page exists but figure unverified in fetch.
- **T03** coefficient -> far-ai | grant | 59347676 | cited: https://www.longtermwiki.com/wiki/E138 | Tier-2 wiki lists components (~$28.675M, $6.65M, $2.16M, $1.7M + $12M regrant); $59.3M cumulative not confirmed.
- **T04** coefficient -> redwood | grant | 63086000 | cited: https://thenextweb.com/news/coefficient-giving-ai-safety-funding-ipo-correlation | One $36.566M award confirmed (= T73); $63.1M cumulative unconfirmed.
- **T05** coefficient -> longview | grant | 26251590 | cited: https://coefficientgiving.org/ | Homepage aggregate only.
- **T06** coefficient -> constellation | grant | 22950000 | cited: https://coefficientgiving.org/ | Leads: coefficientgiving.org/grants/constellation-general-support/ ($16.75M, 2024-06-19) and a $3M coworking grant (2023-06-06) — unfetched.
- **T13** arc -> metr | transfer | 4553935 | cited: ProPublica ARC org page | Officer/compensation tables only; no Schedule I in HTML. Needs the 990 PDF.
- **T14** vanguard-charitable -> metr | daf_grant | 4000000 | cited: ProPublica Vanguard org page | Filings/compensation only; no METR mention. Needs the 990 PDF.
- **T15** founders-pledge -> metr | daf_grant | 184000 | cited: https://projects.propublica.org/nonprofits/ | Generic landing page. founderspledge.com/research/frontier-ai-grantmaking is live but shows no METR $184k.
- **T16** svcf -> metr | daf_grant | 20000 | cited: ProPublica SVCF org page | Confirms SVCF operates a DAF but lists no grantees. Needs the 990 PDF.
- **T33** sff -> apollo | recommendation | 1133500 | cited: https://survivalandflourishing.fund/recommendations | Round totals only. Components: 2024 Apollo $251k via Rethink Priorities; 2023-H2 Apollo $490k — need year pages.
- **T39** sff -> redwood | recommendation | 2372000 | cited: https://survivalandflourishing.fund/recommendations | Round totals only. Component: 2023-H1 Redwood $1,098,000 — need year page.
- **T43** sff -> far-ai | recommendation | 5593577 | cited: https://survivalandflourishing.fund/recommendations | Round totals only. Component: 2025 FAR $919k (= T67) — need year pages.
- **T55** yc -> andon | investment | 500000 | cited: https://pitchbook.com/profiles/company/541549-09 | PitchBook paywalled; no YC/Andon announcement found.
- **T58** coefficient -> rand | grant | 76955751 | cited: https://coefficientgiving.org/ | Homepage aggregate only.
- **T59** us-gov -> rand | contract | 488777692 | cited: ProPublica RAND org page | Nonprofit profile; no $488M figure. Needs the 990 PDF or contract record.

## A2. Sources fetched but quote span not found on cited page (needs re-pointing or re-wording)
Resolved in the grok pass: sequoia-irregular, rand-audacious-2024, ifp-caisi-funding, openai-kolter-board, averi-funding, decoder-epoch, alignment-project-about, openai-alignment-project. Remaining:
- **op-palisade** (https://www.openphilanthropy.org/grants/) — signals: palisade.11
- **op-constellation** (https://www.openphilanthropy.org/grants/constellation-programmatic-act) — signals: metr.21
- **op-longview** (https://www.openphilanthropy.org/grants/longview-philanthropy-nuclear-security-g) — signals: (check)
- **op-far-general-support** (https://www.openphilanthropy.org/grants/far-ai-general-support/) — signals: (check)
- **instrumentl-arc-990** (https://www.instrumentl.com/990-report/alignment-research-center) — signals: metr.21 — page renders generic 990 explainer; figures JS-gated. Needs the 990 PDF.
- **securebio-oaif** (EA Forum) — signals: (5 assessment anchors) — never fetched.
- **csa-caisi** (Cloud Security Alliance) — signals: (4 assessment anchors) — never fetched.
- **coefficient-index** (https://coefficientgiving.org/grants/) — signals: (3 assessment anchors) — never fetched.
- **dealroom-grayswan** (Dealroom) — paywall likely.
- **transluce-about**, **transluce-policy** (3 quotes), **metr-about**, **metr-team**, **propublica-metr-arc** — never fetched.
- **longtermwiki-far** (E138): fetch tool hard-fails on this URL specifically. Needs alternate route.

## A3. Special cases
- **metr-donor-rule-history**: URL is a Wayback wildcard (web.archive.org/web/2025*/metr.org/about); archive.org CDX returned 503. Needs a concrete snapshot timestamp. Sole cite for metr.14 (1 assessment anchor).
- **ms-redteam**: Microsoft Security blog topic URL 404s; needs a current post slug. Sole cite for msft.02–msft.08 (7 assessment anchors).
- **evaluators-ledger**: cited blob path 404s (file moved in kevinnbass/metr-money-figure). Import origin, not a confirm. Cited by 20 assessment anchors — the single biggest weak-anchor driver.
- **ted-864574-notice**: TED renders a JS shell in static fetch; grok reported the lot values but I could not independently re-fetch. Needs JS-capable fetch or the notice PDF.
- **openai-kolter-board vs kolter-bio**: resolved — bio says 'chairs the Safety and Security Committee', OpenAI page says he 'joins' it. Signal grayswan.01 now cites kolter-bio for the chair claim and openai-kolter-board for the board-seat half. Curator call recorded in AUDIT-5.
- **bloomberg-nvidia-anthropic**: resolved — record deleted; hfoai.10 re-pointed at fortune-hf-nvidia + tnw-hf-nvidia with the claim trimmed to the acquisition.

## B. Never attempted by me (a better agent should try these)
The grok pass opened most of the original 41. These remain unfetched by any agent:
- **coefficient-index** (https://coefficientgiving.org/grants/) — 3 assessment anchors depend on it.
- **csa-caisi** (Cloud Security Alliance) — 4 assessment anchors.
- **securebio-oaif** (EA Forum) — 5 assessment anchors.
- **dealroom-grayswan** (Dealroom) — likely paywalled.
- **op-palisade**, **op-constellation**, **op-longview**, **op-far-general-support** (Open Philanthropy grant pages).
- **transluce-about**, **transluce-policy**, **metr-about**, **metr-team**, **propublica-metr-arc**.
- **longtermwiki-far** (E138): fetch hard-fails; needs alternate route.
- **T22** (SecureBio X post): grok-reported $17.2M; X not attempted by me.
- **T54** (TNW Hugging Face/Nvidia): grok-reported $12.93bn; my browser task failed.

## Phase-2 note (assessment anchors, 2026-09-15, updated after grok pass)
Structural audit of all 224 assessments vs their cited signals (no browser needed):
- 38 anchors cite signals whose sources are not yet confirmed (was 85 before the grok pass).
- Top culprits: evaluators-ledger (20 cites — the import path moved; dead cite), ms-redteam (7 cites — Microsoft topic URL 404s), securebio-oaif (5), csa-caisi (4), coefficient-index (3).
- No assessment cites a nonexistent signal. No anchor rests on a source proven false.
