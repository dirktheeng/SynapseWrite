"""Draws circuit parts beside their matrix rows, and the mix of parts per family. Usage: circuit_fig.py measured.json figures_dir"""
import json,sys,html
C=json.load(open(sys.argv[1]));O=sys.argv[2];T=C['tot'];tot=sum(T.values())
INK,MUT,LINE,BG='#1c2733','#5b6b7b','#c9d3dd','#fbfcfd';BLUE,TEAL,AMB='#2563c9','#0f9d8a','#d97706'
def t(x,y,s,sz=14,c=INK,a='start',w=400,mono=False):
    f=' font-family="ui-monospace,Menlo,Consolas,monospace"' if mono else ''
    return f'<text x="{x}" y="{y}" font-size="{sz}" fill="{c}" text-anchor="{a}" font-weight="{w}"{f}>{html.escape(str(s))}</text>'
def wrap(w,h,b,ti):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{html.escape(ti)}" font-family="-apple-system,\'Segoe UI\',Helvetica,Arial,sans-serif"><title>{html.escape(ti)}</title><rect width="{w}" height="{h}" rx="12" fill="{BG}" stroke="{LINE}"/>{b}</svg>'
def wire(d,c=INK):return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2"/>'
def AND(x,y,lab='&'):return wire(f'M{x} {y+9}h18M{x} {y+29}h18M{x+58} {y+19}h18')+f'<path d="M{x+18} {y}h20a20 19 0 0 1 0 38h-20z" fill="#e8f0fc" stroke="{BLUE}" stroke-width="2"/>'
def OR(x,y):return wire(f'M{x} {y+9}h22M{x} {y+29}h22M{x+60} {y+19}h16')+f'<path d="M{x+16} {y}q30 0 44 19q-14 19 -44 19q10 -19 0 -38z" fill="#e8f0fc" stroke="{BLUE}" stroke-width="2"/>'
def CMP(x,y):return wire(f'M{x} {y+9}h18M{x} {y+29}h18M{x+56} {y+19}h20')+f'<path d="M{x+18} {y-2}v42l38 -21z" fill="#e8f0fc" stroke="{BLUE}" stroke-width="2"/>'+t(x+24,y+13,'+',11)+t(x+24,y+33,'−',11)
def SW(x,y):return wire(f'M{x} {y+26}h22M{x+54} {y+26}h22M{x+38} {y}v14',TEAL)+f'<circle cx="{x+24}" cy="{y+26}" r="3" fill="{TEAL}"/><circle cx="{x+52}" cy="{y+26}" r="3" fill="{TEAL}"/><path d="M{x+24} {y+26}L{x+50} {y+15}" stroke="{TEAL}" stroke-width="2"/>'
def ADD(x,y):return wire(f'M{x} {y+9}h22M{x} {y+29}h22M{x+56} {y+19}h20',TEAL)+f'<circle cx="{x+38}" cy="{y+19}" r="18" fill="#e2f5f2" stroke="{TEAL}" stroke-width="2"/>'+t(x+38,y+25,'Σ',17,INK,'middle',700)
def REG(x,y):return wire(f'M{x} {y+19}h18M{x+58} {y+19}h18M{x+66} {y+19}v28h-56v-28',AMB)+f'<rect x="{x+18}" y="{y}" width="40" height="38" rx="3" fill="#fdf1e0" stroke="{AMB}" stroke-width="2"/>'+t(x+38,y+24,'D',15,INK,'middle',700)
R=[(AND,'AND','step( a + b − 1 )','F row: a=1, b=1   bias −1',f"{C['n']['AND-form']:,} in this exact form"),(OR,'OR','step( a + b )','F row: a=1, b=1   bias 0',f"{C['n']['OR-form']:,} in this exact form"),(CMP,'Comparator','step( x − 214 )','F row: x=1   bias −214',f"{T['Comparator']:,}, plus {T['Gated threshold']:,} with an enable"),(SW,'Switch','relu( v + en·2^40 − 2^40 )','F row: v=1, en=2^40   bias −2^40',f"{T['Switch for a number']:,}"),(ADD,'Adder','a + b','F row: a=1, b=1   identity',f"{T['Adder or wire']:,}, with wires"),(REG,'Register','r(t) = r(t−1) + set − clear','R row: r=1, then gated changes',"state held over ticks")]
b=t(30,38,'Circuit parts, and the matrix rows that make them',20,INK,'start',700)+t(30,62,'Weights are the wiring. Example rows show the form; counts are from the shipped weight file.',14,MUT)
for x_,l in ((30,'Part'),(210,'Neuron'),(500,'Its row in the matrix'),(770,'Count')):b+=t(x_,92,l,13,MUT,'start',700)
for i,(fn,n,f,row,c) in enumerate(R):
    y=108+i*64;b+=fn(30,y)+t(118,y+24,n,14.5,INK,'start',600)+t(210,y+24,f,13,INK,'start',400,True)+t(500,y+24,row,13,INK,'start',400,True)+t(770,y+24,c,13,INK)
    if i<5:b+=f'<path d="M30 {y+54}H970" stroke="#e6ebf0"/>'
open(O+'/circuit_parts.svg','w').write(wrap(1000,500,b,'Circuit parts and their matrix rows'))
K=[('Plain logic gate','#123f8f','Plain logic gate'),('Gated threshold','#2563c9','Gated threshold'),('Comparator','#7aa7e6','Comparator'),('Switch for a number','#0b7d6e','Switch for a number'),('Adder or wire','#3bb8a6','Adder or wire'),('Ramp or clamp','#a0dcd2','Ramp or clamp'),('Register that only holds','#d97706','Holding register'),('Constant or input','#c9d3dd','Constant or input')]
b=t(30,38,'Which circuit parts each family uses',20,INK,'start',700)+t(30,62,'Share of each family\'s neurons. Blue outputs 0 or 1. Green carries numbers. Amber only holds a value.',14,MUT)
rows=[('All neurons',T)]+[(n,C['per'][n]) for n in C['names']]
for i,(n,d) in enumerate(rows):
    y=84+i*36;tt=sum(d.values());b+=t(30,y+18,n,13.5,INK,'start',700 if i==0 else 400);x=270
    for k,c,_ in K:
        w=660*d.get(k,0)/tt
        if w>0:b+=f'<rect x="{x:.1f}" y="{y}" width="{max(w-1,.5):.1f}" height="26" fill="{c}"><title>{n}: {k} {d.get(k,0):,}</title></rect>'
        x+=w
    b+=t(940,y+18,f'{tt:,}',12,MUT)
y=84+len(rows)*36+6
for j,(k,c,l) in enumerate(K):
    X=30+(j%4)*235;Y=y+(j//4)*26;b+=f'<rect x="{X}" y="{Y}" width="14" height="14" fill="{c}"/>'+t(X+20,Y+12,f'{l} {100*T[k]/tot:.1f}%',12.5)
open(O+'/circuit_mix.svg','w').write(wrap(1000,y+66,b,'Mix of circuit parts per family'))
