"""Compiles openly licensed font outlines into per-glyph weight vectors, advances and kerning."""
import io,glob,math,os,unicodedata
import numpy as np
GAMMA=0.8
from fontTools.ttLib import TTFont
from PIL import Image,ImageDraw,ImageFont
PTS=[11,12,14,16,18,20,24,28,36,9,10,8,7]   # size index 0 is the default 11 pt
SW,SH,LW,LH=24,28,60,64                     # small and large patch sizes
FAM=['carlito','caladea']
_root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _path(fam,sub,w,st): return f'{_root}/fonts/{fam}/package/files/{fam}-{sub}-{w}-{st}.woff'
def _load(fam,sub,w,st):
    f=TTFont(_path(fam,sub,w,st)); f.flavor=None; b=io.BytesIO(); f.save(b); return b.getvalue()
CACHE={}
def _bytes(fi,bold,ital,sub='latin'):
    k=(fi,bold,ital,sub)
    if k not in CACHE: CACHE[k]=_load(FAM[fi],sub,700 if bold else 400,'italic' if ital else 'normal')
    return CACHE[k]
TT={}
def tt(fi,bold,ital,sub='latin'):
    k=(fi,bold,ital,sub)
    if k not in TT: TT[k]=TTFont(io.BytesIO(_bytes(fi,bold,ital,sub)))
    return TT[k]
def font(fi,bold,ital,px,sub='latin'): return ImageFont.truetype(io.BytesIO(_bytes(fi,bold,ital,sub)),px)
def small(si): return PTS[si]<=14
def metrics(si,fi=0):
    px=round(PTS[si]*96/72); f=font(fi,0,0,px); a,d=f.getmetrics()
    return a,round((a+d)*1.08)
# ---- character repertoire. Cells hold Windows-1252 style internal codes ----
# 32..126 ASCII, 127 list bullet, 128..159 the cp1252 punctuation block, 160..255 Latin-1.
def cp1252(code):
    if code==127: return '•'
    try: return bytes([code]).decode('cp1252')
    except UnicodeDecodeError: return None
CODES=[c for c in range(32,256) if cp1252(c) is not None and cp1252(c) not in ('\x7f','\x81','\x8d','\x8f','\x90','\x9d')]
UNI_MAP={ord(cp1252(c)):c for c in range(128,160) if cp1252(c)}      # unicode point to internal code
def _src(fi,bold,ital,ch):
    "Which font file has this character: the Latin subset first, then Latin extended."
    if ord(ch) in tt(fi,bold,ital).getBestCmap(): return 'latin'
    if ord(ch) in tt(fi,bold,ital,'latin-ext').getBestCmap(): return 'latin-ext'
    return None
OS=8                                        # oversampling for unhinted ink
def _xsnap(fi,bold,ital,px):
    "Vertical scale that puts the x-height on a pixel row. Horizontal positions stay exact."
    f=tt(fi,bold,ital); xh=f['OS/2'].sxHeight/f['head'].unitsPerEm*px
    return max(1,round(xh))/xh if xh>0 else 1.0
def _render(fi,bold,ital,si,ch):
    """Ink from the unhinted outline: drawn 8x large (hinting is then negligible), box filtered.
    Hinted ink at text sizes is narrower than the advance, which left holes after letters such as m."""
    px=round(PTS[si]*96/72); W,H=(SW,SH) if small(si) else (LW,LH)
    sub=_src(fi,bold,ital,ch)
    if sub is None: return {}
    f=font(fi,bold,ital,px*OS,sub); a,_=font(fi,bold,ital,px).getmetrics()
    im=Image.new('L',(W*OS,(H+8)*OS),0); d=ImageDraw.Draw(im); d.text((2*OS,(a+4)*OS),ch,font=f,fill=255,anchor='ls')
    A=np.asarray(im,dtype=np.float64)
    ys=_xsnap(fi,bold,ital,px)
    # row r of the output covers these oversampled rows, measured from the baseline
    base=(a+4)*OS; rows=np.arange((H+8)*OS); yo=np.floor((base+(rows-base+0.5)*ys)/OS-4).astype(int)
    out_={}
    acc=np.zeros((H,W)); cnt=np.zeros(H)
    cols=A.reshape((H+8)*OS,W,OS).mean(axis=2)
    for r_,yy in enumerate(yo):
        if 0<=yy<H: acc[yy]+=cols[r_]; cnt[yy]+=1
    for y in range(H):
        if cnt[y]==0: continue
        for x in range(W):
            c=acc[y,x]/cnt[y]/255
            if c<=0: continue
            q=round(min(1,c**GAMMA)*15)
            if q: out_[(x,y)]=q
    return out_
def adv_em(fi,bold,ital,code):
    "Unhinted advance in ems, read from the font tables."
    ch=cp1252(code)
    sub=_src(fi,bold,ital,ch)
    if sub is None: return adv_em(fi,bold,ital,32)
    f=tt(fi,bold,ital,sub); g=f.getBestCmap()[ord(ch)]
    return f['hmtx'][g][0]/f['head'].unitsPerEm
def glyph(fi,bold,ital,si,code):
    """Returns (rounded advance, [(x,y,level 1..15)]) with the baseline at the size's ascent."""
    ch=cp1252(code); P=_render(fi,bold,ital,si,ch)
    px=round(PTS[si]*96/72)
    return round(adv_em(fi,bold,ital,code)*px),[(x,y,q) for (x,y),q in P.items()]
def base_of(code):
    "An accented letter is compiled as its ASCII base letter plus a shared delta."
    ch=cp1252(code)
    d=unicodedata.normalize('NFD',ch)
    if len(d)>1 and ord(d[0])<127: return ord(d[0])
    return None
def face_program(fi,bold,ital,si):
    """Glyph ink as a list of (codes that fire this group, [(x,y,signed level)]).
    Base letters fire for themselves and their accented forms. Each accented form then only
    adds the pixels that differ. Identical deltas (same accent, same width) share one group."""
    img={c:_render(fi,bold,ital,si,cp1252(c)) for c in CODES}
    groups={}
    for c in CODES:
        b=base_of(c)
        if b is None or b not in img:
            key=('g',c); groups[key]=[[c],[(x,y,q) for (x,y),q in img[c].items()]]
    for c in CODES:
        b=base_of(c)
        if b is None or b not in img: continue
        groups[('g',b)][0].append(c)
        A,B=img[c],img[b]; d=[]
        for k in set(A)|set(B):
            v=A.get(k,0)-B.get(k,0)
            if abs(v)>1 or (k in A)!=(k in B): d.append((k[0],k[1],v))
        key=('d',tuple(sorted(d)))
        if key in groups: groups[key][0].append(c)
        else: groups[key]=[[c],d]
    return [v for v in groups.values() if v[1]]
def kern_pairs(thr=0.014):
    """Pair adjustments from each face's GPOS kern feature, in ems, kept when above thr.
    Returns {(left code,right code):{(fi,bold,ital):ems}}."""
    out={}
    rep=[c for c in CODES if c<127 or c>=160]
    for fi in range(2):
      for bo in range(2):
        for it in range(2):
            f=tt(fi,bo,it); cm=f.getBestCmap(); upm=f['head'].unitsPerEm
            g2c={}
            for c in rep:
                g=cm.get(ord(cp1252(c)))
                if g: g2c.setdefault(g,[]).append(c)
            if 'GPOS' not in f: continue
            tb=f['GPOS'].table; seen=set()
            for fr in tb.FeatureList.FeatureRecord:
                if fr.FeatureTag!='kern': continue
                for li in fr.Feature.LookupListIndex:
                    if li in seen: continue
                    seen.add(li); pairs={}
                    for st in tb.LookupList.Lookup[li].SubTable:
                        st=getattr(st,'ExtSubTable',st)
                        if not hasattr(st,'Coverage'): continue
                        cov=st.Coverage.glyphs
                        if st.Format==1:
                            for gl,ps in zip(cov,st.PairSet):
                                for r in ps.PairValueRecord:
                                    v=getattr(r.Value1,'XAdvance',0) if r.Value1 else 0
                                    pairs.setdefault((gl,r.SecondGlyph),v)
                        else:
                            c1d=st.ClassDef1.classDefs; c2d=st.ClassDef2.classDefs
                            for gl in cov:
                                if gl not in g2c: continue
                                rec=st.Class1Record[c1d.get(gl,0)].Class2Record
                                for g2 in g2c:
                                    r=rec[c2d.get(g2,0)]
                                    v=getattr(r.Value1,'XAdvance',0) if r.Value1 else 0
                                    pairs.setdefault((gl,g2),v)
                    for (a,b),v in pairs.items():
                        if v and a in g2c and b in g2c and abs(v)/upm>=thr:
                            for ca in g2c[a]:
                                if ca>=127: continue
                                for cb in g2c[b]:
                                    if cb>=127: continue
                                    out.setdefault((ca,cb),{})[(fi,bo,it)]=v/upm
    return out
