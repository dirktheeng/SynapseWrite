// Loads build/net.bin.gz and build/engine.wasm in node the same way the glue does.
const fs=require('fs'),zlib=require('zlib');
module.exports=async()=>{const t0=process.hrtime.bigint();const blob=zlib.gunzipSync(fs.readFileSync('build/net.bin.gz'));const t1=process.hrtime.bigint();
 const hl=blob.readUInt32LE(0);const h=JSON.parse(blob.subarray(4,4+hl).toString());let o=4+hl;o+=(4-o%4)%4;
 const {instance:{exports:e}}=await WebAssembly.instantiate(fs.readFileSync(process.env.ENGINE||'build/engine.wasm'),{});
  e.setup(h.n,h.e,h.L,h.nports,h.bank,h.ni,h.nt,h.zn);new Uint8Array(e.memory.buffer,e.p_z(),h.zn).set(blob.subarray(o,o+h.zn));e.finish();
 for(const [i,v] of h.init)e.inject(i,v);const bank=()=>new Float32Array(e.memory.buffer,e.p_bank(),h.bank);{const b=bank();for(const [a,v] of h.bank_init)b[a]=v;}
 console.log('load ms gunzip',Number(t1-t0)/1e6,'rest',Number(process.hrtime.bigint()-t1)/1e6);
 return {e,h,bank};};
