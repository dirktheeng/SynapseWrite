// Headless event driver shared by the a7 tests: runs events through the engine and writes framebuffers as PNG.
const fs=require('fs'),zlib=require('zlib'),crypto=require('crypto');const load=require('./load');
const ids=JSON.parse(fs.readFileSync('build/ui_ids.json'));
function png(rgba,w,h){const crcT=[];for(let n=0;n<256;n++){let c=n;for(let k=0;k<8;k++)c=c&1?0xedb88320^(c>>>1):c>>>1;crcT[n]=c>>>0;}
 const crc=b=>{let c=~0;for(const x of b)c=crcT[(c^x)&255]^(c>>>8);return (~c)>>>0;};const ch=(t,d)=>{const l=Buffer.alloc(4);l.writeUInt32BE(d.length);const td=Buffer.concat([Buffer.from(t),d]);const r=Buffer.alloc(4);r.writeUInt32BE(crc(td));return Buffer.concat([l,td,r]);};
 const raw=Buffer.alloc((w*3+1)*h);let o=0;for(let y=0;y<h;y++){raw[o++]=0;for(let x=0;x<w;x++){const i=(y*w+x)*4;raw[o++]=rgba[i];raw[o++]=rgba[i+1];raw[o++]=rgba[i+2];}}
 const ih=Buffer.alloc(13);ih.writeUInt32BE(w,0);ih.writeUInt32BE(h,4);ih[8]=8;ih[9]=2;return Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),ch('IHDR',ih),ch('IDAT',zlib.deflateSync(raw,{level:1})),ch('IEND',Buffer.alloc(0))]);}
module.exports=async()=>{const {e,h,bank}=await load();let tm=0,tnow=100000;
 const raw=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);e.inject(h.ev[4],20000);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);const E0=e.edges();const O0=e.ops?[0,1,2,3].reduce((q,i)=>q+e.ops(i),0):0;const t0=process.hrtime.bigint();
  const n=e.run(h.halt,30000000);const ms=Number(process.hrtime.bigint()-t0)/1e6;const m=e.val(h.timer);if(m)tm=m;A.saved=e.val(h.saveout)?[e.val(h.saveout),e.val(h.outbase)]:A.saved;const ed=e.edges()-E0;if(n>=60000000)console.log('STUCK event',k);return {n,ed,w:e.ops?ed+[0,1,2,3].reduce((q,i)=>q+e.ops(i),0)-O0:0,ms};};
 const add=(a,b)=>({n:a.n+b.n,ed:a.ed+b.ed,w:a.w+b.w,ms:a.ms+b.ms});
 const A={raw,add,e,h,bank,ids,saved:null,
  key:(c,m=0)=>raw(2,typeof c==='string'?c.charCodeAt(0):c,m,tnow+=5000),
  type:s=>{let r;for(const ch of s)r=A.key(ch);return r;},
  click:(x,y)=>add(raw(3,x,y,tnow+=5000),raw(4,x,y)),
  ctl:(id)=>{const c=ids[id];if(!c)throw new Error(id);return A.click(c[0],c[1]);},
  paste:s=>{const b=bank();for(let i=0;i<s.length;i++)b[h.cb2+i]=s.charCodeAt(i);return raw(8,0,0,s.length);},
  move:(x,y)=>raw(11,x,y),wheel:d=>raw(6,0,0,d+1000),tick:()=>raw(7),
  // background repagination runs to its end, as the host's short timer would do it
  settle:()=>{let t={n:0,ed:0,w:0,ms:0};for(let c=0;c<4000;c++){tm=0;t=add(t,raw(7));if(tm!==1)break;}return t;},
  file:(k,u)=>{const b=bank();for(let i=0;i<u.length;i++)b[h.file+i]=u[i];return raw(k,0,0,u.length);},
  savedBytes:()=>{const b=bank(),[n,a]=A.saved;const u=Buffer.alloc(n);for(let i=0;i<n;i++)u[i]=b[a+i];return u;},
  fb:()=>new Uint8Array(e.memory.buffer,e.p_fb(),1280*800*4),
  hash:(y0=174,y1=776)=>{const f=A.fb();return crypto.createHash('md5').update(f.subarray(y0*1280*4,y1*1280*4).filter((_,i)=>(i&3)!=3)).digest('hex').slice(0,10);},
  shot:(p)=>{fs.writeFileSync(p,png(A.fb(),1280,800));},tm:()=>tm};
 raw(1);return A;};
