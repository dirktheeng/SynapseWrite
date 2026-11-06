// p3: PDF named destinations and outline from bookmarks, internal links; .docx run and paragraph properties; equation matrices and nesting.
// Test files are built here as raw .docx parts. LibreOffice stands in as an independent reader; it is not Word.
// Usage: node test/p3.js [pdf|docx|eq]
const d=require('./drive');const fs=require('fs');const {execSync}=require('child_process');const crypto=require('crypto');const zlib=require('zlib');
const only=process.argv[2];const hh=b=>crypto.createHash('md5').update(b).digest('hex');
const O='build/p3';execSync(`mkdir -p ${O}`);
const sh=c=>execSync(c,{maxBuffer:1<<26}).toString();
const W='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"';
const MK=`
import zipfile,sys
z=zipfile.ZipFile(sys.argv[1],'w',zipfile.ZIP_DEFLATED)
ct='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
extra=sys.argv[4:]
for i in range(0,len(extra),2): ct+='<Override PartName="/%s" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.%s+xml"/>'%(extra[i],extra[i].split('/')[-1][:-4])
z.writestr('[Content_Types].xml',ct+'</Types>')
z.writestr('_rels/.rels','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
z.writestr('word/_rels/document.xml.rels',open(sys.argv[3]).read())
z.writestr('word/document.xml',open(sys.argv[2]).read())
for i in range(0,len(extra),2): z.writestr(extra[i],open(extra[i+1]).read())
z.close()`;fs.writeFileSync(`${O}/mk.py`,MK);
const mk=(name,body,rels='',parts={})=>{
 fs.writeFileSync(`${O}/${name}.xml`,`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document ${W}><w:body>${body}<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>`);
 fs.writeFileSync(`${O}/${name}.rels`,`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">${rels}</Relationships>`);
 const ex=[];for(const k in parts){const f=`${O}/${name}_${k.replace(/\W/g,'_')}`;fs.writeFileSync(f,parts[k]);ex.push(k,f);}
 sh(`python3 ${O}/mk.py ${O}/${name}.docx ${O}/${name}.xml ${O}/${name}.rels ${ex.join(' ')}`);return `${O}/${name}.docx`;};
const P=(...r)=>`<w:p>${r.join('')}</w:p>`, Rn=(t,pr='')=>`<w:r>${pr?'<w:rPr>'+pr+'</w:rPr>':''}<w:t xml:space="preserve">${t}</w:t></w:r>`;
const BR='<w:r><w:br w:type="page"/></w:r>';
const png=b=>{let p=8,w,hg,ct,id=[];while(p<b.length){const n=b.readUInt32BE(p),t=b.toString('ascii',p+4,p+8),dd=b.subarray(p+8,p+8+n);if(t==='IHDR'){w=dd.readUInt32BE(0);hg=dd.readUInt32BE(4);ct=dd[9];}if(t==='IDAT')id.push(dd);p+=12+n;}
 const bpp=ct===6?4:3,raw=zlib.inflateSync(Buffer.concat(id)),st=w*bpp,o=Buffer.alloc(w*hg*4),cur=Buffer.alloc(st),prv=Buffer.alloc(st);
 for(let y=0;y<hg;y++){const f=raw[y*(st+1)];for(let i=0;i<st;i++){const x=raw[y*(st+1)+1+i],a=i>=bpp?cur[i-bpp]:0,u=prv[i],c=i>=bpp?prv[i-bpp]:0;let v;
  if(f===0)v=x;else if(f===1)v=x+a;else if(f===2)v=x+u;else if(f===3)v=x+((a+u)>>1);else{const pp=a+u-c,pa=Math.abs(pp-a),pb=Math.abs(pp-u),pc=Math.abs(pp-c);v=x+(pa<=pb&&pa<=pc?a:pb<=pc?u:c);}cur[i]=v&255;}
  for(let x=0;x<w;x++){for(let k=0;k<3;k++)o[(y*w+x)*4+k]=cur[x*bpp+k];o[(y*w+x)*4+3]=255;}cur.copy(prv);}
 return {width:w,height:hg,data:o};};
const px=(im,x,y)=>{const i=(y*im.width+x)*4;return [im.data[i],im.data[i+1],im.data[i+2]];};
const dark=(im,x0,y0,x1,y1)=>{let n=0;for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++){const c=px(im,x,y);if(c[0]+c[1]+c[2]<300)n++;}return n;};
const inkBox=(im,x0,x1,y0,y1)=>{let a=1e9,b=-1,t=1e9,u=-1;for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++){const c=px(im,x,y);if(c[0]+c[1]+c[2]<380){a=Math.min(a,x);b=Math.max(b,x);t=Math.min(t,y);u=Math.max(u,y);}}return [a,b,t,u];};
const xml=(f,m='word/document.xml')=>sh(`python3 -c "import zipfile;print(zipfile.ZipFile('${f}').read('${m}').decode())"`);
(async()=>{const res=[];const ok=(n,v,x)=>{res.push([n,!!v]);console.log(v?'PASS':'FAIL',n,x===undefined?'':x);};
 const {b,p}=await d();await p.evaluate(()=>{window.annMax=60000000});
 const K=k=>p.keyboard.press(k);
 const open=async f=>{await p.evaluate(u=>annOpen(new Blob([new Uint8Array(u)])),[...fs.readFileSync(f)]);await p.waitForTimeout(300);await K('Control+Home');await p.mouse.move(1270,5);await p.waitForTimeout(100);};
 const save=async f=>{const [dl]=await Promise.all([p.waitForEvent('download'),K('Control+s')]);await dl.saveAs(f);};
 const pdf=async f=>{const [dl]=await Promise.all([p.waitForEvent('download',{timeout:240000}),K('Control+p')]);await dl.saveAs(f);};
 const shot=async()=>await p.screenshot({clip:{x:0,y:174,width:1280,height:602}});
 if(!only||only==='pdf'){
  const LINK='http://example.com/x';
  const f=mk('bm',
   P(Rn('First page. '),`<w:hyperlink w:anchor="sec1">${Rn('go to section','<w:color w:val="0563C1"/><w:u w:val="single"/>')}</w:hyperlink>`,Rn(' and '),`<w:hyperlink w:anchor="Odd_name.2">${Rn('the odd one')}</w:hyperlink>`,Rn(' and '),`<w:hyperlink r:id="rId7">${Rn('outside')}</w:hyperlink>`)+
   P(BR)+P(Rn('Second page top line.'))+P(Rn('Line two. '),'<w:bookmarkStart w:id="0" w:name="sec1"/>',Rn('Section one text'),'<w:bookmarkEnd w:id="0"/>')+
   P('<w:bookmarkStart w:id="1" w:name="_Toc99"/>',Rn('hidden bookmark text'),'<w:bookmarkEnd w:id="1"/>')+
   P(BR)+P(Rn('Third page. '),'<w:bookmarkStart w:id="2" w:name="Odd_name.2"/>',Rn('odd target'),'<w:bookmarkEnd w:id="2"/>'),
   `<Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="${LINK}" TargetMode="External"/>`);
  await open(f);await pdf(`${O}/bm.pdf`);
  let qc;try{qc=sh(`qpdf --check ${O}/bm.pdf 2>&1`);}catch(e){qc=e.stdout.toString();}
  ok('qpdf finds no errors',/No syntax or stream encoding errors/.test(qc),qc.split('\n').slice(-3).join(' '));
  const py=`
import pypdf,json,sys
r=pypdf.PdfReader(sys.argv[1]); pg={p.indirect_reference.idnum:i+1 for i,p in enumerate(r.pages)}
dests={k.lstrip('/'):(pg.get(v.page.idnum if hasattr(v.page,'idnum') else v.page.indirect_reference.idnum),float(v.top)) for k,v in r.named_destinations.items()}
def walk(o,lv):
    out=[]
    for it in o:
        if isinstance(it,list): out+=walk(it,lv+1)
        else: out.append([it.title,lv,r.get_destination_page_number(it)+1])
    return out
links=[]
for i,p in enumerate(r.pages):
    for a in (p.get('/Annots') or []):
        a=a.get_object(); act=a.get('/A'); links.append([i+1,str(a.get('/Dest')),str(act.get('/URI')) if act else None,[float(x) for x in a['/Rect']]])
print(json.dumps({'dests':dests,'outline':walk(r.outline,0),'links':links,'pages':len(r.pages)}))`;
  fs.writeFileSync(`${O}/rd.py`,py);const R=JSON.parse(sh(`python3 ${O}/rd.py ${O}/bm.pdf`));console.log(JSON.stringify(R));
  ok('three pages',R.pages===3,R.pages);
  ok('each bookmark is a named destination on its page (pypdf)',R.dests.sec1&&R.dests.sec1[0]===2&&R.dests._Toc99&&R.dests._Toc99[0]===2&&R.dests['Odd_name.2']&&R.dests['Odd_name.2'][0]===3,JSON.stringify(R.dests));
  const pinf=sh(`pdfinfo -dests ${O}/bm.pdf`);ok('poppler lists the same destinations',/\b2 \[ XYZ[^\]]*\] "sec1"/.test(pinf)&&/\b3 \[ XYZ[^\]]*\] "Odd_name.2"/.test(pinf),pinf.split('\n').filter(l=>/XYZ/.test(l)).join(' | '));
  // the destination is at the bookmarked line: line two sits below the top line of page 2
  const top=R.dests.sec1?R.dests.sec1[1]:0;ok('destination top is the bookmarked line, below the first line of the page',top<792-72-10&&top>792-72-60,top);
  const pb=sh(`pdftotext -f 2 -l 2 -bbox ${O}/bm.pdf -`);const mw=pb.match(/yMin="([\d.]+)"[^>]*>Section</);ok('the line pdftotext finds "Section" on is the destination top within 4 pt',mw&&Math.abs((792-(+mw[1]))-top)<4,mw&&mw[1]);
  ok('outline lists visible bookmarks, not hidden ones',R.outline.some(o=>o[0]==='sec1'&&o[2]===2)&&R.outline.some(o=>o[0]==='Odd_name.2'&&o[2]===3)&&!R.outline.some(o=>o[0]==='_Toc99'),JSON.stringify(R.outline));
  const L=R.links;ok('internal links are link annotations to the named destination',L.some(l=>l[0]===1&&l[1]==='/sec1')&&L.some(l=>l[0]===1&&l[1]==='/Odd_name.2'),JSON.stringify(L));
  ok('the external link is still a URI action',L.some(l=>l[0]===1&&l[2]===LINK));
  // the link box covers the linked words
  const lb=sh(`pdftotext -f 1 -l 1 -bbox ${O}/bm.pdf -`);const g=lb.match(/xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">go</);const il=L.find(l=>l[1]==='/sec1');
  ok('the internal link box covers the word "go"',g&&il&&il[3][0]<=+g[1]+1&&il[3][2]>=+g[3]-1&&792-il[3][3]<=+g[2]+2&&792-il[3][1]>=+g[4]-2,JSON.stringify([g&&g.slice(1,5),il&&il[3]]));
 }
 if(!only||only==='docx'){
  // run properties: emboss, imprint, outline, shadow, character scale, language; paragraph outline level
  const f=mk('rp',
   P(Rn('Embossed','<w:emboss/>'),Rn(' '),Rn('Imprinted','<w:imprint/>'),Rn(' '),Rn('Outlined','<w:outline/>'),Rn(' '),Rn('Shadowed','<w:shadow/>'))+
   P(Rn('Wide scale','<w:w w:val="200"/>'),Rn(' '),Rn('Narrow scale','<w:w w:val="66"/>'),Rn(' plain'))+
   P(Rn('Deutsch','<w:lang w:val="de-DE"/>'),Rn(' '),Rn('English','<w:lang w:val="en-GB" w:eastAsia="ja-JP"/>'),Rn(' '),Rn('again German','<w:lang w:val="de-DE"/>'))+
   P('<w:pPr><w:outlineLvl w:val="2"/></w:pPr>',Rn('outline level three'))+
   P(Rn('Plain line')));
  await open(f);const s1b=await shot();fs.writeFileSync(`${O}/rp.png`,s1b);const s1=png(s1b);
  const st=await p.evaluate(()=>({t:annStats.t9,e:annStats.e9}));console.log('open',JSON.stringify(st));
  await save(`${O}/rp1.docx`);const x1=xml(`${O}/rp1.docx`);fs.writeFileSync(`${O}/rp1.xml`,x1);
  for(const [t,r] of [['Embossed','<w:emboss/>'],['Imprinted','<w:imprint/>'],['Outlined','<w:outline/>'],['Shadowed','<w:shadow/>'],['Wide scale','<w:w w:val="200"/>'],['Narrow scale','<w:w w:val="66"/>'],['Deutsch','<w:lang w:val="de-DE"/>'],['again German','<w:lang w:val="de-DE"/>'],['English','<w:lang w:val="en-GB" w:eastAsia="ja-JP"/>']]){
   const m=x1.match(new RegExp('<w:r><w:rPr>((?!</w:r>).)*'+t));ok(`${t} saved with ${r}`,m&&m[0].includes(r),m&&m[0]);}
  ok('outline level saved',/<w:outlineLvl w:val="2"\/>((?!<\/w:p>).)*outline level three/.test(x1));
  {const m=(x1.match(/<w:r>((?!<\/w:r>).)*Plain line/)||[''])[0];ok('a plain run gains none of these properties',m&&!/emboss|imprint|outline|shadow|<w:w |<w:lang/.test(m),m);}
  const v=sh(`python3 test/a5_validate.py ${O}/rp1.docx || true`);ok('save passes schema, content type and relationship checks',/ OK\n/.test(v),v.slice(0,300));
  await open(`${O}/rp1.docx`);const s2=await shot();ok('save and reopen is pixel identical',hh(s2)===hh(s1b));
  await save(`${O}/rp2.docx`);ok('second save XML identical',xml(`${O}/rp2.docx`)===x1);
  sh(`rm -rf ${O}/lo; timeout 120 soffice --headless --convert-to docx:"MS Word 2007 XML" --outdir ${O}/lo ${O}/rp1.docx >/dev/null 2>&1`);
  const lo=xml(`${O}/lo/rp1.docx`);const want=['<w:emboss/>','<w:imprint/>','<w:outline/>','<w:shadow/>','w:val="200"','w:val="66"','de-DE','en-GB'];
  ok('LibreOffice reads emboss, imprint, outline, shadow, scale and language (stand-in, not Word)',want.every(s=>lo.includes(s)),want.filter(s=>!lo.includes(s)).join(' '));
  ok('LibreOffice reads the outline level (stand-in, not Word)',/<w:outlineLvl w:val="2"\/>/.test(lo));
 }
 if(!only||only==='eq'){
  const C=(x,y)=>p.mouse.click(x,y),T=t=>p.keyboard.type(t),Wt=ms=>p.waitForTimeout(ms);
  const eqshot=async n=>{const f=`${O}/${n}.png`;await p.screenshot({clip:{x:223,y:150,width:816,height:300},path:f});return f;};
  const py=s=>sh(`python3 - <<'P'\n${s}\nP`).trim();
  const same=(a,b)=>+py(`from PIL import Image,ImageChops;b=ImageChops.difference(Image.open('${a}').convert('RGB'),Image.open('${b}').convert('RGB')).getbbox();print(0 if not b else b[2]-b[0])`)<=2;
  // cells of a matrix in a screenshot: ink row blocks between the two marker letters, and in each block the ink runs apart by 4 or more columns
  const cells=f=>JSON.parse(py(`from PIL import Image
im=Image.open('${f}').convert('L');w,h=im.size;p=im.load()
dk=lambda x,y:p[x,y]<160
cols=[x for x in range(w) if any(dk(x,y) for y in range(40,220))]
segs=[];
for x in cols:
  if segs and x-segs[-1][1]<=3: segs[-1][1]=x
  else: segs.append([x,x])
# the matrix lies between the first marker word and the last one
x0,x1=segs[0][1]+1,segs[-1][0]-1
rows=[y for y in range(30,220) if any(dk(x,y) for x in range(x0,x1+1))]
blk=[]
for y in rows:
  if blk and y-blk[-1][1]<=1: blk[-1][1]=y
  else: blk.append([y,y])
out=[]
for a,b in blk:
  xs=[x for x in range(x0,x1+1) if any(dk(x,y) for y in range(a,b+1))]
  r=[]
  for x in xs:
    if r and x-r[-1][1]<4: r[-1][1]=x
    else: r.append([x,x])
  out.append({'y':[a,b],'c':[(u+v)/2 for u,v in r]})
print(json.dumps({'box':[x0,x1],'rows':out}) if True else '')`.replace('from PIL','import json\nfrom PIL')));
  const LINE='M mat(a&bbb)(cc&d)(eee&f) z';
  await open(mk('blank',P(Rn(''))));   // a fresh document, whatever ran before
  await T(LINE);await C(135,47);await C(725,76);await C(80,47);await K('Control+Home');await K('End');await Wt(200);
  const s0=await eqshot('mat3');const x=xml(await (async()=>{await save(`${O}/m3.docx`);return `${O}/m3.docx`;})());fs.writeFileSync(`${O}/m3.xml`,x);
  const t_=s=>`<m:r><m:t xml:space="preserve">${s}</m:t></m:r>`;
  ok('a three row matrix is saved as m:m with three m:mr of two cells',x.includes(`<m:m><m:mr><m:e>${t_('a')}</m:e><m:e>${t_('bbb')}</m:e></m:mr><m:mr><m:e>${t_('cc')}</m:e><m:e>${t_('d')}</m:e></m:mr><m:mr><m:e>${t_('eee')}</m:e><m:e>${t_('f')}</m:e></m:mr></m:m>`),(x.match(/<m:m>.*<\/m:m>/)||[''])[0]);
  const c0=cells(s0);console.log(JSON.stringify(c0));const R0=c0.rows.filter(r=>r.y[1]-r.y[0]>=3);
  ok('three rows of ink, each of two cells',R0.length===3&&R0.every(r=>r.c.length===2),JSON.stringify(R0));
  const spread=k=>{const v=R0.map(r=>r.c[k]);return Math.max(...v)-Math.min(...v);};
  ok('cells of different widths are centred in their columns on screen (centres within 1.5 px)',R0.length===3&&spread(0)<=1.5&&spread(1)<=1.5,`${R0.length===3?spread(0):''} ${R0.length===3?spread(1):''}`);
  await open(`${O}/m3.docx`);await K('Control+Home');await K('End');await Wt(200);const s1=await eqshot('mat3_re');ok('saved and opened again, pixel identical',same(s0,s1));
  await pdf(`${O}/m3.pdf`);let qc;try{qc=sh(`qpdf --check ${O}/m3.pdf 2>&1`);}catch(e){qc=e.stdout.toString();}
  ok('PDF is clean for qpdf',/No syntax or stream encoding errors/.test(qc));
  const bb=sh(`pdftotext -bbox ${O}/m3.pdf -`);const wd={};for(const m of bb.matchAll(/xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</g))wd[m[5]]=wd[m[5]]||{cx:(+m[1]+ +m[3])/2,y:+m[2]};
  console.log(JSON.stringify(wd));const has=['a','bbb','cc','d','eee','f'].every(k=>wd[k]);
  ok('PDF prints every cell, in three rows',has&&wd.a.y<wd.cc.y&&wd.cc.y<wd.eee.y&&Math.abs(wd.a.y-wd.bbb.y)<1&&Math.abs(wd.eee.y-wd.f.y)<1);
  ok('PDF centres the cells in their columns (within 1 pt)',has&&Math.max(wd.a.cx,wd.cc.cx,wd.eee.cx)-Math.min(wd.a.cx,wd.cc.cx,wd.eee.cx)<=1&&Math.max(wd.bbb.cx,wd.d.cx,wd.f.cx)-Math.min(wd.bbb.cx,wd.d.cx,wd.f.cx)<=1);
  sh(`pdftoppm -r 96 -f 1 -l 1 -png ${O}/m3.pdf ${O}/m3p`);
  // a foreign file: a four row, three column matrix in OMML reads back with all rows
  const NS='xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"';const rr=t=>`<m:e><m:r><m:t>${t}</m:t></m:r></m:e>`;
  const om=`<m:oMath><m:m>${[['1','0','x'],['0','22','y'],['0','0','333'],['4','5','6']].map(r=>'<m:mr>'+r.map(rr).join('')+'</m:mr>').join('')}</m:m></m:oMath>`;
  const ff=mk('m4',P(Rn('Q '),om,Rn(' end')));await open(ff);await K('Control+Home');await K('End');await Wt(200);const s2=await eqshot('mat4');
  await save(`${O}/m4s.docx`);const x4=xml(`${O}/m4s.docx`);
  ok('a foreign four row, three column matrix keeps every row and cell',x4.includes(`<m:mr><m:e>${t_('0')}</m:e><m:e>${t_('22')}</m:e><m:e>${t_('y')}</m:e></m:mr>`)&&x4.includes(`<m:mr><m:e>${t_('4')}</m:e><m:e>${t_('5')}</m:e><m:e>${t_('6')}</m:e></m:mr></m:m>`)&&(x4.match(/<m:mr>/g)||[]).length===4,(x4.match(/<m:m>.*<\/m:m>/)||[''])[0]);
  const c4=cells(s2);const R4=c4.rows.filter(r=>r.y[1]-r.y[0]>=3);console.log(JSON.stringify(R4));
  ok('four rows drawn, three cells each, columns aligned',R4.length===4&&R4.every(r=>r.c.length===3)&&[0,1,2].every(k=>{const v=R4.map(r=>r.c[k]);return Math.max(...v)-Math.min(...v)<=1.5;}));
  const two=mk('m2',P(Rn('Q '),`<m:oMath><m:m><m:mr>${rr('a')+rr('b')}</m:mr><m:mr>${rr('c')+rr('d')}</m:mr></m:m></m:oMath>`,Rn(' end')));await open(two);await K('Control+Home');await K('End');await Wt(200);const h2=cells(await eqshot('mat2')),h4=c4;
  ok('a four row matrix makes its line taller than a two row one',(h4.rows.slice(-1)[0].y[1]-h4.rows[0].y[0])>(h2.rows.slice(-1)[0].y[1]-h2.rows[0].y[0])+20,JSON.stringify([h2.rows.map(r=>r.y),h4.rows.map(r=>r.y)]));
 }
 await b.close();
 console.log(`${res.filter(r=>r[1]).length}/${res.length} passed`);process.exit(0);})();
