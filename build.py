import base64
import os
d=os.path.dirname(os.path.abspath(__file__))+'/'
g=open(d+'build/net.bin.gz','rb').read();w=open(d+'build/engine.wasm','rb').read();j=open(d+'host/glue.js').read()
html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SynapseWrite Editor</title>
<style>:root{{--bg:#333}}html,body{{margin:0;height:100%;background:var(--bg)}}canvas{{display:block;margin:auto;max-width:100%;cursor:text;outline:none}}</style></head>
<body><canvas id="screen" width="1280" height="800" tabindex="0"></canvas>
<script>window.ENG_B64="{base64.b64encode(w).decode()}";window.NET_B64="{base64.b64encode(g).decode()}";</script><script>{j}</script></body></html>'''
open(d+'build/index.html','w').write(html);print(len(html))
