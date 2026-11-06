// Reviewer a3: Word interaction. Driven by events, judged on images and saved or copied text.
const d=require('./drive');const crypto=require('crypto');const fs=require('fs');const only=process.argv[2];
const res=[];const hash=b=>crypto.createHash('md5').update(b).digest('hex');
const shot=async p=>{await p.mouse.move(1270,5);await p.waitForTimeout(30);return p.screenshot({clip:{x:0,y:0,width:1280,height:800}});};
const run=async(p,st)=>{for(const s of st){if(typeof s==='function')await s(p);else if(s.startsWith('#'))await p.keyboard.press(s.slice(1));else await p.keyboard.type(s);}};
const K=k=>'#'+k;
const take=async st=>{for(let t=0;;t++){try{const A=await d();await run(A.p,st);const i=await shot(A.p);await A.b.close();return i;}catch(e){if(t>=3)throw e;await new Promise(r=>setTimeout(r,20000));}}};
async function cmp(name,a,b,wantSame=true){if(only&&!name.includes(only))return;const ia=await take(a);const ib=await take(b);
 const ok=(hash(ia)===hash(ib))===wantSame;res.push([name,ok]);console.log(ok?'PASS':'FAIL',name);if(!ok){fs.writeFileSync(`build/rv_${res.length}_a.png`,ia);fs.writeFileSync(`build/rv_${res.length}_b.png`,ib);}}
const same=(n,a,b)=>cmp(n,a,b,true);const diff=(n,a,b)=>cmp(n,a,b,false);
const LONG='alpha bravo charlie delta echo foxtrot golf hotel india juliet kilo lima mike november oscar papa quebec romeo sierra tango uniform victor whiskey xray yankee zulu alpha bravo charlie delta';
const click=(x,y,o)=>async p=>{await p.mouse.click(x,y,o||{});};
const paste=t=>async p=>{await p.evaluate(t=>annPaste(t),t);};
const lines=n=>Array.from({length:n},(_,i)=>'line '+i).join('\n');
(async()=>{
 await same('ctrl left to word start',['one two three',K('Control+ArrowLeft'),'X',K('End')],['one two Xthree']);
 await same('ctrl left twice',['one two three',K('Control+ArrowLeft'),K('Control+ArrowLeft'),'X',K('End')],['one Xtwo three']);
 await same('ctrl right to next word',['one two three',K('Home'),K('Control+ArrowRight'),'X',K('End')],['one Xtwo three']);
 await same('ctrl right stops at punctuation',['one, two',K('Home'),K('Control+ArrowRight'),'X',K('End')],['oneX, two']);
 await same('ctrl left crosses paragraph',['one',K('Enter'),'two',K('Home'),K('Control+ArrowLeft'),'X'],['oneX',K('Enter'),'two',K('ArrowUp'),K('End')]);
 await same('ctrl shift left selects word',['one two',K('Control+Shift+ArrowLeft'),'X'],['one X']);
 await same('ctrl shift right selects word',['one two',K('Home'),K('Control+Shift+ArrowRight'),'X',K('End')],['Xtwo']);
 await same('ctrl backspace deletes word',['one two',K('Control+Backspace')],['one ']);
 await same('ctrl backspace merges at start',['one',K('Enter'),K('Control+Backspace')],['one']);
 await same('ctrl delete deletes word',['one two',K('Home'),K('Control+Delete'),K('End')],['two']);
 await same('ctrl backspace undo',['one two',K('Control+Backspace'),K('Control+z')],['one two']);
 await same('ctrl up and down',['one',K('Enter'),'two',K('Control+ArrowUp'),'X',K('Control+ArrowDown'),'Y'],['one',K('Enter'),'XtwoY']);
 const SC=(x,y)=>async p=>{await p.keyboard.down('Shift');await p.mouse.click(x,y);await p.keyboard.up('Shift');};
 await same('shift click extends',['abcdef',K('Home'),SC(345,296),K('Delete'),K('End')],['abcdef',K('Home'),K('Shift+ArrowRight'),K('Shift+ArrowRight'),K('Shift+ArrowRight'),K('Shift+ArrowRight'),K('Delete'),K('End')]);
 await diff('shift click selects something',['abcdef',K('Home'),SC(345,296)],['abcdef',K('Home')]);
 await same('end on wrapped line stays and is idempotent',[LONG,K('Home'),K('Home'),K('ArrowUp'),K('Home'),K('End'),K('End'),'X'],[LONG,K('Home'),K('ArrowUp'),K('Home'),K('End'),'X']);
 await diff('end then type stays on first line',[LONG,K('Home'),K('ArrowUp'),K('End')],[LONG,K('Home')]);
 await same('page down moves caret then up returns',[paste(lines(200)),K('Control+Home'),K('PageDown'),K('PageUp'),K('PageUp'),'X'],[paste(lines(200)),K('Control+Home'),'X']);
 await diff('page down moves caret',[paste(lines(200)),K('Control+Home'),K('PageDown'),'X'],[paste(lines(200)),K('Control+Home'),'X']);
 await same('page up at top goes to start',['ab',K('Enter'),'cd',K('PageUp'),'X'],['ab',K('Enter'),'cd',K('Control+Home'),'X']);
 await diff('shift page down selects',[paste(lines(200)),K('Control+Home'),K('Shift+PageDown'),K('Delete')],[paste(lines(200)),K('Control+Home'),K('PageDown')]);
 await same('arrow while scrolled away returns to caret',[paste(lines(200)),K('Control+Home'),async p=>{await p.mouse.move(600,400);await p.mouse.wheel(0,3000);await p.waitForTimeout(100);},K('ArrowDown'),'X'],[paste(lines(200)),K('Control+Home'),K('ArrowDown'),'X']);
 await same('overtype replaces',['abcd',K('Home'),K('Insert'),'XY',K('Insert'),K('End')],['XYcd']);
 await same('overtype undo',['abcd',K('Home'),K('Insert'),'X',K('Control+z'),K('Insert'),K('End')],['abcd']);
 await diff('tab is not four spaces',['a',K('Tab'),'b'],['a    b']);
 await same('tab stops align',['a',K('Tab'),'X'],['aaa',K('Backspace'),K('Backspace'),K('Tab'),'X']);
 await same('tab backspace',['a',K('Tab'),K('Backspace'),'b'],['ab']);
 await same('shift enter backspace',['a',K('Shift+Enter'),K('Backspace'),'b'],['ab']);
 await diff('shift enter breaks without new paragraph',['a',K('Shift+Enter'),'b'],['a',K('Enter'),'b']);
 await same('shift enter arrow',['a',K('Shift+Enter'),'b',K('ArrowLeft'),K('ArrowLeft'),'X',K('End')],['aX',K('Shift+Enter'),'b',K('ArrowUp'),K('End')]);
 await same('grow font shortcut',['ab',K('Shift+ArrowLeft'),K('Control+]')],['ab',K('Shift+ArrowLeft'),K('Control+Shift+>')]);
 await diff('grow font changes',['ab',K('Shift+ArrowLeft'),K('Control+]')],['ab',K('Shift+ArrowLeft')]);
 await diff('ctrl m indents',['ab',K('Control+m')],['ab']);
 await same('ctrl m then shift undoes',['ab',K('Control+m'),K('Control+Shift+m')],['ab']);
 await diff('ctrl 2 double spaces',['ab',K('Enter'),'cd',K('Control+a'),K('Control+2')],['ab',K('Enter'),'cd',K('Control+a')]);
 await same('shift f3 upper',['abc def',K('Control+a'),K('Shift+F3'),K('End')],['ABC DEF']);
 await same('shift f3 lower',['abc def',K('Control+a'),K('Shift+F3'),K('Shift+F3'),K('End')],['abc def']);
 await same('shift f3 title',['abc def',K('Control+a'),K('Shift+F3'),K('Shift+F3'),K('Shift+F3'),K('End')],['Abc Def']);
 await same('shift f3 undo',['abc',K('Control+a'),K('Shift+F3'),K('Control+z'),K('End')],['abc']);
 await same('f3 finds next',['ab ab',K('Control+Home'),K('Control+f'),'ab',K('Enter'),K('Escape'),K('F3'),'X',K('End')],['ab X',K('End')]);
 await diff('find highlights all matches',['cat dog cat',K('Control+f'),'cat'],['cat dog dog',K('Control+f'),'cat']);
 await same('highlight goes when bar closes',['cat cat',K('Control+f'),'cat',K('Escape'),K('End')],['cat cat',K('End')]);
 // margin click selects the line, and a double click the paragraph
 await same('margin click selects line',['abc',K('Enter'),'def',click(260,296),K('Delete')],['abc',K('Enter'),'def',K('ArrowUp'),K('Home'),K('Shift+End'),K('Delete')]);
 // context menu
 const RC=(x,y)=>async p=>{await p.mouse.click(x,y,{button:'right'});};
 await diff('right click draws a menu',['abc',RC(400,400)],['abc']);
 await same('escape closes the menu',['abc',RC(400,400),K('Escape')],['abc',click(400,400)]);
 await same('menu select all then bold keeps selection',['abc',RC(330,296),K('ArrowDown'),K('ArrowDown'),K('ArrowDown'),K('ArrowDown'),K('Enter'),K('Delete'),'x'],['x']);
 await same('right click inside selection keeps it for bold',['abc def',K('Control+a'),RC(330,296),K('Escape'),K('Delete')],['']);
 // drag autoscroll
 await diff('drag below the page scrolls',[paste(lines(200)),K('Control+Home'),async p=>{await p.mouse.move(400,300);await p.mouse.down();await p.mouse.move(400,795);await p.waitForTimeout(800);await p.mouse.up();}],[paste(lines(200)),K('Control+Home'),async p=>{await p.mouse.move(400,300);await p.mouse.down();await p.mouse.move(400,700);await p.waitForTimeout(800);await p.mouse.up();}]);
 // files: tab and line break survive save, reopen and PDF
 if(!only||only==='file'){const A=await d();const p=A.p;await run(p,['a',K('Tab'),'b',K('Shift+Enter'),'c',K('Enter'),'d']);const i0=await shot(p);
  const [dl]=await Promise.all([p.waitForEvent('download'),p.keyboard.press('Control+s')]);await dl.saveAs('build/rv_tab.docx');
  const x=require('child_process').execSync(`python3 -c "import zipfile;print(zipfile.ZipFile('build/rv_tab.docx').read('word/document.xml').decode())"`).toString();const o1=x.includes('<w:tab/>')&&x.includes('<w:br/>');res.push(['docx has tab and br',o1]);console.log(o1?'PASS':'FAIL','docx has tab and br');
  const [dp]=await Promise.all([p.waitForEvent('download'),p.keyboard.press('Control+p')]);await dp.saveAs('build/rv_tab.pdf');const t=require('child_process').execSync('pdftotext -layout build/rv_tab.pdf -').toString();console.log(JSON.stringify(t.slice(0,60)));const o3=/a\s+b/.test(t)&&/c/.test(t);res.push(['pdf text',o3]);console.log(o3?'PASS':'FAIL','pdf text');await A.b.close();
  const B=await d();const f=fs.readFileSync('build/rv_tab.docx').toString('base64');await B.p.evaluate(async f=>{const u=Uint8Array.from(atob(f),c=>c.charCodeAt(0));await annOpen(new Blob([u]));},f);await B.p.waitForTimeout(3000);const i1=await shot(B.p);fs.writeFileSync('build/rv_reopen.png',i1);fs.writeFileSync('build/rv_before.png',i0);await B.b.close();}
 const ok=res.filter(r=>r[1]).length;console.log(`${ok}/${res.length} passed`);
})();
