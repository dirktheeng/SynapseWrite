# ---- imp6: F4 repeats the last formatting command ----
# i6lk names the last command that can be repeated: 1 a character format (FMTS, its registers fm, fcol, fsi, fhl
# and the rest still hold the last values), 2 alignment, 3 a paragraph style, 4 a list. F4 enters that command again.
i6lk=R()
def imp6_key_rules(KD,ND): return [(ND(139),'IMP6_RP',None)]
