// Deterministic work per event, as a surrogate for time on a busy machine. Runs the real weights in node on the
// counting engine (clang -DCOUNT ... -o build/engine_count.wasm host/engine.c) and drives them only through events.
// Multiply-adds: pushed edges, lazy input reads in the sweep, and reads inside lazy pulls. Activations: neuron visits plus pulls.
// FLOPs = 2 x multiply-adds + activations. Port work (pixel fills and copies in the engine) is reported separately as port calls.
// Usage: NODE_PATH=$(npm root -g) node test/flops.js [out.json]
const fs=require('fs'),path=require('path');process.env.ENGINE=process.env.ENGINE||'build/engine_count.wasm';
const load=require(path.resolve(__dirname,'load.js'));const log=console.log;console.log=()=>{};
(async()=>{const {e,h}=await load();e.workp();const ops=()=>[0,1,2,3].map(k=>e.ops(k));
 const run=()=>{let t=0;while(t<80000000){const n=e.run(h.halt,1000000);t+=n;if(e.val(h.halt))break;}return t;};
 const ev=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);return run();};
 const key=(s,m=0)=>{for(let i=0;i<6;i++){const c=s.charCodeAt(i)||0;if(c)e.inject(h.keyv[i],c);}e.inject(h.keyl,s.length);return ev(2,0,m,1000);};
 // Background work runs on timer events, as the glue does when the network asks for a timer. Settle until a timer tick is idle.
 const settle=()=>{let tot=0;for(let i=0,quiet=0;i<20000&&quiet<3;i++){if(!e.val(h.timer))break;const n=ev(7);tot+=n;quiet=n<200?quiet+1:0;}return tot;};
 const out=[];const meas=(name,fn)=>{const o0=ops(),E0=e.edges();const t=fn();const o1=ops(),E1=e.edges();
  const push=E1-E0,lz=(o1[1]-o0[1])+(o1[3]-o0[3]),act=(o1[0]-o0[0])+(o1[2]-o0[2]);const r={event:name,ticks:t,push_macs:push,lazy_macs:lz,activations:act,flops:2*(push+lz)+act};out.push(r);log(JSON.stringify(r));};
 meas('start',()=>ev(1));
 let s='';for(let i=0;i<1900;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';
 for(let i=0;i<s.length&&i<h.cb2max;i++)e.bset(h.cb2+i,s.charCodeAt(i));meas('paste 1900 paragraphs',()=>ev(8,0,0,Math.min(s.length,h.cb2max)));meas('background layout',settle);
 meas('type at end',()=>key('x'));meas('type at end, again',()=>key('y'));
 meas('select all',()=>key('a',1));meas('jump to top',()=>key('ArrowLeft'));meas('type at top',()=>key('z'));meas('down',()=>key('ArrowDown'));
 meas('enter at top',()=>key('Enter'));meas('undo',()=>key('z',1));
 meas('wheel down',()=>ev(6,1000,0,1100));meas('click in text',()=>ev(3,560,300,5000)+ev(4,560,300));meas('mouse move',()=>ev(22,600,420,0));
 meas('bold',()=>key('b',1));
 if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out,null,0));
})();
