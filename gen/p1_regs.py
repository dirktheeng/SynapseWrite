# ---- p1 (tier 1): registers ----
# qcod counts Word find codes other than ^p in the query (^t ^l ^^ ^s ^- ^? ^# ^$); p1k is the kind of the code being matched:
# 0 a literal character in xc, 1 any character, 2 any digit, 3 any letter.
qcod=R();p1k=R()
exec(open('p1_keys.py').read())
# ---- p1: the clipboard as HTML. One bank region holds the HTML the network writes on copy, and the HTML the glue hands in on paste ----
P1HB=14400000; P1HMAX=98000; P1ST=14499000; region('p1 clipboard HTML',P1HB,P1HB+P1HMAX+8); region('p1 paste format stack',P1ST,P1ST+8*32)
p1_htmlout=Bus(net); p1hl=R()
p1hi,p1hk,p1hs,p1ho,p1hc,p1fb,p1fi,p1fu,p1fp,p1fc,p1fk,p1fn,p1ff=[R() for _ in range(13)]
p1hm,p1rn,p1pt,p1pb,p1sp,p1d,p1ch,p1vk,p1pc,p1sk,p1nv,p1nf,p1nd,p1rk,p1so,p1fy,p1al,p1j=[R() for _ in range(18)]
p1c=[R() for _ in range(3)]
p1lo,p1nk,p1lk,p1li=[R() for _ in range(4)]
P1_SYX,P1_SYY=1092,87   # Insert > Symbol menu position (gen/p1_menus.py)
p1wcm=R()   # Review > Word Count message: timer ticks left to show it, as pmsg
