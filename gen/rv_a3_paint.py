# find match highlight: at each cell while the find bar is open, compare the query against the paragraph ahead
on('RVA3_H0',(qmrk,'IMP3_H0',None),(net.ge(rv_hk,qlen,S('RVA3_H0')),'RVA3_HM',None),(net.gt(off+rv_hk,plen_-1,S('RVA3_H0')),'RVA3_HG',None),(None,'RVA3_H1',{r1:pbs+off+rv_hk,r2:as_x(Q)+rv_hk}))
_rv_e=S('RVA3_H1'); on('RVA3_H1',(net.eq(low(R1,_rv_e),low(R2,_rv_e),_rv_e),'RVA3_H0',{rv_hk:rv_hk+1}),(None,'RVA3_HG',None))
on('RVA3_HM',(t1_fw,'RVA3_H2',{r1:pbs+net.relu(off-1),r2:pbs+off+qlen}),(None,'RVA3_HG',{rv_mhe:off+qlen}))
_rv_e=S('RVA3_H2'); ok_=net.and_(net.or_(net.eq(off,0,_rv_e),ONE-t1_isw(R1,_rv_e)),net.or_(net.ge(off+qlen,plen_,_rv_e),ONE-t1_isw(R2,_rv_e)))
on('RVA3_H2',(ok_,'RVA3_HG',{rv_mhe:off+qlen}),(None,'RVA3_HG',None))
on('RVA3_HG',(None,'C1',{r1:pbs+off,rs:pbs+1024+off}))
