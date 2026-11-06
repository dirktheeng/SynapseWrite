"""Writes the README section that describes every sub-network. Counts come from build/provenance.json. Fails if a sub-network has no description."""
import json,sys,re
README,PROV=sys.argv[1:3];G=json.load(open(PROV))['groups']
from nets_data import F
seen=[n for _,_,r in F for n,_,_ in r];assert len(seen)==len(set(seen))
miss=set(G)-set(seen);extra=set(seen)-set(G);assert not miss and not extra,(miss,extra)
o=['<!-- networks:start -->','## Every sub-network, and why it exists','','The build traces each neuron to one of %d named sub-networks. This is the whole list, with neuron counts from the current build. Names are the exact labels in [`PROVENANCE.md`](PROVENANCE.md), and some keep working labels from when they were written (`a4`, `rv a3`, `tier 2`).'%len(G),'','<p align="center"><img src="docs/figures/network_path.svg" alt="Animated path of a key press through the sub-networks"></p>','']
for h,intro,r in F:
    tot=sum(G[n]['neurons'] for n,_,_ in r);o+=[f'### {h} ({tot:,} neurons)','',intro,'','| Sub-network | Neurons | What it does | Why it exists |','|---|---:|---|---|']
    for n,d,w in sorted(r,key=lambda x:-G[x[0]]['neurons']):o.append(f"| `{n}` | {G[n]['neurons']:,} | {d} | {w} |")
    o.append('')
o.append('<!-- networks:end -->')
sec='\n'.join(o)
s=open(README).read()
if '<!-- networks:start -->' in s:s=re.sub(r'<!-- networks:start -->.*<!-- networks:end -->',lambda m:sec,s,flags=re.S)
else:
    s=s.replace('## What is not the network',sec+'\n\n## What is not the network')
    s=s.replace('[Boundaries](#what-is-not-the-network)','[Every sub-network](#every-sub-network-and-why-it-exists) · [Boundaries](#what-is-not-the-network)')
open(README,'w').write(s)
print(len(F),'families',len(seen),'networks')
