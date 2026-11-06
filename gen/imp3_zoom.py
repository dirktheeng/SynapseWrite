# Zoom commands, status bar controls, read mode, and pictures at other scales.
_g0=net.cur[0]
net.group('zoom')
zu=R();zv=R();zrs=R();zvr=R()
ZPCT=[50,75,100,125,150,175,200,250,300,400,500]; ZVH=[1204,803,602,482,402,344,301,241,201,151,120]; NZT=len(ZPCT)
e=S('IMP3_ZA'); _h=[net.eq(zt,k_,e) for k_ in range(NZT)]
_a={ZLH[j_]:_h[k_] for j_,k_ in enumerate([0,1]+list(range(3,NZT)))}
_a[zpct]=sum((_h[k_]*ZPCT[k_] for k_ in range(NZT)),X()); _a[VHZ]=sum((_h[k_]*ZVH[k_] for k_ in range(NZT)),X())
on('IMP3_ZA',(None,'V8_HS0',{**_a,t1_rv:0,clip0:0,clip1:0,v8u:1}))
on('IMP3_ZI',(None,'IMP3_ZA',{zt:net.min_(zt+1,NZT-1)})); on('IMP3_ZO',(None,'IMP3_ZA',{zt:net.relu(zt-1)})); on('IMP3_Z100',(None,'IMP3_ZA',{zt:2})); on('IMP3_ZP',(None,'IMP3_ZA',{zt:0})); on('IMP3_ZW',(None,'IMP3_ZA',{zt:4}))
# a click in the status bar
e=S('IMP3_ZC'); _lv=sum((net.ge(hx_,1109+112/(NZT-1)*(k_+0.5),e) for k_ in range(NZT-1)),X())
on('IMP3_ZC',(net.and_(net.ge(hx_,1000,e),net.lt(hx_,1024,e),ONE-rdm),'IMP3_RE',None),(net.and_(net.ge(hx_,1000,e),net.lt(hx_,1050,e),rdm),'IMP3_RX',None),
 (net.and_(net.ge(hx_,1088,e),net.lt(hx_,1106,e)),'IMP3_ZO',None),(net.and_(net.ge(hx_,1224,e),net.lt(hx_,1242,e)),'IMP3_ZI',None),(net.and_(net.ge(hx_,1106,e),net.lt(hx_,1224,e)),'IMP3_ZA',{zt:_lv}),(None,'HALT',None))
# status bar painter
_g=(150,150,150); _d=(90,90,90); _bl=(43,87,154); _bk=(243,242,241)
on('IMP3_ZS0',(None,'IMP3_ZS0b',{rA:(1086,777,194,23,_bk,0),rB:(640,796,446,4,_bk,0)}))
on('IMP3_ZS0b',(None,'IMP3_ZS1',{rB:(1110,788,112,1,_g,0),rC:(1092,788,10,1,_d,0),rD:(1228,788,9,1,_d,0)}))
on('IMP3_ZS1',(None,'IMP3_ZS2',{rA:(1232,784,1,9,_d,0),rB:(zt*(112/(NZT-1))+1109,782,3,13,_d,0),rC:(1000,796,50,2,_bk,0),rD:(1000+(ONE-rdm)*26,796,24,2,_bl,0),sx:1244}))
text_chain('IMP3_ZS2',[zpct,'%'],'IMP3_ZS6')
on('IMP3_ZS6',(None,'ST1',{sx:12}))
on('IMP3_MK',(None,'UI',{t1_marks:ONE-t1_marks,clip0:0,clip1:0}))
# all styles: a menu written from the style table. Ten rows at a time; the last row moves on and comes back round
MSX=900; MSW=156; MSN=10
on('IMP3_SM',(None,'T1_M0',{t1_mop:13,t1_mrow:99,t1_mtop:127,t1_mx:MSX,clip0:0,clip1:0,zso:0}))
e=S('T1_MM13'); on('T1_MM13',(net.ge(zso,nsty,e),'T1_MM13',{zso:0}),(None,'IMP3_SM1',{zr:0,rA:(MSX+2,129,MSW+1,RH*(MSN+1)+1,(200,198,196),0),rB:(MSX-1,126,MSW+2,RH*(MSN+1)+2,(150,148,146),0),rC:(MSX,127,MSW,RH*(MSN+1),WHITE,0)}))
e=S('IMP3_SM1'); _sy=as_x(127)+zr*RH; _sh=net.ge(zso+zr,nsty,e)
on('IMP3_SM1',(net.ge(zr,MSN,e),'IMP3_SM5',None),(_sh,'IMP3_SM5',None),(None,'IMP3_SM2',{zc:0,sx:MSX+8,rA:(MSX,_sy,MSW,RH,WHITE,254),rB:(MSX,_sy,3,G_(as_x(RH),net.eq(t1_mrow,zr,e)),(43,87,154),254)}))
on('IMP3_SM2',(None,'IMP3_SM3',{r1:as_x(STY)+(zso+zr)*STYN+28+zc}))
e=S('IMP3_SM3'); on('IMP3_SM3',(net.or_(net.eq(R1,0,e),net.ge(zc,18,e)),'IMP3_SM1',{zr:zr+1}),(None,'IMP3_SM2',{gly:(R1,0,sx,_sy+2,0,0),sx:sx+adv,zc:zc+1}))
e=S('IMP3_SM5'); on('IMP3_SM5',(None,'IMP3_SM6',{rA:(MSX,as_x(127)+RH*MSN,MSW,RH,WHITE,254),rB:(MSX,as_x(127)+RH*MSN,3,G_(as_x(RH),net.eq(t1_mrow,MSN,e)),(43,87,154),254),sx:MSX+8}))
text_chain('IMP3_SM6',['More styles'],'T1_END',y=as_x(127)+RH*MSN+2,f=0,b=0)
e=S('IMP3_SA'); on('IMP3_SA',(net.lt(t2si,nsty,e),'T2_SA0',None),(None,'T1_MX',None))
# read mode: the bars are covered, the ruler goes, and only moving, finding, copying and printing keys act
on('IMP3_RE',(None,'UI',{rdm:1,zvr:t1_ruler,t1_ruler:0,t1_rv:0,clip0:0,clip1:0}))
on('IMP3_RX',(None,'UI',{rdm:0,t1_ruler:zvr,t1_rv:0,clip0:0,clip1:0}))
on('IMP3_RB',(None,'IMP3_RB1',{rA:(0,0,1280,174,(243,242,241),0),rB:(0,173,1280,1,(198,198,198),0),sx:500}))
text_chain('IMP3_RB1',['Read Mode: press Esc to edit'],'T1_M0',y=as_x(100))
# pictures: one destination pixel at a time. The source row advances when the scaled position passes it
_zs=lambda e_:sum((net.gate(as_x(e_),h_)*z_ for h_,z_ in zip(ZLH,ZL)),X())
_zi=lambda e_:sum((net.gate(as_x(e_),h_)*(1/z_) for h_,z_ in zip(ZLH,ZL)),X())
on('IMP3_IM0',(None,'IMP3_IM1',{zu:0,zv:0,zrs:0}))
e=S('IMP3_IM1'); on('IMP3_IM1',(net.ge(zv,_zs(pih),e),'T3_IH0',None),(net.ge(zu,_zs(pim),e),'IMP3_IM2',{zu:0,zv:zv+1}),(None,'IMP3_IM1',{imr:(zfx0(x)+zu,zfyb(sy)+zv,as_x(IMG0)+pio+iaddr+_zi(zu),1,1,1),zu:zu+1}))
e=S('IMP3_IM2'); on('IMP3_IM2',(net.ge(_zi(zv),zrs+1,e),'IMP3_IM2',{zrs:zrs+1,iaddr:iaddr+pim}),(None,'IMP3_IM1',None))
net.group(_g0)
