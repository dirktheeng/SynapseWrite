// rv_a6: equations as OMML in saved files; math read from a foreign file. LibreOffice stands in for a reader, it is not Word.
const dr=require('./drive');const fs=require('fs');const {execSync}=require('child_process');
const sh=c=>execSync(c,{stdio:['ignore','pipe','pipe']}).toString();const crypto=require('crypto');
(async()=>{const res=[];const ok=(n,v,x)=>{res.push([n,!!v]);console.log(v?'PASS':'FAIL',n,x===undefined?'':x);};
 let A=await dr();await A.p.evaluate(()=>{window.annMax=60000000});
 const K=k=>A.p.keyboard.press(k),T=t=>A.p.keyboard.type(t),C=(x,y)=>A.p.mouse.click(x,y),W=ms=>A.p.waitForTimeout(ms);
 const save=async f=>{const [d]=await Promise.all([A.p.waitForEvent('download',{timeout:240000}),K('Control+s')]);await d.saveAs(f);return sh(`unzip -p ${f} word/document.xml`);};
 const open=async f=>{await A.p.evaluate(async u=>{await annOpen(new Blob([new Uint8Array(u)]))},[...fs.readFileSync(f)]);await W(300);};
 const clip={x:223,y:190,width:816,height:300};let hn=0;const hash=async()=>{const f='build/a6h'+(hn++)+'.png';await A.p.screenshot({clip,path:f});return f;};
 const same=(a,b)=>{const r=sh(`python3 -c "from PIL import Image,ImageChops;b=ImageChops.difference(Image.open('${a}').convert('RGB'),Image.open('${b}').convert('RGB')).getbbox();print(0 if not b else b[2]-b[0])"`).trim();return +r<=2;};// a caret blink is one column
 await T('Before ');await K('Enter');await T('E=mc^2 and x_1');await C(135,47);await C(725,76);await C(80,47);await K('Enter');await T('after');await K('Control+Home');await W(100);
 const h0=await hash();await A.p.screenshot({path:'build/a6e1.png'});const x=await save('build/a6e.docx');
 ok('equation saved as m:oMath with m:sSup and m:sSub',/<m:oMath>/.test(x)&&/<m:sSup><m:e>.*<m:t[^>]*>c<\/m:t>.*<\/m:e><m:sup>.*<m:t[^>]*>2<\/m:t>.*<\/m:sup><\/m:sSup>/.test(x)&&/<m:sSub>/.test(x),x.slice(x.indexOf('<m:oMath>'),x.indexOf('<m:oMath>')+200));
 ok('xml parses, math namespace declared',/xmlns:m=/.test(x)&&sh(`python3 -c "import docx;d=docx.Document('build/a6e.docx');print(len(d.paragraphs))"`).trim()==='3');
 await open('build/a6e.docx');await W(100);const h1=await hash();await A.p.screenshot({path:'build/a6e2.png'});ok('save and open is pixel identical',same(h0,h1));
 // libreoffice-math is not installed here, so LibreOffice cannot show math; the element order is checked against the OMML schema by hand instead.
 ok('m:r holds w:rPr then m:t, and the paragraph holds the m:oMath',/<w:p>(?:(?!<\/w:p>).)*<m:oMath><m:r><w:rPr>(?:(?!<\/w:rPr>).)*<\/w:rPr><m:t /.test(x));
 sh(`python3 - <<'P'
import docx
from docx.oxml import parse_xml
ns='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"'
d=docx.Document();p=d.add_paragraph('Let ')
p._p.append(parse_xml('<m:oMath %s><m:f><m:num><m:r><m:t>a+b</m:t></m:r></m:num><m:den><m:r><m:t>c</m:t></m:r></m:den></m:f><m:r><m:t>=</m:t></m:r><m:rad><m:deg/><m:e><m:r><m:t>x</m:t></m:r></m:e></m:rad><m:sSup><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup></m:oMath>'%ns))
p.add_run(' done')
d.save('build/a6f3.docx')
P`);
 await open('build/a6f3.docx');await W(100);await A.p.screenshot({path:'build/a6e3.png'});const y=await save('build/a6f4.docx');
 const tx=(y.match(/<(?:m|w):t[ >][^<]*<|<(?:m|w):t>[^<]*</g)||[]).map(s=>s.replace(/<[^>]*>/,'').replace('<','')).join('');
 ok('foreign math keeps its structure: fraction, root, superscript',/<m:f><m:num>.*>a\+b<.*<m:den>.*>c<.*<\/m:f>/.test(y)&&/<m:rad>.*>x<.*<\/m:rad>/.test(y)&&/<m:sSup><m:e>.*>y<.*<m:sup>.*>2</.test(y)&&tx.includes('Let ')&&tx.includes(' done'),tx);
 // built up fraction and root
 await A.b.close();A=await dr();await A.p.evaluate(()=>{window.annMax=60000000});
 await T('Solve x=(a+b)/(c-1) and sqrt(y+2) now');await C(135,47);await C(725,76);await C(80,47);await K('Control+End');await K('Enter');await T('next line');await K('Control+Home');await W(100);
 const h2=await hash();await A.p.screenshot({path:'build/a6e4.png'});const z=await save('build/a6e5.docx');
 ok('fraction and root saved as m:f and m:rad',/<m:f><m:num>.*>a\+b<\/m:t>.*<m:den>.*>c-1<\/m:t>.*<\/m:f>/.test(z)&&/<m:rad>.*>y\+2<\/m:t>.*<\/m:rad>/.test(z),z.slice(z.indexOf('<m:f>'),z.indexOf('<m:f>')+150));
 await open('build/a6e5.docx');await W(100);const h3=await hash();await A.p.screenshot({path:'build/a6e6.png'});ok('built up forms reopen pixel identical',same(h2,h3));
 const [dp]=await Promise.all([A.p.waitForEvent('download',{timeout:240000}),K('Control+p')]);await dp.saveAs('build/a6e.pdf');let qc;try{qc=sh('qpdf --check build/a6e.pdf 2>&1');}catch(e){qc=e.stdout.toString();}ok('PDF with built up forms is clean',/No syntax/.test(qc)&&!/WARNING/.test(qc));
 ok('PDF has the texts',/a\+b/.test(sh('pdftotext build/a6e.pdf -'))&&/y\+2/.test(sh('pdftotext build/a6e.pdf -')));
 await K('Control+Home');await K('End');
 await A.b.close();console.log(res.filter(r=>r[1]).length+'/'+res.length+' passed');
})();
