# the format menu, and what numbering.xml says
net.group('list formats')
on('V6_LM',(None,'T1_M0',{t1_mop:14,t1_mrow:99,t1_mtop:LFY,t1_mx:LFX,clip0:0,clip1:0}))
on('V6_LF',(None,'V6_LG',{r1:cb+LIST}))
e=S('V6_LG'); _lb=net.bits(R1,9,e); _kd=net.lt(alv,13,e)+1
on('V6_LG',(None,'SETLI',{alv:_kd+(_lb[2]+_lb[3]*2)*4+alv*16}))
e=S('V6_LT'); _pc0=net.eq(W[0],37,e); _pc1=net.eq(W[1],37,e); _sf=G_(W[2],_pc0)+G_(W[3],net.and_(ONE-_pc0,_pc1)); _sp=net.eq(_sf,41,e); _par=net.eq(W[0],40,e)
_nh=net.decode(v6nf,6,e)
_v=(net.and_(_nh[0],_par)*3+net.and_(_nh[0],ONE-_par,_sp)*2+net.and_(_nh[0],ONE-_par,ONE-_sp,net.step(_sf-40))*1+net.and_(_nh[0],ONE-_par,ONE-_sp,ONE-net.step(_sf-40))*12
 +_nh[1]*4+net.and_(_nh[1],net.or_(_sp,_par))*1+_nh[2]*6+net.and_(_nh[2],_sp)*1+_nh[3]*8+net.and_(_nh[3],net.or_(_sp,_par))*1+_nh[4]*10+net.and_(_nh[4],_sp)*1)
_cb=lambda c_:net.eq(W[0],c_,e)
_v=_v+G_(as_x(13)+_cb(111)*1+net.and_(_cb(0xE2),net.eq(W[2],0x93,e))*2+_cb(62)*3+_cb(42)*4+net.and_(_cb(0xC2),net.eq(W[1],0xB7,e))*5+net.and_(_cb(0xC2),net.eq(W[1],0xA7,e))*6+net.and_(_cb(38),net.eq(W[3],50,e),net.eq(W[5],49,e))*2+net.and_(_cb(38),net.eq(W[1],103,e))*3+net.and_(_cb(38),net.eq(W[2],49,e),net.eq(W[3],56,e))*5+net.and_(_cb(38),net.eq(W[2],49,e),net.eq(W[3],54,e))*6,_nh[5])
_dfl=net.step(net.and_(net.eq(t2lv,0,e),net.step(net.eq(_v,1,e)+net.eq(_v,13,e)))+net.and_(net.eq(t2lv,1,e),net.step(net.eq(_v,4,e)+net.eq(_v,14,e)))+net.and_(net.eq(t2lv,2,e),net.step(net.eq(_v,8,e)+net.eq(_v,15,e))))
_Fv=G_(_v,ONE-_dfl)+_dfl*62+net.and_(_dfl,_nh[5])*1
on('V6_LT',(net.lt(t2lv,3,e),'V6_LU',{v6nf:_Fv,r1:as_x(NUMT)+256+t2an}),(None,'PX',None))
e=S('V6_LU'); _lh=net.decode(t2lv,3,e); on('V6_LU',(None,'PX',{oi:oi+17,w1:(as_x(NUMT)+256+t2an,R1+G_(v6nf,_lh[0])+G_(v6nf,_lh[1])*64+G_(v6nf,_lh[2])*4096)}))
