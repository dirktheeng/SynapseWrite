"""Shared by the glyph network tests: reference raster, ROM patches, net building and engine runs."""
import sys,os,json,subprocess,tempfile,time,math
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT+'/gen')
import numpy as np
import rom,glyphnet as gn
OUT=ROOT+'/build/glyph'; os.makedirs(OUT,exist_ok=True)
PTSZ=[9,11,13,14,18,36]
def ppem(pt): return round(pt*96/72)
def geom(pt,fi=0):
    "Patch geometry of a size: same origin as the ROM. A size the ROM lacks takes the metrics PIL gives at that ppem."
    px=ppem(pt); f=rom.font(fi,0,0,px); a,_=f.getmetrics()
    small=pt<=14; W,H=(rom.SW,rom.SH) if small else (rom.LW,rom.LH)
    return dict(px=px,a=a,W=W,H=H,small=small,rows=min(H,a+math.ceil(0.32*px)+1))
def ref_raster(fi,bo,it,code,pt,tol=None,N=8):
    """Accurate unhinted raster: N x N point samples per pixel over a very finely flattened outline, nonzero winding.
    It shares only the outline source with the network; it uses a finer flattening and plain arithmetic."""
    G=geom(pt,fi); px,a=G['px'],G['a']; W,H=G['W'],G['H']
    E=np.array(gn.edges(gn.contours(fi,bo,it,code,tol=1e-4)),dtype=float).reshape(-1,5)
    out=np.zeros((H,W))
    if len(E)==0: return out
    Y0,X0,Y1,X1,S=E.T; m=(X1-X0)/(Y1-Y0)
    xs=(np.arange(W*N)+.5)/N-gn.X0PATCH
    for r in range(H):
        for k in range(N):
            y=(a-r-(k+.5)/N)/px
            ac=(Y0<=y)&(y<Y1)
            if not ac.any(): continue
            xc=(X0[ac]+(y-Y0[ac])*m[ac])*px
            w=np.zeros(W*N)
            for x_,s_ in zip(xc,S[ac]): w[xs>x_]+=s_
            out[r]+=(np.abs(w)>0.5).reshape(W,N).sum(1)/(N*N)
    return out
def rom_bitmap(fi,bo,it,code,pt):
    "Exactly the ROM's pixels, in the same way rom._render produces them, for any point size."
    G=geom(pt,fi); px,a=G['px'],G['a']; W,H=G['W'],G['H']
    from PIL import Image,ImageDraw
    ch=rom.cp1252(code); sub=rom._src(fi,bo,it,ch)
    f=rom.font(fi,bo,it,px,sub); a2,_=rom.font(fi,bo,it,px).getmetrics()
    im=Image.new('L',(W,H),0); ImageDraw.Draw(im).text((2,a2),ch,font=f,fill=255,anchor='ls')
    v=np.asarray(im,dtype=float); return np.round(v*15/255)/15
def build(name,faces,codes,**kw):
    t=time.time(); g=gn.GlyphNet(faces,codes,**kw); st=g.save(f'{OUT}/{name}.bin.gz'); st['build_s']=round(time.time()-t,1)
    st['per']={f'{k[0]},{k[1]}':v for k,v in g.per.items()}
    json.dump(st,open(f'{OUT}/{name}.json','w')); return st
def count_engine():
    p=ROOT+'/build/engine_count.wasm'
    if not os.path.exists(p): subprocess.check_call(f'clang -DCOUNT --target=wasm32 -O3 -nostdlib -mbulk-memory -msimd128 -Wl,--no-entry -Wl,-z,stack-size=1048576 -o {p} {ROOT}/host/engine.c',shell=True)
    return p
def run(name,draws,count=False):
    "Runs the draws on the real engine. Returns [(H x W coverage rows)], per draw counters, ms."
    o=f'{OUT}/{name}.{os.getpid()}.out'; rq=o+'.req'
    json.dump(dict(net=f'{OUT}/{name}.bin.gz',draws=draws,out=o,engine=count_engine() if count else ROOT+'/build/engine.wasm'),open(rq,'w'))
    subprocess.check_call(['node','test/glyphnet_run.js',rq],cwd=ROOT)
    a=np.fromfile(o,dtype=np.float32); r=json.load(open(o+'.json'))
    res=[]
    for d,x in zip(draws,r['res']):
        res.append(a[x['a']:x['a']+d['rows']*d['cells']].reshape(d['rows'],d['cells']).astype(float))
    os.remove(o);os.remove(o+'.json');os.remove(rq)
    return res,r['res'],r['ms']
def draw(code,face,pt,snap=(0,0),fi=0,**kw):
    G=geom(pt,fi)
    return dict(ch=code,face=face,s=G['px'],y0=G['a'],rows=G['rows'],cells=G['W'],snapy=snap[0],snapx=snap[1],large=0 if G['small'] else 1,**kw)
def pad(r,G):
    o=np.zeros((G['H'],G['W'])); o[:r.shape[0],:r.shape[1]]=r[:G['H'],:G['W']]; return o
