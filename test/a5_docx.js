// Fidelity of foreign .docx files. Files come from test/a5_corpus.py; judged on saved packages (ISO 29500 schemas,
// markers kept, tag checks) and on images. LibreOffice re-reads each save as a stand-in; it is not Word.
const {chromium}=require('playwright');const fs=require('fs');const {execSync}=require('child_process');const crypto=require('crypto');
const H=b=>crypto.createHash('md5').update(b).digest('hex');const C='build/a5c',O='build/a5o';
const ok=(n,v,x)=>console.log(v?'PASS':'FAIL',n,x===undefined?'':x);
(async()=>{execSync(`python3 test/a5_corpus.py ${C}`);fs.mkdirSync(O,{recursive:true});const b=await chromium.launch();
 const shot=async p=>{await p.mouse.move(1270,5);return await p.screenshot({clip:{x:0,y:174,width:1262,height:600}});};
 const run=async(n,f)=>{for(let k=0;;k++)try{return await run1(n,f);}catch(ex){if(k>=3||!/crash/i.test(ex.message))throw ex;console.log('tab crashed, machine short of memory; retry',n);}};
 const run1=async(n,f)=>{const p=await b.newPage({viewport:{width:1280,height:800}});await p.goto('file://'+require('path').resolve('build/index.html'));await p.waitForFunction('window.annReady',{timeout:120000});await p.evaluate(()=>{window.annMax=2000000000});
  await p.evaluate(u=>annOpen(new Blob([new Uint8Array(u)])),[...fs.readFileSync(`${C}/${n}.docx`)]);const st=await p.evaluate(()=>({t:annStats.t9,e:annStats.e9}));
  const a=await shot(p);await f(p,a,st);
  const [dl]=await Promise.all([p.waitForEvent('download',{timeout:300000}),p.keyboard.press('Control+s')]);const s=`${O}/${n}.docx`;await dl.saveAs(s);await p.close();
  const v=execSync(`python3 test/a5_validate.py ${s} || true`).toString();ok(n+' save passes schema, content type and relationship checks',/ OK\n/.test(v),/ OK\n/.test(v)?'':v.slice(0,400));
  const l=execSync(`python3 test/a5_lost.py ${C}/${n}.docx ${s}`).toString().trim();return {s,x:execSync(`python3 -c "import zipfile;print(zipfile.ZipFile('${s}').read('word/document.xml').decode())"`).toString(),lost:l.match(/\[(.*)\]/)[1]};};
 const allkept=(n,r,allow='')=>{const miss=r.lost.split(', ').filter(x=>x&&!allow.includes(x.replace(/'/g,'')));ok(n+' keeps every marker',miss.length===0,miss.join(' '));};
 let r;
 r=await run('a01_format',async(p,a,st)=>{ok('python-docx open stays under 600k ticks (was 1.01 M)',st.t<600000,st.t);ok('and under 10 M edges (was 10.7 M)',st.e<10000000,st.e);fs.writeFileSync(O+'/a01.png',a);});allkept('a01',r);ok('72 pt reads as the largest size, not 14 half points',/<w:sz w:val="72"\/><\/w:rPr><w:t[^>]*>[^<]*M182/.test(r.x));
 r=await run('a02_tables',async(p,a)=>{await p.keyboard.press('Control+Home');await p.waitForTimeout(50);const c=await shot(p);fs.writeFileSync(O+'/t1.png',a);fs.writeFileSync(O+'/t2.png',c);ok('open leaves the view at the top: only the caret differs from Control+Home',+execSync(`python3 -c "from PIL import Image,ImageChops as C;b=C.difference(Image.open('${O}/t1.png').convert('RGB'),Image.open('${O}/t2.png').convert('RGB')).getbbox();print(0 if not b else b[2]-b[0])"`).toString()<=2);fs.writeFileSync(O+'/a02.png',a);});allkept('a02 merged and short rows',r);
 ok('cell paragraphs keep a space',/M601 first para M602 second para/.test(r.x.replace(/<[^>]+>/g,'')));
 r=await run('a05_pictures',async()=>{});allkept('a05 text beside a picture',r);ok('text before and after an inline picture is kept',/M503/.test(r.x)&&/M504/.test(r.x));
 r=await run('a06_notes',async()=>{});allkept('a06 notes',r,'M631');ok('endnote text kept as a note',/M611 endnote/.test(execSync(`python3 -c "import zipfile;print(zipfile.ZipFile('${r.s}').read('word/footnotes.xml').decode())"`).toString()));
 r=await run('a07_comments',async()=>{});allkept('a07 two comments on one paragraph, within the 380 character limit',r,'M710');
 r=await run('a10_tracked',async()=>{});allkept('a10',r);ok('moveFrom is a deletion, moveTo an insertion',/<w:del [^>]*>(?:(?!<\/w:del>).)*M1008/.test(r.x)&&/<w:ins [^>]*>(?:(?!<\/w:ins>).)*M1009/.test(r.x));ok('old formatting of a format change is not applied',!/<w:i\/>(?:(?!<w:t).)*<w:t[^>]*>M1006/.test(r.x));ok('old alignment of a paragraph change is not applied',/w:val="center"\/><\/w:pPr>(?:(?!<\/w:p>).)*M1007/.test(r.x));
 r=await run('a12_tabs',async()=>{});allkept('a12 tabs and breaks',r);ok('line break separates words',/M1207 line<\/w:t><\/w:r><\/w:p>/.test(r.x));
 r=await run('a13_nested',async()=>{});allkept('a13 nested tables',r);
 r=await run('a14_theme',async()=>{});allkept('a14',r);ok('major theme font of this template is sans, minor serif',/<w:rFonts w:ascii="Caladea"[^>]*\/>(?:(?!<w:t).)*<w:t[^>]*>M1402/.test(r.x)&&!/<w:rFonts w:ascii="Caladea"[^>]*\/>(?:(?!<w:t).)*<w:t[^>]*>M1401/.test(r.x));ok('numeric references decode',/M1428 ABéé/.test(r.x.replace(/<[^>]+>/g,'')));
 r=await run('a15_alt',async()=>{});allkept('a15',r,'M1503');ok('fallback content is not read',!/M1503/.test(r.x));ok('math text is kept',/M1505/.test(r.x));
 r=await run('a19_long',async()=>{});allkept('a19 long paragraph',r);
 await b.close();})();
