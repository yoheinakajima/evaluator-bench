"""Static pages for every entity, regime, and source, plus index pages.

Layout of dist/:
  index.html            the overview (built from site/template.html)
  style.css, site.js    shared stylesheet extracted from the template; tooltip and graph-focus script
  evaluators/index.html scorecard table
  entities/index.html   every ledger entity with distance, rows, confirmed share
  regimes/index.html    the sixteen assurance regimes
  sources/index.html    every cited source with tier and audit status
  entity/<id>.html      everything about one entity, with the funding graph focused on it
  regime/<id>.html      milestones, mechanisms, path signature
  source/<id>.html      the source and everything that cites it

All pages are plain HTML with relative links so GitHub Pages serves them from any base path.
"""
from __future__ import annotations
import json, pathlib, re, html as _html
from .load import ROOT, DIMS
from .ledger import load_ledger, distances, exposure
from .figures import funding_graph
from .paths import paths, analogues, mechanisms, LETTER_LABEL
from .timeline import ladder, STAGES
from .verify import LEDGER_ALIAS

DIST = ROOT / "dist"; SITE = ROOT / "site"
REPO = "https://github.com/yoheinakajima/evaluator-bench/blob/main/"
TIER = {"filing": "tier 1 filing", "index": "tier 1 index", "ledger": "tier 2 ledger", "self": "tier 3 self", "press": "tier 4 press"}

def esc(s) -> str:
    return _html.escape(str(s if s is not None else ""), quote=True)

def badge(status: str | None) -> str:
    st = status or "unaudited"
    col = "color:var(--teal)" if st == "confirmed" else ("color:#7A4E0E" if st == "imported" else "")
    return f'<span class="gid" style="{col}">{esc(st)}</span>'

def tier(x: dict) -> str:
    return f'<span class="gid">{esc(TIER.get(x.get("source_type"), "tier not set"))}</span>'

def money(t: dict) -> str:
    if not t["amount_usd"]: return "undisclosed"
    v = float(t["amount_usd"])
    return f"${v/1e9:.2f}B" if v >= 1e9 else f"${v/1e6:.2f}M"

SITE_JS = r"""
(function(){
  var tip=null;
  function show(el,html){hide();tip=document.createElement('div');tip.className='ltip';tip.innerHTML=html;document.body.appendChild(tip);
    var r=el.getBoundingClientRect();var x=r.left,y=r.bottom+6;if(x+330>window.innerWidth)x=Math.max(8,window.innerWidth-330);tip.style.left=x+'px';tip.style.top=y+'px';}
  function hide(){if(tip){tip.remove();tip=null;}}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  if(!window.__benchTips){
    document.querySelectorAll('.fig [data-tip]').forEach(function(el){
      el.addEventListener('mouseenter',function(){show(el,esc(el.getAttribute('data-tip')));});
      el.addEventListener('mouseleave',hide);
      el.addEventListener('click',function(){var live=el.closest('.fig')&&el.closest('.fig').nextElementSibling;if(live&&live.classList.contains('figlive'))live.textContent=el.getAttribute('data-tip');});
    });
    window.addEventListener('scroll',hide,{passive:true});
  }
  document.querySelectorAll('svg.fundgraph').forEach(function(svg){
    var nodes=svg.querySelectorAll('.node'),edges=svg.querySelectorAll('.edge');
    function focus(id){var keep={};keep[id]=1;edges.forEach(function(e){var a=e.dataset.from,b=e.dataset.to;if(a===id||b===id){keep[a]=1;keep[b]=1;e.classList.remove('dim');}else e.classList.add('dim');});
      nodes.forEach(function(n){if(keep[n.dataset.node])n.classList.remove('dim');else n.classList.add('dim');});}
    function clear(){nodes.forEach(function(n){n.classList.remove('dim');});edges.forEach(function(e){e.classList.remove('dim');});}
    nodes.forEach(function(n){n.addEventListener('mouseenter',function(){focus(n.dataset.node);});n.addEventListener('mouseleave',clear);
      n.addEventListener('click',function(ev){if(ev.target.closest('a'))return;focus(n.dataset.node);});});
  });
})();
"""

GRAPH_CSS = "\n  svg.fundgraph .node.dim,svg.fundgraph .edge.dim{opacity:.1;transition:opacity .15s ease}\n  svg.fundgraph .node{transition:opacity .15s ease}\n  .tbl{width:100%;border-collapse:collapse;font-size:13.5px}\n  .tbl th,.tbl td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--rule-soft);vertical-align:top}\n  .tbl th{font-weight:600;color:var(--muted);font-size:12.5px;background:var(--paper)}\n  .tbl td.num{text-align:right;font-variant-numeric:tabular-nums}\n  .pagehead{padding:30px 0 10px}\n  .pagehead .kicker{color:var(--muted);font-size:14px}\n  .cols{display:grid;grid-template-columns:1fr 1fr;gap:18px 28px}\n  @media (max-width:860px){.cols{grid-template-columns:1fr}}\n  .card{background:var(--panel);border:1px solid var(--rule);border-radius:6px;padding:14px 16px;margin-top:12px}\n  .card h3{font-size:20px;margin-bottom:6px}\n  .card ul{list-style:none;margin:0;padding:0}\n  .card li{padding:7px 0;border-top:1px solid var(--rule-soft);font-size:13.5px}\n  .card li a.src{display:block;color:var(--muted);font-size:12.5px;margin-top:2px}\n  .dimrow{display:grid;grid-template-columns:150px 1fr;gap:10px;padding:10px 0;border-top:1px solid var(--rule-soft)}\n  .dimrow .v{font-weight:600}\n  .dimrow .anchor{color:var(--muted);font-size:12.5px}\n  .dimrow ul{list-style:none;margin:6px 0 0;padding:0}\n  .dimrow li{padding:3px 0 3px 14px;position:relative;font-size:13.5px}\n  .dimrow li::before{content:'';position:absolute;left:0;top:9px;width:8px;height:8px;border-radius:2px;background:var(--teal)}\n  .dimrow li.against::before{background:var(--ox)}\n"

def layout(title: str, body: str, depth: int, active: str = "") -> str:
    pre = "../" * depth
    nav = [("index.html", "Home", "home"), ("evaluators/index.html", "Evaluators", "evaluators"), ("entities/index.html", "Entities", "entities"),
           ("regimes/index.html", "Regimes", "regimes"), ("sources/index.html", "Sources", "sources")]
    links = "".join(f'<a href="{pre}{h}"{" style=\"color:var(--ink)\"" if key == active else ""}>{t}</a>' for h, t, key in nav)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}: Evaluator Bench</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}style.css"></head><body>
<header class="wrap top"><a class="wordmark" href="{pre}index.html">Evaluator <em>Bench</em></a><nav>{links}<a href="https://github.com/yoheinakajima/evaluator-bench">Repo</a></nav></header>
<main class="wrap">{body}</main>
<footer><div class="wrap"><span>Evaluator Bench, an open dataset built on ActiveGraph. Every number traces to a row and a source.</span><span>Generated by bench.site</span></div></footer>
<script src="{pre}site.js"></script></body></html>"""

def write(path: pathlib.Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(html)

# ---------------------------------------------------------------- shared data
def _ctx(bench: dict) -> dict:
    L = load_ledger(); d = distances(L); ex = {x["id"]: x for x in exposure(L)}
    ev_by_ledger = {LEDGER_ALIAS.get(e["id"], e["id"]): e for e in bench["evaluators"]}
    signals_by_source: dict[str, list] = {}
    for e in bench["evaluators"]:
        for s in e["signals"]:
            for sid in s["sources"]: signals_by_source.setdefault(sid, []).append((e, s))
    regs = {p.stem: json.loads(p.read_text()) for p in (ROOT / "data" / "industries").glob("*.json")}
    return dict(L=L, d=d, ex=ex, ev_by_ledger=ev_by_ledger, signals_by_source=signals_by_source, regs=regs,
                paths={p["id"]: p for p in paths()}, analog={a["id"]: a for a in analogues()}, mech={m["id"]: m for m in mechanisms()}, ladder={r["id"]: r for r in ladder()})

# ---------------------------------------------------------------- entity pages
def entity_page(eid: str, bench: dict, C: dict) -> str:
    L, d, E = C["L"], C["d"], C["L"]["entities"]; e = E[eid]; dist = d.get(eid)
    ev = C["ev_by_ledger"].get(eid)
    head = f"""<div class="pagehead"><div class="kicker">{esc(e['kind'])}; distance from a lab: {'unattributed' if dist is None else int(dist)}</div>
      <h1 style="font-size:clamp(32px,5vw,52px)">{esc(e['name'])}</h1><p class="lead">{esc(e.get('notes',''))}</p></div>"""
    parts = [head]
    if ev:
        parts.append(_scorecard(ev, bench, C))
    parts.append(_ledger_block(eid, C))
    parts.append(f'<h2 style="margin-top:26px">Funding graph, focused</h2><p class="lead">Neighbours at full strength, everything else faded. Hover any name to move the focus; click a name to open its page.</p><div class="fig">{funding_graph(focus=eid, L=L)}</div><div class="figlive" aria-live="polite"></div>')
    return layout(e["name"], "".join(parts), 1, "entities")

def _src_link(sid: str, bench: dict) -> str:
    x = bench["sources"].get(sid)
    if not x: return esc(sid)
    return f'<a class="src" href="../source/{esc(sid)}.html">{esc(x["title"])} ({esc(x["publisher"])}{", " + esc(x["published"]) if x.get("published") else ""}) {tier(x)}{badge(x.get("audit_status"))}</a>'

def _scorecard(ev: dict, bench: dict, C: dict) -> str:
    dims = {x["key"]: x for x in bench["dimensions"]}
    floor_k = min(DIMS, key=lambda k: ev["values"][k])
    scores = "; ".join(f"{esc(bench['presets'][k]['label'])} {v}" for k, v in ev["scores"].items())
    rows = []
    for k in DIMS:
        a = ev["assessments"][k]; dm = dims[k]
        sigs = [s for s in ev["signals"] if s["dimension"] == k]
        items = "".join(f'<li class="{s["direction"]}">{esc(s["claim"])}<br>{" ".join(_src_link(x, bench) for x in s["sources"])}<span class="gid">{esc(s.get("as_of") or s["recorded"])}</span></li>' for s in sigs)
        oq = "".join(f"<li>Open: {esc(q)}</li>" for q in a.get("open_questions", []))
        rows.append(f'<div class="dimrow"><div><div class="v">{esc(dm["label"])} {a["value"]}/4</div><div class="anchor">{esc(dm["anchors"][a["value"]])}</div></div><div><div style="font-size:13.5px">{esc(a["rationale"])}</div><ul>{items}{oq}</ul></div></div>')
    ex = C["ex"].get(LEDGER_ALIAS.get(ev["id"], ev["id"]))
    exp = ""
    if ex:
        b = "; ".join(f'{("hop " + k[3:]) if k.startswith("hop") else k}: {v["rows"]} row{"s" if v["rows"] != 1 else ""}' + (" (" + ", ".join(f"{m} ${a/1e6:.1f}M" for m, a in v["by_measure"].items()) + ")" if v["by_measure"] else "") for k, v in ex["buckets"].items())
        ties = ", ".join(f'{esc(t["via"])} ({esc(t["role"])}, distance {t["distance"]}, {esc(t["status"])})' for t in ex["lab_tied_seats"]) or "none within two steps recorded"
        exp = f'<div class="card"><h3>Traced money and ties</h3><p style="font-size:13.5px">{esc(b) if b else "no inflow rows yet"}. Confirmed rows: {ex["confirmed_rows"]} of {ex["inflow_rows"]}. Second hop traced for {ex["second_hop"]["traced"]} of {ex["second_hop"]["sources"]} sources{(": untraced " + esc(", ".join(ex["second_hop"]["untraced"]))) if ex["second_hop"]["untraced"] else ""}. Ties: {ties}. Bounded negatives on file: {len(ex["negatives"])}.</p></div>'
    return f"""<div class="card"><h3>Scorecard</h3><p style="font-size:13.5px">{esc(ev['summary'])}</p>
      <p style="font-size:13.5px;color:var(--muted)">{esc(bench['types'][ev['type']])}, {esc(ev['hq'])}. Confidence {esc(ev['confidence'])}. Domains: {esc(", ".join(ev['domains']))}. Scores by preset: {scores}. Weakest dimension: {esc(dims[floor_k]['label'].lower())} {ev['values'][floor_k]}/4.</p>
      <p style="font-size:13.5px"><b>What would move the score.</b> {esc(ev.get('what_would_move_the_score',''))}</p>
      {''.join(rows)}</div>{exp}"""

def _ledger_block(eid: str, C: dict) -> str:
    L, E = C["L"], C["L"]["entities"]
    link = lambda i: f'<a href="{esc(i)}.html">{esc(E[i]["name"] if i in E else i)}</a>'
    def srcl(url): return f'<a class="src" href="{esc(url)}" target="_blank" rel="noopener">{esc(url)}</a>'
    inflow = [t for t in L["transfers"] if t["to"] == eid]; outflow = [t for t in L["transfers"] if t["from"] == eid]
    held = [r for r in L["relationships"] if r["subject"] == eid]; hosted = [r for r in L["relationships"] if r["object"] == eid]
    negs = [n for n in L["negatives"] if n["evaluator"] == eid]
    def card(title, items):
        return f'<div class="card"><h3>{title}</h3><ul>{"".join(items)}</ul></div>' if items else ""
    a = card("Money in", [f'<li><b>{esc(t["row_id"])}</b> from {link(t["from"])}: {esc(t["measure"])} {money(t)}, {esc(t["date"])}. {esc(t["purpose"])} {badge(t["audit_status"])}<span class="gid">{esc(TIER.get(t["source_type"], ""))}</span>{srcl(t["source_url"])}</li>' for t in inflow])
    b = card("Money out", [f'<li><b>{esc(t["row_id"])}</b> to {link(t["to"])}: {esc(t["measure"])} {money(t)}, {esc(t["date"])}. {esc(t["purpose"])} {badge(t["audit_status"])}{srcl(t["source_url"])}</li>' for t in outflow])
    c = card("Roles held", [f'<li><b>{esc(r["row_id"])}</b> {esc(r["role"])} at {link(r["object"])}{", " + esc(r["start"]) if r["start"] else ""}{" to " + esc(r["end"]) if r["end"] else ""}. {esc(r["notes"])} {badge(r["audit_status"])}{srcl(r["source_url"])}</li>' for r in held])
    dd = card("Roles hosted", [f'<li><b>{esc(r["row_id"])}</b> {link(r["subject"])}: {esc(r["role"])}{", " + esc(r["start"]) if r["start"] else ""}{" to " + esc(r["end"]) if r["end"] else ""}. {esc(r["notes"])} {badge(r["audit_status"])}{srcl(r["source_url"])}</li>' for r in hosted])
    n = card("Bounded negatives", [f'<li><b>{esc(x["row_id"])}</b> {esc(x["claim"])} [{esc(x["searched"])}, snapshot {esc(x["snapshot"])}] {badge(x["audit_status"])}{srcl(x["source_url"])}</li>' for x in negs])
    if not any((a, b, c, dd, n)):
        return f'<div class="card"><h3>Ledger</h3><p style="font-size:13.5px">No rows yet. Add one in <a href="{REPO}data/ledger/">data/ledger/</a>.</p></div>'
    neigh = sorted({t["from"] for t in inflow} | {t["to"] for t in outflow} | {r["object"] for r in held} | {r["subject"] for r in hosted})
    nb = f'<div class="card"><h3>One hop away</h3><p style="font-size:13.5px">{", ".join(link(i) for i in neigh)}</p></div>' if neigh else ""
    return f'<h2 style="margin-top:26px">Ledger</h2><div class="cols"><div>{a}{b}{n}</div><div>{c}{dd}{nb}</div></div>'

# ---------------------------------------------------------------- regime pages
def regime_page(rid: str, C: dict) -> str:
    o = C["regs"][rid]; p = C["paths"][rid]; an = C["analog"].get(rid); m = C["mech"].get(rid); lad = C["ladder"][rid]
    ms = sorted(o["milestones"], key=lambda x: (x["year"], x["kind"]))
    rows = "".join(f'<tr><td class="num">{x["year"]}</td><td>{esc(x["kind"].replace("_", " "))}</td><td>{esc(x["event"])}</td><td class="num">{esc(x.get("strength", ""))}</td><td>{esc(x.get("harm", ""))}{(": " + esc(x["trigger_criterion"])) if x.get("trigger_criterion") else ""}</td><td><a href="{esc(x["source"])}" target="_blank" rel="noopener">source</a></td></tr>' for x in ms)
    stages = "".join(f'<tr><td>{esc(lab)}</td><td class="num">{lad["stages"][c] or "not reached"}</td></tr>' for c, lab, _ in STAGES)
    mech = ""
    if m:
        mech = f'<div class="card"><h3>Mechanisms</h3><table class="tbl"><tr><th></th><th>Before reform</th><th>Now</th></tr>' + "".join(f'<tr><td>{k}</td><td>{esc(m["before"][k])}</td><td>{esc(m["now"][k])}</td></tr>' for k in ("pays", "selects", "access", "publishes", "oversees")) + f'</table><p style="font-size:13px;color:var(--muted);margin-top:8px">{esc(m["note"])}</p></div>'
    sig = " ".join(f'<span class="gid">{c} {esc(LETTER_LABEL[c])}</span>' for c in p["letters"])
    body = f"""<div class="pagehead"><div class="kicker">Assurance regime; jurisdiction {esc(o.get('jurisdiction',''))}</div><h1 style="font-size:clamp(32px,5vw,52px)">{esc(o['name'])}</h1><p class="lead">{esc(o['ai_analogue'])}</p></div>
    <div class="cols"><div><div class="card"><h3>Path signature</h3><p style="font-size:13.5px">{sig}</p><p style="font-size:13px;color:var(--muted)">{('Similarity of its opening to frontier AI: ' + f"{1 - an['distance']:.2f}" + ' (matched opening ' + esc(an['matched_opening']) + ')') if an else 'Reference path.'}</p></div>
    <div class="card"><h3>Stages reached</h3><table class="tbl">{stages}</table></div></div><div>{mech}
    <div class="card"><h3>Payer, access, publication</h3><p style="font-size:13.5px"><b>Who pays.</b> {esc(o['payer'])}<br><b>Access.</b> {esc(o['access'])}<br><b>Publication.</b> {esc(o['publication'])}</p></div></div></div>
    <h2 style="margin-top:26px">Milestones</h2><div class="card"><table class="tbl"><tr><th>Year</th><th>Kind</th><th>Event</th><th>Strength</th><th>Harm</th><th></th></tr>{rows}</table>
    <p style="font-size:12.5px;color:var(--muted);margin-top:8px">{esc(o.get('status',''))} Data: <a href="{REPO}data/industries/{esc(rid)}.json">data/industries/{esc(rid)}.json</a></p></div>"""
    return layout(o["name"], body, 1, "regimes")

# ---------------------------------------------------------------- source pages
def source_page(sid: str, bench: dict, C: dict) -> str:
    x = bench["sources"][sid]
    cites = C["signals_by_source"].get(sid, [])
    items = "".join(f'<li><a href="../entity/{esc(LEDGER_ALIAS.get(e["id"], e["id"]))}.html">{esc(e["name"])}</a>, {esc(s["dimension"])} ({esc(s["direction"])}): {esc(s["claim"])}</li>' for e, s in cites)
    L = C["L"]; E = L["entities"]
    lrows = [t for t in L["transfers"] if t["source_url"] == x["url"]] + [r for r in L["relationships"] if r["source_url"] == x["url"]] + [n for n in L["negatives"] if n["source_url"] == x["url"]]
    litems = "".join(f'<li><b>{esc(r["row_id"])}</b> {esc(r.get("purpose") or r.get("claim") or (r.get("role", "") + " at " + E.get(r.get("object", ""), {}).get("name", "")))} {badge(r["audit_status"])}</li>' for r in lrows)
    body = f"""<div class="pagehead"><div class="kicker">{esc(x['publisher'])}{', ' + esc(x['published']) if x.get('published') else ''}; retrieved {esc(x['retrieved'])} {tier(x)}{badge(x.get('audit_status'))}</div>
    <h1 style="font-size:clamp(28px,4vw,44px)">{esc(x['title'])}</h1><p class="lead"><a href="{esc(x['url'])}" target="_blank" rel="noopener">{esc(x['url'])}</a></p><p class="lead">{esc(x.get('note',''))}</p>
    {('<p class="lead">Imported from ' + esc(x['imported_from']) + '.</p>') if x.get('imported_from') else ''}{('<p class="lead">Found via <a href="' + esc(x['discovered_via']) + '">' + esc(x['discovered_via']) + '</a>.</p>') if x.get('discovered_via') else ''}</div>
    <div class="cols"><div class="card"><h3>Signals citing this source</h3><ul>{items or '<li>none</li>'}</ul></div><div class="card"><h3>Ledger rows citing this URL</h3><ul>{litems or '<li>none</li>'}</ul></div></div>"""
    return layout(x["title"], body, 1, "sources")

# ---------------------------------------------------------------- index pages
def evaluators_index(bench: dict, C: dict) -> str:
    dims = {x["key"]: x for x in bench["dimensions"]}
    rows = []
    for e in sorted(bench["evaluators"], key=lambda e: -e["scores"]["lab"]):
        lid = LEDGER_ALIAS.get(e["id"], e["id"]); fl = min(DIMS, key=lambda k: e["values"][k]); ex = C["ex"].get(lid)
        rows.append(f'<tr><td><a href="../entity/{esc(lid)}.html">{esc(e["name"])}</a><br><span style="color:var(--muted);font-size:12px">{esc(bench["types"][e["type"]])}, {esc(e["hq"])}</span></td>' + "".join(f'<td class="num">{e["scores"][k]}</td>' for k in ("lab", "regulator", "public", "equal")) + f'<td>{esc(dims[fl]["label"].lower())} {e["values"][fl]}</td><td>{esc(e["confidence"])}</td><td class="num">{(str(ex["confirmed_rows"]) + "/" + str(ex["inflow_rows"])) if ex else ""}</td><td>{esc(", ".join(e["domains"]))}</td></tr>')
    body = f"""<div class="pagehead"><h1 style="font-size:clamp(32px,5vw,52px)">Evaluators</h1><p class="lead">{len(bench['evaluators'])} organizations scored on eight independence dimensions. Columns show the weighted score under each preset, the weakest dimension, confidence, and how many ledger inflow rows are confirmed. Open a row for the full scorecard, ledger, and focused graph.</p></div>
    <div class="card"><table class="tbl"><tr><th>Evaluator</th><th>Lab</th><th>Regulator</th><th>Public</th><th>Equal</th><th>Floor</th><th>Confidence</th><th>Confirmed rows</th><th>Domains</th></tr>{''.join(rows)}</table></div>"""
    return layout("Evaluators", body, 1, "evaluators")

def entities_index(C: dict) -> str:
    L, d, E = C["L"], C["d"], C["L"]["entities"]
    cnt_in = {}; cnt_out = {}; conf = {}
    for t in L["transfers"]:
        cnt_in[t["to"]] = cnt_in.get(t["to"], 0) + 1; cnt_out[t["from"]] = cnt_out.get(t["from"], 0) + 1
        if t["audit_status"] == "confirmed": conf[t["to"]] = conf.get(t["to"], 0) + 1
    roles = {}
    for r in L["relationships"]: roles[r["subject"]] = roles.get(r["subject"], 0) + 1; roles[r["object"]] = roles.get(r["object"], 0) + 1
    order = ["lab", "evaluator", "funder", "investor", "intermediary", "daf", "public", "person"]
    rows = []
    for k in order:
        for e in sorted((x for x in E.values() if x["kind"] == k), key=lambda x: x["name"].lower()):
            dd = d.get(e["id"])
            rows.append(f'<tr><td><a href="../entity/{esc(e["id"])}.html">{esc(e["name"])}</a></td><td>{esc(k)}</td><td class="num">{"" if dd is None else int(dd)}</td><td class="num">{cnt_in.get(e["id"], 0)}</td><td class="num">{cnt_out.get(e["id"], 0)}</td><td class="num">{roles.get(e["id"], 0)}</td><td class="num">{conf.get(e["id"], 0)}</td><td style="color:var(--muted);font-size:12.5px">{esc(e.get("notes", ""))}</td></tr>')
    summ = {k: sum(1 for x in E.values() if x["kind"] == k) for k in order}
    body = f"""<div class="pagehead"><h1 style="font-size:clamp(32px,5vw,52px)">Entities</h1><p class="lead">{len(E)} entities in the ledger: {', '.join(f'{v} {k}' for k, v in summ.items() if v)}. Distance 0 is a lab; 1 a direct tie; higher runs through principals and funders. Each page shows every row in and out and the funding graph focused on that node.</p></div>
    <div class="card"><table class="tbl"><tr><th>Entity</th><th>Kind</th><th>Distance</th><th>Money in</th><th>Money out</th><th>Roles</th><th>Confirmed in</th><th>Notes</th></tr>{''.join(rows)}</table></div>"""
    return layout("Entities", body, 1, "entities")

def regimes_index(C: dict) -> str:
    rows = []
    for rid, lad in C["ladder"].items():
        o = C["regs"][rid]; an = C["analog"].get(rid); p = C["paths"][rid]
        rows.append(f'<tr><td><a href="../regime/{esc(rid)}.html">{esc(o["name"])}</a></td><td>{esc(p["letters"])}</td><td class="num">{lad["reached"]}/7</td><td class="num">{lad["first"]}</td><td class="num">{f"{1 - an['distance']:.2f}" if an else "ref"}</td><td>{esc(o.get("jurisdiction", ""))}</td><td style="color:var(--muted);font-size:12.5px">{esc(o["payer"])}</td></tr>')
    body = f"""<div class="pagehead"><h1 style="font-size:clamp(32px,5vw,52px)">Regimes</h1><p class="lead">Sixteen assurance regimes coded as dated milestones. The path signature is the ordered sequence of moves (V voluntary, T trigger, M mandate, S standards, O oversight, I independence, A access or publication, D delegation, P payer shift, R rollback). Similarity compares each regime's opening to frontier AI's path so far.</p></div>
    <div class="card"><table class="tbl"><tr><th>Regime</th><th>Path</th><th>Stages</th><th>First milestone</th><th>Similarity to AI</th><th>Jurisdiction</th><th>Who pays</th></tr>{''.join(rows)}</table></div>"""
    return layout("Regimes", body, 1, "regimes")

def sources_index(bench: dict, C: dict) -> str:
    rows = []
    for sid, x in sorted(bench["sources"].items(), key=lambda kv: (kv[1]["publisher"].lower(), kv[1]["title"].lower())):
        n = len(C["signals_by_source"].get(sid, []))
        rows.append(f'<tr><td><a href="../source/{esc(sid)}.html">{esc(x["title"])}</a></td><td>{esc(x["publisher"])}</td><td>{esc(x.get("published", ""))}</td><td>{esc(TIER.get(x.get("source_type"), "not set"))}</td><td>{badge(x.get("audit_status"))}</td><td class="num">{n}</td></tr>')
    counts = {}
    for x in bench["sources"].values(): counts[x.get("audit_status", "unaudited")] = counts.get(x.get("audit_status", "unaudited"), 0) + 1
    body = f"""<div class="pagehead"><h1 style="font-size:clamp(32px,5vw,52px)">Sources</h1><p class="lead">{len(bench['sources'])} sources cited by signals: {', '.join(f'{v} {k}' for k, v in sorted(counts.items()))}. Tier 1 is a filing or a funder's own index; tier 2 a third-party ledger; tier 3 the organization's own statement; tier 4 press.</p></div>
    <div class="card"><table class="tbl"><tr><th>Source</th><th>Publisher</th><th>Published</th><th>Tier</th><th>Audit</th><th>Signals</th></tr>{''.join(rows)}</table></div>"""
    return layout("Sources", body, 1, "sources")

# ---------------------------------------------------------------- driver
def render_all(bench: dict) -> dict:
    C = _ctx(bench)
    tpl = (SITE / "template.html").read_text()
    css = re.search(r"<style>(.*?)</style>", tpl, re.S).group(1)
    write(DIST / "style.css", css + GRAPH_CSS)
    write(DIST / "site.js", SITE_JS)
    n = 0
    for eid in C["L"]["entities"]:
        write(DIST / "entity" / f"{eid}.html", entity_page(eid, bench, C)); n += 1
    for rid in C["regs"]:
        write(DIST / "regime" / f"{rid}.html", regime_page(rid, C)); n += 1
    for sid in bench["sources"]:
        write(DIST / "source" / f"{sid}.html", source_page(sid, bench, C)); n += 1
    write(DIST / "evaluators" / "index.html", evaluators_index(bench, C))
    write(DIST / "entities" / "index.html", entities_index(C))
    write(DIST / "regimes" / "index.html", regimes_index(C))
    write(DIST / "sources" / "index.html", sources_index(bench, C))
    return {"pages": n + 4}
