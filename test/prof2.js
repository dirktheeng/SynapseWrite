const fs=require('fs');require('./load')().then(({e,h,bank})=>{
const nm=JSON.parse(fs.readFileSync('build/names.json'));const st=JSON.parse(fs.readFileSync('build/states.json'));
 const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);return e.run(h.halt,50000000);};
 D(1);const mode=process.argv[2];
 const u=fs.readFileSync('build/p_rgb.png');{const bb=bank();for(let i=0;i<u.length;i++)bb[h.file+i]=u[i];}
 const os=new Int32Array(e.memory.buffer,e.p_ostart(),h.n+1);const v=new Float64Array(e.memory.buffer,e.p_v(),h.n);
 const cnt=new Float64Array(h.n);let total=0,ticks=0;const N=+process.argv[3]||20000;
 e.inject(h.ev[0],10);e.inject(h.ev[3],u.length);
 const t0=Date.now();for(let t=0;t<N;t++){e.run(h.halt,1);ticks++;for(let i=0;i<h.n;i++)if(v[i]!=0){const f=os[i+1]-os[i];cnt[i]+=f;total+=f;}if(e.val(h.halt))break;}
 console.log('ticks',ticks,'edges/tick',Math.round(total/ticks));
 const top=[...cnt.keys()].sort((a,b)=>cnt[b]-cnt[a]).slice(0,24);for(const i of top)console.log(i,(cnt[i]/ticks).toFixed(1),os[i+1]-os[i],nm[i]||st[i]||'');
});
