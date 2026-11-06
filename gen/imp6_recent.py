# ---- imp6: recent colors ----
# Eight registers hold the last exact colors applied through the More Colors path (V4_HY: typed hex, the picker grid,
# or a recent cell), each as the color plus one so that zero means empty. The newest goes first; a color already in
# the list moves to the front instead of being doubled. The text color menu draws them in a row under Color Picker,
# and a click on one sends it back into V4_HY, so the exact color, undo and save come from the one path.
IMP6_NRC=8
i6rc=[R() for _ in range(IMP6_NRC)]
def imp6_recent_cells(u,x,y):
    "The static part of the recent row: eight framed cells with hover, row ids 48 to 55."
    for i_ in range(IMP6_NRC):
        cx_=x+i_*GC; u.r(cx_,y,GC,GC,WHITE,254,PAL_B[5],48+i_); u.r(cx_+3,y+3,GC-6,GC-6,(150,150,150),254); u.r(cx_+4,y+4,GC-8,GC-8,WHITE,254)
def imp6_recent_rules(mr,CM,e):
    g_=net.and_(net.step(mr[3]),net.ge(t1_mrow,48,e),net.lt(t1_mrow,48+IMP6_NRC,e)); d_=net.decode(t1_mrow-48,IMP6_NRC,g_)
    v_=sum((G_(i6rc[k_],d_[k_]) for k_ in range(IMP6_NRC)),X())
    return [(net.and_(g_,net.step(v_)),'V4_HY',{v4h:v_-1,**CM}),(g_,'RD0',{**CM})]
