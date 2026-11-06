"""Tier 3 ribbon commands. Each has its own raw object id within its tab, so each gets a hover highlight.
Ids are looked up with the tab in the BTN rules. Raw ids below 9 on Layout and View are remapped, so they are not used here."""
from app_pal import B as _B
# (tab,id,x,y,w,h,label,state,swatch color or None)
BTNS=[]
def add(tab,id_,x,y,w,h,label,state,color=None): BTNS.append((tab,id_,x,y,w,h,label,state,color))
R0,R1,R2=64,86,108; RH=21
# Insert: table tools and header, footer
X=84
for i,(lb,st) in enumerate((('Row Above','T3_C_RA'),('Row Below','T3_C_RB'),('Delete Row','T3_C_DR'))): add(1,8+i,X,R0+22*i,76,RH,lb,st)
X=162
for i,(lb,st) in enumerate((('Col Left','T3_C_CL'),('Col Right','T3_C_CR'),('Delete Col','T3_C_DC'))): add(1,11+i,X,R0+22*i,70,RH,lb,st)
SH=[(0,_B[0]),(2,_B[2]),(5,_B[5]),(13,_B[13]),(14,_B[14]),(15,_B[15])]
for i,(k,c) in enumerate(SH): add(1,14+i,236+(i%2)*24,R0+(i//2)*22,22,RH,'','T3_C_S%d'%k,c)
X=380
add(1,20,X,R0+22,84,RH,'Footer','T3_C_F0'); add(1,21,X+86,R0,100,RH,'First Header','T3_C_H1'); add(1,22,X+86,R0+22,100,RH,'First Footer','T3_C_F1')
add(1,23,X,R0+44,84,RH,'Page Number','T3_C_PG'); add(1,24,X+86,R0+44,100,RH,'No First Page','T3_C_NF')
# Layout: orientation, margins, section break
add(2,10,62,R0,78,RH,'Portrait','T3_C_POR'); add(2,11,62,R0+22,78,RH,'Landscape','T3_C_LAN')
add(2,12,142,R0,60,RH,'Normal','T3_C_MN'); add(2,13,142,R0+22,60,RH,'Narrow','T3_C_MS'); add(2,14,142,R0+44,60,RH,'Wide','T3_C_MW')
add(3,8,74,R0,92,RH,'Update Table','T3_C_TU')
add(4,8,120,R0+22,104,RH,'Delete Comment','T3_C_CD')
