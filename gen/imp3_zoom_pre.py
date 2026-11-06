# Zoom: a linear map between the document's own pixels and the screen, sitting between the paint buses and the ports.
# Levels are one-hot registers; at 100 percent none is on, so every gate here stays closed and adds no work.
# Layout, hit lists and saved files keep document pixels; only what reaches the ports and what comes back from the mouse is mapped.
ZL=[0.5,0.75,1.25,1.5]; ZLH=[net.reg() for _ in ZL]; ZCX=631
zdoc=net.step(clip0-173.5); zrul=net.reg(); VHZ=net.reg(DOCB-DOCY); zt=net.reg(2); zpct=net.reg(100); rdm=net.reg()
_zx=[net.and_(h_,net.or_(zdoc,zrul)) for h_ in ZLH]; _zy=[net.and_(h_,zdoc) for h_ in ZLH]
zany=net.or_(*ZLH)
def _zmap(e,hs,factor,a):
    e=as_x(e); o=e
    for h_,z_ in zip(hs,ZL): o=o+(factor(z_)-1)*(net.gate(e,h_)-h_*a)
    return o
def zfx0(e): return _zmap(e,ZLH,lambda z_:z_,ZCX)
def zfy0(e): return _zmap(e,ZLH,lambda z_:z_,DOCY)
def zev(e): return _zmap(e,ZLH,lambda z_:1/z_,ZCX)
def zevy(e): return _zmap(e,ZLH,lambda z_:1/z_,DOCY)
def _zw(e,hs):
    e=as_x(e); o=e
    for h_,z_ in zip(hs,ZL): o=o+(z_-1)*net.gate(e,h_)+h_*0.7
    return o
def _zwire(e): w_=net.wire(); net.connect(w_,e); return w_
# the scrollbar rule fires on the tick that closes the document clip
_ZRE2=fsm.S('RE2')
for r_ in (rA,rB,rC,rD):
    r_.z={1:_zwire(_zmap(r_.b[1].w,[net.and_(h_,ONE-_ZRE2) for h_ in _zx],lambda z_:z_,ZCX)),2:_zwire(_zmap(r_.b[2].w,[net.and_(h_,ONE-_ZRE2) for h_ in _zy],lambda z_:z_,DOCY+YB)),
          3:_zwire(_zw(r_.b[3].w,[net.and_(h_,ONE-_ZRE2) for h_ in _zx])),4:_zwire(_zw(r_.b[4].w,[net.and_(h_,ONE-_ZRE2) for h_ in _zy]))}
_zgh={}
def _zgl():
    if not _zgh:
        p_=ONE-net.step(g_fx.w)     # the pointer is a glyph and stays on the screen's own pixels
        _zgh['x']=[net.and_(h_,p_) for h_ in _zx]; _zgh['y']=[net.and_(h_,p_) for h_ in _zy]
    return _zgh
def zgx(e): return _zwire(_zmap(e,_zgl()['x'],lambda z_:z_,ZCX))
def zgy(e): return _zwire(_zmap(e,_zgl()['y'],lambda z_:z_,DOCY+YB))
def zfyb(e): return _zmap(as_x(e)+YB,ZLH,lambda z_:z_,DOCY+YB)-YB
def zoom_sizes(size_hot):
    "The size the glyph unit draws: the nearest whole point to the scaled size."
    out=[X() for _ in size_hot]; _zgy_h=_zgl()['y']; anyz=net.or_(*_zgy_h)
    for i_,h_ in enumerate(size_hot):
        n_,s_=tsplit(h_,anyz); out[i_]=out[i_]+n_
        for z_h,z_ in zip(_zgy_h,ZL):
            t_=rom.sz_near(max(4,min(72,rom.SZ[i_]*z_))); out[t_]=out[t_]+net.and_(s_,z_h)
    return out
