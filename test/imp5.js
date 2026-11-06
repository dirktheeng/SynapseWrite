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

 if(!only||only=='style'){
  const name=(A,txt)=>{A.type(txt);A.settle();A.key(13);A.settle();};
  let A=await lib();A.type('Boxed');A.settle();A.key(97,1);A.key(98,1);A.settle();A.key(133,1);A.settle();const h0=A.hash(174,776);
  A.click(1186,74);A.settle();name(A,'My Note');A.settle();let s=part(A,'word/styles.xml');ok('style created',/styleId="MyNote"/.test(s));
  A.key(122,1);A.settle();A.click(600,700);A.settle();s=part(A,'word/styles.xml');let x=part(A,'word/document.xml');A.shot('build/imp5_su.png');
  ok('one undo takes back the new style and its use',!/MyNote/.test(s)&&!/MyNote/.test(x),(s.match(/styleId="[^"]*"/g)||[]).slice(-2).join(' '));
  A.key(121,1);A.settle();s=part(A,'word/styles.xml');x=part(A,'word/document.xml');ok('redo brings both back',/styleId="MyNote"/.test(s)&&/<w:pStyle w:val="MyNote"\/>/.test(x));
  A.key(122,1);A.settle();A.click(1186,74);A.settle();name(A,'My Note');s=part(A,'word/styles.xml');ok('after undo the name is free again, made once',(s.match(/styleId="MyNote"/g)||[]).length==1,(s.match(/styleId="MyNote"/g)||[]).length);
  A.key(122,1);A.settle();A.click(1106,120);A.settle();A.shot('build/imp5_su2.png');A.key(27);A.settle();
  A=await lib();A.click(1186,74);A.settle();name(A,'Empty Note');A.key(122,1);A.settle();s=part(A,'word/styles.xml');ok('on an empty paragraph one undo takes it back too',!/EmptyNote/.test(s));
  // a character style too
  A=await lib();A.type('red bold');A.settle();A.key(97,1);A.key(98,1);A.settle();A.click(1186,96);A.settle();name(A,'Alert');A.key(122,1);A.settle();s=part(A,'word/styles.xml');x=part(A,'word/document.xml');
  ok('undo of a character style creation',!/Alert/.test(s)&&!/rStyle/.test(x)&&/<w:b\/>/.test(x));
 }

 if(!only||only=='keys'){
  const txt=x=>[...x.matchAll(/<w:t[^>]*>([^<]*)/g)].map(m=>m[1]).join('');
  let A=await lib();A.type('a');A.key(32,3);A.type('b');A.key('_',3);A.type('c');A.settle();A.shot('build/imp5_k1.png');let x=part(A,'word/document.xml');
  ok('Ctrl+Shift+Space types a no-break space',txt(x).includes('a b'),JSON.stringify(txt(x)));
  ok('Ctrl+Shift+- types a no-break hyphen',txt(x).includes('b‑c'),JSON.stringify(txt(x)));
  const ink=count(A,223,1039,174,400,(r)=>r<120);let B=await lib();B.type('a');B.key(32,3);B.type('b-c');B.settle();const ink2=count(B,223,1039,174,400,(r)=>r<120);ok('the no-break hyphen draws as a hyphen',ink==ink2&&ink>40,[ink,ink2]);
  A=await lib();A.key('e',3);A.settle();A.type('tracked');A.settle();x=part(A,'word/document.xml');ok('Ctrl+Shift+E turns tracking on',/<w:ins [^>]*>.*tracked/.test(x));
  A.key('e',3);A.settle();A.type(' plain');A.settle();x=part(A,'word/document.xml');ok('and off again',/plain/.test(x)&&!(x.match(/<w:ins [^>]*>(?:(?!<\/w:ins>).)*<\/w:ins>/g)||[]).some(q=>/plain/.test(q)),x.slice(x.indexOf('<w:body'),x.indexOf('<w:body')+400));
  A=await lib();A.type('m');A.settle();let h=A.hash(174,776);A.key('*',3);A.settle();A.shot('build/imp5_k2.png');const hm=A.hash(174,776);B=await lib();B.type('m');B.settle();B.ctl('0:233');B.ctl('4:209');B.settle();B.click(600,700);B.settle();A.click(600,700);A.settle();
  ok('Ctrl+Shift+8 shows marks, like the button',hm!==h&&A.hash(174,776)===B.hash(174,776));
  A=await lib();A.file(9,doc('<w:p><w:r><w:t xml:space="preserve">one two three </w:t></w:r><w:fldSimple w:instr=" NUMWORDS "><w:r><w:t>99</w:t></w:r></w:fldSimple></w:p>'));
  x=part(A,'word/document.xml');const w0=(x.match(/NUMWORDS[^>]*>.*?<w:t[^>]*>(\d+)/)||[])[1];A.key(138);x=part(A,'word/document.xml');const w1=(x.match(/NUMWORDS[^>]*>.*?<w:t[^>]*>(\d+)/)||[])[1];
  ok('F9 updates fields',w1!==undefined&&w1!=='99'&&w1!==w0||(w0!=='99'&&w1===w0),[w0,w1]);
  A=await lib();A.key('f',3);A.settle();A.shot('build/imp5_k3.png');B=await lib();B.click(231,75);B.settle();ok('Ctrl+Shift+F opens the font menu',A.hash(95,600)===B.hash(95,600)&&A.hash(95,600)!==(await lib()).hash(95,600));
  A=await lib();A.key('p',3);A.settle();B=await lib();B.click(282,75);B.settle();B.shot('build/imp5_k4.png');ok('Ctrl+Shift+P opens the size menu',A.hash(95,600)===B.hash(95,600));
 }

 if(!only||only=='colbr'){
  const sect='<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/><w:cols w:num="2" w:space="720"/></w:sectPr>';
  const right=A=>count(A,640,1030,190,330,(r)=>r<120),left=A=>count(A,230,620,190,330,(r)=>r<120);
  let A=await lib();A.file(9,doc('<w:p><w:r><w:t>left words</w:t></w:r></w:p><w:p><w:r><w:br w:type="column"/><w:t>right words</w:t></w:r></w:p>'+sect));A.settle();A.shot('build/imp5_cb1.png');
  ok('a column break in a file starts the second column',right(A)>100&&left(A)>100,[left(A),right(A)]);
  let x=part(A,'word/document.xml');ok('saved as a column break run',/<w:r><w:br w:type="column"\/><\/w:r>/.test(x)&&!/pageBreakBefore/.test(x),x.slice(x.indexOf('<w:body'),x.indexOf('<w:body')+300));
  let B=await lib();B.file(9,A.savedBytes());B.settle();A.click(600,700);A.settle();B.click(600,700);B.settle();ok('reopens pixel equal',A.hash(174,776)===B.hash(174,776));
  // typed: Ctrl+Shift+Enter
  A=await lib();A.file(9,doc('<w:p><w:r><w:t>left words</w:t></w:r></w:p>'+sect));A.settle();A.key(133,1);A.settle();const r0=right(A);A.key(13,3);A.settle();A.type('typed right');A.settle();A.shot('build/imp5_cb2.png');
  ok('Ctrl+Shift+Enter moves the rest to the next column',r0==0&&right(A)>100,[r0,right(A)]);
  x=part(A,'word/document.xml');ok('typed break saved',/<w:br w:type="column"\/>[^]*typed right/.test(x));
  let nu=0;for(;nu<20;nu++){x=part(A,'word/document.xml');if(!/type="column"/.test(x))break;A.key(122,1);A.settle();}A.click(600,700);A.settle();A.shot('build/imp5_cb3.png');x=part(A,'word/document.xml');ok('undo takes the break away, after the typing',!/type="column"/.test(x)&&!/typed/.test(x)&&/left words/.test(x)&&right(A)==0,[nu,right(A)]);
  A.key(121,1);A.settle();x=part(A,'word/document.xml');ok('redo puts it back',/type="column"/.test(x)&&!/typed/.test(x),'');
  // one column: it acts as a page break
  A=await lib();A.type('first');A.key(13,3);A.type('second');A.settle();x=part(A,'word/document.xml');A.shot('build/imp5_cb4.png');
  B=await lib();B.type('first');B.key(13,1);B.type('second');B.settle();B.shot('build/imp5_cb5.png');ok('in one column it breaks the page, drawn as Ctrl+Enter draws',/type="column"/.test(x)&&A.hash(0,800)===B.hash(0,800));
 }

 if(!only||only=='pick'){
  const px=(A,x,y)=>{const f=A.fb(),i=(y*1280+x)*4;return [f[i],f[i+1],f[i+2]];};const hx=c=>c.map(v=>v.toString(16).padStart(2,'0')).join('').toUpperCase();
  let A=await lib();A.type('Picked words');A.key(97,1);A.settle();A.click(299,102);A.settle();A.click(300,236);A.settle();A.shot('build/imp5_p1.png');
  const want=[[4,1],[6,5],[1,7]].map(([r,c])=>[r,c,px(A,270+c*22+11,115+r*22+11)]);
  ok('the picker grid opens from the color menu',new Set(want.map(w=>hx(w[2]))).size==3&&want.every(w=>hx(w[2])!='FFFFFF'),want.map(w=>hx(w[2])).join(' '));
  const [r,c,col]=want[0];A.click(270+c*22+11,115+r*22+11);A.settle();A.click(600,700);A.settle();A.shot('build/imp5_p2.png');
  let x=part(A,'word/document.xml');ok('a pick sets that exact color',new RegExp('w:color w:val="'+hx(col)+'"').test(x),hx(col)+' '+(x.match(/w:color[^>]*/)||[])[0]);
  const n=count(A,223,1039,174,776,(a,b,d)=>Math.abs(a-col[0])<=2&&Math.abs(b-col[1])<=2&&Math.abs(d-col[2])<=2);ok('drawn in that exact color',n>20,n);
  A.key(122,1);A.settle();x=part(A,'word/document.xml');ok('undo takes it off',!new RegExp(hx(col)).test(x));
  // another cell, through the keyboard free path: open, pick a dark teal
  A.key(97,1);A.settle();A.click(299,102);A.settle();A.click(300,236);A.settle();const [r2,c2,col2]=want[1];A.click(270+c2*22+11,115+r2*22+11);A.settle();x=part(A,'word/document.xml');ok('a second pick',new RegExp('w:color w:val="'+hx(col2)+'"').test(x),hx(col2));
  // Esc closes it with no change
  A=await lib();A.type('none');A.key(97,1);A.settle();A.click(299,102);A.settle();A.click(300,236);A.settle();A.key(27);A.settle();x=part(A,'word/document.xml');ok('Esc leaves the color alone',!/w:color w:val="(?!000000)/.test(x));
 }

 if(!only||only=='vruler'){
  const band=A=>{const f=A.fb();let a=-1,b=-1;for(let y=174;y<776;y++){const i=(y*1280+10)*4;if(f[i]>=250&&f[i+1]>=250){if(a<0)a=y;b=y;}}return [a,b];};
  const mar=x=>(x.match(/<w:pgMar [^>]*/)||[''])[0];
  let A=await lib();A.paste('Margin text here\n'.repeat(3));A.settle();A.move(600,700);A.settle();const b0=band(A),h0=A.hash(174,776);
  A.raw(3,9,b0[0],1e6);A.settle();A.raw(22,9,b0[0]+48,1);A.settle();A.raw(4,9,b0[0]+48);A.settle();A.move(600,700);A.settle();A.shot('build/imp5_vr1.png');const b1=band(A);
  let x=part(A,'word/document.xml');ok('dragging the top margin edge down half an inch',/w:top="2160"/.test(mar(x)),mar(x));
  ok('the ruler band and the text move with it',b1[0]==b0[0]+48&&A.hash(174,776)!==h0,JSON.stringify([b0,b1]));
  A.key(122,1);A.settle();A.move(600,700);A.settle();x=part(A,'word/document.xml');ok('undo brings the margin back',/w:top="1440"/.test(mar(x))&&A.hash(174,776)===h0,mar(x));
  // a small move snaps to a sixteenth of an inch
  A.raw(3,9,b0[0]+2,2e6);A.settle();A.raw(4,9,b0[0]-22);A.settle();x=part(A,'word/document.xml');ok('up a quarter inch, snapped',/w:top="1080"/.test(mar(x)),mar(x));
  // at 150 percent the travel is unzoomed
  A=await lib();A.paste('Zoomed\n');A.settle();for(let i=0;i<2;i++){A.click(1232,788);A.settle();}const z0=band(A);A.raw(3,9,z0[0],1e6);A.settle();A.raw(4,9,z0[0]+72);A.settle();x=part(A,'word/document.xml');ok('at 150 percent, 72 px is half an inch',/w:top="2160"/.test(mar(x)),mar(x)+' '+z0);
  A=await lib();A.paste('Bottom\n');A.settle();for(let i=0;i<2;i++){A.click(1096,788);A.settle();}A.move(600,700);A.settle();const q0=band(A);A.shot('build/imp5_vr5.png');A.raw(3,9,q0[1]+1,1e6);A.settle();A.raw(4,9,q0[1]+1-24);A.settle();A.move(600,700);A.settle();const q1=band(A);x=part(A,'word/document.xml');
  ok('at 50 percent the bottom margin edge drags up',/w:bottom="2160"/.test(mar(x))&&q1[1]==q0[1]-24,mar(x)+' '+JSON.stringify([q0,q1]));
  // a press away from the edges does nothing
  A=await lib();A.paste('x\n');A.settle();A.move(600,700);A.settle();const c0=band(A),hc=A.hash(174,776);A.raw(3,9,c0[0]+100,1e6);A.settle();A.raw(4,9,c0[0]+200);A.settle();A.move(600,700);A.settle();x=part(A,'word/document.xml');ok('a press inside the band changes nothing',/w:top="1440" w:right="1440" w:bottom="1440"/.test(mar(x))&&JSON.stringify(band(A))===JSON.stringify(c0),mar(x));
 }

 if(!only||only=='tcol'){
  const sect='<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/><w:cols w:num="2" w:space="720"/></w:sectPr>';
  const cell=t=>`<w:tc><w:tcPr><w:tcW w:w="2000" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>${t}</w:t></w:r></w:p></w:tc>`;
  const B4='<w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4"/><w:left w:val="single" w:sz="4"/><w:bottom w:val="single" w:sz="4"/><w:right w:val="single" w:sz="4"/><w:insideH w:val="single" w:sz="4"/><w:insideV w:val="single" w:sz="4"/></w:tblBorders></w:tblPr>';
  const tbl=`<w:tbl>${B4}<w:tblGrid><w:gridCol w:w="2000"/><w:gridCol w:w="2000"/></w:tblGrid><w:tr>${cell('a1')+cell('b1')}</w:tr><w:tr>${cell('a2')+cell('b2')}</w:tr></w:tbl>`;
  const rule=(A,x0,x1)=>count(A,x0,x1,300,360,(r,g,b)=>r<40&&g<40&&b<40);
  let A=await lib();A.file(9,doc('<w:p><w:r><w:t>left</w:t></w:r></w:p><w:p><w:r><w:br w:type="column"/><w:t>right col</w:t></w:r></w:p>'+tbl+'<w:p><w:r><w:t>after</w:t></w:r></w:p>'+sect));A.settle();A.move(1200,700);A.settle();A.shot('build/imp5_tc1.png');
  ok('a table in the second column draws its rules there',rule(A,630,1000)>300&&rule(A,300,600)<20,[rule(A,300,600),rule(A,630,1000)]);
  // the cell text and the rule agree: each cell's text sits right of its left rule
  const f=A.fb();let lx=-1;for(let x=630;x<700;x++){const i=(330*1280+x)*4;if(f[i]<40){lx=x;break;}}let tx=-1;for(let x=lx+2;x<lx+40;x++){let ink=false;for(let y=330;y<348;y++){const i=(y*1280+x)*4;if(f[i]<120)ink=true;}if(ink){tx=x;break;}}
  ok('cell text is inside its rules',lx>630&&tx>lx&&tx-lx<12,[lx,tx]);
  // a click in a cell of the second column types there
  A.click(lx+200,340);A.key(133);A.type('Z');A.settle();let x=part(A,'word/document.xml');ok('a click in the second column cell edits that cell',/<w:t[^>]*>b2Z</.test(x),(x.match(/<w:t[^>]*>b2[^<]*/)||[])[0]);
  // PDF draws the rules in the second column too
  A.key(112,1);const pn=A.e.val(A.h.fileout)||0,pa=A.e.val(A.h.outbase);const pb=Buffer.alloc(pn);for(let i=0;i<pn;i++)pb[i]=A.e.bget(pa+i);require('fs').writeFileSync('build/imp5_tc.pdf',pb);
  require('child_process').execSync('pdftoppm -r 96 -f 1 -l 1 -singlefile build/imp5_tc.pdf build/imp5_tcp');
  const pp=require('fs').readFileSync('build/imp5_tcp.ppm');const hd=pp.toString('latin1',0,40).split(/\s+/);const W=+hd[1],off=pp.indexOf('255\n')+4;
  const pdark=(x0,x1,y0,y1)=>{let n=0;for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++){const i=off+(y*W+x)*3;if(pp[i]<160&&pp[i+1]<160)n++;}return n;};
  ok('PDF draws the table rules in the second column',pdark(400,720,110,170)>500&&pdark(90,380,110,170)<60,[pdark(90,380,110,170),pdark(400,720,110,170)]);
  // a table inserted in a two column section fits the column
  A=await lib();A.file(9,doc('<w:p><w:r><w:t>two col text</w:t></w:r></w:p>'+sect));A.settle();A.key(133,1);A.key(13);A.ctl('0:230');A.ctl('1:240');A.settle();A.click(600,700);A.settle();A.shot('build/imp5_tc2.png');x=part(A,'word/document.xml');
  const ws=[...x.matchAll(/<w:gridCol w:w="(\d+)"/g)].map(m=>+m[1]);const tot=ws.reduce((a,b)=>a+b,0);ok('an inserted table fits the column',ws.length>=2&&tot<=4500&&tot>=4400,JSON.stringify(ws));
 }
 const f=R.filter(x=>!x).length;console.log(`imp5: ${R.length-f} passed, ${f} failed`);process.exit(f?1:0);
})();
