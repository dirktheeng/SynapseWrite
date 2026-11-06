# rv_a6: math in a file. m:t runs become equation characters; a fraction or a root comes in as its linear form.
a6es=R();a6ec=R()
def A6_PX_RULES(e):
    return [(pat('<m:r>',e),'PX',{ics:t2ps,rnop:0,oi:oi+5}),(net.or_(pat('<m:t>',e),pat('<m:t ',e)),'A6E_R0',{oi:oi+4}),
     (pat('<m:sup>',e),'PX',{a6es:1,oi:oi+7}),(pat('</m:sup>',e),'PX',{a6es:0,oi:oi+8}),(pat('<m:sub>',e),'PX',{a6es:2,oi:oi+7}),(pat('</m:sub>',e),'PX',{a6es:0,oi:oi+8}),
     (pat('<m:num>',e),'A6E_I1',{oi:oi+7,a6ec:40}),(pat('</m:num>',e),'A6E_I2',{oi:oi+8,a6ec:41}),(pat('<m:den>',e),'A6E_I1',{oi:oi+7,a6ec:40}),(pat('</m:den>',e),'A6E_I1',{oi:oi+8,a6ec:41}),
     (pat('<m:rad>',e),'A6E_Ra',{oi:oi+7}),(pat('</m:rad>',e),'A6E_I1',{oi:oi+8,a6ec:41}),(pat('</m:oMat',e),'A6Q_S0',{oi:oi+10,a6qi:0,a6qa:0,a6qcv:0,a6qrr.r:a6qrr.id('PX')})]
a6qrr=t3ret('A6Q_RR');a6qi=R();a6qa=R();a6qcv=R();a6qn=R()
EQT=1330000; EQR=64; EQC0=300
