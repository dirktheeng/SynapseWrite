# ---- reviewer a4: paragraph cells and registers needed before the layout network is written ----
# Slot cells past the comment text: tab stops 4084-4087 (px + kind*4096, 0 none; kind 0 left, 1 center, 2 right),
# keep next 4090, keep lines 4091, border bits 4092 (1 top, 2 bottom, 4 left, 8 right), header row 4093, right indent px 4094.
A4T=4084;A4C=4088;A4K=4090;A4L=4091;A4B=4092;A4H=4093;A4R=4094
ra4=RPort(8);ra4t=RPort(4);A4O=ra4.out;A4TO=ra4t.out
a4da=R();a4rS=R();a4rR=R();a4rF=R();a4m=[R() for _ in range(4)];a4dl=R();a4lt=R();a4rc=R();a4k=R();a4l=R();a4b=R();a4hf=R();a4rr=R();a4kf=R();a4kd=R();a4kbr=R();a4la=R();a4kp=R()
a4fp=R();a4fs=R();a4fpp=R();a4fst=R();a4fps=R();a4ff=[R() for _ in range(7)];a4cw=R();a4cm=R();a4ws=R();a4ss=R();a4cfk=R();a4cfq=R();a4sha=R()
a4wk=R();a4wl=R();a4wb=R();a4wr=R();a4wt=[R() for _ in range(4)];a4inb=R();a4inr=R();a4rsn=R();a4rbb=R();a4rk=R();a4roi=R();a4rsk=R()
def A4_META(e):
    return {a4kf:net.and_(e,net.or_(net.step(A4O[2]),net.step(A4O[3]),net.and_(net.ge(rp6.out[5],2,e),net.lt(rp6.out[5],5,e)))),a4k:net.and_(e,net.or_(net.step(A4O[2]),net.and_(net.ge(rp6.out[5],2,e),net.lt(rp6.out[5],5,e)))),a4b:A4O[4],a4hf:A4O[5],a4rr:A4O[6]}
def A4_R9():
    e=S('R9'); return net.and_(e,ONE-net.step(tcols),net.or_(net.step(pbg),net.step(a4b)),net.or_(full,net.eq(pi,cp,e),net.eq(pi,oldcp,e)))
def A4_W4(e):
    global a4wp_,a4wo_
    a4wp_,a4wo_=wp,wo
    "Change case, one character of the range walker. Case differs by 32 in both ASCII and Latin-1."
    c3=net.and_(e,net.eq(wm,3,e))
    isup=net.or_(net.and_(net.ge(R1,65,c3),net.lt(R1,91,c3)),net.and_(net.ge(R1,192,c3),net.lt(R1,223,c3),ONE-net.eq(R1,215,c3)))
    islo=net.or_(net.and_(net.ge(R1,97,c3),net.lt(R1,123,c3)),net.and_(net.ge(R1,224,c3),net.lt(R1,255,c3),ONE-net.eq(R1,247,c3)))
    hm=net.decode(a4cm,5,c3)   # 0 sentence, 1 lower, 2 upper, 3 title, 4 toggle
    toU=net.or_(net.and_(islo,hm[2]),net.and_(islo,hm[4]),net.and_(islo,hm[0],a4ss),net.and_(islo,hm[3],a4ws))
    toL=net.or_(net.and_(isup,hm[1]),net.and_(isup,hm[4]),net.and_(isup,hm[0],ONE-a4ss),net.and_(isup,hm[3],ONE-a4ws))
    chg=net.or_(toU,toL); log(chg,8,wp,wo,R1,0); w1.drive(chg,(wbase+wo,R1+toL*32-toU*32)); w3.drive(chg,(wbase+DIRTY,1))
    fsm.set(a4ws,c3,c3-t1_isw(R1,c3))
    fsm.set(a4ss,net.or_(net.eq(R1,46,c3),net.eq(R1,33,c3),net.eq(R1,63,c3)),1); fsm.set(a4ss,net.or_(isup,islo),0)
    fsm.set(a4ws,S('WNL'),1); fsm.set(a4ss,S('WNL'),1)
def A4_PX(e):
    "XML tags for the paragraph properties of this reviewer."
    return [(pat('<w:rPr>',e),'PX',{a4inr:1,oi:oi+7}),(pat('</w:rPr>',e),'PX',{a4inr:0,oi:oi+8}),(net.and_(a4inr,pat('<w:shd ',e)),'PX',{oi:oi+7}),
     (pat('<w:keepN',e),'A4_RK0',{a4rk:A4K,oi:oi+11}),(pat('<w:keepL',e),'A4_RK0',{a4rk:A4L,oi:oi+12}),
     (pat('<w:pBdr>',e),'PX',{a4inb:1,oi:oi+8}),(pat('</w:pBdr',e),'PX',{a4inb:0,oi:oi+8}),
     (net.and_(a4inb,pat('<w:top ',e)),'A4_RB0',{a4rbb:1,oi:oi+7}),(net.and_(a4inb,pat('<w:botto',e)),'A4_RB0',{a4rbb:2,oi:oi+8}),
     (net.and_(a4inb,pat('<w:left ',e)),'A4_RB0',{a4rbb:4,oi:oi+8}),(net.and_(a4inb,pat('<w:right',e)),'A4_RB0',{a4rbb:8,oi:oi+8}),
     (pat('<w:tab ',e),'A4_RS0',{a4roi:oi+7,oi:oi+7})]
