# ---- imp6: zip CRC check on open ----
# The dry inflate of the main part ends in IMP_V1. Its bytes at OUTB go through the save path's CRC network
# (A7_CR, four bytes a step), and the sum with the directory's CRC must be all ones in each half. A main part
# cut at the output limit is not checked, since its CRC cannot be known.
_g6=net.cur[0]; net.group('zip crc check')
i6cl=R(); i6ch=R()
on('IMP_V1',(None,'IMP6_C0',{rl:FA+zp+16}))
on('IMP6_C0',(None,'A7_CR',{i6cl:W[0]+W[1]*256,i6ch:W[2]+W[3]*256,a7_cra:as_x(OUTB),a7_crn:ob,a7cr.r:a7cr.id('IMP6_C1')}))
e=S('IMP6_C1')
_ok=net.or_(net.and_(net.eq(crcL+i6cl,65535,e),net.eq(crcH+i6ch,65535,e)),ONE-net.eq(ob,vusz,e))
on('IMP6_C1',(_ok,'OP0',{vdry:0,vob:ob}),(None,'IMP_VF',None))
net.group(_g6)
