# RULES: how a signal becomes a value

Version 0.1, 15 September 2026. These rules are written before they are applied and are applied to every organization the same way. A value on a dimension is not a curator's impression of the file; it is the tightest admissible cap (from evidence against) or, failing any cap, the highest admissible floor (from evidence for), where every signal names the anchor it supports under the rule that says so. Where a floor and a cap disagree, the assessment carries a written resolution naming the rule that decides it, and the disagreement stays on the card.

`python -m bench verify` enforces the mechanics (CONTRACT C22 to C25). This file is the meaning. Change the rule before changing a value.

## 0. Mechanics

- **Bounds.** Every signal carries `bound`: an against-signal sets a cap (`{"cap": n}`), a for-signal sets a floor (`{"floor": n}`), and either may be `null` when the signal is informational under a rule below (say which rule in `bound_note`). The anchor texts in `data/dimensions.json` are the lookup table; the rule numbers below are the tie-breaks.
- **Derivation.** For one assessment under one evidence policy, take the admissible non-superseded signals. If any cap exists, the value is the smallest cap. Otherwise the value is the largest floor. No admissible signal: the value is unevidenced under that policy and renders as a dash, never as a number.
- **Conflict.** If the largest admissible floor exceeds the smallest admissible cap, the build fails unless the assessment has a `resolution` naming the rule that decides, and the stored value lies between the two. The conflict is shown on the card.
- **Evidence status clamps bounds.** A signal whose sources are all `confirmed` may set any bound. A signal with a `confirmed` or `unaudited` source but not all confirmed may set caps no lower than 1 and floors no higher than 3. A signal whose sources are only `imported` or `unverifiable` supports 2 and nothing else. `differs` and superseded signals support nothing. This is CONTRACT C14 restated as a clamp.
- **Extremes need spans and second sources.** A cap of 0 is effective only if the signal carries a quoted span from a confirmed source (C15, C17; an against-signal from the organization's own page is an admission against interest and satisfies the source test on its own). A floor of 4 is effective only if the signal carries a quoted span (C15) and either cites a provenance-1 or provenance-2 source or cites two independent sources of which at least one is not self-published (C16). A bound that fails these tests is clamped to 1 or 3 and the card says which rule held it.
- **Evidence policies** decide admissibility (see `bench/policy.py`): leads included (everything not quarantined), standard (at least one confirmed source; the default), against interest (standard, and self-published sources count only for signals against the organization), verified spans (standard with a quoted span), primary only (provenance 1 or 2, confirmed, with a span).
- **Stored value.** The `value` in `data/assessments/` is the derivation under the leads-included policy, the curator's reading of the full record. The site's default is the standard policy. Both are computed at build time; the verifier fails if the stored value disagrees with its derivation.
- **Bands.** Independence has floors. An evidenced 0 on funding, governance, personnel, role incompatibility, scope control, or publication rights is a disqualifying floor; an evidenced 1 on one of those is a conditional floor; otherwise the organization is clear. Access depth and method transparency count in the weighted number and never place an organization in a band: a 0 there means the labs have not let it in, or it has not published its methods, not that it is compromised (D-002). The band sorts first; the number, shown only after the reader chooses weights (D-003), ranks within it.

## 1. Funding (F)

Anchors: 0 owned or controlled by a frontier developer or a lab investor (a stake of 20% or more, or a business unit); 1 material revenue or investment from evaluated labs or their investors; 2 labs pay per engagement, otherwise diversified; 3 mostly philanthropic or public money, some lab-linked pooled funds; 4 no lab money, diversified philanthropic or public funding, disclosed and bounded.

- **F.1 Ownership.** A frontier developer, or an investor in a frontier developer, holding 20% or more of the evaluator's equity, voting or not, caps at 0. Twenty percent is the significant-influence threshold in equity accounting and the level at which financial-audit independence rules treat an interest as controlling. A business unit of a developer is 0.
- **F.2 In-kind.** Compute, credits, tokens, and pre-release access consumed in evaluating a lab's own model are the substrate of the evaluation, not a payment (D-004). They never bound funding, never enter the hop buckets of the money matrix, and are not counted as a direct lab tie; they stay in the ledger as `in_kind` rows. Only general operating compute or credits that fund the organization's work beyond the evaluation count as lab money, and only when the amount is disclosed and exceeds 5% of annual operating cost (cap 2) or is undisclosed and the evaluator itself says its operations depend on it (cap 3). In-kind never caps below 2 on its own.
- **F.3 Fees.** Labs paying per engagement caps at 2. If a published policy caps lab revenue at 10% or less of annual revenue, charges market rates, and retains publication rights, the cap is 3 instead.
- **F.4 Lab investors.** A material investment from a lab, or from a fund that has invested in a frontier developer, caps at 1. Material means a priced round in which that fund led or co-led, or a stake of 5% or more.
- **F.4b Owners of labs.** A grant or investment from an entity that owns 20% or more of a frontier developer (a lab's foundation, parent, or controlling shareholder) is lab-linked money under F.4 whether or not it is restricted to a division. A documented firewall and a public disclosure are recorded on the card and lift nothing, as financial-audit affiliate rules treat fees from a client's affiliate. Material means 5% or more of annual revenue in the year received.
- **F.5 Material revenue.** Lab revenue that is the organization's principal revenue (50% or more, or the only revenue disclosed, or "every major lab" with no other base named) caps at 1. Per-engagement lab fees beside a disclosed non-lab base cap at 2 (F.3).
- **F.6 Pooled and donor-advised money.** Grants through pooled funds, donor-advised funds, or funder collectives whose underlying donors are not public cap at 3. Grants from a funder whose principal is an investor in a frontier developer cap at 3. This is the "some lab-linked pooled funds" of anchor 3, and it is the ceiling for most philanthropically funded evaluators until donors are named and a bounded negative is confirmed.
- **F.7 Personal donations from lab employees.** Disclosed and at or below 10% of annual revenue: cap 3. Above 10%: cap 2. Undisclosed: no bound (nothing to score), but a policy that permits them caps at 3.
- **F.8 Donor-rule age.** A no-lab-money rule younger than 24 months, or amended more than once in any 24-month window, floors at most 3.
- **F.9 Public bodies.** Public funding floors at 3. A 4 requires a confirmed bounded negative in a filing or index (C8) and no material lab in-kind under F.2. Administering a grant pool that includes lab money caps at 3.
- **F.10 Undisclosed structure.** A private company whose capital structure is undisclosed caps at 3; undisclosed structure and undisclosed client base caps at 2.
- **F.11 Evaluation credits and undisclosed in-kind.** Credits or access used for the evaluation itself, and any in-kind whose amount is undisclosed and which the evaluator does not describe as operating support: informational (`bound: null`), recorded on the access mechanism instead.
- **F.12 Four.** A 4 requires a confirmed bounded negative (C8), a tier-1 source on a cited signal (C10), a quoted span, and a second independent source (C16).
- **F.13 Partial bounded negatives.** Confirmed bounded negatives from primary filings that cover some, but not all, of an organization's disclosed or plausible funder base are evidence toward independence and float the funding value to a floor of 3; they do not by themselves satisfy F.12's requirement for a 4, which needs a bounded negative covering the full disclosed base.

## 2. Governance (G)

Anchors: 0 unit or subsidiary of a lab or a lab's investor; 1 private for-profit with no published conflict-of-interest policy; 2 for-profit or public benefit corporation with a published conflict policy; 3 nonprofit or public body with a conflict policy; 4 nonprofit or public body with a published conflict policy, an independent board, and external review.

- **G.1 Legal form alone.** "Nonprofit", "academic", or "public body" with no published conflict policy floors at 2, not 3. Anchor 3 requires the policy.
- **G.2 What counts as a conflict policy.** A published policy floors at 3 (nonprofit or public body) or 2 (for-profit or PBC) only if it names at least two of: recusal for financial interests, no outcome-contingent fees, no investments or side grants from evaluated labs, disclosure of lab-linked revenue. Statutory civil-service conflict rules count for a public body.
- **G.3 Lab-investor money in a round.** Participation by a fund that has invested in a frontier developer caps at 2 even with mission board seats.
- **G.4 Member-governed consortia** whose members include the labs being benchmarked cap at 2.
- **G.5 Political steerability.** A public body whose leadership or mandate changed more than once in twelve months caps at 3.
- **G.6 Ownership** at 20% or more by a lab or a lab investor is 0 (same threshold as F.1).
- **G.7 Four** requires tier-1 evidence of an independent board and of external review.
- **G.8 Undisclosed board composition.** Where a governing body's structure is disclosed (mission seats, a stated seat count, a first appointee) but the full membership is not published, caps at 3; a 4 needs the whole board named (G.7).

## 3. Personnel (P)

Anchors: 0 leaders hold governance roles at an evaluated lab with no recusal; 1 leaders hold equity or advisory roles at labs, informal recusal; 2 frequent two-way hiring, recusal on request; 3 recusal policy and disclosure of lab ties; 4 cooling-off periods, disclosed ties, no equity in labs.

- **P.1 Lab board or committee seats.** A founder, executive, or director holding a board or committee seat at an evaluated lab caps at 1 with a personal recusal and at 0 without one.
- **P.2 Advisory roles.** An executive or director advising an evaluated lab caps at 1.
- **P.3 Two-way hiring.** Documented hiring from, or departures to, evaluated labs without a cooling-off rule caps at 2. An organizational cooling-off policy or a statutory post-employment rule for the body's staff lifts the cap.
- **P.4 Seats one hop from a lab.** A board member or advisor who is a partner at a lab investor, a founder of a lab contractor, or an employee of a lab caps at 2 regardless of recusal.
- **P.5 Recusal policy.** A published mandatory recusal rule plus disclosure of individual lab ties floors at 3.
- **P.6 Absence of evidence.** "No lab roles found" floors at 2, not 3. A 3 needs the policy in P.5.
- **P.7 Employees of a lab** (a first-party team) or leadership that moved to a lab under an ownership transaction: 0 or 1 by P.1.
- **P.8 Four** requires a cooling-off rule, disclosed ties, and no equity, with tier-1 evidence (C10).

## 4. Access depth, lab-granted (A)

Anchors: 0 public API only; 1 pre-release API with safeguards on; 2 pre-release with safeguards off or extended time; 3 helpful-only or weights-level access, chain of thought, logs, on-site; 4 embedded, training-time, or incident access.

- **A.1 Score what was granted.** The deepest documented engagement sets the floor. Access is recorded as revocable unless A.2 applies; the mechanism tag on the card says so.
- **A.2 Enforceable access.** Access resting on statute, regulation, or a court-enforceable agreement floors at 3 even if not yet exercised, and the card tags it statutory.
- **A.3 Voluntary access.** "The lab can decline to renew" is recorded as a mechanism, not as a cap; it does not lower the value by itself.
- **A.4 Government agreements** (memoranda, testing agreements, classified work): 3.
- **A.5 Embedded, on-site, or incident access:** 4.
- **A.6 No engagement yet:** 0.

## 5. Scope control (S)

Anchors: 0 lab defines tasks and can decline findings; 1 lab defines scope, evaluator picks methods; 2 scope negotiated per engagement; 3 evaluator sets scope and can add questions; 4 evaluator sets scope, can investigate incidents, can refuse sign-off.

- **S.1 Lab-set window or excluded questions** in the most recent major engagement caps at 3.
- **S.2 Cannot add questions:** cap 2.
- **S.3 Regulator as client** setting scope by tender or contract: 3.
- **S.4 Statutory scope.** A public body with the legal power to define scope and compel participation: 4. Voluntary memoranda: 3.
- **S.5 Four needs incident or sign-off rights.** Self-directed research with no engagement to refuse floors at 3. A 4 requires documented incident-investigation rights or a documented right to refuse sign-off.
- **S.6 Co-authoring** research with a lab while evaluating it caps at 3.

## 6. Publication rights (R)

Anchors: 0 no publication, or lab approval required; 1 lab-edited summaries only; 2 publishes, lab reviews with broad redaction; 3 publishes, redaction limited to security, redactions disclosed; 4 full editorial control, record of adverse findings, redaction statements.

- **R.1 Security-only redactions** with a public statement of what was redacted floors at 3.
- **R.2 Editorial feedback.** Lab feedback on emphasis, structure, or tone that the evaluator incorporated caps at 3 if the evaluator discloses that it happened and what changed, and at 2 if it does not.
- **R.3 System cards only.** Findings that reach the public only as lab-summarized system-card citations cap at 1; if the organization also publishes its own reports on other work, cap 2.
- **R.4 Statutory non-publication.** A public body is scored on what reaches the public: nothing per model, 1; aggregated trends, 2; reports to a regulator only, 2. The card tags the mechanism statutory so it is not read as a lab holding the pen.
- **R.5 Four.** No lab pre-publication review, plus at least one published finding the evaluated lab did not welcome (a safety failure, a disputed result, a low grade the lab contested). A leaderboard ranking alone is not an adverse finding. Track record is load-bearing here.
- **R.6 Funder approval over disclosure.** A contract or arrangement under which a lab controlled whether or when the evaluator could disclose who funded a benchmark or evaluation caps at 2 for the period it applied and at 3 after the evaluator published a disclosure policy.
- **R.7 "Publishes" alone.** A statement that an organization publishes its results, with no statement about who reviews them before publication, floors at 2. A 3 needs either no lab review or security-only redactions disclosed (R.1).

## 7. Method transparency (M)

Anchors: 0 closed; 1 summaries only; 2 methods described in prose; 3 tasks or code partly open; 4 open code, tasks, reproducible runs, factsheets.

- **M.1 Four** requires open code and open tasks and evidence that a third party has re-run them or that per-evaluation factsheets are published. Open code alone is 3.
- **M.2 Prose-only** methods: 2. Summaries: 1.
- **M.3 A public leaderboard** with open tasks and logs: 3; with third-party re-runs documented: 4.

## 8. Role incompatibility (X)

Anchors: 0 sells defense or monitoring products to evaluated labs; 1 sells products or services other than the evaluation itself to labs or to their customers; 2 consults for labs; 3 tools are open or free to the ecosystem; 4 no commercial products.

- **X.1 Selling the fix.** Guardrails, monitoring, or defense products sold to an evaluated lab: 0. A product sold to unspecified parties in the evaluated ecosystem caps at 2 until a lab customer is documented, and the card carries a document request.
- **X.2 Products and services to labs.** Data, tooling, licensed evaluation products, or deployment services delivered to an evaluated lab for money: 1. The fee for evaluating the lab's own model is not a second role; it is scored on funding (F.3) and does not cap here.
- **X.3 Consulting.** Paid consultation or framework work for a lab: 2. Paid consultation clients listed on a transparency page count.
- **X.4 Free or open tools** used by labs: 3. Labs using a free tool are not customers.
- **X.5 Financial interest.** An evaluator that invests its own funds in evaluated labs caps at 2; in a diversified portfolio that may include listed labs, 3.
- **X.6 Co-producing** a benchmark with a vendor owned by a lab caps at 3.
- **X.7 Four** requires a bounded statement of no commercial products with a span and a second source (C16).
- **X.8 Undisclosed earned revenue.** Program-service or contract revenue in a filing whose clients are not disclosed caps at 3 until the clients are named; if a lab is named among them, X.2 applies.

## 9. Track record and mis-dimensioned facts

A pledge to evaluate is not an evaluation. An organization with no published evaluation of a frontier model floors at 0 on access and takes no floor above 2 on scope, publication, or methods. This does not apply to a public body whose access or scope rests on statute or regulation: a legal power is not a pledge, and A.2 and S.4 govern those dimensions for it.

A signal whose fact belongs to another dimension (an ownership fact recorded on access, a funding-disclosure fact recorded on methods) is informational on the dimension it sits on (`bound: null`, `bound_note` naming this section) and is re-recorded on the right dimension as a new signal.

## 10. Role classification

Role is derived, not typed. `python -m bench verify` rejects a stored role that disagrees.

- **Government:** a public body (type `gov`).
- **First-party:** a unit of a frontier developer (type `bigtech`).
- **Vendor:** venture-backed (type `vc`), or a role-incompatibility value of 1 or 0 (sells products or services to labs), or a private company that consults for labs (X of 2 with type `private`).
- **Independent referee:** nonprofit, public benefit corporation, or academic group whose published work is evaluation or research, with no products sold to evaluated labs. Lab fees for the evaluation itself do not change the class; they change the funding value.
- **Benchmark or consortium:** an organization whose evaluation output is a leaderboard or a standard rather than engagements keeps `role: benchmark`; it is placed in a list by its owner's type (academic and nonprofit with referees; consortia funded by member labs with commercial and first-party).
- **Expected entrant:** watchlist only, never ranked.

List placement on the site: independent referees; government institutes; commercial and first-party (vendors, lab units, lab-funded consortia).

## 11. Population

Scope (D-001): an organization is in scope if it evaluates or red-teams frontier models for safety-relevant properties, meaning dangerous capabilities (biological, chemical, cyber, autonomy), misuse, alignment and scheming, security, safeguards, and incident investigation, or if it is a public body or standards body with a role in that layer. Capability and performance leaderboards, and organizations whose only frontier work is capability benchmarking, are out of scope; if already in the directory they are retained with `status: out-of-scope`, unranked, shown in their own section, and excluded from every statistic.

Inclusion, within that scope: cited as an external evaluator or red team in at least one frontier system card or government evaluation report in the last 24 months; or named in a statute, code, or standard as an evaluator; or operating a safety benchmark cited by a frontier developer for a frontier model. `data/exclusions.json` records every candidate checked, the criterion applied, and the result. A hypothetical composite is never scored.

## 12. People

Public roles only. No inference about motive or timing. A named individual is contacted with their card and a reply window when the bench publishes a claim about them that binds to a score, or when an open question about their gift or role needs a document only they can supply (`bench outreach --people`). People named only in background role mentions — public, confirmed, and not load-bearing for any score — are covered by the public correction channel, not a cold email. An open question that concerns a named person's gift or role is phrased as a request for a document, never as an unresolved suspicion, and goes to the person as the release goes public; until the outreach log shows a contact date, the card is provisional.

## 13. Weights

Each preset in `data/presets.json` carries a `derivation` paragraph naming the persona and the external instrument the weights follow. The lab-procurement preset was fixed in the seed script on 15 September 2026 before the population pass of the same day; it was not registered anywhere outside this repository, so it is called the confirmatory preset, not a pre-registered one. The other presets are sensitivity checks.
