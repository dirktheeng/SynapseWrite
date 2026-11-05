// Prints the state sequence and named registers for a short paste. Usage: node test/trace.js reg1,reg2
const fs=require('fs');const load=require('./load');
load().then(({e,h,bank})=>{const st=JSON.parse(fs.readFileSync('build/states.json'));const nm=JSON.parse(fs.readFileSync('build/names.json'));const ids=Object.keys(st).map(Number);
 const regs=(process.argv[2]||'').split(',').filter(x=>x);const rid=regs.map(r=>+Object.keys(nm).find(k=>nm[k]===r));
 const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);return e.run(h.halt,80000000);};D(1);
 const s='ab\ncd';{const b=bank();for(let i=0;i<s.length;i++)b[h.cb2+i]=s.charCodeAt(i);}
 e.inject(h.ev[0],8);e.inject(h.ev[3],s.length);
 for(let t=0;t<40;t++){e.run(h.halt,1);const f=ids.filter(i=>e.val(i)).map(i=>st[i]);console.log(t,f.join(','),regs.map((r,k)=>r+'='+e.val(rid[k])).join(' '));}
});
