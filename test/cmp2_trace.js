// Per tick trace of the repeat key (type at end, again) after the flops.js prelude: active FSM states and work per tick.
// Usage: ENGINE=build/engine_count.wasm node test/cmp2_trace.js [which]   which: again (default) | first | top
const fs=require('fs'),path=require('path');process.env.ENGINE=process.env.ENGINE||'build/engine_count.wasm';
const load=require(path.resolve(__dirname,'load.js'));const log=console.log;console.log=()=>{};
(async()=>{const {e,h}=await load();e.workp();const st=JSON.parse(fs.readFileSync('build/states.json'));const ids=Object.keys(st).map(Number);
 const gn=JSON.parse(fs.readFileSync('build/ngroups.json'));
 const run=()=>{let t=0;while(t<80000000){const n=e.run(h.halt,1000000);t+=n;if(e.val(h.halt))break;}return t;};
 const ev=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);return run();};
 const kinj=(s,m=0)=>{for(let i=0;i<6;i++){const c=s.charCodeAt(i)||0;if(c)e.inject(h.keyv[i],c);}e.inject(h.keyl,s.length);e.inject(h.ev[0],2);if(m)e.inject(h.ev[2],m);e.inject(h.ev[3],1000);};
 const key=(s,m=0)=>{kinj(s,m);return run();};
 const settle=()=>{for(let i=0,quiet=0;i<20000&&quiet<3;i++){if(!e.val(h.timer))break;const n=ev(7);quiet=n<200?quiet+1:0;}};
 ev(1);let s='';for(let i=0;i<1900;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';
 for(let i=0;i<s.length&&i<h.cb2max;i++)e.bset(h.cb2+i,s.charCodeAt(i));ev(8,0,0,Math.min(s.length,h.cb2max));settle();
 const which=process.argv[2]||'again';
 if(which!='first')key('x');
 if(which=='top'){key('a',1);key('ArrowLeft');}
 const W=()=>new Float32Array(e.memory.buffer,e.workp(),h.n);
 kinj(process.env.CH||(which=='top'?'z':'y'));let tot=0,t=0;const gt={};
 for(;t<5000;t++){const w0=Float32Array.from(W());const F=()=>new Float32Array(e.memory.buffer,e.firep(),h.n);const f0=Float32Array.from(F());const ops0=[0,1,2,3].map(k=>e.ops(k));const E0=e.edges();const act=ids.filter(i=>e.val(i)>0.5).map(i=>st[i]);e.run(h.halt,1);const ops1=[0,1,2,3].map(k=>e.ops(k));
  const fl=2*(e.edges()-E0)+2*(ops1[1]-ops0[1]+ops1[3]-ops0[3])+(ops1[0]-ops0[0])+(ops1[2]-ops0[2]);const w=W();const g={};for(let i=0;i<h.n;i++){const d=w[i]-w0[i];if(d)g[gn[i]]=(g[gn[i]]||0)+d;}
  tot+=fl;if(process.env.TT&&+process.env.TT==t){const db=JSON.parse(fs.readFileSync('build/netdbg.json'));const ln={};db.new.forEach((n,o)=>{if(n>=0)ln[n]=(db.line[o]||'').split(' ').slice(0,+(process.env.DEPTH||1)).join(' ');});const gl={},gc={};for(let i=0;i<h.n;i++){const d=w[i]-w0[i];if(d){gl[ln[i]]=(gl[ln[i]]||0)+d;gc[ln[i]]=(gc[ln[i]]||0)+1;}}for(const k of Object.keys(gl).sort((a,b)=>gl[b]-gl[a]).slice(0,50))log('  L',k,gl[k],'neurons',gc[k]);if(process.env.FIRES){const f=F();const fan=i=>e.ostart(i+1)-e.ostart(i);const r=[];for(let i=0;i<h.n;i++){const c=f[i]-f0[i];if(c>=+process.env.FIRES)r.push([i,c,w[i]-w0[i]]);}r.sort((a,b)=>b[2]-a[2]);let sw=0;for(const [i,c,d] of r){sw+=d;log('  F',i,ln[i],'fires',c,'work',d,'fan',fan(i));}log('  F total',r.length,sw);const LL={};for(let i=0;i<h.n;i++){const d=w[i]-w0[i],c=f[i]-f0[i];if(d||c){const k=ln[i];LL[k]=LL[k]||[0,0,0];LL[k][0]+=d;LL[k][1]+=c;LL[k][2]++;}}for(const k of Object.keys(LL).sort((a,b)=>LL[b][0]-LL[a][0]).slice(0,60))log('  G',k,'work',LL[k][0],'fires',LL[k][1],'neurons',LL[k][2]);}if(process.env.NEUR){const fan=i=>e.ostart(i+1)-e.ostart(i);const ix=[];for(let i=0;i<h.n;i++){const d=w[i]-w0[i];if(d)ix.push([i,d]);}ix.sort((a,b)=>b[1]-a[1]);for(const [i,d] of ix.slice(0,+process.env.NEUR))log('  N',i,ln[i],d,'fan',fan(i));}}const top=Object.entries(g).sort((a,b)=>b[1]-a[1]).slice(0,+(process.env.NG||3)).map(x=>x[0]+':'+x[1]).join(' ');
  log(t,act.join(','),'ops',fl,'|',top);if(e.val(h.halt))break;}
 if(process.env.VALS)log('VALS',process.env.VALS.split(',').map(i=>i+'='+e.val(+i)).join(' '));
 log('total ops-ish',tot,'ticks',t+1);
})();
