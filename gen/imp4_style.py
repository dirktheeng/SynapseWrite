# ---- imp4: creating and renaming styles, character styles ----
# A new style is a table entry written from the caret's own format, like the update path reads it. A character style is an entry with cell 47 set and a mask of the fields it sets.
net.group('style create and rename')
on('V5_NS0',(net.or_(net.ge(nsty,STYMAX,S('V5_NS0')),net.lt(prl,1,S('V5_NS0'))),'RD0',None),(None,'V5_DS',{v5i:0,v5j:0,v5k:0}))
# the id is the name without spaces; an id already in the table is refused and the bar stays open
e=S('V5_DS'); on('V5_DS',(net.ge(v5i,nsty,e),'V5_N0',None),(None,'V5_D0',{v5j:0,v5k:0}))
on('V5_D0',(None,'V5_D1',{r1:as_x(PRB)+v5j,r2:as_x(STY)+v5i*STYN+8+v5k}))
e=S('V5_D1'); _end=net.ge(v5j,prl,e); _sp=net.and_(ONE-_end,net.eq(R1,32,e))
on('V5_D1',(net.and_(_end,net.eq(R2,0,e)),'RD0',{mode:8}),(_end,'V5_DS',{v5i:v5i+1}),(_sp,'V5_D0',{v5j:v5j+1}),(net.eq(R1,R2,e),'V5_D0',{v5j:v5j+1,v5k:v5k+1}),(None,'V5_DS',{v5i:v5i+1}))
on('V5_N0',(None,'V5_N1',{r1:cb+PSTY,rs:cb+1024+net.relu(co-1),rl:cb+LEN,rp6:cb+PIND,v5n:nsty}))
e=S('V5_N1'); _h=net.step(clen); _nh=e-net.and_(e,_h)
on('V5_N1',(None,'V5_N2',{t2nr_:G_(RSR,_h)+G_(ty,_nh),v4uk:G_(RSK,_h)+G_(ity.k,_nh),v4un:G_(RSN,_h)+G_(ity.n,_nh),t2f[1]:rl.out[2],t2f[2]:rp6.out[0],t2f[3]:rp6.out[1],t2f[4]:rp6.out[2],t2f[5]:rp6.out[3],t2f[6]:rp6.out[4],nsty:nsty+1,grp:grp+1}))
e=S('V5_N2'); _YD=style_decode(t2nr_,e)
# undo record 13 restores the style count, in the same group as the style's first use, so one undo takes back both
log(e,13,cp,0,v5n,v5n+1)
_mk=_YD['bold']+_YD['ital']*2+_YD['und']*4+net.step(_YD['font'])*8+net.or_(net.step(_YD['color']),net.step(v4uk))*16+_YD['strike']*32+net.step(_YD['vert'])*64+net.step(_YD['hl'])*128+net.step(_YD['size'])*256
on('V5_N2',(None,'V5_N3',{wln:(as_x(STY)+v5n*STYN,t2nr_,G_(t2f[1],ONE-v4c),G_(t2f[2],ONE-v4c),G_(t2f[3],ONE-v4c),G_(t2f[4],ONE-v4c),G_(t2f[5],ONE-v4c)),w1:(as_x(STY)+v5n*STYN+6,G_(t2f[6],ONE-v4c)),w2:(as_x(STY)+v5n*STYN+7,0),w3:(as_x(STY)+v5n*STYN+46,0),w4:(as_x(STY)+v5n*STYN+47,v4c),ymsk:_mk}))
on('V5_N3',(None,'V5_N4',{w1:(as_x(STYX)+v5n*4,v4uk),w2:(as_x(STYX)+v5n*4+1,v4un),w3:(as_x(STYX)+v5n*4+2,ymsk),v5j:0,v5k:0}))
on('V5_N4',(None,'V5_N5',{r1:as_x(PRB)+v5j}))
e=S('V5_N5'); _end=net.ge(v5j,prl,e); _sp=net.and_(ONE-_end,net.eq(R1,32,e)); _nm=net.lt(v5j,17,e); _idok=net.lt(v5k,19,e)
on('V5_N5',(_end,'V5_N6',{w1:(as_x(STY)+v5n*STYN+8+v5k,0),w2:(as_x(STY)+v5n*STYN+28+net.min_(v5j,17),0)}),
 (_sp,'V5_N4',{v5j:v5j+1,w2:(as_x(STY)+v5n*STYN+28+net.min_(v5j,17),G_(R1,_nm))}),
 (None,'V5_N4',{v5j:v5j+1,v5k:v5k+net.and_(e,_idok),w1:(as_x(STY)+v5n*STYN+8+net.min_(v5k,18),G_(R1,_idok)),w2:(as_x(STY)+v5n*STYN+28+net.min_(v5j,17),G_(R1,_nm))}))
# both apply paths open a new undo group (the paragraph path through FMTS over the paragraph's text); stepping back one, and holding T2_SA1's own step with a4cfq, puts the use in the creation's group
on('V5_N6',(v4c,'V5_CA',{t2si:v5n,grp:grp-1}),(None,'T2_SA0',{t2si:v5n,a4cfq:1,grp:grp-net.step(clen)}))
# applying a character style: its fields go over each run's own, and the run remembers the style
on('V5_CA',(None,'V5_CB',{rl:as_x(STY)+t2si*STYN,r1:as_x(STYX)+t2si*4,r2:as_x(STYX)+t2si*4+1,rU:as_x(STYX)+t2si*4+2}))
on('V5_CB',(None,'FMTS',{ysr:rl.out[0],fpk:R1,fpn:R2,ymsk:rU.out[0],fpy:t2si+1,fm:16,fcol:0}))
# a menu pick: paragraph styles apply as before, character styles take the path above
on('V5_MP',(None,'V5_MQ',{r1:as_x(STY)+t2si*STYN+47}))
e=S('V5_MQ'); on('V5_MQ',(net.eq(R1,1,e),'V5_CA',None),(None,'IMP3_SA',None))
# rename: every name cell is rewritten with an undo record, so undo brings the old name back
on('V5_RN0',(net.lt(prl,1,S('V5_RN0')),'RD0',None),(None,'V5_RN1',{r1:cb+PSTY,rs:cb+1024+net.relu(co-1)}))
e=S('V5_RN1'); _yy=net.and_(e,net.step(clen),net.step(RSY)); on('V5_RN1',(None,'V5_RN2',{v5n:G_(RSY-1,_yy)+G_(R1,e-_yy),v5j:0,grp:grp+1}))
on('V5_RN2',(None,'V5_RN3',{r1:as_x(STY)+v5n*STYN+28+v5j,r2:as_x(PRB)+v5j}))
e=S('V5_RN3'); _nv=G_(R2,net.and_(e,net.lt(v5j,prl,e))); log(e,7,as_x(STY)+v5n*STYN+28+v5j,0,R1,_nv)
on('V5_RN3',(net.ge(v5j,17,e),'UI',{w1:(as_x(STY)+v5n*STYN+28+v5j,0),clip0:0,clip1:0}),(None,'V5_RN2',{w1:(as_x(STY)+v5n*STYN+28+v5j,_nv),v5j:v5j+1}))
