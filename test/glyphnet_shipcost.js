// The shipping network's real cost for painting: count engine, a full page repaint, split by state.
const fs=require('fs');process.env.ENGINE='build/engine_count.wasm';const load=require('./load');
load().then(({e,h,bank})=>{const st=JSON.parse(fs.readFileSync('build/states.json'));const ids=Object.keys(st).map(Number);
 const work=()=>e.edges()+[0,1,2,3].reduce((a,k)=>a+e.ops(k),0);
 const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);return e.run(h.halt,80000000);};
 D(1);let s='';while(s.length<12000)s+='The quick brown fox jumps over the lazy dog while minimum Home Document Quality glyph tests run on. ';
 {const b=bank();for(let i=0;i<s.length;i++)b[h.cb2+i]=s.charCodeAt(i);}D(8,0,0,s.length);
 e.inject(h.ev[0],6);e.inject(h.ev[3],400);let w0=work(),res={},last=w0,ticks=0;
 for(let n=0;n<2000000;n++){const fired=[];for(const i of ids)if(e.val(i))fired.push(st[i]);e.run(h.halt,1);ticks++;const w=work(),O=w-last;last=w;const nm=fired[0]||'?';(res[nm]=res[nm]||[0,0]);res[nm][0]++;res[nm][1]+=O;if(e.val(h.halt))break;}
 const top=Object.entries(res).sort((a,b)=>b[1][1]-a[1][1]).slice(0,6);
 // idle tick cost
 let w1=work();e.run(h.halt,1);const idle=work()-w1;
 console.log(JSON.stringify({ticks,total:last-w0,top,idle,edges:e.edges()}));
 // wall clock with the normal engine is taken from bench.js
}).catch(x=>console.log(x.stack));
