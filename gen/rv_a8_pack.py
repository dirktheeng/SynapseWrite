"""Compiles the finished network and writes the weight file. Called once at the end of app.py.
A8_SNAP in the environment saves the finished network so the format and compile stages can be rerun alone."""
import json,struct,gzip,sys,os,pickle,collections
import numpy as np
from nn import *
def nid(x): return next(iter(x.t))
def pack(net,precs,S,N0,K):
    if os.environ.get('A8_SNAP'):
        net.ports=[]; sys.setrecursionlimit(100000)
        pickle.dump((net,precs,S,N0,K),open(os.environ['A8_SNAP'],'wb'),protocol=4)
    import rv_a8_opt; rv_a8_opt.prune(net,precs,N0.values())
    c=net.compile(); new=c['new']
    gn_=[''] *c['n']
    for g_,ids_ in net.groups.items():
        for i_ in ids_:
            if new[i_]>=0: gn_[new[i_]]=g_
    json.dump(gn_,open('../build/ngroups.json','w'))
    print('neurons',c['n'],'layers',c['L'],file=sys.stderr)
    names={new[v_]:k_ for k_,v_ in N0.items() if new[v_]>=0}
    json.dump(names,open('../build/names.json','w'))
    json.dump({str(new[nid(r_)]):k_ for k_,r_ in S.items() if new[nid(r_)]>=0},open('../build/states.json','w'))
    pr=[]
    for r in precs:
        if r[0] in (1,2):
            d=r[3]
            pr+=[r[0],new[nid(r[1])],new[nid(r[2])],new[nid(d)],r[4],new[nid(r[5])] if r[5] is not None else -1]
        elif r[0]==3: pr+=[3]+[new[nid(q)] for q in r[1:]]
        elif r[0]==4: pr+=[4,new[nid(r[1])],new[nid(r[2])],new[nid(r[3])],new[nid(r[4][0])],r[5],r[6],new[nid(r[7])],new[nid(r[8])]]
        elif r[0]==6: pr+=[6]+[new[nid(q)] for q in r[1:]]
        elif r[0]==7: pr+=[7,new[nid(r[1])],new[nid(r[2])],new[nid(r[3])]]+list(r[4:])
        elif r[0]==5: pr+=[5,new[nid(r[1])],new[nid(r[2])],new[nid(r[3])]]
    n=c['n']; import rv_a8_fmt; raw,fh=rv_a8_fmt.encode(c,pr)
    SLOT0,SECB,T2=K['SLOT0'],K['SECB'],K['T2_ROM']
    hdr=dict(fmax=K['BANK']-K['FILE'],file=K['FILE'],n=n,L=c['L'],nports=len(pr),bank=K['BANK'],
     ev=[new[q] for q in K['EV']],cb=K['CB'],cb2=K['CB2'],init=[[new[i],v] for i,v in net.init.items()],
     bank_init=[*[[SECB+i_,v_] for i_,v_ in enumerate((1,816,K['PH'],K['PX'],K['TX'],K['TW'],96,864))],[K['LEN']+SLOT0,0],[K['DIRTY']+SLOT0,1],[K['PT'],SLOT0],[SLOT0+K['SAVE'],112],[SLOT0+K['SAVE']+1,16],[SLOT0+K['SAVE']+2,1],[SLOT0+K['PSPA'],K['DEFSPA']]]+T2)
    hdr.update({k:new[v] for k,v in K['HS'].items()}); hdr.update(fh)
    h=json.dumps(hdr,separators=(',',':')).encode()
    blob=struct.pack('<I',len(h))+h+b'\0'*((4-(len(h)+4)%4)%4)+raw
    gz=gzip.compress(blob,9)
    open('../build/net.bin.gz','wb').write(gz)
    prov={k:len(v) for k,v in net.groups.items()}
    json.dump(dict(neurons=n,edges=fh['e'],layers=c['L'],groups=prov,states=len(S)),open('../build/provenance.json','w'),indent=1)
    print('lazy',fh['ni'],'edges',fh['e'],'raw',len(blob),'gz',len(gz),file=sys.stderr)
