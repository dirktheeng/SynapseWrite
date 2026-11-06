# ---- feat1: .docx reader and writer for caps, small caps, double strike, hidden text, character spacing, run shading, links, bookmarks,
# contextual spacing and widow control. Rules that find the tags are F1_PX in feat1_regs.py. ----
_f1g=net.cur[0]; net.group('feat1 docx reader')
def _f1ics(x_=None,h_=None,z_=None):
    "The run style being read with some of feat1's fields replaced."
    return (cs,ics.k,ics.n,ics.y,ics.e[0] if x_ is None else x_,ics.e[1] if h_ is None else h_,ics.e[2] if z_ is None else z_)
# on or off, as T2_TV: a bare tag is on; a value starting 0, f or n is off
on('F1_TV',(None,'F1_TV1',{rl:OA+oi}))
e=S('F1_TV1'); on('F1_TV1',(net.eq(W[0],47,e),'F1_XB',{t2v:1}),(None,'F1_TV2',{rl:OA+oi+8}))
e=S('F1_TV2'); on('F1_TV2',(net.or_(net.eq(W[0],48,e),net.eq(W[0],102,e),net.eq(W[0],110,e)),'F1_XB',{t2v:0}),(None,'F1_XB',{t2v:1}))
e=S('F1_XB'); _xb=net.bits(ics.e[0],18,e); _bh=net.decode(f1bit,9,e); _xn=as_x(ics.e[0])
for j_ in range(4):
    _xn=_xn+net.and_(_bh[1<<j_],t2v,ONE-_xb[j_])*(1<<j_)-net.and_(_bh[1<<j_],ONE-t2v,_xb[j_])*(1<<j_)
on('F1_XB',(None,'PX',{ics:_f1ics(x_=_xn)}))
# character spacing: w:val in twips, signed, kept within 511
on('F1_SP',(None,'F1_SP1',{rl:OA+oi}))
e=S('F1_SP1'); on('F1_SP1',(net.eq(W[0],62,e),'PX',None),(pat('w:val="',e),'F1_N0',{oi:oi+7,f1n:0,f1neg:0}),(None,'F1_SP',{oi:oi+1}))
on('F1_N0',(None,'F1_N1',{rl:OA+oi}))
e=S('F1_N1'); _dg=net.and_(net.ge(W[0],48,e),net.lt(W[0],58,e))
on('F1_N1',(_dg,'F1_N0',{f1n:net.min_(f1n*10+W[0]-48,99999),oi:oi+1}),(net.eq(W[0],45,e),'F1_N0',{f1neg:1,oi:oi+1}),(None,'F1_SPW',None))
e=S('F1_SPW'); _v=net.min_(f1n,511); _sb=net.bits(ics.e[0],18,e); _old=sum((_sb[k_]*(1<<k_) for k_ in range(4,14)),X())
on('F1_SPW',(None,'PX',{ics:_f1ics(x_=as_x(ics.e[0])-_old+(G_(_v,ONE-f1neg)-G_(_v,f1neg)+e*512)*X_SP)}))
# run shading: the fill, exact, plus one; auto is none
on('F1_SH',(None,'F1_SH1',{rl:OA+oi}))
e=S('F1_SH1'); on('F1_SH1',(net.eq(W[0],62,e),'PX',None),(pat('w:fill="',e),'F1_SH2',{oi:oi+8,rl:OA+oi+8}),(None,'F1_SH',{oi:oi+1}))
e=S('F1_SH2'); _au=pat('auto',e)
def _f1hx(c_): return as_x(c_)-48-net.ge(c_,65,e)*7-net.ge(c_,97,e)*32
_rgb=sum((_f1hx(W[i_])*(1<<(20-4*i_)) for i_ in range(6)),X())+1
on('F1_SH2',(_au,'PX',{ics:_f1ics(z_=X())}),(None,'PX',{ics:_f1ics(z_=_rgb),oi:oi+6}))
# a link: r:id is looked up in the relationships part, w:anchor is kept as the name it points at
on('F1_HL',(None,'F1_HL1',{rl:OA+oi}))
e=S('F1_HL1'); on('F1_HL1',(net.eq(W[0],62,e),'PX',None),(pat('r:id="',e),'F1_RI0',{oi:oi+6,rid_n:0}),(pat('w:anchor',e),'F1_AN0',{oi:oi+10,f1i:0}),(None,'F1_HL',{oi:oi+1}))
on('F1_RI0',(None,'F1_RI1',{r1:OA+oi}))
e=S('F1_RI1'); on('F1_RI1',(net.ge(rid_n,900,e),'F1_HL',None),(net.eq(R1,34,e),'T3_BR1',{rq:0,ridret.r:ridret.id('F1_RT0')}),(None,'F1_RI0',{w1:(as_x(RIDB)+rid_n,R1),rid_n:rid_n+1,oi:oi+1}))
_lb=as_x(F1LT)+f1ll*F1LS
on('F1_RT0',(None,'F1_RT1',{f1i:0}))
e=S('F1_RT1'); on('F1_RT1',(net.or_(net.ge(f1i,tl,e),net.ge(f1i,F1LS-3,e)),'F1_HL',{w1:(_lb+1+f1i,0),w2:(_lb,1)}),(None,'F1_RT2',{r1:as_x(RELB)+tgt+f1i}))
on('F1_RT2',(None,'F1_RT1',{w1:(_lb+1+f1i,R1),f1i:f1i+1}))
on('F1_AN0',(None,'F1_AN1',{r1:OA+oi}))
e=S('F1_AN1'); on('F1_AN1',(net.or_(net.eq(R1,34,e),net.ge(f1i,F1LS-3,e)),'F1_HL',{w1:(_lb+1+f1i,0),w2:(_lb,2)}),(None,'F1_AN0',{w1:(_lb+1+f1i,R1),f1i:f1i+1,oi:oi+1}))
# bookmarks: a start opens a new id that the following runs carry, with its name; an end closes it
e=S('F1_BK'); _nb=net.min_(f1nb+1,F1N)
on('F1_BK',(pat('Start',e),'F1_BS',{oi:oi+16,f1lbk:_nb,f1nb:_nb,f1i:0}),(pat('End',e),'PX',{f1lbk:0,oi:oi+14}),(None,'PX',{oi:oi+1}))
_bb=as_x(F1BT)+f1lbk*F1BS
on('F1_BS',(None,'F1_BS1',{rl:OA+oi}))
e=S('F1_BS1'); on('F1_BS1',(net.eq(W[0],62,e),'PX',{w1:(_bb,0)}),(pat('w:name="',e),'F1_BN0',{oi:oi+8}),(None,'F1_BS',{oi:oi+1}))
on('F1_BN0',(None,'F1_BN1',{r1:OA+oi}))
e=S('F1_BN1'); on('F1_BN1',(net.or_(net.eq(R1,34,e),net.ge(f1i,F1BS-2,e)),'PX',{w1:(_bb+f1i,0)}),(None,'F1_BN0',{w1:(_bb+f1i,R1),f1i:f1i+1,oi:oi+1}))
# widow control: on unless the value is 0, false or off
on('F1_WC',(None,'F1_WC1',{rl:OA+oi}))
e=S('F1_WC1'); on('F1_WC1',(net.eq(W[0],47,e),'PX',{f1pw:0,w1:(cb+F1PX,f1pc)}),(None,'F1_WC2',{rl:OA+oi+8}))
e=S('F1_WC2'); _off=net.or_(net.eq(W[0],48,e),net.eq(W[0],102,e),net.and_(net.eq(W[0],111,e),net.eq(W[1],102,e)))
on('F1_WC2',(_off,'PX',{f1pw:1,w1:(cb+F1PX,f1pc+2)}),(None,'PX',{f1pw:0,w1:(cb+F1PX,f1pc)}))
for _s in ('T2_PR',): fsm.set(f1pc,S(_s),0); fsm.set(f1pw,S(_s),0)
for _q in (f1ll,f1lbk,f1nl,f1nb): fsm.set(_q,S('OP0'),0)
net.group('feat1 docx writer')
# ---- writer ----
fsm.set(ins_x,S('SVr'),RSX); fsm.set(ins_h,S('SVr'),RSH); fsm.set(ins_z,S('SVr'),RSZ)
for _s in ('T2Ya','V5_WC6'): fsm.set(ins_x,S(_s),0); fsm.set(ins_z,S(_s),0)
e=S('T2RP'); _wx=x_decode(ins_x,e)
for r_,v_ in zip(f1wx,(_wx['caps'],_wx['smc'],_wx['dst'],_wx['hid'],_wx['sp'])): fsm.set(r_,e,v_)
on('F1_R0',(f1wx[0],'F1_Rc',None),(None,'F1_R1',None)); lit('F1_Rc',b'<w:caps/>','F1_R1')
on('F1_R1',(f1wx[1],'F1_Rm',None),(None,'F1_R4',None)); lit('F1_Rm',b'<w:smallCaps/>','F1_R4')
on('F1_R5',(f1wx[2],'F1_Rd',None),(None,'T2R4n',None)); lit('F1_Rd',b'<w:dstrike/>','T2R4n')
on('F1_R6',(f1wx[3],'F1_Rv',None),(None,'T2R5',None)); lit('F1_Rv',b'<w:vanish/>','T2R5')
on('F1_R7',(net.step(f1wx[4]),'F1_Rs',None),(None,'F1_R7z',None)); lit('F1_Rs',b'<w:spacing w:val="','F1_Rs1'); e=S('F1_Rs1'); on('F1_Rs1',(net.lt(f1wx[4],512,e),'F1_Rsm',None),(None,'F1_Rsp',None)); lit('F1_Rsm',b'-','F1_Rsn'); vnum('F1_Rsn',as_x(512)-f1wx[4],'F1_Rs2'); vnum('F1_Rsp',f1wx[4]-512,'F1_Rs2'); lit('F1_Rs2',b'"/>','F1_R7z')
on('F1_R8',(net.step(ins_z),'F1_Rh',None),(None,'F1_RB',None)); lit('F1_Rh',b'<w:shd w:val="clear" w:color="auto" w:fill="','F1_Rh0')
f1nbz=[R() for _ in range(6)]; e=S('F1_Rh0'); _zb=net.bits(ins_z-1,24,e)
on('F1_Rh0',(None,'F1_Rhx0',{f1nbz[j_]:_zb[20-4*j_]+_zb[21-4*j_]*2+_zb[22-4*j_]*4+_zb[23-4*j_]*8 for j_ in range(6)}))
for j_ in range(6):
    e=S(f'F1_Rhx{j_}'); em_en.lin(e); em_b.add(e,48+f1nbz[j_]+net.ge(f1nbz[j_],10,e)*7); on(f'F1_Rhx{j_}',(None,f'F1_Rhx{j_+1}' if j_<5 else 'F1_Rhz',None))
lit('F1_Rhz',b'"/>','F1_RB')
# links and bookmarks around runs: before a run opens, close what it is not in and open what it is in
e=S('F1_WO'); _hb=net.bits(ins_h,20,e); _lk=sum((_hb[k_]*(1<<k_) for k_ in range(12)),X()); _bk=sum((_hb[k_]*(1<<(k_-12)) for k_ in range(12,20)),X())
on('F1_WO',(net.and_(net.step(f1wl),ONE-net.eq(f1wl,_lk,e)),'F1_WOa',{f1k:_lk,f1q:_bk}),(None,'F1_WO2',{f1k:_lk,f1q:_bk}))
lit('F1_WOa',b'</w:hyperlink>','F1_WO2'); fsm.set(f1wl,S('F1_WOa'),0)
e=S('F1_WO2'); on('F1_WO2',(net.and_(net.step(f1wb),ONE-net.eq(f1wb,f1q,e)),'F1_BE0',{f1i:1}),(None,'F1_WO3',None))
lit('F1_BE0',b'<w:bookmarkEnd w:id="','F1_BE1'); vnum('F1_BE1',f1wb,'F1_BE2'); lit('F1_BE2',b'"/>','F1_BE3')
e=S('F1_BE3'); on('F1_BE3',(net.eq(f1i,2,e),'F1_WZ1',{f1wb:0}),(None,'F1_WO3',{f1wb:0}))
e=S('F1_WO3'); on('F1_WO3',(net.and_(net.step(f1q),ONE-net.eq(f1wb,f1q,e)),'F1_BS0',{f1wb:f1q}),(None,'F1_WO4',None))
lit('F1_BS0',b'<w:bookmarkStart w:id="','F1_BS0a'); vnum('F1_BS0a',f1wb,'F1_BS0b'); lit('F1_BS0b',b'" w:name="','F1_BS0c')
on('F1_BS0c',(None,'T2SS',{t2w:as_x(F1BT)+f1wb*F1BS,t2sr.r:t2sr.id('F1_BS0d')})); lit('F1_BS0d',b'"/>','F1_WO4')
e=S('F1_WO4'); on('F1_WO4',(net.and_(net.step(f1k),ONE-net.eq(f1wl,f1k,e)),'F1_HO0',{f1wl:f1k,r1:as_x(F1LT)+f1k*F1LS}),(None,'T4_SO',None))
e=S('F1_HO0'); on('F1_HO0',(net.eq(R1,1,e),'F1_HO1',None),(net.eq(R1,2,e),'F1_HO4',None),(None,'F1_HO7',None))
lit('F1_HO1',b'<w:hyperlink r:id="rIdL','F1_HO2'); vnum('F1_HO2',f1wl,'F1_HO3'); lit('F1_HO3',b'">','T4_SO')
lit('F1_HO4',b'<w:hyperlink w:anchor="','F1_HO5'); on('F1_HO5',(None,'T2SS',{t2w:as_x(F1LT)+f1wl*F1LS+1,t2sr.r:t2sr.id('F1_HO3')}))
lit('F1_HO7',b'<w:hyperlink>','T4_SO')
# a link never runs past its paragraph; a bookmark may, and the last one closes before the section properties
on('F1_WE',(net.step(f1wl),'F1_WEa',None),(None,'T3_CE0',None)); lit('F1_WEa',b'</w:hyperlink>','T3_CE0'); fsm.set(f1wl,S('F1_WEa'),0)
on('F1_WZ',(net.step(f1wb),'F1_BE0',{f1i:2}),(None,'F1_WZ1',None)); on('F1_WZ1',(None,'T3_SVE',None))
for _q in (f1wl,f1wb): fsm.set(_q,S('SAVE'),0)
# relationships for external links, after the pictures'
on('F1_RL0',(None,'F1_RL1',{f1i:1}))
e=S('F1_RL1'); on('F1_RL1',(net.gt(f1i,f1nl,e),'T3_RL9',None),(None,'F1_RL2',{r1:as_x(F1LT)+f1i*F1LS}))
e=S('F1_RL2'); on('F1_RL2',(net.eq(R1,1,e),'F1_RL3',None),(None,'F1_RL1',{f1i:f1i+1}))
lit('F1_RL3',b'<Relationship Id="rIdL','F1_RL4'); vnum('F1_RL4',f1i,'F1_RL5'); lit('F1_RL5',b'" Type="'+RTYPE+b'hyperlink" Target="','F1_RL6')
on('F1_RL6',(None,'T2SS',{t2w:as_x(F1LT)+f1i*F1LS+1,t2sr.r:t2sr.id('F1_RL7')})); lit('F1_RL7',b'" TargetMode="External"/>','F1_RL8'); on('F1_RL8',(None,'F1_RL1',{f1i:f1i+1}))
# paragraph extras: contextual spacing beside the list rule, widow control off after the page break flag
e=S('SVm'); fsm.set(f1sc,e,net.bits(A4O[7],2,e)[0]); fsm.set(f1sw,e,net.ge(A4O[7],2,e)); fsm.set(f1sc,S('T2Ya'),0)
on('F1_WW',(f1sw,'F1_WW1',None),(None,'T2W4',None)); lit('F1_WW1',b'<w:widowControl w:val="0"/>','T2W4')
e=S('A4_Q0'); fsm.set(f1qnwc,e,net.ge(A4O[7],2,e))
net.group(_f1g)
