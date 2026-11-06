# ---- .docx writer: zip container, CRC32 and XML are all produced here ----
# Parts: static members, a dynamic styles.xml written from the style table, a dynamic document.xml.
t2nr=Ret('T2NR');t2pr=Ret('T2PR');t2rr=Ret('T2RR');t2pp=Ret('T2PP');t2sr=Ret('T2SR')
zo=R();zdr=Ret('T2ZD');usize=R();t2ur=Ret('T2UR')
t2n=R();t2run=R();t2pk=R();t2full=R();t2w=R();t2j=R();t2pa=R();t2st=R();t2psv=R()
qsty_=R()
# number printing without leading zeros
cur_='T2_NV'
for pw_ in (100000,10000,1000,100,10,1):
    nx_='T2NR' if pw_==1 else f'T2_NV{pw_}'
    e=S(cur_); base=net.gate(t2n,e); val=base
    for big in (100000,10000,1000,100,10):
        if big>pw_:
            dd=X()
            for t in range(1,10): dd=dd+net.step(val-big*t+0.5)
            val=val-dd*big
    dg=X()
    for t in range(1,10): dg=dg+net.step(val-pw_*t+0.5)
    show=e if pw_==1 else net.and_(e,net.step(base-pw_+0.5))
    em_en.lin(show); em_b.add(show,48+dg)
    on(cur_,(None,nx_,None)); cur_=nx_
def vnum(st,val,nx): on(st,(None,'T2_NV',{t2n:val,t2nr.r:t2nr.id(nx)}))
# run properties: ins_st holds the cell. t2full also writes the "off" forms so a paragraph style cannot leak in.
sv_in=Bus(net); sv_en=Bus(net); SV=style_decode(sv_in.w,sv_en.w)
sv_en.lin(S('T2RP')); sv_in.add(S('T2RP'),ins_st)
rv_f,rv_b,rv_i,rv_u,rv_s,rv_c,rv_h,rv_v,rv_z,rv_n=[R() for _ in range(10)]
lit('T2RP',b'<w:rPr>','T2RP1')
fsm.set(rv_f,S('T2RP'),SV['font']);fsm.set(rv_b,S('T2RP'),SV['bold']);fsm.set(rv_i,S('T2RP'),SV['ital']);fsm.set(rv_u,S('T2RP'),SV['und']);fsm.set(rv_s,S('T2RP'),SV['strike']);fsm.set(rv_c,S('T2RP'),SV['color']);fsm.set(rv_h,S('T2RP'),SV['hl']);fsm.set(rv_v,S('T2RP'),SV['vert']);fsm.set(rv_z,S('T2RP'),SV['size']);fsm.set(rv_n,S('T2RP'),SV['nop'])
on('T2RP1',(rv_f,'T2Rf1',None),(t2full,'T2Rf0',None),(None,'T2R2',None))
lit('T2Rf1',b'<w:rFonts w:ascii="Caladea" w:hAnsi="Caladea"/>','T2R2'); lit('T2Rf0',b'<w:rFonts w:ascii="Carlito" w:hAnsi="Carlito"/>','T2R2')
on('T2R2',(rv_b,'T2Rb1',None),(t2full,'T2Rb0',None),(None,'T2R3',None))
lit('T2Rb1',b'<w:b/>','T2R3'); lit('T2Rb0',b'<w:b w:val="0"/>','T2R3')
on('T2R3',(rv_i,'T2Ri1',None),(t2full,'T2Ri0',None),(None,'T2R4',None))
lit('T2Ri1',b'<w:i/>','T2R4'); lit('T2Ri0',b'<w:i w:val="0"/>','T2R4')
on('T2R4',(rv_s,'T2Rs1',None),(None,'T2R4n',None)); lit('T2Rs1',b'<w:strike/>','T2R4n')
on('T2R4n',(rv_n,'T2Rn',None),(None,'T2R5',None)); lit('T2Rn',b'<w:noProof/>','T2R5')
e=S('T2R5'); h_=net.decode(rv_c,32,e)
on('T2R5',*[(h_[j],f'T2Rk{j}',None) for j in range(1,32)],(t2full,'T2Rk0',None),(None,'T2R6',None))
for j in range(32): lit(f'T2Rk{j}',('<w:color w:val="%02X%02X%02X"/>'%PAL_F[j]).encode(),'T2R6')
lit('T2R6',b'<w:sz w:val="','T2R7')
e=S('T2R7'); h_=net.decode(rv_z,len(rom.PTS),e); hp=X()
for si,h in enumerate(h_): hp=hp+h*(rom.PTS[si]*2)
vnum('T2R7',hp,'T2R8'); lit('T2R8',b'"/>','T2R9')
e=S('T2R9'); h_=net.decode(rv_h,8,e)
on('T2R9',*[(h_[j],f'T2Rh{j}',None) for j in range(1,8)],(None,'T2RA',None))
for j in range(1,8): lit(f'T2Rh{j}',('<w:highlight w:val="%s"/>'%HL_NAMES[j-1]).encode(),'T2RA')
on('T2RA',(rv_u,'T2Ru1',None),(t2full,'T2Ru0',None),(None,'T2RB',None))
lit('T2Ru1',b'<w:u w:val="single"/>','T2RB'); lit('T2Ru0',b'<w:u w:val="none"/>','T2RB')
e=S('T2RB')
on('T2RB',(net.eq(rv_v,1,e),'T2Rv1',None),(net.eq(rv_v,2,e),'T2Rv2',None),(None,'T2RC',None))
lit('T2Rv1',b'<w:vertAlign w:val="superscript"/>','T2RC'); lit('T2Rv2',b'<w:vertAlign w:val="subscript"/>','T2RC')
lit('T2RC',b'</w:rPr>','T2PR')
# paragraph properties from al, pind, pfirst_, plsp, pspb, pspa. lsf is the list kind.
lit('T2PP0',b'<w:spacing w:before="','T2P1'); vnum('T2P1',pspb*15,'T2P2')
lit('T2P2',b'" w:after="','T2P3'); vnum('T2P3',pspa*15,'T2P4')
lit('T2P4',b'" w:line="','T2P5')
e=S('T2P5'); h_=net.decode(plsp,6,e); lv=X()
for i,v_ in enumerate((240,276,360,480,600,720)): lv=lv+h_[i]*v_
vnum('T2P5',lv,'T2P6')
lit('T2P6',b'" w:lineRule="auto"/>','T2P7')
e=S('T2P7')
pfv=pf_val(pfirst_)
hasind=net.and_(e,ONE-net.step(lsf),net.or_(net.step(pind),net.step(pfv),net.step(-pfv)))
on('T2P7',(hasind,'T2Pi',None),(None,'T2Pj',None))
lit('T2Pi',b'<w:ind w:left="','T2Pi1'); vnum('T2Pi1',pind*15,'T2Pi2')
e=S('T2Pi2'); on('T2Pi2',(net.step(pfv),'T2Pi3',None),(net.step(-pfv),'T2Pi5',None),(None,'T2Pi7',None))
lit('T2Pi3',b'" w:firstLine="','T2Pi4'); vnum('T2Pi4',pfv*15,'T2Pi7')
lit('T2Pi5',b'" w:hanging="','T2Pi6'); vnum('T2Pi6',pfv*(-15),'T2Pi7')
lit('T2Pi7',b'"/>','T2Pj')
on('T2Pj',(net.step(lsf),'A2_CSL',None),(None,'A2_JC',None)); lit('A2_CSL',b'<w:contextualSpacing/>','A2_JC'); lit('A2_JC',b'<w:jc w:val="','T2Pk')
e=S('T2Pk'); h_=net.decode(al,4,e)
on('T2Pk',(h_[1],'T2Pc1',None),(h_[2],'T2Pc2',None),(h_[3],'T2Pc3',None),(None,'T2Pc0',None))
lit('T2Pc0',b'left','T2Pl');lit('T2Pc1',b'center','T2Pl');lit('T2Pc2',b'right','T2Pl');lit('T2Pc3',b'both','T2Pl')
lit('T2Pl',b'"/>','T2PP')
# text bytes from a table cell string; t2w is the address, the string ends at a zero cell
on('T2SS',(None,'T2SS1',{r1:t2w}))
e=S('T2SS1'); em_en.lin(net.and_(e,net.step(R1))); em_b.add(net.and_(e,net.step(R1)),R1)
on('T2SS1',(net.step(R1),'T2SS',{t2w:t2w+1}),(None,'T2SR',None))
# ---- styles part: written between zdyn and zdend in t3_features ----
on('T2Y0',(None,'T2Y1',{t2j:0}))
e=S('T2Y1'); on('T2Y1',(net.ge(t2j,nsty,e),'T2YT',None),(None,'T2Y1b',{r2:as_x(STY)+t2j*STYN+47}))
on('T2Y1b',(net.step(R2),'T2Y1',{t2j:t2j+1}),(None,'T2Y2',None))   # character styles are not written back
lit('T2Y2',b'<w:style w:type="paragraph"','T2Y3')
e=S('T2Y3'); on('T2Y3',(net.eq(t2j,0,e),'T2Yd',None),(None,'T2Y4',None))
lit('T2Yd',b' w:default="1"','T2Y4')
lit('T2Y4',b' w:styleId="','T2Y5')
on('T2Y5',(None,'T2SS',{t2w:as_x(STY)+t2j*STYN+8,t2sr.r:t2sr.id('T2Y6')}))
lit('T2Y6',b'"><w:name w:val="','T2Y7')
on('T2Y7',(None,'T2SS',{t2w:as_x(STY)+t2j*STYN+28,t2sr.r:t2sr.id('T2Y8')}))
lit('T2Y8',b'"/><w:qFormat/><w:pPr>','T2Y9')
on('T2Y9',(None,'T2Ya',{rl:as_x(STY)+t2j*STYN}))
e=S('T2Ya')
on('T2Ya',(None,'T2PP0',{ins_st:rl.out[0],al:rl.out[1],pind:rl.out[2],pfirst_:rl.out[3],plsp:rl.out[4],pspb:rl.out[5],pspa:rl.out[6],lsf:0,t2full:0,t2pp.r:t2pp.id('T2Yb')}))
lit('T2Yb',b'</w:pPr>','T2Yc')
on('T2Yc',(None,'T2RP',{t2pr.r:t2pr.id('T2Ye')}))
lit('T2Ye',b'</w:style>','T2Yf')
on('T2Yf',(None,'T2Y1',{t2j:t2j+1}))
lit('T2YT',docx_tpl.STY_T,'T2YE')
# freeze crc and size of styles.xml and patch its local header
crcL=X();crcH=X()
for j,c_ in enumerate(crcr):
    if j<16: crcL=crcL+c_*(1<<j)
    else: crcH=crcH+c_*(1<<(j-16))
cfL=R();cfH=R();dsize=R()
def le_bytes(val,en,n=4):
    bt=net.bits(val,8*n,en)
    return [sum((bt[8*k+i]*(1<<i) for i in range(8)),X()) for k in range(n)]
def crc_b(ix,en):
    return le_bytes(cfL if ix<2 else cfH,en,2)[ix%2]
# subroutine: write crc and both sizes at t2pa
vals=[('c',i) for i in range(4)]+[('s',i) for i in range(4)]+[('u',i) for i in range(4)]
cur_='T2Q'
for n_,(kd,ix) in enumerate(vals):
    ee2=S(cur_); bv_=crc_b(ix,ee2) if kd=='c' else le_bytes(dsize if kd=='s' else usize,ee2)[ix]
    nx_=f'T2Q{n_}'
    on(cur_,(None,nx_,{fw2:(t2pa+n_,bv_)})); cur_=nx_
on(cur_,(None,'T2SR',None))
fsm.set(pi,S('SAVE'),0); fsm.set(t2run,S('SAVE'),0); fsm.set(t2pk,S('SAVE'),0)
e=S('SVP'); on('SVP',(net.ge(pi,npar,e),'T3_SVE',None),(net.ge(fp,3900000,e),'T3_SVE',None),(None,'SVa',{r1:as_x(PT)+pi}))
on('SVa',(None,'SVm',{pbs:R1,rl:R1+LEN,rp6:R1+PIND,rc:R1+2062,rmeta:R1+META,rim:R1+IMF}))
e=S('SVm'); lb_=net.bits(rl.out[3],4,e)
on('SVm',(None,'T3_SV0',{scols:rc.out[0],sci:rc.out[1],scw:MT[0],ssh:MT[2],pim:rim.out[0],pih:rim.out[1],pio:rim.out[2],plen_:rl.out[0],al:rl.out[2],lsf:lb_[0]+lb_[1]*2,plvl:lb_[2]+lb_[3]*2,pbk:rl.out[7],off:0,pind:rp6.out[0],pfirst_:rp6.out[1],plsp:rp6.out[2],pspb:rp6.out[3],pspa:rp6.out[4],psty:rp6.out[5],t2psv:99999}))
lit('SVj',b'<w:p><w:pPr>','SVa2')
on('SVa2',(net.step(psty),'T2W0',None),(None,'T2W2',None))
lit('T2W0',b'<w:pStyle w:val="','T2W1')
on('T2W1',(None,'T2SS',{t2w:as_x(STY)+psty*STYN+8,t2sr.r:t2sr.id('T2W1b')}))
lit('T2W1b',b'"/>','T2W2')
on('T2W2',(pbk,'T2W3',None),(None,'T2W4',None)); lit('T2W3',b'<w:pageBreakBefore/>','T2W4')
e=S('T2W4')
newrun=net.and_(e,net.eq(lsf,2,e),ONE-net.eq(t2pk,2,e))
fsm.set(t2run,newrun,t2run+1); fsm.set(t2pk,e,lsf)
on('T2W4',(net.step(lsf),'T2W5',None),(None,'T2W9',None))
lit('T2W5',b'<w:numPr><w:ilvl w:val="','T2W6')
vnum('T2W6',plvl,'T2W7'); lit('T2W7',b'"/><w:numId w:val="','T2W8')
e=S('T2W8'); vnum('T2W8',G_(net.min_(t2run,docx_tpl.NUMRUNS)+1,net.eq(lsf,2,e))+net.eq(lsf,1,e),'T2W8b')
lit('T2W8b',b'"/></w:numPr>','T2W9')
on('T2W9',(None,'T3_TA0',None))
on('T2Wa',(None,'T3_SNA',None))
e=S('SVC'); on('SVC',(net.step(pim),'T3_SD0',None),(net.ge(off,plen_,e),'SVe',None),(None,'SVr',{r1:pbs+off,r2:pbs+1024+off}))
e=S('SVr'); chg=net.step(net.step(R2-t2psv)+net.step(t2psv-R2))
on('SVr',(net.ge(R1,1000,e),'T3_SF0',{ins_ch:R1}),(chg,'SVx',{ins_ch:R1,ins_st:R2}),(None,'SVch',{ins_ch:R1,ins_st:R2}))
e=S('SVx'); first=net.eq(t2psv,99999,e)
on('SVx',(first,'T4_SO',None),(None,'T4_SC',{t4cr.r:t4cr.id('T4_SO')}))
lit('SVo',b'<w:r>','SVo2')
on('SVo2',(None,'T2RP',{t2full:net.step(psty),t2pr.r:t2pr.id('T4_TO')}))
on('SVrs',(None,'SVch',{t2psv:ins_st}))
# text bytes, in UTF-8. Latin-1 takes two bytes; the punctuation block has compiled byte sequences.
e=S('SVch'); amp=net.eq(ins_ch,38,e);ltc=net.eq(ins_ch,60,e);gtc=net.eq(ins_ch,62,e);hi1=net.ge(ins_ch,160,e);pun=net.and_(net.ge(ins_ch,128,e),net.lt(ins_ch,160,e)); other=e-amp-ltc-gtc-hi1-pun
em_en.lin(other); em_b.add(other,ins_ch)
on('SVch',(amp,'SVa_',{off:off+1}),(ltc,'SVl_',{off:off+1}),(gtc,'SVg_',{off:off+1}),(hi1,'T2U2',{off:off+1,t2ur.r:t2ur.id('SVC')}),(pun,'T2U3',{off:off+1,t2ur.r:t2ur.id('SVC')}),(None,'SVC',{off:off+1}))
e=S('T2U2'); c3=net.ge(ins_ch,192,e); em_en.lin(e); em_b.add(e,194+c3)
on('T2U2',(None,'T2U2b',None))
e=S('T2U2b'); c3=net.ge(ins_ch,192,e); em_en.lin(e); em_b.add(e,as_x(ins_ch)-c3*64)
on('T2U2b',(None,'T2UR',None))
def pun_byte(st,nx,ix):
    e=S(st); h_=net.decode(ins_ch-128,32,e); v=X(); more=X()
    for c_ in range(128,160):
        ch_=rom.cp1252(c_) or '?'; bs=ch_.encode('utf-8')
        if ix<len(bs): v=v+h_[c_-128]*bs[ix]
        if ix+1<len(bs): more=more+h_[c_-128]
    em_en.lin(e); em_b.add(e,v)
    return more
m0=pun_byte('T2U3','T2U4',0); on('T2U3',(net.step(m0),'T2U4',None),(None,'T2UR',None))
m1=pun_byte('T2U4','T2U5',1); on('T2U4',(net.step(m1),'T2U5',None),(None,'T2UR',None))
m2=pun_byte('T2U5','T2UR',2); on('T2U5',(None,'T2UR',None))
lit('SVa_',b'&amp;','SVC');lit('SVl_',b'&lt;','SVC');lit('SVg_',b'&gt;','SVC')
e=S('SVe'); on('SVe',(net.eq(t2psv,99999,e),'SVe2',None),(None,'T4_SC',{t4cr.r:t4cr.id('SVe2')}))
on('SVe2',(None,'T3_CE0',None))
