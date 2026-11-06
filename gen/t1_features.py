# Tier 1 features. Sections are exec'd inside app.py's global scope at hook points.
#@@ regs
GC=22;RH=22                                   # menu row height
t1_hov=R();t1_hb=R();t1_hvo=R();t1_nh=R();t1_mop=R();t1_mrow=R(99);t1_mtop=R();t1_uid=R();t1_mx=R()
t1_tdrag=R();t1_grab=R();t1_thh=R();t1_clk=R();t1_lx=R();t1_ly=R();t1_lt=R();t1_s=R();t1_e=R();t1_c=R()
t1_lastk=R();t1_kt=R();t1_pz=R();t1_case=R();t1_fw=R();t1_ruler=R(1);t1_marks=R();t1_pb=R();t1_pdm=R();t1_pdd=R();t1_tmp=R()
t1_rv=R();t1_rL=R();t1_rW=R();t1_rI=R();t1_cr=R()
t1_cntp=R();t1_cw=R();t1_co_=R();t1_cn=R();t1_ci=R();t1_cb=R();t1_cB=R();t1_cl=R();t1_ck=R()
t1_mopb=net.step(t1_mop)
CSTART={t1_cntp:1,t1_cw:0,t1_co_:0,t1_cn:0,t1_ci:0}
def t1_isw(v,en):
    "A word character: letter, digit, underscore or apostrophe."
    return net.or_(net.and_(net.ge(v,192,en),ONE-net.eq(v,215,en),ONE-net.eq(v,247,en)),net.and_(net.ge(v,65,en),net.lt(v,91,en)),net.and_(net.ge(v,97,en),net.lt(v,123,en)),net.and_(net.ge(v,48,en),net.lt(v,58,en)),net.eq(v,95,en),net.eq(v,39,en))
def t1_text(start,txt,x0,y,f,b,nxt,st=9):
    "A display list of glyphs at fixed pens."
    xx=x0;si=st&15;u=ui.L()
    for ch in txt:
        u.i.append(('g',ord(ch),st,xx,y,f,b,False)); xx+=rom.adv_px(0,(st>>4)&1,0,si,ord(ch))
    net.rec(S(nxt),ui.emit(net,fsm,rA,None,YB,u.i,start,t1_mrow,t1_hb,bg))
#@@ keys
# undo grouping inputs: a pause or any navigation or command key starts a new group
fsm.set(t1_pz,en,t1_pzn); fsm.set(t1_kt,en,evc)
t1_nav=X()
for c_ in range(128,136): t1_nav=t1_nav+N(c_)
fsm.set(t1_lastk,net.step(t1_nav+net.and_(en,ctrl)),0)
#@@ md
e=S('MD'); adx=net.relu(eva-t1_lx)+net.relu(t1_lx-eva); ady=net.relu(evb-t1_ly)+net.relu(t1_ly-evb)
t1_rep=net.and_(net.lt(adx,5,e),net.lt(ady,5,e),net.lt(evc,t1_lt+500,e))
t1_clkn=as_x(0)+e+net.and_(t1_rep,net.eq(t1_clk,1,e))*1+net.and_(t1_rep,net.eq(t1_clk,2,e))*2
T1_CLICK={shiftk:net.bits(evm,4,e)[1],t1_clk:t1_clkn,t1_lx:eva,t1_ly:evb,t1_lt:evc}
# double click: extend to the run of same class characters, then over trailing spaces
def t1_cls(v,en):
    sp_=net.eq(v,32,en); w_=t1_isw(v,en); return w_+(en-w_-sp_)*2
e=S('T1_W0'); on('T1_W0',(net.eq(clen,0,e),'RD0',{ap:cp,ao:co,drag:0}),(None,'T1_W1',{r1:cb+net.min_(co,clen-1),t1_s:net.min_(co,clen-1),t1_e:net.min_(co,clen-1)}))
e=S('T1_W1'); on('T1_W1',(None,'T1_WL',{t1_c:t1_cls(R1,e)}))
e=S('T1_WL'); on('T1_WL',(net.eq(t1_s,0,e),'T1_WR',None),(None,'T1_WL2',{r1:cb+t1_s-1}))
e=S('T1_WL2'); on('T1_WL2',(net.eq(t1_cls(R1,e),t1_c,e),'T1_WL',{t1_s:t1_s-1}),(None,'T1_WR',None))
e=S('T1_WR'); on('T1_WR',(net.ge(t1_e+1,clen,e),'T1_WT',None),(None,'T1_WR2',{r1:cb+t1_e+1}))
e=S('T1_WR2'); on('T1_WR2',(net.eq(t1_cls(R1,e),t1_c,e),'T1_WR',{t1_e:t1_e+1}),(None,'T1_WT',None))
on('T1_WT',(net.step(t1_c),'T1_WS',{t1_e:t1_e+1}),(None,'T1_WD',{t1_e:t1_e+1}))
e=S('T1_WS'); on('T1_WS',(net.ge(t1_e,clen,e),'T1_WD',None),(None,'T1_WS2',{r1:cb+t1_e}))
e=S('T1_WS2'); on('T1_WS2',(net.eq(R1,32,e),'T1_WS',{t1_e:t1_e+1}),(None,'T1_WD',None))
e=S('T1_WD'); _wd={ap:cp,ao:t1_s,co:t1_e,drag:0,blink:0}
on('T1_WD',(net.eq(a4cw,1,e),'A4_CC',{**_wd,a4cw:0}),(net.eq(a4cw,2,e),'A4_FA0',{**_wd,a4cw:0}),(None,'RD0',_wd))
#@@ para
# a paragraph property change is logged as op 6, so it undoes and joins the group
e=S('T1_PA'); t1_newv=G_(alv,ONE-t1_pdm)+G_(net.min_(net.relu(R2+t1_pdd-1000),480),t1_pdm)
log(e,6,pwalk,pfld,R2,t1_newv)
on('T1_PA',(None,'PA2',{w1:(t1_pb+pfld,t1_newv),w2:(t1_pb+DIRTY,1)}))
on('PA2',(net.lt(pwalk,hi_p,S('PA2')),'PA0',{pwalk:pwalk+1}),(a4cfk,'A4_CF1',{a4cfk:0}),(None,'RD0',{lc:1,t1_pdm:0}))
mark_d(S('T1_UP'),cp);mark_d(S('T1_VP'),cp)
on('T1_UP',(None,'UCK',{w1:(cb+uo,uch),w2:(cb+DIRTY,1)}))
on('T1_VP',(None,'VCK',{w1:(cb+uo,ust),w2:(cb+DIRTY,1)}))
#@@ find
# whole word check on the search walker
e=S('T1_FW0'); t1_ok=net.and_(net.or_(net.eq(fo,0,e),ONE-t1_isw(R1,e)),net.or_(net.ge(fo+qlen,fl,e),ONE-t1_isw(R2,e)))
on('T1_FW0',(t1_ok,'FJ',{ap:fp,ao:fo,jp:fp,jo:fo+qlen,jret.r:jret.id('FOUND')}),(None,'F3',{fo:fo+1,fk:0}))
# match counter: walks the document in slices through 1 ms timer events
e=S('T1_C0'); on('T1_C0',(net.or_(net.eq(mode,0,e),net.eq(mode,3,e),net.ge(mode,4,e),net.eq(qlen,0,e)),'T1_CF',None),(None,'T1_C1',{t1_cb:0}))
e=S('T1_C1'); on('T1_C1',(net.ge(t1_cw,npar,e),'T1_CF',None),(net.ge(t1_cb,1500,e),'T1_CS',None),(None,'T1_C2',{r1:as_x(PT)+t1_cw}))
on('T1_C2',(None,'T1_C3',{t1_cB:R1,r2:R1+LEN}))
on('T1_C3',(qmrk,'IMP3_C0',{t1_cl:R2,t1_ck:0}),(None,'T1_C4',{t1_cl:R2,t1_ck:0}))
e=S('T1_C4'); on('T1_C4',(net.gt(t1_co_+qlen,t1_cl,e),'T1_C1',{t1_cw:t1_cw+1,t1_co_:0,t1_cb:t1_cb+1}),(net.ge(t1_cb,1500,e),'T1_CS',None),(None,'T1_C5',{r1:t1_cB+t1_co_+t1_ck,r2:as_x(Q)+t1_ck,t1_cb:t1_cb+1}))
e=S('T1_C5'); m5=net.eq(low(R1,e),low(R2,e),e); done5=net.and_(m5,net.ge(t1_ck+1,qlen,e))
on('T1_C5',(net.and_(done5,t1_fw),'T1_C6',{r1:t1_cB+net.relu(t1_co_-1),r2:t1_cB+t1_co_+qlen}),(done5,'T1_C7',None),(m5,'T1_C4',{t1_ck:t1_ck+1}),(None,'T1_C4',{t1_co_:t1_co_+1,t1_ck:0}))
e=S('T1_C6'); ok6=net.and_(net.or_(net.eq(t1_co_,0,e),ONE-t1_isw(R1,e)),net.or_(net.ge(t1_co_+qlen,t1_cl,e),ONE-t1_isw(R2,e)))
on('T1_C6',(ok6,'T1_C7',None),(None,'T1_C4',{t1_co_:t1_co_+1,t1_ck:0}))
e=S('T1_C7'); on('T1_C7',(None,'T1_C4',{t1_cn:t1_cn+1,t1_ci:t1_ci+net.and_(net.ge(Lo,t1_cw*2048+t1_co_,e),has_sel),t1_co_:t1_co_+qlen,t1_ck:0}))
on('T1_CF',(None,'T1_CD',{t1_cntp:0,t1_cr:1}))
on('T1_CS',(None,'T1_CD',{t1_cr:1}))
e=S('T1_CD'); on('T1_CD',(net.or_(net.eq(qlen,0,e),net.eq(mode,0,e)),'T1_CE',None),(net.and_(net.eq(t1_cn,0,e),t1_cntp),'T1_CE',{rA:(PX+386,DOCY+4,80,20,PAL_B[3],0)}),(net.eq(t1_cn,0,e),'T1_CTn',{rA:(PX+386,DOCY+4,80,20,PAL_B[3],0)}),(net.step(t1_ci),'T1_CTa',{rA:(PX+386,DOCY+4,80,20,PAL_B[3],0),sx:PX+388}),(None,'T1_CTb',{rA:(PX+386,DOCY+4,80,20,PAL_B[3],0),sx:PX+388}))
#@@ biu
e=S('TB1')
def t1_hc(r,id_):
    hv=net.and_(e-net.and_(e,r),net.eq(t1_hov,id_,e)); idle=e-net.and_(e,r)-hv
    return tuple(net.and_(e,r)*PAL_B[1][i]+hv*PAL_B[5][i]+idle*PAL_B[3][i] for i in range(3))
def t1_bg(st,r,id_,en):
    hv=net.and_(en-net.and_(en,r),net.eq(t1_hov,id_,en)); bg[1].lin(net.and_(en,r)); bg[5].lin(hv); bg[3].lin(en-net.and_(en,r)-hv)
on('TB1',(None,'TB2',{rA:(112,90,26,24,t1_hc(fbr,201),201),rB:(138,90,26,24,t1_hc(fir,202),202),rC:(164,90,26,24,t1_hc(fur,203),203)}))
t1_bg('TB2',fbr,201,S('TB2'));t1_bg('TB3',fir,202,S('TB3'));t1_bg('TB4',fur,203,S('TB4'))
on('TB2',(None,'TB3',{gly:(ord('B'),9+16,121,94,0,None)}))
on('TB3',(None,'TB4',{gly:(ord('I'),9+32,149,94,0,None)}))
on('TB4',(None,'TB5',{gly:(ord('U'),9+64,172,94,0,None)}))
on('TB5',(None,'TB6',{rA:(243,65,32,20,(255,255,255),243),sx:249}))
#@@ btn
rules+=[(B[35],'T1_M0',{t1_mop:4,t1_mrow:99,t1_mtop:DOCY+27,clip0:0,clip1:0}),
 (B[62],'T1_M0',{t1_mop:1,t1_mrow:99,t1_mtop:87,clip0:0,clip1:0}),
 (B[60],'T1_M0',{t1_mop:2,t1_mrow:99,t1_mtop:87,clip0:0,clip1:0}),
 (B[61],'T1_M0',{t1_mop:3,t1_mrow:99,t1_mtop:115,t1_mx:270,clip0:0,clip1:0}),
 (B[55],'RD0',{t1_tdrag:1,t1_grab:hy_-thumb,autos:0}),
 (B[64],'PB0',{grp:grp+1,t1_lastk:0}),
 (B[65],'PA0',{pwalk:lo_p,pfld:PIND,t1_pdm:1,t1_pdd:1000-48,grp:grp+1,t1_lastk:0}),
 (B[66],'PA0',{pwalk:lo_p,pfld:PIND,t1_pdm:1,t1_pdd:1000+48,grp:grp+1,t1_lastk:0}),
 (B[67],'PA0',{pwalk:lo_p,pfld:PSPA,t1_pdm:1,t1_pdd:1000-8,grp:grp+1,t1_lastk:0}),
 (B[68],'PA0',{pwalk:lo_p,pfld:PSPA,t1_pdm:1,t1_pdd:1000+8,grp:grp+1,t1_lastk:0}),
 (B[69],'T1_M0',{t1_mop:5,t1_mrow:99,t1_mtop:127,clip0:0,clip1:0}),
 (B[70],'T1_M0',{t1_mop:6,t1_mrow:99,t1_mtop:127,clip0:0,clip1:0}),
 (B[72],'UI',{t1_ruler:ONE-t1_ruler,clip0:0,clip1:0}),
 (B[73],'UI',{t1_marks:ONE-t1_marks,clip0:0,clip1:0})]
#@@ late
fsm.set(t1_rv,S('UI'),0)
# ---- hover: reads the object id under the pointer from the last image ----
on('T1_HV',(None,'T1_HV1',{pix:(hx_,hy_)}))
e=S('T1_HV1'); isb=net.or_(net.and_(net.ge(A_,201,e),net.lt(A_,250,e)),net.and_(net.ge(A_,251,e),net.lt(A_,254,e)),net.eq(A_,255,e))
newh=G_(A_,isb)+a4_hover(e); hch=net.step(net.gt(newh,t1_hov,e)+net.lt(newh,t1_hov,e))
inrow=net.eq(A_,254,e); nr=X(); _p2ir=net.gate(e,inrow)   # p2: the row is worked out only over a menu row, so other moves read none of it
for k_ in range(1,21): nr=nr+net.ge(hy_,t1_mtop+RH*k_,_p2ir)
_gm=net.or_(net.eq(t1_mop,3,e),net.eq(t1_mop,7,e),net.eq(t1_mop,10,e)); _gc=X()
for k_ in range(1,8): _gc=_gc+net.ge(hx_,t1_mx+GC*k_,_p2ir)
newr=G_(nr,net.and_(inrow,ONE-_gm))+G_(nr*8+_gc,net.and_(inrow,_gm))+(e-inrow)*99; rch=net.step(net.gt(newr,t1_mrow,e)+net.lt(newr,t1_mrow,e))
on('T1_HV1',(net.and_(t1_mopb,rch),'T1_M0',{t1_mrow:newr,t1_nh:1,clip0:0,clip1:0}),(t1_mopb,'T1_HH',None),
 (hch,'UI',{t1_hov:newh,t1_hvo:1,t1_nh:1,clip0:0,clip1:0}),(None,'T1_HH',None))
on('T1_HH',(a11busy,'A11_T3',None),(mp_ptr_on,'PT0',{mp_ptq:1,mp_pts_x:mp_ptx,mp_pts_y:mp_pty,mp_ptr_dr:1,pix:(mp_ptx,mp_pty),ptsave:(mp_ptx-PTHX,mp_pty-PTHY,PTRB,PTW,PTH,0)}),(None,'T1_HF',None))
on('T1_HF',(None,'IDLE',None)); halt.lin(S('T1_HF'))
# ---- thumb drag: inverse of the thumb position formula, rounded by a bit decomposition ----
e=S('T1_TM0'); t1_tv=net.relu(evb-t1_grab-(DOCY+4)); ph0=net.decode(pagesT,128,e); sv=X()
for k_ in range(1,128): sv=sv+net.gate(t1_tv*(k_*PST/(VH-8)),ph0[k_])
sb_=net.bits(sv,18,e)
on('T1_TM0',(None,'RD0',{scroll:sum((b_*(1<<i_) for i_,b_ in enumerate(sb_)),X()),autos:0}))
# ---- find bar pieces ----
t1_text('T1_FL','Find',PX+8,DOCY+6,0,3,'T1_FL9')
on('T1_FL9',(None,'FBL',{fi_:0,sx:PX+64}))
on('T1_FX0',(None,'T1_FX1',{rA:(PX+362,DOCY+4,22,20,PAL_B[3],235),rB:(PX+362,DOCY+4,22,1,(160,160,160),235),rC:(PX+362,DOCY+23,22,1,(160,160,160),235)}))

t1_bus=(g_en,g_ch,g_st,g_x,g_y,g_draw,fg)
def t1_chain(st,u,nxt):
    last=ui.emit(net,fsm,rA,t1_bus,YB,u.i,st,t1_mrow,t1_hb,bg); net.rec(S(nxt),last)
_u=ui.L(); _u.art(PX+365,DOCY+6,'chev',235); t1_chain('T1_FX1',_u,'T1_FX2')
on('T1_FX2',(None,'T1_CD',{t1_cr:0}))
text_chain('T1_CTa',[t1_ci,' of ',t1_cn],'T1_CE',y=DOCY+6,f=0,b=3)
text_chain('T1_CTb',[t1_cn,' found'],'T1_CE',y=DOCY+6,f=0,b=3)
t1_text('T1_CTn','No results',PX+388,DOCY+6,0,3,'T1_CE')
on('T1_CE',(t1_cr,'HALT',{t1_cr:0}),(None,'T1_FY',None))
e=S('T1_FY'); on('T1_FY',(net.eq(mode,2,e),'FB4',{rA:(PX+504,DOCY+4,236,20,WHITE,0),rB:(PX+750,DOCY+4,60,20,PAL_B[5],200+39),rC:(PX+504,DOCY+3,236,1,(160,160,160),0),rD:(PX+504,DOCY+24,236,1,(160,160,160),0),fi_:0,sx:PX+508}),(None,'TB0',None))
t1_text('T1_FZ','With',PX+470,DOCY+6,0,3,'T1_FZ2')
t1_text('T1_FZ2','All',PX+770,DOCY+6,0,5,'TB0')
# ---- post paint: ribbon refresh after a menu closes, ruler, view checks, open menu ----
on('T1_POST',(t1_uid,'UI',{t1_uid:0,t1_hvo:1,clip0:0,clip1:0}),(None,'T1_R0',None))
on('T1_R0',(None,'T1_R1',{ra4t:cb+A4T,ra4:cb+A4C,rc:cb+2062,rl:cb+SAVE,rp6:cb+PIND,r1:cb+LIST,rmeta:cb+META}))
e=S('T1_R1'); tb9=net.step(rc.out[0]); two9=net.and_(ONE-tb9,net.eq(ncol,2,e)); one9=net.and_(e,ONE-tb9,ONE-two9)
rL9=s_tx+G_(MT[1],tb9)+tb9*6+net.gate(rl.out[5],e)
rW9=G_(MT[0],tb9)+G_(s_tw,one9)+G_((s_tw-24)*0.5,two9)
_lb9=net.bits(R1,9,e); rI9=net.gate(rp6.out[0],e)+net.step(R1)*48+(_lb9[2]+_lb9[3]*2)*48
on('T1_R1',(net.and_(e,ONE-t1_ruler),'T1_V0',None),
 (net.and_(t1_rv,net.eq(rL9,t1_rL,e),net.eq(rW9,t1_rW,e),net.eq(rI9,t1_rI,e),net.eq(rp6.out[1],a4rF,e),net.eq(A4O[6],a4rR,e),net.eq(A4TO[0]+A4TO[1]*3+A4TO[2]*7+A4TO[3]*13,a4rS,e)),'T1_V0',None),
 (None,'T1_RDz',{zrul:1,t1_rL:rL9,t1_rW:rW9,t1_rI:rI9,t1_rv:1,a4rF:rp6.out[1],a4rR:A4O[6],a4rS:A4TO[0]+A4TO[1]*3+A4TO[2]*7+A4TO[3]*13,a4m[0]:A4TO[0],a4m[1]:A4TO[1],a4m[2]:A4TO[2],a4m[3]:A4TO[3]}))
on('T1_RDz',(None,'T1_RDa',{rZ:(0,150,1280,24,(230,230,230),0)}))
on('T1_RDa',(None,'T1_RT',{rB:(s_px,154,s_pw,16,(198,198,198),0),rC:(t1_rL,154,t1_rW,16,WHITE,0)}))
exec(open('rv_a1_ruler.py').read())
MC=(96,94,92)
for i_ in range(5):
    on(f'T1_RM{i_}',(None,f'T1_RM{i_+1}' if i_<4 else 'A4_RZ0',{
      rA:(t1_rL+t1_rI+pf_val(a4rF)-4+i_,150+i_,9-2*i_,1,MC,0),
      rB:(t1_rL+t1_rI-i_,169+i_,1+2*i_,1,MC,0),
      rC:(t1_rL+t1_rW-a4rR-i_,169+i_,1+2*i_,1,MC,0)}))
e=S('T1_V0'); on('T1_V0',(rdm,'IMP3_RB',None),(net.eq(tab,5,e),'T1_V1',None),(None,'T1_M0',None))
e=S('T1_V1'); rA.drive(net.and_(e,t1_ruler),(15,72,8,8,ui.BLUE,201)); rB.drive(net.and_(e,t1_marks),(15,98,8,8,ui.BLUE,202))
on('T1_V1',(None,'T1_M0',None))
# ---- menus: rows use alpha 254, the row is computed from the pointer y ----
T1_SZ=[8,9,10,11,12,14,16,18,20,22,24,26,28,36,48,72]    # rows of the size menu, in points
T1_CN=['Black','Gray','White','Blue','Red','Green','Orange','Purple']
def t1_gmenu(k,x,y,colors,more=None,more2=None,recent=False,nxt='T1_END'):
    "A grid of color swatches; the cell comes from the pointer x and y."
    u=ui.L(); rows_=(len(colors)+7)//8
    n_=rows_+(1 if more else 0)+(1 if recent else 0)
    u.r(x+2,y+2,GC*8+1,GC*n_+1,(200,198,196),0); u.r(x-1,y-1,GC*8+2,GC*n_+2,(150,148,146),0)
    if more: u.r(x,y+rows_*GC,GC*8,GC,WHITE,254,PAL_B[5],rows_*8); u.t(x+8,y+rows_*GC+1,more,9,0,0,True)
    if more2: n_+=1; u.r(x+2,y+2,GC*8+1,GC*n_+1,(200,198,196),0); u.r(x-1,y-1,GC*8+2,GC*n_+2,(150,148,146),0); u.r(x,y+rows_*GC,GC*8,GC,WHITE,254,PAL_B[5],rows_*8); u.t(x+8,y+rows_*GC+1,more,9,0,0,True); u.r(x,y+(rows_+1)*GC,GC*8,GC,WHITE,254,PAL_B[5],rows_*8+8); u.t(x+8,y+(rows_+1)*GC+1,more2,9,0,0,True)
    for i_,c_ in enumerate(colors):
        cx_=x+(i_%8)*GC; cy_=y+(i_//8)*GC
        u.r(cx_,cy_,GC,GC,WHITE,254,PAL_B[5],i_); u.r(cx_+3,cy_+3,GC-6,GC-6,(150,150,150),254); u.r(cx_+4,cy_+4,GC-8,GC-8,c_,254)
    if recent: imp6_recent_cells(u,x,y+(rows_+2)*GC)
    t1_chain(f'T1_MM{k}',u,nxt)
def t1_menu(k,x,y,w,labels,draw=None):
    u=ui.L(); n=len(labels)
    u.r(x+2,y+2,w+1,RH*n+1,(200,198,196),0); u.r(x-1,y-1,w+2,RH*n+2,(150,148,146),0)
    for r_,lb in enumerate(labels):
        u.r(x,y+r_*RH,w,RH,WHITE,254,PAL_B[5],r_)
        if draw: draw(u,r_,x,y+r_*RH)
        else: u.t(x+8,y+r_*RH+2,lb,9,0,0,True)
    t1_chain(f'T1_MM{k}',u,'T1_END')
def _fnt(u,r_,x,y): u.t(x+8,y+2,(rom.FAM_NAMES+['Other font...'])[r_],9+rom.st_of_font(r_ if r_<len(rom.FAM) else 0),0,0,True)
def _col(u,r_,x,y):
    u.r(x+6,y+4,14,14,(120,120,120),254); u.r(x+7,y+5,12,12,PAL_F[r_],254); u.t(x+26,y+2,T1_CN[r_],9,0,0,True)
def _fop(u,r_,x,y):
    u.r(x+6,y+4,14,14,(120,120,120),254); u.r(x+7,y+5,12,12,WHITE,254); u.k(t1_fw if r_ else t1_case,x+9,y+7,8,8,ui.BLUE,254)
    u.t(x+26,y+2,['Match case','Whole words'][r_],9,0,0,True)
t1_menu(1,112,87,128,[0]*(len(rom.FAM)+1),_fnt)
t1_menu(2,242,87,48,[str(i_) for i_ in T1_SZ])
t1_gmenu(3,270,115,PAL_F,'More Colors...',IMP5_PICK_ROW,recent=True,nxt='IMP6_RC0')
t1_gmenu(15,270,115,IMP5_PICK)
t1_gmenu(7,306,115,[(255,255,255)]+PAL_B[6:13])
t1_menu(8,464,115,70,['1.0','1.15','1.5','2.0'])
t1_menu(4,PX+362,DOCY+27,130,[0,0],_fop)
t1_menu(5,6,127,190,['Normal: 1 in sides','Moderate: 0.75 in sides','Narrow: 0.5 in'])
t1_menu(6,708,127,70,['1.0','1.15','1.5','2.0'])
t1_menu(14,LFX,LFY,130,LF_LABELS+['Restart at 1','Continue Numbering'])   # p2: the last two rows set or clear the caret item's restart flag
e=S('T1_M0'); mh=net.decode(t1_mop,21,e)
on('T1_M0',(mh[12],'RVA3_MM0',None),*[(mh[k_],f'T1_MM{k_}',None) for k_ in (*range(1,12),13,14,15,20)],(None,'T1_END',None))
on('T1_END',(t1_nh,'T1_HH',{t1_nh:0,t1_hvo:0,rB:(1265,thumb,12,net.min_(t1_thh,net.relu(as_x(DOCB)-thumb)),tuple(as_x(205)-net.eq(t1_hov,255,S('T1_END'))*65 for _ in range(3)),255)}),(None,'HALT',{t1_hvo:0}))
on('T1_MD',(None,'T1_MD1',{pix:(hx_,hy_)}))
e=S('T1_MD1'); nr1=X()
for k_ in range(1,21): nr1=nr1+net.ge(hy_,t1_mtop+RH*k_,e)   # p2: 21 rows for the List Style menu
_gm1=net.or_(net.eq(t1_mop,3,e),net.eq(t1_mop,7,e),net.eq(t1_mop,10,e),net.eq(t1_mop,15,e)); _gc1=X()
for k_ in range(1,8): _gc1=_gc1+net.ge(hx_,t1_mx+GC*k_,e)
on('T1_MD1',(net.eq(A_,254,e),'T1_MR',{t1_mrow:G_(nr1,ONE-_gm1)+G_(nr1*8+_gc1,_gm1)}),(None,'T1_MX',None))
on('T1_MX',(None,'RD0',{t1_mop:0,t1_uid:1,t1_mrow:99}))
e=S('T1_MK'); nrw=mh_n=X()
mk0=net.decode(t1_mop,21,e); nrw=nrw+G_(a6nr,mk0[20])
for k_,c_ in ((1,9),(2,11),(3,33),(4,2),(5,3),(6,4),(7,8),(8,4),(9,5),(10,64),(15,64),(11,7),(12,8),(13,11),(14,19)): nrw=nrw+mk0[k_]*c_
on('T1_MK',(net.eq(eva,27,e),'T1_MX',None),(net.and_(net.eq(eva,13,e),net.lt(t1_mrow,64,e)),'T1_MR',None),(net.eq(eva,13,e),'T1_MX',None),
 (net.and_(net.eq(eva,131,e),net.ge(t1_mrow+1,nrw,e)),'T1_M0',{t1_mrow:0}),(net.eq(eva,131,e),'T1_M0',{t1_mrow:t1_mrow+1}),
 (net.and_(net.eq(eva,129,e),net.or_(net.eq(t1_mrow,0,e),net.eq(t1_mrow,99,e))),'T1_M0',{t1_mrow:nrw-1}),(net.eq(eva,129,e),'T1_M0',{t1_mrow:t1_mrow-1}),(None,'HALT',None))
e=S('T1_MR'); mr=net.decode(t1_mop,21,e); rr_=net.decode(t1_mrow,34,e); CM={t1_mop:0,t1_uid:1,t1_mrow:99}; mrules=[]
def mc(k_,r_): return net.and_(net.step(mr[k_]),net.step(rr_[r_]))
for r_ in range(len(rom.FAM)): mrules.append((mc(1,r_),'FMTS',{fm:10,fcol:r_,fnx:0,**CM}))
mrules.append((mc(1,8),'V4_PR',{prk:5,**CM}))
for r_,si_ in enumerate(T1_SZ): mrules.append((mc(2,r_),'FMTS',{fm:9,fsi:rom.sz_raw(rom.SZ.index(si_)),**CM}))
for r_ in range(32): mrules.append((mc(3,r_),'FMTS',{fm:7,fcol:r_,fck:0,**CM}))
mrules+=imp5_pick_rules(mr,CM,e)+imp6_recent_rules(mr,CM,e)
mrules.append((net.and_(net.step(mr[3]),net.ge(t1_mrow,32,e),net.lt(t1_mrow,64,e)),'V4_PR',{prk:1,**CM}))
for r_ in range(8): mrules.append((mc(7,r_),'FMTS',{fm:15,fhl:r_,**CM}))
mrules.append((mc(4,0),'RD0',{t1_case:ONE-t1_case,**CSTART,**CM}))
mrules.append((mc(4,1),'RD0',{t1_fw:ONE-t1_fw,**CSTART,**CM}))
for r_,v_ in enumerate((3,8,4)): mrules.append((mc(5,r_),'T3_SP0',{tsop:v_,**CM}))
for r_ in range(4):
    mrules.append((mc(6,r_),'PA0',{pwalk:lo_p,pfld:PLSP,alv:r_ or 6,grp:grp+1,t1_lastk:0,**CM}));mrules.append((mc(8,r_),'PA0',{pwalk:lo_p,pfld:PLSP,alv:r_ or 6,grp:grp+1,t1_lastk:0,**CM}))
for r_,(st_,a_) in enumerate((('CUT',{rv_rp:1}),('COPY',{rv_rp:1}),('HALT',{wpaste:1,rv_rp:1}),('SELALL',{}),('FMTS',{fm:1}),('FMTS',{fm:2}),('FMTS',{fm:3}),('RD0',{mode:1,field:0,qrep:1,**CSTART}),('V4_PR',{prk:7}),('P2_CA0',{p2m:1}),('P2_CA0',{p2m:2}))): mrules.append((mc(12,r_),st_,{**a_,**CM}))
mrules+=a4_mrules(mc,CM,e)+a4_mrules2(mc,CM,e)
for r_ in range(8): mrules.append((mc(20,r_),'A6S_PK',{a6sr:r_,**CM}))
for r_ in range(10): mrules.append((mc(13,r_),'V5_MP',{t2si:zso+r_,**CM}))
mrules.append((mc(13,10),'T1_M0',{zso:zso+10,t1_mrow:99}))
for r_ in range(19): mrules.append((mc(14,r_),'V6_LF',{alv:r_+1,**CM}))
for r_ in range(2): mrules.append((mc(14,19+r_),'P2_RS0',{alv:1-r_,grp:grp+1,**CM}))
on('T1_MR',*mrules,(None,'T1_MX',None))
