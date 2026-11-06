# ---- imp6: repeat ----
_g6=net.cur[0]; net.group('repeat last command')
e=S('FMTS'); fsm.set(i6lk,net.and_(e,ONE-net.eq(fm,8,e)),1)
fsm.set(i6lk,S('SETAL'),2); fsm.set(i6lk,S('T2_SA0'),3); fsm.set(i6lk,S('T2_LI'),4)
e=S('IMP6_RP')
on('IMP6_RP',(net.eq(i6lk,1,e),'FMTS',None),(net.eq(i6lk,2,e),'SETAL',None),(net.eq(i6lk,3,e),'T2_SA0',None),(net.eq(i6lk,4,e),'T2_LI',None),(None,'RD0',None))
net.group(_g6)
