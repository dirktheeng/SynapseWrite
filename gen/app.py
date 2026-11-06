"""Writes the application network. Python here only computes weights at build time."""
import json,struct,gzip,sys,time
from nn import *
import rom,docx_tpl,glyphnet
# Sections of generator files run through exec; this names each one after its file so provenance can trace every neuron.
_open,_exec=open,exec; _srcs={}
def open(p,*a,**k):
    f=_open(p,*a,**k)
    if str(p).endswith('.py') and not a: _srcs[p]=f.read(); f.seek(0)
    return f
def exec(src,g=None,l=None):
    fr=sys._getframe(1)
    if g is None: g,l=fr.f_globals,fr.f_locals
    elif l is None: l=g
    _exec(compile(src,next((p for p,t in _srcs.items() if src in t),'app.py'),'exec'),g,l)
net=Net(); fsm=FSM(net); on=fsm.on; ONE=net.ONE; G_=net.gate
# ---- memory map (one passive tensor store) ----
# Bank map. Low cells: PT 0, VL 20000, Q 21000, RPL 21200, HD 21400, HIT 22000, TGW 23300, SECB 23400, NUMT 25000, STY0 26000, TBL 30000, MKT 32000,
# STY 40000, deflate hash 50000, mail merge 60000 and 100000, FNB 500000, XR 900000, ZT 1000000, HFB, FORD, FORD2, RIDB, PDFN up to 1020000, CB 1400000, CB2 1600000, slots 2000000.
# STYT 1100000 is the interned style table; PUS 999000 and PFT 999100 hold PDF face use and offsets. Glyph tag table TAGB 61000000, glyph store GSTORE 61500000, PDF font bytes FROMB 63000000.
# The bank is paged by the engine: a page takes wasm memory only when first written, so far apart regions cost nothing until used.
# High cells: undo 14500000, OUTB 20000000, IMG0 24000000, SAVEB 32000000 and everything from OUTP up only matters while reading, so a large save may run over it.
PT=0; VL=20000; Q=21000; RPL=21200; HD=21400; UB=14500000; UEND_=19999000; CB=1400000; SLOT0=2000000; STRIDE=4096; SAVEB=32000000; OUTP=40000000; PNGB=46000000; AUXB=50000000; RELB=51000000; CMB=51200000; FILE=53000000; IMG0=24000000; OUTB=20000000; TBL=30000; SLOTMAX=14400000; TAGB=61000000; GSTORE=61500000; GSTORE_END=63000000; FROMB=63000000; BANK=67000000
# Regions fail the build if they overlap: see region() in nn.py. Bounds are exclusive at the end.
for r_ in (('undo',14500000,20000000),('STYT interned styles',1100000,1100000+4096),('TAGB glyph tags',61000000,61500000),('GSTORE glyph store',61500000,63000000),('FROMB PDF fonts',63000000,64000000),
 ('a4 PDF numbering table',23800,25000),('a6 PDBM bookmarks',1200000,1264016),('a6 SGB suggestions',1302000,1310000),('a6 DICTB user words',1310000,1320000),('a6 AUTHB authors',1320000,1330000),('a6 EQT math records',1330000,1375000),
 ('a7 free slots and zero cells',1384000,1389100),('PTRB pointer',1390000,1391000),('a11 reserved',1391000,1393200),('CB clipboard',1400000,1600000),('CB2',1600000,2000000),('slots',2000000,14400000),
 ('MGB mail merge',100000,500000),('FNB',500000,900000),('XR',900000,999000),('PUS and PFT',999000,1000000),('ZT and PDFN',1000000,1020000)): region(*r_)
for r_ in (('META',3673,3681),('RBOT',3681,3683),('FNHT',3683,3684),('IMN',3684,3687),('a6 revision',3687,3690),('FNS',3690,3693),('paragraph properties',3693,3699),('CMTL',3699,3700),('comment text',3700,4084),('a4 tabs and keeps',4084,4095)): region(*r_,space='slot')
PDATE,PAUTH,PMK=3687,3688,3689; LEN,DIRTY,ALIGN,LIST,NLINES,WORDS,ENDY,PBRK=2048,2049,2050,2051,2052,2053,2054,2055; SAVE=2056; LINES=2064; IMF=3670; CMTL=3699; CMT=3700; FNS=3690; FNL=3692
# Slot cells from 3670: IMF 3670-3672, META 3673-3680, RBOT 3681-3682, FNHT 3683, IMN 3684-3686, revision day, author and mark 3687-3689, FNS 3690-3692, paragraph properties 3693-3698, CMTL 3699, comment text 3700-4095.
META=3673; CWO,CXO,CSH,SECN,TOCF,TSRC,TPG,SSI=[META+i_ for i_ in range(8)]; RBOT=3681; FNHT=3683; ZT=1000000; HFB=1010000; FORD=1012000; FORD2=1014000; RIDB=1016000; FNB=500000; FNMAX=1500; HIT=22000; TGW=23300; SECB=23400
# paragraph properties: left indent px, first line offset px, line spacing index, space before px, space after px, style index. LIST holds kind+4*level.
# The first line offset is stored as 0 for none or PFO+offset, as gates clamp negative values; pf_val gives the signed value at use.
PIND,PFIRST,PLSP,PSPB,PSPA,PSTY=3693,3694,3695,3696,3697,3698; DEFSPA=11; PFO=4096
def pf_val(v): return v-net.step(v)*PFO
STY=40000; STY0=26000; STYN=48; NUMT=25000; MKT=32000; SCR=SLOTMAX; DEFREC=198; STYMAX=196   # style table, its ROM copy, numbering kinds, list marker ROM, scratch record
# ---- screen geometry ----
DOCY,DOCB=174,776; VH=DOCB-DOCY; PX=223; TX=319; TW=624; PH=1056; PST=1072; YB=4096
from app_pal import F as PAL_F,B as PAL_B,HL_NAMES
# ---- ports ----
STYT_=1100000; IDXM_=(1<<18)-1
class RPort:
    def __init__(s,cells,varlen=False):
        s.en=Bus(net);s.addr=Bus(net);s.cells=cells;s.out=net.input(cells) if cells>1 else [net.input()]
        s.len=Bus(net) if varlen else None; net.ports.append(s)
    def drive(s,c,v):
        a,n=v if s.len else (v,None)
        s.en.lin(c); s.addr.add(c,a)
        if s.len: s.len.add(c,n)
    def rec(s,nm): return [2,s.en.w,s.addr.w,s.out[0],s.cells,s.len.w if s.len else None]
class StylePort(RPort):
    "Reads a style cell and, in the same tick, the record its index selects: out[0] the cell, out[1] the record."
    def __init__(s): RPort.__init__(s,2)
    def rec(s,nm): return [10,s.en.w,s.addr.w,s.out[0],STYT_,IDXM_,1,1]
class WPort:
    def __init__(s,cells,data=None,varlen=False):
        s.en=Bus(net);s.addr=Bus(net);s.cells=cells;s.len=Bus(net) if varlen else None;s.ext=data
        if data is None:
            s.d=[Bus(net) for _ in range(cells)]
            # consecutive data neurons are required by the port
        net.ports.append(s)
    def drive(s,c,v):
        s.en.lin(c); s.addr.add(c,v[0])
        if s.len: s.len.add(c,v[1])
        elif s.ext is None:
            for b,x in zip(s.d,v[1:]): b.add(c,x)
    def rec(s,nm): return [1,s.en.w,s.addr.w,(s.ext if s.ext is not None else s.d[0].w),s.cells,s.len.w if s.len else None]
class RectPort:
    def __init__(s):
        s.b=[Bus(net) for _ in range(9)]; net.ports.append(s)
    def drive(s,c,v):
        x,y,w,h,col,a=v; s.b[0].lin(c)
        for b,e in zip(s.b[1:5],(x,as_x(y)+YB,w,h)): b.add(c,e)
        if isinstance(col,tuple):
            for b,e in zip(s.b[5:8],col): b.add(c,e)
        s.b[8].add(c,a)
    def lin(s,tok,x,y,w,h,col,a):
        s.b[0].lin(tok)
        for b,e in zip(s.b[1:],(x,y+YB,w,h,col[0],col[1],col[2],a)):
            if e: b.lin(tok*e)
    def rec(s,nm): return [3]+[b.w for b in s.b]+[clip0,clip1]
class CopyPort:
    "Copies a block of pixel words between bank and screen, leaving the id plane alone: {6,en,x,y,addr,w,h,dir,y0,y1}. dir 1 writes the screen. A cell is R+G*256+B*65536, the screen's own word."
    def __init__(s,y0,y1):
        s.b=[Bus(net) for _ in range(7)];s.c=(y0,y1); net.ports.append(s)
    def drive(s,c,v):
        s.b[0].lin(c); s.b[1].lin(net.gate(as_x(v[0])+64,c)-c*64)   # x may be just off the left edge
        for b,e in zip(s.b[2:],(as_x(v[1])+YB,v[2],v[3],v[4],v[5])): b.add(c,e)
    def rec(s,nm): return [6]+[b.w for b in s.b]+list(s.c)
class PixPort:
    def __init__(s):
        s.en=Bus(net);s.x=Bus(net);s.y=Bus(net);s.out=net.input(4); net.ports.append(s)
    def drive(s,c,v): s.en.lin(c); s.x.add(c,v[0]); s.y.add(c,v[1])
    def rec(s,nm): return [5,s.en.w,s.x.w,s.y.w,s.out[0]]
class PatchPort:
    def __init__(s,en,x,y,data,w,h): s.a=(en,x,y,data,w,h); net.ports.append(s)
    kind=4
    def rec(s,nm): e,x,y,d,w,h=s.a; return [s.kind,e,x,y,d,w,h,clip0,clip1]
class SpritePort(PatchPort):
    "A patch write with no clip: it always covers the whole screen."
    def rec(s,nm): e,x,y,d,w,h=s.a; return [4,e,x,y,d,w,h,ZERO_R,ZERO_R]
class CallPort:
    "Runs the other clock domain until its done neuron fires. This domain is stopped meanwhile."
    def __init__(s,en,done,args,rets=()): s.en=en;s.done=done;s.args=args;s.rets=rets;net.ports.append(s)
    def rec(s,nm): return [8,s.en,s.done,s.args,s.rets]
clip0=net.reg(); clip1=net.reg(); ZERO_R=net.reg()
rb=RPort(1100,True); wb=WPort(1100,rb.out[0],True)   # block copy through 1100 neurons
rc=RPort(2); rf=RPort(3); r1=RPort(1); r2=RPort(1); rl=RPort(8); rlog=RPort(6); rp6=RPort(6)
w1=WPort(1);w2=WPort(1);w3=WPort(1);w4=WPort(1);wlog=WPort(6);wvl=WPort(6);wln=WPort(6)
rmeta=RPort(8);MT=rmeta.out;wht=WPort(6);imr=CopyPort(clip0,clip1);rim=RPort(3);rU=RPort(1);rV=RPort(1);rA=RectPort();rB=RectPort();rC=RectPort();rD=RectPort();pix=PixPort()
R1=r1.out[0];R2=r2.out[0]
rs=StylePort(); RSC=rs.out[0]; RSR=rs.out[1]
ev_kind,ev_a,ev_b,ev_c=net.input(4); ev_t=net.input(); evt=net.reg(); ev_m=net.input()
kv=net.input(6); kvl=net.input()
KBV=1391000; KBL=1392000; KBQ=1393000; NAMEB=1393100; KBMAX=1000; KBSEN=8; NAME_DOCX='Document1.docx'; NAME_PDF='Document1.pdf'   # field text from the glue, last field text, field sentinel, file names
halt=Bus(net); timer=Bus(net); clipout=Bus(net)
# ---- glyph network ----
net.group('glyph network')
g_en=Bus(net);g_ch=Bus(net);g_st=Bus(net);g_x=Bus(net);g_y=Bus(net);g_draw=Bus(net)
fg=[Bus(net) for _ in PAL_F]; bg=[Bus(net) for _ in PAL_B]
GE=g_en.w
# A character's style cell holds an index into the interned style table, with the per character flags above it:
#   cell: table index 0-17, math 18, ins 19, del 20, field kind 21-22, no proof 23.
#   record: size 0-3 and 19-21, bold 4, ital 5, und 6, font 7 and 22-23, color low 8-10, strike 11, sup 12, sub 13, highlight 14-16, color high 17-18.
# Record 0 is the default: Carlito 11 pt. A record is never changed once written, so undo, clipboard and files only move indices.
ST_STRIKE,ST_VERT,ST_SUP,ST_SUB,ST_HL,ST_INS,ST_DEL,ST_F0,ST_NOP,ST_MATH=1<<11,1<<12,1<<12,1<<13,1<<14,1<<19,1<<20,1<<21,1<<23,1<<18
STYT=1100000; STYCAP=4096; IDXM=(1<<18)-1
def style_decode(val,en):
    b=net.bits(val,24,en)
    return dict(size=b[0]+b[1]*2+b[2]*4+b[3]*8+b[19]*(1<<19)+b[20]*(1<<20)+b[21]*(1<<21),si=b[0]+b[1]*2+b[2]*4+b[3]*8+b[19]*16+b[20]*32+b[21]*64,sb=b[:4]+b[19:22],bold=b[4],ital=b[5],und=b[6],font=b[7]+b[22]*2+b[23]*4,fontraw=b[7]*128+b[22]*(1<<22)+b[23]*(1<<23),fb=[b[7],b[22],b[23]],color=b[8]+b[9]*2+b[10]*4+b[17]*8+b[18]*16,
      colraw=b[8]*256+b[9]*512+b[10]*1024+b[17]*131072+b[18]*262144,strike=b[11],vert=b[12]+b[13]*2,sup=b[12],sub=b[13],hl=b[14]+b[15]*2+b[16]*4)
def flag_decode(val,en):
    "The flags of a cell. Most cells have none, so one neuron answers for them."
    v=as_x(val); nz=net.step(v-(1<<18)+0.5+as_x(en)*M-M); rem=net.gate(v,nz); o={}
    for k_,nm_ in ((23,'nop'),(22,'f1'),(21,'f0'),(20,'dele'),(19,'ins'),(18,'math')):
        o[nm_]=net.step(rem-(1<<k_)+0.5); rem=rem-o[nm_]*(1<<k_)
    o['flags']=o['ins']*ST_INS+o['dele']*ST_DEL+o['f0']*ST_F0+o['f1']*ST_F0*2+o['nop']*ST_NOP+o['math']*ST_MATH
    return o
MATHFAM=1; MATHRAW=rom.font_raw(MATHFAM)   # an equation character carries the math flag, which no ordinary text can get. Choosing another font for it makes it ordinary text.
def is_math(D): return net.and_(D['fb'][0],ONE-D['fb'][1],ONE-D['fb'][2],D['math'])
g_fl=Bus(net)
SD=style_decode(g_st.w,GE); SD.update(flag_decode(g_fl.w,GE))
# Glyph addressing is a decision tree: each node is enabled by its parent and reads its
# selector lazily, so a lookup visits a path through the tree and not all of the table.
def tnode(parent,sel,neg=False):
    return net.step(parent*M-M+((ONE-sel) if neg else sel)-0.5)
def tsplit(parent,sel): return tnode(parent,sel,True),tnode(parent,sel)
def _tree(parent,sels,n):
    "Leaves 0 to n-1 of a binary tree over the bits. Values past the table go nowhere."
    if not sels: return [parent]
    half=1<<(len(sels)-1); l0,l1=tsplit(parent,sels[-1])
    return _tree(l0,sels[:-1],min(n,half))+(_tree(l1,sels[:-1],n-half) if n>half else [])
NS=rom.NSZ
_leaf=_tree(GE,SD['sb'],NS)
raw_hot=_leaf[:NS]
# character index in binary; values past the table (code 255) clamp to an empty entry
_chv=net.relu(g_ch.w-32+1+GE*M-M)
_chok=net.step(_chv)
_chbits=net.bits(_chv-1-net.relu(_chv-225),8,_chok)
def chartree(root,bits,k,idxs,leaf):
    "Walks the binary digits, building nodes only where the table has an entry."
    S_=set(idxs)
    def walk(node,lo,k_):
        if k_<0: leaf(node,lo); return
        mid=lo+(1<<k_)
        if any(i_ in S_ for i_ in range(lo,mid)): walk(tnode(node,bits[k_],True),lo,k_-1)
        if any(i_ in S_ for i_ in range(mid,mid+(1<<k_))): walk(tnode(node,bits[k_]),mid,k_-1)
    walk(root,0,k)
adv=net.wire();asc=net.wire();asc_e=net.wire();lh=net.wire();rise=net.wire();strk=net.wire()
# superscript and subscript draw a smaller compiled size; the line keeps the nominal metrics
def script_size(i):
    return rom.sz_near(round(rom.SZ[i]*0.72))
vflag=net.step(SD['sup']+SD['sub'])
size_hot=[X() for _ in range(NS)]
for i_ in range(NS):
    n_,s_=tsplit(raw_hot[i_],vflag); size_hot[i_]=size_hot[i_]+n_; size_hot[script_size(i_)]=size_hot[script_size(i_)]+s_
for si,h in enumerate(raw_hot):
    px=round(rom.SZ[si]*96/72); net.connect(strk,h*round(px*0.28))
    net.connect(rise,net.and_(h,SD['sup'])*round(px*0.36)); net.connect(rise,net.and_(h,SD['sub'])*(-round(px*0.16)))
GLW=rom.GLW; FACES=rom.FACES; SQUIG=129     # code with no character: one period of the spelling squiggle
# metrics: one tree per face gives the advance in ems, then the drawn size scales it. No ink is touched.
net.group('glyph metrics')
t0=time.time()
FH={}
FONT_HOT=_tree(GE,SD['fb'],len(rom.FAM))
FACE_OF={}
for fi,fn_ in enumerate(FONT_HOT):
    # a family without a face draws its nearest one
    b0,b1=tsplit(fn_,SD['bold'])
    for bo,bn_ in enumerate((b0,b1)):
        i0,i1=tsplit(bn_,SD['ital'])
        for it,lf_ in enumerate((i0,i1)):
            f_=rom.face_of(fi,bo,it); FACE_OF[fi,bo,it]=f_; FH[f_]=FH.get(f_,X())+lf_
# line metrics: per size and family. The glyph unit's baseline comes from the drawn size.
for si,h in enumerate(raw_hot):
    for fi,fn_ in enumerate(FONT_HOT):
        a,l=rom.metrics_sz(si,fi); t_=tnode(h,fn_); net.connect(asc,t_*a); net.connect(lh,t_*l)
for si,h in enumerate(size_hot):
    for fi,fn_ in enumerate(FONT_HOT):
        a,l=rom.metrics_sz(si,fi); net.connect(asc_e,tnode(h,fn_)*a)
aem=net.wire()
for f_ in FACES:
    tb_={c_-32:rom.adv_em(*f_,c_) for c_ in rom.CODES}
    if f_==(0,0,0): tb_[SQUIG-32]=4/12
    def _al(G,ix,tb_=tb_): net.connect(aem,G*tb_[ix])
    chartree(tnode(FH[f_],_chok),_chbits,7,tb_,_al)
for si,h in enumerate(size_hot): net.connect(adv,net.gate(aem*round(rom.SZ[si]*96/72),h))
# kerning: a tree over the previous character, then over the current one. A pair that exists fires kany.
kp_en=Bus(net); kp_in=Bus(net)
kp_ok=net.and_(kp_en.w,net.lt(kp_in.w,127,kp_en.w))
_kb=net.bits(kp_in.w-32,7,kp_ok)
KP=rom.kern_pairs()
kf={f_:net.wire() for f_ in FACES}; kany=net.wire()
_left={}
for (l_,r_),vals in KP.items(): _left.setdefault(l_-32,{})[r_-32]=vals
def _kl(G,lx_):
    d_=_left[lx_]
    def _kr(N,rx_):
        net.connect(kany,N)
        for f_,v_ in d_[rx_].items(): net.connect(kf[f_],N*v_)
    chartree(tnode(G,_chok),_chbits,7,d_,_kr)
chartree(kp_ok,_kb,6,_left,_kl)
kanyb=net.step(kany)
k1=X()
for f_ in FACES: k1=k1+net.gate(kf[f_]+1,tnode(FH[f_],kanyb))
kern=net.wire()
for si,h in enumerate(size_hot):
    px=round(rom.SZ[si]*96/72); h_k=tnode(h,kanyb)
    net.connect(kern,net.gate(k1*px,h_k)-h_k*px)
print('metric trees',time.time()-t0,'s',len(KP),'kern pairs',file=sys.stderr)
# the drawing unit: its own clock domain, entered through a call port, so the paint state stalls while it runs
net.group('glyph unit')
exec(open('ptr_shapes.py').read())
_sq=_layer([".K..","K.K.","...K"],0,rom.metrics(9)[0],'K')
_pseudo={0:{SQUIG:(_sq,True)},len(FACES):PTR_GLYPHS}
glyph_unit=glyphnet.GlyphUnit(net,FACES,rom.CODES,_pseudo,GLW,TAGB,GSTORE,GSTORE_END,(clip0,clip1),PAL_F,PAL_B,ONE,PatchPort,SpritePort)
_A=glyph_unit.A
_face=net.wire(); _sz=net.wire(); _ppem=net.wire(); _pt=net.wire(); _fg=net.wire(); _bg=net.wire(); _base=net.wire(); g_nc=Bus(net); g_fx=Bus(net)
for f_ in FACES: net.connect(_face,FH[f_]*FACES.index(f_))
net.connect(_face,g_fx.w)
for si,h in enumerate(size_hot):
    px=round(rom.SZ[si]*96/72); net.connect(_sz,h*si); net.connect(_ppem,h*px); net.connect(_pt,h*rom.SZ[si])
for j,b_ in enumerate(fg): net.connect(_fg,b_.w*(j+1))
for j,b_ in enumerate(bg): net.connect(_bg,b_.w*(j+1))
net.connect(_base,g_y.w+asc_e)
GCALL=CallPort(net.step(g_draw.w),glyph_unit.fin,[(net.step(g_draw.w),_A['go']),(g_ch.w,_A['ch']),(_face,_A['face']),(_sz,_A['sz']),(_ppem,_A['ppem']),(_pt,_A['pt']),(g_x.w,_A['x']),(_base,_A['y']),(_fg,_A['fg']),(_bg,_A['bg']),(g_nc.w,_A['nc'])])
# the style table's interner: its own domain too, called with a record value, returns the record's index
net.domain(1); net.group('style interner')
I_go=net.input(); I_val=net.input(); I_fb=net.input()
IF=FSM(net)
iv=net.reg(); ifb=net.reg(); iout=net.reg(); ifull=net.reg(); icnt=net.reg(1.0); im_v=net.reg(); im_o=net.reg(); ii=net.reg()
IF.set(iv,I_go,I_val); IF.set(ifb,I_go,I_fb); IF.set(ifull,I_go,0)
irR=RPort(1); iW=WPort(1); irR.dom=1; iW.dom=1; IRD=irR.out[0]
net.rec(IF.S('I0'),I_go)
e=IF.S('I0'); imemo=net.eq(iv,im_v,e)
IF.on('I0',(imemo,'IE',{iout:im_o}),(None,'IS',{ii:0}))   # record 0 is searched too: the default style must not get a second index
e=IF.S('IS')
IF.on('IS',(net.ge(ii,icnt,e),'IA',None),(None,'IC',{irR:as_x(STYT)+ii}))
e=IF.S('IC')
IF.on('IC',(net.eq(IRD,iv,e),'IM',{iout:ii}),(None,'IS',{ii:ii+1}))
e=IF.S('IA')
IF.on('IA',(net.ge(icnt,STYCAP,e),'IE',{iout:ifb,ifull:1}),(None,'IM',{iout:icnt,icnt:icnt+1,iW:(as_x(STYT)+icnt,iv)}))
IF.on('IM',(None,'IE',{im_v:iv,im_o:iout}))
IF.on('IE',(None,None,None))
IF.finish()
net.domain(0); net.group('glyph patch')
ic_en=Bus(net); ic_val=Bus(net); ic_fb=Bus(net); ROUT=net.input(); RFULL=net.input()
_ic_go=net.step(ic_en.w)
CallPort(_ic_go,IF.S('IE'),[(_ic_go,I_go),(ic_val.w,I_val),(ic_fb.w,I_fb)],[(iout,ROUT),(ifull,RFULL)])
class Interned:
    "A style held both as a record and as its table index. Assigning the record interns it; the index is ready two ticks later."
    def __init__(s,rec,idx): s.rec=rec; s.idx=idx
    def drive(s,c,val):
        fsm.set(s.rec,c,val); ic_en.lin(c); ic_val.add(c,val); ic_fb.add(c,s.idx); d_=net.reg(); net.rec(d_,c); fsm.set(s.idx,d_,ROUT)
class GlyPort:
    def drive(s,c,v):
        ch,st,x,y,f,b=v; g_en.lin(c); g_ch.add(c,ch); g_st.add(c,rom.lit(st) if isinstance(st,int) else st); g_x.add(c,x); g_y.add(c,as_x(y)+YB); g_draw.lin(c)
        fg[f].lin(c) if isinstance(f,int) else None; bg[b].lin(c) if isinstance(b,int) else None
gly=GlyPort()
net.group('shared control registers')
# ---- control registers ----
R=net.reg
s_px=R(PX);s_pw=R(816);s_ph=R(PH);s_tx=R(TX);s_tw=R(TW);s_mt=R(96);s_th=R(864);s_ps=R(PST);hitn=R();pbg=R();bc0=R(255);bc1=R(255);bc2=R(255);fnh=R();bfnh=R();pfc=R();pff=R();pfh=R();pfy=R();pfx=R();pfw=R();dnum=R();lnfh=R();lfn=R();lfb=R();lfh=R();lfnb=R();lfhb=R();ptoc=R();ptsrc=R();ptpg=R();hfk=R();hfb=R(HFB);hftp=R();rdp=R();hfl=[R() for _ in range(4)];tdk=R();cursec=R();bsec=R();nsec=R(1);cxl=R(PX);cxr=R(PX+816)
cp=R();cb=R(SLOT0);co=R();clen=R();ap=R();ao=R();scroll=R();npar=R(1);nextb=R(SLOT0+STRIDE);ty=R();tab=R()
drag=R();usp=R(UB);urp=R(UB);grp=R(1);nolog=R();blink=R();autos=R();mode=R();qlen=R();rlen=R();field=R()
tsop=R();spb=R();scols=R();sci=R();scw=R();ssh=R();spc=R();t4k=R();arj=R();evk=R();eva=R();evb=R();evc=R();shiftk=R();trk=R();sp_on=R(1);a6qk0=R();a6qs=R();a6nc=R();a6pm2=R();a6pm=R();a6hf=R();a6fg=R();a6w=R();a6pg=R()
tyi=R(); ity=Interned(ty,tyi); TST=tyi+trk*ST_INS
hx_=R();hy_=R();fm=R();alv=R();jp=R();jo=R();hdir=R();hact=R();btn=R();hcol=R();vi=R();clipr=R()
clipl=R();wpaste=R();full=R(1);fastok=R();oldcp=R();wassel=R();bgp=R();bgm=R();bcnt=R();dfrom=R();bpi=R();byy=R();bptop=R();bpg=R(1);bws=R();bln=R();tcols=R();tci=R();rw=R(624);rx0=R();rleft=R(223);rright=R(1039);rowtop=R();rowmax=R();tiv=R();tin=R();tic=R();tip=R();tir=R();sx=R();ncol=R();xcol=R();bxc=R();hlen=R();hdi=R();di_=R();ti_=R();tk_=R();tbase=R();tl_=R();tpg=R();tdig=R();tivx=R();fnn=R();fnp=R();bfn=R();bfp=R();pfn=R();fni=R();pim=R();pih=R();pio=R();irow=R();iaddr=R();wpic=R();imgp=R();ci_=R();cl_=R();wopen=R();lc=R(1);vm=R();pagesT=R(1);wtot=R();ytot=R(112);oend=R();sidx=R()
pind=R();pfirst_=R();plsp=R();pspb=R();pspa=R();psty=R();plvl=R();lfi=R();mkn=R();t2si=R();nsty=R(6);fsi=R();fhl=R();td0=R();td1=R()
pi=R();pbs=R();yy=R();wl_=R();wb_=R();wdx=R();wdy=R();wdw=R();wdd=R();wbgf=R();ptop=R();pages=R();wsum=R();vln=R();listn=R();lj=R();nl=R();al=R();lsf=R();plen_=R();wdp=R()
# Tier 1 features live in t1_features.py; each section is exec'd at its hook point
T1S={x.split('\n',1)[0].strip():x.split('\n',1)[1] for x in open('t1_features.py').read().split('#@@')[1:]}
def T1(n): exec(T1S[n],globals())
T1('regs')
exec(open('rv_a4_regs.py').read())
a7_vw=R();a7_far=R();a7_jmp=R();a7_wb=R();A7BUD=15000   # characters of layout one event may do before the rest goes to the background
# dispatch tables for subroutine returns
class Ret:
    def __init__(s,name): s.r=R(); s.t=[]; s.name=name
    def id(s,st):
        if st not in s.t: s.t.append(st)
        return s.t.index(st)+1
    def gen(s):
        en=fsm.S(s.name); n=len(s.t)+1
        if n<6: h=net.decode(s.r,n,en)
        else:   # two digit one-hot: only the lines of the active digit are visited, and the lines exclude each other
            nb=len(bin(n-1))-2; lo_=nb//2; b_=net.bits(s.r,nb,en)
            dl=net.decode(sum((b_[i]*(1<<i) for i in range(lo_)),X()),1<<lo_,en); dh=net.decode(sum((b_[i]*(1<<(i-lo_)) for i in range(lo_,nb)),X()),1<<(nb-lo_),en)
            h=[net.step(dh[i>>lo_]+dl[i&((1<<lo_)-1)]-1.5) for i in range(n)]
        for i,st in enumerate(['HALT']+s.t): fsm.states[s.name][1].append((h[i],st))
jret=Ret('JR');wret_=Ret('T3_WR');oret=Ret('OR');dret=Ret('DR');wret=Ret('WR');t4cr=Ret('T4_CR')
S=fsm.S
exec(open('rv_a9_dl.py').read())
Kc=cp*2048+co;Ka=ap*2048+ao
Hi=net.max_(Kc,Ka);Lo=net.min_(Kc,Ka);has_sel=net.step(Hi-Lo)
lo_a=net.step(Kc-Ka)     # anchor is the low end
lo_p=G_(ap,lo_a)+G_(cp,ONE-lo_a);lo_o=G_(ao,lo_a)+G_(co,ONE-lo_a)
hi_p=G_(cp,lo_a)+G_(ap,ONE-lo_a);hi_o=G_(co,lo_a)+G_(ao,ONE-lo_a)
at_a=ONE-has_sel
# ---- event dispatch ----
exec(open('rv_a3_pre.py').read())
net.group('event dispatch')
a11busy=R()
exec(open('pointer.py').read())
kh=net.decode(evk,14,S('DISP'))
exec(open('pointer2.py').read())
exec(open('rv_a11_input.py').read())
_rv_m=net.bits(evm,5,S('DISP')); fsm.set(rv_eol,net.or_(kh[2],kh[3],kh[8],kh[9],kh[10]),0); fsm.set(rv_try,kh[2],0)
on('DISP',*PTR_DISP,(net.and_(kh[3],t1_mopb),'T1_MD',{hx_:eva,hy_:evb}),(net.and_(kh[3],_rv_m[4]),'RVA3_RC0',{hx_:eva,hy_:evb}),(net.and_(kh[2],t1_mopb),'T1_MK',None),(net.and_(kh[4],t1_tdrag),'RD0',{drag:0,t1_tdrag:0}),(kh[11],'T1_HV',{hx_:eva,hy_:evb}),(kh[1],'UI',{clip0:0,clip1:0}),(kh[2],'T2_KM',{shiftk:net.bits(evb,2,S('DISP'))[1]}),(kh[3],'MD',{hx_:eva,hy_:evb}),
   (kh[4],'T3_MU',{drag:0}),(kh[5],'MV',None),(kh[6],'WH',None),(kh[7],'TM',{blink:ONE-blink,autos:0}),(kh[8],'PASTE',{}),(kh[9],'A12_OV0',{}),(kh[10],'PG_0',{}),(None,'HALT',None))
on('IDL2',(None,'HALT',None))
on('MV',(t1_tdrag,'T1_TM0',None),(net.and_(S('MV'),net.step(tdk)),'T3_MV',None),(net.and_(S('MV'),drag),'MD2',{hx_:net.max_(net.min_(eva,s_px+s_pw-2),s_px+1),hy_:net.max_(net.min_(evb,DOCB-6),DOCY+6),shiftk:1}),(None,'HALT',None))
on('WH',(None,'RD0',{scroll:net.relu(scroll+evc-1000),autos:0,a7_jmp:0}))   # ev_c carries delta+1000
e=S('TM'); _a6stale=net.and_(a6hf,ONE-has_sel,ONE-drag,net.eq(mode,0,e),net.step(net.gt(wtot,a6w,e)+net.lt(wtot,a6w,e)+net.gt(pagesT,a6pg,e)+net.lt(pagesT,a6pg,e)))
_rv_tm=S('TM'); on('TM',(net.and_(_rv_tm,drag,net.or_(net.lt(mp_pty,DOCY+8,_rv_tm),net.ge(mp_pty,DOCB-8,_rv_tm))),'RVA3_AS0',None),(t1_cntp,'T1_C0',{blink:blink}),(bgp,'BG',{blink:blink}),(_a6stale,'T4_FU',{blink:blink,a6fg:1,nolog:1,a6w:wtot,a6pg:pagesT}),(None,'A11_C0',None))
on('BG',(None,'T3_RS0',{fnh:bfnh,cursec:bsec,fnn:bfn,fnp:bfp,xcol:bxc,pi:bpi,yy:byy,ptop:bptop,pages:bpg,wsum:bws,listn:bln,full:1,vm:0,bgm:1,bcnt:0,clip0:DOCY,clip1:800-DOCB}))
_rv_hf=S('HF'); _rv_bg=net.or_(bgp,t1_cntp); timer.lin(_rv_hf*530-net.and_(_rv_hf,_rv_bg)*529-net.and_(_rv_hf,drag,ONE-_rv_bg,net.or_(net.lt(mp_pty,DOCY+8,_rv_hf),net.ge(mp_pty,DOCB-8,_rv_hf)))*495)
# ---- character code tables: internal cells use Windows-1252 style codes ----
net.group('character maps')
um_en=Bus(net); um_in=Bus(net); UMV=um_in.w; UME=um_en.w
um_out=net.gate(UMV,net.lt(UMV,127,UME))+net.gate(UMV,net.and_(net.ge(UMV,160,UME),net.lt(UMV,256,UME)))
for u_,c_ in rom.UNI_MAP.items(): um_out=um_out+net.eq(UMV,u_,UME)*c_
def i2u(v,en):
    "Internal code to unicode point for text leaving the network."
    o=net.and_(en,net.ge(v,128,en),net.lt(v,160,en)); hi=net.decode(as_x(v)-128,32,o); ex_=X()
    for c_ in range(128,160):
        ch_=rom.cp1252(c_)
        if ch_: ex_=ex_+hi[c_-128]*(ord(ch_)-c_)
    return as_x(v)+ex_
# ---- key handling ----
net.group('key handling')
en=S('KEY'); k=net.decode(eva,256,en); kb=net.bits(evb,2,en); ctrl=kb[0]; shf=kb[1]; nc=ONE-ctrl
def K(c): return net.and_(k[ord(c) if isinstance(c,str) else c],ctrl)
def N(c): return net.and_(k[c],nc)
printable=X()
for c in list(range(32,127))+list(range(160,256)): printable=printable+k[c]
findon=net.step(mode)
A_KEEP=net.and_(en,shf)
t1_pzn=net.gt(evc,t1_kt+2000,en)
on('KEY',(net.and_(a4fp,N(27)),'RD0',{a4fp:0,a4fs:0,t1_uid:1}),
 (net.and_(net.eq(mode,7,en),N(13)),'T2_TS',{mode:0}),(net.and_(net.eq(mode,7,en),N(8)),'RD0',{td0:td1,td1:0}),
 (net.and_(net.eq(mode,6,en),N(27)),'RD0',{mode:0}),
 (net.and_(net.eq(mode,5,en),net.or_(N(27),N(13))),'FNE',{mode:0}),(net.and_(net.eq(mode,5,en),N(8)),'FNc',None),(net.and_(net.eq(mode,4,en),net.or_(N(27),N(13))),'RD0',{mode:0}),(net.and_(net.eq(mode,4,en),N(8)),'CMc',None),(net.and_(net.eq(mode,3,en),net.or_(N(27),N(13))),'T3_HE',{mode:0}),(net.and_(net.eq(mode,3,en),N(8)),'RD0',{hlen:net.relu(hlen-1)}),(net.and_(findon,N(27)),'RD0',{mode:0}),
 (net.and_(findon,N(9)),'RD0',{field:ONE-field}),
 (net.and_(findon,N(13)),'FIND',{}),
 (net.and_(findon,N(8)),'RD0',{qlen:G_(net.relu(qlen-1),ONE-field)+G_(qlen,field),rlen:G_(net.relu(rlen-1),field)+G_(rlen,ONE-field),**CSTART}),
 (net.and_(findon,net.and_(printable,nc)),'FTYPE',{}),
 *rv_key_rules(),
 (N(128),'MOVL',{}),(N(130),'MOVR',{}),(N(129),'MOVU',{}),(N(131),'MOVD',{}),(N(132),'MOVH',{}),(N(133),'MOVE',{}),
 (N(134),'RD0',{scroll:net.relu(scroll-500),autos:0}),(N(135),'RD0',{scroll:scroll+500,autos:0}),
 (K(132),'MVJ',{jp:0,jo:0,jret.r:jret.id('MVEND')}),(K(133),'MVJ',{jp:net.relu(npar-1),jo:2047,jret.r:jret.id('MVEND')}),(K('p'),'PDF',{}),(K('s'),'SAVE',{}),(K('o'),'HALT',{wopen:1}),(K('z'),'UNDO',{}),(K('y'),'REDO',{}),(K('a'),'SELALL',{}),(K('c'),'COPY',{}),(K('x'),'CUT',{}),
 (K('b'),'FMTS',{fm:1}),(K('i'),'FMTS',{fm:2}),(K('u'),'FMTS',{fm:3}),
 (K('e'),'SETAL',{alv:1}),(K('l'),'SETAL',{alv:0}),(K('r'),'SETAL',{alv:2}),(K('j'),'SETAL',{alv:3}),
 (K('f'),'RD0',{mode:1,field:0,**CSTART}),(K('h'),'RD0',{mode:2,field:0,**CSTART}),
 (N(141),'A6S_0',{}),(K(13),'PB0',{grp:grp+1}),(N(8),'BKSP',{grp:grp+net.step(net.step(t1_lastk-2)+net.step(2-t1_lastk)+t1_pzn+has_sel),t1_lastk:2}),(N(127),'DELK',{grp:grp+net.step(net.step(t1_lastk-3)+net.step(3-t1_lastk)+t1_pzn+has_sel),t1_lastk:3}),(N(13),'ENTER',{grp:grp+1}),(N(9),'TABK',{}),
 (net.and_(printable,nc),'TYPE',{}),
 (None,'HALT',None))
# find field typing
on('CMc',(None,'CMd',{r1:cb+CMTL}))
on('CMd',(None,'RD0',{w1:(cb+CMTL,net.relu(R1-1))}))
on('CMa',(None,'CMb',{r1:cb+CMTL}))
on('CMb',(net.ge(R1,380,S('CMb')),'RD0',None),(None,'RD0',{w1:(cb+CMT+R1,eva),w2:(cb+CMTL,R1+1)}))
on('FTYPE',(net.eq(mode,7,S('FTYPE')),'T2_TD',None),(net.eq(mode,6,S('FTYPE')),'RD0',None),(net.eq(mode,5,S('FTYPE')),'FNa',None),(net.eq(mode,4,S('FTYPE')),'CMa',None),(net.and_(net.eq(mode,3,S('FTYPE')),net.ge(hlen,255,S('FTYPE'))),'RD0',None),(net.eq(mode,3,S('FTYPE')),'RD0',{w1:(hfb+hlen,eva),hlen:hlen+1}),(field,'RD0',{w1:(as_x(RPL)+rlen,eva),rlen:rlen+1}),(None,'RD0',{w1:(as_x(Q)+qlen,eva),qlen:qlen+1,**CSTART}))
T1('keys')
ins_ch=R();ins_st=R();kprev=R();ins_rec=R();a6qk=R()
cont_ty=S('TYPE')
on('TYPE',(net.and_(has_sel,cont_ty),'DS0',{dret.r:dret.id('TY2'),grp:grp+1,t1_lastk:1}),(None,'TY2',{grp:grp+net.step(net.eq(eva,32,S('TYPE'))+net.step(net.step(t1_lastk-1)+net.step(1-t1_lastk))+t1_pz),t1_lastk:1}))
on('TY2',(net.and_(rv_ovr,net.lt(co,clen,S('TY2'))),'DEL',{oret.r:oret.id('RVA3_OV')}),(net.ge(clen,1000,S('TY2')),'RD0',None),(None,'INS',{ins_ch:eva,ins_st:TST,oret.r:oret.id('AF_FAST')}))
on('AF_FAST',(None,'AFTER_ED',{fastok:1}))
on('TABK',(None,'TK1',{r1:cb+2062,rc:cb+2062}))
on('TK1',(net.and_(net.step(R1),shiftk,net.step(cp)),'MVJ',{jp:cp-1,jo:0,jret.r:jret.id('MVEND')}),(net.and_(net.step(R1),net.ge(rc.out[1]+1,rc.out[0],S('TK1')),net.lt(cp+1,npar,S('TK1'))),'A4_TK0',{r1:as_x(PT)+cp+1,a4hk2:rc.out[0]}),(net.and_(net.step(R1),net.ge(rc.out[1]+1,rc.out[0],S('TK1'))),'T3_C_RB',None),(net.and_(net.step(R1),net.lt(cp+1,npar,S('TK1'))),'MVJ',{jp:cp+1,jo:0,jret.r:jret.id('A4_TS')}),(net.step(R1),'TAB2',{ins_ch:9,ins_st:TST,oret.r:oret.id('AFTER_ED')}),(None,'T2_TB',{r1:cb+LIST}));on('TAB2',(None,'INS',None))
tabn=R()
on('TAB3',(net.ge(tabn,3,S('TAB3')),'AFTER_ED',{tabn:0}),(None,'INS',{tabn:tabn+1,ins_ch:32,ins_st:TST,oret.r:oret.id('TAB3')}))
# while the background has not reached the caret it is below the viewport: an edit there needs no paint, since the background lays it out and then jumps to it
_a7e=S('AFTER_ED'); on('AFTER_ED',(net.and_(a7_far,bgp,net.ge(cp,bpi,_a7e)),'HALT',{ap:cp,ao:co,autos:0,blink:0,a7_jmp:1,fastok:0}),(net.and_(fastok,ONE-a7_far),'SYNC',{ap:cp,ao:co,autos:1,blink:0}),(None,'SYNC',{ap:cp,ao:co,autos:1,blink:0,lc:1}))
on('SYNC',(None,'RD0',{ap:cp,ao:co}))
on('BKSP',(has_sel,'DS0',{dret.r:dret.id('AFTER_ED')}),(trk,'T4_BK',None),(None,'BK1',{oret.r:oret.id('AFTER_ED')}))
on('BK1',(net.step(co),'DEL',{co:co-1}),(None,'T2_BK',{r1:cb+LIST}))
on('DELK',(has_sel,'DS0',{dret.r:dret.id('AFTER_ED')}),(trk,'T4_DK',None),(net.lt(co,clen,S('DELK')),'DEL',{oret.r:oret.id('AFTER_ED')}),
   (net.lt(cp+1,npar,S('DELK')),'DK2',{jp:cp+1,jo:0,jret.r:jret.id('DK3')}),(None,'AFTER_ED',None))
on('DK2',(None,'J0',None));on('DK3',(None,'MG0',{oret.r:oret.id('AFTER_ED')}))
on('ENTER',(has_sel,'DS0',{dret.r:dret.id('EN2')}),(None,'EN2',None))
on('EN2',(None,'EN3',{r1:cb+2062}))
on('EN3',(net.step(R1),'AFTER_ED',None),(None,'T2_EN0',{r1:cb+LIST,r2:cb+PSTY}))
on('PB0',(has_sel,'DS0',{dret.r:dret.id('PB1')}),(None,'PB1',None))
on('PB1',(None,'SPLIT',{oret.r:oret.id('PB2')}))
on('PB2',(None,'AFTER_ED',{w1:(cb+PBRK,1)}))
# ---- caret moves ----
def moved(c): return {autos:1,blink:0}
on('MOVL',(net.and_(has_sel,ONE-shiftk),'MVJ',{jp:lo_p,jo:lo_o,jret.r:jret.id('MVCL')}),(net.step(co),'MVEND',{co:co-1}),(net.step(cp),'MVJ',{jp:cp-1,jo:2047,jret.r:jret.id('MVEND')}),(None,'MVEND',None))
on('MVJ',(None,'J0',None));on('MVCL',(None,'MVEND',{ap:cp,ao:co}))
on('MOVR',(net.and_(has_sel,ONE-shiftk),'MVJ',{jp:hi_p,jo:hi_o,jret.r:jret.id('MVCL')}),(net.lt(co,clen,S('MOVR')),'MVEND',{co:co+1}),(net.lt(cp+1,npar,S('MOVR')),'MVJ',{jp:cp+1,jo:0,jret.r:jret.id('MVEND')}),(None,'MVEND',None))
# vertical and line moves read the last screenshot through the hit network
scr_cy=cy+DOCY-scroll
on('MOVU',(None,'HT',{hx_:cx,hy_:net.relu(scr_cy-3),hdir:1,hact:1}))
on('MOVD',(None,'HT',{hx_:cx,hy_:scr_cy+chh+3,hdir:0+2,hact:1}))
on('MOVH',(None,'HT',{hx_:cxl+2,hy_:scr_cy+2,hdir:0,hact:1}))
on('MOVE',(None,'HT',{hx_:cxr-6,hy_:scr_cy+2,hdir:0,hact:1}))
# line start or end lands on the shared end state
on('MVEND',(shiftk,'TYSY',{autos:1,blink:0}),(None,'TYSY',{ap:cp,ao:co,autos:1,blink:0,fastok:1}))
on('TYSY',(net.step(co),'TYS2',{rs:cb+1024+co-1}),(net.step(clen),'TYS2',{rs:cb+1024}),(None,'ASC0',None))
on('ASC0',(None,'ASC1',{r1:as_x(PT)+cp}))
on('ASC1',(None,'ASC2',{r2:R1+SAVE,rU:R1+ENDY}))
e=S('ASC2')
on('ASC2',(net.lt(rU.out[0],scroll+40,e),'RD0',{scroll:G_(net.relu(R2-40),net.step(cp)),fastok:0}),(net.gt(R2+20,scroll+VH-40,e),'RD0',{scroll:net.relu(R2+60-VH),fastok:0}),(None,'RD0',None))
on('SELALL',(None,'SA2',{ap:0,ao:0,jp:net.relu(npar-1),jo:2047,jret.r:jret.id('SA3')}));on('SA2',(None,'J0',None));on('SA3',(bsn,'BS_N',{bsn:0,bstg:0,t1_uid:1}),(None,'RD0',{autos:0}))
on('BS_N',(has_sel,'DS0',{dret.r:dret.id('AFTER_ED'),grp:grp+1}),(None,'RD0',None))
# ---- hit test on the screenshot ----
net.group('screenshot hit test')
T1('md')
e=S('MD'); on('MD',(net.and_(e,t1_ruler,net.ge(hy_,150,e),net.lt(hy_,174,e),ONE-t1_mopb),'A4_RM0',T1_CLICK),(None,'T3_H0',{hdir:0+3,hact:0,drag:1,grp:grp+1,vi:0,t1_lastk:0,**T1_CLICK}))
on('MD2',(None,'HT',{hdir:3,hact:2}))
on('HT',(None,'HT1',{pix:(hx_,hy_)}))
A_=pix.out[3]; e1=S('HT1')
on('HT1',(net.and_(e1,net.step(A_-199),net.eq(hact,2,e1)),'MVEND',None),(net.and_(e1,net.step(A_-199)),'BTN',{btn:A_-200,drag:0,t1_hov:A_,t1_prs:net.lt(A_,250,e1),t1_uid:net.and_(net.lt(A_,250,e1),ONE-t1_mopb)}),
 (net.step(A_),'VL0',{hcol:A_-1,vi:0}),
 (net.and_(e1,net.eq(hdir,1,e1),net.ge(hy_,DOCY+4,e1)),'HT',{hy_:hy_-3}),
 (net.and_(e1,net.eq(hdir,2,e1),net.lt(hy_,DOCB-4,e1)),'HT',{hy_:hy_+3}),
 (net.and_(e1,net.eq(hdir,3,e1),net.ge(hy_,DOCY+4,e1),net.lt(hy_,DOCB,e1)),'HT',{hy_:hy_-2}),
 (net.and_(e1,net.eq(hact,1,e1),net.eq(evk,2,e1),ONE-rv_try,net.eq(eva,129,e1),net.step(scroll),net.step(cp)),'RD0',{scroll:net.relu(scroll-240),rv_rekey:1,rv_try:1,autos:0}),
 (net.and_(e1,net.eq(hact,1,e1),net.eq(evk,2,e1),ONE-rv_try,net.eq(eva,131,e1),net.lt(cp+1,npar,e1)),'RD0',{scroll:scroll+240,rv_rekey:1,rv_try:1,autos:0}),
 (None,'MVEND',{drag:G_(drag,net.eq(hact,2,e1))}))
on('VL0',(None,'VL1',{rl:as_x(VL)+vi*6}))
RL=rl.out
e2=S('VL1')
vj=R()
on('VL1',(net.and_(e2,net.ge(hy_,RL[0],e2),net.lt(hy_,RL[1],e2),net.ge(hx_,RL[4],e2),net.lt(hx_,RL[5],e2)),'VLa',{jp:RL[2],vj:RL[3],r1:as_x(PT)+RL[2]}),
 (net.ge(vi,150,e2),'MVEND',None),(None,'VL0',{vi:vi+1}))
on('VLa',(None,'VLb',{rl:R1+LINES+vj*8}))
_rv_e=S('VLb'); on('VLb',(None,'J0',{jo:rl.out[0]+hcol,jret.r:jret.id('HEND'),rv_le:rl.out[1],rv_eol:net.and_(net.ge(rl.out[0]+hcol,rl.out[1],_rv_e),net.gt(rl.out[1],rl.out[0],_rv_e))}))
hactb=net.decode(hact,3,S('HEND'))
on('HEND',(hactb[0],'HE0',{}),(None,'MVEND',None))
_rv_e=S('HE0'); _rv_mg=net.lt(hx_,s_tx-3,_rv_e)
on('HE0',(rv_cmq,'RVA3_CM1',{rv_cmq:rv_cmq}),(shiftk,'MVEND',None),(net.and_(_rv_mg,net.eq(t1_clk,1,_rv_e)),'RD0',{ap:cp,ao:co,co:rv_le,drag:0,blink:0}),(net.and_(_rv_mg,net.eq(t1_clk,2,_rv_e)),'RD0',{ap:cp,ao:0,co:clen,drag:0,blink:0}),(net.and_(_rv_mg,net.eq(t1_clk,3,_rv_e)),'SELALL',{drag:0}),(net.eq(t1_clk,2,S('HE0')),'T1_W0',None),(net.eq(t1_clk,3,S('HE0')),'RD0',{ap:cp,ao:0,co:clen,drag:0,blink:0}),(None,'TYSY',{ap:cp,ao:co,blink:0}))
# ---- jump: load caret paragraph ----
on('J0',(None,'J1',{r1:as_x(PT)+jp}))
on('J1',(None,'J2',{cb:R1,r2:R1+LEN}))
on('J2',(None,'JR',{clen:R2,cp:jp,co:net.min_(jo,R2)}))
# ---- edit primitives with undo log ----
exec(open('rv_a7_regs.py').read())
net.group('edit primitives')
def mark_d(c,p): fsm.set(dfrom,c,net.min_(dfrom,net.relu(p-1)))
def log(c,op,p,o,ch,st):
    mark_d(c,p)
    cc=net.and_(c,ONE-nolog)
    wlog.drive(cc,(usp,op,p,o,ch,st,grp))
    wrap_=net.ge(usp,UEND_,cc); nxtu=net.gate(usp+6,cc-wrap_)+wrap_*UB
    fsm.set(usp,cc,nxtu); fsm.set(urp,cc,nxtu)
on('INS',(None,'I1',{rb:(cb+co,clen-co)}))
on('I1',(None,'I2',{wb:(cb+co+1,clen-co),rb:(cb+1024+co,clen-co)}))
e=S('I2'); log(e,1,cp,co,ins_ch,ins_st)
on('I2',(None,'OR',{wb:(cb+1024+co+1,clen-co),w1:(cb+co,ins_ch),w2:(cb+1024+co,ins_st),w3:(cb+LEN,clen+1),w4:(cb+DIRTY,1),co:co+1,clen:clen+1}))
on('DEL',(None,'D1',{r1:cb+co,r2:cb+1024+co}))
on('D1',(None,'D2',{ins_ch:R1,ins_st:R2,rb:(cb+co+1,net.relu(clen-co-1))}))
on('D2',(None,'D3',{wb:(cb+co,net.relu(clen-co-1)),rb:(cb+1024+co+1,net.relu(clen-co-1))}))
e=S('D3'); log(e,2,cp,co,ins_ch,ins_st)
on('D3',(None,'OR',{wb:(cb+1024+co,net.relu(clen-co-1)),w3:(cb+LEN,clen-1),w4:(cb+DIRTY,1),clen:clen-1}))
on('SPLIT',*A7_SPLIT,(net.ge(nextb,SLOTMAX,S('SPLIT')),'OR',None),(None,'S1',{rb:(cb+co,clen-co)}))
on('S1',(None,'S2',{wb:(nextb,clen-co),rb:(cb+1024+co,clen-co),rU:cb+PMK}))
on('S2',(None,'S3',{ra4:cb+A4C,wb:(nextb+1024,clen-co),w1:(nextb+LEN,clen-co),w2:(nextb+DIRTY,1),w3:(cb+LEN,co),w4:(cb+DIRTY,1),r1:cb+ALIGN,r2:cb+LIST,rp6:cb+PIND,a6pm2:rU.out[0]}))
on('S3',(None,'S4',{w3:(nextb+PMK,G_(a6pm2,ONE-a6nc)),w4:(cb+PMK,G_(trk,ONE-a6nc)+G_(a6pm2,a6nc)),rmeta:cb+META,rl:cb+A4T,wvl:(nextb+A4K,A4O[2],A4O[3],A4O[4],A4O[5],A4O[6],A4O[7]),w1:(nextb+ALIGN,R1),w2:(nextb+LIST,R2),wln:(nextb+PIND,*rp6.out),rb:(as_x(PT)+cp+1,net.relu(npar-cp-1))}))
e=S('S4'); log(e,3,cp,co,0,0)
on('S4',(None,'OR',{wln:(nextb+A4T,*rl.out[:6]),wvl:(nextb+CSH-2,0,0,MT[2],0,0,0),wb:(as_x(PT)+cp+2,net.relu(npar-cp-1)),w1:(as_x(PT)+cp+1,nextb),cp:cp+1,cb:nextb,co:0,clen:clen-co,npar:npar+1,nextb:G_(nextb+STRIDE,ONE-a7_re)+G_(a7_sv,a7_re),a7_re:0,a7_pre:0}))
pb=R();plen=R()
on('MERGE',(None,'M1',{r1:as_x(PT)+cp-1}))
on('M1',(None,'M2',{pb:R1,r2:R1+LEN,r1:cb+PMK}))
on('M2',(net.ge(R2+clen,1000,S('M2')),'OR',None),(None,'M3',{plen:R2,rb:(cb,clen),a6pm2:R1}))
on('M3',(None,'M4',{wb:(pb+plen,clen),rb:(cb+1024,clen)}))
on('M4',(None,'M5',{w3:(pb+PMK,a6pm2),wb:(pb+1024+plen,clen),w1:(pb+LEN,plen+clen),w2:(pb+DIRTY,1),rb:(as_x(PT)+cp+1,net.relu(npar-cp-1))}))
e=S('M5'); log(e,4,cp-1,plen,0,0)
a7_m5(e)
on('M5',(net.gt(npar-cp-1,1100,e),'A7_SD0',{wb:(as_x(PT)+cp,net.relu(npar-cp-1)),cp:cp-1,co:plen,cb:pb,clen:clen+plen,npar:npar-1,a7_ss:cp+1101,a7_sd:cp+1100,a7_sk:npar-cp-1101,a7sr.r:a7sr.id('OR')}),(None,'OR',{wb:(as_x(PT)+cp,net.relu(npar-cp-1)),cp:cp-1,co:plen,cb:pb,clen:clen+plen,npar:npar-1}))
on('MG0',(None,'MG1',{r1:as_x(PT)+cp-1}))
on('MG1',(None,'MG2',{rc:cb+2062,r2:R1+2062,rim:R1+IMF}))
on('MG2',(net.step(rc.out[0]+R2),'MGJ',{jp:cp-1,jo:2047,jret.r:jret.id('OR')}),(net.step(rim.out[0]),'T3_MP0',None),(None,'T3_MZ',None))
on('MGJ',(None,'J0',None))
# delete selection
e=S('DSL')
on('DSL',(net.ge(Ka,Kc,e),'DR',None),(net.step(co-1),'A7_D0',None),(net.step(co),'DEL',{co:co-1,oret.r:oret.id('DSL')}),(net.ge(cp-ap,3,e),'A7_P1',{rc:cb+2062}),(None,'MG0',{oret.r:oret.id('DSL')}))
# ---- undo and redo ----
net.group('undo')
U=rlog.out; uop=R();up=R();uo=R();uch=R();ust=R();ug=R();ub=R()
on('UNDO',(net.ge(usp,UB+6,S('UNDO')),'U1',{rlog:usp-6,nolog:1}),(None,'HALT',None))
on('U1',(None,'U2',{uop:U[0],up:U[1],uo:U[2],uch:U[3],ust:U[4],ug:U[5],usp:usp-6}))
h=net.decode(uop,13,S('U2'))
on('U2',*a7_undo_rules(h),(h[1],'UJ',{jp:up,jo:uo,jret.r:jret.id('DEL'),oret.r:oret.id('UCK')}),
 (h[2],'UJ',{jp:up,jo:uo,jret.r:jret.id('UI2'),oret.r:oret.id('UCK')}),
 (h[3],'UJ',{jp:up+1,jo:0,jret.r:jret.id('MERGE'),oret.r:oret.id('UCK')}),
 (h[4],'UJ',{jp:up,jo:uo,jret.r:jret.id('SPLIT'),oret.r:oret.id('UCK')}),
 (h[5],'UJ',{jp:up,jo:uo,jret.r:jret.id('UST'),oret.r:oret.id('UCK')}),(h[6],'UJ',{jp:up,jo:co,jret.r:jret.id('T1_UP')}),(h[7],'UCK',{w1:(up,uch)}),(h[8],'UJ',{jp:up,jo:2047,jret.r:jret.id('T3_US'),oret.r:oret.id('UCK')}),(None,'UCK',None))
on('UJ',(None,'J0',None))
on('UI2',(None,'INS',{ins_ch:uch,ins_st:ust}))
mark_d(S('UST'),cp);mark_d(S('VST'),cp)
on('UST',(None,'UCK',{w1:(cb+1024+co,uch),w2:(cb+DIRTY,1)}))
on('UCK',(net.ge(usp,UB+6,S('UCK')),'UCK2',{rlog:usp-6}),(None,'UEND',None))
on('UCK2',(net.eq(U[5],ug,S('UCK2')),'U1',{rlog:usp-6}),(None,'UEND',None))
on('UEND',(a4da,'A4_UD',{nolog:0,autos:1,blink:0,lc:1}),(None,'SYNC',{nolog:0,autos:1,blink:0,lc:1}))
on('REDO',(net.lt(usp,urp,S('REDO')),'V1',{rlog:usp,nolog:1}),(None,'HALT',None))
on('V1',(None,'V2',{uop:U[0],up:U[1],uo:U[2],uch:U[3],ust:U[4],ug:U[5],usp:usp+6}))
h=net.decode(uop,13,S('V2'))
on('V2',*a7_redo_rules(h),(h[1],'UJ',{jp:up,jo:uo,jret.r:jret.id('UI2'),oret.r:oret.id('VCK')}),
 (h[2],'UJ',{jp:up,jo:uo,jret.r:jret.id('DEL'),oret.r:oret.id('VCK')}),
 (h[3],'UJ',{jp:up,jo:uo,jret.r:jret.id('SPLIT'),oret.r:oret.id('VCK')}),
 (h[4],'UJ',{jp:up+1,jo:0,jret.r:jret.id('MERGE'),oret.r:oret.id('VCK')}),
 (h[5],'UJ',{jp:up,jo:uo,jret.r:jret.id('VST'),oret.r:oret.id('VCK')}),(h[6],'UJ',{jp:up,jo:co,jret.r:jret.id('T1_VP')}),(h[7],'VCK',{w1:(up,ust)}),(h[8],'UJ',{jp:up,jo:2047,jret.r:jret.id('T3_VS'),oret.r:oret.id('VCK')}),(None,'VCK',None))
on('VST',(None,'VCK',{w1:(cb+1024+co,ust),w2:(cb+DIRTY,1)}))
on('VCK',(net.lt(usp,urp,S('VCK')),'VCK2',{rlog:usp}),(None,'UEND',None))
on('VCK2',(net.eq(U[5],ug,S('VCK2')),'V1',{rlog:usp}),(None,'UEND',None))
# ---- range walker for copy and formatting ----
net.group('range walker')
wp=R();wbase=R();wo=R();wlen=R();wn=R();wm=R();wfirst=R();ftgt=R()
on('DS0',(trk,'T4_DS0',{wp:lo_p,wo:lo_o,wm:2,wfirst:1,fm:11,wret.r:wret.id('T4_DS1')}),(None,'DS1',{ap:lo_p,ao:lo_o,jp:hi_p,jo:hi_o,jret.r:jret.id('DSL')}));on('DS1',(None,'J0',None))
Kw=wp*2048+wo; wsel=Bus(net)
on('COPY',(has_sel,'W0',{wp:lo_p,wo:lo_o,wn:0,wm:1,wret.r:wret.id('COPYE')}),(None,'HALT',None))
on('CUT',(has_sel,'W0',{wp:lo_p,wo:lo_o,wn:0,wm:1,wret.r:wret.id('CUT2'),grp:grp+1}),(None,'HALT',None))
on('CUT2',(None,'DS0',{dret.r:dret.id('AFTER_ED'),clipl:wn+1,clipn:wn,clipi:0}))
on('COPYE',(None,'HALT',{clipl:wn+1,clipn:wn,clipi:0}))
clipout.add(S('HF'),clipl); fsm.set(clipl,S('HF'),0)
wantp=Bus(net); wantp.lin(S('HF')*0+wpaste); fsm.set(wpaste,S('HF'),0)
e=S('W0')
on('W0',(None,'W1',{r1:as_x(PT)+wp}))
on('W1',(None,'W2',{wbase:R1,r2:R1+LEN}))
on('W2',(None,'W3',{wlen:R2}))
e=S('W3')
on('W3',(net.and_(net.step(a7_rn),net.or_(net.ge(Kw,Hi,e),net.ge(wo,wlen,e))),'A7_FL',None),(net.ge(Kw,Hi,e),'WR',None),(net.and_(net.eq(wm,1,e),net.ge(wn,589900,e)),'WR',None),(net.ge(wo,wlen,e),'WNL',{}),(net.eq(wm,2,e),'A7_FW',{rpw:wbase+1024+wo,rs:wbase+1024+wo}),(net.eq(wm,1,e),'A7_CW',{rpw:wbase+wo}),(None,'W4',{r1:wbase+wo,rs:wbase+1024+wo}))
e=S('WNL')
on('WNL',(None,'WNL2',{wp:wp+1,wo:0,wn:wn+net.eq(wm,1,e)}))
wnl_c=net.and_(e,net.eq(wm,1,e)); w1.drive(wnl_c,(as_x(CB)+wn,10))
on('WNL2',(None,'W0',None))
# style arithmetic for formatting commands
fin=Bus(net); fen=Bus(net); fcl=Bus(net); FD=style_decode(fin.w,fen.w); FD.update(flag_decode(fcl.w,fen.w)); fsz=FD['size']
fin.add(S('TYS2'),RSR); fen.lin(S('TYS2'))
on('TYS2',(None,'ASC0',{ity:RSR-FD['vert']*ST_VERT}))
szh=net.decode(FD['si'],NS,fen.w)
_STEPS=[7,8,9,10,11,12,14,16,18,20,22,24,26,28,36,48,72]     # grow and shrink walk these points, as Word does
up_=X();dn_=X()
for i in range(NS):
    pt_=rom.SZ[i]; up_=up_+szh[i]*rom.sz_raw(rom.SZ.index(min([q_ for q_ in _STEPS if q_>pt_],default=72))); dn_=dn_+szh[i]*rom.sz_raw(rom.SZ.index(max([q_ for q_ in _STEPS if q_<pt_],default=7)))
fmh=net.decode(fm,16,fen.w); fcol=R(); fpre=R(); fcb=net.bits(fcol,5,fen.w); fcolraw=fcb[0]*256+fcb[1]*512+fcb[2]*1024+fcb[3]*131072+fcb[4]*262144
ffontraw=fcb[0]*128+fcb[1]*(1<<22)+fcb[2]*(1<<23)
tb=ONE-FD['bold'];ti=ONE-FD['ital'];tu=ONE-FD['und'];tf=ONE-FD['fb'][0];ts_=ONE-FD['strike'];tv_=G_(ONE-FD['sup'],fmh[13])+G_((ONE-FD['sub'])*2,fmh[14])
def field_new(tg):
    s_=fin.w
    return (G_(s_-FD['bold']*16+tg[0]*16,fmh[1])+G_(s_-FD['ital']*32+tg[1]*32,fmh[2])+G_(s_-FD['und']*64+tg[2]*64,fmh[3])
      +G_(s_-fsz+up_,fmh[4])+G_(s_-fsz+dn_,fmh[5])+G_(s_-FD['fontraw']+tg[3]*128,fmh[6])+G_(s_-FD['colraw']+fcolraw,fmh[7])+G_(fpre+0,fmh[8])
      +G_(s_-fsz+fsi,fmh[9])+G_(s_-FD['fontraw']+ffontraw,fmh[10])+G_(s_,fmh[11])
      +G_(s_-FD['strike']*ST_STRIKE+tg[4]*ST_STRIKE,fmh[12])+G_(s_-FD['vert']*ST_VERT+tg[5]*ST_VERT,fmh[13]+fmh[14])+G_(s_-FD['hl']*ST_HL+fhl*ST_HL,fmh[15]))
fist=wfirst
t_bold=G_(tb,fist)+G_(ftgt,ONE-fist);t_it=G_(ti,fist)+G_(ftgt,ONE-fist);t_un=G_(tu,fist)+G_(ftgt,ONE-fist);t_f=G_(tf,fist)+G_(ftgt,ONE-fist);t_s=G_(ts_,fist)+G_(ftgt,ONE-fist);t_v=G_(tv_,fist)+G_(ftgt,ONE-fist)
newst=field_new((t_bold,t_it,t_un,t_f,t_s,t_v))
tgt_now=G_(t_bold,fmh[1])+G_(t_it,fmh[2])+G_(t_un,fmh[3])+G_(t_f,fmh[6])+G_(t_s,fmh[12])+G_(t_v,fmh[13]+fmh[14])
on('FMTS',(has_sel,'W0',{wp:lo_p,wo:lo_o,wm:2,wfirst:1,grp:grp+1,wret.r:wret.id('FEND')}),(None,'FTY',{wfirst:1}))
fen.lin(S('W4')*1); fin.add(S('W4'),RSR); fcl.add(S('W4'),RSC); fen.lin(S('FTY')); fin.add(S('FTY'),ty)
on('FTY',(net.eq(fm,8,S('FTY')),'T2_SP0',{ity:net.relu(newst),wfirst:0}),(None,'RD0',{ity:net.relu(newst),wfirst:0}))
e=S('W4')
cc=net.and_(e,net.eq(wm,1,e)); w1.drive(cc,(as_x(CB)+wn,i2u(R1,cc)-net.eq(R1,11,cc))); 
fm_c=net.and_(e,net.eq(wm,2,e))
# the new record is interned in this tick; the next state writes its index with the cell's flags kept
ic_en.lin(fm_c); ic_val.add(fm_c,net.relu(newst)); ic_fb.add(fm_c,RSC-FD['flags'])
wcold=R(); wflg=R(); fsm.set(wcold,fm_c,RSC); fsm.set(wflg,fm_c,FD['flags']+net.and_(fm_c,fmh[11],ONE-FD['dele'])*ST_DEL)
fsm.set(ftgt,fm_c,tgt_now); fsm.set(wfirst,fm_c,0)
A4_W4(e)
on('W4',(fm_c,'W5',None),(None,'W3',{wo:wo+1,wn:wn+net.eq(wm,1,e)}))
e=S('W5'); wnew=ROUT+wflg
w2.drive(e,(wbase+1024+wo,wnew)); w3.drive(e,(wbase+DIRTY,1)); log(e,5,wp,wo,wcold,wnew)
on('W5',(None,'W3',{wo:wo+1}))
fsm.set(pfull,RFULL_,PMSG)
on('FEND',(net.eq(fm,8,S('FEND')),'T2_SP0',{ap:cp,ao:co,lc:1,ity:fpre}),(None,'RD0',{lc:1}))
# paragraph properties over the selected paragraphs
t2b=R()
on('SETAL',(None,'PA0',{pwalk:lo_p,pfld:ALIGN,grp:grp+1,t1_lastk:0}))
on('SETLI',(None,'PA0',{pwalk:lo_p,pfld:LIST,grp:grp+1,t1_lastk:0}))
on('PA0',(None,'PA1',{r1:as_x(PT)+pwalk}))
e=S('PA1'); mark_d(e,pwalk)
on('PA1',(None,'T1_PA',{t1_pb:R1,r2:R1+pfld}))
T1('para')
# ---- find and replace ----
net.group('find and replace')
fp=R();fbs=R();fo=R();fl=R();fk=R();wrap=R();rall=R();ri=R()
def low(x,en): return x+net.and_(net.ge(x,65,en),net.lt(x,91,en),ONE-t1_case)*32+net.and_(net.ge(x,192,en),net.lt(x,223,en),ONE-net.eq(x,215,en),ONE-t1_case)*32
def low0(x,en): return x+net.and_(net.ge(x,65,en),net.lt(x,91,en))*32   # ignores the find option
e=S('FIND')
on('FIND',(net.step(net.and_(net.eq(mode,2,e),has_sel)+0),'RP0',{grp:grp+1}),(None,'FN1',{fp:hi_p,fo:hi_o,wrap:0}))
on('FN1',(net.step(S('FN1')-net.step(qlen)),'RD0',None),(None,'A7_FQ1',{r1:as_x(Q)}))
e=S('F0')
on('F0',(net.and_(net.ge(fp,npar,e),wrap),'RD0',{rall:0,**CSTART}),(net.ge(fp,npar,e),'F0',{fp:0,fo:0,wrap:1}),(None,'F1',{r1:as_x(PT)+fp}))
on('F1',(None,'F2',{fbs:R1,r2:R1+LEN}))
on('F2',(None,'F3',{fl:R2,fk:0}))
e=S('F3')
on('F3',(net.step(fo+qlen-fl),'F0',{fp:fp+1,fo:0}),(net.and_(e,ONE-net.step(fk)),'A7_FF',{rpw:fbs+fo}),(None,'F4',{r1:fbs+fo+fk,r2:as_x(Q)+fk}))
e=S('F4'); m=net.eq(low(R1,e),low(R2,e),e)
on('F4',(net.and_(m,net.ge(fk+1,qlen,e),t1_fw),'T1_FW0',{r1:fbs+net.relu(fo-1),r2:fbs+fo+qlen}),(net.and_(m,net.ge(fk+1,qlen,e)),'FJ',{ap:fp,ao:fo,jp:fp,jo:fo+qlen,jret.r:jret.id('FOUND')}),(m,'F3',{fk:fk+1}),(None,'F3',{fo:fo+1,fk:0}))
on('FJ',(None,'J0',None))
on('FOUND',(net.and_(S('FOUND'),rall),'RP0',{wrap:wrap}),(None,'RD0',{autos:1,blink:0,**CSTART}))
T1('find')
on('RP0',(None,'DS0',{dret.r:dret.id('RP1')}))
on('RP1',(None,'RP2',{ri:0}))
e=S('RP2')
on('RP2',(net.ge(ri,rlen,e),'RP4',None),(None,'RP3',{r1:as_x(RPL)+ri}))
on('RP3',(None,'INS',{ins_ch:R1,ins_st:TST,ri:ri+1,oret.r:oret.id('RP2')}))
on('RP4',(None,'SYNC2',{ap:cp,ao:co})); on('SYNC2',(None,'FIND2',None))
on('FIND2',(None,'FN1',{fp:cp,fo:co,wrap:0}))
# ---- paste ----
net.group('paste')
CB2=CB+200000; pi_=R()
on('PASTE',(net.eq(mode,6,S('PASTE')),'T4_M0',{mode:0}),(has_sel,'DS0',{dret.r:dret.id('PS1'),grp:grp+1}),(None,'PS1',{grp:grp+1}))
on('PS1',(None,'PS2',{pi_:0}))
# Block paste. A window of cells is read at once. Their control characters are weighted by
# position so one threshold layer finds how many cells lead before the first of them, and those
# cells go to the paragraph, the styles and the undo log in a single write. A window that starts
# with a control character, or a full paragraph, takes the single character path.
PSN=32
pn_=R(); PSW_=rpw.out
e=S('PS2')
_pe=net.or_(net.ge(pi_,evc,e),net.ge(nextb,SLOTMAX,e))
on('PS2',(net.and_(_pe,net.step(a7_pn)),'A7_PF',None),(_pe,'AFTER_ED',None),(net.and_(net.ge(usp,UEND_-2200,e),ONE-net.step(a7_pn)),'PS2',{usp:UB,urp:UB}),(None,'PSW',{rpw:as_x(CB2)+pi_}))
e=S('PSW')
_bad=[net.step(as_x(32)-PSW_[i_]-0.5+e*M-M)+net.step(PSW_[i_]-126.5+e*M-M) for i_ in range(PSN)]
_score=sum((_bad[i_]*float(2**(PSN-1-i_)) for i_ in range(PSN)),X())
_lead=e*PSN-sum((net.step(_score-float(2**(PSN-1-i_))+0.5) for i_ in range(PSN)),X())
_n1=_lead-net.relu(_lead-(evc-pi_)+e*M-M)
_cap=net.relu(as_x(1000)-clen+e*M-M)
_n2=_n1-net.relu(_n1-_cap+e*M-M)
_tail=clen-co
on('PSW',(net.and_(net.step(a7_pn),ONE-net.step(_n2)),'A7_PF',None),(ONE-net.step(_n2),'PS3',{r1:as_x(CB2)+pi_}),(net.step(_tail),'PSS1',{pn_:_n2,rb:(cb+co,_tail)}),(None,'PSY',{pn_:_n2,rpw:as_x(CB2)+pi_}))
on('PSS1',(None,'PSS2',{wb:(cb+co+pn_,clen-co),rb:(cb+1024+co,clen-co)}))
on('PSS2',(None,'PSY',{wb:(cb+1024+co+pn_,clen-co),rpw:as_x(CB2)+pi_}))
e=S('PSY'); mark_d(e,cp)
_st=[net.wire() for _ in range(PSN)]
_tyg=G_(TST,e)
for w_ in _st: net.connect(w_,_tyg)
wpst.ext=_st[0]; net.aligned.append([next(iter(w_.t)) for w_ in _st])
cc_=net.and_(e,ONE-nolog)
wplc=WPort(PSN,rpw.out[0],True); wplc.drive(cc_,(usp+6+a7_pn,pn_)); fsm.set(a7_pp,cc_,cp); fsm.set(a7_po,net.and_(cc_,ONE-net.step(a7_pn)),co); fsm.set(a7_pn,cc_,a7_pn+pn_)
on('PSY',(None,'PS2',{wpch:(cb+co,pn_),wpst:(cb+1024+co,pn_),w3:(cb+LEN,clen+pn_),w4:(cb+DIRTY,1),co:co+pn_,clen:clen+pn_,pi_:pi_+pn_}))
e=S('PS3')
on('PS3',(net.eq(R1,10,e),'SPLIT',{pi_:pi_+1,oret.r:oret.id('PS2')}),(net.and_(net.lt(R1,32,e),ONE-net.eq(R1,9,e)),'PS2',{pi_:pi_+1}),(net.ge(clen,1000,e),'PS2',{pi_:pi_+1}),(None,'T2_PS',{ins_ch:R1,pi_:pi_+1}))
exec(open('rv_a7_bulk.py').read())
# ---- layout and paint walk ----
net.group('layout and paint')
ls_=R();le_=R();lx=R();lhh=R();lasc=R();lex=R();off=R();col=R();x=R();lb=R();lbx=R();lspb=R();lsn=R();xw=R();prevsp=R();wc=R()
lend=R();lwid=R();lspc=R();llast=R();pcp=R();cacol=R();thumb=R()
tpad=net.step(tcols)*6
xc_=net.step(xcol)
lleft=rleft+G_(s_tx-s_px+xcol,xc_)
lright=rright+xcol
GRAY=(230,230,230);WHITE=(255,255,255);SEL=PAL_B[1]
_rv_r0=S('RD0'); fsm.set(rv_hl,_rv_r0,net.and_(net.ge(mode,1,_rv_r0),net.lt(mode,3,_rv_r0),net.step(qlen))); fsm.set(rv_mhe,S('R4'),0)
on('RD0',(None,'RD1',{clip0:DOCY,clip1:800-DOCB,full:ONE-net.and_(S('RD0'),fastok,ONE-wassel,ONE-has_sel,ONE-a7_far),fastok:0}))
fsm.set(a7_wb,S('RD1'),0); fsm.set(a7_vw,net.and_(S('RD1'),a7_far,bgp,ONE-lc),1); fsm.set(a7_vw,S('RE1'),0)   # a walk of the viewport alone: it leaves the background's saved position alone
minc=net.min_(cp,oldcp);maxc=net.max_(cp,oldcp)
e=S('RD1')
on('RD1',(net.and_(e,ONE-full),'RF0',{sidx:minc,vm:0}),
 (lc,'VS2048',{rA:(0,DOCY,1262,VH,GRAY,0),sidx:0,vm:0,vln:0,bgp:0,hitn:0}),
 (None,'VS2048',{rA:(0,DOCY,1262,VH,GRAY,0),sidx:0,vm:1,vln:0,hitn:0}))
on('VSEND',(lc,'RF0',{sidx:net.min_(sidx,dfrom)}),(None,'RF0',None))
on('RF0',(None,'RF1',{r1:as_x(PT)+sidx}))
on('RF1',(None,'RF2',{r2:R1+FNHT,rl:R1+SAVE,rc:R1+2062,rf:R1+FNS,rmeta:R1+META}))
RL=rl.out
fload={fnh:R2,fnn:rf.out[0],fnp:rf.out[1],yy:RL[0],ptop:RL[1],pages:RL[2],wsum:RL[3],listn:RL[4],xcol:RL[5],pi:sidx}
RC=rc.out
on('RF2',(net.and_(full,net.step(RC[1])),'RF0',{sidx:sidx-RC[1]}),(None,'T3_RS0',{**fload,rowmax:0,cursec:MT[7]}))
on('T3_RS0',(None,'T3_RS1',{rl:as_x(SECB)+cursec*8}))
def sload(W_): return {ncol:W_[0],s_pw:W_[1],s_ph:W_[2],s_px:W_[3],s_tx:W_[4],s_tw:W_[5],s_mt:W_[6],s_th:W_[7],s_ps:W_[2]+16}
on('T3_RS1',(bgm,'R1',sload(RL)),(full,'T3_RS2',sload(RL)),(None,'R1',sload(RL)))
def page_shadow(st,nxt,top,keep=None):
    "A soft shadow from three nested rectangles, then the page. Alpha stays 0."
    a_=dict(keep or {}); a_.update({rA:(s_px-3,top-2,s_pw+7,s_ph+6,(226,226,226),0),rB:(s_px-2,top-1,s_pw+5,s_ph+4,(216,216,216),0),rC:(s_px-1,top,s_pw+3,s_ph+2,(198,198,198),0)})
    on(st,(None,nxt,a_))
on('T3_RS2',(None,'T3_RS3',{rA:(s_px-3,ptop+DOCY-scroll-2,s_pw+7,s_ph+6,(226,226,226),0),rB:(s_px-2,ptop+DOCY-scroll-1,s_pw+5,s_ph+4,(216,216,216),0),rC:(s_px-1,ptop+DOCY-scroll,s_pw+3,s_ph+2,(198,198,198),0)}))
on('T3_RS3',(None,'PNV',{rB:(s_px,ptop+DOCY-scroll,s_pw,s_ph,WHITE,0)}))
steps=[2048,1024,512,256,128,64,32,16,8,4,2,1]
for i,st_ in enumerate(steps):
    nxt=f'VS{steps[i+1]}' if i+1<len(steps) else 'VSEND'
    e=S(f'VS{st_}')
    on(f'VS{st_}',(net.lt(sidx+st_,npar,e),f'VSa{st_}',{r1:as_x(PT)+sidx+st_}),(None,nxt,None))
    on(f'VSa{st_}',(None,f'VSb{st_}',{r2:R1+SAVE+1}))
    e=S(f'VSb{st_}')
    on(f'VSb{st_}',(net.ge(scroll,R2+PST,e),nxt,{sidx:sidx+st_}),(None,nxt,None))
e=S('R1')
fsm.set(a7_far,net.and_(S('R1'),a7_vw,net.ge(pi,npar,S('R1'))),0)
saveb={bfnh:fnh,bsec:cursec,bfn:fnn,bfp:fnp,bxc:xcol,bpi:pi,byy:yy,bptop:ptop,bpg:pages,bws:wsum,bln:listn}
on('R1',(net.and_(a4hw,net.ge(pi,a4he,e)),'A4_HC',None),(a4hw,'R2',{r1:as_x(PT)+pi}),(net.and_(a7_vw,net.gt(yy,scroll+VH,e),net.gt(pi,cp,e),net.or_(xc_,net.lt(ncol,2,e))),'RE0',{a7_far:0}),(net.and_(a7_vw,net.gt(yy,scroll+VH,e),net.or_(xc_,net.lt(ncol,2,e))),'RE0',{autos:0,a7_jmp:net.or_(a7_jmp,autos)}),(net.and_(bgm,net.ge(pi,npar,e)),'BGD',None),(net.and_(net.ge(pi,npar,e),full,ONE-vm,net.step(fnp)),'T3_PFE',{pfc:fnp,pff:fnn-fnp,pfh:fnh,pfy:ptop+s_mt+s_th,pfx:s_tx,pfw:s_tw}),(net.and_(net.ge(pi,npar,e),full,vm,net.step(fnp)),'T3_PFE',{pfc:fnp,pff:fnn-fnp,pfh:fnh,pfy:ptop+s_mt+s_th,pfx:s_tx,pfw:s_tw}),(net.ge(pi,npar,e),'RE0',None),
 (net.and_(bgm,net.ge(bcnt,60,e)),'HALT',{**saveb,bgm:0}),(net.and_(full,ONE-vm,ONE-bgm,net.ge(a7_wb,A7BUD,e),net.gt(yy,scroll+VH,e),net.or_(xc_,net.lt(ncol,2,e))),'RE0',{**saveb,bgp:1,autos:0,a7_far:ONE-net.gt(pi,cp,e),a7_jmp:autos}),(net.and_(full,ONE-vm,ONE-bgm,net.ge(a7_wb,A7BUD,e)),'RD0',{**saveb,bgp:1,lc:0,a7_far:ONE-net.gt(pi,cp,e),a7_jmp:autos,autos:0}),(net.and_(full,ONE-vm,ONE-bgm,autos,net.gt(pi,cp,e),net.lt(cy,scroll+40,e),net.or_(xc_,net.lt(ncol,2,e))),'RE0',{**saveb,bgp:1}),(net.and_(full,ONE-vm,ONE-bgm,ONE-autos,has_sel,net.gt(yy,scroll+VH,e),net.or_(xc_,net.lt(ncol,2,e))),'RE0',{**saveb,bgp:1}),
 (net.and_(full,ONE-vm,ONE-bgm,net.gt(yy,scroll+VH,e),net.gt(pi,cp,e),net.or_(xc_,net.lt(ncol,2,e))),'RE0',{**saveb,bgp:1}),(net.and_(ONE-full,net.gt(pi,maxc,e)),'RE0',None),(net.and_(vm,net.gt(yy,scroll+VH,e),net.or_(xc_,net.lt(ncol,2,e))),'RE0',None),(None,'R2',{r1:as_x(PT)+pi}))
on('R2',(None,'R3',{r2:R1+PMK,ra4:R1+A4C,rmeta:R1+META,rim:R1+IMF,pbs:R1,rl:R1+LEN,rc:R1+2062,rf:R1+FNS,rp6:R1+PIND}))
on('R2X',(None,'R3',{r2:pbs+PMK,ra4:pbs+A4C,rmeta:pbs+META,rim:pbs+IMF,rl:pbs+LEN,rc:pbs+2062,rf:pbs+FNS,rp6:pbs+PIND}))
RL=rl.out
pbk=R()
e3=S('R3'); tb3=net.step(rc.out[0]); nt3=ONE-tb3
two=net.and_(nt3,net.eq(ncol,2,e3)); one3=net.and_(nt3,ONE-two); col2=(s_tw-24)*0.5
geom_w=G_(MT[0],tb3)+G_(s_tw,one3)+G_(col2,two); geom_x=G_(MT[1],tb3)
shh=net.decode_z(MT[2],len(PAL_B),e3)
def bcv(k): return sum((shh[i_]*PAL_B[i_][k] for i_ in range(len(PAL_B))),X())
meta0={ptoc:MT[4],ptsrc:MT[5],ptpg:MT[6],bc0:bcv(0),bc1:bcv(1),bc2:bcv(2),pbg:MT[2],pim:rim.out[0],pih:rim.out[1],pio:rim.out[2],pfn:rf.out[2],tcols:rc.out[0],tci:rc.out[1],rw:geom_w,rx0:geom_x,rleft:G_(s_px,nt3)+G_(s_tx+1+MT[1],tb3),rright:G_(s_px+s_pw,one3)+G_(s_tx+col2,two)+G_(s_tx+MT[1]+MT[0],tb3)}
newsec=net.and_(e3,net.step(MT[3]),net.step(net.step(MT[3]-1-cursec-0.5)+net.step(cursec-MT[3]+1-0.5)))
lb3=net.bits(RL[3],4,e3)
meta={**A4_META(e3),**meta0,plen_:RL[0],al:RL[2],lsf:lb3[0]+lb3[1]*2,plvl:lb3[2]+lb3[3]*2,pind:rp6.out[0],pfirst_:rp6.out[1],plsp:rp6.out[2],pspb:rp6.out[3],pspa:rp6.out[4],psty:rp6.out[5],lfi:rp6.out[1],nl:RL[4],wdp:RL[5],oend:RL[6],pbk:RL[7],a6pm:R2}
on('R3',(newsec,'T3_SB0',{cursec:MT[3]-1,rl:as_x(SECB)+(MT[3]-1)*8}),(net.step(RL[1]),'LAY0',{**meta,lfn:0,lfb:0,lfh:0,lfnb:0,lfhb:0,lj:0,ls_:0,off:0,lx:0,lb:0,lbx:0,lsn:0,lspb:0,lasc:0,lhh:0,wc:0,prevsp:1,llast:0}),(None,'R3B',meta))
e=S('R3B')
pb_=net.and_(ONE-net.eq(a4hlast,pi+1,e),net.or_(a4kbr,net.and_(pbk,net.gt(yy,ptop+s_mt,e)),net.and_(net.step(tcols),net.eq(tci,0,e),net.gt(yy+60,ptop+s_mt+s_th,e))))
pfsave={pfc:fnp,pff:fnn-fnp,pfh:fnh,pfy:ptop+s_mt+s_th,pfx:s_tx,pfw:s_tw,fnh:0}
pnew={**pfsave,fnp:0,ptop:ptop+s_ps,yy:ptop+s_ps+s_mt,pages:pages+1,xcol:0}
on('R3B',(net.and_(net.step(tcols),net.eq(tci,0,e),ONE-a4hw,net.gt(yy,ptop+s_mt,e),net.step(net.step(pi+1-a4kd-0.5)+net.step(a4kd-pi-1-0.5))),'A4_KR0',None),(net.and_(a4kf,ONE-net.step(tcols),net.gt(yy,ptop+s_mt,e),net.step(net.step(pi+1-a4kd-0.5)+net.step(a4kd-pi-1-0.5))),'A4_K0',None),(net.and_(pb_,full),'PSH_B',{**pnew,rB:(s_px-2,ptop+s_ps+DOCY-scroll-1,s_pw+5,s_ph+4,(216,216,216),0),rC:(s_px-1,ptop+s_ps+DOCY-scroll,s_pw+3,s_ph+2,(198,198,198),0)}),(pb_,'A4_H0',pnew),(None,'R4',None))
e=S('R4'); e_=net.and_(e,ONE-a4hw)
w4.drive(e_,(pbs+FNHT,fnh))
def list_step(ln_,kind,lvl,e):
    "Multi level list counters, 8 bits per level packed in one cell. Returns the new pack and this item's number."
    lbits=net.bits(ln_,24,e); lc0=sum((lbits[i]*(1<<i) for i in range(8)),X()); lc1=sum((lbits[8+i]*(1<<i) for i in range(8)),X()); lc2=sum((lbits[16+i]*(1<<i) for i in range(8)),X())
    lvh=net.decode(lvl,4,e); isnum=net.eq(kind,2,e); inlist=net.step(kind)
    deep=lvh[2]+lvh[3]
    n0=G_(lc0+net.and_(isnum,lvh[0]),net.and_(e,inlist,ONE-net.and_(lvh[0],net.eq(kind,1,e)))); n1=G_(lc1+net.and_(isnum,lvh[1]),net.and_(e,inlist,ONE-lvh[0])); n2=G_(lc2+net.and_(isnum,deep),net.and_(e,inlist,deep))
    return n0+n1*256+n2*65536, G_(n0,lvh[0])+G_(n1,lvh[1])+G_(n2,deep)
nlist,mk_now=list_step(listn,lsf,plvl,e)
fsm.set(mkn,e,mk_now)
w3.drive(e_,(pbs+SSI,cursec));wln.drive(e_,(pbs+SAVE,yy,ptop,pages,wsum,listn,xcol));w1.drive(e_,(pbs+FNS,fnn));w2.drive(e_,(pbs+FNS+1,fnp))
intab=net.step(tcols); c0=net.eq(tci,0,e)
fsm.set(rowtop,net.and_(e,c0),yy); fsm.set(rowmax,net.and_(e,c0),0)
rA.drive(net.and_(e,intab,full),(rleft,yy+DOCY-scroll,net.relu(rw-1),3,(bc0,bc1,bc2),0))
on('R4',(intab,'R5',{wsum:wsum+wdp,lj:0,listn:nlist,yy:yy+3}),(net.gt(yy,ptop+s_mt,e),'A4_R5',{wsum:wsum+wdp,lj:0,listn:nlist,yy:yy+pspb}),(None,'A4_R5',{wsum:wsum+wdp,lj:0,listn:nlist}))
e=S('R5')
on('R5',(net.ge(lj,nl,e),'RP',None),(None,'R6',{rl:pbs+LINES+lj*8,r2:pbs+LINES+lj*8+11}))
def keep_lines(e,y,top,h0,h1,j,n,mt,th,extra=0):
    "True when this line must start a new page so that no single line is stranded."
    bt=as_x(top)+mt+th; over2=net.gt(as_x(y)+h0+h1+extra,bt,e); over3=net.gt(as_x(y)+h0+h1*2+extra,bt,e)
    n2=net.eq(n,2,e);n3=net.eq(n,3,e);n4=net.ge(n,4,e);j0=net.eq(j,0,e)
    return net.and_(net.gt(y,as_x(top)+mt,e),net.or_(net.and_(j0,n2,over2),net.and_(j0,n3,over3),net.and_(j0,n4,over2),net.and_(n4,net.eq(as_x(j)+2,n,e),over2)))
e=S('R6'); fnx_=fnh+RL[7]+net.step(fnh+RL[7])*14
ne=net.or_(net.and_(net.gt(yy+RL[3]+fnx_,ptop+s_mt+s_th,e),net.gt(yy,ptop+s_mt,e)),net.and_(ONE-net.step(tcols),keep_lines(e,yy,ptop,RL[3],R2,lj,nl,s_mt,s_th,fnx_)))
lm={lnfh:RL[7],ls_:RL[0],le_:RL[1],lx:RL[2],lhh:RL[3],lasc:RL[4],lex:RL[5]}
c1=net.and_(ne,net.eq(ncol,2,e),ONE-net.step(xcol))
on('R6',(c1,'T3_R6X',{**lm,yy:ptop+s_mt,xcol:col2+24}),(net.and_(ne,full),'PSH_N',{**pfsave,**lm,fnp:0,xcol:0,ptop:ptop+s_ps,yy:ptop+s_ps+s_mt,pages:pages+1,rB:(s_px-2,ptop+s_ps+DOCY-scroll-1,s_pw+5,s_ph+4,(216,216,216),0),rC:(s_px-1,ptop+s_ps+DOCY-scroll,s_pw+3,s_ph+2,(198,198,198),0)}),(ne,'T3_R6X',{**pfsave,**lm,fnp:0,xcol:0,ptop:ptop+s_ps,yy:ptop+s_ps+s_mt,pages:pages+1}),(None,'T3_R6X',lm))
def _t10(v,e):
    b_=net.gate(v,e); t_=X()
    for k_ in range(1,10): t_=t_+net.step(b_-10*k_+0.5)
    return t_
pgret=Ret('T3_PGR')
def page_num(st0,nxt): on(st0,(None,'T3_PFT',{pgret.r:pgret.id(nxt)}))
on('PSH_B',(None,'PNB',{rB:(s_px,ptop+DOCY-scroll,s_pw,s_ph,WHITE,0)}));on('PSH_N',(None,'PN',{rB:(s_px,ptop+DOCY-scroll,s_pw,s_ph,WHITE,0)}))
page_num('T3_PS','R2X');page_num('PN','T3_R6X');page_num('PNV','R1');page_num('PNB','A4_H0');page_num('PN0','R1')
e=S('R7')
here=net.and_(ONE-a4hw,net.eq(pi,cp,e),net.or_(net.and_(ONE-rv_eol,net.ge(co,ls_,e),net.or_(net.lt(co,le_,e),net.eq(le_,plen_,e))),net.and_(rv_eol,net.gt(co,ls_,e),net.ge(le_,co,e))))
fsm.set(cy,here,yy);fsm.set(chh,here,lhh);fsm.set(pcp,here,pages);fsm.set(cxl,here,lleft);fsm.set(cxr,here,lright)
vis=net.and_(net.gt(yy+lhh,scroll,e),net.lt(yy,scroll+VH,e))
pa=net.or_(full,net.eq(pi,cp,e),net.eq(pi,oldcp,e))
cvl=net.and_(vis,full); wvl.drive(cvl,(as_x(VL)+vln*6,yy+DOCY-scroll,yy+DOCY-scroll+lhh,pi,lj,lleft,lright)); fsm.set(vln,cvl,vln+1)
on('R7',(net.and_(vis,pa),'R8',None),(None,'R9',None))
sy=yy+DOCY-scroll
indb=net.gate(plvl*48+48,net.step(lsf))
ind=indb+net.eq(ptoc,2,S('R8'))*24
e=S('R8')
tx0=s_tx+rx0+xcol+tpad-48; r8a={rA:(lleft,sy,lright-lleft,lhh,(bc0,bc1,bc2),1),rB:(s_tx+xcol-12,sy,1,lhh,WHITE,0),x:tx0+ind+lx,off:ls_,col:1}    # the whole line is cleared first; characters then only set ids, so a letter's overhang survives its neighbor
on('R8',(net.and_(net.eq(ls_,0,e),net.eq(lsf,1,e)),'BUL',r8a),(net.and_(net.eq(ls_,0,e),net.eq(lsf,2,e)),'NUM',r8a),(None,'C0',r8a))
gly_y=sy+lasc-asc_e-rise
BULS=[127,ord('o'),150,150]
e=S('BUL'); bh=net.decode(plvl,4,e); bch=X()
for i_,b_ in enumerate(BULS): bch=bch+bh[i_]*b_
on('BUL',(None,'C0',{gly:(bch,0,x-24,gly_y,0,0)}))
mk_i=R()
on('NUM',(None,'NUM2',{mk_i:0,sx:x-24}))
on('NUM2',(None,'NUM3',{r1:as_x(MKT)+net.min_(plvl,2)*2048+mkn*8+mk_i}))
on('NUM3',(net.step(R1),'NUM2',{gly:(R1,0,sx,gly_y,0,0),sx:sx+adv,mk_i:mk_i+1}),(None,'C0',None))
e=S('C0')
exec(open('rv_a3_paint.py').read()); e=S('C0')
on('C0',(net.ge(off,le_,e),'CE',None),(net.and_(rv_hl,net.ge(off,rv_mhe,e)),'RVA3_H0',{rv_hk:0}),(None,'C1',{r1:pbs+off,rs:pbs+1024+off}))
fsm.set(kprev,S('R8'),0)
e=S('C1')
Kp=pi*2048+off; insel=net.and_(net.ge(Kp,Lo,e),net.lt(Kp,Hi,e)); rv_mh=net.and_(rv_hl,ONE-insel,net.lt(off,rv_mhe,e)); nosel=e-insel-rv_mh
isfnc=net.ge(R1,1000,e); isp=net.eq(R1,32,e); xtra=G_(lex,isp)+rv_tabw(x-(tx0+48),net.eq(R1,9,e)); _rv_ne=net.and_(e,rv_eol); chere=net.and_(net.eq(pi,cp,e),net.eq(off,co,e),ONE-net.eq(off,ls_,_rv_ne))
fsm.set(cx,chere,x);fsm.set(cacol,chere,col)
g_en.lin(e);g_ch.add(e,R1);g_st.add(e,RSR);g_fl.add(e,RSC);g_x.add(e,x+kern+0.5);g_y.add(e,gly_y+YB)
ke2=net.and_(e,net.step(kprev));kp_en.lin(ke2);kp_in.add(ke2,kprev)
g_draw.lin(e-isp-isfnc)
trk_=net.and_(e,net.or_(SD['ins'],SD['dele'])); a2_chg=R(); fsm.set(a2_chg,trk_,1)   # tracked text is drawn in the review color
colh=net.decode_z(G_(SD['color'],ONE-trk_)+trk_*4,32,e)
for j in range(32): fg[j].lin(colh[j])
hlh=net.decode_z(SD['hl'],8,e); nohl=net.and_(nosel,hlh[0])
fld_=net.and_(nohl,net.or_(SD['f0'],SD['f1']))    # fields get a light shade
bg[1].lin(insel);bg[3].lin(fld_)
nsh_=nohl-fld_; bgh_=net.decode_z(pbg,len(PAL_B),nsh_)   # the plain background is the cell shade
for j in range(len(PAL_B)): bg[j].lin(bgh_[j])
hlcol=[insel*SEL[i]+fld_*PAL_B[3][i] for i in range(3)]
for h_i in range(1,8):
    hn=net.and_(nosel,hlh[h_i]); bg[5+h_i].lin(hn)
    for i in range(3): hlcol[i]=hlcol[i]+hn*PAL_B[5+h_i][i]
bg[6].lin(rv_mh); hlcol=[hlcol[i]+rv_mh*PAL_B[6][i] for i in range(3)]
adv2=adv*0.5
for rr,xx,ww,aa in ((rA,x,adv2+1,col),(rB,x+adv2,adv2+1+xtra+kern,col+1)):
    rr.b[0].lin(e)
    for b,val in zip(rr.b[1:],(xx,sy+YB,ww,lhh)): b.add(e,val)
    for i in range(3): rr.b[5+i].lin(hlcol[i])
    rr.b[5].lin(nsh_*(-1))
    rr.b[8].add(e,aa)
und=net.and_(e,net.or_(SD['und'],SD['ins'])); ske=net.and_(e,net.or_(SD['strike'],SD['dele']))
for rr,en_,yv in ((rC,und,sy+lasc+2-rise),(rD,ske,sy+lasc-strk-rise)):
    rr.b[0].lin(en_)
    for b,val in zip(rr.b[1:5],(x+kern,as_x(yv)+YB,adv+xtra+1,X(c=1))): b.add(en_,val)
    for i in range(3):
        cv=X()
        for j in range(32): cv=cv+colh[j]*PAL_F[j][i]
        rr.b[5+i].add(en_,cv)
    rr.b[8].add(en_,col)
mk_=net.and_(e,isp,t1_marks,ONE-und); rC.drive(mk_,(x+net.gate(adv*0.5,mk_),sy+lasc-6,2,2,(120,120,160),col))
exec(open('t4_spell.py').read())
adv_c={x:x+adv+kern+xtra,col:col+1,off:off+1,kprev:R1}
on('C1',(net.eq(R1,9,e),'A4_PT0',None),(net.and_(net.ge(R1,300,e),ONE-isfnc),'A6Q_C0',{a6qk:R1-300,a6qs:insel}),(isfnc,'T3_CF0',None),(sp_bad,'A6D_0',{**adv_c,sx:sp_x0,sp_xe:x,sp_r:0,a6oe:off}),(net.ge(off+1,le_,e),'CE',adv_c),(rv_hl,'C0',adv_c),(None,'C1',{**adv_c,r1:pbs+off+1,rs:pbs+1024+off+1}))
e=S('CE'); chere2=net.and_(net.eq(pi,cp,e),net.eq(off,co,e))
fsm.set(cx,chere2,x);fsm.set(cacol,chere2,col)
mk2=net.and_(e,t1_marks,net.eq(le_,plen_,e)); rB.drive(mk2,(x+5,sy+lasc-12,1,14,(120,120,160),col)); rC.drive(mk2,(x+1,sy+lasc-12,4,6,(120,120,160),col))
mk3=net.and_(e,ONE-t1_marks,net.eq(le_,plen_,e),net.step(a6pm),ONE-net.step(tcols)); rB.drive(mk3,(x+5,sy+lasc-12,1,14,(187,0,0),col)); rC.drive(mk3,(x+1,sy+lasc-12,4,6,(187,0,0),col))   # rv_a6: a tracked paragraph mark
on('IM0',(net.ge(irow,pih,S('IM0')),'T3_IH0',None),(None,'IM0',{imr:(x,sy+irow,as_x(IMG0)+pio+iaddr,pim,1,1),irow:irow+1,iaddr:iaddr+pim}))
_ce_fill=(x,sy,lright-x,lhh,(-1,0,0),net.min_(col,199)-net.eq(kprev,11,e))
a2_pm=net.and_(e,net.eq(le_,plen_,e),net.ge(pi*2048+le_,Lo,e),net.lt(pi*2048+le_,Hi,e)); rD.drive(a2_pm,(x,sy,net.min_(5,net.relu(lright-x)),lhh,SEL,net.min_(col,199)))
on('CE',(sp_bad2,'A6D_0',{sx:sp_x0,sp_xe:x,sp_r:1,sp_in:0,a6oe:off}),(net.and_(net.step(ptoc),net.eq(le_,plen_,e)),'T3_TD0',{rA:_ce_fill}),(net.step(pim),'A11_IM',{irow:0,iaddr:0,rA:_ce_fill}),(net.and_(net.eq(ls_,0,e),ONE-net.step(tcols)),'CB0',{rA:_ce_fill}),(None,'R9',{rA:_ce_fill}))
on('A11_IM',(None,'IM0',{rA:(x,sy,pim,pih,(255,255,255),1)}))   # the picture's ids; the rows then bring only color
on('CB0',(None,'CB1',{r1:pbs+CMTL}))
on('CB1',(net.step(R1),'T3_CB2',{wl_:R1,wb_:pbs+CMT,wdx:1052,wdy:sy+5,wdw:198,wdd:0,wbgf:0,wret_.r:wret_.id('T3_CB3')}),(None,'R9',None))
on('R9',(A4_R9(),'A4_D0',None),(None,'R5',{yy:yy+lhh,lj:lj+1}))
rA.drive(net.and_(S('R9'),a2_chg),(s_tx+xcol-12,sy,1,lhh,(64,64,64),0)); fsm.set(a2_chg,S('R9'),0)
e=S('RP')
ch_=net.step(net.step(yy-oend)+net.step(oend-yy)+0)
w1.drive(net.and_(e,ONE-a4hw),(pbs+ENDY,yy))
notlast=net.and_(net.step(tcols),net.lt(tci+1,tcols,e)); lastc_=net.and_(net.step(tcols),ONE-notlast)
newmax=net.max_(rowmax,yy+3)
adv_={bcnt:bcnt+bgm}
e=S('RP')
on('RP',(net.and_(ONE-full,ch_),'RD0',{lc:1}),
 (net.and_(ONE-full,net.step(lsf),ONE-net.step(tcols),net.lt(pi+1,npar,e)),'A2_LS0',None),
 (net.step(ONE-full+0),'R1',{yy:yy+pspa,pi:pi+1}),
 (notlast,'R1',{yy:rowtop,rowmax:newmax,pi:pi+1,**adv_}),
 (lastc_,'RB0',{rowmax:newmax,tiv:0,**adv_}),
 (net.and_(net.step(lsf),net.lt(pi+1,npar,e)),'A2_LS0',adv_),
 (None,'R1',{yy:yy+pspa,pi:pi+1,**adv_}))
BC=(0,0,0); by0=rowtop+DOCY-scroll
# line breaking network
net.group('line breaking')
ww=rw-a4rr-net.step(tcols)*12-indb-pind-pf_val(lfi)-net.step(ptoc)*44
def measure(c,ch,st,cell=None):
    g_en.lin(c);g_ch.add(c,ch);g_st.add(c,rom.lit(st) if isinstance(st,int) else st)
    if cell is not None: g_fl.add(c,cell)
e=S('LAY0')
on('LAY0',(net.step(pim),'EM',{lasc:0,lhh:pih,lend:0,lwid:pim,lspc:0,llast:1}),(net.eq(plen_,0,e),'LE0',None),(None,'L1',None))
e=S('LE0'); measure(e,32,ty)
on('LE0',(None,'EM',{lasc:asc,lhh:lh,lend:0,lwid:0,lspc:0,llast:1}))
fsm.set(kprev,S('LAY0'),0)
_rv_e=S('L1'); on('L1',(net.and_(net.step(off),net.ge(off,plen_,_rv_e)),'RVA3_LE0',None),(None,'L2',{r1:pbs+off,rs:pbs+1024+off}))
e=S('L2'); measure(e,R1,RSR,RSC); ke2=net.and_(e,net.step(kprev)); kp_en.lin(ke2); kp_in.add(ke2,kprev)
sp=net.eq(R1,32,e); _rv_tb=net.eq(R1,9,e); _rv_lt=rv_tabw(lx+indb+pind+pf_val(lfi),_rv_tb); _rv_vt=net.eq(R1,11,e); _rv_sb=net.or_(sp,_rv_tb); _ov=net.gt(lx+adv+kern+_rv_lt,ww,e); over=net.and_(_ov,ONE-sp,net.gt(off,ls_,_ov));   # a line always takes its first character, or a very narrow cell never ends
hasb=net.gt(lb,ls_,e); nsp=e-sp
lastc=net.ge(off+1,plen_,e); newword=net.and_(nsp,prevsp)
advance={kprev:R1,lx:lx+adv+kern+_rv_lt,lasc:net.max_(asc,lasc),lhh:net.max_(lh,lhh),off:off+1,prevsp:_rv_sb,wc:wc+newword,lsn:lsn+sp}
fsm.set(lb,net.and_(_rv_sb,ONE-over),off+1);fsm.set(lbx,net.and_(_rv_sb,ONE-over),lx+kern+_rv_lt);fsm.set(lspb,net.and_(_rv_sb,ONE-over),lsn)
isfl=net.ge(R1,1000,e); fsm.set(lfnb,net.and_(_rv_sb,ONE-over),lfn);fsm.set(lfhb,net.and_(_rv_sb,ONE-over),lfh)
on('L2',(net.eq(R1,9,e),'A4_LT0',{ra4t:pbs+A4T,lasc:net.max_(asc,lasc),lhh:net.max_(lh,lhh)}),(net.and_(net.ge(R1,300,e),ONE-isfl),'A6Q_L0',{a6qk:R1-300,r1:as_x(1330000)+(R1-300)*64+1,r2:as_x(1330000)+(R1-300)*64}),(isfl,'T3_LF0',{r1:as_x(FNB)+(R1-1000)*256+254}),(_rv_vt,'EM',{**advance,prevsp:ONE,lend:off+1,lwid:lx,lspc:lsn,llast:0}),(net.and_(over,hasb),'EM',{lend:lb,lwid:lbx,lspc:lspb,off:lb,llast:0,lfn:lfnb,lfh:lfhb}),
 (over,'EM',{lend:off,lwid:lx,lspc:lsn,llast:0}),
 (lastc,'EM',{**advance,lend:off+1,lwid:lx+adv+kern+_rv_lt,lspc:lsn,llast:1}),
 (None,'L2',{**advance,r1:pbs+off+1,rs:pbs+1024+off+1}))
e=S('EM'); delta=net.relu(ww-lwid); alh=net.decode(al,4,e)
just=net.and_(alh[3],ONE-llast,ONE-a4lt); sph=net.decode(lspc,64,just); ex=X()
deltaj=net.gate(delta,just)
for k_ in range(1,64): ex=ex+net.gate(deltaj*(1.0/k_),sph[k_])
x0=net.gate(delta*0.5,alh[1])+net.gate(delta,alh[2])+pind+pf_val(lfi)+48
# line spacing adds room above the text. The extra is a compiled table per spacing choice.
# Index 0 is the default of 1.08 lines, which the metrics already hold. Index 6 is true single spacing.
LSPF=[rom.LDEF,1.15,1.5,2.0,2.5,3.0,1.0]
ls_en=net.and_(e,net.step(plsp),ONE-net.step(pim)); lsh_=net.decode(plsp,7,ls_en); lxtra=X()
for i_ in range(1,7):
    k_=LSPF[i_]/rom.LDEF-1
    lxtra=lxtra+net.gate(lhh*abs(k_),lsh_[i_])*(1 if k_>0 else -1)
# Lines sit on whole pixels. The fraction left over goes to the next line of the paragraph, so a long paragraph keeps the true pitch.
lcar=R(); fsm.set(lcar,S('LAY0'),0.5); _lpx=lhh+lxtra+lcar-0.5; _lbit=net.bits(_lpx,12,e); lhint=sum((_lbit[i_]*(1<<i_) for i_ in range(12)),X())
fsm.set(lcar,e,_lpx-lhint+0.5)
wln.drive(e,(pbs+LINES+lj*8,ls_,lend,x0,lhint,lasc+lxtra,ex));w1.drive(e,(pbs+LINES+lj*8+6,lfb));w2.drive(e,(pbs+LINES+lj*8+7,lfh))
on('EM',(llast,'LF',{lj:lj+1}),(None,'L1',{lj:lj+1,ls_:off,lx:0,lb:off,lbx:0,lsn:0,lspb:0,lasc:0,lhh:0,lfi:0,kprev:0,lfb:lfn,lfh:0,lfnb:lfn,lfhb:0}))
_lf={w1:(pbs+NLINES,lj),w2:(pbs+DIRTY,0),w3:(pbs+WORDS,wc),wtot:wtot+wc-wdp,bcnt:bcnt+G_(plen_*0.01,bgm),a7_wb:a7_wb+plen_}
on('LF',(a4la,'A4_KL',_lf),(None,'R2X',_lf))
# ---- end of walk: autoscroll, caret, scrollbar, status bar ----
net.group('chrome')
e=S('RE0')
endw=net.and_(e,full,ONE-vm,ONE-bgp); fsm.set(dfrom,endw,99999); fsm.set(pagesT,endw,pages);fsm.set(wtot,endw,wsum);fsm.set(ytot,endw,ptop+s_ps);fsm.set(lc,e,0)
on('RE0',(net.and_(autos,net.lt(cy,scroll+40,e)),'RD0',{scroll:net.relu(cy-40),autos:0}),
 (net.and_(autos,net.gt(cy+chh,scroll+VH-40,e)),'RD0',{scroll:net.relu(cy+chh-VH+40),autos:0}),
 (net.gt(scroll,net.relu(ytot-VH+20),e),'RD0',{scroll:net.relu(ytot-VH+20)}),(None,'RE1',None))
e=S('RE1'); showc=net.and_(e,ONE-has_sel,ONE-blink,ONE-net.step(mode),ONE-a7_far)
rA.drive(showc,(cx,cy+DOCY-scroll,1,chh,(0,0,0),cacol))
fsm.set(dfrom,net.and_(S('RE1'),ONE-full,ONE-bgp),99999)
on('BGD',(None,'RD0',{bgp:0,bgm:0,dfrom:99999,pagesT:pages,wtot:wsum,ytot:ptop+s_ps,lc:0,a7_far:0,autos:a7_jmp,a7_jmp:0}))
on('RE1',(None,'RE2',{oldcp:cp,wassel:has_sel}))
e=S('RE2'); ph=net.decode(pagesT,128,e); th=X();ty_=X()
for k_ in range(1,128):
    th=th+ph[k_]*max(20,int((VH-8)/k_)); ty_=ty_+net.gate(scroll*((VH-8)/(k_*PST)),ph[k_])
on('RE2',(None,'RE3',{clip0:0,clip1:0,rA:(1262,DOCY,18,VH,(243,242,241),250),rB:(1265,ty_+DOCY+4,12,th,tuple(as_x(205)-net.step(t1_tdrag+net.eq(t1_hov,255,e))*65 for _ in range(3)),255),thumb:ty_+DOCY+4,t1_thh:th}))
on('RE3',(None,'STATUS',{rA:(0,DOCB+1,640,23,PAL_B[3],0)}))
# number and text drawing states
def text_chain(start,items,nxt,y=None,f=1,b=3):
    """items are strings or number registers; each glyph takes one tick."""
    cur=start
    for i,it in enumerate(items):
        if isinstance(it,str):
            for j,ch in enumerate(it):
                n=f'{start}_{i}_{j}'; e=S(cur)
                # advance x through the glyph network itself
                on(cur,(None,n,{gly:(ord(ch),9,sx,sb_y if y is None else y,f,b),sx:sx+adv}))
                cur=n
        else:
            for pw in (100000,10000,1000,100,10,1):
                n=f'{start}_{i}_p{pw}'; e=S(cur)
                base=net.gate(it,e); val=base
                for big in (100000,10000,1000,100,10):
                    if big>pw:
                        dd=X()
                        for t in range(1,10): dd=dd+net.step(val-big*t+0.5)
                        val=val-dd*big
                dg=X()
                for t in range(1,10): dg=dg+net.step(val-pw*t+0.5)
                show=e if pw==1 else net.step(base-pw+0.5)
                on(cur,(show,n,{gly:(48+dg,9,sx,sb_y if y is None else y,f,b),sx:sx+adv}),(None,n,None))
                cur=n
    on(cur,(None,nxt,None))
sb_y=as_x(DOCB+6)
on('STATUS',(None,'ST1',{sx:12}))
text_chain('ST1',['Page ',pcp,' of ',pagesT,'      ',wtot,' words      English (United States)'],'PM0')
on('PM0',(net.step(pfull),'PMf',None),(net.step(pmsg),'PMa',None),(None,'T4_ST',None))
on('PMf',(None,'PMg',{sx:sx+18}))
text_chain('PMg',['Too many different text formats: this one was not applied'],'T4_ST')
on('PMa',(None,'PMb',{sx:sx+18}))
text_chain('PMb',['Press Ctrl+V to paste from other apps'],'T4_ST')
# find bar
e=S('FB0')
fbx=R();fi_=R()
_a2s={rA:(PX+503,DOCY+3,1,22,(160,160,160),0),rB:(PX+740,DOCY+3,1,22,(160,160,160),0)}
on('FB6',(net.eq(field,1,S('FB6')),'T1_FZ',{**_a2s,rD:(sx,DOCY+6,1,16,(0,0,0),0)}),(None,'T1_FZ',_a2s))
on('FB0',(net.eq(mode,6,e),'T4_MB',None),(net.eq(mode,7,e),'TB0',None),(net.step(net.eq(mode,4,e)+net.eq(mode,5,e)),'A2_NB0',{rA:(PX,DOCY,816,28,PAL_B[3],0),rB:(PX,DOCY+27,816,1,(160,160,160),0),rC:(PX+84,DOCY+4,676,20,WHITE,0)}),(net.eq(mode,3,e),'A2_HB0',{rA:(PX,DOCY,816,28,PAL_B[3],0),rB:(PX,DOCY+27,816,1,(160,160,160),0),rC:(PX+84,DOCY+4,676,20,WHITE,0),fi_:0,sx:PX+88}),(net.step(mode),'FB1',{rA:(PX,DOCY,816,28,PAL_B[3],0),rB:(PX,DOCY+27,816,1,(160,160,160),0),rC:(PX+60,DOCY+4,300,20,WHITE,0)}),(None,'TB0',None))
on('HB',(net.ge(fi_,hlen,S('HB')),'A2_HBE',{rD:(sx,DOCY+6,1,16,(0,0,0),0)}),(None,'HB2',{r1:hfb+fi_}))
on('HB2',(None,'HB',{gly:(R1+net.eq(R1,1,S('HB2'))*34,0,sx,DOCY+4,0,0),sx:sx+adv,fi_:fi_+1}))
on('FB1',(None,'T1_FL',{rA:(PX+60,DOCY+3,324,1,(160,160,160),0),rB:(PX+60,DOCY+24,324,1,(160,160,160),0),rC:(PX+59,DOCY+3,1,22,(160,160,160),0)}))
on('FBL',(net.ge(fi_,qlen,S('FBL')),'FB3',None),(None,'FBR',{r1:as_x(Q)+fi_}))
on('FBR',(None,'FBL',{gly:(R1,0,sx,DOCY+4,0,0),sx:sx+adv,fi_:fi_+1}))
on('FB3',(net.eq(field,0,S('FB3')),'T1_FX0',{rD:(sx,DOCY+6,1,16,(0,0,0),0)}),(None,'T1_FX0',None))
on('FB4',(net.ge(fi_,rlen,S('FB4')),'FB6',None),(None,'FBS',{r1:as_x(RPL)+fi_}))
on('FBS',(None,'FB4',{gly:(R1,0,sx,DOCY+4,0,0),sx:sx+adv,fi_:fi_+1}))


# ribbon state: highlights and the current size and font, read from the typing style
fbr=R();fir=R();fur=R();fszv=R();ffn=R()
e=S('TB0'); measure(e,32,ty)
home_=net.eq(tab,0,e)
on('TB0',(net.eq(tab,0,e),'TB1',{fbr:net.relu(SD['bold']+0),fir:net.relu(SD['ital']+0),fur:net.relu(SD['und']+0),ffn:net.relu(SD['font']+0),fszv:G_(sum((h*p for h,p in zip(raw_hot,rom.SZ)),X()),ONE-net.eq(mode,7,e))+G_(td1*10+td0,net.eq(mode,7,e))}),(None,'T1_POST',None))
T1('biu')
on('TB6',(None,'TB6B',{rA:(113,65,110,20,(255,255,255),206)}))
e=S('TB6B'); tens_=sum((net.ge(fszv,10*q_,e) for q_ in range(1,10)),X())
on('TB6B',(None,'TB7',{gly:(48+tens_,9,sx,68,0,0),sx:sx+adv}))
e=S('TB7'); tens7=sum((net.ge(fszv,10*q_,e) for q_ in range(1,10)),X())
on('TB7',(None,'TBF0',{gly:(48+fszv-tens7*10,9,sx,68,0,0)}))
_FN=rom.FAM_NAMES; _FL=max(map(len,_FN))
on('TBF0',(None,'TBF1',{sx:117}))
for i in range(_FL):
    e=S(f'TBF{i+1}'); h_=net.decode(ffn,len(_FN),e); v_=X()
    for j,n_ in enumerate(_FN): v_=v_+h_[j]*ord((n_+' '*_FL)[i])
    on(f'TBF{i+1}',(None,f'TBF{i+2}' if i<_FL-1 else 'T1_POST',{gly:(v_,9,sx,68,0,0),sx:sx+adv}))
# ---- buttons ----
net.group('ribbon actions')
e=S('BTN'); B=net.decode(btn+net.and_(net.eq(tab,0,e),net.ge(btn,40,e),net.lt(btn,44,e))*20+net.and_(net.eq(tab,2,e),net.lt(btn,9,e))*63+net.and_(net.eq(tab,5,e),net.lt(btn,9,e))*71,80,e)
rules=[]
tabh=net.decode(tab,6,e)
def TB(i,t): return net.and_(net.step(B[i]),net.step(tabh[t]))
# Raw ids 35, 54 and 55 are global (find options, menu row, thumb), so these tabs use low raw ids
rules+=[(TB(3,1),'T4_FI',{t4k:1}),(TB(4,1),'T4_FI',{t4k:3}),(TB(5,1),'T4_FI',{t4k:2}),(TB(1,1),'T4_FU',{grp:grp+1}),(TB(2,1),'T4_EQ',{grp:grp+1}),(TB(2,4),'RD0',{sp_on:ONE-sp_on}),(TB(3,4),'RD0',{trk:ONE-trk}),(TB(4,4),'T4_AR',{arj:0,grp:grp+1}),(TB(1,4),'T4_AR',{arj:1,grp:grp+1}),(TB(1,3),'RD0',{mode:6}),]
for i in range(1,7): rules.append((B[i],'FMTS',{fm:i}))
for i in range(8): rules.append((B[7+i],'FMTS',{fm:7,fcol:i}))
rules+= [(B[15],'SETAL',{alv:0}),(B[16],'SETAL',{alv:1}),(B[17],'SETAL',{alv:2}),(B[18],'SETAL',{alv:3}),(B[19],'T2_LI',{alv:1}),(B[20],'T2_LI',{alv:2}),(B[63],'RD0',{mode:7,td0:0,td1:0})]
for i in range(4): rules.append((B[21+i],'T2_SA0',{t2si:i}))
rules+=[(B[25],'RD0',{mode:1,field:0}),(B[26],'UI',{bstg:1,t1_hov:0,clip0:0,clip1:0}),(B[27],'UNDO',None),(B[28],'REDO',None)]
for i in range(6): rules.append((B[29+i],'UI',{tab:i,clip0:0,clip1:0}))
rules+=[(B[36],'HALT',{wpaste:1}),(B[37],'COPY',None),(B[38],'CUT',None),(B[39],'RALL',None),(B[50],'SB',None)]
for i,n_ in enumerate((2,3,4)): rules.append((B[40+i],'TI0',{tin:n_,tic:0,tir:n_*n_-1,grp:grp+1}))
rules+=[(B[53],'PDF',None),(B[52],'HALT',{wpic:1}),(B[51],'T3_C_FN',None),(B[49],'RD0',{mode:4,field:0}),(B[48],'HALT',{wopen:1}),(B[47],'SAVE',None),(B[43],'T3_SP0',{tsop:6}),(B[44],'T3_SP0',{tsop:7}),(B[45],'TC0',{ti_:0,grp:grp+1}),(B[46],'T3_C_H0',None)]
T1('btn')
on('DA0',(net.ge(di_,npar,S('DA0')),'RD0',{lc:1,dfrom:0}),(None,'DA1',{r1:as_x(PT)+di_}))
on('DA1',(None,'DA0',{w1:(R1+DIRTY,1),di_:di_+1}))
# table of contents: copy headings into paragraphs at the caret
on('TC0',(None,'TC1',{r1:cb+LEN}))
e=S('TC1'); on('TC1',(net.ge(ti_,npar,e),'AFTER_ED',None),(None,'TC2',{r1:as_x(PT)+ti_}))
on('TC2',(None,'TC3',{tbase:R1,r1:R1+LEN,r2:R1+PSTY,rl:R1+SAVE}))
e=S('TC3'); ish=net.and_(net.step(R1),net.or_(net.eq(R2,2,e),net.eq(R2,3,e),net.eq(R2,4,e)))
tlev=R()
on('TC3',(ish,'TC4',{tl_:R1,tk_:0,tpg:rl.out[2],tlev:1+net.ge(R2,3,e)}),(None,'TC1',{ti_:ti_+1}))
e=S('TC4'); on('TC4',(net.ge(tk_,tl_,e),'T3_TC0x',{tk_:0}),(None,'TC5',{r1:tbase+tk_}))
on('TC5',(None,'INS',{ins_ch:R1,ins_st:0,tk_:tk_+1,oret.r:oret.id('TC4')}))
on('RALL',(None,'FN1',{fp:0,fo:0,wrap:0,rall:1,ap:0,ao:0,cp:0,co:0,grp:grp+1}))
on('SB',(net.lt(evb,thumb,S('SB')),'RD0',{scroll:net.relu(scroll-500),autos:0}),(None,'RD0',{scroll:scroll+500,autos:0}))
# ---- .docx writer: zip container, CRC32 and XML are all produced here ----
net.group('docx writer')
import zlib
fw=WPort(1); fw2=WPort(1); fp=R(); embase=R(SAVEB); em_en=Bus(net); em_b=Bus(net); savel=R(); crci=Bus(net)
fw.drive(em_en.w,(embase+fp,em_b.w))
fsm.set(fp,em_en.w,fp+1)
# CRC32 is linear over GF(2): each next bit is the parity of a fixed subset of bits.
def crc_next(c,b):
    return (zlib.crc32(bytes([b]),c^0xffffffff)^0xffffffff)&0xffffffff
a7_cen=Bus(net); a7_cby=Bus(net); ens=a7_cen.w; bb=net.bits(a7_cby.w,8,ens)
crcr=[R(1) for _ in range(32)]
gc=[net.gate(c_,ens) for c_ in crcr]
rows=[[] for _ in range(32)]
for i in range(32):
    o=crc_next(1<<i,0)
    for j in range(32):
        if o>>j&1: rows[j].append(gc[i])
for i in range(8):
    o=crc_next(0,1<<i)
    for j in range(32):
        if o>>j&1: rows[j].append(bb[i])
for j in range(32):
    sm=X(); 
    for t_ in rows[j]: sm=sm+t_
    par=X()
    for k_ in range(1,len(rows[j])+1): par=par+net.step(sm-k_+0.5)*(1 if k_%2 else -1)
    fsm.set(crcr[j],ens,par); fsm.set(crcr[j],crci.w,1)
def lit(name,data,nxt):
    "A token chain whose outgoing weights hold literal bytes."
    tok=S(name); fsm.states[name][1].append((tok,None))
    seq=[net.reg() for _ in range(len(data)+1)]; net.rec(seq[0],tok)
    for i,b_ in enumerate(data):
        em_en.lin(seq[i]); em_b.lin(seq[i]*b_); net.rec(seq[i+1],seq[i])
    net.rec(S(nxt),seq[-1])
exec(open('rv_a10_rom.py').read())
exec(open('rv_a10_num.py').read())
exec(open('t2_write.py').read())
exec(open('rv_a7_save.py').read())
saveout=Bus(net); saveout.add(S('HF'),savel); fsm.set(savel,S('HF'),0)
outbase=Bus(net); outbase.add(S('HF'),embase)
exec(open('t3_pre.py').read())
exec(open('pdf_write.py').read())
# ---- .docx reader: zip walk, inflate (canonical Huffman), LZ77 and XML matching ----
net.group('docx reader')
exec(open('docx_read.py').read())
exec(open('a12_guard.py').read())
exec(open('t4_features.py').read())
exec(open('t2_features.py').read())
exec(open('t3_features.py').read())
net.group('late commands')
exec(open('rv_a2_canvas.py').read())
exec(open('rv_a4_features.py').read())
exec(open('rv_a5_docx.py').read())
exec(open('rv_a6_spell.py').read())
# ---- ribbon commands: id plus tab select the command, first rule wins ----
_L0=[(PIND,-24,0),(PIND,24,0),(PFIRST,-24,1),(PFIRST,24,1),(PSPB,-8,0),(PSPB,8,0),(PSPA,-8,0),(PSPA,8,0)]
fr_=[(TB(8,0),'RD0',{mode:1,field:0}),(TB(9,0),'RD0',{mode:2,field:0}),(TB(10,0),'FMTS',{fm:12}),(TB(11,0),'FMTS',{fm:13}),(TB(12,0),'FMTS',{fm:14}),
 (TB(13,0),'T2_PD',{pfld:PIND,t2d:1000-24,t2mn:0}),(TB(14,0),'T2_PD',{pfld:PIND,t2d:1000+24,t2mn:0}),(TB(7,0),'FMTS',{fm:7,fcol:4}),(TB(44,0),'FMTS',{fm:15,fhl:1}),
 (TB(45,0),'T1_M0',{t1_mop:7,t1_mrow:99,t1_mtop:115,t1_mx:306,clip0:0,clip1:0}),(TB(46,0),'T1_M0',{t1_mop:8,t1_mrow:99,t1_mtop:115,clip0:0,clip1:0}),
 (TB(49,0),'T2_SA0',{t2si:4}),(TB(51,0),'T2_SA0',{t2si:5}),(TB(52,0),'T2_UM0',None)]
for i_,(fld,dv,mn) in enumerate(_L0): fr_.append((TB(16+i_,2),'T2_PD',{pfld:fld,t2d:1000+dv,t2mn:mn}))
for i_,id_ in enumerate((24,36,37,38,39,40)): fr_.append((TB(id_,2),'PA0',{pwalk:lo_p,pfld:PLSP,alv:i_ or 6,grp:grp+1}))
fr_.append((TB(15,2),'T3_C_SB',None))
fr_.insert(0,(net.and_(net.step(B[35]),net.lt(hy_,150,S('BTN'))),'A4_X',None))
for bt_ in t3_btn.BTNS: fr_.append((TB(bt_[1],bt_[0]),bt_[7],None))
on('BTN',*fr_,*rules,(None,'HALT',None))
# ---- File screen ----
on('BS_MD',(None,'BS_M1',{pix:(hx_,hy_)}))
e=S('BS_M1')
on('BS_M1',(net.eq(A_,201,e),'UI',{bstg:0,clip0:0,clip1:0}),(net.or_(net.eq(A_,202,e),net.eq(A_,206,e)),'SELALL',{bsn:1}),(net.eq(A_,203,e),'HALT',{wopen:1,bsq:1}),(net.eq(A_,204,e),'SAVE',{bsq:1}),(net.eq(A_,205,e),'PDF',{bsq:1}),(None,'HALT',None))
# ---- internal clipboard: the network's own copy feeds paste when the system clipboard can't ----
# The two buffers overlap when the copy is long, so the blocks move from the top down.
clik=R(); CLIMAX=390000; _clk=net.min_(cli,1000)
e=S('CLI0'); on('CLI0',(net.eq(cli,0,e),'PASTE',{evc:net.min_(clipn,CLIMAX)}),(None,'CLI1',{rb:(as_x(CB)+cli-_clk,_clk),clik:_clk}))
on('CLI1',(None,'CLI0',{wb:(as_x(CB2)+cli-clik,clik),cli:cli-clik}))
# ---- ribbon drawn by a chain of tokens; each token's outgoing weights hold one draw item ----
net.group('ribbon display list')
import ui
exec(open('rv_a3_keys.py').read())
T1('late')
a4_late()
rv_a4_btn.FP=a4fp
ui.build(net,fsm,rA,g_en,g_ch,g_st,g_x,g_y,g_draw,fg,bg,YB,tab,S,t1_hov,t1_hb,t1_hvo,bstg,t1_prs)
exec(open('pointer3.py').read())
exec(open('rv_a11_out.py').read())
net.group('ribbon display list')
# ---- finish ----
pat_finish()
for r in (a7r,a7sr,a7cr,jret,oret,dret,wret,bret,gret,hret,cret,iret,nrr,frr,t4r,fvr,t4cr,zret,zdr,pfr,pfcr,t2pr,t2rr,t2pp,t2sr,t2ur,pgret,wret_,lret,lbret)+tuple(T3_RETS): r.gen()
_undef={nx_ for _,(r_,o_) in fsm.states.items() for _c,nx_ in o_ if nx_ is not None and nx_ not in fsm.states}
assert not _undef,_undef
_dead=[k_ for k_,(r_,o_) in fsm.states.items() if not o_]
assert not _dead,_dead
fsm.finish()
def nid(x):
    if isinstance(x,X): return next(iter(x.t))
    return x
wvl_data=[wlog,wln,wvl,w1,w2,w3,w4,fw,fw2,wo,imw,wl_i,xw,wht]+T3_WPORTS
for p in wvl_data: net.aligned.append([nid(b.w) for b in p.d])
net.keep=[nid(q) for q in (dsave.w,halt.w,timer.w,clipout.w,saveout.w,outbase.w,pdfout.w,picout.w,openout.w,wantp.w,ev_kind,ev_a,ev_b,ev_c,ev_t,ev_m)]
net.keep+=[nid(q) for q in (a11bad,*kv,kvl,c_pass.w,c_ff.w,c_fb.w,c_hold.w,c_chold.w,c_kbo.w,c_file.w,c_namea.w,c_namen.w)]
for p in net.ports:
    for q in p.rec(None)[1:]:
        if isinstance(q,X): net.keep.append(nid(q))
        elif isinstance(q,int): pass
    if isinstance(p,PatchPort): net.keep+=[nid(q) for q in p.a[:3]]
    if isinstance(p,CallPort):
        net.keep.append(nid(p.en)); net.keep.append(nid(p.done)); net.keep+=[nid(q) for q,_d in p.args]
    if isinstance(p,(RPort,PixPort)): net.keep+=[nid(q) for q in p.out]
import rv_a8_opt; _a8rep=rv_a8_opt.prune(net,[p.rec(None) for p in net.ports],[next(iter(v_.t)) for v_ in list(globals().values()) if isinstance(v_,X) and len(v_.t)==1])
c=net.compile(); new=c['new']
import os
if os.environ.get('NETDBG'): json.dump(dict(new=new,act=c['act'],bias=c['bias'],lazy=c['lazy'],out=c['out'],pull=net.pullv,line=getattr(net,'line',{})),open('../build/netdbg.json','w'))
gn_=[''] *c['n']
for g_,ids_ in net.groups.items():
    for i_ in ids_:
        if new[i_]>=0: gn_[new[i_]]=g_
json.dump(gn_,open('../build/ngroups.json','w'))
print('neurons',c['n'],'layers',c['L'],file=sys.stderr)
names={new[next(iter(v_.t))]:k_ for k_,v_ in list(globals().items()) if isinstance(v_,X) and len(v_.t)==1 and new[next(iter(v_.t))]>=0}
print('named regs in AND inputs',sorted(names[new[j]] for j in net.bool_regs_seen if new[j] in names),file=sys.stderr)
json.dump(names,open('../build/names.json','w'))
json.dump({str(new[next(iter(r_.t))]):k_ for k_,(r_,_) in fsm.states.items() if new[next(iter(r_.t))]>=0},open('../build/states.json','w'))
pr=[]
_ports=[p for p in net.ports if not getattr(p,'dom',0)]+[None]+[p for p in net.ports if getattr(p,'dom',0)]
for p in _ports:
    if p is None: pr+=[9]; continue
    r=p.rec(None)
    if r[0]==8: pr+=[8,new[nid(r[1])],new[nid(r[2])],len(r[3]),len(r[4])]+[new[nid(q)] for a_ in list(r[3])+list(r[4]) for q in a_]
    elif r[0]==10: pr+=[10,new[nid(r[1])],new[nid(r[2])],new[nid(r[3])]]+list(r[4:])
    elif r[0] in (1,2):
        d=r[3]
        pr+=[r[0],new[nid(r[1])],new[nid(r[2])],new[nid(d)],r[4],new[nid(r[5])] if r[5] is not None else -1]
    elif r[0]==3: pr+=[3]+[new[nid(q)] for q in r[1:]]
    elif r[0] in (4,11): pr+=[r[0],new[nid(r[1])],new[nid(r[2])],new[nid(r[3])],new[nid(r[4][0])],r[5],r[6],new[nid(r[7])],new[nid(r[8])]]
    elif r[0] in (5,6): pr+=[r[0]]+[new[nid(q)] for q in r[1:]]
import numpy as np
n=c['n']
def _var(vals):
    o=bytearray()
    for x_ in vals:
        while x_>=128: o.append((x_&127)|128); x_>>=7
        o.append(x_)
    return bytes(o)
_zz=lambda x_:(x_<<1) if x_>=0 else ((-x_)<<1)-1
ww_=[];iww=[]
for i in range(n):
    c['out'][i]=sorted(c['out'][i]); ww_+=[w_ for _d,w_ in c['out'][i]]; iww+=[w_ for _j,w_ in c['lazy'][i]]
import collections
_wc=collections.Counter(ww_)+collections.Counter(iww)
wtab=sorted(_wc,key=lambda w_:(-_wc[w_],w_)); wix={w_:k_ for k_,w_ in enumerate(wtab)}; assert len(wtab)<65536,len(wtab)
_bc=collections.Counter(c['bias']); btab=sorted(_bc,key=lambda w_:(-_bc[w_],w_)); bix={w_:k_ for k_,w_ in enumerate(btab)}
_i0,_i1,_i2,_i3=[],[],[],[]; _ipv=[0,0,0,0]; _d1,_d2=[],[]; _pf=0
for i in range(n):
    for k_,(j_,w_) in enumerate(c['lazy'][i]):
        q_=min(k_,3); s_=~j_ if j_<0 else j_; (_i0,_i1,_i2,_i3)[q_].append(_zz(s_-_ipv[q_])*2+(1 if j_<0 else 0)); _ipv[q_]=s_
    prev_=None
    for d_,w_ in c['out'][i]:
        if prev_ is None: _d1.append(_zz(d_-_pf)); _pf=d_
        else: _d2.append(d_-prev_)
        prev_=d_
_streams=[_var(len(c['lazy'][i]) for i in range(n)),_var(len(c['out'][i]) for i in range(n)),bytes(c['act']),_var(bix[w_] for w_ in c['bias']),_var(_i0),_var(_i1),_var(_i2),_var(_i3),_var(wix[w_] for w_ in iww),_var(_d1),_var(_d2),_var(wix[w_] for w_ in ww_)]
_zb=struct.pack('<12I',*[len(z_) for z_ in _streams])+b''.join(_streams)
hdr=dict(dsave=new[nid(dsave.w)],dict=DICTB,fmax=TAGB-FILE,outbase=new[nid(outbase.w)],zn=len(_zb),nb=len(btab),pdfout=new[nid(pdfout.w)],ni=len(iww),nt=len(wtab),wpic=new[nid(picout.w)],wopen=new[nid(openout.w)],file=FILE,saveout=new[nid(saveout.w)],n=n,e=len(ww_),L=c['L'],nports=len(pr),bank=BANK,halt=new[nid(halt.w)],timer=new[nid(timer.w)],clipout=new[nid(clipout.w)],wantp=new[nid(wantp.w)],
 ev=[new[nid(q)] for q in (ev_kind,ev_a,ev_b,ev_c,ev_t,ev_m)],cb=CB,cb2=CB2,n1=c['n1'],init=[[new[i],v] for i,v in net.init.items() if not net.dom[i]],init1=[[new[i],v] for i,v in net.init.items() if net.dom[i]],
 bank_init=[*[[SECB+i_,v_] for i_,v_ in enumerate((1,816,PH,PX,TX,TW,96,864))],[LEN+SLOT0,0],[DIRTY+SLOT0,1],[PT,SLOT0],[SLOT0+SAVE,112],[SLOT0+SAVE+1,16],[SLOT0+SAVE+2,1],[SLOT0+PSPA,DEFSPA]]+T2_ROM+PF_INIT)
hdr.update(keyv=[new[nid(q)] for q in kv],keyl=new[nid(kvl)],pass_=new[nid(c_pass.w)],ffield=new[nid(c_ff.w)],fback=new[nid(c_fb.w)],hold=new[nid(c_hold.w)],chold=new[nid(c_chold.w)],kbo=new[nid(c_kbo.w)],fileout=new[nid(c_file.w)],namea=new[nid(c_namea.w)],namen=new[nid(c_namen.w)],kbv=KBV,kbq=KBQ,screenbad=new[nid(a11bad)],kbmax=KBMAX,cb2max=390000)
hdr['bank_init']+=[[KBL+i_,126] for i_ in range(KBSEN)]+[[KBQ+i_,126] for i_ in range(KBSEN)]+[[NAMEB+i_,ord(c_)] for i_,c_ in enumerate(NAME_DOCX+NAME_PDF)]
import os
raw=b''.join([_zb,np.array(c['lstart'],dtype=np.int32).tobytes(),np.array(pr,dtype=np.int32).tobytes(),np.array(wtab,dtype=np.float64).tobytes(),np.array(btab,dtype=np.float64).tobytes()])
ROM_RUNS.append([DLROM,b''.join(int(v_).to_bytes(3,'little') for v_ in a9_rom),3])
raw+=rom_finish(hdr)
h=json.dumps(hdr,separators=(',',':')).encode()
blob=struct.pack('<I',len(h))+h+b'\0'*((4-(len(h)+4)%4)%4)+raw
gz=gzip.compress(blob,9)
if os.environ.get('NETSTAT'):
    import rv_a8_fmt; _a8b,_=rv_a8_fmt.encode(c,pr); print('a8 encoder gz',len(gzip.compress(_a8b,9)),'fonts encoder gz',len(gzip.compress(raw[:len(raw)-sum(len(d) for a,d,w in [[0,bytes(PF_ROM),1],[0,bytes(_litb),1]]+ROM_RUNS)],9)),file=sys.stderr)
    print({k_:(len(v_),len(gzip.compress(v_,6))) for k_,v_ in zip('ist ost act bias i0 i1 i2 i3 iw d1 d2 wz'.split(),_streams)},'wtab',len(wtab),'btab',len(btab),'hdr',len(h),file=sys.stderr)
exec(open('a12_dbg.py').read())
open('../build/net.bin.gz','wb').write(gz)
exec(open('rv_a11_prov.py').read())
print('lazy',len(iww),'edges',len(ww_),'raw',len(blob),'gz',len(gz),file=sys.stderr)
_mx=max((v_[1]-v_[0])*96+5 for v_ in glyph_unit.ext.values()); _my=max((v_[3]-v_[2])*96+3 for v_ in glyph_unit.ext.values())
print('glyph unit',glyph_unit.stats,'slots',glyph_unit.nup,glyph_unit.ndn,glyph_unit.nua,glyph_unit.nda,'bank',glyph_unit.nbank,'widest px',round(_mx),'tallest px',round(_my),'of',GLW,file=sys.stderr)
