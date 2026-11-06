# ---- the mouse pointer: drawn by the network, kept out of the id plane ----
# The sprite is a patch write, which never touches alpha, so hit tests read true ids at all times.
# Every event starts by restoring the colors under the sprite and ends by saving them and drawing again.
net.group('pointer')
PTW,PTH,PTHX,PTHY=28,30,12,10; PTRB=1390000       # patch size, hot spot in the patch, saved colors in the bank
bstg=R();bsq=R();bsn=R();clipn=R();clipi=R();pmsg=R();t1_prs=R();cli=R();mp_ptx=R();mp_pty=R();mp_pts_x=R();mp_pts_y=R();mp_ptr_on=R();mp_ptr_dr=R();mp_ptr_lock=R();mp_ptq=R();mp_pta=R();mp_ptc=R();mp_ptk=R();mp_ptv=R()
ptsave=CopyPort(ZERO_R,ZERO_R); ptrest=CopyPort(ZERO_R,ZERO_R)   # no clip, whole screen
on('HALT',(a11busy,'A11_T3',None),*RV_HALT,(bsq,'UI',{bsq:0,bstg:0,clip0:0,clip1:0}),(mp_ptr_on,'PT0',{mp_pts_x:mp_ptx,mp_pts_y:mp_pty,mp_ptr_dr:1,pix:(mp_ptx,mp_pty),ptsave:(mp_ptx-PTHX,mp_pty-PTHY,PTRB,PTW,PTH,0)}),(None,'HF',None))
on('HF',(None,'IDLE',None)); halt.lin(S('HF'))
