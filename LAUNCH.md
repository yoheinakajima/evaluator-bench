# Launch checklist

State at v0.9: the repository builds, verifies, and tests clean; the site has 200-odd pages with navigation to every item type, a Contribute page with human and agent instructions, a Dockets page, and a Status page. What follows is what a person has to do that a build cannot.

## Before the repository is public

1. **Push and enable Pages.** `git remote add origin git@github.com:yoheinakajima/evaluator-bench.git && git push -u origin main --tags`. In repository settings, set Pages to deploy from GitHub Actions; `.github/workflows/pages.yml` publishes `dist/`. Every link on the site already assumes this repository path.
2. **Fill `DISCLOSURE.md`.** Four bracketed fields. The Method section and the Status page link to it; an empty disclosure on a site about independence is the first thing a reader will notice.
3. **Add the `ANTHROPIC_API_KEY` secret** so the machine-review job can run the model check on pull requests. Without it the job still re-fetches sources and checks quotes.
4. **Decide the right-of-reply timing.** PROCESS.md says two weeks before a score is published or moves by more than one anchor. Packets for the ten organizations whose scores changed are in `outreach/`. Either send them and hold publication for fourteen days, or publish now with each affected evaluator page carrying "reply requested <date>" and file replies as they come. The second is defensible for a v0 with every score marked provisional; say which you chose in the Method section.

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
