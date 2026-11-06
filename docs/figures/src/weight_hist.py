"""Histograms of real weights and biases per family of sub-networks, on a signed power of two axis. Usage: weight_hist.py repo out.png"""
import gzip,json,struct,sys,math,collections
import numpy as np
sys.path.insert(0,sys.path[0]);from nets_data import F as FAMS
import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
REPO,OUT=sys.argv[1:3];B=REPO+'/build/'
blob=gzip.open(B+'net.bin.gz').read();hl=struct.unpack('<I',blob[:4])[0];h=json.loads(blob[4:4+hl]);o=(4+hl+3)&~3
N=h['n'];zb=blob[o:o+h['zn']];o+=h['zn'];L=np.frombuffer(blob,'<i4',h['L']+1,o);o+=4*(h['L']+1)+4*h['nports'];wt=np.frombuffer(blob,'<f8',h['nt'],o);o+=8*h['nt'];bt=np.frombuffer(blob,'<f8',h['nb'],o)
gs=json.load(open(B+'ngroups.json'));fam={};names=[]
HUB={'compiled control','shared control registers','bank and port wiring'}
for h_,_,r in FAMS:
    names.append(h_)
    for n,_,_ in r:fam[n]='Hub: control and wiring' if n in HUB else h_
names.insert(0,'Hub: control and wiring')
fi=np.array([names.index(fam[g]) for g in gs])
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
ni=[0]*N;no=[0]*N;bi=np.zeros(N)
for i in range(N):ni[i]=rv(0);no[i]=rv(1);pos[2]+=1;bi[i]=bt[rv(3)]
ly=np.searchsorted(L,np.arange(N),side='right')-1;D=[];W=[];pv=[0]*4
for i in range(N):
    for c0 in range(ni[i]):
        c=min(c0,3);x=rv(4+c);pv[c]+=uz(x>>1);D.append(i);W.append(wt[rv(8)])
pf=0
for i in range(N):
    if no[i]:
        pf+=uz(rv(9));t=pf
        for k in range(no[i]):
            if k:t+=rv(10)
            D.append(t);W.append(wt[rv(11)])
D=np.array(D);W=np.array(W);print(len(W),'distinct',len(np.unique(W)),'biases nonzero',int((bi!=0).sum()),'distinct',len(np.unique(bi)))
def cats(v):
    v=v[v!=0];a=np.abs(v);big=a>=2**38;ones=a==1;lg=np.log2(a);p2=(lg==np.round(lg))&~big&~ones;ints=(a==np.round(a))&~big&~ones&~p2;fr=~(big|ones|p2|ints)
    return dict(n=len(v),big=big.sum(),ones=ones.sum(),p2=p2.sum(),ints=ints.sum(),frac=fr.sum(),neg=(v<0).sum())
T={}
for nm,mw,mb in [('All',np.ones(len(W),bool),np.ones(N,bool))]+[(n,fi[D]==k,fi==k) for k,n in enumerate(names)]:
    T[nm]=(cats(W[mw]),cats(bi[mb]))
    a,b=T[nm];print(nm,{k:(round(100*a[k]/a['n'],1) if k!='n' else a[k]) for k in a},'| b',{k:(round(100*b[k]/max(1,b['n']),1) if k!='n' else b[k]) for k in b})
ex=W[np.abs(W)>=2**38];print('near infinity weights exact 2^40',int((np.abs(ex)==2**40).sum()),'of',len(ex))
exb=bi[np.abs(bi)>=2**38];print('bias exact -2^40',int((exb==-2**40).sum()),'of',len(exb),'within 1000',int((np.abs(np.abs(exb)-2**40)<=1000).sum()));print('common weights',collections.Counter(W.tolist()).most_common(8));print('common biases',collections.Counter(bi.tolist()).most_common(8))
BLUE,AMB,INK,MUT,LINE='#2563c9','#d97706','#1c2733','#5b6b7b','#c9d3dd'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.edgecolor':LINE,'text.color':INK,'axes.labelcolor':MUT,'xtick.color':MUT,'ytick.color':MUT})
def sl(v):
    v=v[v!=0];return np.sign(v)*np.maximum(np.round(np.log2(np.abs(v))),-12)+np.sign(v)*13  # gap around zero: -2^-12 .. 2^-12
edges=np.arange(-54.5,55.5,1)
fig,ax=plt.subplots(len(names)+1,2,figsize=(13,14.5),sharex=True,constrained_layout=True)
fig.suptitle('Most weights and biases are ±1, signed powers of two, or near ±2^40, a stand-in for infinity',fontsize=15,fontweight='bold',x=.01,ha='left')
ticks=[-53,-43,-33,-23,-13,13,23,33,43,53];labs=['-2^40','-2^30','-2^20','-2^10','-1','1','2^10','2^20','2^30','2^40']
for r,(nm,mw,mb) in enumerate([('All',np.ones(len(W),bool),np.ones(N,bool))]+[(n,fi[D]==k,fi==k) for k,n in enumerate(names)]):
    for c,(val,col,ti) in enumerate(((W[mw],BLUE,'weights'),(bi[mb],AMB,'biases (nonzero)'))):
        A=ax[r,c];A.hist(sl(val),bins=edges,color=col,rwidth=.8,log=True);A.set_ylim(.7,5e6 if r==0 or nm.startswith('Drawing') else 2e5);A.spines[['top','right']].set_visible(False);A.grid(axis='y',color='#e6ebf0',lw=.6);A.set_axisbelow(True)
        A.axvline(0,color=LINE,lw=.8);A.set_xticks(ticks);A.set_xticklabels(labs);A.tick_params(length=0)
        s=T[nm][c];A.set_title(f"{nm}: {s['n']:,} {ti}",loc='left',fontsize=10,fontweight='bold')
        A.text(.995,.82,f"±2^40 range {100*s['big']/max(1,s['n']):.0f}%   ±1 {100*s['ones']/max(1,s['n']):.0f}%   other 2^n {100*s['p2']/max(1,s['n']):.0f}%   other integers {100*s['ints']/max(1,s['n']):.0f}%   fractions {100*s['frac']/max(1,s['n']):.0f}%",transform=A.transAxes,ha='right',fontsize=8,color=MUT)
fig.supxlabel('Value, by nearest power of two (log scale, no zero bin: zeros are simply absent). Vertical axis: count, log scale.',fontsize=10,color=MUT)
fig.savefig(OUT,dpi=110,facecolor='#fbfcfd')
