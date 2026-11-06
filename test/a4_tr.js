const fs=require('fs');const load=require('./load');
load().then(({e,h,bank})=>{const st=JSON.parse(fs.readFileSync('build/states.json'));const ids=Object.keys(st).map(Number);
 const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);return e.run(h.halt,80000000);};D(1);
 D(2,97);D(3,182,47,10);D(4,182,47);const m=process.argv[2]||'';if(m.includes('b')){D(3,950,74,1000);D(4,950,74);}if(m.includes('s')){D(3,1012,96,2000);D(4,1012,96);}
 e.inject(h.ev[0],2);e.inject(h.ev[1],112);e.inject(h.ev[2],1);
 let prev=new Set();const last=[];let t=0;for(;t<3000000;t++){const n=e.run(h.halt,1);const f=ids.length&&t%1===0?null:null;if(e.val(h.halt)){break}
   if(t%1==0){const on=ids.filter(i=>e.val(i)>0.5).map(i=>st[i]);last.push(on.join('+'));if(last.length>70)last.shift();}
   if(t>400000)break;}
 console.log(t,'pdf',e.val(h.pdfout));const nm=JSON.parse(fs.readFileSync('build/names.json'));const vv=k=>e.val(+Object.keys(nm).find(q=>nm[q]===k));console.log(['qp','qlj','qnl','qo','qe','fp','qa4s','qa4b','a4gap','qsty','qfn','qbase'].map(k=>k+'='+vv(k)).join(' '));console.log(last.slice(-45).join(' '));const bb=bank();const f=e.val(+Object.keys(nm).find(q=>nm[q]==='fp'));let o='';for(let i=f-150;i<f;i++)o+=String.fromCharCode(bb[20000000+i]);console.log(JSON.stringify(o));
});
