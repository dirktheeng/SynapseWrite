const d=require('./drive');const fs=require('fs');const st=JSON.parse(fs.readFileSync('build/states.json'));(async()=>{const {b,p}=await d();
 await p.evaluate(()=>{window.annMax=4000000});p.on('crash',()=>console.log('CRASH'));p.on('console',m=>console.log('C',m.text().slice(0,200)));
 const act=async l=>{const r=await p.evaluate(st=>{const o=[];for(const k in st)if(annVal(+k))o.push(st[k]);return [annStats.ticks,annStats.events,o];},st);console.log(l,JSON.stringify(r));};
 await p.evaluate(()=>{setInterval(()=>console.log('tick',annStats.events,annStats.ticks,Math.round(annStats.ms)),1500)});await p.evaluate(()=>{let s='';for(let i=0;i<1900;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';setTimeout(()=>annPaste(s),10)});await p.waitForTimeout(45000);
 await act('paste');for(let i=0;i<8;i++){await p.waitForTimeout(150);await act('w'+i);}
 await p.keyboard.type('x');await act('x');
 await b.close();})().catch(e=>console.log('ERR',e.message.slice(0,100)));
