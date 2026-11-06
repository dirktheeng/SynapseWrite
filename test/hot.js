const fs=require('fs'),zlib=require('zlib');const blob=zlib.gunzipSync(fs.readFileSync('build/net.bin.gz'));
const hl=blob.readUInt32LE(0);const h=JSON.parse(blob.subarray(4,4+hl).toString());let o=4+hl;o+=(4-o%4)%4;
WebAssembly.instantiate(fs.readFileSync('build/engine.wasm'),{}).then(({instance:{exports:e}})=>{
 e.setup(h.n,h.e,h.L,h.nports,h.bank,h.ni);const put=(p,n)=>{new Uint8Array(e.memory.buffer,p,n).set(blob.subarray(o,o+n));o+=n;};
 put(e.p_istart(),4*(h.n+1));put(e.p_isrc(),4*h.ni);put(e.p_iw(),8*h.ni);put(e.p_act(),h.n);put(e.p_bias(),8*h.n);put(e.p_ostart(),4*(h.n+1));put(e.p_dst(),4*h.e);put(e.p_w(),8*h.e);put(e.p_lstart(),4*(h.L+1));put(e.p_ports(),4*h.nports);e.finish();
 for(const [i,v] of h.init)e.inject(i,v);const bank=()=>new Float32Array(e.memory.buffer,e.p_bank(),h.bank);{const b=bank();for(const [a,v] of h.bank_init)b[a]=v;}
 const names=JSON.parse(fs.readFileSync('build/names.json'));
 const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);const E0=e.edges();const n=e.run(h.halt,8000000);console.log('ev',k,'ticks',n,'edges/tick',(e.edges()-E0)/n);};
 D(1);D(2,120);D(2,121);D(2,122);
 // live values at the halt tick
 const v=new Float64Array(e.memory.buffer,e.p_v(),h.n);const os=new Int32Array(e.memory.buffer,e.p_ostart(),h.n+1);
 const rows=[];let tot=0;for(let i=0;i<h.n;i++)if(v[i]!==0){const f=os[i+1]-os[i];tot+=f;rows.push([f,names[i]||i,v[i]]);}
 rows.sort((a,b)=>b[0]-a[0]);console.log('live',rows.length,'edges',tot);console.log(rows.slice(0,30).map(r=>r.join(':')).join(' '));
}).catch(e=>console.log('ERR',e.stack));
