const d=require('./drive');(async()=>{const {b,p}=await d();const fn=async t=>{await p.mouse.click(262,47);await p.mouse.click(190,76);await p.keyboard.type(t);await p.keyboard.press('Enter');await p.mouse.click(80,47);};
 await p.keyboard.type('A claim that needs a source');await fn('First source, 2026.');await p.keyboard.press('End');await p.keyboard.press('Enter');
 await p.keyboard.type('Another statement');await fn('Second note.');await p.keyboard.press('End');await p.keyboard.press('Enter');
 await p.evaluate(()=>{let s='';for(let i=0;i<45;i++)s+='Filler line '+i+'\n';annPaste(s)});await p.waitForTimeout(100);
 await p.mouse.move(600,400);await p.mouse.wheel(0,-5000);await p.waitForTimeout(100);await p.mouse.wheel(0,420);await p.waitForTimeout(150);await p.screenshot({path:'build/t15.png'});await b.close();})();
