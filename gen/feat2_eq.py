# ---- feat2: states of the new built up forms: measure, paint, save as OMML, print. Kinds and cells: gen/feat2_eq_pre.py ----
_f2g=net.cur[0]; net.group('feat2 built up math')
_f2r=_qrec(a6qk); F2SM=as_x(rom.lit(9)); F2NO=as_x(0); F2BK=(0,0,0)
F2SYM=as_x(rom.sz_raw(rom.SZ.index(18))+MATHRAW); F2A18=rom.metrics(4)[0]   # the n-ary symbol: 18 pt, upright
# symbol width, at the end of measuring: a sum or product sign is measured, the integral is drawn from rects
e=S('F2Q_SM'); _k4=net.eq(a6qkd,4,e); _ss1=net.and_(_k4,net.eq(a6qsb,1,e)); _ss2=net.and_(_k4,net.eq(a6qsb,2,e))
measure(e,32+G_(as_x(UO+931-32),_ss1)+G_(as_x(UO+928-32),_ss2),F2SYM)
on('F2Q_SM',(None,'A6Q_B8',{a6qsw:G_(adv,net.or_(_ss1,_ss2))+G_(as_x(9),net.and_(e,ONE-_ss1,ONE-_ss2))}))
# ---- paint, from the baseline down the screen ----
_fb=sy+lasc; _fox=net.relu(a6qnw-2); _fcx=x+a6qwd*0.5; _fym=_fb-A0Q+1
def _frect(*r): return tuple(r)+(F2BK,col)
# root with an index: the index small and raised, then the radical sign after it
_qdraw('F2Q_K3',_f2r+8,a6qnl,_fb-8-A9Q,F2SM,'F2Q_K3_b')
on('F2Q_K3_b',(None,'F2Q_K3_c',{rB:_frect(x+_fox+1,_fb-5,3,1),rC:_frect(x+_fox+4,_fb-5,1,6),rD:_frect(x+_fox+5,_fb-A0Q-1,1,A0Q+2),sx:x+_fox+7,a6qm:0}))
_qdraw('F2Q_K3_c',_f2r+36,a6qdl,_fb-A0Q,F2NO,'F2Q_K3_d')
on('F2Q_K3_d',(None,'A6Q_CE',{rB:_frect(x+_fox+5,_fb-A0Q-1,a6qwd-_fox-6,1)}))
# n-ary: the sign, the lower limit under it, the upper limit over it
e=S('F2Q_K4'); _s1=net.eq(a6qsb,1,e); _s2=net.eq(a6qsb,2,e); _sg=net.or_(_s1,_s2); _sym=G_(as_x(UO+931),_s1)+G_(as_x(UO+928),_s2)
_sx=x+(a6qwd-a6qsw)*0.5; _sy_=_fb+2-F2A18; _lo={sx:x+(a6qwd-a6qnw)*0.5,a6qm:0}
on('F2Q_K4',(net.and_(_sg,a6qs),'F2Q_K4_m',{gly:(_sym,F2SYM,_sx,_sy_,0,1),**_lo}),(_sg,'F2Q_K4_m',{gly:(_sym,F2SYM,_sx,_sy_,0,0),**_lo}),
 (None,'F2Q_K4_m',{rB:_frect(_fcx,_fb-13,1,16),rC:_frect(_fcx+1,_fb-14,2,1),rD:_frect(_fcx-2,_fb+2,2,1),**_lo}))
_qdraw('F2Q_K4_m',_f2r+8,a6qnl,_fb+4,F2SM,'F2Q_K4_u')
on('F2Q_K4_u',(None,'F2Q_K4_v',{sx:x+(a6qwd-a6qdw)*0.5,a6qm:0}))
_qdraw('F2Q_K4_v',_f2r+36,a6qdl,_fb-14-A9Q,F2SM,'A6Q_CE')
# accent: the base, then its mark above
_qdraw('F2Q_K5',_f2r+8,a6qnl,_fb-A0Q,F2NO,'F2Q_K5_m')
e=S('F2Q_K5_m'); _ak=[net.eq(a6qsb,k_,e) for k_ in range(1,6)]
on('F2Q_K5_m',(_ak[0],'A6Q_CE',{rB:_frect(_fcx-2,_fym+1,2,1),rC:_frect(_fcx,_fym,1,1),rD:_frect(_fcx+1,_fym+1,2,1)}),
 (_ak[2],'F2Q_K5_t',{rB:_frect(_fcx-3,_fym+1,1,1),rC:_frect(_fcx-2,_fym,2,1),rD:_frect(_fcx,_fym+1,2,1)}),
 (_ak[3],'A6Q_CE',{rB:_frect(_fcx-1,_fym,2,2)}),
 (_ak[4],'A6Q_CE',{rB:_frect(x+1,_fym+1,a6qwd-2,1),rC:_frect(x+a6qwd-3,_fym,1,3),rD:_frect(x+a6qwd-4,_fym-1,1,5)}),
 (None,'A6Q_CE',{rB:_frect(x+1,_fym+1,a6qwd-2,1)}))
on('F2Q_K5_t',(None,'A6Q_CE',{rB:_frect(_fcx+2,_fym,1,1)}))
# delimiter: as tall as its line, so it grows with a fraction, an n-ary or a matrix beside it
e=S('F2Q_K6'); _dk={c_:net.eq(a6qsb,c_,e) for c_ in (40,41,91,93)}
on('F2Q_K6',(_dk[40],'A6Q_CE',{rB:_frect(x+2,sy+4,1,lhh-8),rC:_frect(x+3,sy+2,1,2),rD:_frect(x+3,sy+lhh-4,1,2)}),
 (_dk[41],'A6Q_CE',{rB:_frect(x+3,sy+4,1,lhh-8),rC:_frect(x+2,sy+2,1,2),rD:_frect(x+2,sy+lhh-4,1,2)}),
 (_dk[91],'A6Q_CE',{rB:_frect(x+2,sy+2,1,lhh-4),rC:_frect(x+3,sy+2,2,1),rD:_frect(x+3,sy+lhh-3,2,1)}),
 (_dk[93],'A6Q_CE',{rB:_frect(x+3,sy+2,1,lhh-4),rC:_frect(x+1,sy+2,2,1),rD:_frect(x+1,sy+lhh-3,2,1)}),
 (None,'A6Q_CE',{rB:_frect(x+2,sy+2,1,lhh-4)}))
# matrix: two rows where a fraction has its texts, columns apart by a space
_qdraw('F2Q_K7',_f2r+8,a6qnl,_fb-6-A9Q,F2SM,'F2Q_K7_b',amp=True)
on('F2Q_K7_b',(None,'F2Q_K7_c',{a6qm:0,sx:x+(a6qwd-a6qdw)*0.5}))
_qdraw('F2Q_K7_c',_f2r+36,a6qdl,_fb-3,F2SM,'A6Q_CE',amp=True)
# ---- OMML. A delimiter or an n-ary opens a container that the following math goes into; a closing delimiter or the end of the math zone closes it.
# Open containers are a stack in one register, two bits each: 1 delimiter, 2 n-ary.
_MT=b'<m:r><m:t xml:space="preserve">'; _ME=b'</m:t></m:r>'
lit('F2Q_X3',b'<m:rad><m:deg>'+_MT,'F2Q_X3_a'); _qtext('F2Q_X3_a',_f2r+8,a6qnl,'F2Q_X3_b'); lit('F2Q_X3_b',_ME+b'</m:deg><m:e>'+_MT,'F2Q_X3_c')
on('F2Q_X3_c',(None,'F2Q_X3_d',{a6qm:0})); _qtext('F2Q_X3_d',_f2r+36,a6qdl,'F2Q_X3_e'); lit('F2Q_X3_e',_ME+b'</m:e></m:rad>','A6E_ER')
e=S('F2Q_X4'); on('F2Q_X4',(net.eq(a6qsb,1,e),'F2Q_X4_s',None),(net.eq(a6qsb,2,e),'F2Q_X4_p',None),(None,'F2Q_X4_i',None))
lit('F2Q_X4_s',b'<m:nary><m:naryPr><m:chr m:val="\xe2\x88\x91"/>','F2Q_X4_a'); lit('F2Q_X4_p',b'<m:nary><m:naryPr><m:chr m:val="\xe2\x88\x8f"/>','F2Q_X4_a'); lit('F2Q_X4_i',b'<m:nary><m:naryPr>','F2Q_X4_a')
lit('F2Q_X4_a',b'<m:limLoc m:val="undOvr"/></m:naryPr><m:sub>'+_MT,'F2Q_X4_b'); _qtext('F2Q_X4_b',_f2r+8,a6qnl,'F2Q_X4_c'); lit('F2Q_X4_c',_ME+b'</m:sub><m:sup>'+_MT,'F2Q_X4_d')
on('F2Q_X4_d',(None,'F2Q_X4_e',{a6qm:0})); _qtext('F2Q_X4_e',_f2r+36,a6qdl,'F2Q_X4_f'); lit('F2Q_X4_f',_ME+b'</m:sup><m:e>','F2Q_X4_g')
on('F2Q_X4_g',(None,'A6E_ER',{a6ws:a6ws*4+2}))
e=S('F2Q_X5'); _xa=[net.eq(a6qsb,k_,e) for k_ in range(1,6)]
on('F2Q_X5',*[(_xa[k_],f'F2Q_X5_{k_}',None) for k_ in range(1,5)],(None,'F2Q_X5_0',None))
for k_,ch_ in enumerate((b'\xcc\x82',b'\xcc\x85',b'\xcc\x83',b'\xcc\x87',b'\xe2\x83\x97')):
    lit(f'F2Q_X5_{k_}',b'<m:acc><m:accPr><m:chr m:val="'+ch_+b'"/></m:accPr><m:e>'+_MT,'F2Q_X5_a')
_qtext('F2Q_X5_a',_f2r+8,a6qnl,'F2Q_X5_b'); lit('F2Q_X5_b',_ME+b'</m:e></m:acc>','A6E_ER')
e=S('F2Q_X6'); _xo={c_:net.eq(a6qsb,c_,e) for c_ in (40,91,124)}
on('F2Q_X6',(_xo[40],'F2Q_X6_p',None),(_xo[91],'F2Q_X6_b',None),(_xo[124],'F2Q_X6_v',None),(None,'F2E_DC',None))
for n_,(o_,c_) in (('p','()'),('b','[]'),('v','||')):
    lit('F2Q_X6_'+n_,b'<m:d><m:dPr><m:begChr m:val="'+o_.encode()+b'"/><m:endChr m:val="'+c_.encode()+b'"/></m:dPr><m:e>','F2Q_X6_z')
on('F2Q_X6_z',(None,'A6E_ER',{a6ws:a6ws*4+1}))
_MC=_ME+b'</m:e><m:e>'+_MT
lit('F2Q_X7',b'<m:m><m:mr><m:e>'+_MT,'F2Q_X7_a'); _qtext('F2Q_X7_a',_f2r+8,a6qnl,'F2Q_X7_b',amp=_MC); lit('F2Q_X7_b',_ME+b'</m:e></m:mr><m:mr><m:e>'+_MT,'F2Q_X7_c')
on('F2Q_X7_c',(None,'F2Q_X7_d',{a6qm:0})); _qtext('F2Q_X7_d',_f2r+36,a6qdl,'F2Q_X7_e',amp=_MC); lit('F2Q_X7_e',_ME+b'</m:e></m:mr></m:m>','A6E_ER')
def _f2pop(st,nn,nd,empty,after_d):
    e=S(st); b_=net.bits(a6ws,24,e); top=b_[0]+b_[1]*2
    on(st,(net.eq(a6ws,0,e),empty,None),(net.eq(top,2,e),nn,{a6ws:(a6ws-2)*0.25}),(None,nd,{a6ws:(a6ws-top)*0.25}))
    lit(nn,b'</m:e></m:nary>',st); lit(nd,b'</m:e></m:d>',after_d)
_f2pop('F2E_DC','F2E_DN','F2E_DD','A6E_ER','A6E_ER')   # a closing delimiter closes the n-ary sums inside it, then its own; with none open it writes nothing
_f2pop('F2E_FL','F2E_FN','F2E_FD','F2E_FR','F2E_FL')   # the end of the math zone closes everything
fsm.set(a6ws,S('SAVE'),0)
# ---- PDF, in screen pixels up from the baseline ----
def _fpd(st,items,nx):
    "Writes literals and numbers in turn; two numbers in a row get a space between them."
    seq=[]
    for it in items:
        if not isinstance(it,bytes) and seq and not isinstance(seq[-1],bytes): seq.append(b' ')
        seq.append(it)
    for i_,it in enumerate(seq):
        cur=st if i_==0 else f'{st}_{i_}'; nxt=nx if i_==len(seq)-1 else f'{st}_{i_+1}'
        if isinstance(it,bytes): lit(cur,it,nxt)
        else: number(cur,it,nxt)
_SK=b'0 0 0 RG 1 w '
_ptext('F2Q_P3',qxx,qyb+8,12,_f2r+8,a6qnl,'F2Q_P3_b')
_prect('F2Q_P3_b',qxx+a6qox+1,qyb+5,3,1,'F2Q_P3_c'); _prect('F2Q_P3_c',qxx+a6qox+4,net.relu(qyb-1),1,6,'F2Q_P3_d'); _prect('F2Q_P3_d',qxx+a6qox+5,net.relu(qyb-1),1,A0Q+2,'F2Q_P3_e'); _prect('F2Q_P3_e',qxx+a6qox+5,qyb+A0Q,a6qwd-a6qox-6,1,'F2Q_P3_f')
on('F2Q_P3_f',(None,'F2Q_P3_g',{a6qm:0})); _ptext('F2Q_P3_g',qxx+a6qox+7,qyb,15,_f2r+36,a6qdl,'A6Q_PE')
_pcx=qxx+a6qwd*0.5; _px0=_pcx-a6qsw*0.5+1; _px1=_pcx+a6qsw*0.5-1
e=S('F2Q_P4'); on('F2Q_P4',(net.eq(a6qsb,1,e),'F2Q_P4_s',None),(net.eq(a6qsb,2,e),'F2Q_P4_p',None),(None,'F2Q_P4_i',None))
_fpd('F2Q_P4_s',[_SK,_px1,qyb+12,b' m ',_px0,qyb+12,b' l ',_pcx,qyb+5,b' l ',_px0,qyb-2,b' l ',_px1,qyb-2,b' l S\n'],'F2Q_P4_l')
_prect('F2Q_P4_p',_px0,qyb+12,a6qsw-2,2,'F2Q_P4_q'); _prect('F2Q_P4_q',_px0+1,qyb-2,2,14,'F2Q_P4_r'); _prect('F2Q_P4_r',_px1-3,qyb-2,2,14,'F2Q_P4_l')
_fpd('F2Q_P4_i',[_SK,_pcx+4,qyb+13,b' m ',_pcx+2,qyb+16,_pcx,qyb+14,_pcx,qyb+5,b' c ',_pcx,qyb-4,_pcx-2,qyb-6,_pcx-4,qyb-3,b' c S\n'],'F2Q_P4_l')
on('F2Q_P4_l',(None,'F2Q_P4_m',{a6qm:0})); _ptext('F2Q_P4_m',qxx+(a6qwd-a6qnw)*0.5,qyb-16,12,_f2r+8,a6qnl,'F2Q_P4_u')
on('F2Q_P4_u',(None,'F2Q_P4_v',{a6qm:0})); _ptext('F2Q_P4_v',qxx+(a6qwd-a6qdw)*0.5,qyb+14,12,_f2r+36,a6qdl,'A6Q_PE')
_ptext('F2Q_P5',qxx+1,qyb,15,_f2r+8,a6qnl,'F2Q_P5_m')
e=S('F2Q_P5_m'); _pa=[net.eq(a6qsb,k_,e) for k_ in range(1,6)]
on('F2Q_P5_m',(_pa[0],'F2Q_P5_h',None),(_pa[2],'F2Q_P5_t',None),(_pa[3],'F2Q_P5_d',None),(_pa[4],'F2Q_P5_v',None),(None,'F2Q_P5_b',None))
_fpd('F2Q_P5_h',[_SK,_pcx-3,qyb+12,b' m ',_pcx,qyb+15,b' l ',_pcx+3,qyb+12,b' l S\n'],'A6Q_PE')
_fpd('F2Q_P5_t',[_SK,_pcx-3,qyb+13,b' m ',_pcx-1,qyb+16,_pcx+1,qyb+11,_pcx+3,qyb+14,b' c S\n'],'A6Q_PE')
_prect('F2Q_P5_d',_pcx-1,qyb+13,2,2,'A6Q_PE'); _prect('F2Q_P5_b',qxx+1,qyb+13,a6qwd-2,1,'A6Q_PE')
_prect('F2Q_P5_v',qxx+1,qyb+13,a6qwd-2,1,'F2Q_P5_w'); _fpd('F2Q_P5_w',[_SK,qxx+a6qwd-4,qyb+16,b' m ',qxx+a6qwd-1,qyb+13,b' l ',qxx+a6qwd-4,qyb+10,b' l S\n'],'A6Q_PE')
_ptop=qph-(qyy-qtop); _pbot=_ptop-qh
e=S('F2Q_P6'); _pd={c_:net.eq(a6qsb,c_,e) for c_ in (40,41,91,93)}
on('F2Q_P6',(_pd[40],'F2Q_P6_a',None),(_pd[41],'F2Q_P6_b',None),(_pd[91],'F2Q_P6_c',None),(_pd[93],'F2Q_P6_d',None),(None,'F2Q_P6_e',None))
_fpd('F2Q_P6_a',[_SK,qxx+4,_ptop-2,b' m ',qxx+1,_ptop-6,qxx+1,_pbot+6,qxx+4,_pbot+2,b' c S\n'],'A6Q_PE')
_fpd('F2Q_P6_b',[_SK,qxx+2,_ptop-2,b' m ',qxx+5,_ptop-6,qxx+5,_pbot+6,qxx+2,_pbot+2,b' c S\n'],'A6Q_PE')
_fpd('F2Q_P6_c',[_SK,qxx+4,_ptop-2,b' m ',qxx+2,_ptop-2,b' l ',qxx+2,_pbot+2,b' l ',qxx+4,_pbot+2,b' l S\n'],'A6Q_PE')
_fpd('F2Q_P6_d',[_SK,qxx+2,_ptop-2,b' m ',qxx+4,_ptop-2,b' l ',qxx+4,_pbot+2,b' l ',qxx+2,_pbot+2,b' l S\n'],'A6Q_PE')
_prect('F2Q_P6_e',qxx+2,_pbot+2,1,qh-4,'A6Q_PE')
_ptext('F2Q_P7',qxx+(a6qwd-a6qnw)*0.5,qyb+7,12,_f2r+8,a6qnl,'F2Q_P7_b',amp=True)
on('F2Q_P7_b',(None,'F2Q_P7_c',{a6qm:0})); _ptext('F2Q_P7_c',qxx+(a6qwd-a6qdw)*0.5,net.relu(qyb+3-A9Q),12,_f2r+36,a6qdl,'A6Q_PE',amp=True)
exec(open('feat2_eqrd.py').read())
net.group(_f2g)
