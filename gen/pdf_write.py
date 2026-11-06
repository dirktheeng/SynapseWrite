# ---- PDF writer: objects, content streams and the xref table are all produced here ----
net.group('pdf writer')
XR=900000; nv=R(); nret=Ret('NR'); qp=R();qb=R();qyy=R();qtop=R();qlj=R();qnl=R();qcols=R();qci=R();qx=R();qh=R();qa=R();qs=R();qe=R();qo=R();qst=R();qpg=R();qstart=R();qlenat=R();qobj=R();qi=R();qxr=R();qcur=R()
qsz=R();qfn=R();qbase=R()
pfc=Ret('T4_PFC')
def number(st,val,nx):
    on(st,(None,'NUM7',{nv:val,nret.r:nret.id(nx)}))
cur_n='NUM7'
for pw_ in (1000000,100000,10000,1000,100,10,1):
    nx_=f'NUMd{pw_}' if pw_>1 else 'NR'
    e=S(cur_n); val=net.gate(nv,e)
    for big in (1000000,100000,10000,1000,100,10):
        if big>pw_:
            dd=X()
            for t in range(1,10): dd=dd+net.step(val-big*t+0.5)
            val=val-dd*big
    dg=X()
    for t in range(1,10): dg=dg+net.step(val-pw_*t+0.5)
    em_en.lin(e); em_b.add(e,48+dg)
    on(cur_n,(None,nx_,None)); cur_n=nx_
import pdf_fonts
head=b'%PDF-1.4\n'
off=len(head); body=b''; offs={}
offs[1]=off+len(body); body+=b'1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n'
for ob_,bb_ in sorted(pdf_fonts.objects(3,11).items()):
    offs[ob_]=off+len(body); body+=bb_
FIRST=27
pfr=Ret('T4_PFR')
on('PDF',(None,'PD_h',{fp:0,embase:OUTB}))
lit('PD_h',head+body,'PD_x')
xw=WPort(1)
seq=sorted(offs.items())
cur_n='PD_x'
for i_,(ob_,of_) in enumerate(seq):
    nx_=f'PD_x{i_}'
    on(cur_n,(None,nx_,{xw:(as_x(XR)+ob_,of_)})); cur_n=nx_
on(cur_n,(None,'PD_0',{qp:0,qpg:0,qtop:0,qobj:FIRST}))
qlsf=R();qln=R();qxc=R();qpw=R();qph=R();qpo=R();qxx=R();qcx0=R();qop=R();qund=R();qdel=R();qrise=R();qadv=R();qex=R();qind=R();qry=R();qrc=R();qpa=R();qpv=R();qri=R();qhi=R()
# open a page: page object then content object with a fixed width length
def pg_open(st,nx):
    n1=st+'a';n2=st+'b';n3=st+'c';n4=st+'d';n5=st+'e';n6=st+'f'
    on(st,(None,n1,{xw:(as_x(XR)+qobj,fp),qpg:qpg+1}))
    number(n1,qobj,n2)
    lit(n2,b' 0 obj\n<</Type/Page/Parent 2 0 R/Contents ',n3)
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
    lit(st,b'\nendstream\nendobj\n',n1)
    on(n1,(None,nx,{qcur:qlenat,nv:0,qobj:qobj+2,qi:fp-qstart-18}))
    # length is patched digit by digit into the reserved field
pg_close('PD_C','PD_LP')
# patch seven digits: units of qi at qlenat
cur_n='PD_LP'
for k_,pw_ in enumerate((1000000,100000,10000,1000,100,10,1)):
    nx_=f'PD_LP{k_}' if pw_>1 else 'PD_LR'
    e=S(cur_n); val=net.gate(qi,e)
    for big in (1000000,100000,10000,1000,100,10):
        if big>pw_:
            dd=X()
            for t in range(1,10): dd=dd+net.step(val-big*t+0.5)
            val=val-dd*big
    dg=X()
    for t in range(1,10): dg=dg+net.step(val-pw_*t+0.5)
    on(cur_n,(None,nx_,{fw2:(as_x(OUTB)+qlenat+k_,48+dg)})); cur_n=nx_
e=S('PD_LR'); on('PD_LR',(net.ge(qp,npar,e),'PD_E',None),(None,'PD_O',None))
pg_open('PD_O','PD_L5')
pg_open('PD_0','PD_1')
# walk paragraphs using the saved layout
e=S('PD_1'); on('PD_1',(net.ge(qp,npar,e),'PD_C',None),(net.ge(fp,3800000,e),'PD_C',{qp:npar}),(None,'PD_2',{r1:as_x(PT)+qp}))
on('PD_2',(None,'PD_3',{qb:R1,rl:R1+SAVE,rc:R1+2062,rim:R1+IMF,r2:R1+LIST}))
e=S('PD_3')
first_p=net.eq(qtop,0,e)
pl_={qyy:rl.out[0],qcols:rc.out[0],qci:rc.out[1],qln:rl.out[4],qxc:rl.out[5],qlsf:R2,qind:net.step(R2)*48,qpw:rim.out[0],qph:rim.out[1],qpo:rim.out[2]}
on('PD_3',(first_p,'PD_4',{**pl_,qtop:rl.out[1]}),
 (net.gt(rl.out[1],qtop,e),'PD_C',{**pl_,qtop:rl.out[1]}),
 (None,'PD_4',pl_))
on('PD_L5',(None,'PD_4',None))
on('PD_4',(None,'PD_5',{r1:qb+NLINES}))
on('PD_5',(None,'PD_6',{qnl:R1,qlj:0}))
e=S('PD_6'); on('PD_6',(net.ge(qlj,qnl,e),'PD_N',None),(None,'PD_7',{rl:qb+LINES+qlj*8,rc:qb+2062}))
e=S('PD_7'); e7=e
Wl=rl.out
tb7=net.step(rc.out[0]); hc7=net.decode(rc.out[0],9,e7); hi7=net.decode(rc.out[1],9,e7); gx7=X()
for cc_ in range(1,9):
    for ii_ in range(cc_): gx7=gx7+net.and_(net.step(hc7[cc_]),net.step(hi7[ii_]))*(ii_*(TW//cc_)+6)
ovf=net.and_(net.gt(qyy+Wl[3],qtop+960,e),net.gt(qyy,qtop+96,e))
lmv={qs:Wl[0],qe:Wl[1],qx:Wl[2]-48+gx7+96,qh:Wl[3],qa:Wl[4],qo:Wl[0],qex:Wl[5]}
col2=net.and_(ovf,net.eq(ncol,2,e),ONE-net.step(qxc))
on('PD_7',(col2,'PD_8',{**lmv,qyy:qtop+96,qxc:324}),(ovf,'PD_C2',{**lmv,qyy:qtop+PST+96,qtop:qtop+PST,qxc:0}),(None,'PD_8',lmv))
pg_close('PD_C2','PD_QH')
cur_n='PD_QH'
for k_,pw_ in enumerate((1000000,100000,10000,1000,100,10,1)):
    nx_=f'PD_LQ{k_}' if pw_>1 else 'PD_O2'
    e=S(cur_n); val=net.gate(qi,e)
    for big in (1000000,100000,10000,1000,100,10):
        if big>pw_:
            dd=X()
            for t in range(1,10): dd=dd+net.step(val-big*t+0.5)
            val=val-dd*big
    dg=X()
    for t in range(1,10): dg=dg+net.step(val-pw_*t+0.5)
    on(cur_n,(None,nx_,{fw2:(as_x(OUTB)+qlenat+k_,48+dg)})); cur_n=nx_
pg_open('PD_O2','PD_8')
# one text line: positioned chunks of a word and its trailing space, in screen pixels
qsty=R(); qyb=as_x(1056)-(qyy-qtop+qa)
e=S('PD_8')
on('PD_8',(net.and_(net.eq(qs,0,e),net.eq(qlsf,1,e)),'T4P_BU',None),(net.and_(net.eq(qs,0,e),net.eq(qlsf,2,e)),'T4P_NU',None),(None,'PD_R',None))
on('PD_R',(net.step(qpw),'T4P_IM',None),(None,'PD_9',{qsty:999999,qop:0,qxx:qx+qind+qxc}))
e=S('PD_9'); on('PD_9',(net.ge(qo,qe,e),'PD_Z',None),(None,'PD_A',{r1:qb+qo,r2:qb+1024+qo}))
e=S('PD_A'); measure(e,R1,R2)
pdiff=net.step(net.step(R2-qsty)+net.step(qsty-R2)); psp=net.eq(R1,32,e)
ladv={ins_ch:R1,ins_st:R2,qadv:adv+G_(qex,psp)}
on('PD_A',(net.and_(pdiff,qop),'T4P_CL',{**ladv,pfc.r:pfc.id('PD_F')}),(pdiff,'PD_F',ladv),(qop,'PD_Tc',ladv),(None,'T4P_O',ladv))
sv_en.lin(S('PD_F')); sv_in.add(S('PD_F'),ins_st)
e=S('PD_F'); zh=net.decode(SV['size'],11,e); pts=X()
for i_,h_ in enumerate(zh): pts=pts+h_*round(rom.PTS[i_]*96/72)
ptk=net.or_(SV['ins'],SV['dele'])
on('PD_F',(None,'PD_Fa',{qsty:ins_st,qfn:SV['bold']+SV['ital']*2+SV['font']*4+3,qsz:pts,qbase:G_(SV['color'],ONE-ptk)+ptk*4,qund:net.or_(SV['und'],SV['ins']),qdel:SV['dele'],qrise:SV['sup']*5+net.and_(e,ONE-SV['sub'])*3}))
lit('PD_Fa',b'/F','PD_Fb')
e=S('PD_Fb'); on('PD_Fb',(None,'PD_Fc',None))
em_en.lin(e); em_b.add(e,48+qfn-3)
lit('PD_Fc',b' ','PD_Fd')
number('PD_Fd',qsz,'PD_Fe')
lit('PD_Fe',b' Tf ','PD_Ff')
e=S('PD_Ff'); ch8=net.decode(qbase,8,e)
PCS=['0 0 0','.35 .35 .35','1 1 1','.17 .34 .6','.75 0 0','0 .5 .24','.9 .47 0','.44 .19 .63']
on('PD_Ff',*[(ch8[j],f'PD_Co{j}',None) for j in range(8)],(None,'T4P_O',None))
for j,pc_ in enumerate(PCS): lit(f'PD_Co{j}',(pc_+' rg\n').encode(),'T4P_O')
on('T4P_O',(None,'T4P_Oa',{qcx0:qxx,qop:1}))
lit('T4P_Oa',b'BT 1 0 0 1 ','T4P_Ob'); number('T4P_Ob',qxx,'T4P_Oc'); lit('T4P_Oc',b' ','T4P_Od')
number('T4P_Od',qyb+qrise-3,'T4P_Oe'); lit('T4P_Oe',b' Tm (','PD_Tc')
e=S('PD_Tc'); esc=net.or_(net.eq(ins_ch,40,e),net.eq(ins_ch,41,e),net.eq(ins_ch,92,e))
on('PD_Tc',(esc,'PD_Te',None),(None,'PD_Td',None))
lit('PD_Te',b'\\','PD_Td')
e=S('PD_Td'); em_en.lin(e); em_b.add(e,ins_ch)
on('PD_Td',(None,'PD_Tg',{qo:qo+1,qxx:qxx+qadv}))
e=S('PD_Tg')
on('PD_Tg',(net.eq(ins_ch,32,e),'T4P_CL',{pfc.r:pfc.id('PD_9')}),(None,'PD_9',None))
# closing a chunk draws its underline or strike line
on('T4P_CL',(None,'T4P_Ca',{qop:0}))
lit('T4P_Ca',b')Tj ET\n','T4P_C2')
on('T4P_C2',(qdel,'T4P_Ra',{qry:qyb+5}),(qund,'T4P_Ra',{qry:qyb-2}),(None,'T4_PFC',None))
number('T4P_Ra',qcx0,'T4P_Rb'); lit('T4P_Rb',b' ','T4P_Rc'); number('T4P_Rc',qry,'T4P_Rd'); lit('T4P_Rd',b' ','T4P_Re'); number('T4P_Re',qxx-qcx0,'T4P_Rf'); lit('T4P_Rf',b' 1 re f\n','T4_PFC')
on('PD_Z',(qop,'T4P_CL',{pfc.r:pfc.id('PD_Y')}),(None,'PD_Y',None))
on('PD_Y',(None,'PD_6',{qyy:qyy+qh,qlj:qlj+1}))
# list markers
lit('T4P_BU',b'BT /F0 15 Tf 0 0 0 rg 1 0 0 1 ','T4P_Bb'); number('T4P_Bb',qx+qind+qxc-20,'T4P_Bc'); lit('T4P_Bc',b' ','T4P_Bd'); number('T4P_Bd',qyb,'T4P_Be'); lit('T4P_Be',b' Tm (\\225)Tj ET\n','PD_R')
lit('T4P_NU',b'BT /F0 15 Tf 0 0 0 rg 1 0 0 1 ','T4P_Nb'); number('T4P_Nb',qx+qind+qxc-32,'T4P_Nc'); lit('T4P_Nc',b' ','T4P_Nd'); number('T4P_Nd',qyb,'T4P_Ne'); lit('T4P_Ne',b' Tm (','T4P_Nf')
e=S('T4P_Nf'); tn_=X()
for t in range(1,10): tn_=tn_+net.ge(qln,t*10,e)
em_en.lin(e); em_b.add(e,48+tn_)
on('T4P_Nf',(None,'T4P_Ng',None))
e=S('T4P_Ng'); tn_=X()
for t in range(1,10): tn_=tn_+net.ge(qln,t*10,e)
em_en.lin(e); em_b.add(e,48+qln-tn_*10)
on('T4P_Ng',(None,'T4P_Nh',None))
lit('T4P_Nh',b'.)Tj ET\n','PD_R')
# a picture as an inline image with hex filter; the cells hold packed RGB
lit('T4P_IM',b'q ','T4P_I1'); number('T4P_I1',qpw,'T4P_I2'); lit('T4P_I2',b' 0 0 ','T4P_I3'); number('T4P_I3',qph,'T4P_I4'); lit('T4P_I4',b' ','T4P_I5')
number('T4P_I5',qx+qind+qxc,'T4P_I6'); lit('T4P_I6',b' ','T4P_I7'); number('T4P_I7',as_x(1056)-(qyy-qtop)-qph,'T4P_I8'); lit('T4P_I8',b' cm\nBI /W ','T4P_I9')
number('T4P_I9',qpw,'T4P_Ia'); lit('T4P_Ia',b' /H ','T4P_Ib'); number('T4P_Ib',qph,'T4P_Ic'); lit('T4P_Ic',b' /CS /RGB /BPC 8 /F /AHx ID\n','T4P_Id')
on('T4P_Id',(None,'T4P_P0',{qri:0,qrc:0,qpa:as_x(IMG0)+qpo}))
e=S('T4P_P0')
on('T4P_P0',(net.or_(net.ge(qrc,qph,e),net.ge(fp,3980000,e)),'T4P_PE',None),(net.ge(qri,qpw,e),'T4P_P0',{qri:0,qrc:qrc+1}),(None,'T4P_P1',{r1:qpa}))
on('T4P_P1',(None,'T4P_H0',{qpv:R1,qpa:qpa+1,qri:qri+1}))
for i_ in range(6):
    st=f'T4P_H{i_}'; e=S(st); bt=net.bits(qpv,24,e); sh=20-4*i_
    nib=bt[sh]+bt[sh+1]*2+bt[sh+2]*4+bt[sh+3]*8
    em_en.lin(e); em_b.add(e,48+nib+net.ge(nib,10,e)*7)
    on(st,(None,f'T4P_H{i_+1}' if i_<5 else 'T4P_P0',None))
lit('T4P_PE',b'>\nEI Q\n','PD_Y')
e=S('PD_N'); tbl=net.and_(net.step(qcols),net.lt(qci+1,qcols,e))
on('PD_N',(None,'PD_1',{qp:qp+1,qyy:qyy+11}))
# after the last stream: pages tree, xref, trailer
on('PD_E',(None,'PD_E1',{xw:(as_x(XR)+2,fp)}))
res=b''.join(('/F%d %d 0 R'%(i_,3+i_)).encode() for i_ in range(8))
# page furniture: header text and footer page number, same places as the screen
A9=rom.metrics(9)[0]
lit('T4P_FU',b'BT /F0 12 Tf .35 .35 .35 rg 1 0 0 1 96 ','T4P_Fa'); number('T4P_Fa',as_x(1056-48-A9),'T4P_Fb'); lit('T4P_Fb',b' Tm (','T4P_Fc')
on('T4P_Fc',(None,'T4P_Fd',{qhi:0}))
e=S('T4P_Fd'); on('T4P_Fd',(net.ge(qhi,hlen,e),'T4P_Fg',None),(None,'T4P_Fe',{r1:as_x(HD)+qhi}))
e=S('T4P_Fe'); esc2=net.or_(net.eq(R1,40,e),net.eq(R1,41,e),net.eq(R1,92,e))
on('T4P_Fe',(esc2,'T4P_Ff',{qcur:R1}),(None,'T4P_Fx',{qcur:R1}))
lit('T4P_Ff',b'\\','T4P_Fx')
e=S('T4P_Fx'); em_en.lin(e); em_b.add(e,qcur); on('T4P_Fx',(None,'T4P_Fd',{qhi:qhi+1}))
lit('T4P_Fg',b')Tj ET\nBT /F0 12 Tf 1 0 0 1 ','T4P_Fh')
e=S('T4P_Fh'); fx=as_x(400)+net.lt(qpg,10,e)*8
number('T4P_Fh',fx,'T4P_Fi')
lit('T4P_Fi',b' ','T4P_Fj'); number('T4P_Fj',as_x(1056-(PH-60)-A9),'T4P_Fk'); lit('T4P_Fk',b' Tm (','T4P_Fl')
e=S('T4P_Fl'); tp=X()
for t in range(1,13): tp=tp+net.ge(qpg,t*10,e)
on('T4P_Fl',(net.ge(qpg,10,e),'T4P_Fm',None),(None,'T4P_Fn',None))
em_en.lin(net.and_(e,net.ge(qpg,10,e))); em_b.add(net.and_(e,net.ge(qpg,10,e)),48+tp)
on('T4P_Fm',(None,'T4P_Fn',None))
e=S('T4P_Fn'); tp2=X()
for t in range(1,13): tp2=tp2+net.ge(qpg,t*10,e)
em_en.lin(e); em_b.add(e,48+qpg-tp2*10)
on('T4P_Fn',(None,'T4P_Fo',None))
lit('T4P_Fo',b')Tj ET\n','T4_PFR')
lit('PD_E1',b'2 0 obj\n<</Type/Pages/MediaBox[0 0 612 792]/Resources<</Font<<'+res+b'>>>>/Count ','PD_E2')
number('PD_E2',qpg,'PD_E3')
lit('PD_E3',b'/Kids[','PD_K0')
on('PD_K0',(None,'PD_K1',{qi:FIRST}))
e=S('PD_K1'); on('PD_K1',(net.ge(qi,qobj,e),'PD_K9',None),(None,'PD_K2',None))
number('PD_K2',qi,'PD_K3'); lit('PD_K3',b' 0 R ','PD_K4')
on('PD_K4',(None,'PD_K1',{qi:qi+2}))
lit('PD_K9',b']>>\nendobj\n','PD_X0')
on('PD_X0',(None,'PD_X1',{qxr:fp}))
lit('PD_X1',b'xref\n0 ','PD_X2')
number('PD_X2',qobj,'PD_X3')
lit('PD_X3',b'\n0000000000 65535 f \n','PD_X4')
on('PD_X4',(None,'PD_X5',{qi:1}))
e=S('PD_X5'); on('PD_X5',(net.ge(qi,qobj,e),'PD_T0',None),(None,'PD_X6',{r1:as_x(XR)+qi}))
on('PD_X6',(None,'PD_X6b',{qcur:R1}))
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
pdfout=Bus(net); pdfout.add(S('HALT'),pdfl); fsm.set(pdfl,S('HALT'),0)
