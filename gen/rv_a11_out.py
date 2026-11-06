# ---- file output: one length, one data base, and the file name as a table entry the network selects ----
net.group('file output command')
c_file=Bus(net); c_file.lin(saveout.w+pdfout.w)
_sa,_sb=net.step(saveout.w),net.step(pdfout.w)
c_namea=Bus(net); c_namea.lin(_sa*NAMEB+_sb*(NAMEB+len(NAME_DOCX)))
c_namen=Bus(net); c_namen.lin(_sa*len(NAME_DOCX)+_sb*len(NAME_PDF))
