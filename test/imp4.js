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
  A=await lib();A.file(9,doc('<w:p><w:pPr><w:pStyle w:val="H9"/></w:pPr><w:r><w:t>Styled</w:t></w:r></w:p>',{'word/styles.xml':`<w:styles ${W}><w:style w:type="paragraph" w:styleId="H9"><w:name w:val="H nine"/><w:rPr><w:color w:val="2F5496"/></w:rPr></w:style></w:styles>`}));A.settle();ok('style color drawn exactly',near(A,0x2f,0x54,0x96,2)>10,near(A,0x2f,0x54,0x96,2));x=part(A,'word/styles.xml');ok('style color saved exactly',/2F5496/.test(x));
  // PDF
  A=await lib();A.file(9,doc('<w:p><w:r><w:rPr><w:color w:val="5A1FB3"/></w:rPr><w:t>PDF color</w:t></w:r></w:p>'));A.settle();A.key(112,1);A.settle();const pn=A.e.val(A.h.fileout)||0,pa=A.e.val(A.h.outbase);const pb=Buffer.alloc(pn);for(let i=0;i<pn;i++)pb[i]=A.e.bget(pa+i);const pdf=pb.toString('latin1');ok('PDF carries the exact color',/0\.34 0\.12 0\.69 rg/.test(pdf),(pdf.match(/[\d.]+ [\d.]+ [\d.]+ rg/g)||[]).slice(0,4).join('|'));
  // underline follows
  A=await lib();A.file(9,doc('<w:p><w:r><w:rPr><w:color w:val="5A1FB3"/><w:u w:val="single"/></w:rPr><w:t>Under</w:t></w:r></w:p>'));A.settle();A.shot('build/imp4_c5.png');const pu=count(A,319,360,270,320,(r,g,b)=>r==0x5a&&g==0x1f&&b==0xb3);ok('underline in the exact color',pu>20,pu);
 }
 console.log(R.filter(x=>x).length+'/'+R.length);process.exit(R.every(x=>x)?0:1);
})();
