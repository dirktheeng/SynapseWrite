# ---- p1: Ctrl+Alt shortcuts, as key rules ahead of the Ctrl ones (Ctrl+Alt+1 is a heading, not single spacing) ----
# The glue sends Alt as bit 16 of the modifier word. Ctrl+Alt+1, 2, 3 apply Heading 1 to 3; Ctrl+Alt+M opens a comment;
# (style indexes: 2, 3, 4 are Heading 1 to 3). Ctrl+Alt+F inserts a footnote; Ctrl+Alt+C, R, T and . type the copyright, registered and trade mark signs and an ellipsis
# (internal codes are Windows-1252: 169, 174, 153, 133).
def p1_key_rules(KD,ND):
    alt=net.ge(evb,16,en)
    def KA(c): return net.and_(KD(c),alt)
    return [(KA(ord('1')),'T2_SA0',{t2si:2}),(KA(ord('2')),'T2_SA0',{t2si:3}),(KA(ord('3')),'T2_SA0',{t2si:4}),
     (KA(ord('m')),'RD0',{mode:4,field:0}),(KA(ord('f')),'T3_C_FN',None),
     (KA(ord('c')),'TYPE',{eva:169}),(KA(ord('r')),'TYPE',{eva:174}),(KA(ord('t')),'TYPE',{eva:153}),(KA(ord('.')),'TYPE',{eva:133})]
