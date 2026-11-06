"""The glyph unit: a directly programmed network that draws text. Every weight below is written from an open font
outline or from a font metric. There is no training, fitting, search, or transform basis.

It is a separate clock domain inside the application network, entered through a call port. While it runs, the paint state
is stalled. One call draws one glyph:
  tag read: key = face, size, code. The tag holds a block address in the store and the block header holds the key,
    so a stale tag after a flush fails the compare, and a flush is only a reset of the bump pointer.
  hit path: one pixel row per tick from the store, through one row plane (coverage and color to pixel), to the patch port.
  miss path: the generator below writes the glyph to the store, then the tag is read again.
Generator, one tick per sample line:
  glyph register -> binary tree over the glyph's outline heights -> the outline edges that cross y.
  edge neuron: its weights are the edge's line coefficients, x = X0*s + m*(y - Y(Y0)) + stem shift.
  slot wires: edges whose height spans are disjoint share a wire, chosen by interval colouring.
  ramp bank: R_q = relu(q - x), so a pixel's share of a crossing is R_(q+1) - R_q (analytic in x).
  signed sum = winding. A clamp gives coverage. K sample lines accumulate into one pixel row.
Size scales through the s input. Vertical snapping is a piecewise linear height map whose knots are rounded font metrics.
Horizontal snapping (edges shifted by the rounded offsets of their nearest stems) exists here, but no face in the current font table uses it.
An accented letter fires its base letter's program and its accent's program, using the font's own composite data."""
import math
from fontTools.pens.basePen import BasePen
from nn import *
import rom
PAD=64.0      # crossing wires carry x+PAD so that gates (which clamp at zero) can pass them
YP=256.0      # the height register carries y+YP for the same reason
DP=8.0        # stem shift registers carry shift+DP
AO=256.0      # accent shift registers carry shift+AO
HDR=7         # store block header: key+1, rows, cells, x origin, top, offset+1 of its pixel record, generation of that record
RECB=68000000; RECE=75000000; RECW=32; RECH=32     # pixel records of small glyphs drawn black on white
OFF=64        # offset of header values that may be negative
GRID_EM=1024  # outline vertices are kept on a grid of 1/1024 em (the same weights recur, and the file compresses)
TOL_PX,TOL_PPEM=0.15,48   # flatness: 0.15 pixel at 36 pt
K=4           # sample lines per pixel row
def tol_em(): return TOL_PX/TOL_PPEM
class Flat(BasePen):
    def __init__(s,gs,tol):
        super().__init__(gs); s.tol=tol; s.cs=[]
    def _moveTo(s,p): s.cs.append([p])
    def _lineTo(s,p): s.cs[-1].append(p)
    def _qCurveToOne(s,c,p):
        a=s._getCurrentPoint(); dx=a[0]-2*c[0]+p[0]; dy=a[1]-2*c[1]+p[1]
        n=max(1,math.ceil(math.sqrt(math.hypot(dx,dy)/(4*s.tol))))
        for i in range(1,n+1):
            t=i/n; u=1-t
            s.cs[-1].append((u*u*a[0]+2*u*t*c[0]+t*t*p[0],u*u*a[1]+2*u*t*c[1]+t*t*p[1]))
    def _curveToOne(s,c1,c2,p):
        a=s._getCurrentPoint()
        d=max(math.hypot(a[0]-2*c1[0]+c2[0],a[1]-2*c1[1]+c2[1]),math.hypot(c1[0]-2*c2[0]+p[0],c1[1]-2*c2[1]+p[1]))
        n=max(1,math.ceil(math.sqrt(3*d/(4*s.tol))))
        for i in range(1,n+1):
            t=i/n; u=1-t
            s.cs[-1].append(tuple(u**3*a[k]+3*u*u*t*c1[k]+3*u*t*t*c2[k]+t**3*p[k] for k in (0,1)))
    def _closePath(s): pass
    def _endPath(s): pass
def merge(c,tol,quant):
    "Removes a vertex that lies on the line through its neighbours, within tol."
    q=[]
    for p in c:
        p=(round(p[0]*quant)/quant,round(p[1]*quant)/quant)
        if not q or q[-1]!=p: q.append(p)
    if len(q)>1 and q[0]==q[-1]: q.pop()
    ch=True
    while ch and len(q)>2:
        ch=False; o=[]; n=len(q); i=0
        while i<n:
            a,b,d=o[-1] if o else q[-1],q[i],q[(i+1)%n]
            ux,uy=d[0]-a[0],d[1]-a[1]; L=math.hypot(ux,uy)
            if L>0 and abs(ux*(b[1]-a[1])-uy*(b[0]-a[0]))/L<tol and 0<=(ux*(b[0]-a[0])+uy*(b[1]-a[1]))<=L*L:
                ch=True
                if i+1<n: o.append(d)
                i+=2
            else: o.append(b); i+=1
        q=o
    return q
_NC={}
def named(fi,bo,it,sub,name):
    "Closed flattened contours of one font glyph in em units (y up)."
    key=(fi,bo,it,sub,name)
    if key in _NC: return _NC[key]
    f=rom.tt(fi,bo,it,sub); gs=f.getGlyphSet(); upm=f['head'].unitsPerEm; t_=tol_em()*upm
    p=Flat(gs,t_); gs[name].draw(p); out=[]
    for c in p.cs:
        m=merge(c,t_/8,GRID_EM/upm)
        if len(m)>=3: out.append([(a/upm,b/upm) for a,b in m])
    _NC[key]=out; return out
def src(fi,bo,it,code):
    ch=rom.cp1252(code)
    if ch is None: return None
    sub=rom._src(fi,bo,it,ch)
    return (sub,rom.tt(fi,bo,it,sub).getBestCmap()[ord(ch)]) if sub else None
def contours(fi,bo,it,code):
    s_=src(fi,bo,it,code)
    return named(fi,bo,it,*s_) if s_ else []
def edges(cs):
    "Non horizontal edges as (Y0,X0,Y1,X1,sign), Y0<Y1. Sign is +1 for upward, the left side of ink in a TrueType outline."
    E=[]
    for c in cs:
        for i,a in enumerate(c):
            b=c[(i+1)%len(c)]
            if a[1]==b[1]: continue
            E.append((a[1],a[0],b[1],b[0],1) if a[1]<b[1] else (b[1],b[0],a[1],a[0],-1))
    return E
EXTTAG=(1<<30,0); PFM={}; XO=4096    # glyph x arrives lifted by XO: a page wider than the window draws to the left of it
def _ymax(fi,bo,it,ch):
    cs=contours(fi,bo,it,ord(ch)); ys=[p[1] for c in cs for p in c]; return (max(ys),min(ys)) if ys else (0.0,0.0)
_FM={}
def face_metrics(fi,bo,it):
    "Heights the snapping knots are written from, read off the outlines of named letters."
    k=(fi,bo,it)
    if k in _FM: return _FM[k]
    xh=_ymax(fi,bo,it,'x')[0]; cap=_ymax(fi,bo,it,'H')[0]; asc=_ymax(fi,bo,it,'d')[0]; des=_ymax(fi,bo,it,'p')[1]
    xo=max(_ymax(fi,bo,it,'o')[0]-xh,0); co=max(_ymax(fi,bo,it,'O')[0]-cap,0); bo_=max(-_ymax(fi,bo,it,'o')[1],0)
    # vertical stem width from the lower case l: its widest near vertical span
    xs=[p[0] for c in contours(fi,bo,it,ord('l')) for p in c]; ws=(max(xs)-min(xs)) if xs else 0.0
    if it==0:
        # a serif l is wider than its stem, so read the width at mid height through the crossings
        h=asc/2; cr=[]
        for Y0,X0,Y1,X1,_s in edges(contours(fi,bo,it,ord('l'))):
            if Y0<=h<Y1: cr.append(X0+(h-Y0)*(X1-X0)/(Y1-Y0))
        if len(cr)>=2: ws=max(cr)-min(cr)
    m=dict(xh=xh,cap=cap,asc=max(asc,cap),des=des,xo=xo,co=co,bo=bo_,stem=ws); _FM[k]=m; return m
def stems(fi,bo,it,cs):
    """Vertical stems found by a fixed rule: a run of near vertical upward edges paired with the nearest
    near vertical downward run, with a width near the face's standard stem. Italics have none."""
    if it: return []
    fm=face_metrics(fi,bo,it); runs=[]
    for c in cs:
        n=len(c); seg=[]
        for i in range(n):
            a,b=c[i],c[(i+1)%n]; dx,dy=b[0]-a[0],b[1]-a[1]
            seg.append((1 if dy>0 else -1) if dy!=0 and abs(dx)<=0.3*abs(dy) else 0)
        i0=next((i for i in range(n) if seg[i]!=seg[i-1]),None)
        if i0 is None: continue
        i=0
        while i<n:
            j=(i0+i)%n; sg=seg[j]; ln=1
            while i+ln<n and seg[(i0+i+ln)%n]==sg: ln+=1
            if sg:
                pts=[c[(i0+i+q)%n] for q in range(ln+1)]; ys=[p[1] for p in pts]; xs=[p[0] for p in pts]
                if max(ys)-min(ys)>=0.05: runs.append((sg,min(xs) if sg>0 else max(xs),min(ys),max(ys)))
            i+=ln
    out=[]
    for sg,x,y0,y1 in sorted(r for r in runs if r[0]>0):
        best=None
        for sg2,x2,y2,y3 in runs:
            if sg2>0 or x2<=x: continue
            ov=min(y1,y3)-max(y0,y2)
            if ov<0.3*min(y1-y0,y3-y2): continue
            if best is None or x2<best: best=x2
        if best is None: continue
        w=best-x
        if 0.6*fm['stem']<=w<=1.5*fm['stem']: out.append((x,best,y1-y0))
    out.sort(); keep=[]
    for st in out:
        if keep and st[0]<keep[-1][1]:     # overlapping in x: the taller stem wins
            if st[2]>keep[-1][2]: keep[-1]=st
            continue
        keep.append(st)
    if len(keep)>4: keep=sorted(sorted(keep,key=lambda q:-q[2])[:4])
    return keep
def _shift_weights(xm,st):
    "Which stem shift registers move an edge at em x position xm, and by what share. Returns [(unit,0 or 1 for left or right edge,weight)]."
    if not st: return []
    pts=[]
    for u,(l,r,_h) in enumerate(st): pts+=[(l,u,0),(r,u,1)]
    if xm<=pts[0][0]: return [(pts[0][1],pts[0][2],1.0)]
    if xm>=pts[-1][0]: return [(pts[-1][1],pts[-1][2],1.0)]
    for a,b in zip(pts,pts[1:]):
        if a[0]<=xm<=b[0] and b[0]>a[0]:
            t=round((xm-a[0])/(b[0]-a[0])*8)/8
            return [(u_,e_,w_) for u_,e_,w_ in ((a[1],a[2],1-t),(b[1],b[2],t)) if w_]
    return []
SLOPE_BITS=9
def q_slope(m):
    "Keeps a fixed number of significant bits so that slopes share the engine's weight dictionary."
    if m==0: return 0.0
    e=math.floor(math.log2(abs(m))); return round(m/2**(e-SLOPE_BITS))*2**(e-SLOPE_BITS)
GRID_X=GRID_EM
def structure(fi,bo,it,codes):
    """How each code of one face is made, from the font's own composite data: {code:[(program key,dx,dy)]}.
    Two components without a transform, the first in place, make base + accent. Anything else is drawn whole.
    Programs used as a second component form the accent group: they take their position from shift registers."""
    S={}
    for c in codes:
        s_=src(fi,bo,it,c)
        if not s_: continue
        sub,name=s_; f=rom.tt(fi,bo,it,sub); g=f['glyf'][name]; upm=f['head'].unitsPerEm
        comp=getattr(g,'components',None) if g.isComposite() else None
        if comp and len(comp)==2 and not any(hasattr(q,'transform') for q in comp) and comp[0].x==0 and comp[0].y==0 and not f['glyf'][comp[0].glyphName].isComposite() and not f['glyf'][comp[1].glyphName].isComposite():
            S[c]=[((sub,comp[0].glyphName),0.0,0.0),((sub,comp[1].glyphName),comp[1].x/upm,comp[1].y/upm)]
        else: S[c]=[((sub,name),0.0,0.0)]
    acc={p[1][0] for p in S.values() if len(p)==2}
    # a program cannot be both: a base that is also someone's accent makes that code whole
    for c,p in list(S.items()):
        if len(p)==2 and p[0][0] in acc:
            s_=src(fi,bo,it,c); S[c]=[(s_,0.0,0.0)]
    acc={p[1][0] for p in S.values() if len(p)==2}
    return S,acc
class GlyphUnit:
    def __init__(g,net,faces,codes,pseudo,LW,TAG,STORE,STORE_END,clip,palF,palB,ONE,patch_cls,sprite_cls):
        """faces: list of (fi,bo,it). codes: real codes. pseudo: {face index:{code:(contours,raw)}} shapes that are not font glyphs."""
        g.net=net; g.faces=faces; g.codes=codes; g.pseudo=pseudo; g.LW=LW; g.TAG=TAG; g.STORE=STORE; g.STORE_END=STORE_END; g.clip=clip
        g.palF=palF; g.palB=palB; g.patch_cls=patch_cls; g.sprite_cls=sprite_cls
        g.stats=dict(edges=0,knots=0,stems=0,programs=0,accent_programs=0); g.per={}
        net.domain(1); net.group('glyph unit')
        g._build()
        net.domain(0)
    def _slots(g,E):
        "Interval colouring: sweep by lower height, take the lowest free slot of the edge's direction."
        res=[None]*len(E); free={1:[],-1:[]}
        for i in sorted(range(len(E)),key=lambda i:(E[i][0],E[i][1])):
            Y0,_,Y1,_,sg=E[i]; L=free[sg]
            for k,end in enumerate(L):
                if end<=Y0: L[k]=Y1; res[i]=k; break
            else: L.append(Y1); res[i]=len(L)-1
        return res,len(free[1]),len(free[-1])
    def _build(g):
        net=g.net; ONE=net.ONE; LW=g.LW
        # ---- arguments, valid on the go tick only ----
        A=g.A=dict(go=net.input(),ch=net.input(),face=net.input(),sz=net.input(),ppem=net.input(),pt=net.input(),x=net.input(),y=net.input(),fg=net.input(),bg=net.input(),nc=net.input(),fc=net.input())
        go=A['go']
        fin=net.wire()
        def L0(val,load,clear): 
            r=net.reg(); net.rec(r,r-net.relu(r+clear*M-M)+net.gate(val,load)); return r
        def L(val,load=go): return L0(val,load,fin)
        Lch=L(A['ch']);Lface=L(A['face']);Lsz=L(A['sz']);Lppem=L(A['ppem']);Lpt=L(A['pt']);Lx=L(A['x']);Ly=L(A['y']);Lfg=L(A['fg']);Lbg=L(A['bg']);Lnc=L(A['nc']);Lfc=L(A['fc'])
        # ---- tag read ----
        retry=net.reg(); s0=net.reg(); s1=net.reg(); net.rec(s0,go+retry); net.rec(s1,s0)
        g.FK=rom.NSZ*256
        g.key=Lface*g.FK+Lsz*256+Lch
        _xf,_xt=EXTTAG; _xd=_xt-g.TAG-_xf*g.FK; g.tagaddr=lambda k_,en_: net.gate(k_+g.TAG,en_)+net.gate(Lface*0+_xd,net.step(en_*M-M+Lface-_xf+0.5))
        kw=net.wire(); net.connect(kw,g.tagaddr(g.key,s0))
        tagout=net.input(1+HDR); tag,H=tagout[0],tagout[1:]
        rd=_TagRead(s0,kw,tag,g.STORE,1+HDR); net.ports.append(rd); rd.dom=1
        kl=net.gate(g.key+1,s1)          # the block must carry this key
        hit=net.step(s1-net.step(kl-H[0]-0.5)-net.step(H[0]-kl-0.5)-0.5)
        miss=net.step(s1-hit-0.5)
        # ---- hit path ----
        rowsz=net.step(net.gate(H[1],hit)-0.5)
        # A small glyph drawn black on white before: its pixels were recorded off the row plane, so one read and one patch draw it, with no row loop and no plane.
        recg=net.reg()
        fast_=net.wire(); fnc_=net.wire()
        fs_=net.wire(); blk=net.and_(hit,rowsz,net.step(fast_+fs_),ONE-fnc_,net.step(H[5]-0.5),net.ge(H[6],recg,hit),net.ge(recg,H[6],hit))
        start=net.and_(hit,rowsz,ONE-blk); empty=hit-net.and_(hit,rowsz)
        brun=net.reg(); brows=net.reg(); bcells=L(H[2],start)
        baddr=net.reg(); bpy=net.reg(); bwr=net.reg(); blast=net.reg()
        lastt=net.step(brun*M-M+1.5-brows)     # one row left
        net.rec(brun,brun-lastt+start)
        net.rec(brows,brows-brun+net.gate(H[1],start))
        net.rec(baddr,baddr-net.relu(baddr+fin*M-M)+net.gate(tag+g.STORE+HDR,start)+net.gate(bcells,brun))
        bpx=L(Lx-H[3]+OFF+OFF,start)
        net.rec(bpy,bpy-net.relu(bpy+fin*M-M)+net.gate(Ly-H[4]+OFF,start)+bwr-blast)
        net.rec(bwr,brun); net.rec(blast,lastt)
        blk1=net.reg(); net.rec(blk1,blk)
        net.connect(fin,net.step(blast+empty+blk1))
        g.fin=fin
        rowcov=net.input(LW) if LW>1 else [net.input()]
        rr=_RowRead(brun,baddr,rowcov[0],LW,bcells); net.ports.append(rr); rr.dom=1
        # ---- colour: one line per channel bit of the selected palette entries, held during the draw ----
        sg=net.reg(); s1g=net.reg(); net.rec(sg,go); net.rec(s1g,sg)      # first pass only; a retry after a miss loads nothing twice
        fcu=net.step(Lfc); fgb=net.and_(net.eq(Lfg,1,sg),ONE-fcu)
        fast=L(net.and_(fgb,net.eq(Lbg,1,sg)),sg); fsel=L(net.and_(fgb,net.eq(Lbg,2,sg)),sg)
        bgw=L(net.eq(Lbg,1,sg),sg); net.connect(fast_,fast); net.connect(fs_,fsel); net.connect(fnc_,Lnc)   # selected text takes the same record: on the selection color the darker pixel wins, as it does for overlapping letters
        slow0=net.and_(s1g,ONE-fast,ONE-empty)
        def lines(pal,val,en_=None):
            h=net.decode(val-1,len(pal),slow0 if en_ is None else en_); out=[]
            for k in range(3):
                for b_,wt in enumerate(GRIDW):
                    e_=X()
                    for j,col in enumerate(pal):
                        if gridbits(col[k])[b_]: e_=e_+h[j]
                    if e_.t: out.append((k,wt,L(net.step(e_),slow0)))
            return out
        fce=net.and_(slow0,fcu); fxl=[]; fxv=[]; fgl=lines(g.palF,Lfg,net.and_(slow0,ONE-fcu)); bgl=lines(g.palB,Lbg)
        # an exact color: one line per bit of each channel, weighted as a binary number
        _fcb=net.bits(Lfc-1,24,fce)
        for k in range(3):
            for b_ in range(4,8): fxl.append((k,17<<(b_-4),L(_fcb[16-8*k+b_],fce)))
            fxv.append(L(sum((_fcb[16-8*k+b_]*(1<<b_) for b_ in range(8)),X()),fce))
        # ---- row plane ----
        data=[net.wire() for _ in range(4*LW)]
        nonw=ONE-fast
        for i in range(LW):
            c=rowcov[i]; m=net.step(c)
            o=[(m-c)*255]*3
            nw=net.step(m*M-M+nonw-0.5)
            sl=net.step(nw*M-M+fsel-0.5); slow=net.step(nw*M-M+(ONE-fsel)-0.5)
            cs=net.relu(sl*M-M+m-c)
            for k in range(3): o[k]=o[k]+cs*(g.palB[1][k]-255)
            slb=net.step(slow*M-M+(ONE-bgw)-0.5)   # on white the base term above is already the background, so its lines rest
            ic=net.relu(slb*M-M+m-c)
            for k in range(3): o[k]=o[k]-ic*255
            slz=net.step(slow*M-M+(ONE-fcu)-0.5)   # the palette's lines rest for an exact color, whose own wake instead
            for k,wt,ln in fgl: o[k]=o[k]+net.relu(slz*M-M+c+ln-1)*wt
            # An exact color: a fully covered pixel takes the channel values as they are, three neurons; an edge pixel blends the top four bits of each.
            slx=net.step(slow*M-M+fcu-0.5); fuq=net.step(slx*M-M+c-0.9); slq=net.step(slx-fuq-0.5)
            for k in range(3): o[k]=o[k]+net.relu(fuq*M-M+fxv[k])
            for k,wt,ln in fxl: o[k]=o[k]+net.relu(slq*M-M+c+ln-1)*wt
            for k,wt,ln in bgl: o[k]=o[k]+net.relu(slb*M-M+m-c+ln-1)*wt
            for k in range(3): net.connect(data[4*i+k],o[k])
            net.connect(data[4*i+3],m)
        net.aligned.append([next(iter(w.t)) for w in data])
        px=net.wire(); py=net.wire()
        net.connect(px,net.gate(bpx,bwr)-bwr*(OFF+XO)); net.connect(py,net.gate(bpy,bwr))
        p1=g.patch_cls(net.step(bwr-Lnc*2-fast*2-0.5),px,py,data,LW,1); p2=g.sprite_cls(net.step(bwr+Lnc*2-2.5),px,py,data,LW,1); p3=g.patch_cls(net.step(bwr+fast-Lnc*2-1.5),px,py,data,LW,1); p3.kind=11
        p1.dom=1;p2.dom=1;p3.dom=1
        # ---- pixel records ----
        net.group('glyph pixel records')
        recin=g.recin=net.input(4*RECW*RECH)
        rp=net.reg(init=1.0); net.rec(recg,recg+net.step(blast*M-M+rp-(RECE-RECB-RECW*RECH*4-8)))   # the ring wraps: older records are stale by generation
        rd4=_RowRead(blk,net.gate(H[5]-1+RECB,blk),recin[0],4*RECW*RECH,net.gate(H[1]*(4*RECW),blk)); net.ports.append(rd4); rd4.dom=1
        rbx=L(Lx-H[3]+OFF+OFF,blk); rby=L(Ly-H[4]+OFF,blk)
        qx=net.wire(); qy=net.wire(); net.connect(qx,net.gate(rbx,blk1)-blk1*(OFF+XO)); net.connect(qy,net.gate(rby,blk1))
        p4=g.patch_cls(blk1,qx,qy,recin,RECW,RECH); p4.kind=11; p4.dom=1
        # a first draw records: rows are written from the row plane, then the block's header takes the record's place
        small=net.and_(start,ONE-net.step(H[1]-RECH-0.5),ONE-net.step(H[2]-RECW-0.5),fast_,ONE-fnc_)
        rcn=L(small,start); rtag=L(tag+g.STORE,start)
        rrow=net.reg(); net.rec(rrow,rrow-net.relu(rrow+fin*M-M)+net.gate(rp,start)+(bwr-blast)*(4*RECW))
        wren=net.step(bwr+rcn-1.5)
        ra_=net.wire(); net.connect(ra_,net.gate(rrow+RECB-1,wren))
        p=_Write(wren,ra_,data[0],4*RECW); net.ports.append(p); p.dom=1
        rend=net.step(blast+rcn-1.5)
        rh=[net.wire(),net.wire()]; net.connect(rh[0],net.gate(rp,rend)); net.connect(rh[1],net.gate(recg,rend)); net.aligned.append([next(iter(w.t)) for w in rh])
        rha=net.wire(); net.connect(rha,net.gate(rtag+5,rend))
        p=_Write(rend,rha,rh[0],2); net.ports.append(p); p.dom=1
        rwrap=net.step(blast*M-M+rp-(RECE-RECB-RECW*RECH*4-8))
        rcount=net.reg(); net.rec(rcount,rcount-net.relu(rcount+fin*M-M)+net.gate(H[1],start))
        net.rec(rp,rp-net.relu(rp+rwrap*M-M)+rwrap+net.gate(rcount*(4*RECW),rend))
        # ---- miss path: the generator ----
        g._generator(miss,Lch,Lface,Lppem,Lpt,g.key,retry,fin)
    def _generator(g,st,Lch,Lface,Lppem,Lpt,key,retry,fin):
        net=g.net; ONE=net.ONE; LW=g.LW
        done=net.wire(); g._doneb=net.step(done)
        haswire=net.wire(); has=net.step(haswire); run_=net.and_(st,has); nog=st-run_     # a code with no outline runs nothing
        def latch(val,load=run_,clear=done):
            r=net.reg(); net.rec(r,r-net.relu(r+clear*M-M)+net.gate(val,load)); return r
        I_s=g._sin=Lppem
        s=g.s=latch(I_s); yr=g.yr=net.reg(); rows=net.reg(); addr=net.reg(); 
        # one hot face and a binary tree over the character, walked only on the start tick
        faceidx=Lface
        NF=max(len(g.faces),max(g.pseudo)+1)
        # extended pages have a decoder of their own, so a common face does not pay for them
        _xf0=EXTTAG[0] if EXTTAG[0]<NF else NF
        stx=net.step(st*M-M+faceidx-_xf0+0.5); st0=net.step(st-stx-0.5)
        fh=net.decode(faceidx,_xf0,st0,hot=True)+(net.decode(faceidx-_xf0,NF-_xf0,stx,hot=True) if NF>_xf0 else [])
        chv=net.relu(Lch-32+1+st*M-M); chok=net.step(chv); bits=net.bits(chv-1,8,chok)
        leaf={}
        def tnode(p,sel,neg=False): return net.step(p*M-M+((ONE-sel) if neg else sel)-0.5)
        prog_codes={}
        for fi,f in enumerate(g.faces): prog_codes[fi]=list(g.codes)
        for fi,d in g.pseudo.items(): prog_codes[fi]=sorted(set(prog_codes.get(fi,[]))|set(d))
        def tree(root,fi):
            S=set(c-32 for c in prog_codes[fi])
            def walk(node,lo,k):
                if k<0: leaf[fi,lo+32]=node; return
                mid=lo+(1<<k)
                if any(lo<=i<mid for i in S): walk(tnode(node,bits[k],True),lo,k-1)
                if any(mid<=i<mid+(1<<k) for i in S): walk(tnode(node,bits[k]),mid,k-1)
            walk(root,0,7)
        for fi in range(NF): tree(tnode(fh[fi],chok),fi)
        # snapping is chosen per draw: x and y at text sizes of the humanist upright, y elsewhere up to 24 pt, none above
        net.group('snapping layer')
        snapyv=net.step(as_x(24.5)-Lpt+st*M-M)
        ny=net.step(st*M-M+(ONE-snapyv)-0.5); sy=net.step(st*M-M+snapyv-0.5)
        xrule=X()
        for fi,f in enumerate(g.faces):
            if rom.x_snap_face(*f): xrule=xrule+fh[fi]
        sx=net.and_(net.step(xrule),net.ge(Lpt,11,st),net.lt(Lpt,19,st))
        def per_face(name):
            e=X()
            for fi,f in list(enumerate(g.faces))+list(PFM.items()):
                z=face_metrics(*f)[name]
                e=e+net.gate(I_s*z,fh[fi])
            return e
        def floor_(v,en,nb=9):
            rem=net.gate(v,en); o=X()
            for k in reversed(range(nb)):
                b=net.step(rem-2**k+1e-7); o=o+b*2**k; rem=rem-b*2**k
            return o
        def knot(name,off=0.5):
            v=per_face(name)
            return floor_(v+off,sy)+net.gate(v,ny), v
        kn=g.kn={}
        v_des=X()
        for fi,f in list(enumerate(g.faces))+list(PFM.items()): v_des=v_des+net.gate(I_s*(-face_metrics(*f)['des']),fh[fi])
        kn['D']=latch(floor_(v_des+0.5,sy)+net.gate(v_des,ny))
        kxh,vxh=knot('xh'); kcap,vcap=knot('cap'); kasc,vasc=knot('asc')
        kn['XH']=latch(kxh); kn['CAP']=latch(kcap); kn['ASC']=latch(kasc)
        def over(name): return latch(net.gate(per_face(name),ny))
        kn['Bo']=over('bo'); kn['XHo']=over('xo'); kn['CAPo']=over('co')
        # ---- block geometry, one set per face, from the face's extreme outline values ----
        net.group('glyph geometry')
        ext={}
        for fi in range(NF):
            f=g.faces[fi] if fi<len(g.faces) else None; xs=[];ys=[]
            if f:
                for c in g.codes:
                    for ct in contours(*f,c):
                        xs+=[p[0] for p in ct]; ys+=[p[1] for p in ct]
            for c,(cs,_raw) in g.pseudo.get(fi,{}).items():
                for ct in cs: xs+=[p[0] for p in ct]; ys+=[p[1] for p in ct]
            ext[fi]=(min(xs),max(xs),min(ys),max(ys))
        g.ext=ext
        def fx(j):
            e=X()
            for fi in range(NF): e=e+net.gate(I_s*ext[fi][j]+OFF,fh[fi])
            return e
        T=floor_(fx(3),st)+2; B=floor_(fx(2),st)-1; Lf=floor_(fx(0),st)-2; Rt=floor_(fx(1),st)
        OX=as_x(2*OFF)-Lf
        cells=net.wire(); _c=Rt-Lf+3; net.connect(cells,_c-net.relu(_c-LW))
        rowsv=net.gate(T-B,has)
        # ---- store: bump allocation, flushed when a largest block might not fit ----
        net.group('glyph store')
        bp=net.reg(init=g.STORE+8)
        maxb=LW*220+HDR+8
        flush=net.step(st*M-M+bp-(g.STORE_END-maxb))
        a0=net.gate(bp,st-flush)+flush*(g.STORE+8)
        hw=[net.wire() for _ in range(5)]
        for w_,v_ in zip(hw,(net.gate(key+1,st),rowsv,net.gate(cells,st),net.gate(OX,st),net.gate(T,st))): net.connect(w_,v_)
        net.aligned.append([next(iter(w.t)) for w in hw])
        a0w=net.wire(); net.connect(a0w,a0)
        tagv=net.wire(); net.connect(tagv,a0-st*g.STORE); tkw=net.wire(); net.connect(tkw,g.tagaddr(key,st))
        p=_Write(st,a0w,hw[0],5); net.ports.append(p); p.dom=1
        # a new block has no record yet: two cells from the record plane, which is at rest here
        a5w=net.wire(); net.connect(a5w,a0+st*5); p=_Write(st,a5w,g.recin[0],2); net.ports.append(p); p.dom=1
        p=_Write(st,tkw,tagv,1); net.ports.append(p); p.dom=1
        g.a0=a0;
        # stem units: a stem's rounded position, then its edge shifts, held in registers
        net.group('stem units')
        NU=4; bc=[net.wire() for _ in range(NU)]; bh=[net.wire() for _ in range(NU)]; uen=[net.wire() for _ in range(NU)]
        Wv=per_face('stem')
        g.dL=[];g.dR=[]
        for u in range(NU):
            en=net.step(uen[u])
            wg=net.gate(Wv+X(),en)
            fv=floor_(bc[u]-wg*0.5+16.5,en)
            Lp=fv-en*16
            g.dL.append(latch(st*DP+net.relu(Lp-bc[u]+bh[u]+en*4+en*M-M)-en*4))
            g.dR.append(latch(st*DP+net.relu(Lp+wg-bc[u]-bh[u]+en*4+en*M-M)-en*4))
        net.group('row sequencer')
        ph=[net.reg() for _ in range(K)]; first=latch(run_,run_,ph[0])
        wr=net.step(ph[0]*M-M+0.5-first)
        rpos=net.step(rows-0.5)
        dn=net.step(wr*M-M+0.5-rows)
        net.connect(done,dn); net.connect(done,nog)
        net.rec(retry,net.step(dn+nog))
        net.rec(yr,yr-net.relu(yr+done*M-M)+net.gate(T-OFF+YP-0.5/K,run_))
        net.rec(rows,rows-net.relu(rows+done*M-M)+net.gate(rowsv,run_)-net.step(ph[0]*M-M+rpos-0.5))
        net.rec(ph[0],run_+ph[K-1])
        net.rec(ph[1],ph[0]-dn)
        for i in range(2,K): net.rec(ph[i],ph[i-1])
        runr=latch(run_,run_)
        net.rec(yr,(runr-dn)*(-1.0/K))
        d2=net.reg(); net.rec(d2,dn)
        clr=net.step(wr+d2)
        cl=latch(cells)
        net.rec(addr,addr-net.relu(addr+done*M-M)+net.gate(a0+HDR,run_)+net.gate(cl,wr-dn))
        net.rec(bp,bp-net.relu(bp+(dn+nog)*M-M)+net.gate(addr+cl,dn)+net.gate(a0+HDR,nog))
        # ---- programs ----
        net.group('glyph weights (outline edges)')
        y=yr
        ax=net.reg();ay=net.reg()
        prog={}; comp={}     # program key -> data; (fi,code) -> composition
        for fi,f in enumerate(g.faces):
            S,acc=structure(*f,g.codes)
            for c,parts in S.items():
                comp[fi,c]=parts
                for (pk,_dx,_dy) in parts:
                    k=(fi,)+pk
                    if k not in prog:
                        cs=named(*f,*pk); E=edges(cs); sl,nu,nd=g._slots(E)
                        prog[k]=dict(cs=cs,E=E,sl=sl,nup=nu,ndn=nd,acc=pk in acc,raw=False,st=stems(*f,cs) if rom.x_snap_face(*f) and pk not in acc else [],fm=face_metrics(*f),lf=net.wire())
        _same={(f,str(p_['cs'])):k_ for k_,p_ in prog.items() for f in [g.faces[k_[0]]] if not p_['acc'] and p_['cs']}
        for fi,d in g.pseudo.items():
            for c,(cs,raw) in d.items():
                # the same outline in the same face is one program: a Cyrillic A fires the Latin A's weights
                if fi in PFM and cs:
                    q_=_same.get((PFM[fi],str(cs)))
                    if q_: comp[fi,c]=[(('alias',q_),0.0,0.0)]; continue
                k=(fi,'pseudo',c); E=edges(cs); sl,nu,nd=g._slots(E)
                if fi in PFM and cs: _same[PFM[fi],str(cs)]=k
                fm=face_metrics(*g.faces[fi]) if fi<len(g.faces) else (face_metrics(*PFM[fi]) if fi in PFM else None)
                prog[k]=dict(cs=cs,E=E,sl=sl,nup=nu,ndn=nd,acc=False,raw=raw,st=[],fm=fm,lf=net.wire()); comp[fi,c]=[(('pseudo',c),0.0,0.0)]
        nu=max([1]+[p['nup'] for p in prog.values() if not p['acc']]); nd=max([1]+[p['ndn'] for p in prog.values() if not p['acc']])
        nua=max([0]+[p['nup'] for p in prog.values() if p['acc']]); nda=max([0]+[p['ndn'] for p in prog.values() if p['acc']])
        g.nup,g.ndn,g.nua,g.nda=nu,nd,nua,nda
        slots={1:[net.wire() for _ in range(nu)],-1:[net.wire() for _ in range(nd)]}; aslots={1:[net.wire() for _ in range(nua)],-1:[net.wire() for _ in range(nda)]}
        axv=X();ayv=X()
        dxh=kxh-vxh; dcap=kcap-vcap
        for (fi,c),parts in comp.items():
            lf=leaf.get((fi,c))
            if lf is None: continue
            for j,(pk,dx,dy) in enumerate(parts):
                k=pk[1] if pk[0]=='alias' else (fi,)+pk; P=prog[k]
                if P['E']: net.connect(haswire,lf)
                net.connect(P['lf'],lf)
                if j==1:
                    # the accent keeps its distance from the snapped height of its base
                    fm_=face_metrics(*g.faces[fi]); up_=max(p_[1] for c_ in P['cs'] for p_ in c_)+dy>fm_['xh']*0.8 if P['cs'] else False
                    axv=axv+net.gate(I_s*dx+AO,lf); ayv=ayv+net.gate(I_s*dy+AO,lf)
                    if up_: ayv=ayv+net.gate(dcap+8 if c<96 or 192<=c<223 else dxh+8,lf)-lf*8
                elif P['acc']:
                    axv=axv+lf*AO; ayv=ayv+lf*AO
        net.rec(ax,ax-net.relu(ax+done*M-M)+axv); net.rec(ay,ay-net.relu(ay+done*M-M)+ayv)
        for k,P in prog.items():
            if not P['E']: continue
            g._glyph(k,P,slots,aslots,kn,s,y,bc,bh,uen,sx,done,ax,ay,net.step(P['lf']))
        # ---- ramp bank, shared by all glyphs and written once ----
        net.group('ramp bank')
        # A column past the glyph's cells is never stored, so each tier of columns opens only for a glyph that wide.
        BLK=8; TIERS=[t_ for t_ in (8,16,24,32,48,64,96,128) if t_<LW]; ctier=[latch(net.step(cells-t_-0.5)) for t_ in TIERS]
        def tier_of(q): return next((i_ for i_,t_ in enumerate(TIERS) if q<=t_),len(TIERS))
        def tiers(en):
            o_=[en]
            for c_ in ctier: o_.append(net.and_(o_[-1],c_))
            return o_
        ox=latch(OX)
        w=[X() for _ in range(LW)]; nbank=0; blockfull={a_:net.wire() for a_ in range(0,LW,BLK)}
        for gp in (slots,aslots):
            for sg,L_ in gp.items():
                for xk in L_:
                    en=net.step(xk); et=tiers(en)
                    xs=net.wire(); net.connect(xs,net.relu(xk+ox+en*M-M))
                    # Blocks of columns. Left of the crossing nothing opens. Right of it every column gains the same whole unit, from one neuron. Only the block holding the crossing needs its ramps.
                    for a_ in range(0,LW,BLK):
                        b_=min(a_+BLK,LW); e_=et[tier_of(a_+1)]
                        full=net.step(e_*M-M+(a_+PAD+OFF)-xs); pe=net.and_(e_,net.step(e_*M-M+(b_+PAD+OFF)-xs),ONE-full)
                        R={q:net.relu(pe*M-M+(q+PAD+OFF)-xs) for q in range(a_+1,b_+1)}; nbank+=b_-a_
                        net.connect(blockfull[a_],full*sg)     # whole columns meet in one sum per block: edges that cancel there wake no column
                        for p_ in range(a_,b_): w[p_]=w[p_]+(R[p_+1]-R.get(p_,X()))*sg
        for a_,f_ in blockfull.items():
            for p_ in range(a_,min(a_+BLK,LW)): w[p_]=w[p_]+f_
        g.nbank=nbank
        net.group('coverage')
        ac=[net.reg() for _ in range(LW)]
        out=[net.wire() for _ in range(LW)]
        clrt=tiers(clr); wrt=tiers(wr)
        for p_ in range(LW):
            wp=net.wire(); net.connect(wp,w[p_])
            cov=net.relu(wp)-net.relu(wp-1)
            net.rec(ac[p_],ac[p_]-net.relu(ac[p_]+clrt[tier_of(p_+1)]*M-M)+cov*(1.0/K))
            # darkening curve, the same one the old rasterizer used, written as a piecewise linear map of final coverage
            a_=net.relu(ac[p_]+wrt[tier_of(p_+1)]*M-M)
            net.connect(out[p_],a_*GAMMA_K[0]-net.relu(a_-0.25)*GAMMA_K[1]-net.relu(a_-0.5)*GAMMA_K[2]-net.relu(a_-0.75)*GAMMA_K[3])
        net.aligned.append([next(iter(w_.t)) for w_ in out])
        p=_Write(wr,addr,out[0],LW,cl); net.ports.append(p); p.dom=1
    def _ymap(g,fm,Y,s,kn):
        "The height map as a linear expression over s and the knot registers. Identity when the knots are unrounded."
        xh,cap,asc,des,xo,co,bo=fm['xh'],fm['cap'],fm['asc'],fm['des'],fm['xo'],fm['co'],fm['bo']
        A=[(des,-kn['D'])]
        if bo>0: A.append((-bo,-kn['Bo']))
        A.append((0.0,X()))
        A.append((xh,kn['XH']))
        if xo>0: A.append((xh+xo,kn['XH']+kn['XHo']))
        A.append((cap,kn['CAP']))
        if co>0: A.append((cap+co,kn['CAP']+kn['CAPo']))
        if asc>cap+co: A.append((asc,kn['ASC']))
        A=[a for i,a in enumerate(A) if i==0 or a[0]>A[i-1][0]]
        if Y<=A[0][0]: return A[0][1]+s*(Y-A[0][0])
        if Y>=A[-1][0]: return A[-1][1]+s*(Y-A[-1][0])
        for (a,ka),(b,kb) in zip(A,A[1:]):
            if a<=Y<=b:
                t=round((Y-a)/(b-a)*256)/256
                return ka*(1-t)+kb*t
    def _glyph(g,k,P,slots,aslots,kn,s,y,bc,bh,uen,sx,done,ax,ay,lf):
        net=g.net; E=P['E']; fm=P['fm']; st=P['st']; accp=P['acc']; raw=P['raw'] or fm is None
        if st:
            lfs=net.step(lf*M-M+sx-0.5)
            for u,(l,r,_h) in enumerate(st):
                net.connect(uen[u],lfs); net.connect(bc[u],net.gate(g._sin*((l+r)/2),lfs)); net.connect(bh[u],net.gate(g._sin*((r-l)/2),lfs))
            g.stats['stems']+=len(st)
        gr=net.reg(); net.boolreg=getattr(net,'boolreg',set()); net.boolreg.add(next(iter(gr.t))); net.rec(gr,gr-net.and_(gr,g._doneb)+lf)   # the live program wakes its own clear, so done has no fan out to every program
        keys=sorted(set(e[0] for e in E)|set(e[2] for e in E))
        dy={}
        for yk in keys:
            n=net.wire()
            if accp: ex=y-(ay-AO)-s*yk
            elif raw: ex=y-s*yk
            else: ex=y-g._ymap(fm,yk,s,kn)
            net.connect(n,ex); dy[yk]=n-YP
        # one threshold per outline height: an edge is live between the thresholds of its two ends
        # The heights are sorted and the map keeps their order, so the rest of a group of heights is tested only once its lowest has passed.
        ge={}
        for i_,yk in enumerate(keys):
            ge[yk]=net.step((gr if i_%16==0 else ge[keys[i_-i_%16]])*M-M+dy[yk])
        sl_=aslots if accp else slots
        for i,e in enumerate(E):
            Y0,X0,Y1,X1,sg=e
            m=q_slope((X1-X0)/(Y1-Y0))
            ex=s*(round(X0*GRID_X)/GRID_X)+dy[Y0]*m
            if accp: ex=ex+ax-AO
            for u,side,wt in _shift_weights((X0+X1)/2,st):
                r_=(g.dL if side==0 else g.dR)[u]
                ex=ex+(r_-DP)*wt
            ex=ex+PAD
            net.connect(sl_[sg][P['sl'][i]],net.relu(ex+(ge[Y0]-ge[Y1])*M-M))
        g.stats['edges']+=len(E); g.stats['knots']+=len(keys); g.stats['programs']+=1; g.stats['accent_programs']+=1 if accp else 0
GAMMA_K=(1.32,0.35,0.09,0.06)
GRIDW=(136,68,34,17,5)
def gridbits(v):
    assert v%17 in (0,5),v
    return [(v//17>>(3-i))&1 for i in range(4)]+[1 if v%17==5 else 0]
class _TagRead:
    def __init__(s,en,addr,out,base,n): s.a=(en,addr,out,base,n)
    def rec(s,nm): e,a,o,b,n=s.a; return [10,e,a,o,b,-1,1,n-1]
class _RowRead:
    def __init__(s,en,addr,out,cells,ln): s.a=(en,addr,out,cells,ln)
    def rec(s,nm): e,a,o,c,l=s.a; return [2,e,a,o,c,l]
class _Write:
    def __init__(s,en,addr,data,cells,ln=None): s.a=(en,addr,data,cells,ln)
    def rec(s,nm): e,a,d,c,l=s.a; return [1,e,a,d,c,l]
