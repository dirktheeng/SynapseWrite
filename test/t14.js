const d=require('./drive');(async()=>{const {b,p}=await d();
 await p.keyboard.type('This paragraph carries a review comment shown in the margin.');
 await p.mouse.click(322,47);await p.mouse.click(58,76);await p.keyboard.type('Please check this claim');await p.keyboard.press('Enter');
 await p.mouse.click(80,47);await p.waitForTimeout(100);await p.screenshot({path:'build/t14.png'});await b.close();})();
