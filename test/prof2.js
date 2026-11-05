// Fan-out weighted activity per neuron, sampled during an event. Usage: node prof2.js png|paint
const fs=require('fs'),zlib=require('zlib');const blob=zlib.gunzipSync(fs.readFileSync('build/net.bin.gz'));
const hl=blob.readUInt32LE(0);const h=JSON.parse(blob.subarray(4,4+hl).toString());let o=4+hl;o+=(4-o%4)%4;
WebAssembly.instantiate(fs.readFileSync('build/engine.wasm'),{}).then(({instance:{exports:e}})=>{
 e.setup(h.n,h.e,h.L,h.nports,h.bank,h.ni);const put=(p,n)=>{new Uint8Array(e.memory.buffer,p,n).set(blob.subarray(o,o+n));o+=n;};
 put(e.p_istart(),4*(h.n+1));put(e.p_isrc(),4*h.ni);put(e.p_iw(),8*h.ni);put(e.p_act(),h.n);put(e.p_bias(),8*h.n);put(e.p_ostart(),4*(h.n+1));put(e.p_dst(),4*h.e);put(e.p_w(),8*h.e);put(e.p_lstart(),4*(h.L+1));put(e.p_ports(),4*h.nports);e.finish();
 for(const [i,v] of h.init)e.inject(i,v);const bank=()=>new Float32Array(e.memory.buffer,e.p_bank(),h.bank);{const b=bank();for(const [a,v] of h.bank_init)b[a]=v;}
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
