# XML tags the document scan reacts to, beyond the baseline set
def T3_PX_MORE(e): return [(pat('<wp:exte',e),'T3_EX0',{oi:oi+8}),(pat('<a:blip ',e),'T3_BL0',{oi:oi+8}),
 (pat('<w:footn',e),'T3_RF0',{oi:oi+8}),(pat('<w:comme',e),'T3_RC0',{oi:oi+8}),
 (pat('<w:pageB',e),'T3_RB2',{oi:oi+8}),(pat('<w:softH',e),'INS',{ins_ch:173,ins_st:csi+rhi,oi:oi+8,oret.r:oret.id('PX')}),(pat('<w:br/>',e),'RVA3_RBR',{oi:oi+7}),(pat('<w:br ',e),'T3_RB0',{oi:oi+6}),(pat('<w:tab/>',e),'T3_RT0',{oi:oi+8}),(pat('<w:tab ',e),'T3_RT1',{oi:oi+7}),(pat('<w:ind ',e),'T3_RI0',{oi:oi+7}),
 (pat('<w:sectP',e),'PX',{sv_nc:1,sv_pw:816,sv_ph:PH,sv_ml:96,sv_mr:96,sv_mt:96,sv_mb:96,oi:oi+8}),(pat('</w:sect',e),'T3_RE0',{oi:oi+8}),
 (pat('<w:pgSz ',e),'T3_RZ0',{oi:oi+8}),(pat('<w:pgMar',e),'T3_RZ0',{oi:oi+8}),(pat('<w:cols ',e),'T3_RZ0',{oi:oi+8}),(pat('<w:title',e),'PX',{hftp:1,oi:oi+8}),
 (pat('<w:heade',e),'T3_RH0',{oi:oi+8,rhk:0}),(pat('<w:foote',e),'T3_RH0',{oi:oi+8,rhk:2})]
sv_nc=R();sv_pw=R();sv_ph=R();sv_ml=R();sv_mr=R();sv_mt=R();sv_mb=R();rhk=R()
