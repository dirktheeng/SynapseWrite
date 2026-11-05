# ---- Tier 3 features, exec'd from app.py ----
net.group('tier3')
T3_RETS=[];T3_WPORTS=[]
import t3_btn
def t3ret(n):
    r_=Ret(n); T3_RETS.append(r_); return r_
def floorv(val,en,nb=14):
    "Exact floor of a nonnegative value, by descending thresholds."
    rem=net.gate(val,en); out=X()
    for k_ in reversed(range(nb)):
        b_=net.step(rem-2**k_+1e-6); out=out+b_*(2**k_); rem=rem-b_*(2**k_)
    return out
# undo op 6: swap one slot cell with the value held in the log entry
for st_,at_,nx_ in (('T3_US',usp,'UCK'),('T3_VS',usp-6,'VCK')):
    on(st_,(None,st_+'1',{r1:cb+uo}))
    e=S(st_+'1'); mark_d(e,cp)
    wlog.drive(e,(at_,6,up,uo,R1,0,ug))
    on(st_+'1',(None,'JR',{jret.r:0,w1:(cb+uo,uch),w2:(cb+DIRTY,1)}) if False else (None,'OR',{w1:(cb+uo,uch),w2:(cb+DIRTY,1)}))
_chain=[0]
def set_chain(start,items,nxt):
    "Logged writes of slot cells of the caret paragraph, one per entry (offset,value)."
    cur=start
    for i_,(of_,v_) in enumerate(items):
        n_=f'{start}_{i_}'
        on(cur,(None,n_,{r1:cb+of_}))
        e=S(n_); log(e,6,cp,of_,R1,0)
        cur2=f'{start}_w{i_}'
        on(n_,(None,cur2,{w1:(cb+of_,v_),w2:(cb+DIRTY,1)}))
        cur=cur2
    on(cur,(None,nxt,None))
# ---- table scan: finds the first cell, row count, and caret row ----
tn=R();tc=R();ts=R();trows=R();trk=R();tq=R();ti=R();fa0=R();fa1=R();fa2=R();tnw=R();run=R();ipos=R()
a1=R();a1v=R();a2=R();a2v=R();a1m=R();tscmd=t3ret('T3_SR');kret=t3ret('T3_KR')
def scan(st,ret):
    on(st,(None,'T3_TS0',{tscmd.r:tscmd.id(ret),grp:grp+1}))
on('T3_TS0',(None,'T3_TS1',{rc:cb+2062}))
e=S('T3_TS1')
on('T3_TS1',(net.step(rc.out[0]),'T3_TS2',{tn:rc.out[0],tc:rc.out[1],ts:cp-rc.out[1],trows:1,trk:0}),(None,'RD0',None))
e=S('T3_TS2')
on('T3_TS2',(net.ge(ts,tn+1,e),'T3_TS3',{r1:as_x(PT)+ts-1}),(None,'T3_TS5P',None))
on('T3_TS3',(None,'T3_TS4',{r2:R1+2062}))
e=S('T3_TS4')
on('T3_TS4',(net.eq(R2,tn,e),'T3_TS2',{ts:ts-tn,trows:trows+1,trk:trk+1}),(None,'T3_TS5P',None))
on('T3_TS5P',(None,'T3_TS5',{tq:cp-tc+tn}))
e=S('T3_TS5')
on('T3_TS5',(net.lt(tq,npar,e),'T3_TS6',{r1:as_x(PT)+tq}),(None,'T3_SR',None))
on('T3_TS6',(None,'T3_TS7',{r2:R1+2062}))
e=S('T3_TS7')
on('T3_TS7',(net.eq(R2,tn,e),'T3_TS5',{tq:tq+tn,trows:trows+1}),(None,'T3_SR',None))
def jump(st,p,o,ret):
    on(st,(None,st+'_J',{jp:p,jo:o,jret.r:jret.id(ret)})); on(st+'_J',(None,'J0',None))
# ---- insert table ----
tin_w=R()
for i_,n_ in enumerate((2,3,4)): pass
on('TI0',(None,'SPLIT',{oret.r:oret.id('T3_TI0'),tip:cp+1}))
e=S('T3_TI0'); hti=net.decode(tin,5,e)
on('T3_TI0',(None,'TI1',{tin_w:floorv(G_(s_tw*0.5,hti[2])+G_(s_tw*(1.0/3),hti[3])+G_(s_tw*0.25,hti[4]),e),run:0}))
e=S('TI1'); wr=net.ge(tic+1,tin,e)
set_chain('TI1',[(2062,tin),(2063,tic),(CWO,tin_w),(CXO,run)],'T3_TI2')
e=S('T3_TI2'); wr=net.ge(tic+1,tin,e)
on('T3_TI2',(wr,'T3_TI3',{tic:0,run:0}),(None,'T3_TI3',{tic:tic+1,run:run+tin_w}))
e=S('T3_TI3')
on('T3_TI3',(net.step(tir),'SPLIT',{tir:tir-1,oret.r:oret.id('TI1')}),(None,'SPLIT',{oret.r:oret.id('TI2')}))
on('TI2',(None,'J0',{jp:tip,jo:0,jret.r:jret.id('AFTER_ED')}))
# ---- row insert ----
rowst=R();rsh=R();
for st_,bel in (('T3_C_RA',0),('T3_C_RB',1)):
    scan(st_,st_+'1')
    on(st_+'1',(None,st_+'2',{rowst:cp-tc+tn*bel,ti:0}))
    jump(st_+'2',rowst-1,2047,'T3_IR0' if bel==0 else 'T3_IRb')
fsm.set(rsh,S('T3_C_RA1'),1);fsm.set(rsh,S('T3_C_RB1'),0)
on('T3_IRb',(None,'T3_IR0',None))
e=S('T3_IR0')
on('T3_IR0',(net.ge(ti,tn,e),'T3_IR5',{ti:0}),(None,'SPLIT',{ti:ti+1,oret.r:oret.id('T3_IR0')}))
e=S('T3_IR5')
on('T3_IR5',(net.ge(ti,tn,e),'T3_IRE',None),(None,'T3_IR5J',{jp:rowst+ti,jo:0,jret.r:jret.id('T3_IR6')}))
on('T3_IR5J',(None,'J0',None))
on('T3_IR6',(None,'T3_IR7',{r1:as_x(PT)+cp+G_(tn,rsh)-G_(tn,ONE-rsh)}))
on('T3_IR7',(None,'T3_IR8',{rmeta:R1+META}))
on('T3_IR8',(None,'T3_IR9',{fa0:MT[0],fa1:MT[1],fa2:MT[2]}))
set_chain('T3_IR9',[(2062,tn),(2063,ti),(CWO,fa0),(CXO,fa1),(CSH,fa2)],'T3_IRa')
on('T3_IRa',(None,'T3_IR5',{ti:ti+1}))
jump('T3_IRE',rowst,0,'AFTER_ED')
# ---- kill the caret cell: delete text, clear fields, merge away ----
on('T3_K0',(None,'T3_K1',{co:clen}))
e=S('T3_K1')
on('T3_K1',(net.step(co),'DEL',{co:co-1,oret.r:oret.id('T3_K1')}),(None,'T3_K2',None))
set_chain('T3_K2',[(2062,0),(2063,0),(CWO,0),(CXO,0),(CSH,0)],'T3_K3')
on('T3_K3',(None,'MERGE',{oret.r:oret.id('T3_KR')}))
# ---- row delete ----
scan('T3_C_DR','T3_DR1')
on('T3_DR1',(None,'T3_DR2',{rowst:cp-tc,ti:0}))
e=S('T3_DR2')
on('T3_DR2',(net.ge(ti,tn,e),'T3_END',{jp:net.min_(rowst,npar-1)}),(None,'T3_DR3',{jp:rowst,jo:0,jret.r:jret.id('T3_K0'),kret.r:kret.id('T3_DR4')}))
on('T3_DR3',(None,'J0',None))
on('T3_DR4',(None,'T3_DR2',{ti:ti+1}))
on('T3_END',(None,'T3_END2',{jo:0,jp:net.min_(jp,npar-1),jret.r:jret.id('AFTER_ED')}))
on('T3_END2',(None,'J0',None))
# ---- column operations: structural pass, then a field pass over every cell ----
p2n=R();p2i=R();p2q=R();p2end=R();cwk=R();capt=R()
on('T3_P2',(None,'T3_P2a',{p2q:ts,p2i:0,run:0,p2end:trows}) )
e=S('T3_P2a')
on('T3_P2a',(net.eq(p2end,0,e),'T3_END',{jp:capt}),(None,'T3_P2J',{jp:p2q,jo:0,jret.r:jret.id('T3_P2b')}))
on('T3_P2J',(None,'J0',None))
on('T3_P2b',(None,'T3_P2c',{rmeta:cb+META}))
e=S('T3_P2c'); h1=net.eq(p2i,a1,e); h2=net.eq(p2i,a2,e)
on('T3_P2c',(None,'T3_P2d',{fa0:net.relu(MT[0]+G_(a1v,h1)-G_(a1m,h1)+G_(a2v,h2)-G_(a2m if False else tdk*0,h2)) if False else net.relu(MT[0]+G_(a1v,h1)-G_(a1m,h1)+G_(a2v,h2)-G_(cwk,h2))}))
set_chain('T3_P2d',[(2062,p2n),(2063,p2i),(CWO,fa0),(CXO,run)],'T3_P2e')
e=S('T3_P2e'); lastc2=net.ge(p2i+1,p2n,e)
on('T3_P2e',(lastc2,'T3_P2a',{p2q:p2q+1,p2i:0,run:0,p2end:p2end-1}),(None,'T3_P2a',{p2q:p2q+1,p2i:p2i+1,run:run+fa0}))
# column insert
half=R();cinc=R()
for st_,rt in (('T3_C_CL',0),('T3_C_CR',1)):
    scan(st_,st_+'1')
    on(st_+'1',(net.ge(tn,8,S(st_+'1')),'RD0',None),(None,'T3_CI0',{ipos:tc+rt,ti:0,tq:ts+tc+rt-1}))
on('T3_CI0',(None,'T3_CI1',{rmeta:cb+META}))
e=S('T3_CI1')
on('T3_CI1',(None,'T3_CI2',{half:floorv(MT[0]*0.5,e)}))
e=S('T3_CI2')
on('T3_CI2',(net.ge(ti,trows,e),'T3_CI5',None),(None,'T3_CI3',{jp:tq,jo:2047,jret.r:jret.id('T3_CI4')}))
on('T3_CI3',(None,'J0',None))
on('T3_CI4',(None,'SPLIT',{ti:ti+1,tq:tq+tn+1,oret.r:oret.id('T3_CI2')}))
e=S('T3_CI5'); isr=net.eq(ipos,tc,e)
on('T3_CI5',(None,'T3_P2',{p2n:tn+1,a1:ipos,a1v:half,a1m:0,a2:tc+G_(as_x(1),isr),a2v:0,cwk:half,capt:ts+ipos}))
# column delete
scan('T3_C_DC','T3_DC1')
on('T3_DC1',(None,'T3_DC2',{rmeta:cb+META,ti:0,tq:ts+tc}))
on('T3_DC2',(None,'T3_DC3',{half:MT[0]}))
e=S('T3_DC3')
on('T3_DC3',(net.ge(ti,trows,e),'T3_DC6',None),(None,'T3_DC4',{jp:tq,jo:0,jret.r:jret.id('T3_K0'),kret.r:kret.id('T3_DC5')}))
on('T3_DC4',(None,'J0',None))
on('T3_DC5',(None,'T3_DC3',{ti:ti+1,tq:tq+tn-1}))
e=S('T3_DC6')
on('T3_DC6',(net.ge(tn,2,e),'T3_P2',{p2n:tn-1,a1:net.relu(tc-1),a1v:half,a1m:0,a2:99,a2v:0,cwk:0,capt:ts+net.relu(tc-1)}),(None,'T3_END',{jp:net.min_(ts,npar-1)}))
# ---- shading of the selected cells ----
shv=R();shp=R()
for k_,_ in t3_btn.SH:
    on(f'T3_C_S{k_}',(None,'T3_SH0',{shv:k_,shp:lo_p,grp:grp+1}))
on('T3_SH0',(None,'T3_SH1',{jp:shp,jo:0,jret.r:jret.id('T3_SH2'),fa2:cp,fa1:co}))
on('T3_SH1',(None,'J0',None))
on('T3_SH2',(None,'T3_SH3',{rc:cb+2062}))
e=S('T3_SH3')
on('T3_SH3',(net.step(rc.out[0]),'T3_SH4',None),(None,'T3_SH5',None))
set_chain('T3_SH4',[(CSH,shv)],'T3_SH5')
e=S('T3_SH5')
on('T3_SH5',(net.lt(shp,net.max_(fa2,ap),e),'T3_SH0x',{shp:shp+1}),(None,'T3_END',{jp:fa2}))
on('T3_SH0x',(None,'T3_SH1',{jp:shp,jo:0,jret.r:jret.id('T3_SH2')}))
# ---- row end: fill the rest of each cell, draw rules, record column border hit zones ----
on('RB0',(None,'RB1',{tivx:0}))
e=S('RB1')
on('RB1',(net.ge(tiv,tcols,e),'R1',{yy:rowmax+1,pi:pi+1,rB:(s_tx+tivx,by0,1,rowmax-rowtop+1,BC,0)}),(None,'T3_RBa',{r1:as_x(PT)+pi+1-tcols+tiv}))
on('T3_RBa',(None,'T3_RBb',{r2:R1+ENDY,rmeta:R1+META}))
e=S('T3_RBb'); shr=net.decode(MT[2],len(PAL_B),e)
def bcr(k): return sum((shr[i_]*PAL_B[i_][k] for i_ in range(len(PAL_B))),X())
on('T3_RBb',(None,'T3_RBc',{rA:(s_tx+MT[1]+1,R2+DOCY-scroll,net.relu(MT[0]-1),net.relu(rowmax-R2),(bcr(0),bcr(1),bcr(2)),0),rB:(s_tx+MT[1],by0,1,rowmax-rowtop,BC,0),rC:(s_tx+MT[1],by0,MT[0]+1,1,BC,0),fa0:MT[0],fa1:MT[1]}))
on('T3_RBc',(None,'RB1',{rA:(s_tx+fa1,rowmax+DOCY-scroll,fa0+1,1,BC,0),wht:(as_x(HIT)+hitn*6,s_tx+fa1+fa0-3,by0,s_tx+fa1+fa0+4,rowmax+DOCY-scroll,tiv+1,pi+1-tcols),hitn:hitn+1,tiv:tiv+1,tivx:fa1+fa0}))
# ---- mouse: object hit zones are compared in the network before the pixel hit test ----
tdx=R();tdy=R();tdc=R();tdr=R();tcw=R();tcw2=R()
e=S('T3_H0')
on('T3_H0',(net.ge(vi,hitn,e),'HT',{vi:0}),(None,'T3_H1',{rl:as_x(HIT)+vi*6}))
e=S('T3_H1'); hin=net.and_(net.ge(hx_,RL[0],e),net.lt(hx_,RL[2],e),net.ge(hy_,RL[1],e),net.lt(hy_,RL[3],e))
on('T3_H1',(hin,'T3_H2',{tdk:RL[4],tdr:RL[5],tdx:hx_,tdy:hy_,drag:0}),(None,'T3_H0',{vi:vi+1}))
on('T3_H2',(None,'HALT',None))
on('T3_MV',(None,'RD0',{tdx:tdx}))
tmx=R();tmy=R()
fsm.set(tmx,S('T3_MV'),eva);fsm.set(tmy,S('T3_MV'),evb)
fsm.set(tmx,S('T3_H1')*0+net.and_(S('T3_H1'),hin),hx_)
e=S('RE1'); dgd=net.and_(e,net.step(tdk),net.lt(tdk,17,e))
rC.drive(dgd,(tmx,DOCY,1,VH,(43,87,154),0))
# column border release: resize through the field pass
e=S('T3_MU'); ck_=net.and_(e,net.step(tdk),net.lt(tdk,17,e))
on('T3_MU',(ck_,'T3_CW0',{tmx:eva,tdc:tdk-1,tdk:0,jp:tdr,jo:0,jret.r:jret.id('T3_CW1')}),(net.and_(e,net.step(tdk)),'T3_IMU',None),(None,'IDL2',None))
on('T3_CW0',(None,'J0',None))
scan('T3_CW1','T3_CW2')
on('T3_CW2',(None,'T3_CW3',{r1:as_x(PT)+ts+tdc,r2:as_x(PT)+ts+net.min_(tdc+1,tn-1)}))
on('T3_CW3',(None,'T3_CW4',{rmeta:R1+META,tcw2:R2}))
on('T3_CW4',(None,'T3_CW5',{tcw:MT[0],rmeta:tcw2+META}))
e=S('T3_CW5'); lastcol=net.ge(tdc+1,tn,e)
gr=net.relu(tmx-tdx); sh_=net.relu(tdx-tmx)
tot_nb=MT[0]
grow=net.min_(gr,G_(as_x(4000),lastcol)+G_(net.relu(MT[0]-20),e-lastcol))
shrink=net.min_(sh_,net.relu(tcw-20))
on('T3_CW5',(None,'T3_P2',{p2n:tn,a1:tdc,a1v:grow,a1m:shrink,a2:G_(tdc+1,e-lastcol)+G_(as_x(99),lastcol),a2v:shrink,cwk:grow,capt:cp}))
on('T3_IMU',(None,'IDL2',{tdk:0}))

# ---- ribbon commands behind button id 54: tab, x and y select the command ----
e=S('T3_BTN'); b3=[]
for tb_,x_,y_,w_,h_,lb_,st_,c_ in t3_btn.BTNS:
    b3.append((net.and_(net.eq(tab,tb_,e),net.ge(hx_,x_,e),net.lt(hx_,x_+w_,e),net.ge(hy_,y_,e),net.lt(hy_,y_+h_,e)),st_,None))
on('T3_BTN',*b3,(None,'HALT',None))

# ---- sections: a paragraph with SECN>0 starts a new section on a new page, record SECN-1 ----
e=S('T3_SB0')
on('T3_SB0',(None,'T3_SB1',None))
e=S('T3_SB1')
sbadv={ptop:ptop+s_ps,yy:ptop+s_ps+RL[6],pages:pages+1,fnp:0,xcol:0,**sload(RL)}
on('T3_SB1',(full,'T3_SB2',sbadv),(None,'R2X',sbadv))
on('T3_SB2',(None,'T3_PS',{rB:(s_px,ptop+DOCY-scroll,s_pw,s_ph,WHITE,0)}))
sv_nc=R();sv_pw=R();sv_ph=R();sv_ml=R();sv_mr=R();sv_mt=R();sv_mb=R();sv_i=R();csc=R();swret=t3ret('T3_SWR')
# write record sv_i from the fields above
pxv=(as_x(1262)-sv_pw)*0.5
SWV=[sv_nc,sv_pw,sv_ph,pxv,pxv+sv_ml,sv_pw-sv_ml-sv_mr,sv_mt,sv_ph-sv_mt-sv_mb]
cur_='T3_SW'
for i_,v_ in enumerate(SWV):
    nx_=f'T3_SW{i_}' if i_<7 else 'T3_SWR'
    on(cur_,(None,nx_,{w1:(as_x(SECB)+sv_i*8+i_,net.relu(v_))})); cur_=nx_
# change the caret section: read, edit, write, relayout everything
on('T3_SP0',(None,'T3_SP1',{r1:cb+SSI}))
on('T3_SP1',(None,'T3_SP2',{csc:R1,sv_i:R1,rl:as_x(SECB)+R1*8}))
e=S('T3_SP2'); op_=net.decode(tsop,8,e)
base_={sv_nc:RL[0],sv_pw:RL[1],sv_ph:RL[2],sv_ml:RL[4]-RL[3],sv_mr:RL[1]-RL[4]+RL[3]-RL[5],sv_mt:RL[6],sv_mb:RL[2]-RL[6]-RL[7]}
def ovr(k_,v_):
    d_=dict(base_); d_.update(v_); return (op_[k_],'T3_SP3',d_)
on('T3_SP2',ovr(1,{sv_pw:net.min_(RL[1],RL[2]),sv_ph:net.max_(RL[1],RL[2])}),ovr(2,{sv_pw:net.max_(RL[1],RL[2]),sv_ph:net.min_(RL[1],RL[2])}),
 ovr(3,{sv_ml:96,sv_mr:96,sv_mt:96,sv_mb:96}),ovr(4,{sv_ml:48,sv_mr:48,sv_mt:48,sv_mb:48}),ovr(5,{sv_ml:144,sv_mr:144,sv_mt:96,sv_mb:96}),
 ovr(6,{sv_nc:1}),ovr(7,{sv_nc:2}),(None,'RD0',None))
on('T3_SP3',(None,'T3_SW',{swret.r:swret.id('T3_SP4')}))
on('T3_SP4',(None,'DA0',{di_:0}))
for st_,k_ in (('T3_C_POR',1),('T3_C_LAN',2),('T3_C_MN',3),('T3_C_MS',4),('T3_C_MW',5)):
    on(st_,(None,'T3_SP0',{tsop:k_}))
# section break at the caret: the following paragraph opens a copy of this section's record
on('T3_C_SB',(net.ge(nsec,39,S('T3_C_SB')),'RD0',None),(None,'T3_SB5',{grp:grp+1,r1:cb+SSI}))
on('T3_SB5',(None,'T3_SB6',{rl:as_x(SECB)+R1*8,sv_i:nsec}))
on('T3_SB6',(None,'SPLIT',{**base_,oret.r:oret.id('T3_SB7')}))
on('T3_SB7',(None,'T3_SW',{swret.r:swret.id('T3_SB8')}))
on('T3_SB8',(None,'T3_SB9',{nsec:nsec+1}))
set_chain('T3_SB9',[(SECN,nsec)],'AFTER_ED')

# ---- number without leading zeros, shared by every XML writer ----
nret2=t3ret('T3_NR'); nv2=R()
cur_n='T3_NZ'
for pw_ in (10000000,1000000,100000,10000,1000,100,10,1):
    nx_=f'T3_NZ{pw_}' if pw_>1 else 'T3_NR'
    e=S(cur_n); val=net.gate(nv2,e)
    for big in (10000000,1000000,100000,10000,1000,100,10):
        if big>pw_:
            dd=X()
            for t in range(1,10): dd=dd+net.step(val-big*t+0.5)
            val=val-dd*big
    dg=X()
    for t in range(1,10): dg=dg+net.step(val-pw_*t+0.5)
    show=e if pw_==1 else net.step(net.gate(nv2,e)-pw_+0.5)
    em_en.lin(show); em_b.add(show,48+dg)
    on(cur_n,(None,nx_,None)); cur_n=nx_
def numz(st,val,nx): on(st,(None,'T3_NZ',{nv2:val,nret2.r:nret2.id(nx)}))
# ---- zip container: every member carries its name, CRC and size in a table ----
znum=R();zo=R();znl=R();zds=R();zret=t3ret('T3_ZRT');cdoff=R();zk2=R();zL=R();zH=R();zs=R()
def lh_(name): return struct.pack('<IHHHHHIIIHH',0x04034b50,20,0,0,0,0x21,0,0,0,len(name),0)+name
def zbegin(st,name,nxt):
    on(st,(None,st+'a',{zo:fp,znl:len(name)}))
    lit(st+'a',lh_(name),st+'b')
    crci.lin(S(st+'b'))
    on(st+'b',(None,nxt,{zds:fp}))
def zend(st,nxt): on(st,(None,'T3_ZE',{zret.r:zret.id(nxt)}))
e=S('T3_ZE')
on('T3_ZE',(None,'T3_ZF',{zL:as_x(65535)-crcL,zH:as_x(65535)-crcH,zs:fp-zds}))
cur_='T3_ZF'
for i_ in range(12):
    nx_=f'T3_ZF{i_}'; e=S(cur_)
    v_={0:zL,1:zL,2:zH,3:zH}.get(i_,zs)
    bv_=le_bytes(v_,e,2)[i_%2] if i_<4 else le_bytes(zs,e)[(i_-4)%4]
    on(cur_,(None,nx_,{fw2:(zo+14+i_,bv_)})) if False else on(cur_,(None,nx_,{fw2:(as_x(FILE)+zo+14+i_,bv_)})); cur_=nx_
on(cur_,(None,cur_+'t',{w1:(as_x(ZT)+znum*6,zo),w2:(as_x(ZT)+znum*6+1,znl),w3:(as_x(ZT)+znum*6+2,zL),w4:(as_x(ZT)+znum*6+3,zH)}))
on(cur_+'t',(None,'T3_ZRT',{w1:(as_x(ZT)+znum*6+4,zs),znum:znum+1}))
XHEAD=b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
WNS=b'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"'
CTYPES=XHEAD+b'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'+b''.join(b'<Override PartName="/word/%s.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.%s+xml"/>'%(a_,b_) for a_,b_ in ((b'footnotes',b'footnotes'),(b'comments',b'comments'),(b'header1',b'header'),(b'header2',b'header'),(b'footer1',b'footer'),(b'footer2',b'footer')))+b'</Types>'
RTYPE=b'http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
RELS=XHEAD+b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="'+RTYPE+b'officeDocument" Target="word/document.xml"/></Relationships>'
DRELS0=XHEAD+b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+b''.join(b'<Relationship Id="%s" Type="%s%s" Target="%s.xml"/>'%(i_,RTYPE,t_,f_) for i_,t_,f_ in ((b'rIdF',b'footnotes',b'footnotes'),(b'rIdC',b'comments',b'comments'),(b'rIdH1',b'header',b'header1'),(b'rIdH2',b'header',b'header2'),(b'rIdR1',b'footer',b'footer1'),(b'rIdR2',b'footer',b'footer2')))
on('SAVE',(None,'SV0',{fp:0,znum:0}))
zbegin('SV0',b'[Content_Types].xml','T3_Z1'); lit('T3_Z1',CTYPES,'T3_Z1e'); zend('T3_Z1e','T3_Z2')
zbegin('T3_Z2',b'_rels/.rels','T3_Z3'); lit('T3_Z3',RELS,'T3_Z3e'); zend('T3_Z3e','T3_Z4')
zbegin('T3_Z4',b'word/document.xml','SVB')
lit('SVB',XHEAD+b'<w:document '+WNS+b'><w:body>','T3_SVB2')
on('T3_SVB2',(None,'SVP',{spc:0}))
# table structure around each cell paragraph
TB=b'<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders>'+b''.join(b'<w:%s w:val="single" w:sz="4" w:space="0" w:color="auto"/>'%k_ for k_ in (b'top',b'left',b'bottom',b'right',b'insideH',b'insideV'))+b'</w:tblBorders></w:tblPr><w:tblGrid>'
e=S('T3_SV0'); newt=net.and_(e,net.step(spc),net.step(net.step(spc-scols-0.5)+net.step(scols-spc-0.5)))
on('T3_SV0',(newt,'T3_SV1',None),(None,'T3_SV2',None))
lit('T3_SV1',b'</w:tbl>','T3_SV1b'); on('T3_SV1b',(None,'T3_SV2',{spc:0}))
e=S('T3_SV2')
on('T3_SV2',(net.eq(scols,0,e),'SVj',None),(net.step(spc),'T3_SV6',None),(None,'T3_SV3',None))
lit('T3_SV3',TB,'T3_SV4'); fsm.set(ti,S('T3_SV3'),0)
e=S('T3_SV4')
on('T3_SV4',(net.ge(ti,scols,e),'T3_SV5',None),(None,'T3_SV4a',{r1:as_x(PT)+pi+ti}))
on('T3_SV4a',(None,'T3_SV4b',{r2:R1+CWO}))
on('T3_SV4b',(None,'T3_SV4c',{tcw:R2}))
lit('T3_SV4c',b'<w:gridCol w:w="','T3_SV4d'); numz('T3_SV4d',tcw*15,'T3_SV4e'); lit('T3_SV4e',b'"/>','T3_SV4f')
on('T3_SV4f',(None,'T3_SV4',{ti:ti+1}))
lit('T3_SV5',b'</w:tblGrid>','T3_SV6')
e=S('T3_SV6')
on('T3_SV6',(net.eq(sci,0,e),'T3_SV6r',None),(None,'T3_SV7',None))
lit('T3_SV6r',b'<w:tr>','T3_SV7')
lit('T3_SV7',b'<w:tc><w:tcPr><w:tcW w:w="','T3_SV7a'); numz('T3_SV7a',scw*15,'T3_SV7b')
lit('T3_SV7b',b'" w:type="dxa"/>','T3_SV8')
e=S('T3_SV8')
on('T3_SV8',(net.step(ssh),'T3_SV8a',None),(None,'T3_SV9',None))
lit('T3_SV8a',b'<w:shd w:val="clear" w:color="auto" w:fill="','T3_SV8b')
e=S('T3_SV8b'); hsh_=net.decode(ssh,len(PAL_B),e)
on('T3_SV8b',*[(hsh_[i_],f'T3_SVh{i_}',None) for i_ in range(len(PAL_B))],(None,'T3_SV8c',None))
for i_,c_ in enumerate(PAL_B): lit(f'T3_SVh{i_}',('%02X%02X%02X'%c_).encode(),'T3_SV8c')
lit('T3_SV8c',b'"/>','T3_SV9')
lit('T3_SV9',b'</w:tcPr>','SVj')
e=S('T3_SVN')
on('T3_SVN',(net.step(scols),'T3_SVc',None),(None,'SVP',{pi:pi+1,spc:0}))
lit('T3_SVc',b'</w:tc>','T3_SVd')
e=S('T3_SVd')
on('T3_SVd',(net.ge(sci+1,scols,e),'T3_SVr',None),(None,'SVP',{pi:pi+1,spc:scols}))
lit('T3_SVr',b'</w:tr>','T3_SVs'); on('T3_SVs',(None,'SVP',{pi:pi+1,spc:scols}))
e=S('T3_SVE')
on('T3_SVE',(net.step(spc),'T3_SVEa',None),(None,'SVT',None))
lit('T3_SVEa',b'</w:tbl>','SVT')
lit('SVT',b'<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>','T3_Z4e')
zend('T3_Z4e','T3_Z5')
zbegin('T3_Z5',b'word/_rels/document.xml.rels','T3_Z6'); lit('T3_Z6',DRELS0+b'</Relationships>','T3_Z6e'); zend('T3_Z6e','T3_CD0')
# central directory from the member table, then the end record
on('T3_CD0',(None,'T3_CD1',{cdoff:fp,zk2:0}))
e=S('T3_CD1')
on('T3_CD1',(net.ge(zk2,znum,e),'T3_EO0',None),(None,'T3_CD2',{rl:as_x(ZT)+zk2*6}))
on('T3_CD2',(None,'T3_CD3',{zo:RL[0],znl:RL[1],zL:RL[2],zH:RL[3],zs:RL[4]}))
lit('T3_CD3',struct.pack('<IHHHHHH',0x02014b50,20,20,0,0,0,0x21),'T3_CDb0')
cur_='T3_CDb0'
for i_ in range(4):
    nx_=f'T3_CDb{i_+1}'; e=S(cur_); em_en.lin(e); em_b.add(e,le_bytes(zL if i_<2 else zH,e,2)[i_%2]); on(cur_,(None,nx_,None)); cur_=nx_
for i_ in range(8):
    nx_=f'T3_CDs{i_}'; e=S(cur_); em_en.lin(e); em_b.add(e,le_bytes(zs,e)[i_%4]); on(cur_,(None,nx_,None)); cur_=nx_
for i_ in range(2):
    nx_=f'T3_CDn{i_}'; e=S(cur_); em_en.lin(e); em_b.add(e,le_bytes(znl,e,2)[i_]); on(cur_,(None,nx_,None)); cur_=nx_
lit(cur_,b'\0'*12,'T3_CDo0')
cur_='T3_CDo0'
for i_ in range(4):
    nx_=f'T3_CDo{i_+1}'; e=S(cur_); em_en.lin(e); em_b.add(e,le_bytes(zo,e)[i_]); on(cur_,(None,nx_,None)); cur_=nx_
on(cur_,(None,'T3_CDm',{tq:0}))
e=S('T3_CDm')
on('T3_CDm',(net.ge(tq,znl,e),'T3_CD1',{zk2:zk2+1}),(None,'T3_CDm2',{r1:as_x(FILE)+zo+30+tq}))
e=S('T3_CDm2'); em_en.lin(e); em_b.add(e,R1); on('T3_CDm2',(None,'T3_CDm',{tq:tq+1}))
on('T3_EO0',(None,'T3_EO1',{zs:fp-cdoff}))
lit('T3_EO1',struct.pack('<IHH',0x06054b50,0,0),'T3_EOc0')
cur_='T3_EOc0'
for i_ in range(4):
    nx_=f'T3_EOc{i_+1}'; e=S(cur_); em_en.lin(e); em_b.add(e,le_bytes(znum,e,2)[i_%2]); on(cur_,(None,nx_,None)); cur_=nx_
for i_ in range(8):
    nx_=f'T3_EOd{i_}'; e=S(cur_); em_en.lin(e); em_b.add(e,le_bytes(zs if i_<4 else cdoff,e)[i_%4]); on(cur_,(None,nx_,None)); cur_=nx_
lit(cur_,b'\0\0','T3_EOe')
on('T3_EOe',(None,'HALT',{savel:fp}))
# ---- .docx reader additions ----
aval=R();nmret=t3ret('T3_NMR')
on('T3_NA',(None,'T3_NA1',{rl:OA+oi}))
e=S('T3_NA1')
on('T3_NA1',(net.eq(W[0],34,e),'T3_NB',{oi:oi+1,aval:0}),(None,'T3_NA',{oi:oi+1}))
on('T3_NB',(None,'T3_NB1',{rl:OA+oi}))
e=S('T3_NB1')
isd=net.and_(net.ge(W[0],48,e),net.lt(W[0],58,e))
on('T3_NB1',(isd,'T3_NB',{aval:aval*10+W[0]-48,oi:oi+1}),(None,'T3_NMR',None))
on('T3_GC',(None,'T3_NA',{nmret.r:nmret.id('T3_GC2')}))
e=S('T3_GC2')
on('T3_GC2',(None,'PX',{w1:(as_x(TGW)+gcount,floorv(aval*(1.0/15)+0.5,e)),gcount:gcount+1}))
on('T3_TC0',(None,'SPLIT',{oret.r:oret.id('T3_TC1')}))
on('T3_TC1',(None,'T3_TC2',{r1:as_x(TGW)+tcidx}))
on('T3_TC2',(None,'T3_TC3',{w1:(cb+2062,gcount),w2:(cb+2063,tcidx),w3:(cb+CWO,R1),w4:(cb+CXO,gx),gx:gx+R1,incell:1}))
on('T3_TC3',(None,'PX',{w1:(cb+ALIGN,0)}))
e=S('T3_SHD')
on('T3_SHD',(None,'T3_SHD1',{rl:OA+oi}))
e=S('T3_SHD1')
fillm=pat('w:fill="',e)
on('T3_SHD1',(fillm,'T3_SHD2',{rl:OA+oi+8}),(net.eq(W[0],62,e),'PX',None),(None,'T3_SHD',{oi:oi+1}))
e=S('T3_SHD2')
hx_m=[]; 
for i_,c_ in enumerate(PAL_B):
    if i_ in (0,1,3,4): continue
    hx_m.append((pat('%02X%02X%02X'%c_,e),i_))
sv_=X()
for c_,i_ in hx_m: sv_=sv_+c_*i_
anyp=net.or_(*[c_ for c_,_ in hx_m]); isa=pat('auto',e); isw=pat('FFFFFF',e)
on('T3_SHD2',(net.or_(isa,isw),'PX',None),(anyp,'PX',{w1:(cb+CSH,sv_)}),(None,'PX',{w1:(cb+CSH,5)}))
# member walk: 1 relationships, 2 footnotes, 3 comments, 4 document
on('T3_Z0',(None,'X_C0',{zp:zp0,ztarget:4,obase:OUTB}))
on('T3_ZN',(None,'OPEND',None))
on('T3_ZX',(None,'PX',{oi:0}))
on('T3_ZC',(None,'X_C0',{zp:zp+46+nm+ext+cmt}))
# picture hooks are filled in below
on('T3_PF',(pgdoc,'PX',None),(None,'HALT',None))
on('T3_PQ',(None,'PX',None))
set_chain('T3_PG0',[(IMF,dw),(IMF+1,dh),(IMF+2,imgp),(3684,dw),(3685,dh),(3686,imgp)],'T3_PG1')
on('T3_PG1',(None,'SPLIT',{imgp:dst,oret.r:oret.id('AFTER_ED')}))
