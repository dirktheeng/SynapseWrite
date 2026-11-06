# ---- p3: bookmarks as PDF named destinations and outline items, internal links as GoTo link annotations ----
# Destination table: entry b (1..255) at P3DT+b*4 holds the export serial, the page object and the line top in pixels.
# An entry counts only when its serial is this export's, so the table needs no clearing pass.
_p3pg=net.cur[0]; net.group('p3 pdf destinations')
P3DT=1196000; region('p3 PDF destinations',P3DT,P3DT+4*(F1N+1))
p3ser=R();p3b=R();p3i=R();p3np=R();p3ne=R();p3hx=R()
fsm.set(p3ser,S('PDF'),p3ser+1)
p3nr=t3ret('P3_NR')
# a printed chunk that carries a bookmark: the first one of each bookmark gives its destination and, unless the name is hidden (starts with _), an outline item
e=S('P3_B0'); _hb=net.bits(f2ch,24,e); _bk=sum((_hb[k_]*(1<<(k_-12)) for k_ in range(12,20)),X())
on('P3_B0',(net.step(_bk),'P3_B1',{p3b:_bk,r1:as_x(P3DT)+_bk*4}),(None,'F2P_C3',None))
e=S('P3_B1'); _y=qph-(qyy-qtop)
on('P3_B1',(net.eq(R1,p3ser,e),'F2P_C3',None),(None,'P3_B2',{w1:(as_x(P3DT)+p3b*4,p3ser),w2:(as_x(P3DT)+p3b*4+1,qobj),w3:(as_x(P3DT)+p3b*4+2,_y),r1:as_x(F1BT)+p3b*F1BS}))
e=S('P3_B2'); _rec=as_x(PDBM)+(a6pn+1)*PDST
on('P3_B2',(net.or_(net.eq(R1,95,e),net.eq(R1,0,e),net.ge(a6pn,4000,e)),'F2P_C3',None),(None,'P3_B3',{wln:(_rec,as_x(F1BT)+p3b*F1BS,1,qobj,_y,0,0)}))
on('P3_B3',(None,'F2P_C3',{wln:(_rec+6,0,0,0,0,0,0),a6pn:a6pn+1}))
# a name as a PDF name object: letters, digits, _ - . as they are, every other byte as #hh; stops at a zero or the limit
on('P3_NM',(None,'P3_NM1',{r1:p3np}))
e=S('P3_NM1'); _c=R1
_reg=net.or_(net.and_(net.ge(_c,48,e),net.lt(_c,58,e)),net.and_(net.ge(_c,65,e),net.lt(_c,91,e)),net.and_(net.ge(_c,97,e),net.lt(_c,123,e)),net.eq(_c,95,e),net.eq(_c,45,e),net.eq(_c,46,e))
on('P3_NM1',(net.or_(net.eq(_c,0,e),net.ge(p3np,p3ne,e)),'P3_NR',None),(_reg,'P3_NM2',{qcur:_c,p3np:p3np+1}),(None,'P3_NH0',{qcur:_c,p3np:p3np+1}))
e=S('P3_NM2'); em_en.lin(e); em_b.add(e,qcur); on('P3_NM2',(None,'P3_NM',None))
e=S('P3_NH0'); _hb2=net.bits(qcur,8,e); _hi=sum((_hb2[k_]*(1<<(k_-4)) for k_ in range(4,8)),X()); _lo=sum((_hb2[k_]*(1<<k_) for k_ in range(4)),X())
em_en.lin(e); em_b.add(e,35); on('P3_NH0',(None,'P3_NH1',{p3hx:_lo,qcur:_hi}))
e=S('P3_NH1'); em_en.lin(e); em_b.add(e,48+qcur+net.ge(qcur,10,e)*7); on('P3_NH1',(None,'P3_NH2',None))
e=S('P3_NH2'); em_en.lin(e); em_b.add(e,48+p3hx+net.ge(p3hx,10,e)*7); on('P3_NH2',(None,'P3_NM',None))
# a link annotation: an external target is a URI action, a target in the document a named destination
on('P3_K0',(None,'P3_K1',{r1:as_x(F1LT)+f2a[4]*F1LS}))
e=S('P3_K1'); on('P3_K1',(net.eq(R1,2,e),'P3_K2',None),(None,'P3_K5',None))
lit('P3_K2',b'/Dest/','P3_K3'); on('P3_K3',(None,'P3_NM',{p3np:as_x(F1LT)+f2a[4]*F1LS+1,p3ne:as_x(F1LT)+f2a[4]*F1LS+F1LS-1,p3nr.r:p3nr.id('P3_K4')}))
lit('P3_K4',b'>>\n','F2P_U8')
lit('P3_K5',b'/A<</S/URI/URI(','F2P_U')
# the destinations dictionary, after the outline: one entry per bookmark that was printed
on('P3_DS0',(None,'P3_DS1',{xw:(as_x(XR)+DROOT,fp),p3i:1}))
lit('P3_DS1',b'%d 0 obj\n<<'%DROOT,'P3_DS2')
e=S('P3_DS2'); on('P3_DS2',(net.gt(p3i,F1N,e),'P3_DSZ',None),(None,'P3_DS3',{rl:as_x(P3DT)+p3i*4}))
e=S('P3_DS3'); on('P3_DS3',(net.eq(rl.out[0],p3ser,e),'P3_DS4',{a6r[0]:rl.out[1],a6r[1]:rl.out[2]}),(None,'P3_DS2',{p3i:p3i+1}))
lit('P3_DS4',b'\n/','P3_DS5'); on('P3_DS5',(None,'P3_NM',{p3np:as_x(F1BT)+p3i*F1BS,p3ne:as_x(F1BT)+p3i*F1BS+F1BS-1,p3nr.r:p3nr.id('P3_DS6')}))
lit('P3_DS6',b'[','P3_DS7'); number('P3_DS7',a6r[0],'P3_DS8'); lit('P3_DS8',b' 0 R/XYZ 0 ','P3_DS9'); numz('P3_DS9',a6r[1]*0.75,'P3_DSa'); lit('P3_DSa',b' 0]','P3_DSb')
on('P3_DSb',(None,'P3_DS2',{p3i:p3i+1}))
lit('P3_DSZ',b'>>\nendobj\n','PD_X0')
net.group(_p3pg)
