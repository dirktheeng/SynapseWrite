const d=require('./drive');const fs=require('fs');(async()=>{const {b,p}=await d();await p.evaluate(()=>{window.annMax=30000000});
 const pic=async f=>{await p.evaluate(u=>annPic(new Blob([new Uint8Array(u)])),[...fs.readFileSync(f)]);await p.waitForTimeout(500);const s=await p.evaluate('annStats');console.log(f,'k10',Math.round(s.k10),'ticks',s.t10);};
 await p.keyboard.type('Picture below');await p.keyboard.press('Enter');await pic('build/p_rgb.png');await p.keyboard.type('after');await p.waitForTimeout(100);await p.screenshot({path:'build/t16.png'});
 await b.close();})();
