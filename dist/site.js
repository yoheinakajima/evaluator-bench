
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
    var adj={},kind={};
    nodes.forEach(function(n){var id=n.dataset.node;kind[id]=n.dataset.kind||'';adj[id]=[];});
    edges.forEach(function(e){var a=e.dataset.from,b=e.dataset.to;if(adj[a]&&adj[b]){adj[a].push(b);adj[b].push(a);}});
    function bfs(sources){var d={},q=[];sources.forEach(function(s){if(!(s in d)){d[s]=0;q.push(s);}});while(q.length){var u=q.shift();(adj[u]||[]).forEach(function(w){if(!(w in d)){d[w]=d[u]+1;q.push(w);}});}return d;}
    function trace(id){var d1=bfs([id]),keepN={},keepE={};keepN[id]=1;
      ['lab','evaluator'].forEach(function(want){var d2=bfs(Object.keys(adj).filter(function(n){return kind[n]===want;})),D=d2[id];
        if(D===undefined)return;
        Object.keys(adj).forEach(function(v){if(d1[v]!==undefined&&d2[v]!==undefined&&d1[v]+d2[v]===D)keepN[v]=1;});
        edges.forEach(function(e){var a=e.dataset.from,b=e.dataset.to;
          if((d1[a]!==undefined&&d2[b]!==undefined&&d1[a]+1+d2[b]===D)||(d1[b]!==undefined&&d2[a]!==undefined&&d1[b]+1+d2[a]===D))keepE[a+'|'+b]=1;});});
      return {n:keepN,e:keepE};}
    function focus(id){var t=trace(id);
      edges.forEach(function(e){if(t.e[e.dataset.from+'|'+e.dataset.to])e.classList.remove('dim');else e.classList.add('dim');});
      nodes.forEach(function(n){if(t.n[n.dataset.node])n.classList.remove('dim');else n.classList.add('dim');});}
    function clear(){nodes.forEach(function(n){n.classList.remove('dim');});edges.forEach(function(e){e.classList.remove('dim');});}
    nodes.forEach(function(n){n.addEventListener('mouseenter',function(){focus(n.dataset.node);});n.addEventListener('mouseleave',clear);
      n.addEventListener('click',function(ev){if(ev.target.closest('a'))return;focus(n.dataset.node);});});
  });
})();
