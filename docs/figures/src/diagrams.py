"""Writes the README's SVG diagrams. Animations are SMIL, which GitHub shows inside <img>. Numbers come from build/provenance.json and the capture."""
import json,sys,html
O,CAP,PROV=sys.argv[1],sys.argv[2],sys.argv[3]
INK,MUT,LINE,BG,CARD='#1c2733','#5b6b7b','#c9d3dd','#fbfcfd','#ffffff'
BLUE,AMB,TEAL,VIO,RED='#2563c9','#d97706','#0f9d8a','#7a5cd6','#c0392b'
TINT={BLUE:'#e8f0fc',AMB:'#fdf1e0',TEAL:'#e2f5f2',VIO:'#efebfa',MUT:'#eef1f4',RED:'#fbe9e7'}
def svg(w,h,body,title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{html.escape(title)}" font-family="-apple-system,'Segoe UI',Helvetica,Arial,sans-serif">
<title>{html.escape(title)}</title><rect width="{w}" height="{h}" rx="12" fill="{BG}" stroke="{LINE}"/>{body}</svg>'''
def t(x,y,s,sz=14,c=INK,a='start',w=400,extra=''):
    return f'<text x="{x}" y="{y}" font-size="{sz}" fill="{c}" text-anchor="{a}" font-weight="{w}" {extra}>{html.escape(str(s))}</text>'
def box(x,y,w,h,c,title,sub=None,sz=15,fill=None):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill or TINT[c]}" stroke="{c}" stroke-width="1.5"/>'
    cy=y+h/2+(-3 if sub else 5)
    s+=t(x+w/2,cy,title,sz,INK,'middle',600)
    if sub:
        for i,l in enumerate(sub if isinstance(sub,list) else [sub]): s+=t(x+w/2,cy+18+i*16,l,12,MUT,'middle')
    return s
def arrow(d,c=LINE,dash=''):
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="1.6" marker-end="url(#a{c[1:]})" {"stroke-dasharray=%r"%dash if dash else ""}/>'
def defs(*cs):
    return '<defs>'+''.join(f'<marker id="a{c[1:]}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="{c}"/></marker>' for c in cs)+'</defs>'
def pulse(d,c,begin,dur,total,r=6):
    b,e=begin/total,(begin+dur)/total
    kt=f'0;{b:.4f};{e:.4f};1'
    return f'''<circle r="{r}" fill="{c}" opacity="0"><animateMotion path="{d}" dur="{total}s" repeatCount="indefinite" calcMode="linear" keyPoints="0;0;1;1" keyTimes="{kt}"/><animate attributeName="opacity" dur="{total}s" repeatCount="indefinite" keyTimes="0;{b:.4f};{max(b+.001,b):.4f};{e:.4f};{min(e+.001,1):.4f};1" values="0;0;1;1;0;0"/></circle>'''
def flash(x,y,w,h,c,begin,dur,total):
    b,e=begin/total,(begin+dur)/total
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{c}" opacity="0"><animate attributeName="opacity" dur="{total}s" repeatCount="indefinite" keyTimes="0;{b:.4f};{(b+e)/2:.4f};{e:.4f};1" values="0;0;.28;0;0"/></rect>'
def write(n,s): open(f'{O}/{n}.svg','w').write(s)
P=json.load(open(PROV))
# ---------- one tick ----------
T=8;b=defs(LINE,TEAL,VIO,MUT)
b+=t(30,38,'One tick of the neural program',20,INK,'start',700)+t(30,60,'Every event starts ticks. Ticks repeat until the network raises halt.',14,MUT)
L=[(90,'Event vector','key, mouse, timer, file',AMB),(180,'Memory read vectors','asked for on the last tick',TEAL),(270,'Recurrent state','one-hot states, registers',BLUE),(360,'Last screenshot','pixels and id plane',VIO)]
R=[(80,'Next screenshot','RGBA tensor',VIO),(155,'Memory operations','address, write, mask',TEAL),(230,'Recurrent state','next values',BLUE),(305,'Timer request','for example caret blink',AMB),(380,'Halt','stop and wait',RED)]
for y,a,s,c in L: b+=box(30,y,210,66,c,a,s)+arrow(f'M240 {y+33}H372')
for y,a,s,c in R: b+=box(760,y,210,60,c,a,s)+arrow(f'M628 {y+30}H758')
b+=f'<rect x="374" y="90" width="252" height="336" rx="14" fill="{TINT[BLUE]}" stroke="{BLUE}" stroke-width="2"/>'
b+=flash(374,90,252,336,BLUE,1.1,1.5,T)
import random
rng=random.Random(7)
for lx in range(5):
    for ly in range(5):
        x,y=412+lx*44,190+ly*32
        b+=f'<circle cx="{x}" cy="{y}" r="6" fill="{CARD}" stroke="{BLUE}"><animate attributeName="fill" dur="{T}s" repeatCount="indefinite" keyTimes="0;{(1.1+lx*.28)/T:.3f};{(1.25+lx*.28)/T:.3f};{(1.45+lx*.28)/T:.3f};1" values="{CARD};{CARD};{BLUE if rng.random()<.32 else CARD};{CARD};{CARD}"/></circle>'
b+=t(500,126,'One sparse network',17,INK,'middle',700)+t(500,146,f"{P['neurons']:,} neurons, {P['layers']} layers",13,MUT,'middle')+t(500,164,f"{P['states']:,} control states",13,MUT,'middle')
for i,(y,_,_,c) in enumerate(L): b+=pulse(f'M240 {y+33}H372',c,.1+i*.12,.9,T)
for i,(y,_,_,c) in enumerate(R): b+=pulse(f'M628 {y+30}H758',c,2.7+i*.1,.8,T)
# feedback rails
b+=f'<rect x="30" y="462" width="940" height="44" rx="9" fill="{TINT[MUT]}" stroke="{LINE}"/>'+t(500,489,'Passive memory bank and glue: they execute what the network asked, and decide nothing',14,INK,'middle',600)
ret='M970 185H985V484H970'
b+=arrow('M970 185H985V462','#0f9d8a')+arrow('M30 484H14V213H28','#0f9d8a')
b+=pulse('M970 185H985V462',TEAL,3.6,.9,T,5)+pulse('M30 484H14V213H28',TEAL,5.5,1.3,T,5)
b+=t(500,532,'Reads arrive on the next tick and last one tick, so the network plans its memory traffic like a pipeline.',13,MUT,'middle')
write('tick_loop',svg(1000,552,b,'One tick: event, memory reads, state and last screenshot flow through the network to the next screenshot, memory operations, state, timer and halt'))
# ---------- neurons and gate ----------
T=6;b=defs(LINE,BLUE)
b+=t(30,38,'Three neurons, and the gate that makes them a computer',20,INK,'start',700)
def curve(x,y,name,form,path):
    s=f'<rect x="{x}" y="{y}" width="190" height="178" rx="9" fill="{CARD}" stroke="{LINE}"/>'
    ax=x+95;ay=y+105
    s+=f'<path d="M{x+18} {ay}H{x+172}M{ax} {y+36}V{y+148}" stroke="{LINE}"/>'
    s+=f'<path d="{path(ax,ay)}" fill="none" stroke="{BLUE}" stroke-width="3" stroke-linecap="round"/>'
    return s+t(x+14,y+26,name,15,INK,'start',700)+t(x+95,y+168,form,13,MUT,'middle')
b+=curve(30,60,'Identity','y = x',lambda a,c:f'M{a-60} {c+40}L{a+60} {c-60}')
b+=curve(235,60,'Step','y = 1 if x > 0',lambda a,c:f'M{a-70} {c}H{a}V{c-50}H{a+70}')
b+=curve(440,60,'ReLU','y = max(0, x)',lambda a,c:f'M{a-70} {c}H{a}L{a+60} {c-60}')
# gate
b+=f'<rect x="650" y="60" width="320" height="178" rx="9" fill="{CARD}" stroke="{LINE}"/>'
b+=t(666,86,'Big-M gate',15,INK,'start',700)+t(666,110,'y = relu(v + en * M - M),  M = 2^40',13,MUT)
def togg(a,bb,x,y,sz=20,c=INK):
    return f'<text x="{x}" y="{y}" font-size="{sz}" font-weight="700" fill="{c}" text-anchor="middle">{a}<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" values="1;1;0;0;1" keyTimes="0;.48;.5;.98;1"/></text><text x="{x}" y="{y}" font-size="{sz}" font-weight="700" fill="{c}" text-anchor="middle" opacity="0">{bb}<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" values="0;0;1;1;0" keyTimes="0;.48;.5;.98;1"/></text>'
b+=t(700,150,'v',14,MUT,'middle')+t(700,178,'42',20,INK,'middle',700)
b+=t(810,150,'en',14,MUT,'middle')+togg('1','0',810,178,20,AMB)
b+=t(920,150,'y',14,MUT,'middle')+togg('42','0',920,178,20,BLUE)
b+=t(810,216,'Open: v passes. Closed: output is exactly 0.',12.5,MUT,'middle')
b+=f'<rect x="30" y="256" width="940" height="52" rx="9" fill="{TINT[BLUE]}" stroke="{BLUE}"/>'+t(500,288,'Neurons rest at zero, and a closed gate skips its value inputs, so idle parts of the network cost nothing.',14.5,INK,'middle',600)
write('neuron_gate',svg(1000,326,b,'Identity, step and ReLU neurons, and a big-M gate passing or blocking a value'))
# ---------- FSM ----------
T=7.5;b=defs(LINE,AMB)
b+=t(30,38,'Control flow is a token moving through one-hot state neurons',20,INK,'start',700)
b+=t(30,60,'Exactly one state neuron is 1. Its weights open the gates that load registers and drive ports.',14,MUT)
S=[('Idle','waiting',90),('Key handling','name the key',270),('Edit','write text cell',450),('Layout','break lines',630),('Paint','draw glyphs',810)]
Y=90
for i,(a,s_,x) in enumerate(S):
    b+=box(x-75,Y,150,70,MUT if i==0 else BLUE,a,s_)
    if i<4: b+=arrow(f'M{x+75} {Y+35}H{S[i+1][2]-77}')
    b+=flash(x-75,Y,150,70,AMB,i*1.3,1.3,T)
b+=arrow(f'M810 {Y+70}V{Y+102}H90V{Y+72}','#d97706','5 4')+t(450,Y+97,'halt raised, wait for the next event',13,AMB,'middle',600)
b+=pulse(f'M90 {Y-14}H810',AMB,0,5.2,T,7)
Yb=232
b+=f'<rect x="30" y="{Yb}" width="940" height="128" rx="9" fill="{CARD}" stroke="{LINE}"/>'
b+=t(50,Yb+28,'Written in the generator, not trained:',14,INK,'start',700)
code=["on('KEY_TYPED',","   (is_enter,  'SPLIT_PARA', {}),","   (None,      'INS_CHAR',   {cursor: cursor + 1, dirty: ONE}))"]
for i,l in enumerate(code): b+=f'<text x="50" y="{Yb+56+i*22}" font-size="14" font-family="ui-monospace,Menlo,Consolas,monospace" fill="{INK}" xml:space="preserve">{html.escape(l)}</text>'
b+=t(610,Yb+56,'Each rule becomes an AND neuron.',13.5,MUT)+t(610,Yb+78,'Each assignment becomes a gated weight.',13.5,MUT)+t(610,Yb+100,'State names here are illustrative of the rule form.',13.5,MUT)
write('fsm',svg(1000,380,b,'A token moves through one-hot state neurons: idle, key handling, edit, layout, paint'))
# ---------- glue ----------
b=defs(LINE)
b+=t(30,38,'Where the logic lives',20,INK,'start',700)
b+=f'<rect x="30" y="58" width="560" height="350" rx="12" fill="{TINT[BLUE]}" stroke="{BLUE}" stroke-width="2"/>'+t(50,88,'The network: everything the app decides',16,INK,'start',700)
it=['Key names to editing commands','Hit testing from the screen id plane','Layout, line breaking, pagination','Drawing every glyph, icon and widget','Undo log, find, spell check, tables','Zip, inflate, deflate, CRC, XML, PNG, PDF','Every memory address, read, write and mask','File names, messages, when to set a timer']
for i,s_ in enumerate(it): b+=t(50,118+i*33,'+',16,BLUE,'start',700)+t(70,118+i*33,s_,14.5)
b+=t(50,396,f"{P['neurons']:,} neurons, written by a deterministic generator",13,MUT)
b+=f'<rect x="610" y="58" width="360" height="172" rx="12" fill="{TINT[MUT]}" stroke="{MUT}" stroke-width="2"/>'+t(630,88,'host/glue.js: 81 lines',16,INK,'start',700)
for i,s_ in enumerate(['Start inference, repeat ticks to halt','Encode events and bytes as vectors','Show the output tensor with putImageData','Execute named commands from output neurons']): b+=t(630,116+i*26,s_,13.5)
b+=f'<rect x="610" y="240" width="360" height="168" rx="12" fill="{TINT[TEAL]}" stroke="{TEAL}" stroke-width="2"/>'+t(630,270,'host/engine.c: 140 lines',16,INK,'start',700)
for i,s_ in enumerate(['Sparse layered neuron evaluation','Passive ports: bank, image, patch, copy','Zero-rest live lists and lazy pulls','No character codes, no document logic']): b+=t(630,298+i*26,s_,13.5)
b+=t(500,436,'test/audit.py holds exact allow lists for every condition and string in the glue, and fails on anything new.',13,MUT,'middle')
write('glue_boundary',svg(1000,456,b,'The network holds all application logic; glue and engine only run it'))
# ---------- pipeline: build ----------
T=7;b=defs(LINE)
b+=t(30,38,'From Python to weights to a single web page',20,INK,'start',700)
st=[(30,'gen/*.py',['Deterministic','weight generator'],BLUE),(225,'Open fonts',['Outlines become','edge neurons'],VIO),(420,'Optimizer passes',['Dead code, merge','duplicates'],MUT),(615,'Compact stream',['Layer order,','varints, gzip'],TEAL),(810,'index.html',['3.2 MB, static,','one file'],AMB)]
for i,(x,a,s_,c) in enumerate(st):
    b+=box(x,70,160,92,c,a,s_)
    if i<4: b+=arrow(f'M{x+160} 116H{st[i+1][0]-2}'); b+=pulse(f'M{x+160} 116H{st[i+1][0]-2}',c,i*1.3,1,T)
b+=t(500,196,'No data set, loss, gradient, search or fitting exists anywhere in this path. Python only runs at build time.',14,MUT,'middle')
write('build_pipeline',svg(1000,214,b,'Build pipeline from generator to static page'))
# ---------- docx ----------
T=10;b=defs(LINE,TEAL)
b+=t(30,38,'File formats are networks too',20,INK,'start',700)+t(30,60,'Glue only moves bytes into the bank and out again. No library parses or writes these files.',14,MUT)
op=['File bytes','Zip directory','Inflate','XML automaton','Interned styles','Paragraph slots']
sv=['Paragraph slots','XML writer','Deflate','CRC32','Zip container','Download']
sa=['from the glue','find members','Huffman, LZ77','tags, runs, tables','find or add','the document'];sb=['the document','document parts','hash matches','over each part','table driven','on command']
W=140;G=23
def row(y,ns,sb_,c,off):
    s=t(30,y-10,off,14,c,'start',700)
    for i,n in enumerate(ns):
        x=30+i*(W+G);s+=box(x,y,W,70,c,n,sb_[i],13.5)
        if i<5:s+=arrow(f'M{x+W} {y+35}H{x+W+G-2}')
    return s
b+=row(100,op,sa,BLUE,'Open')+row(220,sv,sb,TEAL,'Save')
b+=pulse(f'M30 92H{30+5*(W+G)+W}',BLUE,0,4.5,T,7)+pulse(f'M30 212H{30+5*(W+G)+W}',TEAL,5,4.5,T,7)
b+=t(500,322,'Pictures (PNG) and PDF export follow the same pattern, including embedded font subsets in the PDF.',13.5,MUT,'middle')
write('docx_pipeline',svg(1000,342,b,'Open and save pipelines through zip, inflate, XML, deflate and CRC networks'))
# ---------- memory map ----------
R_=[('0 to 100 K','Fixed tables: hit targets, styles, numbering, sections',BLUE),('100 K to 1.02 M','Mail merge, footnotes, zip records, headers and footers',BLUE),('1.1 M to 1.4 M','Interned styles, bookmarks, spell suggestions, equations',VIO),('1.4 M to 2 M','Clipboards',AMB),('2 M to 14.4 M','Paragraph slots: 4,096 cells each',TEAL),('14.5 M to 20 M','Undo log',AMB),('20 M to 61 M','Output bytes, pictures, save and load work space',MUT),('61 M to 63 M','Glyph cache: tags, then drawn glyphs',VIO),('63 M to 67 M','Read only tables: PDF fonts, literals, display lists',BLUE)]
b=t(30,38,'One passive memory bank',20,INK,'start',700)+t(30,60,'Cells are 32-bit floats. Pages exist only once written, so far apart regions cost nothing until used. Not to scale.',14,MUT)
for i,(a,s_,c) in enumerate(R_):
    y=78+i*38;b+=f'<rect x="30" y="{y}" width="150" height="32" rx="6" fill="{TINT[c]}" stroke="{c}"/>'+t(105,y+21,a,13,INK,'middle',600)+t(196,y+21,s_,14)
b+=t(30,y+60,'The build fails if any two declared regions overlap: region() in gen/nn.py.',13,MUT)
write('memory_map',svg(800,y+74,b,'Memory bank map'))
# ---------- charts ----------
G_=P['groups'];fam={'Font outlines as neurons':['glyph weights (outline edges)'],'Glyph machinery and metrics':['glyph unit','glyph metrics','ramp bank','coverage','glyph network','snapping layer','glyph geometry','row sequencer','glyph store','glyph patch','style interner'],'Ribbon and chrome':['ribbon display list','chrome','ribbon actions','pointer','canvas look','a4 ruler'],'File formats':[k for k in G_ if k.startswith(('docx','pdf','zip','png'))]}
used=set(sum(fam.values(),[]));fam['Editing, layout and everything else']=[k for k in G_ if k not in used]
rows=sorted(((k,sum(G_[g]['neurons'] for g in v if g in G_)) for k,v in fam.items()),key=lambda r:-r[1]);tot=sum(r[1] for r in rows)
assert tot==P['neurons']
b=t(30,38,'Where the neurons are',20,INK,'start',700)+t(30,60,f"{P['neurons']:,} neurons in {len(G_)} named sub-networks. Most of the weight is the fonts.",14,MUT)
for i,(k,n) in enumerate(rows):
    y=84+i*44;w=max(4,520*n/rows[0][1]);b+=t(30,y+19,k,14)+f'<rect x="290" y="{y}" width="{w:.1f}" height="28" rx="4" fill="{BLUE}"><title>{k}: {n:,}</title></rect>'+t(298+w,y+19,f'{n:,} ({100*n/tot:.1f}%)',13,INK)
write('subnetwork_sizes',svg(1000,y+50,b,'Neuron counts per family of sub-networks'))
C=json.load(open(CAP+'/meta.json'));lab={'key_same':'Type a letter','key_new':'Type a new letter','mouse_move':'Move the mouse','click':'Click in text','wheel':'Scroll one notch','bold':'Press Ctrl+B','paste':'Paste two lines'}
rows=[m for k in lab for m in C['meta'] if m['name']==k]
b=t(30,38,'Almost all of the network is silent on any event',20,INK,'start',700)+t(30,60,f"Neurons that fired at least once, out of {C['N']:,}. Short document, measured on the real weights.",14,MUT)
mx=max(m['fired'] for m in rows)
for i,m in enumerate(rows):
    y=84+i*40;w=max(4,520*m['fired']/mx);b+=t(30,y+18,lab[m['name']],14)+f'<rect x="210" y="{y}" width="{w:.1f}" height="26" rx="4" fill="{BLUE}"><title>{m["fired"]} neurons, {m["ticks"]} ticks</title></rect>'+t(218+w,y+18,f"{m['fired']:,} = {100*m['fired']/C['N']:.2f}%, {m['ticks']} ticks",13)
write('event_cost',svg(1000,y+48,b,'Fraction of neurons firing per event'))
json.dump([[lab[m['name']],m['ticks'],m['edges'],m['fired']] for m in rows],open(CAP+'/event_table.json','w'))
