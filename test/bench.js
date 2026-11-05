// Headless benchmark and per-state profile of the network, run in node through the engine only.
// Usage: node test/bench.js [prof]    prof adds per-state ticks and edges for each event.
const fs=require('fs'),zlib=require('zlib');const load=require('./load');
load().then(({e,h,bank})=>{
 const st=JSON.parse(fs.readFileSync('build/states.json'));const ids=Object.keys(st).map(Number);
 const prof=process.argv[2]==='prof';const out={};
 const D=(label,k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);
  const E0=e.edges();const O0=e.ops?[0,1,2,3].map(k=>e.ops(k)):null;let n=0;const t0=process.hrtime.bigint();
  if(prof){const cnt={},ed={};let last=E0;while(n<80000000){const fired=[];for(const i of ids)if(e.val(i))fired.push(st[i]);e.run(h.halt,1);n++;const d=e.edges()-last;last+=d;const s=fired[0]||'?';cnt[s]=(cnt[s]||0)+1;ed[s]=(ed[s]||0)+d;if(e.val(h.halt))break;}
   const top=Object.keys(ed).sort((x,y)=>ed[y]-ed[x]).slice(0,14);console.log(label,'ticks',n,'edges',e.edges()-E0);for(const s of top)console.log('   ',s,cnt[s],ed[s],(ed[s]/cnt[s]).toFixed(0));}
  else n=e.run(h.halt,80000000);
  const ms=Number(process.hrtime.bigint()-t0)/1e6;const oc=O0?' work '+Math.round(e.edges()-E0+[0,1,2,3].reduce((a,k)=>a+e.ops(k)-O0[k],0)):'';console.log(label.padEnd(24),ms.toFixed(2).padStart(10),'ms ticks',n,'edges',e.edges()-E0,oc);out[label]=ms;};
 const t0=Date.now();D('init',1);
 let s='';for(let i=0;i<1900;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';
 s=s.slice(0,390000);{const b=bank();for(let i=0;i<s.length;i++)b[h.cb2+i]=s.charCodeAt(i);}D('paste1900',8,0,0,s.length);
 for(let i=0;i<3;i++)D('type at end',2,120);D('wheel',6,0,0,400);D('selall',2,97,1);D('left',2,128);D('type at top',2,122);D('down',2,131);D('enter',2,13);D('undo',2,122,1);
 const u=fs.readFileSync('build/p_rgb.png');{const b=bank();for(let i=0;i<u.length;i++)b[h.file+i]=u[i];}D('png',10,0,0,u.length);
 console.log(JSON.stringify(out));
}).catch(x=>console.log(x.stack));
