"""Removes neurons that compute nothing of use before numbering. Same function, fewer neurons.
Duplicates: two combinational neurons with the same activation, bias and inputs have the same output at every tick, so
consumers read one of them. Dead: a neuron no port, glue read or named register depends on is dropped."""
def prune(s,precs,named=()):
    from nn import X
    import sys
    n=len(s.act); roots=set(getattr(s,'keep',())); roots.add(s.ONE_id); roots.update(s.init); roots.update(named)
    if hasattr(s,'ONE1'): roots.add(s.ONE1)
    for ids in s.aligned: roots.update(ids)
    def walk(q):
        if isinstance(q,X): roots.update(q.t)
        elif isinstance(q,(list,tuple)):
            for z in q: walk(z)
    for r in precs: walk(r)
    for r in precs:          # read port cells are written by the port
        if r[0]==2: b=next(iter(r[3].t)); roots.update(range(b,b+r[4]))
        if r[0]==5: b=next(iter(r[3].t)); roots.update(range(b,b+4))
    s.port_en={next(iter(r[1].t)) for r in precs if isinstance(r[1],X) and len(r[1].t)==1}
    agg=[None]*n
    for i in range(n):
        a={}
        for j,w in s.inp[i]: a[j]=a.get(j,0)+w
        agg[i]={j:w for j,w in a.items() if w!=0}
    rep=list(range(n)); dom=getattr(s,'dom',[0]*n); ndup=0; bool_in=getattr(s,'bool_in',set())
    import os
    zero=set()               # a closed gate whose enables cancelled once duplicates merged: it can never open
    while not os.environ.get('NODUP'):
        seen={}; c=0
        for pass_ in (0,1):      # roots first, so a duplicate resolves to the neuron that has to stay
            for i in range(n):
                if s.kind[i]!='comb' or rep[i]!=i or (i in roots)!=(pass_==0): continue
                a={}
                for j,w in agg[i].items(): a[rep[j]]=a.get(rep[j],0)+w
                if i not in zero and s.act[i]!=0 and s.bias[i]<=-2.0**39 and not any(w>=2.0**39 for j,w in a.items() if j not in zero): zero.add(i); c+=1; continue
                k=(s.act[i],s.bias[i],dom[i],tuple(sorted(a.items())))
                o=seen.get(k)
                if o is None: seen[k]=i
                elif i not in roots: rep[i]=o; c+=1
        ndup+=c
        if not c: break
    for i in range(n):
        if rep[i]!=rep[rep[i]]: rep[i]=rep[rep[i]]
    for i in range(n):
        if i in zero: s.inp[i]=[]; s.bias[i]=0.0
        else: s.inp[i]=[(rep[j],w) for j,w in s.inp[i] if rep[j] not in zero]
    print('never open',len(zero),file=sys.stderr)
    alive=[False]*n; st=list(roots)
    for i in st: alive[i]=True
    while st:
        for j,_ in s.inp[st.pop()]:
            if not alive[j]: alive[j]=True; st.append(j)
    for i in range(n):
        if not alive[i]: s.inp[i]=[]
    s.alive=alive
    print('duplicates',ndup,'dead',n-sum(alive),file=sys.stderr)
    return rep
