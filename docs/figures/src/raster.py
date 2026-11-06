"""Writes the README's GIFs and PNGs from real outputs: neural_activity.gif from the capture, id_plane.png from the screen tensor, glyph_raster.gif from a real font outline with the glyph network's own arithmetic."""
import json,sys,math,glob,io,subprocess,os
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
O,CAP,REPO,HERO=sys.argv[1:5]
def ttf(w,st='normal'):
    f=TTFont(f'{REPO}/fonts/carlito/package/files/carlito-latin-{w}-{st}.woff');f.flavor=None;b=io.BytesIO();f.save(b);return b.getvalue(),f
FB,TT=ttf(400);FBB,_=ttf(700)
F=lambda s,b=False:ImageFont.truetype(io.BytesIO(FBB if b else FB),s)
INK,MUT,LINE,BG=(28,39,51),(91,107,123),(201,211,221),(251,252,253);BLUE,AMB,TEAL,VIO=(37,99,201),(217,119,6),(15,157,138),(122,92,214)
C=json.load(open(CAP+'/meta.json'));N=C['N'];gs=C['gs'];groups=C['groups']
# ---- treemap with area proportional to the square root of the neuron count, so small sub-networks can be seen ----
cnt={g:0 for g in groups};first={}
pos=np.zeros(N,int)
for i,g in enumerate(gs):pos[i]=cnt[g];cnt[g]+=1
items=sorted([g for g in groups if cnt[g]],key=lambda g:-cnt[g])
W0,H0=660,430
def squar(its,x,y,w,h,out):
    if not its:return
    if len(its)==1:out[its[0][0]]=(x,y,w,h);return
    tot=sum(a for _,a in its);acc=0;k=0
    for k,(g,a) in enumerate(its):
        acc+=a
        if acc>=tot/2:break
    k=min(k,len(its)-2);A=sum(a for _,a in its[:k+1])/tot
    if w>=h:squar(its[:k+1],x,y,w*A,h,out);squar(its[k+1:],x+w*A,y,w*(1-A),h,out)
    else:squar(its[:k+1],x,y,w,h*A,out);squar(its[k+1:],x,y+h*A,w,h*(1-A),out)
rects={};squar([(g,math.sqrt(cnt[g])) for g in items],0,0,W0,H0,rects)
px=np.zeros((N,2),int)
for i,g in enumerate(gs):
    x,y,w,h=rects[g];w_=max(int(w)-2,1);h_=max(int(h)-2,1);k=int(pos[i]*w_*h_/cnt[g]);px[i]=(int(x)+1+k%w_,int(y)+1+k//w_)
base=Image.new('RGB',(W0,H0),(238,241,244));d=ImageDraw.Draw(base)
SHORT={'glyph weights (outline edges)':'font outlines','glyph unit':'glyph unit','glyph metrics':'metrics','ribbon display list':'ribbon','compiled control':'compiled control','ramp bank':'ramps','docx crc':'crc','rv a3 interaction':'interaction','docx reader':'docx reader','coverage':'coverage','chrome':'chrome','layout and paint':'layout + paint','key handling':'keys','screenshot hit test':'hit test','line breaking':'lines','edit primitives':'edit','pointer':'pointer','pdf writer':'pdf',}
for g,(x,y,w,h) in rects.items():
    d.rectangle([x,y,x+w,y+h],outline=(255,255,255))
lab=Image.new('RGBA',(W0,H0),(0,0,0,0));dl=ImageDraw.Draw(lab)
for g,(x,y,w,h) in rects.items():
    if g in SHORT and w>46 and h>18:dl.text((x+4,y+2),SHORT[g],font=F(13),fill=(60,75,90,255))
def frame(heat,lit,ev,tick,total,fired,shot):
    im=Image.new('RGB',(1180,540),BG);d=ImageDraw.Draw(im);d.text((24,14),'What the network does for one event',font=F(24,True),fill=INK)
    d.text((24,46),ev,font=F(19),fill=BLUE)
    mp=np.array(base,dtype=float)
    a=heat[...,None];mp=mp*(1-a)+np.array(AMB,float)*a
    M=Image.fromarray(mp.astype('uint8'));M.paste(lab,(0,0),lab);im.paste(M,(24,78))
    d.text((24,514),'Each tile is a named sub-network, each dot its neurons. Tile area follows the square root of its size.',font=F(15),fill=MUT)
    S=shot.resize((470,294),Image.LANCZOS);im.paste(S,(692,78));d.rectangle([692,78,1162,372],outline=LINE)
    d.text((692,386),f'tick {tick:,} of {total:,}',font=F(22,True),fill=INK)
    d.text((692,416),f'{fired:,} of {N:,} neurons have fired',font=F(18),fill=INK)
    d.text((692,442),f'{100*fired/N:.2f}% of the network',font=F(18),fill=MUT)
    d.text((692,478),'Right: the real screen tensor when the event finished.',font=F(15),fill=MUT)
    return im
def fbimg(n):
    a=np.frombuffer(open(f'{CAP}/fb_{n}.bin','rb').read(),'uint8').reshape(800,1280,4).copy();return a
fr=[];dur=[]
EV=[('key_new','Key press: a letter this size has never drawn, so its font program runs'),('key_same','Key press: the same letter, now from the glyph cache'),('click','Mouse click: the hit test reads the id plane under the pointer'),('bold','Ctrl+B: format the typing state, repaint the ribbon')]
for n,lab_ in EV:
    m=next(q for q in C['meta'] if q['name']==n);heat=np.zeros((H0,W0));seen=set();shot=Image.fromarray(fbimg(n)[...,:3])
    for f in m['frames']:
        heat*=.72
        if f['n']:
            idx=np.array(f['n']);yy=px[idx,1];xx=px[idx,0]
            for dy in (-1,0,1):
                for dx in (-1,0,1):heat[(yy+dy).clip(0,H0-1),(xx+dx).clip(0,W0-1)]=1
        seen.update(f['n']);fr.append(frame(heat,None,lab_,f['tick'],m['ticks'],len(seen),shot));dur.append(110)
    dur[-1]=1700
pal=fr[0].convert('P',palette=Image.ADAPTIVE,colors=128)
fr2=[f.quantize(palette=pal,dither=Image.NONE) for f in fr]
fr2[0].save(O+'/neural_activity.gif',save_all=True,append_images=fr2[1:],duration=dur,loop=0,optimize=True)
# ---- id plane ----
a=fbimg('bold');rgb=Image.fromarray(a[...,:3]);al=a[...,3]
hue=(al.astype(int)*97)%360
def h2r(h):
    c=.62;x=c*(1-abs((h/60)%2-1));m=.32
    i=(h//60)%6;v=[(c,x,0),(x,c,0),(0,c,x),(0,x,c),(x,0,c),(c,0,x)];return tuple(int((u+m)*255) for u in v[i])
lut=np.array([h2r(i*97%360) for i in range(256)],'uint8');lut[0]=(240,242,245);idp=lut[al]
W=1280;out=Image.new('RGB',(1320,470),BG);d=ImageDraw.Draw(out)
out.paste(rgb.resize((640,400),Image.LANCZOS),(13,56));out.paste(Image.fromarray(idp).resize((640,400),Image.NEAREST),(667,56))
d.text((13,18),'Color channels: what you see',font=F(24,True),fill=INK);d.text((667,18),f'Alpha channel: what the network reads ({len(np.unique(al))} ids)',font=F(24,True),fill=INK)
out.save(O+'/id_plane.png',optimize=True)
# ---- glyph ----
class Flat(BasePen):
    def __init__(s,gs,tol=4):super().__init__(gs);s.cs=[];s.tol=tol
    def _moveTo(s,p):s.cs.append([p])
    def _lineTo(s,p):s.cs[-1].append(p)
    def _qCurveToOne(s,c,p):
        a=s._getCurrentPoint();dx=a[0]-2*c[0]+p[0];dy=a[1]-2*c[1]+p[1];n=max(1,math.ceil(math.sqrt(math.hypot(dx,dy)/(4*s.tol))))
        for i in range(1,n+1):
            t=i/n;u=1-t;s.cs[-1].append((u*u*a[0]+2*u*t*c[0]+t*t*p[0],u*u*a[1]+2*u*t*c[1]+t*t*p[1]))
    def _curveToOne(s,c1,c2,p):
        a=s._getCurrentPoint();
        for i in range(1,9):
            t=i/8;u=1-t;s.cs[-1].append(tuple(u**3*a[k]+3*u*u*t*c1[k]+3*u*t*t*c2[k]+t**3*p[k] for k in (0,1)))
    def _closePath(s):s.cs[-1].append(s.cs[-1][0])
    def _endPath(s):pass
gset=TT.getGlyphSet();cm=TT.getBestCmap();pen=Flat(gset);gset[cm[ord('g')]].draw(pen);em=TT['head'].unitsPerEm
E_=[(a,b) for c in pen.cs for a,b in zip(c,c[1:]) if a[1]!=b[1]]
ppem=30;K=4;s=ppem/em
xs=[p[0]*s for c in pen.cs for p in c];ys=[p[1]*s for c in pen.cs for p in c]
x0,x1,y0,y1=math.floor(min(xs))-1,math.ceil(max(xs))+1,math.floor(min(ys))-1,math.ceil(max(ys))+1
wpx,hpx=x1-x0,y1-y0
cov=np.zeros((hpx,wpx));gif=[];durs=[]
CW=380;scale=min(330/wpx,420/hpx)
sc=lambda x,y:(40+(x-x0)*scale,96+(y1-y)*scale)
gx=lambda x:800+(x)*min(330/wpx,420/hpx)
for row in range(hpx):
    for k in range(K):
        y=y1-(row+(k+.5)/K)
        cross=[]
        for a,b in E_:
            ya,yb=a[1]*s,b[1]*s
            if min(ya,yb)<=y<max(ya,yb):
                cross.append((a[0]*s+(y-ya)*(b[0]-a[0])*s/(yb-ya),1 if yb>ya else -1))
        # ramps R_q=relu(q-x); a pixel's share of a crossing is R_(q+1)-R_q; the signed sum is the winding
        line=np.zeros(wpx)
        for x,sg in cross:
            for q in range(wpx):
                ql=x0+q;line[q]+=sg*(max(0,ql+1-x)-max(0,ql-x))
        line=np.clip(np.abs(line),0,1);cov[row]+=line/K
        if k in (0,2) or True:
            im=Image.new('RGB',(1180,540),BG);d=ImageDraw.Draw(im)
            d.text((24,14),'Drawing a letter with neurons: no bitmap ships in the weights',font=F(24,True),fill=INK)
            d.text((24,46),'One tick per sample line. Four lines build one pixel row of the glyph cache.',font=F(18),fill=MUT)
            d.text((40,74),'1. Weights hold the outline edges',font=F(17,True),fill=BLUE)
            for a,b in E_:
                act=min(a[1]*s,b[1]*s)<=y<max(a[1]*s,b[1]*s)
                d.line([sc(a[0]*s,a[1]*s),sc(b[0]*s,b[1]*s)],fill=AMB if act else MUT,width=3 if act else 2)
            yy=sc(0,y)[1];d.line([(40,yy),(40+wpx*scale,yy)],fill=BLUE,width=1)
            for x,sg in cross:
                c=sc(x,y);d.ellipse([c[0]-5,c[1]-5,c[0]+5,c[1]+5],fill=AMB)
            bx=440;d.text((bx,74),'2. Ramps and winding on this line',font=F(17,True),fill=BLUE)
            cell=min(10,300/wpx)
            for q in range(wpx):
                v=line[q];h=int(v*90);d.rectangle([bx+q*cell,300-h,bx+(q+1)*cell-1,300],fill=BLUE if v>0 else LINE)
            d.line([(bx,300),(bx+wpx*cell,300)],fill=MUT)
            d.text((bx,312),'R(q) = relu(q - x)',font=F(17),fill=INK);d.text((bx,336),'pixel share = R(q+1) - R(q)',font=F(17),fill=INK);d.text((bx,360),'signed sum, clamped = coverage',font=F(17),fill=INK)
            d.text((bx,400),f'{len(cross)} of {len(E_)} edge neurons cross this line',font=F(16),fill=MUT);d.text((bx,424),f'pixel row {row+1} of {hpx}, sample {k+1} of {K}',font=F(16),fill=MUT)
            cx=800;d.text((cx,74),'3. Coverage accumulates',font=F(17,True),fill=BLUE);cs=min(340/wpx,420/hpx)
            for r in range(hpx):
                for q in range(wpx):
                    v=min(1,cov[r,q]);c=tuple(int(255-(255-i)*v) for i in INK)
                    d.rectangle([cx+q*cs,96+r*cs,cx+(q+1)*cs-1,96+(r+1)*cs-1],fill=c,outline=(236,239,243))
            d.text((24,514),f'Carlito g at {ppem} pixels per em, real outline. Snapping and hinting omitted here for clarity.',font=F(15),fill=MUT)
            gif.append(im);durs.append(70)
durs[-1]=1800
pal=gif[-1].convert('P',palette=Image.ADAPTIVE,colors=64)
g2=[f.quantize(palette=pal,dither=Image.NONE) for f in gif[::1]]
g2[0].save(O+'/glyph_raster.gif',save_all=True,append_images=g2[1:],duration=durs,loop=0,optimize=True)
