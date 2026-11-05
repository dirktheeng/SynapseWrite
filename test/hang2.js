const d=require('./drive');const fs=require('fs');const st=JSON.parse(fs.readFileSync('build/states.json'));(async()=>{const {b,p}=await d();
 await p.evaluate(()=>{window.annMax=2000000});p.on('crash',()=>console.log('CRASH'));
 const act=async l=>{const r=await p.evaluate(st=>{const o=[];for(const k in st)if(annVal(+k))o.push(st[k]);return [annStats.ticks,annStats.events,o];},st);console.log(l,JSON.stringify(r));};
 const K=async k=>{await p.keyboard.press(k);await act(k);},T=async t=>{await p.keyboard.type(t);await act(t);};
 await T('Round');await p.mouse.click(660,88);await act('h1');await K('End');await K('Enter');await p.mouse.click(485,88);await act('normal');
 await T('Plain ');await K('Control+b');await T('bold');await K('Control+b');await K('Enter');
 await T('Serif text');await K('Shift+Home');await p.mouse.click(149,75);await act('font');await K('End');await K('Enter');
 await T('Red');await K('Shift+Home');await p.mouse.click(239,102);await act('red');await K('End');
 await b.close();})();
