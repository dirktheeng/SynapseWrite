// Records the real app through real browser events. Run from the repo root after ./make.sh: node docs/figures/src/hero.js OUTDIR
const {chromium}=require('playwright'),path=require('path'),fs=require('fs');const out=process.argv[2];fs.mkdirSync(out,{recursive:true});
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:800}});
await p.goto('file://'+path.resolve('build/index.html'));await p.waitForFunction('window.annReady',{timeout:120000});
let n=0;const snap=async(k=1)=>{const s=await p.screenshot();for(let i=0;i<k;i++)fs.writeFileSync(`${out}/f${String(n++).padStart(4,'0')}.png`,s);};
const type=async(t,st=2)=>{for(let i=0;i<t.length;i++){await p.keyboard.type(t[i]);if(i%st==st-1)await snap();}await snap();};
await p.mouse.move(640,420);await snap(6);
await type('SynapseWrite',1);await p.keyboard.press('Control+a');await p.mouse.move(880,95);await snap(3);await p.mouse.click(880,95);await snap(6);await p.keyboard.press('Control+End');await p.keyboard.press('Enter');await p.keyboard.press('Control+a');await p.keyboard.press('Control+End');
await p.mouse.click(545,95);await snap(2);
await type('Every pixel on this screen, each letter, and every button is computed by a single neural network whose weights were written by a program, not trained.');await snap(4);
await p.keyboard.press('Enter');await p.mouse.click(229,75);await p.mouse.move(170,142);await snap(8);await p.mouse.click(170,142);await snap(2);
await type('Fonts are compiled into neurons.',2);await snap(3);
await p.keyboard.press('Enter');await p.keyboard.press('Control+b');await type('Bold',1);await p.keyboard.press('Control+b');await p.keyboard.press('Control+i');await type(' and italic',2);await p.keyboard.press('Control+i');await snap(4);
for(let i=0;i<14;i++)await p.keyboard.press('Shift+ArrowLeft');await snap(6);await p.keyboard.press('Control+End');
await p.mouse.move(128,47);await p.mouse.click(128,47);await snap(8);await p.mouse.move(337,47);await p.mouse.click(337,47);await snap(8);await p.mouse.move(60,47);await p.mouse.click(60,47);await snap(14);
console.log('frames',n);await b.close();})();
