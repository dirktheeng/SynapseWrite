// imp6: zip CRC on open, .docx fidelity, F4 repeat, recent colors, hyphenation. Driven by events, judged on images and saved files.
const lib=require('./a7_lib'),{part,count,W}=require('./imp4_lib');const zlib=require('zlib');const fs=require('fs');const {execSync}=require('child_process');
const R=[];const ok=(n,c,x)=>{R.push(!!c);console.log(c?'PASS':'FAIL',n,x===undefined?'':x);};
const only=process.argv[2];
const zip=(files,o={})=>{const ps=[],cd=[];let off=0;for(const [n,dd] of Object.entries(files)){const d=Buffer.from(dd),c=o.stored?d:zlib.deflateRawSync(d),nm=Buffer.from(n);const crc=zlib.crc32(d)>>>0;const l=Buffer.alloc(30);l.writeUInt32LE(0x04034b50,0);l.writeUInt16LE(20,4);l.writeUInt16LE(o.stored?0:8,8);l.writeUInt32LE(crc,14);l.writeUInt32LE(c.length,18);l.writeUInt32LE(d.length,22);l.writeUInt16LE(nm.length,26);ps.push(l,nm,c);const k=Buffer.alloc(46);k.writeUInt32LE(0x02014b50,0);k.writeUInt16LE(20,6);k.writeUInt16LE(o.stored?0:8,10);k.writeUInt32LE(crc,16);k.writeUInt32LE(c.length,20);k.writeUInt32LE(d.length,24);k.writeUInt16LE(nm.length,28);k.writeUInt32LE(off,42);cd.push(k,nm);off+=30+nm.length+c.length;}
 const a=Buffer.concat(ps),b=Buffer.concat(cd),e=Buffer.alloc(22);e.writeUInt32LE(0x06054b50,0);e.writeUInt16LE(Object.keys(files).length,8);e.writeUInt16LE(Object.keys(files).length,10);e.writeUInt32LE(b.length,12);e.writeUInt32LE(a.length,16);return Buffer.concat([a,b,e]);};
const body=b=>`<?xml version="1.0"?><w:document ${W}><w:body>${b}</w:body></w:document>`;
const plain=n=>body(Array(n).fill('<w:p><w:r><w:t>Plain words on a line of their own</w:t></w:r></w:p>').join(''));
const dark=(A,x0,x1,y0,y1)=>count(A,x0,x1,y0,y1,(r,g,b)=>r<120&&g<120&&b<120);
const statusH=A=>A.hash(777,800);
exports.zip=zip;
(async()=>{
 if(!only||only=='crc'){
  const good=zip({'word/document.xml':plain(6)},{stored:true});
  const bad=Buffer.from(good);const at=bad.indexOf('Plain');bad[at]='Q'.charCodeAt(0);
  const goodD=zip({'word/document.xml':plain(6)});
  // a deflated part whose CRC field is wrong: the stream inflates to the stated size
  const badD=Buffer.from(goodD);const cdo=badD.readUInt32LE(badD.length-6);badD.writeUInt32LE((badD.readUInt32LE(cdo+16)^1)>>>0,cdo+16);
  for(const [nm,f] of [['stored part with a changed byte',bad],['deflated part with a wrong CRC',badD]]){
   let A=await lib();A.type('keep this');A.settle();const h=dark(A,319,420,174,776);const s0=statusH(A);const r=A.file(9,f);A.settle();A.shot('build/imp6_crc.png');
   ok(nm+': document stays',Math.abs(dark(A,319,420,174,776)-h)<=20,h);ok(nm+': message',statusH(A)!==s0);A.key('!');A.settle();const x=part(A,'word/document.xml');ok(nm+': document edits on',/keep this!/.test(x));}
  for(const [nm,f] of [['a stored part with the right CRC opens',good],['a deflated part with the right CRC opens',goodD]]){let A=await lib();A.type('old');A.file(9,f);A.settle();ok(nm,part(A,'word/document.xml').includes('Plain words'));}
  // a longer main part, to see the cost of the check
  let A=await lib();const r=A.file(9,zip({'word/document.xml':plain(400)}));A.settle();ok('a 400 paragraph file opens with the check',(part(A,'word/document.xml').match(/Plain words/g)||[]).length===400);
 }

 if(!only||only=='f4'){
  // a character format: bold on the first word, then F4 on the last word
  let A=await lib();A.type('one mid two');A.settle();A.key(132);for(let i=0;i<3;i++)A.key(130,2);A.key('b',1);A.settle();
  A.key(133);for(let i=0;i<3;i++)A.key(128,2);A.key(139);A.settle();A.shot('build/imp6_f4.png');let x=part(A,'word/document.xml');
  const bold=w=>new RegExp('<w:b/>(?:(?!</w:r>).)*<w:t[^>]*>'+w).test(x);
  ok('F4 repeats bold on a new selection',bold('one')&&bold('two')&&!bold(' mid'),x.match(/<w:body>.*<\/w:p>/)[0].slice(0,600));
  A.key('z',1);A.settle();x=part(A,'word/document.xml');ok('one undo takes the repeat back',bold('one')&&!bold('two'));
  // alignment: center the first paragraph, F4 in the second
  let B=await lib();B.type('first');B.key(13);B.type('second');B.key(13);B.type('third');B.settle();B.key(132,1);B.key('e',1);B.settle();B.key(131);B.key(139);B.settle();x=part(B,'word/document.xml');
  const jc=(x.match(/<w:p>.*?<\/w:p>/g)||[]).map(p=>(p.match(/w:jc w:val="(\w+)"/)||[])[1]);ok('F4 repeats centering in the next paragraph',jc[0]=='center'&&jc[1]=='center'&&jc[2]!='center',JSON.stringify(jc));
  // with nothing to repeat, F4 changes nothing
  let C=await lib();C.type('nothing');C.settle();const x0=part(C,'word/document.xml');C.key(139);C.settle();C.key('!');C.settle();ok('F4 with nothing to repeat changes nothing',part(C,'word/document.xml')===x0.replace('nothing<','nothing!<'));
 }

 if(!only||only=='recent'){
  const px=(A,x,y)=>{const f=A.fb(),i=(y*1280+x)*4;return [f[i],f[i+1],f[i+2]];};const hx=c=>c.map(v=>v.toString(16).padStart(2,'0')).join('').toUpperCase();
  const menu=A=>{A.click(299,102);A.settle();};const cell=(r,c)=>[270+c*22+11,115+r*22+11];
  let A=await lib();A.type('first words');A.key(97,1);A.settle();menu(A);const empty=hx(px(A,...cell(6,0)));A.shot('build/imp6_rc0.png');
  A.click(300,236);A.settle();const c1=px(A,...cell(4,1));A.click(...cell(4,1));A.settle();
  A.key(97,1);A.settle();menu(A);A.click(300,236);A.settle();const c2=px(A,...cell(6,5));A.click(...cell(6,5));A.settle();
  A.key(97,1);A.settle();menu(A);A.shot('build/imp6_rc1.png');const r0=hx(px(A,...cell(6,0))),r1=hx(px(A,...cell(6,1))),r2=hx(px(A,...cell(6,2)));
  ok('the recent row starts empty',empty=='FFFFFF',empty);
  ok('recent colors show newest first',r0==hx(c2)&&r1==hx(c1)&&r2=='FFFFFF',[r0,r1,r2,hx(c1),hx(c2)].join(' '));
  A.key(27);A.settle();A.key(133,1);A.key(13);A.type('fresh colored words');A.settle();A.key(132);A.key(133,2);A.settle();menu(A);A.click(...cell(6,1));A.settle();A.click(600,700);A.settle();A.shot('build/imp6_rc2.png');
  let x=part(A,'word/document.xml');ok('a recent cell applies its exact color',new RegExp('w:color w:val="'+hx(c1)+'"/>(?:(?!</w:r>).)*fresh').test(x),hx(c1));
  const n=count(A,223,1039,174,776,(a,b,d)=>Math.abs(a-c1[0])<=2&&Math.abs(b-c1[1])<=2&&Math.abs(d-c1[2])<=2);ok('drawn in that color',n>20,n);
  A.key(132);A.key(133,2);A.settle();menu(A);const q0=hx(px(A,...cell(6,0))),q1=hx(px(A,...cell(6,1)));ok('the used color moves to the front, not doubled',q0==hx(c1)&&q1==hx(c2)&&hx(px(A,...cell(6,2)))=='FFFFFF',[q0,q1].join(' '));
  A.click(...cell(6,6));A.settle();const x2=part(A,'word/document.xml');ok('an empty recent cell changes nothing',x2===x);
  A.key('z',1);A.settle();x=part(A,'word/document.xml');ok('undo takes the recent color off',!new RegExp(hx(c1)+'"/>(?:(?!</w:r>).)*fresh').test(x));
 }
 console.log(R.filter(x=>x).length,'passed,',R.filter(x=>!x).length,'failed');process.exit(R.every(x=>x)?0:1);
})();
