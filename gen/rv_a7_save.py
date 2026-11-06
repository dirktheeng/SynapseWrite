# ---- save: CRC by the word over a finished member, and plain text copied by the window ----
net.group('docx crc')
a7_cra=R();a7_crn=R();a7_cro=R();a7cr=Ret('A7_CRE')
def a7_crc_tables():
    "Four 256 entry tables as weights: a walk of a binary tree over each byte of crc xor data lights one leaf."
    def tree(parent,sels):
        if not sels: return [parent]
        sl=sels[-1]; n0=net.step(parent*M-M+(ONE-sl)-0.5); n1=net.step(parent*M-M+sl-0.5)
        return tree(n0,sels[:-1])+tree(n1,sels[:-1])
    e=S('A7_CR2'); W4_=rl.out[:4]; dbits=[]
    for c_ in W4_: dbits+=net.bits(c_,8,e)
    x=[net.step(gc2-d_-0.5+e*M-M)+net.step(d_-gc2-0.5+e*M-M) for gc2,d_ in zip(crcr,dbits)]
    out=[X() for _ in range(32)]
    def adv(c,n):
        for _ in range(n): c=crc_next(c,0)
        return c
    for p_ in range(4):
        lv=tree(e,x[8*p_:8*p_+8])
        for v_,leaf in enumerate(lv):
            o=adv(v_<<(8*p_),4)
            for j in range(32):
                if o>>j&1: out[j]=out[j]+leaf
    for j in range(32):
        s_=out[j]; par=net.step(s_-0.5)-net.step(s_-1.5)+net.step(s_-2.5)-net.step(s_-3.5)
        fsm.set(crcr[j],e,par)
a7_crc_tables()
# picture chunks are written with their running CRC, so that stream still feeds the byte network
_pc=net.and_(em_en.w,a7_png); a7_cen.lin(_pc); a7_cby.add(_pc,em_b.w); fsm.set(a7_png,S('T3_M8'),1); fsm.set(a7_png,S('T3_GPw'),0)
crci.lin(S('A7_CR'))
on('A7_CR',(None,'A7_CR1',{a7_cro:0}))
e=S('A7_CR1')
on('A7_CR1',(net.ge(a7_crn,a7_cro+4,e),'A7_CR2',{rl:a7_cra+a7_cro}),(net.ge(a7_cro,a7_crn,e),'A7_CRE',None),(None,'A7_CR3',{r1:a7_cra+a7_cro}))
on('A7_CR2',(None,'A7_CR1',{a7_cro:a7_cro+4}))
e=S('A7_CR3'); a7_cen.lin(e); a7_cby.add(e,R1)
on('A7_CR3',(None,'A7_CR1',{a7_cro:a7_cro+1}))
# text window: a run of plain characters in the current style goes straight to the output
e=S('A7_SW'); WC=rpw.out; WS=a7_rw2.out
_b=[]
for i_ in range(PSN):
    c_=WC[i_]
    _b.append(net.step(net.step(as_x(32)-c_-0.5+e*M-M)+net.step(c_-126.5+e*M-M)+net.eq(c_,38,e)+net.eq(c_,60,e)+net.eq(c_,62,e)+net.step(WS[i_]-t2psv-0.5+e*M-M)+net.step(t2psv-WS[i_]-0.5+e*M-M)))
_ls=a7_lead(_b,e); _ns=_ls-net.relu(_ls-(plen_-off)+e*M-M)
wpch.drive(net.and_(e,net.step(_ls)),(embase+fp,_ns))
on('A7_SW',(net.step(_ls),'SVC',{fp:fp+_ns,off:off+_ns}),(None,'SVr',{r1:pbs+off,r2:pbs+1024+off}))
