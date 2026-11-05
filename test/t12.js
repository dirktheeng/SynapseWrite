const d=require('./drive');const fs=require('fs');(async()=>{const {b,p}=await d();
 for(const [f,o] of [[process.argv[2],process.argv[3]]]){const u=[...fs.readFileSync(f)];
  await p.evaluate(u=>annOpen(new Blob([new Uint8Array(u)])),u);await p.waitForTimeout(800);
  console.log(JSON.stringify(await p.evaluate('annStats')).slice(0,200));await p.screenshot({path:o});}
 await b.close();})();
