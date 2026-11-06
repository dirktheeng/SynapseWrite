// Invariants over random edit sequences, judged by images and saved files only.
// undo to the start is the start image; redo to the end is the end image; save and reopen is the same image and the same XML.
// node test/fuzz_inv.js FROM TO EDITS [u|s]
const {World,ui,unzip,R}=require('./fuzz_lib');const {rng}=require('./fuzz.js');const fs=require('fs');
const STY=['0:221','0:223','0:224','0:249','0:222'],LST=['0:210','0:212'];
function edits(seed,n){const r=rng(seed),I=k=>Math.floor(r()*k),P=a=>a[I(a.length)];const A=[];const TX='abcdefgh ijkl mnop,.;&<>"\'';
 for(let i=0;i<n;i++){const q=r();
  if(q<.4){let t='';for(let j=1+I(14);j>0;j--)t+=P(TX.split(''));A.push(['t',t]);}
  else if(q<.5)A.push(['k',13,0]);
  else if(q<.58)A.push(['k',P([8,127]),0]);
  else if(q<.66)A.push(['k',P([128,129,130,131,132,133]),P([0,0,2])]);
  else if(q<.72)A.push(['k',P([98,105,117]),1]);
  else if(q<.77)A.push(['k',P([101,108,114,106]),1]);
  else if(q<.84){let t='';for(let j=I(60);j>0;j--)t+=r()<.08?'\n':P(TX.split(''));A.push(['p',t]);}
  else if(q<.9)A.push(['b',P(STY)]);
  else if(q<.94)A.push(['b',P(LST)]);
  else if(q<.97)A.push(['c',320+I(500),190+I(200)]);
  else A.push(['k',13,1]);}
 return A;}
function apply(w,a){if(a[0]=='t')w.type(a[1]);else if(a[0]=='k')w.key(a[1],a[2]);else if(a[0]=='p'){if(a[1])w.paste(a[1]);}else if(a[0]=='b')w.click(...ui[a[1]]);else if(a[0]=='c')w.click(a[1],a[2]);w.lastAct=a;}
const norm=w=>{w.hover(1270,5);w.key(132,1);w.key(27);w.hover(1270,5);return w.docHash();};
const docOf=u=>unzip(u)['word/document.xml'].toString();
function caseU(seed,n){const w=new World({cap:8000000});w.type('Start text here');w.key(13);w.type('second');w.now+=5000;const H0=norm(w);w.now+=5000;for(const a of edits(seed,n))apply(w,a);const H1=norm(w);const msgs=[];
 let last=null,same=0,c=0;for(;c<n*3+20&&same<4;c++){w.now+=50;w.key(122,1);const k=w.docHash();same=k==last?same+1:0;last=k;}const H2=norm(w);if(H2!=H0){msgs.push('undo image');w.screen(R(`build/inv_u_${seed}.png`));}
 same=0;last=null;for(c=0;c<n*3+20&&same<4;c++){w.now+=50;w.key(121,1);const k=w.docHash();same=k==last?same+1:0;last=k;}const H3=norm(w);if(H3!=H1)msgs.push('redo image');
 return [w,msgs];}
function caseS(seed,n){const w=new World({cap:8000000});w.now+=5000;for(const a of edits(seed,n))apply(w,a);const H1=norm(w);const msgs=[];const u=w.save();if(!u)return [w,['no save']];let x1;try{x1=docOf(u);}catch(e){return [w,['zip '+e.message]];}
 w.openBytes(u);w.settle();const H2=norm(w);if(H2!=H1){msgs.push('reopen image');w.screen(R(`build/inv_s_${seed}.png`));}const u2=w.save();try{const x2=docOf(u2);if(x2!==x1){msgs.push('second save xml differs');fs.writeFileSync(R(`build/inv_s_${seed}_a.xml`),x1);fs.writeFileSync(R(`build/inv_s_${seed}_b.xml`),x2);}}catch(e){msgs.push('zip2 '+e.message);}
 return [w,msgs];}
if(require.main===module){const [from,to,n,mode]=[+process.argv[2],+process.argv[3],+process.argv[4]||30,process.argv[5]||'us'];let bad=0,tot=0;
 for(let s=from;s<to;s++)for(const m of mode){const t0=Date.now();const [w,msgs]=(m=='u'?caseU:caseS)(s,n);const f=w.fails.map(f=>f.cls+' '+f.id);const all=[...msgs,...new Set(f)];tot++;if(all.length)bad++;console.log(all.length?'FAIL':'PASS',m,s,'ticks',w.ticks,((Date.now()-t0)/1000|0)+'s',all.slice(0,4).join(' ; '));}
 console.log('inv failures',bad,'of',tot);}
module.exports={edits,apply,caseU,caseS};
