# ---- reviewer a4: commands missing against Word. Exec'd from app.py after the Tier 3 features ----
net.group('a4 commands')
import rv_a4_btn
# commands past the 8 bit id space: alpha 235 in the ribbon, command from the pointer
def _a4reg(b,e): return net.and_(net.eq(tab,b[0],e),net.ge(hx_,b[1],e),net.lt(hx_,b[1]+b[3],e),net.ge(hy_,b[2],e),net.lt(hy_,b[2]+b[4],e))
e=S('A4_X')
on('A4_X',*[(_a4reg(b_,e),b_[6],None) for b_ in rv_a4_btn.BTNS],(None,'HALT',None))
def a4_hover(e):
    "Hover key of a command that shares alpha 235."
    e2=net.and_(e,net.eq(A_,235,e),net.lt(hy_,150,e)); h_=X()
    for i_,b_ in enumerate(rv_a4_btn.BTNS): h_=h_+_a4reg(b_,e2)*(100*(i_+1))
    return h_
# clear formatting: list off, then the Normal record over the selection, or over the paragraph when there is no selection
on('A4_CF',(None,'PA0',{pwalk:lo_p,pfld:LIST,alv:0,t1_pdm:0,grp:grp+1,a4cfk:1,t1_lastk:0}))
on('A4_CF1',(has_sel,'A4_CF2',{rl:as_x(STY)}),(None,'T2_SA0',{t2si:0,a4cfq:1}))
on('A4_CF2',(None,'A4_CF3',None))
on('A4_CF3',(None,'W0',{fpre:W_[0],t2f[1]:W_[1],t2f[2]:W_[2],t2f[3]:W_[3],t2f[4]:W_[4],t2f[5]:W_[5],t2f[6]:W_[6],fm:8,t2si:0,t2lo:lo_p,t2hi:hi_p,t2um:0,a4wp_:lo_p,a4wo_:lo_o,wm:2,wfirst:1,wret.r:wret.id('FEND')}))
fsm.set(a4cfq,S('T2_SA2'),0)
# change case: a menu, then the range walker in mode 3. Without a selection the word at the caret is selected first.
on('A4_CM',(None,'T1_M0',{t1_mop:9,t1_mrow:99,t1_mtop:131,clip0:0,clip1:0}))
on('A4_CC',(has_sel,'W0',{a4wp_:lo_p,a4wo_:lo_o,wm:3,a4ws:1,a4ss:1,grp:grp+1,wret.r:wret.id('A4_CE')}),(None,'T1_W0',{a4cw:1}))
on('A4_CE',(None,'RD0',{lc:1}))
fsm.set(a4cw,S('RD0'),0)
# format painter: the first click takes the run format and paragraph record at the caret, mouse up applies them. A double click stays on.
e=S('A4_FP')
on('A4_FP',(net.and_(a4fp,net.eq(t1_clk,2,e)),'RD0',{a4fs:1}),(a4fp,'RD0',{a4fp:0,a4fs:0}),(has_sel,'A4_FPs',{r1:as_x(PT)+lo_p}),(None,'A4_FP1',{r1:cb+ALIGN,rp6:cb+PIND,a4fst:ty}))
on('A4_FPs',(None,'A4_FPt',{r2:R1+1024+lo_o}))
on('A4_FPt',(None,'A4_FP1',{a4fst:R2,r1:cb+ALIGN,rp6:cb+PIND}))
e=S('A4_FP1')
on('A4_FP1',(None,'RD0',{a4ff[1]:R1,a4ff[2]:rp6.out[0],a4ff[3]:rp6.out[1],a4ff[4]:rp6.out[2],a4ff[5]:rp6.out[3],a4ff[6]:rp6.out[4],a4fps:rp6.out[5],a4fpp:net.or_(e-net.and_(e,has_sel),net.gt(hi_p,lo_p,e)),a4fp:1,a4fs:0}))
_a4set={fpre:a4fst,t2f[1]:a4ff[1],t2f[2]:a4ff[2],t2f[3]:a4ff[3],t2f[4]:a4ff[4],t2f[5]:a4ff[5],t2f[6]:a4ff[6],t2si:a4fps,fm:8,t2lo:lo_p,t2hi:hi_p,t2um:0,a4fp:a4fs,t1_uid:1}
e=S('A4_FA0')
on('A4_FA0',(has_sel,'W0',{**_a4set,a4wp_:lo_p,a4wo_:lo_o,wm:2,wfirst:1,grp:grp+1,wret.r:wret.id('A4_FE')}),(net.eq(clen,0,e),'A4_FE',{**_a4set,grp:grp+1}),(None,'T1_W0',{a4cw:2}))
on('A4_FE',(a4fpp,'T2_SP0',{ap:cp,ao:co,lc:1,ty:fpre}),(None,'RD0',{lc:1,ty:fpre}))
# paragraph switches through the logged paragraph field pass
def a4_toggle(st,fld):
    on(st,(None,'A4_TG1',{r1:cb+fld,pfld:fld}))
a4_toggle('A4_TK',A4K);a4_toggle('A4_TL',A4L);a4_toggle('A4_TP',PBRK)
on('A4_TG1',(None,'PA0',{pwalk:lo_p,alv:ONE-net.step(R1),t1_pdm:0,grp:grp+1,t1_lastk:0}))
for v_ in (0,1,2,15): on(f'A4_BD{v_}',(None,'PA0',{pwalk:lo_p,pfld:A4B,alv:v_,t1_pdm:0,grp:grp+1,t1_lastk:0}))
for k_ in (0,2,5,13,14,15): on(f'A4_SH{k_}',(None,f'T3_C_S{k_}',{a4sha:1}))
fsm.set(a4sha,S('T3_END'),0)
# table insert from a grid of any size up to 8 by 8
on('A4_GO',(None,'T1_M0',{t1_mop:10,t1_mrow:99,t1_mtop:127,t1_mx:826,clip0:0,clip1:0}))
a4gr=R();a4gc=R();a4gv=R()
e=S('T1_MM10'); _b=net.bits(t1_mrow,7,e)
a4gh=[[R() for _ in range(8)] for _ in range(8)]; _gcv=_b[0]+_b[1]*2+_b[2]*4; _grv=_b[3]+_b[4]*2+_b[5]*4; _gok=net.lt(t1_mrow,64,e); _d10={}
for r_ in range(8):
    for c_ in range(8): _d10[a4gh[r_][c_]]=net.and_(_gok,net.ge(_grv,r_,e),net.ge(_gcv,c_,e))
on('T1_MM10',(None,'A4_GM',{**_d10,a4gc:_gcv,a4gr:_grv,a4gv:_gok}))
e=S('A4_GI'); _gh=net.decode(a4gr,8,e); _prod=X()
for r_ in range(8): _prod=_prod+G_((a4gc+1)*(r_+1),_gh[r_])
on('A4_GI',(None,'TI0',{tin:a4gc+1,tic:0,tir:_prod-1,grp:grp+1}))
def a4_mrules(mc,CM,e):
    _b=net.bits(t1_mrow,7,e)
    return [(mc(9,r_),'A4_CC',{a4cm:r_,**CM}) for r_ in range(5)]+[(net.and_(net.eq(t1_mop,10,e),net.lt(t1_mrow,64,e)),'A4_GI',{a4gc:_b[0]+_b[1]*2+_b[2]*4,a4gr:_b[3]+_b[4]*2+_b[5]*4,**CM})]
def a4_late():
    t1_menu(9,112,131,170,['Sentence case','lowercase','UPPERCASE','Capitalize Each Word','tOGGLE cASE'])
    x_,y_=826,127; u=ui.L()
    u.r(x_+2,y_+2,GC*8+1,GC*8+23,(200,198,196),0); u.r(x_-1,y_-1,GC*8+2,GC*8+22,(150,148,146),0); u.r(x_,y_,GC*8,GC*8+20,WHITE,0)
    for r_ in range(8):
        for c_ in range(8):
            cx_=x_+c_*GC; cy_=y_+r_*GC
            u.r(cx_,cy_,GC,GC,WHITE,254); u.r(cx_+2,cy_+2,GC-4,GC-4,(150,150,150),254); u.r(cx_+3,cy_+3,GC-6,GC-6,WHITE,254)
            u.k(a4gh[r_][c_],cx_+3,cy_+3,GC-6,GC-6,PAL_B[5],254)
    t1_chain('A4_GM',u,'A4_GL')
    on('A4_GL',(a4gv,'A4_GL1',{gly:(49+a4gc,9,x_+8,y_+GC*8+1,0,0)}),(None,'T1_END',None))
    on('A4_GL1',(None,'A4_GL2',{gly:(120,9,x_+19,y_+GC*8+1,0,0)}))
    on('A4_GL2',(None,'T1_END',{gly:(49+a4gr,9,x_+29,y_+GC*8+1,0,0)}))
# ---- keep with next and keep lines: sum the heights the paragraph must share a page with, before its first line ----
net.group('a4 keep')
a4kq=R();a4kh=R();a4kb=R();a4kn=R();a4kj=R();a4kl=R();a4kc=R();a4ks=R()
on('A4_K0',(None,'A4_K1',{a4kq:pi,a4kh:0,a4kn:0}))
on('A4_K1',(None,'A4_K2',{r1:as_x(PT)+a4kq}))
on('A4_K2',(None,'A4_K3',{a4kb:R1,r2:R1+DIRTY,rc:R1+2062,rmeta:R1+META,ra4:R1+A4C,rp6:R1+PIND,rl:R1+LEN}))
e=S('A4_K3'); _nxt=net.gt(a4kq,pi,e); _kn=net.or_(net.step(A4O[2]),net.and_(net.ge(rp6.out[5],2,e),net.lt(rp6.out[5],5,e)))
_kself=net.and_(ONE-_nxt,a4k)
_secs=net.and_(_nxt,net.step(MT[3]),net.step(net.step(MT[3]-1-cursec-0.5)+net.step(cursec-MT[3]+1-0.5)))
_cont=net.and_(net.or_(_kn,net.and_(ONE-_nxt,a4k)),net.or_(net.and_(ONE-_nxt,a4k),ONE-_nxt,_nxt))
_lim=G_(net.min_(rl.out[4],as_x(2)),net.and_(_nxt,ONE-_kn))+G_(rl.out[4],e-net.and_(_nxt,ONE-_kn))
on('A4_K3',(_secs,'A4_K9',None),(net.and_(_nxt,net.step(R2)),'R2',{pi:a4kq,a4kp:pi,a4la:1,r1:as_x(PT)+a4kq}),
 (None,'A4_K4',{a4kh:a4kh+G_(rp6.out[3],_nxt),a4kj:0,a4kl:_lim,a4kc:net.and_(_kn,e-net.and_(net.step(rc.out[0]),_nxt)),a4ks:rp6.out[4]}))
e=S('A4_K4'); on('A4_K4',(net.ge(a4kj,a4kl,e),'A4_K6',None),(None,'A4_K5',{r2:a4kb+LINES+a4kj*8+3}))
on('A4_K5',(None,'A4_K4',{a4kh:a4kh+R2,a4kj:a4kj+1}))
e=S('A4_K6'); on('A4_K6',(net.and_(a4kc,net.lt(a4kq+1,npar,e),net.lt(a4kn,8,e)),'A4_K1',{a4kq:a4kq+1,a4kn:a4kn+1,a4kh:a4kh+a4ks}),(None,'A4_K9',None))
e=S('A4_K9'); on('A4_K9',(None,'R3B',{a4kd:pi+1,a4kbr:net.and_(net.lt(a4kh,s_th,e),net.gt(yy+a4kh,ptop+s_mt+s_th,e))}))
fsm.set(a4kd,S('RD0'),0); fsm.set(a4kbr,S('R4'),0)
on('A4_KL',(None,'R2',{pi:a4kp,a4la:0,r1:as_x(PT)+a4kp}))
# ---- paragraph shading and borders ----
net.group('a4 borders')
a4nq=R();a4nb=R();a4ns=R();a4ny=R();a4dt=R();a4db=R();a4gap=R();a4nr=t3ret('A4_NBR')
e=S('A4_R5'); _dec=net.and_(e,ONE-net.step(tcols),net.or_(net.step(pbg),net.step(a4b)))
on('A4_R5',(_dec,'A4_NB0',{a4nq:pi,a4nb:a4b,a4ns:pbg,a4ny:yy,a4nr.r:a4nr.id('R5')}),(None,'R5',None))
e=S('A4_NB0'); on('A4_NB0',(net.step(a4nq),'A4_NB1',{r1:as_x(PT)+a4nq-1}),(None,'A4_NB4',{a4dt:1,a4gap:0}))
on('A4_NB1',(None,'A4_NB2',{ra4:R1+A4C,rmeta:R1+META,r2:R1+ENDY}))
e=S('A4_NB2'); _same=net.and_(net.eq(A4O[4],a4nb,e),net.eq(MT[2],a4ns,e))
on('A4_NB2',(None,'A4_NB4',{a4dt:e-_same,a4gap:G_(net.relu(a4ny-R2),_same)}))
e=S('A4_NB4'); on('A4_NB4',(net.lt(a4nq+1,npar,e),'A4_NB5',{r1:as_x(PT)+a4nq+1}),(None,'A4_NBR',{a4db:1}))
on('A4_NB5',(None,'A4_NB6',{ra4:R1+A4C,rmeta:R1+META}))
e=S('A4_NB6'); on('A4_NB6',(None,'A4_NBR',{a4db:e-net.and_(net.eq(A4O[4],a4nb,e),net.eq(MT[2],a4ns,e))}))
e=S('A4_D0'); _hang=net.relu(as_x(0)-pf_val(pfirst_))
def _bx(e): return s_tx+xcol+pind+net.relu(indb-26)-net.relu(as_x(0)-pf_val(pfirst_))-4,s_tx+xcol+rw-a4rr+4
bx0,bx1=_bx(e); _bc=(bc0,bc1,bc2)
_gc=net.and_(e,net.eq(lj,0,e),ONE-a4dt,net.step(a4gap),net.lt(a4gap,100,e))
rC.drive(_gc,(bx0,sy-a4gap,bx1-bx0,a4gap,_bc,0))
on('A4_D0',(None,'A4_D1',{rA:(lleft,sy,net.relu(bx0-lleft),lhh,WHITE,1),rB:(bx1,sy,net.relu(lright-bx1),lhh,WHITE,net.min_(col,199))}))
e=S('A4_D1'); bx0,bx1=_bx(e); _bb=net.bits(a4b,4,e); _j0=net.eq(lj,0,e); _jl=net.ge(lj+1,nl,e); KC=(0,0,0)
_gs=G_(a4gap,net.and_(_j0,ONE-a4dt,net.lt(a4gap,100,e)))
rA.drive(_bb[2],(bx0,sy-_gs,1,lhh+_gs,KC,0)); rB.drive(_bb[3],(bx1-1,sy-_gs,1,lhh+_gs,KC,0))
rC.drive(net.and_(_bb[0],_j0,a4dt),(bx0,sy-1,bx1-bx0,1,KC,0)); rD.drive(net.and_(_bb[1],_jl,a4db),(bx0,sy+lhh,bx1-bx0,1,KC,0))
on('A4_D1',(None,'R5',{yy:yy+lhh,lj:lj+1}))
# PDF: the same rectangles, one line at a time
qa4b=R();qa4s=R();qa4r=R();qa4p=R();qa4f=R()
fsm.set(qa4p,S('PD_3'),rp6.out[0]); fsm.set(qa4f,S('PD_3'),rp6.out[1])
e=S('A4_Q0'); _nt=e-net.and_(e,net.step(qcols)); _qd=net.and_(_nt,net.or_(net.step(MT[2]),net.step(A4O[4])))
on('A4_Q0',(_qd,'A4_NB0',{qa4b:A4O[4],qa4s:G_(MT[2],_nt),qa4r:A4O[6],a4nq:qp,a4nb:A4O[4],a4ns:MT[2],a4ny:qyy,a4nr.r:a4nr.id('A4_Q1')}),(None,'A4_Q1',{qa4b:0,qa4s:0,qa4r:A4O[6]}))
on('A4_Q1',(None,'PD_5',{r1:qb+NLINES}))
e=S('A4_QL'); on('A4_QL',(net.or_(net.step(qa4s),net.step(qa4b)),'A4_QS',None),(None,'T2_PM',None))
e=S('A4_QS'); _hq=net.decode(qa4s,len(PAL_B),e)
on('A4_QS',*[(_hq[i_],f'A4_Qc{i_}',None) for i_ in range(1,len(PAL_B))],(None,'A4_QG',None))
for i_,c_ in enumerate(PAL_B):
    if i_: lit(f'A4_Qc{i_}',('%.3f %.3f %.3f rg '%tuple(v_/255 for v_ in c_)).encode(),'A4_QF')
def _qx(e): return qml+qxc+qa4p+net.relu(qind-26)-net.relu(as_x(0)-pf_val(qa4f))-4
def _qw(e):
    tw_=G_(floorv((qtw-24)*0.5,e),net.eq(qnc,2,e))+G_(qtw,e-net.eq(qnc,2,e))
    return tw_-qa4r-qa4p-net.relu(qind-26)+net.relu(as_x(0)-pf_val(qa4f))+8
def _qrect(st,xf,y,wf,h,nx):
    e=S(st); number(st,xf(e),st+'a'); lit(st+'a',b' ',st+'b'); e=S(st+'b'); number(st+'b',y,st+'c'); lit(st+'c',b' ',st+'d')
    e=S(st+'d'); number(st+'d',wf(e),st+'e'); lit(st+'e',b' ',st+'f'); number(st+'f',h,st+'g'); lit(st+'g',b' re f\n',nx)
_qy=qph-(qyy-qtop+qh)
_qrect('A4_QF',_qx,_qy,_qw,qh,'A4_QFx')
e=S('A4_QFx'); on('A4_QFx',(net.and_(net.eq(qlj,0,e),ONE-a4dt,net.step(a4gap),net.lt(a4gap,100,e)),'A4_QH',None),(None,'A4_QG',None))
_qrect('A4_QH',_qx,_qy+qh,_qw,a4gap,'A4_QG')
lit('A4_QG',b'0 0 0 rg\n','A4_QB0')
e=S('A4_QB0'); _qb=net.bits(qa4b,4,e)
a4qb=[R() for _ in range(4)]
on('A4_QB0',(None,'A4_QB1',{a4qb[0]:_qb[0],a4qb[1]:_qb[1],a4qb[2]:_qb[2],a4qb[3]:_qb[3]}))
e=S('A4_QB1'); on('A4_QB1',(a4qb[2],'A4_QL0',None),(None,'A4_QB2',None))
_qrect('A4_QL0',_qx,_qy,lambda e:as_x(1),qh,'A4_QB2')
e=S('A4_QB2'); on('A4_QB2',(a4qb[3],'A4_QR0',None),(None,'A4_QB3',None))
_qrect('A4_QR0',lambda e:_qx(e)+_qw(e)-1,_qy,lambda e:as_x(1),qh,'A4_QB3')
e=S('A4_QB3'); on('A4_QB3',(net.and_(a4qb[0],net.eq(qlj,0,e),a4dt),'A4_QT0',None),(None,'A4_QB4',None))
_qrect('A4_QT0',_qx,_qy+qh,_qw,1,'A4_QB4')
e=S('A4_QB4'); on('A4_QB4',(net.and_(a4qb[1],net.ge(qlj+1,qnl,e),a4db),'A4_QU0',None),(None,'T2_PM',None))
_qrect('A4_QU0',_qx,_qy,_qw,1,'T2_PM')
# ---- .docx writer: pPr children ----
net.group('a4 docx')
lit('A4_WK',b'<w:keepNext/>','A4_W2'); lit('A4_WL',b'<w:keepLines/>','A4_W3')
on('A4_W2',(a4wl,'A4_WL',None),(None,'A4_W3',None))
on('A4_W3',(pbk,'T2W3',None),(None,'T2W4',None))
e=S('A4_W0'); _wb=net.bits(a4wb,4,e)
a4wq=[R() for _ in range(4)]
on('A4_W0',(net.step(a4wb),'A4_Wb',{a4wq[0]:_wb[0],a4wq[1]:_wb[1],a4wq[2]:_wb[2],a4wq[3]:_wb[3]}),(None,'A4_Ws',None))
lit('A4_Wb',b'<w:pBdr>','A4_Wb0')
cur_='A4_Wb0'
for i_,(tg_,q_) in enumerate(((b'top',0),(b'left',2),(b'bottom',1),(b'right',3))):
    nx_=f'A4_Wb{i_+1}'
    on(cur_,(a4wq[q_],cur_+'L',None),(None,nx_,None)); lit(cur_+'L',b'<w:%s w:val="single" w:sz="4" w:space="1" w:color="auto"/>'%tg_,nx_); cur_=nx_
lit(cur_,b'</w:pBdr>','A4_Ws')
e=S('A4_Ws'); _hs=net.decode(G_(ssh,net.eq(scols,0,e)),len(PAL_B),e)
on('A4_Ws',*[(_hs[i_],f'A4_Wc{i_}',None) for i_ in range(1,len(PAL_B))],(None,'A4_Wt',None))
for i_,c_ in enumerate(PAL_B):
    if i_: lit(f'A4_Wc{i_}',b'<w:shd w:val="clear" w:color="auto" w:fill="%02X%02X%02X"/>'%c_,'A4_Wt')
e=S('A4_Wt'); _any=net.or_(*[net.step(a4wt[i_]) for i_ in range(4)])
e=S('A4_Wt'); _any=net.or_(*[net.step(a4wt[i_]) for i_ in range(4)])
on('A4_Wt',(_any,'A4_WT',None),(None,'T3_TA0',None))
lit('A4_WT',b'<w:tabs>','A4_WT0')
for i_ in range(4):
    st_=f'A4_WT{i_}'; nx_=f'A4_WT{i_+1}'; e=S(st_)
    on(st_,(net.step(a4wt[i_]),st_+'a',None),(None,nx_,None))
    e=S(st_+'a'); kd_=net.ge(a4wt[i_],4096,e)+net.ge(a4wt[i_],8192,e)
    on(st_+'a',(net.eq(kd_,1,e),st_+'c',None),(net.eq(kd_,2,e),st_+'r',None),(None,st_+'l',None))
    for c_,w_ in (('l',b'left'),('c',b'center'),('r',b'right')): lit(st_+c_,b'<w:tab w:val="'+w_+b'" w:pos="',st_+'n')
    e=S(st_+'n'); kd_=net.ge(a4wt[i_],4096,e)+net.ge(a4wt[i_],8192,e); numz(st_+'n',(a4wt[i_]-kd_*4096)*15,st_+'z'); lit(st_+'z',b'"/>',nx_)
lit('A4_WT4',b'</w:tabs>','T3_TA0')
# ---- .docx reader ----
on('A4_RK0',(None,'A4_RK1',{rl:OA+oi}))
e=S('A4_RK1'); on('A4_RK1',(net.eq(W[0],47,e),'PX',{w1:(cb+a4rk,1)}),(None,'A4_RK2',{rl:OA+oi+8}))
e=S('A4_RK2'); on('A4_RK2',(net.or_(net.eq(W[0],48,e),net.eq(W[0],102,e)),'PX',{w1:(cb+a4rk,0)}),(None,'PX',{w1:(cb+a4rk,1)}))
on('A4_RB0',(None,'T2_VF',{t2rr.r:t2rr.id('A4_RB1')}))
on('A4_RB1',(None,'A4_RB2',{rl:OA+oi,r1:cb+A4B}))
e=S('A4_RB2'); on('A4_RB2',(net.or_(pat('none',e),pat('nil',e)),'PX',None),(None,'PX',{w1:(cb+A4B,R1+a4rbb)}))
# a tab stop definition: read kind and position, then let the leader rule look at the same tag
on('A4_RS0',(None,'T2_VF',{t2rr.r:t2rr.id('A4_RS1')}))
on('A4_RS1',(None,'A4_RS2',{rl:OA+oi}))
e=S('A4_RS2'); _rsk=net.eq(W[0],99,e)*net.eq(W[1],101,e)*1 if False else None
on('A4_RS2',(net.and_(net.eq(W[0],99,e),net.eq(W[1],108,e)),'T3_RT1',{oi:a4roi}),(None,'A4_RS3',{a4rsk:net.and_(net.eq(W[0],99,e),net.eq(W[1],101,e))+net.or_(net.eq(W[0],114,e),net.eq(W[0],101,e))*2}))
on('A4_RS3',(None,'A4_RS4',{rl:OA+oi}))
e=S('A4_RS4'); on('A4_RS4',(net.eq(W[0],62,e),'T3_RT1',{oi:a4roi}),(pat('w:pos="',e),'T2_NM',{oi:oi+6,t2n_:0,t2rr.r:t2rr.id('A4_RS5')}),(None,'A4_RS3',{oi:oi+1}))
on('A4_RS5',(None,'T2_DV',{t2q:0,t2sr.r:t2sr.id('A4_RS6')}))
e=S('A4_RS6'); _ok=net.lt(a4rsn,4,e); w1.drive(_ok,(cb+A4T+a4rsn,t2q+a4rsk*4096))
on('A4_RS6',(None,'T3_RT1',{oi:a4roi,a4rsn:a4rsn+_ok}))
# ---- real tabs: the layout network finds each tab's width and keeps (offset, width) pairs in the paragraph; paint and PDF look them up ----
net.group('a4 tabs')
A4TW=2025; A4TN=11
a4tn=R();a4ts=R();a4tk_=R();a4tw=R();a4tc=R();a4ti=R();a4tq=R();a4tb=R();a4trel=R()
e=S('A4_LT0'); a4trel_=lx+pind+pf_val(lfi)+indb; _kd=[net.ge(A4TO[i_],4096,e)+net.ge(A4TO[i_],8192,e) for i_ in range(4)]; _p=[A4TO[i_]-_kd[i_]*4096 for i_ in range(4)]
_gt=[net.gt(_p[i_],a4trel_,e) for i_ in range(4)]; _c=[G_(_p[i_],_gt[i_])+(e-_gt[i_])*60000 for i_ in range(4)]
_gi=net.gt(pind,a4trel_,e); _mn=net.min_(net.min_(net.min_(_c[0],_c[1]),net.min_(_c[2],_c[3])),G_(pind,_gi)+(e-_gi)*60000)
_rv=net.gate(a4trel_,e); _k=X()
for i_ in range(1,27): _k=_k+net.step(_rv-48*i_+0.001)
_hc=net.lt(_mn,60000,e)
_kk=X()
for i_ in range(4): _kk=_kk+G_(_kd[i_],net.eq(_c[i_],_mn,e))
on('A4_LT0',(None,'A4_LT1',{a4ts:G_(_mn,_hc)+G_((_k+1)*48,e-_hc),a4tk_:G_(_kk,_hc),a4trel:a4trel_,a4tc:0,a4tq:off_+1}))
e=S('A4_LT1'); on('A4_LT1',(net.step(a4tk_),'A4_LM0',None),(None,'A4_LT2',{a4tw:net.relu(a4ts-a4trel)}))
e=S('A4_LM0'); on('A4_LM0',(net.ge(a4tq,plen_,e),'A4_LMz',None),(None,'A4_LM1',{r1:pbs+a4tq,r2:pbs+1024+a4tq}))
e=S('A4_LM1'); _tab=net.eq(R1,9,e); _c1=e-_tab; measure(_c1,R1,R2)
on('A4_LM1',(_tab,'A4_LMz',None),(None,'A4_LM0',{a4tc:a4tc+adv,a4tq:a4tq+1}))
e=S('A4_LMz'); on('A4_LMz',(net.eq(a4tk_,2,e),'A4_LT2',{a4tw:net.relu(a4ts-a4trel-a4tc)}),(None,'A4_LT2',{a4tw:net.relu(a4ts-a4trel-a4tc*0.5)}))
e=S('A4_LT2'); _w=net.min_(a4tw,net.relu(ww-lx)); _ok=net.lt(a4tn,A4TN,e)
w1.drive(_ok,(pbs+A4TW+a4tn*2,off_)); w2.drive(_ok,(pbs+A4TW+a4tn*2+1,_w))
_adv={a4tn:a4tn+_ok,a4lt:1,kprev:0,lx:lx+_w,off_:off_+1,prevsp:1,a4_lb:off_+1,lbx:lx+_w,lspb:lsn,lfnb:lfn,lfhb:lfh}
on('A4_LT2',(net.ge(off_+1,plen_,e),'EM',{**_adv,lend:off_+1,lwid:lx+_w,lspc:lsn,llast:1}),(None,'L1',_adv))
fsm.set(a4tn,S('LAY0'),0); fsm.set(a4lt,S('LAY0'),0); fsm.set(a4lt,S('EM'),0)
# lookup used by paint and PDF
a4lr=t3ret('A4_LUR');a4lk=R();a4lb=R()
e=S('A4_LU0'); on('A4_LU0',(net.ge(a4ti,A4TN,e),'A4_LUR',{a4tw:48}),(None,'A4_LU1',{r1:a4lb+A4TW+a4ti*2,r2:a4lb+A4TW+a4ti*2+1}))
e=S('A4_LU1'); on('A4_LU1',(net.eq(R1,a4lk,e),'A4_LUR',{a4tw:R2}),(None,'A4_LU0',{a4ti:a4ti+1}))
on('A4_PT0',(None,'A4_LU0',{a4ti:0,a4lk:off_,a4lb:pbs,a4lr.r:a4lr.id('A4_PT3')}))
e=S('A4_PT3'); _kp=pi*2048+off_; _is=net.and_(net.ge(_kp,Lo,e),net.lt(_kp,Hi,e)); _ns=e-_is
_col=tuple(_is*SEL[i_]+G_((bc0,bc1,bc2)[i_],_ns) for i_ in range(3))
_mk=net.and_(e,t1_marks); rC.drive(_mk,(a4_x+1,sy+lasc-6,net.relu(a4tw-2),1,(120,120,160),col))
on('A4_PT3',(None,'C0',{rA:(a4_x,sy,a4tw*0.5+1,lhh,_col,col),rB:(a4_x+a4tw*0.5,sy,a4tw*0.5+1,lhh,_col,col+1),a4_x:a4_x+a4tw,col:col+1,off_:off_+1,kprev:0}))
on('A4_QX0',(None,'A4_LU0',{a4ti:0,a4lk:qo,a4lb:qb,a4lr.r:a4lr.id('A4_QX1')}))
on('A4_QX1',(None,'PD_9',{qxx:qxx+a4tw,qo:qo+1,qpc:0}))
e=S('A4_SF0'); on('A4_SF0',(net.eq(t2psv,99999,e),'A4_SF2',None),(None,'T4_SC',{t4cr.r:t4cr.id('A4_SF2')}))
lit('A4_SF2',b'<w:r><w:tab/></w:r>','A4_SF3'); on('A4_SF3',(None,'SVC',{t2psv:99999,off_:off_+1}))
# ---- the ruler: first line, left and right indent markers, margins, tab stops ----
net.group('a4 ruler')
a4tkind=R();a4so=R();a4sk=R();a4dm=R()
on('A4_RM0',(None,'A4_RM1',{ra4t:cb+A4T,ra4:cb+A4C,rp6:cb+PIND,rc:cb+2062}))
e=S('A4_RM1')
def _near(v,e): return net.and_(net.lt(hx_,as_x(v)+6,e),net.gt(hx_,as_x(v)-6,e))
_Lx=t1_rL+t1_rI; _Fx=_Lx+pf_val(rp6.out[1]); _Rx=t1_rL+t1_rW-A4O[6]; _top=net.lt(hy_,157,e); _low=net.ge(hy_,166,e); _mid=e-_top-_low; _notb=e-net.step(rc.out[0])
_kd=[net.ge(A4TO[i_],4096,e)+net.ge(A4TO[i_],8192,e) for i_ in range(4)]; _p=[A4TO[i_]-_kd[i_]*4096 for i_ in range(4)]
_st=[net.and_(net.step(A4TO[i_]),_near(t1_rL+_p[i_],e),e-_top) for i_ in range(4)]
_drag=lambda k_:{tdk:k_,tdx:hx_,tmx:hx_,drag:0}
_srules=[(_st[i_],'A4_RMd',{**_drag(40+i_),a4so:_p[i_],a4sk:_kd[i_]}) for i_ in range(4)]
_inw=net.and_(net.gt(hx_,t1_rL,e),net.lt(hx_,t1_rL+t1_rW,e))
_empty=X(); _e0=e-net.step(A4TO[0]); _e1=net.and_(e-_e0,ONE-net.step(A4TO[1])); _e2=net.and_(e-_e0-_e1,ONE-net.step(A4TO[2]))
_slot=_e1*1+_e2*2+(e-_e0-_e1-_e2)*3
on('A4_RM1',(net.and_(net.ge(hx_,200,e),net.lt(hx_,222,e)),'RD0',{a4tkind:G_(a4tkind+1,net.lt(a4tkind,2,e)),t1_rv:0}),
 (net.and_(_top,_near(_Fx,e)),'A4_RMd',_drag(30)),(net.and_(_low,_near(_Rx,e)),'A4_RMd',_drag(32)),(net.and_(_low,_near(_Lx,e)),'A4_RMd',_drag(31)),*_srules,
 (net.and_(_mid,_notb,_near(t1_rL,e)),'A4_RMd',_drag(33)),(net.and_(_mid,_notb,_near(t1_rL+t1_rW,e)),'A4_RMd',_drag(34)),
 (_inw,'PA0',{pwalk:lo_p,pfld:G_(as_x(A4T)+_slot,e),alv:floorv((hx_-t1_rL)*(1.0/6)+0.5,e)*6+a4tkind*4096,t1_pdm:0,grp:grp+1,t1_lastk:0,t1_rv:0}),(None,'HALT',None))
on('A4_RMd',(None,'HALT',None))
e=S('A4_RU'); _d=floorv((eva-tdx+1200)*(1.0/6)+0.5,e)*6-200
_kh=net.decode(net.relu(tdk-30),15,e); _off=net.or_(net.lt(evb,130,e),net.ge(evb,190,e))
_u={tdk:0,a4dl:_d,t1_rv:0}
_tr=[(_kh[10+i_],'A4_RUt',{**_u,pfld:as_x(A4T)+i_,a4tb:net.gt(evb,130,e)-net.ge(evb,190,e)}) for i_ in range(4)]
on('A4_RU',(_kh[0],'T2_PD',{**_u,pfld:PFIRST,t2d:_d,t2mn:1}),(_kh[1],'T2_PD',{**_u,pfld:PIND,t2d:_d,t2mn:0,a4rc:1}),(_kh[2],'T2_PD',{**_u,pfld:A4R,t2d:as_x(2000)-_d,t2mn:0}),
 (_kh[3],'T3_SP0',{**_u,tsop:9}),(_kh[4],'T3_SP0',{**_u,tsop:10}),*_tr,(None,'RD0',_u))
e=S('A4_RUt'); on('A4_RUt',(None,'PA0',{pwalk:lo_p,alv:G_(net.relu(a4so+a4dl-1000)+a4sk*4096,a4tb),t1_pdm:0,grp:grp+1,t1_lastk:0}))
e=S('RE1'); rD.drive(net.and_(e,net.ge(tdk,30,e)),(tmx,DOCY,1,VH,(43,87,154),0))
# ruler marks for tab stops and the stop kind selector
rkc=(60,60,60)
for i_ in range(4):
    pass
def _sm(i_,e):
    v_=a4m[i_]; k1=net.and_(net.ge(v_,4096,e),net.lt(v_,8192,e)); k2=net.ge(v_,8192,e); return v_-k1*4096-k2*8192,k1,k2
for s_,(ia,ib) in enumerate(((0,1),(2,3))):
    st_=f'A4_RZ{s_}'; e=S(st_); pa_,ka,kb=_sm(ia,e); pb_2,kc_,kd_=_sm(ib,e)
    ca=net.and_(e,net.step(a4m[ia])); cb_=net.and_(e,net.step(a4m[ib]))
    rA.drive(ca,(t1_rL+pa_,160,2,8,rkc,0)); rB.drive(ca,(t1_rL+pa_-kb*5-ka*3,166,6,2,rkc,0)); rC.drive(cb_,(t1_rL+pb_2,160,2,8,rkc,0)); rD.drive(cb_,(t1_rL+pb_2-kd_*5-kc_*3,166,6,2,rkc,0))
    on(st_,(None,f'A4_RZ{s_+1}',None))
e=S('A4_RZ2'); hk_=net.decode(a4tkind,3,e)
on('A4_RZ2',(None,'A4_RZ3',{rA:(200,153,20,18,(255,255,255),0),rB:(200,153,20,1,(150,150,150),0),rC:(200,170,20,1,(150,150,150),0)}))
e=S('A4_RZ3'); hk_=net.decode(a4tkind,3,e)
on('A4_RZ3',(None,'T1_V0',{gly:(hk_[0]*76+hk_[1]*67+hk_[2]*82,9,206,154,0,0)}))
# section records are logged, so margin, size and column changes undo
cur_='A4_SL'
for i_,v_ in enumerate(SWV):
    nx_=f'A4_SLa{i_}'; nn_=f'A4_SLb{i_}'
    on(cur_,(None,nx_,{r1:as_x(SECB)+sv_i*8+i_}))
    e=S(nx_); log(e,7,as_x(SECB)+sv_i*8+i_,0,R1,net.relu(v_))
    on(nx_,(None,nn_,None)); cur_=nn_
on(cur_,(None,'T3_SW',{swret.r:swret.id('T3_SP4')}))
e=S('U2'); fsm.set(a4da,net.and_(e,net.eq(uop,7,e),net.lt(up,as_x(SECB)+400,e),net.ge(up,SECB,e)),1)
e=S('V2'); fsm.set(a4da,net.and_(e,net.eq(uop,7,e),net.lt(up,as_x(SECB)+400,e),net.ge(up,SECB,e)),1)
on('A4_UD',(None,'DA0',{ap:cp,ao:co,di_:0,a4da:0}))
