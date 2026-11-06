# rv_a6: math in a file. m:t runs become equation characters; a built up form comes in as its linear form.
# feat2: every math tag is caught by two prefix patterns, '<m:' and '</m:', and told apart in its own state (gen/feat2_eqrd.py), so the shared window gains no thresholds.
a6es=R();a6ec=R()
def A6_PX_RULES(e):
    return [(pat('</m:',e),'F2R_1',{rl:OA+oi+4}),(pat('<m:',e),'F2R_0',{rl:OA+oi+3})]
a6qrr=t3ret('A6Q_RR');a6qi=R();a6qa=R();a6qcv=R();a6qn=R()
EQT=1330000; EQR=64; EQC0=300
# feat2 reader registers: pending keyword at the next m:e (1 sqrt, 2 hat, 3 bar, 4 tilde, 5 dot, 6 vec, 7 left(, 8 left[, 9 left|), the closing delimiter,
# inside an n-ary (and its symbol: 1 sum, 2 product, 3 integral), inside a matrix with its row and cell counts, and the string being typed.
a6kw=R();a6de=R();a6nx=R();a6ns=R();a6mx=R();a6mr=R();a6mc=R();f2ep=R();f2el=R()
