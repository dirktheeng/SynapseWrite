const d=require('./drive');(async()=>{for(const [n,extra] of [[200,''],[950,''],[1000,''],[1800,''],[1900,''],[1800,'\n']]){const {b,p}=await d();
 await p.evaluate(([n,ex])=>{let s='';for(let i=0;i<n;i++)s+='Paragraph '+i+' exists to make a long document that spans many pages so we can measure how the network behaves at that scale with line breaking.\n';annPaste(s+ex)},[n,extra]);
 const r=[];for(let i=0;i<4;i++){await p.keyboard.type('x');r.push(await p.evaluate('annStats.ticks'));}
 await p.keyboard.press('Backspace');r.push('bk',await p.evaluate('annStats.ticks'));
 for(let i=0;i<30;i++)await p.keyboard.press('ArrowUp');r.push('up30',await p.evaluate('annStats.ticks'));
 await p.keyboard.type('y');r.push(await p.evaluate('annStats.ticks'));await p.keyboard.type('y');r.push(await p.evaluate('annStats.ticks'));
 console.log(n,JSON.stringify(r));await b.close();}})();
