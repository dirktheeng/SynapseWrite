// Glue: runs ANN inference, encodes events and bytes as vectors, displays the output
// tensor, and executes what the network commands. It never inspects document data.
(async()=>{
const b64=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
const gunzip=async u=>new Uint8Array(await new Response(new Blob([u]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer());
const blob=await gunzip(b64(window.NET_B64));
const hl=new DataView(blob.buffer).getUint32(0,true);const h=JSON.parse(new TextDecoder().decode(blob.subarray(4,4+hl)));
let o=4+hl;o+=(4-o%4)%4;
const {instance:{exports:e}}=await WebAssembly.instantiate(b64(window.ENG_B64),{});
e.setup(h.n,h.e,h.L,h.nports,h.bank,h.ni,h.nt,h.dn,h.wn);
const mem=()=>e.memory.buffer;
const put=(ptr,bytes)=>{new Uint8Array(mem(),ptr,bytes).set(blob.subarray(o,o+bytes));o+=bytes;};
put(e.p_istart(),4*(h.n+1));put(e.p_isrc(),4*h.ni);put(e.p_iwi(),2*h.ni);put(e.p_act(),h.n);put(e.p_bias(),8*h.n);put(e.p_ostart(),4*(h.n+1));put(e.p_dz(),h.dn);put(e.p_wz(),h.wn);put(e.p_lstart(),4*(h.L+1));put(e.p_ports(),4*h.nports);put(e.p_wtab(),8*h.nt);
e.finish();
for(const [i,v] of h.init)e.inject(i,v);
const bank=()=>new Float32Array(mem(),e.p_bank(),h.bank);
{const b=bank();for(const [a,v] of h.bank_init)b[a]=v;}
const cv=document.getElementById('screen'),ctx=cv.getContext('2d',{alpha:false,willReadFrequently:true});const img=ctx.createImageData(1280,800);
let timer=0;const stats=window.annStats={ticks:0,ms:0,edges:0,events:0};
const dispatch=(k,a=0,b=0,c=0)=>{
 const t0=performance.now();const E0=e.edges();
 e.inject(h.ev[0],k);e.inject(h.ev[4],Math.floor((Date.now()-new Date().getTimezoneOffset()*6e4)/864e5));if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);
 const n=e.run(h.halt,window.annMax||50000000);
 {const dr=new Uint8Array(mem(),e.p_drow(),801),f=new Uint32Array(mem(),e.p_fb(),1024000),q=new Uint32Array(img.data.buffer);for(let y=0;y<800;y++)if(dr[y]){let z=y;while(dr[z])dr[z++]=0;for(let i=y*1280,j=z*1280;i<j;i++)q[i]=f[i]|0xff000000;ctx.putImageData(img,0,0,0,y,1280,z-y);y=z;}}
 const clip=e.val(h.clipout);if(clip){const bb=bank();const cs=[];for(let i=0;i<clip-1;i++)cs.push(bb[h.cb+i]);const txt=String.fromCharCode(...cs);window.annClip=txt;try{navigator.clipboard.writeText(txt).catch(()=>{});}catch(_){}}
 const sv=e.val(h.saveout),pd=e.val(h.pdfout);if(sv||pd){const n=sv||pd,bb=bank(),a0=e.val(h.outbase);const u=new Uint8Array(n);for(let i=0;i<n;i++)u[i]=bb[a0+i];saveFile(u,sv?'Document1.docx':'Document1.pdf');}
 if(e.val(h.wpic)){const f=document.createElement('input');f.type='file';f.onchange=()=>f.files[0]&&openPic(f.files[0]);f.click();}
 if(e.val(h.wopen)){const f=document.createElement('input');f.type='file';f.onchange=()=>f.files[0]&&openFile(f.files[0]);f.click();}
 const wp=e.val(h.wantp);
 const ms=e.val(h.timer);clearTimeout(timer);if(ms)timer=setTimeout(()=>dispatch(7),ms);
 if(wp)try{navigator.clipboard.readText().then(pasteText).catch(()=>{});}catch(_){}
 stats.ticks=n;stats.ms=performance.now()-t0;stats['k'+k]=stats.ms;stats['t'+k]=n;stats['e'+k]=e.edges()-E0;stats.edges=e.edges()-E0;stats.events++;
};
const pasteText=t=>{const bb=bank();const n=Math.min(t.length,390000);for(let i=0;i<n;i++)bb[h.cb2+i]=t.charCodeAt(i);dispatch(8,0,0,n);};
window.annPaste=pasteText;
const openFile=async f=>{const u=new Uint8Array(await f.arrayBuffer());const bb=bank();const n=Math.min(u.length,400000);for(let i=0;i<n;i++)bb[h.file+i]=u[i];dispatch(9,0,0,n);};
const openPic=async f=>{const u=new Uint8Array(await f.arrayBuffer());const bb=bank();const n=Math.min(u.length,400000);for(let i=0;i<n;i++)bb[h.file+i]=u[i];dispatch(10,0,0,n);};window.annPic=openPic;window.annOpen=openFile;window.addEventListener('dragover',ev=>ev.preventDefault());window.addEventListener('drop',ev=>{ev.preventDefault();if(ev.dataTransfer.files[0])openFile(ev.dataTransfer.files[0]);});
const saveFile=async (u,name)=>{let dl=null;try{dl=window.claude?await window.claude.use('downloads'):null;}catch(_){}
 if(dl){try{await dl.save({filename:name,data:u});}catch(_){}return;}
 const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([u]));a.download=name;a.click();};
const NAMED={Backspace:8,Tab:9,Enter:13,Escape:27,Delete:127,ArrowLeft:128,ArrowUp:129,ArrowRight:130,ArrowDown:131,Home:132,End:133,PageUp:134,PageDown:135};
const mods=ev=>(ev.ctrlKey||ev.metaKey?1:0)+(ev.shiftKey?2:0);
window.addEventListener('keydown',ev=>{let c=NAMED[ev.key];if(!c&&ev.key.length===1)c=(ev.ctrlKey||ev.metaKey)?ev.key.toLowerCase().charCodeAt(0):ev.key.charCodeAt(0);
 if(!c)return;if((ev.ctrlKey||ev.metaKey)&&c===118)return;ev.preventDefault();dispatch(2,c,mods(ev));});
window.addEventListener('paste',ev=>{ev.preventDefault();pasteText(ev.clipboardData.getData('text'));});
const pos=ev=>{const r=cv.getBoundingClientRect();return [Math.round((ev.clientX-r.left)*1280/r.width),Math.round((ev.clientY-r.top)*800/r.height)];};
cv.addEventListener('mousedown',ev=>{const [x,y]=pos(ev);dispatch(3,x,y);});
window.addEventListener('mouseup',ev=>{const [x,y]=pos(ev);dispatch(4,x,y);});
let moving=false;window.addEventListener('mousemove',ev=>{if(!ev.buttons||moving)return;moving=true;requestAnimationFrame(()=>{moving=false;const [x,y]=pos(ev);dispatch(5,x,y);});});
cv.addEventListener('wheel',ev=>{ev.preventDefault();dispatch(6,0,0,Math.round(ev.deltaY)+1000);},{passive:false});
window.annDispatch=dispatch;window.annVal=i=>e.val(i);dispatch(1);window.annReady=true;
})();
