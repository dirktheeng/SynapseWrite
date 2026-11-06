// Phone emulation: tap to summon the field, type through it, and compare against desktop typing.
const {chromium,devices}=require('playwright');const crypto=require('crypto');const fs=require('fs');const url='file://'+require('path').resolve(__dirname,'../build/index.html');
(async()=>{const b=await chromium.launch();
 const c=await b.newContext({...devices['Pixel 7'],viewport:{width:1280,height:800}});const p=await c.newPage();p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto(url);await p.waitForFunction('window.annReady');
 await p.touchscreen.tap(600,400);await p.waitForTimeout(100);
 console.log('field focused',await p.evaluate(()=>document.activeElement.id==='kb'));
 await p.keyboard.insertText('hellx');await p.evaluate(()=>{const t=document.getElementById('kb');t.value='~~~~~~~';t.dispatchEvent(new Event('input'));});await p.keyboard.insertText('o\nworld');
 // composition style: the field grows and is rewritten before compositionend
 await p.evaluate(()=>{const t=document.getElementById('kb');t.dispatchEvent(new Event('compositionstart'));t.value='~~~~~~~~ a';t.dispatchEvent(new Event('input'));t.value='~~~~~~~~ ab';t.dispatchEvent(new Event('input'));t.value='~~~~~~~~ ac';t.dispatchEvent(new Event('input'));t.dispatchEvent(new Event('compositionend'));});
 await p.waitForTimeout(50);await p.keyboard.press('End');const A=await p.screenshot({clip:{x:0,y:174,width:1262,height:600}});fs.writeFileSync('build/touch.png',await p.screenshot());
 const q=await b.newPage({viewport:{width:1280,height:800},deviceScaleFactor:devices['Pixel 7'].deviceScaleFactor});await q.goto(url);await q.waitForFunction('window.annReady');await q.mouse.click(600,400);await q.keyboard.type('hello');await q.keyboard.press('Enter');await q.keyboard.type('world ac');await q.keyboard.press('End');const B=await q.screenshot({clip:{x:0,y:174,width:1262,height:600}});
 const h=x=>crypto.createHash('md5').update(x).digest('hex');console.log('same as desktop typing',h(A)===h(B));
 await p.evaluate(()=>{let s='';for(let i=0;i<60;i++)s+='line\n';annPaste(s)});
 const before=await p.screenshot();
 const cd=await c.newCDPSession(p);await cd.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:600,y:300}]});await cd.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:600,y:500}]});await p.waitForTimeout(100);await cd.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await p.waitForTimeout(100);
 console.log('drag scrolls',h(before)!==h(await p.screenshot()));await b.close();})();
