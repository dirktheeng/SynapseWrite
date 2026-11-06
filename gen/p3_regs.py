# ---- p3: registers and reader rules for emboss, imprint, outline, shadow, character scale, language and paragraph outline level ----
# Where they live, with no new style cell: the link and bookmark field of a style entry holds the link id in bits 0-7 (F1N is 255),
# a language id in bits 8-11, the bookmark id in bits 12-19, and outline, shadow, emboss, imprint in bits 20-23. The extended field
# holds the character scale in percent in bits 14-23 (0 for none). Language entry i (1..15) at P3LT+i*64 is the attribute text of
# w:lang as it stands in the XML, zero ended; entry 16 is the scratch for a new one. The paragraph outline level is kept as
# (level+1)/32 in feat1's paragraph extras cell, below every threshold that reads its two flag bits.
P3LT=1197100; P3LS=64; P3NL=15; region('p3 languages',P3LT,P3LT+P3LS*(P3NL+2))
p3bit=R();p3n=R();p3nl=R();p3s=R();p3k=R();p3m=R();p3j=R();p3ol=R();p3wol=R()
p3wf=[R() for _ in range(4)]; p3wl=R(); p3ws=R()
def P3_PX(e):
    "Tags for p3, after feat1's."
    dx=net.eq(ztarget,4,e)
    return [(pat('<w:embos',e),'P3_TV',{p3bit:2,oi:oi+9}),(pat('<w:impri',e),'P3_TV',{p3bit:3,oi:oi+10}),(pat('<w:shado',e),'P3_TV',{p3bit:1,oi:oi+9}),
     (pat('<w:outli',e),'P3_OU',{oi:oi+10,rl:OA+oi+10}),(pat('<w:w w:v',e),'P3_SC',{oi:oi+12,p3n:0}),(net.and_(a4inr,pat('<w:lang ',e)),'P3_LG',{oi:oi+8})]
