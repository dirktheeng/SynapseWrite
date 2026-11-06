// usage: node test/a2s.js ; sample documents built by events, screenshots to shots_a2
const d=require('./drive');const fs=require('fs');const dir=process.env.OUT||'shots_a2';
(async()=>{const {b,p,check}=await d();const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t),C=(x,y)=>p.mouse.click(x,y);
 const shot=async n=>{await p.mouse.move(1270,5);await p.waitForTimeout(60);await p.screenshot({path:dir+'/'+n+'.png'});};
 const tabs={home:[80,47],ins:[135,47],lay:[192,47],ref:[262,47],rev:[333,47]};const go=t=>C(...tabs[t]);
 const pic=async f=>{await p.evaluate(u=>annPic(new Blob([new Uint8Array(u)])),[...fs.readFileSync(f)]);await p.waitForTimeout(800);};
 // headings, lists
 await T('Document Title');await C(575,88);await K('End');await K('Enter');await C(485,88);
 await T('Heading One');await C(660,88);await K('End');await K('Enter');await C(485,88);
 await T('Body under heading with a mispeled wrd for the spell check marks.');await K('Enter');
 await T('Heading Two');await C(750,88);await K('End');await K('Enter');await C(485,88);
 await T('Body under second heading.');await K('Enter');
 await C(325,76);await T('Bullet one');await K('Enter');await T('Bullet two');await K('Enter');await K('Tab');await T('Nested bullet');await K('Enter');await K('Enter');await K('Enter');
 await C(360,76);await T('Numbered one');await K('Enter');await T('Numbered two');await K('Enter');await K('Tab');await T('Nested number');await K('Enter');await K('Enter');await K('Enter');
 await T('Final paragraph.');
 await shot('a_styles');
 await K('Shift+Home');await shot('a_sel');await K('End');await K('Enter');
 // tracked changes
 await go('rev');await C(250,76);await T('Inserted with tracking and ');await go('home');await K('Shift+Home');await K('Backspace');await go('rev');await C(250,76);await T('keep ');
 await K('Enter');await T('Comment target sentence here.');await K('Shift+Home');await C(58,76);await T('A comment long enough that it must wrap to a second line in the balloon for sure');await K('Enter');await go('home');
 await shot('b_track');
 await b.close();
 const {b:b2,p:q}=await d();{const p=q;const K=k=>p.keyboard.press(k),T=t=>p.keyboard.type(t),C=(x,y)=>p.mouse.click(x,y);const go=t=>C(...tabs[t]);
 const shot=async n=>{await p.mouse.move(1270,5);await p.waitForTimeout(60);await p.screenshot({path:dir+'/'+n+'.png'});};
 const pic=async f=>{await p.evaluate(u=>annPic(new Blob([new Uint8Array(u)])),[...fs.readFileSync(f)]);await p.waitForTimeout(800);};
 await T('Table below');await K('Enter');await go('ins');await C(116,76);await T('a1');await K('Tab');await T('b1');await K('Tab');await T('c1');await K('Tab');await T('a2');await K('Tab');await T('b2 with longer text that wraps in the cell');await K('Tab');await T('c2');
 await shot('c_table');
 const X0=770;await C(X0+132+1*20+9,102);await K('ArrowUp');await C(X0+132+3*20+9,102);await shot('c_shade');
 await K('Control+End');await K('ArrowDown');await K('Enter');await T('Text and note');await go('ref');await C(190,76);await T('First footnote text');await K('Enter');await go('home');await T(' after');
 await shot('d_note');
 await K('Enter');await pic('build/p_a.png');await T('after pic');await shot('e_pic0');
 await p.mouse.click(420,500);await shot('e_pic');
 await K('Escape');await K('Control+End');await go('ins');await C(275,76);await T('Header text');await C(1062,102);await K('Enter');await C(1062,76);await T('Footer text');await C(1062,102);await K('Enter');await shot('f_hf');
 await C(1062,76);await shot('f_hfedit');await K('Escape');
 await K('Control+Home');await K('Control+f');await T('text');await shot('g_find');await K('Enter');await shot('g_find2');await K('Escape');
 await K('Control+h');await T('text');await K('Tab');await T('word');await shot('g_repl');await K('Escape');
 await K('Control+f');await T('zzzz');await K('Enter');await shot('g_nf');await K('Escape');
 await b2.close();}
 })();
