const d=require('./drive');(async()=>{const {b,p}=await d();
 const dump=async()=>p.evaluate(()=>{const B=annBank();const out=[];for(let i=0;i<8;i++){const s=B[i];if(!s)break;const l=B[s+2048];let t='';for(let k=0;k<l;k++)t+=String.fromCharCode(B[s+k]);out.push([s,l,t,Array.from(B.slice(s+1024,s+1024+Math.min(l,6)))]);}return JSON.stringify(out)});
 await p.keyboard.type('abcdef');await p.keyboard.press('ArrowLeft');await p.keyboard.press('ArrowLeft');await p.keyboard.press('Enter');
 console.log(await dump());
 await p.keyboard.type('XY');console.log(await dump());
 await p.mouse.click(660,88);console.log(await dump());
 await p.screenshot({path:'build/t2.png'});await b.close();})();
