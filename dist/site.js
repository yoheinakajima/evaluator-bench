
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
