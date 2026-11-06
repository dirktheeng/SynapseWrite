// Runs a fixed event script headless and writes the framebuffer at each checkpoint to build/fb_<n>.raw,
// so two builds of the network can be compared pixel by pixel. Usage: node test/fbdump.js
const fs=require('fs');const load=require(process.env.LOADJS||process.cwd()+'/test/load');
load().then(({e,h,bank})=>{
 const D=(k,a=0,b=0,c=0)=>{e.inject(h.ev[0],k);if(a)e.inject(h.ev[1],a);if(b)e.inject(h.ev[2],b);if(c)e.inject(h.ev[3],c);return e.run(h.halt,80000000);};
 const T=s=>{for(const c of s)D(2,c=='\n'?13:c.charCodeAt(0));};const K=(c,m=0)=>D(2,typeof c=='string'?c.charCodeAt(0):c,m);const C=(x,y)=>{D(3,x,y);D(4,x,y);};
 let n=0;const snap=()=>{for(let i=0;i<8;i++)D(7);const f=new Uint8Array(e.memory.buffer,e.p_fb(),1280*800*4);fs.writeFileSync('build/fb_'+(n++)+'.raw',f);};
 const paste=s=>{const b=bank();for(let i=0;i<s.length;i++)b[h.cb2+i]=s.charCodeAt(i);D(8,0,0,s.length);};
 D(1);snap();
 T('Plain text with words\nSecond line ');K('b',1);T('bold ');K('b',1);K('i',1);T('italic ');K('i',1);K('u',1);T('under');K('u',1);T(' done\n');snap();
 C(660,88);T('Heading large');K(133);K(13);C(485,88);T('Body again');K(13);T('Serif');K(132,2);C(149,75);K(133);K(13);snap();
 T('Red text here');K(132,2);C(239,102);snap();K(133);K(13);
 K('a',1);snap();K(128);
 paste('one two\nthree\n'+('word word word word word word word word word word word word word word word word word word word word word word word '.repeat(4)+'\n').repeat(5));snap();
 D(6,0,0,1300);snap();K('z',1);snap();K('y',1);snap();K('a',1);K(127);snap();
 const u=fs.readFileSync('build/p_rgb.png');{const b=bank();for(let i=0;i<u.length;i++)b[h.file+i]=u[i];}D(10,0,0,u.length);snap();
 K('z',1);snap();
 console.log('snaps',n);
}).catch(x=>console.log(x.stack));
