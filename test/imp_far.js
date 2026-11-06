// Typing below the part the background has reached: the caret and the text show on that event, not when the background ends.
const lib=require('./a7_lib');const R=[];const ok=(n,c,x)=>{R.push(!!c);console.log(c?'PASS':'FAIL',n,x===undefined?'':x);};
const text=()=>{let s='';for(let i=0;i<1900;i++)s+='This paragraph number '+i+' exists and has some ordinary words in it.\n';return s;};
(async()=>{let A=await lib();A.paste(text());const h0=A.hash();const r=[];for(const ch of 'xyz'){const before=A.hash();const q=A.key(ch);r.push(q.ed);ok('key '+ch+' changes the screen at once',A.hash()!==before);}
 A.shot('build/imp_far1.png');console.log('edges',r);const f=A.fb();let dark=0;for(let y=174;y<776;y++)for(let x=223;x<1040;x++){const i=(y*1280+x)*4;if(f[i]<90&&f[i+1]<90&&f[i+2]<90)dark++;}ok('text on the screen',dark>50,dark);
 A.settle();const h1=A.hash();A.shot('build/imp_far2.png');
 let B=await lib();B.paste(text());B.settle();for(const ch of 'xyz')B.key(ch);B.settle();ok('the same image after the background ends as typing after it',h1===B.hash(),h1+' '+B.hash());
 console.log(R.every(x=>x)?'ALL PASS':'FAILED');process.exit(0);
})();
