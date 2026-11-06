"""Side by side text lines at 3x zoom: current ROM, directly written network without and with snapping.
Each glyph is drawn by the engine; the layout follows the shipping rule (fractional pen, floored per glyph)."""
from glyphnet_common import *
from PIL import Image,ImageDraw,ImageFont
TEXT='minimum Home Document Quality glyph'
KP=rom.kern_pairs()
def layout(f,pt,text):
    px=ppem(pt); pen=0.0; o=[]; prev=None
    for c in text:
        k=ord(c)
        if prev is not None: pen+=KP.get((prev,k),{}).get(f,0)*px
        o.append((k,int(math.floor(pen+0.5)),pen)); pen+=rom.adv_em(*f,k)*px; prev=k
    return o,int(pen)+8
def blit(fb,g,x):
    h=min(fb.shape[0],g.shape[0]); w=min(fb.shape[1]-x,g.shape[1])
    fb[:h,x:x+w]=np.maximum(fb[:h,x:x+w],g[:h,:w])
def line_img(cells,scale=3,label=None):
    v=np.clip(1-cells,0,1)
    im=Image.fromarray((v*255+.5).astype(np.uint8),'L').resize((cells.shape[1]*scale,cells.shape[0]*scale),Image.NEAREST)
    return im
LB=ImageFont.load_default()
def sheet(fam,face,fidx,net,pts,fn,extra=None):
    rows=[]
    for pt in pts:
        f=face; G=geom(pt,f[0]); o,wd=layout(f,pt,TEXT); wd+=4
        H=G['H'] if G['H']<30 else G['rows']
        A=np.zeros((H,wd));B=A.copy();C=A.copy();D=A.copy()
        codes=[k for k,_,_ in o]
        dr=[draw(k,fidx,pt,(0,0)) for k in codes]+[draw(k,fidx,pt,(1,1)) for k in codes]+[draw(k,fidx,pt,(1,0)) for k in codes]
        res,_,_=run(net,dr)
        n=len(codes)
        for i,(k,x,_) in enumerate(o):
            blit(A,rom_bitmap(*f,k,pt),x); blit(B,pad(res[i],G),x); blit(C,pad(res[i+n],G),x); blit(D,pad(res[i+2*n],G),x)
        rows.append((pt,[('ROM bitmap',A),('network, no snap',B),('network, y and x snap',C),('network, y snap only',D)]))
    W=max(r[1][0][1].shape[1] for r in rows)*3+150
    Ht=sum(sum(a.shape[0]*3+4 for _,a in r[1])+10 for r in rows)
    im=Image.new('L',(W,Ht),255); d=ImageDraw.Draw(im); y=0
    for pt,ls in rows:
        for lab,a in ls:
            d.text((2,y+a.shape[0]*3//2-6),f'{pt} pt {lab}',fill=90,font=LB); im.paste(line_img(a),(146,y)); y+=a.shape[0]*3+4
        y+=10
    im.save(fn)
if __name__=='__main__':
    os.makedirs(ROOT+'/shots',exist_ok=True)
    F8=[(fi,b,i) for fi in (0,1) for b in (0,1) for i in (0,1)]
    if not os.path.exists(f'{OUT}/full.bin.gz') or '--build' in sys.argv:
        st=build('full',F8,gn.ASCII); print({k:v for k,v in st.items() if k!='per'})
    for fi,fam in enumerate(('carlito','caladea')):
        for b,i in ((0,0),(1,0),(0,1),(1,1)):
            sheet(fam,(fi,b,i),F8.index((fi,b,i)),'full',PTSZ,f'{ROOT}/shots/glyph_{fam}_{"b" if b else "r"}{"i" if i else ""}.png')
