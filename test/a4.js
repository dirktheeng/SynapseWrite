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
  const s=await A.shot();fs.writeFileSync('build/a4_g.png',s);await A.tab(1);await A.C(...P.grid);await A.p.mouse.click(826+22*2+5,127+22*2+5);await A.save('build/a4_g3.docx');ok('no nested table',(xml('build/a4_g3.docx').match(/<w:tc>/g)||[]).length===15);await A.b.close();const B=await open_();await B.tab(1);await B.C(...P.grid);await B.p.mouse.click(826+22*7+5,127+22*7+5);await B.save('build/a4_g2.docx');const y=xml('build/a4_g2.docx');ok('grid inserts 8 by 8',(y.match(/<w:tc>/g)||[]).length===64,(y.match(/<w:tc>/g)||[]).length);fs.writeFileSync('build/a4_g8.png',await B.shot());await B.b.close();}
 if(want('keep')){const mk=async(flag)=>{const A=await open_();let s='';for(let i=0;i<42;i++)s+='filler\n';await A.p.evaluate(x=>annPaste(x),s);await A.p.waitForTimeout(300);await A.T('Keep me');if(flag){await A.tab(2);await A.C(...P.knext);await A.tab(0);}await A.K('End');await A.K('Enter');await A.p.evaluate(x=>annPaste(x),'body one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty twenty one twenty two twenty three twenty four twenty five twenty six twenty seven twenty eight twenty nine thirty thirty one thirty two thirty three thirty four thirty five thirty six seven eight nine');await A.p.waitForTimeout(300);await A.save('build/a4_k.docx');await A.pdf('build/a4_k.pdf');const t=execSync('pdftotext -f 2 -l 2 build/a4_k.pdf -').toString();return {A,t};};
  // find a filler count that puts the line at the page foot
  const {A,t}=await mk(true);fs.writeFileSync('build/a4_k.png',await A.shot());const x=xml('build/a4_k.docx');ok('keepNext saved',x.includes('<w:keepNext/>'));console.log('page 2:',t.slice(0,80));await A.b.close();}
 if(want('border')){const A=await open_();await A.T('Boxed para');await A.tab(2);await A.C(...P.box);await A.C(...P.sh[2]);await A.tab(0);await A.K('End');await A.K('Enter');await A.T('Second joined para');await A.K('Enter');await A.tab(2);await A.C(...P.nob);await A.C(...P.sh[0]);await A.tab(0);await A.T('Plain after');const a=await A.shot();fs.writeFileSync('build/a4_b.png',a);
  await A.save('build/a4_b.docx');const x=xml('build/a4_b.docx');ok('pBdr saved',x.includes('<w:pBdr><w:top w:val="single"')&&x.includes('w:fill='),x.slice(x.indexOf('<w:body>'),x.indexOf('<w:body>')+200));
  await A.open('build/a4_b.docx');await A.K('Control+End');const c=await A.shot();fs.writeFileSync('build/a4_b2.png',c);ok('borders and shading survive reopen',h(a)===h(c));
  await A.K('Escape');await A.pdf('build/a4_b.pdf');execSync('pdftoppm -r 96 -png -f 1 -l 1 build/a4_b.pdf build/a4_bp');const t=execSync('qpdf --check build/a4_b.pdf 2>&1 || true').toString();ok('PDF checks',/No syntax or stream encoding errors/.test(t),t.slice(-80));
  const lt=lotxt('build/a4_b.docx');ok('LibreOffice reads the file',lt.includes('Boxed para'));await A.b.close();}

 if(want('tabs')){const A=await open_();await A.T('a');await A.K('Tab');await A.T('b');await A.K('Enter');await A.T('aaaaaaaaaaaaaaaaaaa');await A.K('Tab');await A.T('c');const a=await A.shot();fs.writeFileSync('build/a4_t.png',a);
  await A.save('build/a4_t.docx');const x=xml('build/a4_t.docx');ok('tab saved as w:tab',(x.match(/<w:tab\/>/g)||[]).length===2);
  await A.open('build/a4_t.docx');await A.K('Control+End');const c=await A.shot();ok('tabs survive reopen',h(a)===h(c));
  const lt=lotxt('build/a4_t.docx');ok('LibreOffice sees the tab',/a\s{3,}b/.test(lt),lt.slice(0,50));
  await A.pdf('build/a4_t.pdf');const pt=execSync('pdftotext -layout build/a4_t.pdf -').toString();ok('own PDF places the tab',/a\s{3,}b/.test(pt),pt.slice(0,50));
  // a stop from the ruler: click at 2 in, then tab goes there. Selector to right aligned, stop at 4 in.
  const B=await open_();await B.C(319+192,160);await B.T('x');await B.K('Tab');await B.T('stop');const b=await B.shot();fs.writeFileSync('build/a4_t2.png',await B.shot({x:0,y:150,width:1262,height:200}));
  await B.save('build/a4_t2.docx');const y=xml('build/a4_t2.docx');ok('stop saved',y.includes('<w:tab w:val="left" w:pos="2880"/>'),y.slice(y.indexOf('<w:body>'),y.indexOf('<w:body>')+120));
  await B.open('build/a4_t2.docx');await B.K('Control+End');const b2=await B.shot();ok('stop survives reopen',h(b)===h(b2));
  await B.K('Enter');await B.K('Control+z');
  await B.C(210,160);await B.C(210,160);await B.C(319+384,160);await B.K('End');await B.K('Tab');await B.T('right');const r=await B.shot();fs.writeFileSync('build/a4_t3.png',r);await B.save('build/a4_t3.docx');const z=xml('build/a4_t3.docx');ok('right stop saved',z.includes('w:val="right" w:pos="5760"'));await B.K('Control+z');
  await A.b.close();await B.b.close();}
 if(want('ruler')){const drag=async(A,x0,y0,x1,y1)=>{await A.p.mouse.move(x0,y0);await A.p.mouse.down();await A.p.mouse.move((x0+x1)/2,y1);await A.p.mouse.move(x1,y1);await A.p.mouse.up();};
  const para='Ruler text that is long enough to wrap around on to at least a second line so that the first line and the left indent can both be seen on this page with room.';
  const A=await open_();await A.T(para);const a0=await A.shot();await drag(A,319,152,367,152);const a1=await A.shot();fs.writeFileSync('build/a4_r1.png',await A.p.screenshot());ok('first line marker changes layout',h(a0)!==h(a1));
  await A.save('build/a4_r.docx');let x=xml('build/a4_r.docx');ok('first line 0.5 in',x.includes('w:firstLine="720"'),x.slice(x.indexOf('<w:ind'),x.indexOf('<w:ind')+60));
  await A.K('Control+z');const a2=await A.shot();ok('undo of marker drag',h(a2)===h(a0));
  await drag(A,319,171,343,171);await A.save('build/a4_r.docx');x=xml('build/a4_r.docx');ok('hanging marker keeps first line',x.includes('w:left="360"')&&x.includes('w:hanging="360"'),x.slice(x.indexOf('<w:ind'),x.indexOf('<w:ind')+60));await A.K('Control+z');
  await drag(A,943,171,895,171);await A.save('build/a4_r.docx');x=xml('build/a4_r.docx');ok('right indent saved',x.includes('w:right="720"'),x.slice(x.indexOf('<w:ind'),x.indexOf('<w:ind')+60));fs.writeFileSync('build/a4_r2.png',await A.p.screenshot());
  await A.K('Control+End');const c0=await A.shot();await A.open('build/a4_r.docx');await A.K('Control+End');const c1=await A.shot();ok('right indent survives reopen',h(c0)===h(c1));
  const B=await open_();await B.T(para);const b0=await B.shot();await drag(B,319,162,271,162);const b1=await B.shot();fs.writeFileSync('build/a4_r3.png',await B.p.screenshot());await B.save('build/a4_r2.docx');const y=xml('build/a4_r2.docx');ok('left margin drag',y.includes('w:left="720"'),(y.match(/<w:pgMar[^>]*>/)||[''])[0]);
  await B.K('Control+z');const b2=await B.shot();ok('margin drag undoes',h(b2)===h(b0));await A.b.close();await B.b.close();}
 if(want('merge')){const q={merge:[919,74],split:[919,96],hdr:[919,118]};const A=await open_();await A.tab(1);await A.C(...P.grid);await A.p.mouse.click(826+22*2+5,127+22*1+5);await A.T('one');await A.K('Tab');await A.T('two');await A.K('Tab');await A.T('three');await A.K('Tab');await A.T('r2a');await A.K('Tab');await A.T('r2b');await A.K('Tab');await A.T('r2c');
  const a0=await A.shot();await A.K('Control+Home');await A.K('Shift+ArrowRight');await A.K('Shift+ArrowRight');await A.K('Shift+ArrowRight');await A.K('Shift+ArrowRight');await A.C(...q.merge);const a1=await A.shot();fs.writeFileSync('build/a4_m1.png',a1);
  await A.save('build/a4_m.docx');let x=xml('build/a4_m.docx');ok('merge saves gridSpan',x.includes('<w:gridSpan w:val="2"/>')&&(x.match(/<w:tc>/g)||[]).length===5,(x.match(/<w:tc>/g)||[]).length);ok('merged text kept',x.replace(/<[^>]+>/g,'').includes('onetwo'),x.replace(/<[^>]+>/g,'').slice(-30));
  ok('grid comes from a full row',(x.match(/<w:gridCol/g)||[]).length===3&&!x.includes('<w:gridCol w:w="0"'));
  await A.K('Control+End');const a2=await A.shot();await A.open('build/a4_m.docx');await A.K('Control+End');const a3=await A.shot();fs.writeFileSync('build/a4_m2.png',a3);ok('merged cell survives reopen',h(a2)===h(a3));
  const lt=lotxt('build/a4_m.docx');ok('LibreOffice reads the merged table',lt.includes('onetwo'),lt.slice(0,60));
  await A.K('Control+z');
  await A.K('Control+Home');await A.C(...q.split);const a4=await A.shot();fs.writeFileSync('build/a4_m3.png',a4);await A.save('build/a4_m3.docx');x=xml('build/a4_m3.docx');ok('split restores the cells',!x.includes('gridSpan')&&(x.match(/<w:tc>/g)||[]).length===6,(x.match(/<w:tc>/g)||[]).length);
  await A.K('Control+End');await A.C(...q.split);await A.save('build/a4_m4.docx');x=xml('build/a4_m4.docx');ok('split of a plain cell adds one cell',(x.match(/<w:tc>/g)||[]).length===7&&x.includes('gridSpan'),(x.match(/<w:tc>/g)||[]).length);fs.writeFileSync('build/a4_m4.png',await A.shot());
  await A.K('Control+z');await A.b.close();
  const B=await open_();await B.tab(1);await B.C(...P.grid);await B.p.mouse.click(826+22*1+5,127+22*0+5);await B.T('HEADER');await B.tab(1);await B.C(...q.hdr);await B.tab(0);await B.K('Tab');await B.T('H2');
  for(let i=0;i<40;i++){await B.K('Tab');await B.T('row '+i);await B.K('Tab');await B.T('x');}await B.tab(1);await B.K('Tab');
  let n=0;
  await B.tab(0);await B.save('build/a4_h.docx');x=xml('build/a4_h.docx');ok('tblHeader saved',x.includes('<w:tblHeader/>'));
  fs.writeFileSync('build/a4_h.png',await B.p.screenshot());await B.b.close();}
 if(want('pagenum')){const A=await open_();await A.tab(1);await A.C(420,74);await A.p.keyboard.type('Page ');await A.C(422,118);await A.K('Enter');await A.C(1003,74);await A.C(1000,88+22*1+10);await A.tab(0);await A.T('text');const a=await A.shot();fs.writeFileSync('build/a4_n.png',await A.p.screenshot());
  await A.save('build/a4_n.docx');const x=xml('build/a4_n.docx');ok('format saved',x.includes('w:fmt="lowerRoman"'),(x.match(/<w:pgNumType[^>]*>/)||[''])[0]);
  await A.pdf('build/a4_n.pdf');const t=execSync('pdftotext build/a4_n.pdf -').toString();ok('PDF shows roman',/Page i\b/.test(t),t.slice(0,40));
  await A.open('build/a4_n.docx');await A.K('Control+End');const c=await A.shot();ok('format survives reopen',h(a)===h(c));
  const lt=lotxt('build/a4_n.docx');ok('LibreOffice shows roman',/Page i\b/.test(lt),lt.slice(0,40));await A.b.close();}
 console.log(R.filter(r=>!r[1]).length,'failed of',R.length);process.exit(0);
})();
