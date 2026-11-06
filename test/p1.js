// p1: tier 1 gaps. Find codes, Ctrl+Alt shortcuts and more. Driven by events, judged on images and saved files.
const lib=require('./a7_lib'),{xml,paras,count}=require('./imp3_lib');const R=[];const ok=(n,c,x)=>{R.push(!!c);console.log(c?'PASS':'FAIL',n,x===undefined?'':x);};
const only=process.argv[2];
const yel=(r,g,b)=>r>200&&g>180&&b<170; // match tint
(async()=>{
 if(!only||only=='find'){
  // ^t finds a tab: select it and type over it
  let A=await lib();A.paste('name\tvalue\nplain line\n');A.settle();A.key(102,1);A.type('e^tv');A.settle();A.shot('build/p1_find1.png');
  const h=count(A,319,900,174,776,yel);ok('a ^t match is tinted',h>40,h);
  A.key(13);A.settle();A.key(27);A.settle();A.type('X');A.settle();let p=paras(xml(A));ok('^t finds the tab',p[0]=='namXalue',JSON.stringify(p));
  // replace all with codes: tabs to ^l line breaks
  A=await lib();A.paste('a\tb\tc\n');A.settle();A.key(104,1);A.type('^t');A.key(9);A.type('^l');A.key(13);A.settle();A.key(13);A.settle();A.key(13);A.settle();A.key(27);A.settle();
  let x=xml(A);ok('^t replaced by ^l writes line breaks',/a<\/w:t><w:br\/><w:t[^>]*>b<\/w:t><w:br\/><w:t[^>]*>c/.test(x)&&!/w:tab/.test(x),(x.match(/<w:body>.*<\/w:body>/)||[''])[0].slice(0,300));
  // ^# any digit, ^$ any letter, ^? any character
  A=await lib();A.paste('code x7y and q42\n');A.settle();A.key(102,1);A.type('^$^#^#');A.key(13);A.settle();A.key(27);A.settle();A.type('Z');A.settle();p=paras(xml(A));ok('^$^#^# finds a letter and two digits',p[0]=='code x7y and Z',JSON.stringify(p));
  A=await lib();A.paste('cat cot cut\n');A.settle();A.key(104,1);A.type('c^?t');A.key(9);A.type('dog');A.key(13);A.settle();A.key(13);A.settle();A.key(13);A.settle();A.key(13);A.settle();A.key(27);A.settle();p=paras(xml(A));ok('^? matches any character in a replace',p[0]=='dog dog dog',JSON.stringify(p));
  // ^^ is a literal caret, so ^^p searches for the two characters ^p
  A=await lib();A.paste('up ^p down\nnext\n');A.settle();A.key(102,1);A.type('^^p');A.key(13);A.settle();A.key(27);A.settle();A.type('M');A.settle();p=paras(xml(A));ok('^^p finds a literal ^p',p[0]=='up M down'&&p[1]=='next',JSON.stringify(p));
  // codes with a mark
  A=await lib();A.paste('end1\nstart\n');A.settle();A.key(102,1);A.type('^#^ps');A.key(13);A.settle();A.key(27);A.settle();A.type('Q');A.settle();p=paras(xml(A));ok('a code and ^p together',p[0]=='endQtart',JSON.stringify(p));
  // the count: four digits
  A=await lib();A.paste('1 a 2 b 3 c 4\n');A.settle();A.key(102,1);A.type('^#');A.settle();A.shot('build/p1_find2.png');const n=count(A,319,900,174,776,yel);ok('every digit is tinted',n>40,n);
 }
 const f=R.filter(x=>!x).length;console.log(R.length-f,'passed',f,'failed');process.exit(f?1:0);
})();
