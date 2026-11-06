// rv_a6: tracked paragraph marks, author and date, live fields, merge fields. Driven by events, judged on saved files.
const dr=require('./drive');const fs=require('fs');const {execSync}=require('child_process');
const sh=c=>execSync(c,{stdio:['ignore','pipe','pipe']}).toString();
const xml=f=>sh(`unzip -p ${f} word/document.xml`);
const paras=f=>sh(`python3 -c "import docx;print('|'.join(p.text for p in docx.Document('${f}').paragraphs))"`).trim();
(async()=>{const res=[];const ok=(n,v,x)=>{res.push([n,!!v]);console.log(v?'PASS':'FAIL',n,x===undefined?'':x);};
 let A=await dr();
 const fresh=async()=>{await A.b.close();A=await dr();await A.p.evaluate(()=>{window.annMax=60000000});};
 const K=k=>A.p.keyboard.press(k),T=t=>A.p.keyboard.type(t),C=(x,y)=>A.p.mouse.click(x,y),W=ms=>A.p.waitForTimeout(ms);
 const save=async f=>{const [d]=await Promise.all([A.p.waitForEvent('download',{timeout:120000}),K('Control+s')]);await d.saveAs(f);return xml(f);};
 const open=async f=>{await A.p.evaluate(async u=>{await annOpen(new Blob([new Uint8Array(u)]))},[...fs.readFileSync(f)]);await W(300);};
 const REV=async()=>{await C(334,47)};const HOME=async()=>{await C(80,47)};
 const TRK=async()=>{await REV();await C(252,76);await HOME()};const ACC=async()=>{await REV();await C(336,76);await HOME()};const REJ=async()=>{await REV();await C(400,76);await HOME()};
 await fresh();
 await TRK();await T('one');await K('Enter');await T('two');await TRK();let x=await save('build/a6t1.docx');
 const today=new Date();const ymd=`${today.getFullYear()}-${String(today.getMonth()+1).padStart(2,'0')}-${String(today.getDate()).padStart(2,'0')}`;
 ok('Enter while tracking saves an inserted paragraph mark',/<w:pPr>.*<w:rPr><w:ins w:id="\d+" w:author="SynapseWrite" w:date="[^"]+"\/><\/w:rPr>.*<\/w:pPr>/.test(x),x.slice(0,300));
 ok('run revisions carry today as date',x.includes(`w:date="${ymd}T00:00:00Z"`),ymd);
 await A.p.screenshot({path:'build/a6t_mark.png'});
 await open('build/a6t1.docx');x=await save('build/a6t1b.docx');ok('mark survives reopen',/<w:rPr><w:ins /.test(x));
 await REJ();x=await save('build/a6t1c.docx');ok('reject all removes inserted text and joins the paragraphs',paras('build/a6t1c.docx')==='',JSON.stringify(paras('build/a6t1c.docx')));
 await K('Control+z');await W(100);x=await save('build/a6t1d.docx');ok('undo of reject brings both paragraphs back',/one/.test(x)&&/two/.test(x)&&(x.match(/<w:p>/g)||[]).length===2&&/<w:rPr><w:ins /.test(x));
 await fresh();
 await T('aa');await K('Enter');await T('bb');await K('Control+Home');await K('End');await TRK();await K('Delete');await TRK();
 x=await save('build/a6t2.docx');ok('Delete at paragraph end marks it deleted',/<w:rPr><w:del w:id/.test(x)&&paras('build/a6t2.docx')==='aa|bb',paras('build/a6t2.docx'));
 await ACC();await save('build/a6t2b.docx');ok('accept joins them',paras('build/a6t2b.docx')==='aabb',paras('build/a6t2b.docx'));
 await K('Control+z');await W(100);x=await save('build/a6t2c.docx');ok('undo restores the mark and the split',paras('build/a6t2c.docx')==='aa|bb'&&/<w:rPr><w:del w:id/.test(x),paras('build/a6t2c.docx'));
 await REJ();x=await save('build/a6t2d.docx');ok('reject clears the mark and keeps both',paras('build/a6t2d.docx')==='aa|bb'&&!/<w:rPr><w:del /.test(x));
 await K('Control+End');await K('Home');await TRK();await K('Backspace');await TRK();x=await save('build/a6t2e.docx');ok('Backspace at paragraph start marks the previous one',/<w:rPr><w:del w:id/.test(x));
 // a foreign file: author and date stay
 sh(`python3 - <<'P'
import docx
d=docx.Document();p=d.add_paragraph();d.add_paragraph('after')
from docx.oxml import parse_xml
ns='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
p._p.append(parse_xml('<w:ins %s w:id="9" w:author="Jane Roe" w:date="2020-03-04T10:00:00Z"><w:r><w:t>hers</w:t></w:r></w:ins>'%ns))
q=d.add_paragraph();q._p.append(parse_xml('<w:ins %s w:id="10" w:author="Bob Poe" w:date="2024-12-31T10:00:00Z"><w:r><w:t>his</w:t></w:r></w:ins>'%ns))
d.save('build/a6t3.docx')
P`);
 await open('build/a6t3.docx');x=await save('build/a6t3b.docx');
 ok('authors and dates from a file are kept',/w:author="Jane Roe" w:date="2020-03-04T/.test(x)&&/w:author="Bob Poe" w:date="2024-12-31T/.test(x),(x.match(/w:author="[^"]+" w:date="[^"]+"/g)||[]).join(';'));
 sh('cd build && rm -rf a6lo && mkdir a6lo && timeout -s KILL 120 soffice --headless --convert-to pdf --outdir a6lo a6t1.docx >/dev/null 2>&1 || true');ok('LibreOffice (not Word) opens the tracked file',fs.existsSync('build/a6lo/a6t1.pdf'));
 // live fields
 await fresh();
 await T('alpha beta ');await C(135,47);await C(560,76);await C(80,47);await W(800);await T(' gamma delta epsilon');await W(1600);
 x=await save('build/a6f.docx');const wc=(x.match(/NUMWORDS[^>]*>.*?<w:t[^>]*>(\d+)/)||[])[1];ok('word count field follows typing after a pause',+wc>=5&&+wc<=6,wc||x.slice(x.indexOf('<w:body'),x.indexOf('<w:body')+500));
 await K('Control+z');await W(50);
 await fresh();
 await C(135,47);await C(430,76);await C(80,47);await W(800);await K('Control+Home');for(let i=0;i<1;i++){await K('Control+Enter');}await W(1600);
 x=await save('build/a6f2.docx');const pg=(x.match(/ PAGE [^>]*>.*?<w:t[^>]*>(\d+)/)||[])[1];ok('page field follows a page break after a pause',pg==='2',pg);
 // merge fields
 sh(`python3 - <<'P'
import docx
d=docx.Document();p=d.add_paragraph('Dear ')
from docx.oxml import parse_xml
ns='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
p._p.append(parse_xml('<w:fldSimple %s w:instr=" MERGEFIELD Name \\\\* MERGEFORMAT "><w:r><w:t>\\u00abName\\u00bb</w:t></w:r></w:fldSimple>'%ns))
r=p.add_run(' of ')
p._p.append(parse_xml('<w:fldSimple %s w:instr=" MERGEFIELD City "><w:r><w:t>\\u00abCity\\u00bb</w:t></w:r></w:fldSimple>'%ns))
d.save('build/a6m.docx')
P`);
 await fresh();await open('build/a6m.docx');await A.p.screenshot({path:'build/a6m_shot.png'});
 x=await save('build/a6m2.docx');ok('MERGEFIELD is read and written back as a field',/w:instr=" MERGEFIELD Name "/.test(x)&&/w:instr=" MERGEFIELD City "/.test(x),x.slice(x.indexOf('<w:body'),x.indexOf('<w:body')+400));
 await C(250,47);await C(299,76);await W(100);await A.p.evaluate(()=>annPaste('Name,City\nAda,Paris\nBob,Oslo\n'));await W(300);
 await save('build/a6m3.docx');const pt=paras('build/a6m3.docx');ok('merge fills MERGEFIELD values, one copy per row',/Dear Ada of Paris/.test(pt)&&/Dear Bob of Oslo/.test(pt),pt);
 await fresh();await T('Hi ');await C(250,47);await C(150,97);await C(80,47);await T('Who');await A.p.screenshot({path:'build/a6m_btn.png'});x=await save('build/a6m4.docx');ok('Merge Field button inserts a field',/MERGEFIELD Who /.test(x),paras('build/a6m4.docx'));
 await A.b.close();console.log(res.filter(r=>r[1]).length+'/'+res.length+' passed');
})();
