// Per-neuron pushed edges in ticks that start in a named state, during a file open. Lines from build/netdbg.json (NETDBG=1 build).
// Usage: ENGINE=build/engine_count.wasm node test/cmp2_sprof.js file.docx STATE [max ticks sampled]
const fs=require('fs');const load=require('./load');
load().then(({e,h,bank})=>{e.workp();const st=JSON.parse(fs.readFileSync("build/states.json"));const wid=+Object.keys(st).find(i=>st[i]===process.argv[3]);
 const db=JSON.parse(fs.readFileSync('build/netdbg.json'));const ln={};db.new.forEach((n,o)=>{if(n>=0)ln[n]=(db.line[o]||'').split(' ')[0];});
 const fan=new Float64Array(h.n);for(let i=0;i<h.n;i++)fan[i]=e.ostart(i+1<h.n?i+1:i)-e.ostart(i);
 e.inject(h.ev[0],1);e.run(h.halt,2000000000);
 const u=fs.readFileSync(process.argv[2]);const b=bank();for(let i=0;i<u.length;i++)b[h.file+i]=u[i];
 e.inject(h.ev[0],9);e.inject(h.ev[3],u.length);const F=()=>new Float32Array(e.memory.buffer,e.firep(),h.n);
 const cnt=new Float64Array(h.n);let n=0,tot=0;const MAX=+(process.argv[4]||2000);
 for(;;){const hit=e.val(wid)>0.5&&n<MAX;let f0;if(hit)f0=Float32Array.from(F());const E0=e.edges();e.run(h.halt,1);if(hit){n++;tot+=e.edges()-E0;const f=F();for(let i=0;i<h.n;i++){const d=f[i]-f0[i];if(d)cnt[i]+=d*fan[i];}}if(e.val(h.halt))break;}
 console.log('ticks',n,'edges/tick',(tot/n).toFixed(1));const L={};for(let i=0;i<h.n;i++)if(cnt[i]){L[ln[i]]=(L[ln[i]]||0)+cnt[i];}
 for(const k of Object.keys(L).sort((a,b)=>L[b]-L[a]).slice(0,25))console.log(' ',k,(L[k]/n).toFixed(2));
 const top=[...cnt.keys()].sort((a,b)=>cnt[b]-cnt[a]).slice(0,25);for(const i of top)console.log('  #',i,ln[i],(cnt[i]/n).toFixed(2),'fan',fan[i]);});
