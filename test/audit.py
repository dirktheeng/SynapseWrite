# Architecture audit. Fails (exit 1) unless glue and engine hold the rules: glue only runs inference,
# encodes events and bytes, displays tensors and executes commands. Every check is an exact allow list,
# so anything new must be argued for here. Usage: python3 test/audit.py [--glue file] [--engine file]
import re,glob,json,os,sys
d=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
def arg(n,dflt): return sys.argv[sys.argv.index(n)+1] if n in sys.argv else dflt
glue=open(arg('--glue',d+'host/glue.js')).read(); eng=open(arg('--engine',d+'host/engine.c')).read(); r=[]
def ok(name,cond,detail=''): r.append((name,cond,detail))
code=re.sub(r'^\s*//.*$','',glue,flags=re.M)
# ---- display and page building ----
for api in ['fillText','strokeText','fillRect','drawImage','innerHTML','style.','FontFace','measureText','<div','<span','outerHTML','insertAdjacent','appendChild','classList']:
    ok(f'glue does not use {api}',api not in code)
ok('one display call only: putImageData',code.count('putImageData')==1)
tags=sorted(re.findall(r"createElement\('([^']*)'\)",code))
ok('createElement: exactly one file input and one download anchor',tags==['a','input'],tags)
ok('every createElement is a literal tag',code.count('createElement')==len(tags))
# ---- glue must not parse or interpret text ----
for api in ['toLowerCase','toUpperCase','localeCompare','.slice(','.split(','.match(','.replace(','.indexOf(','.includes(','.substr','.trim(','.startsWith','.endsWith','RegExp','.at(','codePointAt','normalize(','.test(','switch','.key===','.key==','.keyCode','.which','.code']:
    ok(f'glue does not use {api}',api not in code)
ok('glue branches on no bank cell',not re.search(r"(bb|bank\(\))\[[^\]]*\]\s*(==|!=|<|>)",code))
# every string in the glue is an event name, a host API name, or a page element id
STRS={'gzip','screen','2d','copy','text/plain','cut','input','file','downloads','a','dragover','drop','keydown','paste','mousedown','mouseup','mouseleave','mouseenter','mousemove','wheel','kb','compositionstart','compositionend','pointerdown','pointermove','click','touchstart','touchmove','text','k','t','e','','eng','net','contextmenu','utf-16le','synapse_dict','[]',
      'text/html'}   # p1: the clipboard's HTML type, set from the network's HTML twin and read on paste as code units
found=set(re.findall(r"'([^'\n]*)'",code))
ok('every string literal is on the allow list (no key names, file names, sentinels, newlines)',found<=STRS,sorted(found-STRS))
# every condition in the glue, exactly. New ones must be added here and justified.
CONDS={'!ok':'clipboard fallback chain','dl':'host download service','dr[y]':'dirty row flag from the engine','dr[z]':'dirty row flag from the engine','pendClip!==null':'command state',
 'held':'network command','clip':'network command','!held':'network command','fl':'network command','e.val(h.wpic)':'network command','e.val(h.wopen)':'network command','kb':'network command',
 'e.val(h.ffield)':'network command','e.val(h.fback)':'network command','ms':'network command','wp':'network command','a':'skip zero inject','b':'skip zero inject','c':'skip zero inject',
 'ev.dataTransfer.files[0]':'host: a file was dropped','!e.val(h.pass_)':'network command','waiting':'host frame scheduling','e.val(h.hold)':'network command','!img||!img.data.length':'display image remade when memory growth detaches it','Uint8Array.fromBase64':'host: native base64','busy':'host: a slice is running','ds':'network command: save the dictionary','evm':'skip zero inject','m>=lim&&!window.annMax':'host: the slice ran out','nx':'host: queued event',
 'hm':'network command: the network wrote an HTML twin of the copy (its length plus one)','ph':'network command: there is an HTML twin to hand over (empty when the network wrote none)'}
ifs=[]
for m in re.finditer(r'\b(if|while)\(',code):
    i=m.end();dep=1
    while dep: dep+={'(':1,')':-1}.get(code[i],0);i+=1
    ifs.append(code[m.end():i-1])
ok('every if and while condition is on the allow list',set(ifs)<=set(CONDS),sorted(set(ifs)-set(CONDS)))
loops=set(re.sub(r'\s','',m) for m in re.findall(r'for\((?:let|const) \w+=[^;]*;([^;]*);',code))
ok('loops only walk tensors and the key vector',loops<={'y>=0','i<j','i<n','i<6','i<s.length','i<ds','i<fl','j--'},sorted(loops))
ok('logical or only guards host values',set(re.findall(r'[\w.\]\)]+\|\|[\w.\']+',code))<={"window.annMax||5000000","ev.key||''","i)||0",")||'"},re.findall(r'[\w.\]\)]+\|\|[\w.\']+',code))
ok('and only guards host values',set(re.findall(r'[\w.\[\]]+&&',code))<={'f.files[0]&&','g&&','lim&&'},re.findall(r'[\w.\[\]]+&&',code))
ok('state in glue is host scheduling and clipboard hand off only',set(re.findall(r'\blet (\w+)',code.replace('let i','').replace('let y','').replace('let z','')))<={'o','timer','dl','ok','s','waiting','img','evm','busy','n','x','j'},re.findall(r'\blet (\w+)',code))
nums={int(x) for x in re.findall(r'(?<![\w.#])\d{3,}(?![\w.])',code)}
ok('large numbers are only screen size, offsets of encodings and time',nums<={1280,800,801,864,1024000,8192,1000,5000000,256},sorted(nums))
_tern=re.findall(r'[^?\s]\?[^.?]',re.sub(r"'[^']*'",'',code))
ok('no ternary but the host download service and the base64 choice',len(_tern)<=1,_tern)
ok('event kinds in the glue are exactly the raw and cooked host kinds',set(re.findall(r'dispatch\((\d+)',code))=={'1','3','4','6','7','11','13','2','8','21','22','23','24','25','26','27'},sorted(set(re.findall(r'dispatch\((\d+)',code))))
ok('window.addEventListener handlers do not test event fields',not re.search(r'if\(ev\.(?!dataTransfer)',code))
ok('no literal comparison anywhere in glue',not re.search(r'(===|!==|==|!=)\s*(\d|\'|")',code),re.findall(r'.{15}(?:===|!==|==|!=)\s*[\d\'"].{5}',code))
# ---- engine: passive ports only ----
ports=eng[eng.index('static void write_port'):eng.index('static inline void run_ports')]
ok('engine port kinds are exactly 1 3 4 6, 8 call, 11 darkest patch, and reads 2 5 10',sorted(re.findall(r'case (\d+):',ports),key=int)==['1','3','4','6','8','11'],re.findall(r'case (\d+):',ports))
ok('engine has no special value for a clip',not re.search(r'y1==0',eng))
sh=re.findall(r'[\w\]\)]+\s*(?:>>|<<)\s*\w+',ports)
ok('engine ports unpack nothing: the only shifts split a patch index or a bank page',set(sh)<={'q>>2','unsigned)a>>16'},sh)
ok('engine has no color packing constants',not re.search(r'65535|<<16|[^)]>>16|<<8|>>8',ports))
lits=sorted({int(x) for x in re.findall(r'(?<![\w.])\d{2,}(?![\w.])',eng[eng.index('finish'):eng.index('static inline void run_ports')])})
ok('engine holds no character or key codes',not set(lits)&set(list(range(32,127))+[128,129,130,131,132,133,134,135]),lits)
ok('engine and glue size',eng.count('\n')<=150 and code.count('\n')<=85,(eng.count('\n'),code.count('\n')))
# ---- no training ----
bad=re.compile(r'\b(backward|autograd|optimizer|adam|sgd|loss\s*=|gradient\s*=|torch|tensorflow|keras|fit\(|train\(|np\.random|random\.|minimize|curve_fit|polyfit|lstsq|sklearn|scipy\.optimize)\b',re.I)
hits=[]
for f in glob.glob(d+'gen/*.py')+glob.glob(d+'host/*'):
    for ln,l in enumerate(open(f).read().split('\n'),1):
        if bad.search(l) and 'no loss' not in l: hits.append((f,ln,l.strip()[:100]))
ok('no training, fitting or randomness in generator or host',not hits,hits)
# ---- provenance ----
p=json.load(open(d+'build/provenance.json'));G=p['groups']
ok('no neuron falls into an unnamed core group',not any(k=='core' for k in G),G.get('core'))
ok('every neuron belongs to a named group',sum(v['neurons'] for v in G.values())==p['neurons'],(sum(v['neurons'] for v in G.values()),p['neurons']))
ok('every group has a purpose',all(v['purpose'] for v in G.values()),[k for k,v in G.items() if not v['purpose']])
ok('every neuron is traced to a generator file',all(sum(v['files'].values())==v['neurons'] for v in G.values()),[k for k,v in G.items() if sum(v['files'].values())!=v['neurons']])
ok('every generator file exists',all(os.path.exists(d+'gen/'+f) for v in G.values() for f in v['files']),[f for v in G.values() for f in v['files'] if not os.path.exists(d+'gen/'+f)])
md=open(d+'PROVENANCE.md').read()
ok('PROVENANCE.md lists every group and no gap',all('| '+k+' |' in md for k in G) and 'NO PURPOSE RECORDED' not in md)
ok('PROVENANCE.md is from this build',f"{p['neurons']} neurons" in md)
for n,c,x in r:
    if not c or '-v' in sys.argv: print('PASS' if c else 'FAIL',n,x if not c else '')
fails=sum(not c for _,c,_ in r)
print(f'audit: {len(r)-fails} of {len(r)} passed; glue {code.count(chr(10))} lines, {len(code)} bytes; engine {eng.count(chr(10))} lines; {len(G)} groups')
sys.exit(1 if fails else 0)
