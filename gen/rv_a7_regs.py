# Registers and undo rules for the bulk operations in rv_a7_bulk.py. Log records may hold a payload:
# [header op,p,o,n,st,grp][payload][footer, same six cells]. Undo reads the footer, redo the header.
# op 9: n paragraph slot pointers removed at index p. op 10: n characters and n styles deleted at p,o.
# op 11: run of n cells at p,o restyled from payload[0] to payload[1]. op 12: n characters of style st inserted at p,o.
A7Z=1388000; A7FREE=1384000   # 1100 cells that stay zero, then the stack of free paragraph slots
a7_n=R();a7_pa=R();a7_st=R();a7_c=R();a7_low=R();a7_ss=R();a7_sd=R();a7_sk=R();a7_dd=R();a7_re=R();a7_sv=R();a7_pre=R();a7_fs=R()
a7_rn=R();a7_ro=R();a7_rp=R();a7_rold=R();a7_rnew=R();a7_fv=R();a7_fk=R();a7_fo=R();a7_q0=R();a7_q1=R();a7_pn=R();a7_pp=R();a7_po=R();a7_sb=R()
a7r=Ret('A7_R');a7sr=Ret('A7_SR')
_e_sp=S('SPLIT')
A7_SPLIT=[(net.and_(net.ge(nextb,SLOTMAX,_e_sp),ONE-net.step(a7_fs),ONE-a7_re),'OR',None),(net.and_(net.gt(npar-cp-1,1100,_e_sp),ONE-a7_pre),'A7_SU0',{a7_ss:npar,a7_sd:cp+1101,a7_dd:1,a7_pre:1,a7sr.r:a7sr.id('SPLIT')}),
          (net.and_(net.step(a7_fs),ONE-a7_re),'A7_AL0',{r1:as_x(A7FREE)+a7_fs-1,a7_fs:a7_fs-1,a7_re:1,a7_sv:nextb})]
def a7_m5(e): w1.drive(e,(as_x(A7FREE)+a7_fs,cb)); fsm.set(a7_fs,e,a7_fs+1)
def a7_undo_rules(h):
    return [(h[9],'A7_U9',{usp:usp-uch-6,a7_n:uch,a7_ss:npar,a7_sd:up,a7_dd:uch,a7sr.r:a7sr.id('A7_U9B')}),
     (h[10],'UJ',{usp:usp-uch*2-6,a7_pa:usp-uch*2,a7_n:uch,a7_sb:1,jp:up,jo:uo,jret.r:jret.id('A7_BI0'),a7r.r:a7r.id('UCK')}),
     (h[11],'A7_U11',{a7_nd:ust,rc:usp-2,usp:usp-8,a7_fk:uch,a7_fo:uo,jp:up,jo:uo,a7r.r:a7r.id('UCK')}),
     (h[12],'UJ',{usp:usp-uch-6,a7_n:uch,jp:up,jo:uo,jret.r:jret.id('A7_BD0'),a7r.r:a7r.id('UCK')})]
def a7_redo_rules(h):
    return [(h[9],'A7_V9',{usp:usp+uch+6,npar:npar-uch,a7_ss:up+uch,a7_sd:up,a7_sk:npar-up-uch,a7sr.r:a7sr.id('A7_V9B')}),
     (h[10],'UJ',{usp:usp+uch*2+6,a7_n:uch,jp:up,jo:uo,jret.r:jret.id('A7_BD0'),a7r.r:a7r.id('VCK')}),
     (h[11],'A7_U11',{a7_nd:ust,rc:usp+0,usp:usp+8,a7_fk:uch,a7_fo:uo,a7_sb:1,jp:up,jo:uo+uch-1,a7r.r:a7r.id('VCK')}),
     (h[12],'UJ',{usp:usp+uch+6,a7_pa:usp,a7_n:uch,a7_sb:0,jp:up,jo:uo,jret.r:jret.id('A7_BI0'),a7r.r:a7r.id('VCK')})]
PSN=32; rpw=RPort(PSN); wpch=WPort(PSN,rpw.out[0],True); wpst=WPort(PSN,None,True)
a7_rs=R();a7_nd=R()
a7_png=R(); a7_rw2=RPort(PSN)
a7_far=R();a7_jmp=R();a7_wb=R();A7BUD=15000   # characters of layout one event may do before the rest goes to the background
