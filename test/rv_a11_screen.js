// The screen check: damage to the image is repaired by a later blink tick, and undamaged documents never trigger it.
// Headless through the engine, since damage cannot be made through events. Judged on the framebuffer.
const load=require(process.cwd()+'/test/load');const fs=require('fs');
let fails=0;const ok=(n,c,x)=>{if(!c)fails++;console.log(c?'PASS':'FAIL',n,x===undefined?'':x);};
load().then(({e,h,bank})=>{
 const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);return e.run(h.halt,80000000);};
 const T=s=>{for(const c of s)D(2,c=='\n'?13:c.charCodeAt(0));};
 const paste=s=>{const b=bank();for(let i=0;i<s.length;i++)b[h.cb2+i]=s.charCodeAt(i);D(8,0,0,s.length);};
 const fb=()=>new Uint8Array(e.memory.buffer,e.p_fb(),1280*800*4);const bad=()=>{for(let i=0;i<4;i++)D(7);};
 const tot=()=>{const k=e.val(h.screenbad);return k;};
 const seen=[];const count=async()=>0;
 D(1);T('Plain text with words\nSecond line\n\n');D(12);
 paste('A longer paragraph that runs on for quite a while so that it wraps across more than one line of the page and keeps going.\n\nThird\n');
 D(2,'e'.charCodeAt(0),1);T('centered\n');D(2,'l'.charCodeAt(0),1);
 for(let i=0;i<30;i++)D(7);
 const ref=fb().slice();D(7);D(7);
 let same=true;{const f=fb();for(let i=0;i<f.length;i++)if(f[i]!==ref[i]){same=false;break;}}
 ok('blink pairs leave the image alone',same);
 ok('no false alarm on an undamaged document',tot()===0,tot());
 // damage: wipe colors and ids over several text lines
 {const f=fb();for(let y=190;y<320;y++)for(let x=223;x<1040;x++){const o=4*(y*1280+x);f[o]=f[o+1]=f[o+2]=128;f[o+3]=0;}}
 for(let i=0;i<40;i++)D(7);D(7);D(7);
 let diff=0;{const f=fb();for(let i=0;i<f.length;i++)if(f[i]!==ref[i])diff++;}
 ok('damage repaired by the blink tick check',diff===0,diff);
 ok('the check is what found it',tot()>0,tot());
 console.log(fails?'FAILED':'all passed');process.exit(fails?1:0);
});
