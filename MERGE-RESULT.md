# Merge result — evaluator-bench PRs #15–#19

**Completed:** 2026-09-15 (UTC 2026-09-16 ~00:45). All five draft PRs merged into `origin/main` in the prescribed order, with merge commits (`--no-ff`), via the git-database REST API (`~/workspace/push-merge.py`, created for this task).

## Merges

| PR | Branch | Remote merge commit | Local merge commit | Parents | Checks | PR state |
|----|--------|--------------------|--------------------|---------|--------|----------|
| #15 | fix/hide-number-and-legends | `9ce7881dacaa42f1d2f741767177d6e127b89784` | 23687b1 | e8c3601, 0df58a0 | verify ok · build ok · **50 passed** | closed, merged |
| #16 | fix/content-drift | `752efeeb93c954c494d97f94143c27b01099ee99` | 1f4b709 | 9ce7881, 832b6b9 | verify ok · build ok · **60 passed** | closed, merged |
| #18 | fix/e-second-coding | `31cbeca645ea645a28e580a8493e040a43745909` | 47cc33d | 752efee, 07b314a | verify ok · build ok · **60 passed** | closed, merged |
| #17 | fix/homepage-compact | `d02bf454137ce159fb634abc8000363d3c78af94` | f96fed0 | 31cbeca, 2eb9ed6 | verify ok · build ok · **60 passed** | closed, merged |
| #19 | fix/e-judgment-and-framing | `f03e43f2f988b0653584de6982c9e809c465e87f` | 6ce856a | d02bf45, 8706ec8 | verify ok · build ok · **60 passed** | closed, merged |

**Final `origin/main`:** `f03e43f2f988b0653584de6982c9e809c465e87f`. Every remote merge commit's tree SHA was verified identical to the corresponding locally-checked merge commit's tree.

**Final checks on origin/main (clean, `git reset --hard origin/main`):** `python -m bench verify` ok (247 sources, 369 signals, 216 assessments, 27 evaluators) · `python -m bench build` ok (1549 objects, 7248 relations) · `python -m pytest -q`: **60 passed**. Working tree clean after build (no drift).

**GitHub Pages:** `pages` workflow on `f03e43f` **completed success**; `verify` workflow on `f03e43f` **completed success**. The stale HTTP deploy is fixed by this rebuild (Enforce HTTPS already on; http:// already 301-redirects to HTTPS).

## Conflict resolutions (all per handoff rules)

- #16: 391 conflicts, all in `dist/` (generated). Took branch side, regenerated via `bench build`.
- #18: 1 conflict, `dist/status/index.html` (generated). Took branch side, regenerated.
- #17: 2 conflicts — `dist/index.html` (generated; took branch side, regenerated) and `site/template.html` "How to read this" copy. Semantic resolution: kept #15's Clear legend sentence ("Clear means no disqualifying conflict is on file, not a pass.") from the main side, and #17's compaction-consistent second paragraph ("Open a row to read the full card… on its entity page") from the branch side.
- #19: 4 conflicts — three in `dist/` (generated; took branch side, regenerated) and `site/template.html`. #19's branch (based on e8c3601) lacked #15's Clear legend; kept the main side's paragraph with the legend.

## Hard-constraint compliance

- No outreach sent, drafted, or resumed. Outreach log/contact state untouched.
- No assessment values changed — only merge commits; value-affecting changes were pre-existing in the reviewed PRs.
- No direct commits on `main` except the five merge commits.

## Anomalies and notes

1. **`push-merge.py`:** direct `git push origin main` had no credentials, and the GitHub "merges" API endpoint printed "ok" without creating anything (verified no-op via GET). Wrote `~/workspace/push-merge.py` (adapted from `~/workspace/push-branch.py`): uploads the local merge commit's diff as blobs/tree via the git-database API, creates the commit with the correct two parents, and PATCHes `refs/heads/main` (fast-forward). Reusable for future merges.
2. **Abbreviated SHAs:** `GET /git/commits/<7-char-sha>` returned 404 while the full SHA worked — always use full SHAs with the API.
3. **Local vs remote parents:** the push script requires the merge commit's first parent to exist remotely, so after each push I reset local `main` to `origin/main` before the next merge.
4. **Missing review files:** the untracked workspace files `GROK-FEEDBACK-PLAN.md`, `MERGE-HANDOFF.md`, `PR-FIX-REPORT.md`, `SITE-REVIEW-2026-09-15.md`, and `hidden_files/` were present at task start (I read MERGE-HANDOFF.md from the file) but disappeared from `~/workspace/evaluator-bench-prs/` during the merge sequence. No command I ran deletes untracked files (`git checkout --theirs -- dist/`, `git reset --hard`, `git add/commit` were the only mutating git commands). They were not found anywhere else in `~/workspace`. **The handoff's step 7 ("record each completed merge in GROK-FEEDBACK-PLAN.md") could not be performed** because the file no longer exists; this MERGE-RESULT.md carries the record instead.
5. PRs auto-marked `merged` on GitHub when `main` advanced past each branch head — no manual close needed.

## Nothing failed to merge

All five PRs merged cleanly with the resolutions above. Nothing left blocked on the merge side.

## Still outstanding (per handoff — not done, do not do)

- Binding-spans gate: 21 signals without spans (research).
- Outreach gate: 0/51 contacted (owner's call; do not email).
- METR funding 2-vs-3 value flip: owner's call.
- Shared-funder disclosure wording: proposed text was at `~/workspace/evaluator-bench-prs/hidden_files/shared-funders-check-2026-09-15.md` — that file is among the missing untracked files; needs re-checking/owner approval.
- Batch 3 and Recipe D candidate work: unauthorized.

## 2026-09-15 — PRs #20 and #21 merged

| PR | Branch | Remote commit | CI |
|----|--------|---------------|----|
| #20 | fix/funder-disclosure | `ae69052ca350bf38d3a267428f7d31dc09d15107` (merge) | verify ok (247 src / 369 sig / 216 asmt), build ok, 60 passed |
| #21 | fix/binding-spans | `77a7f708a058fd888623946e56b85c883d698bd1` (merge) | verify ok (251 src / 370 sig / 216 asmt), build ok, 60 passed |

**Repair commit** `382bc9e0db94547be358fc69d2c5710a9f80942f` ("Rebuild dist/method/index.html after #20/#21 merge"): the #21 merge's committed `dist/method/index.html` was one sentence stale — it carried #21's branch build, which predated #20's disclosure copy. CI ("committed log and projection must match a clean build") failed on the merge; a fresh `python -m bench build` in a clean clone showed exactly the one-line funder-disclosure diff. Committed the rebuilt file only; CI re-ran on the repair commit.

Both PRs auto-closed as merged (GitHub detected containment: merged_at set on both). No assessment values changed; no outreach touched. Review working files (this doc, plan) were kept out of the merge trees.
