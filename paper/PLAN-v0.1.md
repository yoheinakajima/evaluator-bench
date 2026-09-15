# Evaluator Bench: credibility plan for v0.1

Written 15 Sep 2026 against the live site, the v0 data (`dist/bench.json`), two independent reviews, and the curator's proposal that unverifiable sources should not move a score by default. Freeze is 29 Sep 2026. Every number below is computed from the v0 build.

## 0. The three moves

1. **Scores become recomputable from evidence under a reader-selectable evidence policy.** By default, no source the reader cannot open and verify moves a number. Nothing is deleted; weaker evidence is kept as leads and shown when the reader asks for it.
2. **Hidden judgment becomes visible rule.** Signals carry anchor bounds. Tie-breaks are written down. Bands replace numeric caps. Extremes need spans. A second coder and a dissent field sit on every contested card.
3. **The conflicts, the limits, and the byline sit next to the score,** not at byte 80,000.

If these three land, the METR question, the AVERI question, and the Scale question stop being arguments about the curator and become arguments about a rule anyone can read, and the site stops rewarding silence because silence renders as "unevidenced" rather than as a number.

## 1. Fairness audit: what is arbitrary today

Each row is something a hostile reader can point at. "Phase" refers to section 7.

| # | Where judgment is hidden | Why it is attackable | Fix | Phase |
|---|---|---|---|---|
| 1 | Source quality never touches the number. The Kevin Bass `evaluators.csv`, marked unverifiable by the project itself, is cited by 27 ranked signals across 11 evaluators. | "Every score traces to a source" is true, but some trace to a source you say cannot be checked. | Evidence policies (section 2). Under the default policy those 27 signals become inadmissible; 21 assessments go unevidenced instead of numbered. | 1 |
| 2 | 32 assessments sit at 0 or 4. 29 rest on a single signal, 28 have no quoted span, and 24 rest only on the organization's own statements. | A 4 on method transparency or role incompatibility handed out on one self-published page is the definition of rewarding self-report. | Extremes rule: a 0 or 4 requires a quoted span and either a non-self source or an admission against interest. Until met, the value is held at the nearest supportable anchor and labeled. | 1 |
| 3 | Anchor text and evidence disagree, and the rationale does not say why. Scale F=0 under the anchor "majority owned or funded by a frontier developer" for a 49% non-voting stake. 170 of 208 rationales read "Anchor N on X given the cited signals." | Under gating, F=0 caps at 40 and F=1 caps at 60. The single most consequential call on the site has a placeholder rationale. | Signal bounds plus written tie-breaks (sections 2.3, 4.1). The rationale is generated from the binding signal and must be prose wherever signals conflict. | 1 |
| 4 | The evidence bar is asymmetric: a 4 on funding, governance, or personnel needs a tier-1 source; a 0 needs any confirmed source. | Reads as harder to earn a top score than a bottom one. | Keep the asymmetry (absence of conflict is only provable in filings) but state it on the rubric page, and raise the 0 bar to a span plus admission-or-non-self-source. | 1 |
| 5 | Gate caps of 40 and 60 are unexplained numbers. | 60 versus 59 implies precision the design disclaims. | Bands: Disqualifying floor (any 0), Conditional (any 1), Clear. Band first, number second, number ranks within band only. | 2 |
| 6 | Weights are called "pre-registered" with no public timestamped artifact, and no derivation. | The word does work it has not earned. | Either link a commit or registration that predates the population pass, or drop the word. Publish a one-paragraph derivation per preset. Show rank ranges across presets instead of a single rank. | 2 |
| 7 | Role classification is unwritten. Apollo is a referee and Irregular a vendor though both take lab fees; Nemesys is a vendor "because paid contracting." | Role decides which list an organization is compared in. | Written rule (section 4.2), applied mechanically, disagreements logged. | 1 |
| 8 | No inclusion criteria and no exclusion list. | The population looks like "the AISI and METR cluster plus whoever was in the training data." | Criteria plus a named-exclusions page (section 4.3). | 2 |
| 9 | Publication rights gives CAISI a 1 for statutory non-publication and would give a vendor a 1 for lab-held pens. | Same number, different mechanism. | Keep the outcome measure (what reaches the public), add a mechanism tag (statutory, lab-controlled, self-imposed, unknown), and split the default view into lists so the two are not sorted together. | 2 |
| 10 | A hypothetical composite is scored beside real organizations. | Teaches the wrong lesson about what a score is. | Remove from the scored watchlist; move the composite to the paper's discussion. | 0 |
| 11 | Curator proximity. METR at F=3 and R=3 with in-kind lab compute, a young donor rule, lab-set scope and tone feedback. AVERI at 79 on a thin track record. | Looks like home-team gravity whether or not it is. | Do not re-score by fiat. Write the tie-break rules (in-kind materiality, editorial feedback, track record), apply them to all 26, and add a dissent field on every card. Second coder on every extreme and the top ten. | 1, 2 |
| 12 | Two populations reported as one: the homepage money section counts 28, the status page and paper count 26. | Reader cannot tell which number to cite. | One population for every statistic (26 ranked). Watchlist stats only on the watchlist. | 0 |
| 13 | Source tiers are miscoded: MarkTechPost and a Davis Wright Tremaine client alert are tier-3 self; aggregator press (Unite.AI, Dealroom, AlphaSignal) shares a tier with CNBC and Forbes. The paper's opening claim about the two CEO pledges cites aggregators. | Tier is what the evidence policy keys on. | Recode; split press into primary and aggregator; cite the primary announcements for the pledge claim. | 1 |
| 14 | Padded signals ("Nonprofit." as a for-signal) still exist and still floor values, even though for/against counts were removed from the UI. | Legal form is not conduct. | Under the bounds model each signal must name the anchor it supports; "nonprofit" alone floors governance at 2, not 3. | 1 |
| 15 | Single coder, first draft by a lab's model, no agreement statistic. | The cheapest criticism to make and the hardest to answer without a second human. | Human second coder on extremes and the top ten by freeze; full population by v0.2; publish per-dimension agreement. | 2 |
| 16 | Dataset B uses secondary sources and hindsight-selected triggers. | Historians will pick at milestone years; the lag result is described as a finding in places. | Caveat on the homepage figure, not only in the paper; outcome-independent trigger enumeration in phase 3. | 0, 3 |
| 17 | Quoted spans exist for 44 of 314 signals. One of ten sampled spans (securebio.01) is not on the cited page. | "Inspectability" without spans is a promise, not a property. | Span gate on every binding signal before freeze (section 2.5). Run `bench review` over the existing corpus, not only over PRs. | 1 |

## 2. Evidence policies: the design

### 2.1 Classify every source on two axes

Keep the two facts separate instead of collapsing them into one tier.

- **Provenance:** 1 filing or funder index; 2 third-party ledger; 3 the organization's own statement; 4a primary press (named reporter, editorial outlet); 4b aggregator press and newsletters.
- **Verification:** confirmed with span (fetched, quote found verbatim); confirmed (fetched, no span captured); unaudited; imported; unverifiable.

Every signal inherits the best source it cites. A signal's direction (for or against the organization) is already recorded.

### 2.2 Five policies, one default

| Policy | Rule | Ranked signals admissible today (of 295) | Assessments left unevidenced (of 208) |
|---|---|---|---|
| Leads included | Everything, including unverifiable and imported | 295 | 0 |
| **Standard (default)** | Confirmed sources only, any provenance | 257 | 21 |
| Against interest | Standard, and self-published sources count only for signals against the organization | 143 | 101 |
| Verified spans | Standard, and the signal carries a quoted span | 38 | 182 |
| Primary only | Provenance 1 or 2, confirmed, with span | 1 | 207 |

What this says about v0: the default is viable today (21 dark cells, concentrated in Microsoft AI Red Team, Nemesys, and EquiStamp, which is where the evidence is thinnest). The two stricter views are honest and brutal, and "Primary only" is the paper's central finding rendered as a table: from outside the field, one signal in the corpus can be verified. Ship that view. It is the strongest argument on the site.

"Skip self-reported facts" as a blanket rule is the wrong cut. Self-publication is the best evidence there is for admissions (OpenAI covered our costs; we accept employee donations). The statement-against-interest rule keeps those and discounts the self-serving ones. Lawyers and auditors will recognize the rule, which is the point.

### 2.3 Make scores recomputable: bounds on signals

The assessment value is currently a curator's read of all signals at once, so a source cannot be switched off without a human re-reading. Fix that at the schema level.

- Each signal declares the anchor it supports on its dimension: an against-signal sets a **cap** ("Meta holds 49%: funding at most 1"), a for-signal sets a **floor** ("written no-lab-money rule: funding at least 3"). The anchor text in `data/dimensions.json` is the lookup table.
- Under a policy, only admissible signals contribute. Value = the tightest admissible cap if any cap exists, else the highest admissible floor. No admissible signal: **unevidenced**, rendered as a dash, never as a number.
- Where an admissible floor exceeds an admissible cap, the verifier flags a **conflict** and the build fails unless the assessment carries a prose rationale naming the rule that resolves it. That is the only place judgment is allowed, and it is now visible.
- The rationale for non-conflict assessments is generated: "Capped at 3 by metr.19 (in-kind compute from OpenAI, below the materiality threshold in RULES.md section 1.2)." The 170 boilerplate rationales disappear by construction.
- Score under a policy is computed over evidenced dimensions and displayed with coverage: **81 · 8/8 evidenced**, or **60 · 5/8**. A dimension that is unevidenced does not trip a gate; the card shows "floor unevidenced" instead.
- "What would move the score" becomes computed: "Publish a cooling-off policy (floors personnel at 3): 81 becomes 84 under lab procurement." This turns the site from a verdict into a standard organizations can meet.

### 2.4 Verifier rules to add

- C15: any assessment at 0 or 4 must be supported by a signal with a quoted span.
- C16: a 4 requires a provenance-1 or -2 source, or two independent sources of which at least one is not self-published.
- C17: a 0 requires a span and either a non-self source or an admission against interest.
- C18: every binding signal (the one that sets the value under the default policy) carries a span before a tag is cut.
- C19: an assessment with no Standard-admissible signal is stored as unevidenced, never as a value.
- C20: role is derived from the classification rule, not typed in.
- C21: one population for every published statistic; the watchlist contributes to none.

### 2.5 Span coverage as a gate, scoped to what matters

Three hundred spans in two weeks is not realistic if every one is done by hand. The gate is narrower and defensible: every binding signal has a span. Order of work: the 32 extremes first (about 40 signals, one day), then binding signals for the top ten and bottom six, then the rest. Non-binding signals may lag to v0.2 because the score does not depend on them. Run the existing machine review over the whole corpus now; it will catch the securebio.01 mismatch and others like it.

### 2.6 What this buys

The one-sentence answer to "is it fair": by default, no number on this site moves on a source you cannot open and check yourself, the stricter views are one click away, and nothing was thrown away to get there.

## 3. Presentation of scores

- **Band before number.** Disqualifying floor, Conditional, Clear. The number ranks within the band. Drop the 40 and 60 caps as numbers; the band is the cap.
- **Evidence coverage beside every score,** as in 2.3, and the evidence-policy selector next to the weight presets, defaulting to Standard.
- **Three default lists, one rubric.** Independent referees; government institutes; commercial and first-party (vendors, lab units, lab-funded consortia). Benchmarks and academic groups sort by their owner's type. The single sorted list remains available as a view, not the default.
- **Competence chip on every score:** "Independence only. Not quality, coverage, or competence." Persistent, not a paragraph.
- **Rank range across presets** rather than a single rank, since the site already computes the range.
- **Sort by weakest dimension** as a peer to sort by score.
- **Mechanism tag on publication rights and access** (statutory, lab-controlled, self-imposed, unknown).
- **Hypothetical composite removed** from anything that renders a number.

## 4. Rules to write down

### 4.1 RULES.md: tie-breaks per dimension

The point is not the specific thresholds; it is that they are written before they are applied and applied to all 26.

- **Funding.** In-kind compute or access counts as lab money when it exceeds a stated share of annual operating cost (propose 5%) or when the amount is undisclosed. Pooled funds and donor-advised funds with non-public donors cap at 3 until the donors are named. A donor rule younger than 24 months or amended more than once in that window does not floor above 3.
- **Governance.** Legal form alone floors at 2. A published conflict policy floors at 3 only if it names recusal, outcome-contingent fees, and lab investments. Independent board evidenced in a filing is required for 4.
- **Personnel.** Two-way hiring without a published cooling-off rule caps at 2. Board or advisor seats within one hop of a lab cap at 2 regardless of recusal.
- **Access.** Score what labs have granted, as now. Access that rests on statute or a court-enforceable agreement floors at 3 even if shallow, and the card says which.
- **Scope.** Lab-set time window or excluded questions cap at 3; evaluator inability to add questions caps at 2.
- **Publication.** Security redactions with a public statement of what was redacted: 3. Lab feedback on emphasis or tone that was incorporated caps at 3 if the evaluator discloses what changed, at 2 if it does not. Summaries only: 1. Statutory non-publication is scored on outcome and tagged by mechanism.
- **Methods.** Open code and tasks that a third party has actually re-run: 4. Open but not re-run: 3. Prose only: 2.
- **Role incompatibility.** Selling defenses, guardrails, or monitoring to an evaluated lab: 0. Selling to a lab's customers: 1. Consulting on frameworks for a lab: 2.
- **Track record.** A published finding the lab did not like (scheming, reward hacking, safeguard failure, shutdown resistance) is the only path to 4 on publication. It is load-bearing, not a bullet.

Apply these and let METR, AVERI, and Scale land where the rules put them. If METR stays at 3 on funding, the card now says why in one sentence that cites a threshold.

### 4.2 Role classification

- **Independent referee:** nonprofit, public benefit corporation, or academic group whose published mission is evaluation or research, with no products sold to evaluated labs. Lab fees for evaluation do not change the class; they change the funding score.
- **Government:** a public body.
- **Vendor:** sells products or services to labs beyond the evaluation itself, or is venture-backed with lab-adjacent investors.
- **First-party:** a unit of a developer.
- **Benchmark or consortium:** publishes a leaderboard or standard rather than engagements; classified by its owner's type for list placement.

### 4.3 Inclusion criteria and named exclusions

Inclusion: cited as an external evaluator or red team in at least one frontier system card or government evaluation report in the last 24 months; or named in a statute, code, or standard as an evaluator; or operating a leaderboard cited by a frontier developer for a frontier model. Publish the list of candidates checked and why each is in or out. Candidates a reader will expect to see addressed, with the reason or the score: Artificial Analysis, LM Arena, Stanford HELM and CRFM, EleutherAI, Vals AI, Patronus, Haize Labs, Lakera, Promptfoo, Giskard, Trail of Bits, NCC Group, Apart Research, Virtue AI, the Japan, Singapore, Korea, Canada, France and Germany institutes, and lab-internal evaluation teams other than Microsoft's. Verify each against the criteria; several will be out, and the reason should be one line on the exclusions page.

### 4.4 People policy

Public roles only. No inference about motive or timing. Every named individual receives their card and a reply window, the same as an organization. Open questions that concern a named person's gift or role are phrased as a request for a document, not as an unresolved suspicion, and are sent to the person before they are published.

### 4.5 Weights

Each preset gets a paragraph explaining who the persona is and which external instrument the weights follow (AEF-1 conditions, SB 315's financial-interest test, financial-audit independence rules). Drop "pre-registered" unless a timestamped artifact predates the population pass. In phase 3, elicit weights from a small panel of evaluators, regulators, and lab safety leads and publish the survey beside the presets.

## 5. Process credibility

- **Proactive right of reply.** Email every ranked organization and every named individual their card, the rules, and the deadline. The status page tracks contacted, replied, no reply, with dates. Passive "corrections welcome" is not how journalism or audit does this.
- **Second coder.** A human with domain knowledge, not another lab's model, codes every extreme and the top ten and bottom six before the freeze, the full population by v0.2. Disagreements are logged in the rationale; per-dimension agreement is published on the status page.
- **Dissent field.** Every card carries the strongest case for one notch lower and one notch higher, written by the curator. This converts hidden judgment into visible judgment and is what a reader who disagrees will engage with.
- **Disclosure.** Byline on the homepage with the six lines that matter: curator, fund, Epistemedia, ActiveGraph, first draft by Claude, holdings. Replace "none known" on shared funders with the result of an actual check of Untapped Capital's limited partners against the funder list in the ledger, or with "not checked."
- **External signed reviews.** Two or three named reviewers (an audit-independence scholar, a former regulator, an evaluator who is not scored) publish signed reviews in `paper/`, including the ones that disagree.
- **Freeze realism.** Keep 29 Sep as the close of the launch round, but do not call any tag citable until the span gate, the second coder pass on extremes, and the reply window have completed. Tag it "v0.1 candidate" until then.

## 6. Site and paper fixes

### 6.1 Before anyone shares the link

- HTTPS: the server presents a `*.github.io` certificate. Remove and re-add the custom domain in Pages settings to trigger provisioning, then enable Enforce HTTPS.
- The Independence bar column renders at zero height (`.bar` is `display:inline`).
- Favicon, Open Graph and Twitter card tags, canonical URL.
- Phone navigation scrolls horizontally with no affordance; nine of eleven links are off-screen at load. Wrap or collapse. Figures that scroll sideways need a visible cue.

### 6.2 Homepage

Above the fold: banner, thesis, byline and conflicts line, evidence-policy and weight controls, the three lists, then a 400-word "how to read this." Everything else moves: rubric and signals to `/rubric`, cases to `/cases`, regimes and paths to `/regimes`, money matrix and graph to `/ledger`, method to `/method`. Keep a one-screen "Where we are" teaser with the Dataset B caveat on it.

### 6.3 Voice and consistency

- Cut the audit-literature nouns from the homepage (gated ordinal projections, bounded negatives, quarantined rows, event-log digest). Keep hops, floors, the dated banner. A glossary page holds the rest.
- "Product conflicts" in the README versus "Role incompatibility" in the UI. Pick one.
- "UK AI Safety Institute" in paper section 5.5 versus "UK AI Security Institute" everywhere else.
- "Six engagements" in the cases section; the Irregular and Sequoia case is an investor overlap.
- Funding-graph caption copy runs sentences together.
- One sentence under the access slider explaining why lab-granted access is scored as revocable.

### 6.4 Paper

- Section 5.8 contains two overlapping passes that repeat the same sentences. Keep the release projection, delete the audit-path narrative or move it to `paper/NOTES.md`.
- H4 is cited twice; H1 through H3 are never stated. Publish the hypotheses or drop the labels.
- Table 3 points readers to an internal notes file.
- The opening claim about the two CEO pledges should cite the primary announcements.
- Section 5.2 is called a finding in places and a description in others. Use one word.

### 6.5 Data

- Fix securebio.01, which quotes text that is not on the cited page.
- Recode MarkTechPost and the Davis Wright Tremaine alert as press; split press into primary and aggregator.
- Run `bench review` over the whole corpus and file every mismatch as an issue.

## 7. Schedule and ship gates

**Phase 0, 15 to 16 Sep.** Section 6.1 in full. Remove the hypothetical composite from scoring. One population for all statistics. Byline and competence chip on the homepage. Dataset B caveat on the figure. Paper editorial fixes in 6.4.

**Phase 1, by 22 Sep.** Source classes and evidence policies (2.1, 2.2) in schema, verifier, and UI. Signal bounds (2.3) added to all 295 ranked signals, with conflicts resolved in prose. Verifier rules C15 to C21. RULES.md and role rule (4.1, 4.2) written and applied. Spans on all extremes and all binding signals for the top ten and bottom six. Tier recoding. Corpus-wide machine review. Right-of-reply emails sent with a dated log.

**Phase 2, by 29 Sep.** Bands, coverage, rank ranges, three lists, mechanism tags, computed "what would move the score." Second coder on extremes and top ten and bottom six, agreement published. Dissent field on every card. Inclusion criteria and exclusions page. Funder-overlap check completed and disclosed. Homepage restructure. Weight derivation paragraphs.

**Phase 3, October.** Full second-coder pass. Weight elicitation panel. Outcome-independent trigger enumeration and primary-source verification for Dataset B. External signed reviews. Docket submissions to Epistemedia. Spans on all remaining signals.

**Gates for a citable tag:** every binding signal has a span; every extreme has a second coder; every ranked organization and named individual has been contacted with a dated record; the default policy is Standard and the Primary-only view is live; RULES.md is published and every conflict rationale cites it; the homepage carries the byline and the competence chip.

## 8. Criticism and answer

| Who | The criticism | The answer after this plan |
|---|---|---|
| Counsel for a scored organization | "You scored us 0 on a blog post and a spreadsheet you admit is unverifiable." | Extremes need a span and a non-self source or an admission; unverifiable sources are inadmissible by default; the rule that produced the value is cited on the card; they had the card and the rules before publication. |
| Lab policy lead | "This ranks independence, and people will read it as quality." | Band before number, competence chip on every score, three lists, domain filters, and the persistent statement that a 60 with a thin file is not "fairly independent." |
| Competing evaluator | "METR gets the benefit of the doubt because they look like the independent evaluator." | RULES.md thresholds for in-kind money, donor-rule age, and editorial feedback, applied to all 26; a dissent field on the card; a second coder on every extreme. |
| Academic reviewer | "Single coder, LLM-drafted, no agreement statistic, hindsight-selected triggers." | Second coder with published agreement; hypotheses published or labels dropped; Dataset B caveat on the figure and an outcome-independent enumeration in phase 3. |
| Journalist | "Who built this and what do they own?" | Byline and holdings on the homepage; funder overlap checked, not "none known"; the Claude draft disclosed next to the score, not in a repo file. |
| Regulator | "Can I use this as a shortlist?" | No, and the site says so on the first screen. What it can be used for: the rules, the ledger, and the list of documents that would move each score. |
| A skeptic of the field | "Fifty-four percent self-published. This is inspectability theater." | The Primary-only view shows exactly what can be verified from outside: one signal. That is the finding, shown as a table instead of a sentence, and the evidence policy selector lets anyone choose their own bar. |
| A scored person | "You published an open question about my donation." | People policy: document requests, not suspicions; the person receives the card and a reply window before publication. |

## 9. Where this plan disagrees with the feedback

- **Do not re-score METR one notch down by hand.** Trading one judgment for another does not make the site fairer. Write the in-kind, donor-rule, and editorial-feedback rules, apply them to everyone, and let the number fall where it falls. If it stays at 3, the card now says why with a threshold.
- **Do not skip self-reports wholesale.** Self-publication is the best evidence for admissions. Use the against-interest rule.
- **Excluding low-quality sources must produce "unevidenced," not a better number.** If a missing source silently defaults to a middle value, the site is back to rewarding silence. A dash is the honest render.
- **Keep the number, but demote it.** Reviewer two's instinct to treat scores as illustrations goes too far; the bounds model makes the number derivable, so it can stay, ranked within a band and shown with coverage.
- **One rubric, three lists.** Splitting the rubric by type would make the historical comparison incoherent. Splitting the default view fixes the product problem.
- **Do not promise every span by 29 Sep.** Gate the binding signals and the extremes. The rest can lag because the score does not depend on them.
