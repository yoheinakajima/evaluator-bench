"""Static pages for every entity, regime, and source, plus index and topic pages.

Layout of dist/:
  index.html            the directory (built from site/template.html)
  style.css, site.js    shared stylesheet extracted from the template; tooltip and graph-focus script
  evaluators/index.html scorecard tables, one per list (referees, government, commercial and first-party)
  entities/index.html   every ledger entity with distance, rows, confirmed share
  regimes/index.html    the interactive stage ladder, the three regime figures, and the sixteen regimes
  ledger/index.html     the money matrix and the funding graph
  rubric/index.html     dimensions and anchors, what raises and lowers a score, RULES.md, weights, glossary
  cases/index.html      the six cases that set the bar
  method/index.html     how the scores are made, the evidence, and the disclosure
  exclusions/index.html population criteria and every candidate checked
  sources/index.html    every cited source with tier and audit status
  status/index.html     coverage, evidence policies, gates for a citable tag, right-of-reply log
  entity/<id>.html      everything about one entity, with the funding graph focused on it
  regime/<id>.html      milestones, mechanisms, path signature
  source/<id>.html      the source and everything that cites it

All pages are plain HTML with relative links so GitHub Pages serves them from any base path.
"""
from __future__ import annotations
import csv, json, pathlib, re, html as _html
from .load import ROOT, DATA, DIMS
from .ledger import load_ledger, distances, exposure
from .figures import funding_graph
from .paths import paths, analogues, mechanisms, LETTER_LABEL
from .timeline import ladder, STAGES
from .verify import LEDGER_ALIAS
from .policy import POLICIES, POLICY_ORDER, DEFAULT_POLICY, derive, admissible
from .score import BAND_LABEL, BAND_DESC, BAND_ORDER, score, band, coverage
from .roles import ROLE_LABEL, GROUP_LABEL, GROUP_DESC, GROUP_ORDER

DIST = ROOT / "dist"; SITE = ROOT / "site"


def event_digest() -> str:
    """Short sha256 of the event log: the build stamp printed on every page."""
    import hashlib
    ev = ROOT / "graph" / "events.jsonl"
    return hashlib.sha256(ev.read_bytes()).hexdigest()[:12] if ev.exists() else "unknown"
REPO = "https://github.com/yoheinakajima/evaluator-bench/blob/main/"
TIER = {"filing": "tier 1 filing", "index": "tier 1 index", "ledger": "tier 2 ledger", "self": "tier 3 self", "press": "tier 4 press", "docket": "docket draft (not evidence)"}
DIM_LABEL = {"F": "Funding", "G": "Governance", "P": "Personnel", "A": "Access depth", "S": "Scope control", "R": "Publication rights", "M": "Method transparency", "X": "Role incompatibility"}


def esc(s) -> str:
    return _html.escape(str(s if s is not None else ""), quote=True)


def badge(status: str | None) -> str:
    st = status or "unaudited"
    col = "color:var(--teal)" if st == "confirmed" else ("color:#7A4E0E" if st == "imported" else "")
    return f'<span class="gid" style="{col}">{esc(st)}</span>'


def tier(x: dict) -> str:
    t = TIER.get(x.get("source_type"), "tier not set")
    if x.get("source_type") == "press" and x.get("press_kind"): t += f" ({x['press_kind']})"
    if x.get("source_type") == "self" and x.get("self_of"): t += f" ({x['self_of']})"
    return f'<span class="gid">{esc(t)}</span>'


def bandchip(b: str) -> str:
    t = ' title="No floor triggered: no disqualifying conflict on file — not a pass"' if b == "clear" else ""
    return f'<span class="band {esc(b)}"{t}>{esc(BAND_LABEL.get(b, b))}</span>'


def _hidden_score(v) -> str:
    """A weighted composite, hidden until the reader asks for it."""
    return f'<span class="evscore" data-score="{"" if v is None else v}">–</span>'


EVSCORE_REVEAL_SCRIPT = r"""
<script>
(function(){
  var btn = document.getElementById('evscore-reveal');
  if(!btn) return;
  btn.addEventListener('click', function(){
    document.querySelectorAll('.evscore').forEach(function(el){
      var v = el.getAttribute('data-score');
      el.textContent = (v === null || v === '') ? '–' : v;
    });
    btn.textContent = 'Scores revealed';
    btn.setAttribute('disabled', 'disabled');
    var note = document.getElementById('evscore-note');
    if (note) note.textContent = 'Showing the weighted numbers. Two readers with different priorities see different numbers, and both are right; a two-point gap means nothing.';
  });
})();
</script>"""


def money(t: dict) -> str:
    flags = []
    if t.get("superseded_by"): flags.append(f"superseded by {t['superseded_by']} — excluded from sums")
    if t.get("component_of"): flags.append(f"detail of {t['component_of']} — not additive")
    if t.get("round_total"): flags.append("round total, not one investor's check")
    if t.get("audit_status") in ("differs", "unverifiable"): flags.append("quarantined — excluded from sums")
    if t.get("audit_status") == "imported": flags.append("imported figure, not re-derived — never summed")
    if not t["amount_usd"]: base = "undisclosed"
    else:
        v = float(t["amount_usd"])
        base = (f"€{v/1e6:.2f}M (EUR, not converted)" if (t.get("currency") or "USD") == "EUR"
                else (f"${v/1e9:.2f}B" if v >= 1e9 else f"${v/1e6:.2f}M"))
    return base + ("; " + "; ".join(flags) if flags else "")


SITE_JS = r"""
(function(){
  var tip=null;
  function show(el,html){hide();tip=document.createElement('div');tip.className='ltip';tip.innerHTML=html;document.body.appendChild(tip);
    var r=el.getBoundingClientRect();var x=r.left,y=r.bottom+6;if(x+330>window.innerWidth)x=Math.max(8,window.innerWidth-330);tip.style.left=x+'px';tip.style.top=y+'px';}
  function hide(){if(tip){tip.remove();tip=null;}}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  document.querySelectorAll('.fig [data-tip]').forEach(function(el){
    el.addEventListener('mouseenter',function(){show(el,esc(el.getAttribute('data-tip')));});
    el.addEventListener('mouseleave',hide);
    el.addEventListener('click',function(){var live=el.closest('.fig')&&el.closest('.fig').nextElementSibling;if(live&&live.classList.contains('figlive'))live.textContent=el.getAttribute('data-tip');});
  });
  window.addEventListener('scroll',hide,{passive:true});
  document.querySelectorAll('svg.fundgraph').forEach(function(svg){
    var nodes=svg.querySelectorAll('.node'),edges=svg.querySelectorAll('.edge');
    var kind={},col={},down={},up={};
    nodes.forEach(function(n){var id=n.dataset.node;kind[id]=n.dataset.kind||'';col[id]=parseInt(n.dataset.col||'4',10);down[id]=[];up[id]=[];});
    edges.forEach(function(e){var a=e.dataset.from,b=e.dataset.to;if(!(a in down)||!(b in down))return;
      var ca=col[a],cb=col[b];
      if(cb<=ca)down[a].push(b); if(ca<=cb)down[b].push(a);
      if(cb>=ca)up[a].push(b); if(ca>=cb)up[b].push(a);});
    function bfs(g,sources){var d={},q=[];sources.forEach(function(s){if(!(s in d)){d[s]=0;q.push(s);}});while(q.length){var u=q.shift();(g[u]||[]).forEach(function(w){if(!(w in d)){d[w]=d[u]+1;q.push(w);}});}return d;}
    function rev(g){var r={};Object.keys(g).forEach(function(a){(g[a]||[]).forEach(function(b){(r[b]=r[b]||[]).push(a);});});return r;}
    function dtrace(g,id,toLab){var rg=rev(g),d1=bfs(g,[id]),keepN={},keepE={};keepN[id]=1;
      Object.keys(g).forEach(function(t){if(toLab?kind[t]!=='lab':kind[t]!=='evaluator')return;
        var D=d1[t];if(D===undefined)return;var d2=bfs(rg,[t]);
        Object.keys(g).forEach(function(v){if(d1[v]!==undefined&&d2[v]!==undefined&&d1[v]+d2[v]===D)keepN[v]=1;});
        Object.keys(g).forEach(function(a){(g[a]||[]).forEach(function(b){
          if(d1[a]!==undefined&&d2[b]!==undefined&&d1[a]+1+d2[b]===D)keepE[a+'|'+b]=1;});});});
      return {n:keepN,e:keepE};}
    function trace(id){var a=dtrace(down,id,true),b=dtrace(up,id,false),n={},e={};
      [a,b].forEach(function(t){Object.keys(t.n).forEach(function(k){n[k]=1;});Object.keys(t.e).forEach(function(k){e[k]=1;});});
      return {n:n,e:e};}
    function focus(id){var t=trace(id);
      edges.forEach(function(e){var k1=e.dataset.from+'|'+e.dataset.to,k2=e.dataset.to+'|'+e.dataset.from;
        if(t.e[k1]||t.e[k2])e.classList.remove('dim');else e.classList.add('dim');});
      nodes.forEach(function(n){if(t.n[n.dataset.node])n.classList.remove('dim');else n.classList.add('dim');});}
    function clear(){nodes.forEach(function(n){n.classList.remove('dim');});edges.forEach(function(e){e.classList.remove('dim');});}
    nodes.forEach(function(n){n.addEventListener('mouseenter',function(){focus(n.dataset.node);});n.addEventListener('mouseleave',clear);
      n.addEventListener('click',function(ev){if(ev.target.closest('a'))return;focus(n.dataset.node);});});
  });
})();
"""

GRAPH_CSS = "\n  .cols>div,.detail-grid>div,.dimrow>div{min-width:0}\n  .dimrow li,.dimrow .anchor{overflow-wrap:anywhere}\n  @media (max-width:600px){.dimrow{grid-template-columns:1fr}}\n  .card li a.src,.card li,.prov,.sub,.pagehead .lead{overflow-wrap:anywhere;word-wrap:break-word}\n  .card li a.srcurl,.pagehead .lead a{word-break:break-all}\n  .fig{max-width:100%}\n  .paper h1{font-size:26px}.paper h2{font-size:20px;margin-top:22px}.paper h3{font-size:16px;margin-top:16px}.paper p,.paper li{font-size:14.5px;max-width:78ch}.paper table{border-collapse:collapse;font-size:13px;display:block;overflow-x:auto}.paper th,.paper td{border-bottom:1px solid var(--rule-soft);padding:5px 8px;text-align:left}\n  .banner{background:#EAF4F1;border-bottom:1px solid var(--rule);padding:10px 20px;font-size:13.5px;text-align:center}\n  .banner b{font-weight:600}\n  .card table.tbl{display:block;overflow-x:auto;max-width:100%}\n  @media (min-width:900px){.card table.tbl{display:table}}\n  svg.fundgraph .node.dim,svg.fundgraph .edge.dim{opacity:.1;transition:opacity .15s ease}\n  svg.fundgraph .node{transition:opacity .15s ease}\n  .tbl{width:100%;border-collapse:collapse;font-size:13.5px}\n  .tbl th,.tbl td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--rule-soft);vertical-align:top}\n  .tbl th{font-weight:600;color:var(--muted);font-size:12.5px;background:var(--paper)}\n  .tbl td.num{text-align:right;font-variant-numeric:tabular-nums}\n  .pagehead{padding:18px 0 8px}\n  .pagehead h1{font-size:clamp(24px,3.6vw,36px)!important}\n  .pagehead .lead{font-size:14.5px}\n  .pagehead .kicker{color:var(--muted);font-size:14px}\n  .cols{display:grid;grid-template-columns:1fr 1fr;gap:18px 28px}\n  @media (max-width:860px){.cols{grid-template-columns:1fr}}\n  .card{background:var(--panel);border:1px solid var(--rule);border-radius:6px;padding:14px 16px;margin-top:12px}\n  .card h3{font-size:16px;margin-bottom:6px}\n  .card ul{list-style:none;margin:0;padding:0}\n  .card li{padding:7px 0;border-top:1px solid var(--rule-soft);font-size:13.5px}\n  .card li a.src{display:block;color:var(--muted);font-size:12.5px;margin-top:2px}\n  .dimrow{display:grid;grid-template-columns:170px 1fr;gap:10px;padding:10px 0;border-top:1px solid var(--rule-soft)}\n  .dimrow .v{font-weight:600}\n  .dimrow .anchor{color:var(--muted);font-size:12.5px}\n  .dimrow ul{list-style:none;margin:6px 0 0;padding:0}\n  .dimrow li{padding:3px 0 3px 14px;position:relative;font-size:13.5px}\n  .dimrow li::before{content:'';position:absolute;left:0;top:9px;width:8px;height:8px;border-radius:2px;background:var(--teal)}\n  .dimrow li.against::before{background:var(--ox)}\n  .dimrow li.binding{background:var(--teal-tint);border-radius:4px;padding-left:18px}\n  .dimrow li.binding::before{left:4px}\n  .dimrow li.out{opacity:.55}\n  .dimrow .derived{font-size:13.5px;margin:0 0 4px;max-width:72ch}\n  .dimrow .derived.dark{color:var(--muted);font-style:italic}\n  .quote{display:block;font-size:12.5px;border-left:2px solid var(--rule);padding-left:8px;margin:3px 0}\n  .rules h1{font-size:24px}.rules h2{font-size:19px;margin-top:22px}.rules h3{font-size:16px;margin-top:14px}.rules p,.rules li{font-size:14.5px;max-width:78ch}.rules ul{padding-left:20px}\n  .gate-ok{color:var(--teal);font-weight:600}.gate-fail{color:var(--ox);font-weight:600}\n  .rdim{border-top:2px solid var(--ink);padding-top:10px}.rdim h3{font-size:17px;margin-bottom:4px}.rdim p{font-size:14px;color:var(--muted);margin-bottom:8px}\n  .anchors{list-style:none;margin:0;padding:0;font-size:13px}.anchors li{display:grid;grid-template-columns:20px 1fr;gap:8px;padding:3px 0;border-top:1px solid var(--rule-soft)}.anchors li b{font-weight:600;color:var(--teal)}\n  .rubric{display:grid;grid-template-columns:repeat(2,1fr);gap:14px 28px;margin-top:22px}@media (max-width:820px){.rubric{grid-template-columns:1fr}}\n  .signals{display:grid;grid-template-columns:1fr 1fr;gap:22px 36px;margin-top:20px}@media (max-width:820px){.signals{grid-template-columns:1fr}}\n  .signals .ev li{max-width:none}\n  .cases{display:grid;gap:14px;margin-top:20px}.case{display:grid;grid-template-columns:200px 1fr;gap:18px;padding:14px 0;border-top:1px solid var(--rule)}@media (max-width:720px){.case{grid-template-columns:1fr;gap:6px}}.case h3{font-size:16px}.case .verdict{font-size:12.5px;color:var(--muted);margin-top:4px}.case p{font-size:14px;max-width:70ch}\n  .lwrap{overflow-x:auto;margin-top:18px;border:1px solid var(--rule);border-radius:6px;background:var(--panel)}\n  .lgrid{display:grid;grid-template-columns:230px repeat(7,86px) 150px;min-width:max-content;font-size:13px}\n  .lrow{display:contents}\n  .lgrid .lname,.lgrid .lcell,.lgrid .lbar{padding:6px 8px;border-bottom:1px solid var(--rule-soft);display:flex;align-items:center;min-height:34px}\n  .lgrid .lname{position:sticky;left:0;background:var(--panel);z-index:1;justify-content:space-between;gap:8px;text-align:left}\n  .lgrid .lhead .lname,.lgrid .lhead .lcell,.lgrid .lhead .lbar{background:var(--paper);font-weight:600;border-bottom:1px solid var(--rule);justify-content:center;min-height:38px}\n  .lgrid .lhead .lname{justify-content:flex-start}\n  .lgrid .lhead .lcell{cursor:help}\n  .lcell{justify-content:center}\n  .lcell button,.lname button{font:inherit;border:none;cursor:pointer;width:100%;height:100%;min-height:26px;border-radius:3px;color:var(--ink);background:none;text-align:inherit;padding:0 4px}\n  .lname button{display:flex;justify-content:space-between;align-items:center;gap:8px}\n  .lcell button.s0{background:var(--teal-tint)} .lcell button.s1{background:#8CC5BB} .lcell button.s2{background:var(--teal);color:#fff}\n  .lcell button.sn{background:none;border:1px dashed var(--rule);color:var(--muted)}\n  .lcell button:hover,.lname button:hover{outline:2px solid var(--ink);outline-offset:-2px}\n  .lcell button[aria-pressed=\"true\"],.lname button[aria-pressed=\"true\"]{outline:2px solid var(--ink);outline-offset:-2px}\n  .lrow.ai .lname,.lrow.ai .lcell,.lrow.ai .lbar{background:#EAF4F1}\n  .lrow.ai .lname{font-weight:600}\n  .lbar i{display:block;height:10px;background:var(--teal);opacity:.75;border-radius:2px;margin-right:6px}\n  .lbar{color:var(--muted);font-size:12px}\n  .marks{display:inline-flex;gap:6px;align-items:center}\n  .dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--ox)}\n  .ring{display:inline-block;width:8px;height:8px;border-radius:50%;border:2px solid var(--amber);box-sizing:border-box}\n  .llegend{display:flex;flex-wrap:wrap;gap:8px 16px;font-size:12.5px;color:var(--muted);margin-top:8px;align-items:center}\n  .llegend span{margin-right:12px}\n  .llegend .sw{display:inline-block;width:14px;height:10px;border-radius:2px;vertical-align:middle;margin-right:4px}\n  .sw.s0{background:var(--teal-tint)} .sw.s1{background:#8CC5BB} .sw.s2{background:var(--teal)} .sw.sn{border:1px dashed var(--rule)}\n  .llegend a{color:var(--muted);margin-left:auto}\n  .ldetail{margin-top:12px;background:var(--panel);border:1px solid var(--rule);border-radius:6px;padding:14px 16px}\n  .ldetail h3{font-size:17px;margin-bottom:4px}\n  .ldetail .sub{color:var(--muted);font-size:13.5px;margin-bottom:10px;max-width:70ch}\n  .ldetail ul{list-style:none;margin:0;padding:0}\n  .ldetail li{padding:8px 0;border-top:1px solid var(--rule-soft);font-size:14px;max-width:72ch}\n  .ldetail li b{font-weight:600;margin-right:6px}\n  .ldetail .kind{font-size:11.5px;color:var(--muted);border:1px solid var(--rule);border-radius:4px;padding:0 6px;margin-left:6px;vertical-align:middle}\n  .ldetail li a{color:var(--muted);font-size:12.5px;display:block;margin-top:2px}\n  .ldetail .ctx{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px 20px;margin-top:12px;font-size:13px;color:var(--ink)}\n  .ldetail .ctx b{display:block;font-weight:600;font-size:12.5px;color:var(--muted);margin-bottom:2px}\n  .ldetail .close{float:right;font-size:13px;background:none;border:1px solid var(--rule);border-radius:999px;padding:3px 10px;color:var(--muted)}\n  .ltip{position:fixed;z-index:20;max-width:320px;background:var(--ink);color:#fff;font-size:12.5px;line-height:1.4;padding:8px 10px;border-radius:6px;pointer-events:none;box-shadow:0 4px 14px rgba(0,0,0,.18)}\n  @media (hover:none){.ltip{display:none!important}}\n  .figlive{font-size:13.5px;color:var(--ink);background:var(--panel);border:1px solid var(--rule);border-top:none;border-radius:0 0 6px 6px;padding:8px 12px;max-width:100%;min-height:0}\n  .figlive:empty{display:none}\n  [data-tip]:hover rect,[data-tip]:hover circle{filter:brightness(1.12)}\n"


def release_banner(pre: str) -> str:
    rp = ROOT / "data" / "release.json"
    if not rp.exists(): return ""
    r = json.loads(rp.read_text())
    if r.get("stage") == "preview":
        return f'<div class="banner">Preview of the first release. Everything here is one batch of initial research, and every score is provisional until <b>{esc(r.get("window_until") or "the window closes")}</b>. Organizations and people named here, and anyone else, can submit corrections or evidence until then; what arrives becomes the launch round of the paper. No tag is citable until the <a href="{pre}status/index.html">gates</a> pass. <a href="{pre}contribute/index.html">How to submit</a>.{(" " + esc(r["note"])) if r.get("note") else ""}</div>'
    if r.get("stage") == "published":
        return f'<div class="banner">Published as <b>{esc(r.get("tag") or "v0")}</b> on {esc(r.get("set_on"))}. Scores continue to move as evidence is merged; the next dated reading is the annual update. <a href="{pre}contribute/index.html">Submit evidence</a>.</div>'
    return ""


def _ranked_signals(bench: dict):
    ranked = {e["id"] for e in bench["evaluators"] if e.get("status", "ranked") == "ranked"}
    return [s for e in bench["evaluators"] if e["id"] in ranked for s in e["signals"]]


def evidence_summary(bench: dict) -> str:
    """Build the evidence text from the same projection it describes."""
    signals = _ranked_signals(bench)
    sources = {sid: bench["sources"][sid] for s in signals for sid in s["sources"]}
    pct = lambda n, d: round(100 * n / d) if d else 0
    self_count = sum(s.get("source_type") == "self" for s in sources.values())
    tier1_count = sum(s.get("source_type") in ("filing", "index") for s in sources.values())
    quote_count = sum(bool(s.get("quote")) for s in signals)
    std = sum(1 for s in signals if admissible(s, bench["sources"], "standard"))
    prim = sum(1 for s in signals if admissible(s, bench["sources"], "primary"))
    return (
        "The scores measure what the public record shows, and the public record is largely what the evaluators say about themselves. "
        f"Among the {len(sources)} unique sources cited by {len(signals)} signals for the ranked population, {self_count} ({pct(self_count, len(sources))}%) are tier-3 self-published and {tier1_count} ({pct(tier1_count, len(sources))}%) are tier-1 sources (regulatory filings or public indexes). "
        f"{quote_count} of {len(signals)} signals ({pct(quote_count, len(signals))}%) carry an exact quoted span. "
        f"Under the Retrieved & confirmed evidence policy {std} of {len(signals)} signals count; under the Primary only policy {prim} do. "
        "That scarcity is a finding, not a data gap to be patched: the field's independence cannot yet be verified from outside the field. "
        "An evidence-based score would reward silence if silence defaulted to a number; here an unevidenced dimension renders as a dash and is excluded from the score, and every card shows the evidence tier of what it rests on."
    )


def policy_table(bench: dict, pre: str = "") -> str:
    signals = _ranked_signals(bench); ranked = [e for e in bench["evaluators"] if e.get("status", "ranked") == "ranked"]
    rows = []
    for p in POLICY_ORDER:
        adm = sum(1 for s in signals if admissible(s, bench["sources"], p))
        dark = sum(1 for e in ranked for k in DIMS if e["values_by_policy"][p][k] is None)
        rows.append(f'<tr{" style=\"background:var(--teal-tint)\"" if p == DEFAULT_POLICY else ""}><td>{esc(POLICIES[p]["label"])}{" (default)" if p == DEFAULT_POLICY else ""}</td><td style="color:var(--muted)">{esc(POLICIES[p]["desc"])}</td><td class="num">{adm} of {len(signals)}</td><td class="num">{dark} of {len(ranked) * len(DIMS)}</td></tr>')
    return f'<table class="tbl"><tr><th>Evidence policy</th><th>Rule</th><th>Ranked signals that count</th><th>Assessments unevidenced</th></tr>{"".join(rows)}</table>'


def layout(title: str, body: str, depth: int, active: str = "") -> str:
    pre = "../" * depth
    nav = [("index.html", "Directory", "home"), ("rubric/index.html", "Rubric and rules", "rubric"), ("regimes/index.html", "Where we are", "regimes"), ("ledger/index.html", "Money", "ledger"),
           ("evaluators/index.html", "Evaluators", "evaluators"), ("entities/index.html", "Entities", "entities"), ("sources/index.html", "Sources", "sources"), ("cases/index.html", "Cases", "cases"),
           ("paper/index.html", "Paper", "paper"), ("method/index.html", "Method", "method"), ("exclusions/index.html", "Population", "exclusions"), ("status/index.html", "Status", "status"), ("contribute/index.html", "Contribute", "contribute")]
    links = "".join(f'<a href="{pre}{h}"{" style=\"color:var(--ink)\"" if key == active else ""}>{t}</a>' for h, t, key in nav)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}: Evaluator Bench</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%230F766E'/%3E%3Crect x='14' y='18' width='36' height='6' rx='2' fill='%23fff'/%3E%3Crect x='14' y='29' width='26' height='6' rx='2' fill='%23fff'/%3E%3Crect x='14' y='40' width='36' height='6' rx='2' fill='%23fff'/%3E%3C/svg%3E">
<meta property="og:title" content="{esc(title)}: Evaluator Bench"><meta property="og:image" content="https://evaluatorbench.com/og.png"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&family=Manrope:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}style.css"></head><body>
<header class="wrap top"><a class="wordmark" href="{pre}index.html">Evaluator <em>Bench</em></a><nav>{links}<a href="https://github.com/yoheinakajima/evaluator-bench">Repo</a></nav></header>
{release_banner(pre)}<main class="wrap">{body}</main>
<footer><div class="wrap"><span>Evaluator Bench, an open dataset built on ActiveGraph. Every number traces to a row and a source.</span><span>Generated by bench.site · build {event_digest()}</span></div></footer>
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
      <h1>{esc(e['name'])}</h1><p class="lead">{esc(e.get('notes',''))}</p></div>"""
    parts = [head]
    if ev:
        parts.append(_scorecard(ev, bench, C))
    parts.append(_ledger_block(eid, C))
    parts.append(f'<h2 style="margin-top:26px">Funding graph, focused</h2><p class="lead">Every one-way chain to a lab and to an evaluator at full strength, everything else faded. Hover any name to trace its connections; click a name to open its page.</p><div class="fig">{funding_graph(focus=eid, L=L)}</div><div class="figlive" aria-live="polite"></div>')
    return layout(e["name"], "".join(parts), 1, "entities")


def _src_link(sid: str, bench: dict) -> str:
    x = bench["sources"].get(sid)
    if not x: return esc(sid)
    return f'<a class="src" href="../source/{esc(sid)}.html">{esc(x["title"])} ({esc(x["publisher"])}{", " + esc(x["published"]) if x.get("published") else ""}) {tier(x)}{badge(x.get("audit_status"))}</a>'


def _bound_text(s: dict) -> str:
    b = s.get("bound")
    if not b: return f"informational ({esc(s.get('bound_note', ''))})" if s.get("bound_note") else "informational"
    return (f"caps at {b['cap']}" if "cap" in b else f"floors at {b['floor']}") + (f" by {esc(s['rule'])}" if s.get("rule") else "")


def _scorecard(ev: dict, bench: dict, C: dict) -> str:
    dims = {x["key"]: x for x in bench["dimensions"]}
    vals = ev["values_by_policy"][DEFAULT_POLICY]; b = band(vals); cov = coverage(vals)
    scores = "; ".join(f"{esc(bench['presets'][k]['label'])} {_hidden_score(v)}" for k, v in ev["scores"].items())
    fl = ev.get("floor")
    rows = []
    for k in DIMS:
        a = ev["assessments"][k]; dm = dims[k]; dd = a["derived"][DEFAULT_POLICY]; v = dd["v"]
        sigs = [s for s in ev["signals"] if s["dimension"] == k]
        items = "".join(f'<li class="{s["direction"]}{" binding" if s["id"] in dd["b"] else ""}{" out" if s["id"] in dd["x"] else ""}">{esc(s["claim"])} <span class="gid">{_bound_text(s)}</span>{"<span class=\"gid\" style=\"color:var(--teal)\">binding</span>" if s["id"] in dd["b"] else ""}{"<span class=\"gid\">not counted under standard</span>" if s["id"] in dd["x"] else ""}{("<span class=\"quote\">&ldquo;" + esc(s["quote"]) + "&rdquo;</span>") if s.get("quote") else ""}<br>{" ".join(_src_link(x, bench) for x in s["sources"])}<span class="gid">{esc(s.get("as_of") or s["recorded"])}</span></li>' for s in sigs)
        oq = "".join(f"<li>Document request: {esc(q)}</li>" for q in a.get("open_questions", []))
        flags = ""
        if a.get("mechanism"): flags += f'<div class="gid mech" style="margin-top:4px">mechanism: {esc(a["mechanism"])}</div>'
        if dd["h"]: flags += '<div class="gid" style="margin-top:4px;color:#7A4E0E;border-color:#7A4E0E">held at a supportable anchor</div>'
        if dd["c"]: flags += '<div class="gid" style="margin-top:4px;color:var(--ox);border-color:var(--ox)">floor and cap disagree</div>'
        leads = ev["values"][k]
        left = (f'<div class="v">{esc(dm["label"])} {"–" if v is None else str(v) + "/4"}</div>'
                + (f'<div class="anchor">{"No admissible evidence under the standard policy." if v is None else "Anchor " + str(v) + ": " + esc(dm["anchors"][v])}</div>')
                + (f'<div class="anchor">With leads included: {leads}/4</div>' if leads != v else "")
                + f'<div class="anchor" style="margin-top:4px">evidence: {esc(a.get("evidence_tier","unknown"))}</div>{flags}')
        right = f'<div class="derived {"dark" if v is None else ""}">{esc(a["rationale_derived"])}</div>'
        if a.get("rationale"): right += f'<div class="derived" style="color:var(--muted)">Curator: {esc(a["rationale"])}</div>'
        if a.get("resolution"): right += f'<div class="derived">Resolution: {esc(a["resolution"].get("rule"))} decides {esc(a["resolution"].get("value"))}. {esc(a["resolution"].get("note"))}</div>'
        rows.append(f'<div class="dimrow"><div>{left}</div><div>{right}<ul>{items}{oq}</ul></div></div>')
    # policy mini-table
    ptbl = '<table class="tbl"><tr><th>Dimension</th>' + "".join(f"<th>{esc(POLICIES[p]['label'])}</th>" for p in POLICY_ORDER) + "</tr>"
    for k in DIMS:
        ptbl += f"<tr><td>{esc(dims[k]['label'])}</td>" + "".join(f'<td class="num">{"–" if ev["values_by_policy"][p][k] is None else ev["values_by_policy"][p][k]}</td>' for p in POLICY_ORDER) + "</tr>"
    for pname in bench["presets"]:
        ptbl += f"<tr><td>Score, {esc(bench['presets'][pname]['label'])}</td>" + "".join(f'<td class="num">{_hidden_score(ev["scores_by_policy"][p][pname]["score"])} <span class="gid">{("not ranked" if ev.get("status", "ranked") != "ranked" else esc(BAND_LABEL[ev["scores_by_policy"][p][pname]["band"]]))}, {ev["scores_by_policy"][p][pname]["coverage"]}/8</span></td>' for p in POLICY_ORDER) + "</tr>"
    ptbl += "</table>"
    moves = ev.get("what_moves", {}).get("lab", [])[:3]
    mv = "".join(f'<li>{esc(DIM_LABEL[m["dimension"]])} {m["from_value"]} to {m["to_value"]}: score {_hidden_score(m["score"])}{(", band becomes " + BAND_LABEL[m["band"]].lower()) if BAND_ORDER[m["band"]] < BAND_ORDER[b] else ""}</li>' for m in moves)
    dissent = ev.get("dissent") or {}
    ex = C["ex"].get(LEDGER_ALIAS.get(ev["id"], ev["id"]))
    exp = ""
    if ex:
        bb = "; ".join(f'{("hop " + k[3:]) if k.startswith("hop") else k}: {v["rows"]} row{"s" if v["rows"] != 1 else ""}' + (" (" + ", ".join(f"{m} ${a/1e6:.1f}M" for m, a in v["by_measure"].items()) + ")" if v["by_measure"] else "") for k, v in ex["buckets"].items())
        ties = ", ".join(f'{esc(t["via"])} ({esc(t["role"])}, distance {t["distance"]}, {esc(t["status"])})' for t in ex["lab_tied_seats"]) or "none within two steps recorded"
        exp = f'<div class="card"><h3>Traced money and ties</h3><p style="font-size:13.5px">{esc(bb) if bb else "no inflow rows yet"}. Confirmed rows: {ex["confirmed_rows"]} of {ex["inflow_rows"]}{(" (" + str(ex["quarantined_rows"]) + " excluded after a re-fetch disagreed or could not be verified: " + ", ".join(ex["quarantined_ids"]) + ")") if ex["quarantined_rows"] else ""}{(" Evaluation credits recorded but never counted: " + ", ".join(ex["credit_ids"]) + ".") if ex.get("credit_rows") else ""} Dollar sums: confirmed + unaudited USD rows only; imported figures are not re-derived and never summed. Second hop traced for {ex["second_hop"]["traced"]} of {ex["second_hop"]["sources"]} sources{(": untraced " + esc(", ".join(ex["second_hop"]["untraced"]))) if ex["second_hop"]["untraced"] else ""}. Ties: {ties}. Checked and not found: {len(ex["negatives"])}.</p></div>'
    return f"""<div class="card"><h3>Scorecard</h3><p style="font-size:13.5px">{esc(ev['summary'])}</p>
      {('<p style="font-size:13.5px;border-left:3px solid var(--amber);padding-left:10px">' + esc(ev['funding_tension']) + '</p>') if ev.get('funding_tension') else ''}
      <p style="font-size:13.5px;color:var(--muted)">{esc(bench['types'][ev['type']])}, {esc(ev['hq'])}. {esc(ROLE_LABEL.get(ev['role'], ev['role']))}; listed with {esc(GROUP_LABEL.get(ev.get('list_group', 'referee'), '').lower())}. Confidence {esc(ev['confidence'])}. Domains: {esc(", ".join(ev['domains']))}.</p>
      <p style="font-size:13.5px">{bandchip(b) if ev.get("status", "ranked") == "ranked" else '<span class="band" style="color:var(--muted)">not ranked</span>'} <span class="gid">{cov}/8 evidenced · {esc(POLICIES[DEFAULT_POLICY]["label"])}</span> Scores by preset: {scores}. Weakest evidenced dimension: {esc(dims[fl]['label'].lower()) if fl else 'none'} {vals[fl] if fl else ''}{'/4' if fl else ''}.{(" " + esc(BAND_DESC[b])) if ev.get("status", "ranked") == "ranked" else ""}{" No floor triggered means no disqualifying conflict is on file, not a pass." + (" Partial evidence (" + str(cov) + "/8)." if cov < 8 else " Full evidence.") if b == "clear" and ev.get("status", "ranked") == "ranked" else ""}</p>
      <p style="font-size:13px;color:var(--muted)" id="evscore-note">The weighted numbers are hidden until you ask for them: two readers with different priorities see different numbers, and neither is the site's. <button class="cta small" id="evscore-reveal">Reveal weighted scores</button></p>
      <p style="font-size:13.5px"><b>What would move the score.</b> {esc(ev.get('what_would_move_the_score',''))}</p>{('<ul style="font-size:13.5px;margin:0 0 8px 18px">' + mv + '</ul>') if mv else ''}
      {('<p style="font-size:13.5px"><b>Dissent, lower.</b> ' + esc(dissent.get('lower')) + '</p><p style="font-size:13.5px"><b>Dissent, higher.</b> ' + esc(dissent.get('higher')) + '</p>') if dissent else ''}
      <p style="font-size:12.5px;color:var(--muted)">Each value is the tightest admissible cap or, with no cap, the highest admissible floor, under <a href="{REPO}RULES.md">RULES.md</a>. The binding signal is highlighted. A dash means no admissible signal sets a bound under the Retrieved & confirmed policy.</p>
      {''.join(rows)}</div>
      <div class="card"><h3>Values under each evidence policy</h3>{ptbl}</div>{exp}{EVSCORE_REVEAL_SCRIPT}"""


def _ledger_block(eid: str, C: dict) -> str:
    L, E = C["L"], C["L"]["entities"]
    link = lambda i: f'<a href="{esc(i)}.html">{esc(E[i]["name"] if i in E else i)}</a>'
    def srcl(url): return f'<a class="src srcurl" href="{esc(url)}" target="_blank" rel="noopener">{esc(url)}</a>'
    inflow = [t for t in L["transfers"] if t["to"] == eid]; outflow = [t for t in L["transfers"] if t["from"] == eid]
    held = [r for r in L["relationships"] if r["subject"] == eid]; hosted = [r for r in L["relationships"] if r["object"] == eid]
    negs = [n for n in L["negatives"] if n["evaluator"] == eid]
    def card(title, items):
        return f'<div class="card"><h3>{title}</h3><ul>{"".join(items)}</ul></div>' if items else ""
    a = card("Money in", [f'<li><b>{esc(t["row_id"])}</b> from {link(t["from"])}: {esc(t["measure"])} {money(t)}, {esc(t["date"])}. {esc(t["purpose"])} {badge(t["audit_status"])}<span class="gid">{esc(TIER.get(t["source_type"], ""))}</span>{srcl(t["source_url"])}</li>' for t in inflow])
    b = card("Money out", [f'<li><b>{esc(t["row_id"])}</b> to {link(t["to"])}: {esc(t["measure"])} {money(t)}, {esc(t["date"])}. {esc(t["purpose"])} {badge(t["audit_status"])}{srcl(t["source_url"])}</li>' for t in outflow])
    c = card("Roles held", [f'<li><b>{esc(r["row_id"])}</b> {esc(r["role"])} at {link(r["object"])}{", " + esc(r["start"]) if r["start"] else ""}{" to " + esc(r["end"]) if r["end"] else ""}. {esc(r["notes"])} {badge(r["audit_status"])}{srcl(r["source_url"])}</li>' for r in held])
    dd = card("Roles hosted", [f'<li><b>{esc(r["row_id"])}</b> {link(r["subject"])}: {esc(r["role"])}{", " + esc(r["start"]) if r["start"] else ""}{" to " + esc(r["end"]) if r["end"] else ""}. {esc(r["notes"])} {badge(r["audit_status"])}{srcl(r["source_url"])}</li>' for r in hosted])
    n = card("Checked and not found", [f'<li><b>{esc(x["row_id"])}</b> {esc(x.get("answers") or x["claim"])}<br><span style="color:var(--muted)">Searched {esc(x["searched"])}, snapshot {esc(x["snapshot"])}: {esc(x["claim"])}.{(" Prompted by " + esc(x["prompted_by"]) + ".") if x.get("prompted_by") else ""}</span> {badge(x["audit_status"])}{srcl(x["source_url"])}</li>' for x in negs])
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
    body = f"""<div class="pagehead"><div class="kicker">Assurance regime; jurisdiction {esc(o.get('jurisdiction',''))}</div><h1>{esc(o['name'])}</h1><p class="lead">{esc(o['ai_analogue'])}</p></div>
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
    items = "".join(f'<li><a href="../entity/{esc(LEDGER_ALIAS.get(e["id"], e["id"]))}.html">{esc(e["name"])}</a>, {esc(s["dimension"])} ({esc(s["direction"])}): {esc(s["claim"])}{("<span class=\"quote\">&ldquo;" + esc(s["quote"]) + "&rdquo;</span>") if s.get("quote") and (s.get("quote_source") in (None, sid)) else ""}</li>' for e, s in cites)
    L = C["L"]; E = L["entities"]
    lrows = [t for t in L["transfers"] if t["source_url"] == x["url"]] + [r for r in L["relationships"] if r["source_url"] == x["url"]] + [n for n in L["negatives"] if n["source_url"] == x["url"]]
    litems = "".join(f'<li><b>{esc(r["row_id"])}</b> {esc(r.get("purpose") or r.get("claim") or (r.get("role", "") + " at " + E.get(r.get("object", ""), {}).get("name", "")))} {badge(r["audit_status"])}</li>' for r in lrows)
    body = f"""<div class="pagehead"><div class="kicker">{esc(x['publisher'])}{', ' + esc(x['published']) if x.get('published') else ''}; retrieved {esc(x['retrieved'])} {tier(x)}{badge(x.get('audit_status'))}</div>
    <h1>{esc(x['title'])}</h1><p class="lead"><a href="{esc(x['url'])}" target="_blank" rel="noopener">{esc(x['url'])}</a></p><p class="lead">{esc(x.get('note',''))}</p>
    {('<p class="lead">Imported from ' + esc(x['imported_from']) + '.</p>') if x.get('imported_from') else ''}{('<p class="lead">Found via <a href="' + esc(x['discovered_via']) + '">' + esc(x['discovered_via']) + '</a>.</p>') if x.get('discovered_via') else ''}</div>
    <div class="cols"><div class="card"><h3>Signals citing this source</h3><ul>{items or '<li>none</li>'}</ul></div><div class="card"><h3>Ledger rows citing this URL</h3><ul>{litems or '<li>none</li>'}</ul></div></div>"""
    return layout(x["title"], body, 1, "sources")


# ---------------------------------------------------------------- index pages
def _ev_row(e: dict, bench: dict, dims: dict, C: dict) -> str:
    lid = LEDGER_ALIAS.get(e["id"], e["id"]); ex = C["ex"].get(lid); vals = e["values_by_policy"][DEFAULT_POLICY]; fl = e.get("floor")
    sd = {k: ("" if e["scores"][k] is None else str(e["scores"][k])) for k in ("lab", "regulator", "public", "equal")}
    cells = ["<tr>"]
    cells.append('<td><a href="../entity/' + lid + '.html">' + esc(e["name"]) + "</a><br>" +
                 '<span style="color:var(--muted);font-size:12px">' + esc(bench["types"][e["type"]]) + ", " + esc(e["hq"]) + "</span></td>")
    role = esc(ROLE_LABEL.get(e["role"], e["role"]))
    band = bandchip(e["band"]) if e.get("status", "ranked") == "ranked" else '<span class="band" style="color:var(--muted)">not ranked</span>'
    cells.append("<td>" + role + "</td><td>" + band + "</td>")
    cells.append('<td class="num evscore" data-lab="' + sd["lab"] + '" data-regulator="' + sd["regulator"] +
                 '" data-public="' + sd["public"] + '" data-equal="' + sd["equal"] + '">\u2013</td>')
    cells.append('<td class="num">' + str(e["coverage"]) + "/8</td>")
    cells.append("<td>" + ((esc(dims[fl]["label"].lower()) + " " + str(vals[fl])) if fl else "none") + "</td>")
    cells.append("<td>" + esc(e["confidence"]) + "</td>")
    cells.append('<td class="num">' + ((str(ex["confirmed_rows"]) + "/" + str(ex["inflow_rows"])) if ex else "") + "</td>")
    cells.append("<td>" + esc(", ".join(e["domains"])) + "</td></tr>")
    return "".join(cells)


EV_SCORE_SCRIPT = r"""
<script>
(function(){
  var preset = "lab";
  var labels = {lab: "Lab procurement", regulator: "Regulator or auditor", public: "Public trust", equal: "Equal weights"};
  document.querySelectorAll('#evscore-ctl [data-preset]').forEach(function(b){
    b.addEventListener('click', function(){
      preset = b.getAttribute('data-preset');
      document.querySelectorAll('#evscore-ctl [data-preset]').forEach(function(x){
        x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
      });
      document.getElementById('evscore-btn').textContent = 'Score with these weights (' + labels[preset] + ')';
    });
  });
  document.getElementById('evscore-btn').addEventListener('click', function(){
    document.querySelectorAll('.evscore').forEach(function(td){
      var v = td.getAttribute('data-' + preset);
      td.textContent = v === '' ? '–' : v;
    });
    document.querySelectorAll('th.evscore-h').forEach(function(th){
      th.textContent = 'Score (' + labels[preset] + ')';
    });
    var note = document.getElementById('evscore-note');
    if (note) note.textContent = 'Showing the weighted number under the ' + labels[preset] + ' preset. Two readers with different presets will see different numbers, and both are right; a two-point gap means nothing.';
  });
})();
</script>"""


def evaluators_index(bench: dict, C: dict) -> str:
    dims = {x["key"]: x for x in bench["dimensions"]}
    ranked = [e for e in bench["evaluators"] if e.get("status", "ranked") == "ranked"]
    watch = [e for e in bench["evaluators"] if e.get("status") == "watchlist"]
    outs = [e for e in bench["evaluators"] if e.get("status") == "out-of-scope"]
    key = lambda e: (BAND_ORDER[e["band"]], -(e["scores"]["lab"] if e["scores"]["lab"] is not None else -1), e["name"].lower())
    head = "<tr><th>Evaluator</th><th>Role</th><th>Band</th><th class=\"evscore-h\">Score</th><th>Evidenced</th><th>Floor</th><th>Confidence</th><th>Confirmed rows</th><th>Domains</th></tr>"
    body = f"""<div class="pagehead"><h1>Evaluators</h1><p class="lead">{len(ranked)} ranked organizations in three lists, scored on eight independence dimensions under the Retrieved & confirmed evidence policy (confirmed sources only). Band first: an evidenced 0 on a conflict dimension (funding, governance, personnel, role incompatibility, scope, publication) is a disqualifying floor, a 1 a conditional floor; access and methods never set a band. The band, the coverage, the weakest evidenced dimension, and the eight dimension values show by default. The weighted number is hidden until you choose a preset and press the button: two readers with different presets will see different numbers, and both are right. Open a row for the derivation, the binding signals, the ledger, and the focused graph. Independence only; not quality, coverage, or competence. A "no floor triggered" band means no disqualifying conflict is on file; it is not a pass.</p></div>
    <div class="card" id="evscore-ctl"><h3>Score with a weight preset</h3><p style="font-size:13.5px;color:var(--muted)" id="evscore-note">The number is yours, so it is hidden until you choose weights. Pick a preset, then press the button to reveal the weighted number for every row.</p>
    <div class="marks" role="group" aria-label="Weight presets" style="margin:8px 0">
      <button class="linkbtn" data-preset="lab" aria-pressed="true">Lab procurement</button>
      <button class="linkbtn" data-preset="regulator" aria-pressed="false">Regulator or auditor</button>
      <button class="linkbtn" data-preset="public" aria-pressed="false">Public trust</button>
      <button class="linkbtn" data-preset="equal" aria-pressed="false">Equal weights</button>
      <button class="cta small" id="evscore-btn" style="margin-left:8px">Score with these weights (Lab procurement)</button>
    </div></div>{EV_SCORE_SCRIPT}"""
    for g in GROUP_ORDER:
        rows = [_ev_row(e, bench, dims, C) for e in sorted((x for x in ranked if x.get("list_group") == g), key=key)]
        body += f"""<div class="pagehead" style="margin-top:20px"><h2>{esc(GROUP_LABEL[g])} <span class="gid">{len(rows)}</span></h2><p class="lead">{esc(GROUP_DESC[g])}</p></div><div class="card"><table class="tbl">{head}{''.join(rows)}</table></div>"""
    if watch:
        wrows = [_ev_row(e, bench, dims, C) for e in sorted(watch, key=key)]
        body += f"""<div class="pagehead" style="margin-top:26px"><h2>Watchlist (not ranked)</h2><p class="lead">Expected entrants scored on the same rubric but excluded from rankings and every statistic: initiatives announced with no evaluations yet. Hypothetical composites are not scored (RULES 11).</p></div>
    <div class="card"><table class="tbl">{head}{''.join(wrows)}</table></div>"""
    if outs:
        orows = [_ev_row(e, bench, dims, C) for e in sorted(outs, key=key)]
        body += f"""<div class="pagehead" style="margin-top:26px"><h2>Out of scope, retained for the record</h2><p class="lead">Organizations whose frontier work is capability benchmarking rather than safety evaluation (RULES 11, <a href="{REPO}DECISIONS.md">decision D-001</a>). Records, bounds, and derivations are unchanged; they are unranked and excluded from every statistic.</p></div>
    <div class="card"><table class="tbl">{head}{''.join(orows)}</table></div>"""
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
    body = f"""<div class="pagehead"><h1>Entities</h1><p class="lead">{len(E)} entities in the ledger: {', '.join(f'{v} {k}' for k, v in summ.items() if v)}. Distance 0 is a lab; 1 a direct tie; higher runs through principals and funders. Each page shows every row in and out and the funding graph focused on that node. People are recorded by public role only, and everyone the bench publishes a score-affecting claim about receives their card before a tag is cut (RULES 12).</p></div>
    <div class="card"><table class="tbl"><tr><th>Entity</th><th>Kind</th><th>Distance</th><th>Money in</th><th>Money out</th><th>Roles</th><th>Confirmed in</th><th>Notes</th></tr>{''.join(rows)}</table></div>"""
    return layout("Entities", body, 1, "entities")


def regimes_index(bench: dict, C: dict, timeline_rows: list) -> str:
    rows = []
    for rid, lad in C["ladder"].items():
        o = C["regs"][rid]; an = C["analog"].get(rid); p = C["paths"][rid]
        rows.append(f'<tr><td><a href="../regime/{esc(rid)}.html">{esc(o["name"])}</a></td><td>{esc(p["letters"])}</td><td class="num">{lad["reached"]}/7</td><td class="num">{lad["first"]}</td><td class="num">{f"{1 - an['distance']:.2f}" if an else "ref"}</td><td>{esc(o.get("jurisdiction", ""))}</td><td style="color:var(--muted);font-size:12.5px">{esc(o["payer"])}</td></tr>')
    table = f"""<p class="lead">Sixteen assurance regimes coded as dated milestones. The path signature is the ordered sequence of moves (V voluntary, T trigger, M mandate, S standards, O oversight, I independence, A access or publication, D delegation, P payer shift, R rollback). Similarity compares each regime's opening to frontier AI's path so far.</p>
    <div class="card"><table class="tbl"><tr><th>Regime</th><th>Path</th><th>Stages</th><th>First milestone</th><th>Similarity to AI</th><th>Jurisdiction</th><th>Who pays</th></tr>{''.join(rows)}</table></div>"""
    from .build import fill_placeholders
    frag = (SITE / "regimes.html").read_text().replace("<!--__REGIMES_TABLE__-->", table)
    return layout("Where we are", fill_placeholders(frag, bench, timeline_rows), 1, "regimes")


def ledger_index(bench: dict, C: dict) -> str:
    from .build import fill_placeholders
    frag = (SITE / "ledger.html").read_text()
    return layout("Money and ties", fill_placeholders(frag, bench, []), 1, "ledger")


def sources_index(bench: dict, C: dict) -> str:
    rows = []
    for sid, x in sorted(bench["sources"].items(), key=lambda kv: (kv[1]["publisher"].lower(), kv[1]["title"].lower())):
        n = len(C["signals_by_source"].get(sid, []))
        rows.append(f'<tr><td><a href="../source/{esc(sid)}.html">{esc(x["title"])}</a></td><td>{esc(x["publisher"])}</td><td>{esc(x.get("published", ""))}</td><td>{esc(TIER.get(x.get("source_type"), "not set"))}{(" (" + esc(x["press_kind"]) + ")") if x.get("press_kind") else ""}</td><td>{badge(x.get("audit_status"))}</td><td class="num">{n}</td></tr>')
    counts = {}
    for x in bench["sources"].values(): counts[x.get("audit_status", "unaudited")] = counts.get(x.get("audit_status", "unaudited"), 0) + 1
    body = f"""<div class="pagehead"><h1>Sources</h1><p class="lead">{len(bench['sources'])} sources cited by signals: {', '.join(f'{v} {k}' for k, v in sorted(counts.items()))}. Tier 1 is a filing or a funder's own index; tier 2 a third-party ledger; tier 3 the organization's own statement; tier 4 press, split into primary (a named editorial outlet) and aggregator (newsletters, wikis, wires, law-firm alerts). Under the Retrieved & confirmed evidence policy only confirmed sources move a value; imported and unverifiable ones stay visible as leads.</p></div>
    <div class="card"><table class="tbl"><tr><th>Source</th><th>Publisher</th><th>Published</th><th>Tier</th><th>Audit</th><th>Signals</th></tr>{''.join(rows)}</table></div>"""
    return layout("Sources", body, 1, "sources")


# ---------------------------------------------------------------- topic pages
def rubric_index(bench: dict) -> str:
    guide = json.loads((DATA / "guide.json").read_text())
    bykey = {d["key"]: d for d in bench["dimensions"]}
    def dimcard(d):
        return f'<div class="rdim"><h3>{esc(d["label"])}</h3><p>{esc(d["desc"])}</p><ul class="anchors">{"".join(f"<li><b>{i}</b><span>{esc(a)}</span></li>" for i, a in enumerate(d["anchors"]))}</ul></div>'
    struct = "".join(dimcard(bykey[k]) for k in ["F", "G", "P", "X", "S", "R"] if k in bykey)
    cond = "".join(dimcard(bykey[k]) for k in ["A", "M"] if k in bykey)
    raises = "".join(f"<li>{esc(x)}</li>" for x in guide["raises"]); lowers = "".join(f"<li>{esc(x)}</li>" for x in guide["lowers"])
    try:
        import markdown
        rules = markdown.markdown((ROOT / "RULES.md").read_text(), extensions=["tables"])
    except ImportError:
        rules = "<pre>" + esc((ROOT / "RULES.md").read_text()) + "</pre>"
    presets = "".join(f'<li><b>{esc(p["label"])}.</b> {" ".join(f"{k} {v}" for k, v in p["weights"].items())}. {esc(p.get("derivation", ""))}</li>' for p in bench["presets"].values())
    glossary = "".join(f"<li><b>{esc(t)}.</b> {esc(x)}</li>" for t, x in guide["glossary"])
    body = f"""<div class="pagehead"><h1>The rubric and the rules</h1><p class="lead">Eight dimensions, each scored 0 to 4 from public evidence, then weighted. Six score <b>structural independence</b>: funding, governance, personnel, role incompatibility, scope control, publication rights. Two record the <b>evaluation conditions</b> that make the work possible: access depth and method transparency. The conditions count in the number and never set a band — deeper access is granted by the lab being evaluated, so it is evidence about the relationship, not independence from it. The dimensions follow the AI Evaluator Forum's AEF-1 operating conditions and the financial-audit independence rules that Illinois SB 315 imports for frontier AI, with two additions the field tends to skip: who owns the evaluator, and whether it sells fixes to the companies it grades. A value is not a curator's impression: each signal names the anchor it supports and the rule below that says so, and the value is the tightest cap or, with no cap, the highest floor.</p></div>
    <h2>Structural independence</h2>
    <div class="rubric">{struct}</div>
    <h2 style="margin-top:30px">Evaluation conditions</h2>
    <p class="lead">What labs have granted and what has been published. Scored 0 to 4 like the rest, counted in the number, never a band.</p>
    <div class="rubric">{cond}</div>
    <h2 style="margin-top:30px">What raises and lowers a score</h2>
    <p class="lead">The list is deliberately concrete: each item is something you can verify from a filing, a contract term, a system card, or a published policy.</p>
    <div class="signals"><div><h3>Raises the score</h3><div class="ev for"><ul>{raises}</ul></div></div><div><h3>Lowers the score</h3><div class="ev against"><ul>{lowers}</ul></div></div></div>
    <h2 style="margin-top:30px">Weights</h2><div class="card"><ul>{presets}</ul></div>
    <h2 style="margin-top:30px">The rules</h2><div class="card rules">{rules}</div>
    <h2 style="margin-top:30px">Glossary</h2><div class="card"><ul>{glossary}</ul></div>"""
    return layout("Rubric and rules", body, 1, "rubric")


def cases_index() -> str:
    cases = json.loads((DATA / "cases.json").read_text())
    items = "".join(f'<div class="case"><div><h3>{esc(c["t"])}</h3><div class="verdict">{esc(c["v"])}</div></div><p>{esc(c["p"])}<br><span class="verdict">{esc(c["c"])}</span></p></div>' for c in cases)
    body = f"""<div class="pagehead"><h1>Cases that set the bar</h1><p class="lead">Six cases from the last two years, read for what they reveal about each dimension: five engagements and one investor overlap. Epoch AI is retained out of scope as a capability benchmark (decision D-001); its FrontierMath case stays because it set the funder-disclosure norm the safety evaluators now follow. Longer treatments and sources are in the repo under <a href="{REPO}paper/">paper/</a>.</p></div><div class="cases">{items}</div>"""
    return layout("Cases", body, 1, "cases")


def method_index(bench: dict) -> str:
    body = f"""<div class="pagehead"><h1>How the scores are made</h1></div>
    <div class="card"><h3>Values</h3><p style="font-size:14.5px;max-width:74ch">Each evaluator gets a 0 to 4 on eight dimensions using only public evidence: filings, funding announcements, system cards, published policies, contracts described in reports, and press. Every signal names the anchor it supports and the rule in <a href="../rubric/index.html">RULES.md</a> that says so. The value on a dimension is the tightest admissible cap or, with no cap, the highest admissible floor. Where a floor and a cap disagree, the assessment carries a written resolution naming the rule, and the card shows the conflict. A 0 needs a quoted span; a 4 needs a span and a tier-1 or tier-2 source or two independent sources with one not self-published; a bound from sources that were not all confirmed cannot set an extreme. Bounds that fail these tests are held at the nearest supportable anchor and the card says which rule held them.</p></div>
    <div class="card"><h3>Evidence policies</h3><p style="font-size:14.5px;max-width:74ch">The reader chooses what counts. The default, Retrieved & confirmed, admits a signal only if at least one cited source was re-fetched and confirmed, so no number moves on a source you cannot open and check. Imported and unverifiable leads stay visible and count for nothing. A dimension with no admissible signal renders as a dash and is excluded from the score; the coverage count sits beside every score.</p>{policy_table(bench, "../")}</div>
    <div class="card"><h3>Bands and scores</h3><p style="font-size:14.5px;max-width:74ch">The weighted total over the evidenced dimensions is scaled to 100 under four weight presets, each with a written derivation. Independence has floors, so the band comes first: an evidenced 0 on a conflict dimension (funding, governance, personnel, role incompatibility, scope, publication) is a disqualifying floor, a 1 on one of those a conditional floor, otherwise no floor is triggered — no disqualifying conflict is on file, not a pass. Access and methods count in the number and never set a band, because a 0 there means the labs have not let the organization in or it has not published its methods, not that it is compromised. The number ranks within a band, and on the directory it is hidden until the reader chooses weights, so two readers with different priorities see different numbers and neither is the site's. The lab-procurement preset is the confirmatory view; it was fixed in the seed script before the population pass but not registered outside this repository. The other presets are sensitivity checks, not alternative truths. The preset weightings lean on the AI Evaluator Forum's AEF-1 operating conditions and the financial-audit independence rules that Illinois SB 315 imports for frontier AI: funding and publication rights carry the most weight where a reader of the report would first test it. Scores are ordinal projections over anchored rubrics: a ten-point gap is not twice the independence, and a two-point gap is nothing.</p></div>
    <div class="card"><h3>Independence is one axis</h3><p style="font-size:14.5px;max-width:74ch">Competence, domain coverage, staffing, and turnaround are others, and a highly independent evaluator with no cyber team is the wrong pick for a cyber evaluation. Use the domain filters alongside the score. Government bodies are scored on what reaches the public and what access they hold, with the mechanism tagged statutory where the constraint is the law rather than a lab. An entry is not an endorsement, and a low score is not an accusation; it means the public record does not yet show the safeguards that would earn a higher one.</p></div>
    <div class="card"><h3>How good is the evidence</h3><p style="font-size:14.5px;max-width:74ch">{evidence_summary(bench)}</p></div>
    <div class="card"><h3>Who made this, and what they hold</h3><p style="font-size:14.5px;max-width:74ch">Curated by Yohei Nakajima: managing partner at Untapped Capital, a pre-seed and seed venture fund; operator of Epistemedia, the claim-adjudication layer this repository drafts dockets into; author of ActiveGraph, the runtime the build runs on. The site is a collaboration between the curator and models from several developers: the first draft of the curation and the rules pass were written by Claude (Anthropic); Codex (OpenAI) and Grok (xAI) ran independent verification passes recorded in <a href="{REPO}paper/audits/">paper/audits/</a>; Gemini (Google) and Muse reviewed and criticized the site and the paper. Their review is recorded in paper/audits/ as part of the independence record, not as assurance of correctness. Anthropic, OpenAI, xAI, and Google are labs in this ledger, evaluated by organizations scored here. On the concern that Anthropic's model produced a ranking with METR, the evaluator Anthropic named in its September 2026 commitment, at the top: every value is derived from public bounds under rules applied to every organization the same way, the ranking is re-derivable by anyone with any tool or none, and the against-interest and primary-only views are one click away; if a model's involvement had tilted a value, it would show as a bound or a rule, both open to correction. Holdings: small publicly disclosed shareholdings in Google, Meta, and SpaceX, which owns xAI; assessments of evaluators with confirmed ledger ties to those labs say so in their rationale. Untapped Capital's funders include holders of shares in private AI labs; the limited-partner roster is private, so no further detail is disclosed. The curator has personal relationships with people at some of the labs in this ledger; no relationship is a source for any row — every claim rests on a public, cited source. One coder; a second coder on every extreme is a gate for a citable tag. The full statement is in <a href="{REPO}DISCLOSURE.md">DISCLOSURE.md</a>.</p></div>
    <div class="card"><h3>What we already know is weak</h3><p style="font-size:14.5px;max-width:74ch">The first full build had nine known problems, from a ladder that implies a sequence regimes do not follow to triggers selected with hindsight. They are written up in <a href="{REPO}paper/CRITIQUE.md">the critique</a>, kept so reviewers can see what the authors already know is weak and what the current version does about each one.</p></div>
    <div class="card"><h3>Scores move when evidence moves</h3><p style="font-size:14.5px;max-width:74ch">Send a contract term, a policy, or a correction and the entry updates with the source attached. Every ranked organization and every person the bench publishes a score-affecting claim about receives their card and a fourteen-day reply window before a tag is cut; the <a href="../status/index.html">status page</a> tracks who has been contacted. After first publication, a score that moves by more than one anchor triggers a fresh record packet before the next tag.</p><a class="cta" href="../contribute/index.html">How to submit evidence</a></div>
    <div class="card"><h3>Agents</h3><p style="font-size:13.5px;max-width:74ch">Machine-readable: <a href="../llms.txt">llms.txt</a>, <a href="../bench.json">bench.json</a>, and per-evaluator JSON under <a href="../evaluators/index.json">evaluators/</a> (slugs match the entity pages).</p></div>"""
    return layout("Method", body, 1, "method")


def exclusions_index(bench: dict) -> str:
    p = DATA / "exclusions.json"
    entries = json.loads(p.read_text()) if p.exists() else []
    rows = "".join(f'<tr><td>{esc(e.get("name"))}</td><td>{esc(e.get("type_guess", ""))}</td><td>{esc(e.get("result", ""))}</td><td>{esc(", ".join(e.get("criteria_met", [])) or "none")}</td><td>{esc(e.get("reason", ""))}{(" <a href=\"" + esc(e["evidence_url"]) + "\" target=\"_blank\" rel=\"noopener\">source</a>") if e.get("evidence_url") else ""}</td><td>{esc(e.get("checked_on", ""))}</td></tr>' for e in entries)
    counts = {}
    for e in entries: counts[e.get("result", "unclear")] = counts.get(e.get("result", "unclear"), 0) + 1
    body = f"""<div class="pagehead"><h1>Population: who is in, who is out</h1><p class="lead">An organization is in scope if, within the 24 months to the evidence clock, it was cited as an external evaluator or red team in a frontier system card or a government evaluation report; or it is named in a statute, code, or standard as an evaluator; or it operates a leaderboard a frontier developer cites for a frontier model (RULES 11). Candidates that met a criterion but are not yet scored are listed as in-scope candidates for the next batch. Nothing here is a judgment about quality. The directory approximates the organizations demonstrably participating in the institutional frontier-AI evaluation ecosystem — not all credible frontier-AI evaluators. The excluded and unclear lists are part of the finding, not housekeeping. A hypothetical composite is never scored.</p></div>
    <div class="card"><p style="font-size:13.5px;color:var(--muted)">{len(entries)} candidates checked{(": " + ", ".join(f"{v} {k}" for k, v in sorted(counts.items()))) if entries else ". The candidate list is being checked; results land here as they are verified"}. Every entry names the URL that decided it.</p>
    <table class="tbl"><tr><th>Candidate</th><th>Type</th><th>Result</th><th>Criteria met</th><th>Reason</th><th>Checked</th></tr>{rows or '<tr><td colspan="6">No candidates recorded yet.</td></tr>'}</table></div>"""
    return layout("Population", body, 1, "exclusions")


# ---------------------------------------------------------------- dockets, status, contribute
AGENT_PROMPT = "Open https://github.com/yoheinakajima/evaluator-bench and read AGENTS.md and RULES.md. Choose one recipe (add evidence about an evaluator, confirm an imported ledger row, or draft a docket). Fetch every source yourself in this run, copy quoted spans exactly, give every new signal a bound and the RULES.md rule code behind it, run python -m bench verify && python -m bench build && pytest -q, commit the regenerated graph/ and dist/, and open a pull request using the template. Do not change values, anchors, rules, or the verifier. If you cannot complete a recipe without guessing, stop and report what is missing."


def dockets_index(C: dict) -> str:
    rows = []
    for d in sorted((ROOT / "dockets").iterdir()):
        if not d.is_dir() or not (d / "proposal.json").exists(): continue
        p = json.loads((d / "proposal.json").read_text())
        from .docket import recorded_status
        status = recorded_status(d.name)
        rows.append(f'<tr><td><a href="{REPO}dockets/{esc(d.name)}/proposal.json">{esc(p["question"])}</a></td><td class="num">{len(p["sources"])}</td><td class="num">{sum(len(s["exact_spans"]) for s in p["sources"])}</td><td class="num">{len(p["results"])}</td><td>{esc(status)}</td><td>not submitted</td></tr>')
    body = f"""<div class="pagehead"><h1>Dockets</h1><p class="lead">Contestable claims that Bench evidence bears on, drafted in Epistemedia's research-proposal format (v0.2) and passed through Epistemedia's own validator. A docket is a <b>draft</b>: not a finding, not evidence, not citable by any signal. It becomes usable evidence only after submission to <a href="https://epistemedia.org/agents/submit/">epistemedia.org</a> and independent review there by someone other than the drafter. No docket here has been submitted.</p></div>
    <div class="card"><table class="tbl"><tr><th>Question</th><th>Sources</th><th>Spans</th><th>Results</th><th>Validation</th><th>Epistemedia</th></tr>{''.join(rows)}</table>
    <p style="font-size:13px;color:var(--muted);margin-top:8px">Build and validate: <code>python -m bench docket build &lt;slug&gt; &amp;&amp; python -m bench docket validate &lt;slug&gt;</code>. Certificate format and the path to signed machine verification: <a href="{REPO}paper/CERTIFICATION.md">paper/CERTIFICATION.md</a>.</p></div>"""
    return layout("Dockets", body, 1, "dockets")


def _csv(p: pathlib.Path) -> list[dict]:
    if not p.exists(): return []
    with open(p, newline="") as f: return [dict(r) for r in csv.DictReader(f)]


def _status_counts(rows) -> dict:
    counts = {}
    for r in rows:
        st = r.get("audit_status") or "unknown"
        counts[st] = counts.get(st, 0) + 1
    return counts


def _status_breakdown(counts: dict, total: int) -> str:
    order = ["confirmed", "unaudited", "imported", "differs", "unverifiable", "superseded", "quarantined", "unknown"]
    parts = [f"{counts[s]} {s}" for s in order if counts.get(s)]
    assert sum(counts.values()) == total, f"status buckets do not close: {counts} vs {total}"
    return f"{total} (" + ", ".join(parts) + ")"


def _population_summary() -> str:
    """One-line summary of the population candidates checked (data/exclusions.json)."""
    ex = json.loads((DATA / "exclusions.json").read_text())
    n_out = sum(1 for x in ex if x.get("result") == "out")
    n_cand = sum(1 for x in ex if x.get("result") == "in-scope-candidate")
    n_unclear = sum(1 for x in ex if x.get("result") == "unclear")
    return (f"{len(ex)} organizations have been checked against the population criteria "
            f"(RULES.md section 11): {n_out} out of scope, {n_cand} in-scope candidates, "
            f"{n_unclear} unclear.")


def status_index(bench: dict, C: dict) -> str:
    from .gates import gates
    L = C["L"]
    ev = ROOT / "graph" / "events.jsonl"; commit = event_digest()
    tr = L["transfers"]
    tstat = _status_counts(tr)
    srcs = bench["sources"].values()
    sstat = _status_counts(srcs)
    ranked = [e for e in bench["evaluators"] if e.get("status", "ranked") == "ranked"]; watch = [e for e in bench["evaluators"] if e.get("status") == "watchlist"]
    rsig = _ranked_signals(bench); quotes = sum(1 for s in rsig if s.get("quote"))
    ev_by_ledger = {LEDGER_ALIAS.get(e["id"], e["id"]): e for e in bench["evaluators"]}
    ex = [x for x in C["ex"].values() if ev_by_ledger.get(x["id"], {}).get("status", "ranked") == "ranked" and x["id"] in ev_by_ledger]
    from .ledger import hop0_split
    split = hop0_split(list(ex))
    near = sum(1 for x in ex if any(k in ("hop0", "hop1") for k in x["buckets"])); direct = sum(1 for x in ex if "hop0" in x["buckets"]); traced = sum(x["second_hop"]["traced"] for x in ex); srcn = sum(x["second_hop"]["sources"] for x in ex)
    gs = gates()
    grows = "".join(f'<tr><td>{esc(g["gate"])}</td><td class="{"gate-ok" if g["ok"] else "gate-fail"}">{"PASS" if g["ok"] else "FAIL"}</td><td style="color:var(--muted)">{esc(g["detail"])}</td></tr>' for g in gs)
    log = _csv(DATA / "outreach-log.csv")
    sent = sum(1 for r in log if r.get("contacted")); replied = sum(1 for r in log if r.get("replied"))
    lrows = "".join(f'<tr><td>{esc(r["name"])}</td><td>{esc(r["kind"])}</td><td>{esc(r.get("contacted") or "")}</td><td>{esc(r.get("replied") or "")}</td><td style="color:var(--muted)">{esc(r.get("status") or "")}</td></tr>' for r in log)
    sc = _csv(DATA / "coding" / "second-coder.csv"); coded = [r for r in sc if r.get("coder")]
    agree = sum(1 for r in coded if (r.get("agrees_with_stored") or "").lower() in ("yes", "true", "1"))
    body = f"""<div class="pagehead"><h1>Status</h1><p class="lead">What the record holds, how much of it has been re-derived, what counts under each evidence policy, who has been contacted, and what stands between this preview and a citable tag. Built {esc(bench['built_at'][:10])}; event-log digest {esc(commit)}; {esc(bench.get('rules', ''))}. Every statistic on this page covers the {len(ranked)} ranked organizations; the {len(watch)} watchlist entr{"y" if len(watch) == 1 else "ies"} and the {sum(1 for e in bench["evaluators"] if e.get("status") == "out-of-scope")} retained out-of-scope entries contribute to none.</p></div>
    <div class="card"><h3>Gates for a citable tag</h3><table class="tbl"><tr><th>Gate</th><th></th><th>Where it stands</th></tr>{grows}</table><p style="font-size:13px;color:var(--muted);margin-top:8px">Recomputed at every build by <code>python -m bench gates</code>. <code>bench release --stage published</code> refuses while any gate fails.</p></div>
    <div class="cols">
    <div class="card"><h3>Coverage</h3><table class="tbl">
      <tr><td>Ranked organizations</td><td class="num">{len(ranked)}</td></tr><tr><td>Watchlist (not ranked)</td><td class="num">{len(watch)}</td></tr><tr><td>Out of scope, retained</td><td class="num">{sum(1 for e in bench["evaluators"] if e.get("status") == "out-of-scope")}</td></tr><tr><td>Signals (ranked)</td><td class="num">{len(rsig)}</td></tr><tr><td>Signals with an exact quote (ranked)</td><td class="num">{quotes}</td></tr>
      <tr><td>Sources</td><td class="num">{_status_breakdown(sstat, len(bench['sources']))}</td></tr>
      <tr><td>Ledger transfers</td><td class="num">{_status_breakdown(tstat, len(tr))}</td></tr><tr><td>Ledger roles</td><td class="num">{len(L['relationships'])}</td></tr><tr><td>Checked and not found (bounded negatives)</td><td class="num">{len(L['negatives'])}</td></tr>
      <tr><td>Entities</td><td class="num">{len(L['entities'])}</td></tr><tr><td>Regimes</td><td class="num">{len(C['regs'])}</td></tr></table></div>
    <div class="card"><h3>Exposure (ranked only)</h3><table class="tbl">
      <tr><td>Ranked evaluators with a direct lab tie (hop 0), any kind</td><td class="num">{direct} of {len(ex)}</td></tr>
      <tr><td>of which: lab cash for evaluation work (evaluation credits are recorded, never counted)</td><td class="num">{split['funding']}</td></tr>
      <tr><td>of which: a lab owns a stake or is acquiring the evaluator</td><td class="num">{split['ownership']}</td></tr>
      <tr><td>of which: no-fee partnership or membership only</td><td class="num">{split['partnership']}</td></tr>
      <tr><td>Ranked evaluators with an inflow from a lab or a lab-tied party (hop 0 or 1)</td><td class="num">{near} of {len(ex)}</td></tr>
      <tr><td>Funding sources with a second hop traced</td><td class="num">{traced} of {srcn}</td></tr></table>
      <h3 style="margin-top:14px">Evidence standard</h3><p style="font-size:13.5px">Imported rows are leads copied from another project's ledger and satisfy no gate. A 4 on funding requires a confirmed bounded negative in a filing or index. A 0 needs a quoted span; a 4 needs a span and a second source. Scores are readings of the public record at the build date, not endorsements.</p></div></div>
    <div class="card"><h3>What counts under each evidence policy</h3>{policy_table(bench, "../")}</div>
    <div class="card"><h3>Population</h3><p style="font-size:13.5px">{_population_summary()} The full table is on the <a href="../exclusions/">exclusions page</a>.</p></div>
    <div class="card"><h3>Right of reply</h3><p style="font-size:13.5px">{len(log)} recipients ({sum(1 for r in log if r["kind"] == "organization")} organizations, {sum(1 for r in log if r["kind"] == "person")} people); {sent} contacted, {replied} replied. The citable-tag gate tracks the ranked organizations and the materially-named people (the bench's claim text names them in a score-binding signal — RULES 12); any remaining rows are outside the gate. Packets are generated by <code>bench outreach --all</code>; sending is a human action, logged here with the date.</p><table class="tbl"><tr><th>Recipient</th><th>Kind</th><th>Contacted</th><th>Replied</th><th>Status</th></tr>{lrows or '<tr><td colspan="5">No packets generated yet.</td></tr>'}</table></div>
    <div class="card"><h3>Second coder</h3><p style="font-size:13.5px">{len(coded)} assessment(s) second-coded{(f"; {agree} agree with the stored value") if coded else ""}. A human second coder on every extreme (every stored 0 or 4) is a gate for a citable tag; the full population follows by v0.2. Disagreements are logged in <code>data/coding/second-coder.csv</code> and in the assessment's resolution.</p></div>
    <div class="card"><h3>Open questions</h3><p style="font-size:13.5px">Kept in <a href="{REPO}paper/OPEN-QUESTIONS.md">paper/OPEN-QUESTIONS.md</a> with status, routes tried, and the document that would close each. Audits in <a href="{REPO}paper/audits/">paper/audits/</a>. Replies from named organizations and people are filed as signals; after first publication, a score that moves by more than one anchor triggers a record packet (<code>bench outreach</code>).</p>
    <h3 style="margin-top:14px">Data</h3><p style="font-size:13.5px"><a href="../bench.json">bench.json</a> (evaluators, assessments with per-policy derivations, signals, sources), <a href="../exposure.json">exposure.json</a>, <a href="../timeline.json">timeline.json</a>, <a href="{REPO}data/ledger/">ledger CSVs</a>, <a href="{REPO}graph/events.jsonl">event log</a>, <a href="{REPO}RULES.md">RULES.md</a>. Code Apache-2.0; data CC BY 4.0. Disclosure: <a href="{REPO}DISCLOSURE.md">DISCLOSURE.md</a>.</p></div>"""
    return layout("Status", body, 1, "status")


def contribute_index() -> str:
    body = f"""<div class="pagehead"><h1>Contribute</h1><p class="lead">Scores here move only when evidence moves. A contribution is a source, a signal with an exact quote and a bound, a ledger row, a confirmed re-derivation, or a docket. Nobody edits a value directly, including the maintainers: values are derived from the signals under <a href="{REPO}RULES.md">RULES.md</a>.</p></div>
    <div class="cols"><div>
    <div class="card"><h3>If you are a person</h3><ul>
      <li><b>Ten minutes.</b> Open any evaluator page, follow a source link, and check that the quoted span is there. If it is not, open an issue with the signal id.</li>
      <li><b>An hour.</b> Confirm an imported ledger row: open its source, compare the figure, set <code>audit_status</code> to confirmed or differs, add a line to the audit file, open a pull request.</li>
      <li><b>An afternoon.</b> Add evidence: a source you fetched yourself, a signal with a quote under 120 characters copied exactly, the anchor it supports as a bound, and the rule code that says so.</li>
      <li><b>If you work at an evaluator or a lab.</b> You are welcome to contribute; say so in the pull request. Evaluators can publish their contract terms and the relevant dimensions move on their own. To file a formal response, use the <a href="https://github.com/yoheinakajima/evaluator-bench/issues/new?template=right-of-reply.md">right-of-reply issue template</a>; it is filed as a signal with the date received.</li>
      <li><b>If you are named as a person.</b> The same reply channel is yours. Bench records public roles only and asserts no motive; an open question about a role or a gift is a request for a document. People about whom the bench publishes a score-affecting claim are contacted about their card as the release goes public (RULES 12); everyone else named is covered by this reply channel. Until the outreach log shows a contact date, treat the card as provisional.</li></ul>
      <p style="font-size:13.5px;margin-top:10px">Full recipes and rules of evidence: <a href="{REPO}AGENTS.md">AGENTS.md</a>, <a href="{REPO}CONTRIBUTING.md">CONTRIBUTING.md</a>, <a href="{REPO}CONTRACT.md">CONTRACT.md</a>, <a href="{REPO}RULES.md">RULES.md</a>.</p></div>
    <div class="card"><h3>What happens to a pull request</h3><ul>
      <li>CI runs the verifier (the CONTRACT), rebuilds the graph and site, checks the committed event log matches a clean build, and runs the tests. The verifier rejects a stored value that disagrees with its derivation, a signal without a bound, and a role that disagrees with the rule.</li>
      <li>A machine review re-fetches every source the PR cites, checks that each quoted span appears verbatim, asks a model whether each claim is supported, qualified, or unsupported, and flags any assessment change with no new signal on that dimension. The report is posted on the PR.</li>
      <li>A maintainer reads the report and merges or asks for changes. Merged evidence appears on the site at the next build and in the next annual update paper.</li></ul></div></div>
    <div>
    <div class="card"><h3>If you are pointing an agent here</h3><p style="font-size:13.5px">Copy this instruction to a coding agent with repository access:</p>
      <blockquote style="border-left:3px solid var(--teal);margin:8px 0;padding:8px 12px;font-size:13.5px;background:var(--paper)">{esc(AGENT_PROMPT)}</blockquote>
      <p style="font-size:13.5px">The agent must fetch sources itself, never sum across money measures, never turn a bounded absence into zero, name public roles only, and assert no motive. Its pull request is a queue item, not accepted evidence, until the checks and a maintainer pass it.</p></div>
    <div class="card"><h3>Contested claims</h3><p style="font-size:13.5px">Some claims here will be contested. We draft the contestable ones as proposals for independent review by a third party, Epistemedia, where a reviewer other than the drafter checks each quoted span; a draft is not evidence and none has been reviewed yet. <a href="../dockets/index.html">The drafts</a> and <a href="{REPO}paper/CERTIFICATION.md">how review would work</a>.</p></div>
    <div class="card"><h3>What we will not accept</h3><p style="font-size:13.5px">Private communications, screenshots of paywalled pages, claims about a person's intent, non-public individuals, value edits without a signal, hypothetical organizations, and deletions of rows (supersede them instead).</p></div></div></div>"""
    return layout("Contribute", body, 1, "contribute")


def paper_index() -> str:
    try:
        import markdown
        body_md = (ROOT / "paper" / "draft.md").read_text()
        html = markdown.markdown(body_md, extensions=["tables"])
    except ImportError:
        html = "<pre>" + esc((ROOT / "paper" / "draft.md").read_text()) + "</pre>"
    rp = ROOT / "data" / "release.json"; rel = json.loads(rp.read_text()) if rp.exists() else {}
    note = f'<div class="card"><h3>Draft, accepting submissions</h3><p style="font-size:13.5px">This is the working draft. Submissions merged before {esc(rel.get("window_until") or "the window closes")} form the launch-round section; the paper is then pinned to a tag once the <a href="../status/index.html">gates</a> pass. Every number regenerates from the repository at that tag. Comment by opening an issue; correct by opening a pull request with evidence (<a href="../contribute/index.html">how</a>).</p></div>' if rel.get("stage") == "preview" else ""
    cite = """<div class="card"><h3>Cite this</h3><pre id="citblock" style="white-space:pre-wrap;font-size:13px">Nakajima, Y. (2026). Who Pays the Referee? Measuring Third-Party Evaluator Independence in Frontier AI Against the History of Assurance Regimes (v0.1 draft). https://github.com/yoheinakajima/evaluator-bench</pre><p style="font-size:13px;color:var(--muted)">Machine-readable citation: <a href="https://github.com/yoheinakajima/evaluator-bench/blob/main/CITATION.cff">CITATION.cff</a></p><button class="cta small" id="citbtn">Copy citation</button><script>(function(){document.getElementById('citbtn').addEventListener('click',function(){var t=document.getElementById('citblock').textContent;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){document.getElementById('citbtn').textContent='Copied';},function(){document.getElementById('citbtn').textContent='Select the text above';});});})();</script></div>"""
    return layout("Paper", f'<div class="pagehead"><div class="kicker">Working draft, regenerated from the repository</div></div>{note}{cite}<div class="card paper">{html}</div>', 1, "paper")


# ---------------------------------------------------------------- agent access

SITE_BASE = "https://yoheinakajima.github.io/evaluator-bench"


def llms_txt(bench: dict) -> str:
    """Compact orientation file for AI agents fetching this site."""
    evs = bench["evaluators"]
    ranked = [e for e in evs if e.get("status", "ranked") == "ranked"]
    return "\n".join([
        "# Evaluator Bench",
        "A curator's ledger of third-party AI-evaluator independence: six structural-independence",
        "dimensions (funding, governance, personnel, role incompatibility, scope, publication) plus two",
        "evaluation-condition dimensions (access depth, method transparency). Each evaluator gets 0-4",
        "per dimension, derived as the tightest admissible cap (or highest admissible floor) from",
        "bounded public signals under written rules — re-derivable by anyone from the quoted spans.",
        "An entry is not an endorsement; a low score is not an accusation; a 'no floor triggered' band",
        "means no disqualifying conflict is on file, not a pass. Curator: Yohei Nakajima (Untapped Capital).",
        "",
        "## Machine data",
        f"- bench.json — everything: {len(evs)} evaluators, {sum(len(e.get('signals', [])) for e in evs)} signals,",
        f"  {len(bench['sources'])} sources, rules, evidence policies, weight presets (0-4 ordinal, not ratios).",
        "- evaluators/index.json — slug, name, type, status, band, and JSON URL for every evaluator.",
        "- evaluators/<slug>.json — one evaluator's full record: assessments with per-policy derivations,",
        "  binding signals with verbatim quoted spans (<120 chars), and the sources those signals cite.",
        "- exposure.json, timeline.json — ledger exposure and the regime timeline.",
        f"Slugs match the entity pages: evaluators/<slug>.json <-> entity/<slug>.html.",
        "",
        "## How to read it",
        "Method: /method/. A 0 on a conflict dimension needs a quoted span; an extreme (0 or 4) is",
        "second-coded. Values are derived, never typed; the verifier rejects stored values that",
        "disagree with their derivation. Scores move when evidence moves: open a PR with a source.",
        "",
        "## Disclosure",
        "Holdings: publicly disclosed shares in Google, Meta, and SpaceX (owner of xAI).",
        "Untapped Capital's funders include holders of shares in private AI labs; the LP roster is",
        "private, so no further detail is disclosed. The curator knows people at some of the labs in",
        "this ledger; no relationship is a source for any row. Full: DISCLOSURE.md.",
        "",
        f"Built {bench['built_at']} ({bench['rules']}); {len(ranked)} of {len(evs)} evaluators ranked.",
        "",
    ])


def write_agent_access(bench: dict) -> int:
    """Emit llms.txt, per-evaluator JSON records, and evaluators/index.json."""
    slugs = {}
    evdir = DIST / "evaluators"
    evdir.mkdir(exist_ok=True)
    index = []
    for e in bench["evaluators"]:
        slug = LEDGER_ALIAS.get(e["id"], e["id"])
        sids = set()
        for s in e.get("signals", []):
            sids.update(s.get("sources", []) or [])
            if s.get("quote_source"):
                sids.add(s["quote_source"])
        doc = {
            "meta": {
                "version": bench["version"], "rules": bench["rules"],
                "default_policy": bench["default_policy"], "built_at": bench["built_at"],
                "page_url": f"{SITE_BASE}/entity/{slug}.html",
            },
            "evaluator": e,
            "sources": {sid: bench["sources"][sid] for sid in sorted(sids) if sid in bench["sources"]},
        }
        (evdir / f"{slug}.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
        slugs[slug] = e["id"]
        index.append({
            "slug": slug, "name": e["name"], "type": e["type"],
            "status": e.get("status", "ranked"), "band": e.get("band"),
            "json_url": f"evaluators/{slug}.json", "page_url": f"entity/{slug}.html",
        })
    (evdir / "index.json").write_text(json.dumps({
        "built_at": bench["built_at"], "count": len(index), "evaluators": index,
    }, indent=1, ensure_ascii=False) + "\n")
    (DIST / "llms.txt").write_text(llms_txt(bench))
    # Sweep stale per-evaluator JSONs so a removed evaluator leaves no orphan.
    for p in evdir.glob("*.json"):
        if p.name != "index.json" and p.stem not in slugs:
            p.unlink()
    return len(slugs)


# ---------------------------------------------------------------- driver
def render_all(bench: dict, timeline_rows: list | None = None) -> dict:
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
    write(DIST / "regimes" / "index.html", regimes_index(bench, C, timeline_rows or []))
    write(DIST / "ledger" / "index.html", ledger_index(bench, C))
    write(DIST / "sources" / "index.html", sources_index(bench, C))
    write(DIST / "rubric" / "index.html", rubric_index(bench))
    write(DIST / "cases" / "index.html", cases_index())
    write(DIST / "method" / "index.html", method_index(bench))
    write(DIST / "exclusions" / "index.html", exclusions_index(bench))
    write(DIST / "dockets" / "index.html", dockets_index(C))
    write(DIST / "status" / "index.html", status_index(bench, C))
    write(DIST / "contribute" / "index.html", contribute_index())
    write(DIST / "paper" / "index.html", paper_index())
    agent_n = write_agent_access(bench)
    # Sweep stale pages: an entity or source removed from data/ must not linger
    # in dist/ as a reachable-but-orphaned page.
    expected = {"index.html"}
    for name in ("evaluators", "entities", "regimes", "ledger", "sources", "rubric", "cases",
                 "method", "exclusions", "dockets", "status", "contribute", "paper"):
        expected.add(f"{name}/index.html")
    expected |= {f"entity/{eid}.html" for eid in C["L"]["entities"]}
    expected |= {f"regime/{rid}.html" for rid in C["regs"]}
    expected |= {f"source/{sid}.html" for sid in bench["sources"]}
    stale = [p for p in DIST.rglob("*.html") if p.relative_to(DIST).as_posix() not in expected]
    for p in stale:
        p.unlink()
    return {"pages": n + 12, "stale_removed": len(stale)}
