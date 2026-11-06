// Helpers for the imp3 tests: events in, images and saved files out.
const zlib=require('zlib');
exports.xml=(A,part='word/document.xml')=>{A.key(115,1);const u=A.savedBytes();let p=0;while(p<u.length-30&&u.readUInt32LE(p)==0x04034b50){const m=u.readUInt16LE(p+8),c=u.readUInt32LE(p+18),n=u.readUInt16LE(p+26),x=u.readUInt16LE(p+28);const nm=u.subarray(p+30,p+30+n).toString();const d=u.subarray(p+30+n+x,p+30+n+x+c);if(nm==part)return (m?zlib.inflateRawSync(d):d).toString();p+=30+n+x+c;}return '';};
exports.paras=s=>[...s.matchAll(/<w:p[ >].*?<\/w:p>|<w:p\/>/gs)].map(m=>[...m[0].matchAll(/<w:t[^>]*>([^<]*)<\/w:t>/g)].map(q=>q[1]).join(''));
// counts pixels in a box whose color passes a test
exports.count=(A,x0,x1,y0,y1,t)=>{const f=A.fb();let d=0;for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++){const i=(y*1280+x)*4;if(t(f[i],f[i+1],f[i+2]))d++;}return d;};
