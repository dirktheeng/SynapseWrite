// rv_a6: PDF highlight and bookmarks from headings. Driven by events, judged on the file.
const d=require('./drive');const fs=require('fs');const {execSync}=require('child_process');
const sh=c=>execSync(c,{stdio:['ignore','pipe','pipe']}).toString();
(async()=>{const res=[];const ok=(n,v,x)=>{res.push([n,!!v]);console.log(v?'PASS':'FAIL',n,x===undefined?'':x);};
 const {b,p}=await d();await p.evaluate(()=>{window.annMax=60000000});const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t),C=(x,y)=>p.mouse.click(x,y);
 const ids=JSON.parse(fs.readFileSync('build/ui_ids.json'));
 const gal=(i)=>C(545+i*84,95);
 await T('Chapter (One)');await gal(1);await K('End');await K('Enter');await gal(0);
 await T('Yellow marked words here');await K('Shift+Home');await C(880+6*26+8,72);await K('End');await K('Enter');
 await T('Section A');await gal(2);await K('End');await K('Enter');await gal(0);
 await p.evaluate(()=>{let s='';for(let i=0;i<60;i++)s+='Filler line number '+i+'.\n';annPaste(s)});await p.waitForTimeout(300);
 await T('Sub one');await gal(3);await K('End');await K('Enter');await gal(0);
 await T('Chapter Two');await gal(1);await K('End');await K('Enter');await gal(0);
 await T('Section B');await gal(2);await K('End');await K('Enter');await gal(0);
 await T('end');await p.waitForTimeout(200);
 await C(600,47);await p.mouse.wheel(0,-90000);await p.waitForTimeout(300);
 const [dl]=await Promise.all([p.waitForEvent('download'),K('Control+p')]);await dl.saveAs('build/a6.pdf');await b.close();
 let q;try{q=sh('qpdf --check build/a6.pdf 2>&1');}catch(e){q=e.stdout.toString();}ok('qpdf --check clean',/No syntax or stream encoding errors/.test(q)&&!/WARNING/.test(q),q.split('\n').slice(-3).join(' '));
 const o=sh(`python3 - <<'P'
import pypdf
r=pypdf.PdfReader('build/a6.pdf')
def w(l,d=0):
  for x in l:
    if isinstance(x,list): w(x,d+1)
    else: print(d,x.title,r.get_destination_page_number(x)+1,round(float(x.top)))
w(r.outline)
P`);console.log(o);
 const L=o.trim().split('\n').map(s=>s.split(' '));
 ok('outline tree nests by heading level',o.includes('0 Chapter (One) 1')&&/1 Section A 1/.test(o)&&/2 Sub one \d/.test(o)&&/0 Chapter Two \d/.test(o)&&/1 Section B \d/.test(o));
 ok('first heading points near the page top',/Chapter \(One\) 1 (7[0-9][0-9])/.test(o));
 sh('rm -f build/a6p-*; pdftoppm -r 96 -f 1 -l 1 -png build/a6.pdf build/a6p');
 const pf=fs.readdirSync('build').filter(f=>f.startsWith('a6p-'))[0];
 const r=sh(`python3 - <<'P'
from PIL import Image
a=Image.open('build/${pf}').convert('RGB');y=0;k=0
for j in range(a.height):
  for i in range(a.width):
    c=a.getpixel((i,j))
    if c[0]>240 and c[1]>240 and c[2]<40:y+=1
    if c[0]<60 and c[1]<60 and c[2]<60:k+=1
print(y,k)
P`).trim().split(' ').map(Number);ok('highlight is drawn and the text stays dark',r[0]>1000&&r[1]>500,r.join(','));
 console.log(res.filter(r=>r[1]).length+'/'+res.length+' passed');
})();
