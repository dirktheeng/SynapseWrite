const fs=require('fs');const load=require('./load');
load().then(({e,h,bank})=>{const nm=JSON.parse(fs.readFileSync('build/names.json'));
 const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);return e.run(h.halt,80000000);};console.log(D(1));
 console.log('key',D(2,97));console.log(D(3,182,47,10),D(4,182,47));console.log('sh',D(3,1012,96,2000),D(4,1012,96));
 const v=k=>e.val(+Object.keys(nm).find(q=>nm[q]===k));console.log('sha',v('a4sha'),'qa4s',v('qa4s'),'fp',v('fp'));
 console.log('pdf',D(2,112,1),e.val(h.pdfout),'fp',v('fp'),'qp',v('qp'));
 console.log('again',D(6,0,0,1000),e.val(h.pdfout),'fp',v('fp'),'qp',v('qp'));
});
