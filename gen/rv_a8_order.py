"""Neuron numbering. The engine needs only a topological numbering with registers first, so the numbering is free to
serve locality: a neuron goes as close as possible after the neuron made before it, so a subnetwork stays together in
memory and targets are near their sources. No search: one pass over the graph with a heap keyed on creation order."""
import heapq
def order(s,mode='kahn'):
    n=len(s.act); dom=getattr(s,'dom',[0]*n); super_={}; 
    for g,ids in enumerate(s.aligned):
        for i in ids: super_[i]=ids[0]
    rep=lambda i:super_.get(i,i)
    alive=getattr(s,'alive',None) or [True]*n
    indeg={};cons={}
    for i in range(n):
        if not alive[i] or s.kind[i]=='reg': continue
        r=rep(i); indeg.setdefault(r,0)
        for j,_ in s.inp[i]:
            if s.kind[j]=='reg' or not alive[j]: continue
            q=rep(j)
            if q==r: continue
            cons.setdefault(q,[]).append(r); indeg[r]+=1
    members={}
    for ids in s.aligned:
        members[ids[0]]=ids
    h=[r for r,d in indeg.items() if d==0]; heapq.heapify(h); comb=[]
    while h:
        r=heapq.heappop(h)
        comb+=members.get(r,[r])
        for c in cons.get(r,()):
            indeg[c]-=1
            if indeg[c]==0: heapq.heappush(h,c)
    assert len(comb)==sum(1 for i in range(n) if alive[i] and s.kind[i]!='reg'),'cycle through an aligned group'
    regs=[i for i in range(n) if alive[i] and s.kind[i]=='reg']
    idxs=[];lstart=[0]
    for d in sorted(set(dom)):
        idxs+=[i for i in regs if dom[i]==d]; lstart.append(len(idxs))
        idxs+=[i for i in comb if dom[i]==d]; lstart.append(len(idxs))
    return idxs,lstart
