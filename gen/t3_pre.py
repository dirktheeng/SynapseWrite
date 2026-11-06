# helpers shared by the Tier 3 writers
off_=off;hlen_=hlen
T3_RETS=[];T3_WPORTS=[]
import t3_btn
def t3ret(n):
    r_=Ret(n); T3_RETS.append(r_); return r_
def floorv(val,en,nb=14):
    "Exact floor of a nonnegative value, by descending thresholds."
    rem=net.gate(val,en); out=X()
    for k_ in reversed(range(nb)):
        b_=net.step(rem-2**k_+1e-6); out=out+b_*(2**k_); rem=rem-b_*(2**k_)
    return out
# ---- number without leading zeros, shared by every XML writer ----
nret2=t3ret('T3_NR'); nvz=R()
cur_n='T3_NZ'
for pw_ in (10000000,1000000,100000,10000,1000,100,10,1):
    nx_=f'T3_NZ{pw_}' if pw_>1 else 'T3_NR'
    e=S(cur_n); val=net.gate(nvz,e)
    for big in (10000000,1000000,100000,10000,1000,100,10):
        if big>pw_:
            dd=X()
            for t in range(1,10): dd=dd+net.step(val-big*t+0.5)
            val=val-dd*big
    dg=X()
    for t in range(1,10): dg=dg+net.step(val-pw_*t+0.5)
    show=e if pw_==1 else net.step(net.gate(nvz,e)-pw_+0.5)
    em_en.lin(show); em_b.add(show,48+dg)
    on(cur_n,(None,nx_,None)); cur_n=nx_
def numz(st,val,nx): on(st,(None,'T3_NZ',{nvz:val,nret2.r:nret2.id(nx)}))
