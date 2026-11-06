# ---- rv_a6: built up fractions and roots. One character in the text (code 300 and up) stands for a record: kind, width, lengths, then the two texts.
# Its glyphs and rules are drawn by these states. Record: 0 kind (1 fraction, 2 root), 1 width, 2 and 3 text lengths, 4 and 5 text widths, 8 first text, 36 second text.
a6qj=R();a6qd=R();a6qsr=R();a6qe=R();a6qnb=R();a6qnl=R();a6qdb=R();a6qdl=R();a6qkd=R();a6qm=R();a6qw=R();a6qnw=R();a6qst=R();a6qc=R();a6qwd=R();a6qdw=R();a6qx=R()
fsm.set(a6qn,S('OP0'),0)
_qrec=lambda k_:as_x(EQT)+k_*EQR
_aln=lambda v,en: net.or_(net.and_(net.ge(v,48,en),net.lt(v,58,en)),net.and_(net.ge(v,65,en),net.lt(v,91,en)),net.and_(net.ge(v,97,en),net.lt(v,123,en)))
SKIP={a6qi:a6qi+1}
on('A6Q_EQ2',(net.step(a6qcv),'T4_EQ0',{ap:cp,ao:co}),(None,'T4_EQ0',None))
e=S('A6Q_S0'); on('A6Q_S0',(net.ge(a6qi,clen,e),'A6Q_RR',None),(None,'A6Q_S1',{rl:cb+a6qi,r2:cb+1024+a6qi}))
fd_in('A6Q_S1')
e=S('A6Q_S1'); W8=rl.out; _ok=net.or_(a6qa,net.and_(FD['font'],FD['nop']))
_isq=net.and_(_ok,net.eq(W8[0],115,e),net.eq(W8[1],113,e),net.eq(W8[2],114,e),net.eq(W8[3],116,e),net.eq(W8[4],40,e))
_isl=net.and_(_ok,net.eq(W8[0],47,e),net.step(a6qi))
on('A6Q_S1',(_isq,'A6Q_R0',{a6qj:a6qi+5,a6qd:1}),(_isl,'A6Q_N0',None),(None,'A6Q_S0',SKIP))
# root: the matching parenthesis
e=S('A6Q_R0'); on('A6Q_R0',(net.ge(a6qj,clen,e),'A6Q_S0',SKIP),(None,'A6Q_R1',{r1:cb+a6qj}))
e=S('A6Q_R1'); _op=net.eq(R1,40,e);_cl=net.eq(R1,41,e)
on('A6Q_R1',(_op,'A6Q_R0',{a6qd:a6qd+1,a6qj:a6qj+1}),(net.and_(_cl,net.eq(a6qd,1,e)),'A6Q_B0',{a6qkd:2,a6qnb:a6qi+5,a6qnl:a6qj-a6qi-5,a6qdb:0,a6qdl:0,a6qsr:a6qi,a6qe:a6qj+1}),(_cl,'A6Q_R0',{a6qd:a6qd-1,a6qj:a6qj+1}),(None,'A6Q_R0',{a6qj:a6qj+1}))
# fraction: what stands left of the slash. a6qj counts from one, so that zero means the start of the paragraph
on('A6Q_N0',(None,'A6Q_N1',{r1:cb+a6qi-1}))
e=S('A6Q_N1'); on('A6Q_N1',(net.eq(R1,41,e),'A6Q_N2',{a6qj:a6qi-1,a6qd:1}),(_aln(R1,e),'A6Q_N6',{a6qj:a6qi}),(None,'A6Q_S0',SKIP))
e=S('A6Q_N2'); on('A6Q_N2',(net.eq(a6qj,0,e),'A6Q_S0',SKIP),(None,'A6Q_N3',{r1:cb+a6qj-1}))
e=S('A6Q_N3'); _op=net.eq(R1,40,e);_cl=net.eq(R1,41,e)
on('A6Q_N3',(_cl,'A6Q_N2',{a6qd:a6qd+1,a6qj:a6qj-1}),(net.and_(_op,net.eq(a6qd,1,e)),'A6Q_D0',{a6qnb:a6qj,a6qnl:a6qi-1-a6qj,a6qsr:a6qj-1}),(_op,'A6Q_N2',{a6qd:a6qd-1,a6qj:a6qj-1}),(None,'A6Q_N2',{a6qj:a6qj-1}))
e=S('A6Q_N6'); on('A6Q_N6',(net.eq(a6qj,0,e),'A6Q_D0',{a6qnb:0,a6qnl:a6qi,a6qsr:0}),(None,'A6Q_N7',{r1:cb+a6qj-1}))
e=S('A6Q_N7'); on('A6Q_N7',(_aln(R1,e),'A6Q_N6',{a6qj:a6qj-1}),(None,'A6Q_D0',{a6qnb:a6qj,a6qnl:a6qi-a6qj,a6qsr:a6qj}))
# and right of it
e=S('A6Q_D0'); on('A6Q_D0',(net.ge(a6qi+1,clen,e),'A6Q_S0',SKIP),(None,'A6Q_D1',{r1:cb+a6qi+1}))
e=S('A6Q_D1'); on('A6Q_D1',(net.eq(R1,40,e),'A6Q_D2',{a6qj:a6qi+2,a6qd:1}),(_aln(R1,e),'A6Q_D5',{a6qj:a6qi+1}),(None,'A6Q_S0',SKIP))
e=S('A6Q_D2'); on('A6Q_D2',(net.ge(a6qj,clen,e),'A6Q_S0',SKIP),(None,'A6Q_D3',{r1:cb+a6qj}))
e=S('A6Q_D3'); _op=net.eq(R1,40,e);_cl=net.eq(R1,41,e)
on('A6Q_D3',(_op,'A6Q_D2',{a6qd:a6qd+1,a6qj:a6qj+1}),(net.and_(_cl,net.eq(a6qd,1,e)),'A6Q_B0',{a6qkd:1,a6qdb:a6qi+2,a6qdl:a6qj-a6qi-2,a6qe:a6qj+1}),(_cl,'A6Q_D2',{a6qd:a6qd-1,a6qj:a6qj+1}),(None,'A6Q_D2',{a6qj:a6qj+1}))
e=S('A6Q_D5'); on('A6Q_D5',(net.ge(a6qj,clen,e),'A6Q_B0',{a6qkd:1,a6qdb:a6qi+1,a6qdl:a6qj-a6qi-1,a6qe:a6qj}),(None,'A6Q_D6',{r1:cb+a6qj}))
e=S('A6Q_D6'); on('A6Q_D6',(_aln(R1,e),'A6Q_D5',{a6qj:a6qj+1}),(None,'A6Q_B0',{a6qkd:1,a6qdb:a6qi+1,a6qdl:a6qj-a6qi-1,a6qe:a6qj}))
# the record
e=S('A6Q_B0'); _bad=net.or_(net.eq(a6qnl,0,e),net.gt(a6qnl,27,e),net.gt(a6qdl,27,e),net.ge(a6qn,690,e),net.and_(net.eq(a6qkd,1,e),net.eq(a6qdl,0,e)))
_rq=_qrec(a6qn)
on('A6Q_B0',(_bad,'A6Q_S0',SKIP),(None,'A6Q_B1',{rb:(cb+a6qnb,a6qnl)}))
on('A6Q_B1',(None,'A6Q_B2',{wb:(_rq+8,a6qnl)}))
on('A6Q_B2',(None,'A6Q_B3',{rb:(cb+a6qdb,a6qdl)}))
on('A6Q_B3',(None,'A6Q_B4',{wb:(_rq+36,a6qdl),w1:(_rq,a6qkd),w2:(_rq+2,a6qnl),w3:(_rq+3,a6qdl),a6qm:0,a6qw:0}))
def _qst(v,en,kind_bigger):
    lo=low0(v,en); lett=net.and_(net.ge(lo,97,en),net.lt(lo,123,en))
    return kind_bigger+128+lett*32
e=S('A6Q_B4'); on('A6Q_B4',(net.ge(a6qm,a6qnl,e),'A6Q_B6',{a6qnw:a6qw,a6qm:0,a6qw:0}),(None,'A6Q_B5',{r1:_rq+8+a6qm}))
e=S('A6Q_B5'); measure(e,R1,_qst(R1,e,G_(as_x(9),net.eq(a6qkd,1,e)))); on('A6Q_B5',(None,'A6Q_B4',{a6qw:a6qw+adv,a6qm:a6qm+1}))
e=S('A6Q_B6'); on('A6Q_B6',(net.ge(a6qm,a6qdl,e),'A6Q_B8',{a6qdw:a6qw}),(None,'A6Q_B7',{r1:_rq+36+a6qm}))
e=S('A6Q_B7'); measure(e,R1,_qst(R1,e,as_x(9))); on('A6Q_B7',(None,'A6Q_B6',{a6qw:a6qw+adv,a6qm:a6qm+1}))
e=S('A6Q_B8'); _wd=G_(net.max_(a6qnw,a6qdw)+6,net.eq(a6qkd,1,e))+G_(a6qnw+10,net.eq(a6qkd,2,e))
on('A6Q_B8',(None,'A6Q_B9',{w1:(_rq+1,_wd),w2:(_rq+4,a6qnw),w3:(_rq+5,a6qdw),co:a6qsr,r2:cb+1024+a6qsr,a6qj:a6qe-a6qsr}))
on('A6Q_B9',(None,'A6Q_Ba',{a6qst:R2}))
e=S('A6Q_Ba'); on('A6Q_Ba',(net.eq(a6qj,0,e),'INS',{ins_ch:as_x(EQC0)+a6qn,ins_st:a6qst,oret.r:oret.id('A6Q_Bb')}),(None,'DEL',{a6qj:a6qj-1,oret.r:oret.id('A6Q_Ba')}))
on('A6Q_Bb',(None,'A6Q_S0',{a6qn:a6qn+1,a6qi:a6qsr+1,a6qcv:a6qcv+1}))
fsm.set(co,net.and_(S('A6Q_RR'),net.or_(ONE-a6qa,net.step(a6qcv))),clen)
# layout: taller line, width from the record
e=S('A6Q_L0'); _lastq=net.ge(a6off+1,plen_,e); _fr=net.eq(R2,1,e); _aq=G_(as_x(18),_fr)+G_(as_x(17),e-_fr); _hq=G_(as_x(28),_fr)+G_(as_x(23),e-_fr)
_qcom={lasc:net.max_(_aq,lasc),lhh:net.max_(_hq,lhh),a6off:a6off+1}
on('A6Q_L0',(_lastq,'EM',{**_qcom,lend:a6off+1,lwid:lx+R1,lspc:lsn,llast:1}),(None,'L1',{**_qcom,lx:lx+R1,prevsp:0,kprev:0}))
# paint
A9Q=rom.metrics(9)[0]; A0Q=rom.metrics(0)[0]
def _qdraw(st,base,ln,y,bst,nx):
    n1=st+'g'
    e=S(st); on(st,(net.ge(a6qm,ln,e),nx,None),(None,n1,{r1:base+a6qm,a6qm:a6qm+1}))
    e=S(n1); g_=_qst(R1,e,bst)
    on(n1,(a6qs,st,{gly:(R1,g_,sx,y,0,1),sx:sx+adv}),(None,st,{gly:(R1,g_,sx,y,0,0),sx:sx+adv}))
on('A6Q_C0',(None,'A6Q_C1',{rl:_qrec(a6qk)}))
e=S('A6Q_C1'); RQ=rl.out; _fr=net.eq(RQ[0],1,e); _bar=sy+lasc-5; _base=sy+lasc
_col=tuple(G_(b_,ONE-a6qs)+a6qs*SEL[i_] for i_,b_ in enumerate((bc0,bc1,bc2)))
_qs={a6qkd:RQ[0],a6qwd:RQ[1],a6qnl:RQ[2],a6qdl:RQ[3],a6qnw:RQ[4],a6qdw:RQ[5],a6qm:0}
on('A6Q_C1',(_fr,'A6Q_FN',{**_qs,rA:(x,sy,RQ[1],lhh,_col,col),rB:(x+1,_bar,RQ[1]-2,1,(0,0,0),col),sx:x+(RQ[1]-RQ[4])*0.5}),
 (None,'A6Q_RN',{**_qs,rA:(x,sy,RQ[1],lhh,_col,col),rB:(x+1,_base-5,3,1,(0,0,0),col),rC:(x+4,_base-5,1,6,(0,0,0),col),rD:(x+5,_base-A0Q-1,1,A0Q+2,(0,0,0),col),sx:x+7}))
_qdraw('A6Q_FN',_qrec(a6qk)+8,a6qnl,_bar-1-A9Q,as_x(9),'A6Q_FD')
on('A6Q_FD',(None,'A6Q_Fd',{a6qm:0,sx:x+(a6qwd-a6qdw)*0.5}))
_qdraw('A6Q_Fd',_qrec(a6qk)+36,a6qdl,_bar+2,as_x(9),'A6Q_CE')
_qdraw('A6Q_RN',_qrec(a6qk)+8,a6qnl,_base-A0Q,as_x(0),'A6Q_RB')
on('A6Q_RB',(None,'A6Q_CE',{rB:(x+5,_base-A0Q-1,a6qwd-6,1,(0,0,0),col)}))
on('A6Q_CE',(None,'C0',{x:x+a6qwd,col:col+1,a6off:a6off+1}))
# docx: m:f and m:rad
def _qtext(st,base,ln,nx):
    e=S(st); on(st,(net.ge(a6qm,ln,e),nx,None),(None,st+'r',{r1:base+a6qm,a6qm:a6qm+1}))
    e=S(st+'r'); _a=net.eq(R1,38,e);_l=net.eq(R1,60,e);_g=net.eq(R1,62,e);_o=e-_a-_l-_g; em_en.lin(_o); em_b.add(_o,R1)
    on(st+'r',(_a,st+'a',None),(_l,st+'l',None),(_g,st+'k',None),(None,st,None))
    lit(st+'a',b'&amp;',st); lit(st+'l',b'&lt;',st); lit(st+'k',b'&gt;',st)
on('A6Q_X0',(None,'A6Q_X1',{rl:_qrec(a6qk)}))
e=S('A6Q_X1'); _qx={a6qnl:rl.out[2],a6qdl:rl.out[3],a6qm:0}
on('A6Q_X1',(net.eq(rl.out[0],1,e),'A6Q_Xf',_qx),(None,'A6Q_Xr',_qx))
lit('A6Q_Xf',b'<m:f><m:num><m:r><m:t xml:space="preserve">','A6Q_Xn'); _qtext('A6Q_Xn',_qrec(a6qk)+8,a6qnl,'A6Q_Xm')
lit('A6Q_Xm',b'</m:t></m:r></m:num><m:den><m:r><m:t xml:space="preserve">','A6Q_Xz'); on('A6Q_Xz',(None,'A6Q_Xd',{a6qm:0})); _qtext('A6Q_Xd',_qrec(a6qk)+36,a6qdl,'A6Q_Xe')
lit('A6Q_Xe',b'</m:t></m:r></m:den></m:f>','A6E_ER')
lit('A6Q_Xr',b'<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e><m:r><m:t xml:space="preserve">','A6Q_Xs'); _qtext('A6Q_Xs',_qrec(a6qk)+8,a6qnl,'A6Q_Xt')
lit('A6Q_Xt',b'</m:t></m:r></m:e></m:rad>','A6E_ER')
# PDF
on('A6Q_P0',(qop,'T4P_CL',{pfcr.r:pfcr.id('A6Q_P1')}),(None,'A6Q_P1',None))
on('A6Q_P1',(None,'A6Q_P2',{rl:_qrec(a6qk)}))
_qpx={a6qkd:rl.out[0],a6qwd:rl.out[1],a6qnl:rl.out[2],a6qdl:rl.out[3],a6qnw:rl.out[4],a6qdw:rl.out[5],a6qm:0}
on('A6Q_P2',(None,'A6Q_P3',_qpx))
def _prect(st,xv,yv,wv,hv,nx):
    number(st,xv,st+'a'); lit(st+'a',b' ',st+'b'); number(st+'b',yv,st+'c'); lit(st+'c',b' ',st+'d'); number(st+'d',wv,st+'e'); lit(st+'e',b' ',st+'f'); number(st+'f',hv,st+'g'); lit(st+'g',b' re f\n',nx)
def _ptext(st,xv,yv,sz,base,ln,nx):
    lit(st,b'BT /F6 '+str(sz).encode()+b' Tf 0 0 0 rg 1 0 0 1 ',st+'a'); number(st+'a',xv,st+'b'); lit(st+'b',b' ',st+'c'); number(st+'c',yv,st+'d'); lit(st+'d',b' Tm (',st+'e')
    e=S(st+'e'); on(st+'e',(net.ge(a6qm,ln,e),st+'z',None),(None,st+'f',{r1:base+a6qm,a6qm:a6qm+1}))
    e=S(st+'f'); _s=net.or_(net.eq(R1,40,e),net.eq(R1,41,e),net.eq(R1,92,e)); on(st+'f',(_s,st+'g',{qcur:R1}),(None,st+'h',{qcur:R1}))
    lit(st+'g',b'\\',st+'h'); e=S(st+'h'); em_en.lin(e); em_b.add(e,qcur); on(st+'h',(None,st+'e',None))
    lit(st+'z',b')Tj ET\n',nx)
lit('A6Q_P3',b'0 0 0 rg\n','A6Q_P4')
e=S('A6Q_P4'); on('A6Q_P4',(net.eq(a6qkd,1,e),'A6Q_Pb',None),(None,'A6Q_Pr',None))
_prect('A6Q_Pb',qxx+1,qyb+5,a6qwd-2,1,'A6Q_Pn')
_ptext('A6Q_Pn',qxx+(a6qwd-a6qnw)*0.5,qyb+7,12,_qrec(a6qk)+8,a6qnl,'A6Q_Pz')
on('A6Q_Pz',(None,'A6Q_Pd',{a6qm:0}))
_ptext('A6Q_Pd',qxx+(a6qwd-a6qdw)*0.5,net.relu(qyb+3-A9Q),12,_qrec(a6qk)+36,a6qdl,'A6Q_PE')
_prect('A6Q_Pr',qxx+1,qyb+5,3,1,'A6Q_Pr2'); _prect('A6Q_Pr2',qxx+4,net.relu(qyb-1),1,6,'A6Q_Pr3'); _prect('A6Q_Pr3',qxx+5,net.relu(qyb-1),1,A0Q+2,'A6Q_Pr4'); _prect('A6Q_Pr4',qxx+5,qyb+A0Q,a6qwd-6,1,'A6Q_Pr5')
_ptext('A6Q_Pr5',qxx+7,qyb,15,_qrec(a6qk)+8,a6qnl,'A6Q_PE')
on('A6Q_PE',(None,'PD_9',{qxx:qxx+a6qwd,qsty:999999,qop:0}))
