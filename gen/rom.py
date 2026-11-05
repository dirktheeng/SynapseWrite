"""Compiles openly licensed font outlines into per-glyph weight vectors."""
import io,glob,math,os
from fontTools.ttLib import TTFont
from PIL import Image,ImageDraw,ImageFont
PTS=[11,12,14,16,18,20,24,28,36,9,10]   # size index 0 is the default 11 pt
SW,SH,LW,LH=24,28,60,64                 # small and large patch sizes
def _load(fam,w,st):
    p=f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/fonts/{fam}/package/files/{fam}-latin-{w}-{st}.woff'
    f=TTFont(p); f.flavor=None; b=io.BytesIO(); f.save(b); return b.getvalue()
FAM=['carlito','caladea']
CACHE={}
def font(fi,bold,ital,px):
    k=(fi,bold,ital)
    if k not in CACHE: CACHE[k]=_load(FAM[fi],700 if bold else 400,'italic' if ital else 'normal')
    return ImageFont.truetype(io.BytesIO(CACHE[k]),px)
def small(si): return PTS[si]<=14
def metrics(si,fi=0):
    px=round(PTS[si]*96/72); f=font(fi,0,0,px); a,d=f.getmetrics()
    return a,round((a+d)*1.08)
def glyph(fi,bold,ital,si,code):
    """Returns (advance, [(x,y,level 1..15)]) with the baseline at the size's ascent."""
    px=round(PTS[si]*96/72); f=font(fi,bold,ital,px); ch='•' if code==127 else chr(code)
    a,_=f.getmetrics(); W,H=(SW,SH) if small(si) else (LW,LH)
    im=Image.new('L',(W,H),0); d=ImageDraw.Draw(im); d.text((2,a),ch,font=f,fill=255,anchor='ls')
    adv=round(f.getlength(ch)); pts=[]
    px_=im.load()
    for y in range(H):
        for x in range(W):
            q=round(px_[x,y]*15/255)
            if q: pts.append((x,y,q))
    return adv,pts
