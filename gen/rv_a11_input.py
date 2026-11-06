# ---- raw event interpretation ----
# The glue sends what the browser delivered: key name code units, modifier bits, field text, pointer type.
# This layer decides what each one means and either re-enters the cooked dispatch or halts at once.
# Raw kinds: 2 with a nonzero key length (key), 21 pointer, 22 mouse move, 23 mouse enter, 24 click,
# 25 touch start, 26 touch move, 27 field text. A direct kind 2 with no key vector is an already cooked key.
# Commands back to the glue are read on the halting tick, like the clipboard and save commands.
net.group('raw event interpretation')
a11k=R();a11kh=R();a11kl=R();a11ty=R();a11ln=R(KBSEN);a11vn=R();a11i=R();a11nb=R();a11comp=R()
a11pass=R();a11ff=R();a11fb=R();a11hold=R();a11chold=R();a11kbo=R(KBSEN+1)
# the name of a key reaches the network as code units; four coordinates separate the names it knows
_kh=kv[0]+kv[1]*128+kv[5]*16384+kvl*2097152
def _khash(s): return ord(s[0])+ord(s[1])*128+(ord(s[5]) if len(s)>5 else 0)*16384+len(s)*2097152
KEYNAMES={'Backspace':8,'Tab':9,'Enter':13,'Escape':27,'Delete':127,'ArrowLeft':128,'ArrowUp':129,'ArrowRight':130,'ArrowDown':131,'Home':132,'End':133,'PageUp':134,'PageDown':135}
assert len({_khash(s) for s in KEYNAMES})==len(KEYNAMES)
_cook={evk:ev_kind,eva:ev_a,evb:ev_b,evc:ev_c,evt:ev_t}
on('IDLE',(net.step(kvl),'A11_R',{a11k:1,eva:kv[0],evb:ev_b,evc:ev_c,evt:ev_t,a11kh:_kh,a11kl:kvl}),
 (net.step(ev_kind-19.5),'A11_R',{a11k:ev_kind-19,eva:ev_a,evb:ev_b,evc:ev_c,evt:ev_t}),
 (net.step(ev_kind),'DISP',_cook))
fsm.states['IDLE'][0]; net.init[next(iter(S('IDLE').t))]=1.0
e=S('A11_R'); _rk=net.decode(a11k,9,e); _t=net.ge(evc,1,e)
on('A11_R',(_rk[1],'A11_K',None),(_rk[2],'A11_P',None),
 (_rk[3],'DISP',{evk:G_(5,_t)+G_(11,ONE-_t),a11hold:_t,evc:0}),
 (net.and_(_rk[4],net.or_(_t,mp_ptr_lock)),'A11_HF',None),(_rk[4],'DISP',{evk:11,evc:0}),
 (_rk[5],'A11_HF',{a11ff:mp_ptr_lock}),
 (_rk[6],'A11_HF',{a11ty:G_(eva+1,net.eq(evb,1,e))}),
 (_rk[7],'A11_TM',None),
 (net.and_(_rk[8],net.eq(eva,1,e)),'A11_HF',{a11comp:1}),
 (_rk[8],'A11_T0',{a11vn:evc,a11i:0,a11busy:1,a11comp:G_(a11comp,ONE-net.eq(eva,2,e))}),
 (None,'A11_HF',None))
# keys: a single unit is a character, folded to lower case under Ctrl or Cmd; a longer name goes through the table
e=S('A11_K'); _mb=net.bits(evb,4,e); _cm=net.or_(_mb[0],_mb[2]); _one=net.eq(a11kl,1,e)
_kc=G_(eva,_one)+net.and_(_cm,_one,net.ge(eva,65,e),net.lt(eva,91,e))*32
for s_,c_ in KEYNAMES.items(): _kc=_kc+net.eq(a11kh,_khash(s_),e)*c_
_kcm=_cm+_mb[1]*2
_isv=net.and_(_cm,net.eq(_kc,118,e)); _isc=net.and_(_cm,net.or_(net.eq(_kc,99,e),net.eq(_kc,120,e)))
on('A11_K',(ONE-net.step(_kc),'A11_HF',{a11pass:1}),
 # Ctrl+V and Ctrl+C or X leave the browser to fire paste, copy or cut; Ctrl+V first moves focus to the field, where some browsers require it
 (_isv,'A11_HF',{a11pass:1,a11ff:net.and_(e,ONE-_mb[3],ONE-mp_ptr_lock),a11fb:net.and_(e,ONE-_mb[3],ONE-mp_ptr_lock)}),
 (_isc,'DISP',{evk:2,eva:_kc,evb:_kcm,a11pass:1,a11chold:1}),
 (None,'DISP',{evk:2,eva:_kc,evb:_kcm}))
# pointer type: t means touch, m means mouse. Touch hides the drawn pointer and locks it until a real mouse returns.
e=S('A11_P'); _pt=net.eq(eva,116,e); _pm=net.eq(eva,109,e)
on('A11_P',(net.and_(_pt,net.eq(evb,0,e),ONE-mp_ptr_lock),'DISP',{evk:12,eva:1,evb:0}),
 (net.and_(_pm,mp_ptr_lock),'DISP',{evk:12,eva:2,evb:0}),(None,'A11_HF',None))
# touch drag: the difference from the last y becomes a wheel event, limited to 900 per event. a11ty holds y+1, 0 when not tracking.
e=S('A11_TM'); _tv=net.and_(net.ge(a11ty,1,e),net.eq(evb,1,e)); _tu=a11ty-1-eva
_tc=as_x(1000)+net.min_(net.relu(_tu),900)-net.min_(net.relu(-_tu),900)
on('A11_TM',(ONE-_tv,'A11_HF',{a11pass:1}),(net.eq(a11ty,eva+1,e),'A11_HF',None),(None,'DISP',{evk:6,eva:0,evb:0,evc:_tc,a11ty:eva+1}))
# hidden field text: compare with the last text, then replay as backspaces and characters through the key path.
# HALT comes back to A11_T3 while busy, so each key is a full edit in one dispatch.
e=S('A11_T0')
on('A11_T0',(net.or_(net.ge(a11i,a11vn,e),net.ge(a11i,a11ln,e)),'A11_T2',None),(None,'A11_T1',{r1:as_x(KBV)+a11i,r2:as_x(KBL)+a11i}))
e=S('A11_T1'); on('A11_T1',(net.eq(R1,R2,e),'A11_T0',{a11i:a11i+1}),(None,'A11_T2',None))
on('A11_T2',(None,'A11_T3',{a11nb:net.relu(a11ln-a11i)}))
e=S('A11_T3')
on('A11_T3',(net.ge(a11nb,1,e),'DISP',{evk:2,eva:8,evb:0,evc:0,a11nb:a11nb-1}),(net.lt(a11i,a11vn,e),'A11_T4',{r1:as_x(KBV)+a11i}),(None,'A11_T5',None))
e=S('A11_T4'); _ch=R1+net.eq(R1,10,e)*3; _kk={evk:2,eva:_ch,evb:0,evc:0,a11i:a11i+1}
on('A11_T4',(a11comp,'DISP',{**_kk,w1:(as_x(KBL)+a11i,R1)}),(None,'DISP',_kk))
# while composing the field text is kept for the next diff; otherwise the field returns to its sentinel
on('A11_T5',(a11comp,'HALT',{a11ln:a11vn,a11busy:0}),(None,'A11_T6',{rb:(as_x(KBQ),KBSEN)}))
on('A11_T6',(None,'HALT',{wb:(as_x(KBL),KBSEN),a11ln:KBSEN,a11busy:0,a11kbo:KBSEN+1}))
on('A11_HF',(None,'IDLE',None)); halt.lin(S('A11_HF'))
# commands, valid on the tick that halts
_HS=S('HF')+S('T1_HF')+S('A11_HF')
def _a11cmd(r):
    b=Bus(net); b.add(_HS,r); fsm.set(r,_HS,0); return b
c_pass=_a11cmd(a11pass);c_ff=_a11cmd(a11ff);c_fb=_a11cmd(a11fb);c_hold=_a11cmd(a11hold);c_chold=_a11cmd(a11chold);c_kbo=_a11cmd(a11kbo)
