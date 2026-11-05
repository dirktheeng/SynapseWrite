const d=require('./drive');(async()=>{const {b,p}=await d();
 const L='This paragraph exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.';
 const tk=async(l)=>console.log(l,await p.evaluate('annStats.ticks'));
 await p.evaluate(L=>annPaste(L+'\n'+L+'\n'+L),L);await tk('paste');
 for(let i=0;i<3;i++){await p.keyboard.type('x');await tk('type end 2-line');}
 await p.evaluate(()=>{let s='';for(let i=0;i<40;i++)s+='a\n';annPaste(s+'b b b')});await tk('paste more');
 for(let i=0;i<3;i++){await p.keyboard.type('x');await tk('type end short');}
 await p.evaluate(L=>annPaste('\n'+L),L);await tk('p');
 for(let i=0;i<3;i++){await p.keyboard.type('x');await tk('type end 2-line, scrolled');}
 await p.screenshot({path:'build/t8.png'});await b.close();})();
