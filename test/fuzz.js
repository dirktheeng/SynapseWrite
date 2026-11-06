// Seeded event fuzzer over the real weights on the checked engine. Random keys, clicks, drags, ribbon commands,
// paste, undo, redo, save, open, across menus and modes. Judged by the checker, images and saved files.
// node test/fuzz.js run FROM TO STEPS [profile]   | node test/fuzz.js replay FILE | node test/fuzz.js regress | node test/fuzz.js min SEED STEPS PROFILE
const fs=require('fs');const {World,ui,NAMED,R,grp,names,unzip}=require('./fuzz_lib');
const rng=s=>()=>{s|=0;s=s+0x6D2B79F5|0;let t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return ((t^t>>>14)>>>0)/4294967296;};
const uik=Object.keys(ui);const fixtures={};for(const f of ['p_rgb.png','p_a.png'])try{fixtures[f]=fs.readFileSync(R('build/'+f));}catch(_){}
const TX=' abcdefghijklmnopqrstuvwxyzABCXYZ0123456789.,;:!?\'"-()&<>{}^_~/\\%#@\t';
function gen(seed,steps,profile){const r=rng(seed),I=n=>Math.floor(r()*n),P=a=>a[I(a.length)];const A=[];
 const W={mix:[30,8,6,10,3,3,3,2,2,3,1,1,2,1],edit:[50,6,3,12,1,3,5,3,3,1,0,0,0,0],menu:[12,6,1,40,1,0,1,1,0,1,0,0,0,0],ui:[10,24,16,12,6,0,2,1,0,6,0,0,1,1],file:[20,3,2,6,1,4,2,2,6,1,5,5,1,0]}[profile||'mix'];
 const tot=W.reduce((a,b)=>a+b);const pos=()=>r()<.6?[280+I(700),180+I(590)]:[I(1280),I(800)];
 for(let s=0;s<steps;s++){let x=r()*tot,k=0;while(x>=W[k]){x-=W[k];k++;}
  switch(k){
  case 0:{const q=r();if(q<.6){let t='';const n=1+I(12);for(let i=0;i<n;i++)t+=P(TX);A.push(['t',t]);}else if(q<.8)A.push(['k',P(Object.values(NAMED)),P([0,0,0,2,1,3])]);else if(q<.96)A.push(['k',P('abcdefghijklmnopqrstuvwxyz=+]['.split('')).charCodeAt(0),P([1,1,1,3])]);else A.push(['k',I(256),0]);break;}
  case 1:{const p=pos();A.push(['c',p[0],p[1]]);break;}
  case 2:{const p=pos(),q=pos();A.push(['g',p[0],p[1],q[0],q[1],1+I(3)]);break;}
  case 3:{const c=ui[P(uik)];const tab=+P(uik).split(':')[0];A.push(['c',c[0],c[1]]);break;}
  case 4:A.push(['w',P([-900,-400,-120,120,400,900])]);break;
  case 5:{const q=r();const n=q<.5?1+I(40):q<.9?I(800):2000+I(12000);let t='';for(let i=0;i<n;i++)t+=r()<.04?'\n':P(TX);A.push(['p',t.slice(0,n)]);break;}
  case 6:A.push(['k',122,1]);break;
  case 7:A.push(['k',121,1]);break;
  case 8:A.push(['s']);break;
  case 9:A.push(['T']);break;
  case 10:A.push(['o',P(['last','last','junk','trunc','flip','flip']),I(1e9)]);break;
  case 11:A.push(['i',P(['p_rgb.png','p_a.png','junk','trunc:p_rgb.png','flip:p_rgb.png','flip:p_a.png']),I(1e9)]);break;
  case 12:A.push(['h',I(1280),I(800)]);break;
  case 13:A.push(['K',P([1,2]),I(3)]);break;}}
 return A;}
function mutate(u,kind,sd){const r=rng(sd),I=n=>Math.floor(r()*n);if(!u||!u.length)u=new Uint8Array(30);u=new Uint8Array(u);
 if(kind==='junk'){const n=I(3000);const o=new Uint8Array(n);for(let i=0;i<n;i++)o[i]=I(256);if(r()<.5&&n>4){o[0]=0x50;o[1]=0x4b;o[2]=3;o[3]=4;}return o;}
 if(kind==='trunc')return u.subarray(0,I(u.length));
 const n=1+I(16);for(let i=0;i<n;i++){const a=I(u.length);u[a]=r()<.5?u[a]^(1<<I(8)):I(256);}return u;}
function apply(w,a){switch(a[0]){
 case 't':for(const ch of a[1]){if(w.dead)break;w.key(ch==='\n'?13:ch.charCodeAt(0));}break;
 case 'k':w.key(a[1],a[2]);break;
 case 'c':w.click(a[1],a[2]);break;
 case 'g':{w.hover(a[1],a[2]);w.down(a[1],a[2]);const n=a[5];for(let i=1;i<=n;i++)w.dragTo(Math.round(a[1]+(a[3]-a[1])*i/n),Math.round(a[2]+(a[4]-a[2])*i/n));w.up(a[3],a[4]);break;}
 case 'w':w.wheel(a[1]);break;
 case 'p':w.paste(a[1]);break;
 case 's':w.save();break;
 case 'T':w.timer();break;
 case 'o':{const base=w.lastSave;w.openBytes(mutate(base,a[1]==='last'?'none':a[1],a[2]));if(a[1]==='last'&&!base){}break;}
 case 'i':{const [k,f]=a[1].includes(':')?a[1].split(':'):[null,a[1]];const b=fixtures[f]||new Uint8Array(40);w.picBytes(k?mutate(b,k,a[2]):a[1]==='junk'?mutate(b,'junk',a[2]):b);break;}
 case 'h':w.hover(a[1],a[2]);break;
 case 'K':w.D(a[1]===1?12:13,a[2]);break;}}
function runTrace(A,opt={}){const w=new World({cap:opt.cap||40000000});let i=0;for(;i<A.length&&!w.dead;i++){w.step=i;const f0=w.fails.length;apply(w,A[i]);if(w.fails.length>f0&&opt.stopFirst)break;}return w;}
const sig=f=>f.cls+' '+f.id;
function ddmin(A,target){const test=B=>{const w=runTrace(B,{stopFirst:false});return w.fails.some(f=>sig(f)===target);};let n=2;A=A.slice();
 // single hit prefix first
 for(let hi=1;hi<=A.length;hi=Math.min(A.length,hi*2)){if(test(A.slice(0,hi))){A=A.slice(0,hi);break;}if(hi===A.length)break;}
 while(A.length>=2&&n<=A.length){const sz=Math.ceil(A.length/n);let red=false;for(let i=0;i<n;i++){const B=[...A.slice(0,i*sz),...A.slice((i+1)*sz)];if(B.length&&test(B)){A=B;n=Math.max(n-1,2);red=true;break;}}if(!red){if(n===A.length)break;n=Math.min(A.length,n*2);}}return A;}
const report=(w)=>{const m={};for(const f of w.fails){const k=sig(f);(m[k]=m[k]||{n:0,first:f}).n++;}return m;};
(async()=>{const [cmd,...a]=process.argv.slice(2);
 if(cmd==='run'){const [from,to,steps,prof]=[+a[0],+a[1],+a[2]||200,a[3]||'mix'];const all={};let bad=0,tot=0,ticks=0;const t0=Date.now();
  for(let s=from;s<to;s++){const w=runTrace(gen(s,steps,prof));ticks+=w.ticks;tot++;const m=report(w);const ks=Object.keys(m);if(ks.length)bad++;for(const k of ks){const q=all[k]=all[k]||{seeds:[],n:0,ev:m[k].first.ev,st:m[k].first.info&&m[k].first.info.st,x:m[k].first.info&&m[k].first.info.x};q.n+=m[k].n;q.seeds.push(s);}
   const wn=[...w.warn.keys()];for(const k of wn){const q=all['~'+k]=all['~'+k]||{seeds:[],n:0,x:w.warn.get(k).x,st:w.warn.get(k).st,ev:w.warn.get(k).ev};q.n++;q.seeds.push(s);}
   console.log('seed',s,prof,'ticks',w.ticks,'events',w.events,'fails',w.fails.length,w.dead?'DEAD':'',ks.slice(0,3).join(' | '),((Date.now()-t0)/1000|0)+'s');}
  console.log('SUMMARY',prof,'seeds',tot,'seeds with crash class',bad,'distinct',Object.keys(all).filter(k=>k[0]!='~').length,'ticks',ticks);
  for(const k of Object.keys(all).sort())console.log(k,JSON.stringify({n:all[k].n,seeds:all[k].seeds.slice(0,6),ev:all[k].ev,st:all[k].st,x:all[k].x}));
  fs.writeFileSync(R(`build/fuzz_${prof}_${from}_${to}.json`),JSON.stringify(all));return;}
 if(cmd==='min'){const [seed,steps,prof,target]=[+a[0],+a[1],a[2],a[3]];const A=gen(seed,steps,prof);const M=ddmin(A,target);console.log(JSON.stringify(M));return;}
 if(cmd==='regress'){const S=JSON.parse(fs.readFileSync(R('test/fuzz_data/seeds.json')));let bad=0;for(const c of S){const A=c.trace||gen(c.seed,c.steps,c.prof);const w=runTrace(A);const m=Object.keys(report(w));console.log(m.length?'FAIL':'PASS',c.name,'ticks',w.ticks,m.slice(0,3).join(' | '));if(m.length)bad++;}console.log('regress',S.length-bad,'of',S.length);process.exit(bad?1:0);}
})();
module.exports={gen,apply,runTrace,mutate,rng};
