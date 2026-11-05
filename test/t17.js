const d=require('./drive');const fs=require('fs');(async()=>{const {b,p}=await d();const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t);
 await p.evaluate(()=>{window.annMax=30000000});
 await T('Report (draft)');await p.mouse.click(660,88);await K('End');await K('Enter');await p.mouse.click(485,88);
 await T('Plain ');await K('Control+b');await T('bold');await K('Control+b');await T(' and ');await K('Control+i');await T('italic');await K('Control+i');await K('Enter');
 await p.evaluate(()=>{let s='';for(let i=0;i<40;i++)s+='Filler line '+i+'\n';annPaste(s)});await p.waitForTimeout(300);
 const [dl]=await Promise.all([p.waitForEvent('download'),K('Control+p')]);await dl.saveAs('build/out.pdf');console.log(await p.evaluate('annStats.ticks'));await b.close();})();
