"""Animated worked example of one sweep through a lower triangular matrix."""
import sys,html
O=sys.argv[1]
INK,MUT,LINE,BG,BLUE,AMB,TEAL='#1c2733','#5b6b7b','#c9d3dd','#fbfcfd','#2563c9','#d97706','#0f9d8a'
T=10
def t(x,y,s,sz=16,c=INK,a='middle',w=400,extra=''):return f'<text x="{x}" y="{y}" font-size="{sz}" fill="{c}" text-anchor="{a}" font-weight="{w}" {extra}>{html.escape(str(s))}</text>'
def on(start,end=T):
    a,b=start/T,end/T
    return f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="0;{a:.3f};{a+.01:.3f};{b:.3f};{min(b+.01,1):.3f};1" values="0;0;1;1;0;0" />' if end<T else f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="0;{a:.3f};{a+.01:.3f};.98;1" values="0;0;1;1;0"/>'
def cell(x,y,s,c=INK,fill='#fff',b=False):return f'<rect x="{x}" y="{y}" width="56" height="44" fill="{fill}" stroke="{LINE}"/>'+t(x+28,y+29,s,18,c,'middle',700 if b else 400)
b=t(30,38,'One sweep: filling in the vector from the top down',20,INK,'start',700)+t(30,62,'Each row only uses numbers above it, so the same vector can appear on both sides with nothing circular.',14.5,MUT,'start')
Y=108;MX=300;VX=120;RX=570;IX=690
b+=t(VX+28,Y-12,'v',18,BLUE,'middle',700)+t(MX+84,Y-12,'F',18,BLUE,'middle',700)+t(RX+28,Y-12,'v',18,BLUE,'middle',700)+t(IX+28,Y-12,'input',15,BLUE,'middle',700)
names='abc';F_=[['0','0','0'],['10','0','0'],['1','1','0']];inp=['5','0','0'];vals=['5','50','55'];rows=['a = 5','b = 10 × a = 50','c = a + b = 55']
for r in range(3):
    y=Y+r*44
    b+=t(VX-14,y+29,names[r],17,MUT,'end')
    b+=cell(VX,y,'')+cell(RX,y,'')+cell(IX,y,inp[r],INK,'#fdf1e0')
    for c in range(3):b+=cell(MX+c*56,y,F_[r][c],INK if F_[r][c]!='0' else '#a8b4c0','#e8f0fc' if F_[r][c]!='0' else '#fff',F_[r][c]!='0')
    s0=1+r*2.6
    b+=f'<rect x="{MX-4}" y="{y-2}" width="176" height="48" rx="6" fill="none" stroke="{AMB}" stroke-width="3" opacity="0">{on(s0,s0+2.4)}</rect>'
    for X in (VX,RX):b+=f'<g opacity="0">{on(s0+.9)}'+t(X+28,y+29,vals[r],19,BLUE,'middle',700)+'</g>'
    b+=f'<g opacity="0">{on(s0,s0+2.4)}'+t(500,Y+176,f'Step {r+1}:  {rows[r]}',19,INK,'middle',700)+'</g>'
b+=t(VX+90,Y+74,'=',28,INK)+t(MX+196,Y+74,'×',24,INK)+t(RX+88,Y+74,'+',26,INK)
b+=f'<g opacity="0">{on(8.8)}'+t(500,Y+176,'Done. Multiply it out and you get the same vector back.',18,TEAL,'middle',700)+'</g>'
s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 310" width="1000" height="310" role="img" aria-label="Animated forward substitution example" font-family="-apple-system,\'Segoe UI\',Helvetica,Arial,sans-serif"><title>One sweep through a lower triangular matrix</title><rect width="1000" height="310" rx="12" fill="{BG}" stroke="{LINE}"/>{b}</svg>'
open(O+'/equation_sweep.svg','w').write(s)
