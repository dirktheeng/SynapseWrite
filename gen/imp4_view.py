# ---- imp4: sliding a page wider than the window, and the vertical ruler ----
net.group('view: side scroll and vertical ruler')
e=S('V8_HS0'); _zw_=net.gate(s_pw,ONE-zany)+sum((net.gate(s_pw,h_)*z_ for h_,z_ in zip(ZLH,ZL)),X()); _xl=net.gate(s_px,ONE-zany)+sum((net.gate(s_px-ZCX+1000,h_)*z_+h_*(ZCX-1000*z_) for h_,z_ in zip(ZLH,ZL)),X())
on('V8_HS0',(None,'V8_HS1',{hsmax:net.relu(_zw_+40-1262)}))
e=S('V8_HS1'); on('V8_HS1',(None,'V8_HS2',{hsv:net.min_(hsv,hsmax),zwd:net.step(hsmax)}))
e=S('V8_HS2'); on('V8_HS2',(v8u,'UI',{zsf:as_x(4096)+G_(as_x(20)-_xl-hsv+3000,zwd)-zwd*3000,v8u:0}),(None,'RD0',{zsf:as_x(4096)+G_(as_x(20)-_xl-hsv+3000,zwd)-zwd*3000,fastok:0,autos:0}))
# the bar along the foot of the document area. A click beside the thumb moves by a window's part.
_tk=[1262/(816*z_+40) for z_ in ZL]; _lg=(243,242,241)
# p1: the thumb's scale per level and orientation: a page wider than 900 px is drawn at the landscape scale (1056 px)
p1_land=net.gt(s_pw,900,S('V8_E0')); p1_tkh=[net.and_(h_,ONE-p1_land) for h_ in ZLH]+[net.and_(h_,p1_land) for h_ in ZLH]
_tk=_tk+[1262/(1056*z_+40) for z_ in ZL]; ZLH2=p1_tkh
on('V8_E0',(zwd,'V8_V0',{rA:(0,DOCB-12,1262,12,_lg,250),rB:(sum((net.gate(hsv,h_)*k_ for h_,k_ in zip(ZLH2,_tk)),X()),DOCB-9,sum((h_*round(1262*k_) for h_,k_ in zip(ZLH2,_tk)),X()),8,(205,205,205),250),v8tx:sum((net.gate(hsv,h_)*k_ for h_,k_ in zip(ZLH2,_tk)),X()),v8tw:sum((h_*round(1262*k_) for h_,k_ in zip(ZLH2,_tk)),X())}),(None,'V8_V0',None))
e=S('V8_HC'); on('V8_HC',(net.lt(hx_,v8tx,e),'V8_HS0',{hsv:net.relu(hsv-400),v8u:0,drag:0}),(net.ge(hx_,v8tx+v8tw,e),'V8_HS0',{hsv:hsv+400,v8u:0,drag:0}),(None,'RD0',{drag:0,v8dg:1,v8x0:hx_,v8h0:hsv}))
# vertical ruler: scale of the first page in view, at the window's left. Each mark is one token.
_vc=(138,136,134); _zs_=(ONE-zany)+sum((h_*z_ for h_,z_ in zip(ZLH,ZL)),X())
_vb0=zfy0(as_x(vrt)-scroll+DOCY+vrm)
e=S('V8_V0')
_vh=sum((net.gate(vrh,h_)*z_ for h_,z_ in zip(ZLH,ZL)),X())+net.gate(vrh,ONE-zany)
_vt=net.max_(_vb0,as_x(DOCY)); _ve=net.min_(_vb0+_vh,as_x(DOCB))
on('V8_V0',(net.and_(t1_ruler,ONE-rdm,ONE-p1vf,full),'V8_V1',{rA:(2,DOCY,16,VH,(198,198,198),0),rB:(2,_vt,16,net.relu(_ve-_vt),(253,253,253),0),vrc:0}),(None,'RE3',{vrc:0}))
_vi=[]
for q_ in range(1,41):
    o_=q_*24
    if q_%4==0: _vi.append(('g',o_,48+q_//4))
    else: _vi.append(('r',o_,7 if q_%2==0 else 3))
_vt0=S('V8_V1'); fsm.states['V8_V1'][1].append((_vt0,None))
_vs=[net.reg() for _ in range(len(_vi)+1)]; net.rec(_vs[0],_vt0)
for i_,it_ in enumerate(_vi):
    t_=_vs[i_]; _y=_vb0+_zs_*it_[1]; sh_=net.and_(net.gt(vrh,it_[1],t_),net.ge(_y,DOCY+6,t_),net.lt(_y,DOCB-8,t_))
    if it_[0]=='r': rA.drive(sh_,(as_x(10)-it_[2]*0.5,_y,it_[2],1,_vc,0))
    else:
        g_en.lin(sh_); g_draw.lin(sh_); g_ch.lin(sh_*it_[2]); g_st.lin(sh_*rom.lit(11)); g_x.lin(sh_*7); g_y.add(sh_,_y+YB-7); fg[1].lin(sh_); bg[0].lin(sh_)
    net.rec(_vs[i_+1],t_)
net.rec(S('RE3'),_vs[-1])
