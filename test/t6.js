const d=require('./drive');(async()=>{const {b,p}=await d();
 await p.keyboard.type('A table inserted by the network:');await p.keyboard.press('Enter');
 await p.mouse.click(135,47);await p.mouse.click(116,76);await p.mouse.click(80,47);
 for(const t of ['Layer','Neurons','Purpose','Glyph patch','108,316','Rasterize text and blend colors in each cell of the table so long text wraps inside its column','Line breaking','184','Width and justification']){await p.keyboard.type(t);await p.keyboard.press('Tab');}
 await p.waitForTimeout(100);await p.screenshot({path:'build/t6.png'});await b.close();})();
