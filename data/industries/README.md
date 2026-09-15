# Dataset B: assurance-regime lifecycles

One file per regime. Fields:

- `milestones[]`: `year`, `kind`, `event`, `source`, and for rule kinds a `strength` 1 to 4; for triggers a `harm` class and a `trigger_criterion`.
- `mechanisms.before` and `mechanisms.now`: who pays (A assessed party, R regulator or state, O party with opposing exposure such as an insurer, Ph philanthropy), who selects the assessor (A, R, O, self), access (shallow, deep, embedded), publication (none, summary, public), oversight of assessors (none, self-reg, regulator).
- `jurisdiction`, `payer`, `access`, `publication`, `ai_analogue`, `status`.

Milestone kinds: voluntary_assurance, trigger, mandate, standards, accreditation, independence_rule, delegation_reform, payer_reform, access_expansion, publication_rule, delegation, payer_shift, rollback.

Strength rubric for rule kinds: 1 disclosure or voluntary text; 2 a standard or private rule; 3 a statutory mandate or accreditation with enforcement; 4 a structural change (separation of functions, rotation, a new body that inspects assessors, payment rerouted, delegation reclaimed).

Trigger criterion, applied before looking at what followed: an incident qualifies if it caused ten or more deaths, losses above one billion dollars, or a documented integrity failure of the assurance itself (fraud, forged or omitted findings, certified product found non-compliant). Incidents that met the criterion and were followed by no rule belong in the dataset too; adding them is the main open task.

Status: seed. Years are spot-checked against secondary sources. Verify each milestone against a primary source before citing.
