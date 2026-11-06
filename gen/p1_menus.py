# ---- p1: Insert > Symbol, a menu of common symbols (exec'd from t1_features.py with the other menus) ----
# Each row types its character through the typing path, so it takes the typing format and undoes like typing.
P1_SYM=[(169,'Copyright'),(174,'Registered'),(153,'Trade mark'),(128,'Euro'),(163,'Pound'),(165,'Yen'),(167,'Section'),(182,'Paragraph'),
 (176,'Degree'),(177,'Plus or minus'),(215,'Multiply'),(247,'Divide'),(133,'Ellipsis'),(149,'Bullet'),(189,'One half'),(188,'One quarter')]

def _p1sym(u,r_,x,y): u.t(x+8,y+2,chr(P1_SYM[r_][0]),9,0,0,True); u.t(x+30,y+2,P1_SYM[r_][1],9,0,0,True)
t1_menu(16,P1_SYX,P1_SYY,150,[n_ for _,n_ in P1_SYM],_p1sym)
def p1_sym_rules(mc,CM): return [(mc(16,r_),'TYPE',{eva:c_,**CM}) for r_,(c_,_) in enumerate(P1_SYM)]
