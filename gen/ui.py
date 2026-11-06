"""Ribbon display list. Each draw item becomes outgoing weights of one token neuron.
All icons are original pixel art written below as text rows; each run becomes a rectangle."""
import rom
import t3_btn
from nn import X
from app_pal import B as _PB
BLUE=_PB[4];LG=_PB[3];BD=(209,209,209);WHT=(255,255,255);HVG=_PB[5];HVB=_PB[16];INK=(51,51,51);PRS=_PB[12]
TBLUE=3  # palette index of blue text
def twidth(s,si=9,b=0):
    "Width of a string at exact advances, the same metric the document text uses."
    px=round(rom.PTS[si]*96/72)
    return round(sum(rom.adv_em(0,b,0,ord(c))*px for c in s))
IDS={}     # (tab, alpha) to the center of the control, for the test coordinate map
ST=lambda si=9,b=0:si+16*b
ART={'K':(68,68,68),'B':(43,87,154),'L':(160,190,230),'W':(255,255,255),'G':(150,150,150),'g':(205,205,205),'Y':(238,190,70),'R':(200,60,50),'O':(190,130,60),'T':(50,140,100),'C':(0,120,190),'D':(90,90,90),'b':(24,90,189),'l':(198,219,244),'w':(250,250,250),'P':(190,130,60),'r':(209,52,56),'o':(214,140,60),'t':(40,150,110),'s':(150,195,235),'h':(120,120,120)}
ICON={
'paste':["....GGGGGG......","..OOGKKKKGOO....",".OOOGGGGGGOOO...",".OOOOOOOOOOOO...",".OOOWWWWWWWWWW..",".OOOWggggggggW..",".OOOWWWWWWWWWW..",".OOOWggggggggW..",".OOOWWWWWWWWWW..",".OOOWggggggggW..",".OOOWWWWWWWWWW..",".OOOWggggggggW..",".OOOWWWWWWWWWW..",".OOOWWWWWWWWWW..","....WWWWWWWWWW..","................"],
'cut':["................","...K.......K....","...K.......K....","....K.....K.....","....K.....K.....",".....K...K......",".....K...K......","......K.K.......",".......K........","......K.K.......","...BBB...BBB....","..B..B...B..B...","..B..B...B..B...","...BB.....BB....","................","................"],
'copy':["..GGGGGGGG......","..GWWWWWWG......","..GWggggWG......","..GWWWWBBBBBBBB.","..GWgggBWWWWWWB.","..GWWWWBWggggWB.","..GWgggBWWWWWWB.","..GWWWWBWggggWB.","..GWgggBWWWWWWB.","..GWWWWBWggggWB.","..GGGGGBWWWWWWB.",".......BWggggWB.",".......BWWWWWWB.",".......BBBBBBBB.","................","................"],
'undo':["................","................",".....W..........","....WW..........","...WWWWWWWW.....","..WWWWWWWWWWW...","...WWW.....WWW..","....WW......WW..",".....W......WW..","............WW..","...........WWW..",".........WWWW...","........WWW.....","................","................","................"],
'redo':["................","................","..........W.....","..........WW....",".....WWWWWWWW...","...WWWWWWWWWWW..","..WWW.....WWW...","..WW......WW....","..WW......W.....","..WW............","..WWW...........","...WWWW.........",".....WWW........","................","................","................"],
'save':["................","..WWWWWWWWWWW...","..WLLWWWWWLLWW..","..WLLWWWWWLLLW..","..WLLWWWWWLLLW..","..WLLLLLLLLLLW..","..WLLLLLLLLLLW..","..WLLLLLLLLLLW..","..WLWWWWWWWWLW..","..WLWWWWWWWWLW..","..WLWWWWWWWWLW..","..WLWWWWWWWWLW..","..WWWWWWWWWWWW..","................","................","................"],
'open':["................","................","..WWWW..........",".WLLLLW.........",".WLLLLLWWWWWW...",".WLLLLLLLLLLW...",".WLWWWWWWWWWWWW.",".WLW..........W.",".WLW.........W..",".WW.........WW..",".W..........W...",".WWWWWWWWWWWW...","................","................","................","................"],
'pdf':["...WWWWWWW......","...WWWWWWWW.....","...WWWWWWWWW....","...WWWWWWWWWW...","...WWWWWWWWWW...","...WWWWWWWWWW...","...WWWWWWWWWW...",".RRRRRRRRRRRRR..",".RWWRWWRRWWWRR..",".RWRWRWRRWRRRR..",".RWWRRWRRWWRRR..",".RWRRRWWRWRRRR..",".RRRRRRRRRRRRR..","...WWWWWWWWWW...","...WWWWWWWWWW...","................"],
'bul':["................","................",".KK..KKKKKKKKKK.",".KK..KKKKKKKKKK.","................","................","................",".BB..KKKKKKKKKK.",".BB..KKKKKKKKKK.","................","................","................",".KK..KKKKKKKKKK.",".KK..KKKKKKKKKK.","................","................"],
'num':["................",".BB.............","..B..KKKKKKKKKK.","..B..KKKKKKKKKK.",".BBB............","................",".BB.............","...B.KKKKKKKKKK.","..B..KKKKKKKKKK.",".BBB............","................",".BB.............",".BB..KKKKKKKKKK.","...B.KKKKKKKKKK.",".BB.............","................"],
'find':["................",".....BBBBB......","....B.....B.....","...B.......B....","...B.......B....","...B.......B....","...B.......B....","....B.....B.....",".....BBBBBG.....","..........GG....","...........GG...","............GG..",".............GG.","................","................","................"],
'repl':["................","..BBB...........",".B...B...KKK....",".BBBBB..K...K...",".B...B..K...K...",".B...B..K...K...","...........GG...","............GG..","..GGGGGGGGGGGGG.","............GG..","...........GG...","..KKKKK.........","..K....K........","..KKKKK.........","..K....K........","..KKKKK........."],
'table':["................",".BBBBBBBBBBBBBB.",".BLLLLBLLLLBLLB.",".BLLLLBLLLLBLLB.",".BBBBBBBBBBBBBB.",".BWWWWBWWWWBWWB.",".BWWWWBWWWWBWWB.",".BBBBBBBBBBBBBB.",".BWWWWBWWWWBWWB.",".BWWWWBWWWWBWWB.",".BBBBBBBBBBBBBB.",".BWWWWBWWWWBWWB.",".BWWWWBWWWWBWWB.",".BBBBBBBBBBBBBB.","................","................"],
'head':["..GGGGGGGGGGGG..","..GBBBBBBBBBBG..","..GBBBBBBBBBBG..","..GWWWWWWWWWWG..","..GWggggggggWG..","..GWWWWWWWWWWG..","..GWggggggggWG..","..GWWWWWWWWWWG..","..GWggggggggWG..","..GWWWWWWWWWWG..","..GWggggggggWG..","..GWWWWWWWWWWG..","..GWWWWWWWWWWG..","..GGGGGGGGGGGG..","................","................"],
'pic':["................",".GGGGGGGGGGGGGG.",".GLLLLLLLLLLLLG.",".GLLLLLLLYYLLLG.",".GLLLLLLLYYLLLG.",".GLLLLLLLLLLLLG.",".GLLLTLLLLLLLLG.",".GLLTTTLLLTLLLG.",".GLTTTTTLTTTLLG.",".GTTTTTTTTTTTTG.",".GTTTTTTTTTTTTG.",".GGGGGGGGGGGGGG.","................","................","................","................"],
'col1':["................","..KKKKKKKKKKKK..","................","..KKKKKKKKKKKK..","................","..KKKKKKKKKKKK..","................","..KKKKKKKKKKKK..","................","..KKKKKKKKKKKK..","................","..KKKKKKKKKKKK..","................","................","................","................"],
'col2':["................",".KKKKKK..KKKKKK.","................",".KKKKKK..KKKKKK.","................",".KKKKKK..KKKKKK.","................",".KKKKKK..KKKKKK.","................",".KKKKKK..KKKKKK.","................",".KKKKKK..KKKKKK.","................","................","................","................"],
'brk':["..GWWWWWWWWWWG..","..GWggggggggWG..","..GWWWWWWWWWWG..","..GGGGGGGGGGGG..","................",".B.B.B.B.B.B.B..","................","..GGGGGGGGGGGG..","..GWWWWWWWWWWG..","..GWggggggggWG..","..GWWWWWWWWWWG..","..GWggggggggWG..","..GWWWWWWWWWWG..","..GWWWWWWWWWWG..","..GGGGGGGGGGGG..","................"],
'marg':["GGGGGGGGGGGGGGGG","GWWWWWWWWWWWWWWG","GWWBWWWWWWWWBWWG","GWWBWggggggWBWWG","GWWBWWWWWWWWBWWG","GWWBWggggggWBWWG","GWWBWWWWWWWWBWWG","GWWBWggggggWBWWG","GWWBWWWWWWWWBWWG","GWWBWggggggWBWWG","GWWBWWWWWWWWBWWG","GWWBWggggggWBWWG","GWWBWWWWWWWWBWWG","GWWWWWWWWWWWWWWG","GGGGGGGGGGGGGGGG","................"],
'ind-':["................","..KKKKKKKKKKKK..","................","......KKKKKKKK..","...B............","..BB..KKKKKKKK..",".BBBBBB.........","..BB..KKKKKKKK..","...B............","......KKKKKKKK..","................","..KKKKKKKKKKKK..","................","................","................","................"],
'ind+':["................","..KKKKKKKKKKKK..","................","......KKKKKKKK..","..B.............","..BB..KKKKKKKK..",".BBBBBB.........","..BB..KKKKKKKK..","..B.............","......KKKKKKKK..","................","..KKKKKKKKKKKK..","................","................","................","................"],
'sp-':["................","......KKKKKKKK..","................","......KKKKKKKK..","................","...B............","..BBB...........",".BBBBB..........","...B............","...B............","......KKKKKKKK..","................","......KKKKKKKK..","................","................","................"],
'sp+':["................","......KKKKKKKK..","................","......KKKKKKKK..","................","...B............","...B............",".BBBBB..........","..BBB...........","...B............","......KKKKKKKK..","................","......KKKKKKKK..","................","................","................"],
'lsp':["...B............","..BBB...KKKKKKK.",".BBBBB..........","...B............","...B....KKKKKKK.","...B............","...B............","...B....KKKKKKK.","...B............","...B............",".BBBBB..KKKKKKK.","..BBB...........","...B............","........KKKKKKK.","................","................"],
'ruler':["................","................","................","YYYYYYYYYYYYYYYY","YKYYKYYKYYKYYKYY","YKYYKYYKYYKYYKYY","YKYYYYYKYYYYYKYY","YYYYYYYYYYYYYYYY","YYYYYYYYYYYYYYYY","................","................","................","................","................","................","................"],
'marks':["................","....BBBBBBBB....","...BBBBBB.B.....","..BBBBBBB.B.....","..BBBBBBB.B.....","...BBBBBB.B.....","....BBBBB.B.....",".......BB.B.....",".......BB.B.....",".......BB.B.....",".......BB.B.....",".......BB.B.....",".......BB.B.....","................","................","................"],
'toc':["................",".BBBBB..........",".BBBBB....KKKK..","................","...KKKKKK.G.G.K.","................","...KKKKKK.G.G.K.","................",".BBBBB..........",".BBBBB....KKKK..","................","...KKKKKK.G.G.K.","................","...KKKKKK.G.G.K.","................","................"],
'fn':["................","..KKKKKKKKKK.B..","............BB..","..KKKKKKKKKK.B..","................","..KKKKKKKKKK....","................","................","................",".GGGGGG.........","................",".B.KKKKKKKKKK...",".B..............",".B.KKKKKKKK.....","................","................"],
'cmt':["................",".BBBBBBBBBBBBBB.",".BWWWWWWWWWWWWB.",".BWggggggggggWB.",".BWWWWWWWWWWWWB.",".BWggggggggggWB.",".BWWWWWWWWWWWWB.",".BWggggggWWWWWB.",".BWWWWWWWWWWWWB.",".BBBBBBWWBBBBBB.",".......WWB......",".......WB.......",".......B........","................","................","................"],
'chev':["................","................","................","................","................","..KKKKKKK.......","...KKKKK........","....KKK.........",".....K..........","................","................","................","................","................","................","................"],
}
def _big():
    "32 by 32 icons, drawn with flat shapes on a character grid. Original art."
    from PIL import Image,ImageDraw
    P=" KDGghbBlLwWProtsYC"
    out={}
    def mk(name,f):
        im=Image.new('P',(32,32),0); im.putpalette([v_ for k_ in range(256) for v_ in (k_,k_,k_)]); d=ImageDraw.Draw(im)
        def R(x0,y0,x1,y1,c,o=None): d.rectangle((x0,y0,x1,y1),fill=P.index(c),outline=P.index(o) if o else None)
        def Ln(x0,y0,x1,y1,c,w=1): d.line((x0,y0,x1,y1),fill=P.index(c),width=w)
        f(R,Ln,d,P)
        out[name]=[''.join('.' if im.getpixel((x,y))==0 else P[im.getpixel((x,y))] for x in range(32)) for y in range(32)]
    def page(R,x0=7,y0=3,x1=24,y1=28): R(x0,y0,x1,y1,'w','h')
    def lines(R,x0,x1,ys,c='g'):
        for y in ys: R(x0,y,x1,y,c)
    def paste(R,L,d,P):
        R(5,5,21,27,'P','D'); R(10,2,16,7,'g','D'); R(13,11,27,29,'w','h'); lines(R,16,24,(15,18,21,24),'h')
    def table(R,L,d,P):
        R(4,6,27,25,'w','b'); R(5,7,26,10,'l')
        for x in (11,19): L(x,6,x,25,'b')
        for y in (11,18): L(4,y,27,y,'b')
    def pic(R,L,d,P):
        R(3,6,28,25,'s','h'); d.polygon([(4,24),(12,13),(18,20),(22,16),(27,24)],fill=P.index('t')); R(21,9,24,12,'Y')
    def head_(R,L,d,P):
        page(R); R(8,4,23,9,'l'); lines(R,10,21,(13,16,19,22))
    def marg(R,L,d,P):
        page(R,5,3,26,28); L(10,4,10,27,'b'); L(21,4,21,27,'b'); L(6,8,25,8,'b'); L(6,23,25,23,'b'); lines(R,12,19,(12,15,18))
    def brk(R,L,d,P):
        R(7,2,24,11,'w','h'); lines(R,10,21,(5,8)); 
        for x in range(4,28,4): R(x,15,x+1,15,'b')
        R(7,19,24,29,'w','h'); lines(R,10,21,(23,26))
    def toc(R,L,d,P):
        page(R,5,3,26,28); R(8,7,16,8,'b'); lines(R,10,17,(12,17,22),'h'); lines(R,21,23,(12,17,22),'h')
        for y in (12,17,22):
            for x in (18,20): R(x,y,x,y,'g')
    def fn(R,L,d,P):
        page(R); lines(R,10,21,(7,10,13),'g'); R(19,6,21,8,'b'); L(10,20,16,20,'h'); lines(R,10,21,(23,26),'b')
    def cmt(R,L,d,P):
        R(4,5,27,21,'w','b'); d.polygon([(10,22),(10,28),(16,22)],fill=P.index('w'),outline=P.index('b')); L(11,21,15,21,'w'); lines(R,8,23,(10,13,16),'h')
    def spell(R,L,d,P):
        L(7,5,3,19,'b',2); L(7,5,11,19,'b',2); L(5,13,9,13,'b',2); R(14,5,15,19,'b'); R(14,5,20,6,'b'); R(14,11,20,12,'b'); R(14,18,20,19,'b'); R(21,6,22,11,'b'); R(21,13,22,18,'b'); L(9,25,15,29,'t',2); L(15,29,26,20,'t',2)
    def track(R,L,d,P):
        page(R,5,3,22,28); lines(R,8,19,(8,12,16,20),'g'); L(16,25,27,12,'r',2); L(14,27,16,25,'D',2)
    def eqn(R,L,d,P):
        L(24,6,7,6,'b',2); L(7,6,16,16,'b',2); L(16,16,7,26,'b',2); L(7,26,24,26,'b',2)
    def merge(R,L,d,P):
        R(4,8,27,24,'w','b'); L(4,8,16,17,'b'); L(27,8,16,17,'b')
    def sty(R,L,d,P):
        R(5,5,26,26,'w','h'); L(10,21,15,9,'b',2); L(15,9,20,21,'b',2); L(12,17,18,17,'b')
    def lsp(R,L,d,P):
        L(7,5,7,26,'b'); d.polygon([(7,3),(3,9),(11,9)],fill=P.index('b')); d.polygon([(7,28),(3,22),(11,22)],fill=P.index('b')); lines(R,14,27,(7,13,19,25),'D')
    def col2(R,L,d,P):
        page(R,5,3,26,28); lines(R,8,14,(7,10,13,16,19,22),'h'); lines(R,17,23,(7,10,13,16,19,22),'h')
    for n,f in dict(paste=paste,table=table,pic=pic,head=head_,marg=marg,brk=brk,toc=toc,fn=fn,cmt=cmt,spell=spell,track=track,eqn=eqn,merge=merge,sty=sty,lsp=lsp,col2=col2).items(): mk('B'+n,f)
    return out
ICON.update(_big())
# a small style preview chevron and small icons for the Home rows
ICON['ind-'] =ICON['ind-']; ICON['app']=["................",".wwwwwwwwwwwwww.",".wbbbbbbbbbbbbw.",".wbbwwwwwwwbbbw.",".wbwwbbbbbwwbbw.",".wbwwbbbbbbbbbw.",".wbbwwwwwwbbbbw.",".wbbbbbwwwwwbbw.",".wbbbbbbbbwwbbw.",".wbwwbbbbbwwbbw.",".wbbwwwwwwwbbbw.",".wbbbbbbbbbbbbw.",".wwwwwwwwwwwwww.","................","................","................"]
ICON['srch']=["................","......WWWWW.....",".....W.....W....","....W.......W...","....W.......W...","....W.......W...",".....W.....W....","......WWWWW.....","..........WW....","...........WW...","............WW..",".............WW.","................","................","................","................"]
ICON['back']=["................","................","......W.........",".....WW.........","....WW..........","...WW...........","..WWWWWWWWWWWW..","...WW...........","....WW..........",".....WW.........","......W.........","................","................","................","................","................"]
ICON['proof']=["................","..DDDDDDDDD.....","..DWWWWWWWDD....","..DWggggWWWDD...","..DWWWWWWWWWD...","..DWgggggWWWD...","..DWWWWWWWWWD...","..DWgggWWWWtD...","..DWWWWWWWttD...","..DWWWtWWttWD...","..DWWWttttWWD...","..DWWWWttWWWD...","..DDDDDDDDDDD...","................","................","................"]
ICON['vread']=["................","................",".DDDDDD.DDDDDD..",".DWWWWD.DWWWWD..",".DWggWD.DWggWD..",".DWWWWD.DWWWWD..",".DWggWD.DWggWD..",".DWWWWD.DWWWWD..",".DWggWD.DWggWD..",".DWWWWD.DWWWWD..",".DDDDDD.DDDDDD..","................","................","................","................","................"]
ICON['vprint']=["................","....DDDDDDDD....","....DWWWWWWD....","....DWggggWD....","....DWWWWWWD....","....DWggggWD....","....DWWWWWWD....","....DWggggWD....","....DWWWWWWD....","....DWggggWD....","....DWWWWWWD....","....DDDDDDDD....","................","................","................","................"]
ICON['vweb']=["................","................","..DDDDDDDDDDDD..","..DbbbbbbbbbbD..","..DWWWWWWWWWWD..","..DWggggggggWD..","..DWWWWWWWWWWD..","..DWggggggggWD..","..DWWWWWWWWWWD..","..DDDDDDDDDDDD..","................","................","................","................","................","................"]
ICON['tick']=["................","................","............t...","...........tt...","..........tt....",".........tt.....","..t.....tt......","..tt...tt.......","...tt.tt........","....ttt.........",".....t..........","................","................","................","................","................"]
ICON['cross']=["................","................","...r.......r....","..rrr.....rrr...","...rrr...rrr....","....rrr.rrr.....",".....rrrrr......","......rrr.......",".....rrrrr......","....rrr.rrr.....","...rrr...rrr....","..rrr.....rrr...","...r.......r....","................","................","................"]
class L:
    def __init__(s): s.i=[];s.tab=None
    def r(s,x,y,w,h,c,a=0,hc=None,key=None):
        s.i.append(('r',x,y,w,h,c,a,hc,key if key is not None else a))
        if a>=200 and s.tab is not None: IDS.setdefault(f'{s.tab}:{a}',(x+w//2,y+h//2))
    def k(s,cond,x,y,w,h,c,a=0): s.i.append(('k',cond,x,y,w,h,c,a))
    def t(s,x,y,txt,st=9,f=0,b=3,hv=False):
        "Whole pixel pens rounded from exact advances, so a label matches document spacing."
        si=st&15;bo=(st>>4)&1;fi=(st>>7)&1;px=round(rom.PTS[si]*96/72); xf=float(x)
        for ch in txt:
            s.i.append(('g',ord(ch),st,round(xf),y,f,b,hv)); xf+=rom.adv_em(fi,bo,0,ord(ch))*px
        return round(xf)
    def art(s,x,y,name,a=0,sc=1):
        """Pixel art: horizontal runs, merged with an identical run on the row above."""
        rows=ICON[name]; live={}
        out=[]
        for j,row in enumerate(rows+['.'*len(rows[0])]):
            runs={};i=0
            while i<len(row):
                c=row[i]
                if c=='.': i+=1; continue
                k=i
                while k<len(row) and row[k]==c: k+=1
                runs[(i,k,c)]=1; i=k
            for q in list(live):
                if q not in runs:
                    i_,k_,c_=q; y0=live.pop(q)
                    out.append((x+i_*sc,y+y0*sc,(k_-i_)*sc,(j-y0)*sc,ART[c_]))
            for q in runs:
                if q not in live: live[q]=j
        for o in out: s.r(o[0],o[1],o[2],o[3],o[4],a)
    def btn(s,x,y,w,h,label,id_,st=9,f=0,b=3,bgc=LG,hc=HVG):
        s.r(x,y,w,h,bgc,200+id_,hc)
        tw=twidth(label,st&15,(st>>4)&1); s.t(x+(w-tw)//2,y+(h-rom.metrics(st&15)[1])//2+1,label,st,f,b,True)
    def ibtn(s,x,y,w,h,label,id_,icon,b=3,bgc=LG):
        "Small icon on the left, label on the right."
        s.r(x,y,w,h,bgc,200+id_,HVG); s.art(x+3,y+(h-16)//2,icon,200+id_)
        s.t(x+22,y+(h-rom.metrics(9)[1])//2+1,label,9,0,b,True)
    def ic(s,x,y,w,h,id_,icon):
        "Icon only."
        s.r(x,y,w,h,LG,200+id_,HVG); s.art(x+(w-16)//2,y+(h-16)//2,icon,200+id_)
    def big(s,x,y,w,h,label,id_,icon,chev=False):
        "Large icon on top, label below."
        s.r(x,y,w,h,LG,200+id_,HVG); s.art(x+(w-32)//2,y+4,'B'+icon,200+id_)
        tw=twidth(label); lx=x+(w-tw)//2-(5 if chev else 0); e=s.t(lx,y+h-20,label,9,0,3,True)
        if chev: s.art(e-3,y+h-19,'chev',200+id_)
    def qbtn(s,x,y,w,h,icon,id_):
        s.r(x,y,w,h,BLUE,200+id_,HVB); s.art(x+(w-16)//2,y+(h-16)//2,icon,200+id_)
ROW=(64,86,108)
TABN=['File','Home','Insert','Layout','References','Review','View']
def common():
    u=L(); u.tab='c'; u.r(0,0,1280,32,BLUE); u.r(0,32,1280,28,LG)
    u.art(8,8,'app')
    u.qbtn(32,6,26,20,'save',47); u.qbtn(60,6,26,20,'undo',27); u.qbtn(88,6,26,20,'redo',28); u.qbtn(116,6,26,20,'open',48); u.qbtn(144,6,26,20,'pdf',53)
    u.t(250,9,'Document1 - SynapseWrite',9,2,4)
    # search box opens the find bar
    u.r(480,5,360,22,(68,119,187),225,(85,136,204)); u.art(486,8,'srch',225); u.t(508,9,'Search',9,2,16)
    # status bar: the left part is live, the right part is static
    u.r(0,776,1280,1,BD); u.r(640,777,640,23,LG)
    x=1000
    for i,ic_ in enumerate(('vread','vprint','vweb')):
        if i==1: u.r(x+i*26,778,24,21,(221,221,221))
        u.art(x+i*26+4,780,ic_)
    u.r(1110,788,110,1,(150,150,150)); u.r(1164,782,3,13,(90,90,90))
    u.r(1092,788,10,1,(90,90,90)); u.r(1228,788,9,1,(90,90,90)); u.r(1232,784,1,9,(90,90,90))
    u.t(1244,781,'100%',9,1,3)
    return u,['Home','Insert','Layout','References','Review','View']
def tabbar(u,names,sel):
    x=8; w=twidth('File')+24
    u.r(x,33,w,27,LG,200+26,HVG); u.t(x+12,39,'File',9,0,3,True); x+=w
    for i,nm in enumerate(names):
        w=twidth(nm)+24
        if i==sel:
            u.r(x,33,w,27,LG,200+29+i); e=u.t(x+12,39,nm,9+16,TBLUE,3); u.r(x+12,56,e-x-12,3,BLUE,200+29+i)
        else:
            u.r(x,33,w,27,LG,200+29+i,HVG); u.t(x+12,39,nm,9,0,3,True)
        x+=w
    u.r(0,60,1280,90,LG); u.r(0,149,1280,1,BD)
    u.r(0,150,1280,24,GRAYW)
GRAYW=(230,230,230)
def ruler():
    "Inch ticks and numbers; the network redraws them when the markers move."
    u=L()
    for k in range(0,9):
        xx=319+k*96
        if xx<=943:
            if k==0 or k==7: pass
            else: u.r(xx-16,161,1,3,(138,136,134)); u.r(xx-48,159,1,7,(138,136,134)); u.r(xx-80,161,1,3,(138,136,134))
            if 0<k<7: u.i.append(('g',48+k,11,xx-3,155,1,0,False))
    return u
def group_label(u,x,w,t):
    u.t(x+(w-twidth(t))//2,131,t,9,1,3); u.r(x+w+4,64,1,80,BD)
def effect(u,x,id_,ch,sc=None,bar=None):
    u.r(x,90,26,24,LG,200+id_,HVG); e=u.t(x+8,94,ch,9,0,3,True)
    if sc: u.t(e,90 if sc=='^' else 99,'2',11,0,3,True)
    if bar: u.r(x+6,101,12,1,(0,0,0),200+id_)
HOME={'font':(112,64,112),'size':(242,64,34),'biu':(112,138,164),'fill':0}
def home(u):
    u.big(6,64,46,62,'Paste',36,'paste'); u.ibtn(54,64,52,21,'Cut',38,'cut'); u.ibtn(54,86,52,21,'Copy',37,'copy'); group_label(u,6,100,'Clipboard')
    x=112
    u.r(x,64,112,22,(170,170,170),206); u.btn(x+112,64,16,22,'',42); u.art(x+112,67,'chev',242)
    u.r(242,64,34,22,(170,170,170),243); u.btn(276,64,14,22,'',40); u.art(275,67,'chev',240)
    u.btn(292,64,24,22,'A+',4); u.btn(316,64,24,22,'A-',5)
    effect(u,190,10,'S',bar=True); effect(u,216,12,'x','_'); effect(u,242,11,'x','^')
    u.r(270,90,24,24,LG,207,HVG); u.t(277,92,'A',9,0,3,True); u.r(274,107,16,3,(187,0,0),207)
    u.btn(294,90,12,24,'',41); u.art(292,94,'chev',241)
    u.r(306,90,24,24,LG,244,HVG); u.t(311,92,'ab',9,0,3,True); u.r(310,107,16,3,(255,255,0),244)
    u.btn(330,90,12,24,'',45); u.art(328,94,'chev',245)
    group_label(u,112,230,'Font')
    x=350
    u.ic(x,64,28,24,19,'bul'); u.ic(x+30,64,28,24,20,'num'); u.ic(x+62,64,28,24,13,'ind-'); u.ic(x+92,64,28,24,14,'ind+')
    for i in range(4):
        xx=x+i*28; u.r(xx,90,26,24,LG,200+15+i,HVG)
        for ln,wd in enumerate((16,10,16,10) if i<3 else (16,16,16,16)):
            off={0:4,1:(26-wd)//2,2:22-wd,3:5}[i]; u.r(xx+off,94+ln*4,wd,2,(70,70,70),200+15+i)
    u.ic(x+114,90,28,24,46,'lsp')
    group_label(u,x,144,'Paragraph')
    x=504
    TL=(('Normal',9-9+0,0,0),('Heading 1',2,TBLUE,2),('Heading 2',1,TBLUE,3),('Heading 3',0+16,TBLUE,4),('Title',3,0,1),('Quote',0+32,1,5))
    IDT={0:21,1:22,2:23,3:24,4:49,5:51}
    for i,(nm,st,f,sid) in enumerate(TL):
        tx=x+i*84; id_=IDT[sid]
        u.r(tx,64,82,62,(218,218,218),200+id_); u.r(tx+1,65,80,60,WHT,200+id_,HVG)
        px=round(rom.PTS[st&15]*96/72); pv='AaBbCc' if px<=16 else 'AaBb'; 
        u.t(tx+(82-_tw(pv,st))//2,66+(36-rom.metrics(st&15)[1])//2,pv,st,f,0,True)
        u.t(tx+(82-twidth(nm))//2,106,nm,9,0,0,True)
    u.big(x+6*84+2,64,48,62,'Update',52,'sty')
    group_label(u,x,6*84+50,'Styles')
    x=1066
    u.ibtn(x,64,80,24,'Find',8,'find'); u.ibtn(x,90,80,24,'Replace',9,'repl'); group_label(u,x,80,'Editing')
def _tw(s,st):
    si=st&15;bo=(st>>4)&1;it=(st>>5)&1;px=round(rom.PTS[si]*96/72)
    return round(sum(rom.adv_em(0,bo,it,ord(c))*px for c in s))
GRIDC=22
def insert(u):
    for i,(lb,id_) in enumerate((('2 x 2',40),('3 x 3',41),('4 x 4',42))): u.ibtn(6,ROW[i],70,21,lb,id_,'table')
    group_label(u,6,276,'Tables'); u.big(314,64,54,62,'Picture',52,'pic'); group_label(u,314,54,'Pictures')
    u.ibtn(380,64,84,21,'Header',46,'head'); group_label(u,380,186,'Header and Footer')
    x=576
    u.btn(x,64,84,21,'Page Field',3); u.btn(x,86,84,21,'Date',4); u.btn(x+86,64,84,21,'Word Count',5); u.btn(x+86,86,84,21,'Update All',1); group_label(u,x,170,'Fields')
    u.big(756,64,60,62,'Equation',2,'eqn'); group_label(u,756,60,'Math')
def layout(u):
    u.big(6,64,52,62,'Margins',6,'marg',True); group_label(u,6,196,'Page Setup')
    u.ibtn(212,64,70,21,'One',43,'col1'); u.ibtn(212,86,70,21,'Two',44,'col2'); group_label(u,212,70,'Columns')
    u.big(290,64,56,62,'Page Break',1,'brk'); u.big(348,64,62,62,'Section',15,'brk'); group_label(u,290,120,'Breaks')
    x=420
    for r,(nm,a,b) in enumerate((('Left',16,17),('First',18,19))):
        u.t(x+2,ROW[r]+3,nm,9,0,3); u.btn(x+44,ROW[r],22,21,'-',a); u.btn(x+68,ROW[r],22,21,'+',b)
    for r,(nm,a,b) in enumerate((('Before',20,21),('After',22,23))):
        u.t(x+100,ROW[r]+3,nm,9,0,3); u.btn(x+146,ROW[r],22,21,'-',a); u.btn(x+170,ROW[r],22,21,'+',b)
    u.ibtn(x,ROW[2],90,21,'Indent -',2,'ind-'); u.ibtn(x+100,ROW[2],90,21,'Indent +',3,'ind+')
    u.ibtn(x+200,ROW[0],84,21,'Space -',4,'sp-'); u.ibtn(x+200,ROW[1],84,21,'Space +',5,'sp+')
    u.big(x+288,64,46,62,'Line',7,'lsp',True)
    for i,l in enumerate(('1.0','1.15','1.5','2.0','2.5','3.0')): u.btn(x+336+(i%2)*38,ROW[i//2],36,21,l,(24,36,37,38,39,40)[i])
    group_label(u,x,410,'Paragraph')
def refs(u):
    u.big(6,64,66,62,'Contents',45,'toc'); group_label(u,6,162,'Table of Contents')
    u.big(176,64,62,62,'Footnote',51,'fn'); group_label(u,176,62,'Footnotes'); u.big(246,64,66,62,'Mail Merge',1,'merge'); group_label(u,246,66,'Mailings')
def review(u):
    u.big(6,64,54,62,'Spelling',2,'spell'); group_label(u,6,54,'Proofing')
    u.big(68,64,50,62,'Comment',49,'cmt'); group_label(u,68,156,'Comments')
    u.big(232,64,56,62,'Track',3,'track'); u.ibtn(290,64,76,21,'Accept',4,'tick'); u.ibtn(290,86,76,21,'Reject',1,'cross'); group_label(u,232,134,'Tracking')
def view(u):
    for i,(nm,ic) in enumerate((('Ruler','ruler'),('Formatting Marks','marks'))):
        u.r(8,64+i*26,150,24,LG,200+1+i,HVG); u.r(12,69+i*26,14,14,(120,120,120),200+1+i); u.r(13,70+i*26,12,12,WHT,200+1+i)
        u.art(30,68+i*26,ic,200+1+i); u.t(50,68+i*26,nm,9,0,3,True)
    group_label(u,8,150,'Show')
def backstage():
    u=L(); u.tab='bs'
    u.r(0,0,1280,800,WHT); u.r(0,0,180,800,BLUE)
    u.qbtn(10,12,40,32,'back',1)
    for i,(nm,id_) in enumerate((('New',2),('Open',3),('Save',4),('Print',5))):
        y=70+i*44; u.r(0,y,180,44,BLUE,200+id_,HVB); u.t(24,y+14,nm,9+16,2,4)
    u.t(230,44,'New',5,0,0)
    u.r(230,100,132,172,(200,198,196),206,(24,90,189)); u.r(232,102,128,168,WHT,206)
    u.t(236,282,'Blank document',9,0,0)
    u.t(230,330,'File commands save and open .docx files. Print writes a PDF.',9,1,0)
    return u
def emit(net,fsm,rA,bus,YB,items,seq0_state,hv_reg,hb,bg,prs=None):
    """Writes a token chain for the items and returns the last token."""
    g_en,g_ch,g_st,g_x,g_y,g_draw,fg=bus
    tok=fsm.S(seq0_state); fsm.states[seq0_state][1].append((tok,None))
    seq=[net.reg() for _ in range(len(items)+1)]
    net.rec(seq[0],tok)
    for i,it in enumerate(items):
        t=seq[i]
        if it[0]=='r':
            _,x,y,w,h,c,a,hc,key=it; rA.lin(t,x,y,w,h,c,a)
            if hc is not None:
                on=net.eq(hv_reg,key,t)
                for j in range(3):
                    if hc[j]!=c[j]: rA.b[5+j].lin(on*(hc[j]-c[j]))
                if prs is not None and hc is HVG:
                    pr_=net.and_(on,prs)
                    for j in range(3): rA.b[5+j].lin(pr_*(PRS[j]-hc[j]))
                fsm.set(hb,t,on)
        elif it[0]=='k':
            _,cond,x,y,w,h,c,a=it; rA.lin(net.and_(t,cond),x,y,w,h,c,a)
        else:
            _,ch,st,x,y,f,b,hv=it
            g_en.lin(t);g_draw.lin(t);g_ch.lin(t*ch);g_st.lin(t*st);g_x.lin(t*x);g_y.lin(t*(y+YB));fg[f].lin(t)
            if hv:
                c=net.and_(t,hb); bg[b].lin(t-c); bg[5].lin(c)
            else: bg[b].lin(t)
        net.rec(seq[i+1],t)
    return seq[len(items)]
def build(net,fsm,rA,g_en,g_ch,g_st,g_x,g_y,g_draw,fg,bg,YB,tab,S,hov,hb,hvo,bs,prs):
    bus=(g_en,g_ch,g_st,g_x,g_y,g_draw,fg)
    en=S('UI'); hot=net.decode(tab,6,en)
    u0,names=common()
    fsm.on('UI',(bs,'BS_UI',None),*[(hot[i],f'UI_{i}',None) for i in range(6)],(None,'RD0',None))
    last=emit(net,fsm,rA,bus,YB,backstage().i,'BS_UI',hov,hb,bg); net.rec(fsm.state('T1_END'),last)
    for k in range(6):
        u=L(); u.tab=k; u.i=list(u0.i); tabbar(u,names,k)
        (home,insert,layout,refs,review,view)[k](u)
        for bt in t3_btn.BTNS:
            if bt[0]==k:
                tb_,id_,x_,y_,w_,h_,lb_,st_,c_=bt
                u.r(x_,y_,w_,h_,LG,200+id_,HVG)
                if c_ is not None: u.r(x_+2,y_+2,w_-4,h_-4,(170,170,170),200+id_); u.r(x_+3,y_+3,w_-6,h_-6,c_,200+id_)
                elif lb_: u.t(x_+(w_-twidth(lb_))//2,y_+(h_-rom.metrics(9)[1])//2+1,lb_,9,0,3,True)
        last=emit(net,fsm,rA,bus,YB,u.i,f'UI_{k}',hov,hb,bg,prs)
        c=net.and_(last,hvo)   # a hover redraw skips the document walk
        net.rec(fsm.state('RD0'),last-c); net.rec(fsm.state('TB0'),c)

    import json
    json.dump(IDS,open('../build/ui_ids.json','w'))
