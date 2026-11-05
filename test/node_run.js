const fs=require('fs'),zlib=require('zlib');const blob=zlib.gunzipSync(fs.readFileSync('build/net.bin.gz'));
const hl=blob.readUInt32LE(0);const h=JSON.parse(blob.subarray(4,4+hl).toString());let o=4+hl;o+=(4-o%4)%4;
WebAssembly.instantiate(fs.readFileSync('build/engine.wasm'),{}).then(({instance:{exports:e}})=>{
 e.setup(h.n,h.e,h.L,h.nports,h.bank,h.ni);const put=(p,n)=>{new Uint8Array(e.memory.buffer,p,n).set(blob.subarray(o,o+n));o+=n;};
 put(e.p_istart(),4*(h.n+1));put(e.p_isrc(),4*h.ni);put(e.p_iw(),8*h.ni);put(e.p_act(),h.n);put(e.p_bias(),8*h.n);put(e.p_ostart(),4*(h.n+1));put(e.p_dst(),4*h.e);put(e.p_w(),8*h.e);put(e.p_lstart(),4*(h.L+1));put(e.p_ports(),4*h.nports);e.finish();
 for(const [i,v] of h.init)e.inject(i,v);const bank=()=>new Float32Array(e.memory.buffer,e.p_bank(),h.bank);{const b=bank();for(const [a,v] of h.bank_init)b[a]=v;}
 console.log('mem MB',e.memory.buffer.byteLength/1e6);
 const st=JSON.parse(fs.readFileSync('build/states.json'));
 const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);const t=Date.now();const n=e.run(h.halt,8000000);const on=[];for(const k2 in st)if(e.val(+k2))on.push(st[k2]);console.log('ev',k,'ticks',n,Date.now()-t,'ms',on.join(','),'timer',e.val(h.timer));};
 D(1);let s='';for(let i=0;i<1900;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';
 s=s.slice(0,390000);const b=bank();for(let i=0;i<s.length;i++)b[h.cb2+i]=s.charCodeAt(i);D(8,0,0,s.length);
 for(let i=0;i<4;i++)D(7);D(2,120);D(2,121);
}).catch(e=>console.log('ERR',e.stack));
