"""Ribbon display list. Each draw item becomes outgoing weights of one token neuron."""
import rom
from nn import X
TW=rom
BLUE=(43,87,154);LG=(243,243,243);BD=(208,208,208);WHT=(255,255,255);TAB=(255,255,255)
def twidth(s,si=9,b=0):
    return sum(rom.glyph(0,b,0,si,ord(c))[0] for c in s)
ST=lambda si=9,b=0:si+16*b
class L:
    def __init__(s): s.i=[]
    def r(s,x,y,w,h,c,a=0): s.i.append(('r',x,y,w,h,c,a))
    def t(s,x,y,txt,st=9,f=0,b=3):
        si=st&15;bo=(st>>4)&1;fi=(st>>7)&1
        for ch in txt:
            s.i.append(('g',ord(ch),st,x,y,f,b)); x+=rom.glyph(fi,bo,0,si,ord(ch))[0]
        return x
    def btn(s,x,y,w,h,label,id_,st=9,f=0,b=3,bgc=LG):
        s.r(x,y,w,h,bgc,200+id_)
        tw=twidth(label,st&15,(st>>4)&1); s.t(x+(w-tw)//2,y+(h-rom.metrics(st&15)[1])//2,label,st,f,b)
def common():
    u=L(); u.r(0,0,1280,32,BLUE); u.r(0,32,1280,28,BLUE)
    u.btn(10,6,22,20,'<',27,9,2,4,BLUE); u.btn(34,6,22,20,'>',28,9,2,4,BLUE); u.btn(60,6,40,20,'Save',47,9,2,4,BLUE); u.btn(102,6,40,20,'Open',48,9,2,4,BLUE); u.btn(144,6,40,20,'PDF',53,9,2,4,BLUE)
    x=(1280-twidth('Document1 - SynapseWrite'))//2; u.t(x,9,'Document1 - SynapseWrite',9,2,4)
    x0=56;names=['Home','Insert','Layout','References','Review','View']
    return u,names
def tabbar(u,names,sel):
    x=56
    for i,nm in enumerate(names):
        w=twidth(nm)+24
        if i==sel:
            u.r(x,34,w,26,LG,200+29+i); u.t(x+12,39,nm,9,3,3)
        else:
            u.r(x,34,w,26,BLUE,200+29+i); u.t(x+12,39,nm,9,2,4)
        x+=w+2
    u.r(0,60,1280,90,LG); u.r(0,149,1280,1,BD)
    # ruler
    u.r(0,150,1280,24,(240,240,240)); u.r(223,154,816,16,(200,200,200)); u.r(319,154,624,16,WHT)
    n=0
    for k in range(0,9):
        xx=319+k*96
        if xx<=943:
            if k==0 or k==7: pass
            else: u.r(xx-16,161,1,3,(120,120,120)); u.r(xx-48,160,1,5,(120,120,120)); u.r(xx-80,161,1,3,(120,120,120))
            if 0<k<7: u.i.append(('g',48+k,9,xx-3,155,1,0))
    u.r(0,173,1280,1,BD)
def group_label(u,x,w,t):
    u.t(x+(w-twidth(t))//2,131,t,9,1,3); u.r(x+w+3,64,1,80,BD)
def home(u):
    x=8
    u.btn(x,64,50,62,'Paste',36); u.btn(x+52,64,50,20,'Cut',38); u.btn(x+52,86,50,20,'Copy',37); group_label(u,x,102,'Clipboard'); x+=112
    u.r(x,64,58,22,WHT,206); u.btn(x+60,64,24,22,'A+',4); u.btn(x+86,64,24,22,'A-',5)
    u.btn(x,90,24,24,'B',1,9+16); u.btn(x+26,90,24,24,'I',2); u.btn(x+52,90,24,24,'U',3)
    cx=x+82
    for i,c in enumerate([0,4,3,5]):
        u.r(cx+i*26,92,22,20,LG,200+7+c); u.r(cx+i*26+3,95,16,14,__import__('app_pal').F[c],200+7+c)
    group_label(u,x,182,'Font'); x+=192
    u.btn(x,64,34,24,'*',19); u.btn(x+36,64,34,24,'1.',20)
    for i in range(4):
        xx=x+i*30; u.r(xx,92,28,24,LG,200+15+i)
        for ln,wd in enumerate((18,12,18,12) if i<3 else (18,18,18,18)):
            off={0:4,1:(28-wd)//2,2:24-wd,3:5}[i]; u.r(xx+off,96+ln*4,wd,2,(70,70,70),200+15+i)
    group_label(u,x,122,'Paragraph'); x+=132
    for i,(nm,st) in enumerate((('Normal',0),('Title',10),('Heading 1',0),('Heading 2',0))):
        u.btn(x+i*88,64,84,50,nm,21+i,9,3 if i>=2 else 0,0,WHT)
    group_label(u,x,348,'Styles'); x+=358
    u.btn(x,64,70,24,'Find',25); u.btn(x,90,70,24,'Replace',26); group_label(u,x,72,'Editing')
def insert(u):
    u.btn(8,64,70,24,'Table 2x2',40); u.btn(82,64,70,24,'Table 3x3',41); u.btn(156,64,70,24,'Table 4x4',42); group_label(u,8,218,'Tables'); u.btn(240,64,70,24,'Header',46); group_label(u,240,72,'Header'); u.btn(322,64,70,24,'Picture',52); group_label(u,322,72,'Pictures')
def layout(u):
    u.btn(8,64,80,24,'One Column',43); u.btn(92,64,80,24,'Two Columns',44); group_label(u,8,164,'Columns')
def refs(u):
    u.btn(8,64,120,24,'Table of Contents',45); group_label(u,8,122,'Table of Contents'); u.btn(142,64,100,24,'Insert Footnote',51); group_label(u,142,102,'Footnotes')
def review(u):
    u.btn(8,64,100,24,'New Comment',49); group_label(u,8,102,'Comments')
def stub(u,labels):
    x=8
    for g,items in labels:
        w=sum(twidth(i)+22 for i in items)
        xx=x
        for i in items:
            ww=twidth(i)+18; u.t(xx+9,78,i,9,1,3); xx+=ww+4
        group_label(u,x,w,g); x+=w+10
STUBS={1:[('Pages',['Cover Page','Blank Page','Page Break']),('Tables',['Table']),('Illustrations',['Pictures','Shapes','Icons','Chart'])],
 2:[('Page Setup',['Margins','Orientation','Size','Columns','Breaks']),('Paragraph',['Indent','Spacing'])],
 3:[('Table of Contents',['Table of Contents','Add Text']),('Footnotes',['Insert Footnote'])],
 4:[('Proofing',['Spelling','Word Count']),('Comments',['New Comment']),('Tracking',['Track Changes'])],
 5:[('Views',['Read Mode','Print Layout','Web Layout']),('Show',['Ruler','Gridlines','Navigation Pane']),('Zoom',['Zoom','100%'])]}
def build(net,fsm,rA,g_en,g_ch,g_st,g_x,g_y,g_draw,fg,bg,YB,tab,S):
    en=S('UI'); hot=net.decode(tab,6,en)
    u0,names=common()
    fsm.on('UI',*[(hot[i],f'UI_{i}',None) for i in range(6)],(None,'RD0',None))
    for k in range(6):
        u=L(); u.i=list(u0.i); tabbar(u,names,k)
        home(u) if k==0 else (insert(u) if k==1 else layout(u) if k==2 else refs(u) if k==3 else review(u) if k==4 else stub(u,STUBS[k]))
        tok=fsm.S(f'UI_{k}')
        fsm.states[f'UI_{k}'][1].append((tok,None))
        seq=[net.reg() for _ in range(len(u.i)+1)]
        net.rec(seq[0],tok)
        for i,it in enumerate(u.i):
            t=seq[i]
            if it[0]=='r':
                _,x,y,w,h,c,a=it; rA.lin(t,x,y,w,h,c,a)
            else:
                _,ch,st,x,y,f,b=it
                g_en.lin(t);g_draw.lin(t);g_ch.lin(t*ch);g_st.lin(t*st);g_x.lin(t*x);g_y.lin(t*(y+YB));fg[f].lin(t);bg[b].lin(t)
            net.rec(seq[i+1],t)
        net.rec(fsm.state('RD0'),seq[len(u.i)])
