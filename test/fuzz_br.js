// The same seeded traces through the real page in Chromium: real keyboard and mouse, the real glue. Page errors and
// tick cap hits are crashes. Without undo the saved XML must match the Node world run of the same trace, which ties the harness to the page.
// node test/fuzz_br.js FROM TO STEPS [browser]
const fs=require('fs'),path=require('path');const pw=require('playwright');const {gen}=require('./fuzz.js');const F=require('./fuzz.js');const {World,NAMED,unzip,R}=require('./fuzz_lib');
const NM={};for(const k in NAMED)NM[NAMED[k]]=k.replace(/^(Left|Up|Right|Down)$/,'Arrow$1');
const keyName=(c,m)=>{let n=NM[c]||(c>=32&&c<127?String.fromCharCode(c):null);if(!n)return null;if(m&1)n='Control+'+n;if(m&2&&!(c>=65&&c<=90))n='Shift+'+n;return n;};
const safe=A=>A.filter(a=>!(a[0]=='k'&&(a[2]&1)&&(a[1]==118||a[1]==99||a[1]==120||a[1]==111||a[1]==112))&&a[0]!='T'&&a[0]!='K'&&!(a[0]=='k'&&!keyName(a[1],a[2]))&&a[0]!='i');
(async()=>{const [from,to,steps]=[+process.argv[2],+process.argv[3],+process.argv[4]||60];const bn=process.argv[5]||'chromium';let crash=0,diff=0,tot=0;
 const b=await pw[bn].launch();
 for(let s=from;s<to;s++){const A=safe(gen(s,steps,'edit')).filter(a=>a[0]!='o'&&!(a[0]=='k'&&(a[2]&1)&&(a[1]==122||a[1]==121)));
  const c=await b.newContext({viewport:{width:1280,height:800},acceptDownloads:true});const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+R('build/index.html'));await p.waitForFunction('window.annReady',{timeout:120000});await p.evaluate(()=>{window.annMax=20000000});
  let hang=0;const chk=async()=>{const t=await p.evaluate('annStats.ticks');if(t>=20000000)hang++;};
  for(const a of A){switch(a[0]){
   case 't':await p.keyboard.type(a[1]);break;
   case 'k':await p.keyboard.press(keyName(a[1],a[2]));break;
   case 'c':await p.mouse.click(a[1],a[2]);break;
   case 'g':await p.mouse.move(a[1],a[2]);await p.mouse.down();await p.mouse.move(a[3],a[4]);await p.waitForTimeout(30);await p.mouse.up();break;
   case 'w':await p.mouse.wheel(0,a[1]);await p.waitForTimeout(10);break;
   case 'p':await p.evaluate(t=>annPaste(t),a[1]);break;
   case 's':{const [d]=await Promise.all([p.waitForEvent('download',{timeout:60000}),p.keyboard.press('Control+s')]);break;}
   case 'h':await p.mouse.move(a[1],a[2]);break;}
   await chk();}
  const [dl]=await Promise.all([p.waitForEvent('download',{timeout:60000}),p.keyboard.press('Control+s')]);const f=R(`build/fz_br_${s}.docx`);await dl.saveAs(f);let x=null;try{x=unzip(fs.readFileSync(f))['word/document.xml'].toString();}catch(e){errs.push('zip '+e.message);}
  await c.close();
  tot++;const nerr=errs.length+hang;if(nerr)crash++;console.log(nerr?'CRASH':'ok',bn,s,'actions',A.length,errs.slice(0,2).join(';').slice(0,200),hang?'HANG':'');}
 await b.close();console.log('browser',bn,'runs',tot,'crashing',crash);process.exit(crash?1:0);})();
