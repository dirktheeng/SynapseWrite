"""Ribbon commands past the 8 bit id space. They all draw with alpha 235 inside the ribbon, and the network picks the command from
the pointer position, so each has its own hover key (235+100*(index+1)) and its own highlight."""
EXT=235
# (tab,x,y,w,h,label,state,icon,color)
BTNS=[]
def add(tab,x,y,w,h,label,state,icon=None,color=None): BTNS.append((tab,x,y,w,h,label,state,icon,color))
add(0,54,108,52,21,'Painter','A4_FP','paint')
add(0,112,115,58,15,'Aa Case','A4_CM'); add(0,172,115,76,15,'Clear Format','A4_CF')
add(1,826,64,54,62,'Table','A4_GO','table')
add(1,884,64,70,21,'Merge','A4_MG'); add(1,884,86,70,21,'Split','A4_SPL'); add(1,884,108,70,21,'Header Row','A4_HB'); add(1,958,64,90,21,'Number Format','A4_PG')
add(2,840,64,76,21,'Keep Next','A4_TK'); add(2,840,86,76,21,'Keep Lines','A4_TL'); add(2,840,108,76,21,'Page Before','A4_TP')
add(2,922,64,56,21,'Box','A4_BD15'); add(2,922,86,56,21,'Bottom','A4_BD2'); add(2,922,108,56,21,'Top','A4_BD1'); add(2,980,64,66,21,'No Border','A4_BD0')
from app_pal import B as _B
for i,k in enumerate((0,2,5,13,14,15)): add(2,980+(i%3)*22,86+(i//3)*22,21,21,'','A4_SH%d'%k,None,_B[k])
LABELS=[(2,840,76,'Pagination'),(2,922,124,'Borders, Shading')]
LABELS1=[(1,826,128,'Table Tools'),(1,958,90,'Page Numbers')]
