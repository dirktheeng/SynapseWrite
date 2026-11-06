# ---- one window comparator ----
# The eight cell window is packed into two 32 bit words. Each word feeds one bank of sorted thresholds, and a pattern
# is a range between two thresholds, since a prefix is a range of the big endian word. A pattern over four characters
# is the AND of a range in each word. The pattern table is these weights. Every user ANDs the line with its own state.
_ws=net.wire(); _wen=net.step(_ws); _wes=set(); _wlines={}
_wg=[net.gate(sum((W[i+o]*(1<<(24-8*i)) for i in range(4)),X())+1,_wen) for o in (0,4)]
_wth=[{},{}]
def _wthr(b,v):
    if v>=1<<32: return X()
    if v not in _wth[b]: _wth[b][v]=net.step(_wg[b]-v-0.5)
    return _wth[b][v]
def _wrange(b,s):
    v=0
    for ch in s: v=v*256+ord(ch)
    span=256**(4-len(s)); v*=span
    return _wthr(b,v)-_wthr(b,v+span)
def pat(st,e,offs=0):
    assert offs in (0,4) and offs+len(st)<=8, st
    k=next(iter(e.t)) if len(e.t)==1 else None
    assert k is not None and e.t[k]==1, st
    if k not in _wes: _wes.add(k); net.connect(_ws,e)
    if (st,offs) not in _wlines:    # a bare wire here would have no known bound, and every rule reading it would be pushed
        _wlines[(st,offs)]=_wrange(1,st) if offs==4 else _wrange(0,st) if len(st)<=4 else net.and_(_wrange(0,st[:4]),_wrange(1,st[4:]))
    return _wlines[(st,offs)]
def tag(n,end): return sum((pat(n+q,e) for q in end),X())   # the lines exclude each other
tagA=tag
def pat_finish(): print('window comparator patterns',len(_wlines),'thresholds',len(_wth[0])+len(_wth[1]),file=sys.stderr)
