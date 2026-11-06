// Save through the network, reopen through the network, and require an identical image.
// Also reopen after LibreOffice re-saves the file with deflate compression.
const d=require('./drive');const fs=require('fs');const {execSync}=require('child_process');const crypto=require('crypto');
const h=b=>crypto.createHash('md5').update(b).digest('hex');
const shot=async p=>{await p.mouse.move(1270,5);return await p.screenshot({clip:{x:0,y:174,width:1280,height:626}});};
(async()=>{const res=[];const {b,p}=await d();await p.evaluate(()=>{window.annMax=8000000});
 const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t);
 await T('Round trip & <check>');await p.mouse.click(660,88);await K('End');await K('Enter');await p.mouse.click(485,88);
 await T('Plain ');await K('Control+b');await T('bold');await K('Control+b');await T(' ');await K('Control+i');await T('italic');await K('Control+i');await T(' ');await K('Control+u');await T('under');await K('Control+u');await K('Enter');
 await T('Centered');await K('Control+e');await K('Enter');await K('Control+l');await T('Right');await K('Control+r');await K('Enter');await K('Control+l');
 await T('Serif text');await K('Shift+Home');await p.mouse.click(149,75);await K('End');await K('Enter');
 await T('Red');await K('Shift+Home');await p.mouse.click(239,102);await K('End');
 await p.waitForTimeout(50);await K('End');const a=await shot(p);fs.writeFileSync('build/rt_a.png',a);
 const [dl]=await Promise.all([p.waitForEvent('download'),K('Control+s')]);await dl.saveAs('build/rt.docx');
 const open=async f=>{await p.evaluate(u=>annOpen(new Blob([new Uint8Array(u)])),[...fs.readFileSync(f)]);await p.waitForTimeout(600);return await p.evaluate('annStats.k9');};
 const ms=await open('build/rt.docx');await K('Control+End');const c=await shot(p);fs.writeFileSync('build/rt_c.png',c);res.push(['save then open is pixel identical',h(a)===h(c),ms]);
 execSync('rm -rf build/rtlo; timeout 120 soffice --headless --convert-to docx:"MS Word 2007 XML" --outdir build/rtlo build/rt.docx >/dev/null 2>&1');
 const ms2=await open('build/rtlo/rt.docx');await K('Control+End');const e=await shot(p);fs.writeFileSync('build/rt_e.png',e);res.push(['open after LibreOffice deflate is pixel identical',h(a)===h(e),ms2]);
 const [dl2]=await Promise.all([p.waitForEvent('download'),K('Control+s')]);await dl2.saveAs('build/rt2.docx');
 const x=f=>execSync(`python3 -c "import zipfile,sys;print(zipfile.ZipFile('${f}').read('word/document.xml').decode())"`).toString();
 res.push(['second save equals first save, XML',x('build/rt.docx')===x('build/rt2.docx')]);
 console.log(res);fs.writeFileSync('build/roundtrip.json',JSON.stringify(res));await b.close();})();
