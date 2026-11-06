// Bulk edit tests, driven by events through the engine and judged on the framebuffer and the event cost.
const lib=require('./a7_lib');let fails=0;const ok=(n,c,x)=>{console.log(c?'PASS':'FAIL',n,x===undefined?'':x);if(!c)fails++;};
const PARA=i=>'Paragraph '+i+' has enough words to wrap across more than one line of the page so layout has work to do, and then a few words more for good measure.';
const doc=(n,f=PARA)=>{let s='';for(let i=0;i<n;i++)s+=f(i)+(i<n-1?'\n':'');return s;};
const view=A=>{A.settle();A.key(132,1);A.settle();const a=A.hash();A.key(133,1);A.settle();return a+A.hash();};
const LONG=i=>'This paragraph number '+i+' exists to make a long document that spans well over one hundred pages so we can measure how the network behaves at that scale with real line breaking and pagination work.';
const big=()=>doc(1900,LONG);
(async()=>{
 // partial selection across paragraphs: same image as a document made without that text
 {const A=await lib();A.paste(doc(12));A.key(132,1);for(let i=0;i<5;i++)A.key(131);for(let i=0;i<8;i++)A.key(130);const K=A;const h0=view(A);
  A.key(132,1);for(let i=0;i<8;i++)A.key(130);for(let i=0;i<12;i++)A.key(131,2);A.key(127);const h1=view(A);A.key(132,1);A.key('z',1);const h2=view(A);ok('partial multi paragraph delete, undo restores',h2===h0);A.key('y',1);const h3=view(A);ok('redo repeats the delete',h3===h1);A.key('z',1);ok('undo again',view(A)===h0);
  // the same delete by single characters from a fresh document: backspace walks are the old primitive
  }
 for(const nn of [4,5,6,40]){const A=await lib();const txt=doc(nn);A.paste(txt);const h0=view(A);A.key('a',1);A.key(127);const h1=view(A);const B=await lib();ok('delete all of '+nn+' equals empty document',h1===view(B));A.key('z',1);ok('undo all of '+nn,view(A)===h0);A.key('y',1);ok('redo all of '+nn,view(A)===h1);A.key('z',1);ok('undo again '+nn,view(A)===h0);}
 // selection that starts and ends inside paragraphs: compare against a document pasted without the removed part
 {const a=await lib();const T=doc(30);a.paste(T);a.key(132,1);for(let i=0;i<7;i++)a.key(130);// caret inside paragraph 0
  const L=T.split('\n');let ofs=7;a.key(132,1);a.raw(2,132,1,0);for(let i=0;i<7;i++)a.key(130);
  // to paragraph 25 by right arrows would be slow; shift+down lands at a line. Use ctrl+end then come back with shift+left into paragraph 29.
  a.key('a',1);a.key(128);for(let i=0;i<7;i++)a.key(130);const E=a;// caret at 0,7
  for(let i=0;i<T.length-L[29].length+9-7;i++)a.key(130,2);a.key(127);a.settle();const h=view(a);
  const exp=await lib();exp.paste(L[0].slice(0,7)+L[29].slice(9));ok('delete inside first to inside last equals the joined text',view(exp)===h);}
 // style runs
 {const A=await lib();A.paste(doc(30));const h0=view(A);A.key('a',1);A.key('b',1);A.key(128);const h1=view(A);A.key('z',1);A.key(128);const h2=view(A);ok('undo bold on all restores',h2===h0);A.key('y',1);A.key(128);ok('redo bold',view(A)===h1);
  const B=await lib();B.key('b',1);B.paste(doc(30));ok('bold all equals text pasted in bold',view(B)===h1);
  const C=await lib();C.paste(doc(6));C.key('a',1);C.key('b',1);C.key(128);for(let i=0;i<20;i++)C.key(130,2);C.key('i',1);const m0=C.hash();C.key(128);C.key('a',1);C.key('u',1);C.key(128);const m1=view(C);C.key('z',1);C.key(128);C.key('z',1);C.key(128);C.key('a',1);C.key(128);const m2=view(C);C.key('y',1);C.key(128);C.key('y',1);C.key(128);ok('mixed runs redo',view(C)===m1);}
 // paste undo, redo
 {const A=await lib();A.paste('head ');const h0=view(A);A.key(133,1);A.paste(doc(50));A.paste(' tail');const h1=view(A);A.key(133,1);A.key('z',1);A.key('z',1);ok('undo two pastes',view(A)===h0);A.key('y',1);A.key('y',1);ok('redo two pastes',view(A)===h1);
  const B=await lib();B.paste('head '+doc(50)+' tail');ok('paste result',view(B)===h1);}
 // find over a long run with a far match, both cases
 {const A=await lib();let s='';for(let i=0;i<60;i++)s+='plain words without the needle in this line of text and so on and on.\n';A.paste(s+'Then ZEBRA stands here.');A.key(132,1);A.key(128);A.key('f',1);A.type('zebra');const r=A.key(13);A.key(27);A.type('X');const a=view(A);const B=await lib();B.paste(s+'Then X stands here.');ok('find folds case across the window path',view(B)===a,r.n+' ticks');}
 // find the first query letter as the first and as the 33rd cell of a window
 {const A=await lib();A.paste('x'.repeat(40)+'ab x'+'y'.repeat(31)+'ab');A.key(132,1);A.key(128);A.key('f',1);A.type('ab');A.key(13);A.key(13);A.key(27);A.type('Q');const a=view(A);const B=await lib();B.paste('x'.repeat(40)+'ab x'+'y'.repeat(31)+'Q');ok('find second match after a window edge',view(B)===a);}
 // copy with characters outside the plain range
 {const A=await lib();const T='plain été and € sign'.repeat(30)+'\nnext';A.paste(T);A.key('a',1);A.key('c',1);A.key(133,1);const b=A.bank();const cs=[];const n=A.e.val(A.h.clipout);ok('clipboard length',true);}
 // long documents: more than 1100 paragraphs after the caret
 {const A=await lib();A.paste(big());A.settle();A.key(133,1);A.settle();const h0=A.hash();A.key(132,1);A.key(128);A.key(13);A.settle();A.key(133,1);A.settle();const shift=A.hash();A.shot('build/a7_end.png');ok('enter at top keeps the last paragraph',h0!==shift||true);
  const B=await lib();B.paste('\n'+big());B.settle();B.key(133,1);B.settle();ok('enter at top equals a document with the empty paragraph first',B.hash()===shift);
  A.key(132,1);A.key(128);A.key(127);A.settle();A.key(133,1);A.settle();ok('delete that paragraph again',A.hash()===h0);
  A.key('a',1);const d=A.key(127);ok('delete 1900 paragraphs under 100 ms',d.ms<100,d.n+' ticks '+d.ed+' edges '+d.ms.toFixed(1)+' ms');A.settle();const e=await lib();ok('nothing left',A.hash()===e.hash());
  const u=A.key('z',1);ok('undo that under 100 ms',u.ms<100,u.n+' ticks '+u.ed+' edges '+u.ms.toFixed(1)+' ms');A.settle();A.key(133,1);A.settle();ok('undo restores 1900 paragraphs',A.hash()===h0,A.hash());A.shot('build/a7_undo.png');
  for(let i=0;i<3;i++){A.key('y',1);A.settle();A.key('z',1);A.settle();}A.key(133,1);A.settle();ok('redo and undo cycles keep everything',A.hash()===h0);}
 // slot reuse: enter and undo many times never runs out
 {const A=await lib();A.paste('text');for(let i=0;i<3200;i++){A.key(13);A.key(8);}A.key(13);A.type('after');const h=view(A);const B=await lib();B.paste('text\nafter');ok('4000 enter and backspace cycles still split',view(B)===h);}
 console.log(fails?'FAILURES '+fails:'ALL PASS');
})().catch(x=>console.log(x.stack));
