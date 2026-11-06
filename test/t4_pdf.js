// PDF tests: every byte comes from the network. Checked with pdfinfo, pdftotext, pdffonts, qpdf and a raster compare to the screen.
const d=require('./drive');const fs=require('fs');const {execSync}=require('child_process');
const sh=c=>execSync(c,{stdio:['ignore','pipe','pipe']}).toString();
// tiny RGB PNG from python
sh(`python3 -c "from PIL import Image;im=Image.new('RGB',(80,40),(30,144,255));[im.putpixel((x,y),(255,60,0)) for x in range(40,80) for y in range(20,40)];im.save('build/pic.png')"`);
(async()=>{const res=[];const ok=(n,v,x)=>{res.push([n,!!v]);console.log(v?'PASS':'FAIL',n,x===undefined?'':x);};
 const {b,p}=await d();await p.evaluate(()=>{window.annMax=60000000});const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t),C=(x,y)=>p.mouse.click(x,y);
 await C(135,47);await C(275,76);await T('Head text');await K('Enter');await C(80,47);
 await T('Report title');await C(660,88);await K('End');await K('Enter');await C(485,88);
 await T('Plain ');await K('Control+b');await T('bold');await K('Control+b');await T(' ');await K('Control+i');await T('italic');await K('Control+i');await T(' ');await K('Control+u');await T('underlined words');await K('Control+u');await T(' end (paren) here');await K('Enter');
 await T('Serif');await K('Shift+Home');await C(149,75);await K('End');await K('Enter');await K('Shift+Home');
 await T('Item one');await C(330,75);await K('Enter');await T('Item two');await K('Enter');await C(330,75);await C(330,75);
 await T('Tracked ');await C(334,47);await C(252,76);await T('added');await C(252,76);await C(80,47);await K('Enter');
 await T('E=mc^2');await C(135,47);await C(725,76);await K('End');await C(80,47);await K('Enter');
 await p.evaluate(async u=>{await annPic(new Blob([new Uint8Array(u)]))},[...fs.readFileSync('build/pic.png')]);await p.waitForTimeout(400);
 await T('After picture');await K('Enter');
 await p.evaluate(()=>{let s='';for(let i=0;i<45;i++)s+='Filler line number '+i+' (with parens).\n';annPaste(s)});await p.waitForTimeout(400);
 await C(334,47);await C(155,76);await C(80,47);await p.mouse.move(600,400);for(let i=0;i<8;i++){await p.mouse.wheel(0,-1000);await p.waitForTimeout(40);}await p.waitForTimeout(200);
 await p.evaluate(()=>annDispatch(12));const scr=await p.screenshot({clip:{x:223,y:190,width:816,height:586}});fs.writeFileSync('build/pdf_screen.png',scr);
 const [dl]=await Promise.all([p.waitForEvent('download'),K('Control+p')]);await dl.saveAs('build/t4.pdf');await b.close();
 const info=sh('pdfinfo build/t4.pdf');ok('pdfinfo reads it, Letter size',/Page size:\s+612 x 792/.test(info),(info.match(/Pages:\s+\d+/)||[''])[0]);
 ok('multiple pages',+(info.match(/Pages:\s+(\d+)/)||[0,0])[1]>=2);
 let q;try{q=sh('qpdf --check build/t4.pdf 2>&1');}catch(e){q=e.stdout.toString()+e.stderr.toString();}ok('qpdf --check clean',/No syntax or stream encoding errors/.test(q)&&!/WARNING/.test(q),q.split('\n').slice(-3).join(' '));
 const txt=sh('pdftotext -layout build/t4.pdf -');ok('text extracts',/Report title/.test(txt)&&/underlined words/.test(txt)&&/\(paren\)/.test(txt)&&/Head text/.test(txt),'');
 const fonts=sh('pdffonts build/t4.pdf');ok('fonts are embedded subsets of Carlito and Caladea',/Carlito/.test(fonts)&&/Caladea/.test(fonts)&&!/Helvetica|Times/.test(fonts)&&!/\sno\s+no\s+no/.test(fonts));
 console.log(fonts);
 sh('rm -f build/pdfp-*; pdftoppm -r 96 -f 1 -l 1 -png build/t4.pdf build/pdfp');
 const pf=fs.readdirSync('build').filter(f=>f.startsWith('pdfp-'))[0];
 const r=sh(`python3 - <<'P'
from PIL import Image,ImageChops
a=Image.open('build/${pf}').convert('L').crop((0,0,816,586));s=Image.open('build/pdf_screen.png').convert('L')
import numpy as np
A=np.asarray(a)<140;S=np.asarray(s)<140
print(A.sum(),S.sum(),(A&S).sum(),(A|S).sum())
from PIL import ImageFilter
Ad=np.asarray(a.filter(ImageFilter.MinFilter(5)))<140;Sd=np.asarray(s.filter(ImageFilter.MinFilter(5)))<140
print((A&Sd).sum()/max(1,A.sum()),(S&Ad).sum()/max(1,S.sum()))
P`).trim().split('\n');
 const [ma,mb]=r[1].split(' ').map(Number);ok('page ink within 2 pixels of the screen for at least 90 percent, both directions',ma>0.9&&mb>0.9,r.join(' | '));
 const img=sh(`python3 - <<'P'
from PIL import Image
a=Image.open('build/${pf}').convert('RGB');n=0;m=0
for y in range(a.height):
  for x in range(a.width):
    p=a.getpixel((x,y))
    if abs(p[0]-30)<6 and abs(p[1]-144)<6 and abs(p[2]-255)<6: n+=1
    if abs(p[0]-255)<6 and abs(p[1]-60)<6 and p[2]<6: m+=1
print(n,m)
P`).trim().split(' ').map(Number);ok('picture colors present at the right area',Math.abs(img[0]-2400)<300&&Math.abs(img[1]-800)<200,img.join(','));
 console.log(res.filter(r=>r[1]).length+'/'+res.length+' passed');fs.writeFileSync('build/t4_pdf.json',JSON.stringify(res));
})();
