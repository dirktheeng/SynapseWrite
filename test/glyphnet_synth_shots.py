"""Real faces against one regular outline plus the shear layer and the bold offset."""
from glyphnet_shots import *
rows=[]
for fi,fam in enumerate(('carlito','caladea')):
  for lab,fl,real in (('bold',dict(bold=1),(fi,1,0)),('italic',dict(slant=1),(fi,0,1)),('bold italic',dict(bold=1,slant=1),(fi,1,1))):
    for pt in (11,18):
      G=geom(pt,fi); o,wd=layout(real,pt,TEXT); wd+=4; H=G['rows']+2
      A=np.zeros((H,wd));B=A.copy(); idx=[(0,1,0),(0,0,1),(0,1,1)].index(real[0:0]+(0,)+real[1:]) if 0 else 0
      F4=[(fi,b,i) for b in (0,1) for i in (0,1)]
      r1,_,_=run(fam,[draw(k,F4.index(real),pt,(0,0),fi=fi) for k,_,_ in o]); r2,_,_=run(fam+'_synth',[draw(k,0,pt,(0,0),fi=fi,**fl) for k,_,_ in o])
      for i,(k,x,_) in enumerate(o): blit(A,pad(r1[i],G),x); blit(B,pad(r2[i],G),x)
      rows+=[(f'{fam} {pt} real {lab}',A),(f'{fam} {pt} synthetic {lab}',B)]
W=max(a.shape[1] for _,a in rows)*3+170; im=Image.new('L',(W,sum(a.shape[0]*3+3 for _,a in rows)),255); d=ImageDraw.Draw(im); y=0
for l,a in rows: d.text((2,y+a.shape[0]),l,fill=90,font=LB); im.paste(line_img(a),(166,y)); y+=a.shape[0]*3+3
im.crop((0,0,W,im.size[1]//2)).save(ROOT+'/shots/glyph_synth_carlito.png'); im.crop((0,im.size[1]//2,W,im.size[1])).save(ROOT+'/shots/glyph_synth_caladea.png')
