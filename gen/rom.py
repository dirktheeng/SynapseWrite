"""Font data the generator writes weights from: openly licensed outlines, advances and kerning."""
import io,glob,math,os,unicodedata
import numpy as np
from fontTools.ttLib import TTFont
from PIL import ImageFont
PTS=[11,12,14,16,18,20,24,28,36,9,10,8,7]   # size index 0 is the default 11 pt
FAM=['carlito','caladea','arimo','tinos','cousine','open-sans','oswald','caveat']
FAM_NAMES=['Carlito','Caladea','Arimo','Tinos','Cousine','Open Sans','Oswald','Caveat']
FAM_FACES=[(1,1),(1,1),(1,1),(1,1),(1,1),(1,1),(1,0),(1,0)]     # has a bold, has an italic
FAM_ALIAS=['Calibri','Cambria','Arial','Times New Roman','Courier New',None,None,None]   # the commercial family each one stands in for, by metrics
_root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _path(fam,sub,w,st): return f'{_root}/fonts/{fam}/package/files/{fam}-{sub}-{w}-{st}.woff'
def _load(fam,sub,w,st):
    f=TTFont(_path(fam,sub,w,st),recalcTimestamp=False); f.flavor=None; b=io.BytesIO(); f.save(b); return b.getvalue()
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
SZ=list(range(11,73))+[7,8,9,10,4,5,6]            # font sizes a style record can hold; field value 0 is the default 11 pt
NSZ=len(SZ)
def sz_raw(v): return (v&15)+((v>>4)<<19)    # a size field value placed in the record's bit positions
def sz_near(pt): return min((i for i in range(NSZ) if SZ[i]>=7),key=lambda i:(abs(SZ[i]-pt),SZ[i]))   # 4, 5, 6 pt are only for drawing at small zoom
def st_font(st): return ((st>>7)&1)+(((st>>25)&3)*2)
def font_raw(f): return ((f&1)<<7)+((f>>1)<<22)
def lit(st):
    "Record value of a style written at build time: old size index in the low bits, flags at 16, 32, 64, font at 128 and 1<<25, color and so on above."
    return sz_raw(SZ.index(PTS[st&15]))+(st&(16|32|64))+font_raw(st_font(st))+(st&0x7FF00)
GLW=180     # pixel columns of the glyph unit's row plane: the widest glyph at 72 pt
FACES=[(fi,bo,it) for fi in range(len(FAM)) for bo in range(1+FAM_FACES[fi][0]) for it in range(1+FAM_FACES[fi][1])]
def x_snap_face(fi,bo,it): return False      # viewed side by side (shots/fonts_xsnap_compare.png): stems snapped in x are crisper, but letters space unevenly because pens are whole pixels
def face_of(fi,bo,it): return (fi,bo if FAM_FACES[fi][0] else 0,it if FAM_FACES[fi][1] else 0)
def st_of_font(f): return ((f&1)<<7)+((f>>1)<<25)
_MS={}; LDEF=1.08
def metrics_sz(si,fi):
    "Ascent and line height in pixels at a size field value, for one family, from the family's own tables."
    k=(si,fi)
    if k not in _MS:
        # The font's own Windows metrics, which set single spacing, at the true size. The default paragraph is 1.08 lines, as the extra goes above the text.
        px=SZ[si]*96/72; t=tt(fi,0,0); o=t['OS/2']; u=t['head'].unitsPerEm; a=o.usWinAscent*px/u; l=(o.usWinAscent+o.usWinDescent)*px/u
        _MS[k]=(round(a+l*(LDEF-1)),round(l*LDEF*256)/256)
    return _MS[k]
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
