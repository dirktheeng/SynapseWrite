# ---- p1: Ctrl+Alt shortcuts, as one key rule after the Ctrl ones of rv_key_rules, which leave Ctrl+Alt alone, and ahead of the plain Ctrl ones in app.py ----
# The input network cooks Alt held with Ctrl or Cmd into bit 2 of the modifier word (p1_alt, from the key state's bits). Ctrl+Alt+1, 2, 3 apply Heading 1 to 3 (style indexes 2 to 4); Ctrl+Alt+M
# opens a comment; Ctrl+Alt+F inserts a footnote; Ctrl+Alt+C, R, T and . type the copyright, registered and trade mark signs
# and an ellipsis (internal codes are Windows-1252: 169, 174, 153, 133). One rule in the key state takes every Ctrl+Alt key, so a
# plain key pays for one small condition; P1_ALT then picks the command from the key code, which stays in eva. Any other
# printable Ctrl+Alt key types its character: AltGr arrives as Ctrl+Alt, and is how many keyboards type @, the euro sign or braces.
P1_ALTK=[(ord('1'),'T2_SA0',{'t2si':2}),(ord('2'),'T2_SA0',{'t2si':3}),(ord('3'),'T2_SA0',{'t2si':4}),(ord('m'),'RD0',{'mode':4,'field':0}),
 (ord('f'),'T3_C_FN',None),(ord('c'),'TYPE',{'eva':169}),(ord('r'),'TYPE',{'eva':174}),(ord('t'),'TYPE',{'eva':153}),(ord('.'),'TYPE',{'eva':133})]
def p1_key_rules(KD,ND):
    return [(net.and_(ctrl,p1_alt,ONE-findon),'P1_ALT',None)]
def p1_alt_state():
    e_=S('P1_ALT'); rr=[]
    for c_,st_,a_ in P1_ALTK: rr.append((net.eq(eva,c_,e_),st_,{globals()[n_]:v_ for n_,v_ in a_.items()} if a_ else None))
    pr_=net.or_(net.and_(net.ge(eva,32,e_),net.lt(eva,127,e_)),net.and_(net.ge(eva,160,e_),net.lt(eva,256,e_)),net.ge(eva,256,e_))
    on('P1_ALT',*rr,(pr_,'TYPE',None),(None,'HALT',None))
