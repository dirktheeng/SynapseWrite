# ---- p1: states behind the new ribbon commands (gen/p1_btn.py) ----
_gp1r=net.cur[0]; net.group('tier 1 ribbon commands')
p1_alt_state()
on('P1_CB',(None,'IMP5_CB0',{grp:grp+1,t1_lastk:0}))   # column break, as Ctrl+Shift+Enter
on('P1_TW',(None,'TYPE',{eva:11}))                     # text wrapping break: with no floating objects it is a line break, as Shift+Enter
on('P1_CM',(None,'RD0',{mode:4,field:0}))              # comment, as Review > Comment
on('P1_SY',(None,'T1_M0',{t1_mop:16,t1_mrow:99,t1_mtop:P1_SYY,t1_mx:P1_SYX,clip0:0,clip1:0}))
# Word Count: words and pages as the status bar knows them, paragraphs, and characters with spaces summed from the paragraph lengths
p1wi=R();p1wn=R()
on('P1_WC',(None,'P1_WC1',{p1wi:0,p1wn:0}))
e=S('P1_WC1'); on('P1_WC1',(net.ge(p1wi,npar,e),'RD0',{p1wcm:PMSG}),(None,'P1_WC2',{r1:as_x(PT)+p1wi}))
on('P1_WC2',(None,'P1_WC2b',{r2:R1+LEN})); on('P1_WC2b',(None,'P1_WC1',{p1wn:p1wn+R2,p1wi:p1wi+1}))
text_chain('P1_WM',[p1wn,' characters with spaces, ',npar,' paragraphs'],'T4_ST')
fsm.set(p1wcm,net.and_(kh[7],net.step(p1wcm)),p1wcm-1); fsm.set(p1wcm,net.and_(net.or_(kh[2],kh[3]),net.step(p1wcm)),0)
# Blank Page: a page break, an empty paragraph, a page break, as Word inserts it
on('P1_BP',(None,'SPLIT',{grp:grp+1,oret.r:oret.id('P1_BP1')})); on('P1_BP1',(None,'SPLIT',{w1:(cb+PBRK,1),oret.r:oret.id('P1_BP2')}))
e=S('P1_BP2'); log(e,6,cp,PBRK,0,1); on('P1_BP2',(None,'AFTER_ED',{w1:(cb+PBRK,1)}))
# views: draft and web layout set their flag and lay the whole document out again; print layout clears both
on('P1_VD',(None,'DA0',{p1vdr:1,p1vwb:0,rdm:0,di_:0,clip0:0,clip1:0})); on('P1_VW',(None,'DA0',{p1vdr:0,p1vwb:1,rdm:0,di_:0,clip0:0,clip1:0}))
on('P1_VP',(rdm,'IMP3_RX',{p1vdr:0,p1vwb:0}),(p1vf,'DA0',{p1vdr:0,p1vwb:0,di_:0,clip0:0,clip1:0}),(None,'HALT',None))
net.group(_gp1r)
