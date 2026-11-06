"""Animated tour of ten sub-networks: where their neurons live and real weights from the shipped file. Usage: subunits.py repo out.gif"""
import gzip,json,struct,io,sys,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
REPO,OUT=sys.argv[1:3];B=REPO+'/build/'
blob=gzip.open(B+'net.bin.gz').read();hl=struct.unpack('<I',blob[:4])[0];h=json.loads(blob[4:4+hl]);o=(4+hl+3)&~3
N=h['n'];zb=blob[o:o+h['zn']];o+=h['zn'];L=np.frombuffer(blob,'<i4',h['L']+1,o).copy();o+=4*(h['L']+1)+4*h['nports'];wt=np.frombuffer(blob,'<f8',h['nt'],o);o+=8*h['nt'];bt=np.frombuffer(blob,'<f8',h['nb'],o)
gs=json.load(open(B+'ngroups.json'));nm=json.load(open(B+'names.json'));n1=h['n1']
names=nm if isinstance(nm,dict) else {str(i):x for i,x in enumerate(nm)}
ln=struct.unpack('<12I',zb[:48]);p=[48]
for x in ln:p.append(p[-1]+x)
pos=p[:12]
def rv(k):
    x=0;s=0;q=pos[k]
    while True:
        b=zb[q];q+=1;x|=(b&127)<<s;s+=7
        if not b&128:break
    pos[k]=q;return x
uz=lambda x:(x>>1)^-(x&1)
ni=[0]*N;no=[0]*N;act=np.zeros(N,int);bias=np.zeros(N)
for i in range(N):ni[i]=rv(0);no[i]=rv(1);act[i]=zb[pos[2]]&3;pos[2]+=1;bias[i]=bt[rv(3)]
ly=np.searchsorted(L,np.arange(N),side='right')-1;S=[];D=[];W_=[];RR=[]
pv=[0]*4
for i in range(N):
    for c0 in range(ni[i]):
        c=min(c0,3);x=rv(4+c);pv[c]+=uz(x>>1);S.append(pv[c]);D.append(i);W_.append(wt[rv(8)]);RR.append(0)
pf=0
for i in range(N):
    if no[i]:
        e=L[ly[i]+1];pf+=uz(rv(9));t=pf
        for k in range(no[i]):
            if k:t+=rv(10)
            w=wt[rv(11)];S.append(i);D.append(t);W_.append(w);RR.append(1 if t<e else 0)
S,D,W_,RR=map(np.array,(S,D,W_,RR));G=np.array(gs);print(len(S))
order=np.argsort(D,kind='stable');starts=np.searchsorted(D[order],np.arange(N+1))
inp=lambda i:order[starts[i]:starts[i+1]]
def ft(w):
    t=TTFont(f'{REPO}/fonts/carlito/package/files/carlito-latin-{w}-normal.woff');t.flavor=None;b=io.BytesIO();t.save(b);return b.getvalue()
R_,B_=ft(400),ft(700);F=lambda s,b=False:ImageFont.truetype(io.BytesIO(B_ if b else R_),s)
INK,MUT,LINE,BG=(28,39,51),(91,107,123),(201,211,221),(251,252,253);BLUE,AMB,TEAL=(37,99,201),(217,119,6),(15,157,138)
UNITS=[('raw event interpretation','Names keys and pointer events'),('key handling','Turns a key into a command'),('screenshot hit test','Finds what is under the pointer'),('edit primitives','Inserts and deletes, logs undo'),('compiled control','Next value of every register'),('line breaking','Decides where lines end'),('glyph weights (outline edges)','Font outlines as neurons'),('ramp bank','Turns a crossing into pixel shares'),('docx crc','Checksums saved bytes'),('pdf writer','Writes PDF objects and text')]
SP=380;bin_=N/SP;base=np.full((SP,SP,3),255,'uint8');a=(D/bin_).astype(int);c=(S/bin_).astype(int);base[a,c]=(214,221,229)
AN={0:'Identity',1:'Step',2:'ReLU',3:'Hold'}
def fw(w):
    a_=abs(w)
    if a_==0:return '0'
    sg='-' if w<0 else ''
    if a_>=2**38:
        e=round(math.log2(a_));r=a_-2**e
        if r==0:return f'{sg}2^{e}'
        return f"{sg}(2^{e} {'+' if r>0 else '-'} {abs(r):,.6g})"
    e=round(math.log2(a_))
    if a_==2**e and e>=8:return f'{sg}2^{e}'
    return f'{w:.6g}'
def pick(g):
    idx=np.nonzero(G==g)[0];can=[]
    for i in idx:
        k=inp(i)
        if 2<=len(k)<=6:can.append(i)
    can=np.array(can if can else idx);lay=ly[can];out=[]
    gate=[i for i in can if np.abs(W_[inp(i)]).max()>=2**39 and np.abs(W_[inp(i)]).min()<2**39]
    frac=[i for i in can if np.any(W_[inp(i)]%1!=0)]
    for pool in (frac[:],gate[:],list(can)):
        if pool:
            for q in (len(pool)//4,len(pool)//2,3*len(pool)//4):
                if pool[q] not in out:out.append(pool[q])
    return out[:3]
frames=[];durs=[]
for u,(g,why) in enumerate(UNITS):
    idx=np.nonzero(G==g)[0];m=np.isin(D,idx);hm=base.copy();hm[a[m],c[m]]=AMB
    ns=pick(g);lays=ly[idx];dom='second clock' if idx.min()>=n1 else 'main clock' if idx.max()<n1 else 'both clocks';acts={k:int((act[idx]==k).sum()) for k in range(4)}
    for pi,i in enumerate(ns):
        im=Image.new('RGB',(1200,620),BG);d=ImageDraw.Draw(im)
        d.text((28,16),g,font=F(32,True),fill=INK);d.text((28,56),why,font=F(20),fill=BLUE);d.text((1172,24),f'{u+1} of {len(UNITS)}',font=F(18),fill=MUT,anchor='ra')
        d.text((28,92),'Where it lives in the matrices',font=F(19,True),fill=INK)
        im.paste(Image.fromarray(hm),(28,120));d.rectangle([27,119,28+SP,120+SP],outline=INK)
        d.line([(28,120+int(n1/bin_)),(28+SP,120+int(n1/bin_))],fill=(120,130,140));d.line([(28+int(n1/bin_),120),(28+int(n1/bin_),120+SP)],fill=(120,130,140))
        d.text((28,506),'Amber: weights into these neurons. Dot is about %s neurons.'%f'{int(bin_):,}',font=F(14),fill=MUT)
        y=532
        d.text((28,y),f'{len(idx):,} neurons, {dom}, layers {lays.min()} to {lays.max()}',font=F(17,True),fill=INK)
        d.text((28,y+24),'  '.join(f'{AN[k]} {acts[k]:,}' for k in (1,2,0,3) if acts[k]),font=F(16),fill=MUT);d.text((28,y+48),f'Index numbers run from {idx.min():,} to {idx.max():,}',font=F(15),fill=MUT)
        X=440;d.text((X,92),f'One real neuron, example {pi+1} of {len(ns)}',font=F(19,True),fill=INK)
        d.rounded_rectangle([X,120,1172,596],10,fill=(255,255,255),outline=LINE)
        d.text((X+18,134),f'Neuron {i:,}',font=F(24,True),fill=INK)
        q=[('Layer',str(ly[i])),('Activation',AN[act[i]]),('Bias b',fw(bias[i]))]
        for j,(k_,v_) in enumerate(q):
            d.text((X+18+j*220,172),k_,font=F(15),fill=MUT);d.text((X+18+j*220,192),v_,font=F(21,True),fill=INK)
        ky=232;d.text((X+18,ky),'Weights coming in, as they appear in row %s of the matrices'%f'{i:,}',font=F(17,True),fill=INK);ky+=30
        for x_,t_ in ((X+18,'From neuron'),(X+140,'In sub-network'),(X+440,'Weight'),(X+600,'Matrix')):d.text((x_,ky),t_,font=F(15,True),fill=MUT)
        ky+=24;d.line([(X+18,ky-3),(1156,ky-3)],fill=LINE)
        ii=inp(i)[:9]
        for e_ in ii:
            s=int(S[e_]);d.text((X+18,ky),f'{s:,}',font=F(17),fill=INK);d.text((X+140,ky),gs[s][:30],font=F(17),fill=INK);d.text((X+440,ky),fw(W_[e_]),font=F(18,True),fill=BLUE);d.text((X+600,ky),'R (last tick)' if RR[e_] else 'F (same tick)',font=F(16),fill=AMB if RR[e_] else MUT);ky+=28
        if not len(ii):d.text((X+18,ky),'No F or R inputs: it takes its value from outside input.',font=F(17),fill=MUT)
        d.text((X+18,566),f'Output = {AN[act[i]]}( bias + sum of weight × that neuron\'s value )' if act[i]!=3 else 'Output = its own value + bias + sum of weight × value',font=F(16),fill=MUT)
        frames.append(im);durs.append(1900)
pal=frames[0].convert('P',palette=Image.ADAPTIVE,colors=64)
f2=[f.quantize(palette=pal,dither=Image.NONE) for f in frames]
f2[0].save(OUT,save_all=True,append_images=f2[1:],duration=durs,loop=0,optimize=True)
print(len(frames),'frames')
