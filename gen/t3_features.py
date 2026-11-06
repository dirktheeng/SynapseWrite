# ---- Tier 3 features, exec'd from app.py ----
net.group('tier3')
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
rbb=R()
on('T3_RBa',(None,'T3_RBb',{rbb:R1,r2:R1+ENDY,rmeta:R1+META}))
e=S('T3_RBb'); shr=net.decode(MT[2],len(PAL_B),e)
def bcr(k): return sum((shr[i_]*PAL_B[i_][k] for i_ in range(len(PAL_B))),X())
on('T3_RBb',(None,'T3_RBc',{rA:(s_tx+MT[1]+1,R2+DOCY-scroll,net.relu(MT[0]-1),net.relu(rowmax-R2),(bcr(0),bcr(1),bcr(2)),0),rB:(s_tx+MT[1],by0,1,rowmax-rowtop,BC,0),rC:(s_tx+MT[1],by0,MT[0]+1,1,BC,0),fa0:MT[0],fa1:MT[1]}))
on('T3_RBc',(None,'RB1',{w1:(rbb+RBOT,rowmax),w2:(rbb+RBOT+1,rowtop),rA:(s_tx+fa1,rowmax+DOCY-scroll,fa0+1,1,BC,0),wht:(as_x(HIT)+hitn*6,s_tx+fa1+fa0-3,by0,s_tx+fa1+fa0+4,rowmax+DOCY-scroll,tiv+1,pi+1-tcols),hitn:hitn+1,tiv:tiv+1,tivx:fa1+fa0}))
# ---- mouse: object hit zones are compared in the network before the pixel hit test ----
tdx=R();tdy=R();tdc=R();tdr=R();tcw=R();tcw2=R()
e=S('T3_H0')
on('T3_H0',(net.ge(vi,hitn,e),'HT',{vi:0}),(None,'T3_H1',{rl:as_x(HIT)+vi*6}))
e=S('T3_H1'); hin=net.and_(net.ge(hx_,RL[0],e),net.lt(hx_,RL[2],e),net.ge(hy_,RL[1],e),net.lt(hy_,RL[3],e),net.or_(net.lt(RL[4],17,e),net.eq(RL[5],cp,e)))
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

# ---- ribbon commands behind button id 54: tab, x and y select the command ----
e=S('T3_BTN'); b3=[]
for tb_,x_,y_,w_,h_,lb_,st_,c_ in t3_btn.BTNS:
    b3.append((net.and_(net.eq(tab,tb_,e),net.ge(hx_,x_,e),net.lt(hx_,x_+w_,e),net.ge(hy_,y_,e),net.lt(hy_,y_+h_,e)),st_,None))
on('T3_BTN',*b3,(None,'HALT',None))

# ---- sections: a paragraph with SECN>0 starts a new section on a new page, record SECN-1 ----
e=S('T3_SB0')
sbadv={**pfsave,ptop:ptop+s_ps,yy:ptop+s_ps+RL[6],pages:pages+1,fnp:0,xcol:0,**sload(RL)}
on('T3_SB0',(full,'T3_SB2',sbadv),(None,'R2X',sbadv))
on('T3_SB2',(None,'T3_PS',{rB:(s_px,ptop+DOCY-scroll,s_pw,s_ph,WHITE,0)}))
sv_i=R();csc=R();swret=t3ret('T3_SWR')
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

sxr=t3ret('T3_SXR')
# ---- zip container: every member carries its name, CRC and size in a table ----
rhf=R();qsec=R();znum=R();zo=R();znl=R();zds=R();zret=t3ret('T3_ZRT');cdoff=R();zk2=R();zL=R();zH=R();zs=R()
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
on('T3_SVB2',(None,'SVP',{spc:0,qsec:0}))
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
on('SVT',(None,'T3_SX',{sxr.r:sxr.id('T3_SVT2')}))
lit('T3_SVT2',b'</w:body></w:document>','T3_Z4e')
zend('T3_Z4e','T3_XM0')
zbegin('T3_Z5',b'word/_rels/document.xml.rels','T3_Z6'); lit('T3_Z6',DRELS0,'T3_RL0'); zend('T3_Z6e','T3_M0')
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
on('T3_Z0',(None,'X_C0',{zp:zp0,ztarget:1,obase:RELB,ob:0}))

# ---- PDF: page size from the section, table rules and shading ----
qcw=R();qsh=R();qrb=R();qrt=R()
qload=lambda W_:{qpw:W_[1],qph:W_[2],qml:W_[4]-W_[3],qmt:W_[6],qth:W_[7],qps:W_[2]+16}
on('T3_PQ0',(None,'T3_PQ1',{rl:as_x(SECB)}))
on('T3_PQ1',(None,'PD_0',qload(RL)))
on('T3_PQ2',(None,'T3_PQ3',{qcw:MT[0],qcx:MT[1],qsh:MT[2],rl:as_x(SECB)+MT[7]*8,r1:qb+RBOT,r2:qb+RBOT+1}))
on('T3_PQ3',(None,'PD_3',{**qload(RL),qrb:R1,qrt:R2,rl:qb+SAVE,rc:qb+2062}))
e=S('PD_4')
on('PD_4',(net.step(qcols),'T3_PT0',None),(None,'T3_PT9',None))
on('T3_PT9',(None,'PD_5',{r1:qb+NLINES}))
e=S('T3_PT0'); hq=net.decode(qsh,len(PAL_B),e)
on('T3_PT0',*[(hq[i_],f'T3_PTc{i_}',None) for i_ in range(1,len(PAL_B))],(None,'T3_PT5',None))
for i_,c_ in enumerate(PAL_B):
    if i_: lit(f'T3_PTc{i_}',('%.3f %.3f %.3f rg '%tuple(v_/255 for v_ in c_)).encode(),'T3_PT1')
def rect_nums(st,nx):
    numz(st,(qml+qcx)*0.75,st+'a'); lit(st+'a',b' ',st+'b'); numz(st+'b',net.relu(qph-qrb+qtop)*0.75,st+'c'); lit(st+'c',b' ',st+'d')
    numz(st+'d',qcw*0.75,st+'e'); lit(st+'e',b' ',st+'f'); numz(st+'f',net.relu(qrb-qrt)*0.75,nx)
rect_nums('T3_PT1','T3_PT2'); lit('T3_PT2',b' re f\n','T3_PT5')
lit('T3_PT5',b'.47 .47 .47 RG .75 w ','T3_PT6'); rect_nums('T3_PT6','T3_PT7'); lit('T3_PT7',b' re S 0 0 0 rg\n','T3_PT9')

# ---- pictures: handles, resize by nearest neighbour resampling in the network ----
IMN=3684
imret=t3ret('T3_RSR')
set_chain('T3_PG0',[(IMF,dw),(IMF+1,dh),(IMF+2,imgp),(IMN,dw),(IMN+1,dh),(IMN+2,imgp)],'T3_PG1')
on('T3_PG1',(None,'SPLIT',{imgp:dst,oret.r:oret.id('AFTER_ED')}))
HC=(43,87,154)
e=S('T3_IH0'); ish_=net.eq(pi,cp,e); shf_=net.and_(ish_,full)
on('T3_IH0',(ish_,'T3_IH1',{rA:(x+pim-8,sy+pih-8,8,8,HC,0),rB:(x+pim-8,sy+pih*0.5-4,8,8,HC,0),rC:(x+pim*0.5-4,sy+pih-8,8,8,HC,0)}),(None,'CB0',None))
on('T3_IH1',(None,'T3_IH2',{rA:(x,sy,pim,1,HC,0),rB:(x,sy+pih-1,pim,1,HC,0),rC:(x,sy,1,pih,HC,0),wht:(as_x(HIT)+hitn*6,x+pim-8,sy+pih-8,x+pim+6,sy+pih+6,19,pi),hitn:hitn+1}))
on('T3_IH2',(None,'T3_IH3',{rA:(x+pim-1,sy,1,pih,HC,0),wht:(as_x(HIT)+hitn*6,x+pim-8,sy+pih*0.5-7,x+pim+6,sy+pih*0.5+7,17,pi),hitn:hitn+1}))
on('T3_IH3',(None,'CB0',{wht:(as_x(HIT)+hitn*6,x+pim*0.5-7,sy+pih-8,x+pim*0.5+7,sy+pih+6,18,pi),hitn:hitn+1}))
e=S('RE1'); dgi=net.and_(e,net.ge(tdk,17,e))
rB.drive(dgi,(tmx,DOCY,1,VH,HC,0)); rC.drive(dgi,(0,tmy,1262,1,HC,0)) if False else None
rs_w=R();rs_h=R();rs_a=R();rs_sw=R();rs_sh=R();rs_sa=R();rs_ex=R();rs_ey=R();rs_x=R();rs_y=R();rs_p=R();rs_row=R();rsd=R()
tk3=R()
fsm.set(tmy,net.and_(S('T3_MU'),net.step(tdk)),evb)
on('T3_IMU',(None,'T3_IM1',{tk3:tdk,tdk:0,tmx:eva,rmeta:cb+META,rim:cb+IMF,r1:cb+IMN,r2:cb+IMN+1,rc:cb+IMN+2}))
e=S('T3_IM1'); hk=net.decode(tk3-17,3,e); kw=hk[0]+hk[2]; kh2=hk[1]
W0=rim.out[0];H0=rim.out[1]
nw=net.min_(net.max_(W0+tmx-tdx,16),s_tw); nh=net.max_(H0+tmy-tdy,16)
on('T3_IM1',(net.ge(imgp,7400000,e),'RD0',None),(None,'T3_IM2',{rs_sw:R1,rs_sh:R2,rs_sa:rc.out[0],rs_w:G_(nw,kw)+G_(W0,e-kw),rs_h:G_(nh,kh2)+G_(H0,e-kh2),rs_a:imgp,fa0:W0,fa1:H0,fa2:hk[2]}))
# a corner drag keeps the aspect ratio: h = H0*w/W0 by repeated addition
e=S('T3_IM2')
on('T3_IM2',(net.step(fa2),'T3_IM3',{rs_x:0,rs_ex:0,rs_y:0}),(None,'T3_IM5',None))
e=S('T3_IM3')
on('T3_IM3',(net.ge(rs_x,rs_w,e),'T3_IM5',{rs_h:net.max_(rs_y,16)}),(None,'T3_IM4',{rs_x:rs_x+1,rs_ex:rs_ex+fa1}))
e=S('T3_IM4')
on('T3_IM4',(net.ge(rs_ex,fa0,e),'T3_IM4',{rs_ex:rs_ex-fa0,rs_y:rs_y+1}),(None,'T3_IM3',None))
on('T3_IM5',(None,'T3_RS9',{imret.r:imret.id('T3_IM6')}))
on('T3_IM6',(None,'T3_IM7',{grp:grp+1}))
set_chain('T3_IM7',[(IMF,rs_w),(IMF+1,rs_h),(IMF+2,rs_a)],'T3_IM8')
on('T3_IM8',(None,'AFTER_ED',None))
# resample: source rs_sa (rs_sw x rs_sh) to destination at imgp (rs_w x rs_h); imgp advances
on('T3_RS9',(None,'T3_RSa',{rs_y:0,rs_ey:0,rs_row:rs_sa,rsd:imgp}))
e=S('T3_RSa')
on('T3_RSa',(net.ge(rs_y,rs_h,e),'T3_RSR',{imgp:rsd}),(None,'T3_RSb',{rs_x:0,rs_ex:0,rs_p:rs_row}))
e=S('T3_RSb')
on('T3_RSb',(net.ge(rs_x,rs_w,e),'T3_RSf',{rs_ey:rs_ey+rs_sh}),(None,'T3_RSc',{r1:as_x(IMG0)+rs_p}))
on('T3_RSc',(None,'T3_RSd',{w1:(as_x(IMG0)+rsd,R1),rsd:rsd+1,rs_x:rs_x+1,rs_ex:rs_ex+rs_sw}))
e=S('T3_RSd')
on('T3_RSd',(net.ge(rs_ex,rs_w,e),'T3_RSd',{rs_ex:rs_ex-rs_w,rs_p:rs_p+1}),(None,'T3_RSb',None))
e=S('T3_RSf')
on('T3_RSf',(net.ge(rs_ey,rs_h,e),'T3_RSf',{rs_ey:rs_ey-rs_h,rs_row:rs_row+rs_sw}),(None,'T3_RSa',{rs_y:rs_y+1}))
rw_b=R();idl=R();mr_=R();mx_=R();as1=R();as2=R();aux_l=R();mzret=R()
# ---- pictures in .docx: the drawing element, relationships, and a PNG written by the network ----
A_NS=b'http://schemas.openxmlformats.org/drawingml/2006/main'; P_NS=b'http://schemas.openxmlformats.org/drawingml/2006/picture'
simg=R();mq=R();cpad=R()
def pad3(st,val,nx):
    "Three zero padded digits."
    e=S(st); v0=net.gate(val,e); h_=X()
    for t in range(1,10): h_=h_+net.step(v0-100*t+0.5)
    em_en.lin(e); em_b.add(e,48+h_); on(st,(None,st+'t',None))
    e=S(st+'t'); v0=net.gate(val,e); h_=X()
    for t in range(1,10): h_=h_+net.step(v0-100*t+0.5)
    r0=v0-h_*100; t_=X()
    for t in range(1,10): t_=t_+net.step(r0-10*t+0.5)
    em_en.lin(e); em_b.add(e,48+t_); on(st+'t',(None,st+'u',None))
    e=S(st+'u'); v0=net.gate(val,e); h_=X()
    for t in range(1,10): h_=h_+net.step(v0-100*t+0.5)
    r0=v0-h_*100; t_=X()
    for t in range(1,10): t_=t_+net.step(r0-10*t+0.5)
    em_en.lin(e); em_b.add(e,48+r0-t_*10); on(st+'u',(None,nx,None))
lit('T3_SD0',b'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="','T3_SD1')
numz('T3_SD1',pim*9525,'T3_SD2'); lit('T3_SD2',b'" cy="','T3_SD3'); numz('T3_SD3',pih*9525,'T3_SD4')
lit('T3_SD4',b'"/><wp:docPr id="','T3_SD5'); numz('T3_SD5',simg+1,'T3_SD6')
lit('T3_SD6',b'" name="Picture"/><a:graphic xmlns:a="'+A_NS+b'"><a:graphicData uri="'+P_NS+b'"><pic:pic xmlns:pic="'+P_NS+b'"><pic:nvPicPr><pic:cNvPr id="0" name="image"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="rIdI','T3_SD7')
pad3('T3_SD7',simg,'T3_SD8')
lit('T3_SD8',b'"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off_ x="0" y="0"/><a:ext cx="','T3_SD9')
numz('T3_SD9',pim*9525,'T3_SDa'); lit('T3_SDa',b'" cy="','T3_SDb'); numz('T3_SDb',pih*9525,'T3_SDc')
lit('T3_SDc',b'"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>','T3_SDd')
on('T3_SDd',(None,'SVe',{simg:simg+1}))
fsm.set(simg,S('SAVE'),0)
on('T3_RL0',(None,'T3_RL1',{mq:0,simg:0}))
e=S('T3_RL1')
on('T3_RL1',(net.ge(mq,npar,e),'T3_RL9',None),(None,'T3_RL2',{r1:as_x(PT)+mq}))
on('T3_RL2',(None,'T3_RL3',{r2:R1+IMF}))
e=S('T3_RL3')
on('T3_RL3',(net.step(R2),'T3_RL4',None),(None,'T3_RL1',{mq:mq+1}))
lit('T3_RL4',b'<Relationship Id="rIdI','T3_RL5'); pad3('T3_RL5',simg,'T3_RL6')
lit('T3_RL6',b'" Type="'+RTYPE+b'image" Target="media/image','T3_RL7'); pad3('T3_RL7',simg,'T3_RL8')
lit('T3_RL8',b'.png"/>','T3_RLa'); on('T3_RLa',(None,'T3_RL1',{mq:mq+1,simg:simg+1}))
lit('T3_RL9',b'</Relationships>','T3_Z6e')
# second CRC over the same byte stream, for PNG chunks
crc2=[R(1) for _ in range(32)]; crc2i=Bus(net)
gc2=[net.gate(c_,ens) for c_ in crc2]
rows2=[[] for _ in range(32)]
for i in range(32):
    o=crc_next(1<<i,0)
    for j in range(32):
        if o>>j&1: rows2[j].append(gc2[i])
for i in range(8):
    o=crc_next(0,1<<i)
    for j in range(32):
        if o>>j&1: rows2[j].append(bb[i])
for j in range(32):
    sm_=X()
    for t_ in rows2[j]: sm_=sm_+t_
    par=X()
    for k_ in range(1,len(rows2[j])+1): par=par+net.step(sm_-k_+0.5)*(1 if k_%2 else -1)
    fsm.set(crc2[j],ens,par); fsm.set(crc2[j],crc2i.w,1)
c2L=X();c2H=X()
for j,c_ in enumerate(crc2):
    if j<16: c2L=c2L+c_*(1<<j)
    else: c2H=c2H+c_*(1<<(j-16))
c2fL=R();c2fH=R()
def be_emit(st,val,nx,n=4):
    cur=st
    for i_ in reversed(range(n)):
        nx_=f'{st}_{i_}' if i_ else nx
        e=S(cur); em_en.lin(e); em_b.add(e,le_bytes(val,e,4)[i_]); on(cur,(None,nx_,None)); cur=nx_
def crc_emit(st,nx):
    on(st,(None,st+'a',{c2fL:as_x(65535)-c2L,c2fH:as_x(65535)-c2H}))
    cur=st+'a'
    for i_,(v_,b_) in enumerate(((c2fH,1),(c2fH,0),(c2fL,1),(c2fL,0))):
        nx_=f'{st}b{i_}' if i_<3 else nx
        e=S(cur); em_en.lin(e); em_b.add(e,le_bytes(v_,e,2)[b_]); on(cur,(None,nx_,None)); cur=nx_
# media member per picture paragraph
on('T3_M0',(None,'T3_M1',{mq:0,simg:0}))
e=S('T3_M1')
on('T3_M1',(net.ge(mq,npar,e),'T3_CD0',None),(None,'T3_M2',{r1:as_x(PT)+mq}))
on('T3_M2',(None,'T3_M3',{rim:R1+IMF}))
e=S('T3_M3')
on('T3_M3',(net.step(rim.out[0]),'T3_M4',{pim:rim.out[0],pih:rim.out[1],pio:rim.out[2]}),(None,'T3_M1',{mq:mq+1}))
MNAME0=b'word/media/image'
on('T3_M4',(None,'T3_M5',{zo:fp,znl:len(MNAME0)+7}))
lit('T3_M5',struct.pack('<IHHHHHIIIHH',0x04034b50,20,0,0,0,0x21,0,0,0,len(MNAME0)+7,0)+MNAME0,'T3_M6')
pad3('T3_M6',simg,'T3_M7'); lit('T3_M7',b'.png','T3_M8')
crci.lin(S('T3_M8'))
on('T3_M8',(None,'T3_GP0',{zds:fp,rw_b:pim*3+1}))
# PNG signature, IHDR
lit('T3_GP0',bytes([0x89,80,78,71,13,10,26,10,0,0,0,13]),'T3_GP1')
crc2i.lin(S('T3_GP1'))
lit('T3_GP1',b'IHDR','T3_GP2'); be_emit('T3_GP2',pim,'T3_GP3'); be_emit('T3_GP3',pih,'T3_GP4')
lit('T3_GP4',bytes([8,2,0,0,0]),'T3_GP5'); crc_emit('T3_GP5','T3_GP6')
on('T3_GP6',(None,'T3_GP7',{idl:6,mr_:0}))
e=S('T3_GP7')
on('T3_GP7',(net.ge(mr_,pih,e),'T3_GP8',None),(None,'T3_GP7',{idl:idl+rw_b+5,mr_:mr_+1}))
be_emit('T3_GP8',idl,'T3_GP9')
crc2i.lin(S('T3_GP9'))
lit('T3_GP9',b'IDAT','T3_GPa'); lit('T3_GPa',bytes([0x78,1]),'T3_GPb')
on('T3_GPb',(None,'T3_GPc',{mr_:0,as1:1,as2:0,rs_p:pio}))
e=S('T3_GPc')
on('T3_GPc',(net.ge(mr_,pih,e),'T3_GPz',None),(net.ge(mr_+1,pih,e),'T3_GPd1',None),(None,'T3_GPd0',None))
lit('T3_GPd0',bytes([0]),'T3_GPe'); lit('T3_GPd1',bytes([1]),'T3_GPe')
cur_='T3_GPe'
for i_,exprs in enumerate(('l0','l1','n0','n1')):
    nx_=f'T3_GPf{i_}'; e=S(cur_)
    vv=le_bytes(rw_b,e,2) if exprs[0]=='l' else le_bytes(as_x(65535)-rw_b,e,2)
    em_en.lin(e); em_b.add(e,vv[int(exprs[1])]); on(cur_,(None,nx_,None)); cur_=nx_
def adl(e,b_):
    n1=as1+b_; o1=net.ge(n1,65521,e); v1=net.gate(n1,e)-o1*65521
    n2=as2+v1; o2=net.ge(n2,65521,e); v2=net.gate(n2,e)-o2*65521
    fsm.set(as1,e,v1); fsm.set(as2,e,v2)
e=S(cur_); em_en.lin(e); em_b.add(e,0) if False else None; adl(e,0)
on(cur_,(None,'T3_GPg',{mx_:0}))
e=S('T3_GPg')
on('T3_GPg',(net.ge(mx_,pim,e),'T3_GPc',{mr_:mr_+1}),(None,'T3_GPh',{r1:as_x(IMG0)+rs_p}))
e=S('T3_GPh'); pb_i=net.bits(R1,24,e)
pR=sum((pb_i[16+k_]*(1<<k_) for k_ in range(8)),X());pG=sum((pb_i[8+k_]*(1<<k_) for k_ in range(8)),X());pB=sum((pb_i[k_]*(1<<k_) for k_ in range(8)),X())
on('T3_GPh',(None,'T3_GPi',{fa0:pR,fa1:pG,fa2:pB,rs_p:rs_p+1,mx_:mx_+1}))
for st_,nx_,v_ in (('T3_GPi','T3_GPj',fa0),('T3_GPj','T3_GPk',fa1),('T3_GPk','T3_GPg',fa2)):
    e=S(st_); em_en.lin(e); em_b.add(e,v_); adl(e,v_); on(st_,(None,nx_,None))
be_emit('T3_GPz',as2*65536+as1,'T3_GPy')
crc_emit('T3_GPy','T3_GPx')
lit('T3_GPx',bytes([0,0,0,0])+b'IEND'+bytes([0xAE,0x42,0x60,0x82]),'T3_GPw')
zend('T3_GPw','T3_GPv')
on('T3_GPv',(None,'T3_M1',{mq:mq+1,simg:simg+1}))
# ---- reading pictures: extent, relationship lookup, member lookup, PNG decode ----
ext_w=R();ext_h=R();rq=R();rid_n=R();rok=R();tgt=R();tl=R();sob=R();soi=R();ri_=R();RIDB=23700;rels_l=R();ztl=R()
on('T3_EX0',(None,'T3_NA',{nmret.r:nmret.id('T3_EX1')}))
on('T3_EX1',(None,'T3_NA',{ext_w:floorv(aval*(1.0/9525)+0.5,S('T3_EX1')),nmret.r:nmret.id('T3_EX2')}))
on('T3_EX2',(None,'PX',{ext_h:floorv(aval*(1.0/9525)+0.5,S('T3_EX2'))}))
on('T3_BL0',(None,'T3_BL1',{rl:OA+oi}))
e=S('T3_BL1')
on('T3_BL1',(pat('r:embed=',e),'T3_BL2',{oi:oi+9,rid_n:0}),(net.eq(W[0],62,e),'PX',None),(None,'T3_BL0',{oi:oi+1}))
on('T3_BL2',(None,'T3_BL3',{r1:OA+oi}))
e=S('T3_BL3')
on('T3_BL3',(net.eq(R1,34,e),'T3_BR0',{rq:0}),(None,'T3_BL2',{w1:(as_x(RIDB)+rid_n,R1),rid_n:rid_n+1,oi:oi+1}))
rlb=as_x(RELB); ridret=t3ret('T3_RIR')
# find the target of relationship rid in the relationships part; tgt and tl give the string
on('T3_BR0',(None,'T3_BR1',{ridret.r:ridret.id('T3_BM0')}))
on('T3_BR1',(None,'T3_BR2',{rl:rlb+rq}))
e=S('T3_BR2')
on('T3_BR2',(net.ge(rq,rels_l,e),'T3_RIF',None),(pat('<Relatio',e),'T3_BR3',{rq:rq+13,rok:0,tgt:0}),(None,'T3_BR1',{rq:rq+1}))
on('T3_BR3',(None,'T3_BR4',{rl:rlb+rq}))
e=S('T3_BR4')
on('T3_BR4',(net.eq(W[0],62,e),'T3_BR9',None),(pat(' Id="',e),'T3_BC0',{rq:rq+5,ri_:0}),(pat('Target="',e),'T3_BR3',{tgt:rq+8,rq:rq+8}),(None,'T3_BR3',{rq:rq+1}))
on('T3_BC0',(None,'T3_BC1',{r1:rlb+rq+ri_,r2:as_x(RIDB)+ri_}))
e=S('T3_BC1')
on('T3_BC1',(net.ge(ri_,rid_n,e),'T3_BR3',{rok:net.eq(R1,34,e),rq:rq+ri_}),(net.eq(R1,R2,e),'T3_BC0',{ri_:ri_+1}),(None,'T3_BR3',{rok:0}))
e=S('T3_BR9')
on('T3_BR9',(net.and_(rok,net.step(tgt)),'T3_BT0',{tl:0}),(None,'T3_BR1',None))
on('T3_BT0',(None,'T3_BT1',{r1:rlb+tgt+tl}))
e=S('T3_BT1')
on('T3_BT1',(net.eq(R1,34,e),'T3_BT2',{r1:rlb+tgt}),(None,'T3_BT0',{tl:tl+1}))
e=S('T3_BT2')
on('T3_BT2',(net.eq(R1,47,e),'T3_RIR',{tgt:tgt+1,tl:tl-1}),(None,'T3_RIR',None))
on('T3_RIF',(None,'PX',{rhf:0}))
# member with a name ending in the target
on('T3_BM0',(None,'X_C0',{zp:zp0,ztarget:5,sob:ob,soi:oi,obase:G_(as_x(PNGB),ONE-rhf)+G_(as_x(AUXB),rhf),ob:0,mzret:1}))
on('T3_ZC',(net.lt(nm,tl,S('T3_ZC')),'X_C0',{zp:zp+46+nm+ext+cmt}),(None,'T3_ZC1',{zk:0}))
e=S('T3_ZC1')
on('T3_ZC1',(net.ge(zk,tl,e),'C7',{rl:FA+loff+26}),(None,'T3_ZC2',{r1:FA+zp+46+nm-tl+zk,r2:rlb+tgt+zk}))
e=S('T3_ZC2')
on('T3_ZC2',(net.eq(R1,R2,e),'T3_ZC1',{zk:zk+1}),(None,'X_C0',{zp:zp+46+nm+ext+cmt}))
mzret_h=None
e=S('T3_ZN'); zh=net.decode(ztarget,6,e)
ZN={ob:0}
on('T3_ZN',(zh[1],'T3_Z2n',None),(zh[2],'T3_Z3n',None),(zh[3],'T3_Z4n',None),(zh[5],'T3_ZNe',None),(None,'OPEND',None))
on('T3_ZNe',(None,'PX',{ob:sob,oi:soi,obase:OUTB}))
e=S('T3_ZX'); zh2=net.decode(ztarget,6,e)
on('T3_ZX',(zh2[1],'T3_Z2n',{rels_l:ob}),(zh2[2],'T3_FN0',{aux_l:ob}),(zh2[3],'T3_CM0',{aux_l:ob}),(net.and_(zh2[5],ONE-rhf),'T3_ZP',{pgl:ob}),(net.and_(zh2[5],rhf),'T3_HP0',{aux_l:ob}),(None,'PX',{oi:0}))
on('T3_ZP',(None,'PG_1',{rl:as_x(PNGB),pbase:PNGB,pgdoc:1}))
on('T3_PF',(pgdoc,'T3_PF2',{ob:sob,oi:soi,obase:OUTB,pgdoc:0}),(None,'HALT',None))
on('T3_PF2',(None,'PX',None))
on('T3_PQ',(None,'T3_PQa',{ob:sob,oi:soi,obase:OUTB,pgdoc:0,rs_sw:dw,rs_sh:dh,rs_sa:imgp,rs_w:G_(ext_w,net.step(ext_w))+G_(dw,ONE-net.step(ext_w)),rs_h:G_(ext_h,net.step(ext_h))+G_(dh,ONE-net.step(ext_h)),imgp:dst}))
on('T3_PQa',(None,'T3_PQb',{w1:(cb+IMN,rs_sw),w2:(cb+IMN+1,rs_sh),w3:(cb+IMN+2,rs_sa),w4:(cb+DIRTY,1)}))
e=S('T3_PQb'); same_=net.and_(net.eq(rs_w,rs_sw,e),net.eq(rs_h,rs_sh,e))
on('T3_PQb',(same_,'T3_PQd',{rs_a:rs_sa}),(None,'T3_RS9',{rs_a:imgp,imret.r:imret.id('T3_PQd')}))
on('T3_PQd',(None,'PX',{wl_i:(cb+IMF,rs_w,rs_h,rs_a),ext_w:0,ext_h:0}))

on('T3_Z2n',(None,'X_C0',{zp:zp0,ztarget:2,obase:AUXB,ob:0}))
on('T3_Z3n',(None,'X_C0',{zp:zp0,ztarget:3,obase:AUXB,ob:0}))
on('T3_Z4n',(None,'X_C0',{zp:zp0,ztarget:4,obase:OUTB,ob:0}))
# ---- wrapped text, count only or drawn, for footnotes and balloons ----
ws_=R();wi_=R();wx_=R();wlb_=R();wend=R();wcnt=R()
on('T3_W',(None,'T3_W1',{ws_:0,wcnt:0}))
on('T3_W1',(None,'T3_W2',{wi_:ws_,wx_:0,wlb_:ws_}))
e=S('T3_W2')
on('T3_W2',(net.ge(wi_,wl_,e),'T3_WD',{wend:wl_}),(None,'T3_W3',{r1:wb_+wi_}))
e=S('T3_W3'); measure(e,R1,9)
ov_=net.gt(wx_+adv,wdw,e); spw=net.eq(R1,32,e)
fsm.set(wlb_,net.and_(spw,ONE-ov_),wi_+1)
on('T3_W3',(net.and_(ov_,net.gt(wlb_,ws_,e)),'T3_WD',{wend:wlb_}),(ov_,'T3_WD',{wend:net.max_(wi_,ws_+1)}),(None,'T3_W2',{wx_:wx_+adv,wi_:wi_+1}))
e=S('T3_WD')
on('T3_WD',(wdd,'T3_WE',{wi_:ws_,sx:wdx}),(None,'T3_WF',None))
e=S('T3_WE')
on('T3_WE',(net.ge(wi_,wend,e),'T3_WF',None),(None,'T3_WG',{r1:wb_+wi_}))
e=S('T3_WG')
g_en.lin(e);g_draw.lin(e-net.eq(R1,32,e));g_ch.add(e,R1);g_st.add(e,9);g_x.add(e,sx);g_y.add(e,wdy+YB);fg[0].lin(e);bg[0].lin(net.and_(e,ONE-wbgf));bg[2].lin(net.and_(e,wbgf))
on('T3_WG',(None,'T3_WE',{sx:sx+adv,wi_:wi_+1}))
e=S('T3_WF')
on('T3_WF',(net.ge(wend,wl_,e),'T3_WR',{wcnt:wcnt+1,wdy:wdy+16}),(None,'T3_W1',{wcnt:wcnt+1,wdy:wdy+16,ws_:wend}))
# balloon: count lines, fill, draw
on('T3_CB2',(None,'T3_W',None))
on('T3_CB3',(None,'T3_CB4',{rA:(1044,sy,214,wcnt*16+6,PAL_B[2],0),rB:(s_tx+s_tw,sy+8,net.relu(as_x(1044)-s_tx-s_tw),1,(200,170,60),0),wdy:sy+3,wdd:1,wret_.r:wret_.id('R9')}))
on('T3_CB4',(None,'T3_W',None))
set_chain('T3_C_CD0',[(CMTL,0)],'AFTER_ED')
on('T3_C_CD',(None,'T3_C_CD0',{grp:grp+1}))
# ---- footnotes: reference char 1000+id in the text, text in a store, drawn at the page foot ----
fed=R();fedb=R();flen=R()
e=S('T3_C_FN')
on('T3_C_FN',(net.step(co),'T3_FN1',{r1:cb+co-1}),(None,'T3_FN3',None))
e=S('T3_FN1')
on('T3_FN1',(net.ge(R1,1000,e),'T3_FN5',{fed:R1-1000,r2:as_x(FNB)+(R1-1000)*256+255}),(None,'T3_FN3',None))
on('T3_FN5',(None,'T3_FN2',{flen:R2,fedb:as_x(FNB)+fed*256}))
on('T3_FN3',(has_sel,'RD0',None),(None,'T3_FN4',{fnc:fnc+1,grp:grp+1,flen:0}))
on('T3_FN4',(None,'INS',{w1:(as_x(FNB)+fnc*256+254,16),w2:(as_x(FNB)+fnc*256+255,0),fed:fnc,fedb:as_x(FNB)+fnc*256,ins_ch:fnc+1000,ins_st:ty,oret.r:oret.id('T3_FN2')}))
on('T3_FN2',(None,'AFTER_ED',{mode:5,field:0}))
on('FNE',(None,'RD0',{lc:1,dfrom:net.relu(cp-1),w1:(cb+DIRTY,1)}))
on('FNc',(None,'T3_FR',{flen:net.relu(flen-1)}))
on('FNa',(net.ge(flen,250,S('FNa')),'RD0',None),(None,'T3_FR',{w1:(fedb+flen,eva),flen:flen+1}))
on('T3_FR',(None,'T3_W',{wl_:flen,wb_:fedb,wdw:s_tw-22,wdd:0,wdx:0,wdy:0,wbgf:0,wret_.r:wret_.id('T3_FS9')}))
on('T3_FS9',(None,'RD0',{w1:(fedb+254,wcnt*16),w2:(fedb+255,flen),w3:(cb+DIRTY,1),lc:1,dfrom:net.relu(cp-1)}))
# layout of a marker: fixed width, adds its note height to the line
e=S('T3_LF0'); lasm=net.ge(off_+1,plen_,e)
on('T3_LF0',(lasm,'EM',{lfh:lfh+R1,lfn:lfn+1,lend:off_+1,lwid:lx+8,lspc:lsn,llast:1,off_:off_+1}),(None,'L1',{lfh:lfh+R1,lfn:lfn+1,lx:lx+8,off_:off_+1,prevsp:0}))
# lines with markers push note ids in document order
fsi=R();fsc=R()
on('T3_R6X',(net.step(lnfh),'T3_FS0',{fsi:ls_,fsc:0}),(None,'R7',None))
e=S('T3_FS0')
on('T3_FS0',(net.ge(fsi,le_,e),'T3_FSE',None),(None,'T3_FS1',{r1:pbs+fsi}))
e=S('T3_FS1')
on('T3_FS1',(net.ge(R1,1000,e),'T3_FS2',{w1:(as_x(FORD)+fnn,R1-1000),r2:as_x(FNB)+(R1-1000)*256+254,fsi:fsi+1}),(None,'T3_FS0',{fsi:fsi+1}))
on('T3_FS2',(None,'T3_FS0',{fnh:fnh+R2,fnn:fnn+1,fnp:fnp+1,fsc:fsc+1}))
on('T3_FSE',(None,'R7',{dnum:fnn-fsc+1}))
# marker glyphs
def two(v,e_):
    b_=net.gate(v,e_); t_=_t10(v,e_); return t_,b_-t_*10
e=S('T3_CF0'); t_,u_=two(dnum,e)
on('T3_CF0',(net.ge(dnum,10,e),'T3_CF1',{rA:(x,sy,8,lhh,(bc0,bc1,bc2),col),gly:(48+t_,9,x-2,sy-3,0,0),x:x+5}),(None,'T3_CF1',{rA:(x,sy,8,lhh,(bc0,bc1,bc2),col)}))
e=S('T3_CF1'); t_,u_=two(dnum,e)
on('T3_CF1',(None,'C0',{gly:(48+u_,9,x-2,sy-3,0,0),x:x+8-net.ge(dnum,10,e)*5,col:col+1,off_:off_+1,dnum:dnum+1}))
# page foot: separator, then each note of the page in order
fk=R();fbase=R();fid=R();ftail=R()
e=S('T3_PFT')
on('T3_PFT',(net.and_(net.step(pfc),full),'T3_FT0',{fk:0,wdy:pfy-pfh+DOCY-scroll,ftail:1,rA:(pfx,pfy-pfh-6+DOCY-scroll,200,1,(120,120,120),0)}),(None,'T3_HD0',None))

on('T3_PFE',(None,'T3_FT0',{fk:0,wdy:pfy-pfh+DOCY-scroll,ftail:0,rA:(pfx,pfy-pfh-6+DOCY-scroll,200,1,(120,120,120),0)}))
e=S('T3_FT0')
on('T3_FT0',(net.ge(fk,pfc,e),'T3_FTE',{pfc:0}),(None,'T3_FT1',{r1:as_x(FORD)+pff+fk}))
on('T3_FT1',(None,'T3_FT2',{fbase:as_x(FNB)+R1*256,r2:as_x(FNB)+R1*256+255}))
e=S('T3_FT2'); t_,u_=two(pff+fk+1,e)
on('T3_FT2',(net.ge(pff+fk+1,10,e),'T3_FT3',{wl_:R2,gly:(48+t_,9,pfx,wdy,0,0)}),(None,'T3_FT3',{wl_:R2}))
e=S('T3_FT3'); t_,u_=two(pff+fk+1,e)
on('T3_FT3',(None,'T3_W',{gly:(48+u_,9,pfx+6,wdy,0,0),wb_:fbase,wdx:pfx+20,wdw:pfw-22,wdd:1,wbgf:0,fk:fk+1,wret_.r:wret_.id('T3_FT0')}))
on('T3_FTE',(ftail,'T3_HD0',None),(None,'RE0',None))
# ---- headers and footers: four strings, char 1 is the page number field ----
hk_=R();hi_=R();hdy=R();hdb=R();hdl=R();hstep=R()
e=S('T3_HD0'); first_=net.and_(hftp,net.eq(pages,1,e))
on('T3_HD0',(first_,'T3_HD1',{hdb:as_x(HFB)+256,hdl:hfl[1],hi_:0,sx:s_tx,hdy:ptop+48+DOCY-scroll,hstep:0}),(None,'T3_HD1',{hdb:as_x(HFB),hdl:hfl[0],hi_:0,sx:s_tx,hdy:ptop+48+DOCY-scroll,hstep:0}))
e=S('T3_HD1')
on('T3_HD1',(net.ge(hi_,hdl,e),'T3_HD5',None),(None,'T3_HD2',{r1:hdb+hi_}))
e=S('T3_HD2')
on('T3_HD2',(net.eq(R1,1,e),'T3_HN0',{hi_:hi_+1}),(None,'T3_HD1',{gly:(R1,9,sx,hdy,1,0),sx:sx+adv,hi_:hi_+1}))
e=S('T3_HN0'); v_=net.gate(pages,e); h3=X()
for t in range(1,10): h3=h3+net.step(v_-100*t+0.5)
on('T3_HN0',(net.ge(pages,100,e),'T3_HN1',{gly:(48+h3,9,sx,hdy,1,0),sx:sx+adv}),(None,'T3_HN1',None))
e=S('T3_HN1'); v_=net.gate(pages,e); h3=X()
for t in range(1,10): h3=h3+net.step(v_-100*t+0.5)
r3=v_-h3*100; t3=X()
for t in range(1,10): t3=t3+net.step(r3-10*t+0.5)
on('T3_HN1',(net.ge(pages,10,e),'T3_HN2',{gly:(48+t3,9,sx,hdy,1,0),sx:sx+adv}),(None,'T3_HN2',None))
e=S('T3_HN2'); v_=net.gate(pages,e); h3=X()
for t in range(1,10): h3=h3+net.step(v_-100*t+0.5)
r3=v_-h3*100; t3=X()
for t in range(1,10): t3=t3+net.step(r3-10*t+0.5)
on('T3_HN2',(None,'T3_HD1',{gly:(48+r3-t3*10,9,sx,hdy,1,0),sx:sx+adv}))
e=S('T3_HD5'); first_=net.and_(hftp,net.eq(pages,1,e))
on('T3_HD5',(net.step(hstep),'T3_PGR',None),(first_,'T3_HD1',{hstep:1,hdb:as_x(HFB)+768,hdl:hfl[3],hi_:0,sx:s_tx,hdy:ptop+s_ph-60+DOCY-scroll}),(None,'T3_HD1',{hstep:1,hdb:as_x(HFB)+512,hdl:hfl[2],hi_:0,sx:s_tx,hdy:ptop+s_ph-60+DOCY-scroll}))
# edit one of the four strings in the mode 3 bar
def hedit(st,k_,tp=None):
    acts={hfk:k_,hfb:as_x(HFB)+k_*256,hlen_:hfl[k_],mode:3}
    if tp: acts[hftp]=1
    on(st,(None,'RD0',acts))
hedit('T3_C_H0',0);hedit('T3_C_F0',2);hedit('T3_C_H1',1,1);hedit('T3_C_F1',3,1)
on('T3_C_NF',(None,'RD0',{hftp:0,lc:1}))
on('T3_C_PG',(net.eq(mode,3,S('T3_C_PG')),'RD0',{w1:(hfb+hlen_,1),hlen_:hlen_+1}),(None,'RD0',None))
e=S('T3_HE'); hh_=net.decode(hfk,4,e)
for i_ in range(4): fsm.set(hfl[i_],hh_[i_],hlen_)
on('T3_HE',(None,'RD0',None))
# ---- table of contents ----
on('T3_TC0x',(None,'T3_TC1x',None))
set_chain('T3_TC1x',[(TOCF,tlev),(TSRC,tbase)],'TCG')
e=S('TCG'); adj=net.gt(ti_,cp,e)
on('TCG',(None,'SPLIT',{ti_:ti_+1+adj,oret.r:oret.id('TC1')}))
e=S('T3_TD0')
on('T3_TD0',(None,'T3_TD1',{r1:ptsrc+SAVE+2}))
e=S('T3_TD1'); hs=net.step(ptsrc)
tval=G_(R1,hs)+G_(ptpg,ONE-hs)
DW0=rom.glyph(0,0,0,0,48)[0]; DOTW=rom.glyph(0,0,0,0,46)[0]+2
tdg=R(); tpv=R(); txe=R()
n3=net.ge(tval,10,e)+net.ge(tval,100,e)+1
on('T3_TD1',(None,'T3_TD2',{tpv:tval,txe:s_tx+s_tw-n3*DW0-4}))
e=S('T3_TD2')
on('T3_TD2',(net.ge(x+DOTW,txe,e),'T3_TN0',{sx:txe+4}),(None,'T3_TD2',{gly:(46,0,x,gly_y,0,0),x:x+DOTW}))
e=S('T3_TN0'); v_=net.gate(tpv,e); h3=X()
for t in range(1,10): h3=h3+net.step(v_-100*t+0.5)
on('T3_TN0',(net.ge(tpv,100,e),'T3_TN1',{gly:(48+h3,0,sx,gly_y,0,0),sx:sx+DW0}),(None,'T3_TN1',None))
e=S('T3_TN1'); v_=net.gate(tpv,e); h3=X()
for t in range(1,10): h3=h3+net.step(v_-100*t+0.5)
r3=v_-h3*100; t3=X()
for t in range(1,10): t3=t3+net.step(r3-10*t+0.5)
on('T3_TN1',(net.ge(tpv,10,e),'T3_TN2',{gly:(48+t3,0,sx,gly_y,0,0),sx:sx+DW0}),(None,'T3_TN2',None))
e=S('T3_TN2'); v_=net.gate(tpv,e); h3=X()
for t in range(1,10): h3=h3+net.step(v_-100*t+0.5)
r3=v_-h3*100; t3=X()
for t in range(1,10): t3=t3+net.step(r3-10*t+0.5)
on('T3_TN2',(None,'R9',{gly:(48+r3-t3*10,0,sx,gly_y,0,0)}))
# update: clear the flags on the first run of entries, delete it, rebuild at that place
tu0=R();tu1=R()
on('T3_C_TU',(None,'T3_TU1',{tq:0,grp:grp+1}))
e=S('T3_TU1')
on('T3_TU1',(net.ge(tq,npar,e),'RD0',None),(None,'T3_TU2',{r1:as_x(PT)+tq}))
on('T3_TU2',(None,'T3_TU3',{r2:R1+TOCF}))
e=S('T3_TU3')
on('T3_TU3',(net.step(R2),'T3_TU4',{tu0:tq}),(None,'T3_TU1',{tq:tq+1}))
e=S('T3_TU4')
on('T3_TU4',(net.ge(tq,npar,e),'T3_TU8',None),(None,'T3_TU5',{r1:as_x(PT)+tq}))
on('T3_TU5',(None,'T3_TU6',{r2:R1+TOCF}))
e=S('T3_TU6')
on('T3_TU6',(net.step(R2),'T3_TU7',{jp:tq,jo:0,jret.r:jret.id('T3_TU7b')}),(None,'T3_TU8',None))
on('T3_TU7',(None,'J0',None))
set_chain('T3_TU7b',[(TOCF,0),(TSRC,0),(TPG,0)],'T3_TU7c')
on('T3_TU7c',(None,'T3_TU4',{tq:tq+1}))
e=S('T3_TU8')
on('T3_TU8',(None,'T3_TU9',{jp:tu0,jo:0,jret.r:jret.id('T3_TUa')}))
on('T3_TU9',(None,'J0',None))
on('T3_TUa',(None,'T3_TUb',{ap:cp,ao:0,jp:net.min_(tq,npar-1),jo:0,jret.r:jret.id('T3_TUc')}))
on('T3_TUb',(None,'J0',None))
on('T3_TUc',(None,'DS0',{dret.r:dret.id('T3_TUd')}))
on('T3_TUd',(None,'TC0',{ti_:0,ap:cp,ao:co}))
# ---- .docx writer: section properties, tabs, markers, comments, notes, header and footer parts ----
sx1=R();sx2=R();sx3=R();sx4=R();sx5=R();sx6=R();sx7=R();sx8=R();snext=R();ctl=R()
on('T3_SX',(None,'T3_SXa',{rl:as_x(SECB)+qsec*8}))
on('T3_SXa',(None,'T3_SXb',{sx1:RL[0],sx2:RL[1],sx3:RL[2],sx4:RL[4]-RL[3],sx5:RL[1]-RL[4]+RL[3]-RL[5],sx6:RL[6],sx7:RL[2]-RL[6]-RL[7]}))
lit('T3_SXb',b'<w:sectPr>','T3_SXc')
cur_='T3_SXc'
for i_,(ty_,rid_,tag_) in enumerate(((b'default',b'rIdH1',b'header'),(b'first',b'rIdH2',b'header'),(b'default',b'rIdR1',b'footer'),(b'first',b'rIdR2',b'footer'))):
    nx_=f'T3_SXd{i_}'
    on(cur_,(net.step(hfl[i_]),cur_+'L',None),(None,nx_,None))
    lit(cur_+'L',b'<w:%sReference w:type="%s" r:id="%s"/>'%(tag_,ty_,rid_),nx_); cur_=nx_
lit(cur_,b'<w:pgSz w:w="','T3_SXe'); numz('T3_SXe',sx2*15,'T3_SXf'); lit('T3_SXf',b'" w:h="','T3_SXg'); numz('T3_SXg',sx3*15,'T3_SXh')
e=S('T3_SXh')
on('T3_SXh',(net.gt(sx2,sx3,e),'T3_SXi',None),(None,'T3_SXj',None)); lit('T3_SXi',b'" w:orient="landscape','T3_SXj')
lit('T3_SXj',b'"/><w:pgMar w:top="','T3_SXk'); numz('T3_SXk',sx6*15,'T3_SXl'); lit('T3_SXl',b'" w:right="','T3_SXm'); numz('T3_SXm',sx5*15,'T3_SXn')
lit('T3_SXn',b'" w:bottom="','T3_SXo'); numz('T3_SXo',sx7*15,'T3_SXp'); lit('T3_SXp',b'" w:left="','T3_SXq'); numz('T3_SXq',sx4*15,'T3_SXr')
lit('T3_SXr',b'" w:header="720" w:footer="720" w:gutter="0"/><w:cols w:num="','T3_SXs'); numz('T3_SXs',sx1,'T3_SXt'); lit('T3_SXt',b'"/>','T3_SXu')
e=S('T3_SXu')
on('T3_SXu',(net.and_(hftp,net.eq(qsec,0,e)),'T3_SXv',None),(None,'T3_SXw',None)); lit('T3_SXv',b'<w:titlePg/>','T3_SXw')
lit('T3_SXw',b'</w:sectPr>','T3_SXR')
# paragraph properties around jc
TOCB=b'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="'
on('T3_TA0',(net.step(spb),'T3_TAp',None),(None,'T3_TAq',None))
lit('T3_TAp',b'<w:pageBreakBefore/>','T3_TAq')
on('T3_TAq',(None,'T3_TA1',{r1:pbs+TOCF,rmeta:pbs+META}))
e=S('T3_TA1')
on('T3_TA1',(net.step(R1),'T3_TA2',{tlev:R1,tu1:MT[1]*0+s_tw*15}),(None,'SVj2',None))
lit('T3_TA2',TOCB,'T3_TA3'); numz('T3_TA3',tu1,'T3_TA4'); lit('T3_TA4',b'"/></w:tabs>','T3_TA5')
e=S('T3_TA5')
on('T3_TA5',(net.eq(tlev,2,e),'T3_TA6',None),(None,'SVj2',None)); lit('T3_TA6',b'<w:ind w:left="360"/>','SVj2')
# sectPr in the last paragraph of a section, then comment range start
on('T3_SNA',(net.lt(pi+1,npar,S('T3_SNA')),'T3_SNB',{r1:as_x(PT)+pi+1}),(None,'T3_SNE',{snext:0}))
on('T3_SNB',(None,'T3_SNC',{r2:R1+SECN}))
on('T3_SNC',(None,'T3_SND',{snext:R2}))
e=S('T3_SND')
on('T3_SND',(net.step(snext),'T3_SX',{sxr.r:sxr.id('T3_SNF')}),(None,'T3_SNE',None))
on('T3_SNF',(None,'T3_SNE',{qsec:snext-1}))
lit('T3_SNE',b'</w:pPr>','T3_SNG')
on('T3_SNG',(None,'T3_SNH',{r1:pbs+CMTL}))
e=S('T3_SNH')
on('T3_SNH',(net.step(R1),'T3_SNI',{ctl:R1}),(None,'SVC',{ctl:0}))
lit('T3_SNI',b'<w:commentRangeStart w:id="','T3_SNJ'); numz('T3_SNJ',pi,'T3_SNK'); lit('T3_SNK',b'"/>','SVC')
# end of paragraph: TOC tab and number, comment reference
e=S('T3_CE0')
on('T3_CE0',(None,'T3_CE1',{r1:pbs+TOCF,r2:pbs+TSRC}))
e=S('T3_CE1')
on('T3_CE1',(net.step(R1),'T3_CE2',{tu0:R2}),(None,'T3_CE6',None))
e=S('T3_CE2')
on('T3_CE2',(None,'T3_CE3',{r1:tu0+SAVE+2,r2:pbs+TPG}))
e=S('T3_CE3'); hs=net.step(tu0)
on('T3_CE3',(None,'T3_CE4',{tpv:G_(R1,hs)+G_(R2,ONE-hs)}))
lit('T3_CE4',b'<w:r><w:tab/></w:r><w:r><w:t>','T3_CE5'); numz('T3_CE5',tpv,'T3_CE5a'); lit('T3_CE5a',b'</w:t></w:r>','T3_CE6')
e=S('T3_CE6')
on('T3_CE6',(net.step(ctl),'T3_CE7',None),(None,'T3_CEz',None))
lit('T3_CE7',b'<w:commentRangeEnd w:id="','T3_CE8'); numz('T3_CE8',pi,'T3_CE9'); lit('T3_CE9',b'"/><w:r><w:commentReference w:id="','T3_CEa'); numz('T3_CEa',pi,'T3_CEb'); lit('T3_CEb',b'"/></w:r>','T3_CEz')
# footnote reference inside the run stream; saved ids run 1,2,3 in text order and index a table of store ids
sfn=R();FORD2=43000
e=S('T3_SF0')
on('T3_SF0',(net.eq(lsf,99999,e),'T3_SF2',None),(None,'T3_SF1',None))
lit('T3_SF1',docx_tpl.R_CLOSE,'T3_SF2')
lit('T3_SF2',b'<w:r><w:rPr><w:vertAlign w:val="superscript"/></w:rPr><w:footnoteReference w:id="','T3_SF3'); numz('T3_SF3',sfn+1,'T3_SF4'); lit('T3_SF4',b'"/></w:r>','T3_SF5')
on('T3_SF5',(None,'SVC',{lsf:99999,off_:off_+1,w1:(as_x(FORD2)+sfn,ins_ch-1000),sfn:sfn+1}))
fsm.set(sfn,S('SAVE'),0)
# literal text run writer
xb=R();xl=R();xi=R();xret=t3ret('T3_XR')
TRUN=b'<w:r><w:t xml:space="preserve">'
on('T3_XT',(None,'T3_XT0',None))
lit('T3_XT0',TRUN,'T3_XT1'); fsm.set(xi,S('T3_XT'),0)
e=S('T3_XT1')
on('T3_XT1',(net.ge(xi,xl,e),'T3_XTz',None),(None,'T3_XT2',{r1:xb+xi}))
e=S('T3_XT2'); a_=net.eq(R1,38,e);b_=net.eq(R1,60,e);c_=net.eq(R1,62,e);d_=net.eq(R1,1,e); o_=e-a_-b_-c_-d_
em_en.lin(o_); em_b.add(o_,R1)
on('T3_XT2',(a_,'T3_XTa',{xi:xi+1}),(b_,'T3_XTb',{xi:xi+1}),(c_,'T3_XTc',{xi:xi+1}),(d_,'T3_XTd',{xi:xi+1}),(None,'T3_XT1',{xi:xi+1}))
lit('T3_XTa',b'&amp;','T3_XT1');lit('T3_XTb',b'&lt;','T3_XT1');lit('T3_XTc',b'&gt;','T3_XT1')
lit('T3_XTd',b'</w:t></w:r><w:fldSimple w:instr=" PAGE "><w:r><w:t>1</w:t></w:r></w:fldSimple>'+TRUN,'T3_XT1')
lit('T3_XTz',b'</w:t></w:r>','T3_XR')
# footnotes part
zbegin('T3_XM0',b'word/footnotes.xml','T3_XF0')
lit('T3_XF0',XHEAD+b'<w:footnotes '+WNS+b'><w:footnote w:type="separator" w:id="-1"><w:p><w:r><w:separator/></w:r></w:p></w:footnote><w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:r><w:continuationSeparator/></w:r></w:p></w:footnote>','T3_XF1')
fsm.set(mq,S('T3_XF0'),1)
e=S('T3_XF1')
on('T3_XF1',(net.gt(mq,sfn,e),'T3_XF9',None),(None,'T3_XF1a',{r1:as_x(FORD2)+mq-1}))
on('T3_XF1a',(None,'T3_XF2',{xb:as_x(FNB)+R1*256,r2:as_x(FNB)+R1*256+255}))
on('T3_XF2',(None,'T3_XF3',{xl:R2}))
lit('T3_XF3',b'<w:footnote w:id="','T3_XF4'); numz('T3_XF4',mq,'T3_XF5')
lit('T3_XF5',b'"><w:p><w:r><w:rPr><w:vertAlign w:val="superscript"/></w:rPr><w:footnoteRef/></w:r>','T3_XF6')
on('T3_XF6',(None,'T3_XT',{xret.r:xret.id('T3_XF7')}))
lit('T3_XF7',b'</w:p></w:footnote>','T3_XF8'); on('T3_XF8',(None,'T3_XF1',{mq:mq+1}))
lit('T3_XF9',b'</w:footnotes>','T3_XFe'); zend('T3_XFe','T3_XC00')
# comments part
zbegin('T3_XC00',b'word/comments.xml','T3_XC0')
lit('T3_XC0',XHEAD+b'<w:comments '+WNS+b'>','T3_XC1'); fsm.set(mq,S('T3_XC0'),0)
e=S('T3_XC1')
on('T3_XC1',(net.ge(mq,npar,e),'T3_XC9',None),(None,'T3_XC2',{r1:as_x(PT)+mq}))
on('T3_XC2',(None,'T3_XC3',{xb:R1+CMT,r2:R1+CMTL}))
e=S('T3_XC3')
on('T3_XC3',(net.step(R2),'T3_XC4',{xl:R2}),(None,'T3_XC1',{mq:mq+1}))
lit('T3_XC4',b'<w:comment w:id="','T3_XC5'); numz('T3_XC5',mq,'T3_XC6'); lit('T3_XC6',b'" w:author="SynapseWrite" w:initials="SW"><w:p>','T3_XC7')
on('T3_XC7',(None,'T3_XT',{xret.r:xret.id('T3_XC8')}))
lit('T3_XC8',b'</w:p></w:comment>','T3_XCa'); on('T3_XCa',(None,'T3_XC1',{mq:mq+1}))
lit('T3_XC9',b'</w:comments>','T3_XCe'); zend('T3_XCe','T3_XH0')
# header and footer parts
cur_='T3_XH0'
for i_,(nm_,tg_) in enumerate(((b'header1',b'hdr'),(b'header2',b'hdr'),(b'footer1',b'ftr'),(b'footer2',b'ftr'))):
    st_=f'T3_XHa{i_}'; nx_=f'T3_XHn{i_}'
    zbegin(cur_,b'word/%s.xml'%nm_,st_)
    lit(st_,XHEAD+b'<w:%s '%tg_+WNS+b'><w:p>',st_+'b')
    on(st_+'b',(None,'T3_XT',{xb:as_x(HFB)+i_*256,xl:hfl[i_],xret.r:xret.id(st_+'c')}))
    lit(st_+'c',b'</w:p></w:%s>'%tg_,st_+'e'); zend(st_+'e',nx_); cur_=nx_
on(cur_,(None,'T3_Z5',None))
# ---- .docx reader: parts that feed the note and comment stores, header strings ----
ai=R();ad=R();alen=R();aend=R();akind=R();askip=R();aret=t3ret('T3_AR'); AU=as_x(AUXB)
on('T3_FN0',(None,'T3_A0',{ai:0,akind:1,ad:as_x(FNB),alen:0,askip:0,aret.r:aret.id('T3_Z3n')}))
on('T3_CM0',(None,'T3_A0',{ai:0,akind:2,ad:as_x(CMB),alen:0,askip:0,aret.r:aret.id('T3_Z4n')}))
on('T3_HP0',(None,'T3_A0',{ai:0,akind:3,ad:as_x(HFB)+rhk*256,alen:0,askip:0,aret.r:aret.id('T3_HP1')}))
e=S('T3_HP1'); hh_=net.decode(rhk,4,e)
for i_ in range(4): fsm.set(hfl[i_],hh_[i_],alen)
on('T3_HP1',(None,'PX',{ob:sob,oi:soi,obase:OUTB,rhf:0}))
e=S('T3_A0')
on('T3_A0',(net.ge(ai,aux_l,e),'T3_AR',None),(None,'T3_A1',{rl:AU+ai}))
e=S('T3_A1'); k1=net.eq(akind,1,e);k2=net.eq(akind,2,e);k3=net.eq(akind,3,e)
on('T3_A1',(net.and_(net.step(k1),pat('<w:footn',e)),'T3_AI0',{ai:ai+8}),(net.and_(k2,pat('<w:comme',e)),'T3_AI0',{ai:ai+8}),
 (net.and_(k1,pat('</w:foot',e)),'T3_AE0',{ai:ai+8}),(net.and_(k2,pat('</w:comm',e)),'T3_AE0',{ai:ai+8}),
 (net.and_(k3,pat('<w:fldSi',e)),'T3_A0',{ai:ai+8,askip:1,w1:(ad+alen,1),alen:alen+1}),(pat('</w:fldS',e),'T3_A0',{ai:ai+8,askip:0}),
 (pat('<w:instr',e),'T3_AF0',{ai:ai+8}),(pat('"end"',e),'T3_A0',{ai:ai+5,askip:0}),(pat('"separa',e),'T3_A0',{ai:ai+7}),
 (net.and_(net.eq(W[0],60,e),net.eq(W[1],119,e),net.eq(W[2],58,e),net.eq(W[3],116,e),net.or_(net.eq(W[4],32,e),net.eq(W[4],62,e))),'T3_AX0',{ai:ai+4}),
 (None,'T3_A0',{ai:ai+1}))
on('T3_AF0',(None,'T3_AF1',{rl:AU+ai}))
e=S('T3_AF1')
on('T3_AF1',(net.eq(W[0],62,e),'T3_AF2',{rl:AU+ai+1}),(None,'T3_AF0',{ai:ai+1}))
e=S('T3_AF2')
on('T3_AF2',(net.or_(pat('PAGE',e),pat(' PAGE',e)),'T3_A0',{askip:1,w1:(ad+alen,1),alen:alen+1}),(None,'T3_A0',{askip:1}))
on('T3_AI0',(None,'T3_AI1',{rl:AU+ai}))
e=S('T3_AI1')
okt=net.or_(net.and_(k1 if False else net.eq(akind,1,e),pat('ote ',e)),net.and_(net.eq(akind,2,e),pat('nt ',e)))
on('T3_AI1',(okt,'T3_AI2',None),(None,'T3_A0',None))
on('T3_AI2',(None,'T3_AI3',{rl:AU+ai}))
e=S('T3_AI3')
on('T3_AI3',(pat('w:id="',e),'T3_AI4',{ai:ai+6,aval:0}),(net.eq(W[0],62,e),'T3_A0',None),(None,'T3_AI2',{ai:ai+1}))
on('T3_AI4',(None,'T3_AI5',{r1:AU+ai}))
e=S('T3_AI5')
isd2=net.and_(net.ge(R1,48,e),net.lt(R1,58,e))
on('T3_AI5',(isd2,'T3_AI4',{aval:aval*10+R1-48,ai:ai+1}),(None,'T3_AI6',None))
e=S('T3_AI6'); k1_=net.eq(akind,1,e)
on('T3_AI6',(None,'T3_A0',{ad:G_(as_x(FNB)+aval*256,k1_)+G_(as_x(CMB)+aval*256,e-k1_),alen:0,aend:aval,askip:0}))
# close a note: record length and line count
e=S('T3_AE0')
on('T3_AE0',(net.eq(akind,1,e),'T3_W',{wl_:alen,wb_:ad,wdw:s_tw-22,wdd:0,wdx:0,wdy:0,wbgf:0,wret_.r:wret_.id('T3_AE1')}),(None,'T3_A0',{w1:(ad+255,alen)}))
on('T3_AE1',(None,'T3_A0',{w1:(ad+254,wcnt*16),w2:(ad+255,alen)}))
# text inside the part
on('T3_AX0',(None,'T3_AX1',{rl:AU+ai}))
e=S('T3_AX1')
on('T3_AX1',(net.eq(W[0],62,e),'T3_AX2',{ai:ai+1}),(None,'T3_AX0',{ai:ai+1}))
on('T3_AX2',(None,'T3_AX3',{rl:AU+ai}))
e=S('T3_AX3')
amp2=net.eq(W[0],38,e)
on('T3_AX3',(net.eq(W[0],60,e),'T3_A0',None),(net.step(askip),'T3_AX2',{ai:ai+1}),
 (net.and_(amp2,net.eq(W[1],97,e)),'T3_AX2',{w1:(ad+alen,38),alen:alen+1,ai:ai+5}),
 (net.and_(amp2,net.eq(W[1],108,e)),'T3_AX2',{w1:(ad+alen,60),alen:alen+1,ai:ai+4}),
 (net.and_(amp2,net.eq(W[1],103,e)),'T3_AX2',{w1:(ad+alen,62),alen:alen+1,ai:ai+4}),
 (net.or_(net.gt(W[0],126,e),net.lt(W[0],32,e),net.ge(alen,250,e)),'T3_AX2',{ai:ai+1}),
 (None,'T3_AX2',{w1:(ad+alen,W[0]),alen:alen+1,ai:ai+1}))
# references in document.xml
on('T3_RF0',(None,'T3_RF1',{rl:OA+oi}))
e=S('T3_RF1')
on('T3_RF1',(pat('oteRefer',e),'T3_NA',{nmret.r:nmret.id('T3_RF2')}),(None,'PX',None))
on('T3_RF2',(None,'INS',{fnc:net.max_(fnc,aval),ins_ch:aval+1000,ins_st:0,oret.r:oret.id('PX')}))
on('T3_RC0',(None,'T3_RC1',{rl:OA+oi}))
e=S('T3_RC1')
on('T3_RC1',(pat('ntRefere',e),'T3_NA',{nmret.r:nmret.id('T3_RC2')}),(None,'PX',None))
on('T3_RC2',(None,'T3_RC3',{tq:0,xb:as_x(CMB)+aval*256,r1:as_x(CMB)+aval*256+255}))
on('T3_RC3',(None,'T3_RC4',{xl:net.min_(R1,199),w1:(cb+CMTL,net.min_(R1,199))}))
e=S('T3_RC4')
on('T3_RC4',(net.ge(tq,xl,e),'PX',None),(None,'T3_RC5',{r1:xb+tq}))
on('T3_RC5',(None,'T3_RC4',{w1:(cb+CMT+tq,R1),tq:tq+1}))
# TOC entries and tabs
e=S('T3_RT0')
on('T3_RT0',(rtoc,'PX',{rdig:1,tpgv:0}),(None,'INS',{ins_ch:32,ins_st:cs,tabn:0,oret.r:oret.id('T3_RT3')}))
on('T3_RT3',(None,'INS',{ins_ch:32,ins_st:cs,oret.r:oret.id('T3_RT4')}));on('T3_RT4',(None,'INS',{ins_ch:32,ins_st:cs,oret.r:oret.id('T3_RT5')}));on('T3_RT5',(None,'INS',{ins_ch:32,ins_st:cs,oret.r:oret.id('PX')}))
on('T3_RT1',(None,'T3_RT2',{rl:OA+oi}))
e=S('T3_RT2')
on('T3_RT2',(pat('"dot"',e),'PX',{rtoc:1,w1:(cb+TOCF,1),oi:oi+5}),(net.eq(W[0],62,e),'PX',None),(None,'T3_RT1',{oi:oi+1}))
on('T3_RI0',(rtoc,'PX',{w1:(cb+TOCF,2)}),(None,'PX',None))
# section properties
on('T3_RZ0',(None,'T3_RZ1',{rl:OA+oi}))
e=S('T3_RZ1')
on('T3_RZ1',(pat('w:w="',e),'T3_NA',{nmret.r:nmret.id('T3_RZa')}),(pat('w:h="',e),'T3_NA',{nmret.r:nmret.id('T3_RZb')}),(pat('w:top="',e),'T3_NA',{nmret.r:nmret.id('T3_RZc')}),(pat('w:right=',e),'T3_NA',{nmret.r:nmret.id('T3_RZd')}),(pat('w:bottom',e),'T3_NA',{nmret.r:nmret.id('T3_RZe')}),(pat('w:left="',e),'T3_NA',{nmret.r:nmret.id('T3_RZf')}),(pat('w:num="',e),'T3_NA',{nmret.r:nmret.id('T3_RZg')}),(net.eq(W[0],62,e),'PX',None),(None,'T3_RZ0',{oi:oi+1}))
for st_,rg_ in (('a',sv_pw),('b',sv_ph),('c',sv_mt),('d',sv_mr),('e',sv_mb),('f',sv_ml)):
    e=S('T3_RZ'+st_); on('T3_RZ'+st_,(None,'T3_RZ0',{rg_:floorv(aval*(1.0/15)+0.5,e)}))
on('T3_RZg',(None,'T3_RZ0',{sv_nc:net.min_(aval,2)}))
on('T3_RE0',(None,'T3_SW',{sv_i:rdsec,swret.r:swret.id('T3_RE1')}))
on('T3_RE1',(None,'PX',{rdsec:rdsec+1,rdp:rdsec+2,nsec:rdsec+2}))
# header and footer references
on('T3_RH0',(None,'T3_RH1',{rl:OA+oi}))
e=S('T3_RH1')
on('T3_RH1',(pat('"first"',e),'T3_RH0',{rhk:rhk+1,oi:oi+7}),(pat('"even"',e),'PX',None),(pat('r:id="',e),'T3_RH2',{oi:oi+6,rid_n:0}),(net.eq(W[0],62,e),'PX',None),(None,'T3_RH0',{oi:oi+1}))
on('T3_RH2',(None,'T3_RH3',{r1:OA+oi}))
e=S('T3_RH3')
hhv=net.decode(rhk,4,e); had=sum((net.and_(hhv[i_],net.step(hfl[i_])) for i_ in range(4)),X())
on('T3_RH3',(net.and_(net.eq(R1,34,e),net.step(had)),'PX',None),(net.eq(R1,34,e),'T3_BR0',{rq:0,rhf:1}),(None,'T3_RH2',{w1:(as_x(RIDB)+rid_n,R1),rid_n:rid_n+1,oi:oi+1}))

on('T3_RB0',(None,'T3_RB1',{rl:OA+oi}))
e=S('T3_RB1')
on('T3_RB1',(pat('"page"',e),'T3_RB2',None),(net.eq(W[0],62,e),'PX',None),(None,'T3_RB0',{oi:oi+1}))
on('T3_RB2',(None,'PX',{w1:(cb+PBRK,1)}))

# ---- paragraph merge by the user: metadata goes through the log first, so undo brings it back ----
MZF=[(IMF,0),(IMF+1,0),(IMF+2,0),(IMN,0),(IMN+1,0),(IMN+2,0),(SECN,0),(TOCF,0),(TSRC,0),(TPG,0),(CMTL,0)]
set_chain('T3_MZ',MZF,'MERGE')
# backspace into a picture removes the picture: clear it, come back, merge the empty paragraph away
on('T3_MP0',(None,'T3_MP1',{jp:cp-1,jo:0,jret.r:jret.id('T3_MP2')}))
on('T3_MP1',(None,'J0',None))
set_chain('T3_MP2',MZF[:6],'T3_MP3')
on('T3_MP3',(None,'T3_MP4',{jp:cp+1,jo:0,jret.r:jret.id('T3_MZ')}))
on('T3_MP4',(None,'J0',None))
