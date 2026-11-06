const d=require('./drive');const fs=require('fs');(async()=>{const {b,p}=await d();await p.evaluate(()=>{window.annMax=8000000});p.on('crash',()=>console.log('CRASH'));const out=[];
 let K='k3';const stat=async(l,k='k2')=>{const s=await p.evaluate('annStats');const v=Math.round((s[k]||0)*10)/10;out.push([l,v]);console.log(l,v,'ms','ticks',s['t'+k.slice(1)],'edges',s['e'+k.slice(1)]);};
 await p.evaluate(()=>{let s='';for(let i=0;i<1900;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';annPaste(s)});
 await stat('paste 1900 paragraphs','k8');
 await p.screenshot({path:'build/t4a.png'});
 for(let i=0;i<3;i++){await p.keyboard.type('x');await stat('type at end');}
 await p.mouse.move(600,400);await p.mouse.wheel(0,-600);await p.waitForTimeout(300);await stat('wheel','k6');
 await p.keyboard.press('Control+a');await stat('select all');
 await p.keyboard.press('ArrowLeft');await stat('jump to top');
 await p.keyboard.type('z');await stat('type at top');
 await p.keyboard.press('ArrowDown');await stat('down');
 await p.keyboard.press('Enter');await stat('enter at top of long doc');
 await p.keyboard.press('Control+z');await stat('undo enter');
 await p.screenshot({path:'build/t4.png'});
 // cold paint: a page of text in a font and size no glyph has been drawn in, so every glyph goes through the generator
 {const q=await b.newPage({viewport:{width:1280,height:800}});await q.goto('file://'+require('path').resolve(__dirname,'../build/index.html'));await q.waitForFunction('window.annReady',{timeout:120000});await q.evaluate(()=>{window.annMax=60000000});
  await q.evaluate(()=>{let s='';for(let i=0;i<30;i++)s+='The quick brown fox jumps over the lazy dog, then packs five dozen liquor jugs and vexes a sphinx. 0123456789\n';annPaste(s)});
  const cold=async(l,r,sz)=>{await q.keyboard.press('Control+a');await q.mouse.click(229,75);await q.mouse.click(170,98+r*22);let ms=await q.evaluate(()=>Math.max(annStats.k3||0,annStats.k4||0,annStats.k2||0));out.push([l,Math.round(ms*10)/10]);console.log(l,Math.round(ms*10)/10,'ms');};
  await cold('cold page, new family at 11 pt',2);await cold('cold page, another new family at 11 pt',3);await cold('cold page, script family at 11 pt',7);
  await q.keyboard.press('Control+a');await q.mouse.click(258,75);await q.keyboard.type('36');await q.keyboard.press('Enter');const m36=await q.evaluate(()=>annStats.k2);out.push(['cold page, 36 pt',Math.round(m36*10)/10]);console.log('cold page, 36 pt',m36);await q.close();}
 fs.writeFileSync('build/latency.json',JSON.stringify(out,null,0));console.log('wasm MB',await p.evaluate(()=>annMem()/1e6));await b.close();})();
