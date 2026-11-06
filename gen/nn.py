"""Weight generator primitives. Every weight is written directly from reasoning about
what the neuron must compute. There is no loss, gradient, data set, or search here."""
ID,STEP,RELU=0,1,2
M=float(2**40)
class X:
    """Lazy linear expression over neurons. Linear maps fold into the next real neuron."""
    __slots__=('t','c')
    def __init__(s,t=None,c=0.0): s.t=t or {}; s.c=float(c)
    def __add__(s,o):
        o=as_x(o); t=dict(s.t)
        for k,w in o.t.items():
            t[k]=t.get(k,0)+w
            if t[k]==0: del t[k]
        return X(t,s.c+o.c)
    __radd__=__add__
    def __neg__(s): return X({k:-w for k,w in s.t.items()},-s.c)
    def __sub__(s,o): return s+(-as_x(o))
    def __rsub__(s,o): return as_x(o)-s
    def __mul__(s,k):
        if k==0: return X()
        return X({n:w*k for n,w in s.t.items()},s.c*k)
    __rmul__=__mul__
    def is_const(s): return not s.t
def as_x(o): return o if isinstance(o,X) else X(c=o)

class Net:
    def __init__(s):
        s.act=[];s.bias=[];s.inp=[];s.kind=[];s.init={};s.names={};s.ports=[];s.groups={};s.cur=['core'];s.aligned=[]
        s.ONE_id=s._new(ID,0,'reg'); s.init[s.ONE_id]=1.0; s.inp[s.ONE_id].append((s.ONE_id,1.0)); s.ONE=X({s.ONE_id:1.0})
    def _new(s,a,b,kind='comb'):
        s.act.append(a);s.bias.append(b);s.inp.append([]);s.kind.append(kind)
        s.groups.setdefault(s.cur[0],[]).append(len(s.act)-1); return len(s.act)-1
    def group(s,name): s.cur[0]=name
    def _feed(s,i,e):
        e=as_x(e)
        for k,w in e.t.items(): s.inp[i].append((k,w))
        return e.c
    def _node(s,a,e):
        e=as_x(e)
        if a!=ID and s.ONE_id in e.t:   # the constant neuron folds into the bias
            t=dict(e.t); w=t.pop(s.ONE_id); e=X(t,e.c+w)
        i=s._new(a,0.0); c=s._feed(i,e)
        if a==ID:
            if c: s.inp[i].append((s.ONE_id,c))
        elif c>0: s.inp[i].append((s.ONE_id,c))
        else: s.bias[i]=c
        return X({i:1.0})
    def relu(s,e): return s._node(RELU,e)
    def step(s,e): return s._node(STEP,e)
    def wire(s): return X({s._new(ID,0.0):1.0})
    def connect(s,w,e):
        i=next(iter(w.t)); c=s._feed(i,e)
        if c: s.inp[i].append((s.ONE_id,c))
    def input(s,n=1):
        a=[s._new(ID,0.0,'reg') for _ in range(n)]
        return [X({i:1.0}) for i in a] if n>1 else X({a[0]:1.0})
    def reg(s,init=0.0):
        i=s._new(ID,0.0,'reg')
        if init: s.init[i]=float(init)
        return X({i:1.0})
    def rec(s,r,e):
        """Recurrent connection: e(t) feeds register r(t+1)."""
        i=next(iter(r.t)); e=as_x(e); c=e.c
        for k,w in e.t.items(): s.inp[i].append((k,w))
        if c: s.inp[i].append((s.ONE_id,c))
    def gate(s,val,en):
        val=as_x(val);en=as_x(en)
        if val.is_const(): return en*val.c
        return s.relu(val+en*M-M)
    def and_(s,*a):
        e=X(c=-(len(a)-1))
        for x in a: e=e+x
        r=s.step(e)
        # An AND's inputs are 0 or 1 by construction, so any of them may wake it.
        s.bool_in=getattr(s,'bool_in',set()); s.bool_in.add(next(iter(r.t)))
        s.and_args=getattr(s,'and_args',[]); s.and_args.append((next(iter(r.t)),a))   # only read by the debug table
        return r
    def or_(s,*a):
        e=X()
        for x in a: e=e+x
        return s.step(e)
    def ge(s,a,b,en):
        """Integer a>=b when en is 1, otherwise 0."""
        return s.step(as_x(a)-b+0.5+as_x(en)*M-M)
    def gt(s,a,b,en): return s.ge(a,as_x(b)+1,en)
    def lt(s,a,b,en): return s.ge(b,as_x(a)+1,en)
    def eq(s,a,b,en): return s.and_(s.ge(a,b,en),s.ge(b,a,en))
    def max_(s,a,b): return as_x(b)+s.relu(as_x(a)-b)
    def min_(s,a,b): return as_x(a)-s.relu(as_x(a)-b)
    def decode(s,val,n,en,hot=False):
        """One-hot layer. A gate neuron first zeroes the value, so no threshold neuron
        is visited unless the decoder is enabled. hot=True adds a true one-hot neuron so
        a wide fan-out is visited only for the single active line."""
        v=s.relu(as_x(val)+1+as_x(en)*M-M)
        g=[s.step(v-(i+1)+0.5) for i in range(n)]+[X()]
        if hot: return [s.step(g[i]-g[i+1]-0.5) for i in range(n)]
        return [g[i]-g[i+1] for i in range(n)]
    def decode_z(s,val,n,en):
        """Decoder for values that are nearly always zero: a zero value visits one neuron only."""
        v=as_x(val); nz=s.step(v); e2=s.and_(en,nz); h=s.decode(v,n,e2); z=s.and_(en,X({s.ONE_id:1.0})-nz)
        return [z]+h[1:]
    def decode2(s,val,n,en):
        """Two level one-hot decoder: value to two nibble digits, then an AND per line. Few visits per use."""
        b=s.bits(val,8,en)
        lo=s.decode(b[0]+b[1]*2+b[2]*4+b[3]*8,16,en); hi=s.decode(b[4]+b[5]*2+b[6]*4+b[7]*8,16,en)
        return [s.step(hi[i>>4]+lo[i&15]-1.5) for i in range(n)]
    def bits(s,val,nb,en):
        """Binary digits by descending thresholds. Returns low-to-high bits."""
        rem=s.gate(val,en);out=[None]*nb
        for k in reversed(range(nb)):
            b=s.step(rem-2**k+0.5); out[k]=b; rem=rem-b*(2**k)
        return out
    # ---- compile ----
    def compile(s):
        n=len(s.act); layer=[-1]*n; state=[0]*n
        import sys; sys.setrecursionlimit(1000000)
        order=[]
        for root in range(n):
            if state[root]: continue
            stack=[(root,0)]
            while stack:
                i,idx=stack.pop()
                if idx==0:
                    if state[i]: continue
                    state[i]=1
                if s.kind[i]=='reg': layer[i]=0; state[i]=2; continue
                adv=False; ins=s.inp[i]
                while idx<len(ins):
                    j=ins[idx][0]; idx+=1
                    if state[j]==0: stack.append((i,idx)); stack.append((j,0)); adv=True; break
                    if state[j]==1:
                        names={n_:k_ for k_,v_ in s.groups.items() for n_ in v_}
                        chain=[x_[0] for x_ in stack]+[i,j]
                        k0=chain.index(j)
                        raise Exception('combinational loop at neuron %d: %s'%(i,[(q,names.get(q),s.act[q],round(s.bias[q],1),[(a_,round(b_,2)) for a_,b_ in s.inp[q]][:5]) for q in chain[k0:]]))
                if adv: continue
                layer[i]=1+max([layer[j] for j,_ in ins],default=0); state[i]=2
        L=max(layer)+1
        key=[(0,i) for i in range(n)]
        for g,ids in enumerate(s.aligned):
            ml=max(layer[i] for i in ids)
            for p,i in enumerate(ids): layer[i]=ml; key[i]=(g+1,p)
        L=max(layer)+1
        idxs=sorted(range(n),key=lambda i:(layer[i],key[i])); new=[0]*n
        for a,i in enumerate(idxs): new[i]=a
        lstart=[0]*(L+1)
        for i in range(n): lstart[layer[i]+1]+=1
        for l in range(L): lstart[l+1]+=lstart[l]
        out=[[] for _ in range(n)]; lazy=[[] for _ in range(n)]
        # Evaluation modes. Every one computes the same function as visiting all inputs.
        # gated: with the enable off the output is zero whatever the values are, so the value
        #   inputs are read only after the enable fires.
        # trigger: if one input being zero already forces the output to zero, only that input
        #   needs to wake the neuron and the others are read after it does.
        # pull: a neuron all of whose consumers read it lazily computes only when read.
        # sticky: a register whose only activity is holding itself keeps its value in place.
        keep=set(getattr(s,'keep',()));
        for ids in s.aligned: keep.update(ids)
        boolreg=getattr(s,'boolreg',set())
        INF=float('inf')
        def bounds(j):
            if s.act[j]==STEP or j in boolreg: return 0.0,1.0
            if s.act[j]==RELU: return 0.0,INF
            return -INF,INF
        ins=[]; push=[None]*n; npush=[0]*n; nread=[0]*n; trig={}
        for i in range(n):
            agg={}
            for j,w in s.inp[i]: agg[j]=agg.get(j,0)+w
            agg={j:w for j,w in agg.items() if w!=0}
            ins.append(agg)
            if s.kind[i]=='reg': P=set(agg)
            else:
                P=set(agg)
                if s.act[i] in (STEP,RELU):
                    ctl=[j for j,w in agg.items() if abs(w)>=M/2]
                    if s.bias[i]<=-M/2 and ctl: P=set(ctl)
                    else:
                        tops=[]; boolin=i in getattr(s,'bool_in',())
                        for j,w in agg.items():
                            lo_,hi_=(0.0,1.0) if boolin and s.kind[j]=='reg' else bounds(j)
                            tops.append(w*(hi_ if w>0 else lo_))
                        ninf=sum(1 for t in tops if t==INF); tot=s.bias[i]+sum(t for t in tops if t!=INF)
                        best=None
                        if boolin:
                            for j in agg:
                                if s.kind[j]=='reg' and j not in boolreg and j!=s.ONE_id: s.bool_regs_seen=getattr(s,'bool_regs_seen',set())|{j}
                        for (j,w),t in zip(agg.items(),tops):
                            if w<=0: continue
                            rest=(tot-t) if t!=INF else tot
                            if (ninf-(t==INF))==0 and rest<=1e-12:
                                rank=(0 if j in boolreg else 1 if s.act[j]==STEP else 2)
                                if best is None or rank<best[0]: best=(rank,j)
                        if best: P={best[1]}; trig[i]=best[1]
            push[i]=P
            for j in agg:
                if j in P: npush[j]+=1
                else: nread[j]+=1
        pull=[False]*n; work=[i for i in range(n)]
        PULLMAX=getattr(s,'pullmax',12)
        while work:
            i=work.pop()
            if pull[i] or npush[i] or s.kind[i]=='reg' or i in keep or len(ins[i])>PULLMAX: continue
            pull[i]=True
            for j in push[i]:
                npush[j]-=1; nread[j]+=1
                if not npush[j]: work.append(j)
            push[i]=set()
        act=list(s.act); nsticky=0
        for i in range(n):
            if s.kind[i]=='reg' and ins[i].get(i)==1.0 and npush[i]==1:
                push[i].discard(i); del ins[i][i]; act[i]=3; nsticky+=1
        for i in range(n):
            rd=[]
            for j,w in ins[i].items():
                if j in push[i]: out[new[j]].append((new[i],w))
                else: rd.append((abs(w),~new[j] if pull[j] else new[j],w))
            rd.sort(key=lambda q:-q[0])
            if pull[i] and i in trig:     # read the input that decides first; zero ends the evaluation
                t_=trig[i]; rd=[q for q in rd if abs(q[1] if q[1]>=0 else ~q[1])==new[t_]]+[q for q in rd if abs(q[1] if q[1]>=0 else ~q[1])!=new[t_]]
                act[i]=act[i]|4
            lazy[new[i]]=[(q[1],q[2]) for q in rd]
        import sys as _s
        print('pull',sum(pull),'sticky',nsticky,file=_s.stderr)
        s.pullv=[pull[i] for i in idxs]
        return dict(lazy=lazy,n=n,L=L,new=new,lstart=lstart,out=out,act=[act[i] for i in idxs],bias=[s.bias[i] for i in idxs],layer=layer)

class Bus:
    """A shared vector signal. Each source is gated by the condition that selects it."""
    def __init__(s,net): s.net=net; s.w=net.wire()
    def add(s,cond,val): s.net.connect(s.w,s.net.gate(val,cond))
    def lin(s,e): s.net.connect(s.w,e)

class FSM:
    """Control registers whose next values are gated sums over one-hot state neurons."""
    def __init__(s,net): s.net=net; s.states={}; s.assign={}
    def state(s,name,init=0):
        if name not in s.states:
            s.states[name]=[s.net.reg(init),[]]
            if not hasattr(s.net,'boolreg'): s.net.boolreg=set()
            s.net.boolreg.add(next(iter(s.states[name][0].t)))
        return s.states[name][0]
    def S(s,name): return s.state(name)
    def set(s,r,cond,val):
        k=next(iter(r.t)); s.assign.setdefault(k,[r,[]])[1].append((cond,as_x(val)))
    def on(s,name,*rules):
        """rules: (cond or None, next state name, {target:value}). First true rule wins."""
        net=s.net; st=s.state(name); rem=st
        s.seen_on=getattr(s,'seen_on',set())
        assert name not in s.seen_on, 'state defined twice: '+name
        s.seen_on.add(name)
        for cond,nxt,acts in rules:
            c=rem if cond is None else net.and_(rem,cond)
            if cond is not None: rem=rem-c
            s.states[name][1].append((c,nxt))
            for tgt,val in (acts or {}).items(): s.apply(tgt,c,val)
    def apply(s,t,c,val):
        if isinstance(t,Bus): t.add(c,val)
        elif isinstance(t,X): s.set(t,c,val)
        else: t.drive(c,val)
    def finish(s):
        net=s.net
        for name,(r,outs) in s.states.items():
            e=r
            for c,_ in outs: e=e-c
            net.rec(r,e)
        # Optional trap: a level that steers the token out of a set of states. Any cycle holds an edge to a state of
        # equal or lower index, so guarding those edges (and edges leaving the set) is enough to catch every loop.
        guard=set(); trap=getattr(s,'trap',None)
        if trap is not None:
            idx={n_:i_ for i_,n_ in enumerate(s.states)}; bar=set(s.trap_bar); reach=set(); st_=list(s.trap_roots)
            while st_:
                q_=st_.pop()
                if q_ in reach or q_ in bar: continue
                reach.add(q_)
                st_+=[nx for _,nx in s.states[q_][1] if nx is not None]
            for q_ in reach:
                for _,nx in s.states[q_][1]:
                    if nx is not None and (idx[nx]<=idx[q_] or nx in bar) and nx not in ('OPEND','HALT','T3_PF'): guard.add((q_,nx))
            print('trap reach',len(reach),'guarded edges',len(guard),file=__import__('sys').stderr)
        for name,(r,outs) in s.states.items():
            for c,nxt in outs:
                if nxt is None: continue
                if (name,nxt) in guard:
                    k_=net.and_(c,trap); net.rec(s.state(nxt),c-k_); net.rec(s.state(s.trap_to),k_)
                else: net.rec(s.state(nxt),c)
        for k,(r,lst) in s.assign.items():
            anyc=X()
            for c,_ in lst: anyc=anyc+c
            e=r-net.relu(r+anyc*M-M)
            for c,v in lst: e=e+net.gate(v,c)
            net.rec(r,e)
