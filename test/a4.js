// Reviewer a4 suite. Driven only by input events, judged on images and saved files. Real coordinates, no remap table.
const fs=require('fs'),crypto=require('crypto');const {execSync}=require('child_process');const {chromium}=require('playwright');
const R=[];const ok=(n,c,x)=>{R.push([n,!!c]);console.log(c?'PASS':'FAIL',n,x===undefined?'':x);};
const h=b=>crypto.createHash('md5').update(b).digest('hex');
const open_=async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:800}});p.on('pageerror',e=>console.log('PAGEERR',e.message));
 await p.goto('file://'+require('path').resolve(__dirname,'../build/index.html'));await p.waitForFunction('window.annReady',{timeout:120000});await p.evaluate(()=>{window.annMax=30000000});
 const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t),C=(x,y,o)=>p.mouse.click(x,y,o);
 const tab=i=>C([80,128,182,250,318,372][i],47);
 const shot=async(cl)=>{await p.mouse.move(1270,5);await p.waitForTimeout(40);return await p.screenshot({clip:cl||{x:0,y:174,width:1262,height:602}});};
 const save=async f=>{const [dl]=await Promise.all([p.waitForEvent('download'),K('Control+s')]);await dl.saveAs(f);};
 const pdf=async f=>{const [dl]=await Promise.all([p.waitForEvent('download'),K('Control+p')]);await dl.saveAs(f);};
 const open=async f=>{await p.evaluate(u=>annOpen(new Blob([new Uint8Array(u)])),[...fs.readFileSync(f)]);await p.waitForTimeout(600);};
 return {b,p,K,T,C,tab,shot,save,pdf,open};};
const xml=(f,m='word/document.xml')=>execSync(`python3 -c "import zipfile;print(zipfile.ZipFile('${f}').read('${m}').decode())"`,{maxBuffer:1<<26}).toString();
const lotxt=(f)=>{execSync(`rm -rf build/lo_a4; timeout 150 soffice --headless --convert-to pdf --outdir build/lo_a4 ${f} >/dev/null 2>&1`);const n=f.split('/').pop().replace('.docx','.pdf');return execSync(`pdftotext -layout build/lo_a4/${n} -`).toString();};
const only=process.argv[2];const want=n=>!only||only.split(',').includes(n);
(async()=>{
 const P={painter:[67,118],caseb:[140,122],clear:[210,122],grid:[853,95],knext:[878,74],klines:[878,96],pbefore:[878,118],box:[950,74],bottom:[950,96],top:[950,118],nob:[1013,74],sh:[[990,96],[1012,96],[1034,96],[990,118],[1012,118],[1034,118]]};
 if(want('ribbon')){const A=await open_();
  fs.writeFileSync('build/a4_home.png',await A.shot({x:0,y:0,width:1280,height:174}));await A.tab(1);fs.writeFileSync('build/a4_ins.png',await A.shot({x:0,y:0,width:1280,height:174}));await A.tab(2);
  const a=await A.shot({x:0,y:60,width:1280,height:90});fs.writeFileSync('build/a4_lay.png',await A.shot({x:0,y:0,width:1280,height:174}));
  await A.p.mouse.move(878,74);await A.p.waitForTimeout(60);const b=await A.p.screenshot({clip:{x:840,y:64,width:76,height:21}});await A.p.mouse.move(878,96);await A.p.waitForTimeout(60);const c=await A.p.screenshot({clip:{x:840,y:64,width:76,height:21}});ok('extension commands have their own hover',h(b)!==h(c));await A.b.close();}
 if(want('case')){const A=await open_();await A.T('hello big world. next one');await A.K('Control+a');const m=async r=>{await A.C(...P.caseb);await A.C(150,131+r*22+10);};
  await m(2);await A.K('Control+s').catch(()=>{});
  const txt=async()=>{await A.save('build/a4_c.docx');return xml('build/a4_c.docx').replace(/<[^>]+>/g,'');};
  let t=await txt();ok('uppercase',t.includes('HELLO BIG WORLD. NEXT ONE'),t.slice(-30));
  await A.K('Control+a');await m(1);t=await txt();ok('lowercase',t.includes('hello big world. next one'),t.slice(-30));
  await A.K('Control+a');await m(0);t=await txt();ok('sentence case',t.includes('Hello big world. Next one'),t.slice(-30));
  await A.K('Control+a');await m(3);t=await txt();ok('capitalize each word',t.includes('Hello Big World. Next One'),t.slice(-30));
  await A.K('Control+a');await m(4);t=await txt();ok('toggle case',t.includes('hELLO bIG wORLD. nEXT oNE'),t.slice(-30));
  await A.K('Control+z');t=await txt();ok('undo of change case',t.includes('Hello Big World. Next One'),t.slice(-30));
  await A.K('Control+End');await A.K('ArrowLeft');await m(2);t=await txt();ok('no selection changes the word at the caret',t.includes('Next ONE')||t.includes('Next ONE'),t.slice(-30));await A.b.close();}
 if(want('clear')){const A=await open_();await A.T('plain');const a=await A.shot();const B=await open_();await B.T('plain');await B.K('Control+a');await B.K('Control+b');await B.K('Control+i');await B.K('Control+u');await B.K('Control+End');await B.K('Control+a');const b0=await B.shot();await B.C(...P.clear);await B.K('Control+End');const b=await B.shot();ok('clear formatting over a selection',h(a)===h(b));
  await B.K('Control+z');await B.K('Control+End');await B.K('Control+a');const b2=await B.shot();ok('undo of clear formatting',h(b0)===h(b2));await B.K('Control+End');await A.b.close();
  const C=await open_();await C.T('Head');await C.C(628,95);const hh=await C.shot();await C.C(...P.clear);await C.K('End');const c=await C.shot();const D=await open_();await D.T('Head');const d=await D.shot();ok('clear without selection resets the paragraph',h(c)===h(d)&&h(hh)!==h(c));await C.b.close();await D.b.close();await B.b.close();}
 if(want('painter')){const A=await open_();await A.T('src dst');await A.K('Home');for(let i=0;i<3;i++)await A.K('Shift+ArrowRight');await A.K('Control+b');await A.K('Control+i');await A.C(...P.painter);
  const rb=await A.shot({x:54,y:108,width:52,height:21});fs.writeFileSync('build/a4_pa.png',rb);
  await A.K('End');for(let i=0;i<3;i++)await A.K('Shift+ArrowLeft');
  // drag select dst with the mouse would need positions: a click on the word applies to the word
  await A.p.mouse.click(345,296);await A.K('End');const a=await A.shot();
  const B=await open_();await B.T('src dst');await B.K('Home');for(let i=0;i<3;i++)await B.K('Shift+ArrowRight');await B.K('Control+b');await B.K('Control+i');await B.K('End');for(let i=0;i<3;i++)await B.K('Shift+ArrowLeft');await B.K('Control+b');await B.K('Control+i');await B.K('End');const b=await B.shot();
  fs.writeFileSync('build/a4_p1.png',a);fs.writeFileSync('build/a4_p2.png',b);ok('painter copies run format to a word',h(a)===h(b));
  await A.T('x');await A.b.close();await B.b.close();}
 if(want('grid')){const A=await open_();await A.tab(1);await A.C(...P.grid);await A.p.mouse.move(826+22*4+5,127+22*2+5);await A.p.waitForTimeout(80);const m=await A.p.screenshot();fs.writeFileSync('build/a4_grid.png',m);await A.p.mouse.click(826+22*4+5,127+22*2+5);await A.tab(0);await A.T('a');await A.K('Tab');await A.T('b');await A.save('build/a4_g.docx');const x=xml('build/a4_g.docx');ok('grid inserts 5 by 3',(x.match(/<w:tc>/g)||[]).length===15&&(x.match(/<w:tr>/g)||[]).length===3,(x.match(/<w:tc>/g)||[]).length);
  const s=await A.shot();fs.writeFileSync('build/a4_g.png',s);await A.tab(1);await A.C(...P.grid);await A.p.mouse.click(826+22*7+5,127+22*7+5);await A.save('build/a4_g2.docx');const y=xml('build/a4_g2.docx');ok('grid inserts 8 by 8 more',(y.match(/<w:tc>/g)||[]).length>=79,(y.match(/<w:tc>/g)||[]).length);await A.K('Control+z');await A.b.close();}
 if(want('keep')){const mk=async(flag)=>{const A=await open_();let s='';for(let i=0;i<42;i++)s+='filler\n';await A.p.evaluate(x=>annPaste(x),s);await A.p.waitForTimeout(300);await A.T('Keep me');if(flag){await A.tab(2);await A.C(...P.knext);await A.tab(0);}await A.K('End');await A.K('Enter');await A.p.evaluate(x=>annPaste(x),'body one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty twenty one twenty two twenty three twenty four twenty five twenty six twenty seven twenty eight twenty nine thirty thirty one thirty two thirty three thirty four thirty five thirty six seven eight nine');await A.p.waitForTimeout(300);await A.save('build/a4_k.docx');await A.pdf('build/a4_k.pdf');const t=execSync('pdftotext -f 2 -l 2 build/a4_k.pdf -').toString();return {A,t};};
  // find a filler count that puts the line at the page foot
  const {A,t}=await mk(true);fs.writeFileSync('build/a4_k.png',await A.shot());const x=xml('build/a4_k.docx');ok('keepNext saved',x.includes('<w:keepNext/>'));console.log('page 2:',t.slice(0,80));await A.b.close();}
 if(want('border')){const A=await open_();await A.T('Boxed para');await A.tab(2);await A.C(...P.box);await A.C(...P.sh[2]);await A.tab(0);await A.K('End');await A.K('Enter');await A.T('Second joined para');await A.K('Enter');await A.tab(2);await A.C(...P.nob);await A.C(...P.sh[0]);await A.tab(0);await A.T('Plain after');const a=await A.shot();fs.writeFileSync('build/a4_b.png',a);
  await A.save('build/a4_b.docx');const x=xml('build/a4_b.docx');ok('pBdr saved',x.includes('<w:pBdr><w:top w:val="single"')&&x.includes('w:fill='),x.slice(x.indexOf('<w:body>'),x.indexOf('<w:body>')+200));
  await A.open('build/a4_b.docx');await A.K('Control+End');const c=await A.shot();fs.writeFileSync('build/a4_b2.png',c);ok('borders and shading survive reopen',h(a)===h(c));
  await A.pdf('build/a4_b.pdf');execSync('pdftoppm -r 96 -png -f 1 -l 1 build/a4_b.pdf build/a4_bp');const t=execSync('qpdf --check build/a4_b.pdf 2>&1 || true').toString();ok('PDF checks',/No syntax or stream encoding errors/.test(t),t.slice(-80));
  const lt=lotxt('build/a4_b.docx');ok('LibreOffice reads the file',lt.includes('Boxed para'));await A.b.close();}
 console.log(R.filter(r=>!r[1]).length,'failed of',R.length);process.exit(0);
})();
