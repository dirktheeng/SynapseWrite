// Worst case interactive events, headless and driven only by events through the engine.
// Usage: ENGINE=build/engine_count.wasm node test/a7_bench.js [scenario ...]   Prints ticks, edges, work and ms per event.
const fs=require('fs');const load=require('./load');const ids=JSON.parse(fs.readFileSync('build/ui_ids.json'));
const only=process.argv.slice(2);const WORD='Sphinx of black quartz judge my vow and then the quick brown fox jumps over a lazy dog again. ';
const para=n=>{let s='';while(s.length<n)s+=WORD;return s.slice(0,n);};
const MISS='wrold teh recieve adress seperate definately goverment occured neccessary tommorow ';
const SEN=[];const rows=[];
async function scen(name,fn){if(only.length&&!only.includes(name))return;
 const {e,h,bank}=await load();let tm=0;
 const raw=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);e.inject(h.ev[4],20000);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);const E0=e.edges();const O0=e.ops?[0,1,2,3].reduce((q,i)=>q+e.ops(i),0):0;const t0=process.hrtime.bigint();
  const n=e.run(h.halt,60000000);const ms=Number(process.hrtime.bigint()-t0)/1e6;const m=e.val(h.timer);if(m)tm=m;const ed=e.edges()-E0;return {n,ed,w:e.ops?ed+[0,1,2,3].reduce((q,i)=>q+e.ops(i),0)-O0:0,ms};};
 let tnow=100000;
 const A={raw,
  key:(c,m=0)=>raw(2,typeof c==='string'?c.charCodeAt(0):c,m,tnow+=500),
  type:s=>{let r;for(const ch of s)r=A.key(ch);return r;},
  click:(x,y)=>{const a=raw(3,x,y,tnow+=500);const b=raw(4,x,y);return add(a,b);},
  ctl:(id)=>{const c=ids[id];if(!c)throw new Error(id);return A.click(c[0],c[1]);},
  paste:s=>{const b=bank();for(let i=0;i<s.length;i++)b[h.cb2+i]=s.charCodeAt(i);return raw(8,0,0,s.length);},
  move:(x,y)=>raw(11,x,y),wheel:d=>raw(6,0,0,d+1000),tick:()=>raw(7),
  bg:()=>{let c=0,t=add0();while(c<2000){tm=0;const r=raw(7);t=add(t,r);c++;if(tm!==1)break;}return t;},
  file:(k,u)=>{const b=bank();for(let i=0;i<u.length;i++)b[h.file+i]=u[i];return raw(k,0,0,u.length);},
  log:(l,r)=>{const ms=r.ms;rows.push([name,l,r.n,r.ed,r.w,ms]);console.log((name+' / '+l).padEnd(46),String(r.n).padStart(9),'ticks',String(r.ed).padStart(11),'edges',String(r.w).padStart(11),'work',ms.toFixed(1).padStart(9),'ms');},
  e,h,bank,tm:()=>tm};
 const add0=()=>({n:0,ed:0,w:0,ms:0});const add=(a,b)=>({n:a.n+b.n,ed:a.ed+b.ed,w:a.w+b.w,ms:a.ms+b.ms});
 raw(1);await fn(A);}
const SZ=[9,36];
const SIZEM=['0:242'];
(async()=>{
 await scen('p1000',A=>{A.paste(para(990));A.key(132,1);A.log('type at start of 990 char para',A.key('x'));A.log('type again',A.key('y'));A.log('space',A.key(' '));A.log('backspace',A.key(8));A.log('enter splits',A.key(13));A.log('undo split',A.key('z',1));A.log('arrow left',A.key(128));A.log('arrow down',A.key(131));});
 await scen('p1000doc',A=>{let s='';for(let i=0;i<40;i++)s+=para(990)+'\n';A.paste(s);A.log('wheel',A.wheel(300));A.key(132,1);A.log('jump top',A.key(128));A.log('type at top',A.key('x'));A.log('type 2',A.key('y'));A.log('enter',A.key(13));A.log('bg1',A.tick());A.log('undo',A.key('z',1));A.key(131);A.log('down',A.key(131));A.log('shift down',A.key(131,2));A.log('shift down 2',A.key(131,2));A.log('hover doc',A.move(600,400));A.log('hover 2',A.move(610,400));});
 const sized=(idx)=>A=>{let s='';for(let i=0;i<30;i++)s+=para(300)+'\n';A.paste(s);A.key('a',1);A.ctl('0:242');const r=A.click(210+0,119+idx*22);A.log('apply size to all',r);A.key(132,1);A.key(128);A.log('wheel',A.wheel(100));A.log('type',A.key('x'));A.log('type2',A.key('y'));A.log('backspace',A.key(8));A.log('enter',A.key(13));A.log('undo',A.key('z',1));A.log('select all',A.key('a',1));A.log('arrow off',A.key(128));A.log('shift right',A.key(130,2));A.log('shift right2',A.key(130,2));};
 await scen('small',sized(0));
 await scen('large',sized(8));
 await scen('tracked',A=>{A.ctl('0:233');A.click(252,76);A.ctl('4:233');A.ctl('0:229');let s='';for(let i=0;i<20;i++)s+=para(400)+'\n';A.log('tracked paste',A.paste(s));A.key(132,1);A.log('top',A.key(128));A.log('type',A.key('x'));A.log('type2',A.key('y'));A.log('backspace',A.key(8));A.log('undo',A.key('z',1));});
 await scen('spell',A=>{let s='';for(let i=0;i<40;i++)s+=MISS.repeat(5)+'\n';A.paste(s);A.key(132,1);A.key(128);A.log('type',A.key('x'));A.log('type2',A.key('y'));A.log('wheel',A.wheel(100));A.log('sel all',A.key('a',1));});
 await scen('twocol',A=>{let s='';for(let i=0;i<60;i++)s+=para(400)+'\n';A.paste(s);A.click(192,47);A.log('two columns',A.click(132,76));A.ctl('0:229');A.key(132,1);A.log('top',A.key(128));A.log('type',A.key('x'));A.log('enter',A.key(13));A.log('wheel',A.wheel(200));});
 await scen('tables',A=>{A.click(135,47);for(let i=0;i<8;i++){A.click(116,76);for(let c=0;c<9;c++){A.type('c'+c);A.key(9);}A.key(133,1);A.key(13);A.click(135,47);}A.click(80,47);A.log('wheel',A.wheel(100));A.key(132,1);A.key(128);A.log('type cell',A.key('x'));A.log('type2',A.key('y'));A.log('tab',A.key(9));A.log('enter',A.key(13));A.log('select all',A.key('a',1));A.log('arrow',A.key(128));});
 await scen('pics',A=>{const u=fs.readFileSync('build/p_rgb.png');A.log('picture 1',A.file(10,u));for(let i=0;i<12;i++){A.file(10,u);A.key(13);}A.log('wheel',A.wheel(200));A.log('wheel2',A.wheel(200));A.key(132,1);A.log('top',A.key(128));A.log('type',A.key('x'));A.log('enter',A.key(13));A.log('undo',A.key('z',1));A.log('hover',A.move(500,500));});
 await scen('sel',A=>{let s='';for(let i=0;i<1900;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';A.paste(s.slice(0,390000));
   A.log('type end',A.key('x'));A.log('select all',A.key('a',1));A.log('copy',A.key('c',1));A.log('bold all',A.key('b',1));A.log('undo bold',A.key('z',1));A.key('a',1);A.log('delete all',A.key(127));A.log('undo delete',A.key('z',1));A.log('redo',A.key('y',1));A.log('undo',A.key('z',1));});
 await scen('long',A=>{let s='';for(let i=0;i<1900;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';A.paste(s.slice(0,390000));
   A.key(132,1);A.log('ctrl home',A.key(128));A.log('type top',A.key('x'));A.log('enter top',A.key(13));A.log('type after enter',A.key('y'));let c=0;A.log('bg slice',A.tick());A.log('type during bg',A.key('q'));A.log('bg slice2',A.tick());A.log('hover',A.move(600,400));A.log('hover ribbon',A.move(130,75));A.log('hover ribbon2',A.move(300,100));A.log('hover off',A.move(600,500));A.log('press',A.raw(3,600,400,999999));A.log('drag',A.raw(5,600,420));A.log('drag2',A.raw(5,600,440));A.log('release',A.raw(4,600,440));A.log('wheel',A.wheel(400));A.key(135);A.log('pgdn',A.key(135));A.log('shift down',A.key(131,2));
   A.log('ctrl end',A.key(133,1));A.log('bg all',A.bg());A.log('type end',A.key('z'));
   A.key(132,1);A.key(128);A.key('f',1);for(const ch of 'zzz')A.key(ch);A.log('find absent',A.key(13));A.key(27);A.key('h',1);for(const ch of 'network')A.key(ch);A.key(9);for(const ch of 'graph')A.key(ch);A.log('replace next',A.key(13));A.key(27);});

 const longd=()=>{let s='';for(let i=0;i<1900;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';return s.slice(0,390000);};
 await scen('bulk',A=>{const t=A.paste(longd());A.log('paste',t);A.log('undo paste',A.key('z',1));A.log('redo paste',A.key('y',1));A.key('a',1);A.log('type over all',A.key('x'));A.log('undo',A.key('z',1));A.key('a',1);A.log('cut',A.key('x',1));A.log('undo cut',A.key('z',1));});
 await scen('para',A=>{A.paste(longd());A.key('a',1);A.log('center all',A.key('e',1));A.log('undo',A.key('z',1));A.key('a',1);A.log('heading style',A.ctl('0:223'));A.log('undo',A.key('z',1));A.key('a',1);A.log('bullets',A.ctl('0:215'));A.log('undo',A.key('z',1));});
 await scen('trkbulk',A=>{A.paste(longd());A.click(334,47);A.click(252,76);A.click(80,47);A.key('a',1);A.log('tracked delete all',A.key(127));A.log('undo',A.key('z',1));A.click(334,47);A.click(336,76);A.click(80,47);});
 await scen('files',A=>{A.paste(longd());A.log('save',A.key('s',1));const u=A.savedBytes?null:null;});
})().catch(x=>console.log(x.stack));
