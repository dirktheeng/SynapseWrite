// Ordinary Caladea text marked Ignore (no proof) stays ordinary text in a saved file; an equation still saves as math. Driven by events, judged on the saved file.
const d=require('./drive');const fs=require('fs');const {execSync}=require('child_process');
const sh=c=>execSync(c,{stdio:['ignore','pipe','pipe']}).toString();
(async()=>{const res=[];const ok=(n,v,x)=>{res.push([n,!!v]);console.log(v?'PASS':'FAIL',n,x===undefined?'':x);};
 const {b,p}=await d();await p.evaluate(()=>{window.annMax=60000000});const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t),C=(x,y)=>p.mouse.click(x,y),W=ms=>p.waitForTimeout(ms);
 const save=async f=>{const [dl]=await Promise.all([p.waitForEvent('download',{timeout:240000}),K('Control+s')]);await dl.saveAs(f);return sh(`unzip -p ${f} word/document.xml`);};
 const open=async f=>{await p.evaluate(async u=>{await annOpen(new Blob([new Uint8Array(u)]))},[...fs.readFileSync(f)]);await W(300);};
 await C(182,75);await C(150,120);await T('zorblax ');await K('ArrowLeft');await K('ArrowLeft');await K('ContextMenu');await W(100);await K('ArrowUp');await K('Enter');await W(200);
 await K('Control+End');await K('Enter');await T('qux');
 const x=await save('build/mm1.docx');
 ok('Ignore on a Caladea word saves as no proof',/<w:rFonts[^>]*Caladea[^>]*\/><w:noProof\/>|<w:noProof\/>[^>]*<w:rFonts[^>]*Caladea/.test(x),x.slice(x.indexOf('<w:body>'),x.indexOf('<w:body>')+300));
 ok('the word stays an ordinary run',/<w:t[^>]*>[^<]*zorblax/.test(x));
 ok('no math in the file',!/m:oMath|<m:t/.test(x));
 await open('build/mm1.docx');const y=await save('build/mm2.docx');
 ok('after reopen it is still ordinary text with no proof',!/m:oMath/.test(y)&&/<w:noProof\/>/.test(y)&&/<w:t[^>]*>[^<]*zorblax/.test(y));
 // the Equation command still makes math in the same font
 await K('Control+End');await K('Enter');await T('E=mc^2');await C(135,47);await C(725,76);await C(80,47);await W(100);
 const z=await save('build/mm3.docx');
 ok('an equation still saves as math beside it',/<m:oMath>/.test(z)&&/<m:sSup>/.test(z)&&/<w:t[^>]*>[^<]*zorblax/.test(z));
 await open('build/mm3.docx');const v=await save('build/mm4.docx');
 ok('and reads back as math, with the word still ordinary',/<m:oMath>/.test(v)&&/<m:sSup>/.test(v)&&/<w:t[^>]*>[^<]*zorblax/.test(v));
 await b.close();console.log(res.filter(r=>r[1]).length+'/'+res.length+' passed');
})();
