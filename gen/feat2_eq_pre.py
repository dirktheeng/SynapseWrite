# ---- feat2: more built up forms, rule lists that the rv_a6 states take in. States are in gen/feat2_eq.py ----
# Record kinds: 1 fraction, 2 square root (rv_a6); 3 root with an index, 4 n-ary with limits, 5 accent, 6 delimiter, 7 two row matrix.
# Record cell 6 is the sub kind: n-ary 1 sum, 2 product, 3 integral; accent 1 hat, 2 bar, 3 tilde, 4 dot, 5 vector;
# delimiter: its character, 40 ( 41 ) 91 [ 93 ] 124 opening bar, 125 closing bar. Cell 7 is the n-ary symbol width.
# Texts: root: index then radicand; n-ary: lower then upper limit; accent: the base; matrix: first row then second, & between columns.
F2KW=[('root(',3,0),('sum(',4,1),('prod(',4,2),('int(',4,3),('hat(',5,1),('bar(',5,2),('tilde(',5,3),('dot(',5,4),('vec(',5,5),('mat(',7,0)]
F2DL=[('left(',40),('left[',91),('left|',124),('right)',41),('right]',93),('right|',125)]
def F2Q_KW(e,W8,ok):
    "Linear form keywords, at the scan state: a group keyword starts its first group, a delimiter is a record of its own."
    c_={}
    def m(w):
        for i_,ch in enumerate(w):
            if (i_,ch) not in c_: c_[(i_,ch)]=net.eq(W8[i_],ord(ch),e)
        return net.and_(ok,*[c_[(i_,ch)] for i_,ch in enumerate(w)])
    r=[(m(w),'A6Q_R0',{a6qj:a6qi+len(w),a6qd:1,a6qkd:k,a6qsb:s,a6qkl:len(w)}) for w,k,s in F2KW]
    r+=[(m(w),'A6Q_B0',{a6qkd:6,a6qsb:s,a6qnb:0,a6qnl:0,a6qdb:0,a6qdl:0,a6qsr:a6qi,a6qe:a6qi+len(w)}) for w,s in F2DL]
    return r
def F2Q_WD(e):
    "Widths of the new kinds."
    k=lambda v: net.eq(a6qkd,v,e)
    return (G_(net.relu(a6qnw-2)+a6qdw+10,k(3))+G_(net.max_(net.max_(a6qsw,a6qnw),a6qdw)+4,k(4))+G_(a6qnw+2,k(5))+G_(as_x(6),k(6)))
def F2Q_PAINT(e,RQ,qs,bg):
    return [(net.eq(RQ[0],3,e),'F2Q_K3',{**qs,rA:bg,sx:x}),(net.eq(RQ[0],4,e),'F2Q_K4',{**qs,rA:bg}),(net.eq(RQ[0],5,e),'F2Q_K5',{**qs,rA:bg,sx:x+1}),
            (net.eq(RQ[0],6,e),'F2Q_K6',{**qs,rA:bg}),(net.eq(RQ[0],7,e),'P3_MP0',{**qs,rA:bg})]
def F2Q_XML(e,out,qx): return [(net.eq(out[0],k_,e),f'F2Q_X{k_}' if k_<7 else 'P3_X7',qx) for k_ in range(3,8)]
def F2Q_PDF(e): return [(net.eq(a6qkd,k_,e),f'F2Q_P{k_}' if k_<7 else 'P3_PP0',None) for k_ in range(3,8)]
