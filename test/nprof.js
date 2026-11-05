// Per-neuron fan-out profile restricted to ticks that follow a named state. Usage: node test/nprof.js STATE [event]
const fs=require('fs');const load=require('./load');
load().then(({e,h,bank})=>{
 const st=JSON.parse(fs.readFileSync('build/states.json'));const nm=JSON.parse(fs.readFileSync('build/names.json'));const ids=Object.keys(st).map(Number);
 const want=process.argv[2];const wid=+ids.find(i=>st[i]===want);
 const os=new Int32Array(e.memory.buffer,e.p_ostart(),h.n+1);const v=new Float64Array(e.memory.buffer,e.p_v(),h.n);
 const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);return e.run(h.halt,80000000);};
 D(1);let s='';for(let i=0;i<40;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how.\n';{const b=bank();for(let i=0;i<s.length;i++)b[h.cb2+i]=s.charCodeAt(i);}
 e.inject(h.ev[0],8);e.inject(h.ev[3],s.length);
 const cnt=new Float64Array(h.n);let ticks=0,total=0,fires=0;
 for(let t=0;t<3000000;t++){const hit=e.val(wid)!=0;e.run(h.halt,1);if(hit){ticks++;for(let i=0;i<h.n;i++)if(v[i]!=0){const f=os[i+1]-os[i];cnt[i]+=f;total+=f;fires++;}}if(e.val(h.halt))break;}
 console.log('state',want,'ticks',ticks,'edges/tick',(total/ticks).toFixed(0),'fired/tick',(fires/ticks).toFixed(0));
 const top=[...cnt.keys()].sort((a,b)=>cnt[b]-cnt[a]).slice(0,+process.argv[3]||30);for(const i of top)console.log(i,(cnt[i]/ticks).toFixed(1),'fan',os[i+1]-os[i],nm[i]||st[i]||'');
});
