# ---- imp4: list formats. A LIST cell holds kind+4*level+16*format. Format 0 is the look fixed by level, as before. ----
from docx_tpl import LFMT
lfm=R();v6qf=R();v6nf=R()
LFX=1090; LFY=127
LF_LABELS=[l_ for *_,l_ in LFMT]
def list_mark(f_,en):
    "What a format means, as lines over its number: marker table, capitals, opening character, closing character, bullet."
    h=net.decode(f_,len(LFMT)+1,net.and_(en,net.step(f_))); t_=u_=p_=s_=b_=X()
    for i_,(tb,up,pre,suf,bul,_) in enumerate(LFMT):
        l_=h[i_+1]
        t_=t_+l_*tb; u_=u_+l_*up; p_=p_+l_*pre; s_=s_+l_*suf; b_=b_+l_*bul
    return t_,u_,p_,s_,b_
