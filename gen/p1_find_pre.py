# ---- p1: Word find codes, read by the shared matcher (exec'd from imp3_find.py) ----
# In the query: ^t tab, ^l manual line break, ^^ a caret, ^s no-break space, ^- optional hyphen, ^? any character,
# ^# any digit, ^$ any letter. In the replacement the five character codes insert their character. ^p stays as it was.
# A code is two cells of the query and one of the document. A query with codes but no ^p tries every start in a paragraph.
_gp1=net.cur[0]; net.group('find codes')
_p1P1L={116:9,108:11,94:94,115:160,45:173}; _p1P1K={63:1,35:2,36:3}
def p1_code(v,en):
    o=X()
    for c_ in list(_p1P1L)+list(_p1P1K): o=o+net.eq(v,c_,en)
    return o
def p1_lit(v,en):
    o=X()
    for c_,t_ in _p1P1L.items(): o=o+net.eq(v,c_,en)*t_
    return o
def p1_kind(v,en):
    o=X()
    for c_,t_ in _p1P1K.items(): o=o+net.eq(v,c_,en)*t_
    return o
# matcher: the cell at xo against the code in xc and p1k
e=S('P1_XC'); on('P1_XC',(net.ge(xo,zxl,e),'IMP3_XR',None),(None,'P1_XD',{r1:zxb+xo}))
e=S('P1_XD')
_p1dg=net.and_(net.ge(R1,48,e),net.lt(R1,58,e))
_p1lt=net.or_(net.and_(net.ge(R1,65,e),net.lt(R1,91,e)),net.and_(net.ge(R1,97,e),net.lt(R1,123,e)),net.and_(net.ge(R1,192,e),net.lt(R1,256,e),ONE-net.eq(R1,215,e),ONE-net.eq(R1,247,e)))
_p1ok=net.or_(net.and_(net.eq(p1k,0,e),net.eq(R1,xc,e)),net.eq(p1k,1,e),net.and_(net.eq(p1k,2,e),_p1dg),net.and_(net.eq(p1k,3,e),_p1lt))
on('P1_XD',(_p1ok,'IMP3_X0',{xq:xq+2,xo:xo+1}),(None,'IMP3_XR',None))
# find walker, codes without marks: every start from fo
e=S('P1_F0'); on('P1_F0',(net.gt(fo,fl-qseg0,e),'F0',{fp:fp+1,fo:0}),(None,'IMP3_X',{xp:fp,zxb:fbs,zxl:fl,xo:fo,xcand:fo,zxret.r:zxret.id('P1_F1')}))
on('P1_F1',(xok,'FJ',{ap:fp,ao:xcand,jp:xp,jo:xo,jret.r:jret.id('FOUND')}),(None,'P1_F0',{fo:fo+1}))
# match counter, codes without marks
e=S('P1_C0'); on('P1_C0',(net.gt(t1_co_,t1_cl-qseg0,e),'T1_C1',{t1_cw:t1_cw+1,t1_co_:0,t1_cb:t1_cb+1}),(net.ge(t1_cb,1500,e),'T1_CS',None),
 (None,'IMP3_X',{xp:t1_cw,zxb:t1_cB,zxl:t1_cl,xo:t1_co_,xcand:t1_co_,t1_cb:t1_cb+qseg0,zxret.r:zxret.id('P1_C1')}))
e=S('P1_C1'); on('P1_C1',(xok,'P1_C0',{t1_cn:t1_cn+1,t1_ci:t1_ci+net.and_(net.ge(Lo,t1_cw*2048+xcand,e),has_sel),t1_co_:xo}),(None,'P1_C0',{t1_co_:t1_co_+1}))
net.group(_gp1)
