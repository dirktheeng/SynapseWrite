// usage: node test/shot.js out.png 'js steps'  (steps run with p, K, T in scope)
const d=require('./drive');(async()=>{const {b,p}=await d();const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t),C=(x,y)=>p.mouse.click(x,y);
 await eval('(async()=>{'+process.argv[3]+'})()');await p.mouse.move(1270,5);await p.waitForTimeout(100);await p.screenshot({path:process.argv[2]});console.log(await p.evaluate('annStats'));await b.close();})();
