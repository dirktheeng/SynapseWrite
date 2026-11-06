# ---- Tier 2 subsystems: style table, paragraph commands, list keys, typed size, docx reader helpers ----
net.group('tier 2')
# ROM images. Written once at build time; the network reads them through its memory ports.
T2_ROM=list(FN_ROM)
def _rec(i,run,al=0,ind=0,fi=0,lsp=0,spb=0,spa=DEFSPA,sid='',name='',pt=None):
    vals=[rom.lit(run)+(rom.sz_raw(rom.SZ.index(pt)) if pt else 0),al,ind,fi,lsp,spb,spa,0]
    for base in (STY0,STY):
        a=base+i*STYN
        for j,v in enumerate(vals):
            if v: T2_ROM.append([a+j,v])
        for j,c in enumerate(sid): T2_ROM.append([a+8+j,ord(c)])
        for j,c in enumerate(name): T2_ROM.append([a+28+j,ord(c)])
BLUE3=3*256
_rec(0,0,sid='Normal',name='Normal')
_rec(1,7,spa=0,sid='Title',name='Title')
_rec(2,3+BLUE3,spb=16,spa=0,sid='Heading1',name='heading 1')
_rec(3,BLUE3,spb=3,spa=0,sid='Heading2',name='heading 2',pt=13)
_rec(4,1+BLUE3,spb=3,spa=0,sid='Heading3',name='heading 3')
_rec(5,0+20*256+32,al=1,spb=13,spa=11,sid='Quote',name='Quote')
def _roman(n):
    r=''
    for v,t in ((100,'c'),(90,'xc'),(50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')):
        while n>=v: r+=t; n-=v
    return r
def _alpha(n):
    q,m=divmod(n-1,26); return chr(97+m)*(q+1)
for lv,fn in enumerate((str,_alpha,_roman)):
    for n in range(1,256):
        for j,ch in enumerate((fn(n)+'.')[:7]): T2_ROM.append([MKT+lv*2048+n*8+j,ord(ch)])
# keys outside Latin-1 go through the code map, and bypass the key decoder
e=S('T2_KU'); um_en.lin(e); um_in.add(e,eva)
on('T2_KM',(net.ge(eva,256,S('T2_KM')),'T2_KU',None),(None,'KEY',None))
on('T2_KU',(net.and_(net.step(um_out),findon),'FTYPE',{eva:um_out}),(net.step(um_out),'TYPE',{eva:um_out}),(None,'HALT',None))
e=S('T2_PS'); um_en.lin(e); um_in.add(e,ins_ch)
e=S('T2_PS'); _pm=net.and_(e,pfm); on('T2_PS',(net.step(um_out),'INS',{ins_ch:um_out,ins_st:G_(pfst,_pm)+G_(TST,e-_pm),oret.r:oret.id('PS2')}),(None,'PS2',None))
e=S('T2_U8'); um_en.lin(e); um_in.add(e,t2cp)
on('T2_U8',(None,'T2_U9',{ins_ch:um_out}))
e=S('T2_U9')
on('T2_U9',(net.ge(clen,1000,e),'TX2',None),(net.step(ins_ch),'INS',{ins_st:csi+rhi,oret.r:oret.id('TX2')}),(None,'INS',{ins_ch:63,ins_st:csi+rhi,oret.r:oret.id('TX2')}))
# typed font size
e=S('T2_TD'); dig=net.and_(net.ge(eva,48,e),net.lt(eva,58,e))
on('T2_TD',(dig,'RD0',{td1:td0,td0:eva-48}),(None,'RD0',None))
e=S('T2_TS'); szv=td1*10+td0; hz=net.decode(szv,100,e); near=X()
for v_ in range(100): near=near+hz[v_]*rom.sz_raw(rom.sz_near(v_))
on('T2_TS',(net.eq(szv,0,e),'RD0',None),(None,'FMTS',{fm:9,fsi:near}))
# list toggles and keys
e=S('T2_LI0')
on('T2_LI',(None,'T2_LI0',{r1:cb+LIST}))
lb0=net.bits(R1,9,e); kind0=lb0[0]+lb0[1]*2; lvl0=lb0[2]*4+lb0[3]*8
on('T2_LI0',(net.eq(kind0,alv,e),'SETLI',{alv:0}),(None,'SETLI',{alv:alv+lvl0}))
e=S('T2_TB'); lb1=net.bits(R1,9,e); k1_=lb1[0]+lb1[1]*2; l1_=lb1[2]+lb1[3]*2
inlist1=net.and_(e,net.step(k1_),net.or_(net.eq(co,0,e),has_sel))
_f1=sum((lb1[4+k_]*(16<<k_) for k_ in range(5)),X())
on('T2_TB',(net.and_(inlist1,shiftk),'PA0',{pwalk:lo_p,pfld:LIST,alv:k1_+net.relu(l1_-1)*4+_f1,grp:grp+1}),
 (inlist1,'PA0',{pwalk:lo_p,pfld:LIST,alv:k1_+net.min_(l1_+1,2)*4+_f1,grp:grp+1}),
 (None,'TYPE',{eva:9}))
t2es=R()
e=S('T2_EN0'); lb2=net.bits(R1,9,e); k2_=lb2[0]+lb2[1]*2; l2_=lb2[2]+lb2[3]*2
emp=net.and_(e,net.step(k2_),net.eq(clen,0,e))
on('T2_EN0',(net.and_(emp,net.step(l2_)),'PA0',{pwalk:cp,pfld:LIST,alv:k2_+(l2_-1)*4}),(emp,'PA0',{pwalk:cp,pfld:LIST,alv:0}),(None,'SPLIT',{t2es:R2,oret.r:oret.id('T2_EN1')}))
# after a styled paragraph ends at its last character, the next paragraph is Normal
e=S('T2_EN1')
on('T2_EN1',(net.and_(net.step(t2es),net.eq(clen,0,e)),'T2_EN2',{rl:as_x(STY),r1:as_x(STYX),r2:as_x(STYX)+1}),(None,'AFTER_ED',None))
W_=rl.out
on('T2_EN2',(None,'AFTER_ED',{ity:(W_[0],R1,R2,X()),w1:(cb+ALIGN,W_[1]),wln:(cb+PIND,W_[2],W_[3],W_[4],W_[5],W_[6],0)}))
on('T2_BK',(net.step(R1),'PA0',{pwalk:cp,pfld:LIST,alv:0}),(net.step(cp),'MG0',{}),(None,'AFTER_ED',None))
# applying a style: format the runs, then write each paragraph property with undo records
t2f=[R() for _ in range(8)]; t2lo=R();t2hi=R();t2i_=R();t2o=R();t2val=R();t2um=R()
on('T2_SA0',(None,'T2_SA1',{rl:as_x(STY)+t2si*STYN,t2um:0,r1:as_x(STYX)+t2si*4,r2:as_x(STYX)+t2si*4+1}))
on('T2_SA1',(None,'T2_SA2',{fpk:R1,fpn:R2,fpy:0,fpre:W_[0],t2f[1]:W_[1],t2f[2]:W_[2],t2f[3]:W_[3],t2f[4]:W_[4],t2f[5]:W_[5],t2f[6]:W_[6],fm:8,t2lo:lo_p,t2hi:hi_p,grp:grp+1-a4cfq,ap:lo_p,ao:0}))
on('T2_SA2',(None,'J0',{jp:t2hi,jo:2047,jret.r:jret.id('FMTS')}))
on('T2_SP0',(None,'T2_SP1',{pwalk:t2lo}))
on('T2_SP1',(None,'T2_SP2',{r1:as_x(PT)+pwalk}))
on('T2_SP2',(None,'T2_SF',{t2b:R1,t2i_:0}))
e=S('T2_SF'); hf=net.decode(t2i_,7,e); FLD=[ALIGN,PIND,PFIRST,PLSP,PSPB,PSPA,PSTY]; t2of_=X(); val_=X()
for i_,f_ in enumerate(FLD):
    t2of_=t2of_+hf[i_]*f_
    val_=val_+(G_(t2si,hf[i_]) if f_==PSTY else G_(t2f[i_+1],hf[i_]))
on('T2_SF',(None,'T2_SG',{t2o:t2of_,t2val:val_,r2:t2b+t2of_}))
e=S('T2_SG'); log(e,6,pwalk,t2o,R2,t2val)
on('T2_SG',(net.lt(t2i_,6,e),'T2_SF',{t2i_:t2i_+1,w1:(t2b+t2o,t2val),w2:(t2b+DIRTY,1)}),
 (t2um,'T2_UC0',{w1:(t2b+t2o,t2val),w2:(t2b+DIRTY,1)}),
 (net.lt(pwalk,t2hi,e),'T2_SP1',{pwalk:pwalk+1,w1:(t2b+t2o,t2val),w2:(t2b+DIRTY,1)}),
 (None,'RD0',{lc:1,ap:cp,ao:co,w1:(t2b+t2o,t2val),w2:(t2b+DIRTY,1)}))
# update a style from the caret paragraph, then carry the change to all its paragraphs
t2or=R();t2nr_=R();t2c=R();t2l=R();t2ni=R();t2ni_rec_=Interned(R(),t2ni)
on('T2_UM0',(None,'T2_UM1',{r1:cb+PSTY,rs:cb+1024,rl:cb+LEN,rp6:cb+PIND}))
e=S('T2_UM1'); hasc=net.step(clen)
on('T2_UM1',(None,'T2_UM2',{t2si:R1,t2nr_:G_(RSR,hasc)+G_(ty,e-net.and_(e,hasc)),v4uk:G_(RSK,hasc)+G_(ity.k,e-net.and_(e,hasc)),v4un:G_(RSN,hasc)+G_(ity.n,e-net.and_(e,hasc)),t2ni_rec_:(G_(RSR,hasc)+G_(ty,e-net.and_(e,hasc)),G_(RSK,hasc)+G_(ity.k,e-net.and_(e,hasc)),G_(RSN,hasc)+G_(ity.n,e-net.and_(e,hasc)),X()),t2f[1]:rl.out[2],t2f[2]:rp6.out[0],t2f[3]:rp6.out[1],t2f[4]:rp6.out[2],t2f[5]:rp6.out[3],t2f[6]:rp6.out[4],grp:grp+1}))
on('T2_UM2',(None,'T2_UM3',{r1:as_x(STY)+t2si*STYN,r2:as_x(STYX)+t2si*4,w1:(as_x(STYX)+t2si*4,v4uk),w2:(as_x(STYX)+t2si*4+1,v4un)}))
on('T2_UM3',(None,'T2_UT',{t2or:R1,v4ok:R2,t2i_:0}))
e=S('T2_UT'); hq=net.decode(t2i_,7,e); vq=G_(t2nr_,hq[0])
for i_ in range(1,7): vq=vq+G_(t2f[i_],hq[i_])
on('T2_UT',(None,'T2_UU',{t2val:vq,r2:as_x(STY)+t2si*STYN+t2i_}))
e=S('T2_UU'); log(e,7,as_x(STY)+t2si*STYN+t2i_,0,R2,t2val)
on('T2_UU',(net.lt(t2i_,6,e),'T2_UT',{t2i_:t2i_+1,w1:(as_x(STY)+t2si*STYN+t2i_,t2val)}),(None,'T2_UW',{pwalk:0,t2um:1,w1:(as_x(STY)+t2si*STYN+t2i_,t2val)}))
e=S('T2_UW'); on('T2_UW',(net.ge(pwalk,npar,e),'RD0',{lc:1,dfrom:0,t2um:0,ity:(t2nr_,v4uk,v4un,X())}),(None,'T2_UX',{r1:as_x(PT)+pwalk}))
on('T2_UX',(None,'T2_UY',{t2b:R1,r2:R1+PSTY,rl:R1+LEN}))
e=S('T2_UY'); on('T2_UY',(net.eq(R2,t2si,e),'T2_SF',{t2i_:0,t2l:rl.out[0]}),(None,'T2_UW',{pwalk:pwalk+1}))
on('T2_UC0',(None,'T2_UC1',{t2c:0}))
e=S('T2_UC1'); on('T2_UC1',(net.ge(t2c,t2l,e),'T2_UW',{pwalk:pwalk+1}),(None,'T2_UC2',{rs:t2b+1024+t2c}))
e=S('T2_UC2'); hit_=net.and_(net.eq(RSR,t2or,e),net.eq(RSK,v4ok,e),net.lt(RSC,ST_INS,e)); log(hit_,5,pwalk,t2c,RSC,t2ni); w1.drive(hit_,(t2b+1024+t2c,t2ni))
on('T2_UC2',(None,'T2_UC1',{t2c:t2c+1}))
# paragraph property stepping
t2d=R();t2mn=R()
on('T2_PD',(None,'T2_PD0',{pwalk:lo_p,grp:grp+1}))
on('T2_PD0',(None,'T2_PD1',{r1:as_x(PT)+pwalk}))
on('T2_PD1',(None,'T2_PD2',{t2b:R1,r2:R1+pfld,r1:R1+PIND}))
e=S('T2_PD2'); t2dd=t2d-1000; t2nvv=G_(net.max_(pf_val(R2)+t2dd,as_x(0)-R1)+PFO,t2mn)+G_(net.relu(R2+t2dd),e-net.and_(e,t2mn))
on('T2_PD2',(None,'T2_PD3',{t2val:t2nvv,t2o:R2}))
e=S('T2_PD3'); log(e,6,pwalk,pfld,t2o,t2val)
on('T2_PD3',(net.lt(pwalk,hi_p,e),'T2_PD0',{pwalk:pwalk+1,w1:(t2b+pfld,t2val),w2:(t2b+DIRTY,1)}),(a4rc,'T2_PD0',{pwalk:lo_p,a4rc:0,pfld:PFIRST,t2d:as_x(2000)-a4dl,t2mn:1,w1:(t2b+pfld,t2val),w2:(t2b+DIRTY,1)}),(None,'RD0',{lc:1,w1:(t2b+pfld,t2val),w2:(t2b+DIRTY,1)}))
# ---- .docx reader helpers ----
net.group('docx reader tier 2')
# open: restore the built in styles and clear the numbering tables
t2z=R()
on('T2_OR0',(None,'T2_OR1',{rb:(as_x(STY0),6*STYN)}))
on('T2_OR1',(None,'T2_OR2',{wb:(as_x(STY),6*STYN),t2z:0,w1:(cb+PSPA,0),w2:(as_x(STY)+6,0)}))
e=S('T2_OR2'); on('T2_OR2',(net.ge(t2z,512,e),'OP1',{w1:(t2cb0+PSPA,DEFSPA)}),(None,'T2_OR2',{w1:(as_x(NUMT)+t2z,0),w2:(as_x(A4PT_)+t2z,0),w3:(as_x(STYX)+t2z,0),t2z:t2z+1}))
# member walk order is in T3_ZN; end of a scanned part moves to the next part
e=S('T2_ZN')
on('T2_ZN',(net.eq(ztarget,6,e),'T3_Z6n',None),(net.eq(ztarget,7,e),'T3_Z7n',None),(None,'OPEND',None))
# A file that sets no line spacing anywhere is single spaced, as in Word: PLSP index 6. docDefaults overwrite the scratch record, and record 0 stands for a paragraph with no style.
on('T3_Z6n',(None,'X_C0',{ztarget:7,zp:zp0,ob:0,obase:OUTP,cb:SCR,ics:as_x(0),t2df:0,t2ps:0,w1:(as_x(SCR)+ALIGN,0),w2:(as_x(SCR)+LIST,0),w3:(as_x(STY)+4,6),wln:(as_x(SCR)+PIND,0,0,6,0,0,0)}))
on('T3_Z7n',(net.step(ONE-t2df),'IMP_DD0',{r1:as_x(SCR)+PLSP}),(None,'IMP_DD2',None))
on('IMP_DD0',(None,'IMP_DD2',{w1:(as_x(STY)+4,R1)}))
on('IMP_DD2',(None,'PX',{ztarget:4,oi:0,ob:vob,obase:OUTB,cb:t2cb0,t2skip:0}))
# attribute search: moves oi to the first value after w:val=" in this tag
e=S('T2_VF1')
on('T2_VF',(None,'T2_VF1',{rl:OA+oi}))
on('T2_VF1',(net.eq(W[0],62,e),'PX',None),(pat('w:val="',e),'T2RR',{oi:oi+7}),(None,'T2_VF',{oi:oi+1}))
# number after the next quote
on('T2_NM',(None,'T2_NM1',{rl:OA+oi}))
e=S('T2_NM1'); on('T2_NM1',(net.eq(W[0],34,e),'T2_NM2',{oi:oi+1,t2n_:0}),(None,'T2_NM',{oi:oi+1}))
on('T2_NM2',(None,'T2_NM3',{rl:OA+oi}))
e=S('T2_NM3'); dg_=net.and_(net.ge(W[0],48,e),net.lt(W[0],58,e))
on('T2_NM3',(dg_,'T2_NM2',{t2n_:t2n_*10+W[0]-48,oi:oi+1}),(net.eq(W[0],45,e),'T2_NM2',{oi:oi+1}),(None,'T2RR',None))
# twips to pixels by repeated subtraction, rounding
t2q=R()
e=S('T2_DV')
on('T2_DV',(net.ge(t2n_,1500,e),'T2_DV',{t2n_:t2n_-1500,t2q:t2q+100}),(net.ge(t2n_,150,e),'T2_DV',{t2n_:t2n_-150,t2q:t2q+10}),(net.ge(t2n_,15,e),'T2_DV',{t2n_:t2n_-15,t2q:t2q+1}),(net.ge(t2n_,8,e),'T2SR',{t2q:t2q+1}),(None,'T2SR',None))
# run property write: decode the current style once per tag
cse=S('T2_C'); CSD=style_decode(cs,cse); hk=net.decode(t2k,10,cse)
_tvf=net.bits(t2v,3,hk[3])
csn=(G_(cs-CSD['bold']*16+t2v*16,hk[0])+G_(cs-CSD['ital']*32+t2v*32,hk[1])+G_(cs-CSD['und']*64+t2v*64,hk[2])+G_(cs-CSD['fontraw']+_tvf[0]*128+_tvf[1]*(1<<22)+_tvf[2]*(1<<23),hk[3])
 +G_(cs-CSD['strike']*ST_STRIKE+t2v*ST_STRIKE,hk[4])+G_(cs-CSD['vert']*ST_VERT+t2v*ST_VERT,hk[5])+G_(cs-CSD['hl']*ST_HL+t2v*ST_HL,hk[6])+G_(cs-CSD['size']+t2v,hk[8])+G_(cs,hk[9]))
tvc=R()
vb_=net.bits(t2v,5,hk[7]); csn=csn+G_(cs-CSD['colraw']+vb_[0]*256+vb_[1]*512+vb_[2]*1024+vb_[3]*131072+vb_[4]*262144,hk[7])
fsm.set(rnop,hk[9],t2v)
for b_,k_ in enumerate((0,1,2,3,7,4,5,6,8)): fsm.set(v4m[b_],hk[k_],1)
on('T2_C',(None,'PX',{ics:(csn,net.relu(ics.k-hk[7]*M)+G_(t2kx,hk[7]),net.relu(ics.n-hk[3]*M)+G_(t2nx,hk[3]),ics.y,*ics.e),t2kx:0,t2nx:0}))
# on or off: a bare tag is on; a value starting 0, f or n is off
on('T2_TV',(None,'T2_TV1',{rl:OA+oi}))
e=S('T2_TV1')
on('T2_TV1',(net.eq(W[0],47,e),'T2_C',{t2v:1}),(None,'T2_TV2',{rl:OA+oi+8}))
e=S('T2_TV2')
on('T2_TV2',(net.or_(net.eq(W[0],48,e),net.eq(W[0],102,e),net.eq(W[0],110,e)),'T2_C',{t2v:0}),(None,'T2_C',{t2v:1}))
e=S('T2_HL'); hv=X()
for i_,nm_ in enumerate(HL_NAMES): hv=hv+pat(nm_[:8],e)*(i_+1)
_p2hx=sum((pat(n_[:8],e)*(j_+1) for j_,(n_,c_) in enumerate(HL_X)),X())   # p2: Word's further highlight names
on('T2_HL',(None,'P2_HLX',{t2k:6,t2v:hv,oi:oi+20,p2xh:_p2hx}))
e=S('T2_VA'); sup_=pat('sup',e); sub_=pat('sub',e)
on('T2_VA',(None,'T2_C',{t2k:5,t2v:sup_+sub_*2,oi:oi+20}))
# spacing and indent attributes
t2fld=R()
on('T2_IN',(net.step(R1),'PX',None),(None,'T2_AT',None))
on('T2_AT',(None,'T2_AT1',{rl:OA+oi}))
e=S('T2_AT1')
def att(p_,fld,nxt='T2_A0'): return (pat(p_,e),'T2_NM',{oi:oi+len(p_)-(1 if p_.endswith('"') else 0),t2fld:fld,t2n_:0,t2rr.r:t2rr.id(nxt)})
on('T2_AT1',(net.eq(W[0],62,e),'PX',None),
 att('w:right=',A4R),att('w:end="',A4R),att('w:before',PSPB),att('w:after=',PSPA),att('w:left="',PIND),att('w:start=',PIND),att('w:firstL',PFIRST,'T2_A2b'),att('w:hangin',PFIRST,'T2_A2'),att('w:line="',PLSP,'T2_A4'),
 (pat('w:lineRu',e),'T2_A6',{rl:OA+oi+12}),(None,'T2_AT',{oi:oi+1}))
on('T2_A0',(None,'T2_DV',{t2q:0,t2sr.r:t2sr.id('T2_A1')}))
on('T2_A1',(None,'T2_AT',{w1:(cb+t2fld,t2q)}))
on('T2_A2',(None,'T2_DV',{t2q:0,t2sr.r:t2sr.id('T2_A3')}))
on('T2_A3',(None,'T2_AT',{w1:(cb+t2fld,as_x(PFO)-t2q)}))
on('T2_A2b',(None,'T2_DV',{t2q:0,t2sr.r:t2sr.id('T2_A3b')}))
on('T2_A3b',(None,'T2_AT',{w1:(cb+t2fld,as_x(PFO)+t2q)}))
e=S('T2_A4'); lv_=net.gt(t2n_,267,e)+net.gt(t2n_,300,e)+net.gt(t2n_,420,e)+net.gt(t2n_,540,e)+net.gt(t2n_,660,e)+(e-net.gt(t2n_,250,e))*6   # 240 true single, 259 the default
on('T2_A4',(net.step(t2lk),'T2_AT',{w1:(cb+PLSP,net.min_(t2n_,4095)+t2lk*4096),t2lk:0}),(None,'T2_AT',{w1:(cb+PLSP,lv_),t2lnv:net.min_(t2n_,4095),t2lh:1}))
e=S('T2_A6'); _ex=net.eq(W[0],101,e); _al=net.and_(net.eq(W[0],97,e),net.eq(W[1],116,e)); _lkv=_ex*1+_al*2; notauto=net.or_(_ex,_al)
on('T2_A6',(net.and_(notauto,t2lh),'T2_AT',{oi:oi+12,w1:(cb+PLSP,t2lnv+_lkv*4096),t2lh:0}),(notauto,'T2_AT',{oi:oi+12,t2lk:_lkv}),(None,'T2_AT',{oi:oi+12,t2lh:0}))
# numbering part
t2an=R();t2nx=R();t2lv=R();t2il=R()
e=S('T2_AB'); isdef=pat('actNum ',e); isref=pat('actNumId',e)
on('T2_AB',(isdef,'T2_NM',{oi:oi+8,t2n_:0,t2rr.r:t2rr.id('T2_AB2')}),(isref,'T2_NM',{oi:oi+8,t2n_:0,t2rr.r:t2rr.id('T2_AB3')}),(None,'PX',{oi:oi+8}))
on('T2_AB2',(None,'PX',{t2an:net.min_(t2n_,255)}))
on('T2_AB3',(None,'T2_AB4',{r1:as_x(NUMT)+256+net.min_(t2n_,255)}))
on('T2_AB4',(None,'PX',{w1:(as_x(NUMT)+t2nx,R1)}))
on('T2_NX',(None,'PX',{t2nx:net.min_(t2n_,255)}))
on('T2_LV',(None,'PX',{t2lv:t2n_}))
e=S('T2_FM'); on('T2_FM',(None,'PX',{oi:oi+18,v6nf:lpat('lowerLet',e)+lpat('upperLet',e)*2+lpat('lowerRom',e)*3+lpat('upperRom',e)*4+lpat('bullet',e)*5}))
on('T2_IL',(None,'PX',{t2il:net.min_(t2n_,2)}))
on('T2_NI',(None,'T2_NI1',{r1:as_x(NUMT)+net.min_(t2n_,255)}))
e=S('T2_NI1'); _ib=net.bits(R1,18,e); _il=net.decode(t2il,3,e); _F=sum((_il[j_]*0 for j_ in range(0)),X())
for j_ in range(3): _F=_F+G_(sum((_ib[6*j_+b_]*(1<<b_) for b_ in range(6)),X()),_il[j_])
_fnum=net.step(net.and_(net.ge(_F,1,e),net.lt(_F,13,e))+net.eq(_F,62,e)); kd=e+_fnum+G_(_F,net.lt(_F,20,e))*16
_p2r=net.and_(e,_fnum,net.step(t2n_),ONE-net.eq(t2n_,p2ln,e))   # p2: a numbered list item with a numId other than the last numbered one restarts, as Word numbers per numId
on('T2_NI1',(net.step(t2n_),'PX',{w1:(cb+LIST,kd+t2il*4),w2:(cb+PIND,0),w3:(cb+PFIRST,0),w4:(cb+F1PX,f1pc+f1pw*2+_p2r*0.25),p2rsr:_p2r,p2ln:G_(t2n_,_fnum)+G_(p2ln,e-_fnum),t2il:0}),(None,'PX',{w1:(cb+LIST,0),t2il:0}))
# style part
t2ido=R();t2oi=R();t2i=R();t2jj=R();t2fnd=R()
e=S('T2_STQ'); on('T2_STQ',(net.or_(net.eq(W[0],32,e),net.eq(W[0],62,e)),'T2_ST0',{oi:oi+8}),(None,'PX',{oi:oi+8}))
on('T2_ST0',(net.step(ONE-t2df),'T2_SW',{t2si:DEFREC,t2df:1,t2rr.r:t2rr.id('IMP_DD1')}),(None,'T2_ST0b',None))
on('IMP_DD1',(None,'IMP_DD3',{r1:as_x(SCR)+PLSP}))
on('IMP_DD3',(None,'T2_ST0b',{w1:(as_x(STY)+4,R1)}))
t2chr=R()
on('T2_ST0b',(None,'T2_ST',{t2skip:1,t2ido:0,t2chr:0,ics:(cs,ics.k,ics.n,ics.y),**{m_:0 for m_ in v4m}}))   # p2: a style's extended field starts empty
on('T2_ST',(None,'T2_ST1',{rl:OA+oi}))
e=S('T2_ST1')
on('T2_ST1',(net.eq(W[0],62,e),'T2_ST2',None),(pat('w:type="',e),'T2_ST3',{rl:OA+oi+8}),(pat('w:styleI',e),'T2_ST',{t2ido:oi+11,oi:oi+11}),(None,'T2_ST',{oi:oi+1}))
e=S('T2_ST3'); on('T2_ST3',(pat('paragrap',e),'T2_ST',{t2skip:0,oi:oi+8}),(pat('characte',e),'T2_ST',{t2skip:0,t2chr:1,oi:oi+8}),(pat('table"',e),'T2_ST',{t2skip:0,t2chr:2,oi:oi+8}),(None,'T2_ST',{oi:oi+8}))
on('T2_ST2',(t2skip,'PX',None),(None,'T2_FS',{t2oi:oi,oi:t2ido,t2i:0,t2jj:0,a5d:1,t2rr.r:t2rr.id('T2_ST4')}))
# id search: compares the string at oi against each table id
e=S('T2_FS'); on('T2_FS',(net.ge(t2i,G_(nsty,ONE-a5d)+a5d*6,e),'T2RR',{t2fnd:0}),(None,'T2_FS1',{r1:as_x(STY)+t2i*STYN+8+t2jj,r2:OA+oi+t2jj}))
e=S('T2_FS1'); q_=net.eq(R2,34,e)
_lim=G_(nsty,ONE-a5d)+a5d*6   # the next read goes out with the verdict, so each compare takes one tick
on('T2_FS1',(net.and_(q_,net.eq(R1,0,e)),'T2RR',{t2fnd:1}),(net.and_(ONE-q_,net.eq(R1,R2,e)),'T2_FS1',{t2jj:t2jj+1,r1:as_x(STY)+t2i*STYN+8+t2jj+1,r2:OA+oi+t2jj+1}),
 (net.ge(t2i+1,_lim,e),'T2RR',{t2i:t2i+1,t2jj:0,t2fnd:0}),(None,'T2_FS1',{t2i:t2i+1,t2jj:0,r1:as_x(STY)+(t2i+1)*STYN+8,r2:OA+oi}))
e=S('T2_ST4')
on('T2_ST4',(t2fnd,'T2_ST9',{t2si:t2i,a5d:0}),(net.lt(nsty,STYMAX,e),'T2_ST5',{t2si:nsty,nsty:nsty+1,t2jj:0,a5d:0}),(None,'T2_ST9',{t2si:DEFREC+1,a5d:0}))
on('T2_ST5',(None,'T2_ST6',{r1:OA+oi+t2jj}))
e=S('T2_ST6'); on('T2_ST6',(net.or_(net.eq(R1,34,e),net.ge(t2jj,19,e)),'T2_ST9',{w1:(as_x(STY)+t2si*STYN+8+t2jj,0)}),(None,'T2_ST5',{w1:(as_x(STY)+t2si*STYN+8+t2jj,R1),t2jj:t2jj+1}))
on('T2_ST9',(None,'T2_AP',{oi:t2oi,t2i:DEFREC,w1:(as_x(STY)+t2si*STYN+46,0)}))
on('T2_NA',(t2skip,'PX',None),(None,'T2_NA1',{t2jj:0}))
on('T2_NA1',(None,'T2_NA2',{r1:OA+oi+t2jj}))
e=S('T2_NA2'); on('T2_NA2',(net.or_(net.eq(R1,34,e),net.ge(t2jj,17,e)),'PX',{w1:(as_x(STY)+t2si*STYN+28+t2jj,0),oi:oi+t2jj}),(None,'T2_NA1',{w1:(as_x(STY)+t2si*STYN+28+t2jj,R1),t2jj:t2jj+1}))
# save the scratch record into the table
on('T2_SW',(None,'T2_SW1',{rl:as_x(SCR)+ALIGN,rp6:as_x(SCR)+PIND}))
on('V4_SW2',(None,'T2RR',{w3:(as_x(STYX)+t2si*4+3,ics.e[0]),w1:(as_x(STYX)+t2si*4+1,ics.n),w2:(as_x(STYX)+t2si*4+2,sum((v4m[b_]*(1<<b_) for b_ in range(9)),X()))}))
on('T2_SW1',(None,'V4_SW2',{w4:(as_x(STYX)+t2si*4,ics.k),wln:(as_x(STY)+t2si*STYN,cs,rl.out[0],rp6.out[0],rp6.out[1],rp6.out[2],rp6.out[3]),w1:(as_x(STY)+t2si*STYN+6,rp6.out[4]),w2:(as_x(STY)+t2si*STYN+7,rl.out[1]),w3:(as_x(STY)+t2si*STYN+47,t2chr)}))
on('T2_SC',(None,'PX',{t2skip:0}))
# a run style reference: the run starts from the character style's properties
on('T2_RS1',(None,'T2_FS',{t2i:0,t2jj:0,t2rr.r:t2rr.id('T2_RS2')}))
on('T2_RS2',(t2fnd,'T2_RS3',{rl:as_x(STY)+t2i*STYN,r1:as_x(STYX)+t2i*4,r2:as_x(STYX)+t2i*4+1,rU:as_x(STYX)+t2i*4+2}),(None,'PX',None))
e=S('T2_RS3'); _rmb=net.bits(rU.out[0],9,e)
on('T2_RS3',(None,'PX',{ics:(style_over(cs,style_decode(cs,e),style_decode(W[0],e),_rmb),net.relu(ics.k-_rmb[4]*M)+G_(R1,_rmb[4]),net.relu(ics.n-_rmb[3]*M)+G_(R2,_rmb[3]),t2i+1)}))
# paragraph style reference, also basedOn: apply a table record to the current record
fsm.set(p2bo,S('T2_PS1'),1); fsm.set(p2bo,S('T2_PR'),0)   # p2: only a basedOn or pStyle reference merges the base's mask, not the paragraph default
on('T2_PS1',(None,'T2_FS',{t2i:0,t2jj:0,t2rr.r:t2rr.id('T2_PS2')}))
on('T2_PS2',(t2fnd,'T2_AP',None),(None,'PX',None))
on('T2_PR',(None,'T2_AP',{t2i:G_(a5ts,incell),a5ns:incell,a4rsn:0,a4inb:0,a4inr:0,wvl:(cb+A4K,0,0,0,a4rhc,0,0),wht:(cb+A4T,0,0,0,0,0,0)}))
on('T2_AP',(None,'T2_AP1',{rl:as_x(STY)+t2i*STYN,r1:as_x(STYX)+t2i*4,r2:as_x(STYX)+t2i*4+1,rU:as_x(STYX)+t2i*4+2,rV:as_x(STYX)+t2i*4+3}))   # p2: the fourth cell is the style's extended field
e=S('T2_AP1'); _p2bm=net.bits(rU.out[0],9,net.and_(e,p2bo))   # p2: a style based on a character style also takes the fields its base sets
on('T2_AP1',(None,'PX',{**{m_:net.or_(m_,b_) for m_,b_ in zip(v4m,_p2bm)},t2il:0,t2ps:W[0],t2pK:R1,t2pN:R2,p2pe:rV.out[0],ics:(W[0],R1,R2,X(),rV.out[0]),w1:(cb+ALIGN,W[1]),w2:(cb+LIST,W[7]),a5ns:0,wln:(cb+PIND,W[2],W[3],W[4],W[5],W[6],G_(t2i,ONE-a5ns))}))
# PDF list markers, in the page's pixel coordinates
e=S('T2_PM'); on('T2_PM',(net.and_(net.eq(qs,0,e),net.step(qk)),'T2_PMa',None),(None,'PD_R',None))
lit('T2_PMa',b'BT /F0 15 Tf 0 0 0 rg 1 0 0 1 ','T2_PMb')
e=S('T2_PMb'); number('T2_PMb',qx+qind+qxc-20-net.eq(qk,2,e)*6,'T2_PMc'); lit('T2_PMc',b' ','T2_PMd')
number('T2_PMd',qyb,'T2_PMe'); lit('T2_PMe',b' Tm (','T2_PMf')
e=S('T2_PMf'); _lm=list_mark(v6qf,e); on('T2_PMf',(net.eq(qk,1,e),'T2_PMg',None),(net.step(_lm[2]),'V6_PE',{qi:0}),(None,'T2_PMh',{qi:0}))
lit('V6_PE',b'\\(','T2_PMh')
e=S('T2_PMg'); bq=net.decode(ql,4,net.and_(e,ONE-net.step(v6qf))); _lm=list_mark(v6qf,e); em_en.lin(e); em_b.add(e,bq[0]*149+bq[1]*111+bq[2]*150+bq[3]*150+_lm[4]+net.eq(_lm[4],127,e)*22)
on('T2_PMg',(None,'T2_PMz',None))
e=S('T2_PMh'); _lm=list_mark(v6qf,e); on('T2_PMh',(None,'T2_PMi',{r1:as_x(MKT)+(_lm[0]+G_(net.min_(ql,2),ONE-net.step(v6qf)))*2048+qmk*8+qi}))
e=S('T2_PMi'); _lm=list_mark(v6qf,e); _dot=net.eq(R1,46,e); _sf=_lm[3]+G_(as_x(46),ONE-net.step(v6qf)); _go0=net.and_(e,net.step(R1),ONE-net.and_(_dot,ONE-net.step(_sf))); _par=net.and_(_dot,net.eq(_sf,41,e)); _go=_go0-net.and_(_go0,_par)
em_en.lin(_go); em_b.add(_go,R1-net.and_(_lm[1],net.ge(R1,97,e))*32+G_(_sf,_dot)-_dot*46)
on('T2_PMi',(_par,'V6_PF',None),(_go0,'T2_PMh',{qi:qi+1}),(None,'T2_PMz',None))
lit('V6_PF',b'\\)','T2_PMz')
lit('T2_PMz',b')Tj ET\n','PD_R')
