// Fuzz world: the real weights on the checked engine, driven only through the same event vector the glue encodes.
// It does what the glue does with the outputs (clipboard, save bytes, file pickers, timers). It knows nothing of the application.
const fs=require('fs'),zlib=require('zlib'),path=require('path'),crypto=require('crypto');
const R=p=>path.resolve(__dirname,'..',p);
const blob=zlib.gunzipSync(fs.readFileSync(R('build/net.bin.gz')));const hl=blob.readUInt32LE(0);const h=JSON.parse(blob.subarray(4,4+hl).toString());
const off0=(4+hl+3)&~3;
const states=JSON.parse(fs.readFileSync(R('build/states.json')));const stIds=Object.keys(states).map(Number);
const names=JSON.parse(fs.readFileSync(R('build/names.json')));
const dbg=JSON.parse(fs.readFileSync(R('build/dbg.json')));const dbin=fs.readFileSync(R('build/dbg.bin'));
const ui=JSON.parse(fs.readFileSync(R('build/ui_ids.json')));
const modChecked=new WebAssembly.Module(fs.readFileSync(R('build/engine_check.wasm')));
const modPlain=new WebAssembly.Module(fs.readFileSync(R('build/engine.wasm')));
let groups=null;const grp=i=>{if(!groups)groups=JSON.parse(fs.readFileSync(R('build/ngroups.json')));return groups[i];};
const KN={1:'OOB_WRITE',2:'OOB_READ',3:'RECT_OOB',4:'ROW_OOB',5:'TWO_TOKENS',6:'STATE_NONBOOL',7:'AND_NONBOOL',8:'NONFINITE',9:'F32_LOSS',10:'REGION_CROSS',11:'BAD_ADDR',12:'PATCH'};
const NAMED={Backspace:8,Tab:9,Enter:13,Escape:27,Delete:127,Left:128,Up:129,Right:130,Down:131,Home:132,End:133,PageUp:134,PageDown:135};
class World{
 constructor(o={}){this.checked=o.checked!==false;this.cap=o.cap||60000000;this.now=1000;this.fails=[];this.ticks=0;this.saves=[];this.events=0;this.warn=new Map();
  const {exports:e}=new WebAssembly.Instance(this.checked?modChecked:modPlain,{});this.e=e;let o_=off0;
  e.setup(h.n,h.e,h.L,h.nports,h.bank,h.ni,h.nt,h.nb,h.zn,h.n1);const put=(p,n)=>{new Uint8Array(e.memory.buffer,p,n).set(blob.subarray(o_,o_+n));o_+=n;};
  put(e.p_zb(),h.zn);put(e.p_lstart(),4*(h.L+1));put(e.p_ports(),4*h.nports);put(e.p_wtab(),8*h.nt);put(e.p_btab(),8*h.nb);e.finish();
  if(this.checked){e.dbg_init(h.bank,stIds.length,dbg.regs.length,dbg.na,dbg.nas,dbg.nw);const M=()=>e.memory.buffer;
   new Int32Array(M(),e.d_ptr(0),stIds.length).set(stIds);new Int32Array(M(),e.d_ptr(1),dbg.regs.length).set(dbg.regs);
   let q=0;const take=(k,n,T)=>{const a=new T(M(),e.d_ptr(k),n);const by=n*T.BYTES_PER_ELEMENT;a.set(new T(dbin.buffer.slice(dbin.byteOffset+q,dbin.byteOffset+q+by)));q+=by;};
   take(2,dbg.na+1,Int32Array);take(3,dbg.nas,Int32Array);take(4,dbg.nas,Float64Array);take(5,dbg.na,Float64Array);take(6,dbg.na,Int32Array);take(7,h.n+1,Int32Array);take(8,dbg.nw,Int32Array);this.seen=0;}
  for(const [i,v] of h.init)e.inject(i,v);e.dom();for(const [i,v] of h.init1)e.inject(i,v);e.dom();for(const [a,v] of h.bank_init)e.bset(a,v);{let q=o_;for(const [a,n,w] of h.rom)for(let i=0;i<n;i++,q+=w){const x=w==1?blob[q]:blob[q]+256*blob[q+1]+(w>2?65536*blob[q+2]:0);if(x)e.bset(a+i,x);}}
  this.pendTimer=0;this.pendOpen=false;this.pendPic=false;this.sysClip='';this.clip=null;this.dead=false;
  if(!o.noboot)this.D(1);}
 bank(){const e=this.e;return new Proxy({},{get:(_,k)=>e.bget(+k),set:(_,k,x)=>{e.bset(+k,x);return true;}});}
 fb(){return new Uint32Array(this.e.memory.buffer,this.e.p_fb(),1024000);}
 hash(y0=0,y1=800,x0=0,x1=1280){const f=this.fb();let a=2166136261>>>0,b=0x9747b28c;for(let y=y0;y<y1;y++){for(let i=y*1280+x0,j=y*1280+x1;i<j;i++){const c=f[i]&0xffffff;a=Math.imul(a^c,16777619);b=Math.imul(b^(c>>>3),0x5bd1e995);}}return (a>>>0).toString(16)+(b>>>0).toString(16);}
 snap(){return this.fb().slice();}
 box(a,b,y0=174,y1=776){let x0=9999,x1=-1,yy0=9999,yy1=-1,n=0;for(let y=y0;y<y1;y++)for(let x=0;x<1280;x++){const i=y*1280+x;if((a[i]^b[i])&0xffffff){n++;if(x<x0)x0=x;if(x>x1)x1=x;if(y<yy0)yy0=y;if(y>yy1)yy1=y;}}return n?`${n}px x${x0}-${x1} y${yy0}-${yy1}`:'none';}
 docHash(){return this.hash(174,776,0,1280);}
 active(){const on=[];for(const i of stIds)if(this.e.val(i))on.push(states[i]);return on;}
 D(k,a=0,b=0,c=0){if(this.dead)return 0;const e=this.e;this.events++;this.lastEv=[k,a,b,c];
  e.inject(h.ev[0],k);e.inject(h.ev[4],20000);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);
  let n;try{n=e.run(h.halt,this.cap);}catch(x){if(this.checked)this.scan();this.fail('TRAP',x.message);this.dead=true;return 0;}
  this.ticks+=n;this.lastTicks=n;
  if(n>=this.cap&&!e.val(h.halt)){if(this.checked)this.scan();this.fail('HANG',this.active().join(','));this.dead=true;return n;}
  if(this.checked)this.scan();
  const clip=e.val(h.clipout);if(clip){const bb=this.bank();const cs=[];for(let i=0;i<clip-1&&i<400000;i++)cs.push(bb[h.cb+i]);this.clip=String.fromCharCode(...cs.slice(0,120000));this.clipN=clip-1;this.sysClip=this.clip;}
  const sv=e.val(h.saveout),pd=e.val(h.pdfout);if(sv||pd){const nn=sv||pd,bb=this.bank(),a0=e.val(h.outbase);if(a0<0||a0+nn>h.bank)this.fail('SAVE_OOB',a0+'+'+nn);else{const u=new Uint8Array(nn);for(let i=0;i<nn;i++)u[i]=bb[a0+i];if(sv)this.lastSave=u;else this.lastPdf=u;}}
  if(e.val(h.wpic))this.pendPic=true;if(e.val(h.wopen))this.pendOpen=true;
  const wp=e.val(h.wantp);const ms=e.val(h.timer);if(ms)this.pendTimer=ms;
  if(wp){if(this.denyClip)this.D(13,1);else this.paste(this.sysClip);}
  return n;}
 scan(){const e=this.e,nn=e.d_n();if(nn<=this.seen)return;const l=new DataView(e.memory.buffer,e.d_ptr(9));for(let i=this.seen;i<nn;i++){const o=i*24;const k=l.getInt32(o,true),a=l.getInt32(o+8,true),b=l.getInt32(o+12,true),x=l.getFloat64(o+16,true);this.note(k,a,b,x);}this.seen=nn;}
 note(k,a,b,x){const nm=KN[k];let id;
  if(k==5)id=states[a]+'+'+states[b];else if(k==6)id=states[a];else if(k==7)id='and#'+a;else id='port@'+a+(k==10?'/'+dbg.regn[dbg.regs[b]]:'');
  const rec=nm+' '+id;const info={ev:this.lastEv,x,st:this.active().slice(0,4).join(','),n:this.events};
  if(k==9||k==10){if(!this.warn.has(rec))this.warn.set(rec,info);}else this.fail(nm,id,info);}
 fail(cls,id,info){this.fails.push({cls,id,ev:this.lastEv,n:this.events,info});}
 key(c,m=0){this.now+=7;return this.D(2,c,m,this.now);}
 type(s){for(const ch of s)this.key(ch==='\n'?13:ch.charCodeAt(0));}
 down(x,y){this.now+=30;this.D(3,x,y,this.now);}
 up(x,y){this.now+=5;this.D(4,x,y);}
 click(x,y){this.D(11,x,y);this.down(x,y);this.up(x,y);}
 dragTo(x,y){this.now+=16;this.D(5,x,y);}
 hover(x,y){this.D(11,x,y);}
 wheel(d){this.D(6,0,0,d+1000);}
 timer(ms){if(ms==null)ms=this.pendTimer;if(!ms)return;this.pendTimer=0;this.now+=ms;this.D(7);}
 settle(max=400){let i=0;while(this.pendTimer&&i++<max&&this.pendTimer<400){this.timer();}return i;}
 paste(t,fromKey=0){const bb=this.bank();const n=Math.min(t.length,390000);for(let i=0;i<n;i++)bb[h.cb2+i]=t.charCodeAt(i);this.D(8,fromKey,0,n);}
 openBytes(u){const bb=this.bank();const n=Math.min(u.length,h.fmax);for(let i=0;i<n;i++)bb[h.file+i]=u[i];this.pendOpen=false;this.D(9,0,0,n);}
 picBytes(u){const bb=this.bank();const n=Math.min(u.length,h.fmax);for(let i=0;i<n;i++)bb[h.file+i]=u[i];this.pendPic=false;this.D(10,0,0,n);}
 save(){this.lastSave=null;this.key(115,1);return this.lastSave;}
 screen(f){const zp=this.fb();const out=Buffer.alloc(1280*800*3);for(let i=0;i<1024000;i++){const c=zp[i];out[i*3]=c&255;out[i*3+1]=(c>>8)&255;out[i*3+2]=(c>>16)&255;}
  // minimal PNG writer for looking at failures
  const crcT=[];for(let n=0;n<256;n++){let c=n;for(let k=0;k<8;k++)c=c&1?0xedb88320^(c>>>1):c>>>1;crcT[n]=c>>>0;}const crc=b=>{let c=0xffffffff;for(const x of b)c=crcT[(c^x)&255]^(c>>>8);return (c^0xffffffff)>>>0;};
  const chunk=(t,d)=>{const l=Buffer.alloc(4);l.writeUInt32BE(d.length);const td=Buffer.concat([Buffer.from(t),d]);const r=Buffer.alloc(4);r.writeUInt32BE(crc(td));return Buffer.concat([l,td,r]);};
  const raw=Buffer.alloc((1280*3+1)*800);for(let y=0;y<800;y++)out.copy(raw,y*(1280*3+1)+1,y*1280*3,(y+1)*1280*3);const ih=Buffer.alloc(13);ih.writeUInt32BE(1280,0);ih.writeUInt32BE(800,4);ih[8]=8;ih[9]=2;
  fs.writeFileSync(f,Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),chunk('IHDR',ih),chunk('IDAT',zlib.deflateSync(raw)),chunk('IEND',Buffer.alloc(0))]));}
}
// Reads a saved zip with node only, checking every CRC. Returns {name:Buffer} or throws.
function unzip(u){u=Buffer.from(u);let eo=u.length-22;while(eo>=0&&u.readUInt32LE(eo)!==0x06054b50)eo--;if(eo<0)throw Error('no EOCD');const n=u.readUInt16LE(eo+10);let o=u.readUInt32LE(eo+16);const r={};
 for(let i=0;i<n;i++){if(u.readUInt32LE(o)!==0x02014b50)throw Error('bad CD');const meth=u.readUInt16LE(o+10),crc=u.readUInt32LE(o+16),cs=u.readUInt32LE(o+20),us=u.readUInt32LE(o+24),nl=u.readUInt16LE(o+28),xl=u.readUInt16LE(o+30),cl=u.readUInt16LE(o+32),lo=u.readUInt32LE(o+42);const name=u.subarray(o+46,o+46+nl).toString();
  const dn=u.readUInt16LE(lo+26),dx=u.readUInt16LE(lo+28);const d=u.subarray(lo+30+dn+dx,lo+30+dn+dx+cs);const v=meth?zlib.inflateRawSync(d):d;if(v.length!==us)throw Error('size '+name);if(zlib.crc32(v)>>>0!==crc>>>0)throw Error('crc '+name);r[name]=v;o+=46+nl+xl+cl;}
 return r;}
module.exports={World,h,dbg,states,names,ui,NAMED,grp,unzip,R};
