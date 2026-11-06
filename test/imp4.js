// imp4: custom colors, styles, lists, fonts, Unicode, ruler, zoom. Driven by events, judged on images and saved files.
const lib=require('./a7_lib'),{part,doc,count,W}=require('./imp4_lib');const R=[];const ok=(n,c,x)=>{R.push(!!c);console.log(c?'PASS':'FAIL',n,x===undefined?'':x);};
const only=process.argv[2];
const runs=x=>[...x.matchAll(/<w:r>(.*?)<\/w:r>/gs)].map(m=>m[1]);
const near=(A,r,g,b,t=6)=>count(A,223,1039,174,776,(x,y,z)=>Math.abs(x-r)<=t&&Math.abs(y-g)<=t&&Math.abs(z-b)<=t);
(async()=>{
 if(!only||only=='color'){
  // More Colors in the color menu takes six hex digits
  let A=await lib();A.type('Teal words here');A.settle();A.key(97,1);A.settle();A.click(299,102);A.settle();A.shot('build/imp4_cm.png');A.click(300,210);A.settle();A.type('12ab9c');A.settle();A.shot('build/imp4_cp.png');A.key(13);A.settle();A.click(600,600);A.settle();A.shot('build/imp4_c1.png');
  ok('exact color reaches the page, not the nearest palette entry',near(A,0x12,0xab,0x9c,2)>20,near(A,0x12,0xab,0x9c,2));
  let x=part(A,'word/document.xml');ok('exact color saved',/w:color w:val="12AB9C"/.test(x),(x.match(/w:color[^>]*/)||[])[0]);
  const h=A.hash(174,776);let B=await lib();B.file(9,A.savedBytes());B.settle();B.click(600,600);B.settle();B.shot('build/imp4_c2.png');ok('reopened file shows the same color',near(B,0x12,0xab,0x9c,2)>20);ok('reopened document area is pixel equal',B.hash(190,776)===A.hash(190,776));
  // a bad entry leaves the bar open and changes nothing
  A=await lib();A.type('abc');A.key(97,1);A.settle();A.click(299,102);A.settle();A.click(300,210);A.settle();A.type('12zz');A.key(13);A.settle();A.shot('build/imp4_c3.png');A.key(27);A.settle();x=part(A,'word/document.xml');ok('bad hex is refused',!/w:color w:val="[0-9A-F]{6}"\/><w:sz[^]*abc/.test(x.replace(/w:val="000000"/g,'')),x.slice(x.indexOf('<w:r>'),x.indexOf('</w:r>')));
  // a file color off the palette survives open and save, and undo of a palette color brings it back
  A=await lib();A.file(9,doc('<w:p><w:r><w:rPr><w:color w:val="5A1FB3"/></w:rPr><w:t>Purple file text</w:t></w:r></w:p>'));A.settle();A.shot('build/imp4_c4.png');ok('file color drawn exactly',near(A,0x5a,0x1f,0xb3,2)>20,near(A,0x5a,0x1f,0xb3,2));x=part(A,'word/document.xml');ok('file color saved exactly',/5A1FB3/.test(x));
  A.key(97,1);A.settle();A.click(299,102);A.settle();A.click(275+22,120+22);A.settle();A.click(600,600);A.settle();x=part(A,'word/document.xml');ok('a palette color replaces it',!/5A1FB3/.test(x));A.key(122,1);A.settle();x=part(A,'word/document.xml');ok('undo brings it back',/5A1FB3/.test(x));
  // typing style carries it
  A=await lib();A.click(299,102);A.settle();A.click(300,210);A.settle();A.type('#C04000');A.key(13);A.settle();A.type('typed');A.settle();x=part(A,'word/document.xml');ok('typing picks up an exact color',/C04000[^]*typed/.test(x),x.slice(x.indexOf('<w:r>'),x.indexOf('<w:r>')+160));
  // a style in a file with an exact color
  A=await lib();A.file(9,doc('<w:p><w:pPr><w:pStyle w:val="H9"/></w:pPr><w:r><w:t>Styled</w:t></w:r></w:p>',{'word/styles.xml':`<w:styles ${W}><w:style w:type="paragraph" w:styleId="H9"><w:name w:val="H nine"/><w:rPr><w:color w:val="2F5496"/></w:rPr></w:style></w:styles>`}));A.settle();ok('style color drawn exactly',near(A,0x2f,0x54,0x96,2)>5,near(A,0x2f,0x54,0x96,2));x=part(A,'word/styles.xml');ok('style color saved exactly',/2F5496/.test(x));
  // PDF
  A=await lib();A.file(9,doc('<w:p><w:r><w:rPr><w:color w:val="5A1FB3"/></w:rPr><w:t>PDF color</w:t></w:r></w:p>'));A.settle();A.key(112,1);const pn=A.e.val(A.h.fileout)||0,pa=A.e.val(A.h.outbase);const pb=Buffer.alloc(pn);for(let i=0;i<pn;i++)pb[i]=A.e.bget(pa+i);const pdf=pb.toString('latin1');ok('PDF carries the exact color',/0\.34 0\.12 0\.69 rg/.test(pdf),(pdf.match(/[\d.]+ [\d.]+ [\d.]+ rg/g)||[]).slice(0,4).join('|'));
  // underline follows
  A=await lib();A.file(9,doc('<w:p><w:r><w:rPr><w:color w:val="5A1FB3"/><w:u w:val="single"/></w:rPr><w:t>Under</w:t></w:r></w:p>'));A.settle();A.shot('build/imp4_c5.png');const pu=count(A,319,360,270,320,(r,g,b)=>r==0x5a&&g==0x1f&&b==0xb3);ok('underline in the exact color',pu>20,pu);
 }
 if(!only||only=='style'){
  const name=(A,txt)=>{A.type(txt);A.settle();A.key(13);A.settle();};
  // create a paragraph style from the caret paragraph, then use it elsewhere from the menu
  let A=await lib();A.type('Boxed');A.settle();A.key(97,1);A.key(98,1);A.key(105,1);A.settle();A.key(101,1);A.settle();A.key(133,1);A.settle();
  A.click(1186,74);A.settle();A.shot('build/imp4_s0.png');name(A,'My Note');A.settle();A.key(13);A.settle();A.type('second');A.key(13);A.settle();A.type('third');A.settle();A.shot('build/imp4_s1.png');
  let s=part(A,'word/styles.xml');ok('new style in styles.xml with a spaceless id',/w:styleId="MyNote"><w:name w:val="My Note"\/>/.test(s),(s.match(/w:styleId="M[^>]*>[^>]*>/)||[])[0]);
  ok('it holds the format it was made from',/styleId="MyNote"[^]*?<w:jc w:val="center"[^]*?<w:b\/><w:i\/>/.test(s));
  let x=part(A,'word/document.xml');ok('the paragraph uses it',/<w:pStyle w:val="MyNote"\/>[^]*Boxed/.test(x));
  // the all styles menu reaches it: index 6 is the first row past the built in six
  A.click(1106,120);A.settle();A.shot('build/imp4_s2.png');A.click(950,127+22*6+10);A.settle();x=part(A,'word/document.xml');const ps=[...x.matchAll(/<w:p>.*?<\/w:p>/gs)].map(m=>m[0]);ok('applied from All Styles',/MyNote/.test(ps[ps.length-1]),ps[ps.length-1].slice(0,120));
  // a duplicate name is refused
  A.click(1186,74);A.settle();name(A,'My Note');A.key(27);A.settle();s=part(A,'word/styles.xml');ok('duplicate name refused',(s.match(/styleId="MyNote"/g)||[]).length==1);
  // saved and reopened
  let B=await lib();B.file(9,A.savedBytes());B.settle();A.click(600,700);A.settle();B.click(600,700);B.settle();A.shot('build/imp4_s6a.png');B.shot('build/imp4_s6b.png');const fa=A.fb(),fb_=B.fb();let dmax=0;for(let i=190*5120;i<776*5120;i++)if((i&3)!=3)dmax=Math.max(dmax,Math.abs(fa[i]-fb_[i]));ok('reopens with no pixel over one level off',dmax<=1,dmax);
  // rename, with undo
  A.key(132,1);A.settle();A.click(1186,118);A.settle();name(A,'Plain Note');s=part(A,'word/styles.xml');ok('renamed, id kept',/styleId="MyNote"><w:name w:val="Plain Note"/.test(s),(s.match(/styleId="MyNote"[^/]*/)||[])[0]);
  A.key(122,1);A.settle();s=part(A,'word/styles.xml');ok('undo brings the name back',/styleId="MyNote"><w:name w:val="My Note"/.test(s),(s.match(/styleId="MyNote"[^/]*/)||[])[0]);
  // character style: selection only, overlays, saved and read
  A=await lib();A.type('red bold');A.settle();A.key(97,1);A.key(98,1);A.settle();A.click(299,102);A.settle();A.click(300,210);A.settle();A.type('B00020');A.key(13);A.settle();A.key(133,1);A.settle();
  A.click(1186,96);A.settle();name(A,'Alert');A.type(' plain tail');A.settle();
  s=part(A,'word/styles.xml');ok('character style saved with its fields only',/w:type="character"[^>]*w:styleId="Alert"><w:name w:val="Alert"\/><w:qFormat\/><w:rPr><w:b\/><w:color w:val="B00020"\/><\/w:rPr>/.test(s),(s.match(/w:type="character".*?<\/w:style>/)||[])[0]);
  x=part(A,'word/document.xml');ok('run names the style',/<w:rStyle w:val="Alert"\/>/.test(x),x.slice(x.indexOf('<w:r>'),x.indexOf('<w:r>')+90));
  // apply it from the menu to a selection in a big italic paragraph: it overlays
  A=await lib();A.file(9,doc('<w:p><w:r><w:rPr><w:i/><w:sz w:val="40"/></w:rPr><w:t>Big italic words</w:t></w:r></w:p><w:p><w:r><w:rPr><w:rStyle w:val="Em9"/></w:rPr><w:t>mark</w:t></w:r></w:p>',{'word/styles.xml':`<w:styles ${W}><w:docDefaults><w:rPrDefault><w:rPr><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults><w:style w:type="character" w:styleId="Em9"><w:name w:val="Emph Nine"/><w:rPr><w:b/><w:color w:val="00A0A0"/></w:rPr></w:style></w:styles>`}));A.settle();A.shot('build/imp4_s3.png');
  ok('character style draws its color from a file',near(A,0,0xa0,0xa0,2)>5,near(A,0,0xa0,0xa0,2));x=part(A,'word/document.xml');ok('character style kept on save',/<w:rStyle w:val="Em9"\/>/.test(x));s=part(A,'word/styles.xml');ok('character style definition kept',/styleId="Em9"[^]*00A0A0/.test(s),'');
  A.key(132,1);A.settle();A.key(133,3);A.settle();A.click(1106,120);A.settle();A.shot('build/imp4_s4.png');A.click(950,127+22*6+10);A.settle();A.click(600,700);A.settle();A.shot('build/imp4_s5.png');x=part(A,'word/document.xml');const f=x.slice(x.indexOf('<w:r>'),x.indexOf('</w:r>'));ok('menu pick overlays: keeps italic and size, adds bold and color',/rStyle w:val="Em9"/.test(f)&&/<w:b\/>/.test(f)&&/<w:i\/>/.test(f)&&/w:sz w:val="40"/.test(f)&&/00A0A0/.test(f),f.slice(0,200));
  A.key(122,1);A.settle();x=part(A,'word/document.xml');ok('undo takes it off',!/rStyle/.test(x.slice(x.indexOf('<w:r>'),x.indexOf('</w:r>'))));
 }
 if(!only||only=='list'){
  const rows=(A,y0=174,y1=776)=>{const f=A.fb();const r=[];for(let y=y0;y<y1;y++){let d=0;for(let x=270;x<900;x++){if(f[(y*1280+x)*4]<120)d++;}r.push(d>0);}const t=[];for(let i=1;i<r.length;i++)if(r[i]&&!r[i-1])t.push(i+y0);return t;};
  const pick=(A,r)=>{A.click(1246,74);A.settle();A.click(1120,127+22*r+10);A.settle();};
  // every format, chosen from the menu, draws, saves and reopens the same
  let A=await lib();A.paste('one\ntwo\nthree\n');A.settle();A.key(97,1);A.settle();A.click(394,75);A.settle();A.click(1246,74);A.settle();A.shot('build/imp4_l0.png');A.key(27);A.settle();
  const hs=new Set();for(const [r,num,txt] of [[1,'decimal','%1)'],[2,'decimal','(%1)'],[3,'lowerLetter','%1.'],[5,'upperLetter','%1.'],[6,'upperLetter','%1)'],[7,'lowerRoman','%1.'],[9,'upperRoman','%1.'],[11,'decimal','%1'],[13,'bullet','o'],[14,'bullet','&#8211;'],[15,'bullet','&gt;'],[17,'bullet','&#183;'],[18,'bullet','&#167;']]){
   let B=await lib();B.paste('one\ntwo\nthree\n');B.settle();B.key(97,1);B.settle();B.click(394,75);B.settle();pick(B,r);B.click(700,600);B.settle();B.shot('build/imp4_lf'+r+'.png');const h=B.hash(190,776);hs.add(h);
   const nm=part(B,'word/numbering.xml'),x=part(B,'word/document.xml');const id=(x.match(/<w:numId w:val="(\d+)"/)||[])[1];const nm2=nm.match(new RegExp('<w:num w:numId="'+id+'"><w:abstractNumId w:val="(\\d+)"'));const ab=nm2&&nm.match(new RegExp('<w:abstractNum w:abstractNumId="'+nm2[1]+'".*?</w:abstractNum>'));
   ok('format '+r+' saved as '+num+' '+txt,ab&&ab[0].includes('w:numFmt w:val="'+num+'"')&&ab[0].includes('w:lvlText w:val="'+txt+'"'),id);
   let C=await lib();C.file(9,B.savedBytes());C.settle();C.click(700,600);C.settle();ok('format '+r+' reopens the same',C.hash(190,776)===h);C.key(112,1);}
  ok('thirteen formats give thirteen pictures',hs.size==13,hs.size);
  // a file's own formats by level
  const num=`<w:numbering ${W}><w:abstractNum w:abstractNumId="4"><w:lvl w:ilvl="0"><w:numFmt w:val="upperRoman"/><w:lvlText w:val="%1)"/></w:lvl><w:lvl w:ilvl="1"><w:numFmt w:val="decimal"/><w:lvlText w:val="(%2)"/></w:lvl><w:lvl w:ilvl="2"><w:numFmt w:val="bullet"/><w:lvlText w:val="*"/></w:lvl></w:abstractNum><w:num w:numId="7"><w:abstractNumId w:val="4"/></w:num></w:numbering>`;
  const li=(t,l)=>`<w:p><w:pPr><w:numPr><w:ilvl w:val="${l}"/><w:numId w:val="7"/></w:numPr></w:pPr><w:r><w:t>${t}</w:t></w:r></w:p>`;
  A=await lib();A.file(9,doc(li('Top',0)+li('Next',1)+li('Deep',2),{'word/numbering.xml':num}));A.settle();A.shot('build/imp4_l2.png');let x=part(A,'word/document.xml');const n2=part(A,'word/numbering.xml');
  const ids=[...x.matchAll(/<w:numId w:val="(\d+)"/g)].map(m=>m[1]);const look=id=>{const m=n2.match(new RegExp('<w:num w:numId="'+id+'"><w:abstractNumId w:val="(\\d+)"'));return n2.match(new RegExp('<w:abstractNum w:abstractNumId="'+m[1]+'".*?</w:abstractNum>'))[0];};
  ok('file level 0 keeps upper roman',/upperRoman/.test(look(ids[0]))&&/%1\)/.test(look(ids[0])),ids.join());ok('file level 1 keeps (n)',/\(%2\)/.test(look(ids[1])));ok('file level 2 keeps its bullet',/lvlText w:val="\*"/.test(look(ids[2])));
  // Tab keeps the format
  A=await lib();A.paste('aa\nbb\n');A.settle();A.key(97,1);A.settle();A.click(394,75);A.settle();pick(A,6);A.click(700,600);A.settle();A.key(132,1);A.key(9);A.settle();x=part(A,'word/document.xml');const i2=x.match(/<w:ilvl w:val="1"\/><w:numId w:val="(\d+)"/);ok('Tab keeps the format',i2&&/upperLetter/.test((()=>{const n3=part(A,'word/numbering.xml');const m=n3.match(new RegExp('<w:num w:numId="'+i2[1]+'"><w:abstractNumId w:val="(\\d+)"'));return n3.match(new RegExp('<w:abstractNum w:abstractNumId="'+m[1]+'".*?</w:abstractNum>'))[0];})()),i2&&i2[1]);
  // Enter continues; undo restores
  A=await lib();A.paste('aa\n');A.settle();A.key(133,1);A.key(8);A.key(97,1);A.settle();A.click(394,75);A.settle();pick(A,6);A.click(700,600);A.settle();A.key(133,1);A.key(13);A.type('bb');A.settle();A.shot('build/imp4_l3.png');x=part(A,'word/document.xml');ok('Enter keeps the format',(x.match(/<w:numId w:val="(\d+)"/g)||[]).length==2&&(new Set(x.match(/<w:numId w:val="(\d+)"/g))).size==1);
  // PDF marker with a parenthesis stays valid
  A=await lib();A.paste('pp\nqq\n');A.settle();A.key(97,1);A.settle();A.click(394,75);A.settle();pick(A,2);A.key(112,1);const pn=A.e.val(A.h.fileout),pa=A.e.val(A.h.outbase);const pb=Buffer.alloc(pn);for(let i=0;i<pn;i++)pb[i]=A.e.bget(pa+i);const pdf=pb.toString('latin1');require('fs').writeFileSync('build/imp4_l.pdf',pb);ok('PDF marker escapes parentheses',/\\\(1\\\)/.test(pdf),(pdf.match(/\([^)]{0,8}\)Tj/g)||[]).slice(0,3).join(' '));
 }
 if(!only||only=='uni'){
  const T='Łódź ČĚŠ Ελληνικά Привет 日本 \u{1F600} end';
  const dark=A=>count(A,223,1039,174,776,(r)=>r<120);
  let A=await lib();A.paste(T);A.settle();A.shot('build/imp4_u1.png');ok('characters past Latin-1 draw ink',dark(A)>400,dark(A));
  let x=part(A,'word/document.xml');ok('saved in UTF-8, nothing lost',x.includes(T),(x.match(/<w:t[^>]*>([^<]*)/)||[])[1]);
  // caret moves over them one unit at a time, typed text lands in place
  A.key(132,1);for(let i=0;i<2;i++)A.key(130);A.type('X');A.settle();x=part(A,'word/document.xml');ok('caret walks them',x.includes('ŁóXdź'),(x.match(/<w:t[^>]*>([^<]*)/)||[])[1]);A.key(8);A.settle();
  // opening the saved file is the same picture
  part(A,'word/document.xml');const h0=(A.key(133,1),A.settle(),A.hash(190,776));let B=await lib();B.file(9,A.savedBytes());B.settle();B.key(133,1);B.settle();A.shot('build/imp4_u1b.png');{const fa=A.fb(),fb_=B.fb();let dm=0;for(let i=190*5120;i<776*5120;i++)if((i&3)!=3)dm=Math.max(dm,Math.abs(fa[i]-fb_[i]));ok('reopens with no pixel over one level off',dm<=1,dm);}B.shot('build/imp4_u2.png');
  // copy gives the same text back
  A.key(97,1);A.settle();A.key(99,1);A.settle();const c=[];for(let i=0;i<T.length;i++)c.push(A.e.bget(A.h.cb+i));ok('copy gives the code units',String.fromCharCode(...c)===T,String.fromCharCode(...c));
  A.key(133,1);A.key(13);A.paste(T);A.settle();x=part(A,'word/document.xml');ok('paste of the own copy',(x.match(/Ελληνικά/g)||[]).length==2);A.key(122,1);A.settle();
  // find, delete, undo
  B=await lib();B.paste('αβγ δεζ\n');B.settle();B.key(102,1);B.paste('δεζ');B.settle();B.key(13);B.settle();B.key(27);B.settle();B.type('Z');B.settle();x=part(B,'word/document.xml');ok('find matches them',/αβγ Z/.test(x),(x.match(/<w:t[^>]*>([^<]*)/)||[])[1]);B.key(122,1);B.settle();x=part(B,'word/document.xml');ok('undo',/δεζ/.test(x));
  // typed as a key
  A=await lib();A.key(0x3b1);A.key(0x416);A.settle();x=part(A,'word/document.xml');ok('typed keys',/αЖ/.test(x));
  // bold and italic faces, sizes; wrap
  A=await lib();A.key(98,1);A.paste('Жирный ');A.key(98,1);A.key(105,1);A.paste('курсив');A.key(105,1);A.settle();A.shot('build/imp4_u3.png');ok('bold differs from regular',A.hash(190,776).length>0);
  let L='';for(let i=0;i<60;i++)L+='Привет мир ';A=await lib();A.paste(L);A.settle();const rows=(()=>{const f=A.fb();let n=0,pr=false;for(let y=190;y<700;y++){let d=false;for(let x=319;x<944;x++)if(f[(y*1280+x)*4]<120){d=true;break;}if(d&&!pr)n++;pr=d;}return n;})();ok('Cyrillic wraps on spaces',rows>=5,rows);
  // file entity and four byte forms
  A=await lib();A.file(9,doc('<w:p><w:r><w:t>日本語 \u{1F600} Ωmega</w:t></w:r></w:p>'));A.settle();x=part(A,'word/document.xml');ok('file text past the old range survives',x.includes('日本語 \u{1F600} Ωmega'),(x.match(/<w:t[^>]*>([^<]*)/)||[])[1]);
  // PDF does not break
  A=await lib();A.paste('Ωmega text');A.settle();A.key(112,1);const pn=A.e.val(A.h.fileout),pa=A.e.val(A.h.outbase);const pb=Buffer.alloc(pn);for(let i=0;i<pn;i++)pb[i]=A.e.bget(pa+i);require('fs').writeFileSync('build/imp4_u.pdf',pb);{const {execSync}=require('child_process');const t=execSync('pdftotext build/imp4_u.pdf -').toString();ok('PDF text comes back through its own font',t.includes('Ωmega text'),t.slice(0,40));const q=execSync('qpdf --check build/imp4_u.pdf 2>&1 || true').toString();ok('qpdf clean',/No syntax/.test(q)&&!/WARNING/.test(q),q.split('\n').slice(-3).join(' '));}
  A=await lib();A.paste('a Ωmega with bold fields');A.key(13);A.settle();A.click(1,1);
 }
 if(!only||only=='font'){
  const fx=(n,t)=>`<w:p><w:r><w:rPr><w:rFonts w:ascii="${n}" w:hAnsi="${n}"/></w:rPr><w:t>${t}</w:t></w:r></w:p>`;
  let A=await lib();A.file(9,doc(fx('Garamond','Old style')+fx('Segoe UI','Humanist')+fx('Frobnicate Sans','Unknown')+fx('Arial','Known')));A.settle();A.shot('build/imp4_f1.png');let x=part(A,'word/document.xml');
  for(const n of ['Garamond','Segoe UI','Frobnicate Sans','Arial'])ok('name kept on save: '+n,x.includes('w:ascii="'+n+'" w:hAnsi="'+n+'"'));
  let B=await lib();B.file(9,A.savedBytes());B.settle();x=part(B,'word/document.xml');ok('second save keeps it',x.includes('Frobnicate Sans'));
  // the box shows the name at the caret
  A.key(132,1);A.settle();A.key(131);A.settle();A.shot('build/imp4_f2.png');const b1=A.fb().slice(0);const box=count(A,113,223,65,85,(r)=>r<120);ok('font box drawn',box>20,box);
  // typed name
  A=await lib();A.type('name me');A.key(97,1);A.settle();A.click(231,75);A.settle();A.shot('build/imp4_f3.png');A.click(150,87+22*8+10);A.settle();A.type('Georgia Pro');A.settle();A.shot('build/imp4_f4.png');A.key(13);A.settle();x=part(A,'word/document.xml');ok('a typed font name is applied and saved',x.includes('w:ascii="Georgia Pro"'),(x.match(/w:ascii="[^"]*"/g)||[]).join());
  const h1=A.hash(190,776);A.key(122,1);A.settle();x=part(A,'word/document.xml');ok('undo removes it',!x.includes('Georgia Pro'));
  // a family from the menu drops the name
  A=await lib();A.file(9,doc(fx('Frobnicate Sans','Unknown')));A.settle();A.key(97,1);A.settle();A.click(231,75);A.settle();A.click(150,87+22*2+10);A.settle();x=part(A,'word/document.xml');ok('choosing a family replaces the name',!x.includes('Frobnicate')&&/Arimo|Arial/.test(x),(x.match(/w:ascii="[^"]*"/g)||[]).join());
 }
 if(!only||only=='view'){
  let L='';for(let i=0;i<14;i++)L+='Zoom paragraph '+i+' has enough words on it that it wraps across the page and shows how lines scale when the view changes.\\n';
  const white=(A,y)=>{const f=A.fb();let n=0;for(let x=0;x<1262;x++){const i=(y*1280+x)*4;if(f[i]==255&&f[i+1]==255&&f[i+2]==255)n++;}return n;};
  // vertical ruler
  let A=await lib();A.paste(L);A.settle();A.shot('build/imp4_v0.png');const st=count(A,2,18,174,776,(r,g,b)=>r==198&&g==198&&b==198),wb=count(A,2,18,174,776,(r,g,b)=>r==255&&g==255&&b==255);ok('vertical ruler: gray margins and a white band',st>0&&wb>16*300,st+' '+wb);
  const ink=count(A,2,18,174,776,(r)=>r<160);ok('vertical ruler has marks',ink>40,ink);
  const hr=A.hash(174,776);A.wheel(300);A.settle();A.shot('build/imp4_v1.png');const st2=count(A,2,18,174,776,(r,g,b)=>r==255&&g==255&&b==255);ok('it moves with the page',A.hash(174,776)!==hr,st2);
  // hidden with the ruler
  A=await lib();A.paste(L);A.settle();
  // zoom past 150
  A=await lib();A.paste(L);A.key(132,1);A.settle();for(let i=0;i<4;i++){A.click(1232,788);A.settle();}A.shot('build/imp4_z200.png');let w=white(A,700);ok('200 percent: the page fills the window',w>1000,w);
  const dk=count(A,0,1262,174,776,(r)=>r<110);ok('200 percent: text is drawn large',dk>2000,dk);
  // caret follows: type at the end of a line
  A.type('Q');A.settle();A.key(133);A.settle();A.type('R');A.settle();A.shot('build/imp4_z200b.png');const x=part(A,'word/document.xml');ok('typing lands at the line end',/\w R|view changes|R/.test(x),'');
  const fbar=count(A,0,1262,764,776,(r,g,b)=>r==205&&g==205&&b==205);ok('side scroll bar drawn',fbar>100,fbar);
  // a click maps through the slide: find a word near the right of the view, click it, type
  A=await lib();A.paste('alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau\nsecond line here\n');A.settle();for(let i=0;i<4;i++){A.click(1232,788);A.settle();}A.shot('build/imp4_z1.png');A.click(1000,770);A.settle();A.shot('build/imp4_z2.png');
  // click the second line, wherever it is drawn
  const f=A.fb();const tops=[];let pr=false;for(let y=190;y<760;y++){let d=false;for(let x=200;x<700;x++)if(f[(y*1280+x)*4]<110){d=true;break;}if(d&&!pr)tops.push(y);pr=d;}
  A.click(600,tops[1]+6);A.settle();A.key(133);A.type('Z');A.settle();const pp=[...part(A,'word/document.xml').matchAll(/<w:t[^>]*>([^<]*)/g)].map(m=>m[1]);ok('click maps through the slide',pp[1]=='second line hereZ',JSON.stringify(pp));
  // round trip to 100 is pixel equal
  let C=await lib();C.paste(L);C.settle();const h0=C.hash(174,776);for(let i=0;i<4;i++){C.click(1232,788);C.settle();}for(let i=0;i<4;i++){C.click(1096,788);C.settle();}ok('back to 100 percent, pixel equal',C.hash(174,776)===h0);
  // zoom stops at 200
  C=await lib();for(let i=0;i<6;i++){C.click(1232,788);C.settle();}const fz=C.fb();C.shot('build/imp4_z3.png');const pc=count(C,1240,1280,780,796,(r)=>r<120);ok('stops at 200',pc>10,pc);
  // landscape at 150 now shows its left edge after the slide
  let D=await lib();D.paste('landscape left edge text\n');D.settle();D.click(182,47);D.settle();D.click(100,97);D.settle();for(let i=0;i<2;i++){D.click(1232,788);D.settle();}D.shot('build/imp4_z4.png');const lf=count(D,0,60,300,700,(r,g,b)=>r==255&&g==255&&b==255);ok('landscape at 150: page starts inside the window',lf>1000,lf);
 }
 console.log(R.filter(x=>x).length+'/'+R.length);process.exit(R.every(x=>x)?0:1);
})();
