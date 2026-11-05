"""Subsets the two openly licensed font families to the characters the editor can show, for
embedding as literal bytes. The bytes go out through a token chain like any other literal."""
import io,zlib
import rom
from fontTools.ttLib import TTFont
from fontTools import subset
ORDER=[(0,400,'normal','Carlito','Carlito'),(0,700,'normal','Carlito-Bold','Carlito'),(0,400,'italic','Carlito-Italic','Carlito'),(0,700,'italic','Carlito-BoldItalic','Carlito'),
       (1,400,'normal','Caladea','Caladea'),(1,700,'normal','Caladea-Bold','Caladea'),(1,400,'italic','Caladea-Italic','Caladea'),(1,700,'italic','Caladea-BoldItalic','Caladea')]
def objects(first_font,first_extra):
    """Returns {object number: bytes}. Fonts are numbered from first_font; descriptors and files from first_extra."""
    out={}
    for i,(fi,w,st,name,_) in enumerate(ORDER):
        f=TTFont(io.BytesIO(rom._load(rom.FAM[fi],w,st)))
        o=subset.Options();o.hinting=False;o.layout_features=[];o.name_IDs=[1];o.notdef_outline=True;o.drop_tables+=['GSUB','GPOS','GDEF','kern','meta','DSIG','FFTM']
        s=subset.Subsetter(o);s.populate(unicodes=list(range(32,127))+[0x2022]);s.subset(f)
        b=io.BytesIO();f.save(b);ttf=b.getvalue();zd=zlib.compress(ttf,9)
        upm=f['head'].unitsPerEm;cm=f.getBestCmap();hm=f['hmtx'];k=1000/upm
        wd=[round(hm[cm[c]][0]*k) if c in cm else 0 for c in range(32,127)]+[0]*22+[round(hm[cm[0x2022]][0]*k)]
        h=f['head'];hh=f['hhea'];tag='ABCDE'+chr(65+i)+'+'+name
        fo,de,ff=first_font+i,first_extra+i*2,first_extra+i*2+1
        out[fo]=(f'{fo} 0 obj\n<</Type/Font/Subtype/TrueType/BaseFont/{tag}/FirstChar 32/LastChar 149/Widths[{" ".join(map(str,wd))}]/Encoding/WinAnsiEncoding/FontDescriptor {de} 0 R>>\nendobj\n').encode()
        fl=32+(64 if st=='italic' else 0)
        out[de]=(f'{de} 0 obj\n<</Type/FontDescriptor/FontName/{tag}/Flags {fl}/FontBBox[{round(h.xMin*k)} {round(h.yMin*k)} {round(h.xMax*k)} {round(h.yMax*k)}]/ItalicAngle {-12 if st=="italic" else 0}/Ascent {round(hh.ascent*k)}/Descent {round(hh.descent*k)}/CapHeight {round(hh.ascent*k*0.8)}/StemV {120 if w==700 else 80}/FontFile2 {ff} 0 R>>\nendobj\n').encode()
        out[ff]=(f'{ff} 0 obj\n<</Length {len(zd)}/Length1 {len(ttf)}/Filter/FlateDecode>>\nstream\n').encode()+zd+b'\nendstream\nendobj\n'
    return out
