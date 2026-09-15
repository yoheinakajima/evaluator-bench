# Launch checklist

v0 is presented as one batch of initial research with a public correction window; corrections after that go through the contribution path and feed the first annual update. Evidence that cannot be re-derived is held, marked, and excluded from figures (PROCESS section 12); it does not move a ranking.

State at v0: the repository builds, verifies, and tests clean; the site has 200-odd pages with navigation to every item type, a Contribute page with human and agent instructions, a Dockets page, and a Status page. What follows is what a person has to do that a build cannot.

## Before the repository is public

1. **Pages and HTTPS.** Pages deploys from GitHub Actions (`.github/workflows/pages.yml` publishes `dist/`); the custom domain evaluatorbench.com is set and HTTPS is enforced (done 2026-09-15).
   Original step: **Push and enable Pages.** The already-created GitHub repository contains only its boilerplate initial commit, so fetch it and replace it with the prepared history using `git push --force-with-lease -u origin main`, then `git push origin v0`. In repository settings, set Pages to deploy from GitHub Actions; `.github/workflows/pages.yml` publishes `dist/`. Every link on the site already assumes this repository path.
2. **Keep `DISCLOSURE.md` current.** Filled by the curator 2026-09-15. The Method section and the Status page link to it; the shared-funders field is a best-effort "none known" and must be updated if that changes.
3. **Add the `ANTHROPIC_API_KEY` secret** so the machine-review job can run the model check on pull requests. Without it the job still re-fetches sources and checks quotes.
4. **Run the gates.** `python -m bench gates` lists what stands between the preview and a citable tag: a quoted span on every binding signal, a second coder on every extreme, a dated contact for every ranked organization and named person, RULES.md published with every conflict resolved, the byline and competence chip on the homepage. `bench release --stage published` refuses while any gate fails. `bench outreach --all` writes the packets; sending them and filling `data/outreach-log.csv` is a person's job. The funder-overlap check in DISCLOSURE.md is also a person's job and is due before the freeze.
5. **Publish as a preview with a two-week window.** `python -m bench release --stage preview --until <date fourteen days after the push>` and rebuild; every page carries the banner. This is the first publication, presented as one batch of initial research. No notices go to individual organizations for it: the preview window, the contribute page, and the right-of-reply issue template are the channel for everyone. When the window closes: `python -m bench changelog --since <preview commit>` becomes the launch-round section, then `python -m bench release --stage published --tag v0`, rebuild, tag. From then on, a published score that moves by more than one anchor triggers `bench outreach <id>` and a fourteen-day wait before the next tag.

## Reviews and the heartbeat

- Pull requests: CI runs `verify`, `build`, the drift check, the tests, and `bench review` (re-fetch, span check, model judgment) automatically. Merging is a person's decision; CODEOWNERS requires a maintainer on `data/`, `dockets/`, the verifier and the CONTRACT.
- Daily: `.github/workflows/daily.yml` runs at 13:17 UTC. It re-runs the machine review on every open pull request and posts the report, and spot-checks five confirmed sources for fetch failures, opening an issue if one fails. It runs on GitHub's schedule, not in a chat session, so it does not depend on anyone being present. To have a model judge support on each PR, set `ANTHROPIC_API_KEY` in repository secrets; without it the review still checks quotes.
- Branch protection: require the always-run `verify` workflow to pass before merging, and require one review.

## First week after publishing

5. **Run the next audit from a networked machine.** Audit the unresolved rows by id (for example, `python -m bench audit T01 T02 T03`), hash the fetches into `data/artifacts.csv`, then write the next `paper/audits/AUDIT-<n>.md` with verdicts. Version 0 has no imported transfer rows left, so `--all-imported` is reserved for future imports rather than a launch task.
6. **Submit the dockets.** From a clone of epistemedia, follow `epistemedia research submission-guide` for each of the six `dockets/*/proposal.json` (the `complete` and `submit` steps add the digests and the ready-for-review stamp). Certificates come only from Epistemedia's independent review.
7. **Wayback captures.** For every confirmed source, save a capture and record the `id_` URL in the source's `capture` field so digests are byte-stable.

## First month

8. **Second coder.** Version 0.1 has one coder. A human second coder, not another lab's model, codes every extreme and the top ten and bottom six before the freeze (`data/coding/second-coder.csv`), the full population by v0.2; agreement is shown on the status page. Public correction continues alongside: everything is published and anyone can file a correction; accepted changes are reported in the annual update with the row that moved them.
9. **Primary sources for Dataset B.** Replace the Wikipedia citations milestone by milestone; the `status` field on each regime says so until done.
10. **Announce with the agent prompt** on the Contribute page, so the first contributions arrive in the format the CI expects.

## Standing

- Tag `v<year>.<n>` at each paper; `python -m bench changelog --since <previous tag>` is the paper's input.
- Re-run `bench outreach` whenever a score moves by more than one anchor.
