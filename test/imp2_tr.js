// Debug tool: what each state costs for one event. Usage: node test/imp2_tr.js  (edit the script of events at the bottom)
const fs=require('fs');const lib=require('./a7_lib');const st=JSON.parse(fs.readFileSync('build/states.json'));const ids=Object.keys(st).map(Number);
const text=(n=1900)=>{let s='';for(let i=0;i<n;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';return s;};
(async()=>{const A=await lib();const e=A.e,h=A.h;
 const trace=(label,k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);e.inject(h.ev[4],20000);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);const S={};let n=0,E=e.edges();for(;n<3000000;n++){e.run(h.halt,1);const E1=e.edges();const f=ids.filter(i=>e.val(i)).map(i=>st[i]).join(',')||'?';const q=S[f]||(S[f]=[0,0]);q[0]++;q[1]+=E1-E;E=E1;if(e.val(h.halt))break;}
  const tot=Object.values(S).reduce((a,q)=>a+q[1],0);console.log('--',label,'ticks',n+1,'edges',tot);for(const k of Object.keys(S).sort((a,b)=>S[b][1]-S[a][1]).slice(0,+process.env.TOP||14))console.log('  ',k.padEnd(14),S[k][0],S[k][1]);};
 A.paste(text());
 trace('key x',2,120,0,1e6);A.shot('build/tr1.png');trace('key y',2,121,0,1e6+1e4);A.shot('build/tr2.png');
 trace('ctrl a',2,97,1,1e6+2e4);A.shot('build/tr3.png');
 process.exit(0);
})();
