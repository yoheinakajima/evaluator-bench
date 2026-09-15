# Review 2: UI pass with rendered screenshots

14 Sep 2026, v0.9. Pages rendered with wkhtmltoimage at 1200 px and 400 px (JavaScript off, so injected rows and the ladder are absent; inline SVG figures and all CSS render). Old WebKit lacks flex and grid `gap`, so some spacing in the renders is tighter than in a current browser; the fixes below are for real defects.

## Fixed

- `.hero` and `.top` set `padding: … 0 …`, which overrode the `.wrap` side padding; on phones the wordmark and the headline touched the left edge. Now padding-top and padding-bottom only.
- Headline font changed to Manrope (700/800, tighter tracking); wordmark 19 px; h1 28 to 44 px instead of 40 to 76; hero padding 22 px; weights panel and section spacing reduced. The first screen now shows the headline, the lede, the weights and the first rows.
- Navigation: single row, horizontally scrollable on small screens, with margin fallbacks; home nav trimmed to Directory, Where we are, Paths, the six type pages, Paper, Contribute, Repo.
- Figures: SVGs carried fixed width and height attributes, so a scaled-down figure left blank space in its box. Attributes dropped; figures scale to the container with a 640 px floor and horizontal scroll.
- Responses plot: the "none" label overlapped the 20-year tick; hollow points moved up and labelled "no rule" at the top right. Paths figure: right column clipped; widened.
- Entity pages on phones: grid children (`.cols`, `.dimrow`, `.detail-grid`) lacked `min-width:0` and long URLs did not break, so the page rendered wider than the viewport. Fixed; dimension rows stack under 600 px; raw URLs break anywhere, titles wrap at word boundaries.
- Ladder: last column widened so its header fits.
- Copy: the graph caption still referred to the removed ledger browser.
- Data: 68 sources seeded from search snippets had no tier or audit status and showed "tier not set, unaudited". Tiers assigned by publisher; status `unaudited` added to the schema for sources cited from snippets and not fetched in full; eleven sources fetched in full marked confirmed.

## Checked, no change

- Banner wraps cleanly at 400 px.
- Index tables scroll horizontally on phones.
- Tooltips reposition inside the viewport; touch writes the text under the figure.
- No element uses a fixed pixel width outside the SVGs.

## Not verifiable here

- Font rendering (Google Fonts blocked in the sandbox; fallbacks rendered).
- JavaScript-injected sections (directory rows, ladder, cases, rubric); their CSS is unchanged from the version checked by DOM tests.
