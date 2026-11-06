// Debug tool: per neuron group fan out during the paint after the first far key. ENGINE=build/engine_count.wasm
const fs=require('fs');const lib=require('./a7_lib');const gn=JSON.parse(fs.readFileSync('build/ngroups.json'));const nm=JSON.parse(fs.readFileSync('build/names.json'));const st=JSON.parse(fs.readFileSync('build/states.json'));
const text=(n=1900)=>{let s='';for(let i=0;i<n;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';return s;};
(async()=>{const A=await lib();const e=A.e,h=A.h;A.paste(text());const wp=e.workp(),fp=e.firep();let w=new Float32Array(e.memory.buffer,wp,h.n);w.fill(0);new Float32Array(e.memory.buffer,fp,h.n).fill(0);const E0=e.edges();A.key(process.argv[3]||'x');console.log('edges',e.edges()-E0);w=new Float32Array(e.memory.buffer,wp,h.n);const f=new Float32Array(e.memory.buffer,fp,h.n);
 const os=i=>e.ostart(i+1)-e.ostart(i);const G={};for(let i=0;i<h.n;i++){const g=gn[i];const q=G[g]||(G[g]=[0,0]);q[0]+=f[i]*os(i);q[1]+=w[i];}
 for(const k of Object.keys(G).sort((a,b)=>G[b][0]-G[a][0]).slice(0,12))console.log(k.padEnd(30),G[k][0],G[k][1]);
 const top=[...f.keys()].sort((a,b)=>f[b]*os(b)-f[a]*os(a)).slice(0,+process.argv[2]||40);for(const i of top)console.log(i,gn[i],'fires',f[i],'fan',os(i),nm[i]||st[i]||'');process.exit(0);
})();
