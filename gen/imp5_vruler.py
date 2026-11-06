# ---- imp5: dragging the margins on the vertical ruler ----
# A press within 5 px of the top or bottom margin edge on the vertical ruler starts a ruler drag (tdk 35 top, 36 bottom),
# keeping the press y. Release goes through A4_RU like the horizontal ruler: the travel, unzoomed and snapped to 1/16 in,
# becomes a top or bottom margin of the caret's section (T3_SP2 edits 11 and 12), with undo and a full relayout.
_g5=net.cur[0]; net.group('vertical ruler drag')
e=S('IMP5_VR0')
_zs5=(ONE-zany)+sum((h_*z_ for h_,z_ in zip(ZLH,ZL)),X())
_vb5=zfy0(as_x(vrt)-scroll+DOCY+vrm); _vh5=sum((net.gate(vrh,h_)*z_ for h_,z_ in zip(ZLH,ZL)),X())+net.gate(vrh,ONE-zany)
def _nr5(v): return net.and_(net.lt(hy_,as_x(v)+6,e),net.gt(hy_,as_x(v)-6,e))
on('IMP5_VR0',(_nr5(_vb5),'HALT',{tdk:35,tdy:hy_,tmx:0,drag:0}),(_nr5(_vb5+_vh5),'HALT',{tdk:36,tdy:hy_,tmx:0,drag:0}),(None,'HALT',{drag:0}))
def imp5_vr_ru(_kh,_u,e):
    "Rules for A4_RU: the release of a vertical ruler drag. a4dl carries the snapped travel plus 1000."
    _dy=floorv((zevy(evb)-zevy(tdy)+1200)*(1.0/6)+0.5,e)*6-200
    return [(_kh[5],'T3_SP0',{**_u,tsop:11,a4dl:_dy}),(_kh[6],'T3_SP0',{**_u,tsop:12,a4dl:_dy})]
net.group(_g5)
