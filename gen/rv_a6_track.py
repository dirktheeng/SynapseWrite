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
_lb=net.bits(_yy,12,e); _ly=net.and_(e,ONE-_lb[0],ONE-_lb[1]); _mhr=net.decode(_m,13,e); _cum=X(); _c=0
for m_,d_ in enumerate((31,28,31,30,31,30,31,31,30,31,30,31),1): _cum=_cum+_mhr[m_]*_c; _c+=d_
_late=sum((_mhr[m_] for m_ in range(3,13)),X())
_days=net.relu(_yy-1970)*365+_q+_cum+net.step(_late+_ly-1.5)+net.relu(_d-1)
on('A6R_D1',(None,'T4_TS',{w1:(cb+PDATE,_days),oi:oi+10}))

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

# ---- equations in a saved file: one m:r per character, m:sSup and m:sSub for script runs ----
a6nk=R();a6er=t3ret('A6E_ER')
fd_in('A6E_2','A6E_S1')
lit('A6E_CL',b'</m:oMath>','A6E_CL2'); on('A6E_CL2',(None,'SVr',{a6em:0,r1:pbs+a6off,r2:pbs+1024+a6off}))
lit('A6E_CE',b'</m:oMath>','A6E_CE2'); on('A6E_CE2',(None,'SVe',{a6em:0}))
e=S('A6E_0'); on('A6E_0',(net.eq(t2psv,99999,e),'A6E_01',None),(None,'T4_SC',{t4cr.r:t4cr.id('A6E_01')}))
on('A6E_01',(a6em,'A6E_1',{t2psv:99999}),(None,'A6E_02',{t2psv:99999,a6em:1}))
lit('A6E_02',b'<m:oMath>','A6E_1')
e=S('A6E_1'); on('A6E_1',(net.ge(a6off+1,plen_,e),'A6E_B',{a6nk:0}),(None,'A6E_2',{r1:pbs+a6off+1,r2:pbs+1024+a6off+1}))
e=S('A6E_2'); _eqn=net.and_(FD['font'],FD['nop'],net.lt(R1,1000,e))
on('A6E_2',(net.and_(_eqn,FD['sup']),'A6E_Bu',{a6nk:1}),(net.and_(_eqn,FD['sub']),'A6E_Bb',{a6nk:2}),(None,'A6E_B',{a6nk:0}))
lit('A6E_Bu',b'<m:sSup><m:e>','A6E_B'); lit('A6E_Bb',b'<m:sSub><m:e>','A6E_B')
on('A6E_B',(None,'A6E_R',{a6er.r:a6er.id('A6E_A')}))
on('A6E_A',(net.eq(a6nk,1,S('A6E_A')),'A6E_Au',{a6off:a6off+1}),(net.eq(a6nk,2,S('A6E_A')),'A6E_Ab',{a6off:a6off+1}),(None,'SVC',{a6off:a6off+1}))
lit('A6E_Au',b'</m:e><m:sup>','A6E_S0'); lit('A6E_Ab',b'</m:e><m:sub>','A6E_S0')
e=S('A6E_S0'); on('A6E_S0',(net.ge(a6off,plen_,e),'A6E_SE',None),(None,'A6E_S1',{r1:pbs+a6off,r2:pbs+1024+a6off}))
e=S('A6E_S1'); _eqn=net.and_(FD['font'],FD['nop'],net.lt(R1,1000,e)); _same=net.or_(net.and_(FD['sup'],net.eq(a6nk,1,e)),net.and_(FD['sub'],net.eq(a6nk,2,e)))
on('A6E_S1',(net.and_(_eqn,_same),'A6E_R',{ins_ch:R1,ins_st:R2,a6off:a6off+1,a6er.r:a6er.id('A6E_S0')}),(None,'A6E_SE',None))
e=S('A6E_SE'); on('A6E_SE',(net.eq(a6nk,1,e),'A6E_Eu',None),(None,'A6E_Eb',None))
lit('A6E_Eu',b'</m:sup></m:sSup>','SVC'); lit('A6E_Eb',b'</m:sub></m:sSub>','SVC')
# one character: run properties keep size and color, so a file comes back the same
e=S('A6E_R'); on('A6E_R',(net.ge(ins_ch,300,e),'A6Q_X0',{a6qk:ins_ch-300}),(None,'A6E_Ro',None))
lit('A6E_Ro',b'<m:r>','A6E_R1')
on('A6E_R1',(None,'T2RP',{t2full:net.step(psty),t2pr.r:t2pr.id('A6E_R2')}))
lit('A6E_R2',b'<m:t xml:space="preserve">','A6E_C')
e=S('A6E_C'); _amp=net.eq(ins_ch,38,e);_lt=net.eq(ins_ch,60,e);_gt=net.eq(ins_ch,62,e);_hi=net.ge(ins_ch,160,e);_pn=net.and_(net.ge(ins_ch,128,e),net.lt(ins_ch,160,e)); _ot=e-_amp-_lt-_gt-_hi-_pn
em_en.lin(_ot); em_b.add(_ot,ins_ch)
on('A6E_C',(_amp,'A6E_Ca',None),(_lt,'A6E_Cl',None),(_gt,'A6E_Cg',None),(_hi,'T2U2',{t2ur.r:t2ur.id('A6E_D')}),(_pn,'T2U3',{t2ur.r:t2ur.id('A6E_D')}),(None,'A6E_D',None))
lit('A6E_Ca',b'&amp;','A6E_D'); lit('A6E_Cl',b'&lt;','A6E_D'); lit('A6E_Cg',b'&gt;','A6E_D')
lit('A6E_D',b'</m:t></m:r>','A6E_ER')
# ---- reader: bytes of m:t become characters styled as the Equation command styles them ----
fsm.set(a6es,S('OP0'),0)
ST_EQ=128+ST_NOP
def _eqstyle(en,chv):
    fin.add(en,cs+rhi); fen.lin(en)
    lo=low0(chv,en); lett=net.and_(net.ge(lo,97,en),net.lt(lo,123,en))
    s1=net.eq(a6es,1,en); s2=net.eq(a6es,2,en)
    return cs+rhi+G_(ONE-FD['font'],en)*128+G_(ONE-FD['nop'],en)*ST_NOP+G_(ONE-FD['ital'],lett)*32+G_(ONE-FD['sup'],s1)*ST_SUP+G_(ONE-FD['sub'],s2)*ST_SUB
on('A6E_R0',(None,'A6E_R1a',{rl:OA+oi}))
e=S('A6E_R1a'); on('A6E_R1a',(net.eq(W[0],62,e),'A6E_R2a',{oi:oi+1}),(None,'A6E_R0',{oi:oi+1}))
on('A6E_R2a',(None,'A6E_R3',{rl:OA+oi}))
e=S('A6E_R3'); _am=net.eq(W[0],38,e); _b2=net.and_(net.ge(W[0],192,e),net.lt(W[0],224,e)); _b3=net.ge(W[0],224,e)
_v2=(W[0]-192)*64+(W[1]-128); _big=net.and_(_b2,net.gt(_v2,255,e))
_chv=W[0]
_ent=net.and_(_am,net.eq(W[1],108,e))*60+net.and_(_am,net.eq(W[1],103,e))*62+net.and_(_am,net.eq(W[1],97,e))*38
_sta=_eqstyle(e,G_(W[0],e))
on('A6E_R3',(net.eq(W[0],60,e),'PX',None),
 (net.and_(_am,net.eq(W[1],97,e)),'INS',{ins_ch:38,ins_st:_sta,oi:oi+5,oret.r:oret.id('A6E_R2a')}),
 (_am,'INS',{ins_ch:_ent,ins_st:_sta,oi:oi+4,oret.r:oret.id('A6E_R2a')}),
 (_big,'INS',{ins_ch:63,ins_st:_sta,oi:oi+2,oret.r:oret.id('A6E_R2a')}),
 (_b2,'INS',{ins_ch:_v2,ins_st:_sta,oi:oi+2,oret.r:oret.id('A6E_R2a')}),
 (_b3,'INS',{ins_ch:63,ins_st:_sta,oi:oi+3,oret.r:oret.id('A6E_R2a')}),
 (None,'INS',{ins_ch:W[0],ins_st:_sta,oi:oi+1,oret.r:oret.id('A6E_R2a')}))
# linear form of fractions and roots
e=S('A6E_I1'); _st=_eqstyle(e,as_x(0)); on('A6E_I1',(None,'INS',{ins_ch:a6ec,ins_st:_st,oret.r:oret.id('PX')}))
e=S('A6E_I2'); _st=_eqstyle(e,as_x(0)); on('A6E_I2',(None,'INS',{ins_ch:a6ec,ins_st:_st,oret.r:oret.id('A6E_I3')}))
e=S('A6E_I3'); on('A6E_I3',(None,'A6E_I1',{a6ec:47}))
for i_,ch_ in enumerate('sqrt('):
    st=f'A6E_Ra' if i_==0 else f'A6E_Ra{i_}'; nx=f'A6E_Ra{i_+1}' if i_<4 else 'PX'
    e=S(st); _st=_eqstyle(e,as_x(ord(ch_))); on(st,(None,'INS',{ins_ch:ord(ch_),ins_st:_st,oret.r:oret.id(nx)}))

exec(open('rv_a6_math.py').read())
