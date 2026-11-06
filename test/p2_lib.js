// p2 headless parts: events in through the engine, judged on framebuffers and saved files. Nothing is verified in real Word.
const lib=require('./a7_lib'),{part,doc,count,W}=require('./imp4_lib');
const runs=x=>[...x.matchAll(/<w:r>(.*?)<\/w:r>/gs)].map(m=>m[1]);
module.exports=async(ok,only)=>{
 if(!only||only=='cstyle'){
  // Update on a character style: the caret run's format becomes the style, and every run of the style takes it
  const sty=`<w:styles ${W}><w:docDefaults><w:rPrDefault><w:rPr><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults><w:style w:type="character" w:styleId="Em9"><w:name w:val="Emph Nine"/><w:rPr><w:b/></w:rPr></w:style></w:styles>`;
  const body='<w:p><w:r><w:t xml:space="preserve">alpha </w:t></w:r><w:r><w:rPr><w:rStyle w:val="Em9"/></w:rPr><w:t>mark</w:t></w:r></w:p><w:p><w:r><w:t xml:space="preserve">beta </w:t></w:r><w:r><w:rPr><w:rStyle w:val="Em9"/></w:rPr><w:t>mark</w:t></w:r><w:r><w:t xml:space="preserve"> tail</w:t></w:r></w:p>';
  let A=await lib();A.file(9,doc(body,{'word/styles.xml':sty}));A.settle();A.click(600,700);A.settle();const h0=A.hash();
  // select the first "mark" (End, then Shift+Left four times), make it italic and red, then put the caret in it and press Update
  A.key(132,1);A.key(133);for(let i=0;i<4;i++)A.key(128,2);A.key(105,1);A.settle();A.key(133);A.settle();
  A.click(1034,95);A.settle();A.click(600,700);A.settle();A.shot('build/p2/cstyle_upd.png');
  const s=part(A,'word/styles.xml'),x=part(A,'word/document.xml');const r=runs(x);
  const def=(s.match(/w:styleId="Em9".*?<\/w:style>/s)||[''])[0];
  ok('character style Update: the definition takes the caret format (bold and italic)',/<w:b\/>/.test(def)&&/<w:i\/>/.test(def),def);
  const m2=r.filter(t=>/Em9/.test(t));
  ok('every run of the style takes the new field: the second paragraph\'s run is italic too',m2.length==2&&m2.every(t=>/<w:i\/>/.test(t)&&/<w:b\/>/.test(t)),m2.join(' | '));
  ok('runs of no style are untouched',r.filter(t=>/tail|beta|alpha/.test(t)).every(t=>!/<w:i\/>|<w:b\/>/.test(t)),r.join(' | '));
  // reference: the same document written with bold italic runs draws the same page
  const ref=body.replace(/<w:rStyle w:val="Em9"\/>/g,'<w:rStyle w:val="Em9"/><w:i/>');
  let B=await lib();B.file(9,doc(ref,{'word/styles.xml':sty}));B.settle();B.click(600,700);B.settle();A.click(600,700);A.settle();
  ok('the page equals one written with the style italic',A.hash(190,776)===B.hash(190,776));
  A.key(122,1);A.settle();A.click(600,700);A.settle();const s2=part(A,'word/styles.xml'),x2=part(A,'word/document.xml');
  ok('one undo takes back the definition and the second run',!/<w:i\/>/.test((s2.match(/w:styleId="Em9".*?<\/w:style>/s)||[''])[0])&&runs(x2).filter(t=>/Em9/.test(t)&&/<w:i\/>/.test(t)).length==1,runs(x2).join(' | '));
 }
};
