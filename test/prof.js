const d=require('./drive');(async()=>{const {b,p}=await d();
 await p.keyboard.type('hello world');
 const r=await p.evaluate(()=>{const e=annE,h=annH;const os=new Int32Array(e.memory.buffer,e.p_ostart(),h.n+1);const cnt=new Float64Array(h.n);
  const B=annBank();for(let i=0;i<200;i++)B[h.cb2+i]=97;
  e.inject(h.ev[0],8);e.inject(h.ev[3],150);let total=0,ticks=0;
  while(ticks<1200){const n=e.run(h.halt,1);ticks++;const v=new Float64Array(e.memory.buffer,e.p_v(),h.n);for(let i=0;i<h.n;i++)if(v[i]!=0){const f=os[i+1]-os[i];cnt[i]+=f;total+=f;}if(n==1&&e.val(h.halt))break;}
  const top=[...cnt.keys()].sort((a,b)=>cnt[b]-cnt[a]).slice(0,25).map(i=>[i,cnt[i]/ticks,os[i+1]-os[i]]);
  return {ticks,per:total/ticks,top};});
 console.log(r.ticks,r.per);for(const t of r.top)console.log(t.join(' '));await b.close();})();
