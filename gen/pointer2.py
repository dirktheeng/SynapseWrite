# pointer position and visibility come from the event; the colors under the sprite come back first
e=S('DISP')
_pmove=net.or_(kh[3],kh[4],kh[5],kh[11])
_pnz=net.step(eva+evb)
fsm.set(mp_ptx,net.and_(_pmove,_pnz),eva); fsm.set(mp_pty,net.and_(_pmove,_pnz),evb)
fsm.set(mp_ptr_on,net.and_(_pmove,_pnz,ONE-mp_ptr_lock),1)
fsm.set(mp_ptr_on,net.or_(net.and_(kh[11],ONE-_pnz),kh[12]),0)
ptrest.drive(net.and_(e,mp_ptr_dr),(mp_pts_x-PTHX,mp_pts_y-PTHY)); fsm.set(mp_ptr_dr,e,0)
fsm.set(mp_ptr_lock,net.and_(kh[12],net.eq(eva,1,e)),1); fsm.set(mp_ptr_lock,net.and_(kh[12],net.eq(eva,2,e)),0)
# clipboard notices: 1 read denied, 2 write failed. The message counts down on blink ticks and ends on a key or a click.
PMSG=9
_pn=net.step(pmsg)
fsm.set(pmsg,net.and_(kh[7],_pn),pmsg-1); fsm.set(pmsg,net.and_(net.or_(kh[2],kh[3]),_pn),0)
_kv=net.eq(eva,1,e); _hasi=net.step(clipn)
_ikey=net.and_(kh[8],_kv,_hasi,net.or_(clipi,net.eq(evc,0,e)))
PTR_DISP=[(kh[12],'T1_HH',None),
 (net.and_(kh[13],net.eq(eva,2,e)),'T1_HH',{clipi:1}),
 (net.and_(kh[13],_hasi),'CLI0',{pmsg:PMSG,cli:0}),(kh[13],'RD0',{pmsg:PMSG}),
 (_ikey,'CLI0',{cli:0}),
 (net.and_(bstg,kh[3]),'BS_MD',{hx_:eva,hy_:evb}),(net.and_(bstg,kh[2],net.eq(eva,27,e)),'UI',{bstg:0,clip0:0,clip1:0}),
 (net.and_(bstg,net.or_(kh[2],kh[5],kh[6],kh[7],kh[8],kh[9],kh[10])),'HALT',None),(net.and_(bstg,kh[4]),'HALT',{drag:0}),
 (net.and_(kh[4],t1_prs),'UI',{drag:0,t1_prs:0,t1_hvo:1,t1_nh:1,clip0:0,clip1:0})]
