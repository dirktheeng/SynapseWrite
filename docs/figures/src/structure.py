"""Draws the whole network as its equation, from the shipped weight file. Usage: structure.py capture_dir repo_dir out.png"""
import gzip,json,struct,bisect,collections,io,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
SC,REPO,OUT=sys.argv[1:4]
blob=gzip.open(REPO+'/build/net.bin.gz').read();hl=struct.unpack('<I',blob[:4])[0];h=json.loads(blob[4:4+hl]);o=(4+hl+3)&~3
N=h['n'];zb=blob[o:o+h['zn']];o+=h['zn'];L=np.frombuffer(blob,'<i4',h['L']+1,o);o+=4*(h['L']+1);ports=np.frombuffer(blob,'<i4',h['nports'],o).tolist();o+=4*h['nports'];wt=np.frombuffer(blob,'<f8',h['nt'],o);o+=8*h['nt'];bt=np.frombuffer(blob,'<f8',h['nb'],o)
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
for i in range(N):
    ni[i]=rv(0);no[i]=rv(1);a=zb[pos[2]];pos[2]+=1;act[i]=a&3;bias[i]=bt[rv(3)]
S=500;B=N/S;Fm=np.zeros((S,S));Rm=np.zeros((S,S));ly=np.searchsorted(L,np.arange(N),side='right')-1;nf=nr=0;ex=None
pv=[0]*4
for i in range(N):
    for c0 in range(ni[i]):
        c=min(c0,3);x=rv(4+c);pv[c]+=uz(x>>1);rv(8);Fm[int(i/B),int(pv[c]/B)]+=1;nf+=1
pf=0
for i in range(N):
    if no[i]:
        e=L[ly[i]+1];pf+=uz(rv(9));t=pf;rv(11)
        for k in range(no[i]):
            if k:t+=rv(10);rv(11)
            if t<e:Rm[int(t/B),int(i/B)]+=1;nr+=1
            else:Fm[int(t/B),int(i/B)]+=1;nf+=1
print(json.dumps(dict(F=nf,R=nr,n1=h['n1'],N=N,nw=int(h['nt']),nb=int(h['nb']),act={int(k):int((act==k).sum()) for k in range(4)},layers=h['L'],sz=[int(L[i+1]-L[i]) for i in range(h['L'])][:0])))
tt=TTFont(REPO+'/fonts/carlito/package/files/carlito-latin-400-normal.woff');tt.flavor=None;b1=io.BytesIO();tt.save(b1);tb=TTFont(REPO+'/fonts/carlito/package/files/carlito-latin-700-normal.woff');tb.flavor=None;b2=io.BytesIO();tb.save(b2)
F=lambda s,bo=False:ImageFont.truetype(io.BytesIO((b2 if bo else b1).getvalue()),s)
INK,MUT,LINE,BG=(28,39,51),(91,107,123),(201,211,221),(251,252,253);BLUE,AMB,TEAL,VIO,RED=(37,99,201),(217,119,6),(15,157,138),(122,92,214),(192,57,43)
DJ='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';G=lambda z:ImageFont.truetype(DJ,z);W,H=1640,1130;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
d.text((36,24),'The whole app as vectors, matrices and activations',font=F(36,True),fill=INK)
d.text((36,68),'Drawn from the shipped weight file. Every neuron has the same index in every vector and matrix. The same v(t) appears twice because later layers read earlier layers within a tick.',font=F(21),fill=MUT)
d.text((36,102),'v(t) = σ( b + F·v(t) + R·v(t-1) + u(t) )',font=G(26),fill=BLUE)
Y=190;SH=500
def spy(M,x,title,sub,dil=1):
    a=np.full((S,S,3),255.0);v=M>0;l=np.log10(M.clip(1))/max(1,np.log10(M.max()));c=np.array(BLUE,float);base=np.array((185,208,245),float)
    col=(base[None,None]*(1-l[...,None])+np.array((12,50,130),float)*l[...,None]);a[v]=col[v]
    I=Image.fromarray(a.astype('uint8'))
    if dil>1:
        from PIL import ImageFilter;I=I.filter(ImageFilter.MinFilter(dil))
    im.paste(I,(x,Y));d.rectangle([x-1,Y-1,x+S,Y+S],outline=INK)
    n1=int(h['n1']/B);d.line([(x+n1,Y),(x+n1,Y+S)],fill=AMB);d.line([(x,Y+n1),(x+S,Y+n1)],fill=AMB)
    d.text((x,Y-52),title,font=F(25,True),fill=INK);d.text((x,Y-24),sub,font=F(17),fill=MUT)
act_col={0:(150,160,170),1:BLUE,2:TEAL,3:AMB}
def strip(x,arr,title,sub=None,w=30):
    a=np.array(arr,'uint8');I=Image.fromarray(a).resize((w,S),Image.NEAREST);im.paste(I,(x,Y));d.rectangle([x-1,Y-1,x+w,Y+S],outline=INK)
    d.text((x+w/2,Y-52),title,font=(G(21) if title=='σ' else F(23,True)),fill=INK,anchor='ma')
    if sub:d.text((x+w/2,Y-24),sub,font=F(15),fill=MUT,anchor='ma')
def sym(x,s,sz=44):d.text((x,Y+S/2),s,font=F(sz,True),fill=INK,anchor='mm')
def binv(idx,c):
    a=np.full((S,1,3),244,'uint8');
    for i in idx:a[min(S-1,int(i/B)),0]=c
    return a
C=json.load(open(SC+'/cap/meta.json'));m=[q for q in C['meta'] if q['name']=='key_same'][0];fr=m['frames'];k=max(range(1,len(fr)),key=lambda j:len(fr[j]['n']));
vt=fr[k]['n'];vp=fr[k-1]['n']
inp=list(h['ev'])+list(h['keyv'])+[h['keyl']];q=0;readout=[];np_=0
while q<len(ports):
    kk=ports[q];n=6 if kk in(1,2) else 12 if kk==3 else 9 if kk in(4,11) else 10 if kk==6 else 5+2*ports[q+3]+2*ports[q+4] if kk==8 else 1 if kk==9 else 8 if kk==10 else 5 if kk==5 else 4
    np_+=(kk!=9)
    if kk==2:readout+=list(range(ports[q+3],ports[q+3]+ports[q+4]))
    if kk==5:readout+=list(range(ports[q+4],ports[q+4]+4))
    if kk==10:readout+=[ports[q+3],ports[q+3]+1]
    q+=n
x=36
strip(x,binv(vt,BLUE),'v(t)','this tick');x+=30;sym(x+24,'=');x+=48
sig=np.zeros((S,1,3),'uint8')
for r in range(S):
    a=act[int(r*B):int((r+1)*B)];vals,cn=np.unique(a,return_counts=True);sig[r,0]=act_col[vals[cn.argmax()]]
strip(x,sig,'σ','each');x+=30;sym(x+22,'(',52);x+=38
strip(x,binv(np.nonzero(bias)[0],MUT),'b','bias');x+=30;sym(x+22,'+');x+=44
spy(Fm,x,'F: same tick',f'{nf:,} nonzero weights');Fx=x;x+=S+8;sym(x+8,'·',60);x+=20
strip(x,binv(vt,BLUE),'v(t)','this tick');x+=30;sym(x+22,'+');x+=44
spy(Rm,x,'R: last tick',f'{nr:,} nonzero weights',3);Rx=x;x+=S+8;sym(x+8,'·',60);x+=20
strip(x,binv(vp,BLUE),'v(t-1)','last');x+=30;sym(x+22,'+');x+=44
strip(x,binv(inp+readout,AMB),'u(t)','input');x+=30;sym(x+20,')',52)
yy=Y+S+22
d.text((Fx,yy),f'Each dot is about {int(B):,} neurons square. Below the diagonal: signals only flow to later layers.',font=F(16),fill=MUT)
d.text((Rx,yy),'Registers, loops and state tokens: how the network carries values to the next tick.',font=F(16),fill=MUT)
d.text((Fx,yy+22),f'Amber lines split the clock domains: {h["n1"]:,} main neurons, then {N-h["n1"]:,} mostly font neurons. No weight crosses.',font=F(16),fill=AMB)
yb=yy+66
# activations
d.text((36,yb),'σ',font=G(20),fill=INK);d.text((58,yb),': each neuron has its own',font=F(22,True),fill=INK)
cnt=[('Step',1,'1 if x > 0, else 0',int((act==1).sum())),('ReLU',2,'max(0, x)',int((act==2).sum())),('Identity',0,'x',int((act==0).sum())),('Hold',3,'keeps its value, adds x',int((act==3).sum()))]
for i,(a,c,f,n) in enumerate(cnt):
    x0=36+i*170;d.rounded_rectangle([x0,yb+36,x0+160,yb+176],8,fill=(255,255,255),outline=LINE);col=act_col[c];ax,ay=x0+80,yb+112
    d.line([(x0+18,ay),(x0+142,ay)],fill=LINE);d.line([(ax,yb+70),(ax,yb+150)],fill=LINE)
    pts={1:[(x0+18,ay),(ax,ay),(ax,ay-32),(x0+142,ay-32)],2:[(x0+18,ay),(ax,ay),(x0+132,ay-36)],0:[(x0+36,ay+30),(x0+124,ay-30)],3:[(x0+18,ay-22),(x0+142,ay-22)]}[c]
    d.line(pts,fill=col,width=4)
    d.text((x0+10,yb+42),a,font=F(18,True),fill=INK);d.text((x0+10,yb+152),f'{n:,}',font=F(16),fill=MUT)
    d.text((x0+150,yb+42),f if len(f)<10 else '',font=F(13),fill=MUT,anchor='ra')
# gate example
gx=740;d.text((gx,yb),'What one row looks like: a gate',font=F(22,True),fill=INK)
d.text((gx,yb+34),'y = relu(v + en · 2^40 − 2^40)',font=F(19),fill=BLUE)
cols=['...','v','...','en','...'];cw=62;tx=gx+50;ty=yb+70
for i,c in enumerate(cols):d.text((tx+cw*i+cw/2,ty),c,font=F(17,True),fill=INK,anchor='ma')
vals=['0','1','0','2^40','0']
for i,c in enumerate(vals):
    d.rectangle([tx+cw*i,ty+24,tx+cw*(i+1),ty+58],fill=(232,240,252) if c!='0' else (255,255,255),outline=LINE);d.text((tx+cw*i+cw/2,ty+32),c,font=F(17,c!='0'),fill=INK if c!='0' else MUT,anchor='ma')
d.text((gx,ty+32),'F[y]',font=F(18,True),fill=INK);d.text((tx+cw*5+14,ty+32),'b[y] = −2^40, activation = ReLU',font=F(18),fill=INK)
d.text((gx,ty+74),'If en = 1, then y = v. If en = 0, then y = 0.',font=F(18),fill=MUT)
# ports
px=36;py=yb+200
d.rounded_rectangle([px,py,W-36,py+98],10,fill=(226,245,242),outline=TEAL,width=2)
d.text((px+18,py+12),f'Outside the equation: {np_} ports, each naming which entries of v are its enable, address and data',font=F(20,True),fill=INK)
d.text((px+18,py+44),'When an enable is nonzero, the engine runs the operation on the memory bank or the screen. Read data lands in u(t+1), which is why reads arrive one tick later.',font=F(18),fill=INK)
d.text((px+18,py+70),'Events come in the same way: the glue writes 13 event and key entries of u, then repeats ticks until the halt entry of v fires.',font=F(18),fill=INK)
d.text((36,py+112),f'v(t) here is one real moment while typing a letter. Strips are {S} pixels tall, so each mark can stand for up to {int(B):,} neurons: the vectors are far emptier than they look. u(t) marks every input neuron, not its values at one tick.',font=F(16),fill=MUT)
im=im.crop((0,0,W,py+142));im.save(OUT,optimize=True)

np_count=np_;print(np_count)
