// Edges per event by sub-network, for the t4 events and a file open. Build the COUNT engine first (test/work.sh).
// Usage: ENGINE=build/engine_count.wasm node test/eprof.js [file.docx]
const fs=require('fs');const load=require('./load');
load().then(({e,h,bank})=>{const gn=JSON.parse(fs.readFileSync('build/ngroups.json'));const nm=JSON.parse(fs.readFileSync('build/names.json'));e.workp();const W=()=>new Float32Array(e.memory.buffer,e.workp(),h.n);const F=()=>new Float32Array(e.memory.buffer,e.firep(),h.n);
 const fan=new Float64Array(h.n);for(let i=0;i<h.n;i++)fan[i]=e.ostart(i+1<h.n?i+1:i)-e.ostart(i);
 const D=(label,k,a=0,b=0,c=0)=>{const f0=Float32Array.from(F());const w0=Float32Array.from(W());e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);const E0=e.edges();const n=e.run(h.halt,2000000000);
  const f=F(),w=W();const g={};for(let i=0;i<h.n;i++){const d=process.env.WORK?w[i]-w0[i]:(f[i]-f0[i])*fan[i];if(d)g[gn[i]]=(g[gn[i]]||0)+d;}
  console.log(label,'ticks',n,'edges',e.edges()-E0);if(process.env.TOP&&label==process.env.TOP){if(process.env.LINES){const db=JSON.parse(fs.readFileSync('build/netdbg.json'));const ln={};db.new.forEach((n,o)=>{if(n>=0)ln[n]=(db.line[o]||'').split(' ')[0];});const gl={};for(let i=0;i<h.n;i++){const d=w[i]-w0[i];if(d)gl[ln[i]]=(gl[ln[i]]||0)+d;}for(const k of Object.keys(gl).sort((a,b)=>gl[b]-gl[a]).slice(0,40))console.log('  L',k,gl[k]);}const ix=[...Array(h.n).keys()].map(i=>[i,process.env.WORK?w[i]-w0[i]:(f[i]-f0[i])*fan[i],f[i]-f0[i]]).sort((a,b)=>b[1]-a[1]).slice(0,40);for(const [i,d,c] of ix)console.log('  #',i,gn[i],d,'fires',c,'fan',fan[i],nm[i]||'');}for(const k of Object.keys(g).sort((a,b)=>g[b]-g[a]).slice(0,14))console.log('   ',k.padEnd(34),g[k]);};
 D('init',1);
 if(process.argv[2]){const u=fs.readFileSync(process.argv[2]);const b=bank();for(let i=0;i<u.length;i++)b[h.file+i]=u[i];D('open',9,0,0,u.length);return;}
 let s='';for(let i=0;i<1900;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';
 s=s.slice(0,390000);{const b=bank();for(let i=0;i<s.length;i++)b[h.cb2+i]=s.charCodeAt(i);}D('paste1900',8,0,0,s.length);
 for(let i=0;i<3;i++)D('type at end'+i,2,120);D('wheel',6,0,0,400);D('selall',2,97,1);D('left',2,128);D('type at top',2,122);D('down',2,131);D('enter',2,13);D('undo',2,122,1);
});
