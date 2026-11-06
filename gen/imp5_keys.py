# ---- imp5: more Word shortcuts, as key rules ahead of the plain ones ----
# Ctrl+Shift+Space types a no-break space, Ctrl+Shift+- (key "_") a no-break hyphen U+2011, Ctrl+Shift+E turns tracking on or off,
# Ctrl+Shift+8 (key "*") shows or hides marks, F9 updates fields, Ctrl+Shift+F and Ctrl+Shift+P open the font and size menus.
def imp5_key_rules(KD,ND):
    return [(net.and_(KD(32),shf),'TYPE',{eva:160}),(KD(ord('_')),'T2_KU',{eva:0x2011}),
     (net.and_(KD(ord('e')),shf),'RD0',{trk:ONE-trk}),(KD(ord('*')),'IMP3_MK',None),(ND(138),'T4_FU',{grp:grp+1}),
     (net.and_(KD(ord('f')),shf),'T1_M0',{t1_mop:1,t1_mrow:99,t1_mtop:87,clip0:0,clip1:0}),
     (net.and_(KD(ord('p')),shf),'T1_M0',{t1_mop:2,t1_mrow:99,t1_mtop:87,clip0:0,clip1:0})]
