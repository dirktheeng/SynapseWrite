// Work per network group during the long paste. Run after: clang -DCOUNT build/engine_count.wasm (test/work.sh). Usage: ENGINE=build/engine_count.wasm node test/gprof.js paste|png|wheel
const fs=require('fs');const load=require('./load');
load().then(({e,h,bank})=>{const gn=JSON.parse(fs.readFileSync('build/ngroups.json'));const nm=JSON.parse(fs.readFileSync('build/names.json'));const st=JSON.parse(fs.readFileSync('build/states.json'));
 const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);return e.run(h.halt,80000000);};D(1);
 let s='';for(let i=0;i<300;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';
 const mode=process.argv[2]||'paste';let n;
 if(mode=='png'){const p=e.workp();const w=new Float32Array(e.memory.buffer,p,h.n);const u=fs.readFileSync('build/p_rgb.png');const b=bank();for(let i=0;i<u.length;i++)b[h.file+i]=u[i];n=D(10,0,0,u.length);rep(w)}
 else if(mode=='paste'){const p=e.workp();const w=new Float32Array(e.memory.buffer,p,h.n);const b=bank();for(let i=0;i<s.length;i++)b[h.cb2+i]=s.charCodeAt(i);n=D(8,0,0,s.length);rep(w)}
 else {const b=bank();for(let i=0;i<s.length;i++)b[h.cb2+i]=s.charCodeAt(i);D(8,0,0,s.length);const p=e.workp();const w=new Float32Array(e.memory.buffer,p,h.n);n=D(6,0,0,700);rep(w)}
 function rep(w){const g={};let tot=0;for(let i=0;i<h.n;i++){g[gn[i]]=(g[gn[i]]||0)+w[i];tot+=w[i];}
  console.log('ticks',n,'work',tot);for(const k of Object.keys(g).sort((a,b)=>g[b]-g[a]).slice(0,10))console.log(k.padEnd(32),g[k],(100*g[k]/tot).toFixed(1)+'%');
  const top=[...w.keys()].sort((a,b)=>w[b]-w[a]).slice(0,+process.argv[3]||30);for(const i of top)console.log(i,gn[i],(w[i]/n).toFixed(2),nm[i]||st[i]||'');}
});
