const {chromium}=require('playwright');
module.exports=async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:800}});
 p.on('pageerror',e=>console.log('PAGEERR',e.message));
 await p.goto('file://'+require('path').resolve(__dirname,'../build/index.html'));await p.waitForFunction('window.annReady',{timeout:60000});return {b,p};};
