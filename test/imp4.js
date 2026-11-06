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
 console.log(R.filter(x=>x).length+'/'+R.length);process.exit(R.every(x=>x)?0:1);
})();
