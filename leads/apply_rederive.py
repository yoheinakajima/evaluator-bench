"""Apply leads/rederive.json to data/: sources, entities, ledger rows, signals.

    python leads/apply_rederive.py

One-off, like apply_bounds.py. Sources are pulled programmatically from the
agent's verified JSON (58 distinct ids across 8 questions, notes merged on
the handful that recur). Ledger rows, negatives, and signals are applied by
hand below because they need repo-specific judgment (component_of vs
superseded_by, measure separation, row-id assignment) that a mechanical
merge would get wrong — see paper/audits/AUDIT-7.md for the reasoning on
each call. Run once; a second run is a no-op (every write checks first).
"""
import csv, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
LEDGER = DATA / "ledger"
CLOCK = "2026-09-15"
RD = json.loads((ROOT / "leads" / "rederive.json").read_text())

def rd(p): return json.loads(p.read_text())
def wr(p, o, indent=1): p.write_text(json.dumps(o, indent=indent, ensure_ascii=False) + "\n")
def read_csv(name): return list(csv.DictReader(open(LEDGER / name, newline="")))
def write_csv(name, rows, cols):
    with open(LEDGER / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for r in rows: w.writerow({c: r.get(c, "") for c in cols})

log = []

# ---------------------------------------------------------------- 1. sources, pulled from the agent's JSON
by_id: dict[str, dict] = {}
for entry in RD:
    for s in entry["sources"]:
        sid = s["id"]
        if sid in by_id and by_id[sid]["note"] != s["note"]:
            by_id[sid]["note"] = by_id[sid]["note"].rstrip(".") + ". " + s["note"]
        else:
            by_id.setdefault(sid, dict(s))

n_new = n_skip = 0
for sid, fields in by_id.items():
    p = DATA / "sources" / f"{sid}.json"
    if p.exists():
        n_skip += 1; continue
    rec = {k: v for k, v in fields.items() if k != "id"}
    rec = {"id": sid, **rec}
    if rec.get("source_type") != "press": rec.pop("press_kind", None)
    if rec.get("source_type") != "self": rec.pop("self_of", None)
    wr(p, rec); n_new += 1
log.append(f"sources: {n_new} new, {n_skip} already existed (of {len(by_id)} distinct ids cited)")

# ---------------------------------------------------------------- 2. entities
ecols = ["id", "name", "kind", "notes"]
erows = read_csv("entities.csv")
eids = {r["id"] for r in erows}
if "high-tide" not in eids:
    erows.append(dict(id="high-tide", name="High Tide Foundation", kind="funder",
                       notes="Audacious funder collective; EIN 20-1164239; paid RAND directly for Project Canary (990-PF TY2024)"))
    write_csv("entities.csv", erows, ecols)
    log.append("entities: added high-tide")
else:
    log.append("entities: high-tide already present")

# ---------------------------------------------------------------- 3. transfers
tcols = ["row_id", "from", "to", "date", "amount_usd", "measure", "purpose", "source_url", "source_type",
         "snapshot", "audit_status", "notes", "currency", "superseded_by", "component_of", "round_total", "class"]
trows = read_csv("transfers.csv")
tby = {r["row_id"]: r for r in trows}
next_t = max(int(r["row_id"][1:]) for r in trows) + 1

def update_t(row_id, **fields):
    r = tby[row_id]
    for k, v in fields.items(): r[k] = v
    log.append(f"transfers: updated {row_id} ({', '.join(fields)})")

def new_t(**fields):
    global next_t
    if "from_" in fields: fields["from"] = fields.pop("from_")
    rid = f"T{next_t}"; next_t += 1
    r = {c: "" for c in tcols}; r["row_id"] = rid; r.update(fields)
    trows.append(r); tby[rid] = r
    log.append(f"transfers: added {rid} {fields.get('from')}->{fields.get('to')} {fields.get('amount_usd')}")
    return rid

# T08 Apollo cumulative: decomposes into three real grants; the row itself stops being a
# standalone claim (its own URL is gone) without contradicting the total.
update_t("T08", audit_status="unverifiable",
    notes="re-derivation 2026-09-15: coefficientgiving.org/grants/apollo-research-general-support/ 403; the $4,410,180 total decomposes into $1,535,480 (Jun 2023) + $2,178,700 (May 2024), both confirmed on archived Open Philanthropy pages, plus $696,000 (May 2026) that exists only in the removed third-party index and stays imported. Not contradicted; not independently re-derivable as a single row. See the three component rows.")
new_t(from_="coefficient", to="apollo", date="2023-06", amount_usd=1535480, measure="recommendation",
      purpose="startup costs (Open Philanthropy grant page, archived)",
      source_url="https://web.archive.org/web/20230912095624/https://www.openphilanthropy.org/grants/apollo-research-startup-funding/",
      source_type="index", snapshot=CLOCK, audit_status="confirmed", **{"class": "cash"},
      notes="equals Apollo's Manifund self-report of about $1.5M; payment leg not visible under Apollo's name in Good Ventures 990-PF FY2024 (likely paid via fiscal sponsor)")
new_t(from_="coefficient", to="apollo", date="2024-05", amount_usd=2178700, measure="recommendation",
      purpose="general support (Open Philanthropy grant page, archived)",
      source_url="https://web.archive.org/web/20240717140504/https://www.openphilanthropy.org/grants/apollo-research-general-support/",
      source_type="index", snapshot=CLOCK, audit_status="confirmed", **{"class": "cash"},
      notes="page states it follows the June 2023 support")
new_t(from_="coefficient", to="apollo", date="2026-05", amount_usd=696000, measure="recommendation",
      purpose="staff support, per the third-party Algolia extract of Coefficient's index; no public page was ever captured",
      source_url="https://raw.githubusercontent.com/kevinnbass/metr-money-figure/master/research/evaluators.csv",
      source_type="ledger", snapshot="2026-09-11", audit_status="imported", **{"class": "cash"},
      notes="imported kevinnbass/metr-money-figure:EV02; $1,535,480 + $2,178,700 + $696,000 = $4,410,180 = T08's total")

# T09 Irregular/Pattern Labs: confirmed to the dollar against the Good Ventures filing.
update_t("T09", audit_status="confirmed", measure="recommendation", date="2024-02-28",
    notes="re-derivation 2026-09-15: matches Good Ventures 990-PF payments to PATTERN LABS TECH INC ($4,533,333 grant dated 2024-03-05 in FY2024 plus $2,266,667 in FY2025 = $6,800,000, against the index's $6,799,999). Recommendation measure; the payments are the two filing rows below, kept separate (never summed with this row). Imported kevinnbass/metr-money-figure:EV07.")
new_t(from_="good-ventures", to="irregular", date="2024-03-05", amount_usd=4533333, measure="grant",
      purpose="developing software tools, products and analysis focused on global security (990-PF FY2024 Part XV, paid; expenditure-responsibility grant to a non-charity)",
      source_url="https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202501349349105365_public.xml",
      source_type="filing", snapshot=CLOCK, audit_status="confirmed", **{"class": "cash"},
      notes="first tranche of the $6.8M Coefficient-recommended award; grantee had expended $2,639,613 by its 3/15/25 report")
new_t(from_="good-ventures", to="irregular", date="FY2025 (2024-07-01 to 2025-06-30)", amount_usd=2266667, measure="grant",
      purpose="developing software tools, products and analysis focused on global security (approved for future payment in FY2024; paid in FY2025 Part XV)",
      source_url="https://projects.propublica.org/nonprofits/full_text/202641359349102829/IRS990PF",
      source_type="filing", snapshot=CLOCK, audit_status="confirmed", **{"class": "cash"},
      notes="second tranche; $4,533,333 + $2,266,667 = $6,800,000")
new_t(from_="good-ventures", to="irregular", date="2024-06-30", amount_usd=3000000, measure="investment",
      purpose="Pattern Labs Tech Inc listed among Good Ventures' corporate stock holdings at $3,000,000 book and fair value (990-PF FY2024 Part II)",
      source_url="https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202501349349105365_public.xml",
      source_type="filing", snapshot=CLOCK, audit_status="confirmed", **{"class": "ownership"},
      notes="book value of an equity stake, not a round size; stake percentage undisclosed; Good Ventures' principal (Moskovitz) is an Anthropic investor")

# T10/T75 Palisade: the two real awards sum exactly to the old cumulative; T10 stays
# superseded (it already was), T75 gets promoted to confirmed with its real span.
update_t("T10", audit_status="superseded", measure="recommendation",
    notes="re-derivation 2026-09-15: $3,803,463 = $1,680,000 (June 2024) + $2,123,463 (May 2025, two grants), both confirmed on archived Open Philanthropy pages. Not contradicted; the earlier 'contradicted' note was wrong. Superseded by the two real award rows (T75 and the new June-2024 row) so nothing is double-counted. Imported kevinnbass/metr-money-figure:EV19.")
update_t("T75", audit_status="confirmed", date="2025-05",
    purpose="two grants totaling $2,123,463 for general support (Open Philanthropy grant page, archived)",
    source_url="https://web.archive.org/web/20251005184735/https://www.openphilanthropy.org/grants/palisade-research-general-support-2025/",
    notes="re-derived 2026-09-15 from the archived page; this is the 2025 pair only and does not contradict the now-superseded T10")
new_t(from_="coefficient", to="palisade", date="2024-06", amount_usd=1680000, measure="recommendation",
      purpose="general support (Open Philanthropy grant page, archived; amount updated August 2024)",
      source_url="https://web.archive.org/web/20240805094803/https://www.openphilanthropy.org/grants/palisade-research-general-support/",
      source_type="index", snapshot=CLOCK, audit_status="confirmed", **{"class": "cash"},
      notes="first of the two awards behind the $3,803,463 cumulative (T10, now superseded by this row and T75)")

# SecureBio: no existing ledger row at all until this pass.
for date, amt, purpose, url in [
    ("2022-11", 1420937, "biosecurity research, three years (Open Philanthropy grant page, archived)", "https://web.archive.org/web/20230528163412/https://www.openphilanthropy.org/grants/securebio-biosecurity-research/"),
    ("2023-08", 570000, "pathogen early warning project (amount updated October 2024 from $340,000)", "https://web.archive.org/web/20250619192437/https://www.openphilanthropy.org/grants/securebio-pathogen-early-warning-project/"),
    ("2024-11", 4000000, "general support over three years (Open Philanthropy grant page, archived)", "https://web.archive.org/web/20250513041511/https://www.openphilanthropy.org/grants/securebio-general-support/"),
    ("2025-02", 3430000, "Nucleic Acid Observatory program", "https://web.archive.org/web/20250426075953/https://www.openphilanthropy.org/grants/securebio-nucleic-acid-observatory/"),
    ("2025-03", 37000, "AI benchmark improvements: expert baseline for the Virology Capabilities Test", "https://web.archive.org/web/20250711085512/https://www.openphilanthropy.org/grants/securebio-ai-benchmark-improvements/"),
    ("2025-03", 18548, "AI biological capabilities dashboard (page body says $18,550)", "https://web.archive.org/web/20250711091335/https://www.openphilanthropy.org/grants/securebio-ai-biological-capabilities-dashboard/"),
]:
    new_t(from_="coefficient", to="securebio", date=date, amount_usd=amt, measure="recommendation", purpose=purpose,
          source_url=url, source_type="index", snapshot=CLOCK, audit_status="confirmed", **{"class": "cash"}, notes="")
securebio_payment_url_far = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202441369349105564_public.xml"
securebio_payment_url_fy24 = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202501349349105365_public.xml"
securebio_payment_url_fy25 = "https://projects.propublica.org/nonprofits/full_text/202641359349102829/IRS990PF"
new_t(from_="good-ventures", to="securebio", date="FY2023 (2022-07-01 to 2023-06-30)", amount_usd=1420937, measure="grant",
      purpose="research and activities for reducing risks from advanced biotechnologies (990-PF Part XV)",
      source_url=securebio_payment_url_far, source_type="filing", snapshot=CLOCK, audit_status="confirmed", **{"class": "cash"},
      notes="payment leg of the November 2022 recommendation")
new_t(from_="good-ventures", to="securebio", date="FY2024 (2023-07-01 to 2024-06-30)", amount_usd=507000, measure="grant",
      purpose="project on pathogen early warning systems (990-PF Part XV)",
      source_url=securebio_payment_url_fy24, source_type="filing", snapshot=CLOCK, audit_status="confirmed", **{"class": "cash"},
      notes="payment leg of the August 2023 recommendation (later updated to $570,000)")
new_t(from_="good-ventures", to="securebio", date="FY2025 (2024-07-01 to 2025-06-30)", amount_usd=4230000, measure="grant",
      purpose="three Part XV lines: general support 1,400,000; public health early warning system for pandemic preparedness 230,000; general support 2,600,000",
      source_url=securebio_payment_url_fy25, source_type="filing", snapshot=CLOCK, audit_status="confirmed", **{"class": "cash"},
      notes="read from the gzipped ProPublica render")

# METR: Vanguard confirmed; second-hop ARC route; Canary partner-level detail (component
# of the already-confirmed T27 aggregate, so it is never double-summed with it).
update_t("T14", audit_status="confirmed", date="FY2025 (2024-07-01 to 2025-06-30)", amount_usd=4000000,
    source_url="https://projects.propublica.org/nonprofits/full_text/202621329349306657/IRS990ScheduleI", source_type="filing",
    notes="Schedule I row 15424: MODEL EVALUATION AND THREAT RESEARCH, EIN 99-1219864, $4,000,000 FMV, FOR RECIPIENT'S EXEMPT PURPOSE; read 2026-09-15 from the gzipped ProPublica render, corroborated by a full-text search for the name plus METR's ZIP+4 (917231722), which returns only this filing. Underlying donor not public. Imported kevinnbass/metr-money-figure:M87.")
new_t(from_="vanguard-charitable", to="arc", date="FY2025 (2024-07-01 to 2025-06-30)", amount_usd=1500000, measure="daf_grant",
      purpose="990 Schedule I row 547; underlying donor not public",
      source_url="https://projects.propublica.org/nonprofits/full_text/202621329349306657/IRS990ScheduleI",
      source_type="filing", snapshot=CLOCK, audit_status="confirmed", **{"class": "cash"},
      notes="second-hop route for metr.21; same Vanguard filing that pays METR $4,000,000")
new_t(from_="valhalla", to="rand", date="2024", amount_usd=10000000, measure="grant",
      purpose="Project Canary, an artificial intelligence safety initiative (990-PF TY2024 Part XV)",
      source_url="https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202502559349100000_public.xml",
      source_type="filing", snapshot=CLOCK, audit_status="confirmed", **{"class": "cash"}, component_of="T27",
      notes="Audacious partner paying RAND directly for Canary; component of the $38M commitment already recorded at T27, not additive to it")
new_t(from_="high-tide", to="rand", date="2024", amount_usd=333334, measure="grant",
      purpose="'to support the Project Canary' as filed (990-PF TY2024 Part XV)",
      source_url="https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349100135_public.xml",
      source_type="filing", snapshot=CLOCK, audit_status="confirmed", **{"class": "cash"}, component_of="T27",
      notes="component of the $38M Canary commitment (T27), not additive to it")

# UK AISI Alignment Project: T46 already correctly framed; add the re-check.
update_t("T46", notes=tby["T46"]["notes"] + " [re-check 2026-09-15] AISI's own Clarification Questions and How-to-Apply pages confirm the funding agreement is between the funder(s) and the host organisation only, and funds are paid directly to the host organisation: OpenAI's £5.6m funds grants under its own agreement, not AISI's core budget, consistent with this row's original framing.")

write_csv("transfers.csv", trows, tcols)

print("\n".join(log))

# ---------------------------------------------------------------- 4. negatives
ncols = ["row_id", "evaluator", "claim", "searched", "snapshot", "source_url", "source_type", "audit_status", "notes", "answers", "prompted_by"]
nrows = read_csv("negatives.csv")
nby = {r["row_id"]: r for r in nrows}
next_n = max(int(r["row_id"][1:]) for r in nrows) + 1

def update_n(row_id, **fields):
    r = nby[row_id]
    for k, v in fields.items(): r[k] = v
    log.append(f"negatives: updated {row_id} ({', '.join(fields)})")

def new_n(evaluator, claim, searched, source_url, source_type, audit_status, notes, answers="", prompted_by=""):
    global next_n
    rid = f"N{next_n}"; next_n += 1
    r = dict(row_id=rid, evaluator=evaluator, claim=claim, searched=searched, snapshot=CLOCK,
             source_url=source_url, source_type=source_type, audit_status=audit_status, notes=notes,
             answers=answers, prompted_by=prompted_by)
    nrows.append(r); nby[rid] = r
    log.append(f"negatives: added {rid} ({evaluator})")
    return rid

update_n("N01", audit_status="unverifiable",
    searched="Coefficient grants index (third-party Algolia snapshot, 2,911 rows, 2026-09-11); the public index page no longer exists",
    notes="re-derivation 2026-09-15: coefficientgiving.org/grants/ is HTTP 404 to fetch_text and 403 to browser-UA curl; every Wayback capture since 2025-12-06 is 404; the live site search indexes articles, people and pages only and returns no grant record for METR or Model Evaluation. The 2,911-row snapshot is a third-party Algolia extract, not a public record. Superseded in practice by N22 (archived grant-page slugs) and N23 (ProPublica full-text corpus). Imported kevinnbass/metr-money-figure:M33.")
new_n("metr",
    "no METR- or Model-Evaluation-named grant page among 2,737 archived openphilanthropy.org/grants/ slugs, while ARC (2), Apollo Research (2), Palisade Research (2), and SecureBio (6) pages are present",
    "Wayback Machine CDX index of openphilanthropy.org/grants/*, status 200, collapsed by URL, queried by initial letter a to z; 2,737 distinct slugs after dropping query-string and /page/ variants",
    "http://web.archive.org/cdx/search/cdx?url=openphilanthropy.org/grants/m*&collapse=urlkey&fl=original&filter=statuscode:200&limit=20000",
    "index", "confirmed",
    "substitute for N01 after the public index was removed at the Nov 2025 rebrand; absence of a capture is not proof a page never existed")
new_n("metr",
    "Model Evaluation and Threat Research appears in eight e-filed 990 filings only: ARC (Schedules R, N, I, O, 2024), METR's own 990 (2024), Founders Pledge Schedule I (2024), Silicon Valley Community Foundation Schedule I (2024), Vanguard Charitable Schedule I (2025); no filing by Good Ventures, Pew, Packard, a Schmidt-family foundation, or TED Foundation names it",
    "ProPublica Nonprofit Explorer full-text search of e-filed 990-series returns, fiscal years 2014 forward",
    "https://projects.propublica.org/nonprofits/full_text_search?q=%22Model+Evaluation+and+Threat+Research%22",
    "index", "confirmed",
    "corpus-wide; says nothing about grants routed through DAFs under other names or paid after the latest indexed filing")
update_n("N02", audit_status="confirmed",
    searched="990-PF Part XV, fiscal years ending 30 June 2022 to 30 June 2025 (315, 464, 493, and about 900 paid-grant lines)",
    source_url="https://projects.propublica.org/nonprofits/organizations/461008520",
    notes="re-derived 2026-09-15 from IRS e-file XML objects 202341359349105939, 202441369349105564, 202501349349105365 and the gzipped ProPublica full_text render of 202641359349102829; case-insensitive grep for 'model evaluation' and 'metr': none; ARC $1,250,000 in FY2023 only. Imported kevinnbass/metr-money-figure:M104.")
update_n("N03", audit_status="confirmed",
    claim="no METR- or ARC-named grant in the 990-PFs of the three Schmidt-family filers (Eric and Wendy Schmidt Fund for Strategic Innovation TY2020-2024; Schmidt Family Foundation TY2020-2024; Eric and Wendy Schmidt Operating Foundation, short TY2024); Schmidt Sciences itself is not a 990 filer",
    searched="990-PF Part XV of EINs 46-3460261 (5 filings), 20-4170342 (5 filings), 99-5077186 (1 filing)",
    source_url="https://projects.propublica.org/nonprofits/organizations/463460261",
    notes="verdict differs from the imported wording: 'Schmidt Sciences 990-PF 2021 to 2024' does not exist as a corpus (ProPublica API search for 'schmidt sciences' returns 0 organizations); the negative holds for the three foundations that do file. METR names Schmidt Sciences as a supporter; the vehicle is not visible in any 990. Imported kevinnbass/metr-money-figure:M99.")
update_n("N04", audit_status="confirmed",
    searched="990 Schedule I, fiscal years ending 30 June 2021 to 30 June 2025 (439, 407, 401, 391, 535 recipient lines)",
    source_url="https://projects.propublica.org/nonprofits/organizations/562307147",
    notes="re-derived 2026-09-15 from IRS e-file XML objects 202221029349301247, 202340889349301359, 202440829349300334, 202520859349300727, 202620849349301332; no METR, Model Evaluation, or ARC line. Imported kevinnbass/metr-money-figure:M98.")
update_n("N05", audit_status="confirmed",
    searched="990-PF Part XV, tax years 2021 to 2024 (1,400, 1,158, 1,097, 1,029 paid-grant lines)",
    source_url="https://projects.propublica.org/nonprofits/organizations/942278431",
    notes="re-derived 2026-09-15 from IRS e-file XML objects 202223199349107432, 202303149349102680, 202433199349102603, 202533209349100148; no METR, Model Evaluation, or ARC line. Imported kevinnbass/metr-money-figure:M97.")
update_n("N18", notes=nby["N18"]["notes"] + " [re-check 2026-09-15] USAspending's award search for CAISI/Center for AI Standards and Innovation returns no awards at all, so no CAISI contract to METR, Apollo, or other private evaluators is visible there either; still imported pending a NIST procurement-record check (see the new bounded negative on caisi.17).")
update_n("N19", audit_status="confirmed",
    claim="no grant page under Pattern Labs or Irregular among 2,737 archived openphilanthropy.org/grants/ slugs, and no grant record for either name in Coefficient's live site search; the grant itself is recorded in Good Ventures' 990-PF under Pattern Labs Tech Inc",
    notes="re-run 2026-09-15 under both names; the absence is of a public page, not of the grant (see the Good Ventures transfer rows); imported T09 is not contradicted, and is now confirmed against the filing.")
update_n("N21", audit_status="unverifiable",
    notes=nby["N21"]["notes"] + " [re-check 2026-09-15] the grants pages named in 'searched' no longer exist (coefficientgiving.org/grants/ 404 since 2025-12; openphilanthropy.org/grants/ 301s to /funds); see N22 and N23 for the corpora that still exist.")
new_n("metr",
    "no METR, RAND, or Canary grant in TED Foundation Inc 990-PF Part XV, TY2021 to TY2024 (3, 6, 1, and 2 paid-grant lines)",
    "TED Foundation Inc (EIN 82-1934592) 990-PF Part XV, four e-filed returns",
    "https://projects.propublica.org/nonprofits/organizations/821934592", "filing", "confirmed",
    "consistent with the Audacious FAQ: TED does not fund grantees; partners pay directly (Valhalla and High Tide paid RAND in TY2024). TY2025 returns, due late 2026, are where further Canary payments would surface.")
new_n("apollo",
    "no Form D or other filing naming Apollo Research in EDGAR full-text search (2025-01-01 to 2026-09-15); no return of allotment (SH01) at Companies House for Apollo Research AI Ltd after its GBP 0.01 incorporation capital; PSC register states no registrable person",
    "SEC EDGAR full-text search (forms D and unrestricted) and company-name search; Companies House filing history and PSC register for company 15289159 through 2026-04-10",
    "https://efts.sec.gov/LATEST/search-index?q=%22Apollo%20Research%22&forms=D&dateRange=custom&startdt=2025-06-01&enddt=2026-09-15",
    "index", "confirmed",
    "the PBC is a Delaware entity (EIN 93-4310599) and Delaware publishes no cap table; seed round size and Macroscopic's stake are therefore not derivable from public records; a fixed charge to HSBC Innovation Banking (MR01, 9 Dec 2025) is the only financing record on the UK subsidiary")
new_n("caisi",
    "no award or agreement naming the Center for AI Standards and Innovation, CAISI, or 'AI Standards and Innovation' in USAspending's award search (FY2024 to 2026-09-15, all award types)",
    "USAspending spending_by_award API, three keyword queries, all award types; NIST news releases on CAISI agreements",
    "https://api.usaspending.gov/api/v2/search/spending_by_award/", "index", "confirmed",
    "bounded: USAspending carries federal outflows only, so it cannot show a lab paying NIST; NIST's CRADA and reimbursable-agreement records were not searchable; does not on its own satisfy F.9's filing-or-index negative for lab money")
new_n("euaio",
    "Commission Decision C(2024) 390 Article 8 names only Union budget sources for the AI Office: DG CONNECT staff, Digital Europe Programme administrative appropriations for external staff, and DEP Specific Objective 2 for operational expenditure",
    "Commission Decision of 24 January 2024 establishing the European AI Office, C/2024/1459, Article 8 (Official Journal PDF)",
    "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A32024D01459", "filing", "confirmed",
    "a legal act, not a ledger: it fixes the funding source but does not enumerate receipts")
write_csv("negatives.csv", nrows, ncols)

# ---------------------------------------------------------------- 5. signals
def add_signal(eid, sig):
    p = DATA / "signals" / f"{eid}.json"; L = rd(p)
    if any(s["id"] == sig["id"] for s in L):
        log.append(f"signal {sig['id']} already present; skipped"); return
    sig = {"evaluator": eid, "recorded": CLOCK, "curator": "yohei/claude v0.6 (re-derivation)", "as_of": CLOCK, **sig}
    L.append(sig); wr(p, L)
    ap = DATA / "assessments" / f"{eid}.json"; A = rd(ap)
    for a in A:
        if a["dimension"] == sig["dimension"] and sig["id"] not in a["signals"]:
            a["signals"].append(sig["id"])
    wr(ap, A)
    log.append(f"signal {sig['id']} added to {eid}.{sig['dimension']}")

add_signal("metr", dict(id="metr.24", dimension="F", direction="for",
    claim="Bounded negatives re-derived from primary filings on 2026-09-15: no METR-named grant in Good Ventures 990-PF FY2022-2025, Pew 990 Schedule I FY2021-2025, Packard 990-PF TY2021-2024, the three Schmidt-family foundations TY2020-2024, or TED Foundation 990-PF TY2021-2024; ProPublica's full-text index of e-filed 990s names METR in eight filings only.",
    sources=["propublica-metr-fulltext", "good-ventures-propublica", "pew-propublica", "packard-propublica", "schmidt-fsi-propublica"],
    bound={"floor": 3}, rule="F.13",
    quote="Nonprofits (1) People (0) Filings (8)", quote_source="propublica-metr-fulltext"))
add_signal("metr", dict(id="metr.25", dimension="F", direction="against",
    claim="Vanguard Charitable, a donor-advised fund whose underlying donor is not public, paid METR $4,000,000 in its fiscal year to June 2025 per its 990 Schedule I (row 15424), the largest single filing-disclosed grant to METR; the same filing pays ARC $1,500,000.",
    sources=["vanguard-fy2025-schedi-render", "propublica-metr-zip-search"],
    bound={"cap": 3}, rule="F.6",
    quote="Vanguard Charitable Endowment Program — Form 990, Schedule I (2025) Malvern, PA", quote_source="propublica-metr-zip-search"))
add_signal("apollo", dict(id="apollo.16", dimension="F", direction="against",
    claim="Coefficient / Open Philanthropy recommended $1,535,480 (June 2023, startup costs) and $2,178,700 (May 2024, general support) to Apollo per archived grant pages, with a further $696,000 (May 2026) in the removed index; Coefficient's principal funder is an Anthropic investor.",
    sources=["op-apollo-startup-2023", "op-apollo-general-2024", "apollo-manifund"],
    bound={"cap": 3}, rule="F.6",
    quote="Open Philanthropy recommended a grant of $2,178,700 to Apollo Research for general support.", quote_source="op-apollo-general-2024"))
add_signal("apollo", dict(id="apollo.17", dimension="F", direction="against",
    claim="The January 2026 seed round's size and each investor's stake, including Macroscopic Ventures' (an Anthropic Series A and B investor), are undisclosed: no Form D in EDGAR, no share allotment at Companies House, and the PBC is a Delaware entity with no public cap table.",
    sources=["apollo-pbc-round", "edgar-fts-apollo-form-d", "ch-apollo-research-ai-filings", "ch-apollo-research-ai-psc"],
    bound={"cap": 3}, rule="F.10",
    quote="The round was oversubscribed.", quote_source="apollo-pbc-round"))
add_signal("apollo", dict(id="apollo.18", dimension="G", direction="against",
    claim="The PBC board has three seats, of which the 3rd (and later 6th) are designated mission seats; only the first mission director, Daniel Kokotajlo, is named, and the remaining directors are not published on Apollo's pages or in Companies House (which shows only the UK subsidiary's directors, Hobbhahn and Akin).",
    sources=["apollo-pbc-round", "ch-apollo-research-ai-officers", "apollo-team"],
    bound={"cap": 3}, rule="G.8",
    quote="Our first mission director is Daniel Kokotajlo.", quote_source="apollo-pbc-round"))
add_signal("irregular", dict(id="irregular.15", dimension="F", direction="against",
    claim="Good Ventures Foundation, Coefficient's principal funder and an Anthropic investor's foundation, paid Pattern Labs Tech Inc $4,533,333 (grant dated 5 March 2024) and $2,266,667 (FY2025) for developing software tools, products and analysis focused on global security, and held a $3,000,000 stake in the company at 30 June 2024 per its 990-PF.",
    sources=["good-ventures-990pf-fy2024-xml", "good-ventures-990pf-fy2025-render"],
    bound={"cap": 3}, rule="F.6",
    quote="PATTERN LABS TECH INC 108 W 13TH ST STE 100 WILMINGTON DE 19801 2024-03-05 4533333", quote_source="good-ventures-990pf-fy2024-xml"))
add_signal("palisade", dict(id="palisade.14", dimension="F", direction="against",
    claim="Coefficient / Open Philanthropy recommended $1,680,000 (June 2024) and two grants totaling $2,123,463 (May 2025) to Palisade for general support per archived grant pages, $3,803,463 in all; Coefficient's principal funder is an Anthropic investor.",
    sources=["op-palisade-2024", "op-palisade-2025"],
    bound={"cap": 3}, rule="F.6",
    quote="Open Philanthropy recommended two grants totaling $2,123,463 to Palisade Research for general support.", quote_source="op-palisade-2025"))
add_signal("securebio", dict(id="securebio.24", dimension="F", direction="against",
    claim="Coefficient / Open Philanthropy recommended six grants to SecureBio totaling about $9.48M from November 2022 to March 2025, including $4,000,000 general support over three years, paid by Good Ventures Foundation (an Anthropic investor's foundation) per its 990-PFs; only $55,548 of it sits in the AI focus area.",
    sources=["op-securebio-general-2024", "op-securebio-benchmark-2025", "good-ventures-990pf-fy2023-xml", "good-ventures-990pf-fy2024-xml", "good-ventures-990pf-fy2025-render"],
    bound={"cap": 3}, rule="F.6",
    quote="Open Philanthropy recommended a grant of $4,000,000 over three years to SecureBio for general support.", quote_source="op-securebio-general-2024"))
add_signal("caisi", dict(id="caisi.17", dimension="F", direction="for",
    claim="The FY2026 Commerce-Justice-Science joint explanatory statement provides no less than $55,000,000 for NIST's AI research and measurement science and, within it, up to $10,000,000 to expand NIST's AI efforts through the U.S. Center for AI Standards and Innovation: appropriated public money.",
    sources=["cjs-fy2026-jes-division-a", "caisi-funding"],
    bound={"floor": 3}, rule="F.9",
    quote="up to $ I 0,000,000 is to expand on N IST's A l e ffo 11s th ro ugh the U.S. Cente r fo r A l Standards and Innovation", quote_source="cjs-fy2026-jes-division-a"))
add_signal("euaio", dict(id="euaio.14", dimension="F", direction="for",
    claim="Commission Decision C(2024) 390 Article 8 funds the AI Office from DG CONNECT staff, Digital Europe Programme administrative appropriations, and DEP Specific Objective 2 'Artificial Intelligence' for operational expenditure, naming no non-Union source.",
    sources=["eurlex-ai-office-decision-pdf", "euaio-office-decision"],
    bound={"floor": 3}, rule="F.9",
    quote="Operational expenditure of the Office shall be covered by the financial resources allocated to Specific Objective 2", quote_source="eurlex-ai-office-decision-pdf"))
add_signal("ukaisi", dict(id="ukaisi.15", dimension="F", direction="for",
    claim="Alignment Project grants are contracted and paid by each funder directly to the host organisation; DSIT/AISI's own grants are statutory grants under section 5 of the Science and Technology Act 1965 managed by an AISI research lead, and other funders issue their own terms, so OpenAI's £5.6m is not received into AISI's budget even though AISI runs the selection.",
    sources=["alignment-project-cq-pdf", "alignment-project-how-to-apply", "alignment-project-gfa-example"],
    bound={"floor": 3}, rule="F.9",
    quote="the Funding Agreement (GFA) will be between the funder(s) and the host organisation only", quote_source="alignment-project-cq-pdf"))

print("\n".join(log))
print(f"\ntotal log lines: {len(log)}")
