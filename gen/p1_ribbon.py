# ---- p1: states behind the new ribbon commands (gen/p1_btn.py) ----
_gp1r=net.cur[0]; net.group('tier 1 ribbon commands')
p1_alt_state()
on('P1_CB',(None,'IMP5_CB0',{grp:grp+1,t1_lastk:0}))   # column break, as Ctrl+Shift+Enter
on('P1_TW',(None,'TYPE',{eva:11}))                     # text wrapping break: with no floating objects it is a line break, as Shift+Enter
on('P1_CM',(None,'RD0',{mode:4,field:0}))              # comment, as Review > Comment
net.group(_gp1r)
