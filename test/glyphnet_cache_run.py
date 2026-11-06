"""Cache hit path on the real engine for a typical small and large glyph. Also verifies the framebuffer has ink."""
from glyphnet_common import *
for pt,W,H in ((11,rom.SW,rom.SH),(36,rom.LW,rom.LH)):
    gn.cache_blit_net(W,H,f'{OUT}/blit{W}.bin.gz')
    res,_,_=run('carlito',[draw(ord('m'),0,pt,(1,1),fi=0)]); G=geom(pt); c=pad(res[0],G).astype(np.float32); c.tofile(f'{OUT}/cov{W}.f32')
    print(pt,'ink cells',int((c>0).sum()),subprocess.check_output(['node','test/glyphnet_cache.js',f'{OUT}/blit{W}.bin.gz',f'{OUT}/cov{W}.f32',str(W),str(H),'20000'],cwd=ROOT).decode())
