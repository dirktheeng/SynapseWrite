const d=require('./drive');(async()=>{const {b,p}=await d();
 const tab=x=>p.mouse.click(x,47);
 await p.keyboard.type('Report');await p.mouse.click(660,88);await p.keyboard.press('End');await p.keyboard.press('Enter');await p.mouse.click(485,88);
 await p.keyboard.type('Intro text.');await p.keyboard.press('Enter');await p.keyboard.type('Results');await p.mouse.click(750,88);await p.keyboard.press('End');await p.keyboard.press('Enter');await p.mouse.click(485,88);
 await tab(135);await p.mouse.click(275,76);await p.keyboard.type('Quarterly header');await p.keyboard.press('Enter');
 await tab(262);await p.mouse.click(68,76);await tab(82);
 await p.waitForTimeout(100);await p.screenshot({path:'build/t10a.png'});
 await p.evaluate(()=>{let s='';for(let i=0;i<14;i++)s+='Column text flows down the left side of the page first and then continues in the right column before the next page begins. Paragraph '+i+'.\n';annPaste(s)});
 await tab(193);await p.mouse.click(132,76);await tab(82);await p.waitForTimeout(100);await p.screenshot({path:'build/t10b.png'});await b.close();})();
