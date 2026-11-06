// Load cost on a throttled CPU. Times each load phase by wrapping the browser calls the glue uses, without changing the page.
// usage: node test/rv_a8_load.js [index.html] [runs]
const {chromium}=require('playwright');const path=require('path');
const file=path.resolve(process.argv[2]||path.join(__dirname,'../build/index.html'));const runs=+(process.argv[3]||3);
const wrap=()=>{const T=window.__T={};const now=()=>performance.now();
 const A=window.atob;let nA=0;window.atob=s=>{const t=now();const r=A(s);(T.atob=T.atob||[]).push([s.length,now()-t]);return r;};
 const W=WebAssembly.instantiate;WebAssembly.instantiate=async(...a)=>{const t=now();const r=await W.apply(WebAssembly,a);T.wasm=now()-t;T.wasmAt=now();return r;};
 const J=JSON.parse;JSON.parse=s=>{const t=now();const r=J(s);T.json=(T.json||0)+now()-t;return r;};
 const R=Response.prototype.arrayBuffer;Response.prototype.arrayBuffer=async function(){const t=now();const r=await R.call(this);T.gunzip=now()-t;return r;};
 T.start=now();};
(async()=>{const b=await chromium.launch();for(const rate of [1,4,6]){const res=[];
 for(let i=0;i<runs;i++){const ctx=await b.newContext({viewport:{width:1280,height:800}});const p=await ctx.newPage();const c=await ctx.newCDPSession(p);await c.send('Emulation.setCPUThrottlingRate',{rate});
  await p.addInitScript(wrap);const t=Date.now();await p.goto('file://'+file,{waitUntil:'commit'});await p.waitForFunction('window.annReady',{timeout:300000,polling:50});
  await p.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
  const R=await p.evaluate(()=>{const T=window.__T,s=window.annStats;const nav=performance.getEntriesByType('navigation')[0];const paint=performance.getEntriesByName('first-contentful-paint')[0];
   return {ready:window.annReadyAt||0,nav:nav&&nav.domInteractive,fcp:paint&&paint.startTime,atob:(T.atob||[]).reduce((a,x)=>a+x[1],0),gunzip:T.gunzip,json:T.json,wasm:T.wasm,first:s.ms,ticks:s.ticks,edges:s.edges,now:performance.now(),hmem:performance.memory&&performance.memory.usedJSHeapSize};});
  R.wall=Date.now()-t;res.push(R);await ctx.close();}
 res.sort((a,x)=>a.wall-x.wall);const m=res[0];console.log(`x${rate} wall ${m.wall} fcp ${m.fcp&&m.fcp.toFixed(0)} domint ${m.nav&&m.nav.toFixed(0)} atob ${m.atob.toFixed(0)} gunzip ${m.gunzip&&m.gunzip.toFixed(0)} json ${m.json&&m.json.toFixed(1)} wasm ${m.wasm&&m.wasm.toFixed(1)} first-dispatch ${m.first.toFixed(0)} ticks ${m.ticks} edges ${m.edges} all ${res.map(x=>x.wall)}`);}
 await b.close();})();
