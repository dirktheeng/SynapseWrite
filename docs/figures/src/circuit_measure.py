"""Classifies every neuron by the circuit part it acts like, from its activation, bias and incoming weights. Usage: circuit_measure.py repo out.json"""
import gzip,json,struct,sys,collections,re
import numpy as np
sys.path.insert(0,sys.path[0]);from nets_data import F as FAMS
REPO,OUT=sys.argv[1:3];B=REPO+'/build/'
blob=gzip.open(B+'net.bin.gz').read();hl=struct.unpack('<I',blob[:4])[0];h=json.loads(blob[4:4+hl]);o=(4+hl+3)&~3
N=h['n'];zb=blob[o:o+h['zn']];o+=h['zn'];L=np.frombuffer(blob,'<i4',h['L']+1,o);o+=4*(h['L']+1)+4*h['nports'];wt=np.frombuffer(blob,'<f8',h['nt'],o);o+=8*h['nt'];bt=np.frombuffer(blob,'<f8',h['nb'],o)
gs=json.load(open(B+'ngroups.json'));HUB={'compiled control','shared control registers','bank and port wiring'};fam={};names=['Hub: control and wiring']
for f,_,r in FAMS:
    names.append(f)
    for n,_,_ in r:fam[n]='Hub: control and wiring' if n in HUB else f
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
ni=[0]*N;no=[0]*N;act=np.zeros(N,int);bi=np.zeros(N)
for i in range(N):ni[i]=rv(0);no[i]=rv(1);act[i]=zb[pos[2]]&3;pos[2]+=1;bi[i]=bt[rv(3)]
ly=np.searchsorted(L,np.arange(N),side='right')-1;inw=[[] for _ in range(N)];pv=[0]*4
for i in range(N):
    for c0 in range(ni[i]):
        c=min(c0,3);x=rv(4+c);pv[c]+=uz(x>>1);inw[i].append((pv[c],wt[rv(8)]))
pf=0
for i in range(N):
    if no[i]:
        pf+=uz(rv(9));t=pf
        for k in range(no[i]):
            if k:t+=rv(10)
            inw[t].append((i,wt[rv(11)]))
BIG=2**38
def kind(i):
    a=act[i];w=[x for _,x in inw[i]];bg=any(abs(x)>=BIG for x in w);unit=all(abs(x)==1 for x in w);b=bi[i]
    if a==3:return 'Register that only holds'
    if a==1:
        if bg:return 'Gated threshold'
        if not w:return 'Constant or input'
        if unit and b==round(b):return 'Plain logic gate'
        return 'Comparator'
    if a==2:
        if bg or b<=-BIG:return 'Switch for a number'
        return 'Ramp or clamp'
    if not w:return 'Constant or input'
    return 'Adder or wire'
K=[kind(i) for i in range(N)]
tot=collections.Counter(K);print(tot)
per={n:collections.Counter() for n in names}
for i,k in enumerate(K):per[fam[gs[i]]][k]+=1
for n in names:print(n,dict(per[n]))
ex={}
for i in range(N):
    w=sorted(x for _,x in inw[i])
    if act[i]==1 and w==[1,1] and bi[i]==-1 and 'AND' not in ex:ex['AND']=(i,gs[i],bi[i],[(s,x) for s,x in inw[i]])
    if act[i]==1 and len(w)>=2 and set(w)=={1} and bi[i]==0 and 'OR' not in ex:ex['OR']=(i,gs[i],bi[i],[(s,x) for s,x in inw[i]])
    if act[i]==1 and w==[-1] and bi[i]==1 and 'NOT' not in ex:ex['NOT']=(i,gs[i],bi[i],[(s,x) for s,x in inw[i]])
    if act[i]==2 and w==[1,2**40] and bi[i]==-2**40 and 'SWITCH' not in ex:ex['SWITCH']=(i,gs[i],bi[i],[(s,x) for s,x in inw[i]])
    if act[i]==0 and w==[1,1] and bi[i]==0 and 'ADD' not in ex:ex['ADD']=(i,gs[i],bi[i],[(s,x) for s,x in inw[i]])
print(ex)
n=collections.Counter()
for i in range(N):
    w=sorted(x for _,x in inw[i])
    if act[i]==1 and len(w)>=2 and set(w)=={1.0}:
        if bi[i]==-(len(w)-1):n['AND-form']+=1
        elif bi[i]==0:n['OR-form']+=1
    if act[i]==1 and w==[-1] and bi[i]==1:n['NOT']+=1
print(n)
json.dump(dict(tot=tot,per={k:dict(v) for k,v in per.items()},names=names,n=n,ex=ex),open(OUT,'w'),default=float)
