// imp3: find across paragraphs. Driven by events, judged on images and saved files.
const lib=require('./a7_lib'),{xml,paras,count}=require('./imp3_lib');const R=[];const ok=(n,c,x)=>{R.push(!!c);console.log(c?'PASS':'FAIL',n,x===undefined?'':x);};
const only=process.argv[2];
const sel=(r,g,b)=>b>r+20&&r>120;     // selection tint
const yel=(r,g,b)=>r>200&&g>180&&b<170; // match tint
(async()=>{
 if(!only||only=='find'){
  const T='alpha end\nstart beta\nthird line\nalpha end\nstart gamma\nlast\n';
  let A=await lib();A.paste(T);A.settle();A.key(102,1);A.type('end^pstart');A.settle();A.shot('build/imp3_find1.png');
  const h1=count(A,319,900,174,776,yel);ok('every match across a mark is tinted',h1>100,h1);
  A.key(13);A.settle();A.shot('build/imp3_find2.png');
  A.key(27);A.settle();
  // the selection reaches into the next paragraph: typing replaces it and merges the two
  A.type('X');A.settle();let p=paras(xml(A));ok('first match selected across the mark',p[0]=='alpha X beta'&&p.length==6,JSON.stringify(p));
  A=await lib();A.paste(T);A.settle();A.key(104,1);A.type('end^pstart');A.key(9);A.type(' + ');A.key(13);A.settle();A.key(13);A.settle();A.key(13);A.settle();A.key(27);A.settle();
  p=paras(xml(A));ok('replace merges paragraphs',p[0]=='alpha  +  beta'&&p[2]=='alpha  +  gamma',JSON.stringify(p));
  A=await lib();A.paste('one two\nthree\n');A.settle();A.key(104,1);A.type('one two');A.key(9);A.type('a^pb');A.key(13);A.settle();A.key(13);A.settle();A.key(27);A.settle();p=paras(xml(A));ok('replacement with a mark splits',p[0]=='a'&&p[1]=='b'&&p[2]=='three',JSON.stringify(p));
  A=await lib();A.paste('x\ny\nz\nq\n');A.settle();A.key(102,1);A.type('^py^pz');A.settle();A.key(13);A.settle();A.key(27);A.settle();A.type('M');A.settle();p=paras(xml(A));ok('two marks, query starting with one',p[0]=='xM'&&p[1]=='q',JSON.stringify(p));
  A=await lib();A.paste('alpha\nbeta\n');A.settle();A.key(102,1);A.type('zz^pq');A.settle();A.key(13);A.settle();A.key(27);A.settle();A.type('M');A.settle();p=paras(xml(A));ok('no match leaves the text',p[0].includes('alpha')&&p[1]=='beta',JSON.stringify(p));
  // pasting into the bar
  A=await lib();A.paste('red\nblue\n');A.settle();A.key(102,1);A.paste('red\nblue');A.settle();A.shot('build/imp3_find3.png');A.key(13);A.settle();A.key(27);A.settle();A.type('Z');A.settle();p=paras(xml(A));ok('pasted lines search as marks',p[0]=='Z',JSON.stringify(p));
  // same paragraph queries still work the old way
  A=await lib();A.paste('cat dog cat\n');A.settle();A.key(102,1);A.type('cat');A.key(13);A.settle();A.key(13);A.settle();A.key(27);A.settle();A.type('Q');A.settle();p=paras(xml(A));ok('plain query walks in one paragraph',p[0]=='cat dog Q',JSON.stringify(p));
  // whole words across a mark
  A=await lib();
 }
 if(!only||only=='zoom'){
  const dk=(A,x0,x1,y0,y1)=>count(A,x0,x1,y0,y1,(r,g,b)=>r<110&&g<110&&b<110);
  let L='';for(let i=0;i<14;i++)L+='Zoom paragraph '+i+' has enough words on it that it wraps across the page and shows how lines scale when the view changes in size.\n';
  let A=await lib();A.paste(L);A.settle();A.key(13,1);A.settle();A.type('Second page');A.settle();A.shot('build/imp3_z100.png');const h100=A.hash(0,800);
  A.click(1096,788);A.settle();A.shot('build/imp3_z75.png');const h75=A.hash(174,776);ok('zoom out changes the page',h75!==h100);
  A.click(1096,788);A.settle();A.shot('build/imp3_z50.png');const white=(A,y)=>{const f=A.fb();let l=-1,r=-1;for(let x=0;x<1262;x++){const i=(y*1280+x)*4;if(f[i]==255&&f[i+1]==255&&f[i+2]==255){if(l<0)l=x;r=x;}}return r-l+1;};const w=white(A,380);ok('half size page is about 408 px wide',Math.abs(w-408)<12,w);
  const q=A=>{A.key(128);A.key(130);return A.hash(174,776);};A.click(1096,788);A.settle();const q1=q(A);A.click(1096,788);A.settle();ok('zoom stops at 50',q1===q(A));
  // caret: click on a known line at 50 percent and type: the letter lands in the paragraph clicked
  A.click(1232,788);A.click(1232,788);A.settle();
  A.click(1232,788);A.click(1232,788);A.settle();A.shot('build/imp3_z150.png');const w2=white(A,700);ok('page at 150 percent is about 1224 px wide',Math.abs(w2-1224)<14,w2);
  A.click(1096,788);A.click(1096,788);A.settle();
  let B=await lib();B.paste(L);B.settle();B.key(13,1);B.settle();B.type('Second page');B.settle();ok('round trip to 100 percent is pixel equal to one that never zoomed',q(A)===q(B));
  // click maps through the zoom
  for(const [lvl,clicks] of [['50',2],['150',-2]]){let C=await lib();C.paste('alpha beta gamma\nsecond line here\nthird line here\n');C.settle();for(let i=0;i<Math.abs(clicks);i++)C.click(clicks>0?1096:1232,788);C.settle();
   // the second paragraph sits at this screen y at this zoom: find it by ink rows
   const rows=[];const f=C.fb();for(let y=174;y<700;y++){let n=0;for(let x=100;x<1200;x++){const i=(y*1280+x)*4;if(f[i]<110)n++;}rows.push(n>0);}
   const tops=[];for(let i=1;i<rows.length;i++)if(rows[i]&&!rows[i-1])tops.push(i+174);
   C.click(631,tops[1]+3);C.settle();C.key(133);C.type('Q');C.settle();const p=paras(xml(C));ok('click at '+lvl+' percent lands in the second paragraph',p[1]=='second line hereQ',JSON.stringify(p));C.shot('build/imp3_zc'+lvl+'.png');
   // arrow moves with hit test
   C.key(129);C.type('R');C.settle();const p2=paras(xml(C));ok('arrow up at '+lvl+' percent reaches the line above',p2[0].includes('R'),JSON.stringify(p2));}
  // view tab commands, ruler, read mode
  let D=await lib();D.paste('read mode text\n');D.settle();D.ctl('0:234');D.ctl('5:210');D.settle();D.shot('build/imp3_zv.png');const hz=D.hash(174,776);D.ctl('5:212');D.settle();ok('View tab zoom in then 100 percent',D.hash(174,776)!==hz);
  D.ctl('5:215');D.settle();D.shot('build/imp3_read.png');D.type('x');D.key(8);D.settle();D.key(27);D.settle();D.shot('build/imp3_read2.png');const p3=paras(xml(D));ok('read mode refuses edits and Esc returns',p3[0]=='read mode text',JSON.stringify(p3));
  // picture at 150 percent
  let E=await lib();E.file(10,require('fs').readFileSync('build/p_rgb.png'));E.settle();const pb=E.hash(174,776);E.click(1232,788);E.settle();E.shot('build/imp3_zpic.png');ok('picture repaints when zoomed',E.hash(174,776)!==pb);
  // costs: at 100 percent nothing is added
 }
 if(!only||only=='clip'){
  const runs=x=>[...x.matchAll(/<w:r>(.*?)<\/w:r>/gs)].map(m=>[/<w:b\/>/.test(m[1]),(m[1].match(/<w:t[^>]*>([^<]*)/)||[])[1]]);
  let A=await lib();A.type('plain ');A.key(98,1);A.type('bold');A.key(98,1);A.type(' tail');A.key(13);A.settle();A.type('second');A.key(101,1);A.settle();
  A.key(97,1);A.settle();A.key(99,1);A.settle();const text=[];for(let i=0;i<40;i++){const c=A.bank()[A.h.cb+i];if(!c)break;text.push(String.fromCharCode(c));}const clip=text.join('');ok('plain text still leaves for the system clipboard',clip.startsWith('plain bold tail\nsecond'),JSON.stringify(clip));
  A.key(133,1);A.key(13);A.paste(clip.slice(0,'plain bold tail\nsecond'.length));A.settle();A.shot('build/imp3_clip.png');const x=xml(A);const b=[...x.matchAll(/<w:r>(?:(?!<\/w:r>).)*<w:b\/>(?:(?!<\/w:r>).)*<w:t[^>]*>bold/gs)].length;ok('bold survives a paste of the own copy',b==2,b);
  const ps=[...x.matchAll(/<w:p>.*?<\/w:p>/gs)].map(m=>/w:jc w:val="center"/.test(m[0]));ok('paragraph record travels with its mark, tail keeps its own',ps[2]==false,JSON.stringify(ps));
  const u0=paras(x).length;A.key(122,1);A.settle();ok('undo removes the paste as one step',paras(xml(A)).length<u0,paras(xml(A)).length+' of '+u0);
  // centered paragraph copied with its mark
  let B=await lib();B.type('head');B.key(101,1);B.key(13);B.key(108,1);B.type('body');B.settle();B.key(132,1);for(let i=0;i<5;i++)B.key(130,2);B.settle();B.key(99,1);B.settle();const c2=String.fromCharCode(...Array.from({length:5},(_,i)=>B.bank()[B.h.cb+i]));B.key(133,1);B.key(13);B.paste(c2);B.settle();let y=xml(B);const c3=[...y.matchAll(/<w:p[ >].*?<\/w:p>/gs)].map(m=>/w:jc w:val="center"/.test(m[0]));ok('a copied paragraph mark brings its alignment',c3[2]==true,JSON.stringify(c3));B.key(122,1);B.settle();y=xml(B);const c4=[...y.matchAll(/<w:p[ >].*?<\/w:p>/gs)].map(m=>/w:jc w:val="center"/.test(m[0]));ok('undo takes the alignment back',c4[2]!==true,JSON.stringify(c4));
  // other text stays plain
  let C=await lib();C.key(98,1);C.type('abc');C.key(98,1);C.type(' m');C.key(97,1);C.key(99,1);C.key(133,1);C.paste('xyz');C.settle();ok('text from elsewhere is plain',!/<w:b\/>[^]*xyz/.test(xml(C).replace(/<\/w:r>/g,'</w:r>\n').split('\n').filter(l=>l.includes('xyz')).join('')));
  // cut then paste keeps format
  let D=await lib();D.key(98,1);D.type('cut');D.key(98,1);D.key(97,1);D.key(120,1);D.settle();D.paste('cut');D.settle();ok('cut then paste keeps bold',/<w:b\/>/.test(xml(D)));
 }
 console.log(R.filter(x=>x).length+'/'+R.length+' passed');process.exit(R.every(x=>x)?0:1);
})();
