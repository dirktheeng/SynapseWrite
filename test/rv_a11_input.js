// Decisions moved out of the glue: judged by what the page does with real events.
const {chromium}=require('playwright');const url='file://'+require('path').resolve(__dirname,'../build/index.html');
let fails=0;const ok=(n,c,x)=>{if(!c)fails++;console.log(c?'PASS':'FAIL',n,x===undefined?'':x);};
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1280,height:800},acceptDownloads:true});
 const open=async()=>{const p=await ctx.newPage();await p.goto(url);await p.waitForFunction('window.annReady');await p.mouse.click(600,400);return p;};
 const shot=p=>p.screenshot({clip:{x:0,y:174,width:1262,height:600}});
 {const p=await open();const pv=(k,o={})=>p.evaluate(([k,o])=>!window.dispatchEvent(new KeyboardEvent('keydown',{key:k,cancelable:true,...o})),[k,o]);
  for(const k of ['Shift','Control','F5','F12','Help','Dead','Unidentified','CapsLock'])ok(k+' keeps the browser default and does nothing',!(await pv(k)));
  for(const k of ['Backspace','Tab','Enter','Escape','ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home','End','PageUp','PageDown','Delete','a','é'])ok(k+' is taken by the editor',await pv(k));
  ok('Ctrl+V keeps the browser default',!(await pv('v',{ctrlKey:true})));ok('Ctrl+C keeps the browser default',!(await pv('c',{ctrlKey:true})));ok('Cmd+X keeps the browser default',!(await pv('x',{metaKey:true})));ok('Ctrl+B is taken',await pv('b',{ctrlKey:true}));
  await pv('b',{ctrlKey:true});await p.close();}
 {// Help must not act as Home, and a Ctrl letter arrives the same in either case
  const p=await open();await p.keyboard.type('abc');await p.evaluate(()=>window.dispatchEvent(new KeyboardEvent('keydown',{key:'Help',cancelable:true})));await p.keyboard.type('d');await p.mouse.move(1270,5);await p.waitForTimeout(30);const A=await shot(p);
  const q=await open();await q.keyboard.type('abcd');await q.mouse.move(1270,5);await q.waitForTimeout(30);ok('an unknown key name with the shape of a known one does nothing',A.equals(await shot(q)));
  await p.keyboard.type('x');await p.evaluate(()=>window.dispatchEvent(new KeyboardEvent('keydown',{key:'B',ctrlKey:true,cancelable:true})));await p.keyboard.type('y');await q.keyboard.type('x');await q.evaluate(()=>window.dispatchEvent(new KeyboardEvent('keydown',{key:'b',ctrlKey:true,cancelable:true})));await q.keyboard.type('y');let same=false;for(let i=0;i<4&&!same;i++){await p.keyboard.press('End');await q.keyboard.press('End');same=(await shot(p)).equals(await shot(q));}ok('Ctrl with caps lock acts like Ctrl',same);
  await p.close();await q.close();}
 {const p=await open();await p.keyboard.type('save me');const [d]=await Promise.all([p.waitForEvent('download'),p.keyboard.press('Control+s')]);ok('network names the docx',d.suggestedFilename()==='Document1.docx',d.suggestedFilename());
  const [d2]=await Promise.all([p.waitForEvent('download'),p.keyboard.press('Control+p')]);ok('network names the pdf',d2.suggestedFilename()==='Document1.pdf',d2.suggestedFilename());await p.close();}
 {const p=await open();await p.keyboard.type('line');const v=await p.evaluate(()=>document.getElementById('kb').value);ok('field sentinel comes from the network',v==='~~~~~~~~',v);await p.close();}
 await b.close();console.log(fails?'FAILED '+fails:'all passed');process.exit(fails?1:0);})();
