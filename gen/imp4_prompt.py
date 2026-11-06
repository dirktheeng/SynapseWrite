# ---- imp4: one prompt bar with many duties. It takes a short text and hands it to the command that asked. ----
net.group('prompt bar')
PRL=['','Color (RRGGBB):','','New style name:','Rename style to:','Font name:','Character style:']
on('V4_PR',(None,'RD0',{mode:8,prl:0,field:0}))
_b_=(160,160,160)
e=S('V4_B0'); _ph=net.decode(prk,len(PRL),e)
on('V4_B0',*[(_ph[k_],f'V4_BL{k_}',{sx:PX+8,rA:(PX+120,DOCY+3,400,1,_b_,0),rB:(PX+120,DOCY+24,400,1,_b_,0),rC:(PX+119,DOCY+3,1,22,_b_,0),rD:(PX+520,DOCY+3,1,22,_b_,0)}) for k_ in range(len(PRL)) if PRL[k_]],(None,'V4_B1',None))
for k_,t_ in enumerate(PRL):
    if t_: text_chain(f'V4_BL{k_}',[t_],'V4_B1',y=DOCY+4,f=0,b=3)
on('V4_B1',(None,'V4_B2',{fi_:0,sx:PX+124}))
e=S('V4_B2'); on('V4_B2',(net.ge(fi_,prl,e),'TB0',{rD:(sx,DOCY+6,1,16,(0,0,0),0)}),(None,'V4_B3',{r1:as_x(PRB)+fi_}))
on('V4_B3',(None,'V4_B2',{gly:(R1,0,sx,DOCY+4,0,0),sx:sx+adv,fi_:fi_+1}))
# what the text does
e=S('V4_PX'); _px=net.decode(prk,len(PRL),e)
on('V4_PX',(_px[1],'V4_HX',{v4h:0,v4i:0,v4j:0}),(_px[3],'V5_NS0',{v4c:0}),(_px[6],'V5_NS0',{v4c:1}),(_px[4],'V5_RN0',None),(_px[5],'V4_FT0',{v4i:0}),(None,'RD0',None))
# a color typed as six hex digits, with or without a leading #
on('V4_HX',(None,'V4_HX1',{r1:as_x(PRB)+v4i}))
e=S('V4_HX1'); _dg=net.and_(net.ge(R1,48,e),net.lt(R1,58,e)); _up=net.and_(net.ge(R1,65,e),net.lt(R1,71,e)); _lo=net.and_(net.ge(R1,97,e),net.lt(R1,103,e)); _isx=net.step(_dg+_up+_lo)
on('V4_HX1',(net.and_(net.ge(v4i,prl,e),net.eq(v4j,6,e)),'V4_HY',{r1:as_x(_ctab)+0}),(net.ge(v4i,prl,e),'RD0',{mode:8}),(net.and_(net.eq(v4i,0,e),net.eq(R1,35,e)),'V4_HX',{v4i:1}),
 (net.and_(_isx,net.lt(v4j,6,e)),'V4_HX',{v4i:v4i+1,v4j:v4j+1,v4h:v4h*16+hexd(R1,e)}),(None,'RD0',{mode:8}))
e=S('V4_HY'); _hb=net.bits(v4h,24,e); fsm.set(v4i,e,(_hb[21]+_hb[22]*2+_hb[23]*4)*64+(_hb[13]+_hb[14]*2+_hb[15]*4)*8+(_hb[5]+_hb[6]*2+_hb[7]*4))
on('V4_HY',(None,'V4_HZ',None)); on('V4_HZ',(None,'V4_HW',{r1:as_x(_ctab)+v4i}))
on('V4_HW',(None,'FMTS',{fm:7,fcol:R1,fck:v4h+1,t1_uid:1}))
# a font name: a name in the table comes back as its id; a new one is added. Names the family tables already know need no id.
e=S('V4_FS'); on('V4_FS',(net.ge(v4i,v4fc,e),'V4_FA',{v4j:0}),(None,'V4_FS1',{r1:as_x(FNT)+v4i*32+v4j,r2:OA+oi+v4j}))
e=S('V4_FS1'); _q=net.eq(R2,34,e)
on('V4_FS1',(net.and_(_q,net.eq(R1,0,e)),'V4_FE',{t2nx:net.relu(v4i-FNSD)}),(net.and_(ONE-_q,net.eq(R1,R2,e),net.lt(v4j,31,e)),'V4_FS',{v4j:v4j+1}),(None,'V4_FS',{v4i:v4i+1,v4j:0}))
e=S('V4_FA'); on('V4_FA',(net.ge(v4fc,FNMAXN,e),'V4_FE',{t2nx:0}),(None,'V4_FA1',{r2:OA+oi+v4j}))
e=S('V4_FA1'); on('V4_FA1',(net.or_(net.eq(R2,34,e),net.ge(v4j,31,e),net.eq(R2,0,e)),'V4_FE',{w1:(as_x(FNT)+v4fc*32+v4j,0),t2nx:v4fc-FNSD,v4fc:v4fc+1}),(None,'V4_FA',{w1:(as_x(FNT)+v4fc*32+v4j,R2),v4j:v4j+1}))
on('V4_FE',(v4ty,'FMTS',{fm:10,fcol:t2v,fnx:t2nx,t2nx:0,obase:OUTB,v4ty:0,oi:0,t1_uid:1}),(None,'T2_C',{oi:oi+8}))
# a typed font name goes through the reader's own name rules, from a buffer closed by a quote
e=S('V4_FT0'); on('V4_FT0',(net.ge(v4i,prl,e),'V4_FT2',{wln:(as_x(FTB)+prl,34,34,34,34,34,34)}),(None,'V4_FT1',{r1:as_x(PRB)+v4i}))
on('V4_FT1',(None,'V4_FT0',{w1:(as_x(FTB)+v4i,R1),v4i:v4i+1}))
on('V4_FT2',(net.lt(prl,1,S('V4_FT2')),'RD0',None),(None,'V4_FT3',{obase:FTB,oi:0,v4ty:1,rl:as_x(FTB)}))
on('V4_FT3',(None,'RF9',None))
# saving: character style, font name, exact color
on('V4_RY0',(net.step(ins_y),'V4_RY1',None),(None,'T2RP1',None))
lit('V4_RY1',b'<w:rStyle w:val="','V4_RY2'); on('V4_RY2',(None,'T2SS',{t2w:as_x(STY)+(ins_y-1)*STYN+8,t2sr.r:t2sr.id('V4_RY3')})); lit('V4_RY3',b'"/>','T2RP1')
lit('V4_RN0',b'<w:rFonts w:ascii="','V4_RN1'); on('V4_RN1',(None,'T2SS',{t2w:as_x(FNT)+(ins_n+FNSD)*32,t2sr.r:t2sr.id('V4_RN2')}))
lit('V4_RN2',b'" w:hAnsi="','V4_RN3'); on('V4_RN3',(None,'T2SS',{t2w:as_x(FNT)+(ins_n+FNSD)*32,t2sr.r:t2sr.id('V4_RN4')})); lit('V4_RN4',b'"/>','T2R2')
lit('V4_RK0',b'<w:color w:val="','V4_RK1')
v4nb=[R() for _ in range(6)]; e=S('V4_RK1'); _kb=net.bits(ins_k-1,24,e)
on('V4_RK1',(None,'V4_RKh0',{v4nb[j_]:_kb[20-4*j_]+_kb[21-4*j_]*2+_kb[22-4*j_]*4+_kb[23-4*j_]*8 for j_ in range(6)}))
for j_ in range(6):
    e=S(f'V4_RKh{j_}'); em_en.lin(e); em_b.add(e,48+v4nb[j_]+net.ge(v4nb[j_],10,e)*7); on(f'V4_RKh{j_}',(None,f'V4_RKh{j_+1}' if j_<5 else 'V4_RKz',None))
lit('V4_RKz',b'"/>','V4_R60')
# PDF: an exact color as three decimals
e=S('V4_PK0'); _qb=net.bits(v4qk-1,24,e); v4pc=[R() for _ in range(3)]
on('V4_PK0',(None,'V4_PK1_0',{v4pc[k_]:sum((_qb[16-8*k_+b_]*(1<<b_) for b_ in range(8)),X()) for k_ in range(3)}))
for k_ in range(3):
    lit(f'V4_PK1_{k_}',b'0.',f'V4_PK2_{k_}')
    e=S(f'V4_PK2_{k_}'); _v=v4pc[k_]*(99/255); _t=sum((net.ge(_v,q_*10,e) for q_ in range(1,10)),X()); em_en.lin(e); em_b.add(e,48+_t)
    on(f'V4_PK2_{k_}',(None,f'V4_PK3_{k_}',None))
    e=S(f'V4_PK3_{k_}'); _v=v4pc[k_]*(99/255); _t=sum((net.ge(_v,q_*10,e) for q_ in range(1,10)),X()); _o=sum((net.ge(_v-_t*10,q_,e) for q_ in range(1,10)),X()); em_en.lin(e); em_b.add(e,48+_o)
    lit(f'V4_PK4_{k_}',b' ' if k_<2 else b' rg\n',f'V4_PK1_{k_+1}' if k_<2 else 'T4P_O')
    on(f'V4_PK3_{k_}',(None,f'V4_PK4_{k_}',None))
# the font box shows a kept font name
on('V4_TN0',(None,'V4_TN1',{v4j:0}))
on('V4_TN1',(None,'V4_TN2',{r1:as_x(FNT)+(ity.n+FNSD)*32+v4j}))
e=S('V4_TN2'); on('V4_TN2',(net.or_(net.eq(R1,0,e),net.ge(sx,206,e)),'T1_POST',None),(None,'V4_TN1',{gly:(R1,9,sx,68,0,0),sx:sx+adv,v4j:v4j+1}))
FN_ROM=[[FNT+(i_+1)*32+j_,ord(c_)] for i_,n_ in enumerate(FNSEED) for j_,c_ in enumerate(n_)]
for k_ in (3,4,6): on(f'V4_PS{k_}',(None,'V4_PR',{prk:k_}))
# ---- characters past Latin-1 ----
net.group('extended characters')
# leaving as UTF-8: a code unit, and a surrogate pair joined into four bytes
v7h=R();v7l=R()
e=S('V7_U0'); _u=ins_ch-UO; _hi=net.and_(net.ge(_u,0xD800,e),net.lt(_u,0xDC00,e)); _lo=net.and_(net.ge(_u,0xDC00,e),net.lt(_u,0xE000,e),net.step(v7h))
_lone=net.and_(net.ge(_u,0xDC00,e),net.lt(_u,0xE000,e),ONE-net.step(v7h))   # half a pair alone cannot be written as UTF-8
on('V7_U0',(_hi,'SVC',{v7h:_u-0xD800+1}),(_lo,'V7_U4',{t2cp:(v7h-1)*1024+_u-0xDC00+65536,v7h:0}),(_lone,'V7_U3',{t2cp:0xFFFD}),(None,'V7_U3',{t2cp:_u,v7h:0}))
def _emit(st,val,nx):
    e_=S(st); em_en.lin(e_); em_b.add(e_,val(e_)); on(st,(None,nx,None))
def _cb_(k_): 
    return lambda e_: (lambda b_: 128+sum((b_[k_*6+j_]*(1<<j_) for j_ in range(6)),X()))(net.bits(t2cp,21,e_))
e=S('V7_U3'); on('V7_U3',(net.lt(t2cp,0x800,e),'V7_B2',None),(None,'V7_B3',None))
_emit('V7_B2',lambda e_:(lambda b_:192+sum((b_[6+j_]*(1<<j_) for j_ in range(5)),X()))(net.bits(t2cp,21,e_)),'V7_B0')
_emit('V7_B3',lambda e_:(lambda b_:224+sum((b_[12+j_]*(1<<j_) for j_ in range(4)),X()))(net.bits(t2cp,21,e_)),'V7_B1')
_emit('V7_U4',lambda e_:(lambda b_:240+sum((b_[18+j_]*(1<<j_) for j_ in range(3)),X()))(net.bits(t2cp,21,e_)),'V7_B5')
_emit('V7_B5',_cb_(2),'V7_B1'); _emit('V7_B1',_cb_(1),'V7_B0'); _emit('V7_B0',_cb_(0),'SVC')
# arriving as four UTF-8 bytes: two cells, as in the browser's own strings
e=S('V7_R4'); _rb=net.bits(t2cp,20,e)
on('V7_R4',(None,'INS',{ins_ch:as_x(UO)+0xD800+sum((_rb[10+j_]*(1<<j_) for j_ in range(10)),X()),ins_st:csi+rhi,v7l:sum((_rb[j_]*(1<<j_) for j_ in range(10)),X()),oret.r:oret.id('V7_R5')}))
on('V7_R5',(None,'INS',{ins_ch:as_x(UO)+0xDC00+v7l,ins_st:csi+rhi,oret.r:oret.id('TX2')}))
lit('V9_SH',b'</w:t><w:softHyphen/><w:t xml:space="preserve">','SVC')
