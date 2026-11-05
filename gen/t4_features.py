# ---- Tier 4: spelling marks, tracked changes, fields, equations, mail merge ----
net.group('tier 4 features')
t4r=Ret('T4_RR'); fvr=Ret('T4_FVR')
def fd_in(*names):
    for n_ in names: fin.add(S(n_),R2); fen.lin(S(n_))
# wavy underline: repeated code 128 glyph over the word's extent
e=S('T4_SQ')
on('T4_SQ',(net.ge(sx,sp_xe,e),'T4_SQ1',None),(None,'T4_SQ',{gly:(128,9,sx,sy+lasc+1,4,0),sx:sx+adv}))
on('T4_SQ1',(sp_r,'CE',{sp_r:0}),(None,'C0',None))
# status bar flag
on('T4_ST',(trk,'T4_ST1',None),(None,'FB0',None))
text_chain('T4_ST1',['     Track Changes: On'],'FB0')
# ---- tracked deletion ----
e=S('T4_BK')
on('T4_BK',(net.step(co),'T4_BK1',{r2:cb+1024+co-1}),(net.step(cp),'MVJ',{jp:cp-1,jo:2047,jret.r:jret.id('AFTER_ED')}),(None,'AFTER_ED',None))
fd_in('T4_BK1','T4_DK1','T4_AM','T4_UM','T4_UE','T4_EM')
e=S('T4_BK1'); mk=net.and_(e,ONE-FD['ins'],ONE-FD['dele']); log(mk,5,cp,co-1,R2,R2+4096)
on('T4_BK1',(FD['ins'],'DEL',{co:co-1,oret.r:oret.id('AFTER_ED')}),(FD['dele'],'AFTER_ED',{co:co-1}),(None,'AFTER_ED',{co:co-1,w1:(cb+1024+co-1,R2+4096),w2:(cb+DIRTY,1)}))
e=S('T4_DK')
on('T4_DK',(net.lt(co,clen,e),'T4_DK1',{r2:cb+1024+co}),(net.lt(cp+1,npar,e),'MVJ',{jp:cp+1,jo:0,jret.r:jret.id('AFTER_ED')}),(None,'AFTER_ED',None))
e=S('T4_DK1'); mk=net.and_(e,ONE-FD['ins'],ONE-FD['dele']); log(mk,5,cp,co,R2,R2+4096)
on('T4_DK1',(FD['ins'],'DEL',{oret.r:oret.id('AFTER_ED')}),(FD['dele'],'AFTER_ED',{co:co+1}),(None,'AFTER_ED',{co:co+1,w1:(cb+1024+co,R2+4096),w2:(cb+DIRTY,1)}))
on('T4_DS0',(None,'W0',None))
on('T4_DS1',(None,'MVJ',{jp:hi_p,jo:hi_o,jret.r:jret.id('T4_DS2')}))
on('T4_DS2',(None,'DR',{ap:cp,ao:co}))
# ---- range loop shared by accept, reject and equation ----
a_ep=R();a_eo=R();a_sp=R();a_so=R()
def range_start(st,next_loop,noselpara):
    e=S(st)
    if noselpara: acts={a_ep:cp,a_eo:2047,a_sp:cp,a_so:co,jp:cp,jo:0}
    else: acts={a_ep:net.relu(npar-1),a_eo:2047,a_sp:cp,a_so:co,jp:0,jo:0}
    on(st,(has_sel,st+'a',{a_ep:hi_p,a_eo:hi_o,a_sp:cp,a_so:co,jp:lo_p,jo:lo_o}),(None,st+'a',acts))
    on(st+'a',(None,'J0',{jret.r:jret.id(next_loop)}))
def range_loop(st,body):
    e=S(st)
    on(st,(net.and_(net.eq(cp,a_ep,e),net.ge(co,a_eo,e)),'T4_AE',None),
       (net.and_(net.ge(co,clen,e),net.lt(cp,a_ep,e)),'J0',{jp:cp+1,jo:0,jret.r:jret.id(st)}),
       (net.ge(co,clen,e),'T4_AE',None),(None,body,{r1:cb+co,r2:cb+1024+co}))
on('T4_AE',(None,'J0',{jp:a_sp,jo:a_so,jret.r:jret.id('T4_AF')}))
on('T4_AF',(None,'AFTER_ED',{fastok:0}))
range_start('T4_AR','T4_AL',False); range_loop('T4_AL','T4_AM')
e=S('T4_AM')
rmv=net.or_(net.and_(arj,FD['ins']),net.and_(ONE-arj,FD['dele']))
clr=net.and_(e,ONE-rmv,net.or_(FD['ins'],FD['dele']))
newa=R2-FD['ins']*2048-FD['dele']*4096
log(clr,5,cp,co,R2,newa)
on('T4_AM',(rmv,'DEL',{a_eo:a_eo-net.eq(cp,a_ep,e),oret.r:oret.id('T4_AL')}),(clr,'T4_AL',{w1:(cb+1024+co,newa),w2:(cb+DIRTY,1),co:co+1}),(None,'T4_AL',{co:co+1}))
# ---- fields: runs of characters whose style word holds the field kind ----
fst=R();t4nv=R();t4y=R();t4d=R();t4m=R();t4lp=R()
on('T4_FI',(has_sel,'DS0',{dret.r:dret.id('T4_FI2'),grp:grp+1}),(None,'T4_FI2',{grp:grp+1}))
on('T4_FI2',(None,'T4_FV',{fst:TST+t4k*8192,fvr.r:fvr.id('AFTER_ED')}))
on('T4_FV',(None,'T4_FV1',{r1:cb+SAVE+2}))
e=S('T4_FV1')
on('T4_FV1',(net.eq(t4k,1,e),'T4_NI',{t4nv:R1,t4r.r:t4r.id('T4_FVR')}),(net.eq(t4k,2,e),'T4_NI',{t4nv:wtot,t4r.r:t4r.id('T4_FVR')}),(None,'T4_DY1',{t4y:1970,t4d:evt}))
PW=(100000,10000,1000,100,10,1)
for i_,pw_ in enumerate(PW):
    st=f'T4_NI{pw_}'; nx=f'T4_NI{PW[i_+1]}' if pw_>1 else 'T4_RR'
    e=S(st); base=net.gate(t4nv,e); val=base
    for big in PW:
        if big>pw_:
            dd=X()
            for t in range(1,10): dd=dd+net.step(val-big*t+0.5)
            val=val-dd*big
    dg=X()
    for t in range(1,10): dg=dg+net.step(val-pw_*t+0.5)
    show=e if pw_==1 else net.step(base-pw_+0.5)
    on(st,(show,'INS',{ins_ch:48+dg,ins_st:fst,oret.r:oret.id(nx)}),(None,nx,None))
on('T4_NI',(None,'T4_NI100000',None))
# days since 1970 to a civil date, valid for 1970 to 2099
e=S('T4_DY1'); ybits=net.bits(t4y,12,e); leap=net.and_(e,ONE-ybits[0],ONE-ybits[1]); yd=365+leap
on('T4_DY1',(net.ge(t4d,yd,e),'T4_DY1',{t4d:t4d-yd,t4y:t4y+1}),(None,'T4_DM',{t4m:1,t4lp:leap}))
e=S('T4_DM'); mh=net.decode(t4m,13,e); ml=X()
for m_,d_ in enumerate((31,28,31,30,31,30,31,31,30,31,30,31),1): ml=ml+mh[m_]*d_
ml=ml+G_(t4lp,net.step(mh[2]))
on('T4_DM',(net.ge(t4d,ml,e),'T4_DM',{t4d:t4d-ml,t4m:t4m+1}),(None,'T4_DS',None))
on('T4_DS',(None,'T4_NI',{t4nv:t4m,t4r.r:t4r.id('T4_D2')}))
on('T4_D2',(None,'INS',{ins_ch:47,ins_st:fst,oret.r:oret.id('T4_D3')}))
on('T4_D3',(None,'T4_NI',{t4nv:t4d+1,t4r.r:t4r.id('T4_D4')}))
on('T4_D4',(None,'INS',{ins_ch:47,ins_st:fst,oret.r:oret.id('T4_D5')}))
on('T4_D5',(None,'T4_NI',{t4nv:t4y,t4r.r:t4r.id('T4_FVR')}))
# update: walk the document, replace each field run with a fresh value
on('T4_FU',(None,'J0',{a_ep:net.relu(npar-1),a_eo:2047,a_sp:cp,a_so:co,jp:0,jo:0,jret.r:jret.id('T4_UL')}))
range_loop('T4_UL','T4_UM')
e=S('T4_UM'); fkv=FD['f0']+FD['f1']*2
on('T4_UM',(net.step(fkv),'T4_UD',{t4k:fkv,fst:R2}),(None,'T4_UL',{co:co+1}))
e=S('T4_UD')
on('T4_UD',(net.lt(co,clen,e),'T4_UE',{r2:cb+1024+co}),(None,'T4_FV',{fvr.r:fvr.id('T4_UL')}))
e=S('T4_UE'); fkv2=FD['f0']+FD['f1']*2
on('T4_UE',(net.eq(fkv2,t4k,e),'DEL',{oret.r:oret.id('T4_UD')}),(None,'T4_FV',{fvr.r:fvr.id('T4_UL')}))
# ---- equations: a linear form with ^ and _ becomes italic letters and shifted small script ----
eq_sc=R();eq_gr=R();eq_pre=R()
on('T4_EQ',(None,'T4_EQ0',{eq_sc:0,eq_gr:0,eq_pre:0}))
range_start('T4_EQ0','T4_EL',True); range_loop('T4_EL','T4_EM')
e=S('T4_EM')
isc=net.eq(R1,94,e);isb=net.eq(R1,95,e);opn=net.and_(net.eq(R1,123,e),eq_pre);cls=net.and_(net.eq(R1,125,e),eq_gr)
app=net.and_(e,ONE-isc,ONE-isb,ONE-opn,ONE-cls)
lo_=low(R1,e); lett=net.and_(net.ge(lo_,97,e),net.lt(lo_,123,e),app)
hsc=net.and_(app,net.step(eq_sc)); s1=net.and_(hsc,net.eq(eq_sc,1,e)); s2=net.and_(hsc,net.eq(eq_sc,2,e))
neweq=R2+G_(ONE-FD['ital'],lett)*32+G_(ONE-FD['font'],app)*128+G_(ONE-FD['nop'],app)*131072+G_(as_x(9),hsc)-G_(FD['size'],hsc)+G_(ONE-FD['sup'],s1)*32768+G_(ONE-FD['sub'],s2)*65536
log(app,5,cp,co,R2,neweq)
adj_=a_eo-net.eq(cp,a_ep,e)
dl_={a_eo:adj_,oret.r:oret.id('T4_EL')}
on('T4_EM',(isc,'DEL',{**dl_,eq_sc:1,eq_gr:0,eq_pre:1}),(isb,'DEL',{**dl_,eq_sc:2,eq_gr:0,eq_pre:1}),(opn,'DEL',{**dl_,eq_gr:1,eq_pre:0}),(cls,'DEL',{**dl_,eq_gr:0,eq_sc:0}),
 (None,'T4_EL',{w1:(cb+1024+co,neweq),w2:(cb+DIRTY,1),co:co+1,eq_pre:0,eq_sc:G_(eq_sc,eq_gr)}))
# ---- mail merge: CSV from the clipboard buffer into a cell table, then one copy of the document per row ----
MGT=60000; MGB=100000
mi=R();mq=R();mo=R();mfs=R();mc=R();mrb=R();mnr=R();mncol=R();mn0=R();mr=R();mrba=R();mp=R();msb=R();mlen=R();mso=R();mol=R();mst=R();mnb=R();mnl=R();mk=R();mhs=R();mi2=R();mvl=R();mpb=R();mimw=R();mimh=R();mimo=R()
BANNER='Mail Merge: paste CSV now (Ctrl+V). The first row is the header; {Name} in the document is replaced. Esc cancels.'
on('T4_MB',(None,'T4_MBa',{rA:(PX,DOCY,816,28,(255,242,171),0),sx:PX+8}))
cur_='T4_MBa'
for i_,ch_ in enumerate(BANNER):
    nx=f'T4_MBc{i_}' if i_<len(BANNER)-1 else 'TB0'
    on(cur_,(None,nx,{gly:(ord(ch_),9,sx,DOCY+6,0,2),sx:sx+adv})); cur_=nx
on('T4_M0',(None,'T4_M1',{mi:0,mq:0,mo:0,mfs:0,mc:0,mrb:0,mnr:0,mncol:0,grp:grp+1}))
e=S('T4_M1')
on('T4_M1',(net.ge(mi,evc,e),'T4_M1z',None),(net.ge(mnr,500,e),'T4_M5',None),(None,'T4_M2',{rl:as_x(CB2)+mi}))
e=S('T4_M1z')
on('T4_M1z',(net.or_(net.step(mc),net.gt(mo,mfs,e)),'T4_M3',{mi:mi+1}),(None,'T4_M5',None))
e=S('T4_M2'); c_=rl.out[0]; n_=rl.out[1]
q_=net.eq(c_,34,e);comma=net.eq(c_,44,e);nl_=net.eq(c_,10,e);cr_=net.eq(c_,13,e)
blank=net.and_(net.eq(mc,0,e),net.ge(mfs,mo,e))
lit_c={w1:(as_x(MGB)+mo,c_),mo:mo+1,mi:mi+1}
closef={w1:(as_x(MGT)+mrb+mc*2,mfs),w2:(as_x(MGT)+mrb+mc*2+1,mo-mfs),mfs:mo,mi:mi+1}
on('T4_M2',(net.and_(mq,q_,net.eq(n_,34,e)),'T4_M1',{w1:(as_x(MGB)+mo,34),mo:mo+1,mi:mi+2}),
 (net.and_(mq,q_),'T4_M1',{mq:0,mi:mi+1}),(mq,'T4_M1',lit_c),(q_,'T4_M1',{mq:1,mi:mi+1}),
 (net.and_(comma,net.ge(mc,31,e)),'T4_M1',{mi:mi+1}),
 (comma,'T4_M1',{**closef,mc:mc+1}),
 (net.and_(nl_,blank),'T4_M1',{mi:mi+1}),(nl_,'T4_M3',{mi:mi+1}),(cr_,'T4_M1',{mi:mi+1}),(None,'T4_M1',lit_c))
e=S('T4_M3')
on('T4_M3',(None,'T4_M4',{w1:(as_x(MGT)+mrb+mc*2,mfs),w2:(as_x(MGT)+mrb+mc*2+1,mo-mfs),mfs:mo,mc:mc+1,mncol:G_(mc+1,net.eq(mnr,0,e))+G_(mncol,net.step(mnr))}))
e=S('T4_M4')   # rows with too few cells get empty cells
on('T4_M4',(net.lt(mc,mncol,e),'T4_M4',{w1:(as_x(MGT)+mrb+mc*2,0),w2:(as_x(MGT)+mrb+mc*2+1,0),mc:mc+1}),(None,'T4_M1',{mc:0,mrb:mrb+64,mnr:mnr+1}))
e=S('T4_M5')
on('T4_M5',(net.lt(mnr,2,e),'RD0',None),(None,'T4_M6',{mn0:npar,mr:1,mrba:64,nolog:1}))
e=S('T4_M6')
on('T4_M6',(net.ge(mr,mnr,e),'T4_MZ',{mi2:0}),(None,'T4_M7',{mp:0}))
e=S('T4_M7')
on('T4_M7',(net.ge(mp,mn0,e),'T4_M6',{mr:mr+1,mrba:mrba+64}),(net.ge(nextb,SLOTMAX,e),'T4_MZ',{mi2:0}),(None,'T4_M8',{r1:as_x(PT)+mp}))
on('T4_M8',(None,'T4_M9',{msb:R1,rl:R1+LEN,rc:R1+2062,rim:R1+IMF}))
e=S('T4_M9'); WL=rl.out
on('T4_M9',(None,'T4_MA',{mlen:WL[0],w1:(nextb+ALIGN,WL[2]),w2:(nextb+LIST,WL[3]),w3:(nextb+2062,rc.out[0]),w4:(nextb+2063,rc.out[1]),mimw:rim.out[0],mimh:rim.out[1],mimo:rim.out[2],mpb:net.step(WL[7]+net.and_(net.eq(mp,0,e),net.gt(mr,1,e)))}))
on('T4_MA',(None,'T4_MA2',{w1:(nextb+IMF,mimw),w2:(nextb+IMF+1,mimh),w3:(nextb+IMF+2,mimo),w4:(nextb+PBRK,mpb)}))
on('T4_MA2',(None,'T4_MC',{w1:(as_x(PT)+npar,nextb),wln:(nextb+SAVE,112,16,1,0,0,0),mso:0,mol:0}))
e=S('T4_MC')
on('T4_MC',(net.ge(mso,mlen,e),'T4_MP',None),(net.ge(mol,1000,e),'T4_MP',None),(None,'T4_MD',{r1:msb+mso,r2:msb+1024+mso}))
e=S('T4_MD')
on('T4_MD',(net.eq(R1,123,e),'T4_ME',{mst:R2,mnb:mso+1,mnl:0}),(None,'T4_MC',{w1:(nextb+mol,R1),w2:(nextb+1024+mol,R2),mol:mol+1,mso:mso+1}))
e=S('T4_ME')
on('T4_ME',(net.ge(mnb+mnl,mlen,e),'T4_ML',None),(None,'T4_MF',{r1:msb+mnb+mnl}))
e=S('T4_MF')
on('T4_MF',(net.eq(R1,125,e),'T4_MG',{mk:0}),(None,'T4_ME',{mnl:mnl+1}))
e=S('T4_MG')
on('T4_MG',(net.ge(mk,mncol,e),'T4_ML',None),(None,'T4_MH',{rc:as_x(MGT)+mk*2}))
e=S('T4_MH')
on('T4_MH',(net.eq(rc.out[1],mnl,e),'T4_MI',{mhs:rc.out[0],mi2:0}),(None,'T4_MG',{mk:mk+1}))
e=S('T4_MI')
on('T4_MI',(net.ge(mi2,mnl,e),'T4_MK',None),(None,'T4_MJ',{r1:as_x(MGB)+mhs+mi2,r2:msb+mnb+mi2}))
e=S('T4_MJ')
on('T4_MJ',(net.eq(low(R1,e),low(R2,e),e),'T4_MI',{mi2:mi2+1}),(None,'T4_MG',{mk:mk+1}))
on('T4_MK',(None,'T4_MM',{rc:as_x(MGT)+mrba+mk*2}))
on('T4_MM',(None,'T4_MN',{mhs:rc.out[0],mvl:rc.out[1],mi2:0}))
e=S('T4_MN')
on('T4_MN',(net.or_(net.ge(mi2,mvl,e),net.ge(mol,1000,e)),'T4_MC',{mso:mnb+mnl+1}),(None,'T4_MO',{r1:as_x(MGB)+mhs+mi2}))
on('T4_MO',(None,'T4_MN',{w1:(nextb+mol,R1),w2:(nextb+1024+mol,mst),mol:mol+1,mi2:mi2+1}))
on('T4_ML',(None,'T4_MC',{w1:(nextb+mol,123),w2:(nextb+1024+mol,mst),mol:mol+1,mso:mnb}))
on('T4_MP',(None,'T4_M7',{w1:(nextb+LEN,mol),w2:(nextb+DIRTY,1),npar:npar+1,nextb:nextb+STRIDE,mp:mp+1}))
e=S('T4_MZ')
on('T4_MZ',(net.ge(mi2+mn0,npar,e),'T4_MX',None),(None,'T4_MZ1',{r1:as_x(PT)+mn0+mi2}))
on('T4_MZ1',(None,'T4_MZ',{w1:(as_x(PT)+mi2,R1),mi2:mi2+1}))
on('T4_MX',(None,'J0',{npar:npar-mn0,jp:0,jo:0,jret.r:jret.id('T4_MW')}))
on('T4_MW',(None,'SYNC',{nolog:0,usp:UB,urp:UB,autos:1,lc:1,dfrom:0,scroll:0,bgp:0,fastok:0,blink:0}))
