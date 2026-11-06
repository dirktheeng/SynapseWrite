# ---- p3: .docx reader and writer for emboss, imprint, outline, shadow, character scale, language and paragraph outline level ----
# Rules that find the tags are P3_PX in p3_regs.py. Kept through open and save; not drawn differently on screen or in PDF.
_p3g=net.cur[0]; net.group('p3 docx properties')
# on or off, as F1_TV: a bare tag is on; a value starting 0, f or n is off. The flag is bit 20+p3bit of the link field.
on('P3_TV',(None,'P3_TV1',{rl:OA+oi}))
e=S('P3_TV1'); on('P3_TV1',(net.eq(W[0],47,e),'P3_XB',{t2v:1}),(None,'P3_TV2',{rl:OA+oi+8}))
e=S('P3_TV2'); on('P3_TV2',(net.or_(net.eq(W[0],48,e),net.eq(W[0],102,e),net.eq(W[0],110,e)),'P3_XB',{t2v:0}),(None,'P3_XB',{t2v:1}))
e=S('P3_XB'); _hb=net.bits(ics.e[1],24,e); _bh=net.decode(p3bit,4,e); _hn=as_x(ics.e[1])
for j_ in range(4):
    _hn=_hn+net.and_(_bh[j_],t2v,ONE-_hb[20+j_])*(1<<(20+j_))-net.and_(_bh[j_],ONE-t2v,_hb[20+j_])*(1<<(20+j_))
on('P3_XB',(None,'PX',{ics:_f1ics(h_=_hn)}))
# w:outline in a run, or w:outlineLvl in a paragraph of the document part
e=S('P3_OU'); on('P3_OU',(net.eq(W[0],76,e),'P3_OL',{rl:OA+oi+11}),(None,'P3_TV',{p3bit:0}))
e=S('P3_OL'); _d=W[0]-48; _dg=net.and_(net.ge(W[0],48,e),net.lt(W[0],58,e),net.eq(ztarget,4,e))
on('P3_OL',(_dg,'PX',{p3ol:_d+1,w1:(cb+F1PX,f1pc+f1pw*2+(_d+1)*(1/32)),oi:oi+12}),(None,'PX',{oi:oi+3}))
fsm.set(p3ol,S('T2_PR'),0)
# character scale: w:val in percent, kept up to 1023 in bits 14-23 of the extended field
on('P3_SC',(None,'P3_SC1',{rl:OA+oi}))
e=S('P3_SC1'); _dg=net.and_(net.ge(W[0],48,e),net.lt(W[0],58,e))
on('P3_SC1',(_dg,'P3_SC',{p3n:net.min_(p3n*10+W[0]-48,99999),oi:oi+1}),(None,'P3_SCW',None))
e=S('P3_SCW'); _xb=net.bits(ics.e[0],24,e); _old=sum((_xb[k_]*(1<<k_) for k_ in range(14,24)),X())
on('P3_SCW',(None,'PX',{ics:_f1ics(x_=as_x(ics.e[0])-_old+net.min_(p3n,1023)*(1<<14))}))
# language: the attribute text is copied to the scratch entry, then looked for among the known ones; a new one takes the next id, up to 15
_lb=lambda i_: as_x(P3LT)+i_*P3LS
on('P3_LG',(None,'P3_LC0',{p3s:net.min_(p3nl+1,P3NL+1),p3k:0}))
on('P3_LC0',(None,'P3_LC1',{rl:OA+oi}))
e=S('P3_LC1'); on('P3_LC1',(net.or_(net.eq(W[0],47,e),net.eq(W[0],62,e),net.ge(p3k,P3LS-2,e)),'P3_LM0',{w1:(_lb(p3s)+p3k,0),p3m:p3k,p3j:1}),(None,'P3_LC0',{w1:(_lb(p3s)+p3k,W[0]),p3k:p3k+1,oi:oi+1}))
e=S('P3_LM0'); on('P3_LM0',(net.gt(p3j,p3nl,e),'P3_LN',None),(None,'P3_LM1',{p3k:0}))
on('P3_LM1',(None,'P3_LM2',{r1:_lb(p3j)+p3k,r2:_lb(p3s)+p3k}))
e=S('P3_LM2'); on('P3_LM2',(ONE-net.eq(R1,R2,e),'P3_LM0',{p3j:p3j+1}),(net.ge(p3k,p3m,e),'P3_LS',{p3n:p3j}),(None,'P3_LM1',{p3k:p3k+1}))
e=S('P3_LN'); on('P3_LN',(net.lt(p3nl,P3NL,e),'P3_LS',{p3n:p3nl+1,p3nl:p3nl+1}),(None,'P3_LS',{p3n:0}))
e=S('P3_LS'); _hb2=net.bits(ics.e[1],24,e); _ol=sum((_hb2[k_]*(1<<k_) for k_ in range(8,12)),X())
on('P3_LS',(None,'PX',{ics:_f1ics(h_=as_x(ics.e[1])-_ol+p3n*256)}))
fsm.set(p3nl,S('OP0'),0)
net.group('p3 docx writer')
# ---- writer ----
for _s in ('T2Ya','V5_WC6'): fsm.set(ins_h,S(_s),0)
e=S('T2RP'); _wb=net.bits(ins_h,24,e); _xw=net.bits(ins_x,24,e)
for j_ in range(4): fsm.set(p3wf[j_],e,_wb[20+j_])
fsm.set(p3wl,e,sum((_wb[k_]*(1<<(k_-8)) for k_ in range(8,12)),X())); fsm.set(p3ws,e,sum((_xw[k_]*(1<<(k_-14)) for k_ in range(14,24)),X()))
# after double strike: outline, shadow, emboss, imprint, in schema order
for j_,t_ in enumerate((b'<w:outline/>',b'<w:shadow/>',b'<w:emboss/>',b'<w:imprint/>')):
    nx_=f'P3_R{j_+1}' if j_<3 else 'T2R4n'
    on(f'P3_R{j_}',(p3wf[j_],f'P3_Rt{j_}',None),(None,nx_,None)); lit(f'P3_Rt{j_}',t_,nx_)
# after spacing: the scale
on('P3_SW0',(net.step(p3ws),'P3_SW1',None),(None,'F1_R7z',None)); lit('P3_SW1',b'<w:w w:val="','P3_SW2'); vnum('P3_SW2',p3ws,'P3_SW3'); lit('P3_SW3',b'"/>','F1_R7z')
# after vertical alignment: the language, its attribute text as read
on('P3_LW0',(net.step(p3wl),'P3_LW1',None),(None,'T2RC',None)); lit('P3_LW1',b'<w:lang ','P3_LW2')
on('P3_LW2',(None,'T2SS',{t2w:_lb(p3wl),t2sr.r:t2sr.id('P3_LW3')})); lit('P3_LW3',b'/>','T2RC')
# paragraph outline level, after the alignment
e=S('SVm'); fsm.set(p3wol,e,A4O[7]*32-floorv(A4O[7],e,3)*32); fsm.set(p3wol,S('T2Ya'),0)
e=S('P3_OL0'); on('P3_OL0',(net.step(p3wol),'P3_OL1',None),(None,'T2PP',None)); lit('P3_OL1',b'<w:outlineLvl w:val="','P3_OL2')
e=S('P3_OL2'); em_en.lin(e); em_b.add(e,47+p3wol); on('P3_OL2',(None,'P3_OL3',None)); lit('P3_OL3',b'"/>','T2PP')
net.group(_p3g)
