const d=require('./drive');const fs=require('fs');(async()=>{const {b,p}=await d();const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t);
 await T('The quick brwon fox is speling wrod correctly dont it\'s dogs\' 2nd');await K('Enter');await T('Second line teh');await K('Enter');
 await p.mouse.click(322,47);await p.waitForTimeout(100); fs.writeFileSync('build/q1.png',await p.screenshot());await b.close();})();
