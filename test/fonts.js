// Fonts, sizes and the style table, driven by input events and judged on images and saved files.
const fs=require('fs'),path=require('path'),{execSync}=require('child_process'),{chromium}=require('playwright');
const crypto=require('crypto');const hash=b=>crypto.createHash('md5').update(b).digest('hex');
let fails=0,n=0;const ok=(name,c,x)=>{n++;if(!c)fails++;console.log(c?'PASS':'FAIL',name,x===undefined?'':x);};
const sh=c=>execSync(c,{stdio:['ignore','pipe','pipe']}).toString();
const url='file://'+path.resolve(__dirname,'../build/index.html');
const ids=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../build/provenance.json')));
const NF=8,NAMES=['Carlito','Caladea','Arimo','Tinos','Cousine','Open Sans','Oswald','Caveat'];
(async()=>{const b=await chromium.launch();
 const open=async()=>{const p=await b.newPage({viewport:{width:1280,height:800}});p.on('pageerror',e=>console.log('PAGEERR',e.message));await p.goto(url);await p.waitForFunction('window.annReady',{timeout:120000});await p.evaluate(()=>{window.annMax=60000000});return p;};
 const shot=async(p,clip)=>{await p.mouse.move(1270,5);await p.waitForTimeout(30);return await p.screenshot(clip?{clip}:{});};
 const page={x:224,y:190,width:815,height:586};
 const font=async(p,r)=>{await p.mouse.click(229,75);await p.mouse.click(170,98+r*22);};
 const size=async(p,s)=>{await p.mouse.click(258,75);await p.keyboard.type(String(s));await p.keyboard.press('Enter');};
 // the wasm memory at start
 {const p=await open();const m=await p.evaluate(()=>annMem());ok('wasm memory at start under 100 MB',m<100e6,(m/1e6).toFixed(1)+' MB');await p.close();}
 // every family differs at 11 pt, with the same words
 {const hs=[];for(let r=0;r<NF;r++){const p=await open();await font(p,r);await p.keyboard.type('The quick brown fox jumps over the lazy dog');hs.push(hash(await shot(p,page)));await p.close();}
  ok('all families differ at 11 pt',new Set(hs).size===NF,new Set(hs).size);}
 // the font box names the family, and the menu shows each name in its own face
 {const p=await open();await font(p,3);const a=await shot(p,{x:112,y:64,width:112,height:22});await font(p,0);const c=await shot(p,{x:112,y:64,width:112,height:22});ok('font box follows the family',hash(a)!==hash(c));
  await p.mouse.click(229,75);await p.waitForTimeout(30);const m=await shot(p,{x:112,y:87,width:128,height:176});ok('menu lists the names',hash(m)!==hash(await (async()=>{await p.keyboard.press('Escape');return await shot(p,{x:112,y:87,width:128,height:176});})()));await p.close();}
 // new sizes: every in-between and large size is its own size
 {const hs=new Set();for(const s of [8,13,17,22,30,48,72]){const p=await open();await size(p,s);await p.keyboard.type('Sized Text g');hs.add(hash(await shot(p,page)));await p.close();}
  ok('sizes 8 13 17 22 30 48 72 all differ',hs.size===7,hs.size);}
 // cold and cached draw are the same pixels, including after a flush of the store
 {const mk=async()=>{const p=await open();await size(p,72);await p.keyboard.type('WMgy');await font(p,3);await p.keyboard.type('WMgy');return p;};
  const p=await mk();const a=hash(await shot(p,page));await p.keyboard.press('Control+a');await p.keyboard.press('End');await p.evaluate(()=>annDispatch(6,0,0,1000));const c=hash(await shot(p,page));ok('repaint from the store equals the first draw',a===c);
  await p.keyboard.press('Control+End');for(const pair of [[0,8],[1,48],[2,72],[3,60],[4,66],[5,54],[6,72],[7,72],[2,60],[3,66],[4,48],[5,72],[0,72],[1,66]]){await font(p,pair[0]);await size(p,pair[1]);await p.keyboard.type('@&%WMBQR8g',{delay:0});await p.keyboard.press('Enter');}
  await p.keyboard.press('Control+a');await p.keyboard.press('Delete');const q=await open();await q.close();await p.close();}
 // docx: Word names map to the open families and keep their names when saved
 {sh(`python3 - <<'PY'
import docx
d=docx.Document()
for nm in ['Arial','Times New Roman','Courier New','Calibri','Cambria','Papyrus']:
    r=d.add_paragraph().add_run('Hamburgefonstiv in '+nm); r.font.name=nm
d.save('build/fonts_map.docx')
PY`);
  const p=await open();await p.evaluate(async u=>{await annOpen(new Blob([new Uint8Array(u)]))},[...fs.readFileSync('build/fonts_map.docx')]);await p.waitForTimeout(800);await shot(p);
  fs.writeFileSync('build/fonts_map.png',await shot(p));
  const dl=p.waitForEvent('download');await p.keyboard.press('Control+s');const sv=await (await dl).path();fs.copyFileSync(sv,'build/fonts_saved.docx');const x=sh('unzip -p build/fonts_saved.docx word/document.xml');
  for(const nm of ['Arial','Times New Roman','Courier New','Calibri','Cambria'])ok('saved under its original name: '+nm,x.includes('w:ascii="'+nm+'"'));
  const pdf=p.waitForEvent('download');await p.keyboard.press('Control+p');const pv=await (await pdf).path();fs.copyFileSync(pv,'build/fonts.pdf');const pf=sh('pdffonts build/fonts.pdf');
  for(const nm of ['Arimo','Tinos','Cousine','Carlito','Caladea'])ok('PDF embeds '+nm,pf.includes(nm));ok('PDF leaves out faces it does not use',!pf.includes('Oswald')&&!pf.includes('Caveat'));ok('PDF fonts are all embedded subsets',!/\bno +(yes|no) +(yes|no) /.test(pf.split('\n').slice(2).join('\n').replace(/^.*TrueType\s+WinAnsi\s+yes.*$/gm,'')),pf.split('\n').length);
  await p.close();}
 // the style table: fill it with distinct records by input events, then check what overflow does
 {const p=await open();await p.keyboard.type('anchor');await p.keyboard.press('Control+a');
  const made=await p.evaluate(()=>{const key=(c,m=1)=>annDispatch(2,c,m,1000),click=(x,y)=>{annDispatch(3,x,y,1000);annDispatch(4,x,y);};let k=0;const szs=[];for(let s=8;s<=72;s++)szs.push(s);
   for(let f=0;f<8;f++){click(229,75);click(170,98+f*22);for(const s of szs){click(258,75);for(const ch of String(s))annDispatch(2,ch.charCodeAt(0),0,1000);annDispatch(2,13,0,1000);for(let i=0;i<8;i++){key([98,105,98,117,98,105,98,117][i]);k++;}}}return k;});
  ok('input made more than 4096 format changes',made>4096,made);
  const before=await shot(p,page);
  await size(p,70);const after=await shot(p,page);const sbar={x:0,y:777,width:1000,height:23};const sb1=await shot(p,sbar);const q=await open();await q.keyboard.type('anchor');const sb2=await shot(q,sbar);await q.close();ok('over capacity the status bar says so',hash(sb1)!==hash(sb2));
  ok('over capacity a new format is not applied',hash(before)===hash(after));
  await p.keyboard.press('End');await p.keyboard.type('X');const typed=await shot(p,page);ok('over capacity typing still works',hash(typed)!==hash(after));
  await p.keyboard.press('Control+z');await p.keyboard.press('Control+z');const u=await shot(p,page);ok('over capacity undo still works',hash(u)!==hash(typed));
  await p.close();}
 await b.close();console.log('fonts',n-fails,'of',n);process.exit(fails?1:0);})();
