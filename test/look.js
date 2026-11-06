// Pointer, File screen, glyph spacing, and clipboard. Driven by real input events; judged on the canvas image.
const http=require('http'),fs=require('fs'),path=require('path'),{chromium}=require('playwright');let fails=0,n=0;
const ok=(name,c,x)=>{n++;if(!c)fails++;console.log(c?'PASS':'FAIL',name,x===undefined?'':x);};
const html=fs.readFileSync(path.resolve(__dirname,'../build/index.html'));
const fb=async(p,x=0,y=0,w=1280,h=800)=>Buffer.from(await p.evaluate(([x,y,w,h])=>{const d=document.getElementById('screen').getContext('2d').getImageData(x,y,w,h).data,o=new Uint8Array(d.length/4*3);for(let i=0,j=0;i<d.length;i+=4){o[j++]=d[i];o[j++]=d[i+1];o[j++]=d[i+2];}let s='';for(let i=0;i<o.length;i+=32768)s+=String.fromCharCode.apply(null,o.subarray(i,i+32768));return btoa(s);},[x,y,w,h]),'base64');
const same=(a,b)=>a.equals(b);
// the sprite: pixels that differ from the hidden image, relative to the hot spot
// mask of pixels the sprite turned black; white fill can vanish on white, so shapes are compared on black ink
const sig=async(p,x,y)=>{await p.mouse.move(x,y);const X0=Math.max(0,x-12),Y0=Math.max(0,y-10),W=Math.min(28,1280-X0),H=Math.min(30,800-Y0);const a=await fb(p,X0,Y0,W,H);await p.evaluate(()=>annDispatch(12));const b=await fb(p,X0,Y0,W,H);const s=new Set();for(let j=0;j<H;j++)for(let i=0;i<W;i++){const k=3*(j*W+i);if(a[k]<40&&a[k+1]<40&&a[k+2]<40&&(b[k]>=40||b[k+1]>=40))s.add((X0+i-x)+','+(Y0+j-y));}return {s,cnt:s.size};};
const like=(a,b)=>{let c=0;for(const k of a.s)if(b.s.has(k))c++;return c/Math.max(1,a.s.size+b.s.size-c)>0.7;};
(async()=>{const srv=http.createServer((q,r)=>{r.setHeader('content-type','text/html');r.end(html);}).listen(0,'127.0.0.1');await new Promise(r=>srv.once('listening',r));const url='http://127.0.0.1:'+srv.address().port+'/';
 const b=await chromium.launch();
 const open=async(opts={},init)=>{const c=await b.newContext({viewport:{width:1280,height:800},...opts});if(init)await c.addInitScript(init);const p=await c.newPage();p.on('pageerror',e=>console.log('PAGEERR',e.message));await p.goto(url);await p.waitForFunction('window.annReady');return {c,p};};
 {const {p}=await open();
  ok('native cursor hidden on canvas',await p.evaluate(()=>getComputedStyle(document.getElementById('screen')).cursor)==='none');
  await p.keyboard.type('Sample text for the pointer');
  const ribbon=await sig(p,700,140),gray=await sig(p,100,500),status=await sig(p,500,778),scroll=await sig(p,1270,500),page=await sig(p,700,600),text=await sig(p,340,296),margin=await sig(p,260,500),btn=await sig(p,125,102),box=await sig(p,160,75);
  ok('arrow has ink',ribbon.cnt>40,ribbon.cnt);ok('same arrow on ribbon and gray',like(ribbon,gray));ok('same arrow on status bar',like(ribbon,status));ok('same arrow on scrollbar',like(ribbon,scroll));ok('arrow over a button',like(btn,ribbon));
  ok('I-beam differs from arrow',!like(page,ribbon)&&page.cnt>10,page.cnt);ok('I-beam over text same as page',like(text,page));ok('I-beam in the font box',like(box,page));ok('left margin arrow differs',!like(margin,ribbon)&&!like(margin,page)&&margin.cnt>10);
  // no trails, and the exact image comes back
  await p.evaluate(()=>annDispatch(12));await p.keyboard.press('End');const A=await fb(p);
  for(let i=0;i<40;i++)await p.mouse.move(40+i*30,20+i*19);await p.mouse.move(600,500);await p.keyboard.press('End');
  const M=await fb(p);let out=0;for(let j=0;j<800;j++)for(let i=0;i<1280;i++){if(i>=588&&i<616&&j>=490&&j<520)continue;const k=3*(j*1280+i);if(M[k]!==A[k]||M[k+1]!==A[k+1]||M[k+2]!==A[k+2])out++;}
  ok('no trails outside the pointer',out===0,out);await p.evaluate(()=>annDispatch(12));await p.keyboard.press('End');ok('hiding restores the identical image',same(A,await fb(p)));
  // pointer over text the caret blinks under, then a paint: nothing is left behind
  await p.mouse.move(345,296);await p.keyboard.type(' more');await p.mouse.move(600,500);await p.evaluate(()=>annDispatch(12));const B1=await fb(p);
  const {p:q}=await open();await q.keyboard.type('Sample text for the pointer more');await q.evaluate(()=>annDispatch(12));ok('painting under the pointer leaves no sprite',same(B1,await fb(q)));
  // cost
  const t=await p.evaluate(()=>{const ts=[];for(let i=0;i<300;i++){annDispatch(11,600+(i%50),400+(i%40));ts.push(annStats.ms);}ts.sort((a,b)=>a-b);return [ts[150],ts[285],annStats.edges];});ok('pointer move under 3 ms',t[1]<3,'median '+t[0].toFixed(2)+' p95 '+t[1].toFixed(2)+' edges '+t[2]);
  // click still hits with the sprite on top
  await p.keyboard.press('Control+a');await p.mouse.move(125,102);await p.mouse.down();await p.mouse.up();await p.mouse.move(600,500);await p.evaluate(()=>annDispatch(12));const X1=await fb(p);
  await p.mouse.move(600,500);await p.evaluate(()=>annDispatch(12));await p.keyboard.press('Control+b');await p.keyboard.press('Control+b');await p.evaluate(()=>annDispatch(12));ok('button click under the pointer',same(X1,await fb(p)));
 }
 {const {p}=await open();await p.mouse.click(190,47);await p.waitForTimeout(30);await p.evaluate(()=>annDispatch(12));const lay=await fb(p);await p.mouse.move(127,47);await p.mouse.click(127,47);await p.evaluate(()=>annDispatch(12));
  // insert a table: border shape
  await p.mouse.click(40,75);await p.waitForTimeout(100);const page=await sig(p,700,600);
  let best=null;for(let x=620;x<640&&!best;x+=2){const s=await sig(p,x,335);if(!like(s,page)&&s.cnt>10){const arrow=await sig(p,100,500);if(!like(s,arrow))best=[x,s];}}
  ok('resize arrow over a table border',!!best,best&&best[0]);
 }
 {const {p}=await open();await p.evaluate(()=>annDispatch(12));const A=await fb(p);await p.mouse.click(28,47);await p.waitForTimeout(30);await p.evaluate(()=>annDispatch(12));const F=await fb(p);ok('File screen covers the app',!same(A,F));
  await p.mouse.move(90,92);await p.waitForTimeout(20);await p.evaluate(()=>annDispatch(12));ok('File screen hover',!same(F,await fb(p)));
  await p.mouse.click(30,28);await p.mouse.move(1270,5);await p.waitForTimeout(30);await p.evaluate(()=>annDispatch(12));ok('Back returns to the identical app',same(A,await fb(p)));
  await p.keyboard.type('gone');await p.mouse.click(28,47);await p.mouse.click(90,92);await p.mouse.move(1270,5);await p.waitForTimeout(30);await p.evaluate(()=>annDispatch(12));ok('New clears the document',same(A,await fb(p)));
 }
 // glyph spacing: white gap between the ink of neighbors
 {const {p}=await open();const gap=async s=>{await p.keyboard.press('Control+a');await p.keyboard.press('Delete');await p.keyboard.type(s);await p.keyboard.press('Control+Home');await p.mouse.move(1270,5);await p.waitForTimeout(600);
   return await p.evaluate(()=>{const c=document.getElementById('screen'),d=c.getContext('2d').getImageData(320,288,300,20).data;const cols=[];for(let x=0;x<300;x++){let m=255;for(let y=0;y<20;y++)m=Math.min(m,d[4*(y*300+x)]);cols.push(m<170);}const runs=[];let x=0;while(x<300){if(!cols[x]){let k=x;while(k<300&&!cols[k])k++;runs.push(k-x);x=k;}else x++;}return runs.slice(1,-1);});};
  const avg=a=>a.reduce((u,v)=>u+v,0)/(a.length||1);const me=await gap('mememememememe'),ne=await gap('nenenenenenene');const after=a=>a.filter((_,i)=>i%2===0);
  // on ink: two gaps per pair (m to e, e to next)
  ok('gap after m close to gap after n',Math.abs(avg(after(me))-avg(after(ne)))<=0.75,'m '+avg(after(me)).toFixed(2)+' n '+avg(after(ne)).toFixed(2));
  ok('no gap after m over 2 px at body size',Math.max(...after(me))<=2,Math.max(...after(me)));
 }
 // clipboard, with permission
 {const {c,p}=await open();await c.grantPermissions(['clipboard-read','clipboard-write'],{origin:url});
  await p.mouse.click(600,300);await p.keyboard.type('hello');await p.keyboard.press('Control+a');await p.keyboard.press('Control+c');await p.keyboard.press('End');await p.waitForTimeout(100);
  ok('Ctrl+C reaches the system clipboard',await p.evaluate(()=>navigator.clipboard.readText())==='hello');
  await p.keyboard.press('ArrowRight');await p.keyboard.press('Control+v');await p.waitForTimeout(150);await p.mouse.move(1270,5);await p.evaluate(()=>annDispatch(12));const a=await fb(p);
  const {p:q}=await open();await q.keyboard.type('hellohello');await q.mouse.move(1270,5);await q.evaluate(()=>annDispatch(12));ok('real Ctrl+V pastes',same(a,await fb(q)));
  await p.evaluate(()=>navigator.clipboard.writeText(' world'));await p.keyboard.press('Control+v');await p.waitForTimeout(150);await p.evaluate(()=>annDispatch(12));const a2=await fb(p);await q.keyboard.type(' world');await q.evaluate(()=>annDispatch(12));ok('Ctrl+V pastes text from outside',same(a2,await fb(q)));
  ok('canvas keeps focus after paste',await p.evaluate(()=>document.activeElement.id)==='screen');
  await p.evaluate(()=>navigator.clipboard.writeText('!'));await p.mouse.click(28,90);await p.waitForTimeout(150);await p.mouse.move(1270,5);await p.evaluate(()=>annDispatch(12));const a3=await fb(p);await q.keyboard.type('!');await q.mouse.move(1270,5);await q.waitForTimeout(30);await q.evaluate(()=>annDispatch(12));ok('Paste button with permission',same(a3,await fb(q)));
 }
 // clipboard denied, as in a frame without the permission
 {const deny=()=>{const n=navigator.clipboard;Object.defineProperty(navigator,'clipboard',{value:{readText:()=>Promise.reject(new Error('denied')),writeText:()=>Promise.reject(new Error('denied'))}});document.execCommand=()=>false;};
  const {p}=await open({},deny);await p.mouse.click(600,300);await p.keyboard.type('abc');await p.evaluate(()=>annDispatch(12));const A=await fb(p);
  await p.mouse.click(28,90);await p.waitForTimeout(100);await p.mouse.move(1270,5);await p.evaluate(()=>annDispatch(12));const M=await fb(p);let st=0;for(let j=777;j<800;j++)for(let i=0;i<640;i++)if(M[3*(j*1280+i)]!==A[3*(j*1280+i)])st++;ok('denied Paste button draws a status message',st>50,st);
  await p.keyboard.type('d');await p.evaluate(()=>annDispatch(12));const G=await fb(p);const {p:q}=await open();await q.keyboard.type('abcd');await q.mouse.move(1270,5);await q.waitForTimeout(20);await q.evaluate(()=>annDispatch(12));
  let s2=0;const Q=await fb(q);for(let j=777;j<800;j++)for(let i=0;i<640;i++)if(G[3*(j*1280+i)]!==Q[3*(j*1280+i)])s2++;ok('message ends on the next key',s2===0,s2);
  // copy and cut with write denied still paste inside the app
  await p.keyboard.press('Control+a');await p.mouse.click(84,97);await p.waitForTimeout(100);await p.keyboard.press('End');await p.keyboard.press('ArrowRight');await p.mouse.click(28,90);await p.waitForTimeout(100);await p.keyboard.type('z');await p.mouse.move(1270,5);await p.evaluate(()=>annDispatch(12));const I=await fb(p);
  await q.keyboard.press('End');await q.keyboard.type('abcdz');await q.evaluate(()=>annDispatch(12));ok('denied clipboard: Copy then Paste button works inside the app',same(I,await fb(q)));
  await p.keyboard.press('Control+a');await p.mouse.click(84,75);await p.waitForTimeout(100);await p.keyboard.press('Control+v');await p.waitForTimeout(150);
  await p.keyboard.type('!');await p.mouse.move(1270,5);await p.evaluate(()=>annDispatch(12));const I2=await fb(p);await q.keyboard.type('!');await q.evaluate(()=>annDispatch(12));ok('denied clipboard: Cut then Ctrl+V works inside the app',same(I2,await fb(q)));
 }
 console.log(n-fails,'of',n);await b.close();srv.close();process.exit(fails?1:0);})();
