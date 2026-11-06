"""Font data the generator writes weights from: openly licensed outlines, advances and kerning."""
import io,glob,math,os,unicodedata
import numpy as np
from fontTools.ttLib import TTFont
from PIL import ImageFont
PTS=[11,12,14,16,18,20,24,28,36,9,10,8,7]   # size index 0 is the default 11 pt
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
NSZ=len(PTS)
GLW=150     # pixel columns of the glyph unit's row plane
FACES=[(fi,bo,it) for fi in range(len(FAM)) for bo in range(2) for it in range(2)]
def x_snap_face(fi,bo,it): return fi==0 and not it
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
def adv_em(fi,bold,ital,code):
    "Unhinted advance in ems, read from the font tables."
    ch=cp1252(code)
    sub=_src(fi,bold,ital,ch)
    if sub is None: return adv_em(fi,bold,ital,32)
    f=tt(fi,bold,ital,sub); g=f.getBestCmap()[ord(ch)]
    return f['hmtx'][g][0]/f['head'].unitsPerEm
def adv_px(fi,bold,ital,si,code):
    "Rounded advance at a compiled size, for layouts written at build time."
    return round(adv_em(fi,bold,ital,code)*round(PTS[si]*96/72))
def kern_pairs(thr=0.014):
    """Pair adjustments from each face's GPOS kern feature, in ems, kept when above thr.
    Returns {(left code,right code):{(fi,bold,ital):ems}}."""
    out={}
    rep=[c for c in CODES if c<127 or c>=160]
    for fi,bo,it in FACES:
        if 1:
          if 1:
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
