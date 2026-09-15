# CONTRACT

Invariants. `python -m bench verify` enforces them; CI blocks merges that break them. Change the CONTRACT before changing behavior. The meaning behind the mechanics is in `RULES.md`.

1. Every source has an `id`, an `http(s)` URL, and a `retrieved` date. A source nobody cites is an error (C5).
2. Every signal names one evaluator, one dimension, one direction (for or against), a claim, and at least one source id that exists (C2).
3. Every assessment names one evaluator and one dimension, has an integer value 0 to 4 equal to its anchor, and at least one signal id on the same evaluator and dimension (C3). A rationale is optional prose; the derivation is generated.
4. Every evaluator has all eight dimensions assessed and at least one signal, a confidence in {high, med, low}, a type from `data/types.json`, and a dissent (the strongest case that the weakest dimension should be one notch lower, and one notch higher). A hypothetical composite is never an evaluator (C4).
5. A value of 4 requires at least one `for` signal; a value of 0 requires at least one `against` signal (C6).
6. Scores are never stored in `data/`. They are a projection computed at build time from assessments and presets, under every evidence policy, with a band and a coverage count.
7. `graph/events.jsonl` is generated with a frozen clock and a fixed run id. It is committed. A rebuild on unchanged data must be byte-identical; CI checks this.
8. Signals are append-only in spirit. To retract a claim, add `superseded_by` pointing at the replacing signal rather than deleting, unless the original was a curation error.
9. The seed script `bench/seed_v0.py` and the migration `bench/apply_bounds.py` are history. Edits go to `data/` directly.
10. Money and roles are rows in `data/ledger/` before they are claims in signals. Rows carry `source_type` and `audit_status`. Rows are never summed across measures. Undisclosed amounts are counted, not valued.
11. A "none found" is a bounded negative in `data/ledger/negatives.csv` naming the corpus, snapshot date, and source. A 4 on funding requires a confirmed negative in a filing or index (C8).
12. `imported` rows satisfy no gate. Promotion to `confirmed` requires a re-fetch by a named person on a date, recorded in an audit file.
13. Every evaluator is an entity in the ledger; nobody is exempt from exposure (C9).
14. A 4 on Funding, Governance, or Personnel requires tier-1 (filing or index) evidence on a cited signal (C10).
15. Dates must be YYYY, YYYY-MM, or YYYY-MM-DD, and no record may be dated after the frozen evidence clock (C11).
16. Every preset's weights cover exactly the eight dimensions, sum to 100, and carry a derivation paragraph naming the persona and the instrument the weights follow (C12).
17. A `docket`-type source may never carry `audit_status: confirmed` without an independent, signed certificate from review at epistemedia.org by someone other than the drafter; `verify` fails closed (C13).
18. Evidence status clamps what a signal may set (C14): a signal whose sources are all `confirmed` may set any bound; one with a `confirmed` or `unaudited` source but not all confirmed may set caps no lower than 1 and floors no higher than 3; one whose sources are only `imported` or `unverifiable` supports 2 and nothing else; `differs` and superseded signals support nothing. Transfer rows carry a `class` (cash, in_kind, ownership, partnership); population counts of direct lab ties are reported by class, and an acquisition or a no-fee partnership is never reported as lab funding.
19. Every signal declares a `bound` and the `RULES.md` rule code behind it: an against-signal sets a cap, a for-signal sets a floor, or the bound is null with a `bound_note` naming the rule that makes the signal informational (C22).
20. The stored value of every assessment is the derivation of its signals' bounds under the leads-included policy: the smallest effective cap, or, with no cap, the largest effective floor. Where the largest floor exceeds the smallest cap, the assessment carries a `resolution` naming the rule and the value it decides, and the value lies between the two (C23). The `evidence_limited` flag is the computed held state, never typed (C24).
21. A cap of 0 is effective only with a quoted span from a confirmed source (C15, C17; an against-signal from the organization's own page is an admission against interest). A floor of 4 is effective only with a quoted span (C15) and either a tier-1 or tier-2 source or two independent confirmed sources of which at least one is not self-published (C16). Bounds that fail these tests are held at 1 or 3 and the site says which rule held them.
22. Role is derived from type and the role-incompatibility value under `RULES.md` section 10; a stored role that disagrees is an error, and `list_group`, if stored, must agree (C25).
23. Press sources carry `press_kind` (primary or aggregator); no other source type does (C26).
24. The site's default evidence policy is standard (at least one confirmed source); the leads-included, against-interest, verified-spans, and primary-only policies are computed at every build and selectable by the reader.
25. Every published statistic covers the ranked population; watchlist entries contribute to none.
26. A citable tag requires the gates in `bench/gates.py` to pass: every binding signal has a span, every extreme has a second coder, every ranked organization and named person has been contacted, the default policy is standard and the primary-only view is live, RULES.md is published and every conflict cites a rule, and the homepage carries the byline and the competence chip. `bench release --stage published` refuses otherwise.
