const d=require('./drive');(async()=>{for(const n of [1030,1200,1400,1540,1560]){const {b,p}=await d();
 await p.evaluate(n=>{let s='';for(let i=0;i<n;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';annPaste(s)},n);
 const r=[];for(let i=0;i<2;i++){await p.keyboard.type('x');r.push(await p.evaluate('annStats.t2'));}
 await p.evaluate(()=>annPaste('abc def'));await p.keyboard.type('x');r.push('nonempty',await p.evaluate('annStats.t2'));await p.keyboard.type('x');r.push(await p.evaluate('annStats.t2'));
 await p.keyboard.press('Control+a');await p.keyboard.press('ArrowLeft');await p.keyboard.press('ArrowDown');await p.keyboard.type('z');r.push('top',await p.evaluate('annStats.t2'));await p.keyboard.type('z');r.push(await p.evaluate('annStats.t2'));
 await p.waitForTimeout(1500);await p.keyboard.type('z');r.push('wait',await p.evaluate('annStats.t2'));
 console.log(n,JSON.stringify(r));await b.close();}})();
