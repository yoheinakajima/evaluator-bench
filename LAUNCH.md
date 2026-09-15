# Launch checklist

State at v0.9: the repository builds, verifies, and tests clean; the site has 200-odd pages with navigation to every item type, a Contribute page with human and agent instructions, a Dockets page, and a Status page. What follows is what a person has to do that a build cannot.

## Before the repository is public

1. **Push and enable Pages.** `git remote add origin git@github.com:yoheinakajima/evaluator-bench.git && git push -u origin main --tags`. In repository settings, set Pages to deploy from GitHub Actions; `.github/workflows/pages.yml` publishes `dist/`. Every link on the site already assumes this repository path.
2. **Fill `DISCLOSURE.md`.** Four bracketed fields. The Method section and the Status page link to it; an empty disclosure on a site about independence is the first thing a reader will notice.
3. **Add the `ANTHROPIC_API_KEY` secret** so the machine-review job can run the model check on pull requests. Without it the job still re-fetches sources and checks quotes.
4. **Publish as a preview with a two-week window.** `python -m bench release --stage preview --until <date fourteen days out>` and rebuild; every page carries the banner. **Nothing has been sent to any evaluator.** Send the packets in `outreach/` yourself, then record it with `python -m bench release --stage preview --until <date> --packets-sent <date>` and rebuild; until that date is set, the banner says the record will be sent, not that it was. Set the window end fourteen days after the send date, not after the push. Public routes (no personal addresses): METR via metr.org contact or the giving address on its site; Apollo via apolloresearch.ai/contact; Transluce via info@transluce.org (published on its site); AVERI via averi.org; UK AISI via aisi.gov.uk; US CAISI via nist.gov/caisi; EU AI Office via the AI Office contact page; SaferAI via safer-ai.org; Palisade via palisaderesearch.org; HAL via the Princeton project page. The window is the right of reply owed to the ten organizations whose scores changed, and it is open to anyone else as a submission window. When it closes: `python -m bench changelog --since <preview commit>` becomes the "launch round" section of the paper, then `python -m bench release --stage published --tag v0`, rebuild, tag.

## Reviews and the heartbeat

- Pull requests: CI runs `verify`, `build`, the drift check, the tests, and `bench review` (re-fetch, span check, model judgment) automatically. Merging is a person's decision; CODEOWNERS requires a maintainer on `data/`, `dockets/`, the verifier and the CONTRACT.
- Daily: `.github/workflows/daily.yml` runs at 13:17 UTC. It re-runs the machine review on every open pull request and posts the report, and spot-checks five confirmed sources for fetch failures, opening an issue if one fails. It runs on GitHub's schedule, not in a chat session, so it does not depend on anyone being present. To have a model judge support on each PR, set `ANTHROPIC_API_KEY` in repository secrets; without it the review still checks quotes.
- Branch protection: require the `contribution-check` workflow to pass before merging, and require one review.

## First week after publishing

5. **Run the audit from a networked machine.** `python -m bench audit --all-imported` re-fetches the 40 imported rows and hashes them into `data/artifacts.csv`; then write `paper/audits/AUDIT-2.md` with verdicts and promote rows.
6. **Submit the dockets.** From a clone of epistemedia, follow `epistemedia research submission-guide` for each of the six `dockets/*/proposal.json` (the `complete` and `submit` steps add the digests and the ready-for-review stamp). Replace the manual v0 certificate with whatever Epistemedia's review returns.
7. **Wayback captures.** For every confirmed source, save a capture and record the `id_` URL in the source's `capture` field so digests are byte-stable.

## First month

8. **Second coder on Dataset A.** Independent pass over strength, harm class, mechanisms, and the 224 assessments; agreement reported in the paper.
9. **Primary sources for Dataset B.** Replace the Wikipedia citations milestone by milestone; the `status` field on each regime says so until done.
10. **Announce with the agent prompt** on the Contribute page, so the first contributions arrive in the format the CI expects.

## Standing

- Tag `v<year>.<n>` at each paper; `python -m bench changelog --since <previous tag>` is the paper's input.
- Re-run `bench outreach` whenever a score moves by more than one anchor.
