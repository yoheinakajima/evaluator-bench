# Right of reply: Humane Intelligence

Prepared 2026-09-15. Reply requested within 14 days of sending. This is the complete record Evaluator Bench holds about Humane Intelligence; nothing else feeds the score. Values are derived from the signals' bounds under RULES.md; the default site view uses the standard evidence policy (confirmed sources only).

## How to reply

- Correct a fact: open a pull request adding a signal with a source, or reply with the rows and sources and we file them as a signal marked `source_type: self`.
- Dispute an anchor: say which anchor text you believe applies and which rule in RULES.md decides it; the resolution field records the disagreement even if the value does not change.
- Publish terms: contract terms on scope, access, and publication rights move the relevant dimensions on their own.
- Silence is recorded as silence, not as agreement.

## Current assessments

### Funding: 3/4 (standard policy: 3)
Anchor 3: Mostly philanthropic or public money; some lab-linked pooled funds.
Derivation: Floored at 3 by humane.02 (F.9): Government partners rather than lab clients.. No admissible signal caps it.
- [for, floors at 3, F.9] Government partners rather than lab clients. Quote: "Humane Intelligence would not be able to do its important work without the support of our funders" Sources: Humane Intelligence (https://www.humane-intelligence.org/)

### Governance: 2/4 (standard policy: 2)
Anchor 2: For-profit or PBC with a published COI policy.
Derivation: Floored at 2 by humane.04 (G.1): Nonprofit.. No admissible signal caps it.
- [for, floors at 2, G.1] Nonprofit. Quote: "Humane Intelligence is a 501(c)(3) nonprofit dedicated to breaking down barriers to AI deployment for social good" Sources: Humane Intelligence (https://www.humane-intelligence.org/)

### Personnel: 2/4 (standard policy: 2)
Anchor 2: Frequent two-way hiring; recusal on request.
Derivation: Capped at 2 by humane.10 (P.4): Humane Intelligence's advisory group includes a Senior Research Scientist at Meta, and its board president previously worked on OpenAI's Human Data team; no recusal or cooling-off rule is published.. Floors up to 2 from humane.05 do not exceed the cap.
- [for, floors at 2, P.6] No lab roles found. Sources: Humane Intelligence (https://www.humane-intelligence.org/)
- [against, caps at 2, P.4] Humane Intelligence's advisory group includes a Senior Research Scientist at Meta, and its board president previously worked on OpenAI's Human Data team; no recusal or cooling-off rule is published. Quote: "Dr. Diego Garcia-Olano Senior Research Scientist, Meta" Sources: Board & Advisory - Humane Intelligence (https://www.humane-intelligence.org/board-advisory/)
- Document request: Request to Humane Intelligence: the board and advisory-group conflict-of-interest policy, and whether advisory-group members employed by a model developer recuse from evaluations involving that developer's models.
- Document request: Request to Humane Intelligence: whether any cooling-off rule applies to directors previously employed by a model developer, and the dates of the board president's OpenAI employment as stated in the published bio.

### Access depth (lab-granted): 1/4 (standard policy: 1)
Anchor 1: Pre-release API with safeguards on.
Derivation: Capped at 1 by humane.03 (A.6): Public-model access only.. Held: C15: a 0 needs a quoted span.
- [against, caps at 0, A.6] Public-model access only. Sources: Humane Intelligence (https://www.humane-intelligence.org/)

### Scope control: 3/4 (standard policy: 3)
Anchor 3: Evaluator sets scope and can add questions.
Derivation: Floored at 3 by humane.06 (S.5): Designs its own exercises.. No admissible signal caps it.
- [for, floors at 3, S.5] Designs its own exercises. Quote: "We collaboratively design and run rigorous evaluations" Sources: Humane Intelligence (https://www.humane-intelligence.org/)

### Publication rights: 3/4 (standard policy: 3)
Anchor 3: Publishes; redaction limited to security; redactions disclosed.
Derivation: Floored at 3 by humane.01 (R.5): Publishes openly; public exercises.. No admissible signal caps it.
- [for, floors at 3, R.5] Publishes openly; public exercises. Sources: Humane Intelligence (https://www.humane-intelligence.org/)

### Method transparency: 2/4 (standard policy: 2)
Anchor 2: Methods described in prose.
Derivation: Floored at 2 by humane.07 (M.2): Methods published.. No admissible signal caps it.
- [for, floors at 2, M.2] Methods published. Quote: "using our own software, which we are releasing under an open source software license in 2026" Sources: Humane Intelligence (https://www.humane-intelligence.org/)

### Role incompatibility: 2/4 (standard policy: 2)
Anchor 2: Consults for labs.
Derivation: Conflict: floor 3 from humane.08 (X.7) against cap 2 from humane.09 (X.1); resolved at 2 by X.1: humane.08's raw floor of 4 is held to 3 by C15/C16 and still exceeds the X.1 cap; X.1 decides because the paid-services statement is on the organization's own page.
Resolution: X.1 decides 2: humane.08's raw floor of 4 is held to 3 by C15/C16 and still exceeds the X.1 cap; X.1 decides because the paid-services statement is on the organization's own page.
- [for, floors at 4, X.7] No commercial products. Sources: Humane Intelligence (https://www.humane-intelligence.org/)
- [against, caps at 2, X.1] Humane Intelligence sells red-teaming events and contextual evaluations as paid services using its own software, and invites clients to 'hire us'; the client list is not published. Quote: "Humane Intelligence offers red teaming events as a paid service using our own software" Sources: Humane Intelligence (https://www.humane-intelligence.org/)
- Document request: Request to Humane Intelligence: a list of paid red-teaming and contextual-evaluation clients since 2024, or a statement of whether any client is a frontier developer.

## Dissent on the card

- Lower: Access should be 0. No pre-release access is documented anywhere: the public exercises, bias bounties and NIST and IMDA partnerships tested deployed models, no system card names Humane Intelligence as a pre-release tester, and no lab engagement is on record. The card shows 1 only because the anchor-0 claim lacks a quoted span (C15), not because anything above public access was ever granted.
- Higher: Access should be 2. Humane Intelligence co-ran the NIST ARIA pilot and the Singapore IMDA multilingual red-teaming exercise, in which participating developers supplied models under government programs; A.4 treats government testing agreements as 3. If those exercises gave structured access beyond the public API, even with safeguards on, the documented engagement is at least anchor 2.

## Ledger rows naming the organization


## What would move the score

Pre-release access for the harms it covers.

Replies are filed as signals with the date received. Evaluator Bench: https://github.com/yoheinakajima/evaluator-bench
