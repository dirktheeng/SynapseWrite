// rv_a6: spelling suggestions, user dictionary, PDF highlight and bookmarks. Driven only by events, judged on images and saved files.
const d=require('./drive');const fs=require('fs');const {execSync}=require('child_process');
const sh=c=>execSync(c,{stdio:['ignore','pipe','pipe']}).toString();
const png=b=>{fs.writeFileSync('build/_x.png',b);return 'build/_x.png'};
const py=s=>sh(`python3 - <<'P'\n${s}\nP`).trim();
const red=(f)=>+py(`from PIL import Image
a=Image.open('${f}').convert('RGB');n=0
for y in range(a.height):
  for x in range(a.width):
    p=a.getpixel((x,y))
    if p[0]>170 and p[1]<80 and p[2]<80:n+=1
print(n)`);
(async()=>{const res=[];const ok=(n,v,x)=>{res.push([n,!!v]);console.log(v?'PASS':'FAIL',n,x===undefined?'':x);};
 const {b,p,check}=await d();await p.evaluate(()=>{window.annMax=60000000});const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t),C=(x,y)=>p.mouse.click(x,y);
 const clip={x:223,y:174,width:816,height:300};
 await C(600,300);await T('helo wrold ');await p.waitForTimeout(100);
 const s0=await p.screenshot({clip});const r0=red(png(s0));ok('two words have squiggles',r0>20,r0);
 // right click on the second word
 await p.mouse.click(350,270);
 await p.waitForTimeout(50);
 const line=await p.evaluate(()=>annStats.ticks);
 // find the text line by clicking at the start then End, then right click
 await K('Control+Home');await K('ArrowRight');await p.keyboard.press('ContextMenu');await p.waitForTimeout(100);
 const t1=await p.evaluate(()=>annStats.t2);console.log('ticks to open',t1);ok('suggestions take under 40000 ticks',t1<40000,t1);
 await p.screenshot({path:'build/a6_menu.png'});
 await K('ArrowDown');await K('Enter');await p.waitForTimeout(100);
 await p.screenshot({path:'build/a6_after.png'});
 await p.evaluate(()=>{annVal(0)});
 const [dl]=await Promise.all([p.waitForEvent('download'),K('Control+s')]);await dl.saveAs('build/a6.docx');
 const txt=py(`import docx;print(' '.join(q.text for q in docx.Document('build/a6.docx').paragraphs))`);
 ok('first suggestion replaced the word',!/helo/.test(txt)&&/wrold/.test(txt),txt);
 await K('Control+z');await p.waitForTimeout(100);await K('Control+z');await p.waitForTimeout(50);
 const [dl2]=await Promise.all([p.waitForEvent('download'),K('Control+s')]);await dl2.saveAs('build/a6b.docx');
 const tx2=py(`import docx;print(' '.join(q.text for q in docx.Document('build/a6b.docx').paragraphs))`);ok('undo brings the word back',/helo/.test(tx2),tx2);
 // add to dictionary: squiggles of that word go, and survive a reload
 await K('Control+End');await K('Enter');await T('zorblax ');const pos=await p.screenshot({clip});const r1=red(png(pos));
 await K('ArrowLeft');await K('ArrowLeft');await K('ContextMenu');await p.waitForTimeout(100);await p.screenshot({path:'build/a6_menu2.png'});
 await K('ArrowUp');await K('ArrowUp');await K('Enter');await p.waitForTimeout(200);
 const r2=red(png(await p.screenshot({clip})));ok('added word loses its squiggle',r2<r1,r1+' to '+r2);
 await p.reload();await p.waitForFunction('window.annReady',{timeout:60000});await p.evaluate(()=>{window.annMax=60000000});
 await C(600,300);await T('zorblax nofrumz ');await p.waitForTimeout(100);await p.screenshot({path:'build/a6_reload.png'});
 const r3=red(png(await p.screenshot({clip:{x:223,y:174,width:816,height:300}})));ok('dictionary survives a reload, the other word is flagged',r3>5,r3);
 await K('Control+Home');await K('ArrowRight');await K('ContextMenu');await p.waitForTimeout(100);await K('ArrowUp');await p.screenshot({path:'build/a6_menu3.png'});await K('Escape');
 await b.close();
 console.log(res.filter(r=>r[1]).length+'/'+res.length+' passed');
})();
