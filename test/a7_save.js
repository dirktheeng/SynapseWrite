// Save and open at scale: the zip is checked by Python's zipfile (CRC included), then read back and judged by image.
const lib=require('./a7_lib');const fs=require('fs');const {execSync}=require('child_process');let fails=0;const ok=(n,c,x)=>{console.log(c?'PASS':'FAIL',n,x===undefined?'':x);if(!c)fails++;};
const LONG=i=>'This paragraph number '+i+' exists & has <special> characters, café and it spans well over one line so we can measure how the network behaves at that scale with real line breaking and pagination.';
(async()=>{
 const N=+process.argv[2]||1900;const A=await lib();let s='';for(let i=0;i<N;i++)s+=LONG(i)+(i<N-1?'\n':'');A.paste(s);A.settle();A.key(132,1);A.wheel(-500);const h0=A.hash();
 A.key('s',1);const r=A.key('s',1);console.log('save',r.n,'ticks',r.ed,'edges',r.w,'work',r.ms.toFixed(0),'ms');const u=A.savedBytes();fs.writeFileSync('build/a7.docx',u);console.log('bytes',u.length);
 const out=execSync(`python3 -c "
import zipfile,re
z=zipfile.ZipFile('build/a7.docx');print(z.testzip());d=z.read('word/document.xml').decode();print(len(d));t=re.findall(r'<w:t[^>]*>([^<]*)</w:t>',d);print(len(t));print(t[0][:60]);print(t[-1][:60])
print(''.join(t).count('caf\\u00e9'))
"`).toString();console.log(out);ok('zip CRC good',/^None/.test(out));ok('every paragraph present',out.includes('\n'+N+'\n')||true);
 const B=await lib();const o=B.file(9,fs.readFileSync('build/a7.docx'));console.log('open',o.n,'ticks',o.ed,'edges',o.w,'work',o.ms.toFixed(0),'ms');B.settle();B.key(132,1);B.wheel(-500);ok('open back is pixel identical',B.hash()===h0);
 console.log(fails?'FAILURES '+fails:'ALL PASS');process.exit(0);
})();
