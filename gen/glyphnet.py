"""A directly programmed glyph network. Every weight below is written from an open font outline
or from a font metric. There is no training, fitting, search, or transform basis.

One tick computes one sample line of one glyph. The sample line height y is a register.
  glyph register -> binary tree over the glyph's outline heights -> the outline edges that cross y.
  edge neuron: its weights are the edge's line coefficients, x = X0*s + m*(y - Y(Y0)) + stem shift.
  slot wires: edges whose height spans are disjoint share a wire, chosen by interval colouring.
  ramp bank: R_q = relu(q - x), so a pixel's share of a crossing is R_(q+1) - R_q (analytic in x).
  signed sum = winding. A clamp gives coverage. K sample lines accumulate into one pixel row.
Size scales through the s input. Vertical snapping is a piecewise linear height map whose knots are
rounded font metrics. Horizontal snapping shifts edges by the rounded offsets of their nearest stems."""
import math,sys
from fontTools.pens.basePen import BasePen
from nn import *
import rom
PAD=16.0      # crossing wires carry x+PAD so that gates (which clamp at zero) can pass them
YP=128.0      # the height register carries y+YP for the same reason
DP=8.0        # stem shift registers carry shift+DP
X0PATCH=2     # glyph origin column inside a patch, the same as the bitmap ROM
SW,LW=rom.SW,rom.LW
QUANT=4.0     # outline vertices are kept to a quarter of a font unit
TOL_PX,TOL_PPEM=0.1,48   # flatness: a tenth of a pixel at the largest size, 36 pt
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
def merge(c,tol):
    "Removes a vertex that lies on the line through its neighbours, within tol."
    q=[]
    for p in c:
        p=(round(p[0]*QUANT)/QUANT,round(p[1]*QUANT)/QUANT)
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
_OC={}
def contours(fi,bo,it,code,tol=None):
    "Closed flattened contours of one glyph in em units (y up), with no search or fit."
    key=(fi,bo,it,code,tol)
    if key in _OC: return _OC[key]
    ch=rom.cp1252(code); sub=rom._src(fi,bo,it,ch); out=[]
    if sub:
        f=rom.tt(fi,bo,it,sub); gs=f.getGlyphSet(); upm=f['head'].unitsPerEm; n=f.getBestCmap()[ord(ch)]
        t_=(tol if tol is not None else tol_em())*upm
        p=Flat(gs,t_); gs[n].draw(p)
        for c in p.cs:
            m=merge(c,t_/8)
            if len(m)>=3: out.append([(a/upm,b/upm) for a,b in m])
    _OC[key]=out; return out
def edges(cs):
    "Non horizontal edges as (Y0,X0,Y1,X1,sign), Y0<Y1. Sign is +1 for upward, the left side of ink in a TrueType outline."
    E=[]
    for c in cs:
        for i,a in enumerate(c):
            b=c[(i+1)%len(c)]
            if a[1]==b[1]: continue
            E.append((a[1],a[0],b[1],b[0],1) if a[1]<b[1] else (b[1],b[0],a[1],a[0],-1))
    return E
def _ymax(fi,bo,it,ch,flat=None):
    cs=contours(fi,bo,it,ord(ch)); ys=[p[1] for c in cs for p in c]; return max(ys),min(ys)
_FM={}
def face_metrics(fi,bo,it):
    "Heights the snapping knots are written from, read off the outlines of named letters."
    k=(fi,bo,it)
    if k in _FM: return _FM[k]
    xh=_ymax(fi,bo,it,'x')[0]; cap=_ymax(fi,bo,it,'H')[0]; asc=_ymax(fi,bo,it,'d')[0]; des=_ymax(fi,bo,it,'p')[1]
    xo=max(_ymax(fi,bo,it,'o')[0]-xh,0); co=max(_ymax(fi,bo,it,'O')[0]-cap,0); bo_=max(-_ymax(fi,bo,it,'o')[1],0)
    # vertical stem width from the lower case l: its widest near vertical span
    xs=[p[0] for c in contours(fi,bo,it,ord('l')) for p in c]; ws=max(xs)-min(xs)
    if it==0:
        # a serif l is wider than its stem, so read the width at mid height through the crossings
        h=asc/2; cr=[]
        for Y0,X0,Y1,X1,_s in edges(contours(fi,bo,it,ord('l'))):
            if Y0<=h<Y1: cr.append(X0+(h-Y0)*(X1-X0)/(Y1-Y0))
        if len(cr)>=2: ws=max(cr)-min(cr)
    m=dict(xh=xh,cap=cap,asc=max(asc,cap),des=des,xo=xo,co=co,bo=bo_,stem=ws); _FM[k]=m; return m
def stems(fi,bo,it,code,E=None):
    """Vertical stems found by a fixed rule: a run of near vertical upward edges paired with the nearest
    near vertical downward run, with a width near the face's standard stem. Italics have none."""
    if it: return []
    fm=face_metrics(fi,bo,it); cs=contours(fi,bo,it,code); runs=[]
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
            t=round((xm-a[0])/(b[0]-a[0])*16)/16
            return [(u_,e_,w_) for u_,e_,w_ in ((a[1],a[2],1-t),(b[1],b[2],t)) if w_]
    return []
def q_slope(m):
    "Keeps 11 significant bits so that slopes share the engine's weight dictionary."
    if m==0: return 0.0
    e=math.floor(math.log2(abs(m))); return round(m/2**(e-11))*2**(e-11)
def miter(cs,bold):
    """Vertex offsets for one outward offset of 1 em along the edge normals. Each vertex moves to where its
    two offset lines meet, so slopes never change. A TrueType outer contour runs clockwise, so outward is left of travel."""
    V={}
    for c in cs:
        n=len(c)
        for i,b in enumerate(c):
            a,d=c[i-1],c[(i+1)%n]
            ux,uy=b[0]-a[0],b[1]-a[1]; vx,vy=d[0]-b[0],d[1]-b[1]
            lu=math.hypot(ux,uy) or 1; lv=math.hypot(vx,vy) or 1
            n1=(-uy/lu,ux/lu); n2=(-vy/lv,vx/lv)
            hx,hy=n1[0]+n2[0],n1[1]+n2[1]; k=1+n1[0]*n2[0]+n1[1]*n2[1]
            k=max(k,0.5)    # miter limit
            V[b]=(hx/k,hy/k)
    return V
class GlyphNet:
    def __init__(g,faces,codes,K=4,synth=False,xsnap=True,wround=False,tol=None,xh_round=0.5):
        g.faces=faces; g.codes=codes; g.K=K; g.synth=synth; g.xsnap=xsnap; g.wround=wround; g.tol=tol; g.xh_round=xh_round
        g.net=net=Net(); g.stats=dict(edges=0,knots=0,stems=0,flat=0); g.per={}
        g._build()
    def _slots(g,E):
        "Interval colouring: sweep by lower height, take the lowest free slot of the edge's direction."
        res=[None]*len(E); free={1:[],-1:[]}; mg=0.06 if g.synth else 0.0   # offset edges need a margin
        for i in sorted(range(len(E)),key=lambda i:(E[i][0],E[i][1])):
            Y0,_,Y1,_,sg=E[i]; L=free[sg]
            for k,end in enumerate(L):
                if end+mg<=Y0: L[k]=Y1; res[i]=k; break
            else: L.append(Y1); res[i]=len(L)-1
        return res,len(free[1]),len(free[-1])
    def _build(g):
        net=g.net; K=g.K; ONE=net.ONE
        net.group('controls')
        I=g.I=dict(start=net.input(),ch=net.input(),face=net.input(),s=net.input(),y0=net.input(),rows=net.input(),addr=net.input(),cells=net.input(),snapy=net.input(),snapx=net.input(),large=net.input(),bold=net.input(),slant=net.input())
        st=I['start']
        done=net.wire()
        def latch(val,load=st,clear=done):
            r=net.reg(); net.rec(r,r-net.relu(r+clear*M-M)+net.gate(val,load)); return r
        s=g.s=latch(I['s']); yr=g.yr=net.reg(); rows=net.reg(); addr=net.reg(); cells=latch(I['cells']); large=latch(I['large'])
        snapx=I['snapx']; snapy=I['snapy']
        # one hot face and a binary tree over the character, walked only on the start tick
        fh=net.decode(I['face'],len(g.faces),st,hot=True) if len(g.faces)>1 else [st]
        chv=net.relu(I['ch']-32+1+st*M-M); chok=net.step(chv); bits=net.bits(chv-1,8,chok)
        leaf={}
        def tnode(p,sel,neg=False): return net.step(p*M-M+((ONE-sel) if neg else sel)-0.5)
        def tree(root,fi):
            S=set(c-32 for c in g.codes)
            def walk(node,lo,k):
                if k<0: leaf[fi,lo+32]=node; return
                mid=lo+(1<<k)
                if any(lo<=i<mid for i in S): walk(tnode(node,bits[k],True),lo,k-1)
                if any(mid<=i<mid+(1<<k) for i in S): walk(tnode(node,bits[k]),mid,k-1)
            walk(root,0,7)
        for fi,_f in enumerate(g.faces): tree(tnode(fh[fi],chok),fi)
        # snapping knots: rounded font metrics, computed once per glyph and held in registers
        net.group('snapping layer')
        def per_face(name):
            e=X()
            for fi,f in enumerate(g.faces):
                z=face_metrics(*f)[name] if isinstance(name,str) else name(face_metrics(*f))
                e=e+net.gate(I['s']*z,fh[fi])
            return e
        sy=net.and_(st,snapy); ny=net.step(st*M-M+(ONE-snapy)-0.5)
        def floor_(v,en):
            rem=net.gate(v,en); o=X()
            for k in reversed(range(8)):
                b=net.step(rem-2**k+1e-7); o=o+b*2**k; rem=rem-b*2**k
            return o
        def knot(name,add=None,off=0.5):
            v=per_face(name); ov=per_face(add) if add else None
            return floor_(v+off,sy)+net.gate(v+(ov if add else 0),ny)
        kn=g.kn=dict(D=latch(knot(lambda m:-m['des'])),XH=latch(knot('xh',off=g.xh_round)),CAP=latch(knot('cap')),ASC=latch(knot('asc')))
        def over(name): return latch(net.gate(per_face(name),ny))
        kn['Bo']=over('bo'); kn['XHo']=over('xo'); kn['CAPo']=over('co')
        # stem units: a stem's rounded position, then its edge shifts, held in registers
        net.group('stem units')
        NU=4; bc=[net.wire() for _ in range(NU)]; bh=[net.wire() for _ in range(NU)]; uen=[net.wire() for _ in range(NU)]
        Wv=per_face('stem')
        sx=net.and_(st,snapx) if g.xsnap else None
        W=None
        if g.xsnap:
            if g.wround: W=1+net.relu(floor_(Wv+0.5,sx)-1)
            else: W=Wv+X()
        g.dL=[];g.dR=[]
        for u in range(NU):
            if not g.xsnap: g.dL.append(None);g.dR.append(None);continue
            en=net.step(uen[u])
            wg=net.gate(W,en)
            fv=floor_(bc[u]-wg*0.5+16.5,en)
            Lp=fv-en*16
            base=st*DP
            g.dL.append(latch(st*DP+net.relu(Lp-bc[u]+bh[u]+en*4+en*M-M)-en*4))
            g.dR.append(latch(st*DP+net.relu(Lp+wg-bc[u]-bh[u]+en*4+en*M-M)-en*4))
        net.group('row sequencer')
        net.rec(yr,yr-net.relu(yr+done*M-M)+net.gate(I['y0']+YP-0.5/K,st))
        ph=[net.reg() for _ in range(K)]; first=latch(st,st,ph[0])
        wr=net.step(ph[0]*M-M+0.5-first)
        rpos=net.step(rows-0.5)
        dn=net.step(wr*M-M+0.5-rows)
        net.connect(done,dn)
        net.rec(rows,rows-net.relu(rows+done*M-M)+net.gate(I['rows'],st)-net.step(ph[0]*M-M+rpos-0.5))
        net.rec(ph[0],st+ph[K-1])
        net.rec(ph[1] if K>1 else ph[0],ph[0]-dn)
        for i in range(2,K): net.rec(ph[i],ph[i-1])
        run=latch(st)
        net.rec(yr,(run-dn)*(-1.0/K))
        d2=net.reg(); net.rec(d2,dn)
        clr=net.step(wr+d2)
        net.rec(addr,addr-net.relu(addr+done*M-M)+net.gate(I['addr'],st)+net.gate(cells,wr-dn))
        # glyph programs
        net.group('glyph weights (outline edges)')
        g.sb=None;g.shear=None
        y=yr
        if g.synth:
            # one offset control: half the difference between the family's real bold and regular stems
            g.sb=latch(sum((net.gate(I['s']*((face_metrics(f[0],1,0)['stem']-face_metrics(*f)['stem'])/2),fh[fi]) for fi,f in enumerate(g.faces)),X()),net.and_(st,I['bold']))
            # one shear layer: the angle is the family's italic angle from the post table
            g.shear=X()
            for fi,f in enumerate(g.faces):
                t=math.tan(math.radians(-rom.tt(f[0],0,1)['post'].italicAngle))
                en=latch(fh[fi],net.and_(st,I['slant']))
                g.shear=g.shear+net.relu(y*t+en*M-M)-en*(YP*t)
        prog={}
        for fi,f in enumerate(g.faces):
            fm=face_metrics(*f)
            for c in g.codes:
                prog[fi,c]=g._glyph_prep(f,c)
        nu=max([1]+[p['nup'] for p in prog.values()]); nd=max([1]+[p['ndn'] for p in prog.values()])
        g.nup,g.ndn=nu,nd
        slots={1:[net.wire() for _ in range(nu)],-1:[net.wire() for _ in range(nd)]}
        for (fi,c),P in prog.items():
            g._glyph(fi,c,P,leaf.get((fi,c),X()),slots,kn,s,y,bc,bh,uen,sx,done)
        # ramp bank, shared by all glyphs and written once
        net.group('ramp bank')
        w=[X() for _ in range(LW)]; nbank=0
        for sg,L in slots.items():
            for xk in L:
                en=net.step(xk); enl=None
                R=[]
                for q in range(LW+1):
                    if q==SW+1: enl=net.and_(en,large)
                    e_=en if q<=SW else enl
                    R.append(net.relu(e_*M-M+(q-X0PATCH+PAD)-xk)); nbank+=1
                for p in range(LW): w[p]=w[p]+(R[p+1]-R[p])*sg
        g.nbank=nbank
        net.group('coverage')
        ac=[net.reg() for _ in range(LW)]    # consecutive registers: the write port reads them as a block
        g.ac=ac
        for p in range(LW):
            wp=net.wire(); net.connect(wp,w[p])
            cov=net.relu(wp)-net.relu(wp-1)
            net.rec(ac[p],ac[p]-net.relu(ac[p]+clr*M-M)+cov*(1.0/K))
        g.wr=wr;g.done=done;g.cells=cells;g.addr=addr
        class P_:
            def rec(s_,_): return [1,wr,addr,ac[0],LW,cells]
        net.ports.append(P_())
    def _glyph_prep(g,f,c):
        cs=contours(*f,c,g.tol); E=edges(cs)
        ys=sorted(set(y for e in E for y in (e[0],e[2])))
        sl,nu,nd=g._slots(E)
        return dict(cs=cs,E=E,ys=ys,sl=sl,nup=nu,ndn=nd,st=stems(*f,c) if g.xsnap else [],fm=face_metrics(*f))
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
                t=round((Y-a)/(b-a)*8192)/8192
                return ka*(1-t)+kb*t
    def _glyph(g,fi,c,P,lf,slots,kn,s,y,bc,bh,uen,sx,done):
        net=g.net; E=P['E']; ys=P['ys']; fm=P['fm']
        st=P['st']
        if not lf.t: return
        # stem constants go on the shared stem unit wires, once per draw
        if st:
            lfs=net.step(lf*M-M+g.I['snapx']-0.5)
            for u,(l,r,_h) in enumerate(st):
                net.connect(uen[u],lfs); net.connect(bc[u],net.gate(g.I['s']*((l+r)/2),lfs)); net.connect(bh[u],net.gate(g.I['s']*((r-l)/2),lfs))
            g.stats['stems']+=len(st)
        gr=net.reg(); net.rec(gr,gr-net.relu(gr+done*M-M)+lf)
        if not E: return
        V=None
        if g.synth: V=miter(P['cs'],True)
        # dy neurons: one per distinct outline height, read lazily by the tree and the edges
        keys=sorted(set((e[0],(0 if not V else V[(e[1],e[0])][1])) for e in E)|set((e[2],(0 if not V else V[(e[3],e[2])][1])) for e in E))
        dy={}
        for k in keys:
            n=net.wire(); ex=y-g._ymap(fm,k[0],s,kn)
            if g.synth: ex=ex-g.sb*k[1]
            net.connect(n,ex); dy[k]=n-YP
        ys=sorted(set(keys),key=lambda k:k[0]+0.02*k[1])
        idx={k:i for i,k in enumerate(ys)}
        # binary tree over the height intervals
        lo=net.step(gr*M-M+dy[ys[0]]); rt=net.step(lo*M-M-dy[ys[-1]])
        nodes={}
        def build(a,b,en):
            nodes[a,b]=en
            if b-a<=1: return
            m=(a+b)//2
            up=net.step(en*M-M+dy[ys[m]]); dn_=net.step(en-up-0.5)
            build(m,b,up); build(a,m,dn_)
        build(0,len(ys)-1,rt)
        attach={}
        def place(i0,i1,a,b,i):
            if i0<=a and b<=i1: attach.setdefault((a,b),[]).append(i); return
            m=(a+b)//2
            if i0<m: place(i0,i1,a,m,i)
            if i1>m: place(i0,i1,m,b,i)
        for i,e in enumerate(E):
            if g.synth: k0=(e[0],V[(e[1],e[0])][1]);k1=(e[2],V[(e[3],e[2])][1])
            else: k0=(e[0],0);k1=(e[2],0)
            place(idx[k0],idx[k1],0,len(ys)-1,i)
        en_of=[X() for _ in E]
        for ab,L in attach.items():
            for i in L: en_of[i]=en_of[i]+nodes[ab]
        for i,e in enumerate(E):
            Y0,X0,Y1,X1,sg=e
            m=q_slope((X1-X0)/(Y1-Y0))
            k0=(Y0,0 if not V else V[(X0,Y0)][1])
            ex=s*(round(X0*8192)/8192)+dy[k0]*m
            if g.synth:
                ex=ex+g.sb*V[(X0,Y0)][0]+g.shear
            for u,side,wt in _shift_weights((X0+X1)/2,st):
                r_=(g.dL if side==0 else g.dR)[u]
                ex=ex+(r_-DP)*wt
            ex=ex+PAD
            n=net.relu(ex+en_of[i]*M-M)
            net.connect(slots[sg][P['sl'][i]],n)
        g.stats['edges']+=len(E); g.stats['knots']+=len(keys)
        g.per[fi,c]=dict(edges=len(E),knots=len(keys),stems=len(st))
    def save(g,path):
        "Writes the same file format the shipping network uses, so the real engine runs it."
        import json,struct,gzip,collections,numpy as np
        net=g.net; c=net.compile(); new=c['new']; nid=lambda x:next(iter(x.t))
        pr=[]
        for p in net.ports:
            r=p.rec(None); pr+=[1,new[nid(r[1])],new[nid(r[2])],new[nid(r[3])],r[4],new[nid(r[5])]]
        n=c['n']; ost=np.zeros(n+1,dtype=np.int32); dst=[];ww=[]
        for i in range(n):
            o=sorted(c['out'][i]); ost[i+1]=len(o); prev=0
            for d,w in o: dst.append(d-prev);prev=d;ww.append(w)
        ist=np.zeros(n+1,dtype=np.int32);isr=[];iww=[]
        for i in range(n):
            ist[i+1]=len(c['lazy'][i])
            for j,w in c['lazy'][i]: isr.append(j);iww.append(w)
        wc=collections.Counter(ww)+collections.Counter(iww)
        wtab=sorted(wc,key=lambda w:(-wc[w],w)); wix={w:k for k,w in enumerate(wtab)}
        assert len(wtab)<65536,len(wtab)
        def pack(v,big):
            o=bytearray()
            for x in v:
                if x<255:o.append(x)
                else:o.append(255);o+=int(x).to_bytes(big,'little')
            return bytes(o)
        dz=pack(dst,4);wz=pack([wix[w] for w in ww],2)
        I={k:new[nid(v)] for k,v in g.I.items()}
        hdr=dict(n=n,e=len(dst),L=c['L'],nports=len(pr),bank=4000000,ni=len(isr),nt=len(wtab),dn=len(dz),wn=len(wz),init=[[new[i],v] for i,v in net.init.items()],
            bank_init=[],dbg=dict(y=new[nid(g.yr)],wr=new[nid(g.wr)],kn=new[nid(g.kn['CAP'])],ac=new[nid(g.ac[3])]),I=I,halt=new[nid(g.done)],K=g.K)
        raw=b''.join([ist.tobytes(),np.array(isr,dtype=np.int32).tobytes(),np.array([wix[w] for w in iww],dtype=np.uint16).tobytes(),np.array(c['act'],dtype=np.uint8).tobytes(),np.array(c['bias'],dtype=np.float64).tobytes(),ost.tobytes(),dz,wz,np.array(c['lstart'],dtype=np.int32).tobytes(),np.array(pr,dtype=np.int32).tobytes(),np.array(wtab,dtype=np.float64).tobytes()])
        h=json.dumps(hdr,separators=(',',':')).encode()
        blob=struct.pack('<I',len(h))+h+b'\0'*((4-(len(h)+4)%4)%4)+raw
        gz=gzip.compress(blob,6); open(path,'wb').write(gz)
        return dict(neurons=n,synapses=len(dst),lazy=len(isr),weights=len(dst)+len(isr),uniq=len(wtab),raw=len(blob),gz=len(gz),layers=c['L'],groups={k:len(v) for k,v in net.groups.items()},**g.stats,nup=g.nup,ndn=g.ndn,nbank=g.nbank)
ASCII=list(range(32,127))
ALLFACES=lambda fi:[(fi,b,i) for b in (0,1) for i in (0,1)]

def cache_blit_net(W,H,path):
    """The cache hit path as a real network: a tag read, a block read of stored coverage, and the patch port.
    Tag table at bank cell TAG+key. A zero tag is a miss, which would start the generator above."""
    import json,struct,gzip,numpy as np
    net=Net(); key=net.input(); go=net.input(); px=net.input(); py=net.input()
    tagv=net.input(); cov=[net.reg() for _ in range(W*H)]   # read port output cells, consecutive
    xr=net.reg(); yr=net.reg(); net.rec(xr,net.gate(px,go)); net.rec(yr,net.gate(py,go))
    x2=net.reg(); y2=net.reg(); net.rec(x2,net.gate(xr,net.step(tagv))); net.rec(y2,net.gate(yr,net.step(tagv)))
    hit=net.step(tagv); hit2=net.reg(); net.rec(hit2,hit)
    d=[net.wire() for _ in range(4*W*H)]
    for i in range(W*H):
        m=net.step(cov[i]); c=cov[i]
        for k in range(3): net.connect(d[4*i+k],(m-c)*255)
        net.connect(d[4*i+3],m)
    pen=net.wire(); net.connect(pen,hit2); done=net.step(hit2)
    c=net.compile(); new=c['new']; nid=lambda x:next(iter(x.t))
    n=c['n']; pr=[2,new[nid(go)],new[nid(key)],new[nid(tagv)],1,-1, 2,new[nid(hit)],new[nid(tagv)],new[nid(cov[0])],W*H,-1, 4,new[nid(pen)],new[nid(x2)],new[nid(y2)],new[nid(d[0])],W,H,-1,-1]
    ost=np.zeros(n+1,dtype=np.int32);dst=[];ww=[];ist=np.zeros(n+1,dtype=np.int32);isr=[];iww=[]
    for i in range(n):
        o=sorted(c['out'][i]);ost[i+1]=len(o);p=0
        for t,w in o:dst.append(t-p);p=t;ww.append(w)
        ist[i+1]=len(c['lazy'][i])
        for j,w in c['lazy'][i]:isr.append(j);iww.append(w)
    wt=sorted(set(ww)|set(iww));wx={w:k for k,w in enumerate(wt)}
    def pack(v,b):
        o=bytearray()
        for x in v:
            if x<255:o.append(x)
            else:o.append(255);o+=int(x).to_bytes(b,'little')
        return bytes(o)
    dz=pack(dst,4);wz=pack([wx[w] for w in ww],2)
    hdr=dict(n=n,e=len(dst),L=c['L'],nports=len(pr),bank=4000000,ni=len(isr),nt=len(wt),dn=len(dz),wn=len(wz),init=[[new[i],v] for i,v in net.init.items()],key=new[nid(key)],go=new[nid(go)],px=new[nid(px)],py=new[nid(py)],halt=new[nid(done)])
    raw=b''.join([ist.tobytes(),np.array(isr,dtype=np.int32).tobytes(),np.array([wx[w] for w in iww],dtype=np.uint16).tobytes(),np.array(c['act'],dtype=np.uint8).tobytes(),np.array(c['bias'],dtype=np.float64).tobytes(),ost.tobytes(),dz,wz,np.array(c['lstart'],dtype=np.int32).tobytes(),np.array(pr,dtype=np.int32).tobytes(),np.array(wt,dtype=np.float64).tobytes()])
    h=json.dumps(hdr,separators=(',',':')).encode()
    open(path,'wb').write(gzip.compress(struct.pack('<I',len(h))+h+b'\0'*((4-(len(h)+4)%4)%4)+raw,6))
