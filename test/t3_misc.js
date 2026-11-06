// Tier 3: sections, headers and footers, footnotes, comments, table of contents. Event driven, judged on images and saved files.
const d=require('./drive');const fs=require('fs');const crypto=require('crypto');const H=b=>crypto.createHash('md5').update(b).digest('hex');const {execSync}=require('child_process');
const res=[];const ok=(n,c)=>{res.push([n,!!c]);console.log(c?'PASS':'FAIL',n);};
(async()=>{const {b,p,check}=await d();const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t);const C=(x,y)=>p.mouse.click(x,y);
 const sh=async n=>{await p.mouse.move(1270,5);await check(n);const b_=await p.screenshot({clip:{x:0,y:174,width:1262,height:600}});if(n)fs.writeFileSync('build/'+n+'.png',b_);return H(b_);};
 const tabs={home:[80,47],ins:[135,47],lay:[192,47],ref:[262,47],rev:[333,47]};const go=t=>C(...tabs[t]);
 const save=async f=>{const [dl]=await Promise.all([p.waitForEvent('download'),K('Control+s')]);await dl.saveAs(f);await check('save');};
 const open=async f=>{await p.evaluate(u=>annOpen(new Blob([new Uint8Array(u)])),[...fs.readFileSync(f)]);await p.waitForTimeout(1500);await check('open');};
 // heading and body
 await T('Chapter One');await C(660,88);await K('End');await K('Enter');await C(485,88);
 await T('Body text with a note');
 const n0=await sh();
 await go('ref');await C(190,76);await T('First note text that is long enough to wrap onto a second line at the foot of the page so that the height of the area grows as the words keep coming along');await K('Enter');
 await go('home');await T(' more');const n1=await sh('m1');ok('footnote changes page',n0!==n1);
 await K('Control+z');await K('Control+z');
 let n2=await sh('m1b');
 await K('Control+y');await K('Control+y');const n3=await sh('m1c');ok('footnote redo restores',n3===n1);
 await K('Enter');
 // comment
 await go('rev');await C(58,76);await T('A comment long enough that it must wrap to a second line in the balloon for sure');await K('Enter');const c1=await sh('m2');
 await C(58,102);const c2=await sh('m2b');ok('delete comment changes image',c1!==c2);await K('Control+z');const c3=await sh();ok('delete comment undo',c3===c1);
 await T('x');await K('Enter');
 // second heading, TOC above
 await T('Chapter Two');await C(80,47);await K('Shift+Home');await C(660,88);await K('End');await K('Enter');await C(485,88);
 await go('ref');await C(68,76);const t1=await sh('m3');
 await go('home');await T('zz');await K('Backspace');await K('Backspace');
 await K('Control+Enter');await T('After break');await K('Enter');
 await go('ins');await C(275,76);await T('Head ');await C(1062,102);await K('Enter');
 await C(1062,76);await T('Foot P');await C(1062,102);await K('Enter');
 const h1=await sh('m4');
 await C(1138,76);await T('FIRST');await K('Enter');const h2=await sh('m4b');ok('first page header differs',h1!==h2);
 await go('lay');await T('');await C(1155,76);await T('Second section');await C(1071,76);const s1=await sh('m5');
 await p.mouse.move(600,400);await p.mouse.wheel(0,1100);await p.waitForTimeout(150);const s2=await sh('m5b');
 await go('ref');await C(68,102);const t2=await sh('m6');
 await p.mouse.move(600,400);await p.mouse.wheel(0,-3000);await p.waitForTimeout(150);await sh('m6b');
 const nz=async()=>{await p.mouse.move(600,400);for(let i=0;i<6;i++){await p.mouse.wheel(0,-900);await p.waitForTimeout(60);}await C(600,300);await p.waitForTimeout(50);};await nz();const a=await sh('m7');
 await save('build/m.docx');await open('build/m.docx');await nz();const a2=await sh('m8');ok('all features save then open identical',a===a2);
 execSync('rm -rf build/mlo; timeout 120 soffice --headless --convert-to docx:"MS Word 2007 XML" --outdir build/mlo build/m.docx >/dev/null 2>&1; timeout 120 soffice --headless --convert-to pdf --outdir build/mlo build/m.docx >/dev/null 2>&1; pdftoppm -r 40 -png build/mlo/m.pdf build/mlo/p');
 await open('build/mlo/m.docx');await nz();const a3=await sh('m9');ok('all features after LibreOffice identical',a===a3);
 const x=f=>require('child_process').execSync(`python3 -c "import zipfile;z=zipfile.ZipFile('${f}');print(z.testzip());[print(n) for n in z.namelist()]"`).toString();console.log(x('build/m.docx').split('\n').join(' '));
 const [dl]=await Promise.all([p.waitForEvent('download'),K('Control+p')]);await dl.saveAs('build/m.pdf');{const t_=execSync('pdftotext -layout build/m.pdf -').toString();ok('PDF has the footnote text',/First note text/.test(t_));ok('PDF has the header and footer',/Head 2/.test(t_)&&/Foot P2/.test(t_));ok('PDF table of contents has dots and page numbers',/Chapter One\s*\.[. ]+\d/.test(t_));}
 // second scenario: two notes numbered in text order, a two column narrow section, shaded table inside the document
 await K('Control+a');await K('Delete');await go('home');
 await T('First');await go('ref');await C(190,76);await T('alpha');await K('Enter');await K('Home');await C(190,76);await T('beta');await K('Enter');await go('home');await K('End');const f2=await sh('n1');
 await go('lay');await C(1155,76);await C(132,76);await C(1050,102);await go('home');
 for(let i=0;i<40;i++){await T('Words in a narrow two column section keep flowing down the page. ');}
 await p.waitForTimeout(80);const f3=await sh('n2');
 await nz();const f4=await sh('n3');
 await save('build/n.docx');await open('build/n.docx');await nz();const f5=await sh('n4');ok('two column narrow section save then open identical',f4===f5);
 execSync('rm -rf build/nlo; timeout 120 soffice --headless --convert-to pdf --outdir build/nlo build/n.docx >/dev/null 2>&1; pdftoppm -r 40 -png build/nlo/n.pdf build/nlo/p');
 // margins chosen from the Tier 1 menu live in the section, so they save
 await K('Control+a');await K('Delete');await go('home');await T('Menu margin text');await go('lay');await C(291,90);await p.waitForTimeout(40);await C(320,182);await p.waitForTimeout(40);await go('home');await C(600,300);await p.waitForTimeout(60);const q1=await sh('q1');
 await save('build/q.docx');const qx=execSync(`python3 -c "import zipfile;print(zipfile.ZipFile('build/q.docx').read('word/document.xml').decode())"`).toString();ok('margins menu saved in sectPr',/w:left="720"/.test(qx)&&/w:right="720"/.test(qx));
 await open('build/q.docx');await C(600,300);await p.waitForTimeout(60);const q2=await sh('q2');ok('margins menu reopens identical',q1===q2);
 console.log(JSON.stringify(res));await b.close();})();
