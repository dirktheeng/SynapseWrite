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
