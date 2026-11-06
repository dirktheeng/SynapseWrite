# Find across paragraphs. In the query, ^p stands for a paragraph mark, as in Word. A query with a mark can only start where its
_g0=net.cur[0]
# first mark lands on the end of a paragraph, so each paragraph has one candidate start: its length minus the characters before the mark.
# One matcher serves the find walker, the match counter and the paint highlight, with a return table of its own.
net.group('find across paragraphs')
zxret=Ret('IMP3_XR')
exec(open('p1_find_pre.py').read())
# facts about the query, recomputed when it changes
QMAX=190
on('IMP3_Q0',(None,'IMP3_Q1',{qsi:0,qs_:0,qnm:0,qseg0:0,qsegL:0,qcod:0}))
e=S('IMP3_Q1'); on('IMP3_Q1',(net.ge(qsi,qlen,e),'RD0',{qmrk:net.step(qnm+qcod),qseg0:G_(qseg0,net.step(qnm))+G_(qs_,e-net.step(qnm)),qsegL:qs_}),(None,'IMP3_Q2',{r1:as_x(Q)+qsi}))
e=S('IMP3_Q2'); on('IMP3_Q2',(net.and_(net.eq(R1,94,e),net.lt(qsi+1,qlen,e)),'IMP3_Q3',{r1:as_x(Q)+qsi+1}),(None,'IMP3_Q1',{qsi:qsi+1,qs_:qs_+1}))
e=S('IMP3_Q3'); _fm=net.and_(e,ONE-net.step(qnm)); on('IMP3_Q3',(p1_code(R1,e),'IMP3_Q1',{qsi:qsi+2,qs_:qs_+1,qcod:qcod+1}),(net.eq(R1,112,e),'IMP3_Q1',{qsi:qsi+2,qs_:0,qnm:qnm+1,qseg0:G_(qs_,_fm)+G_(qseg0,e-_fm)}),(None,'IMP3_Q1',{qsi:qsi+1,qs_:qs_+1}))
# the matcher: from paragraph xp, base zxb, length zxl, offset xo. xok says whether the whole query matched; xp and xo then hold its end
on('IMP3_X',(None,'IMP3_X0',{xq:0,xsb:zxb,xso:xo,xok:0}))
e=S('IMP3_X0'); on('IMP3_X0',(net.ge(xq,qlen,e),'IMP3_XW',None),(None,'IMP3_X1',{r2:as_x(Q)+xq}))
e=S('IMP3_X1'); on('IMP3_X1',(net.and_(net.eq(R2,94,e),net.lt(xq+1,qlen,e)),'IMP3_X2',{r2:as_x(Q)+xq+1,xc:94}),(net.ge(xo,zxl,e),'IMP3_XR',None),(None,'IMP3_X3',{xc:R2,r1:zxb+xo}))
e=S('IMP3_X2'); on('IMP3_X2',(p1_code(R2,e),'P1_XC',{xc:p1_lit(R2,e),p1k:p1_kind(R2,e)}),(ONE-net.eq(R2,112,e),'IMP3_X2L',None),(net.lt(xo,zxl,e),'IMP3_XR',None),(net.ge(xp+1,npar,e),'IMP3_XR',None),(None,'IMP3_X5',{r1:as_x(PT)+xp+1,xq:xq+2,xp:xp+1}))
e=S('IMP3_X2L'); on('IMP3_X2L',(net.ge(xo,zxl,e),'IMP3_XR',None),(None,'IMP3_X3',{r1:zxb+xo}))
on('IMP3_X5',(None,'IMP3_X6',{zxb:R1,r2:R1+LEN}))
on('IMP3_X6',(None,'IMP3_X0',{zxl:R2,xo:0}))
e=S('IMP3_X3'); on('IMP3_X3',(net.eq(low(R1,e),low(xc,e),e),'IMP3_X0',{xq:xq+1,xo:xo+1}),(None,'IMP3_XR',None))
on('IMP3_XW',(t1_fw,'IMP3_XW1',{r1:xsb+net.relu(xso-1),r2:zxb+xo}),(None,'IMP3_XR',{xok:1}))
e=S('IMP3_XW1'); on('IMP3_XW1',(net.and_(net.or_(net.eq(xso,0,e),ONE-t1_isw(R1,e)),net.or_(net.ge(xo,zxl,e),ONE-t1_isw(R2,e))),'IMP3_XR',{xok:1}),(None,'IMP3_XR',None))
# find walker
e=S('IMP3_F0'); _c=fl-qseg0
on('IMP3_F0',(net.eq(qnm,0,e),'P1_F0',None),(net.or_(net.gt(qseg0,fl,e),net.gt(fo,fl-qseg0+0,e)),'F0',{fp:fp+1,fo:0}),(None,'IMP3_X',{xp:fp,zxb:fbs,zxl:fl,xo:_c,xcand:_c,zxret.r:zxret.id('IMP3_F1')}))
on('IMP3_F1',(xok,'FJ',{ap:fp,ao:xcand,jp:xp,jo:xo,jret.r:jret.id('FOUND')}),(None,'F0',{fp:fp+1,fo:0}))
# match counter
e=S('IMP3_C0'); _c=t1_cl-qseg0
on('IMP3_C0',(net.eq(qnm,0,e),'P1_C0',None),(net.or_(net.gt(qseg0,t1_cl,e),net.gt(t1_co_,t1_cl-qseg0+0,e)),'T1_C1',{t1_cw:t1_cw+1,t1_co_:0,t1_cb:t1_cb+1}),(None,'IMP3_X',{xp:t1_cw,zxb:t1_cB,zxl:t1_cl,xo:_c,xcand:_c,t1_cb:t1_cb+qlen,zxret.r:zxret.id('IMP3_C1')}))
e=S('IMP3_C1'); on('IMP3_C1',(xok,'T1_C1',{t1_cn:t1_cn+1,t1_ci:t1_ci+net.and_(net.ge(Lo,t1_cw*2048+xcand,e),has_sel),t1_cw:xp,t1_co_:xo}),(None,'T1_C1',{t1_cw:t1_cw+1,t1_co_:0}))
# a search that ends in the query text goes through the same facts; pasting into the bar, and marks in the replacement
on('IMP3_P0',(None,'IMP3_P1',{pi_:0}))
e=S('IMP3_P1'); on('IMP3_P1',(net.ge(pi_,evc,e),'IMP3_Q0',None),(None,'IMP3_P2',{r1:as_x(CB2)+pi_}))
e=S('IMP3_P2')
_tgt=G_(as_x(RPL)+rlen,field)+G_(as_x(Q)+qlen,e-net.and_(e,field)); _tl=G_(rlen,field)+G_(qlen,e-net.and_(e,field))
_nl=net.eq(R1,10,e); _bad=net.and_(net.lt(R1,32,e),ONE-net.eq(R1,9,e),ONE-_nl)
_lim=net.ge(_tl+2,QMAX,e)
_cf=net.and_(e,field); _cq=e-_cf
_adv=lambda n_:{qlen:qlen+G_(as_x(n_),_cq),rlen:rlen+G_(as_x(n_),_cf)}
on('IMP3_P2',(net.or_(_bad,_lim),'IMP3_P1',{pi_:pi_+1}),(_nl,'IMP3_P3',{w1:(_tgt,94),w2:(_tgt+1,112),pi_:pi_+1,**_adv(2)}),(None,'IMP3_P1',{w1:(_tgt,um_out+G_(R1,net.eq(R1,9,e))),pi_:pi_+1,**_adv(1)}))
um_en.lin(e); um_in.add(e,R1)
on('IMP3_P3',(None,'IMP3_P1',None))
on('IMP3_RQ',(field,'IMP3_P0',{qrep:0}),(qrep,'IMP3_P0',{qlen:0,qrep:0,**CSTART}),(None,'IMP3_P0',CSTART))
e=S('RP3'); on('RP3',(net.and_(net.eq(R1,94,e),net.lt(ri+1,rlen,e)),'IMP3_R1',{r1:as_x(RPL)+ri+1}),(None,'INS',{ins_ch:R1,ins_st:TST,ri:ri+1,oret.r:oret.id('RP2')}))
e=S('IMP3_R1'); on('IMP3_R1',(net.and_(p1_code(R1,e),ONE-net.step(p1_kind(R1,e))),'INS',{ins_ch:p1_lit(R1,e),ins_st:TST,ri:ri+2,oret.r:oret.id('RP2')}),(net.eq(R1,112,e),'SPLIT',{ri:ri+2,oret.r:oret.id('RP2')}),(None,'INS',{ins_ch:94,ins_st:TST,ri:ri+1,oret.r:oret.id('RP2')}))
net.group(_g0)
