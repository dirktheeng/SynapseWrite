"""Writes the application network. Python here only computes weights at build time."""
import json,struct,gzip,sys,time
from nn import *
import rom
net=Net(); fsm=FSM(net); on=fsm.on; ONE=net.ONE; G_=net.gate
# ---- memory map (one passive tensor store) ----
PT=0; VL=20000; Q=21000; RPL=21200; HD=21400; UB=14500000; UEND_=19999000; CB=1400000; SLOT0=2000000; STRIDE=4096; BANK=32000000; IMG0=24000000; OUTB=20000000; TBL=30000; SLOTMAX=14400000
LEN,DIRTY,ALIGN,LIST,NLINES,WORDS,ENDY,PBRK=2048,2049,2050,2051,2052,2053,2054,2055; SAVE=2056; LINES=2064; IMF=3670; CMTL=3699; CMT=3700; FNS=3690; FNL=3692; FNT=3900
# ---- screen geometry ----
DOCY,DOCB=174,776; VH=DOCB-DOCY; PX=223; TX=319; TW=624; PH=1056; PST=1072; YB=4096
PAL_F=[(0,0,0),(89,89,89),(255,255,255),(43,87,154),(192,0,0),(0,128,60),(230,120,0),(112,48,160)]
PAL_B=[(255,255,255),(197,217,241),(255,242,171),(243,243,243),(43,87,154)]
# ---- ports ----
class RPort:
    def __init__(s,cells,varlen=False):
        s.en=Bus(net);s.addr=Bus(net);s.cells=cells;s.out=net.input(cells) if cells>1 else [net.input()]
        s.len=Bus(net) if varlen else None; net.ports.append(s)
    def drive(s,c,v):
        a,n=v if s.len else (v,None)
        s.en.lin(c); s.addr.add(c,a)
        if s.len: s.len.add(c,n)
    def rec(s,nm): return [2,s.en.w,s.addr.w,s.out[0],s.cells,s.len.w if s.len else None]
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
class ImgPort:
    def __init__(s):
        s.b=[Bus(net) for _ in range(5)]; net.ports.append(s)
    def drive(s,c,v):
        s.b[0].lin(c)
        for b,e in zip(s.b[1:],(v[0],as_x(v[1])+YB,v[2],v[3])): b.add(c,e)
    def rec(s,nm): return [6]+[b.w for b in s.b]+[clip0,clip1]
class PixPort:
    def __init__(s):
        s.en=Bus(net);s.xy=Bus(net);s.out=net.input(4); net.ports.append(s)
    def drive(s,c,v): s.en.lin(c); s.xy.add(c,as_x(v[0])+as_x(v[1])*65536)
    def rec(s,nm): return [5,s.en.w,s.xy.w,s.out[0]]
class PatchPort:
    def __init__(s,en,x,y,data,w,h): s.a=(en,x,y,data,w,h); net.ports.append(s)
    def rec(s,nm): e,x,y,d,w,h=s.a; return [4,e,x,y,d,w,h,clip0,clip1]
clip0=net.reg(); clip1=net.reg()
rb=RPort(1100,True); wb=WPort(1100,rb.out[0],True)   # block copy through 1100 neurons
rc=RPort(2); rf=RPort(3); r1=RPort(1); r2=RPort(1); rl=RPort(8); rlog=RPort(6)
w1=WPort(1);w2=WPort(1);w3=WPort(1);w4=WPort(1);wlog=WPort(6);wvl=WPort(6);wln=WPort(6)
imr=ImgPort();rim=RPort(3);rU=RPort(1);rV=RPort(1);rA=RectPort();rB=RectPort();rC=RectPort();pix=PixPort()
R1=r1.out[0];R2=r2.out[0]
ev_kind,ev_a,ev_b,ev_c=net.input(4)
halt=Bus(net); timer=Bus(net); clipout=Bus(net)
# ---- glyph network ----
net.group('glyph network')
g_en=Bus(net);g_ch=Bus(net);g_st=Bus(net);g_x=Bus(net);g_y=Bus(net);g_draw=Bus(net)
fg=[Bus(net) for _ in PAL_F]; bg=[Bus(net) for _ in PAL_B]
GE=g_en.w
def style_decode(val,en):
    b=net.bits(val,11,en); return dict(size=b[0]+b[1]*2+b[2]*4+b[3]*8,sb=b[:4],bold=b[4],ital=b[5],und=b[6],font=b[7],colbits=b[8:],color=b[8]+b[9]*2+b[10]*4)
SD=style_decode(g_st.w,GE)
# Glyph addressing is a decision tree: each node is enabled by its parent and reads its
# selector lazily, so a lookup visits a path through the tree and not all of the table.
def tnode(parent,sel,neg=False):
    return net.step(parent*M-M+((ONE-sel) if neg else sel)-0.5)
def tsplit(parent,sel): return tnode(parent,sel,True),tnode(parent,sel)
def _tree(parent,sels):
    if not sels: return [parent]
    l0,l1=tsplit(parent,sels[-1])
    return _tree(l0,sels[:-1])+_tree(l1,sels[:-1])
_leaf=_tree(GE,SD['sb'])
size_hot=_leaf[:10]+[sum(_leaf[10:],X())]
# character index: base 16 digits by two thermometers, one hot digits read lazily
_chv=net.relu(g_ch.w-32+1+GE*M-M)
_ht=[net.step(_chv-16*k_-0.5) for k_ in range(1,6)]
_base=net.step(_chv)
chr_hi=[net.step(_base-_ht[0]-0.5)]+[net.step(_ht[k_]-(_ht[k_+1] if k_<4 else X())-0.5) for k_ in range(5)]
_rem=_chv-sum((t_*16 for t_ in _ht),X())
_lt=[_base]+[net.step(_rem-j_-0.5) for j_ in range(1,16)]
chr_lo=[net.step(_lt[j_]-(_lt[j_+1] if j_<15 else X())-0.5) for j_ in range(16)]
adv=net.wire();asc=net.wire();lh=net.wire();small=net.wire()
for si,h in enumerate(size_hot):
    a,l=rom.metrics(si); net.connect(asc,h*a); net.connect(lh,h*l)
    if rom.small(si): net.connect(small,h)
SW,SH,LW,LH=rom.SW,rom.SH,rom.LW,rom.LH
fastw=net.and_(g_draw.w,small,fg[0].w,bg[0].w)
fastsel=net.and_(g_draw.w,small,fg[0].w,bg[1].w)
net.group('glyph patch')
GLY={}; _used=[set(),set()]
for fi in range(2):
  for bo in range(2):
    for it in range(2):
      for si in range(11):
        for ci in range(96):
            a_,pts=rom.glyph(fi,bo,it,si,32+ci); GLY[fi,bo,it,si,ci]=(a_,pts)
            _used[rom.small(si)].update((x_,y_) for x_,y_,_q in pts)
def plane(w,h,used,fastsel_):
    """One coverage layer per patch. An ink pixel enables its colour neurons, which read the
    selected colour lazily. Black on white needs no colour neurons at all. Pixels no glyph
    ever covers have no neurons except the output cells the patch port reads."""
    cov={};data=[net.wire() for _ in range(4*w*h)]
    nonw=ONE-fastw
    for y_ in range(h):
      for x_ in range(w):
        if (x_,y_) not in used: continue
        i=y_*w+x_; c=net.wire(); cov[i]=c; m=net.step(c)
        o=[(m-c)*255]*3
        nw=net.step(m*M-M+nonw-0.5)
        slow=nw
        if fastsel_:
            sl=net.step(nw*M-M+fastsel-0.5); slow=net.step(nw*M-M+(ONE-fastsel)-0.5)
            cs=net.relu(sl*M-M+m-c)
            for k in range(3): o[k]=o[k]+cs*(PAL_B[1][k]-255)
        ic=net.relu(slow*M-M+m-c)
        for k in range(3): o[k]=o[k]-ic*255
        for j,col in enumerate(PAL_F):
            g=net.relu(slow*M-M+c+fg[j].w-1)
            for k in range(3):
                if col[k]: o[k]=o[k]+g*col[k]
        for j,col in enumerate(PAL_B):
            g=net.relu(slow*M-M+m-c+bg[j].w-1)
            for k in range(3):
                if col[k]: o[k]=o[k]+g*col[k]
        for k in range(3): net.connect(data[4*i+k],o[k])
        net.connect(data[4*i+3],m)
    return cov,data
cov_s,dat_s=plane(SW,SH,_used[1],True); cov_l,dat_l=plane(LW,LH,_used[0],False)
on_s=net.and_(g_draw.w,small); on_l=net.and_(g_draw.w,ONE-small)
net.group('glyph weights (font outlines)')
t0=time.time()
for si in range(11):
  sh_=size_hot[si]
  f0,f1=tsplit(sh_,SD['font'])
  for fi,fn_ in enumerate((f0,f1)):
    b0,b1=tsplit(fn_,SD['bold'])
    for bo,bn_ in enumerate((b0,b1)):
      i0,i1=tsplit(bn_,SD['ital'])
      for it,fh in enumerate((i0,i1)):
        for hi_ in range(6):
          Fh=net.step(fh*M-M+chr_hi[hi_]-0.5)
          for lo_ in range(16):
            a,pts=GLY[fi,bo,it,si,hi_*16+lo_]
            if not a and not pts: continue
            G=net.step(Fh*M-M+chr_lo[lo_]-0.5)
            if a: net.connect(adv,G*a)
            if pts:
                Gd=net.step(G*M-M+g_draw.w-0.5); cv=cov_s if rom.small(si) else cov_l; w_=SW if rom.small(si) else LW
                for x_,y_,q in pts: net.connect(cv[y_*w_+x_],Gd*(q/15.0))
print('glyph weights',time.time()-t0,'s',file=sys.stderr)
class GlyPort:
    def drive(s,c,v):
        ch,st,x,y,f,b=v; g_en.lin(c); g_ch.add(c,ch); g_st.add(c,st); g_x.add(c,x); g_y.add(c,as_x(y)+YB); g_draw.lin(c)
        fg[f].lin(c) if isinstance(f,int) else None; bg[b].lin(c) if isinstance(b,int) else None
gly=GlyPort()
gx=g_x.w-2; gy=g_y.w
for en,d,w,h in ((on_s,dat_s,SW,SH),(on_l,dat_l,LW,LH)):
    px_=net.wire();py_=net.wire();net.connect(px_,net.gate(gx+2,en)-en*2);net.connect(py_,net.gate(gy,en))
    # neurons in a patch are consecutive after compile by port remap
    PatchPort(net.step(en),px_,py_,d,w,h)
net.group('core')
# ---- control registers ----
R=net.reg
cp=R();cb=R(SLOT0);co=R();clen=R();ap=R();ao=R();scroll=R();npar=R(1);nextb=R(SLOT0+STRIDE);ty=R();tab=R()
drag=R();usp=R(UB);urp=R(UB);grp=R(1);nolog=R();blink=R();autos=R();mode=R();qlen=R();rlen=R();field=R()
evk=R();eva=R();evb=R();evc=R();shiftk=R()
hx_=R();hy_=R();fm=R();alv=R();jp=R();jo=R();hdir=R();hact=R();btn=R();hcol=R();vi=R();clipr=R()
clipl=R();wpaste=R();full=R(1);fastok=R();oldcp=R();wassel=R();bgp=R();bgm=R();bcnt=R();dfrom=R();bpi=R();byy=R();bptop=R();bpg=R(1);bws=R();bln=R();tcols=R();tci=R();rw=R(624);rx0=R();rleft=R(223);rright=R(1039);rowtop=R();rowmax=R();tiv=R();tin=R();tic=R();tip=R();tir=R();sx=R();ncol=R();xcol=R();bxc=R();hlen=R();hdi=R();di_=R();ti_=R();tk_=R();tbase=R();tl_=R();tpg=R();tdig=R();tivx=R();fnn=R();fnp=R();bfn=R();bfp=R();pfn=R();fni=R();pim=R();pih=R();pio=R();irow=R();iaddr=R();wpic=R();imgp=R();ci_=R();cl_=R();wopen=R();lc=R(1);vm=R();pagesT=R(1);wtot=R();ytot=R(112);oend=R();sidx=R()
pi=R();pbs=R();yy=R();ptop=R();pages=R();wsum=R();vln=R();listn=R();lj=R();nl=R();al=R();lsf=R();plen_=R();wdp=R()
# dispatch tables for subroutine returns
class Ret:
    def __init__(s,name): s.r=R(); s.t=[]; s.name=name
    def id(s,st):
        if st not in s.t: s.t.append(st)
        return s.t.index(st)+1
    def gen(s):
        en=fsm.S(s.name); h=net.decode(s.r,len(s.t)+1,en)
        on(s.name,*[(h[i+1],st,None) for i,st in enumerate(s.t)],(None,'HALT',None))
jret=Ret('JR');oret=Ret('OR');dret=Ret('DR');wret=Ret('WR')
S=fsm.S
Kc=cp*2048+co;Ka=ap*2048+ao
Hi=net.max_(Kc,Ka);Lo=net.min_(Kc,Ka);has_sel=net.step(Hi-Lo)
lo_a=net.step(Kc-Ka)     # anchor is the low end
lo_p=G_(ap,lo_a)+G_(cp,ONE-lo_a);lo_o=G_(ao,lo_a)+G_(co,ONE-lo_a)
hi_p=G_(cp,lo_a)+G_(ap,ONE-lo_a);hi_o=G_(co,lo_a)+G_(ao,ONE-lo_a)
at_a=ONE-has_sel
# ---- event dispatch ----
net.group('event dispatch')
on('IDLE',(net.step(ev_kind),'DISP',{evk:ev_kind,eva:ev_a,evb:ev_b,evc:ev_c}))
fsm.states['IDLE'][0]; net.init[next(iter(S('IDLE').t))]=1.0
kh=net.decode(evk,11,S('DISP'))
on('DISP',(kh[1],'UI',{clip0:0,clip1:0}),(kh[2],'KEY',{shiftk:net.bits(evb,2,S('DISP'))[1]}),(kh[3],'MD',{hx_:eva,hy_:evb}),
   (kh[4],'IDL2',{drag:0}),(kh[5],'MV',None),(kh[6],'WH',None),(kh[7],'TM',{blink:ONE-blink,autos:0}),(kh[8],'PASTE',{}),(kh[9],'OP0',{}),(kh[10],'PG_0',{}),(None,'HALT',None))
on('IDL2',(None,'HALT',None))
on('MV',(net.and_(S('MV'),drag),'MD2',{hx_:eva,hy_:evb,shiftk:1}),(None,'HALT',None))
on('WH',(None,'RD0',{scroll:net.relu(scroll+evc-1000),autos:0}))   # ev_c carries delta+1000
on('TM',(bgp,'BG',{blink:blink}),(None,'RD0',{fastok:1}))
on('BG',(None,'R1',{fnn:bfn,fnp:bfp,xcol:bxc,pi:bpi,yy:byy,ptop:bptop,pages:bpg,wsum:bws,listn:bln,full:1,vm:0,bgm:1,bcnt:0,clip0:DOCY,clip1:DOCB}))
on('HALT',(None,'IDLE',None)); halt.lin(S('HALT'))
timer.lin(S('HALT')*530-net.and_(S('HALT'),bgp)*529)
# ---- key handling ----
net.group('key handling')
en=S('KEY'); k=net.decode(eva,136,en); kb=net.bits(evb,2,en); ctrl=kb[0]; shf=kb[1]; nc=ONE-ctrl
def K(c): return net.and_(k[ord(c) if isinstance(c,str) else c],ctrl)
def N(c): return net.and_(k[c],nc)
printable=X()
for c in range(32,127): printable=printable+k[c]
findon=net.step(mode)
A_KEEP=net.and_(en,shf)
on('KEY',
 (net.and_(net.eq(mode,5,en),net.or_(N(27),N(13))),'FNE',{mode:0}),(net.and_(net.eq(mode,5,en),N(8)),'FNc',None),(net.and_(net.eq(mode,4,en),net.or_(N(27),N(13))),'RD0',{mode:0}),(net.and_(net.eq(mode,4,en),N(8)),'CMc',None),(net.and_(net.eq(mode,3,en),net.or_(N(27),N(13))),'RD0',{mode:0}),(net.and_(net.eq(mode,3,en),N(8)),'RD0',{hlen:net.relu(hlen-1)}),(net.and_(findon,N(27)),'RD0',{mode:0}),
 (net.and_(findon,N(9)),'RD0',{field:ONE-field}),
 (net.and_(findon,N(13)),'FIND',{}),
 (net.and_(findon,N(8)),'RD0',{qlen:G_(net.relu(qlen-1),ONE-field)+G_(qlen,field),rlen:G_(net.relu(rlen-1),field)+G_(rlen,ONE-field)}),
 (net.and_(findon,net.and_(printable,nc)),'FTYPE',{}),
 (N(128),'MOVL',{}),(N(130),'MOVR',{}),(N(129),'MOVU',{}),(N(131),'MOVD',{}),(N(132),'MOVH',{}),(N(133),'MOVE',{}),
 (N(134),'RD0',{scroll:net.relu(scroll-500),autos:0}),(N(135),'RD0',{scroll:scroll+500,autos:0}),
 (K('p'),'PDF',{}),(K('s'),'SAVE',{}),(K('o'),'HALT',{wopen:1}),(K('z'),'UNDO',{}),(K('y'),'REDO',{}),(K('a'),'SELALL',{}),(K('c'),'COPY',{}),(K('x'),'CUT',{}),
 (K('b'),'FMTS',{fm:1}),(K('i'),'FMTS',{fm:2}),(K('u'),'FMTS',{fm:3}),
 (K('e'),'SETAL',{alv:1}),(K('l'),'SETAL',{alv:0}),(K('r'),'SETAL',{alv:2}),(K('j'),'SETAL',{alv:3}),
 (K('f'),'RD0',{mode:1,field:0}),(K('h'),'RD0',{mode:2,field:0}),
 (K(13),'PB0',{grp:grp+1}),(N(8),'BKSP',{grp:grp+1}),(N(127),'DELK',{grp:grp+1}),(N(13),'ENTER',{grp:grp+1}),(N(9),'TABK',{}),
 (net.and_(printable,nc),'TYPE',{}),
 (None,'HALT',None))
# find field typing
on('CMc',(None,'CMd',{r1:cb+CMTL}))
on('CMd',(None,'RD0',{w1:(cb+CMTL,net.relu(R1-1))}))
on('CMa',(None,'CMb',{r1:cb+CMTL}))
on('CMb',(net.ge(R1,380,S('CMb')),'RD0',None),(None,'RD0',{w1:(cb+CMT+R1,eva),w2:(cb+CMTL,R1+1)}))
on('FNE',(None,'RD0',{lc:1,dfrom:0,w1:(cb+DIRTY,1)}))
on('FNc',(None,'FNd',{r1:cb+FNL}))
on('FNd',(None,'RD0',{w1:(cb+FNL,net.relu(R1-1)),lc:1,dfrom:net.relu(cp-1)}))
on('FNa',(None,'FNb',{r1:cb+FNL}))
on('FNb',(net.ge(R1,180,S('FNb')),'RD0',None),(None,'RD0',{w1:(cb+FNT+R1,eva),w2:(cb+FNL,R1+1),lc:1,dfrom:net.relu(cp-1)}))
on('FTYPE',(net.eq(mode,5,S('FTYPE')),'FNa',None),(net.eq(mode,4,S('FTYPE')),'CMa',None),(net.eq(mode,3,S('FTYPE')),'RD0',{w1:(as_x(HD)+hlen,eva),hlen:hlen+1}),(field,'RD0',{w1:(as_x(RPL)+rlen,eva),rlen:rlen+1}),(None,'RD0',{w1:(as_x(Q)+qlen,eva),qlen:qlen+1}))
ins_ch=R();ins_st=R()
cont_ty=S('TYPE')
on('TYPE',(net.and_(has_sel,cont_ty),'DS0',{dret.r:dret.id('TY2'),grp:grp+1}),(None,'TY2',{grp:grp+net.step(net.eq(eva,32,S('TYPE')))}))
on('TY2',(net.ge(clen,1000,S('TY2')),'RD0',None),(None,'INS',{ins_ch:eva,ins_st:ty,oret.r:oret.id('AF_FAST')}))
on('AF_FAST',(None,'AFTER_ED',{fastok:1}))
on('TABK',(None,'TK1',{r1:cb+2062}))
on('TK1',(net.and_(net.step(R1),net.lt(cp+1,npar,S('TK1'))),'MVJ',{jp:cp+1,jo:0,jret.r:jret.id('MVEND')}),(None,'TAB2',{ins_ch:32,ins_st:ty,oret.r:oret.id('TAB3')}));on('TAB2',(None,'INS',None))
tabn=R()
on('TAB3',(net.ge(tabn,3,S('TAB3')),'AFTER_ED',{tabn:0}),(None,'INS',{tabn:tabn+1,ins_ch:32,ins_st:ty,oret.r:oret.id('TAB3')}))
on('AFTER_ED',(fastok,'SYNC',{ap:cp,ao:co,autos:1,blink:0}),(None,'SYNC',{ap:cp,ao:co,autos:1,blink:0,lc:1}))
on('SYNC',(None,'RD0',{ap:cp,ao:co}))
on('BKSP',(has_sel,'DS0',{dret.r:dret.id('AFTER_ED')}),(None,'BK1',{oret.r:oret.id('AFTER_ED')}))
on('BK1',(net.step(co),'DEL',{co:co-1}),(net.step(cp),'MG0',{}),(None,'AFTER_ED',None))
on('DELK',(has_sel,'DS0',{dret.r:dret.id('AFTER_ED')}),(net.lt(co,clen,S('DELK')),'DEL',{oret.r:oret.id('AFTER_ED')}),
   (net.lt(cp+1,npar,S('DELK')),'DK2',{jp:cp+1,jo:0,jret.r:jret.id('DK3')}),(None,'AFTER_ED',None))
on('DK2',(None,'J0',None));on('DK3',(None,'MG0',{oret.r:oret.id('AFTER_ED')}))
on('ENTER',(has_sel,'DS0',{dret.r:dret.id('EN2')}),(None,'EN2',None))
on('EN2',(None,'EN3',{r1:cb+2062}))
on('EN3',(net.step(R1),'AFTER_ED',None),(None,'SPLIT',{oret.r:oret.id('AFTER_ED')}))
on('PB0',(has_sel,'DS0',{dret.r:dret.id('PB1')}),(None,'PB1',None))
on('PB1',(None,'SPLIT',{oret.r:oret.id('PB2')}))
on('PB2',(None,'AFTER_ED',{w1:(cb+PBRK,1)}))
# ---- caret moves ----
def moved(c): return {autos:1,blink:0}
on('MOVL',(net.and_(has_sel,ONE-shiftk),'MVJ',{jp:lo_p,jo:lo_o,jret.r:jret.id('MVCL')}),(net.step(co),'MVEND',{co:co-1}),(net.step(cp),'MVJ',{jp:cp-1,jo:2047,jret.r:jret.id('MVEND')}),(None,'MVEND',None))
on('MVJ',(None,'J0',None));on('MVCL',(None,'MVEND',{ap:cp,ao:co}))
on('MOVR',(net.and_(has_sel,ONE-shiftk),'MVJ',{jp:hi_p,jo:hi_o,jret.r:jret.id('MVCL')}),(net.lt(co,clen,S('MOVR')),'MVEND',{co:co+1}),(net.lt(cp+1,npar,S('MOVR')),'MVJ',{jp:cp+1,jo:0,jret.r:jret.id('MVEND')}),(None,'MVEND',None))
# vertical and line moves read the last screenshot through the hit network
cx=R();cy=R();chh=R(19)
scr_cy=cy+DOCY-scroll
on('MOVU',(None,'HT',{hx_:cx+1,hy_:net.relu(scr_cy-3),hdir:1,hact:1}))
on('MOVD',(None,'HT',{hx_:cx+1,hy_:scr_cy+chh+3,hdir:0+2,hact:1}))
on('MOVH',(None,'HT',{hx_:PX+2,hy_:scr_cy+2,hdir:0,hact:1}))
on('MOVE',(None,'HT',{hx_:PX+810,hy_:scr_cy+2,hdir:0,hact:1}))
# line start or end lands on the shared end state
on('MVEND',(shiftk,'TYSY',{autos:1,blink:0}),(None,'TYSY',{ap:cp,ao:co,autos:1,blink:0,fastok:1}))
on('TYSY',(net.step(co),'TYS2',{r2:cb+1024+co-1}),(None,'ASC0',None))
on('TYS2',(net.step(R2),'ASC0',{ty:R2}),(None,'ASC0',{ty:0}))
on('ASC0',(None,'ASC1',{r1:as_x(PT)+cp}))
on('ASC1',(None,'ASC2',{r2:R1+SAVE}))
e=S('ASC2')
on('ASC2',(net.lt(R2,scroll+40,e),'RD0',{scroll:net.relu(R2-40),fastok:0}),(net.gt(R2+20,scroll+VH-40,e),'RD0',{scroll:net.relu(R2+60-VH),fastok:0}),(None,'RD0',None))
on('SELALL',(None,'SA2',{ap:0,ao:0,jp:net.relu(npar-1),jo:2047,jret.r:jret.id('SA3')}));on('SA2',(None,'J0',None));on('SA3',(None,'RD0',{autos:0}))
# ---- hit test on the screenshot ----
net.group('screenshot hit test')
on('MD',(None,'HT',{hdir:0+3,hact:0,drag:1,grp:grp+1}))
on('MD2',(None,'HT',{hdir:3,hact:2}))
on('HT',(None,'HT1',{pix:(hx_,hy_)}))
A_=pix.out[3]; e1=S('HT1')
on('HT1',(net.and_(e1,net.step(A_-199)),'BTN',{btn:A_-200,drag:0}),
 (net.step(A_),'VL0',{hcol:A_-1,vi:0}),
 (net.and_(e1,net.eq(hdir,1,e1),net.ge(hy_,DOCY+4,e1)),'HT',{hy_:hy_-3}),
 (net.and_(e1,net.eq(hdir,2,e1),net.lt(hy_,DOCB-4,e1)),'HT',{hy_:hy_+3}),
 (net.and_(e1,net.eq(hdir,3,e1),net.ge(hy_,DOCY+4,e1),net.lt(hy_,DOCB,e1)),'HT',{hy_:hy_-2}),
 (None,'MVEND',{drag:0}))
on('VL0',(None,'VL1',{rl:as_x(VL)+vi*6}))
RL=rl.out
e2=S('VL1')
vj=R()
on('VL1',(net.and_(e2,net.ge(hy_,RL[0],e2),net.lt(hy_,RL[1],e2),net.ge(hx_,RL[4],e2),net.lt(hx_,RL[5],e2)),'VLa',{jp:RL[2],vj:RL[3],r1:as_x(PT)+RL[2]}),
 (net.ge(vi,150,e2),'MVEND',None),(None,'VL0',{vi:vi+1}))
on('VLa',(None,'VLb',{rl:R1+LINES+vj*8}))
on('VLb',(None,'J0',{jo:rl.out[0]+hcol,jret.r:jret.id('HEND')}))
hactb=net.decode(hact,3,S('HEND'))
on('HEND',(hactb[0],'HE0',{}),(None,'MVEND',None))
on('HE0',(None,'RD0',{ap:cp,ao:co,blink:0}))
# ---- jump: load caret paragraph ----
on('J0',(None,'J1',{r1:as_x(PT)+jp}))
on('J1',(None,'J2',{cb:R1,r2:R1+LEN}))
on('J2',(None,'JR',{clen:R2,cp:jp,co:net.min_(jo,R2)}))
# ---- edit primitives with undo log ----
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
on('SPLIT',(net.ge(nextb,SLOTMAX,S('SPLIT')),'OR',None),(None,'S1',{rb:(cb+co,clen-co)}))
on('S1',(None,'S2',{wb:(nextb,clen-co),rb:(cb+1024+co,clen-co)}))
on('S2',(None,'S3',{wb:(nextb+1024,clen-co),w1:(nextb+LEN,clen-co),w2:(nextb+DIRTY,1),w3:(cb+LEN,co),w4:(cb+DIRTY,1),r1:cb+ALIGN,r2:cb+LIST}))
on('S3',(None,'S4',{w1:(nextb+ALIGN,R1),w2:(nextb+LIST,R2),rb:(as_x(PT)+cp+1,net.relu(npar-cp-1))}))
e=S('S4'); log(e,3,cp,co,0,0)
on('S4',(None,'OR',{wb:(as_x(PT)+cp+2,net.relu(npar-cp-1)),w1:(as_x(PT)+cp+1,nextb),cp:cp+1,cb:nextb,co:0,clen:clen-co,npar:npar+1,nextb:nextb+STRIDE}))
pb=R();plen=R()
on('MERGE',(None,'M1',{r1:as_x(PT)+cp-1}))
on('M1',(None,'M2',{pb:R1,r2:R1+LEN}))
on('M2',(net.ge(R2+clen,1000,S('M2')),'OR',None),(None,'M3',{plen:R2,rb:(cb,clen)}))
on('M3',(None,'M4',{wb:(pb+plen,clen),rb:(cb+1024,clen)}))
on('M4',(None,'M5',{wb:(pb+1024+plen,clen),w1:(pb+LEN,plen+clen),w2:(pb+DIRTY,1),rb:(as_x(PT)+cp+1,net.relu(npar-cp-1))}))
e=S('M5'); log(e,4,cp-1,plen,0,0)
on('M5',(None,'OR',{wb:(as_x(PT)+cp,net.relu(npar-cp-1)),cp:cp-1,co:plen,cb:pb,clen:clen+plen,npar:npar-1}))
on('MG0',(None,'MG1',{r1:as_x(PT)+cp-1}))
on('MG1',(None,'MG2',{rc:cb+2062,r2:R1+2062}))
on('MG2',(net.step(rc.out[0]+R2),'MGJ',{jp:cp-1,jo:2047,jret.r:jret.id('OR')}),(None,'MERGE',None))
on('MGJ',(None,'J0',None))
# delete selection
on('DS0',(None,'DS1',{ap:lo_p,ao:lo_o,jp:hi_p,jo:hi_o,jret.r:jret.id('DSL')}));on('DS1',(None,'J0',None))
e=S('DSL')
on('DSL',(net.ge(Ka,Kc,e),'DR',None),(net.step(co),'DEL',{co:co-1,oret.r:oret.id('DSL')}),(None,'MG0',{oret.r:oret.id('DSL')}))
# ---- undo and redo ----
net.group('undo')
U=rlog.out; uop=R();up=R();uo=R();uch=R();ust=R();ug=R();ub=R()
on('UNDO',(net.ge(usp,UB+6,S('UNDO')),'U1',{rlog:usp-6,nolog:1}),(None,'HALT',None))
on('U1',(None,'U2',{uop:U[0],up:U[1],uo:U[2],uch:U[3],ust:U[4],ug:U[5],usp:usp-6}))
h=net.decode(uop,6,S('U2'))
on('U2',(h[1],'UJ',{jp:up,jo:uo,jret.r:jret.id('DEL'),oret.r:oret.id('UCK')}),
 (h[2],'UJ',{jp:up,jo:uo,jret.r:jret.id('UI2'),oret.r:oret.id('UCK')}),
 (h[3],'UJ',{jp:up+1,jo:0,jret.r:jret.id('MERGE'),oret.r:oret.id('UCK')}),
 (h[4],'UJ',{jp:up,jo:uo,jret.r:jret.id('SPLIT'),oret.r:oret.id('UCK')}),
 (h[5],'UJ',{jp:up,jo:uo,jret.r:jret.id('UST'),oret.r:oret.id('UCK')}),(None,'UCK',None))
on('UJ',(None,'J0',None))
on('UI2',(None,'INS',{ins_ch:uch,ins_st:ust}))
mark_d(S('UST'),cp);mark_d(S('VST'),cp)
on('UST',(None,'UCK',{w1:(cb+1024+co,uch),w2:(cb+DIRTY,1)}))
on('UCK',(net.ge(usp,UB+6,S('UCK')),'UCK2',{rlog:usp-6}),(None,'UEND',None))
on('UCK2',(net.eq(U[5],ug,S('UCK2')),'U1',{rlog:usp-6}),(None,'UEND',None))
on('UEND',(None,'SYNC',{nolog:0,autos:1,blink:0,lc:1}))
on('REDO',(net.lt(usp,urp,S('REDO')),'V1',{rlog:usp,nolog:1}),(None,'HALT',None))
on('V1',(None,'V2',{uop:U[0],up:U[1],uo:U[2],uch:U[3],ust:U[4],ug:U[5],usp:usp+6}))
h=net.decode(uop,6,S('V2'))
on('V2',(h[1],'UJ',{jp:up,jo:uo,jret.r:jret.id('UI2'),oret.r:oret.id('VCK')}),
 (h[2],'UJ',{jp:up,jo:uo,jret.r:jret.id('DEL'),oret.r:oret.id('VCK')}),
 (h[3],'UJ',{jp:up,jo:uo,jret.r:jret.id('SPLIT'),oret.r:oret.id('VCK')}),
 (h[4],'UJ',{jp:up+1,jo:0,jret.r:jret.id('MERGE'),oret.r:oret.id('VCK')}),
 (h[5],'UJ',{jp:up,jo:uo,jret.r:jret.id('VST'),oret.r:oret.id('VCK')}),(None,'VCK',None))
on('VST',(None,'VCK',{w1:(cb+1024+co,ust),w2:(cb+DIRTY,1)}))
on('VCK',(net.lt(usp,urp,S('VCK')),'VCK2',{rlog:usp}),(None,'UEND',None))
on('VCK2',(net.eq(U[5],ug,S('VCK2')),'V1',{rlog:usp}),(None,'UEND',None))
# ---- range walker for copy and formatting ----
net.group('range walker')
wp=R();wbase=R();wo=R();wlen=R();wn=R();wm=R();wfirst=R();ftgt=R()
Kw=wp*2048+wo; wsel=Bus(net)
on('COPY',(has_sel,'W0',{wp:lo_p,wo:lo_o,wn:0,wm:1,wret.r:wret.id('COPYE')}),(None,'HALT',None))
on('CUT',(has_sel,'W0',{wp:lo_p,wo:lo_o,wn:0,wm:1,wret.r:wret.id('CUT2'),grp:grp+1}),(None,'HALT',None))
on('CUT2',(None,'DS0',{dret.r:dret.id('AFTER_ED'),clipl:wn+1}))
on('COPYE',(None,'HALT',{clipl:wn+1}))
clipout.add(S('HALT'),clipl); fsm.set(clipl,S('HALT'),0)
wantp=Bus(net); wantp.lin(S('HALT')*0+wpaste); fsm.set(wpaste,S('HALT'),0)
e=S('W0')
on('W0',(None,'W1',{r1:as_x(PT)+wp}))
on('W1',(None,'W2',{wbase:R1,r2:R1+LEN}))
on('W2',(None,'W3',{wlen:R2}))
e=S('W3')
on('W3',(net.ge(Kw,Hi,e),'WR',None),(net.ge(wo,wlen,e),'WNL',{}),(None,'W4',{r1:wbase+wo,r2:wbase+1024+wo}))
e=S('WNL')
on('WNL',(None,'WNL2',{wp:wp+1,wo:0,wn:wn+net.eq(wm,1,e)}))
wnl_c=net.and_(e,net.eq(wm,1,e)); w1.drive(wnl_c,(as_x(CB)+wn,10))
on('WNL2',(None,'W0',None))
# style arithmetic for formatting commands
fin=Bus(net); fen=Bus(net); FD=style_decode(fin.w,fen.w); fsz=FD['size']
szh=net.decode(fsz,11,fen.w)
UP={0:1,1:2,2:3,3:4,4:5,5:6,6:7,7:8,8:8,9:10,10:0}; DN={1:0,2:1,3:2,4:3,5:4,6:5,7:6,8:7,0:10,10:9,9:9}
up_=X();dn_=X()
for i in range(11): up_=up_+szh[i]*UP[i]; dn_=dn_+szh[i]*DN[i]
fmh=net.decode(fm,16,fen.w); fcol=R(); fpre=R()
tb=ONE-FD['bold'];ti=ONE-FD['ital'];tu=ONE-FD['und'];tf=ONE-FD['font']
def field_new(tg):
    s_=fin.w
    return (G_(s_-FD['bold']*16+tg[0]*16,fmh[1])+G_(s_-FD['ital']*32+tg[1]*32,fmh[2])+G_(s_-FD['und']*64+tg[2]*64,fmh[3])
      +G_(s_-fsz+up_,fmh[4])+G_(s_-fsz+dn_,fmh[5])+G_(s_-FD['font']*128+tg[3]*128,fmh[6])+G_(s_-FD['color']*256+fcol*256,fmh[7])+G_(fpre+0,fmh[8]))
fist=wfirst
t_bold=G_(tb,fist)+G_(ftgt,ONE-fist);t_it=G_(ti,fist)+G_(ftgt,ONE-fist);t_un=G_(tu,fist)+G_(ftgt,ONE-fist);t_f=G_(tf,fist)+G_(ftgt,ONE-fist)
newst=field_new((t_bold,t_it,t_un,t_f))
tgt_now=G_(t_bold,fmh[1])+G_(t_it,fmh[2])+G_(t_un,fmh[3])+G_(t_f,fmh[6])
on('FMTS',(has_sel,'W0',{wp:lo_p,wo:lo_o,wm:2,wfirst:1,grp:grp+1,wret.r:wret.id('FEND')}),(None,'FTY',{wfirst:1}))
fen.lin(S('W4')*1); fin.add(S('W4'),R2); fen.lin(S('FTY')); fin.add(S('FTY'),ty)
on('FTY',(None,'RD0',{ty:net.relu(newst),wfirst:0}))
e=S('W4')
cc=net.and_(e,net.eq(wm,1,e)); w1.drive(cc,(as_x(CB)+wn,R1)); 
fm_c=net.and_(e,net.eq(wm,2,e))
w2.drive(fm_c,(wbase+1024+wo,newst)); w3.drive(fm_c,(wbase+DIRTY,1)); log(fm_c,5,wp,wo,R2,newst)
fsm.set(ftgt,fm_c,tgt_now); fsm.set(wfirst,fm_c,0)
on('W4',(None,'W3',{wo:wo+1,wn:wn+net.eq(wm,1,e)}))
on('FEND',(net.eq(fm,8,S('FEND')),'RD0',{ap:cp,ao:co,lc:1}),(None,'RD0',{lc:1}))
# paragraph properties over the selected paragraphs
pwalk=R();pfld=R()
on('SETAL',(None,'PA0',{pwalk:lo_p,pfld:ALIGN}))
on('SETLI',(None,'PA0',{pwalk:lo_p,pfld:LIST}))
on('PA0',(None,'PA1',{r1:as_x(PT)+pwalk}))
e=S('PA1'); mark_d(e,pwalk)
on('PA1',(None,'PA2',{w1:(R1+pfld,alv),w2:(R1+DIRTY,1)}))
on('PA2',(net.lt(pwalk,hi_p,S('PA2')),'PA0',{pwalk:pwalk+1}),(None,'RD0',{lc:1}))
# ---- find and replace ----
net.group('find and replace')
fp=R();fbs=R();fo=R();fl=R();fk=R();wrap=R();rall=R();ri=R()
def low(x,en): return x+net.and_(net.ge(x,65,en),net.lt(x,91,en))*32
e=S('FIND')
on('FIND',(net.step(net.and_(net.eq(mode,2,e),has_sel)+0),'RP0',{grp:grp+1}),(None,'FN1',{fp:hi_p,fo:hi_o,wrap:0}))
on('FN1',(net.step(S('FN1')-net.step(qlen)),'RD0',None),(None,'F0',None))
e=S('F0')
on('F0',(net.and_(net.ge(fp,npar,e),wrap),'RD0',{rall:0}),(net.ge(fp,npar,e),'F0',{fp:0,fo:0,wrap:1}),(None,'F1',{r1:as_x(PT)+fp}))
on('F1',(None,'F2',{fbs:R1,r2:R1+LEN}))
on('F2',(None,'F3',{fl:R2,fk:0}))
e=S('F3')
on('F3',(net.step(fo+qlen-fl),'F0',{fp:fp+1,fo:0}),(None,'F4',{r1:fbs+fo+fk,r2:as_x(Q)+fk}))
e=S('F4'); m=net.eq(low(R1,e),low(R2,e),e)
on('F4',(net.and_(m,net.ge(fk+1,qlen,e)),'FJ',{ap:fp,ao:fo,jp:fp,jo:fo+qlen,jret.r:jret.id('FOUND')}),(m,'F3',{fk:fk+1}),(None,'F3',{fo:fo+1,fk:0}))
on('FJ',(None,'J0',None))
on('FOUND',(net.and_(S('FOUND'),rall),'RP0',{wrap:wrap}),(None,'RD0',{autos:1,blink:0}))
on('RP0',(None,'DS0',{dret.r:dret.id('RP1')}))
on('RP1',(None,'RP2',{ri:0}))
e=S('RP2')
on('RP2',(net.ge(ri,rlen,e),'RP4',None),(None,'RP3',{r1:as_x(RPL)+ri}))
on('RP3',(None,'INS',{ins_ch:R1,ins_st:ty,ri:ri+1,oret.r:oret.id('RP2')}))
on('RP4',(None,'SYNC2',{ap:cp,ao:co})); on('SYNC2',(None,'FIND2',None))
on('FIND2',(None,'FN1',{fp:cp,fo:co,wrap:0}))
# ---- paste ----
net.group('paste')
CB2=CB+200000; pi_=R()
on('PASTE',(has_sel,'DS0',{dret.r:dret.id('PS1'),grp:grp+1}),(None,'PS1',{grp:grp+1}))
on('PS1',(None,'PS2',{pi_:0}))
e=S('PS2')
on('PS2',(net.ge(pi_,evc,e),'AFTER_ED',None),(None,'PS3',{r1:as_x(CB2)+pi_}))
e=S('PS3')
on('PS3',(net.eq(R1,10,e),'SPLIT',{pi_:pi_+1,oret.r:oret.id('PS2')}),(net.lt(R1,32,e),'PS2',{pi_:pi_+1}),(net.ge(clen,1000,e),'PS2',{pi_:pi_+1}),(None,'INS',{ins_ch:R1,ins_st:ty,pi_:pi_+1,oret.r:oret.id('PS2')}))
# ---- layout and paint walk ----
net.group('layout and paint')
ls_=R();le_=R();lx=R();lhh=R();lasc=R();lex=R();off=R();col=R();x=R();lb=R();lbx=R();lspb=R();lsn=R();xw=R();prevsp=R();wc=R()
lend=R();lwid=R();lspc=R();llast=R();pcp=R();cacol=R();thumb=R()
tpad=net.step(tcols)*6
xc_=net.step(xcol)
lleft=rleft+G_(as_x(TX-PX)+xcol,xc_)
lright=rright+xcol
GRAY=(230,230,230);WHITE=(255,255,255);SEL=PAL_B[1]
on('RD0',(None,'RD1',{clip0:DOCY,clip1:DOCB,full:ONE-net.and_(S('RD0'),fastok,ONE-wassel,ONE-has_sel),fastok:0}))
minc=net.min_(cp,oldcp);maxc=net.max_(cp,oldcp)
e=S('RD1')
on('RD1',(net.and_(e,ONE-full),'RF0',{sidx:minc,vm:0}),
 (lc,'VS2048',{rA:(0,DOCY,1262,VH,GRAY,0),sidx:0,vm:0,vln:0,bgp:0}),
 (None,'VS2048',{rA:(0,DOCY,1262,VH,GRAY,0),sidx:0,vm:1,vln:0}))
on('VSEND',(lc,'RF0',{sidx:net.min_(sidx,dfrom)}),(None,'RF0',None))
on('RF0',(None,'RF1',{r1:as_x(PT)+sidx}))
on('RF1',(None,'RF2',{rl:R1+SAVE,rc:R1+2062,rf:R1+FNS}))
RL=rl.out
fload={fnn:rf.out[0],fnp:rf.out[1],yy:RL[0],ptop:RL[1],pages:RL[2],wsum:RL[3],listn:RL[4],xcol:RL[5],pi:sidx}
RC=rc.out
on('RF2',(net.and_(full,net.step(RC[1])),'RF0',{sidx:sidx-RC[1]}),(full,'PNV',{**fload,rowmax:0,rB:(PX,RL[1]+DOCY-scroll,816,PH,WHITE,0)}),(None,'R1',fload))
steps=[2048,1024,512,256,128,64,32,16,8,4,2,1]
for i,st_ in enumerate(steps):
    nxt=f'VS{steps[i+1]}' if i+1<len(steps) else 'VSEND'
    e=S(f'VS{st_}')
    on(f'VS{st_}',(net.lt(sidx+st_,npar,e),f'VSa{st_}',{r1:as_x(PT)+sidx+st_}),(None,nxt,None))
    on(f'VSa{st_}',(None,f'VSb{st_}',{r2:R1+SAVE+1}))
    e=S(f'VSb{st_}')
    on(f'VSb{st_}',(net.ge(scroll,R2+PST,e),nxt,{sidx:sidx+st_}),(None,nxt,None))
e=S('R1')
saveb={bfn:fnn,bfp:fnp,bxc:xcol,bpi:pi,byy:yy,bptop:ptop,bpg:pages,bws:wsum,bln:listn}
on('R1',(net.and_(bgm,net.ge(pi,npar,e)),'BGD',None),(net.ge(pi,npar,e),'RE0',None),
 (net.and_(bgm,net.ge(bcnt,60,e)),'HALT',{**saveb,bgm:0}),
 (net.and_(full,ONE-vm,ONE-bgm,net.gt(yy,scroll+VH,e),net.gt(pi,cp,e),net.or_(xc_,net.lt(ncol,2,e))),'RE0',{**saveb,bgp:1}),(net.and_(ONE-full,net.gt(pi,maxc,e)),'RE0',None),(net.and_(vm,net.gt(yy,scroll+VH,e),net.or_(xc_,net.lt(ncol,2,e))),'RE0',None),(None,'R2',{r1:as_x(PT)+pi}))
on('R2',(None,'R3',{rim:R1+IMF,pbs:R1,rl:R1+LEN,rc:R1+2062,rf:R1+FNS}))
on('R2X',(None,'R3',{rim:pbs+IMF,rl:pbs+LEN,rc:pbs+2062,rf:pbs+FNS}))
RL=rl.out
pbk=R()
e3=S('R3'); hc_=net.decode(rc.out[0],9,e3); hi_c=net.decode(rc.out[1],9,e3); tb3=net.step(rc.out[0])
geom_w=X(c=0); geom_x=X()
for cc_ in range(1,9):
    geom_w=geom_w+hc_[cc_]*(TW//cc_)
    for ii_ in range(cc_): geom_x=geom_x+net.and_(net.step(hc_[cc_]),net.step(hi_c[ii_]))*(ii_*(TW//cc_))
two=net.and_(net.step(hc_[0]),net.eq(ncol,2,e3))
geom_w=geom_w+(hc_[0]-two)*TW+two*300
meta0={pim:rim.out[0],pih:rim.out[1],pio:rim.out[2],pfn:rf.out[2],tcols:rc.out[0],tci:rc.out[1],rw:geom_w,rx0:geom_x,rleft:hc_[0]*PX+G_(as_x(TX+1)+geom_x,tb3),rright:(hc_[0]-two)*(PX+816)+two*(TX+300)+G_(as_x(TX)+geom_x+geom_w,tb3)}
meta={**meta0,plen_:RL[0],al:RL[2],lsf:RL[3],nl:RL[4],wdp:RL[5],oend:RL[6],pbk:RL[7]}
on('R3',(net.step(RL[1]),'LAY0',{**meta,lj:0,ls_:0,off:0,lx:0,lb:0,lbx:0,lsn:0,lspb:0,lasc:0,lhh:0,wc:0,prevsp:1,llast:0}),(None,'R3B',meta))
e=S('R3B')
pb_=net.or_(net.and_(pbk,net.gt(yy,ptop+96,e)),net.and_(net.step(tcols),net.eq(tci,0,e),net.gt(yy+60,ptop+96+864,e)),net.and_(net.step(pfn),net.eq(fnp,0,e),net.gt(yy+120,ptop+96+864,e)))
pnew={fnp:0,ptop:ptop+PST,yy:ptop+PST+96,pages:pages+1,xcol:0}
on('R3B',(net.and_(pb_,full),'PNB',{**pnew,rB:(PX,ptop+PST+DOCY-scroll,816,PH,WHITE,0)}),(pb_,'R4',pnew),(None,'R4',None))
e=S('R4')
fsm.set(fnn,net.and_(e,net.step(pfn)),fnn+1);fsm.set(fnp,net.and_(e,net.step(pfn)),fnp+1)
nlist=G_(listn+1,net.eq(lsf,2,e))
wln.drive(e,(pbs+SAVE,yy,ptop,pages,wsum,listn,xcol));w1.drive(e,(pbs+FNS,fnn));w2.drive(e,(pbs+FNS+1,fnp))
intab=net.step(tcols); c0=net.eq(tci,0,e)
fsm.set(rowtop,net.and_(e,c0),yy); fsm.set(rowmax,net.and_(e,c0),0)
on('R4',(intab,'R5',{wsum:wsum+wdp,lj:0,listn:nlist,yy:yy+3}),(None,'R5',{wsum:wsum+wdp,lj:0,listn:nlist}))
e=S('R5')
on('R5',(net.ge(lj,nl,e),'RP',None),(None,'R6',{rl:pbs+LINES+lj*8}))
e=S('R6'); ne=net.and_(net.gt(yy+RL[3]+net.step(fnp)*98,ptop+96+864,e),net.gt(yy,ptop+96,e))
lm={ls_:RL[0],le_:RL[1],lx:RL[2],lhh:RL[3],lasc:RL[4],lex:RL[5]}
c1=net.and_(ne,net.eq(ncol,2,e),ONE-net.step(xcol))
on('R6',(c1,'R7',{**lm,yy:ptop+96,xcol:324}),(net.and_(ne,full),'PN',{**lm,fnp:0,xcol:0,ptop:ptop+PST,yy:ptop+PST+96,pages:pages+1,rB:(PX,ptop+PST+DOCY-scroll,816,PH,WHITE,0)}),(ne,'R7',{**lm,fnp:0,xcol:0,ptop:ptop+PST,yy:ptop+PST+96,pages:pages+1}),(None,'R7',lm))
DEAD=lambda *a:None
DEAD('R6',(net.and_(ne,full),'PN',{**lm,ptop:ptop+PST,yy:ptop+PST+96,pages:pages+1,rB:(PX,ptop+PST+DOCY-scroll,816,PH,WHITE,0)}),(ne,'R7',{**lm,ptop:ptop+PST,yy:ptop+PST+96,pages:pages+1}),(None,'R7',lm))
def _t10(v,e):
    b_=net.gate(v,e); t_=X()
    for k_ in range(1,10): t_=t_+net.step(b_-10*k_+0.5)
    return t_
def page_num(st0,nxt):
    st=st0+'n'; e=S(st0); hy=ptop+48+DOCY-scroll
    on(st0,(None,st0+'h',{hdi:0,sx:as_x(TX)}))
    e=S(st0+'h')
    on(st0+'h',(net.ge(hdi,hlen,e),st,None),(None,st0+'i',{r1:as_x(HD)+hdi}))
    on(st0+'i',(None,st0+'h',{gly:(R1,9,sx,hy,1,0),sx:sx+adv,hdi:hdi+1}))
    e=S(st); base=net.gate(pages,e); tn=X()
    for t in range(1,13): tn=tn+net.step(base-10*t+0.5)
    fy=ptop+PH-60+DOCY-scroll
    on(st,(net.step(base-9.5),st+'b',{gly:(48+tn,9,PX+400,fy,1,0)}),(None,st+'b',None))
    e=S(st+'b'); base=net.gate(pages,e); tn=X()
    for t in range(1,13): tn=tn+net.step(base-10*t+0.5)
    on(st+'b',(None,nxt,{gly:(48+pages-tn*10,9,PX+408,fy,1,0)}))
page_num('PN','R7');page_num('PNV','R1');page_num('PNB','R4');page_num('PN0','R1')
e=S('R7')
here=net.and_(net.eq(pi,cp,e),net.ge(co,ls_,e),net.or_(net.lt(co,le_,e),net.eq(le_,plen_,e)))
fsm.set(cy,here,yy);fsm.set(chh,here,lhh);fsm.set(pcp,here,pages)
vis=net.and_(net.gt(yy+lhh,scroll,e),net.lt(yy,scroll+VH,e))
pa=net.or_(full,net.eq(pi,cp,e),net.eq(pi,oldcp,e))
cvl=net.and_(vis,full); wvl.drive(cvl,(as_x(VL)+vln*6,yy+DOCY-scroll,yy+DOCY-scroll+lhh,pi,lj,lleft,lright)); fsm.set(vln,cvl,vln+1)
on('R7',(net.and_(vis,pa),'R8',None),(None,'R9',None))
sy=yy+DOCY-scroll
ind=net.step(lsf)*48
e=S('R8')
on('R8',(net.and_(net.eq(ls_,0,e),net.eq(lsf,1,e)),'BUL',{rA:(lleft,sy,as_x(TX)+rx0+xcol+tpad-lleft+lx+ind,lhh,WHITE,1),x:as_x(TX)+rx0+xcol+tpad+ind+lx,off:ls_,col:1}),
 (net.and_(net.eq(ls_,0,e),net.eq(lsf,2,e)),'NUM',{rA:(lleft,sy,as_x(TX)+rx0+xcol+tpad-lleft+lx+ind,lhh,WHITE,1),x:as_x(TX)+rx0+xcol+tpad+ind+lx,off:ls_,col:1}),
 (None,'C0',{rA:(lleft,sy,as_x(TX)+rx0+xcol+tpad-lleft+lx+ind,lhh,WHITE,1),x:as_x(TX)+rx0+xcol+tpad+ind+lx,off:ls_,col:1}))
gly_y=sy+lasc-asc
on('BUL',(None,'C0',{gly:(127,0,x-20,gly_y,0,0)}))
e=S('NUM'); nb=net.ge(listn,10,e); tens=X(); 
for t in range(1,10): tens=tens+net.ge(listn,t*10,e)
on('NUM',(nb,'NUM2',{gly:(48+tens,0,x-32,gly_y,0,0)}),(None,'NUM2',None))
e=S('NUM2'); on('NUM2',(None,'NUM3',{gly:(48+listn-tens*10,0,x-24,gly_y,0,0)}))
on('NUM3',(None,'C0',{gly:(46,0,x-16,gly_y,0,0)}))
e=S('C0')
on('C0',(net.ge(off,le_,e),'CE',None),(None,'C1',{r1:pbs+off,r2:pbs+1024+off}))
e=S('C1')
Kp=pi*2048+off; insel=net.and_(net.ge(Kp,Lo,e),net.lt(Kp,Hi,e)); nosel=e-insel
isp=net.eq(R1,32,e); xtra=G_(lex,isp); chere=net.and_(net.eq(pi,cp,e),net.eq(off,co,e))
fsm.set(cx,chere,x);fsm.set(cacol,chere,col)
g_en.lin(e);g_ch.add(e,R1);g_st.add(e,R2);g_x.add(e,x);g_y.add(e,gly_y+YB)
g_draw.lin(e-isp)
colh=net.decode(SD['color'],8,e)
for j in range(8): fg[j].lin(colh[j])
bg[1].lin(insel);bg[0].lin(nosel)
adv2=adv*0.5
def selcol(i): return G_(as_x(SEL[i]),insel)+G_(as_x(255),nosel)
for rr,xx,ww,aa in ((rA,x,adv2+1,col),(rB,x+adv2,adv2+1+xtra,col+1)):
    rr.b[0].lin(e)
    for b,val in zip(rr.b[1:],(xx,sy+YB,ww,lhh)): b.add(e,val)
    for i in range(3): rr.b[5+i].lin(insel*SEL[i]+nosel*255)
    rr.b[8].add(e,aa)
und=net.and_(e,SD['und']); ucol=colh
rC.drive(und,(x,sy+lasc+2,adv+xtra,1,(0,0,0),col))
on('C1',(None,'C0',{x:x+adv+xtra,col:col+1,off:off+1}))
e=S('CE'); chere2=net.and_(net.eq(pi,cp,e),net.eq(off,co,e))
fsm.set(cx,chere2,x);fsm.set(cacol,chere2,col)
on('IM0',(net.ge(irow,pih,S('IM0')),'CB0',None),(None,'IM0',{imr:(x,sy+irow,as_x(IMG0)+pio+iaddr,pim),irow:irow+1,iaddr:iaddr+pim}))
on('CE',(net.step(pim),'IM0',{irow:0,iaddr:0,rA:(x,sy,lright-x,lhh,WHITE,net.min_(col,199))}),(net.and_(net.eq(ls_,0,e),ONE-net.step(tcols)),'CB0',{rA:(x,sy,lright-x,lhh,WHITE,net.min_(col,199))}),(None,'R9',{rA:(x,sy,lright-x,lhh,WHITE,net.min_(col,199))}))
on('CB0',(None,'CB1',{r1:pbs+CMTL}))
e=S('CB1'); BAL=PAL_B[2]
on('CB1',(net.step(R1),'CB2',{cl_:R1,ci_:0,sx:1048,rA:(1044,sy,214,lhh+4,BAL,0),rB:(TX+TW,sy+8,101,1,(200,170,60),0)}),(None,'R9',None))
e=S('CB2')
on('CB2',(net.or_(net.ge(ci_,cl_,e),net.gt(sx,1240,e)),'R9',None),(None,'CB3',{r1:pbs+CMT+ci_}))
on('CB3',(None,'CB2',{gly:(R1,9,sx,sy+2,0,2),sx:sx+adv,ci_:ci_+1}))
on('R9',(None,'R5',{yy:yy+lhh,lj:lj+1}))
e=S('RP')
ch_=net.step(net.step(yy-oend)+net.step(oend-yy)+0)
w1.drive(e,(pbs+ENDY,yy))
notlast=net.and_(net.step(tcols),net.lt(tci+1,tcols,e)); lastc_=net.and_(net.step(tcols),ONE-notlast)
newmax=net.max_(rowmax,yy+3)
adv_={bcnt:bcnt+bgm}
fy=ptop+96+864-88+fnp*22-22+DOCY-scroll
on('FOOT0',(None,'FOOT1',{gly:(48+net.gate(fnn,S('FOOT0'))-_t10(fnn,S('FOOT0'))*10,9,x+1,yy-lhh+DOCY-scroll,0,0),sx:as_x(TX)+22,fni:0,rA:(TX,ptop+96+864-92+DOCY-scroll,200,1,(120,120,120),0)}))
on('FOOT1',(None,'FOOT2',{gly:(48+net.gate(fnn,S('FOOT1'))-_t10(fnn,S('FOOT1'))*10,9,as_x(TX)+6,fy,0,0)}))
e=S('FOOT2')
on('FOOT2',(net.ge(fni,pfn,e),'RP',{pfn:0}),(None,'FOOT3',{r1:pbs+FNT+fni}))
on('FOOT3',(None,'FOOT2',{gly:(R1,9,sx,fy,0,0),sx:sx+adv,fni:fni+1}))
e=S('RP')
on('RP',(net.and_(net.step(pfn),net.lt(fnp,5,e)),'FOOT0',{}),(net.and_(ONE-full,ch_),'RD0',{lc:1}),
 (net.step(ONE-full+0),'R1',{yy:yy+11,pi:pi+1}),
 (notlast,'R1',{yy:rowtop,rowmax:newmax,pi:pi+1,**adv_}),
 (lastc_,'RB0',{rowmax:newmax,tiv:0,**adv_}),
 (None,'R1',{yy:yy+11,pi:pi+1,**adv_}))
BC=(120,120,120); by0=rowtop+DOCY-scroll
on('RB0',(None,'RB1',{rA:(TX,by0,TW,1,BC,0),rB:(TX,rowmax+DOCY-scroll,TW,1,BC,0),rC:(TX+TW,by0,1,rowmax-rowtop,BC,0)}))
e=S('RB1'); cwd=rw
on('RB1',(net.ge(tiv,tcols,e),'R1',{yy:rowmax+1,pi:pi+1}),(None,'RB1',{rA:(as_x(TX)+tivx,by0,1,rowmax-rowtop,BC,0),tiv:tiv+1,tivx:tivx+rw}))
fsm.set(tivx,S('RB0'),0)
# line breaking network
net.group('line breaking')
ww=rw-net.step(tcols)*12-net.step(lsf)*48
def measure(c,ch,st): g_en.lin(c);g_ch.add(c,ch);g_st.add(c,st)
e=S('LAY0')
on('LAY0',(net.step(pim),'EM',{lasc:0,lhh:pih,lend:0,lwid:pim,lspc:0,llast:1}),(net.eq(plen_,0,e),'LE0',None),(None,'L1',None))
e=S('LE0'); measure(e,32,ty)
on('LE0',(None,'EM',{lasc:asc,lhh:lh,lend:0,lwid:0,lspc:0,llast:1}))
on('L1',(None,'L2',{r1:pbs+off,r2:pbs+1024+off}))
e=S('L2'); measure(e,R1,R2)
sp=net.eq(R1,32,e); over=net.and_(net.gt(lx+adv,ww,e),ONE-sp); hasb=net.gt(lb,ls_,e); nsp=e-sp
lastc=net.ge(off+1,plen_,e); newword=net.and_(nsp,prevsp)
advance={lx:lx+adv,lasc:net.max_(asc,lasc),lhh:net.max_(lh,lhh),off:off+1,prevsp:sp,wc:wc+newword,lsn:lsn+sp}
fsm.set(lb,net.and_(sp,ONE-over),off+1);fsm.set(lbx,net.and_(sp,ONE-over),lx);fsm.set(lspb,net.and_(sp,ONE-over),lsn)
on('L2',(net.and_(over,hasb),'EM',{lend:lb,lwid:lbx,lspc:lspb,off:lb,llast:0}),
 (over,'EM',{lend:off,lwid:lx,lspc:lsn,llast:0}),
 (lastc,'EM',{**advance,lend:off+1,lwid:lx+adv,lspc:lsn,llast:1}),
 (None,'L1',advance))
e=S('EM'); delta=net.relu(ww-lwid); alh=net.decode(al,4,e)
just=net.and_(alh[3],ONE-llast); sph=net.decode(lspc,64,just); ex=X()
deltaj=net.gate(delta,just)
for k_ in range(1,64): ex=ex+net.gate(deltaj*(1.0/k_),sph[k_])
x0=net.gate(delta*0.5,alh[1])+net.gate(delta,alh[2])
wln.drive(e,(pbs+LINES+lj*8,ls_,lend,x0,lhh,lasc,ex))
on('EM',(llast,'LF',{lj:lj+1}),(None,'L1',{lj:lj+1,ls_:off,lx:0,lb:off,lbx:0,lsn:0,lspb:0,lasc:0,lhh:0}))
on('LF',(None,'R2X',{w1:(pbs+NLINES,lj),w2:(pbs+DIRTY,0),w3:(pbs+WORDS,wc),wtot:wtot+wc-wdp}))
# ---- end of walk: autoscroll, caret, scrollbar, status bar ----
net.group('chrome')
e=S('RE0')
endw=net.and_(e,full,ONE-vm,ONE-bgp); fsm.set(dfrom,endw,99999); fsm.set(pagesT,endw,pages);fsm.set(wtot,endw,wsum);fsm.set(ytot,endw,yy);fsm.set(lc,e,0)
on('RE0',(net.and_(autos,net.lt(cy,scroll+40,e)),'RD0',{scroll:net.relu(cy-40),autos:0}),
 (net.and_(autos,net.gt(cy+chh,scroll+VH-40,e)),'RD0',{scroll:net.relu(cy+chh-VH+40),autos:0}),
 (net.gt(scroll,ytot,e),'RD0',{scroll:net.relu(ytot-300)}),(None,'RE1',None))
e=S('RE1'); showc=net.and_(e,ONE-has_sel,ONE-blink,ONE-net.step(mode))
rA.drive(showc,(cx,cy+DOCY-scroll,1,chh,(0,0,0),cacol))
fsm.set(dfrom,net.and_(S('RE1'),ONE-full,ONE-bgp),99999)
on('BGD',(None,'RD0',{bgp:0,bgm:0,dfrom:99999,pagesT:pages,wtot:wsum,ytot:yy,lc:0}))
on('RE1',(None,'RE2',{oldcp:cp,wassel:has_sel}))
e=S('RE2'); ph=net.decode(pagesT,128,e); th=X();ty_=X()
for k_ in range(1,128):
    th=th+ph[k_]*max(20,int((VH-8)/k_)); ty_=ty_+net.gate(scroll*((VH-8)/(k_*PST)),ph[k_])
on('RE2',(None,'RE3',{clip0:0,clip1:0,rA:(1262,DOCY,18,VH,(240,240,240),250),rB:(1265,ty_+DOCY+4,12,th,(190,190,190),250),thumb:ty_+DOCY+4}))
on('RE3',(None,'STATUS',{rA:(0,DOCB,1280,24,PAL_F[3],0)}))
# number and text drawing states
def text_chain(start,items,nxt):
    """items are strings or number registers; each glyph takes one tick."""
    cur=start
    for i,it in enumerate(items):
        if isinstance(it,str):
            for j,ch in enumerate(it):
                n=f'{start}_{i}_{j}'; e=S(cur)
                # advance x through the glyph network itself
                on(cur,(None,n,{gly:(ord(ch),9,sx,sb_y,2,4),sx:sx+adv}))
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
                on(cur,(show,n,{gly:(48+dg,9,sx,sb_y,2,4),sx:sx+adv}),(None,n,None))
                cur=n
    on(cur,(None,nxt,None))
sb_y=as_x(DOCB+6)
on('STATUS',(None,'ST1',{sx:12}))
text_chain('ST1',['Page ',pcp,' of ',pagesT,'     ',wtot,' words'],'FB0')
# find bar
e=S('FB0')
fbx=R();fi_=R()
on('FB6',(None,'TB0',{gly:(ord('R'),9,PX+418,DOCY+7,0,0)}))
on('FB0',(net.step(net.eq(mode,4,e)+net.eq(mode,5,e)),'TB0',None),(net.eq(mode,3,e),'HB',{rA:(PX,DOCY,816,28,(250,250,250),0),rB:(PX,DOCY+27,816,1,(160,160,160),0),rC:(PX+60,DOCY+4,700,20,WHITE,0),fi_:0,sx:PX+64}),(net.step(mode),'FB1',{rA:(PX,DOCY,816,28,(250,250,250),0),rB:(PX,DOCY+27,816,1,(160,160,160),0),rC:(PX+60,DOCY+4,300,20,WHITE,0)}),(None,'TB0',None))
on('HB',(net.ge(fi_,hlen,S('HB')),'TB0',None),(None,'HB2',{r1:as_x(HD)+fi_}))
on('HB2',(None,'HB',{gly:(R1,0,sx,DOCY+6,0,0),sx:sx+adv,fi_:fi_+1}))
on('FB1',(None,'FBL',{fi_:0,sx:PX+64,gly:(ord('F'),9,PX+8,DOCY+7,0,0)}))
on('FBL',(net.ge(fi_,qlen,S('FBL')),'FB3',None),(None,'FBR',{r1:as_x(Q)+fi_}))
on('FBR',(None,'FBL',{gly:(R1,0,sx,DOCY+6,0,0),sx:sx+adv,fi_:fi_+1}))
on('FB3',(net.eq(mode,2,S('FB3')),'FB4',{rA:(PX+440,DOCY+4,300,20,WHITE,0),rB:(PX+750,DOCY+4,60,20,(225,225,225),200+39),fi_:0,sx:PX+444}),(None,'TB0',None))
on('FB4',(net.ge(fi_,rlen,S('FB4')),'FB6',None),(None,'FBS',{r1:as_x(RPL)+fi_}))
on('FBS',(None,'FB4',{gly:(R1,0,sx,DOCY+6,0,0),sx:sx+adv,fi_:fi_+1}))


# ribbon state: highlights and the current size and font, read from the typing style
fbr=R();fir=R();fur=R();fszv=R();ffn=R()
e=S('TB0'); measure(e,32,ty)
home_=net.eq(tab,0,e)
on('TB0',(home_,'TB1',{fbr:net.relu(SD['bold']+0),fir:net.relu(SD['ital']+0),fur:net.relu(SD['und']+0),ffn:net.relu(SD['font']+0),fszv:sum((h*p for h,p in zip(size_hot,rom.PTS)),X())}),(None,'HALT',None))
e=S('TB1')
def hc(r): return tuple(net.gate(as_x(a),r)+net.gate(as_x(b),e-net.and_(e,r)) for a,b in zip((205,225,245),(243,243,243)))
on('TB1',(None,'TB2',{rA:(120,90,24,24,hc(fbr),201),rB:(146,90,24,24,hc(fir),202),rC:(172,90,24,24,hc(fur),203)}))
on('TB2',(None,'TB3',{gly:(ord('B'),9+16,128,94,0,3)}))
on('TB3',(None,'TB4',{gly:(ord('I'),9+32,155,94,0,3)}))
on('TB4',(None,'TB5',{gly:(ord('U'),9+64,180,94,0,3)}))
on('TB5',(None,'TB6',{rA:(232,64,30,22,(255,255,255),200+4),sx:238}))
on('TB6',(None,'TB6B',{rA:(120,64,58,22,(255,255,255),206)}))
e=S('TB6B'); tens_=net.ge(fszv,10,e)+net.ge(fszv,20,e)+net.ge(fszv,30,e)
on('TB6B',(None,'TB7',{gly:(48+tens_,9,sx,68,0,0),sx:sx+adv}))
e=S('TB7'); tens7=net.ge(fszv,10,e)+net.ge(fszv,20,e)+net.ge(fszv,30,e)
on('TB7',(None,'TBF0',{gly:(48+fszv-tens7*10,9,sx,68,0,0)}))
A_N='Carlito';B_N='Caladea'
cur='TBF0'; 
on('TBF0',(None,'TBF1',{sx:124}))
for i,(a_,b_) in enumerate(zip(A_N,B_N)):
    e=S(f'TBF{i+1}')
    on(f'TBF{i+1}',(None,f'TBF{i+2}' if i<6 else 'HALT',{gly:(net.gate(as_x(ord(b_)),ffn)+net.gate(as_x(ord(a_)),e-net.and_(e,ffn)),9,sx,68,0,0),sx:sx+adv}))
# ---- buttons ----
net.group('ribbon actions')
e=S('BTN'); B=net.decode(btn,56,e)
rules=[]
for i in range(1,7): rules.append((B[i],'FMTS',{fm:i}))
for i in range(8): rules.append((B[7+i],'FMTS',{fm:7,fcol:i}))
rules+= [(B[15],'SETAL',{alv:0}),(B[16],'SETAL',{alv:1}),(B[17],'SETAL',{alv:2}),(B[18],'SETAL',{alv:3}),(B[19],'SETLI',{alv:1}),(B[20],'SETLI',{alv:2})]
PRE=[0,7,3+3*256,1+3*256+16]
for i,p in enumerate(PRE): rules.append((B[21+i],'PRE',{fm:8,fpre:p}))
rules+=[(B[25],'RD0',{mode:1,field:0}),(B[26],'RD0',{mode:2,field:0}),(B[27],'UNDO',None),(B[28],'REDO',None)]
for i in range(6): rules.append((B[29+i],'UI',{tab:i,clip0:0,clip1:0}))
rules+=[(B[36],'HALT',{wpaste:1}),(B[37],'COPY',None),(B[38],'CUT',None),(B[39],'RALL',None),(B[50],'SB',None)]
for i,n_ in enumerate((2,3,4)): rules.append((B[40+i],'TI0',{tin:n_,tic:0,tir:n_*n_-1,grp:grp+1}))
rules+=[(B[53],'PDF',None),(B[52],'HALT',{wpic:1}),(B[51],'RD0',{mode:5,field:0}),(B[49],'RD0',{mode:4,field:0}),(B[48],'HALT',{wopen:1}),(B[47],'SAVE',None),(B[43],'DA0',{ncol:1,di_:0}),(B[44],'DA0',{ncol:2,di_:0}),(B[45],'TC0',{ti_:0,grp:grp+1}),(B[46],'RD0',{mode:3})]
on('BTN',*rules,(None,'HALT',None))
on('DA0',(net.ge(di_,npar,S('DA0')),'RD0',{lc:1,dfrom:0}),(None,'DA1',{r1:as_x(PT)+di_}))
on('DA1',(None,'DA0',{w1:(R1+DIRTY,1),di_:di_+1}))
# table of contents: copy headings into paragraphs at the caret
on('TC0',(None,'TC1',{r1:cb+LEN}))
e=S('TC1'); on('TC1',(net.ge(ti_,npar,e),'AFTER_ED',None),(None,'TC2',{r1:as_x(PT)+ti_}))
on('TC2',(None,'TC3',{tbase:R1,r1:R1+LEN,r2:R1+1024,rl:R1+SAVE}))
TH0,TH1=3+3*256,1+3*256+16
e=S('TC3'); ish=net.and_(net.step(R1),net.or_(net.eq(R2,TH0,e),net.eq(R2,TH1,e)))
on('TC3',(ish,'TC4',{tl_:R1,tk_:0,tpg:rl.out[2]}),(None,'TC1',{ti_:ti_+1}))
e=S('TC4'); on('TC4',(net.ge(tk_,tl_,e),'TCP',{tk_:0}),(None,'TC5',{r1:tbase+tk_}))
on('TC5',(None,'INS',{ins_ch:R1,ins_st:0,tk_:tk_+1,oret.r:oret.id('TC4')}))
# page number after dots
def tc_ins(st,ch,nx): on(st,(None,'INS',{ins_ch:ch,ins_st:0,oret.r:oret.id(nx)}))
tc_ins('TCP',46,'TCQ');tc_ins('TCQ',46,'TCR');tc_ins('TCR',46,'TCS');tc_ins('TCS',32,'TCD')
e=S('TCD'); bg_=net.gate(tpg,e); hd_=X()
for t in range(1,4): hd_=hd_+net.step(bg_-100*t+0.5)
rm=bg_-hd_*100; tn_=X()
for t in range(1,10): tn_=tn_+net.step(rm-10*t+0.5)
on('TCD',(net.step(bg_-99.5),'INS',{ins_ch:48+hd_,ins_st:0,oret.r:oret.id('TCE')}),(None,'TCE',None))
e=S('TCE'); bg2=net.gate(tpg,e); h2=X()
for t in range(1,4): h2=h2+net.step(bg2-100*t+0.5)
rm2=bg2-h2*100; t2=X()
for t in range(1,10): t2=t2+net.step(rm2-10*t+0.5)
on('TCE',(net.step(bg2-9.5),'INS',{ins_ch:48+t2,ins_st:0,tdig:rm2-t2*10,oret.r:oret.id('TCF')}),(None,'TCF',{tdig:rm2-t2*10}))
on('TCF',(None,'INS',{ins_ch:as_x(48)+tdig,ins_st:0,oret.r:oret.id('TCG')}))
e=S('TCG'); adj=net.gt(ti_,cp,e)
on('TCG',(None,'SPLIT',{ti_:ti_+1+adj,oret.r:oret.id('TC1')}))
on('TI0',(None,'SPLIT',{oret.r:oret.id('TI1'),tip:cp+1}))
e=S('TI1'); wr=net.ge(tic+1,tin,e)
fsm.set(tic,net.and_(e,wr),0); fsm.set(tic,e-net.and_(e,wr),tic+1)
on('TI1',(net.step(tir),'SPLIT',{w1:(cb+2062,tin),w2:(cb+2063,tic),w3:(cb+DIRTY,1),tir:tir-1,oret.r:oret.id('TI1')}),
 (None,'SPLIT',{w1:(cb+2062,tin),w2:(cb+2063,tic),w3:(cb+DIRTY,1),oret.r:oret.id('TI2')}))
on('TI2',(None,'J0',{jp:tip,jo:0,jret.r:jret.id('AFTER_ED')}))
on('PRE',(None,'FMTS',{ap:cp,ao:0,co:clen,grp:grp+1}))
on('RALL',(None,'FN1',{fp:0,fo:0,wrap:0,rall:1,ap:0,ao:0,cp:0,co:0,grp:grp+1}))
on('SB',(net.lt(evb,thumb,S('SB')),'RD0',{scroll:net.relu(scroll-500),autos:0}),(None,'RD0',{scroll:scroll+500,autos:0}))
# ---- .docx writer: zip container, CRC32 and XML are all produced here ----
net.group('docx writer')
import docx_tpl,zlib
FILE=1000000
fw=WPort(1); fw2=WPort(1); fp=R(); em_en=Bus(net); em_b=Bus(net); savel=R(); crci=Bus(net)
fw.drive(em_en.w,(as_x(FILE)+fp,em_b.w))
fsm.set(fp,em_en.w,fp+1)
# CRC32 is linear over GF(2): each next bit is the parity of a fixed subset of bits.
def crc_next(c,b):
    return (zlib.crc32(bytes([b]),c^0xffffffff)^0xffffffff)&0xffffffff
ens=em_en.w; bb=net.bits(em_b.w,8,ens)
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
STATIC,HOLE_AT,HEAD=docx_tpl.static_part()
XMLH,XMLT=docx_tpl.xml_parts()
on('SAVE',(None,'SV0',{fp:0}))
lit('SV0',STATIC,'SVB')
docstart=len(STATIC)
crci.lin(S('SVB'))
lit('SVB',XMLH,'SVP')
fsm.set(pi,S('SAVE'),0)
e=S('SVP'); on('SVP',(net.ge(pi,npar,e),'SVT',None),(None,'SVa',{r1:as_x(PT)+pi}))
on('SVa',(None,'SVm',{pbs:R1,rl:R1+LEN}))
on('SVm',(None,'SVj',{plen_:rl.out[0],al:rl.out[2],off:0,lsf:99999}))
lit('SVj',docx_tpl.P_OPEN,'SVa2')
e=S('SVa2'); h_=net.decode(al,4,e)
on('SVa2',(h_[1],'SVc1',None),(h_[2],'SVc2',None),(h_[3],'SVc3',None),(None,'SVc0',None))
lit('SVc0',b'left','SVd');lit('SVc1',b'center','SVd');lit('SVc2',b'right','SVd');lit('SVc3',b'both','SVd')
lit('SVd',docx_tpl.P_MID,'SVC')
e=S('SVC'); on('SVC',(net.ge(off,plen_,e),'SVe',None),(None,'SVr',{r1:pbs+off,r2:pbs+1024+off}))
e=S('SVr'); chg=net.step(net.step(R2-lsf)+net.step(lsf-R2)); 
on('SVr',(chg,'SVx',{ins_ch:R1,ins_st:R2}),(None,'SVch',{ins_ch:R1,ins_st:R2}))
e=S('SVx'); first=net.eq(lsf,99999,e)
on('SVx',(first,'SVo',None),(None,'SVcl',None))
lit('SVcl',docx_tpl.R_CLOSE,'SVo')
lit('SVo',b'<w:r><w:rPr>','SVs')
# decode the run style with a dedicated style decoder
sv_in=Bus(net); sv_en=Bus(net); SV=style_decode(sv_in.w,sv_en.w)
for st_ in ('SVs','SVs1','SVs2','SVs3','SVs4','SVs5','SVs6','SVs7','SVz','SVz2','SVz3'):
    sv_en.lin(S(st_)); sv_in.add(S(st_),ins_st)
szh_=net.decode(SV['size'],11,S('SVz')); 
on('SVs',(SV['font'],'SVfa',None),(None,'SVs1',None)); lit('SVfa',b'<w:rFonts w:ascii="Caladea" w:hAnsi="Caladea"/>','SVs1')
on('SVs1',(SV['bold'],'SVb',None),(None,'SVs2',None)); lit('SVb',b'<w:b/>','SVs2')
on('SVs2',(SV['ital'],'SVi',None),(None,'SVs4',None)); lit('SVi',b'<w:i/>','SVs4')
colh_=net.decode(SV['color'],8,S('SVs4'))
on('SVs4',*[(colh_[j],f'SVk{j}',None) for j in range(1,8)],(None,'SVs5',None))
for j in range(1,8):
    r_,g__,b__=PAL_F[j]; lit(f'SVk{j}',('<w:color w:val="%02X%02X%02X"/>'%(r_,g__,b__)).encode(),'SVs5')
on('SVs5',(None,'SVs6',None))
lit('SVs6',b'<w:sz w:val="','SVz')
hp=X()
for si,h in enumerate(szh_): hp=hp+h*(rom.PTS[si]*2)
tn8=X()
for t in range(1,8): tn8=tn8+net.step(net.gate(hp,S('SVz'))-10*t+0.5)
szv=R()
on('SVz',(None,'SVz2',{szv:hp}))
e=S('SVz2'); tn2=X(); base2=net.gate(szv,e)
for t in range(1,8): tn2=tn2+net.step(base2-10*t+0.5)
em_en.lin(e); em_b.add(e,48+tn2)
on('SVz2',(None,'SVz3',None))
e=S('SVz3'); tn3=X(); base3=net.gate(szv,e)
for t in range(1,8): tn3=tn3+net.step(base3-10*t+0.5)
em_en.lin(e); em_b.add(e,48+base3-tn3*10)
lit('SVz4',b'"/>','SVs3')
on('SVz3',(None,'SVz4',None))
on('SVs3',(SV['und'],'SVu',None),(None,'SVs7',None)); lit('SVu',b'<w:u w:val="single"/>','SVs7')
lit('SVs7',b'</w:rPr><w:t xml:space="preserve">','SVrs')
on('SVrs',(None,'SVch',{lsf:ins_st}))
e=S('SVch'); amp=net.eq(ins_ch,38,e);ltc=net.eq(ins_ch,60,e);gtc=net.eq(ins_ch,62,e); other=e-amp-ltc-gtc
em_en.lin(other); em_b.add(other,ins_ch)
on('SVch',(amp,'SVa_',{off:off+1}),(ltc,'SVl_',{off:off+1}),(gtc,'SVg_',{off:off+1}),(None,'SVC',{off:off+1}))
lit('SVa_',b'&amp;','SVC');lit('SVl_',b'&lt;','SVC');lit('SVg_',b'&gt;','SVC')
e=S('SVe'); on('SVe',(net.eq(lsf,99999,e),'SVe2',None),(None,'SVe1',None))
lit('SVe1',docx_tpl.R_CLOSE,'SVe2')
lit('SVe2',b'</w:p>','SVn')
on('SVn',(None,'SVP',{pi:pi+1}))
lit('SVT',XMLT,'SVF')
# freeze the CRC and size, patch the local header, write the central directory
frozen=[R() for _ in crcr]; dsize=R(); cdst=R()
crcL=X();crcH=X()
for j,c_ in enumerate(crcr):
    if j<16: crcL=crcL+c_*(1<<j)
    else: crcH=crcH+c_*(1<<(j-16))
cfL=R();cfH=R()
e=S('SVF')
fsm.set(cfL,e,as_x(65535)-crcL);fsm.set(cfH,e,as_x(65535)-crcH); fsm.set(dsize,e,fp-docstart); fsm.set(cdst,e,fp)
on('SVF',(None,'SVF1',None))
def le_bytes(val,en,n=4):
    bt=net.bits(val,8*n,en)
    return [sum((bt[8*k+i]*(1<<i) for i in range(8)),X()) for k in range(n)]
def crc_b(ix,en):
    return le_bytes(cfL if ix<2 else cfH,en,2)[ix%2]
on('SVF1',(None,'SVF2',{fw2:(as_x(FILE+HOLE_AT),crc_b(0,S('SVF1')))}))
seq_=['SVF2','SVF3','SVF4','SVF5','SVF6','SVF7','SVF8','SVF9']
vals=[]
for i in range(1,4): vals.append((HOLE_AT+i,'c',i))
for i in range(4): vals.append((HOLE_AT+4+i,'s',i))
for i in range(4): vals.append((HOLE_AT+8+i,'s',i))
cur_='SVF2'
for n_,(ad,kd,ix) in enumerate(vals):
    ee2=S(cur_); bv_=crc_b(ix,ee2) if kd=='c' else le_bytes(dsize,ee2)[ix]
    nx=f'SVG{n_}'
    on(cur_,(None,nx,{fw2:(as_x(FILE+ad),bv_)})); cur_=nx
# central directory
cdirs=docx_tpl.central(docstart)
on(cur_,(None,'CD0',None))
prev='CD0'; cdl=R()
for n_,part in enumerate(cdirs):
    nx=f'CDp{n_}'
    if not isinstance(part,bytes) and part==('end',0):
        fsm.set(cdl,S(prev),fp-cdst-12); on(prev,(None,prev+'w',None)); prev=prev+'w'
    if isinstance(part,bytes):
        lit(prev,part,nx)
    else:
        kd,ix=part; ee3=S(prev)
        if kd=='end':
            bv=le_bytes(cdl,ee3)
        else:
            bv=None
        vb=bv[ix] if kd=='end' else (crc_b(ix,ee3) if kd=='c' else le_bytes({'s':dsize,'o':cdst}[kd],ee3)[ix])
        em_en.lin(ee3); em_b.add(ee3,vb); on(prev,(None,nx,None))
    prev=nx
on(prev,(None,'HALT',{savel:fp}))
saveout=Bus(net); saveout.add(S('HALT'),savel); fsm.set(savel,S('HALT'),0)
exec(open('pdf_write.py').read())
# ---- .docx reader: zip walk, inflate (canonical Huffman), LZ77 and XML matching ----
net.group('docx reader')
exec(open('docx_read.py').read())
# ---- ribbon drawn by a chain of tokens; each token's outgoing weights hold one draw item ----
net.group('ribbon display list')
import ui
ui.build(net,fsm,rA,g_en,g_ch,g_st,g_x,g_y,g_draw,fg,bg,YB,tab,S)
# ---- finish ----
for r in (jret,oret,dret,wret,bret,gret,hret,cret,iret,nret): r.gen()
fsm.finish()
def nid(x):
    if isinstance(x,X): return next(iter(x.t))
    return x
wvl_data=[wlog,wln,wvl,w1,w2,w3,w4,fw,fw2,wo,imw,wl_i,xw]
for p in wvl_data: net.aligned.append([nid(b.w) for b in p.d])
for b in (dat_s,dat_l): net.aligned.append([nid(w_) for w_ in b])
c=net.compile(); new=c['new']
print('neurons',c['n'],'layers',c['L'],file=sys.stderr)
names={new[next(iter(v_.t))]:k_ for k_,v_ in list(globals().items()) if isinstance(v_,X) and len(v_.t)==1}
json.dump(names,open('../build/names.json','w'))
json.dump({str(new[next(iter(r_.t))]):k_ for k_,(r_,_) in fsm.states.items()},open('../build/states.json','w'))
pr=[]
for p in net.ports:
    r=p.rec(None)
    if r[0] in (1,2):
        d=r[3]
        pr+=[r[0],new[nid(r[1])],new[nid(r[2])],new[nid(d)],r[4],new[nid(r[5])] if r[5] is not None else -1]
    elif r[0]==3: pr+=[3]+[new[nid(q)] for q in r[1:]]
    elif r[0]==4: pr+=[4,new[nid(r[1])],new[nid(r[2])],new[nid(r[3])],new[nid(r[4][0])],r[5],r[6],new[nid(r[7])],new[nid(r[8])]]
    elif r[0]==6: pr+=[6]+[new[nid(q)] for q in r[1:]]
    elif r[0]==5: pr+=[5,new[nid(r[1])],new[nid(r[2])],new[nid(r[3])]]
import numpy as np
n=c['n'];ost=np.zeros(n+1,dtype=np.int32);
dst=[];ww_=[]
for i in range(n):
    o=sorted(c['out'][i]); ost[i+1]=len(o)      # sizes, ascending targets, delta coded
    prev=0
    for d,w_ in o: dst.append(d-prev);prev=d;ww_.append(w_)
ist=np.zeros(n+1,dtype=np.int32);isr=[];iww=[]
for i in range(n):
    ist[i+1]=len(c['lazy'][i])
    for j_,w_ in c['lazy'][i]: isr.append(j_);iww.append(w_)
wtab=sorted(set(ww_)|set(iww)); wix={w_:k_ for k_,w_ in enumerate(wtab)}; assert len(wtab)<65536
hdr=dict(pdfout=new[nid(pdfout.w)],ni=len(isr),nt=len(wtab),wpic=new[nid(picout.w)],wopen=new[nid(openout.w)],file=FILE,saveout=new[nid(saveout.w)],n=n,e=len(dst),L=c['L'],nports=len(pr),bank=BANK,halt=new[nid(halt.w)],timer=new[nid(timer.w)],clipout=new[nid(clipout.w)],wantp=new[nid(wantp.w)],
 ev=[new[nid(q)] for q in (ev_kind,ev_a,ev_b,ev_c)],cb=CB,cb2=CB2,init=[[new[i],v] for i,v in net.init.items()],
 bank_init=[[LEN+SLOT0,0],[DIRTY+SLOT0,1],[PT,SLOT0],[SLOT0+SAVE,112],[SLOT0+SAVE+1,16],[SLOT0+SAVE+2,1]])
import os
dd=np.array(dst,dtype=np.int32)
raw=b''.join([ist.tobytes(),np.array(isr,dtype=np.int32).tobytes(),np.array([wix[w_] for w_ in iww],dtype=np.uint16).tobytes(),np.array(c['act'],dtype=np.uint8).tobytes(),np.array(c['bias'],dtype=np.float64).tobytes(),ost.tobytes(),dd.tobytes(),np.array([wix[w_] for w_ in ww_],dtype=np.uint16).tobytes(),np.array(c['lstart'],dtype=np.int32).tobytes(),np.array(pr,dtype=np.int32).tobytes(),np.array(wtab,dtype=np.float64).tobytes()])
h=json.dumps(hdr,separators=(',',':')).encode()
blob=struct.pack('<I',len(h))+h+b'\0'*((4-(len(h)+4)%4)%4)+raw
gz=gzip.compress(blob,9)
open('../build/net.bin.gz','wb').write(gz)
prov={k:len(v) for k,v in net.groups.items()}
json.dump(dict(neurons=n,edges=len(dst),layers=c['L'],groups=prov,states=len(fsm.states)),open('../build/provenance.json','w'),indent=1)
print('lazy',len(isr),'edges',len(dst),'raw',len(blob),'gz',len(gz),file=sys.stderr)
