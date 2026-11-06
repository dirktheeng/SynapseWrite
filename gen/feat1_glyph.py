# ---- feat1: the extended field of a style entry, as the glyph network sees it ----
# Extended field (entry cell 4): caps 1, small caps 2, double strike 4, hidden 8, character spacing in bits 4-13 as twips+512 (0 for none).
# Most characters have none, so one neuron answers for them and the digits are read only when it fires.
X_CAPS,X_SMC,X_DST,X_HID,X_SP=1,2,4,8,16
def x_decode(val,en):
    v=as_x(val); nz=net.step(v-0.5+(as_x(en)*M-M if en is not None else 0)); b=net.bits(v,24,nz)   # p3: bits 14-23 hold the character scale
    sp=sum((b[k_]*(1<<(k_-4)) for k_ in range(4,14)),X())
    g=lambda x_: net.gate(x_,nz)   # a pull reads the one nonzero test first, so the digits are never pulled for plain text
    return dict(nz=nz,caps=g(b[0]),smc=g(b[1]),dst=g(b[2]),hid=g(b[3]),sp=sp,spn=g(net.step(sp)))
_f1g=net.cur[0]; net.group('feat1 run effects')
F1G=x_decode(F1_EX,None)   # the bus is driven only beside g_en, so it needs no enable, and a zero field never wakes a neuron
_f1c=net.gate(g_ch.w,F1G['nz'])   # zero for the usual character, so the tests below are not pushed as the text changes
_f1low=net.gate(net.and_(net.or_(F1G['caps'],F1G['smc']),net.or_(net.and_(net.ge(_f1c,97,F1G['nz']),net.lt(_f1c,123,F1G['nz'])),net.and_(net.ge(_f1c,224,F1G['nz']),net.lt(_f1c,255,F1G['nz']),ONE-net.eq(_f1c,247,F1G['nz'])))),F1G['nz'])
F1_CH=g_ch.w-_f1low*32                     # caps and small caps draw and measure the capital
F1_SMCL=net.gate(_f1low+F1G['smc']-1,F1G['nz'])        # a small capital takes a smaller compiled size
F1_HID=F1G['hid']
def F1_SPLIT(h,vflag):
    "Normal, script and small capital leaves of one size; only a flagged character goes past the first split. Hidden text, as Word shows it with marks off, gets no size: no width, no ink."
    n_,s_=tsplit(h,net.step(vflag+F1_SMCL+F1_HID)); s_=tnode(s_,F1_HID,True)
    # p2: a small capital (not raised or lowered) takes its own size, 0.8 of the run's, not the script size
    v_,c_=tsplit(s_,net.step(F1_SMCL-vflag-0.5)); return n_,v_,c_
# character spacing in pixels, added to the advance; hidden text keeps none
_f1sen=net.gate(F1G['spn']-F1_HID,F1G['nz']); F1_SPX=net.gate(F1G['sp']*(1/15),_f1sen)-_f1sen*(512/15)
net.group(_f1g)
