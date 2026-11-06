# ---- feat2: run effects in PDF from the feat1 fields of a style entry: character spacing as Tc, run shading, double strike, external links as link annotations ----
# Small capitals are in the page walk itself (pdf_write.py): a small capital run is its own chunk at the script size.
_f2pg=net.cur[0]; net.group('feat2 pdf run effects')
F2LKB=1376000; F2LKN=200; region('feat2 PDF link boxes',F2LKB,F2LKB+5*F2LKN)   # per page: left, right, bottom, height, link id
f2ti=R();f2tf=R();f2tn=R();f2li=R();f2up=R();f2a=[R() for _ in range(5)];f2c=[R() for _ in range(3)]
def _f2num(st,val,digits,pad,nx): on(st,(None,'A10_N',{**_start(val,digits,pad),nrr.r:nrr.id(nx)}))
# Tc: f2tw is the chunk's spacing in twips plus 512, f2tc the spacing in force plus 100 (registers hold no negatives). Written as pixels to two places.
e=S('F2P_T0'); _tw=f2tw-512; _neg=net.lt(_tw,0,e); _abs=net.relu(_tw)+net.relu(0-_tw)
_H=floorv(_abs*(20/3)+0.5,e,12); _I=floorv(_H*0.01+0.001,e,6)
on('F2P_T0',(None,'F2P_T1',{f2tn:_neg,f2ti:_I,f2tf:_H-_I*100,f2tc:_tw*(1/15)+100}))
on('F2P_T1',(f2tn,'F2P_Tm',None),(None,'F2P_T2',None)); lit('F2P_Tm',b'-','F2P_T2')
vnum('F2P_T2',f2ti,'F2P_T3'); lit('F2P_T3',b'.','F2P_T4'); _f2num('F2P_T4',f2tf,2,True,'F2P_T5'); lit('F2P_T5',b' Tc\n','T4P_Oa')
# after a chunk: its shade under it with a Multiply blend (as highlight), double strike, and a link box for the page's annotations
e=S('F2P_C0'); on('F2P_C0',(net.step(f2cz),'F2P_S0',None),(None,'F2P_C1',None))
e=S('F2P_S0'); _zb=net.bits(f2cz-1,24,e)
on('F2P_S0',(None,'F2P_S1',{f2c[j_]:sum((_zb[16-8*j_+k_]*(1<<k_) for k_ in range(8)),X()) for j_ in range(3)}))
lit('F2P_S1',b'q /M gs ','F2P_Sc0')
for j_ in range(3):
    st=f'F2P_Sc{j_}'; nx=f'F2P_Sc{j_+1}' if j_<2 else 'F2P_Sr'; e=S(st)
    on(st,(net.ge(f2c[j_],255,e),st+'o',None),(None,st+'d',None))
    lit(st+'o',b'1 ',nx); lit(st+'d',b'.',st+'e'); _f2num(st+'e',f2c[j_]*(1000/255),3,True,st+'f'); lit(st+'f',b' ',nx)
lit('F2P_Sr',b'rg ','F2P_Sx')
number('F2P_Sx',qcx0,'F2P_Sx1'); lit('F2P_Sx1',b' ','F2P_Sx2'); number('F2P_Sx2',qph-(qyy-qtop)-qh,'F2P_Sx3'); lit('F2P_Sx3',b' ','F2P_Sx4'); number('F2P_Sx4',qxx-qcx0,'F2P_Sx5'); lit('F2P_Sx5',b' ','F2P_Sx6'); number('F2P_Sx6',qh,'F2P_Sx7'); lit('F2P_Sx7',b' re f Q\n','F2P_C1')
e=S('F2P_C1'); on('F2P_C1',(net.bits(f2cx,14,e)[2],'F2P_D0',None),(None,'F2P_C2',None))
for i_,dy_ in enumerate((3,7)):
    st=f'F2P_D{i_}'; nx='F2P_D1' if i_==0 else 'F2P_C2'
    number(st,qcx0,st+'a'); lit(st+'a',b' ',st+'b'); number(st+'b',qyb+dy_,st+'c'); lit(st+'c',b' ',st+'d'); number(st+'d',qxx-qcx0,st+'e'); lit(st+'e',b' 1 re f\n',nx)
e=S('F2P_C2'); _hb=net.bits(f2ch,20,e); _lk=sum((_hb[k_]*(1<<k_) for k_ in range(12)),X())
on('F2P_C2',(net.and_(net.step(_lk),net.lt(f2ln,F2LKN,e)),'F2P_L0',{r1:as_x(F1LT)+_lk*F1LS,f2a[4]:_lk}),(None,'F2P_C3',None))
e=S('F2P_L0'); _lb=as_x(F2LKB)+f2ln*5
on('F2P_L0',(net.eq(R1,1,e),'F2P_C3',{w1:(_lb,qcx0),w2:(_lb+1,qxx),w3:(_lb+2,qph-(qyy-qtop)-qh),w4:(_lb+3,qh),xw:(_lb+4,f2a[4]),f2ln:f2ln+1}),(None,'F2P_C3',None))
# the page's annotations object, after its content stream: external links only, as URI actions; rects in points
on('F2P_A0',(None,'F2P_A1',{xw:(as_x(XR)+qobj-1,fp),f2li:0}))
number('F2P_A1',qobj-1,'F2P_A2'); lit('F2P_A2',b' 0 obj\n[','F2P_A3')
e=S('F2P_A3'); on('F2P_A3',(net.ge(f2li,f2ln,e),'F2P_AZ',None),(None,'F2P_A4',{rl:as_x(F2LKB)+f2li*5}))
on('F2P_A4',(None,'F2P_A5',{**{f2a[i_]:rl.out[i_] for i_ in range(5)}}))
lit('F2P_A5',b'<</Type/Annot/Subtype/Link/Border[0 0 0]/Rect[','F2P_R0')
for i_,(v_,nx_) in enumerate(((f2a[0]*0.75,b' '),(f2a[2]*0.75,b' '),(f2a[1]*0.75,b' '),((f2a[2]+f2a[3])*0.75,b']/A<</S/URI/URI('))):
    numz(f'F2P_R{i_}',v_,f'F2P_R{i_}x'); lit(f'F2P_R{i_}x',nx_,f'F2P_R{i_+1}' if i_<3 else 'F2P_U')
on('F2P_U',(None,'F2P_U0',{f2up:as_x(F1LT)+f2a[4]*F1LS+1}))
on('F2P_U0',(None,'F2P_U1',{rl:f2up}))
e=S('F2P_U1'); _W=rl.out; _amp=net.and_(net.eq(_W[0],38,e),net.eq(_W[1],97,e),net.eq(_W[2],109,e),net.eq(_W[3],112,e),net.eq(_W[4],59,e)); _esc=net.or_(net.eq(_W[0],40,e),net.eq(_W[0],41,e),net.eq(_W[0],92,e))
on('F2P_U1',(net.or_(net.eq(_W[0],0,e),net.ge(f2up,as_x(F1LT)+f2a[4]*F1LS+F1LS,e)),'F2P_U9',None),(_amp,'F2P_U2',{f2up:f2up+5}),(_esc,'F2P_U3',{qcur:_W[0],f2up:f2up+1}),(None,'F2P_U4',{qcur:_W[0],f2up:f2up+1}))
lit('F2P_U2',b'&','F2P_U0'); lit('F2P_U3',b'\\','F2P_U4'); e=S('F2P_U4'); em_en.lin(e); em_b.add(e,qcur); on('F2P_U4',(None,'F2P_U0',None))
lit('F2P_U9',b')>>>>\n','F2P_U8'); on('F2P_U8',(None,'F2P_A3',{f2li:f2li+1}))
lit('F2P_AZ',b']\nendobj\n','F2P_AR')
net.group(_f2pg)
