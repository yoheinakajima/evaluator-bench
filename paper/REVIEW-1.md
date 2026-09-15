# Review 1: code and site

14 Sep 2026, pre-release review 1. A read-through of `bench/`, `site/`, `data/`, and the built `dist/` with a link check.

## Found and fixed

- The home page embedded the entire ledger JSON twice (LEDGER and DIST constants) for a browser that had moved to entity pages. Removed; index.html dropped from 616 KB to 549 KB, and the graph, stage, and exposure data it still needs remain inline.
- Index-page tables overflowed on phones. They now scroll horizontally below 900 px.
- No `<meta name="description">` on the home page. Added.
- `README.md` command list and layout section were behind the site split; updated.
- Verify now reports quote coverage (17 of 280 signals carry an exact span) so the gap is visible on every run rather than only in the docket work.

## Found and left, with reasons

- Tooltips are hover-first; on touch, a tap writes the text below the figure. Acceptable; a modal would be better for the graph on phones.
- Pages are regenerated wholesale on every build (198 files). Fine at this size; if the ledger grows past a few thousand rows, generate incrementally.
- `bench review` and `bench audit` need network and, for the model check, an API key; they run in CI and not in the build environment this was written in. Both degrade to a reduced report rather than failing.
- The naive link checker flags eleven JavaScript template strings inside `<script>`; they are not links. Real internal links: 11,007 checked, none broken.

## Data quality notes

- 28 of 68 inflow rows confirmed; 40 remain imported. Every imported row names its origin row id.
- Three evaluators (CAISI, EU AI Office, HAL) sit at funding 3 solely because no confirmed bounded negative exists; the gate is uniform, the readings are provisional, and each open question names the document that restores 4.
- Dataset B years are spot-checked against secondary sources; no milestone has a primary source yet.
- The six dockets pass Epistemedia's validator except the two networked steps. (A self-issued certificate existed at the time of this review; it was removed before v0, and the verifier now rejects any docket source claiming confirmation without independent review.)

## Tests

11 pass: CONTRACT integrity, projection matches data, byte-reproducible event log, provenance on every score/assessment/signal, ledger validity, every evaluator in the ledger, amounts never cross measures, labs at distance zero, every entity has a page, focus mode fades non-neighbours.
