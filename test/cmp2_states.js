// Ticks spent in chosen FSM states during a file open, and edges pushed in those ticks.
// Usage: ENGINE=build/engine_count.wasm node test/cmp2_states.js file.docx STATE,STATE,...
const fs=require('fs');const load=require('./load');
load().then(({e,h,bank})=>{const st=JSON.parse(fs.readFileSync('build/states.json'));const want=new Set((process.argv[3]||'').split(','));const ids=Object.keys(st).map(Number).filter(i=>!process.argv[3]||want.has(st[i]));
 e.inject(h.ev[0],1);e.run(h.halt,2000000000);
 const u=fs.readFileSync(process.argv[2]);const b=bank();for(let i=0;i<u.length;i++)b[h.file+i]=u[i];
 e.inject(h.ev[0],9);e.inject(h.ev[3],u.length);const cnt={},ed={};let t=0,E=e.edges();
 for(;;t++){const on=ids.filter(i=>e.val(i)>0.5);const E0=e.edges();e.run(h.halt,1);const d=e.edges()-E0;for(const i of on){cnt[st[i]]=(cnt[st[i]]||0)+1;ed[st[i]]=(ed[st[i]]||0)+d;}if(e.val(h.halt))break;}
 console.log('ticks',t+1,'edges',e.edges()-E);for(const k of Object.keys(cnt).sort((a,b)=>ed[b]-ed[a]))console.log(k.padEnd(10),'ticks',cnt[k],'edges',ed[k]);});
