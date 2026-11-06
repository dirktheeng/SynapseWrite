// Opens each file through the network and records ticks, edges, stuck state, a screenshot per page view,
// and the saved file. Usage: node test/a5_open.js OUTDIR file.docx ...
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const out=process.argv[2];fs.mkdirSync(out,{recursive:true});
(async()=>{const b=await chromium.launch();
 for(const f of process.argv.slice(3)){const n=path.basename(f,'.docx');
  const p=await b.newPage({viewport:{width:1280,height:800}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+path.resolve(__dirname,'../build/index.html'));await p.waitForFunction('window.annReady',{timeout:120000});
  const AM=+(process.env.AM||2000000000);await p.evaluate(a=>{window.annMax=a},AM);
  const t0=Date.now();const u=[...fs.readFileSync(f)];
  await p.evaluate(u=>annOpen(new Blob([new Uint8Array(u)])),u);
  const st=await p.evaluate(()=>({t:annStats.t9,e:annStats.e9,ms:annStats.k9}));
  const ms=Date.now()-t0;await p.mouse.move(1270,5);await p.keyboard.press('Control+Home');await p.waitForTimeout(100);
  await p.screenshot({path:`${out}/${n}_1.png`});
  // page through a few screens
  for(let i=2;i<=(+process.env.SHOTS||3);i++){await p.keyboard.press('PageDown');await p.keyboard.press('PageDown');await p.waitForTimeout(60);await p.screenshot({path:`${out}/${n}_${i}.png`});}
  await p.keyboard.press('Control+Home');
  let saved=null;try{const [dl]=await Promise.all([p.waitForEvent('download',{timeout:60000}),p.keyboard.press('Control+s')]);saved=`${out}/${n}_saved.docx`;await dl.saveAs(saved);}catch(ex){errs.push('save: '+ex.message.slice(0,80));}
  const sv=await p.evaluate(()=>({t:annStats.t2,e:annStats.e2}));
  console.log(JSON.stringify({n,bytes:u.length,openTicks:st.t,openEdges:st.e,wallMs:ms,stuck:st.t>=AM,saveTicks:sv.t,errs}));
  await p.close();}
 await b.close();})();
