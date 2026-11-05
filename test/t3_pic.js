const d=require('./drive');const fs=require('fs');const crypto=require('crypto');const H=b=>crypto.createHash('md5').update(b).digest('hex');const {execSync}=require('child_process');
const res=[];const ok=(n,c)=>{res.push([n,!!c]);console.log(c?'PASS':'FAIL',n);};
(async()=>{const {b,p,check}=await d();const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t);
 const pic=async f=>{await p.evaluate(u=>annPic(new Blob([new Uint8Array(u)])),[...fs.readFileSync(f)]);await p.waitForTimeout(1500);await check('pic');};
 const sh=async n=>{await p.mouse.move(1270,5);await p.waitForTimeout(30);const b_=await p.screenshot({clip:{x:0,y:174,width:1262,height:600}});if(n)fs.writeFileSync('build/'+n+'.png',b_);return b_;};
 await T('Pic');await K('Enter');await pic('build/p_a.png');await T('after');const a=await sh('pc0');
 const {PNG}=(()=>{try{return require('pngjs')}catch(e){return {}}})();
 // click the picture: handles appear
 await p.mouse.click(420,174+100+30);const h=await sh('pc1');ok('handles appear when picture clicked',H(a)!==H(h));
 // alpha: read pixels by python
 // corner drag
 const bx=319+200,by=174+96+24+120;  // lower right
 await p.mouse.move(bx-2,by);await p.mouse.down();await p.mouse.move(bx+98,by+40);await p.waitForTimeout(80);await p.mouse.up();await p.waitForTimeout(300);await check('resize');
 const r=await sh('pc2');ok('corner drag resizes',H(r)!==H(h));
 await K('Control+z');await p.waitForTimeout(100);const u=await sh('pc3');
 await K('Control+y');await p.waitForTimeout(100);const y=await sh('pc4');
 await K('ArrowDown');await K('End');const a2=await sh('pc5');
 const save=async f=>{const [dl]=await Promise.all([p.waitForEvent('download'),K('Control+s')]);await dl.saveAs(f);await check('save');};
 const open=async f=>{await p.evaluate(u=>annOpen(new Blob([new Uint8Array(u)])),[...fs.readFileSync(f)]);await p.waitForTimeout(2000);await check('open');};
 await save('build/pc.docx');await open('build/pc.docx');await K('ArrowDown');await K('ArrowDown');await K('End');await p.waitForTimeout(100);const a3=await sh('pc6');ok('picture docx save then open identical',H(a2)===H(a3));
 execSync('rm -rf build/pclo; timeout 120 soffice --headless --convert-to docx:"MS Word 2007 XML" --outdir build/pclo build/pc.docx >/dev/null 2>&1');
 await open('build/pclo/pc.docx');await K('ArrowDown');await K('ArrowDown');await K('End');await p.waitForTimeout(100);const a4=await sh('pc7');ok('picture open after LibreOffice identical',H(a2)===H(a4));
 console.log(JSON.stringify(res));await b.close();})();
