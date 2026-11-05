"""Ribbon display list. Each draw item becomes outgoing weights of one token neuron.
All icons are original pixel art written below as text rows; each run becomes a rectangle."""
import rom
from nn import X
BLUE=(24,90,189);LG=(243,242,241);BD=(210,208,206);WHT=(255,255,255);HVG=(225,225,225);HVB=(58,118,208);INK=(50,49,48)
TBLUE=3  # palette index of blue text
def twidth(s,si=9,b=0):
    return sum(rom.glyph(0,b,0,si,ord(c))[0] for c in s)
ST=lambda si=9,b=0:si+16*b
ART={'K':(68,68,68),'B':(43,87,154),'L':(160,190,230),'W':(255,255,255),'G':(150,150,150),'g':(205,205,205),'Y':(238,190,70),'R':(200,60,50),'O':(190,130,60),'T':(50,140,100),'C':(0,120,190)}
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
class L:
    def __init__(s): s.i=[]
    def r(s,x,y,w,h,c,a=0,hc=None,key=None): s.i.append(('r',x,y,w,h,c,a,hc,key if key is not None else a))
    def k(s,cond,x,y,w,h,c,a=0): s.i.append(('k',cond,x,y,w,h,c,a))
    def t(s,x,y,txt,st=9,f=0,b=3,hv=False):
        si=st&15;bo=(st>>4)&1;fi=(st>>7)&1
        for ch in txt:
            s.i.append(('g',ord(ch),st,x,y,f,b,hv)); x+=rom.glyph(fi,bo,0,si,ord(ch))[0]
        return x
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
        tw=twidth(label,st&15,(st>>4)&1); s.t(x+(w-tw)//2,y+(h-rom.metrics(st&15)[1])//2,label,st,f,b,True)
    def ibtn(s,x,y,w,h,label,id_,icon,b=3,bgc=LG):
        "Small icon on the left, label on the right."
        s.r(x,y,w,h,bgc,200+id_,HVG); s.art(x+3,y+(h-16)//2,icon,200+id_)
        s.t(x+22,y+(h-rom.metrics(9)[1])//2,label,9,0,b,True)
    def big(s,x,y,w,h,label,id_,icon,chev=False):
        "Large icon on top, label below."
        s.r(x,y,w,h,LG,200+id_,HVG); s.art(x+(w-32)//2,y+3,icon,200+id_,2)
        tw=twidth(label); lx=x+(w-tw)//2-(6 if chev else 0); e=s.t(lx,y+h-20,label,9,0,3,True)
        if chev: s.art(e-3,y+h-20,'chev',200+id_)
    def qbtn(s,x,y,w,h,icon,id_):
        s.r(x,y,w,h,BLUE,200+id_,HVB); s.art(x+(w-16)//2,y+(h-16)//2,icon,200+id_)
def common():
    u=L(); u.r(0,0,1280,32,BLUE); u.r(0,32,1280,28,LG)
    u.qbtn(10,6,22,20,'undo',27); u.qbtn(34,6,22,20,'redo',28); u.qbtn(60,6,40,20,'save',47); u.qbtn(102,6,40,20,'open',48); u.qbtn(144,6,40,20,'pdf',53)
    x=(1280-twidth('Document1 - SynapseWrite'))//2; u.t(x,9,'Document1 - SynapseWrite',9,2,4)
    names=['Home','Insert','Layout','References','Review','View']
    return u,names
def tabbar(u,names,sel):
    x=56
    for i,nm in enumerate(names):
        w=twidth(nm)+24
        if i==sel:
            u.r(x,34,w,26,LG,200+29+i); u.t(x+12,38,nm,9,TBLUE,3); u.r(x+10,56,w-20,3,BLUE,200+29+i)
        else:
            u.r(x,34,w,26,LG,200+29+i,HVG); u.t(x+12,38,nm,9,0,3,True)
        x+=w+2
    u.r(0,60,1280,90,LG); u.r(0,149,1280,1,BD)
    u.r(0,150,1280,24,(240,240,240)); u.r(0,173,1280,1,BD)
def ruler():
    "Inch ticks and numbers; the network redraws them when the markers move."
    u=L()
    for k in range(0,9):
        xx=319+k*96
        if xx<=943:
            if k==0 or k==7: pass
            else: u.r(xx-16,161,1,3,(120,120,120)); u.r(xx-48,160,1,5,(120,120,120)); u.r(xx-80,161,1,3,(120,120,120))
            if 0<k<7: u.i.append(('g',48+k,9,xx-3,155,1,0,False))
    u.r(0,173,1280,1,BD)
    return u
def group_label(u,x,w,t):
    u.t(x+(w-twidth(t))//2,131,t,9,1,3); u.r(x+w+3,66,1,78,BD)
def home(u):
    x=8
    u.big(x,64,50,62,'Paste',36,'paste'); u.ibtn(x+52,64,50,22,'Cut',38,'cut'); u.ibtn(x+52,88,50,22,'Copy',37,'copy'); group_label(u,x,102,'Clipboard'); x+=112
    # boxes hold the current font and size, drawn live by the network
    u.r(x,64,58,22,BD,206); u.btn(x+58,64,14,22,'',42); u.art(x+57,68,'chev',242)
    u.r(x+74,64,30,22,BD,240); u.btn(x+104,64,14,22,'',40); u.art(x+103,68,'chev',240)
    u.btn(x+120,64,24,22,'A+',4); u.btn(x+146,64,24,22,'A-',5)
    for c,xx in ((0,x+82),(4,x+108),(3,x+134)):
        u.r(xx,90,24,24,LG,200+7+c,HVG); u.t(xx+7,92,'A',9,0,3,True); u.r(xx+3,108,18,4,__import__('app_pal').F[c],200+7+c)
    u.r(x+160,90,20,24,LG,241,HVG); u.art(x+162,94,'chev',241)
    group_label(u,x,182,'Font'); x+=192
    u.r(x,64,34,24,LG,219,HVG); u.art(x+9,68,'bul',219)
    u.r(x+36,64,34,24,LG,220,HVG); u.art(x+45,68,'num',220)
    for i in range(4):
        xx=x+i*30; u.r(xx,92,28,24,LG,200+15+i,HVG)
        for ln,wd in enumerate((18,12,18,12) if i<3 else (18,18,18,18)):
            off={0:4,1:(28-wd)//2,2:24-wd,3:5}[i]; u.r(xx+off,96+ln*4,wd,2,(70,70,70),200+15+i)
    group_label(u,x,122,'Paragraph'); x+=132
    for i,(nm,st,f) in enumerate((('Normal',9,0),('Title',2+16,0),('Heading 1',1,TBLUE),('Heading 2',9+16,TBLUE))):
        u.r(x+i*88,64,84,50,BD,200+21+i)
        u.r(x+i*88+1,65,82,48,WHT,200+21+i,HVG)
        tw=sum(rom.glyph(0,(st>>4)&1,0,st&15,ord(c))[0] for c in nm)
        u.t(x+i*88+(84-tw)//2,64+(50-rom.metrics(st&15)[1])//2,nm,st,f,0,True)
    group_label(u,x,348,'Styles'); x+=358
    u.ibtn(x,64,70,24,'Find',25,'find'); u.ibtn(x,90,70,24,'Replace',26,'repl'); group_label(u,x,72,'Editing')
def insert(u):
    u.ibtn(8,64,70,24,'2 x 2',40,'table'); u.ibtn(82,64,70,24,'3 x 3',41,'table'); u.ibtn(156,64,70,24,'4 x 4',42,'table'); group_label(u,8,218,'Tables')
    u.ibtn(240,64,70,24,'Header',46,'head'); group_label(u,240,72,'Header'); u.ibtn(322,64,70,24,'Picture',52,'pic'); group_label(u,322,72,'Pictures')
def layout(u):
    u.ibtn(8,64,80,24,'One',43,'col1'); u.ibtn(92,64,80,24,'Two',44,'col2'); group_label(u,8,164,'Columns')
    u.big(186,64,62,62,'Page Break',1,'brk'); group_label(u,186,62,'Breaks')
    u.big(260,64,62,62,'Margins',6,'marg',True); group_label(u,260,62,'Page Setup')
    u.ibtn(334,64,86,24,'Indent -',2,'ind-'); u.ibtn(334,90,86,24,'Indent +',3,'ind+')
    u.ibtn(424,64,86,24,'Space -',4,'sp-'); u.ibtn(424,90,86,24,'Space +',5,'sp+')
    u.big(514,64,62,62,'Line',7,'lsp',True); group_label(u,334,242,'Paragraph')
def refs(u):
    u.ibtn(8,64,122,24,'Table of Contents',45,'toc'); group_label(u,8,122,'Table of Contents'); u.ibtn(142,64,100,24,'Footnote',51,'fn'); group_label(u,142,102,'Footnotes')
def review(u):
    u.ibtn(8,64,100,24,'Comment',49,'cmt'); group_label(u,8,102,'Comments')
def view(u):
    for i,(nm,ic) in enumerate((('Ruler','ruler'),('Formatting Marks','marks'))):
        u.r(8,64+i*26,150,24,LG,200+1+i,HVG); u.r(12,69+i*26,14,14,(120,120,120),200+1+i); u.r(13,70+i*26,12,12,WHT,200+1+i)
        u.art(30,68+i*26,ic,200+1+i); u.t(50,68+i*26,nm,9,0,3,True)
    group_label(u,8,150,'Show')
def emit(net,fsm,rA,bus,YB,items,seq0_state,hv_reg,hb,bg):
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
def build(net,fsm,rA,g_en,g_ch,g_st,g_x,g_y,g_draw,fg,bg,YB,tab,S,hov,hb,hvo):
    bus=(g_en,g_ch,g_st,g_x,g_y,g_draw,fg)
    en=S('UI'); hot=net.decode(tab,6,en)
    u0,names=common()
    fsm.on('UI',*[(hot[i],f'UI_{i}',None) for i in range(6)],(None,'RD0',None))
    for k in range(6):
        u=L(); u.i=list(u0.i); tabbar(u,names,k)
        (home,insert,layout,refs,review,view)[k](u)
        last=emit(net,fsm,rA,bus,YB,u.i,f'UI_{k}',hov,hb,bg)
        c=net.and_(last,hvo)   # a hover redraw skips the document walk
        net.rec(fsm.state('RD0'),last-c); net.rec(fsm.state('TB0'),c)
