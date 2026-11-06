// Wall clock of the same full repaint with the normal engine, best of 20.
const fs=require('fs');const load=require('./load');
load().then(({e,h,bank})=>{const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);return e.run(h.halt,80000000);};
 D(1);let s='';while(s.length<12000)s+='The quick brown fox jumps over the lazy dog while minimum Home Document Quality glyph tests run on. ';
 {const b=bank();for(let i=0;i<s.length;i++)b[h.cb2+i]=s.charCodeAt(i);}D(8,0,0,s.length);
 let best=1e9;for(let i=0;i<20;i++){const t=process.hrtime.bigint();D(6,0,0,i%2?400:-400);best=Math.min(best,Number(process.hrtime.bigint()-t)/1e6);}
 console.log(JSON.stringify({best_ms:best}));}).catch(x=>console.log(x.stack));
