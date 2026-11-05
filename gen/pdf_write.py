# ---- PDF writer: objects, content streams and the xref table are all produced here ----
net.group('pdf writer')
XR=900000; nv=R(); nret=Ret('NR'); qp=R();qb=R();qyy=R();qtop=R();qlj=R();qnl=R();qcols=R();qci=R();qx=R();qh=R();qa=R();qs=R();qe=R();qo=R();qst=R();qpg=R();qstart=R();qlenat=R();qobj=R();qi=R();qxr=R();qcur=R()
qsz=R();qfn=R();qbase=R()
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
FONTS=['Helvetica','Helvetica-Bold','Helvetica-Oblique','Helvetica-BoldOblique','Times-Roman','Times-Bold','Times-Italic','Times-BoldItalic']
head=b'%PDF-1.4\n'
objs=[]
off=len(head); body=b''; offs={}
offs[1]=off+len(body); body+=b'1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n'
for i_,f_ in enumerate(FONTS):
    offs[3+i_]=off+len(body); body+=('%d 0 obj\n<</Type/Font/Subtype/Type1/BaseFont/%s/Encoding/WinAnsiEncoding>>\nendobj\n'%(3+i_,f_)).encode()
FIRST=11
on('PDF',(None,'PD_h',{fp:0}))
lit('PD_h',head+body,'PD_x')
xw=WPort(1)
seq=sorted(offs.items())
cur_n='PD_x'
for i_,(ob_,of_) in enumerate(seq):
    nx_=f'PD_x{i_}'
    on(cur_n,(None,nx_,{xw:(as_x(XR)+ob_,of_)})); cur_n=nx_
on(cur_n,(None,'PD_0',{qp:0,qpg:0,qtop:0,qobj:FIRST}))
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
    on(n6+'k',(None,nx,{qstart:fp}))
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
    on(cur_n,(None,nx_,{fw2:(as_x(FILE)+qlenat+k_,48+dg)})); cur_n=nx_
e=S('PD_LR'); on('PD_LR',(net.ge(qp,npar,e),'PD_E',None),(None,'PD_O',None))
pg_open('PD_O','PD_L5')
pg_open('PD_0','PD_1')
# walk paragraphs using the saved layout
e=S('PD_1'); on('PD_1',(net.ge(qp,npar,e),'PD_C',None),(None,'PD_2',{r1:as_x(PT)+qp}))
on('PD_2',(None,'PD_3',{qb:R1,rl:R1+SAVE,rc:R1+2062,rp6:R1+PIND,rim:R1+ALIGN}))
e=S('PD_3')
first_p=net.eq(qtop,0,e)
qyy0=rl.out[0]+G_(rp6.out[3],net.gt(rl.out[0],rl.out[1]+96,e))
qlb=net.bits(rim.out[1],4,e); qkind=qlb[0]+qlb[1]*2; qlvl=qlb[2]+qlb[3]*2
qk=R();ql=R();qmk=R();qln=R()
qln_new,qmk_new=list_step(rl.out[4],qkind,qlvl,e)
qex={qk:qkind,ql:qlvl,qmk:qmk_new}
on('PD_3',(first_p,'PD_4',{qyy:qyy0,qtop:rl.out[1],qcols:rc.out[0],qci:rc.out[1],**qex}),
 (net.gt(rl.out[1],qtop,e),'PD_C',{qyy:qyy0,qtop:rl.out[1],qcols:rc.out[0],qci:rc.out[1],**qex}),
 (None,'PD_4',{qyy:qyy0,qcols:rc.out[0],qci:rc.out[1],**qex}))
on('PD_L5',(None,'PD_4',None))
on('PD_4',(None,'PD_5',{r1:qb+NLINES}))
on('PD_5',(None,'PD_6',{qnl:R1,qlj:0}))
e=S('PD_6'); on('PD_6',(net.ge(qlj,qnl,e),'PD_N',None),(None,'PD_7',{rl:qb+LINES+qlj*8,rc:qb+2062,r2:qb+LINES+qlj*8+11}))
e=S('PD_7'); e7=e
Wl=rl.out
tb7=net.step(rc.out[0]); hc7=net.decode(rc.out[0],9,e7); hi7=net.decode(rc.out[1],9,e7); gx7=X()
for cc_ in range(1,9):
    for ii_ in range(cc_): gx7=gx7+net.and_(net.step(hc7[cc_]),net.step(hi7[ii_]))*(ii_*(TW//cc_)+6)
ovf=net.or_(net.and_(net.gt(qyy+Wl[3],qtop+960,e),net.gt(qyy,qtop+96,e)),net.and_(ONE-tb7,keep_lines(e,qyy,qtop,Wl[3],R2,qlj,qnl)))
qind=net.gate(ql*48+48,net.step(qk))
lmv={qs:Wl[0],qe:Wl[1],qx:(Wl[2]+gx7+96+qind)*0.75,qh:Wl[3],qa:Wl[4],qo:Wl[0]}
on('PD_7',(ovf,'PD_C2',{**lmv,qyy:qtop+PST+96,qtop:qtop+PST}),(None,'T2_PM',lmv))
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
    on(cur_n,(None,nx_,{fw2:(as_x(FILE)+qlenat+k_,48+dg)})); cur_n=nx_
pg_open('PD_O2','T2_PM')
# one text line with style runs
lit('PD_8',b'BT 1 0 0 1 ','PD_8x')
number('PD_8x',qx,'PD_8s'); lit('PD_8s',b' ','PD_8y')
number('PD_8y',net.relu(as_x(792)-(qyy-qtop+qa)*0.75),'PD_8t'); lit('PD_8t',b' Tm ','PD_R')
qsty=R()
on('PD_R',(None,'PD_9',{qsty:99999}))
e=S('PD_9'); on('PD_9',(net.ge(qo,qe,e),'PD_Z',None),(None,'PD_A',{r1:qb+qo,r2:qb+1024+qo}))
e=S('PD_A')
on('PD_A',(net.step(net.step(R2-qsty)+net.step(qsty-R2)),'PD_F',{qsty:R2,ins_ch:R1,ins_st:R2}),(None,'PD_T',{ins_ch:R1}))
for st_ in ('PD_F',): sv_en.lin(S(st_)); sv_in.add(S(st_),ins_st)
e=S('PD_F'); zh=net.decode(SV['size'],len(rom.PTS),e); pts=X(); ptv=X()
for i_,h_ in enumerate(zh): pts=pts+h_*rom.PTS[i_]; ptv=ptv+h_*rom.PTS[script_size(i_)]
vf_=net.step(SV['sup']+SV['sub']); qv=R()
on('PD_F',(None,'PD_Fa',{qfn:SV['bold']+SV['ital']*2+SV['font']*4+3,qsz:G_(pts,ONE-vf_)+G_(ptv,vf_),qbase:SV['color'],qv:SV['vert']}))
lit('PD_Fa',b'/F','PD_Fb')
e=S('PD_Fb'); on('PD_Fb',(None,'PD_Fc',None))
em_en.lin(e); em_b.add(e,48+qfn-3)
lit('PD_Fc',b' ','PD_Fd')
number('PD_Fd',qsz,'PD_Fe')
lit('PD_Fe',b' Tf ','PD_Fv')
e=S('PD_Fv'); on('PD_Fv',(net.eq(qv,1,e),'PD_Fv1',None),(net.eq(qv,2,e),'PD_Fv2',None),(None,'PD_Fv0',None))
lit('PD_Fv0',b'0 Ts ','PD_Ff');lit('PD_Fv1',b'4 Ts ','PD_Ff');lit('PD_Fv2',b'-2 Ts ','PD_Ff')
e=S('PD_Ff'); ch8=net.decode(qbase,32,e)
PCS=['%.2f %.2f %.2f'%(c_[0]/255,c_[1]/255,c_[2]/255) for c_ in PAL_F]
on('PD_Ff',*[(ch8[j],f'PD_Co{j}',None) for j in range(32)],(None,'PD_T',None))
for j,pc_ in enumerate(PCS): lit(f'PD_Co{j}',(pc_+' rg ').encode(),'PD_T')
on('PD_T',(None,'PD_Tb',None))
lit('PD_Tb',b'(','PD_Tc')
e=S('PD_Tc'); esc=net.or_(net.eq(ins_ch,40,e),net.eq(ins_ch,41,e),net.eq(ins_ch,92,e))
on('PD_Tc',(esc,'PD_Te',None),(None,'PD_Td',None))
lit('PD_Te',b'\\','PD_Td')
e=S('PD_Td'); em_en.lin(e); em_b.add(e,ins_ch)
on('PD_Td',(None,'PD_Tf',{qo:qo+1}))
lit('PD_Tf',b') Tj ','PD_9')
lit('PD_Z',b'ET\n','PD_Y')
on('PD_Y',(None,'PD_6',{qyy:qyy+qh,qlj:qlj+1}))
e=S('PD_N'); tbl=net.and_(net.step(qcols),net.lt(qci+1,qcols,e))
on('PD_N',(None,'PD_1',{qp:qp+1,qyy:qyy+11}))
# after the last stream: pages tree, xref, trailer
on('PD_E',(None,'PD_E1',{xw:(as_x(XR)+2,fp)}))
res=b''.join(('/F%d %d 0 R'%(i_,3+i_)).encode() for i_ in range(8))
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
