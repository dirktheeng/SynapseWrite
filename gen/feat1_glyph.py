# ---- feat1: the extended field of a style entry, as the glyph network sees it ----
# Extended field (entry cell 4): caps 1, small caps 2, double strike 4, hidden 8, character spacing in bits 4-13 as twips+512 (0 for none).
# Most characters have none, so one neuron answers for them and the digits are read only when it fires.
X_CAPS,X_SMC,X_DST,X_HID,X_SP=1,2,4,8,16
def x_decode(val,en):
    v=as_x(val); nz=net.step(v-0.5+as_x(en)*M-M); b=net.bits(v,14,nz)
    sp=sum((b[k_]*(1<<(k_-4)) for k_ in range(4,14)),X())
    return dict(nz=nz,caps=b[0],smc=b[1],dst=b[2],hid=b[3],sp=sp,spn=net.step(sp))
_f1g=net.cur[0]; net.group('feat1 run effects')
g_ex=Bus(net)
F1G=x_decode(g_ex.w,GE)
_f1c=g_ch.w
_f1low=net.and_(net.or_(F1G['caps'],F1G['smc']),net.or_(net.and_(net.ge(_f1c,97,F1G['nz']),net.lt(_f1c,123,F1G['nz'])),net.and_(net.ge(_f1c,224,F1G['nz']),net.lt(_f1c,255,F1G['nz']),ONE-net.eq(_f1c,247,F1G['nz']))))
F1_CH=g_ch.w-_f1low*32                     # caps and small caps draw and measure the capital
F1_SMCL=net.and_(_f1low,F1G['smc'])        # a small capital takes a smaller compiled size
F1_HID=F1G['hid']
def F1_VIS(h): return tnode(h,F1_HID,True)  # hidden text, as Word shows it with marks off: no width, no ink
def F1_SCS(i): return rom.sz_near(round(rom.SZ[i]*0.8))
# character spacing in pixels, added to the advance; hidden text keeps none
F1_SPX=net.gate(F1G['sp']*(1/15),net.and_(F1G['spn'],ONE-F1_HID))-net.and_(F1G['spn'],ONE-F1_HID)*(512/15)
net.group(_f1g)
