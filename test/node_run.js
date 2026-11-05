const fs=require('fs');require('./load')().then(({e,h,bank})=>{
console.log('mem MB',e.memory.buffer.byteLength/1e6);
 const st=JSON.parse(fs.readFileSync('build/states.json'));
 const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);const t=Date.now();const n=e.run(h.halt,8000000);const on=[];for(const k2 in st)if(e.val(+k2))on.push(st[k2]);console.log('ev',k,'ticks',n,Date.now()-t,'ms',on.join(','),'timer',e.val(h.timer));};
 D(1);let s='';for(let i=0;i<1900;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';
 s=s.slice(0,390000);const b=bank();for(let i=0;i<s.length;i++)b[h.cb2+i]=s.charCodeAt(i);D(8,0,0,s.length);
 for(let i=0;i<4;i++)D(7);D(2,120);D(2,121);
}).catch(e=>console.log('ERR',e.stack));
