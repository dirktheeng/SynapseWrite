"""Debug tables for build/engine_check.wasm, written next to the weights and never loaded by the page.
An AND neuron assumes each argument is 0 or 1. Arguments that are a single step neuron or a state token are
boolean by construction; the others (linear combinations, data registers) are listed for the checker."""
_dbg_args=[]
_bset=getattr(net,'boolreg',set())
for _r,_a in net.and_args:
    if new[_a8rep[_r]]<0: continue
    for _x in _a:
        _x=as_x(_x); _x=X({_a8rep[_k]:_w for _k,_w in _x.t.items()},_x.c)
        if any(new[_k]<0 for _k in _x.t): continue
        if len(_x.t)==1 and not _x.c:
            (_k,_w),=_x.t.items()
            if _w==1 and (net.act[_k]==STEP or _k in _bset or _k==net.ONE_id): continue
        if not _x.t: continue
        _dbg_args.append((new[_a8rep[_r]],_x))
_pv=net.pullv
_ast=[0];_asr=[];_aw=[];_ac=[];_aand=[];_inv={}
for _g,(_r,_x) in enumerate(_dbg_args):
    _aand.append(_r);_ac.append(_x.c)
    for _k,_w in _x.t.items():
        _n=new[_k];_asr.append(~_n if _pv[_n] else _n);_aw.append(_w);_inv.setdefault(_n,[]).append(_g)
    _ast.append(len(_asr))
_wst=np.zeros(n+1,dtype=np.int32);_war=[]
for _i in range(n):
    _l=_inv.get(_i,[]);_wst[_i+1]=_wst[_i]+len(_l);_war+=_l
_regs=sorted(set(v_ for k_,v_ in dict(VL=VL,Q=Q,RPL=RPL,HD=HD,HIT=HIT,TGW=TGW,SECB=SECB,NUMT=NUMT,STY0=STY0,TBL=30000,MKT=MKT,STY=STY,DEFL=50000,MM1=60000,MM2=100000,FNB=FNB,XR=900000,ZT=ZT,HFB=HFB,FORD=FORD,FORD2=FORD2,RIDB=RIDB,CB=CB,CB2=1600000,SLOT0=SLOT0,UB=UB,OUTB=OUTB,IMG0=IMG0,SAVEB=SAVEB,OUTP=OUTP,PNGB=PNGB,AUXB=AUXB,RELB=RELB,CMB=CMB,FILE=FILE,BANK=BANK).items()))
json.dump(dict(regs=_regs,regn={str(v_):k_ for k_,v_ in dict(VL=VL,Q=Q,RPL=RPL,HD=HD,HIT=HIT,TGW=TGW,SECB=SECB,NUMT=NUMT,STY0=STY0,TBL=30000,MKT=MKT,STY=STY,DEFL=50000,MM1=60000,MM2=100000,FNB=FNB,XR=900000,ZT=ZT,HFB=HFB,FORD=FORD,FORD2=FORD2,RIDB=RIDB,CB=CB,CB2=1600000,SLOT0=SLOT0,UB=UB,OUTB=OUTB,IMG0=IMG0,SAVEB=SAVEB,OUTP=OUTP,PNGB=PNGB,AUXB=AUXB,RELB=RELB,CMB=CMB,FILE=FILE,BANK=BANK).items()},na=len(_aand),nas=len(_asr),nw=len(_war),stride=STRIDE,slotmax=SLOTMAX,len_=LEN),open('../build/dbg.json','w'))
with open('../build/dbg.bin','wb') as _f:
    for _arr in (np.array(_ast,dtype=np.int32),np.array(_asr,dtype=np.int32),np.array(_aw,dtype=np.float64),np.array(_ac,dtype=np.float64),np.array(_aand,dtype=np.int32),_wst,np.array(_war,dtype=np.int32)): _f.write(_arr.tobytes())
