# Reviewer a3: Word style caret, selection and shortcut behavior. Registers and the key rule table.
# Exec'd before the event dispatch; the states these rules name are written in rv_a3_keys.py.
rv_wm=R();rv_ovr=R();rv_eol=R();rv_le=R();rv_try=R();rv_rekey=R();rv_pgq=R();rv_py=R();rv_s0=R();rv_pgd=R();rv_asq=R();rv_rp=R();rv_cmq=R()
rv_sH=R();rv_sL=R();rv_scp=R();rv_sco=R();rv_sap=R();rv_sao=R();rv_sh=R();rv_mhe=R();rv_hl=R();rv_hk=R()
rv_cc=R();rv_ctp=R();rv_chi=R();rv_clo=R();rv_cap=R();rv_cao=R();rv_nc=R();rv_st=R()
evm=R(); rv_qm=R(); cx=R();cy=R();chh=R(19);pwalk=R();pfld=R()
def rv_key_rules():
    nf=ONE-findon
    def KD(c): return net.and_(K(c),nf)
    def ND(c): return net.and_(N(c),nf)
    off_=net.or_(net.lt(cy,scroll+4,en),net.gt(cy+chh,scroll+VHZ-4,en))
    vert=net.or_(N(129),N(131),N(132),N(133))
    D={grp:grp+1,t1_lastk:0}
    PI_=lambda d: {pwalk:lo_p,pfld:PIND,t1_pdm:1,t1_pdd:1000+d,grp:grp+1,t1_lastk:0}
    LS_=lambda v: {pwalk:lo_p,pfld:PLSP,alv:v,grp:grp+1,t1_lastk:0}
    return [
     (N(137)-net.and_(N(137),shf),'RVA3_F3',None),(net.and_(N(137),shf),'RVA3_CC0',None),(N(140),'SAVE',{}),
     (KD(128),'RVA3_ML',None),(KD(130),'RVA3_MR',None),(KD(129),'RVA3_PU',None),(KD(131),'RVA3_PD',None),
     (KD(8),'RVA3_KB',None),(KD(127),'RVA3_KD',None),
     (net.and_(ND(13),shf),'TYPE',{eva:11}),
     (net.and_(ND(127),shf),'CUT',None),(KD(136),'COPY',None),(net.and_(ND(136),shf),'HALT',{wpaste:1}),(ND(136),'RD0',{rv_ovr:ONE-rv_ovr}),
     (net.and_(vert,off_,ONE-rv_try),'RD0',{scroll:net.relu(cy-VHZ*0.5),rv_rekey:1,rv_try:1,autos:0}),
     (ND(134),'RD0',{scroll:net.relu(scroll-(VHZ-40)),rv_s0:scroll,rv_py:net.max_(net.min_(zfy0(cy+DOCY-scroll),DOCB-30),DOCY+4),rv_pgq:1,rv_pgd:0,autos:0,t1_lastk:0}),
     (ND(135),'RD0',{scroll:scroll+(VHZ-40),rv_s0:scroll,rv_py:net.max_(net.min_(zfy0(cy+DOCY-scroll),DOCB-30),DOCY+4),rv_pgq:1,rv_pgd:1,autos:0,t1_lastk:0}),
     (KD(60),'FMTS',{fm:5}),(KD(91),'FMTS',{fm:5}),(KD(62),'FMTS',{fm:4}),(KD(93),'FMTS',{fm:4}),(KD(61),'FMTS',{fm:14}),(KD(43),'FMTS',{fm:13}),
     (net.and_(KD(ord('m')),shf),'PA0',PI_(-48)),(KD(ord('m')),'PA0',PI_(48)),
     (KD(ord('1')),'PA0',LS_(6)),(KD(ord('5')),'PA0',LS_(2)),(KD(ord('2')),'PA0',LS_(3)),
     (net.and_(KD(ord('l')),shf),'T2_LI',{alv:1}),(net.and_(KD(ord('n')),shf),'T2_SA0',{t2si:0}),
    ]
def rv_tabw(p,en_):
    "Width from pen position p to the next default stop, every half inch (48 px). All in weights."
    g_=net.relu(as_x(p)+en_*M-M); k_=X()
    for i_ in range(1,30): k_=k_+net.step(g_-48*i_+0.001)
    return en_*48+k_*48-g_
RV_HALT=[(rv_rekey,'KEY',{rv_rekey:0}),(rv_pgq,'RVA3_PG1',{rv_pgq:0}),(rv_asq,'RVA3_AS1',{rv_asq:0}),(rv_cmq,'RVA3_CM2',None),(rv_rp,'RD0',{rv_rp:0})]
