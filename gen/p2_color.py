# ---- p2: Word's further highlight values ----
# The record holds seven highlights in three bits, and the extended and link fields are full (feat1, p3). The eight others (dark blue, teal,
# dark green, violet, dark red, dark yellow, gray 50 and black) are kept as a run shade of their color with the blue channel one up (HL_XZ):
# the screen and the PDF draw them through the exact shade path, and the writer names a marked value as a highlight instead of a shade.
_p2c=net.cur[0]; net.group('p2 further highlights')
e=S('P2_HLX'); _hx=net.decode(p2xh,9,e)
on('P2_HLX',(net.step(p2xh),'T2_C',{ics:(cs,ics.k,ics.n,ics.y,ics.e[0],ics.e[1],sum((_hx[j_+1]*z_ for j_,z_ in enumerate(HL_XZ)),X()))}),(None,'T2_C',None))
e=S('T2RP'); _en=net.gate(e,net.step(ins_z)); fsm.set(p2xh,e,sum((net.eq(ins_z,z_,_en)*(j_+1) for j_,z_ in enumerate(HL_XZ)),X()))
net.group(_p2c)
fsm.set(p2pe,S('OP0'),0)   # p2: no paragraph style's extended field carries into a new file
