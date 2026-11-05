const d=require('./drive');(async()=>{const {b,p}=await d();
 await p.keyboard.type('Report & <summary>');await p.mouse.click(660,88);await p.keyboard.press('End');await p.keyboard.press('Enter');await p.mouse.click(485,88);
 await p.keyboard.type('Plain then ');await p.keyboard.press('Control+b');await p.keyboard.type('bold');await p.keyboard.press('Control+b');await p.keyboard.type(' then ');await p.keyboard.press('Control+i');await p.keyboard.type('italic');await p.keyboard.press('Control+i');await p.keyboard.press('Enter');
 await p.keyboard.type('Centered');await p.keyboard.press('Control+e');
 const [dl]=await Promise.all([p.waitForEvent('download'),p.keyboard.press('Control+s')]);await dl.saveAs('build/out.docx');await b.close();})();
