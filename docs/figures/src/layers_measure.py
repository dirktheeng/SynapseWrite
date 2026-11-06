import gzip,json,struct,io,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
SC,REPO=sys.argv[1:3]
blob=gzip.open(REPO+'/build/net.bin.gz').read();hl=struct.unpack('<I',blob[:4])[0];h=json.loads(blob[4:4+hl]);o=(4+hl+3)&~3
N=h['n'];zb=blob[o:o+h['zn']];o+=h['zn'];L=np.frombuffer(blob,'<i4',h['L']+1,o).copy()
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
ni=[0]*N;no=[0]*N;actk=np.zeros(N,int)
for i in range(N):ni[i]=rv(0);no[i]=rv(1);actk[i]=zb[pos[2]]&3;pos[2]+=1;rv(3)
ly=np.searchsorted(L,np.arange(N),side='right')-1
src=[];dst=[]
pv=[0]*4
for i in range(N):
    for c0 in range(ni[i]):
        c=min(c0,3);x=rv(4+c);pv[c]+=uz(x>>1);rv(8);src.append(pv[c]);dst.append(i)
pf=0
for i in range(N):
    if no[i]:
        e=L[ly[i]+1];pf+=uz(rv(9));t=pf;rv(11)
        for k in range(no[i]):
            if k:t+=rv(10);rv(11)
            if t>=e:src.append(i);dst.append(t)
src=np.array(src);dst=np.array(dst)
assert (ly[src]<ly[dst]).all()
n1=h['n1'];lb=int(ly[n1]);print('entries',len(src),'layers',h['L'],'domain boundary at layer',lb,'L[lb]',L[lb],'n1',n1,'main layers',lb,'second',h['L']-lb)
sz=L[1:]-L[:-1];print('largest',sz.max(),'at layer',sz.argmax(),'median',np.median(sz),'main sizes first',sz[:6].tolist())
print('cross',int(((src<n1)!=(dst<n1)).sum()))
C=json.load(open(SC+'/cap/meta.json'));m=[q for q in C['meta'] if q['name']=='key_same'][0];fr=m['frames'];k=max(range(1,len(fr)),key=lambda j:len(fr[j]['n']));act=np.zeros(N,bool);act[fr[k]['n']]=True
used=act[src];print('frame ticks',fr[k-1]['tick'],fr[k]['tick'],'active',int(act.sum()),'entries in active cols',int(used.sum()))
np.savez(SC+'/fdot.npz',src=src,dst=dst,ly=ly,L=L,act=act,lb=lb,n1=n1,actk=actk)
