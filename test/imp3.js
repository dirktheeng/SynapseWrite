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
 console.log(R.filter(x=>x).length+'/'+R.length+' passed');process.exit(R.every(x=>x)?0:1);
})();
