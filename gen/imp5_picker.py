# ---- imp5: a color picker grid ----
# A second row under More Colors opens a grid of 64 colors: eight hues (and gray) across, light tints to dark shades down.
# Each cell's exact color is a weight. A pick goes into the More Colors path at V4_HY with the color as six hex digits,
# so the exact color, the nearest palette entry, undo and save all come from that one path.
import colorsys
IMP5_PICK_ROW='Color Picker...'
def _pick():
    out=[]
    L=[0.92,0.84,0.74,0.62,0.5,0.38,0.27,0.17]
    H=[None,0.0,0.07,0.14,0.33,0.5,0.6,0.78]
    for l_ in L:
        for h_ in H:
            if h_ is None: v_=round(255*(0.98-0.98*(L.index(l_)/7.0))); out.append((v_,v_,v_))
            else: r_,g_,b_=colorsys.hls_to_rgb(h_,l_,0.85 if h_ not in (0.14,) else 0.9); out.append((round(r_*255),round(g_*255),round(b_*255)))
    return out
IMP5_PICK=_pick(); assert len(IMP5_PICK)==64 and len(set(IMP5_PICK))==64
def imp5_pick_rules(mr,CM,e):
    # row 40 of menu 3 (the second extra row) opens the grid; a grid cell sends its color to the hex path
    r_=[(net.and_(net.step(mr[3]),net.ge(t1_mrow,40,e),net.lt(t1_mrow,48,e)),'T1_M0',{t1_mop:15,t1_mrow:99,t1_mtop:115,t1_mx:270,clip0:0,clip1:0})]
    g_=net.and_(net.step(mr[15]),net.lt(t1_mrow,64,e)); d_=net.decode(t1_mrow,64,g_)
    hx_=sum((d_[i_]*(c_[0]*65536+c_[1]*256+c_[2]) for i_,c_ in enumerate(IMP5_PICK)),X())
    r_.append((g_,'V4_HY',{v4h:hx_,**CM}))
    return r_
