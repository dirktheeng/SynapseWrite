// p2: formatting and layout gaps closed on branch p2. Each part is driven by events (opening a file, keys) and judged on images and saved files.
// Small capitals: a lowercase letter in a small caps run draws as a capital at 0.8 of the run's size, on screen and in PDF.
// Test files are built here as raw .docx parts. Nothing is verified in real Word.
const dr=require('./drive');const fs=require('fs');const {execSync}=require('child_process');
const sh=c=>execSync(c,{stdio:['ignore','pipe','pipe']}).toString();
const O='build/p2';execSync(`rm -rf ${O}; mkdir -p ${O}`);
const W_='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"';
const py=s=>sh(`python3 - <<'P'\n${s}\nP`).trim();
const mk=(name,body)=>{fs.writeFileSync(`${O}/${name}.xml`,`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document ${W_}><w:body>${body}<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>`);
 py(`import zipfile
z=zipfile.ZipFile('${O}/${name}.docx','w',zipfile.ZIP_DEFLATED)
z.writestr('[Content_Types].xml','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
z.writestr('_rels/.rels','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
z.writestr('word/document.xml',open('${O}/${name}.xml').read())
z.close()`);return `${O}/${name}.docx`;};
const P=(...r)=>`<w:p>${r.join('')}</w:p>`, Rn=(t,pr='')=>`<w:r>${pr?'<w:rPr>'+pr+'</w:rPr>':''}<w:t xml:space="preserve">${t}</w:t></w:r>`;
(async()=>{const res=[];const ok=(n,v,x)=>{res.push([n,!!v]);console.log(v?'PASS':'FAIL',n,x===undefined?'':x);};
 const A=await dr();await A.p.evaluate(()=>{window.annMax=60000000});const K=k=>A.p.keyboard.press(k),W=ms=>A.p.waitForTimeout(ms);
 const open=async f=>{await A.p.evaluate(async u=>{await annOpen(new Blob([new Uint8Array(u)]))},[...fs.readFileSync(f)]);await W(300);await K('Control+End');await A.p.mouse.move(1270,5);await W(100);};
 const pdf=async f=>{const [d]=await Promise.all([A.p.waitForEvent('download',{timeout:240000}),K('Control+p')]);await d.saveAs(f);};
 const clip={x:300,y:240,width:700,height:110};
 // 24 pt: the small capitals take 19 pt (24 x 0.8 = 19.2), so the run equals a capital at 24 pt followed by capitals at 19 pt
 const s24='<w:sz w:val="48"/>',s19='<w:sz w:val="38"/>';
 const smc=mk('smc',P(Rn('Small','<w:smallCaps/>'+s24),Rn(' end',s24)));
 const ref=mk('ref',P(Rn('S',s24),Rn('MALL',s19),Rn(' end',s24)));
 await open(ref);await A.p.screenshot({clip,path:`${O}/ref.png`});
 await open(smc);await A.p.screenshot({clip,path:`${O}/smc.png`});
 // column heights of the ink: capital S and the small capitals
 const box=f=>JSON.parse(py(`from PIL import Image
im=Image.open('${f}').convert('L');w,h=im.size;p=im.load()
xs=[x for x in range(w) if any(p[x,y]<128 for y in range(h))]
# the first word: columns up to the first gap of 8 or more
ws=[];g=[xs[0]]
for x in xs[1:]:
  if x-g[-1]>=8: ws.append(g);g=[x]
  else: g.append(x)
ws.append(g);a=[w for w in ws if len(w)>=3][0]   # a caret is one column
def top(x0,x1): return min(y for y in range(h) for x in range(x0,x1+1) if p[x,y]<128)
def bot(x0,x1): return max(y for y in range(h) for x in range(x0,x1+1) if p[x,y]<128)
print([top(a[0],a[0]+8),bot(a[0],a[0]+8),top(a[0]+18,a[-1]),bot(a[0]+18,a[-1]),a[0],a[-1]])`));
 const bs=box(`${O}/smc.png`),br=box(`${O}/ref.png`);
 const capH=bs[1]-bs[0],smH=bs[3]-bs[2];
 ok('small capitals are 0.8 of the capital height (24 pt run)',smH/capH>0.74&&smH/capH<0.86,`capital ${capH} px, small capital ${smH} px, ratio ${(smH/capH).toFixed(3)}`);
 ok('small caps run draws like a 24 pt capital beside 19 pt capitals: same heights and width within 2 px',Math.abs(bs[2]-br[2])<=1&&Math.abs(bs[3]-br[3])<=1&&Math.abs((bs[5]-bs[4])-(br[5]-br[4]))<=2,`${bs} vs ${br}`);
 await pdf(`${O}/smc.pdf`);sh(`qpdf --qdf --object-streams=disable ${O}/smc.pdf ${O}/smq.pdf`);const Q=fs.readFileSync(`${O}/smq.pdf`,'latin1');
 const tf=[...Q.matchAll(/\/F\w+ 0*([\d.]+) Tf[^(]*\(([^)]*)\)/g)].map(m=>[+m[1],m[2]]);
 const fS=tf.find(t=>t[1]==='S'),fM=tf.find(t=>t[1]==='MALL');
 ok('PDF prints the small capitals at 0.8 of the size: 19 pt beside 24 pt (32 and 25 px)',fS&&fM&&fS[0]===32&&fM[0]===25,JSON.stringify(tf));
 // further highlights in PDF: dark blue prints as its exact color, with automatic text in white
 const hl=mk('hl',P(Rn('plain '),Rn('dark blue words here','<w:highlight w:val="darkBlue"/>')));await open(hl);await pdf(`${O}/hl.pdf`);
 sh(`pdftoppm -r 96 -f 1 -l 1 -png ${O}/hl.pdf ${O}/hlp`);const HP=`${O}/`+fs.readdirSync(O).find(f=>/^hlp.*png$/.test(f));
 const hc=JSON.parse(py(`from PIL import Image
im=Image.open('${HP}').convert('RGB');w,h=im.size;p=im.load()
b=[(x,y) for y in range(h) for x in range(w) if abs(p[x,y][0]-0)<=3 and abs(p[x,y][1]-0)<=3 and abs(p[x,y][2]-128)<=3]
xs=[q[0] for q in b];ys=[q[1] for q in b]
wt=sum(1 for y in range(min(ys),max(ys)+1) for x in range(min(xs),max(xs)+1) if min(p[x,y])>235)
print([len(b),wt])`));
 ok('PDF prints the dark blue highlight in its exact color',hc[0]>500,hc);
 // lists in PDF: numbering goes on across a plain paragraph within one numId and restarts at a new one
 {const NUM='<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/></w:lvl></w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num><w:num w:numId="2"><w:abstractNumId w:val="0"/></w:num></w:numbering>';
  const L=(id,t)=>`<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="${id}"/></w:numPr></w:pPr><w:r><w:t>${t}</w:t></w:r></w:p>`;
  fs.writeFileSync(`${O}/num.xml`,NUM);const f=mk('lists',L(1,'one')+L(1,'two')+P(Rn('plain'))+L(1,'three')+P(Rn('plain again'))+L(2,'fresh'));
  py(`import zipfile
z=zipfile.ZipFile('${f}','a')
z.writestr('word/numbering.xml',open('${O}/num.xml').read())
z.close()`);
  await open(f);await pdf(`${O}/lists.pdf`);const t=sh(`pdftotext -layout ${O}/lists.pdf -`).replace(/\s+/g,' ');
  ok('PDF numbers 1, 2, 3 across the plain paragraph and 1 for the new numId',/1\. one 2\. two plain 3\. three plain again 1\. fresh/.test(t),t.slice(0,120));}
 await A.b.close();
 // the headless parts: character style update, based on styles, further highlights
 await require('./p2_lib')(ok,process.argv[2]);
 const nf=res.filter(r=>!r[1]).length;console.log(`${res.length-nf}/${res.length} passed`);process.exit(nf?1:0);})();
