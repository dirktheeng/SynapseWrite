// p1: tier 1 gaps. Find codes, Ctrl+Alt shortcuts and more. Driven by events, judged on images and saved files.
const lib=require('./a7_lib'),{xml,paras,count}=require('./imp3_lib');const R=[];const ok=(n,c,x)=>{R.push(!!c);console.log(c?'PASS':'FAIL',n,x===undefined?'':x);};
const only=process.argv[2];
// a key through the glue's path: key name code units, length and raw modifier bits (ctrl 1, shift 2, meta 4, alt 16), cooked by the input network
const rk=(A,name,m)=>{for(let i=0;i<6;i++)A.e.inject(A.h.keyv[i],name.charCodeAt(i)||0);A.e.inject(A.h.keyl,name.length);return A.raw(2,0,m,Date.now()%100000+200000);};
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

 if(!only||only=='alt'){
  // Ctrl+Alt+1 is Heading 1 (not single spacing), Ctrl+Alt+2 Heading 2
  let A=await lib();A.type('Top');A.key(13);A.type('Sub');A.key(13);A.type('Body');A.settle();A.key(132,1);rk(A,'1',17);A.settle();A.key(131);rk(A,'2',17);A.settle();A.shot('build/p1_alt1.png');
  let x=xml(A);const st=(x.match(/<w:p>.*?<\/w:p>/g)||[]).map(p=>(p.match(/w:pStyle w:val="(\w+)"/)||[])[1]);ok('Ctrl+Alt+1 and 2 apply Heading 1 and 2',st[0]=='Heading1'&&st[1]=='Heading2'&&!st[2],JSON.stringify(st));
  ok('Ctrl+Alt+1 does not set single spacing',!/w:line="240"/.test((x.match(/<w:p>.*?<\/w:p>/)||[''])[0]));
  // symbols
  A=await lib();A.type('x');rk(A,'c',17);rk(A,'r',17);rk(A,'t',17);rk(A,'.',17);A.settle();x=xml(A);ok('Ctrl+Alt+C R T . type the signs and an ellipsis',x.includes('x©®™…'),(x.match(/<w:t[^>]*>[^<]*/g)||[]).join('|'));
  // AltGr arrives as Ctrl+Alt: its character types (an at sign and a euro sign); Ctrl+Alt+C is not a copy
  A=await lib();A.type('mail');rk(A,'@',17);rk(A,'\u20ac',17);A.type('x');A.settle();x=xml(A);ok('AltGr characters type',x.includes('mail@\u20acx'),(x.match(/<w:t[^>]*>[^<]*/g)||[]).join('|'));
  // a footnote and a comment
  A=await lib();A.type('Note here');rk(A,'f',17);A.settle();A.type('the note');A.settle();x=xml(A);const fn=A.part?A.part('word/footnotes.xml'):'';
  ok('Ctrl+Alt+F inserts a footnote',/w:footnoteReference/.test(x),(x.match(/<w:body>.*<\/w:body>/)||[''])[0].slice(0,300));
  A=await lib();A.type('Talk');rk(A,'m',17);A.settle();A.type('a remark');A.key(13);A.settle();A.shot('build/p1_alt2.png');x=xml(A);ok('Ctrl+Alt+M adds a comment',/w:commentReference|w:commentRangeStart/.test(x));
 }

 if(!only||only=='ribbon'){
  // Layout > Text Wrapping and Column Break
  let A=await lib();A.type('left');A.click(182,47);A.settle();A.click(1100,96);A.settle();A.type('right');A.click(1100,74);A.settle();A.type('next');A.settle();A.shot('build/p1_rib1.png');
  let x=xml(A);ok('Text Wrapping writes a line break',/left<\/w:t><w:br\/><w:t[^>]*>right/.test(x),(x.match(/<w:body>.*<\/w:body>/)||[''])[0].slice(0,500));
  ok('Column Break writes a column break',/<w:br w:type="column"\/><\/w:r>(?:(?!<\/w:p>).)*next/.test(x));
  A=await lib();A.type('a');A.click(182,47);A.settle();A.click(1100,74);A.settle();A.key('z',1);A.settle();x=xml(A);ok('the column break undoes',!/w:type="column"/.test(x)&&/>a</.test(x));
  // Insert > Comment and Footnote
  A=await lib();A.type('Talk');A.click(127,47);A.settle();A.click(1100,96);A.settle();A.type('remark');A.key(13);A.settle();x=xml(A);ok('Insert > Comment adds a comment',/w:commentReference|w:commentRangeStart/.test(x));
  A.click(1100,118);A.settle();A.type('fn');A.settle();x=xml(A);ok('Insert > Footnote adds a footnote',/w:footnoteReference/.test(x));
  // View > Read Mode, then View > Print Layout from the read view is not reachable (bars covered), so Esc; the button acts in print layout without harm
  A=await lib();A.type('stay');A.click(372,47);A.settle();const h0=A.hash(0,800);A.click(398,74);A.settle();A.shot('build/p1_rib2.png');A.type('!');A.settle();ok('Print Layout in print layout keeps editing',/stay!/.test(xml(A)));
 }

 if(!only||only=='zoom'){
  // zoom in from 100 percent up to 500 by the status bar plus, as Word goes to 500
  const ink=(A)=>{const f=A.fb();let t=-1,b=-1;for(let y=174;y<770;y++){for(let x=20;x<1262;x++){const i=(y*1280+x)*4;if(f[i]<90&&f[i+1]<90&&f[i+2]<90){if(t<0)t=y;b=y;break;}}}return b-t+1;};
  let A=await lib();A.type('Zoom Hello');A.settle();const h1=ink(A);for(let i=0;i<4;i++){A.click(1232,788);A.settle();}A.key(128);A.key(130);A.settle();const h2=ink(A);
  for(let i=0;i<4;i++){A.click(1232,788);A.settle();}A.key(128);A.key(130);A.settle();A.shot('build/p1_z500.png');const h5=ink(A);
  ok('500 percent draws text five times as tall as 100',Math.abs(h5/h1-5)<0.8,[h1,h2,h5]);
  const q=A=>{A.key(128);A.key(130);A.settle();return A.hash(174,800);};const s5=q(A);A.click(1232,788);A.settle();ok('zoom stops at 500',q(A)===s5);
  // typing at 500 percent lands at the caret, then back to 100 is pixel equal to one that never zoomed
  A.type('!');A.settle();for(let i=0;i<8;i++){A.click(1096,788);A.settle();}
  A.key(132,1);A.settle();ok('typing at 500 lands at the caret, and back at 100 the text is its own size',/Zoom Hello!/.test(xml(A))&&ink(A)===h1,ink(A));
  // the View tab steps up to 500 too
  let C=await lib();C.type('Zoom Hello');C.click(372,47);C.settle();for(let i=0;i<8;i++){C.click(210,74);C.settle();}C.key(128);C.key(130);C.settle();C.shot('build/p1_z500v.png');ok('View > Zoom In reaches 500',Math.abs(ink(C)/h1-5)<0.8,ink(C));
 }

 if(!only||only=='land'){
  // a landscape page at 150 percent: the thumb is the window's share of the page, and it drags with the pointer
  const thumb=A=>{const f=A.fb();let a=-1,b=-1;for(let x=0;x<1262;x++){const i=(770*1280+x)*4;if(f[i]==205&&f[i+1]==205&&f[i+2]==205){if(a<0)a=x;b=x;}}return [a,b];};
  let A=await lib();A.type('Wide page');A.click(182,47);A.settle();A.click(100,96);A.settle();A.click(75,47);A.settle();A.click(1232,788);A.settle();A.click(1232,788);A.settle();A.shot('build/p1_land.png');
  const t0=thumb(A),w=t0[1]-t0[0]+1,want=Math.round(1262*1262/(1056*1.5+40));ok('landscape thumb is the window share of the page',Math.abs(w-want)<=2,[t0,want]);
  const cx=(t0[0]+t0[1])>>1;A.raw(3,cx,770,1e6);A.settle();A.raw(22,cx+60,770,1);A.settle();A.raw(22,cx+150,770,1);A.settle();const t1=thumb(A);A.raw(4,cx+150,770);A.settle();
  ok('the landscape thumb drags with the pointer',Math.abs(t1[0]-t0[0]-150)<=2,[t0,t1]);
 }
 const f=R.filter(x=>!x).length;console.log(R.length-f,'passed',f,'failed');process.exit(f?1:0);
})();
