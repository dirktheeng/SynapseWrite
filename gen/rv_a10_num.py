# ---- one number writer ----
# The value is scaled so its top digit sits at 10^7. Each tick the digit is nine thresholds, then the rest moves up a place.
# A start state chooses the field: digits (nk) and whether leading zeros show (nsh). Rounding: largest integer below value+.5.
nvv=R(); nk=R(); nsh=R(); nrr=Ret('A10_NR'); _NP=10000000
_ne=net.wire(); net.connect(_ne,S('A10_N')); net.connect(_ne,S('A10_NI'))
_gv=net.gate(nvv,_ne); ndig=X()
for t in range(1,10): ndig=ndig+net.step(_gv-_NP*t)
def _start(val,digits,pad): return {nvv:(as_x(val)+0.5)*(10**(8-digits)),nk:digits,nsh:1 if pad else 0}
def vnum(st,val,nx): on(st,(None,'A10_N',{**_start(val,6,False),nrr.r:nrr.id(nx)}))
def numz(st,val,nx): on(st,(None,'A10_N',{**_start(val,8,False),nrr.r:nrr.id(nx)}))
def number(st,val,nx): on(st,(None,'A10_N',{**_start(val,7,True),nrr.r:nrr.id(nx)}))
_e=S('A10_N'); _last=net.eq(nk,1,_e); _show=net.and_(_e,net.step(nsh+_last+ndig))
em_en.lin(_show); em_b.add(_show,48+ndig)
_next=lambda: {nvv:(nvv-ndig*_NP)*10,nk:nk-1}
on('A10_N',(_last,'A10_NR',None),(None,'A10_N',{**_next(),nsh:_show}))
# the same digits typed into the document as a field, through the insert routine
_e=S('A10_NI'); _lasti=net.eq(nk,1,_e); _showi=net.and_(_e,net.step(nsh+_lasti+ndig))
def num_field(st,val_reg,sty,nx):
    "Sets up typing val_reg at state st, returning to nx."
    on(st,(None,'A10_NI',_start(val_reg,6,False)))
    on('A10_NI',(_showi,'INS',{ins_ch:48+ndig,ins_st:sty,oret.r:oret.id('A10_NJ'),**_next(),nsh:_showi}),(None,'A10_NJ',{**_next(),nsh:_showi}))
    on('A10_NJ',(net.step(nk),'A10_NI',None),(None,nx,None))
# ---- one binary field writer: zip and PNG fields, low byte first or high byte first ----
fv=R(); fk_=R(); frr=Ret('A10_FR')
_fe=net.wire(); net.connect(_fe,S('A10_F')); net.connect(_fe,S('A10_G'))
_fb=net.bits(fv,32,_fe)
_flo=sum((_fb[i]*(1<<i) for i in range(8)),X()); _fhi=sum((_fb[24+i]*(1<<i) for i in range(8)),X())
for _s,_b in (('A10_F',_flo),('A10_G',_fhi)):
    _e=S(_s); em_en.lin(_e); em_b.add(_e,_b)
on('A10_F',(net.eq(fk_,1,S('A10_F')),'A10_FR',None),(None,'A10_F',{fv:(fv-_flo)*(1/256),fk_:fk_-1}))
# the rest goes through its own gate first: a weight of 2^39 on a bit would read as a gate's enable (see nn.compile)
_frest=net.gate(fv-_fhi*(1<<24),S('A10_G'))
on('A10_G',(net.eq(fk_,1,S('A10_G')),'A10_FR',None),(None,'A10_G',{fv:_frest*256,fk_:fk_-1}))
def lefield(st,val,n,nx): on(st,(None,'A10_F',{fv:val,fk_:n,frr.r:frr.id(nx)}))
def befield(st,val,n,nx): on(st,(None,'A10_G',{fv:as_x(val)*(1<<(8*(4-n))),fk_:n,frr.r:frr.id(nx)}))
