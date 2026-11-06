// imp5: side scroll by wheel and thumb drag, and the other imp5 work. Driven by events, judged on images and saved files.
const lib=require('./a7_lib'),{part,doc,count,W}=require('./imp4_lib');const R=[];const ok=(n,c,x)=>{R.push(!!c);console.log(c?'PASS':'FAIL',n,x===undefined?'':x);};
const only=process.argv[2];
const thumb=A=>{const f=A.fb();let a=-1,b=-1;for(let x=0;x<1262;x++){const i=(770*1280+x)*4;if(f[i]==205&&f[i+1]==205&&f[i+2]==205){if(a<0)a=x;b=x;}}return [a,b];};
(async()=>{
 if(!only||only=='side'){
  const L='alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau\nsecond line here\n';
  let A=await lib();A.paste(L);A.settle();for(let i=0;i<4;i++){A.click(1232,788);A.settle();}A.shot('build/imp5_w0.png');
  const t0=thumb(A),h0=A.hash(174,760);
  A.e.inject(A.h.ev[5],2);A.wheel(300);A.settle();A.shot('build/imp5_w1.png');const t1=thumb(A);
  ok('Shift+wheel slides the page sideways',A.hash(174,760)!==h0&&t1[0]>t0[0],JSON.stringify([t0,t1]));
  const sc=A.hash(174,760);A.wheel(0);A.settle();
  A.raw(6,1000-200,0,1000);A.settle();A.shot('build/imp5_w2.png');const t2=thumb(A);ok('a sideways wheel delta slides back',t2[0]<t1[0]&&t2[0]>t0[0],JSON.stringify([t1,t2]));
  A.raw(6,1000-5000+4500,0,1000);A.settle();const t3=thumb(A);ok('sliding stops at the left edge',t3[0]==t0[0],JSON.stringify(t3));
  // a plain wheel still scrolls down, not sideways
  let B=await lib();B.paste(L.repeat(30));B.settle();for(let i=0;i<4;i++){B.click(1232,788);B.settle();}const b0=thumb(B),bh=B.hash(174,760);B.wheel(300);B.settle();const b1=thumb(B);ok('plain wheel scrolls down and leaves the slide',b1[0]==b0[0]&&B.hash(174,760)!==bh,JSON.stringify([b0,b1]));
  // dragging the thumb
  A=await lib();A.paste(L);A.settle();for(let i=0;i<4;i++){A.click(1232,788);A.settle();}const d0=thumb(A);const cx=(d0[0]+d0[1])>>1;
  A.raw(3,cx,770,1e6);A.settle();A.raw(22,cx+60,770,1);A.settle();A.raw(22,cx+150,770,1);A.settle();A.shot('build/imp5_d1.png');const d1=thumb(A);A.raw(4,cx+150,770);A.settle();
  ok('dragging the thumb moves it with the pointer',Math.abs(d1[0]-d0[0]-150)<=2,JSON.stringify([d0,d1]));
  A.raw(22,cx+400,770,1);A.settle();const d2=thumb(A);ok('after release a move does not drag it',d2[0]==d1[0],JSON.stringify(d2));
  A.raw(3,(d2[0]+d2[1])>>1,770,2e6);A.settle();A.raw(22,2000,770,1);A.settle();const d3=thumb(A);A.raw(4,1200,770);A.settle();ok('dragging past the end stops at the right edge',d3[1]>=1255&&d3[1]<1262,JSON.stringify(d3));
  // text typed after a drag lands where the caret was
  A.key(133);A.type('Q');A.settle();const x=part(A,'word/document.xml');ok('editing still works after a drag',/Q/.test(x));
 }
 const f=R.filter(x=>!x).length;console.log(`imp5: ${R.length-f} passed, ${f} failed`);process.exit(f?1:0);
})();
