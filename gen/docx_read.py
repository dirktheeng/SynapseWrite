
openout=Bus(net); openout.add(S('HF'),wopen); fsm.set(wopen,S('HF'),0)
iret=Ret('IR');bret=Ret('BR');gret=Ret('GR');hret=Ret('HR');cret=Ret('CR')
ip=R();cur=R();nb=R();bitv=R();gbn=R();gbv=R();gbw=R();gbi=R();ob=R();oi=R();zp=R();pfirst=R();cs=R();csi=R();ics=Interned(cs,csi);ntxt=R()
lln=R();bfinal=R();nlen=R();ndist=R();ncode=R();idx=R();prev=R();rept=R();rval=R();cval=R()
csd=None;code=R();first=R();index=R();hlen=R();cnt=R();hb=R();sym=R();ln=R();lb=R();lc_=R();sb=R();dist=R();copyn=R()
rins=R();rdel=R();rfk=R();rvb=R();rnop=R();rhi=rins*ST_INS+rdel*ST_DEL+rfk*ST_F0+rnop*ST_NOP
LN=TBL+1200; CLH=TBL+800; LH=TBL; DH=TBL+400; OFFS=TBL+1000
exec(open('t3_px.py').read())
exec(open('rv_a5_regs.py').read())
rtoc=R();rdig=R();tpgv=R();fnc=R();rdsec=R();gcount=R();tcidx=R();gx=R();incell=R()
exec(open('rv_a6_eqrd.py').read())
def T3_PX_RULES(e):
    return [(tag('<w:tbl',' >'),'PX',{gcount:0,tcidx:0,gx:0,pfirst:0,a5ts:0,oi:oi+6}),(pat('<w:gridC',e),'T3_GC',{oi:oi+8}),(tag('<w:tc',' >'),'T3_TC0',{oi:oi+5}),(pat('</w:tc>',e),'A5_TCE',{oi:oi+7}),(pat('</w:tr>',e),'A5_TRE',{oi:oi+7}),(net.and_(net.or_(a5tcp,net.and_(net.eq(ztarget,4,e),ONE-a5tp,ONE-incell)),pat('<w:shd ',e)),'T3_SHD',{oi:oi+7})]+T3_PX_MORE(e)
# open: reset the document, then walk zip members
t2cp=R();t2k=R();t2v=R();t2n_=R();t2cb0=R();t2skip=R();t2df=R();t2ps=R()
on('OP0',(None,'T3_OP',{**{q_:0 for q_ in falias},cursec:0,nsec:1,imgp:0,fnc:0,rdsec:0,rdp:0,hftp:0,hfl[0]:0,hfl[1]:0,hfl[2]:0,hfl[3]:0,rins:0,rdel:0,rfk:0,t2cb0:nextb,t2skip:0,t2ps:0,nsty:6,wln:(nextb+SAVE,112,16,1,0,0,0),w1:(as_x(PT),nextb),w2:(nextb+DIRTY,1),w3:(nextb+LEN,0),cp:0,cb:nextb,co:0,clen:0,ap:0,ao:0,npar:1,nextb:nextb+STRIDE,usp:UB,urp:UB,scroll:0,nolog:1,zp:0,pfirst:1,cs:0,ity:as_x(0),dfrom:0,lc:1,bgp:0}))
on('T3_OP',(None,'T3_OP2',None))
for i_,v_ in enumerate((1,816,PH,PX,TX,TW,96,864)):
    on('T3_OP2' if i_==0 else f'T3_OP2{i_}',(None,f'T3_OP2{i_+1}' if i_<7 else 'T2_OR0',{w1:(as_x(SECB)+i_,v_)}))
FA=as_x(FILE)
W=rl.out
exec(open('rv_a10_pat.py').read())
vdry=R();vusz=R();vob=R();ilim=R();oblim=R();ztarget=R();zp0=R();zk=R();ibase=R();obase=R(OUTB);mth=R();csz=R();nm=R();ext=R();cmt=R();loff=R()
# locate the end record by scanning back, then walk the central directory
on('OP1',(None,'ZE0',{zp:net.relu(evc-22)}))
on('ZE0',(None,'ZE1',{rl:FA+zp}))
e=S('ZE1')
sig=net.and_(net.eq(W[0],80,e),net.eq(W[1],75,e),net.eq(W[2],5,e),net.eq(W[3],6,e))
on('ZE1',(sig,'ZE2',{rl:FA+zp+16}),(net.eq(zp,0,e),'OPEND',None),(None,'ZE0',{zp:zp-1}))
on('ZE2',(None,'T3_Z0',{zp0:W[0]+W[1]*256+W[2]*65536}))
e=S('X_C0'); on('X_C0',(net.ge(zp,evc,e),'T3_ZN',None),(None,'X_C1',{rl:FA+zp}))
e=S('X_C1')
on('X_C1',(net.and_(net.eq(W[0],80,e),net.eq(W[1],75,e),net.eq(W[2],1,e),net.eq(W[3],2,e)),'C2',{rl:FA+zp+8}),(None,'T3_ZN',None))
on('C2',(None,'C3',{mth:W[2]+W[3]*256,rl:FA+zp+20}))
on('C3',(None,'C4',{csz:W[0]+W[1]*256+W[2]*65536,vusz:W[4]+W[5]*256+W[6]*65536+W[7]*16777216,rl:FA+zp+28}))
on('C4',(None,'C5',{nm:W[0]+W[1]*256,ext:W[2]+W[3]*256,cmt:W[4]+W[5]*256,rl:FA+zp+42}))
on('C5',(None,'C6',{loff:W[0]+W[1]*256+W[2]*65536,rl:FA+zp+46+nm-8}) if False else (None,'C5b',{loff:W[0]+W[1]*256+W[2]*65536}))
on('C5b',(net.ge(loff,evc,S('C5b')),'T3_ZN',None),(None,'C6',{rl:FA+zp+46+nm-8}))
e=S('C6')
ztg=net.decode(ztarget,9,e)
on('C6',(net.or_(net.and_(ztg[4],pat('ment.xml',e),net.eq(nm,17,e)),net.and_(ztg[1],pat('xml.rels',e),net.eq(nm,28,e)),net.and_(ztg[2],pat('otes.xml',e),net.eq(nm,18,e)),net.and_(ztg[3],pat('ents.xml',e),net.eq(nm,17,e)),net.and_(ztg[7],pat('yles.xml',e),net.eq(nm,15,e)),net.and_(ztg[6],pat('ring.xml',e),net.eq(nm,18,e)),net.and_(ztg[0],pat('eme1.xml',e)),net.and_(ztg[8],pat('otes.xml',e),net.eq(nm,17,e))),'C7',{rl:FA+loff+26}),(ztg[5],'T3_ZC',{zk:0}),(None,'X_C0',{zp:zp+46+nm+ext+cmt}))
on('C7',(None,'Z7',{ip:loff+30+W[0]+W[1]*256+W[2]+W[3]*256,ob:0,nb:0,cur:0}))
e=S('Z7')
_olim=X()
for b_,t_ in ((OUTB,IMG0),(AUXB,RELB),(RELB,CMB),(PNGB,AUXB),(OUTP,PNGB)): _olim=_olim+net.eq(obase,b_,e)*(t_-b_-1000)
on('Z7',(net.eq(mth,8,e),'BH',{ibase:FA,iret.r:iret.id('A12_S0'),ilim:evc,oblim:_olim}),(None,'ZS',{oi:0,ibase:FA,oblim:_olim}))
# stored member
OA=obase
e=S('ZS'); on('ZS',(net.or_(net.ge(oi,csz,e),net.ge(oi,oblim,e),net.ge(ip+oi,evc,e)),'A12_S0',{oi:0}),(None,'ZS1',{r1:FA+ip+oi}))
wo=WPort(1)
on('ZS1',(None,'ZS',{wo:(OA+oi,R1),oi:oi+1,ob:oi+1}))
# bit reader: the current byte is kept bit reversed, so the next bit is one threshold and
# a field or Huffman code takes one tick per bit
def nextbit(e_): return net.step(cur-127.5+e_*M-M)
def reversed_(e_):
    b_=net.bits(R1,8,e_); return sum((b_[k_]*(2**(7-k_)) for k_ in range(8)),X())
# n bit field
def getn(st,n,ret):
    on(st,(None,'GBL',{gbn:n,gbv:0,gbw:1,gbi:0,gret.r:gret.id(ret)}))
e=S('GBL'); hbit=nextbit(e)
# a whole field that the current byte still holds is taken in one tick: the byte's bits, then one line per field width
_gq=net.and_(e,net.eq(gbi,0,e),net.ge(nb,gbn,e)); _gb=net.bits(cur,8,_gq); _gh=net.decode(gbn,9,_gq)
_gv=X(); _gc=X()
for n_ in range(1,9):
    _gv=_gv+net.gate(sum((_gb[7-k_]*(2**k_) for k_ in range(n_)),X()),_gh[n_])
    _gc=_gc+net.gate(sum((_gb[7-k_]*(2**(7-k_+n_)) for k_ in range(n_,8)),X()),_gh[n_])
# a field across a byte boundary: up to three bits a tick while the byte and the field both have them
_hb2=net.step(cur-hbit*128-63.5+e*M-M); _hb3=net.step(cur-hbit*128-_hb2*64-31.5+e*M-M)
on('GBL',(net.ge(gbi,gbn,e),'GR',None),(net.and_(_gq,net.step(gbn)),'GR',{gbv:_gv,gbi:gbn,cur:_gc,nb:nb-gbn}),(net.eq(nb,0,e),'GBR',{r1:ibase+ip,ip:ip+1}),
 (net.and_(net.ge(nb,3,e),net.ge(gbn,gbi+3,e)),'GBL',{gbv:gbv+G_(gbw,hbit)+G_(gbw*2,_hb2)+G_(gbw*4,_hb3),gbw:gbw*8,gbi:gbi+3,cur:Shift((cur-hbit*128-_hb2*64-_hb3*32)*8,2048),nb:Dec(nb,3)}),
 (net.and_(net.ge(nb,2,e),net.ge(gbn,gbi+2,e)),'GBL',{gbv:gbv+G_(gbw,hbit)+G_(gbw*2,_hb2),gbw:gbw*4,gbi:gbi+2,cur:Shift((cur-hbit*128-_hb2*64)*4,1024),nb:Dec(nb,2)}),
 (None,'GBL',{gbv:gbv+G_(gbw,hbit),gbw:gbw*2,gbi:gbi+1,cur:Shift((cur-hbit*128)*2,512),nb:Dec(nb,1)}))
on('GBR',(net.gt(ip,ilim,S('GBR')),'A12_IE',None),(None,'GBL',{cur:reversed_(S('GBR')),nb:8}))
# Huffman decode, after puff: count[] at hb, symbols at hb+16. Each length's limit (first code plus count) and the
# symbol offset less its first code (lifted by HBASE, as memory writes cannot carry a negative) sit at hb+HLIM+2*len,
# so one read per bit decides and no first or index register has to be carried along.
HLIM=320; HBASE=65536; fq=R()
# Up to three bits a tick: the read window holds the limit and offset of four lengths, so the code so far and its next
# one, two and three bits are each compared with their own length's limit in the same tick. Limits past 15 are 0.
on('DEC',(None,'X_D3',{code:0,hlen:0,rl:hb+HLIM}))
e=S('X_D3'); b1_=nextbit(e); b2_=net.step(cur-b1_*128-63.5+e*M-M); b3_=net.step(cur-b1_*128-b2_*64-31.5+e*M-M)
c1_=code*2+b1_; c2_=code*4+b1_*2+b2_; c3_=code*8+b1_*4+b2_*2+b3_
n1_=net.ge(nb,1,e); n2_=net.ge(nb,2,e); n3_=net.ge(nb,3,e)
s1_=Shift((cur-b1_*128)*2,512); s2_=Shift((cur-b1_*128-b2_*64)*4,1024); s3_=Shift((cur-b1_*128-b2_*64-b3_*32)*8,2048)
on('X_D3',(net.lt(code,W[0],e),'D4',{r2:hb+W[1]-HBASE+code}),(net.ge(hlen,15,e),'OPEND',None),
 (net.and_(n1_,net.lt(c1_,W[2],e)),'D4',{r2:hb+W[3]-HBASE+c1_,cur:s1_,nb:Dec(nb,1)}),
 (net.and_(n2_,net.lt(c2_,W[4],e)),'D4',{r2:hb+W[5]-HBASE+c2_,cur:s2_,nb:Dec(nb,2)}),
 (n3_,'X_D3',{code:c3_,cur:s3_,nb:Dec(nb,3),hlen:hlen+3,rl:hb+HLIM+6+hlen*2}),
 (n2_,'X_D3',{code:c2_,cur:s2_,nb:Dec(nb,2),hlen:hlen+2,rl:hb+HLIM+4+hlen*2}),
 (n1_,'X_D3',{code:c1_,cur:s1_,nb:Dec(nb,1),hlen:hlen+1,rl:hb+HLIM+2+hlen*2}),
 (None,'CMP2_XR',{r1:ibase+ip,ip:ip+1}))
on('CMP2_XR',(net.gt(ip,ilim,S('CMP2_XR')),'A12_IE',None),(None,'X_D3',{cur:reversed_(S('CMP2_XR')),nb:8,rl:hb+HLIM+hlen*2}))
on('D4',(None,'HR',{sym:R2}))
# build table from lengths LN[lb..lb+ln)
bi=R();bo=R()
on('BLD',(None,'BC',{bi:0}))
e=S('BC')
on('BC',(net.ge(bi,16,e),'BD',{bi:0}),(None,'BC',{w1:(hb+bi,0),bi:bi+1}))
e=S('BD')
on('BD',(net.ge(bi,ln,e),'BE',{bi:1,bo:0,fq:0,w1:(hb+HLIM,0),w2:(hb+HLIM+32,0),w3:(hb+HLIM+34,0)}),(None,'BD1',{r1:as_x(LN)+lb+bi}))
on('BD1',(None,'BD2',{r2:hb+R1,cval:R1}))
on('BD2',(None,'BD',{w1:(hb+cval,R2+1),bi:bi+1}))
e=S('BE')
on('BE',(net.ge(bi,16,e),'BF',{bi:0}),(None,'BE1',{r1:hb+bi}))
on('BE1',(None,'BE',{w1:(as_x(OFFS)+bi,bo),w2:(hb+HLIM+bi*2,fq+R1),w3:(hb+HLIM+1+bi*2,as_x(HBASE+16)+bo-fq),fq:(fq+R1)*2,bo:bo+R1,bi:bi+1}))
e=S('BF')
on('BF',(net.ge(bi,ln,e),'CR',None),(None,'BF1',{r1:as_x(LN)+lb+bi}))
e=S('BF1')
on('BF1',(net.step(R1),'BF2',{cval:R1,r2:as_x(OFFS)+R1}),(None,'BF',{bi:bi+1}))
on('BF2',(None,'BF',{w1:(hb+16+R2,bi),w2:(as_x(OFFS)+cval,R2+1),bi:bi+1}))
# block header
getn('BH',1,'BH1')
on('BH1',(None,'BH1b',{bfinal:gbv}))
getn('BH1b',2,'BH2')
e=S('BH2'); ty_h=net.decode(gbv,4,e)
on('BH2',(ty_h[0],'ST0',{nb:0}),(ty_h[1],'FX0',{idx:0}),(ty_h[2],'DY0',None),(None,'OPEND',None))
# stored block
on('ST0',(None,'X_ST1',{rl:ibase+ip}))
on('X_ST1',(None,'ST2',{copyn:W[0]+W[1]*256,ip:ip+4}))
e=S('ST2')
on('ST2',(net.or_(net.ge(ip,ilim,e),net.ge(ob,oblim,e)),'A12_IE',None),(net.step(copyn),'ST3',{r1:ibase+ip}),(None,'BEND',None))
on('ST3',(None,'ST2',{wo:(OA+ob,R1),ob:ob+1,ip:ip+1,copyn:copyn-1}))
# fixed tables
e=S('FX0')
fl=X(c=0); a1=net.lt(idx,144,e);a2=net.and_(net.ge(idx,144,e),net.lt(idx,256,e));a3=net.and_(net.ge(idx,256,e),net.lt(idx,280,e));a4=net.ge(idx,280,e)
on('FX0',(net.ge(idx,288,e),'FX1',None),(None,'FX0',{w1:(as_x(LN)+idx,a1*8+a2*9+a3*7+a4*8),idx:idx+1}))
on('FX1',(None,'BLD',{hb:LH,lb:0,ln:288,cret.r:cret.id('FX2')}))
on('FX2',(None,'FX3',{idx:0}))
e=S('FX3')
on('FX3',(net.ge(idx,30,e),'FX4',None),(None,'FX3',{w1:(as_x(LN)+idx,5),idx:idx+1}))
on('FX4',(None,'BLD',{hb:DH,lb:0,ln:30,cret.r:cret.id('CODES')}))
# dynamic tables
getn('DY0',5,'DY1')
on('DY1',(None,'DY1b',{nlen:gbv+257})); getn('DY1b',5,'DY2')
on('DY2',(None,'DY2b',{ndist:gbv+1})); getn('DY2b',4,'DY3')
on('DY3',(None,'DY4',{ncode:gbv+4,idx:0}))
e=S('DY4')
on('DY4',(net.ge(idx,19,e),'DY5',{idx:0}),(None,'DY4',{w1:(as_x(LN)+idx,0),idx:idx+1}))
e=S('DY5')
on('DY5',(net.ge(idx,ncode,e),'DY7',None),(None,'DY5g',None))
getn('DY5g',3,'DY6')
ORDER=[16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15]
e=S('DY6'); oh=net.decode(idx,19,e); od=X()
for i_,v_ in enumerate(ORDER): od=od+oh[i_]*v_
on('DY6',(None,'DY5',{w1:(as_x(LN)+od,gbv),idx:idx+1}))
on('DY7',(None,'BLD',{hb:CLH,lb:0,ln:19,cret.r:cret.id('DY8')}))
on('DY8',(None,'DY9',{idx:0,prev:0}))
e=S('DY9')
on('DY9',(net.ge(idx,nlen+ndist,e),'DYA',None),(None,'DEC',{hb:CLH,hret.r:hret.id('DYs')}))
e=S('DYs')
on('DYs',(net.lt(sym,16,e),'DY9',{w1:(as_x(LN)+idx,sym),prev:sym,idx:idx+1}),(net.eq(sym,16,e),'DYr2',{rval:prev}),(net.eq(sym,17,e),'DYr3',{rval:0}),(None,'DYr7',{rval:0}))
getn('DYr2',2,'DYa2');getn('DYr3',3,'DYa3');getn('DYr7',7,'DYa7')
on('DYa2',(None,'DYl',{rept:gbv+3}));on('DYa3',(None,'DYl',{rept:gbv+3}));on('DYa7',(None,'DYl',{rept:gbv+11}))
e=S('DYl')
on('DYl',(net.step(rept),'DYl',{w1:(as_x(LN)+idx,rval),idx:idx+1,rept:rept-1,prev:rval}),(None,'DY9',None))
on('DYA',(None,'BLD',{hb:LH,lb:0,ln:nlen,cret.r:cret.id('DYB')}))
on('DYB',(None,'BLD',{hb:DH,lb:nlen,ln:ndist,cret.r:cret.id('CODES')}))
# literal and length codes
on('CODES',(net.ge(ob,oblim,S('CODES')),'A12_IE',None),(None,'DEC',{hb:LH,hret.r:hret.id('CS')}))
LB=[3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,67,83,99,115,131,163,195,227,258]
LE=[0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0]
DB=[1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025,1537,2049,3073,4097,6145,8193,12289,16385,24577]
DE=[0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13]
e=S('CS')
lit_=net.lt(sym,256,e); eob=net.eq(sym,256,e)
on('CS',(lit_,'CODES',{wo:(OA+ob,sym),ob:ob+1}),(eob,'BEND',None),(None,'CL0',None))
_ltab=rom_table(sum(([LB[min(i_,28)],LE[min(i_,28)]] for i_ in range(32)),[]))
on('CL0',(None,'A10_CL',{rl:as_x(_ltab)+(sym-257)*2}))
on('A10_CL',(None,'CL1',{lc_:W[0],gbn:W[1],gbv:0,gbw:1,gbi:0,gret.r:gret.id('CL2')}))
on('CL1',(None,'GBL',None))
on('CL2',(None,'DEC',{copyn:lc_+gbv,hb:DH,hret.r:hret.id('CD_')}))
_dtab=rom_table(sum(([DB[min(i_,29)],DE[min(i_,29)]] for i_ in range(32)),[]))
on('CD_',(None,'A10_CD',{rl:as_x(_dtab)+sym*2}))
on('A10_CD',(None,'CD1',{lb:W[0],gbn:W[1],gbv:0,gbw:1,gbi:0,gret.r:gret.id('CD2')}))
on('CD1',(None,'GBL',None))
e=S('CD2'); on('CD2',(net.or_(net.eq(lb,0,e),net.gt(lb+gbv,ob,e)),'A12_IE',None),(None,'CC',{dist:lb+gbv}))
e=S('CC')
# match copy: a block up to the distance at a time, overlapping copies repeat
ncp=R(); nc_=net.min_(copyn,dist)
on('CC',(net.step(copyn),'CC1',{rb:(OA+ob-dist,nc_),ncp:nc_}),(None,'CODES',None))
on('CC1',(None,'CC',{wb:(OA+ob,ncp),ob:ob+ncp,copyn:copyn-ncp}))
on('BEND',(bfinal,'IR',{oi:0}),(None,'BH',None))
# XML scan: an eight-cell window is compared against literal tags in one tick
e=S('PX')
on('PX',(net.ge(oi,ob,e),'T2_ZN',None),(None,'PX1',{rl:OA+oi}))
e=S('PX1')
lt_=net.eq(W[0],60,e)
_adv=a5_adv(e)    # no bracket at the head of the window: the next window's read goes out now, so a run of text takes one tick per window
on('PX1',(net.and_(ONE-lt_,net.ge(oi+_adv,ob,e)),'T2_ZN',{oi:oi+_adv}),(lt_,'PX2',{rl:OA+oi}),(None,'PX1',{oi:oi+_adv,rl:OA+oi+_adv}))
e=S('PX2')
on('PX2',(net.ge(nextb,SLOTMAX,e),'T2_ZN',None),(net.and_(t2skip,ONE-pat('</w:styl',e)),'PX',{oi:oi+1}),
 (pat('</w:styl',e),'T2_SW',{oi:oi+8,t2rr.r:t2rr.id('T2_SC')}),
 *A5_PX_EARLY(e),
 *F1_PX(e),
 (tag('<w:p',' >'),'PN1',{oi:oi+4}),
 (tag('<w:t',' >'),'TX0',{oi:oi+4}),
 (tag('<w:r',' >'),'PX',{ics:(t2ps,t2pK,t2pN,X(),X(),f1lb,X()),rnop:0,oi:oi+4}),
 (tag('<w:b','/ '),'T2_TV',{t2k:0,oi:oi+4}),
 (tag('<w:i','/ '),'T2_TV',{t2k:1,oi:oi+4}),
 (tag('<w:u','/ '),'T2_TV',{t2k:2,oi:oi+4}),
 (pat('<w:strik',e),'T2_TV',{t2k:4,oi:oi+9}),
 (pat('<w:noPro',e),'T2_C',{t2k:9,t2v:1,oi:oi+8}),
 (pat('<w:delTe',e),'TX0',{oi:oi+4}),
 (pat('<w:ins ',e),'T4_TS',{rvb:3,oi:oi+6}),
 (pat('<w:del ',e),'T4_TS',{rvb:4,oi:oi+6}),
 (pat('</w:ins>',e),'PX',{rins:0,oi:oi+8}),
 (pat('</w:del>',e),'PX',{rdel:0,oi:oi+8}),
 (pat('<w:fldSi',e),'T4_FL',{rl:OA+oi+23}),
 (pat('</w:fldS',e),'PX',{rfk:0,oi:oi+8}),
 (pat('<w:rStyl',e),'T2_VF',{oi:oi+8,t2rr.r:t2rr.id('T2_RS1')}),
 (pat('<w:sz ',e),'SZ0',{rl:OA+oi+13}),
 (pat('<w:color',e),'A5_CO',{oi:oi+8}),
 (pat('<w:rFont',e),'A5_RF',{oi:oi+9}),
 (pat('<w:highl',e),'T2_HL',{rl:OA+oi+20}),
 (pat('<w:vertA',e),'T2_VA',{rl:OA+oi+20}),
 (pat('<w:jc ',e),'JC0',{rl:OA+oi+13}),
 (net.and_(rtoc,pat('<w:ind ',e)),'T3_RI0',{oi:oi+7}),
 (pat('<w:pStyl',e),'T2_VF',{oi:oi+8,t2rr.r:t2rr.id('T2_PS1')}),
 (pat('<w:ilvl ',e),'T2_NM',{oi:oi+8,t2n_:0,t2rr.r:t2rr.id('T2_IL')}),
 (pat('<w:numId',e),'T2_NM',{oi:oi+8,t2n_:0,t2rr.r:t2rr.id('T2_NI')}),
 (pat('<w:spaci',e),'T2_AT',{oi:oi+8}),
 (pat('<w:ind ',e),'T2_IN',{oi:oi+7,r1:cb+LIST}),
 (pat('<w:pageB',e),'PX',{oi:oi+8,w1:(cb+PBRK,1)}),
 (pat('<w:style',e),'T2_STQ',{rl:OA+oi+8}),
 (pat('<w:based',e),'T2_VF',{oi:oi+8,t2rr.r:t2rr.id('T2_PS1')}),
 (pat('<w:name ',e),'T2_VF',{oi:oi+8,t2rr.r:t2rr.id('T2_NA')}),
 (pat('<w:abstr',e),'T2_AB',{rl:OA+oi+8}),
 (pat('<w:num ',e),'T2_NM',{oi:oi+7,t2n_:0,t2rr.r:t2rr.id('T2_NX')}),
 (pat('<w:lvl ',e),'T2_NM',{oi:oi+7,t2n_:0,t2rr.r:t2rr.id('T2_LV')}),
 (pat('<w:numFm',e),'T2_FM',{rl:OA+oi+17}),(lpat('<w:lvlTe',e),'V6_LT',{rl:OA+oi+18}),
 *A4_PX(e),
 *A6_PX_RULES(e),*T3_PX_RULES(e),
 (None,'PX',{oi:oi+1}))
e=S('SZ0')
_q1=net.or_(net.eq(W[1],34,e),net.eq(W[1],39,e));_q2=net.and_(e,ONE-_q1,net.or_(net.eq(W[2],34,e),net.eq(W[2],39,e)))
hpv=net.min_(G_(W[0]-48,_q1)+G_((W[0]-48)*10+(W[1]-48),_q2)+G_((W[0]-48)*100+(W[1]-48)*10+W[2]-48,e-_q1-_q2),as_x(199))
_stab=rom_table([0]+[rom.sz_raw(rom.sz_near(hp_/2) if hp_ else 0) for hp_ in range(200)])
on('SZ0',(None,'A10_SZ',{r1:as_x(_stab)+net.relu(hpv+1),oi:oi+13}))
on('A10_SZ',(None,'T2_C',{t2k:8,t2v:R1}))
e=S('JC0'); j1=net.eq(W[0],99,e);j2=net.or_(net.eq(W[0],114,e),net.eq(W[0],101,e));j3=net.eq(W[0],98,e)
on('JC0',(None,'PX',{w1:(cb+ALIGN,j1*1+j2*2+j3*3),oi:oi+13}))
e=S('PN1')
fsm.set(a5aft,S('PN1'),0)
on('PN1',(net.and_(incell,net.step(clen),net.lt(clen,1000,e)),'INS',{ins_ch:32,ins_st:csi+rhi,oret.r:oret.id('A5_PN')}),(incell,'T2_PR',{rins:0,rdel:0,rfk:0}),(pfirst,'T2_PR',{pfirst:0,rins:0,rdel:0,rfk:0}),(None,'SPLIT',{oret.r:oret.id('T3_PN2'),rins:0,rdel:0,rfk:0,a6nc:1}))
on('T3_PN2',(None,'T2_PR',{a6nc:0,w3:(cb+CSH,0),w1:(cb+ALIGN,0),w2:(cb+SECN,rdp),rdp:0,rtoc:0,rdig:0}))
# text inside a run
e=S('TX0')
on('TX0',(None,'TX1',{rl:OA+oi}))
e=S('TX1'); on('TX1',(net.eq(W[0],62,e),'TX2',{oi:oi+1}),(None,'TX0',{oi:oi+1}))
on('TX2',(None,'TX3',{rl:OA+oi,rpw:OA+oi}))

e=S('TX3')
amp_=net.eq(W[0],38,e);ltx=net.eq(W[0],60,e)
isdg_=net.and_(net.ge(W[0],48,e),net.lt(W[0],58,e))
_wt=rpw.out
_ntx=a7_lead([net.step(net.step(as_x(32)-_wt[i_]-0.5+e*M-M)+net.step(_wt[i_]-126.5+e*M-M)+net.eq(_wt[i_],38,e)+net.eq(_wt[i_],60,e)) for i_ in range(PSN)],e)
_ncap=net.relu(as_x(950)-clen+e*M-M); _ntx2=_ntx-net.relu(_ntx-_ncap+e*M-M); _tgo=net.and_(e,ONE-rdig,net.step(_ntx2-1.5),net.eq(co,clen,e)); _tg=G_(csi+rhi,_tgo)
for w_ in _st: net.connect(w_,_tg)
wpch.drive(_tgo,(cb+co,_ntx2)); wpst.drive(_tgo,(cb+1024+co,_ntx2)); w3.drive(_tgo,(cb+LEN,clen+_ntx2)); w4.drive(_tgo,(cb+DIRTY,1))
on('TX3',(_tgo,'TX2',{oi:oi+_ntx2,co:co+_ntx2,clen:clen+_ntx2}),(ltx,'PX',None),(net.and_(rdig,isdg_),'TX2',{tpgv:tpgv*10+W[0]-48,oi:oi+1,w1:(cb+TPG,tpgv*10+W[0]-48)}),(rdig,'T3_RT0',{oi:a5bk,rdig:0,rtoc:0,w1:(cb+TOCF,0),w2:(cb+TPG,0)}),
 (net.and_(amp_,net.eq(W[1],35,e)),'A5_NE',{oi:oi+2}),
 (net.and_(ONE-incell,net.or_(net.ge(clen,1000,e),net.and_(net.eq(W[0],32,e),net.ge(clen,950,e)))),'SPLIT',{a5pb:cb,oret.r:oret.id('A5_LP')}),
 (net.and_(amp_,net.eq(W[1],97,e),net.eq(W[2],112,e)),'INS',{ins_ch:39,ins_st:csi+rhi,oi:oi+6,oret.r:oret.id('TX2')}),
 (net.and_(amp_,net.eq(W[1],113,e)),'INS',{ins_ch:34,ins_st:csi+rhi,oi:oi+6,oret.r:oret.id('TX2')}),
 (net.and_(amp_,net.eq(W[1],97,e)),'INS',{ins_ch:38,ins_st:csi+rhi,oi:oi+5,oret.r:oret.id('TX2')}),
 (net.and_(amp_,net.eq(W[1],108,e)),'INS',{ins_ch:60,ins_st:csi+rhi,oi:oi+4,oret.r:oret.id('TX2')}),
 (net.and_(amp_,net.eq(W[1],103,e)),'INS',{ins_ch:62,ins_st:csi+rhi,oi:oi+4,oret.r:oret.id('TX2')}),
 (net.and_(net.ge(W[0],192,e),net.lt(W[0],224,e)),'T2_U8',{t2cp:(W[0]-192)*64+(W[1]-128),oi:oi+2}),
 (net.and_(net.ge(W[0],224,e),net.lt(W[0],240,e)),'T2_U8',{t2cp:(W[0]-224)*4096+(W[1]-128)*64+(W[2]-128),oi:oi+3}),
 (net.ge(W[0],240,e),'V7_R4',{t2cp:(W[0]-240)*262144+(W[1]-128)*4096+(W[2]-128)*64+(W[3]-128)-65536,oi:oi+4}),
 (net.or_(net.gt(W[0],126,e),net.lt(W[0],32,e),net.ge(clen,1000,e)),'TX2',{oi:oi+1}),
 # plain text always lands at the end of the paragraph being read, so it is written here and the next byte is already on its way
 (None,'TX3',{w1:(cb+co,W[0]),w2:(cb+1024+co,csi+rhi),w3:(cb+LEN,clen+1),co:co+1,clen:clen+1,oi:oi+1,rl:OA+oi+1}))
e=S('RF9')
def _seed1(n_): return 1+next((i_ for i_,q_ in enumerate(FNSEED) if q_.startswith(n_)),0)
_RF=[('Segoe',5,0),('Book Ant',3,0),('Palatino',3,0),('Century',3,0),('Baskervi',3,0),('Lucida C',4,0),('Liberati',2,0),('Trebuche',5,0),('Noto San',5,0),('Noto Ser',3,0),('Roboto',2,0),('Aptos',0,0),('Corbel',0,0),('Candara',0,0),('Constant',1,0),('Caladea',1,0),('Cambria',1,1),('Arimo',2,0),('Arial',2,1),('Helvetic',2,0),('Tinos',3,0),('Times',3,1),('Georgia',3,0),('Garamond',3,0),('Cousine',4,0),('Courier',4,1),('Consolas',4,0),('Open San',5,0),('Verdana',5,0),('Tahoma',5,0),('Oswald',6,0),('Caveat',7,0),('Carlito',0,0),('Calibri',0,1)]
on('RF9',(pat('Liberati',e),'A5_LIB',{rl:OA+oi+11}),*[(lpat(n_,e),'V4_FS',{t2k:3,t2v:f_,v4i:_seed1(n_),v4f:1,v4j:0,**({falias[f_]:1} if a_ else {})}) for n_,f_,a_ in _RF],(None,'V4_FS',{t2k:3,t2v:0,v4i:1,v4j:0}))
e=S('CO0'); cvv=X(); exact=X()
for j_ in range(1,32):
    p_=lpat('%02X%02X%02X'%PAL_F[j_],e); cvv=cvv+p_*j_; exact=exact+p_
def hexd(c_,en): return as_x(c_)-48-net.ge(c_,65,en)*7-net.ge(c_,97,en)*32
hr=net.bits(hexd(W[0],e),4,e);hg=net.bits(hexd(W[2],e),4,e);hb_=net.bits(hexd(W[4],e),4,e)
hix=(hr[1]+hr[2]*2+hr[3]*4)*64+(hg[1]+hg[2]*2+hg[3]*4)*8+(hb_[1]+hb_[2]*2+hb_[3]*4)
exf=exact; au=pat('auto',e)
_ctab=[]
for i_ in range(512):
    r_,g_,b_=((i_>>6)&7)*36+18,((i_>>3)&7)*36+18,(i_&7)*36+18
    _ctab.append(min(range(32),key=lambda j:(PAL_F[j][0]-r_)**2+(PAL_F[j][1]-g_)**2+(PAL_F[j][2]-b_)**2))
_ctab=rom_table(_ctab)
def _hx(c_): return hexd(c_,e)
_rgbv=_hx(W[0])*(1<<20)+_hx(W[1])*(1<<16)+_hx(W[2])*(1<<12)+_hx(W[3])*(1<<8)+_hx(W[4])*16+_hx(W[5])+1
on('CO0',(au,'T2_C',{t2k:7,t2v:0,oi:oi+6}),(exf,'T2_C',{t2k:7,t2v:cvv,oi:oi+6}),(None,'A10_CO',{r1:as_x(_ctab)+hix,oi:oi+6,t2kx:_rgbv}))
on('A10_CO',(None,'T2_C',{t2k:7,t2v:R1}))
on('OPEND',(vdry,'IMP_VF',None),(None,'OPE2',{nolog:0,clip0:0,clip1:0}))
on('OPE2',(None,'A5_CX0',{autos:1,lc:1,dfrom:0,ity:as_x(0),a5i:1}))

# ---- PNG reader: chunks, inflate, row filters, decimation to fit the page ----
net.group('png reader')
picout=Bus(net); picout.add(S('HF'),wpic); fsm.set(wpic,S('HF'),0)
pbase=R();pgdoc=R();pgl=R();pw=R();ph=R();pdep=R();pct=R();pbp=R();pst=R();dst=R();cl2=R();ck=R();psz=R();pcy=R();pos=R();ix=R();rowf=R();ky=R();kx=R();dw=R();dh=R();dcnt=R();pst0=R();rstart=R()
on('PG_0',(None,'PG_1',{rl:FA,pbase:FA,pgdoc:0,pgl:evc}))
e=S('PG_1')
on('PG_1',(net.and_(net.eq(W[1],80,e),net.eq(W[2],78,e),net.eq(W[3],71,e)),'PG_C',{ip:8,dst:0,grp:grp+1,pw:0,ph:0}),(None,'T3_PF',None))
on('PG_C',(net.ge(ip,pgl,S('PG_C')),'T3_PF',None),(None,'PG_D',{rl:pbase+ip}))
e=S('PG_D'); ihdr=pat('IHDR',e,4);idat=pat('IDAT',e,4);iend=pat('IEND',e,4)
lenv=W[1]*65536+W[2]*256+W[3]
on('PG_D',(ihdr,'PG_H',{rl:pbase+ip+8}),(idat,'PG_I',{cl2:lenv,ip:ip+8}),(iend,'PG_Z',None),(None,'PG_C',{ip:ip+12+lenv}))
on('PG_H',(None,'PG_H2',{pw:W[2]*256+W[3],ph:W[6]*256+W[7],rl:pbase+ip+16}))
e=S('PG_H2'); ok=net.and_(net.eq(W[0],8,e),net.eq(W[4],0,e),net.or_(net.eq(W[1],0,e),net.eq(W[1],2,e),net.eq(W[1],4,e),net.eq(W[1],6,e)))
on('PG_H2',(ok,'PG_C',{pct:W[1],pbp:net.eq(W[1],0,e)+net.eq(W[1],2,e)*3+net.eq(W[1],4,e)*2+net.eq(W[1],6,e)*4,ip:ip+25}),(None,'T3_PF',None))
e=S('PG_I'); nc2=cl2-net.relu(cl2-1100); on('PG_I',(net.ge(ip,pgl,e),'PG_Z',None),(net.step(cl2),'PG_J',{rb:(pbase+ip,nc2),ncp:nc2}),(None,'PG_C',{ip:ip+4}))
on('PG_J',(None,'PG_I',{wb:(pbase+dst,ncp),dst:dst+ncp,ip:ip+ncp,cl2:cl2-ncp}))
# inflate the concatenated stream after its two byte header
on('PG_Z',(None,'PG_Y',{ibase:pbase,obase:OUTP,ip:2,ob:0,nb:0,cur:0,iret.r:iret.id('PG_U'),ilim:dst,oblim:PNGB-OUTP-300000}))
on('PG_Y',(None,'BH',None))
# stride by repeated addition
on('PG_U',(None,'PG_U1',{pst:0,dcnt:0}))
e=S('PG_U1'); on('PG_U1',(net.ge(dcnt,pbp,e),'PG_U2',{pst:pst+1}),(None,'PG_U1',{pst:pst+pw,dcnt:dcnt+1}))
e=S('PG_U2'); on('PG_U2',(net.or_(net.eq(pw,0,e),net.eq(ph,0,e)),'T3_PF',None),(None,'PG_R',{pos:0,pcy:0}))
# row filters
OAp=as_x(OUTP)
e=S('PG_R'); on('PG_R',(net.ge(pcy,ph,e),'PG_K',{ck:1,psz:624}),(net.ge(pos,ob,e),'T3_PF',None),(None,'PG_F',{r1:OAp+pos}))
on('PG_F',(None,'PG_X',{rowf:R1,pos:pos+1,ix:0,rstart:pos+1}))
e=S('PG_X')
on('PG_X',(net.eq(rowf,0,e),'PG_R',{pcy:pcy+1,pos:pos+pst-1}),(net.ge(ix,pst-1,e),'PG_R',{pcy:pcy+1}),(None,'PG_P',{r1:OAp+pos,r2:G_(OAp+pos-pbp,net.ge(ix,pbp,e)),rU:G_(OAp+pos-pst,net.step(pcy)),rV:G_(OAp+pos-pst-pbp,net.and_(net.ge(ix,pbp,e),net.step(pcy)))}))
e=S('PG_P'); ft=net.decode(rowf,5,e)
hasL=net.ge(ix,pbp,e);hasU=net.step(pcy)
a_=G_(R2,hasL);b_=G_(rU.out[0],hasU);c_=G_(rV.out[0],net.and_(hasL,hasU))
xv=R1
sm=a_+b_; avg=(sm-net.bits(sm,9,ft[3])[0])*0.5
def abs_(x): return net.relu(x)+net.relu(-x)
a4=G_(a_,ft[4]);b4=G_(b_,ft[4]);c4=G_(c_,ft[4])
pa=abs_(b4-c4);pb=abs_(a4-c4);pc=abs_(a4+b4-c4*2)
ca=net.and_(ft[4],net.ge(pb,pa,ft[4]),net.ge(pc,pa,ft[4]));cb_p=net.and_(ft[4],ONE-ca,net.ge(pc,pb,ft[4]));cc=ft[4]-ca-cb_p
paeth=G_(a4,ca)+G_(b4,cb_p)+G_(c4,cc)
pred=G_(a_,ft[1])+G_(b_,ft[2])+G_(avg,ft[3])+G_(paeth,ft[4])
tot=xv+pred; ov=net.ge(tot,256,e)
hasL2=net.ge(ix+1,pbp,e);hasU2=net.step(pcy)
on('PG_P',(net.ge(ix+1,pst-1,e),'PG_R',{wo:(OAp+pos,tot-ov*256),pos:pos+1,ix:ix+1,pcy:pcy+1}),
 (None,'PG_P',{wo:(OAp+pos,tot-ov*256),pos:pos+1,ix:ix+1,r1:OAp+pos+1,r2:G_(OAp+pos+1-pbp,hasL2),rU:G_(OAp+pos+1-pst,hasU2),rV:G_(OAp+pos+1-pst-pbp,net.and_(hasL2,hasU2))}))
# smallest integer factor that fits 624 by 800
e=S('PG_K'); on('PG_K',(net.ge(psz,pw,e),'PG_L',{dcnt:ck*800}),(None,'PG_K',{ck:ck+1,psz:psz+624}))
e=S('PG_L'); on('PG_L',(net.ge(dcnt,ph,e),'PG_M',{pos:0,pcy:0,dh:0,ky:0,dst:imgp,dcnt:0}),(None,'PG_L',{ck:ck+1,dcnt:dcnt+800}))
# copy kept pixels as packed RGB; rows start at pos
e=S('PG_M'); on('PG_M',(net.ge(pcy,ph,e),'PG_Q',None),(net.lt(ky,ck,e)*0+net.step(ky),'PG_S',{pos:pos+pst,pcy:pcy+1,ky:ky+1}),(None,'PG_N',{ix:0,kx:0,dw:0,rstart:pos+1}))
e=S('PG_S'); on('PG_S',(net.ge(ky,ck,e),'PG_M',{ky:0}),(None,'PG_M',None))
e=S('PG_N'); on('PG_N',(net.ge(ix,pw,e),'PG_O',{pos:rstart+pst-1,pcy:pcy+1,dh:dh+1,ky:ky+1}),(net.step(kx),'PG_N2',{ix:ix+1,kx:kx+1}),(None,'PG_N3',{rl:OAp+rstart+dcnt}))
fsm.set(dcnt,net.and_(S('PG_N'),net.step(kx)),dcnt+pbp)
e=S('PG_N2'); on('PG_N2',(net.ge(kx,ck,e),'PG_N',{kx:0}),(None,'PG_N',None))
on('PG_O',(net.ge(ky,ck,S('PG_O')),'PG_M',{ky:0,dcnt:0}),(None,'PG_M',{dcnt:0}))
e=S('PG_N3'); gray=net.or_(net.eq(pct,0,e),net.eq(pct,4,e))
rv0=W[0]; gv0=G_(W[0],gray)+G_(W[1],e-gray); bv0=G_(W[0],gray)+G_(W[2],e-gray)
# alpha blend on white, by shift and add on the alpha bits: (c*a+255*(255-a)+127)/255
ha2=net.eq(pct,4,e);ha4=net.eq(pct,6,e)
av=G_(W[1],ha2)+G_(W[3],ha4)+(e-ha2-ha4)*255
abt=net.bits(av,8,e)
def blend(c_):
    s_=X(c=0)
    for k_ in range(8): s_=s_+G_(c_*(2**k_),abt[k_])
    rem_=net.gate((s_+(as_x(255)-av)*255+127)*(1.0/255),e); o_=X()
    for k_ in reversed(range(8)):
        b_=net.step(rem_-2**k_+1e-6); o_=o_+b_*(2**k_); rem_=rem_-b_*(2**k_)
    return o_
rv=blend(rv0);gv=blend(gv0);bv=blend(bv0)
imw=WPort(1); wl_i=WPort(3)
imw.drive(e,(as_x(IMG0)+dst,rv+gv*256+bv*65536))
on('PG_N3',(net.ge(dst,SAVEB-IMG0-2000,e),'T3_PF',None),(net.ge(ck,2,e),'PG_N',{dst:dst+1,dw:dw+1,dcnt:dcnt+pbp,ix:ix+1,kx:1}),(None,'PG_N',{dst:dst+1,dw:dw+1,dcnt:dcnt+pbp,ix:ix+1,kx:0}))
# insert a picture paragraph at the caret
e=S('PG_Q'); on('PG_Q',(pgdoc,'T3_PQ',None),(net.eq(clen,0,e),'T3_PG0',None),(None,'SPLIT',{oret.r:oret.id('PG_Q2')}))   # an empty paragraph takes the picture itself
on('PG_Q2',(None,'T3_PG0',None))
