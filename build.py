import base64
import os
d=os.path.dirname(os.path.abspath(__file__))+'/'
import glob
_lic=sorted(glob.glob(d+'fonts/*/package/LICENSE'))
_crs='\n'.join(open(f_,encoding='utf-8').read().split('\n\n')[0].split(' Carlito-')[0].split(' Caladea-')[0].split(' Arimo-')[0].split(' Tinos-')[0].split(' Cousine-')[0].split(' OpenSans-')[0] for f_ in _lic)
_ofl=open(_lic[0],encoding='utf-8').read().split('\n\n',1)[1]
NOTICE=('The weights of this page are written from these fonts:\n'+_crs+'\n\n'+_ofl).replace('--','- -')
g=open(d+'build/net.bin.gz','rb').read();w=open(d+'build/engine.wasm','rb').read();j=open(d+'host/glue.js').read()
html=f'''<!doctype html><!--{NOTICE}--><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SynapseWrite Editor</title>
<style>:root{{--bg:#333}}html,body{{margin:0;height:100%;background:var(--bg)}}canvas{{display:block;margin:auto;max-width:100%;cursor:none;outline:none}}#kb{{position:fixed;left:0;top:0;width:1px;height:1px;opacity:0;font-size:16px;border:0;padding:0;resize:none}}canvas{{touch-action:pinch-zoom}}</style></head>
<body><canvas id="screen" width="1280" height="800" tabindex="0"></canvas><textarea id="kb" aria-label="Keyboard input" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false"></textarea>
<script>window.ENG_B64="{base64.b64encode(w).decode()}";window.NET_B64="{base64.b64encode(g).decode()}";</script><script>{j}</script></body></html>'''
open(d+'build/index.html','w').write(html);print(len(html))
