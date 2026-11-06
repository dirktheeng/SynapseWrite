// Glue: runs ANN inference, encodes events and bytes as vectors, displays the output
// tensor, and executes what the network commands. It never interprets event or document data.
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
let timer=0,pendClip=null;
// Clipboard write: the async API, then the copy event, then a code telling the network that only its own copy holds the text.
const writeClip=t=>{const fail=()=>{let ok=false;try{ok=document.execCommand('copy');}catch(_){}if(!ok)dispatch(13,2);};try{navigator.clipboard.writeText(t).catch(fail);}catch(_){fail();}};
window.addEventListener('copy',ev=>{if(pendClip!==null){ev.clipboardData.setData('text/plain',pendClip);ev.preventDefault();}});window.addEventListener('cut',ev=>{if(pendClip!==null){ev.clipboardData.setData('text/plain',pendClip);ev.preventDefault();}});
const stats=window.annStats={ticks:0,ms:0,edges:0,events:0};
// A text the network placed in the bank: code units to a browser string.
const text=(a,n)=>{const bb=bank();let s='';for(let i=0;i<n;i+=8192)s+=String.fromCharCode(...bb.subarray(a+i,a+Math.min(n,i+8192)));return s;};
const pick=fn=>{const f=document.createElement('input');f.type='file';f.onchange=()=>f.files[0]&&fn(f.files[0]);f.click();};
const dispatch=(k,a=0,b=0,c=0)=>{
 const t0=performance.now();const E0=e.edges();
 e.inject(h.ev[0],k);e.inject(h.ev[4],Math.floor((Date.now()-new Date().getTimezoneOffset()*6e4)/864e5));if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);
 const n=e.run(h.halt,window.annMax||50000000);
 {const dr=new Uint8Array(mem(),e.p_drow(),801),f=new Uint32Array(mem(),e.p_fb(),1024000),q=new Uint32Array(img.data.buffer);for(let y=0;y<800;y++)if(dr[y]){let z=y;while(dr[z])dr[z++]=0;for(let i=y*1280,j=z*1280;i<j;i++)q[i]=f[i]|0xff000000;ctx.putImageData(img,0,0,0,y,1280,z-y);y=z;}}
 // Commands from the network, each read from its own output neuron.
 const held=e.val(h.chold),clip=e.val(h.clipout);if(held)pendClip=null;if(clip){const t=text(h.cb,clip-1);window.annClip=t;pendClip=t;if(!held)writeClip(t);}
 const fl=e.val(h.fileout);if(fl){const a0=e.val(h.outbase);saveFile(new Uint8Array(bank().subarray(a0,a0+fl)),text(e.val(h.namea),e.val(h.namen)));}
 if(e.val(h.wpic))pick(openPic);
 if(e.val(h.wopen))pick(openFile);
 const kb=e.val(h.kbo);if(kb)ti.value=text(h.kbq,kb-1);
 if(e.val(h.ffield))ti.focus({preventScroll:true});
 if(e.val(h.fback))setTimeout(()=>cv.focus({preventScroll:true}),0);
 const wp=e.val(h.wantp);
 const ms=e.val(h.timer);if(ms){clearTimeout(timer);timer=setTimeout(()=>dispatch(7),ms);}
 if(wp)try{navigator.clipboard.readText().then(t=>pasteText(t)).catch(()=>dispatch(13,1));}catch(_){dispatch(13,1);}
 stats.ticks=n;stats.ms=performance.now()-t0;stats['k'+k]=stats.ms;stats['t'+k]=n;stats['e'+k]=e.edges()-E0;stats.edges=e.edges()-E0;stats.events++;
};
const units=(a,t,n)=>{const bb=bank();for(let i=0;i<n;i++)bb[a+i]=t.charCodeAt(i);};
const pasteText=(t,fromKey=0)=>{const n=Math.min(t.length,h.cb2max);units(h.cb2,t,n);dispatch(8,fromKey,0,n);};
window.annPaste=t=>pasteText(t);
const bytes=(k)=>async f=>{const u=new Uint8Array(await f.arrayBuffer());const n=Math.min(u.length,h.fmax);bank().set(u.subarray(0,n),h.file);dispatch(k,0,0,n);};
const openFile=bytes(9),openPic=bytes(10);window.annPic=openPic;window.annOpen=openFile;window.addEventListener('dragover',ev=>ev.preventDefault());window.addEventListener('drop',ev=>{ev.preventDefault();if(ev.dataTransfer.files[0])openFile(ev.dataTransfer.files[0]);});
const saveFile=async (u,name)=>{let dl=null;try{dl=window.claude?await window.claude.use('downloads'):null;}catch(_){}
 if(dl){try{await dl.save({filename:name,data:u});}catch(_){}return;}
 const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([u]));a.download=name;a.click();};
// Keys: the code units of the key name, its length, and raw modifier bits. The network names them and says whether the browser default stands.
window.addEventListener('keydown',ev=>{const s=ev.key||'';for(let i=0;i<6;i++)e.inject(h.keyv[i],s.charCodeAt(i)||0);e.inject(h.keyl,s.length);
 dispatch(2,0,ev.ctrlKey+2*ev.shiftKey+4*ev.metaKey+8*ev.repeat,Math.floor(performance.now()));if(!e.val(h.pass_))ev.preventDefault();});
window.addEventListener('paste',ev=>{ev.preventDefault();pasteText(ev.clipboardData.getData('text'),1);});
const pos=ev=>{const r=cv.getBoundingClientRect();return [Math.round((ev.clientX-r.left)*1280/r.width),Math.round((ev.clientY-r.top)*800/r.height)];};
cv.addEventListener('mousedown',ev=>{cv.focus({preventScroll:true});const [x,y]=pos(ev);dispatch(3,x,y,Math.floor(performance.now()));});
window.addEventListener('mouseup',ev=>{const [x,y]=pos(ev);dispatch(4,x,y);});
// Mouse moves carry the raw button mask. When the network asks to hold, later moves wait for the next frame and only the latest runs.
let waiting=false,queued=null;const frame=f=>{if(waiting){queued=f;return;}f();if(e.val(h.hold)){waiting=true;requestAnimationFrame(()=>{waiting=false;const g=queued;queued=null;g&&frame(g);});}};
cv.addEventListener('mouseleave',()=>dispatch(11));cv.addEventListener('mouseenter',ev=>{const [x,y]=pos(ev);dispatch(23,x,y,ev.buttons);});window.addEventListener('mousemove',ev=>frame(()=>{const [x,y]=pos(ev);dispatch(22,x,y,ev.buttons);}));
cv.addEventListener('wheel',ev=>{ev.preventDefault();dispatch(6,0,0,Math.round(ev.deltaY)+1000);},{passive:false});
// The hidden field summons the on-screen keyboard. Its whole text goes to the network, with 1 at composition start and 2 at composition end.
const ti=document.getElementById('kb');const field=phase=>{const v=ti.value,n=Math.min(v.length,h.kbmax);units(h.kbv,v,n);dispatch(27,phase,0,n);};
ti.addEventListener('input',()=>field(0));ti.addEventListener('compositionstart',()=>field(1));ti.addEventListener('compositionend',()=>field(2));
window.addEventListener('pointerdown',ev=>dispatch(21,ev.pointerType.charCodeAt(0)));window.addEventListener('pointermove',ev=>dispatch(21,ev.pointerType.charCodeAt(0),1));
cv.addEventListener('click',()=>dispatch(24));
const ty=ev=>Math.round(ev.touches[0].clientY*1280/cv.getBoundingClientRect().width);
cv.addEventListener('touchstart',ev=>dispatch(25,ty(ev),ev.touches.length),{passive:true});
cv.addEventListener('touchmove',ev=>{dispatch(26,ty(ev),ev.touches.length);if(!e.val(h.pass_))ev.preventDefault();},{passive:false});
window.annDispatch=dispatch;window.annVal=i=>e.val(i);dispatch(1);window.annReady=true;
})();
