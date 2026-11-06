// Tier 4 file tests: tracked changes, fields and equations through .docx; deflate; word/styles.xml.
// LibreOffice stands in as an independent reader. It is not Word.
const d=require('./drive');const fs=require('fs');const {execSync}=require('child_process');const crypto=require('crypto');
const h=b=>crypto.createHash('md5').update(b).digest('hex');
const shot=async p=>{await p.mouse.move(1270,5);return await p.screenshot({clip:{x:0,y:174,width:1280,height:602}});};
const py=c=>execSync(`python3 -c "${c}"`).toString();
(async()=>{const res=[];const ok=(n,v,x)=>{res.push([n,!!v]);console.log(v?'PASS':'FAIL',n,x===undefined?'':x);};
 const {b,p}=await d();await p.evaluate(()=>{window.annMax=30000000});
 const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t),C=(x,y)=>p.mouse.click(x,y);
 const INS=()=>C(135,47),REV=()=>C(334,47),HOME=()=>C(80,47);
 const open=async f=>{await p.evaluate(u=>annOpen(new Blob([new Uint8Array(u)])),[...fs.readFileSync(f)]);await p.waitForTimeout(500);};
 const save=async f=>{const [dl]=await Promise.all([p.waitForEvent('download'),K('Control+s')]);await dl.saveAs(f);};
 await T('Keep this text.');await K('Enter');await REV();await C(252,76);await T('added words');await K('Enter');await C(252,76);
 await T('Remove me now');await C(252,76);await K('Shift+Home');await K('Delete');await C(252,76);await K('End');await K('Enter');
 await INS();await T('Page ');await C(434,76);await T(' words ');await C(560,76);await K('Enter');
 await T('E=mc^2 and x_1');await C(725,76);await K('End');await HOME();await p.waitForTimeout(100);
 const a=await shot(p);fs.writeFileSync('build/t4a.png',a);await save('build/t4.docx');
 const x=py("import zipfile;print(zipfile.ZipFile('build/t4.docx').read('word/document.xml').decode())");fs.writeFileSync('build/t4.xml',x);
 ok('w:ins with author saved',/<w:ins w:id="\d+" w:author="SynapseWrite" w:date="[^"]+">.*added words/.test(x));
 ok('w:del with w:delText saved',/<w:del w:id="\d+" w:author="SynapseWrite" w:date="[^"]+"><w:r>.*<w:delText[^>]*>Remove me now<\/w:delText>/.test(x));
 ok('PAGE and NUMWORDS fields saved',/fldSimple w:instr=" PAGE "/.test(x)&&/fldSimple w:instr=" NUMWORDS "/.test(x));
 ok('superscript and subscript saved',/vertAlign w:val="superscript"/.test(x)&&/vertAlign w:val="subscript"/.test(x));
 ok('zip passes CRC, members deflated',py("import zipfile;z=zipfile.ZipFile('build/t4.docx');print(z.testzip(),all(i.compress_type==8 for i in z.infolist()))").trim()==='None True');
 py("import xml.dom.minidom as m,zipfile;m.parseString(zipfile.ZipFile('build/t4.docx').read('word/document.xml'))");ok('document.xml is well formed',true);
 await open('build/t4.docx');await HOME();await K('Control+End');
 const a2=await shot(p);fs.writeFileSync('build/t4a2.png',a2);
 ok('tracked, field and equation runs reopen pixel identical',h(a)===h(a2));
 await save('build/t4b.docx');const x2=py("import zipfile;print(zipfile.ZipFile('build/t4b.docx').read('word/document.xml').decode())");ok('second save XML identical after reopen',x===x2);
 // the marks are live after reopen: reject restores, accept removes
 await REV();await C(400,76);await HOME();await save('build/t4c.docx');const x3=py("import zipfile;print(zipfile.ZipFile('build/t4c.docx').read('word/document.xml').decode())");
 ok('reject after reopen drops insert, restores delete',!/added words/.test(x3)&&/Remove me now/.test(x3)&&!/w:del /.test(x3));
 execSync('rm -rf build/lo4; timeout 120 soffice --headless --convert-to txt:Text --outdir build/lo4 build/t4.docx >/dev/null 2>&1');
 const lo=fs.readFileSync('build/lo4/t4.txt','utf8');ok('LibreOffice reads the file (stand-in, not Word)',/Keep this text/.test(lo)&&/added words/.test(lo),JSON.stringify(lo.slice(0,160)));
 await b.close();
 // date fields from a fixed time vector, including leap day boundaries
 for(const [iso,want] of [['2026-11-05T12:00:00Z','11/5/2026'],['2024-02-29T12:00:00Z','2/29/2024'],['2024-12-31T12:00:00Z','12/31/2024'],['2025-01-01T12:00:00Z','1/1/2025'],['2023-03-01T12:00:00Z','3/1/2023']]){
  const {b,p}=await d();await p.evaluate(t=>{const v=new Date(t).getTime()+new Date().getTimezoneOffset()*0;Date.now=()=>v;},iso);await p.mouse.click(135,47);await p.mouse.click(493,76);await p.waitForTimeout(50);
  const [dl]=await Promise.all([p.waitForEvent('download'),p.keyboard.press('Control+s')]);await dl.saveAs('build/dt.docx');const x=py("import zipfile;print(zipfile.ZipFile('build/dt.docx').read('word/document.xml').decode())");
  const m=x.match(/instr=" DATE ">.*?preserve">([^<]*)</);ok('date field '+iso.slice(0,10),m&&m[1]===want,m&&m[1]);await b.close();}
 // deflate on a large document
 {const {b,p}=await d();await p.evaluate(()=>{window.annMax=60000000;let s='';for(let i=0;i<400;i++)s+='This paragraph number '+i+' makes the file big enough to measure compression on the document part.\n';annPaste(s);});await p.waitForTimeout(500);
  const t0=Date.now();const [dl]=await Promise.all([p.waitForEvent('download'),p.keyboard.press('Control+s')]);await dl.saveAs('build/big.docx');const ms=await p.evaluate('annStats.ms');
  const r=py("import zipfile;z=zipfile.ZipFile('build/big.docx');print(z.testzip());i=z.getinfo('word/document.xml');print(i.file_size,i.compress_size)").trim().split('\n');
  ok('large file passes CRC and shrinks at least 5 times',r[0]==='None'&&(+r[1].split(' ')[0])/(+r[1].split(' ')[1])>5,r[1]+' bytes, '+Math.round(ms)+' ms');
  await p.evaluate(u=>annOpen(new Blob([new Uint8Array(u)])),[...fs.readFileSync('build/big.docx')]);await p.waitForTimeout(800);const [dl2]=await Promise.all([p.waitForEvent('download'),p.keyboard.press('Control+s')]);await dl2.saveAs('build/big2.docx');
  ok('large file reopens through own inflate unchanged',py("import zipfile;a=zipfile.ZipFile('build/big.docx').read('word/document.xml');b=zipfile.ZipFile('build/big2.docx').read('word/document.xml');print(a==b)").trim()==='True');await b.close();}
 // styles.xml: same look through styles and through direct formatting
 fs.writeFileSync('build/mk.py',`
import zipfile
CT='<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'
NS='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
ST='<w:styles '+NS+'><w:docDefaults><w:rPrDefault><w:rPr><w:sz w:val="24"/></w:rPr></w:rPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:color w:val="C00000"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/></w:pPr><w:rPr><w:b/><w:sz w:val="40"/></w:rPr></w:style><w:style w:type="character" w:styleId="Em"><w:name w:val="Em"/><w:rPr><w:i/><w:sz w:val="24"/></w:rPr></w:style></w:styles>'
def doc(b): return '<w:document '+NS+'><w:body>'+b+'</w:body></w:document>'
A='<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>Title here</w:t></w:r></w:p><w:p><w:r><w:t>Body </w:t></w:r><w:r><w:rPr><w:b/></w:rPr><w:t>bold</w:t></w:r><w:r><w:rPr><w:rStyle w:val="Em"/></w:rPr><w:t> slanted</w:t></w:r></w:p><w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:rPr><w:b w:val="0"/></w:rPr><w:t>Plain weight</w:t></w:r></w:p>'
def R(t,x): return '<w:r><w:rPr>'+x+'</w:rPr><w:t>'+t+'</w:t></w:r>'
C='<w:color w:val="C00000"/>'
B='<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'+R('Title here','<w:b/>'+C+'<w:sz w:val="40"/>')+'</w:p><w:p>'+R('Body ',C+'<w:sz w:val="24"/>')+R('bold','<w:b/>'+C+'<w:sz w:val="24"/>')+R(' slanted','<w:i/><w:sz w:val="24"/>')+'</w:p><w:p><w:pPr><w:jc w:val="center"/></w:pPr>'+R('Plain weight',C+'<w:sz w:val="40"/>')+'</w:p>'
for name,body,sty in (('sa',A,ST),('sb',B,None)):
    z=zipfile.ZipFile('build/'+name+'.docx','w',zipfile.ZIP_DEFLATED); z.writestr('[Content_Types].xml',CT)
    if sty: z.writestr('word/styles.xml',sty)
    z.writestr('word/document.xml',doc(body)); z.close()
`);execSync('python3 build/mk.py');
 {const {b,p}=await d();await p.evaluate(()=>{window.annMax=30000000});
  const op=async f=>{await p.evaluate(u=>annOpen(new Blob([new Uint8Array(u)])),[...fs.readFileSync(f)]);await p.waitForTimeout(400);};
  await op('build/sa.docx');await p.keyboard.press('Control+Home');const sa=await shot(p);fs.writeFileSync('build/sa.png',sa);await op('build/sb.docx');await p.keyboard.press('Control+Home');const sb=await shot(p);fs.writeFileSync('build/sb.png',sb);
  ok('styles.xml: pStyle, basedOn, docDefaults, rStyle, jc, b=0 match direct formatting',h(sa)===h(sb));await b.close();}
 console.log(res.filter(r=>r[1]).length+'/'+res.length+' passed');fs.writeFileSync('build/t4_docx.json',JSON.stringify(res));
})();
