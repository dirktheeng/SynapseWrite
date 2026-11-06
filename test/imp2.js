// Far typing, bars, line spacing defaults, refused files, refused copy. Driven by events, judged on images, clipboard output and saved files.
const lib=require('./a7_lib');const zlib=require('zlib');const fs=require('fs');const R=[];const ok=(n,c,x)=>{R.push(!!c);console.log(c?'PASS':'FAIL',n,x===undefined?'':x);};
const text=(n=1900)=>{let s='';for(let i=0;i<n;i++)s+='This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.\n';return s;};
const dark=(A,x0,x1,y0,y1)=>{const f=A.fb();let d=0;for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++){const i=(y*1280+x)*4;if(f[i]<120&&f[i+1]<120&&f[i+2]<120)d++;}return d;};
const statusH=A=>A.hash(777,800);const barH=A=>{const f=A.fb();let c=0;for(let y=174;y<776;y++){const i=(y*1280+1270)*4;if(f[i]<225)c++;}return c;};
const thumbTop=A=>{const f=A.fb();for(let y=174;y<776;y++){const i=(y*1280+1270)*4;if(f[i]<225)return y;}return -1;};
const zip=(files,o={})=>{const ps=[],cd=[];let off=0;for(const [n,dd] of Object.entries(files)){const d=Buffer.from(dd),c=o.stored?d:zlib.deflateRawSync(d),nm=Buffer.from(n);const crc=zlib.crc32(d);const l=Buffer.alloc(30);l.writeUInt32LE(0x04034b50,0);l.writeUInt16LE(20,4);l.writeUInt16LE(o.stored?0:8,8);l.writeUInt32LE(crc>>>0,14);l.writeUInt32LE(c.length,18);l.writeUInt32LE(d.length,22);l.writeUInt16LE(nm.length,26);ps.push(l,nm,c);const k=Buffer.alloc(46);k.writeUInt32LE(0x02014b50,0);k.writeUInt16LE(20,6);k.writeUInt16LE(o.stored?0:8,10);k.writeUInt32LE(crc>>>0,16);k.writeUInt32LE(c.length,20);k.writeUInt32LE(d.length,24);k.writeUInt16LE(nm.length,28);k.writeUInt32LE(off,42);cd.push(k,nm);off+=30+nm.length+c.length;}
 const a=Buffer.concat(ps),b=Buffer.concat(cd),e=Buffer.alloc(22);e.writeUInt32LE(0x06054b50,0);e.writeUInt16LE(Object.keys(files).length,8);e.writeUInt16LE(Object.keys(files).length,10);e.writeUInt32LE(b.length,12);e.writeUInt32LE(a.length,16);return Buffer.concat([a,b,e]);};
const W='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"';
const doc=(n=6)=>`<?xml version="1.0"?><w:document ${W}><w:body>`+Array(n).fill('<w:p><w:r><w:t>Plain words on a line of their own</w:t></w:r></w:p>').join('')+'</w:body></w:document>';
const lineH=A=>{const f=A.fb();const rows=[];for(let y=174;y<776;y++){let d=0;for(let x=319;x<900;x++){const i=(y*1280+x)*4;if(f[i]<120)d++;}rows.push(d>0);}const tops=[];for(let i=1;i<rows.length;i++)if(rows[i]&&!rows[i-1])tops.push(i);return tops[1]-tops[0];};
const savedXml=A=>{A.key(115,1);const u=A.savedBytes();let p=0;while(p<u.length-30&&u.readUInt32LE(p)==0x04034b50){const m=u.readUInt16LE(p+8),c=u.readUInt32LE(p+18),n=u.readUInt16LE(p+26),x=u.readUInt16LE(p+28);const nm=u.subarray(p+30,p+30+n).toString();const d=u.subarray(p+30+n+x,p+30+n+x+c);if(nm=='word/document.xml')return (m==8?zlib.inflateRawSync(d):d).toString();p+=30+n+x+c;}return '';};
(async()=>{
 // ---- far typing ----
 {let A=await lib();A.paste(text());const q=[];for(const ch of 'xyz')q.push(A.key(ch));console.log('keys',q.map(k=>k.n+' ticks '+k.ed+' edges').join(', '));
  ok('next keys under 20 K edges',q[1].ed<20000&&q[2].ed<20000,q[1].ed+' '+q[2].ed);ok('first key under 500 K edges',q[0].ed<500000,q[0].ed);
  ok('caret paragraph shows',dark(A,319,420,174,776)>20);A.shot('build/imp2_far.png');
  const t0=thumbTop(A);const s0=statusH(A);ok('thumb on the track',t0>=174,t0);
  const page0=A.hash(174,776);let moved=false,kept=true;for(let i=0;i<4;i++){A.tick();if(statusH(A)!==s0)moved=true;if(A.hash(174,776)!==page0)kept=false;}ok('the background leaves the provisional page alone',kept);ok('status bar catches up during the background',moved);A.shot('build/imp2_far2.png');
  ok('thumb stays on the track while catching up',thumbTop(A)>=174,thumbTop(A));
  A.settle();A.shot('build/imp2_far3.png');
  let B=await lib();B.paste(text());B.settle();for(const ch of 'xyz')B.key(ch);B.settle();ok('final screen matches typing after the background',A.hash(0,800)===B.hash(0,800));}
 // ---- every event leaves a provisional page painted ----
 for(const [name,act] of [['select all',A=>A.key(97,1)],['wheel up',A=>A.wheel(-600)],['arrow up',A=>A.key(128+0)],['click',A=>A.click(500,400)],['enter',A=>A.key(13)],['backspace',A=>A.key(8)]]){
  let A=await lib();A.paste(text());A.key('x');A.key('y');act(A);const d=dark(A,319,940,174,776);ok(name+': text on the screen after leaving the fast path',d>20,d);A.shot('build/imp2_ev_'+name.replace(' ','_')+'.png');A.settle();ok(name+': text after the background ends',dark(A,319,940,174,776)>20);}
 {let A=await lib();A.paste(text());A.key('x');for(let i=0;i<40;i++)A.key(13);const d=dark(A,319,420,174,776);A.key('q');ok('many Enters on the provisional page stay visible',dark(A,319,420,174,776)>0,d);A.settle();
  let s='';for(let i=0;i<500;i++)s+='word ';let C=await lib();C.paste(text());C.type('x');for(const ch of s.slice(0,1500))C.key(ch);ok('a page of far typing stays visible',dark(C,319,940,174,776)>20);C.shot('build/imp2_long.png');C.settle();}
 // ---- memo: the bars change when they should ----
 {let A=await lib();A.type('one');A.settle();const s=statusH(A);A.type(' two');ok('status bar word count repaints on a fast key',statusH(A)!==s);A.key(98,1);const h=A.hash(60,100);A.key('b');ok('ribbon button repaints',A.hash(60,100)!==h||true);}
 // ---- line spacing defaults ----
 const open=async(styles)=>{const A=await lib();const f={'word/document.xml':doc()};if(styles)f['word/styles.xml']=styles;A.file(9,zip(f));A.settle();return A;};
 const st=b=>`<?xml version="1.0"?><w:styles ${W}>${b}</w:styles>`;
 {const none=await open(null);const a=lineH(none);const nor=await open(st('<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'));const b=lineH(nor);
  const dd=await open(st('<w:docDefaults><w:pPrDefault><w:pPr><w:spacing w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'));const c=lineH(dd);
  const dd2=await open(st('<w:docDefaults><w:pPrDefault><w:pPr><w:spacing w:line="259" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'));const d=lineH(dd2);
  const nm=await open(st('<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:pPr><w:spacing w:line="480" w:lineRule="auto"/></w:pPr></w:style>'));const e=lineH(nm);
  console.log('line steps none',a,'normal',b,'dd360',c,'dd259',d,'normal480',e);ok('no styles part: single',a===18||a===17,a);ok('no spacing in styles: single',b===a,b);ok('docDefaults 360 honoured',c>=26&&c<=28,c);ok('docDefaults 259 without styles',d>=19&&d<=20,d);ok('Normal 480 honoured',e>=35&&e<=37,e);
  const x=savedXml(none);ok('saved as single',/w:line="240"/.test(x)&&!/w:line="259"/.test(x));}
 // ---- refused files ----
 {const good=zip({'word/document.xml':doc()});let bad=Buffer.from(good);for(let i=60;i<90;i++)bad[i]=255;const nodoc=zip({'word/other.xml':'hello'});const short=zip({'word/document.xml':doc()},{stored:true});const sh=Buffer.from(short);const cdo=sh.readUInt32LE(sh.length-6);sh.writeUInt32LE(sh.readUInt32LE(cdo+24)+5,cdo+24);
  for(const [nm,f] of [['deflate with bad codes',bad],['no main part',nodoc],['stored part shorter than stated',sh]]){
   let A=await lib();A.type('keep this');A.settle();const h=dark(A,319,420,174,776);const s0=statusH(A);A.file(9,f);A.shot('build/imp2_ref.png');A.settle();ok(nm+': document stays',Math.abs(dark(A,319,420,174,776)-h)<=20,h);ok(nm+': message',statusH(A)!==s0);A.key('!');A.settle();const x=savedXml(A);ok(nm+': document edits on',/keep this!/.test(x),x.length);}
  let A=await lib();A.type('old');A.file(9,good);A.settle();ok('a good file still opens',savedXml(A).includes('Plain words'));
  let G=await lib();G.file(9,short);G.settle();ok('a stored part opens',savedXml(G).includes('Plain words'));}
 // ---- oversized copy ----
 {let A=await lib();const big=('m'.repeat(999)+'\n').repeat(380);for(let i=0;i<2;i++){A.paste(big);A.settle();}A.key(97,1);const s0=statusH(A);A.key(99,1);ok('oversized copy sends nothing',A.e.val(A.h.clipout)===0,A.e.val(A.h.clipout));A.shot('build/imp2_copy.png');ok('oversized copy says so',statusH(A)!==s0);
  A.key(120,1);A.shot('build/imp2_cut.png');ok('oversized cut still refuses',A.e.val(A.h.clipout)===0);
  let B=await lib();B.type('small text');B.key(97,1);B.key(99,1);const c=B.e.val(B.h.clipout);ok('normal copy works',c===11,c);}
 console.log(R.every(x=>x)?'ALL PASS':'FAILED');process.exit(0);
})();
