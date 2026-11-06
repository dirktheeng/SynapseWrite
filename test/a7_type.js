// Typing right after a bulk operation: judged by edge counts and by the framebuffer once the background has finished.
const lib=require('./a7_lib');const R=[];const ok=(n,c,x)=>{R.push(!!c);console.log(c?'PASS':'FAIL',n,x===undefined?'':x);};
const text=()=>{let s='';for(let i=0;i<1900;i++)s+='This paragraph number '+i+' exists and has some ordinary words in it.\n';return s;};
const prep=async()=>{const A=await lib();A.paste(text());A.settle();return A;};
(async()=>{
 // the caret is at the end, under the viewport, when the background is still working
 let A=await prep();A.key(97,1);const b0=A.key(98,1);console.log('bold all edges',b0.ed);A.key(130);console.log('right edges');
 const t=[];for(const ch of 'xyz')t.push(A.key(ch).ed);console.log('type edges',t);
 ok('typing after a bulk op stays under 1 M edges a key',Math.max(...t)<1000000,t.join(' '));
 A.settle();const h1=A.hash();A.shot('build/a7_type1.png');
 let B=await prep();B.key(97,1);B.key(98,1);B.key(130);B.settle();for(const ch of 'xyz')B.key(ch);B.settle();const h2=B.hash();B.shot('build/a7_type2.png');
 ok('the same image as typing after the background finished',h1===h2,h1+' '+h2);
 console.log(R.every(x=>x)?'ALL PASS':'FAILED');process.exit(0);
})();
