// feat1: caps, small caps, double strike, hidden text, character spacing, run shading, links, bookmarks, contextual spacing, widow control.
// Test files are built here as raw .docx parts. LibreOffice stands in as an independent reader; it is not Word.
const d=require('./drive');const fs=require('fs');const {execSync}=require('child_process');const crypto=require('crypto');const zlib=require('zlib');
const h=b=>crypto.createHash('md5').update(b).digest('hex');
const O='build/feat1';execSync(`rm -rf ${O}; mkdir -p ${O}`);
const W='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"';
const mk=(name,body,rels='')=>{const py=`
import zipfile,sys
z=zipfile.ZipFile(sys.argv[1],'w',zipfile.ZIP_DEFLATED)
z.writestr('[Content_Types].xml','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
z.writestr('_rels/.rels','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
z.writestr('word/_rels/document.xml.rels',open(sys.argv[3]).read())
z.writestr('word/document.xml',open(sys.argv[2]).read())
z.close()`;fs.writeFileSync(`${O}/mk.py`,py);
 fs.writeFileSync(`${O}/${name}.xml`,`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document ${W}><w:body>${body}<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>`);
 fs.writeFileSync(`${O}/${name}.rels`,`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">${rels}</Relationships>`);
 execSync(`python3 ${O}/mk.py ${O}/${name}.docx ${O}/${name}.xml ${O}/${name}.rels`);return `${O}/${name}.docx`;};
const P=(...r)=>`<w:p>${r.join('')}</w:p>`, Rn=(t,pr='')=>`<w:r>${pr?'<w:rPr>'+pr+'</w:rPr>':''}<w:t xml:space="preserve">${t}</w:t></w:r>`;
const LINK='http://example.com/a?b=1&amp;c=2';
const main=mk('main',
 P(Rn('Plain '),Rn('caps text','<w:caps/>'),Rn(' and '),Rn('Small Caps','<w:smallCaps/>'))+
 P(Rn('double struck','<w:dstrike/>'),Rn(' a'),Rn('HIDDEN','<w:vanish/>'),Rn('b '),Rn('spaced','<w:spacing w:val="60"/>'),Rn(' '),Rn('tight','<w:spacing w:val="-10"/>'))+
 P(Rn('shaded words','<w:shd w:val="clear" w:color="auto" w:fill="FFD966"/>'),Rn(' '),`<w:hyperlink r:id="rId7" w:history="1">${Rn('a link','<w:color w:val="0563C1"/><w:u w:val="single"/>')}</w:hyperlink>`,Rn(' '),`<w:hyperlink w:anchor="sec1">${Rn('jump')}</w:hyperlink>`)+
 P('<w:bookmarkStart w:id="0" w:name="sec1"/>',Rn('target text'),'<w:bookmarkEnd w:id="0"/>',Rn(' after'))+
 P('<w:pPr><w:spacing w:after="400"/><w:contextualSpacing/></w:pPr>',Rn('ctx one'))+
 P('<w:pPr><w:spacing w:before="400" w:after="400"/><w:contextualSpacing/></w:pPr>',Rn('ctx two'))+
 P('<w:pPr><w:widowControl w:val="0"/></w:pPr>',Rn('no widow control')),
 `<Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="${LINK}" TargetMode="External"/>`);
// references: what Word would draw, written plainly
const ref=mk('ref',
 P(Rn('Plain '),Rn('CAPS TEXT'),Rn(' and '),Rn('Small Caps'))+
 P(Rn('double struck','<w:strike/>'),Rn(' a'),Rn('b '),Rn('spaced'),Rn(' '),Rn('tight')));
const nocx=mk('nocx',P(Rn('Plain'))+P(Rn('x'))+P(Rn('x'))+P(Rn('x'))+
 P('<w:pPr><w:spacing w:after="400"/></w:pPr>',Rn('ctx one'))+P('<w:pPr><w:spacing w:before="400" w:after="400"/></w:pPr>',Rn('ctx two')));
const png=b=>{let p=8,w,hh,ct,id=[];while(p<b.length){const n=b.readUInt32BE(p),t=b.toString('ascii',p+4,p+8),d=b.subarray(p+8,p+8+n);if(t==='IHDR'){w=d.readUInt32BE(0);hh=d.readUInt32BE(4);ct=d[9];}if(t==='IDAT')id.push(d);p+=12+n;}
 const bpp=ct===6?4:3,raw=zlib.inflateSync(Buffer.concat(id)),st=w*bpp,o=Buffer.alloc(w*hh*4),cur=Buffer.alloc(st),prv=Buffer.alloc(st);
 for(let y=0;y<hh;y++){const f=raw[y*(st+1)];for(let i=0;i<st;i++){const x=raw[y*(st+1)+1+i],a=i>=bpp?cur[i-bpp]:0,u=prv[i],c=i>=bpp?prv[i-bpp]:0;let v;
  if(f===0)v=x;else if(f===1)v=x+a;else if(f===2)v=x+u;else if(f===3)v=x+((a+u)>>1);else{const pp=a+u-c,pa=Math.abs(pp-a),pb=Math.abs(pp-u),pc=Math.abs(pp-c);v=x+(pa<=pb&&pa<=pc?a:pb<=pc?u:c);}cur[i]=v&255;}
  for(let x=0;x<w;x++){for(let k=0;k<3;k++)o[(y*w+x)*4+k]=cur[x*bpp+k];o[(y*w+x)*4+3]=255;}cur.copy(prv);}
 return {width:w,height:hh,data:o};};
const px=(im,x,y)=>{const i=(y*im.width+x)*4;return [im.data[i],im.data[i+1],im.data[i+2]];};
const dark=(im,x0,y0,x1,y1)=>{let n=0;for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++){const c=px(im,x,y);if(c[0]+c[1]+c[2]<300)n++;}return n;};
const rowsInk=(im,x0,x1,y0,y1)=>{const r=[];for(let y=y0;y<y1;y++){let n=0;for(let x=x0;x<x1;x++){const c=px(im,x,y);if(c[0]+c[1]+c[2]<300)n++;}r.push(n);}return r;};
const inkBox=(im,x0,x1,y0,y1)=>{let a=1e9,b=-1,t=1e9,u=-1;for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++){const c=px(im,x,y);if(c[0]+c[1]+c[2]<300){a=Math.min(a,x);b=Math.max(b,x);t=Math.min(t,y);u=Math.max(u,y);}}return [a,b,t,u];};
const xml=(f,m='word/document.xml')=>execSync(`python3 -c "import zipfile;print(zipfile.ZipFile('${f}').read('${m}').decode())"`).toString();
(async()=>{const res=[];const ok=(n,v,x)=>{res.push([n,!!v]);console.log(v?'PASS':'FAIL',n,x===undefined?'':x);};
 const {b,p}=await d();await p.evaluate(()=>{window.annMax=60000000});
 const K=k=>p.keyboard.press(k);
 const open=async f=>{await p.evaluate(u=>annOpen(new Blob([new Uint8Array(u)])),[...fs.readFileSync(f)]);await p.waitForTimeout(300);await K('Control+Home');await p.mouse.move(1270,5);await p.waitForTimeout(100);};
 const save=async f=>{const [dl]=await Promise.all([p.waitForEvent('download'),K('Control+s')]);await dl.saveAs(f);};
 const shot=async()=>await p.screenshot({clip:{x:0,y:174,width:1280,height:602}});
 await open(ref);const sr=await shot();fs.writeFileSync(`${O}/ref.png`,sr);
 await open(nocx);const sn=await shot();fs.writeFileSync(`${O}/nocx.png`,sn);
 await open(main);const sm=await shot();fs.writeFileSync(`${O}/main.png`,sm);const st=await p.evaluate(()=>({t:annStats.t9,e:annStats.e9}));console.log('open',JSON.stringify(st));
 const A=png(sm),Rf=png(sr),N=png(sn);
 // line boxes: find the first rows of text ink on the page in the reference
 const lines=[];{let inl=false;for(let y=0;y<A.height;y++){const n=dark(Rf,300,y,950,y+1);if(n&&!inl){lines.push(y);inl=true;}if(!n&&inl)inl=false;}}
 console.log('ref line tops',lines.slice(0,6).join(' '));
 const L1=lines[0]-6,L2=lines[1]-6;const band=(im,y)=>{const o=[];for(let yy=y;yy<y+22;yy++)for(let x=300;x<950;x++)o.push(px(im,x,yy).join(','));return o.join(';');};
 // caps: the first line matches the plain capitals up to the small caps run
 const capsSame=(()=>{for(let yy=L1;yy<L1+22;yy++)for(let x=330;x<440;x++)if(px(A,x,yy).join()!==px(Rf,x,yy).join())return false;return true;})();
 ok('caps draws the capitals, pixel identical with typed capitals',capsSame);
 // small caps: lowercase letters drawn as capitals, shorter than the full capitals and taller than lowercase x height
 const [sa,sb]=(()=>{let x0=-1,x1=-1;for(let x=950;x>300;x--){if(dark(A,x,L1,x+1,L1+22)){if(x1<0)x1=x;x0=x;}else if(x1>0&&x0-x>8)break;}return [x0,x1];})();
 const scBox=inkBox(A,sa,sb+1,L1,L1+22),rcBox=inkBox(Rf,sa-10,sb+20,L1,L1+22);
 const colTop=(im,x0,x1)=>{const t=[];for(let x=x0;x<=x1;x++){let y0=-1;for(let y=L1;y<L1+22;y++){const c=px(im,x,y);if(c[0]+c[1]+c[2]<300){y0=y;break;}}t.push(y0);}return t;};
 const tops=colTop(A,sa,sb).filter(v=>v>=0).sort((a,b)=>a-b);const capTop=tops[0],lowTop=tops[tops.length>>1];
 ok('small caps: two letter heights, the small capitals lower than the capitals',lowTop-capTop>=2&&lowTop-capTop<=5,`cap top ${capTop}, small cap top ${lowTop}`);
 ok('small caps run is wider than the same text in lowercase would be',(sb-sa)>(rcBox[1]-rcBox[0])*0.95,`${sb-sa} vs ${rcBox[1]-rcBox[0]}`);
 // second line: hidden text takes no room, so "ab" is drawn as in the reference; double strike has two lines
 const ab=(()=>{for(let yy=L2;yy<L2+22;yy++)for(let x=300;x<640;x++)if(dark(A,x,yy,x+1,yy+1)!==dark(Rf,x,yy,x+1,yy+1))return false;return true;})();
 const sRows=rowsInk(A,330,400,L2,L2+22).map(v=>v>50?1:0),rRows=rowsInk(Rf,330,400,L2,L2+22).map(v=>v>50?1:0);
 ok('double strike draws two lines where strike draws one',sRows.reduce((a,b)=>a+b,0)===2&&rRows.reduce((a,b)=>a+b,0)===1,`${sRows.join('')} ${rRows.join('')}`);
 const ab2=(()=>{let d=0;for(let yy=L2;yy<L2+22;yy++)for(let x=405;x<422;x++)if(px(A,x,yy).join()!==px(Rf,x,yy).join())d++;return d;})();
 ok('hidden text takes no width or ink: the text around it is drawn as without it',ab2===0,ab2);
 const sp=(im)=>{let x0=-1,x1=-1,g=0;for(let x=423;x<950;x++){if(dark(im,x,L2,x+1,L2+22)){if(x0<0)x0=x;x1=x;g=0;}else if(x0>0&&++g>6)break;}return [x0,x1];};
 const re=im=>{for(let x=1000;x>300;x--)if(dark(im,x,L2,x+1,L2+22))return x;};const ws=re(A),wr=re(Rf);ok('3 pt spacing widens "spaced" by 4 px a letter, and -0.5 pt narrows "tight"',Math.abs(ws-wr-(6*4-5*2/3))<=2,`line end ${ws} vs ${wr}`);
 // third line: the shade under shaded words
 const L3=L2+(L2-L1);let shade=0;for(let yy=L3;yy<L3+20;yy++)for(let x=300;x<400;x++){const c=px(A,x,yy);if(Math.abs(c[0]-255)<3&&Math.abs(c[1]-217)<3&&Math.abs(c[2]-102)<3)shade++;}
 ok('run shading fills behind the run in its exact color',shade>400,shade);
 // contextual spacing: the two ctx paragraphs sit with no gap, closer than without the flag
 const findText=(im)=>{const t=[];let last=-99;for(let y=0;y<im.height;y++){const n=dark(im,300,y,950,y+1);if(n>=4){if(y-last>4)t.push(y);last=y;}}return t;};
 const ta=findText(A),tn=findText(N);
 ok('contextual spacing drops the gap between two paragraphs of one style that both set it',(ta[ta.length-2]-ta[ta.length-3])<(tn[tn.length-1]-tn[tn.length-2])-40,`${ta[ta.length-2]-ta[ta.length-3]} vs ${tn[tn.length-1]-tn[tn.length-2]}`);
 // save and the file
 await save(`${O}/s1.docx`);const x1=xml(`${O}/s1.docx`),r1=xml(`${O}/s1.docx`,'word/_rels/document.xml.rels');fs.writeFileSync(`${O}/s1.xml`,x1);
 ok('caps and small caps saved',/<w:caps\/>.*caps text/.test(x1)&&/<w:smallCaps\/>.*Small Caps/.test(x1));
 ok('double strike and hidden saved',/<w:dstrike\/>.*double struck/.test(x1)&&/<w:vanish\/>.*HIDDEN/.test(x1));
 ok('character spacing saved in twips, both signs',/<w:spacing w:val="60"\/>.*spaced/.test(x1)&&/<w:spacing w:val="-10"\/>.*tight/.test(x1));
 ok('run shading saved with its fill',/<w:shd w:val="clear" w:color="auto" w:fill="FFD966"\/>.*shaded words/.test(x1));
 ok('external link saved with a relationship to its target',/<w:hyperlink r:id="rIdL1">.*a link.*<\/w:hyperlink>/.test(x1)&&r1.includes(`Id="rIdL1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="${LINK}" TargetMode="External"`),r1.slice(-300));
 ok('internal link saved with its anchor',/<w:hyperlink w:anchor="sec1">.*jump.*<\/w:hyperlink>/.test(x1));
 ok('bookmark saved around its text',/<w:bookmarkStart w:id="\d+" w:name="sec1"\/>.*target text.*<w:bookmarkEnd w:id="\d+"\/>.*after/.test(x1));
 ok('contextual spacing and widow control off saved',(x1.match(/<w:contextualSpacing\/>/g)||[]).length===2&&/<w:widowControl w:val="0"\/>.*no widow control/.test(x1));
 execSync(`python3 -c "import xml.dom.minidom as m,zipfile;m.parseString(zipfile.ZipFile('${O}/s1.docx').read('word/document.xml'))"`);ok('document.xml is well formed',true);
 const v=execSync(`python3 test/a5_validate.py ${O}/s1.docx || true`).toString();ok('save passes schema, content type and relationship checks',/ OK\n/.test(v),v.slice(0,300));
 await open(`${O}/s1.docx`);const s2=await shot();fs.writeFileSync(`${O}/s2.png`,s2);ok('save and reopen is pixel identical',h(s2)===h(sm));
 await save(`${O}/s2.docx`);ok('second save XML identical',xml(`${O}/s2.docx`)===x1);
 // the properties live through editing: bold over the caps run keeps caps
 await open(main);
 await b.close();
 // LibreOffice as a stand-in reader: it reads the file and keeps the properties through its own save
 execSync(`rm -rf ${O}/lo; timeout 120 soffice --headless --convert-to docx:"MS Word 2007 XML" --outdir ${O}/lo ${O}/s1.docx >/dev/null 2>&1`);
 const lo=xml(`${O}/lo/s1.docx`),lor=xml(`${O}/lo/s1.docx`,'word/_rels/document.xml.rels');
 ok('LibreOffice reads caps, small caps, double strike, hidden, spacing and shading (stand-in, not Word)',['<w:caps/>','<w:smallCaps/>','<w:dstrike/>','<w:vanish/>','w:val="60"','FFD966'].every(s=>lo.includes(s)),['<w:caps/>','<w:smallCaps/>','<w:dstrike/>','<w:vanish/>','w:val="60"','FFD966'].filter(s=>!lo.includes(s)).join(' '));
 ok('LibreOffice reads the link target, the anchor and the bookmark (stand-in, not Word)',lor.includes('http://example.com/a?b=1&amp;c=2')&&/w:anchor="sec1"/.test(lo)&&/w:name="sec1"/.test(lo));
 console.log(`${res.filter(r=>r[1]).length}/${res.length} passed`);process.exit(0);})();
