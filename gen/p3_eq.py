# ---- p3: matrices with any number of rows and aligned columns ----
# The linear form takes more groups: mat(a&b)(c&d)(e&f). The record keeps the first row as its first text and every later row as its
# second text, the rows apart by ")(" as typed, so the scan, the copy and the 27 character limit stay as they were. Cell 6 holds the row count.
# One walker serves three duties: it measures each column (widest cell), then for each cell measures it and either draws it centred in
# its column or prints it in the PDF. A '&' at depth 0 ends a cell; a ')' at depth 0 in the second text, or the end of the first text, ends a row.
_p3eg=net.cur[0]; net.group('p3 matrix')
P3MC=8; P3G=6; P3P=A9Q+3; P3HP=(P3P+1)//2; P3PP=A9Q+4   # columns, gap between columns, row pitch on screen, half pitch, row pitch in the PDF
p3cw=[R() for _ in range(P3MC)]
p3p=R();p3c=R();p3r=R();p3dp=R();p3w=R();p3s0=R();p3md=R();p3tg=R();p3nc=R();p3rows=R();p3cc=R();p3rb=R();p3ch=R();p3pb=R();p3pl=R();p3sk=R();p3px=R()
# the scan: after the second group, a third and more groups join it for a matrix
on('P3_MR0',(None,'P3_MR1',{r1:cb+a6qj+1}))
e=S('P3_MR1'); on('P3_MR1',(net.and_(net.eq(R1,40,e),net.eq(a6qkd,7,e)),'A6Q_D2',{a6qj:a6qj+2,a6qd:1}),(None,'A6Q_B0',None))
# ---- the walker ----
_N1=a6qnl; _N2=a6qdl; _END=a6qnl+1+a6qdl
def _wstart(tg,rb,more=None):
    d={p3tg:tg,p3rb:rb,p3p:0,p3c:0,p3r:0,p3dp:0,p3w:0,p3s0:0,p3md:0,p3nc:1,p3rows:1,**{q_:0 for q_ in p3cw}}
    return {**d,**(more or {})}
e=S('P3_W0'); _ad=G_(p3rb+8+p3p,net.lt(p3p,_N1,e))+G_(p3rb+36+p3p-_N1-1,net.gt(p3p,_N1,e))
on('P3_W0',(net.ge(p3p,_END,e),'P3_WS',{p3sk:0}),(net.eq(p3p,_N1,e),'P3_WS',{p3sk:1}),(None,'P3_W1',{r1:_ad}))
e=S('P3_W1'); _d0=net.eq(p3dp,0,e); _rowsep=net.and_(net.eq(R1,41,e),_d0,net.gt(p3p,_N1,e))
_dm=net.eq(p3md,2,e)
on('P3_W1',(net.and_(net.eq(R1,38,e),_d0),'P3_WS',{p3sk:3}),(_rowsep,'P3_WS',{p3sk:2}),
 (_dm,'P3_WD',{p3ch:R1,p3dp:p3dp+net.eq(R1,40,e)-net.eq(R1,41,e)}),(None,'P3_WM',{p3ch:R1,p3dp:p3dp+net.eq(R1,40,e)-net.eq(R1,41,e)}))
e=S('P3_WM'); measure(e,p3ch,_qst(p3ch,e,F2SM)); on('P3_WM',(None,'P3_W0',{p3w:p3w+adv,p3p:p3p+1}))
e=S('P3_WD'); _gy=sy+lasc-6-A9Q+p3r*P3P-net.relu(p3rows-2)*P3HP; _g=_qst(p3ch,e,F2SM)
on('P3_WD',(a6qs,'P3_W0',{gly:(p3ch,_g,sx,_gy,0,1),sx:sx+adv,p3p:p3p+1}),(None,'P3_W0',{gly:(p3ch,_g,sx,_gy,0,0),sx:sx+adv,p3p:p3p+1}))
# a separator: p3sk is 0 the end, 1 the end of the first text, 2 a row break in the second text, 3 a column break
e=S('P3_WS'); _sk=net.decode(p3sk,4,e); _cd=net.decode(p3c,P3MC,e); _m=net.decode(p3md,3,e)
_cn=net.min_(p3c+1,P3MC-1); _skip=_sk[1]+_sk[2]*2+_sk[3]
_colx=sum((G_(sum((p3cw[k_] for k_ in range(j_)),X())+P3G*j_,_cd[j_]) for j_ in range(P3MC)),X())
_ccw=sum((G_(p3cw[j_],_cd[j_]) for j_ in range(P3MC)),X())
_next={p3c:G_(_cn,_sk[3]),p3r:p3r+_sk[1]+_sk[2],p3p:p3p+_skip}
on('P3_WS',
 (net.and_(_m[0],_sk[0]),'P3_WE',{q_:net.max_(q_,G_(p3w,_cd[j_])) for j_,q_ in enumerate(p3cw)}),
 (_m[0],'P3_W0',{**{q_:net.max_(q_,G_(p3w,_cd[j_])) for j_,q_ in enumerate(p3cw)},**_next,p3w:0,p3nc:net.max_(p3nc,G_(p3c+2,_sk[3])),p3rows:p3rows+_sk[1]+_sk[2]}),
 (net.and_(_m[1],net.eq(p3tg,1,e)),'P3_WP',{p3cc:p3w,p3md:2,p3pb:G_(p3rb+8+p3s0,net.lt(p3s0,_N1,e))+G_(p3rb+36+p3s0-_N1-1,net.gt(p3s0,_N1,e)),p3pl:p3p-p3s0,
   p3px:qxx+3+_colx+(_ccw-p3w)*0.5,a6qm:0}),
 (_m[1],'P3_W0',{p3cc:p3w,p3md:2,p3p:p3s0,p3dp:0,sx:x+3+_colx+(_ccw-p3w)*0.5}),
 (_sk[0],'P3_WZ',None),
 (None,'P3_W0',{**_next,p3s0:p3p+_skip,p3w:0,p3md:1,p3dp:0}))
# the first pass is done: the column widths are known
_tot=sum(p3cw,X())+(p3nc-1)*P3G
e=S('P3_WE'); on('P3_WE',(net.eq(p3tg,2,e),'P3_WB',{a6qnw:_tot,a6qdw:_tot,w1:(p3rb+6,p3rows)}),(None,'P3_W0',{p3p:0,p3c:0,p3r:0,p3dp:0,p3w:0,p3s0:0,p3md:1}))
on('P3_WB',(None,'A6Q_B8',None))
e=S('P3_WZ'); on('P3_WZ',(net.eq(p3tg,1,e),'A6Q_PE',None),(None,'A6Q_CE',None))
# the record's width at the end of measuring
e=S('P3_SM'); on('P3_SM',(None,'P3_W0',_wstart(2,_qrec(a6qn))))
# paint: the walker draws; the background was set by the dispatch
on('P3_MP0',(None,'P3_W0',_wstart(0,_qrec(a6qk))))
# PDF: each cell is a text object at its column, rows from the baseline up
_pdfy=qyb+7-p3r*P3PP+net.relu(p3rows-2)*P3HP
on('P3_PP0',(None,'P3_W0',_wstart(1,_qrec(a6qk))))
_ptext('P3_WP',p3px,_pdfy,12,p3pb,p3pl,'P3_W0')
# ---- OMML: m:m with one m:mr per row and one m:e per cell ----
_MT=b'<m:r><m:t xml:space="preserve">'; _ME=b'</m:t></m:r>'; _MC=_ME+b'</m:e><m:e>'+_MT; _MRW=_ME+b'</m:e></m:mr><m:mr><m:e>'+_MT
lit('P3_X7',b'<m:m><m:mr><m:e>'+_MT,'P3_X7a'); _qtext('P3_X7a',_qrec(a6qk)+8,a6qnl,'P3_X7b',amp=_MC); lit('P3_X7b',_MRW,'P3_X7c')
on('P3_X7c',(None,'P3_X8',{a6qm:0,p3dp:0}))
e=S('P3_X8'); on('P3_X8',(net.ge(a6qm,a6qdl,e),'P3_X8z',None),(None,'P3_X8r',{r1:_qrec(a6qk)+36+a6qm,a6qm:a6qm+1}))
e=S('P3_X8r'); _d0=net.eq(p3dp,0,e); _a=net.eq(R1,38,e); _l=net.eq(R1,60,e); _g2=net.eq(R1,62,e)
_rs=net.and_(net.eq(R1,41,e),_d0); _cs=net.and_(_a,_d0); _o=e-_a-_l-_g2-_rs; em_en.lin(_o); em_b.add(_o,R1)
on('P3_X8r',(_rs,'P3_X8w',{a6qm:a6qm+1}),(_cs,'P3_X8c',None),(_a,'P3_X8a',None),(_l,'P3_X8l',None),(_g2,'P3_X8k',None),(None,'P3_X8',{p3dp:p3dp+net.eq(R1,40,e)-net.eq(R1,41,e)}))
lit('P3_X8w',_MRW,'P3_X8'); lit('P3_X8c',_MC,'P3_X8'); lit('P3_X8a',b'&amp;','P3_X8'); lit('P3_X8l',b'&lt;','P3_X8'); lit('P3_X8k',b'&gt;','P3_X8')
lit('P3_X8z',_ME+b'</m:e></m:mr></m:m>','A6E_ER')
net.group(_p3eg)
