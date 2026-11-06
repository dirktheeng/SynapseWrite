// Deterministic regression run through the engine only, driven by events. Prints a hash of the screen after each step,
// a hash of every saved file, and the ticks and edges each step took. Two builds with the same function print the same hashes.
// Usage: node test/a10_regress.js FIXTURE_DIR OUT_DIR  (run from the folder holding build/)
const fs=require('fs'),crypto=require('crypto');const FX=process.argv[2]||'test/fixtures';const OUT=process.argv[3];
const md5=b=>crypto.createHash('md5').update(b).digest('hex').slice(0,12);
require('./load')().then(({e,h,bank})=>{
 const lines=[];let totT=0,totE=0;
 const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);e.inject(h.ev[4],20000);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);const n=e.run(h.halt,80000000);totT+=n;return n;};
 const fb=()=>md5(Buffer.from(new Uint8Array(e.memory.buffer,e.p_fb(),1280*800*4)));
 const take=(nm)=>{const sv=e.val(h.saveout),pd=e.val(h.pdfout),n=sv||pd;if(!n)return null;const bb=bank(),a0=e.val(h.outbase),u=Buffer.alloc(n);for(let i=0;i<n;i++)u[i]=bb[a0+i];if(OUT)fs.writeFileSync(OUT+'/'+nm,u);return u;};
 const step=(nm,f)=>{const E0=e.edges();const T0=totT;const u=f();const dE=e.edges()-E0;totE+=dE;lines.push([nm.padEnd(16),fb(),('t '+(totT-T0)).padEnd(12),('e '+dE).padEnd(14),u&&u.length?'file '+u.length+' '+md5(u):''].join(' '));};
 const K=(c,m=0)=>D(2,c,m,1000),T=s=>{for(const ch of s)K(ch==='\n'?13:ch.charCodeAt(0));},C=(x,y)=>{D(3,x,y,1000);D(4,x,y);};
 const P=s=>{const bb=bank();for(let i=0;i<s.length;i++)bb[h.cb2+i]=s.charCodeAt(i);D(8,0,0,s.length);};
 const F=(k,f)=>{const u=fs.readFileSync(f),bb=bank();for(let i=0;i<u.length;i++)bb[h.file+i]=u[i];D(k,0,0,u.length);};
 const HOME=()=>C(80,47),INS=()=>C(135,47),LAY=()=>C(192,47),REF=()=>C(262,47),REV=()=>C(334,47);
 const save=nm=>{K(115,1);return take(nm);},pdf=nm=>{K(112,1);return take(nm);};
 step('init',()=>D(1));
 step('type',()=>T("Round trip & <check> (parens) don't dogs' teh wrongg 123 Ship\n"));
 step('bold',()=>{K(98,1);T('bold');K(98,1);T(' ');K(105,1);T('ital');K(105,1);T(' ');K(117,1);T('under');K(117,1);K(13);});
 step('align',()=>{T('Centered');K(101,1);K(13);K(108,1);T('Right');K(114,1);K(13);K(108,1);});
 step('font',()=>{T('Serif');K(133,2);C(149,75);K(133);K(13);T('Big');K(133,2);C(239,102);K(133);K(13);});
 step('latin',()=>{P('Caf\xe9 na\xefve \x93quoted\x94 \x80 \x97 end\n');});
 step('list',()=>{T('Item one');C(330,75);K(13);T('Item two');K(13);C(330,75);C(330,75);});
 step('table',()=>{INS();C(116,76);T('cell a');K(9);T('cell b');K(131);K(131);K(131);K(133);HOME();});
 step('header',()=>{INS();C(275,76);T('Head text');K(13);HOME();});
 step('tracked',()=>{T('Tracked ');REV();C(252,76);T('added');C(252,76);HOME();K(13);});
 step('fields',()=>{INS();T('Page ');C(434,76);T(' words ');C(560,76);K(13);T('E=mc^2 and x_1');C(725,76);K(133);HOME();K(13);});
 step('pic',()=>{F(10,FX+'/p_rgb.png');T('After pic');K(13);F(10,FX+'/p_a.png');T('After alpha');K(13);});
 step('note',()=>{REF();C(116,76);T('Note text');K(27);HOME();T(' more');K(13);});
 step('filler',()=>{let s='';for(let i=0;i<45;i++)s+='Filler line number '+i+' (with parens) and wrongwordd.\n';P(s);});
 step('find',()=>{K(102,1);T('Filler');K(13);K(13);K(27);});
 step('save1',()=>save('a.docx'));
 step('pdf1',()=>pdf('a.pdf'));
 let saved=null;
 step('save2',()=>{saved=save('b.docx');return saved;});
 if(saved){const p=(OUT||'.')+'/tmp_open.docx';fs.writeFileSync(p,saved);step('open',()=>F(9,p));step('resave',()=>save('c.docx'));step('pdf2',()=>pdf('b.pdf'));}
 step('open_lo',()=>F(9,FX+'/lo.docx'));
 step('save_lo',()=>save('d.docx'));
 if(fs.existsSync(FX+'/foreign.docx')){step('open_fg',()=>F(9,FX+'/foreign.docx'));step('save_fg',()=>save('f.docx'));}
 step('merge_src',()=>{C(80,47);K(97,1);K(127);T('Hello {Name}, from {City}!');K(13);});
 step('banner',()=>{REF();C(299,76);});
 step('merge',()=>{P('Name,City\nAnn,"Rome, IT"\nBob,Oslo\n');HOME();});
 step('save_merge',()=>save('e.docx'));
 for(const l of lines)console.log(l);console.log('total ticks',totT,'edges',totE,'mem',e.memory.buffer.byteLength);
}).catch(x=>console.log(x.stack));
