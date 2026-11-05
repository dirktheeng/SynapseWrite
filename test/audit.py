# Architecture audit: glue size, forbidden APIs, training code, provenance.
import re,glob,json,os
import os
d=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
glue=open(d+'host/glue.js').read(); eng=open(d+'host/engine.c').read(); r=[]
for api in ['fillText','strokeText','fillRect','drawImage','innerHTML','style.','FontFace','measureText','<div','<span']:
    r.append((f'glue does not use {api}',api not in glue))
r.append(('one display call only: putImageData',glue.count('putImageData')==1))
r.append(('glue branches on no document text: no charCode comparison',not re.search(r"bb\[[^\]]*\]\s*(==|===|<|>)",glue)))
bad=re.compile(r'\b(backward|autograd|optimizer|adam|sgd|loss\s*=|gradient\s*=|torch|tensorflow|keras|fit\(|train\()\b',re.I)
hits=[]
for f in glob.glob(d+'gen/*.py')+glob.glob(d+'host/*'):
    src=open(f).read()
    for ln,l in enumerate(src.split('\n'),1):
        if bad.search(l) and 'no loss' not in l: hits.append((f,ln,l.strip()))
r.append(('no training code in generator or host',not hits))
p=json.load(open(d+'build/provenance.json'))
for n,ok in r: print('PASS' if ok else 'FAIL',n)
print('hits',hits)
print('glue.js lines',glue.count('\n'),'bytes',len(glue),'| engine.c lines',eng.count('\n'))
print(json.dumps(p,indent=0)[:900])
