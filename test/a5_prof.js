// Work per state while opening a file with the counting engine. Run test/work.sh's clang line first.
// Usage: ENGINE=build/engine_count.wasm node test/a5_prof.js file.docx [top]
const fs=require('fs');const load=require('./load');
load().then(({e,h,bank})=>{const gn=JSON.parse(fs.readFileSync('build/ngroups.json'));const nm=JSON.parse(fs.readFileSync('build/names.json'));const st=JSON.parse(fs.readFileSync('build/states.json'));
 const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);return e.run(h.halt,2000000000);};D(1);
 const u=fs.readFileSync(process.argv[2]);const b=bank();for(let i=0;i<u.length;i++)b[h.file+i]=u[i];
 const p=e.workp();const w=new Float32Array(e.memory.buffer,p,h.n);const n=D(9,0,0,u.length);
 const g={};let tot=0;for(let i=0;i<h.n;i++){g[gn[i]]=(g[gn[i]]||0)+w[i];tot+=w[i];}
 console.log('ticks',n,'work',tot);for(const k of Object.keys(g).sort((a,b)=>g[b]-g[a]).slice(0,8))console.log(k.padEnd(32),g[k],(100*g[k]/tot).toFixed(1)+'%');
 const top=[...w.keys()].filter(i=>st[i]).sort((a,b)=>w[b]-w[a]).slice(0,+process.argv[3]||30);for(const i of top)console.log(st[i].padEnd(12),w[i]);
});
