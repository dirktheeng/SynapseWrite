// Repeat draw on the real engine: tag read, block read, patch port. Bank: tag at key, coverage at 1000.
const fs=require('fs'),zlib=require('zlib');
(async()=>{const [,,net,cov,W,H,N]=process.argv;const blob=zlib.gunzipSync(fs.readFileSync(net));const hl=blob.readUInt32LE(0);const h=JSON.parse(blob.subarray(4,4+hl).toString());let o=4+hl;o+=(4-o%4)%4;
 for(const eng of ['build/engine.wasm','build/engine_count.wasm']){let oo=o;
 const {instance:{exports:e}}=await WebAssembly.instantiate(fs.readFileSync(eng),{});
 e.setup(h.n,h.e,h.L,h.nports,h.bank,h.ni,h.nt,h.dn,h.wn);const put=(p,n)=>{new Uint8Array(e.memory.buffer,p,n).set(blob.subarray(oo,oo+n));oo+=n;};
 put(e.p_istart(),4*(h.n+1));put(e.p_isrc(),4*h.ni);put(e.p_iwi(),2*h.ni);put(e.p_act(),h.n);put(e.p_bias(),8*h.n);put(e.p_ostart(),4*(h.n+1));put(e.p_dz(),h.dn);put(e.p_wz(),h.wn);put(e.p_lstart(),4*(h.L+1));put(e.p_ports(),4*h.nports);put(e.p_wtab(),8*h.nt);e.finish();
 for(const [i,v] of h.init)e.inject(i,v);
 const bank=new Float32Array(e.memory.buffer,e.p_bank(),h.bank);const c=new Float32Array(fs.readFileSync(cov).buffer);bank.set(c,1000);bank[5]=1000;
 const n=+N,t0=process.hrtime.bigint();let ticks=0;const E0=e.edges();
 for(let i=0;i<n;i++){e.inject(h.go,1);e.inject(h.key,5);e.inject(h.px,10+i%800);e.inject(h.py,4096+100);ticks+=e.run(h.halt,20);e.run(h.halt,1);ticks++;}
 const ms=Number(process.hrtime.bigint()-t0)/1e6;
 console.log(JSON.stringify({eng,us_per_draw:ms*1000/n,ticks:ticks/n,edges:(e.edges()-E0)/n,ops:e.ops?[0,1,2,3].map(k=>e.ops(k)/n):null}));}
})().catch(x=>{console.log(x.stack||x);process.exit(1)});
