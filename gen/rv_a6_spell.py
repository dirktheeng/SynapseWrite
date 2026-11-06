# ---- rv_a6: spelling suggestions and a user dictionary ----
# Weights pull double duty: the compiled word automaton that checks words during paint also judges each candidate here.
# Candidates are one edit from the word (swap, delete, doubled letter, replace, insert). The letter wires of the automaton are read by state A6S_W as well as by paint.
SGB=1302000; WB=SGB; CD=SGB+64; FND=SGB+128; FRW=33; DICTB=1310000; DICTMAX=255
a6ws=R();a6we=R();a6n=R();a6i=R();a6up=R();a6au=R();a6src=R();a6cl=R();a6wi=R();a6ok=R();a6op=R();a6p=R();a6c=R();a6fn=R();a6kf=R();a6s_=R();a6d_=R();a6t0=R();a6t1=R();a6k=R();a6st=R();a6l=R();a6mr=R();a6mx=R();a6rl=R()
a6wr=t3ret('A6S_WR')
_wchar=lambda v,en: net.or_(net.and_(net.ge(v,65,en),net.lt(v,91,en)),net.and_(net.ge(v,97,en),net.lt(v,123,en)),net.eq(v,39,en),net.eq(v,146,en))
_apos=lambda v,en: net.or_(net.eq(v,39,en),net.eq(v,146,en))
# word around the caret
a6cm=R()   # set when a right click asked: a word with no suggestion to offer falls through to the edit menu
on('A6S_0',(ONE-sp_on,'A6S_NO',None),(None,'A6S_L',{a6ws:co,a6we:co}))
on('A6S_NO',(a6cm,'RVA3_CMM',None),(None,'A6S_KM',None))
on('A6S_KM',(None,'T1_M0',{t1_mop:12,t1_mrow:99,t1_mtop:net.min_(scr_cy+chh,DOCB-RH*8-4),t1_mx:net.min_(cx,as_x(1262-170)),clip0:0,clip1:0}))
e=S('A6S_L'); on('A6S_L',(net.eq(a6ws,0,e),'A6S_R',None),(None,'A6S_L1',{r1:cb+a6ws-1}))
e=S('A6S_L1'); on('A6S_L1',(_wchar(R1,e),'A6S_L',{a6ws:a6ws-1}),(None,'A6S_R',None))
e=S('A6S_R'); on('A6S_R',(net.ge(a6we,clen,e),'A6S_T0',None),(None,'A6S_R1',{r1:cb+a6we}))
e=S('A6S_R1'); on('A6S_R1',(_wchar(R1,e),'A6S_R',{a6we:a6we+1}),(None,'A6S_T0',None))
e=S('A6S_T0'); on('A6S_T0',(net.ge(a6ws,a6we,e),'A6S_NO',None),(None,'A6S_T1',{r1:cb+a6ws}))
e=S('A6S_T1'); on('A6S_T1',(_apos(R1,e),'A6S_T0',{a6ws:a6ws+1}),(None,'A6S_T2',{r1:cb+a6we-1}))
e=S('A6S_T2'); on('A6S_T2',(_apos(R1,e),'A6S_T0',{a6we:a6we-1}),(None,'A6S_C0',{a6n:a6we-a6ws,a6i:0,a6up:0,a6au:1}))
# lowered copy of the word
e=S('A6S_C0'); on('A6S_C0',(net.gt(a6n,30,e),'A6S_NO',None),(net.ge(a6i,a6n,e),'A6S_CK',None),(None,'A6S_C1',{r1:cb+a6ws+a6i}))
e=S('A6S_C1'); _up=net.and_(net.ge(R1,65,e),net.lt(R1,91,e)); _ap=_apos(R1,e)
on('A6S_C1',(None,'A6S_C0',{w1:(as_x(WB)+a6i,R1+_up*32+net.eq(R1,146,e)*(39-146)),a6i:a6i+1,a6up:a6up+net.and_(_up,net.eq(a6i,0,e)),a6au:net.and_(a6au,net.or_(_up,_ap))}))
on('A6S_CK',(None,'A6S_W0',{a6src:WB,a6cl:a6n,a6wr.r:a6wr.id('A6S_CK2')}))
on('A6S_CK2',(a6ok,'A6S_NO',{a6ok:0}),(None,'A6S_G0',{a6op:1,a6p:0,a6c:0,a6fn:0,a6kf:0}))
# walk a candidate through the automaton: one letter a tick
fsm.set(sp_in,S('A6S_W0'),0); fsm.set(sp_pa,S('A6S_W0'),0); fsm.set(sp_ap,S('A6S_W0'),0)
e=S('A6S_W0'); on('A6S_W0',(None,'A6S_W',{r1:a6src,a6wi:1}))
e=S('A6S_W'); on('A6S_W',(net.ge(a6wi,a6cl,e),'A6S_WE',None),(None,'A6S_W',{r1:a6src+a6wi,a6wi:a6wi+1}))
e=S('A6S_WE'); on('A6S_WE',(None,'A6S_WR',{a6ok:net.step(sp_acc+sp_pa-0.5)}))
fsm.set(sp_in,S('A6S_WE'),0); fsm.set(sp_pa,S('A6S_WE'),0); fsm.set(sp_ap,S('A6S_WE'),0)
# the next candidate. Operators: 1 swap, 2 delete, 3 doubled letter, 4 replace, 5 insert. Letters go by English frequency.
A6LET='eaiotnsrlcdmupghbyfvwkxzjq'
e=S('A6S_G0'); oph=net.decode(a6op,7,e)
s_=G_(a6p+2,oph[1])+G_(a6p+1,oph[2])+G_(a6p,oph[3])+G_(a6p+1,oph[4])+G_(a6p,oph[5])
d_=G_(a6p+2,oph[1])+G_(a6p,oph[2])+G_(a6p+1,oph[3])+G_(a6p+1,oph[4])+G_(a6p+1,oph[5])
on('A6S_G0',(None,'A6S_G1',{a6s_:s_,a6d_:d_,a6cl:G_(a6n,oph[1])+G_(a6n-1,oph[2])+G_(a6n+1,oph[3])+G_(a6n,oph[4])+G_(a6n+1,oph[5]),rb:(as_x(WB),a6p),rc:as_x(WB)+a6p-oph[3]}))
on('A6S_G1',(None,'A6S_G2',{wb:(as_x(CD),a6p),a6t0:rc.out[0],a6t1:rc.out[1],rb:(as_x(WB)+a6s_,net.relu(a6n-a6s_))}))
e=S('A6S_G2'); oq=net.decode(a6op,7,e); lh_=net.decode(a6c,26,e); lv_=X()
for i_,ch_ in enumerate(A6LET): lv_=lv_+lh_[i_]*ord(ch_)
_wbs={wb:(as_x(CD)+a6d_,net.relu(a6n-a6s_))}
on('A6S_G2',(oq[1],'A6S_G3',{**_wbs,w1:(as_x(CD)+a6p,a6t1),w2:(as_x(CD)+a6p+1,a6t0)}),(oq[2],'A6S_G3',_wbs),(oq[3],'A6S_G3',{**_wbs,w1:(as_x(CD)+a6p,a6t0)}),(None,'A6S_G3',{**_wbs,w1:(as_x(CD)+a6p,lv_)}))
on('A6S_G3',(None,'A6S_W0',{a6src:CD,a6wr.r:a6wr.id('A6S_H0')}))
# a hit is kept if no earlier row has it
on('A6S_H0',(a6ok,'A6S_H1',{a6ok:0,a6k:0}),(None,'A6S_NX',None))
_frow=lambda k_:as_x(FND)+k_*FRW
e=S('A6S_H1'); on('A6S_H1',(net.ge(a6k,a6fn,e),'A6S_HS',None),(None,'A6S_H2',{r1:_frow(a6k)}))
e=S('A6S_H2'); on('A6S_H2',(net.eq(R1,a6cl,e),'A6S_H3',{a6i:0}),(None,'A6S_H1',{a6k:a6k+1}))
e=S('A6S_H3'); on('A6S_H3',(net.ge(a6i,a6cl,e),'A6S_NX',None),(None,'A6S_H4',{r1:_frow(a6k)+1+a6i,r2:as_x(CD)+a6i}))
e=S('A6S_H4'); on('A6S_H4',(net.eq(R1,R2,e),'A6S_H3',{a6i:a6i+1}),(None,'A6S_H1',{a6k:a6k+1}))
on('A6S_HS',(None,'A6S_HT',{rb:(as_x(CD),a6cl),w1:(_frow(a6fn),a6cl)}))
on('A6S_HT',(None,'A6S_NX',{wb:(_frow(a6fn)+1,a6cl),a6fn:a6fn+1,a6kf:a6kf+1}))
# advance, with a limit per operator so that one kind cannot fill the list
e=S('A6S_NX'); on_=net.decode(a6op,7,e)
cap=on_[1]*2+on_[2]*2+on_[3]*1+on_[4]*3+on_[5]*2
_full=net.ge(a6kf,cap,e); _c25=net.ge(a6c,25,e)
on('A6S_NX',(net.ge(a6fn,6,e),'A6S_OP',None),
 (net.and_(net.step(on_[1]),net.or_(_full,net.ge(a6p+2,a6n,e))),'A6S_G0',{a6op:2,a6p:0,a6kf:0}),
 (net.step(on_[1]),'A6S_G0',{a6p:a6p+1}),
 (net.and_(net.step(on_[2]),net.or_(_full,net.ge(a6p+1,a6n,e))),'A6S_G0',{a6op:3,a6p:1,a6kf:0}),
 (net.step(on_[2]),'A6S_G0',{a6p:a6p+1}),
 (net.and_(net.step(on_[3]),net.or_(_full,net.ge(a6p,a6n,e))),'A6S_G0',{a6op:4,a6p:G_(as_x(1),e),a6c:0,a6kf:0}),
 (net.step(on_[3]),'A6S_G0',{a6p:a6p+1}),
 (net.and_(net.step(on_[4]),net.or_(_full,net.and_(_c25,net.eq(a6p,0,e)))),'A6S_G0',{a6op:5,a6p:0,a6c:0,a6kf:0}),
 (net.and_(net.step(on_[4]),_c25,net.ge(a6p+1,a6n,e)),'A6S_G0',{a6p:0,a6c:0}),
 (net.and_(net.step(on_[4]),_c25),'A6S_G0',{a6p:a6p+1,a6c:0}),
 (net.step(on_[4]),'A6S_G0',{a6c:a6c+1}),
 (net.and_(net.step(on_[5]),net.or_(_full,net.and_(_c25,net.ge(a6p,a6n,e)))),'A6S_OP',None),
 (net.and_(net.step(on_[5]),_c25),'A6S_G0',{a6p:a6p+1,a6c:0}),
 (None,'A6S_G0',{a6c:a6c+1}))
# the menu: rows are the hits, then Add to Dictionary and Ignore
A6MW=170
e=S('A6S_OP'); _fm=a6fn+net.and_(e,ONE-net.step(a6fn)); _rows=_fm+2; _y0=scr_cy+chh
_flip=net.gt(_y0+_rows*RH,780,e)
on('A6S_OP',(None,'T1_M0',{a6cm:0,a6nr:G_(_rows,e),a6mf:G_(_fm,e),t1_mop:20,t1_mrow:99,t1_mtop:G_(_y0,e-_flip)+G_(net.relu(scr_cy-_rows*RH),_flip),t1_mx:net.min_(cx,as_x(1270-A6MW)),clip0:0,clip1:0}))
on('T1_MM20',(None,'A6M_1',{a6mr:0,rB:(t1_mx+2,t1_mtop+2,A6MW+1,a6nr*RH+1,(200,198,196),0),rC:(t1_mx-1,t1_mtop-1,A6MW+2,a6nr*RH+2,(150,148,146),0)}))
e=S('A6M_1'); _hv=net.eq(a6mr,t1_mrow,e); _ry=t1_mtop+a6mr*RH; _hc=tuple(as_x(255)-_hv*34 for _ in range(3))
_isw=net.lt(a6mr,a6fn,e)
on('A6M_1',(net.ge(a6mr,a6nr,e),'T1_END',None),(_isw,'A6M_W0',{rA:(t1_mx,_ry,A6MW,RH,_hc,254),sx:t1_mx+8,a6i:0,r1:_frow(a6mr)}),
 (net.eq(a6mr,a6mf,e),'A6M_LA',{rA:(t1_mx,_ry,A6MW,RH,_hc,254),sx:t1_mx+8}),(net.eq(a6mr,a6mf+1,e),'A6M_LI',{rA:(t1_mx,_ry,A6MW,RH,_hc,254),sx:t1_mx+8}),
 (None,'A6M_LN',{rA:(t1_mx,_ry,A6MW,RH,_hc,254),sx:t1_mx+8}))
def _a6label(st,txt,nx):
    cur=st
    for i_,ch_ in enumerate(txt):
        n=f'{st}_{i_}' if i_<len(txt)-1 else nx
        e=S(cur); hv=net.eq(a6mr,t1_mrow,e); yv=t1_mtop+a6mr*RH+2
        on(cur,(hv,n,{gly:(ord(ch_),9,sx,yv,0,5),sx:sx+adv}),(None,n,{gly:(ord(ch_),9,sx,yv,0,0),sx:sx+adv}))
        cur=n
on('A6M_NR',(None,'A6M_1',{a6mr:a6mr+1}))
_a6label('A6M_LA','Add to Dictionary','A6M_NR'); _a6label('A6M_LI','Ignore','A6M_NR'); _a6label('A6M_LN','(no suggestions)','A6M_NR')
on('A6M_W0',(None,'A6M_W1',{a6rl:R1}))
e=S('A6M_W1'); on('A6M_W1',(net.ge(a6i,a6rl,e),'A6M_NR',None),(None,'A6M_W2',{r1:_frow(a6mr)+1+a6i}))
def _cased(v,en,ix):
    "Capitals follow the word: the first letter, or all of them."
    u_=net.and_(net.or_(a6au,net.and_(net.step(a6up),net.eq(ix,0,en))),net.ge(v,97,en),net.lt(v,123,en))
    return v-u_*32
e=S('A6M_W2'); _g=_cased(R1,e,a6i); _hv=net.eq(a6mr,t1_mrow,e); _yv=t1_mtop+a6mr*RH+2
on('A6M_W2',(_hv,'A6M_W1',{gly:(_g,9,sx,_yv,0,5),sx:sx+adv,a6i:a6i+1}),(None,'A6M_W1',{gly:(_g,9,sx,_yv,0,0),sx:sx+adv,a6i:a6i+1}))
# a row was chosen
e=S('A6S_PK'); on('A6S_PK',(net.lt(a6sr,a6fn,e),'A6S_RP',{grp:grp+1,co:a6ws,ap:cp,ao:a6ws,r1:_frow(a6sr),rs:cb+1024+a6ws}),(net.eq(a6sr,a6mf,e),'A6S_AD',{r1:as_x(DICTB)}),(net.eq(a6sr,a6mf+1,e),'A6S_IG0',{a6i:a6ws,grp:grp+1}),(None,'RD0',None))
fd_in('A6S_RP','A6S_TD1','A6S_IG2')
e=S('A6S_RP'); on('A6S_RP',(None,'A6S_RQ',{a6rl:R1,a6st:RSC+net.and_(trk,ONE-FD['ins'],e)*ST_INS-FD['dele']*ST_DEL,a6i:0}))
e=S('A6S_RQ'); on('A6S_RQ',(net.ge(a6i,a6n,e),'A6S_IN',{a6i:0}),(trk,'A6S_TD1',{rs:cb+1024+co}),(None,'DEL',{a6i:a6i+1,oret.r:oret.id('A6S_RQ')}))
e=S('A6S_TD1'); _mk=net.and_(e,ONE-FD['ins'],ONE-FD['dele']); log(_mk,5,cp,co,RSC,RSC+ST_DEL)
on('A6S_TD1',(FD['ins'],'DEL',{a6i:a6i+1,oret.r:oret.id('A6S_RQ')}),(FD['dele'],'A6S_RQ',{co:co+1,a6i:a6i+1}),(None,'A6S_RQ',{co:co+1,a6i:a6i+1,w1:(cb+1024+co,RSC+ST_DEL),w2:(cb+DIRTY,1)}))
e=S('A6S_IN'); on('A6S_IN',(net.ge(a6i,a6rl,e),'AFTER_ED',None),(None,'A6S_I2',{r1:_frow(a6sr)+1+a6i}))
e=S('A6S_I2'); on('A6S_I2',(None,'INS',{ins_ch:_cased(R1,e,a6i),ins_st:a6st,a6i:a6i+1,oret.r:oret.id('A6S_IN')}))
# add to the user dictionary: a table in the bank, kept in browser storage by the glue at the network's command
a6ds=R(); dsave=Bus(net); dsave.add(S('HF'),a6ds); fsm.set(a6ds,S('HF'),0)
_dent=lambda k_:as_x(DICTB)+1+k_*FRW
on('A6S_AD',(None,'A6S_A1',{a6k:R1}))
e=S('A6S_A1'); on('A6S_A1',(net.ge(a6k,DICTMAX,e),'RD0',None),(None,'A6S_A2',{rb:(as_x(WB),a6n),w1:(_dent(a6k),a6n),w2:(as_x(DICTB),a6k+1)}))
on('A6S_A2',(None,'DA0',{wb:(_dent(a6k)+1,a6n),di_:0,a6ds:1+(DICTMAX+1)*FRW}))
# ignore: the word is marked no proof, which also saves as w:noProof
e=S('A6S_IG0'); on('A6S_IG0',(net.ge(a6i,a6we,e),'AFTER_ED',None),(None,'A6S_IG2',{rs:cb+1024+a6i}))
e=S('A6S_IG2'); _nn=net.and_(e,ONE-FD['nop']); log(_nn,5,cp,a6i,RSC,RSC+ST_NOP)
on('A6S_IG2',(_nn,'A6S_IG0',{w1:(cb+1024+a6i,RSC+ST_NOP),w2:(cb+DIRTY,1),a6i:a6i+1}),(None,'A6S_IG0',{a6i:a6i+1}))
# paint: a word the automaton refused is looked up in the user table before the squiggle
e=S('A6D_0'); on('A6D_0',(None,'A6D_1',{r1:as_x(DICTB)}))
e=S('A6D_1'); on('A6D_1',(net.eq(R1,0,e),'T4_SQ',None),(None,'A6D_2',{a6dm:R1,a6dk:0,a6dl:a6oe-a6o0}))
e=S('A6D_2'); on('A6D_2',(net.ge(a6dk,a6dm,e),'T4_SQ',None),(None,'A6D_3',{rf:_dent(a6dk),r1:pbs+a6o0,r2:pbs+a6o0+1}))
e=S('A6D_3'); on('A6D_3',(net.and_(net.eq(rf.out[0],a6dl,e),net.eq(low0(R1,e),rf.out[1],e),net.or_(net.lt(a6dl,2,e),net.eq(low0(R2,e),rf.out[2],e))),'A6D_4',{a6di:2}),(None,'A6D_2',{a6dk:a6dk+1}))
e=S('A6D_4'); on('A6D_4',(net.ge(a6di,a6dl,e),'T4_SQ1',None),(None,'A6D_5',{r1:_dent(a6dk)+1+a6di,r2:pbs+a6o0+a6di}))
e=S('A6D_5'); on('A6D_5',(net.eq(R1,low0(R2,e),e),'A6D_4',{a6di:a6di+1}),(None,'A6D_2',{a6dk:a6dk+1}))
