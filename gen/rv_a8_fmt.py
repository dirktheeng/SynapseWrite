"""Weight file body. Every section is a stream of small integers so gzip sees repeating patterns and the raw size stays small.
Each integer is base 128, low digits first. The engine decodes these streams once, in finish().
A neuron's first target is stored relative to the previous neuron's first target, since neighbours feed neighbours; later
targets as gaps. Lazy sources are relative to the reader, with one bit for pull. Weights and biases are table indices."""
import numpy as np,collections
def leb(a):
    o=bytearray(); ap=o.append
    for v in a:
        while v>=128: ap(v&127|128); v>>=7
        ap(v)
    return bytes(o)
def zig(v): return (v<<1) if v>=0 else ((-v)<<1)-1
def encode(c,pr):
    n=c['n']; osz=[];first=[];rest=[];wv=[];prev=0
    isz=[];isv=[];iv=[]
    for i in range(n):
        o=sorted(c['out'][i]); osz.append(len(o))
        if o:
            first.append(zig(o[0][0]-prev)); prev=o[0][0]
            rest.extend(o[k+1][0]-o[k][0] for k in range(len(o)-1))
            wv.extend(w for _,w in o)
        l=c['lazy'][i]; isz.append(len(l))
        for s,w in l:
            pull=s<0; a=~s if pull else s
            isv.append(zig(i-a)*2+pull); iv.append(w)
    wc=collections.Counter(wv)+collections.Counter(iv)
    wtab=sorted(wc,key=lambda w:(-wc[w],w)); wix={w:k for k,w in enumerate(wtab)}
    bc=collections.Counter(c['bias']); btab=sorted(bc,key=lambda w:(-bc[w],w)); bix={w:k for k,w in enumerate(btab)}
    body=b''.join([leb(osz),leb(first),leb(rest),leb([wix[w] for w in wv]),leb(isz),leb(isv),leb([wix[w] for w in iv]),
        bytes(c['act']),leb([bix[b] for b in c['bias']]),leb(c['lstart']),np.array(pr,dtype=np.int32).tobytes(),np.array(wtab,dtype=np.float64).tobytes(),np.array(btab,dtype=np.float64).tobytes()])
    return body,dict(zn=len(body),nt=len(wtab),nb=len(btab),e=len(wv),ni=len(iv))
