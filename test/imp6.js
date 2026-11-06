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
 console.log(R.filter(x=>x).length,'passed,',R.filter(x=>!x).length,'failed');process.exit(R.every(x=>x)?0:1);
})();
