# Dockets

Epistemedia research proposals drafted from Bench evidence. One folder per question.

- `draft.json`: authored proposal in Epistemedia's v0.2 format, results without the generated atom closure.
- `proposal.json`: built by `python -m bench docket build <slug>`; validated by `python -m bench docket validate <slug>`.

A built docket is not a submission. The networked steps (`epistemedia research complete`, `submit`, and a draft pull request) add the artifact digests and the queue entry; a separate reviewer on the Epistemedia side decides whether it is promoted. See `paper/EPISTEMEDIA.md`.
