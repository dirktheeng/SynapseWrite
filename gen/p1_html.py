# ---- p1: the clipboard as HTML, both ways ----
# Copy: after the in-app copy has filled CB (text), CBS (style cells) and CBP (paragraph records), the network writes an HTML
# twin of the selection through the shared byte emitter into P1HB: a <p> per paragraph with its alignment, a <span> per change
# of run format with bold, italic, underline, size in points, color and font family, and text with < > & escaped.
# The glue hands it to the browser as text/html beside the plain text, without reading it.
# Paste: when the browser's clipboard has HTML, the glue puts its code units in P1HB and their count in the event. The network
# scans it like the .docx reader scans XML, with an eight cell window: block tags make paragraphs (text-align is read), inline
# tags and style attributes set run properties through the reader's own run property write (T2_C) and its color and font
# name rules, a stack in P1ST restores the format at a closing tag, entities and white space are read as a browser shows them,
# and comments, style, script, head and title are skipped. A paste of the network's own copy keeps taking the exact in-app path.
_gph=net.cur[0]; net.group('clipboard html')
# ===== copy: the writer =====
on('P1_HW0',(None,'P1_HWm',{embase:as_x(P1HB),fp:0,p1hi:0,p1hk:0,p1hs:0,p1ho:0,p1lo:0,p1nk:0}))
lit('P1_HWm',b'<meta charset="utf-8">','P1_HP')
e=S('P1_HP'); on('P1_HP',(net.ge(p1hi,wn,e),'P1_HZ',None),(net.gt(fp,P1HMAX-400,e),'P1_HAB',None),(net.ge(p1hk,csk,e),'P1_HPl',{r1:as_x(PT)+hi_p}),(None,'P1_HP1',{r1:as_x(CBP)+p1hk*8+6,r2:as_x(CBP)+p1hk*8+7,p1j:0}))
# the last paragraph of a selection has no mark in the copy: its alignment and list are read from the document
on('P1_HPl',(None,'P1_HP1',{r1:R1+ALIGN,r2:R1+LIST,p1j:1}))
e=S('P1_HP1'); _p1hasr=net.or_(net.lt(p1hk,csk,e),p1j); _p1lb=net.bits(R2,2+4,e)
on('P1_HP1',(None,'P1_HL',{p1al:G_(R1,_p1hasr),p1nk:G_(_p1lb[0]+_p1lb[1]*2,_p1hasr)}))
# a list paragraph is an item of a <ul> or <ol>, opened and closed as the kind changes
e=S('P1_HL'); _p1cl=net.and_(net.step(p1lo),ONE-net.eq(p1lo,p1nk,e))
on('P1_HL',(net.and_(_p1cl,net.eq(p1lo,1,e)),'P1_HLcu',{p1lo:0}),(net.and_(_p1cl,net.eq(p1lo,2,e)),'P1_HLco',{p1lo:0}),(None,'P1_HL1',None))
lit('P1_HLcu',b'</ul>','P1_HL1'); lit('P1_HLco',b'</ol>','P1_HL1')
e=S('P1_HL1'); _p1op=net.and_(net.step(p1nk),ONE-net.eq(p1lo,p1nk,e))
on('P1_HL1',(net.and_(_p1op,net.eq(p1nk,1,e)),'P1_HLou',{p1lo:1}),(net.and_(_p1op,net.eq(p1nk,2,e)),'P1_HLoo',{p1lo:2}),(None,'P1_HL2',None))
lit('P1_HLou',b'<ul style="margin:0">','P1_HL2'); lit('P1_HLoo',b'<ol style="margin:0">','P1_HL2')
on('P1_HL2',(net.step(p1nk),'P1_HLi',None),(None,'P1_HLp',None)); lit('P1_HLi',b'<li','P1_HA'); lit('P1_HLp',b'<p','P1_HA')
e=S('P1_HA'); on('P1_HA',*[(net.eq(p1al,v_,e),'P1_HPa%d'%v_,None) for v_ in (1,2,3)],(None,'P1_HPa0',None))
for v_,nm_ in ((0,None),(1,'center'),(2,'right'),(3,'justify')):
    lit('P1_HPa%d'%v_,(b' style="margin:0">' if nm_ is None else b' style="margin:0;text-align:%s">'%nm_.encode()),'P1_HC')
e=S('P1_HC'); on('P1_HC',(net.ge(p1hi,wn,e),'P1_HZ0',None),(net.gt(fp,P1HMAX-400,e),'P1_HAB',None),(None,'P1_HC1',{r1:as_x(CB)+p1hi,r2:as_x(CBS)+p1hi}))
e=S('P1_HC1'); on('P1_HC1',(net.eq(R1,10,e),'P1_HN',{p1hi:p1hi+1}),(net.eq(R2+1,p1hs,e),'P1_HE',{p1hc:R1}),(None,'P1_HX',{p1hc:R1,p1hs:R2+1,rs:as_x(CBS)+p1hi}))
on('P1_HN',(p1ho,'P1_HNs',None),(None,'P1_HNq',None)); lit('P1_HNs',b'</span>','P1_HNq')
on('P1_HNq',(net.step(p1nk),'P1_HNl',None),(None,'P1_HNp',None)); lit('P1_HNl',b'</li>','P1_HN1'); lit('P1_HNp',b'</p>','P1_HN1')
on('P1_HN1',(None,'P1_HP',{p1hk:p1hk+1,p1hs:0,p1ho:0}))
# a new run format: decode the style read by rs, close the open span, open one
e=S('P1_HX'); _p1D=style_decode(RSR,e); _p1szh=net.decode(_p1D['si'],rom.NSZ,e)
on('P1_HX',(p1ho,'P1_HXc',{p1fb:_p1D['bold'],p1fi:_p1D['ital'],p1fu:_p1D['und'],p1fp:sum((h_*rom.SZ[i_] for i_,h_ in enumerate(_p1szh)),X()),p1fc:_p1D['color'],p1fk:RSK,p1fn:RSN,p1ff:_p1D['font']}),
 (None,'P1_HY',{p1fb:_p1D['bold'],p1fi:_p1D['ital'],p1fu:_p1D['und'],p1fp:sum((h_*rom.SZ[i_] for i_,h_ in enumerate(_p1szh)),X()),p1fc:_p1D['color'],p1fk:RSK,p1fn:RSN,p1ff:_p1D['font']}))
lit('P1_HXc',b'</span>','P1_HY'); lit('P1_HY',b'<span style="','P1_S1')
on('P1_S1',(p1fb,'P1_S1t',None),(None,'P1_S2',None)); lit('P1_S1t',b'font-weight:bold;','P1_S2')
on('P1_S2',(p1fi,'P1_S2t',None),(None,'P1_S3',None)); lit('P1_S2t',b'font-style:italic;','P1_S3')
on('P1_S3',(p1fu,'P1_S3t',None),(None,'P1_S4',None)); lit('P1_S3t',b'text-decoration:underline;','P1_S4')
lit('P1_S4',b'font-size:','P1_S4n'); vnum('P1_S4n',p1fp,'P1_S4z'); lit('P1_S4z',b'pt;','P1_S5')
_p1pct=[('color:#%02X%02X%02X;'%PAL_F[j]).encode() for j in range(32)]; _p1pcb=rom_str(b''.join(_p1pct)); _p1pcl=len(_p1pct[0])
on('P1_S5',(net.step(p1fk),'P1_S5k',None),(net.step(p1fc),'A10_L0',{la_:as_x(_p1pcb)+p1fc*_p1pcl,ln_lit:_p1pcl,lret.r:lret.id('P1_S6')}),(None,'P1_S6',None))
lit('P1_S5k',b'color:#','P1_S5h')
e=S('P1_S5h'); _p1kb=net.bits(p1fk-1,24,e); _p1nb=[_p1kb[20-4*j_]+_p1kb[21-4*j_]*2+_p1kb[22-4*j_]*4+_p1kb[23-4*j_]*8 for j_ in range(6)]
on('P1_S5h',(None,'P1_S5d0',{v4nb[j_]:_p1nb[j_] for j_ in range(6)}))
for j_ in range(6):
    e=S(f'P1_S5d{j_}'); em_en.lin(e); em_b.add(e,48+v4nb[j_]+net.ge(v4nb[j_],10,e)*7); on(f'P1_S5d{j_}',(None,f'P1_S5d{j_+1}' if j_<5 else 'P1_S5z',None))
lit('P1_S5z',b';','P1_S6')
e=S('P1_S6'); _p1fh=net.decode(p1ff,len(rom.FAM_NAMES),e)
on('P1_S6',(net.step(p1fn),'P1_S6n',None),*[(_p1fh[j_],f'P1_S6f{j_}',None) for j_ in range(len(rom.FAM_NAMES))],(None,'P1_S7',None))
for j_,n_ in enumerate(rom.FAM_NAMES): lit(f'P1_S6f{j_}',("font-family:'%s';"%(rom.FAM_ALIAS[j_] or n_)).encode(),'P1_S7')
lit('P1_S6n',b"font-family:'",'P1_S6m'); on('P1_S6m',(None,'T2SS',{t2w:as_x(FNT)+(p1fn+FNSD)*32,t2sr.r:t2sr.id('P1_S6z')})); lit('P1_S6z',b"';",'P1_S7')
lit('P1_S7',b'">','P1_HO'); on('P1_HO',(None,'P1_HE',{p1ho:1}))
# one character, escaped
e=S('P1_HE'); _p1lt=net.eq(p1hc,60,e); _p1gt=net.eq(p1hc,62,e); _p1am=net.eq(p1hc,38,e); _p1br=net.eq(p1hc,11,e); _p1raw=net.and_(e,ONE-_p1lt,ONE-_p1gt,ONE-_p1am,ONE-_p1br)
em_en.lin(_p1raw); em_b.add(_p1raw,p1hc)
on('P1_HE',(_p1lt,'P1_HElt',{p1hi:p1hi+1}),(_p1gt,'P1_HEgt',{p1hi:p1hi+1}),(_p1am,'P1_HEam',{p1hi:p1hi+1}),(_p1br,'P1_HEbr',{p1hi:p1hi+1}),(None,'P1_HC',{p1hi:p1hi+1}))
lit('P1_HElt',b'&lt;','P1_HC'); lit('P1_HEgt',b'&gt;','P1_HC'); lit('P1_HEam',b'&amp;','P1_HC'); lit('P1_HEbr',b'<br>','P1_HC')
on('P1_HZ0',(p1ho,'P1_HNs2',None),(None,'P1_HZq',None)); lit('P1_HNs2',b'</span>','P1_HZq')
on('P1_HZq',(net.step(p1nk),'P1_HZl',None),(None,'P1_HZp',None)); lit('P1_HZl',b'</li>','P1_HZ'); lit('P1_HZp',b'</p>','P1_HZ')
e=S('P1_HZ'); on('P1_HZ',(net.eq(p1lo,1,e),'P1_HZcu',{p1lo:0}),(net.eq(p1lo,2,e),'P1_HZco',{p1lo:0}),(None,'P1_HZE',None)); lit('P1_HZcu',b'</ul>','P1_HZE'); lit('P1_HZco',b'</ol>','P1_HZE')
on('P1_HZE',(None,'IMP3_CSX',{p1hl:fp+1,embase:SAVEB}))
on('P1_HAB',(None,'IMP3_CSX',{p1hl:0,embase:SAVEB}))     # too long for the region: the copy goes as plain text only
# ===== paste: the reader =====
e=S('P1_HQ'); on('P1_HQ',(net.step(evb),'P1_R0',None),(None,'PS2',{pi_:0,pfm:0}))
on('P1_R0',(None,'P1_R1',{obase:as_x(P1HB),oi:0,p1rn:evb,p1hm:1,p1pt:net.step(co),p1pb:0,p1sp:ONE-net.step(co),p1d:0,p1pc:0,p1lk:0,p1li:0,ics:(ty,ity.k,ity.n,ity.y,*ity.e)}))
e=S('P1_R1'); on('P1_R1',(net.ge(oi,p1rn,e),'P1_RZ',None),(None,'P1_R2',{rl:OA+oi}))
e=S('P1_R2'); _p1lt=net.eq(W[0],60,e); _p1ws=net.or_(net.eq(W[0],32,e),net.eq(W[0],9,e),net.eq(W[0],10,e),net.eq(W[0],13,e))
def LP(*ss): return net.or_(*[lpat(s_,e) for s_ in ss])
_blk_o=['<p>','<p ','<div','<li','<h1','<h2','<h3','<h4','<h5','<h6','<tr','<blockq','<pre','<table']
_blk_c=['</p>','</div','</li','</h1','</h2','</h3','</h4','</h5','</h6','</tr','</block','</pre','</td','</th']
_in_b=['<b>','<b ','<strong']; _in_i=['<i>','<i ','<em>','<em ']; _in_u=['<u>','<u ','<ins>','<ins ']; _in_s=['<s>','<s ','<strike','<del>','<del ']
_in_o=['<span','<font','<a ','<a>','<sup','<sub','<small','<big','<code','<mark','<cite','<label']
_in_c=['</b>','</stro','</i>','</em>','</u>','</ins>','</s>','</strik','</del>','</span','</font','</a>','</sup','</sub','</small','</big','</code','</mark','</cite','</label']
on('P1_R2',(net.and_(_p1lt,lpat('<!--',e)),'P1_SKC',{oi:oi+4}),
 (net.and_(_p1lt,LP('<style','<STYLE')),'P1_SKT',{p1sk:1,oi:oi+6}),(net.and_(_p1lt,LP('<script','<SCRIPT')),'P1_SKT',{p1sk:2,oi:oi+7}),
 (net.and_(_p1lt,LP('<head','<HEAD')),'P1_SKT',{p1sk:3,oi:oi+5}),(net.and_(_p1lt,LP('<title','<TITLE')),'P1_SKT',{p1sk:4,oi:oi+6}),
 (net.and_(_p1lt,LP('<ul','<UL')),'P1_TG',{p1lk:1,oi:oi+3}),(net.and_(_p1lt,LP('<ol','<OL')),'P1_TG',{p1lk:2,oi:oi+3}),
 (net.and_(_p1lt,LP('</ul','</ol','</UL','</OL')),'P1_TG',{p1lk:0,p1pb:1,p1sp:1,oi:oi+4}),
 (net.and_(_p1lt,LP('<li','<LI')),'P1_BO',{p1li:1,oi:oi+3}),(net.and_(_p1lt,LP(*_blk_o)),'P1_BO',{p1li:0,oi:oi+2}),(net.and_(_p1lt,LP(*_blk_c)),'P1_TG',{p1pb:1,p1sp:1,oi:oi+2}),
 (net.and_(_p1lt,LP('<br','<BR')),'P1_BR',{p1ch:11,oi:oi+3}),
 (net.and_(_p1lt,LP(*_in_b)),'P1_IO',{p1vk:1,oi:oi+2}),(net.and_(_p1lt,LP(*_in_i)),'P1_IO',{p1vk:2,oi:oi+2}),(net.and_(_p1lt,LP(*_in_u)),'P1_IO',{p1vk:3,oi:oi+2}),
 (net.and_(_p1lt,LP(*_in_s)),'P1_IO',{p1vk:4,oi:oi+2}),(net.and_(_p1lt,LP(*_in_o)),'P1_IO',{p1vk:0,oi:oi+2}),
 (net.and_(_p1lt,LP(*_in_c)),'P1_IC',{oi:oi+2}),
 (_p1lt,'P1_TG',{oi:oi+1}),
 (lpat('&amp;',e),'P1_TX',{p1ch:38,oi:oi+5}),(lpat('&lt;',e),'P1_TX',{p1ch:60,oi:oi+4}),(lpat('&gt;',e),'P1_TX',{p1ch:62,oi:oi+4}),
 (lpat('&nbsp;',e),'P1_TX',{p1ch:160,oi:oi+6}),(lpat('&quot;',e),'P1_TX',{p1ch:34,oi:oi+6}),(lpat('&#39;',e),'P1_TX',{p1ch:39,oi:oi+5}),(lpat('&#160;',e),'P1_TX',{p1ch:160,oi:oi+6}),
 (net.and_(_p1ws,p1sp),'P1_R1',{oi:oi+1}),(_p1ws,'P1_TX',{p1ch:32,oi:oi+1}),
 (None,'P1_TX',{p1ch:W[0],oi:oi+1}))
# text: a pending paragraph break goes in first; then the character in the run format, through the input code map
e=S('P1_TX'); on('P1_TX',(net.and_(p1pb,p1pt),'SPLIT',{p1pb:0,p1pt:0,oret.r:oret.id('P1_TX2')}),(None,'P1_TX2',{p1pb:0}))
e=S('P1_TX2'); um_en.lin(e); um_in.add(e,p1ch)
on('P1_TX2',(net.ge(clen,1000,e),'P1_R1',None),(net.step(um_out),'INS',{ins_ch:um_out,ins_st:csi+trk*ST_INS,p1pt:1,p1sp:net.eq(p1ch,32,e),oret.r:oret.id('P1_R1')}),(None,'P1_R1',None))
on('P1_BR',(None,'P1_BR2',None)); e=S('P1_BR2'); um_en.lin(e); um_in.add(e,p1ch)
on('P1_BR2',(net.ge(clen,1000,e),'P1_TG',None),(None,'INS',{ins_ch:11,ins_st:csi+trk*ST_INS,p1pt:1,p1sp:1,oret.r:oret.id('P1_TG')}))
# skip to the end of a tag, a comment, or an element whose text is not shown
on('P1_TG',(None,'P1_TG1',{rl:OA+oi}))
e=S('P1_TG1'); on('P1_TG1',(net.ge(oi,p1rn,e),'P1_RZ',None),(net.eq(W[0],62,e),'P1_R1',{oi:oi+1}),(None,'P1_TG',{oi:oi+1}))
on('P1_SKC',(None,'P1_SKC1',{rl:OA+oi}))
e=S('P1_SKC1'); on('P1_SKC1',(net.ge(oi,p1rn,e),'P1_RZ',None),(lpat('-->',e),'P1_R1',{oi:oi+3}),(None,'P1_SKC',{oi:oi+1}))
on('P1_SKT',(None,'P1_SKT1',{rl:OA+oi}))
e=S('P1_SKT1'); _p1end=net.or_(net.and_(net.eq(p1sk,1,e),LP('</style','</STYLE')),net.and_(net.eq(p1sk,2,e),LP('</scrip','</SCRIP')),net.and_(net.eq(p1sk,3,e),LP('</head','</HEAD')),net.and_(net.eq(p1sk,4,e),LP('</title','</TITLE')))
on('P1_SKT1',(net.ge(oi,p1rn,e),'P1_RZ',None),(_p1end,'P1_TG',{oi:oi+2}),(None,'P1_SKT',{oi:oi+1}))
# a block: a paragraph break if this paragraph already has text, then its attributes (text-align)
e=S('P1_BO'); on('P1_BO',(p1pt,'SPLIT',{p1pt:0,p1pb:0,p1sp:1,p1al:0,oret.r:oret.id('P1_AW')}),(None,'P1_AW',{p1pb:0,p1sp:1,p1al:0}))   # a block with no text-align is left aligned
on('P1_BA',(None,'P1_BA1',{rl:OA+oi}))
e=S('P1_BA1'); on('P1_BA1',(net.ge(oi,p1rn,e),'P1_RZ',None),(net.eq(W[0],62,e),'P1_R1',{oi:oi+1}),(lpat('text-ali',e),'P1_AL',{oi:oi+10}),(None,'P1_BA',{oi:oi+1}))
on('P1_AL',(None,'P1_AL1',{rl:OA+oi}))
e=S('P1_AL1'); _p1sk=net.or_(net.eq(W[0],58,e),net.eq(W[0],32,e))
on('P1_AL1',(_p1sk,'P1_AL',{oi:oi+1}),(lpat('center',e),'P1_AW',{p1al:1}),(lpat('right',e),'P1_AW',{p1al:2}),(lpat('justify',e),'P1_AW',{p1al:3}),(lpat('left',e),'P1_AW',{p1al:0}),(None,'P1_BA',None))
on('P1_AW',(None,'P1_AW2',{r1:cb+ALIGN}))
e=S('P1_AW2'); log(e,6,cp,ALIGN,R1,p1al)
on('P1_AW2',(None,'P1_LW',{w1:(cb+ALIGN,p1al),w2:(cb+DIRTY,1)}))
# a list item takes the list kind (1 bullets, 2 numbers) at the first level; any other block is not in a list
on('P1_LW',(None,'P1_LW2',{r1:cb+LIST})); e=S('P1_LW2'); _p1lv=G_(p1lk,p1li); log(e,6,cp,LIST,R1,_p1lv)
on('P1_LW2',(None,'P1_BA',{w1:(cb+LIST,_p1lv),w2:(cb+DIRTY,1)}))
# an inline tag: push the run format, set what the tag means, then read its attributes
_p1push={wln:(as_x(P1ST)+p1d*8,cs,ics.k,ics.n,ics.y,ics.e[0],ics.e[1]),w1:(as_x(P1ST)+p1d*8+6,ics.e[2]),p1d:net.min_(p1d+1,31)}
e=S('P1_IO'); on('P1_IO',(net.eq(p1vk,1,e),'T2_C',{**_p1push,t2k:0,t2v:1}),(net.eq(p1vk,2,e),'T2_C',{**_p1push,t2k:1,t2v:1}),(net.eq(p1vk,3,e),'T2_C',{**_p1push,t2k:2,t2v:1}),(net.eq(p1vk,4,e),'T2_C',{**_p1push,t2k:4,t2v:1}),(None,'P1_IA',_p1push))
on('P1_HR',(None,'P1_IA',None))     # back from the run property write
e=S('P1_IC'); on('P1_IC',(net.step(p1d),'P1_IC1',{rl:as_x(P1ST)+p1d*8-8,p1d:p1d-1}),(None,'P1_TG',None))
on('P1_IC1',(None,'P1_TG',{ics:tuple(W[i_] for i_ in range(7))}))
# attributes of an inline tag: style properties and the old font attributes
on('P1_IA',(None,'P1_IA1',{rl:OA+oi}))
e=S('P1_IA1'); _p1nd=ONE-net.eq(p1pc,45,e)
on('P1_IA1',(net.ge(oi,p1rn,e),'P1_RZ',None),(net.eq(W[0],62,e),'P1_R1',{oi:oi+1}),
 (lpat('font-wei',e),'P1_V0',{p1vk:1,oi:oi+11}),(lpat('font-sty',e),'P1_V0',{p1vk:2,oi:oi+10}),(lpat('text-dec',e),'P1_V0',{p1vk:3,oi:oi+15}),
 (lpat('font-siz',e),'P1_V0',{p1vk:4,oi:oi+9}),(net.and_(_p1nd,lpat('color',e)),'P1_V0',{p1vk:5,oi:oi+5}),(lpat('font-fam',e),'P1_V0',{p1vk:6,oi:oi+11}),
 (lpat('face=',e),'P1_V0',{p1vk:6,oi:oi+4}),(None,'P1_IA',{oi:oi+1,p1pc:W[0]}))
on('P1_V0',(None,'P1_V1',{rl:OA+oi}))
e=S('P1_V1'); _p1sk=net.or_(*[net.eq(W[0],c_,e) for c_ in (58,32,34,39,61)])
_p1dg=net.and_(net.ge(W[0],48,e),net.lt(W[0],58,e)); _p1vk=net.decode(p1vk,7,e)
on('P1_V1',(_p1sk,'P1_V0',{oi:oi+1}),(net.and_(_p1vk[3],lpat('-line',e)),'P1_V0',{oi:oi+5}),
 (net.and_(_p1vk[1],net.or_(lpat('bold',e),net.and_(_p1dg,net.ge(W[0],54,e)))),'T2_C',{t2k:0,t2v:1}),(net.and_(_p1vk[1],net.or_(lpat('normal',e),lpat('lighter',e),_p1dg)),'T2_C',{t2k:0,t2v:0}),
 (net.and_(_p1vk[2],net.or_(lpat('italic',e),lpat('oblique',e))),'T2_C',{t2k:1,t2v:1}),(net.and_(_p1vk[2],lpat('normal',e)),'T2_C',{t2k:1,t2v:0}),
 (net.and_(_p1vk[3],lpat('underlin',e)),'T2_C',{t2k:2,t2v:1}),(net.and_(_p1vk[3],lpat('line-thr',e)),'T2_C',{t2k:4,t2v:1}),(net.and_(_p1vk[3],lpat('none',e)),'T2_C',{t2k:2,t2v:0}),
 (net.and_(_p1vk[4],_p1dg),'P1_NZ',{p1nv:0,p1nf:0,p1nd:0}),
 (net.and_(_p1vk[5],net.eq(W[0],35,e)),'P1_CH',{oi:oi+1}),(net.and_(_p1vk[5],lpat('rgb(',e)),'P1_RG',{oi:oi+4,p1rk:0,p1nv:0}),
 (_p1vk[6],'P1_FN',{p1j:0}),
 (None,'P1_IA',None))
# a size: digits, an optional fraction, then pt or px, to half points and the reader's size table
on('P1_NZ',(None,'P1_NZ1',{rl:OA+oi}))
e=S('P1_NZ1'); _p1dg=net.and_(net.ge(W[0],48,e),net.lt(W[0],58,e))
_p1hpt=p1nv*2+net.ge(p1nf,5,e); _p1hpx=floorv(p1nv*1.5+p1nf*0.15+0.5,e); _p1px=lpat('px',e)
_p1hp=net.min_(G_(_p1hpx,_p1px)+G_(_p1hpt,e-_p1px),as_x(199))
on('P1_NZ1',(net.and_(_p1dg,net.eq(p1nd,0,e)),'P1_NZ',{p1nv:p1nv*10+W[0]-48,oi:oi+1}),(net.and_(_p1dg,net.eq(p1nd,1,e)),'P1_NZ',{p1nf:W[0]-48,p1nd:2,oi:oi+1}),(_p1dg,'P1_NZ',{oi:oi+1}),
 (net.eq(W[0],46,e),'P1_NZ',{p1nd:1,oi:oi+1}),(net.or_(lpat('pt',e),_p1px),'A10_SZ',{r1:as_x(_stab)+net.relu(_p1hp+1),oi:oi+2}),(None,'P1_IA',None))
# a color: #rrggbb through the reader's own color rule, or rgb(r, g, b)
on('P1_CH',(None,'P1_CH1',{rl:OA+oi})); on('P1_CH1',(None,'CO0',None))
on('P1_RG',(None,'P1_RG1',{rl:OA+oi}))
e=S('P1_RG1'); _p1dg=net.and_(net.ge(W[0],48,e),net.lt(W[0],58,e)); _p1sep=net.or_(net.eq(W[0],44,e),net.eq(W[0],41,e)); _p1rk=net.decode(p1rk,3,e)
on('P1_RG1',(_p1dg,'P1_RG',{p1nv:p1nv*10+W[0]-48,oi:oi+1}),(net.and_(_p1sep,_p1rk[2]),'P1_RG2',{p1c[2]:net.min_(p1nv,as_x(255)),oi:oi+1}),
 (_p1sep,'P1_RG',{**{p1c[j_]:G_(net.min_(p1nv,as_x(255)),_p1rk[j_])+G_(p1c[j_],e-_p1rk[j_]) for j_ in range(2)},p1rk:p1rk+1,p1nv:0,oi:oi+1}),(net.ge(oi,p1rn,e),'P1_RZ',None),(None,'P1_RG',{oi:oi+1}))
e=S('P1_RG2'); _p1q=[floorv(p1c[j_]*(1.0/32),e,nb=4) for j_ in range(3)]
on('P1_RG2',(None,'A10_CO',{r1:as_x(_ctab)+_p1q[0]*64+_p1q[1]*8+_p1q[2],t2kx:p1c[0]*65536+p1c[1]*256+p1c[2]+1}))
# a font family: the first name, unquoted, into the typed font name buffer, then the reader's name rules
on('P1_FN',(None,'P1_FN1',{rl:OA+oi}))
e=S('P1_FN1'); _p1q=net.or_(net.eq(W[0],34,e),net.eq(W[0],39,e)); _p1endc=net.or_(*[net.eq(W[0],c_,e) for c_ in (44,59,34,39,38,62)])
on('P1_FN1',(net.and_(net.eq(p1j,0,e),lpat('&quot;',e)),'P1_FN',{oi:oi+6}),(net.and_(net.eq(p1j,0,e),net.or_(_p1q,net.eq(W[0],32,e))),'P1_FN',{oi:oi+1}),
 (net.or_(_p1endc,net.ge(p1j,30,e)),'P1_FN2',{wln:(as_x(FTB)+p1j,34,34,34,34,34,34)}),(None,'P1_FN',{w1:(as_x(FTB)+p1j,W[0]),p1j:p1j+1,oi:oi+1}))
on('P1_FN2',(net.eq(p1j,0,S('P1_FN2')),'P1_IA',None),(None,'P1_FN3',{p1so:oi,p1fy:1,obase:as_x(FTB),oi:0,rl:as_x(FTB)}))
on('P1_FN3',(None,'RF9',{rl:as_x(FTB)}))
on('P1_RZ',(None,'AFTER_ED',{obase:as_x(OUTB),p1hm:0}))
net.group(_gph)
