import io,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
SC,REPO=sys.argv[1:3];Z=np.load(SC+'/fdot.npz');src,dst,ly,L,lb,n1,ak=[Z[k] for k in ('src','dst','ly','L','lb','n1','actk')];lb=int(lb);n1=int(n1);NL=len(L)-1;N=len(ly)
def ft(w):
    t=TTFont(f'{REPO}/fonts/carlito/package/files/carlito-latin-{w}-normal.woff');t.flavor=None;b=io.BytesIO();t.save(b);return b.getvalue()
R_,B_=ft(400),ft(700);F=lambda s,b=False:ImageFont.truetype(io.BytesIO(B_ if b else R_),s);G=lambda s:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',s)
INK,MUT,LINE,BG=(28,39,51),(91,107,123),(201,211,221),(251,252,253);BLUE,AMB,TEAL,GRY=(37,99,201),(217,119,6),(15,157,138),(150,160,170)
AC={1:BLUE,2:TEAL,0:GRY,3:AMB};ORD=[1,2,0,3];AN={1:'Step',2:'ReLU',0:'Identity',3:'Hold'}
n=np.diff(L);nnz=np.bincount(ly[dst],minlength=NL);ac=np.zeros((NL,4),int)
for k in range(4):ac[:,k]=np.bincount(ly[ak==k],minlength=NL)
RH=4;W,H=1640,1040;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
d.text((36,20),'F · v(t), layer by layer: sizes and activations',font=F(36,True),fill=INK)
d.text((36,64),'Each layer k computes  v_k = σ_k( b_k + Σ_{j<k} F_kj · v_j + last tick and input terms ), then the next layer can use it. Drawn from the shipped weight file.',font=G(14),fill=MUT)
X0=36;Y0=170;cl=X0+40;c1=cl+6;BW=230;c2=c1+BW+24;AW=200;c3=c2+AW+24
lg=lambda v,m:(np.log10(np.maximum(v,1))/np.log10(m))
d.text((c1,Y0-62),'Vector size n_k',font=F(19,True),fill=INK);d.text((c1,Y0-38),'neurons in the layer (log scale)',font=F(15),fill=MUT)
d.text((c2,Y0-62),'Activations',font=F(19,True),fill=INK);d.text((c2,Y0-38),'share of the layer',font=F(15),fill=MUT)
d.text((c3,Y0-62),'Weights into the layer',font=F(19,True),fill=INK);d.text((c3,Y0-38),'nonzero F entries (log scale)',font=F(15),fill=MUT)
for k in range(NL):
    y=Y0+k*RH+(10 if k>=lb else 0)
    d.rectangle([c1,y,c1+BW*lg(n[k],n.max()),y+RH-2],fill=BLUE)
    x=c2
    for a_ in ORD:
        w=AW*ac[k,a_]/n[k]
        if w>0:d.rectangle([x,y,x+w,y+RH-2],fill=AC[a_])
        x+=w
    if nnz[k]:d.rectangle([c3,y,c3+BW*lg(nnz[k],nnz.max()),y+RH-2],fill=BLUE)
    if k%25==0 or k==lb:d.text((cl,y-6),str(k),font=F(14),fill=MUT,anchor='ra')
yb=Y0+lb*RH+3;d.line([(X0,yb),(c3+BW,yb)],fill=AMB,width=1);
d.text((c3+BW,yb-1),'',font=F(1))
d.text((X0,Y0-24),'layer',font=F(14),fill=MUT)
for i,a_ in enumerate(ORD):
    x=c2+i*0;
ly2=Y0+NL*RH+22
x=c2-200
for a_ in ORD:
    d.rectangle([x,ly2+3,x+14,ly2+17],fill=AC[a_]);d.text((x+20,ly2),f'{AN[a_]} {int(ac[:,a_].sum()):,}',font=F(16),fill=INK);x+=150
d.text((X0,ly2+30),f'Rows are real layers. Amber line: main clock ({lb} layers) above, second clock ({NL-lb} layers) below.',font=F(15),fill=MUT)
# table
T=c3+BW+36;Y=Y0-62
d.text((T,Y),'Sample layers, with the real matrix sizes',font=F(19,True),fill=INK);d.text((T,Y+24),'F_k is everything feeding layer k: n_k rows by all earlier neurons in that clock domain.',font=F(15),fill=MUT)
big=int(np.argmax(n[lb:]))+lb;sel=[0,1,2,5,25,75,int(np.argmax(nnz[:lb])),151,lb,lb+1,big,big+1,NL-1];sel=sorted(set(sel))
cols=[('Layer',T,0),('v_k',T+58,0),('F_k size',T+122,0),('nonzero',T+290,0),('Step',T+360,0),('ReLU',T+420,0),('Id',T+478,0)]
yy=Y0-4
for c,x,_ in cols:d.text((x,yy),c,font=F(15,True),fill=MUT)
d.line([(T,yy+22),(W-30,yy+22)],fill=LINE);yy+=30
for k in sel:
    s0=L[k]-(0 if k<lb else n1);dm=k>=lb
    if k==lb:
        d.line([(T,yy-3),(W-30,yy-3)],fill=AMB);d.text((T,yy),'second clock',font=F(14,True),fill=AMB);yy+=22
    vals=[str(k),f'{n[k]:,}',f'{n[k]:,} × {s0:,}',f'{nnz[k]:,}',f'{ac[k,1]:,}',f'{ac[k,2]:,}',f'{ac[k,0]:,}']
    for (c,x,_),v in zip(cols,vals):d.text((x,yy),v,font=F(15),fill=INK)
    yy+=27
yy+=12
d.rounded_rectangle([T,yy,W-30,yy+232],10,fill=(255,255,255),outline=LINE);q=yy+12
for s,b_ in [('Whole matrix F',True),(f'{N:,} × {N:,}, with {len(src):,} nonzero entries',False),(f'Main block: {n1:,} × {n1:,}. Second block: {N-n1:,} × {N-n1:,}',False),('',False),('The vectors',True),(f'v(t) has {N:,} numbers, split among {NL} layers',False),('F · v(t) gives one total per neuron, the same length',False),('',False),('Layer 0 has no F input: it reads only last tick and inputs.' if nnz[0]==0 else f'Layer 0 has {nnz[0]} F inputs.',False)]:
    d.text((T+14,q),s,font=F(16,b_),fill=INK);q+=23
im.crop((0,0,W,max(ly2+62,yy+244))).save(sys.argv[3],optimize=True)
print(n[:4],nnz[:4],sel,n[big],nnz.max(),[ (k,int(n[k]),int(nnz[k])) for k in sel])
