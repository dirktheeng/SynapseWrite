// feat2: equation structures (root with index, n-ary with limits, accents, growing delimiters, two row matrix) drawn, edited, saved and read as OMML,
// and the PDF run effects (small caps, double strike, character spacing, run shading, link annotations).
// Test files are built here. LibreOffice here has no Math module, so OMML is checked against its schema order by hand and read back by this program only;
// LibreOffice stands in for a reader of the run properties only, and it is not Word.
const dr=require('./drive');const fs=require('fs');const {execSync}=require('child_process');
const sh=c=>execSync(c,{stdio:['ignore','pipe','pipe']}).toString();
const O='build/feat2';execSync(`rm -rf ${O}; mkdir -p ${O}`);
const only=process.argv[2]||'';
(async()=>{const res=[];const ok=(n,v,x)=>{res.push([n,!!v]);console.log(v?'PASS':'FAIL',n,x===undefined?'':x);};
 let A;const K=k=>A.p.keyboard.press(k),T=t=>A.p.keyboard.type(t),C=(x,y)=>A.p.mouse.click(x,y),W=ms=>A.p.waitForTimeout(ms);
 const start=async()=>{if(A)await A.b.close();A=await dr();await A.p.evaluate(()=>{window.annMax=60000000});};
 const save=async f=>{const [d]=await Promise.all([A.p.waitForEvent('download',{timeout:240000}),K('Control+s')]);await d.saveAs(f);return sh(`unzip -p ${f} word/document.xml`);};
 const pdf=async f=>{const [d]=await Promise.all([A.p.waitForEvent('download',{timeout:240000}),K('Control+p')]);await d.saveAs(f);};
 const open=async f=>{await A.p.evaluate(async u=>{await annOpen(new Blob([new Uint8Array(u)]))},[...fs.readFileSync(f)]);await W(300);};
 const clip={x:223,y:150,width:816,height:300};let hn=0;const shot=async()=>{const f=`${O}/s${hn++}.png`;await A.p.screenshot({clip,path:f});return f;};
 const py=s=>sh(`python3 - <<'P'\n${s}\nP`).trim();
 const same=(a,b)=>+py(`from PIL import Image,ImageChops;b=ImageChops.difference(Image.open('${a}').convert('RGB'),Image.open('${b}').convert('RGB')).getbbox();print(0 if not b else b[2]-b[0])`)<=2;   // a caret blink is one column
 const cols=(a,b)=>+py(`from PIL import Image,ImageChops;d=ImageChops.difference(Image.open('${a}').convert('L'),Image.open('${b}').convert('L')).point(lambda v:255 if v else 0);w,h=d.size;p=d.load();print(sum(1 for x in range(w) if any(p[x,y] for y in range(h))))`);   // caret columns
 const wellformed=f=>py(`import zipfile,xml.dom.minidom as M\ntry:\n M.parseString(zipfile.ZipFile('${f}').read('word/document.xml'));print('ok')\nexcept Exception as e: print(e)`)==='ok';
 // ink rows of the first text line block in an image region: [top, bottom]
 const inkrows=(f,x0,y0,x1,y1)=>JSON.parse(py(`from PIL import Image
im=Image.open('${f}').convert('L').crop((${x0},${y0},${x1},${y1}));w,h=im.size;p=im.load()
rows=[y for y in range(h) if any(p[x,y]<128 for x in range(w))]
# the first block: rows until a gap of 6
blk=[];
for y in rows:
  if blk and y-blk[-1]>6: break
  blk.append(y)
print([blk[0],blk[-1]] if blk else [0,0])`));
 const LINE='A root(3)(x+1) and sum(i=1)(n) k and hat(v) bar(y) vec(F) tilde(a) dot(b) left( (a)/(b) right) mat(a&b)(c&d) z';
 if(!only||only==='eq'){
 await start();
 await T(LINE);await C(135,47);await C(725,76);await C(80,47);await K('Control+End');await K('Enter');await T('left( x');await C(135,47);await C(725,76);await C(80,47);
 await K('Control+End');await K('Enter');await T('after');await K('Control+Home');await W(200);
 const s0=await shot();fs.copyFileSync(s0,`${O}/typed.png`);const x=await save(`${O}/t.docx`);fs.writeFileSync(`${O}/t.xml`,x);
 const t_=s=>`<m:r><m:t xml:space="preserve">${s}</m:t></m:r>`;
 ok('root with index saved as m:rad with m:deg',x.includes(`<m:rad><m:deg>${t_('3')}</m:deg><m:e>${t_('x+1')}</m:e></m:rad>`));
 ok('sum saved as m:nary with its sign, limits and a body',/<m:nary><m:naryPr><m:chr m:val="∑"\/><m:limLoc m:val="undOvr"\/><\/m:naryPr><m:sub><m:r><m:t xml:space="preserve">i=1<\/m:t><\/m:r><\/m:sub><m:sup><m:r><m:t xml:space="preserve">n<\/m:t><\/m:r><\/m:sup><m:e>.*>k<\/m:t>.*<\/m:e><\/m:nary><\/m:oMath>/.test(x));
 ok('five accents saved as m:acc with their marks',['̂v','̅y','⃗F','̃a','̇b'].every(s=>x.includes(`<m:acc><m:accPr><m:chr m:val="${s[0]}"/></m:accPr><m:e>${t_(s.slice(1))}</m:e></m:acc>`)));
 ok('delimiters saved as m:d holding the fraction',/<m:d><m:dPr><m:begChr m:val="\("\/><m:endChr m:val="\)"\/><\/m:dPr><m:e>.*<m:f><m:num>.*>a<.*<m:den>.*>b<.*<\/m:f>.*<\/m:e><\/m:d>/.test(x));
 ok('matrix saved as m:m with two rows of two cells',x.includes(`<m:m><m:mr><m:e>${t_('a')}</m:e><m:e>${t_('b')}</m:e></m:mr><m:mr><m:e>${t_('c')}</m:e><m:e>${t_('d')}</m:e></m:mr></m:m>`));
 ok('a delimiter left open is closed at the end of its math zone',/<m:d><m:dPr>(?:(?!<\/m:oMath>).)*>x<\/m:t><\/m:r><\/m:e><\/m:d><\/m:oMath>/.test(x));
 ok('saved document is well formed XML',wellformed(`${O}/t.docx`));
 const b0=inkrows(s0,60,110,700,190);ok('the line grows for the sum and the paren is as tall as the line (ink 40 px or more)',b0[1]-b0[0]>=40,b0);
 const xs=py(`from PIL import Image
im=Image.open('${s0}').convert('L');p=im.load()
# columns that hold a vertical run of 30 dark pixels: the two parentheses
c=[x for x in range(60,700) if max(sum(1 for y in range(y0,y0+30) if p[x,y]<128) for y0 in range(110,160,2))>=28];print(len(c))`);
 ok('two delimiters drawn as tall strokes',+xs>=2,xs);
 await open(`${O}/t.docx`);await W(200);const s1=await shot();const top=(f,g)=>{py(`from PIL import Image\nImage.open('${f}').crop((0,0,816,190)).save('${g}')`);return g;};
 ok('save and open is pixel identical (the closed forms)',same(top(s0,`${O}/c0.png`),top(s1,`${O}/c1.png`)));
 const y2=await save(`${O}/t1b.docx`);ok('a delimiter left open reads back closed, as the file holds it',(y2.match(/<m:d>/g)||[]).length===2&&(y2.match(/<\/m:d>/g)||[]).length===2);
 const y=await save(`${O}/t2.docx`);ok('a second save writes the same math',y.slice(y.indexOf('<m:oMath>'))===x.slice(x.indexOf('<m:oMath>')));
 // edit: the matrix is one character; Backspace takes it, undo brings it back
 await K('Control+Home');await K('End');await K('ArrowLeft');await K('ArrowLeft');await K('Backspace');await W(200);
 const s2=await shot();const z=await save(`${O}/t3.docx`);
 ok('Backspace deletes the matrix as one character',!z.includes('<m:m>')&&/>z<\/m:t>/.test(z)&&wellformed(`${O}/t3.docx`)&&!same(s1,s2));
 await K('Control+z');await W(300);const s3=await shot();const z2=await save(`${O}/t4.docx`);ok('undo brings it back (same math saved, same pixels but the caret)',z2.slice(z2.indexOf('<m:oMath>'))===y.slice(y.indexOf('<m:oMath>'))&&cols(s1,s3)<=2,cols(s1,s3));
 // PDF: same forms, line about as tall as on the screen
 await pdf(`${O}/t.pdf`);let qc;try{qc=sh(`qpdf --check ${O}/t.pdf 2>&1`);}catch(e){qc=e.stdout.toString();}
 ok('PDF is clean',/No syntax/.test(qc)&&!/WARNING/.test(qc));
 sh(`pdftoppm -r 96 -f 1 -l 1 -png ${O}/t.pdf ${O}/tp`);const pp=fs.readdirSync(O).find(f=>/^tp.*png$/.test(f));fs.copyFileSync(`${O}/${pp}`,`${O}/typed_pdf.png`);
 const b1=inkrows(`${O}/${pp}`,90,60,780,200);ok('PDF line ink height within 4 px of the screen',Math.abs((b1[1]-b1[0])-(b0[1]-b0[0]))<=4,[b0,b1]);
 const xp=py(`from PIL import Image
im=Image.open('${O}/${pp}').convert('L');p=im.load()
c=[x for x in range(90,780) if max(sum(1 for y in range(y0,y0+30) if p[x,y]<200) for y0 in range(60,160,2))>=26];print(len(c))`);
 ok('PDF draws the tall delimiters',+xp>=2,xp);
 const tx=sh(`pdftotext ${O}/t.pdf -`);ok('PDF has the texts of the forms',/x\+1/.test(tx)&&/i=1/.test(tx),tx.slice(0,120));
 // a file built here: product, integral, tilde accent, an m:bar, square brackets, root with index, a 2 by 2 matrix
 const NS='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"';
 const r=s=>`<m:r><m:t>${s}</m:t></m:r>`;
 const om=`<m:oMath ${NS}><m:nary><m:naryPr><m:chr m:val="∏"/><m:limLoc m:val="undOvr"/></m:naryPr><m:sub>${r('j=0')}</m:sub><m:sup>${r('m')}</m:sup><m:e>${r('q')}</m:e></m:nary>${r('+')}<m:nary><m:naryPr><m:limLoc m:val="undOvr"/></m:naryPr><m:sub>${r('0')}</m:sub><m:sup>${r('1')}</m:sup><m:e>${r('f')}</m:e></m:nary>${r('+')}<m:acc><m:accPr><m:chr m:val="̃"/></m:accPr><m:e>${r('u')}</m:e></m:acc><m:bar><m:barPr><m:pos m:val="top"/></m:barPr><m:e>${r('w')}</m:e></m:bar><m:d><m:dPr><m:begChr m:val="["/><m:endChr m:val="]"/></m:dPr><m:e><m:f><m:num>${r('1')}</m:num><m:den>${r('2')}</m:den></m:f></m:e></m:d><m:rad><m:radPr><m:degHide m:val="0"/></m:radPr><m:deg>${r('4')}</m:deg><m:e>${r('y')}</m:e></m:rad><m:d><m:e><m:m><m:mr><m:e>${r('1')}</m:e><m:e>${r('0')}</m:e></m:mr><m:mr><m:e>${r('0')}</m:e><m:e>${r('1')}</m:e></m:mr></m:m></m:e></m:d></m:oMath>`;
 fs.writeFileSync(`${O}/om.xml`,om);
 py(`import docx
from docx.oxml import parse_xml
d=docx.Document();p=d.add_paragraph('Let ')
p._p.append(parse_xml(open('${O}/om.xml').read()))
p.add_run(' done')
d.add_paragraph('second')
d.save('${O}/f.docx')`);
 await open(`${O}/f.docx`);await W(200);const f0=await shot();fs.copyFileSync(f0,`${O}/foreign.png`);
 const fx=await save(`${O}/f2.docx`);fs.writeFileSync(`${O}/f2.xml`,fx);
 ok('foreign product and integral keep their signs and limits',fx.includes(`<m:chr m:val="∏"/><m:limLoc m:val="undOvr"/></m:naryPr><m:sub>${t_('j=0')}</m:sub><m:sup>${t_('m')}</m:sup>`)&&fx.includes(`<m:nary><m:naryPr><m:limLoc m:val="undOvr"/></m:naryPr><m:sub>${t_('0')}</m:sub><m:sup>${t_('1')}</m:sup>`));
 ok('foreign accent and bar come back as accents',fx.includes(`<m:chr m:val="̃"/></m:accPr><m:e>${t_('u')}</m:e>`)&&fx.includes(`<m:chr m:val="̅"/></m:accPr><m:e>${t_('w')}</m:e>`));
 ok('foreign brackets keep their characters around the fraction',/<m:begChr m:val="\["\/><m:endChr m:val="\]"\/><\/m:dPr><m:e>.*<m:f>.*<\/m:f>.*<\/m:e><\/m:d>/.test(fx));
 ok('foreign root keeps its index',fx.includes(`<m:rad><m:deg>${t_('4')}</m:deg><m:e>${t_('y')}</m:e></m:rad>`));
 ok('foreign matrix keeps rows and cells inside parentheses',fx.includes(`<m:m><m:mr><m:e>${t_('1')}</m:e><m:e>${t_('0')}</m:e></m:mr><m:mr><m:e>${t_('0')}</m:e><m:e>${t_('1')}</m:e></m:mr></m:m>`)&&/<m:begChr m:val="\("\/>(?:(?!<m:d>).)*<m:m>/.test(fx));
 ok('foreign text around the math is kept',/>Let <\/w:t>/.test(fx)&&/> done<\/w:t>/.test(fx)&&wellformed(`${O}/f2.docx`));
 await open(`${O}/f2.docx`);await W(200);const f1=await shot();ok('foreign math saved and opened again is pixel identical',same(f0,f1));
 }
 if(!only||only==='pdf'){
 await start();
 const NS='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"';
 const Rn=(t,pr='')=>`<w:r>${pr?'<w:rPr>'+pr+'</w:rPr>':''}<w:t xml:space="preserve">${t}</w:t></w:r>`,P=(...r)=>`<w:p>${r.join('')}</w:p>`;
 const body=P(Rn('Plain '),Rn('Small Caps','<w:smallCaps/>'),Rn(' end'))+P(Rn('double struck','<w:dstrike/>'),Rn(' plain'))+P(Rn('spaced','<w:spacing w:val="60"/>'),Rn(' spaced '),Rn('tight','<w:spacing w:val="-10"/>'),Rn(' tight'))+
  P(Rn('shaded words','<w:shd w:val="clear" w:color="auto" w:fill="FFD966"/>'),Rn(' then '),`<w:hyperlink r:id="rId7">${Rn('alink','<w:u w:val="single"/>')}</w:hyperlink>`,Rn(' after'));
 fs.writeFileSync(`${O}/p.xml`,`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document ${NS}><w:body>${body}<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>`);
 py(`import zipfile
z=zipfile.ZipFile('${O}/p.docx','w',zipfile.ZIP_DEFLATED)
z.writestr('[Content_Types].xml','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
z.writestr('_rels/.rels','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
z.writestr('word/_rels/document.xml.rels','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="http://example.com/a?b=1&amp;c=(2)" TargetMode="External"/></Relationships>')
z.writestr('word/document.xml',open('${O}/p.xml').read())
z.close()`);
 await open(`${O}/p.docx`);await W(200);await A.p.screenshot({clip,path:`${O}/pscreen.png`});
 await pdf(`${O}/p.pdf`);let qc;try{qc=sh(`qpdf --check ${O}/p.pdf 2>&1`);}catch(e){qc=e.stdout.toString();}
 ok('PDF with run effects is clean',/No syntax/.test(qc)&&!/WARNING/.test(qc),qc.slice(0,200));
 sh(`qpdf --qdf --object-streams=disable ${O}/p.pdf ${O}/pq.pdf`);const Q=fs.readFileSync(`${O}/pq.pdf`,'latin1');
 sh(`pdftoppm -r 96 -f 1 -l 1 -png ${O}/p.pdf ${O}/pp`);const PP=`${O}/`+fs.readdirSync(O).find(f=>/^pp.*png$/.test(f));fs.copyFileSync(PP,`${O}/effects_pdf.png`);
 const bb=sh(`pdftotext -bbox ${O}/p.pdf -`);const words=[...bb.matchAll(/xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</g)].map(m=>({x0:+m[1],y0:+m[2],x1:+m[3],y1:+m[4],t:m[5]}));
 const wd=t=>words.filter(w=>w.t===t);
 const S_=wd('S').concat(wd('Small')),M_=words.filter(w=>/^MALL$|^mall$/i.test(w.t));
 const sz=[...Q.matchAll(/\/F\w+ 0*(\d+) Tf[^\n]*\n?[^(]*\(MALL\)/g)].map(m=>+m[1]);const sz0=[...Q.matchAll(/\/F\w+ 0*(\d+) Tf[^\n]*\n?[^(]*\(S\)/g)].map(m=>+m[1]);
 ok('small capitals print at the smaller size, capitals at full size',sz.length&&sz0.length&&sz[0]<sz0[0],[sz0,sz]);
 ok('small capitals are shorter in the printed page',M_.length&&S_.length&&(M_[0].y1-M_[0].y0)<(S_[0].y1-S_[0].y0),[S_[0],M_[0]]);
 const dsw=wd('double')[0];const lines=dsw?+py(`from PIL import Image
im=Image.open('${PP}').convert('L');p=im.load();k=96/72
x0,x1,y0,y1=int(${dsw.x0}*k)+1,int(${dsw.x1}*k)-1,int(${dsw.y0}*k),int(${dsw.y1}*k)+1
full=[y for y in range(y0,y1) if sum(1 for x in range(x0,x1) if p[x,y]<160)>=(x1-x0)*0.9]
g=0;prev=-9
for y in full:
  if y-prev>1: g+=1
  prev=y
print(g)`):0;
 ok('double strike prints two lines through the word',lines===2,lines);
 ok('character spacing is written as Tc, wide and tight',/4\.00 Tc/.test(Q)&&/-0\.67 Tc/.test(Q)&&/0\.00 Tc/.test(Q));
 const sp=wd('spaced')[0];const gap=sp?sp.x0-72-(sp.x1-sp.x0):0;   // pdftotext splits the spaced letters, so the spaced word is measured from the line start to the plain one, less one space
 ok('spaced word prints wider than the plain one by six gaps of 3 pt',gap>=18&&gap<=23,gap.toFixed(2));
 const shw=wd('shaded')[0];const shc=shw?py(`from PIL import Image
im=Image.open('${PP}').convert('RGB');p=im.load();k=96/72
from collections import Counter
c=Counter(p[x,y] for x in range(int(${shw.x0}*k),int(${shw.x1}*k)) for y in range(int(${shw.y0}*k),int(${shw.y1}*k)))
print(','.join(map(str,c.most_common(1)[0][0])))`):'';
 ok('run shade prints in its exact color under the text',shc.split(',').map(Number).every((v,i)=>Math.abs(v-[255,217,102][i])<=3),shc);
 const ann=[...Q.matchAll(/\/Rect \[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]/g)].map(m=>m.slice(1).map(Number));const lw=wd('alink')[0];
 ok('the external link is a URI link annotation with the target unescaped',/\/S \/URI\s*\/URI \(http:\/\/example\.com\/a\?b=1&c=\\\(2\\\)\)/.test(Q),(Q.match(/\/URI \([^\n]*/)||[''])[0]);
 const ph=792;ok('its box covers the linked word',ann.length>=1&&lw&&ann.some(r=>r[0]<=lw.x0+1&&r[2]>=lw.x1-1&&r[1]<=ph-lw.y1+1&&r[3]>=ph-lw.y0-1),[ann,lw]);
 ok('pages tree and every page reference its annotations',/\/Annots \d+ 0 R/.test(Q)&&!/WARNING/.test(qc));
 }
 await A.b.close();const np=res.filter(r=>r[1]).length;console.log(np+'/'+res.length+' passed');process.exitCode=np===res.length?0:1;
})();
