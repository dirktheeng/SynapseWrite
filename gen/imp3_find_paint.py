# Paint highlight for a query with marks. First, once per paragraph, the earlier paragraphs a match could have started in; then each cell is compared with this paragraph's one candidate start.
_g0=net.cur[0]
net.group('find across paragraphs')
e=S('IMP3_H0'); on('IMP3_H0',(ONE-xbd,'IMP3_HB',{xbd:1,xj:1}),(net.and_(net.eq(qnm,0,e),net.ge(plen_-off,qseg0,e)),'IMP3_X',{xp:pi,zxb:pbs,zxl:plen_,xo:off,zxret.r:zxret.id('P1_H1')}),(net.eq(qnm,0,e),'RVA3_HG',None),(net.and_(net.ge(plen_,qseg0,e),net.eq(off,plen_-qseg0,e)),'IMP3_X',{xp:pi,zxb:pbs,zxl:plen_,xo:off,zxret.r:zxret.id('IMP3_H1')}),(None,'RVA3_HG',None))
on('P1_H1',(xok,'RVA3_HG',{rv_mhe:xo}),(None,'RVA3_HG',None))
on('IMP3_H1',(xok,'RVA3_HG',{rv_mhe:plen_}),(None,'RVA3_HG',None))
e=S('IMP3_HB'); on('IMP3_HB',(net.or_(net.gt(xj,qnm,e),net.gt(xj,pi,e)),'IMP3_H0',None),(None,'IMP3_HC',{r1:as_x(PT)+pi-xj}))
on('IMP3_HC',(None,'IMP3_HD',{zxb:R1,r2:R1+LEN}))
e=S('IMP3_HD'); on('IMP3_HD',(net.gt(qseg0,R2,e),'IMP3_HB',{xj:xj+1}),(None,'IMP3_X',{xp:pi-xj,zxl:R2,xo:R2-qseg0,zxret.r:zxret.id('IMP3_HE')}))
e=S('IMP3_HE'); _last=net.eq(xj,qnm,e)
on('IMP3_HE',(net.and_(xok,_last),'IMP3_H0',{rv_mhe:qsegL}),(xok,'IMP3_H0',{rv_mhe:plen_}),(None,'IMP3_HB',{xj:xj+1}))
net.group(_g0)
