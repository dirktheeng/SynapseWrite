# ---- imp5: column breaks ----
# A paragraph record's PBRK holds 1 for a page break before it and 2 for a column break before it. Layout (R3B) moves a
# column break paragraph to the second column when it starts in the first of two; anywhere else it breaks the page, as in Word.
net.group('column breaks')
# Ctrl+Shift+Enter: split at the caret like Ctrl+Enter, then mark the new paragraph, with an undo record
on('IMP5_CB0',(has_sel,'DS0',{dret.r:dret.id('IMP5_CB1')}),(None,'IMP5_CB1',None))
on('IMP5_CB1',(None,'SPLIT',{oret.r:oret.id('IMP5_CB2')}))
log(S('IMP5_CB2'),6,cp,PBRK,0,2)
on('IMP5_CB2',(None,'AFTER_ED',{w1:(cb+PBRK,2)}))
# save: the break is a run of its own at the head of the paragraph
on('IMP5_SC',(net.eq(pbk,2,S('IMP5_SC')),'IMP5_SCL',None),(None,'T3_SNG',None))
lit('IMP5_SCL',b'<w:r><w:br w:type="column"/></w:r>','T3_SNG')
# open: a column break inside a run splits the paragraph there and marks the second part
e=S('IMP5_CR'); on('IMP5_CR',(net.and_(net.step(clen),ONE-incell),'SPLIT',{oret.r:oret.id('IMP5_CR2')}),(None,'IMP5_CR2',None))
on('IMP5_CR2',(None,'PX',{w1:(cb+PBRK,2)}))
