"""Original 16 pixel icons for ribbon commands, drawn on a character grid at build time. No external assets.
Palette letters are the ART table in ui.py: B blue line, l blue fill, w white, h gray line, g light line, t green, r red, D dark."""
def _cv(n=16): return [['.']*n for _ in range(n)]
def _r(c,x0,y0,x1,y1,ch):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1): c[y][x]=ch
def _box(c,x0,y0,x1,y1,line,fill='w'):
    _r(c,x0,y0,x1,y1,line); _r(c,x0+1,y0+1,x1-1,y1-1,fill)
def _plus(c,cx,cy,ch='t'): _r(c,cx-2,cy,cx+2,cy,ch); _r(c,cx,cy-2,cx,cy+2,ch)
def _x(c,x,y,ch='r'):
    for i in range(5): c[y+i][x+i]=ch; c[y+i][x+4-i]=ch
def _grid(c,x0,y0,x1,y1,xs=(),ys=()):
    _box(c,x0,y0,x1,y1,'B')
    for x in xs: _r(c,x,y0,x,y1,'B')
    for y in ys: _r(c,x0,y,x1,y,'B')
def _page(c,x0=3,y0=1,x1=12,y1=14): _box(c,x0,y0,x1,y1,'h')
def _dig(c,x,y,d,ch='B'):
    F={'1':("010","110","010","010","111"),'2':("110","001","010","100","111"),'3':("110","001","010","001","110"),'#':("01010","11111","01010","11111","01010")}[d]
    for j,row in enumerate(F):
        for i,v in enumerate(row):
            if v=='1': c[y+j][x+i]=ch
def _rows(c): return [''.join(r) for r in c]
def icons():
    out={}
    def mk(name,f):
        c=_cv(); f(c); out[name]=_rows(c)
    def eq(k):
        s=12/k; return [round(1+s*i) for i in range(1,k)]
    for k in (2,3,4):
        mk(f'tb{k}',lambda c,k=k:(_grid(c,1,2,13,14,[1+round(12*i/k) for i in range(1,k)],[2+round(12*i/k) for i in range(1,k)])))
    def rowa(c): _plus(c,8,2); _grid(c,1,6,14,14,(5,10),(10,)); _r(c,2,7,4,9,'l'); _r(c,6,7,9,9,'l'); _r(c,11,7,13,9,'l')
    def rowb(c): _grid(c,1,1,14,9,(5,10),(5,)); _r(c,2,6,4,8,'l'); _r(c,6,6,9,8,'l'); _r(c,11,6,13,8,'l'); _plus(c,8,13)
    def rowd(c): _grid(c,1,1,12,10,(5,9),(5,)); _x(c,10,10)
    def cola(c): _plus(c,2,8); _grid(c,6,1,14,14,(10,),(5,10)); _r(c,7,2,9,4,'l'); _r(c,7,6,9,9,'l'); _r(c,7,11,9,13,'l')
    def colb(c): _grid(c,1,1,9,14,(5,),(5,10)); _r(c,6,2,8,4,'l'); _r(c,6,6,8,9,'l'); _r(c,6,11,8,13,'l'); _plus(c,13,8)
    def cold(c): _grid(c,1,1,10,12,(5,),(4,8)); _x(c,10,10)
    def foot(c): _page(c); _r(c,5,3,10,3,'g'); _r(c,5,5,10,5,'g'); _r(c,5,7,10,7,'g'); _r(c,4,10,11,13,'b')
    def head1(c): _page(c,3,1,12,14); _r(c,4,2,11,5,'b'); _r(c,5,8,10,8,'g'); _r(c,5,10,10,10,'g'); _r(c,5,12,10,12,'g'); _r(c,13,10,15,15,'.'); _dig(c,13,10,'1','r')
    def foot1(c): _page(c,3,1,12,14); _r(c,5,3,10,3,'g'); _r(c,5,5,10,5,'g'); _r(c,4,10,11,13,'b'); _r(c,13,1,15,6,'.'); _dig(c,13,1,'1','r')
    def pgnum(c): _page(c); _r(c,5,3,10,3,'g'); _r(c,5,5,10,5,'g'); _dig(c,7,8,'1')
    def nofirst(c): _page(c,2,1,10,13); _r(c,3,2,9,4,'b'); _r(c,4,7,8,7,'g'); _r(c,4,9,8,9,'g'); _x(c,11,10)
    def fpage(c): _page(c); _dig(c,6,5,'#')
    def fdate(c):
        _box(c,1,2,14,14,'h'); _r(c,1,2,14,5,'b'); _r(c,4,1,4,3,'D'); _r(c,11,1,11,3,'D')
        for y in (8,11):
            for x in (4,7,10): _r(c,x,y,x+1,y+1,'h')
    def fcount(c): _dig(c,0,5,'1'); _dig(c,5,5,'2'); _dig(c,10,5,'3'); _r(c,0,12,12,12,'g')
    def refresh(c):
        for x,y in ((5,2),(6,2),(7,2),(8,2),(9,2),(4,3),(10,3),(3,4),(11,4),(2,5),(2,6),(2,7),(2,8),(2,9),(3,10),(4,11),(5,12),(6,12),(7,12),(8,12),(9,12),(10,11),(11,10),(12,9),(12,8),(13,8)): c[y][x]='B'
        _r(c,11,5,14,5,'B'); _r(c,12,6,13,6,'B'); _r(c,14,3,14,4,'B'); _r(c,12,5,14,5,'B'); c[3][12]='.'
        _r(c,9,5,14,5,'B'); _r(c,14,1,14,5,'B')
    def port(c): _page(c); _r(c,5,4,10,4,'g'); _r(c,5,6,10,6,'g'); _r(c,5,8,10,8,'g'); _r(c,5,10,10,10,'g')
    def land(c): _box(c,1,3,14,12,'h'); _r(c,3,5,12,5,'g'); _r(c,3,7,12,7,'g'); _r(c,3,9,12,9,'g')
    def marg(ins):
        def f(c): _page(c,2,1,13,14); _r(c,2+ins,2,2+ins,13,'B'); _r(c,13-ins,2,13-ins,13,'B'); _r(c,3,1+ins,12,1+ins,'B'); _r(c,3,14-ins,12,14-ins,'B')
        return f
    def delcmt(c): _box(c,1,1,12,9,'B'); _r(c,3,1+2,10,3,'g'); _r(c,3,6,8,6,'g'); _r(c,3,10,5,10,'B'); _r(c,3,11,4,11,'B'); _x(c,10,10)
    def pdfw(c):
        _r(c,3,1,9,14,'W'); _r(c,10,4,12,14,'W'); _r(c,10,2,10,3,'W'); _r(c,11,3,11,3,'W')
        _r(c,5,6,10,6,'b'); _r(c,5,8,10,8,'b'); _r(c,5,10,8,10,'b')
    def newp(c):
        _r(c,3,1,9,1,'W'); _r(c,3,1,3,14,'W'); _r(c,3,14,12,14,'W'); _r(c,12,5,12,14,'W'); _r(c,9,1,9,5,'W'); _r(c,9,5,12,5,'W'); c[2][10]='W'; c[3][11]='W'; c[4][12]='W'
    def prn(c):
        _r(c,4,1,11,1,'W'); _r(c,4,1,4,5,'W'); _r(c,11,1,11,5,'W'); _r(c,1,5,14,5,'W'); _r(c,1,5,1,11,'W'); _r(c,14,5,14,11,'W'); _r(c,1,11,3,11,'W'); _r(c,12,11,14,11,'W'); _r(c,4,9,11,9,'W'); _r(c,4,9,4,14,'W'); _r(c,11,9,11,14,'W'); _r(c,4,14,11,14,'W'); _r(c,6,11,9,11,'W'); c[7][12]='W'
    def minus(c): _r(c,4,7,11,8,'D')
    def plus(c): _r(c,4,7,11,8,'D'); _r(c,7,4,8,11,'D')
    for n,f in dict(rowa=rowa,rowb=rowb,rowd=rowd,cola=cola,colb=colb,cold=cold,foot=foot,head1=head1,foot1=foot1,pgnum=pgnum,nofirst=nofirst,fpage=fpage,fdate=fdate,fcount=fcount,refresh=refresh,port=port,land=land,mnorm=marg(3),mnar=marg(1),mwide=marg(5),delcmt=delcmt,pdfw=pdfw,newp=newp,prn=prn,minus=minus,plus=plus).items(): mk(n,f)
    return out
