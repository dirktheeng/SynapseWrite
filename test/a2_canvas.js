// Document canvas look. Built by real input events, judged on canvas pixels and the saved file.
const d=require('./drive');const {execSync}=require('child_process');const fs=require('fs');let fails=0,n=0;
const ok=(name,c,x)=>{n++;if(!c)fails++;console.log(c?'PASS':'FAIL',name,x===undefined?'':x);};
const img=async p=>{await p.mouse.move(1270,5);await p.waitForTimeout(60);await p.evaluate(()=>annDispatch(12));const b64=await p.evaluate(()=>{const c=document.getElementById('screen').getContext('2d').getImageData(0,0,1280,800).data;let s='';for(let i=0;i<c.length;i+=32768)s+=String.fromCharCode.apply(null,c.subarray(i,i+32768));return btoa(s);});const B=Buffer.from(b64,'base64');const o=new Int32Array(1280*800);for(let i=0;i<o.length;i++)o[i]=B[4*i]<<16|B[4*i+1]<<8|B[4*i+2];return o;};
const px=(I,x,y)=>I[y*1280+x];
const runs=(I,x,y0,y1,f)=>{const r=[];let s=-1;for(let y=y0;y<=y1;y++){const h=y<y1&&f(px(I,x,y));if(h&&s<0)s=y;if(!h&&s>=0){r.push([s,y-s]);s=-1;}}return r;};
const rowsInk=(I,x0,x1,y0,y1,f)=>{const r=[];let s=-1;for(let y=y0;y<=y1;y++){let h=false;if(y<y1)for(let x=x0;x<x1;x++)if(f(px(I,x,y))){h=true;break;}if(h&&s<0)s=y;if(!h&&s>=0){r.push(s);s=-1;}}return r;};
const dark=c=>((c>>16)&255)<110&&((c>>8)&255)<110&&(c&255)<110;
const go={home:[80,47],ins:[135,47],ref:[262,47],rev:[333,47]};
(async()=>{
 {const {b,p}=await d();const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t),C=(x,y)=>p.mouse.click(x,y);
  // table: every rule one pixel, rows and the last row closed
  await C(...go.ins);await C(116,76);await T('a');await K('Tab');await T('b');const I=await img(p);
  const r=runs(I,420,200,500,dark);ok('table has four single pixel rules',r.length===4&&r.every(q=>q[1]===1),JSON.stringify(r));
  ok('table rules are black',px(I,420,r[0][0])===0);
  // change a cell, rule stays
  await T('c');const I2=await img(p);ok('rule survives typing in a cell',JSON.stringify(runs(I2,420,200,500,dark))===JSON.stringify(r));
  await K('Control+End');await K('ArrowDown');await T('below');const I3=await img(p);ok('bottom rule stays above the next paragraph',runs(I3,420,200,r[3][0]+1,dark).length===4);
  await b.close();}
 {const {b,p}=await d();const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t),C=(x,y)=>p.mouse.click(x,y);
  // lists: tight items, marker at the quarter inch, space after the last item
  await C(325,76);await T('Bullet one');await K('Enter');await T('Bullet two');await K('Enter');await K('Enter');await T('After');await K('Control+a');const I=await img(p);
  const rows=rowsInk(I,319,520,270,420,dark);ok('list items one line apart',rows[1]-rows[0]===22,JSON.stringify(rows));ok('space after the last item',rows[2]-rows[1]===33,JSON.stringify(rows));
  let mx=9999;for(let y=rows[0];y<rows[0]+16;y++)for(let x=325;x<366;x++)if(dark(px(I,x,y))&&x<mx)mx=x;ok('bullet starts near the quarter inch',mx>=343&&mx<=347,mx);
  const [dl]=await Promise.all([p.waitForEvent('download'),K('Control+s')]);await dl.saveAs('build/a2c.docx');const xml=execSync('unzip -p build/a2c.docx word/document.xml').toString();ok('list items saved with contextual spacing',(xml.match(/<w:contextualSpacing\/>/g)||[]).length===2);
  const bytes=[...fs.readFileSync('build/a2c.docx')];await p.evaluate(u=>annOpen(new Blob([new Uint8Array(u)])),bytes);await p.waitForTimeout(1200);await K('Control+a');const I2=await img(p);{const r2=rowsInk(I2,319,520,270,420,dark);ok('reopened list looks the same',JSON.stringify(r2)===JSON.stringify(rows),JSON.stringify(r2));};
  // selection shows the paragraph mark
  await K('Control+a');const S=await img(p);const sel=0xccddee;let w=0;for(let x=367;x<600;x++)if(px(S,x,rows[0]+3)===sel)w=x;const I0=await (async()=>I2)();let e=0;for(let x=367;x<600;x++)if(dark(px(I2,x,rows[0]+2))||dark(px(I2,x,rows[0]+6))||dark(px(I2,x,rows[0]+9)))e=x;ok('selection runs past the last glyph',w>e+2,[w,e]);
  await b.close();}
 {const {b,p}=await d();const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t),C=(x,y)=>p.mouse.click(x,y);
  // headings: no gap after, regular weight in the file
  await T('Head');await C(660,88);await K('End');await K('Enter');await C(485,88);await T('Body');const I=await img(p);const rows=rowsInk(I,319,400,270,420,c=>c!==0xffffff);ok('body follows heading closely',rows[1]-rows[0]<34,JSON.stringify(rows));
  // modal bars
  const bar0=await img(p);await C(...go.ref);await C(190,76);const A=await img(p);let ch=0;for(let x=223;x<1040;x++)for(let y=174;y<200;y++)if(px(A,x,y)!==px(bar0,x,y))ch++;ok('footnote bar is drawn',ch>200,ch);
  await T('Note words');const A2=await img(p);let tx=0;for(let y=180;y<198;y++)for(let x=310;x<500;x++)if(dark(px(A2,x,y)))tx++;ok('typed note text shows in the bar',tx>40,tx);
  await K('Enter');await C(...go.home);const A3=await img(p);let bl=0;for(let x=223;x<1040;x++)for(let y=174;y<200;y++)if(px(A3,x,y)!==0xffffff&&px(A3,x,y)!==px(bar0,x,y))bl++;ok('footnote bar is gone after Enter',bl===0,bl);
  await C(...go.rev);await C(58,76);await T('Words');const A4=await img(p);tx=0;for(let y=180;y<198;y++)for(let x=310;x<500;x++)if(dark(px(A4,x,y)))tx++;ok('comment text shows in the bar',tx>20,tx);await K('Enter');
  const A5=await img(p);let card=0,yellow=0;for(let y=180;y<770;y++)for(let x=1044;x<1258;x++){if(px(A5,x,y)===0xffffff)card++;if(px(A5,x,y)===0xffeeaa)yellow++;}ok('comment is a white card',card>1000&&yellow===0,[card,yellow]);
  // tracked insertion draws a change bar in the margin
  await K('Control+End');await K('Enter');await C(250,76);await T('Tracked');const B=await img(p);let bar=0;for(let y=270;y<700;y++)if(px(B,319-12,y)===0x404040)bar++;ok('change bar beside tracked text',bar>=15,bar);
  await K('Shift+Home');await K('Backspace');await C(250,76);await K('Control+a');await C(328,76);const B2=await img(p);
  await b.close();}
 {const {b,p}=await d();await p.keyboard.type('x');await p.mouse.click(135,47);await p.mouse.click(1062,76);await p.keyboard.type('Footer text');await p.keyboard.press('Enter');await p.mouse.click(80,47);await p.mouse.move(600,400);await p.mouse.wheel(0,600);await p.waitForTimeout(200);const I=await img(p);const r=rowsInk(I,319,420,400,770,c=>c!==0xffffff);ok('wheel reaches the footer of a one page document',r.length===2,JSON.stringify(r));let gray=0;for(let y=400;y<776;y++)if(px(I,600,y)!==0xffffff)gray++;ok('page foot and workspace visible',gray>5,gray);await b.close();}
 console.log(n-fails,'of',n);process.exit(fails?1:0);})();
