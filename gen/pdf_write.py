# ---- PDF writer: objects, content streams and the xref table are all produced here ----
net.group('pdf writer')
XR=900000; qp=R();qb=R();qyy=R();qtop=R();qlj=R();qnl=R();qcols=R();qci=R();qx=R();qh=R();qa=R();qs=R();qe=R();qo=R();qst=R();qpg=R();qstart=R();qlenat=R();qobj=R();qi=R();qxr=R();qcur=R()
qph=R();qpw=R();qml=R();qmt=R();qth=R();qps=R();qcx=R();qnc=R();qtw=R();qsz=R();qfn=R();qbase=R()
A9=rom.metrics(9)[0]
pfcr=Ret('T4_PFC');qnr=t3ret('T4P_NR');qfc=R();qf0=R();qfh=R();qfi=R();qfid=R();qtoc=R();qsrc=R();qtpg=R();qtpv=R();qtxe=R();PDFN=1018000
qsvf=R()
def pd_patch(st,nx):
    "Writes the stream length into its reserved seven digit field, then puts the write position back."
    on(st,(None,st+'p',{qsvf:fp,fp:qlenat}))
    number(st+'p',qi,st+'q')
    on(st+'q',(None,nx,{fp:qsvf}))
import pdf_fonts
NFC=len(FACES); OROOT=3+3*NFC; FIRST=OROOT+1; PUS=999000; PFT=999100   # faces used by this PDF, and where each face's bytes are in the read only part of the bank
PF_ROM=bytearray(); PF_INIT=[]
for i_,f_ in enumerate(FACES):
    bl_,o1_,o2_=pdf_fonts.face_blob(i_,*f_,3+3*i_)
    for j_,v_ in enumerate((len(PF_ROM)+1,len(bl_),o1_,o2_)): PF_INIT.append([PFT+i_*4+j_,v_])
    PF_ROM+=bl_
head=b'%PDF-1.4\n'; cat_=b'1 0 obj\n<</Type/Catalog/Pages 2 0 R/Outlines %d 0 R>>\nendobj\n'%OROOT
pfr=Ret('T4_PFR')
on('PDF',(None,'PD_h',{fp:0,embase:OUTB}))
lit('PD_h',head+cat_,'PD_x')
xw=WPort(1)
on('PD_x',(None,'PD_y',{xw:(as_x(XR)+1,len(head)),qi:0}))
e=S('PD_y')
on('PD_y',(net.ge(qi,NFC,e),'PD_y2',None),(None,'PD_y',{xw:(as_x(PUS)+qi,0),w1:(as_x(XR)+qi*3+3,0),w2:(as_x(XR)+qi*3+4,0),w3:(as_x(XR)+qi*3+5,0),qi:qi+1}))
on('PD_y2',(None,'T3_PQ0',{xw:(as_x(PUS),1),qp:0,qpg:0,qtop:0,qobj:FIRST,qfc:0,qf0:0,qfh:0}))
qln=R();qxc=R();qiw=R();qih=R();qpo=R();qxx=R();qcx0=R();qop=R();qund=R();qdel=R();qrise=R();qadv=R();qex=R();qind=R();qry=R();qrc=R();qpa=R();qpv=R();qri=R();qhi=R()
# open a page: page object then content object with a fixed width length
def pg_open(st,nx):
    n1=st+'a';n2=st+'b';n3=st+'c';n4=st+'d';n5=st+'e';n6=st+'f'
    on(st,(None,n1,{xw:(as_x(XR)+qobj,fp),qpg:qpg+1}))
    number(n1,qobj,n2)
    lit(n2,b' 0 obj\n<</Type/Page/Parent 2 0 R/MediaBox[0 0 ',n2+'x')
    numz(n2+'x',qpw*0.75,n2+'y'); lit(n2+'y',b' ',n2+'z'); numz(n2+'z',qph*0.75,n2+'u'); lit(n2+'u',b']/Contents ',n3)
    number(n3,qobj+1,n4)
    lit(n4,b' 0 R>>\nendobj\n',n5)
    on(n5,(None,n6,{xw:(as_x(XR)+qobj+1,fp)}))
    number(n6,qobj+1,n6+'g')
    lit(n6+'g',b' 0 obj\n<</Length ',n6+'h')
    on(n6+'h',(None,n6+'i',{qlenat:fp}))
    number(n6+'i',0,n6+'j')
    lit(n6+'j',b'>>\nstream\n',n6+'k')
    on(n6+'k',(None,n6+'l',{qstart:fp}))
    lit(n6+'l',b'.75 0 0 .75 0 0 cm\n',n6+'m')
    on(n6+'m',(None,'T4P_FU',{pfr.r:pfr.id(nx)}))
def pg_close(st,nx):
    n1=st+'a'
    on(st,(None,'T4P_NT',{qnr.r:qnr.id(st+'z')}))
    lit(st+'z',b'\nendstream\nendobj\n',n1)
    on(n1,(None,nx,{qcur:qlenat,qobj:qobj+2,qi:fp-qstart-18}))
    # length is patched digit by digit into the reserved field
pg_close('PD_C','PD_LP')
pd_patch('PD_LP','PD_LR')
e=S('PD_LR'); on('PD_LR',(net.ge(qp,npar,e),'PD_E',None),(None,'PD_O',None))
pg_open('PD_O','PD_L5')
pg_open('PD_0','PD_1')
# walk paragraphs using the saved layout
e=S('PD_1'); on('PD_1',(net.ge(qp,npar,e),'PD_C',None),(net.ge(fp,3800000,e),'PD_C',{qp:npar}),(None,'PD_2',{r1:as_x(PT)+qp}))
on('PD_2',(None,'T3_PQ2',{qb:R1,rmeta:R1+META}))
e=S('PD_3')
first_p=net.eq(qtop,0,e)
qyy0=rl.out[0]+G_(rp6.out[3],net.gt(rl.out[0],rl.out[1]+qmt,e))
qlb=net.bits(R2,4,e); qkind=qlb[0]+qlb[1]*2; qlvl=qlb[2]+qlb[3]*2
qk=R();ql=R();qmk=R()
qln_new,qmk_new=list_step(rl.out[4],qkind,qlvl,e)
pl_={qyy:qyy0,qcols:rc.out[0],qci:rc.out[1],qln:rl.out[4],qxc:rl.out[5],qk:qkind,ql:qlvl,qmk:qmk_new,qind:G_(qlvl*48+48,net.step(qkind))+net.eq(qtoc,2,e)*24,qiw:rim.out[0],qih:rim.out[1],qpo:rim.out[2]}
on('PD_3',(first_p,'PD_4',{**pl_,qtop:rl.out[1]}),
 (net.gt(rl.out[1],qtop,e),'PD_C',{**pl_,qtop:rl.out[1]}),
 (None,'PD_4',pl_))
on('PD_L5',(None,'PD_4',None))
on('PD_5',(None,'PD_6',{qnl:R1,qlj:0}))
e=S('PD_6'); on('PD_6',(net.ge(qlj,qnl,e),'PD_N',None),(None,'PD_7',{rl:qb+LINES+qlj*8,rc:qb+2062,r2:qb+LINES+qlj*8+11}))
e=S('PD_7'); e7=e
Wl=rl.out
gx7=G_(qcx+6,net.step(qcols))
tb7=net.step(qcols)
qnx_=qfh+Wl[7]+net.step(qfh+Wl[7])*14
ovf=net.or_(net.and_(net.gt(qyy+Wl[3]+qnx_,qtop+qmt+qth,e),net.gt(qyy,qtop+qmt,e)),net.and_(ONE-tb7,keep_lines(e,qyy,qtop,Wl[3],R2,qlj,qnl,qmt,qth,qnx_)))
lmv={qs:Wl[0],qe:Wl[1],rv_qm:gx7+qml,qx:Wl[2]-48+gx7+qml,qh:Wl[3],qa:Wl[4],qo:Wl[0],qex:Wl[5]}
col2=net.and_(ovf,net.eq(qnc,2,e),ONE-net.step(qxc))
on('PD_7',(col2,'PD_8',{**lmv,qyy:qtop+qmt,qxc:(qtw-24)*0.5+24}),(ovf,'PD_C2',{**lmv,qyy:qtop+qps+qmt,qtop:qtop+qps,qxc:0}),(None,'PD_8',lmv))
pg_close('PD_C2','PD_QH')
pd_patch('PD_QH','PD_O2')
pg_open('PD_O2','PD_8')
# one text line: positioned chunks of a word and its trailing space, in screen pixels
qhl=R(); qsty=R(); qyb=qph-(qyy-qtop+qa); qpc=R()
e=S('PD_8')
on('PD_8',(None,'A6P_B0',None))
on('PD_R',(net.step(qiw),'T4P_IM',None),(None,'PD_9',{qsty:999999,qop:0,qxx:qx+qind+qxc,qpc:0}))
e=S('PD_9'); on('PD_9',(net.ge(qo,qe,e),'PD_Z',None),(None,'PD_A',{r1:qb+qo,rs:qb+1024+qo}))
e=S('PD_A'); measure(e,R1,RSR,RSC); ke3=net.and_(e,net.step(qpc)); kp_en.lin(ke3); kp_in.add(ke3,qpc)
pdiff=net.step(net.step(RSC-qsty)+net.step(qsty-RSC)); psp=net.eq(R1,32,e)
ladv={ins_ch:R1,ins_st:RSC,ins_rec:RSR,qadv:adv+kern+G_(qex,psp)+rv_tabw(qxx-rv_qm-qxc,net.eq(R1,9,e)),qpc:R1}
on('PD_A',(net.and_(net.eq(R1,9,e),qop),'T4P_CL',{pfcr.r:pfcr.id('A4_QX0')}),(net.eq(R1,9,e),'A4_QX0',None),(net.and_(net.ge(R1,300,e),net.lt(R1,1000,e)),'A6Q_P0',{qo:qo+1,a6qk:R1-300}),(net.ge(R1,1000,e),'T4P_MK',{qo:qo+1,qfid:R1-1000}),(net.and_(pdiff,qop),'T4P_CL',{**ladv,pfcr.r:pfcr.id('PD_F')}),(pdiff,'PD_F',ladv),(qop,'PD_Tc',ladv),(None,'T4P_O',ladv))
sv_en.lin(S('PD_F')); sv_in.add(S('PD_F'),ins_rec); sv_fl.add(S('PD_F'),ins_st)
e=S('PD_F'); zh=net.decode(SV['si'],rom.NSZ,e); pts=X(); ptv=X()
for i_,h_ in enumerate(zh): pts=pts+h_*round(rom.SZ[i_]*96/72); ptv=ptv+h_*round(rom.SZ[script_size(i_)]*96/72)
ptk=net.or_(SV['ins'],SV['dele']); vf_=net.step(SV['sup']+SV['sub'])
_pfh=net.decode(SV['font'],len(rom.FAM),e); _pfv=X()
for ff_,h_ in enumerate(_pfh):
    for bo_,bb_ in enumerate((ONE-SV['bold'],SV['bold'])):
        for it_,ii_ in enumerate((ONE-SV['ital'],SV['ital'])):
            k_=FACES.index(rom.face_of(ff_,bo_,it_))
            if k_: _pfv=_pfv+net.and_(h_,bb_,ii_)*k_
on('PD_F',(None,'PD_Fa',{qsty:ins_st,qfn:_pfv,qsz:G_(pts,ONE-vf_)+G_(ptv,vf_),qbase:G_(SV['color'],ONE-ptk)+ptk*4,qund:net.or_(SV['und'],SV['ins']),qdel:net.or_(SV['dele'],SV['strike']),qrise:SV['sup']*5+net.and_(e,ONE-SV['sub'])*3,qhl:SV['hl']}))
lit('PD_Fa',b'/F','PD_Fb')
e=S('PD_Fb'); on('PD_Fb',(None,'PD_Fc',{xw:(as_x(PUS)+qfn,1)}))
em_en.lin(e); em_b.add(e,48+qfn+net.ge(qfn,10,e)*7)     # font names /F0 to /F9, /FA and on
lit('PD_Fc',b' ','PD_Fd')
number('PD_Fd',qsz,'PD_Fe')
lit('PD_Fe',b' Tf ','PD_Ff')
PCS=[('%.2f %.2f %.2f rg\n'%(c_[0]/255,c_[1]/255,c_[2]/255)).encode() for c_ in PAL_F]; _pcb=rom_str(b''.join(PCS)); _pcl=len(PCS[0])
on('PD_Ff',(None,'A10_B0',{la_:as_x(_pcb)+qbase*_pcl,ln_lit:_pcl,lbret.r:lbret.id('T4P_O')}))
on('T4P_O',(None,'T4P_Oa',{qcx0:qxx,qop:1}))
lit('T4P_Oa',b'BT 1 0 0 1 ','T4P_Ob'); number('T4P_Ob',qxx,'T4P_Oc'); lit('T4P_Oc',b' ','T4P_Od')
number('T4P_Od',qyb+qrise-3,'T4P_Oe'); lit('T4P_Oe',b' Tm (','PD_Tc')
e=S('PD_Tc'); esc=net.or_(net.eq(ins_ch,40,e),net.eq(ins_ch,41,e),net.eq(ins_ch,92,e))
on('PD_Tc',(esc,'PD_Te',None),(None,'PD_Td',None))
lit('PD_Te',b'\\','PD_Td')
e=S('PD_Td'); em_en.lin(e); em_b.add(e,ins_ch+net.eq(ins_ch,9,e)*23+net.eq(ins_ch,11,e)*21)
on('PD_Td',(None,'PD_Tg',{qo:qo+1,qxx:qxx+qadv}))
e=S('PD_Tg')
on('PD_Tg',(net.or_(net.eq(ins_ch,32,e),net.eq(ins_ch,9,e)),'T4P_CL',{pfcr.r:pfcr.id('PD_9')}),(None,'PD_9',None))
# closing a chunk draws its underline or strike line
on('T4P_CL',(None,'T4P_Ca',{qop:0}))
lit('T4P_Ca',b')Tj ET\n','T4P_C2')
on('T4P_C2',(net.step(qhl),'A6P_FH',None),(None,'A6P_U',None))
number('T4P_Ra',qcx0,'T4P_Rb'); lit('T4P_Rb',b' ','T4P_Rc'); number('T4P_Rc',qry,'T4P_Rd'); lit('T4P_Rd',b' ','T4P_Re'); number('T4P_Re',qxx-qcx0,'T4P_Rf'); lit('T4P_Rf',b' 1 re f\n','T4_PFC')
on('PD_Z',(qop,'T4P_CL',{pfcr.r:pfcr.id('PD_Y')}),(None,'PD_Y',None))
e=S('PD_Y'); on('PD_Y',(net.and_(net.step(qtoc),net.ge(qlj+1,qnl,e)),'T4P_TD0',None),(None,'PD_6',{qyy:qyy+qh,qlj:qlj+1}))
# a table of contents entry: dot leader and the live page number, as on the screen
on('T4P_TD0',(None,'T4P_TD1',{r1:qsrc+SAVE+2}))
e=S('T4P_TD1'); hs_=net.step(qsrc); tv_=G_(R1,hs_)+G_(qtpg,ONE-hs_); DW0_=rom.adv_px(0,0,0,0,48); DOTW_=rom.adv_px(0,0,0,0,46)+2
on('T4P_TD1',(None,'T4P_TD2',{qtpv:tv_,qtxe:qml+qtw-(net.ge(tv_,10,e)+net.ge(tv_,100,e)+1)*DW0_-4}))
e=S('T4P_TD2'); on('T4P_TD2',(net.ge(qxx+DOTW_,qtxe,e),'T4P_TN',None),(None,'T4P_TD3',None))
lit('T4P_TD3',b'BT /F0 15 Tf 0 0 0 rg 1 0 0 1 ','T4P_TD4'); number('T4P_TD4',qxx,'T4P_TD5'); lit('T4P_TD5',b' ','T4P_TD6'); number('T4P_TD6',qyb,'T4P_TD7'); lit('T4P_TD7',b' Tm (.)Tj ET\n','T4P_TD8')
on('T4P_TD8',(None,'T4P_TD2',{qxx:qxx+DOTW_}))
lit('T4P_TN',b'BT /F0 15 Tf 0 0 0 rg 1 0 0 1 ','T4P_TN1'); number('T4P_TN1',qtxe+4,'T4P_TN2'); lit('T4P_TN2',b' ','T4P_TN3'); number('T4P_TN3',qyb,'T4P_TN4'); lit('T4P_TN4',b' Tm (','T4P_TN5'); numz('T4P_TN5',qtpv,'T4P_TN6'); lit('T4P_TN6',b')Tj ET\n','T4P_TN7')
on('T4P_TN7',(None,'PD_6',{qyy:qyy+qh,qlj:qlj+1}))
# a footnote marker: note the id for the page foot, close the chunk, set the number raised
on('T4P_MK',(qop,'T4P_CL',{pfcr.r:pfcr.id('T4P_M1')}),(None,'T4P_M1',None))
on('T4P_M1',(None,'T4P_M2',{w1:(as_x(PDFN)+qfc,qfid),qfc:qfc+1,r2:as_x(FNB)+qfid*256+254}))
on('T4P_M2',(None,'T4P_M3',{qfh:qfh+R2}))
lit('T4P_M3',b'BT /F0 10 Tf 0 0 0 rg 1 0 0 1 ','T4P_M4'); number('T4P_M4',qxx,'T4P_M5'); lit('T4P_M5',b' ','T4P_M6'); number('T4P_M6',qyb+6,'T4P_M7'); lit('T4P_M7',b' Tm (','T4P_M8'); numz('T4P_M8',qfc,'T4P_M9'); lit('T4P_M9',b')Tj ET\n','T4P_Ma')
on('T4P_Ma',(None,'PD_9',{qxx:qxx+8,qsty:999999,qop:0}))
# page foot: a rule, then the notes of this page wrapped as on the screen
e=S('T4P_NT'); on('T4P_NT',(net.lt(qf0,qfc,e),'T4P_N0',{wdy:qmt+qth-qfh,qfi:qf0}),(None,'T4P_NR',None))
lit('T4P_N0',b'0 0 0 rg ','T4P_N1'); number('T4P_N1',qml,'T4P_N2'); lit('T4P_N2',b' ','T4P_N3'); number('T4P_N3',qph-(wdy-6),'T4P_N4'); lit('T4P_N4',b' 200 1 re f\n','T4P_NL')
e=S('T4P_NL'); on('T4P_NL',(net.ge(qfi,qfc,e),'T4P_NR',{qf0:qfc,qfh:0}),(None,'T4P_NA',{r1:as_x(PDFN)+qfi}))
on('T4P_NA',(None,'T4P_NB',{wb_:as_x(FNB)+R1*256,r2:as_x(FNB)+R1*256+255}))
on('T4P_NB',(None,'T4P_NC',{wl_:R2}))
lit('T4P_NC',b'BT /F0 13 Tf 0 0 0 rg 1 0 0 1 ','T4P_ND'); number('T4P_ND',qml,'T4P_NE'); lit('T4P_NE',b' ','T4P_NF'); number('T4P_NF',qph-wdy-A9,'T4P_NG'); lit('T4P_NG',b' Tm (','T4P_NH'); numz('T4P_NH',qfi+1,'T4P_NI'); lit('T4P_NI',b')Tj ET\n','T4P_NJ')
on('T4P_NJ',(None,'T3_W',{wdx:qml+20,wdw:qtw-22,wdd:2,wbgf:0,qfi:qfi+1,wret_.r:wret_.id('T4P_NL')}))
# a picture as an inline image with hex filter; the cells hold packed RGB
lit('T4P_IM',b'q ','T4P_I1'); number('T4P_I1',qiw,'T4P_I2'); lit('T4P_I2',b' 0 0 ','T4P_I3'); number('T4P_I3',qih,'T4P_I4'); lit('T4P_I4',b' ','T4P_I5')
number('T4P_I5',qx+qind+qxc,'T4P_I6'); lit('T4P_I6',b' ','T4P_I7'); number('T4P_I7',qph-(qyy-qtop)-qih,'T4P_I8'); lit('T4P_I8',b' cm\nBI /W ','T4P_I9')
number('T4P_I9',qiw,'T4P_Ia'); lit('T4P_Ia',b' /H ','T4P_Ib'); number('T4P_Ib',qih,'T4P_Ic'); lit('T4P_Ic',b' /CS /RGB /BPC 8 /F /AHx ID\n','T4P_Id')
on('T4P_Id',(None,'T4P_P0',{qri:0,qrc:0,qpa:as_x(IMG0)+qpo}))
e=S('T4P_P0')
on('T4P_P0',(net.or_(net.ge(qrc,qih,e),net.ge(fp,3980000,e)),'T4P_PE',None),(net.ge(qri,qiw,e),'T4P_P0',{qri:0,qrc:qrc+1}),(None,'T4P_P1',{r1:qpa}))
on('T4P_P1',(None,'T4P_H0',{qpv:R1,qpa:qpa+1,qri:qri+1}))
for i_ in range(6):
    st=f'T4P_H{i_}'; e=S(st); bt=net.bits(qpv,24,e); sh=(4,0,12,8,20,16)[i_]   # R, G, B, high digit first
    nib=bt[sh]+bt[sh+1]*2+bt[sh+2]*4+bt[sh+3]*8
    em_en.lin(e); em_b.add(e,48+nib+net.ge(nib,10,e)*7)
    on(st,(None,f'T4P_H{i_+1}' if i_<5 else 'T4P_P0',None))
lit('T4P_PE',b'>\nEI Q\n','PD_Y')
e=S('PD_N'); tbl=net.and_(net.step(qcols),net.lt(qci+1,qcols,e))
on('PD_N',(None,'PD_1',{qp:qp+1,qyy:qyy+11}))
# after the last stream: pages tree, xref, trailer
# the faces this PDF used: each one is copied out of the read only part of the bank, a block per tick
qaddr=R();qrem=R();qn_=R()
on('PD_E',(None,'PF_0',{qi:0}))
e=S('PF_0'); on('PF_0',(net.ge(qi,NFC,e),'PF_E',None),(None,'PF_1',{r1:as_x(PUS)+qi}))
e=S('PF_1'); on('PF_1',(net.step(R1),'PF_2',{rl:as_x(PFT)+qi*4}),(None,'PF_0',{qi:qi+1}))
on('PF_2',(None,'PF_3',{qaddr:as_x(FROMB-1)+RL[0],qrem:RL[1],xw:(as_x(XR)+qi*3+3,fp),w1:(as_x(XR)+qi*3+4,fp+RL[2]),w2:(as_x(XR)+qi*3+5,fp+RL[3])}))
e=S('PF_3'); on('PF_3',(net.step(qrem),'PF_4',{rb:(qaddr,net.min_(qrem,1000)),qn_:net.min_(qrem,1000)}),(None,'PF_0',{qi:qi+1}))
on('PF_4',(None,'PF_3',{wb:(as_x(OUTB)+fp,qn_),fp:fp+qn_,qaddr:qaddr+qn_,qrem:qrem-qn_}))
on('PF_E',(None,'PD_E1',{xw:(as_x(XR)+2,fp)}))
# page furniture: header text and footer page number, same places as the screen
A9=rom.metrics(9)[0]
qfb=R();qfl=R();qfy=R();qfk=R()
e=S('T4P_FU'); fp1=net.and_(hftp,net.eq(qpg,1,e))
on('T4P_FU',(fp1,'T4P_F1',{qfb:as_x(HFB)+256,qfl:hfl[1],qfy:qph-48-A9,qfk:0}),(None,'T4P_F1',{qfb:as_x(HFB),qfl:hfl[0],qfy:qph-48-A9,qfk:0}))
e=S('T4P_F1'); on('T4P_F1',(net.eq(qfl,0,e),'T4P_FN',None),(None,'T4P_Fa',None))
lit('T4P_Fa',b'BT /F0 15 Tf .33 .33 .33 rg 1 0 0 1 ','T4P_Fb'); number('T4P_Fb',qml,'T4P_Fx0'); lit('T4P_Fx0',b' ','T4P_Fc'); number('T4P_Fc',qfy,'T4P_Fx1'); lit('T4P_Fx1',b' Tm (','T4P_Fd0')
on('T4P_Fd0',(None,'T4P_Fd',{qhi:0}))
e=S('T4P_Fd'); on('T4P_Fd',(net.ge(qhi,qfl,e),'T4P_Fg',None),(None,'T4P_Fe',{r1:qfb+qhi}))
e=S('T4P_Fe'); esc2=net.or_(net.eq(R1,40,e),net.eq(R1,41,e),net.eq(R1,92,e))
on('T4P_Fe',(net.eq(R1,1,e),'T4P_Fp',{qhi:qhi+1}),(esc2,'T4P_Ff',{qcur:R1}),(None,'T4P_Fh',{qcur:R1}))
on('T4P_Fp',(None,'A4_QP0',None))
lit('T4P_Ff',b'\\','T4P_Fh')
e=S('T4P_Fh'); em_en.lin(e); em_b.add(e,qcur); on('T4P_Fh',(None,'T4P_Fd',{qhi:qhi+1}))
lit('T4P_Fg',b')Tj ET\n','T4P_FN')
e=S('T4P_FN'); fp2=net.and_(hftp,net.eq(qpg,1,e))
on('T4P_FN',(net.step(qfk),'T4_PFR',None),(fp2,'T4P_F1',{qfb:as_x(HFB)+768,qfl:hfl[3],qfy:as_x(60)-A9,qfk:1}),(None,'T4P_F1',{qfb:as_x(HFB)+512,qfl:hfl[2],qfy:as_x(60)-A9,qfk:1}))
lit('PD_E1',b'2 0 obj\n<</Type/Pages/MediaBox[0 0 612 792]/Resources<</ExtGState<</M<</BM/Multiply>>>>/Font<<','PR_0')
for i_ in range(NFC):
    on(f'PR_{i_}',(None,f'PRa_{i_}',{r1:PUS+i_}))
    nx_=f'PR_{i_+1}' if i_+1<NFC else 'PR_E'
    on(f'PRa_{i_}',(net.step(R1),f'PRb_{i_}',None),(None,nx_,None))
    lit(f'PRb_{i_}',('/F%s %d 0 R'%(chr(48+i_+(7 if i_>=10 else 0)),3+3*i_)).encode(),nx_)
lit('PR_E',b'>>>>/Count ','PD_E2')
number('PD_E2',qpg,'PD_E3')
lit('PD_E3',b'/Kids[','PD_K0')
on('PD_K0',(None,'PD_K1',{qi:FIRST}))
e=S('PD_K1'); on('PD_K1',(net.ge(qi,qobj,e),'PD_K9',None),(None,'PD_K2',None))
number('PD_K2',qi,'PD_K3'); lit('PD_K3',b' 0 R ','PD_K4')
on('PD_K4',(None,'PD_K1',{qi:qi+2}))
lit('PD_K9',b']>>\nendobj\n','A6P_F0')
on('PD_X0',(None,'PD_X1',{qxr:fp}))
lit('PD_X1',b'xref\n0 ','PD_X2')
number('PD_X2',qobj,'PD_X3')
lit('PD_X3',b'\n0000000000 65535 f \n','PD_X4')
on('PD_X4',(None,'PD_X5',{qi:1}))
e=S('PD_X5'); on('PD_X5',(net.ge(qi,qobj,e),'PD_T0',None),(None,'PD_X6',{r1:as_x(XR)+qi}))
e=S('PD_X6'); on('PD_X6',(net.eq(R1,0,e),'PD_Xf',None),(None,'PD_X6b',{qcur:R1}))
lit('PD_Xf',b'0000000000 65535 f \n','PD_X9')
lit('PD_X6b',b'000','PD_X7')
number('PD_X7',qcur,'PD_X8')
lit('PD_X8',b' 00000 n \n','PD_X9')
on('PD_X9',(None,'PD_X5',{qi:qi+1}))
lit('PD_T0',b'trailer\n<</Size ','PD_T1')
number('PD_T1',qobj,'PD_T2')
lit('PD_T2',b'/Root 1 0 R>>\nstartxref\n','PD_T3')
number('PD_T3',qxr,'PD_T4')
lit('PD_T4',b'\n%%EOF\n','PD_END')
pdfl=R(); on('PD_END',(None,'HALT',{pdfl:fp}))
pdfout=Bus(net); pdfout.add(S('HF'),pdfl); fsm.set(pdfl,S('HF'),0)
exec(open('rv_a6_pdf.py').read())
