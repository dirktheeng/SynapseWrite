// Loads build/net.bin.gz and build/engine.wasm in node the same way the glue does.
const fs=require('fs'),zlib=require('zlib');
module.exports=async()=>{const t0=process.hrtime.bigint();const blob=zlib.gunzipSync(fs.readFileSync('build/net.bin.gz'));const t1=process.hrtime.bigint();
 const hl=blob.readUInt32LE(0);const h=JSON.parse(blob.subarray(4,4+hl).toString());let o=4+hl;o+=(4-o%4)%4;
 const {instance:{exports:e}}=await WebAssembly.instantiate(fs.readFileSync('build/engine.wasm'),{});
 e.setup(h.n,h.e,h.L,h.nports,h.bank,h.ni);const put=(p,n)=>{new Uint8Array(e.memory.buffer,p,n).set(blob.subarray(o,o+n));o+=n;};
 put(e.p_istart(),4*(h.n+1));put(e.p_isrc(),4*h.ni);put(e.p_iw(),8*h.ni);put(e.p_act(),h.n);put(e.p_bias(),8*h.n);put(e.p_ostart(),4*(h.n+1));put(e.p_dst(),4*h.e);put(e.p_w(),8*h.e);put(e.p_lstart(),4*(h.L+1));put(e.p_ports(),4*h.nports);e.finish();
 for(const [i,v] of h.init)e.inject(i,v);const bank=()=>new Float32Array(e.memory.buffer,e.p_bank(),h.bank);{const b=bank();for(const [a,v] of h.bank_init)b[a]=v;}
 console.log('load ms gunzip',Number(t1-t0)/1e6,'rest',Number(process.hrtime.bigint()-t1)/1e6);
 return {e,h,bank};};
