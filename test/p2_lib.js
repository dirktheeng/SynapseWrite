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

 if(!only||only=='based'){
  // a character style based on another takes the fields its base sets, not only their values
  const sty=`<w:styles ${W}><w:docDefaults><w:rPrDefault><w:rPr><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults><w:style w:type="character" w:styleId="Base1"><w:name w:val="Base One"/><w:rPr><w:color w:val="00A0A0"/></w:rPr></w:style><w:style w:type="character" w:styleId="Kid1"><w:name w:val="Kid One"/><w:basedOn w:val="Base1"/><w:rPr><w:b/></w:rPr></w:style></w:styles>`;
  let A=await lib();A.file(9,doc('<w:p><w:r><w:t xml:space="preserve">plain </w:t></w:r><w:r><w:rPr><w:rStyle w:val="Kid1"/></w:rPr><w:t>child words here</w:t></w:r></w:p>',{'word/styles.xml':sty}));A.settle();A.click(600,700);A.settle();A.shot('build/p2/based.png');
  const n=count(A,223,1039,174,776,(r,g,b)=>Math.abs(r-0)<=2&&Math.abs(g-0xa0)<=2&&Math.abs(b-0xa0)<=2);
  ok('a run of a style based on a colored character style draws in the base color',n>20,n);
  const s=part(A,'word/styles.xml'),x=part(A,'word/document.xml');const d=(s.match(/w:styleId="Kid1".*?<\/w:style>/s)||[''])[0];
  ok('the child style is saved with its own and its base\'s fields',/<w:b\/>/.test(d)&&/00A0A0/.test(d),d);
  ok('the run is saved with the base color',/Kid1[^]*00A0A0[^]*child/.test(x),runs(x).join(' | '));
 }

 if(!only||only=='hl'){
  // Word's eight further highlight values: drawn in their colors, saved by name, read back the same
  const X=[['darkBlue',0,0,128],['darkCyan',0,128,128],['darkGreen',0,128,0],['darkMagenta',128,0,128],['darkRed',128,0,0],['darkYellow',128,128,0],['darkGray',128,128,128],['black',0,0,0]];
  const body=X.map(([n])=>`<w:p><w:r><w:t xml:space="preserve">plain </w:t></w:r><w:r><w:rPr><w:highlight w:val="${n}"/></w:rPr><w:t>marked ${n}</w:t></w:r></w:p>`).join('')+'<w:p><w:r><w:rPr><w:highlight w:val="yellow"/></w:rPr><w:t>yellow still</w:t></w:r></w:p>';
  let A=await lib();A.file(9,doc(body));A.settle();A.click(600,700);A.settle();A.shot('build/p2/hl.png');
  for(const [n,r,g,b] of X){const c=count(A,223,1039,174,776,(x,y,z)=>x==r&&y==g&&z==b);ok(`highlight ${n} draws its color (${r},${g},${b})`,c>300,c);}
  ok('yellow still draws',count(A,223,1039,174,776,(x,y,z)=>x==255&&y==255&&z==0)>300);
  const x=part(A,'word/document.xml');ok('all eight names saved',X.every(([n])=>new RegExp(`<w:highlight w:val="${n}"/>[^]*?marked ${n}`).test(x)),runs(x).filter(t=>/highlight/.test(t)).map(t=>t.match(/w:val="(\w+)"/)[1]).join(' '));
  ok('yellow saved',/w:val="yellow"\/>[^]*yellow still/.test(x));
  let B=await lib();B.file(9,A.savedBytes());B.settle();B.click(600,700);B.settle();ok('saved file reopens pixel identical',B.hash(190,776)===A.hash(190,776));
  // a ribbon highlight over a further one replaces it on screen and in the file: select the first marked run (the ab highlight button applies yellow)
  A.key(132,1);A.key(133);for(let i=0;i<15;i++)A.key(128,2);A.settle();A.click(314,101);A.settle();A.click(600,700);A.settle();
  {const z=part(A,'word/document.xml');const r0=runs(z).find(t=>/marked darkBlue/.test(t))||'';ok('a ribbon highlight over a further one is saved once',(r0.match(/<w:highlight/g)||[]).length==1&&!/darkBlue"/.test(r0),r0);}
  // spacing read before the highlight keeps both
  let C=await lib();C.file(9,doc('<w:p><w:r><w:rPr><w:caps/><w:spacing w:val="40"/><w:highlight w:val="darkRed"/></w:rPr><w:t>spaced</w:t></w:r></w:p>'));C.settle();const y=part(C,'word/document.xml');
  ok('caps, spacing and a further highlight together are kept',/<w:caps\/>/.test(y)&&/w:spacing w:val="40"/.test(y)&&/darkRed/.test(y),runs(y).join(' | '));
 }

 if(!only||only=='lists'){
  // numbering goes on across plain paragraphs within one numId and restarts at a new numId, as in Word
  const num=`<w:numbering ${W}><w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/></w:lvl></w:abstractNum><w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num><w:num w:numId="2"><w:abstractNumId w:val="0"/><w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num></w:numbering>`;
  const L=(id,t)=>`<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="${id}"/></w:numPr></w:pPr><w:r><w:t>${t}</w:t></w:r></w:p>`,Pp=t=>`<w:p><w:r><w:t>${t}</w:t></w:r></w:p>`;
  const body=L(1,'one')+L(1,'two')+Pp('a plain paragraph')+L(1,'three')+Pp('another plain one')+L(2,'new one')+L(2,'new two');
  // the reference draws the numbers Word would show as typed text with the same indents: 1 2 _ 3 _ 1 2
  let A=await lib();A.file(9,doc(body,{'word/numbering.xml':num}));A.settle();A.click(600,700);A.settle();A.shot('build/p2/lists.png');
  const x=part(A,'word/document.xml');const ids=[...x.matchAll(/<w:numId w:val="(\d+)"\/>/g)].map(m=>+m[1]);
  ok('saved: the interrupted list keeps one numId, the new list another',ids.length==5&&ids[0]==ids[1]&&ids[1]==ids[2]&&ids[3]==ids[4]&&ids[2]!=ids[3],ids.join(' '));
  const nx=part(A,'word/numbering.xml');const ov=id=>new RegExp(`<w:num w:numId="${id}">(?:(?!</w:num>).)*startOverride`).test(nx);
  ok('saved: the first list and the restarted list each start at 1, by override',ov(ids[0])&&ov(ids[3]),ids[0]+' '+ids[3]);
  // the markers on screen: each list line's marker is pixel equal to the marker of the same number in a plain five item list
  const lines=Z=>{const f=Z.fb(),t=[];let on=false;for(let y=180;y<700;y++){let n=0;for(let x=300;x<700;x++){const i=(y*1280+x)*4;if(f[i]<128)n++;}if(n&&!on){t.push(y);on=true;}if(!n)on=false;}return t;};
  const mk=(Z,y)=>{const f=Z.fb(),o=[];for(let yy=y-2;yy<y+14;yy++)for(let x=300;x<345;x++)o.push(f[(yy*1280+x)*4]>128?1:0);return o.join('');};
  let B=await lib();B.file(9,doc(L(1,'x').repeat(5),{'word/numbering.xml':num}));B.settle();B.click(600,700);B.settle();
  const la=lines(A),lb=lines(B),ref=[0,1,2,3,4].map(k=>mk(B,lb[k]));const got=[0,1,3,5,6].map(k=>ref.indexOf(mk(A,la[k]))+1);
  ok('screen numbers: 1 2, plain, 3, plain, then 1 2 again',got.join()=='1,2,3,1,2',got.join());
  // Restart at 1 from the List Style menu on the third item, then undo, then Continue Numbering on the restarted list
  const at=(Z,k)=>{Z.click(600,lines(Z)[k]+6);Z.settle();};
  at(A,3);A.click(1247,74);A.settle();A.shot('build/p2/lists_menu.png');A.click(1150,127+19*22+11);A.settle();A.click(600,700);A.settle();
  let g2=[0,1,3,5,6].map(k=>ref.indexOf(mk(A,lines(A)[k]))+1);ok('Restart at 1 on the third item numbers it 1',g2.join()=='1,2,1,1,2',g2.join());
  let x2=part(A,'word/document.xml');let id2=[...x2.matchAll(/<w:numId w:val="(\d+)"\/>/g)].map(m=>+m[1]);ok('saved: the restarted item opens its own numId',id2[2]!=id2[1]&&id2[2]!=id2[3],id2.join(' '));
  A.key(122,1);A.settle();A.click(600,700);A.settle();g2=[0,1,3,5,6].map(k=>ref.indexOf(mk(A,lines(A)[k]))+1);ok('undo brings back 3',g2.join()=='1,2,3,1,2',g2.join());
  at(A,5);A.click(1247,74);A.settle();A.click(1150,127+20*22+11);A.settle();A.click(600,700);A.settle();
  g2=[0,1,3,5,6].map(k=>ref.indexOf(mk(A,lines(A)[k]))+1);ok('Continue Numbering on the second list goes on from 3',g2.join()=='1,2,3,4,5',g2.join()+' '+[...part(A,'word/document.xml').matchAll(/<w:numId w:val="(\d+)"\/>/g)].map(m=>m[1]).join(' '));
  A.shot('build/p2/lists.png');
 }

 if(!only||only=='link'){
  // Link... from the right-click menu over a selection: the address becomes an external link, saved with a relationship, drawn underlined in the hyperlink blue; undo takes it off
  let A=await lib();A.type('see the site now');A.settle();A.key(132);for(let i=0;i<4;i++)A.key(130);for(let i=0;i<8;i++)A.key(130,2);A.settle();
  // right-click on the selection opens the context menu at the pointer; its last row, Link..., asks for the address
  A.move(362,297);A.e.inject(A.h.ev[5],16);A.raw(3,362,297,9000000);A.e.inject(A.h.ev[5],16);A.raw(4,362,297);A.settle();A.shot('build/p2/link_menu.png');
  A.click(420,297+8*22+11);A.settle();A.shot('build/p2/link_prompt.png');A.type('https://example.org/a?b=1');A.key(13);A.settle();A.click(600,700);A.settle();A.shot('build/p2/link.png');
  const x=part(A,'word/document.xml'),r=part(A,'word/_rels/document.xml.rels');
  const m=x.match(/<w:hyperlink r:id="([^"]+)"[^>]*>(.*?)<\/w:hyperlink>/s);
  ok('the selection is saved inside a hyperlink',m&&/the site/.test(m[2])&&!/see|now/.test(m[2]),m?m[2].slice(0,200):x.slice(0,300));
  ok('its relationship holds the address, external',m&&new RegExp(`Id="${m[1]}"[^>]*Target="https://example.org/a\\?b=1&amp;" TargetMode="External"|Id="${m[1]}"[^>]*Target="https://example.org/a\\?b=1" TargetMode="External"`).test(r),r.slice(-300));
  ok('the link text is underlined in 0563C1',m&&/<w:color w:val="0563C1"\/>/.test(m[2])&&/<w:u w:val="single"\/>/.test(m[2]));
  const blue=count(A,223,1039,174,776,(r_,g,b)=>r_==5&&g==99&&b==193);ok('drawn in the hyperlink blue',blue>40,blue);
  A.key(122,1);A.settle();const y=part(A,'word/document.xml');ok('undo takes the link off',!/<w:hyperlink/.test(y)&&!/0563C1/.test(y));
  // read back: the saved file opens with the link and draws the same
  A.key(121,1);A.settle();A.click(600,700);A.settle();const z=part(A,'word/document.xml');ok('redo brings the link back',/<w:hyperlink/.test(z));let B=await lib();B.file(9,A.savedBytes());B.settle();B.click(600,700);B.settle();
  A.shot('build/p2/link_a.png');B.shot('build/p2/link_b.png');ok('redo, save and reopen: pixel identical',B.hash(190,776)===A.hash(190,776));
 }

 if(!only||only=='follow'){
  // Ctrl+click on an internal link puts the caret at the start of its bookmark
  const body='<w:p><w:hyperlink w:anchor="far"><w:r><w:t>jump there</w:t></w:r></w:hyperlink></w:p>'+'<w:p><w:r><w:t>filler</w:t></w:r></w:p>'.repeat(3)+'<w:p><w:r><w:t xml:space="preserve">before </w:t></w:r><w:bookmarkStart w:id="0" w:name="far"/><w:r><w:t>target</w:t></w:r><w:bookmarkEnd w:id="0"/></w:p>';
  let A=await lib();A.file(9,doc(body));A.settle();A.click(600,700);A.settle();
  const f=A.fb();let y0=-1;for(let y=180;y<700&&y0<0;y++)for(let x=300;x<500;x++)if(f[(y*1280+x)*4]<128){y0=y;break;}
  A.e.inject(A.h.ev[5],1);A.raw(3,330,y0+6,9000000);A.e.inject(A.h.ev[5],1);A.raw(4,330,y0+6);A.settle();   // Ctrl held: bit 0 of the event modifier, as the glue sends it
  A.type('X');A.settle();
  const x=part(A,'word/document.xml');{const t=x.replace(/<[^>]+>/g,'');ok('Ctrl+click on the link: typing lands at the bookmark, the link text is untouched',t.includes('jump there')&&t.includes('before Xtarget'),t.slice(0,80));}
 }

 if(!only||only=='pstyle'){
  // a paragraph style that sets caps, small caps or character spacing: its runs take them, as in Word
  const sty=`<w:styles ${W}><w:docDefaults><w:rPrDefault><w:rPr><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults><w:style w:type="paragraph" w:styleId="Shout"><w:name w:val="Shout"/><w:rPr><w:caps/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Quiet"><w:name w:val="Quiet"/><w:basedOn w:val="Shout"/><w:rPr><w:spacing w:val="40"/></w:rPr></w:style></w:styles>`;
  const P_=(st,t)=>`<w:p><w:pPr><w:pStyle w:val="${st}"/></w:pPr><w:r><w:t>${t}</w:t></w:r></w:p>`;
  let A=await lib();A.file(9,doc(P_('Shout','make me big')+P_('Quiet','wide words'),{'word/styles.xml':sty}));A.settle();A.click(600,700);A.settle();A.shot('build/p2/pstyle.png');
  let B=await lib();B.file(9,doc(P_('Shout','MAKE ME BIG')+`<w:p><w:pPr><w:pStyle w:val="Quiet"/></w:pPr><w:r><w:rPr><w:caps/><w:spacing w:val="40"/></w:rPr><w:t>wide words</w:t></w:r></w:p>`,{'word/styles.xml':sty.replace('<w:rPr><w:caps/></w:rPr>','').replace('<w:rPr><w:spacing w:val="40"/></w:rPr>','')}));B.settle();B.click(600,700);B.settle();B.shot('build/p2/pstyle_ref.png');
  ok('a paragraph style with caps draws its runs in capitals, and a style based on it adds its spacing: pixel equal to direct formatting',A.hash(190,776)===B.hash(190,776));
  const x=part(A,'word/document.xml');ok('saved runs carry the caps and spacing',/<w:caps\/>[^]*make me big/.test(x)&&/<w:spacing w:val="40"\/>[^]*wide words/.test(x),runs(x).join(' | ').slice(0,300));
 }

 if(!only||only=='caps'){
  // All Caps and Small Caps from the right-click menu over a selection, toggled as Word does, with undo
  const rmenu=(Z,x,y,row)=>{Z.move(x,y);Z.e.inject(Z.h.ev[5],16);Z.raw(3,x,y,9000000);Z.e.inject(Z.h.ev[5],16);Z.raw(4,x,y);Z.settle();Z.click(x+60,y+row*22+11);Z.settle();};
  let A=await lib();A.type('see the site now');A.settle();A.key(132);for(let i=0;i<4;i++)A.key(130);for(let i=0;i<8;i++)A.key(130,2);A.settle();
  rmenu(A,362,297,10);A.click(600,700);A.settle();A.shot('build/p2/smc_menu.png');
  let x=part(A,'word/document.xml');{const rr=runs(x);ok('Small Caps from the menu: saved on the selected run only',rr.some(t=>/smallCaps/.test(t)&&/>the site</.test(t))&&rr.filter(t=>/smallCaps/.test(t)).every(t=>/>the site</.test(t)),rr.join(' | ').slice(0,300));}
  let B=await lib();B.file(9,A.savedBytes());B.settle();B.click(600,700);B.settle();ok('the saved file reopens pixel identical',B.hash(190,776)===A.hash(190,776));
  A.key(132);for(let i=0;i<4;i++)A.key(130);for(let i=0;i<8;i++)A.key(130,2);A.settle();rmenu(A,362,297,10);x=part(A,'word/document.xml');ok('Small Caps again takes it off',!/smallCaps/.test(x));
  A.key(132);for(let i=0;i<4;i++)A.key(130);for(let i=0;i<8;i++)A.key(130,2);A.settle();rmenu(A,362,297,9);x=part(A,'word/document.xml');ok('All Caps from the menu: saved',/<w:caps\/>[^]*?the site/.test(x),runs(x).join(' | ').slice(0,200));
  A.key(122,1);A.settle();x=part(A,'word/document.xml');ok('undo takes All Caps off',!/<w:caps\/>/.test(x));
 }
};
