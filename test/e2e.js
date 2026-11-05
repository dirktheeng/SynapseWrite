// End-to-end suite. Driven only by input events; judged only on output images and clipboard output.
// Most checks are metamorphic: two different event sequences must yield an identical image.
const d=require('./drive');const crypto=require('crypto');const fs=require('fs');
let results=[];
const N=s=>s; // no-op
async function fresh(){return await d();}
const shot=async(p)=>{await p.mouse.move(1270,5);return await p.screenshot({clip:{x:0,y:0,width:1280,height:800}});};
const hash=b=>crypto.createHash('md5').update(b).digest('hex');
const seq=async(p,steps)=>{for(const s of steps){if(typeof s==='function')await s(p);else if(s.startsWith('#'))await p.keyboard.press(s.slice(1));else await p.keyboard.type(s);}};
const key=k=>'#'+k;const click=(x,y)=>async p=>{await p.mouse.click(x,y);};
async function same(name,a,b){const A=await fresh();await seq(A.p,a);const ia=await shot(A.p);await A.b.close();const B=await fresh();await seq(B.p,b);const ib=await shot(B.p);await B.b.close();
 const ok=hash(ia)===hash(ib);results.push([name,ok]);console.log(ok?'PASS':'FAIL',name);if(!ok){fs.writeFileSync(`build/fail_a_${results.length}.png`,ia);fs.writeFileSync(`build/fail_b_${results.length}.png`,ib);}}
async function diff(name,a,b){const A=await fresh();await seq(A.p,a);const ia=await shot(A.p);await A.b.close();const B=await fresh();await seq(B.p,b);const ib=await shot(B.p);await B.b.close();
 const ok=hash(ia)!==hash(ib);results.push([name,ok]);console.log(ok?'PASS':'FAIL',name);}
const B=[120+11,102];const I=[146+11,102];const U=[172+11,102];
(async()=>{
 const only=process.argv[2];
 await same('typing and backspace',['abcx',key('Backspace')],['abc']);
 await same('left arrow then insert',['ac',key('ArrowLeft'),'b',key('End')],['abc']);
 await same('delete key',['abxc',key('ArrowLeft'),key('ArrowLeft'),key('Delete'),key('End')],['abc']);
 await same('enter then backspace merges',['ab',key('Enter'),key('Backspace'),'c'],['abc']);
 await same('undo',['abc',' def',key('Control+z')],['abc']);
 await same('undo enter',['abc',key('Enter'),key('Control+z')],['abc']);
 await same('undo then redo',['abc',' d',key('Control+z'),key('Control+y')],['abc d']);
 await same('select all and delete',['hello there',key('Control+a'),key('Delete'),'x'],['x']);
 await same('shift select and replace',['hello',key('Shift+ArrowLeft'),key('Shift+ArrowLeft'),'p'],['help']);
 await same('click places caret',['abc def',click(322,296),'X',key('End')],['aXbc def']);
 await same('drag selection deletes',['abcdef',async p=>{await p.mouse.move(322,296);await p.mouse.down();await p.mouse.move(345,296);await p.waitForTimeout(60);await p.mouse.up();},key('Delete'),key('End')],['aef']);
 await same('up then down round trip',['line one',key('Enter'),'line two',key('ArrowUp'),key('ArrowDown'),'!'],['line one',key('Enter'),'line two!']);
 await same('bold shortcut matches button',['ab',key('Shift+ArrowLeft'),key('Control+b')],['ab',key('Shift+ArrowLeft'),click(...B)]);
 await same('bold toggle returns',['ab',key('Shift+ArrowLeft'),key('Control+b'),key('Control+b')],['ab',key('Shift+ArrowLeft')]);
 await diff('bold changes pixels',['ab',key('Shift+ArrowLeft'),key('Control+b'),key('ArrowRight')],['ab']);
 await diff('italic changes pixels',['ab',key('Shift+ArrowLeft'),key('Control+i'),key('ArrowRight')],['ab']);
 await diff('underline changes pixels',['ab',key('Shift+ArrowLeft'),key('Control+u'),key('ArrowRight')],['ab']);
 await diff('center alignment changes pixels',['ab',key('Control+e')],['ab']);
 await same('align right button matches shortcut',['ab',key('Control+r')],['ab',click(308+2*30+10,102)]);
 await same('tab switch and back',['ab',click(135,47),click(80,47)],['ab']);
 await diff('tab content differs',[click(135,47)],[]);
 await same('wheel scroll returns',[...Array(60).fill(0).map(()=>'text line'+'\n'),async p=>{await p.mouse.move(600,400);await p.mouse.wheel(0,400);await p.waitForTimeout(100);await p.mouse.wheel(0,-400);await p.waitForTimeout(100);}],[...Array(60).fill(0).map(()=>'text line'+'\n')]);
 await same('paste equals typing',[async p=>{await p.evaluate(()=>annPaste('one two\nthree'));}],['one two',key('Enter'),'three']);
 await same('copy and paste',['abc',key('Control+a'),key('Control+c'),key('End'),async p=>{const t=await p.evaluate('annClip');await p.evaluate(x=>annPaste(x),t);}],['abcabc']);
 await same('cut removes',['abc',key('Control+a'),key('Control+x')],[]);
 await same('find selects match, then type replaces',['hello world',key('Control+f'),'world',key('Enter'),key('Escape'),'there'],['hello there']);
 await same('replace field',['aa bb aa',key('Home'),key('Control+h'),'aa',key('Tab'),'c',key('Enter'),key('Enter'),key('Escape'),key('End')],['c bb aa']);
 await same('style preset applies',['abc',click(660,88),key('Control+z'),key('End')],['abc']);
 await diff('heading differs',['abc',click(660,88)],['abc']);
 await diff('bullet list differs',['abc',click(330,75)],['abc']);
 await same('undo of format',['ab',key('Shift+ArrowLeft'),key('Control+b'),key('Control+z'),key('ArrowRight')],['ab']);
 await diff('manual page break',['a',key('Control+Enter'),'b'],['a',key('Enter'),'b']);
 await same('table tab moves to next cell',[click(135,47),click(116,76),click(80,47),'a',key('Tab'),'b'],[click(135,47),click(116,76),click(80,47),'a',key('Tab'),'b']);
 await diff('table differs from plain',[click(135,47),click(116,76),click(80,47),'a',key('Tab'),'b'],[click(80,47),'a',key('Enter'),'b']);
 await same('undo table',['x',click(135,47),click(116,76),click(80,47),key('Control+z'),key('End')],['x']);
 await same('enter in cell does nothing',[click(135,47),click(116,76),click(80,47),'a',key('Enter'),'b'],[click(135,47),click(116,76),click(80,47),'ab']);
 await diff('two columns differ',[...Array(3).fill('some words here '),click(160,47+0),click(132,76),click(80,47)],[...Array(3).fill('some words here ')]);
 await same('toc undo restores',['H',click(660,88),key('End'),key('Enter'),click(485,88),'body',key('Enter'),click(250,47),click(68,76),click(80,47),key('Control+z'),key('End')],['H',click(660,88),key('End'),key('Enter'),click(485,88),'body',key('Enter')]);
 await diff('header differs',[click(135,47),click(275,76),'Head',key('Enter'),click(80,47)],[click(135,47),click(80,47)]);
 await diff('comment shows balloon',['text',click(322,47),click(58,76),'note',key('Enter'),click(80,47)],['text',click(322,47),click(80,47)]);
 await same('comment backspace',['text',click(322,47),click(58,76),'nox',key('Backspace'),'te',key('Enter'),click(80,47)],['text',click(322,47),click(58,76),'note',key('Enter'),click(80,47)]);
 await diff('footnote shows on page',['text',click(262,47),click(190,76),'see',key('Enter'),click(80,47)],['text',click(262,47),click(80,47)]);
const cell=(r,c)=>click(880+c*26+8,64+r*22+8);const lay=(r,c)=>click(200+c*26+8,64+r*22+8);const tabL=click(192,47),tabH=click(80,47);
 const uni=t=>async p=>{for(const ch of t)await p.evaluate(c=>window.dispatchEvent(new KeyboardEvent('keydown',{key:c})),ch);};
 const paste=t=>async p=>{await p.evaluate(x=>annPaste(x),t);};
 await same('accented key equals paste',[uni('\u00e9\u00f1\u20ac')],[paste('\u00e9\u00f1\u20ac')]);
 await diff('accent changes the glyph',[uni('\u00e9')],['e']);
 await same('find folds Latin-1 case',[paste('\u00c9t\u00e9 x'),key('Home'),key('Control+f'),uni('\u00e9t'),key('Enter'),key('Escape'),'A'],[paste('A\u00e9 x')]);
 await same('backspace over an accent',[uni('a\u00e9'),key('Backspace')],['a']);
 await same('Ctrl+Home goes to the start',['ab',key('Enter'),'cd',key('Control+Home'),'X'],['Xab',key('Enter'),'cd',key('ArrowUp'),key('Home'),key('ArrowRight')]);
 await diff('strike changes pixels',['abc',key('Shift+Home'),cell(0,0),key('End')],['abc']);
 await same('strike toggles off',['abc',key('Shift+Home'),cell(0,0),cell(0,0),key('End')],['abc']);
 await same('superscript toggles off',['abc',key('Shift+Home'),cell(0,1),cell(0,1),key('End')],['abc']);
 await diff('superscript differs from subscript',['abc',key('Shift+Home'),cell(0,1),key('End')],['abc',key('Shift+Home'),cell(0,2),key('End')]);
 await same('sub replaces sup',['abc',key('Shift+Home'),cell(0,1),cell(0,2),key('End')],['abc',key('Shift+Home'),cell(0,2),key('End')]);
 await diff('highlight changes pixels',['abc',key('Shift+Home'),cell(0,6),key('End')],['abc']);
 await same('highlight none clears',['abc',key('Shift+Home'),cell(0,6),cell(0,5),key('End')],['abc']);
 await same('undo of highlight',['abc',key('Shift+Home'),cell(0,6),key('Control+z'),key('End')],['abc']);
 await diff('new colors differ',['abc',key('Shift+Home'),cell(1,1),key('End')],['abc',key('Shift+Home'),cell(2,1),key('End')]);
 await diff('left indent moves text',['abc',tabL,lay(0,1),tabH],['abc']);
 await same('left indent steps cancel',['abc',tabL,lay(0,1),lay(0,0),tabH],['abc']);
 await same('undo of indent',['abc',tabL,lay(0,1),tabH,key('Control+z'),key('End')],['abc']);
 await diff('line spacing moves the next line',['a',key('Enter'),'b',key('ArrowUp'),tabL,lay(0,11),tabH,key('End')],['a',key('Enter'),'b',key('ArrowUp'),key('End')]);
 await diff('space before moves text',['a',key('Enter'),'b',tabL,lay(0,5),tabH],['a',key('Enter'),'b']);
 await same('undo of alignment',['abc',key('Control+e'),key('Control+z'),key('End')],['abc']);
 await same('style undo restores paragraph spacing',['a',key('Enter'),'b',click(660,88),key('Control+z'),key('End')],['a',key('Enter'),'b']);
 await same('tab then shift tab returns list level',[click(330,75),'a',key('Enter'),key('Tab'),key('Shift+Tab'),'b'],[click(330,75),'a',key('Enter'),'b']);
 await diff('tab in a list item indents',[click(330,75),'a',key('Enter'),key('Tab'),'b'],[click(330,75),'a',key('Enter'),'b']);
 await same('backspace at list start removes the marker',[click(330,75),'a',key('Home'),key('Backspace'),key('End')],['a']);
 // kerning: same letters in a kerned order are narrower. The caret column finds the width.
 {const caret=async s=>{const A=await fresh();await A.p.keyboard.type(s);await A.p.mouse.move(1270,5);const png=await A.p.screenshot({clip:{x:319,y:280,width:400,height:30}});const {execSync}=require('child_process');fs.writeFileSync('build/k.png',png);const r=execSync(`python3 -c "from PIL import Image;im=Image.open('build/k.png').convert('L');w,h=im.size;print(max(x for x in range(w) if all(im.getpixel((x,y))<40 for y in range(10,20))))"`).toString();await A.b.close();return +r;};
  const a=await caret('AVAVAVAVAVAV'),b=await caret('AAAAAAVVVVVV');const ok=a<b-2;results.push(['kerning narrows AV pairs',ok]);console.log(ok?'PASS':'FAIL','kerning narrows AV pairs',a,b);}
 // page break by volume
 await diff('pagination grows',[async p=>{await p.evaluate(()=>{let s='';for(let i=0;i<60;i++)s+='line\n';annPaste(s);});}],[async p=>{await p.evaluate(()=>{let s='';for(let i=0;i<20;i++)s+='line\n';annPaste(s);});}]);
 const ok=results.filter(r=>r[1]).length;console.log(`${ok}/${results.length} passed`);fs.writeFileSync('build/e2e.json',JSON.stringify(results,null,1));
})();
