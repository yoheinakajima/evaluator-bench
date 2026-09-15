# Ledger

Row-level records behind the funding, governance, and personnel dimensions. Four files.

- `entities.csv`: everything that can pay, receive, hold, or sit. `kind` is evaluator, funder, intermediary, daf, lab, investor, person.
- `transfers.csv`: one money movement per row. `measure` is one of grant, recommendation, commitment, transfer, daf_grant, in_kind, investment, contract. Rows are never summed across measures, and a commitment is not a payment. `amount_usd` is empty when undisclosed; the `purpose` and `notes` say what is known.
- `relationships.csv`: one role per row: investor, observer, board, advisor, employee, founder, principal, pays, contractor, donor, office_host, parent. Dates where public. Only public roles.
- `negatives.csv`: bounded absence. Each row names the corpus searched, the snapshot date, and the source, so "none found" means "not in this filing on this date" and nothing more.

Every row carries `source_type` (filing, index, ledger, self, press) and `audit_status` (imported, confirmed, differs, unverifiable). `imported` means the row was copied from another project's ledger and has not been re-derived from the cited source here. The first import is from github.com/kevinnbass/metr-money-figure (research/*.csv, 2026-09-14); the originating row ids are in `notes`. An imported row does not satisfy any verify gate until its status is confirmed.

`python -m bench exposure` reads these files and reports, per evaluator, inflows by measure and by hop distance from a frontier lab or from a person or organization with a stake in one.
