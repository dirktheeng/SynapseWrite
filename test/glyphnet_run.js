// Runs a glyph network file on the real engine. Input JSON: {net,draws:[{ch,face,s,y0,rows,cells,snapy,snapx,large,bold,slant}]}
// Output: coverage rows as a Float32 binary, and one line of JSON per draw with ticks and work counters.
const fs=require('fs'),zlib=require('zlib');
(async()=>{const req=JSON.parse(fs.readFileSync(process.argv[2]));const blob=zlib.gunzipSync(fs.readFileSync(req.net));
 const hl=blob.readUInt32LE(0);const h=JSON.parse(blob.subarray(4,4+hl).toString());let o=4+hl;o+=(4-o%4)%4;
 const {instance:{exports:e}}=await WebAssembly.instantiate(fs.readFileSync(req.engine||process.env.ENGINE||'build/engine.wasm'),{});
 e.setup(h.n,h.e,h.L,h.nports,h.bank,h.ni,h.nt,h.dn,h.wn);const put=(p,n)=>{new Uint8Array(e.memory.buffer,p,n).set(blob.subarray(o,o+n));o+=n;};
 put(e.p_istart(),4*(h.n+1));put(e.p_isrc(),4*h.ni);put(e.p_iwi(),2*h.ni);put(e.p_act(),h.n);put(e.p_bias(),8*h.n);put(e.p_ostart(),4*(h.n+1));put(e.p_dz(),h.dn);put(e.p_wz(),h.wn);put(e.p_lstart(),4*(h.L+1));put(e.p_ports(),4*h.nports);put(e.p_wtab(),8*h.nt);e.finish();
 for(const [i,v] of h.init)e.inject(i,v);e.run(h.halt,2);
 const I=h.I;let bank=new Float32Array(e.memory.buffer,e.p_bank(),h.bank);const out=[];let addr=16;const res=[];const hasOps=!!e.ops;
 const t00=process.hrtime.bigint();
 for(const d of req.draws){const E0=e.edges();const O0=hasOps?[0,1,2,3].map(k=>e.ops(k)):null;
  const cells=d.cells,n=d.rows*cells;for(let i=0;i<n;i++)bank[addr+i]=0;
  e.inject(I.start,1);e.inject(I.ch,d.ch);e.inject(I.face,d.face+0);e.inject(I.s,d.s);e.inject(I.y0,d.y0);e.inject(I.rows,d.rows);e.inject(I.addr,addr);e.inject(I.cells,cells);
  for(const k of ['snapy','snapx','large','bold','slant'])if(d[k])e.inject(I[k],d[k]);
  const tk=e.run(h.halt,100000)+e.run(h.halt,1);
  res.push({a:addr,t:tk,ed:e.edges()-E0,op:hasOps?[0,1,2,3].map(k=>e.ops(k)-O0[k]):null});
  addr+=n;if(addr>h.bank-10000)throw 'bank';}
 const ms=Number(process.hrtime.bigint()-t00)/1e6;
 fs.writeFileSync(req.out,Buffer.from(bank.buffer,bank.byteOffset,addr*4));
 fs.writeFileSync(req.out+'.json',JSON.stringify({ms,res,n:h.n}));
})().catch(x=>{console.log(x.stack||x);process.exit(1)});
