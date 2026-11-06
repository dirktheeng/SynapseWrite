// Debug tool: the state path of one event, in order, with edges per state.
const fs=require('fs');const lib=require('./a7_lib');const st=JSON.parse(fs.readFileSync('build/states.json'));const ids=Object.keys(st).map(Number);
const text=(n=1900)=>{let s='';for(let i=0;i<n;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';return s;};
(async()=>{const A=await lib();const e=A.e,h=A.h;
 const trace=(label,k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);e.inject(h.ev[4],20000);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);let n=0,E=e.edges();const o=[];for(;n<3000000;n++){e.run(h.halt,1);const E1=e.edges();const f=ids.filter(i=>e.val(i)).map(i=>st[i]).join(',')||'?';o.push(f+':'+(E1-E));E=E1;if(e.val(h.halt))break;}console.log('--',label,n+1,o.join(' '));};
 A.paste(text());A.key('x');
 trace('key y',2,121,0,1e6+1e4);
 process.exit(0);
})();
