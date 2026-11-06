"""Tier 3 ribbon commands. They share one raw object id per tab (TB(RAW,tab) in the BTN rules); the network tells them apart by tab, x and y.
Raw ids 54, 55 and 35 are global for Tier 1, so RAW is one that only the Home tab uses for itself. These buttons have no hover highlight, as an id highlights as a whole."""
from app_pal import B as _B
RAW=9
# (tab,x,y,w,h,label,state,swatch color or None)
BTNS=[]
GROUPS=[]
def add(tab,x,y,w,h,label,state,color=None): BTNS.append((tab,x,y,w,h,label,state,color))
x0=770
add(1,x0,64,64,24,'Row Above','T3_C_RA'); add(1,x0+66,64,64,24,'Row Below','T3_C_RB')
add(1,x0+132,64,56,24,'Col Left','T3_C_CL'); add(1,x0+190,64,60,24,'Col Right','T3_C_CR')
add(1,x0,90,64,24,'Del Row','T3_C_DR'); add(1,x0+66,90,64,24,'Del Col','T3_C_DC')
# palette index of each shade
SH=[(0,_B[0]),(2,_B[2]),(5,_B[5]),(13,_B[13]),(14,_B[14]),(15,_B[15])]
for i,(k,c) in enumerate(SH): add(1,x0+132+i*20,90,18,24,'','T3_C_S%d'%k,c)
GROUPS.append((1,x0,250,'Table Tools'))
L0=964
add(2,L0,64,70,24,'Portrait','T3_C_POR'); add(2,L0+72,64,70,24,'Landscape','T3_C_LAN'); add(2,L0+146,64,90,24,'Section Break','T3_C_SB')
add(2,L0,90,56,24,'Normal','T3_C_MN'); add(2,L0+58,90,56,24,'Narrow','T3_C_MS'); add(2,L0+116,90,56,24,'Wide','T3_C_MW'); GROUPS.append((2,L0,236,'Orientation, Margins, Sections'))
F0=1030
add(1,F0,64,64,24,'Footer','T3_C_F0'); add(1,F0+66,64,84,24,'First Header','T3_C_H1'); add(1,F0+152,64,84,24,'First Footer','T3_C_F1')
add(1,F0,90,64,24,'Page #','T3_C_PG'); add(1,F0+66,90,84,24,'No First Page','T3_C_NF'); GROUPS.append((1,F0,236,'Header and Footer'))
add(3,8,90,122,24,'Update Table','T3_C_TU')
add(4,8,90,100,24,'Delete Comment','T3_C_CD')
