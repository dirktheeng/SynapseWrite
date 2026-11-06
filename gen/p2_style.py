# ---- p2: Update Style on a character style ----
# With the caret in a run of a character style, Update takes the caret's format as the style's new definition (its fields that differ from the default),
# then walks the whole document with the format walk, laying the new fields over every run of that style, as Word's Update to Match Selection does.
# One undo group holds the definition and every run it changed.
_p2g=net.cur[0]; net.group('p2 character style update')
on('P2_UA',(None,'P2_UB',{rs:cb+1024+net.relu(co-1)}))
e=S('P2_UB'); _ch=net.and_(e,net.step(clen),net.step(RSY))
on('P2_UB',(_ch,'P2_U0',{t2si:RSY-1,t2nr_:RSR,v4uk:RSK,v4un:RSN,grp:grp+1,p2sc:cp,p2so:co,p2sa:ap,p2sb:ao}),(None,'T2_UM1',{r1:cb+PSTY,rs:cb+1024,rl:cb+LEN,rp6:cb+PIND}))
e=S('P2_U0'); _YD=style_decode(t2nr_,e)
_mk=_YD['bold']+_YD['ital']*2+_YD['und']*4+net.step(_YD['font'])*8+net.or_(net.step(_YD['color']),net.step(v4uk))*16+_YD['strike']*32+net.step(_YD['vert'])*64+net.step(_YD['hl'])*128+net.step(_YD['size'])*256
on('P2_U0',(None,'P2_U1',{p2mk:_mk,r1:as_x(STY)+t2si*STYN,rl:as_x(STYX)+t2si*4}))
e=S('P2_U1'); log(e,7,as_x(STY)+t2si*STYN,0,R1,t2nr_)
on('P2_U1',(None,'P2_U2',{w1:(as_x(STY)+t2si*STYN,t2nr_),p2x0:rl.out[0],p2x1:rl.out[1],p2x2:rl.out[2]}))
for k_,(o_,n_) in enumerate(((p2x0,v4uk),(p2x1,v4un),(p2x2,p2mk))):
    e=S(f'P2_U{k_+2}'); log(e,7,as_x(STYX)+t2si*4+k_,0,o_,n_)
    on(f'P2_U{k_+2}',(None,f'P2_U{k_+3}',{w1:(as_x(STYX)+t2si*4+k_,n_)}))
# the walk covers the whole document: the selection is set to all of it and given back at the end
on('P2_U5',(None,'W0',{wp:0,p2_wo:0,wm:2,wfirst:1,ap:0,ao:0,cp:npar,co:0,ysr:t2nr_,fpk:v4uk,fpn:v4un,ymsk:p2mk,fpy:t2si+1,fm:16,fcol:0,p2fon:1,p2fys:t2si+1,wret.r:wret.id('P2_CE')}))
on('P2_CE',(None,'RD0',{lc:1,p2fon:0,p2fys:0,cp:p2sc,co:p2so,ap:p2sa,ao:p2sb}))
net.group(_p2g)

# ---- p2: Restart at 1 and Continue Numbering, from the List Style menu ----
# The caret paragraph's restart flag is a quarter in feat1's paragraph cell (below every threshold its other readers use); alv says set (1) or clear (0).
_p2l=net.cur[0]; net.group('p2 list restart')
on('P2_RS0',(None,'P2_RS1',{r1:cb+F1PX}))
e=S('P2_RS1'); _q=net.bits(R1*4,4,e)[0]; _nv=as_x(R1)-_q*0.25+alv*0.25; log(e,6,cp,F1PX,R1,_nv)
on('P2_RS1',(None,'RD0',{w1:(cb+F1PX,_nv),w2:(cb+DIRTY,1),lc:1}))
net.group(_p2l)

# ---- p2: Insert Link (Ctrl+K) ----
# The address typed in the prompt bar becomes a new external entry of feat1's link table; then each selected cell is interned again with that link id,
# underlined and in Word's hyperlink blue (0563C1, palette entry 15 nearest), as Word's Hyperlink style draws it. One undo group. Saved, read and
# printed as any link read from a file.
_p2k=net.cur[0]; net.group('p2 insert link')
_nid=net.min_(f1nl+1,F1N); _lb=as_x(F1LT)+p2nid*F1LS
e=S('P2_LK0'); on('P2_LK0',(net.or_(ONE-has_sel,net.lt(prl,1,e)),'RD0',None),(None,'P2_LK1',{p2nid:_nid,f1nl:_nid,v4i:0,grp:grp+1,p2p:lo_p,p2o:lo_o,p2m:0}))
# All Caps and Small Caps from the right-click menu: the same walk sets or clears the extended field's bit; as Word toggles, the first selected character decides
e=S('P2_CA0'); on('P2_CA0',(ONE-has_sel,'RD0',None),(None,'P2_CA1',{r1:as_x(PT)+lo_p,grp:grp+1,p2p:lo_p,p2o:lo_o}))
on('P2_CA1',(None,'P2_CA2',{rs:R1+1024+lo_o}))
e=S('P2_CA2'); _xb=net.bits(RSX,18,e); on('P2_CA2',(None,'P2_LK3',{p2w:ONE-G_(_xb[0],net.eq(p2m,1,e))-G_(_xb[1],net.eq(p2m,2,e))}))
e=S('P2_LK1'); on('P2_LK1',(net.or_(net.ge(v4i,prl,e),net.ge(v4i,F1LS-3,e)),'P2_LK3',{w1:(_lb+1+v4i,0),w2:(_lb,1)}),(None,'P2_LK2',{r1:as_x(PRB)+v4i}))
on('P2_LK2',(None,'P2_LK1',{w1:(_lb+1+v4i,R1),v4i:v4i+1}))
on('P2_LK3',(None,'P2_LK4',{r1:as_x(PT)+p2p}))
on('P2_LK4',(None,'P2_LK5',{p2b:R1,rl:R1+LEN}))
on('P2_LK5',(None,'P2_LK6',{p2l:rl.out[0]}))
e=S('P2_LK6'); on('P2_LK6',(net.ge(p2p*2048+p2o,Hi,e),'RD0',{lc:1}),(net.ge(p2o,p2l,e),'P2_LK3',{p2p:p2p+1,p2o:0}),(None,'P2_LK7',{rs:p2b+1024+p2o}))
e=S('P2_LK7'); fen.lin(e); fin.add(e,RSR); fcl.add(e,RSC)
_hb=net.bits(RSH,20,e); _nh=as_x(RSH)-sum((_hb[k_]*(1<<k_) for k_ in range(12)),X())+p2nid
_cr=PAL_F.index(PAL_F[15]); _craw=(_cr&1)*256+((_cr>>1)&1)*512+((_cr>>2)&1)*1024+((_cr>>3)&1)*131072+((_cr>>4)&1)*262144
_lm=net.eq(p2m,0,e); _cm=e-_lm; _xb=net.bits(RSX,18,_cm); 
_nr=as_x(RSR)+G_(as_x(64)-FD['und']*64-FD['colraw']+_craw+(1<<22),_lm)-_lm*(1<<22)   # offset, as gates clamp
ic_en.lin(e); ic_val.add(e,_nr); ic_fb.add(e,RSC-FD['flags']); ic_k.add(e,G_(as_x(0x0563C1+1),_lm)+G_(RSK,_cm)); ic_n.add(e,RSN); ic_y.add(e,RSY)
_m1=net.eq(p2m,1,e); _m2=net.eq(p2m,2,e)
[b_.add(e,v_) for b_,v_ in zip(ic_e,(as_x(RSX)+G_((as_x(p2w)-_xb[0])*X_CAPS+8,_m1)-_m1*8+G_((as_x(p2w)-_xb[1])*X_SMC+8,_m2)-_m2*8,G_(_nh,_lm)+G_(RSH,_cm),RSZ))]
on('P2_LK7',(None,'P2_LK8',{p2old:RSC,p2fl:FD['flags']}))
e=S('P2_LK8'); _wn=ROUT+p2fl; log(e,5,p2p,p2o,p2old,_wn)
on('P2_LK8',(None,'P2_LK6',{w2:(p2b+1024+p2o,_wn),w3:(p2b+DIRTY,1),p2o:p2o+1}))
net.group(_p2k)

# ---- p2: Ctrl+click on an internal link moves the caret to its bookmark ----
# The clicked character's link id gives the link table entry; an anchor (kind 2) is compared, character by character, with each bookmark name;
# the first character carrying the matching bookmark id takes the caret. An external link needs the host to open a page, which the glue does not do.
_p2f=net.cur[0]; net.group('p2 follow link')
on('P2_FL0',(None,'P2_FL1',{rs:cb+1024+net.min_(co,clen-1)}))
e=S('P2_FL1'); _hb=net.bits(RSH,20,e); _lk=sum((_hb[k_]*(1<<k_) for k_ in range(12)),X())
on('P2_FL1',(net.eq(_lk,0,e),'IDL2',None),(None,'P2_FL2',{p2old:_lk,r1:as_x(F1LT)+_lk*F1LS}))
e=S('P2_FL2'); on('P2_FL2',(net.eq(R1,2,e),'P2_FB1',{p2nid:1,v4i:0}),(None,'IDL2',None))
e=S('P2_FB1'); on('P2_FB1',(net.gt(p2nid,f1nb,e),'IDL2',None),(None,'P2_FB2',{r1:as_x(F1BT)+p2nid*F1BS+v4i,r2:as_x(F1LT)+p2old*F1LS+1+v4i}))
e=S('P2_FB2'); _ne=net.step(net.gt(R1,R2,e)+net.lt(R1,R2,e))
on('P2_FB2',(_ne,'P2_FB1',{p2nid:p2nid+1,v4i:0}),(net.eq(R1,0,e),'P2_FS1',{p2p:0,p2o:0}),(net.ge(v4i,F1BS-2,e),'P2_FS1',{p2p:0,p2o:0}),(None,'P2_FB1',{v4i:v4i+1}))
e=S('P2_FS1'); on('P2_FS1',(net.ge(p2p,npar,e),'IDL2',None),(None,'P2_FS2',{r1:as_x(PT)+p2p}))
on('P2_FS2',(None,'P2_FS3',{p2b:R1,rl:R1+LEN}))
on('P2_FS3',(None,'P2_FS4',{p2l:rl.out[0]}))
e=S('P2_FS4'); on('P2_FS4',(net.ge(p2o,p2l,e),'P2_FS1',{p2p:p2p+1,p2o:0}),(None,'P2_FS5',{rs:p2b+1024+p2o}))
e=S('P2_FS5'); _hb=net.bits(RSH,20,e); _bk=sum((_hb[12+k_]*(1<<k_) for k_ in range(8)),X())
on('P2_FS5',(net.eq(_bk,p2nid,e),'MVJ',{jp:p2p,jo:p2o,jret.r:jret.id('MVCL')}),(None,'P2_FS4',{p2o:p2o+1}))
net.group(_p2f)
