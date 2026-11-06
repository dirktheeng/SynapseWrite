# ---- imp6: repeat ----
_g6=net.cur[0]; net.group('repeat last command')
e=S('FMTS'); fsm.set(i6lk,net.and_(e,ONE-net.eq(fm,8,e)),1)
fsm.set(i6lk,S('SETAL'),2); fsm.set(i6lk,S('T2_SA0'),3); fsm.set(i6lk,S('T2_LI'),4)
e=S('IMP6_RP')
on('IMP6_RP',(net.eq(i6lk,1,e),'FMTS',None),(net.eq(i6lk,2,e),'SETAL',None),(net.eq(i6lk,3,e),'T2_SA0',None),(net.eq(i6lk,4,e),'T2_LI',None),(None,'RD0',None))
net.group(_g6)
# ---- imp6: recent colors (registers and the menu rule are in imp6_recent.py) ----
_g6r=net.cur[0]; net.group('recent colors')
e=S('V4_HY'); _new=v4h+1
_dup=[net.eq(i6rc[j_],_new,e) for j_ in range(IMP6_NRC)]
fsm.set(i6rc[0],e,_new)
for k_ in range(1,IMP6_NRC):
    _bef=net.or_(*_dup[:k_])
    fsm.set(i6rc[k_],e,G_(i6rc[k_-1],e-_bef)+G_(i6rc[k_],_bef))
IMP6_RX,IMP6_RY=270,115+6*GC
def _rgb(v,e):
    b_=net.bits(v-net.step(v),24,e); has_=net.step(v)
    return tuple(sum((b_[o_+k_]*(1<<k_) for k_ in range(8)),X())+(ONE-has_)*255 for o_ in (16,8,0))
_ports=[rA,rB,rC,rD]
for h_ in range(2):
    st_=f'IMP6_RC{h_}'; e=S(st_)
    on(st_,(None,'IMP6_RC1' if h_==0 else 'T1_END',{_ports[q_]:(IMP6_RX+(4*h_+q_)*GC+4,IMP6_RY+4,GC-8,GC-8,_rgb(i6rc[4*h_+q_],e),254) for q_ in range(4)}))
net.group(_g6r)
