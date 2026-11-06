"""Reviewer a12: the reader must terminate and stay inside its memory on any input.
Three separate duties: a validator keeps the current document when the bytes are not a zip at all, the inflate
stream ends at its input and output limits, and a tick budget catches any remaining reader loop by steering the
token out through back edges of the reader's state graph (see FSM.finish). A budget hit ends the read gracefully."""
rdmode=net.reg(); rdcnt=net.reg(); rddoc=net.reg(); ovp=R(); ovn=R()
RD_BUDGET=45000000
# the zip validator: an end record in the last 64 KB, the only place the format allows one
e=S('A12_OV0'); on('A12_OV0',(net.lt(evc,22,e),'RD0',{pfile:PMSG}),(None,'A12_OV1',{ovp:evc-22,ovn:0}))
on('A12_OV1',(None,'A12_OV2',{rl:FA+ovp}))
e=S('A12_OV2'); _sig=net.and_(net.eq(W[0],80,e),net.eq(W[1],75,e),net.eq(W[2],5,e),net.eq(W[3],6,e))
on('A12_OV2',(_sig,'IMP_V0',{rl:FA+ovp+16}),(net.or_(net.eq(ovp,0,e),net.ge(ovn,65535,e)),'RD0',{pfile:PMSG}),(None,'A12_OV1',{ovp:ovp-1,ovn:ovn+1}))
# The main part is inflated before anything of the current document is touched. If it fails, or does not come to the size the directory states, the file is refused and the document stays. The output stays in place for the read proper.
on('IMP_V0',(None,'X_C0',{vdry:1,zp0:W[0]+W[1]*256+W[2]*65536,zp:W[0]+W[1]*256+W[2]*65536,ztarget:4,obase:OUTB,ob:0}))
exec(open('imp6_crc.py').read())
on('IMP_VF',(None,'RD0',{vdry:0,obase:OUTB,pfile:PMSG}))
fsm.set(obase,S('OP0'),OUTB); fsm.set(rdmode,S('OP0'),1); fsm.set(rddoc,S('OP0'),1); fsm.set(rdmode,S('IMP_V0'),1); fsm.set(rddoc,S('IMP_V0'),1)
fsm.set(rdmode,S('PG_0'),1); fsm.set(rddoc,S('PG_0'),0)
fsm.set(rdmode,S('OPEND'),0); fsm.set(rdmode,S('HALT'),0)
# The budget counts by its own bias: once loaded with 1 it adds 1 per tick through its self connection, one edge a tick, and reading it costs nothing.
_rc=next(iter(rdcnt.t)); net.bias[_rc]=1.0; _rl=S('OP0')+S('PG_0')+S('IMP_V0'); net.rec(rdcnt,rdcnt-net.relu(rdcnt+1+(_rl+S('OPEND')+S('HALT'))*M-M)+_rl)
# Any end of input or output: what was decoded so far is all there is.
on('A12_IE',(None,'IR',{oi:0}))
# The end of every inflated member gets a sentinel holding each terminator that attribute and tag scans wait for.
_SENT=[34,62,60,34,62,60,34,62]
for i_,c_ in enumerate(_SENT):
    on(f'A12_S{i_}',(None,f'A12_S{i_+1}' if i_<len(_SENT)-1 else 'T3_ZX',{wo:(OA+ob+i_,c_)}))
fsm.trap=net.ge(rdcnt,RD_BUDGET,rdmode); fsm.trap_to='A12_TRAP'; fsm.trap_roots=('OP0','PG_0','IMP_V0'); fsm.trap_bar=('OPEND','HALT','INS','SPLIT','PG_Q2','OR','SYNC','T3_PF','A12_TRAP')
on('A12_TRAP',(rddoc,'OPEND',{rdmode:0,obase:OUTB,pgdoc:0}),(None,'HALT',{rdmode:0,obase:OUTB,pgdoc:0}))
# A manual page break is a paragraph property, so it goes through the undo log like the others.
log(S('PB2'),6,cp,PBRK,0,1)
