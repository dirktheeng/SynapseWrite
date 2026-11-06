# ---- rv_a9: display list sequencer. Every ribbon, backstage page, menu and fixed label is a list of records in memory, and this
# one subnetwork plays them, an item per tick, so the drawing weights are shared by all of them. A list used to be a token neuron per item.
# Record: op, x, y+YB, then rect: w h r g b id hover_r hover_g hover_b key sel; glyph: char style fg bg hover_bg.
# sel picks the hover source register for ops 2 and 3, or the condition for op 4.
# Ops: 1 rect, 2 rect with hover, 3 rect with hover and press, 4 rect drawn on a condition, 5 glyph, 6 glyph on hover background, 7 return, 8 end.
import ui
_a9g=net.cur[0]; net.group('ribbon display list')
A9_DLN=14; DLROM=66000000; DLEND=67000000; region('a9 display lists',DLROM,DLEND); a9_rom=[]; a9_seen={}
def a9_put(cells):
    "Interns a run of cells in the ROM and gives its address."
    k_=tuple(cells)
    if k_ not in a9_seen:
        a9_seen[k_]=DLROM+len(a9_rom); a9_rom.extend(cells); assert DLROM+len(a9_rom)<DLEND
    return a9_seen[k_]
def a9_latch(tok,done):
    "A return address as one bit: set by the caller's token, spent when the sequencer reports done."
    l_=net.reg(); net.boolreg.add(next(iter(l_.t))); fin_=net.and_(l_,done)
    net.rec(l_,l_-fin_+tok)
    return fin_
rdl=RPort(A9_DLN); a9_dlp=R(); a9_dlr=R(); a9_e=S('A9_DL'); a9_c=rdl.out
_h=net.decode(a9_c[0],9,a9_e)
_hv=net.step(_h[2]+_h[3]); a9_kon=net.wire(); _r=net.step(_h[1]+_h[2]+_h[3]+a9_kon); _g=net.step(_h[5]+_h[6])
a9_hsel=Bus(net); a9_hd=net.decode(a9_c[13],2,_hv); a9_kd=net.decode(a9_c[13],128,_h[4])
_on=net.eq(a9_hsel.w,a9_c[12],_hv); a9_prs=net.wire(); a9_prsset=[]; _pr=net.and_(_on,a9_prs,_h[3])
a9_hsrc=[t1_hov,t1_mrow]; a9_conds=[]; a9_fgm={}; a9_bgm={}; a9_hbm={}
for i_,r_ in enumerate(a9_hsrc): a9_hsel.add(a9_hd[i_],r_)
rA.b[0].lin(_r)
for j_,k_ in ((1,1),(2,2),(3,3),(4,4),(8,8)): rA.b[j_].add(_r,a9_c[k_])
for j_ in range(3):
    rA.b[5+j_].lin(net.gate(a9_c[5+j_],_r-_on)+net.gate(a9_c[9+j_],_on-_pr)+_pr*ui.PRS[j_])
fsm.set(t1_hb,_hv,_on)
g_en.lin(_g); g_draw.lin(_g); g_x.add(_g,a9_c[1]); g_y.add(_g,a9_c[2]); g_ch.add(_g,a9_c[3]); g_st.add(_g,a9_c[4])
_cb=net.and_(_h[6],t1_hb); _gb=_g-_cb
a9_fd=net.decode(a9_c[5],16,_g); a9_bd=net.decode(a9_c[6],16,_gb); a9_hd2=net.decode(a9_c[7],16,_cb); a9_dldone=_h[8]
on('A9_DL',(_h[8],None,None),(_h[7],'A9_DL',{rdl:a9_dlr,a9_dlp:a9_dlr+A9_DLN}),(None,'A9_DL',{rdl:a9_dlp,a9_dlp:a9_dlp+A9_DLN}))
def _small(m,dec,bus,v):
    if v not in m: m[v]=len(m); assert m[v]<16; bus[v].lin(dec[m[v]])
    return m[v]
def a9_enc(items,hv_reg,prs):
    "Turns the drawing items of ui.L into records."
    hs=[i_ for i_,r_ in enumerate(a9_hsrc) if r_.t==hv_reg.t][0]; o=[]
    for it in items:
        if it[0]=='r':
            _,x,y,w,h,c,a,hc,key=it
            op=1 if hc is None else 3 if (prs is not None and hc is ui.HVG) else 2
            hc_=hc or (0,0,0)
            o+=[op,x,y+YB,w,h,*c,a,*hc_,key if hc is not None else 0,hs if hc is not None else 0]
        elif it[0]=='k':
            _,cond,x,y,w,h,c,a=it
            if not any(q_.t==cond.t for q_ in a9_conds):
                a9_conds.append(cond); assert len(a9_conds)<=128; net.connect(a9_kon,net.and_(a9_kd[len(a9_conds)-1],cond))
            ki=[i_ for i_,q_ in enumerate(a9_conds) if q_.t==cond.t][0]
            o+=[4,x,y+YB,w,h,*c,a,0,0,0,0,ki]
        else:
            _,ch,st,x,y,f,b,hv=it
            hb_=_small(a9_hbm,a9_hd2,bg,5 if hv is True else hv) if hv else 0
            o+=[6 if hv else 5,x,y+YB,ch,rom.lit(st),_small(a9_fgm,a9_fd,fg,f),_small(a9_bgm,a9_bd,bg,b),hb_]+[0]*6
    return o
def a9_emit(net_,fsm_,rA_,bus_,YB_,items,st0,hv_reg,hb_,bg_,prs=None,head=None):
    """Replaces a token chain: stores the items, makes st0 start the sequencer, gives the token for done.
    head is a list shared by several callers, played first."""
    if prs is not None and not a9_prsset: a9_prsset.append(1); net.connect(a9_prs,prs)
    a_=a9_put(a9_enc(items,hv_reg,prs)+[8]+[0]*(A9_DLN-1))
    if head is None: on(st0,(None,'A9_DL',{rdl:a_,a9_dlp:a_+A9_DLN}))
    else:
        h_=a9_put(a9_enc(head,hv_reg,prs)+[7]+[0]*(A9_DLN-1))
        on(st0,(None,'A9_DL',{rdl:h_,a9_dlp:h_+A9_DLN,a9_dlr:a_}))
    return a9_latch(S(st0),a9_dldone)
ui.emit=a9_emit
net.group(_a9g)
