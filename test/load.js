// Loads build/net.bin.gz and build/engine.wasm in node the same way the glue does.
const fs=require('fs'),zlib=require('zlib');
module.exports=async()=>{const t0=process.hrtime.bigint();const blob=zlib.gunzipSync(fs.readFileSync('build/net.bin.gz'));const t1=process.hrtime.bigint();
 const hl=blob.readUInt32LE(0);const h=JSON.parse(blob.subarray(4,4+hl).toString());let o=4+hl;o+=(4-o%4)%4;
 const {instance:{exports:e}}=await WebAssembly.instantiate(fs.readFileSync(process.env.ENGINE||'build/engine.wasm'),{});
 e.setup(h.n,h.e,h.L,h.nports,h.bank,h.ni,h.nt,h.nb,h.zn,h.n1);const put=(p,n)=>{new Uint8Array(e.memory.buffer,p,n).set(blob.subarray(o,o+n));o+=n;};
 put(e.p_zb(),h.zn);put(e.p_lstart(),4*(h.L+1));put(e.p_ports(),4*h.nports);put(e.p_wtab(),8*h.nt);put(e.p_btab(),8*h.nb);e.finish();
 for(const [i,v] of h.init)e.inject(i,v);e.dom();for(const [i,v] of h.init1)e.inject(i,v);e.dom();const bank=()=>new Float32Array(e.memory.buffer,e.p_bank(),h.bank);{const b=bank();for(const [a,v] of h.bank_init)b[a]=v;}
 console.log('load ms gunzip',Number(t1-t0)/1e6,'rest',Number(process.hrtime.bigint()-t1)/1e6);
 return {e,h,bank};};
