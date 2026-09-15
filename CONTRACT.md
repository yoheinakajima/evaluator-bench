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
