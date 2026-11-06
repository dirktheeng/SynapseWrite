// p1: the clipboard as HTML, with real Ctrl+C and Ctrl+V in Chromium. Judged on the system clipboard's HTML, the saved .docx and the canvas.
const http=require('http'),fs=require('fs'),path=require('path'),{execSync}=require('child_process'),{chromium}=require('playwright');
const R=[];const ok=(n,c,x)=>{R.push(!!c);console.log(c?'PASS':'FAIL',n,x===undefined?'':x);};
const html=fs.readFileSync(path.resolve(__dirname,'../build/index.html'));
const xml=f=>execSync(`python3 -c "import zipfile;print(zipfile.ZipFile('${f}').read('word/document.xml').decode())"`).toString();
(async()=>{const srv=http.createServer((q,r)=>{r.setHeader('content-type','text/html');r.end(q.url.startsWith('/edit')?'<div id="ed" contenteditable="true" style="width:600px;height:200px"></div>':html);}).listen(0,'127.0.0.1');await new Promise(r=>srv.once('listening',r));const url='http://127.0.0.1:'+srv.address().port+'/';
 const b=await chromium.launch();const c=await b.newContext({viewport:{width:1280,height:800}});await c.grantPermissions(['clipboard-read','clipboard-write'],{origin:url});
 const open=async()=>{const p=await c.newPage();p.on('pageerror',e=>console.log('PAGEERR',e.message));await p.goto(url);await p.waitForFunction('window.annReady');await p.evaluate(()=>{window.annMax=30000000});await p.mouse.click(600,300);return p;};
 const save=async(p,f)=>{const [dl]=await Promise.all([p.waitForEvent('download'),p.keyboard.press('Control+s')]);await dl.saveAs(f);return xml(f);};
 const clipHtml=p=>p.evaluate(async()=>{const it=(await navigator.clipboard.read())[0];return it.types.includes('text/html')?await (await it.getType('text/html')).text():'';});
 // 1. copy out of the app: bold, italic, a size, a color, centering
 let p=await open();const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t);
 await T('Plain ');await K('Control+b');await T('bold');await K('Control+b');await T(' ');await K('Control+i');await T('italic');await K('Control+i');await K('Enter');await T('Centered line');await K('Control+e');
 await K('Control+a');await K('Control+c');await p.waitForTimeout(150);let h=await clipHtml(p);fs.writeFileSync('build/p1_clip_out.html',h);
 ok('Ctrl+C puts HTML on the system clipboard',/<p /.test(h)&&/font-weight:bold;[^"]*">bold</.test(h)&&/font-style:italic;[^"]*">italic</.test(h)&&/text-align:center/.test(h),h.slice(0,300));
 ok('and the plain text beside it',(await p.evaluate(()=>navigator.clipboard.readText())).replace(/\r/g,'')==='Plain bold italic\nCentered line');
 // 2. that HTML pastes into an ordinary editable page as formatted text
 const q=await c.newPage();await q.goto(url+'edit');await q.click('#ed');await q.keyboard.press('Control+v');await q.waitForTimeout(150);const inner=await q.evaluate(()=>document.getElementById('ed').innerHTML);
 ok('a browser editor reads the copy as bold and italic',/font-weight:\s*(bold|700)[^>]*>bold|<b>bold/.test(inner)&&/italic[^>]*>italic|<i>italic/.test(inner),inner.slice(0,300));
 // 3. and into a second document of the app (not its own copy), keeping the formats
 let p2=await open();await p2.keyboard.press('Control+v');await p2.waitForTimeout(300);let x=await save(p2,'build/p1_clip_rt.docx');
 const run=w=>new RegExp('<w:rPr>(?:(?!</w:rPr>).)*</w:rPr><w:t[^>]*>'+w);
 ok('pasted into another document: bold and italic runs',/<w:b\/>(?:(?!<\/w:rPr>).)*<\/w:rPr><w:t[^>]*>bold/.test(x)&&/<w:i\/>(?:(?!<\/w:rPr>).)*<\/w:rPr><w:t[^>]*>italic/.test(x)&&!/<w:b\/>(?:(?!<\/w:rPr>).)*<\/w:rPr><w:t[^>]*>Plain/.test(x),(x.match(/<w:body>.*<\/w:body>/)||[''])[0].slice(0,500));
 ok('and the centered paragraph',/<w:jc w:val="center"\/><\/w:pPr>(?:(?!<\/w:p>).)*Centered line/.test(x));
 await p2.close();
 // 4. HTML from another program: Word-like markup with styles, entities, a list and a comment
 const src='<html><head><style>p{color:blue}</style><title>skip me</title></head><body><!--StartFragment--><p style="text-align:right">Right <span style="font-size:20pt;color:rgb(255, 0, 0);font-family:&quot;Courier New&quot;">Red big</span> &amp; <u>under</u></p><ol><li>first</li><li>second</li></ol><ul><li><strong>dot</strong></li></ul><!--EndFragment--></body></html>';
 const plain='Right Red big & under\nfirst\nsecond\ndot';
 let p3=await open();await p3.evaluate(async([hh,tt])=>{await navigator.clipboard.write([new ClipboardItem({'text/html':new Blob([hh],{type:'text/html'}),'text/plain':new Blob([tt],{type:'text/plain'})})]);},[src,plain]);
 await p3.keyboard.press('Control+v');await p3.waitForTimeout(300);await p3.mouse.move(1270,5);await p3.waitForTimeout(50);await p3.screenshot({path:'build/p1_clip_in.png'});
 x=await save(p3,'build/p1_clip_in.docx');const body=(x.match(/<w:body>.*<\/w:body>/)||[''])[0];
 ok('a right aligned paragraph',/<w:jc w:val="right"\/><\/w:pPr>(?:(?!<\/w:p>).)*Right/.test(body),body.slice(0,400));
 ok('a 20 pt red Courier New run',/<w:rFonts w:ascii="Courier New"[^>]*\/>(?:(?!<\/w:rPr>).)*<w:color w:val="FF0000"\/>(?:(?!<\/w:rPr>).)*<w:sz w:val="40"\/>(?:(?!<\/w:rPr>).)*<\/w:rPr><w:t[^>]*>Red big/.test(body));
 ok('an entity and an underline',/ &amp; </.test(body)&&/<w:u w:val="single"\/><\/w:rPr><w:t[^>]*>under/.test(body));
 const paras=(body.match(/<w:p>.*?<\/w:p>/g)||[]);const num=paras.map(p_=>(p_.match(/<w:numId w:val="(\d+)"/)||[])[1]);
 ok('numbered and bulleted items as list paragraphs',paras.length>=4&&num[1]&&num[1]===num[2]&&num[3]&&num[3]!==num[1],JSON.stringify(num));
 ok('bold inside the bullet item',/<w:b\/>(?:(?!<\/w:rPr>).)*<\/w:rPr><w:t[^>]*>dot/.test(body));
 ok('style and title text are not pasted',!/skip me|color:blue/.test(body));
 // the canvas: red ink drawn
 const red=await p3.evaluate(()=>{const d=document.getElementById('screen').getContext('2d').getImageData(0,174,1262,600).data;let n=0;for(let i=0;i<d.length;i+=4)if(d[i]>180&&d[i+1]<80&&d[i+2]<80)n++;return n;});ok('red text drawn',red>100,red);
 // 5. one undo takes the whole paste back
 await p3.keyboard.press('Control+z');await p3.waitForTimeout(200);x=await save(p3,'build/p1_clip_undo.docx');ok('one undo removes the paste',!/Red big|first|dot/.test(x),(x.match(/<w:body>.*<\/w:body>/)||[''])[0].slice(0,300));
 await b.close();srv.close();const f=R.filter(v=>!v).length;console.log(R.length-f,'passed',f,'failed');process.exit(f?1:0);})();
