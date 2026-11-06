# Exact colors, font names and character styles. A style table entry is four cells: the record, the exact color plus one, the font name id, the character style id plus one.
STYX=1120000; FNT=1125000; FNSEED=['Caladea','Cambria','Arimo','Arial','Tinos','Times New Roman','Cousine','Courier New','Open Sans','Oswald','Caveat','Carlito','Calibri']; FNSD=len(FNSEED); FNMAXN=64
region('STYX style exact color and font name',STYX,STYX+4*200); region('FNT font names',FNT,FNT+32*FNMAXN)
PRB=1127100; PRMAX=40; FTB=1127200; region('prompt bar text',PRB,PRB+PRMAX+1); region('typed font name',FTB,FTB+PRMAX+16)
fck=R();fnx=R();fpk=R();fpn=R();fpy=R();v4fk=R();v4fn=R();v4fy=R();v4uk=R();v4un=R();v4ok=R()
prk=R();prl=R();v4h=R();v4i=R();v4j=R();v4ty=R();v4fc=R(FNSD+1);t2kx=R();t2nx=R();t2pK=R();t2pN=R();v4qk=R();ptk_q=R();ins_k=R();ins_n=R();ins_y=R()
vrt=R();vrm=R();vrh=R();vrc=R();hsv=R();hsmax=R();v8u=R();v8tx=R();v8tw=R();v4f=R();qxp=R();v4c=R();v4nosz=R();ysr=R();ymsk=R();v5n=R();v5i=R();v5j=R();v5k=R();v4m=[R() for _ in range(9)]
