# Merge handoff — evaluator-bench PRs #20 and #21

**Authorization:** The repository owner (yoheinakajima) explicitly authorized merging in chat on 2026-09-15 ("give me a handoff doc for the agent to merge", and again "Yes" on 2026-09-15 for PRs #20/#21). This supersedes the draft-PRs-only rule for this task. You are the merge agent; merge them now.

## Source repo
- Local primary clone: `~/workspace/evaluator-bench-prs`
- GitHub: `yoheinakajima/evaluator-bench`, base branch `main` (verify HEAD first: `git fetch origin && git rev-parse origin/main` — should be `f03e43f` unless something else merged since)
- Venv: `~/workspace/venv-bench` (Python 3.12). Run `python -m pytest` from the directory you test (the venv's editable install points at the primary clone).
- Push helper: `~/workspace/push-merge.py` (writes merge commits via git-database API and fast-forwards `refs/heads/main`). Known quirks: direct `git push` has no credentials; the GitHub "merges" API prints "ok" without acting; the API needs full SHAs, abbreviated ones 404; always verify every remote write with a GET.

## What to merge (both drafts, nothing else)

| # | Branch | Contents |
|---|--------|----------|
| 20 | `fix/funder-disclosure` | Shared-funder disclosure wording: "no overlap found in public records (checked 2026-09-15); the full limited-partner roster is private, so overlap through undisclosed LPs remains unchecked" — applied to DISCLOSURE.md and the Method page disclosure card |
| 21 | `fix/binding-spans` (remote `185e156`) | Binding-span pass: spans added for the unspanned binding signals; `rand.04` superseded by `rand.04b` (RAND R 2→3); `rand.08` quote_source fixed (`rand-aef` → `rand-integrity`, RAND X now unevidenced); paper §5.5 synced (8 unevidenced, 3 held, role-incompatibility mean 2.30) |

**Merge order: 20 → 21.** #21 touches paper/draft.md and data/; if #21 has real conflicts with #20 (unlikely — #20 is disclosure copy), prefer #21's content on data/paper and #20's on disclosure copy. No conflicts expected.

## Procedure per PR
1. Fetch the branch, merge into `main` with `git merge --no-ff`.
2. Conflicts: only in generated `dist/`/`graph/` are expected. Never hand-edit those — resolve `bench/*.py`, `site/template.html`, data, and paper files, then **regenerate**: `python -m bench verify && python -m bench build`.
3. Checks must pass before each push: `python -m bench verify && python -m bench build && python -m pytest -q`. Note: PR #21 was at 251 sources / 370 signals / 216 assessments with 60/60 passing.
4. Push via `push-merge.py`; verify via GET; mark the PR closed/merged on GitHub; record merge commit SHAs in MERGE-RESULT.md (append).

## Hard constraints
- Do NOT send, draft, or resume outreach emails. Outreach log/contact state untouched.
- Do NOT change any assessment values beyond what the branches already contain (the `rand.R` 2→3 and RAND X held-at-3 were verifier-driven in the PRs — those are already part of the branches and approved; don't relitigate).
- No commits on `main` except the two merge commits.

## After merging
1. On `origin/main`: final `python -m bench verify && python -m bench build && python -m pytest -q` in a clean checkout.
2. Confirm the GitHub Pages workflow rebuilt on the new `main` (completed success) — this refreshes the live site.
3. Report: merge commit SHAs, check results, Pages status, and the new `origin/main` HEAD.

## Still outstanding after this (do not do — report only)
- 8 binding spans still missing (equistamp.07, farai.07, farai.11, msft.07, palisade.09, redwood.08, saferai.04, saferai.07) — documented in PR #21, none fabricated. `redwood.08` needs a primary source.
- Outreach gate 0/51 (owner's call; do not email).
- Batch 3 (deferred), Recipe D candidate work (unauthorized).
