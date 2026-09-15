<!-- Machine-read. Keep the headings. -->
## Change type
one of: add-evidence | confirm-row | new-evaluator | new-milestone | docket | correction

## Evaluators or entities touched
comma-separated ids

## New or changed signal ids
comma-separated, or none

## Assessment changes
`<evaluator>.<dim>: <old> -> <new>` per line, or none

## Sources fetched in this run
one URL per line, each with the date you fetched it

## Disclosure
your relationship, if any, to evaluators or labs named in this PR; or "none"

## Checks
- [ ] `python -m bench verify` passes
- [ ] `python -m bench build` run and `graph/`, `dist/` committed
- [ ] `pytest -q` passes
- [ ] every new signal has a `quote` copied exactly from its source
