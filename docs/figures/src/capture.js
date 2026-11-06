// Runs the real weights in node on the counting engine and records which neurons fire for each event. Run from the repo root after ./make.sh.
// clang -DCOUNT ... -o build/engine_count.wasm host/engine.c ; ENGINE=build/engine_count.wasm node docs/figures/src/capture.js OUT
const fs=require('fs'),path=require('path');process.chdir(process.cwd());
const load=require(path.resolve('test/load.js'));const out=process.argv[2];fs.mkdirSync(out,{recursive:true});
load().then(({e,h})=>{e.workp();
 const N=h.n,M=()=>e.memory.buffer;const V=()=>new Float64Array(M(),e.p_v(),N),F=()=>new Float32Array(M(),e.firep(),N);
 const fb=()=>new Uint8Array(M(),e.p_fb(),1280*800*4);
 const prev=new Float32Array(N);const gs=JSON.parse(fs.readFileSync('build/ngroups.json'));
 const groups=[...new Set(gs)];const gi=new Map(groups.map((g,i)=>[g,i]));
 const frames=[];let fno=0;const meta=[];
 function run(name,set,maxFrames){const E0=e.edges();set();const fired=new Set();let t=0;const perTick=[];const every=[];
  while(t<400000){e.run(h.halt,1);t++;const f=F(),v=V();const now=[];for(let i=0;i<N;i++){if(f[i]!==prev[i]||v[i]!==0){now.push(i);fired.add(i);prev[i]=f[i];}}
   perTick.push(now);if(e.val(h.halt))break;}
  const idx=[];const n=Math.min(maxFrames,t);for(let k=0;k<n;k++)idx.push(Math.floor(k*t/n));
  // a frame carries every neuron fired since the last frame
  const fr=[];for(let k=0;k<n;k++){const a=idx[k],b=k+1<n?idx[k+1]:t;const s=new Set();for(let q=a;q<b;q++)for(const i of perTick[q])s.add(i);fr.push({tick:b,n:[...s]});}
  fs.writeFileSync(`${out}/fb_${name}.bin`,Buffer.from(fb()));
  const byg={};for(const i of fired){byg[gs[i]]=(byg[gs[i]]||0)+1;}
  meta.push({name,ticks:t,edges:e.edges()-E0,fired:fired.size,byg,frames:fr});console.log(name,'ticks',t,'edges',e.edges()-E0,'fired',fired.size,'of',N);}
 const ev=(k,a=0,b=0,c=0)=>()=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);};
 const key=(s,mods=0)=>()=>{for(let i=0;i<6;i++){const c=s.charCodeAt(i)||0;if(c)e.inject(h.keyv[i],c);}e.inject(h.keyl,s.length);ev(2,0,mods,1000)();};
 run('start',ev(1),40);
 const T='Neural programs have no training step.\nEvery weight below is written by a generator.\n';
 for(let i=0;i<T.length;i++)e.bset(h.cb2+i,T.charCodeAt(i));run('paste',ev(8,0,0,T.length),30);
 run('key_new',key('Q'),30);run('key_same',key('Q'),30);run('mouse_move',ev(22,500,400,0),8);run('click',ev(3,560,300,2000),24);ev(4,560,300)();e.run(h.halt,100000);
 run('wheel',ev(6,0,0,1100),12);run('bold',key('b',1),24);
 fs.writeFileSync(`${out}/meta.json`,JSON.stringify({N,groups,gs,meta}));
});
