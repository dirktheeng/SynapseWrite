// Ribbon coordinates moved with the Word style layout. Tests keep their old coordinates and assertions;
// this table sends each old control to the same command in the new layout, found by object id from the build.
// Old commands that now live in a dropdown become two real clicks: open the dropdown, click the cell.
const ids=JSON.parse(require('fs').readFileSync(require('path').resolve(__dirname,'../build/ui_ids.json')));
const BIU={201:[125,102],202:[151,102],203:[177,102]};
const home=[[8,64,50,62,236],[60,64,50,22,238],[60,88,50,22,237],[120,90,26,24,201],[146,90,26,24,202],[172,90,26,24,203],[120,64,58,22,206],[178,64,14,22,242],[194,64,30,22,243],[224,64,14,22,240],[240,64,24,22,204],[266,64,24,22,205],[280,90,20,24,241],[312,64,34,24,219],[348,64,34,24,220],[444,64,84,50,221],[532,64,84,50,222],[620,64,84,50,223],[708,64,84,50,224],[802,64,70,24,208],[802,90,70,24,209]];
for(let i=0;i<4;i++)home.push([312+i*30,92,28,24,215+i]);
const ins=[[8,64,70,24,240],[82,64,70,24,241],[156,64,70,24,242],[240,64,70,24,246],[322,64,70,24,252],[404,64,60,24,203],[468,64,50,24,204],[522,64,76,24,205],[602,64,76,24,201],[690,64,70,24,202],[770,64,64,24,208],[836,64,64,24,209],[902,64,56,24,211],[960,64,60,24,212],[770,90,64,24,210],[836,90,64,24,213],[1030,64,64,24,220],[1096,64,84,24,221],[1182,64,84,24,222],[1030,90,64,24,223],[1096,90,84,24,224]];
for(let i=0;i<6;i++)ins.push([902+i*20,90,18,24,214+i]);
const lay=[[8,64,80,24,243],[92,64,80,24,244],[186,64,62,62,201],[260,64,62,62,206],[334,64,86,24,202],[334,90,86,24,203],[424,64,86,24,204],[424,90,86,24,205],[514,64,62,62,207],[964,64,70,24,210],[1036,64,70,24,211],[1110,64,90,24,215],[964,90,56,24,212],[1022,90,56,24,213],[1080,90,56,24,214]];
for(let c=0;c<8;c++)lay.push([590+c*26,64,24,20,216+c]);
[224,236,237,238,239,240].forEach((a,i)=>lay.push([590+(8+i)*26,64,24,20,a]));
const refs=[[8,64,122,24,245],[8,90,122,24,208],[142,64,100,24,251],[254,64,90,24,201]];
const rev=[[8,64,100,24,249],[8,90,100,24,208],[120,64,70,24,202],[202,64,100,24,203],[306,64,60,24,204],[370,64,60,24,201]];
const vw=[[8,64,150,24,201],[8,90,150,24,202]];
const TABS=[home,ins,lay,refs,rev,vw];
const QAT=[[10,6,22,20,227],[34,6,22,20,228],[60,6,40,20,247],[102,6,40,20,248],[144,6,40,20,253]];
const TABX=[[56,110],[112,162],[164,222],[224,302],[304,364],[366,420]];
const inr=(x,y,r)=>x>=r[0]&&x<r[0]+r[2]&&y>=r[1]&&y<r[1]+r[3];
const cell=(x0,i)=>[x0+(i%8)*22+11,115+Math.floor(i/8)*22+11];
const OPEN={242:{old:[120,87,110,44],dx:-8},240:{old:[194,87,50,242],dx:48},206:{},241:{col:1},245:{},207:{old:[514,127,70,88],dx:194}};
module.exports=(p)=>{let tab=0,menu=null;const m=p.mouse,click=m.click.bind(m),move=m.move.bind(m);
 const at=(a)=>{const c=ids[a];if(BIU[a.split(':')[1]])return BIU[a.split(':')[1]];if(!c)throw new Error('no control '+a);return c;};
 // returns a list of points: all but the last are clicks that come first
 const map=(x,y,isClick)=>{
  if(menu&&menu.old&&inr(x,y,menu.old)){const q=menu.col?cell(270,Math.floor((y-115)/22)):[x+menu.dx,y];if(isClick)menu=null;return [q];}
  if(y>=150){if(isClick)menu=null;return [[x,y]];}
  if(isClick)menu=null;
  if(y<32){for(const r of QAT)if(inr(x,y,r))return [at('c:'+r[4])];return [[x,y]];}
  if(y<60){for(let i=0;i<6;i++)if(x>=TABX[i][0]&&x<TABX[i][1]){if(isClick)tab=i;return [at(i+':'+(229+i))];}return [[x,y]];}
  if(tab===0){
   if(y>=90&&y<114&&x>=202&&x<278){const c=[0,4,3][Math.floor((x-202)/26)];return [at('0:241'),cell(270,c)];}
   if(x>=880){const c=Math.floor((x-880)/26),r=Math.floor((y-64)/22);
    if(r===0){if(c<=4)return [at('0:'+[210,211,212,213,214][c])];if(c<=12)return [at('0:245'),cell(306,c-5)];return [at('0:'+(c===13?249:251))];}
    if(r===1)return [at('0:241'),cell(270,8+c)];
    if(c<9)return [at('0:241'),cell(270,23+c)];return [at('0:252')];}
  }
  for(const r of TABS[tab])if(inr(x,y,r)){
   if(isClick){if(tab===0&&r[4]===242)menu=OPEN[242];if(tab===0&&r[4]===240)menu=OPEN[240];if(tab===0&&r[4]===241)menu={old:[200,115,110,176],col:1};
    if(tab===2&&r[4]===206)menu={old:[260,127,190,66],dx:-254};if(tab===2&&r[4]===207)menu=OPEN[207];}
   return [at(tab+':'+r[4])];}
  return [[x,y]];};
 m.click=async(x,y,o)=>{const q=map(x,y,true);for(const c of q)await click(c[0],c[1],o);};
 m.move=async(x,y,o)=>{const q=map(x,y,false);const c=q[q.length>1?0:0];await move(c[0],c[1],o);};
 const press=p.keyboard.press.bind(p.keyboard);p.keyboard.press=async(k,o)=>{if(k==='Escape'||k==='Enter')menu=null;await press(k,o);};
 return p;};
