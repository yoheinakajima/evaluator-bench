# Push instructions (for the operator or an agent acting for the operator)

Everything below is mechanical. Nothing here changes evidence or scores.

1. Create the empty repository `yoheinakajima/evaluator-bench` on GitHub (public, no README, no license, no .gitignore; the repository already has them).
2. From this directory:
   ```
   git remote add origin git@github.com:yoheinakajima/evaluator-bench.git
   git push -u origin main
   git push origin v0
   ```
   Push only the `v0` tag. Pre-release tags have been removed locally; do not recreate them.
3. Repository settings:
   - Pages: Source = GitHub Actions. `.github/workflows/pages.yml` verifies, rebuilds, checks for drift, and deploys `dist/`.
   - Secrets: add `ANTHROPIC_API_KEY` so `bench review` can run the model check on pull requests (without it the job still re-fetches sources and checks quoted spans).
   - Branch protection on `main`: require the `contribution-check` workflow to pass; require one review; CODEOWNERS is in place for `data/`, `dockets/`, the verifier and the CONTRACT.
   - Enable Issues (two templates are included) and Discussions if wanted.
4. After the first deploy, open the site and check three links: the home page, `/evaluators/`, `/status/`. The Status page reports the event-log digest that the release was built from.
5. Set the window date from the push day: `python -m bench release --stage preview --until <push date + 14 days>`, rebuild, commit, push. If the push happens on 15 September 2026 the committed value (2026-09-29) is already right.
6. When the window closes: `python -m bench changelog --since v0` for the launch-round section, `python -m bench release --stage published --tag v0`, rebuild, commit, tag `v0` again with `-f` only if the release row is the sole change; otherwise tag `v0.1`.

Do not edit `graph/` or `dist/` by hand at any point; they are regenerated and CI rejects drift.
