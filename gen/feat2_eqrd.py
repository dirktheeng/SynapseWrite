# ---- feat2: math tags in a file. Each one comes here from the two prefix patterns of A6_PX_RULES with the bytes after '<m:' or '</m:' in the window.
# A built up form is typed as its linear form (the keywords of gen/feat2_eq_pre.py), which the scan at </m:oMath> builds into records.
_F2S={}
def _f2s(t):
    if t not in _F2S: _F2S[t]=rom_str(t.encode())
    return _F2S[t]
def _f2em(t,more=None,oi_=None):
    "Types the string t into the paragraph as equation characters, then reads on in the XML."
    d={f2ep:as_x(_f2s(t)),f2el:len(t)}
    if oi_ is not None: d[oi]=oi+oi_
    return {**d,**(more or {})}
def _f2sel(tab,reg,e):
    "One of several strings, chosen by a register."
    return {f2ep:sum((G_(as_x(_f2s(t)),net.eq(reg,v,e)) for v,t in tab),X()),f2el:sum((G_(as_x(len(t)),net.eq(reg,v,e)) for v,t in tab),X())}
def _f2m(e,c_,w,off=0):
    for i_,ch in enumerate(w):
        if (i_+off,ch) not in c_: c_[(i_+off,ch)]=net.eq(W[i_+off],ord(ch) if isinstance(ch,str) else ch,e)
    return net.and_(*[c_[(i_+off,ch)] for i_,ch in enumerate(w)])
e=S('F2R_E0'); on('F2R_E0',(net.eq(f2el,0,e),'PX',None),(None,'F2R_E1',{r1:f2ep}))
e=S('F2R_E1'); on('F2R_E1',(None,'A6E_IS',{**_eqstyle(e,R1),ins_ch:R1,oret.r:oret.id('F2R_E0'),f2ep:f2ep+1,f2el:f2el-1}))
_KWT=[(1,'sqrt('),(2,'hat('),(3,'bar('),(4,'tilde('),(5,'dot('),(6,'vec('),(7,'left('),(8,'left['),(9,'left|')]
_NST=[(1,'sum('),(2,'prod('),(3,'int(')]; _NSE=[(1,'sum()'),(2,'prod()'),(3,'int()')]
_DET=[(41,'right)'),(93,'right]'),(125,'right|')]
# opening tags: the window starts after '<m:'
e=S('F2R_0'); c0={}; m0=lambda w: _f2m(e,c0,w)
on('F2R_0',(m0('r>'),'PX',{ics:t2ps,rnop:0,oi:oi+5}),(net.or_(m0('t>'),m0('t ')),'A6E_R0',{oi:oi+4}),
 (net.and_(a6nx,m0('sub>')),'F2R_E0',{**_f2sel(_NST,a6ns,e),oi:oi+7}),(net.and_(a6nx,m0('sub/')),'F2R_E0',{**_f2sel(_NSE,a6ns,e),oi:oi+8}),
 (net.and_(a6nx,m0('sup>')),'F2R_E0',_f2em('(',None,7)),(net.and_(a6nx,m0('sup/')),'F2R_E0',_f2em('()',{a6nx:0},8)),
 (m0('sup>'),'PX',{a6es:1,oi:oi+7}),(m0('sub>'),'PX',{a6es:2,oi:oi+7}),
 (m0('num>'),'A6E_I1',{oi:oi+7,a6ec:40}),(m0('den>'),'A6E_I1',{oi:oi+7,a6ec:40}),
 (m0('rad>'),'PX',{a6kw:1,oi:oi+7}),(m0('deg>'),'F2R_E0',_f2em('root(',{a6kw:0},7)),
 (net.or_(m0('nary>'),m0('nary ')),'PX',{a6nx:1,a6ns:3,oi:oi+7}),
 (net.or_(m0('acc>'),m0('acc ')),'PX',{a6kw:2,oi:oi+6}),(m0('bar>'),'PX',{a6kw:3,oi:oi+6}),
 (net.or_(m0('d>'),m0('d ')),'PX',{a6kw:7,a6de:41,oi:oi+4}),
 (m0('m>'),'PX',{a6mx:1,a6mr:0,oi:oi+4}),
 (net.and_(m0('mr>'),net.eq(a6mr,0,e)),'F2R_E0',_f2em('mat(',{a6mr:1,a6mc:0},5)),(m0('mr>'),'F2R_E0',_f2em('(',{a6mr:a6mr+1,a6mc:0},5)),
 (net.and_(m0('e>'),a6mx,net.step(a6mc)),'F2R_E0',_f2em('&',{a6mc:a6mc+1},4)),(net.and_(m0('e>'),a6mx),'PX',{a6mc:a6mc+1,oi:oi+4}),
 (net.and_(m0('e>'),net.step(a6kw)),'F2R_E0',{**_f2sel(_KWT,a6kw,e),a6kw:0,oi:oi+4}),
 (m0('chr '),'F2R_C0',{rl:OA+oi+14}),(m0('begChr '),'F2R_B0',{rl:OA+oi+17}),(m0('endChr '),'F2R_N0',{rl:OA+oi+17}),
 (None,'PX',{oi:oi+1}))
# closing tags: the window starts after '</m:'
e=S('F2R_1'); c1={}; m1=lambda w: _f2m(e,c1,w)
on('F2R_1',(m1('oMat'),'A6Q_S0',{oi:oi+10,a6qi:0,a6qa:0,a6qcv:0,a6qrr.r:a6qrr.id('PX')}),
 (net.and_(a6nx,m1('sub>')),'F2R_E0',_f2em(')',None,8)),(net.and_(a6nx,m1('sup>')),'F2R_E0',_f2em(')',{a6nx:0},8)),
 (m1('sup>'),'PX',{a6es:0,oi:oi+8}),(m1('sub>'),'PX',{a6es:0,oi:oi+8}),
 (m1('num>'),'A6E_I2',{oi:oi+8,a6ec:41}),(m1('den>'),'A6E_I1',{oi:oi+8,a6ec:41}),(m1('rad>'),'A6E_I1',{oi:oi+8,a6ec:41}),
 (m1('deg>'),'F2R_E0',_f2em(')(',None,8)),
 (net.or_(m1('acc>'),m1('bar>')),'F2R_E0',_f2em(')',None,8)),
 (m1('d>'),'F2R_E0',{**_f2sel(_DET,a6de,e),oi:oi+6}),
 (m1('mr>'),'F2R_E0',_f2em(')',None,7)),(m1('m>'),'PX',{a6mx:0,oi:oi+6}),
 (None,'PX',{oi:oi+1}))
# m:chr: the n-ary sign or the accent, as UTF-8 in the attribute
e=S('F2R_C0'); cc={}; mc=lambda w: _f2m(e,cc,w)
on('F2R_C0',(mc([0xE2,0x88,0x91]),'PX',{a6ns:1,oi:oi+14}),(mc([0xE2,0x88,0x8F]),'PX',{a6ns:2,oi:oi+14}),(mc([0xE2,0x88,0xAB]),'PX',{a6ns:3,oi:oi+14}),
 (net.or_(mc([0xCC,0x82]),mc('^')),'PX',{a6kw:2,oi:oi+14}),(net.or_(mc([0xCC,0x85]),mc([0xCC,0x84]),mc([0xC2,0xAF])),'PX',{a6kw:3,oi:oi+14}),
 (net.or_(mc([0xCC,0x83]),mc('~')),'PX',{a6kw:4,oi:oi+14}),(mc([0xCC,0x87]),'PX',{a6kw:5,oi:oi+14}),(mc([0xE2,0x83,0x97]),'PX',{a6kw:6,oi:oi+14}),
 (None,'PX',{oi:oi+14}))
e=S('F2R_B0'); on('F2R_B0',(net.eq(W[0],91,e),'PX',{a6kw:8,oi:oi+17}),(net.eq(W[0],124,e),'PX',{a6kw:9,oi:oi+17}),(None,'PX',{oi:oi+17}))
e=S('F2R_N0'); on('F2R_N0',(net.eq(W[0],93,e),'PX',{a6de:93,oi:oi+17}),(net.eq(W[0],124,e),'PX',{a6de:125,oi:oi+17}),(None,'PX',{oi:oi+17}))
for _r in (a6kw,a6nx,a6mx,a6mr,a6mc,f2el): fsm.set(_r,S('OP0'),0)
