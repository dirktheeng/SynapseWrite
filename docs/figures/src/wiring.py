"""Draws the connection figures from the measured connections in connect.py's output."""
import json,sys,math,collections,html
sys.path.insert(0,'.');from nets_data import F
sys.argv_=sys.argv;O,CONN,PROV=sys.argv[1:4]
_a=sys.argv;sys.argv=['d',O,CONN,PROV]
INK,MUT,LINE,BG,CARD='#1c2733','#5b6b7b','#c9d3dd','#fbfcfd','#ffffff'
BLUE,AMB,TEAL,VIO,RED='#2563c9','#d97706','#0f9d8a','#7a5cd6','#c0392b'
TINT={BLUE:'#e8f0fc',AMB:'#fdf1e0',TEAL:'#e2f5f2',VIO:'#efebfa',MUT:'#eef1f4',RED:'#fbe9e7'}
C=json.load(open(CONN));G=json.load(open(PROV))['groups']
HUB=['compiled control','shared control registers','bank and port wiring']
fam={};order=[];names=[]
for h,_,r in F:
    fh=h;names.append(h)
    for n,_,_ in r:
        if n not in HUB:fam[n]=h;order.append(n)
for n in HUB:fam[n]='Hub';order.append(n)
E_=C['edges'];FF=collections.Counter();FP=collections.defaultdict(collections.Counter)
for a,b,c in E_:
    if fam[a]!=fam[b]:FF[tuple(sorted((fam[a],fam[b])))]+=c
for a,k,c in C['ports']:FP[fam[a]][k]+=c
def t(x,y,s,sz=13,c=INK,a='start',w=400):return f'<text x="{x}" y="{y}" font-size="{sz}" fill="{c}" text-anchor="{a}" font-weight="{w}">{html.escape(str(s))}</text>'
def rect(x,y,w,h,c,rx=9,sw=1.5,fill=None):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill or TINT[c]}" stroke="{c}" stroke-width="{sw}"/>'
def svg(w,h,b,title):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{html.escape(title)}" font-family="-apple-system,\'Segoe UI\',Helvetica,Arial,sans-serif"><title>{html.escape(title)}</title><rect width="{w}" height="{h}" rx="12" fill="{BG}" stroke="{LINE}"/><defs><marker id="m" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="{MUT}"/></marker></defs>{b}</svg>'
def band(x,y,w,h,c,title,items,tag=None):
    b=rect(x,y,w,h,c)+t(x+14,y+22,title,14,INK,'start',700)
    if tag:b+=t(x+w-14,y+22,tag,11.5,MUT,'end')
    n=len(items);cw=(w-20)/n
    for i,(a,s_) in enumerate(items):
        cx=x+10+i*cw;b+=rect(cx+2,y+32,cw-4,h-42,c,6,1,CARD)+t(cx+cw/2,y+52,a,12,INK,'middle',600)+t(cx+cw/2,y+68,s_,10.5,MUT,'middle')
    return b
def arr(d,sw=1.6,c=MUT):return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{sw}" marker-end="url(#m)"/>'
def pulse(d,c,begin,dur,total,r=6):
    b_,e=begin/total,(begin+dur)/total
    return f'<circle r="{r}" fill="{c}" opacity="0"><animateMotion path="{d}" dur="{total}s" repeatCount="indefinite" calcMode="linear" keyPoints="0;0;1;1" keyTimes="0;{b_:.4f};{e:.4f};1"/><animate attributeName="opacity" dur="{total}s" repeatCount="indefinite" keyTimes="0;{b_:.4f};{b_+.001:.4f};{e:.4f};{min(e+.001,1):.4f};1" values="0;0;1;1;0;0"/></circle>'
W=1000;b=t(30,36,'How everything is connected',22,INK,'start',700)+t(30,58,'Measured from the shipped weight file. Amber is glue, teal is the engine and memory, and the large panel is the network.',13.5,MUT)
y=74
b+=band(30,y,940,84,MUT,'Browser',[('Keyboard','key names'),('Mouse and touch','position, buttons'),('Timer','fires when set'),('Files','picker and drop'),('Clipboard','text'),('Canvas','shows pixels')])
y1=y+84
y=y1+26
b+=band(30,y,940,84,AMB,'Glue: event and byte encoders',[('Event vector','kind and 3 arguments'),('Key vector','name code units'),('Modifiers','raw bits'),('File bytes','into the bank'),('Paste text','into the bank'),('Field text','into the bank')],'host/glue.js')
for x in (120,280,440,600,760):b+=arr(f'M{x} {y1}V{y-2}')
y2=y+84
y=y2+26;net=y
PY=y+40;CW=296;GAP=12
pan=[]
rows=[names[:3],names[3:]]
LH=19
hub_y=None
yy=PY;col=[BLUE,TEAL,BLUE,VIO,AMB,TEAL]
inner=''
fam_pos={}
for ri,r in enumerate(rows):
    mx=max(sum(1 for n in order if fam[n]==h) for h in r);PH=48+mx*LH
    for ci,h in enumerate(r):
        x=48+ci*(CW+GAP);ns=[n for n in sorted(order,key=lambda q:-G[q]['neurons']) if fam[n]==h];c=col[names.index(h)]
        short=h;tot=sum(G[n]['neurons'] for n in ns)
        inner+=rect(x,yy,CW,PH,c)+t(x+12,yy+22,short,13.5,INK,'start',700)+t(x+CW-12,yy+22,f'{tot:,}',11.5,MUT,'end')
        for i,n in enumerate(ns):
            inner+=t(x+12,yy+42+i*LH,n,11.5)+t(x+CW-12,yy+42+i*LH,f"{G[n]['neurons']:,}",10.5,MUT,'end')
        fam_pos[h]=(x+CW/2,yy,yy+PH)
    yy+=PH+ (80 if ri==0 else 0)
    if ri==0:hub_y=yy-60
H_=yy+14-net
b+=rect(30,net,940,H_,BLUE,14,2,'#f5f8fd')+t(46,net+26,'One network. Colored panels are README categories; names are labels on its neurons',15,INK,'start',700)
b+=inner
regs=G['shared control registers']['neurons'];wire=G['bank and port wiring']['neurons']
b+=rect(46,hub_y,908,40,BLUE,8,2)+t(500,hub_y+25,f'Hub: compiled control ({G["compiled control"]["neurons"]:,}), shared registers ({regs:,}), port wiring ({wire:,})',13.5,INK,'middle',700)
def hubcount(h):return sum(c for a,x,c in E_ if (fam[a]==h and fam[x]=='Hub') or (fam[x]==h and fam[a]=='Hub'))
for h,(cx,top,bot) in fam_pos.items():
    n=hubcount(h);sw=max(1.5,min(7,math.log10(max(n,1))*1.2))
    if bot<=hub_y:d=f'M{cx} {bot}V{hub_y}';lab=bot+12
    else:d=f'M{cx} {hub_y+40}V{top}';lab=hub_y+52
    b+=f'<path d="{d}" stroke="{BLUE}" stroke-width="{sw:.1f}" opacity=".7"/>'+t(cx+8,lab+2,f'{n:,}',10.5,MUT)
for x in (120,280,440):b+=arr(f'M{x} {y2}V{net-2}')
y3=net+H_
y=y3+26
pk=[('Memory read','memory read'),('Memory write','memory write'),('Rectangle','screen rectangle'),('Patch','screen patch'),('Pixel read','screen pixel read'),('Copy','screen and memory copy'),('Call','glyph call'),('Style read','style read')]
pc=collections.Counter()
for a,k,c in C['ports']:pc[k]+=c
b+=band(30,y,940,84,TEAL,'Engine: passive ports, driven only by network neurons',[(a,f"{pc[k]} port{'s' if pc[k]!=1 else ''}") for a,k in pk],'host/engine.c')
yp=y
for x in (120,500,880):b+=arr(f'M{x} {y3}V{y-2}')
y4=y+84;y=y4+26
b+=band(30,y,460,84,TEAL,'Memory bank',[('Document','text, styles, undo'),('Work space','files, clip, glyphs')])+band(510,y,460,84,VIO,'Screen tensor',[('Color channels','what you see'),('Alpha channel','object ids')])
b+=arr(f'M260 {y4}V{y-2}')+arr(f'M740 {y4}V{y-2}')
y5=y+84;y=y5+26
b+=band(30,y,940,84,AMB,'Glue: runs ticks and carries out named commands',[('Tick loop','until halt'),('Display','putImageData'),('Set timer','network asks'),('Save file','bytes and name'),('Clipboard','text out, ask in'),('Pickers, focus','open, keyboard')],'host/glue.js')
b+=arr(f'M740 {y5}V{y-2}')
# return rail to browser
ye=y+84
b+=f'<path d="M970 {y+42}H988V{74+42}H972" fill="none" stroke="{MUT}" stroke-width="1.6" marker-end="url(#m)"/>'
b+=t(30,ye+24,'Line numbers: measured connections between that family and the hub. Families also connect to each other directly: see the table below.',12,MUT)
total=14
b+=pulse(f'M280 {y1}V{hub_y+20}',AMB,0,3,total)+pulse(f'M280 {hub_y+20}H500V{yp}',BLUE,3,3,total)+pulse(f'M740 {y4-40}V{y5+26+42}',VIO,6.2,3,total)+pulse(f'M970 {y+42}H988V{74+42}H972',AMB,9.3,3,total)
open(O+'/network_wiring.svg','w').write(svg(1006,ye+40,b,'Connection diagram: browser, glue encoders, network families with hub, engine ports, memory and screen, glue commands'))
# ---- full matrix ----
idx={n:i for i,n in enumerate(order)};n=len(order);M_=[[0]*n for _ in range(n)]
for a,x,c in E_:M_[idx[a]][idx[x]]=c
cs=11;X0=222;Y0=240;mx=max(max(r) for r in M_)
ramp=['#d6e4f8','#a8c6f0','#7aa7e6','#4d87da','#2563c9','#123f8f']
def col_(c):return ramp[min(5,int(math.log10(c)))] if c else None
b=t(24,34,'Every measured connection between sub-networks',20,INK,'start',700)+t(24,56,'Row sends to column. Darker means more connections, on a power of ten scale. The diagonal is wiring inside a sub-network.',13,MUT)
for i,nm in enumerate(order):
    b+=t(X0-6,Y0+i*cs+9,nm,9.5,INK,'end')+f'<text transform="translate({X0+i*cs+8},{Y0-6}) rotate(-55)" font-size="9.5" fill="{INK}">{html.escape(nm)}</text>'
    for j in range(n):
        v=M_[i][j]
        b+=f'<rect x="{X0+j*cs}" y="{Y0+i*cs}" width="{cs-1}" height="{cs-1}" fill="{col_(v) or "#f1f3f6"}">'+(f'<title>{html.escape(nm)} to {html.escape(order[j])}: {v:,}</title>' if v else '')+'</rect>'
last=None
for i,nm in enumerate(order):
    if fam[nm]!=last:
        if i:b+=f'<path d="M{X0-3} {Y0+i*cs-.5}H{X0+n*cs}M{X0+i*cs-.5} {Y0-3}V{Y0+n*cs}" stroke="{INK}" stroke-width="1"/>'
        last=fam[nm]
ly=Y0+n*cs+20
for i,c in enumerate(ramp):
    b+=f'<rect x="{X0+i*62}" y="{ly}" width="60" height="12" fill="{c}"/>'+t(X0+i*62,ly+26,['1+','10+','100+','1,000+','10,000+','100,000+'][i],10.5,MUT)
open(O+'/network_matrix.svg','w').write(svg(X0+n*cs+60,ly+44,b,'Matrix of connections between all sub-networks'))
json.dump({'FF':[[a,b_,c] for (a,b_),c in FF.most_common()],'FP':{k:dict(v) for k,v in FP.items()},'total':sum(c for *_,c in E_),'pushed':0},open(CONN+'.fam.json','w'))
for (a,b_),c in FF.most_common(12):print(c,a,'|',b_)
print(dict(pc))
