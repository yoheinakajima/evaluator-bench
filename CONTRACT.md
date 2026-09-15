# CONTRACT

Invariants. `python -m bench verify` enforces them; CI blocks merges that break them. Change the CONTRACT before changing behavior.

1. Every source has an `id`, an `http(s)` URL, and a `retrieved` date. A source nobody cites is an error (C5).
2. Every signal names one evaluator, one dimension, one direction (for or against), a claim, and at least one source id that exists (C2).
3. Every assessment names one evaluator and one dimension, has an integer value 0 to 4 equal to its anchor, a rationale, and at least one signal id on the same evaluator and dimension (C3).
4. Every evaluator has all eight dimensions assessed and at least one signal, a confidence in {high, med, low}, and a type from `data/types.json` (C4).
5. A value of 4 requires at least one `for` signal; a value of 0 requires at least one `against` signal (C6).
6. Scores are never stored in `data/`. They are a projection computed at build time from assessments and presets.
7. `graph/events.jsonl` is generated with a frozen clock and a fixed run id. It is committed. A rebuild on unchanged data must be byte-identical; CI checks this.
8. Signals are append-only in spirit. To retract a claim, add `superseded_by` pointing at the replacing signal rather than deleting, unless the original was a curation error.
9. The seed script `bench/seed_v0.py` is history. Edits go to `data/` directly.
10. Money and roles are rows in `data/ledger/` before they are claims in signals. Rows carry `source_type` and `audit_status`. Rows are never summed across measures. Undisclosed amounts are counted, not valued.
11. A "none found" is a bounded negative in `data/ledger/negatives.csv` naming the corpus, snapshot date, and source. A 4 on funding requires a confirmed negative in a filing or index (C8).
12. `imported` rows satisfy no gate. Promotion to `confirmed` requires a re-fetch by a named person on a date, recorded in an audit file.
13. Every evaluator is an entity in the ledger; nobody is exempt from exposure (C9).
14. A 4 on Funding, Governance, or Personnel requires tier-1 (filing or index) evidence on a cited signal (C10).
15. Dates must be YYYY, YYYY-MM, or YYYY-MM-DD, and no record may be dated after the frozen evidence clock (C11).
16. Every preset's weights cover exactly the eight dimensions and sum to 100 (C12).
17. A `docket`-type source may never carry `audit_status: confirmed` without an independent, signed certificate from review at epistemedia.org by someone other than the drafter; `verify` fails closed (C13).
14. Extremes need live evidence (C14). A value of 0 or 4 requires a non-superseded signal whose sources are all `confirmed`; 1 or 3 requires a signal with a `confirmed` or `unaudited` source. Assessments held at a supportable value carry `evidence_limited: true`. Transfer rows carry a `class` (cash, in_kind, ownership, partnership); population counts of direct lab ties are reported by class, and an acquisition or a no-fee partnership is never reported as lab funding.
