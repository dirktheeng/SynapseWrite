// Edges per neuron during an open, with where each neuron was generated. Build with NETDBG=1 and the COUNT engine (test/work.sh).
// Usage: ENGINE=build/engine_count.wasm node test/oprof.js file.docx [top] [outfile]
const fs=require('fs');const load=require('./load');
load().then(({e,h,bank})=>{const gn=JSON.parse(fs.readFileSync('build/ngroups.json'));const nm=JSON.parse(fs.readFileSync('build/names.json'));const st=JSON.parse(fs.readFileSync('build/states.json'));
 const db=JSON.parse(fs.readFileSync('build/netdbg.json'));const line={};db.new.forEach((n,o)=>{if(n>=0)line[n]=db.line[o]||'';});
 const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);return e.run(h.halt,2000000000);};D(1);
 const u=fs.readFileSync(process.argv[2]);const b=bank();for(let i=0;i<u.length;i++)b[h.file+i]=u[i];
 e.workp();const E0=e.edges();const O0=[0,1,2,3].map(k=>e.ops(k));const n=D(9,0,0,u.length);
 const f=new Float32Array(e.memory.buffer,e.firep(),h.n);
 console.log('ticks',n,'edges',e.edges()-E0,'visits',e.ops(0)-O0[0],'lazy',e.ops(1)-O0[1],'pull',e.ops(2)-O0[2],'pullreads',e.ops(3)-O0[3]);
 const ed=[];for(let i=0;i<h.n;i++)ed[i]=f[i]*(e.ostart(i+1<h.n?i+1:i)-e.ostart(i));
 const g={},gl={};let tot=0;for(let i=0;i<h.n;i++){g[gn[i]]=(g[gn[i]]||0)+ed[i];tot+=ed[i];const l=(line[i]||'').split(' ')[0];gl[l]=(gl[l]||0)+ed[i];}
 for(const k of Object.keys(g).sort((a,b)=>g[b]-g[a]).slice(0,12))console.log(k.padEnd(32),g[k],(100*g[k]/tot).toFixed(1)+'%');
 for(const k of Object.keys(gl).sort((a,b)=>gl[b]-gl[a]).slice(0,25))console.log(k.padEnd(32),gl[k],(100*gl[k]/tot).toFixed(1)+'%');
 const top=[...ed.keys()].sort((a,b)=>ed[b]-ed[a]).slice(0,+process.argv[3]||40);for(const i of top)console.log(i,(gn[i]||'').slice(0,20),'edges',ed[i],'fires',f[i],'fan',ed[i]/f[i],nm[i]||st[i]||'',line[i]);
 if(process.argv[4])fs.writeFileSync(process.argv[4],JSON.stringify(ed));
});
