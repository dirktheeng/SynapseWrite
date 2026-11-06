# ---- document canvas look (reviewer a2): list spacing, modal bars, balloon, picture handles ----
net.group('canvas look')
# list items of one list sit close together: the space after an item applies only when the next paragraph is no list item
on('A2_LS0',(None,'A2_LS1',{r1:as_x(PT)+pi+1}))
on('A2_LS1',(None,'A2_LS2',{r1:R1+LIST}))
on('A2_LS2',(net.step(R1),'R1',{pi:pi+1}),(None,'R1',{yy:yy+pspa,pi:pi+1}))
# the balloon card goes to the wrapped text writer one tick after its frame
on('A2_CB',(None,'T3_CB4',None))
# picture handles: round white dots, one per working grip
def a2_dot(st,xx,yy_,nx,acts=None):
    on(st,(None,nx,{rA:(xx+2,yy_,5,9,HC,0),rB:(xx,yy_+2,9,5,HC,0),rC:(xx+1,yy_+2,7,5,WHITE,0),rD:(xx+2,yy_+1,5,7,WHITE,0)}))
a2_dot('A2_PH0',x+pim-9,sy+pih-9,'A2_PH1')
a2_dot('A2_PH1',x+pim-9,sy+pih*0.5-4,'A2_PH2')
a2_dot('A2_PH2',x+pim*0.5-4,sy+pih-9,'CB0')
# modal bars: header and footer strings
t1_text('A2_HBa','Header',PX+8,DOCY+6,0,3,'TB0')
t1_text('A2_HBb','First Header',PX+8,DOCY+6,0,3,'TB0')
t1_text('A2_HBc','Footer',PX+8,DOCY+6,0,3,'TB0')
t1_text('A2_HBd','First Footer',PX+8,DOCY+6,0,3,'TB0')
_b=(160,160,160)
on('A2_HB0',(None,'HB',{rA:(PX+84,DOCY+3,676,1,_b,0),rB:(PX+84,DOCY+24,676,1,_b,0),rC:(PX+83,DOCY+3,1,22,_b,0),rD:(PX+760,DOCY+3,1,22,_b,0)}))
e=S('A2_HBE'); _h=net.decode(hfk,4,e)
on('A2_HBE',(_h[0],'A2_HBa',None),(_h[1],'A2_HBb',None),(_h[2],'A2_HBc',None),(None,'A2_HBd',None))
# modal bars: footnote and comment text, the tail that fits the field
a2i=R();a2n=R();a2b=R()
on('A2_NB0',(None,'A2_NB1',{rA:(PX+84,DOCY+3,676,1,_b,0),rB:(PX+84,DOCY+24,676,1,_b,0),rC:(PX+83,DOCY+3,1,22,_b,0),rD:(PX+760,DOCY+3,1,22,_b,0),r1:cb+CMTL,sx:PX+88}))
e=S('A2_NB1'); _m5=net.eq(mode,5,e)

on('A2_NB1',(_m5,'A2_NF',{a2n:flen,a2i:net.relu(flen-88),a2b:fedb}),(None,'A2_NC',{a2n:R1,a2i:net.relu(R1-88),a2b:cb+CMT}))
t1_text('A2_NF','Footnote',PX+8,DOCY+6,0,3,'A2_NL')
t1_text('A2_NC','Comment',PX+8,DOCY+6,0,3,'A2_NL')
on('A2_NL',(net.ge(a2i,a2n,S('A2_NL')),'TB0',{rD:(sx,DOCY+6,1,16,(0,0,0),0)}),(None,'A2_NR',{r1:a2b+a2i}))
on('A2_NR',(None,'A2_NL',{gly:(R1,0,sx,DOCY+4,0,0),sx:sx+adv,a2i:a2i+1}))
# rows of one table share a rule: the next row starts on this row's bottom rule, and text after the table starts below it
on('A2_TB0',(None,'A2_TB1',{r1:as_x(PT)+pi}))
on('A2_TB1',(None,'A2_TB2',{r1:R1+2062}))
on('A2_TB2',(net.step(R1),'R1',{yy:rowmax}),(None,'R1',{yy:rowmax+1}))
