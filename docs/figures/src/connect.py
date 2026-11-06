"""Measures how the sub-networks really connect, by decoding the shipped weight file the way host/engine.c does. Usage: connect.py build_dir out.json"""
import gzip,json,struct,sys,collections
B,OUT=sys.argv[1:3]
blob=gzip.open(B+'/net.bin.gz').read();hl=struct.unpack('<I',blob[:4])[0];h=json.loads(blob[4:4+hl]);o=(4+hl+3)&~3
gs=json.load(open(B+'/ngroups.json'));N=h['n'];assert len(gs)==N
zb=blob[o:o+h['zn']];o+=h['zn'];L=struct.unpack(f"<{h['L']+1}i",blob[o:o+4*(h['L']+1)]);o+=4*(h['L']+1);ports=struct.unpack(f"<{h['nports']}i",blob[o:o+4*h['nports']])
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
ni=[0]*N;no=[0]*N
for i in range(N):ni[i]=rv(0);no[i]=rv(1);pos[2]+=1;rv(3)
E_=collections.Counter()
pv=[0,0,0,0]
for i in range(N):
    for c0 in range(ni[i]):
        c=min(c0,3);x=rv(4+c);pv[c]+=uz(x>>1);rv(8);E_[(gs[pv[c]],gs[i])]+=1
pf=0
for i in range(N):
    if no[i]:
        pf+=uz(rv(9));t=pf;rv(11);E_[(gs[i],gs[t])]+=1
        for k in range(1,no[i]):t+=rv(10);rv(11);E_[(gs[i],gs[t])]+=1
KN={1:'memory write',2:'memory read',3:'screen rectangle',4:'screen patch',11:'screen patch',5:'screen pixel read',6:'screen and memory copy',8:'glyph call',10:'style read'}
P=collections.Counter();q=0
while q<len(ports):
    k=ports[q];n=6 if k in(1,2) else 12 if k==3 else 9 if k in(4,11) else 10 if k==6 else 5+2*ports[q+3]+2*ports[q+4] if k==8 else 1 if k==9 else 8 if k==10 else 5 if k==5 else 4
    if k!=9:
        en=ports[q+1];P[(gs[en],KN.get(k,str(k)))]+=1
    q+=n
g={}
for key in ['halt','chold','clipout','fileout','dsave','wpic','wopen','kbo','ffield','fback','wantp','timer','pass_','hold','outbase','namea','namen']:
    if key in h and isinstance(h[key],int):g[key]=gs[h[key]]
ev={'ev':sorted(set(gs[i] for i in h['ev'])),'keyv':sorted(set(gs[i] for i in h['keyv']))}
json.dump({'edges':[[a,b,c] for (a,b),c in E_.most_common()],'ports':[[a,b,c] for (a,b),c in P.most_common()],'commands':g,'inputs':ev,'hdr':sorted(k for k in h if k not in('rom','init','init1','bank_init'))},open(OUT,'w'),indent=0)
print('edges',sum(E_.values()),'expected',h['e'],'pairs',len(E_))
for (a,b),c in E_.most_common(30):
    if a!=b:print(c,a,'->',b)
print(P.most_common(40));print(g);print(ev)
ext=collections.Counter();
for (a,b),c in E_.items():
    if a!=b:ext[a]+=c;ext[b]+=c
print(ext.most_common(12))
