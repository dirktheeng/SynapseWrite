"""Subsets the two openly licensed font families to the characters the editor can show, for
embedding as literal bytes. The bytes go out through a token chain like any other literal."""
import io,zlib
import rom
from fontTools.ttLib import TTFont
from fontTools import subset
ORDER=[(0,400,'normal','Carlito','Carlito'),(0,700,'normal','Carlito-Bold','Carlito'),(0,400,'italic','Carlito-Italic','Carlito'),(0,700,'italic','Carlito-BoldItalic','Carlito'),
       (1,400,'normal','Caladea','Caladea'),(1,700,'normal','Caladea-Bold','Caladea'),(1,400,'italic','Caladea-Italic','Caladea'),(1,700,'italic','Caladea-BoldItalic','Caladea')]
WANT={c:ord(rom.cp1252(c)) for c in rom.CODES if c!=127}    # WinAnsi code to unicode
def _graft(f,x,uni,o):
    "Adds glyphs from the Latin extended file of the same face to the subset."
    s=subset.Subsetter(o);s.populate(unicodes=sorted(uni&set(x.getBestCmap())));s.subset(x)
    gl=f['glyf'];xg=x['glyf'];xc=x.getBestCmap();nm=lambda g:'x_'+g
    for g in x.getGlyphOrder():
        if g=='.notdef': continue
        gg=xg[g]
        if gg.isComposite():
            for comp in gg.components: comp.glyphName=nm(comp.glyphName)
        gl[nm(g)]=gg; f['hmtx'][nm(g)]=x['hmtx'][g]
    f.setGlyphOrder(gl.glyphOrder)
    f['post'].formatType=3.0
    for t in f['cmap'].tables:
        if t.isUnicode():
            for u,g in xc.items(): t.cmap[u]=nm(g)
def objects(first_font,first_extra):
    """Returns {object number: bytes}. Fonts are numbered from first_font; descriptors and files from first_extra."""
    out={}
    for i,(fi,w,st,name,_) in enumerate(ORDER):
        f=TTFont(io.BytesIO(rom._load(rom.FAM[fi],'latin',w,st)))
        want=set(WANT.values())|{0x2022}
        o=subset.Options();o.hinting=False;o.layout_features=[];o.name_IDs=[1];o.notdef_outline=True;o.drop_tables+=['GSUB','GPOS','GDEF','kern','meta','DSIG','FFTM']
        s=subset.Subsetter(o);s.populate(unicodes=sorted(want&set(f.getBestCmap())));s.subset(f)
        rest=want-set(f.getBestCmap())
        if rest: _graft(f,TTFont(io.BytesIO(rom._load(rom.FAM[fi],'latin-ext',w,st))),rest,o)
        b=io.BytesIO();f.save(b);ttf=b.getvalue();zd=zlib.compress(ttf,9)
        upm=f['head'].unitsPerEm;cm=f.getBestCmap();hm=f['hmtx'];k=1000/upm
        wd=[round(hm[cm[WANT[c]]][0]*k) if c in WANT and WANT[c] in cm else 0 for c in range(32,256)]
        h=f['head'];hh=f['hhea'];tag='ABCDE'+chr(65+i)+'+'+name
        fo,de,ff=first_font+i,first_extra+i*2,first_extra+i*2+1
        out[fo]=(f'{fo} 0 obj\n<</Type/Font/Subtype/TrueType/BaseFont/{tag}/FirstChar 32/LastChar 255/Widths[{" ".join(map(str,wd))}]/Encoding/WinAnsiEncoding/FontDescriptor {de} 0 R>>\nendobj\n').encode()
        fl=32+(64 if st=='italic' else 0)
        out[de]=(f'{de} 0 obj\n<</Type/FontDescriptor/FontName/{tag}/Flags {fl}/FontBBox[{round(h.xMin*k)} {round(h.yMin*k)} {round(h.xMax*k)} {round(h.yMax*k)}]/ItalicAngle {-12 if st=="italic" else 0}/Ascent {round(hh.ascent*k)}/Descent {round(hh.descent*k)}/CapHeight {round(hh.ascent*k*0.8)}/StemV {120 if w==700 else 80}/FontFile2 {ff} 0 R>>\nendobj\n').encode()
        out[ff]=(f'{ff} 0 obj\n<</Length {len(zd)}/Length1 {len(ttf)}/Filter/FlateDecode>>\nstream\n').encode()+zd+b'\nendstream\nendobj\n'
    return out
