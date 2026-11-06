# rv_a5 registers and helpers for the .docx reader; the states are in rv_a5_docx.py.
a5nest=R();a5tcp=R();a5tp=R();a5span=R();a5pad=R();a5tre=R();a5ts=R();a5ns=R();a5aft=R();a5sk=R();a5bk=R();a5maj=R();a5min=R();a5k=R();a5end=R();a5cx=R();a5i=R();a5pb=R();a5qb=R();a5hx=R();a5cb=R()
SERIF_NAMES=('Caladea','Cambria','Times','Georgia','Garamond','Palatino','Book Ant','Bookman','Constant','Baskervi','Noto Ser','DejaVu S','FreeSeri','Minion')
def a5_serif(e_): return net.or_(*[pat(n_,e_) for n_ in SERIF_NAMES if n_!='DejaVu S'])
def a5_adv(en):
    "Bytes that can be skipped: 1 plus the run of later window cells that are not an open bracket."
    cur_=en; a_=X(c=1)
    for i_ in range(1,8):
        cur_=net.and_(cur_,ONE-net.eq(W[i_],60,cur_)); a_=a_+cur_
    return a_
def A5_PX_EARLY(e):
    "Tag rules ahead of the main list. States are by name, so these may refer to later definitions."
    return [(pat('<w:laten',e),'A5_LS',{a5sk:1,oi:oi+8}),(pat('<w:rPrCh',e),'A5_LS',{a5sk:2,oi:oi+8}),(pat('<w:pPrCh',e),'A5_LS',{a5sk:3,oi:oi+8}),(pat('<mc:Fall',e),'A5_LS',{a5sk:4,oi:oi+8}),
     (net.and_(net.step(a5nest),tag('<w:tbl',' >')),'PX',{a5nest:a5nest+1,oi:oi+6}),(net.and_(incell,tag('<w:tbl',' >')),'PX',{a5nest:1,oi:oi+6}),
     (net.and_(net.step(a5nest),pat('</w:tbl>',e)),'PX',{a5nest:a5nest-1,oi:oi+8}),
     (net.and_(net.step(a5nest),net.or_(pat('<w:gridC',e),tag('<w:tc',' >'),pat('</w:tc>',e),pat('</w:tr>',e),pat('<w:shd ',e))),'PX',{oi:oi+1}),
     (pat('<w:tcPr',e),'PX',{a5tcp:1,oi:oi+7}),(pat('</w:tcPr',e),'PX',{a5tcp:0,oi:oi+8}),(pat('<w:tblPr',e),'PX',{a5tp:1,oi:oi+8}),(pat('</w:tblP',e),'PX',{a5tp:0,oi:oi+8}),
     (net.and_(a5tp,pat('<w:jc ',e)),'PX',{oi:oi+6}),(pat('<w:tblSt',e),'A5_TS',{rl:OA+oi+8}),(pat('<w:gridS',e),'A5_GS0',{oi:oi+8}),
     (pat('<w:br/>',e),'A5_BR',{oi:oi+7}),(pat('<w:cr/>',e),'A5_BR',{oi:oi+7}),(pat('<w:noBre',e),'INS',{ins_ch:45,ins_st:cs+rhi,oi:oi+8,oret.r:oret.id('PX')}),
     (tag('<m:t',' >'),'TX0',{oi:oi+4}),(pat('<w:moveF',e),'A5_MV',{rl:OA+oi+8}),(pat('<w:moveT',e),'A5_MT',{rl:OA+oi+8}),(pat('</w:move',e),'PX',{rins:0,rdel:0,oi:oi+8}),
     (pat('<w:endno',e),'A5_EF',{oi:oi+8}),(net.and_(net.eq(ztarget,7,e),net.step(ONE-t2skip),pat('<w:conte',e)),'PX',{a5cx:1,oi:oi+8,w1:(as_x(STY)+t2si*STYN+46,1)}),
     (net.and_(a5aft,ONE-incell,tag('<w:t',' >')),'SPLIT',{a5aft:0,oret.r:oret.id('A5_TX')}),
     (net.and_(net.or_(a5aft,net.step(clen)),ONE-incell,pat('<a:blip ',e)),'SPLIT',{a5aft:0,oret.r:oret.id('A5_BLP')})]
