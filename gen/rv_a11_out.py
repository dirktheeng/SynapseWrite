# ---- file output: one length, one data base, and the file name as a table entry the network selects ----
net.group('file output command')
c_file=Bus(net); c_file.lin(saveout.w+pdfout.w)
_sa,_sb=net.step(saveout.w),net.step(pdfout.w)
c_namea=Bus(net); c_namea.lin(_sa*NAMEB+_sb*(NAMEB+len(NAME_DOCX)))
c_namen=Bus(net); c_namen.lin(_sa*len(NAME_DOCX)+_sb*len(NAME_PDF))
# ---- screen against document: on each blink tick one line of the table is checked on the screen ----
# Every drawn line holds a nonzero object id at its left end, so a zero there means the image no longer
# shows the layout the network holds. That forces a full repaint. One line per tick, three ticks of work.
net.group('screen check')
a11chk=R(); a11bad=R()
e=S('A11_C0')
on('A11_C0',(net.or_(net.eq(vln,0,e),bstg),'RD0',{fastok:1}),(net.ge(a11chk,vln,e),'A11_C0',{a11chk:0}),(None,'A11_C1',{rl:as_x(VL)+a11chk*6}))
e=S('A11_C1')
on('A11_C1',(net.and_(net.ge(RL[0],DOCY,e),net.lt(RL[0],DOCB,e)),'A11_C2',{pix:(RL[4],RL[0]),a11chk:a11chk+1}),(None,'RD0',{fastok:1,a11chk:a11chk+1}))
e=S('A11_C2')
on('A11_C2',(net.eq(pix.out[3],0,e),'RD0',{a11bad:a11bad+1}),(None,'RD0',{fastok:1}))
