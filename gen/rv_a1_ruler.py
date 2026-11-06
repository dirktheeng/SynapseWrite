# Ruler scale: quarter inch ticks, half inch marks and inch numbers, measured from the left text edge t1_rL.
# Each mark is one token; it shows only while its offset lies inside the text width t1_rW, so the scale follows margins, orientation and table cells.
_a1c=(138,136,134); _a1i=[]
for q_ in range(1,41):
    o_=q_*24
    if q_%4==0: _a1i.append(('g',o_-3,48+q_//4))
    else: _a1i.append(('r',o_,159 if q_%2==0 else 161,7 if q_%2==0 else 3))
_a1t=S('T1_RT'); fsm.states['T1_RT'][1].append((_a1t,None))
_a1s=[net.reg() for _ in range(len(_a1i)+1)]; net.rec(_a1s[0],_a1t)
for i_,it_ in enumerate(_a1i):
    t_=_a1s[i_]; sh_=net.gt(t1_rW,it_[1],t_)
    if it_[0]=='r': rA.drive(sh_,(t1_rL+it_[1],it_[2],1,it_[3],_a1c,0))
    else:
        g_en.lin(sh_); g_draw.lin(sh_); g_ch.lin(sh_*it_[2]); g_st.lin(sh_*rom.lit(11)); g_x.add(sh_,t1_rL+it_[1]); g_y.lin(sh_*(155+YB)); fg[1].lin(sh_); bg[0].lin(sh_)
    net.rec(_a1s[i_+1],t_)
net.rec(S('T1_RM0'),_a1s[-1])
