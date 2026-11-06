# ---- spell check: the word list is minimized into a letter automaton written directly as weights ----
# One register per automaton node, one lazy gate per edge. A token moves along the edge
# selected by the current letter while the character is painted, so only the active
# node's outgoing gates are visited. Identical subtrees are merged, which is a pure
# function of the sorted word list: there is no fitting and no search over parameters.
_sp_group=net.cur[0]; net.group('spell dictionary')
CONTR="don't can't won't isn't aren't wasn't weren't hasn't haven't hadn't doesn't didn't shouldn't wouldn't couldn't mustn't needn't ain't shan't i'm i've i'll i'd you're you've you'll you'd he'll he'd she'll she'd it'll it'd we're we've we'll we'd they're they've they'll they'd o'clock".split()
def _sp_build():
    words=open('words_en.txt').read().split()+CONTR+[chr(c) for c in range(97,123)]
    trie={}
    for w in sorted(set(words)):
        n=trie
        for c in w: n=n.setdefault(c,{})
        n['$']={}
    ids={};nodes=[]
    stack=[(trie,False)];memo={}
    def key(n): return tuple(sorted((c,0 if c=='$' else memo[id(n[c])]) for c in n))
    while stack:
        n,done=stack.pop()
        if done:
            k=key(n)
            if k not in ids: ids[k]=len(nodes); nodes.append(k)
            memo[id(n)]=ids[k]
        else:
            stack.append((n,True))
            for c in n:
                if c!='$': stack.append((n[c],False))
    return nodes,memo[id(trie)]
_nodes,_root=_sp_build()
_LI={chr(97+i):i for i in range(26)}; _LI["'"]=26
sp_in=R();sp_dig=R();sp_pa=R();sp_ap=R();sp_x0=R();sp_xe=R();sp_r=R()
_ew=e+S('A6S_W')   # rv_a6: the suggestion walker drives the same letter wires
_lo=low0(R1,_ew)
sp_alpha=net.and_(net.ge(_lo,97,_ew),net.lt(_lo,123,_ew))
sp_hot=net.decode(_lo-97,26,sp_alpha,hot=True)
sp_nop=net.and_(e,SD['nop'])
sp_latin=net.or_(net.and_(net.ge(R1,192,e),ONE-net.eq(R1,215,e),ONE-net.eq(R1,247,e)),net.eq(R1,138,e),net.eq(R1,140,e),net.eq(R1,142,e),net.eq(R1,154,e),net.eq(R1,156,e),net.eq(R1,158,e),net.eq(R1,159,e))   # the word list is ASCII: a word with an accent is left unchecked
sp_digit=net.or_(net.and_(net.ge(R1,48,e),net.lt(R1,58,e)),net.and_(sp_nop,sp_alpha),sp_latin)
sp_apos=net.and_(net.or_(net.eq(R1,39,_ew),net.eq(R1,146,_ew)),sp_in)
sp_bnd=net.and_(e,ONE-sp_alpha,ONE-sp_digit,ONE-sp_apos)
sp_first=net.and_(sp_alpha,ONE-sp_in)
sp_acc=net.wire()
_tok=[net.reg() for _ in _nodes]
_MM=M
def _edge(src,letter,dst):
    h=sp_apos if letter==26 else sp_hot[letter]
    net.rec(_tok[dst],net.step(src*_MM+h-_MM-0.5))
for _i,_k in enumerate(_nodes):
    for _c,_d in _k:
        if _c=='$':
            if _i!=_root: net.connect(sp_acc,_tok[_i])
        elif _i==_root: _edge(sp_first,_LI[_c],_d)
        else: _edge(_tok[_i],_LI[_c],_d)
print('spell automaton nodes',len(_nodes),'edges',sum(len(k) for k in _nodes),file=sys.stderr)
net.group(_sp_group)
fsm.set(sp_in,net.or_(sp_alpha,sp_digit,sp_apos),1); fsm.set(sp_in,sp_bnd,0); fsm.set(sp_in,S('R8'),0)
fsm.set(sp_dig,sp_digit,1); fsm.set(sp_dig,sp_bnd,0); fsm.set(sp_dig,S('R8'),0)
fsm.set(sp_x0,sp_first,x)
a6oe=R();a6o0=R();a6sr=R();a6nr=R();a6mf=R();a6dm=R();a6dk=R();a6dl=R();a6di=R(); fsm.set(a6o0,sp_first,off)   # rv_a6
# an accepted word may be followed by an apostrophe and an optional s
fsm.set(sp_pa,sp_apos,sp_acc); fsm.set(sp_ap,sp_apos,1)
_alpha_nf=net.and_(sp_alpha,sp_in)
fsm.set(sp_pa,_alpha_nf,net.and_(sp_pa,sp_ap,net.step(sp_hot[18]))); fsm.set(sp_ap,_alpha_nf,0)
fsm.set(sp_pa,sp_bnd,0); fsm.set(sp_ap,sp_bnd,0); fsm.set(sp_pa,S('R8'),0); fsm.set(sp_ap,S('R8'),0)
sp_bad=net.step(sp_bnd+sp_in+sp_on-sp_acc-sp_pa-sp_dig-chere-2.5)
_e_ce=S('CE')
_ch2=net.and_(net.eq(pi,cp,_e_ce),net.eq(off,co,_e_ce))
sp_bad2=net.step(_e_ce+sp_in+sp_on-sp_acc-sp_pa-sp_dig-_ch2-2.5)
fsm.set(sp_in,net.and_(_e_ce,ONE-sp_bad2),0); fsm.set(sp_dig,_e_ce,0); fsm.set(sp_pa,_e_ce,0); fsm.set(sp_ap,_e_ce,0)
