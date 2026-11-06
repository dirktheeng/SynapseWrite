"""Tier 3 ribbon commands. Each has its own raw object id within its tab, so each gets a hover highlight.
Ids are looked up with the tab in the BTN rules. Raw ids below 9 on Layout and View are remapped, so they are not used here."""
from app_pal import B as _B
# (tab,id,x,y,w,h,label,state,swatch color or None)
BTNS=[]
def add(tab,id_,x,y,w,h,label,state,color=None): BTNS.append((tab,id_,x,y,w,h,label,state,color))
R0,R1,R2=64,86,108; RH=21
ICONS={}   # (tab,id) to a small icon drawn left of the label
def addi(tab,id_,x,y,w,label,state,icon): add(tab,id_,x,y,w,RH,label,state); ICONS[(tab,id_)]=icon
# Insert: table tools and header, footer
X=70
for i,(lb,st,ic) in enumerate((('Row Above','T3_C_RA','rowa'),('Row Below','T3_C_RB','rowb'),('Delete Row','T3_C_DR','rowd'))): addi(1,8+i,X,R0+22*i,84,lb,st,ic)
X=156
for i,(lb,st,ic) in enumerate((('Col Left','T3_C_CL','cola'),('Col Right','T3_C_CR','colb'),('Delete Col','T3_C_DC','cold'))): addi(1,11+i,X,R0+22*i,76,lb,st,ic)
SH=[(0,_B[0]),(2,_B[2]),(5,_B[5]),(13,_B[13]),(14,_B[14]),(15,_B[15])]
for i,(k,c) in enumerate(SH): add(1,14+i,242+(i%2)*24,R0+(i//2)*22,22,RH,'','T3_C_S%d'%k,c)
X=364
addi(1,20,X,R0+22,94,'Footer','T3_C_F0','foot'); addi(1,21,X+96,R0,106,'First Header','T3_C_H1','head1'); addi(1,22,X+96,R0+22,106,'First Footer','T3_C_F1','foot1')
addi(1,23,X,R0+44,94,'Page Number','T3_C_PG','pgnum'); addi(1,24,X+96,R0+44,106,'No First Page','T3_C_NF','nofirst')
# Layout: orientation, margins, section break
addi(2,10,60,R0,84,'Portrait','T3_C_POR','port'); addi(2,11,60,R0+22,84,'Landscape','T3_C_LAN','land')
addi(2,12,146,R0,70,'Normal','T3_C_MN','mnorm'); addi(2,13,146,R0+22,70,'Narrow','T3_C_MS','mnar'); addi(2,14,146,R0+44,70,'Wide','T3_C_MW','mwide')
addi(3,8,74,R0,102,'Update Table','T3_C_TU','refresh')
addi(4,8,124,R0,118,'Delete Comment','T3_C_CD','delcmt')
add(3,9,74,R0+22,102,RH,'Merge Field','A6_MF')

# View: zoom and read mode
for i_,(lb_,st_) in enumerate((('Zoom In','IMP3_ZI'),('Zoom Out','IMP3_ZO'),('100%','IMP3_Z100'))): add(5,10+i_,170,R0+22*i_,84,RH,lb_,st_)
for i_,(lb_,st_) in enumerate((('One Page','IMP3_ZP'),('Page Width','IMP3_ZW'),('Read Mode','IMP3_RE'))): add(5,13+i_,256,R0+22*i_,94,RH,lb_,st_)

# Commands that already exist in the network and had no button
add(1,6,1058,R0,92,RH,'Page Break','PB0')
add(4,9,392,R0,84,RH,'Show Marks','IMP3_MK')
