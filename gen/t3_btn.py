"""Tier 3 ribbon commands. All use button id 54; the network tells them apart by tab, x and y."""
# (tab,x,y,w,h,label,state,swatch color or None)
BTNS=[]
GROUPS=[]
def add(tab,x,y,w,h,label,state,color=None): BTNS.append((tab,x,y,w,h,label,state,color))
x0=410
add(1,x0,64,64,24,'Row Above','T3_C_RA'); add(1,x0+66,64,64,24,'Row Below','T3_C_RB')
add(1,x0+132,64,56,24,'Col Left','T3_C_CL'); add(1,x0+190,64,60,24,'Col Right','T3_C_CR')
add(1,x0,90,64,24,'Del Row','T3_C_DR'); add(1,x0+66,90,64,24,'Del Col','T3_C_DC')
SH=[(0,(255,255,255)),(2,(255,242,171)),(5,(217,217,217)),(6,(198,224,180)),(7,(189,215,238)),(8,(248,203,173))]
for i,(k,c) in enumerate(SH): add(1,x0+132+i*20,90,18,24,'','T3_C_S%d'%k,c)
GROUPS.append((1,x0,250,'Table Tools'))
add(2,180,64,70,24,'Portrait','T3_C_POR'); add(2,252,64,70,24,'Landscape','T3_C_LAN'); GROUPS.append((2,180,142,'Orientation'))
add(2,334,64,56,24,'Normal','T3_C_MN'); add(2,392,64,56,24,'Narrow','T3_C_MS'); add(2,450,64,56,24,'Wide','T3_C_MW'); GROUPS.append((2,334,172,'Margins'))
add(2,518,64,90,24,'Section Break','T3_C_SB'); GROUPS.append((2,518,90,'Sections'))
