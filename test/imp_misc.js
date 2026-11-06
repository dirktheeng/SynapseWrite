// Item checks, driven by events, judged on images and clipboard.
const d=require('./drive');const fs=require('fs');const R=[];const ok=(n,c,x)=>{R.push(!!c);console.log(c?'PASS':'FAIL',n,x===undefined?'':x);};
const shot=async(p,n)=>{await p.mouse.move(1270,5);await p.waitForTimeout(60);const b=await p.screenshot();if(n)fs.writeFileSync('build/imp_'+n+'.png',b);return b.toString('base64');};
(async()=>{
 {const {b,p}=await d();await p.keyboard.press('Control+f');await p.keyboard.type('abc');await p.keyboard.press('Escape');await p.keyboard.press('Control+f');await p.keyboard.type('xy');const a=await shot(p,'find');await b.close();
  const B=await d();await B.p.keyboard.press('Control+f');await B.p.keyboard.type('xy');const c=await shot(B.p);await B.b.close();ok('reopened find field: typing replaces the old text',a===c);}
 {const {b,p}=await d();await p.evaluate(()=>annOpen(new Blob([new Uint8Array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])])));await p.waitForTimeout(200);const a=await shot(p,'refuse');await b.close();
  const B=await d();const c=await shot(B.p);await B.b.close();ok('refused file changes the status bar',a!==c);}
 {const {b,p}=await d();await p.keyboard.type('One');await p.keyboard.press('Enter');await p.keyboard.type('Two');await p.keyboard.press('Enter');await p.keyboard.type('Three');await p.keyboard.press('Control+a');await shot(p,'sel');await b.close();}
 console.log(R.every(x=>x)?'ALL PASS':'FAILED');process.exit(0);
})();
