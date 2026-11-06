# ---- rv_a6: tracked paragraph marks, author and date on revisions, live fields, merge fields ----
# Slot cell PMK holds the paragraph mark revision: 0 none, 1 inserted, 2 deleted. PDATE holds the day of the last tracked edit, PAUTH an index into the author table.
AUTHB=1320000; AUW=64
w4.drive(net.and_(S('AFTER_ED'),trk),(cb+PDATE,evt))
fsm.set(trk,S('OP0'),0)
# ---- writer: author and date attributes. Called with the id already written ----
a6y=R();a6mm=R();a6dd=R();a6lp=R();a6ai=R();a6al=R();a6ab=R();a6dv=R();a6ml=R()
on('A6T_A0',(None,'A6T_A1',{r1:pbs+PDATE,r2:pbs+PAUTH}))
e=S('A6T_A1'); _hd=net.step(R1); on('A6T_A1',(None,'A6T_A1b',{a6dv:G_(R1,_hd)+G_(evt,e-net.and_(e,_hd)),a6ab:as_x(AUTHB)+R2*AUW,a6ai:R2}))
lit('A6T_A1b',b'" w:author="','A6T_A2')
e=S('A6T_A2'); on('A6T_A2',(net.step(a6ai),'A6T_A3',{r1:a6ab}),(None,'A6T_A9',None))
lit('A6T_A9',b'SynapseWrite','A6T_B0')
on('A6T_A3',(None,'A6T_A4',{a6al:R1,a6ai:0}))
e=S('A6T_A4'); on('A6T_A4',(net.ge(a6ai,a6al,e),'A6T_B0',None),(None,'A6T_A5',{r1:a6ab+1+a6ai,a6ai:a6ai+1}))
e=S('A6T_A5'); em_en.lin(e); em_b.add(e,R1); on('A6T_A5',(None,'A6T_A4',None))
lit('A6T_B0',b'" w:date="','A6T_Y0')
# days since 1970 to a civil date, by the same year and month loop as the date field
on('A6T_Y0',(None,'A6T_Y1',{a6y:1970}))
e=S('A6T_Y1'); _yb=net.bits(a6y,12,e); _lp=net.and_(e,ONE-_yb[0],ONE-_yb[1]); _yd=365+_lp
on('A6T_Y1',(net.ge(a6dv,_yd,e),'A6T_Y1',{a6dv:a6dv-_yd,a6y:a6y+1}),(None,'A6T_Y2',{a6mm:1,a6lp:_lp}))
e=S('A6T_Y2'); _mh=net.decode(a6mm,13,e); _ml=X()
for m_,d_ in enumerate((31,28,31,30,31,30,31,31,30,31,30,31),1): _ml=_ml+_mh[m_]*d_
_ml=_ml+G_(a6lp,net.step(_mh[2]))
on('A6T_Y2',(net.ge(a6dv,_ml,e),'A6T_Y2',{a6dv:a6dv-_ml,a6mm:a6mm+1}),(None,'A6T_Y3',None))
numz('A6T_Y3',a6y,'A6T_Y4')
def _two(st,reg,nx):
    n1=st+'a';n2=st+'b'
    e=S(st); on(st,(net.lt(reg,10,e),n1,None),(None,n2,None))
    lit(n1,b'0',n2); numz(n2,reg,nx)
lit('A6T_Y4',b'-','A6T_Y5'); _two('A6T_Y5',a6mm,'A6T_Y6'); lit('A6T_Y6',b'-','A6T_Y7'); _two('A6T_Y7',a6dv+1,'A6T_Y8'); lit('A6T_Y8',b'T00:00:00Z"','A6T_AR')

# paragraph mark inside pPr
on('T2Wa',(None,'A6T_P0',{r1:pbs+PMK}))
e=S('A6T_P0'); on('A6T_P0',(net.step(scols),'T3_SNA',None),(net.eq(R1,1,e),'A6T_P1',None),(net.eq(R1,2,e),'A6T_P2',None),(None,'T3_SNA',None))
lit('A6T_P1',b'<w:rPr><w:ins w:id="','A6T_P3'); lit('A6T_P2',b'<w:rPr><w:del w:id="','A6T_P3')
number('A6T_P3',t4id,'A6T_P4'); on('A6T_P4',(None,'A6T_A0',{t4id:t4id+1,a6ar.r:a6ar.id('A6T_P5')})); lit('A6T_P5',b'/></w:rPr>','T3_SNA')
# ---- reader: self closed marks, author and date ----
a6ac=R();a6ak=R();a6ai2=R()
fsm.set(a6ac,S('OP0'),0)
_arow=lambda k_:as_x(AUTHB)+k_*AUW
on('A6R_A0',(None,'A6R_A1',{r1:OA+oi}))
e=S('A6R_A1'); on('A6R_A1',(net.eq(R1,34,e),'A6R_A2',{oi:oi+1}),(net.ge(a6an,AUW-2,e),'A6R_A0',{oi:oi+1}),(None,'A6R_A0',{oi:oi+1,w1:(_arow(a6ac+1)+1+a6an,R1),a6an:a6an+1}))
on('A6R_A2',(None,'A6R_A3',{w1:(_arow(a6ac+1),a6an),a6ak:1}))
e=S('A6R_A3'); on('A6R_A3',(net.gt(a6ak,a6ac,e),'A6R_AN',None),(None,'A6R_A4',{r1:_arow(a6ak)}))
e=S('A6R_A4'); on('A6R_A4',(net.eq(R1,a6an,e),'A6R_A5',{a6ai2:0}),(None,'A6R_A3',{a6ak:a6ak+1}))
e=S('A6R_A5'); on('A6R_A5',(net.ge(a6ai2,a6an,e),'T4_TS',{w1:(cb+PAUTH,a6ak)}),(None,'A6R_A6',{r1:_arow(a6ak)+1+a6ai2,r2:_arow(a6ac+1)+1+a6ai2}))
e=S('A6R_A6'); on('A6R_A6',(net.eq(R1,R2,e),'A6R_A5',{a6ai2:a6ai2+1}),(None,'A6R_A3',{a6ak:a6ak+1}))
e=S('A6R_AN'); on('A6R_AN',(net.ge(a6ac,15,e),'T4_TS',None),(None,'T4_TS',{w1:(cb+PAUTH,a6ac+1),a6ac:a6ac+1}))
on('A6R_D0',(None,'A6R_D1',{rl:OA+oi,r1:OA+oi+8,r2:OA+oi+9}))
e=S('A6R_D1'); W7=rl.out
_y=(W7[0]-48)*1000+(W7[1]-48)*100+(W7[2]-48)*10+(W7[3]-48); _m=(W7[5]-48)*10+(W7[6]-48); _d=(R1-48)*10+(R2-48)
_yy=net.gate(_y,e); _b=net.bits(net.relu(_yy-1969),8,e); _q=sum((_b[i_+2]*(1<<i_) for i_ in range(6)),X())
_lb=net.bits(_yy,2,e); _ly=net.and_(e,ONE-_lb[0],ONE-_lb[1]); _mhr=net.decode(_m,13,e); _cum=X(); _c=0
for m_,d_ in enumerate((31,28,31,30,31,30,31,31,30,31,30,31),1): _cum=_cum+_mhr[m_]*_c; _c+=d_
_late=sum((_mhr[m_] for m_ in range(3,13)),X())
_days=net.relu(_yy-1970)*365+_q+_cum+net.step(_late+_ly-1.5)+net.relu(_d-1)
on('A6R_D1',(None,'T4_TS',{w1:(cb+PDATE,_days+1),oi:oi+10}))

# ---- tracked Backspace and Delete across a paragraph mark ----
a6t=R();a6tc=R();a6q=R()
on('A6T_BK',(None,'A6T_BK1',{r1:as_x(PT)+cp-1,rc:cb+2062}))
on('A6T_BK1',(None,'A6T_BK2',{a6t:R1,a6tc:rc.out[0],r2:R1+PMK,rf:R1+2062}))
e=S('A6T_BK2'); _tb=net.step(a6tc+rf.out[0]); _i1=net.and_(e,ONE-_tb,net.eq(R2,1,e)); _mk=net.and_(e,ONE-_tb,ONE-_i1)
log(_mk,7,a6t+PMK,0,R2,2)
on('A6T_BK2',(_tb,'MVJ',{jp:cp-1,jo:2047,jret.r:jret.id('AFTER_ED')}),(_i1,'MG0',{oret.r:oret.id('AFTER_ED')}),(None,'MVJ',{w1:(a6t+PMK,2),jp:cp-1,jo:2047,jret.r:jret.id('AFTER_ED')}))
on('A6T_DK',(None,'A6T_DK1',{r2:cb+PMK,rc:cb+2062}))
e=S('A6T_DK1'); _tb=net.step(rc.out[0]); _i1=net.and_(e,ONE-_tb,net.eq(R2,1,e)); _mk=net.and_(e,ONE-_tb,ONE-_i1)
log(_mk,7,cb+PMK,0,R2,2)
on('A6T_DK1',(_tb,'MVJ',{jp:cp+1,jo:0,jret.r:jret.id('AFTER_ED')}),(_i1,'DK2',{jp:cp+1,jo:0,jret.r:jret.id('DK3')}),(None,'MVJ',{w1:(cb+PMK,2),jp:cp+1,jo:0,jret.r:jret.id('AFTER_ED')}))
# a tracked deletion of a selection also marks the paragraph marks inside it
on('T4_DS1',(None,'A6T_SL',{a6q:lo_p}))
e=S('A6T_SL'); on('A6T_SL',(net.ge(a6q,hi_p,e),'MVJ',{jp:hi_p,jo:hi_o,jret.r:jret.id('T4_DS2')}),(None,'A6T_S1',{r1:as_x(PT)+a6q}))
on('A6T_S1',(None,'A6T_S2',{a6t:R1,r2:R1+PMK,rc:R1+2062}))
e=S('A6T_S2'); _mk=net.and_(e,ONE-net.step(rc.out[0]),net.eq(R2,0,e)); log(_mk,7,a6t+PMK,0,0,2)
on('A6T_S2',(_mk,'A6T_SL',{w1:(a6t+PMK,2),a6q:a6q+1}),(None,'A6T_SL',{a6q:a6q+1}))
# ---- accept and reject of paragraph marks, at the end of each paragraph in the range ----
e=S('T4_AL')
on('T4_AL',(net.and_(net.eq(cp,a_ep,e),net.ge(co,a_eo,e)),'T4_AE',None),(net.ge(co,clen,e),'A6T_M1',{r2:cb+PMK,rc:cb+2062}),(None,'T4_AM',{r1:cb+co,r2:cb+1024+co}))
e=S('A6T_M1'); _pt=ONE-net.step(rc.out[0]); _nx=net.lt(cp,a_ep,e); _ml1=net.eq(R2,1,e); _ml2=net.eq(R2,2,e)
_rm=net.and_(e,_pt,net.or_(net.and_(arj,_ml1),net.and_(ONE-arj,_ml2)))
_mk=net.and_(e,_pt,net.step(R2)); log(_mk,7,cb+PMK,0,R2,0)
_w0={w1:(cb+PMK,0),w2:(cb+DIRTY,1)}
on('A6T_M1',(net.and_(_rm,net.lt(cp+1,npar,e)),'J0',{**_w0,jp:cp+1,jo:0,jret.r:jret.id('A6T_M2')}),
 (net.and_(_mk,_nx),'J0',{**_w0,jp:cp+1,jo:0,jret.r:jret.id('T4_AL')}),(_mk,'T4_AE',_w0),(_nx,'J0',{jp:cp+1,jo:0,jret.r:jret.id('T4_AL')}),(None,'T4_AE',None))
on('A6T_M2',(None,'MERGE',{oret.r:oret.id('A6T_M3')}))
on('A6T_M3',(None,'T4_AL',{a_ep:net.relu(a_ep-1),fastok:0}))
# ---- live fields: after a pause, a change in the word or page total refreshes every field run, without touching undo ----
fsm.set(a6hf,S('T4_FI'),1); fsm.set(a6hf,net.step(rfk),1)
on('T4_AF',(a6fg,'RD0',{a6fg:0,nolog:0,lc:1,fastok:0,ap:cp,ao:co}),(None,'AFTER_ED',{fastok:0}))
_e=net.and_(S('D3'),a6fg); _e1=net.and_(_e,net.eq(cp,a_sp,_e),net.lt(co,a_so,_e)); fsm.set(a_so,_e1,a_so-1)
_e=net.and_(S('I2'),a6fg); _e1=net.and_(_e,net.eq(cp,a_sp,_e),net.ge(a_so,co,_e)); fsm.set(a_so,_e1,a_so+1)
# ---- writer: a merge field is the characters between the guillemets ----
_nmc=lambda v,en: net.or_(net.and_(net.ge(v,65,en),net.lt(v,91,en)),net.and_(net.ge(v,97,en),net.lt(v,123,en)),net.and_(net.ge(v,48,en),net.lt(v,58,en)),net.eq(v,95,en))
fsm.set(a6wp,S('SVch'),0)
e=S('A6W_0'); on('A6W_0',(net.ge(a6wk,plen_,e),'A6W_PL',None),(None,'A6W_1',{r1:pbs+a6wk}))
e=S('A6W_1'); on('A6W_1',(net.and_(net.eq(R1,187,e),net.gt(a6wk,a6off+1,e)),'A6W_2',None),(_nmc(R1,e),'A6W_0',{a6wk:a6wk+1}),(None,'A6W_PL',None))
on('A6W_PL',(None,'SVr',{a6wp:1,r1:pbs+a6off,r2:pbs+1024+a6off}))
e=S('A6W_2'); on('A6W_2',(net.eq(t2psv,99999,e),'A6W_3',None),(None,'T4_SC',{t4cr.r:t4cr.id('A6W_3')}))
on('A6W_3',(None,'A6W_4',{t2psv:99999,a6ai:a6off+1}))
lit('A6W_4',b'<w:fldSimple w:instr=" MERGEFIELD ','A6W_5')
def _a6copy(st,nx):
    e=S(st); on(st,(net.ge(a6ai,a6wk,e),nx,None),(None,st+'r',{r1:pbs+a6ai,a6ai:a6ai+1}))
    e=S(st+'r'); em_en.lin(e); em_b.add(e,R1); on(st+'r',(None,st,None))
_a6copy('A6W_5','A6W_6')
lit('A6W_6',b' "><w:r>','A6W_7')
on('A6W_7',(None,'T2RP',{t2full:net.step(psty),t2pr.r:t2pr.id('A6W_8'),a6ai:a6off+1}))
lit('A6W_8',b'<w:t>\xc2\xab','A6W_9')
_a6copy('A6W_9','A6W_A')
lit('A6W_A',b'\xc2\xbb</w:t></w:r></w:fldSimple>','A6W_B')
on('A6W_B',(None,'SVC',{a6off:a6wk+1}))
# ---- Insert Merge Field: a pair of guillemets with the caret between them ----
on('A6_MF',(None,'A6_MF1',{grp:grp+1}))
on('A6_MF1',(None,'INS',{ins_ch:171,ins_st:TST,oret.r:oret.id('A6_MF2')}))
on('A6_MF2',(None,'INS',{ins_ch:187,ins_st:TST,oret.r:oret.id('A6_MF3')}))
on('A6_MF3',(None,'AFTER_ED',{co:co-1}))
