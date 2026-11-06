const {chromium}=require('playwright');
module.exports=async()=>{const b=await chromium.launch();const p=require('./remap')(await b.newPage({viewport:{width:1280,height:800}}));
 p.on('pageerror',e=>console.log('PAGEERR',e.message));
 await p.goto('file://'+require('path').resolve(__dirname,'../build/index.html'));await p.waitForFunction('window.annReady',{timeout:60000});await p.evaluate(a=>{window.annMax=a},+(process.env.AM||6000000));
 const st=JSON.parse(require('fs').readFileSync(require('path').resolve(__dirname,'../build/states.json')));
 const check=async(l)=>{const r=await p.evaluate(st=>{const on=[];for(const k in st)if(annVal(+k))on.push(st[k]);return [annStats.ticks,on];},st);if(r[0]>=+(process.env.AM||6000000))console.log('STUCK',l||'',r[1].join(','));return r;};
 return {b,p,check};};
