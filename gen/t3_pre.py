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
