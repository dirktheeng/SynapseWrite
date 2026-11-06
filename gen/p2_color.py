# ---- p2: Word's further highlight values ----
# The record holds seven highlights in three bits. The eight others (dark blue, teal, dark green, violet, dark red, dark yellow, gray 50 and black)
# sit in bits 14 to 17 of feat1's extended field; the screen and the PDF draw them through the exact run shade path, and the writer names them.
_p2c=net.cur[0]; net.group('p2 further highlights')
e=S('P2_HLX'); _b=net.bits(ics.e[0],18,e); _old=sum((_b[k_]*(1<<k_) for k_ in range(14,18)),X())
on('P2_HLX',(None,'T2_C',{ics:(cs,ics.k,ics.n,ics.y,as_x(ics.e[0])-_old+p2xh*16384,ics.e[1],ics.e[2])}))
e=S('T2RP'); _b=net.bits(ins_x,18,e); fsm.set(p2xh,e,sum((_b[k_]*(1<<(k_-14)) for k_ in range(14,18)),X()))
net.group(_p2c)
