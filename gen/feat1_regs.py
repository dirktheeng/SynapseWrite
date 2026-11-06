# ---- feat1: registers, tables and reader rules for extended run properties, links, bookmarks and paragraph extras ----
# Link table: entry i (1..255) at F1LT+i*256 holds the kind (1 external, by relationship; 2 anchor in the document; 0 no target), then the target bytes as they
# stand in the XML, zero ended. Bookmark names: entry i (1..255) at F1BT+i*64, zero ended. A character's entry keeps link id + 4096*bookmark id.
F1LT=1130000; F1LS=256; F1BT=1264100; F1BS=64; F1N=255; F1PX=4095
region('feat1 link targets',F1LT,F1LT+F1LS*(F1N+1)); region('feat1 bookmark names',F1BT,F1BT+F1BS*(F1N+1))
region('feat1 paragraph extras',F1PX,F1PX+1,space='slot')   # bit 0 contextual spacing, bit 1 widow control off; carried by splits with the keep cells
f1ll=R();f1lbk=R();f1nl=R();f1nb=R();f1n=R();f1neg=R();f1i=R();f1bit=R();f1pc=R();f1pw=R()
f1wl=R();f1wb=R();f1k=R();f1q=R();ins_x=R();ins_h=R();ins_z=R();f1sc=R();f1sw=R();f1nwc=R();f1qnwc=R()
f1wx=[R() for _ in range(5)]
f1lb=f1ll+f1lbk*4096
def F1_PX(e):
    "Tags for feat1, ahead of the paragraph spacing rule, which would otherwise take a run's w:spacing."
    nid_l=net.min_(f1nl+1,F1N); nid_b=net.min_(f1nb+1,F1N); dx=net.eq(ztarget,4,e)
    return [(tag('<w:caps','/ '),'F1_TV',{f1bit:X_CAPS,oi:oi+7}),(pat('<w:small',e),'F1_TV',{f1bit:X_SMC,oi:oi+12}),(pat('<w:dstri',e),'F1_TV',{f1bit:X_DST,oi:oi+10}),
     (pat('<w:vanis',e),'F1_TV',{f1bit:X_HID,oi:oi+9}),(net.and_(a4inr,pat('<w:spaci',e)),'F1_SP',{oi:oi+10}),(net.and_(a4inr,pat('<w:shd ',e)),'F1_SH',{oi:oi+7}),
     (pat('<w:hyper',e),'F1_HL',{oi:oi+12,f1ll:nid_l,f1nl:nid_l,w1:(as_x(F1LT)+nid_l*F1LS,0),w2:(as_x(F1LT)+nid_l*F1LS+1,0)}),(pat('</w:hype',e),'PX',{f1ll:0,oi:oi+8}),
     (pat('<w:bookm',e),'F1_BK',{rl:OA+oi+11}),
     (net.and_(dx,pat('<w:conte',e)),'PX',{a5cx:1,f1pc:1,w1:(cb+F1PX,1+f1pw*2+p3ol*(1/32)+p2rsr*(1/2048)),oi:oi+8}),
     (net.and_(dx,pat('<w:widow',e)),'F1_WC',{oi:oi+15})]
def F1_META(e):
    "Paragraph extras for layout: widow control off is bit 1 of the cell."
    return {f1nwc:net.ge(A4O[7],2,e)}
def F1_CX(e):
    "Contextual spacing between two paragraphs of one style that both set it, applied as rv_a5 applies a style's: the gap is dropped at the end of open."
    return net.and_(e,net.bits(rU.out[0],2,e)[0],net.bits(rV.out[0],2,e)[0])
