# Annual update paper

Plan, 14 Sep 2026.

Evaluator Bench is a living dataset; the paper is a dated reading of it. Each year (or sooner if the record moves a lot), publish an update built from the diff between two tagged commits.

## Inputs

- `python -m bench changelog --since <last tag> --until <this tag>`: evaluators added, assessment changes with rationale, score movement per preset, sources added by tier and audit status, ledger rows added and promoted, milestones added, dockets added.
- `paper/audits/AUDIT-*.md` for the period: what was re-derived, what differed.
- `paper/OPEN-QUESTIONS.md`: which questions closed and what closed them.
- Reviewed dockets and certificates issued in the period.
- Right-of-reply responses filed as signals.

## Shape

1. What moved and why: every score change, each traced to the signal and source that moved it. No change without a row.
2. What was confirmed: imported rows promoted to confirmed; the share of the ledger now re-derived.
3. What the population looks like now: the exposure matrix, funder concentration, second-hop coverage, compared with the prior year.
4. Where AI sits on the ladder and the path: any new stage reached, any new trigger, any new rule and its strength.
5. What contributors found: PRs merged, what the machine review caught, what it missed.
6. What is still open, with what would close each item.

## Rules

- The update is generated from the repository at two commit hashes named in the paper. Anyone can regenerate the tables.
- No score changes are made for the paper; the paper reports the year's changes as they were merged.
- Evaluators whose scores moved are sent the relevant rows before publication and their replies are filed.
- If nothing material changed, publish a short note saying so, with the confirmation counts.

## Cadence

Tag `v<year>.<n>` at each publication. First update targeted for September 2027, or earlier if the embedded-evaluator contracts, SB 315 audit rules, or a new incident change the record substantially.
