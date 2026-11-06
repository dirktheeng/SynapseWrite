# ---- the mouse pointer's shapes, as outlines the glyph unit draws ----
# Each shape is original pixel art. Each pixel run becomes a rectangle contour, so a shape stays exact on the pixel grid.
# Shapes: 0 arrow, 1 I-beam, 2 left-right, 3 up-down, 4 diagonal, 5 selection arrow. Hot spot is the glyph origin. A white and a black layer.
_PA=["K","KK","KWK","KWWK","KWWWK","KWWWWK","KWWWWWK","KWWWWWWK","KWWWWWWWK","KWWWWWWWWK","KWWWWWKKKKK","KWWKWWK","KWK.KWWK","KK..KWWK","K....KWWK",".....KWWK","......KK"]
_PI=["KKK.KKK","...K...","...K...","...K...","...K...","...K...","...K...","...K...","...K...","...K...","...K...","...K...","...K...","...K...","...K...","...K...","...K...","KKK.KKK"]
_PH=["...K.........K...","..KK.........KK..",".KKK.........KKK.","KKKKKKKKKKKKKKKKK",".KKK.........KKK.","..KK.........KK..","...K.........K..."]
def _pmirror(a): w_=max(map(len,a)); return [r_.ljust(w_,'.')[::-1] for r_ in a]
def _ptrans(a):
    w_=max(map(len,a)); a=[r_.ljust(w_,'.') for r_ in a]
    return [''.join(a[j_][i_] for j_ in range(len(a))) for i_ in range(w_)]
def _pdiag():
    n=13; g_=[['.']*n for _ in range(n)]
    for i_ in range(n): g_[i_][i_]='K'
    for t_ in range(1,5):
        for a_,b_ in ((0,t_),(t_,0),(n-1,n-1-t_),(n-1-t_,n-1)): g_[a_][b_]='K'
    return [''.join(r_) for r_ in g_]
def _phalo(a):
    "A one pixel white rim so a black shape stays visible on dark ink."
    w_=max(map(len,a))+2; h_=len(a)+2; g_=[['.']*w_ for _ in range(h_)]
    for j_,r_ in enumerate(a):
        for i_,c_ in enumerate(r_):
            if c_=='K': g_[j_+1][i_+1]='K'
    o_=[r_[:] for r_ in g_]
    for j_ in range(h_):
        for i_ in range(w_):
            if g_[j_][i_]=='.' and any(0<=j_+v_<h_ and 0<=i_+u_<w_ and g_[j_+v_][i_+u_]=='K' for u_ in (-1,0,1) for v_ in (-1,0,1)): o_[j_][i_]='W'
    return [''.join(r_) for r_ in o_]
PT_SHAPES=[(_PA,0,0),(_phalo(_PI),4,9),(_phalo(_PH),9,4),(_phalo(_ptrans(_PH)),4,9),(_phalo(_pdiag()),7,7),(_pmirror(_PA),10,0)]
def _layer(rows_,hx0,hy0,ch):
    "Runs of one letter as rectangles, in ems at 12 pixels per em, clockwise as a TrueType outer contour is."
    cs=[]
    for j_,r_ in enumerate(rows_):
        i_=0
        while i_<len(r_):
            if r_[i_]!=ch: i_+=1; continue
            k_=i_
            while k_<len(r_) and r_[k_]==ch: k_+=1
            x0,x1=(i_-hx0)/12,(k_-hx0)/12; y1,y0=(hy0-j_)/12,(hy0-j_-1)/12
            cs.append([(x0,y0),(x0,y1),(x1,y1),(x1,y0)])
            i_=k_
    return cs
PTR_GLYPHS={}
for i_,(rows_,hx0,hy0) in enumerate(PT_SHAPES):
    PTR_GLYPHS[33+i_*2]=(_layer(rows_,hx0,hy0,'W'),True)
    PTR_GLYPHS[34+i_*2]=(_layer(rows_,hx0,hy0,'K'),True)
