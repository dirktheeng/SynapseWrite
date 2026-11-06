# Reviewer a3: states behind rv_key_rules, shift click, margin selection, drag autoscroll, context menu, change case.
net.group('rv a3 interaction')
def rv_ws(v,en_): return net.or_(net.eq(v,32,en_),net.eq(v,9,en_),net.eq(v,11,en_))
def rv_cls(v,en_):
    "Character class for word moves: 0 white space, 1 word, 2 punctuation."
    s_=rv_ws(v,en_); w_=t1_isw(v,en_); return w_+(en_-w_-s_)*2
# word moves and word deletes share one walker; rv_wm 1 turns the range into a selection and deletes it
e=S('RVA3_ML'); on('RVA3_ML',(net.step(co),'RVA3_WL0',{rv_wm:0,t1_s:co}),(net.step(cp),'MVJ',{jp:cp-1,jo:2047,jret.r:jret.id('MVEND')}),(None,'MVEND',None))
e=S('RVA3_MR'); on('RVA3_MR',(net.lt(co,clen,e),'RVA3_WR0',{rv_wm:0,t1_e:co}),(net.lt(cp+1,npar,e),'MVJ',{jp:cp+1,jo:0,jret.r:jret.id('MVEND')}),(None,'MVEND',None))
e=S('RVA3_KB'); on('RVA3_KB',(net.or_(has_sel,net.eq(co,0,e)),'BKSP',{grp:grp+1,t1_lastk:0}),(None,'RVA3_WL0',{rv_wm:1,t1_s:co,grp:grp+1,t1_lastk:0}))
e=S('RVA3_KD'); on('RVA3_KD',(net.or_(has_sel,net.ge(co,clen,e)),'DELK',{grp:grp+1,t1_lastk:0}),(None,'RVA3_WR0',{rv_wm:1,t1_e:co,grp:grp+1,t1_lastk:0}))
e=S('RVA3_WL0'); on('RVA3_WL0',(net.eq(t1_s,0,e),'RVA3_LE',None),(None,'RVA3_WL1',{r1:cb+t1_s-1}))
e=S('RVA3_WL1'); on('RVA3_WL1',(rv_ws(R1,e),'RVA3_WL0',{t1_s:t1_s-1}),(None,'RVA3_WL2',{t1_c:rv_cls(R1,e),t1_s:t1_s-1}))
e=S('RVA3_WL2'); on('RVA3_WL2',(net.eq(t1_s,0,e),'RVA3_LE',None),(None,'RVA3_WL3',{r1:cb+t1_s-1}))
e=S('RVA3_WL3'); on('RVA3_WL3',(net.eq(rv_cls(R1,e),t1_c,e),'RVA3_WL2',{t1_s:t1_s-1}),(None,'RVA3_LE',None))
on('RVA3_LE',(rv_wm,'DS0',{ap:cp,ao:t1_s,rv_wm:0,dret.r:dret.id('AFTER_ED')}),(None,'MVEND',{co:t1_s}))
e=S('RVA3_WR0'); on('RVA3_WR0',(net.ge(t1_e,clen,e),'RVA3_RE',None),(None,'RVA3_WR1',{r1:cb+t1_e}))
e=S('RVA3_WR1'); on('RVA3_WR1',(rv_ws(R1,e),'RVA3_WRS',None),(None,'RVA3_WR2',{t1_c:rv_cls(R1,e),t1_e:t1_e+1}))
e=S('RVA3_WR2'); on('RVA3_WR2',(net.ge(t1_e,clen,e),'RVA3_RE',None),(None,'RVA3_WR3',{r1:cb+t1_e}))
e=S('RVA3_WR3'); on('RVA3_WR3',(net.eq(rv_cls(R1,e),t1_c,e),'RVA3_WR2',{t1_e:t1_e+1}),(None,'RVA3_WRS',None))
e=S('RVA3_WRS'); on('RVA3_WRS',(net.ge(t1_e,clen,e),'RVA3_RE',None),(None,'RVA3_WRT',{r1:cb+t1_e}))
e=S('RVA3_WRT'); on('RVA3_WRT',(rv_ws(R1,e),'RVA3_WRS',{t1_e:t1_e+1}),(None,'RVA3_RE',None))
on('RVA3_RE',(rv_wm,'DS0',{ap:cp,ao:co,co:t1_e,rv_wm:0,dret.r:dret.id('AFTER_ED')}),(None,'MVEND',{co:t1_e}))
# paragraph moves
e=S('RVA3_PU'); on('RVA3_PU',(net.step(co),'MVEND',{co:0}),(net.step(cp),'MVJ',{jp:cp-1,jo:0,jret.r:jret.id('MVEND')}),(None,'MVEND',None))
e=S('RVA3_PD'); on('RVA3_PD',(net.lt(cp+1,npar,e),'MVJ',{jp:cp+1,jo:0,jret.r:jret.id('MVEND')}),(None,'MVEND',{co:clen}))
# page moves: scroll a screen, repaint, then find the line under the caret's screen position in the new image
e=S('RVA3_PG1'); same_=net.eq(scroll,rv_s0,e)
on('RVA3_PG1',(net.and_(same_,rv_pgd),'MVJ',{jp:net.relu(npar-1),jo:2047,jret.r:jret.id('MVEND')}),(same_,'MVJ',{jp:0,jo:0,jret.r:jret.id('MVEND')}),
 (rv_pgd,'HT',{hx_:zfx0(cx),hy_:rv_py,hdir:1,hact:1}),(None,'HT',{hx_:zfx0(cx),hy_:rv_py,hdir:2,hact:1}))
# overtype: delete the character ahead, then insert as usual
on('RVA3_OV',(None,'INS',{ins_ch:eva,ins_st:TST,oret.r:oret.id('AF_FAST')}))
# find next
e=S('RVA3_F3'); on('RVA3_F3',(net.step(qlen),'FN1',{fp:hi_p,fo:hi_o,wrap:0}),(None,'RD0',{mode:1,field:0,qrep:1,**CSTART}))
# drag autoscroll: the timer keeps firing while the pointer rests past the top or bottom of the document
e=S('RVA3_AS0'); rv_up=net.lt(mp_pty,DOCY+8,e); rv_d=G_(as_x(DOCY+8)-mp_pty,rv_up)+G_(mp_pty-(DOCB-8),e-rv_up); rv_sp=e*16+net.min_(rv_d,120)
on('RVA3_AS0',(rv_up,'RD0',{scroll:net.relu(scroll-rv_sp),rv_asq:1,autos:0}),(None,'RD0',{scroll:scroll+rv_sp,rv_asq:1,autos:0}))
on('RVA3_AS1',(None,'MD2',{hx_:net.max_(net.min_(mp_ptx,zfx0(s_px+s_pw-2)),zfx0(s_px+1)),hy_:net.max_(net.min_(mp_pty,DOCB-6),DOCY+6),shiftk:1}))
# right click: place the caret unless it lands in the selection, then open the menu at the pointer
e=S('RVA3_RC0'); on('RVA3_RC0',(net.or_(net.lt(hy_,DOCY,e),net.ge(hy_,DOCB,e),net.ge(hx_,1262,e)),'HALT',None),(None,'RVA3_RC1',{pix:(hx_,hy_)}))
e=S('RVA3_RC1'); on('RVA3_RC1',(net.ge(A_,200,e),'HALT',None),(None,'HT',{hdir:3,hact:0,vi:0,drag:0,shiftk:0,t1_clk:1,rv_cmq:1,rv_sL:Lo,rv_sH:Hi,rv_sh:has_sel,rv_scp:cp,rv_sco:co,rv_sap:ap,rv_sao:ao}))
e=S('RVA3_CM1'); rv_in=net.and_(rv_sh,net.ge(Kc,rv_sL,e),net.ge(rv_sH,Kc,e))
on('RVA3_CM1',(rv_in,'MVJ',{jp:rv_scp,jo:rv_sco,jret.r:jret.id('RVA3_CM3')}),(None,'RD0',{ap:cp,ao:co,drag:0,blink:0}))
on('RVA3_CM3',(None,'RD0',{ap:rv_sap,ao:rv_sao,drag:0,blink:0}))
e=S('RVA3_CM2'); on('RVA3_CM2',(net.or_(has_sel,net.gt(hx_,cx+4,e)),'RVA3_CMM',{rv_cmq:0,drag:0}),(None,'A6S_0',{rv_cmq:0,drag:0,a6cm:1}))
on('RVA3_CMM',(None,'T1_M0',{a6cm:0,t1_mop:12,t1_mrow:99,t1_mtop:net.min_(mp_pty,DOCB-RH*8-4),t1_mx:net.min_(mp_ptx,1262-170),clip0:0,clip1:0}))
RV_MENU=['Cut','Copy','Paste','Select All','Bold','Italic','Underline','Find']
cur_='RVA3_MM0'
on(cur_,(None,'RVA3_MMa',{rA:(t1_mx+2,t1_mtop+2,171,RH*8+1,(200,198,196),0),rB:(t1_mx-1,t1_mtop-1,172,RH*8+2,(150,148,146),0)}))
cur_='RVA3_MMa'
for r_,lb_ in enumerate(RV_MENU):
    e=S(cur_); hv_=net.eq(t1_mrow,r_,e); nx_=f'RVA3_MM{r_}_0'
    on(cur_,(None,nx_,{rA:(t1_mx,t1_mtop+r_*RH,170,RH,tuple(e*255-hv_*(255-PAL_B[5][i_]) for i_ in range(3)),254),sx:t1_mx+8}))
    cur_=nx_
    for j_,rv_c_ in enumerate(lb_):
        nx_=f'RVA3_MM{r_}_{j_+1}'; e=S(cur_); hv_=net.eq(t1_mrow,r_,e); bg[5].lin(hv_); bg[0].lin(e-hv_)
        on(cur_,(None,nx_,{gly:(ord(rv_c_),9,sx,t1_mtop+r_*RH+2,0,None),sx:sx+adv})); cur_=nx_
on(cur_,(None,'T1_END',None))
# change case of the selection with Shift+F3, cycling upper, lower, title. Each change is a delete and an insert, so undo works.
e=S('RVA3_CC0'); on('RVA3_CC0',(has_sel,'MVJ',{jp:lo_p,jo:lo_o,rv_chi:Hi,rv_cap:lo_p,rv_cao:lo_o,rv_ctp:1,grp:grp+1,t1_lastk:0,jret.r:jret.id('RVA3_CC1')}),(None,'HALT',None))
e=S('RVA3_CC1'); on('RVA3_CC1',(net.ge(Kc,rv_chi,e),'RVA3_CC9',None),(net.ge(co,clen,e),'MVJ',{jp:cp+1,jo:0,rv_ctp:1,jret.r:jret.id('RVA3_CC1')}),(None,'RVA3_CC2',{r1:cb+co,r2:cb+1024+co}))
e=S('RVA3_CC2'); isup=net.or_(net.and_(net.ge(R1,65,e),net.lt(R1,91,e)),net.and_(net.ge(R1,192,e),net.lt(R1,223,e),ONE-net.eq(R1,215,e))); islo=net.or_(net.and_(net.ge(R1,97,e),net.lt(R1,123,e)),net.and_(net.ge(R1,224,e),net.lt(R1,255,e),ONE-net.eq(R1,247,e)))
rv_ch=net.decode(rv_cc,3,e); want_up=net.or_(rv_ch[0],net.and_(rv_ch[2],rv_ctp)); want_lo=e-want_up
nc_=R1+net.and_(islo,want_up)*(-32)+net.and_(isup,want_lo)*32
chg_=net.or_(net.and_(islo,want_up),net.and_(isup,want_lo))
on('RVA3_CC2',(chg_,'DEL',{rv_nc:nc_,rv_st:R2,rv_ctp:ONE-t1_isw(R1,e),oret.r:oret.id('RVA3_CC3')}),(None,'RVA3_CC1',{co:co+1,rv_ctp:ONE-t1_isw(R1,e)}))
on('RVA3_CC3',(None,'INS',{ins_ch:rv_nc,ins_st:rv_st,oret.r:oret.id('RVA3_CC1')}))
e=S('RVA3_CC9'); rv_cn=net.decode(rv_cc,3,e)
on('RVA3_CC9',(None,'RD0',{ap:rv_cap,ao:rv_cao,rv_cc:rv_cn[0]*1+rv_cn[1]*2,lc:1}))
# forced line break at the very end of a paragraph leaves an empty last line
e=S('RVA3_LE0'); measure(e,32,ty)
on('RVA3_LE0',(None,'EM',{lasc:asc,lhh:lh,lend:off,lwid:0,lspc:0,llast:1}))
# docx: tab and forced line break
lit('RVA3_ST',b'</w:t><w:tab/><w:t xml:space="preserve">','SVC'); lit('RVA3_SB',b'</w:t><w:br/><w:t xml:space="preserve">','SVC')
on('RVA3_RBR',(None,'INS',{ins_ch:11,ins_st:csi+rhi,oret.r:oret.id('PX')}))
