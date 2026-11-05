const d=require('./drive');(async()=>{const {b,p,check}=await d();const K=k=>p.keyboard.press(k);await p.keyboard.type('Body');
await p.mouse.click(262,47);await p.mouse.click(190,76);console.log(await check('fn'));await p.keyboard.type('ab');console.log(await check('ty'));await K('Enter');console.log(await check('en'));await p.screenshot({path:'build/dbg.png'});await b.close();})();
