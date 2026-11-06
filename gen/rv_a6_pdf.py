# ---- rv_a6: PDF highlight and bookmarks from headings ----
# Highlight: a Multiply blend rectangle painted after the chunk, so the text stays dark without measuring the chunk first.
# Bookmarks: one record per heading is taken during the page walk; a forward pass links parents and siblings, then one outline object per record.
PDBM=1200000; PDST=16
a6pn=R();a6pi=R();a6pp=R();a6pv=R();a6l1=R();a6l2=R();a6pb=R();a6pt=R();a6pk=R();a6pl=R()
a6r=[R() for _ in range(9)]; p3bk=R()   # p3: the record is a bookmark, its title the bookmark name
fsm.set(a6pn,S('PDF'),0)
e=S('A6P_FH'); hl7=net.decode(qhl,8,e)
on('A6P_FH',*[(hl7[j],f'A6P_H{j}',None) for j in range(1,8)],(None,'A6P_U',None))
for j in range(1,8):
    c_=PAL_B[5+j]; lit(f'A6P_H{j}',(b'q /M gs %.2f %.2f %.2f rg '%(c_[0]/255,c_[1]/255,c_[2]/255)),'A6P_Ha')
number('A6P_Ha',qcx0,'A6P_Hb'); lit('A6P_Hb',b' ','A6P_Hc'); number('A6P_Hc',qph-(qyy-qtop)-qh,'A6P_Hd'); lit('A6P_Hd',b' ','A6P_He'); number('A6P_He',qxx-qcx0,'A6P_Hf'); lit('A6P_Hf',b' ','A6P_Hg'); number('A6P_Hg',qh,'A6P_Hh'); lit('A6P_Hh',b' re f Q\n','A6P_U')
on('A6P_U',(qdel,'T4P_Ra',{qry:qyb+5}),(qund,'T4P_Ra',{qry:qyb-2}),(None,'T4_PFC',None))
# heading record, on the first line of a paragraph once the page is settled
on('A6P_B0',(None,'A6P_B1',{r1:qb+PSTY}))
e=S('A6P_B1'); _ish=net.and_(net.eq(qlj,0,e),net.ge(R1,2,e),net.lt(R1,5,e),net.lt(a6pn,4000,e))
_rec=as_x(PDBM)+(a6pn+1)*PDST
on('A6P_B1',(_ish,'A6P_B2',{a6pv:R1-1,wln:(_rec,qb,R1-1,qobj,qph-(qyy-qtop),0,0)}),(None,'A4_QL',None))
on('A6P_B2',(None,'A4_QL',{wln:(_rec+6,0,0,0,0,0,0),a6pn:a6pn+1}))
# forward pass: each record finds its parent, which keeps first, last and count of its children
_recq=lambda i_:as_x(PDBM)+i_*PDST
on('A6P_F0',(None,'A6P_F1',{w1:(_recq(0)+7,0),w2:(_recq(0)+8,0),w3:(_recq(0)+9,0),a6pi:1,a6l1:0,a6l2:0}))
e=S('A6P_F1'); on('A6P_F1',(net.gt(a6pi,a6pn,e),'A6P_E0',{a6pb:qobj,a6pk:0}),(None,'A6P_F2',{r1:_recq(a6pi)+1}))
e=S('A6P_F2'); _l1=net.eq(R1,1,e);_l2=net.eq(R1,2,e);_l3=net.eq(R1,3,e)
_par=G_(a6l1,_l2)+G_(a6l2,net.and_(_l3,net.step(a6l2)))+G_(a6l1,net.and_(_l3,ONE-net.step(a6l2)))
on('A6P_F2',(_l1,'A6P_F3',{a6pp:_par,a6l1:a6pi,a6l2:0,rc:_recq(_par)+8}),(_l2,'A6P_F3',{a6pp:_par,a6l2:a6pi,rc:_recq(_par)+8}),(None,'A6P_F3',{a6pp:_par,rc:_recq(_par)+8}))
on('A6P_F3',(None,'A6P_F4',{a6pv:rc.out[0],w1:(_recq(a6pp)+8,a6pi),w2:(_recq(a6pp)+9,rc.out[1]+1),w3:(_recq(a6pi)+4,a6pp),w4:(_recq(a6pi)+5,rc.out[0]),r1:_recq(a6pp)+7}))
e=S('A6P_F4'); _nf=net.step(R1)
on('A6P_F4',(None,'A6P_F1',{w1:(_recq(a6pp)+7,G_(R1,_nf)+G_(a6pi,e-net.and_(e,_nf))),w2:(_recq(a6pv)+6,a6pi),a6pi:a6pi+1}))
# outline objects: record i becomes object a6pb+i-1; the root keeps its reserved number
def _oref(st,key,reg,nx):
    n1=st+'a';n2=st+'b';n3=st+'c'
    on(st,(net.step(reg),n1,None),(None,nx,None))
    lit(n1,key,n2); number(n2,a6pb+reg-1,n3); lit(n3,b' 0 R',nx)
e=S('A6P_E0'); on('A6P_E0',(net.ge(a6pk,a6pn,e),'A6P_Z0',{qobj:a6pb+a6pn}),(None,'A6P_E1',{a6pi:a6pk+1,rl:_recq(a6pk+1),rp6:_recq(a6pk+1)+4,xw:(as_x(XR)+a6pb+a6pk,fp)}))
on('A6P_E1',(None,'A6P_E2',{a6pt:rl.out[0],a6r[0]:rl.out[2],a6r[1]:rl.out[3],a6r[2]:rp6.out[0],a6r[3]:rp6.out[1],a6r[4]:rp6.out[2],a6r[5]:rp6.out[3],a6r[6]:rp6.out[4],a6r[7]:rp6.out[5],r1:rl.out[0]+LEN,a6pl:0,p3bk:net.lt(rl.out[0],SLOT0,S('A6P_E1'))}))
on('A6P_E2',(None,'A6P_E3',{a6r[8]:G_(net.min_(G_(R1,S('A6P_E2')),120),net.and_(S('A6P_E2'),ONE-p3bk))+p3bk*(F1BS-1)}))
number('A6P_E3',a6pb+a6pk,'A6P_E4'); lit('A6P_E4',b' 0 obj\n<</Title(','A6P_T0')
e=S('A6P_T0'); on('A6P_T0',(net.ge(a6pl,a6r[8],e),'A6P_Pa',None),(None,'A6P_T1',{r1:a6pt+a6pl,a6pl:a6pl+1}))
e=S('A6P_T1'); _esc=net.or_(net.eq(R1,40,e),net.eq(R1,41,e),net.eq(R1,92,e)); _ok=net.and_(net.ge(R1,32,e),net.lt(R1,256,e))
on('A6P_T1',(net.and_(p3bk,net.eq(R1,0,e)),'A6P_Pa',None),(_esc,'A6P_T2',{qcur:R1}),(_ok,'A6P_T3',{qcur:R1}),(None,'A6P_T0',None))
lit('A6P_T2',b'\\','A6P_T3')
e=S('A6P_T3'); em_en.lin(e); em_b.add(e,qcur); on('A6P_T3',(None,'A6P_T0',None))
lit('A6P_Pa',b')/Parent ','A6P_Pb')
on('A6P_Pb',(net.step(a6r[2]),'A6P_Pc',None),(None,'A6P_Pd',None))
number('A6P_Pc',a6pb+a6r[2]-1,'A6P_Pe'); number('A6P_Pd',OROOT,'A6P_Pe'); lit('A6P_Pe',b' 0 R','A6P_R1')
_oref('A6P_R1',b'/Prev ',a6r[3],'A6P_R2'); _oref('A6P_R2',b'/Next ',a6r[4],'A6P_R3'); _oref('A6P_R3',b'/First ',a6r[5],'A6P_R4'); _oref('A6P_R4',b'/Last ',a6r[6],'A6P_C0')
on('A6P_C0',(net.step(a6r[7]),'A6P_C1',None),(None,'A6P_D0',None))
lit('A6P_C1',b'/Count -','A6P_C2'); number('A6P_C2',a6r[7],'A6P_D0')
lit('A6P_D0',b'/Dest[','A6P_D1'); number('A6P_D1',a6r[0],'A6P_D2'); lit('A6P_D2',b' 0 R/XYZ 0 ','A6P_D3'); numz('A6P_D3',a6r[1]*0.75,'A6P_D4'); lit('A6P_D4',b' 0]>>\nendobj\n','A6P_D5')
on('A6P_D5',(None,'A6P_E0',{a6pk:a6pk+1}))
# the root
on('A6P_Z0',(None,'A6P_Z1',{xw:(as_x(XR)+OROOT,fp),rc:_recq(0)+7,r1:_recq(0)+9}))
on('A6P_Z1',(None,'A6P_Z2',{a6r[5]:rc.out[0],a6r[6]:rc.out[1],a6r[7]:R1}))
lit('A6P_Z2',b'%d 0 obj\n<</Type/Outlines'%OROOT,'A6P_Z3')
_oref('A6P_Z3',b'/First ',a6r[5],'A6P_Z4'); _oref('A6P_Z4',b'/Last ',a6r[6],'A6P_Z5')
lit('A6P_Z5',b'/Count ','A6P_Z6'); number('A6P_Z6',a6r[7],'A6P_Z7'); lit('A6P_Z7',b'>>\nendobj\n','P3_DS0')
