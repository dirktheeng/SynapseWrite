# ---- imp5: the wheel slides a wide page sideways ----
# Shift+wheel (modifier bit 1) turns the vertical delta into a slide; a sideways delta (ev_a, delta+1000) slides when it is at least the vertical one.
# The slide then runs through V8_HS0, which clamps it to the page and repaints, the same path as a click on the bar.
_g5=net.cur[0]; net.group('view: wheel and thumb drag')
e=S('WH'); _wb5=net.bits(evm,2,e); _dx5=eva-1000; _dy5=evc-1000
_ax5=net.relu(_dx5)+net.relu(-1*_dx5); _ay5=net.relu(_dy5)+net.relu(-1*_dy5)
_sd5=net.and_(zwd,net.step(eva),net.gt(_ax5,0,e),net.ge(_ax5,_ay5,e))
WH5=[(net.and_(_wb5[1],zwd),'V8_HS0',{hsv:net.relu(hsv+evc-1000),v8u:0,autos:0}),(_sd5,'V8_HS0',{hsv:net.relu(hsv+eva-1000),v8u:0,autos:0})]
# ---- imp5: dragging the thumb of the side bar ----
# A press on the thumb holds it (v8dg) with the press x and the slide at that moment. While held, a move sets the slide to
# the slide at the press plus the pointer's travel over the thumb's scale k, the same scale that draws the thumb. 3000 is an offset so the gated travel stays positive.
_tk5=[1262/(816*z_+40) for z_ in ZL]
_tr5=sum((net.gate(eva-v8x0+3000,h_)*(1/k_)-h_*(3000/k_) for h_,k_ in zip(ZLH,_tk5)),X())
V8DRAG={hsv:net.relu(v8h0+_tr5),v8u:0,autos:0}
net.group(_g5)
