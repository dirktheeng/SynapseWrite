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
 await p.screenshot({path:'build/t4.png'});fs.writeFileSync('build/latency.json',JSON.stringify(out,null,0));await b.close();})();
