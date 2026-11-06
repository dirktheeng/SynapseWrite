// Chrome look: driven by real clicks, judged on canvas pixels.
const fs=require('fs'),path=require('path'),{chromium}=require('playwright');let fails=0,n=0;
const ok=(name,c,x)=>{n++;if(!c)fails++;console.log(c?'PASS':'FAIL',name,x===undefined?'':x);};
const ids=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../build/ui_ids.json')));
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:800}});p.on('pageerror',e=>console.log('PAGEERR',e.message));
 await p.goto('file://'+path.resolve(__dirname,'../build/index.html'));await p.waitForFunction('window.annReady',{timeout:180000});
 const px=(x,y,w,h)=>p.evaluate(([x,y,w,h])=>Array.from(document.getElementById('screen').getContext('2d').getImageData(x,y,w,h).data),[x,y,w,h]);
 const cols=async(x,y,w,h)=>{const d=await px(x,y,w,h),s=new Set();for(let i=0;i<d.length;i+=4)s.add(d[i]+','+d[i+1]+','+d[i+2]);return s;};
 const settle=async()=>{await p.waitForTimeout(120);};
 const click=async(a)=>{const c=ids[a];await p.mouse.click(c[0],c[1]);await settle();await p.mouse.move(1270,5);await settle();};
 const has=(s,c)=>s.has(c.join(','));
 // search box: text sits on the same color as the box, at rest and on hover
 {const s=await cols(462,6,356,20);ok('search box has no text halo at rest',!has(s,[68,119,187]));
  const c=ids['c:225'];await p.mouse.move(c[0]+100,c[1]);await settle();const h=await cols(490,8,40,16);ok('search hover recolors behind text',!has(h,[51,119,204]),[...h].length);await p.mouse.move(1270,5);await settle();}
 // every labelled small command on these tabs carries art in the icon column, left of its label
 const SM={1:[208,209,210,211,212,213,220,221,222,223,224,203,204,205,201,240,241,242,246],2:[210,211,212,213,214,243,244],3:[208],4:[208,204,201]};
 const W={1:{208:84,209:84,210:84,211:76,212:76,213:76,220:94,221:106,222:106,223:94,224:106,203:88,204:88,205:92,201:92,240:62,241:62,242:62,246:94},2:{210:84,211:84,212:70,213:70,214:70,243:70,244:70},3:{208:102},4:{208:118,204:76,201:76}};
 for(const t of [1,2,3,4]){await click(`${t}:${229+t}`);for(const a of SM[t]){const c=ids[`${t}:${a}`];if(!c){ok(`control ${t}:${a} exists`,false);continue;}
   const x0=c[0]-(W[t][a]>>1)+3,s=await cols(x0,c[1]-8,16,16);s.delete('243,243,243');ok(`tab ${t} id ${a} has an icon`,s.size>=1,s.size);}}
 // ruler: quarter inch marks evenly spaced from the margin, ticks reach the last half inch
 await click('0:229');
 const ticks=async()=>{const d=await px(0,162,1280,1),o=[];for(let x=0;x<1280;x++){const i=x*4;if(d[i]===138&&d[i+1]===136&&d[i+2]===134)o.push(x);}return o;};
 const t0=await ticks();ok('tick marks exist',t0.length>=12,t0.length);const diffs=t0.slice(1).map((v,i)=>v-t0[i]);
 ok('ticks fall on the quarter inch grid',t0.every(x=>(x-319)%24===0),t0.join(' '));ok('ticks reach past 6 inches',t0[t0.length-1]>=319+6*96,t0[t0.length-1]);
 await click('2:231');await click('2:213');const t1=await ticks();
 ok('narrow margins move the scale',t1[0]!==t0[0]&&(t1[0]-(319-48))%24===0,t1.slice(0,3).join(' '));
 ok('narrow margins extend the scale',t1[t1.length-1]>t0[t0.length-1],t1[t1.length-1]);
 await p.screenshot({path:'build/a1_narrow.png'});
 await click('2:212');await click('0:229');
 // File screen: nav hover leaves no box around the label
 await p.mouse.click(ids['0:226'][0],ids['0:226'][1]);await settle();await p.mouse.move(100,136);await settle();const f=await cols(40,118,120,36);ok('File nav hover has no halo',!has(f,[17,85,187]));await p.mouse.move(1270,5);
 await p.mouse.click(30,28);await settle();
 console.log(`${n-fails}/${n}`);await b.close();process.exit(fails?1:0);})();
