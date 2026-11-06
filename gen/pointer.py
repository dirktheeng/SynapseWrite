# ---- the mouse pointer: drawn by the network, kept out of the id plane ----
# The sprite is a patch write, which never touches alpha, so hit tests read true ids at all times.
# Every event starts by restoring the colors under the sprite and ends by saving them and drawing again.
net.group('pointer')
PTW,PTH,PTHX,PTHY=28,30,12,10; PTRB=1390000       # patch size, hot spot in the patch, saved colors in the bank
bstg=R();bsq=R();bsn=R();clipn=R();clipi=R();pmsg=R();t1_prs=R();cli=R();mp_ptx=R();mp_pty=R();mp_pts_x=R();mp_pts_y=R();mp_ptr_on=R();mp_ptr_dr=R();mp_ptr_lock=R();mp_ptq=R();mp_pta=R();mp_ptc=R();mp_ptk=R();mp_ptv=R()
_ptz=net.reg(); ptsave=CopyPort(_ptz,_ptz); ptrest=CopyPort(_ptz,_ptz)   # no clip, whole screen
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
# (rows, hot spot column, hot spot row). Shapes: 0 arrow, 1 I-beam, 2 left-right, 3 up-down, 4 diagonal, 5 selection arrow.
PT_SHAPES=[(_PA,0,0),(_phalo(_PI),4,9),(_phalo(_PH),9,4),(_phalo(_ptrans(_PH)),4,9),(_phalo(_pdiag()),7,7),(_pmirror(_PA),10,0)]
dat_p=[net.wire() for _ in range(4*PTW*PTH)]
ptsh=[net.wire() for _ in PT_SHAPES]    # one enable per shape
for sh_,(rows_,hx0,hy0) in zip(ptsh,PT_SHAPES):
    for j_,r_ in enumerate(rows_):
        for i_,c_ in enumerate(r_):
            if c_=='.': continue
            xx_=i_+PTHX-hx0; yy_=j_+PTHY-hy0; assert 0<=xx_<PTW and 0<=yy_<PTH
            k_=4*(yy_*PTW+xx_); net.connect(dat_p[k_+3],sh_)
            if c_=='W':
                for q_ in range(3): net.connect(dat_p[k_+q_],sh_*255)
class SpritePort:
    "A patch write with no clip: it always covers the whole screen."
    def __init__(s,en,x,y,data,w,h): s.a=(en,x,y,data,w,h); s.z=net.reg(); net.ports.append(s)
    def rec(s,nm): e,x,y,d,w,h=s.a; return [4,e,x,y,d,w,h,s.z,s.z]
e=S('PTD')
ptbx=net.wire(); ptby=net.wire()
net.connect(ptbx,net.gate(mp_ptx+64,e)-e*(64+PTHX)); net.connect(ptby,net.gate(mp_pty+64,e)-e*(64+PTHY)+e*YB)
SpritePort(net.step(e),ptbx,ptby,dat_p,PTW,PTH)
on('HALT',(a11busy,'A11_T3',None),(bsq,'UI',{bsq:0,bstg:0,clip0:0,clip1:0}),(mp_ptr_on,'PT0',{mp_pts_x:mp_ptx,mp_pts_y:mp_pty,mp_ptr_dr:1,pix:(mp_ptx,mp_pty),ptsave:(mp_ptx-PTHX,mp_pty-PTHY,PTRB,PTW,PTH,0)}),(None,'HF',None))
on('HF',(None,'IDLE',None)); halt.lin(S('HF'))
