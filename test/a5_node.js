// Opens files in node with no browser: ticks to the end of the open, or the running states if it does not end.
// Usage: node test/a5_node.js maxticks file.docx ...
const fs=require('fs');const load=require('./load');
(async()=>{const max=+process.argv[2];const st=JSON.parse(fs.readFileSync('build/states.json'));
 for(const f of process.argv.slice(3)){const {e,h,bank}=await load();const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);return e.run(h.halt,max);};D(1);
  const u=fs.readFileSync(f);const b=bank();for(let i=0;i<u.length;i++)b[h.file+i]=u[i];const E0=e.edges();const t0=Date.now();const n=D(9,0,0,u.length);
  const on=[];if(n>=max)for(const k in st)if(e.val(+k))on.push(st[k]);console.log(f.split('/').pop(),'bytes',u.length,'ticks',n,'edges',e.edges()-E0,'ms',Date.now()-t0,n>=max?'NOT FINISHED in '+on.join(','):'done');}
})();
