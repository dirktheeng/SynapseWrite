# ---- bulk edits: whole blocks per tick, so a large operation costs per paragraph and not per character ----
net.group('bulk edits')
def a7_lead(bad,e):
    "How many leading cells pass: the failures are weighted by position so one threshold layer finds the first."
    sc=sum((b_*float(2**(PSN-1-i_)) for i_,b_ in enumerate(bad)),X())
    return e*PSN-sum((net.step(sc-float(2**(PSN-1-i_))+0.5) for i_ in range(PSN)),X())
def a7_log(c,at,op,p,o,n,st): wlog.drive(c,(at,op,p,o,n,st,grp))

def a7_adv(c,nx):
    fsm.set(usp,c,nx); fsm.set(urp,c,nx)
# paragraph table moves through the block port, one 1100 cell chunk per tick pair
_c=net.min_(net.relu(a7_ss-a7_sd),1100)
e=S('A7_SU0')
on('A7_SU0',(net.ge(a7_sd,a7_ss,e),'A7_SR',None),(None,'A7_SU1',{rb:(as_x(PT)+a7_ss-_c,_c)}))
on('A7_SU1',(None,'A7_SU0',{wb:(as_x(PT)+a7_ss-_c+a7_dd,_c),a7_ss:a7_ss-_c}))
_c2=net.min_(a7_sk,1100)
e=S('A7_SD0')
on('A7_SD0',(net.step(S('A7_SD0')-net.step(a7_sk)),'A7_SR',None),(None,'A7_SD1',{rb:(as_x(PT)+a7_ss,_c2)}))
on('A7_SD1',(None,'A7_SD0',{wb:(as_x(PT)+a7_sd,_c2),a7_ss:a7_ss+_c2,a7_sd:a7_sd+_c2,a7_sk:a7_sk-_c2}))
# a reused slot starts from zero cells, as a fresh one does
on('A7_AL0',(None,'A7_AL1',None))
fsm.set(nextb,S('A7_AL0'),R1)
on('A7_AL1',(None,'A7_AL2',{rb:(as_x(A7Z),1024)}))
on('A7_AL2',(None,'A7_AL3',{wb:(nextb+2048,1024),rb:(as_x(A7Z),1024)}))
on('A7_AL3',(None,'SPLIT',{wb:(nextb+3072,1024)}))
# delete part of a paragraph in one record
e=S('A7_D0'); same_=net.eq(cp,ap,e); _st0=G_(ao,same_)
on('A7_D0',(net.ge(usp,UEND_-2200,e),'A7_D0',{usp:UB,urp:UB}),(None,'A7_D1',{a7_st:_st0,a7_n:co-_st0,rb:(cb+_st0,co-_st0)}))
on('A7_D1',(None,'A7_D2',{wb:(usp+6,a7_n),rb:(cb+1024+a7_st,a7_n)}))
on('A7_D2',(None,'A7_D3',{wb:(usp+6+a7_n,a7_n),rb:(cb+co,clen-co)}))
on('A7_D3',(None,'A7_D4',{wb:(cb+a7_st,clen-co),rb:(cb+1024+co,clen-co)}))
e=S('A7_D4'); c_=net.and_(e,ONE-nolog); a7_log(c_,usp,10,cp,a7_st,a7_n,0)
on('A7_D4',(None,'A7_D5',{wb:(cb+1024+a7_st,clen-co),w3:(cb+LEN,clen-a7_n),w4:(cb+DIRTY,1),clen:clen-a7_n,co:a7_st}))
e=S('A7_D5'); c_=net.and_(e,ONE-nolog); a7_log(c_,usp+6+a7_n*2,10,cp,co,a7_n,0); a7_adv(c_,usp+12+a7_n*2); mark_d(e,cp)
on('A7_D5',(None,'DSL',None))
# remove whole paragraphs from the middle of a selection: their slots go to the log untouched,
# so undo restores pointers and the paragraphs keep their line breaks. Table cells stay on the old path.
e=S('A7_P1')
on('A7_P1',(net.step(rc.out[0]),'MG0',{oret.r:oret.id('DSL')}),(None,'A7_P2',{a7_c:cp-1,a7_low:cp,r1:as_x(PT)+cp-1}))
on('A7_P2',(None,'A7_P3',{rc:R1+2062}))
e=S('A7_P3')
on('A7_P3',(net.step(rc.out[0]),'A7_PX',None),(net.or_(net.ge(ap+1,a7_c,e),net.ge(cp-a7_c,1000,e)),'A7_PX',{a7_low:a7_c+1}),(None,'A7_P2',{a7_low:a7_c+1,a7_c:a7_c-1,r1:as_x(PT)+a7_c-1}))
e=S('A7_PX'); npr=cp-a7_low
on('A7_PX',(net.step(S('A7_PX')-net.step(npr)),'MG0',{oret.r:oret.id('DSL')}),(net.ge(usp,UEND_-2200,e),'A7_PX',{usp:UB,urp:UB}),(None,'A7_P6',{rb:(as_x(PT)+a7_low,npr)}))
e=S('A7_P6'); c_=net.and_(e,ONE-nolog); a7_log(c_,usp,9,a7_low,0,npr,0)
on('A7_P6',(None,'A7_P7',{wb:(usp+6,npr)}))
e=S('A7_P7'); c_=net.and_(e,ONE-nolog); a7_log(c_,usp+6+npr,9,a7_low,0,npr,0); a7_adv(c_,usp+12+npr); mark_d(e,a7_low)
on('A7_P7',(None,'A7_SD0',{a7_ss:cp,a7_sd:a7_low,a7_sk:npar-cp,npar:npar-npr,cp:a7_low,a7sr.r:a7sr.id('DSL')}))
# undo and redo of those
on('A7_U9',(None,'A7_SU0',None))
on('A7_U9B',(None,'A7_U9C',{rb:(usp+6,a7_n)}))
e=S('A7_U9C'); mark_d(e,up)
on('A7_U9C',(None,'J0',{wb:(as_x(PT)+up,a7_n),npar:npar+a7_n,jp:up+a7_n,jo:0,jret.r:jret.id('UCK')}))
e=S('A7_V9'); mark_d(e,up)
on('A7_V9',(None,'A7_SD0',None))
on('A7_V9B',(None,'J0',{jp:up,jo:0,jret.r:jret.id('VCK')}))
# insert a logged block at the caret
on('A7_BI0',(None,'A7_BI1',{rb:(cb+co,clen-co)}))
on('A7_BI1',(None,'A7_BI2',{wb:(cb+co+a7_n,clen-co),rb:(cb+1024+co,clen-co)}))
on('A7_BI2',(None,'A7_BI3',{wb:(cb+1024+co+a7_n,clen-co),rb:(a7_pa,a7_n)}))
e=S('A7_BI3'); mark_d(e,cp)
_bi={wb:(cb+co,a7_n),w3:(cb+LEN,clen+a7_n),w4:(cb+DIRTY,1),clen:clen+a7_n,co:co+a7_n}
on('A7_BI3',(a7_sb,'A7_BI4',{**_bi,rb:(a7_pa+a7_n,a7_n)}),(None,'A7_FILL',{**_bi,a7_fv:ust,a7_fk:a7_n,a7_fo:co}))
on('A7_BI4',(None,'A7_R',{wb:(cb+1024+co-a7_n,a7_n),a7_sb:0}))
# delete a block at the caret, no log
on('A7_BD0',(None,'A7_BD1',{rb:(cb+co+a7_n,net.relu(clen-co-a7_n))}))
on('A7_BD1',(None,'A7_BD2',{wb:(cb+co,net.relu(clen-co-a7_n)),rb:(cb+1024+co+a7_n,net.relu(clen-co-a7_n))}))
e=S('A7_BD2'); mark_d(e,cp)
on('A7_BD2',(None,'A7_R',{wb:(cb+1024+co,net.relu(clen-co-a7_n)),w3:(cb+LEN,clen-a7_n),w4:(cb+DIRTY,1),clen:clen-a7_n}))
# one value across a run of style cells, 32 per tick. The paste port's style wires carry it.
e=S('A7_FILL'); _fn=net.min_(a7_fk,PSN); _fg=G_(a7_fv,e)
for w_ in _st: net.connect(w_,_fg)
wpst.drive(net.and_(e,net.step(a7_fk)),(cb+1024+a7_fo,_fn))
on('A7_FILL',(net.gt(a7_fk,PSN,e),'A7_FILL',{a7_fo:a7_fo+PSN,a7_fk:a7_fk-PSN}),(a7_nd,'A7_R',{a7_fk:0,a7_nd:0}),(None,'A7_R',{w4:(cb+DIRTY,1),a7_fk:0}))
# op 11: payload is old value, new value. Undo takes the first, redo the second.
on('A7_U11',(None,'UJ',{a7_fv:G_(rc.out[1],a7_sb)+G_(rc.out[0],ONE-a7_sb),a7_sb:0,jret.r:jret.id('A7_U13')}))
e=S('A7_U13'); mark_d(net.and_(e,ONE-a7_nd),cp)
on('A7_U13',(None,'A7_FILL',None))
# range walker, formatting: runs of equal style are read, changed and written by the window, and
# logged as one record per run, so a uniform paragraph is one record.
e=S('A7_FW'); WIN=rpw.out; fin.add(e,WIN[0]); fen.lin(e)
_nw=a7_lead([X()]+[net.step(WIN[i_]-WIN[0]-0.5+e*M-M)+net.step(WIN[0]-WIN[i_]-0.5+e*M-M) for i_ in range(1,PSN)],e)
_rem=wlen-wo; _sp=net.eq(wp,hi_p,e); _rem2=_rem-net.relu(_rem-(hi_o-wo)+_sp*M-M); _nf=_nw-net.relu(_nw-_rem2+e*M-M)
_dif=net.and_(net.step(a7_rn),net.step(net.step(WIN[0]-a7_rold)+net.step(a7_rold-WIN[0])))
e_ok=net.and_(e,ONE-_dif); _ng=G_(newst,e_ok)
for w_ in _st: net.connect(w_,_ng)
_fmsafe=net.step(fmh[3]+fmh[7]+fmh[11]+fmh[12]+fmh[15]); _e_d=net.and_(e_ok,ONE-_fmsafe)
wpst.drive(e_ok,(wbase+1024+wo,_nf)); w3.drive(_e_d,(wbase+DIRTY,1)); mark_d(_e_d,wp)
fsm.set(ftgt,e_ok,tgt_now); fsm.set(wfirst,e_ok,0)
_fr=net.and_(e_ok,ONE-net.step(a7_rn)); fsm.set(a7_ro,_fr,wo); fsm.set(a7_rold,_fr,WIN[0]); fsm.set(a7_rnew,_fr,_ng); fsm.set(a7_rp,_fr,wp); fsm.set(a7_rs,_fr,_fmsafe)
on('A7_FW',(_dif,'A7_FL',None),(None,'W3',{wo:wo+_nf,a7_rn:a7_rn+_nf}))
e=S('A7_FL'); c_=net.and_(e,ONE-nolog); a7_log(c_,usp,11,a7_rp,a7_ro,a7_rn,a7_rs); w1.drive(c_,(usp+6,a7_rold)); w2.drive(c_,(usp+7,a7_rnew))
on('A7_FL',(None,'A7_FM',None))
e=S('A7_FM'); c_=net.and_(e,ONE-nolog); a7_log(c_,usp+8,11,a7_rp,a7_ro,a7_rn,a7_rs); _wr=net.ge(usp,UEND_-100,c_); a7_adv(c_,G_(usp+14,c_-_wr)+_wr*UB)
on('A7_FM',(None,'W3',{a7_rn:0}))
# range walker, copy: plain characters go by the window
e=S('A7_CW')
_nc=a7_lead([net.step(as_x(32)-WIN[i_]-0.5+e*M-M)+net.step(WIN[i_]-126.5+e*M-M) for i_ in range(PSN)],e)
_rem=wlen-wo; _sp=net.eq(wp,hi_p,e); _rem2=_rem-net.relu(_rem-(hi_o-wo)+_sp*M-M); _nf=_nc-net.relu(_nc-_rem2+e*M-M)
wpch.drive(net.and_(e,net.step(_nc)),(as_x(CB)+wn,_nf))
on('A7_CW',(net.step(_nc),'W3',{wo:wo+_nf,wn:wn+_nf}),(None,'W4',{r1:wbase+wo,r2:wbase+1024+wo}))
# find: the first query character, in either case, is looked for across a window
e=S('A7_FQ1'); _lq=low(R1,e); _al=net.and_(ONE-t1_case,net.or_(net.and_(net.ge(_lq,97,e),net.lt(_lq,123,e)),net.and_(net.ge(_lq,224,e),net.lt(_lq,255,e),ONE-net.eq(_lq,247,e))))
on('A7_FQ1',(None,'F0',{a7_q0:_lq,a7_q1:_lq-_al*32}))
e=S('A7_FF')
_cd=[]
for i_ in range(PSN):
    a_=net.step(WIN[i_]-a7_q0-0.5+e*M-M)+net.step(a7_q0-WIN[i_]-0.5+e*M-M); b_=net.step(WIN[i_]-a7_q1-0.5+e*M-M)+net.step(a7_q1-WIN[i_]-0.5+e*M-M)
    _cd.append(net.step(as_x(1.5)-a_-b_+e*M-M))
_nq=a7_lead(_cd,e)
on('A7_FF',(net.step(_nq),'F3',{fo:fo+_nq}),(None,'F4',{r1:fbs+fo+fk,r2:as_x(Q)+fk}))
# paste record, written when the block run ends
e=S('A7_PF'); c_=net.and_(e,ONE-nolog); a7_log(c_,usp,12,a7_pp,a7_po,a7_pn,TST)
on('A7_PF',(None,'A7_PG',None))
e=S('A7_PG'); c_=net.and_(e,ONE-nolog); a7_log(c_,usp+6+a7_pn,12,a7_pp,a7_po,a7_pn,TST); a7_adv(c_,usp+12+a7_pn)
on('A7_PG',(None,'PS2',{a7_pn:0}))
