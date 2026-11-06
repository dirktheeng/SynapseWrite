// Tier 2 suite. Driven by input events and judged on images, the saved .docx and the saved PDF.
const d=require('./drive');const fs=require('fs');const {execSync}=require('child_process');const crypto=require('crypto');
const h=b=>crypto.createHash('md5').update(b).digest('hex');
const R=[];const ok=(n,c,x)=>{R.push([n,!!c]);console.log(c?'PASS':'FAIL',n,x===undefined?'':x);};
const shot=async p=>{await p.mouse.move(1270,5);await p.waitForTimeout(30);return await p.screenshot({clip:{x:0,y:174,width:1280,height:602}});};
const HX=880,CW=26,CH=22,LX=590;
const open_=async()=>{const {b,p}=await d();await p.evaluate(()=>{window.annMax=30000000});
 const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t),C=(x,y)=>p.mouse.click(x,y);
 const cell=(r,c)=>C(HX+c*CW+8,64+r*CH+8),lay=(r,c)=>C(LX+c*CW+8,64+r*CH+8);
 const uni=async s=>{for(const ch of s)await p.evaluate(c=>window.dispatchEvent(new KeyboardEvent('keydown',{key:c})),ch);};
 const save=async f=>{const [dl]=await Promise.all([p.waitForEvent('download'),K('Control+s')]);await dl.saveAs(f);};
 const pdf=async f=>{const [dl]=await Promise.all([p.waitForEvent('download'),K('Control+p')]);await dl.saveAs(f);};
 const open=async f=>{await p.evaluate(u=>annOpen(new Blob([new Uint8Array(u)])),[...fs.readFileSync(f)]);await p.waitForTimeout(500);};
 return {b,p,K,T,C,cell,lay,uni,save,pdf,open,tabL:()=>C(192,47),tabH:()=>C(80,47)};};
const xml=(f,m='word/document.xml')=>execSync(`python3 -c "import zipfile;print(zipfile.ZipFile('${f}').read('${m}').decode())"`,{maxBuffer:1<<26}).toString();
const lo=(f,to)=>{execSync(`rm -rf build/lo_${to}; timeout 120 soffice --headless --convert-to ${to} --outdir build/lo_${to} ${f} >/dev/null 2>&1`);};
const LAT='Français Été naïve Ñandú Ångström ß æ ø ¿ © € “quoted” — ’';
(async()=>{
 {const A=await open_();await A.uni(LAT);const a=await shot(A.p);fs.writeFileSync('build/t2_latin.png',a);
  const B=await open_();await B.p.evaluate(s=>annPaste(s),LAT);const b=await shot(B.p);ok('Latin-1 typed equals pasted',h(a)===h(b));
  const E=await open_();await E.T('Francais');const e=await shot(E.p);ok('accented text draws',h(a)!==h(e));
  await A.K('Control+a');await A.K('Control+c');const clip=await A.p.evaluate('annClip');ok('clipboard returns unicode',clip===LAT,clip);
  await A.K('End');await A.save('build/t2_l.docx');const x=xml('build/t2_l.docx');ok('docx stores UTF-8',x.includes(LAT),'');
  const c0=await shot(A.p);await A.open('build/t2_l.docx');await A.K('Control+End');const c1=await shot(A.p);
  await B.K('End');const bb=await shot(B.p);ok('docx reopen keeps Latin-1 pixels',h(c1)===h(bb));
  lo('build/t2_l.docx','pdf');ok('LibreOffice reads the Latin-1 text',execSync('pdftotext build/lo_pdf/t2_l.pdf -').toString().trim()===LAT);
  await A.pdf('build/t2_l.pdf');const t=execSync('pdftotext build/t2_l.pdf -').toString();ok('PDF carries Latin-1 and punctuation',t.includes('Français')&&t.includes('€')&&t.includes('“quoted”'),t.trim());
  for(const q of [A,B,E])await q.b.close();}
 {const A=await open_();await A.T('Plain strike sup sub high red');await A.K('Home');
  const sel=async(n)=>{for(let i=0;i<n;i++)await A.K('Shift+ArrowRight');};
  for(let i=0;i<6;i++)await A.K('ArrowRight');await sel(6);await A.cell(0,0);await A.K('ArrowRight');const s1=await shot(A.p);
  await A.K('ArrowRight');await sel(3);await A.cell(0,1);await A.K('ArrowRight');await A.K('ArrowRight');await sel(3);await A.cell(0,2);await A.K('ArrowRight');await A.K('ArrowRight');await sel(4);await A.cell(0,5+1);await A.K('ArrowRight');await A.K('ArrowRight');await sel(3);await A.cell(1,1);await A.K('End');
  const s2=await shot(A.p);fs.writeFileSync('build/t2_fmt.png',s2);ok('run formats change pixels',h(s1)!==h(s2));
  await A.save('build/t2_f.docx');const x=xml('build/t2_f.docx');
  for(const tag of ['<w:strike/>','w:vertAlign w:val="superscript"','w:vertAlign w:val="subscript"','w:highlight w:val="yellow"','w:color w:val="FF0000"'])ok('docx has '+tag,x.includes(tag));
  await A.open('build/t2_f.docx');await A.K('Control+End');const s3=await shot(A.p);fs.writeFileSync('build/t2_fmt2.png',s3);ok('strike, scripts, highlight and color survive reopen',h(s2)===h(s3));
  lo('build/t2_f.docx','docx');await A.open('build/lo_docx/t2_f.docx');await A.K('Control+End');const s4=await shot(A.p);ok('same after a LibreOffice re-save',h(s2)===h(s4));
  await A.K('Control+a');await A.cell(0,0);await A.K('Control+z');await A.K('Control+End');const s5=await shot(A.p);fs.writeFileSync('build/t2_u4.png',s4);fs.writeFileSync('build/t2_u5.png',s5);ok('undo of strike over a selection',h(s5)===h(s4));
  await A.b.close();}
 {const A=await open_();await A.T('size');await A.K('Shift+Home');await A.C(205,75);await A.T('18');await A.K('Enter');await A.K('End');const a=await shot(A.p);
  const B=await open_();await B.T('size');await B.K('Shift+Home');for(let i=0;i<4;i++)await B.C(251,75);await B.K('End');const b=await shot(B.p);ok('typed size 18 equals grow to 18',h(a)===h(b));
  await A.K('Shift+Home');await A.C(205,75);await A.T('13');await A.K('Enter');await A.K('End');const c=await shot(A.p);ok('typed size 13 snaps to a compiled size',h(c)!==h(a));await A.b.close();await B.b.close();}
 {const A=await open_();await A.T('first para text that is long enough to take two lines when it is indented a lot more than usual because of the margin set here');await A.K('Enter');await A.T('second');await A.K('ArrowUp');const a0=await shot(A.p);
  await A.tabL();await A.lay(0,1);await A.lay(0,1);await A.lay(0,3);await A.lay(0,5);await A.lay(0,7);await A.lay(0,10);await A.tabH();const a1=await shot(A.p);fs.writeFileSync('build/t2_para.png',a1);
  ok('paragraph properties change layout',h(a0)!==h(a1));
  await A.save('build/t2_p.docx');const x=xml('build/t2_p.docx');ok('docx ind and spacing',x.includes('w:left="720"')&&x.includes('w:firstLine="360"')&&x.includes('w:before="120"')&&x.includes('w:line="360"'),x.slice(x.indexOf('<w:p>'),x.indexOf('<w:p>')+200));
  await A.K('Control+End');const a2=await shot(A.p);await A.open('build/t2_p.docx');await A.K('Control+End');const a3=await shot(A.p);ok('paragraph properties survive reopen',h(a2)===h(a3));
  lo('build/t2_p.docx','docx');await A.open('build/lo_docx/t2_p.docx');await A.K('Control+End');const a4=await shot(A.p);ok('same after a LibreOffice re-save',h(a2)===h(a4));
  await A.K('ArrowUp');for(let i=0;i<6;i++)await A.K('Control+z');await A.K('Control+End');await A.b.close();
  const B=await open_();await B.T('text');const b0=await shot(B.p);await B.tabL();await B.lay(0,1);await B.lay(0,5);await B.lay(0,10);await B.tabH();await B.K('Control+z');await B.K('Control+z');await B.K('Control+z');await B.K('End');const b1=await shot(B.p);ok('paragraph property undo',h(b0)===h(b1));await B.b.close();}
 {const A=await open_();await A.C(330,75);await A.T('one');await A.K('Enter');await A.K('Tab');await A.T('sub a');await A.K('Enter');await A.T('sub b');await A.K('Enter');await A.K('Tab');await A.T('deep');await A.K('Enter');await A.K('Shift+Tab');await A.K('Shift+Tab');await A.T('two');await A.K('Enter');await A.K('Enter');await A.T('after');await A.K('Enter');await A.C(365,75);await A.T('num one');await A.K('Enter');await A.K('Tab');await A.T('num a');await A.K('Enter');await A.T('num b');await A.K('Enter');await A.K('Tab');await A.T('num i');await A.K('Enter');await A.T('num ii');await A.K('Enter');await A.K('Shift+Tab');await A.K('Shift+Tab');await A.T('num two');
  const a=await shot(A.p);fs.writeFileSync('build/t2_list.png',a);
  await A.save('build/t2_li.docx');const x=xml('build/t2_li.docx');ok('docx numPr with levels',x.includes('<w:ilvl w:val="2"/>')&&x.includes('<w:numId w:val="1"/>')&&x.includes('<w:numId w:val="2"/>'));
  await A.open('build/t2_li.docx');await A.K('Control+End');const a2=await shot(A.p);fs.writeFileSync('build/t2_list2.png',a2);ok('multi level lists survive reopen',h(a)===h(a2));
  lo('build/t2_li.docx','docx');await A.open('build/lo_docx/t2_li.docx');await A.K('Control+End');const a3=await shot(A.p);fs.writeFileSync('build/t2_list3.png',a3);ok('same after a LibreOffice re-save',h(a)===h(a3));
  lo('build/t2_li.docx','pdf');const t=execSync('pdftotext -layout build/lo_pdf/t2_li.pdf -').toString();ok('LibreOffice renders level numbering',/1\.\s+num one/.test(t)&&/a\.\s+num a/.test(t)&&/ii\.\s+num ii/.test(t)&&/2\.\s+num two/.test(t),t);
  await A.pdf('build/t2_li.pdf');const t2=execSync('pdftotext -layout build/t2_li.pdf -').toString();ok('own PDF has markers',/a\.\s*num a/.test(t2)&&/ii\.\s*num ii/.test(t2),t2);
  await A.K('Control+a');await A.b.close();
  const B=await open_();await B.C(330,75);await B.T('x');const b0=await shot(B.p);await B.C(330,75);const b1=await shot(B.p);await B.C(330,75);const b2=await shot(B.p);ok('bullet button toggles',h(b0)!==h(b1)&&h(b0)===h(b2));await B.K('Enter');await B.K('Enter');const b3=await shot(B.p);await B.T('y');const b4=await shot(B.p);ok('enter on an empty item ends the list',h(b3)!==h(b4));await B.K('Control+z');await B.b.close();}
 {const A=await open_();await A.T('Main title');await A.C(660,88);await A.K('End');await A.K('Enter');await A.T('Body after heading');await A.K('Enter');await A.T('Another heading');await A.C(660,88);await A.K('End');const a=await shot(A.p);fs.writeFileSync('build/t2_sty.png',a);
  await A.save('build/t2_s.docx');const x=xml('build/t2_s.docx'),st=xml('build/t2_s.docx','word/styles.xml');
  ok('paragraphs reference styles',(x.match(/<w:pStyle w:val="Heading1"\/>/g)||[]).length===2);ok('styles.xml defines them',st.includes('w:styleId="Heading1"')&&st.includes('<w:name w:val="heading 1"/>'),st.slice(0,300));
  await A.open('build/t2_s.docx');await A.K('Control+End');const a2=await shot(A.p);ok('styled text survives reopen',h(a)===h(a2));
  // edit the definition from the caret paragraph: both headings follow
  await A.K('Shift+Home');await A.C(239,102);await A.K('End');const bb4=await shot(A.p);await A.C(HX+9*CW+8,64+2*CH+8);const b0=await shot(A.p);fs.writeFileSync('build/t2_sty2.png',b0);
  await A.save('build/t2_s2.docx');const st2=xml('build/t2_s2.docx','word/styles.xml');const x2=xml('build/t2_s2.docx');ok('updated style is saved',/w:styleId="Heading1".*?w:color w:val="BB0000"/.test(st2),'');ok('all paragraphs of the style changed',(x2.match(/w:color w:val="BB0000"/g)||[]).length>=2);
  await A.K('Control+z');await A.K('Control+End');const b1=await shot(A.p);fs.writeFileSync('build/t2_sty3.png',b1);ok('undo of a style update',h(b1)===h(bb4));await A.b.close();
  lo('build/t2_s2.docx','pdf');ok('LibreOffice opens the styled file',fs.existsSync('build/lo_pdf/t2_s2.pdf'));
  const B=await open_();await B.T('H');await B.C(660,88);await B.K('End');await B.K('Enter');await B.T('body');const c=await shot(B.p);const C=await open_();await C.T('H');await C.C(660,88);await C.K('End');await C.K('Enter');await C.C(485,88);await C.T('body');const c2=await shot(C.p);ok('next paragraph after a heading is Normal',h(c)===h(c2));await B.b.close();await C.b.close();}
 {const A=await open_();let s='';for(let i=0;i<46;i++)s+='filler line\n';s+='Widow test paragraph one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty twenty one twenty two twenty three twenty four twenty five twenty six twenty seven twenty eight twenty nine thirty thirty one thirty two thirty three thirty four thirty five thirty six';await A.p.evaluate(x=>annPaste(x),s);await A.K('Control+End');await A.p.waitForTimeout(300);
  let found=[];for(let n=0;n<10;n++){await A.pdf('build/t2_w.pdf');const pg=execSync('pdftotext -layout build/t2_w.pdf -').toString().split('\f');
   const c=pg.map(q=>q.split('\n').filter(l=>/one two|twenty|thirteen|thirty|five six|eight nine/.test(l)).length);const parts=c.filter(v=>v>0);found.push(parts.join('+'));
   await A.K('Control+Home');await A.p.evaluate(()=>annPaste('filler\n'));await A.K('Control+End');await A.p.waitForTimeout(100);}
  const bad=found.filter(f=>f.split('+').some(v=>v==='1'));console.log(found.join(' '));ok('no single stranded line across ten page positions',bad.length===0&&found.some(f=>f.includes('+')),found.join(' '));await A.b.close();}
 {const A=await open_();execSync('python3 test/mk_foreign.py build/foreign.docx');await A.open('build/foreign.docx');await A.p.waitForTimeout(25000);await A.p.mouse.move(1270,5);const a=await A.p.screenshot({path:'build/t2_foreign.png'});
  await A.save('build/t2_foreign_out.docx');const x=xml('build/t2_foreign_out.docx');
  ok('foreign file: Latin-1 text',x.includes('R\u00e9sum\u00e9 of Tests')&&x.includes('\u201cCurly\u201d \u2014'));
  ok('foreign file: style references kept',x.includes('w:pStyle w:val="Title"')&&x.includes('w:pStyle w:val="Heading1"')&&x.includes('w:pStyle w:val="Quote"'));
  ok('foreign file: style based lists read',x.includes('<w:numId w:val="1"/>')&&x.includes('<w:numId w:val="2"/>'));
  ok('foreign file: run formats read',x.includes('<w:strike/>')&&x.includes('superscript')&&x.includes('subscript')&&x.includes('w:highlight w:val="yellow"'));
  ok('foreign file: paragraph properties read',x.includes('w:left="720"')&&x.includes('w:firstLine="360"')&&x.includes('w:line="360"')&&x.includes('w:val="both"'));
  await A.b.close();}
 // hanging indent: ribbon, save, reopen, LibreOffice, a file from elsewhere
 {const A=await open_();const LG='hanging words that keep going until the line has to wrap onto another line of text in this very paragraph here';
  await A.T(LG);await A.tabL();await A.lay(0,1);await A.lay(0,1);await A.lay(0,2);await A.tabH();await A.K('Control+End');const a=await shot(A.p);fs.writeFileSync('build/hang_a.png',a);
  await A.save('build/hang.docx');const x=xml('build/hang.docx');ok('hanging indent saved',x.includes('w:left="720"')&&x.includes('w:hanging="360"'));
  await A.open('build/hang.docx');await A.K('Control+End');const b=await shot(A.p);fs.writeFileSync('build/hang_b.png',b);ok('hanging indent reopens pixel identical',h(a)===h(b));
  lo('build/hang.docx','docx');await A.open('build/lo_docx/hang.docx');await A.K('Control+End');const c=await shot(A.p);fs.writeFileSync('build/hang_c.png',c);ok('hanging indent after LibreOffice',h(a)===h(c));
  execSync(`python3 - <<'P'
import zipfile
W='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
z=zipfile.ZipFile('build/hang_f.docx','w')
z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
z.writestr('word/document.xml','<?xml version="1.0"?><w:document %s><w:body><w:p><w:pPr><w:spacing w:before="0" w:after="165"/><w:ind w:left="720" w:hanging="360"/></w:pPr><w:r><w:rPr><w:sz w:val="22"/></w:rPr><w:t>${LG}</w:t></w:r></w:p></w:body></w:document>'%W)
z.close()
P`);
  await A.open('build/hang_f.docx');await A.K('Control+End');const f=await shot(A.p);fs.writeFileSync('build/hang_f.png',f);ok('hanging indent from a foreign file',h(a)===h(f));
  await A.pdf('build/hang.pdf');const box=execSync('pdftotext -bbox build/hang.pdf -').toString();const m=[...box.matchAll(/xMin="([\d.]+)" yMin="([\d.]+)"[^>]*>(hanging|text|another|wrap|line|onto)</g)].map(q=>+q[1]);const fx=m[0];
  const lines=[...box.matchAll(/<word xMin="([\d.]+)" yMin="([\d.]+)"/g)];const y0=+lines[0][2];const nx=lines.find(q=>+q[2]>y0+5);ok('hanging indent in the PDF',nx&&+nx[1]>+lines[0][1]+10,nx&&(lines[0][1]+' '+nx[1]));
  await A.b.close();}
 const n=R.filter(r=>r[1]).length;console.log(`${n}/${R.length} passed`);fs.writeFileSync('build/tier2.json',JSON.stringify(R,null,1));
})();
