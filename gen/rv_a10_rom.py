# ---- string ROM and the one literal emitter ----
# Literal bytes live in memory, not in weights. A literal state loads an address and a count; one small
# loop reads and emits them. Identical strings and substrings share cells. Above the bank map, loaded at start.
# ROM_RUNS holds [address, bytes, bytes per value], started by the spell table; placed in the bank before the first event
LITROM=64000000; LITMAX=1000000; _litb=bytearray()
def rom_str(data):
    k=_litb.find(data)
    if k<0: k=len(_litb); _litb.extend(data); assert len(_litb)<=LITMAX
    return LITROM+k
def rom_finish(hdr):
    "Appends the ROM to the weight file. Glue copies the cells, nothing more."
    runs=[[LITROM,bytes(_litb),1]]+ROM_RUNS; hdr['rom']=[[a,len(d)//w,w] for a,d,w in runs]
    hdr['bank']=max([hdr['bank']]+[a+len(d)//w for a,d,w in runs])
    return b''.join(d for a,d,w in runs)
lit_chain=lit
lr=RPort(1); la_=R(); ln_lit=R(); lc_lit=R(); lret=Ret('A10_LR'); lbret=Ret('A10_LBR')
LO_=lr.out[0]
# per byte, so the CRC sees it: read ahead while emitting the byte read one tick before
on('A10_L0',(None,'A10_L1',{lr:la_,la_:la_+1,ln_lit:ln_lit-1}))
_e=S('A10_L1'); em_en.lin(_e); em_b.add(_e,LO_)
on('A10_L1',(net.step(ln_lit),'A10_L1',{lr:la_,la_:la_+1,ln_lit:ln_lit-1}),(None,'A10_LR',None))
# by block, for bytes the CRC need not see
_e=S('A10_B0'); _nc=net.min_(ln_lit,1100)
on('A10_B0',(net.step(ln_lit),'A10_B1',{rb:(la_,_nc),lc_lit:_nc}),(None,'A10_LBR',None))
on('A10_B1',(None,'A10_B0',{wb:(embase+fp,lc_lit),fp:fp+lc_lit,la_:la_+lc_lit,ln_lit:ln_lit-lc_lit}))
def litb(name,data,nxt):
    "Literal outside any CRC: block copy from the ROM."
    if len(data)<4: return lit_chain(name,data,nxt)
    on(name,(None,'A10_B0',{la_:rom_str(data),ln_lit:len(data),lbret.r:lbret.id(nxt)}))
def lit(name,data,nxt):
    if name.startswith(('PD_','T4P_','T3_PT')): return litb(name,data,nxt)   # PDF has no CRC
    if len(data)<4: return lit_chain(name,data,nxt)       # a chain this short costs no more than a table entry
    on(name,(None,'A10_L0',{la_:rom_str(data),ln_lit:len(data),lret.r:lret.id(nxt)}))
