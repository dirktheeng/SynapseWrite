const d=require('./drive');const fs=require('fs');const st=JSON.parse(fs.readFileSync('build/states.json'));(async()=>{const {b,p}=await d();
 await p.evaluate(()=>{window.annMax=4000000});
 const act=async l=>{const r=await p.evaluate(st=>{const o=[];for(const k in st)if(annVal(+k))o.push(st[k]);return [annStats.ticks,o];},st);console.log(l,JSON.stringify(r));};
 await p.keyboard.type('hello');await act('typed');
 await p.evaluate(()=>{let s='';for(let i=0;i<30;i++)s+='This paragraph '+i+'\n';annPaste(s)});await act('paste');
 await p.keyboard.type('x');await act('x');await p.keyboard.type('y');await act('y');
 await p.keyboard.press('Control+s');await p.waitForTimeout(200);await act('save');
 await b.close();})();
